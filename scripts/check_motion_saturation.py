#!/usr/bin/env python
"""Refuse a build whose i2v clips lose their colour partway through.

EP75 lahaina, 2026-08-25: 37 of 91 hero clips opened in colour and played out as flat
grey. Two reviewers looked at the same frames and disagreed about whether they were depth
maps; neither could settle it by eye. Measuring did: mean RGB chroma fell from 11-27 at
10% of each clip to 0.0-1.3 at 90%, while the source plates were in colour.

The cause was a glob. `comfy_wan.py` collected a job's frames with
`<prefix>_*.png`, and that pattern also matches a DIFFERENT job whose prefix merely starts
with this one -- `lahaina_H041` swept in `lahaina_H041_depth`, so the clip assembled as 81
real frames followed by 81 frames of that scene's depth map. Anchoring the glob on digits
fixed it and re-assembling from each clip's own frames took the count from 37 to 6, all
six being scenes that are genuinely dark or grey (smoke, a night interior, burnt ground).

This check is the guard, because the next contamination will not announce itself either:
a clip whose colour collapses over its own duration is broken no matter what caused it.

    py -3.11 scripts/check_motion_saturation.py --slug lahaina [--json out.json]

Exit 0 = no clip collapses. Exit 1 = at least one does, and each is named with its numbers.
A clip that is low-chroma from start to finish is NOT flagged: that is a grade, not a fault.

2026-08-25, the same evening: this check MEASURED the clip that then failed the render and
passed it anyway. EP75 lahaina's POST-RENDER GATE failed on three black stretches after a
2.5-hour render, and all three were lahaina/motion/H014.mp4 -- recorded here as
s10=0.10, s50=17.8, s90=32.0. Chroma RISING from zero is not a collapse, so the rule above
never looked at it; but chroma near zero at the head of a clip means it is black or grey
THERE, and this file only ever asked about the direction of travel.

Black at the head is worse than it looks, because a cut loops a ~3.4s source into a ~6.3s
slot: one 1.2s black head becomes TWO holes in a single cut, and H014 was used in two cuts.
So the black test is deliberately stricter than the post-render gate it forecasts (0.4s
against 1.2s) -- the render is what costs hours, and this runs before it.
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]

# A clip is broken when it STARTS in colour and ENDS grey. Both halves matter: the floor
# alone would condemn a legitimately desaturated shot, and the ratio alone would condemn a
# clip that merely calms down.
END_GREY = 6.0     # mean chroma at 90% below this is grey to the eye
START_COLOUR = 12.0  # ...but only counts as a collapse if it began in real colour
COLLAPSE = 0.45    # or if it keeps less than this share of the colour it started with

# Black. The post-render gate refuses >= 1.2s in the FILM; a looped cut doubles a clip's
# head, so refuse half that in the CLIP, and refuse a head of any length at all.
HEAD_BLACK = 0.40   # seconds of black starting at t=0 -- the looping case
BODY_BLACK = 0.80   # seconds of black anywhere else
BLACK_RE = re.compile(r"black_start:([\d.]+)\s+black_end:([\d.]+)\s+black_duration:([\d.]+)")


def black_runs(path: str, min_dur: float = 0.20) -> list[tuple[float, float, float]]:
    """(start, end, duration) for every black run at or over `min_dur`, ffmpeg's own test.

    Same detector and same pixel threshold the post-render gate uses, so a clip this
    forecasts as black is black by the gate's definition too.
    """
    out = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-i", path,
         "-vf", f"blackdetect=d={min_dur}:pix_th=0.10", "-an", "-f", "null", "-"],
        capture_output=True, text=True)
    return [(float(a), float(b), float(c)) for a, b, c in BLACK_RE.findall(out.stderr)]


def chroma_at(path: str, frac: float) -> float | None:
    """Mean per-pixel (max-min) over RGB at `frac` through the clip. 0 = pure greyscale."""
    dur = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
        capture_output=True, text=True).stdout.strip()
    t = max(0.05, (float(dur) if dur else 3.0) * frac)
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tf:
        tmp = tf.name
    try:
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", str(t), "-i", path,
                        "-frames:v", "1", "-vf", "scale=160:-1", tmp], check=False)
        arr = np.asarray(Image.open(tmp).convert("RGB")).astype(float)
    except Exception:
        return None
    finally:
        os.unlink(tmp)
    return float((arr.max(axis=2) - arr.min(axis=2)).mean())


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--json", dest="json_out")
    a = ap.parse_args()

    pool = ROOT / "remotion" / "public" / a.slug / "motion"
    clips = sorted(glob.glob(str(pool / "*.mp4")))
    if not clips:
        print(f"[motion-sat] {a.slug}: no motion clips staged -- nothing to measure")
        return 0

    rows, broken, black = [], [], []
    for p in clips:
        s10, s50, s90 = chroma_at(p, 0.10), chroma_at(p, 0.50), chroma_at(p, 0.90)
        if None in (s10, s50, s90):
            print(f"[motion-sat] could not read {os.path.basename(p)} -- not measured")
            continue
        row = {"clip": os.path.basename(p), "s10": s10, "s50": s50, "s90": s90}
        runs = black_runs(p)
        head = [r for r in runs if r[0] < 0.05 and r[2] >= HEAD_BLACK]
        body = [r for r in runs if r[0] >= 0.05 and r[2] >= BODY_BLACK]
        if runs:
            row["black_runs"] = [{"start": a, "end": b, "dur": c} for a, b, c in runs]
        rows.append(row)
        if s10 >= START_COLOUR and (s90 < END_GREY or s90 < s10 * COLLAPSE):
            broken.append(row)
        if head or body:
            black.append((row, head, body))

    if a.json_out:
        Path(a.json_out).write_text(json.dumps(rows, indent=1), encoding="utf-8")

    print(f"[motion-sat] {a.slug}: {len(rows)} clip(s) measured, {len(broken)} losing colour, "
          f"{len(black)} with black (head >= {HEAD_BLACK}s or body >= {BODY_BLACK}s)")
    if broken:
        for r in sorted(broken, key=lambda r: r["s90"]):
            print(f"  COLLAPSE {r['clip']:24s} chroma {r['s10']:5.1f} -> {r['s50']:5.1f} -> {r['s90']:5.1f}")
        print("  These open in colour and end grey. Do not render them. Re-assemble the frame "
              "dirs from each clip's OWN frames (comfy_wan.py collects on a digit-anchored glob "
              "since 2026-08-25) and measure again.")
    if black:
        for row, head, body in sorted(black, key=lambda x: -max(r[2] for r in x[1] + x[2])):
            where = "HEAD" if head else "BODY"
            worst = max(r[2] for r in head + body)
            spans = ", ".join(f"{s:.2f}-{e:.2f}" for s, e, _ in (head + body)[:3])
            print(f"  BLACK-{where:4s} {row['clip']:24s} worst {worst:.2f}s  [{spans}]")
        print("  A cut loops a short source, so a black head is played TWICE per cut. The "
              "post-render gate will refuse the film after the render; refuse the CLIP now. "
              "Quarantine it out of remotion/public/<slug>/motion (and the E: archive copy, "
              "which is copied back), record it in config/footage_blocklist quality_deferred, "
              "and let the builder choose another.")
    if broken or black:
        return 1
    print("[motion-sat] no clip loses its colour and none opens black. This says nothing "
          "about what the clips SHOW.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
