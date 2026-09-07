# EP68 — PACKAGING PACKAGE (v001)

**Episode:** `PD-2026-068-pinto` · slug `pinto`
**Subject:** *Grimshaw v. Ford Motor Co.*, **119 Cal. App. 3d 757** (Ct. App., 4th Dist., Div. 2, 29 May 1981),
and the companion criminal prosecution *State of Indiana v. Ford Motor Co.*, Cause No. 11-431, acquittal
13 March 1980. A 1972 Ford Pinto stalled on a freeway and was rear-ended; a woman died of burns and a
13-year-old survived them. A jury awarded **$125,000,000** in punitive damages, a judge cut it to
**$3,500,000**, and an appellate court affirmed both. The document the whole world quotes for that story
was **excluded from evidence**, was **about rollover across the entire American vehicle market**, and used
a value of life **the federal government had published**.
**Written:** 2026-08-11. **Status:** DRAFT — owner approval required before the script is locked.

> **Order of work for this episode (owner rule):** title, thumbnail and the first twenty seconds are
> designed and approved FIRST. The body is written to serve them. This document is that first
> deliverable. Nothing below may be changed by the script writer without a new revision.

---

## 0. What this is built on, and what was measured while building it

Binding inputs read in full before a word of this was written:
`episodes/_planning/EP68_pinto_FACTS_LEDGER.v001.md` (107 fact rows, 118 machine-verified ✓ VERBATIM
quotations, 20 quarantine entries, 14 open questions), `docs/PD_ONE_PASS_PRODUCTION_SPEC.v2.md`,
`docs/PD_CANON.md`, `.claude/rules/19-ship-gate.md`, `C:/Users/aab15/CLAUDE.md` (the opening design
manual, reproduced as §7 below).

**The ledger's verifier was re-run before this package was written**, not taken on trust:

```bash
cd episodes/PD-2026-068-pinto/01_research/sources && py -3.11 verify_quotes.v001.py
# 118 quotations checked, 0 failed.
# 76 located in machine-extracted sources, 42 located in TRANSCRIBED sources.
```

**And the source gates that were open when the ledger was written have moved.** One is fully closed, one
is closed, two are partly closed. **They are the reason this episode is being made rather than dropped**
— the standing instruction was that if the spine could not be sourced, the episode should be killed:

| Gate | Was | Now |
|---|---|---|
| ○-03 **NHTSA's 1978 Pinto investigation report** — the origin of the corrective death toll | known only as Gary Schwartz described it in a 1991 law review | **RETRIEVED.** `NHTSA Office of Defects Investigation, INVESTIGATION REPORT PHASE I, C7-38, "Alleged Fuel Tank and Filler Neck Damage in Rear-End Collision of Subcompact Passenger Cars, 1971–1976 Ford Pinto / 1975–1976 Mercury Bobcat," May 1978`, 1,160,900 bytes, 18 page images, read on the page. The 38 / 27 / 24 figures are now **the agency's own sentence** |
| ○-09 **44 unread pages of Schwartz** | 12 of 56 pages read | **CLOSED.** All 56 pages read on the page image. Four load-bearing pages re-read independently by this pass against the transcription |
| ○-10 **a second scholar** | the counter-case rested on one author | **PARTIALLY CLOSED.** Lee & Ermann (1999) is genuinely closed-access everywhere; its publisher abstract is held. A fully open **same-first-author companion**, Matthew T. Lee, *Business and Economic History* 27:2 (1998), was retrieved and read on the page |
| ○-06 **a primary court record from Winamac** | two newspapers and one law review | **PARTIALLY CLOSED.** A published California appellate opinion, *Granite Construction Co. v. Superior Court*, 149 Cal. App. 3d 465 (1983), recites the case by its Elkhart filing number — `No. 5324 … filed Sept. 13, 1978` — and states the corporation was acquitted; the *Indiana Law Review* survey for 1981 gives the number at judgment, `No. 11-431 (Pulaski County Cir. Ct.), Mar. 13, 1980`, three times, and states that the case **was not appealed from the trial level**. Both located by exact string search by this pass. **The indictment, docket, verdict form and transcript are still not retrieved.** See §6.5 and film bible §7 |

Measurements that bind this package:

| Measured | Value | Where it came from |
|---|---|---|
| Title band | **59–100 chars**, no question form, no second person, no case citation | spec v2 row 13; `check_packaging_qc.TITLE_MIN_CHARS/TITLE_MAX_CHARS` |
| Narration pace, end to end | **159.5–169.7 wpm** (`docs/PD_CANON.md` rule 25). EP66's delivered master: 4,278 words / 1604.211 s = **160.0** | the narration tool's own printed `measured wpm` is speech-only, excludes inter-chunk silence, and ran **7% fast** on EP66 — it is not used here |
| Thumbnail headline ink, this episode's candidates | **214–245 px** at size 248 (floor 150) | replicated `scripts/build_ep62_65_thumbnails.py` fitter; font resolved to `remotion/public/fonts/Anton.ttf` |
| Archive supply for this story | **14,314 clips across 19 counted registers**, 11,089 after the contract's own screen (623 queries, two rounds). A 20th register — fire — was measured at 1,021 and then **refused** | `EP68_pinto_FOOTAGE_PLAN.v001.md` |
| AE kinetic beats authored | **7**, all between ACT_1 and ACT_4 | `scripts/ae/jobs_ep68_pinto.json` |

**One thing this episode inherits and does not re-litigate.** Every PD long-form before EP66 put 11.5
seconds of silence in front of the first spoken word, straight across the 10→15 s window where the
channel loses 2.13 retention points per second. EP66 closed that hole. **EP68 is built on the closed
version from the start**: `leadSeconds: 0`, `openingVariant: 'overlay'`.

---

## 1. Title candidates

Pattern (row 13): `[dramatic present-tense clause] — [what is withheld] | The Case of [Name]`.
All five are third person, inside 59–100 chars, none begins with a question word, none contains "you",
none contains a case citation or the phrase "Supreme Court Case". Character counts are `len()` of the
exact string including the pipe, measured with `check_packaging_qc`'s own constants.

| # | Title | Chars |
|---|---|---|
| **T1 ★** | Everyone Quotes the Ford Pinto Memo and It Was Not About the Pinto \| The Case of Richard Grimshaw | **97** |
| T2 | The Jury in the Ford Pinto Case Never Saw the Memo Everyone Quotes \| The Case of Richard Grimshaw | **97** |
| T3 | A Ford Report Priced a Human Life and the Price Was the Government's \| The Case of the Pinto Memo | **97** |
| T4 | A Magazine Printed One Page of a Ford Report and America Believes It \| The Case of the Pinto Memo | **97** |
| T5 | Indiana Charged Ford With Homicide Over a Pinto and Lost \| The Case of Winamac, Indiana | **87** |

**Ship T1 as A and T2 as B.** Row 13 requires at least two A/B variants. T1 and T2 test the same
correction from two directions — *the document is misdescribed* against *the jury never saw it* — so the
difference between them is attributable to one variable and not to tone.

One sentence on each, and where each one can go wrong:

- **T1 — RECOMMENDED.** It states the correction as a flat fact and withholds every mechanism: what the
  memo *was* about, who excluded it, what the numbers were, who won. It is also the only candidate whose
  claim is carried by a document this pass read in full — the Grush/Saunby report itself, whose analysis
  is captioned ✓ *"the static rollover requirement proposed for FMVSS 301"* (DOC-06) and whose cost table
  counts ✓ *"11 million cars, 1.5 million light trucks"* (DOC-07). The word "Pinto" appears nowhere in
  that table.
- **T2.** The strongest single fact in the record, and the least known: ✓ *"Ford argues that the
  documentation referred to by Mr. Copp—the 'Grush-Saunby Report'—was excluded from evidence"* (DOC-01).
  It is B rather than A because "the memo everyone quotes" has to do two jobs at once in one clause, and
  T1 does them in two.
- **T3.** Accurate — ✓ *"The NHTSA has calculated a value of $200,000 for each fatality"* (DOC-10) — and
  it is the most emotionally loaded true sentence available. It is not A because "priced a human life"
  reads as an accusation in the first four words and the correction arrives too late to be heard.
- **T4.** True and it names the mechanism the film is really about. Demoted only because "a magazine"
  is a weaker noun than "the Ford Pinto memo" for a viewer scanning a feed.
- **T5 — DO NOT SHIP WITHOUT AN OWNER LINE.** Every clause is true (IN-01, IN-03, IN-09), but it gives
  away the third-act reveal in the title, and it front-loads the half of the story whose primary record
  this pass could not retrieve (§6.5). Kept here because somebody will eventually propose it and this is
  the record of why it was not chosen.

**Accuracy note for whoever writes the metadata.** Four money figures, and they are **not**
interchangeable: the jury's **$2,841,000** compensatory + **$125,000,000** punitive to Grimshaw and
**$659,680** to the Grays (MN-01); the judgment after settlement credits, **$2,516,000** and **$559,680**
(MN-02); the remittitur to **$3,500,000** (MN-03); and the Court of Appeal, which **changed no number**
(MN-05). Never write "$125 million" as what Ford paid (⛔-06). And **$11 and $15.30 are different numbers
from different documents about different requirements** (⛔-17) — the single most inviting error in this
episode.

---

## 2. Thumbnail specification

Buildable by `scripts/build_ep62_65_thumbnails.py` with a `pinto` entry added to its `SPEC` dict —
**no new builder** (invariant 14). What that builder actually does, read from the source and then
replicated here so every number below is measured rather than hoped for:

- Cover-crops the plate to 16:9 → **1280×720**, then lays a **black scrim at alpha 120 over the top 66%**
  (y 0–475), so the picture keeps its own light below that line.
- Searches every contiguous 1–3 line break of the headline × sizes 248→96 step −2 and keeps the split
  whose **tallest glyph ink** is greatest while every line fits 1200 px wide. It warns below 150 px.
- Kicker: fixed **46 px**, drawn as a filled accent tag under the headline. It has **no fitter**, so the
  width was measured by hand below.
- **The font resolves on this machine to `remotion/public/fonts/Anton.ttf`.** Every ink figure below came
  through that same resolution path. **If anyone renames the font files, re-measure** — before 2026-08-11
  the builder fell through to Arial Bold, which is wider and misses the floor at the same line width.

Gate targets: `thumb_subject_luma` wants subject-box (x 0.20–0.80, y 0.12–0.88) mean luma ≥ 60, tallest
bright connected component ≥ **150 px**, dark outline ring ≥ 12 px. `thumbnail_visibility` wants selected
thumb mean luma ≥ 33. `episode_spec.thumbnail_candidates_min` is **3**.

**Plate rules for all three, and they are hard.**

1. **No burned car, no burned person, no fire with a person anywhere near it, no hospital, no injury.**
   The two people in the *Grimshaw* car were a woman who died of burns and a boy of 13 who did not
   (⛔-08, ⛔-09). The three who died in Indiana were a 16-year-old and two 18-year-olds (IN-04). **There
   is no thumbnail of this episode that shows any of that**, and the reason is written into
   `episode_spec.forbidden_subjects` so no tool has to be told twice.
2. **No real vehicle identity.** No Ford badge, no oval, no nameplate, no model script, no grille emblem,
   no licence plate, no dealership signage. The car in these plates is an unbadged early-1970s American
   subcompact hatchback **shape**, never a photograph offered as a real Pinto.
3. **No readable text anywhere in the plate.** No legible document, no memo page a viewer could try to
   read, no letterhead. ⛔-15 bars any generated image presented as the Grush/Saunby report, exhibit 125,
   a crash-test report, an NHTSA letter, the Elkhart indictment or a period front page. Typed paper may
   appear as *texture at an angle*; not one word may resolve.
4. Generated plates commissioned at long edge ≥ 3840. **The lower third must be the brightest part of the
   frame**, because the scrim eats the top 66% and the unscrimmed band at y 475–634 carries
   `subject_luma`. Daylight or bright interior; no night plates.

### Variant 1 — recommended, pairs with T1

- **Image:** eight sheets of typed paper fanned across a grey steel desk under a single bright work lamp,
  photographed from a steep oblique so the type reads as texture and **not one word resolves**; a plain
  metal paper clip at the top edge; the desk surface bright and empty in the lower third. No letterhead,
  no logo, no signature, no numbers legible.
- **Headline:** `WRONG MEMO` — **measured ink 218 px at size 248**, breaking `WRONG / MEMO`.
- **Kicker:** `IT WAS ROLLOVER` — **291 px wide at 46 px** — accent RED `#D22628`.

### Variant 2

- **Image:** the underside of an early-1970s subcompact on a workshop lift, seen from below and slightly
  behind: the rear axle, the differential housing, and the flat face of the tank shell behind it, with a
  plain steel machinist's rule laid across the gap between them. Bright shop light from below-left. No
  badges, no plate, no shop signage, no readable markings on the rule.
- **Headline:** `9 INCHES` — **measured ink 218 px at size 248**, breaking `9 INCHES`.
- **Kicker:** `CRUSH SPACE` — accent GOLD `#E5B53A`.

### Variant 3

- **Image:** a single unbadged early-1970s subcompact hatchback stopped in the middle lane of a wide
  three-lane freeway at midday, small in frame, seen from behind and above; empty lanes either side; dry
  Southern Californian scrub at the shoulder; the asphalt bright and uncluttered across the lower third.
  Nobody in or near the car. No other vehicle in frame.
- **Headline:** `500 OR 27` — **measured ink 220 px at size 248**, breaking `500 OR 27`.
- **Kicker:** `NHTSA, MAY 1978` — **301 px wide at 46 px** — accent GOLD `#E5B53A`.

Measured alternatives, if a variant has to be replaced: `$200,000` **245 px** · `$15.30` **230 px** ·
`$11` **228 px** · `38 CASES` **219 px** · `NOT ADMITTED` **218 px** · `NEVER IN EVIDENCE` **218 px** ·
`11 MILLION CARS` **218 px** · `THE OTHER MEMO` **218 px** · `27` **214 px** · `THE TABLE` **214 px**.
Every one clears the 150 px floor; the choice is editorial, not typographic.

**Archive backing for the plates.** The footage plan measured `fuel tank`, `fuel pump`, `blueprint`,
`technical drawing`, `typewriter`, `documents`, `courthouse`, `courtroom` and every `1970s`/`8mm`/`super
8` period query at **0 usable clips** after two query rounds (FOOTAGE_PLAN §3). **All three thumbnail
plates are therefore generated, not archive stills.** The archive is not asked for the one thing it does
not have.

---

## 3. The first twenty-two seconds, as narration

Written to the shape the channel's own retention data rewards — a date, a place, two people doing one
ordinary thing, ending on something they do not know — and against the tyler failure, which summarised
the outcome inside the first ten seconds and retained 0.447. **Every one of these words is spoken. There
is no silent montage and no silent card.** The narration audio starts at 0:00.

**Pace basis.** `docs/PD_CANON.md` rule 25: measured **159.5–169.7 wpm end to end**, with EP66's delivered
master at **160.0**. The table below is **60 words**, so it occupies **21.2 s at the fast edge (169.7) and
22.6 s at the slow edge (159.5)**; timed at 160.0 it is **22.5 s**. The declared window is
**0:00.0–0:22.5**, and whatever is left over at the fast edge is a hold on the last image, not a gap in
the voice. **Re-time against the real ElevenLabs render before captions are locked** — these are design
targets, not measurements of an audio file that does not exist yet.

**HOOK — 0:00.0–0:22.5** · 60 words · voiced from frame 0 · written before the body, not after it.

| Time | Words spoken | On screen |
|---|---|---|
| **0:00.0–0:02.6** | "September, 1973." | A steel desk under one work lamp, empty. Slow 6% push-in. Nothing on it yet. |
| **0:02.6–0:08.0** | "Two engineers at Ford finish an eight-page report and send it to the federal government." | Two cuts, ~2.7 s each: a hand laying a small stack of typed sheets square on the desk (R081); the same stack, from directly above, a paper clip going on. **No word on any sheet resolves.** |
| **0:08.0–0:12.4** *(THE BEAT)* | "On page six there is a table. It counts deaths, and it prices them." **"table" lands at ≈0:09.6; "prices" at ≈0:11.8.** | Two plates, ~2.2 s each, hard-cut with 0.35 s motion-blurred pushes: the lamp swinging across the page so a ruled grid of figures flares and is gone; then black-level 12% for 4 frames. |
| **0:12.4–0:18.2** | "Four years from now a magazine will reprint that table, and the country will decide it knows what Ford did." | A newsprint web running through a press at speed, then a folded magazine dropping onto a kitchen table. Motion carried left to right through both. No masthead, no headline legible. |
| **0:18.2–0:22.3** | "Almost nobody will notice what the table is about." | Back to the desk, the stack square under the lamp, the room otherwise dark. Slow drift in. |
| **0:22.3–0:22.5** | *(hold — the question is standing, unasked)* | The same stack. |
| **0:22.9–0:26.4** | "Two of the eight pages describe a car rolling over." *(first line after the window — the reversal seed)* | Same desk; the brand overlay rises over the lower band here (§4). |

Exact words at exact seconds, as asked: *"September"* at 0:00.0 · *"engineers"* at ≈0:03.5 ·
*"federal"* at ≈0:07.1 · *"table"* at ≈0:09.6 · *"prices"* at ≈0:11.8 · *"magazine"* at ≈0:14.1 ·
*"Ford"* at ≈0:17.4 · *"notice"* at ≈0:19.8 · *"about"* at ≈0:22.2.

**What is deliberately absent from these twenty-two seconds:** the word Pinto, the word memo, the crash,
Lilly Gray, Richard Grimshaw, the jury, the dollar figures, the recall, Indiana, the acquittal, and any
statement of who was right. A viewer at 0:22 knows that a table of deaths and prices was sent to the
government in 1973, that a magazine will publish it in 1977, and that the country will draw a conclusion
from it. **That viewer does not know what the table is about.** That is the standing question, and the
film spends twenty-nine minutes paying it off.

### Every clause traced to the ledger, before this is recorded

| Clause | Ledger row | Status |
|---|---|---|
| "September, 1973." | DOC-05 ✓ *"part of a petition that Ford filed in September 1973"* | exact |
| "Two engineers at Ford" | DOC-03 ✓ *"E. S. Grush and C. S. Saunby"*, Ford Environmental and Safety Engineering | exact; **neither is named in the hook, and neither is ever named as culpable** (⛔-10) |
| "an eight-page report" | GS — the retrieved copy is 8 pages; PM-06 records that *Mother Jones* called it seven. The film says eight because eight is what was retrieved, and says so in ACT_4 | supported, with the discrepancy carried later |
| "send it to the federal government" | DOC-04 ✓ *"The NHTSA has issued Notice 2 of Docket 70-20 and Notice 1 of Docket 73-20"* | exact |
| "On page six there is a table." | DOC-07 — the cost-benefit table is on p.6 of the retrieved copy | exact |
| "It counts deaths, and it prices them." | DOC-07 ✓ *"Savings - 180 burn deaths…"* / ✓ *"Unit Cost - $200,000 per death…"* | exact, and deliberately does **not** say whose price it is — ⛔-04 is satisfied because the film makes no claim here about Ford's valuation |
| "a magazine will reprint that table" | PM-06 ✓ *"Ford's cost-benefit table is buried in a seven-page company memorandum"*; PM-05 | exact |
| "Two of the eight pages describe a car rolling over." | DOC-06 ✓ *"The analysis discussed below concerns the static rollover requirement proposed for FMVSS 301"* | supported by the retrieved pages; **the count of pages is ours and is stated as ours in ACT_4** |

**Nothing in the hook is an inference about anyone's state of mind** (⛔-02, ⛔-10), **no death toll appears**
(⛔-01), and **the document is never called "the Pinto memo"** (⛔-03) — in the hook it is not called
anything at all, which is the point.

---

## 4. Where the brand opening and the brand endcard go

**`BrandOpening` is placed at 0:22.9**, as a 3.5-second lower-band overlay running **0:22.9–0:26.4**, over
footage and narration that never stop. **`BrandEndcard` is placed at the tail**, 9.0 seconds long,
starting at `narrationSeconds` and running to the end of the composition — i.e. at **≈29:22–29:31** at the
design centre. Both are the canonical components in `remotion/src/components/Bookends.tsx`; **neither is
forked** (invariant 14, spec v2 row 14, which fixes `OPENING_SEC = 3.5` and `ENDCARD_SEC = 9.0`).

**OP — 0:22.9–0:36.0.** The `OP` narration section runs under and past the overlay; the voice does not
stop for the brand mark. This is the whole reason the overlay exists.

Why 22.9 and not earlier: the hook window closes at 22.5, and a brand mark that arrives on top of a
standing question costs less than one that arrives instead of a question. Deleting it is not available —
`op_ed_bookends` is a hard gate measured on the built film by `check_final_acceptance.check_bookends`,
which was rewritten on 2026-08-10 precisely because `leadSeconds: 0` with no variant used to render **no
opening at all** and still pass.

`film.json` for this episode therefore declares, explicitly, both of:

```
"leadSeconds": 0,            // narration starts at frame 0; no silent lead
"openingVariant": "overlay"  // BrandOpening renders as a lower band, not a full-screen card
```

An `openingVariant` that is absent means `'card'`, and `leadSeconds: 0` with `'card'` is the combination
that renders nothing. **Both keys are declared. Neither is inferred.**

---

## 5. Subscribe ask and comment question — and the rule this episode follows

**The ask is NOT spoken.** `scripts/check_script_craft.py` sets the spoken-CTA limit at zero and its own
source comment extends the rule to long-form in terms: *"Long-form inherits it: a narrator who asks for
the subscription spends the payoff on the ask."* EP67 wrote a spoken subscribe line into its packaging
§5 and then did not put it in the script, and that contradiction shipped unresolved. **EP68 resolves it
in the other direction and states the choice out loud** (see §6.1). The ask exists — it is simply not in
the narrator's mouth.

Where the ask actually lives, and what it says:

| Surface | Wording | When |
|---|---|---|
| **Lower-third card**, no voice-over, over the reversal beat at ≈**19:50** | `MORE CASES LIKE THIS — SUBSCRIBE` | 3.0 s, rises and falls with the same overlay motion as the brand band (§7.3), so it reads as house furniture rather than an interruption |
| **`BrandEndcard`**, 9.0 s at the tail | the canonical endcard's own subscribe affordance; no new copy | 29:22–29:31 |
| **Description, line 1** | "There are more cases like this one on the channel, and more coming." | at publish |
| **Pinned comment** | the comment question below, verbatim | at publish |

Both description and pinned-comment claims are true and checkable: the catalogue is warrants, searches,
seizures and records, and the 12:00 JST long-form slot is filled with further episodes in build. Neither
promises a sequel to *this* episode, which the owner has rejected before as a lie. No emotional command,
no "smash", no "if this made you angry" — the audience measures badly on those.

**The reversal beat the card sits on, ≈19:40–20:10** (script guidance, not final prose): the table's own
units are read out one line at a time — one hundred and eighty burn deaths, two hundred thousand dollars
each, eleven dollars a car — and then the last line of the table arrives: *"Sales: eleven million cars.
One and a half million light trucks."* The viewer's own assumption breaks there, not at the verdict.

**Comment question, pinned, never spoken:**

> "The table said eleven dollars a car, times eleven million cars. The court's figure for fixing the
> Pinto was fifteen dollars thirty a car. Name the one word that makes those two numbers different."

Answerable by anyone who has watched to 23:20 — the word is **rollover** — specific to this episode, not
a yes/no, not an emotional prompt. Pin it at publish and put it verbatim in the description's second line.

---

## 6. Where I chose against something binding, and why

1. **The spoken subscribe ask is dropped, against the channel's packaging habit and in favour of
   `check_script_craft`'s zero-CTA rule.** The measurement behind that rule was taken on Shorts, where a
   CTA costs a large fraction of the runtime; the rule's own comment extends it to long-form on a craft
   argument rather than a measurement. I followed the tool rather than the habit because (a) the tool is
   the thing that will be run, (b) the conversion ask survives intact on four other surfaces (§5), and
   (c) a narrator asking for a subscription immediately after the film's central reversal is the worst
   possible placement for it. **This is a deliberate departure from EP67's packaging and it wants an
   owner line.**
2. **The 8-second silent montage hook (spec v2 row 9) is replaced by a 22.5-second voiced cold open
   written FIRST.** Same deviation EP66 and EP67 took, same reason: the current row-9 structure lays 11.5
   seconds of silence across the steepest retention loss in the film. **APR required before the build.**
3. **AE kinetic beats: seven, not the "one or two" the 2026-08-04 approval names.** This record is
   unusual in that the argument *is* arithmetic — five pairs of numbers that folklore has merged, each of
   them a quarantine entry in the ledger. Seven beats over 29.5 minutes is one every ~4.2 minutes, all
   mid-film. Named and bound to their script lines in `scripts/ae/jobs_ep68_pinto.json` and film bible
   §12.5. **This widening also wants an owner line.**
4. **The film names Ford Motor Company, a living corporation, in its title and throughout.** Every
   critical sentence rests on a court's finding or on a retrieved document, never on documentary lore.
   **No individual Ford employee is named as culpable** (⛔-10) — including the two engineers whose report
   the film is largely about. The Elkhart grand jury ✓ *"could have indicted individual Ford executivs,
   but chose to charge only the corpora-"* (IN-06), and the film does not go past a grand jury that
   stopped.
5. **The emotional centre of this story cannot be shown, and the film does not try.** Richard Grimshaw
   was 13 and may be living; Lilly Gray died of burns. No depiction of either, no burned child, no burn
   victim, no archive footage of an injured person, and no dramatisation of the crash (⛔-08, ⛔-09). The
   binding substitution table — what the film shows *instead*, beat by beat — is **film bible §3.5**, and
   it is a contract, not a suggestion. The single strongest thing available is that **the court itself
   stopped**: ✓ *"no purpose would be served by further description of the injuries suffered by
   Grimshaw"* (PP-07). The film adopts the court's restraint as its own rule and says so out loud.

### 6.5 The one gate that is still open, and why it does not stop this episode

**○-06 — the skeleton of the Indiana prosecution is now on the record; its flesh is not.**

What closed: a **published court opinion** reciting the case. *Granite Construction Co. v. Superior
Court*, 149 Cal. App. 3d 465 (Cal. Ct. App. 1983), surveying corporate-homicide prosecutions, writes
✓ *"The 'Pinto' case, where a corporation was acquitted. (State v. Ford Motor Co. (1978) No. 5324, Ind.
Super. Ct., filed Sept. 13, 1978 …)"*. And the **Indiana Law Review** for 1981 gives the number at
judgment — ✓ *"State V. Ford Motor Co., No. 11-431 (Pulaski County Cir. Ct. (Ind.), Mar. 13, 1980)"* —
three times, records that ✓ *"This case was not ap- pealed from the trial level"*, and reports that after
the verdict ✓ *"interviews with the jury after trial indicated that the issue of closing speed was never
resolved by the jury."* Every one of those strings was located by exact search in the retrieved file by
this pass, not taken from a summary. **There are two cause numbers because the venue changed, and
neither may appear on screen without its court** (⛔-26).

What is still open: **the indictment, the docket, any order, the verdict form and the transcript.** The
Elkhart grand-jury indictment ledger is physically located — Indiana Archives Series-19750, a container
spanning 1977–1979 — but the finding aid is series-level and never names the case, and the volume is not
online. Indiana's MyCase refused connection on every attempt, so nothing can be said about its coverage
either way.

**ACT_5 therefore stays at 4 minutes 20, not the ten minutes an Indiana-centred cut would want.** The
skeleton is now sourced to a court and to a state law review; the flesh — the witnesses, the exhibits,
the conduct of the trial — still rests on the press and on secondary accounts, and the act says so. The
weight of the act is carried instead by the counter-case's own limits, which rest on documents this pass
read end to end. **Film bible §7 names the three beats that take a new fact if the rest ever closes.**

---

## 7. OPENING OVERLAY — 動画オープニング設計書ルール準拠

`C:/Users/aab15/CLAUDE.md`（動画オープニング設計書の作成ルール）に従い、すべて数値で書く。
同ルールが禁じる抽象表現はこの節に一つも無い。**フレーム直書きはしない。**F値はすべて
`Math.round(秒 * fps)` の算出結果であり、括弧内は 30fps のときの実数である。

### 7.0 環境・Remotion設定（マニュアル セクション0）

リポジトリから読んだ実値。**記憶ではない。**実装者はここだけ見れば調べ直す必要がない。

| 項目 | 値 | 出所 |
|---|---|---|
| 解像度 | **1920 × 1080** | `remotion/src/brand.ts` `BRAND.video` |
| fps | **30**（オープニング設計書ルールの例示は60だが PD 長尺は 30。**F値は必ず `useVideoConfig()` の fps から算出**） | 同上 |
| composition id | **`Ep68Pinto`**（`remotion/src/Root.tsx` に登録・中身は既存 `CaseFilm` を呼ぶだけ） | `Root.tsx` |
| durationInFrames | `Math.round((narrationSeconds + ENDCARD_SEC) * fps)`（`leadSeconds: 0` のため hook 分の加算は無い） | `CaseFilm.tsx` の算出式。**直書き禁止** |
| 中間画像フォーマット | **png**（`setVideoImageFormat('png')`） | `remotion/remotion.config.ts` |
| コーデック | **h264 / libx264**・**CRF 16** | 同上 |
| pixelFormat | **yuv420p** | 同上 |
| colorSpace（色空間） | **bt709**（`setColorSpace`） | 同上 |
| 音声 | **aac**・ビットレート **320k**（`setAudioBitrate`） | 同上 |
| GPU | **angle**（`setChromiumOpenGlRenderer('angle')`） | 同上 |
| 並列度 concurrency | `os.cpus().length`。ただし WebGL/深度を含む長尺は **`--concurrency=4`** | 同上＋正典 §7 |

必要な依存パッケージ（**導入済み。再インストール不要**）:

```bash
npm i @remotion/motion-blur     # Trail。7.3 の入退場に使う
```

**新規 Composition を作らない。** `Ep68Pinto` は `CaseFilm` を呼び、`BrandOpening` に
`variant='overlay'` を渡すだけである。部品を fork しないこと（invariant 14）。

### 7.1 前提と不変条件

- 対象は既存部品 `remotion/src/components/Bookends.tsx` の `BrandOpening`。**新規作成しない**。
- 追加するのは `variant` プロップのみ。既定 `'card'` は現行の全画面3.5秒であり、
  **EP62–65 は1ビットも変わらない**。EP68 は `'overlay'` を指定する。
- `OPENING_SEC = 3.5` と `ENDCARD_SEC = 9.0` は**変更しない**（row 14 が固定と定める）。
- `BrandEndcard` は末尾 **9.0秒**（`Math.round(9.0 * fps)` = 270F）。位置は
  `from={Math.round(narrationSeconds * fps)}`。

### 7.2 秒数ベースのタイムライン（開始 22.90s ／ 全長 3.50s）

| 区間 | 秒 | F | 起きること |
|---|---|---|---|
| in | 22.90–23.30 | 0–12 | 帯とモノグラムが**下から**入る |
| in | 23.03–23.50 | 4–18 | シリーズ名が**マスク切り上がり**（+4F） |
| in | 23.17–23.70 | 8–24 | タイトルが**マスク切り上がり**（+8F） |
| hold | 23.70–25.50 | 24–78 | 静止。**本編カットと声は裏で継続** |
| out | 25.50–26.40 | 78–105 | 3要素が **-6F ずつ逆スタッガー**で下へ抜ける |

**ナレーションは止めない。**この 3.5 秒の裏で `OP` セクションの台詞が進む
（0:22.9–0:36.0・約36語）。これが本節の存在理由である。

### 7.3 各モーションの数値（**等速は禁止**・opacity 単独も禁止）

| 要素 | 開始F | 終了F | 移動量 | イージング | opacity |
|---|---|---|---|---|---|
| スクリム帯 | 0 | 12 | translateY **+72 → 0 px** | `spring({fps, config:{damping: 20, mass: 0.6}})` | 0 → 0.82（**translateY と併用**） |
| モノグラム | 0 | 12 | translateY **+40 → 0 px** ／ scale **0.94 → 1.0** | `spring({fps, config:{damping: 18, mass: 0.5}})` | 0 → 1（併用） |
| シリーズ名 | 4 | 18 | translateY **+100% → 0 px**（親 `overflow:hidden`） | `Easing.out(Easing.cubic)` | 常時 1（**マスクで見せる**） |
| タイトル | 8 | 24 | translateY **+100% → 0 px**（親 `overflow:hidden`） | `Easing.out(Easing.cubic)` | 常時 1（同上） |
| 退場（3要素） | 78 / 84 / 90 | +15 | translateY **0 → +64 px** | `Easing.in(Easing.cubic)` | 1 → 0（併用） |

- **スタッガー**：入場は +4F ずつ、退場は -6F ずつ。3要素を同時に動かさない。
- **モーションブラー**：入退場の translate に `@remotion/motion-blur` の `Trail`
  （`layers={6} lagInFrames={1.2}`）。hold 区間には掛けない。
- 数値はすべて**定数として1箇所**に置く：`OVERLAY = { inF: 12, holdF: 54, outF: 15, bandH: 360, scale: 0.36 }`。
- §5 の登録カード（≈19:50・3.0秒）は**この同じ OVERLAY 定数と同じモーション**を使う。
  新しい動きを発明しない。

### 7.4 レイヤー構成（下から。最低3層の要件を満たす）

1. **本編カット**（`OffthreadVideo` ／ 静止画）— 止めない。overlay は上に乗るだけ
2. **スクリム帯**（画面下 22%・`rgba(8,10,14,0.82)`・上端 12px はグラデでフェード）
3. **モノグラム**（左・高さ 64px）
4. **文字**（シリーズ名 28px ／ タイトル 46px・`overflow:hidden` の親でマスク）

全画面カードと違い **1層目が生き続ける**。「話が止まらない」の実装上の意味はこれである。

### 7.5 props と型

```ts
type BrandOpeningProps = {
  seriesLabel: string;
  title: string;
  subtitle?: string;
  variant?: 'card' | 'overlay';   // 既定 'card' = 現行。EP62-65 は無変更
};
```

`film.json` 側が受け取る props 名は **`openingVariant`**（`'card' | 'overlay'`）と
**`leadSeconds`**（number）。EP68 は `openingVariant: 'overlay'`・`leadSeconds: 0`。
どちらも任意項目であり、宣言しない既存話の挙動は変わらない。

### 7.6 確認方法

`npm run studio` で `Ep68Pinto` を開き、**22.9s と 26.4s の前後 15F** を1コマ送りで確認する。
見る点は3つ——①本編カットが裏で動き続けているか ②文字が下から**マスクで**現れるか
（フェードだけになっていないか） ③3要素が同時に動いていないか。

**書き出しコマンド**（マニュアル §5 の「props 差し替えで量産できる形」）:

```bash
# 本番（全尺）
bash scripts/_finish_episode.sh pinto Ep68Pinto 68

# オープニングだけ確認する（0:20–0:29 ＝ frames 600-870 @30fps）
cd remotion && npx remotion render Ep68Pinto ../out/ep68_op_check.mp4 \
  --public-dir=public_ep68 --frames=600-870

# variant を差し替えて比較する（card = 現行の全画面 ／ overlay = 本設計）
cd remotion && npx remotion render Ep68Pinto ../out/ep68_op_card.mp4 \
  --public-dir=public_ep68 --frames=600-870 \
  --props='{"openingVariant":"card"}'
```

**props を差し替えるだけで両方が出せること自体が要件である。**`variant` をコードに直書きしない。

## 8. What must happen next, in order

1. **Owner approves T1 (+T2 as B), one thumbnail variant, and the 22.5-second cold open** — this
   package, before the script is locked.
2. **APRs written** for the four deviations in §6: the row-9 hook inversion, the seven AE beats, the
   dropped spoken CTA, and ACT_5 written without a primary Winamac record.
3. **○-06 finished** — the remaining routes are the Indiana Archives' Elkhart County Clerk
   indictment-record ledger (Series-19750, 1977–1979 container, an order or a visit), the Pulaski and
   Elkhart county clerks directly, and MyCase from a different network. If any returns, film bible §7
   names the three beats that take it; if none does, ACT_5 stands as designed.
4. `episodes/PD-2026-068-pinto/episode_spec.v001.json` — **written and validating** (it is).
5. Footage staged from `EP68_pinto_FOOTAGE_PLAN.v001.md` §4, **with a labelled contact sheet looked at
   by a person before any clip enters a cut** — and in this episode that review has a specific job: the
   `crash`, `fire` and `court` registers are contaminated with waves, fireworks and courtship displays,
   and the plan says so with counts.
6. Script written to serve items 1–3, not the other way round.

*This document is the contract for the front of EP68. If a later stage wants to change the title, the
thumbnail or the first twenty-two seconds, it writes v002 and gets it approved again — it does not edit
this file.*
