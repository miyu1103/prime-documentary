#!/bin/bash
# Render every remaining fixed episode back-to-back, without waiting for a human between them.
#
# On 2026-08-06 ten episodes were pulled off the calendar and seven still need a re-render
# before they can go back. Renders cannot overlap -- two at once slowed both to a crawl, which
# is why pd_run.sh holds a lock -- so the only way to go faster is to never leave the GPU idle
# between them. Started by hand, one at a time, each gap was as long as it took someone to
# notice the last one had finished.
#
#   bash scripts/render_queue.sh postoffice:Ep56Postoffice:56 flowers:Ep54Flowers:54 ...
#
# Each entry is slug:composition:number. The queue waits for the render lock to clear, runs the
# episode's own pre-flight, and skips -- loudly -- any episode whose pre-flight refuses, rather
# than burning an hour on inputs a thirty-second check already rejected. A failure does not stop
# the queue; the remaining episodes still get their turn.
set -u
cd /c/Users/aab15/Documents/prime-documentary

LOG=out_render_queue.log
: > "$LOG"

log() { echo "[queue $(date '+%H:%M:%S')] $*" | tee -a "$LOG"; }

for entry in "$@"; do
  slug="${entry%%:*}"; rest="${entry#*:}"; comp="${rest%%:*}"; num="${rest##*:}"

  # Wait for whatever is rendering now. The lock is pd_run.sh's, so respect it rather than
  # racing it: a second render is the failure this whole script exists to avoid.
  waited=0
  while [ -f out_pdrun_render.lock ]; do
    pid=$(cat out_pdrun_render.lock 2>/dev/null | tr -d '[:space:]')
    # NOT `kill -0`: in Git Bash it returns success for a DEAD Windows pid, so the stale-lock
    # branch never fired and this queue once sat 50 minutes behind a process that had exited.
    # tasklist is the only thing here that can actually see a Windows process.
    if [ -n "$pid" ] && ! tasklist //FI "PID eq $pid" 2>/dev/null | grep -q "$pid"; then
      log "lock held by dead pid $pid -- clearing"
      rm -f out_pdrun_render.lock
      break
    fi
    sleep 60
    waited=$((waited + 1))
    [ $((waited % 10)) -eq 0 ] && log "still waiting for the lock ($((waited)) min)"
  done

  log "=== $slug ($comp) ==="
  if ! py -3.11 scripts/check_episode_inputs.py --slug "$slug" >> "$LOG" 2>&1; then
    log "SKIP $slug -- pre-flight refused, see $LOG. Nothing expensive was started."
    continue
  fi

  if /usr/bin/bash scripts/pd_run.sh --name "queue_$slug" \
       --smoke "py -3.11 scripts/check_episode_inputs.py --slug $slug" \
       -- /usr/bin/bash scripts/_finish_episode.sh "$slug" "$comp" "$num" >> "$LOG" 2>&1; then
    log "started $slug -- waiting for it to finish"
  else
    log "FAILED to start $slug -- moving on"
    continue
  fi

  # pd_run.sh returns once the job has survived 60s; the render itself is still going.
  sleep 30
  # Same stale-lock check as the first loop. 2026-08-08: queue_willingham died at the
  # browser-setup timeout, its lock stayed, and this loop -- which had no dead-pid branch --
  # waited 30+ hours behind dead PID 45388. A wait loop without a liveness check is a deadlock.
  while [ -f out_pdrun_render.lock ]; do
    pid=$(cat out_pdrun_render.lock 2>/dev/null | tr -d "[:space:]")
    if [ -n "$pid" ] && ! tasklist //FI "PID eq $pid" 2>/dev/null | grep -q "$pid"; then
      log "lock held by dead pid $pid -- clearing (post-start wait)"
      rm -f out_pdrun_render.lock
      break
    fi
    sleep 60
  done

  master="episodes/PD-2026-0${num}-${slug}/08_edit/${slug}_final_bgm.v001.mp4"
  if [ -f "$master" ]; then
    log "DONE $slug -> $master ($(stat -c %s "$master" 2>/dev/null) bytes)"
  else
    log "WARNING $slug finished but $master is not there -- check out_finish_${slug}.log"
  fi
done

log "=== QUEUE COMPLETE ==="
