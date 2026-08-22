#!/usr/bin/env python3
"""Flashy (派手) 1280x720 thumbnail v002 for EP34 rolin.

Owner asked 派手: real cinematic 'his life savings in the bag' hero, punchy+saturated,
LEFT dark scrim for a text column, XL headline with THICK black stroke, the SHOCK number
$82,000 in gold, a red SEIZED stamp, gold kicker. Highlights rolled off (CAP) so the only
luma>200 cores are the stroked headline glyphs (clears thumb_subject_luma outline gate).
Also refreshes thumbnail_02/03 dark siblings are kept; this becomes thumbnail.selected.v002.
"""
from __future__ import annotations
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

ROOT = Path(__file__).resolve().parents[1]
HERO = Path(r"C:/Users/aab15/AppData/Local/Temp/claude/C--Users-aab15/60b7453e-222c-4da5-8717-945d3d348bf0/scratchpad/thumb/hero_60.png")
OUT = ROOT / "episodes" / "PD-2026-034-rolin" / "09_package" / "thumbnail.selected.v002.png"
W, H = 1280, 720
F = Path("C:/Windows/Fonts")
BLK, BOLD = str(F / "ariblk.ttf"), str(F / "arialbd.ttf")
GOLD, WHITE, RED, INK = (233, 184, 56), (247, 249, 252), (222, 46, 40), (8, 9, 12)


def font(p, s): return ImageFont.truetype(p, s)
def stroked(d, xy, t, fnt, fill, sw=16, sc=(0, 0, 0)):
    d.text(xy, t, font=fnt, fill=fill, stroke_width=sw, stroke_fill=sc)


def build():
    im = Image.open(HERO).convert("RGB")
    # crop the burned-caption band off the bottom (~14%) so no subtitle shows through
    im = im.crop((0, 0, im.width, int(im.height * 0.86)))
    # cover-fill 1280x720
    s = max(W / im.width, H / im.height)
    im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
    im = im.crop(((im.width - W) // 2, (im.height - H) // 2, (im.width - W) // 2 + W, (im.height - H) // 2 + H))
    # flashy grade
    im = ImageEnhance.Contrast(im).enhance(1.12)
    im = ImageEnhance.Color(im).enhance(1.38)
    # highlight rolloff so bright cores don't defeat the headline-outline metric
    arr = np.asarray(im, dtype=np.float64)
    luma = 0.299 * arr[..., 0] + 0.587 * arr[..., 1] + 0.114 * arr[..., 2]
    CAP = 188.0
    over = luma > CAP
    fac = np.ones_like(luma); fac[over] = CAP / luma[over]
    arr = np.clip(arr * fac[..., None], 0, 255).astype(np.uint8)
    im = Image.fromarray(arr)
    # left + bottom dark scrim for text legibility
    scrim = Image.new("L", (W, H), 0)
    sd = ImageDraw.Draw(scrim)
    for x in range(W):
        a = max(0, int(215 * (1 - x / (W * 0.62))))
        sd.line([(x, 0), (x, H)], fill=a)
    black = Image.new("RGB", (W, H), INK)
    im = Image.composite(black, im, scrim.point(lambda v: int(v * 0.9)))
    # bottom band
    bb = Image.new("L", (W, H), 0); ImageDraw.Draw(bb).rectangle([0, H - 120, W, H], fill=150)
    im = Image.composite(Image.new("RGB", (W, H), INK), im, bb)

    d = ImageDraw.Draw(im)
    # kicker
    kf = font(BOLD, 40)
    stroked(d, (60, 60), "NO CRIME.  NO CHARGES.", kf, GOLD, sw=6)
    d.line([(64, 116), (515, 116)], fill=GOLD, width=6)
    # headline (stacked, no overlap)
    hf = font(BLK, 84)
    stroked(d, (56, 148), "THEY TOOK HIS", hf, WHITE, sw=14)
    # shock number XL on its own row
    nf = font(BLK, 190)
    stroked(d, (52, 258), "$82,000", nf, GOLD, sw=20)
    # red SEIZED stamp (rotated)
    stamp = Image.new("RGBA", (560, 180), (0, 0, 0, 0))
    st = ImageDraw.Draw(stamp)
    st.rectangle([6, 6, 554, 174], outline=RED, width=10)
    st.text((36, 34), "SEIZED", font=font(BLK, 108), fill=RED)
    stamp = stamp.rotate(-9, expand=True, resample=Image.BICUBIC)
    im.paste(stamp, (700, 470), stamp)
    # brand
    d.text((60, H - 78), "PRIME  DOCUMENTARY", font=font(BOLD, 34), fill=(214, 220, 232))

    im.save(OUT)
    a = np.asarray(im.convert("RGB"), dtype=np.float64)
    L = 0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2]
    print(f"WROTE {OUT}  size={im.size}  mean_luma={L.mean():.1f} (>=33)  contrast_std={L.std():.1f} (>=40)")


if __name__ == "__main__":
    build()
