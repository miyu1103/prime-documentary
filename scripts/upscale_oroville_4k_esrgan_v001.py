#!/usr/bin/env python3
r"""Bring EP71 (PD-2026-071 "oroville") plates to the ordered 3840 long edge.

WHY THIS EXISTS, AND WHY IT IS NOT A REGENERATION
`runs/qc/oroville_plate_content_review_20260819.v001.md` read all ten contact sheets tile by
tile and found the CONTENT clean on all four ship-blocking classes: no identifiable person, no
resolved glyph, no inundation, no rights defect. The only defect is that 117 of 118 plates were
delivered at 1672x941 against an order that says 3840 twice, so `preflight_render_gate.py`
refuses the render. Regenerating a content-approved set to fix a pixel count would throw away
the one thing that passed -- and Codex's built-in generator is fixed at 1672x941, so it cannot
produce the size at all (owner report, 2026-08-20: O002 came back 1672x941 again).

WHAT THIS DOES
Real-ESRGAN x4plus on the GPU (1672x941 -> 6688x3764), then a LANCZOS downsample to exactly
3840x2160. Downsampling a model upscale recovers detail that a straight stretch cannot: the
existing `E:\pd-media\assets\ai\oroville_upscaled` is a plain 2x at 3344x1880, which is both
soft and still under the floor.

PRECEDENT: EP35 hinders shipped on `upscale_hinders_4k_lanczos_v001.py`, a CPU LANCZOS upscale
written for this exact floor. This is the same move with a better instrument, and
`PD_ONE_PASS_PRODUCTION_SPEC` row 5 permits it in terms: "long edge >= 3840 px (upscale +
denoise + brand LUT grade if the raw gen is smaller)".

HONEST LIMIT: an upscale of a 1672 source is not a native 3840 generation and will be softer
than EP70 wronghouse, whose 160 plates were generated at 3840x2160. It clears the floor
honestly; it does not manufacture detail that was never captured.

NEVER overwrites the source directory. Writes to img_4k/; the parent swaps it in and re-binds
the plate review, because every verdict is bound to a sha256 that this changes.

    "C:/Users/aab15/stable-diffusion-webui/venv/Scripts/python.exe" \
        scripts/upscale_oroville_4k_esrgan_v001.py
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import torch
from PIL import Image
from spandrel import ModelLoader

ROOT = Path(__file__).resolve().parents[1]

# PARAMETERISED 2026-08-21 rather than cloned. The docstring said "clone it per episode"; a third
# copy of a tiled-inference loop is a third place for the tile overlap to drift, and invariant 14
# bars a second implementation of an existing capability. The defaults below are EP71 oroville
# EXACTLY as before, so running this with no arguments does what it always did.
#   py -3.11 scripts/upscale_oroville_4k_esrgan_v001.py                       # EP71, unchanged
#   <venv> scripts/upscale_oroville_4k_esrgan_v001.py --slug lahaina \
#          --src E:/pd-media/assets/ai/lahaina --dst remotion/public/lahaina/img
_ap = __import__("argparse").ArgumentParser()
_ap.add_argument("--slug", default="oroville")
_ap.add_argument("--src", help="source dir of delivered plates")
_ap.add_argument("--dst", help="destination dir for the 3840 output")
_ap.add_argument("--skip-wrong-aspect", action="store_true",
                 help="skip plates that are not 16:9 instead of squashing them into 3840x2160. "
                      "A 2.25:1 plate resized to 16:9 is a crop nobody chose")
_A = _ap.parse_args()

SRC = Path(_A.src) if _A.src else ROOT / "remotion" / "public" / _A.slug / "img"
DST = Path(_A.dst) if _A.dst else ROOT / "remotion" / "public" / _A.slug / "img_4k"
MODEL = Path(r"C:\Users\aab15\stable-diffusion-webui\models\RealESRGAN\RealESRGAN_x4plus.pth")
TARGET = (3840, 2160)
TILE = 512
OVERLAP = 32


def base_pngs() -> list[Path]:
    out, skipped = [], []
    for p in sorted(SRC.glob("*.png")):
        if "_depth" in p.name or p.name.startswith("CONTACT_SHEET"):
            continue
        if _A.skip_wrong_aspect:
            w, h = Image.open(p).size
            if abs(w / h - 16 / 9) / (16 / 9) > 0.02:
                skipped.append((p.name, w, h))
                continue
        out.append(p)
    if skipped:
        print(f"[skip] {len(skipped)} plate(s) are not 16:9 and were NOT upscaled -- "
              f"squashing them into 3840x2160 would be a crop nobody chose. Regenerate these:")
        for n, w, h in skipped:
            print(f"       {n}  {w}x{h} = {w / h:.3f}:1")
    return out


def upscale(model, im: Image.Image, dev: str) -> Image.Image:
    """Tiled x4 inference. Tiling keeps VRAM flat and is why this can run beside nothing else."""
    x = torch.from_numpy(
        __import__("numpy").asarray(im.convert("RGB"), dtype="float32") / 255.0
    ).permute(2, 0, 1).unsqueeze(0).to(dev)
    _, _, h, w = x.shape
    scale = model.scale
    out = torch.zeros((1, 3, h * scale, w * scale), device=dev)
    weight = torch.zeros_like(out)
    for top in range(0, h, TILE - OVERLAP):
        for left in range(0, w, TILE - OVERLAP):
            bot, right = min(top + TILE, h), min(left + TILE, w)
            tile = x[:, :, top:bot, left:right]
            with torch.no_grad():
                res = model(tile)
            out[:, :, top * scale:bot * scale, left * scale:right * scale] += res
            weight[:, :, top * scale:bot * scale, left * scale:right * scale] += 1.0
    out = (out / weight).clamp(0, 1)
    arr = (out[0].permute(1, 2, 0).cpu().numpy() * 255.0).round().astype("uint8")
    return Image.fromarray(arr)


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    if not MODEL.exists():
        print(f"FAIL: model not found: {MODEL}")
        return 2
    srcs = base_pngs()
    todo = [p for p in srcs if max(Image.open(p).size) < TARGET[0]]
    print(f"{len(srcs)} plates in {SRC.name}; {len(todo)} below {TARGET[0]} long edge")
    if not todo:
        print("nothing to do")
        return 0

    dev = "cuda" if torch.cuda.is_available() else "cpu"
    if dev == "cpu":
        print("FAIL: no CUDA. Run with the webui venv python, which has torch+cu121.")
        return 2
    model = ModelLoader().load_from_file(MODEL).eval().to(dev)
    print(f"model {MODEL.name} scale=x{model.scale} on {dev}")

    DST.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    for i, p in enumerate(todo, 1):
        dst = DST / p.name
        if dst.exists() and max(Image.open(dst).size) >= TARGET[0]:
            print(f"[{i}/{len(todo)}] {p.name} already done")
            continue
        im = Image.open(p)
        big = upscale(model, im, dev)
        final = big.resize(TARGET, Image.LANCZOS)
        final.save(dst, "PNG", optimize=False)
        print(f"[{i}/{len(todo)}] {p.name} {im.size[0]}x{im.size[1]} -> "
              f"{big.size[0]}x{big.size[1]} -> {final.size[0]}x{final.size[1]}  "
              f"({time.time() - t0:.0f}s elapsed)")

    # copy through anything already at size so img_4k is a COMPLETE set, not a patch
    for p in srcs:
        if not (DST / p.name).exists():
            Image.open(p).save(DST / p.name, "PNG")
            print(f"carried through at native size: {p.name}")

    bad = [p.name for p in DST.glob("*.png") if max(Image.open(p).size) < TARGET[0]]
    print(f"\ndone in {time.time() - t0:.0f}s -> {DST}")
    print(f"under {TARGET[0]} after the pass: {len(bad)} {bad[:5]}")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
