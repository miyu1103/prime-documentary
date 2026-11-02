#!/bin/bash
# Finish every EP51-56 episode in sequence once i2v is done.
#
# Each episode goes through _finish_episode.sh (assemble -> manifest -> film.json -> slim
# public dir -> guarded render -> BGM -> post-gate). Renders are GPU work and are therefore
# strictly serial; this must not run while the i2v queue is still going.
#
# A failing episode is recorded and the queue moves on, so one bad input cannot cost the
# whole unattended run. The summary at the end is the authority.
#
#   scripts/_finish_all_episodes.sh                 # all six
#   scripts/_finish_all_episodes.sh morton norfolk  # a subset
#
# EP54 is included even though it already has a v001 master: that master was built from the
# pool before the era-inappropriate clips were pruned, so it is rebuilt here with the rest.
set -u
cd /c/Users/aab15/Documents/prime-documentary

LOCK="out_finish_all.lock"
if [ -f "$LOCK" ] && kill -0 "$(cat "$LOCK" 2>/dev/null)" 2>/dev/null; then
  echo "[finish-all] another run (pid $(cat "$LOCK")) is active -- refusing to double-launch"; exit 0
fi
echo $$ > "$LOCK"
trap 'rm -f "$LOCK"' EXIT
LOG="out_finish_all.log"

# slug : composition id : public dir number
JOBS=(
  "flowers:Ep54Flowers:54"
  "morton:Ep52Morton:52"
  "willingham:Ep51Willingham:51"
  "norfolk:Ep53Norfolk:53"
  "burge:Ep55Burge:55"
  "postoffice:Ep56Postoffice:56"
)

want="${*:-}"
echo "[finish-all] START $(date) filter='${want:-all}'" | tee -a "$LOG"

ok=(); bad=()
for job in "${JOBS[@]}"; do
  slug="${job%%:*}"; rest="${job#*:}"; comp="${rest%%:*}"; num="${rest##*:}"
  if [ -n "$want" ] && ! echo " $want " | grep -q " $slug "; then continue; fi
  echo "[finish-all] === $slug ($comp) $(date) ===" | tee -a "$LOG"
  if bash scripts/_finish_episode.sh "$slug" "$comp" "$num" >> "$LOG" 2>&1; then
    ok+=("$slug")
    echo "[finish-all] $slug OK" | tee -a "$LOG"
  else
    bad+=("$slug")
    echo "[finish-all] $slug FAILED -- see out_finish_${slug}.log" | tee -a "$LOG"
  fi
done

echo "[finish-all] DONE $(date)" | tee -a "$LOG"
echo "[finish-all] finished: ${ok[*]:-none}" | tee -a "$LOG"
echo "[finish-all] failed:   ${bad[*]:-none}" | tee -a "$LOG"
for slug in "${ok[@]:-}"; do
  [ -n "$slug" ] || continue
  f=$(ls episodes/PD-2026-0*-${slug}/08_edit/${slug}_final_bgm.v001.mp4 2>/dev/null | head -1)
  [ -n "$f" ] && echo "[finish-all]   $slug -> $f ($(stat -c%s "$f") bytes)" | tee -a "$LOG"
done
echo "[finish-all] NEXT: watch each master END TO END before it is shown to anyone." | tee -a "$LOG"
