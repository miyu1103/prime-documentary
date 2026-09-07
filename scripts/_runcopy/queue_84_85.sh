#!/usr/bin/env bash
# Serial finisher queue for EP84 threemile and EP85 katrina.
#
# WHY A SCRIPT AND NOT TWO COMMANDS. Two silent stalls cost about twelve hours in the EP83
# run: a plate agent died and nothing started the next episode, and an i2v chain finished at
# 03:30 and was noticed at 09:54. A machine that is waiting for a human to notice is a machine
# that is off. This waits for the EP83 render to release the GPU and then runs both episodes
# back to back, writing a heartbeat so its state is a file, not a memory.
#
# It runs the finisher through _runcopy copies for the same reason every long job does: bash
# re-reads a running script by byte offset, so editing scripts/_finish_episode.sh mid-run
# corrupts the shell that is executing it (measured twice: "line 205: LUG}.mp4.log)").
set -u
cd "$(dirname "$0")/../.." || exit 1
HB=runs/queue_84_85.heartbeat

note() { printf '%s  %s\n' "$(date '+%m-%d %H:%M')" "$*" | tee -a "$HB"; }

# Wait for max737 to stop occupying the renderer. Poll on the PROCESS, not on a log line:
# an earlier watchdog grepped for "COMPLETE" and matched a line left by a previous run,
# reporting done with zero clips produced.
note "waiting for the EP83 max737 finisher to exit"
while pgrep -f "finish_max737_v7.sh" > /dev/null 2>&1; do sleep 60; done
note "EP83 finisher has exited"

for pair in "threemile:Ep84ThreeMile:84" "katrina:Ep85Katrina:85"; do
  SLUG=${pair%%:*}; REST=${pair#*:}; COMP=${REST%%:*}; NUM=${REST##*:}
  CP="scripts/_runcopy/finish_${SLUG}_q1.sh"
  cp scripts/_finish_episode.sh "$CP"
  note "START $SLUG ($COMP, EP$NUM)"
  if bash "$CP" "$SLUG" "$COMP" "$NUM" >> "runs/queue_${SLUG}.log" 2>&1; then
    note "DONE  $SLUG -- master built"
  else
    note "FAIL  $SLUG -- see runs/queue_${SLUG}.log (the queue continues to the next episode)"
  fi
done
note "queue finished"
