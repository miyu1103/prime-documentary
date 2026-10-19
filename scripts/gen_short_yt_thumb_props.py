#!/usr/bin/env python3
"""Write ShortThumbYT props for any Short that has no 16:9 thumbnail yet.

A Short's custom thumbnail is what the channel page, search and suggested-video rails show. 40 of
the 74 uploaded Shorts had the *vertical* 1080x1920 cover set as that thumbnail: YouTube fits it
into a 16:9 box, so it renders as a narrow strip between two black bars with the large text cropped
away, and only the small centre line readable. Measured on the live channel 2026-08-10.

Everything needed is already in Root.tsx - the vertical cover declares the headline, the badge and
the hero plate for that Short - so this reuses them rather than inventing new copy that would drift
from the video.

Usage:
  py -3.11 scripts/gen_short_yt_thumb_props.py --missing --dry-run
  py -3.11 scripts/gen_short_yt_thumb_props.py --missing --apply
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RTX = ROOT / "remotion" / "src" / "Root.tsx"
PROPS = ROOT / "runs" / "shorts_thumbs" / "props"
SAMPLES = ROOT / "runs" / "shorts_thumbs" / "samples"
GOLD = "#E5B53A"


def covers() -> dict[str, dict]:
    """headline / badge / hero plate per Short, read from its vertical cover registration."""
    src = RTX.read_text(encoding="utf-8")
    out: dict[str, dict] = {}
    for m in re.finditer(r'id="ShortThumb-(short\d+)"(.{0,1200}?)/>', src, re.S):
        sid, blk = m.group(1), m.group(2)
        head = re.search(r"headline:\s*'(.*?)'", blk, re.S)
        badge = re.search(r"badge:\s*'([^']*)'", blk)
        bg = re.search(r"backgroundSrc:\s*'([^']+)'", blk)
        if not head or not bg:
            continue
        out[sid] = {
            # The TSX source carries the break as the two characters backslash-n; turn it into a
            # real newline so the JSON holds "A\nB" and the component breaks the line. Left alone
            # it renders the backslash on screen.
            "headline": (head.group(1)
                         .replace(chr(92) + "n", chr(10))
                         .replace(chr(92) + "N", chr(10))),
            "badge": badge.group(1) if badge else None,
            "heroImage": bg.group(1),
        }
    return out


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--missing", action="store_true", help="only Shorts with no rendered 16:9 yet")
    ap.add_argument("--shorts", help="explicit list, e.g. 52,53,86-99")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    if not a.apply and not a.dry_run:
        ap.error("pass --apply or --dry-run")

    cov = covers()
    have = {p.stem for p in SAMPLES.glob("short*.png")}
    if a.shorts:
        want = set()
        for part in a.shorts.split(","):
            if "-" in part:
                lo, hi = part.split("-")
                want |= {f"short{n}" for n in range(int(lo), int(hi) + 1)}
            elif part.strip():
                want.add(f"short{part.strip()}")
        targets = sorted(want & cov.keys())
    else:
        targets = sorted(cov.keys() - have)

    written, skipped = 0, []
    for sid in targets:
        c = cov[sid]
        props = {
            "headline": c["headline"],
            # Explicitly blank, not omitted. Remotion merges --props over defaultProps, so leaving
            # it out keeps the composition's example subhead - short99 rendered with
            # "THE GARDNER HEIST - 1990" under it, which is short20's case, not its own.
            "subhead": "",
            "heroImage": c["heroImage"],
            "accent": GOLD,
            "focusY": 26,
        }
        if c["badge"]:
            props["badge"] = c["badge"]
        if not (ROOT / "remotion" / "public" / c["heroImage"]).is_file():
            skipped.append(f"{sid}: hero plate missing ({c['heroImage']})")
            continue
        print(f"  {sid}: {c['headline'].replace(chr(10), ' / ')[:52]}")
        written += 1
        if a.apply:
            PROPS.mkdir(parents=True, exist_ok=True)
            (PROPS / f"{sid}.json").write_text(
                json.dumps(props, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"\n{written} props" + ("" if a.apply else "   (DRY RUN)"))
    for s in skipped[:8]:
        print("  " + s)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
