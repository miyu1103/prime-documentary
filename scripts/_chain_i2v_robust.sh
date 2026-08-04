#!/bin/bash
# Generic robust i2v chain: chunked Wan i2v with a FRESH ComfyUI per chunk, auto-restart on
# crash, correct resume (frame-dir based), then assemble. Generalised from
# _chain_ep50_rei2v_robust.sh so every episode gets the same crash-proof path.
#
#   scripts/_chain_i2v_robust.sh <slug> <target_clip_count> [kinds] [chunk_size]
# e.g.
#   scripts/_chain_i2v_robust.sh willingham 30 M 12
#
# Enforces (feedback-no-render-churn): single-instance lock, fresh ComfyUI per chunk,
# webui VRAM released before each boot, bounded attempts, honest on-disk progress counting.
set -u
cd /c/Users/aab15/Documents/prime-documentary

SLUG="${1:?usage: _chain_i2v_robust.sh <slug> <target> [kinds] [chunk]}"
TARGET="${2:?target clip count required}"
KINDS="${3:-M}"
CHUNK="${4:-12}"
# Optional 5th arg: comma-separated substrings naming the ONLY source plates to convert.
# EP61 weimer motion-converts a named 65 of its 150 commissioned stills; the rest must stay
# stills. Empty = every plate matching KINDS, exactly as before.
ONLY="${5:-}"
# Optional 6th arg: Wan clip length in frames. 81 (the batch default) assembles to 3.4s, which
# has to LOOP inside EP61 weimer's ~5.9s cuts; 121 is the 5B model's native length and covers it.
LENGTH="${6:-}"
# Optional env: constrain WHAT may move. See the --prompt/--neg note in i2v_episode_batch.py.
I2V_PROMPT="${I2V_PROMPT:-}"
I2V_NEG="${I2V_NEG:-}"
I2V_SEED_BASE="${I2V_SEED_BASE:-}"
MAX_ATTEMPTS=60

LOCK="out_i2v_${SLUG}.lock"
LOG="out_i2v_${SLUG}.log"
CVENV="/c/Users/aab15/ComfyUI/venv/Scripts/python.exe"

if [ -f "$LOCK" ] && kill -0 "$(cat "$LOCK" 2>/dev/null)" 2>/dev/null; then
  echo "[chain:$SLUG] another chain (pid $(cat "$LOCK")) is running -- refusing to double-launch"
  exit 0
fi
echo $$ > "$LOCK"
trap 'rm -f "$LOCK"' EXIT

echo "[chain:$SLUG] START $(date) target=$TARGET kinds=$KINDS chunk=$CHUNK" >> "$LOG"

# Progress is counted from the frame dirs comfy_wan actually writes -- never from a tool's word.
count_done(){
  local n=0
  for d in /c/Users/aab15/ae-demo/wan_frames_${SLUG}_*; do
    [ -d "$d" ] || continue
    if [ "$(ls "$d"/*.png 2>/dev/null | wc -l)" -ge 40 ]; then n=$((n+1)); fi
  done
  echo "$n"
}
comfy_up(){ [ "$(curl -s -m 6 -o /dev/null -w '%{http_code}' http://127.0.0.1:8188/system_stats 2>/dev/null)" = "200" ]; }
kill_comfy(){
  for pid in $(netstat -ano 2>/dev/null | grep ':8188' | grep LISTENING | grep -oE '[0-9]+$' | head -1); do
    taskkill //F //PID "$pid" >/dev/null 2>&1
  done
}
ensure_comfy(){
  comfy_up && return 0
  echo "[chain:$SLUG] ComfyUI down -> releasing webui VRAM + launching" >> "$LOG"
  curl -s -m 15 -X POST http://127.0.0.1:7860/sdapi/v1/unload-checkpoint >/dev/null 2>&1
  kill_comfy
  sleep 2
  ( cd /c/Users/aab15/ComfyUI && "$CVENV" main.py >> comfyui_boot.log 2>&1 ) &
  for i in $(seq 1 70); do
    sleep 3
    comfy_up && { echo "[chain:$SLUG] ComfyUI UP after ${i}x3s" >> "$LOG"; sleep 4; return 0; }
  done
  echo "[chain:$SLUG] ComfyUI FAILED to boot" >> "$LOG"
  return 1
}

attempt=0
while [ "$(count_done)" -lt "$TARGET" ] && [ $attempt -lt $MAX_ATTEMPTS ]; do
  attempt=$((attempt+1))
  echo "[chain:$SLUG] attempt $attempt done=$(count_done)/$TARGET $(date)" >> "$LOG"
  # Fresh ComfyUI before EVERY chunk: Wan's VRAM leak reaches a hard crash around
  # 20-30 clips, so we never let one instance get that far.
  kill_comfy
  sleep 3
  ensure_comfy || { sleep 15; continue; }
  I2V_MAX="$CHUNK" py -3.11 scripts/i2v_episode_batch.py --slug "$SLUG" --kinds "$KINDS" ${ONLY:+--only "$ONLY"} ${LENGTH:+--length "$LENGTH"} ${I2V_PROMPT:+--prompt "$I2V_PROMPT"} ${I2V_NEG:+--neg "$I2V_NEG"} ${I2V_SEED_BASE:+--seed-base "$I2V_SEED_BASE"} >> "$LOG" 2>&1
  after=$(count_done)
  echo "[chain:$SLUG] chunk end done=$after/$TARGET" >> "$LOG"
  # assemble what is finished so far (idempotent, safe while more are in flight)
  py -3.11 scripts/assemble_episode_i2v.py --slug "$SLUG" >> "$LOG" 2>&1
  sleep 4
done

FINAL=$(count_done)
echo "[chain:$SLUG] i2v phase end done=$FINAL/$TARGET attempts=$attempt $(date)" >> "$LOG"
py -3.11 scripts/assemble_episode_i2v.py --slug "$SLUG" >> "$LOG" 2>&1
MP4=$(ls "H:/pd-media/assets/ai_video/${SLUG}/motion/"*.mp4 2>/dev/null | wc -l)
kill_comfy   # release VRAM for the next GPU job (renders are serialized behind this)
echo "[chain:$SLUG] COMPLETE frames_done=$FINAL mp4=$MP4 $(date)" >> "$LOG"
