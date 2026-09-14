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
import json
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


def compose(ims: list["Image.Image"], width: int, label: str, stack: bool) -> "Image.Image":
    """One reviewable picture per clip. `stack` puts the frames in a column."""
    h = round(ims[0].height * width / ims[0].width)
    ims = [im.resize((width, h), Image.LANCZOS) for im in ims]
    LAB = 26
    if stack:
        out = Image.new("RGB", (width, h * len(ims) + LAB), (12, 12, 12))
        for k, im in enumerate(ims):
            out.paste(im, (0, k * h))
        ImageDraw.Draw(out).text((4, h * len(ims) + 5), label, fill=(255, 255, 255))
        return out
    out = Image.new("RGB", (width * len(ims), h + LAB), (12, 12, 12))
    for k, im in enumerate(ims):
        out.paste(im, (k * width, 0))
    ImageDraw.Draw(out).text((4, h + 5), label, fill=(255, 255, 255))
    return out


def from_frames(a: argparse.Namespace) -> int:
    """Group pre-extracted `<clip>__NN_t*.jpg` frames into one strip per clip."""
    src = Path(a.from_frames)
    out = Path(a.out) if a.out else ROOT / "runs" / "qc" / "fullframe" / f"{a.slug}_candidates"
    out.mkdir(parents=True, exist_ok=True)
    # The frames dir is a CONTENT CACHE shared across episodes and across re-runs, so it holds
    # clips this episode already dropped mechanically. Reviewing those is wasted looking.
    keep: set[str] | None = None
    if a.limit_to:
        plan = json.loads(Path(a.limit_to).read_text(encoding="utf-8"))
        keep = {str(r["clip"]).split("__")[0] for r in plan.get("presented", [])}
        print(f"[fullframe] limited to {len(keep)} clip(s) still presented by {Path(a.limit_to).name}")
    by_clip: dict[str, list[Path]] = {}
    for f in sorted(src.glob("*.jpg")):
        clip = f.name.split("__")[0]
        if keep is not None and clip not in keep:
            continue
        by_clip.setdefault(clip, []).append(f)
    if not by_clip:
        print(f"no frames in {src}")
        return 1
    for i, (clip, files) in enumerate(sorted(by_clip.items()), 1):
        # spread the picks across the clip's own length, never the first or last frame only
        if len(files) <= a.frames:
            picks = files
        else:
            step = (len(files) - 1) / (a.frames - 1) if a.frames > 1 else 0
            picks = [files[round(k * step)] for k in range(a.frames)]
        ims = [Image.open(p).convert("RGB") for p in picks]
        strip = compose(ims, a.width, f"{i:03d}  {clip}  ({len(files)} frames sampled)", a.stack)
        strip.save(out / f"{i:03d}_{clip[:56]}.png")
    print(f"[fullframe] {a.slug}: {len(by_clip)} clip(s) from cached frames -> {out}")
    print("READ EVERY ONE. Ambiguity fails closed: if you cannot say what country it is in, reject it.")
    return 0


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--pool", help="default remotion/public/<slug>/factory")
    ap.add_argument("--out", help="default runs/qc/fullframe/<slug>")
    ap.add_argument("--frames", type=int, default=2)
    ap.add_argument("--width", type=int, default=900)
    ap.add_argument("--from-frames",
                    help="build strips from ALREADY EXTRACTED jpgs (prestage_footage_review "
                         "writes runs/qc/prestage_frames/<slug>/frames/<clip>__NN_t*.jpg at "
                         "960 px). Judges candidates BEFORE they are copied, which is the "
                         "order prestage_footage_review.py exists to enforce; nothing is "
                         "decoded twice.")
    ap.add_argument("--limit-to",
                    help="a runs/qc/<slug>_prestage.v001.json -- only clips still in its "
                         "`presented` list get a strip")
    ap.add_argument("--stack", action="store_true",
                    help="stack the frames vertically instead of side by side. A 960x1620 "
                         "column survives the reviewer's own downscale at ~929 px per frame; "
                         "the same three frames in a row arrive at ~520 px, which is the tile "
                         "size that hid 24 foreign clips on EP77.")
    a = ap.parse_args()

    if a.from_frames:
        return from_frames(a)

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
        strip = compose(ims, a.width, f"{i:03d}  {clip.name}", a.stack)
        strip.save(out / f"{i:03d}_{clip.stem[:48]}.png")
    for f in tmp.glob("*.jpg"):
        f.unlink()
    tmp.rmdir()
    print(f"[fullframe] {a.slug}: {len(clips)} clip(s) -> {out}")
    print("READ EVERY ONE. Ambiguity fails closed: if you cannot say what country it is in, reject it.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
