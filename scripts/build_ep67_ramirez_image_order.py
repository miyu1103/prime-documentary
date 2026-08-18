#!/usr/bin/env python3
"""Emit EP67 ramirez's Codex image order (.md) and its paste files from ONE data source.

Why one source: EP66's batch C and D matched byte for byte between the order document and the
paste files because both were generated from the same PLATES list. Anything hand-copied drifts,
and a drifted prompt body is a plate nobody can trace back to a beat.

    py -3.11 scripts/build_ep67_ramirez_image_order.py            # write + verify
    py -3.11 scripts/build_ep67_ramirez_image_order.py --verify   # verify only, write nothing

The canonical [NEG] is READ OUT OF EP66's batch D document at generation time, not retyped, so
it is byte-identical by construction. The generator refuses to write if that read fails, if the
identifiability tokens are missing, or if any of the three tokens that caused EP66's 191-plate
rebuild (`human face`, `facial features`, `eyes`) have come back.
"""
from __future__ import annotations

import argparse
import re
import re as _re
import sys
import unicodedata
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:  # pragma: no cover
    pass

ROOT = Path(__file__).resolve().parents[1]
PLANNING = ROOT / "episodes" / "_planning"
BATCH_D = PLANNING / "EP66_openfields_CODEX_BATCH_D.v001.md"
OUT_MD = PLANNING / "EP67_ramirez_CODEX_BATCH_A.v002.md"
OUT_PASTE = PLANNING / "EP67_ramirez_CODEX_PASTE_A"
SAVE_DIR = r"H:\pd-media\assets\ai\ramirez"

# ---------------------------------------------------------------------------------------------
# style blocks
# ---------------------------------------------------------------------------------------------
# [STYLE] is EP67's own: Dublin, CALIFORNIA, 2011-2026 (episode_spec.era_setting). It is NOT
# batch D's -- that one says "late Appalachian autumn, rural Pennsylvania and Middle Tennessee",
# which is the wrong continent's weather for this film.
STYLE = (
    "cinematic still, photographic, restrained documentary framing, muted natural colour, "
    "low contrast but never crushed: shadows keep their detail and the frame reads clearly on a "
    "phone screen, soft falloff toward the edges, shallow depth of field, ordinary suburban and "
    "civic California in the United States between 2011 and 2026, plain worn everyday surfaces, "
    "nothing staged for advertising, nothing in shot that would date the picture outside those "
    "years, ultra-detailed, photoreal, 4K, 16:9, fine film grain, no text, no lettering, "
    "no numerals, no watermark, no logo, no signage"
)

# [HSTYLE] is the plan's own preamble for R073-R096, joined to one line and otherwise unaltered
# (EP67_ramirez_CODEX_BATCH_A.v001.md section 3).
HSTYLE = (
    "photographic, 35mm, natural light, real adults, ordinary clothing, ordinary bodies, "
    "believable American setting, candid framing, no styling, no beauty retouching, "
    "no model look, no stock-photo smiles, faces neutral and unremarkable, "
    "nobody looking at the lens"
)


# Thumbnails get their own [STYLE] and that is deliberate. The canonical [STYLE] above asks for
# low contrast, which is right for a film frame and is exactly why EP65's four thumbnail
# candidates came back dull and had to be re-ordered. A thumbnail is not a film frame.
THUMB_STYLE = (
    "editorial photographic still made to be a video thumbnail, ONE HARD DIRECTIONAL KEY LIGHT "
    "from the side, HIGH CONTRAST AND BRIGHT OVERALL EXPOSURE, the subject clearly brighter than "
    "everything behind it and cleanly separated from it, shadow only where it defines an edge and "
    "never filling the frame, THE ENTIRE UPPER 40 PERCENT OF THE FRAME IS ONE UNBROKEN UNIFORM "
    "FIELD - plain wall, plain sky or plain out-of-focus darkness, with no object, no edge, no "
    "horizon and no detail crossing it anywhere - and the whole subject sits inside the lower 60 "
    "percent with the bottom third the brightest part of the picture, ordinary suburban and civic "
    "California in the United States between 2011 and 2026, ultra-detailed, photoreal, 4K, 16:9, "
    "no text, no lettering, no numerals, no watermark, no logo, no signage"
)


def read_canonical_neg() -> str:
    """Lift batch D's [NEG] out of its own document. Never retyped."""
    text = BATCH_D.read_text(encoding="utf-8")
    cands = [l for l in text.splitlines()
             if l.lstrip().startswith(">") and re.search(r"\btext\b.*\blettering\b", l, re.I)]
    if not cands:
        raise SystemExit(f"no canonical [NEG] blockquote found in {BATCH_D.name}")
    return max(cands, key=len).lstrip("> ").strip()


NEG = read_canonical_neg()

# ---------------------------------------------------------------------------------------------
# reusable clauses. Defined once so 130 plates cannot say them 130 slightly different ways.
# ---------------------------------------------------------------------------------------------
# The POSITIVE ordering for paper. EP66's L146 proved a [NEG] ban alone does not hold: the
# wordmark came back twice after being banned twice. The generator must ASK FOR a shape.
GREY_RULE = (
    "The paper carries no writing of any kind, and this is what is on it instead: EVENLY SPACED "
    "FLAT GREY HORIZONTAL BARS of one uniform width and one uniform weight, laid in parallel "
    "like ruled bands of tone, each bar a solid unbroken block of soft grey with straight ends "
    "and no letter shapes, no word shapes, no gaps between words and no broken or ragged edge "
    "anywhere along it, so the sheet reads as printed matter purely by its rhythm of grey and "
    "white and carries not one readable character"
)
BLANK_PAPER = (
    "The sheet is completely blank: an unbroken field of off-white paper with no print, no "
    "ruling, no letterform, no number and no mark of any kind on it"
)
FLAT_HAND = (
    "THE HAND IS AT REST FLAT ON THE SURFACE, not raised and not held in the air, the palm laid "
    "down in full contact with it and the wrist straight, THE FOUR FINGERS LYING SIDE BY SIDE "
    "AND SEPARATE with a visible line of shadow between each pair and one nail showing on each, "
    "and the thumb clearly apart from the fingers along the near side"
)
NO_BRAND = (
    "No vehicle anywhere in this frame carries a mark of any kind: no badge, no emblem, no oval "
    "on the grille, no wordmark, no nameplate, no model lettering, no dealer sticker and no "
    "plate of any kind on any part of any of them, front or rear"
)
NO_SCREEN = (
    "The screen is never legible: it is a single soft bloom of even light with no icons, no "
    "windows, no rows, no cursor and nothing that could be read as a document"
)
DRAWER_RIG = (
    "The identical camera position, lens and light as every other plate in this drawer set: a "
    "plain dark-wood office desk photographed square-on from a seated eye height about four feet "
    "away, the drawer front filling the lower middle third of the frame and its two straight "
    "horizontal edges level with the bottom of the frame, one soft north window light coming "
    "from the left and falling away to the right, and nothing on the desk except what is named "
    "here"
)

# common per-plate [NEG] additions
N_PAPER = ("readable document, printed words on paper, letterforms, typed lines, printed "
           "paragraph, form fields with labels, letterhead, stamp with words")
N_BRAND = ("licence plate, registration plate, number plate, badge on the grille, oval emblem, "
           "manufacturer wordmark, chrome nameplate, dealership signage, price sticker, "
           "window sticker")
N_SCREEN = "readable screen, spreadsheet on a monitor, web page, icons, cursor, user interface"
N_HAND = ("fingers fused into one mass, fingers merged, webbed fingers, mitten hand, stub "
          "fingers, missing thumb, extra fingers, six fingers, malformed hand, interlocked "
          "fingers, raised hand, hand held up in the air, blurred hand")
N_COURT = ("courtroom, judge's bench, jury box, witness stand, gavel, scales of justice, "
           "state seal, carved motto, engraved lettering on stone, banner, memorial plaque")
N_EU = ("European streetscape, Irish town, Georgian doorway, EU number plate, foreign-language "
        "signage, cobbled lane, thatched roof, tram")

# ---------------------------------------------------------------------------------------------
# the plates. (id, lane, body, neg_add, script_line, ledger)
# `lane` keys into LANES below and decides which paste file a plate lands in and whether the
# [HSTYLE] preamble is prepended.
# ---------------------------------------------------------------------------------------------
P: list[tuple[str, str, str, str, str, str]] = [

    # ---------------------------------------------------------------- A1 the dealership counter
    ("R001", "A1",
     "A wide of a car showroom interior seen from the customer's side of the floor at eye height: "
     "a polished pale floor running away to a full-height glass wall, flat Californian midday "
     "coming through it, two plain mid-size saloon cars parked at an angle on the floor with "
     f"nobody anywhere in the frame. {NO_BRAND}, and there is no dealership signage, no banner, "
     "no price board and no poster anywhere on the walls or the glass. Every surface is bare "
     "painted plasterboard, glass or floor",
     f"{N_BRAND}, {N_EU}, showroom banner, wall poster, price board, balloons, sales pennant",
     "Dublin, California. February 27th, 2011.", "SR-01"),

    ("R002", "A1",
     "A sales desk seen from just behind and above a customer's shoulder, the shoulder a soft "
     "dark mass at the very bottom edge of the frame and out of focus: the desk edge crosses the "
     "middle of the frame, a slim computer monitor stands at the far side TURNED AWAY so only its "
     f"plain back panel and a spill of light round its edge are visible. {NO_SCREEN}. A keyboard "
     "lies flat in front of it and a single set of car keys sits on the far corner of the desk "
     "just out of reach. The desk top is bare wood-effect laminate with no paper on it. Bright "
     "showroom daylight from the left",
     f"{N_SCREEN}, {N_PAPER}, {N_BRAND}, face, head, second person in frame",
     "The salesman runs a credit check, and says Nissan will not sell him the car.", "SR-02 / SR-03"),

    ("R003", "A1",
     "The same sales desk from the same camera position, now with nobody at it at all: the chair "
     "on the far side stands empty and slightly turned out, the keys are still on the far corner "
     f"where they were, the monitor is still turned away. {NO_SCREEN}. Nothing on the desk has "
     "moved. Bright showroom daylight from the left, the floor beyond soft and out of focus",
     f"{N_SCREEN}, {N_PAPER}, person in the chair, hands in frame",
     "That is the entire record of what was said at that counter.", "ND-08"),

    ("R004", "A1",
     "A close, shallow-focus still of a single set of car keys lying on a laminate desk top, the "
     "fob a plain unmarked black plastic rectangle with no buttons legible and no maker's mark, "
     "the ring and two cut keys lying flat beside it, everything beyond the keys dissolving into "
     "soft bright showroom bokeh. Nobody in frame, no hand near them, nothing else on the desk",
     f"{N_BRAND}, keyring tag, engraved key, buttons with symbols, hand, fingers",
     "The salesman runs a credit check, and says Nissan will not sell him the car.", "SR-03"),

    ("R005", "A1",
     "A computer monitor photographed from directly behind it, so the frame is filled by the "
     "plain matte back panel of the case and its plain stand, with the light of the screen "
     "spilling out around the edges of the panel onto the desk and the wall as a soft even glow. "
     "NOT ONE PIXEL OF THE SCREEN ITSELF IS VISIBLE from this angle. No cable labels, no vents "
     "shaped like letters, no maker's mark on the case. Bright interior daylight",
     f"{N_SCREEN}, front of the monitor, reflected screen content, brand logo on the bezel",
     "What came back was a report produced by TransUnion …", "SR-02"),

    ("R006", "A1",
     "A plain black computer keyboard photographed from directly overhead, filling most of the "
     "frame at a slight angle, THE KEYCAPS ALL COMPLETELY BLANK — smooth unmarked squares of dark "
     "plastic with no letters, no numbers and no symbols printed on any of them — and the hard "
     "shadow of a hand and forearm falling across the left half of the keys from outside the "
     "frame. The hand itself is not in shot, only its shadow. Laminate desk visible around the "
     "edges",
     f"{N_PAPER}, letters on the keycaps, symbols on the keys, hand in frame, fingers",
     "The dealership ran his credit, the way a dealership does.", "SR-02"),

    ("R007", "A1",
     "The driver's door and front side window of a plain mid-size saloon car seen square on from "
     "outside at standing height, filling the frame from edge to edge, a clean reflection of pale "
     f"sky and a soft line of parked cars sliding across the glass. {NO_BRAND}. The door handle is "
     "a plain flush chrome bar, the mirror housing is unpainted plastic with nothing on it, and "
     "there is no writing on the glass and no sticker in the corner of the window. Flat "
     "Californian midday",
     f"{N_BRAND}, {N_EU}, inspection sticker, VIN plate, reflection of a person",
     "Sergio Ramirez has come to buy a Nissan Maxima.", "SR-01"),

    ("R008", "A1",
     "A car forecourt at midday: four straight rows of parked cars on hot pale asphalt seen from "
     "standing height at one corner of the lot, heat shimmer rising off the far row, low dry "
     "planting and a plain kerb along the far edge, a flat pale sky above. Nobody in the frame "
     f"and no movement in it. {NO_BRAND}. No price stickers on any "
     "windscreen, no flags, no pennants and no signage of any kind on the lot",
     f"{N_BRAND}, {N_EU}, windscreen price sticker, bunting, flags on poles, dealer sign",
     "Dublin, California. February 27th, 2011.", "SR-01"),

    ("R009", "A1",
     "A full-height showroom glass wall seen from outside on the forecourt, the interior behind it "
     "gone dim and grey because the glass is carrying a bright reflection of the empty lot and the "
     "sky: the cars inside read only as faint dark shapes through the reflection. The glass has no "
     "lettering, no vinyl graphics, no opening hours and no logo on it anywhere. Flat midday light, "
     "nobody in frame",
     f"{N_BRAND}, {N_EU}, vinyl lettering on glass, opening hours, decal, reflection of a person",
     "His name is on a terrorist list.", "SR-03"),

    ("R010", "A1",
     "An empty customer chair at a sales desk, photographed straight on from the far side of the "
     "desk at seated eye height: a plain fabric office chair pushed back a few inches and slightly "
     "askew, the near edge of the desk crossing the bottom of the frame as a dark bar, bright "
     "showroom floor and soft glass beyond. Nothing on the desk, nobody in the frame",
     f"{N_PAPER}, person seated, coat over the chair",
     "He was not a party. He is not named anywhere in either opinion.", "ND-08"),

    ("R011", "A1",
     "A plain grey office printer standing on a low cabinet against a pale wall, seen from the "
     "side at chest height, a single sheet of paper halfway out of its output slot and hanging "
     f"slightly. {BLANK_PAPER}. The printer's own panel is a blank dark rectangle with no icons and "
     "no display, and the machine carries no maker's mark. Soft interior daylight",
     f"{N_PAPER}, {N_SCREEN}, printed page, control panel icons, brand logo on the printer",
     "What came back was a report produced by TransUnion …", "SR-02"),

    ("R012", "A1",
     "A plain unmarked black car key fob lying at the centre of a single contract-sized sheet of "
     f"paper on a laminate desk, photographed from directly overhead. {BLANK_PAPER} — it is a "
     "completely empty white rectangle with two soft fold-creases across it and nothing printed "
     "anywhere, no signature line, no boxes, no small print at the foot. Even light from a window "
     "to the left",
     f"{N_PAPER}, signature line, printed clauses, small print, boxes with labels",
     "His wife bought the car in her own name.", "SR-04"),

    ("R013", "A1",
     "The forecourt seen from inside the showroom through the open front door at the end of the "
     "day: the door frame makes a dark vertical border down both sides of the frame, low late sun "
     "coming in almost level and laying a long bright wedge across the floor tiles in the "
     "foreground, the parked cars outside reduced to dark shapes against the glare. Nobody in "
     "frame, no signage on the door or the glass",
     f"{N_BRAND}, {N_EU}, opening hours on the door, vinyl lettering, sunset orange grade",
     "So that is one man, over about a week, in one town.", "SR-01"),

    ("R014", "A1",
     "A close of a car's wing mirror seen from just behind and to the side, filling the right half "
     "of the frame, the mirror glass carrying a small sharp reflection of an empty asphalt "
     "forecourt with two distant parked cars on it and a pale sky. The mirror housing is plain "
     "unpainted plastic with nothing written on it, and there is no warning text etched into the "
     "mirror glass. Flat daylight",
     f"{N_BRAND}, etched warning text on the mirror, reflection of a person, {N_EU}",
     "A car he did not buy.", "SR-04"),

    ("R015", "A1",
     "An overhead of a working desk top, filling the frame: a keyboard with COMPLETELY BLANK "
     "UNMARKED KEYCAPS, a plain grey mouse, a set of car keys, and a plain white mug with nothing "
     "printed on it, arranged the way a desk actually is rather than composed. No paper anywhere "
     "on the desk. Even overhead interior light, laminate grain visible",
     f"{N_PAPER}, letters on the keycaps, printed mug, notepad, sticky notes",
     "Nobody in this film knows what the salesman was looking at …", "⛔-08"),

    ("R016", "A1",
     "A back-of-house corridor in a commercial building, photographed straight down its length at "
     "eye height: pale painted breeze-block walls, a hard-wearing grey floor, four plain flush "
     "doors in a row on the right and one at the far end, all closed, ALL OF THEM WITH BARE FACES "
     "— no numbers, no nameplates, no signs, no notices. Even fluorescent light from a run of "
     "fittings overhead, nobody in the frame",
     f"{N_PAPER}, door numbers, nameplate, fire notice, exit sign, {N_EU}",
     "because no court ever asked him", "ND-08"),

    ("R017", "A1",
     "The same car forecourt as the wide daylight lot, now with ONE EMPTY BAY IN THE MIDDLE OF AN "
     "OTHERWISE FULL ROW: the painted bay lines make a clear rectangle of bare pale asphalt with a "
     "car parked tight on either side of it, and the asphalt inside the empty bay is very slightly "
     "cleaner than the asphalt around it. Same standing height and same flat light as the earlier "
     f"forecourt plate, nobody in frame. {NO_BRAND}",
     f"{N_BRAND}, {N_EU}, numbers painted in the bay, reserved sign, person, dusk",
     "Two words. A first name and a last name. That was the whole comparison.", "SR-04 / LS-14"),

    # ------------------------------------------------------------------- A2 the two mailings
    ("R018", "A2",
     "A plain white business envelope lying FACE DOWN on a bare wooden kitchen table, "
     "photographed from a low three-quarter angle a foot away, ONE CORNER OF THE FLAP LIFTED "
     "SLIGHTLY AND STANDING PROUD of the table so it catches the light. Low warm morning sun "
     "comes across the table from the left and lays the envelope's own shadow to the right. The "
     "envelope is entirely unmarked: no address, no window, no stamp, no franking, no return "
     "corner, no printing on the flap. The lower third of the frame — the bare table in front of "
     "the envelope — is the brightest part of the picture",
     f"{N_PAPER}, address block, postage stamp, franking mark, window envelope, return address, "
     "barcode",
     "The letter that follows will not say how to argue with it.", "SR-10"),

    ("R019", "A2",
     "The same plain white envelope on the same bare wooden kitchen table in the same morning "
     "light, now lying FACE UP AND FLAT, sealed, its front a completely empty white rectangle: no "
     "address, no name, no window, no stamp, no franking, no printing of any kind on it. Same low "
     "three-quarter angle, same distance, the table grain running away to the right",
     f"{N_PAPER}, address block, postage stamp, franking mark, window envelope, barcode",
     "The next day, Ramirez asked TransUnion for his own credit file.", "SR-05"),

    ("R020", "A2",
     "TWO plain white envelopes lying side by side and slightly overlapping on the same bare "
     "wooden kitchen table, ONE CLEARLY LARGER AND DEEPER THAN THE OTHER so the difference in size "
     "is the subject of the picture, both face up and both completely blank — no address, no "
     "window, no stamp, no franking, no printing at all on either. Morning light from the left, "
     "seen from a low three-quarter angle",
     f"{N_PAPER}, address block, postage stamp, window envelope, franking, barcode",
     "He had two mailings in front of him now.", "SR-09"),

    ("R021", "A2",
     "A plain white envelope lying on a wooden kitchen table with its flap TORN RAGGEDLY OPEN "
     "along the top edge, the torn paper fibres standing up along the tear, the mouth of the "
     "envelope gaping slightly but ANGLED AWAY FROM THE CAMERA SO NOTHING INSIDE IT CAN BE SEEN — "
     "the interior is a flat dark gap. The envelope's face is blank. Morning light from the left",
     f"{N_PAPER}, contents visible, letter emerging, address block, stamp",
     "The day after that, a second envelope arrived.", "SR-05"),

    ("R022", "A2",
     "A single sheet of paper, folded in three and lying open-side-down across the envelope it "
     f"came out of, on a bare wooden kitchen table, photographed from overhead. {GREY_RULE}. The "
     "envelope beneath it is blank. Morning light from the left, the fold creases catching a soft "
     "highlight",
     f"{N_PAPER}, printed paragraphs, headings, bullet points, letterhead, signature",
     "It came with the standard federal summary of a consumer's rights …", "SR-05"),

    ("R023", "A2",
     "A stack of three folded sheets of paper lying on a wooden table, photographed from a very "
     "low angle almost level with the table so that ONLY THE FOLDED EDGES AND THE THICKNESS OF THE "
     "STACK ARE VISIBLE and no printed face of any sheet is turned toward the camera: the picture "
     "is three pale horizontal bands of paper edge with fine shadow between them. Morning light "
     "from the left, everything beyond the stack soft",
     f"{N_PAPER}, printed face visible, text on the edge, page numbers",
     "and it did not enclose another copy of his rights", "SR-05"),

    ("R024", "A2",
     "A domestic letter slot seen from INSIDE a house, on the inside face of a painted front door, "
     "at chest height and square on: the sprung brass flap is pushed up and one plain white "
     "envelope is halfway through it, held in the slot, about to drop. The envelope's visible face "
     "is completely blank. The door is plain painted timber with no numbers, no nameplate and no "
     "notice on it. Cool daylight leaking round the door edge",
     f"{N_PAPER}, house numbers on the door, nameplate, address on the envelope, junk mail, "
     f"{N_EU}",
     "The day after that, a second envelope arrived.", "SR-05"),

    ("R025", "A2",
     "A kitchen table seen from a seated height about two feet back: a plain white blank envelope "
     "lying flat in the middle of the table and a half-drunk mug of coffee gone cold beside it "
     "with a dull skin on the surface, morning light across the table from a window out of frame "
     "left, an ordinary American kitchen soft and dim behind. Nobody in the frame. The envelope "
     "and the mug are both unmarked",
     f"{N_PAPER}, address on the envelope, printed mug, newspaper, phone on the table",
     "Ramirez testified that he was confused by them.", "SR-09"),

    ("R026", "A2",
     "The same kitchen table from the same seated height and the same morning light, now "
     "COMPLETELY CLEARED: bare wood from edge to edge, the grain and two old ring marks the only "
     "things in the lower half of the frame, the same soft kitchen behind. No envelope, no mug, "
     "nobody in the frame",
     f"{N_PAPER}, any object on the table, person",
     "TransUnion eventually removed the alert from his file.", "SR-11"),

    ("R027", "A2",
     "A plain white blank envelope lying on the cloth passenger seat of an ordinary car, "
     "photographed from the driver's side at head height looking down and across, the seat belt "
     "buckle and the door card visible at the edges, flat daylight coming through the side window "
     "and laying a soft bright patch across the seat. The envelope has no address, no stamp and no "
     "printing. Nobody in the car",
     f"{N_PAPER}, address block, stamp, {N_BRAND}, dashboard display, person",
     "He cancelled a trip he had planned.", "SR-10"),

    ("R028", "A2",
     "A single sheet of paper HELD UP FLAT AGAINST A BRIGHT WINDOW and backlit, filling most of "
     "the frame, the light coming through the fibres so the paper glows evenly — AND NOTHING SHOWS "
     "THROUGH IT: no reverse printing, no shadow of type, no watermark, no fold. It is a plain "
     "luminous rectangle. Two hands hold it at the lower corners, both flat against the paper with "
     "fingers straight and separate, seen only as dark silhouetted edges. The window frame is a "
     "soft dark cross behind",
     f"{N_PAPER}, {N_HAND}, reverse printing showing through, watermark, letterhead",
     "Neither one told him how to dispute anything.", "SR-10"),

    ("R029", "A2",
     "A plain kitchen waste bin seen from directly above with its lid open, mostly empty, ONE "
     "PLAIN WHITE ENVELOPE lying alone at the bottom of the liner, creased once across the middle "
     "and face up, completely blank. Dim domestic light from above, the bin's plastic rim making a "
     "bright ellipse around the dark interior",
     f"{N_PAPER}, address on the envelope, other rubbish with packaging, brand packaging",
     "A trip he did not take.", "SR-10"),

    ("R030", "A2",
     "A plain white envelope held flat against the pale metal door of a domestic refrigerator by a "
     "single plain magnet, photographed square on at chest height. The envelope is blank on both "
     "the face and the flap; the magnet is an unmarked coloured disc. The fridge door is bare "
     "around it — no photographs, no notes, no lists, no other magnets. Even kitchen daylight",
     f"{N_PAPER}, notes on the fridge, shopping list, photographs, novelty magnet with text",
     "One said nothing about any alert.", "SR-09"),

    ("R031", "A2",
     "TWO plain white blank envelopes lying flat side by side in the bottom of a shallow open "
     "desk drawer, seen from a standing three-quarter angle looking down into it, the drawer "
     "pulled out about two thirds and the rest of its interior empty dark wood. A hand is not in "
     "frame. Soft north light from the left catching the near edge of the drawer front. Both "
     "envelopes are entirely unmarked",
     f"{N_PAPER}, address block, stamp, other contents in the drawer, hand",
     "The other said he was a potential match to a Treasury list.", "SR-06"),

    # ---------------------------------------------------------------------- A3 the desk drawer
    ("R032", "A3",
     f"A closed office desk drawer. {DRAWER_RIG}. The drawer is fully shut and its front is plain "
     "unmarked wood with one plain brass handle and no label holder and no keyhole plate. ON THE "
     "DESK TOP ABOVE IT lies one plain white envelope, flat, face up, completely blank",
     f"{N_PAPER}, label holder on the drawer, address on the envelope, other objects on the desk",
     "The next day, Ramirez asked TransUnion for his own credit file.", "SR-05 · motif state 1"),

    ("R033", "A3",
     f"The same desk drawer OPEN ABOUT A HAND'S WIDTH. {DRAWER_RIG}. The gap above the drawer front "
     "is a flat black band and NOTHING INSIDE IT IS RESOLVED — no contents, no edges, no paper, "
     "just depth. The desk top above is bare. The brass handle catches one small highlight",
     f"{N_PAPER}, contents visible in the gap, files, folders with tabs",
     "Here is how it worked, in the Supreme Court's words.", "LS-14"),

    ("R034", "A3",
     f"The same desk drawer FULLY OPEN. {DRAWER_RIG}. The drawer is filled from front to back with "
     "ROWS OF IDENTICAL PLAIN CARDS STANDING ON EDGE, packed tight and all the same height, all "
     "the same off-white, their top edges making one continuous straight line across the drawer. "
     "EVERY CARD IS COMPLETELY BLANK — no tabs, no labels, no printing, no colour coding, no "
     "index. The picture is rhythm and repetition, not filing",
     f"{N_PAPER}, tabbed dividers, coloured tabs, handwritten labels, index cards with writing",
     "TransUnion did not compare any data other than first and last names.",
     "LS-14 · motif state 2"),

    ("R035", "A3",
     f"The same fully open drawer of identical blank cards. {DRAWER_RIG}. ONE SINGLE CARD near the "
     "middle of the row STANDS ABOUT AN INCH PROUD of all the others, breaking the straight top "
     "line, and casts a thin shadow down onto its neighbours. Every card, including the proud one, "
     "is completely blank",
     f"{N_PAPER}, writing on the raised card, tab, label, coloured card",
     "OFAC information was the only consumer-report data that TransUnion collected using name "
     "alone.", "LS-17"),

    ("R036", "A3",
     f"The same fully open drawer of identical blank cards, with ONE CARD MISSING: a narrow "
     f"vertical gap in the row where a single card has been taken out, the cards on either side "
     f"leaning very slightly into the space. {DRAWER_RIG}. All remaining cards completely blank",
     f"{N_PAPER}, writing on any card, hand in frame, card lying on the desk",
     "only one thousand, eight hundred and fifty-three of them … had their credit reports "
     "disseminated", "MN-02 · motif state 3"),

    ("R037", "A3",
     f"The same desk drawer CAUGHT IN THE ACT OF CLOSING. {DRAWER_RIG}. The drawer front is a "
     "third of the way out and MOTION-SMEARED HORIZONTALLY along its travel, the rows of blank "
     "cards inside pulled into soft horizontal streaks of off-white by the same movement while the "
     "desk top, the wall and the window light behind stay perfectly sharp. Nobody in frame and no "
     "hand on the handle",
     f"{N_PAPER}, hand on the drawer, whole frame blurred, writing on the cards",
     "as if someone wrote a defamatory letter and then stored it in her desk drawer",
     "HD-08 · motif state 4"),

    ("R038", "A3",
     f"The same desk drawer CLOSED and the desk top above it COMPLETELY BARE. {DRAWER_RIG}. "
     "Nothing on the desk at all — no envelope, no paper, no object — only wood grain, the two "
     "straight edges of the drawer front and one plain brass handle",
     f"{N_PAPER}, any object on the desk, hand",
     "A letter that is not sent does not harm anyone, no matter how insulting the letter is.",
     "HD-08"),

    ("R039", "A3",
     f"The same desk drawer CLOSED, and lying on the desk top above it A SINGLE SMALL SLIP OF "
     f"PAPER about the size of a docket slip, alone in the middle of the bare desk, catching the "
     f"window light. {BLANK_PAPER}. {DRAWER_RIG}. Nothing else on the desk",
     f"{N_PAPER}, printed slip, carbon copy lines, stamp, signature, numbers",
     "But why is it so speculative that a company in the business of selling credit reports to "
     "third parties will in fact sell a credit report to a third party?",
     "KG-04 · motif state 5"),

    ("R040", "A3",
     "The same desk and the same closed drawer SEEN FROM FURTHER BACK, about twelve feet away, so "
     "the desk now sits small in the lower middle of the frame and the whole of a plain empty "
     "office is visible around it: two other bare desks, a run of low cabinets, a bare wall, one "
     "window on the left going blue with dusk while the room falls to shadow. Nobody in the room. "
     "No notices, no whiteboard, no posters on any wall",
     f"{N_PAPER}, wall notices, whiteboard with writing, posters, calendar, person",
     "many of them would first learn that they were injured when they received a check", "HD-10"),

    ("R041", "A3",
     f"The same desk drawer CLOSED, the room now dark. {DRAWER_RIG}. The one difference is the "
     "light: the only light in the frame is ONE BRIGHT WINDOW on the left, so the drawer front, "
     "the desk edge and the handle "
     "read as dim shapes with a single hard rim of light along their left edges, and the rest of "
     "the room falls to deep but never crushed shadow that still holds its detail. Nobody in the "
     "room. Nothing on the desk",
     f"{N_PAPER}, crushed black shadow, lamp, screen glow, person, object on the desk",
     "So this film ends where the record ends.", "⛔-12 · ○-04 · motif state 6"),

    # ------------------------------------------------------------- A4 the courts, from outside
    ("R042", "A4",
     "An American classical civic courthouse facade photographed from the pavement at a low angle "
     "looking up, filling the frame: six plain stone columns, a deep unadorned pediment above "
     "them, cut ashlar stone, hard midday sun raking across it from the left so the flutes throw "
     "black shadow. THE PEDIMENT AND THE FRIEZE ARE COMPLETELY BLANK STONE — no carved lettering, "
     "no motto, no seal, no relief sculpture, no flag, no plaque. Nobody in the frame",
     f"{N_COURT}, {N_EU}, carved inscription on the pediment, statue, flag on a pole",
     "To have Article III standing to sue in federal court, plaintiffs must demonstrate … that "
     "they suffered a concrete harm.", "HD-01 · TURN"),

    ("R043", "A4",
     "A broad flight of stone courthouse steps photographed from the bottom looking up, empty, "
     "THE STONE STILL WET FROM RAIN so the treads hold a cold sheen and a few shallow puddles sit "
     "in the worn hollows. Overcast light with no sun. Plain stone balustrades on either side with "
     "no carving and no plaque on them. Nobody on the steps",
     f"{N_COURT}, {N_EU}, plaque, inscription, person, umbrella",
     "That is the first thing the Supreme Court of the United States said about this case, on the "
     "twenty-fifth of June, 2021.", "ID-01"),

    ("R044", "A4",
     "A heavy bronze door, closed, photographed square on and filling the frame, its surface a "
     "grid of shallow rectangular panels with softly worn edges and a deep green-brown patina "
     "streaked by rain. EVERY PANEL IS BLANK — no relief figures, no words, no seal, no numbers, "
     "no letterbox, no notice taped to it. One plain vertical pull handle. Cool overcast light "
     "from the left",
     f"{N_COURT}, relief sculpture, inscription, seal, notice on the door, opening hours",
     "Justice Kavanaugh delivered the opinion of the Court.", "ID-02"),

    ("R045", "A4",
     "A stone colonnade photographed from inside it looking along its length, the columns marching "
     "away to the right and RAKING LOW LIGHT cutting between them so the floor is a hard ladder of "
     "bright bands and deep shadow. The stone is plain and unadorned, the ceiling coffers empty. "
     "Nobody in the frame, no furniture, no signage",
     f"{N_COURT}, {N_EU}, inscription, statue, banner, person",
     "He was joined by the Chief Justice and by Justices Alito, Gorsuch and Barrett.", "ID-03"),

    ("R046", "A4",
     "A polished marble floor photographed from standing height looking down and across an empty "
     "hall, ONE HARD-EDGED SHAFT OF WINDOW LIGHT lying across it as a bright parallelogram with "
     "the pattern of the glazing bars soft inside it. The marble is veined pale grey; there is no "
     "inlaid seal, no compass rose, no medallion and no lettering set into the floor. Nobody in "
     "the frame",
     f"{N_COURT}, inlaid seal in the floor, mosaic emblem, compass rose, person",
     "The holding is one sentence long.", "HD-02"),

    ("R047", "A4",
     "A tall arched window high in a stone wall SEEN FROM INSIDE A DARK ROOM, the room itself "
     "almost entirely in shadow so that the window is the only bright thing in the frame and the "
     "stone reveal around it is a soft grey gradient. The glass is plain and the view through it "
     "is blown out to featureless white. No furniture, nobody in the room, no lettering anywhere",
     f"{N_COURT}, stained glass, crest in the glass, person, crushed black shadow",
     "An injury in law is not an injury in fact.", "HD-04"),

    ("R048", "A4",
     "A plain three-storey American civic office building of the appellate scale, photographed "
     "square on from across the street in flat overcast light: a regular grid of identical windows, "
     "a plain stone or precast facade, a shallow set-back entrance at the centre. THE BUILDING "
     "CARRIES NO NAME, no lettering above the door, no seal, no flag and no signage of any kind. "
     "An empty pavement across the foreground",
     f"{N_COURT}, {N_EU}, building name in stone, flagpole, sign over the entrance, person",
     "TransUnion appealed, and it appealed to a court that mostly agreed with the jury.", "MN-06"),

    ("R049", "A4",
     "A wide of an empty paved civic plaza in front of a large plain stone building, photographed "
     "from one corner at standing height so the plaza fills the lower two thirds of the frame: "
     "large pale slabs, a shallow step across the middle distance, ONE SINGLE FIGURE crossing it "
     "far away and very small, no bigger than a fiftieth of the frame height, reduced to a dark "
     "shape with no features. Flat overcast light",
     f"{N_COURT}, {N_EU}, sculpture, monument, banner, crowd, recognisable face",
     "Ramirez sued in February 2012. In 2014 the district court certified a class.", "ID-08"),

    ("R050", "A4",
     "A stone cornice photographed from directly below against a hard clear blue sky, so the frame "
     "is split by one strong diagonal edge: heavy plain moulding, weather-darkened joints, a run of "
     "shallow dentils under it, all of it BLANK STONE with no carved lettering, no dates, no seal "
     "and no relief. Bright sunlight from behind the building so the stone reads cool against the "
     "blue",
     f"{N_COURT}, carved date, inscription, gargoyle, statue, flag",
     "It did not decide whether the class was properly certified. It sent that question back.",
     "ND-03"),

    ("R051", "A4",
     "A long empty corridor photographed straight down its length at eye height: a stone floor "
     "running to a vanishing point, tall panelled doors in a row on both sides all closed, plain "
     "plastered walls above a stone dado, cool daylight coming in from a window at the far end. "
     "EVERY DOOR IS BARE — no numbers, no nameplates, no signs, no notices, no directory board on "
     "any wall. Nobody in the corridor",
     f"{N_COURT}, door numbers, nameplate, directory board, exit sign, person",
     "It did not decide whether the 6,332 could sue in a state court.", "ND-04"),

    ("R052", "A4",
     "A close of a brass handrail on a stone stair, the rail running diagonally through the frame "
     "from lower left to upper right, its top face polished bright by decades of hands and its "
     "underside dark with tarnish, the plain stone treads and the moulded stringer soft behind it. "
     "Side light from the left. No engraving on the rail, no plaque on the wall, nobody in frame",
     f"{N_COURT}, engraved rail, plaque, hand on the rail, person",
     "Three judges heard that appeal, and they did not agree with each other.", "ID-07"),

    ("R053", "A4",
     "A plain stone civic facade at dusk photographed from across the street, the sky above it "
     "gone deep blue-grey and the stone reading cold, with ONE HORIZONTAL ROW OF WINDOWS on the "
     "second floor LIT WARM FROM WITHIN while every other window in the building is dark. No "
     "street lighting flare, no signage on the building, no flag, nobody on the pavement",
     f"{N_COURT}, {N_EU}, illuminated sign, floodlighting, flag, person, lens flare",
     "Now — what did the Supreme Court actually decide? Less than almost anyone remembers.",
     "ND-01 … ND-06"),

    # -------------------------------------------- B the identifiers that were never compared
    ("R054", "B",
     "A closed passport-sized booklet lying alone on a dark matte surface, photographed from "
     "directly overhead in soft even light, filling about a third of the frame. THE COVER IS "
     "COMPLETELY BLANK: a plain dark blue-grey grained board with no crest, no coat of arms, no "
     "gold blocking, no country name, no chip symbol and no lettering anywhere on it. The corners "
     "are slightly rounded and softly worn",
     f"{N_PAPER}, coat of arms, gold blocking, country name, chip symbol, crest, passport cover "
     "design",
     "An entry often will have, for example, a full name, an address, a nationality, a passport",
     "LS-08"),

    ("R055", "B",
     "The same passport-sized booklet lying OPEN at its centre spread on the same dark surface, "
     f"photographed from directly overhead. {GREY_RULE} — both facing pages carry only the flat "
     "grey bars, in two short stacks, and nothing else: no photograph window, no machine-readable "
     "zone, no stamps, no crest, no numbers. Soft even light, the gutter shadow down the middle",
     f"{N_PAPER}, photo page, machine readable zone, visa stamps, crest, portrait window",
     "Passport information.", "SR-08"),

    ("R056", "B",
     "A single plain paper form lying flat on a plain desk, photographed from directly overhead "
     "and filling the frame. THE FORM IS A GRID OF EMPTY RULED BOXES AND NOTHING ELSE: fine grey "
     "rectangles in rows, each one completely empty, with no field labels, no headings, no small "
     "print, no numbers, no logo and no signature line anywhere on the sheet. Even soft light, one "
     "shallow crease across the paper",
     f"{N_PAPER}, field labels, headings, printed instructions, tick boxes with words, logo",
     "a tax identification or cedula number", "LS-08"),

    ("R057", "B",
     "A wooden-handled rubber date stamp LYING ON ITS SIDE on a plain desk, close, so that the "
     "rubber face is turned toward the camera at an angle: the raised rubber on the face is a "
     "SOFT ILLEGIBLE JUMBLE OF WORN GREY-BLACK SHAPES with no readable characters, no digits and "
     "no date bands that resolve. Shallow focus, the handle sharp and the face slightly soft. Bare "
     "desk around it",
     f"{N_PAPER}, readable date, digits on the stamp, month letters, ink pad with a brand",
     "a date of birth", "LS-08"),

    ("R058", "B",
     "The curved surface of a physical desk globe photographed very close at a shallow raking "
     "angle, so the horizon of the sphere runs across the frame and the land masses read only as "
     "soft blocks of muted colour: NO COUNTRY NAMES, NO CITY NAMES, NO BORDER LINES AND NO "
     "LETTERING of any kind are legible anywhere on it — the printing dissolves into colour and "
     "grain. One soft window highlight sliding along the curve",
     f"{N_PAPER}, country names, city labels, latitude numbers, readable map text",
     "a nationality", "LS-08"),

    ("R059", "B",
     "A street of ordinary single-storey American suburban houses photographed from the middle of "
     "the road at standing height in flat daylight: identical driveways, mown front lawns, a "
     "kerbline running to a vanishing point, parked cars at the kerb. NO HOUSE NUMBERS ON ANY "
     "HOUSE, no mailbox lettering, no street sign, no realtor board, nobody in the frame. Plain "
     "pale sky",
     f"{N_PAPER}, house numbers, street sign, mailbox with a name, realtor sign, {N_BRAND}, "
     f"{N_EU}",
     "an address", "LS-08"),

    ("R060", "B",
     "The exterior of a small plain civic register office: a low mid-century public building of "
     "pale brick with a flat canopy over a glazed entrance, three steps up, a low wall and a strip "
     "of clipped planting in front, photographed square on from across the pavement in flat "
     "overcast light. THE BUILDING CARRIES NO NAME AND NO SIGN of any kind, the glass beside the "
     "door is clear and empty, and nobody is in the frame",
     f"{N_PAPER}, building name, opening hours, notice board, seal over the door, {N_EU}, person",
     "a place of birth", "LS-08"),

    ("R061", "B",
     "A paper wall calendar hanging on a plain painted wall, photographed square on from six feet "
     "away with the focus set on the wall beside it so THE CALENDAR ITSELF IS OUT OF FOCUS: its "
     "month grid reads only as a soft blur of pale squares and grey smudges, with no digits, no "
     "month name and no weekday letters resolvable anywhere on it. Even daylight from the left, "
     "the wall bare around it",
     f"{N_PAPER}, readable numbers, month name, weekday letters, sharp calendar, photograph on "
     "the calendar",
     "a date of birth", "LS-08"),

    ("R062", "B",
     "A desk nameplate standing on a plain desk, photographed close and square on at desk height, "
     "filling the middle of the frame: a plain brushed brass plate in a plain dark wooden holder, "
     "ITS FACE COMPLETELY BLANK — bare brushed metal with a soft directional grain and one shallow "
     "reflection running along it, and no engraving, no name, no title, no lettering, no logo. The "
     "desk beyond it is empty and soft",
     f"{N_PAPER}, engraved name, job title, initials, logo on the plate",
     "a full name", "LS-08"),

    ("R063", "B",
     "A single plain filing card HELD LIGHTLY BETWEEN THE TIPS OF A THUMB AND A FOREFINGER at the "
     "bottom corner, the rest of the hand out of the frame, the card standing upright and filling "
     "the middle of the picture, front on. THE CARD IS COMPLETELY BLANK — no ruling, no printing, "
     "no writing, no tab, no punch hole. The two visible digits are clearly separate, each with "
     "its own nail and its own shadow on the card. Soft even light, dark soft background",
     f"{N_PAPER}, {N_HAND}, writing on the card, ruled lines, index tab",
     "former names, and aliases", "LS-08"),

    ("R064", "B",
     "A wall of small identical wooden index drawers filling the entire frame, photographed square "
     "on and lit from the left: eight rows by twelve columns of the same little drawer front, each "
     "with the same plain brass cup handle and the same empty brass label holder above it, and "
     "EVERY LABEL HOLDER IS EMPTY — bare metal frames with no cards and no writing in any of them. "
     "The wood is worn pale at the handles",
     f"{N_PAPER}, cards in the label holders, letters on the drawers, alphabet dividers, numbers",
     "It publishes, alongside them, the things that tell one human being from another.", "LS-08"),

    ("R065", "B",
     "A bank of identical grey server cabinets in a cold windowless room, photographed straight "
     "down the aisle between two rows at eye height: perforated dark doors in a long repeating "
     "rank, a hard even overhead light, a bare raised floor. The status lights on the cabinets are "
     "SOFT UNRESOLVED SPECKS OF GREEN AND AMBER with no pattern that could be read, and there are "
     "no maker's marks, no rack labels and no printed asset tags anywhere",
     f"{N_PAPER}, {N_SCREEN}, rack labels, asset tags, brand logo on the cabinets, blue neon glow",
     "run through a computer-based screening system", "LS-09"),

    ("R066", "B",
     "A close, very shallow-focus still of the cut ends of a bundle of fibre optic cables, the "
     "polished ferrules catching small hard points of light, the bundle running out of the bottom "
     "of the frame and everything behind it dissolved into a soft dark wash. No connectors with "
     "printing, no cable labels, no colour-coded tags with writing. Cool light",
     f"{N_PAPER}, cable labels, printed connectors, neon blue grade, {N_SCREEN}",
     "The tool works on approximate string matching.", "LS-11"),

    ("R067", "B",
     "A computer monitor seen square on from the front in a dim room, THE ENTIRE SCREEN A SINGLE "
     "FIELD OF SOFT EVEN PALE LIGHT with no content on it whatsoever: no window, no cursor, no "
     "icon, no line of text, no menu bar, no reflection of a room. The bezel is plain matte black "
     "with no maker's mark. The light from the screen falls on a bare desk in front of it. Nobody "
     "in frame",
     f"{N_SCREEN}, {N_PAPER}, desktop icons, reflection of a person, brand logo on the bezel",
     "Its own search tool carries a warning that using it is not a substitute for undertaking "
     "appropriate due diligence.", "LS-11"),

    ("R068", "B",
     "Hundreds of small identical pale record cards laid out edge to edge IN A DENSE REGULAR GRID "
     "filling the entire frame, photographed from directly overhead in even soft light, the "
     "picture reading as texture and repetition. EVERY CARD IS COMPLETELY BLANK — no printing, no "
     "ruling, no writing, no numbers. ONE SINGLE CARD near the lower middle is LIFTED SLIGHTLY OUT "
     "OF THE GRID at an angle and catches a brighter highlight along its raised edge, throwing a "
     "small shadow onto the cards beneath. The lower edge of the frame is the brightest part of "
     "the picture",
     f"{N_PAPER}, writing on the cards, printed forms, ruled lines, hand, numbers",
     "Thousands of law-abiding Americans happen to share a first and last name with one of the "
     "terrorists, drug traffickers or serious criminals on OFAC's list.", "LS-15"),

    ("R069", "B",
     "The same dense overhead grid of identical blank record cards, now with TWO CARDS LIFTED "
     "slightly out of the grid, FAR APART FROM ONE ANOTHER — one near the upper left, one near the "
     "lower right — each catching its own highlight and throwing its own small shadow, everything "
     "between them flat and identical. Same overhead camera, same even light. All cards completely "
     "blank",
     f"{N_PAPER}, writing on the cards, hand, numbers, arrows, connecting line",
     "The court's own example is that Cortez would match with Cortes.", "LS-16"),

    ("R070", "B",
     "The same field of identical blank record cards photographed FROM A LOW RAKING ANGLE just "
     "above the surface instead of overhead, so the near cards are sharp and huge in the "
     "foreground and the grid recedes fast into soft focus and finally into a pale blur at the top "
     "of the frame. All cards completely blank, no card lifted. Even soft light from the left",
     f"{N_PAPER}, writing on the cards, hand, sharp far cards, numbers",
     "Unsurprisingly, the Supreme Court says, the product generated many false positives.",
     "LS-15"),

    ("R071", "B",
     "A folded stack of continuous fanfold computer paper lying on a plain dark surface, "
     "photographed from a low three-quarter angle so the concertina folds and the perforated "
     f"sprocket margins down both sides are the shape of the picture. {GREY_RULE}, and the sprocket "
     "holes are the only regular punctuation in the frame. Soft side light picking out each fold",
     f"{N_PAPER}, printed rows of figures, column headings, dot matrix text, tractor-feed labels",
     "In collecting other types of data for use on consumer reports — such as tax liens or "
     "bankruptcy judgments", "LS-17"),

    ("R072", "B",
     "ONE single plain pale card lying alone at the centre of an otherwise completely empty dark "
     "table, photographed from a low three-quarter angle a foot away, one soft light from the left "
     "so the card is the brightest thing in the frame and its thin shadow runs away to the right. "
     "THE CARD IS COMPLETELY BLANK. Nothing else is in the frame at all",
     f"{N_PAPER}, writing on the card, second card, hand, spotlight vignette",
     "OFAC information was the only consumer-report data that TransUnion collected using name "
     "alone.", "LS-17"),

    # ------------------------------------------------------------------------ C the people lane
    ("R073", "C",
     "THREE ADULTS SEEN FROM BEHIND at a sales desk, framed from behind their shoulders at seated "
     "height: three backs and three sets of shoulders fill the lower half of the frame as dark "
     "soft masses, NO FACE IS VISIBLE AND NOT ONE HEAD IS TURNED, and the near hands of the "
     "middle figure rest flat on the desk edge in sharp focus with the fingers separate. "
     "Everything beyond them — the desk, the chair opposite, the bright showroom — falls away into "
     "soft focus. Ordinary weekday clothes, no coats, nothing branded",
     f"{N_HAND}, face, profile, turned head, reflection of a face, {N_BRAND}",
     "His wife is with him, and his father-in-law.", "SR-01"),

    ("R074", "C",
     "ONE adult hand alone on a laminate desk beside a set of car keys, photographed close from a "
     f"low three-quarter angle. {FLAT_HAND}. A plain worn wedding band sits on the ring finger. The "
     "skin is mid-forties, dry, ordinary, with visible knuckle creases and short unmanicured "
     "nails. The keys lie a few inches beyond the fingertips, unmarked. Bright daylight from the "
     "left, the rest of the desk soft",
     f"{N_HAND}, manicured nails, jewellery beyond one plain band, wristwatch with a readable "
     f"face, {N_BRAND}",
     "The salesman runs a credit check", "SR-02"),

    ("R075", "C",
     "A hand on a computer keyboard photographed close from the side at desk height, THE PALM AND "
     "FINGERS RESTING DOWN ON THE KEYS rather than typing in mid-air, THE FOUR FINGERS SIDE BY "
     "SIDE AND SEPARATE each on its own key with a line of shadow between them and one nail "
     "visible on each, the thumb down by the space bar and clearly apart. The keycaps are blank "
     "and unmarked. A cool screen light from out of frame right lies along the knuckles and the "
     "back of the hand; THE SCREEN ITSELF IS NOT IN THE FRAME",
     f"{N_HAND}, {N_SCREEN}, letters on the keycaps, hands typing in mid-air, second hand",
     "The salesman runs a credit check", "SR-02"),

    ("R076", "C",
     "A woman's two hands at a counter, framed from the forearms down and seen from just above and "
     "in front, both hands DOWN ON THE COUNTER TOP AND IN FULL CONTACT WITH IT: the left hand lies "
     "flat and steady on the corner of a sheet of paper with its four fingers side by side and "
     "separate, and the right hand rests on the paper on the heel of the palm with a plain pen "
     "held between the thumb and the first two fingers, THE PEN'S TIP TOUCHING THE PAPER AND AT "
     f"REST. Every finger on both hands is separately visible with its own nail. {BLANK_PAPER}. "
     "Bright daylight from the left",
     f"{N_HAND}, {N_PAPER}, hand raised off the surface, pen in mid-air, signature on the paper, "
     "printed contract",
     "His wife bought the car in her own name.", "SR-04"),

    ("R077", "C",
     "A man in his forties SEEN ENTIRELY FROM BEHIND, standing still in the middle of a bright "
     "empty car showroom, framed from the knees up and placed slightly left of centre: an ordinary "
     "dark jacket, ordinary trousers, ordinary short hair, both arms hanging at his sides with the "
     "hands relaxed and the fingers loosely separate. HIS HEAD IS NOT TURNED AND NO PART OF HIS "
     "FACE IS VISIBLE. The showroom glass and floor beyond him are bright and soft",
     f"{N_HAND}, face, profile, turned head, reflection of his face in the glass, {N_BRAND}",
     "A car he did not buy.", "SR-04"),

    ("R078", "C",
     "Two adults WALKING AWAY FROM THE CAMERA across an open car forecourt at midday, seen from "
     "behind and far off so that together they occupy less than a sixth of the frame height and no "
     "feature of either is resolvable — two ordinary dark silhouettes against hot pale asphalt, "
     "one slightly ahead of the other. Rows of parked unmarked cars either side, flat hard light, "
     "a pale sky",
     f"{N_HAND}, face, turned head, {N_BRAND}, close figures, recognisable clothing brand",
     "A car he did not buy.", "SR-04"),

    ("R079", "C",
     "An adult's hands and forearms only, opening an envelope at a wooden kitchen table, framed "
     "from just above and in front with the head and body entirely out of the frame: BOTH HANDS "
     "REST DOWN ON THE TABLE, the left hand flat and holding the envelope steady against the wood "
     "with four separate fingers, the right hand also down on the table working a thumb under the "
     "flap. Every finger on both hands is distinct with its own nail and its own shadow. The "
     "envelope is blank. Morning light from the left",
     f"{N_HAND}, {N_PAPER}, hands raised in the air, address on the envelope, letter opener, face",
     "The day after that, a second envelope arrived.", "SR-05"),

    ("R080", "C",
     "AN INVENTED, COMPLETELY FICTIONAL man in his forties, in three-quarter profile, seated at an "
     "ordinary American kitchen table reading something held low and out of the bottom of the "
     "frame: HIS FACE IS VISIBLE AND IN FOCUS, unremarkable, evenly lit by flat window light, the "
     "expression neutral and unperformed with the eyes cast downward and NOT DIRECTED AT THE "
     "CAMERA. Ordinary short hair, an ordinary plain shirt, no styling, no retouching. The kitchen "
     "behind him is soft: cabinets, a kettle, a window",
     f"{N_HAND}, looking at the camera, smiling for the camera, model look, retouched skin, "
     "studio lighting, celebrity resemblance",
     "Ramirez testified that he was confused by them.", "SR-09"),

    ("R081", "C",
     "The same ordinary American kitchen, the same table and the same flat morning window light, "
     "NOW WITH NOBODY IN IT: the chair he was sitting in stands empty and pushed back at an angle, "
     "the table bare in front of it. Same camera position, same height, same lens. Nothing on the "
     "table, no person anywhere in the frame",
     f"{N_HAND}, person, silhouette in the doorway, object on the table",
     "Neither one told him how to dispute anything.", "SR-10"),

    ("R082", "C",
     "A hand holding a corded telephone handset clamped against a shoulder and an ear, framed "
     "tight from the collarbone up to the jaw ONLY — the chin, the mouth and everything above them "
     "are OUTSIDE THE TOP OF THE FRAME AND NOT VISIBLE. The hand steadies the handset from below "
     "with the four fingers side by side and separate along its length, each with its own nail, "
     "and the thumb apart on the near side. An ordinary shirt collar, ordinary skin, soft interior "
     "light from the left",
     f"{N_HAND}, face, mouth, chin, {N_SCREEN}, mobile phone, brand on the handset",
     "The Supreme Court says he consulted a lawyer …", "SR-11"),

    ("R083", "C",
     "AN INVENTED, COMPLETELY FICTIONAL woman in her thirties at an ordinary office desk, mid-shot "
     "from across the desk at seated height: HER FACE IS VISIBLE AND IN FOCUS, plain and "
     "unremarkable, LOOKING DOWN AT HER WORK AND NOT AT THE CAMERA, the expression neutral and "
     "unperformed. Ordinary work clothes, ordinary hair, no styling and no retouching. Her hands "
     "rest down on the desk with the fingers separate. The monitor beside her is turned away. "
     f"{NO_SCREEN}. A plain open-plan office soft behind her",
     f"{N_HAND}, {N_SCREEN}, looking at the camera, smiling for the camera, model look, retouched "
     "skin, headset, lanyard with a printed badge",
     "Beginning in 2002, TransUnion introduced an add-on product called OFAC Name Screen Alert.",
     "LS-13"),

    ("R084", "C",
     "A pair of hands at a keyboard in a dim open-plan office, framed from just behind and above "
     "the hands with the body out of frame: BOTH PALMS ARE DOWN AND IN CONTACT WITH THE DESK AND "
     "THE KEYS, all eight fingers side by side and separate with a line of shadow between each "
     "pair and both thumbs clearly apart, the keycaps blank and unmarked. Behind and above the "
     "hands, four or five empty desks recede into soft focus and low light. THE SCREEN IS NOT IN "
     "THE FRAME",
     f"{N_HAND}, {N_SCREEN}, letters on the keycaps, hands typing in mid-air, face, person at a "
     "far desk in focus",
     "Accuity's software conducted a name-only search …", "LS-16"),

    ("R085", "C",
     "About EIGHT ordinary adults walking along a city pavement in daylight, photographed from "
     "across the street at standing height with a long lens so the whole group is compressed and "
     "NOBODY IS IN FOCUS — every face is soft and unresolvable, mixed ages, mixed heights, "
     "ordinary weekday clothes, some walking toward the camera and some away. A plain shopfront "
     "run behind them with no readable signage. Flat overcast daylight",
     f"{N_HAND}, sharp face, portrait, {N_PAPER}, shop signage, brand logo, crowd of hundreds",
     "TransUnion sent the same OFAC letter to eight thousand, one hundred and eighty-four other "
     "consumers …", "SR-13"),

    ("R086", "C",
     "A CROWD OF ABOUT FORTY ordinary adults crossing a wide city street on a marked crossing, "
     "photographed from a high angle two floors up looking down, so the people read as a field of "
     "heads, shoulders and shortened bodies and NO FACE IS RESOLVABLE ANYWHERE IN THE FRAME. The "
     "crossing stripes make plain pale bars under them. Mixed ages, ordinary clothes, flat "
     "overcast daylight. No banners, nothing carried, nobody looking up",
     f"{N_HAND}, sharp face, upturned face, banner, placard, protest, {N_PAPER}",
     "The parties stipulated that the class contained eight thousand, one hundred and eighty-five "
     "members …", "MN-02"),

    ("R087", "C",
     "AN INVENTED, COMPLETELY FICTIONAL man in his sixties seated alone on a row of plain chairs "
     "in a bare institutional corridor, mid-shot from the side and slightly in front at seated "
     "eye height: HIS FACE IS VISIBLE, ordinary, tired, entirely neutral, LOOKING ALONG THE "
     "CORRIDOR AND NOT AT THE CAMERA. BOTH HANDS REST FLAT AND SEPARATE ON HIS OWN KNEES, one on "
     "each knee, palms down, THE FINGERS OF EACH HAND SIDE BY SIDE AND APART, NOT CLASPED AND NOT "
     "INTERLOCKED. Plain painted walls, a hard floor, even daylight from a window out of frame",
     f"{N_HAND}, clasped hands, interlocked fingers, hands folded together, looking at the "
     f"camera, model look, {N_PAPER}, {N_COURT}",
     "only one thousand, eight hundred and fifty-three of them", "MN-02"),

    ("R088", "C",
     "TWELVE pairs of shoes and lower legs in a row of waiting-room chairs, photographed from "
     "knee height straight along the row so the frame is a rhythm of feet, ankles and chair legs "
     "and NOTHING ABOVE THE KNEE IS IN THE FRAME. Ordinary worn everyday shoes, mixed styles, some "
     "feet flat, some crossed at the ankle. A hard-wearing floor and the plain steel chair frame "
     "running through the picture. Even overhead light",
     f"{N_HAND}, face, torso, {N_PAPER}, uniform boots, {N_COURT}",
     "The trial ran six days.", "MN-04"),

    ("R089", "C",
     "Two adults' hands on a plain table with a stack of paper between them, framed from directly "
     "above with both bodies out of the frame: THE NEAR HAND LIES FLAT ON THE TABLE WITH ITS "
     "FINGERTIPS AGAINST THE EDGE OF THE STACK, palm down and in full contact with the surface, "
     "four fingers side by side and separate, and THE FAR HAND ALSO LIES FLAT ON THE TABLE just "
     "beyond the stack, waiting, its four fingers likewise separate. Every finger on both hands "
     f"shows its own nail and its own shadow. {GREY_RULE} — and that is the top sheet of the "
     "stack. Even soft light",
     f"{N_HAND}, {N_PAPER}, hands raised, handshake, pointing finger, printed report, signature",
     "Ramirez testified about what happened at the dealership.", "SR-15"),

    ("R090", "C",
     "AN INVENTED, COMPLETELY FICTIONAL woman in her fifties standing on the porch of an ordinary "
     "American suburban house, mid-shot from the front at eye height about ten feet away: HER FACE "
     "IS VISIBLE AND IN FOCUS, ordinary and unremarkable, neutral, LOOKING OFF TO ONE SIDE OF THE "
     "FRAME AND NOT AT THE CAMERA. Her arms are folded across her front with each hand tucked flat "
     "under the opposite upper arm so no fingers are extended into the air. An ordinary cardigan, "
     "ordinary hair, no styling and no retouching. Flat overcast daylight, plain porch boards and "
     "a plain door behind her",
     f"{N_HAND}, looking at the camera, smiling for the camera, model look, retouched skin, house "
     f"numbers, {N_PAPER}",
     "The plaintiffs did not present any evidence that those class members even knew …", "HD-10"),

    ("R091", "C",
     "An ordinary American family kitchen at night WITH NOBODY IN IT, photographed square on from "
     "the far side of the room at standing height: the overhead light off, one small warm lamp or "
     "under-cupboard light on somewhere to the left, a window black behind the sink, TWO CHAIRS "
     "PULLED OUT FROM THE TABLE AND LEFT ASKEW, the table bare. Shadow everywhere but never "
     "crushed — every corner still holds its detail. No person, no reflection of a person",
     f"{N_HAND}, person, silhouette, crushed black shadow, {N_SCREEN}, {N_PAPER}",
     "many of them would first learn that they were injured when they received a check", "HD-10"),

    ("R092", "C",
     "A man in a plain overcoat standing on broad stone civic steps, seen FROM BEHIND AND SLIGHTLY "
     "TO ONE SIDE at three-quarters so that only the very edge of his cheek and jaw is visible and "
     "NO FEATURE OF HIS FACE CAN BE MADE OUT, framed from the knees up and placed left of centre, "
     "one hand hanging at his side with the fingers loosely separate and the other in his coat "
     "pocket. He is looking away up the steps. A plain city street soft and grey behind and below. "
     "Flat overcast daylight",
     f"{N_HAND}, face, profile, turned head, briefcase with a logo, {N_COURT}, {N_EU}",
     "Justice Thomas wrote first, for himself and three colleagues …", "TH-01"),

    ("R093", "C",
     "One hand at rest on the front of a CLOSED office drawer, photographed close from a low "
     f"three-quarter angle. {FLAT_HAND} — here the surface is the flat wooden drawer front itself, "
     "the palm laid against it with the fingers hanging down over the brass handle, separate and "
     "still, not gripping and not pulling. Mid-forties skin, short unmanicured nails. Soft north "
     "light from the left, the desk and the room beyond soft and dim",
     f"{N_HAND}, gripping the handle, pulling the drawer, drawer open, {N_PAPER}",
     "Think about what that does to the desk-drawer letter.", "LS-19 · HD-08"),

    ("R094", "C",
     "TWO INVENTED, COMPLETELY FICTIONAL adults talking in a doorway, mid-shot from about eight "
     "feet away at eye height, one standing inside the room and one in the corridor, TURNED TOWARD "
     "EACH OTHER IN PROFILE SO NEITHER LOOKS ANYWHERE NEAR THE CAMERA. Both faces are visible in "
     "profile, ordinary, mid-conversation and unperformed. Ordinary work clothes. Their hands are "
     "down at their sides or resting on the door frame with fingers separate. The door frame makes "
     "a hard vertical edge between them. Even flat daylight",
     f"{N_HAND}, looking at the camera, model look, retouched skin, {N_PAPER}, lanyard with a "
     f"printed badge, {N_COURT}",
     "If federal courts are closed to these plaintiffs, state courts are not …", "TH-08 · ND-04"),

    ("R095", "C",
     "A plain empty office at dusk, photographed from the doorway at standing height: two or three "
     "bare desks, a run of low cabinets, one window on the left going deep blue, the overhead "
     "lights off so the room is lit only by that window. ONE CHAIR IS TURNED OUT FROM ITS DESK at "
     "an angle, as though somebody had just stood up. NOBODY IS IN THE ROOM. Nothing on any desk. "
     "Shadow that still holds its detail",
     f"{N_HAND}, person, silhouette, {N_SCREEN}, {N_PAPER}, crushed black shadow",
     "Most of them, the majority pointed out, did not know.", "HD-10"),

    ("R096", "C",
     "A wide of an ordinary American residential street at dusk, photographed from the middle of "
     "the road at standing height: single-storey houses either side, driveways, a kerbline running "
     "away, the sky above still pale and the street below already dim. THREE SEPARATE PEOPLE are "
     "in the frame, ALL FAR AWAY AND ALL FAR APART FROM EACH OTHER — one on each pavement and one "
     "at a distant driveway — each no more than a fortieth of the frame height and each reduced to "
     "a soft dark shape with no resolvable feature. No house numbers, no street sign, nobody near "
     "the camera",
     f"{N_HAND}, sharp face, person close to the camera, house numbers, street sign, {N_EU}, "
     "streetlight flare",
     "Six thousand, three hundred and thirty-two of them were told … that nothing had happened "
     "to them yet.", "HD-11"),

    # ------------------------------------------------- E Treasury and the federal register (new)
    ("R097", "E",
     "A plain modern American federal office building photographed square on from across a wide "
     "empty pavement in flat overcast light: a heavy flat stone facade, a regular grid of deep-set "
     "identical windows, a low set-back entrance under a plain canopy. THE FACADE CARRIES NOTHING "
     "AT ALL — no name, no seal, no eagle, no lettering, no flag, no plaque, no notice board. A "
     "bare kerb and an empty road across the foreground, nobody in the frame",
     f"{N_PAPER}, {N_COURT}, {N_EU}, federal seal, eagle, building name, flag, security bollards "
     "with markings",
     "The list is real, and it belongs to the Treasury.", "LS-01"),

    ("R098", "E",
     "A single plain metal flagpole standing empty against a flat pale grey overcast sky, "
     "photographed from below at a slight angle so the pole runs from the bottom right of the "
     "frame up and out of the top: NO FLAG IS ON IT, only the bare halyard hanging slack against "
     "the pole and the plain truck and finial at the top. The upper corner of a plain stone "
     "building edges into the lower left. No wind, no sun, nobody in frame",
     f"{N_PAPER}, {N_COURT}, flag, banner, pennant, eagle finial, emblem, {N_EU}",
     "Their assets are blocked, and United States persons are generally prohibited from dealing "
     "with them.", "LS-02"),

    ("R099", "E",
     "An empty wooden lectern standing alone on a low platform in a plain meeting room, "
     "photographed square on from eight feet away at standing height. THE FRONT PANEL OF THE "
     "LECTERN IS BARE POLISHED WOOD — no seal, no emblem, no crest, no plaque and no lettering on "
     "it anywhere. There is no microphone with a branded flag on it, no paper on the reading "
     "surface and nobody behind it. A plain curtain or plain painted wall behind, even soft light",
     f"{N_PAPER}, {N_COURT}, seal on the lectern, crest, microphone flag, flags behind, person",
     "It is generally unlawful to transact business with any person on the list.", "LS-04"),

    ("R100", "E",
     "A corridor of identical closed office doors photographed straight down its length at eye "
     "height in an ordinary government office building: pale painted walls, a hard-wearing carpet "
     "tile floor, six plain flush doors on the left and six on the right, all shut and ALL OF THEM "
     "COMPLETELY BARE — no numbers, no nameplates, no signs, no notices, no directory. Even "
     "fluorescent light overhead, nobody in the corridor",
     f"{N_PAPER}, door numbers, nameplate, directory board, exit sign, person, {N_EU}",
     "Individuals on the OFAC list are terrorists, drug traffickers, or other serious criminals.",
     "LS-04"),

    ("R101", "E",
     "A glass-fronted public notice case mounted on a plain painted wall, photographed square on "
     "from four feet away, THE CASE COMPLETELY EMPTY: nothing pinned inside it, only the bare "
     "green felt board behind the glass, the plain aluminium frame, one small lock, and a soft "
     "reflection of the opposite wall sliding across the glass. Nothing readable anywhere. Even "
     "corridor light",
     f"{N_PAPER}, notices pinned inside, posters, printed sheets, headings, reflection of a "
     "person",
     "On the eight Treasury pages retrieved for this film, there is no current count of any kind.",
     "LS-05"),

    ("R102", "E",
     "A shelf of about fifteen identical grey paper-bound official volumes standing upright, "
     "photographed square on and close so the row of spines fills the frame: uniform height, "
     "uniform width, uniform dull grey board, softly worn at the head and tail. EVERY SPINE IS "
     "COMPLETELY BLANK — no titles, no volume numbers, no year, no labels, no gilt. Even soft "
     "light from the left, the shelf edge a dark line beneath",
     f"{N_PAPER}, titles on the spines, volume numbers, year, gilt lettering, library labels",
     "There is one official figure, from a 2021 sanctions review …", "LS-05"),

    ("R103", "E",
     "A single aisle in a cold data hall, photographed at eye height with ONE CABINET DOOR "
     "STANDING OPEN on the left: inside it, dense ranks of identical dark equipment and a neat "
     "bundle of pale cabling dropping down the side, everything else in the aisle closed and "
     "identical. No maker's marks, no rack labels, no printed asset tags, no readable status "
     "displays anywhere. Hard even overhead light, nobody in the frame",
     f"{N_PAPER}, {N_SCREEN}, rack labels, asset tags, brand logos, blue neon grade, person",
     "Treasury publishes the list as a data file …", "LS-05 · ⛔-11"),

    ("R104", "E",
     "A plain desk photographed from directly overhead, almost completely empty, with ONE CLOSED "
     "GREY RING BINDER lying alone slightly off centre. THE BINDER IS COMPLETELY UNMARKED — a "
     "plain grey cover with no title, no label window, no spine card, no printing of any kind — "
     "and nothing else is on the desk at all. Even soft light from the left, the desk surface a "
     "flat neutral grey-brown",
     f"{N_PAPER}, label on the binder, spine card, title, sticky notes, pen, hand",
     "That is our count of their file. It is not a Treasury statement …", "⛔-11"),

    # ------------------------------------------------------ F 1970 and the statute (new, ACT_3)
    ("R105", "F",
     "A single plain hardback statute volume lying closed on a wooden desk, photographed from a "
     "low three-quarter angle so the cover and the fore-edge are both visible: heavy dark cloth "
     "boards, softly bumped corners, a plain sewn head band. THE COVER AND THE SPINE ARE "
     "COMPLETELY BLANK — no title, no gilt, no author, no volume number, no library label. One "
     "warm desk light from the left, the rest of the desk bare and soft",
     f"{N_PAPER}, gilt title, spine lettering, library label, embossed crest",
     "In 1970, Congress passed and President Nixon signed the Fair Credit Reporting Act.",
     "MN-09"),

    ("R106", "F",
     "The same plain hardback volume lying OPEN at a middle spread on the same desk in the same "
     f"warm light, photographed from directly overhead so both pages fill the frame. {GREY_RULE} — "
     "each page carries two justified columns of the flat grey bars and nothing else: no headings, "
     "no page numbers, no section marks, no footnotes, no marginal notes. The gutter shadow runs "
     "down the middle and the paper is warm off-white",
     f"{N_PAPER}, printed columns of text, section numbers, page numbers, footnotes, marginalia, "
     "highlighter",
     "it requires a consumer reporting agency to follow reasonable procedures to assure maximum "
     "possible accuracy", "MN-09"),

    ("R107", "F",
     "An empty committee room photographed from the back at standing height: one long plain table "
     "across the far end, a curved run of plain chairs behind it, rows of plain public seating in "
     "the foreground, tall windows down the left throwing flat daylight across the carpet. THE "
     "ROOM IS COMPLETELY EMPTY — nobody in any seat, nothing on the table, no name cards, no "
     "microphones with branded flags, no seal on the wall, no lettering anywhere",
     f"{N_PAPER}, {N_COURT}, name cards, seal on the wall, microphone flags, person, flags",
     "… when the data is an OFAC alert, had been said out loud once already.", "N9-01"),

    ("R108", "F",
     "A green-shaded desk lamp switched on over a wooden desk in an otherwise dark office, "
     "photographed from a seated three-quarter angle: the lamp throws one warm pool of light onto "
     "a plain leather blotter and falls away fast into shadow that still holds its detail. THE "
     "BLOTTER IS COMPLETELY EMPTY — no paper, no pen, no book, nothing in the pool of light at "
     "all. Nobody in the room",
     f"{N_PAPER}, papers on the desk, open book, pen, person, crushed black shadow",
     "In 2005, a consumer sued.", "TH-04"),

    ("R109", "F",
     "A tall stack of folded continuous fanfold paper standing on a plain floor beside a desk, "
     "photographed from a low angle so the stack rises through most of the frame and the "
     f"concertina edges and sprocket margins step up it like a ladder. {GREY_RULE} — visible on "
     "the top sheet and faintly through the fold edges. Cool even office light, the wall behind plain "
     "and bare",
     f"{N_PAPER}, printed figures, column headings, dot matrix text, tractor labels",
     "TransUnion had sold an OFAC credit report about her to a car dealership.", "TH-04"),

    ("R110", "F",
     "TWO identical paper wall calendars hanging SIDE BY SIDE on a plain painted wall, "
     "photographed square on from six feet away with the focus set on the wall so both calendars "
     "are SOFT AND OUT OF FOCUS: each reads only as a pale rectangle with a blurred grid of grey "
     "squares, and NO DIGIT, NO MONTH NAME AND NO WEEKDAY LETTER is resolvable on either of them. "
     "A clear gap of bare wall between the two. Even daylight from the left",
     f"{N_PAPER}, readable numbers, month names, sharp calendar, photograph on the calendar, "
     "circled date",
     "Twenty-seven years apart.", "TH-04"),

    ("R111", "F",
     "A plain heavy exterior door of a civic office building, closed, photographed square on from "
     "four feet away: dark painted timber, a broad brass kick plate at the foot polished bright by "
     "boots, a plain brass pull handle, a plain stone surround. THE DOOR AND THE KICK PLATE AND "
     "THE SURROUND ARE ALL BLANK — no name, no numbers, no opening hours, no seal, no plaque, no "
     "notice taped to the glass. Flat overcast light",
     f"{N_PAPER}, {N_COURT}, opening hours, door number, nameplate, notice, seal, {N_EU}",
     "in August 2010 the Third Circuit affirmed that", "TH-04 · N9-02"),

    ("R112", "F",
     "An open stone stairwell photographed from the bottom looking straight up, so three flights "
     "of plain stone steps and their plain iron balustrades spiral away above the camera and make "
     "a receding rectangular well with a pale skylight at the very top. Every surface is plain — "
     "no signs, no floor numbers, no arrows, no notices. Cool daylight falling down the well, "
     "nobody on any flight",
     f"{N_PAPER}, {N_COURT}, floor numbers, arrows, signs, person, vertigo fisheye distortion",
     "Despite this warning, TransUnion continued to use problematic matching technology …",
     "N9-03"),

    # --------------------------------------------- G the law: ACT_4 / ACT_5 expansion (new, 10)
    ("R113", "G",
     "A tall narrow window set in a deep stone reveal, photographed from inside a plain room at "
     "eye height and slightly to one side, so the thickness of the wall is the subject: the splayed "
     "reveal runs back to a small bright pane and ONE SHAFT OF LIGHT lies along the stone sill and "
     "spills a little way onto the floor. The glass is plain and blown out to white. No furniture, "
     "no lettering, nobody in the room",
     f"{N_PAPER}, {N_COURT}, stained glass, crest, person, crushed black shadow",
     "Congress can write a law that says a company owes you something.", "HD-05 · HD-14"),

    ("R114", "G",
     "A pair of tall panelled doors, CLOSED, photographed dead square on from ten feet away so "
     "they fill the frame symmetrically: dark polished timber, six deep recessed panels each, a "
     "plain brass ring handle on each leaf, a plain stone architrave around them. THE DOORS ARE "
     "COMPLETELY BARE — no lettering, no numbers, no nameplates, no notices, no crest above them. "
     "Low side light so one leaf is a stop brighter than the other",
     f"{N_PAPER}, {N_COURT}, lettering above the doors, crest, nameplate, notice, person",
     "So where is the line?", "HD-06"),

    ("R115", "G",
     "An interior stone archway framing A SECOND, SMALLER ARCHWAY BEYOND IT, photographed dead "
     "square on down the axis so the two openings sit one inside the other like a diagram of "
     "inside and outside: the near arch is dark and close, the far arch is smaller, paler and full "
     "of flat daylight. Both spaces are completely empty — no furniture, no people, no signage, no "
     "carving on either arch",
     f"{N_PAPER}, {N_COURT}, statue in the archway, carving, inscription, person",
     "distinguishes between credit files that consumer reporting agencies maintain internally, and "
     "the consumer credit reports that consumer reporting agencies disseminate to third-party "
     "creditors", "HD-06"),

    ("R116", "G",
     "A bare plastered wall meeting a stone floor, photographed close and square on so the frame "
     "is almost abstract: two thirds pale wall, one third grey stone, one dark horizontal line "
     "where they meet, and ONE HARD DIAGONAL EDGE OF SUNLIGHT cutting across both from the upper "
     "left. Nothing else is in the frame — no skirting detail, no socket, no mark, no object, "
     "nobody",
     f"{N_PAPER}, {N_COURT}, furniture, socket, sign, person, graffiti",
     "The mere presence of an inaccuracy in an internal credit file, if it is not disclosed to a "
     "third party, causes no concrete harm.", "HD-07"),

    ("R117", "G",
     "A plain stone bench set into a shallow alcove in a stone wall, photographed from a "
     "three-quarter angle six feet away: the seat is worn hollow in the middle by long use, the "
     "alcove is plain with no carving and no plaque, and hard side light from the left rakes "
     "across the stone and throws the bench's shadow onto the floor. Nobody sitting on it and "
     "nothing left on it",
     f"{N_PAPER}, {N_COURT}, plaque, inscription, person, coat on the bench",
     "What about the risk that it would be sent later?", "HD-09"),

    ("R118", "G",
     "A wide flight of stone steps photographed FROM ABOVE looking straight down them, so the "
     "treads make a stack of horizontal bands running to the bottom of the frame: the stone is "
     "worn unevenly, deeper in two lanes where people walk and untouched at the edges, and flat "
     "overcast light makes every nosing read as a fine dark line. The steps are completely empty",
     f"{N_PAPER}, {N_COURT}, person, handrail shadow shaped like letters, painted markings, "
     "hazard stripes",
     "So the eight thousand, one hundred and eighty-five split in two.", "HD-11"),

    ("R119", "G",
     "A plain interior balcony rail on an upper floor, photographed from behind the rail looking "
     "down and out over an empty stone hall below: the rail runs across the lower third of the "
     "frame as a strong horizontal, the floor of the hall lies far below with one shaft of window "
     "light across it, and NOBODY IS ANYWHERE IN THE HALL. The rail and the balustrade are plain "
     "with no motif and no lettering",
     f"{N_PAPER}, {N_COURT}, person below, inlaid seal in the floor, banner, sculpture",
     "The judgment below was reversed, and the case was remanded for further proceedings.",
     "HD-12"),

    ("R120", "G",
     "A shuttered window in a dark panelled room, photographed square on from six feet away: the "
     "louvred shutters are almost closed and lay a ladder of hard bright slats across the dark "
     "wood panelling to the right of the window and across the floor. The panelling is plain, the "
     "shadow detail holds everywhere, and there is no furniture, no picture on the wall, no "
     "lettering and nobody in the room",
     f"{N_PAPER}, {N_COURT}, portrait on the wall, framed picture, person, crushed black shadow, "
     "venetian blind noir cliche with smoke",
     "It would be very easy to make the majority sound stupid here, and it was not.", "HD-10"),

    ("R121", "G",
     "A single reading lamp lit on a side table in an otherwise dark panelled room, photographed "
     "from a standing three-quarter angle: the lamp throws a warm pool onto the table and the arm "
     "of an empty upholstered chair beside it, and the rest of the room falls away into shadow "
     "that still holds its grain and its edges. THE TABLE IS EMPTY and the chair is empty. Nobody "
     "in the room",
     f"{N_PAPER}, book on the table, papers, person, crushed black shadow, portrait on the wall",
     "Justice Kagan wrote separately, and shorter.", "KG-01"),

    ("R122", "G",
     "A stone threshold seen from INSIDE a dark room, the heavy door standing wide open onto flat "
     "grey daylight so the doorway is a bright rectangle and the worn stone sill is the brightest "
     "thing in the lower frame: WHAT IS BEYOND THE DOOR IS BLOWN OUT AND FEATURELESS — no street, "
     "no building, no figure, nothing resolvable at all, only even white light. The door leaf and "
     "the jamb are plain with no lettering. Nobody in the frame",
     f"{N_PAPER}, {N_COURT}, view of a street, figure in the doorway, silhouette, sign on the "
     "door",
     "It did not decide what would have happened in a suit for an injunction rather than damages.",
     "ND-05"),

    # ------------------------------ H the money and the cancelled trip (headroom, R123-R130)
    ("R123", "H",
     "A retail bank counter photographed square on from the customer's side at standing height, "
     "the counter running across the frame with a plain glass screen above it and an empty teller "
     "position behind: everything completely unbranded — no name, no logo, no rate board, no "
     "posters, no leaflet stand with printed covers, no numbered ticket display. A plain terminal "
     f"on the counter is turned away. {NO_SCREEN}. Nobody in the frame. Even interior daylight",
     f"{N_PAPER}, {N_SCREEN}, bank logo, rate board, posters, leaflets with text, queue number "
     "display, person",
     "statutory and punitive damages are available under the Act for willful violations",
     "MN-10"),

    ("R124", "H",
     "A single cheque-sized slip of pale paper lying alone on a plain dark surface, photographed "
     f"from directly overhead so it sits small and precise in the middle of the frame. {GREY_RULE}, "
     "in three short groups laid where the lines of a payment slip would be, plus one longer flat "
     "grey bar across the foot where a signature would sit. No numbers, no letters, no name, no "
     "amount box, no printed border. One soft light from the left",
     f"{N_PAPER}, amount box, numbers, signature, bank name, printed border, currency symbol",
     "many of them would first learn that they were injured when they received a check", "HD-10"),

    ("R125", "H",
     "A narrow paper ribbon curling out of a plain mechanical adding machine and falling in a "
     "loose spiral onto the desk beneath it, photographed close from a low three-quarter angle "
     "with the machine soft behind: THE RIBBON IS COMPLETELY BLANK — plain white paper with no "
     "printing, no figures, no rules and no marks anywhere along its length. The machine's keys "
     "are unmarked blanks. Warm side light from the left",
     f"{N_PAPER}, printed figures on the tape, numbers on the keys, brand name on the machine",
     "More than sixty million dollars.", "MN-04"),

    ("R126", "H",
     "A paper till roll unspooled across a plain desk in a long loose S, photographed from "
     "directly overhead so the whole run of paper is visible: THE PAPER IS COMPLETELY BLANK from "
     "the roll to the torn end — no printing, no figures, no lines, no perforation marks. The "
     "roll itself sits at the top of the frame, half unwound. Even soft light",
     f"{N_PAPER}, printed receipt, figures, barcode, dashed lines, totals",
     "And it set no figure.", "MN-11"),

    ("R127", "H",
     "An airport departures hall at a quiet hour, photographed from a mezzanine at a shallow "
     "downward angle: a wide pale floor, a long line of check-in desks along the right, only five "
     "or six travellers spread across the whole space and all of them far off and unresolvable. "
     "THE LARGE DISPLAY BOARDS OVERHEAD ARE BLANK PANELS OF EVEN DARK GREY with nothing on them at "
     "all, and there is no signage, no airline name and no gate lettering anywhere in the frame",
     f"{N_PAPER}, {N_SCREEN}, flight information board, airline logo, gate numbers, signage, "
     f"sharp face, {N_EU}",
     "He cancelled a trip he had planned.", "SR-10"),

    ("R128", "H",
     "A closed hard-shell suitcase standing upright on its wheels in an ordinary domestic hallway "
     "beside a front door, photographed square on from four feet away at chest height: plain dark "
     "shell, plain handle, NO AIRLINE TAGS, NO STICKERS, NO NAME LABEL AND NO BRAND MARK anywhere "
     "on it. The hallway beyond is plain — a bare wall, a plain floor, the door with no numbers on "
     "it. Cool daylight from a fanlight out of frame",
     f"{N_PAPER}, luggage tag, airline sticker, name label, brand logo, house numbers, person",
     "an international vacation he had planned with his family", "SR-10"),

    ("R129", "H",
     "A closed passport-sized booklet lying face up in an open shallow drawer among nothing else, "
     "photographed from a standing angle looking down into the drawer. THE COVER IS COMPLETELY "
     "BLANK — plain dark grained board with no crest, no coat of arms, no gold blocking, no "
     "country name, no chip symbol, no lettering of any kind. The drawer interior is bare wood. "
     "Soft north light from the left",
     f"{N_PAPER}, coat of arms, gold blocking, country name, crest, chip symbol, other contents "
     "in the drawer",
     "ultimately canceled a planned trip to Mexico", "SR-11"),

    ("R130", "H",
     "The empty rear bench seat of an ordinary car photographed from the front passenger position "
     "looking back, in flat daylight through the windows: plain cloth upholstery, three seat belts "
     "hanging slack in their guides, nothing on the seat and nobody in the car. THE SEAT IS "
     "COMPLETELY BARE — nothing fixed to it, nothing strapped into it, no bags and no coats. The "
     "door cards and the headrests are plain and unmarked",
     f"{N_PAPER}, {N_BRAND}, infant seat, booster seat, bags, coats, person, dashboard display",
     "A trip he did not take.", "SR-10 · SR-11"),

    # ---------------------------- J the machine and the company, second angles (headroom, ACT_2)
    ("R131", "J",
     "TWO plain pale filing cards lying side by side and touching along one long edge on a dark "
     "matte surface, photographed from directly overhead in even soft light, THE TWO CARDS ALMOST "
     "BUT NOT QUITE THE SAME SIZE — one is a few millimetres wider and a shade taller than the "
     "other, so their outer edges do not line up and that near-miss is the whole subject of the "
     "picture. BOTH CARDS ARE COMPLETELY BLANK: no printing, no ruling, no writing, no tab, no "
     "punch hole. Nothing else is in the frame",
     f"{N_PAPER}, writing on the cards, hand, arrows, tick, cross, comparison marks",
     "A search would result in a match if the consumer's first and last name were either "
     "identical or similar to a name on the list.", "LS-16"),

    ("R132", "J",
     "A shallow office drawer pulled fully open, seen from a standing angle looking down into it, "
     "filled front to back with IDENTICAL EMPTY HANGING FILE POCKETS on two steel rails: every "
     "pocket the same colour, the same height and slack because nothing is in any of them. ALL "
     "THE TAB HOLDERS ARE EMPTY — bare plastic frames with no cards and no writing in a single "
     "one. Even office light from above, nobody in frame",
     f"{N_PAPER}, cards in the tab holders, handwritten labels, coloured tabs, files inside",
     "Beginning in 2002, TransUnion introduced an add-on product called OFAC Name Screen Alert.",
     "LS-13"),

    ("R133", "J",
     "A bank of grey steel filing cabinets photographed square on from six feet away, TWO DRAWERS "
     "IN THE SAME COLUMN treated differently: the upper drawer is pulled fully out and packed "
     "with identical blank paper files standing on edge, and the drawer below it is shut. EVERY "
     "LABEL HOLDER ON EVERY DRAWER FRONT IS EMPTY — bare metal frames, no cards, no writing, no "
     "numbers anywhere on the run. Flat even office light, nobody in frame",
     f"{N_PAPER}, drawer labels, numbers on the drawers, writing on the files, hand",
     "In collecting other types of data for use on consumer reports — such as tax liens or "
     "bankruptcy judgments — TransUnion used at least one additional identifier …", "LS-17"),

    ("R134", "J",
     "A single plain pale card lying alone on top of a folded stack of continuous fanfold paper, "
     "photographed close from a low three-quarter angle so the card is sharp and the perforated "
     "sprocket margins of the stack run away soft behind it. THE CARD IS COMPLETELY BLANK, and the "
     f"fanfold sheet beneath it carries no writing either. {GREY_RULE}. One soft light from the "
     "left",
     f"{N_PAPER}, writing on the card, printed figures, column headings, hand",
     "TransUnion presented no data showing that any of its name matches through the OFAC product "
     "were correct.", "LS-19"),

    ("R135", "J",
     "An empty corporate meeting room photographed from one corner at standing height: one long "
     "plain table, eight identical chairs pushed in, and a blank pale wall at the far end WITH "
     "NOTHING MOUNTED ON IT AT ALL — no screen, no whiteboard, no poster, no clock, no logo, no "
     "lettering. A run of windows down the left throws flat daylight across the table. Nothing on "
     "the table, nobody in the room",
     f"{N_PAPER}, {N_SCREEN}, whiteboard with writing, company logo, poster, person",
     "the company had determined that the alerts it was placing on consumer credit reports were "
     "exempt from the Fair Credit Reporting Act", "LS-20"),

    ("R136", "J",
     "An internal glazed partition between two offices, photographed square on from four feet "
     "away, the horizontal blind on the far side HALF OPEN so alternating bands of the empty room "
     "beyond and of pale blind slat cross the frame. The room beyond holds one bare desk and one "
     "empty chair. The glass carries a soft reflection of a plain wall and nothing else, and "
     "there is no lettering on it. Nobody in either room",
     f"{N_PAPER}, {N_SCREEN}, lettering on the glass, company name, person, reflection of a face",
     "That was the position. Whether it was right is the next act.", "LS-20"),

    ("R137", "J",
     "A plain corporate reception counter in an empty lobby, photographed square on from ten feet "
     "away at standing height: a long pale stone counter, an empty chair behind it, and a blank "
     "wall rising behind that WITH NOTHING ON IT — no company name, no logo, no lettering, no "
     "artwork, no directory board. A polished floor runs across the foreground and flat daylight "
     "comes from a glazed wall out of frame left. Nobody in the lobby",
     f"{N_PAPER}, company name on the wall, logo, directory board, artwork, person",
     "That is not the sentence that decides this case, though. This one is, and it is a footnote.",
     "LS-17"),

    ("R138", "J",
     "TWO plain pale cards lying flat on a large empty dark table, FAR APART FROM ONE ANOTHER — "
     "one near the left edge of the frame and one near the right, with a wide expanse of bare "
     "dark table between them and absolutely nothing in that gap. Photographed from directly "
     "overhead. BOTH CARDS ARE COMPLETELY BLANK. One soft light from the left so each card casts "
     "its own thin separate shadow",
     f"{N_PAPER}, writing on the cards, line joining them, arrow, hand, third card",
     "For a tax lien, a name was not enough. For a terrorist list, it was.", "LS-17"),

    # -------------------------------- K the letters going out, and the trial (headroom, ACT_3)
    ("R139", "K",
     "A plain mail-room bench photographed from a standing three-quarter angle: a wide grey "
     "worktop with a shallow open tray on it holding A TIGHT ROW OF IDENTICAL PLAIN WHITE "
     "ENVELOPES STANDING ON EDGE, all the same size, packed so their top edges make one straight "
     "unbroken line across the tray. EVERY ENVELOPE IS BLANK — no address, no window, no stamp, "
     "no franking mark. Hard even overhead light, a bare wall behind, nobody in the frame",
     f"{N_PAPER}, address blocks, window envelopes, stamps, franking, barcodes",
     "Between the first of January and the twenty-sixth of July, 2011, the letters kept going "
     "out.", "MN-01"),

    ("R140", "K",
     "The feed tray of a plain grey mailing machine, photographed close from a low three-quarter "
     "angle, A STACK OF IDENTICAL BLANK WHITE ENVELOPES loaded into it with the topmost one just "
     "entering the rollers. EVERY ENVELOPE IS BLANK — no address, no window, no stamp, no "
     "franking mark — and the machine itself carries no maker's name and no control panel with "
     "readable icons. Even workshop light, nobody in the frame",
     f"{N_PAPER}, {N_SCREEN}, address blocks, franking impression, brand name on the machine, "
     "panel icons",
     "TransUnion sent the same OFAC letter to eight thousand, one hundred and eighty-four other "
     "consumers …", "SR-13"),

    ("R141", "K",
     "A wall of identical small residential mailboxes in an apartment lobby, photographed square "
     "on so the grid of doors fills the whole frame: eight across and six down, every door shut, "
     "every one the same brushed aluminium with the same small keyhole and the same little "
     "name-card slot. ALL THE NAME SLOTS ARE EMPTY AND NO DOOR CARRIES A NUMBER. Even flat lobby "
     "light, nobody in the frame",
     f"{N_PAPER}, box numbers, name cards, handwritten labels, junk mail sticking out, person",
     "eight thousand, one hundred and eighty-four other consumers who had also requested copies "
     "of their credit reports in that window", "SR-13"),

    ("R142", "K",
     "A single bundle of identical plain white envelopes held together by a paper band, LYING ON "
     "ITS SIDE AND PUSHED TO ONE END of an otherwise completely empty grey counter, photographed "
     "from a low three-quarter angle so the bare counter runs away empty across the rest of the "
     "frame. Every envelope in the bundle is blank, AND THE PAPER BAND AROUND THEM IS BLANK TOO — "
     "no printing, no writing, no batch mark. Cool even light, nobody in the frame",
     f"{N_PAPER}, printing on the band, batch number, address blocks, stamps, hand",
     "In July 2011, TransUnion finally stopped sending the letters …", "LS-21"),

    ("R143", "K",
     "Six identical plain white paper cups left standing on a bare wooden table in a plain room at "
     "the end of a long day, photographed from a standing three-quarter angle: most upright, two "
     "knocked slightly askew, all of them empty and ALL OF THEM COMPLETELY UNMARKED with no "
     "printing, no logo and no writing on any cup. Nothing else on the table at all. Flat "
     "overhead light, nobody in the room",
     f"{N_PAPER}, printing on the cups, logo, coffee shop branding, notepads, person",
     "The trial ran six days.", "MN-04"),

    # ------------------------- L what was not decided, and the ending (headroom, ACT_5 / ENDING)
    ("R144", "L",
     "A single plain panelled door standing closed at the far end of a dim corridor, photographed "
     "straight down the corridor from twenty feet away at eye height: the walls and the floor "
     "fall away into shadow that still holds all of its detail, and A THIN HARD LINE OF LIGHT "
     "shows under the door and lies a short way out across the floor. The door is completely bare "
     "— no number, no nameplate, no sign, no notice. Nobody in the corridor",
     f"{N_PAPER}, {N_COURT}, door number, nameplate, exit sign, person, crushed black shadow",
     "It did not decide whether TransUnion violated the Fair Credit Reporting Act.", "ND-01"),

    ("R145", "L",
     "The same ordinary American residential street as the dusk plate, photographed from the same "
     "position in the middle of the road at the same standing height, NOW AT FIRST LIGHT AND "
     "COMPLETELY EMPTY: the same houses, the same driveways, the same kerbline running away to "
     "the same vanishing point, the sky pale and cold, every window dark, NOBODY ANYWHERE IN THE "
     "FRAME and nothing moving. No house numbers, no street sign, no parked car in the road",
     f"{N_PAPER}, {N_EU}, house numbers, street sign, person, car headlights, sunrise glow",
     "The record this film is built on ends on the twenty-fifth of June, 2021 …", "⛔-12 · ○-04"),

    ("R146", "L",
     "ONE plain white envelope lying alone at the centre of a large bare wooden table, "
     "photographed from a low angle almost level with the table top so the envelope reads as one "
     "thin bright horizontal in the middle of the frame and the room beyond falls soft and grey. "
     "The envelope is completely blank and still sealed. Nothing else is on the table and nobody "
     "is in the room. Flat even daylight from a window out of frame left",
     f"{N_PAPER}, address block, stamp, person, hand, second envelope",
     "Justice Kagan's question is still on the table, and it is a short one.", "KG-04"),

    # ------------------------------------------------------- T thumbnail plates (never a cut)
    ("T001", "T",
     "A car-dealership sales desk seen from behind the customer's shoulder and slightly above, "
     "THE WHOLE SUBJECT SITTING IN THE LOWER 60 PERCENT OF THE FRAME: TWO ADULT HANDS LIE FLAT "
     "AND SEPARATE ON THE DESK TOP in the near foreground, palms down and in full contact with "
     "the surface, the four fingers of each hand side by side with a line of shadow between each "
     "pair and one nail visible on each, both thumbs clearly apart; a set of unmarked car keys "
     "sits on the far side of the desk just out of their reach; a slim monitor stands at the far "
     f"edge TURNED AWAY so only its plain back is visible. {NO_SCREEN}. Bright showroom glass "
     "and a sunlit forecourt fill the bottom third and are the brightest thing in the picture. "
     "The upper 40 percent is one unbroken field of plain out-of-focus showroom shadow",
     f"{N_HAND}, {N_SCREEN}, {N_PAPER}, {N_BRAND}, face, head, object in the top of the frame, "
     "ceiling detail, hanging sign, low contrast, dull flat lighting, dark subject, "
     "detail crossing the top of the frame",
     "PACKAGING §2 variant 1 — headline NAME ONLY / kicker NO OTHER CHECK", "SR-02 · SR-03"),

    ("T002", "T",
     "The same dealership desk, closer and lower: ONE ADULT HAND LIES FLAT ON THE BARE DESK in "
     "the near lower left of the frame with its four fingers side by side and separate, each with "
     "its own nail and its own shadow, and the thumb clearly apart; A SET OF UNMARKED CAR KEYS "
     "lies on the desk to the right of it. Both are low in the frame and both are hit by one hard "
     "directional key light from the left that makes them markedly brighter than anything behind "
     "them. The bottom third of the frame is bright bare desk. The upper 40 percent is one "
     "unbroken field of plain dark out-of-focus interior with nothing in it at all",
     f"{N_HAND}, {N_SCREEN}, {N_PAPER}, {N_BRAND}, face, object in the top of the frame, "
     "low contrast, dull flat lighting, dark subject, detail crossing the top of the frame",
     "PACKAGING §2 variant 1, alternate — headline NAME ONLY", "SR-02 · SR-03"),

    ("T003", "T",
     "An office desk drawer pulled HALF OPEN with A SINGLE UNOPENED PLAIN WHITE ENVELOPE lying "
     "alone inside it and the rest of the drawer bare empty wood, photographed from a standing "
     "angle looking down, THE DRAWER AND THE ENVELOPE FILLING THE LOWER 60 PERCENT OF THE FRAME. "
     "One hard directional daylight from the left makes the envelope the brightest object in the "
     "picture and lays a crisp shadow from it across the drawer bottom; the bright uncluttered "
     "desk surface runs across the bottom third. The envelope is completely blank — no address, "
     "no window, no stamp. The upper 40 percent is one unbroken field of plain out-of-focus dark "
     "office with nothing crossing it",
     f"{N_PAPER}, address block, stamp, other contents in the drawer, hand, "
     "object in the top of the frame, low contrast, dull flat lighting, dark subject, "
     "detail crossing the top of the frame",
     "PACKAGING §2 variant 2 — headline NEVER SENT / kicker 6,332 FILES", "HD-08"),

    ("T004", "T",
     "The same desk drawer and the same single blank envelope, closer and from a lower angle "
     "almost level with the desk top: the drawer front makes one strong bright horizontal across "
     "the lower third of the frame, the near corner of the envelope rises just above it catching "
     "a hard key light from the left, and the whole picture is bright and high contrast. The "
     "envelope is completely blank. The upper 40 percent is one unbroken field of plain "
     "out-of-focus darkness with nothing in it",
     f"{N_PAPER}, address block, stamp, hand, object in the top of the frame, low contrast, "
     "dull flat lighting, dark subject, detail crossing the top of the frame",
     "PACKAGING §2 variant 2, alternate — headline NEVER SENT", "HD-08"),

    ("T005", "T",
     "A dense field of small identical pale record cards laid edge to edge in a regular grid, "
     "photographed from directly above, ONE CARD LIFTED SLIGHTLY OUT OF THE GRID near the bottom "
     "of the frame and catching a hard directional key light so that it is markedly brighter than "
     "every card around it and throws a crisp shadow onto them. EVERY CARD IS COMPLETELY BLANK — "
     "no printing, no ruling, no writing, no numbers. The grid is brightest along the bottom edge "
     "of the frame, and the upper 40 percent of the frame is one unbroken even field of the same "
     "cards gone soft and featureless out of focus, with no edge crossing it",
     f"{N_PAPER}, writing on the cards, printed forms, hand, numbers, "
     "object in the top of the frame, low contrast, dull flat lighting, dark subject, "
     "detail crossing the top of the frame",
     "PACKAGING §2 variant 3 — headline 8,185 NAMES / kicker ONE CHECK EACH", "MN-02 · LS-15"),

    ("T006", "T",
     "The same field of identical blank record cards, photographed from a slightly raking angle "
     "just above the surface so the near cards are large and bright across the bottom third of "
     "the frame, ONE CARD STANDING PROUD of the others in the lower middle and lit hard from the "
     "left so it is the brightest and sharpest thing in the picture. All cards completely blank. "
     "The upper 40 percent of the frame is one unbroken field of the receding grid gone entirely "
     "soft and even, with no edge and no horizon crossing it",
     f"{N_PAPER}, writing on the cards, hand, numbers, object in the top of the frame, "
     "low contrast, dull flat lighting, dark subject, detail crossing the top of the frame",
     "PACKAGING §2 variant 3, alternate — headline 8,185 NAMES", "MN-02 · LS-15"),
]

# ---------------------------------------------------------------------------------------------
# lanes: (key, human label, paste chunks as list of (first_index, last_index) within the lane)
# ---------------------------------------------------------------------------------------------
LANES: dict[str, dict] = {
    "A1": {"title": "A1 · the dealership counter", "range": "R001–R017", "chunk": 9,
           "act": "HOOK / OP / ACT_1 — bright Californian daylight, glass, chrome, asphalt",
           "mandatory": True},
    "A2": {"title": "A2 · the two mailings", "range": "R018–R031", "chunk": 7,
           "act": "ACT_1 — domestic, kitchen-table scale, morning light",
           "mandatory": True},
    "A3": {"title": "A3 · the desk drawer", "range": "R032–R041", "chunk": 10,
           "act": "ACT_1 → ENDING — the majority's own metaphor, ONE camera position for all ten",
           "mandatory": True},
    "A4": {"title": "A4 · the courts, from outside", "range": "R042–R053", "chunk": 6,
           "act": "ACT_3 / ACT_4 / ACT_5 — stone, doors, columns, light. No courtroom interior",
           "mandatory": True},
    "B":  {"title": "B · the identifiers that were never compared", "range": "R054–R072",
           "chunk": 7,
           "act": "ACT_2 — the objects, never the words. Typography goes over them in Remotion",
           "mandatory": True},
    "C":  {"title": "C · the people lane  [HSTYLE]", "range": "R073–R096", "chunk": 6,
           "act": "all acts — 24 plates, all mandatory, nine carrying a resolvable face",
           "mandatory": True},
    "E":  {"title": "E · Treasury and the federal register", "range": "R097–R104", "chunk": 8,
           "act": "ACT_2 — added at 122; ACT_2 is 23.2% of the narration and the longest act",
           "mandatory": True},
    "F":  {"title": "F · 1970 and the statute", "range": "R105–R112", "chunk": 8,
           "act": "ACT_3 — added at 122; the script's own ACT_3 header already calls R105–R112",
           "mandatory": True},
    "G":  {"title": "G · the law, ACT_4 and ACT_5", "range": "R113–R122", "chunk": 5,
           "act": "ACT_4 / ACT_5 — added at 122; those two acts are 35.5% of the narration and "
                  "owned only four dedicated plates each",
           "mandatory": True},
    "H":  {"title": "H · the money, and the cancelled trip", "range": "R123–R130", "chunk": 4,
           "act": "ACT_1 / ACT_3 / ACT_4 / ACT_5 — headroom tier: ordered, NOT declared",
           "mandatory": False, "tier": "headroom"},
    "J":  {"title": "J · the machine and the company, second angles", "range": "R131–R138",
           "chunk": 4,
           "act": "ACT_2 — headroom tier: ordered, NOT declared",
           "mandatory": False, "tier": "headroom"},
    "K":  {"title": "K · the letters going out, and the trial", "range": "R139–R143", "chunk": 5,
           "act": "ACT_3 — headroom tier: ordered, NOT declared",
           "mandatory": False, "tier": "headroom"},
    "L":  {"title": "L · what was not decided, and the ending", "range": "R144–R146", "chunk": 3,
           "act": "ACT_5 / ENDING — headroom tier: ordered, NOT declared",
           "mandatory": False, "tier": "headroom"},
    "T":  {"title": "T · THUMBNAIL PLATES  [TSTYLE]", "range": "T001–T006", "chunk": 6,
           "act": "front of house — never a cut, never in mandatory_stills, own bright [TSTYLE]",
           "mandatory": False, "tier": "thumb"},
}


# ---------------------------------------------------------------------------------------------
def prompt_body(pid: str, lane: str, body: str, neg_add: str) -> str:
    """The one and only place a prompt string is assembled."""
    head = f"[HSTYLE] {HSTYLE}. " if lane == "C" else ""
    tail = "[TSTYLE]" if lane == "T" else "[STYLE]"
    return f"{head}{body} {tail} Avoid: [NEG], {neg_add}"


def tier_of(lane: str) -> str:
    """declared = in episode_spec.mandatory_stills; headroom = ordered but not declared;
    thumb = front of house, never a cut."""
    return LANES[lane].get("tier", "declared")


def plates_by_lane() -> dict[str, list[tuple]]:
    out: dict[str, list[tuple]] = {k: [] for k in LANES}
    for row in P:
        out[row[1]].append(row)
    return out


def chunks(seq: list, n: int) -> list[list]:
    return [seq[i:i + n] for i in range(0, len(seq), n)]


# ---------------------------------------------------------------------------------------------
def build_md() -> str:
    by = plates_by_lane()
    mand = [r for r in P if tier_of(r[1]) == "declared"]
    extra = [r for r in P if tier_of(r[1]) == "headroom"]
    thumbs = [r for r in P if tier_of(r[1]) == "thumb"]
    L: list[str] = []
    a = L.append

    a("# EP67 · TRANSUNION v. RAMIREZ — IMAGE ORDER (Codex) **v002 · the prompts**")
    a("")
    a("**Episode `PD-2026-067-ramirez` · slug `ramirez` · 2026-08-11**")
    a("")
    a("> **What changed from v001.** v001 named the lanes and the id ranges and contained "
      "**zero prompts** — 0 occurrences of `[STYLE]`, 0 of `Avoid: [NEG]`. It could not be pasted "
      "into anything. This revision writes the prompt bodies. **v001 is not edited and stays on "
      "disk** (invariant 6); everything it says about policy, era and the barred likenesses still "
      "binds and is restated below.")
    a("")
    a(f"> **And the count changed: {len(P)} prompts, not 96.** Re-derived with the builder's own "
      "solver rather than guessed — see §0.1. They are in **three tiers, and the tiers are not "
      "interchangeable**:")
    a(">")
    a(f"> | tier | ids | count | in `episode_spec.mandatory_stills`? |")
    a("> |---|---|---:|---|")
    a(f"> | **1 · declared** | `R001`–`R122` | **{len(mand)}** | **yes** — the film will place "
      "exactly this many still cuts |")
    a(f"> | **2 · headroom** | `R123`–`R146` | **{len(extra)}** | **no** — cover against "
      "rejections and against the script growing |")
    a(f"> | **3 · thumbnail** | `T001`–`T006` | **{len(thumbs)}** | **no** — a thumbnail never "
      "becomes a cut |")
    a(">")
    a("> **Declaring all 152 would fail the build.** `check_spec_satisfied.py` fails any "
      "`mandatory_stills` id that appears in no cut, and at the current script length the solver "
      f"places {len(mand)} still cuts and no more. That correction had to be made late on EP65. "
      "**Do not \"tidy\" these three numbers into agreement.**")
    a("")
    a("**Design:** `EP67_ramirez_FILM_BIBLE.v001.md` · **Front:** `EP67_ramirez_PACKAGING.v001.md` "
      "· **Facts:** `EP67_ramirez_FACTS_LEDGER.v001.md` · **Script:** "
      "`EP67_ramirez_script.en.v001.md`.")
    a("")
    a("**Paste files:** `episodes/_planning/EP67_ramirez_CODEX_PASTE_A/` — one file per group, "
      "generated from the same Python source as this document "
      "(`scripts/build_ep67_ramirez_image_order.py`), so the prompt bodies cannot drift apart.")
    a("")
    a("---")
    a("")

    # 0.1 the count
    a("## 0.1 How many plates, derived rather than chosen")
    a("")
    a("`scripts/build_case_film_generic.py` decides the cut mix. Its constants: `MAX_STILL_REUSE "
      "= 1` (**a still is used once**, so the still-cut count *is* the distinct-still count), "
      "`MIN_VIDEO_SHARE = 0.68`, `_CAP_FACTORY = 1`. The episode declares `target_cut_sec` **3.8** "
      "and `distinct_video_assets` **260**. The builder reads the declared cut length at line 406 "
      "and scales the runtime it hands the solver by `TARGET_CUT_SEC / 3.8`, so 3.8 is what the "
      "real build uses — running the solver at the module default 4.6 gives a different and wrong "
      "answer.")
    a("")
    a("```")
    a("py -3.11 -c \"import sys;sys.path.insert(0,'scripts');import build_case_film_generic as B;"
      "B.TARGET_CUT_SEC=3.8;print(B.solve_totals(60*5000/159.5,260,0,400))\"")
    a("")
    a("across the DECLARED word band script_words [4400,5000] x the measured pace band 159.5-169.7")
    a("still pool left unbounded (400) so the ceiling shows itself:")
    a("")
    a(" words    wpm   narr s |  cuts  video  STILL")
    a("  4400  169.7   1555.7 |   382    260    122")
    a("  4400  159.5   1655.2 |   382    260    122")
    a("  4682  169.7   1655.4 |   382    260    122")
    a("  4682  159.5   1761.3 |   382    260    122")
    a("  5000  169.7   1767.8 |   382    260    122")
    a("  5000  159.5   1880.9 |   382    260    122")
    a("```")
    a("")
    a("**122 is flat across the whole declared band, and that is not a coincidence.** The binding "
      "constraint is not runtime — it is `still_max_for_share = floor(video x (1 - 0.68) / 0.68)`, "
      "and `video` is capped at the declared 260 distinct video assets. `floor(260 x 0.32 / 0.68)` "
      "= **122**. Lengthening the script does not raise the still requirement; only raising "
      "`distinct_video_assets` does.")
    a("")
    a("**Rejection allowance.** EP66's batch C is the only measured rate this channel has: 191 "
      "ordered, **11 REJECT (5.8%)** and 10 further FLAG (**11.0% combined**).")
    a("")
    a("```")
    a("  122 / (1 - 0.058) = 130    hard rejects only")
    a("  122 / (1 - 0.110) = 138    rejects + flags")
    a("```")
    a("")
    a(f"**Ordered: {len([r for r in P if tier_of(r[1]) != 'thumb'])} plates.** 138 from the "
      "reject-and-flag allowance, plus 8 more, because the still ceiling moves with "
      "`distinct_video_assets`: at a video pool of 300 the ceiling is `floor(300 x 0.32 / 0.68)` = "
      "**141**, and archive supply was measured at 5,537 usable clips, so the pool may well be "
      "raised at staging. 146 covers a video pool up to about 310. **Declared: 122.** The "
      "difference is the whole point — see the tier table above.")
    a("")
    a("> **`docs/PD_CANON.md` rule 25 applies: the band is a prediction, the delivered VO is the "
      "measurement.** `episode_spec.v001.json` carries a TODO saying `mandatory_stills` is "
      "re-derived from the measured narration master before assembly. If the delivered master "
      "lands outside 1555.7-1880.9 s, or if `distinct_video_assets` is changed, **re-run the "
      "solver and re-declare** — do not carry 122 forward on faith.")
    a("")
    a("**Where the plates went, and why there.** Narration words per section, counted from the "
      "script with citation comments and stage directions excluded:")
    a("")
    a("| section | words | share | dedicated plates in v001 | added here |")
    a("|---|---:|---:|---|---|")
    a("| HOOK + OP | 196 | 4.6% | borrows from A1 / C | — |")
    a("| ACT_1 | 529 | 12.5% | R001–R031, R073–R082 | R127–R130 (headroom) |")
    a("| ACT_2 | 985 | **23.2%** | R054–R072, R083–R084 | **+8 R097–R104**, +8 R131–R138 "
      "(headroom) |")
    a("| ACT_3 | 827 | 19.5% | R042–R053 shared, R085–R089 | **+8 R105–R112**, +5 R139–R143 "
      "(headroom) |")
    a("| ACT_4 | 676 | **15.9%** | R090, R091 + a shared court lane | **+10 R113–R122 with "
      "ACT_5**, +4 R123–R126 (headroom) |")
    a("| ACT_5 | 830 | **19.6%** | R092–R094 + the same shared court lane | **+10 R113–R122 with "
      "ACT_4**, +3 R144–R146 (headroom) |")
    a("| ENDING | 197 | 4.6% | R017, R041, R095, R096 | R145, R146 (headroom) |")
    a("")
    a("ACT_4 and ACT_5 together are **35.5% of the narration**, and in v001 they had four "
      "dedicated plates each plus a twelve-plate courthouse lane they were expected to share with "
      "ACT_3 — which `MAX_STILL_REUSE = 1` makes impossible: twelve plates across three acts is "
      "four each, full stop. That is why lane G exists and why it is ten plates rather than an "
      "even spread. ACT_2 is the longest act and the one the bible names as most likely to fall "
      "into kamishibai, so it takes eight. ACT_3 takes the eight the script's own ACT_3 header "
      "already calls by name (`R105–R112`).")
    a("")
    a("**Thumbnails are their own lane and add nothing to `mandatory_stills`.** `T001`–`T006` are "
      "two candidates for each of PACKAGING §2's three variants. They are built to a "
      "**thumbnail-only `[TSTYLE]`** (§2) because the canonical `[STYLE]` asks for low contrast — "
      "which is correct for a film frame and is exactly why EP65's four candidates came back dull "
      "and had to be re-ordered. **`[NEG]` is not deviated for them.**")
    a("")
    a("---")
    a("")

    # 1 policy
    a("## 1. Who generates these, and the one thing that is barred")
    a("")
    a("- **Long-form images are Codex by default** (`.claude/rules/19-ship-gate.md` line 10). "
      "Every plate here is a Codex commission. **Do not start a local model to fill this order.**")
    a("- Local generation is an exception, not a lane: **SD3.5 Large** (`sd35_gen.py`) or **SDXL** "
      "(`gen_max.ps1`) only to repair a Codex plate or fill an emergency gap. **Bare SDXL is not "
      "allowed. FLUX.1-dev is not allowed in any deliverable.**")
    a("- **Long edge ≥ 3840, PNG, 16:9.** Every plate is an illustration, never evidence "
      "(CLAUDE invariant 11).")
    a("")
    a("**People are required and faces are welcome** (owner decision 2026-07-04). What is barred "
      "absolutely is the **likeness of a real, identifiable individual**, and in this episode that "
      "has five names attached:")
    a("")
    a("| Never depict as a person | Why |")
    a("|---|---|")
    a("| **Sergio L. Ramirez** | a living private individual (⛔-07) |")
    a("| **his wife, his father-in-law** | same; the record gives their presence and nothing else "
      "(SR-01) |")
    a("| **the Nissan salesman or any dealership employee** | never named, never a party, never "
      "heard (⛔-08) |")
    a("| **the two SDNs who \"purportedly matched\" him** | the record does not print their names "
      "(⛔-09) |")
    a("| **any Justice** | opinions appear as attributed typography, never as a portrait |")
    a("")
    a("Nine plates in lane C carry a resolvable face. **Every one of them is written as INVENTED "
      "and COMPLETELY FICTIONAL in the prompt body itself**, and none is captioned, cut or "
      "narrated as anyone in this record.")
    a("")
    a("**Four things are never produced as an image at all, in any style** (⛔-13): a TransUnion "
      "credit report, the OFAC Letter, an OFAC / SDN list entry, any court record or filing. "
      "Their *words* may be set as Remotion typography — card, not scan.")
    a("")
    a("### 1.1 No readable anything, and it is ordered in the POSITIVE prompt")
    a("")
    a("This episode is dense with the hazard: credit reports, letters, a dealership desk, court "
      "buildings, a passport. **A generator asked for \"a credit report\" writes words on it.** "
      "EP66's `L146` proved a `[NEG]` ban alone does not hold — the wordmark came back twice after "
      "being banned twice. So every document in this order is ordered as a **shape**, in the "
      "positive prompt, using one of two fixed clauses:")
    a("")
    a(f"- **grey ruled blocks** — *{GREY_RULE}*")
    a(f"- **genuinely blank** — *{BLANK_PAPER}*")
    a("")
    a("The same applies to brands (**no Nissan badge, no dealership signage, no TransUnion mark, "
      "no Treasury seal** — the car is *a mid-size saloon*, the lot is *a lot*), to screens "
      f"(*{NO_SCREEN}*), and to hands.")
    a("")
    a("### 1.2 Hands")
    a("")
    a("EP66's `L236` failed twice on a raised hand with fused fingers. The fix that worked was to "
      "**rest the hand flat on a surface**, and that geometry is reused verbatim wherever hands "
      "are the subject:")
    a("")
    a(f"> {FLAT_HAND}")
    a("")
    a("`R087` deviates from v001's wording for this reason: v001 said *\"hands folded\"*, which is "
      "interlocked fingers — the exact failure. It is ordered here as **both hands flat and "
      "separate on his own knees**, and `interlocked fingers` is added to that plate's `[NEG]`.")
    a("")
    a("### 1.3 Era")
    a("")
    a("`era_setting` is **Dublin, CALIFORNIA**, 2011–2026. Nothing may date the shot outside it "
      "and nothing may relocate it: an Irish establishing shot pulled on the word *dublin* is the "
      "mistake the field exists to make visible. Every lane's `[NEG]` carries the European-"
      "streetscape block.")
    a("")
    a("---")
    a("")

    # 2 style
    a("## 2. Style blocks (★ expand before generating)")
    a("")
    a("**`[STYLE]`** — appended to every plate in this order, exactly as written:")
    a("")
    a(f"> {STYLE}")
    a("")
    a("**`[NEG]`** — after `Avoid:`, exactly as written. **This block is byte-identical to EP66 "
      "batch D's** and was lifted out of `EP66_openfields_CODEX_BATCH_D.v001.md` by the generator "
      "rather than retyped:")
    a("")
    a(f"> {NEG}")
    a("")
    a("> ### ★ Per-plate `[NEG]` additions ★")
    a("> Every plate reads `Avoid: [NEG], …`. That means: **expand the canonical block above in "
      "full, then append the extra words.** **Do not delete one word of the canonical block.** "
      "Only additions ever happen.")
    a(">")
    a("> ### ★ The `[NEG]` does not forbid people ★")
    a("> What it forbids is **`recognisable person, identifiable person, likeness of a real "
      "individual, portrait of a named person, celebrity, public figure, deepfake`** — resembling "
      "a real someone. EP66's batch A wrote `human face, facial features, eyes …`, stopped people "
      "appearing at all, and **cost 191 plates a rebuild. Those three tokens are absent here and "
      "must stay absent.**")
    a("")
    a("**`[HSTYLE]`** — prepended (before the body) on lane C only, R073–R096, exactly as "
      "`EP67_ramirez_CODEX_BATCH_A.v001.md` §3 wrote it:")
    a("")
    a(f"> {HSTYLE}")
    a("")
    a("**`[TSTYLE]`** — **thumbnail lane only**, T001–T006. Replaces `[STYLE]` on those six "
      "prompts and nowhere else. The `[NEG]` is unchanged:")
    a("")
    a(f"> {THUMB_STYLE}")
    a("")
    a("---")
    a("")

    # 3 naming
    a("## 3. Naming and delivery")
    a("")
    a("- **Names are exactly `R001.png` … `R146.png` and `T001.png` … `T006.png`.** "
      "`check_spec_satisfied.py` reads "
      "`mandatory_stills` by basename; a plate called `ramirez_drawer_final.png` does not exist as "
      "far as the contract is concerned. **No `_v2`, no `_02`, no `_A`.**")
    a("- **One prompt = one image.** Do not run a prompt twice and keep the better one.")
    a("- **Do not put any `forbidden_subjects` word in a filename** — the gate matches them "
      "word-wise against source filenames, so `R044_gavel_door.png` fails the build even though "
      "the picture is a door.")
    a(f"- Deliver to `{SAVE_DIR}\\`, long edge ≥ 3840, 16:9, PNG.")
    a("- Depth maps for the plates that take 2.5D motion go to "
      "`remotion/public/ramirez/img/<name>_depth.png` — **a still that is only Ken Burns-zoomed is "
      "rejected as kamishibai.**")
    a("- After delivery: build a **labelled contact sheet and look at it**, then "
      "`py -3.11 scripts/check_episode_inputs.py --slug ramirez`.")
    a("")
    a("---")
    a("")

    # 4 the prompts
    a(f"## 4. THE PROMPTS — tier 1, declared, {len(mand)} plates (R001–R122)")
    a("")
    a("Each plate gives the line of narration it lands on and the ledger row behind it. "
      "**A plate with no beat is not commissioned** — that rule is why there are no filler plates "
      "in this order.")
    a("")
    for key, meta in LANES.items():
        rows = by[key]
        if not rows or tier_of(key) != "declared":
            continue
        a(f"### {meta['title']} — {meta['range']} ({len(rows)} plates)")
        a("")
        a(f"*{meta['act']}*")
        a("")
        for pid, lane, body, neg_add, line, ledg in rows:
            a(f"#### `{pid}.png`")
            a("")
            a(f"**Lands on:** \"{line}\" · **ledger** {ledg}")
            a("")
            a(f"- `{pid}.png`")
            a(prompt_body(pid, lane, body, neg_add))
            a("")
            a(f"**Save as:** `{SAVE_DIR}\\{pid}.png`")
            a("")
            a(f"**`[NEG]` addition:** append `, {neg_add}` to the canonical `[NEG]`. "
              "**Delete nothing from the canonical block.**")
            a("")

    # 5 headroom + thumbnails
    a(f"## 5. TIER 2 — headroom, {len(extra)} plates, R123–R146, **not declared in the spec**")
    a("")
    a("**Generate these.** They are not optional in the sense of \"skip them\"; they are ordered "
      "in this pass so that a rejected tier-1 plate can be swapped for a working one without a "
      "second commission round, and so that a longer delivered narration or a raised "
      "`distinct_video_assets` does not leave the film short. What they are *not* is **declared**: "
      "`episode_spec.v001.json` lists R001–R122 only, because a declared still that lands in no "
      "cut fails `check_spec_satisfied.py`.")
    a("")
    a("Every one of them still carries a script line and a ledger row — **a plate with no beat is "
      "not commissioned**, headroom or otherwise.")
    a("")
    a("v001 listed R097–R130 as an optional second pass. Here is what happened to each band, so "
      "nobody has to guess later:")
    a("")
    a("| v001 optional band | disposition |")
    a("|---|---|")
    a("| R097–R104 Treasury / federal register | **promoted to tier 1**, lane E |")
    a("| R105–R112 1970 and the FCRA | **promoted to tier 1**, lane F — the script's ACT_3 header "
      "already called them by name |")
    a("| R113–R120 the money, kept abstract | **band reassigned** to lane G (ACT_4 / ACT_5 stone), "
      "which is where the shortage measured. The four money plates survive as R123–R126 |")
    a("| R121–R126 weather and the four designed silences | **dropped.** The designed silences "
      "already have plates written for them — R091 carries ACT_4's four seconds — and a weather "
      "plate is the definition of 汎用素材 |")
    a("| R127–R130 the cancelled trip | **kept**, as R127–R130 |")
    a("")
    for key, meta in LANES.items():
        rows = by[key]
        if not rows or tier_of(key) != "headroom":
            continue
        a(f"### {meta['title']} — {meta['range']} ({len(rows)} plates)")
        a("")
        a(f"*{meta['act']}*")
        a("")
        for pid, lane, body, neg_add, line, ledg in rows:
            a(f"#### `{pid}.png` *(tier 2 · not declared)*")
            a("")
            a(f"**Lands on:** \"{line}\" · **ledger** {ledg}")
            a("")
            a(f"- `{pid}.png`")
            a(prompt_body(pid, lane, body, neg_add))
            a("")
            a(f"**Save as:** `{SAVE_DIR}\\{pid}.png`")
            a("")
            a(f"**`[NEG]` addition:** append `, {neg_add}` to the canonical `[NEG]`.")
            a("")

    a(f"## 6. TIER 3 — thumbnail plates, {len(thumbs)}, T001–T006, **never a cut**")
    a("")
    a("Two candidates for each of PACKAGING §2's three variants, so the owner has a real A/B "
      "inside each concept rather than one take per idea. **These are never placed in the film "
      "and are never declared in `mandatory_stills`** — a thumbnail is not a cut, and EP65 had to "
      "un-declare its thumbnail plates late for exactly this reason.")
    a("")
    a("They use **`[TSTYLE]`, not `[STYLE]`** (§2). The reason is measured: the canonical "
      "`[STYLE]` asks for low contrast and soft falloff, which is right for a film frame and is "
      "why EP65's four thumbnail candidates were all dull and had to be re-ordered. `[TSTYLE]` "
      "asks for one hard directional key, high contrast, bright exposure and a subject brighter "
      "than its background. **`[NEG]` is not deviated.**")
    a("")
    a("The builder (`scripts/build_ep62_65_thumbnails.py`, PACKAGING §2) lays a black scrim at "
      "alpha 120 over the top 66% and fits the headline into it, and the unscrimmed band at "
      "y 475–634 is what `thumb_subject_luma` measures. So each prompt asks for **the entire upper "
      "40% as one unbroken field** — nothing for a headline to collide with — and for **the bottom "
      "third to be the brightest part of the frame**.")
    a("")
    for key, meta in LANES.items():
        rows = by[key]
        if not rows or tier_of(key) != "thumb":
            continue
        for pid, lane, body, neg_add, line, ledg in rows:
            a(f"#### `{pid}.png` *(thumbnail · not declared · never a cut)*")
            a("")
            a(f"**Serves:** {line} · **ledger** {ledg}")
            a("")
            a(f"- `{pid}.png`")
            a(prompt_body(pid, lane, body, neg_add))
            a("")
            a(f"**Save as:** `{SAVE_DIR}\\{pid}.png`")
            a("")
            a(f"**`[NEG]` addition:** append `, {neg_add}` to the canonical `[NEG]`. "
              "**The canonical `[NEG]` is not deviated for thumbnails.**")
            a("")

    # 7 checks
    a("## 7. Checking this order")
    a("")
    a("```")
    a("py -3.11 scripts/check_image_order_neg.py --file "
      "episodes/_planning/EP67_ramirez_CODEX_BATCH_A.v002.md")
    a("py -3.11 scripts/check_design_doc.py --slug ramirez")
    a("py -3.11 scripts/check_episode_spec.py --slug ramirez")
    a("py -3.11 scripts/build_ep67_ramirez_image_order.py --verify")
    a("```")
    a("")
    a("The first proves the `[NEG]` carries all five token families (face/likeness, readable "
      "text, handwriting, marks of authority, numerals). The last re-derives this document and "
      "the paste files from the same source and reports prompt count, distinct save names, "
      "control characters, block lengths, banned-token counts and md↔paste body equality.")
    a("")
    a("Byte-identity of the `[NEG]` against batch D can be confirmed directly:")
    a("")
    a("```")
    a("py -3.11 -c \"import re;g=lambda p:max([l for l in open(p,encoding='utf-8')"
      ".read().splitlines() if l.lstrip().startswith('>') and re.search(r'\\btext\\b.*"
      "\\blettering\\b',l,re.I)],key=len).lstrip('> ').strip();"
      "d=g('episodes/_planning/EP66_openfields_CODEX_BATCH_D.v001.md');"
      "r=g('episodes/_planning/EP67_ramirez_CODEX_BATCH_A.v002.md');"
      "print('NEG identical:',d==r,len(d),len(r))\"")
    a("```")
    a("")
    a("*Generated 2026-08-11 from `scripts/build_ep67_ramirez_image_order.py`. "
      "Do not hand-edit this file — edit the generator and re-run it, or the paste files drift.*")
    a("")
    return "\n".join(L)


# ---------------------------------------------------------------------------------------------
PASTE_COMMON = [
    "以下を1枚ずつ生成してください。**1プロンプト＝1枚**です。",
    "複数のプロンプトをまとめて1枚にしないでください。同じプロンプトで2枚目を作らないでください。",
    "",
    "──────── 全プロンプト共通の指定 ────────",
    "",
    "各プロンプト末尾の [STYLE] は、次の文言に置き換えてください:",
    "",
    STYLE,
    "",
    "各プロンプト末尾の Avoid: [NEG] は、次の文言に置き換えてください:",
    "",
    NEG,
    "",
    "★[NEG] の後ろに「, ○○, ○○」と語が続いています（全プロンプト）。",
    "　その場合は、上の文言をすべて展開したうえで、その末尾にその語をそのまま足してください。",
    "　上の文言からは1語も削らないでください。",
    "",
    "──────── 絶対条件 ────────",
    "",
    "・**人物は積極的に入れてよい。顔も描いてよい。**（オーナー決定 2026-07-04）",
    "・ただし実在する特定の人物に似せない。有名人・公人・実在の誰かの肖像は不可",
    "・読める文字・数字・手書き・署名・印章・記章・ロゴを一切描かない",
    "・書類は「読めない灰色の横棒の並び」または「完全な白紙」として描く（本文に指定あり）",
    "・車体のバッジ・文字マーク・ネームプレート・グリルの楕円・ナンバープレートも描かない",
    "・実在ブランドを出さない。車は「中型セダン」、販売店は「販売店」でよい",
    "・画面（モニタ・スマホ・PC）は絶対に読めないこと。背面か、ピンぼけか、一様な光",
    "・警察・制服・記章・銃器・血液・法廷内部・天秤・砂時計・握手・子どもを描かない",
    "・手は指が数えられること。融合した指・6本指・親指の欠落・組んだ指は不可。",
    "　**手が主役のときは必ず「平らな面に伏せて置いた手」**（EP66 L236 の失敗と、通った修正）",
    "・舞台は**カリフォルニア州ダブリン**。アイルランドのダブリンではない。欧州の街並みにしない",
    "・写真として撮られたもののように。イラスト、CG、絵画調にしない",
    "",
]


def paste_common(tier: str) -> list[str]:
    """The shared preamble. Thumbnails swap [STYLE] for [TSTYLE]; [NEG] never changes."""
    out = list(PASTE_COMMON)
    if tier == "thumb":
        i = out.index("各プロンプト末尾の [STYLE] は、次の文言に置き換えてください:")
        out[i] = "各プロンプト末尾の [TSTYLE] は、次の文言に置き換えてください:"
        out[i + 2] = THUMB_STYLE
        out.insert(i + 3, "")
        out.insert(i + 4, "★この6枚は**サムネイル専用**です。本編カットの [STYLE]（低コントラスト）は使いません。")
        out.insert(i + 5, "　硬い一灯・高コントラスト・明るい露出。**画面の上40%は何も無い一様な面**にしてください。")
        out.insert(i + 6, "　見出し文字を焼き込む場所です。被写体は下60%に収め、下1/3を一番明るくします。")
    return out


def build_paste() -> dict[str, str]:
    by = plates_by_lane()
    files: dict[str, str] = {}

    groups: list[tuple[str, str, list]] = []
    for key, meta in LANES.items():
        rows = by[key]
        if not rows:
            continue
        for part in chunks(rows, meta["chunk"]):
            groups.append((key, meta["title"], part))

    dec_groups = [g for g in groups if tier_of(g[0]) == "declared"]
    hd_groups = [g for g in groups if tier_of(g[0]) == "headroom"]
    th_groups = [g for g in groups if tier_of(g[0]) == "thumb"]

    def render(fname: str, idx: int, total: int, key: str, title: str, rows: list,
               tier: str) -> None:
        L: list[str] = []
        a = L.append
        tag = {"declared": "バッチ", "headroom": "予備バッチ",
               "thumb": "**サムネイル**バッチ"}[tier]
        a(f"EP67 ramirez — 画像発注 {tag} {idx}/{total}（{len(rows)}枚）")
        a(f"区分: {title}  [{rows[0][0]} – {rows[-1][0]}]")
        a("")
        if tier == "headroom":
            a("★これは**予備**です。**生成してください。**本編の契約（mandatory_stills）には入って")
            a("　いませんが、却下が出たときの差し替えと、ナレーションが伸びた場合の不足に備えます。")
        elif tier == "thumb":
            a("★これは**サムネイル用**です。**動画のカットには一切使いません。**")
            a("　この6枚だけ [STYLE] ではなく **[TSTYLE]** を使います（下記）。**[NEG] は変えません。**")
        else:
            a("★これは新規発注です。同名の既存ファイルはありません。")
        a("　新しい ID を作らない。`_v2` / `_02` / `_A` を作らない。**名前は上の■のとおりちょうど。**")
        a("")
        L += paste_common(tier)
        if key == "C":
            a("──────── この区分だけの追加指定（人物レーン）────────")
            a("")
            a("各プロンプトの先頭 [HSTYLE] は、次の文言に置き換えてください:")
            a("")
            a(HSTYLE)
            a("")
            a("・この24枚のうち9枚は**顔がはっきり写ります。それが狙いです。**")
            a("　ただし全員**架空の他人**です。実在の誰かに似せないでください。")
            a("・カメラ目線にしない。作り笑いをしない。広告のモデル顔にしない。")
            a("")
        a("──────── プロンプト ────────")
        a("")
        for pid, lane, body, neg_add, line, ledg in rows:
            a(f"■ {pid}.png")
            a(prompt_body(pid, lane, body, neg_add))
            a("")
        a("──────── 保存 ────────")
        a("")
        a("生成した画像は上の ■ の名前（例: " + rows[0][0] + ".png）で保存してください。")
        a(f"保存先 {SAVE_DIR}\\")
        a("長辺 3840px 以上・16:9・PNG。")
        files[fname] = "\n".join(L) + "\n"

    for i, (key, title, rows) in enumerate(dec_groups, 1):
        render(f"batch_{i:02d}.txt", i, len(dec_groups), key, title, rows, "declared")
    for i, (key, title, rows) in enumerate(hd_groups, 1):
        render(f"headroom_{i:02d}.txt", i, len(hd_groups), key, title, rows, "headroom")
    for i, (key, title, rows) in enumerate(th_groups, 1):
        render(f"thumbs_{i:02d}.txt", i, len(th_groups), key, title, rows, "thumb")
    return files


# ---------------------------------------------------------------------------------------------
BANNED_IN_NEG = ("human face", "facial features", "eyes")
REQUIRED_IN_NEG = ("recognisable person", "identifiable person", "likeness of a real individual",
                   "portrait of a named person", "celebrity", "public figure", "deepfake")


def verify(md: str, files: dict[str, str]) -> int:
    bad = 0
    print("=" * 92)
    print("MEASURED VERIFICATION")
    print("=" * 92)

    ids = [r[0] for r in P]
    dec = [r[0] for r in P if tier_of(r[1]) == "declared"]
    hd = [r[0] for r in P if tier_of(r[1]) == "headroom"]
    th = [r[0] for r in P if tier_of(r[1]) == "thumb"]
    rids = [i for i in ids if i.startswith("R")]
    print(f"prompts total                 {len(P)}")
    print(f"  tier 1 declared             {len(dec)}  ({dec[0]}..{dec[-1]})")
    print(f"  tier 2 headroom             {len(hd)}  ({hd[0]}..{hd[-1]})")
    print(f"  tier 3 thumbnail            {len(th)}  ({th[0]}..{th[-1]})")
    print(f"distinct plate ids            {len(set(ids))}")
    print(f"R ids contiguous R001..R{len(rids):03d} "
          f"{rids == [f'R{i:03d}' for i in range(1, len(rids) + 1)]}")
    print(f"T ids contiguous T001..T{len(th):03d} "
          f"{th == [f'T{i:03d}' for i in range(1, len(th) + 1)]}")
    if len(set(ids)) != len(ids):
        print("  FAIL duplicate id"); bad += 1

    # distinct save names
    saves = [f"{i}.png" for i in ids]
    print(f"distinct save names           {len(set(saves))}")
    if len(set(saves)) != len(P):
        print("  FAIL save-name collision"); bad += 1

    # per lane
    print("\nper-lane plate counts")
    by = plates_by_lane()
    for k, meta in LANES.items():
        print(f"  {k:2s} {meta['title'][:46]:48s} {len(by[k]):3d}   {meta['range']}")

    # style / neg
    print(f"\n[STYLE] length               {len(STYLE)} chars")
    print(f"[TSTYLE] length              {len(THUMB_STYLE)} chars")
    print(f"[NEG]   length               {len(NEG)} chars")
    print(f"[HSTYLE] length              {len(HSTYLE)} chars")
    dneg = read_canonical_neg()
    print(f"[NEG] byte-identical to EP66 batch D: {NEG == dneg} "
          f"(sha of both: {hash(NEG) == hash(dneg)})")
    if NEG != dneg:
        print("  FAIL NEG drifted"); bad += 1
    for t in REQUIRED_IN_NEG:
        ok = t in NEG
        print(f"  required token {t!r:38s} {'present' if ok else 'MISSING'}")
        if not ok:
            bad += 1
    for t in BANNED_IN_NEG:
        n = NEG.lower().count(t)
        print(f"  banned  token {t!r:39s} count {n}")
        if n:
            print("  FAIL banned token present"); bad += 1

    # control characters
    print("\ncontrol characters")
    corpus = {"<md>": md, **files}
    total_ctrl = 0
    for name, text in corpus.items():
        ctrl = [(i, ch) for i, ch in enumerate(text)
                if unicodedata.category(ch) == "Cc" and ch != "\n"]
        total_ctrl += len(ctrl)
        if ctrl:
            print(f"  {name}: {len(ctrl)} -> {ctrl[:5]}")
            bad += 1
    print(f"  total non-newline control chars across md + {len(files)} paste files: {total_ctrl}")

    # md <-> paste body equality
    print("\nmd <-> paste prompt-body equality")
    joined = "\n".join(files.values())
    miss_md = miss_paste = 0
    for pid, lane, body, neg_add, line, ledg in P:
        b = prompt_body(pid, lane, body, neg_add)
        if b not in md:
            miss_md += 1
            print(f"  {pid}: body NOT in md")
        if b not in joined:
            miss_paste += 1
            print(f"  {pid}: body NOT in paste files")
    print(f"  bodies present in md            {len(P) - miss_md}/{len(P)}")
    print(f"  bodies present in paste files   {len(P) - miss_paste}/{len(P)}")
    bad += miss_md + miss_paste

    # each prompt well formed
    print("\nprompt shape")
    n_style = sum(1 for r in P
                  if prompt_body(r[0], r[1], r[2], r[3]).count(" [STYLE] Avoid: [NEG],") == 1)
    n_t = sum(1 for r in P
              if prompt_body(r[0], r[1], r[2], r[3]).count(" [TSTYLE] Avoid: [NEG],") == 1)
    n_h = sum(1 for r in P if prompt_body(r[0], r[1], r[2], r[3]).startswith("[HSTYLE] "))
    print(f"  exactly one ' [STYLE] Avoid: [NEG],'              {n_style} "
          f"(non-thumb = {len(P) - len(by['T'])})")
    print(f"  exactly one ' [TSTYLE] Avoid: [NEG],'             {n_t} "
          f"(lane T = {len(by['T'])})")
    print(f"  [HSTYLE] prefixed prompts                         {n_h} (lane C = {len(by['C'])})")
    if n_style != len(P) - len(by["T"]) or n_t != len(by["T"]) or n_h != len(by["C"]):
        bad += 1

    # every plate lands on a line that is really in the script
    print("\nscript-line citations")
    sp = _re.sub(r"\s+", " ", (ROOT / "episodes" / "_planning" /
                               "EP67_ramirez_script.en.v001.md").read_text(encoding="utf-8")
                 .replace("*", ""))
    nf = []
    for pid, lane, body, neg_add, line, ledg in P:
        if lane == "T":
            continue                        # thumbnails serve a PACKAGING variant, not a line
        for piece in [p.strip(" …") for p in _re.sub(r"\s+", " ", line).split(" … ")]:
            if piece and piece not in sp:
                nf.append((pid, piece[:70]))
    print(f"  non-thumbnail plates                              {len(P) - len(by['T'])}")
    print(f"  quoted fragments NOT found verbatim in the script {len(nf)} {nf[:5]}")
    print(f"  plates citing a ledger row                        "
          f"{sum(1 for r in P if r[5].strip())}/{len(P)}")
    if nf:
        bad += 1

    # hazards inside prompt bodies
    print("\nhazard scan over the prompt bodies")
    for word, label in (("nissan", "real brand"), ("transunion", "real brand"),
                        ("ofac letter", "forbidden document"), ("credit report", "forbidden doc"),
                        ("gavel", "forbidden subject"), ("courtroom", "forbidden subject"),
                        ("scales of justice", "forbidden subject"), ("handshake", "generic symbol"),
                        ("hourglass", "generic symbol"), ("child", "forbidden subject")):
        hits = [r[0] for r in P
                if word in prompt_body(r[0], r[1], r[2], r[3]).split(" Avoid: ")[0].lower()]
        print(f"  {label:20s} {word!r:20s} in positive body: {len(hits)} {hits[:6]}")
        if hits:
            bad += 1

    # paste chunk sizes
    print("\npaste files")
    for name in sorted(files):
        n = files[name].count("\n■ ")
        print(f"  {name:16s} {n:2d} prompts  {len(files[name]):6d} bytes")

    print("\n" + ("VERIFY: FAIL" if bad else "VERIFY: all measured checks pass"))
    return 1 if bad else 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--verify", action="store_true", help="verify only, write nothing")
    a = ap.parse_args()
    md = build_md()
    files = build_paste()
    if not a.verify:
        OUT_MD.write_text(md, encoding="utf-8", newline="\n")
        OUT_PASTE.mkdir(parents=True, exist_ok=True)
        for name, text in files.items():
            (OUT_PASTE / name).write_text(text, encoding="utf-8", newline="\n")
        print(f"wrote {OUT_MD}")
        print(f"wrote {len(files)} paste files to {OUT_PASTE}")
    return verify(md, files)


if __name__ == "__main__":
    raise SystemExit(main())
