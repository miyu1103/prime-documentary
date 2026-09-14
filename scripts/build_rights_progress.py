#!/usr/bin/env python3
"""Rights-resolution progress, derived from the LEDGER rather than from the resolver's output.

Why this exists: `resolve_item_licences.py` rewrites its verdict file wholesale on every run, so
rows that have already been applied drop out of its view and the file reads as if nothing had been
resolved. Reading it as a progress report is how a finished batch looks unfinished. The ledger is
the record; this counts it.

    resolved_usable   the source answered and the answer clears it (rights_verdict = accept)
    examined_refused  the source answered and the answer refuses it (rights_verdict = reject)
    still_held        review_required with no verdict -- NOT a refusal, just unanswered. A rate
                      limit leaves rows here on purpose so the next run retries them.

    py -3.11 scripts/build_rights_progress.py            # rewrite docs/shelf/rights_progress.v001.json
    py -3.11 scripts/build_rights_progress.py --print    # show it, write nothing
"""
from __future__ import annotations

import argparse
import collections
import datetime as dt
import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ingest_archive_sources import LEDGER_DIR  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "docs", "shelf", "rights_progress.v001.json")


def counts() -> dict:
    per: dict[str, collections.Counter] = collections.defaultdict(collections.Counter)
    for path in sorted(glob.glob(os.path.join(LEDGER_DIR, "*.jsonl"))):
        if os.path.basename(path).startswith("rejects_"):
            continue
        for line in open(path, encoding="utf-8"):
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except Exception:
                continue
            src = row.get("source") or "?"
            verdict = row.get("rights_verdict")
            if verdict == "accept":
                per[src]["resolved_usable"] += 1
            elif verdict == "reject":
                per[src]["examined_refused"] += 1
            elif row.get("license_decision") == "review_required":
                per[src]["still_held"] += 1
    return {s: dict(c) for s, c in sorted(per.items()) if c}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--print", action="store_true", dest="show", help="show, write nothing")
    a = ap.parse_args()

    by_source = counts()
    doc = {
        "_derived_from": f"{LEDGER_DIR}/*.jsonl at "
                         f"{dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
        "_note": "Derived from the ledger by scripts/build_rights_progress.py. "
                 "resolve_item_licences.py rewrites its own output each run, so its verdict file "
                 "under-reports once rows are applied. still_held means unanswered, not refused.",
        "by_source": by_source,
    }
    total = collections.Counter()
    for c in by_source.values():
        total.update(c)
    for src, c in by_source.items():
        print(f"  {src:16s} " + "  ".join(f"{k}={v}" for k, v in sorted(c.items())))
    print(f"  {'TOTAL':16s} " + "  ".join(f"{k}={v}" for k, v in sorted(total.items())))
    if a.show:
        return 0
    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    print(f"\nwrote {os.path.relpath(OUT, ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
