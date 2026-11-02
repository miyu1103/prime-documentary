#!/bin/bash
# EP66-69 i2v, strictly one episode at a time, unattended.
#
# 2026-08-16. Why these four need it at all: _finish_episode.sh stopped openfields at
# check_spec_satisfied with "98 of 185 declared still(s) are in no cut". That is not a gate being
# fussy -- solve_totals splits the cut budget between factory video, motion and stills, and with
# motion=0 the still share caps at 89. Half the plates made FOR the episode never reach the film.
# i2v is what turns those stills into motion clips and lifts the cap. Same arithmetic on all four.
#
# The plate lists are the ones the i2v plans chose (people first: faces and hands are where motion
# changes the film most), not the first N filenames. Extracted from runs/i2v_plans/*_only.csv.
#
# openfields is launched separately and already running when this starts; this waits it out rather
# than racing it. The GPU takes exactly one job -- never run this alongside a render.
#
#   nohup bash scripts/_chain_i2v_ep66_69.sh > out_i2v_ep66_69.log 2>&1 &
set -u
cd /c/Users/aab15/Documents/prime-documentary

LOG="out_i2v_ep66_69.log"
say() { echo "[ep66-69] $* $(date +%H:%M)" | tee -a "$LOG"; }

# slug:target:kinds  -- target counts frame dirs on disk, so a resumed run is correct by
# construction. hyatt already has 15 of its 32 from an earlier session; it needs 17 more.
JOBS="openfields:53:L ramirez:50:R pinto:54:R hyatt:32:H"

for job in $JOBS; do
  slug="${job%%:*}"; rest="${job#*:}"; target="${rest%%:*}"; kinds="${rest##*:}"

  # Wait out any chain already holding this slug -- including the openfields run started by hand.
  while [ -f "out_i2v_${slug}.lock" ] && kill -0 "$(cat "out_i2v_${slug}.lock" 2>/dev/null)" 2>/dev/null; do
    sleep 300
  done

  done_now=$(ls -d /c/Users/aab15/ae-demo/wan_frames_${slug}_* 2>/dev/null | wc -l)
  if [ "$done_now" -ge "$target" ]; then
    say "$slug already at ${done_now}/${target} -- skipping"
    continue
  fi

  only_file="runs/i2v_plans/${slug}_only.csv"
  if [ ! -s "$only_file" ]; then
    say "$slug: no plate list at $only_file -- SKIPPING rather than converting an arbitrary N"
    continue
  fi

  say "$slug START ${done_now}/${target} kinds=$kinds"
  bash scripts/_chain_i2v_robust.sh "$slug" "$target" "$kinds" 6 "$(cat "$only_file")" 121 \
    >> "out_i2v_${slug}_chain.log" 2>&1
  say "$slug END $(ls -d /c/Users/aab15/ae-demo/wan_frames_${slug}_* 2>/dev/null | wc -l)/${target}"
done

say "ALL FOUR DONE -- the GPU is free. Restart the render queue: nohup bash scripts/queue_unattended.sh > out_queue_after_i2v.log 2>&1 &"
