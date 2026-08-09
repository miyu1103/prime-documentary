#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""The one definition of "what is on the shelf".

Every tool that counts the archive had its own copy of this rule, and each copy was wrong
in a different way on 2026-08-09:

  build_archive_inventory counted purged.jsonl -- 64,640 records of DELETED items -- as
  stock, and since a purge row repeats its source row's id, each one counted twice. It
  reported 197,712 items when the shelf held 132,948.

  A one-off count of unjudged pairs included ukna_candidates.jsonl and reported 22,348
  High Street records as unreviewed supply. Every one has file_path: null -- the National
  Archives Discovery API returns metadata and no media, so nothing was ever downloaded.

Both were the same mistake: restating which ledger files mean "we have this" instead of
asking one place. So the rule lives here, and callers iterate.

    from shelf import shelf_rows
    for rec in shelf_rows():
        ...
"""
from __future__ import annotations

import glob
import json
import os
from typing import Iterator

LEDGER_DIR = r"H:\pd-media\assets\archive\_ledger"
ABSENT = os.path.join(LEDGER_DIR, "absent_index.json")

# Records of items we do NOT have, or never took. A purge/quarantine row carries the same
# (source, id) as the row it refers to, so reading these files double-counts as well as
# counting the deleted.
NOT_STOCK = {
    "purged.jsonl",            # deleted, with a tombstone
    "ban_risk_quarantine.jsonl",  # moved off the shelf pending review
    "shot_feedback.jsonl",     # picks and rejects, not items
    "factory_rename.progress.jsonl",
}
NOT_STOCK_SUFFIX = ("_removed.jsonl", "_candidates.jsonl")
NOT_STOCK_PREFIX = ("rejects",)


def is_stock_ledger(basename: str) -> bool:
    """True when this ledger file lists things the shelf actually holds."""
    if not basename.endswith(".jsonl"):
        return False
    if basename in NOT_STOCK or basename.startswith(NOT_STOCK_PREFIX):
        return False
    return not basename.endswith(NOT_STOCK_SUFFIX)


def load_absent() -> set[str]:
    """(source:id) whose file is not on disk. Built by build_absent_index.py.

    The ledgers are append-only and the ingest dedups on (source, id), so a deleted item's
    row has to stay -- removing it invites the lane to fetch the same file again. Readers
    subtract this set instead.
    """
    if not os.path.exists(ABSENT):
        return set()
    with open(ABSENT, encoding="utf-8", errors="replace") as fh:
        return set(json.load(fh).get("absent", {}))


def shelf_rows(include_factory: bool = True,
               absent: set[str] | None = None) -> Iterator[dict]:
    """Yield one record per item the shelf holds. Deleted and never-taken rows excluded.

    `include_factory=False` drops the older 88,740-item factory shelf, which the archive
    inventory reports separately.
    """
    if absent is None:
        absent = load_absent()
    for path in sorted(glob.glob(os.path.join(LEDGER_DIR, "*.jsonl"))):
        base = os.path.basename(path)
        if not is_stock_ledger(base):
            continue
        if base == "factory.jsonl" and not include_factory:
            continue
        with open(path, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                except Exception:
                    continue
                if not (rec.get("file_path") or ""):
                    continue          # ukna: catalogue record, no media was ever fetched
                if f"{rec.get('source')}:{rec.get('id')}" in absent:
                    continue
                yield rec


if __name__ == "__main__":
    import collections
    import sys

    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    n = collections.Counter()
    total = 0
    for r in shelf_rows():
        total += 1
        n[r.get("source")] += 1
    print(f"shelf {total:,} items")
    for s, c in n.most_common():
        print(f"  {s:16} {c:7,}")
