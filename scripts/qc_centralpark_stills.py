#!/usr/bin/env python
"""Technical QC for EP50 Central Park still assets."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-050-centralpark"
MANIFEST = ROOT / "episodes" / EP / "05_visuals" / "asset_manifest.v001.json"
MEDIA_DIR = Path("E:/pd-media/assets/ai/centralpark")
PUBLIC_DIR = ROOT / "remotion" / "public" / "centralpark" / "img"


def expected_ids() -> list[str]:
    return [f"S{i:03d}" for i in range(1, 431)] + [f"M{i:02d}_src" for i in range(1, 86)]


def image_size(path: Path) -> tuple[int, int]:
    with Image.open(path) as im:
        return im.size


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check-resolution", action="store_true")
    ap.add_argument("--check-depth", action="store_true")
    args = ap.parse_args()
    errors: list[str] = []
    if not MANIFEST.is_file():
        errors.append(f"missing manifest {MANIFEST}")
        data = {}
    else:
        data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    manifest_ids = {str(item.get("scene_id")) for item in data.get("stills", [])} if data else set()
    for asset_id in expected_ids():
        media = MEDIA_DIR / f"{asset_id}.png"
        depth = MEDIA_DIR / f"{asset_id}_depth.png"
        if asset_id.startswith("M"):
            scene_id = f"MS{asset_id[1:3]}"
            public = None
        else:
            scene_id = asset_id
            public = PUBLIC_DIR / f"{asset_id}.png"
        if scene_id not in manifest_ids:
            errors.append(f"{scene_id} missing from manifest")
        for label, path in (("media", media), ("public", public)):
            if path is None:
                continue
            if not path.is_file():
                errors.append(f"{asset_id} missing {label} {path}")
                continue
            if args.check_resolution and max(image_size(path)) < 3840:
                errors.append(f"{asset_id} {label} long edge below 3840 {image_size(path)}")
        if args.check_depth:
            if not depth.is_file():
                errors.append(f"{asset_id} missing depth {depth}")
            elif args.check_resolution and max(image_size(depth)) < 3840:
                errors.append(f"{asset_id} depth long edge below 3840 {image_size(depth)}")
    counts = data.get("counts", {}) if data else {}
    expected = {"still_body": 430, "still_i2v_source": 85, "depth_maps": 515, "motion": 85, "factory": 485, "overlay": 60}
    for key, value in expected.items():
        if counts.get(key) != value:
            errors.append(f"manifest {key} expected {value} got {counts.get(key)}")
    if data and data.get("sdxl_used") is not False:
        errors.append("manifest must record sdxl_used=false")
    print(f"{'PASS' if not errors else 'FAIL'} centralpark_stills_qc checked={len(expected_ids())} errors={len(errors)}")
    for err in errors[:60]:
        print(f"  ! {err}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
