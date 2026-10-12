#!/usr/bin/env python3
"""Create EP39 Frazier stub media and a manifest for the implementation lane.

This is intentionally local-only and idempotent. It creates placeholder media
under remotion/public/frazier so the build lane can validate layout, reuse, and
timing gates before the real asset lane finishes.
"""
from __future__ import annotations

import argparse
import colorsys
import hashlib
import json
import math
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageStat

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-039-frazier"
SLUG = "frazier"
FPS = 30
BODY_SECONDS = 705.0

PUB = ROOT / "remotion" / "public" / SLUG
EPDIR = ROOT / "episodes" / EP
MANIFEST = EPDIR / "05_visuals" / "asset_manifest.stub.v001.json"
ANNOTATED = EPDIR / "03_script" / "script.annotated.stub.json"
CAPTIONS_JSON = EPDIR / "08_edit" / "captions.final.stub.json"
CAPTIONS_SRT = EPDIR / "08_edit" / "captions.final.stub.srt"
BEATSHEET = EPDIR / "04_scenes" / "premium_beatsheet.v001.stub.json"

ACT_RANGES = [
    (1, 10, 0),
    (11, 20, 1),
    (21, 30, 2),
    (31, 40, 3),
    (41, 50, 4),
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def scene_act(scene_code: str) -> int:
    n = int(scene_code[1:])
    for lo, hi, act in ACT_RANGES:
        if lo <= n <= hi:
            return act
    return 4


def ensure_dirs() -> None:
    for d in [
        PUB / "img",
        PUB / "factory",
        PUB / "motion",
        PUB / "overlay",
        EPDIR / "03_script",
        EPDIR / "04_scenes",
        EPDIR / "05_visuals",
        EPDIR / "08_edit",
        EPDIR / "09_package",
    ]:
        d.mkdir(parents=True, exist_ok=True)


def font(size: int) -> ImageFont.ImageFont:
    for name in ("C:/Windows/Fonts/arialbd.ttf", "C:/Windows/Fonts/arial.ttf"):
        p = Path(name)
        if p.exists():
            return ImageFont.truetype(str(p), size)
    return ImageFont.load_default()


def still_name(scene: int, variant: int) -> str:
    stem = f"S{scene:02d}"
    return f"{stem}.png" if variant == 1 else f"{stem}_{variant:02d}.png"


def make_still(path: Path, depth_path: Path, scene: int, variant: int) -> None:
    if path.exists() and depth_path.exists():
        return
    hue = ((scene - 1) * 0.041 + (variant - 1) * 0.11) % 1.0
    r, g, b = [int(x * 255) for x in colorsys.hsv_to_rgb(hue, 0.74, 0.36)]
    img = Image.new("RGB", (3840, 2160), (5, 9, 16))
    px = img.load()
    for y in range(2160):
        fy = y / 2159
        for x in range(3840):
            fx = x / 3839
            vignette = max(0.0, 1.0 - 1.15 * math.hypot(fx - 0.5, fy - 0.5))
            stripe = 0.08 * math.sin((fx * 7.0 + fy * 4.0 + hue) * math.tau)
            m = 0.18 + 0.72 * vignette + stripe
            px[x, y] = (int(r * m), int(g * m), int(b * m))
    d = ImageDraw.Draw(img)
    label = f"S{scene:02d} v{variant}"
    fnt = font(260)
    bbox = d.textbbox((0, 0), label, font=fnt)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    d.text(((3840 - tw) / 2, (2160 - th) / 2), label, font=fnt, fill=(245, 247, 250))
    d.rectangle((120, 120, 3720, 2040), outline=(200, 205, 214), width=8)
    img.save(path, "PNG")

    depth = Image.new("L", (3840, 2160), 0)
    dp = depth.load()
    for y in range(2160):
        fy = y / 2159
        for x in range(3840):
            fx = x / 3839
            v = max(0.0, 1.0 - math.hypot(fx - 0.5, fy - 0.48) * 1.45)
            dp[x, y] = int(40 + 205 * v)
    depth.save(depth_path, "PNG")


def ffmpeg() -> str:
    exe = shutil.which("ffmpeg")
    if not exe:
        raise SystemExit("ffmpeg not found on PATH")
    return exe


def run_ffmpeg(out: Path, args: list[str]) -> None:
    if out.exists() and out.stat().st_size > 1024:
        return
    out.parent.mkdir(parents=True, exist_ok=True)
    cmd = [ffmpeg(), "-hide_banner", "-loglevel", "error", "-y", *args, str(out)]
    subprocess.run(cmd, check=True)


def make_video_stub(path: Path, label: str, size: str, rate: int, duration: float, hue: int) -> None:
    fontfile = "C\\:/Windows/Fonts/arial.ttf"
    filt = (
        f"testsrc2=size={size}:rate={rate}:duration={duration},"
        f"hue=h={hue}*PI/180:s=0.85,"
        "format=yuv420p,"
        f"drawtext=fontfile='{fontfile}':text='{label} %{{n}}':"
        "fontcolor=white:fontsize=82:x=(w-text_w)/2:y=(h-text_h)/2"
    )
    run_ffmpeg(
        path,
        [
            "-f",
            "lavfi",
            "-i",
            filt,
            "-an",
            "-c:v",
            "libx264",
            "-preset",
            "ultrafast",
            "-crf",
            "34",
            "-pix_fmt",
            "yuv420p",
            "-movflags",
            "+faststart",
        ],
    )


def make_overlay_stub(path: Path, label: str, hue: int) -> None:
    fontfile = "C\\:/Windows/Fonts/arial.ttf"
    filt = (
        "nullsrc=size=1920x1080:rate=30:duration=8,"
        f"geq=r='32+32*random(1)':g='32+32*random(2)':b='80+80*random(3)',"
        f"hue=h={hue}*PI/180:s=0.9,"
        f"drawtext=fontfile='{fontfile}':text='{label} %{{n}}':"
        "fontcolor=white@0.55:fontsize=54:x=(w-text_w)/2:y=(h-text_h)/2,"
        "format=yuv420p"
    )
    run_ffmpeg(
        path,
        [
            "-f",
            "lavfi",
            "-i",
            filt,
            "-an",
            "-c:v",
            "libx264",
            "-preset",
            "ultrafast",
            "-crf",
            "36",
            "-pix_fmt",
            "yuv420p",
            "-movflags",
            "+faststart",
        ],
    )


def repair_overlay_stubs() -> int:
    repaired = 0
    for i in range(1, 35):
        path = PUB / "overlay" / f"AF-LT-039{i:03d}__stub_overlay_{i:03d}.mp4"
        temp = path.with_name(path.stem + ".repair.mp4")
        if temp.exists():
            temp.unlink()
        make_overlay_stub(temp, f"OV{i:03d}", (i * 23) % 360)
        check = subprocess.run(
            [ffmpeg(), "-hide_banner", "-loglevel", "error", "-i", str(temp), "-f", "null", "-"],
            capture_output=True,
            text=True,
        )
        if check.returncode != 0:
            temp.unlink(missing_ok=True)
            raise SystemExit(f"overlay repair decode failed for {path.name}: {check.stderr[-500:]}")
        temp.replace(path)
        repaired += 1
        print(f"repaired overlay {path.relative_to(ROOT)}")
    return repaired


def make_silence(path: Path) -> None:
    if path.exists() and path.stat().st_size > 1024:
        return
    run_ffmpeg(
        path,
        [
            "-f",
            "lavfi",
            "-i",
            f"anullsrc=r=48000:cl=stereo:d={BODY_SECONDS}",
            "-c:a",
            "libmp3lame",
            "-b:a",
            "64k",
        ],
    )


def media_record(asset_id: str, kind: str, path: Path, public_path: str, scene_code: str, **extra) -> dict:
    width = extra.pop("width", None)
    height = extra.pop("height", None)
    duration = extra.pop("duration_sec", None)
    fps = extra.pop("fps", None)
    frames = extra.pop("frames", None)
    median_luma = extra.pop("median_luma", None)
    if median_luma is None and path.suffix.lower() == ".png":
        median_luma = round(ImageStat.Stat(Image.open(path).convert("L")).median[0], 2)
    return {
        "asset_id": asset_id,
        "kind": kind,
        "max_uses": {"still": 2, "factory": 1, "motion": 2}[kind],
        "public_path": public_path,
        "abs_path": str(path.resolve()),
        "source_path": str(path.resolve()),
        "scene_code": scene_code,
        "act": scene_act(scene_code),
        "variant": extra.pop("variant", None),
        "depth_map": extra.pop("depth_map", None),
        "width": width,
        "height": height,
        "long_edge_px": max([v for v in (width, height) if v] or [0]),
        "duration_sec": duration,
        "fps": fps,
        "frames": frames,
        "sha256": sha256(path),
        "bytes": path.stat().st_size,
        "median_luma": median_luma,
        "af_id": None,
        "theme": "frazier_stub",
        "subtype": kind,
        "saw": None,
        "tags": ["frazier", "stub", f"scene-{scene_code.lower()}"],
        "source": "local_stub",
        "license": "internal_generated",
        "commercial_use": "allowed",
        "reviewed": True,
        "on_theme": True,
        "qc": {"pass": True, "notes": "implementation stub"},
        "stub": True,
        "status": "stub",
        **extra,
    }


def build_manifest() -> dict:
    assets: list[dict] = []
    overlays: list[dict] = []

    idx = 1
    for scene in range(1, 27):
        for variant in range(1, 4):
            name = still_name(scene, variant)
            path = PUB / "img" / name
            depth_name = path.with_name(path.stem + "_depth.png").name
            scene_code = f"S{scene:02d}"
            assets.append(
                media_record(
                    f"ST-039-{idx:03d}",
                    "still",
                    path,
                    f"{SLUG}/img/{name}",
                    scene_code,
                    variant=variant,
                    depth_map=f"{SLUG}/img/{depth_name}",
                    width=3840,
                    height=2160,
                )
            )
            idx += 1

    for i in range(1, 94):
        name = f"AF-BG-039{i:03d}__stub_factory_{i:03d}.mp4"
        scene_code = f"S{((i - 1) % 50) + 1:02d}"
        assets.append(
            media_record(
                f"FC-039-{i:03d}",
                "factory",
                PUB / "factory" / name,
                f"{SLUG}/factory/{name}",
                scene_code,
                duration_sec=6.0,
                fps=30,
                frames=180,
            )
        )

    for i in range(1, 20):
        name = f"MO-039-{i:03d}__stub_motion_{i:03d}.mp4"
        scene_code = f"S{((i + 30 - 1) % 50) + 1:02d}"
        assets.append(
            media_record(
                f"MO-039-{i:03d}",
                "motion",
                PUB / "motion" / name,
                f"{SLUG}/motion/{name}",
                scene_code,
                duration_sec=41 / 16,
                fps=16,
                frames=41,
            )
        )

    for i in range(1, 35):
        name = f"AF-LT-039{i:03d}__stub_overlay_{i:03d}.mp4"
        path = PUB / "overlay" / name
        overlays.append(
            {
                "overlay_id": f"OV-039-{i:03d}",
                "category": ["light_assets", "particle_assets", "vfx_overlays", "loops"][(i - 1) % 4],
                "public_path": f"{SLUG}/overlay/{name}",
                "duration_sec": 8.0,
                "fps": 30,
                "blend_hint": ["add", "screen", "overlay"][(i - 1) % 3],
                "sha256": sha256(path),
                "af_id": f"AF-LT-039{i:03d}",
                "bytes": path.stat().st_size,
                "stub": True,
                "status": "stub",
            }
        )

    return {
        "episode_id": EP,
        "manifest_version": "v001",
        "status": "stub",
        "generated_at": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
        "counts": {
            "still": 78,
            "factory": 93,
            "motion": 19,
            "total": 190,
            "overlays": 34,
            "distinct_scene_codes": 50,
        },
        "caps": {"still": 2, "factory": 1, "motion": 2},
        "assets": assets,
        "overlays": overlays,
    }


def make_stub_script_files() -> None:
    if not ANNOTATED.exists():
        chapters = [
            {"id": "hook", "title": "HOOK", "start": 0, "end": 8},
            {"id": "opening", "title": "OPENING", "start": 8, "end": 70},
            {"id": "act1", "title": "ACT I", "start": 70, "end": 220},
            {"id": "act2", "title": "ACT II", "start": 220, "end": 390},
            {"id": "act3", "title": "ACT III", "start": 390, "end": 540},
            {"id": "act4", "title": "ACT IV", "start": 540, "end": 670},
            {"id": "ending", "title": "ENDING", "start": 670, "end": BODY_SECONDS},
        ]
        spans = []
        for i in range(1, 51):
            start = round(8 + (i - 1) * ((BODY_SECONDS - 18) / 50), 3)
            end = round(min(BODY_SECONDS - 9, start + 10.5), 3)
            spans.append(
                {
                    "span_id": f"SPN-{i:04d}",
                    "scene_code": f"S{i:02d}",
                    "chapter_id": "act" + str(min(4, max(1, (i - 1) // 10 + 1))),
                    "start": start,
                    "end": end,
                    "text": f"Stub narration span {i}.",
                    "on_screen_text": [f"FRAZIER STUB {i:02d}"],
                    "claim_ids": [f"C-039-{i:03d}"],
                }
            )
        ANNOTATED.write_text(
            json.dumps({"episode_id": EP, "status": "stub", "chapters": chapters, "spans": spans}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
    if not CAPTIONS_JSON.exists():
        cues = []
        t = 0.0
        idx = 1
        while t < BODY_SECONDS - 2:
            cues.append({"start": round(t, 3), "end": round(t + 3.2, 3), "text": f"Stub caption {idx}."})
            t += 4.4
            idx += 1
        CAPTIONS_JSON.write_text(json.dumps({"episode_id": EP, "status": "stub", "cues": cues}, ensure_ascii=False, indent=2), encoding="utf-8")
    if not CAPTIONS_SRT.exists():
        cues = json.loads(CAPTIONS_JSON.read_text(encoding="utf-8"))["cues"]
        CAPTIONS_SRT.write_text("\n\n".join(srt_block(i + 1, c) for i, c in enumerate(cues)) + "\n", encoding="utf-8")


def srt_time(sec: float) -> str:
    ms = int(round(sec * 1000))
    h, rem = divmod(ms, 3600_000)
    m, rem = divmod(rem, 60_000)
    s, ms = divmod(rem, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def srt_block(i: int, cue: dict) -> str:
    return f"{i}\n{srt_time(cue['start'])} --> {srt_time(cue['end'])}\n{cue['text']}"


def make_stub_beatsheet() -> None:
    if BEATSHEET.exists():
        return
    fps = 30
    beats = []
    t = 0.0
    for i in range(1, 111):
        dur = 2.2 if i % 5 else 6.0
        kind = "factory" if i % 3 else "hero"
        component = "FactoryClip" if kind == "factory" else "WilliamsScene"
        beats.append(
            {
                "id": f"stub-{i:03d}",
                "kind": kind,
                "component": component,
                "start_frame": int(round(t * fps)),
                "dur_frames": int(round(dur * fps)),
            }
        )
        t += dur
    for j in range(1, 43):
        start = 9.0 + (j - 1) * 16.0
        beats.append(
            {
                "id": f"mg-{j:03d}",
                "kind": "mg_hero" if j % 2 else "act_title",
                "component": "FigureBeats",
                "start_frame": int(round(start * fps)),
                "dur_frames": int(round(5.4 * fps)),
            }
        )
    BEATSHEET.write_text(
        json.dumps({"episode_id": EP, "meta": {"fps": fps, "status": "stub"}, "beats": beats}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--skip-video", action="store_true", help="only write stills/json; useful for quick schema checks")
    ap.add_argument("--repair-overlays", action="store_true", help="atomically rebuild and decode-check all overlay stubs")
    args = ap.parse_args()
    ensure_dirs()
    if args.repair_overlays:
        repaired = repair_overlay_stubs()
        manifest = build_manifest()
        MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
        print(json.dumps({"ok": True, "repaired_overlays": repaired, "manifest": str(MANIFEST)}, ensure_ascii=False))
        return 0
    created = {"stills": 0, "depth": 0, "factory": 0, "motion": 0, "overlay": 0}

    for scene in range(1, 27):
        for variant in range(1, 4):
            path = PUB / "img" / still_name(scene, variant)
            depth = path.with_name(path.stem + "_depth.png")
            before = path.exists() and depth.exists()
            make_still(path, depth, scene, variant)
            if not before:
                created["stills"] += 1
                created["depth"] += 1
                print(f"saved still {path.relative_to(ROOT)}")

    if not args.skip_video:
        make_silence(PUB / "narration.mp3")
        for i in range(1, 94):
            path = PUB / "factory" / f"AF-BG-039{i:03d}__stub_factory_{i:03d}.mp4"
            before = path.exists()
            make_video_stub(path, f"FC{i:03d}", "1920x1080", 30, 6.0, (i * 11) % 360)
            if not before:
                created["factory"] += 1
                print(f"saved factory {path.relative_to(ROOT)}")
        for i in range(1, 20):
            path = PUB / "motion" / f"MO-039-{i:03d}__stub_motion_{i:03d}.mp4"
            before = path.exists()
            make_video_stub(path, f"MO{i:03d}", "1280x720", 16, 41 / 16, (i * 19) % 360)
            if not before:
                created["motion"] += 1
                print(f"saved motion {path.relative_to(ROOT)}")
        for i in range(1, 35):
            path = PUB / "overlay" / f"AF-LT-039{i:03d}__stub_overlay_{i:03d}.mp4"
            before = path.exists()
            make_overlay_stub(path, f"OV{i:03d}", (i * 23) % 360)
            if not before:
                created["overlay"] += 1
                print(f"saved overlay {path.relative_to(ROOT)}")

    make_stub_script_files()
    make_stub_beatsheet()
    manifest = build_manifest()
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    total_bytes = sum(p.stat().st_size for p in (PUB).rglob("*") if p.is_file())
    print(json.dumps({"ok": True, "created": created, "manifest": str(MANIFEST), "public_bytes": total_bytes}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
