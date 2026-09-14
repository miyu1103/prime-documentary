# -*- coding: utf-8 -*-
"""Generate DPT depth maps for a staged episode's hero stills (challenge#1 3D parallax).

The current CaseFilm depth-parallax treatment REQUIRES a `<stem>_depth.png` next to every
hero image (else the render crashes: "Could not load .../<stem>_depth.png"). EP28/29/31
already have them; EP30 (cotton) was built before the port and has none. This fills that
gap locally with Intel/dpt-large (same model the parallel thread used), writing grayscale
'L' depth maps at the source image size — matching the hinton reference format.

Usage: python scripts/gen_depth_maps.py --dir remotion/public/cotton/img
"""
from __future__ import annotations
import argparse
import sys
from pathlib import Path

import numpy as np
import torch
from PIL import Image
from transformers import DPTImageProcessor, DPTForDepthEstimation

MODEL = "Intel/dpt-large"


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True, help="folder of hero PNGs (skips *_depth.png)")
    ap.add_argument("--force", action="store_true", help="regenerate even if _depth exists")
    a = ap.parse_args()
    d = Path(a.dir)
    imgs = sorted(p for p in d.glob("*.png") if not p.stem.endswith("_depth"))
    if not imgs:
        print(f"no hero PNGs in {d}")
        return 2
    print(f"loading {MODEL} (first run downloads ~1.4GB)...", flush=True)
    proc = DPTImageProcessor.from_pretrained(MODEL)
    model = DPTForDepthEstimation.from_pretrained(MODEL).eval()
    torch.set_grad_enabled(False)

    done = skip = 0
    for p in imgs:
        out = p.with_name(p.stem + "_depth.png")
        if out.exists() and not a.force:
            skip += 1
            continue
        im = Image.open(p).convert("RGB")
        inp = proc(images=im, return_tensors="pt")
        pred = model(**inp).predicted_depth  # (1, h', w'), larger = nearer (MiDaS/DPT)
        pred = torch.nn.functional.interpolate(
            pred.unsqueeze(1), size=im.size[::-1], mode="bicubic", align_corners=False
        ).squeeze()
        arr = pred.cpu().numpy()
        arr = (arr - arr.min()) / (arr.max() - arr.min() + 1e-8)  # 0..1
        Image.fromarray((arr * 255).astype(np.uint8), mode="L").save(out)
        done += 1
        print(f"  {out.name}  {im.size}", flush=True)
    print(f"done: generated={done} skipped_existing={skip} total_heroes={len(imgs)} dir={d}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
