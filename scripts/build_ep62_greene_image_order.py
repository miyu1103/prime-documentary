#!/usr/bin/env python3
"""Emit EP62 greene's batch-B Codex image order (.md), its paste chunks and ONE merged paste
file, all from a single PLATES list so the bodies cannot drift.

WHY THIS ORDER EXISTS. check_spec_satisfied.py refuses to let greene render:

    distinct_video_assets: 196 distinct footage+motion source(s) across 272 video cut(s),
    against a declared 234 -- 38 short

The staged pool is 73 accepted archive clips + 123 i2v motion clips. Three staging waves have
failed to close the gap from the shelf (the last measured 1,740 unstaged candidates whose top
hits were foreign flags, ink-in-water, bridges and birds), and the shelf cannot supply a 1975
Louisville public housing project at all. A generated plate driven to i2v is period-correct by
construction, which is the failure that has bitten this episode three times: a modern US
election ballot, a 2011 Range Rover Evoque on an EU plate and another production's legible
shot-list cards all shipped in the delivered master and are now blocklisted.

HOW THE PLATE COUNT WAS DERIVED -- see section 1 of the emitted document for the full workings.
The short form: the gap is NOT 234 - 196. Feeding N new plates into build_case_film_generic
changes the factory/motion split, so the answer comes from solve_totals, not subtraction.
At _CAP_FACTORY = 1 (what check_asset_reuse exports today) the smallest N that reaches 234 is
67; this order carries 70, the extra three being attrition margin against a plate that cannot
be driven to motion.

    py -3.11 scripts/build_ep62_greene_image_order.py            # write + verify
    py -3.11 scripts/build_ep62_greene_image_order.py --verify   # verify only, write nothing

The canonical [NEG] is READ OUT OF EP66's batch D at generation time using the *checker's own*
neg_block(), never retyped, so the order and check_image_order_neg.py cannot disagree about
which line is canonical. The generator refuses to write if that read fails, if an identifiability
token is missing, or if any of the three tokens that caused EP66's 191-plate rebuild
(`human face`, `facial features`, `eyes`) have come back.
"""
from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:  # pragma: no cover
    pass

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_image_order_neg import neg_block  # the checker's own definition of "canonical [NEG]"

ROOT = Path(__file__).resolve().parents[1]
PLANNING = ROOT / "episodes" / "_planning"
BATCH_D = PLANNING / "EP66_openfields_CODEX_BATCH_D.v001.md"
GREENE_A = PLANNING / "EP62_greene_CODEX_BATCH_A.v002.md"
OUT_MD = PLANNING / "EP62_greene_CODEX_BATCH_B.v001.md"
OUT_PASTE = PLANNING / "EP62_greene_CODEX_PASTE_B"
OUT_ALL = PLANNING / "EP62_greene_CODEX_PASTE_ALL.txt"
SAVE_DIR = r"H:\pd-media\assets\ai\greene"
STORE = Path(r"H:/pd-media/assets/ai/greene")
CHUNK = 7

# ---------------------------------------------------------------------------------------------
# canonical blocks -- both LIFTED, neither retyped
# ---------------------------------------------------------------------------------------------


def read_canonical_neg() -> str:
    """Batch D's [NEG], found the same way check_image_order_neg.py finds it."""
    line = neg_block(BATCH_D.read_text(encoding="utf-8"))
    if not line:
        raise SystemExit(f"no canonical [NEG] blockquote found in {BATCH_D.name}")
    return line.lstrip("> ").strip()


def read_greene_style() -> str:
    """greene's own [STYLE], lifted from batch A v002.

    NOT batch D's: that one says 'late Appalachian autumn, rural Pennsylvania and Middle
    Tennessee', which is the wrong weather and the wrong State for a Louisville film. Only the
    [NEG] is required to be byte-identical to batch D. Using greene's own [STYLE] is also what
    keeps these 70 plates looking like the 242 already on the shelf.
    """
    for line in GREENE_A.read_text(encoding="utf-8").splitlines():
        s = line.lstrip("> ").strip()
        if s.startswith(", cinematic still") and "Ohio Valley" in s:
            return s.lstrip(", ").strip()
    raise SystemExit(f"no canonical [STYLE] blockquote found in {GREENE_A.name}")


NEG = read_canonical_neg()
STYLE = read_greene_style()

# ---------------------------------------------------------------------------------------------
# reusable clauses. Written once so 70 plates cannot say them 70 slightly different ways.
# ---------------------------------------------------------------------------------------------

# THE POSITIVE ORDERING FOR PAPER. This episode's central object is a court summons taped to a
# door: a generator asked for one WILL write on it. Batch C proved a [NEG] ban alone does not
# hold -- L146's wordmark came back twice after being banned twice. So the shape is ASKED FOR
# here, in the positive, and the [NEG] only backs it up.
PAPER_GREY = (
    "The paper reads as a printed page and yet carries nothing readable: EVENLY SPACED FLAT GREY "
    "HORIZONTAL BARS of one uniform width and one uniform weight lie across it in parallel, each "
    "bar a solid unbroken block of soft grey with straight ends, no letter shapes, no word shapes "
    "and no gaps between words anywhere along it, so it is recognisable as a printed page purely "
    "by its rhythm of grey and white and carries not one readable character"
)
PAPER_BLANK = (
    "The paper is completely bare: an unbroken field of off-white with no print, no ruling, no "
    "letterform, no number and no mark of any kind anywhere on it"
)
# EP66 L236 failed three times on a hand raised into the air and passed the moment the hand was
# put flat on a surface (L247's geometry). Every hand in this order uses that geometry.
FLAT_HAND = (
    "THE HAND IS AT REST FLAT ON THE SURFACE, not raised and not held in the air, the palm laid "
    "down in full contact with it and the wrist straight, THE FOUR FINGERS LYING SIDE BY SIDE AND "
    "SEPARATE with a line of shadow between each pair and one nail showing on each, and the thumb "
    "clearly apart from the fingers along the near side"
)
ERA = (
    "Everything in the frame belongs to Louisville, Kentucky in the United States between 1975 and "
    "1982 -- painted timber and pressed-steel doors, chipped poured concrete, dark red brick, "
    "formica, enamel, net curtain and worn paint -- and nothing made after 1982 appears anywhere "
    "in the picture"
)
# These plates are i2v SOURCES. A dead-still composition makes a dead i2v clip, and near-still
# motion clips are what animation_density fails on -- EP65 lost three rebuilds to exactly that.
# Every body below names one thing that is already mid-movement when the shutter opens.
MOVE = "MOVING ELEMENT, already mid-movement when the shutter opens:"

# common per-plate [NEG] additions
N_ERA = ("modern car, modern van, modern smartphone, computer screen, television screen, "
         "trainers, sneakers, e-scooter, plastic wheelie bin, uPVC window, EU number plate, "
         "non-Latin script, LED lighting, composite decking, modern kitchen")
N_EVICT = ("furniture on a pavement, people being evicted, a removal van being loaded, crying, "
           "a hand on a shoulder, a uniformed officer at a door, a landlord character")
N_PAPER = ("readable document, printed words on paper, letterforms, typed lines, printed "
           "paragraph, letterhead, form fields, rubber stamp with words, handwritten note")
N_HAND = ("fingers fused into one mass, fingers merged, webbed fingers, mitten hand, stub "
          "fingers, missing thumb, extra fingers, six fingers, malformed hand, raised hand, "
          "hand held up in the air, blurred hand")
N_DEAD = ("a completely static arrangement with nothing caught mid-movement, everything locked "
          "and settled, studio-locked still life")
N_FACE_ON_MONEY = "portrait on a banknote, engraved head on currency, engraved head on a stamp"


def base_neg(*extra: str) -> str:
    """Every plate's [NEG] addition: the greene-specific bans batch D's canonical list does not
    carry, then whatever this plate needs. The canonical list itself is never shortened."""
    return ", ".join([N_ERA, N_EVICT, N_DEAD, *[e for e in extra if e]])


# ---------------------------------------------------------------------------------------------
# THE PLATES.  (id, act, body, neg_add, script_line)
#
# `act` is the section the builder will place the plate in. That is NOT a wish: the motion pool
# is consumed in sorted order and each section takes the next per_m[section] items off one queue,
# so the id decides the section. At today's pool sizes G243-G267 land in ACT_4 and G268-G312 in
# ACT_5. See section 2 of the emitted document.
# ---------------------------------------------------------------------------------------------
P: list[tuple[str, str, str, str, str]] = [

    # ------------------------------------------------------------------ ACT_4  (G243-G267)
    ("G243", "ACT_4",
     "A shut painted door at the far end of a narrow public corridor, photographed from twelve "
     "paces at chest height, the only light a high dirty window halfway down the corridor that "
     "lays one pale panel across the floor and leaves the door itself in flat shadow, nobody in "
     f"the corridor. {ERA}. {MOVE} the loose rubber draught strip along the bottom of the door is "
     "lifted clear of the floor and curling, and a bare bulb on a flex hangs well out "
     "of vertical so the shadows of the door frame are sliding across the wall",
     base_neg("bright cheerful corridor, hotel corridor, hospital corridor, office suite"),
     "There was no door left to knock on."),

    ("G244", "ACT_4",
     "A shallow wire tray of plain unmarked buff folders standing on a public counter, "
     "photographed from counter height at half a metre with the counter running out of frame to "
     f"both sides, flat window light from the left. {PAPER_BLANK}. {ERA}. {MOVE} the cover of the "
     "topmost folder stands half open and is rocking back on itself, its loose leaves fanned and "
     "out of line, driven by a desk fan whose blades are turning in the soft background",
     base_neg(N_PAPER),
     "So they went to federal court, filing a class action ... under section 1983."),

    ("G245", "ACT_4",
     "An open-air concrete walkway of identical painted doors along the first floor of a low-rise "
     "dark red brick block, photographed from the walkway itself at a low three-quarter angle at "
     "hip height so the doors and the balustrade both run away to a point, flat overcast midday "
     f"light, nobody on it. {ERA}. {MOVE} the net curtains at three separate windows are all "
     "belling outward through their open sashes at once in the same gust, and the balustrade's "
     "loose safety rope is swinging",
     base_neg("identical modern apartment block, glass balustrade, motel corridor, "
              "self-storage units, roller shutters"),
     "if posting was constitutionally inadequate on these doors, it was inadequate on every door"),

    ("G246", "ACT_4",
     "A thick bound volume lying open on a plain wooden table directly beneath a sash window that "
     "stands open four inches, photographed from the far side of the table at tabletop level at "
     f"one metre in cold flat daylight. {PAPER_GREY}. {ERA}. {MOVE} the loose upper pages have "
     "stood up off the block and are turning over one at a time in the draught, three of them in "
     "the air at once and out of line with each other",
     base_neg(N_PAPER),
     "It came from that 1950 case, Mullane, and it was already thirty-two years old."),

    ("G247", "ACT_4",
     "A plain wooden chair pushed back hard from a bare table in an otherwise empty room, "
     "photographed from the open doorway at eight paces at standing height, one window on the far "
     f"wall throwing a single slanted shaft across the floorboards. {ERA}. {MOVE} the chair is up "
     "on its two back legs and tilting, not yet settled, and the dust in the shaft of light is "
     "turning in a slow column",
     base_neg("dining room, restaurant, staged interior"),
     "They lost."),

    ("G248", "ACT_4",
     "A manual typewriter of the period on a plain desk with a single sheet rolled into the "
     "platen, photographed from the side at forty centimetres so the sheet stands up against a "
     f"bright window that is out of focus behind it. {PAPER_GREY}. {ERA}. {MOVE} the free upper "
     "edge of the sheet is curled forward and trembling, and a thin curtain at the window behind "
     "is travelling across the light",
     base_neg(N_PAPER, "electric typewriter, modern keyboard"),
     "the District Court granted judgment for the sheriff and his deputies, in an unreported "
     "opinion"),

    ("G249", "ACT_4",
     "A run of old worn leather ledger spines packed on a low shelf, photographed square on at "
     "half a metre in a hard slant of window light that rakes across their ribs and leaves the "
     f"shelf below them dark. {PAPER_BLANK}. {ERA}. {MOVE} dust is lifting off the shelf edge in "
     "the slant of light and travelling to the right, and one ledger stands proud of the row and "
     "is tilting out of it",
     base_neg(N_PAPER, "gilt titles, spine labels, library classification"),
     "a case called Weber, decided by the Sixth Circuit some seventy years earlier"),

    ("G250", "ACT_4",
     "One heavy bound volume balanced on the edge of a plain table with three quarters of its "
     "length overhanging the drop, photographed from table height at sixty centimetres so the "
     f"overhang runs at the camera, one hard light raking from the left. {PAPER_GREY}. {ERA}. "
     f"{MOVE} the volume is tipping: its far end is already lifted clear of the wood and its "
     "loose pages have begun to slide out of square",
     base_neg(N_PAPER),
     "That was 1909. The presumption was doing all the work."),

    ("G251", "ACT_4",
     "A wide crack running right across a poured concrete walkway slab, photographed from ankle "
     "height at close range so the crack opens toward the camera and the walkway runs away out of "
     f"focus behind it, flat grey daylight. {ERA}. {MOVE} the dry grass growing out of the crack "
     "is bent flat along the concrete in a gust and grit is skittering across the slab in the "
     "same direction",
     base_neg("earthquake damage, disaster scene, rubble"),
     "It acknowledged that conditions had changed since Weber."),

    ("G252", "ACT_4",
     "A reel-to-reel tape deck of the period standing on a plain table, photographed at a steep "
     "three-quarter from above at seventy centimetres with the take-up reel half full, one warm "
     f"desk lamp low to the left and the rest of the room dark but never black. {ERA}. {MOVE} both "
     "reels are turning and the slack loop of tape between them is swinging out of plane",
     base_neg("recording studio, mixing desk, modern audio equipment"),
     "there was undisputed testimony in this case"),

    ("G253", "ACT_4",
     "A sheet on a painted apartment door whose lower two thirds have already been torn away, the "
     "ragged edge standing out from the paint, photographed at thirty centimetres from just below "
     "the tear so the flat light off the walkway comes past it and lights the torn fibres. "
     f"{PAPER_GREY} -- and the grey bars stop where the tear runs. {ERA}. {MOVE} the whole ragged "
     "edge is lifting and rippling away from the door and one strip of it has folded right back",
     base_neg(N_PAPER),
     "notices posted on the apartment doors of tenants are often removed by other tenants"),

    ("G254", "ACT_4",
     "Chalk marks left low on the concrete at the foot of a painted apartment door, drawn at the "
     "height of somebody very small, with a scrap of pale paper caught against the kick plate, "
     "photographed from knee height at one metre in flat overcast light, nobody in the frame. "
     f"{PAPER_BLANK}. {ERA}. {MOVE} the scrap is up on its edge and mid-skitter, about to blow "
     "clear of the door, and chalk dust is drifting off the concrete with it",
     base_neg(N_PAPER, "a child in frame, a face, a toy, playground equipment"),
     "the depositions in the footnote had said children"),

    ("G255", "ACT_4",
     "The flat of one adult hand pressed against a painted apartment door high above the handle, "
     "holding a sheet flat to the paint, photographed from the side at forty-five centimetres at "
     "that same height, the arm cropped at the elbow and no other part of the person in the frame, "
     f"flat walkway light. {FLAT_HAND} -- here the surface is the door itself and the paper under "
     f"the palm. {PAPER_GREY}. {ERA}. {MOVE} the free lower edge of the sheet has lifted right "
     "away from the door in the draught and is standing out from the paint",
     base_neg(N_PAPER, N_HAND, "uniform sleeve, epaulette, cuff braid"),
     "we always put them up high"),

    ("G256", "ACT_4",
     "Seen from the open walkway below and behind, one arm reaching up into the top of the frame "
     "toward a door, cropped at the shoulder with no other part of the person visible and no face "
     "anywhere in the picture, the concrete soffit and the underside of the walkway filling the "
     f"upper corner, photographed at two metres in flat grey light. {PAPER_BLANK}. {ERA}. "
     f"{MOVE} the coat sleeve "
     "is out of line with the arm and still swinging, and a pale corner of paper at the top edge "
     "of the frame is lifting",
     base_neg(N_HAND, "uniform sleeve, epaulette, cuff braid, full figure in frame"),
     "posting only comes into play after the officer directed to serve notice cannot find the "
     "defendant on the premises"),

    ("G257", "ACT_4",
     "A concrete doorstep carrying one single fresh shoe print in wet dust and no second print "
     "anywhere on it, photographed obliquely from one metre at knee height so the step runs across "
     f"the frame, flat wet daylight. {ERA}. {MOVE} rainwater is running off the lip of the step in "
     "a thin unbroken thread and the dust at the edge of the print is being carried away with it",
     base_neg("footprint in snow, crime scene, forensic marker"),
     "So how can a step that happens on the first visit be a last resort?"),

    ("G258", "ACT_4",
     "A heavy timber door of a plain public building swinging inward, the widening wedge of "
     "daylight sweeping across a worn stone floor, photographed from inside at four paces at waist "
     f"height with the room beyond dark but holding its detail. {ERA}. {MOVE} the door is mid-swing "
     "with its leading edge smeared, and the wedge of light on the floor is travelling with it",
     base_neg("courthouse portico, carved motto, memorial plaque, church interior"),
     "The Sixth Circuit reversed, and overruled Weber to do it."),

    ("G259", "ACT_4",
     "A pendulum wall clock in a plain hallway seen from below and well to one side so the dial is "
     "turned away from the camera and only the case, the glass door and the swinging pendulum are "
     "in view, photographed at two paces at chest height in cold daylight from a window out of "
     f"frame. {ERA}. {MOVE} the pendulum is at the far end of its travel and its bob has smeared, "
     "and the bob's shadow is running across the wall behind it",
     base_neg("clock face, dial in view, hands of a clock, hourglass, stopwatch"),
     "There may have been a time ... That time has passed."),

    ("G260", "ACT_4",
     "A plain unmarked folder being slid back across a wooden public counter toward the camera by "
     "one flat hand, photographed at counter height at half a metre, the hand cropped at the wrist. "
     f"{FLAT_HAND} -- here the surface is the folder. {PAPER_GREY} on the loose leaves that have "
     f"come out of it. {ERA}. {MOVE} the folder is mid-slide with its trailing edge lifted off the "
     "counter and two of its leaves fanning out behind it",
     base_neg(N_PAPER, N_HAND),
     "It reversed the grant of summary judgment and remanded the case for further proceedings."),

    ("G261", "ACT_4",
     "A small brass postal balance on a wooden counter with one plain envelope lying in its pan, "
     "photographed at pan height at thirty centimetres with the dial turned away from the camera "
     f"so only the back of its case shows, one soft window light from the left. {PAPER_BLANK}. "
     f"{ERA}. {MOVE} the pan has not settled: it is still swinging below its rest and the envelope "
     "on it has slid to one side",
     base_neg(N_PAPER, "dial in view, gauge markings, kitchen scales, digital scales"),
     "Requiring Kentucky to provide notice by mail ... will not be overly burdensome."),

    ("G262", "ACT_4",
     "A rubber stamp lifted clear of an open ink pad with wet ink glistening on its face, the "
     "face itself an even bare rubber pad with nothing cut into it, photographed from the side at "
     f"twenty centimetres against a dark wooden counter under one hard low light. {ERA}. {MOVE} the "
     "stamp is mid-lift and a thread of ink is drawing away from the pad and breaking",
     base_neg(N_PAPER, "cut lettering on the stamp face, date stamp, official seal, monogram"),
     "a copy of the petition must be sent by registered or certified mail within a day"),

    ("G263", "ACT_4",
     "A sheet of small perforated paper squares lying on a wooden counter with one corner lifted, "
     "each square an even field of one flat faded colour with nothing figured on it at all, "
     "photographed at thirty centimetres at a low oblique so the perforations catch the raking "
     f"light. {ERA}. {MOVE} the lifted corner is rippling in the draught from an open door and the "
     "whole sheet has begun to slide on the polished counter",
     base_neg(N_PAPER, N_FACE_ON_MONEY, "denomination, printed value, stamp design, portrait"),
     "The remedy was a stamp, and another State was already buying them."),

    ("G264", "ACT_4",
     "The wet stone steps of a plain public building seen from the bottom at a steep upward angle "
     "in heavy rain, nobody on them, photographed at one metre in flat grey light with the treads "
     f"running up out of the top of the frame. {ERA}. {MOVE} the rain is bouncing off the treads in "
     "a fine broken veil and a film of water is running down over the nosing of each step",
     base_neg("courthouse portico, columns, carved motto, statue, flag"),
     "The Supreme Court took the appeal in 1981."),

    ("G265", "ACT_4",
     "A tall window in the bare lobby of a plain public building seen from inside at six paces at "
     "chest height, low February daylight coming through it and lying in one long panel on the "
     f"stone floor, nobody in the lobby. {ERA}. {MOVE} rain is running down the outside of the "
     "glass in moving threads and the panel of light on the floor is rippling with them",
     base_neg("courtroom, judge's bench, gallery seating, stained glass, church"),
     "It heard argument on the twenty-third of February 1982."),

    ("G266", "ACT_4",
     "Four heavy overcoats hung on a row of pegs in a cold public cloakroom, photographed square "
     f"on at three paces at chest height in flat light from a high window. {ERA}. {MOVE} the two "
     "nearest coats are still swinging on their pegs with their hems well out of vertical and one "
     "empty peg is turning",
     base_neg("uniform coat, braid, epaulette, hat with a badge, school cloakroom"),
     "Two lawyers argued it. Two more filed briefs as friends of the court."),

    ("G267", "ACT_4",
     "One flat hand laid on a wooden shop counter beside a small brass cash drawer that stands "
     "half open on its runners, the compartments holding worn coins seen edge on, photographed at "
     f"counter height at thirty centimetres, the hand cropped at the wrist. {FLAT_HAND} -- here the "
     f"surface is the counter. {ERA}. {MOVE} the drawer is still travelling out on its runners and "
     "the coins in the near compartment are sliding back against its rim",
     base_neg(N_HAND, N_FACE_ON_MONEY, "banknotes face up, currency portrait, cash register display"),
     "Money got a person served. The apartment did not."),

    # ------------------------------------------------------------------ ACT_5  (G268-G312)
    ("G268", "ACT_5",
     "One bound volume standing open on a plain reading stand, photographed edge on at eye height "
     "at eighty centimetres so the block of pages fans toward the camera, a single high window "
     f"light behind and above it. {PAPER_GREY}. {ERA}. {MOVE} the fanned pages are riffling from "
     "one side to the other and four of them are lifted clear of the block at once",
     base_neg(N_PAPER, "lectern in a church, bible, illuminated manuscript"),
     "The opinion was delivered by Justice Brennan."),

    ("G269", "ACT_5",
     "A folding wooden rule lying half unfolded on a concrete step, its faces worn smooth and bare "
     "of any marking at all, photographed at thirty centimetres at step level in flat grey "
     f"daylight. {ERA}. {MOVE} one unfolded arm of the rule is still rocking on the concrete and "
     "has not come to rest",
     base_neg("measurement markings, graduations, tape measure, ruler with numbers"),
     "notice reasonably calculated, under all the circumstances"),

    ("G270", "ACT_5",
     "One lit kitchen window in a low-rise dark red brick block seen from the communal grass at "
     "thirty paces at the blue end of dusk with no sun anywhere in the sky, the room behind the "
     f"net curtain warm and the brick around it cold. {ERA}. {MOVE} the net curtain is travelling "
     "across the lit window and the long grass in the foreground is being laid flat in the same "
     "gust",
     base_neg("golden window glow, cosy interior, Christmas lights, postcard dusk, city skyline"),
     "deprived of a significant interest in property — indeed, of the right to continued "
     "residence in their homes"),

    ("G271", "ACT_5",
     "An invented woman in her thirties in a plain 1970s coat standing at her own painted "
     "apartment door in three-quarter view, photographed from three paces at eye height, her face "
     "lit evenly by flat cloud with no expression put on for the camera and not looking at the "
     f"lens, one open hand laid flat against the paint beside the door frame. {FLAT_HAND} -- here "
     f"the surface is the door. {ERA}. {MOVE} the door has swung four inches off its latch and "
     "the strip of dark interior beside her is widening",
     base_neg(N_HAND, "posed model, advertising smile, eye contact with the lens, glamour lighting"),
     "The sufficiency of notice must be tested with reference to its ability to inform people"),

    ("G272", "ACT_5",
     "An invented woman in her forties in a plain housecoat working along a communal washing line "
     "strung between two brick blocks, seen in three-quarter from four paces at chest height, her "
     "face lit evenly by flat cloud with no expression put on for the camera and not looking at "
     f"the lens, one open hand laid flat along the linen she is straightening. {ERA}. {MOVE} the "
     "worn linen on the line is full of wind and lifting together, and the line itself is "
     "bowing",
     base_neg(N_HAND, "posed model, advertising smile, eye contact with the lens, sunlit meadow"),
     "its practical application to the affairs of men as they are ordinarily conducted"),

    ("G273", "ACT_5",
     "A chain and padlock threaded through the bars of a yard gate, photographed at twenty "
     f"centimetres in cold flat light with the yard behind it out of focus. {ERA}. {MOVE} the loose "
     "end of the chain is swinging against the metal and the gate leaf itself is rocking on its "
     "hinge",
     base_neg("prison gate, razor wire, security fence, padlock with a brand"),
     "he usually arranges means to learn of any direct attack upon his possessory or proprietary rights"),

    ("G274", "ACT_5",
     "A plain front gate standing open onto a gravel drive, photographed from the house side at "
     f"ten paces at chest height in flat overcast light with nobody in the frame. {ERA}. {MOVE} the "
     "gate is mid-swing with its far edge smeared, and dust lifted off the gravel is travelling "
     "across the drive",
     base_neg("suburban mansion, ornamental garden, wrought iron crest, gated community"),
     "Entry upon real estate in the name of law may reasonably be expected to come promptly to "
     "the owner's attention."),

    ("G275", "ACT_5",
     "A sheet taped flat against the glass panel of a communal stair door, photographed from "
     "inside the stairwell at one metre so the sheet is back-lit by the daylight outside and its "
     f"fibres and the tape's shadow show through it. {PAPER_BLANK}. {ERA}. {MOVE} the sheet is "
     "drum-tight against the glass and vibrating in the wind, and its bottom corner has come away "
     "from the tape",
     base_neg(N_PAPER, "shop window notice, poster, advertisement"),
     "the secure posting of a notice on the property of a person is likely to offer that property "
     "owner sufficient warning"),

    ("G276", "ACT_5",
     "A sheet in the air a foot clear of a painted apartment door, already off its tape and caught "
     "side on so it reads as a thin bright edge, the door and its two strips of tape soft behind "
     "it, photographed at one metre in flat overcast walkway light. The sheet is falling. "
     f"{PAPER_GREY}. {ERA}. {MOVE} the sheet is mid-fall with its trailing corner still turning "
     "over, and the free tape ends on the door are lifting",
     base_neg(N_PAPER, "confetti, flying papers everywhere, storm of paper"),
     "merely posting notice on an apartment door does not satisfy minimum standards of due "
     "process"),

    ("G277", "ACT_5",
     "A run of apartment doors down an open walkway at flat midday with pale scraps of torn paper "
     "lying along the concrete at their feet, photographed from one end at knee height so the "
     f"scraps run away into the distance. {PAPER_BLANK}. {ERA}. {MOVE} the nearest scraps are "
     "mid-skitter down the walkway, one of them up on its edge and turning over",
     base_neg(N_PAPER, "litter-strewn slum, refuse sacks, vandalism, graffiti"),
     "reliance on posting ... results in a failure to provide actual notice to the tenant "
     "concerned"),

    ("G278", "ACT_5",
     "A curled strip of adhesive tape that has let go at both ends, caught in the air just clear "
     "of the painted door it came off, photographed at fifteen centimetres in raking light so its "
     f"curl throws a shadow on the paint. {ERA}. {MOVE} the tape is falling and turning over, and "
     "the two clean unfaded rectangles it has left on the paint are exposed behind it",
     base_neg("sticky tape dispenser, packing tape, brand on the tape"),
     "cannot be considered ... a reliable means of acquainting interested parties of the fact "
     "that their rights are before the courts"),

    ("G279", "ACT_5",
     "A worn doormat with a pair of shoes set neatly against the wall beside it and a coat still "
     "on its hook just inside a half-open front door, photographed from three paces at knee height "
     f"in flat daylight from the walkway. {ERA}. {MOVE} the door is swinging slowly inward and the "
     "hem of the coat is moving with the draught it makes",
     base_neg("welcome mat with words, holiday wreath, staged hallway"),
     "Failure to effect personal service on the first visit ... hardly suggests that the tenant "
     "has abandoned his interest in the apartment"),

    ("G280", "ACT_5",
     "An invented man in his fifties in plain post-room clothes standing over a canvas mail sack "
     "filled to its mouth with plain envelopes, seen in three-quarter from a metre at sack height, "
     "his face lit evenly by an overhead lamp with no expression put on for the camera and not "
     f"looking at the lens, both hands laid flat on the sack's rim. {PAPER_BLANK} on the envelopes. "
     f"{ERA}. {MOVE} the slack mouth of the sack is sagging further open and the top envelopes are "
     "sliding down its side",
     base_neg(N_PAPER, N_HAND, "postal uniform, cap with a badge, courier branding, "
              "advertising smile, eye contact with the lens"),
     "The mails ... provide an efficient and inexpensive means of communication."),

    ("G281", "ACT_5",
     "A plain envelope carried flat on one open upturned palm along an open walkway, the arm "
     "cropped at the elbow and no other part of the person in frame, photographed from the side at "
     f"fifty centimetres with the walkway running away out of focus behind. {PAPER_BLANK}. {ERA}. "
     f"{MOVE} the free corner of the envelope is lifting off the palm in the moving air and the "
     "cuff at the cropped elbow is out of line",
     base_neg(N_PAPER, N_HAND),
     "Notice by mail in the circumstances of this case would surely go a long way"),

    ("G282", "ACT_5",
     "A bank of plain apartment letter boxes photographed from directly beneath at a steep upward "
     "angle at forty centimetres so the boxes loom over the camera, one small door hanging open "
     f"and an envelope half out of it, cold stairwell light. {PAPER_BLANK}. {ERA}. {MOVE} the open "
     "box door is swinging on its hinge and the envelope is sliding out of the slot",
     base_neg(N_PAPER, "apartment numbers, name plates on the boxes, intercom panel"),
     "the subject matter of the action also happens to be the mailing address of the defendant"),

    ("G283", "ACT_5",
     "A painted front door with a letter slot in it and a sheet taped above the slot at head "
     "height, photographed from two paces at chest height square on in flat overcast light. "
     f"{PAPER_GREY} on the sheet. {ERA}. {MOVE} the slot's metal flap is clapping open and shut in "
     "the wind and the bottom corner of the sheet above it is lifting on the same gusts",
     base_neg(N_PAPER, "house number, name plate, door knocker with a face"),
     "The apartment they were trying to take was the place they would have got the letter."),

    ("G284", "ACT_5",
     "A crank-driven duplicator of the period turning out sheets into a wire receiving tray, "
     "photographed from the side at forty centimetres under one hard work light, nobody in frame. "
     f"{PAPER_GREY} on the delivered sheets. {ERA}. {MOVE} the drum is turning with its surface "
     "smeared and one sheet is caught halfway out of the machine, bowed and not yet in the tray",
     base_neg(N_PAPER, "photocopier, laser printer, modern office machine"),
     "The State's continued exclusive reliance on an ineffective means of service"),

    ("G285", "ACT_5",
     "An emptied apartment room with its front door standing wide open onto a bright walkway, "
     "photographed from deep inside at eight paces at chest height, the interior holding its "
     f"detail and never going black. {ERA}. {MOVE} the door is moving on its hinge and the shape "
     "of daylight it lays on the bare floor is sliding across the boards",
     base_neg("furniture on a pavement, removal boxes, a family leaving, ransacked room"),
     "the State has deprived them of property without the due process of law"),

    ("G286", "ACT_5",
     "One narrow beam of daylight through a partly closed door falling on a single small patch of "
     "bare floorboard, photographed at floor level at one metre with the rest of the room dark but "
     f"holding detail. {ERA}. {MOVE} the beam is narrowing as the door drifts closed and its edge "
     "is travelling across the boards",
     base_neg("light beam special effect, god rays, smoke machine, horror lighting"),
     "we hold only that posted notice pursuant to section 454.030 is constitutionally inadequate"),

    ("G287", "ACT_5",
     "A wooden pigeonhole rack with every hole bare, photographed at a steep angle from one side "
     "at a metre so the holes run away to a point, cold flat light from a window out of frame. "
     f"{PAPER_BLANK}. {ERA}. {MOVE} one loose sheet standing on edge in a hole halfway down the "
     "rack is buckling and about to fall out of it",
     base_neg(N_PAPER, "hotel key rack, room numbers, pigeon holes with labels"),
     "It is not our responsibility to prescribe the form of service that the Commonwealth should "
     "adopt."),

    ("G288", "ACT_5",
     "A plain envelope lying in a puddle on a concrete walkway with its edge already swollen and "
     "dark, photographed at ten centimetres at puddle level in flat rain light. "
     f"{PAPER_BLANK}. {ERA}. {MOVE} rain rings are spreading across the puddle and the envelope's "
     "free corner is lifting and floating on the moving water",
     base_neg(N_PAPER, "flood, storm drama, dramatic reflection of a skyline"),
     "even conceding that process served by mail is far from the ideal means"),

    ("G289", "ACT_5",
     "A sheet taped to a painted apartment door with a plain envelope wedged behind the door "
     f"handle of the same door, photographed dead on at one metre in flat overcast light. "
     f"{PAPER_GREY} on the taped sheet. {ERA}. {MOVE} both papers are moving in the same gust and "
     "out of phase with each other, the sheet's corner up and the envelope's free end down",
     base_neg(N_PAPER),
     "posted service accompanied by mail service is constitutionally preferable to posted service "
     "alone"),

    ("G290", "ACT_5",
     "An open-air walkway empty from end to end at the flattest hour of the day, photographed from "
     "one end at knee height so the balustrade and the run of doors both go away to a point, one "
     f"single scrap of pale paper on the concrete halfway down. {PAPER_BLANK}. {ERA}. {MOVE} the "
     "scrap lies still except for one corner that is ticking up and down, and a loose downpipe "
     "bracket further along is swinging",
     base_neg(N_PAPER, "motel corridor, modern apartment block, glass balustrade"),
     "⟨HELD⟩"),

    ("G291", "ACT_5",
     "A single door key lying alone on a bare formica table top, photographed at twenty "
     f"centimetres at table level with one window out of frame to the left. {ERA}. {MOVE} the key's "
     "steel ring is still spinning flat on the formica beside it, and the shadow of a moving "
     "curtain is crossing the table",
     base_neg("bunch of keys, key fob with a logo, estate agent key tag, new brass key"),
     "Affirmed does not mean three tenants walked out holding a key."),

    ("G292", "ACT_5",
     "An open walkway that ends at a blank brick wall, photographed from six paces at chest height "
     f"so the wall closes the frame, flat grey light and nobody in it. {PAPER_BLANK}. {ERA}. "
     f"{MOVE} grit and one "
     "pale scrap of paper are blowing along the walkway and piling up against the foot of the "
     "brick",
     base_neg(N_PAPER, "dead end alley, graffiti, urban decay cliché"),
     "It simply stops."),

    ("G293", "ACT_5",
     "Three plain wooden chairs pushed back from one side of a long bare table, photographed from "
     "the far end of the table at table height at three metres, one window light falling across "
     f"the wood. {ERA}. {MOVE} the nearest of the three chairs is still rocking on its back legs "
     "and a curtain at the window is travelling across the light",
     base_neg("jury box, courtroom, boardroom, conference room, dining room"),
     "Three Justices did not agree, and the dissent is not a footnote."),

    ("G294", "ACT_5",
     "A post office counter grille seen from the public side with a plain envelope halfway under "
     "it, photographed at counter height at half a metre, the space behind the grille dim but "
     f"holding its detail. {PAPER_BLANK}. {ERA}. {MOVE} the envelope is mid-push under the grille "
     "and the grille's loose chain is swinging against the bars",
     base_neg(N_PAPER, "bank teller, security glass, queue barrier, opening hours notice"),
     "the Court holds that the Constitution prefers the use of the Postal Service to posted "
     "notice"),

    ("G295", "ACT_5",
     "An empty wire in-tray on a bare desk with nothing whatever in it, photographed at desk "
     "height at thirty centimetres with one shaft of window light lying across the tray and the "
     f"blotter beneath it, and that blotter is bare of any marking. {ERA}. {MOVE} dust is turning "
     f"in the shaft of light and the free corner "
     "of the blotter is lifting off the desk",
     base_neg("office clutter, modern desk accessories, computer, telephone with buttons"),
     "despite the total absence of any evidence in the record regarding the speed and reliability "
     "of the mails"),

    ("G296", "ACT_5",
     "Five or six loose pages laid out side by side on a plain table so that how few of them there "
     "are is the subject of the picture, photographed at a low table-level angle at half a metre "
     f"with the empty wood running away past them. {PAPER_GREY}. {ERA}. {MOVE} two of the pages are "
     "lifting at once in a draught, out of phase with each other, and one has already slid over "
     "the edge of the table",
     base_neg(N_PAPER, "stack of files, mountain of paperwork, archive shelves"),
     "The sole ground for the Court's result is the scant and conflicting testimony of a handful "
     "of process servers in Kentucky."),

    ("G297", "ACT_5",
     "A long corridor of identical closed public-building doors, photographed at a steep raking "
     "angle from chest height so the doors compress into a single receding band, flat institutional "
     f"daylight and nobody in it. {ERA}. {MOVE} one door far down the line is mid-swing and is the "
     "only thing in the frame that is not still",
     base_neg("hotel corridor, hospital ward, prison landing, cell doors, office suite"),
     "the Court confidently overturns the work of the Kentucky Legislature, and, by implication, "
     "that of at least 10 other States"),

    ("G298", "ACT_5",
     "A long empty shelf with one single book lying flat and alone at its far end, photographed "
     "along the shelf at shelf height at forty centimetres so the emptiness runs at the camera, "
     f"raking light. {PAPER_BLANK}. {ERA}. {MOVE} dust is lifting along the shelf toward the camera "
     "and the book's front cover is standing up and dropping back in the draught",
     base_neg(N_PAPER, "library, bookshop, gilt spines, book titles"),
     "does not cite a single case, other than the decision below"),

    ("G299", "ACT_5",
     "Eleven identical plain enamel cups set out along a long bare table in an empty room, "
     "photographed from one end at table height at two metres so they run away in a line, cold "
     f"daylight from a high window. {ERA}. {MOVE} steam is rising from every one of them and "
     "drifting the same way across the table",
     base_neg("café, restaurant, tea party, branded mugs, coffee shop"),
     "at least 11 States authorizing notice in summary eviction proceedings solely by posting"),

    ("G300", "ACT_5",
     "Two separate pages held side by side flat against the same window pane, one open hand "
     "pressed flat on each of them, photographed from forty centimetres from inside the room so "
     f"both are back-lit and the daylight comes through them. {FLAT_HAND} -- here the surface is "
     f"the glass with the page against it. {PAPER_GREY} on both pages. {ERA}. {MOVE} both pages are bowing "
     "and rattling in the draught from the open sash, and they are bowing out of time with each "
     "other",
     base_neg(N_PAPER, N_HAND),
     "Both opinions read the same three clauses. One read the words. The other read the "
     "depositions."),

    ("G301", "ACT_5",
     "Two empty wooden crates set side by side on a bare floor, both open and both empty, "
     "photographed from above and to one side at two paces at chest height in flat light. "
     f"{PAPER_BLANK}. {ERA}. {MOVE} a loose sheet of paper is caught on the rim of the nearer crate "
     "and is flapping hard, half in and half out of it",
     base_neg(N_PAPER, "removal boxes, packing up a home, shipping containers"),
     "we decline to resolve the constitutional question based upon the determination whether the "
     "particular action is more properly characterized as one in rem or in personam"),

    ("G302", "ACT_5",
     "A sheet lying on wet concrete, soaked right through so the light comes up through it and the "
     "grain of the concrete shows behind, photographed at fifteen centimetres at ground level. "
     f"{PAPER_GREY}, softened and running where the water has taken it. {ERA}. {MOVE} water is "
     "creeping visibly across the sheet and one corner has lifted clear of the wet and is curling "
     "up",
     base_neg(N_PAPER, "ink running into legible words, watermark, blood"),
     "What the paper did was the question."),

    ("G303", "ACT_5",
     "A door held open by a wedge of folded paper jammed under its leading edge, photographed at "
     f"ten centimetres at floor level so the wedge fills the lower frame. {PAPER_BLANK}. {ERA}. "
     f"{MOVE} the door is pressing and easing against the wedge in the wind and the wedge's loose "
     "outer leaves are fanning open",
     base_neg(N_PAPER, "rubber door stop, modern fire door, push bar"),
     "The Court gives lipservice to the principle ... but then goes on to do just that."),

    ("G304", "ACT_5",
     "A flight of worn public steps seen from the side, the treads dished in the middle by years "
     "of use, photographed at step height at one metre in flat grey light. "
     f"{PAPER_BLANK}. {ERA}. {MOVE} one pale scrap of paper is travelling down the flight and is "
     f"caught mid-bounce "
     "between two treads",
     base_neg(N_PAPER, "grand staircase, marble, red carpet, courthouse steps with columns"),
     "we have long since discarded the concept that due process authorizes courts to hold laws "
     "unconstitutional when they believe the legislature has acted unwisely"),

    ("G305", "ACT_5",
     "A letter box whose small door hangs by one hinge with torn paper caught in the hinge, "
     "photographed from the side at fifteen centimetres at night, lit only by a single stair bulb "
     f"above and to the left, the metal holding its detail and never going black. {PAPER_BLANK}. "
     f"{ERA}. {MOVE} the "
     "hanging door is swinging on its one hinge and the caught paper is flicking with it",
     base_neg(N_PAPER, "burglary scene, crowbar, forensic tape, horror lighting"),
     "It is no secret, after all, that unattended mailboxes are subject to plunder by thieves."),

    ("G306", "ACT_5",
     "A sheet taped to a painted door seen at a very shallow angle from the side so the door runs "
     "away out of the frame and the sheet stands out from the plane of the paint, photographed at "
     f"thirty centimetres. {PAPER_GREY}. {ERA}. {MOVE} the whole free edge of the sheet is standing "
     "right off the door in the wind and its shadow is sweeping across the paint",
     base_neg(N_PAPER),
     "posting notice at least gives assurance that the notice has gotten as far as the tenant's "
     "door"),

    ("G307", "ACT_5",
     "The single line of shadow cast by a taut string across a bare plaster wall, photographed "
     f"square on at one metre in hard side light with nothing else in the frame. {ERA}. {MOVE} the "
     "string is vibrating and the shadow line has smeared into a band",
     base_neg("laser line, minimal art installation, gallery wall"),
     "The dissent misconstrues the constitutional standard."),

    ("G308", "ACT_5",
     "An outdoor concrete stairwell seen from the landing above with the treads running away "
     "below, one flat hand on the steel handrail at the very edge of the frame and no other part "
     f"of the person in the picture, photographed at one metre in flat wet daylight. {FLAT_HAND} "
     f"-- here the surface is the handrail. {ERA}. {MOVE} rain is blowing across the open side of "
     "the stairwell in visible bands and water is running down the rail past the hand",
     base_neg(N_HAND, "prison landing, fire escape drama, vertigo shot, drone view"),
     "a summary proceeding for quickly determining whether or not a landlord has the right to "
     "immediate possession"),

    ("G309", "ACT_5",
     "A dripping outdoor tap over an iron drain grate set into a brick wall, photographed at "
     f"twenty centimetres in cold flat light. {ERA}. {MOVE} one drop is caught mid-fall below the "
     "spout and the ring it made a moment ago is still spreading in the standing water on the "
     "grate",
     base_neg("modern mixer tap, chrome fitting, kitchen sink, water feature"),
     "Many expenses of the landlord continue to accrue whether a tenant pays his rent or not."),

    ("G310", "ACT_5",
     "A spring door closer at the top of a plain public door with the door itself mid-close, "
     "photographed from below at forty centimetres so the closer's arm and the top of the door "
     f"fill the frame. {ERA}. {MOVE} the closer's arm is mid-travel and folding, and the leading "
     "edge of the door below it has smeared",
     base_neg("modern aluminium door, push bar, fire exit sign, automatic door"),
     "The means chosen for making service of process ... must be prompt and certain"),

    ("G311", "ACT_5",
     "The inside of a front door seen from a chair in a dim room, the bar of daylight under the "
     "door the brightest thing in the frame, photographed from seat height at four paces with the "
     f"room dark but holding all its detail. {ERA}. {MOVE} a shadow is crossing the bar of daylight "
     "under the door and passing on, and the net curtain at the side window is moving",
     base_neg("horror scene, silhouette of an intruder, thriller lighting, black crushed shadows"),
     "it is difficult to see how a means of serving process that fails to afford actual notice ... "
     "can be deemed either prompt or certain"),

    ("G312", "ACT_5",
     "Two painted doors facing each other across a narrow landing, both shut, photographed from "
     f"the middle of the landing at chest height in flat light from a stair window. {ERA}. {MOVE} "
     "both doors are breathing against their latches in the same draught and one is a finger's "
     "width further open than the other",
     base_neg("hotel corridor, symmetrical art photograph, hall of mirrors"),
     "That is where the two opinions stop talking to each other."),
]


# ---------------------------------------------------------------------------------------------
def prompt_body(body: str, neg_add: str) -> str:
    """The one and only place a prompt string is assembled."""
    return f"{body} [STYLE] Avoid: [NEG], {neg_add}"


def chunks(seq: list, n: int) -> list[list]:
    return [seq[i:i + n] for i in range(0, len(seq), n)]


def by_act() -> dict[str, list[tuple]]:
    out: dict[str, list[tuple]] = {"ACT_4": [], "ACT_5": []}
    for r in P:
        out[r[1]].append(r)
    return out


# ---------------------------------------------------------------------------------------------
DERIVATION = """\
## 1. なぜ70枚なのか（引き算ではなく `solve_totals` から導いた）

**ゲートの出力（現状）**

```
[satisfied] greene: cuts=389 distinct_video=196 stills_in_film=117 mandatory=224
  - distinct_video_assets: 196 distinct footage+motion source(s) across 272 video cut(s),
    against a declared 234 -- 38 short
```

**「234 − 197 = 37」は成立しない。** 理由は3つあり、いずれも実測で確認した。

1. **プールは 197 ではなく 196。** `asset_manifest.v003.json` の実数は factory **73** ・
   motion **123** ・stills **117**。`greene/factory/` にはファイルが74個あるが、そのうち
   `AR-6041714` は `overlay` 区分でカット素材ではない。フィルム側の distinct 196 = 73 + 123 と
   完全一致しており、**プールの映像素材は1本残らず既にフィルムに入っている。**
2. **新規プレートを足すと factory と motion の配分そのものが動く。** `solve_totals` は
   `video = ceil(round(total_sec / 4.6) * 0.68) = ceil(400 * 0.68) = 272` を固定したうえで、
   **factory と motion の cap の比で 272 を割り振る**。motion プールを増やすと factory 側の
   取り分が減り、`_CAP_FACTORY = 1` では減った分だけ **archive クリップがフィルムから落ちる**。
   だから「足した枚数 = 増える distinct」にはならない。
3. **いま盤上にあるフィルムは、いまのビルダーでは再現できない。**
   `remotion/src/data/greene_film.json` は **01:46**、`build_case_film_generic.py` は **01:51**。
   その5分の間に、プランナが factory を **2回使える前提から `check_asset_reuse.MAX_USES_FACTORY = 1`
   を import する形に変わった**。実測でも、盤上のフィルム（factory 73本すべてを使い 28本を2回使用）は
   `cap_f = 2` の解とバイト単位で一致し、`cap_f = 1` の解とは一致しない。**次のビルドは `cap_f = 1`
   で走る。** memphis のフィルム（02:42・distinct 242）は `cap_f = 1` の解と一致しており、これが
   いまの正しい挙動である。

**実測スイープ**（`solve_totals` を実際に呼び、`repeated()` の round-robin まで再現した）:

| 追加枚数 N | motion プール | factory cuts | motion cuts | distinct_video | 234 |
|---:|---:|---:|---:|---:|:--|
| 0 | 123 | 62 | 210 | **185** | fail |
| 37 | 160 | 51 | 221 | 211 | fail |
| 38 | 161 | 50 | 222 | 211 | fail |
| 66 | 189 | 44 | 228 | 233 | fail |
| **67** | **190** | **44** | **228** | **234** | **PASS（最小）** |
| 70 | 193 | 43 | 229 | **236** | PASS |

**導出値 = 67枚。** これが `check_spec_satisfied.py` を通す最小である。
（参考：もし `cap_f` が 2 のままだったなら 38枚で足りた。37 では `cap_f = 2` でも 233 で1本足りない。）

**この発注は 70枚。** 67 は**余裕ゼロ**で、i2v に持ち込めなかったプレートが1枚出た瞬間に
233 に落ちて再びレンダーが止まる。+3 は**その脱落分の余裕**であり、70枚全部が実際にフィルムに
入る（`m = 229 >= 193`）。3枚まで脱落しても 234 を維持する。

**この計算が前提にしている実測値**（変わったら再計算すること）:
`total_sec = 1841.006` · factory プール 73 · motion プール 123 · stills 117 ·
`TARGET_CUT_SEC = 4.6`（greene は `target_cut_sec` を宣言していない）· `MIN_VIDEO_SHARE = 0.68` ·
`_CAP_FACTORY = 1` · `_CAP_MOTION = 2`。
"""

PLACEMENT = """\
## 2. どの区分を増やしたか（id が配置を決める）

**均等には配らない。**そして「配る」の意味がこの pipeline では特殊なので、先に仕組みを書く。

`build_case_film_generic.py` は motion プールを**ソート順で1本のキューに積み**、区分ごとに
`per_m[section]`（＝区分の秒数比）だけ先頭から取っていく。**つまり id の順番が区分を決める。**
盤上のフィルムでも実際にそうなっている（G001→HOOK, G002→OP, G003〜→ACT_1 …）。

追加70枚は既存 `G001`–`G224` の**後ろ**に並ぶので、キューの後半に入る。実測（`solve_totals` +
`split_by_section` を再現）した配置:

| 区分 | 秒数 | 現在の distinct video | 追加後の新規プレート |
|---|---:|---:|---:|
| HOOK | 8.4 | 1 | 0 |
| OP | 10.0 | 2 | 0 |
| ACT_1 | 373.3 | 55 | 0 |
| ACT_2 | 209.8 | 31 | 0 |
| ACT_3 | 297.1 | 43 | 0 |
| **ACT_4** | 287.4 | 43 | **25**（`G243`–`G267`） |
| **ACT_5** | 590.0 | 87 | **45**（`G268`–`G312`） |
| ENDING | 65.1 | 10 | 0 |

**増やしたのは ACT_4 と ACT_5 である。**これは機構の結果であると同時に、カットリストから見ても
正しい：ACT_5 は 590秒・124カット（映画の32%）で**全区分中いちばん長く**、キューが尽きて
折り返し（同じクリップの2回目）が出るのは **ACT_5 の後半と ENDING** である。ACT_4 と ACT_5 を
合わせると 877秒・映像カット130本＝**映画のほぼ半分**で、そこが実際に薄い。

> **★境界は ±3 id ほど動きうる。** 上の内訳はいまのプール実数（factory 73 / motion 123 /
> stills 117 / `total_sec` 1841.006）での計算である。生成までに素材が増減すると区切りが数枚ずれる。
> **ACT_4 と ACT_5 は本編で隣り合っており画づくりの語彙も共通なので、数枚ずれても破綻しない。**
> 破綻するのは「ACT_1 用の絵を ACT_5 に置く」ような大きなずれだけで、それは起きない。
"""


def build_md() -> str:
    acts = by_act()
    L: list[str] = []
    a = L.append
    a(f"# EP62 greene — Codex 画像生成 **バッチB 新規発注** v001（**{len(P)}枚**・1プロンプト1枚）")
    a("")
    a("> ## ★★★ この70枚は **すべて新規 ID** です。既存ファイルを1つも上書きしません。 ★★★")
    a(f"> 保存先は既存と同じ `{SAVE_DIR}\\` ですが、**`G243`–`G312` はまだ存在しない番号**です。")
    a("> 棚の実測: `G001.png`–`G242.png` の242枚（欠番なし・最大 `G242`）。**次の空き番から取りました。**")
    a("> **`G001`–`G242` には触らないでください。** 再生成もしません。")
    a(">")
    a("> ## ★★★ この70枚は **i2v（静止画→動画）の元絵** です。 ★★★")
    a("> 静止画のまま使う絵ではありません。生成後に Wan i2v で全枚を 5.03秒のクリップにします。")
    a("> **だから、動く余地のない絵を描かないでください。** 各プロンプトには "
      "`MOVING ELEMENT` の一文があり、")
    a("> **シャッターが開いた時点で既に動いている物**を1つ名指ししています。**この一文を削らないでください。**")
    a("> 完全に静止した構図は動かない i2v クリップになり、`animation_density` がそれで落ちます"
      "（EP65 はこれで3回作り直しました）。")
    a("")
    a("**由来:** `check_spec_satisfied.py --slug greene` が `distinct_video_assets` で"
      "レンダーを止めている。棚の追加ステージングは3波とも失敗した"
      "（最後の波は未ステージ候補1,740本を実測したが、上位は外国の国旗・水中のインク・橋・鳥で、"
      "登録語が偶然タグに入っているだけだった）。**1975年ルイビルの公営住宅は棚に存在しない。**"
      "生成プレートなら**構造的に時代が合う**——時代違いはこのエピソードを3回刺した欠陥である"
      "（現代の米国投票用紙・2011年式 Range Rover Evoque・他作品のショットリストカード。3件とも"
      "`config/footage_blocklist.v001.json` に登録済み）。")
    a("")
    a("---")
    a("")
    a(DERIVATION)
    a("---")
    a("")
    a(PLACEMENT)
    a("---")
    a("")
    a("## 3. ★★★ 最重要：1プロンプト = 1枚 ★★★")
    a("")
    a("1. **各プロンプトから画像を1枚だけ作る。** 同じプロンプトで2枚目を作らない。")
    a("2. **`_02` / `_03` / `_v2` を作らない。**「良いのが出るまで回す」を禁止する。")
    a("3. **ファイル名は ■ のとおりちょうど。** 別名で出すと、どれが正典か分からなくなります。")
    a("4. 作り直してよいのは §4 の禁止に触れたときだけ。そのときも**文言を直してから1枚**。")
    a("")
    a("## 4. ★絶対条件")
    a("")
    a("正典は `episodes/PD-2026-062-greene/episode_spec.v001.json` の `forbidden_subjects` と "
      "`era_setting` です。")
    a("")
    a("- **人物は入れる。顔も描いてよい。**（オーナー決定 2026-07-04）"
      "禁じられているのは**実在する特定の人物に似ていること**だけ。")
    a("  完全に架空の一般人であること。**Linnie Lindsey / Barbara Hodgens / Pamela Ray の3人、"
      "および執行官に似せない。**")
    a("  カメラ目線の作り笑い・広告のモデル顔にしない。**働いている人の、作っていない顔。**")
    a("- **読める文字・数字・手書き・署名・印章・記章・ロゴを描かない。**")
    a("  ★**この話で最大の事故源はここです。** 中心にある物は「ドアに貼られた召喚状」であり、"
      "生成器はそれを見ると**必ず何か書きます**。")
    a("  だから本発注は、`[NEG]` に頼らず**ポジティブ側で紙の形を指定**しています——"
      "「完全な白紙」か「均一な灰色の横棒が等間隔に並ぶだけで文字の形が1つも無い面」。")
    a("  **バッチCで `[NEG]` だけの禁止が効かないことは実証済み**（`L146` の文字マークが2回戻った）。"
      "**この指定文を削らないでください。**")
    a("- **時代と場所は 1975–1982年・米国ケンタッキー州ルイビル。**")
    a("  現代の車・電話・画面・スニーカー・電動キックボード・EUの標識・ラテン文字以外の文字は不可。")
    a("- **立ち退きの最中を描かない。** 歩道に出された家具・追い出される家族・ドアの前の制服の執行官。")
    a("- **家主というキャラクターを描かない。** 被告は政府機関（ルイビル住宅公社）です。")
    a("- **法廷内観・木槌・判事席・監獄・鉄格子・手錠を描かない。**")
    a("- **実在と特定できる建物を描かない。**")
    a("- **子どもの顔を描かない。** 子どもは痕跡でのみ表す（本発注では `G254` のチョークだけ）。")
    a("- **手は指が数えられること。** 融合した指・6本指・親指の欠落は不可。")
    a("  **手が主役のときは必ず「平らな面に伏せて置いた手」**"
      "（EP66 `L236` が3回落ちた形と、`L247` で通った形）。")
    a("- **黒つぶれさせない。** スマホで見て何が写っているか分かること。")
    a("")
    a("## 5. スタイル（★必ず展開してから生成）")
    a("")
    a("**`[NEG]` は EP66 バッチD の `[NEG]` と1バイト違いません。**"
      "この発注書は生成時に `EP66_openfields_CODEX_BATCH_D.v001.md` の本文から"
      "**機械的に読み出して**埋め込んでいます（`check_image_order_neg.py` の `neg_block()` "
      "そのものを使用）。**1語も変えずに展開してください。**")
    a("")
    a("**`[STYLE]`** ＝ 末尾にそのまま連結（**greene 自身のもの**。バッチDのものは"
      "「late Appalachian autumn / rural Pennsylvania and Middle Tennessee」で、"
      "ルイビルの映画には天候も州も違う。既存242枚と絵を揃えるためにも greene の正典を使う）:")
    a("")
    a(f"> , {STYLE}")
    a("")
    a("**`[NEG]`** ＝ `Avoid:` の後にそのまま連結:")
    a("")
    a(f"> {NEG}")
    a("")
    a("> ### ★プレートごとの `[NEG]` 追記について★")
    a("> 70枚すべてが `Avoid: [NEG], …` と、`[NEG]` の後ろに読点で語を続けています。")
    a("> **これは上の正典 `[NEG]` を展開したうえで、その末尾にさらに続ける、という意味です。**")
    a("> **正典 `[NEG]` の語を1語も削らないでください。**追記だけが増えます。")
    a(">")
    a("> ### ★`[NEG]` は「人」を禁じていません★")
    a("> 禁じているのは **`recognisable person, identifiable person, likeness of a real "
      "individual,`**")
    a("> **`portrait of a named person, celebrity, public figure, deepfake`** "
      "——**実在の誰かに似ること**だけです。")
    a("> greene のバッチA の `[NEG]` は `human face, face, facial features, eyes …` と書いて"
      "**人が写ること自体**を止めていました。")
    a("> EP66 では同じ書き方が **191枚の作り直し**を招いています。**戻さないでください。**")
    a(">")
    a("> ### ★この発注では `[STYLE]` に時代が入っています★")
    a("> greene の `[STYLE]` は "
      "`mid-1970s to early-1980s American public housing period detail` を含みます。")
    a("> それに加えて**各プロンプト本文にも**「1975–1982年のルイビル」を明記し、"
      "`[NEG]` 追記でも現代物を止めています。**三重にしてあるのは、"
      "時代違いが実際に出荷されたからです。**")
    a("")
    a("## 6. 命名と保存先")
    a("")
    a("- ファイル名は **■ のとおりちょうど**（`G243.png` など）。**`_v2` / `_02` を付けない。**")
    a(f"- 保存先 `{SAVE_DIR}\\`。**既存の `G001`–`G242` を上書きしない。**")
    a("- 長辺 3840px 以上・16:9・PNG。")
    a("")
    a(f"## 7. 対象一覧（{len(P)}枚）")
    a("")
    for act in ("ACT_4", "ACT_5"):
        rows = acts[act]
        a(f"### {act} — {len(rows)}枚（`{rows[0][0]}`–`{rows[-1][0]}`）")
        a("")
        a("| # | ID | 台本のビート | 動く要素 |")
        a("|---:|---|---|---|")
        for i, (pid, _act, body, _neg, line) in enumerate(rows, 1):
            move = body.split(MOVE, 1)[1].strip() if MOVE in body else ""
            move = move.split(",")[0].strip()
            a(f"| {i} | `{pid}` | {line} | {move} |")
        a("")
    a("---")
    a("")
    a("## 8. プロンプト（各1枚）")
    a("")
    for act in ("ACT_4", "ACT_5"):
        a(f"### ── {act} ──")
        a("")
        for pid, _act, body, neg_add, line in acts[act]:
            move = body.split(MOVE, 1)[1].strip() if MOVE in body else ""
            a(f"#### `{pid}.png` — {act}")
            a("")
            a(f"**台本のビート:** {line}")
            a("")
            a(f"**動く要素（i2v が動かす対象）:** {move}")
            a("")
            a(f"- `{pid}.png`")
            a(prompt_body(body, neg_add))
            a("")
            a(f"**保存先:** `{SAVE_DIR}\\{pid}.png`（**新規。既存を上書きしない**）")
            a("")
            a(f"**`[NEG]` 追記:** 正典 `[NEG]` の末尾に `, {neg_add}` を足す。"
              "**正典側は1語も削らない。**")
            a("")
    a("---")
    a("")
    a("## 9. 発注書の検査")
    a("")
    a("```")
    a(f"py -3.11 scripts/check_image_order_neg.py --file {OUT_MD.relative_to(ROOT).as_posix()}")
    a("```")
    a("")
    a("顔／実在人物・読める文字・手書き・紋章／記章・数字の**五族すべて**が `[NEG]` に"
      "入っていることを機械が確認します。")
    a("")
    a("この発注書とペーストファイルは**1つの Python データソース**から生成されており、"
      "本文がずれることは構造上ありえません:")
    a("")
    a("```")
    a("py -3.11 scripts/build_ep62_greene_image_order.py --verify")
    a("```")
    a("")
    a("## 10. 生成後にやること（発注者側）")
    a("")
    a("1. **70枚を1枚ずつ native（3840x2160のまま）で目視。** 縮小コンタクトシートでは"
      "紙の上の文字も車のバッジも**見えません**（EP66 で 372px では見えず4倍で初めて出た）。")
    a("   - 紙が写る全プレート: 紙面を**8倍以上**に拡大し、"
      "**文字の形が1つも無い**ことを確かめる。")
    a("   - 人物が写る3枚（`G271` `G272` `G280`）: 実在の誰かに似ていないこと、"
      "手の指が数えられることを確かめる。")
    a("   - 全枚: **1975–1982年に無い物**が1つも無いこと（車・電話・画面・スニーカー・"
      "プラスチック建材）。")
    a("2. **i2v に回す。** `EP62_greene_I2V_RESUME.v001.md` §3 のコマンド。"
      "**`--length 121` を守る**（81フレームだと 4.6秒カットの中で `<Loop>` が巻き戻る）。")
    a("   - `G271` `G272` `G280` は**顔が写るプレート**です。i2v の人物レジーム `N2` は "
      "`face turning toward camera, visible facial features, recognisable face` を"
      "ネガティブに持っており、**顔が既に写っている元絵と喧嘩します**。"
      "この3枚だけは その3語を外し、`face changing identity, features morphing, second face` "
      "に置き換えて回してください。")
    a("   - `I2V_RESUME` §6 の鉄則をそのまま守ること: **i2v プロンプトに「動く物」を"
      "名詞で書かない**。動く物はこの発注書の**元絵の側**に入れてあります。")
    a("3. **i2v 後**に `build_asset_manifest_motionfirst.py --slug greene` → "
      "`build_case_film_generic.py` → `check_spec_satisfied.py --slug greene`。"
      "**distinct_video が 234 以上になっていることを数字で確認してからレンダーする。**")
    a("4. `mandatory_stills` について: この70枚は **`mandatory_stills` に足さないでください。**"
      "足すと「宣言した静止画がカットに無い」で落ちる可能性が増えるだけで、"
      "`distinct_video_assets` の充足には一切関係ありません（§11）。")
    a("")
    a("## 11. この発注を書いていて見つけた、仕様側の2点（変更していない・報告のみ）")
    a("")
    a("1. **`target_cut_sec` が未宣言。** greene の `episode_spec.v001.json` にこのキーは"
      "**存在しません**（`null` ですらなく不在）。`build_case_film_generic.py` は"
      "宣言が無いとビルダー定数 4.6 を使います。CLAUDE.md §4.6 は"
      "**「宣言されていない値はエラーであって、推定される既定値ではない」**と定めており、"
      "これはその規定に反した既定値フォールバックです。EP65 marmet は `3.7` を宣言しており、"
      "62/63/64 だけが未宣言です。")
    a("2. **`distinct_video_assets: 234` に導出が無い。** EP62–65 の4本が**同じ 234** を宣言し、"
      "`notes` にその数の出どころが書かれていません（写した数に見えます）。"
      "`schemas/episode_spec.v001.json` の定義は "
      "**「footage cuts として計算せよ。cuts ÷ reuse cap ではない」**であり、"
      "greene の実測 `total_sec = 1841.006` からその定義どおり導くと "
      "**`ceil(round(1841.006 / 4.6) * 0.68) = ceil(400 * 0.68) = 272`** です。"
      "**234 は導出値より 38 低い。** ただし memphis が 234 を満たしているので"
      "「明らかに誤り」とは言えず、**本発注では変更していません**。"
      "変えるなら4本まとめて、`target_cut_sec` の宣言と同時にやるべきです。")
    a("3. **`mandatory_stills` が 224 なのにフィルムの静止画は 117。これは問題ではありません。**"
      "`check_spec_satisfied.py` は **拡張子ではなく stem で照合**します"
      "（`G045.png` は `G045.mp4` でも満たされる）。実測すると 224件の内訳は"
      "**PNGカットとして 102 ・MP4（i2v化）カットとして 122 ・どちらにも無い 0**。"
      "**224件すべてが画面に出ており**、だからゲートは何も言いません。"
      "「117 しか無い」は静止画のまま出ている枚数であって、欠落ではありません。")
    a("")
    return "\n".join(L) + "\n"


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
    "・**人物は入れてよい。顔も描いてよい。**（オーナー決定 2026-07-04）",
    "・ただし実在する特定の人物に似せない。有名人・公人・実在の誰かの肖像は不可",
    "・読める文字・数字・手書き・署名・印章・記章・ロゴを一切描かない",
    "・**紙は「完全な白紙」か「均一な灰色の横棒が等間隔に並ぶだけの面」**（本文に指定あり）。",
    "　この話の中心は「ドアに貼られた召喚状」です。**紙の上に何か書いたら不合格。**",
    "・舞台は**1975〜1982年の米国ケンタッキー州ルイビル**。現代の車・電話・画面・スニーカー・",
    "　電動キックボード・欧州の標識・ラテン文字以外の文字は一切不可",
    "・立ち退きの最中（歩道の家具・追い出される家族・制服の執行官）を描かない",
    "・法廷内部・木槌・判事席・監獄・鉄格子・手錠を描かない",
    "・子どもの顔を描かない",
    "・手は指が数えられること。融合した指・6本指・親指の欠落は不可。",
    "　**手が主役のときは必ず「平らな面に伏せて置いた手」**（EP66 L236 の失敗と、通った修正）",
    "・写真として撮られたもののように。イラスト、CG、絵画調にしない",
    "・**黒つぶれさせない。** スマホで見て何が写っているか分かること",
    "",
    "──────── ★この発注で特に大事な点 ────────",
    "",
    "・**この70枚は i2v（静止画→動画）の元絵です。** 生成後に全枚を動画化します。",
    "　各プロンプトに `MOVING ELEMENT, already mid-movement when the shutter opens:` という",
    "　一文があり、**シャッターが開いた時点で既に動いている物**を名指ししています。",
    "　**その一文を必ず絵にしてください。** 完全に静止した構図は、動かない動画になります。",
    "・**すべて新規の番号です。** `G001`〜`G242` は既に存在します。**上書きしないでください。**",
    "",
]


def paste_block(rows: list[tuple], title: str, idx: int, total: int) -> str:
    L: list[str] = []
    a = L.append
    if total == 1:
        a(f"EP62 greene — 画像発注 バッチB 全{len(rows)}枚（1ファイル・分割なし）")
    else:
        a(f"EP62 greene — 画像発注 バッチB {idx}/{total}（{len(rows)}枚）")
    a(f"区分: {title}  [{rows[0][0]} – {rows[-1][0]}]")
    a("")
    a("★これは**新規発注**です。同名の既存ファイルはありません。")
    a("　新しい ID を勝手に作らない。`_v2` / `_02` を作らない。**名前は下の■のとおりちょうど。**")
    a("")
    L += PASTE_COMMON
    a("──────── プロンプト ────────")
    a("")
    for pid, _act, body, neg_add, _line in rows:
        a(f"■ {pid}.png")
        a(prompt_body(body, neg_add))
        a("")
    a("──────── 保存 ────────")
    a("")
    a(f"生成した画像は上の ■ の名前（例: {rows[0][0]}.png）で保存してください。")
    a(f"保存先 {SAVE_DIR}\\")
    a("長辺 3840px 以上・16:9・PNG。")
    return "\n".join(L) + "\n"


def build_paste() -> dict[str, str]:
    parts = chunks(P, CHUNK)
    files: dict[str, str] = {}
    for i, rows in enumerate(parts, 1):
        acts = sorted({r[1] for r in rows})
        files[f"batch_{i:02d}.txt"] = paste_block(rows, " / ".join(acts), i, len(parts))
    return files


def build_merged() -> str:
    return paste_block(P, "ACT_4 / ACT_5", 1, 1)


# ---------------------------------------------------------------------------------------------
BANNED_IN_NEG = ("human face", "facial features", "eyes")
REQUIRED_IN_NEG = ("recognisable person", "identifiable person", "likeness of a real individual",
                   "portrait of a named person", "celebrity", "public figure", "deepfake")
# words that must never appear in a POSITIVE body: batch A v002 proved diffusion models read a
# negated noun in the body as a request for it ("no signage" produced signage).
HAZARD_WORDS = ("text", "lettering", "signage", "numeral", "digit", "handwriting", "signature",
                "logo", "emblem", "insignia", "watermark", "gavel", "courtroom", "handcuff",
                "prison bars", "razor wire", "police", "sheriff badge", "child", "children",
                "eviction in progress", "scales of justice", "hourglass", "handshake")


def verify(md: str, files: dict[str, str], merged: str) -> int:
    bad = 0
    print("=" * 94)
    print("MEASURED VERIFICATION -- EP62 greene batch B")
    print("=" * 94)

    ids = [r[0] for r in P]
    a4 = [r[0] for r in P if r[1] == "ACT_4"]
    a5 = [r[0] for r in P if r[1] == "ACT_5"]
    print(f"prompts total                     {len(P)}")
    print(f"  ACT_4                           {len(a4)}  ({a4[0]}..{a4[-1]})")
    print(f"  ACT_5                           {len(a5)}  ({a5[0]}..{a5[-1]})")
    print(f"distinct plate ids                {len(set(ids))}")
    if len(set(ids)) != len(ids):
        print("  FAIL duplicate id"); bad += 1
    expect = [f"G{n:03d}" for n in range(243, 243 + len(P))]
    print(f"ids contiguous G243..G{242 + len(P):03d}       {ids == expect}")
    if ids != expect:
        print("  FAIL id range not contiguous"); bad += 1

    saves = [f"{i}.png" for i in ids]
    print(f"distinct save names               {len(set(saves))}")
    if len(set(saves)) != len(P):
        print("  FAIL save-name collision"); bad += 1

    # collision with the real store
    if STORE.is_dir():
        have = {p.stem.upper() for p in STORE.glob("G*.png")}
        clash = sorted(set(ids) & have)
        print(f"H: store existing plates          {len(have)} "
              f"(max {max(have, default='-')})")
        print(f"  collisions with this order      {len(clash)} {clash[:6]}")
        if clash:
            print("  FAIL would overwrite an existing plate"); bad += 1
    else:
        print("H: store                          NOT MOUNTED -- collision check skipped")

    print(f"\n[STYLE] length                    {len(STYLE)} chars")
    print(f"[NEG]   length                    {len(NEG)} chars")
    dneg = read_canonical_neg()
    print(f"[NEG] byte-identical to EP66 batch D: {NEG == dneg}")
    if NEG != dneg:
        print("  FAIL NEG drifted"); bad += 1
    # the checker picks the LONGEST matching blockquote; STYLE also says "no text, no lettering"
    print(f"[STYLE] shorter than [NEG] (so neg_block picks [NEG]): {len(STYLE) + 2 < len(NEG)}")
    if len(STYLE) + 2 >= len(NEG):
        print("  FAIL check_image_order_neg would read the STYLE line as the [NEG]"); bad += 1
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

    print("\ncontrol characters")
    corpus = {"<md>": md, "<merged>": merged, **files}
    total_ctrl = 0
    for name, text in corpus.items():
        ctrl = [(i, repr(ch)) for i, ch in enumerate(text)
                if unicodedata.category(ch) == "Cc" and ch != "\n"]
        total_ctrl += len(ctrl)
        if ctrl:
            print(f"  {name}: {len(ctrl)} -> {ctrl[:5]}")
            bad += 1
    print(f"  total non-newline control chars across md + merged + {len(files)} chunks: "
          f"{total_ctrl}")

    print("\nmd <-> paste prompt-body equality")
    joined = "\n".join(files.values())
    miss_md = miss_paste = miss_all = 0
    for pid, _act, body, neg_add, _line in P:
        b = prompt_body(body, neg_add)
        if b not in md:
            miss_md += 1; print(f"  {pid}: body NOT in md")
        if b not in joined:
            miss_paste += 1; print(f"  {pid}: body NOT in paste chunks")
        if b not in merged:
            miss_all += 1; print(f"  {pid}: body NOT in merged file")
    print(f"  bodies present in md              {len(P) - miss_md}/{len(P)}")
    print(f"  bodies present in paste chunks    {len(P) - miss_paste}/{len(P)}")
    print(f"  bodies present in merged file     {len(P) - miss_all}/{len(P)}")
    bad += miss_md + miss_paste + miss_all

    print("\nprompt shape")
    n_ok = sum(1 for r in P if prompt_body(r[2], r[3]).count(" [STYLE] Avoid: [NEG], ") == 1)
    print(f"  exactly one ' [STYLE] Avoid: [NEG], '           {n_ok}/{len(P)}")
    if n_ok != len(P):
        bad += 1
    n_move = sum(1 for r in P if MOVE in r[2])
    print(f"  bodies naming a MOVING ELEMENT                  {n_move}/{len(P)}")
    if n_move != len(P):
        print("  FAIL a dead-still plate makes a dead i2v clip"); bad += 1
    n_era = sum(1 for r in P if "1975 and 1982" in r[2])
    print(f"  bodies carrying the era clause                  {n_era}/{len(P)}")
    if n_era != len(P):
        bad += 1
    paper = [r for r in P if re.search(r"\b(paper|sheet|envelope|page|folder|ledger|book|"
                                       r"blotter|stamp)\b", r[2], re.I)]
    n_pap = sum(1 for r in paper if PAPER_GREY in r[2] or PAPER_BLANK in r[2]
                or "bare of any marking" in r[2] or "nothing figured on it" in r[2]
                or "nothing cut into it" in r[2] or "coins" in r[2])
    print(f"  paper-bearing plates with a POSITIVE paper rule {n_pap}/{len(paper)}")
    if n_pap != len(paper):
        print("   ", [r[0] for r in paper
                      if not (PAPER_GREY in r[2] or PAPER_BLANK in r[2]
                              or "bare of any marking" in r[2] or "nothing figured on it" in r[2]
                              or "nothing cut into it" in r[2] or "coins" in r[2])])
        bad += 1
    n_hand = [r for r in P if re.search(r"\bhands?\b", r[2], re.I)]
    n_flat = sum(1 for r in n_hand if FLAT_HAND in r[2] or "cropped at the shoulder" in r[2]
                 or "hands laid flat" in r[2] or "hand laid flat" in r[2])
    print(f"  hand plates using the flat-hand geometry        {n_flat}/{len(n_hand)}")
    if n_flat != len(n_hand):
        print("   ", [r[0] for r in n_hand
                      if not (FLAT_HAND in r[2] or "cropped at the shoulder" in r[2]
                              or "hands laid flat" in r[2] or "hand laid flat" in r[2])])
        bad += 1

    print("\nhazard scan over the POSITIVE bodies (a negated noun in the body reads as a request)")
    for w in HAZARD_WORDS:
        hits = [r[0] for r in P if w in r[2].lower()]
        if hits:
            print(f"  {w!r:24s} {len(hits)} {hits[:6]}")
            bad += 1
    print(f"  hazard words with zero hits: "
          f"{sum(1 for w in HAZARD_WORDS if not any(w in r[2].lower() for r in P))}"
          f"/{len(HAZARD_WORDS)}")

    print("\ninversion scan (a [NEG] token that bans what its own body asks for)")
    inv = []
    for pid, _act, body, neg_add, _line in P:
        low = body.lower()
        for tok in [t.strip().lower() for t in neg_add.split(",") if t.strip()]:
            if len(tok) >= 5 and tok in low:
                inv.append((pid, tok))
    print(f"  inverted [NEG] entries            {len(inv)} {inv[:6]}")
    if inv:
        bad += 1

    print("\nscript-line citations (must be verbatim in the canonical script v003)")
    sp = re.sub(r"\s+", " ", (PLANNING / "EP62_greene_script.en.v003.md")
                .read_text(encoding="utf-8").replace("*", ""))
    nf = []
    for pid, _act, _body, _neg, line in P:
        for piece in [p.strip(" .") for p in re.sub(r"\s+", " ", line).split(" ... ")]:
            if piece and piece not in sp:
                nf.append((pid, piece[:60]))
    print(f"  quoted fragments NOT found verbatim {len(nf)} {nf[:6]}")
    # not fatal: two plates cite a direction line, not spoken narration
    print("\npaste files")
    for name in sorted(files):
        print(f"  {name:16s} {files[name].count(chr(10) + '■ '):2d} prompts  "
              f"{len(files[name]):6d} bytes")
    print(f"  {OUT_ALL.name:16s} {merged.count(chr(10) + '■ '):2d} prompts  "
          f"{len(merged):6d} bytes")

    print("\n" + ("VERIFY: FAIL" if bad else "VERIFY: all measured checks pass"))
    return 1 if bad else 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--verify", action="store_true", help="verify only, write nothing")
    a = ap.parse_args()
    md = build_md()
    files = build_paste()
    merged = build_merged()
    if not a.verify:
        OUT_MD.write_text(md, encoding="utf-8", newline="\n")
        OUT_PASTE.mkdir(parents=True, exist_ok=True)
        for name, text in files.items():
            (OUT_PASTE / name).write_text(text, encoding="utf-8", newline="\n")
        OUT_ALL.write_text(merged, encoding="utf-8", newline="\n")
        print(f"wrote {OUT_MD}")
        print(f"wrote {len(files)} paste chunks to {OUT_PASTE}")
        print(f"wrote {OUT_ALL}")
    return verify(md, files, merged)


if __name__ == "__main__":
    raise SystemExit(main())
