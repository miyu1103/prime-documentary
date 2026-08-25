#!/usr/bin/env python3
"""Full-frame review strips: one image per clip, frames large enough to read a country.

Contact sheets are 260 px tiles and the build thread measured what that costs: 17 clips of
foreign footage -- a New York subway sign, a Taipei bridge, Moscow, Venice, an Icelandic
moorland, an Andean altiplano -- were KEPT during pool selection with the note "anonymous, no
place tell", because at tile size the tells are not legible. At full frame they are unmistakable
(docs/PD_HANDOFF_FROM_DESIGN_THREAD.v001.md).

This writes <out>/<NN>_<clip>.png, each a horizontal strip of N frames at --width each, so a
reviewer reads ONE clip at a time at a size where signage, number plates, road markings,
architecture and vegetation resolve.

    py -3.11 scripts/build_fullframe_strips.py --slug keybridge --frames 2 --width 900
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
FFMPEG = shutil.which("ffmpeg") or r"C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe"
FFPROBE = shutil.which("ffprobe") or r"C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffprobe.exe"


def duration(p: Path) -> float:
    r = subprocess.run([FFPROBE, "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", str(p)], capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return 0.0


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--pool", help="default remotion/public/<slug>/factory")
    ap.add_argument("--out", help="default runs/qc/fullframe/<slug>")
    ap.add_argument("--frames", type=int, default=2)
    ap.add_argument("--width", type=int, default=900)
    a = ap.parse_args()

    pool = Path(a.pool) if a.pool else ROOT / "remotion" / "public" / a.slug / "factory"
    out = Path(a.out) if a.out else ROOT / "runs" / "qc" / "fullframe" / a.slug
    out.mkdir(parents=True, exist_ok=True)
    clips = sorted(pool.glob("*.mp4"))
    if not clips:
        print(f"no clips in {pool}")
        return 1

    tmp = out / "_f"
    tmp.mkdir(exist_ok=True)
    for i, clip in enumerate(clips, 1):
        d = duration(clip)
        if d <= 0:
            print(f"  !! {clip.name}: unreadable duration")
            continue
        times = [d * (k + 1) / (a.frames + 1) for k in range(a.frames)]
        ims = []
        for k, t in enumerate(times):
            f = tmp / f"{i:03d}_{k}.jpg"
            subprocess.run([FFMPEG, "-v", "error", "-ss", f"{t:.2f}", "-i", str(clip),
                            "-frames:v", "1", "-q:v", "2", "-y", str(f)],
                           capture_output=True)
            if f.is_file():
                ims.append(Image.open(f).convert("RGB"))
        if not ims:
            print(f"  !! {clip.name}: no frames")
            continue
        h = round(ims[0].height * a.width / ims[0].width)
        ims = [im.resize((a.width, h), Image.LANCZOS) for im in ims]
        LAB = 26
        strip = Image.new("RGB", (a.width * len(ims), h + LAB), (12, 12, 12))
        for k, im in enumerate(ims):
            strip.paste(im, (k * a.width, 0))
        ImageDraw.Draw(strip).text((4, h + 5), f"{i:03d}  {clip.name}", fill=(255, 255, 255))
        strip.save(out / f"{i:03d}_{clip.stem[:48]}.png")
    for f in tmp.glob("*.jpg"):
        f.unlink()
    tmp.rmdir()
    print(f"[fullframe] {a.slug}: {len(clips)} clip(s) -> {out}")
    print("READ EVERY ONE. Ambiguity fails closed: if you cannot say what country it is in, reject it.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
