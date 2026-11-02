#!/usr/bin/env python
"""Technical QC for EP56 Post Office still assets."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-056-postoffice"
MANIFEST = ROOT / "episodes" / EP / "05_visuals" / "asset_manifest.v001.json"
MEDIA_DIR = Path("E:/pd-media/assets/ai/postoffice")
PUBLIC_DIR = ROOT / "remotion" / "public" / "postoffice" / "img"


def expected_ids() -> list[str]:
    return [f"S{i:03d}" for i in range(1, 211)] + [f"M{i:02d}_src" for i in range(1, 43)] + [f"T{i:02d}_face" for i in range(1, 4)]


def image_size(path: Path) -> tuple[int, int]:
    with Image.open(path) as im:
        return im.size


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check-resolution", action="store_true")
    args = ap.parse_args()
    errors: list[str] = []
    data = json.loads(MANIFEST.read_text(encoding="utf-8")) if MANIFEST.is_file() else {}
    manifest_ids = {str(item.get("scene_id")) for item in data.get("stills", [])} if data else set()
    for asset_id in expected_ids():
        media = MEDIA_DIR / f"{asset_id}.png"
        if asset_id.startswith("S"):
            scene_id = asset_id
            public = PUBLIC_DIR / f"{asset_id}.png"
        elif asset_id.startswith("M"):
            scene_id = f"MS{asset_id[1:3]}"
            public = None
        else:
            scene_id = f"T{asset_id[1:3]}"
            public = None
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
    expected = {"still_body": 210, "still_i2v_source": 42, "motion": 42, "factory": 235, "overlay": 30, "thumb_face": 3}
    counts = data.get("counts", {}) if data else {}
    for key, value in expected.items():
        if counts.get(key) != value:
            errors.append(f"manifest {key} expected {value} got {counts.get(key)}")
    if data and any("depth_path" in item for item in data.get("stills", []) + data.get("motion", [])):
        errors.append("depth_path must not exist for EP56")
    print(f"{'PASS' if not errors else 'FAIL'} postoffice_stills_qc checked={len(expected_ids())} errors={len(errors)}")
    for err in errors[:120]:
        print(f"  ! {err}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
