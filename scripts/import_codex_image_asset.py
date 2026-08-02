#!/usr/bin/env python
"""Import one Codex built-in image asset without overwriting existing outputs."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

from PIL import Image


def render(source: Path, destination: Path, width: int, height: int) -> dict[str, object]:
    if destination.exists():
        raise SystemExit(f"refusing to overwrite existing asset: {destination}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(source) as image:
        image = image.convert("RGB")
        source_ratio = image.width / image.height
        target_ratio = width / height
        if source_ratio > target_ratio:
            crop_width = round(image.height * target_ratio)
            left = (image.width - crop_width) // 2
            image = image.crop((left, 0, left + crop_width, image.height))
        elif source_ratio < target_ratio:
            crop_height = round(image.width / target_ratio)
            top = (image.height - crop_height) // 2
            image = image.crop((0, top, image.width, top + crop_height))
        image = image.resize((width, height), Image.Resampling.LANCZOS)
        image.save(destination, "PNG", optimize=True)
    return {
        "path": str(destination),
        "bytes": destination.stat().st_size,
        "width": width,
        "height": height,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--destination", type=Path, action="append", required=True)
    parser.add_argument("--width", type=int, default=3840)
    parser.add_argument("--height", type=int, default=2160)
    args = parser.parse_args()

    if not args.source.is_file():
        raise SystemExit(f"source image not found: {args.source}")

    primary, *copies = args.destination
    result = [render(args.source, primary, args.width, args.height)]
    for destination in copies:
        if destination.exists():
            raise SystemExit(f"refusing to overwrite existing asset: {destination}")
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(primary, destination)
        result.append(
            {
                "path": str(destination),
                "bytes": destination.stat().st_size,
                "width": args.width,
                "height": args.height,
            }
        )
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
