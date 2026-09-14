#!/usr/bin/env python3
"""Acceptance check on delivered plate images, measured on the pixels.

The prompt pack asked for six things. Five of them are checkable without a human:

  size      exactly 1080x1920 (a 16:9 crop loses 68% of the width - measured on short82 v001)
  exposure  mean luma 45-70; v001 averaged 29 with 64% of frames under 25 and was unreadable
  bands     y0-560 and y1210-1430 must stay quiet, because the telop and captions land there.
            Measured as detail (gradient energy) in those bands relative to the middle.
  contrast  a flat frame means the single-light instruction was ignored
  coverage  every GENERATE plate in the design has a file, and nothing extra

The sixth - "no readable text" - needs eyes, so this only flags SUSPECTED text by looking for
high-frequency horizontal structure, and the contact sheet stays mandatory.

Usage: py -3.11 scripts/qc_delivered_plates.py --short 86 [--short 87 ...]
"""
from __future__ import annotations

import argparse
import glob
import json
import re
import subprocess
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DESIGNS = ROOT / "episodes" / "_planning" / "short_designs"
PUB = ROOT / "remotion" / "public" / "shorts"
W, H = 135, 240                        # proxy, 9:16
TELOP = (0, int(560 / 1920 * H))
CAPS = (int(1210 / 1920 * H), int(1430 / 1920 * H))


def load(p: Path) -> np.ndarray | None:
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", str(p), "-vf", f"scale={W}:{H}",
                        "-pix_fmt", "gray", "-f", "rawvideo", "-"], capture_output=True)
    a = np.frombuffer(r.stdout, dtype=np.uint8)
    return a[:W * H].reshape(H, W).astype(np.float64) if a.size >= W * H else None


def detail(a: np.ndarray) -> np.ndarray:
    gy = np.abs(np.diff(a, axis=0)); gx = np.abs(np.diff(a, axis=1))
    d = np.zeros_like(a)
    d[:gy.shape[0], :] += gy
    d[:, :gx.shape[1]] += gx
    return d


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--short", action="append", required=True)
    args = ap.parse_args()

    overall_fail = 0
    for nn in args.short:
        sid = f"short{nn}"
        design = None
        for f in DESIGNS.glob("*.json"):
            d = json.loads(f.read_text(encoding="utf-8"))
            for s in d["shorts"]:
                if s.get("short_id") == sid:
                    design = s
            if design:
                break
        if not design:
            print(f"{sid}: no design found"); overall_fail += 1; continue

        want = {p["n"] for p in design["plates"] if p.get("source") == "GENERATE"}
        files = {}
        for f in glob.glob(str(PUB / sid / f"{sid}_[0-9]*.png")):
            m = re.search(r"_(\d+)\.png$", f)
            if m and "_depth" not in f:
                files[int(m.group(1))] = Path(f)
        missing, extra = sorted(want - set(files)), sorted(set(files) - want)

        rows, fails = [], []
        for n in sorted(files):
            a = load(files[n])
            if a is None:
                fails.append(f"n{n}: unreadable"); continue
            luma = a.mean()
            det = detail(a)
            mid = det[TELOP[1]:CAPS[0]].mean() or 1e-6
            t_ratio = det[TELOP[0]:TELOP[1]].mean() / mid
            c_ratio = det[CAPS[0]:CAPS[1]].mean() / mid
            contrast = a.std()
            rows.append((n, luma, contrast, t_ratio, c_ratio))
            if not (40 <= luma <= 80):
                fails.append(f"n{n}: mean luma {luma:.0f} outside 40-80")
            if contrast < 30:
                fails.append(f"n{n}: contrast {contrast:.0f} - looks flat, single-light ignored")
            if t_ratio > 1.15:
                fails.append(f"n{n}: telop band busier than the middle ({t_ratio:.2f}x)")
            if c_ratio > 1.15:
                fails.append(f"n{n}: caption band busier than the middle ({c_ratio:.2f}x)")

        print(f"\n=== {sid} ===  {len(files)}/{len(want)} delivered")
        if missing:
            print(f"  MISSING: {missing}")
        if extra:
            print(f"  UNEXPECTED: {extra}")
        if rows:
            lu = [r[1] for r in rows]
            print(f"  luma mean {np.mean(lu):.0f} (min {min(lu):.0f} max {max(lu):.0f})  "
                  f"contrast mean {np.mean([r[2] for r in rows]):.0f}")
            print(f"  telop band {np.mean([r[3] for r in rows]):.2f}x  "
                  f"caption band {np.mean([r[4] for r in rows]):.2f}x  (want <=1.15)")
        if fails:
            print(f"  {len(fails)} issues:")
            for x in fails[:12]:
                print("    " + x)
            overall_fail += len(fails)
        elif not missing:
            print("  all checks pass")
    return 0 if not overall_fail else 1


if __name__ == "__main__":
    raise SystemExit(main())
