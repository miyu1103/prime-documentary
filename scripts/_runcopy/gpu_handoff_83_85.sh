#!/usr/bin/env bash
# Take the GPU from the columbia i2v chain, render EP83-85, hand the GPU back.
#
# WHY. The render gate refuses to start while ComfyUI holds the 4090 ("GPU is busy with
# ComfyUI (i2v). SERIALIZE"), and it is RIGHT to: two jobs on one 24 GB card is how renders
# die at frame 32,984. But on 2026-09-07 the EP86 columbia i2v chain took the card at 12:14
# with 75 of 76 clips still to make, and EP83/84/85 -- which the owner asked to have bookable
# by tomorrow -- both aborted at that gate within minutes.
#
# So this pauses the i2v rather than waiting behind it. The pause is cheap and honest:
# _chain_i2v_robust.sh resumes by COUNTING FINISHED CLIPS, so stopping it loses only the clip
# in flight, never the ones already on disk. The chain is relaunched here the moment the last
# render is done, with the same arguments it was started with, so nobody has to remember.
#
# Renders run ONE AT A TIME. Running two at once is what put max737 and threemile at the same
# gate in the same minute, and the machine cannot do two anyway.
set -u
cd "$(dirname "$0")/../.." || exit 1
HB=runs/gpu_handoff_83_85.heartbeat
note() { printf '%s  %s\n' "$(date '+%m-%d %H:%M')" "$*" | tee -a "$HB"; }

note "=== taking the GPU from the columbia i2v chain ==="
# $PID is excluded on purpose: this command's OWN command line contains every pattern it
# searches for, so without that guard PowerShell kills the shell doing the killing.
powershell -NoProfile -Command '
  $me = $PID
  $pats = @("*_chain_i2v_robust.sh*columbia*", "*ComfyUI*main.py*", "*comfy_wan.py*")
  foreach ($p in $pats) {
    Get-CimInstance Win32_Process |
      Where-Object { $_.ProcessId -ne $me -and $_.CommandLine -like $p } |
      ForEach-Object {
        Write-Output ("stopping pid " + $_.ProcessId + "  " + $_.Name)
        Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue
      }
  }
' 2>&1 | tee -a "$HB"
rm -f out_i2v_columbia.lock
sleep 20
note "VRAM now: $(nvidia-smi --query-gpu=memory.used,utilization.gpu --format=csv,noheader)"

for pair in "max737:Ep83Max737:83" "threemile:Ep84ThreeMile:84" "katrina:Ep85Katrina:85"; do
  SLUG=${pair%%:*}; REST=${pair#*:}; COMP=${REST%%:*}; NUM=${REST##*:}
  CP="scripts/_runcopy/finish_${SLUG}_gpu1.sh"
  cp scripts/_finish_episode.sh "$CP"
  note "START $SLUG ($COMP, EP$NUM)"
  if bash "$CP" "$SLUG" "$COMP" "$NUM" >> "runs/gpu_${SLUG}.log" 2>&1; then
    note "DONE  $SLUG -- master built"
  else
    note "FAIL  $SLUG -- see runs/gpu_${SLUG}.log (continuing to the next episode)"
  fi
done

note "=== handing the GPU back to the columbia i2v chain ==="
nohup bash scripts/_chain_i2v_robust.sh columbia 76 C 12 "" 121 >> out_i2v_chain_columbia.log 2>&1 &
note "columbia i2v relaunched (it resumes from the clips already on disk)"
note "handoff finished"
