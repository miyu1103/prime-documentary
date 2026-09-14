# PD-2026-063-correa — Fact + Quotation Re-check v001 (R2/R3)

- Re-check date: 2026-08-04 JST
- Episode: `PD-2026-063-correa` · *Correa v. Hospital San Francisco*, 69 F.3d 1184 (1st Cir. 1995)
- Script under check: `episodes/_planning/EP63_correa_script.en.v002.md` (**v002 — the second pass**)
- Ledger: `episodes/_planning/EP63_correa_FACTS_LEDGER.v001.md` (177 graded rows · 105 VERBATIM)
- Primary source: `episodes/_planning/measurements/EP63_correa_RAW.md` (full opinion, CourtListener cluster 196369). **Nothing else was consulted.**
- Contract: `episodes/PD-2026-063-correa/episode_spec.v001.json` (`forbidden_claims` · `forbidden_subjects`)
- Status: **PASS with 3 NEEDS SOURCE** — no quarantined claim, no fabricated fact, no altered quotation.

> **This packet does not start from zero.** The second pass already fixed three factual defects and
> its mechanical audit already corrected ten quotation divergences. §2 and §3 record each of those as
> **RESOLVED**, with the wording that is in v002 *now*. §4 then re-extracts **every** remaining
> quotation mechanically and re-confirms it against the raw opinion.

---

## 1. GATE STATUS

| Item | Status |
| --- | --- |
| Source read end-to-end for this check | ✓ full opinion, caption through statutory appendix |
| Quotations extracted **mechanically** from v002 (never hand-picked) | ✓ longest-common-run walk against the raw opinion, floor 6 tokens, second pass at floor 4 |
| Every extracted quotation re-matched against the raw opinion | ✓ **189 / 189** |
| Quotation divergences found by this pass | **0** |
| Defects carried in from v001 and confirmed fixed | ✓ 3 factual (§2) + 10 quotation (§3) |
| Quarantined statements (§11 of the ledger, Q-01…Q-14) present in v002 | ✓ **0** (§7) |
| Causation lock | ✓ **held** — see §6 |
| Improper-transfer finding | ✓ stated **once**, marked never reviewed under footnote 7 — see §6.3 |
| Second-source corroboration | ✗ none — single-source packet, as the ledger is |
| **Packet usable for the pre-publish gate** | ✓ **yes**, subject to §7 (3 rows must be resolved before render) |

---

## 2. THE THREE FACTUAL DEFECTS THE SECOND PASS FIXED — all RESOLVED

These are the defects `EP63_correa_FILM_BIBLE.v001.md` §19 identified in v001 (R8 evidence 1, R8 evidence 2, R14).
Each is shown with **the wording that is in v002 now**.

### 2.1 A completed act asserted where the opinion has only a suggestion · **RESOLVED**

| | |
| --- | --- |
| **v001 said** | `The hospital's own witness described a call from it, sending its patient elsewhere.` |
| **v002 says (L292)** | `The hospital's own witness described a call she said came from the hospital, about a patient who would be coming to her instead.` |
| **Ledger row** | **CR-17** (✓) and **CR-18** (✓ VERBATIM) |
| **The opinion's own wording** | *"According to Dr. Rojas, a nurse called from HSF to advise her that the patient would be coming to Hospmed for treatment."* · *"Dr. Rojas said that this conversation probably occurred earlier that day (perhaps around 1:00 p.m.), a datum **suggesting** that HSF **tried to** shunt Ms. Gonzalez to Hospmed as soon as it scrutinized her insurance card."* |
| **Why it was a defect** | `sending its patient elsewhere` states a completed act. The opinion has *suggesting* / *tried to* and nothing more. It approached `forbidden_claims` #3 (`"The hospital refused to treat her because of her insurance"`) and contradicted the script's own line at L99 (`Nobody ever proved why the call was made, or by whom, or what was in anybody's mind.`). |
| **Verdict** | **LOCKED** — attribution returned to the witness; the verb is the opinion's. |

### 2.2 A conditional of the court's collapsed into the indicative · **RESOLVED**

| | |
| --- | --- |
| **v001 said** | `The wait it says she abandoned is a wait it had already ended.` |
| **v002 says (L296)** | `Then the wait it says she abandoned would be a wait it had already ended.` |
| **Ledger row** | **HA-08** (✓ VERBATIM) |
| **The opinion's own wording** | *"If the jury believed the physician's testimony, it could well have found that HSF never intended to treat the decedent, or, at the least, was itself responsible for truncating her wait."* |
| **Why it was a defect** | The court's sentence is conditional from beginning to end (*If the jury believed… it could well have found…*). v001's indicative made the film more certain than the court, which is the operation `forbidden_claims` #3 punishes. |
| **Verdict** | **LOCKED** — the conditional now runs through both halves (`If the hospital had arranged… / Then the wait… would be…`). |

### 2.3 The opinion's one speculative sentence narrated without audible attribution · **RESOLVED**

| | |
| --- | --- |
| **v001 said** | `The reason given for it is the sentence to carry out of this film. It states precisely what the case was about and what it was not.` / `Due to the Hospital's failure to provide even the most rudimentary screening, Ms. Gonzalez spent the few remaining hours of her life in agony…` |
| **v002 says (L375, L377)** | `The court gave its reason in two sentences.` / `Due to the Hospital's failure to provide even the most rudimentary screening, **the court wrote**, Ms. Gonzalez spent the few remaining hours of her life in agony, beset by nausea, dizziness, and chest pains. It is hard to imagine — let alone to quantify in dollars — the sheer terror that she must have felt while waiting for medical attention that never came.` |
| **Ledger row** | **DM-15** (✓ VERBATIM), **TL-14** (✓ VERBATIM) |
| **The opinion's own wording** | identical — *"Due to the Hospital's failure to provide even the most rudimentary screening, Ms. Gonzalez spent the few remaining hours of her life in agony, beset by nausea, dizziness, and chest pains. It is hard to imagine — let alone to quantify in dollars — the sheer terror that she must have felt while waiting for medical attention that never came."* |
| **Why it was a defect** | On the page it was a correct VERBATIM quotation. **Spoken**, with no audible attribution and a narrator's evaluation immediately before it, *"the sheer terror that she must have felt"* is heard as the narrator guessing at a dead woman's mind — the exact operation `forbidden_claims` #4 and ledger Q-05 forbid. |
| **Verdict** | **LOCKED** — `the court wrote` is a broadcast attribution insertion between two of the court's clauses; **not one word of DM-15 is changed, removed or reordered** (confirmed mechanically: §4 run #136, 46 tokens, exact). |

**Also removed by the second pass, and confirmed gone from v002** (out-of-record narrator assertions, RQ-04 class — the opinion contains no statistics and no statement about emergency departments in general):

| v001 wording | present in v002? |
| --- | --- |
| `That caveat is not decoration. Every emergency department runs a queue.` | ✗ removed |
| `Nobody told her the department was full, or that her plan was wrong.` (the plan clause) | ✗ removed — v002 L282 reads `Nobody told her the department was full.` |
| `And it does not say that a wait killed a woman. It says a woman waited, unattended, and that the law had already promised her otherwise.` | ✗ removed (`the law had already promised her otherwise` brushes `forbidden_claims` #10 / Q-10) |

---

## 3. THE TEN QUOTATION DIVERGENCES THE MECHANICAL AUDIT CORRECTED — all RESOLVED

Every row below was a place where v001 put a word into a sentence of the court's, or took one out, or
changed one. **All ten are gone from v002.** The `v002 wording` column is the text in the file now, and
each was re-confirmed against the raw opinion by the mechanical pass in §4 (run number given).

| # | ledger | v001 wording (defect) | **v002 wording (current)** | the opinion's own wording | §4 run | verdict |
|---|---|---|---|---|---|---|
| 1 | **CR-08** | `The Hospital **disagreed**, maintaining that…` | `The Hospital **disagrees**, maintaining that its personnel were told only that Ms. Gonzalez felt dizzy and nauseated.` (L52) | *"The Hospital disagrees, maintaining that its personnel were told only that Ms. Gonzalez felt dizzy and nauseated."* | #5 | **LOCKED** |
| 2 | **EM-11** | `But **the private damages remedy** requires a showing of personal harm…` | `But **the statutory damage remedy** requires a showing of personal harm as a direct result of a participating hospital's violation.` (L167) | *"the statutory damage remedy requires a showing of 'personal harm as a direct result of a participating hospital's violation of [EMTALA]'"* | #53 | **LOCKED** |
| 3 | **HA-16** | `…and **it could not fault the jury** either for crediting his recollection…` | `…and **we cannot fault the jury** either for crediting his recollection or for concluding that the Hospital denied Ms. Gonzalez any vestige of an appropriate screening.` (L270) | *"we cannot fault the jury either for crediting his recollection or for concluding that the Hospital denied Ms. Gonzalez any vestige of an appropriate screening"* | #90 | **LOCKED** |
| 4 | **DM-05** | the reported divergence is the connective **`one that`** — a relative clause of the writer's own placed inside a sentence of the court's, so the court's words were spoken inside the narrator's syntax. **Note on evidence:** the string `one that` is **not** in `EP63_correa_script.en.v001.md` as it stands on disk; that file carries the earlier form of the same defect, the appositive `…the final pretrial order — **an order** intended to control the subsequent course of the action, and **modifiable only** to prevent manifest injustice.` The `one that` form belongs to a working draft between v001 and v002 that was not kept. Both are the same operation on the same sentence, and both are gone. | `It gave special weight to the Hospital's boycott of the final pretrial order. **That order is** intended to control the subsequent course of the action, **and can be modified only** to prevent manifest injustice.` (L357) | *"special weight to the Hospital's boycott of the final pretrial order,"* which *"is intended to 'control the subsequent course of the action,' and can be modified only 'to prevent manifest injustice.'"* | #124 | **LOCKED** |
| 5 | **DM-07** | `A renewed motion under Rule 50(b) is bounded by **the earlier one**.` | `A renewed motion under Rule 50(b) is bounded by **the movant's earlier Rule 50(a) motion**.` (L359) | *"bounded by the movant's earlier Rule 50(a) motion. The movant cannot use such a motion as a vehicle to introduce a legal theory not distinctly articulated in its close-of-evidence motion for a directed verdict."* | #126 | **LOCKED** |
| 6 | **CR-16** | `…during its business hours. **It also allowed** her to see any appropriate health-care provider…` — the court's single sentence split in two and a subject supplied by the writer | `…during its business hours, **but allowed** her to see any appropriate health-care provider in case of an emergency.` (L66) | *"Ms. Gonzalez's health insurance plan required her to seek routine treatment at Hospmed (a local clinic) during its business hours, but allowed her to see any appropriate health-care provider in case of an emergency."* | #11 | **LOCKED** |
| 7 | **CR-21** | `…started intravenous infusions of fluids, **and dispensed** medicine to control the emesis.` | `…the physician immediately started intravenous infusions of fluids. **She also dispensed** medicine to control the emesis.` (L84) | *"when she began vomiting, the physician immediately started intravenous infusions of fluids. She also dispensed medicine to control the emesis."* | #16 | **LOCKED** |
| 8 | **CR-25** | `…as Dr. Rojas **herself** explained…` — an intensifier of the writer's own inside the court's sentence | `…that symptomatology — **as Dr. Rojas explained** — might well herald the onset of an emergency medical condition in the case of a hypertensive diabetic.` (L203) | *"that symptomatology, as Dr. Rojas explained, might well herald the onset of an emergency medical condition in the case of a hypertensive diabetic (such as Ms. Gonzalez)"* | #70 | **LOCKED** |
| 9 | **AS-10** | `…required its emergency room personnel, **among other things**, promptly to take the vital signs…` — a translation of the court's *inter alia* placed inside the quotation | `Its rules, as explicated in its policy statement, required its emergency room personnel promptly to take the vital signs of every patient who visited the facility.` (L235) | *"required its emergency room personnel, inter alia, promptly to take the vital signs of every patient who visited the facility, to make a written record of all such visits, to treat patients suffering from chest pains as critical cases, and to refer all critical cases to an in-house physician immediately"* | #80 | **LOCKED** — *inter alia* elided under the script's QUOTATION RULE, not translated |
| 10 | **AS-11** | `…the Hospital's utter inability to produce any records **anent Ms. Gonzalez's visit**.` — retained a word that does not speak | `…especially Angel Correa's recollections, and the Hospital's utter inability to produce any records.` (L241) | *"the Hospital's utter inability to produce any records anent Ms. Gonzalez's visit"* | #82 | **LOCKED** — tail truncation only; *anent* was **not** replaced with *of* (that would have altered the quotation) |

---

## 4. MECHANICAL EXTRACTION OF EVERY REMAINING QUOTATION IN v002

### 4.1 Method (nothing here is hand-picked)

1. The narration of v002 is reduced to a token stream — headings, `【…】` direction and `⟨HELD⟩` removed, everything else kept. **5,505 tokens.**
2. The raw opinion is normalised (§4.2) into one token string. **8,263 tokens.**
3. A **longest-common-run walk** is made over the narration: at each position, the longest run of consecutive narration tokens that occurs verbatim in the opinion is taken; a run of **6 tokens or more is recorded as a quotation** and the walk jumps past it; otherwise the walk advances one token. **The extractor chooses the quotations, not the writer and not the reviewer.**
4. A second pass at a floor of **4 tokens** recovers the short quoted fragments the first floor steps over (*"This contention is spurious."*, *"Much depends upon circumstances."*, *"unconditional seal of approval"*, *"both disingenuous and unpersuasive"*).
5. Every recorded run is, by construction, an exact match against the opinion. **Any place where the script's wording diverged inside a quotation would show up as a short unmatched gap between two long runs**; all 44 such gaps were read individually (§4.3).

### 4.2 Normalisation applied to the raw capture (and why each is necessary)

The CourtListener capture is a page-image transcription and is not clean. Without these five steps the
comparison produces **false ABSENTs** — it did so in an earlier audit of this episode.

| # | Normalisation | Why |
| --- | --- | --- |
| 1 | Curly quotes `‘ ’ “ ”` → straight | the capture and the ledger use different quote glyphs for the same words |
| 2 | All dash forms `‐ ‑ ‒ – — ― −` → `-`, then folded away | the capture has **lost the opinion's em-dashes**; the ledger restores them with `—` |
| 3 | `§` folded to a space | the capture prints `1395dd(a)` where the opinion prints `§ 1395dd(a)`; the ledger restores `§` |
| 4 | **Lines consisting only of digits are deleted** | **the capture prints the page number on its own line in the middle of a sentence.** e.g. *"…a datum suggesting that HSF tried to shunt Ms."* → `2Ms. Gonzalez's health insurance plan…` → `3` → *"Gonzalez to Hospmed as soon as it scrutinized…"*. **This is the specific defect that caused the earlier false ABSENT.** |
| 5 | Duplicated running headers removed; footnote blocks lifted out of the main flow and appended | the capture repeats every heading (`I. THE FACTS I. THE FACTS`, `SELYA, Circuit Judge.`) and interleaves footnote bodies mid-sentence, which would otherwise split a run in two |
| 6 | Case folded; every non-alphanumeric run collapsed to a single space | so that punctuation, `&amp;`, and line wrapping cannot cause a miss |

### 4.3 Result

| | |
| --- | --- |
| Narration tokens in v002 | **5,505** |
| Quotations extracted at floor 6 | **141 runs** |
| Additional quotations recovered at floor 4 | **48 runs** |
| **Total quotations checked** | **189** |
| **Confirmed verbatim against the raw opinion** | **189 (100%)** |
| Narration tokens that are the court's own words | **2,615 at floor 6 · 2,811 including the short fragments (51%)** |
| Longest single quotation | **60 tokens** (PF-05/PF-06, L367 — the family description) |
| Gap sites between two long runs (≤4 unmatched tokens) | **44 — all read; all are one of three benign classes** |
| — attribution insertions | `the court wrote` · `the opinion continues` · `the opinion says` · `the panel held` · `the opinion records` · `the court replied` · `the appeals court later said` |
| — narrator connective **outside** the court's sentence | `Second:` · `Then the compression.` · `it cited a case` · `it gave` |
| — a number or a name spoken instead of printed | `ninety over sixty` (90/60) · `five hundred thousand dollars` ($500,000) · `Angel, Esther and Gloria` |
| **Gap sites that are a word substituted inside a court sentence** | **0** |

### 4.4 The 189 confirmed quotations

`ledger` = the ledger row(s) whose text contains the fragment, matched mechanically; `—` means the
fragment is the court's wording carried by a ✓ (non-VERBATIM) ledger row rather than by a quoted span.
A `Q-` row in this column means the fragment appears inside a **quarantine row's explanation** (the
quarantine rows quote the opinion in order to forbid misreading it) — **it does not mean a quarantined
claim is used**; see §7.

#### HOOK

**No run of 6 tokens or more, and one of 4** (`to bide her time`, L30, **CR-09**) — the HOOK is the writer's own 20-word compression of ACT_1 and quotes nothing. That is the intended shape (`STRUCTURAL LOCKS · hook 8s cut pre-resolution`), and the extractor confirms it.

#### OP

| # | script L | ledger | tok | the script's wording — identical to the opinion's | verdict |
|---|---|---|---|---|---|
| 1 | L38 | — | 9 | United States Court of Appeals for the First Circuit | LOCKED |

#### ACT_1

| # | script L | ledger | tok | the script's wording — identical to the opinion's | verdict |
|---|---|---|---|---|---|
| 2 | L46 | CR-02 | 6 | a sixty-five-year-old widow | LOCKED |
| 3 | L48 | CR-04 | 6 | her to the emergency room at | LOCKED |
| 4 | L52 | — | 15 | as to whom she saw and what that person was told about her condition. Angel | LOCKED |
| 5 | L52 | CR-01, CR-07, CR-08 | 39 | testified that he implored the receptionist to have someone take care of my mother, because she feels sick and has chest pains. The Hospital disagrees, maintaining that its personnel were told only that Ms. Gonzalez felt dizzy and nauseated | LOCKED |
| 6 | L56 | — | 9 | the sufficiency of the evidence, the court of appeals | LOCKED |
| 7 | L56 | CT-11 | 6 | the facts, and the reasonable inferences | LOCKED |
| 8 | L56 | CT-11 | 10 | in the light most hospitable to the jury's verdict | LOCKED |
| 9 | L56 | CT-12 | 13 | the thicket of conflicting testimony and the chasmal gaps in the direct evidence | LOCKED |
| 10 | L62 | CR-09, RQ-10 | 22 | a Hospital employee assigned the patient a number, forty-seven, told her to bide her time, and checked her medical insurance card | LOCKED |
| 11 | L66 | CR-16 | 31 | plan required her to seek routine treatment at Hospmed, a local clinic, during its business hours, but allowed her to see any appropriate health-care provider in case of an emergency | LOCKED |
| 12 | L72 | CR-01, CR-12 | 23 | Ms. Gonzalez maintained her unproductive vigil for an additional forty-five to seventy-five minutes. The Hospital staff continued blithely to ignore her | LOCKED |
| 13 | L76 | CR-15 | 16 | her.  Weary of waiting, the two women drove to the office of Dr. Acacia Rojas Davis | LOCKED |
| 14 | L78 | CR-13 | 7 | the director of Hospmed, arriving there between | LOCKED |
| 15 | L84 | CR-20 | 24 | Dr. Rojas that she was nauseated and had taken a double dose of her high blood pressure medication. Her blood pressure was very low | LOCKED |
| 16 | L84 | — | 23 | When she began vomiting, the physician immediately started intravenous infusions of fluids. She also dispensed medicine to control the emesis.  Despite these ministrations | LOCKED |
| 17 | L86 | CR-01, CR-23, Q-04 | 55 | Ms. Gonzalez's condition steadily deteriorated. Dr. Rojas had to resuscitate her soon after her arrival. The doctor then attempted to transfer her to the Hato Rey Community Hospital, but could not commandeer an ambulance.  As Dr. Rojas began preparations to transport Ms. Gonzalez by van, the patient expired. Her death, which occurred at around | LOCKED |
| 18 | L99 | CR-17 | 18 | a nurse called from HSF to advise her that the patient would be coming to Hospmed for treatment | LOCKED |
| 19 | L99 | CR-18 | 11 | said that this conversation probably occurred earlier that day, perhaps around | LOCKED |
| 20 | L99 | CR-01, CR-18 | 20 | a datum suggesting that HSF tried to shunt Ms. Gonzalez to Hospmed as soon as it scrutinized her insurance card | LOCKED |

#### ACT_2

| # | script L | ledger | tok | the script's wording — identical to the opinion's | verdict |
|---|---|---|---|---|---|
| 21 | L109 | CR-01, PF-02 | 6 | Ms. Gonzalez's three adult children | LOCKED |
| 22 | L109 | PF-02 | 17 | and four of her grandchildren, the progeny of her late son, Felix Correa, who had predeceased her | LOCKED |
| 23 | L109 | — | 12 | in the United States District Court for the District of Puerto Rico | LOCKED |
| 24 | L111 | PR-02 | 16 | EMTALA — inappropriate screening and improper transfer — and a pendent claim of medical malpractice under local law | LOCKED |
| 25 | L117 | — | 8 | case went to the jury on the two | LOCKED |
| 26 | L117 | PR-06 | 9 | the jury returned a series of special written findings | LOCKED |
| 27 | L119 | EM-18 | 6 | did present an emergency medical condition | LOCKED |
| 28 | L119 | PR-09 | 6 | and the evidence to that effect | LOCKED |
| 29 | L121 | CR-01 | 23 | need not comment upon the jury's finding that HSF also violated EMTALA by improperly transferring Ms. Gonzalez before her condition had stabilized | LOCKED |
| 30 | L123 | — | 12 | in damages on the decedent's account, payable to the heirs. And | LOCKED |
| 31 | L123 | PR-11 | 11 | for the pain, suffering, and mental anguish experienced by the survivors | LOCKED |
| 32 | L129 | PR-13 | 24 | The district court denied the Hospital's post-trial motions for judgment as a matter of law, a new trial, and remission of damages | LOCKED |
| 33 | L131 | PR-15 | 9 | HSF assigns error in no fewer than eight iterations | LOCKED |
| 34 | L137 | EM-01 | 8 | the Emergency Medical Treatment and Active Labor Act | LOCKED |
| 35 | L137 | EM-01 | 18 | this appeal requires us to interpret, for the first time, the Emergency Medical Treatment and Active Labor Act | LOCKED |
| 36 | L141 | — | 16 | As health-care costs spiralled upward and third-party payments assumed increased importance, Congress became concerned | LOCKED |
| 37 | L141 | EM-03 | 28 | about the increasing number of reports that hospital emergency rooms are refusing to accept or treat patients with emergency conditions if the patient does not have medical insurance | LOCKED |
| 38 | L145 | EM-04 | 13 | Needing a carrot to make health-care providers more receptive to the stick | LOCKED |
| 39 | L145 | EM-04 | 32 | Congress simultaneously amended the Social Security Act, conditioning hospitals' continued participation in the federal Medicare program — a lucrative source of institutional revenue — on acceptance of the duties imposed by the new law | LOCKED |
| 40 | L151 | EM-05 | 17 | afford an appropriate medical screening to all persons who come to its emergency room seeking medical assistance | LOCKED |
| 41 | L153 | EM-06, EM-18 | 22 | if an emergency medical condition exists, the participating hospital must render the services that are necessary to stabilize the patient's condition | LOCKED |
| 42 | L153 | EM-06 | 17 | unless transferring the patient to another facility is medically indicated and can be accomplished with relative safety | LOCKED |
| 43 | L155 | EM-07 | 12 | To add bite to its provisions, EMTALA establishes monetary penalties for noncompliance | LOCKED |
| 44 | L155 | EM-07 | 12 | and authorizes private rights of action against those who transgress its mandates | LOCKED |
| 45 | L157 | — | 14 | the hospital is a participating hospital, covered by EMTALA, that operates an emergency department | LOCKED |
| 46 | L157 | EM-08 | 8 | the patient arrived at the facility seeking treatment | LOCKED |
| 47 | L157 | EM-08, EM-18 | 20 | did not afford the patient an appropriate screening in order to determine if she had an emergency medical condition, or | LOCKED |
| 48 | L157 | EM-08, EM-18 | 23 | bade farewell to the patient — whether by turning her away, discharging her, or improvidently transferring her — without first stabilizing the emergency medical condition | LOCKED |
| 49 | L163 | EM-18 | 7 | an emergency medical condition when she arrived | LOCKED |
| 50 | L163 | EM-10 | 14 | this suggestion finds no purchase in the statute's text, and we reject it | LOCKED |
| 51 | L163 | EM-09 | 25 | The failure appropriately to screen, by itself, is sufficient to ground liability as long as the other elements of the cause of action are met | LOCKED |
| 52 | L167 | — | 6 | are imposable irrespective of resulting harm | LOCKED |
| 53 | L167 | — | 20 | the statutory damage remedy requires a showing of personal harm as a direct result of a participating hospital's violation | LOCKED |
| 54 | L167 | EM-11, EM-18 | 23 | to imagine a case in which a patient who does not present an emergency medical condition will meet the statute's causation requirement | LOCKED |
| 55 | L169 | EM-18, PR-09 | 16 | an emergency medical condition, the jury so found, and the evidence to that effect was ample | LOCKED |

#### ACT_3

| # | script L | ledger | tok | the script's wording — identical to the opinion's | verdict |
|---|---|---|---|---|---|
| 56 | L179 | — | 16 | predicate fact: that HSF had accepted the federal government's carrot and agreed to come under | LOCKED |
| 57 | L181 | HA-02 | 28 | introduced into evidence, without objection, HSF's policy statement outlining for its employees and associates how the Hospital intended to ensure compliance with EMTALA in its emergency room | LOCKED |
| 58 | L181 | HA-02 | 18 | health services administrator testified that he had dutifully instructed his staff regarding the fine points of EMTALA compliance | LOCKED |
| 59 | L185 | HA-01 | 8 | This argument has the shrill ring of desperation | LOCKED |
| 60 | L187 | — | 7 | Voiced for the first time on appeal | LOCKED |
| 61 | L187 | HA-04, Q-12, RQ-04 | 22 | had a rational basis on which to conclude that HSF is among the ninety-nine percent of American hospitals covered by EMTALA | LOCKED |
| 62 | L193 | CR-01, EM-18 | 30 | The Hospital asserts that it had no obligation to screen because Ms. Gonzalez did not have an emergency medical condition when she reported to its facility. This theory of defense | LOCKED |
| 63 | L195 | — | 23 | to all who enter the hospitals' emergency departments, whether or not they are in the throes of a medical emergency when they arrive | LOCKED |
| 64 | L197 | — | 9 | his mother was experiencing chest pains. And HSF concedes | LOCKED |
| 65 | L197 | CR-01, CR-26, EM-18 | 22 | that a patient of Ms. Gonzalez's age who suffered from chest pains would be regarded as having an emergency medical condition | LOCKED |
| 66 | L199 | CR-01, CR-27 | 16 | that Ms. Gonzalez did not develop chest pains until some time after she arrived at Hospmed | LOCKED |
| 67 | L201 | — | 13 | There is no principled way in which we can accommodate HSF's request | LOCKED |
| 68 | L201 | HA-06 | 13 | Credibility choices are generally for the jury, not for the court of appeals | LOCKED |
| 69 | L203 | HA-06 | 10 | the chest pains might well have spurted and later subsided | LOCKED |
| 70 | L203 | EM-18 | 27 | of nausea and dizziness, that symptomatology — as Dr. Rojas explained — might well herald the onset of an emergency medical condition in the case of a hypertensive diabetic | LOCKED |
| 71 | L209 | AS-01 | 16 | EMTALA requires an appropriate medical screening, but does not explain what constitutes one. The adjectival phrase | LOCKED |
| 72 | L213 | AS-02 | 44 | Appropriate is one of the most wonderful weasel words in the dictionary, and a great aid to the resolution of disputed issues in the drafting of legislation. Who, after all, can be found to stand up for inappropriate treatment or actions of any sort | LOCKED |
| 73 | L215 | AS-03 | 14 | appropriateness, like nature, is a mutable cloud which is always and never the same | LOCKED |
| 74 | L219 | AS-04 | 48 | A hospital fulfills its statutory duty to screen patients in its emergency room if it provides for a screening examination reasonably calculated to identify critical medical conditions that may be afflicting symptomatic patients, and provides that level of screening uniformly to all those who present substantially similar complaints | LOCKED |
| 75 | L221 | AS-05 | 19 | The essence of this requirement is that there be some screening procedure, and that it be administered even-handedly | LOCKED |
| 76 | L225 | AS-06 | 11 | EMTALA does not create a cause of action for medical malpractice | LOCKED |
| 77 | L225 | AS-07 | 14 | A refusal to follow regular screening procedures in a particular instance contravenes the statute | LOCKED |
| 78 | L225 | AS-07 | 23 | But faulty screening, in a particular case, as opposed to disparate screening or refusing to screen at all, does not contravene the statute | LOCKED |
| 79 | L235 | — | 12 | rules, as explicated in its policy statement, required its emergency room personnel | LOCKED |
| 80 | L235 | AS-10 | 44 | promptly to take the vital signs of every patient who visited the facility. To make a written record of all such visits. To treat patients suffering from chest pains as critical cases. And to refer all critical cases to an in-house physician immediately | LOCKED |
| 81 | L241 | — | 6 | From the evidence adduced at trial | LOCKED |
| 82 | L241 | — | 15 | especially Angel Correa's recollections, and the Hospital's utter inability to produce any records | LOCKED |
| 83 | L249 | AS-11 | 53 | the jury reasonably could have inferred that the Hospital did not measure up to the parameters it had established, and that the decedent was denied the screening — monitoring of vital signs, compilation of a written chart, immediate referral to an in-house physician — that HSF customarily afforded to persons complaining of chest pains | LOCKED |
| 84 | L251 | AS-08 | 29 | In this case, HSF's delay in attending to the patient was so egregious and lacking in justification as to amount to an effective denial of a screening examination | LOCKED |
| 85 | L253 | AS-09 | 19 | thus, we need not decide whether mere negligence in failing to expedite screening would itself violate the federal statute | LOCKED |
| 86 | L256 | AS-13, CR-01, Q-08 | 15 | The jury's finding that HSF denied Ms. Gonzalez an appropriate screening examination is unimpugnable | LOCKED |

#### ACT_4

| # | script L | ledger | tok | the script's wording — identical to the opinion's | verdict |
|---|---|---|---|---|---|
| 87 | L266 | HA-17 | 39 | To be sure, the evidence in this case is not particularly precise. But facts at trial, as in life, do not always appear in black and white. Juries and judges frequently must distinguish between manifold shades of gray.  The | LOCKED |
| 88 | L268 | HA-17 | 6 | that the grays predominate here. That | LOCKED |
| 89 | L270 | HA-16 | 10 | Angel Correa's credibility emerged relatively unscathed from cross-examination | LOCKED |
| 90 | L270 | CR-01, HA-16 | 25 | we cannot fault the jury either for crediting his recollection or for concluding that the Hospital denied Ms. Gonzalez any vestige of an appropriate screening | LOCKED |
| 91 | L270 | HA-14 | 22 | which could have supplied a foolproof answer from its own records, offered nothing to suggest that it did not welcome Medicare patients | LOCKED |
| 92 | L272 | CR-01, HA-15 | 28 | heard testimony from which it could have concluded that Ms. Gonzalez went to the Hospital in critical condition and received only a high number and a cold shoulder | LOCKED |
| 93 | L274 | HA-15 | 7 | A high number and a cold shoulder | LOCKED |
| 94 | L280 | CT-12 | 13 | the thicket of conflicting testimony and the chasmal gaps in the direct evidence | LOCKED |
| 95 | L280 | CR-06 | 15 | conflicted as to whom she saw and what that person was told about her condition | LOCKED |
| 96 | L280 | CR-01, CR-08 | 13 | that its personnel were told only that Ms. Gonzalez felt dizzy and nauseated | LOCKED |
| 97 | L280 | CR-27 | 13 | did not develop chest pains until some time after she arrived at Hospmed | LOCKED |
| 98 | L280 | AS-15, Q-10 | 8 | that an emergency room cannot serve everyone simultaneously | LOCKED |
| 99 | L284 | CR-01 | 14 | neither denied Ms. Gonzalez an initial screening nor refused her essential treatment. Its point | LOCKED |
| 100 | L284 | HA-08 | 16 | that it gave the patient a number, and would have ministered to her had she waited | LOCKED |
| 101 | L292 | CR-01 | 10 | According to Dr. Rojas, HSF referred Ms. Gonzalez to Hospmed | LOCKED |
| 102 | L292 | CR-19 | 13 | we note, as an aside, that HSF called Dr. Rojas as its witness | LOCKED |
| 103 | L294 | — | 8 | If the jury believed the physician's testimony | LOCKED |
| 104 | L294 | HA-08 | 24 | it could well have found that HSF never intended to treat the decedent, or, at the least, was itself responsible for truncating her wait | LOCKED |
| 105 | L300 | AS-14 | 34 | a complete failure to attend a patient who presents a condition that practically everyone knows may indicate an immediate and acute threat to life can constitute a denial of an appropriate medical screening examination | LOCKED |
| 106 | L306 | AS-16 | 6 | absent any explanation or mitigating circumstances | LOCKED |
| 107 | L306 | AS-16 | 13 | that the Hospital's inaction here amounted to a deliberate denial of screening | LOCKED |
| 108 | L312 | AS-17 | 13 | EMTALA should be read to proscribe both actual and constructive dumping of patients | LOCKED |
| 109 | L325 | — | 13 | the suspicion that the patient will be unable adequately to pay her way | LOCKED |
| 110 | L325 | CR-01 | 13 | Ms. Gonzalez had insurance that permitted her hospital visit if an emergency existed | LOCKED |
| 111 | L327 | EM-13 | 33 | Every court of appeals that has considered this issue has concluded that a desire to shirk the burden of uncompensated care is not a necessary element of a cause of action under EMTALA | LOCKED |
| 112 | L329 | EM-12 | 34 | We hold, therefore, that EMTALA, by its terms, covers all patients who come to a hospital's emergency department, and requires that they be appropriately screened, regardless of insurance status or ability to pay | LOCKED |
| 113 | L331 | HA-09 | 46 | All insurance plans are not created equal. Given the bewildering array of coverage conditions, deductibles, reimbursement rates, and the like, sophisticated but esurient providers have ample provocation to discriminate not only between insured and uninsured patients but also among patients who are insured under different plans | LOCKED |
| 114 | L335 | EM-17 | 20 | A participating hospital may not delay provision of an appropriate medical screening examination required under subsection (a) of this section | LOCKED |
| 115 | L335 | EM-17 | 14 | in order to inquire about the individual's method of payment or insurance status | LOCKED |

#### ACT_5

| # | script L | ledger | tok | the script's wording — identical to the opinion's | verdict |
|---|---|---|---|---|---|
| 116 | L353 | — | 13 | first had the opportunity to assert this defense in its answer to the | LOCKED |
| 117 | L353 | — | 17 | the pretrial order, signed by all counsel and entered by the district court, made no mention of | LOCKED |
| 118 | L353 | — | 8 | moved for judgment as a matter of law | LOCKED |
| 119 | L353 | — | 7 | at the close of the plaintiffs' case | LOCKED |
| 120 | L353 | — | 7 | at the close of all the evidence | LOCKED |
| 121 | L355 | DM-03 | 7 | This was a waiver, pure and simple | LOCKED |
| 122 | L357 | DM-04 | 7 | Based on this somber record of inattention | LOCKED |
| 123 | L357 | DM-04 | 10 | HSF forfeited the theory of defense that it now espouses | LOCKED |
| 124 | L357 | DM-05 | 33 | special weight to the Hospital's boycott of the final pretrial order. That order is intended to control the subsequent course of the action, and can be modified only to prevent manifest injustice | LOCKED |
| 125 | L359 | DM-06 | 19 | This motion is a classic example of a litigant locking the barn door long after the horse has bolted | LOCKED |
| 126 | L359 | DM-07 | 41 | 50(b) is bounded by the movant's earlier Rule 50(a) motion. The movant cannot use such a motion as a vehicle to introduce a legal theory not distinctly articulated in its close-of-evidence motion for a directed verdict | LOCKED |
| 127 | L361 | DM-08 | 21 | say it was plain error for the lower court, in the absence of any timely objection, to interpret the statute generously | LOCKED |
| 128 | L365 | DM-11 | 32 | award must endure unless it is grossly excessive, inordinate, shocking to the conscience of the court, or so high that it would be a denial of justice to permit it to stand | LOCKED |
| 129 | L367 | PF-05, PF-06 | 60 | The testimony indicated that the decedent was a matriarchal figure who functioned as the hub of the family circle. Her son Angel lived with her. Her two daughters, Gloria and Esther, resided nearby. Her deceased son's four children — who lost their father a mere five months before their grandmother perished — dwelt in her home for much of their lives | LOCKED |
| 130 | L367 | PF-07 | 6 | expert testified that all three of | LOCKED |
| 131 | L367 | PF-10 | 46 | children suffered depression in the wake of their mother's death, and that the four grandchildren experienced sadness, suffering and the like that would take up to five years to abate.  At trial, HSF neither rebutted this testimony in kind nor effectively impeached it. On appeal | LOCKED |
| 132 | L369 | HA-13 | 13 | as authority for a proposition exactly the opposite of what the case holds | LOCKED |
| 133 | L371 | — | 22 | that the plaintiffs suffered when the woman described by one witness as the trunk of the family tree was cut down. The | LOCKED |
| 134 | L373 | DM-14 | 13 | Though generous, the jury's assessment does not outstrip the bounds of reason | LOCKED |
| 135 | L377 | DM-15 | 13 | Due to the Hospital's failure to provide even the most rudimentary screening | LOCKED |
| 136 | L377 | CR-01, DM-15, TL-14 | 46 | Ms. Gonzalez spent the few remaining hours of her life in agony, beset by nausea, dizziness, and chest pains. It is hard to imagine — let alone to quantify in dollars — the sheer terror that she must have felt while waiting for medical attention that never came | LOCKED |
| 137 | L381 | DM-16, TL-13 | 40 | in which the decedent's travails extended over a period of several hours, is unlike cases involving sudden death in which a decedent's pain and suffering is limited to a few seconds or, at most, a matter of minutes | LOCKED |
| 138 | L385 | CT-09 | 40 | We need go no further. HSF has not presented arguments capable of overcoming the formidable hurdles it faces in challenging either the liability determination or the damage assessment of a properly instructed jury. The judgment below must therefore be affirmed | LOCKED |

#### ENDING

| # | script L | ledger | tok | the script's wording — identical to the opinion's | verdict |
|---|---|---|---|---|---|
| 139 | L395 | AS-09 | 10 | decide whether mere negligence in failing to expedite screening would | LOCKED |
| 140 | L395 | AS-08 | 18 | was so egregious and lacking in justification as to amount to an effective denial of a screening examination | LOCKED |
| 141 | L401 | AS-11 | 6 | referral to an in-house physician | LOCKED |

#### Short quotations below the 6-token floor (recovered by the second pass at floor 4)

| # | script L | ledger | tok | the script's wording — identical to the opinion's | verdict |
|---|---|---|---|---|---|
| S1 | L30 | CR-09 | 4 | to bide her time | LOCKED |
| S2 | L38 | — | 4 | v. Hospital San Francisco | LOCKED |
| S3 | L46 | CR-02 | 4 | On the morning of | LOCKED |
| S4 | L46 | CR-02 | 4 | Chills. Cold sweat. Dizziness | LOCKED |
| S5 | L48 | — | 4 | Carmen Gloria Gonzalez Figueroa | LOCKED |
| S6 | L48 | CR-04 | 5 | where she had been treated | LOCKED |
| S7 | L52 | CR-06 | 4 | The evidence is conflicted | LOCKED |
| S8 | L52 | — | 4 | Correa testified that he | LOCKED |
| S9 | L70 | CR-10, TL-05 | 5 | approximately one hour, Angel called | LOCKED |
| S10 | L72 | CR-12 | 5 | Now accompanied by her daughter | LOCKED |
| S11 | L88 | CR-24 | 5 | was attributed to hypovolemic shock | LOCKED |
| S12 | L95 | CR-24 | 5 | was attributed to hypovolemic shock | LOCKED |
| S13 | L109 | PR-11 | 5 | Angel, Esther and Gloria — and | LOCKED |
| S14 | L109 | PR-11 | 5 | Glendalis, Glorimar, Angelis and Sarai | LOCKED |
| S15 | L111 | PR-02 | 5 | They alleged two violations of | LOCKED |
| S16 | L119 | — | 5 | before her condition had stabilized | LOCKED |
| S17 | L121 | HA-06 | 4 | The court of appeals | LOCKED |
| S18 | L123 | PR-11 | 5 | apiece for the three children | LOCKED |
| S19 | L123 | PR-11 | 5 | apiece for the four grandchildren | LOCKED |
| S20 | L129 | PR-14 | 4 | unconditional seal of approval | LOCKED |
| S21 | L131 | — | 5 | the sufficiency of the evidence | LOCKED |
| S22 | L131 | PR-13 | 4 | a new trial, and | LOCKED |
| S23 | L149 | CR-01 | 5 | patients such as Ms. Gonzalez | LOCKED |
| S24 | L149 | — | 5 | has two linchpin provisions.  First | LOCKED |
| S25 | L163 | EM-08, EM-18 | 5 | had an emergency medical condition | LOCKED |
| S26 | L177 | — | 4 | that EMTALA did not | LOCKED |
| S27 | L181 | — | 4 | during the defense case | LOCKED |
| S28 | L183 | — | 4 | that EMTALA did not | LOCKED |
| S29 | L187 | — | 4 | that the policy statement | LOCKED |
| S30 | L187 | — | 4 | inadmissible hearsay and that | LOCKED |
| S31 | L197 | — | 4 | Angel testified that he | LOCKED |
| S32 | L203 | CR-01 | 4 | even if Ms. Gonzalez | LOCKED |
| S33 | L209 | AS-01 | 4 | is not self-defining | LOCKED |
| S34 | L247 | AS-10 | 4 | a written record of | LOCKED |
| S35 | L256 | — | 4 | That ends the matter | LOCKED |
| S36 | L286 | HA-08 | 4 | This contention is spurious | LOCKED |
| S37 | L292 | CR-17 | 4 | would be coming to | LOCKED |
| S38 | L306 | AS-15 | 4 | Much depends upon circumstances | LOCKED |
| S39 | L306 | — | 5 | the jury could rationally conclude | LOCKED |
| S40 | L327 | — | 4 | question of law, and | LOCKED |
| S41 | L353 | — | 4 | the initial scheduling conference | LOCKED |
| S42 | L359 | — | 4 | under Rule 50(b | LOCKED |
| S43 | L361 | — | 4 | may recover under EMTALA | LOCKED |
| S44 | L365 | — | 4 | for abuse of discretion | LOCKED |
| S45 | L369 | HA-13 | 4 | both disingenuous and unpersuasive | LOCKED |
| S46 | L371 | PF-08 | 5 | It is hard to doubt | LOCKED |
| S47 | L393 | AS-15, Q-10 | 4 | cannot serve everyone simultaneously | LOCKED |
| S48 | L397 | HA-06 | 4 | The court of appeals | LOCKED |

---

## 5. AUTHORISED DEVIATIONS — every place the script does not reproduce the opinion literally

The script's own QUOTATION RULE is: *"quotes may be SHORTENED, never altered… No word of the
narrator's goes inside a sentence of the court's."* These are the seven places where v002 shortens,
inserts an attribution, or shifts a verb. **Each was checked against the raw opinion individually**;
the mechanical pass in §4 reports each of them as a run boundary, not as a substitution.

| # | script L | ledger | what v002 does | the opinion's own wording | verdict |
| --- | --- | --- | --- | --- | --- |
| 5.1 | L300 | **AS-14** | tail truncation: `…can constitute a denial of an appropriate medical screening examination.` | *"…can constitute a denial of an appropriate medical screening examination **under section 1395dd(a)**."* | **LOCKED** — cut at the end, nothing altered. `§ 1395dd(a)` does not speak (FILM_BIBLE §19 R15-b); the full text stays in AS-14 |
| 5.2 | L241 | **AS-11** | tail truncation: `…the Hospital's utter inability to produce any records.` | *"…any records **anent Ms. Gonzalez's visit**."* | **LOCKED** — cut at the end. *anent* was **not** swapped for *of*: replacing a word would have altered the quotation (R15-d) |
| 5.3 | L371 | **DM-13** | **internal** elision: `The sums awarded, the court said, do not shock our collective conscience.` | *"the sums awarded do not shock **or even vellicate** our collective conscience"* | **LOCKED with note** — this is the **only** interior cut in the script. Authorised at FILM_BIBLE §19 R15-c (*vellicate* has no gloss the opinion itself supplies, so the quotation is shortened rather than annotated). It is also the reason this fragment falls below the extractor's floor and is confirmed here by direct comparison rather than by a run |
| 5.4 | L235 | **AS-10** | the court's `inter alia` is elided, not translated | *"required its emergency room personnel, **inter alia**, promptly to take the vital signs…"* | **LOCKED** — the script's QUOTATION RULE names this elision explicitly. v001's `among other things` was a translation inside the quotation and is gone (§3 row 9) |
| 5.5 | 18 sites | — | audible attributions inserted **between** the court's clauses: `the court wrote` · `the opinion says` · `the opinion continues` · `the opinion records` · `the panel held` · `the panel said` · `the court replied` · `the court said` · `the appeals court later said` · `the court summarized` | — | **LOCKED** — broadcast attribution. §4.3 confirms every one of them sits in a gap **between** two exactly-matching runs, never inside one |
| 5.6 | L284 | **HA-08** | reported speech, present → past: `Its point **was** that it gave the patient a number, and would have ministered to her had she waited.` | *"Its point **is** that it gave the patient a number and would have ministered to her had she waited."* | **LOCKED with note** — the sentence is framed as the hospital's argument reported by the narrator (`The hospital said it had neither denied…`), not as a quotation. One verb, tense only, no change of meaning. Flagged so a reviewer can see it was measured, not missed |
| 5.7 | L167 | **EM-11** | `But` joins two of the court's sentences across an elided citation | *"…are imposable irrespective of resulting harm. **See 42 U.S.C. § 1395dd(d)(1)(A).** The statutory damage remedy requires a showing of…"* | **LOCKED** — `But` begins a new sentence and stands **outside** both of the court's sentences; the elided material is a citation, which does not speak |

---

## 6. THE CAUSATION LOCK

> `forbidden_claims` #3: *"The hospital's delay killed her" / "she would have lived if they had seen her."*
> **THE SINGLE MOST LIKELY FACTUAL FAILURE IN THIS EPISODE.**
> Ledger **Q-03** (⛔) and **RQ-06** (○): the opinion attributes her death to hypovolemic shock and
> **never states that HSF's conduct caused it**.

### 6.1 The lines where the script states the negative — verbatim, with line numbers

The lock is not carried by a disclaimer. It is stated six times, in six different registers, and the
third block (L93-95, immediately after the death, held) is the load-bearing one.

**ACT_1 · L80 — the negative about the departure**
> `The opinion does not describe anyone turning her away. It does not describe anyone discharging her. She left because she had been waiting.`

**ACT_1 · L91 — the boundary of the record**
> `That is the whole of what the record says about how she died.`

**ACT_1 · L93–95 — the lock itself, immediately after the death, held**
> `One thing about that death has to be said plainly, because the rest of this case depends on it.`
> `The opinion never says the hospital's delay killed her. It never says she would have lived. Her death was attributed to hypovolemic shock, it happened at another facility, and it happened under a physician's care. The federal case that follows is not about her death. It is about what happened while she was still sitting there.`

**ACT_5 · L379 — the payoff, four words after the court's own reason for the $200,000**
> `Not her death. The waiting.`

**ENDING · L397 — the negative about the holding**
> `It does not find that the hospital dumped her. A jury found a screening violation. The court of appeals held that finding unimpugnable, and said, as a proposition of law, that the statute reaches constructive dumping as well as actual dumping. Those are two different sentences, and the case is the second one.`

**ENDING · L405 — the negative about motive**
> `There is no villain in this record. No decision was ever testified to. Nobody was shown to have looked at an insurance card and formed a judgment about the person holding it.`

### 6.2 What carries the lock structurally, so the narrator does not have to repeat it

| script L | wording | ledger | why it is load-bearing |
| --- | --- | --- | --- |
| L88 | `Her death, which occurred at around half past four, was attributed to hypovolemic shock.` | **CR-24** ✓ VERBATIM | the cause of death is the opinion's own attribution, at another facility, under a physician's care |
| L113–115 | `The malpractice claim did not survive. The district court dismissed it, and that ruling was never appealed.` / `From that point on, nobody in this case was arguing about whether she was treated well. Only about whether she was looked at.` | **PR-04** ✓ VERBATIM · **AS-06** ✓ VERBATIM | the competence-of-care question left the case before the appeal. **This is the structural causation lock**: the film cannot be about whether care would have saved her, because the court was not |
| L123–125 | `Two hundred thousand dollars in damages on the decedent's account, payable to the heirs. And five hundred thousand dollars for the pain, suffering, and mental anguish experienced by the survivors…` | **PR-10 · PR-11** ✓ VERBATIM | the split of the money says what the money was for. Neither figure is for a death |
| L377 | `Due to the Hospital's failure to provide even the most rudimentary screening, the court wrote, Ms. Gonzalez spent the few remaining hours of her life in agony…` | **DM-15** ✓ VERBATIM | **the court's own causal chain runs screening-failure → suffering. It does not run to death.** The film's causal claim is the court's, word for word |

**Mechanical confirmation.** A sweep of the narration for every quarantined formulation (Q-01…Q-12)
returns three hits, and **all three are the script negating the claim**:

| pattern | hits | where |
| --- | --- | --- |
| `killed her` / `would have lived` | 1 | L95 — `The opinion never says the hospital's delay killed her. It never says she would have lived.` |
| `transfer was illegal / unlawful` | 1 | L399 — `It does not hold that the transfer was unlawful.` |
| `guarantee` | 1 | L393 — `It does not guarantee treatment.` |
| turned away · refused over insurance · dramatised death · other patients · receptionist's state of mind · court found dumping · families-can-sue decided · every hospital | **0** | — |

**Verdict: LOCKED.** No assertion in v002 connects the delay to the death, and no image is asked to
make the connection (`forbidden_subjects` bars the collapse, the crash cart, the flatline and the body).

### 6.3 The improper-transfer finding — stated once, marked never reviewed

| | |
| --- | --- |
| **The allegation (not the finding)** | **L109**: `They alleged two violations of a federal statute called EMTALA — inappropriate screening and improper transfer — and a pendent claim of medical malpractice under local law.` (**PR-02** ✓ VERBATIM) |
| **The finding — stated exactly once** | **L117**: `And it found, separately, that the hospital had violated the statute by transferring her improperly, before her condition had stabilized.` (**PR-08** ✓) |
| **Marked unreviewed in the very next line** | **L119**: `That third finding needs a marker on it. The court of appeals never reviewed it. In footnote seven the panel wrote that because it upheld the screening finding, it need not comment upon the jury's finding that HSF also violated EMTALA by improperly transferring Ms. Gonzalez before her condition had stabilized. It is a jury finding that was never tested on appeal. It plays no part in what this case decided.` |
| **The opinion's own wording (footnote 7)** | *"…need not comment upon the jury's finding that HSF also violated EMTALA by improperly transferring Ms. Gonzalez before her condition had stabilized"* — confirmed verbatim, **§4 run #29, 23 tokens** |
| **Restated as a negative in ENDING** | **L399**: `It does not hold that the transfer was unlawful. That finding was never reviewed.` |
| **Occurrences of the finding stated as an affirmed holding** | **0** |
| **Verdict** | **LOCKED** — `forbidden_claims` #7 (`"the court ruled the transfer was illegal"`) and ledger **Q-09** are not touched. The finding appears once, is marked in the same breath, and is denied once at the end |

---

## 7. NON-QUOTATION ASSERTIONS — the three NEEDS SOURCE rows

Everything in §4 is the court's own language and is confirmed. These five are the narrator's own
sentences that make a claim about the world or about the opinion, and they are the only ones in v002
that the ledger does not carry. **Three of them need a source row before the render.**

### 7.1 · L315 · **NEEDS SOURCE**

| | |
| --- | --- |
| **Script wording (L315)** | `Constructive. The word lawyers reach for when the law looks at effect instead of form. **Constructive notice is notice you never received but are treated as having received. Constructive eviction is the landlord who never changes the locks and never has to.**` |
| **Ledger row** | **none** |
| **The opinion's own wording** | none — the strings `constructive notice` and `constructive eviction` **do not occur anywhere in the opinion** (checked mechanically over the normalised raw text) |
| **Why it is flagged** | Two definitions of general law, stated as fact, one line before the film's recognition beat. The ledger's own reading rule is binding here: *"if a sentence you want to say is not on this page, it is not in the opinion, and it does not go in the script."* Nothing about them is wrong; nothing about them is sourced **in this packet**, which is single-source by instruction. |
| **Verdict** | **NEEDS SOURCE** |
| **Two ways to clear it** | (a) add a sourced row to a ledger revision (a legal dictionary is a second source and changes this episode's single-source posture — an owner call); **or (b)** cut both sentences and keep `Constructive. The word lawyers reach for when the law looks at effect instead of form.` followed by L317 `Constructive dumping is the hospital that never turns anybody away.` **Option (b) costs 28 words, needs no new source, and puts the recognition beat one sentence closer to the word that triggers it.** |

### 7.2 · L163 · **NEEDS SOURCE**

| | |
| --- | --- |
| **Script wording (L163)** | `The hospital argued that a screening claim requires proof that the patient actually had an emergency medical condition when she arrived. **Several district courts had said so in passing.** The First Circuit refused: this suggestion finds no purchase in the statute's text, and we reject it.` |
| **Ledger row** | **EM-10** ✓ VERBATIM — but EM-10 carries only the court's rejection, not a description of who had said it |
| **The opinion's own wording (footnote 5)** | *"To be sure, **some courts** have suggested **in dictum** that a plaintiff must show as an ingredient of an inappropriate screening claim that she suffered from an emergency medical condition when she arrived at the hospital. See, e.g., **Miller, 22 F.3d at 630 n.8**; Ruiz v. Kepler, 832 F. Supp. 1444, 1447 (D.N.M. 1993); Huckaby v. East Ala. Med. Ctr., 830 F. Supp. 1399, 1402 (M.D. Ala. 1993)."* |
| **Why it is flagged** | Two divergences in five words. The court says **"some courts"**, not *several district courts* — and **the first authority it cites, *Miller*, 22 F.3d, is a court of appeals, not a district court.** The script also drops **"in dictum"**, which is the court's own reason the suggestion carried no weight. |
| **Verdict** | **NEEDS SOURCE** |
| **Fix (uses the court's own words, no new source, ±0 words)** | `Some courts had said so in dictum.` |

### 7.3 · L331 · **NEEDS SOURCE**

| | |
| --- | --- |
| **Script wording (L331)** | `**The panel thought the premise naive**, and said so in a footnote. All insurance plans are not created equal. Given the bewildering array of coverage conditions, deductibles, reimbursement rates, and the like, sophisticated but esurient providers have ample provocation to discriminate…` |
| **Ledger row** | **HA-09** ✓ VERBATIM |
| **The opinion's own wording (footnote 8)** | *"In all events, this argument is **an oversimplification**, especially in the health care field. All insurance plans are not created equal…"* |
| **Why it is flagged** | *naive* is the narrator's word, and it is attached to a mental state (`the panel **thought**`). The court's word is *an oversimplification*, and the court says it of the **argument**, not of the panel's opinion of the premise. The quoted sentences that follow are exact (§4 run #113, 46 tokens); only the introduction diverges. |
| **Verdict** | **NEEDS SOURCE** |
| **Fix (uses the court's own word, no new source, ±0 words)** | `The panel called the argument an oversimplification, and said so in a footnote.` |

### 7.4 · L333 · **LOCKED with note**

| | |
| --- | --- |
| **Script wording (L333)** | `Esurient. Greedy. A judge picking a rare word rather than an ordinary one.` |
| **Ledger row** | **HA-09** ✓ VERBATIM (supplies *esurient* in context) |
| **Assessment** | A one-word gloss, not a claim about the case. FILM_BIBLE §19 R15-c authorises it **specifically because the court's own sentence supplies the sense** (*ample provocation to discriminate*), and refuses the same treatment for *vellicate*, where nothing in the opinion supplies it (§5.3). The distinction is deliberate and is applied consistently in v002. |
| **Verdict** | **LOCKED with note** — a reviewer who wants zero glosses may cut the three words; nothing depends on them |

### 7.5 · L66 · **LOCKED with note**

| | |
| --- | --- |
| **Script wording (L66)** | `Her health plan required her to seek routine treatment at Hospmed, a local clinic, during its business hours, but allowed her to see any appropriate health-care provider in case of an emergency. **She was entitled to be where she was.**` |
| **Ledger rows** | **CR-16** ✓ VERBATIM (the plan's terms) + **PR-09** ✓ (the jury found she presented an emergency medical condition, *"and the evidence to that effect was ample"*) |
| **Assessment** | An inference, not a new fact: the plan permitted any appropriate provider in an emergency, and the jury found an emergency. It is also the film's answer to `forbidden_claims` #2, so removing it would weaken the lock rather than strengthen it. |
| **Verdict** | **LOCKED with note** — inference from two ✓ rows, no fact added |

---

## 8. TOTALS BY VERDICT

| Class | Rows | LOCKED | NEEDS SOURCE | QUARANTINED |
| --- | ---: | ---: | ---: | ---: |
| §3+§4 quotations extracted mechanically and confirmed against the raw opinion | **189** | **189** | 0 | 0 |
| §2 factual defects carried in from v001, confirmed fixed | 3 | 3 (RESOLVED) | 0 | 0 |
| §3 quotation divergences corrected by the second pass, confirmed fixed | 10 | 10 (RESOLVED) | 0 | 0 |
| §5 authorised shortenings / attributions / one tense shift | 7 | 7 | 0 | 0 |
| §7 narrator assertions the ledger does not carry | 5 | 2 | **3** | 0 |
| §6 quarantine sweep, Q-01…Q-14 | 14 | — | — | **0 present** |
| **Total graded rows** | **214** | **211** | **3** | **0** |

- **Quotation fidelity: 189 / 189 (100%).** Divergences found by this pass: **0**.
- **The court's own words are 2,811 of the 5,505 narration tokens — 51% of the spoken script.**
- **Fabricated facts: 0. Quarantined claims used: 0. Real-person likeness claims: 0.**
- The three NEEDS SOURCE rows are all in §7, all are the narrator's own sentences, and **all three can be cleared with the court's own words at zero net word cost** — except 7.1, which is cleared by a 28-word cut.

---

## 9. WHAT THIS PACKET DOES NOT COVER

- **No second source.** This packet is single-source by instruction, exactly as the ledger is
  (`Rows citing anything other than this opinion: 0`). The three NEEDS SOURCE rows are flagged
  *because* a second source would be needed to keep them, not because the opinion contradicts them.
- **`RQ-01`…`RQ-10` remain ○.** Nothing in v002 asserts anything from that list, and nothing here
  promotes any of them.
- **Images are not checked here.** `forbidden_subjects` is enforced by `check_spec_satisfied.py`
  against the built film and by the labelled contact-sheet review of the 226 commissioned plates.
- **This is not the ship gate.** `scripts/check_final_acceptance.py 63` measures the rendered file.
  This packet is the row-5 input of `docs/PD_ONE_PASS_PRODUCTION_SPEC.v2.md` §B (`fact_recheck.<v>`
  packet (R2/R3) — facts/quotes locked verbatim), and it is a prerequisite to the render, not a
  substitute for the gate.

## 10. SOURCES

- *Correa v. Hospital San Francisco*, 69 F.3d 1184 (1st Cir. 1995) — full text as captured at
  `episodes/_planning/measurements/EP63_correa_RAW.md` (CourtListener cluster 196369).
  **The only source consulted for this packet.**
- `episodes/_planning/EP63_correa_FACTS_LEDGER.v001.md` — 177 graded rows, 105 VERBATIM.
- `episodes/_planning/EP63_correa_script.en.v002.md` — the script under check.
- `episodes/_planning/EP63_correa_script.en.v001.md` — retained for the §2/§3 before-and-after only
  (invariant 6: v001 is not deleted).
- `episodes/_planning/EP63_correa_FILM_BIBLE.v001.md` §19 — the craft review that ordered the
  second pass, and the authority for the deviations recorded in §5.
- `episodes/PD-2026-063-correa/episode_spec.v001.json` — `forbidden_claims`, `forbidden_subjects`.

*v001 · 2026-08-04 · model `episodes/PD-2026-017-onecoin/01_research/fact_recheck.v002.publish.md`*
