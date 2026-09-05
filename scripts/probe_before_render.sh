#!/bin/bash
# Render 60 seconds BEFORE committing to the full film, and refuse the full render if those
# 60 seconds contain black or frozen frames.
#
# EP55 burge rendered three times -- about five hours -- and failed the same gate three times on
# the same 1.43s of black at 911s. The defect was visible in any 60-second slice that crossed a
# cut boundary. Nothing about that needed a two-hour render to discover.
#
#   scripts/probe_before_render.sh <CompId> <film.json> <public_dir> <slug>
#
# Exit 0 = the slice is clean, go ahead. Exit 1 = do not spend the render.
set -u
cd /c/Users/aab15/Documents/prime-documentary
COMP="${1:?compId}"; FILM="${2:?film.json}"; PUB="${3:?public dir}"; SLUG="${4:?slug}"

FPS=30
# Sample from the middle of the body, where the cut rhythm is densest: 60s = 1800 frames.
TOTAL=$(py -3.11 -c "import json;d=json.load(open(r'$FILM',encoding='utf-8'));lead=d['leadSeconds'] if d.get('leadSeconds') is not None else d['hookSeconds']+3.5;print(int((d['narrationSeconds']+lead+9)*$FPS))")
START=$(( TOTAL / 2 ))
END=$(( START + 60 * FPS - 1 ))
OUT="out/${SLUG}_preprobe.mp4"
LOG="out_preprobe_${SLUG}.log"
rm -f "$OUT"

# CONCURRENCY. MEASURED 2026-08-31: this probe killed EP77 keybridge six minutes into its
# render with "Failed to fetch .../motion/H123.mp4". H123 was present and intact in the pool, in
# public_ep77 AND in the E: archive, all 128 clips were there, none was zero-byte, and the disk
# had 288 GB free -- Remotion just guesses "disk space is low" for any failed fetch. It was
# contention, the same class that had cost EP73 uri fifty minutes an hour earlier.
#
# pd_render_guarded.sh already knows how to survive this: it honours PD_RENDER_CONCURRENCY and
# retries once at 4, with a comment calling 4 "the setting long-form WebGL already needs". The
# probe had neither, so the cheap check that exists to SAVE a two-hour render was instead
# throwing the episode away on a failure the expensive step would have shrugged off.
CONC="${PD_RENDER_CONCURRENCY:-}"
CONC_ARG=""
[ -n "$CONC" ] && CONC_ARG="--concurrency=$CONC"

probe_once() {
  ( cd remotion && npx remotion render "$COMP" "../$OUT" --public-dir="$(basename "$PUB")" \
      --frames="${START}-${END}" $1 ) > "$2" 2>&1
}

echo "[probe] rendering frames ${START}-${END} of ${TOTAL} (60s) before the full film"
probe_once "$CONC_ARG" "$LOG"
if [ ! -f "$OUT" ]; then
  echo "[probe] first attempt produced no file -- retrying once at --concurrency=4" >&2
  tail -6 "$LOG" >&2
  rm -f "$OUT"
  probe_once "--concurrency=4" "${LOG%.log}.retry.log"
  LOG="${LOG%.log}.retry.log"
fi
if [ ! -f "$OUT" ]; then
  echo "[probe] REFUSED: the probe render itself failed twice -- see $LOG" >&2
  tail -12 "$LOG" >&2
  exit 1
fi

BLACK=$(ffmpeg -hide_banner -v info -i "$OUT" -vf "blackdetect=d=0.6:pix_th=0.10" -an -f null - 2>&1 \
        | grep -c "black_start" || true)
FROZEN=$(ffmpeg -hide_banner -v info -i "$OUT" -vf "freezedetect=n=-55dB:d=3" -an -f null - 2>&1 \
        | grep -c "freeze_start" || true)
DARK=$(py -3.11 - "$OUT" <<'PY'
import re, subprocess, sys, statistics
r = subprocess.run(["ffmpeg", "-hide_banner", "-v", "info", "-i", sys.argv[1], "-vf",
                    "signalstats,metadata=print:key=lavfi.signalstats.YAVG", "-f", "null", "-"],
                   capture_output=True, text=True)
ys = [float(m.group(1)) for m in re.finditer(r"YAVG=([0-9.]+)", r.stderr)]
print(round(100 * sum(1 for y in ys if y < 45) / max(1, len(ys)), 1))
PY
)

echo "[probe] black stretches: ${BLACK}   frozen stretches: ${FROZEN}   dark frames: ${DARK}%"
if [ "${BLACK:-0}" -gt 0 ] || [ "${FROZEN:-0}" -gt 0 ]; then
  echo "[probe] REFUSED: the 60s slice already shows black/frozen frames. Fix it now -- a full"
  echo "        render would only reproduce this two hours later." >&2
  exit 1
fi
# Record it. Rendering the slice and then discarding the measurement is why the HARD
# probe_receipt gate kept reading a receipt bound to an EARLIER film.json and failing: norfolk,
# willingham and morton were each waived through with a full-length rescan for want of this call.
# --probe re-measures this same slice (motion_energy as well as black and freeze) and stamps the
# current <slug>_film.json sha, which is precisely the binding the acceptance gate looks for.
EPDIR=$(ls -d episodes/PD-*-"$SLUG" 2>/dev/null | head -1)
if [ -z "$EPDIR" ]; then
  echo "[probe] REFUSED: no episodes/PD-*-${SLUG} directory, so the receipt cannot be written." >&2
  echo "        Acceptance would fail later on a receipt from a different render." >&2
  exit 1
fi
if ! py -3.11 scripts/check_final_acceptance.py "$SLUG" --probe "$OUT"; then
  echo "[probe] REFUSED: the receipt records a FAIL on this slice -- do not spend the render." >&2
  exit 1
fi
echo "[probe] clean -- full render approved (receipt written and bound to this film.json)"
