#!/usr/bin/env bash
# Post-render assembly for EP34 rolin. Runs AFTER out/rolin_full.mp4 exists (68,928 frames).
# Steps: verify render -> mux 4-layer WAV -> probe slice -> probe receipt -> full acceptance.
# Does NOT schedule/upload (owner GO required). Idempotent-ish; safe to re-run.
set -u
ROOT="C:/Users/aab15/Documents/prime-documentary"
cd "$ROOT" || exit 2
EP="PD-2026-034-rolin"
VID="remotion/out/rolin_full.mp4"
MUXED="remotion/out/${EP}_film.muxed.v001.mp4"

echo "### 1) verify render exists & frame count"
[ -f "$VID" ] || { echo "MISSING $VID -- render not done"; exit 1; }
frames=$(ffprobe -v error -select_streams v:0 -count_frames -show_entries stream=nb_read_frames -of default=nk=1:nw=1 "$VID" 2>/dev/null)
echo "render frames: $frames (want 68928)"
[ "$frames" = "68928" ] || { echo "FRAME COUNT MISMATCH -- do not proceed"; exit 1; }

echo "### 2) mux 4-layer -14LUFS WAV as sole audio (stamps sha)"
python scripts/build_case_film_mux.py --ep "$EP" --video "$VID" || exit 1
[ -f "$MUXED" ] || { echo "mux did not produce $MUXED"; exit 1; }

echo "### 3) cut a 90s representative body slice for the probe"
# body section (skip hook+opening ~20s; well inside narration). re-encode ok for a motion probe.
ffmpeg -y -ss 300 -t 90 -i "$MUXED" -an -c:v libx264 -crf 18 -pix_fmt yuv420p \
  remotion/out/rolin_probe_slice.mp4 >/dev/null 2>&1 || exit 1

echo "### 4) probe receipt (motion/black/freeze; binds to film.json sha)"
python scripts/check_final_acceptance.py "$EP" --probe remotion/out/rolin_probe_slice.mp4 || echo "PROBE returned non-zero (inspect)"

echo "### 5) FULL acceptance gate (emit receipt)"
python scripts/check_final_acceptance.py "$EP" --render "$MUXED" --emit-receipt --json
echo "### done. Review acceptance_receipt + runtime_band deviation before any owner-GO scheduling."
