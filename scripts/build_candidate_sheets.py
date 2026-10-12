#!/usr/bin/env python
"""Contact sheets for freshly fetched stock candidates, before anything is staged.

The point is the ORDER. EP83's pool sweep found the episode had no aviation footage at all;
twenty-five clips were then fetched and thirteen refused -- a Delta widget tail, the Lufthansa
crane, RYANAIR titles, FedEx, two United globes -- which would all have reached a render if the
clips had been staged first and reviewed later. Real subject footage carries real trade dress,
so the review has to happen on the candidates, not on the pool.

    py -3.11 scripts/build_candidate_sheets.py --ep PD-2026-084-threemile

Writes runs/qc/candidates/<ep>/sheet_NN.png, five clips per sheet, four frames per clip,
each row labelled with the asset id so a verdict can name it.
"""
from __future__ import annotations

import argparse
import glob
import subprocess
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[1]
MEDIA = Path("E:/pd-media/episodes")
PER_SHEET = 5
TILE_W = 520


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ep", required=True)
    ap.add_argument("--per-sheet", type=int, default=PER_SHEET)
    a = ap.parse_args()

    src = MEDIA / a.ep / "05_stock/candidates"
    clips = sorted(glob.glob(str(src / "*.mp4")))
    if not clips:
        print(f"no candidates under {src}", file=sys.stderr)
        return 1
    out = ROOT / "runs/qc/candidates" / a.ep
    out.mkdir(parents=True, exist_ok=True)
    strips = out / "_strips"
    strips.mkdir(exist_ok=True)

    from PIL import Image, ImageDraw

    made = []
    for c in clips:
        stem = Path(c).stem
        s = strips / f"{stem}.png"
        if not s.is_file():
            subprocess.run(
                ["ffmpeg", "-y", "-loglevel", "error", "-i", c,
                 "-vf", f"select='not(mod(n\\,37))',scale={TILE_W}:-1,tile=4x1",
                 "-frames:v", "1", str(s)],
                capture_output=True,
            )
        if s.is_file():
            made.append((stem, s))

    W = TILE_W * 4
    n = 0
    for page in range(0, len(made), a.per_sheet):
        chunk = made[page:page + a.per_sheet]
        imgs = [(name, Image.open(p).convert("RGB")) for name, p in chunk]
        H = sum(im.height + 24 for _, im in imgs)
        sheet = Image.new("RGB", (W, H), (12, 12, 14))
        d = ImageDraw.Draw(sheet)
        y = 0
        for name, im in imgs:
            d.text((8, y + 5), name, fill=(245, 220, 120))
            y += 24
            sheet.paste(im, (0, y))
            y += im.height
        n += 1
        sheet.save(out / f"sheet_{n:02d}.png")
    print(f"{len(made)} candidate(s) -> {n} sheet(s) in {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
