#!/usr/bin/env python3
"""Emit episodes/_planning/EP69_hyatt_filmconfig.v001.json.

Modelled on EP66_openfields_filmconfig.v001.json. Every beat carries the ledger rows behind
it and the MEASURED narration chunk it lands on, computed here with the same arithmetic
build_case_film_generic.build_figures() uses, so `lands_on` is a measurement and not a wish.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(r"C:\Users\aab15\Documents\prime-documentary")
EP = "PD-2026-069-hyatt"
SLUG = "hyatt"
ORDER = ["HOOK", "OP", "ACT_1", "ACT_2", "ACT_3", "ACT_4", "ACT_5", "ENDING"]

MOCA = "Duncan v. Missouri Board for Architects, Professional Engineers and Land Surveyors, 744 S.W.2d 524 (Mo. Ct. App. 1988)"
NBS = "NBS Building Science Series 143, Investigation of the Kansas City Hyatt Regency Walkways Collapse, May 1982"
JPCF = "Pfatteicher, \u201c\u2018The Hyatt Horror\u2019\u201d, ASCE Journal of Performance of Constructed Facilities 14(2), May 2000"

def L3(p, s):  return {"kind": "lowerthird", "primary": p, "secondary": s}
def KIN(lines, emph): return {"kind": "kinetic", "lines": lines, "style": "emphasis", "emphasisWords": emph}
def Q(q, a):   return {"kind": "quote", "quote": q, "attribution": a}
def NT(v, label, **kw): return {"kind": "numberticker", "value": v, "label": label, **kw}
def ST(v, label): return {"kind": "stat", "value": v, "label": label}
def CB(items):  return {"kind": "compbars", "items": items}
def CT(evts):   return {"kind": "casetimeline_c", "events": evts}

# (payload, [ledger rows])  -- one tuple per beat, in section order.
BEATS: dict[str, list[tuple[dict, list[str]]]] = {}

BEATS["HOOK"] = [
    (L3("AI-assisted visualization", "symbolic reconstruction, no real likenesses"), []),
    (KIN(["ONE LONG STEEL ROD", "BECOMES TWO."], ["BECOMES TWO"]), ["CH-01", "CH-02", "CH-04"]),
    (KIN(["ON THE DRAWING,", "IT LOOKS LIKE THE SAME THING."], ["THE SAME THING"]), ["CH-10"]),
]

BEATS["OP"] = [
    (KIN(["NOTHING GOT WEAKER.", "IT WAS ASKED TO CARRY TWICE AS MUCH."], ["TWICE AS MUCH"]),
     ["DS-05", "DS-06", "LD-04"]),
]

BEATS["ACT_1"] = [
    (L3("HYATT REGENCY HOTEL, KANSAS CITY",
        "In service approximately one year. The atrium is about 117 ft by 145 ft in plan and 50 ft high."),
     ["EV-01", "EV-02"]),
    (ST(3, "Suspended walkways spanning the atrium \u2014 at the second, third and fourth floor levels"),
     ["EV-03"]),
    (L3("THE STACK",
        "The second floor walkway hung from the fourth floor walkway directly above it. The third was offset, on its own rods from the roof framing."),
     ["DS-01", "DS-02"]),
    (KIN(["THE WHOLE QUESTION", "IS WHAT HOLDS THE ROD."], ["WHAT HOLDS THE ROD"]),
     ["DS-05", "DS-06"]),
    (L3("THE BOX BEAM",
        "Two 8-inch steel channels laid toe to toe and joined by continuous longitudinal fillet welds. Not a solid section."),
     ["DS-03", "DS-04"]),
    (Q("As originally designed the fourth and second floor walkways were to be supported by what is referred to as a 'one rod' design.",
       MOCA + " \u2014 the court's description of the original detail"),
     ["DS-07"]),
    (NT(6, "Hanger rods \u2014 three down each side of the atrium, about thirty feet of threaded steel apiece", group=False),
     ["DS-07", "CH-07"]),
    (Q("The project design criteria specify a design live load of 100 psf (4.8 kPa) for hotel corridors and lobby areas. This is interpreted by NBS to include the walkways",
       NBS),
     ["DS-08"]),
    (NT(20.3, "Design load at EACH connection under the one-rod arrangement \u2014 NBS Conclusion 6(a)",
        decimals=1, suffix=" kips"),
     ["LD-01", "LD-02"]),
    (Q("The AISC Specification for the Design, Fabrication and Erection of Structural Steel for Buildings forms the basis for the steel design provisions of the Kansas City Building Code.",
       NBS),
     ["DS-09"]),
    (CB([{"label": "Ultimate capacity the code expected of the one-rod connection \u2014 1.67 \u00d7 20.3", "value": 33.9},
         {"label": "Mean ultimate capacity the one-rod connection actually had", "value": 20.5}]),
     ["LD-08", "LD-14"]),
    (NT(60, "Of the capacity expected under the AISC Specification \u2014 the ORIGINAL detail, before any change (NBS)",
        suffix="%"),
     ["LD-15"]),
    (KIN(["THE DETAIL WAS ALREADY ILLEGAL", "BEFORE ANYBODY CHANGED IT."], ["ALREADY ILLEGAL"]),
     ["DS-12", "LD-16"]),
    (Q("The hanger rods and the box beam-hanger rod connections shown on the structural drawings did not meet the design specifications of the Kansas City Building Code.",
       "Administrative Hearing Commission, quoted at 744 S.W.2d 524 \u2014 not contested on appeal"),
     ["DS-12", "LD-16"]),
    (Q("Efforts to obtain copies of the structural design calculations were unsuccessful",
       NBS),
     ["ND-03"]),
    (L3("SPECIAL, AND NON-REDUNDANT",
        "The Commission found the box beam\u2013hanger rod connections to be special connections. All connections are the responsibility of the structural engineer."),
     ["DS-11"]),
    (Q("A 'non-redundant' connection which fails will cause collapse of the structure. The box beam-hanger rod connections were 'non-redundant.'",
       MOCA),
     ["DS-10"]),
    # LAST SLOT, DELIBERATELY. Measured: build_figures reserves only 6.5 s at the tail of a
    # section, and this section's window ends with the 22.0 s H2 assembly hold (289.517-311.517),
    # so the final card of ACT_1 lands inside that hold at EVERY beat count in the declared band
    # [14, 18] -- 14 puts it at 292.5, 18 at 294.6. It cannot be moved out, so it is authored FOR
    # the hold: over 22 wordless seconds of the connection assembling itself, this names the four
    # parts the animation is showing and asserts nothing the ledger does not carry.
    (L3("THE CONNECTION, ASSEMBLED",
        "A rod. A hole through the box beam. A washer. A nut. Each beam sat on its own nut and put only its own share into the steel."),
     ["DS-04", "DS-05", "DS-06"]),
]

BEATS["ACT_2"] = [
    (L3("FAST-TRACK",
        "The building went up while the drawings were still being drawn."),
     ["RV-14"]),
    (Q("The steel fabricator on the Hyatt project, Havens Steel Company, had engineers capable of designing simple, complex, or special connections.",
       MOCA),
     ["CH-06"]),
    (Q("Because of certain fabricating problems Havens proposed to Duncan the use of a 'double rod' system to suspend the second and fourth floor walkways.",
       MOCA),
     ["CH-05"]),
    ({"kind": "mechanism", "mechanism": "faultsplit"}, ["CH-02", "CH-04"]),
    (Q("Under this arrangement all of the second floor walkway load was first transferred to the fourth floor box beams, where both that load and the fourth floor walkway load were transmitted through the box beam-hanger rod connections to the ceiling hanger rods.",
       NBS),
     ["CH-03"]),
    (CB([{"label": "Second floor connection \u2014 unchanged by the redraw", "value": 20.3},
         {"label": "Fourth floor connection \u2014 as built", "value": 40.7}]),
     ["LD-01", "LD-03", "LD-17"]),
    (Q("The change in hanger rod arrangement from a continuous rod to interrupted rods essentially doubled the load to be transferred by the fourth floor box beam-hanger rod connections",
       NBS + " \u2014 Conclusion 6"),
     ["LD-04", "LD-05"]),
    (Q("The effect of this change was to double the load on the fourth floor walkway and the box beam-hanger rod connections on that walkway.",
       MOCA),
     ["LD-06"]),
    (KIN(["NO STEEL WAS REMOVED.", "NO STEEL WAS THINNED."], ["NO STEEL"]),
     ["LD-04", "LD-20"]),
    (Q("There was evidence that one of the architects contacted Duncan to verify that the double rod arrangement was structurally sound and was advised by Duncan that it was.",
       MOCA),
     ["CH-08"]),
    (Q("He called to Duncan's attention questions concerning the strength of the rods and the change from one rod to two. Duncan stated to the technician that the change to two rods was 'basically the same as the one rod concept.'",
       MOCA),
     ["CH-10"]),
    (ST(6, "Separate occasions on which the project engineer was asked about the implications of the change \u2014 the licensing board's investigation, reported in ASCE's journal"),
     ["CH-11"]),
    (Q("Certain information concerning loads and other aspects of the box beam-hanger rod connections which appeared on Duncan's preliminary sketches was not included on the final structural drawings sent to the fabricator.",
       MOCA),
     ["CH-12"]),
    (Q("The Commission found that the structural drawings (S405.1 Secs. 10 and 11) did not communicate to the fabricator that it was to design the box beam-hanger rod connection, and did communicate to the fabricator that those connections had been designed by the engineer.",
       MOCA),
     ["RV-06"]),
    (Q("Duncan testified that he intended for the fabricator to design the connections. Havens prepared its shop drawings on the basis that the connections shown on the design drawings had been designed by the structural engineer.",
       MOCA),
     ["RV-07"]),
    (KIN(["THREE STAMPS.", "THE DRAWING DID NOT CHANGE."], ["DID NOT CHANGE"]),
     ["RV-01"]),
    (Q("The Commission found, and appellants do not dispute, that its own internal procedures called for a detailed check of all special connections.",
       MOCA),
     ["RV-09", "RV-10", "RV-11"]),
    (Q("Under the contract, and under the statute, review and approval of the shop drawings is an engineering function.",
       MOCA),
     ["RV-12", "RV-13"]),
]

BEATS["ACT_3"] = [
    (L3("OCTOBER 1979",
        "With the hotel still going up, the atrium roof collapsed. The investigation established that the cause was poor construction workmanship."),
     ["RV-15"]),
    (Q("In their report to the architects, appellants advised 'we then checked the suspended bridges and found them to be satisfactory.'",
       MOCA),
     ["RV-16", "RV-17"]),
    (Q("Appellants did not do a complete check of the design of all steel in the atrium nor a complete check of the suspended bridges.",
       MOCA),
     ["RV-18"]),
    (KIN(["THE SECOND CHANCE", "CAME AFTER THE CHANGE."], ["AFTER THE CHANGE"]),
     ["RV-15", "RV-16", "RV-17", "RV-18"]),
    (Q("With this change in hanger rod arrangement, the ultimate capacity of the walkways was so significantly reduced that, from the day of construction, they had only minimal capacity to resist their own weight and had virtually no capacity to resist additional loads imposed by people.",
       NBS),
     ["LD-20", "ND-03"]),
    (L3("FRIDAY, 17 JULY 1981",
        "Kansas City is hot. The hotel has been in service about a year."),
     ["ID-01", "EV-01"]),
    (Q("Between 1,500 and 2,000 area residents chose to escape the heat at the Hyatt Regency Hotel's tea dance, a weekly event featuring big band music and a dance contest.",
       JPCF),
     ["EV-04"]),
    (CT([{"year": "7:00 PM", "text": "Crowd in atrium area is estimated at 1500 to 2000"},
         {"year": "7:04 PM", "text": "Band returns from break and begins to play for dance contest"},
         {"year": "7:05 PM", "text": "Second and fourth floor walkways collapse"}]),
     ["EV-05", "EV-06", "EV-07"]),
    (KIN(["NO SECOND PATH.", "NO BEND. NO SAG. NO WARNING."], ["NO SECOND PATH"]),
     ["DS-10", "FN-05"]),
    (Q("Thus, failure of any one connection would have led to complete collapse of the walkway system.",
       NBS),
     ["FN-05"]),
    (Q("In the collapse, the second and fourth floor walkways fell to the atrium floor, with the fourth floor walkway coming to rest on top of the lower walkway.",
       NBS),
     ["EV-09"]),
    (Q("Most of those killed or injured were either on the first floor level of the atrium or on the second floor walkway. The third floor walkway was not involved in the collapse.",
       NBS + " \u2014 executive summary"),
     ["EV-10"]),
    (NT(142000, "Pounds \u2014 the weight of the two walkways, the Missouri Court of Appeals' figure",
        suffix=" lb", group=True),
     ["EV-11"]),
    (NT(71, "Tons of steel and concrete, from four storeys up \u2014 our own arithmetic on the NBS dead-load measurement",
        suffix=" tons"),
     ["EV-12"]),
    (CT([{"year": "7:08 PM", "text": "First call for help"},
         {"year": "7:22 PM", "text": "A call goes out for cutting tools"},
         {"year": "7:52 PM", "text": "More than a hundred firefighters in the building"},
         {"year": "3:15 AM", "text": "The first walkway span is lifted"},
         {"year": "4:30 AM", "text": "Last survivor removed from debris"}]),
     ["EV-08"]),
    (L3("NINE HOURS, TWENTY-FIVE MINUTES",
        "7:05 p.m. to 4:30 a.m. The federal report gives it eleven lines."),
     ["EV-08"]),
    (NT(114, "People died. At least 186 were injured \u2014 the Missouri Court of Appeals' figures"),
     ["ID-02"]),
    (L3("NO NAMES",
        "Neither the federal report nor the court names a single victim. This film names none of the dead."),
     ["ND-09", "ID-04"]),
]

BEATS["ACT_4"] = [
    (L3("20 JULY 1981",
        "Three days after. Senator Eagleton's office contacts the National Bureau of Standards; on 22 July the Mayor formally requests it."),
     ["ID-05"]),
    (Q("In the early phases of the investigation, NBS involvement was limited by court order to visual and photographic observations and measurements.",
       NBS),
     ["ID-06"]),
    (L3("NBS BUILDING SCIENCE SERIES 143",
        "National Bureau of Standards, May 1982. Not NIST \u2014 the Bureau did not become the Institute until 1988."),
     ["ID-05"]),
    (Q("Collapse of the walkways occurred under the action of loads that were substantially less than the design loads specified by the Kansas City Building Code.",
       NBS + " \u2014 Conclusion 1"),
     ["FN-08"]),
    (KIN(["LESS.", "NOT MORE."], ["LESS"]), ["FN-08"]),
    (Q("it is concluded that the most probable cause of failure was insufficient load capacity of the box beam-hanger rod connections.",
       NBS),
     ["FN-01"]),
    (Q("Two factors contributed to the collapse: inadequacy of the original design for the box beam-hanger rod connection, which was identical for all three walkways, and a change in hanger rod arrangement during construction that essentially doubled the load on the box beam-hanger rod connections at the fourth floor walkway.",
       NBS),
     ["FN-02"]),
    (CB([{"label": "Design load at the connection AS DRAWN (one rod)", "value": 20.3},
         {"label": "Design load at the fourth floor connection AS BUILT (two rods)", "value": 40.7}]),
     ["LD-01", "LD-03"]),
    (Q("It would be expected that the ultimate load capacity of the resulting connection would be at least 1.67 times 40.7, or 68 kips (302 kN)",
       NBS),
     ["LD-08", "LD-09"]),
    (Q("Mean ultimate capacities of the fourth floor box beam-hanger rod connections were estimated on the basis of the NBS test series and these capacities ranged from 18.2 kips (81 kN) to 19.3 kips (86 kN) with an average value of 18.6 kips (83 kN)",
       NBS + " \u2014 Conclusion 2(c)"),
     ["LD-10"]),
    (CB([{"label": "Ultimate load the code required of the connection", "value": 68.0},
         {"label": "Ultimate capacity the connection actually had", "value": 18.6}]),
     ["LD-09", "LD-10"]),
    (NT(21.4, "Maximum load on a fourth floor connection at the moment of collapse (NBS)",
        decimals=1, suffix=" kips"),
     ["LD-12"]),
    (KIN(["31% IS A LOAD RATIO.", "THE STRENGTH RATIO IS ABOUT 27% \u2014 OURS, NOT THEIRS."],
         ["A LOAD RATIO"]),
     ["LD-11", "LD-12"]),
    (NT(53, "The load on the night, measured against the 40.7 kip design load (NBS)", suffix="%"),
     ["LD-13"]),
    (Q("Neither the quality of workmanship nor the materials used in the walkway system played a significant role in initiating the collapse",
       NBS + " \u2014 Conclusion 9"),
     ["FN-07"]),
    (Q("Dynamic loads induced by walking or dancing on the walkways would not have been significant in comparison to the static loads.",
       NBS + " \u2014 Conclusion 1(c)"),
     ["FN-12"]),
    (ST(63, "Credible upper-bound combined occupancy of the second and fourth floor walkways at the time of collapse, as NBS counted it"),
     ["FN-09", "DS-08"]),
    (KIN(["WITHOUT THE CHANGE IT WAS STILL ILLEGAL.", "WITHOUT THE CHANGE IT WOULD HAVE HELD."],
         ["WOULD HAVE HELD"]),
     ["LD-14", "LD-15", "LD-17", "LD-18"]),
]

BEATS["ACT_5"] = [
    (KIN(["NO ONE WAS EVER CHARGED", "WITH A CRIME."], ["NO ONE"]), ["DC-21"]),
    (NT(78000000, "Paid out by insurers to settle civil suits as at December 1983 \u2014 a figure at a date, not a final total",
        prefix="$", group=True),
     ["DC-22"]),
    (L3("FEBRUARY 1984",
        "The Missouri Board for Architects, Professional Engineers and Land Surveyors files its complaint."),
     ["ID-07"]),
    (ST(27, "Days of hearing before the Missouri Administrative Hearing Commission"),
     ["DC-01"]),
    (Q("Its 'Statement of the case, Findings of Fact, Conclusions of Law and Decision' are 442 pages in length.",
       MOCA),
     ["DC-02"]),
    (L3("15 NOVEMBER 1985",
        "98 pages of findings of fact, 322 of conclusions of law, 180 numbered findings. The appellants challenged five."),
     ["DC-02", "DC-03"]),
    (L3("THE FINDINGS \u2014 THE PROJECT ENGINEER",
        "Gross negligence in the preparation and completion of a structural drawing; misconduct in misrepresenting to the architects the safety of a connection."),
     ["DC-04", "DC-05"]),
    (L3("THE FINDINGS \u2014 THE SENIOR ENGINEER",
        "Vicariously liable for the acts and omissions of the project engineer; grossly negligent in failing to review, or assure review of, the drawing before affixing his seal."),
     ["DC-06", "DC-07", "DC-08"]),
    (Q("By section 327.411.2 the owner of the seal is responsible for the 'whole ... engineering project' when he places his seal on 'any plans' unless he expressly disclaims responsibility and specifies the documents which he disclaims.",
       MOCA),
     ["DC-09", "DC-10", "DC-11"]),
    (Q("The responsibility for the structural integrity and safety of the walkway connections was Duncan's and that responsibility was non-delegable.",
       MOCA),
     ["DC-12"]),
    (Q("while the engineer may properly delegate the work of performing engineering design functions, he cannot delegate the responsibility",
       "the administrative law judge, quoted in " + JPCF),
     ["DC-13"]),
    (Q("The Commission defined the phrase in the licensing context as 'an act or course of conduct which demonstrates a conscious indifference to a professional duty.'",
       MOCA + " \u2014 gross negligence, defined for the first time in a Missouri licensing case"),
     ["DC-14"]),
    (Q("The structural engineer's duty is to determine that the structural plans which he designs or approves will provide structural safety because if they do not a strong probability of harm exists. Indifference to the duty is indifference to the harm.",
       MOCA),
     ["DC-15"]),
    (Q("That breach occurred at the latest when their design was incorporated into the building with their approval and they were subject to discipline whether or not any collapse subsequently occurred.",
       MOCA),
     ["DC-16", "DC-17"]),
    (Q("the original inadequacies of the structural drawings might not have been critical if a meaningful review of the shop drawings had occurred.",
       MOCA + " \u2014 footnote 7"),
     ["DC-18"]),
    (CT([{"year": "22 Jan 1986", "text": "The Board revokes all three certificates"},
         {"year": "Summer 1986", "text": "ASCE conduct committee: expel, with no privilege ever to rejoin"},
         {"year": "26 Jan 1988", "text": "One finding reversed; the revocations stand"}]),
     ["DC-19", "DC-20", "ID-08", "PR-02", "PR-03"]),
    (Q("Engineers shall hold paramount the safety, health and welfare of the public in the performance of their professional duties",
       "ASCE Code of Ethics, Fundamental Canon 1, as rewritten in 1976"),
     ["PR-01"]),
    (L3("WHAT THE PROFESSION DID",
        "The conduct committee recommended expulsion. The board of direction voted to suspend for three years; he then relinquished his membership. The project engineer faced no ethics committee at all."),
     ["PR-03", "PR-04", "PR-05"]),
]

BEATS["ENDING"] = [
    (CB([{"label": "20.3 kips \u2014 as drawn", "value": 20.3},
         {"label": "40.7 kips \u2014 as built", "value": 40.7},
         {"label": "68 kips \u2014 as the code required", "value": 68.0},
         {"label": "18.6 kips \u2014 as the steel could actually give", "value": 18.6}]),
     ["LD-01", "LD-03", "LD-09", "LD-10"]),
    (KIN(["NOTHING GOT WEAKER.", "ONE BEAM WAS ASKED TO CARRY TWO."], ["ASKED TO CARRY TWO"]),
     ["LD-04", "LD-20"]),
    (Q("In their place stands a single span, supported not by delicate, graceful rods, but standing on stout, sturdy columns",
       JPCF + " \u2014 as at 2000"),
     ["PR-08"]),
    (L3("WHERE THE RECORD ENDS",
        "A court of appeals, January 1988. Nothing here is said about what either engineer has done since."),
     ["DC-23"]),
    (NT(114, "People went to a tea dance and did not come home"), ["ID-02"]),
    (L3("THE CONNECTION THAT FAILED",
        "A rod, a washer, a nut, and a hole through a welded steel beam."),
     ["DS-04", "DS-05"]),
    (KIN(["THE RESPONSIBILITY", "WAS NON-DELEGABLE."], ["NON-DELEGABLE"]), ["DC-12"]),
    (L3("AI-assisted visualization", "symbolic reconstruction, no real likenesses"), []),
]


def main() -> None:
    narr = json.loads((ROOT / "episodes" / EP / "06_audio" / "narration_index.v001.json").read_text("utf-8"))
    chunks = narr["chunks"]
    total = float(narr["total_seconds"])
    starts: dict[str, float] = {}
    for c in chunks:
        starts.setdefault(c["section"], float(c["start"]))
    windows = {sec: (starts[sec], starts[ORDER[i + 1]] if i + 1 < len(ORDER) else total)
               for i, sec in enumerate(ORDER)}

    # The designed holds, MEASURED off the delivered index (not read from the registry): any
    # inter-chunk gap longer than a section boundary. A figure card may not sit across one
    # unless it was authored for it.
    holds = []
    for a, b in zip(chunks, chunks[1:]):
        gap = float(b["start"]) - float(a["end"])
        if gap > 1.9:
            holds.append((float(a["end"]), float(b["start"]), a["id"], round(gap, 2)))
    print("measured holds:", [(h[2], h[3]) for h in holds],
          "total %.1fs" % sum(h[1] - h[0] for h in holds))

    hook_chunks = [c for c in chunks if c["section"] == "HOOK"]
    hook_seconds = round(float(hook_chunks[-1]["end"]), 3)
    hook_line = hook_chunks[-1]["text"]

    figures_by_section: dict[str, list[dict]] = {}
    sources: dict[str, list[dict]] = {}
    for sec in ORDER:
        payloads = [b for b, _ in BEATS[sec]]
        rows = [r for _, r in BEATS[sec]]
        figures_by_section[sec] = payloads
        s, e = windows[sec]
        dur = 3.0 if sec in {"HOOK", "OP"} else 6.0
        lo = s + (0.1 if sec in {"HOOK", "OP"} else 3.0)
        hi = e - (0.1 if sec in {"HOOK", "OP"} else 6.5)
        if hi - lo < dur:
            lo, hi = s, e
        span = max(hi - lo, dur)
        entries = []
        for i, (payload, rr) in enumerate(zip(payloads, rows)):
            start = lo + span * (i + 0.5) / len(payloads) - dur / 2
            start = min(max(start, lo), max(lo, hi - dur))
            end = min(start + dur, total - 0.5)
            over = [c for c in chunks if float(c["start"]) < end and float(c["end"]) > start]
            if over:
                lands = (f"{over[0]['id']} {over[0]['start']:.3f}-{over[-1]['end']:.3f} | "
                         + " / ".join(c["text"] for c in over)[:170])
            else:
                lands = f"NO CHUNK OVERLAPS {start:.3f}-{end:.3f} (designed silence)"
            if not rr:
                lands = "SACRIFICIAL SLOT: build_figures overwrites this payload with the AI disclosure."
            entries.append({"i": i, "kind": payload["kind"], "ledger_rows": rr,
                            "card_window": [round(start, 3), round(end, 3)], "lands_on": lands})
        sources[sec] = entries

    cfg = {
        "schema_version": "pd_filmconfig.v001",
        "slug": SLUG,
        "episode_id": EP,
        "assets": f"episodes/{EP}/05_visuals/asset_manifest.v001.json",
        "narration_index": f"episodes/{EP}/06_audio/narration_index.v001.json",
        "narration": f"{SLUG}/narration.mp3",
        "captions": f"episodes/{EP}/08_edit/captions.final.v001.srt",
        "out": f"remotion/src/data/{SLUG}_film.json",
        "leadSeconds": 0,
        "openingVariant": "overlay",
        "hookSeconds": hook_seconds,
        "hookLine": hook_line,
        "captionLeadSeconds": 0.0,
        "figures_by_section": figures_by_section,
        "_figure_sources": {"_readme": README, **sources},
        "_declared_values": DECLARED | {
            "hookSeconds": (f"{hook_seconds} -- MEASURED, the `end` of the last HOOK chunk "
                            f"({hook_chunks[-1]['id']}) in 06_audio/narration_index.v001.json. The script "
                            f"designs the cold open at 0:00.0-0:21.0 and voices it from frame 0."),
            "hookLine": f"Verbatim, the closing line of the HOOK section: \u201c{hook_line}\u201d (ledger CH-10).",
        },
    }
    out = ROOT / "episodes" / "_planning" / "EP69_hyatt_filmconfig.v001.json"
    out.write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n", "utf-8")
    n = sum(len(v) for v in figures_by_section.values())
    print(f"wrote {out} -- {n} beats: " + ", ".join(f"{s}={len(figures_by_section[s])}" for s in ORDER))
    for sec in ORDER:
        for e in sources[sec]:
            cs, ce = e["card_window"]
            for hs, he, hid, g in holds:
                ov = min(ce, he) - max(cs, hs)
                if ov > 0.05:
                    print(f"  !! {sec}[{e['i']}] {e['kind']} {cs:.1f}-{ce:.1f} overlaps the "
                          f"{g}s hold after {hid} by {ov:.1f}s")


README = [
    "Provenance for figures_by_section. One entry per beat, in the same order, so a reader can check any "
    "card against EP69_hyatt_FACTS_LEDGER.v001.md (138 rows, 140 verbatim quotations, verifier green 140/140). "
    "ledger_rows are the row ids behind every factual assertion on that card; card_window is where "
    "build_case_film_generic.build_figures() will place it against the MEASURED master; lands_on is the "
    "narration it sits over, taken from 06_audio/narration_index.v001.json. Nothing here is read by any tool.",
    "PLACEMENT. build_figures() does not read a per-beat time: it spaces a section's payloads EVENLY inside "
    "the section window (dur 6.0s, and 3.0s in HOOK/OP), reserving 3.0s at the head and 6.5s at the tail. "
    "ORDER and COUNT are therefore the only placement controls. Both were chosen against the delivered "
    "narration index, not against the paper design, and card_window/lands_on above were computed with the "
    "same arithmetic build_figures uses. Every beat was checked to overlap narration it actually illustrates.",
    "BEAT COUNTS. episode_spec figure_beats_per_act is [14, 18]. ACT_1..ACT_5 each carry 18, the ceiling, "
    "because this film's argument IS a sequence of measured numbers and every one of them needs to be seen. "
    "HOOK 3, OP 1, ENDING 8 -- those three are not acts and the floor does not apply to them.",
    "SACRIFICIAL SLOTS. build_figures overwrites figures[0] and figures[-1] of the whole sorted list with the "
    "AI-disclosure lowerthird. HOOK[0] and ENDING[-1] are therefore already that card, so no content beat is "
    "destroyed (EP65's v001 lost its closing line this way).",
    "THE DESIGNED SILENCES, and the one card that sits on one. The delivered master carries 30.0 s of "
    "scripted silence, measured off this index as three inter-chunk gaps: 22.0 s after VC-0074 (the H2 "
    "assembly opening ACT_2), 5.5 s after VC-0173 (H5 pull-through 3.0 + black 2.5, before the 7:05 PM "
    "card) and 2.5 s after VC-0209 (the TURN). Every beat above was checked against all three. ONE "
    "overlaps: ACT_1[17], 294.6-300.6, six seconds inside the 22.0 s hold. It cannot be moved -- "
    "build_figures reserves only 6.5 s at a section tail and this hold is 22 s long, so the last ACT_1 "
    "card lands inside it at every count in the declared band (14 -> 292.5, 18 -> 294.6). Rather than "
    "hide it, that slot is authored FOR the hold: it names the four parts the wordless animation is "
    "assembling and asserts nothing outside DS-04/DS-05/DS-06. The other two holds are clear.",
    "THE SIX NUMBERS. 20.3 -> 40.7 -> 68 -> 18.6 -> 21.4 -> 114. Six AE kinetic beats are separately authored "
    "at scripts/ae/jobs_ep69_hyatt.json and are CUTS, not figures. The figure grid deliberately carries the "
    "same numbers as compbars/numberticker so the argument survives if the owner drops any AE beat. NOTE: the "
    "AE _at timecodes (3:07 / 6:37 / 14:55 / 17:13 / 17:49 / 28:15) were derived from FILM BIBLE 12.5, whose "
    "clock is the word-cumulative model at 160.0 wpm and does NOT charge the 30.0s of designed silence. "
    "Against the delivered master every beat after the 22.0s ACT_2 hold moves later. Re-time them from this "
    "narration index before placing them in hyatt_film.json.",
    "THE LOAD RATIO. Every card that states 31 percent says out loud that it is a LOAD ratio (21.4 against 68), "
    "and that the capacity ratio (18.6 against 68, about 27 percent) is OUR arithmetic and is not NBS's. "
    "Quarantine -01 and ledger LD-11/LD-12 make this the single most likely factual error in the episode; the "
    "Missouri Court of Appeals itself makes the slip in its own footnote 12.",
    "QUOTE CARDS ARE VERBATIM, AND CHECKED. 43 of the 102 beats are `quote` cards. Each was string-"
    "matched back into EP69_hyatt_FACTS_LEDGER.v001.md after this file was written: 42 match the ledger "
    "byte for byte. The 43rd, ACT_4[3] (NBS Conclusion 1), deliberately does NOT: the cached OCR of BSS "
    "143 carries the fault `specif ied` and the ledger says out loud that on screen and in narration the "
    "word is `specified`. Do not 'correct' that card back to the scanner's error.",
    "AGENCY AND DATE. Quarantine -21: it is NBS, it is the National Bureau of Standards, and it is May 1982. "
    "ACT_4[2] is the card that fixes it on screen. No card anywhere says NIST.",
    "NO DEPICTION. Quarantines -10, -11, -12 and -13 bar third-party footage, any depiction of a casualty or "
    "of the occupied room at or near 7:05 p.m., and any real likeness. Every beat here is typography, a "
    "diagram, or a number; none asserts an image of the room, and ACT_3[17] states on screen that the film "
    "names none of the dead (ND-09).",
    "ATTRIBUTION. Every `quote` card names the tribunal or the document it comes from, because the film's rule "
    "is that criticism is a finding and never the narrator's opinion. 142,000 lb and 114 are attributed to the "
    "Missouri Court of Appeals (quarantine -06, -03), never to the federal report.",
    "LEDGER ROWS SPOKEN BUT NOT CARDED (the grid has fewer slots than the script has lines): EV-03 partly, "
    "CH-07/CH-09, RV-02/RV-03/RV-04/RV-05, FN-03/FN-04/FN-13/FN-14, LD-02/LD-05/LD-07/LD-16/LD-18/LD-19, "
    "DC-17, PR-06/PR-07, ND-01/ND-02. All are narrated; none is contradicted by any card above.",
    "STILL MISSING FOR THIS EPISODE, and unchanged by this file: episodes/PD-2026-069-hyatt/05_visuals/"
    "asset_manifest.v001.json, the 113 mandatory stills and >=40 factory clips under remotion/public/hyatt/, "
    "the face-plate register, and an Ep69Hyatt composition in remotion/src/Root.tsx. "
    "build_case_film_generic --dry-run stops at the asset manifest, before it ever reaches these figures.",
]

DECLARED = {
    "leadSeconds": "0 -- SPEC v2 row 9, binding from EP66: the hook is VOICED from frame 0, so the body "
                   "sequence and the narration master both start at 0 and no silent lead is inserted. "
                   "EP69's script heads its cold open `## HOOK (voice from frame 0)`.",
    "openingVariant": "'overlay' -- EP69_hyatt_PACKAGING.v001.md section 4 and the script's OP direction: the "
                      "brand band rises at 0:21.4 over H1 and falls at 0:24.9, and picture and voice do not "
                      "stop under it. With a zero lead there is nothing for a full-screen opening to sit in.",
    "captionLeadSeconds": "0.0 -- 08_edit/captions.final.v001.srt is produced by gen_captions_forced.py, which "
                          "has already applied the house CAPTION_LEAD_SECONDS = 0.60 to every cue. A second "
                          "lead here would double-shift them.",
    "designedSilence": "30.0 s, declared in scripts/gen_narration_case.py EPISODES['PD-2026-069-hyatt']"
                       "['designed_silences'] and present in the delivered master: 22.0 s after "
                       "'Nothing behind any of them if one let go.' (the H2 assembly opening ACT_2), 5.5 s "
                       "after 'Five minutes past seven.' (H5 pull-through 3.0 + black 2.5), and 2.5 s at the "
                       "TURN before NBS Conclusion 1. FILM BIBLE line 144 budgets exactly 22.0 + 2.5 + 2.5 + "
                       "3.0. No figure card may be allowed to sit across a hold; see the card_window values.",
}

if __name__ == "__main__":
    main()
