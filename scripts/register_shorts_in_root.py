#!/usr/bin/env python3
"""Register assembled Shorts as Remotion compositions in Root.tsx.

A Short is not renderable until Root.tsx declares two things for it: the Composition that renders
the video and the Still that renders its cover frame. Assembling writes the data file and nothing
else, so 31 finished Shorts sat un-renderable with every input present - preflight caught it before
a bundle was built, which is the only reason it cost nothing.

The thumbnail headline and badge come from the design, not from a guess: `thumb_headline` and
`thumb_badge` if the design carries them, otherwise the funnel destination's own short title split
across two lines. Both are cover-frame copy and are meant to be read at a glance.

Usage:
  py -3.11 scripts/register_shorts_in_root.py --shorts 182-197,200-205,250-258 --dry-run
  py -3.11 scripts/register_shorts_in_root.py --shorts 182-197,200-205,250-258 --apply
"""
from __future__ import annotations

import argparse
import json
import py_compile
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROOT_TSX = ROOT / "remotion" / "src" / "Root.tsx"
DESIGNS = ROOT / "episodes" / "_planning" / "short_designs"
DATA = ROOT / "remotion" / "src" / "data"


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


def two_lines(text: str, cap: int = 15) -> str:
    """Split a headline across two lines on a word boundary, upper-case, for the cover frame."""
    words = (text or "").upper().split()
    a: list[str] = []
    while words and len(" ".join(a + [words[0]])) <= cap:
        a.append(words.pop(0))
    if not a:
        a = [words.pop(0)] if words else ["FULL CASE"]
    return "\\n".join([" ".join(a), " ".join(words)]).rstrip("\\n") or " ".join(a)


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

    text = ROOT_TSX.read_text(encoding="utf-8")
    imports, blocks, skipped = [], [], 0
    for n in parse_range(a.shorts):
        sid, up = f"short{n}", f"SHORT{n}"
        if f'id="Short-{sid}-yt"' in text:
            skipped += 1
            continue
        if not (DATA / f"{sid}.ts").exists():
            print(f"  {sid}: no data file - assemble it first")
            continue
        d, s = designs.get(n, (None, None))
        if s is None:
            print(f"  {sid}: no design - skipped")
            continue
        # The cover headline is the Short's own first kinetic beat. The long-form destination title
        # was tried first and was wrong twice over: it is a multi-sentence blurb that truncates to
        # nonsense, and all three Shorts of an episode share it, so their covers came out identical.
        # The beat is already two short lines, already unique per Short, and its figures are already
        # checked against the narration.
        kb = s.get("kinetic_beats") or []
        head = s.get("thumb_headline")
        if not head and kb:
            w = kb[0].get("words") or [kb[0].get("big", ""), kb[0].get("label", "")]
            head = "\\n".join(x for x in w if x)
        head = head or (d.get("destination", {}) or {}).get("title") or s["angle"]
        badge = s.get("thumb_badge") or (d["episode_id"].split("-", 3)[3][:14]).upper()
        # The beat headline already carries the LITERAL two characters \n, which is what the TSX
        # needs. Testing for a real newline missed it and re-split the string, turning
        # "PREGNANT\nAND IMPRISONED" into "PREGNANT\NAND / IMPRISONED".
        head_tsx = head if "\\n" in head else two_lines(head)
        imports.append(f"import {{{up}}} from './data/{sid}';")
        blocks.append(
            f"      {{/* ---- SHORT #{n} ---- */}}\n"
            f'      <Composition id="Short-{sid}-yt" component={{Short}}\n'
            f"        durationInFrames={{shortDurationInFrames({up}, BRAND.video.fps)}}\n"
            f"        fps={{BRAND.video.fps}} width={{1080}} height={{1920}}\n"
            f"        defaultProps={{{{data: {up}, platform: 'yt' as const, depth: true, "
            f"method: true}}}} />\n"
            f'      <Still id="ShortThumb-{sid}" component={{ShortThumb}} width={{1080}} '
            f"height={{1920}}\n"
            f"        defaultProps={{{{data: {up}, headline: '{head_tsx}', "
            f"badge: '{badge}', backgroundSrc: 'shorts/{sid}/{sid}_01.png'}}}} />\n")
        print(f"  {sid}: headline '{head_tsx.replace(chr(92)+'n', ' / ')}'  badge '{badge}'")

    print(f"\n{len(blocks)} to register, {skipped} already present"
          + ("" if a.apply else "   (DRY RUN)"))
    if not blocks or not a.apply:
        return 0

    # after the last existing data import, and before the closing tag of the compositions list
    last_import = text.rindex("from './data/")
    eol = text.index("\n", last_import) + 1
    text = text[:eol] + "\n".join(imports) + "\n" + text[eol:]
    close = text.rindex("</>")
    text = text[:close] + "".join(blocks) + text[close:]
    ROOT_TSX.write_text(text, encoding="utf-8")
    print(f"wrote {ROOT_TSX.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
