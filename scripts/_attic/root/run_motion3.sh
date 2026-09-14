#!/bin/bash
cd /c/Users/aab15/Documents/prime-documentary
.venv/Scripts/python.exe scripts/build_motion_from_plates.py --slug memphis --limit 40
.venv/Scripts/python.exe scripts/build_motion_from_plates.py --slug marmet  --limit 30
.venv/Scripts/python.exe scripts/build_motion_from_plates.py --slug correa  --limit 12
echo "===== DONE $(date +%H:%M) ====="
