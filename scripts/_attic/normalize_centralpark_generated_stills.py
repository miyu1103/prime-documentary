#!/usr/bin/env python
"""Lift dark EP50 generated stills while preserving cold-cyan grade."""
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import numpy as np

from generate_centralpark_codex_assets import MANIFEST, MEDIA_AI, PUBLIC, W, H, mean_luma, phash16, sha256

QC_LUMA_SIZE = 64


def backup(path: Path) -> None:
    if not path.exists():
        return
    backup_dir = path.parent / ".bak_prenormalize"
    backup_dir.mkdir(parents=True, exist_ok=True)
    target = backup_dir / path.name
    if not target.exists():
        shutil.copy2(path, target)


def make_depth(src: Path, dst: Path) -> None:
    with Image.open(src) as im:
        gray = ImageOps.grayscale(im).resize((W, H), Image.Resampling.LANCZOS)
    grad = Image.linear_gradient("L").resize((W, H)).transpose(Image.Transpose.FLIP_TOP_BOTTOM)
    depth = Image.blend(gray, grad, 0.35)
    depth = ImageEnhance.Contrast(depth).enhance(1.25).filter(ImageFilter.GaussianBlur(4))
    ImageOps.autocontrast(depth).save(dst, compress_level=4)


def lift_image(path: Path, target_luma: float) -> None:
    current = qc_median_luma(path)
    if current >= target_luma:
        return
    backup(path)
    with Image.open(path) as im:
        im = ImageOps.exif_transpose(im).convert("RGB")
        factor = min(2.25, max(1.0, target_luma / max(1.0, current)))
        im = ImageEnhance.Brightness(im).enhance(factor)
        im = ImageEnhance.Contrast(im).enhance(1.03)
        # Re-check using the same metric as check_visual_asset_qc.py. Some images
        # have bright highlights but a dark median, so one pass is not always enough.
        for _ in range(3):
            small = np.asarray(im.convert("L").resize((QC_LUMA_SIZE, QC_LUMA_SIZE)), dtype=np.float64)
            med = float(np.median(small))
            if med >= target_luma:
                break
            im = ImageEnhance.Brightness(im).enhance(min(1.55, target_luma / max(1.0, med)))
        im.save(path, compress_level=4)


def qc_median_luma(path: Path) -> float:
    with Image.open(path) as im:
        small = np.asarray(
            ImageOps.exif_transpose(im).convert("L").resize((QC_LUMA_SIZE, QC_LUMA_SIZE)),
            dtype=np.float64,
        )
    return float(np.median(small))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="builtin_image_gen_no_sdxl")
    ap.add_argument("--role", default="body", choices=("body", "i2v_source"))
    ap.add_argument("--target-luma", type=float, default=52.0)
    ap.add_argument("--scene-id", action="append", default=[], help="Limit normalization to one or more scene IDs.")
    args = ap.parse_args()
    target_ids = set(args.scene_id)

    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    changed = []
    for item in data.get("stills", []):
        if item.get("role") != args.role or item.get("model") != args.model:
            continue
        if target_ids and item.get("scene_id") not in target_ids:
            continue
        path = Path(str(item["path"]))
        if not path.is_file() or qc_median_luma(path) >= args.target_luma:
            continue
        depth = Path(str(item["depth_path"]))
        if args.role == "body":
            public = PUBLIC / "img" / f"{item['scene_id']}.png"
            public_depth = PUBLIC / "img" / f"{item['scene_id']}_depth.png"
        else:
            public = None
            public_depth = None
        for p in [public, depth, public_depth]:
            if p is None:
                continue
            backup(p)
        lift_image(path, args.target_luma)
        if public is not None:
            shutil.copy2(path, public)
        make_depth(path, depth)
        if public_depth is not None:
            shutil.copy2(depth, public_depth)
        item["sha256"] = sha256(path)
        item["phash"] = phash16(path)
        item["mean_luma"] = mean_luma(path)
        item.setdefault("qc", {})
        item["qc"]["notes"] = str(item["qc"].get("notes", "") + "; luma normalized for centralpark visual QC").strip("; ")
        changed.append(item["scene_id"])
    MANIFEST.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"changed": len(changed), "scene_ids": changed[:80]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
