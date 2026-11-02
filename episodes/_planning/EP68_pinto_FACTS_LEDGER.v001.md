# EP68 · THE FORD PINTO / *GRIMSHAW v. FORD MOTOR CO.* — FACTS LEDGER v001

**Episode:** EP68 · ID `PD-2026-068-pinto` · slug `pinto` · working title *"The Memo Everybody Quotes Was About Something Else"*
**Case:** *Richard Grimshaw, a Minor, etc. v. Ford Motor Company; Carmen Gray, a Minor, etc., et al. v. Ford Motor Company*, Civ. 20095, **119 Cal. App. 3d 757**, 174 Cal. Rptr. 348, Court of Appeal of California, Fourth Appellate District, Division Two, decided **29 May 1981**.
**Companion matter:** *State of Indiana v. Ford Motor Co.*, Elkhart County indictment 13 Sept 1978; tried at Winamac, Pulaski County; **acquittal 13 March 1980**.
**Purpose:** every factual claim the film may make, with its grade and its source.

**Invariant 1: no unsupported factual statement enters an approved script.** A claim graded ○ may not be spoken, shown, put in a telop, or written into a title until it is upgraded.

**Grades:** ✓ **VERBATIM** = quoted word-for-word from a document retrieved and read by this pass, located by exact string search · ✓ = established from a source retrieved by this pass · ○ = research instruction, **NOT a fact** · ⛔ = quarantined, do not use.

---

## PRIMARY SOURCES — and, for this pass, the ONLY sources

| Tag | Document | Retrieved this pass |
|---|---|---|
| **GR** | *Grimshaw v. Ford Motor Co.*, **119 Cal. App. 3d 757** (1981) — **official California Appellate Reports text**, from the Harvard Caselaw Access Project static archive | **YES.** `static.case.law/cal-app-3d/119/cases/0757-01.json` → opinion 175,537 chars; persisted with header as 178,822 chars |
| **GRB** | The same opinion, **independent second copy** — the West / *Cal. Rptr.* typesetting, from FindLaw | **YES.** `caselaw.findlaw.com/court/ca-court-of-appeal/1835119.html` → 182,907 chars. Used only to cross-check GR, never as the quotation base |
| **MJ** | Mark Dowie, **"Pinto Madness"**, *Mother Jones*, September/October 1977 | **YES.** `motherjones.com/politics/1977/09/pinto-madness/` → 51,001 chars |
| **GS** | E. S. Grush & C. S. Saunby, **"Fatalities Associated with Crash Induced Fuel Leakage and Fires"** (Ford, Environmental and Safety Engineering; "Attachment II") — the document popularly called the Pinto Memo | **YES**, as an 8-page **image-only** PDF, 683,084 bytes, from the Center for Auto Safety (`autosafety.org/wp-content/uploads/import/phpq3mJ7F_FordMemo.pdf`). **All 8 pages read as images this pass.** See the transcription warning below |
| **NH** | **NHTSA recall campaign 78V143000** and the recall record for 1971–1976 Pinto, from NHTSA's own API | **YES.** `api.nhtsa.gov/recalls/campaignNumber?campaignNumber=78V143000` and `…/recallsByVehicle` for model years 1971–1976 |
| **SW** | Gary T. Schwartz, **"The Myth of the Ford Pinto Case"**, 43 Rutgers L. Rev. 1013 (1991) — the counter-case | **PARTIALLY.** 56-page **image-only** HeinOnline scan retrieved in full (4,136,905 bytes) via the Internet Archive. **12 of 56 pages read this pass** (1013, 1014, 1016, 1019, 1021, 1022, 1025, 1028, 1029, 1030, 1031, 1032). 44 pages unread — see ○-09 |
| **NDO** | **Associated Press wire report of the indictment**, printed in *The Observer* (Notre Dame/Saint Mary's), 14 September 1978, p. 1 | **YES.** `archives.nd.edu/observer/1978-09-14_v13_013.pdf` → page 1 text 8,382 chars |
| **CSM** | Charles E. Dole, **"Pinto verdict lets US industry off hook"**, *The Christian Science Monitor*, 14 March 1980 | **YES.** `csmonitor.com/1980/0314/031435.html` → 9,031 chars |

Cached under `episodes/PD-2026-068-pinto/01_research/sources/`.
Machine verifier: **`verify_quotes.v001.py`** · offsets: `verified_offsets.v001.json`
**Run status 2026-08-11: 118 quotations checked, 0 failed** (76 in machine-extracted text, 42 in transcriptions). Two of my own transcriptions failed on the first run and were corrected against the source rather than kept.

sha256 of the searchable texts (recorded by the verifier, which re-checks GR on every run):
`GR b64a28c4…` · `GRB 84b4dc32…` · `MJ cf710046…` · `GS 2bb32cc3…` · `NH 270c38c1…` · `SW 547247be…` · `CSM d9325557…` · `NDO 431e4977…`

**Verifier note.** The verifier prints `WARN … (string occurs more than once)` for the six NHTSA
rows. That is expected and is not a failure: NHTSA's API returns one identical record per
model-year/make covered by the campaign, so the same summary text appears eight times in the JSON.
Every other quotation in the ledger occurs exactly once in its source.

**Citation convention.** `@NNNNN` is the **character offset of the first character of the quoted string inside the cached text file** named in the row. All files were normalised to LF newlines before offsets were taken.

---

## ⚠ TWO EXTRACTION WARNINGS — read before quoting anything

**1. Two of the eight sources have no text layer at all.** The Grush/Saunby memo (**GS**) and the Schwartz article (**SW**) are bitmap scans. `pdftotext` returns 8 characters from the memo and only the HeinOnline page stamp from Schwartz; `pypdf` returns nothing from either. For both, the page bitmaps were extracted with pypdf and **read as images**, and the load-bearing passages were **transcribed by hand** into
`SRC-0003T_grush_saunby_transcription.v001.txt` and `SRC-0005T_schwartz_transcription.v001.txt`.
**The page images are the authority. The transcriptions are locators.** A green verifier run on a GS or SW row proves the ledger matches the transcription — it does **not** prove the transcription matches the paper. Every such row is marked **TRANSCRIBED** below, and the page image must be re-read before the words go on screen. The memo photocopy is degraded; single characters are damaged in the original scan (p.1 prints "the rollover portion ot the amended Standard"), and one run of text on p.1 is unreadable and is marked `[SCAN DAMAGED]`. **Do not treat any single character in a transcription as evidence.**

**2. The name is spelled two ways, and the popular spelling is the wrong one.** The official reporter says **"Mrs. Lilly Gray"** (GX-01, and the independent *Cal. Rptr.* copy agrees, GB-01). Schwartz and most popular retellings say **"Lily Gray"** (SW-16). **Use "Lilly Gray"** — the reporter is the record — and never write the name three ways in one film.

---

## 0. GATE STATUS

| # | Gate | Status |
|---|---|---|
| 1 | Read the appellate opinion end to end | **DONE.** Official Cal. App. 3d text, plus an independent second copy cross-checked on the identity and damages sentences (GB-01, GB-02). |
| 2 | Retrieve the document behind the "$200,000 per death / $11 per car" story | **DONE, AND IT CHANGES THE FILM.** All 8 pages read. See §6. |
| 3 | Retrieve the *Mother Jones* article that created the popular story | **DONE.** Full text. |
| 4 | Retrieve NHTSA's recall record for the 1971–76 Pinto | **DONE.** Campaign 78V143000 from NHTSA's own API. |
| 5 | The criminal prosecution, *State of Indiana v. Ford Motor Co.* | **PARTIAL.** **No published judicial opinion was found or retrieved** (○-06). Two contemporaneous press reports were retrieved — the AP wire on the indictment and the *Christian Science Monitor* on the verdict — plus Schwartz's account of the trial evidence. **There is no primary court document for this half of the story.** |
| 6 | The scholarly counter-case | **PARTIAL.** Schwartz retrieved in full, 12 of 56 pages read (○-09). Lee & Ermann (1999) **not retrieved** (○-10). |
| 7 | CourtListener for the docket and any later history | **BLOCKED.** `HTTP 429 — Rate limit exceeded: 125/day. Expected available in 17096 seconds.` on the 2026-08-11 pass. Nothing after 10 September 1981 is sourced. ⛔-16. |
| 8 | Living named parties: **Ford Motor Company** (corporation), **Richard Grimshaw** (a private individual, 13 at the time, may be living) | **CONSTRAINED.** Rules at ⛔-08 through ⛔-11. |
| 9 | The NHTSA Investigation Report the death numbers come from | **NOT RETRIEVED (○-03).** Known only as Schwartz describes it. |

---

## 1. IDENTITY AND POSTURE

| ID | Claim | Grade | Source |
|---|---|---|---|
| ID-01 | The case is *Richard Grimshaw, a Minor, etc., Plaintiff and Appellant, v. Ford Motor Company, Defendant and Appellant; Carmen Gray, a Minor, etc., et al. v. Ford Motor Company*, **Civ. 20095**, Court of Appeal, Fourth District, Division Two, California, decided **29 May 1981**. Official citation **119 Cal. App. 3d 757**; parallel **174 Cal. Rptr. 348**. | ✓ | GR header block (CAP metadata: `decision_date 1981-05-29`, citation `119 Cal. App. 3d 757`); GRB caption |
| ID-02 | The opinion is by **Acting Presiding Justice Tamura**. | ✓ | GR @1721 (`Opinion / TAMURA, Acting P. J.`) |
| ID-03 | It was **not unanimous in its reasoning**. Justice McDaniel concurred; **Justice Kaufman concurred separately**: ✓ **"Although I agree with the ultimate disposition of each"** issue, he was "unable to subscribe en toto" to the parts on Copp's testimony, the in-limine order and the design-defect instructions. | ✓ VERBATIM (opening clause) | GR @147643 |
| ID-04 | ✓ **"A petition for a rehearing was denied June 18, 1981, and the petitions of appellant Ford Motor Company and appellants Gray et al. for a hearing by the Supreme Court were denied September 10, 1981."** **This is the last event in any document retrieved.** | ✓ VERBATIM | GR @148023 |
| ID-05 | The court told the reader what kind of document it is: ✓ **"Since sufficiency of the evidence is in issue only regarding the punitive damage award, we make no attempt to review the evidence bearing on all of the litigated issues."** | ✓ VERBATIM | GR @3706 |
| ID-06 | And how it read the evidence: ✓ **"We will view the evidence in the light most favorable to the parties prevailing below, resolving all conflicts in their favor, and indulging all reasonable inferences favorable to them."** **This is the single most important sentence in the ledger for tone.** ⛔-13. | ✓ VERBATIM | GR @4059 |
| ID-07 | Schwartz makes the same point about the opinion, from the other side: ✓ **"Because the defendant was appealing a jury verdict in favor of the plaintiffs, the court was under an obligation to view all the evidence in a way most favorable to the plaintiffs and essentially to ignore evidence in the record that might be favorable to the defendant."** | ✓ VERBATIM **TRANSCRIBED** | SW @3019 · p.1016 n.9 |
| ID-08 | ✓ **"PIaintiffs settled with the other defendants before and during trial; the case went to verdict only against Ford Motor Company."** (The `PIaintiffs` capital-I is an artefact of the reporter's own typesetting, reproduced by CAP.) | ✓ VERBATIM | GR @151396 |
| ID-09 | The court's summary of the whole appeal: ✓ **"In the ensuing analysis (ad nauseam) of Ford's wide-ranging assault on the judgment, we have concluded that Ford has failed to demonstrate that any errors or irregularities occurred during the trial which resulted in a miscarriage of justice requiring reversal."** | ✓ VERBATIM | GR @19333 |

**9 rows, 7 with a verbatim quotation.**

---

## 2. THE CRASH, AND THE TWO PEOPLE IN THE CAR

| ID | Claim | Grade | Source |
|---|---|---|---|
| PP-01 | The opening sentence of the opinion, which is also the whole case: ✓ **"A 1972 Ford Pinto hatchback automobile unexpectedly stalled on a freeway, erupting into flames when it was rear ended by a car proceeding in the same direction. Mrs. Lilly Gray, the driver of the Pinto, suffered fatal burns and 13-year-old Richard Grimshaw, a passenger in the Pinto, suffered severe and permanently disfiguring burns on his face and entire body."** | ✓ VERBATIM | GR @1751 · cross-checked GRB @1914 |
| PP-02 | ✓ **"On May 28, 1972, Mrs. Gray, accompanied by 13-year-old Richard Grimshaw, set out in the Pinto from Anaheim for Barstow to meet Mr. Gray. The Pinto was then 6 months old and had been driven approximately 3,000 miles."** | ✓ VERBATIM | GR @4973 |
| PP-03 | The cause of the stall was **not** the fuel tank: ✓ **"Shortly after this lane change, the Pinto suddenly stalled and coasted to a halt in the middle lane. It was later established that the carburetor float had become so saturated with gasoline that it suddenly sank, opening the float chamber and causing the engine to flood and stall."** | ✓ VERBATIM | GR @5482 |
| PP-04 | The closing speed, **as the jury found it**: ✓ **"The Galaxie had been traveling from 50 to 55 miles per hour but before the impact had been braked to a speed of from 28 to 37 miles per hour."** ⚠ **Ford's case at trial was the opposite** — see CC-02. Never state the speed without saying whose finding it is. | ✓ VERBATIM | GR @5924 |
| PP-05 | ✓ **"By the time the Pinto came to rest after the collision, both occupants had sustained serious burns. When they emerged from the vehicle, their clothing was almost completely burned off. Mrs. Gray died a few days later of congestive heart failure as a result of the burns."** | ✓ VERBATIM | GR @6523 |
| PP-06 | ✓ **"Grimshaw managed to survive but only through heroic medical measures. He has undergone numerous and extensive surgeries and skin grafts and must undergo additional surgeries over the next 10 years."** | ✓ VERBATIM | GR @6794 |
| PP-07 | **The court then stopped, and the film stops there too:** ✓ **"Because Ford does not contest the amount of compensatory damages awarded to Grimshaw and the Grays, no purpose would be served by further description of the injuries suffered by Grimshaw or the damages sustained by the Grays."** **Everything about Richard Grimshaw's injuries beyond PP-01 and PP-06 is outside the retrieved record.** ⛔-08. | ✓ VERBATIM | GR @7151 |
| PP-08 | The opinion also records that he lost portions of several fingers on his left hand and portions of his left ear, and that his face required many skin grafts. **This is the outer limit; it is in the same sentence block as PP-06 and is recorded here so that the writer knows it exists and knows it is the end of the list.** ⚠ **Recorded but not quoted, and not to be depicted.** | ✓ | GR @6794–7150 (same passage as PP-06) |
| PP-09 | Grimshaw sued **by his guardian ad litem**; the Grays were the heirs of Mrs. Gray. ✓ **"Grimshaw was permitted to amend his complaint to seek punitive damages but the Grays' motion to amend their complaint for a like purpose was denied."** | ✓ VERBATIM | GR @17970 |
| PP-10 | **Whose case went on which theory:** Grimshaw's went to the jury on **negligence and strict liability**; the Grays' went **only on strict liability**. | ✓ | GR @18150 (same passage as PP-09) |
| PP-11 | Schwartz, writing ten years later, spells the driver's name differently and adds the detail that she was Grimshaw's neighbour: ✓ **"In May 1972, Lily Gray began a trip in her 1972 Pinto with her Orange County neighbor, 13-year-old Richard Grimshaw."** ⚠ **"Lily" is Schwartz's spelling. The reporter says "Lilly". See the extraction warning.** | ✓ VERBATIM **TRANSCRIBED** | SW @2331 · p.1016 |

**11 rows, 8 with a verbatim quotation.**

---

## 3. THE CAR — design, crash tests, and what a fix cost

| ID | Claim | Grade | Source |
|---|---|---|---|
| CAR-01 | ✓ **"In 1968, Ford began designing a new subcompact automobile which ultimately became the Pinto. Mr. Iacocca, then a Ford vice president, conceived the project and was its moving force. Ford's objective was to build a car at or below 2,000 pounds to sell for no more than $2,000."** | ✓ VERBATIM | GR @7410 |
| CAR-02 | ✓ **"Pinto, however, was a rush project, so that styling preceded engineering and dictated engineering design to a greater degree than usual. Among the engineering decisions dictated by styling was the placement of the fuel tank."** | ✓ VERBATIM | GR @7797 |
| CAR-03 | The tank sat beh✓ **"ind the rear axle leaving only 9 or 10 inches of 'crush space'—far less than in any other American automobile or Ford overseas subcompact."** (The quotation starts mid-word because the sentence spans a reporter page break; quote it from "leaving only".) | ✓ VERBATIM | GR @8300 |
| CAR-04 | ✓ **"The crash tests revealed that the Pinto's fuel system as designed could not meet the 20-mile-per-hour proposed standard."** Prototypes struck at 21 mph had the tank driven forward and punctured; a production Pinto at 21 mph into a fixed barrier had the fuel neck torn from the tank and the tank punctured by a bolt head on the differential housing. | ✓ VERBATIM (first sentence) + ✓ | GR @10076, and @10200–10600 for the test descriptions |
| CAR-05 | **The court's list of fixes and prices, per car:** longitudinal side members $2.40; cross members $1.80; a single shock-absorbent "flak suit" $4; a tank within a tank and placement over the axle $5.08–$5.79; a nylon bladder $5.25–$8; tank over the axle with a protective barrier $9.95; a smooth differential housing $2.10; a shield between housing and tank $2.35; bumper improvement $2.60; eight inches of crush space $6.40. | ✓ | GR @11600–12780 |
| CAR-06 | **The headline number, and it is not $11:** ✓ **"Equipping the car with a reinforced rear structure, smooth axle, improved bumper and additional crush space at a total cost of $15.30 would have made the fuel tank safe in a 34 to 38-mile-per-hour rear-end collision by a vehicle the size of the Ford Galaxie."** ⚠ **$15.30 is the appellate court's per-car figure for a package of Pinto fixes. $11 is a different figure in a different document about a different requirement for the whole industry (§6). They are not the same number.** ⛔-17. | ✓ VERBATIM | GR @12791 |
| CAR-07 | These prices, like everything else in §3, are the evidence **as the court was obliged to read it** (ID-06). Ford contested them at trial; the opinion does not set out Ford's figures. | ✓ | ID-06 + the absence of any Ford cost figure in GR |

**7 rows, 5 with a verbatim quotation.**

---

## 4. WHAT THE COURT FOUND ABOUT FORD'S MANAGEMENT — and nothing beyond it

| ID | Claim | Grade | Source |
|---|---|---|---|
| MG-01 | ✓ **"The Pinto crash tests results had been forwarded up the chain of command to the ultimate decision-makers and were known to the Ford officials who decided to go forward with production."** | ✓ VERBATIM | GR @14401 |
| MG-02 | **The plaintiffs' principal witness, named by the court:** ✓ **"Harley Copp, a former Ford engineer and executive in charge of the crash testing program, testified that the highest level of Ford's management made the decision to go forward with the production of the Pinto, knowing that the gas tank was vulnerable to puncture and rupture at low rear impact speeds creating a significant risk of death or injury from fire and knowing that 'fixes' were feasible at nominal cost. He testified that management's decision was based on the cost savings which would inure from omitting or delaying the 'fixes.'"** ⚠ **This is testimony the court recites, not an independent judicial finding of fact about any individual.** | ✓ VERBATIM | GR @14586 |
| MG-03 | **The corroborating document that was actually in evidence — exhibit 125:** ✓ **"At an April 1971 product review meeting chaired by Mr. MacDonald, those present received and discussed a report (exhibit 125) prepared by Ford engineers pertaining to the financial impact of a proposed federal standard on fuel system integrity and the cost savings which would accrue from deferring even minimal 'fixes.'"** | ✓ VERBATIM | GR @15292 |
| MG-04 | **Exhibit 125 is quoted at length in the opinion's footnotes**, under the title "Fuel System integrity Program financial review". Its own recommendation, in its own words: ✓ **"A design cost savings $10.9 million (1974-1975) can be realized by this delay."** — the delay being the addition of flak suits or bladders on all affected cars until 1976. | ✓ VERBATIM | GR @150773 |
| MG-05 | Exhibit 125 also states: ✓ **"Currently there are no plans for forward models to repackage the fuel tanks."** and that the Pinto was the ✓ **"[s]mallest car line with most difficulty in achieving compliance."** ⚠ The bracketed `[s]` is the reporter's alteration, not the document's text. | ✓ VERBATIM | GR @16436, @16652 |
| MG-06 | **MG-03 through MG-05 are the film's real "cost-benefit" evidence, and they are stronger than the famous memo, because they were admitted and the famous memo was not.** See §6 and ⛔-05. | ✓ | MG-03–MG-05 + DOC-01 |
| MG-07 | The court's conclusion on malice: ✓ **"There was evidence that Ford could have corrected the hazardous design defects at minimal cost but decided to defer correction of the shortcomings by engaging in a cost-benefit analysis balancing human lives and limbs against corporate profits. Ford's institutional mentality was shown to be one of callous indifference to public safety."** | ✓ VERBATIM | GR @98893 |
| MG-08 | And the legal standard it satisfied: ✓ **"There was substantial evidence that Ford's conduct constituted 'conscious disregard' of the probability of injury to members of the consuming public."** | ✓ VERBATIM | GR @99231 |
| MG-09 | **Individuals named by the opinion, and only in these roles:** Mr. Iacocca (then a Ford vice president / executive vice president; conceived the Pinto), Mr. Robert Alexander (vice president of car engineering), Mr. Harold MacDonald (group vice president of car engineering; chaired the April 1971 meeting), Mr. Kennedy (succeeded Copp on crash testing), Harley Copp (former Ford engineering executive, the plaintiffs' witness). **No court found any of them personally culpable of anything.** ⛔-10. | ✓ | GR @7410, @13484–14400, @16900 |

**9 rows, 7 with a verbatim quotation.**

---

## 5. THE MONEY — four different numbers, and they must never be merged

| ID | Claim | Grade | Source |
|---|---|---|---|
| MN-01 | **(a) WHAT THE JURY AWARDED.** ✓ **"The jury actually awarded Grimshaw $2,841,000 compensatory damages and $125 million punitive damages and the Grays $659,680 compensatory damages."** | ✓ VERBATIM | GR @148220 (footnote 1) |
| MN-02 | **(b) WHAT THE JUDGMENT SAID, after prior settlements were credited.** ✓ **"Pursuant to stipulation that sums previously received by plaintiffs from others should be deducted from the amounts awarded by the jury, the judgment was modified to reflect compensatory damages in favor of Grimshaw for $2,516,000 and in favor of the Grays for $559,680."** | ✓ VERBATIM | GR @148220 (same footnote) |
| MN-03 | **(c) WHAT THE TRIAL COURT REDUCED THE PUNITIVE AWARD TO.** ✓ **"Following a six-month jury trial, verdicts were returned in favor of plaintiffs against Ford Motor Company. Grimshaw was awarded $2,516,000 compensatory damages and $125 million punitive damages; the Grays were awarded $559,680 in compensatory damages. On Ford's motion for a new trial, Grimshaw was required to remit all but $3 1/2 million of the punitive award as a condition of denial of the motion."** | ✓ VERBATIM | GR @2194 · cross-checked GRB @2304 |
| MN-04 | **The remittitur was $125,000,000 → $3,500,000, a reduction of 97.2%.** Our arithmetic on MN-03, labelled as ours. | ✓ (own arithmetic) | MN-03 |
| MN-05 | **(d) WHAT THE COURT OF APPEAL DID.** ✓ **"judgment, the conditional new trial order, and the order denying Ford's motion for judgment notwithstanding the verdict on the issue of punitive damages are affirmed."** and, separately, ✓ **"The judgment in Gray v. Ford Motor Co. is affirmed."** **The Court of Appeal changed no number.** | ✓ VERBATIM | GR @125601, @147554 |
| MN-06 | **The trial court's stated reasons for the reduction**, as the appellate court recites them: it noted ✓ **"based on the fact that Ford's net worth was $7.7 billion and its profits during the last quarter of the year referred to in the financial statement introduced into evidence were more than twice the punitive award, that the award was not disproportionate to Ford's net assets or to its profit generating capacity"** — and then reduced it anyway, because ✓ **"The court noted, however, that the amount of the punitive award was 44 times the compensatory award"** and the excess over compensatory was over $122 million. | ✓ VERBATIM | GR @119226, @119539 |
| MN-07 | **The trial judge expressly refused to say the jury had used the Ford financial exhibit:** the court was ✓ **"not suggesting that the amount was warranted 'or that the jury did utilize Exhibit 125, or any other exhibits, and if they did, that they were justified in so doing.'"** ⚠ **Nobody knows how the jury got to $125 million. Do not explain it.** | ✓ VERBATIM | GR @119023 |
| MN-08 | ✓ **"Here, the judge, exercising his independent judgment on the evidence, determined that a punitive award of $3 1/2 million was 'fair and reasonable.'"** | ✓ VERBATIM | GR @124184 |
| MN-09 | **The Grays got no punitive damages at all**, and that is the *Grays'* half of the case: ✓ **"The Grays' motion to amend their complaint to add allegations seeking punitive damages was denied on the ground such damages are not recoverable in a wrongful death action."** The Court of Appeal affirmed that too — under California law then, punitive damages were not recoverable in a wrongful-death action. **The woman who died recovered nothing punitive; the boy who lived recovered $3.5 million.** | ✓ VERBATIM (first sentence) + ✓ | GR @126673; the wrongful-death analysis runs GR @126800–147553 |
| MN-10 | **What Ford actually paid, and when, is not in any document retrieved.** ○-05, ⛔-16. | ○ | — |

**10 rows, 8 with a verbatim quotation.**

---

## 6. THE DOCUMENT EVERYBODY QUOTES — and what it actually says

> **This section is the reason to make the film.** Retrieved and read in full this pass, 8 pages.

| ID | Claim | Grade | Source |
|---|---|---|---|
| DOC-01 | **The famous memo was excluded from evidence in *Grimshaw*.** The appellate court, dealing with a complaint about plaintiffs' counsel's closing argument: ✓ **"Ford argues that the documentation referred to by Mr. Copp—the 'Grush-Saunby Report'—was excluded from evidence so that the statement was improper."** The court agreed it had been excluded and held the argument harmless because ✓ **"Mr. Copp was permitted to testify that Ford did in fact engage in cost-benefit analyses which balanced life and limb against corporate savings and profits."** **The jury that returned $125 million never saw the memo.** | ✓ VERBATIM | GR @68569, @68975 |
| DOC-02 | Schwartz gives the procedural history of that exclusion: ✓ **"the Grimshaw plaintiffs did not even claim that the document was relevant to the issue of liability; rather, they attempted to introduce it on the issue of punitive damages, as indicative of Ford's corporate mentality. After considering the matter over a period of several weeks, the trial judge ruled against admissibility."** | ✓ VERBATIM **TRANSCRIBED** | SW @4525 · p.1021 |
| DOC-03 | **The memo's real title and authors:** ✓ **"FATALITIES ASSOCIATED WITH CRASH / INDUCED FUEL LEAKAGE AND FIRES / E. S. Grush and C. S. Saunby"**, on Ford "Inter Office" letterhead of **"Environmental and Safety Engineering"**, headed **"Attachment II"**. Signed by Grush and Saunby, "Impact Factors"; concurred by J. D. Hromi, Principal Staff Engineer, and R. B. MacLean, Impact Factors Manager. | ✓ VERBATIM **TRANSCRIBED** | GS @1735 · pp.1, 7 |
| DOC-04 | **It is a submission to the federal regulator, and it says so in its first paragraph:** ✓ **"The NHTSA has issued Notice 2 of Docket 70-20 and Notice 1 of Docket 73-20, both regarding fuel system integrity."** | ✓ VERBATIM **TRANSCRIBED** | GS @1854 · p.1 |
| DOC-05 | Schwartz places it: ✓ **"this document was not prepared with tort liability in mind, but rather for purposes of submission to NHTSA. Specifically, this Ford report was part of a petition that Ford filed in September 1973, urging NHTSA to reconsider the rollover portion of its recently promulgated standard."** and ✓ **"The report was submitted three years after production of the Pinto had begun."** | ✓ VERBATIM **TRANSCRIBED** | SW @5204, @5503 · p.1021 |
| DOC-06 | **It is about ROLLOVER.** ✓ **"The analysis discussed below concerns the static rollover requirement proposed for FMVSS 301."** and the cost-benefit table is captioned ✓ **"BENEFITS AND COSTS RELATING TO FUEL LEAKAGE ASSOCIATED WITH THE / STATIC ROLLOVER TEST PORTION OF FMVSS 208"**. ⚠ **The document contradicts itself on the standard number** — p.4 says FMVSS 301, the Table 3 caption says FMVSS 208. That inconsistency is in the paper. Do not silently pick one. | ✓ VERBATIM **TRANSCRIBED** | GS @5156, @6878 · pp.4, 6 |
| DOC-07 | **The whole table, verbatim:** ✓ **"Savings - 180 burn deaths, 180 serious burn injuries, 2100 burned vehicles. / Unit Cost - $200,000 per death, $67,000 per injury, $700 per vehicle. / Total Benefit - 180x($200,000)+180x($67,000)+2100x($700) = $49.5 million."** and ✓ **"Sales - 11 million cars, 1.5 million light trucks. / Unit Cost - $11 per car, $11 per truck. / Total Cost - 11,000,000x($11)+1,500,000x($11) = $137 million."** | ✓ VERBATIM **TRANSCRIBED** | GS @6995, @7223 · p.6 |
| DOC-08 | **The word "Pinto" does not appear in the table, and the units are the whole American market.** ✓ **"The Retail Price Equivalent (the customer sticker price with no provision for Ford profit) of vehicle modifications necessary to assure compliance with the static rollover portion of the proposed Standard has been determined by Ford to be an average of $11 per passenger car and $11 per light truck. While these are Ford costs, they have been applied across the industry in this analysis."** | ✓ VERBATIM **TRANSCRIBED** | GS @8692 · p.7 |
| DOC-09 | Schwartz states the same conclusion in one sentence: ✓ **"Its calculations—12.5 million vehicles, 180 deaths—referred not to Pintos, but rather to all cars (as well as light trucks) sold by manufacturers in America in a typical year; the $137 million figure concerned the annual cost to be borne not by Ford alone, but by the entire auto industry."** | ✓ VERBATIM **TRANSCRIBED** | SW @6023 · p.1022 |
| DOC-10 | **The $200,000 is NHTSA's number, and the memo says so twice.** ✓ **"The NHTSA has calculated a value of $200,000 for each fatality."** and, in full: ✓ **"The casualty to dollars conversion factors used in this study were the societal cost values prepared by the NHTSA (6). These values are generally higher than similarly-defined costs from other sources, and their use does not signify that Ford accepts or concurs in the values."** Reference (6) is ✓ **"National Highway Traffic Safety Administration, Societal Costs of Motor Vehicle Accidents, Preliminary Report, April 1972."** | ✓ VERBATIM **TRANSCRIBED** | GS @8075, @7666, @10032 · pp.6, 7, 8 |
| DOC-11 | Schwartz: ✓ **"$200,000 is the value-of-life that NHTSA itself had developed in a 1972 study calculating the social cost of motor-vehicle accidents."** and his conclusion: ✓ **"it is proper to conclude that Ford's utilization of this figure in its submission to NHTSA was not deplorable, but was within the range of expected and acceptable advocacy."** | ✓ VERBATIM **TRANSCRIBED** | SW @6568, @7199 · pp.1022, 1025 |
| DOC-12 | **And *Mother Jones* itself reported the NHTSA origin correctly** — it is the framing that is wrong, not the arithmetic. Dowie wrote ✓ **"And in a 1972 report the agency decided a human life was worth $200,725."** two sentences before writing ✓ **"Ever wonder what your life is worth in dollars? Perhaps $10 million? Ford has a better idea: $200,000."** **The article gives the reader the correction and then buries it under the accusation.** | ✓ VERBATIM | MJ @21884, @21353 |
| DOC-13 | **The memo also argues the fire problem is smaller than the government thinks:** ✓ **"The NHTSA estimate of 2000 to 3500 fatalities yearly in fire-involved motor vehicle crashes appears to overstate the seriousness of the fire problem."** Its basis: of 24 fatally injured occupants of burned vehicles in a sample of more than 5,700, ✓ **"In over half of the instances the deceased was not burned at all, and death can be attributed only to the impact injuries"** and ✓ **"For only five of the 24 fatalities examined was fire reasonably classifiable as the clear cause of the death."** ⚠ **This is Ford arguing its own case to a regulator, on a sample of 24. Present it as advocacy, not as a finding.** | ✓ VERBATIM **TRANSCRIBED** | GS @2203, @4430, @4559 · pp.1, 2 |
| DOC-14 | **The memo's own data on rear impact undercuts its own conclusion, and the film should say so:** ✓ **"the likelihood of a given crash resulting in fuel spillage is much higher for rear impacts (26 percent with spillage in the sample studied) than for other crash types, such as frontals (3.5 percent spillage)."** **The document that is used to prove Ford ignored rear-impact fires is a document that told the government rear impact was by far the worst case.** | ✓ VERBATIM **TRANSCRIBED** | GS @2801 · p.1 |
| DOC-15 | **There was a follow-up report on rear impact, and it did not reach the rollover conclusion.** Schwartz: ✓ **"In fact, a follow-up report, prepared by Grush for Ford, focused on the lateral and rear-impact portions of the new NHTSA standard. It found compliance costs of $100 million annually and safety benefits 'as much as $102 million.' Hence those portions of the standard, unlike the rollover portion, might show 'marginal cost-effectiveness.'"** **The follow-up report itself was NOT retrieved (○-11).** | ✓ VERBATIM **TRANSCRIBED** | SW @5598 · p.1021 n.22 |

**15 rows, 15 with a verbatim quotation. Nine of them are TRANSCRIBED and must be re-read on the page image before broadcast.**

---

## 7. *MOTHER JONES*, "PINTO MADNESS" — what it actually claimed

> The article is a source **for what was published in 1977**, and for nothing else. It is not a source for any fact about the Pinto.

| ID | Claim | Grade | Source |
|---|---|---|---|
| PM-01 | The article's standfirst, as *Mother Jones* republishes it: ✓ **"A Mother Jones Classic: For seven years the Ford Motor Company sold cars in which it knew hundreds of people would needlessly burn to death."** By **Mark Dowie**, September/October 1977 issue. | ✓ VERBATIM | MJ @666 |
| PM-02 | **The death-toll claim, in the author's own words:** ✓ **"By conservative estimates Pinto crashes have caused 500 burn deaths to people who would not have been seriously injured if the car had not burst into flames. The figure could be as high as 900."** **The article gives no source for either number in the text retrieved.** ⛔-01. | ✓ VERBATIM | MJ @4430 |
| PM-03 | ✓ **"Ford knows the Pinto is a firetrap, yet it has paid out millions to settle damage suits out of court, and it is prepared to spend millions more lobbying against safety standards."** | ✓ VERBATIM | MJ @4828 |
| PM-04 | **The sentence that became the whole popular story:** ✓ **"Ford waited eight years because its internal 'cost-benefit analysis,' which places a dollar value on human life , said it wasn't profitable to make the changes sooner."** (The stray space before the comma is in the published text.) | ✓ VERBATIM | MJ @5433 |
| PM-05 | **And the sentence that misstates the memo:** ✓ **"This cost-benefit analysis argued that Ford should not make an $11-per-car improvement that would prevent 180 fiery deaths a year."** ⚠ **Compare DOC-06 through DOC-09.** The $11 and the 180 deaths are the *rollover* line of an industry-wide submission to NHTSA. The article describes them as a Pinto decision. | ✓ VERBATIM | MJ @22436 |
| PM-06 | The article names the document: ✓ **"Ford's cost-benefit table is buried in a seven-page company memorandum entitled 'Fatalities Associated with Crash-Induced Fuel Leakage and Fires.'"** ⚠ The copy retrieved this pass is **8 pages** including the references page; Dowie says seven. Recorded, not resolved. | ✓ VERBATIM | MJ @22763 |
| PM-07 | **What the article achieved, per Schwartz:** ✓ **"The Mother Jones article had encouraged consumers to write to NHTSA and demand a recall of earlier Pintos. Responding to the wave of consumer complaints it received, NHTSA began a recall proceeding relating to 1971-1976 Pintos. NHTSA announced its proceeding on September 13, 1977, not long after the Grimshaw trial had begun."** | ✓ VERBATIM **TRANSCRIBED** | SW @3571 · p.1019 |

**7 rows, 7 with a verbatim quotation.**

---

## 8. NHTSA — the recall, from the agency's own record

| ID | Claim | Grade | Source |
|---|---|---|---|
| RC-01 | The Pinto fuel-tank recall is NHTSA campaign ✓ **"78V143000"**, report received ✓ **"19/06/1978"** (19 June 1978), manufacturer Ford Motor Company, component `FUEL SYSTEM, GASOLINE:STORAGE:TANK ASSEMBLY`. | ✓ VERBATIM | NH @122, @236 |
| RC-02 | **Potential number of units affected, per NHTSA:** ✓ **"PotentialNumberofUnitsAffected": 1400000** — **1,400,000**. ⚠ **Not "1.5 million".** See RC-05. | ✓ VERBATIM | NH @338 |
| RC-03 | NHTSA's summary of the defect: ✓ **"IN THE EVENT THE VEHICLE IS STRUCK FROM THE REAR, THE FUEL FILLER PIPE COULD DISCONNECT FROM THE TANK OR THE TANK COULD BE PUNCTURED IN THE FORWARD FACE. THIS WOULD RESULT IN FUEL LEAKAGE."** | ✓ VERBATIM | NH @396 |
| RC-04 | The remedy: ✓ **"THE DEALER WILL INSTALL A LONGER FUEL FILLER PIPE HAVING AN IMPROVED SEAL. ALSO, A POLYETHYLENE SHIELD WILL BE INSTALLED ON THE FRONT OF THE FUEL TANK."** | ✓ VERBATIM | NH @625 |
| RC-05 | **The campaign covers model years 1971, 1972, 1973, 1974, 1975 and 1976 Ford Pinto, and 1975 and 1976 ✓ "Mercury ... BOBCAT".** Contemporaneously, AP reported the recall as covering ✓ **"Pinto and Mercury Bobcats made between 1971 and 1976 that Ford recalled in June because of government complaints about the fuel tank"**, and put the number at 1.5 million. **NHTSA's own record says 1,400,000. Use NHTSA's number and attribute the 1.5 million to the press if it is used at all.** | ✓ VERBATIM | NH @3037 (all 8 model-year/make rows in the campaign) · NDO @4388 |
| RC-06 | **The recall was announced 12 days after the *Grimshaw* verdict and days before a scheduled NHTSA hearing and a *60 Minutes* segment**, per Schwartz: ✓ **"At this point, Ford decided to undertake a 'voluntary' recall."** — the point being that by early June 1978 the verdict was in, the hearing was pending and the broadcast was imminent. | ✓ VERBATIM **TRANSCRIBED** | SW @4227 · p.1019 |
| RC-07 | **NHTSA had issued an initial determination of defect before the recall:** ✓ **"In May 1978, NHTSA issued an initial determination that the Pinto's fuel system was defective, and scheduled a hearing for June 14 to enable Ford to reply."** | ✓ VERBATIM **TRANSCRIBED** | SW @3898 · p.1019 |
| RC-08 | **Other Pinto recalls exist and are not this one.** NHTSA's record for 1971–76 Pinto also returns 70V134000, 70V114000, 71V111000, 71V045000 (carburetor), 71V216000, 73V025000, 73V058000 (tank assembly, 1973 only, received 12 March 1973), 73V118000, 76V067000, 76V112000, 76V134000, 76V170000, 78V069000. ⚠ **Do not conflate 73V058000 with the 1978 recall.** | ✓ | `SRC-0004_nhtsa_recalls_pinto_1971_1976.json` |
| RC-09 | **The completion rate of the recall — how many of the 1,400,000 cars were actually fixed — is not in any document retrieved.** ○-04. | ○ | — |

**9 rows, 7 with a verbatim quotation.**

---

## 9. *STATE OF INDIANA v. FORD MOTOR CO.* — the half of the story Ford won

> ⚠ **No published judicial opinion in this case was found or retrieved this pass.** Everything below rests on two contemporaneous press reports and on Schwartz. There is no primary court document. ○-06.

| ID | Claim | Grade | Source |
|---|---|---|---|
| IN-01 | ✓ **"An Indiana grand jury indicted Ford Motor Co. yesterday on criminal charges stemming from a fiery, triple-fatality Pinto automobile crash, saying the automaker knew Pinto fuel tanks were unsafe but did nothing about it."** (AP, printed 14 September 1978 — so the indictment was returned **13 September 1978**.) | ✓ VERBATIM | NDO @2054 |
| IN-02 | The grand jury's words as AP reported them: ✓ **"The Elkhart Superior Court panel said the tanks were 'recklessly designed and manufactured in such a manner as would likely cause the Pinto to flame and bum upon rearend impact, and that the Ford Motor Co. had a legal duty to warn the general public.'"** (`bum` is an OCR artefact of `burn` in the scanned page; **use `burn` on screen and say the source is a scanned newspaper**.) | ✓ VERBATIM (as scanned) | NDO @2274 |
| IN-03 | ✓ **"The indictment, the first of its kind in an auto defects case, charged Ford with three counts of reckless homicide and one count of criminal recklessness. Maximum penalties would total $36,000 in fines."** **The maximum exposure was thirty-six thousand dollars.** | ✓ VERBATIM | NDO @2526 |
| IN-04 | **The three who died:** ✓ **"The charges stemmed from the Aug. 10 deaths of Judy Ulrich, 18, of Osceola, Ind., her 16-year-old sister, Lynn, and their cousin, Donna Ulrich, 18, of Roanoke, Ill."** | ✓ VERBATIM | NDO @3446 |
| IN-05 | **The van driver was not charged:** ✓ **"The driver of the van, Robert Duggar, 21, of Goshen, was not indicted because 'although he may have been negligent, we do not believe it constituted a criminal act,' the grand jury said in its report."** ⚠ **He is a private individual who was never charged. ⛔-11.** | ✓ VERBATIM | NDO @3760 |
| IN-06 | **The grand jury deliberately did not charge any person:** ✓ **"The grand jury could have indicted individual Ford executivs, but chose to charge only the corpora-"** (sentence continues on an inside page not retrieved; `executivs` is the scan). | ✓ VERBATIM (as scanned) | NDO @5229 |
| IN-07 | **Ford's contemporaneous position:** ✓ **"Ford called the action unprecedented and 'unwarranted' and said it had not broken any Indiana laws."** and ✓ **"Ford denies the tanks are any more susceptible to explosion that other small cars of those model years, when no federal rear-end collision standards existed."** | ✓ VERBATIM | NDO @3022, @4522 |
| IN-08 | **The prosecution's theory:** ✓ **"'The thrust of the state's case will be to show that the design, engineering and manufacturing of the Ford Pinto was inappropriate and recklessly done, that Ford came to know of the cars defects and did nothing about it,' Cosentino said."** | ✓ VERBATIM | NDO @3961 |
| IN-09 | **THE VERDICT: FORD WAS ACQUITTED.** ✓ **"An Indiana farm country jury in the 10-week landmark trial found Ford 'not guilty' in the deaths of three teen-age girls whose 1973-model Pinto exploded when a speeding van struck it in the rear Aug. 10, 1978."** (*Christian Science Monitor*, 14 March 1980 — so the verdict was **13 March 1980**.) | ✓ VERBATIM | CSM @2343 |
| IN-10 | ✓ **"It was the first time a US corporation had been tried on criminal charges."** ⚠ This is the *Monitor*'s characterisation in 1980, not a verified legal-historical finding. Attribute it. | ✓ VERBATIM | CSM @2747 |
| IN-11 | ✓ **"Thev verdict came on the fourth day of deliberations in the lengthy trial in the small Indiana farm community of Winimac and about 12 hours after jurors had filed into Judge Harold Staffeldt's court to report they were hopelessly deadlocked."** ⚠ The town is **Winamac**; `Winimac` is the *Monitor*'s spelling. `Thev` is the *Monitor*'s typo. | ✓ VERBATIM | CSM @3200 |
| IN-12 | **The two theories of the crash, which is the whole trial:** ✓ **"At issue was the design of the Pinto's gas tank. The prosecution had contended the car was moving and that the speed of the impact would not have been sufficient to trigger an explosion if the car had been safely designed in the first place."** and ✓ **"The defense, on the other hand, said the Pinto was stopped and that impact would have caused similar damage to any car at that time."** | ✓ VERBATIM | CSM @2823, @3066 |
| IN-13 | ✓ **"One of the defense's key witnesses, John E. Habberstad, a Spokane-based accident reconstructionist, showed films of test crashes which revealed that, when hit by 1972-model Chevrolet vans, many other cars had similar damage to that which befell the Ford Pinto in which the three girls perished."** and ✓ **"Mr. Habberstat said the crash occurred at 55 m.p.h. with the Pinto stopped."** (The surname is spelled two ways in the same article.) | ✓ VERBATIM | CSM @4335, @4771 |
| IN-14 | **Why the state lost, according to the state:** ✓ **"A major element in the case was the judge's absolute insistence on following the strictest rules of criminal evidence. As a result, charges the prosecution, it was unable to introduce the supportive evidence it needed in order to build its casE."** (`casE` is the *Monitor*'s typo.) | ✓ VERBATIM | CSM @3554 |
| IN-15 | **The mismatch of resources, in the prosecutor's own words:** ✓ **"Earlier this week, the Indiana prosecutor charged: 'It has just been a matter of David and Goliath when it comes to money. They are the Goliath, and we are the David.'"** ✓ **"The prosecution consisted largely of Michael Cosentino and a volunteer staff of law-school professors and students."** ✓ **"Ford Motor Company hired a hard-hitting defense team, headed by James Neal, a Watergate prosecutor, which won repeatedly in jousts with the prosecution and its witnesses."** | ✓ VERBATIM | CSM @3973, @4142, @3801 |
| IN-16 | **What the acquittal meant to the industry, contemporaneously:** ✓ **"Exoneration of the Ford Motor Company on charges of reckless homicide in the so-called Pinto trial in Winimac, Ind., caused a figurative sigh of relief not only by the United States auto industry, but throughout the entire manufacturing establishment."** | ✓ VERBATIM | CSM @2090 |
| IN-17 | **The comparative-safety evidence that only the criminal jury saw** — Ford's FARS exhibits, and the prosecution's answer to them — is at CC-05 and CC-06. | ✓ | see §10 |
| IN-18 | The cause number is given by Schwartz as **State v. Ford Motor Co., Cause No. 11-431**. **Not independently confirmed; no docket retrieved.** | ○ | SW p.1031 n.71 (read, not transcribed) |

**18 rows, 15 with a verbatim quotation. All from press, not from a court.**

---

## 10. THE COUNTER-CASE — and its limits

> Schwartz is a UCLA law professor writing in 1991, retrieved in full but **read only in part** (12 of 56 pages). He is a secondary source; he is cited here because he is the best-documented challenge to the popular story and because a film that only prosecutes is dishonest. **He also finds against Ford in places, and those rows are here too.**

| ID | Claim | Grade | Source |
|---|---|---|---|
| CC-01 | The thesis: ✓ **"One is that several significant factual misconceptions surround the public's understanding of the case. Given the cumulative force of these misconceptions, the case can be properly referred to as 'mythical.'"** | ✓ VERBATIM **TRANSCRIBED** | SW @2094 · p.1013 |
| CC-02 | **Ford's factual case at trial, which the opinion never mentions:** ✓ **"In fact, Ford's basic position at trial—which the court's opinion at no point mentions—was that the approaching car (a Ford Galaxie) had not slowed down at all, and had struck the Gray car at a speed in excess of 50 miles per hour."** ⚠ **Compare PP-04. Two irreconcilable accounts of the closing speed; the jury took the plaintiffs'.** | ✓ VERBATIM **TRANSCRIBED** | SW @3310 · p.1016 n.9 |
| CC-03 | **The actual death count, as NHTSA compiled it:** ✓ **"Relying on a variety of external sources (including Ford), NHTSA indicated that it was aware of thirty-eight instances in which rear-end impact on Pintos had resulted in fuel-tank leakage or fire; these instances, in turn, resulted in twenty-seven deaths and twenty-four nonfatal burn injuries."** **Twenty-seven, not five hundred to nine hundred.** ⚠ **The NHTSA Investigation Report itself was NOT retrieved (○-03).** | ✓ VERBATIM **TRANSCRIBED** | SW @9536 · p.1030 |
| CC-04 | Independently, ✓ **"FARS data showed that from January 1975 through the middle of 1977, seventeen people had died in accidents in which Pinto rear-end collisions resulted in fires."** And Schwartz's own caution: ✓ **"In setting forth this number, however, NHTSA made no effort to estimate how many of these deaths were caused by the Pinto's specific design features."** | ✓ VERBATIM **TRANSCRIBED** | SW @9987, @10311 · p.1030 |
| CC-05 | **The comparative fatality table** (occupant fatalities per million cars in operation, compiled by Schwartz from NHTSA and registration data): AMC Gremlin 274 / 315 · Chevrolet Vega 288 / 310 · Datsun 1200/210 392 / 418 · Datsun 510 294 / 340 · **Ford Pinto 298 / 322** · Toyota Corolla 333 / 293 · VW Beetle 378 / 370, for 1975 / 1976. His reading: ✓ **"This table suggests that for overall safety purposes the Pinto's record was quite respectable."** | ✓ VERBATIM (conclusion) + ✓ (table) **TRANSCRIBED** | SW @9139 and the table above it · p.1029 |
| CC-06 | **AND THE OTHER SIDE OF THE SAME PAGE — the Pinto was over-represented in the accidents that were actually the issue.** Schwartz: at the criminal trial, when the prosecution's expert used FARS to focus on rear-end fire fatalities, ✓ **"These data showed that Pintos, while comprising 1.9% of the auto population, were responsible for"** ✓ **"4.1% of all such fatalities."** | ✓ VERBATIM **TRANSCRIBED** | SW @11698, @11825 · pp.1031–1032 |
| CC-07 | **And Ford's own comparative memo, which Ford did not put in:** ✓ **"It further showed, however, that the Pinto's rear-fire fatality rate, while considerably below the Gremlin's, was considerably above the respective rates of the Vega, Toyota, Mazda, and Datsun."** ✓ **"perhaps for this reason, Ford did not introduce the memorandum during the criminal trial."** | ✓ VERBATIM **TRANSCRIBED** | SW @12124, @12533 · p.1032 |
| CC-08 | **Also against Ford:** ✓ **"In crash-testing, NHTSA compared the Pinto to the Chevrolet Vega, often regarded (along with the Gremlin) as having the least safe gas tank of the other subcompacts for sale in America. In this process, the Pinto consistently flunked tests that the Vega was able to pass."** | ✓ VERBATIM **TRANSCRIBED** | SW @7724 · p.1028 |
| CC-09 | **The scale of the problem in context:** ✓ **"Only one percent of all traffic crashes result in fires; only four percent of all occupant fatalities occur in fire crashes; only 15% of all fatal fire crashes result from rear-end collisions."** | ✓ VERBATIM **TRANSCRIBED** | SW @8422 · p.1029 n.62 |
| CC-10 | **How many suits there actually were:** ✓ **"The accidents identified by NHTSA had led to 29 lawsuits against Ford. Ford had lost or settled eight of these and had prevailed in one or two; the remainder were pending."** and Schwartz's estimate of Ford's exposure: ✓ **"the number of lawsuits that Ford might have anticipated was perhaps 40, rather than 400 or 4000."** ⚠ **Compare PM-03, "paid out millions to settle damage suits out of court".** | ✓ VERBATIM **TRANSCRIBED** | SW @10485, @6877 · pp.1030, 1022 |
| CC-11 | **The Grimshaw record contained almost nothing about the Pinto's real-world performance**, and both sides kept it out: ✓ **"In the Grimshaw record, there was almost no evidence about the actual safety performance of the Pinto in the field."** | ✓ VERBATIM **TRANSCRIBED** | SW @9262 · p.1029 n.64 |
| CC-12 | **What the counter-case does NOT establish.** It does not establish that the Pinto's fuel system was adequately designed; Schwartz records that it flunked tests the Vega passed (CC-08) and that its rear-fire rate was above the relevant average (CC-06, CC-07). It does not disturb the jury's verdict, the trial judge's independent finding of a fair and reasonable $3.5 million, or the appellate affirmance. **The counter-case is against the folklore, not against the judgment.** | ✓ | CC-06 through CC-08 + MN-05 |

**12 rows, 12 with a verbatim quotation. Eleven are TRANSCRIBED.**

---

## 11. ✗ NOT DECIDED / NOT IN THE RECORD — things a viewer will assume

| ID | The assumption | What the retrieved record actually holds |
|---|---|---|
| NR-01 | "A court found that Ford decided it was cheaper to pay the dead than fix the car." | **No.** The court found conscious disregard and callous indifference on the evidence viewed most favourably to the plaintiffs (MG-07, MG-08, ID-06). The document that is quoted for the "cheaper to pay" proposition was **excluded from evidence** (DOC-01) and is **about rollover across the whole industry** (DOC-06 to DOC-09). |
| NR-02 | "The jury saw the memo." | **No.** DOC-01. |
| NR-03 | "Ford paid $125 million." | **No.** The trial court conditioned denial of a new trial on remittitur to $3.5 million and the Court of Appeal affirmed (MN-03, MN-05). What Ford actually paid is unretrieved (MN-10). |
| NR-04 | "Lilly Gray's family got punitive damages." | **No.** MN-09. |
| NR-05 | "Ford was convicted of homicide." | **No. Ford was acquitted on all counts** (IN-09). |
| NR-06 | "The criminal case was about the Grimshaw crash." | **No.** Different crash, different state, different victims, two years later (IN-01, IN-04). |
| NR-07 | "The recall proves NHTSA found the car defective." | NHTSA issued an **initial determination** of defect in May 1978 and set a hearing; Ford recalled before the hearing (RC-06, RC-07). No final agency determination is in any retrieved document. |
| NR-08 | "Ford ignored the crash tests." | The court found the results went up the chain and were known (MG-01). It did **not** find that any named individual concealed anything. |
| NR-09 | "$11 would have fixed the Pinto." | The $11 is the industry-wide **rollover**-compliance figure in a 1973 NHTSA submission (DOC-08). The appellate court's Pinto figure for a package of rear-impact fixes is **$15.30** (CAR-06). ⛔-17. |
| NR-10 | "500 to 900 people burned to death in Pintos." | That is *Mother Jones*'s unsourced estimate (PM-02). NHTSA's compiled figure is **27** (CC-03). ⛔-01. |

**10 rows.**

---

## 12. ⛔ FORBIDDEN CLAIMS — what this film may not say, and why

| # | Forbidden | Why |
|---|---|---|
| ⛔-01 | **Any Pinto death toll**, in narration, telop, thumbnail or title — "500 to 900", "hundreds", "thousands", "we will never know how many". | The only sourced figures are NHTSA's **27 deaths / 38 incidents / 24 nonfatal burn injuries** (CC-03) and FARS's **17** for 1975–mid-1977 (CC-04), and even NHTSA made no attempt to say how many were caused by the Pinto's design (CC-04). The 500–900 is one sentence in a 1977 magazine with no source given (PM-02). **If a number is used at all it must be 27, it must be attributed to NHTSA via Schwartz, and it must carry Schwartz's own caveat.** |
| ⛔-02 | **"Ford knew and decided it was cheaper to let people burn."** Any variant: "Ford did the math on your life", "Ford put a price on your child". | This is the single most-repeated sentence about this case and no retrieved document supports it. The court found conscious disregard on plaintiff-favourable evidence (MG-07/08, ID-06). The document the sentence is built on is about rollover, for the whole industry, submitted to a regulator three years after production began, and it was **kept out of the trial** (DOC-01 to DOC-09). |
| ⛔-03 | **Calling the Grush/Saunby report "the Pinto Memo", or an "internal Ford memo about the Pinto", or "Ford's secret cost-benefit analysis on the Pinto".** | It is a Ford submission to NHTSA in the fuel-system-integrity rulemaking (DOC-04, DOC-05). The word "Pinto" appears nowhere in its cost-benefit table (DOC-07, DOC-08). Correct description: **"a 1973 Ford submission to the federal regulator, arguing against the rollover portion of a proposed fuel-system standard."** |
| ⛔-04 | **"Ford valued a human life at $200,000."** | $200,000 is **NHTSA's** figure from its own 1972 study (DOC-10, DOC-11), and the memo states in terms that Ford does not accept or concur in it (DOC-10). *Mother Jones* reported the NHTSA origin correctly and then wrote "Ford has a better idea" anyway (DOC-12). |
| ⛔-05 | **Showing the memo, or any part of it, as something the *Grimshaw* jury saw or was persuaded by.** | It was excluded (DOC-01). If the memo appears on screen it must be labelled as excluded, and the document the film should show instead is **exhibit 125** (MG-03 to MG-05), which was in evidence. |
| ⛔-06 | **Any sentence in which the jury's number and the reduced number are not both present, or in which "$125 million" stands alone as what Ford paid.** | MN-01 to MN-05. The four numbers are: jury $2,841,000 + $125,000,000; judgment $2,516,000 after settlement credits; remittitur to $3,500,000; affirmed. |
| ⛔-07 | **Saying the Gray family recovered punitive damages, or that "the family won $125 million".** | MN-09. The punitive award was Grimshaw's alone; the Grays were barred by California's wrongful-death rule. |
| ⛔-08 | **Any generated image, AI video, archive photograph or dramatisation depicting Richard Grimshaw, a burned child, a burned adult, a burn victim's face, skin grafts, or a person on fire.** Any description of his injuries beyond PP-01 and PP-06. Any invented interior life, family scene, hospital scene or "he must have felt". | He was **13** at the time and **may be living**. He is a private individual who was a child. The opinion itself declined to describe his injuries further (PP-07); the film has no standing to go past a court that stopped. PD invariant 11. |
| ⛔-09 | **Dramatising Lilly Gray's death, or naming/characterising her surviving family beyond "the Grays" and "Carmen Gray, a Minor".** | She died of burns days after the crash (PP-05). The plaintiffs included a minor. Nothing else about them is in the record. |
| ⛔-10 | **Naming any Ford employee as culpable, criminal, or a decision-maker who "chose profit over lives".** Iacocca, Alexander, MacDonald, Kennedy, Grush, Saunby, Hromi, MacLean. | No court found any individual liable or guilty of anything. The Elkhart grand jury **could have** indicted individuals and deliberately chose not to (IN-06). Roles may be stated exactly as MG-09 and DOC-03 state them, and no further. Harley Copp may be named because he was the plaintiffs' testifying witness and the court names him as such (MG-02). |
| ⛔-11 | **Naming, depicting identifiably, or characterising Robert Duggar, the van driver.** | He was never charged (IN-05) and is a private individual. |
| ⛔-12 | **"The worst car ever made", "the deadliest car in American history", "a rolling firebomb", "a death trap" — asserted in PD's own voice.** | CC-05 shows the Pinto's overall fatality rate mid-pack among its class. The phrases may be **quoted and attributed** to 1977–78 press (PM-01, PM-04) as claims made at the time; they may not be PD's narration. |
| ⛔-13 | **Presenting the appellate opinion as a neutral account of what happened.** | The court says itself it viewed all evidence most favourably to the plaintiffs and made no attempt to review the evidence on other issues (ID-05, ID-06). Schwartz says the same from outside (ID-07). Every §3 and §4 fact must be framed as *what the jury could find* / *the evidence as the appellate court was required to read it*. |
| ⛔-14 | **Quoting the reporter's head matter, syllabus or headnotes as the court's words.** | The persisted GR file marks the head matter explicitly (`=== HEAD MATTER (reporter head matter, NOT part of the opinion) ===` at the top, opinion text begins at offset 1722). No ✓ VERBATIM row in this ledger draws from before offset 1722. |
| ⛔-15 | **Any generated image presented as: the Grush/Saunby memo, exhibit 125, a Ford crash-test report, an NHTSA letter or recall notice, a page of the Grimshaw record, the Elkhart indictment, or a period newspaper front page.** | PD invariant 11. The *text* of exhibit 125 and of the memo may be set as typographic cards, because both are quoted in retrieved documents — but never styled to look like a photograph of the original paper. |
| ⛔-16 | **Anything after 10 September 1981** — whether Ford paid, what became of Richard Grimshaw, Ford's later fuel-system practice, later Pinto litigation, the recall completion rate, or the case's later citation history. | ID-04 is the last event in any retrieved document. **CourtListener returned HTTP 429 (125/day exceeded, ~4.75h to reset) on this pass** and no docket could be checked. ○-05. |
| ⛔-17 | **Treating $15.30 and $11 as the same number, or letting them appear in the same breath without their two different origins.** | CAR-06 vs DOC-08. This is the most inviting arithmetic error in the episode because both are small dollar figures per car. |
| ⛔-18 | **Any claim about how many Pintos burned, how many suits Ford settled, or how much Ford paid out in settlements.** | The only sourced figure is CC-10: **29 lawsuits, eight lost or settled, one or two won, the rest pending** as of the NHTSA investigation. PM-03's "millions to settle damage suits" is *Mother Jones* in 1977 and is not independently sourced. |
| ⛔-19 | **Saying the criminal jury "let Ford off on a technicality", or that the acquittal was bought.** | The retrieved account is that the judge enforced strict criminal evidence rules, that the prosecution said this cost it its case (IN-14), that Ford's defence out-resourced a volunteer prosecution (IN-15), and that Ford's comparative-crash evidence went unrebutted (IN-13, CC-06 note). **State the imbalance as the prosecutor stated it and let it stand. Do not conclude.** |
| ⛔-20 | **Using any fact from an unread page of Schwartz (44 of 56), or from `ij.org`, or from any encyclopaedia, wiki, case-brief site, quiz site or engineering-ethics course PDF.** | Nothing from those was retrieved or is permitted. One such course PDF (`cedengineering.com`, Rossow) was fetched during this pass, read, judged tertiary, and **deleted from the source cache** so that it cannot be cited by accident. |

**20 quarantine entries.**

---

## 13. ○ OPEN QUESTIONS — what a viewer will ask that the record cannot answer

**Nothing here may be spoken, shown, or implied until it is upgraded from a source read directly.**

| ID | Question | Why it is here |
|---|---|---|
| ○-01 | **What did the trial court's new-trial order actually say?** | It is recited by the appellate court (MN-06, MN-07, MN-08) and nowhere else. The order itself was not retrieved and is probably unpublished. |
| ○-02 | **The *Grimshaw* trial transcript.** | Not retrieved. Schwartz quotes it by reporter initials and page (e.g. "PG 2691", "RG 2121-23"). The film may not use any transcript quotation that is not carried inside a retrieved document. |
| ○-03 | **NHTSA's 1978 Investigation Report** — the source of 38 incidents / 27 deaths / 24 injuries. | **NOT RETRIEVED.** Everything in CC-03 comes from Schwartz describing it. This is the single most load-bearing unretrieved document in the ledger, because the film's central corrective number lives in it. **Retrieve it before the 27 goes on screen.** |
| ○-04 | **The recall: notification letters, dates, and completion rate.** | Only the NHTSA database record was retrieved (§8). How many of the 1,400,000 cars were actually modified is unknown. |
| ○-05 | **Anything after 10 September 1981.** | CourtListener HTTP 429. ⛔-16. **The film currently has an ending — the acquittal in 1980 and the affirmance in 1981 — so this does not block the script the way EP67's remand gap did. But it does block any "and today…" line.** |
| ○-06 | **Any primary court document from *State of Indiana v. Ford Motor Co.*** | No published opinion was found. No indictment, no docket, no transcript, no verdict form was retrieved. §9 rests entirely on two newspapers and one law review. **A 30-minute film that spends ten minutes in Winamac needs better than this.** |
| ○-07 | **Richard Grimshaw's life after 1981.** | **DELIBERATELY CLOSED.** He was a child at the time and may be living. Not to be researched, not to be mentioned. ⛔-08. |
| ○-08 | **"Lilly" or "Lily"?** | The official reporter and its independent second copy both say **Lilly** (PP-01, GB-01); Schwartz and the popular literature say Lily (PP-11). Unresolved; the reporter governs. |
| ○-09 | **The other 44 pages of Schwartz.** | Pages 1015, 1017–1018, 1020, 1023–1024, 1026–1027 and 1033–1068 were **not read**. The PDF is cached and the page images are extracted, so this is cheap to close. Parts II and III of the article (public attitudes, duty to warn) are entirely unread. |
| ○-10 | **Lee & Ermann, "Pinto 'Madness' as a Flawed Landmark Narrative", *Social Problems* 46(1) (1999).** | Not retrieved. It is the other major scholarly challenge and it reaches partly different conclusions from Schwartz. The counter-case currently rests on one author. |
| ○-11 | **The follow-up Grush report on lateral and rear impact** ($100 m cost vs "as much as $102 million" benefit). | DOC-15. Known only from Schwartz's footnote; the report is "in my files", i.e. not public. This document, if it exists in an archive, is more relevant to the Pinto than the famous one. |
| ○-12 | **Ford's Pinto production and sales totals, from a primary source.** | Not retrieved. *Mother Jones* says "over two million on the road" and "a half million cars rolling off the assembly lines each year"; those are 1977 journalism, not a Ford or NHTSA figure. |
| ○-13 | **What the 1977-model-year design changes actually were, and when they were decided.** | Only Schwartz's one-line description via the recall (RC-06). |
| ○-14 | **Whether any of the 27 NHTSA-identified deaths involved a car that had been through the recall.** | Not in any retrieved document, and probably unanswerable. Do not imply it either way. |

**14 open questions.**

---

## THE SHAPE THE FACTS ALREADY HAVE

*Not a claim — a note for the writer.*

```
   WHAT THE FILM IS EXPECTED TO SAY          WHAT THE DOCUMENTS SAY

   "the Pinto memo"                    →     a 1973 submission to NHTSA
                                             opposing the ROLLOVER portion
                                             of a proposed standard        (DOC-04/06)

   "$11 would have fixed the Pinto"    →     $11/vehicle × 12.5 m vehicles,
                                             the whole US industry, rollover
                                             compliance                    (DOC-07/08)
                                             — the Pinto figure the COURT used
                                               is $15.30                   (CAR-06)

   "Ford valued a life at $200,000"    →     NHTSA valued a life at $200,000;
                                             the memo says Ford does not
                                             concur                        (DOC-10)

   "500 to 900 burned to death"        →     NHTSA compiled 27             (CC-03)

   "the jury saw the memo and was       →    the memo was EXCLUDED         (DOC-01)
    so appalled it awarded $125 m"           nobody knows how the jury got
                                             to $125 m, and the judge
                                             refused to guess              (MN-07)

   "Ford paid $125 million"            →     remitted to $3.5 million      (MN-03)

   "Ford was found guilty"             →     ACQUITTED, 13 March 1980      (IN-09)
```

**And the honest complication the film owes the viewer — the counter-case is not a defence.**
On the same pages where Schwartz dismantles the folklore, he records that the Pinto **consistently
flunked crash tests the Chevrolet Vega passed** (CC-08); that Pintos were **1.9% of the cars and
4.1% of the rear-end fire deaths** (CC-06); and that **Ford's own comparative memo put the Pinto's
rear-fire rate above the Vega, Toyota, Mazda and Datsun — and Ford did not put that memo in at its
own criminal trial** (CC-07). Meanwhile the document that *was* admitted in *Grimshaw* — exhibit
125, Ford's own "Fuel System integrity Program financial review" — recommends deferring the fix
and states the saving in its own words: ✓ *"A design cost savings $10.9 million (1974-1975) can be
realized by this delay."* (MG-04)

So the film's spine is not "Ford was innocent" and not "Ford was a murderer". It is:

1. **1971–72.** A car goes to market with 9 or 10 inches of crush space, having failed the
   20-mph test its own engineers ran. (CAR-03, CAR-04)
2. **April 1971.** A Ford committee is told the fix can be deferred and the saving is $10.9 m.
   (MG-03, MG-04)
3. **May 1972.** Lilly Gray's Pinto stalls on Interstate 15. She dies of burns. A 13-year-old
   survives. (PP-02 to PP-06)
4. **September 1977.** A magazine publishes a number nobody can source, attached to a document
   about something else, and the number is what everyone remembers. (PM-02, PM-05)
5. **February 1978 / May 1981.** A jury awards $125 m; a judge cuts it to $3.5 m; an appellate
   court affirms both. (MN-01, MN-03, MN-05)
6. **June 1978.** 1,400,000 cars recalled — twelve days after the verdict, days before a hearing
   and a *60 Minutes* segment. (RC-01, RC-02, RC-06)
7. **March 1980.** The State of Indiana tries Ford for homicide and **loses**. (IN-09)
8. **1991.** A law professor takes the story apart and finds that the most quoted facts in it are
   wrong — and that the car still failed tests its competitors passed. (CC-01, CC-08)

The ending is not a verdict. It is that **the true story is worse in one way and better in
another than the famous one, and the famous one is what got told for fifty years.**

---

*Built 2026-08-11 from the official California Appellate Reports text of an opinion read end to
end (178,822 chars), a second independent copy of the same opinion used to cross-check identity
and damages, all eight pages of the Grush/Saunby report read as images, the full text of the
1977 Mother Jones article, NHTSA's own recall database, twelve pages of Gary Schwartz's 1991
article read as images, and two contemporaneous press reports of the Indiana prosecution.
**No fact in this ledger comes from memory, from a search-engine summary, or from a subagent;
every retrieval in it was performed by this pass and every quotation was re-located by exact
string search.** **107 fact rows** (identity 9, crash-and-people 11, car 7, management 9, money 10,
the document 15, Mother Jones 7, NHTSA 9, Indiana 18, counter-case 12) · **10 ✗ not-in-record
rows** · **20 quarantine entries** · **14 open questions**.
**118 distinct quotations are machine-verified ✓ VERBATIM** and re-verifiable with
`verify_quotes.v001.py` (exits non-zero on any failure; last run 2026-08-11, 118/118, exit 0).
**42 of those 118 sit in transcriptions of image-only scans and must be re-read on the page image
before they are spoken on screen.** **Gate ○-03 — NHTSA's Investigation Report — should be closed
before the number 27 is used.** Nothing here has been written into a script.*
