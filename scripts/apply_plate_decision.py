#!/usr/bin/env python3
"""Write a reviewer's plate decision into the scaffolded verdict file.

`check_plate_verdicts.py --scaffold` writes one `unresolved` row per plate, bound to that
plate's sha256. Filling 131 rows by hand is how a verdict ends up on the wrong id, so this
takes {reject: {id: why}, note: {id: text}} -- ids as they are printed on the review sheet,
with or without the .png -- and resolves EVERY remaining row to `accept`.

It refuses when a decision names an id the verdict file does not carry, and it never
touches a plate's sha256: the binding stays whatever --scaffold measured, so a plate that is
regenerated after this run comes back as unresolved, which is the whole point of the binding.

    py -3.11 scripts/apply_plate_decision.py --slug keybridge \
        --decision runs/qc/keybridge_plate_decision.v001.json
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _key(i: str) -> str:
    return i if i.endswith(".png") else f"{i}.png"


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--decision", required=True)
    ap.add_argument("--verdicts")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    vp = Path(a.verdicts) if a.verdicts else ROOT / "runs" / "qc" / f"{a.slug}_plate_verdicts.v001.json"
    doc = json.loads(vp.read_text(encoding="utf-8"))
    dec = json.loads(Path(a.decision).read_text(encoding="utf-8"))
    plates = doc["plates"]

    reject = {_key(k): v for k, v in (dec.get("reject") or {}).items()}
    notes = {_key(k): v for k, v in (dec.get("note") or {}).items()}
    unknown = sorted((set(reject) | set(notes)) - set(plates))
    if unknown:
        for u in unknown:
            print(f"  decision names a plate the verdict file does not carry: {u}")
        print(f"[plates] refusing to write {vp.name}")
        return 1

    n_rej = n_acc = 0
    for name, row in plates.items():
        if name in reject:
            row["verdict"], row["note"] = "reject", reject[name]
            n_rej += 1
        else:
            row["verdict"] = "accept"
            if name in notes:
                row["note"] = notes[name]
            n_acc += 1
    doc.setdefault("plate_review", {})
    # KEEP the scaffold's reviewer when the decision file does not name one. The old default
    # of "unknown" OVERWROTE it, so a reviewer who scaffolded with --reviewer and then applied
    # a decision json without repeating the name erased the only record of who looked. Found
    # on EP83 max737, 2026-08-27, by the reviewer who had to write their own name back in.
    prev_reviewer = doc["plate_review"].get("reviewer")
    doc["plate_review"].update({
        "reviewer": dec.get("reviewer") or prev_reviewer or "unknown",
        "reviewed_at": date.today().isoformat(),
        "method": dec.get("_note", ""),
    })
    if a.dry_run:
        print(f"[plates] DRY RUN: would accept {n_acc}, reject {n_rej}")
        return 0
    vp.write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[plates] {a.slug}: {n_acc} accepted ({len(notes)} with a note), {n_rej} rejected -> {vp.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
