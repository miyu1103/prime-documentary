#!/usr/bin/env bash
# Render EP77 keybridge, EP81 station and EP72 lacmegantic, in slot order, after the uri render.
#
# DO NOT START THIS UNTIL THE Figures.Timeline FIX HAS BEEN LOOKED AT (commit 4bff2186).
# It is committed and tsc-clean and it has NOT been rendered once. The whole point of this
# night's work is that a green check is not a look. Render a Timeline beat, open the frame, and
# only then run this. The guard below refuses to start without the marker file that step writes.
#
# WHY EACH EPISODE IS HERE
#   keybridge  3 clips carrying MSC / MAERSK / ONE livery and a branded radio were blocked, which
#              took the stock pool under MIN_FACTORY; it has since been topped up 39 -> 51 with
#              every new clip read before staging. Slot 09-03.
#   station    3 plates a reviewer REJECTED on 08-27 were cut into the shipped master anyway --
#              a glass-strewn floor and an overturned chair under the card "REPORTED THAT NIGHT.
#              440 TO 458.", both barred by this episode's own forbidden_subjects, and a truss
#              bridge drawing that belongs to a different film. Slot 09-04.
#   lacmegantic 7 clips blocked (the UTLX 663976 / THE UNION TANK CAR CO stencil, an unresolvable
#              excavator wordmark, a sibling of EP73's Russian switchgear, a metro platform and a
#              steam locomotive that are both in this episode's forbidden_subjects, Indian
#              Railways stock, and a wildfire cut under the line about the small Nantes fire) and
#              three false cards corrected at their source. Slot 09-02.
# All three also pick up the lower-third width fix, the Timeline wrap/clamp, and the disclosure
# fix that stops the AI-disclosure card overwriting the film's closing kinetic statement.
#
# ORDER. lacmegantic publishes FIRST (09-02) but is rendered LAST, deliberately: it is the only
# one of the three whose read is still incomplete (2 of 4 ranges in), so its blocklist may still
# grow. Rendering it last buys the readers the most time. If its read lands early, reorder.
set -uo pipefail
cd "$(dirname "$0")/.." || exit 1

LOG=runs/logs/render_queue_20260901.log
say(){ echo "[q] $(date '+%m-%d %H:%M:%S') $*" | tee -a "$LOG"; }

if [ ! -f runs/qc/timeline_fix_looked_at.txt ]; then
  say "REFUSING: runs/qc/timeline_fix_looked_at.txt does not exist."
  say "The Figures.Timeline fix has not been rendered and looked at. Do that first:"
  say "  cd remotion && npx remotion render <Comp> ../out_qc/tl.mp4 --public-dir=<pub> --frames=A-B"
  say "  then open the frame, then: echo 'looked at <frame>' > runs/qc/timeline_fix_looked_at.txt"
  exit 1
fi
say "timeline fix marker present: $(cat runs/qc/timeline_fix_looked_at.txt)"

say "waiting for the uri render to finish (3h ceiling)"
for _ in $(seq 1 360); do
  grep -qE "master written|FAILED rc=|REFUSING" runs/logs/render_uri_20260901.log 2>/dev/null && break
  sleep 30
done
if ! grep -qE "master written|FAILED rc=|REFUSING" runs/logs/render_uri_20260901.log 2>/dev/null; then
  say "uri did not finish within 3h -- NOT starting. A human should look."
  exit 1
fi
say "uri finished: $(grep -E 'master written|FAILED rc=|REFUSING' runs/logs/render_uri_20260901.log | tail -1)"

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

export PD_RENDER_CONCURRENCY=4
FAILED=""
run_one() {
  local slug="$1" comp="$2" nn="$3"
  say "START $slug ($comp, EP$nn)"
  py -3.11 scripts/check_episode_inputs.py --slug "$slug" 2>&1 | tail -1 | tee -a "$LOG" | grep -q "READY to build" || {
    say "SKIP $slug -- inputs not READY"; FAILED="$FAILED $slug(inputs)"; return 1; }
  py -3.11 scripts/check_still_luma.py --slug "$slug" >> "$LOG" 2>&1 || {
    say "SKIP $slug -- a backdrop is cut in as a picture"; FAILED="$FAILED $slug(still-luma)"; return 1; }
  bash scripts/_finish_episode.sh "$slug" "$comp" "$nn" >> "out_finish_${slug}.log" 2>&1
  local rc=$?
  say "END $slug rc=$rc"
  tail -3 "out_finish_${slug}.log" | tee -a "$LOG"
  if [ $rc -ne 0 ]; then FAILED="$FAILED $slug(rc=$rc)"; return $rc; fi
  # The check that uri needed and did not have: read the film THE RENDER wrote, not the bench one.
  py -3.11 - "$slug" <<'PY' | tee -a "$LOG"
import glob, json, pathlib, sys
sys.path.insert(0, 'scripts')
import pd_footage_blocklist as bl
slug = sys.argv[1]
g = glob.glob(f'episodes/PD-*-{slug}/08_edit/{slug}_film.rendered.json')
if not g:
    print(f"[q] {slug}: NO rendered film snapshot -- cannot verify"); raise SystemExit
f = json.loads(pathlib.Path(g[0]).read_text(encoding='utf-8'))
blocked = bl.load_blocked(slug)
hits = sorted({s for c in (f.get('cuts') or [])
               for s in [pathlib.Path(c.get('src', '')).stem]
               if any(b in s for b in blocked)})
print(f"[q] {slug}: rendered film has {len(f.get('cuts') or [])} cuts, blocked present: {hits or 'NONE'}")
PY
  return 0
}
run_one keybridge   Ep77KeyBridge   77 || say "continuing past keybridge"
run_one station     Ep81Station     81 || say "continuing past station"
run_one lacmegantic Ep72Lacmegantic 72 || say "continuing past lacmegantic"

say "restarting the i2v chain"
nohup bash scripts/_chain_i2v_ep78_82.sh >> runs/logs/i2v_queue_relaunch_20260901.log 2>&1 &
say "i2v launched pid=$!"

if [ -n "$FAILED" ]; then
  say "!! FINISHED WITH FAILURES:$FAILED -- those episodes have NO new master."
else
  say "three masters written."
fi
say "NONE OF THEM IS READ. Every master rendered tonight had defects that only a human reading"
say "the pixels found -- and twice this week the worst one was invisible on the contact sheets"
say "and had to be re-sampled from the master at 4 fps. Read them before booking anything."
