#!/usr/bin/env bash
# Same waiter as _wait_gpu_then_finish.sh, pointed at EP72 lacmegantic for the 8/29 slot.
# Free is judged on MEMORY: ComfyUI holds ~18 GB resident between batches.
set -uo pipefail
cd "$(dirname "$0")/.." || exit 1
FREE_MB=4000; NEED=3; EVERY=120
DEADLINE=$(( $(date +%s) + 72000 ))
streak=0
while :; do
  if [ "$(date +%s)" -gt "$DEADLINE" ]; then
    echo "GAVE UP: 20 h elapsed, GPU never released. EP72 was NOT rendered."; exit 2
  fi
  used=$(nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits 2>/dev/null | head -1)
  case "$used" in ''|*[!0-9]*) used=999999 ;; esac
  if [ "$used" -lt "$FREE_MB" ]; then
    streak=$((streak + 1)); echo "$(date '+%H:%M:%S') gpu ${used}MB free ${streak}/${NEED}"
    [ "$streak" -ge "$NEED" ] && break
  else
    [ "$streak" -gt 0 ] && echo "$(date '+%H:%M:%S') gpu ${used}MB busy again, reset"
    streak=0
  fi
  sleep "$EVERY"
done
echo "$(date '+%H:%M:%S') GPU released. Launching the EP72 finisher."
bash scripts/_finish_episode.sh lacmegantic Ep72Lacmegantic 72 >> out_finish_lacmegantic.log 2>&1
rc=$?
echo "$(date '+%H:%M:%S') finisher exited rc=${rc}"
tail -20 out_finish_lacmegantic.log
exit "$rc"
