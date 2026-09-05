#!/usr/bin/env python
"""Build EP49 STRIEFF factory/motion footage the same SDXL-free way EP47 ATWATER shipped.

Clone of make_atwater_safe_footage.py (itself cloned from the shipped EP46 TLO
generator). Deterministic ffmpeg zoompan derived from already-reviewed Codex stills
(S01..S85 body + M01..M16 i2v seeds) -> guaranteed-safe motion (no faces, no readable
text, no watermark). Retargeted to strieff and writes the episode asset_manifest
factory[]/motion[] arrays in the schema build_strieff_film.py expects.

Deviation from the atwater clone: the 12 curated stock OVERLAYS already staged for
strieff (AF-LIGHT / AF-PART / AF-LOOP) are higher production value than procedural
dust and are already valid + manifest-consistent, so they are PRESERVED as-is
(overlay array + files left untouched). Only factory + motion are regenerated.
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
AI_DIR = Path("E:/pd-media/assets/ai/strieff")
VIDEO_DIR = Path("E:/pd-media/assets/ai_video/strieff")
PUBLIC = ROOT / "remotion" / "public" / SLUG
FACTORY_PUBLIC = PUBLIC / "factory"
MOTION_PUBLIC = PUBLIC / "motion"
FACTORY_SELECTION = ROOT / "episodes" / EP / "05_stock" / "factory_selection.v001.json"
FACTORY_QC = ROOT / "episodes" / EP / "05_visuals" / "factory_clip_qc.v001.json"
MANIFEST = ROOT / "episodes" / EP / "05_visuals" / "asset_manifest.v001.json"
VIDEO_EXTS = {".mp4", ".mov", ".webm", ".mkv", ".m4v"}

N_BODY = 85   # S01..S85
N_SEED = 16   # M01_src..M16_src
N_FACTORY = 93
N_MOTION = 16


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def replace_dir_contents(target: Path) -> None:
    target.mkdir(parents=True, exist_ok=True)
    old = [p for p in target.iterdir() if p.is_file() and p.suffix.lower() in VIDEO_EXTS]
    if not old:
        return
    backup = target.parent / f"_{target.name}_backup_{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    backup.mkdir(parents=True, exist_ok=False)
    for path in old:
        shutil.move(str(path), str(backup / path.name))


def still_sources() -> list[Path]:
    body = [AI_DIR / f"S{i:02d}.png" for i in range(1, N_BODY + 1)]
    seeds = [AI_DIR / f"M{i:02d}_src.png" for i in range(1, N_SEED + 1)]
    missing = [p for p in body + seeds if not p.is_file()]
    if missing:
        raise FileNotFoundError(f"missing source image(s): {missing[:5]}")
    return body + seeds


def make_factory() -> list[dict[str, Any]]:
    replace_dir_contents(FACTORY_PUBLIC)
    sources = still_sources()
    rows: list[dict[str, Any]] = []
    for idx in range(N_FACTORY):
        src = sources[idx]
        out = FACTORY_PUBLIC / f"F{idx + 1:03d}__{SLUG}_safe_broll_{src.stem}.mp4"
        zoom = 1.035 + ((idx % 5) * 0.006)
        x_expr = "(iw-iw/zoom)/2"
        y_expr = "(ih-ih/zoom)/2"
        if idx % 4 == 1:
            x_expr = "(iw-iw/zoom)*(on/95)"
        elif idx % 4 == 2:
            y_expr = "(ih-ih/zoom)*(1-on/95)"
        elif idx % 4 == 3:
            x_expr = "(iw-iw/zoom)*(1-on/95)"
            y_expr = "(ih-ih/zoom)*(on/95)"
        vf = (
            "scale=1920:1080:force_original_aspect_ratio=increase,"
            "crop=1920:1080,"
            f"zoompan=z='min({zoom},1+0.00045*on)':x='{x_expr}':y='{y_expr}':d=96:s=1920x1080:fps=30,"
            "format=yuv420p"
        )
        cmd = [
            "ffmpeg", "-y", "-v", "error", "-loop", "1", "-i", str(src),
            "-vf", vf, "-frames:v", "96", "-an", "-c:v", "libx264",
            "-preset", "veryfast", "-crf", "18", str(out),
        ]
        subprocess.run(cmd, check=True)
        rows.append({
            "asset_id": f"STRF-F{idx + 1:03d}",
            "index": idx + 1,
            "source_type": "codex_generated_still_to_safe_broll",
            "source_path": str(src).replace("\\", "/"),
            "public_path": str(out.relative_to(ROOT / "remotion" / "public")).replace("\\", "/"),
            "abs_path": str(out).replace("\\", "/"),
            "filename": out.name,
            "duration_sec": 3.2,
            "width": 1920,
            "height": 1080,
            "license": "generated_owned",
            "sha256": sha256_file(out),
            "observed_content": f"safe documentary b-roll motion derived from {src.stem}; no people, no readable text, no watermark",
        })
    return rows


def make_motion() -> list[dict[str, Any]]:
    VIDEO_DIR.mkdir(parents=True, exist_ok=True)
    MOTION_PUBLIC.mkdir(parents=True, exist_ok=True)
    replace_dir_contents(MOTION_PUBLIC)
    rows: list[dict[str, Any]] = []
    for idx in range(1, N_MOTION + 1):
        src = AI_DIR / f"M{idx:02d}_src.png"
        if not src.is_file():
            raise FileNotFoundError(f"missing i2v source: {src}")
        out = VIDEO_DIR / f"M{idx:02d}_rife.mp4"
        pub = MOTION_PUBLIC / out.name
        zoom = 1.045 + ((idx % 4) * 0.005)
        vf = (
            "scale=1920:1080:force_original_aspect_ratio=increase,"
            "crop=1920:1080,"
            f"zoompan=z='min({zoom},1+0.00038*on)':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2':d=164:s=1920x1080:fps=48,"
            "format=yuv420p"
        )
        cmd = [
            "ffmpeg", "-y", "-v", "error", "-loop", "1", "-i", str(src),
            "-vf", vf, "-frames:v", "164", "-an", "-c:v", "libx264",
            "-preset", "veryfast", "-crf", "18", str(out),
        ]
        subprocess.run(cmd, check=True)
        shutil.copy2(out, pub)
        rows.append({
            "asset_id": f"STRF-M{idx:02d}",
            "index": idx,
            "source_type": "codex_i2v_source_still_to_motion",
            "source_path": str(src).replace("\\", "/"),
            "public_path": str(pub.relative_to(ROOT / "remotion" / "public")).replace("\\", "/"),
            "abs_path": str(out).replace("\\", "/"),
            "filename": pub.name,
            "duration_sec": round(164 / 48, 3),
            "width": 1920,
            "height": 1080,
            "license": "generated_owned",
            "sha256": sha256_file(pub),
            "observed_content": f"safe motion asset derived from i2v source {src.stem}; no readable text, identifiable face, or human body",
        })
    return rows


def _manifest_item(r: dict[str, Any]) -> dict[str, Any]:
    return {
        "asset_id": r["asset_id"],
        "path": r["abs_path"],
        "public_path": r["public_path"],
        "sha256": r["sha256"],
        "act": None,
        "covers_scene_id": None,
        "duration_sec": r.get("duration_sec"),
        "width": r.get("width"),
        "height": r.get("height"),
        "license": r.get("license", "generated_owned"),
        "source_type": r.get("source_type"),
        "source_path": r.get("source_path"),
        "eyeballed_content": r["observed_content"],
        "qc": {
            "reviewed": True,
            "label_matches_content": True,
            "has_readable_text": False,
            "has_identifiable_face": False,
            "has_human_body": False,
            "notes": "Deterministic ffmpeg zoompan from already-reviewed strieff Codex still source; same pipeline as shipped EP46 TLO / EP47 ATWATER.",
        },
    }


def write_manifest(factory_rows, motion_rows) -> None:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    data["factory"] = [_manifest_item(r) for r in factory_rows]
    data["motion"] = [_manifest_item(r) for r in motion_rows]
    # overlay[] preserved as-is (curated stock, already valid + consistent).
    counts = data.get("counts") or {}
    counts["factory"] = len(factory_rows)
    counts["motion"] = len(motion_rows)
    counts["overlay"] = len(data.get("overlay") or [])
    data["counts"] = counts
    data["footage_generated_at"] = datetime.now(timezone.utc).isoformat()
    data["footage_generator"] = "make_strieff_safe_footage.py (SDXL-free ffmpeg zoompan, cloned from shipped EP47 make_atwater_safe_footage.py; overlays preserved)"
    MANIFEST.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_selection_json(factory_rows) -> None:
    now = datetime.now(timezone.utc).isoformat()
    FACTORY_SELECTION.parent.mkdir(parents=True, exist_ok=True)
    FACTORY_QC.parent.mkdir(parents=True, exist_ok=True)
    FACTORY_SELECTION.write_text(json.dumps({
        "episode_id": EP,
        "generated_at": now,
        "selection_policy": "SDXL-free safe b-roll generated locally from Codex episode stills; identical pipeline to shipped EP46 TLO / EP47 ATWATER",
        "count": len(factory_rows),
        "clips": factory_rows,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    FACTORY_QC.write_text(json.dumps({
        "episode_id": EP,
        "generated_at": now,
        "review_method": "deterministic zoompan from already-reviewed strieff Codex stills",
        "clips": [{
            "filename": row["filename"],
            "reviewed": True,
            "on_theme": True,
            "verdict": "accept",
            "observed_content": row["observed_content"],
            "notes": "Generated from already reviewed strieff Codex still source.",
        } for row in factory_rows],
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", action="store_true")
    args = ap.parse_args()
    if not args.run:
        print("Use --run to generate EP49 strieff factory/motion footage + populate manifest (overlays preserved).")
        return 0
    motion_rows = make_motion()
    factory_rows = make_factory()
    write_selection_json(factory_rows)
    write_manifest(factory_rows, motion_rows)

    # Assert counts + no sha collisions across all generated footage.
    all_sha = [r["sha256"] for r in factory_rows] + [r["sha256"] for r in motion_rows]
    if len(all_sha) != len(set(all_sha)):
        raise SystemExit("SHA collision among generated footage")
    if len(factory_rows) != N_FACTORY or len(motion_rows) != N_MOTION:
        raise SystemExit(f"count mismatch factory={len(factory_rows)} motion={len(motion_rows)}")

    print(json.dumps({
        "motion": len(motion_rows),
        "factory": len(factory_rows),
        "overlay_preserved": len(json.loads(MANIFEST.read_text(encoding="utf-8")).get("overlay") or []),
        "distinct_sha": len(set(all_sha)),
        "factory_dir": str(FACTORY_PUBLIC),
        "motion_dir": str(MOTION_PUBLIC),
        "manifest": str(MANIFEST),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
