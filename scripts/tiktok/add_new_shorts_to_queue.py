#!/usr/bin/env python3
"""Add newly rendered Shorts to the TikTok posting source.

The queue builder reads one immutable source file (tt_queue.v1_captions.json) that was written
when the account was rebuilt. Shorts rendered after that - short271-282 for EP066-069 - exist on
disk with covers but appear nowhere in the posting order, so the poster would never reach them.

The opening line comes from the episode's own design file (`shorts[].lines[0]`), not from an
invented summary: the design is what the Short actually says. build_queue_v2.py then rewrites the
hashtags and the CTA the same way it does for every other row.

Refuses to add a Short whose video or cover is missing - a post without a cover can never be
given one afterwards.

Usage:
  py -3.11 scripts/tiktok/add_new_shorts_to_queue.py --check
  py -3.11 scripts/tiktok/add_new_shorts_to_queue.py --apply
"""
from __future__ import annotations

import argparse
import glob
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "remotion" / "out"
DESIGNS = ROOT / "episodes" / "_planning" / "short_designs"
SRC = Path("C:/temp/studio_auto/tt_queue.v1_captions.json")


def first_line(entry: dict) -> str:
    lines = entry.get("lines") or []
    for line in lines:
        text = line.get("text") if isinstance(line, dict) else line
        if text and str(text).strip():
            return str(text).strip()
    return ""


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    if not a.apply and not a.check:
        ap.error("pass --check or --apply")

    src = json.loads(SRC.read_text(encoding="utf-8"))
    have = {str(r["short"]).zfill(2) for r in src}

    found: list[dict] = []
    problems: list[str] = []
    for path in sorted(glob.glob(str(DESIGNS / "*.design.v001.json"))):
        design = json.loads(Path(path).read_text(encoding="utf-8"))
        for entry in design.get("shorts", []):
            sid = str(entry.get("short_id", "")).replace("short", "").zfill(2)
            if not sid or sid in have:
                continue
            video = OUT / f"short{sid}_tt.mp4"
            cover = OUT / f"short{sid}_ttcover.png"
            if not video.exists():
                continue
            if not cover.exists():
                problems.append(f"short{sid}: rendered but has NO COVER")
                continue
            hook = first_line(entry)
            if not hook:
                problems.append(f"short{sid}: design carries no usable opening line")
                continue
            found.append({"short": sid, "file": str(video).replace("\\", "/"),
                          "cover": str(cover).replace("\\", "/"),
                          "caption": hook, "risk": 0})

    found.sort(key=lambda r: int(r["short"]))
    print(f"source rows: {len(src)}   ready to add: {len(found)} -> {[r['short'] for r in found]}")
    for p in problems:
        print("  SKIPPED", p)
    if not found:
        return 0
    print("  first:", found[0]["caption"][:90])
    if a.check:
        print("(--check: nothing written)")
        return 0

    SRC.with_suffix(".bak.json").write_text(json.dumps(src, ensure_ascii=False, indent=1), encoding="utf-8")
    SRC.write_text(json.dumps(src + found, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"source is now {len(src) + len(found)} rows (previous kept as .bak.json)")
    print("next: py -3.11 scripts/tiktok/build_queue_v2.py   then copy tt_queue_v2.json over tt_queue.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
