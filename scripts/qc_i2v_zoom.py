#!/usr/bin/env python
"""Native-resolution crop of one region, plate vs clip frames, for adjudicating a strip finding.

The strips answer "is something there". When the answer is "maybe", the region has to be looked
at without the 2x downscale the strip imposes. This crops the SAME normalised box out of the
4K plate and out of N frames of the clip, upsamples each to a common width, and stacks them so
the plate sits directly above the frames.

    py -3.11 scripts/qc_i2v_zoom.py --slug station --stem S086 --box 0.05,0.05,0.45,0.35
    py -3.11 scripts/qc_i2v_zoom.py --slug station --stem S086 --box 0.0,0.0,0.5,0.4 --frames 20,33,50,67,100

--box is x0,y0,x1,y1 as fractions of the frame. CPU only; no GPU, no encoding.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
OUT_W = 900


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--stem", required=True)
    ap.add_argument("--box", required=True, help="x0,y0,x1,y1 as 0..1 fractions")
    ap.add_argument("--frames", default="0,33,67,100")
    a = ap.parse_args()

    x0, y0, x1, y1 = (float(v) for v in a.box.split(","))
    idxs = [int(v) for v in a.frames.split(",") if v.strip()]

    img_dir = ROOT / "remotion" / "public" / a.slug / "img"
    plate = img_dir / f"{a.stem}.png"
    if not plate.is_file():
        plate = img_dir / "rejected" / f"{a.stem}.png"
    mp4 = ROOT / "remotion" / "public" / a.slug / "motion" / f"{a.stem}.mp4"

    tiles: list[tuple[str, Image.Image]] = []

    pim = Image.open(plate).convert("RGB")
    W, H = pim.size
    tiles.append(("PLATE", pim.crop((int(x0 * W), int(y0 * H), int(x1 * W), int(y1 * H)))))

    with tempfile.TemporaryDirectory() as tmp:
        tmpd = Path(tmp)
        expr = "+".join(f"eq(n\\,{i})" for i in idxs)
        subprocess.run(
            ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(mp4),
             "-vf", f"select='{expr}'", "-vsync", "0", "-frames:v", str(len(idxs)),
             str(tmpd / "f_%02d.png")],
            capture_output=True, timeout=300,
        )
        for k, i in enumerate(idxs, start=1):
            p = tmpd / f"f_{k:02d}.png"
            if not p.is_file():
                continue
            fim = Image.open(p).convert("RGB")
            W2, H2 = fim.size
            tiles.append((f"t frame {i}",
                          fim.crop((int(x0 * W2), int(y0 * H2), int(x1 * W2), int(y1 * H2)))))

    scaled = []
    for name, t in tiles:
        h = max(1, round(t.height * OUT_W / t.width))
        s = t.resize((OUT_W, h), Image.LANCZOS)
        d = ImageDraw.Draw(s)
        d.rectangle([0, 0, 10 + 11 * len(name) + 10 * len(a.stem), 30], fill=(0, 0, 0))
        d.text((6, 9), f"{a.stem} {name}", fill=(255, 255, 0))
        scaled.append(s)

    total_h = sum(s.height + 4 for s in scaled)
    sheet = Image.new("RGB", (OUT_W, total_h), (20, 20, 20))
    y = 0
    for s in scaled:
        sheet.paste(s, (0, y))
        y += s.height + 4

    out = ROOT / "runs" / "qc" / f"{a.slug}_i2v_vs_plate" / "_zoom" / f"{a.stem}.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out)
    print(f"[zoom] {out}  ({OUT_W}x{total_h}, {len(scaled)} tiles)")
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    raise SystemExit(main())
