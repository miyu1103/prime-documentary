#!/usr/bin/env bash
# EP76 morandi -- footage staging, TWO-WORD queries.
#
# Why this exists. The pool was staged, reviewed at round 4, and then 134 clips were
# REMOVED by that review and nothing was staged back. It sat at 41 factory clips
# against episode_spec.v001.json's own declared distinct_video_assets=265, and the
# pre-flight forecast said ~156 of ~266 footage cuts would have to repeat.
#
# Query band: two words. Measured on EP74 itaewon -- five-word queries returned 0 rows,
# one-word queries returned plenty and meant nothing, two words was the only band that hit.
#
# The subject is the Polcevera viaduct in Genoa. episode_spec forbids, among others:
# falling/crashing vehicles, victims, rescue, funerals, ambulances, mugshots, watermarks,
# readable documents, US route shields, American highway signs, US number plates and
# right-hand-drive traffic. Nothing below asks for any of them. The place has to read as
# Italy, so the geography queries carry their own weight.
set -euo pipefail
Q=()
add() { Q+=(--query "$1"); }

# the structure itself -- a concrete cable-stayed viaduct
for q in "concrete bridge" "bridge pier" "bridge column" "bridge deck" "highway bridge" \
         "motorway bridge" "road bridge" "viaduct bridge" "arch bridge" "railway bridge" \
         "elevated highway" "overpass road" "bridge cable" "cable stay" "suspension bridge" \
         "bridge tower" "concrete pillar" "concrete column" "bridge span" "bridge underside"; do add "$q"; done

# what the trial was about: concrete, steel and what time does to them
for q in "cracked concrete" "concrete crack" "crumbling concrete" "weathered concrete" \
         "rusty steel" "rusted metal" "corroded metal" "rusty cable" "steel cable" \
         "reinforcement bar" "rebar concrete" "peeling paint" "damp wall" "water damage" \
         "concrete surface" "steel beam" "metal structure" "old concrete" "stained concrete" \
         "rust stain"; do add "$q"; done

# Italy, Liguria, the port and the valley -- the film fails if this reads as anywhere else
for q in "italian city" "italy street" "italian town" "italian architecture" "italian coast" \
         "european city" "european street" "mediterranean coast" "mediterranean port" \
         "coastal town" "hillside town" "mountain valley" "valley town" "old town" \
         "cobbled street" "narrow alley" "apartment block" "housing block" "terraced houses" \
         "church tower"; do add "$q"; done

# the port that the road served
for q in "port crane" "harbour crane" "container port" "shipping port" "cargo ship" \
         "container yard" "dock crane" "harbour water" "port terminal" "freight truck"; do add "$q"; done

# the road, in a country that drives on the right
for q in "motorway traffic" "highway traffic" "traffic jam" "road tunnel" "tunnel road" \
         "toll booth" "road marking" "lane marking" "truck motorway" "traffic flow" \
         "night motorway" "road barrier" "guard rail" "crash barrier" "road sign"; do add "$q"; done

# the weather on 14 August 2018
for q in "heavy rain" "rain storm" "storm cloud" "thunder storm" "rain window" \
         "wet road" "rain city" "grey sky" "dark cloud" "rain windshield" \
         "lightning storm" "wind tree"; do add "$q"; done

# inspection, maintenance, engineering -- the work that was or was not done
for q in "construction site" "construction worker" "hard hat" "safety helmet" "scaffolding building" \
         "crane construction" "concrete pour" "cement mixer" "site survey" "survey tripod" \
         "measuring tape" "technical drawing" "engineering drawing" "blueprint plan" "site inspection" \
         "worker climbing" "maintenance work" "welding metal" "drill concrete" "work platform"; do add "$q"; done

# the paper: ministry, archive, expert report
for q in "filing cabinet" "document stack" "paper file" "archive shelf" "office corridor" \
         "empty office" "meeting room" "government building" "office desk" "typing keyboard" \
         "signing paper" "stamp paper" "folder shelf" "binder stack" "office window"; do add "$q"; done

# the Tribunale di Genova, 2022-2026
for q in "courthouse exterior" "court building" "empty courtroom" "court corridor" "law book" \
         "legal file" "law library" "judge bench"; do add "$q"; done

# neutral connective tissue and transitions
for q in "concrete wall" "shadow wall" "dust particle" "smoke slow" "water drop" \
         "aerial city" "drone city" "city aerial" "wall clock" "clock time" \
         "empty street" "quiet street" "street lamp" "power line" "pylon sky"; do add "$q"; done

echo "queries: $(( ${#Q[@]} / 2 ))"
py -3.11 -X utf8 scripts/stage_footage_by_title.py --slug morandi "${Q[@]}" \
  --per-query 40 --emit-candidates runs/qc/morandi_candidates_r1.json
