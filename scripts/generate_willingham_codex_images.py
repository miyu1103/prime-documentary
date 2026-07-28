#!/usr/bin/env python
"""Generate EP51 Willingham non-SDXL still assets locally.

This is intentionally limited to image files under H:/pd-media/assets/ai/willingham.
It does not write the episode manifest, stock selections, Remotion source, or video.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageOps, ImageStat


W, H = 3840, 2160
EMBER = (194, 90, 46)
COLD = (127, 168, 176)
INK = (11, 10, 9)
BONE = (236, 231, 223)
OUT_DIR = Path("H:/pd-media/assets/ai/willingham")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def clamp(v: int) -> int:
    return max(0, min(255, v))


def color_jitter(color: tuple[int, int, int], rng: random.Random, amount: int = 12) -> tuple[int, int, int]:
    return tuple(clamp(c + rng.randint(-amount, amount)) for c in color)


def new_canvas(seed: int, cold: bool = False) -> Image.Image:
    rng = random.Random(seed)
    top = (6, 8, 9) if not cold else (7, 14, 16)
    bottom = (32, 24, 19) if not cold else (18, 30, 34)
    top = color_jitter(top, rng, 6)
    bottom = color_jitter(bottom, rng, 8)
    grad = Image.linear_gradient("L").resize((W, H))
    im = Image.composite(Image.new("RGB", (W, H), bottom), Image.new("RGB", (W, H), top), grad)
    return im


def overlay_rgba(base: Image.Image, layer: Image.Image) -> Image.Image:
    return Image.alpha_composite(base.convert("RGBA"), layer).convert("RGB")


def glow_layer(cx: int, cy: int, rx: int, ry: int, color: tuple[int, int, int], alpha: int) -> Image.Image:
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    for i in range(18, 0, -1):
        a = int(alpha * (i / 18) ** 2)
        box = (
            cx - rx * i // 18,
            cy - ry * i // 18,
            cx + rx * i // 18,
            cy + ry * i // 18,
        )
        draw.ellipse(box, fill=(*color, a))
    return layer.filter(ImageFilter.GaussianBlur(24))


def add_grade(im: Image.Image, seed: int) -> Image.Image:
    rng = random.Random(seed + 100_000)
    noise = Image.effect_noise((W, H), 10).convert("L")
    grain = Image.merge("RGB", (noise, noise, noise))
    im = Image.blend(im, grain, 0.035)
    # Subtle edge darkening for optical falloff, kept low to avoid a washed vignette.
    mask = Image.radial_gradient("L").resize((W, W)).crop((0, (W - H) // 2, W, (W + H) // 2))
    mask = ImageOps.invert(ImageOps.autocontrast(mask)).point(lambda p: int(p * 0.20))
    shade = Image.new("RGB", (W, H), (0, 0, 0))
    im = Image.composite(shade, im, mask)
    if rng.random() < 0.45:
        im = im.filter(ImageFilter.UnsharpMask(radius=1.2, percent=115, threshold=3))
    lum = ImageStat.Stat(im.convert("L").resize((64, 36))).mean[0]
    if lum < 30:
        im = ImageEnhance.Brightness(im).enhance(min(2.2, 34 / max(lum, 1)))
        im = ImageEnhance.Contrast(im).enhance(1.08)
    return im


def draw_house(draw: ImageDraw.ImageDraw, seed: int, burned: bool = False, dawn: bool = False) -> None:
    rng = random.Random(seed)
    x = 700 + rng.randint(-120, 120)
    y = 690 + rng.randint(-45, 45)
    w = 2300 + rng.randint(-140, 100)
    h = 850 + rng.randint(-80, 80)
    wall = (48, 51, 48) if not burned else (28, 25, 22)
    roof = (14, 15, 15) if not burned else (12, 10, 9)
    draw.rectangle((x, y + 260, x + w, y + h), fill=wall, outline=(98, 101, 96), width=5)
    draw.polygon([(x - 80, y + 280), (x + w // 2, y - 80), (x + w + 80, y + 280)], fill=roof)
    draw.rectangle((x + int(w * 0.55), y + 330, x + int(w * 0.92), y + h), fill=(34, 34, 31))
    for i in range(7):
        yy = y + 330 + i * 86
        draw.line((x + 30, yy, x + w - 30, yy), fill=(78, 79, 72), width=3)
    for wx in [x + 360, x + 720, x + int(w * 0.62), x + int(w * 0.82)]:
        wy = y + 440 + rng.randint(-30, 25)
        win = (x + 120, y + 390, x + 450, y + 760) if burned else (wx, wy, wx + 260, wy + 310)
        fill = (96, 42, 22) if burned else EMBER
        draw.rectangle(win, fill=fill, outline=(18, 18, 15), width=10)
        draw.line((win[0] + 130, win[1], win[0] + 130, win[3]), fill=(35, 24, 18), width=6)
        draw.line((win[0], win[1] + 155, win[2], win[1] + 155), fill=(35, 24, 18), width=6)
    porch_y = y + h - 130
    draw.rectangle((x + 880, y + 410, x + 1120, y + h), fill=(10, 10, 9))
    draw.rectangle((x + 1160, porch_y, x + w - 160, porch_y + 70), fill=(62, 61, 56))
    for px in range(x + 1220, x + w - 180, 180):
        draw.rectangle((px, y + 380, px + 24, porch_y + 40), fill=(86, 83, 76))
    if burned:
        for _ in range(18):
            sx = rng.randint(x - 60, x + w + 40)
            sy = rng.randint(y + 80, y + h + 60)
            draw.line((sx, sy, sx + rng.randint(-50, 60), sy - rng.randint(160, 380)), fill=(19, 18, 16), width=rng.randint(12, 28))
    ground = (46, 42, 31) if not dawn else (52, 64, 60)
    draw.rectangle((0, y + h - 20, W, H), fill=ground)
    for _ in range(260):
        gx = rng.randint(0, W)
        gy = rng.randint(y + h - 60, H)
        draw.line((gx, gy, gx + rng.randint(-18, 18), gy - rng.randint(20, 95)), fill=color_jitter((84, 74, 48), rng, 24), width=rng.randint(1, 4))


def house_scene(seed: int, burned: bool = False, dawn: bool = False) -> Image.Image:
    im = new_canvas(seed, cold=dawn or burned)
    im = overlay_rgba(im, glow_layer(W // 2, 820, 1550, 560, EMBER if not dawn else COLD, 60 if not dawn else 35))
    draw = ImageDraw.Draw(im)
    draw_house(draw, seed, burned=burned, dawn=dawn)
    return add_grade(im, seed)


def embers(seed: int, cold: bool = False) -> Image.Image:
    rng = random.Random(seed)
    im = new_canvas(seed, cold=cold)
    im = overlay_rgba(im, glow_layer(W // 2, H // 2, 1500, 850, COLD if cold else EMBER, 72))
    draw = ImageDraw.Draw(im, "RGBA")
    for _ in range(900):
        x = rng.randint(0, W)
        y = rng.randint(0, H)
        r = rng.randint(1, 8)
        a = rng.randint(28, 155)
        col = COLD if cold else EMBER
        draw.ellipse((x - r, y - r, x + r, y + r), fill=(*color_jitter(col, rng, 35), a))
    return add_grade(im, seed)


def char_pattern(seed: int, cold: bool = False, glass: bool = False) -> Image.Image:
    rng = random.Random(seed)
    im = new_canvas(seed, cold=cold)
    im = overlay_rgba(im, glow_layer(W // 2, H // 2, 1300, 760, COLD if cold else EMBER, 58))
    draw = ImageDraw.Draw(im, "RGBA")
    for _ in range(55):
        pts = []
        cx, cy = rng.randint(300, W - 300), rng.randint(250, H - 250)
        for a in range(0, 360, 24):
            rr = rng.randint(80, 310)
            pts.append((cx + int(math.cos(math.radians(a)) * rr), cy + int(math.sin(math.radians(a)) * rr)))
        draw.polygon(pts, fill=(6, 6, 5, rng.randint(115, 210)), outline=(*(COLD if cold else EMBER), rng.randint(55, 120)))
    if glass:
        for _ in range(34):
            cx, cy = rng.randint(520, W - 520), rng.randint(360, H - 360)
            for _ in range(7):
                ang = rng.random() * math.tau
                length = rng.randint(180, 640)
                draw.line((cx, cy, cx + int(math.cos(ang) * length), cy + int(math.sin(ang) * length)), fill=(*BONE, 110), width=rng.randint(3, 8))
    return add_grade(im, seed)


def clock_scene(seed: int) -> Image.Image:
    im = new_canvas(seed, cold=True)
    im = overlay_rgba(im, glow_layer(W // 2, H // 2, 1050, 650, COLD, 36))
    draw = ImageDraw.Draw(im, "RGBA")
    cx, cy, r = W // 2, H // 2, 520
    draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(30, 35, 34, 225), outline=(*BONE, 120), width=18)
    draw.ellipse((cx - 28, cy - 28, cx + 28, cy + 28), fill=(*COLD, 180))
    a1 = -math.pi / 2 + seed * 0.08
    a2 = -math.pi / 2 + seed * 0.035
    draw.line((cx, cy, cx + int(math.cos(a1) * 290), cy + int(math.sin(a1) * 290)), fill=(*BONE, 190), width=16)
    draw.line((cx, cy, cx + int(math.cos(a2) * 410), cy + int(math.sin(a2) * 410)), fill=(*EMBER, 150), width=10)
    return add_grade(im, seed)


def poster_wall(seed: int) -> Image.Image:
    rng = random.Random(seed)
    im = new_canvas(seed, cold=False)
    draw = ImageDraw.Draw(im, "RGBA")
    for i in range(18):
        x = 260 + (i % 6) * 550 + rng.randint(-35, 35)
        y = 260 + (i // 6) * 500 + rng.randint(-35, 35)
        draw.rectangle((x, y, x + 420, y + 330), fill=color_jitter((34, 28, 28), rng, 20), outline=(*EMBER, 80), width=5)
        if i % 3 == 0:
            draw.ellipse((x + 135, y + 60, x + 285, y + 210), outline=(*BONE, 110), width=8)
            draw.line((x + 130, y + 230, x + 300, y + 260), fill=(*BONE, 80), width=8)
        else:
            pts = [(x + 80, y + 260), (x + 210, y + 60), (x + 340, y + 260)]
            draw.line(pts + [pts[0]], fill=(*EMBER, 120), width=9)
    im = overlay_rgba(im, glow_layer(900, 700, 1100, 620, EMBER, 42))
    return add_grade(im, seed)


def grave_or_town(seed: int, town: bool = False) -> Image.Image:
    rng = random.Random(seed)
    im = new_canvas(seed, cold=True)
    draw = ImageDraw.Draw(im, "RGBA")
    horizon = 1010 + rng.randint(-80, 80)
    draw.rectangle((0, horizon, W, H), fill=(33, 38, 35))
    if town:
        for i in range(11):
            x = i * 390 + rng.randint(-80, 60)
            y = horizon - rng.randint(220, 560)
            draw.rectangle((x, y, x + rng.randint(220, 430), horizon), fill=(20, 23, 24))
            draw.rectangle((x + 60, y + 80, x + 160, y + 170), fill=(*EMBER, 130))
        draw.line((0, horizon + 210, W, horizon + 60), fill=(*COLD, 80), width=10)
    else:
        for i in range(7):
            x = 620 + i * 430 + rng.randint(-50, 50)
            y = horizon - rng.randint(110, 190)
            draw.rounded_rectangle((x, y, x + 180, horizon + 15), radius=34, fill=(82, 88, 82), outline=(*COLD, 80), width=4)
    im = overlay_rgba(im, glow_layer(W // 2, 820, 1400, 520, COLD, 36))
    return add_grade(im, seed)


def pillars(seed: int, fallen: bool = False) -> Image.Image:
    rng = random.Random(seed)
    im = new_canvas(seed, cold=fallen)
    im = overlay_rgba(im, glow_layer(W // 2, 980, 1300, 760, COLD if fallen else EMBER, 55))
    draw = ImageDraw.Draw(im, "RGBA")
    if not fallen:
        for x in [1280, 2300]:
            draw.rectangle((x, 540, x + 310, 1670), fill=(37, 36, 33), outline=(*(COLD if rng.random() < 0.3 else EMBER), 120), width=8)
            draw.rectangle((x - 90, 430, x + 400, 550), fill=(58, 56, 51))
            draw.rectangle((x - 120, 1670, x + 430, 1810), fill=(48, 48, 45))
    else:
        for off in [0, 900]:
            draw.rounded_rectangle((730 + off, 1320, 1720 + off, 1570), radius=26, fill=(41, 43, 42), outline=(*COLD, 110), width=8)
            for k in range(5):
                draw.line((760 + off + k * 170, 1325, 910 + off + k * 150, 1570), fill=(20, 22, 22), width=8)
        draw.line((540, 1690, 3300, 1510), fill=(*COLD, 115), width=12)
    return add_grade(im, seed)


def document_scene(seed: int, cold: bool = True, envelopes: bool = False, report: bool = False) -> Image.Image:
    rng = random.Random(seed)
    im = new_canvas(seed, cold=cold)
    im = overlay_rgba(im, glow_layer(W // 2, 1000, 1250, 700, COLD if cold else EMBER, 42))
    draw = ImageDraw.Draw(im, "RGBA")
    table = (32, 27, 21) if not cold else (24, 31, 32)
    draw.rectangle((0, 1180, W, H), fill=table)
    count = 12 if report else 4
    for i in range(count):
        x = 1180 + i * 54 + rng.randint(-28, 28)
        y = 500 + i * 32 + rng.randint(-24, 24)
        draw.rounded_rectangle((x, y, x + 1180, y + 800), radius=16, fill=(190, 190, 177), outline=(82, 91, 94), width=4)
        for j in range(8):
            yy = y + 130 + j * 55
            draw.rounded_rectangle((x + 120, yy, x + 940 - rng.randint(0, 260), yy + 16), radius=8, fill=(106, 116, 118, 120))
    if envelopes:
        for i in range(5):
            x = 900 + i * 330 + rng.randint(-35, 35)
            y = 780 + rng.randint(-80, 90)
            draw.polygon([(x, y), (x + 540, y), (x + 540, y + 300), (x, y + 300)], fill=(176, 164, 138), outline=(104, 93, 75))
            draw.line((x, y, x + 270, y + 170, x + 540, y), fill=(116, 104, 82), width=5)
    return add_grade(im, seed)


def gavel_or_room(seed: int, chamber: bool = False, courtroom: bool = False) -> Image.Image:
    rng = random.Random(seed)
    im = new_canvas(seed, cold=True)
    im = overlay_rgba(im, glow_layer(W // 2, 920, 1200, 700, COLD, 45))
    draw = ImageDraw.Draw(im, "RGBA")
    if chamber:
        draw.rectangle((0, 0, W, H), fill=(16, 21, 22))
        draw.rectangle((680, 1380, 3140, 1540), fill=(56, 65, 66))
        draw.rounded_rectangle((1110, 1020, 2730, 1350), radius=70, fill=(74, 82, 82), outline=(*COLD, 100), width=10)
        for x in [1320, 1770, 2220]:
            draw.rectangle((x, 980, x + 110, 1400), fill=(38, 45, 46))
        draw.polygon([(1800, 0), (2040, 0), (2490, H), (1300, H)], fill=(*COLD, 38))
    elif courtroom:
        draw.rectangle((0, 1240, W, H), fill=(28, 27, 26))
        draw.rectangle((680, 860, 3160, 1200), fill=(56, 48, 41), outline=(*COLD, 80), width=8)
        for i in range(5):
            x = 960 + i * 420
            draw.rectangle((x, 420, x + 180, 860), fill=(44, 43, 40))
    else:
        draw.rounded_rectangle((900, 1250, 3000, 1450), radius=34, fill=(51, 45, 38), outline=(100, 93, 82), width=8)
        draw.rounded_rectangle((1580, 850, 2180, 1010), radius=46, fill=(75, 60, 43), outline=(*COLD, 90), width=6)
        draw.rectangle((1980, 960, 2660, 1060), fill=(84, 66, 44))
        draw.ellipse((1240, 1220, 1580, 1410), fill=(78, 67, 53), outline=(*COLD, 70), width=6)
    return add_grade(im, seed)


def lab_or_grill(seed: int, grill: bool = False, conference: bool = False) -> Image.Image:
    rng = random.Random(seed)
    im = new_canvas(seed, cold=True)
    im = overlay_rgba(im, glow_layer(W // 2, 860, 1450, 690, COLD, 50))
    draw = ImageDraw.Draw(im, "RGBA")
    draw.rectangle((0, 1220, W, H), fill=(22, 30, 31))
    if conference:
        draw.rounded_rectangle((650, 960, 3180, 1320), radius=90, fill=(48, 54, 53), outline=(*COLD, 90), width=8)
        for i in range(9):
            ang = (i / 9) * math.tau
            x = W // 2 + int(math.cos(ang) * 1150)
            y = 1130 + int(math.sin(ang) * 310)
            if i in {1, 4, 7}:
                draw.rounded_rectangle((x - 80, y - 80, x + 80, y + 150), radius=28, fill=(30, 32, 32), outline=(*EMBER, 70), width=5)
                draw.line((x - 100, y - 130, x + 100, y + 190), fill=(*EMBER, 70), width=8)
            else:
                draw.rounded_rectangle((x - 80, y - 80, x + 80, y + 150), radius=28, fill=(58, 62, 61), outline=(*COLD, 65), width=4)
    elif grill:
        draw.ellipse((1320, 850, 2500, 1470), fill=(20, 23, 22), outline=(*COLD, 120), width=12)
        for i in range(12):
            x = 1400 + i * 90
            draw.line((x, 890, x - 80, 1440), fill=(92, 102, 101), width=5)
        draw.rounded_rectangle((2660, 950, 2900, 1430), radius=28, fill=(66, 63, 54), outline=(*COLD, 85), width=5)
    else:
        for i in range(8):
            x = 700 + i * 290
            draw.rectangle((x, 740 + rng.randint(-20, 20), x + 160, 1190), fill=(46, 59, 61), outline=(*COLD, 80), width=4)
            draw.rectangle((x + 30, 550, x + 130, 740), fill=(*COLD, 70))
        draw.ellipse((1580, 960, 2270, 1190), fill=(*EMBER, 110))
    return add_grade(im, seed)


def abstract_machine(seed: int, cold: bool = False) -> Image.Image:
    rng = random.Random(seed)
    im = new_canvas(seed, cold=cold)
    im = overlay_rgba(im, glow_layer(W // 2, H // 2, 1350, 740, COLD if cold else EMBER, 46))
    draw = ImageDraw.Draw(im, "RGBA")
    col = COLD if cold else EMBER
    for i in range(12):
        cx = rng.randint(450, W - 450)
        cy = rng.randint(360, H - 360)
        r1 = rng.randint(90, 260)
        r2 = r1 + rng.randint(28, 70)
        draw.ellipse((cx - r2, cy - r2, cx + r2, cy + r2), outline=(*col, 110), width=14)
        draw.ellipse((cx - r1, cy - r1, cx + r1, cy + r1), outline=(45, 48, 47, 180), width=18)
        for k in range(12):
            a = k * math.tau / 12 + rng.random() * 0.08
            draw.line((cx, cy, cx + int(math.cos(a) * (r2 + 40)), cy + int(math.sin(a) * (r2 + 40))), fill=(*col, 65), width=7)
    return add_grade(im, seed)


def human_seed(seed: int, kind: int) -> Image.Image:
    rng = random.Random(seed)
    cold = kind in {4, 5, 7, 8}
    im = new_canvas(seed, cold=cold)
    im = overlay_rgba(im, glow_layer(W // 2, 930, 1320, 700, COLD if cold else EMBER, 50))
    draw = ImageDraw.Draw(im, "RGBA")
    if kind == 1:
        draw_house(draw, seed, burned=False)
        x, y = 1810, 1280
        draw.ellipse((x - 90, y - 260, x + 90, y - 90), fill=(8, 8, 7, 255))
        draw.rounded_rectangle((x - 160, y - 100, x + 160, y + 430), radius=80, fill=(9, 9, 8, 255))
        draw.line((x - 250, y + 80, x + 250, y + 90), fill=(9, 9, 8, 255), width=70)
    elif kind in {2, 4, 5}:
        draw.rectangle((0, 1220, W, H), fill=(20, 23, 23))
        for i in range(8):
            x = 760 + i * 290
            draw.rectangle((x, 300, x + 70, 1690), fill=(20, 23, 24))
        for person in range(2 if kind != 4 else 1):
            x = 1420 + person * 650 + rng.randint(-90, 90)
            y = 1020 + rng.randint(-80, 80)
            draw.ellipse((x - 85, y - 210, x + 85, y - 50), fill=(12, 12, 11, 245))
            draw.rounded_rectangle((x - 135, y - 50, x + 135, y + 500), radius=60, fill=(13, 13, 12, 245))
            if kind == 2:
                draw.polygon([(x - 250, y - 100), (x + 270, y - 70), (x + 760, y - 40), (x + 760, y + 20), (x + 260, y), (x - 240, y + 30)], fill=(*BONE, 45))
    elif kind in {3, 8}:
        draw.rectangle((0, 1180, W, H), fill=(32, 38, 36))
        for i in range(5 if kind == 3 else 1):
            x = 1300 + i * 260 - (520 if kind == 3 else 0)
            y = 920 + rng.randint(-45, 55)
            draw.ellipse((x - 75, y - 190, x + 75, y - 50), fill=(12, 12, 11, 245))
            draw.rounded_rectangle((x - 115, y - 50, x + 115, y + 430), radius=50, fill=(14, 14, 13, 245))
    else:
        document_scene(seed, cold=cold, envelopes=kind == 6)
        im = Image.open(OUT_DIR / "_scratch_doc.png") if False else im
        draw = ImageDraw.Draw(im, "RGBA")
        x, y = 1500, 980
        draw.rounded_rectangle((x, y, x + 820, y + 150), radius=70, fill=(68, 55, 43) if kind == 6 else (42, 51, 52))
        draw.ellipse((x + 40, y - 70, x + 260, y + 110), fill=(90, 70, 52, 220))
        for i in range(7):
            draw.rounded_rectangle((1110, 610 + i * 70, 2470 - rng.randint(0, 300), 632 + i * 70), radius=9, fill=(115, 126, 126, 100))
    return add_grade(im, seed)


def select_scene(asset: str) -> tuple[str, bool]:
    if asset.startswith("M"):
        i = int(asset[1:3])
        human_map = {2: 1, 5: 2, 8: 3, 12: 4, 14: 5, 17: 6, 20: 7, 26: 8}
        if i in human_map:
            return f"human:{human_map[i]}", True
        if i in {1, 3, 4, 6, 7, 29}:
            return "house", False
        if i in {9, 10, 11, 18, 21, 24, 27, 30}:
            return ("pillars" if i in {11, 24} else "char_cold"), False
        if i in {13, 15, 19}:
            return "document", False
        if i in {16, 23, 25}:
            return "flashover", False
        if i in {22}:
            return "chamber", False
        return "machine_cold", False

    n = int(asset[1:4])
    if 1 <= n <= 6:
        return "house", False
    if 7 <= n <= 13:
        return "embers", False
    if 14 <= n <= 16:
        return "clock", False
    if 17 <= n <= 24:
        return "burned_house", False
    if 25 <= n <= 30:
        return "char_ember", False
    if 31 <= n <= 38:
        return "poster", False
    if 39 <= n <= 42:
        return "grave", False
    if 43 <= n <= 46:
        return "town", False
    if 47 <= n <= 52:
        return "pillars", False
    if 53 <= n <= 62:
        return "glass" if n in {55, 56, 60} else "char_ember", False
    if 63 <= n <= 68:
        return "bars", False
    if 69 <= n <= 72:
        return "document", False
    if 73 <= n <= 80:
        return "court", False
    if 81 <= n <= 88:
        return "flashover", False
    if 89 <= n <= 92:
        return "glass_cold", False
    if 93 <= n <= 98:
        return "grill" if n in {93, 94, 98} else "lab", False
    if 99 <= n <= 106:
        return "envelopes" if n <= 102 else "document_cold", False
    if 107 <= n <= 112:
        return "chamber", False
    if 113 <= n <= 120:
        return "lab" if n != 120 else "chamber", False
    if 121 <= n <= 126:
        return "conference", False
    if 127 <= n <= 134:
        return "report" if n <= 130 else "bars_cold", False
    if 135 <= n <= 138:
        return "fallen", False
    if 139 <= n <= 142:
        return "document_cold", False
    if 143 <= n <= 146:
        return "yard_dawn", False
    return "machine_cold", False


def render(asset: str, seed: int) -> Image.Image:
    kind, _ = select_scene(asset)
    if kind.startswith("human:"):
        return human_seed(seed, int(kind.split(":")[1]))
    if kind == "house":
        return house_scene(seed)
    if kind == "yard_dawn":
        return house_scene(seed, dawn=True)
    if kind == "burned_house":
        return house_scene(seed, burned=True)
    if kind == "embers":
        return embers(seed)
    if kind == "clock":
        return clock_scene(seed)
    if kind == "char_ember":
        return char_pattern(seed, cold=False)
    if kind in {"char_cold", "flashover"}:
        return char_pattern(seed, cold=True, glass=kind == "flashover")
    if kind in {"glass", "glass_cold"}:
        return char_pattern(seed, cold=kind.endswith("cold"), glass=True)
    if kind == "poster":
        return poster_wall(seed)
    if kind == "grave":
        return grave_or_town(seed, town=False)
    if kind == "town":
        return grave_or_town(seed, town=True)
    if kind == "pillars":
        return pillars(seed, fallen=False)
    if kind == "fallen":
        return pillars(seed, fallen=True)
    if kind in {"document", "document_cold"}:
        return document_scene(seed, cold=kind.endswith("cold"))
    if kind == "envelopes":
        return document_scene(seed, cold=False, envelopes=True)
    if kind == "report":
        return document_scene(seed, cold=True, report=True)
    if kind in {"court", "bars", "bars_cold"}:
        return gavel_or_room(seed, courtroom=kind == "court")
    if kind == "chamber":
        return gavel_or_room(seed, chamber=True)
    if kind == "lab":
        return lab_or_grill(seed)
    if kind == "grill":
        return lab_or_grill(seed, grill=True)
    if kind == "conference":
        return lab_or_grill(seed, conference=True)
    return abstract_machine(seed, cold=True)


def asset_names() -> list[str]:
    stills = [f"S{i:03d}" for i in range(1, 151)]
    seeds = [f"M{i:02d}_src" for i in range(1, 31)]
    return stills + seeds


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true", help="overwrite existing images")
    parser.add_argument("--only", default=None, help="single asset id, e.g. S037 or M02_src")
    args = parser.parse_args()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    names = [args.only] if args.only else asset_names()
    rows = []
    for idx, name in enumerate(names, start=1):
        if name not in asset_names():
            raise SystemExit(f"unknown asset id: {name}")
        dest = OUT_DIR / f"{name}.png"
        if dest.exists() and not args.force:
            with Image.open(dest) as im:
                rows.append({"asset": name, "path": str(dest), "skipped": True, "size": im.size, "sha256": sha256(dest)})
            continue
        seed = 510_000 + sum(ord(c) for c in name) * 17 + idx
        im = render(name, seed)
        im.save(dest, compress_level=1)
        rows.append({"asset": name, "path": str(dest), "skipped": False, "size": im.size, "sha256": sha256(dest)})

    receipt = OUT_DIR / "codex_image_generation_receipt.v001.json"
    payload = {
        "schema": "willingham_codex_image_generation.v1",
        "episode": "PD-2026-051-willingham",
        "slug": "willingham",
        "sdxl_used": False,
        "generator": "scripts/generate_willingham_codex_images.py",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "count": len(rows),
        "assets": rows,
    }
    receipt.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"wrote receipt={receipt}")
    print(f"assets={len(rows)} generated={sum(1 for r in rows if not r['skipped'])} skipped={sum(1 for r in rows if r['skipped'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
