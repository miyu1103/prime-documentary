#!/usr/bin/env python
"""Flag clips whose change-over-time is a BUMP rather than a DRIFT.

This does not detect people and cannot. It exists to bound the blind spot of a sampled
contact strip: a strip built from frames at 33/67/100 cannot see something that arrives at
frame 45 and is gone by frame 60. Wan drift is monotonic -- the difference from frame 0 grows
and stays. Something that enters and leaves makes a hump.

For each clip it computes mean |luma diff| against frame 0 for every frame at thumbnail size,
then reports:
  peak      - the largest difference
  end       - the difference at the last frame
  bump      - peak minus end, i.e. how much was there at peak that is gone by the end
  unsampled - the largest difference at any frame more than 8 frames from a sampled frame

A large `bump` means a reviewer looking only at sampled frames may have missed a transient.
Clips are printed worst-bump first. Every flagged clip must then be LOOKED AT; this ranks
where to look, it does not decide anything.

    py -3.11 scripts/qc_i2v_transient_screen.py --slug station --samples 33,67,100
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]


def profile(mp4: Path) -> np.ndarray:
    with tempfile.TemporaryDirectory() as t:
        td = Path(t)
        subprocess.run(
            ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(mp4),
             "-vf", "scale=192:108,format=gray", "-vsync", "0", str(td / "f_%03d.png")],
            capture_output=True, timeout=300,
        )
        fs = sorted(td.glob("f_*.png"))
        if not fs:
            return np.zeros(1)
        a0 = np.asarray(Image.open(fs[0]), dtype=np.float32)
        return np.array([float(np.abs(np.asarray(Image.open(f), dtype=np.float32) - a0).mean())
                         for f in fs], dtype=np.float32)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--samples", default="33,67,100")
    ap.add_argument("--workers", type=int, default=4)
    a = ap.parse_args()
    sampled = [int(v) for v in a.samples.split(",")]

    motion = ROOT / "remotion" / "public" / a.slug / "motion"
    stems = sorted(p.stem for p in motion.glob("*.mp4") if not p.stem.endswith("_depth"))

    rows = []
    with cf.ThreadPoolExecutor(max_workers=a.workers) as ex:
        futs = {ex.submit(profile, motion / f"{s}.mp4"): s for s in stems}
        for f in cf.as_completed(futs):
            s = futs[f]
            p = f.result()
            if p.size < 5:
                rows.append((s, -1.0, -1.0, -1.0, -1))
                continue
            far = [i for i in range(p.size) if all(abs(i - k) > 8 for k in sampled)]
            uns = float(p[far].max()) if far else 0.0
            rows.append((s, float(p.max()), float(p[-1]), float(p.max()) - float(p[-1]),
                         int(p.argmax())))

    rows.sort(key=lambda r: -r[3])
    print(f"{'stem':6} {'peak':>7} {'end':>7} {'bump':>7} {'peak@':>6}")
    for s, pk, en, bp, ix in rows[:20]:
        print(f"{s:6} {pk:7.2f} {en:7.2f} {bp:7.2f} {ix:6d}")
    big = [r for r in rows if r[3] > 2.0]
    print(f"\n[screen] {len(rows)} clips; {len(big)} with bump > 2.0 (transient candidates)")
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    raise SystemExit(main())
