#!/usr/bin/env python3
r"""Extend EP68 pinto and EP69 hyatt to EP67's three-tier shape: declared + headroom + thumbnails.

WHY (measured 2026-08-11)
-------------------------
    ep         declared  ordered  thumbs  headroom
    ramirez         122      152       6        24
    pinto           104      104       0         0
    hyatt           113      113       0         0

Both specs declare `thumbnail_candidates_min: 3` and NEITHER ORDER CONTAINED A SINGLE THUMBNAIL
PLATE. And at EP66 batch C's measured reject-and-flag rate, an order with no headroom delivers
fewer usable plates than the contract declares. Both gaps are arithmetic, and both are fixed
before a single plate is generated rather than after the first assembly shows the film is thin.

Re-derived here rather than taken on trust -- see `derivations()` below, which prints the
arithmetic and the solver output it rests on.

WHAT THIS SCRIPT DOES AND DOES NOT TOUCH
-----------------------------------------
  writes   episodes/_planning/EP6X_<slug>_CODEX_BATCH_B.v001.md      (new, immutable: invariant 6)
  writes   episodes/_planning/EP6X_<slug>_CODEX_PASTE_A/headroom_*.txt
  writes   episodes/_planning/EP6X_<slug>_CODEX_PASTE_A/thumbs_01.txt
  writes   episodes/_planning/EP6X_<slug>_CODEX_PASTE_ALL.txt        (regenerated, all tiers)
  reads    episodes/_planning/EP6X_<slug>_CODEX_PASTE_A/batch_*.txt  (the declared prompts)
  reads    episodes/_planning/EP6X_<slug>_CODEX_BATCH_A.v001.md      (the canonical [NEG])
  touches  nothing else. batch_*.txt and BATCH_A.v001.md are never modified.

THE CANONICAL BLOCKS ARE READ, NEVER RETYPED
----------------------------------------------
`[STYLE]`, `[NEG]`, `[HSTYLE]` and the 絶対条件 block are lifted out of the episode's OWN existing
paste files at generation time, so the new tiers cannot say them slightly differently. The `[NEG]`
lifted from the paste files is then cross-checked BYTE FOR BYTE against the `[NEG]` blockquote in
that episode's BATCH_A document, and the generator refuses to write if they differ, if any of the
seven identifiability tokens is missing, or if any of the three tokens that caused EP66's
191-plate rebuild (`human face`, `facial features`, `eyes`) has come back.

    NOTE ON "byte-identical to batch D's". EP67 ramirez reads its `[NEG]` out of EP66's batch D
    and is byte-identical to it (925 chars, verified). EP68 and EP69 ARE NOT AND MUST NOT BE:
    each authored an episode-specific `[NEG]` at 1210 and 1150 chars, adding pinto's twenty-three
    fire words and eight crash words and hyatt's collapse/rubble/rescue and post-1990 bans. Those
    additions are the machine half of ⛔-11..⛔-15 in each film bible. The invariant that actually
    holds -- and that this generator enforces -- is that EVERY tier of an episode's order carries
    that episode's OWN canonical `[NEG]`, unchanged, including the thumbnail lane.

WHY THUMBNAILS GET THEIR OWN [TSTYLE], AND WHY THAT IS NOT A DEVIATION
------------------------------------------------------------------------
The canonical `[STYLE]` of both episodes mandates "low contrast but never crushed", which is
right for a film frame and is exactly why EP65's four thumbnail candidates came back as dull grey
paper and had to be re-ordered. A thumbnail is not a film frame: `thumb_subject_luma` wants a
subject box of mean luma >= 60 and a bright connected component >= 150 px, and the builder
(`build_ep62_65_thumbnails.py`) lays a black scrim at alpha 120 over the top 66% before the
headline goes on. So the thumbnail lane gets one hard directional key, high contrast, bright
exposure, subject brighter than background, the whole subject in the lower 60% with the bottom
third the brightest part, and THE ENTIRE UPPER 40% OF THE FRAME AN UNBROKEN FIELD.

`[NEG]` is NOT deviated for the thumbnail lane. Only the style block changes.

HEADROOM IS ORDERED, NOT DECLARED
-----------------------------------
`check_spec_satisfied.py` fails any `mandatory_stills` id that appears in no cut. Declaring the
headroom would therefore fail the build on plates that exist and are fine. `episode_spec.v001.json`
is not edited by this script, and must not be. Thumbnails are neither declared nor cut.

    py -3.11 scripts/build_ep68_ep69_headroom_order.py             # write + verify
    py -3.11 scripts/build_ep68_ep69_headroom_order.py --verify    # verify only, write nothing
    py -3.11 scripts/build_ep68_ep69_headroom_order.py --derive    # print the arithmetic only
"""
from __future__ import annotations

import argparse
import math
import re
import sys
import unicodedata
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:  # pragma: no cover
    pass

ROOT = Path(__file__).resolve().parents[1]
PLANNING = ROOT / "episodes" / "_planning"
sys.path.insert(0, str(ROOT / "scripts"))

# EP66 batch C is the only measured plate-rejection rate this channel has: 191 ordered,
# 11 REJECT and 10 FLAG. Reproduced mechanically by check_plate_verdicts.ingest_md over
# runs/qc/openfields_plate_verdicts.v001.md -> {'accept': 170, 'reject': 11, 'unresolved': 10}.
EP66_ORDERED = 191
EP66_REJECT = 11
EP66_FLAG = 10
REJECT_ONLY = EP66_REJECT / EP66_ORDERED                      # 0.0576
REJECT_AND_FLAG = (EP66_REJECT + EP66_FLAG) / EP66_ORDERED    # 0.1099

THUMBS_PER_EPISODE = 6      # spec declares thumbnail_candidates_min 3; the packaging documents
                            # specify three variants, and each is ordered as a framing PAIR so a
                            # variant that comes back badly framed still leaves three candidates.

HEADROOM_CHUNK = 7
THUMB_CHUNK = 6


# =============================================================================================
# reading the canonical blocks out of the episode's own files
# =============================================================================================
STYLE_MARK = "各プロンプト末尾の [STYLE] は、次の文言に置き換えてください:"
NEG_MARK = "各プロンプト末尾の Avoid: [NEG] は、次の文言に置き換えてください:"
RULES_OPEN = "──────── 絶対条件 ────────"
RULES_CLOSE = "──────── プロンプト ────────"


def _after_marker(text: str, marker: str) -> str:
    """The first non-blank line after a marker line. Blocks are single lines in the paste files."""
    lines = text.splitlines()
    for i, l in enumerate(lines):
        if l.strip() == marker:
            for j in range(i + 1, len(lines)):
                if lines[j].strip():
                    return lines[j].rstrip()
    raise SystemExit(f"marker not found in paste file: {marker}")


def _rules_block(text: str) -> list[str]:
    lines = text.splitlines()
    try:
        a = lines.index(RULES_OPEN)
        b = lines.index(RULES_CLOSE)
    except ValueError as exc:
        raise SystemExit(f"絶対条件 block not found: {exc}") from exc
    return [l.rstrip() for l in lines[a:b] if l.strip() or True][:-0 or None]


def parse_prompts(text: str) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    lines = text.splitlines()
    for i, l in enumerate(lines):
        if l.startswith("■ "):
            out.append((l[2:].strip(), lines[i + 1].rstrip() if i + 1 < len(lines) else ""))
    return out


def neg_from_doc(doc: Path) -> str:
    from check_image_order_neg import neg_block
    b = neg_block(doc.read_text(encoding="utf-8"))
    if b is None:
        raise SystemExit(f"no canonical [NEG] blockquote in {doc.name}")
    return b.lstrip("> ").strip()


HSTYLE_MARK = "★プロンプト冒頭の [HSTYLE] は、次の文言に置き換えてください:"


def hstyle_of(batch_texts: list[str], prompts: list[tuple[str, str]]) -> str:
    """The [HSTYLE] preamble, READ from the episode own paste files and never retyped.

    The two episodes do it differently and the first version of this function silently returned
    an empty string for one of them, which shipped a merged file whose [HSTYLE] section said
    nothing at all. Caught by reading the emitted file. Both shapes are now handled and an empty
    result is a hard failure:

      EP69 hyatt INLINES the preamble into every people-lane prompt body, so the longest common
                 prefix of those bodies IS the preamble.
      EP68 pinto keeps the literal token `[HSTYLE]` in the body and defines it once, under a
                 marker line, in the people-lane batch file.
    """
    for t in batch_texts:
        if HSTYLE_MARK in t:
            return _after_marker(t, HSTYLE_MARK)
    bodies = [b for _, b in prompts if b.startswith("[HSTYLE] ")]
    if not bodies:
        return ""
    pre = bodies[0]
    for b in bodies[1:]:
        n = 0
        while n < min(len(pre), len(b)) and pre[n] == b[n]:
            n += 1
        pre = pre[:n]
    cut = pre.rfind(". ")
    out = (pre[:cut] if cut > 0 else pre).strip()
    if out in ("", "[HSTYLE]"):
        raise SystemExit("the [HSTYLE] preamble resolved to nothing -- refusing to emit a merged "
                         "file whose people-lane instruction is empty")
    return out


# =============================================================================================
# the new plates
# =============================================================================================
# (id, body, neg_add, script line it carries, ledger/section reference)
#
# EVERY HEADROOM AND THUMBNAIL PROMPT BELOW IS SELF-CONTAINED. None of them says "the same X"
# about a plate that lives in another paste file: on an earlier order eighteen prompts referred
# to "the same desk" with the referent in a different chunk, and a generator has no memory
# between prompts. Where two of these plates are deliberately a pair they are adjacent in the
# SAME file and each still describes its whole scene.

PINTO_HEADROOM: list[tuple[str, str, str, str, str]] = [
    ("R105",
     "A workshop lift raised to chest height with an early-1970s American subcompact hatchback "
     "standing on it, photographed from the side at floor level from twelve feet away so the "
     "whole underbody runs across the middle of the frame as one long dark band, one work light "
     "on a stand throwing hard raking light along it from the left, bare stained concrete in the "
     "foreground and a dim shop wall behind. Nobody is in the frame. No vehicle anywhere in this "
     "frame carries a mark of any kind: no badge, no emblem, no oval on the grille, no wordmark, "
     "no nameplate, no model lettering and no plate of any kind on any part of it, front or rear. "
     "The car is undamaged and intact",
     "licence plate, registration plate, number plate, badge on the grille, oval emblem, "
     "manufacturer wordmark, chrome nameplate, shop signage, price sticker, crumpled bodywork, "
     "collision damage, fire, flame, smoke, scorch marks, person in frame",
     "The design was not on trial. It could not be.",
     "ACT_1 / ACT_4 — H1 register, second camera position"),

    ("R106",
     "A plain pressed-steel fuel tank shell removed from a car and standing alone on a heavy "
     "workbench on its flat forward face, photographed straight on from bench height under one "
     "work lamp, the pressed seam running across it and nothing else on its surface, the metal "
     "dull grey and lightly scuffed, a dark shop falling away behind it. The shell is empty, "
     "clean, dry and undamaged, and there is no liquid, no vapour, no flame and no scorching "
     "anywhere in the picture. No badge, no stamped mark, no label and no writing on it",
     "fire, flame, smoke, fuel spill, liquid, vapour, scorch marks, rust holes, crumpled metal, "
     "stamped lettering, part number, manufacturer wordmark, label, sticker",
     "The remedy was a longer fuel filler pipe with an improved seal, and a polyethylene "
     "shield installed on the front of the fuel tank.",
     "ACT_3 — the tank shell alone, and the remedy"),

    ("R107",
     "A wide three-lane American freeway photographed from the hard shoulder at dusk with a low "
     "wide lens, the pale concrete running away to a low ridge on the horizon and going cold "
     "blue-grey as the light leaves it, dry Southern Californian scrub along the shoulder, the "
     "lane markings just holding their brightness. There is no vehicle anywhere in the frame and "
     "nobody is on the road",
     "vehicles, cars, traffic, headlights, tail lights, street lighting, road signs, gantry, "
     "billboard, golden hour, sunset glow, orange sky",
     "What was left was a fight about speed.",
     "ACT_2 — the H5 freeway register at a second hour"),

    ("R108",
     "A 1970s wire-service teleprinter standing on a steel stand in the corner of a newspaper "
     "office, photographed three-quarter from the side at standing height, a continuous roll of "
     "pale paper feeding up out of the machine and falling in a loose fold to the floor, the "
     "printing on the paper reduced by distance and shallow focus to fine even grey banding with "
     "no character, word or line resolving anywhere on it. Flat overhead office light, nobody in "
     "the room",
     "legible typing, readable words on a page, letterforms, printed paragraph, headline, "
     "masthead, letterhead, manufacturer wordmark on the machine, nameplate, person in frame",
     "The wire report named them:",
     "ACT_3 / ACT_5 — the wire copy, never legible"),

    ("R109",
     "A two-lane blacktop road running dead straight away from the camera between two walls of "
     "corn at full height in flat mid-August light, photographed from the middle of the road at "
     "standing height, the crown of the road slightly raised, telephone poles receding down the "
     "left verge, a wide pale sky above and no cloud shape in it. Northern Indiana farmland. "
     "There is no vehicle in the frame and nobody is on the road, and no sign, board or marker "
     "carries any writing",
     "vehicles, cars, traffic, road signs with words, billboards, mailboxes with names, "
     "farm signage, golden hour, sunset glow, person in frame",
     "On the tenth of August, nineteen seventy-eight, in Elkhart County, Indiana",
     "ACT_5 — Indiana, the road register (IN-04)"),

    ("R110",
     "A tall corrugated-steel grain elevator standing over a set of rail sidings under flat "
     "overcast light in a small Midwestern farming town, photographed from across the tracks at "
     "standing height so the elevator fills the right of the frame and empty gravel and rail run "
     "away to the left, weeds between the sleepers, no lettering, no company name and no painted "
     "sign anywhere on the steel. Nobody is in the frame",
     "painted lettering on the silo, company name, grain co-op sign, billboard, modern trucks, "
     "modern cars, person in frame",
     "and the Indiana register",
     "ACT_5 — the Indiana register (section direction block)"),

    ("R111",
     "A small Midwestern county courthouse square in flat grey light: a modest three-storey "
     "limestone courthouse standing across an empty street with a bare metal flagpole in front of "
     "it carrying no flag, a small open bandstand on the lawn, mature trees bare of leaves, "
     "photographed from the far pavement at standing height. There is no signage of any kind on "
     "the building or the lawn, no vehicle at the kerb and nobody in the frame",
     "courthouse signage, engraved lettering on the stone, plaques, notice boards, flags, "
     "vehicles at the kerb, modern cars, person in frame, courtroom interior",
     "and judgment was entered at Winamac, in the Pulaski County Circuit Court",
     "ACT_5 — Winamac, from outside (IN2-02 / SW2-14)"),

    ("R112",
     "A two-storey small-town American main street at midday, brick shopfronts down both sides "
     "with plain canvas awnings out over the pavement, photographed from the middle of the road "
     "at standing height so the street runs away into flat haze, the pavement empty, the light "
     "hard and colourless. Not one window, awning, board or fascia carries any lettering, name or "
     "number, and there is no vehicle and nobody in the frame",
     "shop signage, fascia lettering, window lettering, awning text, street signs, house numbers, "
     "billboards, parked cars, modern cars, person in frame",
     "On the thirteenth of March nineteen eighty, the jury found Ford not guilty.",
     "ACT_5 — the town, the morning after"),

    ("R113",
     "A gravel county road junction between two flat fields, photographed from the middle of one "
     "road at standing height so both roads run away to the horizon, a single plain white-painted "
     "wooden signpost standing at the corner with two blank arms on it that carry no lettering, no "
     "arrow and no number, dry grass in the verge, a wide pale overcast sky. No vehicle, no "
     "building and nobody in the frame",
     "lettering on the signpost, route numbers, arrows with names, road signs with words, "
     "mailboxes with names, vehicles, person in frame",
     "The venue then changed",
     "ACT_5 — the change of venue (IN2-01 / IN2-02)"),

    ("R114",
     "A plain 1970s American federal hearing room, completely empty: a low carpeted dais across "
     "the far end with a bare wooden lectern standing on it that carries no seal, no crest and no "
     "lettering of any kind, six rows of grey stacking chairs facing it, a run of fluorescent "
     "troffers in a low acoustic-tile ceiling, institutional pale green walls. Photographed from "
     "the back of the room at standing height. Nobody is present",
     "seal on the lectern, crest, flag, insignia, nameplates, lettering on the wall, "
     "courtroom interior, gavel, judge's bench, jury box, witness stand, person in frame",
     "The hearing never happened.",
     "ACT_3 / ACT_4 — the regulator, in public session"),

    ("R115",
     "A long institutional corridor in a 1970s American federal building, photographed straight "
     "down its length from standing height: a painted green dado running the full length of both "
     "walls, a row of identical closed flush doors down the right side with blank plates where "
     "the numbers would be, a hard vinyl floor holding a long reflection, and one bright window "
     "at the far end burning out to white. Nobody is in the corridor",
     "door numbers, name plates with words, directory boards, exit signage, notices on the walls, "
     "person in frame",
     "Then it lists what it did, and the list is worth reading.",
     "ACT_3 — the regulator, from inside"),

    ("R116",
     "A period adding machine standing on a grey steel office desk under one lamp, photographed "
     "close from a low three-quarter angle, a narrow paper till roll feeding up out of the top of "
     "it and curling over the edge of the desk toward the floor in one long loose fall, the "
     "printing on the roll reduced by focus to a soft grey stipple with no figure, column or "
     "character resolving anywhere along it. The desk is otherwise bare",
     "legible numbers, digits on the roll, printed figures, columns of numerals, keys with "
     "numerals, brand name on the machine, nameplate, person in frame",
     "It counts deaths, and it prices them.",
     "ACT_4 — the money, kept abstract (⛔-15: no document facsimile)"),

    ("R117",
     "Rain running down the side window glass of a stationary car, photographed from inside the "
     "car at seat height with the glass filling the frame, the water breaking into long vertical "
     "runs and beads, the world beyond the glass dissolved into soft flat grey with no shape, "
     "edge or object resolving in it. The interior is dark vinyl and hard plastic of the early "
     "1970s, the car is not moving and nobody is in it",
     "readable signage beyond the glass, buildings, other vehicles, headlights, wipers in motion, "
     "person in frame, reflection of a face",
     "Almost nobody will notice what the table is about.",
     "ENDING — one of the film's designed silences"),
]

PINTO_THUMBS: list[tuple[str, str, str, str, str]] = [
    ("T001",
     "Eight sheets of typed paper fanned out across a grey steel office desk, photographed from a "
     "steep oblique angle from just above the near edge of the desk SO THE WHOLE FAN OF PAPER "
     "SITS IN THE LOWER 60 PERCENT OF THE FRAME, one hard directional work lamp raking across it "
     "from the left so the paper is markedly brighter than anything behind it and throws crisp "
     "shadows, a plain steel paper clip on the top sheet. The typing is visible only as an even "
     "grey ribbed texture at that angle and NOT ONE WORD, NUMBER, LINE OR LETTERFORM RESOLVES "
     "ANYWHERE. The bright bare desk top runs across the bottom third and is the brightest part "
     "of the picture. THE ENTIRE UPPER 40 PERCENT OF THE FRAME IS ONE UNBROKEN FIELD of plain "
     "out-of-focus dark office with no object, no edge and no detail crossing it anywhere",
     "legible typing, readable words on a page, letterforms, typed lines, printed paragraph, "
     "letterhead, margins with page numbers, stamp with words, signature, hand, person in frame, "
     "object in the top of the frame, low contrast, dull flat lighting, dark subject, "
     "detail crossing the top of the frame",
     "packaging variant 1 — WRONG MEMO / IT WAS ROLLOVER",
     "PACKAGING §2 variant 1"),

    ("T002",
     "The same fan of eight typed sheets on the same bare grey steel desk, closer and from a "
     "lower angle almost level with the desk top: the near edges of the paper make one strong "
     "bright horizontal band across the lower third of the frame, one hard key light from the "
     "left rakes along them, and the plain steel paper clip catches a specular highlight. At this "
     "angle the typing is pure grey texture and NOT ONE CHARACTER IS READABLE. The picture is "
     "bright and high contrast throughout the lower 60 percent, and THE ENTIRE UPPER 40 PERCENT "
     "IS ONE UNBROKEN FIELD of plain out-of-focus darkness with nothing in it at all",
     "legible typing, readable words on a page, letterforms, typed lines, printed paragraph, "
     "letterhead, stamp with words, signature, hand, person in frame, object in the top of the "
     "frame, low contrast, dull flat lighting, dark subject, detail crossing the top of the frame",
     "packaging variant 1 — second framing",
     "PACKAGING §2 variant 1"),

    ("T003",
     "The underbody of an early-1970s American subcompact hatchback raised high on a workshop "
     "lift, photographed from twelve feet away at standing height so THE WHOLE UNDERBODY RUNS AS "
     "ONE BRIGHT BAND ACROSS THE LOWER 60 PERCENT OF THE FRAME: the rear axle and the differential "
     "housing on the left, the flat forward face of the tank shell on the right, and a plain "
     "unmarked steel machinist's rule laid horizontally across the narrow gap between them, its "
     "graduations too fine and too oblique to read. One hard shop light from below and to the "
     "left makes the metal markedly brighter than anything behind it, and the bright swept "
     "concrete floor runs across the bottom third. THE ENTIRE UPPER 40 PERCENT IS ONE UNBROKEN "
     "FIELD of plain dark out-of-focus shop with nothing crossing it. The car is undamaged, "
     "carries no badge, no emblem, no wordmark, no nameplate and no plate of any kind, and there "
     "is no fire, no smoke, no scorching and no liquid anywhere in the picture",
     "licence plate, registration plate, number plate, badge on the grille, oval emblem, "
     "manufacturer wordmark, chrome nameplate, shop signage, readable markings on the rule, "
     "fire, flame, smoke, scorch marks, fuel spill, crumpled bodywork, hand, person in frame, "
     "object in the top of the frame, low contrast, dull flat lighting, dark subject, "
     "detail crossing the top of the frame",
     "packaging variant 2 — 9 INCHES / CRUSH SPACE",
     "PACKAGING §2 variant 2"),

    ("T004",
     "The same raised underbody and the same plain unmarked steel machinist's rule laid across "
     "the gap between the differential housing and the flat face of the tank shell, now closer "
     "and tighter so the housing, the gap and the rule fill the lower half of the frame and read "
     "large, one hard shop light from below and to the left putting a bright specular edge along "
     "the rule and the machined faces. The bright concrete floor is just visible along the bottom "
     "edge and is the brightest thing in the picture. THE ENTIRE UPPER 40 PERCENT IS ONE UNBROKEN "
     "FIELD of plain dark out-of-focus shop. No badge, no emblem, no wordmark, no nameplate, no "
     "plate, no readable graduation on the rule, and no fire, smoke, scorching or liquid anywhere",
     "licence plate, registration plate, number plate, badge on the grille, oval emblem, "
     "manufacturer wordmark, chrome nameplate, readable markings on the rule, fire, flame, smoke, "
     "scorch marks, fuel spill, crumpled bodywork, hand, person in frame, object in the top of "
     "the frame, low contrast, dull flat lighting, dark subject, "
     "detail crossing the top of the frame",
     "packaging variant 2 — second framing",
     "PACKAGING §2 variant 2"),

    ("T005",
     "A single unbadged early-1970s American subcompact hatchback standing stopped and alone in "
     "the middle lane of a wide dry three-lane freeway at midday, photographed from a fixed high "
     "vantage on a road overbridge looking down and along the carriageway, THE CAR AND THE ROAD "
     "FILLING THE LOWER 60 PERCENT OF THE FRAME with the car small and central in it. Hard "
     "overhead sun makes the pale concrete and the car roof markedly brighter than everything "
     "else, and the bright empty asphalt runs across the bottom third. Dry Southern Californian "
     "scrub along the shoulder, both other lanes completely empty, no other vehicle anywhere. "
     "Nobody is in or near the car, it is undamaged, and it carries no badge, no emblem, no "
     "wordmark, no nameplate and no plate of any kind. THE ENTIRE UPPER 40 PERCENT OF THE FRAME "
     "IS ONE UNBROKEN FIELD of flat white overexposed sky with no cloud, no horizon line, no "
     "gantry, no pole and no detail crossing it anywhere",
     "licence plate, registration plate, number plate, badge on the grille, oval emblem, "
     "manufacturer wordmark, chrome nameplate, other vehicles, traffic, road signs, gantry, "
     "overhead structure, billboards, crumpled bodywork, fire, flame, smoke, person in frame, "
     "object in the top of the frame, horizon crossing the top of the frame, low contrast, "
     "dull flat lighting, dark subject",
     "packaging variant 3 — 500 OR 27 / NHTSA, MAY 1978",
     "PACKAGING §2 variant 3"),

    ("T006",
     "The same unbadged early-1970s American subcompact hatchback standing stopped and alone in "
     "the middle lane of the same wide dry three-lane freeway at midday, now seen from lower and "
     "closer on the same overbridge so the car reads larger from behind and the two empty lanes "
     "spread away on either side of it, all of it inside the lower 60 percent of the frame. Hard "
     "overhead sun, high contrast, the bright pale concrete across the bottom third the brightest "
     "part of the picture, dry scrub at the shoulder. No other vehicle anywhere, nobody in or near "
     "the car, no damage, and no badge, emblem, wordmark, nameplate or plate of any kind. THE "
     "ENTIRE UPPER 40 PERCENT IS ONE UNBROKEN FIELD of flat white overexposed sky with nothing "
     "crossing it",
     "licence plate, registration plate, number plate, badge on the grille, oval emblem, "
     "manufacturer wordmark, chrome nameplate, other vehicles, traffic, road signs, gantry, "
     "overhead structure, billboards, crumpled bodywork, fire, flame, smoke, person in frame, "
     "object in the top of the frame, horizon crossing the top of the frame, low contrast, "
     "dull flat lighting, dark subject",
     "packaging variant 3 — second framing",
     "PACKAGING §2 variant 3"),
]

HYATT_HEADROOM: list[tuple[str, str, str, str, str]] = [
    ("H114",
     "One long length of threaded steel rod about an inch and a quarter across lying diagonally "
     "across a dark oiled workbench, photographed from directly above with a hard raking light "
     "running along the thread so every turn stands out, a plain hand hacksaw lying beside it "
     "with its blade clear of the rod and not touching it. Nothing else is on the bench and "
     "nobody is in the frame",
     "cut rod, sawn end, swarf on the blade, sparks, brand name on the saw, stamped markings on "
     "the rod, person in frame, hands",
     "One long steel rod becomes two shorter ones, four inches apart.",
     "ACT_2 — the change, shown as tool and stock, never as an act"),

    ("H115",
     "The upper face of a short length of hollow rectangular steel box section lying on a "
     "fabricator's bench, photographed from directly above and close so the section runs across "
     "the frame, TWO ROUND HOLES DRILLED THROUGH IT A SHORT DISTANCE APART near the middle of its "
     "length, bright curls of fresh swarf lying around each hole and a light film of cutting oil "
     "on the steel. One hard side light rakes across the surface. No writing, no marking-out "
     "lines with figures, nobody in the frame",
     "dimension callouts, figures written on the steel, marking-out numerals, stamped part "
     "numbers, drawing title block, person in frame, hands",
     "Two walkways will hang from that detail",
     "ACT_2 — the two holes, four inches apart (FN-02)"),

    ("H116",
     "A hotel lift landing of about 1980, empty: two sets of brushed bronze lift doors closed in "
     "a travertine-clad wall, a low bench opposite them, a shallow planter of foliage, warm "
     "downlighters in a plain plaster soffit, tan stone floor holding a soft reflection. "
     "Photographed straight on from standing height. There is no signage, no floor indicator "
     "lettering and no numeral anywhere, and nobody is present",
     "floor numbers, lift indicator numerals, directional signage, hotel branding, logos, "
     "person in frame, crowd",
     "Between fifteen hundred and two thousand area residents chose to escape the heat at the "
     "hotel's tea dance",
     "ACT_3 — the building, an hour before, with nobody in it (EV-04, ⛔-12)"),

    ("H117",
     "A hotel kitchen pass of about 1980, empty and clean: a long stainless steel counter running "
     "across the frame with a row of identical plain white plates stacked on it under a strip of "
     "warm heat lamps, quarry-tiled floor, stainless shelving behind, everything wiped down and "
     "still. Photographed from the service side at standing height. Nobody is present and no "
     "label, ticket or board carries any writing",
     "order tickets with writing, menu boards, labels, brand names on equipment, person in frame, "
     "crowd, food service in progress",
     "a weekly event with big band music and a dance contest",
     "ACT_3 — the evening, from the side nobody watched (EV-04)"),

    ("H118",
     "A low travertine fountain basin in a large open hotel interior, photographed from standing "
     "height at close range so the basin edge runs across the lower half of the frame, the water "
     "flat and still with the jet off, warm afternoon daylight coming down from a glazed roof far "
     "above and lying in one broad soft band across the surface, planting boxes soft behind. "
     "Nobody is in the frame and nothing in it identifies any particular building",
     "hotel branding, logos, signage, plaques, coins in the water, person in frame, crowd, "
     "recognisable real building",
     "Crowd in atrium area is estimated at fifteen hundred to two thousand",
     "ACT_3 — the atrium at rest, an hour before (EV-05, ⛔-12)"),

    ("H119",
     "A heavy steel load cell and a large shackle hanging on a chain in a high-roofed testing "
     "hall, photographed close from below against the dark roof structure so the cell fills the "
     "middle of the frame, its cable running away out of the top of the shot, one hard light "
     "from the side picking out the machined steel and the pin. Nobody is in the frame and the "
     "cell carries no dial face, no scale and no lettering",
     "digits on a display, dial with numerals, calibration plate with figures, brand name, "
     "person in frame, rubble, debris",
     "Permission to weigh the spans and to cut specimens out of them came later, by court order",
     "ACT_4 — weighing, by court order (ID-06)"),

    ("H120",
     "A photographic copy stand in a laboratory of the early 1980s: a plain flat baseboard with a "
     "vertical column behind it, a large-format camera mounted on the column looking straight "
     "down, two adjustable lamps angled onto the board from either side and switched on, and the "
     "board completely empty. Photographed three-quarter from standing height in an otherwise "
     "dim room. Nobody is present",
     "documents on the board, printed pages, photographs of anything, brand name on the camera, "
     "scale bars with numerals, person in frame",
     "their involvement was limited by court order to visual and photographic observations",
     "ACT_4 — what the investigators were allowed to do first (ID-06)"),

    ("H121",
     "A hardbound laboratory notebook lying open on a wooden bench under flat north light, "
     "photographed from directly above so both pages fill the frame, BOTH PAGES COMPLETELY BLANK "
     "with only a faint printed ruling across them, a plain pencil lying across the gutter and a "
     "steel rule along the outer edge of the right-hand page. Nothing else on the bench, nobody "
     "in the frame",
     "handwriting, figures, sketches, printed page numbers, printed headings, readable ruling "
     "labels, person in frame",
     "Efforts to obtain copies of the structural design calculations, the report says, were "
     "unsuccessful.",
     "ACT_4 — the calculations that do not exist in the record"),

    ("H122",
     "A bench-mounted hardness tester of the early 1980s: a heavy cast column and an anvil with a "
     "short steel offcut sitting on it, photographed close from a low three-quarter angle in a "
     "laboratory, one hard light from the right putting a bright edge along the cast housing and "
     "the machined anvil. The instrument's dial is turned away from the camera and no face, "
     "scale or figure is visible anywhere. Nobody is in the frame",
     "dial with numerals, gauge face, digits, calibration plate, brand name, nameplate, "
     "person in frame",
     "and to cut specimens out of them came later, by court order",
     "ACT_4 — the metallurgy (ID-06)"),

    ("H123",
     "A small windowless anteroom outside a hearing room in a plain American public building of "
     "the middle 1980s: four grey stacking chairs standing in a row against a bare painted wall, "
     "an empty coat rail on the opposite wall, a hard vinyl floor, one recessed fluorescent panel "
     "in the ceiling. Photographed straight on from standing height. Nobody is present, and there "
     "is no notice, no sign and no lettering anywhere in the room",
     "notices on the wall, room numbers, name plates, directory boards, seals, person in frame, "
     "courtroom interior, gavel, judge's bench",
     "the Commission conducted twenty-seven days of hearing",
     "ACT_5 — outside the room, twenty-seven times (DC-01)"),

    ("H124",
     "A plain government-issue steel office desk photographed from directly above under flat "
     "north light, the desk top otherwise completely bare, with ONE CLOSED PLAIN MANILA FOLDER "
     "lying square in the middle of it and nothing else at all — no pen, no paper, no telephone. "
     "The folder's tab is blank. Nobody is in the frame",
     "writing on the tab, labels, printed forms, readable documents, seals, person in frame",
     "no one had yet taken responsibility for the collapse",
     "ACT_5 — the file, closed (DC-22)"),

    ("H125",
     "A plain institutional wall clock hanging on a bare painted wall in an empty room, "
     "photographed slightly from below with a long lens so the clock fills the middle of the "
     "frame against flat wall, its face plain white with ONLY BARE TICK MARKS AROUND THE EDGE AND "
     "NO NUMERALS ANYWHERE ON IT, two plain black hands, a plain chrome bezel. Flat daylight from "
     "the left. Nobody is in the frame",
     "numerals on the dial, digits, brand name on the face, maker's mark, lettering, "
     "person in frame",
     "It was filed on the fifteenth of November, 1985.",
     "ACT_5 — time, with the numbers taken off (DC-03)"),

    ("H126",
     "Five identical plain cardboard document boxes with their lids on, stacked two and three "
     "high in the corner of a bare office of the middle 1980s, photographed from standing height "
     "at a shallow angle, one overhead fluorescent panel above them, a hard vinyl floor and plain "
     "painted walls. Every box is completely unmarked — no label, no writing, no number. Nobody "
     "is in the frame",
     "labels with writing, box numbers, case numbers, handwriting on cardboard, seals, "
     "person in frame",
     "Its decision runs four hundred and forty-two pages.",
     "ACT_5 — the record, boxed (DC-02)"),

    ("H127",
     "A very large empty interior atrium in an American building of about 1980 at first light, "
     "photographed from the floor at standing height at one end: pale tan travertine running away "
     "from the camera and still wet from cleaning so it holds one long soft reflection of the "
     "glazed roof five storeys above, the daylight cold and even, planting boxes dark at the "
     "edges. Nobody is present, nothing crosses the space overhead, and nothing in the picture "
     "identifies any particular building",
     "walkways, bridges overhead, suspended structures, hotel branding, logos, signage, "
     "person in frame, crowd, rubble, debris, recognisable real building",
     "One hundred and fourteen people went to a tea dance and did not come home.",
     "ENDING — the room, afterwards (⛔-12, ⛔-14)"),
]

HYATT_THUMBS: list[tuple[str, str, str, str, str]] = [
    ("T001",
     "TWO LENGTHS OF THREADED STEEL ROD about an inch and a quarter across lying side by side on "
     "a dark oiled workbench, ONE LONG AND ONE ROUGHLY HALF ITS LENGTH, with a plain heavy "
     "hexagonal steel nut and one flat round steel washer lying beside them, photographed from "
     "just above the bench at a shallow angle SO ALL OF IT SITS IN THE LOWER 60 PERCENT OF THE "
     "FRAME. One hard directional key light from the left runs along the thread so every turn "
     "stands out and the steel is markedly brighter than anything behind it. The bright bare "
     "bench top runs across the bottom third and is the brightest part of the picture. THE ENTIRE "
     "UPPER 40 PERCENT OF THE FRAME IS ONE UNBROKEN FIELD of plain dark out-of-focus workshop "
     "with no object, no edge and no detail crossing it anywhere",
     "stamped markings on the rod, size markings, grade markings, brand name, dimension "
     "callouts, hand, person in frame, rust, object in the top of the frame, low contrast, "
     "dull flat lighting, dark subject, detail crossing the top of the frame",
     "packaging variant 1 — ONE ROD / TWO RODS · SAME STEEL",
     "PACKAGING §2 variant 1"),

    ("T002",
     "The same two lengths of threaded steel rod, one long and one roughly half its length, lying "
     "side by side on the same dark oiled bench with the same plain nut and flat washer beside "
     "them, now closer and from a lower angle almost level with the bench top so the near ends of "
     "the rods read large across the lower third of the frame and the thread catches one hard key "
     "light from the left as a row of bright specular ridges. High contrast, bright exposure, the "
     "bench top the brightest thing in the picture. THE ENTIRE UPPER 40 PERCENT IS ONE UNBROKEN "
     "FIELD of plain dark out-of-focus workshop with nothing in it at all",
     "stamped markings on the rod, size markings, grade markings, brand name, dimension "
     "callouts, hand, person in frame, rust, object in the top of the frame, low contrast, "
     "dull flat lighting, dark subject, detail crossing the top of the frame",
     "packaging variant 1 — second framing",
     "PACKAGING §2 variant 1"),

    ("T003",
     "A SINGLE THREADED STEEL ROD about an inch and a quarter across PASSING DOWN THROUGH A ROUND "
     "HOLE IN THE FLAT WEB OF A HOLLOW RECTANGULAR STEEL BOX SECTION, with a flat round washer and "
     "a heavy hexagonal nut bearing up against the underside of the web, photographed close and "
     "slightly from below SO THE WHOLE ASSEMBLY SITS IN THE LOWER 60 PERCENT OF THE FRAME. One "
     "hard directional shop light from the left makes the machined steel markedly brighter than "
     "anything behind it and lays a crisp shadow under the nut; the bright lower edge of the box "
     "section runs across the bottom third and is the brightest part of the picture. Clean bright "
     "steel, no rust, no damage, no deformation. THE ENTIRE UPPER 40 PERCENT IS ONE UNBROKEN "
     "FIELD of plain dark out-of-focus shop with nothing crossing it",
     "stamped markings, grade markings, dimension callouts, brand name, rust, bent metal, "
     "torn steel, hand, person in frame, object in the top of the frame, low contrast, "
     "dull flat lighting, dark subject, detail crossing the top of the frame",
     "packaging variant 2 — A NUT AND / A WASHER · 114 PEOPLE",
     "PACKAGING §2 variant 2"),

    ("T004",
     "The same single threaded steel rod passing down through the same round hole in the flat web "
     "of the same hollow rectangular steel box section, the same flat washer and heavy hexagonal "
     "nut bearing up against the underside, now tighter and squarer on so the washer and the nut "
     "fill the lower half of the frame and the machined faces read large. One hard key light from "
     "the left, high contrast, bright exposure, the bright underside of the section running "
     "across the bottom third. Clean bright steel, no rust, no deformation. THE ENTIRE UPPER 40 "
     "PERCENT IS ONE UNBROKEN FIELD of plain dark out-of-focus shop",
     "stamped markings, grade markings, dimension callouts, brand name, rust, bent metal, "
     "torn steel, hand, person in frame, object in the top of the frame, low contrast, "
     "dull flat lighting, dark subject, detail crossing the top of the frame",
     "packaging variant 2 — second framing",
     "PACKAGING §2 variant 2"),

    ("T005",
     "A large tilted drafting board with a big sheet of plain vellum pinned flat across it and a "
     "long parallel rule lying square on the sheet, one plain pencil resting on the bottom edge "
     "of the board and a wooden stool pushed back from it and empty, photographed from standing "
     "height at a shallow angle SO THE BOARD AND THE STOOL SIT IN THE LOWER 60 PERCENT OF THE "
     "FRAME. THE SHEET IS COMPLETELY BLANK: an unbroken field of pale vellum with no line, no "
     "drawing, no ruling, no figure and no mark of any kind on it. ONE HARD DIRECTIONAL KEY LIGHT "
     "from the left makes the sheet the brightest object in the picture and lays a crisp shadow "
     "from the parallel rule across it; the bottom edge of the board is bright and is the "
     "brightest part of the frame. THE ENTIRE UPPER 40 PERCENT OF THE FRAME IS ONE UNBROKEN FIELD "
     "of plain dark out-of-focus drawing office with no object, no edge and no detail crossing it",
     "lines on the sheet, drawing, dimension callouts, drawing title block, figures, handwriting, "
     "printed grid, stamps, hand, person in frame, object in the top of the frame, low contrast, "
     "dull flat lighting, dark subject, detail crossing the top of the frame",
     "packaging variant 3 — NEVER / CALCULATED · NOBODY CHECKED",
     "PACKAGING §2 variant 3 — the packaging's 'low tungsten light' is the FILM-FRAME register "
     "and is deliberately overridden here; see the [TSTYLE] note"),

    ("T006",
     "The same tilted drafting board with the same completely blank sheet of pale vellum pinned "
     "across it and the same long parallel rule lying square on it, now closer and from a lower "
     "angle almost level with the board so the near edge of the board makes one strong bright "
     "horizontal across the lower third of the frame and the blank sheet rises away from it, one "
     "plain pencil in the near corner. THE SHEET IS COMPLETELY BLANK — no line, no drawing, no "
     "figure, no mark. One hard key light from the left, high contrast, bright exposure, the "
     "sheet markedly brighter than everything behind it. THE ENTIRE UPPER 40 PERCENT IS ONE "
     "UNBROKEN FIELD of plain dark out-of-focus drawing office with nothing in it",
     "lines on the sheet, drawing, dimension callouts, drawing title block, figures, handwriting, "
     "printed grid, stamps, hand, person in frame, object in the top of the frame, low contrast, "
     "dull flat lighting, dark subject, detail crossing the top of the frame",
     "packaging variant 3 — second framing",
     "PACKAGING §2 variant 3"),
]


# =============================================================================================
# episodes
# =============================================================================================
def tstyle_for(setting_clause: str) -> str:
    """EP67's thumbnail style with only the setting clause swapped.

    Kept word for word otherwise, because it is the block that produced EP67's six thumbnail
    candidates after EP65's four came back as dull grey paper under the canonical low-contrast
    [STYLE].
    """
    return (
        "editorial photographic still made to be a video thumbnail, ONE HARD DIRECTIONAL KEY "
        "LIGHT from the side, HIGH CONTRAST AND BRIGHT OVERALL EXPOSURE, the subject clearly "
        "brighter than everything behind it and cleanly separated from it, shadow only where it "
        "defines an edge and never filling the frame, THE ENTIRE UPPER 40 PERCENT OF THE FRAME IS "
        "ONE UNBROKEN UNIFORM FIELD - plain wall, plain sky or plain out-of-focus darkness, with "
        "no object, no edge, no horizon and no detail crossing it anywhere - and the whole "
        f"subject sits inside the lower 60 percent with the bottom third the brightest part of "
        f"the picture, {setting_clause}, ultra-detailed, photoreal, 4K, 16:9, no text, no "
        "lettering, no numerals, no watermark, no logo, no signage")


EPISODES: dict[str, dict] = {
    "pinto": {
        "num": 68,
        "title": "EP68 · THE FORD PINTO / *GRIMSHAW v. FORD*",
        "prefix": "R",
        "save_dir": r"E:\pd-media\assets\ai\pinto",
        "headroom": PINTO_HEADROOM,
        "thumbs": PINTO_THUMBS,
        "tstyle_setting": "the United States between 1968 and 1981",
        "headroom_title": "B1 · headroom — ordered, NOT declared",
        "thumb_title": "T · THUMBNAIL PLATES  [TSTYLE]",
        "supersedes": ("§7 of `EP68_pinto_CODEX_BATCH_A.v001.md` sketched an optional batch B at "
                       "`R105`–`R140` to be commissioned **after** the first assembly. That plan "
                       "is superseded: a thin pool discovered after assembly costs a rebuild, and "
                       "the ids used here stay inside the range it reserved, so nothing collides."),
    },
    "hyatt": {
        "num": 69,
        "title": "EP69 · THE HYATT REGENCY WALKWAYS",
        "prefix": "H",
        "save_dir": r"E:\pd-media\assets\ai\hyatt",
        "headroom": HYATT_HEADROOM,
        "thumbs": HYATT_THUMBS,
        "tstyle_setting": "the American Midwest between 1978 and 1988",
        "headroom_title": "B1 · headroom — ordered, NOT declared",
        "thumb_title": "T · THUMBNAIL PLATES  [TSTYLE]",
        "supersedes": ("§8 of `EP69_hyatt_CODEX_BATCH_A.v001.md` said the three thumbnail plates "
                       "would be commissioned later 'with the same `[STYLE]`/`[NEG]`'. The `[NEG]` "
                       "is indeed unchanged. The `[STYLE]` is NOT: the canonical one mandates low "
                       "contrast, which is precisely why EP65's four candidates came back dull and "
                       "had to be re-ordered."),
    },
}


# =============================================================================================
# derivation
# =============================================================================================
def derivations() -> dict[str, dict]:
    """Re-derive the headroom count per episode against the spec and the film builder's solver."""
    import json
    import build_case_film_generic as B

    out: dict[str, dict] = {}
    for slug in EPISODES:
        specp = next((ROOT / "episodes").glob(f"PD-*-{slug}/episode_spec.v001.json"))
        spec = json.loads(specp.read_text(encoding="utf-8"))
        declared = len(spec["mandatory_stills"])
        dv = spec["distinct_video_assets"]
        tc = spec["target_cut_sec"]
        B.TARGET_CUT_SEC = tc
        # still pool left unbounded (999) so the CEILING shows itself rather than the pool size
        solved = {}
        for words in spec["script_words"]:
            for wpm in (169.7, 159.5):
                solved[(words, wpm)] = B.solve_totals(60 * words / wpm, dv, 0, 999)
        ceiling = math.floor(dv * (1 - B.MIN_VIDEO_SHARE) / B.MIN_VIDEO_SHARE)
        need_rf = math.ceil(declared / (1 - REJECT_AND_FLAG))
        need_r = math.ceil(declared / (1 - REJECT_ONLY))
        out[slug] = {
            "declared": declared, "distinct_video_assets": dv, "target_cut_sec": tc,
            "solver": solved, "still_ceiling": ceiling,
            "need_reject_only": need_r, "need_reject_and_flag": need_rf,
            "headroom": need_rf - declared,
            "thumbs": THUMBS_PER_EPISODE,
            "ordered": need_rf + THUMBS_PER_EPISODE,
            "thumbnail_candidates_min": spec.get("thumbnail_candidates_min"),
        }
    return out


def print_derivation(d: dict[str, dict]) -> None:
    print(f"EP66 batch C, the only measured plate-rejection rate this channel has: "
          f"{EP66_ORDERED} ordered, {EP66_REJECT} REJECT ({REJECT_ONLY*100:.1f}%), "
          f"{EP66_FLAG} FLAG -> {REJECT_AND_FLAG*100:.1f}% combined\n")
    for slug, r in d.items():
        print(f"--- {slug}")
        print(f"    declared mandatory_stills            {r['declared']}")
        print(f"    distinct_video_assets                {r['distinct_video_assets']}   "
              f"target_cut_sec {r['target_cut_sec']}")
        vals = {v[2] for v in r["solver"].values()}
        print(f"    solve_totals still-cut ceiling       {sorted(vals)} across the declared "
              f"word x pace band (flat)")
        print(f"      = floor(video x 0.32 / 0.68)       {r['still_ceiling']}")
        print(f"    {r['declared']} / (1 - {REJECT_ONLY:.3f})  hard rejects only      "
              f"= {r['need_reject_only']}")
        print(f"    {r['declared']} / (1 - {REJECT_AND_FLAG:.3f})  rejects + flags       "
              f"= {r['need_reject_and_flag']}")
        print(f"    HEADROOM  {r['need_reject_and_flag']} - {r['declared']} = {r['headroom']}   "
              f"(ordered, NOT declared)")
        print(f"    THUMBS    {r['thumbs']}   (spec thumbnail_candidates_min "
              f"{r['thumbnail_candidates_min']}; three packaging variants x 2 framings)")
        print(f"    ORDERED   {r['declared']} + {r['headroom']} + {r['thumbs']} = {r['ordered']}")
        if r["need_reject_and_flag"] > r["still_ceiling"]:
            print(f"    note: the ordered content total {r['need_reject_and_flag']} EXCEEDS the "
                  f"still ceiling {r['still_ceiling']}; the surplus is pure rejection cover.")
        else:
            print(f"    note: the still ceiling is {r['still_ceiling']}, "
                  f"{r['still_ceiling'] - r['declared']} above the declared count. If the spec is "
                  f"ever re-declared upward after the measured VO, re-run this derivation.")
        print()


# =============================================================================================
# emit
# =============================================================================================
def prompt_line(body: str, neg_add: str, thumb: bool) -> str:
    tail = "[TSTYLE]" if thumb else "[STYLE]"
    return f"{body} {tail} Avoid: [NEG], {neg_add}"


def chunks(seq: list, n: int) -> list[list]:
    return [seq[i:i + n] for i in range(0, len(seq), n)]


def build(slug: str) -> dict[str, str]:
    ep = EPISODES[slug]
    pdir = PLANNING / f"EP{ep['num']}_{slug}_CODEX_PASTE_A"
    doc_a = PLANNING / f"EP{ep['num']}_{slug}_CODEX_BATCH_A.v001.md"

    batch_files = sorted(pdir.glob("batch_*.txt"))
    if not batch_files:
        raise SystemExit(f"no batch_*.txt in {pdir}")
    first = batch_files[0].read_text(encoding="utf-8")
    STYLE = _after_marker(first, STYLE_MARK)
    NEG = _after_marker(first, NEG_MARK)
    RULES = _rules_block(first)

    declared: list[tuple[str, str]] = []
    for f in batch_files:
        declared += parse_prompts(f.read_text(encoding="utf-8"))
    HSTYLE = hstyle_of([f.read_text(encoding="utf-8") for f in batch_files], declared)
    if not HSTYLE or HSTYLE.strip() == "[HSTYLE]":
        raise SystemExit(f"{slug}: could not read the [HSTYLE] preamble out of the paste files")

    # --- the refusals, before a byte is written -------------------------------------------
    doc_neg = neg_from_doc(doc_a)
    if NEG != doc_neg:
        raise SystemExit(f"{slug}: the [NEG] in the paste files and the [NEG] in {doc_a.name} are "
                         f"NOT byte-identical ({len(NEG)} vs {len(doc_neg)} chars)")
    low = NEG.lower()
    missing = [t for t in REQUIRED_IN_NEG if t not in low]
    if missing:
        raise SystemExit(f"{slug}: [NEG] is missing identifiability token(s): {missing}")
    back = [t for t in BANNED_IN_NEG if t in low]
    if back:
        raise SystemExit(f"{slug}: [NEG] has re-acquired {back} -- these three suppressed the "
                         f"people lane and cost EP66 a 191-plate rebuild")

    TSTYLE = tstyle_for(ep["tstyle_setting"])
    files: dict[str, str] = {}

    # --- paste files for the new tiers ------------------------------------------------------
    def common(tier: str) -> list[str]:
        L = ["──────── 全プロンプト共通の指定 ────────", ""]
        if tier == "thumb":
            L += ["各プロンプト末尾の [TSTYLE] は、次の文言に置き換えてください:", "", TSTYLE, "",
                  "★この6枚は**サムネイル専用**です。本編カットの [STYLE]（低コントラスト）は使いません。",
                  "　硬い一灯・高コントラスト・明るい露出。**画面の上40%は何も無い一様な面**にしてください。",
                  "　見出し文字を焼き込む場所です。被写体は下60%に収め、下1/3を一番明るくします。", ""]
        else:
            L += ["各プロンプト末尾の [STYLE] は、次の文言に置き換えてください:", "", STYLE, ""]
        L += ["各プロンプト末尾の Avoid: [NEG] は、次の文言に置き換えてください:", "", NEG, "",
              "★[NEG] の後ろに「, ○○, ○○」と語が続いています（全プロンプト）。",
              "　その場合は、上の文言をすべて展開したうえで、その末尾にその語をそのまま足してください。",
              "　上の文言からは1語も削らないでください。**サムネイルでも [NEG] は変えません。**", ""]
        return L

    def render(idx: int, total: int, rows: list, tier: str) -> str:
        L: list[str] = []
        a = L.append
        tag = "予備バッチ" if tier == "headroom" else "**サムネイル**バッチ"
        title = ep["headroom_title"] if tier == "headroom" else ep["thumb_title"]
        a(f"EP{ep['num']} {slug} — 画像発注 {tag} {idx}/{total}（{len(rows)}枚）")
        a(f"区分: {title}  [{rows[0][0]} – {rows[-1][0]}]")
        a("")
        if tier == "headroom":
            a("★これは**予備**です。**生成してください。**本編の契約（mandatory_stills）には入って")
            a("　いませんが、却下が出たときの差し替えと、ナレーションが伸びた場合の不足に備えます。")
        else:
            a("★これは**サムネイル用**です。**動画のカットには一切使いません。**")
            a("　この6枚だけ [STYLE] ではなく **[TSTYLE]** を使います（下記）。**[NEG] は変えません。**")
        a("　新しい ID を作らない。`_v2` / `_02` / `_A` を作らない。**名前は上の■のとおりちょうど。**")
        a("")
        a("以下を1枚ずつ生成してください。**1プロンプト＝1枚**です。")
        a("複数のプロンプトをまとめて1枚にしないでください。同じプロンプトで2枚目を作らないでください。")
        a("")
        L += common(tier)
        L += RULES
        # The 絶対条件 block is lifted verbatim from batch_01 and may name continuity pairs that
        # live in OTHER files. Say so rather than leave a reader wondering, and name the pairs
        # that are actually in THIS file.
        a("★上の絶対条件は本編バッチから一字も変えずに引き写したものです。そこに出てくる")
        a("　プロンプト ID は本編のもので、このファイルには入っていません。")
        if tier == "thumb":
            pairs = " / ".join(f"{rows[i][0]}+{rows[i+1][0]}"
                               for i in range(0, len(rows) - 1, 2))
            a(f"★このファイルの中では {pairs} がそれぞれ同一シーンの2カットです。")
            a("　各ペアは同じ被写体・同じ場所で、アングルと距離だけを変えてください。")
            a("　ただし各プロンプトは単独で完結して書いてあります。")
        a("")
        a("──────── プロンプト ────────")
        a("")
        for pid, body, neg_add, _line, _ledg in rows:
            a(f"■ {pid}.png")
            a(prompt_line(body, neg_add, tier == "thumb"))
            a("")
        a("──────── 保存 ────────")
        a("")
        a(f"生成した画像は上の ■ の名前（このファイルは {rows[0][0]}.png 〜 {rows[-1][0]}.png）で")
        a("保存してください。**他のバッチの ID を使わないこと。**")
        a(f"保存先 {ep['save_dir']}\\")
        a("長辺 3840px 以上・16:9・PNG。")
        return "\n".join(L) + "\n"

    hgroups = chunks(ep["headroom"], HEADROOM_CHUNK)
    for i, rows in enumerate(hgroups, 1):
        files[f"{pdir.name}/headroom_{i:02d}.txt"] = render(i, len(hgroups), rows, "headroom")
    tgroups = chunks(ep["thumbs"], THUMB_CHUNK)
    for i, rows in enumerate(tgroups, 1):
        files[f"{pdir.name}/thumbs_{i:02d}.txt"] = render(i, len(tgroups), rows, "thumb")

    # --- the merged single file -------------------------------------------------------------
    n_dec, n_hd, n_th = len(declared), len(ep["headroom"]), len(ep["thumbs"])
    M: list[str] = []
    a = M.append
    a(f"EP{ep['num']} {slug} — 画像発注 **統合版・全 {n_dec + n_hd + n_th} 枚**")
    a(f"区分: 本編 {declared[0][0]} – {declared[-1][0]}（{n_dec}枚・契約） ／ "
      f"予備 {ep['headroom'][0][0]}.png – {ep['headroom'][-1][0]}.png（{n_hd}枚・契約外） ／ "
      f"サムネ {ep['thumbs'][0][0]}.png – {ep['thumbs'][-1][0]}.png（{n_th}枚・カットに使わない）")
    a("")
    a(f"★このファイル1本に**全 {n_dec + n_hd + n_th} 枚**が入っています。分割ファイルは同じ内容です。")
    a("　上から順に、**1プロンプト＝1枚**で生成してください。")
    a("　複数のプロンプトをまとめて1枚にしない。同じプロンプトで2枚目を作らない。")
    a("　新しい ID を作らない。`_v2` / `_02` / `_A` を作らない。**名前は ■ のとおりちょうど。**")
    a("")
    a("──────── 全プロンプト共通の指定 ────────")
    a("")
    a("各プロンプト末尾の [STYLE] は、次の文言に置き換えてください:")
    a("")
    a(STYLE)
    a("")
    a(f"★ただし **{ep['thumbs'][0][0]}.png 〜 {ep['thumbs'][-1][0]}.png の6枚だけ**は末尾が "
      f"[TSTYLE] です。")
    a("　その6枚は [STYLE] を使わず、次の文言に置き換えてください:")
    a("")
    a(TSTYLE)
    a("")
    a("　サムネイルは本編カットの低コントラストにしません。硬い一灯・高コントラスト・明るい露出、")
    a("　**画面の上40%は何も無い一様な面**（見出し文字を焼き込む場所）、被写体は下60%、下1/3が一番明るい。")
    a("")
    a("各プロンプト末尾の Avoid: [NEG] は、次の文言に置き換えてください:")
    a("")
    a(NEG)
    a("")
    a("★[NEG] の後ろに「, ○○, ○○」と語が続いているプロンプトがあります。")
    a("　その場合は、上の文言をすべて展開したうえで、その末尾にその語をそのまま足してください。")
    a("　上の文言からは1語も削らないでください。**サムネイルの6枚でも [NEG] は変えません。**")
    if HSTYLE:
        # Two episodes, two shapes, and getting this wrong would tell the generator to do the
        # opposite of what the prompt bodies need. Decided by MEASURING the bodies, not assumed:
        # if the preamble text is already inline in the body, nothing is substituted; if the body
        # carries only the bare token, it must be replaced.
        inline = any(HSTYLE in b for _, b in declared)
        a("")
        if inline:
            a("★[HSTYLE] で始まるプロンプトは人物レーンです。[HSTYLE] の中身はプロンプト本文に")
            a("　すでに書き込まれています。**置換は不要**で、そのまま使ってください。")
            a("　参考のため全文を再掲します:")
        else:
            a("★プロンプト冒頭の [HSTYLE] は人物レーンの印です。**次の文言に置き換えてください:**")
        a("")
        a(HSTYLE)
    a("")
    M += RULES
    a("──────── プロンプト ────────")
    a("")
    for pid, body in declared:
        a(f"■ {pid}")
        a(body)
        a("")
    for pid, body, neg_add, _l, _g in ep["headroom"]:
        a(f"■ {pid}.png")
        a(prompt_line(body, neg_add, False))
        a("")
    for pid, body, neg_add, _l, _g in ep["thumbs"]:
        a(f"■ {pid}.png")
        a(prompt_line(body, neg_add, True))
        a("")
    a("──────── 保存 ────────")
    a("")
    a("生成した画像は上の ■ の名前ちょうどで保存してください（このファイルは "
      f"{declared[0][0]} 〜 {ep['thumbs'][-1][0]}.png）。")
    a(f"保存先 {ep['save_dir']}\\")
    a("長辺 3840px 以上・16:9・PNG。")
    files[f"EP{ep['num']}_{slug}_CODEX_PASTE_ALL.txt"] = "\n".join(M) + "\n"

    # --- the batch B document ---------------------------------------------------------------
    d = derivations()[slug]
    D: list[str] = []
    a = D.append
    a(f"# {ep['title']} — IMAGE ORDER **BATCH B** (Codex) v001")
    a("")
    a(f"**Episode `PD-2026-0{ep['num']}-{slug}` · slug `{slug}` · 2026-08-11**")
    a("")
    a(f"> **What this adds.** Batch A ordered **{n_dec}** plates and nothing else. This adds the "
      f"two tiers it had no room for: **{n_hd} headroom plates** and **{n_th} thumbnail plates**. "
      f"Batch A is not edited and stays on disk (invariant 6); everything it says about policy, "
      f"era, the barred likenesses and the `[NEG]` still binds and is restated below.")
    a("")
    a("| tier | ids | count | in `episode_spec.mandatory_stills`? |")
    a("|---|---|---:|---|")
    a(f"| **1 · declared** | `{declared[0][0][:-4]}`–`{declared[-1][0][:-4]}` | **{n_dec}** | "
      f"**yes** — batch A, unchanged |")
    a(f"| **2 · headroom** | `{ep['headroom'][0][0]}`–`{ep['headroom'][-1][0]}` | **{n_hd}** | "
      f"**no** — cover against rejections and against the script growing |")
    a(f"| **3 · thumbnail** | `{ep['thumbs'][0][0]}`–`{ep['thumbs'][-1][0]}` | **{n_th}** | "
      f"**no** — a thumbnail never becomes a cut |")
    a("")
    a("**Declaring the headroom would fail the build.** `check_spec_satisfied.py` fails any "
      "`mandatory_stills` id that appears in no cut, and the solver places only the declared "
      "number of still cuts. That correction had to be made late on EP65. "
      "**`episode_spec.v001.json` is not edited by this order.** Thumbnails are never declared "
      "and never become cuts.")
    a("")
    a(f"**Paste files:** `EP{ep['num']}_{slug}_CODEX_PASTE_A/headroom_01.txt` … "
      f"`thumbs_01.txt`, and the merged single file "
      f"`EP{ep['num']}_{slug}_CODEX_PASTE_ALL.txt` which now carries **all "
      f"{n_dec + n_hd + n_th}** prompts in one file. Both are emitted from "
      f"`scripts/build_ep68_ep69_headroom_order.py` together with this document, so the prompt "
      f"bodies cannot drift apart; the equality is *checked by the generator*, not asserted here.")
    a("")
    a("---")
    a("")
    a("## 0. How many, derived rather than chosen")
    a("")
    a(f"EP66 batch C is the only measured plate-rejection rate this channel has: "
      f"**{EP66_ORDERED} ordered, {EP66_REJECT} REJECT ({REJECT_ONLY*100:.1f}%) and "
      f"{EP66_FLAG} further FLAG — {REJECT_AND_FLAG*100:.1f}% combined.** Reproduced "
      f"mechanically from `runs/qc/openfields_plate_verdicts.v001.md` by "
      f"`check_plate_verdicts.ingest_md`, which returns "
      f"`{{'accept': 170, 'reject': 11, 'unresolved': 10}}`.")
    a("")
    a("```")
    a(f"declared mandatory_stills          {d['declared']}")
    a(f"distinct_video_assets              {d['distinct_video_assets']}   "
      f"target_cut_sec {d['target_cut_sec']}")
    a(f"build_case_film_generic.solve_totals still-cut ceiling, flat across the whole declared")
    a(f"  script_words x pace band         {sorted({v[2] for v in d['solver'].values()})[0]}"
      f"   = floor({d['distinct_video_assets']} x 0.32 / 0.68)")
    a("")
    a(f"  {d['declared']} / (1 - {REJECT_ONLY:.3f})  =  {d['need_reject_only']}"
      f"     hard rejects only")
    a(f"  {d['declared']} / (1 - {REJECT_AND_FLAG:.3f})  =  {d['need_reject_and_flag']}"
      f"     rejects + flags   <- used")
    a("")
    a(f"HEADROOM  {d['need_reject_and_flag']} - {d['declared']} = {d['headroom']}")
    a(f"THUMBS    {d['thumbs']}   (episode_spec.thumbnail_candidates_min = "
      f"{d['thumbnail_candidates_min']})")
    a(f"ORDERED   {d['declared']} + {d['headroom']} + {d['thumbs']} = {d['ordered']}")
    a("```")
    a("")
    if d["still_ceiling"] > d["declared"]:
        a(f"**Note, measured and not tidied away.** The solver's still-cut ceiling for this "
          f"episode is **{d['still_ceiling']}**, which is {d['still_ceiling'] - d['declared']} "
          f"above the declared {d['declared']}. The headroom above is sized to protect the "
          f"DECLARED count against rejection, not to fill that ceiling. `docs/PD_CANON.md` rule "
          f"25 applies: the band is a prediction and the delivered VO is the measurement — if "
          f"`mandatory_stills` is ever re-derived upward from the real narration master, or if "
          f"`distinct_video_assets` changes, **re-run "
          f"`scripts/build_ep68_ep69_headroom_order.py --derive` and re-order**. Do not carry "
          f"{d['declared']} forward on faith.")
        a("")
    a(f"**Six thumbnails, not three.** `episode_spec.thumbnail_candidates_min` is "
      f"{d['thumbnail_candidates_min']} and the packaging document specifies three variants. Each "
      f"variant is ordered as a **framing pair**, so a variant that comes back badly framed still "
      f"leaves three candidates and no thumbnail has to be re-ordered on the day.")
    a("")
    a(ep["supersedes"])
    a("")
    a("---")
    a("")
    a("## 1. `[NEG]` — this episode's own, unchanged, on every plate in every tier")
    a("")
    a("**This is the canonical `[NEG]`. It is read out of "
      f"`EP{ep['num']}_{slug}_CODEX_BATCH_A.v001.md` at generation time and never retyped, and "
      "the generator refuses to write if the copy in the paste files is not byte-identical to it:**")
    a("")
    a("> " + NEG)
    a("")
    a("**It is NOT deviated for the thumbnail lane.** Only the style block changes there.")
    a("")
    a("**Note what it deliberately does NOT contain: `human face`, `facial features`, `eyes`.** "
      "Those three suppress the people lane, and the people lane is required. What is suppressed "
      "instead is *identifiability*: `recognisable person`, `identifiable person`, `likeness of a "
      "real individual`, `portrait of a named person`, `celebrity`, `public figure`, `deepfake`. "
      "The generator checks for all seven and refuses if any of the three banned tokens returns; "
      "`scripts/check_image_order_neg.py` checks this document independently.")
    a("")
    a("---")
    a("")
    a("## 2. `[STYLE]` — unchanged, on every headroom plate")
    a("")
    a("> " + STYLE)
    a("")
    a("## 3. `[TSTYLE]` — the thumbnail lane only, and why it exists")
    a("")
    a("> " + TSTYLE)
    a("")
    a("**EP65's lesson, stated so nobody undoes this.** The canonical `[STYLE]` above mandates "
      "*low contrast*, which is correct for a film frame and is exactly why EP65's four thumbnail "
      "candidates came back as dull grey paper and had to be re-ordered. A thumbnail is not a "
      "film frame. `build_ep62_65_thumbnails.py` lays a **black scrim at alpha 120 over the top "
      "66%** before the headline goes on, and `thumb_subject_luma` wants a subject box of mean "
      "luma **>= 60** with a bright connected component **>= 150 px**. So: one hard directional "
      "key, high contrast, bright overall exposure, subject brighter than background, the whole "
      "subject inside the lower 60% with the bottom third the brightest part of the picture, and "
      "**the entire upper 40% of the frame an unbroken field** so a headline can be burned into "
      "it. Not a mood; a measurement.")
    a("")
    a("---")
    a("")
    a(f"## 4. Headroom — {n_hd} plates, `{ep['headroom'][0][0]}`–`{ep['headroom'][-1][0]}`, "
      f"**not declared in the spec**")
    a("")
    a("Every one still carries a script line and a section reference — **a plate with no beat is "
      "not commissioned**, headroom or otherwise. Every prompt is **self-contained**: none of "
      "them says \"the same X\" about a plate that lives in another file, because a generator has "
      "no memory between prompts.")
    a("")
    a("| id | script line it carries | where it lands |")
    a("|---|---|---|")
    for pid, _b, _n, line, ledg in ep["headroom"]:
        a(f"| `{pid}` | {line} | {ledg} |")
    a("")
    for pid, body, neg_add, line, ledg in ep["headroom"]:
        a(f"### `{pid}.png` — {ledg}")
        a("")
        a(f"*Script line:* {line}")
        a("")
        a("```")
        a(prompt_line(body, neg_add, False))
        a("```")
        a("")
    a("---")
    a("")
    a(f"## 5. Thumbnails — {n_th} plates, `{ep['thumbs'][0][0]}`–`{ep['thumbs'][-1][0]}`, "
      f"**never declared, never a cut**")
    a("")
    a("| id | packaging variant |")
    a("|---|---|")
    for pid, _b, _n, line, _g in ep["thumbs"]:
        a(f"| `{pid}` | {line} |")
    a("")
    for pid, body, neg_add, line, ledg in ep["thumbs"]:
        a(f"### `{pid}.png` — {line}")
        a("")
        a(f"*Reference:* {ledg}")
        a("")
        a("```")
        a(prompt_line(body, neg_add, True))
        a("```")
        a("")
    a("---")
    a("")
    a("## 6. Delivery")
    a("")
    a(f"- Names are exactly `{ep['headroom'][0][0]}.png` … `{ep['headroom'][-1][0]}.png` and "
      f"`{ep['thumbs'][0][0]}.png` … `{ep['thumbs'][-1][0]}.png`. No `_v2`, no `_02`, no `_A`.")
    a(f"- Deliver to `{ep['save_dir']}`, long edge >= 3840, PNG, 16:9.")
    a("- **Headroom plates are NOT added to `episode_spec.mandatory_stills`** and thumbnail "
      "plates are not added to anything. Neither file is edited by this order.")
    a("- After delivery: `py -3.11 scripts/check_plate_verdicts.py --slug "
      f"{slug} --scaffold --reviewer <name>`, open every plate, record a verdict for each, then "
      f"`py -3.11 scripts/check_episode_inputs.py --slug {slug}`. The plate gate blocks the build "
      "until every plate in the set carries a resolved verdict bound to the file on disk.")
    a("")
    a("*Generated by `scripts/build_ep68_ep69_headroom_order.py`. The prompt bodies in this "
      "document and in the paste files come from one source and the generator checks they are "
      "byte-identical.*")
    files[f"EP{ep['num']}_{slug}_CODEX_BATCH_B.v001.md"] = "\n".join(D) + "\n"
    return files


BANNED_IN_NEG = ("human face", "facial features", "eyes")
REQUIRED_IN_NEG = ("recognisable person", "identifiable person", "likeness of a real individual",
                   "portrait of a named person", "celebrity", "public figure", "deepfake")


# =============================================================================================
# verify
# =============================================================================================
CTRL = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
FULLWIDTH_ALNUM = re.compile(r"[０-９Ａ-Ｚａ-ｚ]")
SHELLISH = re.compile(r"(?:^|\s)(?:py -3\.11|python |bash |cmd\b|\$\(|`[a-z]|&&|\|\||>>|; *rm )")


def verify(all_files: dict[str, dict[str, str]]) -> int:
    bad = 0
    print("=" * 96)
    for slug, files in all_files.items():
        ep = EPISODES[slug]
        pdir = PLANNING / f"EP{ep['num']}_{slug}_CODEX_PASTE_A"
        doc_a = PLANNING / f"EP{ep['num']}_{slug}_CODEX_BATCH_A.v001.md"
        NEG = neg_from_doc(doc_a)
        merged = files[f"EP{ep['num']}_{slug}_CODEX_PASTE_ALL.txt"]
        docb = files[f"EP{ep['num']}_{slug}_CODEX_BATCH_B.v001.md"]

        n_dec = sum(len(parse_prompts(f.read_text(encoding="utf-8")))
                    for f in sorted(pdir.glob("batch_*.txt")))
        want = n_dec + len(ep["headroom"]) + len(ep["thumbs"])
        got = parse_prompts(merged)
        ids = [p for p, _ in got]

        def row(label: str, ok: bool, detail: str = "") -> None:
            nonlocal bad
            if not ok:
                bad += 1
            print(f"  {'ok  ' if ok else 'FAIL'} {label:52s} {detail}")

        print(f"--- EP{ep['num']} {slug}")
        row("merged prompt count", len(got) == want, f"{len(got)} (want {n_dec}+"
            f"{len(ep['headroom'])}+{len(ep['thumbs'])}={want})")
        row("ids unique", len(set(ids)) == len(ids), f"{len(set(ids))} distinct")
        # every declared prompt survives byte-identically into the merged file
        dec_src = []
        for f in sorted(pdir.glob("batch_*.txt")):
            dec_src += parse_prompts(f.read_text(encoding="utf-8"))
        row("declared prompts byte-identical to batch_*.txt", got[:n_dec] == dec_src)
        # NEG byte-identity everywhere it appears
        neg_ok = merged.count(NEG) >= 1 and docb.count(NEG) >= 1
        for name, text in files.items():
            if "/headroom_" in name or "/thumbs_" in name:
                neg_ok = neg_ok and text.count(NEG) == 1
        row("[NEG] byte-identical in every emitted file", neg_ok)
        low = NEG.lower()
        row("[NEG] has all seven identifiability tokens",
            all(t in low for t in REQUIRED_IN_NEG))
        row("[NEG] free of human face / facial features / eyes",
            not any(t in low for t in BANNED_IN_NEG))
        # thumbnails use [TSTYLE], headroom uses [STYLE]
        tids = {p + ".png" for p, _, _, _, _ in ep["thumbs"]}
        hids = {p + ".png" for p, _, _, _, _ in ep["headroom"]}
        t_ok = all(b.rstrip().split(" Avoid:")[0].endswith("[TSTYLE]")
                   for p, b in got if p in tids)
        h_ok = all(b.rstrip().split(" Avoid:")[0].endswith("[STYLE]")
                   for p, b in got if p in hids)
        row("thumbnail prompts end [TSTYLE]", t_ok)
        row("headroom prompts end [STYLE]", h_ok)
        row("every new prompt carries Avoid: [NEG]",
            all(" Avoid: [NEG], " in b for p, b in got if p in tids | hids))
        # control characters (an earlier order emitted BEL bytes)
        ctrl = {n: CTRL.findall(t) for n, t in files.items() if CTRL.search(t)}
        row("no control/BEL bytes in any emitted file", not ctrl, str(list(ctrl)[:2]))
        # A [STYLE]/[TSTYLE] block that contains a shell command. PASTE FILES ONLY: tonight one
        # order shipped a [STYLE] containing a command, and the paste file is the thing that gets
        # pasted into a generator. The batch document is prose FOR A HUMAN and legitimately tells
        # the reader to run check_plate_verdicts.py, so including it here fired on correct text.
        sh = [n for n, t in files.items() if n.endswith(".txt")
              and SHELLISH.search(t.split("──────── プロンプト")[0])]
        row("no shell command inside a style/common block (paste files)", not sh, str(sh[:2]))
        # dangling cross-file reference: "the same X" whose referent is not in this same file
        dangle: list[str] = []
        for name, text in files.items():
            if not name.endswith(".txt"):
                continue
            here = {p for p, _ in parse_prompts(text)}
            for p, b in parse_prompts(text):
                for m in re.finditer(r"\bthe same\b", b, re.I):
                    # allowed only when the referent is named and present in this same file
                    refs = re.findall(r"\b([A-Z]\d{3})\b", b)
                    if not refs and p not in here:
                        dangle.append(f"{name}:{p}")
                    elif refs and not all(r + ".png" in here for r in refs):
                        dangle.append(f"{name}:{p} -> {refs}")
                    break
        # a "the same" inside ONE prompt that describes its own scene fully is fine as long as the
        # thing it repeats is named in that same prompt; flag only cross-file id references.
        row("no 'the same X' pointing at a plate in another file", not dangle, str(dangle[:3]))
        # Full-width LETTERS AND DIGITS only. The first version of this check flagged every
        # east-asian-width "F" character and therefore fired on the ideographic space and the
        # full-width parentheses, slash and equals that the existing paste files have used since
        # EP62 -- correct Japanese typography reported as a defect. A full-width letter or digit
        # is a real hazard, because it would silently break a plate id.
        weird = sorted({c for t in files.values() for c in t if FULLWIDTH_ALNUM.match(c)})
        row("no full-width latin letters or digits", not weird, "".join(weird[:8]))
        # id contiguity of the new tiers
        hnums = [int(p[1:]) for p, _, _, _, _ in ep["headroom"]]
        # The first emitted EP68 merged file printed a bare "[HSTYLE]" with no text under it,
        # because the extractor only handled hyatt shape. Caught by reading the file; now measured.
        batch_texts = [f.read_text(encoding="utf-8") for f in sorted(pdir.glob("batch_*.txt"))]
        hs = hstyle_of(batch_texts, dec_src)
        row("[HSTYLE] preamble present in the merged file, verbatim",
            len(hs) > 40 and hs in merged, f"{len(hs)} chars: {hs[:52]}...")
        # EVERY CITED SCRIPT LINE MUST ACTUALLY BE IN THE SCRIPT. The first draft of the headroom
        # data invented two lines outright ("The agency had opened a defect investigation.",
        # "It sent the company a letter.") and paraphrased six others. A citation nobody checks
        # is a fabrication waiting to be quoted back, so it is checked here against the delivered
        # script, whitespace-normalised so a line wrapped in the markdown still matches.
        sname = "EP{}_{}_script.en.v001.md".format(ep["num"], slug)
        flat = " ".join((PLANNING / sname).read_text(encoding="utf-8").split())
        bad_cite = [pid for pid, _b, _n, line, _g in ep["headroom"]
                    if " ".join(line.split()) not in flat]
        row("every headroom citation is verbatim in the script", not bad_cite, str(bad_cite))
        row("headroom ids contiguous",
            hnums == list(range(hnums[0], hnums[0] + len(hnums))),
            f"{ep['headroom'][0][0]}-{ep['headroom'][-1][0]}")
        print()
    print("=" * 96)
    return bad


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--verify", action="store_true", help="verify only, write nothing")
    ap.add_argument("--derive", action="store_true", help="print the arithmetic and stop")
    a = ap.parse_args()

    d = derivations()
    print_derivation(d)
    if a.derive:
        return 0

    all_files = {slug: build(slug) for slug in EPISODES}

    for slug, files in all_files.items():
        for rel, text in files.items():
            p = PLANNING / rel
            if a.verify:
                cur = p.read_text(encoding="utf-8") if p.is_file() else None
                mark = "same" if cur == text else ("DIFFERS" if cur is not None else "MISSING")
                print(f"[verify] {mark:8s} {rel}")
            else:
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text(text, encoding="utf-8", newline="\n")
                print(f"[write]  {len(text):7d} bytes  {rel}")
    print()
    bad = verify(all_files)
    if bad:
        print(f"{bad} verification failure(s)")
        return 1
    print("all verification checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
