#!/bin/bash
cd /c/Users/aab15/Documents/prime-documentary
for e in 062-greene 063-correa 064-memphis 065-marmet; do
  s=${e#*-}
  echo "===== $s narration"
  .venv/Scripts/python.exe scripts/gen_narration_case.py --ep "PD-2026-$e" 2>&1 | tail -4
done
echo "===== NARRATION DONE"
