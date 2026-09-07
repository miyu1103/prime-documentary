#!/bin/bash
# PD GUARDED RENDER -- the ONLY sanctioned way to render a PD film.
# Enforces: PRE-RENDER GATE (block on fail) -> render -> POST-RENDER GATE (block on fail).
# Never spend 6h of render on a film that will fail QC; never show the owner a defective mp4.
#
# Usage:
#   scripts/pd_render_guarded.sh <compId> <film.json> <public_dir> <out.mp4> <expect_sec>
# e.g.
#   scripts/pd_render_guarded.sh Ep50Centralpark remotion/src/data/centralpark_film.json \
#        remotion/public_slim out/centralpark.mp4 3652
set -u
cd /c/Users/aab15/Documents/prime-documentary
COMP="$1"; FILM="$2"; PUB="$3"; OUT="$4"; EXPECT="${5:-0}"
export PYTHONIOENCODING=utf-8

echo "=== [1/4] PRE-RENDER GATE ==="
py -3.11 scripts/pd_prerender_gate.py "$FILM" "$PUB" || { echo ">>> PRE-RENDER GATE FAILED -- render ABORTED. Fix the film/assets, re-run."; exit 1; }

echo "=== [2/4] GPU ready (Remotion/WebGL needs the 4090 free) ==="
py -3.11 scripts/pd_gpu_lock.py status
# ensure no i2v is holding the GPU
util=$(nvidia-smi --query-gpu=utilization.gpu --format=csv,noheader,nounits 2>/dev/null | head -1)
if [ "${util:-0}" -gt 50 ] && curl -s -m5 -o /dev/null http://127.0.0.1:8188/system_stats 2>/dev/null; then
  echo ">>> GPU is busy with ComfyUI (i2v). SERIALIZE: wait for i2v to finish before rendering. ABORT."; exit 1
fi

echo "=== [3/4] RENDER $COMP -> $OUT ==="
mkdir -p "$(dirname "$OUT")"
LOGF="out_render_$(basename "$OUT").log"
CONC="${PD_RENDER_CONCURRENCY:-}"
# 2026-08-08: willingham died twice at "Timed out after 30000ms while setting up the headless
# browser" while the 2.9GB public-dir copy was still hitting the disk. 120s costs nothing on
# success and rides out that class of disk contention.
TIMEOUT_MS="${PD_RENDER_TIMEOUT_MS:-120000}"
CONC_ARG=""
[ -n "$CONC" ] && CONC_ARG="--concurrency=$CONC"
TIMEOUT_ARG="--timeout=$TIMEOUT_MS"
( cd remotion && npx remotion render "$COMP" "../$OUT" --public-dir="$(basename "$PUB")" $CONC_ARG "$TIMEOUT_ARG" ) > "$LOGF" 2>&1
rc=$?
# EP52 morton, 2026-07-30: the render died on `Failed to fetch .../factory/AR-*.mp4` +
# `Error: Request closed` while a 61-minute acceptance gate was hammering the same disk. The
# clips were all readable afterwards -- it was contention, not corruption. One retry at
# concurrency 4 (the setting long-form WebGL already needs) turns that class of failure from a
# dead queue into a slower render.
if [ $rc -ne 0 ] || [ ! -f "$OUT" ]; then
  echo ">>> RENDER FAILED rc=$rc -- retrying once at --concurrency=4"
  grep -aoE "Failed to fetch [^ ]{0,120}|Error: [A-Za-z ]{0,60}" "$LOGF" | sort | uniq -c | sort -rn | head -3
  rm -f "$OUT"
  ( cd remotion && npx remotion render "$COMP" "../$OUT" --public-dir="$(basename "$PUB")" --concurrency=4 "$TIMEOUT_ARG" ) > "${LOGF%.log}.retry.log" 2>&1
  rc=$?
fi
if [ $rc -ne 0 ] || [ ! -f "$OUT" ]; then echo ">>> RENDER FAILED rc=$rc (see out_render log). ABORT."; exit 1; fi

echo "=== [4/4] POST-RENDER GATE ==="
py -3.11 scripts/pd_postrender_gate.py "$OUT" --expect-sec "$EXPECT" --frames 30 --out "qc_frames_$(basename "$OUT" .mp4)" \
  || { echo ">>> POST-RENDER GATE FAILED -- DO NOT show the owner. Fix + re-render."; exit 1; }

echo "=== GUARDED RENDER COMPLETE: $OUT PASSED both gates. NOW watch the FULL runtime before showing the owner. ==="
