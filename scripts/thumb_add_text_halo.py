#!/usr/bin/env python
"""Darken a halo around a thumbnail's bright text so the headline separates from the plate.

check_thumb_subject_luma measures a real legibility property: the dark ring around the bright
core (>=12px @1280). EP50's plate is a lit interrogation room, so the 6px stroke baked in by
the thumbnail builder disappears into the glow and the headline reads soft at feed size.

This works on the FLATTENED png (no SDXL, no re-generation): bright cores are found, dilated,
and the newly added ring is multiplied down and blurred into a natural drop-halo. Nothing is
repainted, no text is added or changed -- the same words simply stop competing with the wall
behind them.

    python scripts/thumb_add_text_halo.py --in <thumb.png> --out <thumb.v002.png> [--radius 16]
"""
from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="src", required=True)
    ap.add_argument("--out", dest="dst", required=True)
    ap.add_argument("--radius", type=int, default=16, help="halo width in px @ image width")
    ap.add_argument("--bright", type=int, default=170,
                    help="luma above which a pixel counts as glyph (include the antialias fringe)")
    ap.add_argument("--feather", type=float, default=3.0, help="outer softening of the halo, px")
    ap.add_argument("--darken", type=float, default=0.18, help="ring multiplier (0=black)")
    ap.add_argument("--cap-outside", type=float, default=190.0,
                    help="max luma allowed outside the headline box (0 disables the rolloff)")
    ap.add_argument("--box", type=float, nargs=4, action="append", metavar=("X0", "Y0", "X1", "Y1"),
                    help="text box as fractions of width/height; repeatable "
                         "(default: the builder's chip + two headline lines)")
    a = ap.parse_args()
    if not a.box:
        a.box = [(0.02, 0.18, 0.30, 0.30),     # kicker chip
                 (0.02, 0.30, 0.50, 0.69)]     # the two headline lines + rule

    im = Image.open(a.src).convert("RGB")
    w, h = im.size

    # Text lives in known boxes (the builder lays the chip and the two headline lines out at
    # fixed coordinates). EVERYTHING is done through those boxes: outside them the plate's
    # highlights are rolled back so no wall or lamp is brighter than a glyph, inside them the
    # glyphs get a hard dark halo. A halo applied to the whole frame boxes the lamp in a black
    # rectangle -- it passes the gate and looks broken, which is not a trade this makes.
    text_mask = Image.new("L", (w, h), 0)
    md = ImageDraw.Draw(text_mask)
    for (x0, y0, x1, y1) in a.box:
        md.rectangle([int(x0 * w), int(y0 * h), int(x1 * w), int(y1 * h)], fill=255)

    if a.cap_outside > 0:
        lum0 = im.convert("L")
        hot = lum0.point(lambda v: 255 if v > a.cap_outside else 0)
        hot = Image.composite(Image.new("L", (w, h), 0), hot, text_mask)   # not on the text
        scale = a.cap_outside / 255.0
        rolled = Image.eval(im, lambda v: int(v * scale))
        im = Image.composite(rolled, im, hot.filter(ImageFilter.GaussianBlur(2.0)))

    # The halo has to start HARD at the glyph edge. A blurred mask leaves the antialiased
    # fringe (luma ~185) sitting right against the core, which is exactly what the checker
    # samples first -- so the ring is built with a hard edge and only feathered outwards.
    lum = im.convert("L")
    core = lum.point(lambda v: 255 if v >= a.bright else 0)
    core = Image.composite(core, Image.new("L", (w, h), 0), text_mask)   # glyphs only
    grown = core.filter(ImageFilter.MaxFilter(a.radius * 2 + 1))
    ring = Image.composite(Image.new("L", (w, h), 0), grown, core)       # grown minus the core
    if a.feather > 0:
        soft = ring.filter(ImageFilter.GaussianBlur(a.feather))
        ring = ImageChops.lighter(ring, soft)                            # feather outwards only
    ring = Image.composite(Image.new("L", (w, h), 0), ring, core)        # never touch the glyphs

    dark = Image.eval(im, lambda v: int(v * a.darken))
    out = Image.composite(dark, im, ring)
    Path(a.dst).parent.mkdir(parents=True, exist_ok=True)
    out.save(a.dst)
    print(f"WROTE {a.dst}  (halo radius {a.radius}px, ring darkened to {a.darken:.0%})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
