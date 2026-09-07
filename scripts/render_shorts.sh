#!/usr/bin/env bash
# Render a set of Shorts, safely. Use this instead of calling remotion by hand.
#
# Every failure this wraps actually happened, in one session:
#
#   * 12 leftover bundles filled the disk (149 GB) because each render used a fresh --out-dir and
#     nothing deleted the last one. The 13th render then died with ENOSPC mid-copy.
#   * coverfirst.sh happily ran on the PREVIOUS render when the new one had failed, producing a
#     freshly-dated file with stale content. Nothing downstream could tell.
#   * renders were started against a stale public_min mirror three times (missing depth maps,
#     missing fx clips, missing ctathumb).
#   * renders were started against audio older than the design, producing 35 s videos under a 57 s
#     script, twice.
#
# So: one bundle path, deleted first and deleted after; preflight before bundling; and coverfirst
# only runs if the mp4 it is about to wrap is newer than the data file that describes it.
#
# Usage:  bash scripts/render_shorts.sh 143 144 145
#         bash scripts/render_shorts.sh $(seq 150 162)
set -uo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
BUNDLE="${TEMP:-/tmp}/pd_shorts_bundle"       # ONE path, always
cd "$REPO" || exit 1
export PYTHONIOENCODING=utf-8

[ $# -gt 0 ] || { echo "usage: $0 <short numbers...>"; exit 2; }
LIST="$*"
CSV="$(echo "$LIST" | tr ' ' ',')"

echo "=== preflight ==="
py -3.11 scripts/preflight_short_render.py "$CSV" --prune-mirror --fix-mirror || {
  echo "preflight FAILED - not rendering"; exit 1; }

echo "=== free space before bundling ==="
df -h /c 2>/dev/null | tail -1

rm -rf "$BUNDLE"
echo "=== bundling once into $BUNDLE ==="
( cd remotion && npx remotion bundle --public-dir=./public_min --out-dir "$BUNDLE" 2>&1 \
    | grep -vE "^ +at |Bundling [0-9]" | tail -2 )
[ -f "$BUNDLE/index.html" ] || { echo "BUNDLE FAILED"; rm -rf "$BUNDLE"; exit 1; }

fail=0
for n in $LIST; do
  data="remotion/src/data/short${n}.ts"
  out="remotion/out/short${n}_yt.mp4"
  ( cd remotion && npx remotion still "$BUNDLE" "ShortThumb-short${n}" "out/short${n}_thumb.png" 2>&1 | tail -1 )
  ( cd remotion && npx remotion render "$BUNDLE" "Short-short${n}-yt" "out/short${n}_yt.mp4" \
      --codec=h264 --crf=16 --concurrency=4 2>&1 | tail -1 )
  # the guard: never wrap a video that is older than the description it should have been built from
  if [ ! -f "$out" ] || [ "$data" -nt "$out" ]; then
    echo "  short${n}: RENDER DID NOT PRODUCE A FRESH FILE - skipping coverfirst"
    fail=$((fail+1))
    continue
  fi
  bash scripts/coverfirst.sh "$n" 2>&1 | tail -1
done

rm -rf "$BUNDLE"
echo "=== bundle removed; free space now ==="
df -h /c 2>/dev/null | tail -1
echo "RENDER_DONE  failures=$fail"
exit $([ "$fail" -eq 0 ] && echo 0 || echo 1)
