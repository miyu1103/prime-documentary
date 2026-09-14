#!/usr/bin/env bash
# Claim the GPU from the i2v chain at an episode boundary, render one long-form, release.
#
#   bash scripts/_claim_gpu_and_render.sh <slug> <Composition> <NN> <i2v-slug-to-finish> <target>
#
# Why this exists. One 4090, two lanes, and as of 2026-08-27 the same thread owns both. The
# publishing calendar has dated slots that cannot be recovered; the i2v queue has no date.
# So the renders go first and the queue waits -- but only at a boundary, never mid-episode.
#
# How the handover works, measured in _chain_i2v_ep78_82.sh:
#   * `wait_for_gpu` is called ONCE PER ROUND, and a round processes every pending plate of
#     one episode. So writing the lock now does NOT interrupt the round in flight; the chain
#     blocks when it starts the NEXT episode.
#   * the lock is "<pid> <slug>". The chain waits while that pid is alive and the slug is not
#     its own. Hence this script holds the lock for its whole life and removes it at the end.
#   * pd_render_guarded.sh aborts only when GPU util > 50 AND ComfyUI answers. A chain that is
#     waiting leaves ComfyUI up but idle, so the render passes once the round drains.
set -uo pipefail
cd "$(dirname "$0")/.." || exit 1

SLUG="${1:?slug}"; COMP="${2:?composition}"; NN="${3:?episode number}"
I2V_SLUG="${4:?i2v slug that must finish first}"; I2V_TARGET="${5:?its plate count}"
LOCK=out_gpu_comfy.lock
PREV="$(cat "$LOCK" 2>/dev/null || true)"

release(){ [ -n "$PREV" ] && printf '%s' "$PREV" > "$LOCK" || rm -f "$LOCK"; }
trap 'release' EXIT INT TERM

printf '%s %s' "$$" "$SLUG" > "$LOCK"
echo "$(date '+%H:%M:%S') claimed the GPU lock as pid $$ for $SLUG (was: ${PREV:-none})"

# Wait for the in-flight i2v round to drain. Two independent signals, because either one
# alone lies: the delivered count can stall on a quarantine, and utilisation dips between
# clips. Requires BOTH to be quiet, three readings apart.
quiet=0
while :; do
  n=$(ls "remotion/public/${I2V_SLUG}/motion/"*.mp4 2>/dev/null | grep -vc '_depth' || echo 0)
  util=$(nvidia-smi --query-gpu=utilization.gpu --format=csv,noheader,nounits 2>/dev/null | head -1)
  util=${util:-100}
  if [ "$n" -ge "$I2V_TARGET" ] || [ "$util" -lt 50 ]; then
    quiet=$((quiet + 1))
    echo "$(date '+%H:%M:%S') ${I2V_SLUG} ${n}/${I2V_TARGET}, util ${util}% -- quiet ${quiet}/3"
    [ "$quiet" -ge 3 ] && break
  else
    [ "$quiet" -gt 0 ] && echo "$(date '+%H:%M:%S') busy again (${n}/${I2V_TARGET}, ${util}%), reset"
    quiet=0
  fi
  sleep 60
done

echo "$(date '+%H:%M:%S') GPU is ours. Rendering ${SLUG}."
bash scripts/_finish_episode.sh "$SLUG" "$COMP" "$NN" >> "out_finish_${SLUG}.log" 2>&1
rc=$?
echo "$(date '+%H:%M:%S') finisher exited rc=${rc}; releasing the lock so the i2v chain resumes"
tail -6 "out_finish_${SLUG}.log"
exit "$rc"
