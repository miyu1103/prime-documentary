#!/usr/bin/env python3
"""Create non-destructive shadow-lifted EP39 4K production stills.

The Codex originals intentionally use deep night exposure.  The PD visual gate
requires median luma >=45 for at least 60% of the delivery set, so this writes a
new immutable delivery variant with a restrained gamma curve.  Originals and
their existing depth maps remain untouched.
"""
from __future__ import annotations

import hashlib
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "remotion/public/frazier/img"
DEST = SOURCE / "selected"
GAMMA = 0.65
LIFT = 8


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def main() -> int:
    sources = sorted(p for p in SOURCE.glob("FRZ_*.png") if not p.name.endswith("_depth.png"))
    if len(sources) != 89:
        raise AssertionError(f"expected 89 reviewed FRZ stills, found {len(sources)}")
    DEST.mkdir(parents=True, exist_ok=True)
    lut = [round(LIFT + (255 - LIFT) * ((x / 255) ** GAMMA)) for x in range(256)]
    written = 0
    for src in sources:
        dst = DEST / ("FRZC_" + src.name.removeprefix("FRZ_"))
        if dst.exists():
            with Image.open(dst) as check:
                if check.size != (3840, 2160):
                    raise RuntimeError(f"existing corrected still has wrong dimensions: {dst}")
            continue
        with Image.open(src) as im:
            if im.size != (3840, 2160):
                raise RuntimeError(f"source still is not 4K: {src} {im.size}")
            rgb = im.convert("RGB").point(lut * 3)
            rgb.save(dst, format="PNG", optimize=False)
        written += 1
    outputs = sorted(DEST.glob("FRZC_*.png"))
    if len(outputs) != 89:
        raise AssertionError(f"expected 89 corrected stills, found {len(outputs)}")
    print(f"graded={len(outputs)} newly_written={written} gamma={GAMMA} lift={LIFT} dest={DEST}")
    print(f"sample_sha256={sha256(outputs[0])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
