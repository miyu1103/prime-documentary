#!/bin/bash
cd /c/Users/aab15/Documents/prime-documentary
for e in 062-greene 063-correa 064-memphis 065-marmet; do
  echo "===== $e"
  .venv/Scripts/python.exe scripts/check_final_acceptance.py "PD-2026-$e" \
    --render "out/PD-2026-${e}_film.muxed.v001.mp4" 2>&1 | grep -E "FAIL|RESULT"
done
echo "===== ACCEPT DONE"
