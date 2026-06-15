#!/usr/bin/env python3
"""Build 2x2 contact sheets from Midjourney variant sets in the SSD inbox.

For each stem, finds the 4 inbox files whose name contains the stem (Midjourney keeps the
prompt/stem in the filename), and tiles them into one labeled 2x2 PNG so Claude can compare
variants cheaply. Quadrants: top-left=first, top-right=second, bottom-left=third,
bottom-right=fourth (sorted by filename, i.e. variant _0.._3).

Usage:
    py -3.11 scripts/make_contact_sheets.py --stems s005_empty_chair s009_hand_writing
    py -3.11 scripts/make_contact_sheets.py --stems-file <file>   # one stem per line
Output: cache/montages/<stem>.png  (cache/ is gitignored)
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = REPO_ROOT / "cache" / "montages"
IMG_EXT = {".png", ".jpg", ".jpeg", ".webp"}


def media_root() -> Path:
    cfg = json.loads((REPO_ROOT / "config" / "storage.local.json").read_text(encoding="utf-8"))
    return Path(cfg["roots"]["media"]["path"])


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--inbox", default=None)
    ap.add_argument("--stems", nargs="*", default=[])
    ap.add_argument("--stems-file", default=None)
    ap.add_argument("--cell", default="640x360", help="per-image cell WxH")
    args = ap.parse_args(argv)

    stems = list(args.stems)
    if args.stems_file:
        stems += [l.strip() for l in Path(args.stems_file).read_text(encoding="utf-8").splitlines() if l.strip()]
    if not stems:
        print("no stems given"); return 2

    inbox = Path(args.inbox) if args.inbox else (media_root() / "downloads" / "inbox")
    files = [p for p in inbox.iterdir() if p.is_file() and p.suffix.lower() in IMG_EXT]
    cw, ch = (int(x) for x in args.cell.lower().split("x"))
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    font = "C\\:/Windows/Fonts/arial.ttf"
    for stem in stems:
        hits = sorted(p for p in files if stem in p.name)
        if not hits:
            print(f"[skip] {stem}: no files"); continue
        hits = hits[:4]
        while len(hits) < 4:
            hits.append(hits[-1])  # pad if fewer than 4
        labels = ["0", "1", "2", "3"]
        fc = []
        for i, _ in enumerate(hits):
            fc.append(
                f"[{i}:v]scale={cw}:{ch}:force_original_aspect_ratio=decrease,"
                f"pad={cw}:{ch}:(ow-iw)/2:(oh-ih)/2:color=black,"
                f"drawtext=fontfile='{font}':text='{labels[i]}':x=12:y=10:fontsize=44:"
                f"fontcolor=yellow:box=1:boxcolor=black@0.6:boxborderw=8[v{i}]"
            )
        fc.append("[v0][v1][v2][v3]xstack=inputs=4:layout=0_0|w0_0|0_h0|w0_h0[out]")
        out = OUT_DIR / f"{stem}.png"
        cmd = ["ffmpeg", "-y"]
        for p in hits:
            cmd += ["-i", str(p)]
        cmd += ["-filter_complex", ";".join(fc), "-map", "[out]", "-frames:v", "1", str(out)]
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0:
            print(f"[fail] {stem}: {r.stderr.strip().splitlines()[-1] if r.stderr else '?'}")
        else:
            print(f"[ok] {out.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
