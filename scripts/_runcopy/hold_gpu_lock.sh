#!/usr/bin/env bash
# Hold the project's GPU lock for the long-form render chain, so the EP86 i2v chain declines
# politely instead of being killed.
#
# WHY A DEDICATED PROCESS. _chain_i2v_robust.sh validates the lock with `kill -0 <pid>`, and
# that is an MSYS pid, not a Windows one -- writing the supervisor's Windows pid into the file
# makes the lock look STALE and the chain deletes it and starts anyway (measured: `kill -0
# 42692` from Git Bash answers NO for a live bash.exe). So the holder has to be a Git Bash
# process that writes its own `$$`.
#
# WHAT IT REPLACES. The EP86 columbia chain and these renders took the same card three times
# today; with both running the render fell from ~350 frames/min to 124 and once to 38. Killing
# the chain did not converge -- it came back at 15:37 and 16:02 -- and each kill destroys that
# chain's in-flight clip. This is the mechanism the repo already has for exactly this.
#
# It releases on exit, and also when the render chain reports it is finished.
set -u
cd "$(dirname "$0")/../.." || exit 1
LOCK="out_gpu_comfy.lock"
HB="runs/gpu_handoff_83_85.heartbeat"
MAX_HOLD_SECONDS=$((10 * 3600))     # never sit on the card longer than the work could take

echo "$$ longform-renders-EP83-85" > "$LOCK"
trap 'rm -f "$LOCK"; echo "released the GPU lock"' EXIT
echo "holding $LOCK as msys pid $$"

waited=0
while [ "$waited" -lt "$MAX_HOLD_SECONDS" ]; do
  if grep -q "handoff finished" "$HB" 2>/dev/null; then
    echo "render chain reports finished -- releasing"
    exit 0
  fi
  sleep 60
  waited=$((waited + 60))
done
echo "max hold reached -- releasing so nothing is blocked forever"
