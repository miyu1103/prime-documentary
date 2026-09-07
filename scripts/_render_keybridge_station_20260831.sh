#!/usr/bin/env bash
# Stop i2v, render EP77 keybridge and EP81 station, restart i2v. Second attempt at both.
#
# WHY THIS EXISTS. The 08-30 queue got lacmegantic and uri out and then lost both of these:
#   keybridge  died six minutes in when the 60-second PROBE failed on
#              "Failed to fetch .../keybridge/motion/H123.mp4". H123 was present and intact in
#              the pool, in public_ep77 and in the E: archive; all 128 clips were there, none
#              zero-byte, and the disk had 288 GB free. Remotion prints "disk space is low" as a
#              guess for any failed fetch. It was contention -- the same class that had cost uri
#              fifty minutes an hour earlier. probe_before_render.sh has since been given the
#              concurrency argument and the single retry that pd_render_guarded.sh already had.
#   station    was refused by check_episode_inputs: "no factory_clip_qc manifest". The 49 stock
#              clips were staged on 08-30 but the record of WHO LOOKED at them was never written.
#              write_factory_clip_qc.py --slug station has since written it (49 clips, binding
#              =exact), and inputs now says READY to build.
#
# PD_RENDER_CONCURRENCY=4 for the whole run. Measured last night: lacmegantic finished in 92 min
# at the default; uri needed 143 min after falling back to 4; keybridge was thrown away entirely.
# Four is slower per episode and it is the setting long-form WebGL already needs. Two contention
# failures in one night is enough evidence to stop paying for the faster setting.
#
# UNLIKE the script it replaces, this one does NOT hand the card to i2v after a failed render and
# call it done. That is what happened at 01:02: station exited rc=1 and i2v was started 30 seconds
# later as though the night had gone to plan.
set -uo pipefail
cd "$(dirname "$0")/.." || exit 1

LOG=runs/logs/render_kb_station_20260831.log
say(){ echo "[kb-st] $(date '+%m-%d %H:%M:%S') $*" | tee -a "$LOG"; }

# ---- 1. take the card off ComfyUI -------------------------------------------------------
say "stopping the i2v chain"
for pid in $(ps -ef 2>/dev/null | grep -E "_chain_i2v|i2v_episode_batch" | grep -v grep | awk '{print $2}'); do
  kill "$pid" 2>/dev/null
done
sleep 8
# Killing the parent orphans the child that actually holds the VRAM -- measured 2026-08-30, the
# card stayed at 18 GB / 100% with every chain process gone. Tree-kill, then sweep, then PROVE it.
for pid in $(netstat -ano 2>/dev/null | grep ':8188' | grep LISTENING | grep -oE '[0-9]+$' | head -1); do
  taskkill //F //T //PID "$pid" >/dev/null 2>&1
done
for pid in $(powershell -NoProfile -Command "(Get-CimInstance Win32_Process | Where-Object { \$_.Name -match '^python' -and \$_.CommandLine -match 'main\.py' -and (\$_.ExecutablePath -match 'ComfyUI' -or \$_.ExecutablePath -match 'Python310') }).ProcessId" 2>/dev/null | tr -d '\r'); do
  [ -n "$pid" ] && taskkill //F //T //PID "$pid" >/dev/null 2>&1
done
for _ in 1 2 3 4 5 6 7 8 9 10; do
  used=$(nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits 2>/dev/null | head -1)
  [ -z "$used" ] && break
  [ "$used" -lt 4000 ] && break
  sleep 4
done
say "VRAM now ${used:-unknown} MiB"
if [ -n "${used:-}" ] && [ "$used" -ge 4000 ]; then
  say "REFUSING to render into ${used} MiB of occupied VRAM. A human should look."
  exit 1
fi

# ---- 2. the two renders ------------------------------------------------------------------
export PD_RENDER_CONCURRENCY=4
FAILED=""
run_one() {
  local slug="$1" comp="$2" nn="$3"
  say "START $slug ($comp, EP$nn) at concurrency=$PD_RENDER_CONCURRENCY"
  py -3.11 scripts/check_still_luma.py --slug "$slug" >> "$LOG" 2>&1 || {
    say "SKIP $slug -- a backdrop is cut in as a picture"; FAILED="$FAILED $slug(still-luma)"; return 1; }
  bash scripts/_finish_episode.sh "$slug" "$comp" "$nn" >> "out_finish_${slug}.log" 2>&1
  local rc=$?
  say "END $slug rc=$rc"
  tail -4 "out_finish_${slug}.log" | tee -a "$LOG"
  [ $rc -ne 0 ] && FAILED="$FAILED $slug(rc=$rc)"
  return $rc
}
run_one keybridge Ep77KeyBridge 77 || say "continuing past keybridge"
run_one station   Ep81Station   81 || say "continuing past station"

# ---- 3. give the card back ----------------------------------------------------------------
say "restarting the i2v chain (resumes from the delivered mp4s on disk)"
nohup bash scripts/_chain_i2v_ep78_82.sh >> runs/logs/i2v_queue_relaunch_20260831.log 2>&1 &
say "i2v launched pid=$!"
sleep 90
say "i2v 90s in: $(tail -1 out_i2v_ep78_82.log 2>/dev/null)"

if [ -n "$FAILED" ]; then
  say "!! FINISHED WITH FAILURES:$FAILED -- these episodes have NO master. Do not assume otherwise."
else
  say "both masters written. Verify on the *_film.rendered.json snapshot beside each, not on the"
  say "film json you built -- _finish_episode rebuilds it at [4/7] and they are not always the same."
fi
say "Either way: read the shipped frames before booking anything."
