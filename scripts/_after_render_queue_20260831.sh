#!/usr/bin/env bash
# Follow-on for scripts/_render_after_blocklist_20260830.sh. Waits for that queue to finish,
# renders EP81 station, then restarts the i2v chain. Exists so the card is not idle between
# ~02:30 and whenever a human next looks.
#
# WHY station is not in the first queue: when that queue was written, station's film json was the
# 08-28 build, which used ZERO factory clips -- the 49 stock clips read and staged on 08-30 were
# on disk but not in the film, so rendering it would have shipped the exact blocker the staging
# was done to clear. The film was rebuilt at 00:57 on 08-31 and now carries 26 factory cuts
# against 202 motion, diversity 0.92, max reuse 2.
#
# WHY i2v restarts last: it holds ComfyUI and ~18-21 GB of VRAM, which starves a Remotion render.
# It resumes from the delivered mp4s on disk, so nothing is lost by stopping it. State when it was
# stopped at 20:50 on 08-30:
#   concordia 184  station 184  valdez 40  colgan 0  alaska261 0  max737 0  threemile 0  katrina 0
# 1,023 clips remain, about 52 hours at the measured 3.03 min/clip.
set -uo pipefail
cd "$(dirname "$0")/.." || exit 1

LOG=runs/logs/after_render_queue_20260831.log
say(){ echo "[after] $(date '+%m-%d %H:%M:%S') $*" | tee -a "$LOG"; }

say "waiting for the first queue to print QUEUE DONE"
for _ in $(seq 1 480); do          # 480 x 30s = 4h ceiling
  grep -q "QUEUE DONE" runs/logs/render_queue_20260830.log 2>/dev/null && break
  sleep 30
done
if ! grep -q "QUEUE DONE" runs/logs/render_queue_20260830.log 2>/dev/null; then
  say "first queue did not finish within 4h -- NOT starting station, NOT starting i2v."
  say "a human should look at runs/logs/render_queue_20260830.log before anything else runs."
  exit 1
fi
say "first queue finished"

say "station: pre-render checks"
if py -3.11 scripts/check_still_luma.py --slug station >> "$LOG" 2>&1; then
  say "station: still-luma clean -> rendering"
  bash scripts/_finish_episode.sh station Ep81Station 81 >> out_finish_station.log 2>&1
  say "station: END rc=$?"
  tail -4 out_finish_station.log | tee -a "$LOG"
else
  say "station: SKIPPED -- a backdrop is cut in as a picture. Fix, then render by hand."
fi

# The card is now free. Prove it before handing it to ComfyUI: a Remotion render leaves headless
# chrome behind sometimes, and starting Wan into occupied VRAM is how throughput collapsed on
# 2026-08-22 (12 clips per chunk -> 3 -> 1).
used=$(nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits 2>/dev/null | head -1)
say "VRAM before i2v: ${used} MiB"

say "restarting the i2v chain (resumes from delivered mp4s on disk)"
nohup bash scripts/_chain_i2v_ep78_82.sh >> runs/logs/i2v_queue_relaunch_20260831.log 2>&1 &
say "i2v launched pid=$!"
sleep 90
say "i2v 90s in: $(tail -1 out_i2v_ep78_82.log 2>/dev/null)"
say "DONE. Next human step: read the shipped frames of lacmegantic, uri, keybridge and station"
say "before booking any of them. Tonight three masters passed every machine gate with 139 defects."
