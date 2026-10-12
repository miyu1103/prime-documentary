#!/usr/bin/env python3
"""Find shelf images that will not survive being put on screen: truncated, unreadable, or blank.

WHY THIS EXISTS
---------------
The 68-theme eye review (2026-09-04/05) found tiles that were visibly broken -- a colour-bar
glitch across a Daimler photo in `night_road_lamp`, another in `atmosphere_symbolic`, and four
department-store trademark PNGs in `retail_commerce` that render as solid black -- all of them
marked usable, because no check had ever opened the files. A truncated JPEG decodes to garbage
from the break downward; a transparent-only PNG composites as a black rectangle; both read as
defects in a finished film.

This opens every usable image on the shelf and records three cheap facts:

  decode   does PIL parse and fully decode the bytes (truncation surfaces here)
  luma     mean brightness of a 64px thumbnail -- near-0 is a black tile, near-255 blank white
  alpha    for PNGs: share of fully transparent pixels (a logo cut-out composites as black)

Videos are NOT checked. Probing 31k containers means 31k ffprobe processes; the header says
nothing about mid-file corruption, and a decode pass is hours of CPU alongside live renders.
Saying so beats a check that pretends. Output: runs/image_integrity.v001.jsonl (defects only)
and a summary; findings feed build_asset_usability on its next rebuild.

    py -3.11 scripts/check_image_integrity.py            # full sweep (~85k images)
    py -3.11 scripts/check_image_integrity.py --limit 500
"""
from __future__ import annotations

import argparse
import collections
import json
import sys
from pathlib import Path

from PIL import Image, ImageFile

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "runs" / "asset_usability.v001.jsonl"
OUT = ROOT / "runs" / "image_integrity.v001.jsonl"

# Refuse to paper over truncation: with this False (the default), a cut-off file raises
# instead of silently rendering the part that survived.
ImageFile.LOAD_TRUNCATED_IMAGES = False


def inspect(path: str) -> dict | None:
    """One image in, a defect record out -- or None when the file is fine."""
    try:
        with Image.open(path) as im:
            im.load()  # verify() misses truncation in many codecs; a full decode does not
            small = im.convert("RGBA").resize((64, 64))
    except Exception as exc:
        return {"defect": "unreadable", "detail": str(exc)[:120]}
    px = list(small.getdata())
    n = len(px)
    transparent = sum(1 for p in px if p[3] < 8) / n
    opaque = [p for p in px if p[3] >= 8]
    if not opaque:
        return {"defect": "fully_transparent", "detail": "every pixel has alpha 0"}
    luma = sum(0.299 * p[0] + 0.587 * p[1] + 0.114 * p[2] for p in opaque) / len(opaque)
    if transparent > 0.6:
        return {"defect": "mostly_transparent",
                "detail": f"{transparent:.0%} of pixels transparent; composites as black"}
    if luma < 8:
        return {"defect": "near_black", "detail": f"mean luma {luma:.1f}"}
    if luma > 247:
        return {"defect": "near_white", "detail": f"mean luma {luma:.1f}"}
    return None


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()
    if not RECORD.exists():
        sys.exit("run build_asset_usability.py first")

    rows = []
    for line in RECORD.open(encoding="utf-8"):
        r = json.loads(line)
        if r["kind"] == "image" and r["rights"] == "clear":
            rows.append(r)
    if args.limit:
        rows = rows[:args.limit]
    print(f"{len(rows)} usable images to open")

    tally: collections.Counter = collections.Counter()
    checked = 0
    with OUT.open("w", encoding="utf-8", newline="\n") as fh:
        for r in rows:
            checked += 1
            d = inspect(r["path"])
            if d:
                tally[d["defect"]] += 1
                fh.write(json.dumps({"path": r["path"], "theme": r.get("theme"),
                                     "source": r.get("source"), "title": r.get("title"),
                                     **d}, ensure_ascii=False) + "\n")
            if checked % 10000 == 0:
                print(f"  {checked}/{len(rows)}  defects so far: {sum(tally.values())}")

    print(f"\n{checked} opened, {sum(tally.values())} defect(s):")
    for k, v in tally.most_common():
        print(f"  {v:6d}  {k}")
    print(f"wrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
