#!/usr/bin/env python3
"""Refuse an image order whose canonical [NEG] cannot stop the thing it exists to stop.

Why this exists: on 2026-08-05 the visual QC of EP65 found three plates that came back as fully
identifiable elderly women. Two of them (R019, R041) had been ordered as *a sheet of paper* and
*a statute volume* -- their prompt bodies never mentioned a person, so they carried no "no face"
clause, and the episode's canonical [NEG] contained no face-suppressing token at all. Nor did
EP62's, EP63's or EP64's. EP62 G174, ordered as a records room, had already come back the same
way and was caught only by eye; a Haar cascade run over the same plate missed it entirely while
firing on twenty wall textures.

Invariant 11 forbids real-person likeness in generated visuals. The [NEG] block is the mechanism
that is supposed to hold it across every plate in an order, including the ones nobody thought to
write "no face" into. This checks that the mechanism exists.

    py -3.11 scripts/check_image_order_neg.py                       # every batch order in _planning
    py -3.11 scripts/check_image_order_neg.py --file <path>         # one order
    py -3.11 scripts/check_image_order_neg.py --demo-fail           # prove it rejects a bad [NEG]

Exit 0 = every order checked carries the required token families. Exit 1 = at least one does not.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[1]
PLANNING = ROOT / "episodes" / "_planning"

# Each family needs at least ONE of its tokens present. Synonyms are listed because orders are
# written by hand and spell things differently; the point is that the family is covered at all.
REQUIRED: dict[str, tuple[str, ...]] = {
    "face / likeness": ("human face", "facial features", "eye contact", "portrait", "headshot",
                        "identifiable person", "recognisable person", "recognizable person",
                        "looking at the camera", "profile of a face"),
    "readable text": ("text", "lettering", "legible text", "readable text"),
    "handwriting": ("handwriting", "cursive", "signature", "legible signature"),
    "marks of authority": ("seals", "seal", "emblems", "emblem", "logos", "logo",
                           "badge", "insignia"),
    "numerals": ("numerals", "numbers", "digits", "house numbers"),
}


def neg_block(text: str) -> str | None:
    """The canonical [NEG] definition line(s) of an order.

    Orders write it as a blockquote line that begins the avoid-list. Take the longest blockquote
    line that reads like a negative list, so a short mention elsewhere cannot satisfy the check.
    """
    cands = [l for l in text.splitlines()
             if l.lstrip().startswith(">") and re.search(r"\btext\b.*\blettering\b", l, re.I)]
    return max(cands, key=len) if cands else None


def check(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    block = neg_block(text)
    if block is None:
        return [f"{path.name}: no canonical [NEG] definition found "
                f"(expected a blockquote line listing text and lettering)"]
    low = block.lower()
    problems = []
    for family, tokens in REQUIRED.items():
        if not any(t in low for t in tokens):
            problems.append(f"{path.name}: [NEG] has no token for {family!r}. "
                            f"Any plate whose prompt body forgets to say it is unprotected. "
                            f"Add one of: {', '.join(tokens[:4])}")
    return problems


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", help="check one order instead of all of them")
    ap.add_argument("--demo-fail", action="store_true",
                    help="run against a deliberately bad [NEG] to show the check rejecting it")
    a = ap.parse_args()

    if a.demo_fail:
        bad = ("> text, lettering, numerals, handwriting, signatures, seals, emblems, logos, "
               "signage, police uniform, badge, patrol car, gavel, prison bars, handcuffs, "
               "golden hour, drone shot, cartoon, oversaturated")
        tmp = Path(__file__).with_name("_neg_demo.md")
        tmp.write_text("# demo order\n\n" + bad + "\n", encoding="utf-8")
        try:
            problems = check(tmp)
        finally:
            tmp.unlink(missing_ok=True)
        print("[neg] DEMO: an order that bans uniforms, badges and gavels but no faces")
        for p in problems:
            print(f"  REJECT {p}")
        print(f"\n{len(problems)} problem(s) -- this is the shape that let EP62 G174 and "
              f"EP65 R019/R041/R065 through.")
        return 1 if problems else 0

    if a.file:
        paths = [Path(a.file)]
    else:
        paths = sorted(PLANNING.glob("EP*_CODEX_BATCH_*.md"))
    if not paths:
        print("[neg] no image orders found", file=sys.stderr)
        return 1

    problems: list[str] = []
    for p in paths:
        found = check(p)
        problems += found
        print(f"[neg] {'ok  ' if not found else 'FAIL'} {p.name}")

    if problems:
        print(file=sys.stderr)
        for p in problems:
            print(f"  REJECT {p}", file=sys.stderr)
        print(f"\n{len(problems)} problem(s) across {len(paths)} order(s)", file=sys.stderr)
        return 1
    print(f"\n[neg] {len(paths)} order(s): every [NEG] carries all "
          f"{len(REQUIRED)} required token families")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
