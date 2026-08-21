#!/usr/bin/env python3
r"""Prove the archive ledger describes the shelf exactly once, and is not torn.

WHY THIS EXISTS
---------------
2026-08-20. Two copies of `reindex_archive_shelf.py` appended to one ledger at the same
time. The result did not look broken: it looked BIGGER. 66,324 rows for 60,572 files reads
like a fuller shelf, and `shelf_rows()` returned a confident non-zero, which is the exact
check the rebuild brief lists under "done looks like". Underneath, 586 lines were torn in
half and 117 files had no surviving row at all -- so the ingest would have re-downloaded
them, which is the one thing the reindex exists to prevent.

A row count is not an integrity check. This compares the ledger against the FILES, which is
the only authority, and it fails loudly on all three ways the ledger can lie:

  * torn      -- a line that is not valid JSON (concurrent writers)
  * duplicate -- more than one row for the same file_path (a second run, or a retry)
  * missing   -- a media file on the shelf with no row (its row was lost, or never written)

    py -3.11 scripts/check_ledger_integrity.py            # compare against the real shelf
    py -3.11 scripts/check_ledger_integrity.py --quick    # skip the disk walk (torn/dupes only)

Exit 0 only when the ledger and the shelf agree exactly.
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ingest_archive_sources import LEDGER_DIR, TIERS  # noqa: E402
from reindex_archive_shelf import kind_of  # noqa: E402


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true",
                    help="skip the disk walk: reports torn and duplicate rows only")
    args = ap.parse_args()

    print(f"ledger : {LEDGER_DIR}")
    paths: Counter[str] = Counter()
    torn: Counter[str] = Counter()
    rows = 0
    for f in sorted(glob.glob(os.path.join(LEDGER_DIR, "*.jsonl"))):
        name = os.path.basename(f)
        if name.startswith("rejects"):
            continue
        with open(f, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                if not line.strip():
                    continue
                try:
                    rec = json.loads(line)
                except Exception:
                    torn[name] += 1
                    continue
                rows += 1
                paths[str(rec.get("file_path", ""))] += 1

    dupes = {p: n for p, n in paths.items() if n > 1}
    print(f"rows parsed        : {rows}")
    print(f"distinct file_path : {len(paths)}")
    print(f"torn lines         : {sum(torn.values())}"
          + (f"  {dict(torn)}" if torn else ""))
    print(f"duplicated files   : {len(dupes)}")

    missing = 0
    if not args.quick:
        on_disk = 0
        for tier in TIERS:
            root = Path(tier["root"])
            if not root.exists():
                continue
            for p in root.rglob("*"):
                if p.is_file() and kind_of(p.suffix):
                    on_disk += 1
                    if str(p) not in paths:
                        missing += 1
        print(f"media files on disk: {on_disk}")
        print(f"files with NO row  : {missing}")

    ok = not torn and not dupes and missing == 0
    print("\nPASS -- the ledger describes the shelf exactly once" if ok else
          "\nFAIL -- the ledger does not match the shelf; see the counts above")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
