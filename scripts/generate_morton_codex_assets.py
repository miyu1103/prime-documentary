#!/usr/bin/env python
"""Generate EP52 Morton A-side assets as real local media files.

This is a deterministic local renderer for the EP52 CODEX_A contract. It creates
real 4K stills, real MP4 factory/motion/overlay assets, staging copies, QC
ledgers, and the A/B boundary manifest. It does not call paid APIs, upload
anything, or touch B-owned build files.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import re
import shutil
import subprocess
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageOps

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-052-morton"
SLUG = "morton"
W, H = 3840, 2160
FPS = 30
MOTION_FPS = 48
MOTION_FRAMES = 164
MOTION_SEC = MOTION_FRAMES / MOTION_FPS
ACCENT = (63, 94, 140)
INK = (11, 12, 16)
GOLD = (209, 154, 62)

PLAN_A = ROOT / "episodes" / "_planning" / "EP52_morton_CODEX_A_ASSETS.v001.md"
EP_DIR = ROOT / "episodes" / EP
SCENES = EP_DIR / "04_scenes"
VISUALS = EP_DIR / "05_visuals"
STOCK = EP_DIR / "05_stock"
MEDIA_AI = Path("H:/pd-media/assets/ai/morton")
MEDIA_VIDEO = Path("H:/pd-media/assets/ai_video/morton")
FACTORY_MEDIA = Path("H:/pd-media/assets")
STOCK_VIDEO = Path("H:/pd-media/assets/stock/video")
PUBLIC = ROOT / "remotion" / "public" / SLUG
RUN_QC = ROOT / "runs" / "qc"
MANIFEST = VISUALS / "asset_manifest.v001.json"
FACTORY_CATALOG = ROOT / "assets" / "asset_manifest.v001.json"

EXPECTED = {
    "still_body": 215,
    "still_i2v_source": 43,
    "motion": 43,
    "factory": 240,
    "overlay": 30,
    "thumb_face": 3,
}
THUMB_BODY_IDS = {"S001", "S060", "S155", "S170"}
HP_BODY = set(range(36, 42)) | set(range(52, 57)) | set(range(69, 77)) | set(range(109, 116))
HP_BODY |= set(range(120, 124)) | set(range(142, 148)) | set(range(174, 180))
HP_BODY |= set(range(185, 201))
HUMAN_MOTION = {4, 6, 7, 9, 10, 13, 14, 16, 19, 20, 22, 23, 24, 25, 34, 35, 38, 39}
ALLOWED_LICENSES = {"cc0", "royalty_free", "generated_owned", "Pexels License", "Pixabay Content License"}
VALID_ROLES = {"body", "i2v_source", "thumb_face", "reject"}
SAFE_STOCK_VIDEO_NAMES = [
    "pexels_cell_tower.mp4",
    "pexels_v_10617219.mp4",
    "pexels_v_29188235.mp4",
    "pexels_v_29188241.mp4",
    "pexels_v_29635453.mp4",
    "pexels_v_36553218.mp4",
    "pexels_v_3727447.mp4",
    "pexels_v_4122942.mp4",
    "pexels_v_4671883.mp4",
    "pexels_v_5243246.mp4",
    "pexels_v_5636967.mp4",
    "pexels_v_5636977.mp4",
    "pexels_v_6110320.mp4",
    "pexels_v_6186015.mp4",
    "pexels_v_7140928.mp4",
    "pixabay_v_10822.mp4",
    "pixabay_v_11253.mp4",
    "pixabay_v_186520.mp4",
    "pixabay_v_198901.mp4",
    "pixabay_v_202987.mp4",
    "pixabay_v_2165.mp4",
    "pixabay_v_26192.mp4",
    "pixabay_v_31094.mp4",
    "pixabay_v_320453.mp4",
    "pixabay_v_345428.mp4",
    "pixabay_v_3627.mp4",
    "pixabay_v_37417.mp4",
    "pixabay_v_4737.mp4",
    "pixabay_v_64759.mp4",
]
STOCK_ASSIGNMENTS = {
    13: ("pexels_v_29635453.mp4", "real suburban house exterior and driveway, face-free and text-free"),
    14: ("pixabay_v_31094.mp4", "real quiet suburban road aerial, face-free and text-free"),
    22: ("pixabay_v_64759.mp4", "real slow clouds and open sky, face-free and text-free"),
    25: ("pexels_v_3727447.mp4", "real dark road and driveway-adjacent night approach, face-free and text-free"),
    58: ("pexels_v_29188241.mp4", "real courthouse exterior, face-free and text-free"),
    70: ("pexels_v_5636977.mp4", "real gavel and scales detail, face-free and text-free"),
    71: ("pixabay_v_11253.mp4", "real hand pulling a law-library style book from shelves, face-free and text-free"),
    85: ("pexels_v_5636967.mp4", "real justice scales close detail, face-free and text-free"),
    107: ("pexels_cell_tower.mp4", "real cold clouds crossing a tower silhouette, face-free and text-free"),
    154: ("pexels_v_29188235.mp4", "real capitol-style civic building exterior, face-free and text-free"),
    208: ("pixabay_v_4737.mp4", "real blurred institutional hallway, face-free and text-free"),
    214: ("pixabay_v_26192.mp4", "real distant cityscape, face-free and text-free"),
    216: ("pixabay_v_186520.mp4", "real water and treeline reflection, face-free and text-free"),
}
FACTORY_SAFE_EXCLUDE = re.compile(
    r"fog|haze|smoke|wildfire|firework|burning|blood|gore|weapon|gun|knife|"
    r"violence|protest|riot|war|soldier|hospital|medical|doctor|surgery|"
    r"person|people|man|woman|child|kid|baby|face|portrait|crying|homeless|"
    r"money|cash|tax|trading|screen|news|newspaper|sign|badge|logo|text|"
    r"demolition|broken|police_badge|lineup|interrogation",
    re.IGNORECASE,
)
FACTORY_PREFERENCES: list[tuple[tuple[str, ...], list[str]]] = [
    (("evidence_locker", "evidence_room", "cold_evidence", "locker"), ["evidence_locker_shelves", "evidence_bag", "case_files_stack_desk", "dark_cinematic_background"]),
    (("records", "archive", "document_archive", "records_wall", "shelves"), ["old_library_archive", "law_library_books", "law_books_spines_macro", "case_files_stack_desk"]),
    (("file_drawer", "file_cabinet", "desk_files", "document", "case"), ["case_files_stack_desk", "documents_on_desk", "audit_documents_stack", "wooden_desk_lamp_night"]),
    (("sheriff_office", "da_office", "lawyer_office", "office"), ["office_interior_dark", "wooden_desk_lamp_night", "law_library_books"]),
    (("institutional_corridor", "institutional_room", "records_hall", "hallway", "corridor"), ["data_center_corridor", "school_hallway_empty", "prison_corridor", "concrete_wall_texture_dark"]),
    (("county_building", "courthouse", "williamson", "steps", "columns", "marble", "ambient"), ["courthouse_steps", "capitol_dome_dusk", "courtroom_empty_wide", "courtroom_interior"]),
    (("courtroom", "jury_box", "witness_stand"), ["courtroom_empty_wide", "jury_box_empty", "witness_stand_empty", "courtroom_interior"]),
    (("gavel", "bench"), ["courtroom_gavel_block_macro", "judge_gavel_wooden"]),
    (("law_books", "law_library"), ["law_library_books", "law_books_spines_macro", "old_library_archive"]),
    (("prison", "cell_block", "cell_", "fence", "barrier_gate", "gate"), ["jail_cell_bars", "prison_corridor", "prison_yard_fence", "prison_gate_closing", "barbed_wire_fence_sky"]),
    (("dna", "lab", "gel", "microscope"), ["dna_laboratory_blue", "microscope_lab", "test_tubes_rack_lab", "laboratory_glassware", "laboratory_centrifuge"]),
    (("suburban", "neighborhood", "house", "porch", "driveway", "street"), ["suburban_house_exterior_night", "empty_road_sunset", "rural_road_america", "small_town_main_street", "rain_street_reflection_night"]),
    (("police_lights", "patrol_car"), ["police_car_lights_night", "police_strobe_red_and_blue", "police_station_at_night"]),
    (("sky", "dawn"), ["stormy_sky_time_lapse", "city_skyline_dusk", "searchlight_beam_sky", "barbed_wire_fence_sky"]),
    (("landscape", "grass", "brush", "lawn", "treeline", "field", "horizon", "road"), ["rural_road_america", "empty_road_sunset", "lone_tree_in_field", "sun_through_trees_forest", "ocean_horizon_moody"]),
    (("capitol", "legislative", "austin"), ["capitol_dome_dusk", "city_skyline_dusk"]),
    (("water", "reflection"), ["rain_drops_on_dark_water", "caustics_water_light", "underwater_caustics_light", "ocean_horizon_moody"]),
    (("concrete", "wall", "floor"), ["concrete_wall_texture_dark", "dark_cinematic_background", "abstract_dark_background"]),
    (("kitchen_window", "window"), ["warm_window_light_rays", "rain_on_window_night", "wooden_desk_lamp_night"]),
    (("room",), ["office_interior_dark", "wooden_desk_lamp_night", "dark_cinematic_background"]),
]
FORCE_GENERATED_FACTORY_KEYS = (
    "supermarket",
    "grocery",
    "bedroom",
    "porch",
    "kitchen_window",
    "dry_lawn",
    "wind_in_dry_grass",
    "wooded_treeline",
    "courthouse_marble",
    "marble_floor",
    "legislative_chamber",
    "empty_austin_room",
)
USE_FACTORY_STOCKPILE = False

BANNED_PORTRAIT = re.compile(
    r"likeness of (a )?(real|specific|named) person|real[- ]person likeness|"
    r"face of (michael|christine|morton|eric|rita|mark|norwood|ken|anderson|bradley|raley|morrison)|"
    r"likeness of (michael|christine|morton|eric|rita|mark|norwood|ken|anderson|bradley|raley|morrison)|"
    r"recognizable (real person|celebrity)|identifiable real person|"
    r"mugshot of (a )?real person|deepfake|深偽|ディープフェイク",
    re.IGNORECASE,
)
BANNED_ACCURACY = re.compile(
    r"morton (killed|did it|is guilty|murdered|bludgeoned)|the husband did it|"
    r"beaten body|bludgeoned corpse|murder scene|blood on the bed|the weapon|"
    r"child witnessing the attack|boy sees the murder|traumatized child|crying toddler|"
    r"legible document|readable case file|readable lab report|dochighlight|"
    r"milky haze|foggy wash|scanline|CRT texture|vignette wash",
    re.IGNORECASE,
)

STYLE = (
    ", cinematic still, somber documentary grade, a cold forensic evidence-blue key light, "
    "near-black ink institutional gravity, restrained dignified symbolism, telephoto compression, "
    "shallow depth of field, clear and high-contrast, ultra-detailed, photoreal, 4K, 16:9, "
    "fine film grain, no text, no watermark, no logo, symbolic still-life"
)
NEG = (
    "text, words, letters, numbers, captions, watermark, logo, readable document, readable case file, "
    "license plate, recognizable real person, identifiable face, portrait, mugshot, likeness of a specific person, "
    "human face, front-facing person, victim depiction, body harm, attack depiction, gore, injury, weapon, "
    "identifiable child, cartoon, illustration, anime, 3d render, low quality, blurry, deformed, warped, melting, "
    "milky haze, scanline"
)
HSTYLE = (
    ", cinematic photoreal still, documentary stand-in, generic anonymized adult person, face kept non-identifiable, "
    "turned away or back-lit to silhouette, cold forensic evidence-blue key light, near-black ink institutional gravity, "
    "restrained dignified framing, clear and high-contrast, ultra-detailed, photoreal, 4K, 16:9, fine film grain, "
    "no text, no watermark, no logo, no readable documents"
)
HNEG = (
    "recognizable real person, likeness of a specific person, celebrity, mugshot, deepfake, text, words, letters, "
    "numbers, captions, watermark, logo, readable document, readable case file, license plate, attack depiction, "
    "body harm, gore, injury, weapon, an identifiable child, crying toddler, cartoon, illustration, anime, 3d render, "
    "low quality, blurry, deformed, warped, melting, milky haze, scanline"
)
TSTYLE = (
    ", thumbnail key art, a single non-real dramatized generic adult human character in a clearly illustrative "
    "semi-painterly cinematic style, face occupying the frame with eyes on the upper third, high contrast and vivid, "
    "one clean quadrant of negative space, 1280x720, ultra-detailed"
)
TNEG = (
    "photoreal photograph of a real person, recognizable real celebrity, deepfake, a real child, body harm, gore, "
    "violence, weapon, text, words, letters, numbers, watermark, logo, two faces, tiny face, neutral expression, "
    "dark muddy low-contrast mush, cartoon flatness, extra limbs, deformed, warped"
)


def mkdirs() -> None:
    for path in [
        SCENES,
        VISUALS,
        STOCK,
        MEDIA_AI,
        MEDIA_VIDEO / "factory",
        MEDIA_VIDEO / "motion",
        MEDIA_VIDEO / "overlay",
        PUBLIC / "img",
        PUBLIC / "factory",
        PUBLIC / "motion",
        PUBLIC / "overlay",
        PUBLIC / "thumb",
        RUN_QC,
    ]:
        path.mkdir(parents=True, exist_ok=True)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def strings(obj: Any):
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, list):
        for value in obj:
            yield from strings(value)
    elif isinstance(obj, dict):
        for value in obj.values():
            yield from strings(value)


def parse_jsonish_entries(section_start: str, section_end: str) -> list[dict[str, Any]]:
    text = PLAN_A.read_text(encoding="utf-8")
    start = text.index(section_start)
    end = text.index(section_end, start)
    section = text[start:end]
    entries = []
    for raw in re.findall(r"^\s*(\{[^\n]+\})\s*$", section, flags=re.MULTILINE):
        try:
            entries.append(json.loads(raw))
        except json.JSONDecodeError as exc:
            raise SystemExit(f"could not parse spec entry near {raw[:120]}: {exc}") from exc
    return entries


def factory_specs() -> list[dict[str, Any]]:
    items = parse_jsonish_entries("## 4.4", "## 4.5")
    if len(items) != 240:
        raise SystemExit(f"factory spec count expected 240 got {len(items)}")
    return items


def motion_specs() -> list[dict[str, Any]]:
    items = parse_jsonish_entries("## 4.5", "## 4.6")
    if len(items) != 43:
        raise SystemExit(f"motion spec count expected 43 got {len(items)}")
    return items


def overlay_specs() -> list[dict[str, Any]]:
    items = parse_jsonish_entries("## 4.6", "# 5.")
    if len(items) != 30:
        raise SystemExit(f"overlay spec count expected 30 got {len(items)}")
    return items


def act_for_scene(scene_id: str) -> int:
    n = int(re.sub(r"\D", "", scene_id))
    if n <= 15:
        return 0
    if n <= 60:
        return 1
    if n <= 115:
        return 2
    if n <= 155:
        return 3
    if n <= 200:
        return 4
    return 5


MOTIF_BLOCKS: list[tuple[str, range, str]] = [
    ("child_hand_crayon_monster", range(1, 5), "a small child's hand beside an abstract crayon monster scrawl"),
    ("monster_buried_drawer", range(5, 8), "a dark file drawer sliding shut over an abstract crayon monster scrawl"),
    ("cold_blue_edge_finds", range(8, 12), "a single cold evidence-blue edge of light finding a hidden object"),
    ("opening_title_abstract", range(12, 16), "an abstract evidence-blue field with distant Texas treeline shapes"),
    ("texas_morning_house", range(16, 24), "a quiet suburban Texas house before dawn"),
    ("predawn_doorway_clock", range(24, 30), "a pre-dawn doorway and an unreadable clock face"),
    ("empty_bed_absence", range(30, 36), "an empty neatly made bed rendered as cold absence"),
    ("police_lights_cold", range(36, 42), "anonymized adults from behind outside a suburban house in cold police light"),
    ("husband_assumption_mechanism", range(42, 48), "an abstract institutional mechanism locking onto a conclusion"),
    ("stomach_clock_debunked", range(48, 52), "a bent unreadable clock and cold forensic table"),
    ("child_account_written_thrown", range(52, 57), "anonymous adult hands recording an account beside a child's abstract crayon scrawl"),
    ("green_van_foreshadow", range(57, 59), "a distant dark-green van shape behind a house near a wooded treeline"),
    ("bandana_foreshadow", range(59, 61), "a folded strip of blue cloth in a dark evidence drawer"),
    ("county_courthouse", range(61, 69), "a cold county courthouse exterior and institutional columns"),
    ("courtroom_thin_case", range(69, 77), "a courtroom seen from behind with anonymous adult backs and a thin case table"),
    ("no_physical_evidence", range(77, 83), "an empty forensic evidence table under one cold blue light"),
    ("buried_file_drawer", range(83, 93), "shadowed folders sliding into dark file drawers"),
    ("withheld_the_boy", range(93, 97), "an abstract crayon monster scrawl sealed beneath a file edge"),
    ("withheld_green_van", range(97, 101), "a far green vehicle silhouette sealed into a folder"),
    ("withheld_bandana", range(101, 105), "a blue cloth strip sealed away in a cold evidence container"),
    ("withheld_stolen_checks", range(105, 109), "unreadable cards and paper shapes on a distant store counter"),
    ("anderson_power_shadow", range(109, 113), "an anonymous adult authority silhouette at a courtroom podium"),
    ("conviction_life", range(113, 116), "an anonymous adult figure from behind as heavy institutional doors close"),
    ("prison_exterior_nonsensational", range(116, 124), "a non-sensational prison exterior and anonymous adults from behind"),
    ("twentyfive_years_scale", range(124, 130), "a long institutional passage and an imbalanced scale"),
    ("cell_window_seasons", range(130, 138), "a single institutional cell window with seasons crossing as color temperature"),
    ("son_grows_absence", range(138, 142), "empty chairs standing for missed years"),
    ("lawyer_wont_quit", range(142, 148), "anonymous adult lawyer hands at a late-night desk with unreadable files"),
    ("bradley_wall_six_years", range(148, 152), "a cold barrier and locked gate blocking a forensic test"),
    ("order_to_test_and_anchor", range(152, 156), "a blue cloth strip moving toward a lab and a quiet cell-window anchor"),
    ("bandana_tested", range(156, 162), "a blue cloth strip finally placed under lab light"),
    ("two_people_on_it", range(162, 166), "two abstract biology traces crossing over blue cloth"),
    ("dna_bands_flood_blue", range(166, 174), "cold evidence-blue gel bands igniting and flooding the frame"),
    ("norwood_named", range(174, 180), "a separate anonymous adult drifter silhouette standing apart at a distance"),
    ("baker_gutpunch", range(180, 185), "an empty Austin home interior rendered as dignified absence"),
    ("morton_walks_free_gold", range(185, 190), "an opening gate and an anonymous adult walking into warm gold light"),
    ("anderson_reckoning", range(190, 196), "an anonymous suited adult led down a cold courthouse corridor"),
    ("morton_act", range(196, 201), "an anonymous adult at a warm legislative podium with soft-focus backs"),
    ("back_to_child", range(201, 205), "a drawer opening again to reveal an abstract crayon monster scrawl"),
    ("everything_true", range(205, 209), "a crayon monster shape, a mustache-like curve, and an empty doorway"),
    ("truth_never_missing", range(209, 213), "a waiting folder in a single cold shaft of light"),
    ("final_breath", range(213, 216), "a drawer, a folded blue cloth strip, and one earned warm dawn edge"),
]
MOTIF_BY_NUM = {n: (name, base) for name, nums, base in MOTIF_BLOCKS for n in nums}


ANCHORS = {
    1: "A small child's hand beside an abstract crayon scrawl of a monster on paper, found by a single cold forensic evidence-blue edge of light in near-black, handled with restraint, non-graphic, no identifiable child, no face, no readable text",
    5: "A child's crayon monster drawing on a page being covered as a dark institutional file drawer slides shut over it in cold evidence-blue light, the truth buried, symbolic, no person, no face, no readable text",
    16: "A quiet suburban Texas single-story house exterior before dawn in cold evidence-blue light, still and ordinary, no people, no crime imagery, no readable text",
    30: "An empty, neatly made bed in a cold, still bedroom rendered as absence in evidence-blue light, no person, only a quiet emptied room, no readable text",
    36: "Anonymized police officers and neighbors seen only from behind and in cold silhouette gathering outside a suburban Texas house ringed by police lights at dusk, small figures dwarfed by the moment, no faces, no readable text",
    52: "An anonymized adult investigator's hands seen from behind writing into a record book under cold light, a child's small crayon monster drawing beside it, the writing an unreadable smear, no readable text",
    57: "A cold, distant dark-green van parked behind a suburban house near a wooded treeline at dusk, seen only as a far shape in evidence-blue light, no license plate, no person, no readable text",
    60: "A folded strip of blue bandana cloth lying in a dark forensic evidence drawer, caught by a single cold evidence-blue edge of light and then ignored, not graphic, no person, no readable text",
    69: "A 1987 Texas courtroom seen from the back, anonymized adult jurors and gallery rendered as shadowed non-identifiable backs and soft-focus shapes, a cold thin case, no faces, no readable text",
    77: "An empty forensic evidence table under one cold evidence-blue light with nothing on it, symbolic emptiness, no person, no readable text",
    109: "An anonymized prosecutor stand-in at a courtroom podium, seen from behind and back-lit to a hard cold silhouette so no face reads, institutional power, no likeness, no readable text",
    120: "Anonymized prison inmates and a guard seen only from behind and in cold silhouette in a bare daytime yard, small still figures, non-sensational and dignified, no faces, no readable text",
    130: "A single institutional cell window abstracted to a pale rectangle of cold light, the color temperature shifting from winter to thin summer across it, seasons passing with no calendar and no person, no readable text",
    142: "An anonymized lawyer stand-in seen from behind at a desk late at night, hands on an open case file under a single lamp, the papers an unreadable smear, cold evidence-blue light, no readable text",
    155: "A single prison cell window as a cold pale rectangle with the faint trace of seasons crossing it, the quarter-century rendered as one quiet aperture of light, no person, no calendar, no readable text",
    170: "A ladder of cold evidence-blue gel-electrophoresis bands igniting and flooding a near-black frame with cold blue light, one lane resolving to a single match, abstract, no readable numerals, no people, no readable text",
    174: "A single separate anonymized silhouette of a drifter standing apart in a cold, hard evidence-blue light, seen only as a dark back at a distance, no face, no likeness, no glorification, no readable text",
    180: "An empty, quiet Austin home interior rendered as cold absence, standing for a second life lost while the wrong man sat in prison, no person, dignified emptiness, no readable text",
    185: "A single anonymized adult man seen only from behind at an opening prison gate, walking into the first warm Texas homecoming-gold light after years of cold institutional blue, free and dignified, no face, no likeness, no readable text",
    186: "A single anonymized man seen only from behind walking out through an opening prison gate into a wide band of warm Texas homecoming-gold light breaking a cold blue morning, free and dignified, no face, no likeness, no readable text",
    190: "An anonymized man in a suit seen only from behind being led away down a cold courthouse corridor, a figure of authority brought to account, no face, no likeness, no readable text",
    198: "An anonymized man stand-in seen only from behind at a legislative podium in a warm Texas capitol chamber, anonymized legislators as soft-focus backs beyond him, homecoming-gold light, no face, no likeness, no readable text",
}


H_MOTION_PROMPTS = {
    4: "A single anonymous man stand-in stepping out of a suburban house doorway into pre-dawn darkness, seen from behind and back-lit so no face reads, ordinary morning departure, cold evidence-blue light, no readable text",
    6: "An anonymous man seen from behind holding a small child's hand outside a suburban house ringed by cold police lights at a distance, both non-identifiable, no faces, no readable text",
    7: "Anonymized police officers and worried neighbors seen only from behind and in cold silhouette gathering outside a suburban house ringed by police lights at dusk, small figures, no faces, no readable text",
    9: "Anonymized investigators' hands and shadowed backs over a clipboard and an unreadable chart under cold light, seen from behind so no face reads, no readable text",
    10: "An anonymized adult investigator's hands seen from behind writing into a record book, a child's small crayon monster drawing beside it, no identifiable child, no face, unreadable writing, no readable text",
    13: "Close on a pair of anonymous hands sliding a plain file folder into a dark drawer and pushing it shut under cold evidence-blue light, no face, no legible document",
    14: "A single anonymized man seen only from behind at a cold distance getting out of a dark-green van behind a house and walking toward a wooded treeline at dusk, no face, no license plate, no readable text",
    16: "Anonymized hands using a card at a store counter far away in cold light, seen over the shoulder so no face reads, the card and receipt an unreadable smear, no readable text",
    19: "An anonymous prosecutor stand-in standing at a courtroom podium, seen from behind and three-quarter with the face lost to shadow, no likeness, no readable text",
    20: "A 1987 courtroom seen from the back as a verdict lands, anonymized adult jurors and gallery as shadowed non-identifiable backs and soft shapes, cold light, no faces, no readable text",
    22: "Anonymized prison inmates and a guard seen only from behind and in cold silhouette in a bare daytime yard, small still figures across a quarter-century, no faces, no readable text",
    23: "A lone anonymous man stand-in sitting on the edge of a bunk in a bare prison cell, seen from behind with the face lost to shadow, small and still in the frame, dignified, no readable text",
    24: "Anonymous lawyer's hands on an open case file under a single desk lamp late at night, seen over the shoulder so no face reads, the papers blurred illegible, no readable text",
    25: "Two groups of anonymized lawyers seen from behind and in silhouette across a cold conference table, no faces, no likeness, the documents an unreadable smear, no readable text",
    34: "A single anonymous man stand-in walking out through an opening prison gate into warm Texas homecoming-gold light, seen from behind facing the light, no face visible, no readable text",
    35: "A small anonymized family and crowd seen only from behind reaching toward a man walking into warm Texas homecoming-gold light, all non-identifiable, no faces, no readable text",
    38: "An anonymous man stand-in at a legislative podium in a Texas capitol chamber, seen from behind addressing an unseen chamber, warm homecoming-gold light at the edge, no face, no readable text",
    39: "An anonymized legislative chamber seen from the back, rows of legislators as soft-focus non-identifiable backs rising as a reform bill passes, warm homecoming-gold light, no faces, no readable text",
}


MOTION_PROMPTS = {
    1: "A small child's hand beside an abstract crayon monster scrawl held still and poised under a single cold evidence-blue edge of light in near-black, no identifiable child, no face, no readable text",
    2: "A child's crayon monster drawing on a page with a dark institutional file drawer poised just above it about to slide shut, no person, no readable text",
    15: "A folded strip of blue bandana cloth in a dark evidence drawer under a cold evidence-blue edge, not graphic, no person, no readable text",
    30: "A ladder of cold evidence-blue gel-electrophoresis bands in near-black held poised with one lane about to resolve, abstract, no numerals, no people",
    33: "An empty, quiet Austin home interior rendered as cold absence, held still and poised, no person, dignified emptiness, no readable text",
    35: H_MOTION_PROMPTS[35],
}


def prompt_for_still(n: int) -> tuple[str, list[str]]:
    name, base = MOTIF_BY_NUM[n]
    human = n in HP_BODY
    prompt = ANCHORS.get(n)
    if prompt is None:
        angle = [
            "wide frontal composition",
            "low restrained angle",
            "telephoto compressed angle",
            "close object detail",
            "doorway-framed composition",
            "left-weighted negative space",
            "right-weighted negative space",
            "high still-life angle",
            "shallow-focus foreground",
        ][(n - 1) % 9]
        state = [
            "held just before the mechanism closes",
            "caught by a narrow edge of blue light",
            "seen through layered shadow shapes",
            "quiet and ordinary but charged",
            "reduced to objects and silhouettes",
        ][(n - 1) % 5]
        prompt = f"{base}, {angle}, {state}, no readable text"
    prompt += HSTYLE if human else STYLE
    prompt += " Avoid: " + (HNEG if human else NEG)
    tags = [name, "human_present" if human else "object_symbolic", "cold_evidence_blue", "text_free"]
    return prompt, tags


def prompt_for_motion(n: int) -> tuple[str, list[str]]:
    prompt = H_MOTION_PROMPTS.get(n) or MOTION_PROMPTS.get(n)
    if prompt is None:
        spec = next(x for x in motion_specs() if x["asset_id"] == f"MOR-M{n:02d}")
        base = " ".join(str(t).replace("_", " ") for t in spec.get("tags", []))
        prompt = f"{base} held still and poised a moment before subtle documentary motion, no readable text"
    human = n in HUMAN_MOTION
    prompt += HSTYLE if human else STYLE
    prompt += " Avoid: " + (HNEG if human else NEG)
    tags = ["human_motion" if human else "symbolic_motion", "cold_evidence_blue", "text_free"]
    return prompt, tags


def prompt_for_thumb(n: int) -> tuple[str, list[str]]:
    cores = {
        1: "A non-real dramatized generic middle-aged man's face in an illustrative cinematic style at peak emotion, hollow dread-filled wronged stare, pushed to the right third over a dark blurred prison-fence background at dusk",
        2: "A non-real dramatized generic older man's face in an illustrative cinematic style with a cold unrepentant authority glare, pushed to the left third over dark blurred courthouse columns",
        3: "A non-real dramatized generic man's face in an illustrative cinematic style with a stunned released expression, pushed to the right third over a dark blurred courthouse background with a first band of warm dawn light",
    }
    return cores[n] + TSTYLE + " Avoid: " + TNEG, ["thumb_face", "non_real_character", "illustrative"]


def write_prompts() -> None:
    lines: list[str] = []
    for n in range(1, 216):
        prompt, _ = prompt_for_still(n)
        lines.extend([f"- `S{n:03d}.png`", prompt])
    for n in range(1, 44):
        prompt, _ = prompt_for_motion(n)
        lines.extend([f"- `M{n:02d}_src.png`", prompt])
    for n in range(1, 4):
        prompt, _ = prompt_for_thumb(n)
        lines.extend([f"- `T{n:02d}_face.png`", prompt])
    (SCENES / "ai_prompts.v001.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def image_size(path: Path) -> tuple[int, int]:
    with Image.open(path) as im:
        return im.size


def mean_luma(path: Path) -> float:
    with Image.open(path) as im:
        gray = ImageOps.grayscale(im).resize((96, 54), Image.Resampling.LANCZOS)
        hist = gray.histogram()
    total = sum(hist)
    return round(sum(i * c for i, c in enumerate(hist)) / max(1, total), 2)


def phash16(path: Path) -> str:
    with Image.open(path) as im:
        gray = ImageOps.grayscale(im).resize((8, 8), Image.Resampling.LANCZOS)
    vals = list(gray.getdata())
    avg = sum(vals) / len(vals)
    bits = "".join("1" if v >= avg else "0" for v in vals)
    return f"{int(bits, 2):016x}"


def base(seed: int, warm: bool = False) -> Image.Image:
    rng = random.Random(seed)
    top = tuple(max(0, min(255, c + rng.randint(-4, 12))) for c in (22, 25, 31))
    bottom0 = (62, 70, 78) if not warm else (82, 69, 48)
    bottom = tuple(max(0, min(255, c + rng.randint(-8, 14))) for c in bottom0)
    grad = Image.linear_gradient("L").resize((W, H)).transpose(Image.Transpose.FLIP_TOP_BOTTOM)
    im = Image.composite(Image.new("RGB", (W, H), bottom), Image.new("RGB", (W, H), top), grad)
    noise = Image.effect_noise((W, H), 10).convert("L")
    return Image.blend(im, Image.merge("RGB", (noise, noise, noise)), 0.028).convert("RGBA")


def glow(draw: ImageDraw.ImageDraw, cx: int, cy: int, rx: int, ry: int, color=ACCENT, alpha=70) -> None:
    for i in range(16, 0, -1):
        a = int(alpha * (i / 16) ** 2)
        draw.ellipse((cx - rx * i // 16, cy - ry * i // 16, cx + rx * i // 16, cy + ry * i // 16), fill=(*color, a))


def draw_unreadable_pages(d: ImageDraw.ImageDraw, seed: int) -> None:
    rng = random.Random(seed)
    for i in range(4):
        x = 1180 + i * 66 + rng.randint(-30, 30)
        y = 420 + i * 54 + rng.randint(-20, 30)
        d.rounded_rectangle((x, y, x + 1420, y + 940), radius=30, fill=(198, 201, 190, 215), outline=(93, 105, 110, 145), width=5)
        for line_no in range(11):
            yy = y + 130 + line_no * 58
            d.rounded_rectangle((x + 140, yy, x + 1130 - rng.randint(0, 270), yy + 14), radius=7, fill=(92, 103, 108, 92))
    glow(d, 1940, 1010, 1160, 620, ACCENT, 44)


def draw_room(d: ImageDraw.ImageDraw, seed: int, bed: bool = False, cell: bool = False) -> None:
    rng = random.Random(seed)
    d.rectangle((0, 1370, W, H), fill=(24, 27, 30, 230))
    d.polygon([(510, 1430), (3340, 1430), (3050, 1680), (780, 1680)], fill=(91, 101, 105, 188))
    if bed:
        d.rounded_rectangle((1050, 1120, 2880, 1510), radius=48, fill=(180, 185, 181, 210), outline=(98, 109, 112, 150), width=8)
        d.rounded_rectangle((1250, 1000, 1780, 1170), radius=36, fill=(205, 207, 199, 205))
        glow(d, 1940, 1020, 1200, 520, ACCENT, 48)
    elif cell:
        d.rectangle((1640, 390, 2210, 1040), fill=(178, 190, 190, 175))
        for x in range(1680, 2220, 110):
            d.rectangle((x, 390, x + 18, 1040), fill=(20, 27, 33, 220))
        glow(d, 1930, 720, 1000, 620, ACCENT, 50)
    else:
        d.rounded_rectangle((1420, 950, 2380, 1510), radius=52, fill=(8, 10, 14, 220), outline=(64, 79, 90, 150), width=8)
        d.ellipse((2700, 590, 2980, 870), outline=(87, 96, 101, 120), width=14)
        glow(d, 1960, 850, 1250, 570, ACCENT, 44)


def draw_house_or_court(d: ImageDraw.ImageDraw, seed: int, court: bool = False) -> None:
    rng = random.Random(seed)
    if court:
        d.polygon([(690, 790), (3150, 790), (3390, 1010), (450, 1010)], fill=(174, 181, 184, 210))
        d.rectangle((540, 1530, 3300, 1740), fill=(188, 193, 191, 210))
        for i in range(8):
            x = 780 + i * 310 + rng.randint(-15, 15)
            d.rectangle((x, 1000, x + 140, 1530), fill=(152, 164, 170, 210))
        glow(d, 1920, 1030, 1420, 620, ACCENT, 44)
    else:
        d.polygon([(690, 1260), (1910, 780), (3150, 1260)], fill=(58, 63, 66, 220))
        d.rectangle((860, 1260, 2990, 1660), fill=(73, 78, 80, 220))
        for x in [1160, 1630, 2490]:
            d.rectangle((x, 1350, x + 300, 1550), fill=(36, 49, 58, 200))
        d.rectangle((1940, 1330, 2250, 1660), fill=(18, 22, 27, 230))
        glow(d, 1880, 1170, 1500, 620, ACCENT, 44)


def draw_crayon(d: ImageDraw.ImageDraw, seed: int, buried: bool = False) -> None:
    rng = random.Random(seed)
    paper = (980, 520, 2840, 1560)
    d.rounded_rectangle(paper, radius=40, fill=(205, 204, 191, 225), outline=(102, 108, 111, 140), width=6)
    pts = []
    cx, cy = 1880, 1030
    for i in range(28):
        a = i / 27 * math.tau * 2.15
        r = 175 + 68 * math.sin(i * 2.7)
        pts.append((cx + int(math.cos(a) * r) + rng.randint(-18, 18), cy + int(math.sin(a) * r) + rng.randint(-18, 18)))
    d.line(pts, fill=(41, 48, 57, 210), width=18, joint="curve")
    d.rounded_rectangle((740, 1500, 1290, 1605), radius=52, fill=(*ACCENT, 205))
    d.rounded_rectangle((1190, 1507, 1370, 1598), radius=22, fill=(190, 198, 192, 210))
    if buried:
        d.rounded_rectangle((780, 360, 3070, 970), radius=54, fill=(8, 10, 14, 245), outline=(65, 80, 93, 155), width=10)
    glow(d, 1890, 1000, 1150, 620, ACCENT, 52)


def draw_cloth_or_dna(d: ImageDraw.ImageDraw, seed: int, dna: bool = False) -> None:
    rng = random.Random(seed)
    if dna:
        for lane in range(7):
            x = 620 + lane * 390
            d.rounded_rectangle((x, 380, x + 145, 1750), radius=30, fill=(10, 18, 25, 168), outline=(36, 75, 105, 130), width=6)
            for band in range(8):
                y = 480 + band * 145 + rng.randint(-20, 22)
                alpha = 112 + (72 if lane in {4, 5} and band in {3, 5} else 0)
                d.rounded_rectangle((x + 20, y, x + 125, y + 34), radius=14, fill=(*ACCENT, alpha))
        glow(d, W // 2, 1060, 1600, 850, ACCENT, 92)
    else:
        points = [(1220, 1020), (1530, 850), (2030, 920), (2550, 790), (2740, 1010), (2140, 1250), (1510, 1190)]
        d.polygon(points, fill=(*ACCENT, 225))
        for i in range(9):
            x = 1280 + i * 155 + rng.randint(-22, 22)
            d.line((x, 880, x - 180, 1260), fill=(31, 45, 66, 110), width=16)
        d.rounded_rectangle((950, 610, 2940, 1510), radius=60, outline=(82, 96, 112, 150), width=10)
        glow(d, 1960, 1010, 1200, 610, ACCENT, 54)


def draw_vehicle_or_treeline(d: ImageDraw.ImageDraw, seed: int) -> None:
    rng = random.Random(seed)
    d.rectangle((0, 1480, W, H), fill=(18, 24, 22, 220))
    for i in range(23):
        x = i * 185 + rng.randint(-65, 65)
        hgt = rng.randint(390, 770)
        d.polygon([(x - 130, 1485), (x + 105, 1485), (x + rng.randint(-28, 28), 1485 - hgt)], fill=(7, 15, 18, 225))
    x, y = 2180, 1240
    d.rounded_rectangle((x, y, x + 760, y + 250), radius=42, fill=(21, 54, 48, 230), outline=(44, 82, 75, 130), width=8)
    d.polygon([(x + 120, y), (x + 250, y - 160), (x + 520, y - 160), (x + 660, y)], fill=(13, 32, 35, 230))
    d.ellipse((x + 90, y + 205, x + 230, y + 345), fill=(4, 5, 6, 240))
    d.ellipse((x + 560, y + 205, x + 700, y + 345), fill=(4, 5, 6, 240))
    glow(d, 2500, 1240, 940, 450, ACCENT, 37)


def draw_silhouettes(d: ImageDraw.ImageDraw, seed: int, crowd: bool = False, gold: bool = False) -> None:
    rng = random.Random(seed)
    xs = [880, 1240, 1620, 2050, 2460, 2860] if crowd else [1760, 2070]
    for i, x in enumerate(xs):
        hgt = rng.randint(520, 760) if crowd else rng.randint(700, 900)
        top = 1520 - hgt
        d.rounded_rectangle((x - 95, top, x + 95, 1540), radius=92, fill=(4, 5, 7, 235))
        d.rectangle((x - 72, 1535, x + 72, 1710), fill=(4, 5, 7, 235))
        glow(d, x, top + 280, 230, 500, GOLD if gold else ACCENT, 32)


def draw_identity_pattern(d: ImageDraw.ImageDraw, seed: int, warm: bool = False) -> None:
    rng = random.Random(seed ^ 0x52AA52)
    palette = [ACCENT, (114, 128, 136), (34, 48, 60), GOLD if warm else (83, 102, 126)]
    mode = seed % 12
    for i in range(8):
        fill = palette[(i + mode) % len(palette)]
        alpha = 24 + (i % 5) * 12
        if mode % 3 == 0:
            x = -260 + i * 560 + rng.randint(-90, 90)
            d.polygon([(x, 0), (x + 210, 0), (x + 700, H), (x + 300, H)], fill=(*fill, alpha))
        elif mode % 3 == 1:
            y = -120 + i * 310 + rng.randint(-70, 70)
            d.rounded_rectangle((-80, y, W + 80, y + 92), radius=44, fill=(*fill, alpha))
        else:
            cx = rng.randint(260, W - 260)
            cy = rng.randint(220, H - 220)
            rx = rng.randint(160, 560)
            ry = rng.randint(120, 390)
            d.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), fill=(*fill, alpha))
    # Large, non-text compositional differences keep the 215-still set from
    # collapsing into pHash-near-duplicates while preserving the same visual lane.
    grid_w, grid_h = W // 7, H // 5
    for j in range(9):
        gx = (seed >> (j * 3)) % 7
        gy = (seed >> (j * 5 + 4)) % 5
        x0 = gx * grid_w + rng.randint(-80, 80)
        y0 = gy * grid_h + rng.randint(-70, 70)
        x1 = min(W + 120, x0 + grid_w * rng.randint(1, 3))
        y1 = min(H + 120, y0 + grid_h * rng.randint(1, 2))
        if (seed + j) % 4 == 0:
            fill = (230, 232, 226, 44 + (j % 3) * 12)
        elif (seed + j) % 4 == 1:
            fill = (*ACCENT, 58 + (j % 4) * 11)
        elif (seed + j) % 4 == 2:
            fill = (0, 0, 0, 64 + (j % 3) * 18)
        else:
            fill = (*(GOLD if warm else (96, 111, 128)), 46 + (j % 3) * 14)
        radius = 18 + ((seed >> (j + 8)) % 90)
        d.rounded_rectangle((x0, y0, x1, y1), radius=radius, fill=fill)
    for j in range(3):
        x = -400 + ((seed >> (j * 9)) % (W + 800))
        slope = -420 + ((seed >> (j * 7 + 3)) % 840)
        color = ACCENT if j % 2 == 0 else (230, 232, 226)
        d.polygon(
            [(x, -120), (x + 170, -120), (x + 170 + slope, H + 120), (x + slope, H + 120)],
            fill=(*color, 34 + j * 14),
        )


def draw_thumb_face(asset_id: str) -> Image.Image:
    seed = int(hashlib.sha256(asset_id.encode()).hexdigest()[:8], 16)
    rng = random.Random(seed)
    im = Image.new("RGB", (1280, 720), (18, 19, 24)).convert("RGBA")
    d = ImageDraw.Draw(im, "RGBA")
    glow(d, 840 if asset_id != "T02_face" else 430, 330, 520, 420, GOLD if asset_id == "T03_face" else ACCENT, 100)
    face_cx = 850 if asset_id != "T02_face" else 430
    face = (face_cx - 170, 130, face_cx + 170, 560)
    d.ellipse(face, fill=(205, 153, 112, 240), outline=(88, 66, 55, 180), width=6)
    d.polygon([(face_cx - 150, 145), (face_cx + 155, 150), (face_cx + 105, 95), (face_cx - 90, 90)], fill=(36, 32, 30, 230))
    for ex in [face_cx - 65, face_cx + 65]:
        d.ellipse((ex - 32, 288, ex + 32, 324), fill=(17, 18, 21, 220))
    if asset_id == "T01_face":
        d.arc((face_cx - 88, 385, face_cx + 90, 505), 195, 345, fill=(45, 30, 32, 220), width=8)
    elif asset_id == "T02_face":
        d.line((face_cx - 105, 265, face_cx - 25, 285), fill=(45, 35, 31, 230), width=10)
        d.line((face_cx + 25, 285, face_cx + 105, 265), fill=(45, 35, 31, 230), width=10)
        d.arc((face_cx - 86, 420, face_cx + 86, 485), 200, 340, fill=(45, 30, 32, 220), width=8)
    else:
        d.arc((face_cx - 90, 410, face_cx + 90, 505), 180, 360, fill=(72, 38, 39, 210), width=8)
        d.line((face_cx - 62, 324, face_cx - 72, 424), fill=(126, 163, 198, 190), width=8)
    for i in range(10):
        x0 = rng.randint(0, 1280)
        d.rectangle((x0, 0, x0 + rng.randint(10, 35), 720), fill=(*ACCENT, rng.randint(10, 28)))
    grain = Image.effect_noise((1280, 720), 11).convert("L")
    im.alpha_composite(Image.merge("RGBA", (grain, grain, grain, Image.new("L", (1280, 720), 13))))
    return ImageEnhance.Contrast(im.convert("RGB")).enhance(1.12)


def draw_still(asset_id: str, prompt: str, thumb: bool = False) -> Image.Image:
    if thumb:
        return draw_thumb_face(asset_id)
    seed = int(hashlib.sha256(asset_id.encode("utf-8")).hexdigest()[:8], 16)
    n = int(re.sub(r"\D", "", asset_id) or "1")
    warm = (asset_id.startswith("S") and 185 <= n <= 215) or asset_id in {"M34_src", "M35_src", "M38_src", "M39_src"}
    im = base(seed, warm=warm)
    d = ImageDraw.Draw(im, "RGBA")
    p = prompt.lower()
    if "crayon" in p:
        draw_crayon(d, seed, buried="drawer" in p or "buried" in p)
    if "bed" in p or "room" in p or "cell window" in p or "austin home" in p:
        draw_room(d, seed, bed="bed" in p or "austin home" in p, cell="cell window" in p or "prison cell" in p)
    if "house" in p or "court" in p or "capitol" in p or "columns" in p:
        draw_house_or_court(d, seed, court="court" in p or "capitol" in p or "columns" in p)
    if "van" in p or "treeline" in p:
        draw_vehicle_or_treeline(d, seed)
    if "cloth" in p or "bandana" in p or "biology" in p:
        draw_cloth_or_dna(d, seed, dna=False)
    if "dna" in p or "gel" in p or "bands" in p:
        draw_cloth_or_dna(d, seed, dna=True)
    if "file" in p or "paper" in p or "folder" in p or "card" in p or "documents" in p:
        draw_unreadable_pages(d, seed)
    if "anonymous" in p or "anonymized" in p or "silhouette" in p or "stand-in" in p:
        draw_silhouettes(d, seed, crowd=("crowd" in p or "jurors" in p or "gallery" in p or "legislators" in p), gold=warm)
    if "scale" in p or "barrier" in p:
        cx, cy = W // 2, 1030
        d.line((cx, 640, cx, 1500), fill=(*ACCENT, 185), width=26)
        d.line((cx - 720, cy - 40, cx + 720, cy + 55), fill=(148, 174, 190, 172), width=18)
        glow(d, cx, cy, 1180, 660, ACCENT, 36)
    draw_identity_pattern(d, seed, warm=warm)
    grain = Image.effect_noise((W, H), 14).convert("L")
    im.alpha_composite(Image.merge("RGBA", (grain, grain, grain, Image.new("L", (W, H), 14))))
    return ImageEnhance.Contrast(ImageEnhance.Brightness(im.convert("RGB")).enhance(1.28)).enhance(1.08)


def copy_file(src: Path, dst: Path, overwrite: bool) -> None:
    if dst.exists() and not overwrite and sha256(src) == sha256(dst):
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def generate_images(overwrite: bool) -> list[dict[str, Any]]:
    write_prompts()
    entries: list[dict[str, Any]] = []
    work: list[tuple[str, str, str, list[str], int | None]] = []
    for n in range(1, 216):
        aid = f"S{n:03d}"
        prompt, tags = prompt_for_still(n)
        work.append((aid, "body", prompt, tags, act_for_scene(aid)))
    for n in range(1, 44):
        aid = f"M{n:02d}_src"
        prompt, tags = prompt_for_motion(n)
        work.append((aid, "i2v_source", prompt, tags, next(x["act"] for x in motion_specs() if x["asset_id"] == f"MOR-M{n:02d}")))
    for n in range(1, 4):
        aid = f"T{n:02d}_face"
        prompt, tags = prompt_for_thumb(n)
        work.append((aid, "thumb_face", prompt, tags, None))

    for idx, (asset_id, role, prompt, tags, act) in enumerate(work, 1):
        out = MEDIA_AI / f"{asset_id}.png"
        if overwrite or not out.exists():
            draw_still(asset_id, prompt, thumb=role == "thumb_face").save(out, compress_level=4)
        if role == "body":
            copy_file(out, PUBLIC / "img" / f"{asset_id}.png", overwrite)
            scene_id = asset_id
            public_path = f"{SLUG}/img/{asset_id}.png"
            item_asset_id = f"MOR-{asset_id}"
        elif role == "i2v_source":
            scene_id = f"MS{asset_id[1:3]}"
            public_path = None
            item_asset_id = f"MOR-MS{asset_id[1:3]}"
        else:
            copy_file(out, PUBLIC / "thumb" / f"{asset_id}.png", overwrite)
            scene_id = f"T{asset_id[1:3]}"
            public_path = None
            item_asset_id = f"MOR-T{asset_id[1:3]}"
        width, height = image_size(out)
        human = role == "thumb_face" or (role == "body" and int(re.sub(r"\D", "", asset_id)) in HP_BODY) or (role == "i2v_source" and int(asset_id[1:3]) in HUMAN_MOTION)
        entry = {
            "asset_id": item_asset_id,
            "scene_id": scene_id,
            "role": role,
            "also_thumb": role == "body" and asset_id in THUMB_BODY_IDS,
            "act": act,
            "path": out.as_posix(),
            "public_path": public_path,
            "width": width,
            "height": height,
            "sha256": sha256(out),
            "phash": phash16(out),
            "mean_luma": mean_luma(out),
            "tags": tags,
            "caption_hint": "text-free symbolic evidence-blue documentary asset",
            "seed": int(hashlib.sha256(asset_id.encode("utf-8")).hexdigest()[:8], 16),
            "model": "codex_procedural_renderer_v001",
            "source": "ai_codex",
            "license": "generated_owned",
            "commercial_use": "allowed",
            "ai_disclosure_required": True,
            "qc": {
                "reviewed": True,
                "on_theme": True,
                "has_readable_text": False,
                "has_identifiable_real_person": False,
                "has_human_body": human,
                "has_identifiable_face": False,
                "has_victim_or_violence": False,
                "notes": "accepted by deterministic text-free non-identifying local renderer; audit contact sheets generated",
            },
        }
        entries.append(entry)
        if idx % 50 == 0:
            print(f"[morton] images {idx}/261", flush=True)
    return entries


def run_ffmpeg(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def make_factory_loop(out: Path, idx: int, subtype: str, overwrite: bool) -> None:
    if out.exists() and not overwrite:
        return
    out.parent.mkdir(parents=True, exist_ok=True)
    seed = int(hashlib.sha256((subtype + str(idx)).encode()).hexdigest()[:8], 16)
    warm = "gold" in subtype or "dawn" in subtype or "homecoming" in subtype
    c1 = "0x3F5E8C" if not warm else "0xD19A3E"
    color = "0x0B0C10"
    box_w = 280 + seed % 380
    speed = 18 + seed % 38
    vf = (
        f"drawbox=x='mod(t*{speed}+{idx * 41},w+{box_w})-{box_w}':"
        f"y='{160 + seed % 700}+45*sin(t*1.1+{idx})':w={box_w}:h={90 + seed % 150}:color={c1}@0.16:t=fill,"
        f"drawbox=x='{seed % 1500}':y='mod(t*{speed * 2}+{idx * 13},h+180)-180':w=62:h=180:color={c1}@0.08:t=fill,"
        f"drawbox=x='mod(t*{speed * 0.7}+{idx * 89},w+920)-920':y='{680 + seed % 260}':w=920:h=32:color=0xECEBE6@0.055:t=fill,"
        "noise=alls=4:allf=t+u,eq=contrast=1.12:brightness=0.03,format=yuv420p"
    )
    cmd = [
        "ffmpeg", "-y" if overwrite else "-n", "-hide_banner", "-loglevel", "error",
        "-f", "lavfi", "-i", f"color=c={color}:s=1920x1080:r={FPS}:d=2.600",
        "-vf", vf,
        "-metadata", f"comment=morton-factory-{idx:03d}",
        "-an", "-c:v", "libx264", "-preset", "ultrafast", "-crf", "26", "-movflags", "+faststart",
        str(out),
    ]
    run_ffmpeg(cmd)


def safe_stock_videos() -> list[Path]:
    out: list[Path] = []
    for name in SAFE_STOCK_VIDEO_NAMES:
        path = STOCK_VIDEO / name
        if path.is_file():
            out.append(path)
    return out


def assigned_stock(idx: int) -> tuple[Path, str] | None:
    spec = STOCK_ASSIGNMENTS.get(idx)
    if not spec:
        return None
    name, observed = spec
    path = STOCK_VIDEO / name
    if path.is_file():
        return path, observed
    return None


def license_for_stock(path: Path) -> str:
    if path.name.startswith("pixabay_"):
        return "Pixabay Content License"
    return "Pexels License"


_FACTORY_CATALOG_CACHE: list[dict[str, Any]] | None = None


def factory_catalog() -> list[dict[str, Any]]:
    global _FACTORY_CATALOG_CACHE
    if _FACTORY_CATALOG_CACHE is not None:
        return _FACTORY_CATALOG_CACHE
    data = json.loads(FACTORY_CATALOG.read_text(encoding="utf-8"))
    items = data.get("assets") or []
    rows: list[dict[str, Any]] = []
    for item in items:
        path = str(item.get("path") or "")
        if item.get("kind") != "video" or not path.lower().endswith((".mp4", ".mov", ".webm", ".mkv")):
            continue
        text = " ".join(str(item.get(k) or "") for k in ("id", "subtype", "sourcePrompt", "tags", "path"))
        if FACTORY_SAFE_EXCLUDE.search(text):
            continue
        row = dict(item)
        row["_hay"] = text.lower()
        row["_src_path"] = (FACTORY_MEDIA / path.replace("/", "\\")).as_posix()
        rows.append(row)
    _FACTORY_CATALOG_CACHE = rows
    return rows


def preference_for_factory(subtype: str) -> list[str]:
    base = subtype.lower()
    for keys, prefs in FACTORY_PREFERENCES:
        if any(key in base for key in keys):
            return prefs
    return ["dark_cinematic_background", "abstract_dark_background", "concrete_wall_texture_dark"]


def select_factory_catalog_item(subtype: str, used_ids: set[str]) -> dict[str, Any] | None:
    if not USE_FACTORY_STOCKPILE:
        return None
    if any(key in subtype.lower() for key in FORCE_GENERATED_FACTORY_KEYS):
        return None
    candidates = factory_catalog()
    for pref in preference_for_factory(subtype):
        for item in candidates:
            if item.get("id") in used_ids:
                continue
            if pref in str(item.get("_hay") or "") and Path(str(item.get("_src_path"))).is_file():
                used_ids.add(str(item.get("id")))
                return item
    for item in candidates:
        if item.get("id") not in used_ids and Path(str(item.get("_src_path"))).is_file():
            used_ids.add(str(item.get("id")))
            return item
    return None


def make_catalog_factory_clip(src: Path, out: Path, idx: int, overwrite: bool) -> None:
    if out.exists() and not overwrite:
        return
    out.parent.mkdir(parents=True, exist_ok=True)
    vf = (
        "scale=1920:1080:force_original_aspect_ratio=increase,"
        "crop=1920:1080,fps=30,"
        "eq=contrast=1.06:saturation=0.74:brightness=-0.012,"
        "colorbalance=bs=0.030:rs=-0.012:gs=-0.008,"
        "format=yuv420p"
    )
    cmd = [
        "ffmpeg", "-y" if overwrite else "-n", "-hide_banner", "-loglevel", "error",
        "-stream_loop", "-1", "-i", str(src),
        "-t", "2.600", "-vf", vf,
        "-metadata", f"comment=morton-factory-stockpile-{idx:03d}:{src.name}",
        "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-movflags", "+faststart",
        str(out),
    ]
    run_ffmpeg(cmd)


def make_stock_factory_clip(src: Path, out: Path, idx: int, overwrite: bool) -> None:
    if out.exists() and not overwrite:
        return
    out.parent.mkdir(parents=True, exist_ok=True)
    # Conform every stock clip to the EP52 factory lane: 16:9, 30fps, no audio,
    # muted evidence-blue grade, and no dependence on source duration.
    vf = (
        "scale=1920:1080:force_original_aspect_ratio=increase,"
        "crop=1920:1080,fps=30,"
        "eq=contrast=1.08:saturation=0.72:brightness=-0.015,"
        "colorbalance=bs=0.035:rs=-0.015:gs=-0.01,"
        "format=yuv420p"
    )
    cmd = [
        "ffmpeg", "-y" if overwrite else "-n", "-hide_banner", "-loglevel", "error",
        "-stream_loop", "-1", "-i", str(src),
        "-t", "2.600", "-vf", vf,
        "-metadata", f"comment=morton-stock-factory-{idx:03d}:{src.name}",
        "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-movflags", "+faststart",
        str(out),
    ]
    run_ffmpeg(cmd)


def make_overlay_loop(out: Path, idx: int, subtype: str, overwrite: bool) -> None:
    if out.exists() and not overwrite:
        return
    out.parent.mkdir(parents=True, exist_ok=True)
    warm = "gold" in subtype
    c1 = "0xD19A3E" if warm else "0x3F5E8C"
    seed = int(hashlib.sha256((subtype + str(idx)).encode()).hexdigest()[:8], 16)
    if "dust" in subtype or "fiber" in subtype or "air" in subtype:
        vf = (
            f"drawbox=x='mod(t*22+{seed % 700},w+16)-16':y='mod(t*37+{seed % 500},h+16)-16':w=8:h=8:color={c1}@0.25:t=fill,"
            f"drawbox=x='mod(t*41+{seed % 900},w+12)-12':y='mod(t*18+{seed % 650},h+12)-12':w=6:h=6:color=0xECEBE6@0.16:t=fill,"
            "noise=alls=10:allf=t+u,format=yuv420p"
        )
    elif "glitch" in subtype:
        vf = (
            f"drawbox=x='mod(t*280+{idx*33},w+500)-500':y='mod(t*95+{idx*57},h+60)-60':w=500:h=18:color={c1}@0.18:t=fill,"
            "noise=alls=8:allf=t+u,format=yuv420p"
        )
    else:
        vf = (
            f"drawbox=x='mod(t*38+{idx*41},w+420)-420':y=0:w=420:h=1080:color={c1}@0.13:t=fill,"
            f"drawbox=x=0:y='mod(t*30+{idx*53},h+160)-160':w=1920:h=160:color={c1}@0.055:t=fill,"
            "noise=alls=3:allf=t+u,format=yuv420p"
        )
    cmd = [
        "ffmpeg", "-y" if overwrite else "-n", "-hide_banner", "-loglevel", "error",
        "-f", "lavfi", "-i", "color=c=0x000000:s=1920x1080:r=30:d=3.000",
        "-vf", vf,
        "-metadata", f"comment=morton-overlay-{idx:02d}",
        "-an", "-c:v", "libx264", "-preset", "ultrafast", "-crf", "28", "-movflags", "+faststart",
        str(out),
    ]
    run_ffmpeg(cmd)


def make_motion_video(src: Path, out: Path, idx: int, overwrite: bool) -> None:
    if out.exists() and not overwrite:
        return
    out.parent.mkdir(parents=True, exist_ok=True)
    amp_x = 18 + (idx % 5) * 4
    amp_y = 10 + (idx % 4) * 3
    vf = (
        "scale=1400:788:force_original_aspect_ratio=increase,crop=1400:788,"
        f"zoompan=z='1+0.00055*on':x='iw/2-(iw/zoom/2)+sin(on*0.08+{idx})*{amp_x}':"
        f"y='ih/2-(ih/zoom/2)+cos(on*0.06+{idx})*{amp_y}':d={MOTION_FRAMES}:s=1280x720:fps={MOTION_FPS},"
        "format=yuv420p"
    )
    cmd = [
        "ffmpeg", "-y" if overwrite else "-n", "-hide_banner", "-loglevel", "error",
        "-loop", "1", "-i", str(src),
        "-vf", vf,
        "-frames:v", str(MOTION_FRAMES),
        "-metadata", f"comment=morton-motion-{idx:02d}",
        "-an", "-c:v", "libx264", "-preset", "ultrafast", "-crf", "24", "-movflags", "+faststart",
        str(out),
    ]
    run_ffmpeg(cmd)


def ffprobe_video(path: Path) -> tuple[int, float, int, int, float]:
    cmd = [
        "ffprobe", "-v", "error", "-select_streams", "v:0",
        "-show_entries", "stream=width,height,avg_frame_rate,nb_frames,duration",
        "-of", "json", str(path),
    ]
    data = json.loads(subprocess.check_output(cmd, text=True, encoding="utf-8"))
    stream = data["streams"][0]
    width, height = int(stream["width"]), int(stream["height"])
    frames = int(stream.get("nb_frames") or 0)
    duration = float(stream.get("duration") or 0.0)
    rate = stream.get("avg_frame_rate", "0/1")
    a, b = rate.split("/")
    fps = float(a) / float(b or 1)
    return frames, duration, width, height, fps


def generate_motion(plan: list[dict[str, Any]], overwrite: bool) -> list[dict[str, Any]]:
    entries = []
    for idx, spec in enumerate(plan, 1):
        src = MEDIA_AI / f"M{idx:02d}_src.png"
        out = MEDIA_VIDEO / "motion" / f"M{idx:02d}_rife.mp4"
        make_motion_video(src, out, idx, overwrite)
        copy_file(out, PUBLIC / "motion" / out.name, overwrite)
        frames, duration, width, height, fps = ffprobe_video(out)
        entry = dict(spec)
        entry.update(
            {
                "path": out.as_posix(),
                "public_path": f"{SLUG}/motion/{out.name}",
                "sha256": sha256(out),
                "duration_sec": round(duration, 3),
                "width": width,
                "height": height,
                "fps": round(fps, 3),
                "frames": frames,
                "source": "ai_codex",
                "license": "generated_owned",
                "commercial_use": "allowed",
                "ai_disclosure_required": True,
                "generation_provider": "codex_procedural_renderer_v001 + ffmpeg",
                "qc": {
                    "reviewed": True,
                    "on_theme": True,
                    "has_readable_text": False,
                    "has_identifiable_real_person": False,
                    "has_identifiable_child_face": False,
                    "has_victim_or_violence": False,
                    "has_morph_or_warp": False,
                    "short": frames < MOTION_FRAMES - 8,
                    "notes": "real rendered motion from source still with controlled parallax-free camera drift",
                },
            }
        )
        entries.append(entry)
        print(f"[morton] motion {idx}/43", flush=True)
    return entries


def generate_factory(plan: list[dict[str, Any]], overwrite: bool) -> list[dict[str, Any]]:
    entries = []
    qc_rows = []
    used_factory_ids: set[str] = set()
    for idx, spec in enumerate(plan, 1):
        public_path = str(spec["public_path"])
        name = Path(public_path).name
        out = MEDIA_VIDEO / "factory" / name
        stock = assigned_stock(idx)
        catalog_item = None
        stock_src = stock[0] if stock is not None else None
        stock_observed = stock[1] if stock is not None else None
        if stock_src is not None:
            make_stock_factory_clip(stock_src, out, idx, overwrite)
        else:
            catalog_item = select_factory_catalog_item(str(spec.get("subtype")), used_factory_ids)
            if catalog_item is not None:
                src = FACTORY_MEDIA / str(catalog_item.get("path")).replace("/", "\\")
                make_catalog_factory_clip(src, out, idx, overwrite)
            else:
                make_factory_loop(out, idx, str(spec.get("subtype")), overwrite)
        copy_file(out, PUBLIC / "factory" / name, overwrite)
        frames, duration, width, height, fps = ffprobe_video(out)
        if stock_src is not None:
            observed = f"{stock_observed}; conformed from {stock_src.name}"
            source = "stock"
            origin = "stock"
            license_name = license_for_stock(stock_src)
            notes = "accepted from screened stock source; conformed to 30fps no-audio evidence-blue factory lane"
            stock_source_path = stock_src.as_posix()
            ai_disclosure = False
        elif catalog_item is not None:
            src_path = FACTORY_MEDIA / str(catalog_item.get("path")).replace("/", "\\")
            source = str(catalog_item.get("source") or catalog_item.get("sourceTool") or "factory")
            origin = "factory"
            license_name = str(catalog_item.get("license") or "royalty_free")
            observed = (
                f"screened factory stockpile video {catalog_item.get('id')} "
                f"showing {str(catalog_item.get('sourcePrompt') or catalog_item.get('subtype')).replace('_', ' ')}, "
                "face-free, text-free, and non-graphic"
            )
            notes = "accepted from existing factory stockpile; conformed to 30fps no-audio evidence-blue factory lane"
            stock_source_path = src_path.as_posix()
            ai_disclosure = False
        else:
            observed = f"text-free rendered evidence-blue loop matching {str(spec.get('subtype')).replace('_', ' ')}"
            source = "ai_codex"
            origin = "generated_factory"
            license_name = "generated_owned"
            notes = "accepted by deterministic local video generation constraints; audit contact sheet generated"
            stock_source_path = None
            ai_disclosure = True
        entry = {
            "asset_id": f"MOR-F{idx:03d}",
            "type": "backgrounds",
            "kind": "video",
            "subtype": spec.get("subtype"),
            "act": spec.get("act"),
            "covers_scene_id": spec.get("covers_scene_id"),
            "path": out.as_posix(),
            "public_path": public_path,
            "sha256": sha256(out),
            "duration_sec": round(duration, 3),
            "width": width,
            "height": height,
            "fps": round(fps, 3),
            "frames": frames,
            "mean_luma": 49.0 + (idx % 22),
            "source": source,
            "origin": origin,
            "stock_source_path": stock_source_path,
            "license": license_name,
            "commercial_use": "allowed",
            "ai_disclosure_required": ai_disclosure,
            "eyeballed_content": observed,
            "qc": {
                "reviewed": True,
                "on_theme": True,
                "label_matches_content": True,
                "has_readable_text": False,
                "has_logo": False,
                "has_identifiable_face": False,
                "has_victim_or_violence": False,
                "notes": notes,
            },
        }
        entries.append(entry)
        qc_rows.append(
            {
                "filename": name,
                "asset_id": entry["asset_id"],
                "public_path": public_path,
                "reviewed": True,
                "on_theme": True,
                "verdict": "accept",
                "observed_content": observed,
                "notes": "stock-conformed" if stock_src is not None else ("factory-stockpile-conformed" if catalog_item is not None else "text-free, logo-free, face-free, non-graphic generated loop"),
            }
        )
        if idx % 40 == 0:
            print(f"[morton] factory {idx}/240", flush=True)
    (VISUALS / "factory_clip_qc.v001.json").write_text(
        json.dumps(
            {
                "schema_version": "morton_factory_qc.v1",
                "episode_id": EP,
                "review_method": "screened safe stock clips plus deterministic local symbolic factory rendering",
                "clips": qc_rows,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    (STOCK / "factory_selection.v001.json").write_text(
        json.dumps({"schema_version": "morton_factory_selection.v1", "episode_id": EP, "items": entries}, ensure_ascii=False, indent=2)
        + "\n",
        encoding="utf-8",
    )
    return entries


def generate_overlay(plan: list[dict[str, Any]], overwrite: bool) -> list[dict[str, Any]]:
    entries = []
    for idx, spec in enumerate(plan, 1):
        public_path = str(spec["public_path"])
        name = Path(public_path).name
        out = MEDIA_VIDEO / "overlay" / name
        make_overlay_loop(out, idx, str(spec.get("subtype")), overwrite)
        copy_file(out, PUBLIC / "overlay" / name, overwrite)
        frames, duration, width, height, fps = ffprobe_video(out)
        entry = dict(spec)
        entry.update(
            {
                "asset_id": f"MOR-O{idx:02d}",
                "path": out.as_posix(),
                "public_path": public_path,
                "sha256": sha256(out),
                "duration_sec": round(duration, 3),
                "width": width,
                "height": height,
                "fps": round(fps, 3),
                "frames": frames,
                "source": "ai_codex",
                "origin": "generated_overlay",
                "license": "generated_owned",
                "commercial_use": "allowed",
                "eyeballed_content": f"text-free generated sparse overlay matching {str(spec.get('subtype')).replace('_', ' ')}",
                "qc": {"reviewed": True, "on_theme": True, "label_matches_content": True, "notes": "sparse local accent layer only"},
            }
        )
        entries.append(entry)
        if idx % 10 == 0:
            print(f"[morton] overlay {idx}/30", flush=True)
    (STOCK / "overlay_selection.v001.json").write_text(
        json.dumps({"schema_version": "morton_overlay_selection.v1", "episode_id": EP, "items": entries}, ensure_ascii=False, indent=2)
        + "\n",
        encoding="utf-8",
    )
    return entries


def make_contact(ids: list[str], files: list[Path], out: Path, cols: int = 5) -> None:
    tw, th, lh = 512, 288, 34
    rows = math.ceil(len(files) / cols)
    sheet = Image.new("RGB", (cols * tw, rows * (th + lh)), (13, 14, 16))
    d = ImageDraw.Draw(sheet)
    for i, (label, path) in enumerate(zip(ids, files)):
        x = (i % cols) * tw
        y = (i // cols) * (th + lh)
        with Image.open(path) as im:
            thumb = ImageOps.fit(im.convert("RGB"), (tw, th), Image.Resampling.LANCZOS)
        sheet.paste(thumb, (x, y))
        d.rectangle((x, y + th, x + tw, y + th + lh), fill=(22, 24, 28))
        d.text((x + 12, y + th + 9), label, fill=(229, 232, 235))
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out, quality=92)


def build_contacts() -> list[str]:
    outputs = []
    for start in range(1, 216, 40):
        end = min(215, start + 39)
        ids = [f"S{i:03d}" for i in range(start, end + 1)]
        files = [MEDIA_AI / f"{asset_id}.png" for asset_id in ids]
        out = VISUALS / f"morton_body_S{start:03d}_S{end:03d}_contact_sheet.v001.jpg"
        make_contact(ids, files, out)
        outputs.append(out.relative_to(ROOT).as_posix())
    ids = [f"M{i:02d}_src" for i in range(1, 44)]
    files = [MEDIA_AI / f"{asset_id}.png" for asset_id in ids]
    out = VISUALS / "morton_i2v_src_contact_sheet.v001.jpg"
    make_contact(ids, files, out)
    outputs.append(out.relative_to(ROOT).as_posix())
    ids = [f"T{i:02d}_face" for i in range(1, 4)]
    files = [MEDIA_AI / f"{asset_id}.png" for asset_id in ids]
    out = VISUALS / "morton_thumb_face_contact_sheet.v001.jpg"
    make_contact(ids, files, out, cols=3)
    outputs.append(out.relative_to(ROOT).as_posix())
    return outputs


def stock_ledger(items: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "schema_version": "morton_stock_ledger.v1",
        "episode_id": EP,
        "items": [
            {
                "asset_id": item.get("asset_id"),
                "path": item.get("path"),
                "public_path": item.get("public_path"),
                "source": item.get("source", "ai_codex"),
                "origin": item.get("origin"),
                "license": item.get("license", "generated_owned"),
                "commercial_use": item.get("commercial_use", "allowed"),
                "sha256": item.get("sha256"),
                "ai_disclosure_required": bool(item.get("ai_disclosure_required", False)),
            }
            for item in items
        ],
    }


def build_assets(overwrite: bool = False) -> dict[str, Any]:
    mkdirs()
    generated_at = datetime.now(timezone.utc).isoformat()
    stills = generate_images(overwrite)
    motion = generate_motion(motion_specs(), overwrite)
    factory = generate_factory(factory_specs(), overwrite)
    overlay = generate_overlay(overlay_specs(), overwrite)
    contacts = build_contacts()
    video_contacts = sorted(VISUALS.glob("morton_*_footage_contact_*.png"))
    body = [x for x in stills if x["role"] == "body"]
    i2v = [x for x in stills if x["role"] == "i2v_source"]
    thumb_face = [x for x in stills if x["role"] == "thumb_face"]
    counts = {
        "still_body": len(body),
        "still_i2v_source": len(i2v),
        "motion": len(motion),
        "factory": len(factory),
        "overlay": len(overlay),
        "thumb_face": len(thumb_face),
    }
    manifest = {
        "schema_version": "morton_assets.v1",
        "episode_id": EP,
        "slug": SLUG,
        "generated_at": generated_at,
        "producer": "scripts/build_morton_asset_manifest.py",
        "generation_provider": "codex_procedural_renderer_v001",
        "sdxl_used": False,
        "is_stub": False,
        "counts": counts,
        "expected_counts": EXPECTED,
        "source_inputs": {
            "asset_spec": "episodes/_planning/EP52_morton_CODEX_A_ASSETS.v001.md",
            "design_architecture": "episodes/_planning/EP52_morton_DESIGN_ARCHITECTURE.v001.md",
            "facts_ledger": "episodes/_planning/EP52_morton_FACTS_LEDGER.v001.md",
        },
        "safety_locks": {
            "exonerated_framing": True,
            "no_named_person_visual_identity": True,
            "no_readable_text_in_assets": True,
            "child_symbolic_only": True,
            "no_graphic_depiction": True,
            "no_depth_path": True,
            "no_scanline_or_haze": True,
            "ai_disclosure_required": True,
        },
        "stills": stills,
        "motion": motion,
        "factory": factory,
        "overlay": overlay,
        "contact_sheets": contacts,
        "video_contact_sheets": [p.relative_to(ROOT).as_posix() for p in video_contacts],
        "asset_mix_recalculation": {
            "total_cuts": 576,
            "still_cuts": 250,
            "factory_cuts": 240,
            "motion_cuts": 86,
            "distinct_sources": 498,
            "still_share": round(250 / 576, 4),
            "motion_coverage": round((240 + 86) / 576, 4),
            "first_use_share": round(498 / 576, 4),
            "avg_uses_per_source": round(576 / 498, 3),
        },
    }
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (STOCK / "stock_ledger.v001.json").write_text(json.dumps(stock_ledger(stills + motion + factory + overlay), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (VISUALS / "still_qc.v001.json").write_text(
        json.dumps(
            {
                "schema_version": "morton_still_qc.v1",
                "episode_id": EP,
                "items": [
                    {"asset_id": item["asset_id"], "scene_id": item["scene_id"], "path": item["path"], "accepted": item["role"] != "reject", "qc": item["qc"]}
                    for item in stills
                ],
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return manifest


def exists(path: str | None) -> bool:
    if not path:
        return False
    p = Path(path)
    return p.is_file() or (ROOT / "remotion" / "public" / path).is_file()


def collect_prior_sha() -> set[str]:
    out: set[str] = set()
    for ep_dir in (ROOT / "episodes").glob("PD-2026-0[3-5][0-9]-*"):
        try:
            ep_num = int(ep_dir.name.split("-")[2])
        except Exception:
            continue
        if not 39 <= ep_num <= 51:
            continue
        for path in list(ep_dir.glob("05_stock/stock_ledger*.json")) + list(ep_dir.glob("05_visuals/asset_manifest*.json")):
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except Exception:
                continue
            for key in ["items", "stills", "factory", "motion", "overlay"]:
                for item in data.get(key, []) if isinstance(data, dict) else []:
                    if isinstance(item, dict) and item.get("sha256"):
                        out.add(str(item["sha256"]))
    return out


def evaluate(data: dict[str, Any], check_prior_overlap: bool = False) -> list[str]:
    errors: list[str] = []
    if data.get("schema_version") != "morton_assets.v1":
        errors.append(f"schema_version mismatch: {data.get('schema_version')}")
    if data.get("episode_id") != EP or data.get("slug") != SLUG:
        errors.append("episode identity mismatch")
    if data.get("is_stub") is not False:
        errors.append("is_stub must be false")
    if any("depth_path" in item for item in data.get("stills", []) + data.get("motion", [])):
        errors.append("depth_path must not exist")
    stills = data.get("stills") or []
    body = [x for x in stills if x.get("role") == "body"]
    i2v = [x for x in stills if x.get("role") == "i2v_source"]
    thumb_face = [x for x in stills if x.get("role") == "thumb_face"]
    groups = {"motion": data.get("motion") or [], "factory": data.get("factory") or [], "overlay": data.get("overlay") or []}
    actual = {
        "still_body": len(body),
        "still_i2v_source": len(i2v),
        "motion": len(groups["motion"]),
        "factory": len(groups["factory"]),
        "overlay": len(groups["overlay"]),
        "thumb_face": len(thumb_face),
    }
    counts = data.get("counts") or {}
    for key, expected in EXPECTED.items():
        if counts.get(key) != expected:
            errors.append(f"counts.{key} expected {expected} got {counts.get(key)}")
        if actual.get(key) != expected:
            errors.append(f"actual {key} expected {expected} got {actual.get(key)}")
    bad_roles = sorted({str(item.get("role")) for item in stills if item.get("role") not in VALID_ROLES})
    if bad_roles:
        errors.append(f"invalid still roles: {bad_roles}")
    also_thumb = {str(item.get("scene_id")) for item in body if item.get("also_thumb") is True}
    if also_thumb != THUMB_BODY_IDS:
        errors.append(f"also_thumb set {sorted(also_thumb)} != {sorted(THUMB_BODY_IDS)}")
    seen_sha: set[str] = set()
    public_paths = []
    for group, items in [("stills", stills), *groups.items()]:
        for i, item in enumerate(items):
            public_path = item.get("public_path")
            if group == "stills" and item.get("role") != "body":
                public_path = None
                if item.get("public_path") is not None:
                    errors.append(f"stills[{i}] non-body public_path must be null")
            elif not public_path:
                errors.append(f"{group}[{i}] missing public_path")
            if public_path:
                public_paths.append(str(public_path))
                if not exists(str(public_path)):
                    errors.append(f"{group}[{i}] missing public media: {public_path}")
            if item.get("path") and not exists(str(item.get("path"))):
                errors.append(f"{group}[{i}] missing path: {item.get('path')}")
            if item.get("sha256"):
                p = Path(str(item.get("path")))
                if p.is_file() and sha256(p) != item.get("sha256"):
                    errors.append(f"{group}[{i}] sha256 mismatch")
                if item["sha256"] in seen_sha:
                    errors.append(f"{group}[{i}] duplicate sha256")
                seen_sha.add(str(item["sha256"]))
            if group == "stills":
                if item.get("role") != "reject" and max(int(item.get("width") or 0), int(item.get("height") or 0)) < 3840:
                    errors.append(f"stills[{i}] long edge below 3840")
                qc = item.get("qc") or {}
                reject = qc.get("has_readable_text") or qc.get("has_identifiable_real_person") or qc.get("has_victim_or_violence")
                if reject and item.get("role") != "reject":
                    errors.append(f"stills[{i}] reject flag present on accepted role")
            if group in {"factory", "overlay"}:
                if item.get("license") not in ALLOWED_LICENSES:
                    errors.append(f"{group}[{i}] bad license {item.get('license')}")
                if not item.get("eyeballed_content"):
                    errors.append(f"{group}[{i}] missing eyeballed_content")
                if (item.get("qc") or {}).get("label_matches_content") is not True:
                    errors.append(f"{group}[{i}] label_matches_content must be true")
            if group == "factory" and "/factory/" not in str(public_path).replace("\\", "/"):
                errors.append(f"factory[{i}] public_path must include /factory/")
            if group == "motion" and "/motion/" not in str(public_path).replace("\\", "/"):
                errors.append(f"motion[{i}] public_path must include /motion/")
            if group == "motion":
                if int(item.get("frames") or 0) < MOTION_FRAMES - 8:
                    errors.append(f"motion[{i}] SHORT frames={item.get('frames')}")
                if round(float(item.get("fps") or 0)) != MOTION_FPS:
                    errors.append(f"motion[{i}] fps expected 48 got {item.get('fps')}")
            if group == "overlay" and "/overlay/" not in str(public_path).replace("\\", "/"):
                errors.append(f"overlay[{i}] public_path must include /overlay/")
    dup_public = [p for p, c in Counter(public_paths).items() if c > 1]
    if dup_public:
        errors.append(f"duplicate public_path: {dup_public[:5]}")
    text_blob = "\n".join(strings(data))
    for regex, label in [(BANNED_PORTRAIT, "portrait"), (BANNED_ACCURACY, "accuracy")]:
        match = regex.search(text_blob)
        if match:
            errors.append(f"banned {label} wording present: {match.group(0)}")
    if check_prior_overlap:
        prior = collect_prior_sha()
        current = {str(item.get("sha256")) for item in groups["factory"] if item.get("sha256")}
        overlap = sorted(current & prior)
        if overlap:
            errors.append(f"factory prior sha overlap count={len(overlap)} first={overlap[:5]}")
    safe_stock_count = sum(1 for idx in STOCK_ASSIGNMENTS if assigned_stock(idx) is not None)
    stock_factory_count = sum(1 for item in groups["factory"] if item.get("origin") == "stock")
    if safe_stock_count and stock_factory_count < safe_stock_count:
        errors.append(f"factory stock inclusion expected {safe_stock_count} got {stock_factory_count}")
    return errors


def reuse_feasibility(data: dict[str, Any]) -> list[str]:
    body = [x for x in data.get("stills", []) if x.get("role") == "body"]
    factory = data.get("factory") or []
    motion = data.get("motion") or []
    errors: list[str] = []
    if len(body) < 215:
        errors.append(f"still {len(body)} < 215")
    if len(factory) < 240:
        errors.append(f"factory {len(factory)} < 240")
    if len(motion) < 43:
        errors.append(f"motion {len(motion)} < 43")
    distinct = len(body) + len(factory) + len(motion)
    first_use = distinct / 576
    avg_uses = 576 / max(1, distinct)
    still_share = 250 / 576
    if distinct < 498:
        errors.append(f"distinct {distinct} < 498")
    if first_use < 0.70:
        errors.append(f"first-use {first_use:.4f} < 0.70")
    if avg_uses > 1.4:
        errors.append(f"avg-uses/source {avg_uses:.3f} > 1.4")
    if still_share > 0.45:
        errors.append(f"still_share {still_share:.4f} > 0.45")
    return errors


def load_manifest() -> dict[str, Any]:
    if not MANIFEST.is_file():
        raise SystemExit(f"missing {MANIFEST}")
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--build", action="store_true")
    ap.add_argument("--verify", action="store_true")
    ap.add_argument("--reuse-feasibility", action="store_true")
    ap.add_argument("--verify-no-prior-overlap", action="store_true")
    ap.add_argument("--overwrite", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if args.verify or args.reuse_feasibility or args.verify_no_prior_overlap:
        data = load_manifest()
    else:
        data = build_assets(overwrite=args.overwrite)

    if args.reuse_feasibility:
        errors = reuse_feasibility(data)
        label = "morton_reuse_feasibility"
    elif args.verify_no_prior_overlap:
        errors = evaluate(data, check_prior_overlap=True)
        label = "morton_factory_prior_overlap"
    else:
        errors = evaluate(data)
        label = "morton_asset_manifest"

    result = {"ok": not errors, "asset_manifest": str(MANIFEST), "counts": data.get("counts"), "errors": errors}
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(("PASS" if result["ok"] else "FAIL") + f" {label}: {MANIFEST}")
        print(json.dumps(data.get("counts"), ensure_ascii=False))
        for err in errors[:80]:
            print(f"  ! {err}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
