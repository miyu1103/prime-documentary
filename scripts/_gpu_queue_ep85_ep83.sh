#!/bin/bash
# EP85 katrina: 4K upscale then depth. EP83 max737: depth RETRY.
#
# EP85's 186 plates are all delivered at Codex's native 1672x941 and none is staged, which is
# why it was reported as "86 images missing" -- the images were there, the upscale had not run.
# EP83's upscale finished; its depth step died inside 60 seconds with exit 127 on 2026-08-25
# 22:35 (out_gpu_queue_ep83_84.log) and left 188 plates with 0 depth maps. EP84 ran straight
# after it on the same command and produced all 186, so this is a retry, not a fix.
#
# Serial and resumable. i2v is on the same GPU; the upscaler halves its tile size and retries
# rather than dying when VRAM is short.
set -u
cd /c/Users/aab15/Documents/prime-documentary
VENV_SD="C:/Users/aab15/stable-diffusion-webui/venv/Scripts/python.exe"
VENV_COMFY="C:/Users/aab15/ComfyUI/venv/Scripts/python.exe"
LOG=out_gpu_queue_ep85_ep83.log
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

run_step ep85-upscale "$VENV_SD" scripts/upscale_plates_4k_esrgan.py --slug katrina --src "E:/pd-media/05_visuals/katrina/img" --prefix W --count 186 --resume
run_step ep85-depth   "$VENV_COMFY" tools/depth/gen_depth.py remotion/public/katrina/img
run_step ep83-depth   "$VENV_COMFY" tools/depth/gen_depth.py remotion/public/max737/img
echo "[queue] done $(date)" >> "$LOG"

# Count the disk, not the exit codes: the previous queue reported "done" with 0 depth maps.
for s in katrina max737; do
  n=$(ls remotion/public/$s/img/*.png 2>/dev/null | grep -vc _depth)
  d=$(ls remotion/public/$s/img/*_depth.png 2>/dev/null | wc -l)
  echo "[queue] $s: $n png / $d depth" >> "$LOG"
done
