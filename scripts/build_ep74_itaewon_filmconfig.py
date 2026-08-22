"""Emit episodes/_planning/EP74_itaewon_filmconfig.v001.json.

Every figure below is taken from a line the narration actually speaks. That is the whole
rule for this file: an on-screen card that states something the voice does not state is an
unsupported factual statement on screen (CLAUDE invariant 1), and check_packaging_claims
would be reading it against a script that never said it. The chunk each card sits against
is named in the comment beside it so the next person can check the pairing in one grep of
06_audio/narration_index.v001.json.

EP74 is R3: 159 real deaths, living convicted and acquitted officials, and a design that
forbids DEPICTING the crush. Two consequences show up here and nowhere else:

  * No card dramatises the thirteen minutes. The ACT_3 figures state density, force and
    time as the PLOS One study states them, and stop. There is no "159 DEAD" kinetic in
    emphasis style, because a number set large and struck onto the screen is a poster, and
    the people it counts were real last Saturday of October.
  * Every card about a named person carries the disposition of the case with it. Lee Im-jae
    was convicted at first instance and his appeal is SUSPENDED, not decided. A card that
    names him without that is a card that convicts a living man the record has not finished
    with.

Figure counts are 13-17 per act, from episode_spec.figure_beats_per_act.
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
EP = "PD-2026-074-itaewon"


def lt(primary: str, secondary: str) -> dict:
    return {"kind": "lowerthird", "primary": primary, "secondary": secondary}


def kin(lines: list[str], emphasis: list[str] | None = None, style: str = "plain") -> dict:
    f = {"kind": "kinetic", "lines": lines, "style": style}
    if emphasis:
        f["emphasisWords"] = emphasis
    return f


def q(quote: str, attribution: str) -> dict:
    return {"kind": "quote", "quote": quote, "attribution": attribution}


FIGURES = {
    # ---------------------------------------------------------------- HOOK (21.2s)
    "HOOK": [
        lt("AI-assisted visualization", "symbolic reconstruction, no real likenesses"),
        kin(["6:34 P.M.", "29 OCTOBER 2022."], ["6:34 P.M."], "emphasis"),  # VC-0001
    ],
    # ---------------------------------------------------------------- OP
    "OP": [
        lt("ITAEWON, YONGSAN DISTRICT, SEOUL", "A street about fifty metres long. Five metres wide at the top, three point two at the bottom."),
    ],
    # ---------------------------------------------------------------- ACT_1: the street, and the number of people
    "ACT_1": [
        lt("THE ALLEY", "About 50 metres long. Twenty-five seconds to walk, at a normal pace, without stopping."),
        kin(["5 METRES WIDE AT THE TOP.", "3.2 AT THE BOTTOM."], ["3.2"], "emphasis"),
        lt("3.2 METRES", "Two cars side by side. The end that opens onto the main road."),
        lt("PLOS ONE, 2024", "A peer-reviewed reconstruction puts the average width of the alley at under four metres along its length."),
        lt("THE HAMILTON HOTEL", "An illegally extended terrace on the northern side — 17.2 square metres — along the side that faces the alley."),
        lt("ITAEWON", "Foreign restaurants, bars that stay open, a few minutes from a station on two lines."),
        lt("AL JAZEERA, 1 NOVEMBER 2022", "An estimated hundred thousand people, many in their teens and twenties, dressed in costume."),
        kin(["100,000 PEOPLE.", "ONE DISTRICT.", "ON FOOT.", "IN THE DARK."], ["100,000"], "emphasis"),
        lt("SEOUL TRANSPORTATION CORPORATION", "81,573 people left the train at Itaewon station that day."),
        lt("THE SAME SATURDAY, A YEAR EARLIER", "31,878."),
        kin(["2.6 TIMES AS MANY."], ["2.6"], "emphasis"),
        lt("6 P.M. – 7 P.M.", "10,747 people out of the station."),
        lt("7 P.M. – 8 P.M.", "11,873."),
        lt("8 P.M. – 9 P.M.", "11,666."),
        lt("ONE STOP AWAY", "A state-owned company was counting them as they came, hour by hour."),
        kin(["AT 6:34 P.M.,", "SOMEBODY DECIDED THIS", "WAS FOR THE POLICE."], ["6:34 P.M."], "emphasis"),
    ],
    # ---------------------------------------------------------------- ACT_2: the eleven calls
    "ACT_2": [
        kin(["ELEVEN CALLS."], ["ELEVEN"], "emphasis"),
        lt("6:34 P.M. – 10:11 P.M.", "Police in Itaewon received eleven distress reports about dangerous levels of overcrowding."),
        lt("112", "In South Korea, the number you dial for the police."),
        lt("CALL 1 — 6:34 P.M.", "People were being forced uphill into a place with no room to come back down. Somebody should come and control it."),
        lt("CALL 2 — 8:09 P.M.", "One hour and thirty-five minutes after the first."),
        lt("TWO DIFFERENT PEOPLE", "Two different calls. The same evening. The same street."),
        lt("CALL 11 — 10:11 P.M.", "The last of the eleven."),
        kin(["3 HOURS,", "37 MINUTES,", "BETWEEN THE FIRST", "AND THE LAST."], ["3 HOURS", "37 MINUTES"], "emphasis"),
        lt("THREE HOURS AND THIRTY-SEVEN MINUTES", "Long enough to drive across a country."),
        lt("WHAT A CALL IS", "A report entering an organisation. What the organisation does with it is a separate question."),
        lt("THE 112 SITUATION ROOM", "The room where the reports arrive."),
        lt("NOT A CRIME REPORT", "None of the eleven describes an offence. They describe a street."),
        lt("THE RECORD", "The calls exist as transcripts. That is why they can be counted at all."),
        lt("WHAT IS NOT ESTABLISHED", "This film does not claim that any single call, answered differently, would have changed the outcome."),
    ],
    # ---------------------------------------------------------------- ACT_3: the alley, without depicting it
    "ACT_3": [
        lt("PLOS ONE, 2024", "Four researchers published a study of that night, reconstructing the crowd from the record."),
        lt("AVERAGE DENSITY DURING THE CRUSH", "7.57 people per square metre. Maximum 9.95."),
        lt("ONE SQUARE METRE", "A doormat."),
        lt("FORCE, AVERAGE PEAK", "1,063 newtons per metre."),
        lt("FORCE, MAXIMUM", "1,961 newtons per metre."),
        lt("EIGHTEEN SQUARE METRES", "The study records over three hundred people concentrated in that area. Eighteen square metres is a small bedroom."),
        lt("A PASSAGE BETWEEN TWO BUILDINGS", "Two directions, instead of every direction."),
        lt("10:15 P.M.", "The study's timeline puts the first report of a crushing accident, involving approximately ten people, at this minute."),
        lt("10:18 P.M.", "The police chief ordered all available personnel to the scene."),
        lt("10:28 P.M.", "The first emergency rescue team arrived."),
        kin(["THIRTEEN MINUTES."], ["THIRTEEN"], "plain"),
        lt("THE OFFICIAL FIGURE", "157 in the immediate aftermath. 158 by 14 November. 159 by 3 January."),
        lt("159", "Recorded by the ministry and carried by the reporting."),
        lt("INJURED", "A further 196 people."),
        lt("26 OF THE 159", "Foreign nationals, from fourteen countries."),
        lt("OCTOBER 2025", "46 relatives of 21 of those 26 travelled to Seoul for a week, at the official invitation of the Korean government."),
        lt("CAUSE OF DEATH", "About one in ten may not have died of asphyxiation — crush syndrome, rhabdomyolysis, or organ damage from compression."),
    ],
    # ---------------------------------------------------------------- ACT_4: the state, and what an audit found
    "ACT_4": [
        kin(["137 OFFICERS."], ["137"], "emphasis"),
        lt("137", "The number deployed in the district that night."),
        lt("A REAL DEPLOYMENT", "137 officers is not a token force."),
        lt("AGAINST 100,000 PEOPLE", "Most of them working on crime rather than crowds."),
        kin(["ONE OFFICER", "FOR EVERY 730 PEOPLE."], ["730"], "emphasis"),
        lt("THE AUDIT", "It arrived on 23 October 2025 — three years later."),
        lt("YONGSAN POLICE STATION JURISDICTION", "Rallies and demonstrations: 34 in the whole of 2021."),
        lt("MAY – OCTOBER 2022", "921."),
        kin(["34 IN A YEAR.", "921 IN SIX MONTHS."], ["921"], "emphasis"),
        lt("THE OTHER PART OF THE DISTRICT", "On the last Saturday in October, there were 137."),
        lt("WHAT THIS FILM DOES NOT SAY", "That more officers would have changed the outcome. Nobody has established that."),
        lt("'WOULD HAVE'", "A film that says would have about a hundred and fifty-nine deaths is making something up."),
        lt("THE MINISTER", "The National Assembly impeached the Minister of the Interior and Safety."),
        lt("25 JULY 2023", "All nine judges of the Constitutional Court rejected the impeachment, unanimously. He was reinstated."),
        lt("HOLD THOSE TWO TOGETHER", "The audit, and the reinstatement."),
    ],
    # ---------------------------------------------------------------- ACT_5: the law, and an appeal that stopped
    "ACT_5": [
        lt("LEE IM-JAE, THEN 54", "Former chief of the Yongsan police station. Sentenced at first instance to three years without labour."),
        lt("THE CHARGE", "Professional negligence resulting in death and injury."),
        lt("SONG BYUNG-JU", "Head of the station's 112 situation room. Two years without labour."),
        lt("A SITUATION TEAM LEADER", "One year, suspended."),
        lt("APPEALS PENDING", "None of these convictions is final. Both appeals were later suspended by the court."),
        lt("THE DEFINITION", "A hundred thousand people walking into a district because it is the twenty-ninth of October is not anybody's event."),
        lt("FRAMEWORK ACT ON THE MANAGEMENT OF DISASTERS AND SAFETY", "Article 66-11: safety management measures when holding a local festival."),
        lt("A LOCAL FESTIVAL", "Held by somebody. That is what the article is for."),
        lt("ARTICLE 73-9", "The article added afterwards."),
        lt("APRIL 2026", "A member of the National Assembly proposed adding a penalty."),
        lt("THE PROPOSED PENALTY", "An administrative fine of up to two million won for failing to file a plan, and a power to demand a bad plan be improved."),
        kin(["THE RULE EXISTS.", "THE PENALTY", "WAS STILL A BILL."], ["STILL A BILL"], "emphasis"),
        lt("14 JULY 2025", "The 13th criminal division of the Seoul High Court suspended the appeal of the former station chief and two officers from his 112 room."),
        lt("28 AUGUST 2025", "A different bench did the same with the district office chief's appeal."),
        lt("SUSPENDED, NOT DECIDED", "A criminal appeal about a hundred and fifty-nine deaths was paused by the court, because nobody had yet established what happened."),
        lt("STILL OPEN", "As this film is made, the appeals have not resumed."),
    ],
    # ---------------------------------------------------------------- ENDING
    "ENDING": [
        lt("SEOUL, AFTERWARDS", "The city listed 71 areas where large crowds were expected, and put 909 cameras into them."),
        kin(["909 CAMERAS,", "AND A PLASTIC BARRIER", "AT KNEE HEIGHT."], ["909"], "emphasis"),
    ],
}


def main() -> int:
    spec = json.loads((ROOT / "episodes" / EP / "episode_spec.v001.json").read_text("utf-8"))
    lo, hi = spec["figure_beats_per_act"]
    for act in ("ACT_1", "ACT_2", "ACT_3", "ACT_4", "ACT_5"):
        n = len(FIGURES[act])
        if not lo <= n <= hi:
            print(f"ERROR: {act} has {n} figures, spec declares [{lo},{hi}]")
            return 2

    cfg = {
        "schema_version": "pd_filmconfig.v001",
        "slug": "itaewon",
        "episode_id": EP,
        "assets": f"episodes/{EP}/05_visuals/asset_manifest.v001.json",
        "narration_index": f"episodes/{EP}/06_audio/narration_index.v001.json",
        "narration": "itaewon/narration.mp3",
        "captions": f"episodes/{EP}/08_edit/captions.final.v001.srt",
        "out": "remotion/src/data/itaewon_film.json",
        "leadSeconds": 0,
        "openingVariant": "overlay",
        "hookSeconds": 21.24,
        "hookLine": "Thirty-four minutes past six, on a Saturday evening in Seoul, someone pushed their way out of a crowded alley",
        "captionLeadSeconds": 0.0,
        "figures_by_section": FIGURES,
        "_figure_sources": {
            "_readme": [
                "Every figure states something the narration states. The pairing is checkable: grep the",
                "phrase in 06_audio/narration_index.v001.json and the chunk carrying it comes back.",
                "TWO ARE LOAD-BEARING AND MUST NOT BE CUT.",
                "ACT_4 'WHAT THIS FILM DOES NOT SAY' and \"'WOULD HAVE'\": the film states on screen that",
                "nobody has established that more officers would have changed the outcome. Without them the",
                "137-versus-100,000 cards read as an accusation the record does not support.",
                "ACT_5 'APPEALS PENDING' and 'SUSPENDED, NOT DECIDED': Lee Im-jae, Song Byung-ju and the",
                "district office chief are living men whose appeals are SUSPENDED. Every card naming a",
                "conviction is followed by a card saying it is not final. R3 depends on that pairing.",
            ],
            "counts": {k: len(v) for k, v in FIGURES.items()},
        },
        "_declared_values": {
            "leadSeconds": "0 -- the hook is voiced from frame 0, per the owner standard that the hook comes first.",
            "openingVariant": "'overlay' -- brand band over the hook's settle; the voice does not stop.",
            "hookSeconds": "21.24 -- measured, the end of the last HOOK chunk in narration_index (VC-0004), not estimated.",
            "captionLeadSeconds": "0.0 -- gen_captions_forced already applies its own lead shift; a second one would double it.",
            "captions": "captions.final.v001.srt -- the canonical name 52 other episodes use. gen_captions_forced writes captions.v002.srt; it is copied, not renamed, so the tool's own output stays where the tool expects it.",
            "assets": "asset_manifest.v001.json -- built 2026-08-23 from the REVIEWED pool: stills 92, people 28, factory 249, overlay 4.",
        },
    }
    out = ROOT / "episodes" / "_planning" / "EP74_itaewon_filmconfig.v001.json"
    out.write_text(json.dumps(cfg, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"wrote {out.relative_to(ROOT)}")
    print("figures per section:", {k: len(v) for k, v in FIGURES.items()})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
