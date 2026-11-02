#!/usr/bin/env bash
# Rebuild and re-render EP77 keybridge after its FIRST full read (49 sheets, two readers).
#
# WHY. The 08-31 master is clean for 46 of 49 sheets, but three cuts carry a legible third-party
# mark and all three were opened at full resolution and confirmed before anything was blocked:
#   11:35  MSC across a ship's hull and MAERSK across the container stacks (pexels_6595373)
#   1:01   ONE -- Ocean Network Express livery -- on a magenta container, and again at 1:06
#          inverted (pexels_10391545)
#   6:05   a branded consumer radio filling the frame in two hands for four seconds, script
#          wordmark plus a maker's emblem (pexels_29570736)
# Blocked in config/footage_blocklist.v001.json and already pruned from the pool: 35 -> 31 stock
# clips. The film used 34 of the 35, so no unused sibling of those shoots can return on the
# rebuild -- the trap that cost EP72 three renders.
#
# station is NOT in this run. It also needs a re-render (three reviewer-rejected plates), but its
# slot is 09-04 and uri publishes at 12:00 JST TODAY. If uri's read comes back dirty it needs this
# card next, so this run takes one episode and hands the GPU straight back.
#
# PD_RENDER_CONCURRENCY=4: two contention failures on 08-30 (uri lost ~50 min, keybridge was
# thrown away at the probe) are enough evidence to stop paying for the faster setting.
set -uo pipefail
cd "$(dirname "$0")/.." || exit 1

LOG=runs/logs/render_keybridge_20260901.log
say(){ echo "[kb] $(date '+%m-%d %H:%M:%S') $*" | tee -a "$LOG"; }

say "stopping the i2v chain (it holds ComfyUI and ~18-21 GB)"
for pid in $(ps -ef 2>/dev/null | grep -E "_chain_i2v|i2v_episode_batch" | grep -v grep | awk '{print $2}'); do
  kill "$pid" 2>/dev/null
done
sleep 8
# Killing the parent orphans the child that actually holds the VRAM -- measured 2026-08-30, the
# card stayed at 18 GB with every chain process gone. Tree-kill, then sweep, then PROVE it.
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

export PD_RENDER_CONCURRENCY=4
say "START keybridge (Ep77KeyBridge, EP77) at concurrency=$PD_RENDER_CONCURRENCY"
py -3.11 scripts/check_still_luma.py --slug keybridge >> "$LOG" 2>&1 || {
  say "SKIP -- a backdrop is cut in as a picture"; exit 1; }
bash scripts/_finish_episode.sh keybridge Ep77KeyBridge 77 >> out_finish_keybridge.log 2>&1
RC=$?
say "END keybridge rc=$RC"
tail -4 out_finish_keybridge.log | tee -a "$LOG"

say "restarting the i2v chain (resumes from the delivered mp4s on disk)"
nohup bash scripts/_chain_i2v_ep78_82.sh >> runs/logs/i2v_queue_relaunch_20260901.log 2>&1 &
say "i2v launched pid=$!"

if [ "$RC" -ne 0 ]; then
  say "!! FAILED rc=$RC -- keybridge has NO new master. Do not assume otherwise."
  exit 1
fi
say "master written. Verify on keybridge_film.rendered.json beside it, not on the film json"
say "you built -- _finish_episode rebuilds it at [4/7] and they are not always the same."
say "THEN READ IT AGAIN. This is a NEW render: the 49-sheet read above describes the OLD bytes."
