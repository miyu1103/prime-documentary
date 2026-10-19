#!/usr/bin/env python3
r"""Contact sheets of i2v motion clips, first frame against last, for a human to read.

WHY THIS EXISTS
---------------
2026-08-21, EP70 wronghouse. `check_plate_verdicts` binds a verdict to the STILL. i2v then
makes a different artifact out of that still, and nothing on the ship path looks at it. On
EP70 that gap let Wan populate empty frames: W044's plate is a lit front door and a parked car
with nobody in it, and the clip has a woman in a white top walk up to the door -- in a film
about an FBI team raiding the wrong family's house. W012 grew three pedestrians, W035 a figure
that fills the frame, W066 a head and a hand.

**Neither of the documented remedies works here.** `i2v_episode_batch.py` carries a note from
EP61 weimer about exactly this (a dog in a blue harness; a hand) and offers `--prompt`, `--neg`
and `--seed-base` for it. Measured on W044: a prompt saying the scene "is empty and remains
empty", a negative listing person/people/human/figure/hand/face, and a fresh seed produced a
clip that is indistinguishable from the original. `comfy_wan.py` wires the negative into the
graph correctly, so it was applied and Wan overrode it.

So the defect has to be CAUGHT rather than prevented. This builds the sheet; a person reads it.
A clip whose last frame contains someone who is not in its plate is not a craft complaint, it
is `real_person_likeness` in an episode that declares 209 forbidden subjects.

WHAT IT CANNOT DO
-----------------
It does not detect people. It samples frames and lays them out. Every judgement is the
reviewer's, and a clip that only misbehaves in its middle frames can pass a first/last pair --
pass `--samples 4` when the register is one where that matters.

    py -3.11 scripts/qc_motion_clips.py --slug wronghouse
    py -3.11 scripts/qc_motion_clips.py --slug wronghouse --samples 4 --per-sheet 6
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def frames_of(clip: Path, out_dir: Path, samples: int) -> list[Path]:
    """Evenly spaced frames across the clip, written as jpgs. Empty list on failure."""
    n = probe_frames(clip)
    if n <= 1:
        return []
    idx = [int(round(i * (n - 1) / (samples - 1))) for i in range(samples)]
    sel = "+".join(f"eq(n\\,{i})" for i in idx)
    out = out_dir / f"{clip.stem}_row.jpg"
    r = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(clip), "-vf",
         f"select='{sel}',tile={samples}x1,scale={340 * samples}:-1", "-frames:v", "1",
         "-y", str(out)], capture_output=True, text=True)
    return [out] if out.exists() and r.returncode == 0 else []


def probe_frames(clip: Path) -> int:
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0",
                        "-count_frames", "-show_entries", "stream=nb_read_frames",
                        "-of", "csv=p=0", str(clip)], capture_output=True, text=True)
    try:
        return int(r.stdout.strip().split(",")[0])
    except Exception:
        return 0


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--samples", type=int, default=3, help="frames per clip (first..last)")
    ap.add_argument("--per-sheet", type=int, default=8)
    ap.add_argument("--only", help="comma-separated stems")
    args = ap.parse_args()

    from PIL import Image, ImageDraw  # noqa: E402

    motion = ROOT / "remotion" / "public" / args.slug / "motion"
    clips = sorted(motion.glob("*.mp4"))
    if args.only:
        want = {s.strip().upper() for s in args.only.split(",")}
        clips = [c for c in clips if c.stem.upper() in want]
    if not clips:
        print(f"no motion clips under {motion}")
        return 1

    out_dir = ROOT / "runs" / "qc" / "motion_frames" / args.slug
    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"{len(clips)} clip(s) in {motion}")

    rows: list[tuple[str, Path]] = []
    for c in clips:
        made = frames_of(c, out_dir, args.samples)
        if made:
            rows.append((c.stem, made[0]))
        else:
            print(f"  UNREADABLE: {c.name}")

    sheets = []
    for s in range(0, len(rows), args.per_sheet):
        chunk = rows[s:s + args.per_sheet]
        ims = [(stem, Image.open(p)) for stem, p in chunk]
        w = max(im.width for _, im in ims)
        rh = max(im.height for _, im in ims) + 20
        sheet = Image.new("RGB", (w, rh * len(ims) + 26), "black")
        d = ImageDraw.Draw(sheet)
        n = s // args.per_sheet + 1
        d.text((8, 6), f"{args.slug} motion clips -- sheet {n}  "
                       f"(left = first frame, right = last)  "
                       f"REJECT any clip whose people are not in its plate", fill="white")
        for i, (stem, im) in enumerate(ims):
            y = 26 + i * rh
            d.text((8, y + 2), stem, fill="yellow")
            sheet.paste(im, (0, y + 18))
        out = out_dir / f"{args.slug}_motion_{n:02d}.png"
        sheet.save(out)
        sheets.append(str(out.relative_to(ROOT)))

    receipt = ROOT / "runs" / "qc" / f"{args.slug}_motion_sheets.v001.json"
    receipt.write_text(json.dumps(
        {"slug": args.slug, "clips": len(rows), "samples_per_clip": args.samples,
         "sheets": sheets,
         "note": "The sheet is not a detector. A clip is rejected only by a reviewer who "
                 "compared it against its own plate in remotion/public/<slug>/img."},
        ensure_ascii=False, indent=1), encoding="utf-8")

    print(f"{len(sheets)} sheet(s) -> {out_dir}")
    for s in sheets:
        print(f"  {s}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
