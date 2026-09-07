from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
IMG_ROOT = Path(r"E:/pd-media/assets/ai/tekoh")
MOTION_ROOT = Path(r"E:/pd-media/assets/ai_video/tekoh")
PUBLIC = ROOT / "remotion" / "public" / "tekoh"


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def ffmpeg_base(overwrite: bool) -> list[str]:
    return ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y" if overwrite else "-n"]


def make_from_still(src: Path, out: Path, duration: float, variant: int, overwrite: bool) -> bool:
    if out.exists() and not overwrite:
        return False
    out.parent.mkdir(parents=True, exist_ok=True)
    zoom = 0.00025 + (variant % 7) * 0.00007
    sat = 0.82 + (variant % 5) * 0.035
    contrast = 1.00 + (variant % 4) * 0.025
    # Deterministic local motion: subtle zoom + slight grade variation.
    vf = (
        "scale=1920:1080,"
        f"zoompan=z='min(zoom+{zoom:.5f},1.045)':"
        "x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
        f"d={int(duration * 30)}:s=1920x1080:fps=30,"
        f"eq=saturation={sat:.3f}:contrast={contrast:.3f},"
        "format=yuv420p"
    )
    cmd = ffmpeg_base(overwrite) + [
        "-loop", "1",
        "-i", str(src),
        "-vf", vf,
        "-t", f"{duration:.3f}",
        "-r", "30",
        "-an",
        "-c:v", "libx264",
        "-preset", "ultrafast",
        "-crf", "20",
        "-movflags", "+faststart",
        str(out),
    ]
    run(cmd)
    return True


def copy_to_public(src: Path, dest: Path, overwrite: bool) -> bool:
    if dest.exists() and not overwrite:
        return False
    dest.parent.mkdir(parents=True, exist_ok=True)
    data = src.read_bytes()
    dest.write_bytes(data)
    return True


def make_overlay(out: Path, idx: int, overwrite: bool) -> bool:
    if out.exists() and not overwrite:
        return False
    out.parent.mkdir(parents=True, exist_ok=True)
    duration = 4.0
    hue = 0.48 + (idx % 4) * 0.025
    # Text-free animated wash used as an editorial overlay/scrim asset.
    vf = (
        "nullsrc=s=1920x1080:r=30,"
        "format=rgba,"
        f"geq=r='18+35*sin((X+T*90+{idx}*23)/210)':"
        f"g='90+45*sin((Y+T*65+{idx}*17)/240)':"
        f"b='100+40*sin((X+Y+T*50+{idx}*31)/280)':a='255',"
        f"hue=h={hue:.3f}:s=0.55,"
        "boxblur=18:2,format=yuv420p"
    )
    cmd = ffmpeg_base(overwrite) + [
        "-f", "lavfi",
        "-i", vf,
        "-t", f"{duration:.3f}",
        "-an",
        "-c:v", "libx264",
        "-preset", "ultrafast",
        "-crf", "24",
        "-movflags", "+faststart",
        str(out),
    ]
    run(cmd)
    return True


def generate_factory(overwrite: bool) -> int:
    made = 0
    sources = [IMG_ROOT / f"S{i:02d}.png" for i in range(1, 86)]
    for i in range(1, 94):
        src = sources[(i - 1) % len(sources)]
        if make_from_still(src, PUBLIC / "factory" / f"F{i:03d}.mp4", 3.343, i, overwrite):
            made += 1
            print(f"factory F{i:03d}")
    return made


def generate_motion(overwrite: bool) -> int:
    made = 0
    for i in range(1, 17):
        src = IMG_ROOT / f"M{i:02d}_src.png"
        h_out = MOTION_ROOT / f"M{i:02d}.mp4"
        p_out = PUBLIC / "motion" / f"M{i:02d}.mp4"
        if make_from_still(src, h_out, 5.0, i + 100, overwrite):
            made += 1
            print(f"motion M{i:02d}")
        copy_to_public(h_out, p_out, overwrite)
    return made


def generate_overlay(overwrite: bool) -> int:
    made = 0
    for i in range(1, 13):
        if make_overlay(PUBLIC / "overlay" / f"O{i:02d}.mp4", i, overwrite):
            made += 1
            print(f"overlay O{i:02d}")
    return made


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--overwrite", action="store_true")
    args = ap.parse_args()
    print(f"made_factory={generate_factory(args.overwrite)}")
    print(f"made_motion={generate_motion(args.overwrite)}")
    print(f"made_overlay={generate_overlay(args.overwrite)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
