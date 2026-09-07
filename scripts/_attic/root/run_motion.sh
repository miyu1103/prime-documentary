#!/bin/bash
cd /c/Users/aab15/Documents/prime-documentary
for s in correa memphis marmet; do
  echo "===== $s $(date +%H:%M) ====="
  .venv/Scripts/python.exe scripts/build_motion_from_plates.py --slug "$s" --limit 130
done
echo "===== ALL DONE $(date +%H:%M) ====="
