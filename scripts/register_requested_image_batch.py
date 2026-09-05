#!/usr/bin/env python
"""Register the 2026-08-02 requested still additions in existing v003 manifests.

The operation is additive, validates the exact files, backs up each manifest, and is
idempotent. It intentionally avoids rescanning unrelated factory video assets.
"""

from __future__ import annotations

import json
import shutil
from datetime import datetime
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
BACKUP_SUFFIX = ".before-requested-images-20260802.bak"

CONFIG = {
    "postoffice": {
        "episode": "PD-2026-056-postoffice",
        "prefix": "POS-S-",
        "ids": [f"S{i:03d}" for i in range(211, 225)],
        "people": False,
    },
    "fieldtest": {
        "episode": "PD-2026-057-fieldtest",
        "prefix": "FIE-PPL-",
        "ids": [f"P{i:03d}" for i in range(3, 15)],
        "people": True,
    },
    "lejeune": {
        "episode": "PD-2026-058-lejeune",
        "prefix": "LEJ-S-",
        "ids": [f"S{i:03d}" for i in range(211, 225)],
        "people": False,
    },
    "robosigning": {
        "episode": "PD-2026-059-robosigning",
        "prefix": "ROB-S-",
        "ids": [f"S{i:03d}" for i in range(211, 225)],
        "people": False,
    },
}


def entry(slug: str, prefix: str, scene_id: str, people: bool) -> dict[str, object]:
    path = ROOT / "remotion" / "public" / slug / "img" / f"{scene_id}.png"
    if not path.is_file():
        raise SystemExit(f"missing requested image: {path}")
    with Image.open(path) as image:
        image.verify()
    with Image.open(path) as image:
        if image.size != (3840, 2160):
            raise SystemExit(f"unexpected dimensions for {path}: {image.size}")
    number = int(scene_id[1:])
    return {
        "asset_id": f"{prefix}{number:03d}",
        "path": str(path).replace("\\", "/"),
        "public_path": f"{slug}/img/{scene_id}.png",
        "bytes": path.stat().st_size,
        "role": "visible_face" if people else "body",
        "scene_id": scene_id,
    }


def update(slug: str, config: dict[str, object]) -> dict[str, object]:
    manifest = ROOT / "episodes" / str(config["episode"]) / "05_visuals" / "asset_manifest.v003.json"
    data = json.loads(manifest.read_text(encoding="utf-8-sig"))
    backup = manifest.with_name(manifest.name + BACKUP_SUFFIX)
    if not backup.exists():
        shutil.copy2(manifest, backup)

    existing_asset_ids = {item["asset_id"] for item in data["stills"]}
    existing_by_scene = {item["scene_id"]: item for item in data["stills"]}
    added = 0
    for scene_id in config["ids"]:
        item = entry(slug, str(config["prefix"]), scene_id, bool(config["people"]))
        if scene_id in existing_by_scene:
            existing_by_scene[scene_id].update(item)
            if config["people"]:
                for person in data["people"]:
                    if person["scene_id"] == scene_id:
                        person.update(item)
                        break
            continue
        if item["asset_id"] in existing_asset_ids:
            raise SystemExit(f"asset id collision for {slug}: {item['asset_id']}")
        data["stills"].append(item)
        if config["people"]:
            data["people"].append(item.copy())
        added += 1

    if config["people"]:
        data["counts"]["people"] = len(data["people"])
    else:
        data["counts"]["stills"] = sum(1 for item in data["stills"] if item["role"] == "body")
    data["generated_at"] = datetime.now().astimezone().isoformat()
    data["producer"] = "scripts/register_requested_image_batch.py"

    temporary = manifest.with_suffix(manifest.suffix + ".tmp")
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(manifest)
    return {
        "slug": slug,
        "added": added,
        "stills": data["counts"]["stills"],
        "people": data["counts"]["people"],
        "backup": str(backup),
    }


def main() -> int:
    print(json.dumps([update(slug, config) for slug, config in CONFIG.items()], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
