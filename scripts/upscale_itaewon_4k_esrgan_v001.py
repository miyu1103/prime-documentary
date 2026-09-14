#!/usr/bin/env python3
r"""Upscale EP74 Itaewon Codex plates to the required 3840x2160 render set.

Codex built-in image generation currently returns 1672x941 sources. This script
keeps those immutable in img_raw_codex_v001, applies Real-ESRGAN x4plus in tiles,
then reduces with LANCZOS to exactly 3840x2160. It never overwrites a source or
an existing destination plate.

    "C:/Users/aab15/stable-diffusion-webui/venv/Scripts/python.exe" \
        scripts/upscale_itaewon_4k_esrgan_v001.py
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import torch
from PIL import Image
from spandrel import ModelLoader

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "remotion" / "public" / "itaewon" / "img_raw_codex_v002"
DST = ROOT / "remotion" / "public" / "itaewon" / "img"
MODEL = Path(r"C:\Users\aab15\stable-diffusion-webui\models\RealESRGAN\RealESRGAN_x4plus.pth")
TARGET = (3840, 2160)
TILE = 512
OVERLAP = 32


def base_pngs() -> list[Path]:
    return [
        p
        for p in sorted(SRC.glob("I[0-9][0-9][0-9].png"))
        if p.is_file()
    ]


def upscale(model, image: Image.Image, device: str) -> Image.Image:
    x = torch.from_numpy(
        __import__("numpy").asarray(image.convert("RGB"), dtype="float32") / 255.0
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
    if not MODEL.exists():
        print(f"FAIL: model not found: {MODEL}")
        return 2
    sources = base_pngs()
    expected = {f"I{i:03d}.png" for i in range(1, 121)}
    found = {p.name for p in sources}
    missing = sorted(expected - found)
    unexpected = sorted(found - expected)
    if missing or unexpected:
        print(f"FAIL: source inventory missing={missing[:10]} unexpected={unexpected[:10]}")
        return 2
    if DST.exists() and any(DST.glob("*.png")):
        print(f"FAIL: destination is not empty; refusing overwrite: {DST}")
        return 2

    device = "cuda" if torch.cuda.is_available() else "cpu"
    if device == "cpu":
        print("FAIL: no CUDA. Use the stable-diffusion-webui venv Python.")
        return 2
    model = ModelLoader().load_from_file(MODEL).eval().to(device)
    print(f"model {MODEL.name} scale=x{model.scale} on {device}")

    DST.mkdir(parents=True, exist_ok=False)
    started = time.time()
    for index, source in enumerate(sources, 1):
        destination = DST / source.name
        image = Image.open(source)
        large = upscale(model, image, device)
        final = large.resize(TARGET, Image.Resampling.LANCZOS)
        final.save(destination, "PNG", optimize=False)
        print(
            f"[{index}/120] {source.name} {image.width}x{image.height} -> "
            f"{large.width}x{large.height} -> {final.width}x{final.height} "
            f"({time.time() - started:.0f}s elapsed)"
        )

    bad = []
    for path in sorted(DST.glob("I[0-9][0-9][0-9].png")):
        with Image.open(path) as image:
            if image.size != TARGET or image.mode != "RGB":
                bad.append({"file": path.name, "size": image.size, "mode": image.mode})
    print(f"done in {time.time() - started:.0f}s -> {DST}")
    print(f"technical failures: {len(bad)} {bad[:5]}")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
