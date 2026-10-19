# TOPIC PIPELINE v005 — EP60 · 40-minute band, owner-mandated

**Built 2026-07-31.** Supersedes `TOPIC_PIPELINE.v004.md` for EP60 only; v004's EP57–59 slate is unchanged and already in build.
**Status: PROPOSAL.** Nothing approved, nothing scheduled, no build file touched. `state` stays at `idea` until the owner rules.

**What is different about this file:** every previous pipeline recorded demand and saturation as *inherited* or *not re-measured* — v004 §5.8 says so in writing, and its open gate 6 has been open for four consecutive sessions. This file **measured them** with `scripts/topic_demand_probe.py` (YouTube Data API; the API is not blocked, only WebFetch is). The measurement changed the answer, and it also **overturned this file's own predecessor's top pick**.

---

## 0. THE DECISION IN ONE PARAGRAPH

EP60 is **the Champlain Towers South collapse (Surfside, Florida)** at **40 minutes**, built on the **NIST technical findings released 22 June 2026** — six weeks old at the time of writing and the first time the federal government has said what actually failed. The film is not a whodunit and not an engineering explainer: it is a tragedy in the strict sense, because the audience knows the ending from the first sentence and the people in it do not. NIST's finding gives that structure its spine: **the building began failing in early June 2021 and the failure cascaded for about three weeks before the tower came down**, and the margins against failure were, in NIST's co-lead's own words, **"too narrow from the start"** — from 1981. Ninety-eight people died. The settlement was **$1,021,199,000**. No one has been criminally charged.

---

## 1. THE MEASUREMENT THAT DECIDED IT

`py -3.11 scripts/topic_demand_probe.py --preset ep60` · run 2026-07-31 · raw output committed at `episodes/_planning/measurements/TOPIC_DEMAND_PROBE.json`.

Method: for each topic, take the top 15 relevance-ranked search results, discard anything under 3 minutes (news clips and Shorts are not competitors for a 40-minute slot), and report the view distribution (**demand**), the number and size of results ≥20 minutes (**saturation**), and the number of *distinct channels* clearing 100k views (**R-36 two-channel premise test**). Our own two biggest videos are included as controls, so "carries" has a measured meaning rather than a felt one.

| Topic | Median views | Max | ≥100k on N channels | R-36 | Biggest long-form | Verdict |
|---|---|---|---|---|---|---|
| *control* Titan / OceanGate | 1,656,894 | 5,226,937 | 13 | PASS | 3,280,618 (40m) | our #1 video's premise |
| *control* D.B. Cooper | 710,998 | 26,871,854 | 9 | PASS | 26,871,854 (25m) | our #2 video's premise |
| Boeing 737 MAX | 1,302,473 | 14,885,442 | 12 | PASS | 5,061,369 (45m) | demand yes, **incumbents unbeatable** |
| **Surfside collapse** | **347,078** | **1,523,689** | **7** | **PASS** | **915,760 (22m)** | **demand yes, slot open** |
| PG&E / Camp Fire | 174,496 | 1,881,495 | 6 | PASS | 1,881,495 FRONTLINE (54m) | demand yes, **definitive doc exists** |
| Upper Big Branch | 22,488 | 316,661 | 1 | **FAIL** | 316,661 (49m) | reject |
| Guardianship / Fierle | 8,930 | 145,140 | 1 | **FAIL** | 8,930 (57m) | **reject** |
| Delphi salaried pensions | 523 | 1,365 | 0 | **FAIL** | 194 (96m) | **reject** |

**The decisive column is not demand, it is demand ÷ incumbent.** Boeing and D.B. Cooper have proven demand *and* 3–27M-view definitive films; a new entrant is the tenth-best result forever. Surfside has demand on the same order (7 channels over 100k) and **no definitive long-form at all** — the largest is a 22-minute video at 916k. The 40-minute slot on this story is empty, and a federal report published six weeks ago is the reason it is about to be filled by someone.

### 1.1 Two corrections this measurement forces

- **Guardianship / Rebecca Fierle was recommended earlier in this same session, by me, and it is wrong.** The reasoning was "no competing long-form documentary exists, therefore the lane is open". Absence of competitors is equally evidence of absence of demand, and the measurement says it is the second: median 8,930 views, and the only two long-form films on the subject sit at 8,930 and 8,402. v004 §4 had already flagged it as failing the external-demand co-filter and I proceeded anyway. **Do not build it at any length until someone measures demand, not saturation.**
- **`TOPIC_PIPELINE.v004.md` §4 runner-up 3 calls B12 Delphi salaried retirees "the strongest single candidate on the board" for EP60.** Measured: **median 523 views, nothing above 1,365, zero channels over 100k.** The 96-minute congressional field hearing has 194 views. The demographic logic in v004 (older American men, retirement security) is sound and the demand is absent; both can be true. **Delphi is withdrawn as an EP60 candidate.**

### 1.2 Why the pool could not have produced this pick

`CANDIDATE_POOL_US_20260729.v001.md` defines its own scope as *"US cases where an institution destroyed an identifiable person or family… Mass-harm stories with no protagonist were not collected."* Neither of the channel's two biggest videos — Titan and D.B. Cooper — satisfies that definition. The pool also records that **24 of its 36 candidates are CSE**, the archetype it measures as our worst-converting. **A pool whose scope rule excludes our two best results is a structural problem, not a bad session.** Recommend a sibling pool (`CANDIDATE_POOL_DISASTER`) built on the shape that actually wins: *a catastrophe the audience already knows the ending of, where a named institution was warned in writing and did not act.*

---

## 2. RUNTIME: WHY 40 MINUTES IS SAFE **HERE** AND NOT IN GENERAL

The owner set 40 minutes. The honest supporting evidence is narrower than "long videos win", and the file records it as such.

Long-form watch-minutes per video, measured 2026-06-01 → 07-31 (official Analytics API):

| Band | n | watch-min / video |
|---|---|---|
| 9–12 min | 13 | 98 |
| 13–25 min | 5 | 130 |
| 26–40 min | 5 | 512 |
| **26–40 min excluding the top 2** | **3** | **62** |

**93% of the long band is two videos** (Titan 1,868 min; D.B. Cooper 506 min). Remove them and long-form is *worse* than 11–12 minutes. Length is not the lever; **premise is**. The corollary is strict: 40 minutes is justified for EP60 **because its premise measured in the same class as the two that carried the band**, and a 40-minute build of a topic that fails R-36 would reproduce the Swartz result (29 minutes, 23 views, 4.0% AVP, 26 total watch-minutes).

The retention shape of the two winners is also the design target: Titan held **0.96 at 30 seconds** and then ran essentially flat (0.26 → 0.25 → 0.22 from 25% to 95%). People who commit to this shape finish it. Swartz held 0.48 at 30 seconds and never recovered. **The entire risk of a 40-minute film sits in the first 30 seconds.**

**Runtime math** (`PD_ONE_PASS_PRODUCTION_SPEC.v2` row 15, measured pace ~173 wpm): 40:00 total → narration ≈ 36:00 → **6,150–6,350 words**. Hard band; a script outside it is rejected before QC.

---

## 3. EP60 — CHAMPLAIN TOWERS SOUTH · working title *"The Building Was Already Falling"* · 40 min · R2

### 3.1 Verified spine (primary sources; every line below is quotable as written)

| # | Fact | Source |
|---|---|---|
| F-1 | Collapse **24 June 2021**; **98** dead | [NIST, 22 June 2026](https://www.nist.gov/news-events/news/2026/06/nist-releases-technical-findings-what-caused-2021-partial-collapse) |
| F-2 | **Two connections between garage columns and the pool deck failed in early June 2021**, initiating a cascading failure **that spread over about three weeks** | NIST, ibid. |
| F-3 | Mechanism: **punching shear failure** at two columns in the garage under the pool-deck slab; load transferred to elements not strong enough to carry it | NIST, ibid. |
| F-4 | ✓ **VERBATIM — Judith Mitrani-Reiser (NIST co-lead):** *"When building structures are designed and built to required codes and standards, they have margins against failure… In the case of Champlain Towers South, however, these margins against failure were too narrow from the start."* | NIST, ibid. |
| F-5 | ✓ **VERBATIM — Glenn Bell (NIST co-lead):** *"The low margins against failure were primarily caused by two factors… First, severe and widespread deviations in the building's original structural design from the codes and standards of the day, but also some limitations in those codes and standards. And second, deviations in the building's construction from the design drawings."* | NIST, ibid. |
| F-6 | Design deficiencies included pool-deck and street-level slab areas **providing less than half the required strength**; construction deviations included **misplaced reinforcing steel and fewer bars crossing over columns than the design required** | NIST technical findings, as reported by [ENR](https://www.enr.com/articles/63213-nist-report-details-how-design-construction-flaws-led-to-surfside-condo-collapse) — ○ re-read from the NIST document itself before scripting |
| F-7 | **October 2018**: engineer **Frank Morabito** reported failed waterproofing **"causing major structural damage to the concrete structural slab below these areas"** (pool deck, entrance drive, planters) | [NBC 6](https://www.nbcmiami.com/news/local/2018-engineering-report-found-major-structural-damage-in-now-collapsed-condo/2481646/) · ○ obtain the report PDF from the Town of Surfside release |
| F-8 | **9 April 2021**: board president **Jean Wodnicki** wrote to residents that observable damage **"has gotten significantly worse since the initial inspection"**, was **"accelerating"** and would **"begin to multiply exponentially"**; the letter explained an assessment of **more than $15 million** | [Washington Post](https://www.washingtonpost.com/national/months-before-building-collapse-condo-board-president-warned-damage-to-building-was-accelerating/2021/06/29/e68d28e2-d8f6-11eb-bb9e-70fda8c37057_story.html) · [NPR](https://www.npr.org/sections/live-updates-miami-area-condo-collapse/2021/06/29/1011280545/letter-from-condo-board-warned-buildings-damage-has-gotten-significantly-worse) |
| F-9 | **23 June 2022**: Judge **Michael Hanzman** gave final approval to **$1,021,199,000**; **136** units in the building; ~$96M earmarked for unit owners | [NBC News](https://www.nbcnews.com/news/us-news/1-billion-settlement-florida-condo-collapse-approved-judge-rcna34992) |
| F-10 | ✓ **VERBATIM — Judge Hanzman:** *"It will never be enough to compensate them for the tragic loss they have suffered. This settlement is the best we can do. It's a remarkable result. It is extraordinary."* | ibid. |
| F-11 | A Miami-Dade grand jury reported in **December 2021** with condo-safety recommendations and **avoided conclusions about the cause of this collapse**; **no individual or entity has been criminally charged** | [NPR](https://www.npr.org/2021/12/15/1064647589/surfside-condo-collapse-grand-jury) · ○ re-confirm the charging status as of the build date |

**Everything marked ○ is a research instruction, not a fact** (invariant 1). The film may not ship on any ○ line.

### 3.2 The controlling idea

*A building does not fall in thirteen seconds. It falls for forty years, in writing, in front of everyone.*

Stated nowhere in the narration. Carried entirely by the chronology: **1981 too narrow → 2018 written down → April 2021 written down again, harder → early June 2021 it begins → 24 June it arrives.**

### 3.3 Why this can hold 40 minutes when Fierle could not

The reveal ladder has genuine rungs, and each one is a *document*, not an adjective:

- The audience knows the ending at 0:00 — so the question is never "what happens", it is **"how long has this been happening?"**, which is a question that can be asked five times and answered differently each time.
- **Dramatic irony runs for the full 40 minutes.** After the cold open, every scene of ordinary life in that building — a pool deck, a parking space, an April board meeting about money — is watched by an audience that knows. That is the Titan mechanism (E8, known-outcome dread) and it is why Titan ran flat from 25% to 95%.
- The villain is not a person, and the film must not invent one. **The record is the villain**: a 1981 design, a 2018 report, a 2021 letter, a $15M assessment nobody wanted to pay. R-22's "record-anchored damning detail" is satisfied five times over without characterising a single living person's intent.
- **No criminal charges** is not a missing ending; it is the ending. The last movement earns its silence.

### 3.4 The 40-minute beat map (reveal ladder per DEEP_RESEARCH_FINDINGS §0.4)

| Time | % | Beat | Loop / reveal state |
|---|---|---|---|
| 0:00–0:44 | 0–2% | **Cold open.** VO from frame 0. The three-week fact, cut before resolution. | Opens loop L1 *(how did nobody see it?)*; BUT-contradiction planted by **0:32** |
| 0:44–0:49 | | Brand sting ≤5s, audio-continuous | — |
| 0:49–1:10 | | One escalating post-brand sentence + date/place anchor | — |
| 1:10–8:00 | 3–20% | **ACT I — the building.** 1981. Twelve storeys, 136 units, a pool deck over a garage. Named residents, one unrepeatable detail each (R-22). | L1 alive; plant object **O1 = the pool deck** (macro loop, ≥50% of runtime) |
| 8:00–15:00 | 20–37% | **ACT II — 2018, in writing.** Morabito walks the garage; "major structural damage"; the report goes to the board and to the town. Nothing is forbidden, nothing is ordered. | Mid-tier reveal with **≥60s pronoun-withheld delay** (R-23): the report's own sentence read late |
| 15:00–20:00 | 37–50% | **ACT III — the money.** The gap between a report and a repair: three years, a changing board, $15 million, 136 owners who must each agree to pay. **False-relief beat** (R-20): the assessment passes. | **MID REVEAL at ~20:00 (50%)** — the April 2021 letter: they saw it, wrote it down, and used the word *accelerating* |
| 20:00–26:00 | 50–65% | **ACT IV — the last spring.** Ordinary life over a failing slab. Repairs are scheduled. Everything is, on paper, being handled. | L1 tightens; second loop L2 opens *(when exactly did it start?)* |
| 26:00–34:00 | 65–85% | **ACT V — the three weeks.** NIST's finding, staged as a countdown: the two connections fail in early June; the load moves; the failure walks across the deck for three weeks while people sleep above it. | **PRIMARY REVEAL** begins 26:00 — and resolves into F-4: *too narrow from the start* |
| 34:00–36:45 | 85–92% | **1:22 a.m., 24 June 2021.** Thirteen seconds. Held beat before the number: **98**. | All loops resolved by **36:45 (92%)** |
| 36:45–40:00 | 92–100% | **Ending.** $1,021,199,000. 136 units. Hanzman's sentence (F-10). Grand jury: reforms, no cause finding, **no charges**. Falling action only — **nothing new after 92%** (R-4 ladder rule). | — |

### 3.5 Cold open — drafted to the measured winner formula (T2)

> Somewhere in the garage under the swimming pool, in the first week of June 2021, two connections gave way.
> Nobody heard it. Nobody was told. For the next three weeks, the failure moved slowly across the deck while a hundred and thirty-six apartments went on living above it — school runs, a board meeting about money, a repair contract being signed.
> Everyone in this building had been warned. **Twice, in writing.** — *(loop lands ~0:32)*
> On the twenty-fourth of June, at twenty-two minutes past one in the morning, the north-east corner of Champlain Towers South came down in thirteen seconds.

Voice from frame 0. Person-plus-irreversible-event inside the first sentence. Known destination announced (E8). No emotion command anywhere (R-19). Five hard specifics in four sentences (R-21).

### 3.6 Packaging — locked BEFORE scripting (R-35 / R-38, `CTR_PLAYBOOK.v002`)

- **Title A (recommended):** *The Building Was Falling for Three Weeks. Nobody Knew.* — present-tense injustice, stakes-gap on both ends (three weeks → 13 seconds).
- **Title B (A/B):** *Two Reports Said the Building Was Failing. It Took Three Years to Decide.*
- **Banned:** any resolved-form title (*"…Five Years Later"*, *"…What We Learned"*) — R-38.
- **Thumbnail:** the pool deck at night with one lit window above it; text **3 WEEKS / 13 SECONDS**. Per R-6 the thumbnail's scene must be the literal first shot and its words must be spoken within 20 seconds — both hold with the §3.5 cold open.

### 3.7 Craft gates specific to this build

`DEEP_RESEARCH_FINDINGS` §4 measured our two most recent scripts at 20/26 and 21/26, failing in the same three places every time. This film is unusually exposed to all three, so they are pre-committed here:

- **R-19 emotion-command ban.** A film about 98 deaths is where "sit with that" gets written. **Zero** of that class. The grep is a build gate, not a review note.
- **R-20 register.** A 40-minute single-register dirge is the predictable failure. ≥3 registers per act; the warm beats live in Act I (the building as a home) and in the April board meeting, which is genuinely mundane and must be allowed to be.
- **R-21 specificity.** ≥5 hard specifics/min, no 90-second stretch without a number, date or new proper noun. This story supplies them; the risk is elegiac drift in Act V.
- **Victim dignity (invariant 11 + house standard).** The 98 are named only where the family record is public and the naming is dignified; no bodies, no rescue-footage gore, no recreated final moments of an identified person, no fabricated bodycam or timestamp authenticity (R-39). Generated visuals are symbolic reconstruction and are disclosed.

---

## 4. THE HONEST CASE AGAINST (read before approving)

1. **It leaves the law/rights lane.** EP1–59 are courts, police and agencies. This is a structural-failure film. The defence is measured — the two videos that produced 63% of our long-form watch time are both outside that lane — but it is a genuine format shift and should be a deliberate owner decision, not a side effect.
2. **The EP60 ending-shape cap is satisfied on the weaker leg.** v004 §5.9 requires *a punished villain or a restored victim*. There is **no punished villain — nobody has been charged.** The cap is met by the restored-victim leg ($1.02bn, F-9). If the owner wants the stronger leg, **PG&E / Camp Fire** is the substitute: an 84-count involuntary-manslaughter guilty plea, at the cost of competing with FRONTLINE's 1.88M-view definitive film.
3. **Saturation is real, just not decisive.** Seven long-form results already exist. Our claim to the slot is the 22 June 2026 NIST findings, which post-date almost all of them. **That advantage decays every week.** If this is not commissioned soon it should not be commissioned at all.
4. **n is small everywhere.** The band comparison rests on 23 long-form videos and the winner class on two. Nothing here should become a permanent rule.

---

## 5. OPEN GATES — clear before any research spend

| # | Gate | Blocks |
|---|---|---|
| 1 | **Read the NIST technical-findings document itself** (not the press release, not ENR) and re-verify F-2, F-3, F-6 verbatim with page cites. | Everything |
| 2 | **Obtain the October 2018 Morabito report PDF** from the Town of Surfside release and quote F-7 from the document. | Act II |
| 3 | **Obtain the 9 April 2021 Wodnicki letter** in full; F-8 currently rests on two news transcriptions of the same letter. | Act III / mid reveal |
| 4 | **Re-confirm the criminal-charge status as of the build date** (F-11). A charge filed mid-build rewrites the ending and the cap. | Ending |
| 5 | **Confirm the exact collapse time** (1:22 a.m. is widely reported; take it from NIST or the incident record, not from press). | Cold open |
| 6 | **Victim-naming policy ruling** — which of the 98, if any, are named on screen, and on what source basis. Owner call. | Acts I and V |
| 7 | **Owner ruling on §4.1** — is EP60 allowed to leave the law/rights lane? | The pick itself |

---

## 6. NEXT ACTIONS

1. Owner approves, edits, or substitutes (PG&E is the pre-worked alternative — §4.2).
2. On approval: `state=idea → screening → approved`, then clear gates 1–5 before scripting.
3. Packaging first (§3.6) — title and thumbnail locked before a word of script.
4. `EP60_FACTS_LEDGER.v001` built from §3.1 with every ○ resolved to a primary document.
5. `EP60_FILM_BIBLE.v001` per `PD_ONE_PASS_PRODUCTION_SPEC.v2` row 15, sized to **6,150–6,350 words**.
6. Re-run `topic_demand_probe.py` at build start — if a 40-minute Surfside film from a large channel has appeared in the interim, the slot is gone and this pick dies with it.

---

*Provenance: built 2026-07-31. Demand and saturation measured by `scripts/topic_demand_probe.py` against the YouTube Data API (raw: `measurements/TOPIC_DEMAND_PROBE.json`); runtime bands measured against the YouTube Analytics API (2026-06-01 → 07-31, 23 long-form videos); retention shapes from `scripts/_yt_retention_curves.json`. Primary-source verification by WebFetch/WebSearch on 2026-07-31: NIST press release read directly; the Morabito report and the Wodnicki letter are so far transcribed from news reporting and are gated (§5). Novelty check run over `episodes/` for surfside / champlain / camp fire / boeing: the only hits are in `PD-2026-021-dbcooper` (the hijacked aircraft was a Boeing 727) — no collision. No build file was touched; nothing approved, scheduled or published.*
