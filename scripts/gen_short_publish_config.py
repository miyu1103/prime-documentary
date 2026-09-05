#!/usr/bin/env python3
"""Generate publishing CONFIG entries for every rendered Short that has none.

A Short cannot be scheduled at all without an entry in schedule_short_youtube.py's CONFIG: title,
description, tags, the funnel destination, and the sha256 of the exact approved bytes. 82 finished
Shorts were sitting unschedulable - everything rendered, nothing packaged.

Everything needed is already in the design. The title is the Short's angle, trimmed on a word
boundary; the description is that angle, then the question the Short deliberately leaves for the
long-form, then the standing channel line and hashtags built from the episode slug. Hand-writing
this for 82 Shorts would be slow and would drift; deriving it keeps the copy tied to the design
that was verified.

Every string goes through json.dumps. Building one by hand with "\n" inside an f-string wrote a
real newline into the middle of a Python string literal and broke the module once already.

Usage:
  py -3.11 scripts/gen_short_publish_config.py --shorts 104-202 --dry-run
  py -3.11 scripts/gen_short_publish_config.py --shorts 104-202 --apply
"""
from __future__ import annotations

import argparse
import hashlib
import json
import py_compile
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "schedule_short_youtube.py"
DESIGNS = ROOT / "episodes" / "_planning" / "short_designs"
OUT = ROOT / "remotion" / "out"

BOILER = ("Prime Documentary covers the cases that quietly decide what the state may do to you. "
          "The full episode is linked at the top.")
TITLE_CAP = 92          # YouTube truncates around 100; " #Shorts" is appended after this


def sha(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


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


# Words a title must not end on. Trimming on a word boundary is not enough: the first pass ended
# short110 at "...folded in before it reached the", which reads as a sentence someone forgot to
# finish rather than as a title.
DANGLING = {"a", "an", "the", "and", "or", "but", "of", "in", "on", "at", "to", "for", "with",
            "from", "by", "as", "that", "which", "who", "before", "after", "into", "over",
            "under", "is", "was", "were", "be", "been", "his", "her", "its", "their", "this"}


def trim_words(text: str, cap: int) -> str:
    """Trim on a word boundary, then off any word a title should not end on."""
    text = " ".join((text or "").split())
    out: list[str] = []
    if len(text) <= cap:
        out = text.split()
    else:
        for w in text.split():
            if len(" ".join(out + [w])) > cap:
                break
            out.append(w)
    while out and out[-1].strip(" .,;:").lower() in DANGLING:
        out.pop()
    return " ".join(out).rstrip(" .,;:")


def camel(slug: str) -> str:
    return "".join(p.capitalize() for p in re.split(r"[-_ ]+", slug) if p)


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--shorts", required=True)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    if not a.apply and not a.dry_run:
        ap.error("pass --apply or --dry-run")

    designs = {}
    for f in sorted(DESIGNS.glob("*.json")):
        d = json.loads(f.read_text(encoding="utf-8"))
        for s in d["shorts"]:
            designs[int(re.sub(r"\D", "", s["short_id"]))] = (d, s)

    text = SCRIPT.read_text(encoding="utf-8")
    blocks, skipped, problems = [], 0, []
    for n in parse_range(a.shorts):
        if f'    "{n}": {{' in text:
            skipped += 1
            continue
        d, s = designs.get(n, (None, None))
        if s is None:
            continue
        video, thumb = OUT / f"short{n}_yt_coverfirst.mp4", OUT / f"short{n}_thumb.png"
        if not video.exists() or not thumb.exists():
            problems.append(f"short{n}: not rendered yet")
            continue
        vid = (d.get("destination") or {}).get("video_id")
        if not vid:
            problems.append(f"short{n}: design has no destination video_id")
            continue

        slug = d["episode_id"].split("-", 3)[3]
        title = trim_words(s["angle"], TITLE_CAP)
        question = " ".join((s.get("funnel_question_left_for_longform") or "").split())
        tags = ["Shorts", camel(slug), "Law", "Documentary"]
        hashtags = f"#Shorts #{camel(slug)} #Law #Documentary"
        desc = f"{title}.\n\n{question}\n\n{BOILER}\n\n{hashtags}"

        blocks.append(
            f'    "{n}": {{\n'
            f"        # destination for the funnel link; ensure_funnel_description() verifies it "
            f"is public\n"
            f'        "longform": {json.dumps(vid)},\n'
            f'        "ep": {json.dumps(d["episode_id"])},\n'
            f'        "rev": "v001",\n'
            f'        "title": {json.dumps(title + " #Shorts")},\n'
            f'        "description": {json.dumps(desc)},\n'
            f'        "tags": {json.dumps(tags)},\n'
            f"        # v001: generated from the design by gen_short_publish_config.py\n"
            f'        "video_sha256": {json.dumps(sha(video))},\n'
            f'        "thumb_sha256": {json.dumps(sha(thumb))},\n'
            f"    }},\n")
        print(f"  short{n}: {title[:70]}")

    print(f"\n{len(blocks)} to add, {skipped} already present"
          + ("" if a.apply else "   (DRY RUN)"))
    for p in problems:
        print("  " + p)
    if not blocks or not a.apply:
        return 0

    anchor = text.rindex('": {\n        # destination for the funnel link')
    end = text.index("\n    },", anchor) + len("\n    },\n")
    SCRIPT.write_text(text[:end] + "".join(blocks) + text[end:], encoding="utf-8")
    py_compile.compile(str(SCRIPT), doraise=True)
    total = len(re.findall(r'^    "(\d+)": \{', SCRIPT.read_text(encoding="utf-8"), re.M))
    print(f"wrote {SCRIPT.relative_to(ROOT)} - {total} CONFIG entries, syntax checked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
