#!/bin/bash
# Take EP62-65 from "rendered" to "has a green receipt", one job at a time, all night.
#
# Replaces queue_memphis_marmet.sh, which only queued the two remaining renders and so left no
# window for the acceptance scans. An acceptance scan reads a whole 1.8 GB master; that is the
# same disk load that killed three renders earlier today, so it can never overlap one. Ordering
# the short job first in each idle window costs nothing and gets EP62 -- the one the owner has
# already approved -- its receipt hours earlier than it would otherwise.
#
# Order:
#   1. greene  acceptance   (its render finished 17:12; owner approved the film)
#   2. memphis render       (film.json rebuilt 15:38, master on disk predates it -> stale)
#   3. correa  acceptance   (render finishing now)
#   4. marmet  render       (film.json 15:38, master 10:13 -> stale)
#   5. memphis acceptance
#   6. marmet  acceptance
#
# Idleness is asked of WMI, which carries the full command line. `ps -W` prints only the
# interpreter path, so counting "_finish_episode" there returns 0 while one is plainly running --
# a guard that can never fire, which is how the previous queue launched memphis on top of correa.
# Three consecutive idle reads 30s apart are required, because _finish_episode.sh spends whole
# minutes between stages with no remotion process alive at all.
set -u
cd /c/Users/aab15/Documents/prime-documentary
export PATH="/usr/bin:/bin:$PATH"

idle_once() {
  local n
  n=$(powershell -NoProfile -Command \
    "@(Get-CimInstance Win32_Process | Where-Object { (\$_.CommandLine -like '*remotion*render*' -or \$_.CommandLine -like '*_finish_episode.sh*' -or \$_.CommandLine -like '*check_final_acceptance*') -and \$_.CommandLine -notlike '*Win32_Process*' -and \$_.CommandLine -notlike '*shell-snapshots*' }).Count" \
    2>/dev/null | tr -d '\r ' | head -1)
  [ "${n:-1}" = "0" ]
}

wait_idle() {
  local streak=0
  for _ in $(seq 1 1400); do            # up to ~11.7 hours
    if idle_once; then
      streak=$((streak + 1))
      [ "$streak" -ge 3 ] && { echo "[q] idle x3 $(date +%H:%M)"; sleep 20; return 0; }
    else
      streak=0
    fi
    sleep 30
  done
  echo "[q] gave up waiting for an idle machine" >&2
  return 1
}

accept() {   # slug, episode-id, episode-number
  # The tool documents its positional as "episode number or id"; the slug is not a documented
  # form, so the number is passed. The slug is still needed to locate the master.
  local slug="$1" epid="$2" num="$3"
  local master="episodes/$epid/08_edit/${slug}_final_bgm.v001.mp4"
  [ -f "$master" ] || master="out/${slug}.mp4"
  if [ ! -f "$master" ]; then
    echo "[q] $slug: no master to measure ($master) -- skipping acceptance" >&2
    return 0
  fi
  echo "[q] === accept $slug $(date +%H:%M) -> $master ==="
  py -3.11 scripts/check_final_acceptance.py "$num" --render "$master" --emit-receipt \
      > "out_accept_${slug}.log" 2>&1
  echo "[q] accept $slug exit=$? $(date +%H:%M) (see out_accept_${slug}.log)"
}

render() {   # slug, composition, number
  echo "[q] === render $1 $(date +%H:%M) ==="
  bash scripts/pd_run.sh --name "refinish-$1" \
      --smoke "py -3.11 scripts/check_episode_inputs.py --slug $1" \
      -- bash scripts/_finish_episode.sh "$1" "$2" "$3" --allow-video-diversity-deviation \
    || { echo "[q] $1 refused to start" >&2; return 1; }
  sleep 120                              # clear the launch before the idle test resumes
}

wait_idle && accept greene  PD-2026-062-greene  62
wait_idle && render memphis Ep64Memphis 64
wait_idle && accept correa  PD-2026-063-correa  63
wait_idle && render marmet  Ep65Marmet 65
wait_idle && accept memphis PD-2026-064-memphis 64
wait_idle && accept marmet  PD-2026-065-marmet  65

echo "[q] all six jobs attempted $(date +%H:%M)"
