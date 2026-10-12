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

    # Shorts 92-181 are rendered but NOT uploaded - 63 local upload records were reconciled against
    # the channel on 2026-08-04 and every one of the 63 is live, so anything without a record has
    # not shipped and can still be improved. These are the first twelve, in schedule order.
    "short92":  [punch("L4", "fifty years", "50 YEARS", "NO NAME"),
                 number("L6", "1971", "1971", "NO CAMERA")],
    "short93":  [punch("L4", "thirty-six passengers", "36 PASSENGERS", "NEVER KNEW"),
                 punch("L6", "four parachutes", "FOUR CHUTES", "NOT ONE")],
    "short94":  [punch("L5", "five minutes", "FIVE MINUTES", "TO SEE IT"),
                 punch("L7", "Nothing happened", "NOTHING", "HAPPENED")],
    "short95":  [number("L4", "To eleven", "11", "GUILTY PLEAS"),
                 punch("L6", "Sixty-five billion", "$65 BILLION", "ON PAPER ONLY")],
    "short96":  [punch("L4", "about an hour", "30 YEARS", "ONE HOUR"),
                 number("L7", "fifty-four", "54", "TO THE CHAIR")],
    "short97":  [punch("L4", "never solved", "NEVER", "SOLVED"),
                 punch("L7", "fifteen miles away", "15 MILES AWAY", "CLOCKED IN")],
    "short98":  [punch("L5", "music played too loud", "MUSIC", "TOO LOUD"),
                 number("L7", "nine justices", "9", "ALL AGREED")],
    "short99":  [punch("L3", "foot under a descending garage door", "A FOOT", "UNDER THE DOOR"),
                 punch("L6", "Flight in, door open", "FLIGHT IN", "DOOR OPEN")],
    "short100": [punch("L5", "fourteen million dollars", "$14 MILLION", "EVERY DOLLAR GONE"),
                 punch("L7", "standard operating procedure", "STANDARD", "OPERATING PROCEDURE")],
    "short101": [punch("L4", "filing cabinet", "A FILING CABINET", "AN EXECUTION CHAMBER"),
                 punch("L5", "type B", "TYPE B", "TYPE O")],
    "short102": [number("L4", "May 2021", "2021", "NO SUCH POWER"),
                 punch("L7", "key to any door", "A KEY", "TO ANY DOOR")],
    "short103": [punch("L4", "No warrant. No crime", "NO WARRANT", "NO CRIME"),
                 punch("L6", "hear a gunshot inside", "ONE GUNSHOT", "CHANGES IT")],

    # Second batch of the unshipped 75.
    "short104": [punch("L4", "willingness to check", "NOBODY", "WANTED TO CHECK"),
                 punch("L6", "there was no coin", "THERE WAS", "NO COIN")],
    "short105": [punch("L5", "the company set the number", "THE COMPANY", "SET THE NUMBER"),
                 punch("L6", "could not really sell", "YOU COULD", "NOT SELL")],
    "short106": [punch("L3", "a crime he did not commit", "A DECADE", "NOT HIS CRIME"),
                 punch("L6", "a hundred thousand dollars", "$100,000", "FOR 11 YEARS")],
    "short107": [punch("L4", "still be wrong", "HONEST", "AND WRONG"),
                 punch("L7", "certainty wins", "CERTAINTY", "WINS")],
    "short108": [punch("L5", "Two bills", "TWO BILLS", "MOVING QUIETLY"),
                 punch("L6", "switch off entire pieces of the internet", "SWITCH OFF",
                       "THE INTERNET")],
    "short109": [punch("L4", "never really the point", "MONEY WAS", "NEVER THE POINT"),
                 punch("L6", "eighty percent", "80% OF JSTOR", "IN WEEKS")],
    "short110": [punch("L3", "four cases under a single name", "FOUR CASES", "ONE NAME"),
                 number("L7", "1966", "1966", "FIVE TO FOUR")],
    "short111": [punch("L3", "constable has blundered", "THE CONSTABLE", "HAS BLUNDERED"),
                 punch("L7", "form of words", "A FORM", "OF WORDS")],
    "short112": [punch("L5", "privacies of life", "THE PRIVACIES", "OF LIFE"),
                 punch("L6", "a thorough search of a house", "MORE THAN", "A HOUSE SEARCH")],
    "short113": [number("L3", "one hundred and sixteen", "116", "YEARS"),
                 punch("L4", "without a warrant", "NO WARRANT", "NO JUDGE")],
    "short114": [punch("L3", "How much data is too much", "HOW MUCH", "IS TOO MUCH"),
                 punch("L5", "blurry line in the right place", "A BLURRY LINE",
                       "IN THE RIGHT PLACE")],
    "short115": [punch("L3", "property itself is treated as the suspect", "THE PROPERTY",
                       "IS THE SUSPECT"),
                 punch("L7", "policing for profit", "POLICING", "FOR PROFIT")],

    # Third batch. short118 already carries the pair the look was approved on.
    "short116": [punch("L4", "fight for years to reach it", "A CEILING", "MOST NEVER REACH"),
                 number("L6", "2019", "2019", "THE GAP CLOSED")],
    "short117": [punch("L4", "erased from the Constitution", "PUBLIC USE", "ERASED"),
                 number("L7", "five to four", "5-4", "NOT THE USUAL LINES")],
    "short119": [punch("L4", "nurseries of democracy", "NURSERIES", "OF DEMOCRACY"),
                 punch("L5", "for the entire upcoming year", "ONE POST", "ONE YEAR OUT")],
    "short120": [punch("L4", "post that vanished in seconds", "A POST", "THAT VANISHED"),
                 number("L5", "two hundred and fifty", "250", "FRIENDS")],
    "short121": [punch("L4", "aloud from the bench", "READ ALOUD", "FROM THE BENCH"),
                 punch("L6", "one person at a time", "ONE AT A TIME", "OR NO ONE")],
    "short122": [punch("L3", "Take it or leave it", "TAKE IT", "OR LEAVE IT"),
                 punch("L7", "handed over voluntarily", "HANDED OVER", "VOLUNTARILY")],
    "short130": [punch("L5", "the FBI's national DNA index", "CODIS", "THE NATIONAL INDEX"),
                 punch("L7", "rightly or wrongly", "ARRESTED", "RIGHTLY OR WRONGLY")],
    "short131": [punch("L4", "quietly move tomorrow", "THE LINE", "CAN MOVE"),
                 punch("L6", "a single encounter with the police", "ONE ENCOUNTER",
                       "ON FILE FOREVER")],

    # Fourth batch.
    "short132": [punch("L3", "moving line", "A MOVING", "LINE"),
                 punch("L6", "read through walls", "READ", "THROUGH WALLS")],
    "short133": [punch("L4", "get a warrant first", "GET A", "WARRANT FIRST"),
                 number("L6", "a hundred", "100+", "PLANTS")],
    "short134": [punch("L3", "seize a sentence", "YOU CANNOT", "SEIZE A SENTENCE"),
                 number("L5", "1928", "1928", "THE OLD RULE")],
    "short135": [punch("L4", "the more ordinary it becomes to be watched", "THE MORE WATCHED",
                       "THE LESS PRIVATE"),
                 punch("L7", "freed privacy from the walls", "PRIVACY", "LEFT THE WALLS")],
    "short136": [number("L3", "seven minutes", "7", "MINUTES"),
                 punch("L6", "the clock stops", "THE CLOCK", "STOPS")],
    "short137": [punch("L5", "wait by the road", "OUT OF THE CAR", "WAIT BY THE ROAD"),
                 punch("L6", "a second door wide open", "A SECOND DOOR", "LEFT OPEN")],
    "short138": [number("L4", "2023", "2023", "ONE JUDGE"),
                 punch("L7", "no national rule", "NO NATIONAL RULE", "A PATCHWORK")],
    "short139": [punch("L5", "hand over the key", "THE KEY, YES", "THE COMBINATION, NO"),
                 number("L7", "2025", "2025", "THE OPPOSITE")],
    "short140": [punch("L3", "A fence, not the ground", "A FENCE", "NOT THE GROUND"),
                 punch("L7", "pay for the warning he skipped", "NOBODY PAYS",
                       "FOR THE WARNING")],
    "short141": [punch("L4", "no remedy can back up", "NO REMEDY", "NO RIGHT"),
                 number("L6", "the year 2000", "2000", "A CONSTITUTIONAL RULE")],
    "short142": [punch("L5", "never seen the driver's face", "NEVER SAW", "THE DRIVER"),
                 punch("L6", "not a feeling", "FACTS", "NOT A FEELING")],
    "short143": [punch("L5", "came back with a revoked license", "A PLATE",
                       "A REVOKED LICENSE"),
                 punch("L7", "a stereotype about a name, not a fact", "A STEREOTYPE",
                       "NOT A FACT")],
    "short144": [punch("L4", "illegal stop becomes almost free", "THE ILLEGAL STOP",
                       "BECOMES FREE"),
                 punch("L5", "thrown out of the case", "NORMALLY", "IT IS THROWN OUT")],
    "short145": [punch("L4", "incentive to violate the Constitution thus increases",
                       "THE INCENTIVE", "INCREASES"),
                 punch("L7", "the temptation the exclusionary rule", "THE TEMPTATION",
                       "RESTORED")],

    # Fifth batch.
    "short150": [punch("L4", "almost all are turned away", "THOUSANDS SENT",
                       "ALMOST NONE HEARD"),
                 punch("L6", "was convicted. Five years", "NO LAWYER", "FIVE YEARS")],
    "short151": [punch("L4", "With a lawyer, he was acquitted", "ALONE: GUILTY",
                       "WITH A LAWYER: FREE"),
                 punch("L5", "a necessity, not a frill", "A NECESSITY", "NOT A FRILL")],
    "short152": [punch("L4", "sixteen billion dollars", "$16 BILLION", "GONE IN A DAY"),
                 punch("L5", "taps withdraw. Nothing happens", "TAP WITHDRAW",
                       "NOTHING HAPPENS")],
    "short153": [number("L4", "seven counts", "7", "GUILTY COUNTS"),
                 punch("L6", "clawed back for customers", "CLAWED BACK", "YEARS LATER")],
    "short154": [punch("L5", "requires intent to deceive", "FRAUD NEEDS", "INTENT"),
                 punch("L6", "she believed the technology would work", "SHE KNEW",
                       "OR SHE BELIEVED")],
    "short155": [punch("L4", "nine billion dollars", "$9 BILLION", "AT ITS PEAK"),
                 punch("L6", "hundreds of tests", "HUNDREDS OF TESTS", "ONE DROP")],
    "short156": [number("L4", "thirty-six minutes", "36", "MINUTES"),
                 punch("L6", "traded at a single penny", "A GIANT COMPANY", "ONE PENNY")],
    "short157": [punch("L5", "never bought the cars", "HE NEVER", "SPENT IT"),
                 number("L6", "2015", "2015", "HIS PARENTS' HOUSE")],
    "short158": [punch("L4", "wrote the bribe off on their taxes", "THE BRIBE",
                       "WAS TAX-DEDUCTIBLE"),
                 punch("L5", "bribes as good deeds", "BRIBES DRESSED", "AS GOOD DEEDS")],
    "short159": [punch("L4", "genuinely talented student was rejected", "ONE IN BY FRAUD",
                       "ONE OUT ON MERIT"),
                 number("L5", "eight years", "8", "YEARS OPEN")],
    "short160": [punch("L5", "three thousand years old", "A BRONZE BEAKER",
                       "3,000 YEARS OLD"),
                 punch("L6", "three dozen of his works", "A VERMEER", "THREE DOZEN EXIST")],
    "short161": [punch("L4", "hidden inside a single person", "HIDDEN INSIDE", "ONE PERSON"),
                 punch("L5", "Thousands of tips", "THOUSANDS OF TIPS", "NOTHING")],
    "short162": [punch("L4", "too big to become a target", "NO COMPANY", "TOO BIG"),
                 punch("L5", "a hundred billion dollars", "$100 BILLION",
                       "ONE MAN'S MARKET")],
    "short163": [punch("L4", "supposed to kill him in a year", "ONE YEAR TO LIVE",
                       "STILL ALIVE"),
                 punch("L5", "could not get funded anywhere else", "FUNDING",
                       "NOBODY ELSE GAVE")],
    "short164": [punch("L4", "did not have to imagine the crime", "THEY DID NOT",
                       "IMAGINE IT"),
                 number("L6", "2011", "2011", "IT TURNED ON SOUND")],
    "short165": [punch("L4", "tilted in broad daylight", "TILTED", "IN BROAD DAYLIGHT"),
                 punch("L6", "the whisper is worth millions", "A WHISPER",
                       "WORTH MILLIONS")],

    # Sixth and last batch of the unshipped set.
    "short170": [punch("L4", "a collection department", "A COLLECTION", "DEPARTMENT"),
                 punch("L6", "took first, and left you to prove", "THEY TOOK FIRST",
                       "YOU PROVE IT")],
    "short171": [punch("L4", "give up their son at the door", "GIVE UP YOUR SON",
                       "OR LOSE THE HOUSE"),
                 punch("L6", "built for people exactly like them", "NOT FOR CRIMINALS",
                       "FOR PEOPLE LIKE THEM")],
    "short172": [punch("L4", "look a little like somebody else", "JUST LOOK",
                       "LIKE SOMEBODY ELSE"),
                 punch("L6", "A match is a lead, not an arrest", "A MATCH IS A LEAD",
                       "NOT AN ARREST")],
    "short173": [punch("L4", "more than a dozen known wrongful arrests", "A DOZEN KNOWN",
                       "NEARLY ALL BLACK"),
                 punch("L5", "matched by a machine", "THE MACHINE", "WAS BELIEVED")],
    "short174": [punch("L4", "quietly granted an early release", "ONE SERVED",
                       "ONE WALKED OUT"),
                 punch("L5", "doors they never saw close", "DOORS THEY",
                       "NEVER SAW CLOSE")],
    "short175": [punch("L4", "they may not print it", "THEY MAY SAY IT", "NOT PRINT IT"),
                 punch("L5", "The document they handed him", "A DOCUMENT",
                       "THAT WAS FALSE")],
    "short176": [punch("L4", "no state has a law that generally forbids", "NO STATE",
                       "FORBIDS THE LIE"),
                 punch("L6", "the average client served sixteen years", "257 CASES",
                       "16 YEARS EACH")],
    "short177": [punch("L4", "not a rule. It was a news cycle", "NOT A RULE",
                       "A NEWS CYCLE"),
                 punch("L5", "seventy thousand dollars of damage", "35 CANISTERS",
                       "$70,000 OF DAMAGE")],
    "short178": [punch("L4", "further percolation", "FURTHER", "PERCOLATION"),
                 punch("L5", "carried no legal weight", "NO LEGAL", "WEIGHT")],
    "short179": [punch("L4", "Take away the remedy", "NO REMEDY", "NO RULE"),
                 number("L6", "four votes", "4", "VOTES ONLY")],
    "short180": [punch("L4", "thirty-eight thousand people", "100 COURTS", "38,000 PEOPLE"),
                 punch("L5", "Their ruin was its revenue", "THEIR RUIN", "ITS REVENUE")],
    "short181": [number("L4", "1983", "1983", "HE WON"),
                 punch("L5", "refused while able to pay", "REFUSED TO PAY", "OR COULD NOT")],
}


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    # Overlays do not depend on the images or the mix, only on the copy, so they can be built and
    # LOOKED AT before a Short is assembled. A phrase that overflows or refits to an unreadable
    # size is far cheaper to find now than after the plates arrive.
    ap.add_argument("--emit-jobs", metavar="PATH",
                    help="write an After Effects job list for every authored beat and stop")
    ap.add_argument("--from-short", type=int, default=0, help="with --emit-jobs: lowest short id")
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
        if touched and not a.dry_run and not a.emit_jobs:
            f.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")

    if a.emit_jobs:
        jobs = []
        for sid, spec in BEATS.items():
            if int(re.sub(r"\D", "", sid)) < a.from_short:
                continue
            for i, b in enumerate(spec):
                job = {"id": f"{sid}_{'ab'[i]}", "style": b.get("style", "number"),
                       "seconds": b.get("seconds", 2.2)}
                for k in ("big", "bigSize", "label", "labelSize", "words"):
                    if k in b:
                        job[k] = b[k]
                jobs.append(job)
        Path(a.emit_jobs).write_text(json.dumps(jobs, ensure_ascii=False, indent=2),
                                     encoding="utf-8")
        print(f"{len(jobs)} AE jobs -> {a.emit_jobs}")
        print("  these use the DESIGN's seconds; assemble_short may trim one to fit its cut, "
              "and re-running render_beats.sh then is what makes the two agree")
        return 0

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
