"""Prepare review sheets and R-ESRGAN upscaled visual assets for PD-2026-004-ftx.

Uses local A1111 API only. No external API, upload, or paid call.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import time
from pathlib import Path

import requests
from PIL import Image, ImageDraw, ImageOps


API = "http://127.0.0.1:7860"
EP = "PD-2026-004-ftx"
MEDIA = Path(r"H:\pd-media")
VIS = MEDIA / "episodes" / EP / "05_visuals"
SRC_DIRS = [
    VIS / "openai_heroes",
    VIS / "sdxl_coverage_hq_v001",
]
UPSCALED = VIS / "upscaled_4x_v001"
REVIEW = VIS / "_review"
MANIFEST = VIS / "asset_manifest.v001.json"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return "sha256:" + h.hexdigest()


def images() -> list[Path]:
    found: list[Path] = []
    for root in SRC_DIRS:
        if root.exists():
            found.extend(sorted(root.rglob("*.png")))
    return found


def make_sheet(paths: list[Path], out: Path, cols: int = 4) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    thumb_w, thumb_h, label_h = 360, 203, 48
    rows = (len(paths) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * thumb_w, rows * (thumb_h + label_h)), (18, 18, 20))
    draw = ImageDraw.Draw(sheet)
    for idx, path in enumerate(paths):
        im = Image.open(path).convert("RGB")
        thumb = ImageOps.contain(im, (thumb_w, thumb_h), Image.Resampling.LANCZOS)
        canvas = Image.new("RGB", (thumb_w, thumb_h), (5, 5, 6))
        canvas.paste(thumb, ((thumb_w - thumb.width) // 2, (thumb_h - thumb.height) // 2))
        x = (idx % cols) * thumb_w
        y = (idx // cols) * (thumb_h + label_h)
        sheet.paste(canvas, (x, y))
        label = path.stem.replace("PD-2026-004-ftx-", "")
        draw.rectangle([x, y + thumb_h, x + thumb_w, y + thumb_h + label_h], fill=(30, 30, 34))
        draw.text((x + 8, y + thumb_h + 6), label[:46], fill=(238, 238, 238))
        draw.text((x + 8, y + thumb_h + 25), f"{im.width}x{im.height}", fill=(175, 175, 178))
    sheet.save(out, quality=92)


def upscale_one(src: Path, dst: Path, scale: int = 4) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        return
    encoded = base64.b64encode(src.read_bytes()).decode("ascii")
    body = {
        "image": encoded,
        "upscaling_resize": scale,
        "upscaler_1": "R-ESRGAN 4x+",
        "upscaler_2": "None",
    }
    response = requests.post(f"{API}/sdapi/v1/extra-single-image", json=body, timeout=360)
    response.raise_for_status()
    dst.write_bytes(base64.b64decode(response.json()["image"]))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--upscale", action="store_true")
    parser.add_argument("--limit", type=int, default=0)
    args = parser.parse_args()

    paths = images()
    if args.limit:
        paths = paths[: args.limit]
    REVIEW.mkdir(parents=True, exist_ok=True)
    make_sheet(paths, REVIEW / "ftx_visual_assets_contact_sheet.v001.jpg")

    records = []
    started = time.time()
    for idx, src in enumerate(paths, start=1):
        rel = src.relative_to(VIS)
        dst = UPSCALED / rel
        if args.upscale:
            print(f"[{idx}/{len(paths)}] upscale {rel}", flush=True)
            upscale_one(src, dst)
        chosen = dst if dst.exists() else src
        with Image.open(chosen) as im:
            w, h = im.size
        records.append(
            {
                "episode_id": EP,
                "asset_id": chosen.stem,
                "source_file": str(src),
                "prepared_file": str(chosen),
                "width": w,
                "height": h,
                "sha256": sha256(chosen),
                "rights_basis": "owner/generated local project asset; no external upload by Codex",
                "r2_guard": "anonymous/symbolic only; no real-person likeness intended",
            }
        )

    upscaled_paths = [Path(r["prepared_file"]) for r in records if Path(r["prepared_file"]).exists()]
    make_sheet(upscaled_paths, REVIEW / "ftx_visual_assets_prepared_contact_sheet.v001.jpg")
    MANIFEST.write_text(
        json.dumps(
            {
                "episode_id": EP,
                "revision": "v001",
                "kind": "visual_asset_manifest",
                "count": len(records),
                "created_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
                "duration_sec": round(time.time() - started, 2),
                "external_side_effects": "none",
                "records": records,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print(REVIEW / "ftx_visual_assets_contact_sheet.v001.jpg")
    print(REVIEW / "ftx_visual_assets_prepared_contact_sheet.v001.jpg")
    print(MANIFEST)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
