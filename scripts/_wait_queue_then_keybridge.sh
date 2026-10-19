#!/usr/bin/env bash
# Run EP77 keybridge the moment the four-episode queue finishes, so the card never idles.
#
# The queue writes out_render_queue.log and ends with the line "QUEUE DONE". Waiting on that
# string is more honest than waiting on a pid: a pid tells you a process exists, not that the
# work it was doing finished. Three regeneration runs today reported success and did nothing.
set -uo pipefail
cd "$(dirname "$0")/.." || exit 1
while ! grep -q "QUEUE DONE" out_render_queue.log 2>/dev/null; do sleep 120; done
echo "$(date '+%m-%d %H:%M:%S') queue finished; starting keybridge"
bash scripts/_render_keybridge_after.sh
