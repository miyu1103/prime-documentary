#!/bin/bash
# ONE builder, ever. Two of these on one ComfyUI has now happened twice; the second run silently
# doubles up and the clips it makes are attributed to whichever log you happen to read.
cd /c/Users/aab15/Documents/prime-documentary
LOCK=out_motion.lock
if [ -f "$LOCK" ] && kill -0 "$(cat $LOCK 2>/dev/null)" 2>/dev/null; then
  echo "REFUSED: a motion build is already running (pid $(cat $LOCK))"; exit 1
fi
echo $$ > "$LOCK"
trap 'rm -f "$LOCK"' EXIT
for s in correa memphis marmet; do
  echo "===== $s $(date +%H:%M) ====="
  .venv/Scripts/python.exe scripts/build_motion_from_plates.py --slug "$s" --limit 200
done
echo "===== DONE $(date +%H:%M) ====="
