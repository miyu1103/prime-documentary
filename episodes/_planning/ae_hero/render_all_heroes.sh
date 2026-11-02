#!/usr/bin/env bash
# EP38 "Kids for Cash" AE HERO batch runner.
# Renders all 7 hero composites SERIALLY (one AfterFX/aerender at a time).
# Prereq: After Effects 2026 must launch normally (if AE hangs at ~185MB with no
#         window, RESTART WINDOWS first — this env had an AE early-init deadlock 2026-07-18).
# Each clip: cfg_<name>.jsx -> build_hero.jsx (AfterFX -r) -> aerender -> ffprobe + frame grab.
SCR="C:/Users/aab15/AppData/Local/Temp/claude/C--Users-aab15/a9b4b9f9-07d0-4491-8600-2bd16f67f924/scratchpad"
for NAME in money waiver verdict title ninety inventory families; do
  echo "############################ $NAME ############################"
  bash "$SCR/run_hero.sh" "$NAME"
done
echo "############################ SUMMARY ############################"
ls -la "C:/Users/aab15/Documents/prime-documentary/remotion/public/kidsforcash/ae/"
for NAME in money waiver verdict title ninety inventory families; do
  OUT="C:/Users/aab15/Documents/prime-documentary/remotion/public/kidsforcash/ae/hero_${NAME}.mp4"
  if [ -f "$OUT" ]; then
    printf "%-10s " "$NAME"
    ffprobe -v error -select_streams v:0 -show_entries stream=codec_name,width,height,duration -of csv=p=0 "$OUT"
  else
    echo "$NAME MISSING"
  fi
done
