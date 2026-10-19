#!/usr/bin/env bash
# Fetch subject footage for EP84 threemile and EP85 katrina while EP83 renders.
#
# WHY. The EP83 sweep found that episode's stock pool contained no aircraft at all, in a film
# about two aircraft crashes. The same audit on the other two found the same shape: threemile's
# pool is wheat fields, water birds and vinyl records for a story about a reactor; katrina's is
# mountain dams and European canals for a story about earthen levees at sea level. That is why
# the cadence kept putting ducklings under a criminal conviction -- there was nothing better to
# put there.
#
# Nothing here is staged. It downloads candidates only; every clip is opened and judged before
# anything reaches a pool, which is how EP83's twenty-five became eleven.
set -u
cd "$(dirname "$0")/../.." || exit 1
log() { printf '%s  %s\n' "$(date '+%m-%d %H:%M')" "$*"; }

log "=== EP84 threemile (nuclear / Susquehanna / 1979) ==="
for q in "nuclear power plant cooling tower" "power plant control room" \
         "steam rising industrial" "wide river valley aerial" \
         "vintage analog control panel" "1970s television broadcast"; do
  py -3.11 scripts/fetch_stock.py PD-2026-084-threemile --query "$q" --per-source 3 --write 2>&1 \
    | grep -E "^  \+|^Added"
done

log "=== EP85 katrina (levee / flood / New Orleans) ==="
for q in "levee earthen embankment" "flood water in a street" \
         "hurricane storm surge coast" "drainage canal concrete wall" \
         "new orleans neighbourhood aerial" "sheet pile construction"; do
  py -3.11 scripts/fetch_stock.py PD-2026-085-katrina --query "$q" --per-source 3 --write 2>&1 \
    | grep -E "^  \+|^Added"
done
log "=== fetch finished ==="
