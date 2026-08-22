from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
GEN_ROOT = Path(r"C:/Users/aab15/.codex/generated_images")
MEDIA_ROOT = Path(r"E:/pd-media/assets/ai/tlo")
PUBLIC_ROOT = ROOT / "remotion" / "public" / "tlo" / "img"
TARGET = (3840, 2160)


def latest_png() -> Path:
    candidates = [p for p in GEN_ROOT.rglob("*.png") if p.is_file()]
    if not candidates:
        raise SystemExit(f"no generated png found under {GEN_ROOT}")
    return max(candidates, key=lambda p: p.stat().st_mtime)


def fit_16x9(im: Image.Image) -> Image.Image:
    im = im.convert("RGB")
    src_ratio = im.width / im.height
    target_ratio = TARGET[0] / TARGET[1]
    if abs(src_ratio - target_ratio) > 0.01:
        if src_ratio > target_ratio:
            new_w = int(im.height * target_ratio)
            left = (im.width - new_w) // 2
            im = im.crop((left, 0, left + new_w, im.height))
        else:
            new_h = int(im.width / target_ratio)
            top = (im.height - new_h) // 2
            im = im.crop((0, top, im.width, top + new_h))
    return im.resize(TARGET, Image.Resampling.LANCZOS)


def save(src: Path, asset_id: str) -> None:
    with Image.open(src) as im:
        out = fit_16x9(im)
        for folder in (MEDIA_ROOT, PUBLIC_ROOT):
            folder.mkdir(parents=True, exist_ok=True)
            dest = folder / f"{asset_id}.png"
            out.save(dest, "PNG", optimize=True)
            print(f"{dest} {out.size} {dest.stat().st_size}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("asset_id", help="S11 or M01_src")
    args = parser.parse_args()
    src = latest_png()
    save(src, args.asset_id)
    print(f"source={src}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
