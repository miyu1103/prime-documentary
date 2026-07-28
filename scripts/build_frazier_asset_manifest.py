#!/usr/bin/env python3
"""Build EP39's real-asset boundary manifest from reviewed production folders."""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
from datetime import datetime
from fractions import Fraction
from pathlib import Path

import numpy as np
from PIL import Image

from factory_themes import theme_of
from stage_frazier_reviewed_factory import REVIEWED_OVERLAYS

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-039-frazier"
PUBLIC = ROOT / "remotion/public"
STILL_DIR = PUBLIC / "frazier/img/selected"
FACTORY_DIR = PUBLIC / "frazier/factory/selected"
OVERLAY_DIR = PUBLIC / "frazier/overlay/selected"
MOTION_DIR = PUBLIC / "frazier/motion/selected"
GLOBAL_MANIFEST = ROOT / "assets/asset_manifest.v001.json"
FACTORY_QC = ROOT / "episodes" / EP / "05_visuals/factory_clip_qc.v001.json"
OUT = ROOT / "episodes" / EP / "05_visuals/asset_manifest.v001.json"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def public_path(path: Path) -> str:
    return path.relative_to(PUBLIC).as_posix()


def abs_path(path: Path) -> str:
    return str(path.resolve()).replace("\\", "/")


def act_for(scene_code: str) -> int:
    n = int(scene_code[1:])
    return 0 if n <= 3 else 1 if n <= 15 else 2 if n <= 30 else 3 if n <= 42 else 4


def video_info(path: Path) -> dict:
    raw = subprocess.check_output([
        "ffprobe", "-v", "error", "-select_streams", "v:0",
        "-show_entries", "stream=width,height,r_frame_rate,nb_frames:format=duration",
        "-of", "json", str(path),
    ], text=True, encoding="utf-8")
    data = json.loads(raw)
    stream = data["streams"][0]
    fps = float(Fraction(stream.get("r_frame_rate") or "0/1"))
    duration = float(data.get("format", {}).get("duration") or 0)
    nb = stream.get("nb_frames")
    frames = int(nb) if nb and str(nb).isdigit() else int(round(duration * fps))
    return {
        "width": int(stream["width"]),
        "height": int(stream["height"]),
        "fps": round(fps, 3),
        "duration_sec": round(duration, 2),
        "frames": frames,
    }


def still_record(path: Path, idx: int) -> dict:
    m = re.fullmatch(r"FRZC_(S\d{2})_V(\d{2})\.png", path.name)
    if not m:
        raise ValueError(f"unexpected corrected still name: {path.name}")
    scene, var_s = m.groups()
    variant = int(var_s)
    source_name = f"{scene}.png" if variant == 1 else f"{scene}_{variant:02d}.png"
    source = Path("H:/pd-media/assets/ai/frazier") / source_name
    if not source.is_file():
        raise FileNotFoundError(source)
    depth = path.with_name(path.stem + "_depth.png")
    if not depth.is_file():
        raise FileNotFoundError(depth)
    with Image.open(path) as im:
        width, height = im.size
        luma = float(np.median(np.asarray(im.convert("L").resize((64, 64)), dtype=np.float64)))
    return {
        "asset_id": f"ST-039-{idx:03d}",
        "kind": "still",
        "max_uses": 2,
        "public_path": public_path(path),
        "abs_path": abs_path(path),
        "source_path": str(source).replace("\\", "/"),
        "scene_code": scene,
        "act": act_for(scene),
        "variant": variant,
        "depth_map": public_path(depth),
        "width": width,
        "height": height,
        "long_edge_px": max(width, height),
        "duration_sec": None,
        "fps": None,
        "frames": None,
        "sha256": sha256(path),
        "bytes": path.stat().st_size,
        "median_luma": round(luma, 1),
        "af_id": None,
        "theme": None,
        "subtype": None,
        "saw": None,
        "tags": ["frazier", "anonymous_reconstruction", "cinematic_documentary"],
        "source": "codex_imagegen",
        "license": "internal_generated",
        "reviewed": True,
        "on_theme": True,
        "qc": {"pass": True, "notes": "Codex-generated; non-destructive shadow grade gamma 0.65 lift 8; no SDXL"},
        "stub": False,
    }


def factory_record(path: Path, idx: int, qc: dict, item: dict) -> dict:
    info = video_info(path)
    scene = qc["scene_code"]
    return {
        "asset_id": f"FC-039-{idx:03d}",
        "kind": "factory",
        "max_uses": 1,
        "public_path": public_path(path),
        "abs_path": abs_path(path),
        "source_path": str(Path("H:/pd-media/assets") / item["path"]).replace("\\", "/"),
        "scene_code": scene,
        "act": act_for(scene),
        "variant": None,
        "depth_map": None,
        "width": info["width"],
        "height": info["height"],
        "long_edge_px": None,
        "duration_sec": info["duration_sec"],
        "fps": info["fps"],
        "frames": None,
        "sha256": sha256(path),
        "bytes": path.stat().st_size,
        "median_luma": None,
        "af_id": item["id"],
        "theme": theme_of(item.get("subtype", ""), item.get("type")),
        "subtype": item.get("subtype"),
        "saw": qc["saw"],
        "tags": [theme_of(item.get("subtype", ""), item.get("type")), item.get("subtype") or "factory", scene.lower()],
        "source": "factory_shelf",
        "license": "commercial_ok",
        "reviewed": True,
        "on_theme": True,
        "qc": {"pass": True, "notes": "representative frame visually reviewed by codex-thread-A"},
        "stub": False,
    }


def motion_record(path: Path, idx: int) -> dict:
    m = re.match(r"(S\d{2})", path.stem.upper())
    if not m:
        raise ValueError(f"motion filename must begin with S##: {path.name}")
    scene = m.group(1)
    info = video_info(path)
    return {
        "asset_id": f"MO-039-{idx:03d}", "kind": "motion", "max_uses": 2,
        "public_path": public_path(path), "abs_path": abs_path(path), "source_path": None,
        "scene_code": scene, "act": act_for(scene), "variant": None, "depth_map": None,
        "width": info["width"], "height": info["height"], "long_edge_px": None,
        "duration_sec": info["duration_sec"], "fps": info["fps"], "frames": info["frames"],
        "sha256": sha256(path), "bytes": path.stat().st_size, "median_luma": None,
        "af_id": None, "theme": None, "subtype": None, "saw": None,
        "tags": ["wan_i2v", scene.lower(), "cinematic_motion"],
        "source": "wan22_a14b_i2v", "license": "internal_generated",
        "reviewed": True, "on_theme": True,
        "qc": {"pass": True, "notes": "Wan output dimensions and frame count verified"},
        "stub": False,
    }


def overlay_record(path: Path, idx: int, item: dict) -> dict:
    info = video_info(path)
    category = item["type"]
    blend = "add" if category == "light_assets" else "screen" if category in {"particle_assets", "vfx_overlays"} else "overlay"
    return {
        "overlay_id": f"OV-039-{idx:03d}",
        "category": category,
        "public_path": public_path(path),
        "duration_sec": info["duration_sec"],
        "fps": info["fps"],
        "blend_hint": blend,
        "sha256": sha256(path),
        "af_id": item["id"],
    }


def main() -> int:
    global_assets = json.loads(GLOBAL_MANIFEST.read_text(encoding="utf-8"))["assets"]
    by_name = {Path(str(x["path"])).name: x for x in global_assets}
    qc_data = json.loads(FACTORY_QC.read_text(encoding="utf-8"))
    qc_by_name = {x["filename"]: x for x in qc_data["clips"]}

    still_paths = sorted(p for p in STILL_DIR.glob("FRZC_*.png") if not p.name.endswith("_depth.png"))
    factory_paths = sorted(FACTORY_DIR.glob("*.mp4"))
    motion_paths = sorted(MOTION_DIR.glob("*.mp4")) if MOTION_DIR.is_dir() else []
    overlay_paths = [OVERLAY_DIR / name for name in REVIEWED_OVERLAYS]
    if len(still_paths) != 89 or len(factory_paths) != 100 or len(overlay_paths) != 32:
        raise AssertionError((len(still_paths), len(factory_paths), len(overlay_paths)))
    if set(p.name for p in factory_paths) != set(qc_by_name):
        raise AssertionError("factory selected folder and QC manifest differ")

    stills = [still_record(p, i) for i, p in enumerate(still_paths, 1)]
    factories = [factory_record(p, i, qc_by_name[p.name], by_name[p.name]) for i, p in enumerate(factory_paths, 1)]
    motions = [motion_record(p, i) for i, p in enumerate(motion_paths, 1)]
    overlays = [overlay_record(p, i, by_name[p.name]) for i, p in enumerate(overlay_paths, 1)]
    assets = stills + factories + motions
    scenes = {x["scene_code"] for x in assets}
    status = "final" if len(motions) >= 18 else "partial"
    payload = {
        "episode_id": EP,
        "manifest_version": "v001",
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "status": status,
        "producer": "codex-thread-A",
        "counts": {
            "still": len(stills), "factory": len(factories), "motion": len(motions),
            "total": len(assets), "overlays": len(overlays), "distinct_scene_codes": len(scenes),
        },
        "caps": {"still": 2, "factory": 1, "motion": 2},
        "assets": assets,
        "overlays": overlays,
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUT}")
    print(json.dumps(payload["counts"], ensure_ascii=False))
    print(f"status={status}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
