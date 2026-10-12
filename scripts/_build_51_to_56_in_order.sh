#!/bin/bash
# Owner order 2026-07-30 ("51から順番ずつ組み立てていって"): build EP51..EP56 strictly in
# episode order, one at a time, unattended.
#
# For each episode: run the i2v chain for it first (a no-op when its clips are already on
# disk), then _finish_episode.sh (assemble -> manifest -> film.json -> slim public dir ->
# guarded render -> BGM/master-VO -> post-render gate). i2v and render never overlap,
# because the single 4090 takes exactly one job.
#
# EP54 already has a v001 master; it is rebuilt here because that one came from the pool
# before the era-inappropriate / weak-tier clips were pruned.
#
# A failing episode is recorded and the queue moves on. The summary at the end is the
# authority; every finished mp4 still has to be WATCHED before it is shown to the owner.
#
#   scripts/_build_51_to_56_in_order.sh              # 51 -> 56
#   scripts/_build_51_to_56_in_order.sh norfolk      # a subset, same order
set -u
cd /c/Users/aab15/Documents/prime-documentary

LOCK="out_build_51_56.lock"
if [ -f "$LOCK" ] && kill -0 "$(cat "$LOCK" 2>/dev/null)" 2>/dev/null; then
  echo "[queue] another run (pid $(cat "$LOCK")) is active -- refusing to double-launch"; exit 0
fi
echo $$ > "$LOCK"
trap 'rm -f "$LOCK"' EXIT
LOG="out_build_51_56.log"

# episode order : slug : composition id : public dir number
JOBS=(
  "willingham:Ep51Willingham:51"
  "morton:Ep52Morton:52"
  "norfolk:Ep53Norfolk:53"
  "flowers:Ep54Flowers:54"
  "burge:Ep55Burge:55"
  "postoffice:Ep56Postoffice:56"
)

want="${*:-}"
echo "[queue] START $(date) filter='${want:-51..56}'" | tee -a "$LOG"

ok=(); bad=()
for job in "${JOBS[@]}"; do
  slug="${job%%:*}"; rest="${job#*:}"; comp="${rest%%:*}"; num="${rest##*:}"
  if [ -n "$want" ] && ! echo " $want " | grep -q " $slug "; then continue; fi

  echo "[queue] === $slug ($comp) i2v pass $(date) ===" | tee -a "$LOG"
  bash scripts/_chain_i2v_all_episodes.sh "$slug" >> "$LOG" 2>&1
  echo "[queue] === $slug ($comp) finish pass $(date) ===" | tee -a "$LOG"
  if bash scripts/_finish_episode.sh "$slug" "$comp" "$num" >> "$LOG" 2>&1; then
    ok+=("$slug"); echo "[queue] $slug OK $(date)" | tee -a "$LOG"
  else
    bad+=("$slug"); echo "[queue] $slug FAILED -- see out_finish_${slug}.log" | tee -a "$LOG"
  fi
done

echo "[queue] DONE $(date)" | tee -a "$LOG"
echo "[queue] finished: ${ok[*]:-none}" | tee -a "$LOG"
echo "[queue] failed:   ${bad[*]:-none}" | tee -a "$LOG"
for slug in "${ok[@]:-}"; do
  [ -n "$slug" ] || continue
  f=$(ls episodes/PD-2026-0*-${slug}/08_edit/${slug}_final_bgm.v*.mp4 2>/dev/null | tail -1)
  [ -n "$f" ] && echo "[queue]   $slug -> $f ($(stat -c%s "$f") bytes)" | tee -a "$LOG"
done
