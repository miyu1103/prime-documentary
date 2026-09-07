#!/usr/bin/env python3
"""Recompose the EP48 glover face thumbnail from a saved raw (no SDXL).

The face generated center-left, so the module's vertically-centred headline landed
on the eyes (a §4A violation). This keeps the same look but anchors the headline
BLOCK to the lower-left so the eyes stay clear, with the kicker chip top-left.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path
from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "scripts" / "build_face_thumbnails_ep4447.py"
spec = importlib.util.spec_from_file_location("ep4447", SRC)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

W, H = m.W, m.H
RAW = Path(r"C:\Users\aab15\AppData\Local\Temp\claude\C--Users-aab15-OneDrive-Desktop\2fa81074-5db3-40a1-8cda-403c929c15de\scratchpad\glover_raw_seed48513.png")
OUT = ROOT / "episodes" / "PD-2026-048-glover" / "09_package" / "thumbnail.face.v001.png"

KICKER = "THEY RAN YOUR PLATE"
LINES = [("STOPPED FOR", m.WHITE), ("A NAME", m.YELLOW)]
ACCENT = m.YELLOW


def headline_low(img):
    d = ImageDraw.Draw(img)
    MX = 60
    max_w = int(W * 0.52)
    size = 172
    while size > 96:
        f = ImageFont.truetype(m.FONT_ANTON, size)
        widest = max(d.textlength(t, font=f) for t, _ in LINES)
        if widest <= max_w:
            break
        size -= 4
    f = ImageFont.truetype(m.FONT_ANTON, size)
    asc, desc = f.getmetrics()
    adv = int((asc + desc) * 0.86)
    block_h = len(LINES) * adv
    # bottom-anchor the block low so the eyes (upper third) stay clear
    bottom = int(H * 0.93)
    top = bottom - block_h
    # kicker chip above the block
    kf = ImageFont.truetype(m.FONT_BOLD, 30)
    ktext = KICKER
    ktw = d.textlength(ktext, font=kf)
    ky = top - 66
    d.rectangle([MX - 14, ky - 10, MX + ktw + 14, ky + 40], fill=(6, 10, 18))
    d.text((MX, ky), ktext, font=kf, fill=m.WHITE, stroke_width=2, stroke_fill=(0, 0, 0))
    d.rectangle([MX - 14, ky + 44, MX - 14 + ktw + 28, ky + 52], fill=ACCENT)
    # headline lines
    y = top
    stroke = max(10, size // 9)
    for text, color in LINES:
        d.text((MX, y), text, font=f, fill=color, stroke_width=stroke, stroke_fill=(0, 0, 0))
        y += adv
    d.rectangle([MX + 2, y + 4, MX + 2 + int(max_w * 0.62), y + 20], fill=ACCENT)
    return img


def main():
    face = Image.open(RAW).convert("RGB")
    # crop: keep the face centred-left and the open patrol-light road on the right
    z, cx, cy = 1.06, 0.50, 0.40
    sw, sh = face.size
    cw, ch = int(sw / z), int(sh / z)
    cxp, cyp = int(sw * cx), int(sh * cy)
    l = max(0, min(sw - cw, cxp - cw // 2))
    t = max(0, min(sh - ch, cyp - ch // 2))
    face = face.crop((l, t, l + cw, t + ch))
    img = ImageOps.fit(face, (W, H), method=Image.LANCZOS, centering=(0.5, 0.38))
    img = ImageEnhance.Contrast(img).enhance(1.06)
    img = ImageEnhance.Color(img).enhance(1.08)
    img = m.clamp_highlights(img)
    img = m.left_scrim(img, width_frac=0.52, strength=200)
    img = headline_low(img)
    img = m.place_logo(img)
    edge, nbytes = m.save_under_cap(img, OUT)
    print(f"-> {OUT} ({edge}px, {nbytes/1024:.0f} KB)")


if __name__ == "__main__":
    main()
