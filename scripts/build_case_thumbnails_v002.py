#!/usr/bin/env python3
r"""High-CTR v002 thumbnails for the EP25-27 legal series (1280x720).

Rebuild after owner feedback (2026-07-04): v001 read as too dark / low-visibility / "しょぼい".
v002 upgrades: brighter high-contrast/saturated hero (no flat-navy), a focal glow on the
subject, XL headline with a thick BLACK stroke (reads on any background + on mobile), a bold
RED kicker tag (highest-attention color) instead of a thin gold outline, and a heavier bottom
scrim. Writes options + selected per episode.

    py -3.11 scripts/build_case_thumbnails_v002.py --ep katz|rodriguez|kyllo
"""
from __future__ import annotations
import argparse, shutil, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

ROOT = Path(__file__).resolve().parents[1]
W, H = 1280, 720
FONTS = ROOT / "remotion" / "public" / "fonts"
BLK = str(FONTS / "ariblk.ttf")
BOLD = str(FONTS / "arialbd.ttf")
LOGO = ROOT / "remotion" / "public" / "pd_logo.png"
GOLD = (245, 190, 60)
WHITE = (250, 250, 250)
RED = (210, 38, 40)

# per-episode: hero, focus (cx,cy as 0..1 for the glow), kicker, line1(white), line2(gold)
CONFIG = {
    "kyllo": {
        "ep": "PD-2026-025-kyllo",
        "hero": "remotion/public/kyllo/img/COD-S019-heat-reveals-presence.png",
        "focus": (0.70, 0.55),
        "kicker": "NO WARRANT",
        "line1": "THEY SAW",
        "line2": "INSIDE YOUR HOME",
    },
    "katz": {
        "ep": "PD-2026-026-katz",
        "hero": "remotion/public/katz/img/COD-S001-booth-glow-night.png",
        "focus": (0.62, 0.52),
        "kicker": "THE FBI WAS LISTENING",
        "line1": "THEY RECORDED",
        "line2": "EVERY WORD",
    },
    "rodriguez": {
        "ep": "PD-2026-027-rodriguez",
        "hero": "remotion/public/rodriguez/img/COD-S006-patrol-car-behind.png",
        "focus": (0.34, 0.60),
        "kicker": "STOPPED. THEN HELD.",
        "line1": "HOW LONG CAN",
        "line2": "THEY HOLD YOU?",
    },
}


def fit(draw, text, path, target_px, max_w, min_px=54):
    size = target_px
    while size > min_px:
        f = ImageFont.truetype(path, size)
        if draw.textlength(text, font=f) <= max_w:
            return f
        size -= 3
    return ImageFont.truetype(path, size)


def stroked(d, xy, text, font, fill, stroke=(0, 0, 0), sw=8):
    d.text(xy, text, font=font, fill=fill, stroke_width=sw, stroke_fill=stroke)


def build_hero(cfg):
    img = Image.new("RGB", (W, H), (10, 14, 26))
    hero_p = ROOT / cfg["hero"]
    if hero_p.exists():
        hero = Image.open(hero_p).convert("RGB")
        scale = max(W / hero.width, H / hero.height) * 1.04
        hero = hero.resize((int(hero.width * scale), int(hero.height * scale)))
        ox = (hero.width - W) // 2
        oy = (hero.height - H) // 2
        hero = hero.crop((ox, oy, ox + W, oy + H))
        # brighter + punchier than v001 (which was too dark)
        hero = ImageEnhance.Brightness(hero).enhance(1.16)
        hero = ImageEnhance.Contrast(hero).enhance(1.20)
        hero = ImageEnhance.Color(hero).enhance(1.30)
        img.paste(hero, (0, 0))
        # focal glow: lift the subject so the eye lands there
        fx, fy = int(cfg["focus"][0] * W), int(cfg["focus"][1] * H)
        glow = Image.new("L", (W, H), 0)
        gd = ImageDraw.Draw(glow)
        gd.ellipse([fx - 300, fy - 220, fx + 300, fy + 220], fill=90)
        glow = glow.filter(ImageFilter.GaussianBlur(120))
        img = Image.composite(Image.new("RGB", (W, H), (255, 244, 214)), img, glow)
    # left scrim so headline reads (gradient dark -> clear)
    grad = Image.new("L", (W, 1), 0)
    for x in range(W):
        t = max(0.0, 1.0 - x / (W * 0.66))
        grad.putpixel((x, 0), int(250 * (t ** 1.08)))
    grad = grad.resize((W, H))
    img = Image.composite(Image.new("RGB", (W, H), (3, 6, 16)), img, grad)
    # heavier bottom scrim
    bs = Image.new("L", (W, H), 0)
    bd = ImageDraw.Draw(bs)
    bd.rectangle([0, H - 150, W, H], fill=180)
    img = Image.composite(Image.new("RGB", (W, H), (3, 6, 14)), img, bs.filter(ImageFilter.GaussianBlur(55)))
    return img


def render(cfg, out):
    img = build_hero(cfg)
    d = ImageDraw.Draw(img)
    MX = 60
    # RED kicker tag (solid, high attention)
    kf = ImageFont.truetype(BLK, 34)
    kw = d.textlength(cfg["kicker"], font=kf)
    pad = 20
    ky = 66
    d.rectangle([MX, ky, MX + kw + pad * 2, ky + 60], fill=RED)
    d.text((MX + pad, ky + 11), cfg["kicker"], font=kf, fill=WHITE)
    # XL headline, thick black stroke
    max_w = int(W * 0.66)
    y = 168
    f1 = fit(d, cfg["line1"], BLK, 150, max_w)
    f2 = fit(d, cfg["line2"], BLK, 150, max_w)
    for text, f, color in [(cfg["line1"], f1, WHITE), (cfg["line2"], f2, GOLD)]:
        asc, desc = f.getmetrics()
        stroked(d, (MX, y), text, f, color, sw=9)
        y += int((asc + desc) * 0.84)
    # gold underline accent
    d.rectangle([MX, min(y + 6, H - 96), MX + 430, min(y + 15, H - 87)], fill=GOLD)
    # PD logo bottom-right
    if LOGO.exists():
        logo = Image.open(LOGO).convert("RGBA")
        lw = 120
        logo = logo.resize((lw, int(logo.height * lw / logo.width)))
        img.paste(logo, (W - lw - 42, H - logo.height - 36), logo)
    img.save(out)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--ep", required=True, choices=sorted(CONFIG))
    args = ap.parse_args()
    cfg = CONFIG[args.ep]
    outdir = ROOT / "episodes" / cfg["ep"] / "10_thumbnail"
    outdir.mkdir(parents=True, exist_ok=True)
    out = outdir / "thumbnail_ctr.v002.png"
    render(cfg, out)
    print(f"[{args.ep}] wrote {out.relative_to(ROOT)}  ({cfg['kicker']} / {cfg['line1']} {cfg['line2']})")


if __name__ == "__main__":
    main()
