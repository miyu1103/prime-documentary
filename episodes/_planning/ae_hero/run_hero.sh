#!/usr/bin/env bash
# Usage: run_hero.sh <name>
set -u
NAME="$1"
SCR="C:/Users/aab15/AppData/Local/Temp/claude/C--Users-aab15/a9b4b9f9-07d0-4491-8600-2bd16f67f924/scratchpad"
AEDIR="C:/Program Files/Adobe/Adobe After Effects 2026/Support Files"
AFX="$AEDIR/AfterFX.com"
AERENDER="$AEDIR/aerender.exe"
OUT="C:/Users/aab15/Documents/prime-documentary/remotion/public/kidsforcash/ae/hero_${NAME}.mp4"
AEP="$SCR/hero_${NAME}.aep"
LOG="$SCR/hero_build_log.txt"
FRAME="$SCR/frame_${NAME}.png"

echo "=== [$NAME] setup ==="
rm -f "$LOG" "$AEP" "$OUT" "$FRAME" 2>/dev/null
cp "$SCR/cfg_${NAME}.jsx" "$SCR/hero_config.jsx"
# kill any stragglers
taskkill //F //IM AfterFX.com >/dev/null 2>&1
taskkill //F //IM AfterFX.exe >/dev/null 2>&1
sleep 1

echo "=== [$NAME] build (AfterFX -r) ==="
"$AFX" -r "$SCR/build_hero.jsx" >/dev/null 2>&1 &
AFXPID=$!
# poll for DONE_BUILD_OK or BUILD_ERROR
for i in $(seq 1 90); do
  sleep 2
  if [ -f "$LOG" ] && grep -q "DONE_BUILD_OK" "$LOG" 2>/dev/null; then echo "build done @ ${i}x2s"; break; fi
  if [ -f "$LOG" ] && grep -q "BUILD_ERROR\|CONFIG_EVAL_ERROR\|NO_CONFIG" "$LOG" 2>/dev/null; then echo "BUILD FAILED"; cat "$LOG"; fi
done
sleep 2
taskkill //F //IM AfterFX.com >/dev/null 2>&1
taskkill //F //IM AfterFX.exe >/dev/null 2>&1
sleep 1

echo "--- build log ---"; cat "$LOG" 2>/dev/null
if [ ! -f "$AEP" ]; then echo "NO AEP -> abort $NAME"; exit 2; fi

echo "=== [$NAME] aerender ==="
"$AERENDER" -project "$AEP" -comp "HeroComp" -output "$OUT" 2>&1 | tail -20
sleep 1

echo "=== [$NAME] probe ==="
if [ -f "$OUT" ]; then
  ffprobe -v error -select_streams v:0 -show_entries stream=codec_name,width,height,duration,nb_frames,avg_frame_rate -of default=noprint_wrappers=1 "$OUT"
  ffmpeg -y -ss 2.5 -i "$OUT" -frames:v 1 "$FRAME" >/dev/null 2>&1
  echo "frame: $FRAME"
else
  echo "NO OUTPUT MP4 for $NAME"
fi
echo "=== [$NAME] END ==="
