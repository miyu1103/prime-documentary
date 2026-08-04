#!/usr/bin/env python3
"""Write the authored kinetic-typography beats into the Short designs.

Two per Short, on a number or a turn in the middle.

Wording is free (owner, 2026-08-04): the type sharpens what the line says rather than quoting it,
so "THEY KEEP WHAT THEY TAKE" is allowed over a line that never uses those words. Quantities are
not free — a figure on screen that the voice never says is indistinguishable from invention, so
numbers_not_spoken() is a hard stop here, in the assembler and in the design verifier.

Placement is by `anchor`, the phrase the voice is saying at that moment; the assembler works the
cut out from its word position, so a re-timed line moves the overlay with it instead of stranding
it. Nothing here names a cut number.

Owner approved the look on 2026-08-04 (short118). Density is one or two per Short — the assembler
refuses three.

Usage: py -3.11 scripts/author_kinetic_beats.py [--dry-run]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from assemble_short import numbers_not_spoken  # noqa: E402

DESIGNS = ROOT / "episodes" / "_planning" / "short_designs"


def punch(line: str, anchor: str, *words: str, sec: float = 2.3) -> dict:
    return {"line": line, "anchor": anchor, "style": "punch",
            "words": list(words), "bigSize": 108, "seconds": sec}


def number(line: str, anchor: str, big: str, label: str, sec: float = 2.0) -> dict:
    return {"line": line, "anchor": anchor, "style": "number", "big": big, "bigSize": 260,
            "label": label, "labelSize": 84, "seconds": sec}


BEATS: dict[str, list[dict]] = {
    "short190": [punch("L3", "built to move", "A CAR", "CAN DRIVE OFF"),
                 number("L6", "1925", "1925", "STILL THE RULE")],
    "short191": [punch("L5", "the smell of marijuana alone", "THE SMELL", "WAS ENOUGH"),
                 punch("L6", "odor is not enough", "ODOR IS", "NOT ENOUGH")],
    "short192": [number("L3", "1215", "1215", "EVEN THE KING"),
                 punch("L7", "forgotten the limit", "THEY FORGOT", "THE LIMIT")],
    "short193": [punch("L3", "more than six times over", "$2,300 BECAME", "$15,000"),
                 punch("L7", "two courts", "TWO COURTS", "TWO LOSSES")],
    "short194": [punch("L5", "more likely than not", "MORE LIKELY", "THAN NOT"),
                 punch("L7", "spend what it found", "THEY KEEP", "WHAT THEY TAKE")],
    "short195": [punch("L4", "five thousand travelers", "$209 MILLION", "5,000 TRAVELERS"),
                 punch("L7", "fifty-seven arrests", "$22 MILLION", "57 ARRESTS")],
    "short196": [punch("L3", "three hundred one deposits", "$107,702", "301 DEPOSITS"),
                 punch("L7", "not her legal fees", "WON THE CASE", "PAID THE LAWYERS")],
    "short197": [punch("L3", "nine in ten", "9 IN 10", "NO CRIME"),
                 punch("L6", "is not a law", "A MEMO", "IS NOT A LAW")],
    "short182": [punch("L4", "how far it went", "HOW FAR", "IS TOO FAR"),
                 punch("L6", "one cigarette", "ONE CIGARETTE", "IS NOT A LICENSE")],
    "short183": [punch("L4", "refused to sign", "THREE JUSTICES", "SAID NO"),
                 punch("L7", "down to a hunch", "DOWN TO", "A HUNCH")],
    "short184": [punch("L6", "an hour alone in a cell", "AN HOUR", "IN A CELL"),
                 punch("L7", "fifty dollars", "A $50 FINE", "ARRESTED ANYWAY")],
    "short185": [punch("L4", "administrative ease", "ADMINISTRATIVE", "EASE"),
                 punch("L5", "pointless indignity", "POINTLESS", "INDIGNITY")],
    "short186": [punch("L3", "flashover", "FLASHOVER"),
                 punch("L6", "not caused by heat", "NOT HEAT", "COLD WATER")],
    "short187": [punch("L3", "mystics or psychics", "MYSTICS", "OR PSYCHICS"),
                 punch("L7", "nothing since has been undone", "STILL", "NOT OVERTURNED")],
    "short188": [punch("L4", "since been discredited", "JUNK", "SCIENCE"),
                 punch("L6", "no blood on him", "NO BLOOD", "NO WEAPON")],
    "short189": [punch("L4", "for almost nothing", "ONE TEST", "ALMOST FREE"),
                 punch("L6", "ran out the clock", "HE RAN OUT", "THE CLOCK")],
    "short200": [punch("L5", "all seven", "ALL SEVEN", "EXCLUDED"),
                 punch("L7", "the eighth man", "SO THEY MADE HIM", "THE EIGHTH MAN")],
    "short201": [punch("L4", "two hundred twenty-five trials", "6,700 JURORS", "225 TRIALS"),
                 punch("L5", "four and a half times", "FOUR AND A HALF", "TIMES MORE")],
    "short202": [punch("L5", "one hundred and forty-eight", "148 CLAIMS", "HALF BELIEVED"),
                 punch("L7", "decades past its clock", "EVERY CLOCK", "HAD RUN OUT")],
    "short203": [punch("L4", "load-bearing lie", "THE LIE", "THAT HELD IT UP"),
                 number("L7", "2009", "2009", "THEY FINALLY MET")],
    "short204": [punch("L3", "about one a week", "ABOUT ONE", "EVERY WEEK"),
                 punch("L5", "almost everyone took it", "ALMOST", "EVERYONE TOOK IT")],
    "short205": [punch("L4", "sent to prison", "PREGNANT", "AND IMPRISONED"),
                 punch("L6", "not minuted", "NOT MINUTED", "NOT DISCLOSABLE")],
    "short250": [punch("L5", "eighty other compounds", "80+ COMPOUNDS", "TURN IT BLUE"),
                 number("L6", "1974", "1974", "THEY KNEW")],
    "short251": [punch("L3", "fifty-eight per cent", "58%", "PLEADED GUILTY"),
                 punch("L6", "forty-five days for a plea", "45 DAYS", "OR 2 YEARS")],
    "short252": [punch("L3", "no controlled substance", "251 CASES", "NO DRUGS"),
                 punch("L5", "ninety-three per cent", "93%", "WENT TO JAIL")],
    "short253": [punch("L4", "nothing happened", "NOTHING", "HAPPENED"),
                 number("L6", "1987", "1987", "THE LAST PLANT")],
    "short254": [punch("L4", "no legal training", "NO LAWYER", "NO SCIENTIST"),
                 punch("L7", "kitchen table", "A KITCHEN", "TABLE")],
    "short255": [punch("L3", "fifty-fifty is enough", "FIFTY-FIFTY", "IS ENOUGH"),
                 punch("L7", "four hundred and five dollars", "$405", "FOR CANCER")],
    "short256": [punch("L4", "nobody ever called back", "NOBODY", "CALLED BACK"),
                 punch("L5", "thirteen hundred miles", "1,300 MILES", "TO BE HEARD")],
    "short257": [punch("L4", "ten thousand a month", "10,000", "A MONTH"),
                 punch("L7", "four hundred documents a day", "400 A DAY", "HE READ NONE")],
    "short258": [punch("L5", "three hundred and fifty signatures", "$10 AN HOUR", "350 SIGNATURES"),
                 number("L7", "2013", "2013", "$300 EACH")],
}


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    seen, problems, written = set(), [], 0
    for f in sorted(DESIGNS.glob("*.json")):
        d = json.loads(f.read_text(encoding="utf-8"))
        touched = False
        for s in d["shorts"]:
            sid = s["short_id"]
            spec = BEATS.get(sid)
            if not spec or not s.get("lines"):
                continue
            seen.add(sid)
            lines = {l["id"]: l["text"] for l in s["lines"]}
            out = []
            for i, b in enumerate(spec):
                b = dict(b)
                b["suffix"] = "ab"[i]
                text = lines.get(b["line"], "")
                if b["anchor"].lower() not in text.lower():
                    problems.append(f"{sid} {b['suffix']}: anchor {b['anchor']!r} not in "
                                    f"{b['line']}")
                    continue
                # Wording is free (owner, 2026-08-04): the type may sharpen the line rather than
                # quote it. Quantities are not - see numbers_not_spoken.
                segs = b.get("words") or [b.get("big", ""), b.get("label", "")]
                for bad in numbers_not_spoken(segs, text):
                    problems.append(f"{sid} {b['suffix']}: shows {bad!r} but {b['line']} "
                                    f"never says it")
                out.append(b)
            if len(out) == len(spec):
                s["kinetic_beats"] = out
                touched = True
                written += 1
        if touched and not a.dry_run:
            f.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")

    missing = sorted(set(BEATS) - seen)
    for m in missing:
        problems.append(f"{m}: no design with lines found")
    print(f"{written} shorts given kinetic beats" + ("  (DRY RUN)" if a.dry_run else ""))
    if problems:
        print(f"\n{len(problems)} problems:")
        for p in problems:
            print("  " + p)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
