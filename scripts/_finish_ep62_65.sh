#!/bin/bash
# Build EP62-65 review masters in sequence. The owner asked to complete all four assemblies.
# Their commissioned stills and reviewed motion are present, but the strict no-video-reuse
# contract remains red. This queue records that deviation; it never treats the result as publishable.
set -u
cd /c/Users/aab15/Documents/prime-documentary

JOBS=(
  "greene:Ep62Greene:62"
  "correa:Ep63Correa:63"
  "memphis:Ep64Memphis:64"
  "marmet:Ep65Marmet:65"
)

LOG="out_finish_ep62_65.log"
echo "[finish-62-65] START $(date)" | tee -a "$LOG"
ok=()
bad=()

for job in "${JOBS[@]}"; do
  slug="${job%%:*}"
  rest="${job#*:}"
  comp="${rest%%:*}"
  num="${rest##*:}"
  echo "[finish-62-65] === $slug ($comp) $(date) ===" | tee -a "$LOG"
  if bash scripts/_finish_episode.sh "$slug" "$comp" "$num" \
      --allow-video-diversity-deviation >> "$LOG" 2>&1; then
    ok+=("$slug")
    echo "[finish-62-65] $slug OK" | tee -a "$LOG"
  else
    bad+=("$slug")
    echo "[finish-62-65] $slug FAILED -- see out_finish_${slug}.log" | tee -a "$LOG"
  fi
done

echo "[finish-62-65] DONE $(date)" | tee -a "$LOG"
echo "[finish-62-65] finished: ${ok[*]:-none}" | tee -a "$LOG"
echo "[finish-62-65] failed:   ${bad[*]:-none}" | tee -a "$LOG"
test ${#bad[@]} -eq 0
