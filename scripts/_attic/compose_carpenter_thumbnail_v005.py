#!/usr/bin/env python3
"""Compose EP8 Carpenter thumbnail v005 from SDXL background art."""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-008-carpenter"
EPDIR = ROOT / "episodes" / EP
MEDIA = Path(json.loads((ROOT / "config/storage.local.json").read_text("utf-8"))["roots"]["media"]["path"])
SRC = MEDIA / "episodes" / EP / "05_visuals" / "sdxl_thumbnail_v005" / "carpenter_codex_style_phone_map_v005_a_seed932009.png"
THUMB_DIR = EPDIR / "10_thumbnail"
PKG_DIR = EPDIR / "09_package"
RIGHTS = PKG_DIR / "rights_manifest.v001.json"

W, H = 1280, 720
GOLD = (246, 194, 48)
BLUE = (34, 111, 255)
WHITE = (248, 250, 252)
SILVER = (198, 207, 221)

FONT_DISPLAY = r"C:\Windows\Fonts\impact.ttf"
FONT_BODY_BOLD = r"C:\Windows\Fonts\arialbd.ttf"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size=size)


def add_glow(img: Image.Image, layer: Image.Image, radius: int, strength: float) -> None:
    glow = layer.filter(ImageFilter.GaussianBlur(radius))
    a = glow.getchannel("A").point(lambda p: min(255, int(p * strength)))
    glow.putalpha(a)
    img.alpha_composite(glow)
    img.alpha_composite(layer)


def cover(src: Image.Image) -> Image.Image:
    src = src.convert("RGB")
    scale = max(W / src.width, H / src.height)
    rw, rh = int(src.width * scale), int(src.height * scale)
    resized = src.resize((rw, rh), Image.Resampling.LANCZOS)
    # Bias the crop slightly right/down so the phone becomes a strong right-side subject.
    left = min(max(0, int((rw - W) * 0.36)), rw - W)
    top = min(max(0, int((rh - H) * 0.46)), rh - H)
    return resized.crop((left, top, left + W, top + H))


def compose() -> Image.Image:
    base = cover(Image.open(SRC)).convert("RGBA")

    # Cinematic grade: dark title field on the left, richer blue/gold on the right.
    shade = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    spx = shade.load()
    for y in range(H):
        for x in range(W):
            left = max(0.0, 1.0 - x / 760)
            bottom = max(0.0, (y - 555) / 180)
            a = int(238 * (left**1.35) + 55 * bottom)
            spx[x, y] = (0, 0, 0, min(245, a))
    base.alpha_composite(shade)

    # Add a clean, intentional location trail so the thumbnail reads instantly.
    trail = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(trail)
    pts = [(72, 492), (196, 430), (320, 464), (454, 392), (586, 438), (718, 338), (872, 388), (1058, 284)]
    d.line(pts, fill=(*GOLD, 64), width=35, joint="curve")
    d.line(pts, fill=(*GOLD, 246), width=9, joint="curve")
    d.line([(x, y - 1) for x, y in pts], fill=(255, 239, 148, 180), width=3, joint="curve")
    for i, (x, y) in enumerate(pts):
        col = GOLD if i == len(pts) - 1 else BLUE
        r = 17 if i == len(pts) - 1 else 11
        d.ellipse((x - r * 2.2, y - r * 2.2, x + r * 2.2, y + r * 2.2), outline=(*col, 86), width=4)
        d.ellipse((x - r, y - r, x + r, y + r), fill=(*col, 255))
    add_glow(base, trail, 13, 1.2)

    # Subtle edge vignette.
    vig = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    vpx = vig.load()
    cx, cy = W * 0.58, H * 0.50
    for y in range(H):
        for x in range(W):
            rr = math.sqrt(((x - cx) / (W * 0.58)) ** 2 + ((y - cy) / (H * 0.75)) ** 2)
            a = int(max(0, min(105, (rr - 0.55) * 165)))
            vpx[x, y] = (0, 0, 0, a)
    base.alpha_composite(vig)

    d = ImageDraw.Draw(base)
    body = font(FONT_BODY_BOLD, 30)
    body_small = font(FONT_BODY_BOLD, 20)
    display_1 = font(FONT_DISPLAY, 124)
    display_2 = font(FONT_DISPLAY, 118)
    d.text((46, 52), "PHONE LOCATION RECORDS", font=body, fill=GOLD)
    d.rounded_rectangle((46, 96, 382, 103), radius=3, fill=GOLD)
    d.text((46, 124), "127 DAYS", font=display_1, fill=WHITE, stroke_width=3, stroke_fill=(0, 0, 0))
    d.text((46, 224), "NO WARRANT", font=display_2, fill=GOLD, stroke_width=3, stroke_fill=(0, 0, 0))
    d.text((52, 654), "PRIME DOCUMENTARY", font=body_small, fill=SILVER)
    d.rectangle((284, 656, 286, 678), fill=(160, 169, 184))
    d.text((302, 654), "SYMBOLIC RECONSTRUCTION", font=body_small, fill=GOLD)
    return base.convert("RGB")


def contact(v4: Path, v5: Path, out: Path) -> None:
    sheet = Image.new("RGB", (1320, 820), (7, 9, 14))
    d = ImageDraw.Draw(sheet)
    label = font(FONT_BODY_BOLD, 24)
    for i, (title, path) in enumerate([("v004 procedural", v4), ("v005 SDXL art", v5)]):
        im = Image.open(path).convert("RGB")
        im.thumbnail((620, 349), Image.Resampling.LANCZOS)
        x = 30 + i * 650
        y = 54
        d.text((x, 18), title, font=label, fill=WHITE if i == 0 else GOLD)
        sheet.paste(im, (x, y))
    d.text((30, 445), "Decision: v005 replaces the flat procedural look with richer SDXL background art while preserving exact text.", font=label, fill=SILVER)
    sheet.save(out, quality=94)


def write_metadata(selected: Path, contact_path: Path) -> None:
    prompt_meta = json.loads(SRC.with_suffix(".json").read_text("utf-8"))
    options = {
        "schema_version": "1.0.0",
        "episode_id": EP,
        "revision": "v005",
        "generated_at": "2026-06-20T23:45:00+09:00",
        "status": "thumbnail_selected_not_published",
        "publish_performed": False,
        "upload_performed": False,
        "ai_disclosure_required": True,
        "synthetic_content_disclosure_required": True,
        "generator": "Local SDXL via A1111 + Codex/Pillow compositing; no upload",
        "source_visuals": [str(SRC)],
        "recommended_shortlist": ["thumbnail.sdxl_art.v005.png"],
        "selected": "thumbnail.sdxl_art.v005.png",
        "selection_reason": "Replaces v004's flat procedural look with richer generated background art, while keeping text accurate and thumbnail-readable.",
        "options": [
            {
                "id": "sdxl_art_v005",
                "file": f"episodes/{EP}/10_thumbnail/thumbnail.sdxl_art.v005.png",
                "headline": "127 DAYS NO WARRANT",
                "kicker": "PHONE LOCATION RECORDS",
                "sha256": sha256(selected),
                "dimensions": "1280x720",
                "assessment": "Selected. Richer, more cinematic background art; no people, no logos, no fake text; exact title text added in post.",
            }
        ],
        "supporting_assets": [
            {
                "file": str(SRC),
                "sha256": sha256(SRC),
                "prompt_sha256": prompt_meta["prompt_sha256"],
            }
        ],
        "contact_sheet": {
            "file": f"episodes/{EP}/10_thumbnail/thumbnail_contact_sheet.v005.jpg",
            "sha256": sha256(contact_path),
        },
    }
    (THUMB_DIR / "thumbnail_options.v005.json").write_text(json.dumps(options, indent=2, ensure_ascii=False) + "\n", "utf-8")

    final = json.loads((PKG_DIR / "final_delivery.v004.json").read_text("utf-8"))
    final["revision"] = "v005"
    final["generated_at"] = "2026-06-20T23:45:00+09:00"
    final["youtube"]["thumbnail"] = f"episodes/{EP}/09_package/thumbnail.selected.v005.png"
    final["youtube"]["thumbnail_source_option"] = f"episodes/{EP}/10_thumbnail/thumbnail.sdxl_art.v005.png"
    final["thumbnail"] = {
        "file": f"episodes/{EP}/09_package/thumbnail.selected.v005.png",
        "sha256": sha256(PKG_DIR / "thumbnail.selected.v005.png"),
        "dimensions": "1280x720",
        "text": "127 DAYS / NO WARRANT",
        "kicker": "PHONE LOCATION RECORDS",
        "source_option": f"episodes/{EP}/10_thumbnail/thumbnail.sdxl_art.v005.png",
        "selection_reason": options["selection_reason"],
    }
    final["qc"]["thumbnail_options"] = f"episodes/{EP}/10_thumbnail/thumbnail_options.v005.json"
    final["notes"] = [
        "Completion package is ready for owner review or manual upload, but upload/publish was not performed.",
        "Selected thumbnail v005: local SDXL background art with exact post-rendered text, symbolic phone-map reconstruction, and no identifiable person.",
        "All AI-assisted visuals are symbolic reconstruction and require synthetic-content disclosure on YouTube.",
        "Timothy Carpenter is not depicted with an identifiable likeness.",
    ]
    (PKG_DIR / "final_delivery.v005.json").write_text(json.dumps(final, indent=2, ensure_ascii=False) + "\n", "utf-8")

    rights = json.loads(RIGHTS.read_text("utf-8"))
    rights["thumbnail_options"] = f"episodes/{EP}/10_thumbnail/thumbnail_options.v005.json"
    rights["notes"] = "All visuals are symbolic reconstruction; YouTube synthetic-content disclosure required before publish. No upload performed. Thumbnail v005 SDXL background art selected."
    assets = [a for a in rights["assets"] if a.get("type") not in {"thumbnail_render", "thumbnail_selected", "thumbnail_background"}]
    insert_at = next((i for i, a in enumerate(assets) if a.get("asset_id") == "AST-CARP-VO-001"), len(assets))
    thumb_assets = [
        {
            "asset_id": "AST-CARP-THUMB-BG-005",
            "type": "thumbnail_background",
            "scene": "thumbnail_gate",
            "description": "Local SDXL symbolic reconstruction background: abstract phone over city-location map; no people, logos, or readable labels.",
            "file": str(SRC),
            "producer": "Local SDXL via A1111",
            "license": "Owner-generated local AI image; commercial use subject to local model/license review before publish",
            "rights_holder": "Prime Documentary (channel owner)",
            "content_hash": "sha256:" + sha256(SRC),
            "needs_verification": False,
            "ai_disclosure": True,
            "synthetic_content_disclosure_required": True,
        },
        {
            "asset_id": "AST-CARP-THUMB-005",
            "type": "thumbnail_render",
            "scene": "thumbnail_gate",
            "description": "Selected SDXL-art thumbnail with exact project-rendered text.",
            "file": f"episodes/{EP}/10_thumbnail/thumbnail.sdxl_art.v005.png",
            "producer": "Local SDXL via A1111 + Codex/Pillow compositing",
            "license": "Composite thumbnail from owner-generated AI inputs",
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
            "file": f"episodes/{EP}/09_package/thumbnail.selected.v005.png",
            "producer": "Local SDXL via A1111 + Codex/Pillow compositing",
            "license": "Composite thumbnail from owner-generated AI inputs",
            "rights_holder": "Prime Documentary (channel owner)",
            "content_hash": "sha256:" + sha256(PKG_DIR / "thumbnail.selected.v005.png"),
            "needs_verification": False,
            "ai_disclosure": True,
            "synthetic_content_disclosure_required": True,
        },
    ]
    rights["assets"] = assets[:insert_at] + thumb_assets + assets[insert_at:]
    RIGHTS.write_text(json.dumps(rights, indent=2, ensure_ascii=False) + "\n", "utf-8")

    with (EPDIR / "events" / "events.jsonl").open("a", encoding="utf-8") as f:
        f.write(json.dumps({
            "event": "thumbnail_sdxl_art_v005_selected",
            "episode_id": EP,
            "stage": "thumbnail_gate",
            "revision": "v005",
            "actor": "codex",
            "detail": "Generated local SDXL premium thumbnail backgrounds, selected candidate A, composited exact text and location trail into v005, wrote thumbnail_options.v005.json and final_delivery.v005.json, updated rights manifest. Upload/publish not performed.",
            "ts": "2026-06-20T23:45:00+09:00",
        }, ensure_ascii=False) + "\n")


def main() -> int:
    THUMB_DIR.mkdir(parents=True, exist_ok=True)
    PKG_DIR.mkdir(parents=True, exist_ok=True)
    selected = THUMB_DIR / "thumbnail.sdxl_art.v005.png"
    pkg = PKG_DIR / "thumbnail.selected.v005.png"
    contact_path = THUMB_DIR / "thumbnail_contact_sheet.v005.jpg"
    im = compose()
    im.save(selected, quality=96)
    im.save(pkg, quality=96)
    contact(PKG_DIR / "thumbnail.selected.v004.png", selected, contact_path)
    write_metadata(selected, contact_path)
    print(selected)
    print(sha256(selected))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
