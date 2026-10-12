#!/usr/bin/env bash
# Chunked, resumable render of CaseFilm-rolin to dodge the single-session ANGLE/GPU
# instability that killed the monolithic 68,928-frame render at frame 2976 (exit 1,
# no error line). Each chunk is a FRESH remotion process (resets the browser), skips
# already-completed chunks, retries once on failure, then concats losslessly.
set -u
cd "$(dirname "$0")" || exit 2

COMP="CaseFilm-rolin"
TOTAL=68928            # frames 0..68927 (caseFilmDurationInFrames, verified via `remotion compositions`)
CHUNK=3000
DIR="out/rolin_chunks"
LOG="$DIR/render.log"
mkdir -p "$DIR"
echo "=== chunked render start $(date) TOTAL=$TOTAL CHUNK=$CHUNK ===" | tee -a "$LOG"

BUNDLE="build"   # pre-built once via `npx remotion bundle` -> serves build/public WITHOUT
                 # re-copying the 25GB public dir on every chunk (the big waste we hit).
render_one() {
  local s=$1 e=$2 out=$3
  npx remotion render "$BUNDLE" "$COMP" "$out" \
    --frames="${s}-${e}" \
    --codec=h264 --crf=16 --pixel-format=yuv420p --color-space=bt709 \
    --concurrency=4 --gl=angle >>"$LOG" 2>&1
}

frames_of() {  # echo frame count of an mp4, or 0
  ffprobe -v error -select_streams v:0 -count_frames \
    -show_entries stream=nb_read_frames -of default=nk=1:nw=1 "$1" 2>/dev/null || echo 0
}

s=0
while [ "$s" -lt "$TOTAL" ]; do
  e=$(( s + CHUNK - 1 )); [ "$e" -ge "$TOTAL" ] && e=$(( TOTAL - 1 ))
  want=$(( e - s + 1 ))
  out=$(printf "%s/c_%06d_%06d.mp4" "$DIR" "$s" "$e")
  have=$(frames_of "$out")
  if [ "$have" = "$want" ]; then
    echo "[skip] $out ($have frames) $(date)" | tee -a "$LOG"
    s=$(( e + 1 )); continue
  fi
  echo "[render] frames ${s}-${e} -> $out $(date)" | tee -a "$LOG"
  rm -f "$out"
  render_one "$s" "$e" "$out"
  have=$(frames_of "$out")
  if [ "$have" != "$want" ]; then
    echo "[retry] chunk ${s}-${e} produced $have/$want, retrying once $(date)" | tee -a "$LOG"
    rm -f "$out"
    render_one "$s" "$e" "$out"
    have=$(frames_of "$out")
  fi
  if [ "$have" != "$want" ]; then
    echo "[ABORT] chunk ${s}-${e} failed twice ($have/$want). Fix then re-run to resume. $(date)" | tee -a "$LOG"
    exit 1
  fi
  echo "[ok] $out ($have frames) $(date)" | tee -a "$LOG"
  s=$(( e + 1 ))
done

# --- concat (lossless) ---
echo "=== all chunks done; concat $(date) ===" | tee -a "$LOG"
LIST="$DIR/concat.txt"
: > "$LIST"
for f in $(ls "$DIR"/c_*.mp4 | sort); do echo "file '$(basename "$f")'" >> "$LIST"; done
ffmpeg -y -f concat -safe 0 -i "$LIST" -c copy out/rolin_full.mp4 >>"$LOG" 2>&1
final=$(frames_of out/rolin_full.mp4)
echo "=== concat done: out/rolin_full.mp4 has $final / $TOTAL frames $(date) ===" | tee -a "$LOG"
[ "$final" = "$TOTAL" ] && echo "RENDER_COMPLETE_OK" | tee -a "$LOG" || echo "RENDER_FRAME_COUNT_MISMATCH" | tee -a "$LOG"
