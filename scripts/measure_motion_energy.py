#!/usr/bin/env python3
r"""Measure MOTION ENERGY (how much the frame actually moves), not just 'not frozen'.

animation_density only measures the fraction of near-still time; a slow drift / Ken Burns /
weak parallax passes it while looking like a slideshow (Goodhart). This measures the average
inter-frame pixel change (a frame-difference / optical-flow proxy) via ffmpeg
`tblend=difference + signalstats(YAVG)`. Higher YAVG = more real motion. It reports the mean
and the 10th-percentile (sustained-low) energy over the BODY, so a positive LOWER BOUND can be
set — calibrated on a truly-dynamic reference (MotionSample) vs a slideshow.

    py -3.11 scripts/measure_motion_energy.py <mp4> [--body-lo 11.5 --body-hi-from-end 9]
"""
from __future__ import annotations
import argparse, os, re, subprocess, sys


def per_frame_yavg(path: str) -> list[float]:
    # difference between consecutive frames -> signalstats YAVG per frame (0..255)
    out = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-i", path,
         "-vf", "tblend=all_mode=difference,format=gray,signalstats,metadata=print:key=lavfi.signalstats.YAVG:file=-",
         "-an", "-f", "null", os.devnull],
        capture_output=True, text=True, timeout=1800)
    return [float(x) for x in re.findall(r"lavfi\.signalstats\.YAVG=([0-9.]+)", out.stdout + out.stderr)]


def stats(vals: list[float]):
    if not vals:
        return None
    s = sorted(vals)
    n = len(s)
    mean = sum(s) / n
    p10 = s[max(0, int(0.10 * n))]
    p50 = s[n // 2]
    return {"mean": mean, "p10": p10, "p50": p50, "n": n}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mp4")
    ap.add_argument("--fps", type=float, default=30.0)
    ap.add_argument("--body-lo", type=float, default=11.5, help="skip this many head seconds (hook+OP)")
    ap.add_argument("--body-hi-from-end", type=float, default=9.0, help="skip this many tail seconds (endcard)")
    args = ap.parse_args()
    y = per_frame_yavg(args.mp4)
    if not y:
        print("no YAVG parsed (ffmpeg filter unavailable?)"); return 1
    lo = int(args.body_lo * args.fps)
    hi = max(lo + 1, len(y) - int(args.body_hi_from_end * args.fps))
    body = y[lo:hi]
    full_s = stats(y); body_s = stats(body)
    print(f"{os.path.basename(args.mp4)}")
    print(f"  FULL  mean={full_s['mean']:.2f} p10={full_s['p10']:.2f} p50={full_s['p50']:.2f} (frames {full_s['n']})")
    print(f"  BODY  mean={body_s['mean']:.2f} p10={body_s['p10']:.2f} p50={body_s['p50']:.2f} (frames {body_s['n']})")
    print("  (YAVG 0..255 of the inter-frame difference; higher = more real motion. p10 = sustained-low floor.)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
