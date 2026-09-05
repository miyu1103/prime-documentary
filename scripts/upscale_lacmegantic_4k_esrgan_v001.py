#!/usr/bin/env python3
r"""Bring EP72 (PD-2026-072 "lacmegantic") plates to the ordered 3840 long edge.

Cloned from scripts/upscale_oroville_4k_esrgan_v001.py, which was written on 2026-08-20 when the
same constraint bit EP71: Codex's built-in image generation is fixed at 1672x941 and cannot be
prompted out of it, so the route to the required 3840 px long edge is a model upscale, not a
re-order. `PD_ONE_PASS_PRODUCTION_SPEC` row 5 permits it in terms.

WHAT IS DIFFERENT HERE, AND WHY IT MATTERS
The EP72 delivery is not one shape. Measured 2026-08-21 on the 120 delivered plates:

    92 plates  1672x941   ratio 1.777  -- 16:9, the same case as EP71
    28 plates  1881x836   ratio 2.250  -- NOT 16:9

This script handles ONLY the 92. The 28 are a separate decision: a 2.25:1 frame cannot become 16:9
without either black bars (rejected -- the film has no letterbox) or a horizontal crop that throws
away the sides of a composition nobody has looked at yet. They are listed in
`ep72_wide.json` and must be eyeballed before anything is done to them.

Real-ESRGAN x4plus on the GPU (1672x941 -> 6688x3764), then a LANCZOS reduction to exactly
3840x2160. NEVER overwrites the source directory.

    "C:/Users/aab15/stable-diffusion-webui/venv/Scripts/python.exe" \
        scripts/upscale_lacmegantic_4k_esrgan_v001.py
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np
import torch
from PIL import Image
from spandrel import ModelLoader

# The 28 cropped plates go through the SAME pass, from a different folder, so pass --src/--dst
# rather than cloning this file again.
SRC = Path(sys.argv[sys.argv.index("--src") + 1]) if "--src" in sys.argv else \
    Path(r"E:\pd-media\assets\ai\lacmegantic\_v001_raw")
DST = Path(sys.argv[sys.argv.index("--dst") + 1]) if "--dst" in sys.argv else \
    Path(r"E:\pd-media\assets\ai\lacmegantic\_v002_4k")
MODEL = Path(r"C:\Users\aab15\stable-diffusion-webui\models\RealESRGAN\RealESRGAN_x4plus.pth")
TARGET = (3840, 2160)
TILE = 512
OVERLAP = 32
RATIO_TOL = 0.05


def upscale(model, im: Image.Image, dev: str) -> Image.Image:
    x = torch.from_numpy(np.asarray(im.convert("RGB"), dtype="float32") / 255.0)
    x = x.permute(2, 0, 1).unsqueeze(0).to(dev)
    _, _, h, w = x.shape
    scale = model.scale
    out = torch.zeros((1, 3, h * scale, w * scale), device=dev)
    weight = torch.zeros_like(out)
    for top in range(0, h, TILE - OVERLAP):
        for left in range(0, w, TILE - OVERLAP):
            bot, right = min(top + TILE, h), min(left + TILE, w)
            with torch.no_grad():
                res = model(x[:, :, top:bot, left:right])
            out[:, :, top * scale:bot * scale, left * scale:right * scale] += res
            weight[:, :, top * scale:bot * scale, left * scale:right * scale] += 1.0
    arr = ((out / weight).clamp(0, 1)[0].permute(1, 2, 0).cpu().numpy() * 255.0)
    return Image.fromarray(arr.round().astype("uint8"))


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    if not MODEL.exists():
        print(f"FAIL: model not found: {MODEL}")
        return 2
    if not torch.cuda.is_available():
        print("FAIL: no CUDA. Run with the webui venv python (torch+cu121).")
        return 2

    todo, skipped = [], []
    for p in sorted(SRC.glob("*.png")):
        w, h = Image.open(p).size
        if abs(w / h - 16 / 9) > RATIO_TOL:
            skipped.append((p.name, f"{w}x{h}"))
        elif max(w, h) < TARGET[0]:
            todo.append(p)
    print(f"{len(todo)} plates to upscale; {len(skipped)} skipped as NOT 16:9 (decide separately)")

    model = ModelLoader().load_from_file(MODEL).eval().to("cuda")
    DST.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    for i, p in enumerate(todo, 1):
        dst = DST / p.name
        if dst.exists() and max(Image.open(dst).size) >= TARGET[0]:
            print(f"[{i}/{len(todo)}] {p.name} already done")
            continue
        im = Image.open(p)
        big = upscale(model, im, "cuda")
        big.resize(TARGET, Image.LANCZOS).save(dst, "PNG")
        print(f"[{i}/{len(todo)}] {p.name} {im.size[0]}x{im.size[1]} -> "
              f"{big.size[0]}x{big.size[1]} -> {TARGET[0]}x{TARGET[1]}  ({time.time()-t0:.0f}s)")

    bad = [p.name for p in DST.glob("*.png") if max(Image.open(p).size) < TARGET[0]]
    print(f"\ndone in {time.time()-t0:.0f}s -> {DST}")
    print(f"under {TARGET[0]} after the pass: {len(bad)}")
    print(f"STILL OWED, not handled here: {len(skipped)} non-16:9 plates")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
