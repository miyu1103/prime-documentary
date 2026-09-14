#!/usr/bin/env python3
"""One data source for the EP67/EP68/EP69 people-thumbnail order.

Why this file exists, measured
------------------------------
Channel CTR is 1.39% against a 4-6% target and the picture is the ceiling: video
`Enok7A7wGBA` sits at 0.46% on 1,090 impressions behind a fully rule-compliant title, and the
39-title rewrite produced no detectable title-shape effect in either direction. The one plate that
has visibly lifted a thumbnail on this channel is EP65 marmet v006 -- an older man at a counter,
FACE LEGIBLE, a document and a pen in front of him, big type on the empty half. Before it, marmet's
four candidates were text over blurred paper and the owner rejected them as jimi.

EP67/EP68/EP69 cannot produce that picture. Their thumbnail briefs put `face`, `head` and
`person in frame` in the per-plate negative, so every candidate they can make is a still life.
This order replaces that with six plates whose defining property is a legible human face next to
the object.

It emits BOTH deliverables from one dict so the prompt bodies cannot drift:

    episodes/_planning/EP67_69_THUMBS_PEOPLE_CODEX.v001.md
    episodes/_planning/EP67_69_THUMBS_PEOPLE_PASTE_ALL.txt

The canonical [NEG] for each episode is READ OUT OF THAT EPISODE'S OWN BATCH A at build time --
never retyped -- so byte-identity is a property of the build, not of anyone's care.

    py -3.11 scripts/build_ep67_69_thumbs_people.py
    py -3.11 scripts/build_ep67_69_thumbs_people.py --verify   # measure, do not write
"""
from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[1]
PLANNING = ROOT / "episodes" / "_planning"

DOC_OUT = PLANNING / "EP67_69_THUMBS_PEOPLE_CODEX.v001.md"
PASTE_OUT = PLANNING / "EP67_69_THUMBS_PEOPLE_PASTE_ALL.txt"

# --------------------------------------------------------------------------------------------
# The canonical [NEG] is lifted, not retyped. Same extraction rule as
# scripts/check_image_order_neg.py: the longest blockquote line that reads like a negative list.
# --------------------------------------------------------------------------------------------
NEG_SOURCE = {
    "ramirez": "EP67_ramirez_CODEX_BATCH_A.v002.md",
    "pinto": "EP68_pinto_CODEX_BATCH_A.v001.md",
    "hyatt": "EP69_hyatt_CODEX_BATCH_A.v001.md",
}


def lift_neg(filename: str) -> str:
    text = (PLANNING / filename).read_text(encoding="utf-8")
    cands = [l for l in text.splitlines()
             if l.lstrip().startswith(">") and re.search(r"\btext\b.*\blettering\b", l, re.I)]
    if not cands:
        raise SystemExit(f"[build] no canonical [NEG] found in {filename}")
    return max(cands, key=len).lstrip("> ").strip()


NEG = {slug: lift_neg(fn) for slug, fn in NEG_SOURCE.items()}

# --------------------------------------------------------------------------------------------
# Blocks that are byte-identical in all six prompts.
# --------------------------------------------------------------------------------------------

# EP67 delivered 88 of 104 plates at 1672x941 when this sentence lived only in the header.
# EP62's 70 came back all correct once it was in each body. It goes in each body.
RES = ("Output at 3840x2160 pixels, 16:9, long edge at least 3840 -- a smaller file is unusable "
       "and will be rejected.")

# The headline is burned into the top of the frame by build_ep62_65_thumbnails.py, which lays a
# black scrim at alpha 120 over the top 66%. This sentence is IDENTICAL in all six bodies.
UPPER40 = ("THE ENTIRE UPPER 40 PERCENT OF THE FRAME IS ONE UNBROKEN UNIFORM FIELD - plain wall, "
           "plain sky or plain out-of-focus darkness, with no object, no edge, no horizon, no head "
           "and no detail crossing it anywhere - and the whole subject, including the head, sits "
           "inside the lower 60 percent, with the bottom third the brightest part of the picture.")

# A [NEG] ban alone failed twice on EP66 L146, so this goes in the POSITIVE prompt. Identical x6.
NOTEXT = ("Nothing anywhere in this picture carries a readable character: not one word, numeral, "
          "signature, badge, logo, brand mark, nameplate, stamp or piece of signage on any "
          "surface, garment, wall, screen, paper or object in the frame.")

# EP66 L236 failed twice on a raised hand with fused fingers. Resting it flat fixed it. Identical x6.
HANDS = ("THE HAND IS AT REST FLAT ON THE SURFACE, not raised and not held in the air, the palm "
         "laid down in full contact with it and the wrist straight, THE FOUR FINGERS LYING SIDE BY "
         "SIDE AND SEPARATE with a visible line of shadow between each pair and one nail showing "
         "on each, and the thumb clearly apart from the fingers along the near side.")

# The face is the whole point of the order, so it is specified rather than hoped for. Identical x6.
# Deliberately gender-neutral: one of the six subjects is a woman, and an earlier draft of this
# clause said "HIS FACE ... He is" in her prompt, which is a prompt that contradicts itself.
FACE = ("THE FACE IS FULLY VISIBLE, TURNED TOWARD THE KEY LIGHT AND EVENLY LIT, both eyes open and "
        "carrying a catchlight, the whole head well inside the lower 60 percent of the frame and "
        "markedly brighter than the field behind it. THIS PERSON IS COMPLETELY INVENTED AND "
        "FICTIONAL and resembles no living or dead person, no public figure and nobody in any news "
        "photograph; they are uninjured, unhurt and in ordinary health, and they are not looking "
        "at the lens.")

# Documents are ordered as a SHAPE, in the positive prompt. Four plates carry printed paper.
GREYBARS = ("The paper carries no writing of any kind, and this is what is on it instead: EVENLY "
            "SPACED FLAT GREY HORIZONTAL BARS of one uniform width and one uniform weight, laid in "
            "parallel like ruled bands of tone, each bar a solid unbroken block of soft grey with "
            "straight ends and no letter shapes, no word shapes, no gaps between words and no "
            "broken or ragged edge anywhere along it, so the sheet reads as printed matter purely "
            "by its rhythm of grey and white and carries not one readable character.")

# Two plates carry an engineering drawing rather than printed paper. Same rule, drawn shapes.
DRAWLINES = ("The drawing carries no writing, no dimension, no numeral and no callout of any kind, "
             "and this is what is on it instead: PLAIN THIN GREY CONSTRUCTION LINES AND PLAIN GREY "
             "OUTLINES on pale vellum, straight and clean, with no title block, no revision table, "
             "no schedule, no stamp, no seal and not one readable character anywhere on the sheet.")

# Thumbnail-lane [NEG] additions common to all six. Note what is NOT here: no `face`, no `head`,
# no `person in frame`. Those three are the reason the existing T001-T006 briefs can only make
# still lifes, and `human face` / `facial features` / `eyes` are the over-swing that forced 191
# plates to be re-ordered on EP66.
COMMON_ADD = [
    "low contrast", "dull flat lighting", "dark subject",
    "object in the top of the frame", "detail crossing the top of the frame",
    "subject turned away from camera", "seen from behind", "silhouette",
    "backlit rim light only", "motion blur on the subject",
    "fingers fused into one mass", "fingers merged", "webbed fingers", "mitten hand",
    "stub fingers", "missing thumb", "extra fingers", "six fingers", "malformed hand",
    "interlocked fingers", "raised hand", "hand held up in the air", "blurred hand",
    "readable document", "printed words on paper", "letterforms", "typed lines",
    "printed paragraph", "form fields with labels", "letterhead", "stamp with words",
    "readable screen", "icons", "cursor", "user interface",
    "stock-photo smile", "model look", "beauty retouching", "studio backdrop",
]

# One [TSTYLE], shared by all six, so the upper-40 clause cannot differ between episodes.
# The canonical [STYLE] mandates "low contrast, low-key" -- correct for a film frame, and exactly
# why EP65's first four thumbnail candidates came back as grey paper. Period and place therefore
# live in each prompt body instead of in the style token.
TSTYLE = (
    "editorial photographic still made to be a video thumbnail, ONE HARD DIRECTIONAL KEY LIGHT "
    "from the side, HIGH CONTRAST AND BRIGHT OVERALL EXPOSURE, the subject clearly brighter than "
    "everything behind it and cleanly separated from it, shadow only where it defines an edge and "
    "never filling the frame, the face fully lit and legible with both eyes open and a catchlight "
    "in each, photographic, 35mm, real ordinary adults, ordinary bodies and ordinary clothing, "
    "candid, no styling, no beauty retouching, no model look, no stock-photo smile, ultra-detailed, "
    "photoreal, 4K, 16:9, no text, no lettering, no numerals, no watermark, no logo, no signage, "
    + UPPER40
)

# --------------------------------------------------------------------------------------------
# The six plates.
#
# Ids: T001-T006 are already on disk in all three stores (152 files in ramirez, 123 in pinto,
# 133 in hyatt; T001.png..T006.png present in each). T007-T012 are free in ALL THREE stores, and
# they are allocated across the three episodes rather than restarting at T007 in each, so that a
# plate written to the wrong directory shows up as a wrong NAME instead of silently overwriting
# another episode's candidate. Three episodes, three different save directories.
# --------------------------------------------------------------------------------------------
EPISODES = [
    {
        "slug": "ramirez",
        "ep": "EP67",
        "title": "TransUnion LLC v. Ramirez",
        "dir": r"E:\pd-media\assets\ai\ramirez",
        "era": ("A car dealership showroom in Dublin, California, in the United States, on a bright "
                "February afternoon in 2011"),
        "neg_add": [
            "licence plate", "registration plate", "number plate", "badge on the grille",
            "oval emblem", "manufacturer wordmark", "chrome nameplate", "dealership signage",
            "price sticker", "window sticker", "showroom banner", "wall poster", "price board",
            "spreadsheet on a monitor", "web page",
            "European streetscape", "Irish town", "Georgian doorway", "EU number plate",
            "foreign-language signage", "cobbled lane", "thatched roof", "tram",
        ],
        "barred": ("Sergio L. Ramirez, his wife and his father-in-law (all living private "
                   "individuals, CLAUDE inv. 11 / ledger forbidden-row 07); the Nissan salesman or "
                   "any dealership employee, who is never named and was never a party "
                   "(forbidden-row 08); the two SDNs (forbidden-row 09). Forbidden-row 13 bars any "
                   "generated image PRESENTED AS Sergio Ramirez, a real TransUnion credit report, "
                   "the OFAC Letter, or the Dublin dealership. Neither plate below may be "
                   "captioned, cut, narrated or titled as any of them."),
        "neg_tension": ("None. This episode's canonical [NEG] carries no token that fights a "
                        "person in frame."),
        "plates": [
            {
                "id": "T007",
                "variant": "Variant 1 (recommended, pairs with title T1)",
                "headline": "NAME ONLY",
                "headline_ink": "184 px at size 248, breaking NAME / ONLY",
                "kicker": "NO OTHER CHECK",
                "accent": "RED #D22628",
                "ledger": ("SR-01 (*\"On February 27, 2011, Ramirez visited a Nissan dealership in "
                           "Dublin, California\"*), SR-02 (the OFAC advisor alert on the report) and "
                           "SR-03 (*\"A Nissan salesman told Ramirez that Nissan would not sell the "
                           "car to him\"*). LS-06 is the reason the plate is worth a thumbnail: "
                           "OFAC's own Step 3 says a name-only match *\"is not a valid match\"*."),
                "why": ("This is the film's moment and it has two people in it, which is exactly "
                        "what the existing T001-T006 brief forbids. The customer's face carries the "
                        "picture; the salesman is a shoulder and a forearm turning the monitor."),
                "body": (
                    "{era}. A CUSTOMER SITS AT A SALES DESK, seen across the desk from slightly "
                    "above his own shoulder line so that he reads chest-up and central. {face} He "
                    "is in his forties, in a plain open-collar shirt, and his expression is flat "
                    "and unreadable. ONE OF HIS HANDS RESTS ON THE DESK TOP in front of him. "
                    "{hands} A PLAIN BALLPOINT PEN LIES LOOSE ON THE DESK beside it, held by "
                    "nobody. A SINGLE SHEET OF PRINTED PAPER LIES SQUARE ON THE DESK under the "
                    "pen. {greybars} At the far side of the desk a SECOND ADULT, a salesman, is "
                    "cropped by the frame edge to a shoulder, an upper arm and a forearm only, "
                    "with NO PART OF HIS HEAD IN THE PICTURE, and he is TURNING A SLIM COMPUTER "
                    "MONITOR ROUND TOWARD THE CUSTOMER. The screen faces the customer and is never "
                    "legible: it is a single soft bloom of even light with no icons, no windows, "
                    "no rows, no cursor and nothing that could be read as a document. The car keys "
                    "sit on the far corner of the desk, unmarked. One hard directional key light "
                    "comes in from the left through showroom glass and makes the customer's face "
                    "and the paper the brightest things in the picture; the bright bare desk top "
                    "runs across the bottom third. No vehicle in the frame carries a badge, an "
                    "emblem, a wordmark, a nameplate or a plate of any kind, and there is no "
                    "dealership signage, banner, poster or price board anywhere. {notext} {upper40}"
                ),
            },
            {
                "id": "T008",
                "variant": "Variant 1 (the A/B partner for T007 -- same headline, different picture)",
                "headline": "NAME ONLY",
                "headline_ink": "184 px at size 248, breaking NAME / ONLY",
                "kicker": "NO OTHER CHECK",
                "accent": "RED #D22628",
                "ledger": ("SR-04, verbatim: *\"Ramirez's wife had to purchase the car in her own "
                           "name.\"* Held against SR-03, which is why she had to."),
                "why": ("The record's ending, and the only frame in the episode where the human "
                        "cost is a face rather than a document. The man is deliberately pushed out "
                        "of focus and out of the light: the picture is about who is allowed to "
                        "sign."),
                "body": (
                    "{era}. A WOMAN SITS AT THE SAME SALES DESK, chest-up and central, seen from "
                    "just across the desk at her own eye height. {face} She is in her forties, in "
                    "an ordinary blouse, and her expression is flat and tired rather than pleased. "
                    "ONE OF HER HANDS RESTS ON THE DESK TOP beside a single sheet of printed "
                    "paper. {hands} A PLAIN BALLPOINT PEN LIES LOOSE ON THE PAPER, held by nobody. "
                    "{greybars} STANDING WELL BEHIND HER AND CLEARLY OUT OF FOCUS is an adult man, "
                    "a soft dark shape only, one step back from the desk with his hands at his "
                    "sides, DARKER THAN SHE IS AND WITH NO FEATURE RESOLVING ON HIM AT ALL. One "
                    "hard directional key light from the left puts her and the paper in the "
                    "brightest part of the picture and leaves him in shadow; the bright bare desk "
                    "top runs across the bottom third. The showroom behind them is plain and "
                    "featureless, with no vehicle badge, emblem, wordmark, nameplate or plate of "
                    "any kind and no dealership signage, banner, poster or price board anywhere. "
                    "{notext} {upper40}"
                ),
            },
        ],
    },
    {
        "slug": "pinto",
        "ep": "EP68",
        "title": "The Ford Pinto / Grimshaw v. Ford",
        "dir": r"E:\pd-media\assets\ai\pinto",
        "era": ("The United States between 1968 and 1981, period surfaces only -- painted steel, "
                "brushed aluminium, laminate, bakelite, manila card, enamel -- and 1970s clothing "
                "throughout"),
        "neg_add": [
            "licence plate", "registration plate", "number plate", "badge on the grille",
            "oval emblem", "manufacturer wordmark", "chrome nameplate", "model script",
            "dealership signage", "price sticker", "window sticker",
            "scorch marks", "fuel spill", "crumpled bodywork",
            "digital watch", "modern eyewear", "modern haircut", "modern office fittings",
            "courtroom bench in frame", "witness box in frame",
        ],
        "barred": ("Richard Grimshaw -- he was 13 in 1972, may be living, and forbidden-row 08 bars "
                   "any depiction of him, of a burned child, of a burned adult, of skin grafts or "
                   "of a person on fire. Lilly Gray and her family (forbidden-row 09). The Ulrich "
                   "sisters and their cousin. Robert Duggar, the van driver (forbidden-row 11). Any "
                   "named Ford employee (forbidden-row 10). Forbidden-row 15 bars any generated "
                   "image presented as the Grush/Saunby memo, exhibit 125, a crash-test report, an "
                   "NHTSA letter or recall notice, a page of the record, the Elkhart indictment or "
                   "a period front page. NO FORD BADGE, SCRIPT OR BLUE OVAL ANYWHERE. No burned "
                   "person, no injured child, no fire, no wreck."),
        "neg_tension": ("This episode's canonical [NEG] carries `children`. Both subjects below are "
                        "written as adults in their forties or fifties for that reason. It also "
                        "carries `courtroom interior`, `jury box` and `witness stand`, which is why "
                        "T009 is a PUBLIC CORRIDOR OUTSIDE a courtroom and says so in the positive "
                        "prompt rather than relying on the negative."),
        "plates": [
            {
                "id": "T009",
                "variant": "Variant 1 (recommended, pairs with title T1)",
                "headline": "WRONG MEMO",
                "headline_ink": "218 px at size 248, breaking WRONG / MEMO",
                "kicker": "IT WAS ROLLOVER",
                "accent": "RED #D22628 (kicker measured 291 px wide at 46 px)",
                "ledger": ("DOC-01 -- the famous memo was EXCLUDED from evidence in *Grimshaw* -- "
                           "held against DOC-06, the memo's own first line: *\"The analysis "
                           "discussed below concerns the static rollover requirement proposed for "
                           "FMVSS 301.\"* DOC-09 for the units: 12.5 million vehicles, all American "
                           "cars and light trucks, not Pintos."),
                "why": ("The whole episode is that the country convicted Ford on a document the "
                        "jury never saw, about a crash mode this case was not about. A man holding "
                        "that document in a corridor outside the room is the thesis in one frame, "
                        "and it puts a face where four still lifes of paper used to be."),
                "body": (
                    "{era}. A MAN IN HIS FIFTIES STANDS AT A DEEP STONE WINDOW SILL IN A PLAIN "
                    "PUBLIC CORRIDOR OUTSIDE A COURTROOM -- a wide stone-floored public hallway "
                    "with a panelled door closed behind him and a tall window beside him. THIS IS "
                    "A CORRIDOR AND NOT A COURTROOM: there is no bench, no jury box, no witness "
                    "stand, no rail and no gallery seating anywhere in the picture. He is chest-up "
                    "and central, in a wide-lapel 1970s suit with a broad tie, and his expression "
                    "is tired and flat. {face} A PLAIN MANILA FOLDER LIES OPEN AND FLAT ON THE "
                    "BROAD STONE SILL in front of him, with one sheet of typed paper lying square "
                    "in it, held by nobody. ONE OF HIS HANDS RESTS ON THE SILL beside the "
                    "folder. {hands} {greybars} One hard directional key light from the window on "
                    "the left makes his face and the paper markedly brighter than the corridor "
                    "behind him, which falls away plain and dark. The bright stone sill runs "
                    "across the bottom third. {notext} {upper40}"
                ),
            },
            {
                "id": "T010",
                "variant": "Variant 3",
                "headline": "500 OR 27",
                "headline_ink": "220 px at size 248, breaking 500 OR 27",
                "kicker": "NHTSA, MAY 1978",
                "accent": "GOLD #E5B53A (kicker measured 301 px wide at 46 px)",
                "ledger": ("RC-07 (*\"In May 1978, NHTSA issued an initial determination that the "
                           "Pinto's fuel system was defective\"*), RC-01 (campaign 78V143000, "
                           "received 19 June 1978), RC-02 (1,400,000 units) and RC-04 (*\"THE DEALER "
                           "WILL INSTALL A LONGER FUEL FILLER PIPE HAVING AN IMPROVED SEAL\"*). The "
                           "headline's two numbers are PM-02 (Dowie's 500) against CC-03 (NHTSA's "
                           "27)."),
                "why": ("The recall is the one point in the story where all of this reaches an "
                        "ordinary owner, as a piece of paper handed across a service counter. "
                        "It is the episode's only human-scale beat that involves no fire and no "
                        "injury, which is why it is the one that can carry a face."),
                "body": (
                    "{era}. A MAN IN HIS FORTIES STANDS AT A DEALERSHIP SERVICE COUNTER, chest-up "
                    "and central, seen from just across the counter at his own eye height. The "
                    "counter is scuffed laminate over painted steel, the service area behind him "
                    "plain, dark and unresolved. He is in an ordinary 1970s open-collar shirt and "
                    "a work jacket, and his expression is flat and mildly baffled. {face} ONE OF "
                    "HIS HANDS RESTS ON THE COUNTER TOP in front of him. {hands} A SINGLE FOLDED "
                    "SHEET OF PRINTED PAPER LIES OPEN AND SQUARE ON THE COUNTER under it, and a "
                    "plain ballpoint pen lies loose beside it, held by nobody. {greybars} There is "
                    "no car in the picture, no vehicle part, no fire, no smoke, no scorching, no "
                    "damage and no liquid anywhere. One hard directional key light from the left "
                    "makes his face and the paper the brightest things in the frame; the bright "
                    "bare counter top runs across the bottom third. No badge, emblem, wordmark, "
                    "nameplate, oval, script, price board or dealership signage appears on any "
                    "surface. {notext} {upper40}"
                ),
            },
        ],
    },
    {
        "slug": "hyatt",
        "ep": "EP69",
        "title": "The Kansas City Hyatt Regency walkways",
        "dir": r"E:\pd-media\assets\ai\hyatt",
        "era": ("An engineering drawing office in the American Midwest between 1978 and 1980, "
                "tungsten lamps, vellum, brass, oiled steel and painted metal, late-1970s American "
                "working clothes throughout"),
        "neg_add": [
            "engineer's seal", "stamp with a name", "readable schedule",
            "revision cloud with text", "hi-vis vest", "modern hard hat", "plotter",
            "hotel atrium", "glazed atrium roof", "suspended indoor walkway", "hotel lobby",
            "ballroom crowd", "banquet tables", "chandelier",
        ],
        "barred": ("Daniel M. Duncan and Jack D. Gillum -- named publicly, disciplined by a state "
                   "board, possibly living (forbidden-rows 15, 20). Any victim, survivor, rescuer, "
                   "witness, board member or judge (forbidden-row 13). Any Havens Steel employee "
                   "(forbidden-row 16). Forbidden-row 14 bars any image that reads as an authentic "
                   "record: drawing S405.1, Shop Drawing 30, a page of the Commission decision, a "
                   "Missouri professional engineer's seal, an NBS test photograph. Forbidden-rows "
                   "11 and 12 bar a body, an injured person, a rescue, debris with a person under "
                   "it, and the crowded lobby at or before the moment of collapse FROM ANY ANGLE. "
                   "The Hyatt Regency itself -- its atrium, walkways, signage or logo -- is barred "
                   "as a picture. NEITHER PLATE BELOW SHOWS A BUILDING."),
        "neg_tension": ("This episode's canonical [NEG] carries the bare token `body`, alongside "
                        "`injured person`, `casualty` and `crowd of people indoors`. `body` will "
                        "fight a person in frame if the positive prompt is weak, and it is NOT "
                        "deviated. Both plates below are therefore framed CHEST-UP at a bench, "
                        "never full-length, and both say `uninjured, unhurt and in ordinary health` "
                        "in the positive prompt. If a delivered plate comes back empty of people, "
                        "the fix is to strengthen the positive, not to cut a word from [NEG]."),
        "plates": [
            {
                "id": "T011",
                "variant": "Variant 1 (recommended, pairs with title T1) -- the ONE ROD half",
                "headline": "ONE ROD / TWO RODS",
                "headline_ink": "218 px at size 248",
                "kicker": "SAME STEEL",
                "accent": "RED #D22628",
                "ledger": ("DS-04 (*\"The box beams were fabricated from MC8 x 8.5 shapes joined toe "
                           "to toe by continuous longitudinal welds.\"*), DS-05 (*\"The walkway "
                           "hangers were 1 1/4 in (32 mm) diameter rods threaded top and bottom to "
                           "receive a nut and washer.\"*) and DS-07 (*\"As originally designed the "
                           "fourth and second floor walkways were to be supported by what is "
                           "referred to as a 'one rod' design.\"*)."),
                "why": ("Hero object H1 and H2 and a face in the same frame. The existing Variant 1 "
                        "plate is two rods on a bench with the brief's own line `no hands` in it -- "
                        "which is why it cannot do what EP65 v006 did."),
                "body": (
                    "{era}. AN ENGINEER SITS AT A DRAWING BOARD, chest-up and central, seen from "
                    "across the board at his own eye height, the tilted board filling the bottom "
                    "of the frame in front of him. {face} He is in his fifties, in a plain shirt "
                    "with the sleeves rolled, no jacket, no tie and no hat of any kind, and his "
                    "expression is flat and absorbed. LYING FLAT ON THE BOARD DIRECTLY IN FRONT OF "
                    "HIM, LARGE AND SHARP IN THE NEAR FOREGROUND, IS THE DETAIL ITSELF: a short "
                    "length of thick steel rod, threaded along its whole length, PASSING THROUGH A "
                    "DRILLED HOLE IN THE FLAT WEB OF A SHORT SECTION OF WELDED STEEL BOX BEAM made "
                    "of two eight-inch channels joined open-face to open-face by a continuous weld "
                    "bead, with a plain hexagonal nut and a plain flat washer bearing on the "
                    "underside. IT IS A SINGLE CONTINUOUS ROD, ONE ROD ONLY, running clean through "
                    "the beam. ONE OF HIS HANDS RESTS ON THE BOARD beside it. {hands} A plain "
                    "wooden pencil and a parallel rule lie loose on the board, held by nobody. The "
                    "large sheet of pale vellum under all of it is a technical drawing. "
                    "{drawlines} One hard directional key light from a tungsten lamp on the left "
                    "makes his face and the machined steel markedly brighter than the office "
                    "behind him, which falls away plain and dark. The bright board surface runs "
                    "across the bottom third. There is no building, no atrium, no walkway, no "
                    "lobby, no crowd, no rubble and no damage anywhere in the picture. {notext} "
                    "{upper40}"
                ),
            },
            {
                "id": "T012",
                "variant": "Variant 1 (the A/B partner for T011) -- the TWO RODS half",
                "headline": "ONE ROD / TWO RODS",
                "headline_ink": "218 px at size 248",
                "kicker": "SAME STEEL",
                "accent": "RED #D22628",
                "ledger": ("CH-01 (*\"during construction, shop drawings were prepared by the steel "
                           "fabricator which called for the use of two sets of hanger rods rather "
                           "than a single set\"*), CH-02 (as actually constructed), CH-04 (the "
                           "second rod offset 4 inches so the two do not share a hole) and LD-04, "
                           "NBS's own conclusion word: the change *\"essentially doubled the load "
                           "to be transferred by the fourth floor box beam-hanger rod "
                           "connection.\"*"),
                "why": ("The same fictional engineer, the same board, the same lamp -- and the "
                        "detail has one more rod in it. Run as an A/B against T011 it tests whether "
                        "the object or the face is doing the work, on a picture where everything "
                        "else is held constant."),
                "body": (
                    "{era}. THE SAME ENGINEER AT THE SAME DRAWING BOARD, same chest-up framing, "
                    "same lamp, same clothes. {face} LYING FLAT ON THE BOARD DIRECTLY IN FRONT OF "
                    "HIM, LARGE AND SHARP IN THE NEAR FOREGROUND, IS THE CHANGED DETAIL: the same "
                    "short section of welded steel box beam made of two eight-inch channels joined "
                    "open-face to open-face by a continuous weld bead, but now with TWO SEPARATE "
                    "THREADED STEEL RODS instead of one -- an upper rod passing down through one "
                    "drilled hole in the flat web and stopping there on a plain hexagonal nut and "
                    "a plain flat washer, and a SECOND, ENTIRELY SEPARATE ROD hanging from a "
                    "SECOND drilled hole about four inches along the beam from the first, so that "
                    "THE TWO RODS ARE PLAINLY NOT THE SAME ROD AND DO NOT PASS THROUGH THE SAME "
                    "HOLE. ONE OF HIS HANDS RESTS ON THE BOARD beside it. {hands} A plain wooden "
                    "pencil and a parallel rule lie loose on the board, held by nobody. The large "
                    "sheet of pale vellum under all of it is a technical drawing. {drawlines} One "
                    "hard directional key light from a tungsten lamp on the left makes his face "
                    "and the machined steel markedly brighter than the office behind him. The "
                    "bright board surface runs across the bottom third. There is no building, no "
                    "atrium, no walkway, no lobby, no crowd, no rubble and no damage anywhere in "
                    "the picture. {notext} {upper40}"
                ),
            },
        ],
    },
]

FILL = {
    "face": FACE, "hands": HANDS, "notext": NOTEXT, "upper40": UPPER40,
    "greybars": GREYBARS, "drawlines": DRAWLINES,
}


def render_body(ep: dict, plate: dict) -> str:
    """The prompt body, exactly as it goes to Codex. Both outputs call this and nothing else."""
    text = plate["body"].format(era=ep["era"], **FILL)
    text = re.sub(r"\s+", " ", text).strip()
    neg = ", ".join(COMMON_ADD + ep["neg_add"])
    return f"{text} {RES} [TSTYLE] Avoid: [NEG], {neg}"


def all_plates():
    for ep in EPISODES:
        for plate in ep["plates"]:
            yield ep, plate, render_body(ep, plate)


# --------------------------------------------------------------------------------------------
# Output 1: the order document
# --------------------------------------------------------------------------------------------
def build_doc() -> str:
    L: list[str] = []
    a = L.append
    a("# EP67 / EP68 / EP69 - SIX THUMBNAIL PLATES WITH A LEGIBLE FACE (Codex) v001")
    a("")
    a("**2026-08-11 - one order, three episodes, three different save directories.**")
    a("")
    a("| episode | plates | save directory |")
    a("|---|---|---|")
    for ep in EPISODES:
        ids = ", ".join(f"`{p['id']}.png`" for p in ep["plates"])
        a(f"| **{ep['ep']} {ep['slug']}** - {ep['title']} | {ids} | `{ep['dir']}\\` |")
    a("")
    a("> **They do not all go in the same folder.** Three episodes, three directories. Every plate "
      "below states its own full save path, and the merged paste file "
      "`EP67_69_THUMBS_PEOPLE_PASTE_ALL.txt` states it again above each prompt.")
    a("")
    a("**Generated by `scripts/build_ep67_69_thumbs_people.py`.** This document and the paste file "
      "come out of the same dict in that script and the prompt bodies are byte-identical between "
      "them by construction. **Edit the script, not either output.**")
    a("")
    a("---")
    a("")
    a("## 0. Why these six exist, measured")
    a("")
    a("Channel CTR is **1.39%** against a 4-6% target. The picture is the ceiling, not the title: "
      "`Enok7A7wGBA` sits at **0.46% on 1,090 impressions** behind a fully rule-compliant title, and "
      "the 39-title rewrite showed **no detectable title-shape effect in either direction**.")
    a("")
    a("The one thing that has visibly lifted a thumbnail on this channel is **EP65 marmet v006**: an "
      "older man at a counter, **face legible**, a document and a pen in front of him, big type on "
      "the empty half. Before it, marmet's four candidates were all text over blurred paper and the "
      "owner rejected them as *jimi*.")
    a("")
    a("**EP67, EP68 and EP69 cannot currently produce that picture.** Their `T001`-`T006` briefs put "
      "`face`, `head` and `person in frame` in the per-plate negative, so the only candidates they "
      "can make are still lifes - hands, an envelope, blank cards, paper, steel, a parked car. All "
      "of them gate green. **None of them can do what marmet v006 did.** These six plates are the "
      "missing lane, not a replacement: `T001`-`T006` stay on disk and stay eligible.")
    a("")
    a("**Depicted people are wanted and faces are fine** - owner decision 2026-07-04. What is barred "
      "is the likeness of a **real** individual, and every plate below says INVENTED and FICTIONAL "
      "in its own prompt body.")
    a("")
    a("---")
    a("")
    a("## 1. Ids, and why they are not all T007")
    a("")
    a("`T001.png`-`T006.png` are **already on disk in all three stores** (measured 2026-08-11: 152 "
      "files in `ramirez`, 123 in `pinto`, 133 in `hyatt`; `T001`-`T006` present in each, nothing "
      "above `T006` anywhere). `T007`-`T012` are free in **all three**.")
    a("")
    a("They are allocated **across** the three episodes rather than restarting at `T007` in each, so "
      "that a plate written into the wrong directory shows up as a **wrong name** instead of "
      "silently overwriting another episode's candidate. Six prompts, six distinct names, three "
      "directories.")
    a("")
    a("- **No `_v2`, no `_02`, no `_A`, no new ids.** One prompt = one image. Do not run a prompt "
      "twice and keep the better one.")
    a("- **Long edge >= 3840, PNG, 16:9.** The sentence `" + RES + "` is in **every prompt body**, "
      "immediately before the style token. EP67 delivered **88 of 104 plates at 1672x941** when it "
      "lived only in the header; EP62's 70 came back all correct once it was in each body.")
    a("- These six are **thumbnail candidates and never film cuts.** They add nothing to "
      "`mandatory_stills` and no `check_spec_satisfied.py` id changes.")
    a("")
    a("---")
    a("")
    a("## 2. `[TSTYLE]` - thumbnail-only, and why the canonical `[STYLE]` is not used")
    a("")
    a("The canonical `[STYLE]` in each episode's batch A mandates **\"low contrast but never "
      "crushed\"** and soft falloff. That is correct for a film frame and it is **exactly why EP65's "
      "first four thumbnail candidates came back as grey paper**. `[TSTYLE]` replaces `[STYLE]` on "
      "these six prompts and nowhere else. Period and place live in each prompt body instead of in "
      "the style token, so that **one** `[TSTYLE]` serves all three episodes and the upper-40 clause "
      "cannot drift between them.")
    a("")
    a("> " + TSTYLE)
    a("")
    a("**The upper-40 requirement, in identical words in all six prompt bodies** (the thumbnail "
      "builder lays a black scrim at alpha 120 over the top 66%, and the headline is burned into "
      "that band):")
    a("")
    a("> " + UPPER40)
    a("")
    a("---")
    a("")
    a("## 3. `[NEG]` - not deviated, and different for each episode")
    a("")
    a("**Each episode's `[NEG]` is its own.** They are not interchangeable: pinto's bans fire, "
      "burning and crash words; hyatt's bans collapse, rubble and rescue; ramirez's bans the "
      "European streetscape. Each block below was **lifted out of that episode's own batch A by the "
      "generator at build time and never retyped**, so byte-identity is a property of the build.")
    a("")
    for ep in EPISODES:
        a(f"### {ep['ep']} {ep['slug']} - `[NEG]`, byte-identical to `{NEG_SOURCE[ep['slug']]}`")
        a("")
        a("> " + NEG[ep["slug"]])
        a("")
    a("> ### The `[NEG]` does not forbid people, and must not be made to")
    a("> Each block carries the seven identifiability tokens - `recognisable person`, `identifiable "
      "person`, `likeness of a real individual`, `portrait of a named person`, `celebrity`, `public "
      "figure`, `deepfake`. **None of them contains `human face`, `facial features` or `eyes`.** "
      "That over-swing is what stopped people appearing at all on EP66 batch A and **forced 191 "
      "plates to be re-ordered**. Do not add them back, and do not add `face`, `head` or `person in "
      "frame` to a per-plate addition either - that is the exact clause that made `T001`-`T006` "
      "incapable of this picture.")
    a("")
    a("> ### Per-plate additions are additions")
    a("> Every prompt reads `Avoid: [NEG], ...`. **Expand that episode's canonical block above in "
      "full first, then append the extra words. Delete nothing.**")
    a("")
    a("**Additions common to all six** (thumbnail composition, hands, readable matter):")
    a("")
    a("> " + ", ".join(COMMON_ADD))
    a("")
    a("---")
    a("")
    a("## 4. The rules that have bitten, stated once")
    a("")
    a("1. **No readable text, numeral, signature, badge or logo anywhere** - and it is ordered in "
      "the **POSITIVE** prompt, identically in all six, because a `[NEG]` ban alone failed twice on "
      "EP66 `L146`:")
    a("")
    a("   > " + NOTEXT)
    a("")
    a("2. **Documents are shapes.** Printed paper is ordered as grey ruled blocks and an "
      "engineering drawing as plain grey construction lines, both in the positive prompt:")
    a("")
    a("   > " + GREYBARS)
    a("")
    a("   > " + DRAWLINES)
    a("")
    a("3. **Hands: countable, unfused fingers.** EP66 `L236` failed twice on a raised hand. The fix "
      "that worked was resting it flat on a surface, and that geometry is in all six bodies "
      "verbatim. **No plate below has anyone gripping, holding up or interlocking anything**; pens "
      "and rules lie loose, held by nobody.")
    a("")
    a("   > " + HANDS)
    a("")
    a("4. **The face is specified, not hoped for**, identically in all six:")
    a("")
    a("   > " + FACE)
    a("")
    a("---")
    a("")
    a("## 5. THE SIX PLATES")
    a("")
    n = 0
    for ep in EPISODES:
        a(f"### {ep['ep']} {ep['slug']} - {ep['title']}")
        a("")
        a(f"**Save both to `{ep['dir']}\\`.** Era for both: {ep['era']}.")
        a("")
        a(f"**Never depict.** {ep['barred']}")
        a("")
        a(f"**`[NEG]` tension to know about.** {ep['neg_tension']}")
        a("")
        for plate in ep["plates"]:
            n += 1
            body = render_body(ep, plate)
            a(f"#### `{plate['id']}.png` - {plate['variant']}")
            a("")
            a(f"**Ledger.** {plate['ledger']}")
            a("")
            a(f"**Why this plate.** {plate['why']}")
            a("")
            a(f"**Type it carries** (PACKAGING section 2, measured, unchanged): headline "
              f"`{plate['headline']}` - {plate['headline_ink']} - kicker `{plate['kicker']}` - "
              f"accent {plate['accent']}. **The type is burned in later by "
              f"`scripts/build_ep62_65_thumbnails.py`; it is not in the plate.**")
            a("")
            a("**Prompt:**")
            a("")
            a("```")
            a(body)
            a("```")
            a("")
            a(f"**Save as:** `{ep['dir']}\\{plate['id']}.png`")
            a("")
    a("---")
    a("")
    a("## 6. After delivery")
    a("")
    a("1. **Look at all six on a labelled contact sheet.** The factory-shelf incident and EP65's "
      "three identifiable elderly women both got through machine gates. A face plate is the one "
      "kind of plate where the eye is the only instrument that works.")
    a("2. Check each face against the barred list in section 5 for that episode. If a plate reads "
      "as a real person, it is rejected outright - there is no repair.")
    a("3. `py -3.11 scripts/check_image_order_neg.py --file "
      "episodes/_planning/EP67_69_THUMBS_PEOPLE_CODEX.v001.md`")
    a("4. Build the candidate through `scripts/build_ep62_65_thumbnails.py` with the headline and "
      "kicker above unchanged, then measure `thumb_subject_luma` (subject box x 0.20-0.80, y "
      "0.12-0.88, mean luma >= 60; tallest bright connected component >= 150 px; dark outline ring "
      ">= 12 px) and `thumbnail_visibility` (selected thumb mean luma >= 33).")
    a("5. **Run each new candidate against that episode's existing `T001`-`T006`, not instead of "
      "them.** The measurement that matters is whether a face beats a still life on this channel, "
      "and it only exists if both are in the test.")
    a("")
    return "\n".join(L) + "\n"


# --------------------------------------------------------------------------------------------
# Output 2: the merged paste file. One file. The owner has asked repeatedly not to be handed a
# directory of chunks.
# --------------------------------------------------------------------------------------------
def build_paste() -> str:
    L: list[str] = []
    a = L.append
    a("EP67 / EP68 / EP69 - サムネ用「顔が見える」プレート **全 6 枚**")
    a("EP67 ramirez: T007.png, T008.png ／ EP68 pinto: T009.png, T010.png ／ "
      "EP69 hyatt: T011.png, T012.png")
    a("")
    a("★このファイル1本に**全 6 枚**が入っています。分割ファイルはありません。")
    a("　上から順に、**1プロンプト＝1枚**で生成してください。")
    a("　複数のプロンプトをまとめて1枚にしない。同じプロンプトで2枚目を作らない。")
    a("　新しい ID を作らない。`_v2` / `_02` / `_A` を作らない。**名前は ■ のとおりちょうど。**")
    a("")
    a("★★ **保存先は3つあります。同じフォルダに入れないでください。** ★★")
    for ep in EPISODES:
        ids = " / ".join(f"{p['id']}.png" for p in ep["plates"])
        a(f"　{ids}  ->  {ep['dir']}\\")
    a("")
    a("──────── この6枚に共通の指定 ────────")
    a("")
    a("各プロンプト末尾の [TSTYLE] は、次の文言に置き換えてください（本編カットの [STYLE] は使いません。")
    a("本編の [STYLE] は low contrast 指定で、EP65 のサムネ4枚が地味になった原因そのものです）:")
    a("")
    a(TSTYLE)
    a("")
    a("　硬い一灯・高コントラスト・明るい露出。**顔がはっきり見えること**が今回の全目的です。")
    a("　**画面の上40%は何も無い一様な面**（見出し文字を焼き込む場所）。頭も上40%に入れない。")
    a("　被写体は下60%、下1/3が一番明るい。")
    a("")
    a("★ **人物は必ず入れてください。顔もはっきり描いてください。**（オーナー決定 2026-07-04）")
    a("　禁止なのは「実在する特定の人物に似ていること」だけです。有名人・公人・実在の誰かの肖像は不可。")
    a("　各プロンプト本文に「完全に架空の人物」と書いてあります。その通りに作ってください。")
    a("")
    a("★ **Avoid: [NEG] は話ごとに違います。**同じ文言を3話に使い回さないでください。")
    a("　各プロンプトの直前に、その話の [NEG] を書いてあります。**そこから1語も削らないでください。**")
    a("　[NEG] の後ろに「, ○○, ○○」と語が続く場合は、[NEG] を全部展開したうえで末尾に足してください。")
    a("")
    a("★ **文字・数字・署名・バッジ・ロゴは画面のどこにも出さない。**")
    a("　書類は「読めない灰色の帯」、図面は「読めない灰色の線」として描いてください（本文に指定済み）。")
    a("　手は必ず面に平置き。指は1本ずつ離して数えられること。ペンや定規は置くだけで、握らせない。")
    a("")
    a("★ **長辺 3840px 以上。**各プロンプト本文にも書いてあります。小さいファイルは使えません。")
    a("")
    for ep in EPISODES:
        a("════════════════════════════════════════════════════════════")
        a(f"{ep['ep']} {ep['slug']}  ／  保存先 {ep['dir']}\\")
        a("════════════════════════════════════════════════════════════")
        a("")
        a(f"この2枚の Avoid: [NEG] は、次の文言に置き換えてください（{ep['ep']} 専用）:")
        a("")
        a(NEG[ep["slug"]])
        a("")
        a("この話で絶対に描いてはいけないもの:")
        a(ep["barred"])
        a("")
        for plate in ep["plates"]:
            a(f"■ {plate['id']}.png     （保存先 {ep['dir']}\\{plate['id']}.png）")
            a(render_body(ep, plate))
            a("")
    a("──────── 保存 ────────")
    a("")
    a("生成した画像は上の ■ の名前ちょうどで保存してください。")
    a("**保存先は3つに分かれています:**")
    for ep in EPISODES:
        ids = " / ".join(f"{p['id']}.png" for p in ep["plates"])
        a(f"　{ids}  ->  {ep['dir']}\\")
    a("長辺 3840px 以上・16:9・PNG。")
    a("")
    a("納品後: 6枚を1枚のコンタクトシートに並べて**目で見てください**。")
    a("実在の人物に見えるものが1枚でもあれば、それは修正ではなく不採用です。")
    a("")
    return "\n".join(L) + "\n"


# --------------------------------------------------------------------------------------------
# Measurement
# --------------------------------------------------------------------------------------------
IDENTIFIABILITY = ("recognisable person", "identifiable person", "likeness of a real individual",
                   "portrait of a named person", "celebrity", "public figure", "deepfake")
BANNED_IN_NEG = ("human face", "facial features", "eyes")
BANNED_IN_ADDITIONS = ("face", "head", "person in frame")


def verify(doc: str, paste: str) -> int:
    bad = 0

    def line(ok: bool, msg: str) -> None:
        nonlocal bad
        if not ok:
            bad += 1
        print(f"  {'PASS' if ok else 'FAIL'}  {msg}")

    plates = list(all_plates())
    print("\n=== 1. prompt count and names ===")
    line(len(plates) == 6, f"prompt count = {len(plates)} (want 6)")
    names = [f"{p['id']}.png" for _, p, _ in plates]
    line(len(set(names)) == 6, f"distinct save names = {len(set(names))} -> {', '.join(names)}")
    dirs = {ep["dir"] for ep, _, _ in plates}
    line(len(dirs) == 3, f"distinct save directories = {len(dirs)}")
    for _, plate, body in plates:
        line(f"[TSTYLE] Avoid: [NEG]," in body, f"{plate['id']} carries [TSTYLE] and Avoid: [NEG],")
        line(body.count(RES) == 1 and body.index(RES) < body.index("[TSTYLE]"),
             f"{plate['id']} 3840 sentence present exactly once, before the style token")

    print("\n=== 2. control characters ===")
    for name, blob in (("doc", doc), ("paste", paste)):
        ctrl = {c: blob.count(c) for c in set(blob)
                if unicodedata.category(c) == "Cc" and c != "\n"}
        line(not ctrl, f"{name}: control chars other than LF = {ctrl or 'none'}")
        line("\r" not in blob, f"{name}: no CR")
        line("\x07" not in blob, f"{name}: no BEL")

    print("\n=== 3. [NEG] byte-identity against each episode's own batch A ===")
    for ep in EPISODES:
        src = lift_neg(NEG_SOURCE[ep["slug"]])
        mine = NEG[ep["slug"]]
        line(src == mine, f"{ep['slug']}: lifted == in-memory ({len(mine)} bytes)")
        line(f"\n{mine}\n" in paste or mine in paste,
             f"{ep['slug']}: the exact block appears in the paste file")
        line(f"> {mine}" in doc, f"{ep['slug']}: the exact block appears in the doc")
    negs = [NEG[e["slug"]] for e in EPISODES]
    line(len(set(negs)) == 3, "the three [NEG] blocks are three different blocks, not one reused")

    print("\n=== 4. [NEG] token families ===")
    for ep in EPISODES:
        low = NEG[ep["slug"]].lower()
        miss = [t for t in IDENTIFIABILITY if t not in low]
        line(not miss, f"{ep['slug']}: all 7 identifiability tokens present"
                       f"{'' if not miss else ' - missing ' + ', '.join(miss)}")
        hit = [t for t in BANNED_IN_NEG if t in low]
        line(not hit, f"{ep['slug']}: banned tokens {BANNED_IN_NEG} count = {len(hit)}"
                      f"{'' if not hit else ' -> ' + ', '.join(hit)}")

    print("\n=== 5. per-plate [NEG] additions carry no person-suppressing token ===")
    for ep in EPISODES:
        adds = COMMON_ADD + ep["neg_add"]
        toks = [t.strip().lower() for t in adds]
        hit = [t for t in toks if t in BANNED_IN_ADDITIONS]
        line(not hit, f"{ep['slug']}: bare 'face' / 'head' / 'person in frame' as an addition = "
                      f"{len(hit)}")
        hit2 = [t for t in toks for b in BANNED_IN_NEG if b in t]
        line(not hit2, f"{ep['slug']}: 'human face' / 'facial features' / 'eyes' inside an "
                       f"addition = {len(hit2)}")

    print("\n=== 6. identical-clause counts across the six bodies ===")
    bodies = [b for _, _, b in plates]
    for label, clause, want in (("upper-40 clause", UPPER40, 6),
                                ("3840 sentence", RES, 6),
                                ("no-readable-character clause", NOTEXT, 6),
                                ("flat-hand clause", HANDS, 6),
                                ("invented-face clause", FACE, 6)):
        got = sum(b.count(clause) for b in bodies)
        line(got == want, f"{label}: {got} occurrences across the 6 bodies (want {want})")
    got = sum(b.count(GREYBARS) for b in bodies)
    line(got == 4, f"grey-ruled-blocks clause: {got} (want 4 - the paper plates)")
    got = sum(b.count(DRAWLINES) for b in bodies)
    line(got == 2, f"grey-construction-lines clause: {got} (want 2 - the EP69 drawing plates)")
    line(doc.count(UPPER40) >= 7 and paste.count(UPPER40) >= 7,
         f"upper-40 clause in doc={doc.count(UPPER40)} paste={paste.count(UPPER40)} "
         f"(6 bodies + the [TSTYLE] definition)")

    print("\n=== 7. bodies are byte-identical between the two outputs ===")
    for _, plate, body in plates:
        line(body in doc and body in paste,
             f"{plate['id']}: same {len(body)}-char body in both files")

    print("\n=== 8. a prompt may not contradict itself ===")
    # Two defects found by reading the first build of this file, now mechanised.
    # (a) the shared face clause carried "HIS ... He is" and one of the six subjects is a woman.
    gendered = re.findall(r"\b(his|he|her|she|him|hers)\b", FACE, re.I)
    line(not gendered, f"shared face clause carries no gendered pronoun {gendered or ''}")
    # (b) T009 said the folder was HELD at waist height while the shared hand clause says the hand
    #     is flat on a surface. Every body must anchor a hand on a surface and hold nothing.
    for _, plate, body in plates:
        line("RESTS ON" in body, f"{plate['id']}: a hand is anchored on a named surface")
        held = re.findall(r"\b(holds|holding|gripped|gripping|clutch\w*)\b", body, re.I)
        line(not held, f"{plate['id']}: nothing is held in a hand {held or ''}")
        line("held by nobody" in body,
             f"{plate['id']}: loose objects are stated as unheld")

    print("\n=== 9. no shell command, no template hole, ASCII bodies ===")
    for _, plate, body in plates:
        line("{" not in body and "}" not in body, f"{plate['id']}: no unfilled placeholder")
        line(not re.search(r"\$\(|`|\|\||&&|\bpy -3\.11\b", body),
             f"{plate['id']}: no shell syntax in the prompt")
        nonascii = sorted({c for c in body if ord(c) > 127})
        line(not nonascii, f"{plate['id']}: body is pure ASCII {nonascii if nonascii else ''}")
    line("[STYLE]" not in "".join(bodies), "no body uses the canonical [STYLE]")

    print(f"\n{'ALL CHECKS PASS' if not bad else str(bad) + ' CHECK(S) FAILED'}")
    return 1 if bad else 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--verify", action="store_true", help="measure without writing")
    args = ap.parse_args()

    doc, paste = build_doc(), build_paste()
    if not args.verify:
        DOC_OUT.write_text(doc, encoding="utf-8", newline="\n")
        PASTE_OUT.write_text(paste, encoding="utf-8", newline="\n")
        print(f"[build] wrote {DOC_OUT.relative_to(ROOT)} ({len(doc)} chars)")
        print(f"[build] wrote {PASTE_OUT.relative_to(ROOT)} ({len(paste)} chars)")
    return verify(doc, paste)


if __name__ == "__main__":
    raise SystemExit(main())
