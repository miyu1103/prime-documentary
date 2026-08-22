#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-006-terry"
THUMB_DIR = ROOT / "episodes" / EP / "10_thumbnail"
BACKGROUND = THUMB_DIR / "codex_keyart_background.v008.png"
OUT = THUMB_DIR / "thumbnail_option_09_codex_beauty.v001.png"
REPORT = THUMB_DIR / "thumbnail_option_09_codex_beauty.v001.json"

FONT_BOLD = Path(r"C:\Windows\Fonts\impact.ttf")
FONT_UI_BOLD = Path(r"C:\Windows\Fonts\arialbd.ttf")
FONT_UI = Path(r"C:\Windows\Fonts\arial.ttf")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def font(path: Path, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(path), size)


def fit_font(draw: ImageDraw.ImageDraw, text: str, path: Path, max_width: int, start: int, min_size: int) -> ImageFont.FreeTypeFont:
    for size in range(start, min_size - 1, -2):
        f = font(path, size)
        box = draw.textbbox((0, 0), text, font=f, stroke_width=0)
        if box[2] - box[0] <= max_width:
            return f
    return font(path, min_size)


def rounded_rect(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], radius: int, fill, outline=None, width: int = 1) -> None:
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def main() -> int:
    bg = Image.open(BACKGROUND).convert("RGB")
    # Crop to exact 16:9 while preserving the right-side storefront detail.
    w, h = bg.size
    target_ratio = 16 / 9
    if w / h > target_ratio:
        new_w = int(h * target_ratio)
        left = max(0, min(w - new_w, int(w * 0.02)))
        bg = bg.crop((left, 0, left + new_w, h))
    else:
        new_h = int(w / target_ratio)
        top = max(0, min(h - new_h, int(h * 0.03)))
        bg = bg.crop((0, top, w, top + new_h))
    base = bg.resize((1280, 720), Image.Resampling.LANCZOS).convert("RGBA")

    overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)

    # Left-side readability gradient, plus subtle bottom depth.
    for x in range(1280):
        alpha = int(max(0, 225 * (1 - x / 820)))
        od.line((x, 0, x, 720), fill=(0, 0, 0, alpha))
    for y in range(720):
        alpha = int(max(0, 92 * (y - 420) / 300))
        if alpha > 0:
            od.line((0, y, 1280, y), fill=(0, 0, 0, alpha))

    # Cinematic vignette.
    vignette = Image.new("L", base.size, 0)
    vd = ImageDraw.Draw(vignette)
    vd.ellipse((-190, -140, 1470, 900), fill=210)
    vignette = Image.eval(vignette.filter(ImageFilter.GaussianBlur(90)), lambda p: 170 - int(p * 0.72))
    overlay.alpha_composite(Image.merge("RGBA", (Image.new("L", base.size, 0),) * 3 + (vignette,)))

    img = Image.alpha_composite(base, overlay)
    draw = ImageDraw.Draw(img)

    gold = (245, 188, 42, 255)
    warm_white = (248, 248, 240, 255)
    blue = (71, 155, 255, 255)
    near_black = (5, 8, 12, 230)

    # Top legal context.
    eyebrow = "TERRY v. OHIO  /  1968"
    eyebrow_font = font(FONT_UI_BOLD, 34)
    draw.text((54, 48), eyebrow, font=eyebrow_font, fill=gold)
    draw.rectangle((54, 92, 360, 99), fill=gold)

    # Main hook: fewer words, much stronger mobile read.
    main_text = "STOPPED?"
    main_font = fit_font(draw, main_text, FONT_BOLD, 610, 142, 96)
    shadow_pos = (55, 126)
    draw.text(shadow_pos, main_text, font=main_font, fill=(0, 0, 0, 245), stroke_width=7, stroke_fill=(0, 0, 0, 245))
    draw.text((50, 118), main_text, font=main_font, fill=warm_white, stroke_width=4, stroke_fill=(0, 0, 0, 240))

    sub_text = "NO WARRANT"
    sub_font = fit_font(draw, sub_text, FONT_UI_BOLD, 455, 62, 46)
    sub_box = draw.textbbox((0, 0), sub_text, font=sub_font)
    sub_w = sub_box[2] - sub_box[0]
    sub_h = sub_box[3] - sub_box[1]
    rounded_rect(draw, (55, 340, 95 + sub_w, 340 + sub_h + 34), 16, fill=(0, 0, 0, 210), outline=gold, width=4)
    draw.text((75, 353), sub_text, font=sub_font, fill=gold)

    # Simple doctrine cue on the image side, not a busy UI diagram.
    panel = (780, 474, 1185, 644)
    rounded_rect(draw, panel, 18, fill=near_black, outline=(245, 188, 42, 210), width=3)
    small = font(FONT_UI_BOLD, 30)
    draw.text((812, 500), "HUNCH", font=small, fill=(175, 190, 205, 255))
    draw.text((1030, 500), "PROOF", font=small, fill=(175, 190, 205, 255))
    draw.line((826, 560, 1142, 560), fill=(210, 220, 230, 185), width=8)
    draw.line((826, 560, 980, 560), fill=gold, width=8)
    draw.ellipse((948, 528, 992, 572), fill=gold, outline=(255, 220, 80, 255), width=2)
    rs = "REASONABLE SUSPICION"
    rs_font = fit_font(draw, rs, FONT_UI_BOLD, 330, 31, 24)
    rounded_rect(draw, (818, 590, 1148, 626), 8, fill=(3, 18, 32, 235), outline=(71, 155, 255, 220), width=2)
    draw.text((983, 607), rs, font=rs_font, fill=blue, anchor="mm")

    # Brand mark kept small and clean.
    brand = "PRIME DOCUMENTARY"
    brand_font = font(FONT_UI_BOLD, 26)
    draw.text((56, 657), brand, font=brand_font, fill=(230, 238, 245, 240))

    # Mild sharpening after text composition.
    final = img.convert("RGB").filter(ImageFilter.UnsharpMask(radius=1.2, percent=120, threshold=3))
    final.save(OUT, "PNG", optimize=True)

    report = {
        "schema_version": "1.0.0",
        "episode_id": EP,
        "revision": "v001",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "asset": str(OUT.relative_to(ROOT)).replace("\\", "/"),
        "sha256": sha256(OUT),
        "dimensions": "1280x720",
        "source_background": str(BACKGROUND.relative_to(ROOT)).replace("\\", "/"),
        "source_background_sha256": sha256(BACKGROUND),
        "text": {
            "eyebrow": eyebrow,
            "headline": main_text,
            "badge": sub_text,
            "doctrine": "HUNCH / REASONABLE SUSPICION / PROOF",
            "brand": brand,
        },
        "generator": "Codex image generation background plus deterministic PIL thumbnail composition",
        "selection_reason": "Cleaner and more premium than option 08: fewer words, larger mobile-readable hook, stronger legal tension, and the same Codex key-art atmosphere.",
    }
    REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(OUT)
    print(report["sha256"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
