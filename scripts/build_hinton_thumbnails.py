#!/usr/bin/env python3
r"""EP29 hinton — render the 3 thumbnail variants + select one (thumbnail_ready gate).

Prereq: Codex bespoke backgrounds staged as
  remotion/public/hinton/thumb/bg1.png  (death-row door + gold shaft)
  remotion/public/hinton/thumb/bg2.png  (bullet macro + shattered "match")
  remotion/public/hinton/thumb/bg3.png  (cell through bars + shadow figure)
(see episodes/PD-2026-029-hinton/10_thumbnail/CODEX_BACKGROUNDS.md).

Renders the registered Still comps Thumb-hinton-{A,B,C} (ThumbnailFrame, 1280x720)
into 10_thumbnail/ and copies the chosen one to 09_package/thumbnail.selected.png so
check_final_acceptance thumbnail_ready + thumbnail_visibility pass.

Usage:  py -3.11 scripts/build_hinton_thumbnails.py [--select A|B|C]
"""
from __future__ import annotations
import argparse, shutil, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-029-hinton"
PUB = ROOT / "remotion" / "public" / "hinton" / "thumb"
THUMB = ROOT / "episodes" / EP / "10_thumbnail"
PKG = ROOT / "episodes" / EP / "09_package"
VARIANTS = {"A": "Thumb-hinton-A", "B": "Thumb-hinton-B", "C": "Thumb-hinton-C"}


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--select", default="A", choices=list(VARIANTS))
    args = ap.parse_args()

    missing = [f"bg{i}.png" for i in (1, 2, 3) if not (PUB / f"bg{i}.png").exists()]
    if missing:
        print(f"BLOCKED: stage the Codex backgrounds first: {missing} -> {PUB}")
        print("See episodes/%s/10_thumbnail/CODEX_BACKGROUNDS.md" % EP)
        return 2

    THUMB.mkdir(parents=True, exist_ok=True)
    PKG.mkdir(parents=True, exist_ok=True)
    for k, comp in VARIANTS.items():
        out = THUMB / f"thumbnail_{k}.png"
        subprocess.run(["npx", "remotion", "still", comp, str(out)],
                       cwd=str(ROOT / "remotion"), check=True, shell=True)
        # noir Codex backgrounds render dark; lift brightness/contrast so the thumbnail
        # clears the visibility gate (mean luma >= 33, std >= 40 = punchy/high-CTR at 320px).
        from PIL import Image, ImageEnhance
        im = Image.open(out).convert("RGB")
        im = ImageEnhance.Brightness(im).enhance(1.72)   # 派手: bright/loud
        im = ImageEnhance.Contrast(im).enhance(1.34)     # punchy contrast
        im = ImageEnhance.Color(im).enhance(1.5)         # vivid accent
        im = ImageEnhance.Sharpness(im).enhance(1.3)     # crisp at 320px
        im.save(out)
        print("rendered+graded", out.name)
    shutil.copy2(THUMB / f"thumbnail_{args.select}.png", PKG / "thumbnail.selected.png")
    print(f"selected {args.select} -> 09_package/thumbnail.selected.png")
    print("now: check_final_acceptance.py 29 --render <final.mp4> --emit-receipt  (expect GREEN)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
