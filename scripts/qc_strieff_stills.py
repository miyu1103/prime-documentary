#!/usr/bin/env python
"""Technical QC for EP49 Strieff Codex image assets."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
EPISODE_ID = "PD-2026-049-strieff"
MANIFEST = ROOT / "episodes" / EPISODE_ID / "05_visuals" / "asset_manifest.v001.json"
MEDIA_DIR = Path("H:/pd-media/assets/ai/strieff")
PUBLIC_DIR = ROOT / "remotion" / "public" / "strieff" / "img"


def expected_ids() -> list[str]:
    return [f"S{i:02d}" for i in range(1, 86)] + [f"M{i:02d}_src" for i in range(1, 17)]


def image_size(path: Path) -> tuple[int, int]:
    with Image.open(path) as im:
        return im.size


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-resolution", action="store_true")
    parser.add_argument("--check-depth", action="store_true")
    args = parser.parse_args()

    errors: list[str] = []
    data: dict[str, object] = {}
    if MANIFEST.exists():
        data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    else:
        errors.append(f"missing manifest {MANIFEST}")

    manifest_ids = {str(item.get("scene_id")) for item in data.get("stills", [])} if data else set()
    for asset_id in expected_ids():
        media = MEDIA_DIR / f"{asset_id}.png"
        public = PUBLIC_DIR / f"{asset_id}.png"
        depth = MEDIA_DIR / f"{asset_id}_depth.png"
        if asset_id not in manifest_ids:
            errors.append(f"{asset_id} missing from manifest")
        for label, path in (("media", media), ("public", public)):
            if not path.is_file():
                errors.append(f"{asset_id} missing {label} {path}")
                continue
            if args.check_resolution and image_size(path) != (3840, 2160):
                errors.append(f"{asset_id} {label} wrong resolution {image_size(path)}")
        if args.check_depth:
            if not depth.is_file():
                errors.append(f"{asset_id} missing depth {depth}")
            elif image_size(depth) != (3840, 2160):
                errors.append(f"{asset_id} depth wrong resolution {image_size(depth)}")

    counts = data.get("counts", {}) if data else {}
    expected_counts = {
        "still_body": 85,
        "still_i2v_source": 16,
        "motion": 16,
        "factory": 93,
        "overlay": 12,
    }
    for key, expected in expected_counts.items():
        if counts.get(key) != expected:
            errors.append(f"manifest {key} expected {expected} got {counts.get(key)}")
    if data and data.get("sdxl_used") is not False:
        errors.append("manifest must record sdxl_used=false")

    print(f"{'PASS' if not errors else 'FAIL'} strieff_stills_qc checked={len(expected_ids())} errors={len(errors)}")
    for err in errors[:40]:
        print(f"  ! {err}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
