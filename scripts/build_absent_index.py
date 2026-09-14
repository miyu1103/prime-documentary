#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Index the ledger rows whose file is not on disk, without touching the ledgers.

Sampling put the drift at 21.6% — roughly 61,000 of 284,000 rows point at a file that no
longer exists, which means every item count reported from the ledgers has been inflated.

Deleting those rows would fix the count and break two things at once: the ingest dedups on
(source, id), so a removed row invites the lane to fetch the same file again — that is how
46,707 New York City directory scans would come straight back — and a rewrite races the
lanes that are appending right now. So nothing is rewritten. The absent rows are recorded
here instead, and readers subtract them.

Two categories, kept apart because they mean different things:
  purged    - deliberately deleted, and purged.jsonl says so. Expected.
  unexplained - the file is gone and nothing recorded why. A failed move, an interrupted
                download, or a bug. Worth looking at.

    python scripts/build_absent_index.py
Output: E:\\pd-media\\assets\\archive\\_ledger\\absent_index.json
"""
from __future__ import annotations

import glob
import json
import os
import sys
import collections

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

LEDGER_DIR = r"E:\pd-media\assets\archive\_ledger"
OUT = os.path.join(LEDGER_DIR, "absent_index.json")
SKIP = ("reject", "removed", "candidates", "ban_risk", "feedback", "purged",
        "title_df", "bak", "progress", "absent_index", "existing_index")


def ledger_files():
    for p in sorted(glob.glob(os.path.join(LEDGER_DIR, "*.jsonl"))):
        if any(k in os.path.basename(p) for k in SKIP):
            continue
        yield p


def main() -> int:
    purged = set()
    ppath = os.path.join(LEDGER_DIR, "purged.jsonl")
    if os.path.exists(ppath):
        with open(ppath, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                try:
                    r = json.loads(line)
                except Exception:
                    continue
                purged.add(f"{r.get('source')}:{r.get('id')}")
    quarantined = set()
    qpath = os.path.join(LEDGER_DIR, "ban_risk_quarantine.jsonl")
    if os.path.exists(qpath):
        with open(qpath, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                try:
                    r = json.loads(line)
                except Exception:
                    continue
                if r.get("action") == "quarantine":
                    quarantined.add(f"{r.get('source')}:{r.get('id')}")
    print(f"purged.jsonl {len(purged):,} ids   quarantine {len(quarantined):,} ids")

    absent = {}
    per_src = collections.Counter()
    per_reason = collections.Counter()
    total = 0
    for path in ledger_files():
        with open(path, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    r = json.loads(line)
                except Exception:
                    continue
                total += 1
                fp = r.get("file_path", "") or ""
                if fp and os.path.exists(fp):
                    continue
                key = f"{r.get('source')}:{r.get('id')}"
                reason = ("purged" if key in purged else
                          "quarantined" if key in quarantined else "unexplained")
                absent[key] = {"theme": r.get("theme"), "source": r.get("source"),
                               "reason": reason}
                per_src[r.get("source")] += 1
                per_reason[reason] += 1

    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump({"built_from_rows": total, "absent": absent}, fh, ensure_ascii=False)

    print(f"\nledger rows {total:,}   absent {len(absent):,} ({len(absent)/max(total,1)*100:.1f}%)")
    print(f"  真の在庫 = {total - len(absent):,}\n")
    for reason, n in per_reason.most_common():
        print(f"  {reason:12} {n:7,}")
    print("\nby source:")
    for s, n in per_src.most_common(10):
        print(f"  {s:14} {n:7,}")
    print(f"\nwrote {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
