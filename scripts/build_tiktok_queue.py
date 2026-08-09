#!/usr/bin/env python3
"""Build the TikTok upload queue: video, caption and cover for each Short.

The cover is the point. Left to itself TikTok picks a frame, and this channel's Shorts open on a
near-black frame - measured on the live profile on 2026-08-09, the grid was 100 identical black
tiles with unreadable subtitle text on them. A cover cannot be changed once a post exists (every
edit control on a posted or scheduled item is disabled), so it has to be attached here.

The caption is derived from the same design the YouTube copy comes from, so the two platforms say
the same thing about the same Short and neither drifts.

Usage:
  py -3.11 scripts/build_tiktok_queue.py --shorts 33-37,130 --out C:/temp/studio_auto/tt_queue.json
  py -3.11 scripts/build_tiktok_queue.py --all --out C:/temp/studio_auto/tt_queue_all.json
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESIGNS = ROOT / "episodes" / "_planning" / "short_designs"
OUT = ROOT / "remotion" / "out"
YT_HANDLE = "@primedocumentarystudio"
CAPTION_CAP = 150          # keep the hook visible before TikTok's "more" fold


def camel(slug: str) -> str:
    return "".join(p.capitalize() for p in re.split(r"[-_ ]+", slug) if p)



def from_short_data(n: int) -> tuple[str, str]:
    """Opening narration and episode slug, read out of the Short's own source files."""
    data = ROOT / "remotion" / "src" / "data" / f"short{n}.ts"
    timing = ROOT / "remotion" / "src" / "data" / f"short{n}_timing.ts"
    if not data.exists() or not timing.exists():
        return "", ""
    m = re.search(r"PD-\d{4}-\d{3}-([a-z0-9]+)", data.read_text(encoding="utf-8"))
    slug = m.group(1) if m else ""
    words = re.findall(r'"word":\s*"([^"]+)"', timing.read_text(encoding="utf-8"))
    if not words:
        return "", slug
    text = " ".join(words)
    # stop at the end of the second sentence: the hook, not the whole script
    parts = re.split(r"(?<=[.?!])\s+", text)
    return " ".join(parts[:2]).strip(), slug


def parse_range(spec: str) -> list[int]:
    out: list[int] = []
    for part in spec.split(","):
        part = part.strip()
        if "-" in part:
            a, b = part.split("-")
            out += list(range(int(a), int(b) + 1))
        elif part:
            out.append(int(part))
    return out


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--shorts")
    g.add_argument("--all", action="store_true", help="every Short with a TikTok render")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    sys.path.insert(0, str(ROOT / "scripts"))
    sys.path.insert(0, str(ROOT / "src"))
    import schedule_short_youtube
    yt_config = schedule_short_youtube.CONFIG

    designs: dict[int, tuple[dict, dict]] = {}
    for f in sorted(DESIGNS.glob("*.json")):
        d = json.loads(f.read_text(encoding="utf-8"))
        for s in d.get("shorts", []):
            designs[int(re.sub(r"\D", "", s["short_id"]))] = (d, s)

    if a.all:
        want = sorted(int(re.match(r"short(\d+)_tt", p.stem).group(1))
                      for p in OUT.glob("short*_tt.mp4"))
    else:
        want = parse_range(a.shorts)

    queue, problems = [], []
    for n in want:
        video = OUT / f"short{n}_tt.mp4"
        cover = OUT / f"short{n}_ttcover.png"
        if not video.exists():
            problems.append(f"short{n}: no TikTok render")
            continue
        if not cover.exists():
            problems.append(f"short{n}: no cover - render ShortThumb-short{n} with layout=tt")
            continue
        d, s = designs.get(n, (None, None))
        if s is not None:
            slug = d["episode_id"].split("-", 3)[3]
            angle = " ".join((s.get("angle") or "").split())
        else:
            # The early Shorts pre-date the design files. Their copy still exists - it is what the
            # YouTube upload used - so fall back to that rather than dropping 28 finished videos.
            cfg = yt_config.get(str(n).zfill(2)) or yt_config.get(str(n))
            if cfg:
                slug = cfg["ep"].split("-", 3)[3]
                angle = re.sub(r"\s*#Shorts\s*$", "", cfg["title"]).strip()
            else:
                # Last resort for the oldest Shorts, which have neither a design nor a YouTube
                # CONFIG entry: their own spoken opening. It is the hook the video actually leads
                # with, so it is the right thing to put in front of a TikTok viewer anyway.
                angle, slug = from_short_data(n)
                if not angle:
                    problems.append(f"short{n}: no design, no CONFIG and no narration to read")
                    continue
        if len(angle) > CAPTION_CAP:
            angle = angle[:CAPTION_CAP].rsplit(" ", 1)[0]
        angle = angle.rstrip(" .,;:")      # the angle usually already ends in a full stop
        caption = (f"{angle}.\nFull case on YouTube: {YT_HANDLE}\n"
                   # The episode slug is a name invented for our own files - #Tyler, #Hinders -
                   # and nobody browses it. Carry the post on tags people actually follow instead.
                   f"#truecrime #lawtok #documentary #truestory")
        queue.append({"short": n, "file": str(video).replace("\\", "/"),
                      "caption": caption, "cover": str(cover).replace("\\", "/")})

    Path(a.out).write_text(json.dumps(queue, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(queue)} queued -> {a.out}")
    for p in problems[:12]:
        print("  " + p)
    if len(problems) > 12:
        print(f"  ... and {len(problems) - 12} more")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
