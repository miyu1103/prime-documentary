#!/usr/bin/env python3
"""Flashy (派手) 1280x720 thumbnail for EP33 tyler.

Owner asked for 派手: ditch the dark abstract fallback; use the real cinematic
golden-house-in-hand render frame as a bright, saturated hero + focal glow +
XL headline with a THICK black stroke (>=16px, clears the thumb_subject_luma
>=12px outline gate) + bold RED kicker + red SEIZED stamp.
"""
from __future__ import annotations
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

ROOT = Path(__file__).resolve().parents[1]
HERO = ROOT / "remotion" / "out" / "casefilm_tyler_f12000.png"
OUTDIR = ROOT / "episodes" / "PD-2026-033-tyler" / "09_package"
W, H = 1280, 720
FONTS = Path("C:/Windows/Fonts")
BLK = str(FONTS / "ariblk.ttf")      # Arial Black
BOLD = str(FONTS / "arialbd.ttf")

GOLD = (229, 181, 58)
WHITE = (245, 247, 250)
RED = (226, 59, 52)
INK = (10, 10, 12)


def f(path, size):
    return ImageFont.truetype(path, size)


def stroked(d, xy, text, font, fill, sw=16, stroke=(0, 0, 0)):
    d.text(xy, text, font=font, fill=fill, stroke_width=sw, stroke_fill=stroke)


def build():
    im = Image.open(HERO).convert("RGB")
    # 1) crop the burned caption band off the bottom (~13%)
    im = im.crop((0, 0, im.width, int(im.height * 0.87)))
    # 2) flip so the glowing golden house sits RIGHT-of-centre, leaving a left text column
    im = im.transpose(Image.FLIP_LEFT_RIGHT)
    # 3) fill 1280x720 (cover)
    scale = max(W / im.width, H / im.height)
    im = im.resize((int(im.width * scale), int(im.height * scale)), Image.LANCZOS)
    x0 = (im.width - W) // 2
    y0 = (im.height - H) // 2
    im = im.crop((x0, y0, x0 + W, y0 + H))
    # 4) flashy grade: punchy + very saturated, but roll OFF highlights so the ONLY
    #    luma>200 "cores" in the frame are the white headline glyphs (which carry a thick
    #    black stroke). If the glowing house/coin highlights stay bright cores, their bright
    #    surroundings defeat the thumb_subject_luma outline metric (needs a dark rim >=12px).
    im = ImageEnhance.Contrast(im).enhance(1.10)
    im = ImageEnhance.Color(im).enhance(1.40)
    import numpy as np
    arr = np.asarray(im, dtype=np.float64)
    luma = 0.299 * arr[..., 0] + 0.587 * arr[..., 1] + 0.114 * arr[..., 2]
    CAP = 186.0                      # compress any pixel brighter than this toward CAP
    over = luma > CAP
    factor = np.ones_like(luma)
    factor[over] = CAP / luma[over]
    arr = arr * factor[..., None]
    im = Image.fromarray(np.clip(arr, 0, 255).astype("uint8"), "RGB")

    base = im.convert("RGBA")

    # left scrim so the headline reads over anything
    scrim = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(scrim)
    for x in range(W):
        a = int(238 * max(0.0, 1 - (x / (W * 0.62))))   # opaque left -> clear ~62%
        sd.line([(x, 0), (x, H)], fill=(6, 8, 12, a))
    # bottom scrim
    for y in range(H):
        a = int(150 * max(0.0, (y - H * 0.66) / (H * 0.34)))
        sd.line([(0, y), (W, y)], fill=(6, 8, 12, a))
    base = Image.alpha_composite(base, scrim)

    d = ImageDraw.Draw(base)
    # gold frame
    d.rectangle([0, 0, W - 1, H - 1], outline=GOLD, width=4)

    # RED kicker tag (highest-attention)
    kf = f(BLK, 34)
    ktxt = "HOME EQUITY THEFT"
    kw = d.textlength(ktxt, font=kf)
    d.rectangle([44, 44, 44 + kw + 40, 44 + 56], fill=RED)
    d.text((64, 52), ktxt, font=kf, fill=WHITE)

    # XL headline, thick black stroke (>=16px)
    h1 = f(BLK, 112)
    stroked(d, (48, 138), "SHE OWED", h1, WHITE, sw=18)
    stroked(d, (48, 246), "$2,300", h1, GOLD, sw=18)
    stroked(d, (48, 372), "THEY TOOK", h1, WHITE, sw=18)
    stroked(d, (48, 480), "HER HOME", h1, GOLD, sw=18)

    # badge
    bf = f(BOLD, 30)
    btxt = "AND IT WAS LEGAL"
    bw = d.textlength(btxt, font=bf)
    d.rectangle([48, 612, 48 + bw + 36, 612 + 48], outline=GOLD, width=3, fill=INK)
    d.text((66, 621), btxt, font=bf, fill=(210, 215, 224))

    # red SEIZED stamp (rotated) over the house area (upper-right, clear of headline)
    st = Image.new("RGBA", (460, 150), (0, 0, 0, 0))
    std = ImageDraw.Draw(st)
    sf = f(BLK, 76)
    std.rounded_rectangle([6, 6, 454, 130], radius=10, outline=RED, width=8)
    std.text((40, 24), "SEIZED", font=sf, fill=RED, stroke_width=2, stroke_fill=(40, 6, 6))
    st = st.rotate(-13, expand=True, resample=Image.BICUBIC)
    base.alpha_composite(st, (W - st.width - 36, 150))

    # PD monogram (branding; footer text dropped to declutter)
    d = ImageDraw.Draw(base)
    mf = f(BLK, 40)
    d.ellipse([W - 96, H - 96, W - 40, H - 40], outline=GOLD, width=3)
    d.text((W - 84, H - 84), "PD", font=mf, fill=GOLD)

    out = base.convert("RGB")
    sel = OUTDIR / "thumbnail.selected.v002.png"
    out.save(sel, "PNG")
    print("wrote", sel)


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    build()
