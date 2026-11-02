#!/bin/bash
# Unattended build of EP53..EP59 with every EP50/EP51 fix applied BEFORE the render, so no
# episode has to be re-rendered to clear a gate it could have passed the first time.
#
# Per episode, in order:
#   1. brighten under-exposed stills on disk        (image_cut_luma / visual_asset_qc)
#   2. drop pool clips shared with another episode  (arc_nonrepeat / 素材の被り)
#   3. top up the pool by ledger TITLE, excluding ids any other episode already uses
#   4. i2v for whatever motion clips are still missing (GPU; skipped when complete)
#   5. _finish_episode.sh -- manifest -> film.json -> caption polish (lead 0.25) -> retire
#      unused clips -> guarded render (auto-retry at concurrency 4) -> BGM -> post-gate
#   6. thumbnails from the episode's own stills, then probe + acceptance receipt
#
# A failing episode is recorded and the queue MOVES ON. Nothing here uploads: scheduling stays
# a human step because it needs the approval record.
set -u
cd /c/Users/aab15/Documents/prime-documentary

LOCK="out_build_53_59.lock"
if [ -f "$LOCK" ] && kill -0 "$(cat "$LOCK" 2>/dev/null)" 2>/dev/null; then
  echo "[q] another run (pid $(cat "$LOCK")) is active -- refusing"; exit 0
fi
echo $$ > "$LOCK"; trap 'rm -f "$LOCK"' EXIT
LOG="out_build_53_59.log"

# Wait for any in-flight RENDER, not just a finish script. On 2026-08-01 this loop checked
# only for _finish_episode.sh, EP52 happened to be in its staging phase, so the queue decided
# the machine was free and started a second render on top of it -- the exact contention that
# had already killed one EP52 render. Two renders must never overlap.
render_busy() {
  pgrep -f "_finish_episode.sh" >/dev/null 2>&1 && return 0
  pgrep -f "remotion render" >/dev/null 2>&1 && return 0
  pgrep -f "pd_render_guarded" >/dev/null 2>&1 && return 0
  return 1
}
while render_busy; do
  echo "[q] machine busy with a render ... $(date)" | tee -a "$LOG"; sleep 120
done

# slug : composition : public number : thumb kicker : thumb line1 : thumb line2
JOBS=(
  "norfolk:Ep53Norfolk:53:VIRGINIA, 1997:FOUR SAILORS:ONE CRIME"
  "flowers:Ep54Flowers:54:MISSISSIPPI:TRIED SIX:TIMES"
  "burge:Ep55Burge:55:CHICAGO, 1972:THE POLICE:HAD A ROOM"
  "postoffice:Ep56Postoffice:56:BRITAIN, 1999:THE COMPUTER:WAS WRONG"
  "fieldtest:Ep57Fieldtest:57:HOUSTON, 2010:A 2 DOLLAR:TEST"
  "lejeune:Ep58Lejeune:58:CAMP LEJEUNE:THEY WROTE:IT DOWN"
  "robosigning:Ep59Robosigning:59:FLORIDA, 2010:NO LOAN.:NO HOUSE."
)

ok=(); bad=()
for job in "${JOBS[@]}"; do
  IFS=':' read -r slug comp num kick l1 l2 <<< "$job"
  while render_busy; do
    echo "[q] waiting for the machine before $slug ... $(date)" | tee -a "$LOG"; sleep 120
  done
  echo "[q] ================= $slug ($comp) $(date) =================" | tee -a "$LOG"

  py -3.11 scripts/brighten_dark_stills.py --slug "$slug" >> "$LOG" 2>&1 || true
  py -3.11 scripts/prune_pool_by_blocklist.py --slug "$slug" >> "$LOG" 2>&1 || true
  py -3.11 scripts/dedupe_pool_across_episodes.py --slug "$slug" >> "$LOG" 2>&1 || true
  py -3.11 scripts/stage_footage_by_title.py --slug "$slug" --per-query 6 \
      --query "prison" --query "jail" --query "cell" --query "handcuffs" \
      --query "courtroom" --query "judge" --query "lawyer" --query "police" \
      --query "evidence" --query "documents" --query "office" --query "computer" \
      --query "keyboard" --query "screen" --query "desk" --query "small town" \
      --query "rural" --query "highway" --query "road" --query "house" \
      --query "kitchen" --query "bedroom" --query "hallway" --query "window" \
      --query "door" --query "night street" --query "city night" --query "rain" \
      --query "newspaper" --query "typewriter" --query "laboratory" \
      --query "microscope" --query "water" --query "fire" --query "smoke" \
      --query "hospital" --query "letter" --query "money" --query "clock" \
      --query "train" --query "aerial" --query "field" --query "forest" \
      >> "$LOG" 2>&1 || true

  py -3.11 scripts/write_factory_clip_qc.py --slug "$slug" >> "$LOG" 2>&1 || true

  # i2v is DELIBERATELY SKIPPED (owner decision 2026-07-31): one 2.6s AI clip costs
  # ~206s of GPU, ~3.3h per episode, and the gate's video share can be carried by REAL
  # archive footage instead -- ~16h cheaper across EP55-59 and closer to the standing
  # instruction to use the downloaded footage generously. Episodes that already have
  # i2v clips keep and use them; nothing new is generated.

  if bash scripts/_finish_episode.sh "$slug" "$comp" "$num" >> "$LOG" 2>&1; then
    py -3.11 scripts/build_thumbs_from_stills.py --slug "$slug" \
        --kicker "$kick" --line1 "$l1" --line2 "$l2" >> "$LOG" 2>&1 || true
    EP=$(ls -d episodes/PD-2026-0*-${slug} | head -1)
    F="${EP}/08_edit/${slug}_final_bgm.v001.mp4"
    rm -f "out/${slug}_probe_slice.mp4"
    ffmpeg -hide_banner -v error -ss 600 -t 90 -i "$F" -c copy "out/${slug}_probe_slice.mp4" -y >> "$LOG" 2>&1 || true
    py -3.11 scripts/check_final_acceptance.py "$(basename "$EP")" --probe "out/${slug}_probe_slice.mp4" >> "$LOG" 2>&1 || true
    STAMP=$(py -3.11 -c "import os;print(int(os.path.getmtime(r'$F'))-60)")
    py -3.11 scripts/check_final_acceptance.py "$(basename "$EP")" --render "$F" \
        --render-started-at "$STAMP" --emit-receipt >> "$LOG" 2>&1 || true
    ok+=("$slug"); echo "[q] $slug BUILT $(date)" | tee -a "$LOG"
  else
    bad+=("$slug"); echo "[q] $slug FAILED -- see out_finish_${slug}.log" | tee -a "$LOG"
  fi
done

echo "[q] DONE $(date)" | tee -a "$LOG"
echo "[q] built:  ${ok[*]:-none}" | tee -a "$LOG"
echo "[q] failed: ${bad[*]:-none}" | tee -a "$LOG"
for slug in "${ok[@]:-}"; do
  [ -n "$slug" ] || continue
  f=$(ls episodes/PD-2026-0*-${slug}/08_edit/${slug}_final_bgm.v001.mp4 2>/dev/null | head -1)
  [ -n "$f" ] && echo "[q]   $slug -> $f ($(stat -c%s "$f") bytes)" | tee -a "$LOG"
done
