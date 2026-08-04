#!/usr/bin/env bash
# Build and render kinetic-typography beat overlays through After Effects, end to end.
#
# Never call AfterFX/aerender by hand. The build step reports a script failure only as text in its
# own log - the process still exits 0 - and aerender will then happily re-render whatever the LAST
# successful build left in kinetic.aep. That happened: a build died on job 1, and two overlays came
# out at the previous run's durations with byte sizes identical to the earlier render. Nothing in
# any exit code said so. This script refuses to render unless the build log is clean and the .aep
# was written by THIS run.
#
# Usage: scripts/ae/render_beats.sh <jobs.json>
set -euo pipefail

JOBS_SRC="${1:?usage: render_beats.sh <jobs.json>}"
AE_DIR="C:/temp/ae"
AE="/c/Program Files/Adobe/Adobe After Effects 2026/Support Files/AfterFX.exe"
AR="/c/Program Files/Adobe/Adobe After Effects 2026/Support Files/aerender.exe"
JSX="$(cd "$(dirname "$0")" && pwd)/kinetic_beat.jsx"

mkdir -p "$AE_DIR/out"
cp "$JOBS_SRC" "$AE_DIR/jobs.json"

ids=$(python -c "import json,sys;print(' '.join(j['id'] for j in json.load(open(sys.argv[1],encoding='utf-8'))))" "$JOBS_SRC")
for id in $ids; do rm -f "$AE_DIR/out/$id.avi" "$AE_DIR/out/$id.webm"; done
rm -f "$AE_DIR/kinetic.log" "$AE_DIR/kinetic.aep"

echo "== build =="
"$AE" -noui -r "$JSX" || true
cat "$AE_DIR/kinetic.log"
grep -q "FAILED" "$AE_DIR/kinetic.log" && { echo "BUILD FAILED - not rendering"; exit 1; }
[ -f "$AE_DIR/kinetic.aep" ] || { echo "no kinetic.aep from this run - not rendering"; exit 1; }

echo "== render =="
"$AR" -project "$AE_DIR/kinetic.aep" 2>&1 | grep -viE "^PROGRESS:  0:00" | tail -4

echo "== webm (VP9 + alpha) =="
for id in $ids; do
  [ -f "$AE_DIR/out/$id.avi" ] || { echo "MISSING $id.avi"; exit 1; }
  ffmpeg -v error -y -i "$AE_DIR/out/$id.avi" \
     -c:v libvpx-vp9 -pix_fmt yuva420p -b:v 0 -crf 26 -auto-alt-ref 0 -row-mt 1 \
     "$AE_DIR/out/$id.webm"
  # alpha_mode=1 is the WebM flag Chrome reads to composite the alpha plane; ffmpeg's own decoder
  # ignores it and will report yuv420p, so this tag is the only check that means anything here.
  am=$(ffprobe -v error -show_entries stream_tags=alpha_mode -of default=nw=1:nk=1 "$AE_DIR/out/$id.webm")
  [ "$am" = "1" ] || { echo "$id.webm HAS NO ALPHA"; exit 1; }
  echo "  $id.webm  $(stat -c%s "$AE_DIR/out/$id.webm") bytes  alpha_mode=$am"

  # Install into the Short's own public directory. Anywhere else is a guaranteed 404 at render
  # time: public_min mirrors remotion/public/shorts and nothing else, and the bundle is built from
  # the mirror. Job id short<NN>_<suffix> -> shorts/short<NN>/short<NN>_kin_<suffix>.webm
  case "$id" in
    short*_*)
      sid="${id%%_*}"; sfx="${id#*_}"
      dst="$(cd "$(dirname "$0")/../.." && pwd)/remotion/public/shorts/$sid"
      if [ -d "$dst" ]; then
        cp "$AE_DIR/out/$id.webm" "$dst/${sid}_kin_${sfx}.webm"
        echo "    -> shorts/$sid/${sid}_kin_${sfx}.webm"
      else
        echo "    !! no such Short directory: $dst"; exit 1
      fi
      ;;
  esac

  # The AVI is an uncompressed intermediate - about 900 MB for two seconds. 89 of them had
  # quietly reached 47 GB and taken the system drive to 98% full, which is how a render dies
  # mid-copy with ENOSPC. The webm is the deliverable and it is already installed and verified
  # above, so the intermediate goes now rather than "later".
  rm -f "$AE_DIR/out/$id.avi"
done
echo "OK"
