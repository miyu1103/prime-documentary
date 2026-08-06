#!/usr/bin/env python3
"""Reject an i2v clip that moves by destroying the picture instead of moving what is in it.

Why this exists: on 2026-08-06 the motion prompts were strengthened because the first clips had a
third of the reference amplitude, and the channel's standing complaint is that there is not enough
animation. Amplitude went up -- median 8.6 to 19.2 against a reference of 7.4 -- and the pictures
started dissolving. The worst clips fill with white haze or erupt in orange light by the third
second: the heater room whites out, the corridor fogs over, the table catches fire in bloom. The
number went the right way and the thing it stood for went the wrong way.

So amplitude alone is not the test. A clip is good when things IN the picture move and the picture
survives. Three measurements, all on the luma plane:

  amplitude    mean |first - last|. Too low is kamishibai; too high is usually dissolution.
  luma drift   |mean(last) - mean(first)|. Fog and bloom brighten the frame; real motion does not.
  contrast     sd(last) / sd(first). Haze flattens the picture; a value well under 1 is a wash-out.

    py scripts/check_motion_integrity.py --slug correa
    py scripts/check_motion_integrity.py --slug correa --delete      # remove the failures

Exit 0 when every clip passes.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[1]
TMP = Path(r"E:\UserTemp\aab15\claude\C--Users-aab15\d654d1fe-e458-4466-83a4-f13b171f9f50\scratchpad\mi")

# Set from the reference clip the assembly thread already made (amplitude 7.4, drift ~1) and from
# the measured failures (amplitude 50-82, drift 20-60, contrast ratio far from 1).
AMP_MIN, AMP_MAX = 2.5, 30.0
DRIFT_MAX = 12.0
CONTRAST_LO, CONTRAST_HI = 0.72, 1.40
# Detail that was not in the plate: text written onto a blank page, objects arriving in empty
# space. Measured over 427 clips the median is 0.58% and p90 is 2.79%; the defects found by eye
# sit between 5.4 and 13.6.
DETAIL_GAIN_MAX = 3.5
FLAT_SD, DETAIL_SD = 3.0, 9.0


def probe_duration(clip: Path) -> float:
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", str(clip)], capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return 0.0


def grab(clip: Path, t: float) -> np.ndarray | None:
    TMP.mkdir(parents=True, exist_ok=True)
    out = TMP / f"{clip.stem}_{t:.2f}.png"
    r = subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t}", "-i", str(clip),
                        "-frames:v", "1", "-vf", "scale=384:-1", str(out)],
                       capture_output=True, text=True)
    if r.returncode or not out.exists():
        return None
    return np.asarray(Image.open(out).convert("L")).astype("float32")


def local_sd(a: np.ndarray, k: int = 5) -> np.ndarray:
    """Standard deviation in a k x k window, via summed-area tables."""
    def box(x: np.ndarray) -> np.ndarray:
        c = np.cumsum(np.cumsum(x, 0), 1)
        c = np.pad(c, ((1, 0), (1, 0)))
        return (c[k:, k:] - c[:-k, k:] - c[k:, :-k] + c[:-k, :-k]) / (k * k)
    m, m2 = box(a), box(a * a)
    return np.sqrt(np.maximum(m2 - m * m, 0))


def measure(clip: Path) -> dict:
    d = probe_duration(clip)
    a, b = grab(clip, 0.10), grab(clip, max(0.2, d - 0.15))
    if a is None or b is None:
        return {"clip": clip, "ok": False, "why": "unreadable"}
    amp = float(np.abs(a - b).mean())
    drift = float(abs(b.mean() - a.mean()))
    contrast = float(b.std() / a.std()) if a.std() > 1e-6 else 0.0
    sa, sb = local_sd(a), local_sd(b)
    gain = float(((sa < FLAT_SD) & (sb > DETAIL_SD)).mean() * 100)
    why = []
    if amp < AMP_MIN:
        why.append(f"barely moves (amplitude {amp:.1f} < {AMP_MIN})")
    if amp > AMP_MAX:
        why.append(f"amplitude {amp:.1f} > {AMP_MAX} -- usually the picture dissolving")
    if drift > DRIFT_MAX:
        why.append(f"luma drifts {drift:.1f} -- fog, bloom or a light leak")
    if not (CONTRAST_LO <= contrast <= CONTRAST_HI):
        why.append(f"contrast x{contrast:.2f} -- the picture is washing out or crushing")
    if gain > DETAIL_GAIN_MAX:
        why.append(f"{gain:.1f}% of the frame gains detail it did not have -- text written onto "
                   f"blank paper, or objects arriving")
    return {"clip": clip, "dur": d, "amp": amp, "drift": drift, "contrast": contrast,
            "gain": gain, "ok": not why, "why": "; ".join(why)}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--delete", action="store_true",
                    help="remove failing clips so the builder remakes them")
    a = ap.parse_args()

    d = ROOT / "remotion" / "public" / a.slug / "motion"
    clips = sorted(d.glob("*.mp4"))
    if not clips:
        print(f"[motion] {a.slug}: no clips in {d}", file=sys.stderr)
        return 1

    rows = [measure(c) for c in clips]
    bad = [r for r in rows if not r["ok"]]
    amps = np.array([r["amp"] for r in rows if "amp" in r])
    drifts = np.array([r["drift"] for r in rows if "drift" in r])
    gains = np.array([r["gain"] for r in rows if "gain" in r])
    print(f"[motion] {a.slug}: {len(clips)} clip(s)  "
          f"amplitude median {np.median(amps):.1f} (band {AMP_MIN}-{AMP_MAX})  "
          f"luma drift median {np.median(drifts):.1f} (max {DRIFT_MAX})  "
          f"detail gain median {np.median(gains):.2f}% (max {DETAIL_GAIN_MAX})")
    for r in bad:
        print(f"  REJECT {r['clip'].stem}: {r['why']}")
    print(f"[motion] {a.slug}: {len(clips)-len(bad)} pass, {len(bad)} fail")

    if a.delete:
        for r in bad:
            r["clip"].unlink()
        print(f"[motion] deleted {len(bad)} clip(s); re-run the builder to remake them")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
