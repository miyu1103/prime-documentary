#!/usr/bin/env python3
"""Score every commercially-usable archive clip for VERTICAL Shorts use, once, into a cache.

The archive holds ~25,858 clips we may use commercially, and we have been hand-picking twelve at
a time. The blocker was never supply, it was search:

  * filenames lie      - AF-BG-34700__padlock_and_chain.mp4 is titled "handcuffs under police lights"
  * keywords lie       - "bars" returned gold bullion; "court" returned a cartoon judge
  * 9:16 is brutal     - a centre crop of a 16:9 frame keeps 31.6% of the width, so a wide
                         establishing shot is unusable however good the title reads
  * some carry text    - one paper clip had a fully readable "Lease Agreement" on screen

So this measures, per clip, the three things a human otherwise has to eyeball:

  centre_energy  fraction of the frame's detail (Sobel-ish gradient) that falls inside the
                 centre 9:16 column. High = the subject survives the crop.
  motion         mean |frame delta| on a tiny greyscale proxy. Low = a still with a container.
  luma           mean brightness of the CROPPED region, not the whole frame.

Writes E:/pd-media/assets/archive/_qc/vertical_index.jsonl (resumable; re-running skips done rows).

Usage:
  py -3.11 scripts/index_archive_vertical.py --limit 400
  py -3.11 scripts/index_archive_vertical.py --theme crime_police --limit 2000
"""
from __future__ import annotations

import argparse
import glob
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

LEDGER = r"E:\pd-media\assets\archive\_ledger\*.jsonl"
OUT = Path(r"E:\pd-media\assets\archive\_qc\vertical_index.jsonl")
W, H = 128, 72          # proxy frame for the whole 16:9 image
USABLE = {"free_commercial", "pd", "cc0"}


def rows():
    seen = set()
    for f in sorted(glob.glob(LEDGER)):
        for line in open(f, encoding="utf-8", errors="replace"):
            line = line.strip()
            if not line:
                continue
            try:
                d = json.loads(line)
            except Exception:
                continue
            p = d.get("file_path")
            if (not p or p in seen or d.get("kind") != "video"
                    or d.get("license_decision") not in USABLE):
                continue
            seen.add(p)
            yield d


def frames(path: str, n: int = 6) -> np.ndarray | None:
    """n evenly spread greyscale proxy frames."""
    r = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", path, "-vf",
         f"select='not(mod(n\\,15))',scale={W}:{H}", "-vsync", "0", "-frames:v", str(n),
         "-pix_fmt", "gray", "-f", "rawvideo", "-"],
        capture_output=True)
    a = np.frombuffer(r.stdout, dtype=np.uint8)
    k = len(a) // (W * H)
    if k < 2:
        return None
    return a[:k * W * H].reshape(k, H, W).astype(np.int16)


def score(f: np.ndarray) -> dict:
    # detail map = gradient magnitude, averaged over sampled frames
    gy = np.abs(np.diff(f, axis=1)).sum(axis=(0,))[:, :]      # (H-1, W)
    gx = np.abs(np.diff(f, axis=2)).sum(axis=(0,))[:, :]      # (H, W-1)
    detail = np.zeros((H, W), dtype=np.float64)
    detail[:gy.shape[0], :] += gy
    detail[:, :gx.shape[1]] += gx
    # the 9:16 centre column that a Short actually shows
    cw = int(round(H * 9 / 16))
    x0 = (W - cw) // 2
    centre = detail[:, x0:x0 + cw].sum()
    total = detail.sum() or 1.0
    motion = float(np.abs(np.diff(f, axis=0)).mean())
    luma_crop = float(f[:, :, x0:x0 + cw].mean())
    return {"centre_energy": round(centre / total, 4),
            "motion": round(motion, 3),
            "luma_crop": round(luma_crop, 1)}


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=300)
    ap.add_argument("--theme", default=None)
    args = ap.parse_args()

    OUT.parent.mkdir(parents=True, exist_ok=True)
    done = set()
    if OUT.exists():
        for line in OUT.open(encoding="utf-8"):
            try:
                done.add(json.loads(line)["file_path"])
            except Exception:
                pass
    print(f"{len(done)} clips already indexed")

    n = ok = 0
    with OUT.open("a", encoding="utf-8") as fh:
        for d in rows():
            if n >= args.limit:
                break
            p = d["file_path"]
            if p in done or (args.theme and d.get("theme") != args.theme):
                continue
            if not Path(p).exists():
                continue
            n += 1
            f = frames(p)
            if f is None:
                continue
            rec = {"file_path": p, "title": d.get("title"), "theme": d.get("theme"),
                   "license": d.get("license_decision"), "source": d.get("source"), **score(f)}
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
            ok += 1
            if ok % 25 == 0:
                print(f"  indexed {ok}/{n}")
    print(f"indexed {ok} new clips (scanned {n}) -> {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
