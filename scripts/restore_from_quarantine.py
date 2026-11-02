#!/usr/bin/env python3
r"""Restore sheet-approved clips from quarantine back onto the searchable shelf.

The inverse of quarantine_theme.py, and deliberately narrower: it takes an explicit
verdicts file (written after a HUMAN read a labeled contact sheet — never from a gate
alone), moves only rows verdict=="accept", and rewrites each ledger row's file_path the
same tmp-then-replace way quarantine_theme.py does. Nothing is deleted; a rejected row
stays in quarantine with its provenance.

Verdicts file: JSON {index: {"id":..., "file_path":..., "verdict": "accept"|"reject",
"reason": ...}}. file_path must be under _quarantine; the restore target is
E:\pd-archive\<theme>\<name> (same drive as the quarantine, so the move is a rename).

    py -3.11 scripts/restore_from_quarantine.py runs/qc/quarantine_restore_20260825/verdicts.json
    py -3.11 scripts/restore_from_quarantine.py ... --apply
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

LEDGER_DIR = Path(r"E:\pd-archive\_ledger")
QUARANTINE = Path(r"E:\pd-archive\_quarantine")
SHELF = Path(r"E:\pd-archive")


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("verdicts")
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()

    verdicts = json.loads(Path(a.verdicts).read_text(encoding="utf-8"))
    accept_by_path = {}
    for rec in verdicts.values():
        if rec.get("verdict") == "accept":
            accept_by_path[str(Path(rec["file_path"]))] = rec

    moved = missing = 0
    for ledger in sorted(LEDGER_DIR.glob("*.jsonl")):
        rows = []
        changed = False
        for line in ledger.read_text(encoding="utf-8", errors="replace").splitlines():
            if not line.strip():
                continue
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                rows.append(line)
                continue
            fp = str(Path(str(r.get("file_path", ""))))
            rec = accept_by_path.get(fp)
            if rec:
                src = Path(fp)
                theme = src.parent.name
                dst = SHELF / theme / src.name
                if not src.is_file():
                    print(f"  MISSING: {src}")
                    missing += 1
                elif a.apply:
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(src), str(dst))
                    r["file_path"] = str(dst)
                    changed = True
                    moved += 1
                    print(f"  restored: {theme}/{src.name}")
                else:
                    moved += 1
                    print(f"  would restore: {theme}/{src.name}")
            rows.append(json.dumps(r, ensure_ascii=False) if not isinstance(r, str) else r)
        if a.apply and changed:
            tmp = ledger.with_suffix(".jsonl.restore_tmp")
            tmp.write_text("\n".join(rows) + "\n", encoding="utf-8")
            tmp.replace(ledger)

    verb = "restored" if a.apply else "would restore"
    print(f"\n{verb} {moved} file(s); {missing} missing")
    if not a.apply:
        print("(dry run -- nothing moved; add --apply)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
