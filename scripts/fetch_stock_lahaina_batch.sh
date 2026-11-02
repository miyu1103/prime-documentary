#!/bin/bash
# EP75 lahaina — fetch fresh stock for every register the film needs.
#
# WHY: the factory shelf's media is gone (index survives, files do not), and the only clips still
# reachable are per-episode copies under D:\pd-public that have all been used in earlier films.
# Downloading fresh is the one route that gives this episode unused footage. Pexels and Pixabay
# both grant commercial use, and fetch_stock.py writes source/author/licence/sha256 per file.
#
# Queries are the registers in EP75_lahaina_FOOTAGE_PLAN.v001.md, plus the subject registers that
# no shelf could supply. Anything holiday-shaped is NOT queried; the spec's 65 forbidden_subjects
# still apply at review, and a person still opens a labelled contact sheet before a clip is cut.
set -u
cd /c/Users/aab15/Documents/prime-documentary

PER=${1:-6}

QUERIES=(
  "dry grass wind"           "dry grassland hillside"    "brown grass field"
  "wildfire smoke"           "smoke drifting"            "grey smoke sky"
  "smoke over road"          "burnt ground ash"          "embers glowing"
  "overcast sky clouds"      "cloudy sky timelapse"      "storm clouds moving"
  "dust blowing wind"        "dust road"
  "asphalt road empty"       "road driving pov"          "traffic jam cars"
  "car queue road"
  "chain link fence"         "padlock chain"             "wire fence"
  "utility pole power lines" "electrical wires"          "transformer pole"
  "corridor empty building"  "office desk paper"         "documents folder desk"
  "filing cabinet office"    "empty meeting room"
  "hands typing keyboard"    "hand holding phone"        "person silhouette walking"
  "window looking out"       "curtain window light"
  "fire hydrant street"      "water pipe valve"          "water flowing pipe"
  "night street lights"      "street lamp night"
  "mountain slope dry"       "hillside houses"
  "radio vintage device"     "control room screens"
)

echo "[fetch] ${#QUERIES[@]} queries at --per-source $PER  (up to $(( ${#QUERIES[@]} * PER * 2 )) clips)"
i=0
for q in "${QUERIES[@]}"; do
  i=$((i+1))
  printf '[fetch] %2d/%d  %s\n' "$i" "${#QUERIES[@]}" "$q"
  py -3.11 scripts/fetch_stock.py lahaina --query "$q" --per-source "$PER" --write 2>&1 \
    | grep -E "kept|skip|FAIL|error" | head -4
done
echo "[fetch] done"
