#!/bin/bash
# Render memphis then marmet, one at a time, after whatever is rendering now has finished.
#
# Started because the owner asked for EP64 and EP65 as well, and because starting each render by
# hand is how two heavy jobs ended up on the same disk twice today. Three renders died that way
# earlier: no error line in the log, just a process that stopped. The rule this encodes is simply
# that a render never begins while another is running.
#
# It also holds off the acceptance scans. A full-length scan reads the whole master and is exactly
# the kind of disk load that kills a render; they are queued behind every render instead.
set -u
cd /c/Users/aab15/Documents/prime-documentary

busy() {
  powershell -NoProfile -Command \
    "@(Get-CimInstance Win32_Process | Where-Object { \$_.CommandLine -like '*remotion*render*' -and \$_.CommandLine -notlike '*Win32_Process*' }).Count" 2>/dev/null | tr -d '\r ' | head -1
}

wait_for_free() {
  local n
  for _ in $(seq 1 720); do          # up to 6 hours
    n=$(busy)
    [ "${n:-1}" = "0" ] && { echo "[queue] gpu free $(date +%H:%M)"; sleep 20; return 0; }
    sleep 30
  done
  echo "[queue] gave up waiting" >&2
  return 1
}

for job in "memphis:Ep64Memphis:64" "marmet:Ep65Marmet:65"; do
  slug="${job%%:*}"; rest="${job#*:}"; comp="${rest%%:*}"; num="${rest##*:}"
  wait_for_free || exit 1
  echo "[queue] === $slug $(date +%H:%M) ==="
  bash scripts/_finish_episode.sh "$slug" "$comp" "$num" --allow-video-diversity-deviation \
      > "out_refinish_${slug}.log" 2>&1 \
    && echo "[queue] $slug OK $(date +%H:%M)" \
    || echo "[queue] $slug FAILED -- see out_finish_${slug}.log"
done

echo "[queue] renders done $(date +%H:%M) -- acceptance scans can start now"
