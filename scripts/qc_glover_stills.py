#!/usr/bin/env python
"""Technical QC for EP48 Glover image assets."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-048-glover"
MANIFEST = ROOT / "episodes" / EP / "05_visuals" / "asset_manifest.v001.json"
MEDIA_DIR = Path("E:/pd-media/assets/ai/glover")
PUBLIC_DIR = ROOT / "remotion" / "public" / "glover" / "img"


def expected_ids() -> list[str]:
    return [f"S{i:02d}" for i in range(1, 86)] + [f"M{i:02d}_src" for i in range(1, 17)]


def size(path: Path) -> tuple[int, int]:
    with Image.open(path) as im:
        return im.size


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-resolution", action="store_true")
    parser.add_argument("--check-depth", action="store_true")
    args = parser.parse_args()
    errors: list[str] = []
    data = json.loads(MANIFEST.read_text(encoding="utf-8")) if MANIFEST.is_file() else {}
    manifest_ids = {str(item.get("scene_id")) for item in data.get("stills", [])} if data else set()
    for asset_id in expected_ids():
        scene_id = asset_id if asset_id.startswith("S") else f"MS{asset_id[1:3]}"
        media = MEDIA_DIR / f"{asset_id}.png"
        depth = MEDIA_DIR / f"{asset_id}_depth.png"
        public = PUBLIC_DIR / f"{asset_id}.png"
        if scene_id not in manifest_ids:
            errors.append(f"{scene_id} missing from manifest")
        if not media.is_file():
            errors.append(f"{asset_id} missing media {media}")
        elif args.check_resolution and size(media) != (3840, 2160):
            errors.append(f"{asset_id} media wrong resolution {size(media)}")
        if asset_id.startswith("S"):
            if not public.is_file():
                errors.append(f"{asset_id} missing public image {public}")
            elif args.check_resolution and size(public) != (3840, 2160):
                errors.append(f"{asset_id} public wrong resolution {size(public)}")
        if args.check_depth:
            if not depth.is_file():
                errors.append(f"{asset_id} missing depth {depth}")
            elif size(depth) != (3840, 2160):
                errors.append(f"{asset_id} depth wrong resolution {size(depth)}")
    counts = data.get("counts", {}) if data else {}
    if counts.get("still_body") != 85:
        errors.append(f"manifest still_body expected 85 got {counts.get('still_body')}")
    if counts.get("still_i2v_source") != 16:
        errors.append(f"manifest still_i2v_source expected 16 got {counts.get('still_i2v_source')}")
    if data and data.get("sdxl_used") is not False:
        errors.append("manifest must record sdxl_used=false")
    print(f"{'PASS' if not errors else 'FAIL'} glover_stills_qc checked={len(expected_ids())} errors={len(errors)}")
    for err in errors[:40]:
        print(f"  ! {err}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
