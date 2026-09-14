#!/usr/bin/env python3
"""One-shot fix for the 3 real acceptance defects on EP34 rolin (runtime_band is the
owner-approved deviation and is NOT touched):

  1. images_present / animation_density: the body cuts end at 1120.36s but narration runs
     to 1128.265s -> a ~7.9s BLACK tail (also the single >3s near-still hold). FIX: append
     two bright, moving footage cuts (returned-cash theme) to cover the gap.
  2. image_cut_luma: 20/160 hero-image cuts render < YAVG 45 (12.5% > 12%) incl. a 5-cut
     dark run (night-highway seq). FIX: gamma-lift the 14 distinct dark SOURCE color PNGs
     (depth maps untouched). Sizing per measured darkness; highlights preserved (gamma).

Backs up originals; idempotent-ish (re-run restores from backup first). No network/paid API.
After this: re-bundle -> re-render -> re-mux -> re-accept.
"""
from __future__ import annotations
import json, math, shutil
from pathlib import Path
from PIL import Image

ROOT = Path(r"C:\Users\aab15\Documents\prime-documentary")
FILM = ROOT / "remotion" / "src" / "data" / "rolin_film.json"
IMGDIR = ROOT / "remotion" / "public" / "rolin" / "img"
BAK_IMG = IMGDIR / "_orig_dark"

# --- 1) film.json tail fill ------------------------------------------------------------
d = json.loads(FILM.read_text(encoding="utf-8"))
shutil.copy2(FILM, FILM.with_suffix(".json.prefix_bak"))
cuts = d["cuts"]
last_end = max(c["start"] + c["dur"] for c in cuts)     # 1120.36
narr = d["narrationSeconds"]                              # 1128.265
gap = narr - last_end
already = any(c.get("seed") in ("rolin-348", "rolin-349") for c in cuts)
if already:
    print("tail cuts already present -- skipping film.json append")
else:
    half = gap / 2.0
    a = {"start": round(last_end, 3), "dur": round(half, 3), "kind": "footage",
         "src": "rolin/factory/AF-BG-28832__stack_of_hundred_dollar_bills.mp4",
         "seed": "rolin-348", "treatment": "footage"}
    b = {"start": round(last_end + half, 3), "dur": round(narr - (last_end + half), 3),
         "kind": "footage", "src": "rolin/factory/AF-BG-23991__money_counting_machine.mp4",
         "seed": "rolin-349", "treatment": "footage"}
    cuts.extend([a, b])
    FILM.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"appended 2 tail cuts covering {last_end:.2f}->{narr:.2f}s (gap {gap:.2f}s): "
          f"{a['dur']}s bills + {b['dur']}s counting-machine")

# --- 2) brighten the 14 distinct dark source images ------------------------------------
# slug -> min rendered YAVG (gate signalstats metric, measured on muxed v001)
DARK = {"S024":37.2,"S055":37.3,"S006":38.3,"S054":40.2,"S034":40.7,"S062":41.2,
        "S027":41.4,"S061":41.7,"S052":41.8,"S019":42.9,"S032":43.0,"S065":43.2,
        "S033":44.0,"S042":44.5}
TARGET = 53.0  # aim rendered ~53 (comfortable margin over the 45 floor)
BAK_IMG.mkdir(exist_ok=True)

def gamma_for(y: float) -> float:
    # multiplicative lift at mid-gray = TARGET/y == 2**(1-g)  ->  g = 1 - log2(TARGET/y)
    g = 1.0 - math.log2(TARGET / y)
    return max(0.50, min(0.85, g))

for slug, y in DARK.items():
    fn = f"PD-2026-034-{slug}-IMG-001.png"
    src = IMGDIR / fn
    bak = BAK_IMG / fn
    if not bak.exists():
        shutil.copy2(src, bak)          # preserve original once
    im = Image.open(bak).convert("RGB")  # always lift from the ORIGINAL (idempotent)
    g = gamma_for(y)
    lut = [min(255, round(255 * (i / 255.0) ** g)) for i in range(256)]
    im2 = im.point(lut * 3)
    im2.save(src)
    print(f"  {slug}: YAVG {y:.1f} -> gamma {g:.3f} (mid-lift x{2**(1-g):.2f})")

print("DONE. Next: re-bundle -> re-render -> re-mux -> re-accept.")
