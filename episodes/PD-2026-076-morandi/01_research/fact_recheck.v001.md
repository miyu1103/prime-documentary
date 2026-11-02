# PD-2026-076-morandi — Pre-Publish Fact Re-Verification Packet (v001)

- **Episode:** PD-2026-076-morandi — the Morandi bridge, Genoa, 14 August 2018 (30 min)
- **Risk class:** **R3** — 43 real deaths and 13 injured, families living; **32 people convicted at
  first instance five weeks before this film was written, 25 acquitted or time-barred, an appeal
  announced and the written reasons not yet filed.** This is a live criminal proceeding.
- **Produced by:** Claude (Opus 5, Claude Code), 2026-08-21, by live retrieval and by reading two
  primary documents as documents
- **Binds to:** `episodes/_planning/EP76_morandi_script.en.v001.md`,
  `EP76_morandi_FACTS_LEDGER.v001.md`, `episodes/PD-2026-076-morandi/episode_spec.v001.json`
- **Status:** **NOT CLEARED FOR PUBLISH.** Ten items below require a re-check, four of them before
  the film is rendered rather than before it is uploaded. **One of them has a date on it.**

> This packet is the *preparation* for the R3 pre-publish gate, not the gate. A final re-check on the
> day of publish is still required, and §6 is what that day's check has to cover.

---

## 1. What was actually read, and what was not

**Read as documents, this session** — both are scanned image PDFs with zero extractable text, and
both were read by rendering their pages:

| document | extent |
|---|---|
| **MIT Commissione Ispettiva Ministeriale**, relazione on the Polcevera viaduct, Rome, 14 September 2018 | 225 pages; **pages 1–8, 21–31, 47–49, 53–54, 59–60, 74–88 read** |
| **Tribunale di Genova, dispositivo**, RG NR 10468/18 — RG DIB 2037/22, 16 July 2026 | 10 pages, **read in full** |

**NOT read, and the film says so (AB-05):**

| not read | consequence |
|---|---|
| The court-appointed experts' report of December 2020, ~500 pages | **Every row from it is SECONDARY** and barred from carrying a beat (⛔-13, ⛔-14). It is the document every English retelling quotes |
| The 2017 executive retrofitting project | Every statement about it is the Commission quoting or summarising it |
| The trial transcript, or any part of the court file beyond the operative part | The film makes no claim about what any witness said |
| Riccardo Morandi's 1981 report | **AB-04.** The film narrates only that Aspi commissioned it and that maintenance followed |
| Aspi's inspection manual itself | The two quoted thresholds are the Commission quoting the manual (SRC-0003 via SRC-0001) |
| Annexes 1–4 of the MIT report (the 1986–2018 inspection tables, the pier 9–10 stay investigations) | The score sequence is from the Commission's §3.4 summary of them |
| The 2007 concession agreement | Only its date is narrated |

## 2. The four items that must be resolved BEFORE the render

| # | item | why it cannot wait |
|---|---|---|
| **R-1** | **Every named person carries their status in the same breath, in the FILM, not only in the script.** Check the built `film.json` figures array, the caption file and the burned cards — not the markdown. Castellucci: *convicted at first instance*, *the judgment is not final*. Ferrazza: *acquitted*. ⛔-01 | The film is where this fails, not the script |
| **R-2** | **No figure card resolves the cause to one finding.** The form is always: the ministry's commission concluded X in September 2018 and called it *plausible but not definitive*; the court's experts concluded Y in December 2020. ⛔-04 | A card that says "corrosion of the pier 9 stay" as fact contradicts the film's own honesty |
| **R-3** | **No generated glyph anywhere on the delivered plates.** 117 have been read on contact sheets and at full resolution where a tile could not settle it; **the seven regenerated plates must be read the same way before they are staged** | `fabricated_record` is a ship-blocking class, and V085 was accused of exactly this and cleared only by a full-resolution crop |
| **R-4** | **The collapse is never depicted, and no vehicle appears at a broken edge.** V106 is the severed deck seen from a hillside with no debris and no vehicle; confirm nothing in the cut list pairs it with a car | ⛔-06. Discovered after render, this costs a re-render |

## 3. The item with a date on it — **the most likely thing to go wrong**

**The film says the reasons for the judgment have not been written.** That is true on 21 August 2026
and it has an expiry date.

- The Tribunale di Genova gave itself **ninety days from 16 July 2026** to file its reasons
  (MO-132) — i.e. **on or about 14 October 2026**.
- The script's ENDING states: *"We do not yet know the reasoning, we will not know it for weeks, and
  it is a first-instance judgment in a country with three instances."*
- **If this film publishes after the reasons are filed, that sentence is false**, and an appeal may
  by then have been formally lodged rather than merely announced.

**Action, binding:** on the day the publish date is set, re-check whether the *motivazioni* have been
deposited and whether an appeal has been lodged. If either has happened, **ACT_5's last three lines
and the description are rewritten before scheduling.** This is a splice, not a re-render — the lines
sit at the end of ACT_5 and in the ENDING.

## 4. SECONDARY rows that carry weight — re-check before publish

These are narrated and none is from a primary document. Each needs one independent confirmation.

| row | claim | where it lands |
|---|---|---|
| MO-107–MO-113 | The whole of the court experts' report: the pier 9 south stay, the 1993 corrosion figures, the 2017 project's estimates, the 2009 handwritten note | ACT_5. **Attributed on screen as reported, never as the film's own finding** |
| MO-114, MO-116 | Trial opened 7 July 2022; 57 defendants | ACT_5 |
| MO-122 | The sentences sum to 177 years and 25 days | ACT_5 |
| MO-133 | Castellucci's counsel said they would appeal | ACT_5 — **and this is the row §3 turns on** |
| MO-136 | AINOP has recorded more than 20,000 road bridges and the census is unfinished | ENDING |
| MO-138–MO-141 | The new viaduct: designer, opening date, length, cost, and **the 43 lamps that were reduced** | ENDING. ⛔-10 |
| MO-029 | 566 people evacuated | ACT_4 — corroboration only, and the film can drop it without loss |

**Highest priority: MO-141.** The "43 lights, one for each victim" story is repeated everywhere and
the film explicitly contradicts it. If the correction cannot be confirmed in a second source, the
safer move is to cut the sentence rather than to assert either version.

## 5. Living persons — the exposure map

| person | status in the film | check |
|---|---|---|
| **Giovanni Castellucci** | Named once, in ACT_5, with *convicted at first instance*, *twelve years*, *his lawyers said they would appeal* and *the judgment is not final* in the same two sentences | Confirm the built film, the captions, the title, the thumbnail and the description each pass ⛔-01 **read cold, without the film around them** |
| **Roberto Ferrazza** | Named once, in ACT_5, with the acquittal and its formula | Same |
| The other 31 convicted | Described as a number and a range of sentences, never by name | Confirm no figure card introduces a name |
| The other 24 acquitted or time-barred | Described as a number | Confirm |
| **Massimiliano Giacobbi** | **Not named.** Described as "the engineer who signed the retrofitting project in 2017", with the proceedings closed on his death | Confirm no card or description names him |
| **Riccardo Morandi** | Named as the designer. Died 1989; never a defendant. **The film explicitly refuses the claim that he predicted this** | Confirm no line, card or description implies foresight. ⛔-03 |
| The 43 who died, the 13 injured, their families | **No individual appears, is named, aged or characterised** | Confirm no plate resolves a face and no memorial with a face appears |
| Inspectors, the RUP, the verifier, committee members | Described by role, never by name; depicted only as backs and hands | ⛔-07. Confirm the ten carve-out plates resolve no face |

## 6. What the publish-day check must cover

1. **§3 first.** Have the reasons been filed? Has an appeal been lodged? If yes to either, the
   ending is rewritten before anything is scheduled.
2. R-1 through R-4, re-run against the **rendered file**, not the script.
3. The title, the thumbnail text and the description read **cold, in isolation**, against ⛔-01 and
   ⛔-02. A thumbnail reading THEY KNEW would be a `factual_support` failure on its own.
4. That the film still states its own absences aloud: the two findings disagree and are not resolved
   (AB-03), the experts' report was not read (AB-05), Morandi's 1981 report was not read (AB-04).
5. That no figure anywhere — narration, card, caption, title, thumbnail, description — is outside
   the ledger (⛔-11).

## 7. Rows deliberately excluded, so their absence is not read as an oversight

| row | why it is not in the film |
|---|---|
| MO-018-class detail about where people died | The film does not characterise the dead (⛔-05) |
| The names of the other 55 defendants | Naming 57 people in a 30-minute film serves nothing and multiplies R3 exposure to no purpose |
| The weather on 14 August 2018 | Nothing in the retrieved record attributes the collapse to it, and depicting a storm would imply it (⛔-08) |
| Any survivor or bereaved account | Not retrieved, and not sought. The film's argument does not need it and R3 exposure rises sharply with it |
| The 2009 handwritten note, as a beat | SECONDARY, and ⛔-13 bars it from carrying an act's turn. It may be referred to as reported, with its source named on screen |
