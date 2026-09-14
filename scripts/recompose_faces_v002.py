#!/usr/bin/env python3
r"""Recompose OVERLAP face thumbnails -> v002 (no SDXL, CPU only).

Fixes the text-on-face defect on EP045/046/047/048/049 by re-cropping the saved
raw SDXL face so the subject sits in the RIGHT ~40% and the bold headline lives in
a clean dark LEFT column (matches the CLEAN reference layout: young/thompson/tekoh).

Keeps the existing house style: Anton ALL-CAPS headline (white / one yellow shock
word, or a red bar), a top-left kicker chip, an accent underline, PD logo bottom-right.

Writes thumbnail.face.v002.png (never overwrites v001).

    py -3.11 scripts/recompose_faces_v002.py [ep_slug ...]
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "scripts" / "build_face_thumbnails_ep4447.py"
_spec = importlib.util.spec_from_file_location("ep4447", SRC)
m = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(m)

W, H = m.W, m.H
WHITE, YELLOW, RED = m.WHITE, m.YELLOW, m.RED
SCRATCH = Path(r"C:\Users\aab15\AppData\Local\Temp\claude\C--Users-aab15-OneDrive-Desktop\2fa81074-5db3-40a1-8cda-403c929c15de\scratchpad")

# slug -> recompose spec
#   raw       : source SDXL raw (pre-text) in scratch
#   zoom      : crop tightness (bigger = face larger / pushed further right)
#   fx,fy     : face center in the raw (fraction)
#   tx,ty     : where to place the face center in the 1280x720 output (fraction)
#   scrim_w/s : left dark-scrim width fraction / strength
#   kicker/lines/redbar/accent : identical text spec to the original builder
EPS = {
    "PD-2026-043-caniglia": dict(
        raw="PD-2026-043-caniglia_raw_seed43208.png",
        zoom=1.14, fx=0.60, fy=0.38, tx=0.68, ty=0.42, scrim_w=0.54, scrim_s=222,
        kicker="IT WAS A WELFARE CHECK", lines=[("THEY TOOK", WHITE), ("HIS GUNS", WHITE)],
        redbar=True, accent=RED,
    ),
    "PD-2026-045-cleveland": dict(
        raw="PD-2026-045-cleveland_raw_seed45813.png",
        zoom=1.16, fx=0.55, fy=0.42, tx=0.70, ty=0.44, scrim_w=0.54, scrim_s=220,
        kicker="DEBTORS' PRISON", lines=[("JAILED FOR", WHITE), ("BEING POOR", WHITE)],
        redbar=True, accent=RED,
    ),
    "PD-2026-046-tlo": dict(
        raw="PD-2026-046-tlo_raw_seed46431.png",
        zoom=1.30, fx=0.55, fy=0.42, tx=0.69, ty=0.46, scrim_w=0.54, scrim_s=215,
        kicker="NO WARRANT NEEDED", lines=[("SEARCHED", WHITE), ("AT SCHOOL", WHITE)],
        redbar=False, accent=YELLOW,
    ),
    "PD-2026-047-atwater": dict(
        raw="PD-2026-047-atwater_raw_seed47820.png",
        zoom=1.16, fx=0.60, fy=0.16, tx=0.70, ty=0.28, scrim_w=0.52, scrim_s=215,
        kicker="OVER A $50 FINE", lines=[("JAILED OVER", WHITE), ("A SEATBELT", YELLOW)],
        redbar=False, accent=YELLOW,
    ),
    "PD-2026-048-glover": dict(
        raw="PD-2026-048-glover_raw_seed48715.png",
        zoom=1.12, fx=0.62, fy=0.30, tx=0.70, ty=0.36, scrim_w=0.52, scrim_s=210,
        kicker="THEY RAN YOUR PLATE", lines=[("STOPPED FOR", WHITE), ("A NAME", YELLOW)],
        redbar=False, accent=YELLOW,
    ),
    "PD-2026-049-strieff": dict(
        raw="strieff_raw_seed49308.png",
        zoom=1.14, fx=0.52, fy=0.32, tx=0.68, ty=0.36, scrim_w=0.54, scrim_s=218,
        kicker="AN ILLEGAL STOP", lines=[("STOPPED FOR", WHITE), ("NOTHING", YELLOW)],
        redbar=False, accent=YELLOW,
    ),
}


def place(raw, zoom, fx, fy, tx, ty):
    """Crop a 16:9 window from the raw so the face center (fx,fy) lands at (tx,ty)."""
    sw, sh = raw.size
    cw = min(sw, int(sw / zoom))
    ch = int(cw * 9 / 16)
    if ch > sh:
        ch = sh
        cw = int(ch * 16 / 9)
    left = int(fx * sw - tx * cw)
    top = int(fy * sh - ty * ch)
    left = max(0, min(sw - cw, left))
    top = max(0, min(sh - ch, top))
    crop = raw.crop((left, top, left + cw, top + ch))
    return crop.resize((W, H), Image.LANCZOS)


def headline(img, spec):
    """Left-column Anton headline; right edge hard-capped at 50% so it never hits the face."""
    d = ImageDraw.Draw(img)
    MX = 56
    max_w = int(W * 0.46)          # right edge ~ 56 + 589 = 645px (=50.4% of 1280)
    lines = spec["lines"]
    size = 168
    while size > 88:
        f = ImageFont.truetype(m.FONT_ANTON, size)
        widest = max(d.textlength(t, font=f) for t, _ in lines)
        if widest <= max_w:
            break
        size -= 4
    f = ImageFont.truetype(m.FONT_ANTON, size)
    asc, desc = f.getmetrics()
    adv = int((asc + desc) * 0.86)
    block_h = len(lines) * adv
    top = (H - block_h) // 2 + 12
    # kicker chip above the block
    kf = ImageFont.truetype(m.FONT_BOLD, 30)
    ktext = spec["kicker"]
    ktw = d.textlength(ktext, font=kf)
    ky = top - 74
    d.rectangle([MX - 14, ky - 10, MX + ktw + 14, ky + 40], fill=(6, 10, 18))
    d.text((MX, ky), ktext, font=kf, fill=WHITE, stroke_width=2, stroke_fill=(0, 0, 0))
    d.rectangle([MX - 14, ky + 44, MX - 14 + ktw + 28, ky + 52], fill=spec["accent"])
    # headline
    y = top
    stroke = max(10, size // 9)
    for text, color in lines:
        if spec["redbar"]:
            tw = d.textlength(text, font=f)
            d.rectangle([MX - 12, y + int(desc * 0.55), MX + tw + 22, y + adv - int(desc * 0.15)], fill=RED)
            d.text((MX, y), text, font=f, fill=WHITE, stroke_width=4, stroke_fill=(90, 0, 0))
        else:
            d.text((MX, y), text, font=f, fill=color, stroke_width=stroke, stroke_fill=(0, 0, 0))
        y += adv
    if not spec["redbar"]:
        d.rectangle([MX + 2, y + 4, MX + 2 + int(max_w * 0.62), y + 20], fill=spec["accent"])
    return img


def recompose(slug, spec):
    raw = Image.open(SCRATCH / spec["raw"]).convert("RGB")
    img = place(raw, spec["zoom"], spec["fx"], spec["fy"], spec["tx"], spec["ty"])
    img = ImageEnhance.Contrast(img).enhance(1.06)
    img = ImageEnhance.Color(img).enhance(1.08)
    img = m.clamp_highlights(img)
    img = m.left_scrim(img, width_frac=spec["scrim_w"], strength=spec["scrim_s"])
    img = headline(img, spec)
    img = m.place_logo(img)
    out = ROOT / "episodes" / slug / "09_package" / "thumbnail.face.v002.png"
    edge, nbytes = m.save_under_cap(img, out)
    img.save(SCRATCH / f"{slug}_v002_composite.png")
    print(f"  {slug} -> {out.name}  ({edge}px, {nbytes/1024:.0f} KB)", flush=True)
    return out


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    slugs = args or list(EPS.keys())
    for slug in slugs:
        recompose(slug, EPS[slug])


if __name__ == "__main__":
    main()
