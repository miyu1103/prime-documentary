#!/bin/bash
# valdez: upscale the 183 delivered plates to 4K, then depth maps. GPU serial.
set -u
cd /c/Users/aab15/Documents/prime-documentary
VENV_SD="C:/Users/aab15/stable-diffusion-webui/venv/Scripts/python.exe"
VENV_COMFY="C:/Users/aab15/ComfyUI/venv/Scripts/python.exe"
LOG=out_gpu_queue_valdez.log
echo "[queue] start $(date)" > "$LOG"
wait_lock () {
  while [ -f out_pdrun_upscale.lock ]; do
    pid=$(tr -d '[:space:]' < out_pdrun_upscale.lock 2>/dev/null)
    if [ -n "$pid" ] && tasklist //FI "PID eq $pid" 2>/dev/null | grep -q "$pid"; then sleep 60; else break; fi
  done
}
run_step () { name="$1"; shift; wait_lock; echo "[queue] $name $(date)" >> "$LOG"
  bash scripts/pd_run.sh --name "$name" --class upscale \
    --smoke "\"$VENV_SD\" -c \"import torch;print(torch.cuda.is_available())\"" -- "$@" >> "$LOG" 2>&1
  wait_lock; }
run_step ep82-upscale "$VENV_SD" scripts/upscale_plates_4k_esrgan.py --slug valdez --src "E:/pd-media/05_visuals/valdez/img" --prefix V --count 183
run_step ep82-depth   "$VENV_COMFY" tools/depth/gen_depth.py remotion/public/valdez/img
echo "[queue] done $(date)" >> "$LOG"
n=$(ls remotion/public/valdez/img/*.png 2>/dev/null | grep -vc _depth); d=$(ls remotion/public/valdez/img/*_depth.png 2>/dev/null | wc -l)
echo "[queue] valdez: $n png / $d depth" >> "$LOG"
