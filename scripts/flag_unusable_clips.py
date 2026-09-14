#!/usr/bin/env python3
"""Flag archive clips that no documentary Short can use, before a human looks at them.

Every eye-QC pass over this shelf keeps finding the same three shapes, and they are the ones a
score cannot see:

  * chroma-key plates - a bright green field with a prop keyed over it. Six turned up in one
    263-frame review, including a cartoon school bus and a crumpled sheet of paper.
  * near-flat frames - a colour swatch, a blurred wall, a light leak. Nothing is depicted.
  * film-leader and slate frames - a countdown "6", a black card reading "428.NPC.1605".

The first two are measurable from one frame and this measures them. The third is text, and text
detection on a still is not reliable enough to gate on, so it stays with the eye.

This does not replace the eye pass. It removes the cases the eye should never have to spend
attention on, so the review that remains is about whether the picture MEANS the right thing.

Usage:
  py -3.11 scripts/flag_unusable_clips.py --report runs/footage_semantic/bind_report.json
  py -3.11 scripts/flag_unusable_clips.py --report ... --write-pairs
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "runs" / "footage_semantic"
PAIRS = INDEX / "rejected_pairs.txt"

# Calibrated on the known-bad frames from the 2026-08-04 review and on 40 known-good ones.
GREEN_FRAC = 0.25     # a keying plate is mostly green; a lawn or a lit exit sign is not
FLAT_STD = 14.0       # luma standard deviation; a real scene is textured, a swatch is not

# Clips whose own filename declares them synthetic. This channel documents real cases, and
# CLAUDE.md invariant 11 forbids presenting generated visuals as authentic record. Nineteen were
# already bound into finished Shorts before anyone looked - an AI police officer under a line about
# a real arrest, an AI spaceship corridor, a generated red panda. A picture check cannot catch
# these: they are competent images of things that never happened.
SYNTHETIC = re.compile(r"ai[-_]generated|generated[-_]ai|ai[-_]art|midjourney|"
                       r"stable[-_]diffusion|\bcgi\b|3d[-_]render", re.I)


def probe(clip: str) -> tuple[float, float] | None:
    """Green-screen fraction and luma spread, from one frame at 1.2 s."""
    import numpy as np
    r = subprocess.run(["ffmpeg", "-v", "error", "-ss", "1.2", "-i", clip, "-frames:v", "1",
                        "-vf", "scale=160:284", "-pix_fmt", "rgb24", "-f", "rawvideo", "-"],
                       capture_output=True)
    if r.returncode != 0 or len(r.stdout) < 160 * 284 * 3:
        return None
    a = np.frombuffer(r.stdout[:160 * 284 * 3], dtype=np.uint8).reshape(284, 160, 3).astype("int16")
    R, G, B = a[..., 0], a[..., 1], a[..., 2]
    green = ((G > 100) & (G > R * 3 // 2) & (G > B * 3 // 2)).mean()
    luma = (0.299 * R + 0.587 * G + 0.114 * B)
    return float(green), float(luma.std())


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", default=str(INDEX / "bind_report.json"))
    ap.add_argument("--write-pairs", action="store_true",
                    help="append the flagged plates to rejected_pairs.txt")
    # A chroma-key plate is not wrong for one plate, it is unusable everywhere, and the same clip
    # is on the shelf several times under different theme folders - v_95514 sits in both
    # goods_in_motion and economy_crisis. Excluding one path just hands the binder its twin, which
    # is why the flag count stopped falling at three. The global list, matched on basename, ends it.
    ap.add_argument("--write-global", action="store_true",
                    help="add every copy of each flagged clip to rejected_clips.txt (by filename)")
    a = ap.parse_args()

    rows = json.loads(Path(a.report).read_text(encoding="utf-8"))["bound"]
    flagged, unreadable = [], 0
    for i, x in enumerate(rows, 1):
        m = probe(x["bound_file"])
        if m is None:
            unreadable += 1
            continue
        green, std = m
        why = ("declared synthetic in its own filename" if SYNTHETIC.search(Path(x["bound_file"]).name)
               else "chroma-key plate (%.0f%% green)" % (green * 100) if green >= GREEN_FRAC
               else "near-flat frame (luma sd %.1f)" % std if std < FLAT_STD else None)
        if why:
            flagged.append((x, why))
        if i % 200 == 0:
            print(f"  {i}/{len(rows)} probed, {len(flagged)} flagged")

    print(f"\nprobed {len(rows)}  unreadable {unreadable}  FLAGGED {len(flagged)}")
    for x, why in flagged[:40]:
        print(f"  {x['short']} p{x['n']:02d}  {why:<34} {Path(x['bound_file']).name[:52]}")
    if len(flagged) > 40:
        print(f"  ... and {len(flagged) - 40} more")

    if a.write_global and flagged:
        names = {Path(x["bound_file"]).name for x, _ in flagged}
        paths = json.loads((INDEX / "paths.json").read_text(encoding="utf-8"))
        copies = sorted(p for p in paths if Path(p).name in names)
        g = INDEX / "rejected_clips.txt"
        old = g.read_text(encoding="utf-8").rstrip().splitlines() if g.exists() else []
        add = [p for p in copies if p not in old]
        g.write_text("\n".join(old + ["# mechanical: chroma-key / near-flat, every copy on the shelf"]
                               + add) + "\n", encoding="utf-8")
        print(f"\n{len(names)} distinct clips -> {len(add)} paths added to "
              f"{g.relative_to(ROOT)} (duplicates across theme folders included)")

    if a.write_pairs and flagged:
        old = PAIRS.read_text(encoding="utf-8").rstrip().splitlines() if PAIRS.exists() else []
        add = [f"{x['short']} {x['n']} {x['bound_file']}" for x, _ in flagged]
        PAIRS.write_text("\n".join(old + ["# mechanical: chroma-key / near-flat frames"] + add)
                         + "\n", encoding="utf-8")
        print(f"\nappended {len(add)} exclusions to {PAIRS.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
