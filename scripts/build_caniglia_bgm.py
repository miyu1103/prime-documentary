#!/usr/bin/env python
"""Create the EP43 BGM base placeholder for dry-run or validate an existing render."""
from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-043-caniglia"
EDIT = ROOT / "episodes" / EP / "08_edit"
FFMPEG = shutil.which("ffmpeg") or r"C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe"


def make_base(path: Path, dur: float = 733.8) -> None:
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
            f"color=c=0x0a0a0c:s=1920x1080:r=30:d={dur:.3f}",
            "-f",
            "lavfi",
            "-i",
            f"anullsrc=r=48000:cl=stereo:d={dur:.3f}",
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "aac",
            "-b:a",
            "128k",
            "-shortest",
            str(path),
        ],
        check=True,
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dryrun", action="store_true")
    ap.add_argument("render", nargs="?", type=Path)
    ap.add_argument("out", nargs="?", type=Path)
    args = ap.parse_args()
    if args.dryrun:
        out = args.out or EDIT / "_dryrun" / "caniglia_final_bgm.v002.mp4"
        make_base(out)
        print(f"wrote {out}")
        return 0
    render = args.render or EDIT / "caniglia_casefilm.v001.mp4"
    out = args.out or EDIT / "caniglia_final_bgm.v002.mp4"
    if not render.exists():
        print(f"MISSING render {render}")
        return 2
    if out.exists():
        print(f"REFUSE overwrite {out}")
        return 2
    shutil.copy2(render, out)
    print(f"wrote {out} (audio mix placeholder; replace after master narration)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

