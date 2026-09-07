#!/bin/bash
# EP77 keybridge BATCH C/D: 4K upscale then depth for the 16 replacement plates H132-H147.
#
# All 16 were reviewed at 776 px on 2026-08-26 and all 16 passed
# (runs/qc/keybridge_batch_cd_verdicts.v001.json). They replace the 16 rejected for period
# drift, so they carry NEW ids -- reusing a live id overwrites a plate already in the film.
#
# Queues behind whatever holds the upscale lock (EP85 is upscaling on the same GPU).
set -u
cd /c/Users/aab15/Documents/prime-documentary
VENV_SD="C:/Users/aab15/stable-diffusion-webui/venv/Scripts/python.exe"
VENV_COMFY="C:/Users/aab15/ComfyUI/venv/Scripts/python.exe"
LOG=out_gpu_queue_ep77_batchcd.log
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

run_step ep77-cd-upscale "$VENV_SD" scripts/upscale_plates_4k_esrgan.py --slug keybridge \
  --src "E:/pd-media/05_visuals/keybridge/img_raw_codex_batch_c_v001" --prefix H --count 16 --resume
run_step ep77-cd-depth   "$VENV_COMFY" tools/depth/gen_depth.py remotion/public/keybridge/img
echo "[queue] done $(date)" >> "$LOG"

# Count the disk, not the exit codes: a previous queue reported "done" with 0 depth maps.
n=$(ls remotion/public/keybridge/img/*.png 2>/dev/null | grep -vc _depth)
d=$(ls remotion/public/keybridge/img/*_depth.png 2>/dev/null | wc -l)
echo "[queue] keybridge: $n png / $d depth" >> "$LOG"
