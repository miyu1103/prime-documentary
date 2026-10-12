#!/bin/bash
# Render memphis, then marmet, each one only after the machine is genuinely idle.
#
# This replaces run_queue_64_65.sh, whose idle test was wrong in a way that cost a render today.
# It asked only whether a `remotion render` process existed. _finish_episode.sh spends its middle
# stages rebuilding manifests and hardlinking a slim public dir, and during those minutes no
# remotion process exists at all -- so the queue read "free", launched memphis on top of a correa
# that was very much still working, and both had to be killed.
#
# Three things are different here:
#   * idleness means no remotion render AND no _finish_episode.sh shell, not one of the two;
#   * it must hold for three consecutive checks 30s apart, so a gap between stages cannot be
#     mistaken for the end of a job;
#   * the launch goes through pd_run.sh, which takes the render lock and reads the log 60s in.
#
# Both films are already built: their film.json files were rebuilt at 15:38 today with the archive
# footage in them, and both masters on disk predate that, so both are stale and must be re-rendered.
set -u
cd /c/Users/aab15/Documents/prime-documentary
export PATH="/usr/bin:/bin:$PATH"

# `ps -W` prints only the interpreter path, never the script it is running, so counting
# "_finish_episode" there returns 0 while one is plainly running -- a guard that can never fire.
# WMI does carry the full command line, so both halves are asked of WMI in one call.
idle_once() {
  local n
  n=$(powershell -NoProfile -Command \
    "@(Get-CimInstance Win32_Process | Where-Object { (\$_.CommandLine -like '*remotion*render*' -or \$_.CommandLine -like '*_finish_episode.sh*') -and \$_.CommandLine -notlike '*Win32_Process*' -and \$_.CommandLine -notlike '*shell-snapshots*' }).Count" \
    2>/dev/null | tr -d '\r ' | head -1)
  [ "${n:-1}" = "0" ]
}

wait_idle() {
  local streak=0
  for _ in $(seq 1 1200); do            # up to 10 hours
    if idle_once; then
      streak=$((streak + 1))
      if [ "$streak" -ge 3 ]; then
        echo "[queue] idle confirmed 3x $(date +%H:%M)"
        sleep 20
        return 0
      fi
    else
      streak=0
    fi
    sleep 30
  done
  echo "[queue] gave up waiting for an idle machine" >&2
  return 1
}

for job in "memphis:Ep64Memphis:64" "marmet:Ep65Marmet:65"; do
  slug="${job%%:*}"; rest="${job#*:}"; comp="${rest%%:*}"; num="${rest##*:}"
  wait_idle || exit 1
  echo "[queue] === $slug $(date +%H:%M) ==="
  bash scripts/pd_run.sh --name "refinish-$slug" \
      --smoke "py -3.11 scripts/check_episode_inputs.py --slug $slug" \
      -- bash scripts/_finish_episode.sh "$slug" "$comp" "$num" --allow-video-diversity-deviation \
    || { echo "[queue] $slug refused to start -- stopping the queue" >&2; exit 1; }
  sleep 120                              # let it get past the launch before the idle test resumes
done

wait_idle && echo "[queue] memphis and marmet both finished $(date +%H:%M)"
