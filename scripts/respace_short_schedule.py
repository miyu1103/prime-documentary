#!/usr/bin/env python3
"""Give every scheduled Short its own slot: two a day, at 12:00 and 19:00 JST.

Measured on the live channel 2026-08-02: 18 Shorts are scheduled across 9 days, but every one of
them fires at 12:00, so the day's two Shorts land on the feed at the same instant and compete with
each other. One day carries three and another carries one.

This only rewrites `status.publishAt`. It never re-uploads, never changes the video, the title or
the description, and it keeps the day a Short was assigned to unless that day is over-filled.

DANGER, and the reason this script is careful: videos.update with `part=status` REPLACES the whole
status object. A write that omits publishAt UNSCHEDULES the video and it goes public immediately.
This build always sends privacyStatus + publishAt together, and refuses to write if the video is
not private-with-a-future-date to begin with.

Usage:
  py -3.11 scripts/respace_short_schedule.py
  py -3.11 scripts/respace_short_schedule.py --apply
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JST = timezone(timedelta(hours=9))
SLOTS = (12, 19)                      # JST hours, one Short each
CHANNEL_ALLOWLIST = {"UCuQPtAz1rca9eJ4xhvX0yKA"}

sys.path.insert(0, str(Path(__file__).resolve().parent))
# A Short this script cannot see is a Short it will happily schedule on top of. The uploads
# playlist dropped nine videos on 2026-08-03, so enumeration is shared and unioned.
from yt_channel_index import (  # noqa: E402
    authorize, fetch_videos, http, iso_seconds as secs, list_video_ids)


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    auth = authorize(ROOT)
    vids = list(fetch_videos(auth, list_video_ids(auth)).values())

    now = datetime.now(JST)
    shorts = []
    for v in vids:
        s = v["status"]
        if not s.get("publishAt") or s.get("privacyStatus") != "private":
            continue
        if secs(v["contentDetails"]["duration"]) > 185:
            continue
        dt = datetime.fromisoformat(s["publishAt"].replace("Z", "+00:00")).astimezone(JST)
        if dt <= now:
            continue
        shorts.append({"id": v["id"], "dt": dt, "title": v["snippet"]["title"][:44],
                       "chan": v["snippet"].get("channelId")})
    shorts.sort(key=lambda r: (r["dt"], r["id"]))
    if not shorts:
        print("no future-scheduled Shorts"); return 0

    # two per day from the first scheduled day; keep the running order, level the over-filled days
    day0 = shorts[0]["dt"].date()
    plan = []
    for i, s in enumerate(shorts):
        day = day0 + timedelta(days=i // len(SLOTS))
        hour = SLOTS[i % len(SLOTS)]
        target = datetime(day.year, day.month, day.day, hour, 0, tzinfo=JST)
        plan.append({**s, "target": target, "changed": target != s["dt"]})

    per_day = defaultdict(int)
    for p in plan:
        per_day[p["target"].date()] += 1
    print(f"{len(plan)} scheduled Shorts -> {len(per_day)} days, "
          f"{'/'.join(f'{h:02d}:00' for h in SLOTS)} JST\n")
    print(f"{'now (JST)':<17}{'->':^4}{'new (JST)':<17}title")
    for p in plan:
        mark = "" if p["changed"] else "   (unchanged)"
        print(f"{p['dt']:%m/%d %H:%M}     ->  {p['target']:%m/%d %H:%M}     {p['title']}{mark}")
    moving = [p for p in plan if p["changed"]]
    print(f"\n{len(moving)} would move, {len(plan)-len(moving)} stay")

    if not args.apply:
        print("\nDRY RUN — nothing written. Re-run with --apply.")
        return 0

    ok = fail = 0
    for p in moving:
        if p["chan"] not in CHANNEL_ALLOWLIST:
            print(f"  {p['id']} NOT ON ALLOWLISTED CHANNEL — skipped"); fail += 1; continue
        # privacyStatus AND publishAt together: sending one without the other publishes it now
        body = {"id": p["id"], "status": {
            "privacyStatus": "private",
            "publishAt": p["target"].astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        }}
        st, res = http("PUT", "https://www.googleapis.com/youtube/v3/videos?part=status",
                       headers=auth, body=body)
        if st == 200 and res.get("status", {}).get("publishAt"):
            ok += 1
            print(f"  {p['target']:%m/%d %H:%M}  {p['title']}")
        else:
            fail += 1
            print(f"  FAILED {st} {p['id']}: {res.get('error', {}).get('message','')[:110]}")
    print(f"\nmoved {ok}, failed {fail}")
    return 0 if not fail else 1


if __name__ == "__main__":
    raise SystemExit(main())
