#!/usr/bin/env python3
"""Emit episodes/_planning/EP70_wronghouse_filmconfig.v001.json.

Authored 2026-08-18 from EP70_wronghouse_FILM_BIBLE.v001.md and the facts ledger. Every card is
bound to the ledger rows it draws on. The binding disciplines, from the bible §10 and the ledger's
own quarantine table:

- THE CASE IS LIVE. Conduct is *alleged*, *sworn*, or *a court found* -- every card that touches
  the officers' conduct carries its attribution on the card itself.
- TWO ACCOUNTS of the same five minutes: where they diverge (gunpoint-for-an-hour vs no-agent-
  touched-Martin) the cards attribute both and pick neither (F-10 vs F-15).
- THE CHILD is never depicted, never named beyond G.W. as the record spells it, never aged
  (quarantine on our own arithmetic: H-08 pattern -- arithmetic is labelled ours).
- NO COUNT of wrong-house raids nationally (⛔-14); no Collinsville detail beyond E-01..E-05
  (⛔-15); no appointing presidents (bible §10.4).
- THE MOMENT (ACT_5, 29 Apr 2025): Q-05 then Q-06 as typography on black, attributed to the
  transcript, uncut -- the government's answer at full strength, per bible §5.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-070-wronghouse"
SLUG = "wronghouse"

SC = "Martin v. United States, 605 U.S. ___ (2025) — opinion of the Court"
SCC = "Martin v. United States (2025) — Sotomayor, J., concurring"
OA = "Oral argument transcript, Martin v. United States, 29 April 2025"
DCT = "N.D. Ga., summary-judgment order, No. 1:19-cv-04106"
CA11 = "Eleventh Circuit, No. 23-10062"
CMPL = "Plaintiffs' complaint, N.D. Ga. (allegations)"
DDKT = "District-court docket, N.D. Ga."
CNS = "Courthouse News Service, 25 March 2026"


def L3(p, s):  return {"kind": "lowerthird", "primary": p, "secondary": s}
def KIN(lines, emph): return {"kind": "kinetic", "lines": lines, "style": "emphasis", "emphasisWords": emph}
def Q(q, a):   return {"kind": "quote", "quote": q, "attribution": a}
def NT(v, label, **kw): return {"kind": "numberticker", "value": v, "label": label, **kw}
def ST(v, label): return {"kind": "stat", "value": v, "label": label}
def CT(evts):   return {"kind": "casetimeline_c", "events": evts}


BEATS: dict[str, list[tuple[dict, list[str]]]] = {}

BEATS["HOOK"] = [
    (L3("AI-assisted visualization", "symbolic reconstruction, no real likenesses"), []),
    (KIN(["5:00 A.M.", "SUBURBAN ATLANTA."], ["5:00 A.M."]), ["F-01", "F-08"]),
    (KIN(["THEY HAD A WARRANT.", "FOR A DIFFERENT HOUSE."], ["A DIFFERENT HOUSE"]), ["F-02"]),
]

BEATS["OP"] = [
    (KIN(["EVERYONE AGREES IT HAPPENED.", "NOBODY CAN BE HELD RESPONSIBLE."],
         ["NOBODY"]), ["L-04", "L-11"]),
]

BEATS["ACT_1"] = [
    (L3("18 OCTOBER 2017, BEFORE DAWN",
        "The FBI raided the wrong house in suburban Atlanta — the Supreme Court's own first sentence."),
     ["F-01"]),
    (L3("3741 LANDAU LANE",
        "The target: a suspected gang hideout. The warrants named this address."), ["F-02", "G-03"]),
    (L3("3756 DENVILLE TRACE",
        "The house they entered. A quiet family home, three or four houses away."), ["F-02", "G-06"]),
    (ST(6, "SWAT team members at the door, led by Special Agent Lawrence Guerra"), ["F-03"]),
    (L3("THE BREACH",
        "The team breached the front door and detonated a flash-bang grenade — the Court's account."),
     ["F-03"]),
    (KIN(["TEN TO TWENTY SECONDS", "BETWEEN THE KNOCK AND THE DOOR."], ["TEN TO TWENTY"]),
     ["F-08"]),
    (L3("THE CLOSET",
        "Fearing a home invasion, Mr. Cliatt and Ms. Martin hid in a bedroom closet — the Court's account."),
     ["F-04"]),
    (Q("Mr. Cliatt took her to the closet because that is where he keeps his shotgun – he planned on "
       "defending them against the unknown invaders.", CMPL), ["F-13"]),
    (Q("Luckily, the agents opened the closet doors before Mr. Cliatt reached his firearm.", CMPL),
     ["F-14"]),
    (L3("TWO ACCOUNTS, ONE CLOSET",
        "The family swore an agent held Ms. Martin at gunpoint for about an hour. The court found no "
        "agent touched her. The film reports both."), ["F-15", "F-10"]),
    (L3("THE BOY IN THE OTHER ROOM",
        "G.W. pulled the covers over his head — the complaint's words. He is never shown in this film."),
     ["F-16", "F-17"]),
    (Q("G.W. was so afraid that he thought he was going to die.", CMPL), ["F-18"]),
    (L3("THE MAIL",
        "Only then did an officer stumble across some mail with the home's address on it — the Court's account."),
     ["F-07"]),
    (KIN(["THE ROOM WENT SILENT."], ["SILENT"]), ["F-20"]),
    (ST(5, "Minutes, at most, that the agents were in the home — a court finding"), ["F-09"]),
    (L3("5:07 A.M.",
        "The team executed the warrants at the right house — then Agent Guerra returned, and apologized."),
     ["F-11"]),
]

BEATS["ACT_2"] = [
    (L3("OPERATION RED TAPE",
        "Begun in 2015: an FBI operation concerning violent gang activity in Georgia."), ["G-01", "G-02"]),
    (ST(24, "Warrants in the Operation Order — seven searches, seventeen arrests"), ["G-03"]),
    (L3("THE PERSONAL GPS",
        "Agent Guerra says his personal GPS device, set for 3741 Landau Lane, led him to Denville Trace."),
     ["G-04"]),
    (L3("THE BLACK CAMARO",
        "The reference point the team navigated by. The suspect was not known to drive one, or to know "
        "anyone who did."), ["G-07", "G-08"]),
    (L3("THE STREET SIGN. THE MAILBOX.",
        "The agents noticed neither — the house number was visible on the mailbox at the end of the "
        "driveway. A court's description."), ["G-05"]),
    (L3("THE DIFFERENT CAR",
        "A car not present during Agent Guerra's earlier visit sat in the driveway that morning."), ["G-09"]),
    (L3("THE GPS WAS NEVER EXAMINED",
        "Agent Guerra threw the device away not long after the raid — the record's own words."),
     ["G-10", "G-11"]),
    (ST(7, "Of sixteen FBI personnel that night, the FBI could find geolocation data for nine — and "
           "not for these seven"), ["G-13"]),
    (Q("However, no FBI policy or procedure dictates how to locate or navigate to the target, whether "
       "to use a GPS device or what type of GPS device must be used.", DCT), ["G-12"]),
    (KIN(["NO RULE REQUIRED ANY OF IT.", "SO THERE WAS NO RULE TO BREAK."], ["NO RULE"]),
     ["G-12", "L-04"]),
    (Q("The Court considers Guerra's overall preplanning to constitute significant 'precautionary "
       "measures' to avoid mistake.", DCT), ["G-15"]),
    (L3("“INADVERTENTLY”",
        "The district court's word for the execution of a search warrant on the wrong family's home."),
     ["G-14"]),
]

BEATS["ACT_3"] = [
    (L3("WHAT WAS LEFT",
        "Personal injuries and property damage — few explanations and no compensation. The Court's summary."),
     ["H-01"]),
    (ST(7, "Months of leave Ms. Martin was forced to take from her job — the complaint's account"),
     ["H-03"]),
    (ST(2, "Times G.W. changed schools due to his emotional state — the complaint's account"), ["H-04"]),
    (L3("25 OCTOBER 2018",
        "The first paper: detailed tort claims notices to the FBI, one year after the raid."), ["H-05"]),
    (L3("SEPTEMBER 2019",
        "Suit filed. Martin and G.W. on the 11th; Mr. Cliatt on the 18th; consolidated."), ["H-06"]),
    (L3("THE FTCA — THE FRONT DOOR",
        "1946: the United States agrees it can be sued like a private person. That is the whole promise."),
     ["L-01", "L-02"]),
    (ST(13, "Exceptions that claw the promise back — thirteen ways the sentence ends in “except”"),
     ["L-02"]),
    (L3("23 SEPTEMBER 2022 — THEY WIN TWO COUNTS",
        "Assault and false-imprisonment claims survive. Four negligence counts go. Mediation is ordered."),
     ["L-05", "L-06"]),
    (L3("1 NOVEMBER 2022", "Mediation held. Case did not settle — the docket's five words."), ["L-07"]),
    (L3("KORDASH v. UNITED STATES",
        "Decided a month after their win, in a different case. The government asks the court to reconsider "
        "everything in its light."), ["L-08"]),
    (Q("The Court acknowledges that the United States could have possibly raised its Supremacy Clause "
       "argument earlier.", DCT), ["L-09"]),
    (L3("30 DECEMBER 2022 — EVERYTHING GONE",
        "Counts I and II dismissed under the Supremacy Clause. The clerk is directed to close the case."),
     ["L-10", "L-11"]),
    (L3("AND THE AGENT?",
        "Qualified immunity: the law was not clearly established such that Guerra would have known — the "
        "court's finding."), ["L-12"]),
    (L3("22 APRIL 2024",
        "The Eleventh Circuit affirms. Unpublished. Without oral argument."), ["L-14"]),
    (KIN(["THEY WON.", "THEN A CASE THEY WERE NOT PART OF", "TOOK IT AWAY."], ["TOOK IT AWAY"]),
     ["L-05", "L-08", "L-10"]),
]

BEATS["ACT_4"] = [
    (L3("COLLINSVILLE, ILLINOIS — APRIL 1973",
        "Herbert and Evelyn Giglotto woke to the sound of someone smashing down their door — the "
        "concurrence's account."), ["E-01"]),
    (ST(15, "State and federal officers who ransacked the Giglottos' home and tied them up at gunpoint"),
     ["E-02"]),
    (Q("to the sound of someone smashing down their door and bursting into their bedroom",
       SCC + " — the Giglottos' April 1973, in the concurrence's words"), ["E-01"]),
    (L3("THE SECOND HOUSE, THE SAME NIGHT",
        "The officers moved on to the home of Donald Askew — another innocent couple, another bad tip."),
     ["E-03"]),
    (L3("A BAD TIP, CONFESSED",
        "At the Askews' home the officers confessed they had acted on a bad tip — the concurrence's account."),
     ["E-03"]),
    (KIN(["TWO HOUSES IN ILLINOIS.", "ONE LAW FOR THE WHOLE COUNTRY."], ["ONE LAW"]),
     ["E-01", "E-03", "E-05"]),
    (Q("[T]here [was] no effective legal remedy against the Federal Government for the actual physical "
       "damage, much less the pain, suffering and humiliation to which the Giglottos and Askews have "
       "been subjected.", SCC + ", quoting the Senate record"), ["E-04"]),
    (L3("1974 — CONGRESS BUILDS THE BRIDGE",
        "The law-enforcement proviso: six intentional torts by federal officers may proceed. Written "
        "because of Collinsville."), ["E-05"]),
    (Q("innocent individuals who are subjected to raids of the type conducted in Collinsville, "
       "Illinois, will have a cause of action against the individual Federal agents and the Federal "
       "Government.", SCC + ", quoting the Committee"), ["E-05"]),
    (KIN(["CONGRESS FIXED THIS.", "IN 1974.", "ON PURPOSE."], ["ON PURPOSE"]), ["E-05"]),
    (NT(44, "Years between Collinsville and Denville Trace — our arithmetic, and a law older than "
            "either parent in that house", group=False), ["E-08"]),
    (L3("AND THE MAJORITY'S ANSWER",
        "Legislative history cannot displace statutory text. Said at full strength, and not rebutted here."),
     ["L-21"]),
]

BEATS["ACT_5"] = [
    (L3("27 JANUARY 2025",
        "Certiorari granted, limited to two questions. Neither is whether this family gets a trial."),
     ["L-15"]),
    (L3("29 APRIL 2025 — FIRST STREET, WASHINGTON",
        "For the family: Patrick Jaicomo. For the United States: Frederick Liu, Assistant to the "
        "Solicitor General."), ["L-16"]),
    (Q("Oh, he had it identified. He got the right target. He just had the wrong house.",
       "JUSTICE SOTOMAYOR — " + OA), ["Q-01"]),
    (Q("So I don't understand how the act of going into a wrong house can be discretionary.",
       "JUSTICE SOTOMAYOR — " + OA), ["Q-03"]),
    (Q("Well, we understand the discretion here to be the discretion as to how to identify the target "
       "of a search warrant.", "MR. LIU — " + OA), ["Q-04"]),
    # THE MOMENT — bible §5: music stops, these two cards run uncut, then five seconds of nothing.
    (Q("Yeah, you might look at the address of the house before you knock down the door.",
       "JUSTICE GORSUCH — " + OA), ["Q-05"]),
    (Q("— number at the end of the driveway means exposing the agents to potential lines of fire "
       "from the windows.", "MR. LIU — " + OA), ["Q-06"]),
    (Q("How about making sure you're on the right street?", "JUSTICE GORSUCH — " + OA), ["Q-07"]),
    (L3("12 JUNE 2025 — NINE TO NOTHING",
        "Judgment vacated. Gorsuch, J., for a unanimous Court; Sotomayor, J., concurring."), ["L-17"]),
    (Q("The Supremacy Clause does not afford the United States a defense in FTCA suits.", SC), ["L-18"]),
    (L3("WHAT THE COURT DID NOT DECIDE",
        "Whether the discretionary-function exception bars this suit. That question went back down."),
     ["L-20"]),
    (KIN(["A UNANIMOUS SUPREME COURT.", "AND STILL NO TRIAL."], ["STILL NO TRIAL"]),
     ["L-17", "L-19"]),
    (L3("COURTROOM 339, ATLANTA — 25 MARCH 2026",
        "The Eleventh Circuit hears the case again, on remand. As of this film, it has not ruled."),
     ["N-07"]),
    (CT([
        {"label": "the raid", "value": "18 Oct 2017"},
        {"label": "tort claim notices", "value": "25 Oct 2018"},
        {"label": "suit filed", "value": "Sep 2019"},
        {"label": "they win two counts", "value": "23 Sep 2022"},
        {"label": "everything dismissed", "value": "30 Dec 2022"},
        {"label": "affirmed, unpublished", "value": "22 Apr 2024"},
        {"label": "a unanimous Court", "value": "12 Jun 2025"},
        {"label": "argued again, no ruling", "value": "25 Mar 2026"},
    ]), ["F-01", "H-05", "H-06", "L-05", "L-10", "L-14", "L-17", "N-07"]),
]

BEATS["ENDING"] = [
    (NT(8, "Years, and counting, since the door came in — our arithmetic, from the record's dates",
        group=False), ["H-08"]),
    (L3("THE SEVEN-YEAR-OLD UNDER THE BLANKET",
        "is old enough to drive. Our arithmetic. His age today is not stated in any record this film uses."),
     ["H-08"]),
    (KIN(["THE QUESTION IS ALMOST NEVER", "WHETHER IT HAPPENED."], ["WHETHER IT HAPPENED"]), ["L-04"]),
    (KIN(["IT IS WHETHER THE MISTAKE", "WAS THE KIND SOMEBODY WAS ALLOWED TO MAKE."],
         ["ALLOWED TO MAKE"]), ["L-04", "L-20"]),
    (L3("STILL OPEN",
        "The Eleventh Circuit could rule at any time. When it does, this story changes again."), ["N-07"]),
]

NOTES = [
    "ATTRIBUTION IS ON THE CARD. The case is live: every conduct card names its source (the Court, the "
    "district court, the complaint, the docket) because nothing here is the film's own accusation.",
    "TWO ACCOUNTS: ACT_1's closet card carries F-15 (family, sworn: gunpoint, an hour) and F-10 (court "
    "finding: no agent touched Martin) together and picks neither.",
    "THE CHILD: never depicted; G.W. as the record spells it; age never stated (the ENDING card says so "
    "on screen). Bible §7 substitution table binds the pictures, this file binds the words.",
    "⛔-14: no card states any count, rate or trend of wrong-house raids nationally. "
    "⛔-15: Collinsville cards use E-01..E-05 only, and do not say all fifteen officers were federal.",
    "NO POLITICS: N-07 is used for the panel's existence and date only; appointing presidents are on "
    "the record and deliberately not on any card (bible §10.4).",
    "THE MOMENT: ACT_5 cards 6-7 (Q-05, Q-06) run uncut over silence; the builder must not shorten "
    "Liu's answer to make it sound sillier than it is (bible §5).",
]

DECLARED = {
    "leadSeconds": "0 -- SPEC v2 row 9: the hook is voiced from frame 0 ('## HOOK (voice from frame 0)').",
    "openingVariant": "'overlay' -- brand band rises over the hook's last beat; voice does not stop.",
    "captionLeadSeconds": "0.0 -- captions.final.v001.srt already carries the house 0.60 s lead.",
    "hookSeconds": "measured: the sum of HOOK-section chunk durations in narration_index.v001.json.",
    "designedSilence": "5.0 s after THE MOMENT (bible: 'five seconds of nothing before the bed returns').",
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
    out = ROOT / "episodes" / "_planning" / "EP70_wronghouse_filmconfig.v001.json"
    out.write_text(json.dumps(cfg, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    n = sum(len(v) for v in BEATS.values())
    print(f"wrote {out.name}: {n} figures, hookSeconds={hook}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
