#!/bin/bash
# Keep the GPU busy without a human. One job at a time, in deadline order, forever.
#
# Tonight the machine sat idle twice because a job finished and nobody started the next one. The
# GPU takes exactly one job -- i2v and a render cannot overlap -- so a queue that picks the next
# ready episode is worth more than any parallelism.
#
# Idleness is asked of WMI, which carries the full command line. `ps -W` prints only the
# interpreter path, so counting script names there returns 0 while one is plainly running -- the
# guard that let a second render start on top of a live one earlier today.
#
# Renders run from a SNAPSHOT of _finish_episode.sh: editing the original mid-flight desynchronised
# bash's byte offset and killed correa's step 7 after its render had completed.
set -u
cd /c/Users/aab15/Documents/prime-documentary
export PATH="/usr/bin:/bin:$PATH"

SNAP=$(mktemp -d "${TMPDIR:-/tmp}/pdq.XXXXXX")
cp scripts/_finish_episode.sh "$SNAP/_finish_episode.sh"
echo "[q] immutable copy: $SNAP/_finish_episode.sh"

busy() {
  powershell -NoProfile -Command \
    "@(Get-CimInstance Win32_Process | Where-Object { (\$_.CommandLine -like '*remotion*render*' -or \$_.CommandLine -like '*_finish_episode.sh*' -or \$_.CommandLine -like '*check_final_acceptance*' -or \$_.CommandLine -like '*_chain_i2v*' -or \$_.CommandLine -like '*ComfyUI*' -or \$_.CommandLine -like '*build_case_bgm*') -and \$_.CommandLine -notlike '*Win32_Process*' -and \$_.CommandLine -notlike '*shell-snapshots*' -and \$_.CommandLine -notlike '*--help*' -and \$_.CommandLine -notlike '*--version*' -and ((Get-Date) - \$_.CreationDate).TotalHours -lt 8 }).Count" \
    2>/dev/null | tr -d '\r ' | head -1
}

wait_idle() {   # three consecutive idle reads, because a finisher spends minutes between stages
  local streak=0 n
  for i in $(seq 1 960); do
    n=$(busy)
    [ $((i % 20)) -eq 0 ] && echo "[q] heartbeat $(date +%H:%M) busy=$n"
    if [ "${n:-1}" = "0" ]; then
      streak=$((streak + 1))
      [ "$streak" -ge 3 ] && { echo "[q] idle x3 $(date +%H:%M)"; sleep 20; return 0; }
    else
      streak=0
    fi
    sleep 30
  done
  return 1
}

# Is this episode already rendered against the film json on disk? The queue asks this TWICE:
# once to pick a job, and again the instant wait_idle returns. On 2026-08-11 the first ask was
# the only one -- marmet passed it, then waited 3h17m for the GPU, and launched a rebuild of an
# episode that had finished during the wait. 1h35m of GPU, and greene was pushed back by it.
# WAIT FOR THE JOB WE JUST STARTED, NOT FOR THE GPU.
# 2026-08-16, measured: openfields was launched THREE times in eighteen minutes (19:29, 19:42,
# 19:47). `sleep 180; break` hands control back to the loop while the finisher is still in its
# early steps -- [0/7] pre-flight through [4/7] build film.json are python and ffmpeg, so no
# `remotion render` process exists yet and wait_idle correctly reports "idle x3". The job is not
# `already_done` either, because no master exists until step [6/7]. Every guard was working; none
# of them was asking whether THIS episode was already being built. pd_run.sh's own lock did not
# hold it: it cleared its 'render' lock as stale ("Windows pid 8100 is not live") before the
# render had started. Three finishers then wrote the same log and the same film json.
#
# The GPU takes one job at a time regardless, so serialising costs nothing and removes the class.
wait_job() {   # slug -> return when no finisher for this slug is running
  local slug="$1" n
  sleep 60   # pd_run.sh returns after its own 60s liveness read; do not race the process appearing
  while true; do
    # Two traps, both measured here on 2026-08-16:
    #   @(...) forces an array, so .Count is a number even when nothing matches. Without it an
    #   empty result is $null and prints nothing, which reads as "job finished" every time.
    #   The probe MATCHES ITSELF: the query text contains '_finish_episode.sh <slug>', so the
    #   powershell process running it, and the bash -c that spawned it, both satisfy the -like.
    #   It returned 1 with nothing running at all. Excluding the query's own signature fixes it.
    n=$(powershell -NoProfile -Command \
        "@(Get-CimInstance Win32_Process | Where-Object { \$_.CommandLine -like '*_finish_episode.sh $slug *' -and \$_.CommandLine -notlike '*Get-CimInstance*' }).Count" \
        2>/dev/null | tr -d '\r ')
    case "$n" in ''|*[!0-9]*) echo "[q] $slug: process probe returned '$n' -- treating as STILL RUNNING"; n=1 ;; esac
    [ "$n" -eq 0 ] 2>/dev/null && { echo "[q] $slug: finisher exited $(date +%H:%M)"; return 0; }
    sleep 120
  done
}

# 2026-08-23: this answered from mtime against a HARD-CODED v001 master, and it was wrong in
# both directions. Six of the seven live episodes ship as v002, so it was asking about a file
# nobody uses; and mtime says nothing about content, so touching the film json flipped the
# answer. A false "not done" re-rendered two finished, scheduled films (~3 GPU-hours, see the
# JOBS note below). A false "done" is quieter and worse. The manual JOBS_HELD list below exists
# only because of this bug.
#
# It now asks the ship gate own question: does the acceptance receipt sha match a master that
# is actually on disk? Content, not clocks. episode_is_done.py exits 0 done / 1 not / 2 unusable,
# and only exit 0 skips -- an unusable receipt builds rather than silently doing nothing.
already_done() {   # slug num -> true when the accepted film is byte-for-byte on disk
  local slug="$1"
  py -3.11 scripts/episode_is_done.py "$slug" --quiet
  [ $? -eq 0 ]
}

# slug:composition:number, in deadline order. memphis is already scheduled and is not here.
#
# 2026-08-16: trimmed to the three that actually need a render.
#   marmet, greene -- shipped as _final_bgm.v002.mp4. already_done() tests v001 against the film
#     json, and both film jsons were touched on 08-13 AFTER v001 was made, so the test says "not
#     done" and the queue would rebuild two finished, scheduled films. ~3h of GPU for nothing.
#   correa   -- two real_person_likeness plates (C223 cut-0387, AR-5879298 cut-0098) must be
#     replaced before any render; rendering now just bakes them in again.
#   pinto    -- IN. The 1,160-byte pinto_film.json is a placeholder BY DESIGN: its own _placeholder
#     key says step [4/7] runs build_case_film_generic.py against EP68_pinto_filmconfig.v001.json
#     and overwrites it before the render. Nothing to rebuild by hand.
JOBS="openfields:Ep66Openfields:66 ramirez:Ep67Ramirez:67 pinto:Ep68Pinto:68 hyatt:Ep69Hyatt:69"
JOBS_HELD="marmet:Ep65Marmet:65 greene:Ep62Greene:62 correa:Ep63Correa:63"

while true; do
  started=0
  for job in $JOBS; do
    slug="${job%%:*}"; rest="${job#*:}"; comp="${rest%%:*}"; num="${rest##*:}"
    # already rendered against the current film json? then it is not this queue's problem
    already_done "$slug" "$num" && continue
    py -3.11 scripts/check_episode_inputs.py --slug "$slug" --no-forecast >/dev/null 2>&1 || continue
    # A wait that times out must NOT kill the queue. On 2026-08-11 a hung `remotion render
    # --help` held the busy detector at 12 for 545 minutes; had the window expired, `exit 1` would
    # have taken the queue down with it and nothing would have rendered until a human looked.
    wait_idle || { echo "[q] $slug: still busy after the whole wait window -- looping, NOT exiting"; continue; }
    # The wait above can last hours, and the thing it was waiting FOR may have been this very
    # episode. Freshness is re-read here, after the wait, against the same test that selected
    # the job -- never once, before it.
    already_done "$slug" "$num" && { echo "[q] $slug: completed while this job waited for the GPU -- skipping (stale pick)"; continue; }
    echo "[q] === $slug $(date +%H:%M) ==="
    bash scripts/pd_run.sh --name "auto-$slug" \
        --smoke "py -3.11 scripts/check_episode_inputs.py --slug $slug --no-forecast" \
        -- bash "$SNAP/_finish_episode.sh" "$slug" "$comp" "$num" --allow-video-diversity-deviation \
      && { echo "[q] $slug started $(date +%H:%M)"; started=1; wait_job "$slug"; break; } \
      || echo "[q] $slug refused -- next"
  done
  [ "$started" = "0" ] && { echo "[q] nothing ready $(date +%H:%M) -- waiting 10 min"; sleep 600; }
done
