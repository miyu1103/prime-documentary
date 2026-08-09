#!/usr/bin/env python3
"""Pull each Short's publishAt from the channel into its local schedule_result file.

The local files are derived state, not truth: anything that changed a publish time outside this
repo - Studio, a hand edit, an earlier tool run that wrote the channel but died before the file -
leaves them behind. On 2026-08-09 seven were stale, two of them by eleven days, and the re-slotter
reads them to decide what is already placed. Planning a schedule from a stale ledger double-books
a slot.

Reads only. Writes only local json, never the channel.

Usage:
  py -3.11 scripts/sync_short_schedule_ledger.py --dry-run
  py -3.11 scripts/sync_short_schedule_ledger.py --apply
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRUTH = ROOT / "runs" / "shorts_thumbs" / "yt_scheduled.v001.json"


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    if not a.apply and not a.dry_run:
        ap.error("pass --apply or --dry-run")
    if not TRUTH.exists():
        print(f"missing {TRUTH} - run scripts/yt_list_scheduled.py first")
        return 2

    truth = json.loads(TRUTH.read_text(encoding="utf-8"))
    when = {r["id"]: r["publishAt"] for r in truth["scheduled"]}
    gone = {r["id"] for r in truth["unscheduled"]}

    # Only the newest revision per Short. An older revision is a record of what was true then;
    # rewriting it would edit an immutable artifact and, on the way there, report thirty files
    # "out of sync" that were never meant to agree with today's calendar.
    newest: dict[int, tuple[int, Path]] = {}
    for f in ROOT.glob("episodes/*/09_package/short*_youtube_schedule_result.*.json"):
        m = re.match(r"short(\d+)_youtube_schedule_result\.v(\d+)\.json", f.name)
        if not m:
            continue
        n_, rev = int(m.group(1)), int(m.group(2))
        if n_ not in newest or rev > newest[n_][0]:
            newest[n_] = (rev, f)

    n = 0
    for _, f in sorted(newest.values(), key=lambda x: x[1].name):
        d = json.loads(f.read_text(encoding="utf-8"))
        vid = d.get("video_id")
        if not vid:
            continue
        if vid in gone and d.get("publishAt"):
            print(f"  {f.name}: channel has NO publish date - clearing")
            n += 1
            if a.apply:
                d["publishAt"] = None
                f.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
            continue
        real = when.get(vid)
        if not real or (d.get("publishAt") or "")[:16] == real[:16]:
            continue
        print(f"  {f.name}: {d.get('publishAt')} -> {real}")
        n += 1
        if a.apply:
            d["publishAt"] = real
            f.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n{n} out of sync" + ("" if a.apply else "   (DRY RUN)"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
