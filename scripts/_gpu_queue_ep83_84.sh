#!/bin/bash
# EP83 max737 and EP84 threemile: 4K upscale then depth maps. GPU serial, resumable.
set -u
cd /c/Users/aab15/Documents/prime-documentary
VENV_SD="C:/Users/aab15/stable-diffusion-webui/venv/Scripts/python.exe"
VENV_COMFY="C:/Users/aab15/ComfyUI/venv/Scripts/python.exe"
LOG=out_gpu_queue_ep83_84.log
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
run_step ep83-upscale "$VENV_SD" scripts/upscale_plates_4k_esrgan.py --slug max737 --src "E:/pd-media/05_visuals/max737/img" --prefix X --count 188 --resume
run_step ep84-upscale "$VENV_SD" scripts/upscale_plates_4k_esrgan.py --slug threemile --src "E:/pd-media/05_visuals/threemile/img" --prefix T --count 186 --resume
run_step ep83-depth   "$VENV_COMFY" tools/depth/gen_depth.py remotion/public/max737/img
run_step ep84-depth   "$VENV_COMFY" tools/depth/gen_depth.py remotion/public/threemile/img
echo "[queue] done $(date)" >> "$LOG"
for s in max737 threemile; do
  n=$(ls remotion/public/$s/img/*.png 2>/dev/null | grep -vc _depth); d=$(ls remotion/public/$s/img/*_depth.png 2>/dev/null | wc -l)
  echo "[queue] $s: $n png / $d depth" >> "$LOG"
done
