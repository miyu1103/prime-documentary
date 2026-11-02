#!/bin/bash
# EP75 lahaina — SECOND fetch, written after reading all 413 clips of the first one.
#
# WHAT THE FIRST PASS TAUGHT, measured by eye on 21 contact sheets:
#   WORKED  : dry grass, wildfire smoke aerials, burnt ground, storm clouds, road surfaces,
#             chain-link and barbed wire, pylons and utility poles, embers, water pipes, corridors.
#   FAILED  : every query with a person or an office in it. "office desk paper", "hands typing
#             keyboard", "documents folder desk", "control room screens", "hand holding phone",
#             "person silhouette walking", "radio vintage device", "empty meeting room" returned
#             corporate lifestyle stock -- resolved faces, readable screens, green-screen phone
#             props, brand marks. None of it is usable and none of it should be re-queried.
#             Those registers are carried by the 129 commissioned plates, which is what they exist
#             for. Pixabay in particular skews to CGI, flags, cartoon graphics and snow.
#
# So this pass goes DEEPER on the registers that worked rather than wider across ones that did not.
set -u
cd /c/Users/aab15/Documents/prime-documentary
PER=${1:-8}

QUERIES=(
  "brush fire smoke"        "grass fire"              "smoke plume aerial"
  "wildfire aerial"         "smoke hillside"          "smoke drifting field"
  "burned house ruins"      "burnt forest ground"     "scorched earth"
  "ash falling"             "smoke black background"  "ember sparks"
  "dry grass close up"      "grass blowing wind"      "dead grass field"
  "dry hillside"            "arid hillside scrub"
  "overcast sky"            "grey clouds moving"      "cloud timelapse dark"
  "dust storm road"         "dust cloud"
  "empty road aerial"       "rural road overcast"     "road surface close"
  "barbed wire fence"       "chain link fence close"  "wire mesh"
  "electricity pylon"       "power line silhouette"   "utility pole road"
  "water pipe outflow"      "water valve industrial"  "hydrant water"
  "corridor institutional"  "empty hallway"
)

echo "[fetch2] ${#QUERIES[@]} queries at --per-source $PER"
i=0
for q in "${QUERIES[@]}"; do
  i=$((i+1))
  printf '[fetch2] %2d/%d  %s\n' "$i" "${#QUERIES[@]}" "$q"
  py -3.11 scripts/fetch_stock.py lahaina --query "$q" --per-source "$PER" --write 2>&1 \
    | grep -E "Added|skip|FAIL|error" | head -3
done
echo "[fetch2] done"
