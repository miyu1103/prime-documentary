#!/bin/bash
# EP80 concordia BATCH B: 4K upscale then depth for the 3 replacement plates N001, N104, N141.
#
# All three passed review on 2026-08-27 (runs/qc/concordia_batchb_verdicts.v001.json): the
# clinometer is unchanged -- it is the right instrument and the film's own motif -- and the
# open-flame oil lantern the first prompt produced is gone, replaced by a modern LED bulkhead
# light on a ship delivered in 2006.
#
# SAME ids as the plates they replace, because all three are in the spec's mandatory_stills and
# a new id would contradict the contract. The old files are in img/rejected/ and stay there.
#
# i2v is on the same GPU. The upscaler halves its tile size and retries rather than dying when
# VRAM is short, and the lock is honoured.
set -u
cd /c/Users/aab15/Documents/prime-documentary
VENV_SD="C:/Users/aab15/stable-diffusion-webui/venv/Scripts/python.exe"
VENV_COMFY="C:/Users/aab15/ComfyUI/venv/Scripts/python.exe"
LOG=out_gpu_queue_ep80_batchb.log
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

run_step ep80-b-upscale "$VENV_SD" scripts/upscale_plates_4k_esrgan.py --slug concordia \
  --src "E:/pd-media/05_visuals/concordia/img_raw_codex_batch_b_v001" --prefix N --count 3 --resume
run_step ep80-b-depth   "$VENV_COMFY" tools/depth/gen_depth.py remotion/public/concordia/img

# EP82 valdez V079 was delivered into its own batch directory and never upscaled -- the delivery
# report only scanned the directory root, so it read as missing for a day. Same queue, one plate.
run_step ep82-v079-upscale "$VENV_SD" scripts/upscale_plates_4k_esrgan.py --slug valdez \
  --src "E:/pd-media/05_visuals/valdez/img_raw_codex_batch_b_v001" --prefix V --count 1 --resume
run_step ep82-v079-depth   "$VENV_COMFY" tools/depth/gen_depth.py remotion/public/valdez/img

echo "[queue] done $(date)" >> "$LOG"
# Count the disk, not the exit codes: an earlier queue reported "done" with 0 depth maps.
for s in concordia valdez; do
  n=$(ls remotion/public/$s/img/*.png 2>/dev/null | grep -vc _depth)
  d=$(ls remotion/public/$s/img/*_depth.png 2>/dev/null | wc -l)
  echo "[queue] $s: $n png / $d depth" >> "$LOG"
done
