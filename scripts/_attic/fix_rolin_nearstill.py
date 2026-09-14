#!/usr/bin/env python3
"""Fix the 3 body near-still holds >3s that fail animation_density (single<=3s):
  cut#214 depth S036 (5.8s -> 6.0s hold), cut#172 bleed S016 (3.5s), cut#173 footage
  federal_building (3.5s). Split each into sub-cuts: the hard cut is a motion event that
  breaks the freeze span and each shorter half runs its Ken-Burns/push ~2x faster.
Also re-do S024 at a gentler gamma (QC flagged it as over-lifted / milky) while keeping it
above the image_cut_luma floor. Split highest index first so earlier indices stay valid.
"""
import json, io, math, shutil
from pathlib import Path
from PIL import Image

ROOT = Path(r"C:\Users\aab15\Documents\prime-documentary")
FILM = ROOT / "remotion" / "src" / "data" / "rolin_film.json"
IMGDIR = ROOT / "remotion" / "public" / "rolin" / "img"

d = json.loads(FILM.read_text(encoding="utf-8"))
cuts = d["cuts"]
shutil.copy2(FILM, FILM.with_suffix(".json.nearstill_bak"))

def split(idx, n):
    c = cuts[idx]
    s0, dur = c["start"], c["dur"]
    part = dur / n
    subs = []
    for k in range(n):
        nc = dict(c)
        nc["start"] = round(s0 + k * part, 3)
        nc["dur"] = round(part, 3)
        nc["seed"] = f'{c.get("seed","rolin")}-{chr(97+k)}'
        subs.append(nc)
    cuts[idx:idx+1] = subs
    return len(subs)

# highest index first (214 depth -> 2, 173 footage -> 3 for a slow locked shot, 172 bleed -> 2)
for idx, n in [(214, 2), (173, 3), (172, 2)]:
    c = cuts[idx]
    print(f"split cut#{idx} {c['treatment']} dur {c['dur']:.2f}s -> {n} parts of {c['dur']/n:.2f}s")
    split(idx, n)

FILM.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"cuts now: {len(cuts)}")

# gentler S024 (orig YAVG 26.5): was gamma 0.50 (rendered ~62, milky). Use 0.62 -> source ~44 -> render ~50.
bak = IMGDIR / "_orig_dark" / "PD-2026-034-S024-IMG-001.png"
im = Image.open(bak).convert("RGB")
g = 0.62
lut = [min(255, round(255 * (i / 255.0) ** g)) for i in range(256)]
im.point(lut * 3).save(IMGDIR / "PD-2026-034-S024-IMG-001.png")
print(f"S024 re-brightened gentler gamma {g}")
