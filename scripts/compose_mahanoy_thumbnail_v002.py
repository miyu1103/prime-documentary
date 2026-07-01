#!/usr/bin/env python3
"""Compose stronger Mahanoy YouTube thumbnail candidates.

Uses existing symbolic AI plates and deterministic text/layout so the final
thumbnail is readable and advertiser-safe. No real-person likeness or profanity.
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
EP = ROOT / "episodes" / "PD-2026-011-mahanoy"
OUT = EP / "10_thumbnail"
PKG = EP / "09_package"
AI = Path(r"H:\pd-media\assets\ai\mahanoy")

W, H = 1280, 720
YELLOW = (244, 190, 44)
BLUE = (50, 180, 255)
WHITE = (246, 248, 250)
INK = (2, 7, 13)
RED = (230, 49, 55)


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    paths = [
        Path(r"C:\Windows\Fonts") / name,
        Path(r"C:\Windows\Fonts\arialbd.ttf"),
        Path(r"C:\Windows\Fonts\impact.ttf"),
    ]
    for p in paths:
        if p.exists():
            return ImageFont.truetype(str(p), size)
    return ImageFont.load_default()


F_IMPACT = "impact.ttf"
F_ARIAL_BOLD = "arialbd.ttf"
F_ARIAL = "arial.ttf"


def cover(path: Path, size=(W, H), crop_shift=(0.5, 0.5)) -> Image.Image:
    img = Image.open(path).convert("RGB")
    scale = max(size[0] / img.width, size[1] / img.height)
    nw, nh = int(img.width * scale), int(img.height * scale)
    img = img.resize((nw, nh), Image.Resampling.LANCZOS)
    x = int((nw - size[0]) * crop_shift[0])
    y = int((nh - size[1]) * crop_shift[1])
    return img.crop((x, y, x + size[0], y + size[1]))


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return "sha256:" + h.hexdigest()


def draw_text_with_shadow(
    d: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    text: str,
    fnt: ImageFont.FreeTypeFont,
    fill=WHITE,
    stroke=0,
    stroke_fill=(0, 0, 0),
    shadow=(5, 6),
) -> None:
    x, y = xy
    if shadow:
        d.text((x + shadow[0], y + shadow[1]), text, font=fnt, fill=(0, 0, 0, 210), stroke_width=stroke, stroke_fill=(0, 0, 0))
    d.text((x, y), text, font=fnt, fill=fill, stroke_width=stroke, stroke_fill=stroke_fill)


def fit_font(text: str, max_width: int, start: int, name=F_IMPACT, min_size=56) -> ImageFont.FreeTypeFont:
    size = start
    while size >= min_size:
        fnt = font(name, size)
        bbox = ImageDraw.Draw(Image.new("RGB", (10, 10))).textbbox((0, 0), text, font=fnt, stroke_width=4)
        if bbox[2] - bbox[0] <= max_width:
            return fnt
        size -= 4
    return font(name, min_size)


def add_grade(img: Image.Image) -> Image.Image:
    img = ImageEnhance.Contrast(img).enhance(1.18)
    img = ImageEnhance.Color(img).enhance(1.08)
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    for x in range(W):
        a = int(180 * max(0, 1 - x / 620))
        od.line((x, 0, x, H), fill=(0, 0, 0, a))
    od.rectangle((0, 0, W, H), fill=(0, 0, 0, 36))
    return Image.alpha_composite(img.convert("RGBA"), overlay)


def draw_frame(d: ImageDraw.ImageDraw) -> None:
    d.rectangle((0, 0, W - 1, H - 1), outline=YELLOW, width=4)
    d.rectangle((52, 102, 392, 113), fill=YELLOW)
    d.text((52, 58), "STUDENT SPEECH", font=font(F_ARIAL_BOLD, 34), fill=BLUE)
    d.text((55, 650), "PRIME DOCUMENTARY", font=font(F_ARIAL_BOLD, 24), fill=(224, 230, 236))
    d.ellipse((1173, 620, 1218, 665), outline=YELLOW, width=3)
    d.text((1181, 627), "PD", font=font(F_ARIAL_BOLD, 24), fill=WHITE, stroke_width=1, stroke_fill=(0, 0, 0))
    d.line((1155, 674, 1235, 674), fill=YELLOW, width=3)


def round_rect_mask(size: tuple[int, int], radius: int) -> Image.Image:
    mask = Image.new("L", size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, size[0] - 1, size[1] - 1), radius=radius, fill=255)
    return mask


def draw_phone(base: Image.Image, x: int, y: int, w: int, h: int, tilt_deg: float = -5) -> None:
    phone = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    pd = ImageDraw.Draw(phone)
    pd.rounded_rectangle((0, 0, w - 1, h - 1), radius=44, fill=(6, 12, 20), outline=(235, 187, 60), width=7)
    pd.rounded_rectangle((16, 18, w - 17, h - 17), radius=34, fill=(14, 24, 38), outline=(45, 90, 130), width=2)
    pd.rounded_rectangle((w // 2 - 46, 17, w // 2 + 46, 36), radius=10, fill=(1, 5, 10))
    pd.rectangle((40, 76, w - 40, 118), fill=(35, 125, 255, 80))
    pd.text((52, 81), "OFF CAMPUS", font=font(F_ARIAL_BOLD, 28), fill=(210, 238, 255))
    pd.rounded_rectangle((38, 148, w - 38, 302), radius=20, fill=(239, 243, 246), outline=(255, 255, 255), width=2)
    pd.text((58, 166), "PRIVATE POST", font=font(F_ARIAL_BOLD, 24), fill=(24, 30, 38))
    pd.rounded_rectangle((58, 210, w - 58, 270), radius=12, fill=(18, 24, 32))
    pd.text((83, 221), "CENSORED", font=font(F_ARIAL_BOLD, 38), fill=WHITE)
    pd.line((78, 256, w - 78, 224), fill=RED, width=10)
    pd.line((78, 224, w - 78, 256), fill=RED, width=10)
    pd.rounded_rectangle((54, 335, w - 54, 401), radius=16, fill=(220, 38, 38))
    pd.text((74, 350), "PUNISHED", font=font(F_ARIAL_BOLD, 35), fill=WHITE)
    for i in range(10):
        px = 48 + i * 30
        pd.rectangle((px, 458 + (i % 3) * 18, px + 13, 471 + (i % 3) * 18), fill=(45, 180, 255, 150))
    glow = Image.new("RGBA", phone.size, (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.rounded_rectangle((8, 8, w - 9, h - 9), radius=44, outline=(60, 190, 255, 120), width=8)
    glow = glow.filter(ImageFilter.GaussianBlur(10))
    phone = Image.alpha_composite(glow, phone)
    phone = phone.rotate(tilt_deg, resample=Image.Resampling.BICUBIC, expand=True)
    base.alpha_composite(phone, (x, y))


def draw_scotus_badge(d: ImageDraw.ImageDraw, x: int, y: int, text="8-1 SUPREME COURT") -> None:
    f = font(F_ARIAL_BOLD, 31)
    bbox = d.textbbox((0, 0), text, font=f)
    bw = bbox[2] - bbox[0] + 42
    bh = 58
    d.rounded_rectangle((x, y, x + bw, y + bh), radius=7, fill=(4, 14, 24, 235), outline=YELLOW, width=2)
    d.text((x + 21, y + 13), text, font=f, fill=(226, 235, 244))


def draw_main_lines(d: ImageDraw.ImageDraw, lines: list[tuple[str, tuple[int, int, int], int]], start_y: int) -> int:
    y = start_y
    for text, color, size in lines:
        f = fit_font(text, 690, size)
        draw_text_with_shadow(d, (52, y), text, f, fill=color, stroke=3, stroke_fill=(0, 0, 0), shadow=(6, 7))
        bbox = d.textbbox((52, y), text, font=f, stroke_width=3)
        y = bbox[3] + 2
    return y


def compose(name: str, bg_path: Path, lines: list[tuple[str, tuple[int, int, int], int]], badge: str, phone_pos: tuple[int, int, int, int, float]) -> Path:
    bg = cover(bg_path, crop_shift=(0.45, 0.48))
    base = add_grade(bg)
    d = ImageDraw.Draw(base)
    draw_frame(d)
    end_y = draw_main_lines(d, lines, 154)
    badge_y = min(max(end_y + 16, 496), 548)
    draw_scotus_badge(d, 54, badge_y, badge)
    draw_phone(base, *phone_pos)
    # Red arrow from text to phone punishment stamp.
    d.line((690, 415, 840, 384), fill=RED, width=8)
    d.polygon([(840, 384), (811, 365), (818, 402)], fill=RED)
    out = OUT / name
    out.parent.mkdir(parents=True, exist_ok=True)
    base.convert("RGB").save(out, quality=95, subsampling=0)
    return out


def make_contact_sheet(paths: list[Path]) -> Path:
    thumbs = [Image.open(p).convert("RGB").resize((426, 240), Image.Resampling.LANCZOS) for p in paths]
    sheet = Image.new("RGB", (426 * len(paths), 270), (8, 12, 18))
    d = ImageDraw.Draw(sheet)
    for i, im in enumerate(thumbs):
        sheet.paste(im, (426 * i, 0))
        d.text((426 * i + 16, 244), f"OPTION {chr(65+i)}", font=font(F_ARIAL_BOLD, 22), fill=YELLOW)
    path = OUT / "thumbnail.mahanoy_v002_contact_sheet.jpg"
    sheet.save(path, quality=92)
    return path


def main() -> None:
    variants = [
        (
            "thumbnail.mahanoy_option_A.v002.png",
            AI / "SPN-0012.png",
            [("SUSPENDED", WHITE, 98), ("FOR A", WHITE, 82), ("SNAP?", YELLOW, 98)],
            "8-1 SUPREME COURT",
            (780, 128, 330, 520, -6),
        ),
        (
            "thumbnail.mahanoy_option_B.v002.png",
            AI / "SPN-0012.png",
            [("CAN SCHOOL", WHITE, 93), ("PUNISH", YELLOW, 118), ("YOUR POST?", WHITE, 88)],
            "FIRST AMENDMENT",
            (805, 125, 318, 508, -4),
        ),
        (
            "thumbnail.mahanoy_option_C.v002.png",
            AI / "SPN-0027.png",
            [("OFF CAMPUS", WHITE, 92), ("STILL", WHITE, 94), ("PUNISHED?", YELLOW, 106)],
            "8-1 SUPREME COURT",
            (806, 118, 318, 510, -6),
        ),
    ]
    outputs = [compose(*variant) for variant in variants]
    selected = outputs[0]
    final = PKG / "thumbnail.selected.v002.png"
    final.write_bytes(selected.read_bytes())
    sheet = make_contact_sheet(outputs)
    meta = {
        "episode_id": "PD-2026-011-mahanoy",
        "revision": "v002",
        "status": "selected_for_ctr_update",
        "selected": str(final.relative_to(ROOT)).replace("\\", "/"),
        "selected_sha256": sha256(final),
        "selection_reason": "Option A has the clearest one-second story: punishment + Snap/off-campus post + Supreme Court outcome. It matches the recent series thumbnail grammar with large white/yellow text, dark legal background, right-side symbolic object, badge, and gold frame.",
        "candidates": [
            {
                "id": chr(65 + i),
                "file": str(path.relative_to(ROOT)).replace("\\", "/"),
                "sha256": sha256(path),
            }
            for i, path in enumerate(outputs)
        ],
        "contact_sheet": str(sheet.relative_to(ROOT)).replace("\\", "/"),
        "text_safety": {
            "profanity_displayed": False,
            "post_text": "CENSORED",
            "real_person_likeness": False,
        },
    }
    (PKG / "thumbnail_candidates.v002.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(meta, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
