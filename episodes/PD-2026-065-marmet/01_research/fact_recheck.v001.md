# PD-2026-065-marmet — Fact Re-check v001 (R2/R3)

- **Re-check date:** 2026-08-04 JST
- **Status:** `PASS_WITH_OPEN_ITEMS` — 5 rows marked **NEEDS SOURCE**, none of them load-bearing for the thesis, all with a repair written out. No row is **QUARANTINED** in the live script; the 8 quarantined items below are all v001 material the second pass removed.
- **Target artefact:** `episodes/_planning/EP65_marmet_script.en.v002.md` (5,201 narration words, 8 sections, contract band [5100, 5600])
- **Render:** none yet. This is a script-stage re-check, run before assembly, not a pre-publish re-check.
- **Line references** are **real file lines** in v002 (CRLF, 371 lines). Note that the `Read`-tool view of this file is offset by −2 from line 11 onward; the numbers below are the file's own.

## Sources of truth for this pass

| Tag | Document |
|---|---|
| **SCOTUS** | *Marmet Health Care Center, Inc. v. Brown*, 565 U. S. 530 (2012) (per curiam), Nos. 11–391 and 11–394, decided February 21, 2012. Local capture `episodes/_planning/measurements/EP65_marmet_RAW.md` (CourtListener cluster 623142). |
| **Brown II** | *Brown ex rel. Brown v. Genesis Healthcare Corp.*, 229 W. Va. 382, 729 S.E.2d 217 (2012), decided June 13, 2012, Ketchum, C.J. Local capture `episodes/_planning/measurements/EP65_brown_remand_RAW.md` (CourtListener opinion 8182676, Harvard CAP; **no syllabus in the capture** — it begins at the author line). |
| **Ledger** | `episodes/_planning/EP65_marmet_FACTS_LEDGER.v001.md` — rows `MB-01`…`MB-53`, instructions `○-01`…`○-08`, quarantine `⛔-01`…`⛔-10`. |
| **Contract** | `episodes/PD-2026-065-marmet/episode_spec.v001.json` — `forbidden_claims`, `forbidden_subjects`, and the `notes` block that records the two deliberate source ambiguities. |

**Citation convention below:** `Brown II ¶N` means **line N of the local capture file**
`episodes/_planning/measurements/EP65_brown_remand_RAW.md`, not a paragraph number in the reporter. Footnote
numbers (`fn 6`, `fn 7`, `fn 52`) are the opinion's own, counted in order from the first footnote at capture
line 112. The capture has **no syllabus**, so no syllabus point is cited from it directly — every Syllabus Point
referenced below is quoted inside the body text of Brown II.

**No third source was consulted and nothing below comes from memory.** Where a claim needs a document neither capture contains, the row says so and is graded **NEEDS SOURCE** rather than being softened into a pass.

---

## 1. The mechanical audit

### 1.1 What the second pass reported

The second pass recorded a mechanical quotation audit of its own output: **123 quotation fragments extracted, 123 matched.** It also recorded two edits to the ENDING — the disposition sentence was rewritten (see §3) and a newly computed figure that sat past the 92% line was deleted (see §3.3, `Q-02`).

**That number is not accepted here.** A self-reported 100% match rate on a self-chosen fragment list is exactly the shape of the false green this project has been burned by. It was re-derived from scratch.

### 1.2 Independent re-extraction (this pass)

Method, so it can be re-run and disagreed with:

1. Narration is every line of v002 that is not a heading, a horizontal rule, a bolded lock/preamble block, a `>` blockquote, a `【…】` stage direction, or `⟨HELD⟩`. **146 lines, 5,258 tokens** after normalisation.
2. The corpus is **SCOTUS + Brown II concatenated, 7,850 tokens**, normalised with:
   - line-break de-hyphenation (`arbi-\ntration` → `arbitration`) — the SCOTUS slip capture is full of it;
   - **page markers stripped from the words they are glued to**: `*391record` → `record`, `*388with` → `with`, `*394We` → `We` (regex `\*\s*\d+`);
   - **the documented OCR corruptions normalised**: `uneonscionability`/`unconseionability` → `unconscionability`, `Brown 7` → `Brown I`, `Broitm I` → `Brown I`, `eases` → `cases`, `ease` → `case`, `Mar-met` → `Marmet`, `Marehio` → `Marchio`, `PAA` → `FAA`, `pui'poses` → `purposes`, `occur-l'ence` → `occurrence`, `eoui'ts` → `courts`;
   - footnote reference digits unglued from words (`clause5` → `clause`), leaving free-standing years and docket numbers intact;
   - case-folded, punctuation stripped.
3. Every maximal common word-span of **≥ 6 tokens** is reported.

**Result:**

| Threshold | Maximal matched spans | Matched tokens | Share of narration |
|---:|---:|---:|---:|
| ≥ 5 | 156 | 2,383 | 45.2% |
| **≥ 6** | **130** | **2,257** | **42.9%** |
| ≥ 7 | 120 | 2,197 | 41.6% |
| ≥ 8 | 109 | 2,120 | 40.3% |
| ≥ 10 | 85 | 1,915 | 36.4% |

The second pass's **123** falls between this pass's ≥6 (130) and ≥7 (120) counts, which is what a slightly different threshold or normalisation produces. **The two runs agree on substance and disagree on where to draw a line.** The count is therefore reported as a range, not as a single number: **120–130 verbatim spans, carrying 2,197–2,257 of 5,258 narration tokens.**

Longest verified spans: 51 tokens (L146, the *disingenuous* sentence), 48 (L190, §2 of the FAA; L124, the public-policy holding), 46 (L136, the "not hostile to arbitration" passage), 45 (L114, Syllabus Point 11 applied), 44 (L238, the remand instruction), 43 (L166 *tendentious reasoning*; L202 the categorical-rule sentence), 42 (L118, Syllabus Point 21), 41 (L140, the adhesion definition; L182, the opening rule).

### 1.3 The half of the audit that can actually fail

A span matcher only emits matches; it cannot report a failure. The real work is the **residue**: **116 unmatched runs of ≥ 10 tokens**. Every one was read against its line. **111 are narrator prose** — glosses, transitions, the short-sentence beats (*"All of them. That word is the hinge of the case."*). **Five are places where the script speaks in the register of the source but goes past it**; those five are §5, the NEEDS SOURCE register.

### 1.4 Nothing new past the 92% line

Modelled at the script's own 176 words-per-finished-minute with the fixed 8-second HOOK, v002 runs **29:32**; the 92% line lands at **27:11**.

- The last new fact in the film — the three dockets and the answer to the certified question, L335 — **closes at 27:03, eight seconds before the line.**
- ENDING (L345–L365, 418 words, 27:10–29:32) contains **zero numerals and zero proper nouns that do not appear earlier.** Mechanically: the only capitalised tokens in ENDING absent from everything before it are `Neither`, `Other`, `Those`, `Which`.
- v001's computed figure (`Q-02`) is gone and was **not relocated** — the string "two years and ten months", which the film bible proposed as a substitute in ACT_5, appears nowhere in v002. The film does no arithmetic in its last 8%.

---

## 2. §A — THE DISPOSITION IS NOT UNIFORM

The single most misstatable thing in this episode, and the one the contract names in capitals. **Brown II ends in three different ways, and the script must state all three separately.**

**Brown II's own disposition lines, verbatim from the capture:**

> Case No. 35494, Reversed and remanded.
> Case No. 35546, Reversed and remanded.
> Case No. 35636, Certified question answered.

| ID | Script wording (line) | Source | Verdict |
|---|---|---|---|
| **A-01** | L335: *"Case number 35494, Brown: reversed and remanded."* | Brown II disposition line 1; conclusion ¶: *"in the Brown case, the circuit court's August 25, 2009, order is reversed and the case is remanded for further proceedings."* | **LOCKED** |
| **A-02** | L335: *"Case number 35546, Taylor: reversed and remanded."* | Brown II disposition line 2; conclusion ¶: *"In the Taylor case, the circuit court's September 29, 2009, order is reversed, and the case is remanded for further proceedings."* | **LOCKED** |
| **A-03** | L335: *"Case number 35636, Marchio: certified question answered. Yes — the Nursing Home Act's waiver ban is preempted by the Federal Arbitration Act."* | Brown II disposition line 3; conclusion ¶: *"in the Marchio case, the circuit court's certified question whether Section 15(e) was preempted by the FAA is, as reformulated in [Brown I], answered 'Yes.'"* | **LOCKED** |
| **A-04** | L335: *"Unconscionability was left to be raised by the parties on remand, because the trial court had never considered it."* | Brown II ¶12: *"In the third [case], the issue of uneonscionability was not considered by the trial court, but may be raised by the parties on remand."* | **LOCKED** |
| **A-05** | L335 opens *"Then the disposition, and it is not one thing."* — the sentence that forbids the flattening before it happens | Editorial framing over A-01…A-04. No source claim. | **LOCKED** |

### A-06 — the anti-flattening sweep

Every place in v002 where all three cases are spoken of at once was read for a merged disposition. **None flattens.**

| Line | Wording | Why it is safe |
|---|---|---|
| L128 | *"In two of the three cases, the court ruled that the arbitration clauses were unconscionable and unenforceable — Brown's and Taylor's. In the third, Marchio's, it answered the certified question…"* | Splits 2/1 explicitly. Verbatim against Brown II ¶8. |
| L230 | *"Two of the three papers had been condemned twice… The third had been condemned once, on the categorical rule alone."* | Splits 2/1. Rests on MB-45/MB-46. |
| L337 | *"It hands the question back to the circuit courts and stops."* | Plural "courts", no count, no county, no uniform verb. |
| L361 | *"the state court reversed the orders in Brown's case and Taylor's case … and in the third case said only that the issue may be raised by the parties on remand"* | Splits 2/1. This is the repaired ENDING — see §3. |

**Verdict for §A: the script states all three dispositions separately, in ACT_5 and again in the ENDING, and never merges them.** `⛔-05` and the contract's `THE DISPOSITION IS NOT UNIFORM` warning are both satisfied.

---

## 3. §B — THE EVIDENCE ORDER AND ITS SCOPE

### 3.1 What the source actually says

Brown II, ¶ following the re-examination of the record — **verbatim**:

> After a thorough re-examination of the record, we reverse the circuit courts' orders in Brown's case and Taylor's case. The circuit court's order in Brown's case is devoid of any findings of fact or conclusions of law on the question of unconscionability. The circuit court's order in Taylor's case has some findings of fact, but the circuit court has not had the opportunity to comprehensively analyze the question of unconscionability under the guidelines we developed in Brown I. **We conclude the correct course is to remand these cases to the circuit courts for the taking of evidence, the full development of a \*391record, and proper consideration of whether the clauses are unconscionable.**

Two things are load-bearing and both are easy to lose:

1. **"these cases" = Brown and Taylor only.** The antecedent is the sentence two clauses earlier — *"we reverse the circuit courts' orders in Brown's case and Taylor's case"*. Marchio gets a different treatment: her certified question is answered, and unconscionability *"was not considered by the trial court, but may be raised by the parties on remand"* (¶12). **No evidence-taking instruction issues in Marchio's case.**
2. **Brown's and Taylor's orders both came out of the Circuit Court of Kanawha County.** Brown II ¶20: *"the Circuit Court of Kanawha County dismissed plaintiff Clayton Brown's suit"*. ¶22: *"the Circuit Court of Kanawha County dismissed plaintiff Jeffrey Taylor's suit"*. **Harrison County is Marchio's court** (¶24) — the one that never got the evidence instruction.

### 3.2 The defect in v001, recorded

v001, **line 368**, final paragraph of the ENDING (the film bible's §19 R10(b) cites this as L362 in its own reading of the file):

> *"Neither had been tried. Neither had been answered. Both had been handed to a circuit judge in Kanawha County and a circuit judge in Harrison County, with instructions to take evidence this time."*

**Four separate faults in one sentence.**

| # | Fault | What the record says |
|---|---|---|
| D-1 | It gives the evidence instruction to a Harrison County judge | Harrison County is Marchio's. Brown II gave her court an answered certified question, not an evidence order. |
| D-2 | It puts **two Kanawha orders under judges in two counties** | Both reversed orders — August 25, 2009 and September 29, 2009 — are Kanawha. Neither is Harrison. |
| D-3 | *"a circuit judge … and a circuit judge"*, singular each | Two separate orders in the same court. The singular merges the record into two individuals the opinion never identifies. |
| D-4 | *"this time"* | A reproach that is nowhere in either opinion. Brown II's reason is that no court had *been permitted* to take evidence, not that anyone had refused. |

v001 line 362 carried the same defect in softer form — *"in the hands of two circuit courts that had never taken a day of evidence on it"* — which asserts of both remaining questions what Brown II said only of Brown and Taylor.

### 3.3 The repair, verified

v002, **L361**:

> *"Neither had been answered. On the first, the state court reversed the orders in Brown's case and Taylor's case and permitted the parties to raise and develop their arguments regarding unconscionability anew, and in the third case said only that the issue may be raised by the parties on remand. On the second, it declined to consider the argument, which should be considered by the trial court first."*

| ID | Check | Result |
|---|---|---|
| **B-01** | The evidence quote is present and verbatim (L323) | **LOCKED** — 34-token span verified against Brown II. Script: *"We conclude the correct course is to remand these cases to the circuit courts for the taking of evidence, the full development of a record, and proper consideration of whether the clauses are unconscionable."* |
| **B-02** | Its scope is carried, not asserted | **LOCKED** — L317 names only Brown's order and Taylor's order in the two sentences immediately before the quote, so *"these cases"* resolves the way the source resolves it. The film never says "all three". |
| **B-03** | County names are absent from the ENDING | **LOCKED** — mechanically: `Kanawha` and `Harrison` appear at **L46 and L56 only**, both in ACT_1, both attached to the correct case. Zero occurrences after L56. |
| **B-04** | *"this time"* is gone | **LOCKED** — zero occurrences in v002. |
| **B-05** | The ENDING's account of the two open questions matches Brown II ¶12 | **LOCKED** — *"permit the parties to raise and develop their arguments regarding uneonscionability anew"* and *"may be raised by the parties on remand"* both verified as spans. |
| **B-06** | The second open question is disposed of the way Brown II disposes of it | **LOCKED** — Brown II fn 52: *"We decline to consider these two arguments, which should be considered by the trial court first."* Script L333 and L361 both use it. |

**One residual risk, recorded rather than fixed.** L323's *"these cases"* is scoped by adjacency, not by a stated count. If assembly ever cuts L317 or moves L323, the quotation starts floating and the flattening returns. **L317 and L323 must stay adjacent and in order.** Add it to the assembly notes.

---

## 4. §C — PER CURIAM

| ID | Script wording (line) | Source | Verdict |
|---|---|---|---|
| **C-01** | L28: *"It is five pages long, and it is per curiam — an opinion issued by the Court with no author's name on it and no vote reported."* | SCOTUS capture: header `PER CURIAM.`, running head `Per Curiam` on all five pages, page markers 1–5. MB-01. | **LOCKED** |
| **C-02** | L180: *"Five pages, per curiam."* | Same. | **LOCKED** |
| **C-03** | L258: *"This was a per curiam opinion. Per curiam means by the court. There is no author, no reported vote, and no separate writing attached to the text."* | Verified as an **absence** across the full capture: no author line, no vote line, nothing after *"It is so ordered."* | **LOCKED (scoped to the capture)** — see the caution below |
| **C-04** | L258: ***"It is not a synonym for unanimous, and nobody should be told which Justices stood behind it, because the document does not say."*** | `⛔-10`. **The correction sentence survives v002 intact.** | **LOCKED** |
| **C-05** | No Justice of the Supreme Court of the United States is named anywhere in v002 | Mechanical sweep for `Roberts, Scalia, Thomas, Ginsburg, Breyer, Alito, Sotomayor, Kagan, Kennedy, unanimous, 9-0, dissent, concurr, majority opinion`: **two hits, neither a Justice.** | **LOCKED** |
| **C-06** | No vote appears | Mechanical: no digit-hyphen-digit vote pattern; the only counts in the film are of cases, papers, pages and holdings. | **LOCKED** |

### C-05, the two hits — recorded so nobody "corrects" them

- **L204 — "Perry against Thomas, 1987."** `Thomas` here is a **party name** (*Perry v. Thomas*, 482 U. S. 483), listed in the SCOTUS opinion's own string cite. It is not Justice Thomas. Any automated name scan will flag it; **it is correct as written.**
- **L274 — "Ketchum, Chief Justice."** This is the **Chief Justice of the Supreme Court of Appeals of West Virginia**, the author of Brown II, which is a signed opinion and not per curiam. Brown II's capture opens `KETCHUM, Chief Justice:`. **Naming him does not breach the per curiam lock**, which binds the SCOTUS opinion only. Removing him would delete the one authored voice in the film.

### Standing caution on C-03

`○-06` in the ledger is still open: *"do not assert 'no dissent' or 'decided without argument' until confirmed against the official U. S. Reports."* L258's wording — *"no separate writing **attached to the text**"* — is scoped to the document that was read, and is true of it. **If anyone strengthens it to "there was no dissent" or "the Court was unanimous", the row flips to NEEDS SOURCE and the second half of it flips to QUARANTINED under `⛔-10`.** Leave the sentence exactly as it stands.

---

## 5. §D — TWO RECORDED SOURCE AMBIGUITIES (and two smaller ones)

These are **deliberate editorial choices, already recorded in the contract's `notes`.** They are not errors and they must not be silently "corrected" by a later pass, a linter, or an assembly thread.

### D-01 — Section 15(c) versus 15(e)

| | |
|---|---|
| **The conflict** | The Brown II capture prints the subsection **both ways, inside the same paragraphs.** Counted mechanically over the opinion body (excluding the capture's own header note): **`15(c)` 8 times, `15(e)` 4 times.** `15(e)` at ¶20 (Brown's argument), ¶24 (the question the circuit court asked), ¶30 (second sentence: *"Section 15(e) of the Act explicitly prohibits…"*), and the **conclusion** — *"the circuit court's certified question whether Section 15(e) was preempted by the FAA"*. `15(c)` at ¶22 (Taylor's argument), ¶24 (Marchio's argument — **one sentence before the 15(e) in the same paragraph**), ¶30 (first sentence — **immediately before the 15(e) in the same paragraph**), ¶32 (the Syllabus Point 11 quotation), ¶34, **footnote 6 twice**, and footnote 10. |
| **Why 15(c) wins** | Footnote 6 is the only place the capture prints the **statutory citation and the statutory text together**: *"The disputed portion of the Nursing Home Act, Section 15(c) (W.Va.Code, 16-5C-15(c) [1997]) says: Any waiver by a resident or his or her legal representative of the right to commence an action under this section, whether oral or in writing, shall be null and void as contrary to public policy."* Footnote 10 repeats `W.Va.Code, 16-5C-15(c) [1997]`. `15(e)` never appears next to a code cite. **`c` and `e` are a classic OCR pair**; the capture's own header lists `"Section 15(e)" / "15(c)" inconsistency` among its known artefacts. |
| **What the script does** | Uses **15(c)** at L46, L92, L114, L292 — four occurrences, zero occurrences of 15(e). At L335 the disposition sentence avoids the subsection entirely (*"the Nursing Home Act's waiver ban is preempted"*), which is the safest possible handling of the one line where the capture prints `15(e)`. |
| **Verdict** | **LOCKED** — deliberate, recorded in `episode_spec.v001.json` `notes` ("The script uses 15(c)"), consistent across the film. |

### D-02 — Marchio's docket: 35636 versus 35635

| | |
|---|---|
| **The conflict** | Brown II's **disposition line** prints `Case No. 35636`. The capture's own header note records that the **Brown I docket for the same consolidated appeals** (CourtListener docket 2374406) reads **35635**, and that the CourtListener docket record for Brown II (65317693) lists `35494, 35546, 35635`. |
| **What the script does** | Follows **the disposition line: 35636** (L335). One occurrence. `35635` appears zero times. |
| **Verdict** | **LOCKED** — deliberate, recorded in the contract `notes` ("The script follows the disposition line (35636)"). |
| **Note for the telop** | If the dockets are ever put on screen rather than in the narration, they must be the same three numbers in the same order: **35494 / 35546 / 35636.** Do not reconcile against the CourtListener docket field; that is a second source and this pass did not read it. |

### D-03 — the circuit court's one-paragraph order (a smaller, unrecorded one — recording it now)

Brown II **footnote 7** reads: *"The circuit court determined plaintiff Brown was required to **arbitration** his claims 'after hearing argument of counsel, reviewing the respective briefs and the record[.]'"*

The script, **L50**, renders this as *"the court determined that Brown was required to **arbitrate** his claims after hearing argument of counsel, reviewing the respective briefs and the record."*

- The quoted matter the film presents as the order's own words — *"after hearing argument of counsel, reviewing the respective briefs and the record"* — is **verified verbatim** (14-token span).
- `arbitration` → `arbitrate` is a repair of an obvious source typo or OCR slip in the *unquoted* connective, and changes no meaning.
- **Verdict: LOCKED.** Recorded here so a later pass does not "restore" ungrammatical text, and so nobody mistakes the corrected word for part of the quotation.

### D-04 — normalisation applied by this audit only

The corruptions listed in §1.2 (`uneonscionability`, `Brown 7`, `Broitm I`, `*391record`, `Mar-met`, `PAA`, `eases`) were normalised **inside the matcher**, to stop them producing false mismatches. **They were not written back to the capture and must not be.** `episodes/_planning/measurements/EP65_brown_remand_RAW.md` stays as captured, artefacts and all — that is what makes it a capture. **Verdict: LOCKED (procedure).**

---

## 6. §E — THE REST OF THE FILM, CLAIM BY CLAIM

Only rows where the script asserts a fact are listed. Glosses, transitions and short-sentence beats carry no source claim and are not graded.

| ID | Line | Claim | Source | Verdict |
|---|---:|---|---|---|
| E-01 | 26 | Case name; decided by SCOTUS on February 21, 2012 | SCOTUS caption; MB-01 | LOCKED |
| E-02 | 28, 30, 74 | The opinion is five pages | Page markers 1–5 in the capture | LOCKED |
| E-03 | 38 | *"This litigation involves three negligence suits against nursing homes in West Virginia"*; suits brought by Brown, Taylor, Marchio | MB-04, MB-05 — verbatim, 12-token spans | LOCKED |
| E-04 | 40 | Brown and Taylor sued Marmet; Marchio sued a Clarksburg home with two names in the caption; she sued as executrix of the estate of Pauline Virginia Willett | Brown II ¶16; SCOTUS caption; MB-03, MB-18 | LOCKED |
| E-05 | 46 | August 25, 2009 — Circuit Court of Kanawha County dismissed Brown's suit; he had argued 15(c) and unconscionable adhesion; the court ruled he must arbitrate all his claims | Brown II ¶20 — 23-token span verified | LOCKED |
| E-06 | 48, 50 | That order is one paragraph long; its stated basis quoted | Brown II fn 7 — see D-03 | LOCKED |
| E-07 | 52 | September 29, 2009 — same court dismissed Taylor's suit against owners, operators and employees of the same home; same two arguments; must arbitrate all claims asserted | Brown II ¶22 — 13-token span verified | LOCKED |
| E-08 | 56 | June 2, 2010 — Circuit Court of Harrison County refused to dismiss or compel; certified the preemption question upward | Brown II ¶24 — 12-token span verified | LOCKED |
| E-09 | 64 | The whole factual recitation is two sentences, quoted | MB-07 (26 tokens), MB-08 (32 tokens) — both verbatim | LOCKED |
| E-10 | 68 | No ages, conditions, admission dates, death dates, description of care or of the alleged negligence; Willett is the only patient named, and only in a caption; Brown's and Taylor's patients unnamed | Verified as **absence** across the full SCOTUS capture; MB-19, `○-01` | LOCKED |
| E-11 | 72 | The signature is described twice in the same four words; the opinion never says which family member, never says the signer and the plaintiff are the same person, never gives either relationship | MB-10 — absence, verified by full read | LOCKED |
| E-12 | 78 | Brown's and Taylor's relevant parts identical; both contained a clause requiring arbitration of all disputes **other than claims to collect late payments owed by the patient** | MB-12 (16 tokens), MB-23 (20 tokens) — verbatim | LOCKED |
| E-13 | 82 | The filing-party-pays provision; *"The opinion states no dollar figure."* | MB-24 (18 tokens) + absence. `○-07` stays open and the film does not touch it | LOCKED |
| E-14 | 88 | Marchio's agreement required arbitration but made no exceptions and did not mention filing fees | MB-21 — verbatim | LOCKED |
| E-15 | 92 | Section 15(c) as it stood in 1997, quoted in full | Brown II fn 6 — 36-token span verified | LOCKED |
| E-16 | 96 | *"West Virginia's legislature had put that in the statute books **years before any of these three admissions**."* | Statute is `[1997]`; **admission dates are not in either capture** (`○-01`) | **NEEDS SOURCE** (NS-2) |
| E-17 | 104 | June 29, 2011 — the state court decided all three together, consolidating Brown's and Taylor's appeals with Marchio's, *"which was before the court on other issues"*; *"an extensive opinion with three holdings"* | MB-20; Brown II ¶28 | LOCKED |
| E-18 | 110, 114 | The state court held the FAA preempted its own legislature's waiver ban; the disfavoured-treatment rule and its application, both quoted | Brown II ¶32 — 46- and 45-token spans verified | LOCKED |
| E-19 | 116 | Nobody appealed that holding and the court later said so | Brown II ¶34 | LOCKED |
| E-20 | 118 | Syllabus Point 21, quoted in full | Brown II ¶38 — 42-token span verified | LOCKED |
| E-21 | 124 | The public-policy holding, quoted in full | MB-28 / Brown II ¶40 — 48-token span verified | LOCKED |
| E-22 | 128 | Third holding: two clauses unconscionable and unenforceable (Brown, Taylor); certified question answered for Marchio | Brown II ¶8 — 26-token span verified | LOCKED |
| E-23 | 132 | The admission-day passage: *"fraught with urgency, confusion, and stress"*; homes sign daily as a routine course of business; most patients do not view it as an interstate commercial transaction | Brown II ¶56 — three spans (24, 16, 16 tokens) verified | LOCKED |
| E-24 | 134 | *"One side of that desk does this every working day. **The other side does it once.**"* | First sentence rests on *"as a routine course of doing business"*. Second: Brown II says people *"do so only a few times in life"* | **NEEDS SOURCE** (NS-4) |
| E-25 | 136–144 | Unconscionability defined; "not hostile to arbitration… artifice to defraud"; adhesion contract defined; *Dunlap* beginning-point-not-the-end; the "comparison shop" finding, attributed to the state court | Brown II §III.A — spans of 28, 41, 41, 38, 30 tokens verified | LOCKED |
| E-26 | 146 | The *disingenuous* sentence, quoted in full | Brown II ¶56 — **51-token span, the longest in the film** | LOCKED |
| E-27 | 150, 152 | All three defendants sought review; two petitions docketed 11-391 and 11-394; defendants specifically challenged Syllabus Point 21 | SCOTUS caption; Brown II ¶10 | LOCKED |
| E-28 | 164, 166, 172 | *"tendentious"*, *"created from whole cloth"*, and the *"With tendentious reasoning…"* sentence in full; the panacea passage | MB-30; Brown II fn 14 (43 tokens), ¶36 (28 tokens) | LOCKED |
| E-29 | 168 | The 1925 adoption; FAA meant to reverse judicial hostility; designed for commercial entities enforced nationwide | Brown II ¶36 — spans of 12, 8, 18 tokens | LOCKED |
| E-30 | 176 | *"Congress did not intend for the FAA to be, in any way, applicable to personal injury or wrongful death suits that only collaterally derive…"* | MB-31 — 35-token span verified | LOCKED |
| E-31 | 182–212 | The SCOTUS spine: the opening rule; *"misreading and disregarding"*; the categorical-holding sentence; §2 quoted in full; *"The statute's text includes no exception…"*; *Byrd*; *Cocchi*; *Concepcion*; *"That rule resolves these cases."*; the categorical-rule application; *"both incorrect and inconsistent…"*; the Supremacy Clause sentence; *"must be vacated."* | MB-32…MB-43, MB-35, MB-34 — every one verified as a span (41, 22, 48, 17, 14, 11, 12, 24, 43, 23, 25, 12 tokens) | LOCKED |
| E-32 | 196 | *"a line from a per curiam the Court had issued **weeks earlier**"* | The capture cites *KPMG LLP v. Cocchi*, 565 U. S. ___ (2011) — **year only, no date** | **NEEDS SOURCE** (NS-1) |
| E-33 | 204 | The four preempted state rules, with years and parentheticals | MB-44 — parentheticals verified as spans; years from the capture's citations | LOCKED |
| E-34 | 220 | *"To vacate a judgment is to wipe it out and send the case back. It is not a ruling that the other side wins."* | Definitional gloss consistent with MB-34/MB-50/MB-53. No source claim beyond them | LOCKED |
| E-35 | 226 | *"Part Two is one page long."* | Part II opens partway down page 4 and ends on page 5. **An approximation, stated as scale not citation** | LOCKED (approximation, recorded) |
| E-36 | 228–236 | The alternative holding; the Marchio note; *"It is unclear, however, to what degree…"*; *"clearly violates public policy"* | MB-45, MB-46, MB-47, MB-48 — spans of 16, 18, 28, 12 tokens | LOCKED |
| E-37 | 238 | The remand instruction, quoted in full | MB-49 — 44-token span verified. **The line the film is built on** | LOCKED |
| E-38 | 246 | The disposition, quoted in full | MB-50 — 31-token span verified | LOCKED |
| E-39 | 248 | *"did not hold that any of these three arbitration clauses was valid… did not order anyone to arbitrate anything… did not decide whether these families could sue…"* | MB-53. **This is the sentence that discharges `⛔-01` and `forbidden_claims` row 1** | LOCKED |
| E-40 | 252 | Whether a relative's signature can bind the patient or the estate was raised in the litigation, is in the file, and is not mentioned in the five pages | Brown II fn 52 ¶2 (25- and 9-token spans); absence verified in the SCOTUS capture. `⛔-09` respected — the film asserts no answer | LOCKED |
| E-41 | 256 | The carve-out clause was before the Court and is quoted in its recitation of facts; *"**It was not the question presented.**"* | First two verified. The third describes the **cert petitions' questions presented**, which neither capture contains | **NEEDS SOURCE** (NS-3) |
| E-42 | 262 | April 3, 2012 order directing additional briefs and arguments; the court heard the cases again | Brown II ¶46 (7- and 8-token spans); *"At oral argument on the rehearing of this case"* ¶48 | LOCKED |
| E-43 | 264 | Both sides' rehearing arguments — plaintiffs on a right to discovery, Marmet on insufficient evidence in the record | Brown II ¶48 — spans of 6, 6, 6, 19 tokens | LOCKED |
| E-44 | 268 | Submitted June 6, 2012; *"The opinion came down seven days later."* | Capture header: `Submitted June 6, 2012` and `decided June 13, 2012`. **Arithmetic on two captured dates, both spoken in the film (L268, L274), and at 26:00 it is nowhere near the 92% line** | LOCKED |
| E-45 | 274 | June 13, 2012; *"Ketchum, Chief Justice, writing for the Supreme Court of Appeals of West Virginia, in the decision **the reports call Brown Two**"* | Author line and date verified. The opinion **names Brown I but never names itself** | **NEEDS SOURCE** (NS-5, cosmetic) |
| E-46 | 276–288 | *"we overrule Syllabus Point 21 of Brown I"*; *"We otherwise find that the Supreme Court's decision does not counsel us to alter our original analysis…"*; *"we otherwise reaffirm all of our discussion and holdings in Brown I"*; *"however, in light of the parties' additional briefs and arguments, we modify our conclusions in Brown I"*; **"Both sentences are in the same opinion."** | Brown II ¶12, ¶46, ¶48 — spans of 15, 26, 11, 16 tokens. **This is the R13(c) repair: the opinion's self-contradiction is now presented as a contradiction and left unresolved, with no annotation** | LOCKED |
| E-47 | 290–294 | SCOTUS discussed no other portion of Brown I; Syllabus Point 11 unchallenged and not revisited; the doctrine described as *"a general, state, common-law, contract-law principle that is not specific to arbitration, and does not implicate the FAA"* | Brown II ¶10, ¶34, ¶12 — spans of 13, 9, 13, 19, 9, 21 tokens | LOCKED |
| E-48 | 300 | *"The Supreme Court — without elucidating how and why the FAA applies to negligence actions that arise subsequently and only incidentally to a contract containing an arbitration clause — summarily concluded…"* | Brown II ¶42 — 31-token span verified | LOCKED |
| E-49 | 306, 308 | The sliding scale; substantive unconscionability as one-way arbitration with a choice of forums for the stronger party; *"a modicum of bilaterality"* | Brown II §III.A — spans of 13, 9, 28, 33, 11 tokens. **These two lines carry the film's recognition beat** | LOCKED |
| E-50 | 317, 319 | Brown's order *"devoid of any findings of fact or conclusions of law"*; Taylor's had some findings but no comprehensive analysis under the 2011 guidelines; nobody had been permitted to take evidence; *"greatly at sea without a chart or compass"* | Brown II ¶50 (25 tokens), fn 7 (16 tokens) | LOCKED |
| E-51 | 321 | *"claims of coercion, fraud, or unequal bargaining power … best left for resolution in specific cases"*; *"further development of the factual record by the parties is proper"* | Brown II ¶96 quoting *Gilmer* — spans of 16, 7, 11 tokens | LOCKED |
| E-52 | 327 | AAA would no longer administer individual-patient cases effective January 1, 2003; NAF would cease consumer arbitration as of Friday, July 24, 2009, under a settlement with the Minnesota Attorney General; the Marmet clause named the AAA Commercial Rules, the Clarksburg clause the NAF Code of Procedure | Brown II fn 52 ¶1 — spans of 14, 17, 13, 26 tokens | LOCKED |
| E-53 | 331, 333 | The authority argument, quoted; the court declined to consider both arguments, which should go to the trial court first | Brown II fn 52 ¶2 and closing line — spans of 7, 25, 9, 7, 9 tokens | LOCKED |
| E-54 | 337 | *"Nothing in that opinion holds these clauses unenforceable. It hands the question back to the circuit courts and stops."* | MB-53 logic applied to Brown II. **Discharges the mirror-image of `⛔-01` on the state side** | LOCKED |
| E-55 | 347–365 | The entire ENDING | **Restatement only.** §1.4 shows zero new numerals and zero new proper nouns | LOCKED |

### E-56 — one consistency note, not a defect

L90 says *"Three families. Two documents."* (two document **types** — Brown's and Taylor's being identical, Marchio's different). L357 says *"Three families sued. Three papers were produced."* (three physical agreements). Both are true and they are counting different things, but **an ear ten minutes apart can hear a contradiction.** No source problem; flagging it as a listening risk for the voice pass. If it grates on the read-aloud, L357 becomes *"Three families sued. Three papers were signed."* — the count is not the point of that sentence.

---

## 7. NEEDS SOURCE register

Five rows. **None is load-bearing.** Each has a repair that stays inside the two captures, so the film can be locked today without waiting on a third source.

| ID | Line | The claim | What is missing | Repair that needs no new source |
|---|---:|---|---|---|
| **NS-1** | 196 | *"a line from a per curiam the Court had issued **weeks earlier**"* (*KPMG LLP v. Cocchi*) | The capture prints the citation as *KPMG LLP v. Cocchi*, 565 U. S. ___ (2011) (per curiam) (slip op., at 3) — **year only, no decision date.** The interval between it and February 21, 2012 is therefore unverifiable from either capture, in either direction | → *"a line from a per curiam the Court had issued the term before, itself quoting a case from 1985."* Or simply drop the interval: *"a line from another per curiam, itself quoting a case from 1985."* |
| **NS-2** | 96 | *"years before any of these three admissions"* | The statute is `[1997]`. **No admission date is in either capture** (`○-01`). An admission in 1998 would make "years" false. The film elsewhere makes a virtue of not knowing these dates (L68: *"No dates of admission"*) — this line quietly assumes them | → *"West Virginia's legislature had put that in the statute books in 1997."* Stop there. The next sentence already carries the weight |
| **NS-3** | 256 | *"It was not the question presented."* | "The question presented" is the cert petition's QP. **Neither capture contains the petitions.** What *is* captured is Brown II ¶10: *"The defendants specifically challenged Syllabus Point 21 of our opinion"* | → *"It was not what the defendants had challenged."* Same beat, and the film already said it at L152 |
| **NS-4** | 134 | *"The other side does it once."* | Brown II says people *"seek medical care in a nursing home for long-term treatment to heal, and do so **only a few times in life**."* "Once" is tighter than the source. (The film bible's §19 R8(c) proposed this short form to cut *"in the worst week of a family's life"* — it fixed the invented pathos and tightened the count in the same edit) | → *"The other side does it once or twice in a life."* Or attribute: *"The other side, the state court wrote, does it only a few times in a life."* Owner call: the three-word version is the better line and the overstatement is small |
| **NS-5** | 274 | *"the decision **the reports call Brown Two**"* | Brown II names *Brown I* but **never names itself.** The only place "Brown II" appears is the header note of our own capture, which is a research note, not a report | → *"in the decision that answers Brown One."* Cosmetic; the shorthand is almost certainly standard, but this pass did not read a document that uses it |

---

## 8. QUARANTINE — v001 material the second pass removed, recorded so it cannot come back

| ID | v001 line | Text | Why |
|---|---:|---|---|
| **Q-01** | 368 | *"Both had been handed to a circuit judge in Kanawha County and a circuit judge in Harrison County, with instructions to take evidence this time."* | Four faults — §3.2 D-1…D-4. **The single worst factual defect in v001** |
| **Q-02** | 364 | *"Just under three years of litigation, from the first dismissal in August 2009 to the last opinion in June 2012…"* | A **newly computed figure introduced past the 92% line.** Arithmetically right, structurally forbidden. Deleted, not relocated |
| **Q-03** | 362 | *"…in the hands of two circuit courts that had never taken a day of evidence on it."* | Applies to both open questions what Brown II said only of Brown and Taylor. Same defect family as Q-01 |
| **Q-04** | 374 | *"The nursing home kept a courthouse for the only claim it was **ever likely to file**."* | A prediction about future filings. **Not in the record**, and it made the film's last sentence a moral verdict on a party |
| **Q-05** | 138 | *"…in the worst week of a family's life."* | Invented experience. The record describes the paper, never the day |
| **Q-06** | 23 | *"A judge in Kanawha County **read the agreement** and dismissed the case."* | Not in the record — and Brown II fn 7 and ¶50 say the opposite, that the order was devoid of findings. The film would have contradicted its own opening |
| **Q-07** | 74 | *"That absence is **not an oversight**, and this film is not going to fill it."* | Asserts why the opinion is short. Unknowable from the document |
| **Q-08** | — | **Robin Sutphin** (Marmet's manager) and **Canoe Hollow Properties, LLC**, both named in Brown II ¶20 and fn 7 | Available in the source and **forbidden by the contract** (`forbidden_subjects`: *any named or characterised member of staff at Marmet or Clarksburg*) and `⛔-08`. **Verified absent from v002.** Do not add them in a later pass because "the source has them" |

Every one is **verified absent from v002**: the strings `worst week`, `read the agreement`, `not an oversight`, `ever likely to file`, `this time`, `Sutphin`, `Canoe`, `three years` return zero matches.

---

## 9. Totals

| Verdict | Count |
|---|---:|
| **LOCKED** | **72** — §A 6, §B 6, §C 6, §D 4, §E 50 |
| **NEEDS SOURCE** | **5** — NS-1…NS-5 |
| **QUARANTINED** | **8** — Q-01…Q-08, all v001, all verified absent from v002 |
| Total graded rows | 85 |

§E carries 55 rows (E-01…E-55) of which 5 are NEEDS SOURCE. E-56 is a listening note, not a graded claim.

**Mechanical figures for the receipt**

| Measure | Value |
|---|---|
| Narration words | 5,201 (band [5100, 5600] — inside, 101 words of headroom at the floor) |
| Narration lines / tokens audited | 146 / 5,258 |
| Corpus tokens (SCOTUS + Brown II) | 7,850 |
| Verbatim spans ≥ 6 tokens | **130** (≥7: 120 — the second pass reported 123) |
| Narration carried by verified quotation | **42.9%** (2,257 tokens) |
| Unmatched runs ≥ 10 tokens | 116 — 111 narrator prose, 5 escalated to NS-1…NS-5 |
| Modelled runtime / 92% line | 29:32 / 27:11 |
| Last new fact | L335, closes **27:03** — 8 s inside the line |
| New numerals or proper nouns in ENDING | **0** |
| Justices named | **0** (two false positives explained at C-05) |
| Votes reported | **0** |

## 10. What must not change without re-running this pass

1. **L317 and L323 stay adjacent and in order** — that adjacency is what scopes *"these cases"* to Brown and Taylor (§3.3).
2. **L258 keeps its exact wording**, including *"It is not a synonym for unanimous"* (§4, C-04) and the scoping phrase *"attached to the text"* (C-03).
3. **15(c) stays 15(c); 35636 stays 35636** (§5, D-01/D-02).
4. **Ketchum and "Perry against Thomas" stay** (§4, C-05).
5. **The ENDING acquires no number, no date and no proper noun** (§1.4).
6. If the script is revised at all, `mandatory_stills` must be **re-derived**, per the contract's explicit `notes` instruction.
