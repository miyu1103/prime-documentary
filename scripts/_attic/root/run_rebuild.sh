#!/bin/bash
cd /c/Users/aab15/Documents/prime-documentary
for e in 062-greene 063-correa 064-memphis 065-marmet; do
  s=${e#*-}
  echo "===== $s"
  .venv/Scripts/python.exe scripts/build_case_film_audio.py --ep "PD-2026-$e" \
      --film-data "remotion/src/data/${s}_film.json" --render 2>&1 | grep -E "density|rendered mix"
  .venv/Scripts/python.exe scripts/build_case_film_mux.py --ep "PD-2026-$e" \
      --video "out/${s}.mp4" 2>&1 | grep -E "WROTE|receipt ->"
  .venv/Scripts/python.exe scripts/preflight_render_gate.py --ep "PD-2026-$e" 2>&1 | tail -2
done
echo "===== REBUILD DONE"
