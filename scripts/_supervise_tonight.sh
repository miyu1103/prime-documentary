#!/bin/bash
# NOTHING IS ALLOWED TO SILENTLY STOP. Added 2026-08-16 on the owner's instruction:
#
#   「順調？とか君に聞かないと油断すると止まってることが多々ある。そうならないようにしてほしい」
#
# The failure this prevents is not a crash. It is a chain that finishes its own job correctly and
# then leaves the machine idle because the NEXT thing was a sentence in a log instead of a command.
# That is exactly how 08-14 to 08-16 was lost: greene's upload died between "uploaded" and
# "scheduled", nothing restarted it, and nobody looked for two days.
#
# This supervises, it does not do the work:
#   1. the i2v chain for EP66-69 -- restarted if it dies before all four are converted
#   2. the render queue          -- STARTED, not suggested, the moment i2v is finished
#   3. a heartbeat every cycle   -- so "is it running?" is answered by a file, not by asking
#
#   nohup bash scripts/_supervise_tonight.sh > out_supervisor_0816.log 2>&1 &
set -u
cd /c/Users/aab15/Documents/prime-documentary

BEAT="runs/SUPERVISOR_HEARTBEAT.txt"
LOG="out_supervisor_0816.log"
mkdir -p runs
say() { echo "[sup] $(date '+%m-%d %H:%M') $*" | tee -a "$LOG"; }

# slug:target -- target counts frame dirs on disk, the only honest measure of i2v progress.
TARGETS="openfields:53 ramirez:50 pinto:54 hyatt:32"

# COUNT THE CLIPS, NOT THE SCAFFOLDING.
# 2026-08-17: this counted wan_frames_<slug>_* directories. 24.5 GB of those were reclaimed once
# their mp4s existed -- correct, the film reads the mp4 -- and this counter instantly read 157
# finished conversions as unstarted, which would have sent the chain off to regenerate them.
# The mp4 in the render-visible pool IS the deliverable. Ask about that.
count_done() { ls "remotion/public/${1}/motion/"*.mp4 2>/dev/null | wc -l; }

alive() {   # pattern -> 0 when at least one process matches, excluding the probe itself
  local n
  n=$(powershell -NoProfile -Command \
      "@(Get-CimInstance Win32_Process | Where-Object { \$_.CommandLine -like '*$1*' -and \$_.CommandLine -notlike '*Get-CimInstance*' }).Count" \
      2>/dev/null | tr -d '\r ')
  case "$n" in ''|*[!0-9]*) return 0 ;; esac   # unreadable probe -> assume alive, never double-launch
  [ "$n" -gt 0 ]
}

i2v_complete() {
  local job slug target
  for job in $TARGETS; do
    slug="${job%%:*}"; target="${job##*:}"
    [ "$(count_done "$slug")" -ge "$target" ] || return 1
  done
  return 0
}

say "START -- supervising i2v for EP66-69, then the render queue"

while true; do
  {
    echo "supervisor alive $(date '+%Y-%m-%d %H:%M:%S')"
    for job in $TARGETS; do
      slug="${job%%:*}"; target="${job##*:}"
      echo "  i2v $slug $(count_done "$slug")/$target"
    done
    echo "  i2v chain running: $(alive '_chain_i2v' && echo yes || echo no)"
    echo "  render queue running: $(alive 'queue_unattended' && echo yes || echo no)"
  } > "$BEAT"

  if i2v_complete; then
    if alive "queue_unattended"; then
      :
    else
      say "i2v COMPLETE for all four -- starting the render queue myself"
      nohup bash scripts/queue_unattended.sh > out_queue_after_i2v.log 2>&1 &
      sleep 120
    fi
  else
    # i2v still owed. The GPU takes one job, so the queue must NOT be running yet.
    if ! alive "_chain_i2v"; then
      say "i2v chain is NOT running and work remains -- relaunching"
      nohup bash scripts/_chain_i2v_ep66_69.sh >> out_i2v_ep66_69.log 2>&1 &
      sleep 120
    fi
  fi

  sleep 300
done
