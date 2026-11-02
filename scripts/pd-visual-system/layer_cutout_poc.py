#!/usr/bin/env python
"""PD Visual System — P08 2.5D layer cutout (depth-threshold, no-warp).

Splits a hero image into a feathered FOREGROUND cutout (RGBA) and an inpainted
BACKGROUND plate using the Depth-Anything-V2 depth map. These two flat layers feed
the existing Parallax.tsx (rigid translate+scale per layer) → dimensional motion
with NO mesh warping of thin structures (the DepthStill failure mode, P08_FINDING).

Uses the depth map as a robust fg/bg separator (SAM2 box-refinement is a later
precision upgrade). Run in an env with cv2 + numpy.
"""
from __future__ import annotations
import argparse, sys
from pathlib import Path
import numpy as np
import cv2


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--image", required=True)
    ap.add_argument("--depth", default=None, help="default <image>_depth.png")
    ap.add_argument("--outdir", required=True)
    ap.add_argument("--threshold", type=float, default=0.34, help="0..1 depth cut (nearer=bright)")
    ap.add_argument("--feather", type=int, default=25, help="mask feather px (odd)")
    a = ap.parse_args()
    img_p = Path(a.image)
    depth_p = Path(a.depth) if a.depth else img_p.with_name(img_p.stem + "_depth.png")
    if not img_p.exists() or not depth_p.exists():
        print(f"missing image/depth: {img_p} / {depth_p}", file=sys.stderr); return 2
    outdir = Path(a.outdir); outdir.mkdir(parents=True, exist_ok=True)

    img = cv2.imread(str(img_p), cv2.IMREAD_COLOR)               # BGR
    depth = cv2.imread(str(depth_p), cv2.IMREAD_GRAYSCALE)       # 0..255
    depth = cv2.resize(depth, (img.shape[1], img.shape[0]), interpolation=cv2.INTER_LINEAR)

    # foreground = near (bright) region
    thr = int(a.threshold * 255)
    hard = (depth >= thr).astype(np.uint8) * 255
    # clean specks + close gaps so thin chains stay attached
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
    hard = cv2.morphologyEx(hard, cv2.MORPH_CLOSE, k, iterations=2)
    hard = cv2.morphologyEx(hard, cv2.MORPH_OPEN, k, iterations=1)

    f = a.feather | 1
    alpha = cv2.GaussianBlur(hard, (f, f), 0)                    # feathered edge

    # FG cutout (BGRA)
    fg = np.dstack([img, alpha])
    cv2.imwrite(str(outdir / (img_p.stem + "_fg.png")), fg)

    # BG plate: inpaint the fg region so no hole shows behind the parallax move
    dil = cv2.dilate(hard, k, iterations=3)
    bg = cv2.inpaint(img, dil, 10, cv2.INPAINT_TELEA)
    cv2.imwrite(str(outdir / (img_p.stem + "_bg.png")), bg)

    cover = float((hard > 0).mean())
    print(f"wrote {img_p.stem}_fg.png + _bg.png to {outdir}  fg_coverage={cover:.2%} size={img.shape[1]}x{img.shape[0]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
