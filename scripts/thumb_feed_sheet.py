#!/usr/bin/env python
"""Show thumbnail plates at the size a viewer actually sees them: 168x94.

WHY. On 2026-08-23 a plate was called the strongest in an order because, at full resolution,
the object stated the contradiction with no caption -- a wire held short of its terminal clamp
by a band of labelling. Shrunk to feed size the gap vanishes and it reads as "a machine part".
The order's own rule said to shrink it and look, and until this script existed nobody did.

`check_thumb_punch.py` measures light and colour. It cannot measure meaning. This is the other
half: a contact sheet at true feed size, magnified with NEAREST so the pixels a viewer gets are
the pixels you judge, never smoothed into something clearer than reality.

    py -3.11 scripts/thumb_feed_sheet.py E:\\pd-media\\05_visuals\\thumbs\\keybridge_v2
    py -3.11 scripts/thumb_feed_sheet.py <dir> --out sheet.png --zoom 3

Read it and ask one question per plate: in one second, what is the object and what is wrong
with it. If the answer needs the title, the plate is not carrying its half.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

FEED_W, FEED_H = 168, 94


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("directory", type=Path)
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--zoom", type=int, default=3)
    ap.add_argument("--cols", type=int, default=3)
    a = ap.parse_args()

    from PIL import Image, ImageDraw

    files = sorted(a.directory.glob("*.png")) + sorted(a.directory.glob("*.jpg"))
    if not files:
        print(f"no images in {a.directory}")
        return 1

    pad, label_h = 12, 16
    cols = max(1, min(a.cols, len(files)))
    rows = (len(files) + cols - 1) // cols
    W = cols * FEED_W + (cols + 1) * pad
    H = rows * (FEED_H + label_h) + (rows + 1) * pad
    sheet = Image.new("RGB", (W, H), (30, 30, 30))
    draw = ImageDraw.Draw(sheet)

    for i, f in enumerate(files):
        try:
            im = Image.open(f).convert("RGB").resize((FEED_W, FEED_H), Image.LANCZOS)
        except Exception as exc:
            print(f"  unreadable {f.name}: {exc}")
            continue
        c, r = i % cols, i // cols
        x = pad + c * (FEED_W + pad)
        y = pad + r * (FEED_H + label_h + pad)
        sheet.paste(im, (x, y))
        draw.text((x, y + FEED_H + 2), f.stem, fill=(200, 200, 200))

    # NEAREST on purpose: magnify the feed-size pixels, do not invent detail
    sheet = sheet.resize((W * a.zoom, H * a.zoom), Image.NEAREST)
    out = a.out or (a.directory / "_feed_sheet.png")
    sheet.save(out)
    print(f"{len(files)} plate(s) at {FEED_W}x{FEED_H}, magnified {a.zoom}x -> {out}")
    print("Now look. One second per plate: what is the object, and what is wrong with it.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
