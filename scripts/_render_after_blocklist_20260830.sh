#!/usr/bin/env bash
# Three renders, back to back, after the 2026-08-30 shipped-frames read.
#
#   lacmegantic  Ep72Lacmegantic  72   film rebuilt: 16 clips blocklisted (13 readable
#                                      third-party marks incl. ESSO NEDERLAND, Norfolk Southern
#                                      3073, Canadian Pacific 3777, Skanetrafiken; 3 identifiable
#                                      faces incl. L021/L036, each cut in twice). Audit clean,
#                                      still-luma clean, diversity 0.69 / max reuse 2.
#   uri          Ep73Uri          73   film rebuilt: 7 clips blocklisted (1 shot carrying
#                                      CHEVROLET + SILVERADO + TEREX + fleet 906992 + a licence
#                                      plate; 6 identifiable faces incl. the ~9s smiling woman).
#                                      Audit clean, still-luma clean, diversity 0.70 / max 2.
#   keybridge    Ep77KeyBridge    77   first render. Its caption blocker is fixed and its 17
#                                      invented-person clips were regenerated and verified clip
#                                      by clip. NOT yet shipped-frames read -- do that after.
#
# WHY NOT scripts/_render_queue_tonight.sh: that queue also renders concordia, which is ALREADY
# BOOKED (video o98hKLTK93g, 08-31 12:00 JST) against sha f0add8ed. Re-rendering it would produce
# different bytes and break the binding its acceptance receipt and shipped-frames review both
# name. Never re-render a booked master.
#
# The GPU was cleared before this started: the i2v chain was stopped and ComfyUI killed as a tree
# (killing the parent alone orphans a child that keeps ~18 GB at 100%, which is what happened
# tonight and is why kill_comfy exists). Restart i2v with scripts/_chain_i2v_ep78_82.sh when this
# queue is done -- it resumes from the delivered mp4s on disk. State at stop time:
#   concordia 184  station 184  valdez 40  colgan 0  alaska261 0  max737 0  threemile 0  katrina 0
#
# Does NOT stop on failure: a film that fails must not cost the two behind it their slot.
set -uo pipefail
cd "$(dirname "$0")/.." || exit 1

run_one() {
  local slug="$1" comp="$2" nn="$3"
  echo "=============================================================="
  echo "$(date '+%m-%d %H:%M:%S')  START  $slug ($comp, EP$nn)"
  echo "=============================================================="
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
           "keybridge Ep77KeyBridge 77"; do
  # shellcheck disable=SC2086
  run_one $job || echo "$(date '+%H:%M:%S')  continuing past a failure -- the queue does not stop"
done

echo "$(date '+%m-%d %H:%M:%S')  QUEUE DONE. Masters to verify (do NOT trust these exit codes):"
for s in lacmegantic uri keybridge; do
  m=$(ls episodes/PD-2026-0*-"$s"/08_edit/"${s}"_final_bgm.v001.mp4 2>/dev/null | head -1)
  [ -n "$m" ] && printf '  %-12s %s  %s\n' "$s" "$m" "$(stat -c %y "$m" 2>/dev/null | cut -c1-19)"
done
echo "Then, for each: read the shipped frames before booking. Tonight's read found 139 defects"
echo "across three masters that every machine gate had passed."
