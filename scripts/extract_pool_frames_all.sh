#!/bin/bash
# Extract pool contact sheets for the four episodes that cannot build without them.
#
# The gate added tonight refuses a build when a pool has no `pool_frame_review`. It exists because
# EP62 greene shipped a modern US election ballot and a Range Rover into a 1975 Louisville film:
# both passed the t=1s pool sheet, both were only caught by opening the RENDERED master's 78 sheets
# after four hours of rendering. This moves that same look to before the build.
#
# Serial on purpose. Four concurrent ffmpeg sweeps over H: is the disk load that killed three
# renders today, and nothing here is urgent enough to risk the next one.
set -u
cd /c/Users/aab15/Documents/prime-documentary
export PATH="/usr/bin:/bin:$PATH"
for slug in memphis marmet greene correa; do
  echo "[frames] === $slug $(date +%H:%M) ==="
  py -3.11 scripts/check_pool_frames.py --slug "$slug" --sheets-only --jobs 4 \
      > "out_poolframes_${slug}.log" 2>&1
  echo "[frames] $slug exit=$? $(date +%H:%M)  $(tail -1 out_poolframes_${slug}.log | cut -c1-100)"
done
echo "[frames] all four extracted $(date +%H:%M) -- sheets now need human eyes"
