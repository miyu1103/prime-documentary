#!/usr/bin/env python3
"""Generate deterministic Codex key art for EP8 Carpenter thumbnail v004.

The output is a symbolic reconstruction: no people, no logos, no real maps,
and no generated text. Exact thumbnail text is drawn by this script.
"""
from __future__ import annotations

import hashlib
import json
import math
import random
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-008-carpenter"
EPDIR = ROOT / "episodes" / EP
THUMB_DIR = EPDIR / "10_thumbnail"
PKG_DIR = EPDIR / "09_package"
RIGHTS = PKG_DIR / "rights_manifest.v001.json"

W, H = 2560, 1440
OUT_W, OUT_H = 1280, 720
BLACK = (3, 5, 9)
NAVY = (6, 14, 28)
BLUE = (37, 111, 255)
BLUE_2 = (16, 195, 255)
GOLD = (244, 193, 51)
WHITE = (246, 248, 250)
SILVER = (198, 207, 221)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size=size)


FONT_DISPLAY = r"C:\Windows\Fonts\impact.ttf"
FONT_BODY_BOLD = r"C:\Windows\Fonts\arialbd.ttf"


def add_glow(base: Image.Image, layer: Image.Image, radius: int, strength: float = 1.0) -> None:
    glow = layer.filter(ImageFilter.GaussianBlur(radius))
    if strength != 1.0:
        a = glow.getchannel("A").point(lambda p: min(255, int(p * strength)))
        glow.putalpha(a)
    base.alpha_composite(glow)
    base.alpha_composite(layer)


def bezier(points: list[tuple[float, float]], steps: int = 160) -> list[tuple[int, int]]:
    out: list[tuple[int, int]] = []
    for i in range(steps + 1):
        t = i / steps
        x = (
            (1 - t) ** 3 * points[0][0]
            + 3 * (1 - t) ** 2 * t * points[1][0]
            + 3 * (1 - t) * t**2 * points[2][0]
            + t**3 * points[3][0]
        )
        y = (
            (1 - t) ** 3 * points[0][1]
            + 3 * (1 - t) ** 2 * t * points[1][1]
            + 3 * (1 - t) * t**2 * points[2][1]
            + t**3 * points[3][1]
        )
        out.append((int(x), int(y)))
    return out


def make_background() -> Image.Image:
    rng = random.Random(814420)
    img = Image.new("RGBA", (W, H), BLACK + (255,))
    px = img.load()
    for y in range(H):
        for x in range(W):
            nx = x / W
            ny = y / H
            blue_field = math.exp(-(((nx - 0.78) / 0.35) ** 2 + ((ny - 0.48) / 0.52) ** 2))
            gold_field = math.exp(-(((nx - 0.89) / 0.23) ** 2 + ((ny - 0.55) / 0.36) ** 2))
            vignette = min(1.0, ((x - W * 0.5) ** 2 / (W * 0.62) ** 2 + (y - H * 0.5) ** 2 / (H * 0.72) ** 2))
            r = int(4 + blue_field * 6 + gold_field * 5 - vignette * 3)
            g = int(7 + blue_field * 18 + gold_field * 9 - vignette * 3)
            b = int(13 + blue_field * 42 + gold_field * 4 - vignette * 5)
            px[x, y] = (max(0, r), max(0, g), max(0, b), 255)

    # Abstract city/map lattice, concentrated on right half.
    grid = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(grid)
    vanishing = (2140, 210)
    for i in range(34):
        y0 = int(155 + i * 37 + rng.uniform(-10, 10))
        x0 = int(750 + rng.uniform(-60, 80))
        d.line([(x0, y0), vanishing], fill=(*BLUE_2, 28), width=2)
    for i in range(28):
        x0 = int(680 + i * 67 + rng.uniform(-18, 18))
        d.line([(x0, 1350), vanishing], fill=(*BLUE, 22), width=2)
    for i in range(46):
        y = int(185 + i * 25 + rng.uniform(-5, 5))
        d.arc((720, y - 860, 2450, y + 860), 14, 168, fill=(*BLUE, 18), width=2)
    add_glow(img, grid, 6, 0.9)

    # Distant city bokeh and data dust.
    dust = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(dust)
    for _ in range(980):
        x = int(rng.triangular(760, W - 50, 1820))
        y = int(rng.triangular(95, H - 80, 560))
        size = rng.choice([1, 1, 1, 2, 2, 3])
        col = BLUE if rng.random() < 0.72 else GOLD
        alpha = rng.randint(22, 92)
        d.ellipse((x, y, x + size, y + size), fill=(*col, alpha))
    for _ in range(170):
        x = rng.randint(1080, W - 100)
        y = rng.randint(120, H - 120)
        w = rng.randint(4, 13)
        h = rng.randint(2, 8)
        col = GOLD if rng.random() < 0.34 else BLUE_2
        d.rounded_rectangle((x, y, x + w, y + h), radius=2, fill=(*col, rng.randint(28, 76)))
    add_glow(img, dust, 3, 1.2)

    return img


def draw_phone_and_path(img: Image.Image) -> None:
    phone = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(phone)

    # Phone group drawn in local high-res coordinates then rotated for clean antialiasing.
    pw, ph = 740, 1080
    p = Image.new("RGBA", (pw + 180, ph + 180), (0, 0, 0, 0))
    pd = ImageDraw.Draw(p)
    off = 90
    pd.rounded_rectangle((off - 28, off + 35, off + pw + 28, off + ph + 42), radius=126, fill=(0, 0, 0, 128))
    pd.rounded_rectangle((off, off, off + pw, off + ph), radius=116, fill=(4, 7, 13, 255), outline=(226, 235, 246, 185), width=14)
    pd.rounded_rectangle((off + 52, off + 58, off + pw - 52, off + ph - 58), radius=82, fill=(4, 11, 23, 250), outline=(*BLUE, 146), width=5)
    pd.rounded_rectangle((off + 194, off + 30, off + pw - 194, off + 58), radius=14, fill=(4, 6, 11, 255), outline=(69, 82, 104, 155), width=2)
    # Glass glow.
    for r, a in [(300, 24), (205, 42), (118, 88)]:
        pd.ellipse((off + pw * 0.50 - r, off + ph * 0.43 - r, off + pw * 0.50 + r, off + ph * 0.43 + r), fill=(*BLUE, a))

    local_path = bezier([(off + 150, off + 820), (off + 245, off + 515), (off + 410, off + 785), (off + 565, off + 250)], 150)
    pd.line(local_path, fill=(*GOLD, 70), width=72, joint="curve")
    pd.line(local_path, fill=(*GOLD, 255), width=34, joint="curve")
    for i, idx in enumerate([0, 42, 90, 150]):
        x, y = local_path[idx]
        color = GOLD if i == 3 else BLUE
        pd.ellipse((x - 62, y - 62, x + 62, y + 62), outline=(*color, 96), width=8)
        pd.ellipse((x - 30, y - 30, x + 30, y + 30), fill=(*color, 255))

    p = p.rotate(-6.5, resample=Image.Resampling.BICUBIC, expand=True)
    img.alpha_composite(p, (1410, 116))

    # Main location path across the map, behind and into phone.
    path_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(path_layer)
    pts = [(158, 962), (420, 828), (665, 910), (900, 762), (1180, 858), (1425, 647), (1745, 750), (2125, 565)]
    d.line(pts, fill=(*GOLD, 68), width=64, joint="curve")
    d.line(pts, fill=(*GOLD, 245), width=18, joint="curve")
    d.line([(x, y - 2) for x, y in pts], fill=(255, 236, 126, 180), width=5, joint="curve")
    for i, (x, y) in enumerate(pts):
        color = GOLD if i == len(pts) - 1 else BLUE
        r = 28 if i == len(pts) - 1 else 20
        d.ellipse((x - r * 2.2, y - r * 2.2, x + r * 2.2, y + r * 2.2), outline=(*color, 80), width=7)
        d.ellipse((x - r, y - r, x + r, y + r), fill=(*color, 255))
    add_glow(img, path_layer, 18, 1.15)


def add_text_and_finish(bg: Image.Image) -> Image.Image:
    img = bg.resize((OUT_W, OUT_H), Image.Resampling.LANCZOS)
    # Darken left panel without flattening the artwork.
    shade = Image.new("RGBA", (OUT_W, OUT_H), (0, 0, 0, 0))
    spx = shade.load()
    for y in range(OUT_H):
        for x in range(OUT_W):
            t = max(0.0, 1.0 - x / 720)
            a = int(218 * (t**1.45))
            spx[x, y] = (0, 0, 0, a)
    img.alpha_composite(shade)

    # Background-only finish. Keep text crisp by drawing it after grain/vignette.
    rng = random.Random(92241)
    grain = Image.new("RGBA", (OUT_W, OUT_H), (0, 0, 0, 0))
    gpx = grain.load()
    for y in range(OUT_H):
        for x in range(OUT_W):
            n = rng.randint(0, 8)
            gpx[x, y] = (255, 255, 255, n if rng.random() < 0.20 else 0)
    img.alpha_composite(grain)

    vig = Image.new("RGBA", (OUT_W, OUT_H), (0, 0, 0, 0))
    vpx = vig.load()
    cx, cy = OUT_W * 0.56, OUT_H * 0.50
    for y in range(OUT_H):
        for x in range(OUT_W):
            r = math.sqrt(((x - cx) / (OUT_W * 0.56)) ** 2 + ((y - cy) / (OUT_H * 0.72)) ** 2)
            a = int(max(0, min(130, (r - 0.48) * 185)))
            vpx[x, y] = (0, 0, 0, a)
    img.alpha_composite(vig)

    d = ImageDraw.Draw(img)
    body = font(FONT_BODY_BOLD, 30)
    body_small = font(FONT_BODY_BOLD, 20)
    display = font(FONT_DISPLAY, 116)
    display_2 = font(FONT_DISPLAY, 120)

    d.text((46, 52), "PHONE LOCATION RECORDS", font=body, fill=GOLD)
    d.rounded_rectangle((46, 96, 382, 103), radius=3, fill=GOLD)
    d.text((46, 128), "127 DAYS", font=display_2, fill=WHITE, stroke_width=3, stroke_fill=(0, 0, 0))
    d.text((46, 226), "NO WARRANT", font=display, fill=GOLD, stroke_width=3, stroke_fill=(0, 0, 0))
    d.text((52, 654), "PRIME DOCUMENTARY", font=body_small, fill=SILVER)
    d.rectangle((284, 656, 286, 678), fill=(160, 169, 184))
    d.text((302, 654), "SYMBOLIC RECONSTRUCTION", font=body_small, fill=GOLD)
    return img.convert("RGB")


def make_contact(v2: Path, v3: Path, out: Path) -> None:
    sheet = Image.new("RGB", (1320, 820), (7, 9, 14))
    d = ImageDraw.Draw(sheet)
    label = font(FONT_BODY_BOLD, 24)
    for i, (title, path) in enumerate([("v002 selected", v2), ("v004 Codex key art", v3)]):
        im = Image.open(path).convert("RGB")
        im.thumbnail((620, 349), Image.Resampling.LANCZOS)
        x = 30 + i * 650
        y = 54
        d.text((x, 18), title, font=label, fill=WHITE if i == 0 else GOLD)
        sheet.paste(im, (x, y))
    d.text((30, 445), "Decision: v004 keeps the same accurate hook but gives the background a more deliberate poster-art finish.", font=label, fill=SILVER)
    sheet.save(out, quality=94)


def write_metadata(selected: Path, background: Path, contact: Path) -> None:
    options = {
        "schema_version": "1.0.0",
        "episode_id": EP,
        "revision": "v004",
        "generated_at": "2026-06-20T23:12:00+09:00",
        "status": "thumbnail_selected_not_published",
        "publish_performed": False,
        "upload_performed": False,
        "ai_disclosure_required": True,
        "synthetic_content_disclosure_required": True,
        "generator": "Codex deterministic procedural key art via Pillow; no external upload",
        "source_visuals": [],
        "recommended_shortlist": ["thumbnail.codex_keyart.v004.png"],
        "selected": "thumbnail.codex_keyart.v004.png",
        "selection_reason": "Sharper premium key art than v002 while preserving the strongest browse-size hook: 127 DAYS / NO WARRANT.",
        "options": [
            {
                "id": "codex_keyart_v004",
                "file": f"episodes/{EP}/10_thumbnail/thumbnail.codex_keyart.v004.png",
                "headline": "127 DAYS NO WARRANT",
                "kicker": "PHONE LOCATION RECORDS",
                "sha256": sha256(selected),
                "dimensions": "1280x720",
                "assessment": "Selected. Strong left-side typography, more deliberate city-map atmosphere, no people, no brands, no fake map labels.",
            }
        ],
        "supporting_assets": [
            {
                "file": f"episodes/{EP}/10_thumbnail/codex_keyart_background.v004.png",
                "sha256": sha256(background),
                "dimensions": "2560x1440",
            }
        ],
        "contact_sheet": {
            "file": f"episodes/{EP}/10_thumbnail/thumbnail_contact_sheet.v004.jpg",
            "sha256": sha256(contact),
        },
    }
    (THUMB_DIR / "thumbnail_options.v004.json").write_text(json.dumps(options, indent=2, ensure_ascii=False) + "\n", "utf-8")

    final = json.loads((PKG_DIR / "final_delivery.v002.json").read_text("utf-8"))
    final["revision"] = "v004"
    final["generated_at"] = "2026-06-20T23:12:00+09:00"
    final["youtube"]["thumbnail"] = f"episodes/{EP}/09_package/thumbnail.selected.v004.png"
    final["youtube"]["thumbnail_source_option"] = f"episodes/{EP}/10_thumbnail/thumbnail.codex_keyart.v004.png"
    final["thumbnail"] = {
        "file": f"episodes/{EP}/09_package/thumbnail.selected.v004.png",
        "sha256": sha256(PKG_DIR / "thumbnail.selected.v004.png"),
        "dimensions": "1280x720",
        "text": "127 DAYS / NO WARRANT",
        "kicker": "PHONE LOCATION RECORDS",
        "source_option": f"episodes/{EP}/10_thumbnail/thumbnail.codex_keyart.v004.png",
        "selection_reason": options["selection_reason"],
    }
    final["qc"]["thumbnail_options"] = f"episodes/{EP}/10_thumbnail/thumbnail_options.v004.json"
    final["notes"] = [
        "Completion package is ready for owner review or manual upload, but upload/publish was not performed.",
        "Selected thumbnail v004: Codex-generated procedural key art with exact rendered text, symbolic phone-map reconstruction, and no identifiable person.",
        "All AI-assisted visuals are symbolic reconstruction and require synthetic-content disclosure on YouTube.",
        "Timothy Carpenter is not depicted with an identifiable likeness.",
    ]
    (PKG_DIR / "final_delivery.v004.json").write_text(json.dumps(final, indent=2, ensure_ascii=False) + "\n", "utf-8")

    rights = json.loads(RIGHTS.read_text("utf-8"))
    rights["thumbnail_options"] = f"episodes/{EP}/10_thumbnail/thumbnail_options.v004.json"
    rights["notes"] = "All visuals are symbolic reconstruction; YouTube synthetic-content disclosure required before publish. No upload performed. Thumbnail v004 Codex key art selected."
    assets = [a for a in rights["assets"] if a.get("type") not in {"thumbnail_render", "thumbnail_selected", "thumbnail_background"}]
    insert_at = next((i for i, a in enumerate(assets) if a.get("asset_id") == "AST-CARP-VO-001"), len(assets))
    thumb_assets = [
        {
            "asset_id": "AST-CARP-THUMB-BG-003",
            "type": "thumbnail_background",
            "scene": "thumbnail_gate",
            "description": "Codex-generated deterministic procedural symbolic reconstruction background: phone, abstract city grid, and location trail; no people or readable map labels.",
            "file": f"episodes/{EP}/10_thumbnail/codex_keyart_background.v004.png",
            "producer": "Codex + Pillow procedural generation",
            "license": "Owner-generated AI-assisted procedural image",
            "rights_holder": "Prime Documentary (channel owner)",
            "content_hash": "sha256:" + sha256(background),
            "needs_verification": False,
            "ai_disclosure": True,
            "synthetic_content_disclosure_required": True,
        },
        {
            "asset_id": "AST-CARP-THUMB-003",
            "type": "thumbnail_render",
            "scene": "thumbnail_gate",
            "description": "Selected Codex key-art thumbnail with exact project-rendered text.",
            "file": f"episodes/{EP}/10_thumbnail/thumbnail.codex_keyart.v004.png",
            "producer": "Codex + Pillow procedural generation",
            "license": "Composite thumbnail from owner-generated procedural inputs",
            "rights_holder": "Prime Documentary (channel owner)",
            "content_hash": "sha256:" + sha256(selected),
            "needs_verification": False,
            "ai_disclosure": True,
            "synthetic_content_disclosure_required": True,
        },
        {
            "asset_id": "AST-CARP-THUMB-SELECTED-001",
            "type": "thumbnail_selected",
            "scene": "thumbnail_gate",
            "description": "Selected final thumbnail for manual upload.",
            "file": f"episodes/{EP}/09_package/thumbnail.selected.v004.png",
            "producer": "Codex + Pillow procedural generation",
            "license": "Composite thumbnail from owner-generated procedural inputs",
            "rights_holder": "Prime Documentary (channel owner)",
            "content_hash": "sha256:" + sha256(PKG_DIR / "thumbnail.selected.v004.png"),
            "needs_verification": False,
            "ai_disclosure": True,
            "synthetic_content_disclosure_required": True,
        },
    ]
    rights["assets"] = assets[:insert_at] + thumb_assets + assets[insert_at:]
    RIGHTS.write_text(json.dumps(rights, indent=2, ensure_ascii=False) + "\n", "utf-8")

    with (EPDIR / "events" / "events.jsonl").open("a", encoding="utf-8") as f:
        f.write(json.dumps({
            "event": "thumbnail_codex_keyart_v004_selected",
            "episode_id": EP,
            "stage": "thumbnail_gate",
            "revision": "v004",
            "actor": "codex",
            "detail": "Generated polished Codex procedural key art for thumbnail v004 and selected it as final local thumbnail. Wrote thumbnail_options.v004.json, final_delivery.v004.json, and updated rights manifest. Upload/publish not performed.",
            "ts": "2026-06-20T23:12:00+09:00",
        }, ensure_ascii=False) + "\n")


def main() -> int:
    THUMB_DIR.mkdir(parents=True, exist_ok=True)
    PKG_DIR.mkdir(parents=True, exist_ok=True)
    bg_path = THUMB_DIR / "codex_keyart_background.v004.png"
    selected_path = THUMB_DIR / "thumbnail.codex_keyart.v004.png"
    selected_pkg = PKG_DIR / "thumbnail.selected.v004.png"
    contact = THUMB_DIR / "thumbnail_contact_sheet.v004.jpg"

    bg = make_background()
    draw_phone_and_path(bg)
    bg.convert("RGB").save(bg_path, quality=96)
    final = add_text_and_finish(bg)
    final.save(selected_path, quality=96)
    shutil.copy2(selected_path, selected_pkg)
    make_contact(PKG_DIR / "thumbnail.selected.v002.png", selected_path, contact)
    write_metadata(selected_path, bg_path, contact)
    print(selected_path)
    print(sha256(selected_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
