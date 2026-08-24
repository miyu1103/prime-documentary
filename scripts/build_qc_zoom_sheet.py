#!/usr/bin/env python3
"""Zoomed contact sheet for the plates a 260px tile cannot judge.

260px cannot resolve a face or a logo (EP78: two false face calls; EP79: three real logos
invisible until 420px). This builds one sheet at 440px/tile for the handful of flagged ids.

    py -3.11 scripts/build_qc_zoom_sheet.py --slug station --src E:/pd-media/05_visuals/station/img \
        --out runs/qc/plate_sheets/station/station_zoom_01.png --title "faces + liveries" S006 S037 ...
"""
from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw

CELL_W, COLS, PAD, CAP = 440, 4, 6, 22


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--src", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--title", default="zoom QC")
    ap.add_argument("ids", nargs="+")
    a = ap.parse_args()
    src = Path(a.src)
    tiles = []
    for pid in a.ids:
        p = src / f"{pid}.png"
        if not p.is_file():
            print(f"MISSING {p}")
            continue
        im = Image.open(p).convert("RGB")
        h = round(im.height * CELL_W / im.width)
        tiles.append((pid, im.resize((CELL_W, h), Image.LANCZOS)))
    if not tiles:
        return 1
    cell_h = max(h for _, t in tiles for h in [t.height]) + CAP
    rows = (len(tiles) + COLS - 1) // COLS
    sheet = Image.new("RGB", (COLS * (CELL_W + PAD) + PAD, rows * (cell_h + PAD) + PAD + 28), (12, 12, 12))
    d = ImageDraw.Draw(sheet)
    d.text((PAD, 6), f"{a.slug}  zoom {CELL_W}px  {a.title}", fill=(255, 255, 255))
    for i, (pid, t) in enumerate(tiles):
        x = PAD + (i % COLS) * (CELL_W + PAD)
        y = 28 + PAD + (i // COLS) * (cell_h + PAD)
        sheet.paste(t, (x, y))
        d.text((x + 2, y + t.height + 3), pid, fill=(255, 255, 255))
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out)
    print(f"[ok] {out}  ({len(tiles)} tiles)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
