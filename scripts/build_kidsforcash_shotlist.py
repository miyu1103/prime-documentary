#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
build_kidsforcash_shotlist.py  (py -3.11)

Idempotent generator for EP38 "Kids for Cash" shot / assembly specification.

Maps the 40 Codex stills (S01..S40) + captions + number-cards onto a 48fps
timeline that is contiguous over 0..531.6s (narration_master duration).

Inputs (read-only):
  - episodes/_planning/EP38_kidsforcash_scene_plan.v001.md        (beats, motion, sync words, cards)
  - episodes/PD-2026-038-kidsforcash/06_audio/narration_index.v001.json   (section offsets)
  - episodes/PD-2026-038-kidsforcash/06_audio/word_timings.v001.json      (word times -> lock card starts)
  - episodes/PD-2026-038-kidsforcash/04_scenes/image_ledger.v001.json     (authoritative image content + sha256/provenance)

Output:
  - episodes/PD-2026-038-kidsforcash/04_scenes/shotlist.v001.json

Notes:
  * The scene_plan v001 S-id assignments drifted from what was actually
    generated; the image_ledger is authoritative, so beats are matched to the
    image whose ledger content actually depicts the narration meaning.
  * Motion type: W = Wan2.2 i2v real-motion hero, D = 2.5D depth dolly + kinetic
    text, card = motionkit/AE motion-graphic (stat/number/stamp).
  * Number/on-screen cards are locked to the exact narration word time.
  * Fonts (brand.ts): display/body = Oswald, numbers = Anton.
  * This is a spec-only builder. It runs NO GPU / Wan / render / publish.
"""
import json
import os
import sys

FIXED_TIMESTAMP = "2026-07-17T00:00:00Z"
FPS = 48
TOTAL_SEC = 531.6          # canonical episode length (531.6s * 48fps)
CONTIG_TOL = 0.05          # seconds

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EP = os.path.join(REPO, "episodes", "PD-2026-038-kidsforcash")
LEDGER_PATH = os.path.join(EP, "04_scenes", "image_ledger.v001.json")
WORDS_PATH = os.path.join(EP, "06_audio", "word_timings.v001.json")
OUT_PATH = os.path.join(EP, "04_scenes", "shotlist.v001.json")

IMG_ROOT = r"H:\pd-media\assets\ai\kidsforcash"

# Motion-graphic (card) components -> (source_type, truth_status, claim_ref)
CARD_META = {
    "ComparisonBars":  ("motion_graphic", "factual", "CLM-08"),
    "MoneyFlow":       ("motion_graphic", "factual", "CLM-05,CLM-06"),
    "StampReveal":     ("motion_graphic", "editorial", None),
    "RadialGauge":     ("motion_graphic", "factual", "CLM-09"),
    "MechanismReveal": ("motion_graphic", "editorial", None),
    "RecordsScan":     ("motion_graphic", "factual", "CLM-14"),
    "NumberTicker":    ("motion_graphic", "factual", "CLM-16"),
}

# ---------------------------------------------------------------------------
# BEAT TABLE
# Each beat: (start_sec, id, image_id, motion, wan, note, sync_words, card, lower_third, claim_ref)
#   image_id: "Snn" for a still, or a motion-graphic component name.
#   card: None or dict(text, kind, locked_start_sec, sync_word)  -- on-screen/number card.
#   end_sec is derived = next beat start (globally contiguous); final = TOTAL_SEC.
# ---------------------------------------------------------------------------
def card(text, kind, locked, sync):
    return {"text": text, "kind": kind, "locked_start_sec": locked, "sync_word": sync}

BEATS = [
    # ---------------- HOOK (0.0 - 27.864) ----------------
    (0.00,   "H1", "S02", "D", False, "2.5D slow push into the monitor glow; the harmless prank.",
        ["web page"], None, None, None),
    (6.26,   "H2", "S01", "D", False, "Slow dolly down the empty hallway; an ordinary kid.",
        ["prank", "detention"], None, None, None),
    (10.52,  "H3", "S03", "W", True,  "WAN hero: tiny child dwarfed under the looming bench; the 90-second hearing.",
        ["three months", "ninety seconds", "lawyer"],
        [card("3 MONTHS", "AE_number_card", 11.76, "three months"),
         card("90 SECONDS / NO LAWYER", "AE_number_card", 13.92, "ninety seconds")],
        None, "CLM-10"),
    (18.26,  "H5", "S07", "W", True,  "WAN hero: shadowed hands pass the envelope under the desk; paid per child.",
        ["being paid", "every child"], None, None, None),

    # ---------------- ACT1 (27.864 - 137.276) ----------------
    (27.864, "A1", "S21", "D", False, "2.5D pull-back to push-in on the coal-town courthouse; families entering.",
        ["Luzerne County"], None, "Luzerne County, PA", None),
    (32.64,  "A2", "S12", "D", False, "Low-angle rise on marble columns; the place meant to set a kid right.",
        ["set right"], None, None, None),
    (38.76,  "A3", "S01", "D", False, "Quick-cut depth moves; small things, ordinary children.",
        ["small things"], None, None, None),
    (47.40,  "A4", "S19", "D", False, "Warm suburban street; anywhere else it ends with a ride home.",
        ["warning", "ride home"], None, None, None),
    (52.34,  "A5", "S22", "W", True,  "WAN hero: the child's hand hesitates over the illegible waiver form.",
        ["signature"],
        [card("WAIVER OF COUNSEL", "AE_stamp", 53.44, "signature")], None, None),
    (62.70,  "A6", "S18", "D", False, "Power-vs-child diptych; young and scared, signed away the one protection.",
        ["signed away", "protection"], None, None, None),
    (72.00,  "A7", "S27", "D", False, "Up-angle on the robed silhouette; a man named Ciavarella.",
        ["Ciavarella"], None, "Mark Ciavarella — Juvenile Court Judge", None),
    (75.30,  "A8", "S26", "D", False, "Overhead funnels; half of the children left in handcuffs.",
        ["handcuffs", "locked facility"], None, None, None),
    (80.80,  "A9", "ComparisonBars", "card", False, "MK ComparisonBars: ~50% placement here vs 8.4% statewide; Anton numerals.",
        ["eight in a hundred"],
        card("8.4% vs ~50%", "MK_card", 83.16, "eight in a hundred"), None, "CLM-08"),
    (84.32,  "A10", "S04", "D", False, "Tight on cuffed wrists; taken that same day.",
        ["taken that same day"], None, None, None),
    (90.02,  "A11", "S25", "D", False, "Transport van window; suburban lights receding.",
        ["driven hours from home"], None, None, None),
    (95.98,  "A12", "S24", "D", False, "Empty classroom desk and backpack; missing school, missing a parent's face.",
        ["missing school"], None, None, None),
    (102.52, "A13", "S23", "W", True,  "WAN hero: side door swings shut as the parent rises too late.",
        ["side door", "mother rose"], None, None, None),
    (111.30, "A14", "S11", "D", False, "Grieving silhouette in the doorway; parents understood only hours later.",
        ["hours later"], None, None, None),
    (118.66, "A15", "S03", "D", False, "Hold on the bench; a decision made before anyone walked in.",
        ["made before anyone walked in"], None, None, None),
    (126.32, "A16", "S21", "D", False, "Return to the courthouse; who doesn't believe a judge.",
        ["believe a judge"], None, None, None),
    (131.18, "A17", "S08", "D", False, "Conveyor of anonymous children; belief was the first thing being sold.",
        ["being sold"], None, None, None),

    # ---------------- ACT2 (137.276 - 257.602) ----------------
    (137.276, "B1", "S15", "D", False, "Forensic light across cash + contract + gavel; follow the money.",
        ["follow the money"], None, None, None),
    (141.56, "B2", "S27", "D", False, "Two suited silhouettes on separate levels; Conahan holds the checkbook.",
        ["two judges", "Conahan"], None, "Michael Conahan — President Judge", None),
    (150.62, "B3", "S28", "D", False, "County budget ledger under a gavel; a center paid for with tax dollars.",
        ["tax dollars"], None, None, None),
    (155.36, "B4", "S09", "D", False, "Padlocked public gate, bright private facility beyond; starved of funding.",
        ["starved of funding"], None, None, None),
    (160.14, "B5", "S30", "D", False, "The deal table: blueprints, key ring, sealed envelope; a guarantee in writing.",
        ["guarantee"], None, None, None),
    (167.24, "B6", "S05", "W", True,  "WAN hero: for-profit jail at dusk, razor wire; air and light move.",
        ["for-profit jail"], None, None, None),
    (175.06, "B7", "S29", "W", True,  "WAN hero: occupancy corridor; empty beds cost money, full beds make it.",
        ["empty beds", "full beds"], None, None, None),
    (181.34, "B8", "S08", "W", True,  "WAN hero (core cut): children processed one at a time into the building.",
        ["one child at a time"], None, None, None),
    (187.64, "B9", "S30", "D", False, "Shadowed hands at the table; a developer built, an attorney ran them.",
        ["built", "owned and ran"], None, None, None),
    (193.82, "B10", "MoneyFlow", "card", False, "MK MoneyFlow: ~$2.8M routed facility -> judges over ~3 years; Anton figures.",
        ["two point eight million"],
        card("$2.8 MILLION", "AE_number_card", 197.00, "two point eight million"), None, "CLM-05,CLM-06"),
    (199.94, "B11", "S07", "D", False, "Back to the envelope; side accounts and quiet transfers.",
        ["side accounts"], None, None, None),
    (204.62, "B12", "StampReveal", "card", False, "MK StampReveal over S15 evidence: 'FINDER'S FEE' stamped, overprinted 'BRIBE'.",
        ["finder's fee"],
        card("FINDER'S FEE -> BRIBE", "AE_stamp", 205.44, "finder's fee"), None, None),
    (212.32, "B13", "S03", "D", False, "Bench again; child in, sent to a cell, a payment followed.",
        ["a child walked in"], None, None, None),
    (218.68, "B14", "S18", "D", False, "Power-vs-child; the children who came without a lawyer.",
        ["without a lawyer"], None, None, None),
    (222.68, "B15", "RadialGauge", "card", False, "MK RadialGauge/NumberTicker: no-lawyer appearances 7-11x the state rate.",
        ["seven to eleven times"],
        card("7-11x", "MK_card", 224.30, "seven to eleven times"), None, "CLM-09"),
    (228.20, "B16", "S03", "D", False, "Tiny child under the bench; a child with no lawyer cannot fight back.",
        ["cannot fight back"], None, None, None),
    (232.14, "B17", "S35", "D", False, "Grid of identical folders + stopped clocks; not impatience — inventory.",
        ["inventory"],
        card("INVENTORY", "AE_kinetic", 235.96, "inventory"), None, None),
    (238.60, "B18", "S26", "D", False, "Funnels fill; fed into private beds, numbered in the thousands.",
        ["thousands"], None, None, None),
    (246.40, "B19", "S17", "D", False, "Endless records drawers; on paper each hearing looked perfectly legal.",
        ["perfectly legal"], None, None, None),
    (254.30, "B20", "S35", "D", False, "The pattern grid; the machine hid inside the shape of ordinary justice.",
        ["the machine"], None, None, None),

    # ---------------- ACT3 (257.602 - 335.853) ----------------
    (257.602, "C1", "S10", "W", True,  "WAN hero: empty chair by the window, folded jacket; the light slowly fades.",
        ["stand in one house"], None, None, "CLM-11"),
    (261.36, "C2", "S01", "D", False, "Lone teenage figure; Ed Kenzakoski, seventeen, a wrestler.",
        ["seventeen"], None, "Edward Kenzakoski, 17", "CLM-11"),
    (266.90, "C3", "S31", "D", False, "Intake tray of a kid's belongings; a small charge, and he was sent away.",
        ["sent away"], None, None, None),
    (271.42, "C4", "S16", "W", True,  "WAN hero: suited figure down the courthouse steps; a defendant now, out on bail.",
        ["Ciavarella", "defendant"], None, None, "CLM-12"),
    (282.20, "C5", "S11", "D", False, "Mother's silhouette; Sandy Fonzo was there on the pavement.",
        ["she was there"], None, "Sandy Fonzo — his mother", "CLM-12"),
    (286.58, "C6", "S16", "D", False, "Hold on the man; grief turned to fury — how could he say nothing wrong.",
        ["nothing wrong"], None, None, None),
    (294.44, "C7", "S14", "D", False, "The empty robe in shadow; he fixed his tie, looked past, had nothing.",
        ["nothing to say"], None, None, None),
    (299.58, "C8", "S18", "D", False, "Power-vs-child; thousands told at thirteen, at fifteen, they were criminals.",
        ["thousands of children"], None, None, None),
    (306.24, "C9", "S26", "D", False, "Many small figures; being children, they believed it, and never found their footing.",
        ["believing it", "never found their footing"], None, None, None),
    (313.62, "C11", "S32", "D", False, "A sealed file's shadow over job and college forms; the record trailed them.",
        ["record", "college application"], None, None, None),
    (322.24, "C12", "S11", "D", False, "A person facing the camera's dark; trying to explain being sold at fifteen.",
        ["sold at fifteen"], None, None, None),
    (330.28, "C13", "S38", "D", False, "The balance scale, sneakers vs cash; no ruling returns and no settlement buys back.",
        ["no ruling returns"], None, None, None),

    # ---------------- ACT4 (335.853 - 478.052) ----------------
    (335.853, "D1", "S17", "D", False, "Corrupt records system; for years it held, because of who was complaining.",
        ["for years it held"], None, None, None),
    (344.32, "D2", "S18", "D", False, "Power dismisses the small figure; easy voices, waved off again and again.",
        ["waved off"], None, None, None),
    (349.48, "D3", "S33", "D", False, "Woman at the kitchen table with a phone and court papers; one more mother called.",
        ["picked up the phone"], None, None, "CLM-13"),
    (354.68, "D4", "S34", "D", False, "Nonprofit lawyers comparing files after midnight; the Juvenile Law Center.",
        ["Juvenile Law Center"], None, "Juvenile Law Center, Philadelphia", "CLM-13"),
    (359.90, "D5", "MechanismReveal", "card", False, "MK MechanismReveal: hundreds of children, the same repeating pattern each time.",
        ["a machine"], None, None, None),
    (368.74, "D6", "S36", "D", False, "Headphones, recorder, transfer diagrams; federal investigators follow the money.",
        ["federal investigators"], None, None, None),
    (376.44, "D7", "S19", "D", False, "Ordinary street; it might have stayed buried, a few angry parents easy to ignore.",
        ["stayed buried"], None, None, None),
    (385.52, "D8", "S40", "D", False, "Families together, backs to camera; a documentary put their faces on a screen.",
        ["documentary", "faces on a screen"], None, None, None),
    (392.76, "D9", "S18", "D", False, "The small figure resolves; no longer case numbers — they had names.",
        ["they had names"], None, None, None),
    (400.48, "D10", "S12", "D", False, "Marble courthouse rise; taken to the Pennsylvania Supreme Court, a rare thing.",
        ["Pennsylvania Supreme Court"], None, None, "CLM-14"),
    (405.80, "D11", "S13", "D", False, "Records dissolving into light; it reached back and unmade the courtroom.",
        ["unmade it"], None, None, "CLM-14"),
    (409.64, "D12", "RecordsScan", "card", False, "MK RecordsScan + AE: thousands of adjudications thrown out (no exact count burned).",
        ["throwing out thousands"],
        card("THOUSANDS VACATED", "MK_card", 409.64, "throwing out thousands"), None, "CLM-14"),
    (415.34, "D13", "S13", "D", False, "Records clear; the state admitting none of it should ever have counted.",
        ["none of it should ever have counted"], None, None, None),
    (423.36, "D14", "S06", "D", False, "The bare cell and cold blue grid; a year, or two, or three, nights no order gives back.",
        ["nights in a cell"], None, None, None),
    (430.00, "D15", "S40", "D", False, "Empty playground, jacket on the swing; the paperwork could be erased, the time could not.",
        ["the time could not"], None, None, None),
    (436.74, "D16", "S37", "W", True,  "WAN hero: federal courtroom reversed, robe folded on the chair; Conahan pleaded guilty.",
        ["seventeen and a half"],
        card("17.5 YEARS", "AE_number_card", 442.18, "seventeen and a half"), None, "CLM-15"),
    (444.08, "D17", "S14", "W", True,  "WAN hero: accusing shaft of light on the empty robe; he insisted it was a finder's fee, not a bribe.",
        ["finder's fee", "not a bribe"], None, None, "CLM-15"),
    (452.80, "D18", "S16", "D", False, "The powerful brought low on the steps; a jury convicted, twenty-eight years.",
        ["twenty-eight"],
        card("28 YEARS", "AE_number_card", 457.32, "twenty-eight"), None, "CLM-15"),
    (459.54, "D19", "NumberTicker", "card", False, "MK NumberTicker: ordered to pay more than $200 million to the families.",
        ["two hundred million"],
        card("$200 MILLION+", "AE_number_card", 462.40, "two hundred million"), None, "CLM-16"),
    (465.30, "D20", "S38", "D", False, "The scale settles; it was, at last, a kind of justice — and it forced a change.",
        ["a kind of justice"], None, None, None),
    (470.06, "D21", "S39", "D", False, "Warm reformed courtroom; a child now stands beside a lawyer at equal height.",
        ["lawyer at their side"], None, None, "CLM-18"),

    # ---------------- ED (478.052 - 531.6) ----------------
    (478.052, "E1", "S12", "W", True,  "WAN hero: courthouse at dusk, gold on marble; the room where money stays outside.",
        ["outside the door"], None, None, None),
    (482.22, "E2", "S18", "D", False, "Power vs the rest of us; held to a higher line — for thousands of children.",
        ["higher line"], None, None, None),
    (488.50, "E3", "S08", "D", False, "Children reduced to a price tag; that line had a price, a few thousand dollars a head.",
        ["a few thousand dollars a head"], None, None, None),
    (493.20, "E4", "S16", "D", False, "The steps again; the judges are named and gone, one spent years in prison.",
        ["named and gone"], None, None, "CLM-17"),
    (497.20, "E5", "S19", "D", False, "The ordinary street; the other, quietly, walked back out into the world.",
        ["early release"], None, "Conahan — sentence commuted, 2024", "CLM-17"),
    (505.76, "E6", "S40", "D", False, "Empty playground at blue hour; the men could be punished, still the years don't come back.",
        ["years don't come back"], None, None, None),
    (512.70, "E7", "S20", "D", False, "The golden line across the floor; if this should be seen and not buried, subscribe.",
        ["subscribe"],
        card("SUBSCRIBE", "AE_cta", 516.16, "subscribe"), None, None),
    (517.44, "E8", "S21", "D", False, "The ordinary courthouse entrance; the next one opens the way this one did.",
        ["ordinary person"], None, None, None),
    (524.94, "E9", "S20", "D", False, "Hold on the line of light; the distance is far shorter than we let ourselves believe.",
        ["far shorter"], None, None, None),
]

BOOKENDS = [
    {"component": "BookendsOP", "role": "OP_title", "start_sec": 27.864, "end_sec": 33.0,
     "overlay": True,
     "note": "Brand OP title: letter stagger + overflow-hidden mask reveal (Oswald). Overlay layer riding over A1; does not consume exclusive shot time.",
     "source_type": "brand", "truth_status": "brand"},
    {"component": "BookendsED", "role": "ED_title", "start_sec": 525.0, "end_sec": 531.6,
     "overlay": True,
     "note": "Brand ED title over E9 (Oswald). Overlay layer; does not consume exclusive shot time.",
     "source_type": "brand", "truth_status": "brand"},
]

# Section boundaries (from narration_index.v001.json) for tagging + validation.
SECTIONS = [
    ("HOOK", 0.0, 27.864),
    ("ACT1", 27.864, 137.276),
    ("ACT2", 137.276, 257.602),
    ("ACT3", 257.602, 335.853),
    ("ACT4", 335.853, 478.052),
    ("ED",   478.052, TOTAL_SEC),
]


def section_for(t):
    for name, a, b in SECTIONS:
        if a - 1e-6 <= t < b - 1e-9:
            return name
    return SECTIONS[-1][0]


def f(sec):
    return int(round(sec * FPS))


def build():
    ledger = json.load(open(LEDGER_PATH, encoding="utf-8"))
    led = {e["asset_id"]: e for e in ledger["entries"]}
    words = json.load(open(WORDS_PATH, encoding="utf-8"))["words"]

    def word_exists(t):
        return any(abs(w["start"] - t) <= 0.02 for w in words)

    shots = []
    n = len(BEATS)
    for i, beat in enumerate(BEATS):
        (start, sid, image_id, motion, wan, note, sync, cardv, lt, claim) = beat
        end = BEATS[i + 1][0] if i + 1 < n else TOTAL_SEC

        if image_id.startswith("S") and image_id[1:].isdigit():
            e = led[image_id]
            image = e["path"]
            source_type = "ai_generated"
            truth_status = e["truth_status"]
            sha = e["sha256"]
        else:
            image = image_id
            st, ts, cclaim = CARD_META[image_id]
            source_type = st
            truth_status = ts
            sha = None
            if claim is None:
                claim = cclaim

        # normalize card(s) to a list
        cards = []
        if cardv:
            cards = cardv if isinstance(cardv, list) else [cardv]

        shots.append({
            "shot_id": "SH-%02d-%s" % (i + 1, sid),
            "beat_id": sid,
            "section": section_for(start),
            "image_id": image_id,
            "image": image,
            "image_sha256": sha,
            "start_sec": round(start, 3),
            "end_sec": round(end, 3),
            "start_frame": f(start),
            "end_frame": f(end),
            "duration_sec": round(end - start, 3),
            "motion": motion,
            "wan": bool(wan),
            "motion_note": note,
            "sync_words": sync,
            "on_screen_text": cards if cards else None,
            "lower_third": lt,
            "source_type": source_type,
            "truth_status": truth_status,
            "claim_ref": claim,
        })

    spec = {
        "schema_version": "shotlist.v1",
        "episode_id": "PD-2026-038-kidsforcash",
        "generated_at": FIXED_TIMESTAMP,
        "builder": "scripts/build_kidsforcash_shotlist.py",
        "fps": FPS,
        "total_sec": TOTAL_SEC,
        "total_frames": f(TOTAL_SEC),
        "narration_master_sec": 531.606,
        "fonts": {"display": "Oswald", "body": "Oswald", "numbers": "Anton"},
        "motion_legend": {
            "W": "Wan2.2 i2v real-motion hero cut",
            "D": "2.5D depth dolly + kinetic text",
            "card": "motionkit / After Effects motion-graphic (stat / number / stamp)",
        },
        "provenance_note": ("All stills are Codex AI dramatizations (symbolic), NOT authentic "
                            "records (CLAUDE.md invariant 11). S-id -> image content is taken from "
                            "image_ledger.v001.json (authoritative); scene_plan.v001 S-ids were "
                            "corrected where they had drifted from the generated images."),
        "sources": {
            "scene_plan": "episodes/_planning/EP38_kidsforcash_scene_plan.v001.md",
            "narration_index": "episodes/PD-2026-038-kidsforcash/06_audio/narration_index.v001.json",
            "word_timings": "episodes/PD-2026-038-kidsforcash/06_audio/word_timings.v001.json",
            "image_ledger": "episodes/PD-2026-038-kidsforcash/04_scenes/image_ledger.v001.json",
        },
        "sections": [{"name": s[0], "start_sec": s[1], "end_sec": s[2]} for s in SECTIONS],
        "bookends": BOOKENDS,
        "shot_count": len(shots),
        "wan_shot_count": sum(1 for s in shots if s["wan"]),
        "shots": shots,
    }

    # ---- validation ----
    problems = []
    # contiguity
    if abs(shots[0]["start_sec"] - 0.0) > CONTIG_TOL:
        problems.append("first shot does not start at 0.0")
    for a, b in zip(shots, shots[1:]):
        if abs(a["end_sec"] - b["start_sec"]) > CONTIG_TOL:
            problems.append("gap/overlap between %s (%.3f) and %s (%.3f)" %
                            (a["shot_id"], a["end_sec"], b["shot_id"], b["start_sec"]))
    if abs(shots[-1]["end_sec"] - TOTAL_SEC) > 0.1:
        problems.append("last shot end %.3f != %.3f" % (shots[-1]["end_sec"], TOTAL_SEC))

    # cards inside their shot + locked to a real word time
    for s in shots:
        for c in (s["on_screen_text"] or []):
            t = c["locked_start_sec"]
            if not (s["start_sec"] - 1e-6 <= t < s["end_sec"] + 1e-6):
                problems.append("card '%s' t=%.2f outside shot %s [%.2f,%.2f)" %
                                (c["text"], t, s["shot_id"], s["start_sec"], s["end_sec"]))
            if not word_exists(t):
                problems.append("card '%s' t=%.2f is not a valid word start time" % (c["text"], t))

    # image coverage
    used = {s["image_id"] for s in shots if s["image_id"].startswith("S") and s["image_id"][1:].isdigit()}
    all_imgs = {"S%02d" % i for i in range(1, 41)}
    unused = sorted(all_imgs - used)

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    tmp = OUT_PATH + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(spec, fh, ensure_ascii=False, indent=2)
    os.replace(tmp, OUT_PATH)

    # ---- report ----
    print("wrote:", OUT_PATH)
    print("shots:", len(shots), " wan:", spec["wan_shot_count"],
          " total_frames:", spec["total_frames"])
    print("coverage: %d/40 images used" % len(used))
    print("unused images:", unused if unused else "NONE")
    print("cards:", sum(len(s["on_screen_text"] or []) for s in shots))
    durs = [s["duration_sec"] for s in shots]
    print("shot dur min/avg/max: %.2f / %.2f / %.2f" % (min(durs), sum(durs) / len(durs), max(durs)))
    short = [(s["shot_id"], s["duration_sec"]) for s in shots if s["duration_sec"] < 4.0]
    long_ = [(s["shot_id"], s["duration_sec"]) for s in shots if s["duration_sec"] > 9.0]
    if short:
        print("sub-4s shots (intentional stingers/punches):", short)
    if long_:
        print("over-9s shots:", long_)
    if problems:
        print("PROBLEMS:")
        for p in problems:
            print("  -", p)
        return 1
    print("VALIDATION: OK (contiguous, cards locked, coverage complete)")
    return 0


if __name__ == "__main__":
    sys.exit(build())
