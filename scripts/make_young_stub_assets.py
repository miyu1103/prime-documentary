#!/usr/bin/env python
"""Create EP42 Young dry-run media and a stub asset manifest.

Writes only local dry-run media under remotion/public/young_dryrun plus the
stub manifest required by the EP42 build handoff. It never writes production
media under remotion/public/young or E:/pd-media.
"""
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-042-young"
SLUG = "young"
EPDIR = ROOT / "episodes" / EP
PUBLIC = ROOT / "remotion" / "public" / "young_dryrun"
OUT = EPDIR / "05_visuals" / "asset_manifest.stub.v001.json"
DRY_EDIT = EPDIR / "08_edit" / "_dryrun"
FFMPEG = shutil.which("ffmpeg") or r"C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe"
FFPROBE = shutil.which("ffprobe") or r"C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffprobe.exe"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def make_png(path: Path, label: str, color: tuple[int, int, int], size=(3840, 2160)) -> None:
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    im = Image.new("RGB", size, color)
    d = ImageDraw.Draw(im)
    darker = tuple(max(0, c - 18) for c in color)
    lighter = tuple(min(255, c + 34) for c in color)
    for x in range(0, size[0], 160):
        d.line((x, 0, x, size[1]), fill=darker, width=2)
    for y in range(0, size[1], 160):
        d.line((0, y, size[0], y), fill=darker, width=2)
    d.rectangle((size[0] * 0.16, size[1] * 0.18, size[0] * 0.84, size[1] * 0.82), outline=lighter, width=10)
    d.text((size[0] // 2 - 260, size[1] // 2 - 28), label, fill=(245, 247, 250))
    im.save(path)


def make_depth(path: Path, size=(3840, 2160)) -> None:
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    depth = Image.radial_gradient("L").resize(size, Image.Resampling.BILINEAR)
    Image.eval(depth, lambda v: 255 - int(v * 0.72)).save(path)


def ffmpeg_color(path: Path, color: str, dur: float, size: str, fps: int) -> None:
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            FFMPEG,
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-f",
            "lavfi",
            "-i",
            f"color=c={color}:s={size}:r={fps}:d={dur}",
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-movflags",
            "+faststart",
            str(path),
        ],
        check=True,
    )


def ffmpeg_silence(path: Path, dur: float) -> None:
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            FFMPEG,
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-f",
            "lavfi",
            "-i",
            "anullsrc=r=48000:cl=stereo",
            "-t",
            f"{dur:.3f}",
            "-c:a",
            "aac",
            "-b:a",
            "64k",
            str(path),
        ],
        check=True,
    )


def color_hex(seed: int, base: tuple[int, int, int]) -> str:
    r = max(0, min(255, base[0] + (seed * 17) % 70))
    g = max(0, min(255, base[1] + (seed * 29) % 68))
    b = max(0, min(255, base[2] + (seed * 37) % 62))
    return f"0x{r:02x}{g:02x}{b:02x}"


def still_item(asset_id: str, scene_id: str, role: str, idx: int, color: tuple[int, int, int]) -> dict:
    name = f"{scene_id}_{role}_{idx:03d}.png"
    rel = Path("img") / name
    path = PUBLIC / rel
    make_png(path, f"{scene_id} {role}", color)
    depth_path = None
    if role != "thumb":
        depth_path = path.with_name(path.stem + "_depth.png")
        make_depth(depth_path)
    return {
        "asset_id": asset_id,
        "scene_id": scene_id,
        "role": role,
        "path": str(path).replace("\\", "/"),
        "depth_path": str(depth_path).replace("\\", "/") if depth_path else None,
        "public_path": f"young_dryrun/{rel.as_posix()}",
        "width": 3840,
        "height": 2160,
        "sha256": sha256(path),
        "mean_luma": 72.0 + (idx % 40),
        "tags": ["stub", role, "symbolic", "ai-assisted visualization"],
        "caption_hint": f"symbolic dry-run {role} {scene_id}",
        "prompt_sha256": hashlib.sha256(asset_id.encode("utf-8")).hexdigest(),
        "seed": 42000000 + idx,
        "model": "local-stub",
        "source": "stub",
        "commercial_use": "allowed",
        "ai_disclosure_required": True,
        "also_thumb": scene_id in {"S05", "S30", "S60", "S63", "S74", "S84"},
        "qc": {
            "reviewed": True,
            "on_theme": True,
            "has_readable_text": False,
            "has_identifiable_face": False,
            "notes": "dry-run symbolic placeholder, no people",
        },
    }


def main() -> int:
    for rel in ["img", "factory", "motion", "overlay", "audio"]:
        (PUBLIC / rel).mkdir(parents=True, exist_ok=True)
    for rel in ["00_topic", "01_research", "03_script", "04_scenes", "05_visuals", "06_audio", "08_edit", "09_package", "approvals", "events"]:
        (EPDIR / rel).mkdir(parents=True, exist_ok=True)
    DRY_EDIT.mkdir(parents=True, exist_ok=True)

    stills = []
    for i in range(1, 86):
        stills.append(still_item(f"YOUNG-S{i:02d}", f"S{i:02d}", "body", i, (18 + i % 36, 36 + i % 42, 70 + i % 74)))
    for i in range(1, 9):
        stills.append(still_item(f"YOUNG-AE-{i:02d}", f"AE{i:02d}", "ae", i, (42, 54 + i * 3, 86 + i * 4)))
    for i in range(1, 7):
        stills.append(still_item(f"YOUNG-TH-{i:02d}", f"TH{i:02d}", "thumb", i, (32 + i * 4, 50, 92 + i * 6)))

    factory = []
    for i in range(1, 94):
        name = f"AF-YOUNG-STUB-{i:04d}__symbolic_motion.mp4"
        path = PUBLIC / "factory" / name
        ffmpeg_color(path, color_hex(i, (16, 22, 36)), 4.2, "1920x1080", 30)
        factory.append({
            "asset_id": f"AF-YOUNG-STUB-{i:04d}",
            "path": str(path).replace("\\", "/"),
            "public_path": f"young_dryrun/factory/{name}",
            "kind": "video",
            "duration_sec": 4.2,
            "width": 1920,
            "height": 1080,
            "sha256": sha256(path),
            "tags": ["stub", "factory", "symbolic"],
            "qc": {"reviewed": True, "on_theme": True, "no_watermark": True, "no_recognizable_person": True, "notes": "dry-run clip"},
        })

    motion = []
    for i in range(1, 17):
        name = f"M{i:02d}_symbolic_motion.mp4"
        path = PUBLIC / "motion" / name
        ffmpeg_color(path, color_hex(i, (20, 34, 58)), 3.417, "1920x1080", 30)
        motion.append({
            "asset_id": f"YOUNG-M{i:02d}",
            "source_scene_id": f"S{min(85, i * 5):02d}",
            "path": str(path).replace("\\", "/"),
            "public_path": f"young_dryrun/motion/{name}",
            "kind": "video",
            "duration_sec": 3.417,
            "width": 1920,
            "height": 1080,
            "sha256": sha256(path),
            "tags": ["stub", "motion", "symbolic"],
            "qc": {"reviewed": True, "on_theme": True, "artifact_free": True, "notes": "dry-run motion clip"},
        })

    overlay = []
    for i in range(1, 13):
        name = f"AF-YOUNG-OVERLAY-{i:04d}__dust.mp4"
        path = PUBLIC / "overlay" / name
        ffmpeg_color(path, color_hex(i, (8, 10, 14)), 2.0, "1920x1080", 30)
        overlay.append({
            "asset_id": f"AF-YOUNG-OVERLAY-{i:04d}",
            "path": str(path).replace("\\", "/"),
            "public_path": f"young_dryrun/overlay/{name}",
            "kind": "video",
            "blend_hint": "screen",
            "sha256": sha256(path),
            "qc": {"reviewed": True, "on_theme": True, "no_watermark": True, "notes": "dry-run overlay"},
        })

    ffmpeg_silence(PUBLIC / "audio" / "silence.m4a", 720.9)
    ffmpeg_color(DRY_EDIT / "young_final_bgm.v002.mp4", "0x0a0a0c", 733.4, "1920x1080", 30)

    manifest = {
        "schema_version": "young_assets.v1",
        "episode_id": EP,
        "slug": SLUG,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "producer": "scripts/make_young_stub_assets.py",
        "is_stub": True,
        "counts": {
            "still_body": 85,
            "still_ae": 8,
            "still_thumb": 6,
            "motion": 16,
            "factory": 93,
            "overlay": 12,
        },
        "stills": stills,
        "motion": motion,
        "factory": factory,
        "overlay": overlay,
    }
    OUT.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
