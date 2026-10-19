#!/usr/bin/env python
"""PD Visual System — P08 depth-map PoC (Depth Anything V2 SMALL, Apache-2.0).

Standalone `depth_anything_v2` package (NOT transformers — avoids version conflicts),
ViT-S checkpoint only (Base/Large/Giant are CC-BY-NC = forbidden commercial). Writes
<stem>_depth.png (grayscale 'L', source size, 0..1, nearer=brighter) matching the repo
convention consumed by DepthStill/DepthImageV.
"""
from __future__ import annotations
import argparse, sys
from pathlib import Path
import numpy as np
import cv2

CKPT = r"D:\PD_AI_Models\depth\depth_anything_v2_vits.pth"  # ViT-S, Apache-2.0
CFG = dict(encoder="vits", features=64, out_channels=[48, 96, 192, 384])


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", default=None)
    ap.add_argument("--ckpt", default=CKPT)
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    src = Path(a.input)
    if not src.exists():
        print(f"missing input: {src}", file=sys.stderr); return 2
    out = Path(a.output) if a.output else src.with_name(src.stem + "_depth.png")
    if out.exists() and not a.force:
        print(f"exists (use --force): {out}"); return 0
    if a.dry_run:
        print(f"[dry-run] DepthAnythingV2 vits -> {out}"); return 0

    import torch
    from depth_anything_v2.dpt import DepthAnythingV2
    dev = "cuda" if torch.cuda.is_available() else "cpu"
    model = DepthAnythingV2(**CFG)
    model.load_state_dict(torch.load(a.ckpt, map_location="cpu"))
    model = model.to(dev).eval()

    img = cv2.imread(str(src))  # BGR
    if img is None:
        print(f"cv2 could not read {src}", file=sys.stderr); return 2
    with torch.no_grad():
        depth = model.infer_image(img)  # HxW float, larger = nearer
    d = depth.astype("float32")
    d = (d - d.min()) / (d.max() - d.min() + 1e-8)  # 0..1, nearer=bright
    tmp = out.with_name(out.stem + ".tmp.png")  # keep .png so cv2 picks the encoder
    cv2.imwrite(str(tmp), (d * 255).astype(np.uint8))
    tmp.replace(out)
    print(f"wrote {out} {img.shape[1]}x{img.shape[0]} device={dev}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
