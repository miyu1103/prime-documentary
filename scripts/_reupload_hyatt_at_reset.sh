#!/bin/bash
# Re-upload EP69 hyatt when the quota day rolls over, and PROVE it processed.
#
# 2026-08-19. The first upload (Ms9wVUPsO3Y, started 08-18 19:12 UTC) ABORTED IN TRANSFER:
# runs/upload_hyatt_0819.log records twelve resume attempts from 1,292 MB to 1,334 MB of a
# 1,645 MB file and then "upload aborted after 13 network failures". YouTube had already
# applied the metadata it was sent in the resumable-session header, so the video carried a
# title and a publishAt of 2026-08-23T03:00Z while uploadStatus stayed `uploaded` and
# processingStatus stayed `processing` -- eighteen hours later it still had duration P0D, no
# custom thumbnail and no caption track. It has been taken OFF the calendar with
# scripts/unschedule_video.py; it is still private on the channel.
#
# NOTE THE TRAP THAT ALMOST FOOLED THIS SESSION: videos.list reported
# fileDetails.fileSize = 1644589283, byte-for-byte equal to the local v002 master. That is the
# size DECLARED in the resumable session, not the size RECEIVED. A matching byte count is not
# evidence of a completed transfer. The log is.
#
# ROOT CAUSE, measured: two default routes at metric 0 -- Wi-Fi 2 -> 10.40.210.161 and
# Ethernet -> 192.168.210.1, different subnets. Outbound packets can move between interfaces
# mid-connection, which kills an established TCP upload. TURN WI-FI OFF BEFORE RUNNING THIS
# (taskbar toggle, no admin needed). The guard below refuses to start while both are up.
#
#   nohup bash scripts/_reupload_hyatt_at_reset.sh > out_reupload_hyatt.log 2>&1 &
set -u
cd /c/Users/aab15/Documents/prime-documentary

OLD="Ms9wVUPsO3Y"
LOG="out_reupload_hyatt.log"
say() { echo "[hyatt] $(date '+%m-%d %H:%M') $*" | tee -a "$LOG"; }

# ---- guard 1: one network path -------------------------------------------------------
# Count default routes whose INTERFACE IS ACTUALLY UP. Counting rows in the route table
# was wrong: measured 2026-08-20, `Wi-Fi 2` sat at Status=Disconnected with its IP and its
# default route still in the table, so the guard refused an upload on a machine that had
# exactly one live path. A stale row is not a route packets can leave by.
routes=$(pwsh -NoProfile -c "(Get-NetRoute -DestinationPrefix '0.0.0.0/0' | Where-Object { (Get-NetAdapter -InterfaceIndex \$_.ifIndex -ErrorAction SilentlyContinue).Status -eq 'Up' } | Measure-Object).Count" 2>/dev/null | tr -d '\r')
if [ "${routes:-0}" -gt 1 ]; then
  say "REFUSED: $routes default routes are on LIVE adapters. This is what broke the first upload."
  say "         Turn Wi-Fi off (taskbar) so only the wired route remains, then re-run."
  pwsh -NoProfile -c "Get-NetAdapter | Where-Object Status -eq 'Up' | Select-Object Name,Status | Format-Table -AutoSize | Out-String -Width 50" | tee -a "$LOG"
  exit 2
fi
say "network: one default route on a live adapter -- good"

# ---- guard 2: the film still passes its own gate -------------------------------------
if ! py -3.11 scripts/upload_schedule_case_v001.py --ep hyatt --explain-policy 2>&1 | grep -q "decision=permit"; then
  say "REFUSED: ship policy no longer says permit. Read the explain output before forcing."
  exit 3
fi
say "policy: permit"

# ---- wait for the quota day ----------------------------------------------------------
say "waiting for the quota day to roll over (16:00 local)"
while true; do
  room=$(py -3.11 scripts/check_api_budget.py --need 1 2>&1 | grep -oE "remaining +[0-9]+" | grep -oE "[0-9]+")
  [ -n "${room:-}" ] && [ "$room" -ge 2100 ] && break
  sleep 300
done
say "quota available (${room})"

# ---- the old upload has to be gone, or the duplicate-title guard refuses --------------
still=$(py -3.11 scripts/yt_video_status.py --id "$OLD" 2>&1 | grep -c "MISSING")
if [ "$still" -eq 0 ]; then
  say "STOP: $OLD is STILL on the channel. YouTube discarded EP64's dead upload by itself"
  say "      within a day; this one has not gone. Deleting a video is an owner decision:"
  say "      py -3.11 scripts/delete_scheduled_video.py --id $OLD \\"
  say "         --expect-title-prefix 'One Rod Became Two' --apply"
  say "      Re-run this script afterwards."
  exit 4
fi
say "$OLD is gone from the channel -- uploading fresh, no --replaces"

PYTHONIOENCODING=utf-8 py -3.11 scripts/upload_schedule_case_v001.py --ep hyatt \
  >> runs/hyatt_reupload.log 2>&1
rc=$?
say "uploader exit=$rc"
[ $rc -ne 0 ] && { say "UPLOAD FAILED -- see runs/hyatt_reupload.log"; exit 1; }

# ---- the job is NOT done until the API says the bytes arrived and processed ----------
say "uploaded. now proving it processed -- a publishAt is not a schedule."
for i in $(seq 1 60); do
  out=$(py -3.11 scripts/yt_video_status.py --slug hyatt 2>&1)
  echo "$out" | tail -3 >> "$LOG"
  if echo "$out" | grep -q "0 problem"; then
    say "PROCESSED and scheduled. Done."
    exit 0
  fi
  sleep 120
done
say "STILL NOT PROCESSED after two hours -- do not leave it on the calendar."
exit 5
