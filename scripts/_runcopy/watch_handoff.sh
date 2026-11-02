#!/usr/bin/env bash
# Exit as soon as the GPU handoff writes a new DONE/FAIL/finished line.
#
# WHY. The handoff supervisor survived its harness wrapper being killed -- the bash processes
# kept rendering, but the completion notification will never arrive. A job nobody is told about
# is a job that stalls silently, which cost about twelve hours earlier this week. This exists
# only to turn "the heartbeat grew" into a notification.
#
# It polls a FILE, not a process name: pgrep -f cannot see other Git Bash jobs on Windows, which
# is what made a wait-queue fire instantly this morning and render two episodes at once.
set -u
cd "$(dirname "$0")/../.." || exit 1
HB=runs/gpu_handoff_83_85.heartbeat
BASE=$(grep -cE "  (DONE|FAIL|handoff finished)" "$HB" 2>/dev/null || echo 0)
echo "watching $HB -- $BASE completion line(s) so far"
while : ; do
  N=$(grep -cE "  (DONE|FAIL|handoff finished)" "$HB" 2>/dev/null || echo 0)
  if [ "$N" -gt "$BASE" ]; then
    echo "--- heartbeat grew ---"
    tail -6 "$HB"
    exit 0
  fi
  sleep 120
done
