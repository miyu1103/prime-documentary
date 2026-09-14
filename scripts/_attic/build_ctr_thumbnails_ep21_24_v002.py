#!/usr/bin/env python3
"""Build CTR-stronger selected thumbnails for EP21-EP24.

The backgrounds come from each episode's already packaged selected thumbnail.
This keeps the legal/safety visual surface stable while increasing contrast,
scale, and click clarity.
"""
from __future__ import annotations

import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[1]
W, H = 1280, 720
REV = "v002_ctr"


EPISODES = [
    {
        "episode": 21,
        "episode_id": "PD-2026-021-dbcooper",
        "input": ROOT / "episodes/PD-2026-021-dbcooper/09_package/thumbnail.selected.v001.png",
        "output": ROOT / "episodes/PD-2026-021-dbcooper/09_package/thumbnail.selected.v002_ctr.png",
        "headline": ["STILL", "MISSING"],
        "accent": "NO TRACE",
        "primary": "#ffd33d",
        "secondary": "#1f6bff",
        "warning": "#ff3131",
        "safe_note": "Unsolved-case wording only; no suspect named or implied.",
    },
    {
        "episode": 22,
        "episode_id": "PD-2026-022-milken",
        "input": ROOT / "episodes/PD-2026-022-milken/09_package/thumbnail.selected.v001.png",
        "output": ROOT / "episodes/PD-2026-022-milken/09_package/thumbnail.selected.v002_ctr.png",
        "headline": ["GENIUS", "OR GREED?"],
        "accent": "6 PLEAS",
        "primary": "#f6c343",
        "secondary": "#00d1ff",
        "warning": "#ff3b3b",
        "safe_note": "Question framing only; no conviction-at-trial, insider-trading conviction, RICO, or exoneration claim.",
    },
    {
        "episode": 23,
        "episode_id": "PD-2026-023-swartz",
        "input": ROOT / "episodes/PD-2026-023-swartz/09_package/thumbnail.selected.v001.png",
        "output": ROOT / "episodes/PD-2026-023-swartz/09_package/thumbnail.selected.v002_ctr.png",
        "headline": ["13", "FELONIES"],
        "accent": "OPEN WEB",
        "primary": "#e5b53a",
        "secondary": "#1f6bff",
        "warning": "#ffffff",
        "safe_note": "No death/self-harm wording, no single-cause claim, no 35-years wording.",
    },
    {
        "episode": 24,
        "episode_id": "PD-2026-024-rajaratnam",
        "input": ROOT / "episodes/PD-2026-024-rajaratnam/09_package/thumbnail.selected.v001.png",
        "output": ROOT / "episodes/PD-2026-024-rajaratnam/09_package/thumbnail.selected.v002_ctr.png",
        "headline": ["CAUGHT", "ON TAPE"],
        "accent": "WIRETAP",
        "primary": "#f5c542",
        "secondary": "#19c3ff",
        "warning": "#ff3131",
        "safe_note": "Record-safe case wording; avoids profit-size confusion and unrelated cases.",
    },
]


BANNED_TEXT = {
    21: ["SOLVED", "WAS D.B. COOPER", "WAS DB COOPER"],
    22: ["CONVICTED AT TRIAL", "CONVICTED OF INSIDER", "RICO", "EXONERATED"],
    23: ["SUICIDE", "DEATH", "DIED", "CAUSED", "35 YEARS", "METHOD", "NOTE"],
    24: ["$7B PROFIT", "LONGEST SENTENCE", "GUPTA"],
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return "sha256:" + h.hexdigest()


def font(size: int) -> ImageFont.FreeTypeFont:
    candidates = [
        Path("C:/Windows/Fonts/impact.ttf"),
        Path("C:/Windows/Fonts/ariblk.ttf"),
        Path("C:/Windows/Fonts/arialbd.ttf"),
    ]
    for path in candidates:
        if path.exists():
            return ImageFont.truetype(str(path), size=size)
    return ImageFont.load_default()


def cover(path: Path) -> Image.Image:
    img = Image.open(path).convert("RGB")
    return ImageOps.fit(img, (W, H), Image.Resampling.LANCZOS)


def add_gradient(base: Image.Image, primary: str, secondary: str, warning: str) -> Image.Image:
    base = ImageEnhance.Contrast(base).enhance(1.2)
    base = ImageEnhance.Color(base).enhance(1.18)

    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    px = overlay.load()
    p = tuple(int(primary[i : i + 2], 16) for i in (1, 3, 5))
    s = tuple(int(secondary[i : i + 2], 16) for i in (1, 3, 5))
    r = tuple(int(warning[i : i + 2], 16) for i in (1, 3, 5))
    for y in range(H):
        for x in range(W):
            left = max(0, 1 - x / 760)
            right = max(0, (x - 560) / 720)
            top = max(0, 1 - y / 460)
            a = int(110 * left + 70 * right + 34 * top)
            if x < 620:
                color = (0, 0, 0)
            elif y < 260:
                color = s
            else:
                color = p if (x + y) % 7 else r
            px[x, y] = (*color, min(175, a))
    return Image.alpha_composite(base.convert("RGBA"), overlay)


def polygon_glow(draw: ImageDraw.ImageDraw, color: str, side: str) -> None:
    if side == "right":
        pts = [(850, -40), (1340, -20), (1280, 760), (1010, 720), (930, 360)]
    else:
        pts = [(-80, 50), (600, -40), (520, 760), (-60, 720)]
    draw.polygon(pts, fill=color + "56")
    draw.line(pts + [pts[0]], fill="#ffffff66", width=6)


def draw_text_stroked(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    text: str,
    fnt: ImageFont.FreeTypeFont,
    fill: str,
    stroke: int = 8,
    anchor: str = "la",
) -> None:
    draw.text(xy, text, font=fnt, fill=fill, stroke_width=stroke, stroke_fill="#06111f", anchor=anchor)


def fit_font(text: str, max_width: int, start_size: int, min_size: int = 72) -> ImageFont.FreeTypeFont:
    size = start_size
    while size >= min_size:
        f = font(size)
        bbox = ImageDraw.Draw(Image.new("RGB", (10, 10))).textbbox((0, 0), text, font=f, stroke_width=10)
        if bbox[2] - bbox[0] <= max_width:
            return f
        size -= 4
    return font(min_size)


def add_badge(draw: ImageDraw.ImageDraw, text: str, primary: str, warning: str) -> None:
    f = fit_font(text, 330, 46, 34)
    bbox = draw.textbbox((0, 0), text, font=f, stroke_width=4)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x, y = 70, 64
    pad_x, pad_y = 28, 15
    draw.rounded_rectangle(
        [x - pad_x, y - pad_y, x + tw + pad_x, y + th + pad_y],
        radius=14,
        fill="#08111eea",
        outline=warning,
        width=5,
    )
    draw.text((x, y), text, font=f, fill=primary, stroke_width=3, stroke_fill="#000000", anchor="la")


def add_burst(draw: ImageDraw.ImageDraw, center: tuple[int, int], primary: str, secondary: str) -> None:
    cx, cy = center
    for i in range(26):
        angle = i * math.tau / 26
        r1 = 80 + (i % 3) * 18
        r2 = 360 + (i % 5) * 28
        x1 = cx + math.cos(angle) * r1
        y1 = cy + math.sin(angle) * r1
        x2 = cx + math.cos(angle) * r2
        y2 = cy + math.sin(angle) * r2
        draw.line((x1, y1, x2, y2), fill=(primary if i % 2 else secondary) + "55", width=8)


def make_thumb(spec: dict) -> dict:
    text = " ".join(spec["headline"] + [spec["accent"]])
    upper = text.upper()
    for banned in BANNED_TEXT[spec["episode"]]:
        if banned in upper:
            raise RuntimeError(f"EP{spec['episode']} thumbnail text contains banned fragment: {banned}")

    img = cover(spec["input"])
    img = add_gradient(img, spec["primary"], spec["secondary"], spec["warning"])
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)

    add_burst(draw, (1030, 355), spec["primary"], spec["secondary"])
    polygon_glow(draw, spec["secondary"], "right")
    draw.rectangle([0, 0, W - 1, H - 1], outline=spec["primary"], width=14)
    draw.rectangle([16, 16, W - 17, H - 17], outline="#ffffff60", width=3)

    # A large, dark headline plate keeps the text readable at small sizes.
    draw.rounded_rectangle([36, 126, 800, 662], radius=20, fill="#020712f7", outline=spec["primary"], width=7)
    draw.line((56, 138, 785, 138), fill=spec["warning"], width=7)

    add_badge(draw, spec["accent"], spec["primary"], spec["warning"])

    y = 198
    first_size = 166 if len(spec["headline"][0]) < 7 else 146
    for idx, line in enumerate(spec["headline"]):
        max_w = 690
        f = fit_font(line, max_w, first_size if idx == 0 else 154, 84)
        color = "#ffffff" if idx == 0 else spec["primary"]
        if spec["episode"] == 23 and line == "13":
            color = spec["primary"]
            f = fit_font(line, 310, 220, 150)
        draw_text_stroked(draw, (82, y), line, f, color, stroke=10)
        bbox = draw.textbbox((82, y), line, font=f, stroke_width=10, anchor="la")
        y = bbox[3] + 18

    # Directional symbols without extra claims.
    draw.polygon([(1040, 138), (1215, 360), (1040, 582), (1098, 392), (858, 392), (858, 328), (1098, 328)], fill=spec["warning"] + "d8")
    draw.line([(1040, 138), (1215, 360), (1040, 582)], fill="#ffffffbb", width=5)

    img = Image.alpha_composite(img, layer)
    img = img.filter(ImageFilter.UnsharpMask(radius=1.1, percent=125, threshold=3)).convert("RGB")
    spec["output"].parent.mkdir(parents=True, exist_ok=True)
    img.save(spec["output"], "PNG", optimize=True)

    return {
        "episode": spec["episode"],
        "episode_id": spec["episode_id"],
        "input": str(spec["input"]).replace("\\", "/"),
        "output": str(spec["output"]).replace("\\", "/"),
        "size": list(Image.open(spec["output"]).size),
        "sha256": sha256(spec["output"]),
        "headline": " ".join(spec["headline"]),
        "accent": spec["accent"],
        "safety": spec["safe_note"],
    }


def make_contact_sheet(items: list[dict]) -> Path:
    sheet = Image.new("RGB", (W * 2, H * 2), "#10151f")
    for idx, item in enumerate(items):
        thumb = Image.open(item["output"]).convert("RGB")
        x = (idx % 2) * W
        y = (idx // 2) * H
        sheet.paste(thumb, (x, y))
    out = ROOT / "runs/qc/ep21_24_thumbnail_ctr_v002_contact.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out, "PNG", optimize=True)
    return out


def main() -> None:
    results = [make_thumb(spec) for spec in EPISODES]
    contact = make_contact_sheet(results)
    data = {
        "schema_version": "1.0.0",
        "revision": REV,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "purpose": "CTR-stronger replacement thumbnails for already scheduled EP21-EP24.",
        "contact_sheet": str(contact).replace("\\", "/"),
        "items": results,
    }
    out = ROOT / "runs/qc/ep21_24_thumbnail_ctr_v002_qc.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(data, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
