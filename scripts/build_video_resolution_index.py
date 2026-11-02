#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Probe shelf video for real resolution and record it, because the ledger never did.

All 31,156 videos on the shelf have no width or height in their ledger row, so nothing
downstream can tell 4K from 320x240: not the search a shot spec is written from, not the
ship gate, not a contact sheet label. A stratified probe of 360 files found the split is
not uniform at all --

    nara   85% below 720p   (814 videos)
    ia     80% below 720p   (1,425 videos)
    every stock source       0%

-- so the archival half of the shelf, which is the half a documentary actually wants, is
also the half that will look soft next to a 1080p cut. An SD insert in a 1080p film is
visible to the viewer; it has to be a decision, not a surprise.

Probing every video would take hours, so this is resumable and defaults to the sources
that need it. Results go to a sidecar, not the ledgers, which live ingest lanes are
appending to.

    python scripts/build_video_resolution_index.py                 # nara, ia, noaa
    python scripts/build_video_resolution_index.py --source all
Output: E:\\pd-media\\assets\\archive\\_ledger\\video_resolution.json
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from shelf import LEDGER_DIR, shelf_rows  # noqa: E402

OUT = os.path.join(LEDGER_DIR, "video_resolution.json")
VIDEO_EXT = {".mp4", ".mov", ".webm", ".mkv", ".avi", ".mpeg", ".mpg", ".m4v"}
# The sources the sample showed are affected. Stock libraries were 0/40 SD in every case.
ARCHIVAL = ("nara", "ia", "noaa", "loc", "wikimedia", "smithsonian", "met")


def probe(path: str) -> tuple[int, int] | None:
    try:
        p = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "v:0",
             "-show_entries", "stream=width,height", "-of", "json", path],
            capture_output=True, text=True, timeout=60)
        st = json.loads(p.stdout)["streams"][0]
        return int(st["width"]), int(st["height"])
    except Exception:
        return None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--source", default=",".join(ARCHIVAL),
                    help="comma list, or 'all' (default: the archival sources)")
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    want = None if args.source == "all" else set(args.source.split(","))

    known: dict = {}
    if os.path.exists(OUT):
        with open(OUT, encoding="utf-8", errors="replace") as fh:
            known = json.load(fh)
        print(f"resuming with {len(known):,} already probed")

    todo = []
    for r in shelf_rows():
        fp = r.get("file_path", "") or ""
        if os.path.splitext(fp)[1].lower() not in VIDEO_EXT:
            continue
        if want and r.get("source") not in want:
            continue
        key = f"{r.get('source')}:{r.get('id')}"
        if key in known:
            continue
        todo.append((key, fp))
    print(f"{len(todo):,} to probe")

    done = failed = 0
    for key, fp in todo:
        if args.limit and done >= args.limit:
            break
        if not os.path.exists(fp):
            continue
        wh = probe(fp)
        if wh is None:
            failed += 1
            continue
        known[key] = {"w": wh[0], "h": wh[1]}
        done += 1
        if done % 200 == 0:
            with open(OUT, "w", encoding="utf-8") as fh:      # checkpoint
                json.dump(known, fh)
            print(f"  ... {done:,} probed, {failed} unreadable")

    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(known, fh)

    bands = {"4K+": 0, "1080p": 0, "720p": 0, "SD": 0}
    for v in known.values():
        h = v["h"]
        bands["4K+" if h >= 2160 else "1080p" if h >= 1080
              else "720p" if h >= 720 else "SD"] += 1
    print(f"\nprobed {done:,} this run ({failed} unreadable); index holds {len(known):,}")
    for b, n in bands.items():
        print(f"  {b:7} {n:6,}  {n/max(len(known),1)*100:5.1f}%")
    print(f"wrote {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
