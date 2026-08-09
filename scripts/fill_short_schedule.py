#!/usr/bin/env python3
"""Upload and schedule as many backlog Shorts as today's quota allows.

92 finished Shorts were rendered, packaged and sitting on disk while the channel published four a
day from a queue that ran out on 2026-08-16. Uploading them one command at a time is the only
reason the backlog exists, so this walks it.

Two rules it will not break:

  * 12:00 JST belongs to the long-form episode. On 2026-08-09 three episodes and three Shorts were
    scheduled on the same minute at 12:00 and competed with each other in the feed. Shorts go at
    6, 9, 18 and 21 JST and never at 12.
  * The episode uploads come first. videos.insert costs 1600 units against a 10,000/day budget, so
    six Shorts empty it; --reserve holds units back for the episode chain that is waiting on the
    same budget.

Free slots are read from the live channel, not from local files: local schedule_result files were
eleven days stale on 2026-08-09 and planning from them double-booked a slot.

Usage:
  py -3.11 scripts/yt_list_scheduled.py                       # refresh channel truth first
  py -3.11 scripts/fill_short_schedule.py --dry-run
  py -3.11 scripts/fill_short_schedule.py --apply --reserve 6300 --max 3
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import yt_quota  # noqa: E402

JST = dt.timezone(dt.timedelta(hours=9))
SHORT_HOURS = (6, 9, 18, 21)          # 12 JST is the episode slot
TRUTH = ROOT / "runs" / "shorts_thumbs" / "yt_scheduled.v001.json"
UPLOAD_UNITS = yt_quota.UNITS.get("videos.insert", 1600)


def backlog() -> list[str]:
    """Shorts that are rendered and packaged but have no video on the channel."""
    src = (ROOT / "scripts" / "schedule_short_youtube.py").read_text(encoding="utf-8")
    cfg = set(re.findall(r'^    "(\d+)":', src, re.M))
    done = set()
    for f in ROOT.glob("episodes/*/09_package/short*_youtube_schedule_result.*.json"):
        d = json.loads(f.read_text(encoding="utf-8"))
        m = re.match(r"short(\d+)_", f.name)
        if d.get("video_id") and m:
            done.add(m.group(1).zfill(2))
    rendered = {
        re.match(r"short(\d+)_yt_coverfirst", p.stem).group(1).zfill(2)
        for p in (ROOT / "remotion" / "out").glob("short*_yt_coverfirst.mp4")
    }
    return sorted(rendered & cfg - done, key=int)


def free_slots(n: int) -> list[dt.datetime]:
    taken = set()
    for r in json.loads(TRUTH.read_text(encoding="utf-8"))["scheduled"]:
        t = dt.datetime.fromisoformat(r["publishAt"].replace("Z", "+00:00")).astimezone(JST)
        taken.add(t.replace(minute=0, second=0, microsecond=0))
    # start the day after the last thing already on the calendar, so nothing lands in the past
    last = max(taken).date() if taken else dt.datetime.now(JST).date()
    out: list[dt.datetime] = []
    day = last
    while len(out) < n:
        for h in SHORT_HOURS:
            if len(out) >= n:
                break
            slot = dt.datetime(day.year, day.month, day.day, h, tzinfo=JST)
            if slot in taken or slot <= dt.datetime.now(JST):
                continue
            out.append(slot)
        day += dt.timedelta(days=1)
    return out


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--reserve", type=int, default=0,
                    help="units to leave untouched for the episode upload chain")
    ap.add_argument("--max", type=int, default=99)
    a = ap.parse_args()
    if not a.apply and not a.dry_run:
        ap.error("pass --apply or --dry-run")
    if not TRUTH.exists():
        print(f"missing {TRUTH} - run scripts/yt_list_scheduled.py first")
        return 2
    # The channel dump is built from scripts/_yt_audit.json, and that file lists the ids to ask
    # about. Uploads made after the audit are invisible to it: five Shorts were scheduled and the
    # dump still said 29, so a second run would have planned straight over them.
    newest = max((f.stat().st_mtime for f in
                  ROOT.glob("episodes/*/09_package/short*_youtube_schedule_result.*.json")),
                 default=0)
    if newest > TRUTH.stat().st_mtime:
        print("channel dump is older than the newest upload record. Refresh it first:\n"
              "  py -3.11 scripts/yt_full_audit.py && py -3.11 scripts/yt_list_scheduled.py")
        return 2

    todo = backlog()
    usable = max(0, yt_quota.remaining() - a.reserve)
    budget_allows = usable // UPLOAD_UNITS
    n = min(len(todo), budget_allows, a.max)
    print(f"backlog={len(todo)}  quota remaining={yt_quota.remaining()} "
          f"(reserve {a.reserve}) -> {budget_allows} uploads  doing {n}")
    if not n:
        return 0

    slots = free_slots(n)
    for s, slot in zip(todo[:n], slots):
        iso = slot.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        print(f"  short{s} -> {slot.strftime('%m-%d %H:%M')} JST ({iso})")
        if not a.apply:
            continue
        r = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "schedule_short_youtube.py"),
             "--short", s, "--publish-at", iso],
            cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
        tail = "\n".join((r.stdout or "").strip().splitlines()[-3:])
        print(f"    {'OK' if r.returncode == 0 else 'FAILED'}  {tail}")
        if r.returncode != 0:
            print((r.stderr or "").strip()[-600:])
            print("  stopping on first failure - a half-uploaded batch is worse than a short one")
            return 1
    if not a.apply:
        print("\n(DRY RUN)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
