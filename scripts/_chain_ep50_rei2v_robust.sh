#!/bin/bash
# Robust EP50 face-clean re-i2v: auto-restart ComfyUI on crash, resume batch (skips done), assemble.
cd /c/Users/aab15/Documents/prime-documentary
# --- single-instance lock: refuse to start if another chain is alive (prevents the
#     double-launch that garbled the log + double-queued clips on 2026-07-28) ---
LOCK="out_rei2v_robust.lock"
if [ -f "$LOCK" ] && kill -0 "$(cat "$LOCK" 2>/dev/null)" 2>/dev/null; then
  echo "[robust] another chain (pid $(cat "$LOCK")) is running -- refusing to double-launch"; exit 0
fi
echo $$ > "$LOCK"
trap 'rm -f "$LOCK"' EXIT
LOG=out_rei2v_robust.log
CVENV="/c/Users/aab15/ComfyUI/venv/Scripts/python.exe"
echo "[robust] START $(date)" >> $LOG

count_people(){ ls -d /c/Users/aab15/ae-demo/wan_frames_cp_P* 2>/dev/null | wc -l; }
comfy_up(){ [ "$(curl -s -m 6 -o /dev/null -w '%{http_code}' http://127.0.0.1:8188/system_stats 2>/dev/null)" = "200" ]; }

ensure_comfy(){
  comfy_up && return 0
  echo "[robust] ComfyUI down -> freeing webui VRAM + launching" >> $LOG
  curl -s -m 15 -X POST http://127.0.0.1:7860/sdapi/v1/unload-checkpoint >/dev/null 2>&1
  # kill any stale comfy on 8188
  for pid in $(netstat -ano 2>/dev/null | grep ':8188' | grep LISTENING | grep -oE '[0-9]+$' | head -1); do taskkill //F //PID $pid >/dev/null 2>&1; done
  sleep 2
  ( cd /c/Users/aab15/ComfyUI && "$CVENV" main.py >> comfyui_boot.log 2>&1 ) &
  for i in $(seq 1 70); do
    sleep 3
    comfy_up && { echo "[robust] ComfyUI UP after ${i}x3s" >> $LOG; sleep 4; return 0; }
  done
  echo "[robust] ComfyUI FAILED to boot" >> $LOG; return 1
}

attempt=0
while [ "$(count_people)" -lt 76 ] && [ $attempt -lt 40 ]; do
  attempt=$((attempt+1))
  echo "[robust] attempt $attempt people=$(count_people)/76 $(date)" >> $LOG
  # CHUNK MODE: if I2V_MAX set, force a FRESH ComfyUI before each chunk so Wan's
  # VRAM leak never accumulates to the ~8-30-clip hard crash.
  if [ -n "${I2V_MAX:-}" ] && comfy_up; then
    for pid in $(netstat -ano 2>/dev/null | grep ':8188' | grep LISTENING | grep -oE '[0-9]+$' | head -1); do taskkill //F //PID $pid >/dev/null 2>&1; done
    sleep 3
  fi
  ensure_comfy || { sleep 15; continue; }
  py -3.11 scripts/i2v_centralpark_batch.py >> out_i2v_reclean2.log 2>&1
  echo "[robust] batch/chunk returned people=$(count_people)/76" >> $LOG
  sleep 4
done

echo "[robust] i2v phase done people=$(count_people)/76 -> assemble $(date)" >> $LOG
py -3.11 scripts/assemble_centralpark_i2v.py >> out_i2v_reclean2.log 2>&1
CPN=$(ls E:/pd-media/assets/ai_video/centralpark/motion2/cp_P*.mp4 2>/dev/null | wc -l)
echo "[robust] ASSEMBLE DONE cp_P mp4=$CPN" >> $LOG
# free VRAM for the render: kill ComfyUI
for pid in $(netstat -ano 2>/dev/null | grep ':8188' | grep LISTENING | grep -oE '[0-9]+$' | head -1); do taskkill //F //PID $pid >/dev/null 2>&1; done
echo "[robust] EP50 face-clean i2v+assemble COMPLETE cp_P=$CPN $(date)" >> $LOG
