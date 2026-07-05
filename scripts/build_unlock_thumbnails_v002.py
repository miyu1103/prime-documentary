#!/usr/bin/env python3
"""EP31 thumbnails v002 — 派手 (loud/high-CTR) pass.

Same headlines/backgrounds as v001, but punchier: neon glow behind the headline,
bigger type, a radial accent burst behind the subject, and stronger brightness/
contrast/saturation. Outputs >=3 @1280x720 + a selected (acceptance thumbnail_*).
No real-person likeness (backgrounds are faceless).
"""
from __future__ import annotations

import hashlib
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-031-unlock"
EPDIR = ROOT / "episodes" / EP
BG_DIR = Path(r"H:\pd-media\episodes\PD-2026-031-unlock\10_thumbnail\backgrounds")
OUT = EPDIR / "10_thumbnail"
PKG = EPDIR / "09_package"
W, H = 1280, 720
GOLD = (255, 196, 44)
BLUE = (46, 130, 255)
WHITE = (250, 251, 255)
IMPACT = Path(r"C:\Windows\Fonts\impact.ttf")

# (candidate, bg, [(line, fill, glow)], burst_color, burst_xy)
CANDS = [
    ("A", "PD-2026-031-THUMB-T1.png",
     [("THEY CAN FORCE", WHITE, BLUE), ("YOUR THUMB", GOLD, GOLD)], BLUE, (0.62, 0.62)),
    ("B", "PD-2026-031-THUMB-T3.png",
     [("YOUR PASSCODE", GOLD, GOLD), ("> FACE ID", BLUE, BLUE)], GOLD, (0.72, 0.55)),
    ("C", "PD-2026-031-THUMB-T2.png",
     [("FACE ID =", WHITE, BLUE), ("NO RIGHTS?", GOLD, GOLD)], BLUE, (0.30, 0.42)),
]
SELECTED = "A"


def font(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(IMPACT), size=size)


def sha(p: Path) -> str:
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


def radial_burst(base: Image.Image, color, cx, cy, radius=430, strength=150) -> Image.Image:
    """A bright accent glow behind the subject to make it pop."""
    glow = Image.new("RGB", (W, H), (0, 0, 0))
    d = ImageDraw.Draw(glow)
    d.ellipse([cx - radius, cy - radius, cx + radius, cy + radius], fill=color)
    glow = glow.filter(ImageFilter.GaussianBlur(radius // 2))
    glow = ImageEnhance.Brightness(glow).enhance(strength / 255)
    return Image.blend(base, ImageChops_screen(base, glow), 0.55)


def ImageChops_screen(a, b):
    from PIL import ImageChops
    return ImageChops.screen(a, b)


def scrim(img: Image.Image) -> Image.Image:
    ov = Image.new("L", (W, H), 0)
    px = ov.load()
    for x in range(W):
        t = 1 - (x / W)
        a = int(140 * max(0.0, t) ** 1.2)
        for y in range(H):
            px[x, y] = a
    return Image.composite(Image.new("RGB", (W, H), (3, 6, 16)), img, ov)


def draw_headline(base: Image.Image, lines) -> Image.Image:
    d0 = ImageDraw.Draw(base)
    size = 190
    fnt = font(size)
    longest = max(lines, key=lambda l: d0.textlength(l[0], font=font(180)))[0]
    while d0.textlength(longest, font=fnt) > W * 0.72 and size > 96:
        size -= 4
        fnt = font(size)
    lh = int(size * 1.0)
    y = (H - lh * len(lines)) // 2
    x = 60
    for text, fill, glow_c in lines:
        # neon glow layer (accent color, blurred)
        gl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        gd = ImageDraw.Draw(gl)
        gd.text((x, y), text, font=fnt, fill=glow_c + (255,), stroke_width=6, stroke_fill=glow_c + (255,))
        gl = gl.filter(ImageFilter.GaussianBlur(16))
        base.paste(Image.new("RGB", (W, H), glow_c), (0, 0), gl.split()[3].point(lambda a: int(a * 0.9)))
        # hard shadow + heavy stroke + fill
        d = ImageDraw.Draw(base)
        d.text((x + 6, y + 8), text, font=fnt, fill=(0, 0, 0), stroke_width=16, stroke_fill=(0, 0, 0))
        d.text((x, y), text, font=fnt, fill=fill, stroke_width=11, stroke_fill=(0, 0, 0))
        y += lh
    return base


def build(cand, bgfile, lines, burst_c, burst_xy) -> Path:
    bg = cover(Image.open(BG_DIR / bgfile))
    bg = radial_burst(bg, burst_c, int(W * burst_xy[0]), int(H * burst_xy[1]))
    bg = scrim(bg)
    bg = draw_headline(bg, lines)
    # 派手 grade: punchy brightness/contrast/saturation
    bg = ImageEnhance.Color(bg).enhance(1.35)
    bg = ImageEnhance.Contrast(bg).enhance(1.18)
    bg = ImageEnhance.Brightness(bg).enhance(1.14)
    OUT.mkdir(parents=True, exist_ok=True)
    p = OUT / f"thumbnail.unlock_option_{cand}.v002.png"
    bg.save(p, "PNG")
    return p


def main() -> int:
    made = {}
    for cand, bgfile, lines, bc, bxy in CANDS:
        made[cand] = build(cand, bgfile, lines, bc, bxy)
        print("wrote", made[cand].name)
    PKG.mkdir(parents=True, exist_ok=True)
    dst = PKG / "thumbnail.selected.v002.png"
    shutil.copy2(made[SELECTED], dst)
    print("selected:", SELECTED, "->", dst.name, sha(dst)[:23])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
