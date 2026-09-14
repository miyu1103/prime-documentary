#!/usr/bin/env python
"""Decode 8 real source frames spread across the young_film cut list into a contact sheet so the
orchestrator can eyeball that the cuts are REAL footage/stills (not stubs / black)."""
from __future__ import annotations
import json, subprocess, sys, tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
PUB = ROOT / "remotion" / "public"
FILM = json.loads((ROOT / "remotion/src/data/young_film.json").read_text(encoding="utf-8"))
OUT = ROOT / "runs" / "qc" / "young_realbuild_frames.png"
OUT.parent.mkdir(parents=True, exist_ok=True)

cuts = FILM["cuts"]
# 8 cuts spread evenly across the timeline; guarantee a mix of footage + stills
idxs = [round(i * (len(cuts) - 1) / 7) for i in range(8)]
picks = [cuts[i] for i in idxs]
# ensure at least 2 stills and 2 footage in the sample
if sum(1 for c in picks if c["kind"] == "img") == 0:
    picks[-1] = next(c for c in cuts if c["kind"] == "img")

CW, CH = 640, 360
cols, rows = 4, 2
pad, lab = 10, 46
sheet = Image.new("RGB", (cols * CW + (cols + 1) * pad, rows * (CH + lab) + (rows + 1) * pad), (18, 18, 22))
draw = ImageDraw.Draw(sheet)
try:
    font = ImageFont.truetype("arial.ttf", 15)
    fontb = ImageFont.truetype("arialbd.ttf", 16)
except Exception:
    font = fontb = ImageFont.load_default()

tmp = Path(tempfile.mkdtemp())
for n, c in enumerate(picks):
    src = PUB / c["src"]
    thumb = None
    if src.suffix.lower() in (".mp4", ".mov", ".webm"):
        fp = tmp / f"f{n}.png"
        subprocess.run(["ffmpeg", "-y", "-ss", "1.0", "-i", str(src), "-frames:v", "1",
                        "-vf", f"scale={CW}:{CH}:force_original_aspect_ratio=decrease,"
                               f"pad={CW}:{CH}:(ow-iw)/2:(oh-ih)/2", str(fp)],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if fp.is_file():
            thumb = Image.open(fp).convert("RGB")
    else:
        im = Image.open(src).convert("RGB")
        im.thumbnail((CW, CH))
        thumb = Image.new("RGB", (CW, CH), (0, 0, 0))
        thumb.paste(im, ((CW - im.width) // 2, (CH - im.height) // 2))
    if thumb is None:
        thumb = Image.new("RGB", (CW, CH), (60, 0, 0))
        ImageDraw.Draw(thumb).text((20, CH // 2), "DECODE FAILED", fill=(255, 120, 120), font=fontb)
    r, col = divmod(n, cols)
    x = pad + col * (CW + pad)
    y = pad + r * (CH + lab + pad)
    sheet.paste(thumb, (x, y))
    kind = "FACTORY (real motion)" if c["kind"] == "footage" else f"STILL ({c.get('treatment')})"
    name = Path(c["src"]).name
    draw.text((x + 4, y + CH + 4), f"cut {cuts.index(c):03d} @ {c['start']:.0f}s  [{c['act']}]  {kind}",
              fill=(240, 240, 245), font=fontb)
    draw.text((x + 4, y + CH + 24), name[:64], fill=(150, 200, 255), font=font)

sheet.save(OUT)
print("wrote", OUT)
print("sampled cuts:", [(cuts.index(c), c["kind"], Path(c["src"]).name) for c in picks])
