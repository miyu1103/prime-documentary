#!/usr/bin/env python
"""Build EP47 Atwater asset manifest, contact sheets, and local depth maps."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageOps

ROOT = Path(__file__).resolve().parents[1]
EPISODE_ID = "PD-2026-047-atwater"
SLUG = "atwater"
MEDIA_DIR = Path("E:/pd-media/assets/ai/atwater")
PUBLIC_DIR = ROOT / "remotion" / "public" / SLUG / "img"
VISUALS_DIR = ROOT / "episodes" / EPISODE_ID / "05_visuals"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def expected_ids() -> list[str]:
    body = [f"S{i:02d}" for i in range(1, 86)]
    motion = [f"M{i:02d}_src" for i in range(1, 17)]
    return body + motion


def make_depth(src: Path, dst: Path) -> None:
    with Image.open(src) as im:
        gray = ImageOps.grayscale(im).resize((960, 540), Image.Resampling.LANCZOS)
        gradient = Image.linear_gradient("L").resize(gray.size).transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        depth = Image.blend(gray, gradient, 0.35).filter(ImageFilter.GaussianBlur(radius=5))
        depth = ImageOps.autocontrast(depth)
        depth = depth.resize((3840, 2160), Image.Resampling.BICUBIC)
        dst.parent.mkdir(parents=True, exist_ok=True)
        depth.save(dst)


def make_contact_sheet(ids: list[str], out_path: Path, columns: int = 5) -> None:
    thumb_w, thumb_h = 512, 288
    label_h = 34
    rows = (len(ids) + columns - 1) // columns
    sheet = Image.new("RGB", (columns * thumb_w, rows * (thumb_h + label_h)), (16, 16, 18))
    draw = ImageDraw.Draw(sheet)
    for idx, asset_id in enumerate(ids):
        x = (idx % columns) * thumb_w
        y = (idx // columns) * (thumb_h + label_h)
        src = MEDIA_DIR / f"{asset_id}.png"
        with Image.open(src) as im:
            thumb = ImageOps.fit(im.convert("RGB"), (thumb_w, thumb_h), Image.Resampling.LANCZOS)
        sheet.paste(thumb, (x, y))
        draw.rectangle((x, y + thumb_h, x + thumb_w, y + thumb_h + label_h), fill=(24, 24, 28))
        draw.text((x + 12, y + thumb_h + 9), asset_id, fill=(230, 230, 235))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out_path, quality=92)


def main() -> int:
    VISUALS_DIR.mkdir(parents=True, exist_ok=True)
    errors: list[str] = []
    stills: list[dict[str, object]] = []

    for asset_id in expected_ids():
        role = "still_i2v_source" if asset_id.startswith("M") else "body"
        src = MEDIA_DIR / f"{asset_id}.png"
        public = PUBLIC_DIR / f"{asset_id}.png"
        depth = MEDIA_DIR / f"{asset_id}_depth.png"
        if not src.is_file():
            errors.append(f"missing media image {src}")
            continue
        if not public.is_file():
            errors.append(f"missing public image {public}")
            continue
        with Image.open(src) as im:
            width, height = im.size
        with Image.open(public) as im:
            public_size = im.size
        if (width, height) != (3840, 2160):
            errors.append(f"{asset_id} media size {width}x{height}")
        if public_size != (3840, 2160):
            errors.append(f"{asset_id} public size {public_size[0]}x{public_size[1]}")
        if not depth.is_file():
            make_depth(src, depth)
        stills.append(
            {
                "asset_id": f"ATW-{asset_id}",
                "scene_id": asset_id,
                "role": role,
                "path": src.as_posix(),
                "depth_path": depth.as_posix(),
                "public_path": f"{SLUG}/img/{asset_id}.png",
                "width": width,
                "height": height,
                "sha256": sha256(src),
                "ai_disclosure_required": True,
                "caption_hint": "symbolic visualization only",
                "tags": ["symbolic", SLUG, "no_people", "no_likeness"],
                "qc": {"reviewed": False, "notes": ""},
            }
        )

    body_ids = [f"S{i:02d}" for i in range(1, 86)]
    motion_ids = [f"M{i:02d}_src" for i in range(1, 17)]
    make_contact_sheet(body_ids[:45], VISUALS_DIR / "atwater_body_S01_S45_contact_sheet.v001.jpg")
    make_contact_sheet(body_ids[45:], VISUALS_DIR / "atwater_body_S46_S85_contact_sheet.v001.jpg")
    make_contact_sheet(motion_ids, VISUALS_DIR / "atwater_i2v_src_contact_sheet.v001.jpg", columns=4)

    manifest = {
        "schema_version": "atwater_assets.v1",
        "episode_id": EPISODE_ID,
        "slug": SLUG,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "producer": "scripts/build_atwater_asset_manifest.py",
        "generation_provider": "Codex built-in image_gen",
        "sdxl_used": False,
        "is_stub": False,
        "counts": {
            "still_body": len([x for x in stills if x["role"] == "body"]),
            "still_i2v_source": len([x for x in stills if x["role"] == "still_i2v_source"]),
            "depth_maps": len(list(MEDIA_DIR.glob("*_depth.png"))),
        },
        "safety_locks": {
            "no_living_private_person_likeness": True,
            "no_visible_children": True,
            "no_readable_case_text_in_images": True,
            "court_holding": "Supreme Court upheld warrantless custodial arrest for fine-only seatbelt misdemeanor.",
        },
        "stills": stills,
        "contact_sheets": [
            "episodes/PD-2026-047-atwater/05_visuals/atwater_body_S01_S45_contact_sheet.v001.jpg",
            "episodes/PD-2026-047-atwater/05_visuals/atwater_body_S46_S85_contact_sheet.v001.jpg",
            "episodes/PD-2026-047-atwater/05_visuals/atwater_i2v_src_contact_sheet.v001.jpg",
        ],
        "errors": errors,
    }
    out = VISUALS_DIR / "asset_manifest.v001.json"
    out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(("PASS" if not errors else "FAIL") + f" atwater_assets stills={len(stills)} errors={len(errors)}")
    for err in errors[:30]:
        print(f"  ! {err}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
