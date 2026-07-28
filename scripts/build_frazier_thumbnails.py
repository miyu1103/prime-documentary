#!/usr/bin/env python3
"""Create EP39 Frazier thumbnail concept PNGs.

Local deterministic thumbnails only; no external assets and no real-person likeness.
"""
from __future__ import annotations

import json
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageStat

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "episodes" / "PD-2026-039-frazier" / "09_package"
W, H = 1280, 720
INK = (5, 8, 14)
NAVY = (11, 26, 43)
BLUE = (31, 107, 255)
GOLD = (229, 181, 58)
WHITE = (245, 247, 250)
SILVER = (200, 205, 214)


def font(size: int, bold: bool = True) -> ImageFont.ImageFont:
    names = ["C:/Windows/Fonts/arialbd.ttf", "C:/Windows/Fonts/arial.ttf"] if bold else ["C:/Windows/Fonts/arial.ttf"]
    for n in names:
        p = Path(n)
        if p.exists():
            return ImageFont.truetype(str(p), size)
    return ImageFont.load_default()


def draw_title(d: ImageDraw.ImageDraw, text: str, y: int, color=WHITE) -> None:
    f = font(94)
    words = text.split()
    lines = []
    cur = ""
    for w in words:
        test = (cur + " " + w).strip()
        if d.textlength(test, font=f) <= 1120:
            cur = test
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    for i, line in enumerate(lines[:2]):
        bbox = d.textbbox((0, 0), line, font=f, stroke_width=7)
        x = (W - (bbox[2] - bbox[0])) / 2
        d.text((x, y + i * 96), line, font=f, fill=color, stroke_width=7, stroke_fill=(0, 0, 0))


def background() -> Image.Image:
    img = Image.new("RGB", (W, H), INK)
    px = img.load()
    for y in range(H):
        for x in range(W):
            t = x / W
            v = int(10 + 18 * (1 - y / H))
            px[x, y] = (int(NAVY[0] * (1 - t) + INK[0] * t) + v // 8, int(NAVY[1] * (1 - t) + INK[1] * t) + v // 10, int(NAVY[2] * (1 - t) + INK[2] * t) + v)
    return img


def thumb1(path: Path) -> None:
    img = background()
    d = ImageDraw.Draw(img)
    d.rectangle((130, 140, 980, 470), fill=(238, 238, 226), outline=SILVER, width=5)
    for i in range(12):
        y = 178 + i * 20
        d.line((190, y, 900, y), fill=(170, 170, 160), width=3)
    d.rectangle((0, 520, W, H), fill=(0, 0, 0))
    d.rectangle((90, 170, 330, 650), fill=(45, 34, 28))
    d.rounded_rectangle((60, 112, 420, 235), radius=40, fill=(175, 135, 90))
    d.line((390, 252, 1000, 132), fill=GOLD, width=18)
    d.text((318, 232), "FAKE", font=font(120), fill=(170, 20, 18), stroke_width=4, stroke_fill=(70, 0, 0))
    draw_title(d, "POLICE CAN LIE", 540, GOLD)
    img.save(path)


def thumb2(path: Path) -> None:
    img = background()
    d = ImageDraw.Draw(img)
    d.ellipse((430, 160, 850, 600), fill=(201, 150, 118))
    d.rectangle((0, 0, W, 270), fill=NAVY)
    d.rectangle((0, 500, W, H), fill=INK)
    d.rounded_rectangle((700, 100, 1180, 320), radius=36, fill=WHITE)
    d.polygon([(790, 320), (740, 390), (860, 320)], fill=WHITE)
    d.text((748, 165), "I DID IT", font=font(72), fill=INK)
    d.line((650, 370, 910, 370), fill=GOLD, width=12)
    d.line((775, 350, 795, 390), fill=INK, width=9)
    draw_title(d, "I DIDN'T DO IT", 540, WHITE)
    img.save(path)


def thumb3(path: Path) -> None:
    img = background()
    d = ImageDraw.Draw(img)
    d.ellipse((70, 80, 620, 630), fill=(16, 24, 36), outline=BLUE, width=12)
    for angle in range(0, 360, 18):
        import math

        x1 = 345 + 190 * math.cos(math.radians(angle))
        y1 = 355 + 190 * math.sin(math.radians(angle))
        x2 = 345 + 242 * math.cos(math.radians(angle))
        y2 = 355 + 242 * math.sin(math.radians(angle))
        d.line((x1, y1, x2, y2), fill=SILVER, width=4)
    for angle in (5, 35, 82, 143, 210, 286):
        import math

        d.line((345, 355, 345 + 205 * math.cos(math.radians(angle)), 355 + 205 * math.sin(math.radians(angle))), fill=BLUE, width=7)
    d.rectangle((760, 95, 1135, 630), fill=(45, 50, 58), outline=SILVER, width=8)
    d.rectangle((840, 220, 1055, 380), fill=(18, 24, 32), outline=BLUE, width=5)
    d.rectangle((625, 330, 745, 350), fill=WHITE)
    draw_title(d, "NO ONE COMING", 540, WHITE)
    img.save(path)


def score(path: Path) -> dict:
    img = Image.open(path).convert("L")
    small = img.resize((320, 180))
    return {
        "file": path.name,
        "mean_luma": round(ImageStat.Stat(img).mean[0], 2),
        "small_contrast": round(ImageStat.Stat(small).stddev[0], 2),
    }


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    paths = [OUT / "thumbnail.v001-01.png", OUT / "thumbnail.v001-02.png", OUT / "thumbnail.v001-03.png"]
    thumb1(paths[0])
    print(f"saved {paths[0]}")
    thumb2(paths[1])
    print(f"saved {paths[1]}")
    thumb3(paths[2])
    print(f"saved {paths[2]}")
    selected = OUT / "thumbnail.selected.v001.png"
    shutil.copy2(paths[0], selected)
    print(f"saved {selected}")
    report = {"episode_id": "PD-2026-039-frazier", "selected": selected.name, "visibility": [score(p) for p in [*paths, selected]]}
    (OUT / "thumbnail_visibility.stub.v001.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
