#!/usr/bin/env python3
r"""EP28 forfeiture FLASHY CTR thumbnails v003 (owner: "サムネは派手に").

Louder than v002: brighter high-contrast hero, a RED radial burst behind the headline,
a GIANT glowing gold "$40" focal graphic (the shock number), XL black-stroked headline,
solid red kicker tag, gold underline, PD mark. 3 options + selected. 1280x720.

    py -3.11 scripts/build_forfeiture_thumbnails_v003.py
"""
from __future__ import annotations
import shutil, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

ROOT = Path(__file__).resolve().parents[1]
W, H = 1280, 720
FONTS = ROOT / "remotion" / "public" / "fonts"
BLK = str(FONTS / "ariblk.ttf")
BOLD = str(FONTS / "arialbd.ttf")
LOGO = ROOT / "remotion" / "public" / "pd_logo.png"
IMG = "remotion/public/forfeiture/img"
GOLD = (255, 196, 48)
WHITE = (252, 252, 252)
RED = (222, 34, 38)

# (hero, focus, kicker, line1 white, line2 gold, big_number)
OPTIONS = [
    (f"{IMG}/PD-2026-028-S005-IMG-001.png", (0.62, 0.42), "$40 OF DRUGS · NO CONVICTION", "THEY TOOK", "THE HOUSE", None),
    (f"{IMG}/PD-2026-028-S032-IMG-001.png", (0.55, 0.50), "NO CHARGE. NO TRIAL.", "THEY CAN TAKE", "YOUR HOUSE", None),
    (f"{IMG}/PD-2026-028-S033-IMG-001.png", (0.45, 0.55), "OVER $40 OF DRUGS", "THEY SEIZED", "A FAMILY'S HOME", None),
]
SELECTED = 0


def fit(d, text, path, target, max_w, floor=54):
    s = target
    while s > floor:
        f = ImageFont.truetype(path, s)
        if d.textlength(text, font=f) <= max_w:
            return f
        s -= 3
    return ImageFont.truetype(path, s)


def build_hero(hero_rel, focus):
    img = Image.new("RGB", (W, H), (8, 12, 22))
    hp = ROOT / hero_rel
    if hp.exists():
        hero = Image.open(hp).convert("RGB")
        sc = max(W / hero.width, H / hero.height) * 1.05
        hero = hero.resize((int(hero.width * sc), int(hero.height * sc)))
        ox, oy = (hero.width - W) // 2, (hero.height - H) // 2
        hero = hero.crop((ox, oy, ox + W, oy + H))
        hero = ImageEnhance.Brightness(hero).enhance(1.28)     # brighter = 派手
        hero = ImageEnhance.Contrast(hero).enhance(1.28)
        hero = ImageEnhance.Color(hero).enhance(1.42)
        img.paste(hero, (0, 0))
        # warm focal glow on the subject
        fx, fy = int(focus[0] * W), int(focus[1] * H)
        glow = Image.new("L", (W, H), 0)
        ImageDraw.Draw(glow).ellipse([fx - 330, fy - 240, fx + 330, fy + 240], fill=120)
        img = Image.composite(Image.new("RGB", (W, H), (255, 240, 205)), img, glow.filter(ImageFilter.GaussianBlur(130)))
    # left scrim
    grad = Image.new("L", (W, 1), 0)
    for x in range(W):
        t = max(0.0, 1.0 - x / (W * 0.64))
        grad.putpixel((x, 0), int(250 * (t ** 1.05)))
    img = Image.composite(Image.new("RGB", (W, H), (2, 5, 14)), img, grad.resize((W, H)))
    # RED radial burst behind the headline (the 派手 pop)
    burst = Image.new("L", (W, H), 0)
    ImageDraw.Draw(burst).ellipse([-220, 150, 760, 700], fill=120)
    img = Image.composite(Image.new("RGB", (W, H), RED), img, burst.filter(ImageFilter.GaussianBlur(160)))
    # bottom scrim
    bs = Image.new("L", (W, H), 0)
    ImageDraw.Draw(bs).rectangle([0, H - 150, W, H], fill=170)
    img = Image.composite(Image.new("RGB", (W, H), (2, 5, 12)), img, bs.filter(ImageFilter.GaussianBlur(55)))
    return img


def render(o, out):
    hero, focus, kicker, l1, l2, num = o
    img = build_hero(hero, focus)
    d = ImageDraw.Draw(img)
    MX = 58
    # giant glowing $number (shock focal) upper-right
    if num:
        nf = ImageFont.truetype(BLK, 300)
        nw = d.textlength(num, font=nf)
        nx, ny = W - nw - 70, 40
        gl = Image.new("L", (W, H), 0)
        ImageDraw.Draw(gl).text((nx, ny), num, font=nf, fill=255)
        img.paste(Image.new("RGB", (W, H), GOLD), (0, 0), gl.filter(ImageFilter.GaussianBlur(26)))
        d = ImageDraw.Draw(img)
        d.text((nx, ny), num, font=nf, fill=GOLD, stroke_width=8, stroke_fill=(0, 0, 0))
    # red kicker tag
    kf = ImageFont.truetype(BLK, 36)
    kw = d.textlength(kicker, font=kf)
    d.rectangle([MX, 60, MX + kw + 40, 128], fill=RED)
    d.text((MX + 20, 71), kicker, font=kf, fill=WHITE)
    # XL headline, thick stroke
    y = 176
    mw = int(W * 0.70)
    for text, color in [(l1, WHITE), (l2, GOLD)]:
        f = fit(d, text, BLK, 168, mw)
        asc, desc = f.getmetrics()
        d.text((MX, y), text, font=f, fill=color, stroke_width=10, stroke_fill=(0, 0, 0))
        y += int((asc + desc) * 0.82)
    d.rectangle([MX, min(y + 8, H - 92), MX + 470, min(y + 18, H - 82)], fill=GOLD)
    if LOGO.exists():
        logo = Image.open(LOGO).convert("RGBA")
        lw = 122
        logo = logo.resize((lw, int(logo.height * lw / logo.width)))
        img.paste(logo, (W - lw - 40, H - logo.height - 34), logo)
    img.save(out)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    outdir = ROOT / "episodes" / "PD-2026-028-forfeiture" / "10_thumbnail"
    outdir.mkdir(parents=True, exist_ok=True)
    made = []
    for i, o in enumerate(OPTIONS, 1):
        out = outdir / f"thumbnail_option_{i:02d}.v003.png"
        render(o, out)
        made.append(out)
        print(f"  option {i}: {out.name}  ({o[2]} / {o[3]} {o[4]}{' + '+o[5] if o[5] else ''})")
    sel = outdir / "thumbnail_ctr.v003.png"
    shutil.copy2(made[SELECTED], sel)
    pkg = ROOT / "episodes" / "PD-2026-028-forfeiture" / "09_package"
    shutil.copy2(made[SELECTED], pkg / "thumbnail.selected.v003.png")
    print(f"selected -> option {SELECTED+1} + 09_package/thumbnail.selected.v003.png")


if __name__ == "__main__":
    main()
