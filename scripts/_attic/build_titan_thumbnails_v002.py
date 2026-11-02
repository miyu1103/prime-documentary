#!/usr/bin/env python3
"""Build CTR-oriented Titan thumbnail v002 from existing symbolic assets.

No external API, upload, publish, or approval action is performed.
"""
from __future__ import annotations

import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-016-titan"
EPDIR = ROOT / "episodes" / EP
THUMB = EPDIR / "10_thumbnail"
PACKAGE = EPDIR / "09_package"
W, H = 1280, 720


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return "sha256:" + h.hexdigest()


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def font(size: int, impact: bool = True) -> ImageFont.FreeTypeFont:
    names = ["impact.ttf", "arialbd.ttf", "segoeuib.ttf"] if impact else ["arialbd.ttf", "segoeuib.ttf"]
    for name in names:
        p = Path("C:/Windows/Fonts") / name
        if p.exists():
            return ImageFont.truetype(str(p), size)
    return ImageFont.load_default()


def fit_text(draw: ImageDraw.ImageDraw, text: str, max_width: int, start: int) -> ImageFont.FreeTypeFont:
    size = start
    while size > 36:
        f = font(size)
        box = draw.textbbox((0, 0), text, font=f, stroke_width=4)
        if box[2] - box[0] <= max_width:
            return f
        size -= 4
    return font(size)


def main() -> int:
    src = THUMB / "background.THUMB-01.png"
    if not src.exists():
        raise FileNotFoundError(src)
    PACKAGE.mkdir(parents=True, exist_ok=True)
    base = Image.open(src).convert("RGB").resize((W, H), Image.Resampling.LANCZOS)
    base = ImageEnhance.Color(base).enhance(1.08)
    base = ImageEnhance.Contrast(base).enhance(1.34)
    base = ImageEnhance.Sharpness(base).enhance(1.22)

    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    for x in range(W):
        a = int(235 * max(0, 1 - x / 780))
        d.line((x, 0, x, H), fill=(0, 0, 0, a))
    d.rectangle((0, 0, W, 92), fill=(0, 0, 0, 96))
    d.rectangle((0, H - 86, W, H), fill=(0, 0, 0, 112))

    warning = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wd = ImageDraw.Draw(warning)
    wd.polygon([(0, 0), (540, 0), (390, H), (0, H)], fill=(198, 38, 38, 76))
    warning = warning.filter(ImageFilter.GaussianBlur(2))

    img = Image.alpha_composite(base.convert("RGBA"), warning)
    img = Image.alpha_composite(img, overlay)
    d = ImageDraw.Draw(img)

    yellow = (255, 213, 70, 255)
    white = (255, 255, 255, 255)
    red = (215, 43, 43, 255)
    black = (0, 0, 0, 255)

    d.rounded_rectangle((54, 42, 276, 88), radius=8, fill=red)
    d.text((76, 49), "TITAN", font=font(30, impact=False), fill=white)
    d.text((304, 50), "LAST DIVE", font=font(29, impact=False), fill=yellow)

    line1 = "THEY WERE"
    line2 = "WARNED"
    f1 = fit_text(d, line1, 670, 112)
    f2 = fit_text(d, line2, 720, 178)
    y1 = 206
    d.text((64, y1), line1, font=f1, fill=white, stroke_width=7, stroke_fill=black)
    d.text((64, y1 + 118), line2, font=f2, fill=yellow, stroke_width=8, stroke_fill=black)
    d.rectangle((64, 585, 604, 594), fill=red)
    d.text((64, 610), "A preventable disaster", font=font(34, impact=False), fill=white, stroke_width=3, stroke_fill=black)

    out = THUMB / "thumbnail.titan_selected.v002.png"
    pkg = PACKAGE / "thumbnail.selected.v002.png"
    img.convert("RGB").save(out, quality=96)
    shutil.copy2(out, pkg)

    meta = {
        "schema_version": "1.0.0",
        "episode_id": EP,
        "revision": "v002",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status": "selected_candidate_owner_gate_required",
        "external_side_effects": {"paid_api": False, "upload": False, "publish": False, "schedule": False},
        "selected_youtube_title": "They Were Warned — The Last Dive of the Titan",
        "working_title": "Pure Waste — The Last Dive of the Titan",
        "selected_thumbnail": rel(pkg),
        "selected_thumbnail_sha256": sha256(pkg),
        "source_background": rel(src),
        "thumbnail_text": "THEY WERE WARNED",
        "ctr_rationale": "More immediate than 'Pure Waste' for cold audiences: clear conflict, warning hook, high contrast, mobile-readable two-line text.",
        "safety": {
            "real_person_likeness": False,
            "brand_marks": False,
            "graphic_implosion_or_remains": False,
            "synthetic_disclosure_required": True,
        },
    }
    meta_path = PACKAGE / "title_thumbnail_candidates.v002.json"
    meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"thumbnail": rel(pkg), "sha256": meta["selected_thumbnail_sha256"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
