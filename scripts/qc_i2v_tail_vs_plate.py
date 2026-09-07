#!/usr/bin/env python
"""Contact sheets that put each i2v clip's LAST frame directly under its source plate.

Why the pairing and not just the tails: the failure this catches is the generator ADDING
something the plate never had -- a man in a suit on a blank concrete wall, a woman's face at a
kerbside, measured on EP61 weimer and again on EP77 keybridge, where 30 of 112 clips (27%)
grew people. A tail sheet alone shows a person and leaves the reviewer guessing whether the
plate had one. Side by side the question answers itself.

The last frame is used because Wan drifts away from its conditioning image over the clip: if
anything was invented, that is where it is largest.

    py -3.11 scripts/qc_i2v_tail_vs_plate.py --slug concordia
    py -3.11 scripts/qc_i2v_tail_vs_plate.py --slug concordia --only N094,N101

Writes runs/qc/<slug>_tail_vs_plate/sheet_NN.png (8 pairs each, plate above tail) plus an
index.txt naming every cell in order, so a finding can be turned into a stem without counting
tiles. This measures nothing on its own -- it is a tool for looking, and looking is the point.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
CELL_W, CELL_H = 480, 270
COLS, ROWS = 4, 2
PER_SHEET = COLS * ROWS
MIN_OK_BYTES = 100_000


def tail_frame(mp4: Path, dest: Path) -> bool:
    """Grab the frame 0.2 s before the end. Returns False if ffmpeg produced nothing."""
    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-sseof", "-0.2",
           "-i", str(mp4), "-vframes", "1", "-vf", f"scale={CELL_W}:{CELL_H}", str(dest)]
    try:
        subprocess.run(cmd, capture_output=True, timeout=60)
    except subprocess.TimeoutExpired:
        return False
    return dest.is_file() and dest.stat().st_size > 0


def label(img: Image.Image, text: str) -> None:
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 130, 18], fill=(0, 0, 0))
    d.text((4, 4), text, fill=(255, 255, 0))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--only", default=None, help="comma list of stems to sheet")
    a = ap.parse_args()

    motion = ROOT / "remotion" / "public" / a.slug / "motion"
    img_dir = ROOT / "remotion" / "public" / a.slug / "img"
    out_dir = ROOT / "runs" / "qc" / f"{a.slug}_tail_vs_plate"
    out_dir.mkdir(parents=True, exist_ok=True)

    stems = sorted(p.stem for p in motion.glob("*.mp4")
                   if not p.stem.endswith("_depth") and p.stat().st_size > MIN_OK_BYTES)
    if a.only:
        want = {s.strip() for s in a.only.split(",") if s.strip()}
        stems = [s for s in stems if s in want]
    if not stems:
        print(f"[qc] {a.slug}: no finished clips to sheet")
        return 0

    index = []
    with tempfile.TemporaryDirectory() as tmp:
        tmpd = Path(tmp)
        sheet_no = 0
        for start in range(0, len(stems), PER_SHEET):
            chunk = stems[start:start + PER_SHEET]
            sheet_no += 1
            sheet = Image.new("RGB", (CELL_W * COLS, CELL_H * 2 * ROWS), (24, 24, 24))
            for i, stem in enumerate(chunk):
                col, row = i % COLS, i // COLS
                x, y = col * CELL_W, row * CELL_H * 2

                plate = img_dir / f"{stem}.png"
                if plate.is_file():
                    pim = Image.open(plate).convert("RGB").resize((CELL_W, CELL_H))
                    label(pim, f"{stem} PLATE")
                    sheet.paste(pim, (x, y))

                tf = tmpd / f"{stem}.png"
                if tail_frame(motion / f"{stem}.mp4", tf):
                    tim = Image.open(tf).convert("RGB")
                    label(tim, f"{stem} TAIL")
                    sheet.paste(tim, (x, y + CELL_H))
                index.append(f"sheet_{sheet_no:02d} cell{i} {stem}")
            sheet.save(out_dir / f"sheet_{sheet_no:02d}.png")

    (out_dir / "index.txt").write_text("\n".join(index), encoding="utf-8")
    print(f"[qc] {a.slug}: {len(stems)} clip(s) -> {sheet_no} sheet(s) in {out_dir}")
    print("[qc] each cell is PLATE above TAIL. A subject in the tail that is absent from the")
    print("[qc] plate above it is an invented subject and the clip must be re-rolled.")
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    raise SystemExit(main())
