#!/usr/bin/env python3
"""Upscale one six-image thumbnail candidate set to exact 3840x2160.

The source set is immutable. The destination must not exist or must be empty.
Real-ESRGAN x4plus performs the detail reconstruction, followed by one exact
LANCZOS resize to the delivery dimensions.
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import torch
from PIL import Image
from spandrel import ModelLoader


MODEL = Path(r"C:\Users\aab15\stable-diffusion-webui\models\RealESRGAN\RealESRGAN_x4plus.pth")
TARGET = (3840, 2160)
EXPECTED = {f"T{i:02d}.png" for i in range(1, 7)}
TILE = 512
OVERLAP = 32


def upscale(model, image: Image.Image, device: str) -> Image.Image:
    numpy = __import__("numpy")
    tensor = torch.from_numpy(
        numpy.asarray(image.convert("RGB"), dtype="float32") / 255.0
    ).permute(2, 0, 1).unsqueeze(0).to(device)
    _, _, height, width = tensor.shape
    scale = model.scale
    output = torch.zeros((1, 3, height * scale, width * scale), device=device)
    weight = torch.zeros_like(output)
    for top in range(0, height, TILE - OVERLAP):
        for left in range(0, width, TILE - OVERLAP):
            bottom = min(top + TILE, height)
            right = min(left + TILE, width)
            tile = tensor[:, :, top:bottom, left:right]
            with torch.no_grad():
                result = model(tile)
            output[:, :, top * scale:bottom * scale, left * scale:right * scale] += result
            weight[:, :, top * scale:bottom * scale, left * scale:right * scale] += 1.0
    output = (output / weight).clamp(0, 1)
    array = (output[0].permute(1, 2, 0).cpu().numpy() * 255.0).round().astype("uint8")
    return Image.fromarray(array)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--src", type=Path, required=True)
    parser.add_argument("--dst", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    args = parse_args()
    if not MODEL.is_file():
        print(f"FAIL model missing: {MODEL}")
        return 2
    if not args.src.is_dir():
        print(f"FAIL source missing: {args.src}")
        return 2
    found = {path.name for path in args.src.glob("T[0-9][0-9].png") if path.is_file()}
    if found != EXPECTED:
        print(f"FAIL source inventory missing={sorted(EXPECTED-found)} unexpected={sorted(found-EXPECTED)}")
        return 2
    if args.dst.exists() and any(args.dst.iterdir()):
        print(f"FAIL destination is not empty: {args.dst}")
        return 2
    if args.dst.resolve() == args.src.resolve():
        print("FAIL source and destination are identical")
        return 2
    device = "cuda" if torch.cuda.is_available() else "cpu"
    if device != "cuda":
        print("FAIL CUDA unavailable")
        return 2
    model = ModelLoader().load_from_file(MODEL).eval().to(device)
    args.dst.mkdir(parents=True, exist_ok=True)
    started = time.time()
    for index, name in enumerate(sorted(EXPECTED), 1):
        source = args.src / name
        destination = args.dst / name
        if destination.exists():
            print(f"FAIL collision: {destination}")
            return 2
        with Image.open(source) as original:
            raw_size = original.size
            large = upscale(model, original, device)
            final = large.resize(TARGET, Image.Resampling.LANCZOS)
            final.save(destination, "PNG", optimize=False)
        print(f"[{index}/6] {name} {raw_size[0]}x{raw_size[1]} -> {large.width}x{large.height} -> 3840x2160")
    failures = []
    for name in sorted(EXPECTED):
        with Image.open(args.dst / name) as image:
            if image.size != TARGET or image.mode != "RGB":
                failures.append((name, image.size, image.mode))
    print(f"DONE seconds={time.time()-started:.1f} failures={failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
