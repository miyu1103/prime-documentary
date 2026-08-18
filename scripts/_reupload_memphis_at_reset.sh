#!/bin/bash
# Re-upload EP64 memphis when the quota day rolls over, and PROVE it processed.
#
# 2026-08-17. The first upload was interrupted mid-transfer at 00:50 JST when the upload
# processes were force-killed. YouTube kept the video, accepted a publishAt, a thumbnail and a
# caption track -- and left uploadStatus=`uploaded`, processingStatus=`processing` eleven hours
# later, because the bytes were incomplete. It read as scheduled everywhere and would have
# reached 08-18 12:00 JST as a broken publish. e8zdPvBfb5k has been taken off the calendar.
#
# A date is not a schedule. This waits for quota, uploads over it with --replaces, and then
# refuses to call the job done until the API says the new video is `processed` / `succeeded`.
#
#   nohup bash scripts/_reupload_memphis_at_reset.sh > out_reupload_memphis.log 2>&1 &
set -u
cd /c/Users/aab15/Documents/prime-documentary

OLD="e8zdPvBfb5k"
LOG="out_reupload_memphis.log"
say() { echo "[memphis] $(date '+%m-%d %H:%M') $*" | tee -a "$LOG"; }

say "waiting for the quota day to roll over (16:00 local)"
while true; do
  room=$(py -3.11 scripts/check_api_budget.py --need 1 2>&1 | grep -oE "remaining +[0-9]+" | grep -oE "[0-9]+")
  [ -n "${room:-}" ] && [ "$room" -ge 2100 ] && break
  sleep 300
done
say "quota available (${room}) -- uploading"

# NO --replaces. Re-measured 2026-08-17 13:10: e8zdPvBfb5k returns zero items from videos.list,
# twice, seconds apart -- YouTube discarded the upload that never finished processing. --replaces
# refuses when its target does not exist ("no such video on this channel"), so passing it here
# would fail the job for the wrong reason. The receipt guard covers the same ground: it now
# checks whether any prior receipt's video is STILL LIVE, and supersedes only when none is.
say "old video $OLD is gone from the channel -- uploading fresh, no --replaces"
PYTHONIOENCODING=utf-8 py -3.11 scripts/upload_schedule_case_v001.py --ep memphis \
  >> runs/memphis_reupload.log 2>&1
rc=$?
say "uploader exit=$rc"
[ $rc -ne 0 ] && { say "UPLOAD FAILED -- see runs/memphis_reupload.log"; exit 1; }

NEW=$(grep -oE "video_id=[A-Za-z0-9_-]+" runs/memphis_reupload.log | tail -1 | cut -d= -f2)
say "new video ${NEW:-UNKNOWN}"
[ -z "$NEW" ] && { say "could not read the new video id"; exit 1; }

# A DATE IS NOT A SCHEDULE. Do not report success until YouTube says the file is good.
for i in $(seq 1 60); do
  read -r up proc < <(py -3.11 -c "
import sys; sys.path.insert(0,'scripts')
from pathlib import Path
from yt_channel_index import authorize, http, API
a=authorize(Path('.'))
st,r=http('GET',f'{API}/videos?part=status,processingDetails&id=$NEW',headers=a)
i=(r.get('items') or [{}])[0]
print(i.get('status',{}).get('uploadStatus'), i.get('processingDetails',{}).get('processingStatus'))
" 2>/dev/null)
  say "processing check $i: upload=$up processing=$proc"
  [ "$up" = "processed" ] && [ "$proc" = "succeeded" ] && { say "OK memphis is genuinely ready: $NEW"; exit 0; }
  sleep 120
done
say "STILL NOT PROCESSED after two hours -- do not trust the schedule on $NEW"
exit 1
