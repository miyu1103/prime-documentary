#!/usr/bin/env python3
"""Write the authored kinetic-typography beats into the Short designs.

Two per Short, on a number or a turn in the middle. Every phrase below is lifted VERBATIM from the
narration line it sits on, which is the only reason the type can be trusted to match the voice —
assemble_short.py re-checks it and warns on any token the line does not contain.

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
DESIGNS = ROOT / "episodes" / "_planning" / "short_designs"


def punch(line: str, anchor: str, *words: str, sec: float = 2.3) -> dict:
    return {"line": line, "anchor": anchor, "style": "punch",
            "words": list(words), "bigSize": 108, "seconds": sec}


def number(line: str, anchor: str, big: str, label: str, sec: float = 2.0) -> dict:
    return {"line": line, "anchor": anchor, "style": "number", "big": big, "bigSize": 260,
            "label": label, "labelSize": 84, "seconds": sec}


BEATS: dict[str, list[dict]] = {
    "short190": [punch("L3", "built to move", "A CAR IS", "BUILT TO MOVE"),
                 number("L6", "1925", "1925", "YOUR GLOVEBOX")],
    "short191": [punch("L5", "the smell of marijuana alone", "THE SMELL", "ALONE"),
                 punch("L6", "odor is not enough", "ODOR IS", "NOT ENOUGH")],
    "short192": [number("L3", "1215", "1215", "MAGNA CARTA"),
                 punch("L7", "forgotten the limit", "FORGOTTEN", "THE LIMIT")],
    "short193": [punch("L3", "more than six times over", "MORE THAN", "SIX TIMES OVER"),
                 punch("L7", "two courts", "TWO COURTS", "TWO LOSSES")],
    "short194": [punch("L5", "more likely than not", "MORE LIKELY", "THAN NOT"),
                 punch("L7", "emptied your bag", "EMPTIED", "YOUR BAG")],
    "short195": [punch("L4", "five thousand travelers", "FIVE THOUSAND", "TRAVELERS"),
                 punch("L7", "fifty-seven arrests", "FIFTY-SEVEN", "ARRESTS")],
    "short196": [punch("L3", "three hundred one deposits", "THREE HUNDRED", "ONE DEPOSITS"),
                 punch("L7", "not her legal fees", "NOT HER", "LEGAL FEES")],
    "short197": [punch("L3", "nine in ten", "NINE", "IN TEN"),
                 punch("L6", "is not a law", "A POLICY MEMO", "IS NOT A LAW")],
    "short182": [punch("L4", "related in scope", "RELATED", "IN SCOPE"),
                 punch("L6", "past what set it off", "PAST WHAT", "SET IT OFF")],
    "short183": [punch("L4", "refused to sign", "THREE JUSTICES", "REFUSED"),
                 punch("L7", "down to a hunch", "DOWN TO", "A HUNCH")],
    "short184": [punch("L6", "an hour alone in a cell", "AN HOUR", "IN A CELL"),
                 punch("L7", "fifty dollars", "FIFTY", "DOLLARS")],
    "short185": [punch("L4", "administrative ease", "ADMINISTRATIVE", "EASE"),
                 punch("L5", "pointless indignity", "POINTLESS", "INDIGNITY")],
    "short186": [punch("L3", "flashover", "FLASHOVER"),
                 punch("L6", "not caused by heat", "NOT CAUSED", "BY HEAT")],
    "short187": [punch("L3", "mystics or psychics", "MYSTICS", "OR PSYCHICS"),
                 punch("L7", "nothing since has been undone", "NOTHING SINCE", "HAS BEEN UNDONE")],
    "short188": [punch("L4", "since been discredited", "SINCE", "DISCREDITED"),
                 punch("L6", "no blood on him", "NO BLOOD", "NO WEAPON")],
    "short189": [punch("L4", "for almost nothing", "FOR ALMOST", "NOTHING"),
                 punch("L6", "ran out the clock", "RAN OUT", "THE CLOCK")],
    "short200": [punch("L5", "all seven", "ALL SEVEN", "EXCLUDED"),
                 punch("L7", "the eighth man", "THE EIGHTH", "MAN")],
    "short201": [punch("L4", "two hundred twenty-five trials", "TWO HUNDRED", "TWENTY-FIVE TRIALS"),
                 punch("L5", "four and a half times", "FOUR AND", "A HALF TIMES")],
    "short202": [punch("L5", "one hundred and forty-eight", "ONE HUNDRED", "FORTY-EIGHT CLAIMS"),
                 punch("L7", "decades past its clock", "DECADES PAST", "ITS CLOCK")],
    "short203": [punch("L4", "load-bearing lie", "THE LOAD-BEARING", "LIE"),
                 number("L7", "2009", "2009", "THEY FINALLY MET")],
    "short204": [punch("L3", "about one a week", "ABOUT ONE", "A WEEK"),
                 punch("L5", "almost everyone took it", "ALMOST", "EVERYONE TOOK IT")],
    "short205": [punch("L4", "fifteen months", "FIFTEEN", "MONTHS"),
                 punch("L6", "not minuted", "NOT MINUTED", "NOT DISCLOSABLE")],
    "short250": [punch("L5", "eighty other compounds", "EIGHTY OTHER", "COMPOUNDS"),
                 number("L6", "1974", "1974", "NOT SOLE EVIDENCE")],
    "short251": [punch("L3", "fifty-eight per cent", "FIFTY-EIGHT", "PER CENT"),
                 punch("L7", "forty-five days", "FORTY-FIVE", "DAYS")],
    "short252": [punch("L3", "no controlled substance", "NO CONTROLLED", "SUBSTANCE"),
                 punch("L5", "ninety-three per cent", "NINETY-THREE", "PER CENT")],
    "short253": [punch("L4", "nothing happened", "NOTHING", "HAPPENED"),
                 number("L6", "1987", "1987", "THE PLANT CLOSED")],
    "short254": [punch("L4", "no legal training", "NO LEGAL", "TRAINING"),
                 punch("L7", "kitchen table", "A KITCHEN", "TABLE")],
    "short255": [punch("L3", "fifty-fifty is enough", "FIFTY-FIFTY", "IS ENOUGH"),
                 punch("L7", "four hundred and five dollars", "FOUR HUNDRED", "AND FIVE DOLLARS")],
    "short256": [punch("L4", "nobody ever called back", "NOBODY EVER", "CALLED BACK"),
                 punch("L5", "thirteen hundred miles", "THIRTEEN", "HUNDRED MILES")],
    "short257": [punch("L4", "ten thousand a month", "TEN THOUSAND", "A MONTH"),
                 punch("L7", "four hundred documents a day", "FOUR HUNDRED", "A DAY")],
    "short258": [punch("L5", "three hundred and fifty signatures", "THREE HUNDRED FIFTY", "AN HOUR"),
                 number("L7", "2013", "2013", "THE PAYMENT TABLE")],
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
                phrase = " ".join(b.get("words") or [b.get("big", ""), b.get("label", "")])
                low = text.lower().replace(",", "").replace(".", "")
                for tok in re.findall(r"[A-Za-z0-9-]+", phrase):
                    if len(tok) > 2 and tok.lower() not in low:
                        problems.append(f"{sid} {b['suffix']}: {tok!r} is not spoken in "
                                        f"{b['line']}")
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
