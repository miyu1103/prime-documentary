#!/bin/bash
# One unattended chain: wait for narration, rebuild every downstream artefact, render, mux, accept.
cd /c/Users/aab15/Documents/prime-documentary
for i in $(seq 1 240); do grep -q "NARRATION DONE" out_regen.log 2>/dev/null && break; sleep 15; done
echo "== narration done $(date +%H:%M)"

for e in 062-greene 063-correa 064-memphis 065-marmet; do
  s=${e#*-}; n=${e%%-*}; n=${n#0}
  echo "===== $s $(date +%H:%M)"
  .venv/Scripts/python.exe scripts/build_case_film_generic.py \
      --config "episodes/_planning/EP${n}_${s}_filmconfig.v001.json" 2>&1 \
      | grep -E "distinct_assets|duration_sec_with_bookends|captions"
done
echo "== film json rebuilt $(date +%H:%M)"

bash scripts/_finish_ep62_65.sh
echo "== FINISH CHAIN DONE $(date +%H:%M)"
