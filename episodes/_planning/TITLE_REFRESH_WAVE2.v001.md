# TITLE REFRESH — WAVE 2 (v001)

**Status:** STAGING ONLY. Nothing was written to YouTube. No episode file was modified.
**Date:** 2026-08-03
**Scope:** the 25 lowest-viewed **public long-forms** (views 0–13) out of 47 public long-forms.
**Measurement source:** `episodes/_planning/measurements/DISTRIBUTION_STATE.v001.json` (measured 2026-08-01T22:03Z).
**Machine output:** `episodes/_planning/measurements/TITLE_REFRESH_WAVE2.v001.json` — carries only the recommended candidate, and only for the 20 videos where the recommendation is a change.

---

## 0. The measured problem

| fact | value |
|---|---|
| public long-forms | 47 |
| total views across all 47 | 1,335 |
| median views | 11 |
| bottom five | 0, 0, 1, 1, 1 |
| channel CTR (Studio, measured) | **2.31%** against a 6% target |

The bottom 25 videos in this document hold **158 views between them** — 11.8% of the catalogue's
views across 53% of its titles. Every one of them is a title with nothing to lose.

## 1. Rules this wave obeys (not invented here)

Sourced from `docs/PD_WINNING_PATTERN.md`, `episodes/_planning/CTR_PLAYBOOK.v002.md` §2, and
`episodes/_planning/DEEP_RESEARCH_FINDINGS.v001.md` (R-35, R-37, R-38, R-6, R-a).

1. **Long-form grammar is declarative sentence-case, 6–12 words, told as a story beat.**
   Shorts grammar (question form, second person) is a different language and is never ported in.
2. **Measured anti-signals, removed on sight:** colon (0.34×), em-dash / pipe (0.43×), "you" (0.44×),
   ALLCAPS (0.45×), question mark (0.83×). Eleven of the 25 current titles carry at least one.
3. **Stakes-gap packaging (R-35):** the trivial cause and the catastrophic outcome, with numbers on
   both ends where the record supplies exact ones. `$40 of drugs → the whole house`.
4. **Present-tense injustice (R-38):** sell the wrong in progress. Resolved-relief packaging
   ("Exonerated after N years", "Freed after N years") is banned — the measured ceiling is ~6×.
5. **Status / authority reversal goes in the title where the case has one (R-37).**
6. **Packaging ⇔ opening promise (R-6):** the title's scene should be the film's actual first shot.
   Several candidates below were chosen *because* they are the literal cold open.
7. **Truth is the product.** Every candidate below is traceable to the episode's own script or its
   published description. Where a script carried an accuracy lock (Theranos acquittal ≠ exoneration,
   Sarao did not "cause" the crash, the Sourovelis family kept their house, Susette Kelo's house was
   moved not demolished), the candidate is written to respect it. Deviations found and corrected
   during drafting are logged in §4.

## 2. The proven grammar on this channel

The five best-performing titles are all sentence-case, past or present, one concrete actor, one
irreversible act, no punctuation tricks — and four of the five were produced by the wave-1 refresh
(`title_refresh_mapping.v001.json`, applied 2026-07-25):

| views | title |
|---|---|
| 236 | Following the deposit rule is what made her a suspect |
| 175 | He called safety pure waste and dove anyway |
| 159 | Police Can Stop and Frisk You Without Arresting You |
| 68 | He showed the officer the receipt and was arrested anyway |
| 64 | Fifty years later the FBI still cannot name him |

---

## 3. The table

Ordered by views ascending. **REC** = the candidate carried into the JSON. **KEEP** = leave the live
title alone; reasoning in the row. `T` in the last column = this title needs a thumbnail change too.

### 3.1 — Zero and one view

| # | video id / slug | current title | views | candidate A | candidate B | recommendation | T |
|---|---|---|---|---|---|---|---|
| 1 | `LXFjJqE6vKU` · 015-theranos | Behind the $9 billion promise was a machine that failed | **0** | A jury convicted her for investors and acquitted her for patients | One drop of blood was worth nine billion dollars until a reporter checked | **REC A** — the current title has no person and no event; the film's actual spine is the split verdict, and no other Theranos video on the platform leads with it. | **T** |
| 2 | `2pLWw_vhfI8` · 049-strieff | The Stop Was Illegal — the Supreme Court Kept the Evidence Anyway | **0** | The stop was illegal and the evidence stayed in anyway | The stop was illegal and an old warrant saved the evidence | **REC B** — A is only the current title with the em-dash removed; B names the concrete object (an old traffic warrant) that the whole doctrine turns on. | |
| 3 | `g5yFmDt48oU` · 013-king | The Supreme Court Let Police Take Your DNA at Arrest | **1** | A cheek swab at booking solved a rape from six years earlier | The swab was not why they arrested him and it convicted him | **REC A** — concrete irreversible event, drops "you" and the institutional subject; the six-year gap is exact (2009 arrest, 2003 offence). | |
| 4 | `rrftLmSVivk` · 025-kyllo | Can the Police Scan Your Home From the Street? | **1** | An agent read the heat off his walls from a public street | The agent never left the street and it was still a search | **REC A** — kills the question mark and is the film's literal first shot (R-6): a man on a public street at 3 a.m. pointing a device at a house. | **T** |
| 5 | `AxOlQ2NIaBU` · 045-cleveland | She Was Jailed Because She Was Too Poor to Pay a Fine | **1** | A stack of traffic tickets put her in an Alabama jail cell | Montgomery jailed her to sit out a debt she could not pay | **REC A** — textbook stakes gap, mundane cause to catastrophic outcome, and the stack of tickets is a thumbnail-able object where "too poor" is not. | |

### 3.2 — Two and three views

| # | video id / slug | current title | views | candidate A | candidate B | recommendation | T |
|---|---|---|---|---|---|---|---|
| 6 | `An0to4U0hJQ` · 003-mapp | The Police Broke In — So the Court Let Her Go | **2** | Three officers waved a piece of paper and called it a warrant | The paper they waved at her door was not a warrant | **REC A** — the episode is literally titled *The Paper That Was Not a Warrant*; A is its opening scene, is object-anchored, and withholds the payoff the current title spends. | **T** |
| 7 | `89SQoRgAD7U` · 010-kelo | Your Home for a Developer? The Kelo Supreme Court Case | **2** | The homes came down and the development was never built | Pfizer left New London after the homes were already gone | **REC A** — the current title is the worst-packaged in the set (question mark, case-name jargon, no event). A is the film's own sharpest verdict and needs no prior knowledge of Pfizer or New London. | **T** |
| 8 | `4uuY6G0LmHo` · 040-lech | Police Destroyed His Home Chasing a Stranger — Then Paid Him Nothing | **2** | The city offered five thousand dollars for the house it destroyed | A stranger picked their door at random and police destroyed the house | **REC A** — the $5,000 offer against the $250,000 he borrowed to rebuild is the sharpest stakes gap in the catalogue, and the figure appears in the family's own Supreme Court petition. | **T** |
| 9 | `cQFql7tT1fE` · 001-miranda | Read Rights or It's Out \| Miranda v. Arizona | **3** | He won at the Supreme Court and went back to prison anyway | Four sentences rewrote every arrest in America | **REC A** — removes the pipe and the case-name jargon; A is the film's own hook promise and its Act IV payoff, and it is dramatic irony rather than a doctrine label. | |
| 10 | `cSfe3iGnBBM` · 011-mahanoy | Can Your School Punish You for a Post You Made Off Campus? | **3** | A fourteen-year-old's weekend Snapchat reached the Supreme Court and won | A cheerleader posted on a Saturday and her school punished her | **REC B** — A spends the 8-1 outcome in the title; B is the wrong-in-progress form the research says breaks out, and it drops the question mark and both "you"s. | |
| 11 | `X40EbUw5kzQ` · 039-frazier | Police Are Allowed to Lie to You Until You Confess — Even If You're Innocent | **3** | The fingerprint they told him about did not exist | An officer invented a fingerprint and the confession still counted | **REC A** — nine words, one object, one invented fact, zero jargon. The current title is 15 words with an em-dash and three second-person pronouns. Strongest single rewrite in this wave. | **T** |

### 3.3 — Five views

| # | video id / slug | current title | views | candidate A | candidate B | recommendation | T |
|---|---|---|---|---|---|---|---|
| 12 | `ch2hQ5jhDmQ` · 002-gideon | He Had No Lawyer. So He Wrote the Supreme Court in Pencil. | **5** | He asked the judge for a lawyer and the judge said no | With a lawyer at the second trial the jury acquitted him | **REC A** — the current title is already close to house grammar and is the weakest case for change in this block; A wins narrowly because it sells the injustice in progress instead of handing over the pencil, which is the film's best single image and belongs on the thumbnail. B is rejected as resolved-relief packaging (R-38). | |
| 13 | `waA4XJ9bYcE` · 004-ftx | The Hidden Code Door Behind the $8 Billion FTX Fraud | **5** | The app still showed the money after it was already gone | Prosecutors said one line of code let Alameda spend customer money | **REC A** — A is the film's cold open verbatim (3 a.m., taps withdraw, nothing happens), needs no attribution hedge, and beats a topic label. | |
| 14 | `1pox44KsaV8` · 012-arbitration | The Fine Print That Quietly Took Your Right to Sue | **5** | A thirty dollar phone charge ended their right to sue together | Thirty dollars in tax on a free phone reached the Supreme Court | **REC A** — puts an exact number on the trivial end of the stakes gap and states the irreversible consequence; drops "your". | |
| 15 | `YhEJHK279f8` · 028-forfeiture | Their Son Was Charged. The City Came for His Parents' House. | **5** | Forty dollars of drugs and the city came for the whole house | The defendant in the case was the house itself | **REC A** — numbers on both ends of the gap ($40 against a $300,000 house), and "came for" preserves the fact that the family ultimately kept it. B is the film's most startling line but reads as abstract in a feed. | **T** |
| 16 | `YQIhk2dKZHU` · 031-unlock | Police Can Force Your Thumb — But Maybe Not Your Mind | **5** | A federal court let officers press his thumb to the phone | The same locked phone is protected in one state and opened in another | **REC A** — of-record and specific (*United States v. Payne*, 9th Cir. 2024); drops the em-dash and both second-person pronouns. | |

### 3.4 — Eight to thirteen views

| # | video id / slug | current title | views | candidate A | candidate B | recommendation | T |
|---|---|---|---|---|---|---|---|
| 17 | `XWYWAgkExH4` · 007-riley | Police Took His Phone. Then They Opened It. | **8** | An officer took the phone from his pocket and started reading | Nine justices agreed that the phone in his pocket needed a warrant | **REC A** — marginal call: the current title is already in-grammar. A is the script's own Act I line, adds the sensory verb, and keeps the outcome withheld. Low priority relative to the rest of this wave. | |
| 18 | `j8U8c4BB_GQ` · 019-varsityblues | He sold a side door into America's best universities | **8** | Fifty five people were charged and fifty three were convicted | She paid fifteen thousand dollars and served fourteen days | **KEEP** — a wave-1 title already in the proven grammar (person, object, past tense, 9 words). Eight views on a 27-minute film three weeks old is a thumbnail and long-form-CTR problem, not a title problem. B is the stakes-gap challenger if the owner wants an A/B later. | |
| 19 | `gR_nzXIyIlk` · 036-williams | Thirty hours in jail because an algorithm chose his photo | **10** | Detroit police arrested him in his own driveway on a computer's guess | The match was a probability and they arrested him on it anyway | **KEEP** — exact number, concrete object, irreversible act, 10 words. This is the grammar the other 24 rows are being rewritten *toward*. Do not touch it. | |
| 20 | `Pmh6h5SfWw4` · 038-kidsforcash | A Judge Took $2.8 Million to Send Kids to Prison | **10** | The hearing lasted ninety seconds and no one mentioned a lawyer | A prank web page sent a seventeen-year-old away for three months | **KEEP** — already the stakes-gap form with an exact number of record, a trusted-role reversal, and 10 words. It is also the most self-carrying premise in the catalogue. Spend on the thumbnail here, not the title. | |
| 21 | `5Jap-0h43A4` · 018-flashcrash | The Day $1 Trillion Vanished in 36 Minutes | **11** | A London bedroom trader was blamed for a trillion dollar crash | He pleaded guilty to spoofing and served his sentence at home | **REC A** — the current title is an event label with no person; A restores the human and the bedroom-against-a-trillion gap while "was blamed for" honours the script's causation lock (never assert he caused the crash). | |
| 22 | `rYV4rxtQCV0` · 024-rajaratnam | A billionaire heard his own voice on an FBI tape | **11** | The jury convicted him on all fourteen counts | He refused to plead guilty and the jury convicted him on fourteen counts | **KEEP** — wave-1 title, in-grammar, and the tape is the film's central object and its cold open. Eleven views on a 28-minute finance film is the lane problem the research already named, not the title. | |
| 23 | `68oWZRiOnB8` · 026-katz | The FBI taped a microphone to a phone booth roof | **11** | They never opened the door and it was still an illegal search | A microphone outside the booth ended a rule that stood forty years | **KEEP** — wave-1 title, object-anchored, caught mid-happening, 10 words. Nothing here to improve. | |
| 24 | `tpAKfHKuwqY` · 027-rodriguez | The Traffic Stop Was Over. Then the Dog Arrived. | **11** | The ticket was written and then the dog circled the car | The Supreme Court said the stop may not last one minute longer | **REC A** — marginal call: the current title is serviceable. A is more concretely mid-happening and puts the two physical objects (ticket, dog) in the same sentence. Deliberately avoids a minute count because the record says "about seven to eight". | |
| 25 | `GGW1SIAAgkY` · 044-tekoh | Police Skipped His Rights — Then He Learned He Couldn't Even Sue | **13** | A jury acquitted him and he still could not sue the deputy | Nobody read him his rights and his statement went to trial | **REC A** — removes the em-dash; A is the film's genuine impossible-moral-premise (acquitted, and still blocked), which is a second injustice rather than resolved relief, so R-38 does not bar it. The 6-3 vote stays withheld, per the episode's own scope lock. | |

---

## 4. Accuracy corrections made while drafting

Four candidates were written, checked against the script, and rewritten because they were not true.
Logged here because the check is the point.

| episode | draft that failed | why | shipped instead |
|---|---|---|---|
| 010-kelo | "They took her pink house and the land is still empty" | The script says Susette Kelo's house **survived** — it was taken apart and moved to another lot in New London, where it still stands. Only the neighbourhood was demolished. | "The homes came down and the development was never built" |
| 028-forfeiture | "Forty dollars of drugs and the city took the whole house" | The city seized and sealed the house and locked the family out, then withdrew in 2015; the family **kept** the house. "Took" states an outcome that did not happen. | "Forty dollars of drugs and the city came for the whole house" |
| 015-theranos | "…and cleared her for the patients" | The script carries an explicit lock: acquittal is not exoneration. "Cleared" implies exoneration. | "…and acquitted her for patients" |
| 018-flashcrash | "He moved the largest market on earth from a London bedroom" | Direct violation of the episode's causation lock. The film never asserts Sarao caused the crash, only that his conduct contributed to or exacerbated an imbalance. | "A London bedroom trader was blamed for a trillion dollar crash" |

Two further numbers were deliberately left **out** of titles despite being tempting:

- **045-cleveland** — the $1,554 debt and the $200/$40 monthly split are flagged `confidence: medium`
  in the episode's own fact ledger (single source, Fines and Fees Justice Center). Not title-grade.
- **027-rodriguez** — the dog alerted "about seven to eight minutes" after the stop ended. There is no
  exact minute of record, so no minute count appears in the candidate.

## 5. Thumbnails

Seven rows are marked **T**. In each case the new title promises a scene the existing thumbnail was
not built to show, so shipping the title alone would create the packaging⇔opening mismatch the
research flags (R-6, the florence signature). Highest priority first:

| slug | why the thumbnail must move | the scene the title now promises |
|---|---|---|
| 015-theranos | **Measured 0.00% CTR at 481 impressions** — the bright graphics collage is the cautionary exemplar in CTR_PLAYBOOK v002 §0. The title is the second problem here, not the first. | a courtroom split, withheld — not a device, not a founder |
| 039-frazier | title is now an object ("the fingerprint") that the current thumb does not contain | a fingerprint card under harsh institutional light |
| 040-lech | the offer, not the rubble, is the hook now | a demolished house behind a single small figure; one text element, no "$5,000 → $250,000" graphic (banned by §1) |
| 028-forfeiture | "$40" against "the whole house" needs the house, sealed | a sealed front door with the city's notice on it |
| 003-mapp | title is now the paper | a hand holding a sheet of paper at a lit doorway, three silhouettes |
| 010-kelo | title is now the empty ground | cleared lots at dusk, one foundation slab |
| 025-kyllo | title is now the street-side scan | a parked car on a dark street, a house across the road, one lit window |

Additionally, **038-kidsforcash** and **019-varsityblues** keep their titles — for those two, the
thumbnail is where any remaining spend belongs.

I did not view the live thumbnails in this pass. These are construction-level mismatches derived from
the titles themselves plus the per-video CTR table in CTR_PLAYBOOK v002 §0; a visual QC pass at
mobile-feed size (~168px) is still owed before any thumbnail work ships.

## 6. What this wave does not claim

- Wave 1 was applied **2026-07-25**, nine days before this measurement. Several of the low-view videos
  in §3 have carried their current titles for barely a week, and eleven of the 25 were published in
  the last three weeks. Views this low are also an age and impressions problem. **Titles are the free
  lever, not the only one** — the research ranks end screens and playlists above titling for total lift.
- No CTR prediction is attached to any candidate. The instrument (`yt_studio_video_ctr.py`) needs a
  fresh Studio cookie and a 2–4 week window after any change; absolute CTR from it is ±, only deltas
  within the same instrument are trustworthy.
- Five KEEP rows mean five fewer things to measure. That is deliberate.

## 7. Apply procedure (owner, when approved)

```
# copy the staged file into the path the apply script reads
cp episodes/_planning/measurements/TITLE_REFRESH_WAVE2.v001.json \
   episodes/_planning/title_refresh_mapping.v001.json      # NOTE: this overwrites wave 1's mapping

py -3.11 scripts/apply_title_refresh_v001.py               # dry run first, always
py -3.11 scripts/apply_title_refresh_v001.py --apply
```

`apply_title_refresh_v001.py` round-trips the full existing snippet and replaces only the title, so
descriptions, tags and categoryId survive; `status`/`publishAt` are never in the request. It writes
`title_refresh_receipt.v001.json` with before/after per video.

**Before running:** wave 1's receipt lives at `episodes/_planning/title_refresh_receipt.v001.json` and
the apply script overwrites it. Copy both wave-1 files aside first if that provenance matters.
