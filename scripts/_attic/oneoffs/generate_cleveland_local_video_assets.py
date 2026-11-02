#!/usr/bin/env python
"""Generate local EP45 Cleveland video assets from Codex stills.

This avoids external video providers: factory clips and motion seeds are
deterministic Ken Burns-style MP4s from the approved Codex images, and overlays
are procedural light/grain plates.
"""
from __future__ import annotations

import math
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
AI = Path("E:/pd-media/assets/ai/cleveland")
MOTION_SRC = Path("E:/pd-media/assets/ai_video/cleveland")
PUBLIC = ROOT / "remotion" / "public" / "cleveland"
FACTORY = PUBLIC / "factory"
MOTION = PUBLIC / "motion"
OVERLAY = PUBLIC / "overlay"


def run_ffmpeg(args: list[str]) -> None:
    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *args]
    subprocess.run(cmd, check=True)


def ken_burns(src: Path, dst: Path, *, dur: float, phase: float, strength: float) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        return
    x_amp = int(95 * strength)
    y_amp = int(54 * strength)
    vf = (
        "scale=2304:1296:force_original_aspect_ratio=increase,"
        "crop=1920:1080:"
        f"x='192+{x_amp}*sin(2*PI*t/{dur:.3f}+{phase:.3f})':"
        f"y='108+{y_amp}*cos(2*PI*t/{dur:.3f}+{phase:.3f})',"
        "eq=contrast=1.035:saturation=0.92:brightness=-0.015,"
        "format=yuv420p"
    )
    run_ffmpeg([
        "-loop", "1",
        "-t", f"{dur:.3f}",
        "-i", str(src),
        "-vf", vf,
        "-r", "24",
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "22",
        "-movflags", "+faststart",
        str(dst),
    ])


def make_overlay(dst: Path, *, kind: int, dur: float = 4.0, fps: int = 24) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        return
    frames = int(dur * fps)
    w, h = 1920, 1080
    rng = np.random.default_rng(45000 + kind)
    proc = subprocess.Popen(
        [
            "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
            "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{w}x{h}", "-r", str(fps),
            "-i", "-", "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "24",
            "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(dst),
        ],
        stdin=subprocess.PIPE,
    )
    assert proc.stdin is not None
    yy, xx = np.mgrid[0:h, 0:w]
    for f in range(frames):
        t = f / max(frames - 1, 1)
        base = np.zeros((h, w, 3), dtype=np.float32)
        noise = rng.normal(0, 5.5, (h, w, 1)).astype(np.float32)
        if kind % 3 == 0:
            cx = int((0.15 + 0.7 * t) * w)
            band = np.exp(-((xx - cx) ** 2) / (2 * (80 + kind * 6) ** 2))
            color = np.array([190, 174, 145], dtype=np.float32)
            base += band[..., None] * color * 0.34
        elif kind % 3 == 1:
            cy = int((0.2 + 0.55 * (1 - t)) * h)
            band = np.exp(-((yy - cy) ** 2) / (2 * (55 + kind * 4) ** 2))
            color = np.array([145, 158, 170], dtype=np.float32)
            base += band[..., None] * color * 0.30
        else:
            r = np.sqrt(((xx - w / 2) / w) ** 2 + ((yy - h / 2) / h) ** 2)
            vignette = np.clip((r - 0.18) * 1.9, 0, 1)
            color = np.array([110, 118, 126], dtype=np.float32)
            base += vignette[..., None] * color * 0.23
        arr = np.clip(base + noise + 6, 0, 255).astype(np.uint8)
        im = Image.fromarray(arr, "RGB").filter(ImageFilter.GaussianBlur(0.35))
        proc.stdin.write(im.tobytes())
    proc.stdin.close()
    if proc.wait() != 0:
        raise RuntimeError(f"ffmpeg failed for {dst}")


def main() -> int:
    FACTORY.mkdir(parents=True, exist_ok=True)
    MOTION.mkdir(parents=True, exist_ok=True)
    OVERLAY.mkdir(parents=True, exist_ok=True)
    MOTION_SRC.mkdir(parents=True, exist_ok=True)

    factory_sources = [AI / f"S{i:02d}.png" for i in range(1, 85)] + [AI / f"M{i:02d}_src.png" for i in range(1, 9)]
    for idx, src in enumerate(factory_sources, 1):
        ken_burns(src, FACTORY / f"F{idx:03d}_codex_kb.mp4", dur=3.25, phase=idx * 0.37, strength=0.65 + (idx % 5) * 0.06)
        if idx % 20 == 0:
            print(f"factory {idx}/92", flush=True)

    for idx in range(1, 17):
        src = AI / f"M{idx:02d}_src.png"
        name = f"M{idx:02d}_rife.mp4"
        dst = MOTION_SRC / name
        ken_burns(src, dst, dur=4.25, phase=idx * 0.61, strength=1.05)
        pub = MOTION / name
        if not pub.exists():
            pub.write_bytes(dst.read_bytes())
        print(f"motion {idx}/16", flush=True)

    for idx in range(1, 13):
        make_overlay(OVERLAY / f"O{idx:02d}_codex_overlay.mp4", kind=idx)
    print("done factory=92 motion=16 overlay=12")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
