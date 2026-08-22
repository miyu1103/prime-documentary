#!/usr/bin/env python
"""Import the latest Codex built-in imagegen output for EP59 robosigning."""
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-059-robosigning"
QUEUE = ROOT / "episodes" / EP / "05_visuals" / "imagegen_prompt_queue.v001.json"
MEDIA_AI = Path("E:/pd-media/assets/ai/robosigning")
PUBLIC = ROOT / "remotion" / "public" / "robosigning"
GEN_ROOT = Path.home() / ".codex" / "generated_images"
TARGET_SIZE = (3840, 2160)


def generated_files() -> list[Path]:
    if not GEN_ROOT.is_dir():
        return []
    return sorted(
        [p for p in GEN_ROOT.rglob("*.png") if p.is_file()],
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )


def queue_item(asset_id: str) -> dict:
    data = json.loads(QUEUE.read_text(encoding="utf-8"))
    for item in data["items"]:
        if item["asset_id"] == asset_id or Path(item["file"]).stem == asset_id:
            return item
    raise SystemExit(f"asset not found in queue: {asset_id}")


def public_dir_for(asset_id: str) -> Path | None:
    if asset_id.startswith("S") or asset_id.startswith("M"):
        return PUBLIC / "img"
    if asset_id.startswith("T"):
        return PUBLIC / "thumb"
    if asset_id.startswith("F"):
        return PUBLIC / "face"
    return None


def import_image(src: Path, asset_id: str, replace: bool = False) -> dict:
    item = queue_item(asset_id)
    out = MEDIA_AI / item["file"]
    if out.exists() and not replace:
        raise SystemExit(f"target already exists, refusing overwrite: {out}")
    MEDIA_AI.mkdir(parents=True, exist_ok=True)
    with Image.open(src) as im:
        im = im.convert("RGB")
        # Center-crop to 16:9, then upscale to the technical delivery size.
        w, h = im.size
        target_ratio = TARGET_SIZE[0] / TARGET_SIZE[1]
        ratio = w / h
        if ratio > target_ratio:
            nw = int(h * target_ratio)
            left = (w - nw) // 2
            im = im.crop((left, 0, left + nw, h))
        elif ratio < target_ratio:
            nh = int(w / target_ratio)
            top = (h - nh) // 2
            im = im.crop((0, top, w, top + nh))
        im = im.resize(TARGET_SIZE, Image.Resampling.LANCZOS)
        im.save(out, "PNG", optimize=True)
    pub_dir = public_dir_for(asset_id)
    public_path = None
    if pub_dir is not None:
        pub_dir.mkdir(parents=True, exist_ok=True)
        public_path = pub_dir / item["file"]
        if public_path.exists() and not replace:
            raise SystemExit(f"public target already exists, refusing overwrite: {public_path}")
        shutil.copyfile(out, public_path)
    return {
        "asset_id": asset_id,
        "source": str(src),
        "media": str(out),
        "public": str(public_path) if public_path else None,
        "width": TARGET_SIZE[0],
        "height": TARGET_SIZE[1],
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("asset_id", nargs="?")
    ap.add_argument("--src")
    ap.add_argument("--latest", action="store_true")
    ap.add_argument("--recent", nargs="+", help="Import the newest N generated images into these asset ids, oldest-to-newest.")
    ap.add_argument("--replace", action="store_true", help="Replace an asset created by this importer.")
    args = ap.parse_args()
    if args.recent:
        files = generated_files()
        if len(files) < len(args.recent):
            raise SystemExit(f"need {len(args.recent)} generated images, found {len(files)}")
        selected = list(reversed(files[: len(args.recent)]))
        results = [import_image(src, asset_id, replace=args.replace) for src, asset_id in zip(selected, args.recent)]
        print(json.dumps(results, ensure_ascii=False, indent=2))
        return 0
    if not args.asset_id:
        raise SystemExit("provide asset_id or --recent")
    if args.latest:
        files = generated_files()
        if not files:
            raise SystemExit(f"no generated images under {GEN_ROOT}")
        src = files[0]
    elif args.src:
        src = Path(args.src)
    else:
        raise SystemExit("provide --src <path> or --latest")
    if not src.is_file():
        raise SystemExit(f"source not found: {src}")
    print(json.dumps(import_image(src, args.asset_id, replace=args.replace), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
