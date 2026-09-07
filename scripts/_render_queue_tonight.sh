#!/usr/bin/env bash
# Render the five episodes whose i2v is already complete, back to back, so the card is never idle.
#
# Order is by publish date, soonest first, so a failure late in the night costs the slot with
# the most slack rather than the least:
#
#   lacmegantic  8/29  re-render: a GWR intercity at Paddington and a COSCO/EVERGREEN container
#                      rake were cut into a film about a Quebec runaway freight, and three
#                      plates were empty grounds. All removed, film rebuilt, still-luma clean.
#   uri          8/30  re-render: the bar chart at 14:32-14:37 was captioned FORFEITURE CASES /
#                      YEAR, a string hardcoded in Figures.tsx that every bar-chart episode got.
#                      Component fixed; the film itself needs no change, only a new render.
#   keybridge    8/31  first render, after the 17 invented-people clips are regenerated
#   concordia    9/1   first render
#   station      9/2   first render
#
# Each render is ~1h30m-2h. Five is roughly nine hours, so from a 23:00 start the last one
# lands around 08:00 and every slot keeps more than a day of margin.
#
# WHY A SCRIPT AND NOT FIVE COMMANDS: the GPU is the constraint for the next four days, and a
# card that sits idle between 02:00 and 09:00 because nobody was awake to start the next one is
# the whole schedule slipping. This starts the next one the moment the previous exits.
#
# It does NOT stop on failure. A film that fails its post-render gate must not block the four
# behind it -- the failure is recorded and the queue moves on, because a second episode's slot
# is worth more than a tidy log.
set -uo pipefail
cd "$(dirname "$0")/.." || exit 1

run_one() {
  local slug="$1" comp="$2" nn="$3"
  echo "=============================================================="
  echo "$(date '+%m-%d %H:%M:%S')  START  $slug ($comp, EP$nn)"
  echo "=============================================================="
  # Pre-render, cheap, and each has already caught a wasted render this week:
  #   still-luma  -- EP76 burned 2h36m on 4.43s of black from an empty backdrop plate
  #   inputs      -- names every missing input in one pass instead of failing at [4/7]
  py -3.11 scripts/check_still_luma.py --slug "$slug" || {
    echo "$(date '+%H:%M:%S')  SKIP $slug -- a backdrop is cut in as a picture. Fix, then re-queue."
    return 1
  }
  bash scripts/_finish_episode.sh "$slug" "$comp" "$nn" >> "out_finish_${slug}.log" 2>&1
  local rc=$?
  echo "$(date '+%m-%d %H:%M:%S')  END    $slug rc=$rc"
  tail -4 "out_finish_${slug}.log"
  return $rc
}

for job in "lacmegantic Ep72Lacmegantic 72" \
           "uri Ep73Uri 73" \
           "keybridge Ep77KeyBridge 77" \
           "concordia Ep80Concordia 80" \
           "station Ep81Station 81"; do
  # shellcheck disable=SC2086
  run_one $job || echo "$(date '+%H:%M:%S')  continuing past a failure -- the queue does not stop"
done

echo "$(date '+%m-%d %H:%M:%S')  QUEUE DONE. Masters to verify (do NOT trust these exit codes):"
for s in lacmegantic uri keybridge concordia station; do
  m=$(ls episodes/PD-2026-0*-"$s"/08_edit/"${s}"_final_bgm.v001.mp4 2>/dev/null | head -1)
  [ -n "$m" ] && printf '  %-12s %s\n' "$s" "$m"
done
