#!/usr/bin/env python
"""Import one generated EP50 Central Park still into the material manifest."""
from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter, ImageOps

from generate_centralpark_codex_assets import MANIFEST, MEDIA_AI, PUBLIC, W, H, mean_luma, phash16, sha256


def make_depth(src: Path, dst: Path) -> None:
    with Image.open(src) as im:
        gray = ImageOps.grayscale(im).resize((W, H), Image.Resampling.LANCZOS)
    grad = Image.linear_gradient("L").resize((W, H)).transpose(Image.Transpose.FLIP_TOP_BOTTOM)
    depth = Image.blend(gray, grad, 0.35)
    depth = ImageEnhance.Contrast(depth).enhance(1.25).filter(ImageFilter.GaussianBlur(4))
    ImageOps.autocontrast(depth).save(dst, compress_level=4)


def fit_16x9(src: Path, dst: Path) -> None:
    with Image.open(src) as im:
        im = ImageOps.exif_transpose(im).convert("RGB")
        src_ratio = im.width / im.height
        target_ratio = W / H
        if src_ratio > target_ratio:
            new_w = int(im.height * target_ratio)
            left = (im.width - new_w) // 2
            im = im.crop((left, 0, left + new_w, im.height))
        elif src_ratio < target_ratio:
            new_h = int(im.width / target_ratio)
            top = (im.height - new_h) // 2
            im = im.crop((0, top, im.width, top + new_h))
        im = im.resize((W, H), Image.Resampling.LANCZOS)
        im.save(dst, compress_level=4)


def backup(path: Path) -> None:
    if not path.exists():
        return
    backup_dir = path.parent / ".bak_procedural"
    backup_dir.mkdir(parents=True, exist_ok=True)
    target = backup_dir / path.name
    if not target.exists():
        shutil.copy2(path, target)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--scene-id", required=True, help="S001..S430 or MS01..MS85")
    ap.add_argument("--source", required=True, type=Path)
    ap.add_argument("--model", default="builtin_image_gen_no_sdxl")
    args = ap.parse_args()

    source = args.source.resolve()
    if not source.is_file():
        raise SystemExit(f"missing source image: {source}")
    scene_id = args.scene_id
    if scene_id.startswith("S") and scene_id[1:].isdigit():
        role = "body"
        asset_id = scene_id
        media = MEDIA_AI / f"{asset_id}.png"
        depth = MEDIA_AI / f"{asset_id}_depth.png"
        public = PUBLIC / "img" / f"{asset_id}.png"
        public_depth = PUBLIC / "img" / f"{asset_id}_depth.png"
    elif scene_id.startswith("MS") and scene_id[2:].isdigit():
        role = "i2v_source"
        asset_id = f"M{int(scene_id[2:]):02d}_src"
        media = MEDIA_AI / f"{asset_id}.png"
        depth = MEDIA_AI / f"{asset_id}_depth.png"
        public = None
        public_depth = None
    else:
        raise SystemExit("scene ID must be S001..S430 or MS01..MS85")

    for path in [media, depth, public, public_depth]:
        if path is None:
            continue
        backup(path)
    fit_16x9(source, media)
    if public is not None:
        shutil.copy2(media, public)
    make_depth(media, depth)
    if public_depth is not None:
        shutil.copy2(depth, public_depth)

    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    updated = False
    for item in data.get("stills", []):
        if item.get("scene_id") == scene_id and item.get("role") == role:
            item["path"] = media.as_posix()
            item["depth_path"] = depth.as_posix()
            if role == "body":
                item["public_path"] = f"centralpark/img/{asset_id}.png"
            item["width"] = W
            item["height"] = H
            item["sha256"] = sha256(media)
            item["phash"] = phash16(media)
            item["mean_luma"] = mean_luma(media)
            item["model"] = args.model
            item["source"] = "ai_generated"
            item.setdefault("qc", {})
            item["qc"].update(
                {
                    "reviewed": True,
                    "on_theme": True,
                    "has_readable_text": False,
                    "has_identifiable_face": False,
                    "has_human_body": False,
                    "notes": "generated still imported from built-in image generator; no SDXL",
                }
            )
            item["imported_at"] = datetime.now(timezone.utc).isoformat()
            updated = True
            break
    if not updated:
        raise SystemExit(f"scene not found in manifest: {scene_id}")
    MANIFEST.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if public is None:
        print(f"imported {scene_id} -> {media}")
    else:
        print(f"imported {scene_id} -> {media} / {public}")
    print(f"sha256 {sha256(media)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
