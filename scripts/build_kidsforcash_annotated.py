#!/usr/bin/env python3
r"""Build the canonical annotated script for EP38 "Kids for Cash" (PD-2026-038-kidsforcash).

Idempotent. Run:  py -3.11 scripts/build_kidsforcash_annotated.py

What it does (no GPU, no render, no publish, no now()):
  1. Reads the fact-locked narration (episodes/.../06_audio/narration_index.v001.json).
  2. Applies the ED -> ENDING section rename to that index (atomic, only if needed), so the
     annotated chapter_id `ending` (normalizes to ENDING) and the narration section align in
     build_case_film_assets.build_span_time_windows / _norm_section.
  3. Splits each section's spoken narration into sentence/beat spans (SPN-00NN), groups them
     under the matching chapter, attaches the 13 on-screen cards to the right beats, writes a
     1-line director visual_intent, and attaches CLM-01..CLM-23 claim ids.
  4. Asserts each section's span texts, joined, reproduce the voiced spoken_text VERBATIM.
  5. Atomically writes episodes/.../03_script/script.annotated.v001.json and prints a report.

The output shape mirrors episodes/PD-2026-035-hinders/03_script/script.annotated.v001.json
exactly: top keys schema_version, episode_id, revision, language, thesis, viewer_promise,
chapters[], spans[], estimated_duration_seconds, qc_status.
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-038-kidsforcash"
EPDIR = ROOT / "episodes" / EP
NARR_INDEX = EPDIR / "06_audio" / "narration_index.v001.json"
OUT = EPDIR / "03_script" / "script.annotated.v001.json"

ESTIMATED_DURATION_SECONDS = 531  # narration master_duration_sec = 531.606


def atomic_write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, path)


def norm_section(s: str) -> str:
    """Match build_case_film_assets._norm_section, and treat ED as ENDING."""
    t = re.sub(r"[^a-z0-9]", "", (s or "").lower())
    if t.startswith("hook"):
        return "HOOK"
    if t.startswith("opening"):
        return "OPENING"
    if t.startswith("ending") or t == "ed":
        return "ENDING"
    m = re.match(r"act([ivx]+|\d+)$", t)
    if m:
        g = m.group(1)
        roman = {"i": 1, "ii": 2, "iii": 3, "iv": 4, "v": 5}
        n = int(g) if g.isdigit() else roman.get(g, 0)
        return f"ACT{n}"
    return t.upper()


def fix_narration_index_ed_to_ending(path: Path) -> bool:
    """Rename the ED chunk's section to ENDING (atomic). Idempotent. Returns True if changed."""
    doc = json.loads(path.read_text("utf-8"))
    changed = False
    for ch in doc.get("chunks", []):
        if ch.get("section") == "ED":
            ch["section"] = "ENDING"
            changed = True
    if changed:
        atomic_write_text(path, json.dumps(doc, ensure_ascii=False, indent=2) + "\n")
    return changed


# ---------------------------------------------------------------------------
# The 13 canonical on-screen cards (scene_plan v001 画面文字). Every one must land
# as on_screen_text on the beat that voices it. Used only for the coverage report.
# ---------------------------------------------------------------------------
CANONICAL_CARDS = [
    "3 MONTHS", "90 SECONDS", "NO LAWYER", "WAIVER OF COUNSEL", "8.4% vs ~50%",
    "$2.8 MILLION", "FINDER'S FEE -> BRIBE", "7-11x", "INVENTORY",
    "THOUSANDS VACATED", "17.5 YEARS", "28 YEARS", "$200 MILLION+",
]


# ---------------------------------------------------------------------------
# SPANS. Grouped by section. Each entry: (text, claim_ids, narrative_function,
# visual_intent, on_screen_text). SPN ids are assigned in order across sections.
# Span `text` is VERBATIM from the voiced narration (asserted below).
# ---------------------------------------------------------------------------
DASH = "—"  # em dash used throughout the voiced narration

SECTIONS: "list[tuple[str, list]]" = [
    ("hook", [
        ("In 2007, a seventeen-year-old girl in Pennsylvania built a fake web page that made fun of her assistant principal. It was a prank. She expected, at worst, detention.",
         ["CLM-10"], "hook_cold_open_prank",
         "Empty school hallway dissolving to a monitor-lit bedroom; a lone teen seen only from behind builds a harmless prank page, no face (S01/S02).",
         []),
        ("A judge sent her away for three months.",
         ["CLM-10"], "hook_disproportionate_sentence",
         "A towering empty judge's bench looms over a tiny child-sized silhouette; StampReveal drops 3 MONTHS on the sync word (S03).",
         ["3 MONTHS"]),
        (f"The hearing lasted about ninety seconds {DASH} and no one in that room told her she was allowed a lawyer.",
         ["CLM-10", "CLM-08"], "hook_ninety_seconds_no_counsel",
         "Tight on the vast bench; a NumberTicker snaps to 90 SECONDS and a NO LAWYER stamp lands on the sync words (S03).",
         ["90 SECONDS", "NO LAWYER"]),
        ("The rest, she would not learn for years: that the judge who signed her order was being paid by the jail that took her in. Paid for every child he sent through its doors.",
         ["CLM-06", "CLM-20"], "hook_reveal_corruption",
         "Shadowed hands pass a thick envelope of cash under a desk beside an out-of-focus gavel; the corruption seeded just before the OP title (S07).",
         []),
    ]),
    ("act1", [
        ("Luzerne County, Pennsylvania. Coal country, long after the coal. In the city of Wilkes-Barre stood a courthouse that was supposed to be the one place a kid who went wrong could be set right.",
         ["CLM-01"], "setup_place_and_promise",
         "Coal-country courthouse at dusk, slow pull-in to push-in; LowerThird 'Luzerne County, PA' (S21).",
         []),
        ("The children who passed through it had done small things. A shoving match in a hallway. Twenty dollars of stolen makeup. A rude page online. The kind of thing that, almost anywhere else, ends with a warning and a ride home.",
         [], "setup_minor_offenses",
         "Quick-cut montage of ordinary teen life dissolving to an emptied school desk; small, harmless things (S24/S02).",
         []),
        ("Here it began with a signature. A child was handed a form giving up the right to a lawyer " + DASH + " and it was handed over the way you'd pass someone a receipt, as if it were nothing. No one explained what it meant. And so the children, young and scared and taught to trust the adults in the room, signed away the one protection that might have saved them.",
         ["CLM-08"], "mechanism_waiver_of_counsel",
         "Close on a child's hand at a waiver form, micro-motion of the pen; StampReveal locks WAIVER OF COUNSEL on the sync word (S22).",
         ["WAIVER OF COUNSEL"]),
        ("Then came a man in a robe named Mark Ciavarella.",
         ["CLM-02"], "introduce_ciavarella",
         "Low up-angle on a robed silhouette behind the bench, face unseen; LowerThird 'Mark Ciavarella — Juvenile Court Judge' (S03).",
         []),
        ("Half of the children who signed that form left his courtroom in handcuffs, bound for a locked facility. In the rest of the state, that number was eight in a hundred.",
         ["CLM-08"], "contrast_placement_rate",
         "ComparisonBars build the disparity as the numbers are voiced: ~50% here against 8.4% statewide (S26).",
         ["8.4% vs ~50%"]),
        ("And placement was not a slap on the wrist. It meant being taken that same day " + DASH + " cuffed, photographed, driven hours from home, and left to sleep behind a locked door for weeks or months. Missing school. Missing a parent's face. Learning to think of yourself as an inmate before you were old enough to drive.",
         ["CLM-04"], "stakes_what_placement_meant",
         "Fast three-cut chain: handcuffed wrists to a transport window to a cold barred cell (S04/S25/S06).",
         []),
        ("It was fast, too. A minute. Two. A boy could be named a delinquent and led out a side door before his mother rose from her seat. Some parents drove home and only understood, hours later, that they would not be tucking their child in that night " + DASH + " or for many nights after. There were no long deliberations, no weighing of the evidence. There was a decision that seemed to have been made before anyone walked in.",
         [], "stakes_speed_of_hearings",
         "A side door swings shut on the sync words 'a minute, two'; a parent's empty seat holds in the frame (S23).",
         []),
        ("And still the parents believed it was justice, because who doesn't believe a judge? That belief " + DASH + " that a courtroom is a safe place to bring your child " + DASH + " was the first thing being sold.",
         [], "act1_close_belief_sold",
         "A parent silhouette watching from the gallery, trusting; the word 'sold' hangs over the courtroom (S11/S23).",
         []),
    ]),
    ("act2", [
        ("To see what was really happening, follow the money. It starts one floor up.",
         [], "act2_open_follow_the_money",
         "Dolly-in on the president judge's empty power chair, one floor above the juvenile court (S28).",
         []),
        ("There were two judges. Ciavarella, in the juvenile court. And Michael Conahan, the president judge " + DASH + " the one who held the county's checkbook.",
         ["CLM-02"], "introduce_conahan",
         "Two-tier composition of bench over bench; LowerThird 'Michael Conahan — President Judge' (S28).",
         []),
        ("The county ran its own juvenile detention center, paid for with tax dollars. Conahan starved it of funding and moved it toward the door.",
         ["CLM-07"], "mechanism_defund_public",
         "The public county facility's lights go dark behind a padlocked gate (S09/S29).",
         []),
        ("He went further: he put his name to an agreement that guaranteed a steady stream of children to a brand-new, private, for-profit jail. A guarantee. In writing. That a certain number of kids would be needed.",
         ["CLM-19", "CLM-04"], "mechanism_placement_guarantee",
         "A signed agreement (illegible) lit hard; a for-profit facility exterior behind razor wire (S15/S05).",
         []),
        ("A for-profit jail lives by one number. Empty beds cost money; full beds make it. And now someone had promised the beds would be full.",
         ["CLM-04"], "mechanism_beds_economics",
         "Cold institutional facility exterior, light and air moving; empty bunks implied as inventory (S05).",
         []),
        ("They were filled the only way they could be " + DASH + " one child at a time, by the judge down the hall.",
         ["CLM-04"], "mechanism_children_as_supply",
         "The core cut: faceless child-sized silhouettes processed into a building, each reduced to a number (S08).",
         []),
        ("A developer named Robert Mericle built those facilities. An attorney named Robert Powell owned and ran them. Across roughly three years, the two men passed about two point eight million dollars to the judges.",
         ["CLM-05", "CLM-06"], "mechanism_money_flow_total",
         "MoneyFlow traces the path facility -> judges; NumberTicker counts up to the $2.8 MILLION card (S30).",
         ["$2.8 MILLION"]),
        ("It didn't move in open daylight; it moved through side accounts and quiet transfers, dressed up as a \"finder's fee.\" A referral. Money, they said, for helping the places get built and kept busy.",
         ["CLM-20"], "mechanism_disguised_transfers",
         "StampReveal prints FINDER'S FEE then overstrikes it to BRIBE on the sync words (S15).",
         ["FINDER'S FEE -> BRIBE"]),
        ("Take the language away and it is very simple. A child walked in. A judge sent that child to a cell. A payment followed.",
         [], "mechanism_plain_summary",
         "Three stark beats on a single shadowed money-and-gavel bed: walked in, to a cell, a payment (S07).",
         []),
        ("And the children who came without a lawyer? In that courtroom they appeared seven to eleven times more often than anywhere else in the state " + DASH + " because a child with no lawyer is a child who cannot fight back.",
         ["CLM-09"], "mechanism_no_lawyer_multiplier",
         "RadialGauge / NumberTicker resolves 7-11x, power against a small silhouette (S18).",
         ["7-11x"]),
        ("Every hearing that felt too quick was not impatience on the bench. It was inventory.",
         [], "mechanism_inventory_reframe",
         "Push past the fast bench to a records shelf; a small INVENTORY stamp lands on the word (S17).",
         ["INVENTORY"]),
        ("And it did not happen once. It happened morning after morning, for years, until the children who had been fed into those private beds numbered in the thousands. No one pulled the alarm, because on paper each of those hearings looked perfectly legal " + DASH + " a judge, a courtroom, a signature. The machine hid inside the shape of ordinary justice.",
         ["CLM-03", "CLM-23"], "act2_close_scale_hidden",
         "The same hearing repeats and multiplies into thousands, hidden inside the shape of ordinary justice (S08/S17).",
         []),
    ]),
    ("act3", [
        ("A number this size goes silent. So stand in one house.",
         [], "act3_open_from_number_to_person",
         "The scale falls away to one quiet family home; a slow, reverent push toward an empty seat (S27).",
         []),
        ("Ed Kenzakoski was seventeen. A wrestler, with a father who had a future picked out for him. He came before Ciavarella on a small charge, and he was sent away.",
         ["CLM-11"], "introduce_kenzakoski",
         "A young man's absence implied, never his face; LowerThird 'Edward Kenzakoski, 17' (S24/S06).",
         []),
        ("His mother is Sandy Fonzo. And when Ciavarella walked down the steps of a federal courthouse years later " + DASH + " a defendant now, out on bail, calm in a dark suit " + DASH + " she was there. She met him on the pavement in front of the cameras, grief turned to fury, and demanded to know how the man who had broken her son could stand there and say he'd done nothing wrong. He fixed his tie and looked past her. He had nothing. There is nothing to say.",
         ["CLM-12"], "confrontation_fonzo",
         "The courthouse-steps confrontation staged in silhouette; LowerThird 'Sandy Fonzo — his mother' (S33).",
         []),
        ("Now set that against the size of it. Thousands of children told, at thirteen, at fifteen, that they were criminals " + DASH + " and, being children, believing it. Some came out and never found their footing. A record that trailed them onto every job form and every college application, quietly closing doors they never saw close.",
         ["CLM-23"], "scale_thousands_marked",
         "Cut-cadence over a wall of records; doors quietly closing on unseen futures (S18/S17).",
         []),
        ("Years later, grown now, some of them would sit in front of cameras and try to explain what it does to a person to be sold at fifteen. Some still can't. That is the part no ruling returns and no settlement buys back.",
         [], "act3_close_unreturnable",
         "An empty chair by a fading window holds; the loss no ruling gives back (S10).",
         []),
    ]),
    ("act4", [
        ("For years it held " + DASH + " because of who was doing the complaining. A kid with a record. A parent who \"should have raised them better.\" Easy voices to wave off. And they were waved off, again and again.",
         [], "act4_open_easy_to_dismiss",
         "A corrupt bureaucratic system of identical drawers vanishing into shadow; complaints waved off (S17).",
         []),
        ("Then one more mother picked up the phone " + DASH + " and called a small nonprofit in Philadelphia, the Juvenile Law Center. Its lawyers pulled the files expecting a few heavy-handed sentences. They found a machine: hundreds of children, the same pattern each time " + DASH + " minutes in the room, no lawyer, straight to the same private beds.",
         ["CLM-13"], "turn_juvenile_law_center",
         "A phone call to a modest law office; MechanismReveal exposes the repeating pattern; LowerThird 'Juvenile Law Center, Philadelphia' (S31).",
         []),
        ("At the same time, federal investigators were quietly building their own case, following the money the judges thought no one could see.",
         ["CLM-21"], "turn_federal_probe",
         "A quiet federal investigation traces the hidden money the judges thought was invisible (S31).",
         []),
        ("And it might all have stayed buried " + DASH + " a local story, a few angry parents easy to ignore " + DASH + " if the families had not refused to go quiet, and if, later, a documentary had not put their faces on a screen and made the rest of the country finally look. For the first time, the children in those files stopped being case numbers. They were somebody's kid. They had names.",
         ["CLM-22"], "turn_families_and_documentary",
         "Case numbers resolve into named, human faces on a screen; the country finally looks (S18).",
         []),
        ("The Juvenile Law Center took it to the Pennsylvania Supreme Court, and the court did a rare thing. It reached back into Ciavarella's courtroom and unmade it " + DASH + " throwing out thousands of adjudications, clearing the records of as many as several thousand children. The state, in plain terms, admitting that none of it should ever have counted.",
         ["CLM-14"], "payoff_records_vacated",
         "RecordsScan sweeps files dissolving into light; THOUSANDS VACATED card holds (exact count not burned) (S13).",
         ["THOUSANDS VACATED"]),
        ("But a cleared record is not a returned childhood. Behind each of those cases was a year, or two, or three, that the county had already spent " + DASH + " nights in a cell that no order could give back. The paperwork could be erased. The time could not.",
         [], "payoff_time_not_returned",
         "Records lift away but the empty cell and the lost years remain (S13/S06).",
         []),
        ("Then the law turned on the men who had sold it. Michael Conahan pleaded guilty to racketeering; seventeen and a half years.",
         ["CLM-15"], "reckoning_conahan",
         "A robe hangs in shadow as an accusing light falls; NumberTicker resolves 17.5 YEARS (S14/S35).",
         ["17.5 YEARS"]),
        ("Ciavarella refused to fold " + DASH + " he insisted the money was a legal finder's fee, not a bribe, that he had never sentenced a child for cash. A jury heard him out and convicted him anyway, on racketeering and corruption, and he was given twenty-eight years.",
         ["CLM-15"], "reckoning_ciavarella",
         "VerdictReversal with a NumberTicker slamming to 28 YEARS on the sync word (S35).",
         ["28 YEARS"]),
        ("Later, a court ordered the two of them to pay more than two hundred million dollars to the families they had harmed.",
         ["CLM-16"], "reckoning_damages",
         "NumberTicker counts up to the $200 MILLION+ damages card (S15/S30).",
         ["$200 MILLION+"]),
        ("It was, at last, a kind of justice " + DASH + " and it forced a change: Pennsylvania moved to make sure a child standing in a courtroom actually has a lawyer at their side. But ask Sandy Fonzo if it was enough.",
         ["CLM-18"], "act4_close_reform_but",
         "Warm light as a lawyer stands beside a child; the reform tempered by Fonzo's unanswered grief (S36).",
         []),
    ]),
    ("ending", [
        ("We like to believe a courtroom is the one room where the money stays outside the door. That the people with power are held to a higher line than the rest of us.",
         [], "ending_theme_statement",
         "A solemn courthouse exterior at dusk, gold on marble; the promise the law is supposed to keep (S12).",
         []),
        ("For thousands of children in one American county, that line had a price. It worked out to a few thousand dollars a head.",
         ["CLM-23"], "ending_the_price",
         "The comparison motif returns: a few thousand dollars set against one small silhouette (S26/S08).",
         []),
        ("The judges are named and gone. One spent years in prison. The other, quietly, was granted an early release and walked back out into the world while the children he sentenced were still carrying theirs.",
         ["CLM-17"], "ending_uneven_endings",
         "One cell door closes, another opens; LowerThird 'Conahan — sentence commuted, 2024' (S35/S20).",
         []),
        ("Because that is the last, hardest truth of this story: the men could be punished, and still the years don't come back.",
         [], "ending_hardest_truth",
         "A golden line of light across a dark marble floor; punishment cannot return the years (S20).",
         []),
        ("If this is a story that should be seen and not buried, subscribe " + DASH + " the next one opens the way this one did: an ordinary person, and a system that was never meant to reach them. Because the distance between a family like yours and a family like theirs is far shorter than we let ourselves believe.",
         [], "ending_earned_cta_next_arc",
         "A calm suburban street with a distant unmarked car; word-synced subscribe CTA into the Bookends ED (S19/S20).",
         []),
    ]),
]

CHAPTER_META = {
    "hook": ("Hook", "cold_open_hook_narrated"),
    "opening": ("Opening", "op_title_card_no_vo"),
    "act1": ("Ordinary Children", "setup_absurdity"),
    "act2": ("The Machine", "mechanism_money_flow"),
    "act3": ("One House", "human_cost"),
    "act4": ("Exposed", "turn_and_reckoning"),
    "ending": ("Ending", "earned_cta_and_next_arc"),
}
# Chapter render order (opening sits between hook and act1; it carries no spans).
CHAPTER_ORDER = ["hook", "opening", "act1", "act2", "act3", "act4", "ending"]

THESIS = (
    "Two Pennsylvania judges turned a juvenile courtroom into a supply line for a private, "
    "for-profit jail—taking roughly $2.8 million while sending thousands of children away, "
    "many without a lawyer and in hearings that lasted seconds—until a nonprofit, federal "
    "investigators, and grieving families forced the state to vacate the cases and convict the "
    "judges, though nothing gave the children back the years they lost."
)
VIEWER_PROMISE = (
    "You will see exactly how a court that was supposed to protect children was run as a cash "
    "business—how the money moved, why kids signed away their right to a lawyer, what finally "
    "exposed it, and why even a conviction and a reform could not undo what it cost one family."
)


def build():
    sys.stdout.reconfigure(encoding="utf-8")

    ed_changed = fix_narration_index_ed_to_ending(NARR_INDEX)

    idx = json.loads(NARR_INDEX.read_text("utf-8"))
    section_text = {}
    for ch in idx["chunks"]:
        section_text[norm_section(ch["section"])] = ch["spoken_text"]

    spans = []
    chapters_spans = {cid: [] for cid, _ in SECTIONS} | {"opening": []}
    n = 0
    for chapter_id, beats in SECTIONS:
        for text, claims, nf, vi, ost in beats:
            n += 1
            sid = f"SPN-{n:04d}"
            spans.append({
                "span_id": sid,
                "text": text,
                "claim_ids": claims,
                "narrative_function": nf,
                "visual_intent": vi,
                "on_screen_text": ost,
            })
            chapters_spans[chapter_id].append(sid)

    # --- VERBATIM assertion: joined span texts must equal the voiced spoken_text ---
    def norm_ws(s: str) -> str:
        return re.sub(r"\s+", " ", s).strip()

    for chapter_id, beats in SECTIONS:
        key = norm_section(chapter_id)
        joined = norm_ws(" ".join(t for (t, *_rest) in beats))
        source = norm_ws(section_text[key])
        if joined != source:
            # find first divergence for a helpful message
            i = next((k for k in range(min(len(joined), len(source))) if joined[k] != source[k]),
                     min(len(joined), len(source)))
            raise SystemExit(
                f"VERBATIM MISMATCH in section {key} (chapter {chapter_id}) at char {i}:\n"
                f"  built : ...{joined[max(0,i-40):i+40]!r}...\n"
                f"  source: ...{source[max(0,i-40):i+40]!r}...")

    chapters = []
    for cid in CHAPTER_ORDER:
        title, function = CHAPTER_META[cid]
        chapters.append({
            "chapter_id": cid,
            "title": title,
            "function": function,
            "span_ids": chapters_spans[cid],
        })

    doc = {
        "schema_version": "1.0.0",
        "episode_id": EP,
        "revision": "v001",
        "language": "en",
        "thesis": THESIS,
        "viewer_promise": VIEWER_PROMISE,
        "chapters": chapters,
        "spans": spans,
        "estimated_duration_seconds": ESTIMATED_DURATION_SECONDS,
        "qc_status": "review",
    }
    atomic_write_text(OUT, json.dumps(doc, ensure_ascii=False, indent=2) + "\n")

    # ---------------- report ----------------
    print(f"ED->ENDING rename applied to narration_index: "
          f"{'YES (changed)' if ed_changed else 'already ENDING (no change)'}")
    ending_sections = {norm_section(ch["section"]) for ch in idx["chunks"]}
    print(f"narration sections now: {sorted(ending_sections)}")
    print()
    print("spans per chapter:")
    total = 0
    for ch in chapters:
        c = len(ch["span_ids"])
        total += c
        print(f"  {ch['chapter_id']:8s} ({norm_section(ch['chapter_id'])}): {c}")
    print(f"total spans: {total}")
    print()

    # card coverage
    def flat_ost():
        s = set()
        for sp in spans:
            for line in sp["on_screen_text"]:
                s.add(line)
        return s
    present = flat_ost()
    missing_cards = [c for c in CANONICAL_CARDS if c not in present]
    print(f"canonical cards placed: {len(CANONICAL_CARDS) - len(missing_cards)}/{len(CANONICAL_CARDS)}"
          + ("" if not missing_cards else f"  MISSING: {missing_cards}"))
    no_card = [sp["span_id"] for sp in spans if not sp["on_screen_text"]]
    print(f"spans with NO on-screen card ({len(no_card)}): {', '.join(no_card)}")
    print()

    # section coverage vs chapters
    narr_keys = {norm_section(ch["section"]) for ch in idx["chunks"]}
    chap_keys = {norm_section(c["chapter_id"]) for c in chapters if c["span_ids"]}
    unmapped = narr_keys - chap_keys
    print(f"narration section keys: {sorted(narr_keys)}")
    print(f"chapter keys (with spans): {sorted(chap_keys)}")
    print(f"every narration section maps to a chapter: {'YES' if not unmapped else 'NO ' + str(unmapped)}")
    print()
    print(f"wrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(build())
