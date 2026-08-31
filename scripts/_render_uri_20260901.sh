#!/usr/bin/env bash
# FIFTH render of EP73 uri. It publishes at 12:00 JST today (2026-09-01).
#
# WHY, and it is not the reason the previous four were run.
# The master on disk (08-31 06:05) CONTAINS ALL FIVE CLIPS THAT WERE BLOCKED THE DAY BEFORE:
#   0:33   three ABB manufacturer nameplates      AR-pexels_v_10008320
#   0:58   two more ABB nameplates + a Russian corporate site board with a roundel logo
#                                                 AR-pexels_v_10008388
#   1:08   "ШКАФ ПИТАНИЯ И ОБОГРЕВА ПРИВОДОВ 2" / "ШЗВ 3 ОБР", fully legible
#                                                 AR-pexels_v_10058364
#   1:19   "СВ 110 / ШКАФ / СВ" placard            AR-pexels_v_10058463
#   3:25   the HollyFrontier wordmark and HF monogram painted on a storage tank
#                                                 AR-pexels_v_12891229
# All five are in episodes/PD-2026-073-uri/08_edit/uri_film.rendered.json at exactly those cuts.
# None of them is readable in the 960px QC frames; the reader pulled 1080p crops from the master.
#
# WHY NOTHING CAUGHT IT.
#   1. _finish_episode [2b/7] pruned the img and motion pools and NOT factory -- and every stock
#      clip on the blocklist is a factory clip. The pool was pruned by hand, then the source copy
#      at [1/7] put the clips straight back, and [4/7] built them into the film again.
#   2. audit_films_vs_blocklist reads remotion/src/data/<slug>_film.json. That file was rebuilt
#      clean at 11:45 -- five and a half hours AFTER the render finished -- so the audit reported
#      uri CLEAN while the bytes on disk were not. A film json rebuilt after the fact says nothing
#      about the master, which is what scripts/_render_keybridge_20260901.sh already warned about
#      in its own closing line.
# [2b/7] now prunes factory as well. That is the durable half of the fix.
#
# ALSO IN THIS RENDER, at no extra cost: the lower-third clipping fix (commit 51ac1e79). uri is the
# worst affected film measured so far -- twelve topper cards clipped in their settled state across
# the last seven minutes, so every on-screen source attribution in that stretch was damaged.
#
# PD_RENDER_CONCURRENCY=4. Two contention failures on 08-30 are enough evidence.
set -uo pipefail
cd "$(dirname "$0")/.." || exit 1

LOG=runs/logs/render_uri_20260901.log
say(){ echo "[uri5] $(date '+%m-%d %H:%M:%S') $*" | tee -a "$LOG"; }

# ---- 1. prove the blocked clips cannot come back before spending two hours ------------------
say "checking the five blocked clips are out of the pool AND out of the archive"
BAD=0
for id in 10008320 10008388 10058364 10058463 12891229 30243440 30243437; do
  if ls remotion/public/uri/factory/ 2>/dev/null | grep -q "$id"; then
    say "  STILL IN POOL: $id"; BAD=1
  fi
  if ls /e/pd-media/episodes/PD-2026-073-uri/05_stock/candidates/ 2>/dev/null | grep -q "$id"; then
    say "  STILL IN ARCHIVE (would be restored by [1/7]): $id"; BAD=1
  fi
done
[ "$BAD" -eq 1 ] && { say "REFUSING to render -- a blocked clip can still reach the film."; exit 1; }
for v in U004 U012 U023 U027; do
  if ls remotion/public/uri/motion/ 2>/dev/null | grep -q "^${v}.mp4"; then say "  FACE CLIP STILL IN POOL: $v"; BAD=1; fi
  if ls /e/pd-media/assets/ai_video/uri/motion/ 2>/dev/null | grep -q "^${v}.mp4"; then say "  FACE CLIP STILL IN ARCHIVE: $v"; BAD=1; fi
done
[ "$BAD" -eq 1 ] && { say "REFUSING to render -- a blocked clip can still reach the film."; exit 1; }
say "  clean: none of the seven stock clips and none of the four face clips is in the pool or the archive"

# ---- 2. take the card off ComfyUI ------------------------------------------------------------
say "stopping the i2v chain"
for pid in $(ps -ef 2>/dev/null | grep -E "_chain_i2v|i2v_episode_batch" | grep -v grep | awk '{print $2}'); do
  kill "$pid" 2>/dev/null
done
sleep 8
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
  say "REFUSING to render into ${used} MiB of occupied VRAM."; exit 1
fi

# ---- 3. render --------------------------------------------------------------------------------
export PD_RENDER_CONCURRENCY=4
say "START uri (Ep73Uri, EP73) at concurrency=$PD_RENDER_CONCURRENCY"
py -3.11 scripts/check_still_luma.py --slug uri >> "$LOG" 2>&1 || {
  say "SKIP -- a backdrop is cut in as a picture"; exit 1; }
bash scripts/_finish_episode.sh uri Ep73Uri 73 >> out_finish_uri.log 2>&1
RC=$?
say "END uri rc=$RC"
tail -4 out_finish_uri.log | tee -a "$LOG"

# ---- 4. verify against the film THAT WAS RENDERED, not the one on the bench -------------------
if [ "$RC" -eq 0 ]; then
  say "checking the RENDERED snapshot (not remotion/src/data/uri_film.json) for blocked ids"
  py -3.11 - <<'PY' | tee -a "$LOG"
import json, pathlib
p = pathlib.Path('episodes/PD-2026-073-uri/08_edit/uri_film.rendered.json')
f = json.loads(p.read_text(encoding='utf-8'))
bad = ['10008320', '10008388', '10058364', '10058463', '12891229', '30243440', '30243437',
       'U004', 'U012', 'U023', 'U027']
hits = [pathlib.Path(c.get('src', '')).stem for c in (f.get('cuts') or [])
        if any(b in pathlib.Path(c.get('src', '')).stem for b in bad)]
print(f"[uri5] rendered film: {len(f.get('cuts') or [])} cuts, blocked present: {hits or 'NONE'}")
PY
fi

say "restarting the i2v chain"
nohup bash scripts/_chain_i2v_ep78_82.sh >> runs/logs/i2v_queue_relaunch_20260901.log 2>&1 &
say "i2v launched pid=$!"

if [ "$RC" -ne 0 ]; then
  say "!! FAILED rc=$RC -- uri has NO new master. The 12:00 slot cannot be filled from this run."
  exit 1
fi
say "master written. NOW READ IT AGAIN -- these are new bytes, and the read that found the five"
say "marks describes the OLD ones. Read 0:00-8:00 first: that is where all five were."
