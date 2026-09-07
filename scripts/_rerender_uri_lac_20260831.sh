#!/usr/bin/env bash
# Third render pass for EP73 uri and EP72 lacmegantic, after the SECOND shipped-frames read.
#
# WHY A THIRD PASS. Both were re-rendered on 08-30/31 to remove readable marks and identifiable
# faces. Both were then read again, end to end, and the second read found THIRTEEN more cuts the
# first read had missed -- in films that had already been rebuilt to fix exactly this:
#
#   uri          U010 (a man facing camera against sunlit curtains, held ~2s, then in profile) and
#                two cuts showing "HOSELINE INC." on a control panel, ~10s of a legible corporate
#                name. The first read SAW the HOSELINE mark and filed it as a minor note.
#   lacmegantic  a hopper tagged "FUCK JOE BIDEN" with the film's own "47 / People killed" card
#                still fading over it; "KOMATSU" + "PC 400 LC" on two excavator booms; the
#                reporting mark "ADMWX 28157"; and the four remaining clips of the European wagon
#                shoot whose siblings were blocked by name on 08-30 while these stayed in the pool.
#
# Films are already rebuilt and verified BEFORE any GPU is spent:
#   audit_films_vs_blocklist returns nothing for either
#   uri          364 cuts / 253 distinct / 0.70 / max reuse 2
#   lacmegantic  355 cuts / 244 distinct / 0.69 / max reuse 2
#
# PD_RENDER_CONCURRENCY=4 throughout. Two contention failures on 08-30 (uri lost ~50 min, keybridge
# was thrown away entirely at the probe) are enough evidence to stop paying for the faster setting.
#
# Waits for the previous runner to finish rather than racing it, stops i2v and PROVES the card is
# free before rendering, and does NOT report success for a render that failed.
set -uo pipefail
cd "$(dirname "$0")/.." || exit 1

LOG=runs/logs/rerender_uri_lac_20260831.log
say(){ echo "[re3] $(date '+%m-%d %H:%M:%S') $*" | tee -a "$LOG"; }

say "waiting for the keybridge/station runner to finish"
for _ in $(seq 1 360); do          # 3h ceiling
  grep -qE "FINISHED WITH FAILURES|both masters written" runs/logs/render_kb_station_20260831.log 2>/dev/null && break
  sleep 30
done
if ! grep -qE "FINISHED WITH FAILURES|both masters written" runs/logs/render_kb_station_20260831.log 2>/dev/null; then
  say "previous runner did not finish in 3h -- NOT starting. A human should look at it."
  exit 1
fi
say "previous runner finished"

say "stopping i2v (it is restarted by the previous runner and holds ~18-21 GB)"
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
  say "REFUSING to render into ${used} MiB of occupied VRAM."
  exit 1
fi

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
# uri first: it publishes 09-01, lacmegantic 09-02.
run_one uri         Ep73Uri         73 || say "continuing past uri"
run_one lacmegantic Ep72Lacmegantic 72 || say "continuing past lacmegantic"

say "restarting the i2v chain"
nohup bash scripts/_chain_i2v_ep78_82.sh >> runs/logs/i2v_queue_relaunch_20260831.log 2>&1 &
say "i2v launched pid=$!"
sleep 90
say "i2v 90s in: $(tail -1 out_i2v_ep78_82.log 2>/dev/null)"

if [ -n "$FAILED" ]; then
  say "!! FINISHED WITH FAILURES:$FAILED -- those episodes have NO new master."
else
  say "both masters written. Verify on the *_film.rendered.json snapshot beside each."
fi
say "THEN READ THEM AGAIN. Tonight the second read of these same two films found thirteen cuts"
say "the first read missed, including a hopper tagged FUCK JOE BIDEN under the 47-dead card."
