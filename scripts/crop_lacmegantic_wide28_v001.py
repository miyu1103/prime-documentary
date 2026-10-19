#!/usr/bin/env python3
r"""The 28 EP72 plates that came back 1881x836 (2.25:1) instead of 16:9.

WHY THIS EXISTS
The 2026-08-21 delivery of EP72's 120 plates is not one shape: 92 are 1672x941 (16:9, handled by
`upscale_lacmegantic_4k_esrgan_v001.py`) and 28 are 1881x836, which is 2.25:1. A 2.25:1 frame
cannot become 16:9 without a decision:

  - letterbox   -> rejected. This film has no black bars.
  - stretch     -> rejected. It distorts every subject.
  - re-order    -> Codex returns the shape it returns; there is no reason to expect 16:9 next time.
  - CROP        -> chosen. 1881x836 keeps a 1486x836 window; the question is only WHERE.

WHERE THE WINDOW GOES, AND WHY IT IS NOT ALWAYS THE CENTRE
A centre crop is right for most of these frames and wrong for the few whose subject sits at an edge
-- checked by eye on 2026-08-21 against contact sheets in runs/qc/lacmegantic_wide28: L015's gloved
hand is at the right edge, L036's brake wheel runs off the right, L070's gauge is at the left. So
the window is chosen by MEASUREMENT, not by assumption: slide the 16:9 window across the frame and
keep the position with the most image energy (mean gradient magnitude). Empty sky, dark forest and
flat wet asphalt score low; a wheel, a hand, a gauge, a lit street score high.

The chosen offset is PRINTED for every plate so a human can see which ones moved and check those.

    ./.venv/Scripts/python.exe scripts/crop_lacmegantic_wide28_v001.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

SRC = Path(r"E:\pd-media\assets\ai\lacmegantic\_v001_raw")
DST = Path(r"E:\pd-media\assets\ai\lacmegantic\_v002_cropped169")
RATIO_TOL = 0.05
STEP = 8


def energy_map(im: Image.Image) -> np.ndarray:
    g = np.asarray(im.convert("L"), dtype="float32")
    gx = np.abs(np.diff(g, axis=1, prepend=g[:, :1]))
    gy = np.abs(np.diff(g, axis=0, prepend=g[:1, :]))
    return gx + gy


def best_left(im: Image.Image, keep_w: int) -> tuple[int, str]:
    e = energy_map(im)
    w = im.size[0]
    centre = (w - keep_w) // 2
    best, best_score = centre, -1.0
    for left in range(0, w - keep_w + 1, STEP):
        score = float(e[:, left:left + keep_w].mean())
        if score > best_score:
            best, best_score = left, score
    # only move off centre when it is a real difference, so most frames stay centred
    c_score = float(e[:, centre:centre + keep_w].mean())
    if best_score < c_score * 1.02:
        return centre, "centre"
    return best, f"offset {best - centre:+d}px"


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    todo = []
    for p in sorted(SRC.glob("*.png")):
        w, h = Image.open(p).size
        if abs(w / h - 16 / 9) > RATIO_TOL:
            todo.append(p)
    print(f"{len(todo)} non-16:9 plates to crop")
    DST.mkdir(parents=True, exist_ok=True)

    moved = []
    for p in todo:
        im = Image.open(p).convert("RGB")
        w, h = im.size
        keep_w = int(round(h * 16 / 9))
        left, how = best_left(im, keep_w)
        out = im.crop((left, 0, left + keep_w, h))
        out.save(DST / p.name, "PNG")
        print(f"  {p.name}  {w}x{h} -> {out.size[0]}x{out.size[1]}   {how}")
        if how != "centre":
            moved.append(p.name)

    print(f"\ncropped {len(todo)} -> {DST}")
    print(f"moved off centre ({len(moved)}): {moved}")
    print("NEXT: these are now 16:9 but only ~1486 px wide. Run the ESRGAN pass on this folder to "
          "reach 3840x2160, and EYEBALL the moved ones before accepting them.")
    (DST / "_crop_report.json").write_text(
        json.dumps({"cropped": [p.name for p in todo], "moved_off_centre": moved}, indent=1),
        encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
