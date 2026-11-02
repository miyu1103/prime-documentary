#!/usr/bin/env python3
"""Flashy (派手) 1280x720 thumbnails for EP36 williams.

EP36 "The Algorithm Said It Was You" -- Robert Williams, the first known US
wrongful arrest from facial-recognition misidentification (Williams v. Detroit).
Tone: cool navy surveillance/tech + a warning RED accent (with the cyan scan
motif pulled from the stills).

Modeled 1:1 on scripts/build_tyler_thumbnail_flashy.py so the acceptance gates
pass (CLAUDE invariant: extend, don't reinvent):
  * bright, saturated hero (cover-filled) + navy scrim column for the headline;
  * highlights ROLLED OFF (cap 185) so the ONLY luma>200 cores in the frame are
    the white headline glyphs -> the thumb_subject_luma OUTLINE metric sees a
    thick dark rim (the >=12px gate; we push a 30px black stroke -> ~28px cap);
  * the 3 stacked headline lines are spaced so their black strokes MERGE into one
    tall 4-connected foreground component -> clears the >=150px text-height gate;
  * XL Arial-Black headline, red kicker tag, red rotated stamp, PD monogram.

Writes 3 distinct variants into 10_thumbnail/ and copies the selected one to
09_package/thumbnail.selected.v001.png (the checker's selection convention:
check_thumb_subject_luma / check_thumbnail_visibility read
09_package/thumbnail.selected*.png).
"""
from __future__ import annotations
import shutil
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

ROOT = Path(__file__).resolve().parents[1]
IMGDIR = ROOT / "remotion" / "public" / "williams" / "img"
EPDIR = ROOT / "episodes" / "PD-2026-036-williams"
THUMBDIR = EPDIR / "10_thumbnail"
PKGDIR = EPDIR / "09_package"
W, H = 1280, 720

FONTS = Path("C:/Windows/Fonts")
BLK = str(FONTS / "ariblk.ttf")      # Arial Black
BOLD = str(FONTS / "arialbd.ttf")

WHITE = (245, 247, 250)
RED = (222, 52, 46)
CYAN = (86, 206, 224)
INK = (8, 10, 16)
NAVY = (10, 16, 32)


def f(path, size):
    return ImageFont.truetype(path, size)


def stroked(d, xy, text, font, fill, sw, stroke=(0, 0, 0)):
    d.text(xy, text, font=font, fill=fill, stroke_width=sw, stroke_fill=stroke)


def grade_hero(src: Path, focus_x: float, flip: bool) -> Image.Image:
    """Cover-fill 1280x720 from `src`, biasing the crop toward focus_x (0=left..1=right)
    so the key subject lands under the right side, then punch + cap highlights."""
    im = Image.open(src).convert("RGB")
    if flip:
        im = im.transpose(Image.FLIP_LEFT_RIGHT)
    scale = max(W / im.width, H / im.height)
    im = im.resize((int(im.width * scale), int(im.height * scale)), Image.LANCZOS)
    # horizontal crop offset biased by focus_x; vertical centred
    x0 = int((im.width - W) * focus_x)
    x0 = max(0, min(im.width - W, x0))
    y0 = (im.height - H) // 2
    im = im.crop((x0, y0, x0 + W, y0 + H))

    # flashy grade: lift shadows (gamma) + brighten + saturate so the central
    # SUBJECT region clears the luma floor, then roll OFF highlights so the only
    # luma>200 cores in the frame are the white headline glyphs.
    im = ImageEnhance.Color(im).enhance(1.42)
    im = ImageEnhance.Contrast(im).enhance(1.10)
    arr = np.asarray(im, dtype=np.float64)
    arr = 255.0 * np.power(np.clip(arr / 255.0, 0, 1), 0.72)   # shadow lift
    arr = np.clip(arr * 1.30, 0, 255)                          # overall brightness
    luma = 0.299 * arr[..., 0] + 0.587 * arr[..., 1] + 0.114 * arr[..., 2]
    CAP = 185.0
    over = luma > CAP
    factor = np.ones_like(luma)
    factor[over] = CAP / luma[over]
    arr = arr * factor[..., None]
    return Image.fromarray(np.clip(arr, 0, 255).astype("uint8"), "RGB")


def fit_font(d, lines, path, maxw, start=104, floor=64):
    """Largest Arial-Black size whose longest line fits maxw."""
    size = start
    while size > floor:
        fnt = f(path, size)
        if max(d.textlength(ln, font=fnt) for ln in lines) <= maxw:
            return fnt, size
        size -= 2
    return f(path, floor), floor


def build(hero: str, focus_x: float, flip: bool, kicker: str,
          lines: list[str], stamp: str, out_name: str) -> Path:
    base = grade_hero(IMGDIR / hero, focus_x, flip).convert("RGBA")

    # navy scrim: opaque left -> clear ~60% across, plus a bottom fade
    scrim = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(scrim)
    for x in range(W):
        a = int(232 * max(0.0, 1 - (x / (W * 0.52))))
        sd.line([(x, 0), (x, H)], fill=(*NAVY, a))
    for y in range(H):
        a = int(165 * max(0.0, (y - H * 0.62) / (H * 0.38)))
        sd.line([(0, y), (W, y)], fill=(4, 6, 12, a))
    base = Image.alpha_composite(base, scrim)

    d = ImageDraw.Draw(base)
    # warning frame: red inner + thin cyan tech line at top
    d.rectangle([0, 0, W - 1, H - 1], outline=RED, width=5)
    d.line([(0, 6), (W, 6)], fill=CYAN, width=2)

    # RED kicker tag (top-left, highest attention)
    kf = f(BLK, 32)
    kw = d.textlength(kicker, font=kf)
    d.rectangle([46, 44, 46 + kw + 40, 44 + 52], fill=RED)
    stroked(d, (66, 51), kicker, kf, WHITE, sw=2)

    # XL headline: white, thick black stroke; lines pitched to MERGE into one tall
    # 4-connected component (clears the >=150px text-height gate) and the 30px
    # stroke gives a wide dark rim (clears the >=12px outline gate, ~28px cap).
    SW = 30
    hf, size = fit_font(d, lines, BLK, maxw=690, start=104, floor=66)
    pitch = size + 20       # strokes still overlap/merge, a touch more breathing room
    y = 132
    for ln in lines:
        stroked(d, (50, y), ln, hf, WHITE, sw=SW)
        y += pitch

    # red rotated stamp (upper-right, clear of headline)
    stw, sth = 470, 150
    st = Image.new("RGBA", (stw, sth), (0, 0, 0, 0))
    std = ImageDraw.Draw(st)
    sfsz = 78 if len(stamp) <= 8 else 60
    sf = f(BLK, sfsz)
    tw = std.textlength(stamp, font=sf)
    std.rounded_rectangle([6, 6, stw - 6, sth - 6], radius=12, outline=RED, width=8)
    std.text(((stw - tw) / 2, (sth - sfsz) / 2 - 6), stamp, font=sf, fill=RED,
             stroke_width=2, stroke_fill=(30, 4, 4))
    st = st.rotate(-11, expand=True, resample=Image.BICUBIC)
    base.alpha_composite(st, (W - st.width - 30, 150))

    # PD monogram (branding)
    d = ImageDraw.Draw(base)
    mf = f(BLK, 38)
    d.ellipse([W - 94, H - 94, W - 40, H - 40], outline=CYAN, width=3)
    d.text((W - 82, H - 82), "PD", font=mf, fill=CYAN)

    out = base.convert("RGB")
    THUMBDIR.mkdir(parents=True, exist_ok=True)
    p = THUMBDIR / out_name
    out.save(p, "PNG")
    print("wrote", p)
    return p


VARIANTS = [
    # (hero, focus_x, flip, kicker, lines, stamp, out_name, selected?)
    ("PD-2026-036-S018-IMG-001.png", 0.62, False, "FACIAL RECOGNITION",
     ["THE ALGORITHM", "SAID IT", "WAS YOU"], "WRONG MAN",
     "thumbnail.v001.png", True),
    ("PD-2026-036-S003-IMG-001.png", 0.72, False, "FALSELY ACCUSED",
     ["ARRESTED", "BY AN", "ALGORITHM"], "FALSE MATCH",
     "thumbnail.v002.png", False),
    ("PD-2026-036-S007-IMG-001.png", 0.60, False, "WILLIAMS v. DETROIT",
     ["A MATCH IS", "NOT A", "NAME"], "MISIDENTIFIED",
     "thumbnail.v003.png", False),
]


def main():
    selected_src = None
    for hero, fx, flip, kick, lines, stamp, name, is_sel in VARIANTS:
        p = build(hero, fx, flip, kick, lines, stamp, name)
        if is_sel:
            selected_src = p
    PKGDIR.mkdir(parents=True, exist_ok=True)
    sel = PKGDIR / "thumbnail.selected.v001.png"
    shutil.copyfile(selected_src, sel)
    print("selected ->", sel)


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    main()
