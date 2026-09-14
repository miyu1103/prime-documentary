#!/usr/bin/env python3
r"""Build EP27 Rodriguez CTR thumbnails (1280x720) with the proven Kyllo visual system.

Dark navy grade + large white/gold Arial-Black headline + gold-outlined kicker box +
symbolic hero image bleeding from the right + PD monogram + gold underline. Writes 3
options to episodes/PD-2026-027-rodriguez/10_thumbnail/ and copies the selected CTR option
to 09_package/thumbnail.selected.v001.png (>=3 + selected => acceptance gate passes).

    py -3.11 scripts/build_katz_thumbnails_v001.py
"""
from __future__ import annotations
import shutil
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

ROOT = Path(__file__).resolve().parents[1]
W, H = 1280, 720
EP = ROOT / "episodes" / "PD-2026-027-rodriguez"
OUTDIR = EP / "10_thumbnail"
HERO = ROOT / "remotion" / "public" / "rodriguez" / "img" / "COD-S006-patrol-car-behind.png"
LOGO = ROOT / "remotion" / "public" / "pd_logo.png"
FONTS = ROOT / "remotion" / "public" / "fonts"
BLACK = ImageFont.truetype(str(FONTS / "ariblk.ttf"), 128)   # placeholder sizes reset below
BOLD = str(FONTS / "arialbd.ttf")
BLK = str(FONTS / "ariblk.ttf")
GOLD = (232, 178, 58)
WHITE = (245, 245, 245)
NAVY = (8, 14, 30)

# 3 options: (kicker, line1_white, line2_gold, line3_gold_or_None)
OPTIONS = [
    ("2015 · THEN THE DOG ARRIVED", "HOW LONG CAN", "THEY HOLD YOU?", None),      # CTR selected
    ("THE STOP WAS OVER", "THEY KEPT HIM", "ANYWAY", None),                        # tension
    ("A BROKEN TAILLIGHT", "7 EXTRA MINUTES", "WENT TOO FAR", None),               # specificity
]
SELECTED = 0


def fit(draw, text, path, target_px, max_w):
    size = target_px
    while size > 40:
        f = ImageFont.truetype(path, size)
        if draw.textlength(text, font=f) <= max_w:
            return f
        size -= 3
    return ImageFont.truetype(path, size)


def base_bg():
    img = Image.new("RGB", (W, H), NAVY)
    if HERO.exists():
        hero = Image.open(HERO).convert("RGB")
        # cover-fit into full frame, biased so the booth glow sits on the right
        scale = max(W / hero.width, H / hero.height) * 1.06
        hero = hero.resize((int(hero.width * scale), int(hero.height * scale)))
        # crop to keep the right-side subject
        left = hero.width - W
        hero = hero.crop((max(0, left), max(0, (hero.height - H) // 2),
                          max(0, left) + W, max(0, (hero.height - H) // 2) + H))
        hero = ImageEnhance.Brightness(hero).enhance(0.72)
        hero = ImageEnhance.Color(hero).enhance(1.15)
        # navy multiply wash for cohesion
        wash = Image.new("RGB", (W, H), (10, 22, 52))
        hero = Image.blend(hero, wash, 0.30)
        img.paste(hero, (0, 0))
    # left-to-transparent dark gradient so headline reads
    grad = Image.new("L", (W, 1), 0)
    for x in range(W):
        t = max(0.0, 1.0 - x / (W * 0.62))
        grad.putpixel((x, 0), int(238 * (t ** 1.15)))
    grad = grad.resize((W, H))
    shade = Image.new("RGB", (W, H), (4, 8, 20))
    img = Image.composite(shade, img, grad)
    # top & bottom vignette
    vign = Image.new("L", (W, H), 0)
    vd = ImageDraw.Draw(vign)
    vd.rectangle([0, 0, W, 70], fill=110)
    vd.rectangle([0, H - 90, W, H], fill=130)
    img = Image.composite(Image.new("RGB", (W, H), (4, 8, 18)), img, vign.filter(ImageFilter.GaussianBlur(40)))
    return img


def render(idx, kicker, l1, l2, l3, out):
    img = base_bg()
    d = ImageDraw.Draw(img)
    MX = 62
    # kicker box
    kf = ImageFont.truetype(BOLD, 34)
    kw = d.textlength(kicker, font=kf)
    kx0, ky0 = MX, 74
    pad = 18
    d.rectangle([kx0, ky0, kx0 + kw + pad * 2, ky0 + 58], outline=GOLD, width=3)
    d.text((kx0 + pad, ky0 + 11), kicker, font=kf, fill=GOLD)
    # headline (Arial Black, tight leading)
    y = 172
    max_w = int(W * 0.60)
    f1 = fit(d, l1, BLK, 132, max_w)
    f2 = fit(d, l2, BLK, 132, max_w)
    lines = [(l1, f1, WHITE), (l2, f2, GOLD)]
    if l3:
        f3 = fit(d, l3, BLK, 132, max_w)
        lines.append((l3, f3, GOLD))
    for text, f, color in lines:
        asc, desc = f.getmetrics()
        lh = asc + desc
        # soft shadow for legibility
        d.text((MX + 4, y + 5), text, font=f, fill=(0, 0, 0))
        d.text((MX, y), text, font=f, fill=color)
        y += int(lh * 0.86)
    # gold underline bottom-left
    d.rectangle([MX, H - 66, MX + 470, H - 60], fill=GOLD)
    # PD logo bottom-right
    if LOGO.exists():
        logo = Image.open(LOGO).convert("RGBA")
        lw = 116
        logo = logo.resize((lw, int(logo.height * lw / logo.width)))
        img.paste(logo, (W - lw - 44, H - logo.height - 40), logo)
    img.save(out)
    return out


def main():
    OUTDIR.mkdir(parents=True, exist_ok=True)
    made = []
    for i, (k, a, b, c) in enumerate(OPTIONS, start=1):
        out = OUTDIR / f"thumbnail_option_{i:02d}.v001.png"
        render(i, k, a, b, c, out)
        made.append(out)
        print(f"  option {i}: {out.name}  ({k} / {a} {b})")
    sel = OUTDIR / "thumbnail_option_01_ctr.v001.png"
    shutil.copy2(made[SELECTED], sel)
    pkg = EP / "09_package"
    pkg.mkdir(parents=True, exist_ok=True)
    shutil.copy2(made[SELECTED], pkg / "thumbnail.selected.v001.png")
    print(f"selected -> {sel.name} + 09_package/thumbnail.selected.v001.png (option {SELECTED+1})")
    print(f"[rodriguez] {len(made)} options @ 1280x720, selected=YES")


if __name__ == "__main__":
    main()
