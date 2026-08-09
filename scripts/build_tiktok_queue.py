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
            if not cfg:
                problems.append(f"short{n}: no design and no YouTube CONFIG entry")
                continue
            slug = cfg["ep"].split("-", 3)[3]
            angle = re.sub(r"\s*#Shorts\s*$", "", cfg["title"]).strip()
        if len(angle) > CAPTION_CAP:
            angle = angle[:CAPTION_CAP].rsplit(" ", 1)[0]
        angle = angle.rstrip(" .,;:")      # the angle usually already ends in a full stop
        caption = (f"{angle}.\nFull case on YouTube: {YT_HANDLE}\n"
                   f"#{camel(slug)} #Documentary #TrueStory #Law")
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
