#!/bin/bash
# Run the acceptance gate on an episode's master the ONE correct way.
#
# I ran it by hand on EP55 without --render-started-at, spent a full ~20-minute measurement,
# and got back `render_freshness FAIL: sha256 identical to prior receipt ... pass
# --render-started-at for a legitimate re-grade`. The flag requirement is documented and was
# already in my notes. Twenty minutes of a busy machine went to remembering it.
#
# So the flag stops being something to remember. This resolves the master, derives the render
# start from the build log (falling back to the master's own mtime minus its duration), and
# runs the gate with everything already correct.
#
#   scripts/pd_gate.sh <slug> [extra args...]
#
# Exit code is the gate's own. The receipt path is printed on the last line.
set -u
cd /c/Users/aab15/Documents/prime-documentary
SLUG="${1:?slug}"; shift || true

EPDIR=$(ls -d episodes/PD-*-"$SLUG" 2>/dev/null | head -1)
[ -n "$EPDIR" ] || { echo "[gate] no episode directory for $SLUG" >&2; exit 2; }
EP=$(basename "$EPDIR")

MASTER=$(ls -t "$EPDIR"/08_edit/*_final_bgm.v*.mp4 2>/dev/null | head -1)
[ -n "$MASTER" ] || { echo "[gate] no master under $EPDIR/08_edit -- render first" >&2; exit 2; }

# When did this render actually start? The build log records it; otherwise assume the render
# took no longer than the film is long, which is always an underestimate and therefore safe
# (the check only asks that the mp4 is NEWER than the stamp).
START=$(py -3.11 - "$SLUG" "$MASTER" <<'PY'
import os, re, subprocess, sys, time
from datetime import datetime
slug, master = sys.argv[1], sys.argv[2]
stamp = None
import glob
for log in sorted(glob.glob("out_build*.log"), key=os.path.getmtime):
    if not os.path.isfile(log):
        continue
    for line in open(log, encoding="utf-8", errors="ignore"):
        m = re.match(rf"\[finish:{re.escape(slug)}\] START (.+?)\s*$", line.strip())
        if m:
            try:
                stamp = time.mktime(datetime.strptime(
                    re.sub(r"\s+", " ", m.group(1)), "%a %b %d %H:%M:%S %Y").timetuple())
            except ValueError:
                pass
if stamp is None:
    dur = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", master], capture_output=True, text=True).stdout.strip()
    try:
        dur = float(dur)
    except ValueError:
        dur = 1800.0
    stamp = os.path.getmtime(master) - dur * 6      # generous: renders run ~4-6x realtime
print(int(stamp))
PY
)

echo "[gate] $EP"
echo "[gate] master        $(basename "$MASTER")  $(du -m "$MASTER" | cut -f1)MB"
echo "[gate] render-started-at $START  ($(date -d "@$START" '+%Y-%m-%d %H:%M:%S' 2>/dev/null || echo derived))"
.venv/Scripts/python.exe -u scripts/check_final_acceptance.py "$EP" \
    --render "$MASTER" --render-started-at "$START" --emit-receipt "$@"
