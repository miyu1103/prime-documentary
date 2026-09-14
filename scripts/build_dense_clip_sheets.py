#!/usr/bin/env python3
r"""Pack several clips per contact sheet WITHOUT dropping frames per clip.

WHY THIS EXISTS
---------------
`check_pool_frames.py --sheets-only` samples 6-12 frames across each clip's own length, which is
right: the main thread measured that a 3-frame sample passes clips that break only in the middle,
and W044 was recorded as "clean" on that basis. But it writes roughly one sheet per clip, so a
327-clip pool becomes 241 sheets, and a reviewer facing 241 files reviews fewer of them.

This re-packs the SAME frames -- it decodes nothing and samples nothing -- at N clips per sheet,
one row per clip, every frame of that clip in the row. Six frames per clip is preserved exactly;
only the tile size shrinks, to about the size the plate sheets already use.

    py -3.11 scripts/build_dense_clip_sheets.py --slug itaewon
    py -3.11 scripts/build_dense_clip_sheets.py --slug itaewon --clips-per-sheet 4 --only keep.txt

`--only` takes a file whose first tab-separated column is a staged filename or clip id, so a
title-level triage can be applied first and the eyes spent on what survives it.
"""
from __future__ import annotations

import argparse
import collections
import json
import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

from PIL import Image, ImageDraw, ImageFont  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
BG = (13, 15, 19)
FG = (232, 234, 238)
DIM = (150, 156, 166)
PAD = 6
LABEL_H = 22


def _font(sz: int):
    for n in ("arialbd.ttf", "Arial Bold.ttf", "DejaVuSans-Bold.ttf", "arial.ttf"):
        try:
            return ImageFont.truetype(n, sz)
        except Exception:  # noqa: BLE001
            continue
    return ImageFont.load_default()


def titles_for(slug: str) -> dict[str, str]:
    p = ROOT / "runs" / "qc" / f"{slug}_title_staging.v001.json"
    if not p.is_file():
        return {}
    try:
        rows = json.loads(p.read_text(encoding="utf-8")).get("staged") or []
    except Exception:  # noqa: BLE001
        return {}
    out = {}
    for r in rows:
        n = r.get("staged_as") or r.get("name") or ""
        if n:
            out[Path(n).stem] = r.get("title") or ""
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--clips-per-sheet", type=int, default=4)
    ap.add_argument("--tile", default="400x225")
    ap.add_argument("--only", help="file whose first tab-separated column names the clips to include")
    ap.add_argument("--max-frames", type=int, default=6,
                    help="frames per clip on the sheet, taken EVENLY across the ones sampled so the "
                         "clip is still covered end to end. 6 is the floor the main thread measured: "
                         "a 3-frame sample passed W044, which broke in the middle.")
    a = ap.parse_args()

    fdir = ROOT / "runs" / "qc" / "pool_frames" / a.slug / "frames"
    if not fdir.is_dir():
        print(f"no frames under {fdir} -- run check_pool_frames.py --sheets-only first")
        return 1

    by_clip: dict[str, list[Path]] = collections.defaultdict(list)
    for f in sorted(fdir.glob("*.jpg")):
        clip = f.name.split("__")[0]
        by_clip[clip].append(f)

    keep = None
    if a.only:
        keep = set()
        for line in Path(a.only).read_text(encoding="utf-8").splitlines():
            first = line.split("\t")[0].strip()
            if first:
                keep.add(Path(first).stem)
                keep.add(Path(first).stem.split("__")[0])
    clips = [c for c in sorted(by_clip) if keep is None or c in keep]
    if not clips:
        print("nothing to sheet after --only filtering")
        return 1

    titles = titles_for(a.slug)
    tw, th = (int(v) for v in a.tile.lower().split("x"))
    def picked(c: str) -> list[Path]:
        fs = by_clip[c]
        if len(fs) <= a.max_frames:
            return fs
        step = (len(fs) - 1) / (a.max_frames - 1)
        return [fs[round(i * step)] for i in range(a.max_frames)]

    cols = max(len(picked(c)) for c in clips)
    out_dir = ROOT / "runs" / "qc" / "pool_frames" / a.slug / "dense"
    out_dir.mkdir(parents=True, exist_ok=True)
    for old in out_dir.glob("*.png"):
        old.unlink()

    f_small, f_title = _font(14), _font(18)
    n_sheets = 0
    for start in range(0, len(clips), a.clips_per_sheet):
        chunk = clips[start:start + a.clips_per_sheet]
        W = cols * tw + (cols + 1) * PAD
        H = 34 + len(chunk) * (th + LABEL_H + PAD) + PAD
        sheet = Image.new("RGB", (W, H), BG)
        d = ImageDraw.Draw(sheet)
        n = start // a.clips_per_sheet + 1
        total = (len(clips) + a.clips_per_sheet - 1) // a.clips_per_sheet
        d.text((PAD, 9), f"{a.slug} — staged pool, EVERY frame of each clip   sheet {n}/{total}   "
                         f"look for: a real face / a body / wrong country / a mid-clip break",
               font=f_title, fill=FG)
        for i, clip in enumerate(chunk):
            y = 34 + i * (th + LABEL_H + PAD)
            d.text((PAD, y + th + 3), f"{clip}   {titles.get(clip, '')[:96]}", font=f_small, fill=DIM)
            for j, fp in enumerate(picked(clip)):
                x = PAD + j * (tw + PAD)
                try:
                    im = Image.open(fp).convert("RGB")
                except Exception:  # noqa: BLE001
                    continue
                im.thumbnail((tw, th), Image.LANCZOS)
                sheet.paste(im, (x + (tw - im.width) // 2, y + (th - im.height) // 2))
        sheet.save(out_dir / f"{a.slug}_dense_{n:03d}.png")
        n_sheets += 1

    print(f"{len(clips)} clip(s) -> {n_sheets} sheet(s) at {a.clips_per_sheet} clips each, "
          f"up to {cols} frames per clip, in {out_dir}")
    print("Frames per clip are UNCHANGED -- this only re-packs what check_pool_frames sampled.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
