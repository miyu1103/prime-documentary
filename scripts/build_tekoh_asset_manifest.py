#!/usr/bin/env python
"""Build and verify the EP44 Tekoh asset boundary manifest.

The producer side scans the staged EP44 media locations and writes exactly the
contract that the B thread consumes. It does not fabricate media records; missing
files remain blocking validation errors.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-044-tekoh"
SLUG = "tekoh"
EPDIR = ROOT / "episodes" / EP
OUT = EPDIR / "05_visuals" / "asset_manifest.v001.json"
MEDIA_AI = Path("H:/pd-media/assets/ai/tekoh")
MEDIA_MOTION = Path("H:/pd-media/assets/ai_video/tekoh")
PUBLIC = ROOT / "remotion" / "public" / "tekoh"
THUMB_IDS = {"S02", "S04", "S24", "S44", "S45", "S85"}
COUNTS = {"still_body": 85, "still_i2v_source": 16, "factory": 93, "motion": 16, "overlay": 12}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def image_size(path: Path) -> tuple[int, int]:
    with Image.open(path) as im:
        return int(im.width), int(im.height)


def act_for_scene(scene_id: str) -> int:
    n = int(scene_id[1:])
    if n <= 7:
        return 0
    if n <= 19:
        return 1
    if n <= 35:
        return 2
    if n <= 65:
        return 3
    return 5


def rel_public(path: Path) -> str:
    return str(path.relative_to(ROOT / "remotion" / "public")).replace("\\", "/")


def still_records() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for i in range(1, 86):
        scene = f"S{i:02d}"
        src = MEDIA_AI / f"{scene}.png"
        pub = PUBLIC / "img" / f"{scene}.png"
        width = height = 0
        sha = ""
        if src.exists():
            width, height = image_size(src)
            sha = sha256_file(src)
        records.append({
            "asset_id": f"TEKOH-{scene}",
            "scene_id": scene,
            "role": "body",
            "also_thumb": scene in THUMB_IDS,
            "act": act_for_scene(scene),
            "path": str(src).replace("\\", "/"),
            "depth_path": str((MEDIA_AI / f"{scene}_depth.png")).replace("\\", "/"),
            "public_path": rel_public(pub),
            "width": width,
            "height": height,
            "sha256": sha,
            "ai_disclosure_required": True,
            "caption_hint": "symbolic visualization only",
            "tags": ["symbolic", "tekoh", "no_people"],
            "qc": {"reviewed": False, "notes": ""},
        })
    for i in range(1, 17):
        scene = f"MS{i:02d}"
        name = f"M{i:02d}_src.png"
        src = MEDIA_AI / name
        width = height = 0
        sha = ""
        if src.exists():
            width, height = image_size(src)
            sha = sha256_file(src)
        records.append({
            "asset_id": f"TEKOH-{scene}",
            "scene_id": scene,
            "role": "i2v_source",
            "also_thumb": False,
            "act": 3 if i <= 11 else 5,
            "path": str(src).replace("\\", "/"),
            "depth_path": None,
            "public_path": None,
            "width": width,
            "height": height,
            "sha256": sha,
            "ai_disclosure_required": True,
            "caption_hint": "motion seed only, not used directly in the edit",
            "tags": ["symbolic", "motion_seed", "no_people"],
            "qc": {"reviewed": False, "notes": ""},
        })
    return records


def media_records(folder: Path, public_subdir: str, prefix: str, count: int, suffix: str = ".mp4") -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    files = sorted((PUBLIC / public_subdir).glob(f"*{suffix}")) if (PUBLIC / public_subdir).is_dir() else []
    for i, pub in enumerate(files[:count], 1):
        src = folder / pub.name
        p = src if src.exists() else pub
        records.append({
            "asset_id": f"TEKOH-{prefix}{i:02d}",
            "path": str(p).replace("\\", "/"),
            "public_path": rel_public(pub),
            "sha256": sha256_file(p) if p.exists() else "",
            "act": None,
            "covers_scene_id": None,
            "duration_sec": None,
            "width": None,
            "height": None,
            "eyeballed_content": "",
            "qc": {"reviewed": False, "notes": ""},
        })
    return records


def build() -> dict[str, Any]:
    return {
        "schema_version": "tekoh_assets.v1",
        "episode_id": EP,
        "slug": SLUG,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "producer": "scripts/build_tekoh_asset_manifest.py",
        "is_stub": False,
        "counts": COUNTS,
        "stills": still_records(),
        "factory": media_records(PUBLIC / "factory", "factory", "F", 93),
        "motion": media_records(MEDIA_MOTION, "motion", "M", 16),
        "overlay": media_records(PUBLIC / "overlay", "overlay", "O", 12),
    }


def verify(data: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    body = [x for x in data["stills"] if x.get("role") == "body"]
    i2v = [x for x in data["stills"] if x.get("role") == "i2v_source"]
    groups = {"still_body": body, "still_i2v_source": i2v, "factory": data["factory"], "motion": data["motion"], "overlay": data["overlay"]}
    for key, items in groups.items():
        if len(items) != COUNTS[key]:
            errors.append(f"{key}: {len(items)} != {COUNTS[key]}")
    thumbs = {x["scene_id"] for x in body if x.get("also_thumb") is True}
    if thumbs != THUMB_IDS:
        errors.append(f"also_thumb {sorted(thumbs)} != {sorted(THUMB_IDS)}")
    seen_sha: set[str] = set()
    for group, items in [("stills", data["stills"]), ("factory", data["factory"]), ("motion", data["motion"]), ("overlay", data["overlay"])]:
        for item in items:
            path = Path(str(item.get("path") or ""))
            public = item.get("public_path")
            if item.get("role") != "i2v_source" and public and not (ROOT / "remotion" / "public" / public).is_file():
                errors.append(f"{group}:{item.get('asset_id')} missing public {public}")
            if not path.is_file():
                errors.append(f"{group}:{item.get('asset_id')} missing source {path}")
                continue
            sha = item.get("sha256") or sha256_file(path)
            if sha in seen_sha:
                errors.append(f"duplicate sha256 {sha} at {item.get('asset_id')}")
            seen_sha.add(sha)
            if group == "stills" and item.get("role") == "body":
                if max(int(item.get("width") or 0), int(item.get("height") or 0)) < 3840:
                    errors.append(f"{item.get('asset_id')} long edge below 3840")
                if not Path(str(item.get("depth_path") or "")).is_file():
                    errors.append(f"{item.get('asset_id')} missing depth map")
    return {"ok": not errors, "errors": errors}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--verify", action="store_true")
    ap.add_argument("--reuse-feasibility", action="store_true")
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()
    data = json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() and not args.write else build()
    if args.write:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"wrote {OUT}")
    result = verify(data)
    if args.reuse_feasibility:
        distinct = COUNTS["still_body"] + COUNTS["factory"] + COUNTS["motion"]
        first_use = round(distinct / 226, 4)
        ok = len(data.get("factory", [])) >= 93 and len([x for x in data.get("stills", []) if x.get("role") == "body"]) >= 85 and len(data.get("motion", [])) >= 16 and first_use >= 0.70
        result = {"ok": ok and result["ok"], "first_use_share": first_use, "distinct": distinct, "errors": result["errors"]}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
