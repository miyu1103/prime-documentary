#!/usr/bin/env python
"""One tall PLATE-over-FRAMES strip per i2v clip, at a width where a face still resolves.

Why not qc_i2v_tail_vs_plate.py: that tool packs 8 clips into a 1920x1080 sheet, so each cell
lands at 480x270 and shrinks again on the reader's side. A whole invented body survives that;
a face does not, and neither does a limb at the edge of frame. It also samples only the tail,
which misses a figure that walks in and out inside a 3.4 s clip.

This writes ONE image per clip: the source plate on top, then N frames sampled across the
clip's duration, stacked vertically at 960x540 each. Vertical stacking is deliberate -- a
horizontal row of the same cells costs the same pixels but hands the reader ~520px per frame,
below the width where facial features resolve.

    py -3.11 scripts/qc_i2v_strip_vs_plate.py --slug station
    py -3.11 scripts/qc_i2v_strip_vs_plate.py --slug station --only S042,S077
    py -3.11 scripts/qc_i2v_strip_vs_plate.py --slug station --samples 3

CPU only. It never touches the GPU: no hwaccel, no encoder, decode-and-scale of a 3 s clip.
Runs at below-normal priority so a long-form render keeps its cores.

Measures nothing. It is a tool for looking, and the looking is the whole check.
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import json
import os
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
CELL_W, CELL_H = 960, 540
MIN_OK_BYTES = 100_000


def probe_frames(mp4: Path) -> tuple[int, float]:
    """Return (nb_frames, duration_seconds). Falls back to counting if the header lies."""
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
         "stream=nb_frames,duration", "-of", "json", str(mp4)],
        capture_output=True, text=True, timeout=60,
    )
    n, dur = 0, 0.0
    try:
        st = json.loads(out.stdout)["streams"][0]
        n = int(st.get("nb_frames") or 0)
        dur = float(st.get("duration") or 0.0)
    except Exception:
        pass
    return n, dur


def extract(mp4: Path, idxs: list[int], dest_dir: Path, stem: str) -> dict[int, Path]:
    """Decode once, write the requested frame indices. Returns index -> png path."""
    expr = "+".join(f"eq(n\\,{i})" for i in idxs)
    pat = dest_dir / f"{stem}_%02d.png"
    subprocess.run(
        ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(mp4),
         "-vf", f"select='{expr}',scale={CELL_W}:{CELL_H}", "-vsync", "0",
         "-frames:v", str(len(idxs)), str(pat)],
        capture_output=True, timeout=300,
    )
    got: dict[int, Path] = {}
    for k, i in enumerate(idxs, start=1):
        p = dest_dir / f"{stem}_{k:02d}.png"
        if p.is_file() and p.stat().st_size > 0:
            got[i] = p
    return got


def label(img: Image.Image, text: str, warn: bool = False) -> None:
    d = ImageDraw.Draw(img)
    w = 12 + 11 * len(text)
    d.rectangle([0, 0, w, 34], fill=(0, 0, 0))
    d.text((7, 11), text, fill=(255, 80, 80) if warn else (255, 255, 0))


def build_one(slug: str, stem: str, samples: int, out_dir: Path, tmp_dir: Path) -> str:
    motion = ROOT / "remotion" / "public" / slug / "motion" / f"{stem}.mp4"
    img_dir = ROOT / "remotion" / "public" / slug / "img"
    plate = img_dir / f"{stem}.png"
    plate_note = ""
    if not plate.is_file():
        alt = img_dir / "rejected" / f"{stem}.png"
        if alt.is_file():
            plate, plate_note = alt, " [PLATE WAS REJECTED]"

    n, dur = probe_frames(motion)
    if n <= 1:
        return f"{stem}: FAILED probe"
    fps = (n / dur) if dur else 30.0
    # spread across the clip, always including the last decodable frame
    idxs = sorted({max(0, min(n - 1, round((k + 1) * (n - 1) / samples))) for k in range(samples)})
    frames = extract(motion, idxs, tmp_dir, stem)

    rows = 1 + len(idxs)
    sheet = Image.new("RGB", (CELL_W, CELL_H * rows), (20, 20, 20))

    pim = Image.open(plate).convert("RGB").resize((CELL_W, CELL_H), Image.LANCZOS)
    label(pim, f"{stem}  PLATE (source){plate_note}", warn=bool(plate_note))
    sheet.paste(pim, (0, 0))

    for r, i in enumerate(idxs, start=1):
        y = r * CELL_H
        p = frames.get(i)
        if p is None:
            d = ImageDraw.Draw(sheet)
            d.text((20, y + 20), f"{stem} frame {i} MISSING", fill=(255, 0, 0))
            continue
        fim = Image.open(p).convert("RGB")
        label(fim, f"{stem}  t={i / fps:0.2f}s  (frame {i}/{n - 1})")
        sheet.paste(fim, (0, y))

    sheet.save(out_dir / f"{stem}.png")
    for p in frames.values():
        try:
            p.unlink()
        except OSError:
            pass
    return f"{stem}: ok ({dur:0.2f}s, {n} frames){plate_note}"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--only", default=None)
    ap.add_argument("--samples", type=int, default=3, help="frames sampled from each clip")
    ap.add_argument("--workers", type=int, default=3, help="keep low; a render may be running")
    a = ap.parse_args()

    motion_dir = ROOT / "remotion" / "public" / a.slug / "motion"
    out_dir = ROOT / "runs" / "qc" / f"{a.slug}_i2v_vs_plate"
    out_dir.mkdir(parents=True, exist_ok=True)
    tmp_dir = out_dir / "_frames"
    tmp_dir.mkdir(exist_ok=True)

    stems = sorted(p.stem for p in motion_dir.glob("*.mp4")
                   if not p.stem.endswith("_depth") and p.stat().st_size > MIN_OK_BYTES)
    if a.only:
        want = {s.strip() for s in a.only.split(",") if s.strip()}
        stems = [s for s in stems if s in want]
    if not stems:
        print(f"[qc] {a.slug}: nothing to sheet")
        return 0

    try:  # yield to the render
        os.nice(10)  # type: ignore[attr-defined]
    except Exception:
        pass

    done = 0
    with cf.ThreadPoolExecutor(max_workers=a.workers) as ex:
        futs = {ex.submit(build_one, a.slug, s, a.samples, out_dir, tmp_dir): s for s in stems}
        for f in cf.as_completed(futs):
            done += 1
            msg = f.result()
            if "ok" not in msg or "REJECTED" in msg:
                print(f"[qc] {msg}")
            if done % 25 == 0:
                print(f"[qc] {done}/{len(stems)}")

    print(f"[qc] {a.slug}: {len(stems)} strip(s) in {out_dir}")
    print("[qc] each strip is PLATE on top, then the clip over time. A person, a face, a limb or")
    print("[qc] a moving figure present below but absent from the plate is an invented subject.")
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    raise SystemExit(main())
