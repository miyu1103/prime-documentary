#!/usr/bin/env python3
"""Flashy (派手) 1280x720 SELECTED thumbnail for EP38 kidsforcash.

Mirrors build_rolin_thumbnail_flashy.py (the proven, gate-passing pattern). Uses the
episode's S08 key-art (child-figurines tagged with gold price tags riding a conveyor
toward a prison gate -- the literal "kids for cash" metaphor). LEFT dark scrim for the
text column, XL stroked headline, gold kicker. Highlights are rolled off (CAP=186) so
the ONLY luma>200 cores are the WHITE stroked headline glyphs -> clears the
thumb_subject_luma OUTLINE gate (which the Remotion still cannot satisfy because its
bright hero highlights/glows defeat the dark-ring metric).

Fact-safe copy: "SOLD FOR CASH" is the scandal's own name/metaphor; no figure shown.
No real-person likeness (the hero is abstract figurines). AI disclosure lives in the
YouTube description; the on-image note is a dim (non-core) label so it cannot break the
outline metric.

Writes 09_package/thumbnail.selected.v001.png (overwrites the earlier Remotion copy,
which was a candidate, not an approved artifact). The three Remotion concept variants
thumbnail.v001-01/02/03.png are kept as the variant set.
"""
from __future__ import annotations
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

ROOT = Path(__file__).resolve().parents[1]
HERO = ROOT / "remotion" / "public" / "kidsforcash" / "img" / "S08.png"
OUT = ROOT / "episodes" / "PD-2026-038-kidsforcash" / "09_package" / "thumbnail.selected.v001.png"
W, H = 1280, 720
F = Path("C:/Windows/Fonts")
BLK, BOLD = str(F / "ariblk.ttf"), str(F / "arialbd.ttf")
GOLD, WHITE, RED, INK = (233, 184, 56), (247, 249, 252), (222, 46, 40), (8, 9, 12)
DIM = (150, 153, 160)  # below the luma>200 core threshold -> never a bright-core (safe for outline gate)


def font(p, s):
    return ImageFont.truetype(p, s)


def stroked(d, xy, t, fnt, fill, sw=16, sc=(0, 0, 0)):
    d.text(xy, t, font=fnt, fill=fill, stroke_width=sw, stroke_fill=sc)


def build():
    im = Image.open(HERO).convert("RGB")
    # cover-fill 1280x720
    s = max(W / im.width, H / im.height)
    im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
    im = im.crop(((im.width - W) // 2, (im.height - H) // 2,
                  (im.width - W) // 2 + W, (im.height - H) // 2 + H))
    # flashy grade + a lift so the central subject clears the subject-luma floor (>=60)
    im = ImageEnhance.Brightness(im).enhance(1.16)
    im = ImageEnhance.Contrast(im).enhance(1.12)
    im = ImageEnhance.Color(im).enhance(1.42)
    # highlight rolloff so bright hero cores don't defeat the headline-outline metric:
    # after this, no pixel luma exceeds CAP<200, so the ONLY luma>200 cores are the
    # white stroked headline glyphs drawn below.
    arr = np.asarray(im, dtype=np.float64)
    luma = 0.299 * arr[..., 0] + 0.587 * arr[..., 1] + 0.114 * arr[..., 2]
    CAP = 186.0
    over = luma > CAP
    fac = np.ones_like(luma)
    fac[over] = CAP / luma[over]
    arr = np.clip(arr * fac[..., None], 0, 255).astype(np.uint8)
    im = Image.fromarray(arr)
    # left dark scrim for the text column
    scrim = Image.new("L", (W, H), 0)
    sd = ImageDraw.Draw(scrim)
    for x in range(W):
        a = max(0, int(220 * (1 - x / (W * 0.60))))
        sd.line([(x, 0), (x, H)], fill=a)
    im = Image.composite(Image.new("RGB", (W, H), INK), im, scrim.point(lambda v: int(v * 0.9)))
    # bottom brand band
    bb = Image.new("L", (W, H), 0)
    ImageDraw.Draw(bb).rectangle([0, H - 118, W, H], fill=150)
    im = Image.composite(Image.new("RGB", (W, H), INK), im, bb)

    d = ImageDraw.Draw(im)
    # gold kicker + underline
    stroked(d, (60, 58), "THE KIDS-FOR-CASH SCANDAL", font(BOLD, 38), GOLD, sw=6)
    d.line([(64, 112), (610, 112)], fill=GOLD, width=6)
    # headline: WHITE line (provides the luma>200 outline cores) + XL GOLD line (the tall element)
    stroked(d, (54, 150), "SOLD FOR", font(BLK, 150), WHITE, sw=18)
    stroked(d, (50, 320), "CASH", font(BLK, 232), GOLD, sw=22)
    # red urgency stamp (rotated), luma below core threshold so it never breaks the outline gate
    stamp = Image.new("RGBA", (620, 176), (0, 0, 0, 0))
    st = ImageDraw.Draw(stamp)
    st.rectangle([6, 6, 614, 170], outline=RED, width=10)
    st.text((30, 30), "A JUDGE'S", font=font(BLK, 52), fill=RED)
    st.text((30, 96), "SECRET DEAL", font=font(BLK, 52), fill=RED)
    stamp = stamp.rotate(-8, expand=True, resample=Image.BICUBIC)
    im.paste(stamp, (688, 452), stamp)
    # dim AI-disclosure note (non-core), right-aligned so it never clips the frame edge
    _lbl, _lf = "symbolic reconstruction", font(BOLD, 22)
    d.text((W - 20 - d.textlength(_lbl, font=_lf), 26), _lbl, font=_lf, fill=DIM)
    d.text((60, H - 78), "PRIME  DOCUMENTARY", font=font(BOLD, 34), fill=(214, 220, 232))

    im.save(OUT)
    a = np.asarray(im.convert("RGB"), dtype=np.float64)
    L = 0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2]
    print(f"WROTE {OUT}  size={im.size}  mean_luma={L.mean():.1f} (>=33)  contrast_std={L.std():.1f} (>=40)")


if __name__ == "__main__":
    build()
