#!/usr/bin/env python3
"""Write the per-item licence verdicts back into the ledger.

`resolve_item_licences.py` asks each source what the licence actually is and writes
`runs/item_licence_verdicts.v001.json`. This applies it:

  free    -> pd                the source itself says CC0 / public domain / no known restrictions
  held    -> stays held        CC-BY or stricter, or NARA's "Undetermined" / "Restricted"
  unknown -> untouched         the lookup did not answer (rate limit, 403, no match). NOT a no --
                               re-run the resolver later and these become decidable.

`held` rows get `rights_verdict: "reject"` so a later pass can see they were examined and
refused. `unknown` rows are left exactly as they were, with no verdict, so the next run still
picks them up. That distinction is the whole point: a rate limit must not look like a decision.

STOP any ingest before running: it appends to these same files and has no lock of its own.

    py -3.11 scripts/apply_item_licence_verdicts.py --dry-run
    py -3.11 scripts/apply_item_licence_verdicts.py --stamp 2026-09-02T12:00:00
"""
from __future__ import annotations

import argparse
import collections
import glob
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ingest_archive_sources import LEDGER_DIR  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
VERDICTS = ROOT / "runs" / "item_licence_verdicts.v001.json"


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--stamp", default="")
    args = ap.parse_args()
    if not args.dry_run and not args.stamp:
        sys.exit("--stamp is required for a real run, so the change is dated in the ledger")

    data = json.loads(VERDICTS.read_text("utf-8"))
    plan: dict[tuple[str, str], dict] = {}
    for src, rows in data.items():
        for r in rows:
            if r["verdict"] in ("free", "held"):
                plan[(src, r["id"])] = r
    print(f"{len(plan)} decided row(s) in the verdict file")

    counts: collections.Counter = collections.Counter()
    for path in sorted(glob.glob(os.path.join(LEDGER_DIR, "*.jsonl"))):
        out: list[str] = []
        hit = 0
        for line in open(path, encoding="utf-8"):
            stripped = line.strip()
            if not stripped:
                out.append(stripped)
                continue
            try:
                row = json.loads(stripped)
            except Exception:
                out.append(stripped)
                continue
            key = (row.get("source"), row.get("id"))
            if (row.get("license_decision") != "review_required" or row.get("rights_verdict")
                    or key not in plan):
                out.append(stripped)
                continue
            v = plan[key]
            hit += 1
            if v["verdict"] == "free":
                row["license_decision"] = "pd"
                row["rights_verdict"] = "accept"
                counts["accepted"] += 1
            else:
                row["rights_verdict"] = "reject"
                counts["rejected"] += 1
            row["reindex_basis"] = "item_licence_lookup"
            row["reindex_note"] = f"{key[0]} says: {v['evidence'][:160]}"
            row["reindexed_at"] = args.stamp
            out.append(json.dumps(row, ensure_ascii=False))
        if hit and not args.dry_run:
            tmp = path + ".tmp"
            with open(tmp, "w", encoding="utf-8", newline="\n") as fh:
                fh.write("\n".join(out) + "\n")
            os.replace(tmp, path)
        if hit:
            print(f"  {os.path.basename(path):24s} {hit:6d} row(s)")

    verb = "would be" if args.dry_run else "were"
    print(f"\n{counts['accepted']} row(s) {verb} made usable, "
          f"{counts['rejected']} {verb} refused")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
