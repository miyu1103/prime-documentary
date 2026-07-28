#!/usr/bin/env python
"""Save the latest Codex-generated image as an EP49 Strieff final-v002 candidate."""
from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageFilter, ImageOps

ROOT = Path(__file__).resolve().parents[1]
GENERATED_ROOT = Path.home() / ".codex" / "generated_images"
MEDIA_DIR = Path("H:/pd-media/assets/ai/strieff_final_v002")
PUBLIC_DIR = ROOT / "remotion" / "public" / "strieff_final_v002" / "img"


def latest_generated() -> Path:
    images = list(GENERATED_ROOT.glob("*/*.png"))
    if not images:
        raise SystemExit(f"no generated images under {GENERATED_ROOT}")
    return max(images, key=lambda p: p.stat().st_mtime)


def make_depth(src: Image.Image) -> Image.Image:
    gray = ImageOps.grayscale(src).resize((960, 540), Image.Resampling.LANCZOS)
    gradient = Image.linear_gradient("L").resize(gray.size).transpose(Image.Transpose.FLIP_TOP_BOTTOM)
    depth = Image.blend(gray, gradient, 0.35).filter(ImageFilter.GaussianBlur(radius=5))
    return ImageOps.autocontrast(depth).resize((3840, 2160), Image.Resampling.BICUBIC)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("asset_id", help="S01..S85 or M01_src..M16_src")
    parser.add_argument("--source", type=Path, default=None)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    asset_id = args.asset_id
    if not (asset_id.startswith("S") or (asset_id.startswith("M") and asset_id.endswith("_src"))):
        raise SystemExit(f"unsupported Strieff asset id: {asset_id}")
    src = args.source or latest_generated()
    media = MEDIA_DIR / f"{asset_id}.png"
    public = PUBLIC_DIR / f"{asset_id}.png"
    depth_media = MEDIA_DIR / f"{asset_id}_depth.png"
    depth_public = PUBLIC_DIR / f"{asset_id}_depth.png"
    if not args.force and (media.exists() or public.exists()):
        raise SystemExit(f"{asset_id} already exists; pass --force to replace this candidate")

    MEDIA_DIR.mkdir(parents=True, exist_ok=True)
    PUBLIC_DIR.mkdir(parents=True, exist_ok=True)
    with Image.open(src) as im:
        fitted = ImageOps.fit(im.convert("RGB"), (3840, 2160), Image.Resampling.LANCZOS)
        fitted.save(media, quality=96)
        fitted.save(public, quality=96)
        depth = make_depth(fitted)
        depth.save(depth_media)
        depth.save(depth_public)
    print(f"{asset_id} <- {src}")
    print(f"media={media}")
    print(f"public={public}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
