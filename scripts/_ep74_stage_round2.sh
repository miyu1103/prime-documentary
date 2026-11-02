#!/usr/bin/env bash
# EP74 itaewon -- second footage round, TWO-WORD queries.
#
# Measured on round 1: five-word queries returned 0 rows, one-word queries returned
# plenty and meant nothing ("alley" -> a tree avenue, a bowling alley; "light" ->
# a sparkler; "camera" -> a man's face, from "towards the camera"), and two-word
# queries were the only band that hit -- "seoul night", "night alley" and
# "subway seoul" were almost all usable. Visual QC of round 1 kept 22%.
set -euo pipefail
Q=()
add() { Q+=(--query "$1"); }
# the alley itself, and the register of the hook
for q in "night alley" "narrow alley" "back street" "side street" "wet street" \
         "rain street" "night street" "empty alley" "alley night" "street lamp" \
         "steep street" "cobbled street" "neon sign" "neon street" "street sign"; do add "$q"; done
# Seoul and Korea -- the place has to read as itself
for q in "seoul night" "seoul street" "seoul city" "seoul subway" "seoul skyline" \
         "korea street" "korean street" "korea city" "korean sign" "seoul crowd" \
         "subway seoul" "korea night" "asian street" "asian alley" "asian city"; do add "$q"; done
# an ordinary crowd. NEVER a crush: the design forbids depicting it.
for q in "busy street" "crowded street" "pedestrian crossing" "street crowd" "walking crowd" \
         "city crowd" "night market" "street market" "crowded market" "shopping street" \
         "people walking" "crowd walking" "street party" "halloween costume" "bar street"; do add "$q"; done
# the response: 11 calls, and the organisation that took them
for q in "police car" "police officer" "police station" "emergency light" "ambulance night" \
         "emergency vehicle" "control room" "dispatch centre" "radio dispatch" "call centre" \
         "emergency call" "siren light" "police line" "police tape" "first responder"; do add "$q"; done
# the state: maps, audits, offices, the paper
for q in "government building" "office corridor" "empty office" "meeting room" "office desk" \
         "press conference" "official document" "filing cabinet" "city hall" "municipal building" \
         "office hallway" "document stack" "paper file" "report document" "empty corridor"; do add "$q"; done
# court and law -- Korean courts use no gavel
for q in "courthouse exterior" "court building" "law book" "legal document" "empty courtroom" \
         "judge bench" "law library" "legal file"; do add "$q"; done
# cameras: the case turns on what was recorded
for q in "security camera" "cctv camera" "surveillance monitor" "camera pole" "monitor wall" \
         "cctv footage" "street camera"; do add "$q"; done
# after: barriers, flowers, an empty place
for q in "memorial flowers" "flower memorial" "candle memorial" "metal barrier" "barrier fence" \
         "closed shop" "empty street" "quiet street" "street barrier"; do add "$q"; done
# WAVE 2. Sixteen wave-1 queries hit the per-query cap, so the shelf is deeper than
# the first pass read. Cap raised, and these widen the net along the same two-word band.
for q in "city night" "night city" "urban night" "downtown night" "street night"          "night traffic" "taxi night" "night rain" "rain umbrella" "wet pavement"          "puddle reflection" "narrow street" "stone street" "brick wall" "concrete wall"; do add "$q"; done
for q in "subway station" "metro station" "subway escalator" "station platform" "underground station"          "crowd barrier" "fence barrier" "steel fence" "railing street" "guard rail"; do add "$q"; done
for q in "nightlife street" "bar night" "restaurant street" "street food" "food stall"          "lantern street" "festival night" "crowd festival" "public square" "town square"; do add "$q"; done
for q in "hospital corridor" "hospital exterior" "emergency room" "ambulance street" "medical team"          "news broadcast" "tv news" "newspaper print" "news studio" "camera crew"; do add "$q"; done
for q in "city map" "map table" "aerial city" "drone city" "city aerial"          "wall clock" "clock time" "stamp document" "signature document" "official seal"; do add "$q"; done
echo "queries: $(( ${#Q[@]} / 2 ))"
py -3.11 -X utf8 scripts/stage_footage_by_title.py --slug itaewon "${Q[@]}" \
  --per-query 40 --emit-candidates runs/qc/itaewon_candidates_r2.json
