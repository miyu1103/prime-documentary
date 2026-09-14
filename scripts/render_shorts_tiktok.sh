#!/usr/bin/env bash
# Render the TikTok variant of a set of Shorts.
#
# Same pipeline as render_shorts.sh and the same guards - one bundle path deleted before and
# after, preflight before bundling - but it renders Short-short<N>-tt and writes short<N>_tt.mp4.
#
# Two deliberate differences from the YouTube path:
#   * no coverfirst wrapper. That exists because the YouTube Shorts feed ignores the API-set
#     thumbnail and picks a frame, so the cover is burned into the first 0.7 s. TikTok lets the
#     uploader choose the cover, so burning one in would just cost 0.7 s of the hook.
#   * no thumbnail Still. TikTok has no equivalent slot.
#
# Usage: bash scripts/render_shorts_tiktok.sh 104 105 106
#        bash scripts/render_shorts_tiktok.sh $(seq 104 145)
set -uo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
BUNDLE="${TEMP:-/tmp}/pd_tt_bundle"
cd "$REPO" || exit 1
export PYTHONIOENCODING=utf-8

[ $# -gt 0 ] || { echo "usage: $0 <short numbers...>"; exit 2; }
LIST="$*"
CSV="$(echo "$LIST" | tr ' ' ',')"

echo "=== preflight ==="
py -3.11 scripts/preflight_short_render.py "$CSV" --platform tiktok --prune-mirror --fix-mirror || {
  echo "preflight FAILED - not rendering"; exit 1; }

echo "=== free space ==="
df -h /c 2>/dev/null | tail -1

rm -rf "$BUNDLE"
echo "=== bundling once into $BUNDLE ==="
( cd remotion && npx remotion bundle --public-dir=./public_min --out-dir "$BUNDLE" 2>&1 \
    | grep -vE "^ +at |Bundling [0-9]" | tail -2 )
[ -f "$BUNDLE/index.html" ] || { echo "BUNDLE FAILED"; rm -rf "$BUNDLE"; exit 1; }

fail=0
for n in $LIST; do
  data="remotion/src/data/short${n}.ts"
  out="remotion/out/short${n}_tt.mp4"
  ( cd remotion && npx remotion render "$BUNDLE" "Short-short${n}-tt" "out/short${n}_tt.mp4" \
      --codec=h264 --crf=16 --concurrency=4 2>&1 | tail -1 )
  if [ ! -f "$out" ] || [ "$data" -nt "$out" ]; then
    echo "  short${n}: RENDER DID NOT PRODUCE A FRESH FILE"
    fail=$((fail+1))
    continue
  fi
  # Strip the container tags before TikTok ever sees the file. Remotion writes
  # comment="Made with Remotion 4.0.476", and TikTok reads that as a generation marker: every one
  # of the 126 files uploaded with it carries a "creator labelled this AI-generated" badge, while
  # the same footage with the tag removed shows the AI-generated switch OFF in the uploader.
  # This is a re-mux, not a re-encode - the picture is bit-identical.
  # -f mp4 and a real .mp4 temp name. Without them ffmpeg cannot infer a format from
  # "short10_tt.mp4.clean", fails with "Unable to choose an output format", the && short-circuits
  # the mv, and the script still prints failures=0. Measured 2026-08-17: every TikTok file ever
  # produced here still carried comment=Made with Remotion 4.0.476 - the tag this step exists to
  # remove, and the one that put an AI-generated badge on 127 videos of the first account.
  tmp="${out%.mp4}.clean.mp4"
  if ffmpeg -v error -y -i "$out" -map_metadata -1 -map_chapters -1 -c copy \
            -movflags +faststart -f mp4 "$tmp"; then
    mv -f "$tmp" "$out"
    if ffprobe -v error -show_entries format_tags=comment -of default=nw=1:nk=1 "$out" | grep -qi remotion; then
      echo "METADATA STRIP FAILED (tag survived): $out"
      exit 1
    fi
  else
    echo "METADATA STRIP FAILED (ffmpeg): $out"
    exit 1
  fi
done

rm -rf "$BUNDLE"
echo "=== bundle removed; free space now ==="
df -h /c 2>/dev/null | tail -1
echo "TT_RENDER_DONE  failures=$fail"
