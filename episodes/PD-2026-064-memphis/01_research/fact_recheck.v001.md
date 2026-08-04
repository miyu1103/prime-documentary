# PD-2026-064-memphis — Fact + Quotation Re-check v001 (R2/R3)

- **Episode:** `PD-2026-064-memphis` — *Memphis Light, Gas & Water Division v. Craft*, 436 U. S. 1 (1978)
- **Re-check date:** 2026-08-04 JST
- **Target:** `episodes/_planning/EP64_memphis_script.en.v002.md` (429 lines)
- **Primary source, and the only one:** `episodes/_planning/measurements/EP64_memphis_RAW.md`
  (62,075 chars — CourtListener cluster 109855; Powell majority id 9427172, Stevens dissent id 9427173; filed 1978-05-01)
- **Ledger:** `episodes/_planning/EP64_memphis_FACTS_LEDGER.v001.md` (122 rows, 109 ✓ VERBATIM, 12 quarantine, 6 recorded self-contradictions)
- **Contract:** `episodes/PD-2026-064-memphis/episode_spec.v001.json`
- **Status:** **PASS with one NEEDS SOURCE.** No QUARANTINED string survives in v002.

> **This pass did not start from zero.** The second pass of the script removed three record-fills — one of
> them a §15 disqualifier — and its audit corrected three quotation divergences. §2 records each of those
> as resolved, with the current v002 wording and a mechanical absence check on the retired string. §3 then
> re-extracts **every remaining quotation in the script** and matches it against the RAW opinion.

---

## 0. Method, and the one trap in the tooling

**Extraction is mechanical. Nothing below was hand-picked.**
`ep64_quote_extract.py` / `ep64_map_rows.py` (scratchpad) read the script line by line, strip headings,
`【】` directions and `⟨HELD⟩`, normalise both sides identically (NFKC; curly→straight quotes; em/en
dashes→space; `…`→space; page markers `*19` stripped **including ones glued to a word**; footnote markers
`[7]` stripped; editorial brackets removed so `[T]he` matches `The` and `[them]` matches `them`; `&`→`and`;
`33,000`→`33000`; spelled-out sums mapped to figures; lowercase; punctuation→space), then greedily segment
each line into **maximal runs that appear verbatim in the opinion**. Three verdict classes are computed,
not judged:

| Signal | What it means |
|---|---|
| **longest run ≥ 8 words** | the line is carrying a quotation → judged in §3 |
| **inner MISS of 1–4 words between two HITs of ≥ 4** | a word of the writer's may be sitting inside a sentence of the court's (**ALTERED**) |
| **two adjacent HITs of ≥ 5 with no MISS between** | an internal deletion inside one court sentence (**SPLICE**) |

**Every match is word-boundary, never bare substring.** This is not a preference; it is the defect the
contract already recorded:

> `episode_spec.v001.json` → *"LEDGER/GATE DEFECT recorded 2026-08-04: check_script_craft matches
> quarantined claims as BARE SUBSTRINGS, so two rows in this episode's ledger fire on innocent text.
> Quarantine row -03's string `off for three days` matches inside the ordinary word cut-off, and row -08's
> quoted employee line makes `you have to pay on the other` unusable even when correctly attributed."*

Demonstrated both ways before it was relied on (CLAUDE.md §4.6: *a check that has never been shown to fail
is decoration*):

| Probe | Host string | bare substring | **word boundary** |
|---|---|---|---|
| `off for three days` | `the electric service cutoff for three days` | **fires (false positive)** | does not fire ✔ |
| `off for three days` | `the power was cut off for three days` | fires | **fires ✔ (true positive preserved)** |
| `you have to pay on the other` | `she had to pay on the other bill as well` | does not fire | does not fire ✔ |
| `you have to pay on the other` | `an employee said you have to pay on the other bill` | fires | **fires ✔** |

The word-boundary matcher still catches the real thing. It stops the ledger's two rows firing on innocent
hosts. **In v002 both quarantine strings return 0 hits under both matchers** — the script already works
around them (indirect speech at L91 and L373; `cutoffs for three days` at L141, which never contains the
quarantined string at all).

---

## 1. The three things this episode can get wrong

### 1.A — The record contradicts itself, and the Court never resolved it

Two collisions, both inside one document, both recorded by the ledger at **ML-117** and **ML-118**.
The contract's `notes` bind the script: *"the Court never resolved either, so the script may not pick a side."*

#### 1.A.1 Whose mistake the double billing was

| | |
|---|---|
| **Script, L61** | *"And then the sentence the first half of this case turns on. Because the contractor did not consolidate the meters properly, a condition of which the Crafts were not aware, they continued to receive two bills until January 1974."* |
| **Script, L63** | *"That is the majority's account. The Crafts hired somebody and their man got it wrong."* |
| **Ledger row** | **ML-22** |
| **Opinion (Part I), verbatim** | *"Because the contractor did not consolidate the meters properly, a condition of which the Crafts were not aware, they continued to receive two bills until January 1974."* |
| **Verdict** | **LOCKED** — 27-word verbatim run; explicitly labelled "the majority's account" one line later |

| | |
|---|---|
| **Script, L65** | *"In a footnote, the Court quotes the brief filed by the Crafts' own lawyers."* |
| **Script, L67** | *"Not until after the action was filed were the Crafts able to discover that they continued to receive double computer billings because MLG&W failed to combine the two accounts properly."* |
| **Ledger row** | **ML-30** |
| **Opinion (n. 7, quoting Brief for Respondents 5), verbatim** | *"Not until after the action was filed were the Crafts able to discover that they continued to receive double computer billings because MLG&W failed to combine the two accounts properly…, or that, as a result of the double computer billings, MLG&W had overcharged them for gas service and city service fees."* |
| **Verdict** | **LOCKED** — 32-word verbatim run; attributed twice (*"In a footnote, the Court quotes the brief filed by the Crafts' own lawyers"*), and the script **stops before the "had overcharged them" clause**, which is the ⛔-02 tripwire |

**Does the script adopt either? No.**

> **L69** — *"Set the two side by side. The body of the opinion says a contractor the Crafts hired failed to merge the meters. The footnote says the utility failed to merge the accounts."*
> **L71** — *"The record does not agree with itself about whose mistake this was. The Court never resolves it."*
> **ENDING, L409** — *"The record never settled who put it there. The majority says a contractor the Crafts hired. A footnote quoting their own brief says the utility. Both sentences are printed in the same opinion."*

L71 is a **description of the record**, not a finding by the film. The v001 line ended
*"…Neither will this film."* — a meta-utterance about the film's own method — and it is gone (§2, RF-4).
**Verdict: LOCKED. Neither account adopted, at any of the three places the collision appears.**

#### 1.A.2 How many terminations there were

| | |
|---|---|
| **Script, L75** | *"During this period, the Crafts' utility service was terminated five times for nonpayment."* |
| **Script, L77** | *"During this period. That phrase is the Court's, and it is as precise as the opinion ever becomes. No month for any of the five. No duration. No season. No figure for any bill behind them."* |
| **Ledger row** | **ML-23** / collision at **ML-118** |
| **Opinion (Part I), verbatim** | *"During this period, the Crafts' utility service was terminated five times for nonpayment."* |
| **Script, L363** | *"…because the Crafts refused to pay the balance on the second account, the Division terminated their service on several occasions. The District Court expressly found that the Division sent a final notice before each termination."* (introduced at L361: *"And his account of the dispute itself reverses the majority's."*) |
| **Ledger row** | **ML-99** (DISSENT) |
| **Opinion (Stevens, J., dissenting), verbatim** | *"The Crafts, believing they were being billed twice for the same utilities, did not pay on the second account. In fact, the two accounts were independent; because the Crafts refused to pay the balance on the second account, the Division terminated their service on several occasions. The District Court expressly found that the Division sent a final notice before each termination."* |
| **Script, L365** | *"Five times, said the majority. Several occasions, said the dissent."* |
| **Verdict** | **LOCKED** |

Mechanical confirmation: `five times` occurs in v002 **exactly once** (L75), inside the Court's own
sentence, and the very next spoken line attributes the phrasing to the Court. `several occasions` occurs
twice — once as ML-25 (Mrs. Craft going downtown, majority) and once as ML-99 (dissent) — and L365 stages
the two counts against each other without choosing. **Neither number is ever the film's own.**

---

### 1.B — Nobody ever decided whether the Crafts owed the money

This is the ledger's own nomination for *"the single most likely factual failure in the episode"* (⛔-02),
and the contract repeats it: *"NOBODY EVER DECIDED WHETHER THE CRAFTS OWED THE MONEY, so 'they were
overcharged' is not available."*

**What the script says, and it is a negative:**

| Script line | Wording | Ledger | Verdict |
|---|---|---|---|
| **L209** | *"That credit was never a finding that anybody had been billed too much."* | ML-52, ML-119 | **LOCKED** — a denial, not an assertion |
| **L211** | *"The trial court's own words were that of the balance claimed by MLG&W in March, 1974, some involved **possible** gas overcharges and double or duplicate billings with respect to city service fees."* | **ML-52** · opinion n. 8, quoting Pet. for Cert. 39, verbatim: *"[o]f the balance claimed by MLG&W in March, 1974, some involved possible gas overcharges and double or duplicate billings with respect to city service fees."* | **LOCKED** — the word *possible* is retained, which the ledger requires |
| **L213** | *"Possible. In a document this careful, that word is load-bearing."* | ML-52 | **LOCKED** |
| **L219** | *"Nobody ever decided whether the Crafts owed the money. Not the trial court. Not the court of appeals. Not the Supreme Court."* | ML-86, ML-119 | **LOCKED** |
| **L223** | *"The validity of the damages claim is a matter for initial determination by the courts below."* | **ML-86** · opinion n. 8, verbatim | **LOCKED** — 16-word run |
| **L225** | *"What each side said is on the record. Which side was right is not."* | ML-119 | **LOCKED** |
| **L411** | *"Nor did anyone settle the money. Possible gas overcharges, said the trial court. Genuinely independent accounts, said the dissent. The Supreme Court expressed no opinion and sent the question back down."* | ML-52 / ML-99 / ML-86 | **LOCKED** — both sides attributed in one breath |

**Every appearance of the word, mechanically.** `\bovercharg\w*` returns **five** hits in the spoken body
of v002 (a sixth is in the non-spoken `**Locks:**` header at L9, which reads *"no one overcharged"*).
Each of the five sits inside an attributed quotation, and **none of them is about the Crafts**:

| Line | The sentence | Whose words | About whom |
|---|---|---|---|
| **L211** | *"…some involved **possible gas overcharges** and double or duplicate billings…"* | the **trial court**, quoted (L209 names it: *"The trial court's own words were…"*) | the March 1974 balance — and only *possibly* |
| **L255** | *"If the public utility discontinues service for nonpayment of a disputed amount it does so at its peril and if the public utility was wrong, for example if the customer **was overcharged**, it is liable for damages."* | **Tennessee law**, quoted through the Court from *Trigg* (L253/L255 introduce it: *"the answer was in Tennessee… The same decision put the risk of error on the utility"*) — ML-59 | a hypothetical customer, in a rule of state law |
| **L287** | *"…an opportunity for the presentation to a designated employee of a customer's complaint that he is being **overcharged** or charged for services not rendered."* | the **Supreme Court's holding**, ML-70, verbatim | a generic customer, in the holding |
| **L399** | *"It is an unfortunate fact that when the State assesses taxes or operates a utility, it occasionally **overcharges** the citizen."* | **Stevens, J., dissenting**, ML-111, verbatim (L353 established the byline; L397 re-introduces *"he named what he thought the Court was really doing"*) | the citizen, in general |
| **L411** | *"Possible gas **overcharges**, said the trial court."* | the **trial court**, attributed inline | the balance, *possible* |

**Verdict: LOCKED. No line in the script asserts that the Crafts were overcharged.** The nearest thing to
one — the respondents' brief saying MLG&W *"had overcharged them for gas service and city service fees"*
— is present in the ledger at ML-30 and is **deliberately cut off** in the script at L67.

---

### 1.C — The utility kept the power to cut service after a hearing

| | |
|---|---|
| **Script, L327** (ACT_5, opening line, followed by `⟨HELD⟩`) | *"And petitioners would retain the option to terminate service after affording this opportunity and concluding that the amount billed was justly due."* |
| **Ledger row** | **ML-76** — *"The limit that the film must not omit"* |
| **Opinion (Part IV-B, 436 U. S. at 18–19), verbatim** | *"And petitioners would retain the option to terminate *19 service after affording this opportunity and concluding that the amount billed was justly due."* (the `*19` is the U. S. Reports page break) |
| **Match** | **22-word verbatim run, exact.** `after affording` occurs **once** in the entire opinion, in this sentence. |
| **Verdict** | **LOCKED** |

Reinforced, without the narrator asserting it, at:

- **L329** — *"Retain the option to terminate. After affording the opportunity. After concluding the amount was justly due."*
- **L331** — *"The meter reader stays. The four-day final notice stays. The thirty-day clock stays. What is added is three items on the page, and a designated employee obliged to hear the answer before the clock runs out."*
- **L415** — *"After that, the meter reader may still arrive. The Court said so in the same breath."*

Mechanically, the ⛔-04 / ⛔-06 failure mode is absent: `\bmust now\b`, `\bcannot cut\b`, `\bcan no longer\b`,
`\bnever (be )?cut off\b` → **0 hits**; `struck down`, `overturned`, `reversed the` → **0 hits**
(the disposition is stated as *"The judgment of the Court of Appeals is affirmed."*, L319, ML-84).

#### 1.C.1 — CORRECTED DEFECT: a paraphrase that was printed as the Court's words

**This one is recorded so it cannot come back.**

| | |
|---|---|
| **The defective string** | *"…would retain the option to terminate service after affording **the notice and hearing required**."* |
| **Where it lived** | an **earlier revision of `episode_spec.v001.json`'s `notes`**, inside quotation marks, as if verbatim. It then propagated to `SHORTS_SLATE_EP62-65.v001.md` L292 (`short267`), the "mandatory final content beat" of that short. |
| **Status in the opinion** | **NOT PRESENT.** `"the notice and hearing required"` → **0 occurrences** in `EP64_memphis_RAW.md`. `notice and hearing` occurs **exactly once** in the whole document, in majority n. 15, in a different sentence about a different thing: *"…would erect an artificial barrier between the notice and hearing components of the constitutional guarantee of due process."* |
| **What it replaced** | nine words of the Court's (*"this opportunity and concluding that the amount billed was justly due"*) with six of the writer's |
| **How it got in** | the contract records it: *"it was a paraphrase carried over from a chat summary and written here as verbatim. **Never quote from a summary.**"* |
| **Independent audit** | `SHORTS_SLATE_EP62-65_QUOTE_AUDIT.v001.md` §3.1 — verdict **ALTERED**, ranked #1 in its order of application |
| **Status now** | the contract's `notes` carry the corrected ML-76 text with an explicit "checked against measurements/EP64_memphis_RAW.md on 2026-08-04" |
| **Status in the script** | `the notice and hearing required` → **0 hits in v002**; `notice and hearing` → **0 hits in v002**. The defect never reached the script. |
| **Verdict** | **QUARANTINED — permanently.** Any future line quoting ML-76 is taken from the ledger row's string, never from a note, a summary, or a slate. |

**Still open, and owned by the shorts thread, not this file:** `short267` L292 in
`SHORTS_SLATE_EP62-65.v001.md` was audited but **the slate was not edited** (the audit says so in its own
header). The corrected text is in §3.1 of that audit, ready to apply.

---

## 2. Defects the second pass already resolved — do not re-litigate, do not let them back in

### 2.1 Three record-fills removed (§15 of `PD_SCREENPLAY_STANDARD.v001.md`, R14 of the FILM_BIBLE)

| # | v001 wording | Why it was disqualifying | v002 wording now | Absent from v002? |
|---|---|---|---|---|
| **RF-1** | **v001 L197: *"The judge was uncomfortable."*** | **The §15 immediate disqualifier.** The inner state of a **real, named judge**, asserted with nothing in the record behind it. What the record gives is conduct only: he wrote *"hope"* in quotation marks, suggested $35, recommended two changes, and ruled for the utility. | **L199–L201:** *"The judge then expressed a hope. His word, in quotation marks, in the opinion. He hoped that credit in the amount of thirty-five dollars be issued to reimburse the Crafts for duplicate and unnecessary charges made and expenses incurred by them with respect to terminations which should have been unnecessary had effectual relief been afforded them as requested."* / *"Terminations which should have been unnecessary. That is the trial judge, ruling for the utility."* | ✔ `The judge was uncomfortable` → 0 hits |
| **RF-2** | **v001 L97: *"Missed work. In an opinion this sparing, that detail survived for a reason."*** | An inference about the **Supreme Court's editorial intent**. The record never says why the detail survived. | **L81:** *"Missed work."* — two words, nothing added | ✔ `that detail survived for a reason` → 0 hits |
| **RF-3** | **v001 L27–L29 (HOOK): *"The seller had told them the second set was dead."* / *"It was running."*** | ML-18 and ML-21 are both true, but the HOOK's placement made the second set read as running **from the day they moved in**. The record puts the discovery **a year later** (moved in October 1972, ML-17; meter reader told them October 1973, ML-21). | The 8-second HOOK (L19) no longer makes the claim at all, and ACT_1 carries the record's own sequence: **L45** *"The Crafts assumed, on the basis of information from the seller, that the second set of meters was inoperative."* → **L47** *"The assumption held for a year."* → **L57** *"October 1973. After learning from a MLG&W meter reader that both sets of meters were running in their home…"* | ✔ standalone `It was running.` → 0 hits |

**Two more removed in the same pass, recorded here so they are not reintroduced as "improvements":**

| # | v001 wording | Why | Status |
|---|---|---|---|
| **RF-4** | v001 L87: *"…The Court never resolves it. **Neither will this film.**"* | the film narrating its own method; it tells the audience the unresolved record is a *policy*, and turns §1.A into a performance | ✔ `Neither will this film` → 0 hits (v002 stops at *"The Court never resolves it."*, L71) |
| **RF-5** | v001 L236: *"**The meters were fixed. The two bills were one bill.** Nobody was about to cut anything off."* | **adopts one side of ML-117 in the narrator's voice.** Whether the *meters* or the *accounts* were the thing put right is the collision itself; the opinion's word is `clarified`, and its subject is the problem, not the hardware | ✔ both sentences → 0 hits. **L239** now: *"Respondents no longer desire a hearing to resolve a continuing dispute over their bills, as the double-meter problem has been clarified during this litigation. Nor do respondents aver that there is a present threat of termination of service."* (ML-91, 38-word verbatim run) |

### 2.2 Three quotation divergences corrected

Found by diffing v001 → v002 and re-matching both against the RAW opinion. In each case the **v001** text
was a sentence the Court did not write; the **v002** text is a verbatim run confirmed in `EP64_memphis_RAW.md`.

| # | v001 | The opinion's wording | v002 (current) | Class |
|---|---|---|---|---|
| **QD-1** | *"The Court of Appeals **found** that there is no assurance that the Crafts were mailed the just mentioned flyer."* | *"The Court of Appeals **noted** that 'there is no assurance that the Crafts were mailed the just mentioned flyer,' ibid."* — 436 U. S. at 13, **ML-44** | **L161:** *"The Court of Appeals **noted** that there is no assurance that the Crafts were mailed the just mentioned flyer."* (19-word verbatim run) | **ALTERED** — a writer's verb inside a court sentence, and it upgrades an observation into a finding |
| **QD-2** | *"As judges we have experience in appraising the fairness of legal remedies, but we have no similar ability to balance the cost of scheduling thousands of billing conferences against the benefit of providing additional protection to **the occasional customer.**"* | *"As judges we have experience in appraising the fairness of legal remedies **and judicial proceedings**, but we have no similar ability to balance the cost … to the occasional customer **who may be unable to forestall an unjustified termination**."* — Stevens, J., dissenting, **ML-110** | **L397:** the full sentence, both clauses restored (**75-word verbatim run**) | **SPLICE ×2** — one internal deletion and one tail truncation in a single dissent sentence. The tail is the half that concedes the majority's premise; dropping it made the dissent sound more dismissive than it is (⛔-10) |
| **QD-3** | *"The reference to duplicate charges apparently concerns the two dollars and fifty cents per month city service fee **charged on each set of meters in the duplex.**"* | *"The reference to duplicate charges apparently concerns the $2.50 per month city service fee **which was** charged on each set of meters in the duplex **until after they were consolidated**."* — Stevens, J., dissenting, n. 5, **ML-120** | **L215:** *"…the two dollars and fifty cents per month city service fee which was charged on each set of meters in the duplex until after they were consolidated."* (48-word verbatim run) | **SPLICE + material truncation** — without *"until after they were consolidated"* the fee reads as still running, which is exactly the money question nobody decided (§1.B) |

**Five further elisions the second pass also restored** (each passed the elision-only rule and each still
changed what the viewer was told). Recorded so the restorations are not undone as "tightening":

| Script line | Restored in v002 | Ledger |
|---|---|---|
| **L185** | *"…to be posted **or otherwise available** for convenient inspection by customers"* | ML-15 |
| **L277** | *"**In essence,** recipients of a cutoff notice should be told where, during which hours of the day, and before whom disputed bills appropriately may be considered."* | ML-68 |
| **L299** | *"**The opportunity for** a meeting with a responsible employee empowered to resolve the dispute could be afforded well in advance of the scheduled date of termination."* | ML-75 |
| **L347** | *"**The resolution of a disputed bill normally presents** a limited factual issue susceptible of informal resolution."* | ML-88 |
| **L377 / L383** | *"The dissent advances its own reading of the record **in this case**…"* / *"But **the prior decisions of this Court make clear that** due process is flexible…"* | ML-116 / ML-115 |

### 2.3 Tone defects removed with them (FILM_BIBLE R8 — no villain)

`The courts are open`, `Sue us`, `who might listen`, `describing a complaints department as a rumour`,
`The remedy exists and it costs more than the wrong`, `The vagueness is deliberate`,
`There is the hinge of the whole case`, `A hearing before a shutoff is not the end of shutoffs`
→ **all 8 return 0 hits in v002.** None was a factual error; each put a judgement in the narrator's mouth
that the record does not make. The last one is the important one: v002 replaced the assertion with the
schedule (L331), so the audience draws the conclusion §1.C requires instead of being handed it.

---

## 3. Every remaining quotation, extracted mechanically and matched against the opinion

**98 lines** of v002 carry a run of **≥ 8 words verbatim in `EP64_memphis_RAW.md`**. All 98 are listed.
`verbatim run` = the longest contiguous word run confirmed in the opinion for that line (the greedy
segmenter reports the longest span; most lines match end-to-end and the number understates them where the
line joins narration to quotation).

**Divergence sweep across all 98:**
- **inner MISS (ALTERED): 1** — L133, addressed at §4.2. Not a quotation.
- **SPLICE: 4** — L91, L103, L177, L263. Every one lands on an ellipsis or a citation the source itself
  prints: `(MLG&W)[1]` at L103; `id., at 162-163, 176,` at L177; the opinion's own `. . .` inside ML-62 at
  L263; and at L91 the split falls exactly where the script converts the employee's direct speech into
  reported speech (§4.3). **None is a writer's word inside a court sentence.**

| script line | first words of the quoted passage (normalised) | verbatim run vs RAW | ledger row | verdict |
|---|---|---|---:|---|
| L37 | willie s and mary craft respondents here reside at 1019 alaska street in memph… | 14 w | `ML-16` | **LOCKED** |
| L43 | when the crafts moved into their residence in october 1972 they noticed that t… | 38 w | `ML-17` | **LOCKED** |
| L45 | the crafts assumed on the basis of information from the seller that the second… | 19 w | `ML-18` | **LOCKED** |
| L49 | in 1973 the crafts began receiving two bills their regular bill and a second b… | 32 w | `ML-19` | **LOCKED** |
| L55 | separate monthly bills were received for each set of meters with a city servic… | 19 w | `ML-20` | **LOCKED** |
| L57 | after learning from a mlg and w meter reader that both sets of meters were run… | 39 w | `ML-21` | **LOCKED** |
| L61 | because the contractor did not consolidate the meters properly a condition of … | 27 w | `ML-22` | **LOCKED** — §1.A.1 |
| L67 | not until after the action was filed were the crafts able to discover that the… | 32 w | `ML-30` | **LOCKED** — §1.A.1, cut before the "had overcharged them" clause |
| L75 | during this period the crafts utility service was terminated five times for no… | 13 w | `ML-23` | **LOCKED** — §1.A.2 |
| L79 | on several occasions mrs craft missed work and went to the mlg and w offices i… | 23 w | `ML-25` | **LOCKED** |
| L83 | as found by the district court mrs craft sought in good faith to determine the… | 39 w | `ML-26` | **LOCKED** |
| L87 | on one occasion when mrs craft was attempting to avert a utilities termination… | 69 w | `ML-27` | **LOCKED** — the longest single verbatim run in the script |
| L91 | an employee of uncertain authority told mrs craft apparently without explanati… | 15 w | `ML-28` | **LOCKED** — see §4.3 |
| L97 | in february 1974 the crafts and other mlg and w customers filed this action in… | 24 w | `ML-29` | **LOCKED** |
| L103 | is a division of the city of memphis which provides utility service it is dire… | 36 w | `ML-11/ML-12` | **LOCKED** |
| L107 | as a municipal utility mlg and w enjoys a statutory exemption from regulation … | 19 w | `ML-13` | **LOCKED** |
| L109 | petitioners have abandoned their contention that state action is not present i… | 14 w | `ML-08` | **LOCKED** |
| L111 | because a municipality or governmental unit standing in that capacity is not a… | 19 w | `ML-10` | **LOCKED** |
| L115 | the last day to pay the net amount would be approximately 20 days after the me… | 18 w | `ML-31` | **LOCKED** |
| L117 | approximately 24 days after the meters are read a final notice is mailed stati… | 34 w | `ML-32` | **LOCKED** |
| L121 | electric service is then terminated by the meter reader unless the customer as… | 32 w | `ML-33` | **LOCKED** |
| L123 | if there is no communication prior to termination the meter reader or servicem… | 26 w | `ML-33` | **LOCKED** — the clause v001 dropped; restored by FILM_BIBLE R6 |
| L127 | approximately five days after the electric service cutoff the remaining servic… | 27 w | `ML-34` | **LOCKED** |
| L131 | petitioners provide for at least a 30-day period between the mailing of the bi… | 20 w | `ML-35` | **LOCKED** |
| L133 | …payment is in the mail, shows a paid receipt, or… (narration around ML-33) | 10 w | `ML-33/ML-107` | **LOCKED** — the only machine-flagged inner variant; **§4.2** |
| L137 | during the six months from september 1973 through february 1974 there were 112… | 16 w | `ML-96` | **LOCKED** |
| L139 | the notices contain a prominent legend phone 523-0711 information center | 10 w | `ML-97` | **LOCKED** |
| L141 | calls to the listed phone number are answered by 30 or 40 division employees a… | 66 w | `ML-97` | **LOCKED** — `cutoffs for three days` complete, plural, with the limit |
| L145 | the final notice contained in mlg and w s bills simply stated that payment was… | 31 w | `ML-39` | **LOCKED** |
| L151 | if you are having difficulty paying your utility bill bring your bill to our n… | 19 w | `ML-42` | **LOCKED** |
| L153 | no mention was made of a procedure for the disposition of a disputed claim | 14 w | `ML-42` | **LOCKED** |
| L157 | if there is any dispute concerning the amount due bring your bill to the offic… | 15 w | `ML-43` | **LOCKED** |
| L159 | if there is any dispute concerning the amount due | 9 w | `ML-43` | **LOCKED** |
| L161 | the court of appeals noted that there is no assurance that the crafts were mai… | 19 w | `ML-44` | **LOCKED** — **QD-1 resolved** (`found` → `noted`) |
| L167 | if those counselors cannot satisfy the customer then the customer is referred … | 29 w | `ML-37` | **LOCKED** |
| L171 | …could pay one-half of a past due bill,. / the plaintiffs in this action were participants in the plan | 10 w | `ML-36` | **NEEDS SOURCE** — **§4.1** |
| L175 | william t mullen secretary-treasurer of mlg and w testified that the utility p… | 19 w | `ML-38` | **LOCKED** |
| L177 | and there is no indication in the record that a written account of such a proc… | 26 w | `ML-38` | **LOCKED** |
| L181 | mrs craft s case reveals that the opportunity to invoke that procedure if it e… | 26 w | `ML-38` | **LOCKED** |
| L185 | …posted or otherwise available for convenient inspection… / independent utility district as opposed to a utility division of a municipality | 12 w | `ML-15` | **LOCKED** — `or otherwise available` restored in v002 |
| L191 | after trial the district court refused to certify the plaintiffs class and ren… | 17 w | `ML-47` | **LOCKED** |
| L195 | of the individual plaintiffs was deprived of a due process opportunity to be h… | 32 w | `ML-48` | **LOCKED** |
| L199 | that credit in the amount of 35 be issued to reimburse the crafts for duplicat… | 41 w | `ML-49` | **LOCKED** — the script quotes **more** of the trial court than ML-49 does; all of it verbatim (§4.4) |
| L203 | that mlg and w in the future send a certified or registered mail notice of ter… | 48 w | `ML-50` | **LOCKED** |
| L205 | 1974 the court acknowledged that defendants had issued the recommended credit … | 33 w | `ML-51` | **LOCKED** |
| L211 | that of the balance claimed by mlg and w in march 1974 some involved possible … | 28 w | `ML-52` | **LOCKED** — §1.B, *possible* retained |
| L215 | but the amounts challenged by the crafts as the result of double billing were … | 48 w | `ML-120` | **LOCKED** — **QD-3 resolved** |
| L223 | the validity of the damages claim is a matter for initial determination by the… | 16 w | `ML-86` | **LOCKED** — §1.B |
| L227 | on appeal the court of appeals for the sixth circuit affirmed the district cou… | 36 w | `ML-53` | **LOCKED** |
| L231 | an established procedure for resolution of disputes or some specified avenue o… | 22 w | `ML-54` | **LOCKED** |
| L239 | respondents no longer desire a hearing to resolve a continuing dispute over th… | 38 w | `ML-91` | **LOCKED** — replaces RF-5 |
| L243 | respondents claim for actual and punitive damages arising from mlg and w s ter… | 24 w | `ML-90` | **LOCKED** |
| L251 | rises to the level of a legitimate claim of entitlement protected by the due p… | 16 w | `ML-57` | **LOCKED** |
| L253 | a company supplying electricity to the public has a right to cut off service t… | 34 w | `ML-58` | **LOCKED** |
| L255 | if the public utility discontinues service for nonpayment of a disputed amount… | 25 w | `ML-59` | **LOCKED** — §1.B, *Trigg*, hypothetical customer |
| L257 | all of the inhabitants of the city of its location alike without discriminatio… | 22 w | `ML-61` | **LOCKED** |
| L261 | because petitioners may terminate service only for cause respondents assert a … | 23 w | `ML-63` | **LOCKED** |
| L263 | the customer s right to continued service is conditioned upon payment of the c… | 16 w | `ML-62` | **LOCKED** |
| L269 | an elementary and fundamental requirement of due process in any proceeding whi… | 44 w | `ML-65` | **LOCKED** (*Mullane*, quoted through the Court) |
| L273 | petitioners notification procedure while adequate to apprise the crafts of the… | 36 w | `ML-66` | **LOCKED** |
| L275 | notice in a case of this kind does not comport with constitutional requirement… | 60 w | `ML-67` | **LOCKED** |
| L277 | in essence recipients of a cutoff notice should be told where during which hou… | 26 w | `ML-68` | **LOCKED** — `In essence,` restored in v002 |
| L283 | this court consistently has held that some kind of hearing is required at some… | 25 w | `ML-69` | **LOCKED** |
| L287 | we agree with the court of appeals that due process requires the provision of … | 39 w | `ML-70` | **LOCKED** — §1.B |
| L289 | designated personnel who were duly authorized to review disputed bills with co… | 18 w | `ML-45` | **LOCKED** |
| L291 | whether or not such a procedure may be available to other mlg and w customers … | 28 w | `ML-71` | **LOCKED** |
| L295 | utility service is a necessity of modern life indeed the discontinuance of wat… | 26 w | `ML-73` | **LOCKED** |
| L297 | the risk of an erroneous deprivation given the necessary reliance on computers… | 15 w | `ML-74` | **LOCKED** |
| L299 | nor should some kind of hearing prove burdensome the opportunity for a meeting… | 34 w | `ML-75` | **LOCKED** — `The opportunity for` restored in v002 |
| L301 | petitioners contend that the available common-law remedies of a pretermination… | 35 w | `ML-77` | **LOCKED** — ML-77 paraphrases; the script's fuller sentence is verbatim (§4.4) |
| L305 | although utility service may be restored ultimately the cessation of essential… | 21 w | `ML-78` | **LOCKED** |
| L307 | moreover the probability of error in utility cutoff decisions is not so insubs… | 23 w | `ML-79` | **LOCKED** |
| L309 | equitable remedies are particularly unsuited to the resolution of factual disp… | 26 w | `ML-80` | **LOCKED** |
| L313 | ignores the predicament confronting many individuals who lack the means to pay… | 39 w | `ML-82` | **LOCKED** |
| L317 | because of the failure to provide notice reasonably calculated to apprise resp… | 63 w | `ML-83` | **LOCKED** — the holding, in full |
| L319 | the judgment of the court of appeals is affirmed | 9 w | `ML-84` | **LOCKED** |
| **L327** | **and petitioners would retain the option to terminate service after affording t…** | **22 w** | **`ML-76`** | **LOCKED — §1.C, the limit sentence** |
| L343 | we do not decide whether or under what circumstances any of these additional p… | 17 w | `ML-87` | **LOCKED** |
| L345 | the public utility enjoys a broad discretion in the scheduling and structuring… | 32 w | `ML-88` | **LOCKED** |
| L347 | the resolution of a disputed bill normally presents a limited factual issue su… | 16 w | `ML-88` | **LOCKED** — subject restored in v002 |
| L349 | petitioners have moved to clarify and regularize their notice procedure and it… | 24 w | `ML-46` | **LOCKED** — followed at L351 by *"Possible. Not held."* (ML-89) |
| L357 | in my judgment the court s holding confuses and trivializes the principle that… | 30 w | `ML-93` | **LOCKED** |
| L359 | i have no quarrel with the court s conclusion that as a matter of tennessee la… | 40 w | `ML-94` | **LOCKED** |
| L363 | the crafts believing they were being billed twice for the same utilities did n… | 61 w | `ML-99` | **LOCKED** — §1.A.2 |
| L371 | she was successful in working out a deferred-payment arrangement but apparentl… | 52 w | `ML-100` | **LOCKED** |
| L373 | mrs craft testified on direct examination that after being cut off she went to… | 41 w | `— (gap)` | **LOCKED** against the opinion (dissent n. 7); **no ledger row carries it** — §4.4 |
| L377 | the dissent advances its own reading of the record in this case but offers no … | 22 w | `ML-116` | **LOCKED** — `in this case` restored in v002 |
| L379 | the division s procedures would not be unconstitutional even if we assumed tha… | 41 w | `ML-103` | **LOCKED** |
| L381 | for a homeowner surely need not be told how to complain about an error in a ut… | 83 w | `ML-104` | **LOCKED** |
| L383 | here however the notice is given to thousands of customers of various levels o… | 48 w | `ML-115` | **LOCKED** — lead-in restored in v002 |
| L385 | even accepting the court s predicate a notice which advises customers to call … | 67 w | `ML-105` | **LOCKED** |
| L389 | although the division s terminations number about 2000 each month the record d… | 42 w | `ML-107` | **LOCKED** |
| L391 | a potential loss of utility service sufficiently grievous to qualify as a cons… | 47 w | `ML-108` | **LOCKED** |
| L395 | the crafts dispute involved only a relatively small amount but they did obtain… | 21 w | `ML-122` | **LOCKED** |
| L397 | these justifications suggest that the court s new rule is the product of a pol… | 75 w | `ML-110` | **LOCKED** — **QD-2 resolved** |
| L399 | but if the state has given the citizen fair notice and afforded him procedural… | 62 w | `ML-111` | **LOCKED** |
| L413 | a designated employee empowered to review disputed bills and rectify error | 11 w | `ML-83/ML-70` | **LOCKED** |
| L419 | and explained that she had paid a bill | 8 w | `ML-27` | **LOCKED** — the ENDING callback |

**98 rows: 97 LOCKED, 1 NEEDS SOURCE, 0 QUARANTINED.**

---

## 4. Open items

### 4.1 — **NEEDS SOURCE · L171 · the extended payment plan is truncated, and the line is malformed**

| | |
|---|---|
| **Script, L171** | *"In March 1973 the utility began an extended payment plan, which the trial judge called a generous program. **Customers able to demonstrate financial hardship could pay one-half of a past due bill,.** The plaintiffs in this action were participants in the plan."* |
| **Ledger row** | **ML-36** |
| **Opinion (n. 4, quoting the District Court), verbatim** | *"This **generous program** allows customers able to demonstrate financial hardship to pay **only** one-half of a past due bill **with the balance to be paid in equal installments over the next three bills**. The plaintiffs in this action were participants in the plan."* |
| **Two problems** | (a) **a stray `,.`** — a comma and a full stop with nothing between them, which will be read aloud as a break and will land in the caption file; (b) the sentence stops at *"one-half of a past due bill"*, dropping **the balance clause**. As spoken, the plan sounds like half the debt was waived. It was not: the other half was due in three instalments **on top of current charges** — which is precisely the point the majority makes at ML-82 (L313), *"the customer must make immediate payment of one-half of a disputed past due bill"*. The truncation quietly undercuts the film's own ACT_4 beat. |
| **Verdict** | **NEEDS SOURCE** — the line as written is not supported as a complete statement of the plan. |
| **Fix (ML-36, verbatim, ready to paste)** | *"In March 1973 the utility began an extended payment plan, which the trial judge called a generous program. It allowed customers able to demonstrate financial hardship to pay only one-half of a past due bill, with the balance to be paid in equal installments over the next three bills. The plaintiffs in this action were participants in the plan."* |
| **Blocking?** | **Yes for `script_verified`.** It is a one-line edit and changes no timing of consequence (+18 words). |

### 4.2 — Advisory · L133 · the single machine-flagged inner variant

| | |
|---|---|
| **Script, L133** | *"Thirty days of warnings, and one man at the end of them who is instructed to stop if the customer says payment is in the mail, shows a paid receipt, or **says there is illness in the house**."* |
| **Opinion (n. 4, step iii), ML-33** | *"Electric service is then terminated by the meter reader, unless the customer assures him that payment is in the mail, shows a paid receipt, or **explains that nonpayment was due to illness**."* |
| **Also in the record** | Stevens, J., dissenting, ML-107: *"The District Court found that the Division does not discontinue service when there is **illness in a home**."* |
| **Why it fires** | greedy segmentation reports a one-word inner MISS (`says`). |
| **Why it is not a defect** | this line is **the narrator's summary sentence**, not a quotation: it is the FILM_BIBLE's own commissioned replacement (R8-3) for v001's *"one man at the end of them who might listen"*, written to stop the meter reader reading as a man exercising discretion. The full ML-33 wording is quoted **verbatim two lines earlier at L121** (32-word run), so the audience has already heard the Court's version. |
| **Verdict** | **LOCKED** |
| **Advisory for the VO/caption pass** | *"illness in the house"* is the **dissent's** register (ML-107) attached to the **majority's** step (iii). Both are in the record and neither is contradicted, but ⛔-10 requires attribution every time the two accounts are mixed. If a cheap tightening is wanted, *"or says nonpayment was due to illness"* removes the mix at no cost. |

### 4.3 — Advisory · L91 / L373 · the employee's sentence, deliberately reported rather than quoted

The one line of individual speech in the record is ⛔-08 / quarantine row -08 territory, and both opinions
describe the same exchange in opposite terms. The script renders it as **reported speech on both
appearances**, which is why the SPLICE sweep flags the join:

- **L91 (majority):** *"An employee of uncertain authority told Mrs. Craft, apparently without explanation
  or attempt at investigation, that she had to pay on the other bill as well."* — ML-28. The Court's
  original is *"…'[w]ell, you have to pay on the other' bill."*
- **L373 (dissent):** *"Mrs. Craft testified on direct examination that after being cut off she went to the
  Division's office with the record of her payments on one account. She was told that she had to pay on the
  other account as well. In other words, an official of the Division did resolve the Crafts' dispute,
  correctly as it turned out."* — dissent n. 7 (41-word verbatim run).
- **L375:** *"Same sentence. Same office. One reading calls it a brush-off. The other calls it the answer."*

**Verdict: LOCKED.** The change from direct to reported speech is the documented workaround for the
bare-substring gate (§0) and does not alter what was said; the two readings are staged and neither is
adopted (⛔-10).

### 4.4 — Ledger amendments (not script defects — the script is verified against the opinion)

Three lines quote the opinion correctly but **quote more of it than any ledger row carries**. Invariant 1
is satisfied (the primary source supports every word, checked this pass), but the ledger should be the
place a future writer looks:

| Script line | What is verbatim in the opinion but not in a ledger row | Proposed row |
|---|---|---|
| **L199** | *"…that credit in the amount of $35 be issued to reimburse the Crafts for…"* — ML-49 begins only at *"duplicate and unnecessary charges"* | extend **ML-49** |
| **L301** | *"Petitioners contend that the available common-law remedies of a pretermination injunction, a post-termination suit for damages, and post-payment action for a refund are sufficient to cure any perceived inadequacy in MLG&W's procedures."* — ML-77 paraphrases this and quotes only *"was advanced only obliquely in the Court of Appeals"* | extend **ML-77** |
| **L373** | *"Moreover, Mrs. Craft testified on direct examination that after being cut off she went to the Division's office with the record of her payments on one account. She was told that she had to pay on the other account as well."* — dissent n. 7. **No ledger row carries it**; ML-102 begins at *"It is worth remembering…"* | **add ML-123** (DISSENT), and record it in §12 as part of the ML-121 collision |

### 4.5 — Outside this file's scope

- **`SHORTS_SLATE_EP62-65.v001.md` is unedited.** Its audit found 5 quotation defects and 9 claim defects,
  two of them in this episode's shorts (`short267` §3.1 ML-76, §3.2 ML-97; `short266` §3.3 cover;
  `short265` §6.4). §1.C.1 above is the same defect. Applying them belongs to the shorts thread.
- **⛔-08 is still an OWNER CALL.** The ledger asks whether the Crafts' real names are spoken at all. The
  script speaks them (L37, L49). The shorts slate also puts `WILLIE C.` / `WILLIE S.` on screen without a
  recorded owner decision (audit §8). **Raise before build.** This file does not decide it.
- **○-01 and ○-04 remain open** and the script obeys both: no aftermath for the family, no present-day rule.

---

## 5. Quarantine sweep — all twelve rows, word-boundary matched against v002

| Row | Probe | Hits | Verdict |
|---|---|---:|---|
| ⛔-01 | vote count (`6-3`, `5-4`, "the vote", Justices joining Powell) | 0 in the spoken body | **CLEAR** — L27 says only *"Justice Powell wrote for the Court"* and *"Three Justices dissented"* |
| ⛔-02 | the Crafts overcharged / MLG&W wrong / they did not owe it | 0 unattributed; 5 attributed appearances, all analysed at §1.B | **CLEAR** |
| ⛔-03 | `off for three days` · `cut off in the middle of winter` · `over a $200 bill` · any season/date/duration/sum for the five | **0 under both bare and word-boundary matching.** `\bwinter\b` → 0. `for N days` → 2 hits, both the dissent's three-day telephone stay (ML-97, L141/L143), neither an outage | **CLEAR** — and the contract's THREAT line (「冬に」) never reached the script |
| ⛔-04 | "the Court ordered a hearing before every shutoff" / "utilities must now hold hearings" | 0 (`must now`, `cannot cut`, `can no longer` → 0) | **CLEAR** — §1.C |
| ⛔-05 | any ending for the family | 0 | **CLEAR** |
| ⛔-06 | "a constitutional right to electricity" | 0 | **CLEAR** — L263 carries the conditional (ML-62) |
| ⛔-07 | private/investor-owned utility, a modern bill | 0. `\btoday\b`/`nowadays`/`currently`/`present-day` → 0. The single `modern` is inside ML-73 verbatim (*"a necessity of modern life"*, L295) | **CLEAR** |
| ⛔-08 | generated likeness of the Crafts / 1019 Alaska Street / a named employee | n/a to the script text; the address and names **are spoken** (L37, L49) | **OWNER CALL — §4.5** |
| ⛔-09 | any national statistic, the 16 % figure | 0 (`nationwide`, `across the country`, `16 %`, `sixteen percent` → 0) | **CLEAR** |
| ⛔-10 | dissent's facts as the record / majority's as uncontested | every collision attributed at L61+L63, L65, L363, L365, L373, L375, L411 | **CLEAR** — one advisory at §4.2 |
| ⛔-11 | "reversed" / "struck down" / "enjoined" | 0 | **CLEAR** — L319 *"The judgment of the Court of Appeals is affirmed."* |
| ⛔-12 | calling it a class action / "changed the rules for all Memphis customers" | 1 hit, L227: *"…affirmed the District Court's **refusal to certify a class action**…"* (ML-53, verbatim) followed at L229 by *"The class stayed dead. Everything after it is a judgment about two people at one address."* | **CLEAR** — the only use is inside the refusal |

---

## 6. Tally

| | |
|---|---|
| Lines of v002 read | 429 |
| Sentences extracted mechanically | 397 |
| Quotation-bearing lines judged (run ≥ 8 words) | **98** |
| — **LOCKED** | **97** |
| — **NEEDS SOURCE** | **1** (L171 — §4.1) |
| — **QUARANTINED** | **0** |
| Machine-flagged ALTERED candidates in v002 | 1 → resolved as narration (§4.2) |
| Machine-flagged SPLICE candidates in v002 | 4 → all on the source's own ellipsis, citation or parenthetical |
| Defects carried in from v001 and **resolved** | **8** — 3 record-fills (§2.1) + 3 quotation divergences (§2.2), plus 2 further record-fills (RF-4, RF-5) |
| Further elisions restored in v002 | 5 (§2.2) |
| Tone/villain defects removed | 8 (§2.3) |
| Strings **QUARANTINED** and confirmed absent from v002 | **18** (§2.1–§2.3 + §1.C.1) — every one returns 0 hits |
| Ledger amendments recommended (not script defects) | 3 (§4.4) |
| Quarantine rows swept | 12 of 12 — 11 CLEAR, 1 OWNER CALL (⛔-08) |

**Overall: the script is verbatim-clean against the primary source.** Every one of the 98 quotation-bearing
lines is matched word-for-word in `EP64_memphis_RAW.md`; the three claims this episode was most likely to
get wrong (§1.A, §1.B, §1.C) are each handled as the record requires — both accounts staged and neither
adopted, no overcharge asserted in the film's own voice, and the utility's surviving power to cut service
quoted exactly and reinforced three times. **One line blocks `script_verified`: L171 (§4.1).**

---

*Built 2026-08-04 by mechanical extraction and word-boundary matching against a single primary source —
the full text of 436 U. S. 1 at `episodes/_planning/measurements/EP64_memphis_RAW.md`. No second source was
consulted and no fact in this file comes from memory. The script was not modified by this pass; every fix
above is a recommendation with the source wording attached.*
