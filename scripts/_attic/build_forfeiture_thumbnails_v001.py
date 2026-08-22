#!/usr/bin/env python3
r"""EP28 forfeiture CTR thumbnails (3 options + selected) using the v002 visual system.

Reuses build_case_thumbnails_v002.render (bright hero + focal glow + RED kicker tag + XL
black-stroked headline + gold accent + PD mark). Writes 3 options to 10_thumbnail and copies
the selected to 09_package/thumbnail.selected.v002.png (thumbnail_ready + thumbnail_visibility).

    py -3.11 scripts/build_forfeiture_thumbnails_v001.py
"""
from __future__ import annotations
import shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build_case_thumbnails_v002 import render  # bright hero + red tag + XL stroke text

EP = ROOT / "episodes" / "PD-2026-028-forfeiture"
OUTDIR = EP / "10_thumbnail"
IMG = "remotion/public/forfeiture/img"

# (hero, focus cx/cy 0..1, kicker, line1 white, line2 gold)
OPTIONS = [
    (f"{IMG}/PD-2026-028-S005-IMG-001.png", (0.42, 0.40), "NO CRIME. NO CONVICTION.", "THEY TOOK", "THE HOUSE"),
    (f"{IMG}/PD-2026-028-S032-IMG-001.png", (0.55, 0.50), "NO CHARGE FILED", "THEY CAN TAKE", "YOUR HOUSE"),
    (f"{IMG}/PD-2026-028-S033-IMG-001.png", (0.42, 0.55), "OVER $40 OF DRUGS", "THEY SEIZED", "A FAMILY'S HOME"),
]
SELECTED = 0


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    OUTDIR.mkdir(parents=True, exist_ok=True)
    made = []
    for i, (hero, focus, kicker, l1, l2) in enumerate(OPTIONS, start=1):
        cfg = {"hero": hero, "focus": focus, "kicker": kicker, "line1": l1, "line2": l2}
        out = OUTDIR / f"thumbnail_option_{i:02d}.v002.png"
        render(cfg, out)
        made.append(out)
        print(f"  option {i}: {out.name}  ({kicker} / {l1} {l2})")
    sel = OUTDIR / "thumbnail_ctr.v002.png"
    shutil.copy2(made[SELECTED], sel)
    pkg = EP / "09_package"; pkg.mkdir(parents=True, exist_ok=True)
    shutil.copy2(made[SELECTED], pkg / "thumbnail.selected.v002.png")
    print(f"selected -> option {SELECTED+1} + 09_package/thumbnail.selected.v002.png")
    print(f"[forfeiture] {len(made)} options @ 1280x720, selected=YES")


if __name__ == "__main__":
    main()
