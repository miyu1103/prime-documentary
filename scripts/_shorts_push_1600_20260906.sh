#!/usr/bin/env bash
# One-shot: wait for the 2026-09-06 16:05 JST quota reset, then push the day's 4 Shorts.
# Written 2026-09-05 by the build/publish lane. Delete after it has run.
# (No PD-ShortsPush task exists in Windows Task Scheduler -- verified 2026-09-05 -- so the
#  daily push is driven by these dated one-shots until a durable scheduler is re-established.)
set -u
cd "$(dirname "$0")/.."

TARGET=$(date -d "2026-09-06 16:05" +%s)
NOW=$(date +%s)
WAIT=$((TARGET - NOW))
if [ "$WAIT" -gt 0 ]; then
  echo "[push-timer] sleeping ${WAIT}s until 2026-09-06 16:05 JST"
  sleep "$WAIT"
fi

echo "[push-timer] refreshing channel truth"
py -3.11 scripts/yt_full_audit.py >/dev/null 2>&1
py -3.11 scripts/yt_list_scheduled.py | tail -3

echo "[push-timer] pushing shorts (reserve 1650 for the day's long-form booking)"
py -3.11 scripts/fill_short_schedule.py --apply --reserve 1650
echo "[push-timer] done, exit $?"
