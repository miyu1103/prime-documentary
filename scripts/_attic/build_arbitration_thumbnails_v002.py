#!/usr/bin/env python3
"""Build punchier v002 arbitration thumbnail candidates.

The v001 thumbnail was too dark and explanatory. v002 uses short text, stronger
contrast, and a single clear legal-rights visual metaphor with no real people or
judge likeness.
"""
from __future__ import annotations

import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-012-arbitration"
EPDIR = ROOT / "episodes" / EP
OUT = EPDIR / "10_thumbnail"
PKG = EPDIR / "09_package"
W, H = 1280, 720

FONT_IMPACT = Path(r"C:\Windows\Fonts\impact.ttf")
FONT_ARIAL_BOLD = Path(r"C:\Windows\Fonts\arialbd.ttf")
FONT_ARIAL = Path(r"C:\Windows\Fonts\arial.ttf")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return "sha256:" + h.hexdigest()


def font(path: Path, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(path), size=size)


def gradient(bg1: tuple[int, int, int], bg2: tuple[int, int, int]) -> Image.Image:
    im = Image.new("RGB", (W, H), bg1)
    px = im.load()
    for y in range(H):
        for x in range(W):
            t = (x / W * 0.7 + y / H * 0.3)
            px[x, y] = tuple(int(bg1[i] * (1 - t) + bg2[i] * t) for i in range(3))
    return im


def add_vignette(im: Image.Image) -> Image.Image:
    mask = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(mask)
    for r in range(0, 900, 12):
        alpha = max(0, min(255, int((r - 150) * 0.33)))
        d.ellipse((W // 2 - r, H // 2 - r, W // 2 + r, H // 2 + r), outline=alpha, width=14)
    mask = ImageOps.invert(mask.filter(ImageFilter.GaussianBlur(34)))
    dark = Image.new("RGB", (W, H), (0, 0, 0))
    return Image.composite(dark, im, mask.point(lambda v: int(v * 0.52)))


def glow(draw: ImageDraw.ImageDraw, xy: tuple[int, int, int, int], color: tuple[int, int, int], width: int = 10) -> None:
    for i in range(width, 0, -2):
        a = i / width
        draw.rounded_rectangle(xy, radius=24, outline=tuple(int(c * a) for c in color), width=i)


def draw_contract(draw: ImageDraw.ImageDraw, x: int, y: int, w: int, h: int, *, angle: float = -7) -> Image.Image:
    sheet = Image.new("RGBA", (w, h), (232, 225, 200, 255))
    sd = ImageDraw.Draw(sheet)
    sd.rectangle((0, 0, w - 1, h - 1), outline=(20, 20, 20, 255), width=5)
    sd.rectangle((24, 22, w - 24, 78), fill=(32, 32, 32, 255))
    sd.text((36, 32), "TERMS", fill=(255, 234, 136, 255), font=font(FONT_IMPACT, 42))
    for i in range(10):
        yy = 112 + i * 34
        length = int(w * (0.82 - (i % 3) * 0.11))
        sd.rectangle((35, yy, 35 + length, yy + 12), fill=(96, 87, 70, 255))
    sd.rounded_rectangle((42, h - 116, w - 46, h - 38), radius=16, fill=(10, 10, 10, 255))
    sd.text((70, h - 102), "I AGREE", fill=(255, 222, 40, 255), font=font(FONT_IMPACT, 58))
    rotated = sheet.rotate(angle, expand=True, resample=Image.Resampling.BICUBIC)
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    canvas.alpha_composite(rotated, (x, y))
    return canvas


def draw_stamp(base: Image.Image, text: str, center: tuple[int, int], angle: float = -14, scale: float = 1.0) -> None:
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    f = font(FONT_IMPACT, int(118 * scale))
    bbox = d.textbbox((0, 0), text, font=f, stroke_width=4)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    pad_x, pad_y = int(38 * scale), int(24 * scale)
    rect = (center[0] - tw // 2 - pad_x, center[1] - th // 2 - pad_y, center[0] + tw // 2 + pad_x, center[1] + th // 2 + pad_y)
    for off in range(10, 0, -2):
        d.rounded_rectangle(tuple(v + (off if i in (0, 1) else -off) for i, v in enumerate(rect)), radius=22, outline=(255, 0, 0, 24), width=8)
    d.rounded_rectangle(rect, radius=22, outline=(255, 32, 24, 255), width=int(12 * scale))
    d.text((center[0] - tw // 2, center[1] - th // 2 - 8), text, font=f, fill=(255, 32, 24, 255), stroke_width=5, stroke_fill=(30, 0, 0, 255))
    layer = layer.rotate(angle, center=center, resample=Image.Resampling.BICUBIC)
    base.alpha_composite(layer)


def draw_chain(draw: ImageDraw.ImageDraw, y: int, x0: int, x1: int, color: tuple[int, int, int]) -> None:
    draw.line((x0, y, x1, y), fill=(25, 18, 5), width=34)
    for x in range(x0 + 14, x1, 72):
        draw.ellipse((x - 34, y - 24, x + 34, y + 24), outline=color, width=13)
        draw.ellipse((x - 22, y - 13, x + 22, y + 13), outline=(255, 224, 90), width=5)


def text_block(base: Image.Image, lines: list[str], x: int, y: int, sizes: list[int], fills: list[tuple[int, int, int]], stroke: int = 9) -> None:
    d = ImageDraw.Draw(base)
    yy = y
    for line, size, fill in zip(lines, sizes, fills):
        f = font(FONT_IMPACT, size)
        d.text((x + 9, yy + 11), line, font=f, fill=(0, 0, 0), stroke_width=stroke + 4, stroke_fill=(0, 0, 0))
        d.text((x, yy), line, font=f, fill=fill, stroke_width=stroke, stroke_fill=(0, 0, 0))
        yy += int(size * 0.86)


def draw_pd_badge(base: Image.Image) -> None:
    d = ImageDraw.Draw(base)
    x, y = 1170, 626
    d.ellipse((x, y, x + 58, y + 58), fill=(6, 8, 14), outline=(255, 213, 48), width=5)
    d.text((x + 14, y + 11), "PD", font=font(FONT_IMPACT, 30), fill=(255, 255, 255))


def option_a() -> Image.Image:
    im = gradient((8, 8, 11), (55, 3, 3)).convert("RGBA")
    layer = draw_contract(ImageDraw.Draw(im), 730, 80, 420, 520, angle=8)
    im.alpha_composite(layer)
    d = ImageDraw.Draw(im)
    draw_chain(d, 365, 720, 1240, (190, 120, 12))
    draw_stamp(im, "DENIED", (920, 270), angle=-15, scale=0.95)
    d.polygon([(0, 0), (650, 0), (555, H), (0, H)], fill=(0, 0, 0, 175))
    d.rectangle((0, 590, W, 720), fill=(0, 0, 0, 118))
    text_block(im, ["YOU", "CAN'T", "SUE"], 54, 104, [154, 156, 160], [(255, 255, 255), (255, 216, 24), (255, 255, 255)], stroke=10)
    d.rounded_rectangle((70, 594, 475, 657), radius=10, fill=(255, 30, 22), outline=(255, 242, 150), width=3)
    d.text((96, 601), "FINE PRINT", fill=(255, 255, 255), font=font(FONT_IMPACT, 52), stroke_width=4, stroke_fill=(0, 0, 0))
    draw_pd_badge(im)
    return add_vignette(im.convert("RGB")).convert("RGBA")


def option_b() -> Image.Image:
    im = gradient((2, 12, 22), (130, 4, 0)).convert("RGBA")
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((720, 86, 1180, 560), radius=38, fill=(8, 10, 12), outline=(255, 255, 255), width=9)
    d.rounded_rectangle((758, 132, 1142, 246), radius=18, fill=(255, 216, 26), outline=(0, 0, 0), width=6)
    d.text((812, 147), "I AGREE", fill=(0, 0, 0), font=font(FONT_IMPACT, 76))
    d.line((706, 418, 1218, 288), fill=(255, 32, 20), width=42)
    d.line((706, 418, 1218, 288), fill=(255, 224, 48), width=12)
    draw_chain(d, 386, 690, 1220, (210, 120, 8))
    draw_stamp(im, "LOCKED", (910, 455), angle=-9, scale=0.75)
    d.polygon([(0, 0), (676, 0), (594, H), (0, H)], fill=(0, 0, 0, 188))
    text_block(im, ["I AGREE", "NO COURT?"], 44, 126, [142, 142], [(255, 255, 255), (255, 34, 24)], stroke=10)
    d.rounded_rectangle((56, 598, 530, 660), radius=8, fill=(255, 218, 24), outline=(0, 0, 0), width=5)
    d.text((85, 604), "TAP ONCE", fill=(0, 0, 0), font=font(FONT_IMPACT, 52))
    draw_pd_badge(im)
    return add_vignette(im.convert("RGB")).convert("RGBA")


def option_c() -> Image.Image:
    im = gradient((11, 8, 18), (94, 0, 0)).convert("RGBA")
    d = ImageDraw.Draw(im)
    for i in range(16):
        x = 688 + i * 30
        y = 88 + int(math.sin(i) * 16)
        d.rectangle((x, y, x + 18, 520), fill=(240, 230, 200, 150))
    layer = draw_contract(d, 725, 74, 390, 540, angle=-8)
    im.alpha_composite(layer)
    draw_stamp(im, "TRAPPED", (926, 320), angle=10, scale=0.76)
    d.line((690, 118, 1160, 555), fill=(255, 226, 29), width=24)
    d.line((720, 126, 1188, 556), fill=(0, 0, 0), width=7)
    d.polygon([(0, 0), (690, 0), (570, H), (0, H)], fill=(0, 0, 0, 184))
    text_block(im, ["FINE", "PRINT", "TRAP"], 52, 78, [154, 154, 154], [(255, 255, 255), (255, 255, 255), (255, 216, 24)], stroke=10)
    d.rounded_rectangle((58, 590, 530, 660), radius=10, fill=(255, 34, 24), outline=(255, 232, 70), width=4)
    d.text((84, 599), "READ THIS?", fill=(255, 255, 255), font=font(FONT_IMPACT, 50), stroke_width=3, stroke_fill=(0, 0, 0))
    draw_pd_badge(im)
    return add_vignette(im.convert("RGB")).convert("RGBA")


def contact_sheet(paths: list[Path]) -> None:
    thumbs = []
    for p in paths:
        im = Image.open(p).convert("RGB")
        thumbs.append(ImageOps.fit(im, (426, 240), method=Image.Resampling.LANCZOS))
    sheet = Image.new("RGB", (1280, 240), (12, 12, 12))
    for i, im in enumerate(thumbs):
        sheet.paste(im, (i * 426, 0))
        d = ImageDraw.Draw(sheet)
        d.rectangle((i * 426, 0, i * 426 + 60, 36), fill=(0, 0, 0))
        d.text((i * 426 + 12, 6), "ABC"[i], font=font(FONT_ARIAL_BOLD, 22), fill=(255, 255, 255))
    sheet.save(OUT / "thumbnail.arbitration_v002_contact_sheet.jpg", quality=92)


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    PKG.mkdir(parents=True, exist_ok=True)
    options = [
        ("A", "YOU CAN'T SUE", option_a(), 96, "Strongest blunt promise-conflict hook; huge mobile-readable type and red denial stamp."),
        ("B", "I AGREE / NO COURT?", option_b(), 92, "Best tap-to-consequence concept; slightly more abstract than A."),
        ("C", "FINE PRINT TRAP", option_c(), 88, "Aggressive but less legally precise; good fallback if A feels too direct."),
    ]
    title_candidates = []
    paths: list[Path] = []
    for key, title, im, score, reason in options:
        path = OUT / f"thumbnail.arbitration_option_{key}.v002.png"
        im.convert("RGB").save(path, "PNG", optimize=True)
        paths.append(path)
        title_candidates.append(
            {
                "id": key,
                "thumbnail_text": title,
                "file": str(path.relative_to(ROOT)).replace("\\", "/"),
                "sha256": sha256(path),
                "ctr_score": score,
                "reason": reason,
            }
        )
    selected = paths[0]
    selected_pkg = PKG / "thumbnail.selected.v002.png"
    selected_pkg.write_bytes(selected.read_bytes())
    contact_sheet(paths)
    meta = {
        "schema_version": "1.0.0",
        "episode_id": EP,
        "revision": "v002",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "reason_for_revision": "Owner rejected v001 as too weak; rebuild with louder visual, larger text, and higher mobile contrast.",
        "selection_criterion": "CTR maximum: high contrast, single clear subject, emotional consequence, short text, mobile readability.",
        "selected_title_id": "A",
        "selected_thumbnail": str(selected_pkg.relative_to(ROOT)).replace("\\", "/"),
        "selected_thumbnail_sha256": sha256(selected_pkg),
        "title_candidates": title_candidates,
        "safety": {
            "real_person_likeness": False,
            "judge_likeness": False,
            "case_footage": False,
            "commercial_ok": True,
            "forced_arbitration_text_used": False,
        },
    }
    (PKG / "thumbnail_candidates.v002.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"selected": meta["selected_thumbnail"], "sha256": meta["selected_thumbnail_sha256"], "contact": str((OUT / "thumbnail.arbitration_v002_contact_sheet.jpg").relative_to(ROOT)).replace("\\", "/")}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
