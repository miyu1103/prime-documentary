#!/bin/bash
cd /c/Users/aab15/Documents/prime-documentary
# one at a time, no overlap: the last run had two builders on one ComfyUI
.venv/Scripts/python.exe scripts/build_motion_from_plates.py --slug memphis --limit 45
.venv/Scripts/python.exe scripts/build_motion_from_plates.py --slug marmet  --limit 20
.venv/Scripts/python.exe scripts/build_motion_from_plates.py --slug correa  --limit 5
echo "===== TOPUP DONE $(date +%H:%M) ====="
