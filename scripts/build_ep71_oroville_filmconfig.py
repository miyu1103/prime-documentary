#!/usr/bin/env python3
"""Emit episodes/_planning/EP71_oroville_filmconfig.v001.json.

Authored 2026-08-18 from EP71_oroville_FILM_BIBLE.v001.md and the facts ledger. Binding
disciplines from the ledger's own quarantine table:

- THE DAM DID NOT FAIL and nobody died (SP-04) -- no card implies otherwise.
- COUNTIES ordered the evacuations; the DEFENDANT is the State through DWR (OR-07) -- never
  conflated on any card.
- What the evacuation cost Denise Johnson appears nowhere retrieved (DJ-06) -- the film states
  the absence; no card invents a figure.
- "Officials ignored warnings" is CNN's characterisation, not a finding (FR-05) -- the 2005
  motion is carded as a filing, not as vindication.
- No settlement or judgment for any individual evacuee was found (GC-02) -- carded as an
  established absence, which is the film's ending.
- The 2023 win that WAS affirmed belongs to fish (AF-01..03) -- the sharpest card in the film
  and it is verbatim-grounded.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-071-oroville"
SLUG = "oroville"

CA3 = "Bechtel v. Department of Water Resources, Cal. Ct. App., Third District, 15 March 2022 (unpublished)"
TRIAL = "the trial court's class-certification ruling, as quoted by the Court of Appeal"
CMPL3 = "master complaint, Oroville Dam Cases (allegations)"
OES = "Cal OES After Action Report, 2017"
SAC = "Sacramento Bee interview, February 2017"
FISH = "Oroville Dam Cases, No. C093600, Cal. Ct. App., 5 October 2023"


def L3(p, s):  return {"kind": "lowerthird", "primary": p, "secondary": s}
def KIN(lines, emph): return {"kind": "kinetic", "lines": lines, "style": "emphasis", "emphasisWords": emph}
def Q(q, a):   return {"kind": "quote", "quote": q, "attribution": a}
def NT(v, label, **kw): return {"kind": "numberticker", "value": v, "label": label, **kw}
def ST(v, label): return {"kind": "stat", "value": v, "label": label}
def CT(evts):   return {"kind": "casetimeline_c", "events": evts}


BEATS: dict[str, list[tuple[dict, list[str]]]] = {}

BEATS["HOOK"] = [
    (L3("AI-assisted visualization", "symbolic reconstruction, no real likenesses"), []),
    (KIN(["12 FEBRUARY 2017.", "A SUPERMARKET IN OROVILLE."], ["12 FEBRUARY 2017"]),
     ["DJ-01", "DJ-03"]),
]

BEATS["OP"] = [
    (KIN(["188,000 PEOPLE WERE ORDERED OUT.", "THIS IS WHAT THE COURT SAID THAT WAS WORTH."],
         ["188,000"]), ["CL-01", "CT-09"]),
]

BEATS["ACT_1"] = [
    (L3("OROVILLE DAM, BUTTE COUNTY",
        "The tallest dam in the United States holds back the Feather River above the town."), ["SP-03"]),
    (L3("4:10 P.M. — BUTTE COUNTY",
        "Evacuation of 'the low levels of Oroville and areas downstream.' The county's words, to the minute."),
     ["OR-01"]),
    (Q("[O]fficials now anticipate a failure of the Auxiliary Spillway at Oroville Dam within the "
       "next 60 minutes.", "Butte County's second broadcast, approx. 4:34 p.m."), ["OR-02"]),
    (L3("4:59 P.M. — YUBA COUNTY", "Evacuation of all Yuba County on the valley floor."), ["OR-03"]),
    (L3("6:03 P.M. — SUTTER COUNTY",
        "Immediate evacuation: Live Oak, Yuba City, Nicolaus, and other communities along the Feather "
        "River."), ["OR-04"]),
    (L3("THE SUPERMARKET",
        "Denise Johnson was walking in when the shop announced it was closing for a mandatory "
        "evacuation — her sworn declaration."), ["DJ-03", "DJ-04"]),
    (L3("3:00 P.M. — THE TELEVISION",
        "Francis Bechtel saw a mandatory evacuation order on his screen an hour and ten minutes "
        "before the county's first order. Why is not explained in anything retrieved."),
     ["FB-02", "FB-04", "FB-05"]),
    (ST(15, "Minutes after the broadcast, a sheriff's vehicle came down his street announcing that "
            "residents had to leave — his declaration"), ["FB-03"]),
    (Q("It was just panic. People were running in the streets. Cars were speeding.",
       "Genoa Widener, Oroville resident, contemporaneous press interview"), ["GW-01"]),
    (L3("THE DAM DID NOT FAIL",
        "No flood reached a town. Nobody died and nobody was hurt. The film says so now, on purpose."),
     ["SP-04"]),
    (L3("14 FEBRUARY 2017", "The orders were reduced to a warning. Two days."), ["OR-06"]),
    (KIN(["THE ORDER NEVER NAMED", "ANYWHERE IN PARTICULAR."], ["ANYWHERE IN PARTICULAR"]),
     ["CT-02"]),
]

BEATS["ACT_2"] = [
    (L3("7 FEBRUARY 2017 — FIVE DAYS EARLIER",
        "A section of concrete eroded from the middle of the main spillway. DWR's own photograph is "
        "timestamped."), ["SP-01"]),
    (L3("11 FEBRUARY — THE AFTERNOON BEFORE",
        "Water flowed over the emergency spillway. DWR's own video of that afternoon exists."),
     ["SP-02", "SP-03"]),
    (L3("17 OCTOBER 2005",
        "Friends of the River, the Sierra Club and the South Yuba River Citizens League file a motion "
        "with federal regulators about this exact spillway."), ["FR-01"]),
    (Q("We urged them to put concrete on the spillway – our argument was that without a proper "
       "spillway, this could happen.", "Ron Stork, policy director, Friends of the River"), ["FR-02"]),
    (Q("It was a slow moving crisis that picked up a lot of speed yesterday.",
       "Ron Stork, Friends of the River"), ["FR-03"]),
    (L3("WHAT THIS FILM DOES NOT SAY",
        "'Officials ignored warnings' is a headline's characterisation. No tribunal has found it. "
        "The filing is a fact; the verdict on it is nobody's yet."), ["FR-05"]),
    (ST(12, "Years between the 2005 motion and the February 2017 orders — our arithmetic, from "
            "the record's dates"), ["FR-01", "OR-01"]),
    (L3("PROJECT NO. 2100-052",
        "The federal docket the 2005 motion lives in. The motion itself was not retrieved; this film "
        "quotes nothing from it."), ["FR-04"]),
    (KIN(["THE CONCRETE GAVE WAY", "FIVE DAYS BEFORE THE ORDER."], ["FIVE DAYS"]),
     ["SP-01", "OR-01"]),
    (L3("THE ISSUERS AND THE DEFENDANT",
        "Counties issued the orders. The lawsuit's defendant is the State, through the Department of "
        "Water Resources. The two are not the same and this film never blurs them."), ["OR-07"]),
]

BEATS["ACT_3"] = [
    (L3("THE FAIRGROUNDS",
        "Shelters stood at fairgrounds in surrounding unaffected areas — Chico among them. The state's "
        "own after-action report."), ["SH-01"]),
    (Q("Many of the people, especially low income, ran out with just the shirts on their backs.",
       "Bob Mulholland, volunteer, Silver Dollar Fairgrounds shelter"), ["SH-02"]),
    (L3("THREE WEEKS IN THE APARTMENT",
        "Kaysi and Greg Levias, two boys and a dog, had moved in three weeks earlier. What didn't fit "
        "in the car they piled as high as they could."), ["LV-01", "LV-02"]),
    (L3("THE RANCH",
        "Nicoli Nicholas moved hundreds of cattle, tons of baled hay and his equipment out of Sutter "
        "County — the complaint's account."), ["NN-01", "NN-02"]),
    (NT(150000, "Dollars, at least, in relocation and return costs for the ranch — the complaint's "
                "figure, stated as an allegation", group=True), ["NN-02"]),
    (L3("THE CALVES",
        "On the rented pastures the cows caught a virus; back home, their newborn calves were infected "
        "— the complaint's account."), ["NN-03", "NN-04"]),
    (ST(6, "Rental homes directly downstream in which Jeanette Morton alleges a loss of value"),
     ["JM-01"]),
    (L3("DOWNTOWN OROVILLE",
        "A brewing company closed for about a week — roughly ten thousand dollars, its CFO estimated, "
        "and slow to come back."), ["CP-01", "CP-02"]),
    (L3("POMONA AVENUE",
        "Two day-care centres — one for ages two to five, one for under-threes — forced to suspend "
        "business. The complaint's account."), ["DC-01"]),
    (L3("9 AUGUST 2017",
        "Jeanette Morton files a claim with the State under Government Code section 910. The paperwork "
        "begins."), ["JM-02"]),
]

BEATS["ACT_4"] = [
    (L3("THE CLASS",
        "Approximately 188,000 residents of Oroville, Marysville, Yuba City and other areas near the "
        "Feather River who were ordered to evacuate."), ["CL-01"]),
    (L3("WHAT THEY ASKED FOR",
        "Out-of-pocket expenses for the two-day evacuation, and the value of the lost days — not the "
        "dam, not the spillway, the two days."), ["CL-02"]),
    (L3("THE RULING",
        "Ninety pages. Two plaintiff groups denied class status. Only Bechtel appealed."), ["CL-03"]),
    (Q("There is simply no means by which to readily determine whether a residence or person falls "
       "within a 'mandatory' evacuation zone.", TRIAL), ["CT-04"]),
    (Q("In fact, the evidence and briefing submitted to the trial court demonstrated there was no "
       "defined mandatory evacuation zone and no defined voluntary evacuation zone.", CA3), ["CT-01"]),
    (L3("THE VAGUE AREAS",
        "'Low levels of Oroville and areas downstream.' The orders' own words, read back by the court "
        "as the reason no class can exist."), ["CT-02"]),
    (L3("THE STATE'S EXPERT",
        "Dr. Cova, an expert on human evacuations: the decision to evacuate is left to each household. "
        "There is no known method to count who left."), ["CT-06", "CT-07", "CT-08"]),
    (L3("AND THE STATE'S OTHER ARGUMENT",
        "DWR argued below that even a 'mandatory' evacuation was not actually mandatory — there is no "
        "penalty for ignoring the order."), ["CT-12"]),
    (KIN(["EVERYONE WAS ORDERED OUT.", "AND NO ONE CAN SAY WHO."], ["NO ONE CAN SAY WHO"]),
     ["CT-04", "CT-08"]),
    (Q("This lack of ascertainability would also prevent individual class members from "
       "self-identifying as meeting the class definition.", CA3), ["CT-03"]),
    (Q("[B]ecause there simply is no typical claim among this group, the Court cannot say that the "
       "proposed Plaintiffs have claims typical of the class.", TRIAL), ["CT-05"]),
    (L3("15 MARCH 2022",
        "The judgment is affirmed. The Department of Water Resources shall recover its costs on appeal."),
     ["CT-09", "CT-11"]),
]

BEATS["ACT_5"] = [
    (L3("NOT TO BE PUBLISHED",
        "The opinion is marked unpublished. California's rules prohibit citing it. The rule that "
        "decided 188,000 people's case binds nobody else."), ["CT-10", "CL-01"]),
    (L3("WHAT DENISE JOHNSON LOST",
        "What the evacuation cost her appears nowhere in anything retrieved. The record does not say. "
        "So neither does this film."), ["DJ-06"]),
    (L3("5 OCTOBER 2023 — THE CASE THAT DID WIN",
        "The same Court of Appeal holds DWR liable — in the action the Butte County District Attorney "
        "brought over the river itself."), ["AF-01", "AF-02"]),
    (L3("READ THE WINNING OPINION FOR THE PEOPLE",
        "27,810 characters. 'Evacuate' appears zero times. 'Resident' appears zero times. The win "
        "belongs to the fish."), ["AF-03"]),
    (L3("THE LEDGER, CLOSED",
        "No settlement, verdict or judgment for an individual evacuee was found in any source "
        "retrieved. An established absence."), ["GC-02"]),
    (ST(37, "Pages of scanned government claim forms, public, their names too degraded to read"),
     ["GC-01"]),
    (ST(90, "Pages in the trial-court ruling that ended the class — a ruling not retrievable from "
            "any open source tried"), ["CL-03", "CL-04"]),
    (L3("KLEIN AND RAMIREZ",
        "The other two class representatives. Their declarations were not retrieved; the film tells "
        "this story in two voices, and says so."), ["CR-01", "CR-02", "OQ-02"]),
    (L3("THE ONES WHO DID NOT APPEAL",
        "Marie Giordano, above the dam with three rentals downstream, and the Giordano plaintiffs: "
        "denied alongside Bechtel, and their case ended there."), ["CL-05", "CL-03"]),
    (CT([
        {"label": "regulators asked to line the spillway", "value": "17 Oct 2005"},
        {"label": "spillway concrete erodes", "value": "7 Feb 2017"},
        {"label": "the orders, county by county", "value": "12 Feb 2017"},
        {"label": "orders reduced to a warning", "value": "14 Feb 2017"},
        {"label": "Morton files her claim", "value": "9 Aug 2017"},
        {"label": "class denied, affirmed", "value": "15 Mar 2022"},
        {"label": "DWR liable — to the fish", "value": "5 Oct 2023"},
    ]), ["FR-01", "SP-01", "OR-01", "OR-06", "JM-02", "CT-09", "AF-01"]),
]

BEATS["ENDING"] = [
    (KIN(["THE ORDER WAS FOR EVERYONE.", "THE REMEDY WAS FOR NO ONE."], ["FOR NO ONE"]),
     ["CL-01", "GC-02"]),
    (L3("THE HIDDEN RULE",
        "An order vague enough to move 188,000 people can be too vague to owe any one of them anything."),
     ["CT-02", "CT-04", "GC-02"]),
]

NOTES = [
    "SP-04 IS LOAD-BEARING: an ACT_1 card states on screen that the dam did not fail and nobody was "
    "hurt, before any legal beat. Nothing later may imply otherwise.",
    "OR-07: the issuers-vs-defendant card is in ACT_2 so the viewer carries the distinction into the "
    "courtroom acts. No card calls the counties defendants or DWR the issuer.",
    "FR-05: the 2005 filing is carded as a filing plus Stork's own words. The 'ignored warnings' "
    "characterisation appears only inside the card that disclaims it.",
    "DJ-06 / GC-02 / CL-04 are ABSENCES and are carded as absences -- the film's honesty is that the "
    "record runs out, and the cards say so instead of papering over it.",
    "AF-03: the fish card quotes the grep result (zero occurrences) exactly as measured.",
    "MONEY FIGURES ($150,000, ~$10,000, six homes) are attributed to the complaint or the speaker on "
    "the card itself; none is stated as a court finding.",
]

DECLARED = {
    "leadSeconds": "0 -- the hook is voiced from frame 0.",
    "openingVariant": "'overlay' -- brand band over the hook's settle; voice does not stop.",
    "captionLeadSeconds": "0.0 -- captions.final.v001.srt already carries the house 0.60 s lead.",
    "hookSeconds": "measured: the sum of HOOK-section chunk durations in narration_index.v001.json.",
    "designedSilence": "3.0 s hold on the disposition card in ACT_5 (bible structure table).",
}


def main() -> int:
    idx = json.loads((ROOT / "episodes" / EP / "06_audio" / "narration_index.v001.json")
                     .read_text(encoding="utf-8"))
    hook = round(sum(c.get("duration", c.get("seconds", 0)) for c in idx.get("chunks", [])
                     if c.get("section") == "HOOK"), 3)
    first_hook = next((c.get("spoken_text", "") for c in idx.get("chunks", [])
                       if c.get("section") == "HOOK"), "")
    cfg = {
        "schema_version": "pd_filmconfig.v001",
        "slug": SLUG,
        "episode_id": EP,
        "assets": f"episodes/{EP}/05_visuals/asset_manifest.v003.json",
        "narration_index": f"episodes/{EP}/06_audio/narration_index.v001.json",
        "narration": f"{SLUG}/narration.mp3",
        "captions": f"episodes/{EP}/08_edit/captions.final.v001.srt",
        "out": f"remotion/src/data/{SLUG}_film.json",
        "leadSeconds": 0,
        "openingVariant": "overlay",
        "hookSeconds": hook,
        "hookLine": first_hook[:90],
        "captionLeadSeconds": 0.0,
        "figures_by_section": {k: [b for b, _ in v] for k, v in BEATS.items()},
        "_figure_sources": {"_readme": NOTES,
                            **{k: [rows for _, rows in v] for k, v in BEATS.items()}},
        "_declared_values": DECLARED,
    }
    out = ROOT / "episodes" / "_planning" / "EP71_oroville_filmconfig.v001.json"
    out.write_text(json.dumps(cfg, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    n = sum(len(v) for v in BEATS.values())
    print(f"wrote {out.name}: {n} figures, hookSeconds={hook}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
