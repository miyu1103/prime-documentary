#!/usr/bin/env bash
# One day's worth of Shorts publishing. Run it once per session; it is safe to run twice.
#
# The backlog is 83 finished Shorts and the API allows six uploads a day (videos.insert costs 1600
# against 10,000), so this is a two-week job done a slice at a time rather than one big batch.
#
# Order matters. Each step exists because skipping it broke something:
#   1. drop the channel-index cache - it hid four Shorts uploaded minutes earlier, and the planner
#      then offered slots that were already taken
#   2. re-read the channel - it is the source of truth, not the local records
#   3. pull those times back into the local records, so the planner sees today's calendar
#   4. upload what the quota allows, on free 6/9/18/21 JST slots (12:00 belongs to the episode)
#   5. re-read and report - never finish on a self-declared success
#
# --reserve holds units back when an episode upload is also due today (1650 per episode).
# The COUNT is capped separately, at four, inside fill_short_schedule.py (DAILY_SHORTS_CAP):
# on 2026-08-24 five Shorts spent 9,885 of 10,000 and EP71 oroville, finished and green that
# morning, could not be uploaded. Four Shorts + one long-form + comments + reads = 8,700.
set -uo pipefail
cd "$(dirname "$0")/.." || exit 1
RESERVE="${1:-0}"

rm -f runs/_cache/yt_channel_index.json
py -3.11 scripts/yt_full_audit.py > /dev/null || { echo "audit failed"; exit 1; }
py -3.11 scripts/yt_list_scheduled.py > /dev/null || { echo "dump failed"; exit 1; }
py -3.11 scripts/sync_short_schedule_ledger.py --apply | tail -1
py -3.11 scripts/fill_short_schedule.py --apply --reserve "$RESERVE" || exit 1

rm -f runs/_cache/yt_channel_index.json
py -3.11 scripts/yt_full_audit.py > /dev/null && py -3.11 scripts/yt_list_scheduled.py > /dev/null
py -3.11 - <<'PY'
import json, collections, datetime as dt
JST = dt.timezone(dt.timedelta(hours=9))
sch = json.load(open("runs/shorts_thumbs/yt_scheduled.v001.json", encoding="utf-8"))["scheduled"]
c, day = collections.Counter(), collections.Counter()
for r in sch:
    t = dt.datetime.fromisoformat(r["publishAt"].replace("Z", "+00:00")).astimezone(JST)
    c[t.isoformat()] += 1
    day[t.date().isoformat()] += 1
print(f"scheduled={len(sch)}  collisions={ {k: v for k, v in c.items() if v > 1} or 'none'}")
print("per day:", dict(sorted(day.items())))
PY
