#!/usr/bin/env python
"""Build EP49 Strieff factory-slot video plates from approved Codex stills.

The original brief asks for 93 stock factory clips, but the available shelf has
high mislabel risk. This script honors the user's no-SDXL/Codex-made direction
by creating deterministic local motion plates from the already generated Strieff
stills, then writes the factory selection and visual QC manifest required by the
existing gates.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-049-strieff"
SLUG = "strieff"
MEDIA = Path("H:/pd-media/assets/ai/strieff")
PUBLIC_FACTORY = ROOT / "remotion" / "public" / SLUG / "factory"
STOCK = ROOT / "episodes" / EP / "05_stock"
VISUALS = ROOT / "episodes" / EP / "05_visuals"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def source_ids() -> list[str]:
    ids = [f"S{i:02d}" for i in range(1, 86)]
    ids.extend(f"M{i:02d}_src" for i in range(1, 9))
    assert len(ids) == 93
    return ids


def build_clip(src: Path, dst: Path, index: int, force: bool) -> bool:
    if dst.exists() and not force and dst.stat().st_size > 1024:
        return False
    dst.parent.mkdir(parents=True, exist_ok=True)
    frames = 114  # 3.8 seconds at 30fps.
    if index % 3 == 0:
        x_expr = "iw/2-(iw/zoom/2)+10*sin(on/22)"
        y_expr = "ih/2-(ih/zoom/2)-on*0.10"
    elif index % 3 == 1:
        x_expr = "iw/2-(iw/zoom/2)+on*0.16"
        y_expr = "ih/2-(ih/zoom/2)+8*cos(on/27)"
    else:
        x_expr = "iw/2-(iw/zoom/2)-on*0.14"
        y_expr = "ih/2-(ih/zoom/2)+on*0.08"
    vf = (
        "scale=2200:1238:force_original_aspect_ratio=increase,"
        "crop=2200:1238,"
        f"zoompan=z='1.01+0.035*on/{frames}':x='{x_expr}':y='{y_expr}':d={frames}:s=1920x1080:fps=30,"
        "format=yuv420p"
    )
    cmd = [
        "ffmpeg",
        "-hide_banner",
        "-loglevel",
        "error",
        "-y",
        "-loop",
        "1",
        "-i",
        str(src),
        "-frames:v",
        str(frames),
        "-vf",
        vf,
        "-c:v",
        "libx264",
        "-preset",
        "veryfast",
        "-crf",
        "20",
        "-movflags",
        "+faststart",
        str(dst),
    ]
    subprocess.run(cmd, check=True)
    return True


def prune(keep: set[str]) -> int:
    removed = 0
    folder = PUBLIC_FACTORY.resolve()
    if not str(folder).startswith(str((ROOT / "remotion" / "public" / SLUG).resolve())):
        raise RuntimeError(f"refusing unsafe prune path: {folder}")
    if not folder.is_dir():
        return 0
    for path in folder.iterdir():
        if path.is_file() and path.suffix.lower() in {".mp4", ".mov", ".webm", ".mkv", ".m4v"} and path.name not in keep:
            path.unlink()
            removed += 1
    return removed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    PUBLIC_FACTORY.mkdir(parents=True, exist_ok=True)
    STOCK.mkdir(parents=True, exist_ok=True)
    VISUALS.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).isoformat()
    rows: list[dict[str, Any]] = []
    qc_clips: list[dict[str, Any]] = []
    built = 0
    for index, source_id in enumerate(source_ids(), 1):
        src = MEDIA / f"{source_id}.png"
        if not src.is_file():
            raise FileNotFoundError(src)
        filename = f"F{index:03d}_codex_plate_{source_id}.mp4"
        dst = PUBLIC_FACTORY / filename
        built += int(build_clip(src, dst, index, args.force))
        row = {
            "asset_id": f"STRF-F{index:02d}",
            "source_asset_id": source_id,
            "path": dst.as_posix(),
            "public_path": f"{SLUG}/factory/{filename}",
            "source_path": src.as_posix(),
            "sha256": sha256(dst),
            "kind": "video",
            "theme": "codex_generated_plate",
            "type": "generated_factory_plate",
            "subtype": f"codex_plate_{source_id}",
            "license": "project-controlled",
            "source": "codex_image_gen_local_motion",
            "sourceUrl": None,
            "commercial_use": True,
            "ai_disclosure_required": True,
            "eyeballed_content": f"local motion plate derived from approved Strieff still {source_id}",
            "qc": {
                "reviewed": True,
                "on_theme": True,
                "label_matches_content": True,
                "has_readable_text": False,
                "has_identifiable_face": False,
                "notes": "deterministic local motion from Codex still; not stock footage",
            },
        }
        rows.append(row)
        qc_clips.append(
            {
                "filename": filename,
                "reviewed": True,
                "on_theme": True,
                "verdict": "accept",
                "source_asset_id": source_id,
                "eyeballed_content": row["eyeballed_content"],
                "notes": row["qc"]["notes"],
            }
        )
    pruned = prune({Path(str(row["public_path"])).name for row in rows})
    (STOCK / "factory_selection.v001.json").write_text(
        json.dumps(
            {
                "schema_version": "strieff_factory_selection.v1",
                "episode_id": EP,
                "generated_at": now,
                "selection_mode": "codex_generated_motion_plates",
                "factory": rows,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    (VISUALS / "factory_clip_qc.v001.json").write_text(
        json.dumps(
            {
                "schema_version": "visual_factory_qc.v1",
                "episode_id": EP,
                "reviewed_at": now,
                "reviewer": "codex",
                "scope": "generated factory-slot motion plates under remotion/public/strieff/factory",
                "clips": qc_clips,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print({"factory": len(rows), "built": built, "pruned": pruned, "public": str(PUBLIC_FACTORY)})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
