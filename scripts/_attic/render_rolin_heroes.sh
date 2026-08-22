#!/usr/bin/env bash
# EP34 rolin — super-heavy hero render driver (RESUME + RETRY).
# The Blender hero scripts now render frame-by-frame and SKIP frames already on disk (crash-tolerant),
# while animation stays keyed on the full 1..FE span (correct). So each hero is rendered as ONE whole
# call (FS=1, FE=total => correct camera/physics), and if Blender is killed mid-render (intermittent
# 4K/OptiX kill), simply re-invoking the SAME command resumes from the last frame on disk. This driver
# retries each hero until all its frames exist, then row-6 encodes to remotion/public/rolin/hero_*.mp4.
# Re-launching this whole driver after a kill also resumes (encoded heroes skip, partials continue).
set -u
ROOT="/c/Users/aab15/Documents/prime-documentary"
cd "$ROOT" || exit 1
BL="/c/Program Files/Blender Foundation/Blender 5.1/blender.exe"
OUTV="$ROOT/remotion/public/rolin"
SEQ="$ROOT/out/rolin_hero_seq"
MAX_ATTEMPTS=12
mkdir -p "$OUTV" "$SEQ"

render_hero () {
  local name="$1" script="$2" fe="$3" samples="$4" extra="${5:-}"
  local seqdir="$SEQ/$name" mp4="$OUTV/hero_${name}.mp4"
  if [ -f "$mp4" ]; then echo "[$name] already encoded — skip"; return 0; fi
  mkdir -p "$seqdir"
  echo "=== [$name] target $fe frames @4K/$samples $(date) ==="
  local att total
  for ((att=1; att<=MAX_ATTEMPTS; att++)); do
    total=$(ls "$seqdir"/f_*.png 2>/dev/null | wc -l)
    [ "$total" -ge "$fe" ] && break
    echo "[$name] attempt $att: have $total/$fe, rendering (resume) $(date +%H:%M:%S)"
    "$BL" -b -P "remotion/src/blender/aircash_${script}.py" -- "$seqdir" 3840 2160 1 "$fe" "$samples" $extra \
      >/dev/null 2>&1
  done
  total=$(ls "$seqdir"/f_*.png 2>/dev/null | wc -l)
  if [ "$total" -lt "$fe" ]; then echo "[$name] !! only $total/$fe after $MAX_ATTEMPTS attempts — not encoding"; return 1; fi
  echo "=== [$name] encoding (row-6) $(date) ==="
  ffmpeg -y -hide_banner -loglevel error -framerate 60 -i "$seqdir/f_%04d.png" \
    -c:v libx264 -crf 16 -pix_fmt yuv420p -colorspace bt709 "$mp4" \
    && { echo "[$name] WROTE $mp4 ($(du -m "$mp4"|cut -f1)MB) $(date)"; rm -rf "$seqdir"; } \
    || echo "[$name] !! encode failed"
}

# name                script            FE   samples  extra   (resume partials first, then the rest)
render_hero checkpointconverge checkpointconverge 720 128
render_hero usforfeiture_688b  usforfeiture       360 200 68.8B
render_hero cashstack          cashstack          720 200
render_hero burdenflipscale    burdenflipscale    720 200
render_hero airportcheckpoint  airportcheckpoint  960 200
echo "=== ALL ROLIN HEROES PASS COMPLETE $(date) ==="
ls -la "$OUTV"/hero_*.mp4
