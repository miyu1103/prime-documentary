#!/usr/bin/env python3
"""Remove the container metadata from every TikTok render, and prove it is gone.

Measured 2026-08-17: all 184 TikTok files carried `comment=Made with Remotion 4.0.476`. The
render script has always tried to strip it, but it wrote to "<name>.mp4.clean", ffmpeg could not
infer a format from that extension, the `&&` short-circuited the move, and the run still reported
failures=0. So the tag survived on every file, including the ones already posted.

That tag is what put a "creator labelled this AI-generated" badge on all 127 videos of the first
account. TikTok applies that label automatically from AI metadata and it cannot be removed after
posting.

Stream copy only - the video and audio are untouched, and a file whose tag is already gone is
skipped. Verifies each result by reading the tag back.

Usage:
  py -3.11 scripts/tiktok/strip_metadata.py --check
  py -3.11 scripts/tiktok/strip_metadata.py --apply
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parents[2] / "remotion" / "out"


def comment_of(path: Path) -> str:
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format_tags=comment",
                        "-of", "default=nw=1:nk=1", str(path)],
                       capture_output=True, text=True)
    return (r.stdout or "").strip()


def strip(path: Path) -> tuple[bool, str]:
    tmp = path.with_suffix(".clean.mp4")
    r = subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(path),
                        "-map_metadata", "-1", "-map_chapters", "-1", "-c", "copy",
                        "-movflags", "+faststart", "-f", "mp4", str(tmp)],
                       capture_output=True, text=True)
    if r.returncode != 0 or not tmp.exists():
        return False, (r.stderr or "ffmpeg failed")[:120]
    tmp.replace(path)
    left = comment_of(path)
    if "remotion" in left.lower():
        return False, f"tag survived: {left}"
    return True, ""


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    if not a.apply and not a.check:
        ap.error("pass --check or --apply")

    files = sorted(OUT.glob("short*_tt.mp4"))
    tagged = [f for f in files if comment_of(f)]
    print(f"tiktok renders: {len(files)}   carrying a container comment: {len(tagged)}")
    if not tagged:
        print("nothing to do")
        return 0
    if a.check:
        print("  e.g.", tagged[0].name, "->", comment_of(tagged[0]))
        print("(--check: nothing written)")
        return 0

    ok = 0
    for f in tagged:
        good, why = strip(f)
        if good:
            ok += 1
        else:
            print(f"  FAILED {f.name}: {why}")
    print(f"stripped and verified: {ok}/{len(tagged)}")
    left = [f for f in files if comment_of(f)]
    print(f"still carrying a comment: {len(left)}")
    return 0 if not left else 1


if __name__ == "__main__":
    raise SystemExit(main())
