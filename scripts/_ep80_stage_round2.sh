#!/usr/bin/env bash
# EP80 concordia -- second footage round. Object nouns only, two words.
#
# Round 1 got 16 clips out of 80 candidates because every cruise ship on the shelf carries a
# legible company name (Star Cruises, VIKING, SILJA, P&O, Holland America Line) and this film
# is about a real ship. episode_spec also forbids the wreck itself -- capsized, listing, on its
# side, collision, salvage -- and a long list of countries including Venice, France, the UK and
# Spain, which removes most European stock as well.
#
# So this round does not ask for ships at all. It asks for the things around the story that
# carry no company and no country: water, rock, harbour ironmongery, instruments, the coast.
# Trap 7 from the design handover: ask for the NAME OF A THING. Concept words ("wind", "cliff")
# returned the Grand Canyon, a wind farm, a subway and a goat.
set -euo pipefail
Q=(); add() { Q+=(--query "$1"); }

# the sea itself -- no horizon furniture, no vessel
for q in "sea water" "dark water" "night sea" "calm sea" "open sea" "sea surface" \
         "water surface" "wave crest" "sea foam" "deep water" "black water" "water ripple" \
         "underwater light" "water reflection" "moon water"; do add "$q"; done

# rock and coast: Giglio is granite
for q in "coastal rocks" "rocky shore" "cliff sea" "granite rock" "limestone cliff" \
         "shore rocks" "coast line" "sea cliff" "rock face" "stone shore"; do add "$q"; done

# the harbour, as ironmongery rather than as a place
for q in "mooring rope" "anchor chain" "bollard rope" "harbour wall" "stone pier" \
         "quay wall" "dock ladder" "rusty chain" "steel cable" "rope coil" \
         "metal railing" "steel bollard"; do add "$q"; done

# a deck, close enough that no name is in frame
for q in "ship railing" "steel deck" "porthole window" "deck lights" "navigation light" \
         "life buoy" "life ring" "boat davit" "steel stairs" "watertight door" \
         "engine room" "pipe valve" "metal door"; do add "$q"; done

# the instruments the story turns on
for q in "radar screen" "compass needle" "nautical chart" "chart table" "ship wheel" \
         "bridge console" "instrument panel" "gauge dial" "depth sounder" "control panel" \
         "switch panel" "warning lamp"; do add "$q"; done

# lights on the water
for q in "lighthouse light" "beacon light" "harbour light" "sea buoy" "night harbour" \
         "harbour night" "pier light"; do add "$q"; done

# Italy, without Venice
for q in "italian coast" "tuscan coast" "mediterranean sea" "island coast" "coastal village" \
         "hillside village" "stone village" "olive tree" "italian harbour" "fishing boat" \
         "small harbour" "stone steps"; do add "$q"; done

# the paper and the court that followed
for q in "document stack" "filing cabinet" "paper file" "office corridor" "empty office" \
         "court building" "empty courtroom" "law book" "legal file" "binder shelf"; do add "$q"; done

echo "queries: $(( ${#Q[@]} / 2 ))"
py -3.11 -X utf8 scripts/stage_footage_by_title.py --slug concordia "${Q[@]}" \
  --per-query 40 --emit-candidates runs/qc/concordia_candidates_r2.json
