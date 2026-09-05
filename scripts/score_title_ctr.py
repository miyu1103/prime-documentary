#!/usr/bin/env python
"""Score a title draft on the features that actually moved PD's CTR.

WHERE THE WEIGHTS COME FROM. `scripts/_yt_studio_video_ctr.20260819.json` is Studio's own
28-day window ending 2026-08-19. Restricted to long-form with at least 300 impressions
(n = 38, 57,573 impressions, weighted CTR 1.63 %, median 1.20 %):

    two sentences .............. 1.79 %  vs 1.25 %
    opens on the authority ..... 2.12 %  vs 1.47 %
    >= 70 characters ........... 1.73 %  vs 1.18 %
    contains a `$` figure ...... 1.40 %  vs 1.75 %      <- negative
    contains any digit ......... 1.62 %  vs 1.72 %      <- nothing

The four best converters were 3.89, 3.71, 3.14 and 3.11 %. Reading them against the four
worst (0.00, 0.30, 0.38, 0.39 %) gives one feature the table above cannot express, because it
is not a format but a subject choice:

    3.89  Police Searched the MOTORCYCLE in his DRIVEWAY...
    3.11  A Detective Watched Two Men Pace a STORE WINDOW...
    2.50  Police Took his $42,000 CAR...
    2.24  ...His CARRIER Handed Over 127 DAYS of Where He Had Been
    ----
    0.38  Police Raided the Wrong House and Handcuffed an Innocent Woman   (no object)
    0.96  The Stop Was Illegal - the Supreme Court Kept the Evidence Anyway (no object)
    0.00  The Machine Never Worked. The Company Was Valued at $9 Billion Anyway. (no person)

A NAMED PHYSICAL THING in a NAMED ORDINARY PLACE is what the winners have and the losers do
not. So `object` and `place` carry the heaviest weights here.

HONEST LIMITS, because a weight that is not doubted becomes folklore:
  * n = 38. These are correlations on a small, self-selected set.
  * CTR and impressions are confounded: a topic that earns 4,806 impressions is being shown
    to a different, colder audience than one earning 626, and colder audiences click less.
    Atwater ("A Seatbelt Ticket Carried No Jail Time. She Was Handcuffed in Front of Her
    Children.") has every feature below and converted at 0.39 %. This scorer does not
    explain it. Something not in the title -- almost certainly the thumbnail -- is missing.
  * Nothing here measures whether an audience exists. Run `topic_demand_probe.py` as well.
    GM's 57-cent part scores high here and measured a median of 145 views.

    py -3.11 scripts/score_title_ctr.py --title "..."
    py -3.11 scripts/score_title_ctr.py --pool episodes/_planning/TOPIC_POOL_500.v001.md --top 40
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

AUTHORITY = r"^(the\s+)?(police|a\s+detective|detectives|officers?|an?\s+officer|agents?|a\s+federal|" \
            r"the\s+(state|court|judge|sheriff|city|county|company|bank|hospital|insurer|prosecutor|" \
            r"government|army|navy|regulator|department|lab|jury|fbi|irs|va)|a\s+(judge|sheriff|deputy|" \
            r"prosecutor|federal\s+agent|coroner)|two\s+detectives|a\s+sheriff)"

OBJECT = (r"motorcycle|car\b|truck|jeep|van|boat|ferry|ship|tanker|train|bus|phone|glovebox|"
          r"door|doors|porch|window|safe|ladder|tyre|tire|airbag|helmet|rifle|gun|seatbelt|"
          r"ticket|receipt|letter|deed|note|kit|sample|tape|camera|meter|valve|pump|pipe|"
          r"bin|trench|crib|helicopter|ladder|scaffold|crane|cash|banknote|chips|ring|"
          r"machine|implant|mesh|heater|battery|foam|earplug|powder|seed|manual|form")

PLACE = (r"driveway|garage|porch|kitchen|basement|bedroom|hallway|parking lot|glovebox|"
         r"front (door|porch|yard)|airport|roadside|highway|motel|barn|shed|farm|dock|harbour|"
         r"harbor|platform|rig|refinery|plant|mine|trench|store window|break room|"
         r"waiting room|emergency room|classroom|courthouse|county|street|his own (home|property|garage)")


def score(title: str) -> tuple[int, list[str]]:
    t = title.strip()
    low = t.lower()
    pts, why = 0, []

    sentences = [s for s in re.split(r"(?<=[.!])\s+", t) if s.strip()]
    if len(sentences) >= 2:
        pts += 2; why.append("+2 two sentences")
    else:
        why.append(" 0 single clause")

    if re.match(AUTHORITY, low):
        pts += 2; why.append("+2 opens on the authority")
    else:
        why.append(" 0 does not open on the authority")

    n = len(t)
    if 70 <= n <= 100:
        pts += 1; why.append(f"+1 {n} chars (in band)")
    elif n < 70:
        why.append(f" 0 {n} chars (short: 1.18% band)")
    else:
        why.append(f" 0 {n} chars (over 100)")

    if re.search(OBJECT, low):
        pts += 3; why.append("+3 names a physical object")
    else:
        pts -= 2; why.append("-2 NO physical object")

    if re.search(PLACE, low):
        pts += 3; why.append("+3 names an ordinary place")
    else:
        why.append(" 0 no ordinary place")

    if "$" in t:
        pts -= 1; why.append("-1 carries a $ figure")

    if re.search(r"\b(one|two|three|four|nine|eleven|twenty-seven|\d{1,4})\b", low):
        pts += 1; why.append("+1 a specific count")

    if t.endswith("?"):
        pts -= 3; why.append("-3 question form (v3 forbids)")

    return pts, why


def pool_rows(path: Path):
    for ln in path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^\|\s*(\d+)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|", ln)
        if m:
            yield int(m.group(1)), m.group(2), m.group(3)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--title")
    ap.add_argument("--pool")
    ap.add_argument("--top", type=int, default=40)
    a = ap.parse_args()

    if a.title:
        s, why = score(a.title)
        print(f"score {s}\n  " + "\n  ".join(why))
        return 0

    if not a.pool:
        ap.error("--title or --pool")
    rows = [(n, t, c, *score(t)) for n, t, c in pool_rows(ROOT / a.pool)]
    rows.sort(key=lambda r: (-r[3], r[0]))
    print(f"scored {len(rows)} rows from {a.pool}\n")
    for n, t, c, s, _ in rows[:a.top]:
        print(f"{s:3d}  #{n:<4d} {t[:88]}\n          case: {c[:80]}")
    from collections import Counter
    print("\nscore distribution:", dict(sorted(Counter(r[3] for r in rows).items(), reverse=True)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
