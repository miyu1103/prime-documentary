#!/usr/bin/env python
"""Assemble finished Wan i2v frame-dirs into 1920x1080 mp4 motion clips (generic per episode).

Reads ae-demo/wan_frames_<slug>_<stem>/ and writes
  H:/pd-media/assets/ai_video/<slug>/motion/<stem>.mp4     (media master)
  remotion/public/<slug>/motion/<stem>.mp4                 (render-visible copy)

Idempotent: an existing, healthy output is skipped, so this is safe to run repeatedly while
i2v is still in flight. Generalised from assemble_centralpark_i2v.py.

Usage: py -3.11 scripts/assemble_episode_i2v.py --slug willingham [--fps-in 24] [--dry-run]
"""
from __future__ import annotations

import argparse
import glob
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

FF = shutil.which("ffmpeg") or r"C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe"
ROOT = Path(__file__).resolve().parents[1]
AE_DEMO = Path(r"C:/Users/aab15/ae-demo")
MIN_FRAMES = 40
MIN_OK_BYTES = 50_000


def assemble_one(frames: list[str], out: Path, fps_in: int) -> tuple[bool, str]:
    lst = tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, dir=str(out.parent))
    try:
        for f in frames:
            lst.write(f"file '{f}'\n")
        lst.close()
        cmd = [FF, "-y", "-hide_banner", "-loglevel", "error", "-r", str(fps_in),
               "-f", "concat", "-safe", "0", "-i", lst.name,
               "-vf", "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,fps=30",
               "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", str(out)]
        r = subprocess.run(cmd, capture_output=True, text=True)
        return (out.exists() and out.stat().st_size > MIN_OK_BYTES), r.stderr[-200:]
    finally:
        try:
            os.unlink(lst.name)
        except OSError:
            pass


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--fps-in", type=int, default=24, help="playback rate of the 81 Wan frames")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    out_dir = Path(f"H:/pd-media/assets/ai_video/{a.slug}/motion")
    pub_dir = ROOT / "remotion" / "public" / a.slug / "motion"
    src_dirs = sorted(glob.glob(str(AE_DEMO / f"wan_frames_{a.slug}_*")))
    if not a.dry_run:
        out_dir.mkdir(parents=True, exist_ok=True)
        pub_dir.mkdir(parents=True, exist_ok=True)

    made = skipped = partial = failed = 0
    for d in src_dirs:
        stem = os.path.basename(d).replace(f"wan_frames_{a.slug}_", "")
        frames = sorted(glob.glob(os.path.join(d, "*.png")))
        if len(frames) < MIN_FRAMES:
            partial += 1
            continue
        outp = out_dir / f"{stem}.mp4"
        if outp.exists() and outp.stat().st_size > MIN_OK_BYTES:
            skipped += 1
            if not a.dry_run and not (pub_dir / outp.name).exists():
                shutil.copy(outp, pub_dir / outp.name)
            continue
        if a.dry_run:
            print(f"  would assemble {stem} ({len(frames)} frames)")
            made += 1
            continue
        ok, err = assemble_one(frames, outp, a.fps_in)
        if ok:
            shutil.copy(outp, pub_dir / outp.name)
            made += 1
        else:
            failed += 1
            print(f"FAIL {stem}: {err}", flush=True)

    print(f"[{a.slug}] assembled={made} skipped={skipped} partial(in-flight)={partial} "
          f"failed={failed} (of {len(src_dirs)} frame-dirs)", flush=True)
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    raise SystemExit(main())
