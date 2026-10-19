#!/usr/bin/env python3
r"""Upscale an episode's Codex plates to the 3840x2160 render set — generic --slug form.

Fourth copy of the same one-off (hinders, itaewon, lacmegantic, oroville) parameterised
instead of copied (invariant 14). Codex delivers 1672x941; sources stay immutable where
they were delivered, Real-ESRGAN x4plus runs in tiles, LANCZOS reduces to exactly
3840x2160. Never overwrites a source or an existing destination plate.

Needs the CUDA venv:

    "C:/Users/aab15/stable-diffusion-webui/venv/Scripts/python.exe" \
        scripts/upscale_plates_4k_esrgan.py --slug keybridge \
        --src E:/pd-media/05_visuals/keybridge/img --prefix K --count 131
"""
from __future__ import annotations

import argparse
import re
import sys
import time
from pathlib import Path

import torch
from PIL import Image
from spandrel import ModelLoader

ROOT = Path(__file__).resolve().parents[1]
MODEL = Path(r"C:\Users\aab15\stable-diffusion-webui\models\RealESRGAN\RealESRGAN_x4plus.pth")
TARGET = (3840, 2160)
TILE = 512
OVERLAP = 32


def upscale(model, image: Image.Image, device: str) -> Image.Image:
    import numpy
    x = torch.from_numpy(
        numpy.asarray(image.convert("RGB"), dtype="float32") / 255.0
    ).permute(2, 0, 1).unsqueeze(0).to(device)
    _, _, height, width = x.shape
    scale = model.scale
    out = torch.zeros((1, 3, height * scale, width * scale), device=device)
    weight = torch.zeros_like(out)
    for top in range(0, height, TILE - OVERLAP):
        for left in range(0, width, TILE - OVERLAP):
            bottom, right = min(top + TILE, height), min(left + TILE, width)
            tile = x[:, :, top:bottom, left:right]
            with torch.no_grad():
                result = model(tile)
            out[:, :, top * scale:bottom * scale, left * scale:right * scale] += result
            weight[:, :, top * scale:bottom * scale, left * scale:right * scale] += 1.0
    out = (out / weight).clamp(0, 1)
    array = (out[0].permute(1, 2, 0).cpu().numpy() * 255.0).round().astype("uint8")
    return Image.fromarray(array)


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--src", required=True, help="delivered plates dir (stays immutable)")
    ap.add_argument("--prefix", required=True, help="plate id letter, e.g. K for K001.png")
    ap.add_argument("--count", type=int, help="expected number of plate FILES (optional; "
                    "completeness against the ORDER is check_plate_delivery's job -- EP78-80 "
                    "have legitimate id gaps from withdrawn plates, so contiguity is not checked)")
    ap.add_argument("--dst", help="default: remotion/public/<slug>/img")
    ap.add_argument("--resume", action="store_true",
                    help="skip plates already written at the target size and continue. "
                         "MEASURED 2026-08-25: an EP82 run died at plate 56 of 183 with "
                         "`cuDNN error: CUDNN_STATUS_EXECUTION_FAILED` while another process "
                         "held 14 GB of VRAM, and without this the only way back was to throw "
                         "away 56 good plates and start again.")
    ap.add_argument("--only", help="comma ids (K102,K134) to add into an EXISTING destination. "
                    "Regenerated plates arrive after the first pass, and refusing a non-empty "
                    "destination would otherwise force a full re-upscale of the whole episode. "
                    "Still never overwrites: an id already present in the destination is an error.")
    a = ap.parse_args()

    src = Path(a.src)
    dst = Path(a.dst) if a.dst else ROOT / "remotion" / "public" / a.slug / "img"
    if not MODEL.exists():
        print(f"FAIL: model not found: {MODEL}")
        return 2
    pat = re.compile(rf"^{re.escape(a.prefix)}\d{{3}}\.png$")
    all_pngs = sorted(src.glob("*.png"))
    sources = [p for p in all_pngs if pat.match(p.name)]
    unexpected = [p.name for p in all_pngs if not pat.match(p.name)]
    if unexpected:
        print(f"FAIL: files outside the {a.prefix}NNN.png pattern: {unexpected[:10]}")
        return 2
    if not sources:
        print(f"FAIL: no {a.prefix}NNN.png plates in {src}")
        return 2
    if a.count is not None and len(sources) != a.count:
        print(f"FAIL: {len(sources)} plate file(s), expected {a.count}")
        return 2

    only = [s.strip() for s in a.only.split(",")] if a.only else None
    if only:
        want = {f"{i}.png" for i in only}
        sources = [p for p in sources if p.name in want]
        missing = sorted(want - {p.name for p in sources})
        if missing:
            print(f"FAIL: --only ids not delivered: {missing}")
            return 2
        clash = sorted(p.name for p in sources if (dst / p.name).exists())
        if clash:
            print(f"FAIL: --only would overwrite existing 4K plate(s): {clash}")
            return 2
    if dst.exists() and any(dst.glob("*.png")) and not (a.only or a.resume):
        print(f"FAIL: destination is not empty; refusing overwrite: {dst}")
        return 2

    if a.resume:
        done = set()
        for p in sources:
            q = dst / p.name
            if q.is_file():
                try:
                    with Image.open(q) as im:
                        if im.size == TARGET:
                            done.add(p.name)
                except Exception:
                    pass
        if done:
            print(f"[resume] {len(done)} plate(s) already at {TARGET[0]}x{TARGET[1]}; "
                  f"{len(sources) - len(done)} to go")
        sources = [p for p in sources if p.name not in done]
        if not sources:
            print("[resume] nothing left to do")
            return 0

    device = "cuda" if torch.cuda.is_available() else "cpu"
    if device == "cpu":
        print("FAIL: no CUDA. Use the stable-diffusion-webui venv Python.")
        return 2
    model = ModelLoader().load_from_file(MODEL).eval().to(device)
    print(f"model {MODEL.name} scale=x{model.scale} on {device}  {a.slug}: {len(sources)} plate(s)")

    dst.mkdir(parents=True, exist_ok=True)
    started = time.time()
    global TILE
    failed: list[str] = []
    for index, source in enumerate(sources, 1):
        image = Image.open(source)
        # A CUDA/cuDNN failure on one plate must not throw away the run. Free the cache,
        # halve the tile, try once more, and if it still fails record it and keep going --
        # a run that dies at plate 56 of 183 costs the whole pass (measured 2026-08-25).
        large = None
        for attempt in (1, 2):
            try:
                large = upscale(model, image, device)
                break
            except RuntimeError as e:
                torch.cuda.empty_cache()
                if attempt == 1:
                    TILE = max(128, TILE // 2)
                    print(f"  !! {source.name}: {type(e).__name__}: {str(e)[:70]} -- "
                          f"retrying at tile {TILE}")
                else:
                    print(f"  !! {source.name}: FAILED TWICE, skipping")
                    failed.append(source.name)
        if large is None:
            continue
        final = large.resize(TARGET, Image.Resampling.LANCZOS)
        final.save(dst / source.name, "PNG", optimize=False)
        print(f"[{index}/{len(sources)}] {source.name} {image.width}x{image.height} -> "
              f"{final.width}x{final.height} ({time.time() - started:.0f}s elapsed)")

    bad = []
    for path in sorted(dst.glob("*.png")):
        with Image.open(path) as image:
            if image.size != TARGET or image.mode != "RGB":
                bad.append({"file": path.name, "size": image.size, "mode": image.mode})
    print(f"done in {time.time() - started:.0f}s -> {dst}")
    print(f"technical failures: {len(bad)} {bad[:5]}")
    if failed:
        print(f"GPU failures (not written, re-run with --resume): {len(failed)} {failed[:10]}")
    return 1 if (bad or failed) else 0


if __name__ == "__main__":
    raise SystemExit(main())
