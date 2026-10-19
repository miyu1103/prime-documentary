#!/usr/bin/env python3
"""EP31 (PD-2026-031-unlock) thumbnails: headline over Codex background art.

Composites short UPPERCASE headlines (thumb_prompts.v001) onto the 5 generated
1280x720 background arts, with a legibility scrim, heavy stroke + shadow, and ONE
accent color (gold #E5B53A or electric #1F6BFF). Outputs >=3 candidates to
10_thumbnail/ and a selected to 09_package/ (acceptance thumbnail_ready /
thumbnail_visibility). No real-person likeness (backgrounds are faceless).
"""
from __future__ import annotations

import hashlib
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFont

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-031-unlock"
EPDIR = ROOT / "episodes" / EP
BG_DIR = Path(r"E:\pd-media\episodes\PD-2026-031-unlock\10_thumbnail\backgrounds")
OUT = EPDIR / "10_thumbnail"
PKG = EPDIR / "09_package"
W, H = 1280, 720
GOLD = (229, 181, 58)
BLUE = (31, 107, 255)
WHITE = (245, 247, 250)

IMPACT = Path(r"C:\Windows\Fonts\impact.ttf")

# (candidate, background file, [(line, accent_color_or_None)], anchor)
CANDS = [
    ("A", "PD-2026-031-THUMB-T1.png", [("THEY CAN FORCE", None), ("YOUR THUMB", GOLD)], "left"),
    ("B", "PD-2026-031-THUMB-T3.png", [("YOUR PASSCODE", GOLD), ("> FACE ID", BLUE)], "left"),
    ("C", "PD-2026-031-THUMB-T2.png", [("FACE ID =", None), ("NO RIGHTS?", GOLD)], "left"),
]
SELECTED = "A"


def font(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(IMPACT), size=size)


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return "sha256:" + h.hexdigest()


def cover(img: Image.Image) -> Image.Image:
    img = img.convert("RGB")
    s = max(W / img.width, H / img.height)
    img = img.resize((round(img.width * s), round(img.height * s)), Image.LANCZOS)
    x = (img.width - W) // 2
    y = (img.height - H) // 2
    return img.crop((x, y, x + W, y + H))


def scrim(img: Image.Image, side: str) -> Image.Image:
    """Left-to-right dark gradient so headline stays legible on any art."""
    ov = Image.new("L", (W, H), 0)
    px = ov.load()
    for x in range(W):
        t = 1 - (x / W) if side == "left" else (x / W)
        a = int(150 * max(0.0, t) ** 1.15)
        for y in range(H):
            px[x, y] = a
    black = Image.new("RGB", (W, H), (4, 8, 18))
    return Image.composite(black, img, ov)


def draw_line(d: ImageDraw.ImageDraw, xy, text, fnt, fill):
    x, y = xy
    # drop shadow + heavy stroke for pop at 320px
    d.text((x + 6, y + 7), text, font=fnt, fill=(0, 0, 0),
           stroke_width=14, stroke_fill=(0, 0, 0))
    d.text((x, y), text, font=fnt, fill=fill,
           stroke_width=10, stroke_fill=(0, 0, 0))


def build(cand, bgfile, lines, anchor) -> Path:
    bg = cover(Image.open(BG_DIR / bgfile))
    bg = scrim(bg, anchor)
    d = ImageDraw.Draw(bg)
    # fit font so the longest line spans ~62% width
    size = 168
    fnt = font(size)
    longest = max(lines, key=lambda l: d.textlength(l[0], font=font(160)))[0]
    while d.textlength(longest, font=fnt) > W * 0.62 and size > 90:
        size -= 4
        fnt = font(size)
    lh = int(size * 1.02)
    total = lh * len(lines)
    y = (H - total) // 2
    x = 70
    for text, accent in lines:
        draw_line(d, (x, y), text, fnt, accent or WHITE)
        y += lh
    # lift overall brightness so the thumbnail reads bright/punchy (visibility gate)
    bg = ImageEnhance.Brightness(bg).enhance(1.16)
    bg = ImageEnhance.Contrast(bg).enhance(1.05)
    OUT.mkdir(parents=True, exist_ok=True)
    p = OUT / f"thumbnail.unlock_option_{cand}.v001.png"
    bg.save(p, "PNG")
    return p


def main() -> int:
    made = []
    for cand, bgfile, lines, anchor in CANDS:
        made.append((cand, build(cand, bgfile, lines, anchor)))
        print("wrote", made[-1][1].name)
    PKG.mkdir(parents=True, exist_ok=True)
    sel = dict(made)[SELECTED]
    dst = PKG / "thumbnail.selected.v001.png"
    shutil.copy2(sel, dst)
    print("selected:", SELECTED, "->", dst.name, sha256(dst)[:23])
    print(f"{len(made)} candidates @ {W}x{H} in 10_thumbnail/ + selected in 09_package/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
