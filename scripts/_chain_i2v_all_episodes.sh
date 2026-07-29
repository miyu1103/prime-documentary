#!/bin/bash
# Unattended i2v for every EP51-56 episode that still needs it, strictly one at a time.
#
# Order is by how close each episode is to being finishable, so the earliest completions are
# the most useful: flowers and morton only need their 16 faces (their M plates are already
# animated), then the four episodes that need both M plates and faces.
#
# Each episode runs through _chain_i2v_robust.sh, which restarts ComfyUI fresh per chunk
# (Wan leaks VRAM into a hard crash around 20-30 clips), holds a single-instance lock,
# resumes from the frame dirs on disk rather than any counter, and assembles as it goes.
#
# Measured: ~206s per clip on the 4090. The whole queue is ~15h, so run it overnight and
# NEVER alongside a render -- the GPU takes exactly one job.
#
#   scripts/_chain_i2v_all_episodes.sh            # everything still missing
#   scripts/_chain_i2v_all_episodes.sh morton norfolk
set -u
cd /c/Users/aab15/Documents/prime-documentary

LOCK="out_i2v_all.lock"
if [ -f "$LOCK" ] && kill -0 "$(cat "$LOCK" 2>/dev/null)" 2>/dev/null; then
  echo "[all] another queue (pid $(cat "$LOCK")) is running -- refusing to double-launch"; exit 0
fi
echo $$ > "$LOCK"
trap 'rm -f "$LOCK"' EXIT
LOG="out_i2v_all.log"

# slug : kinds : target   (target = how many frame dirs mean "done" for that kind set)
JOBS=(
  "flowers:P:16"
  "morton:P:16"
  "willingham:M:30"
  "willingham:P:32"
  "norfolk:M:42"
  "norfolk:P:16"
  "burge:M:42"
  "burge:P:16"
  "postoffice:M:42"
  "postoffice:P:16"
)

want="${*:-}"
echo "[all] START $(date)  filter='${want:-none}'" | tee -a "$LOG"

for job in "${JOBS[@]}"; do
  slug="${job%%:*}"; rest="${job#*:}"; kinds="${rest%%:*}"; target="${rest##*:}"
  if [ -n "$want" ] && ! echo " $want " | grep -q " $slug "; then continue; fi

  # count only the frame dirs for THIS kind, so an M target is not satisfied by P clips
  done_n=0
  for d in /c/Users/aab15/ae-demo/wan_frames_${slug}_${kinds}*; do
    [ -d "$d" ] || continue
    [ "$(ls "$d"/*.png 2>/dev/null | wc -l)" -ge 40 ] && done_n=$((done_n+1))
  done
  if [ "$done_n" -ge "$target" ]; then
    echo "[all] $slug/$kinds already complete ($done_n/$target) -- skip" | tee -a "$LOG"
    continue
  fi

  echo "[all] === $slug kinds=$kinds $done_n/$target $(date) ===" | tee -a "$LOG"
  py -3.11 scripts/pd_gpu_lock.py i2v >> "$LOG" 2>&1 || {
    echo "[all] GPU not free for $slug -- aborting queue" | tee -a "$LOG"; exit 1; }
  # the per-episode chain's own target counts ALL of that slug's frame dirs, so pass the
  # cumulative figure: whatever is already done for other kinds, plus this kind's target
  other=0
  for d in /c/Users/aab15/ae-demo/wan_frames_${slug}_*; do
    [ -d "$d" ] || continue
    case "$(basename "$d")" in wan_frames_${slug}_${kinds}*) ;; *)
      [ "$(ls "$d"/*.png 2>/dev/null | wc -l)" -ge 40 ] && other=$((other+1)) ;; esac
  done
  bash scripts/_chain_i2v_robust.sh "$slug" "$((target + other))" "$kinds" 8 >> "$LOG" 2>&1
  echo "[all] $slug/$kinds chain returned $(date)" | tee -a "$LOG"
done

echo "[all] QUEUE DONE $(date)" | tee -a "$LOG"
for slug in flowers morton willingham norfolk burge postoffice; do
  n=$(ls "H:/pd-media/assets/ai_video/${slug}/motion/"*.mp4 2>/dev/null | wc -l)
  echo "[all] $slug motion mp4 = $n" | tee -a "$LOG"
done
echo "[all] NEXT: rebuild manifests -> film.json -> pre-gate -> ONE render each" | tee -a "$LOG"
