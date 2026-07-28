#!/usr/bin/env python
"""Lift EP49 Strieff still exposure for the visual-asset QC luma floor.

Original Codex outputs are preserved once under H:/pd-media/assets/ai/strieff/_pre_grade_backup.
The active media and Remotion public copies are then updated in place, followed
by depth-map regeneration. This uses no SDXL or external provider.
"""
from __future__ import annotations

import shutil
from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter, ImageOps, ImageStat

ROOT = Path(__file__).resolve().parents[1]
MEDIA = Path("H:/pd-media/assets/ai/strieff")
BACKUP = MEDIA / "_pre_grade_backup"
PUBLIC = ROOT / "remotion" / "public" / "strieff" / "img"
TARGET_MEDIAN = 54.0


def ids() -> list[str]:
    return [f"S{i:02d}" for i in range(1, 86)] + [f"M{i:02d}_src" for i in range(1, 17)]


def median_luma(im: Image.Image) -> float:
    gray = ImageOps.grayscale(im).resize((64, 64), Image.Resampling.LANCZOS)
    return float(ImageStat.Stat(gray).median[0])


def grade(im: Image.Image) -> Image.Image:
    out = ImageOps.autocontrast(im.convert("RGB"), cutoff=0.15)
    # Gamma lift opens shadows while keeping highlights below clipping.
    lut = [min(255, int(((i / 255.0) ** 0.58) * 255 + 0.5)) for i in range(256)]
    out = out.point(lut * 3)
    out = ImageEnhance.Brightness(out).enhance(1.12)
    out = ImageEnhance.Contrast(out).enhance(1.04)
    for _ in range(8):
        if median_luma(out) >= TARGET_MEDIAN:
            break
        out = ImageEnhance.Brightness(out).enhance(1.10)
    return out


def make_depth(src: Path, dst: Path) -> None:
    with Image.open(src) as im:
        fitted = ImageOps.fit(im.convert("RGB"), (3840, 2160), Image.Resampling.LANCZOS)
        gray = ImageOps.grayscale(fitted).resize((960, 540), Image.Resampling.LANCZOS)
        gradient = Image.linear_gradient("L").resize(gray.size).transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        depth = Image.blend(gray, gradient, 0.35).filter(ImageFilter.GaussianBlur(radius=5))
        depth = ImageOps.autocontrast(depth).resize((3840, 2160), Image.Resampling.BICUBIC)
        depth.save(dst)


def main() -> int:
    BACKUP.mkdir(parents=True, exist_ok=True)
    PUBLIC.mkdir(parents=True, exist_ok=True)
    changed = 0
    medians: list[float] = []
    for asset_id in ids():
        src = MEDIA / f"{asset_id}.png"
        if not src.is_file():
            raise FileNotFoundError(src)
        backup = BACKUP / src.name
        if not backup.exists():
            shutil.copy2(src, backup)
        with Image.open(src) as im:
            before = median_luma(im)
            out = grade(im) if before < TARGET_MEDIAN else im.convert("RGB")
            after = median_luma(out)
        medians.append(after)
        if after != before:
            out.save(src)
            changed += 1
        shutil.copy2(src, PUBLIC / src.name)
        depth = MEDIA / f"{asset_id}_depth.png"
        make_depth(src, depth)
        shutil.copy2(depth, PUBLIC / depth.name)
    print({
        "changed": changed,
        "count": len(medians),
        "median_min": min(medians),
        "median_max": max(medians),
        "median_avg": round(sum(medians) / len(medians), 2),
        "backup": str(BACKUP),
    })
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
