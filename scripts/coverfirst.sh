#!/usr/bin/env bash
# coverfirst.sh <shortNN> — bake the thumbnail (cover) onto the first ~1.5s of the rendered
# Short so the Shorts feed's first frame reads as the bold cover. libx264 crf18, audio copied.
# Reads  remotion/out/short<NN>_yt.mp4  +  remotion/out/short<NN>_thumb.png
# Writes remotion/out/short<NN>_yt_coverfirst.mp4
set -euo pipefail
N="$1"
OUT="$(cd "$(dirname "$0")/.." && pwd)/remotion/out"
SRC="$OUT/short${N}_yt.mp4"
THUMB="$OUT/short${N}_thumb.png"
DST="$OUT/short${N}_yt_coverfirst.mp4"
[ -f "$SRC" ] || { echo "missing $SRC"; exit 1; }
[ -f "$THUMB" ] || { echo "missing $THUMB"; exit 1; }
ffmpeg -y -i "$SRC" -i "$THUMB" \
  -filter_complex "[1:v]scale=1080:1920,setsar=1[cov];[0:v][cov]overlay=0:0:enable='lte(t,1.5)',format=yuv420p[v]" \
  -map "[v]" -map 0:a -c:v libx264 -crf 18 -preset medium -c:a copy -movflags +faststart "$DST"
echo "coverfirst -> $DST"
