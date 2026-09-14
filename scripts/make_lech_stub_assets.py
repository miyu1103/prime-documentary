#!/usr/bin/env python
"""Create EP40 Lech dry-run media and stub asset manifest."""
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
EP = "PD-2026-040-lech"
EPDIR = ROOT / "episodes" / EP
PUBLIC = ROOT / "remotion" / "public" / "lech_dryrun"
OUT = EPDIR / "05_visuals" / "asset_manifest.stub.v001.json"
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
    for x in range(0, size[0], 160):
        d.line((x, 0, x, size[1]), fill=tuple(max(0, c - 18) for c in color), width=2)
    for y in range(0, size[1], 160):
        d.line((0, y, size[0], y), fill=tuple(max(0, c - 18) for c in color), width=2)
    d.text((size[0] // 2 - 320, size[1] // 2 - 40), label, fill=(245, 247, 250))
    im.save(path)


def make_depth(path: Path, size=(3840, 2160)) -> None:
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    # Fast radial-ish grayscale depth placeholder. It only needs to satisfy
    # CaseFilm's depth-map presence contract during dryrun.
    small = Image.radial_gradient("L").resize(size, Image.Resampling.BILINEAR)
    im = Image.eval(small, lambda v: 255 - int(v * 0.7))
    im.save(path)


def ffmpeg_color(path: Path, color: str, dur: float, size: str, fps: int) -> None:
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        FFMPEG, "-y", "-hide_banner", "-loglevel", "error",
        "-f", "lavfi", "-i", f"color=c={color}:s={size}:r={fps}:d={dur}",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(path),
    ]
    subprocess.run(cmd, check=True)


def ffmpeg_color_frames(path: Path, color: str, frames: int, size: str, fps: int) -> None:
    if path.exists():
        probe = subprocess.run(
            [FFPROBE, "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries", "stream=nb_read_frames", "-of", "csv=p=0", str(path)],
            capture_output=True,
            text=True,
        )
        if probe.returncode == 0 and probe.stdout.strip() == str(frames):
            return
    path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        FFMPEG, "-y", "-hide_banner", "-loglevel", "error",
        "-f", "lavfi", "-i", f"color=c={color}:s={size}:r={fps}",
        "-frames:v", str(frames), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(path),
    ]
    subprocess.run(cmd, check=True)


def ffmpeg_silence(path: Path, dur: float) -> None:
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        FFMPEG, "-y", "-hide_banner", "-loglevel", "error",
        "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
        "-t", f"{dur:.3f}", "-c:a", "aac", "-b:a", "32k", str(path),
    ]
    subprocess.run(cmd, check=True)


def color_hex(seed: int, base: tuple[int, int, int]) -> str:
    r = max(0, min(255, base[0] + (seed * 17) % 80))
    g = max(0, min(255, base[1] + (seed * 29) % 70))
    b = max(0, min(255, base[2] + (seed * 37) % 60))
    return f"0x{r:02x}{g:02x}{b:02x}"


def still_item(asset_id: str, scene_id: str, role: str, idx: int, act: int, color: tuple[int, int, int]) -> dict:
    name = f"{scene_id}_{role}_{idx:03d}.png"
    rel = Path("img") / name
    path = PUBLIC / rel
    make_png(path, f"{scene_id} {role}", color)
    if role != "thumb":
        make_depth(path.with_name(path.stem + "_depth.png"))
    return {
        "asset_id": asset_id,
        "scene_id": scene_id,
        "variation": idx,
        "role": role,
        "act": act,
        "path": str(path).replace("\\", "/"),
        "depth_path": str(path.with_name(path.stem + "_depth.png")).replace("\\", "/") if role != "thumb" else None,
        "public_path": f"lech_dryrun/{rel.as_posix()}",
        "width": 3840,
        "height": 2160,
        "sha256": sha256(path),
        "mean_luma": 90.0 + idx % 80,
        "phash": f"stub-{asset_id}",
        "tags": ["stub", role],
        "caption_hint": f"stub {role} {scene_id}",
        "prompt_sha256": hashlib.sha256(asset_id.encode()).hexdigest(),
        "seed": 40000000 + idx,
        "model": "codex-stub",
        "source": "stub",
        "commercial_use": "allowed",
        "ai_disclosure_required": True,
        "qc": {"reviewed": True, "on_theme": True, "has_readable_text": False, "has_identifiable_face": False, "notes": "dryrun stub"},
    }


def main() -> int:
    for rel in ["img", "factory", "motion", "overlay", "audio"]:
        (PUBLIC / rel).mkdir(parents=True, exist_ok=True)
    (EPDIR / "05_visuals").mkdir(parents=True, exist_ok=True)

    stills = []
    for i in range(1, 71):
        act = 1 if i <= 21 else 2 if i <= 47 else 3 if i <= 63 else 4
        stills.append(still_item(f"LECH-S{i:02d}-01", f"S{i:02d}", "body", i, act, (46, 40 + i % 80, 60)))
    for i in range(1, 16):
        stills.append(still_item(f"LECH-AE-{i:02d}", f"AE{i:02d}", "ae", i, (i % 4) + 1, (64, 48, 28 + i * 6)))
    for i in range(1, 17):
        stills.append(still_item(f"LECH-I2V-{i:02d}", f"MV{i:02d}", "i2v_source", i, (i % 4) + 1, (38, 54, 72 + i * 3)))
    for i in range(1, 10):
        stills.append(still_item(f"LECH-TH-{i:02d}", f"TH{i:02d}", "thumb", i, 9, (96, 70, 34 + i * 4)))

    factory = []
    for i in range(1, 86):
        name = f"AF-STUB-{i:04d}__stub_clip.mp4"
        path = PUBLIC / "factory" / name
        ffmpeg_color(path, color_hex(i, (32, 26, 18)), 4.0, "1920x1080", 30)
        factory.append({
            "asset_id": f"AF-STUB-{i:04d}",
            "path": str(path).replace("\\", "/"),
            "public_path": f"lech_dryrun/factory/{name}",
            "type": "backgrounds",
            "subtype": "stub_clip",
            "kind": "video",
            "license": "Local dryrun stub",
            "sha256": sha256(path),
            "act": (i % 4) + 1,
            "covers_scene_id": None,
            "duration_sec": 4.0,
            "width": 1920,
            "height": 1080,
            "mean_luma": 52.0,
            "eyeballed_content": "dryrun stub clip, no people",
            "qc": {"reviewed": True, "on_theme": True, "no_watermark": True, "no_recognizable_person": True, "no_cartoon": True, "label_matches_content": True, "notes": "dryrun stub"},
        })
    motion = []
    for i in range(1, 17):
        name = f"M{i:02d}_rife.mp4"
        path = PUBLIC / "motion" / name
        ffmpeg_color_frames(path, color_hex(i, (24, 36, 52)), 164, "1280x720", 48)
        motion.append({
            "asset_id": f"LECH-M{i:02d}",
            "source_scene_id": f"S{30+i:02d}",
            "source_still": "",
            "path": str(path).replace("\\", "/"),
            "public_path": f"lech_dryrun/motion/{name}",
            "act": (i % 4) + 1,
            "width": 1280,
            "height": 720,
            "fps": 48,
            "frames": 164,
            "duration_sec": 3.417,
            "sha256": sha256(path),
            "tags": ["stub", "motion"],
            "qc": {"reviewed": True, "on_theme": True, "artifact_free": True, "notes": "dryrun stub"},
        })
    overlay = []
    for i in range(1, 13):
        name = f"AF-OVERLAY-STUB-{i:04d}__dust.mp4"
        path = PUBLIC / "overlay" / name
        ffmpeg_color(path, color_hex(i, (12, 12, 12)), 2.0, "1920x1080", 30)
        overlay.append({
            "asset_id": f"AF-OVERLAY-STUB-{i:04d}",
            "path": str(path).replace("\\", "/"),
            "public_path": f"lech_dryrun/overlay/{name}",
            "type": "particle_assets",
            "subtype": "dust_particles",
            "license": "Local dryrun stub",
            "sha256": sha256(path),
            "blend_hint": "screen",
            "eyeballed_content": "dryrun dust overlay",
            "qc": {"reviewed": True, "on_theme": True, "no_watermark": True, "notes": "dryrun stub"},
        })
    ffmpeg_silence(PUBLIC / "audio" / "silence.m4a", 720.8)
    manifest = {
        "schema_version": "lech_assets.v1",
        "episode_id": EP,
        "slug": "lech",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "producer": "scripts/make_lech_stub_assets.py",
        "is_stub": True,
        "counts": {
            "still_body": 70,
            "still_ae": 15,
            "still_i2v_source": 16,
            "still_thumb": 9,
            "motion": 16,
            "factory": 85,
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
