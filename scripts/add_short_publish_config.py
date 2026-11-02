#!/usr/bin/env python3
"""Add publishing CONFIG entries for Shorts that have been rendered but never packaged.

schedule_short_youtube.py keeps title, description, tags, the funnel destination and the pinned
hashes of the approved bytes in one CONFIG dict. A Short with no entry cannot be scheduled at all,
which is how 100-103 were finished and then stranded.

Every string is emitted with json.dumps rather than by hand. A first attempt built the description
with "\\n\\n" inside an f-string and wrote a literal newline into the middle of a Python string
literal, breaking the whole module - caught by the syntax check, but only after the file was
written. json.dumps cannot get this wrong.

Usage: py -3.11 scripts/add_short_publish_config.py --dry-run | --apply
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
OUT = ROOT / "remotion" / "out"

BOILER = ("Prime Documentary covers the cases that quietly decide what the state may do to you. "
          "The full episode is linked at the top.")

ENTRIES = {
    100: dict(longform="tYZuE76Hwdc", ep="PD-2026-041-thompson",
              title="He won his freedom, then the Supreme Court took the money back",
              question="If one buried report is not enough, what would ever be enough?",
              tags=["Shorts", "Connick v Thompson", "Prosecutorial Misconduct", "Brady",
                    "Death Row", "Law", "Documentary"],
              hashtags="#Shorts #ConnickvThompson #ProsecutorialMisconduct #Brady #DeathRow "
                       "#Documentary"),
    101: dict(longform="tYZuE76Hwdc", ep="PD-2026-041-thompson",
              title="Louisiana set his execution date while the proof sat in a drawer",
              question="The report existed the whole time. Who decided it would never be handed "
                       "over?",
              tags=["Shorts", "Connick v Thompson", "Wrongful Conviction", "Brady", "Death Row",
                    "Law", "Documentary"],
              hashtags="#Shorts #ConnickvThompson #WrongfulConviction #Brady #DeathRow "
                       "#Documentary"),
    102: dict(longform="yRwxBfrOY5o", ep="PD-2026-043-caniglia",
              title="The excuse came from a 1973 case about a car. They used it on a house",
              question="Once the caretaking excuse is gone, what can officers still do at your "
                       "door?",
              tags=["Shorts", "Caniglia v Strom", "Community Caretaking", "Fourth Amendment",
                    "Welfare Check", "Law", "Documentary"],
              hashtags="#Shorts #CanigliavStrom #CommunityCaretaking #FourthAmendment "
                       "#WelfareCheck #Documentary"),
    103: dict(longform="yRwxBfrOY5o", ep="PD-2026-043-caniglia",
              title="The Court did not say police can never come in for your safety",
              question="So where exactly is the line between help and a search?",
              tags=["Shorts", "Caniglia v Strom", "Exigent Circumstances", "Fourth Amendment",
                    "Welfare Check", "Law", "Documentary"],
              hashtags="#Shorts #CanigliavStrom #ExigentCircumstances #FourthAmendment "
                       "#WelfareCheck #Documentary"),
}


def sha(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    if not a.apply and not a.dry_run:
        ap.error("pass --apply or --dry-run")

    text = SCRIPT.read_text(encoding="utf-8")
    blocks = []
    for n, c in ENTRIES.items():
        if f'    "{n}": {{' in text:
            print(f"  short{n}: already has a CONFIG entry - skipped")
            continue
        video, thumb = OUT / f"short{n}_yt_coverfirst.mp4", OUT / f"short{n}_thumb.png"
        if not video.exists() or not thumb.exists():
            print(f"  short{n}: no render or thumbnail on disk - skipped")
            continue
        desc = f"{c['title']}.\n\n{c['question']}\n\n{BOILER}\n\n{c['hashtags']}"
        b = (f'    "{n}": {{\n'
             f'        # destination for the funnel link; ensure_funnel_description() verifies it '
             f'is public\n'
             f'        "longform": {json.dumps(c["longform"])},\n'
             f'        "ep": {json.dumps(c["ep"])},\n'
             f'        "rev": "v001",\n'
             f'        "title": {json.dumps(c["title"] + " #Shorts")},\n'
             f'        "description": {json.dumps(desc)},\n'
             f'        "tags": {json.dumps(c["tags"])},\n'
             f'        # v001: this render already carries the mid-roll kinetic typography\n'
             f'        "video_sha256": {json.dumps(sha(video))},\n'
             f'        "thumb_sha256": {json.dumps(sha(thumb))},\n'
             f'    }},\n')
        blocks.append(b)
        print(f"  short{n}: {c['title'][:58]}...")

    if not blocks:
        print("nothing to add")
        return 0
    anchor = text.index('    "99": {')
    end = text.index("\n    },", anchor) + len("\n    },\n")
    new = text[:end] + "".join(blocks) + text[end:]
    print(f"\n{len(blocks)} entrie(s)" + ("" if a.apply else "   (DRY RUN)"))
    if a.apply:
        SCRIPT.write_text(new, encoding="utf-8")
        py_compile.compile(str(SCRIPT), doraise=True)
        n_now = len(re.findall(r'^    "(\d+)": \{', SCRIPT.read_text(encoding="utf-8"), re.M))
        print(f"wrote {SCRIPT.relative_to(ROOT)} - {n_now} CONFIG entries, syntax checked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
