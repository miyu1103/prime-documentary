#!/usr/bin/env bash
# Wait for the GPU to be released by the design lane's ComfyUI, then finish EP76 morandi.
#
# Why a waiter and not a poll from the session: polling costs a turn every time and the
# owner is away. This burns nothing while it waits and returns exactly once, when the
# render is done or when it has given up.
#
# Free is judged on MEMORY, not utilisation: ComfyUI holds ~18 GB resident between
# batches and drops to almost nothing when it exits. Three consecutive readings, so a
# gap between two batches does not look like an exit.
set -uo pipefail
cd "$(dirname "$0")/.." || exit 1

FREE_MB=4000          # ComfyUI resident is ~18 GB; a released GPU sits far below this
NEED=3                # consecutive free readings before we believe it
EVERY=120             # seconds between readings
DEADLINE=$(( $(date +%s) + 72000 ))   # 20 h, well inside the 8/28 12:00 JST slot

streak=0
while :; do
  if [ "$(date +%s)" -gt "$DEADLINE" ]; then
    echo "GAVE UP: 20 h elapsed and the GPU was never released. EP76 was NOT rendered."
    exit 2
  fi
  used=$(nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits 2>/dev/null | head -1)
  case "$used" in
    ''|*[!0-9]*) used=999999 ;;
  esac
  if [ "$used" -lt "$FREE_MB" ]; then
    streak=$((streak + 1))
    echo "$(date '+%H:%M:%S') gpu ${used}MB free-reading ${streak}/${NEED}"
    [ "$streak" -ge "$NEED" ] && break
  else
    [ "$streak" -gt 0 ] && echo "$(date '+%H:%M:%S') gpu ${used}MB busy again, streak reset"
    streak=0
  fi
  sleep "$EVERY"
done

echo "$(date '+%H:%M:%S') GPU released. Launching the EP76 finisher."
bash scripts/_finish_episode.sh morandi Ep76Morandi 76 >> out_finish_morandi.log 2>&1
rc=$?
echo "$(date '+%H:%M:%S') finisher exited rc=${rc}. Tail of out_finish_morandi.log:"
tail -20 out_finish_morandi.log
exit "$rc"
