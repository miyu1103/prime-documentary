#!/bin/bash
# Report the moment a plate lands below the ordered resolution, instead of after the batch.
#
# EP67 delivered 88 of 104 plates at 1672x941 against an order that states "long edge >= 3840"
# twice, and nobody knew until all 104 were on disk. The size clause now sits in every prompt body
# (EP62's 70 plates all came back at 3840x2160 after that change), but this watches anyway --
# the clause is a request, and the disk is the measurement.
set -u
cd /c/Users/aab15/Documents/prime-documentary
export PATH="/usr/bin:/bin:$PATH"
for _ in $(seq 1 720); do          # ~6 hours at 30s
  py -3.11 - <<'PY'
import sys, time
from pathlib import Path
from PIL import Image
sys.stdout.reconfigure(encoding="utf-8")
state = Path("runs/qc/plate_size_watch.txt")
seen = set(state.read_text(encoding="utf-8").split()) if state.is_file() else set()
new = []
for slug in ("pinto", "hyatt", "ramirez", "greene"):
    d = Path(f"E:/pd-media/assets/ai/{slug}")
    if not d.is_dir():
        continue
    for p in d.glob("*.png"):
        key = f"{slug}/{p.stem}/{p.stat().st_size}"
        if key in seen:
            continue
        try:
            with Image.open(p) as im:
                w, h = im.size
        except Exception:
            continue                        # still being written
        seen.add(key)
        if max(w, h) < 3840:
            new.append(f"{slug} {p.stem} {w}x{h}")
if new:
    print(f"[size] {time.strftime('%H:%M')} UNDERSIZE: " + " | ".join(new[:8])
          + (f"  (+{len(new)-8} more)" if len(new) > 8 else ""))
state.parent.mkdir(parents=True, exist_ok=True)
state.write_text("\n".join(sorted(seen)), encoding="utf-8")
PY
  sleep 30
done
