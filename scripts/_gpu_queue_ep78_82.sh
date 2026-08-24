#!/bin/bash
# Serial GPU queue for the EP77-82 left process: finish the running EP78 upscale, then
# upscale EP79/80/81, then depth maps for every upscaled episode. One GPU job at a time
# (CLAUDE.md rule 7); each step goes through pd_run.sh so locks and first-error checks hold.
# EP82 is NOT here: its pool waits on the regeneration round, then gets its own pass.
set -u
cd /c/Users/aab15/Documents/prime-documentary
VENV_SD="C:/Users/aab15/stable-diffusion-webui/venv/Scripts/python.exe"
VENV_COMFY="C:/Users/aab15/ComfyUI/venv/Scripts/python.exe"
LOG=out_gpu_queue_ep78_82.log
echo "[queue] start $(date)" > "$LOG"

wait_lock () {  # wait for the pd_run 'upscale' class lock to clear
  while [ -f out_pdrun_upscale.lock ]; do
    pid=$(tr -d '[:space:]' < out_pdrun_upscale.lock 2>/dev/null)
    if [ -n "$pid" ] && tasklist //FI "PID eq $pid" 2>/dev/null | grep -q "$pid"; then
      sleep 60
    else
      break
    fi
  done
}

run_step () {  # name, then the command words
  name="$1"; shift
  wait_lock
  echo "[queue] $name $(date)" >> "$LOG"
  bash scripts/pd_run.sh --name "$name" --class upscale \
    --smoke "\"$VENV_SD\" -c \"import torch;print(torch.cuda.is_available())\"" -- "$@" >> "$LOG" 2>&1
  # pd_run returns once the job survived 60s; wait for THIS job to actually finish
  wait_lock
}

# Counts are the FULL delivered set including the 2026-08-25 regeneration round.
run_step ep78-add    "$VENV_SD" scripts/upscale_plates_4k_esrgan.py --slug colgan --src "E:/pd-media/05_visuals/colgan/img" --prefix C --count 168 --only C123,C135
run_step ep79-upscale "$VENV_SD" scripts/upscale_plates_4k_esrgan.py --slug alaska261 --src "E:/pd-media/05_visuals/alaska261/img" --prefix K --count 198
run_step ep80-upscale "$VENV_SD" scripts/upscale_plates_4k_esrgan.py --slug concordia --src "E:/pd-media/05_visuals/concordia/img" --prefix N --count 185
run_step ep77-depth "$VENV_COMFY" tools/depth/gen_depth.py remotion/public/keybridge/img
run_step ep78-depth "$VENV_COMFY" tools/depth/gen_depth.py remotion/public/colgan/img
run_step ep79-depth "$VENV_COMFY" tools/depth/gen_depth.py remotion/public/alaska261/img
run_step ep80-depth "$VENV_COMFY" tools/depth/gen_depth.py remotion/public/concordia/img
run_step ep81-depth "$VENV_COMFY" tools/depth/gen_depth.py remotion/public/station/img
echo "[queue] done $(date)" >> "$LOG"
for s in keybridge colgan alaska261 concordia station; do
  n=$(ls remotion/public/$s/img/*.png 2>/dev/null | wc -l)
  d=$(ls remotion/public/$s/img/*_depth.png 2>/dev/null | wc -l)
  echo "[queue] $s: $n png / $d depth" >> "$LOG"
done
