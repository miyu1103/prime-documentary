#!/usr/bin/env python
"""Build EP49 Strieff local motion clips from Codex-generated i2v source stills.

This is a zero-SDXL, zero-provider-cost fallback that turns M##_src.png plates
into contract-compatible M##_rife.mp4 clips. It is intentionally deterministic
and non-destructive: existing different outputs are left untouched unless
--force is provided.
"""
from __future__ import annotations

import argparse
import hashlib
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "strieff"
SRC_DIR = Path("H:/pd-media/assets/ai/strieff")
OUT_DIR = Path("H:/pd-media/assets/ai_video/strieff")
PUBLIC_DIR = ROOT / "remotion" / "public" / SLUG / "motion"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def copy_public(src: Path, dst: Path) -> bool:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        if sha256(src) != sha256(dst):
            dst.write_bytes(src.read_bytes())
            return True
        return False
    shutil.copy2(src, dst)
    return True


def build_one(index: int, force: bool) -> tuple[Path, bool]:
    src = SRC_DIR / f"M{index:02d}_src.png"
    out = OUT_DIR / f"M{index:02d}_rife.mp4"
    if not src.is_file():
        raise FileNotFoundError(src)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    if out.exists() and not force and out.stat().st_size > 1024:
        copy_public(out, PUBLIC_DIR / out.name)
        return out, False

    frames = 264  # 5.5 seconds at 48fps.
    direction = index % 4
    if direction == 0:
        x_expr = "iw/2-(iw/zoom/2)+18*sin(on/38)"
        y_expr = "ih/2-(ih/zoom/2)-18*cos(on/44)"
    elif direction == 1:
        x_expr = "iw/2-(iw/zoom/2)+on*0.28"
        y_expr = "ih/2-(ih/zoom/2)+10*sin(on/36)"
    elif direction == 2:
        x_expr = "iw/2-(iw/zoom/2)-on*0.24"
        y_expr = "ih/2-(ih/zoom/2)+on*0.10"
    else:
        x_expr = "iw/2-(iw/zoom/2)+12*cos(on/31)"
        y_expr = "ih/2-(ih/zoom/2)-on*0.16"
    vf = (
        "scale=4200:2363:force_original_aspect_ratio=increase,"
        "crop=4200:2363,"
        f"zoompan=z='1.018+0.055*on/{frames}':x='{x_expr}':y='{y_expr}':d={frames}:s=3840x2160:fps=48,"
        "unsharp=5:5:0.35:3:3:0.15,format=yuv420p"
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
        "22",
        "-movflags",
        "+faststart",
        str(out),
    ]
    subprocess.run(cmd, check=True)
    copy_public(out, PUBLIC_DIR / out.name)
    return out, True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    built = 0
    for i in range(1, 17):
        path, did_build = build_one(i, args.force)
        built += int(did_build)
        print(f"{'built' if did_build else 'kept '} {path}")
    print(f"motion_ready=16 newly_built={built} public={PUBLIC_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
