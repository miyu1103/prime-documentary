#!/usr/bin/env python3
"""Find i2v clips that barely move, BEFORE they are built into a film.

EP65 marmet failed acceptance on a single 4.03-second near-still stretch at 18:53. The cause was
one motion clip, R013: 4.8 seconds of i2v output with almost no movement in it, looped to fill a
5.3-second slot. In the previous cut of the same film that clip happened to land on a short slot
and the stretch measured 2.1s, under the 3-second limit. Nothing changed about the clip; the
builder simply gave it more room, and a passing film became a failing one.

That is the shape of the bug worth fixing: the defect was always in the pool, and whether it
surfaced depended on where the shuffle put it. Measuring the pool removes the luck.

Each clip is measured with the same instrument the acceptance gate uses on the finished film --
freezedetect at the -38dB noise floor, which catches NEAR-still, not merely frozen. A clip whose
longest still stretch exceeds the per-cut limit can fail an episode wherever it lands, so it is
reported; a clip that is still for most of its length should not be in the pool at all.

    py -3.11 scripts/check_motion_clip_stillness.py --slug marmet
    py -3.11 scripts/check_motion_clip_stillness.py --slug marmet --quarantine

Exit 1 when any clip is unfit. --quarantine moves those clips out of the render-visible pool
(recoverably, to runs/qc/still_clips/<slug>) and records them so a rebuild cannot use them again.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:  # noqa: BLE001
    pass

ROOT = Path(__file__).resolve().parents[1]

NOISE_DB = -38.0     # same floor as check_final_acceptance's animation_density
MAX_HOLD = 3.0       # the per-cut limit the acceptance gate enforces
STILL_SHARE = 0.60   # a clip still for this much of itself is not motion, whatever the slot


def freeze_spans(path: Path) -> list[tuple[float, float]]:
    r = subprocess.run(
        ["ffmpeg", "-hide_banner", "-v", "info", "-i", str(path),
         "-vf", f"freezedetect=n={NOISE_DB}dB:d=0.5", "-an", "-f", "null", "-"],
        capture_output=True, text=True)
    out, spans, start = r.stderr, [], None
    for m in re.finditer(r"freeze_(start|duration|end):\s*([0-9.]+)", out):
        kind, val = m.group(1), float(m.group(2))
        if kind == "start":
            start = val
        elif kind == "duration" and start is not None:
            spans.append((start, val))
            start = None
    return spans


def duration(path: Path) -> float:
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", str(path)], capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return 0.0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--quarantine", action="store_true",
                    help="move unfit clips out of remotion/public/<slug>/motion (recoverable)")
    ap.add_argument("--max-hold", type=float, default=MAX_HOLD)
    a = ap.parse_args()

    pool = ROOT / "remotion" / "public" / a.slug / "motion"
    clips = sorted(pool.glob("*.mp4"))
    if not clips:
        print(f"[stillness] no clips in {pool}")
        return 0

    rows, unfit = [], []
    for i, c in enumerate(clips, 1):
        dur = duration(c)
        spans = freeze_spans(c)
        longest = max((d for _, d in spans), default=0.0)
        total = sum(d for _, d in spans)
        share = (total / dur) if dur else 0.0
        bad = longest > a.max_hold or share >= STILL_SHARE
        rows.append({"clip": c.name, "seconds": round(dur, 2),
                     "longest_still": round(longest, 2), "still_share": round(share, 3),
                     "unfit": bad})
        if bad:
            unfit.append(rows[-1])
        if i % 25 == 0 or i == len(clips):
            print(f"  [{i}/{len(clips)}] measured, {len(unfit)} unfit so far")

    print(f"\n[stillness] {a.slug}: {len(clips)} clip(s), {len(unfit)} unfit "
          f"(hold > {a.max_hold}s, or still for >= {STILL_SHARE:.0%} of the clip)")
    for r in sorted(unfit, key=lambda r: -r["longest_still"]):
        print(f"    {r['clip']:14s} {r['seconds']:5.2f}s  longest still {r['longest_still']:5.2f}s"
              f"  still {r['still_share'] * 100:4.0f}% of clip")

    out = ROOT / "runs" / "qc" / f"{a.slug}_motion_stillness.v001.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"schema_version": "motion_stillness.v001", "slug": a.slug,
                               "noise_db": NOISE_DB, "max_hold_seconds": a.max_hold,
                               "still_share_limit": STILL_SHARE, "clips": rows},
                              ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[stillness] report -> {out.relative_to(ROOT)}")

    if unfit and a.quarantine:
        dest = ROOT / "runs" / "qc" / "still_clips" / a.slug
        dest.mkdir(parents=True, exist_ok=True)
        for r in unfit:
            src = pool / r["clip"]
            if src.is_file():
                shutil.move(str(src), str(dest / r["clip"]))
        print(f"[stillness] moved {len(unfit)} clip(s) to {dest.relative_to(ROOT)} -- "
              f"rebuild the manifest and film.json before rendering")
    elif unfit:
        print("[stillness] re-run with --quarantine to remove them from the pool")
    return 1 if unfit else 0


if __name__ == "__main__":
    raise SystemExit(main())
