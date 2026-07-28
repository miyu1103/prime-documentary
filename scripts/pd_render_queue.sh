#!/bin/bash
# Serialised render queue for PD long-form episodes.
#
# Renders are GPU/WebGL work and MUST NOT overlap (feedback: serialize-heavy-renders --
# two at once on the 4090 is a silent VRAM crash with no output). This runs them strictly
# one at a time through pd_render_guarded.sh, so each one still gets its pre-render gate
# before it starts and its post-render gate before it counts as done.
#
#   scripts/pd_render_queue.sh willingham morton norfolk burge postoffice
#
# A failing episode does NOT stop the queue: it is recorded and the next one starts, so an
# unattended overnight run cannot be wiped out by one bad input. The summary at the end is
# the authority -- read it, then watch each finished film end to end before showing anyone.
#
# DO NOT launch this until at least one episode has been rendered AND watched: queueing
# every episode before inspecting one is ship-then-inspect at scale, and a systemic defect
# would cost the whole queue (feedback-no-render-churn).
set -u
cd /c/Users/aab15/Documents/prime-documentary

LOCK="out_render_queue.lock"
if [ -f "$LOCK" ] && kill -0 "$(cat "$LOCK" 2>/dev/null)" 2>/dev/null; then
  echo "[queue] another queue (pid $(cat "$LOCK")) is running -- refusing to double-launch"
  exit 0
fi
echo $$ > "$LOCK"
trap 'rm -f "$LOCK"' EXIT

LOG="out_render_queue.log"
declare -A COMP=( [willingham]=Ep51Willingham [morton]=Ep52Morton [norfolk]=Ep53Norfolk \
                  [flowers]=Ep54Flowers [burge]=Ep55Burge [postoffice]=Ep56Postoffice )
declare -A PUBN=( [willingham]=51 [morton]=52 [norfolk]=53 [flowers]=54 [burge]=55 [postoffice]=56 )

ok=(); bad=()
for slug in "$@"; do
  comp="${COMP[$slug]:-}"; num="${PUBN[$slug]:-}"
  if [ -z "$comp" ]; then echo "[queue] unknown slug $slug -- skipped" | tee -a "$LOG"; bad+=("$slug(unknown)"); continue; fi
  film="remotion/src/data/${slug}_film.json"
  pub="remotion/public_ep${num}"
  out="out/${slug}.mp4"
  if [ -f "$out" ]; then
    echo "[queue] $slug already rendered ($out) -- skipping (delete it to force)" | tee -a "$LOG"
    ok+=("$slug(existing)"); continue
  fi
  # expected duration straight from the film the render will consume
  expect=$(py -3.11 -c "import json;d=json.load(open(r'$film',encoding='utf-8'));print(round(d['narrationSeconds']+d['hookSeconds']+3.5+9.0,1))")
  echo "[queue] === $slug -> $comp ($expect s) $(date) ===" | tee -a "$LOG"
  bash scripts/pd_render_guarded.sh "$comp" "$film" "$pub" "$out" "$expect" >> "$LOG" 2>&1
  rc=$?
  if [ $rc -eq 0 ] && [ -f "$out" ]; then
    echo "[queue] $slug PASSED both gates -> $out" | tee -a "$LOG"; ok+=("$slug")
  else
    echo "[queue] $slug FAILED rc=$rc (see $LOG and out_render_${slug}.mp4.log)" | tee -a "$LOG"; bad+=("$slug")
  fi
done

echo "[queue] DONE $(date)" | tee -a "$LOG"
echo "[queue] passed: ${ok[*]:-none}" | tee -a "$LOG"
echo "[queue] failed: ${bad[*]:-none}" | tee -a "$LOG"
echo "[queue] NEXT per episode: build_case_bgm_generic.py -> pd_postrender_gate.py -> WATCH IN FULL" | tee -a "$LOG"
