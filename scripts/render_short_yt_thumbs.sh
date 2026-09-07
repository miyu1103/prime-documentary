#!/usr/bin/env bash
# Render the 16:9 thumbnail for every Short that has props but no rendered image.
#
# This is what the channel page, search results and suggested rails show. 40 uploaded Shorts had
# the vertical 1080x1920 cover set instead - YouTube letterboxes it into black bars and crops the
# headline away, leaving only the small centre line readable.
set -uo pipefail
cd "$(dirname "$0")/.." || exit 1
BUNDLE="${TEMP:-/tmp}/pd_cov"
[ -f "$BUNDLE/index.html" ] || ( cd remotion && npx remotion bundle --public-dir=./public_min --out-dir "$BUNDLE" 2>&1 | tail -1 )
[ -f "$BUNDLE/index.html" ] || { echo "BUNDLE FAILED"; exit 1; }

ok=0; fail=0
for p in runs/shorts_thumbs/props/short*.json; do
  sid=$(basename "$p" .json)
  out="runs/shorts_thumbs/samples/${sid}.png"
  [ -f "$out" ] && [ "$out" -nt "$p" ] && { ok=$((ok+1)); continue; }
  if ( cd remotion && npx remotion still "$BUNDLE" ShortThumbYT "../$out" --props="../$p" >/dev/null 2>&1 ) \
     && [ -f "$out" ]; then ok=$((ok+1)); else echo "  FAIL $sid"; fail=$((fail+1)); fi
done
echo "YT_THUMBS_DONE ok=$ok fail=$fail  total=$(ls runs/shorts_thumbs/samples/short*.png | wc -l)"
