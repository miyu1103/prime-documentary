# PD-2026-062-greene — Fact + Quotation Re-check v001 (R2/R3)

- Re-check date: 2026-08-04 JST
- Status: **PASS_WITH_7_OPEN_ITEMS** — 2 QUARANTINED, 5 NEEDS SOURCE. **Not clear for render until §6 is closed.**
- Episode: PD-2026-062-greene · *Greene v. Lindsey*, 456 U.S. 444 (1982)
- Script under re-check: `episodes/_planning/EP62_greene_script.en.v004.md` (5,460 narration words)
- Prior revision compared against: `episodes/_planning/EP62_greene_script.en.v002.md`
- Ledger: `episodes/_planning/EP62_greene_FACTS_LEDGER.v001.md` (107 rows, 69 VERBATIM)
- Primary source: `episodes/_planning/measurements/EP62_greene_RAW.md` (CourtListener cluster 110705 — Brennan majority, O'Connor dissent, 10 majority footnotes + 2 dissent footnotes, caption block)
- Contract: `episodes/PD-2026-062-greene/episode_spec.v001.json`
- Craft review that drove the second pass: `episodes/_planning/EP62_greene_CRAFT_REVIEW.v001.md`
- Render: **none yet.** This packet locks the script before assembly (`PD_ONE_PASS_PRODUCTION_SPEC.v2.md` §B item 5). A render receipt does not exist and is not claimed.

---

## 0. Method — what was measured, not asserted

The quotation sweep is mechanical. No quotation was hand-picked.

1. Narration was extracted from v003 by rule: every non-empty line that is not a heading, not a blockquote, not a horizontal rule, not a bold metadata line, not a `【】` direction and not `⟨HELD⟩`. Inline `【】` and `⟨HELD⟩` were stripped from surviving lines. Result: **5,460 words.**
2. Both the narration and the whole RAW opinion were normalised identically:
   - curly quotes `‘ ’ “ ”` → straight; en/em dash, figure dash, minus → `-`; `…` → `...`; NBSP → space; backtick → `'`; `&amp;` → `&`
   - **page markers of the `*447` family removed, including ones glued to a word** (`*446 I`, `*454 "Q.`, `*459 however`) and ones that split a word across a page break (`propri *452 etary rights`, `re *460 mains`)
   - `§` → `section`; everything not a letter, digit, period or space dropped; case folded; whitespace collapsed
3. Every maximal span of ≥ 6 consecutive normalised words in v003 that also occurs in the normalised RAW was found by index lookup. Adjacent spans separated by ≤ 14 words were merged into one quotation region.
4. The same sweep was run on v002, and v002 → v003 was diffed sentence by sentence, so every repair the second pass made is shown with its defect.

**Result of the sweep: 99 verbatim spans / 1,930 matched words / 53 merged quotation regions.** Three regions are identifier matches (proper names, the term *forcible entry and detainer action*), leaving **50 quotation passages**, all listed in §4.

**Disclosure about the source file.** `EP62_greene_RAW.md` contains the opinion **twice** — an OCR pass and a clean pass, separated by `===== OPINION BREAK =====`. The OCR pass carries artefacts (`wdth` for *with*, `Brut-scher`, `de-tainer`, `proforma`, `connnection`, `farther` for *further*, `re mains`). The sweep matched against the union of both; **where the two copies disagree, the clean copy governs**, and every row below was confirmed against the clean copy by eye.

---

## 1. Totals by verdict

| Verdict | Count | Where |
|---|---:|---|
| **LOCKED** | **101** | §2 (10) · §3 (14) · §4 (49 of 50) · §5 (28 of 34) |
| **NEEDS SOURCE** | **5** | §4 (1) · §5 (4) — all itemised in §6 |
| **QUARANTINED** | **2** | §5 — both itemised in §6 |
| **Total claim rows** | **108** | |

Separately: the contract's nine `forbidden_claims` were swept individually against v003 — **9 / 9 clear** (§7).
Two further **attribution flags** and two **micro-deviations** are recorded in §6; none is a false statement, and each has a one-line repair.

---

## 2. The craft review's factual defects — F1–F4 and F5, all resolved

`EP62_greene_CRAFT_REVIEW.v001.md` §2 recorded four factual errors and six minor ones against v002 and ordered them fixed before any craft work. Each is shown with the v002 defect and the v003 wording that replaced it.

### F1 — a count of process servers the opinion does not print

- **Claim as v002 stated it** (v002 L340): *"In this case the evidence was **seven or eight men** describing their rounds, and the Housing Authority telling those men that the papers came off the doors."*
- **Ledger row:** GL-74 · gate G5 ("no number appears that the opinion does not print") · contract `forbidden_claims` (no national/uncounted number).
- **What the opinion says:** the dissent's own word is *"a handful of process servers in Kentucky."* Counting distinct deponents in the text gives at most five (majority n.7 at App. 74 / 80 / 82, n.8 at App. 76; dissent's Bacon, Brutscher, the App. 74 man, the CA6 p. 74 man). No figure appears anywhere.
- **v003 (L345):** *"In this case the evidence was a handful of men describing their rounds, and the Housing Authority telling those men that the papers came off the doors."*
- **Verdict: LOCKED.** `seven or eight` does not occur anywhere in v003.

### F2 — a quotation rewritten so that it stopped answering the dissent

- **Claim as v002 stated it** (v002 L316): *"...can be deemed **adequate — whatever the proceeding is called**."*
- **Ledger row:** GL-62 (opinion n.4).
- **The opinion's own wording:** *"...it is difficult to see how a means of serving process that fails to afford actual notice in a 'not insubstantial' number of cases can be deemed **either prompt or certain**."*
- **v003 (L325):** *"From the perspective of the tenant, it wrote, it is difficult to see how a means of serving process that fails to afford actual notice in a not insubstantial number of cases can be deemed either prompt or certain."*
- **Verdict: LOCKED.** The majority's answer now uses the dissent's own test (*prompt and certain*, GL-76), which is what makes it an answer.

### F3 — a witness's hesitation deleted, with the film's heaviest accusation built on the deletion

- **Claim as v002 stated it** (v002 L160): *"They never took them off when we were present, but the Housing Authority told us that they would take them off, so we always put them up high."* — followed by *"...and the men doing the posting kept posting them."* (v002 L165)
- **Ledger row:** GL-39 (n.7, App. 74) · quarantine Q-07 (overstating the record).
- **The opinion's own wording:** *"They never took them off when we were present, but we, **you know, assume —** the Housing Authority told us that they would take them off, so we always put them up high."*
- **v003 (L153):** the ellipsis is restored verbatim. **v003 (L157):** *"The Housing Authority's own staff had told the men doing the posting that the papers came off the doors."* — the added charge of continuing to post is gone.
- **Verdict: LOCKED.**

### F4 — a social picture with no line of record behind it

- **Claim as v002 stated it** (v002 L130): *"Think about who is behind the doors of a public housing project on a **Tuesday at eleven in the morning**. People at work. People at a **second job**... asleep after a **night shift**... The population most likely to miss a single daytime knock is the population the procedure was **aimed at**."* — plus v002 L99 *"in the middle of a working day."*
- **Ledger row:** verified absence (GL-13, GL-42) · quarantine Q-08 (no motive attribution).
- **What the opinion says:** only that nobody was home in a *"good percentage"* of visits (n.8, App. 76). **It never says the visits were in daytime.**
- **v003 (L123):** *"The record does not say what time of day the deputies came. It says only that in a good percentage of cases, nobody was there."* **v003 (L93)** now ends at *"...when a deputy walked up to a door in a Louisville housing project."*
- **Verdict: LOCKED.**

### F5 — the six minor fixes

| # | v002 defect | The opinion's wording | v003 | Ledger | Verdict |
|---|---|---|---|---|---|
| F5-1 | v002 L242: *"Briefs came in from the National Housing Law Project, and from the Antioch School of Law, urging the Court to affirm."* — *urging affirmance* attached to both | Caption block: Madway for the National Housing Law Project; note [*] *"Lynn E. Cunningham filed a brief for the Antioch School of Law et al. as amici curiae urging affirmance."* | L245: *"David Madway filed a brief for the National Housing Law Project. Lynn Cunningham filed one for the Antioch School of Law, urging the Court to affirm."* | GL-11 | **LOCKED** |
| F5-2 | v002 L242: *"how **every summary eviction in the country** begins"* — a national assertion | The record supports only the dissent's *"at least 11 States"* | L245: *"how a summary eviction begins in every State that served notice this way."* | GL-75 · Q-04 | **LOCKED** |
| F5-3 | v002 L220: *"notices posted on the apartment doors of tenants are often removed."* — **"by other tenants" dropped**, making it read as a story about children | District Court, App. 41-42: *"...are often removed **by other tenants**."* | L221: *"...are often removed by other tenants."* | GL-32 | **LOCKED** |
| F5-4 | v002 L274: *"The **Postal Service** is an efficient and inexpensive means of communication."* — *Postal Service* is the **dissent's** word | Majority: *"the **mails** provide an 'efficient and inexpensive means of communication'"* | L275: *"The mails, it wrote, provide an efficient and inexpensive means of communication."* | GL-59 | **LOCKED** |
| F5-5 | v002 L300: *"On this flimsy basis, the Court overturns the work of the Kentucky Legislature."* — **"confidently" silently dropped** | Dissent: *"the Court **confidently** overturns the work of the Kentucky Legislature and, by implication, that of at least 10 other States."* | L303 restores *confidently*. The trailing clause is dropped, and the count is carried in the same passage at L311 (*"at least 11 States"*), as the review directed | GL-74 · GL-75 | **LOCKED** |
| F5-6 | v002 L265: *"reliance on posting **under this statute**"* | *"reliance on posting **pursuant to the provisions of § 454.030**"* | L269 restores the full clause | GL-56 | **LOCKED** |

**Contract erratum from the craft review, now confirmed closed:** the review flagged `episode_spec.v001.json` `forbidden_claims` as reading *"Pannell Ray"*. Grepped 2026-08-04: the spec reads **Pamela Ray**. No action outstanding.

---

## 3. Quotation alterations found by the mechanical audit, and their repairs

The second pass's quotation audit was recorded as finding **eight further alterations**. Those eight are not itemised anywhere in the repository, so the same audit was **re-run for this packet** on v002 and v003 against RAW. It enumerates **fourteen** quotation alterations outside F1–F5. All fourteen are shown below with the defect and the repair; if the recorded count was eight, the other six were repaired in the same batch without being separately logged. Nothing here is outstanding.

| # | Script line (v002 → v003) | Claim as v002 stated it | The opinion's own wording | v003 wording | Ledger | Verdict |
|---|---|---|---|---|---|---|
| A01 | L83 → L75 | Statute quoted as two sentences: *"...with any member of the defendant's family **over sixteen years of age**. And if no such person is found, he may serve the notice by posting a copy **on a conspicuous part of** the premises."* | *"...with any member of the defendant's family **thereon** over sixteen (16) years of age, and if no such person is found he may serve the notice by posting a copy **thereof in a conspicuous place on** the premises."* | L75 reads the clause continuously and restores *thereon*, *thereof*, and *in a conspicuous place on* | GL-16 | **LOCKED** |
| A02 | L175 → L175 | Brutscher's deposition converted to reported speech: *"One server told the court he had been warned beforehand — that Carter Bacon had told him he suspected..."* | *"I had been warned beforehand that, by Mr. Bacon, Carter Bacon, that he suspected — he wasn't certain, but he suspected that on some occasions the Writs had been torn off the doors by kids."* | L175 restores the deposition verbatim (micro-deviation noted at §6 FLAG-3) | GL-45 | **LOCKED** |
| A03 | L183 → L183 | *"the crews always tried to put the paper up above where a **small child could not reach** — and that he had never had a complaint **about children ripping notices off**, and had never seen a child **try**."* | *"we always try to put the paper up above where, a, **say a small child can't reach it**."* / *"asked whether he had 'had complaints about **small** children ripping them off,' answered that he had never had a complaint and had never seen a child **try to rip a notice off**."* | L183 restores all three | GL-46 | **LOCKED** |
| A04 | L189 → L191 | *"after their opportunity **to** appeal had lapsed"* | *"after their opportunity **for** appeal had lapsed"* | L191: *for* | GL-24 | **LOCKED** |
| A05 | L236 → L237 | The Sixth Circuit's act folded into a participle and paraphrased: *"— **noting** with approval the provisions of the New York counterpart **to the Kentucky statute, under which a copy is also mailed** when notice is served by posting."* | *"**The court then noted** with approval the provisions of the New York counterpart of § 454.030, which provides that when notice is served by posting, **a copy of the petition must be sent by registered or certified mail within a day of** the posting."* | L237 restores n.2 verbatim | GL-37 | **LOCKED** |
| A06 | L270 → L273 | *"**Failure to reach the tenant on one visit**... might be **constitutionally sufficient**."* | *"The **failure to effect personal service on the first visit** hardly suggests that the tenant has abandoned his interest in the apartment such that mere pro forma notice might be **held constitutionally adequate**."* | L273 restores both | GL-58 | **LOCKED** |
| A07 | L268 → L271 | *"**And so** posting on the apartment door **could not** be considered a reliable means..."* | *"**Under these conditions**, notice by posting on the apartment door **cannot** be considered a 'reliable means of acquainting interested parties of the fact that their rights are before the courts.'"* | L271: *"And under these conditions, notice by posting on the apartment door cannot be considered a reliable means..."* | GL-57 | **LOCKED** |
| A08 | L282 → L283 | The holding shortened: *"the State **deprived** them of property **without due process of law**."* | *"the State **has deprived** them of property without **the** due process of law **required by the Fourteenth Amendment**."* | L283 restores the full holding | GL-63 | **LOCKED** |
| A09 | L298 → L301 | Two dissent sentences fused: *"...to posted notice **— and it reaches** this conclusion despite..."* | *"...to posted notice. **The Court reaches** this conclusion despite the total absence of any evidence in the record regarding the speed and reliability of the mails."* | L301 restores the sentence break and *The Court* | GL-73 | **LOCKED** |
| A10 | L314 → L321 | *"**A** forcible entry and detainer action is a summary proceeding for quickly determining **whether** a landlord has the right to immediate possession."* | *"**Kentucky's** forcible entry and detainer action is a summary proceeding for quickly determining **whether or not** a landlord has the right to immediate possession **of leased premises**."* | L321 restores all three | GL-76 | **LOCKED** |
| A11 | L314 → L321 | The *Normet* passage cut to *"speedy adjudication is desirable to prevent subjecting the landlord to undeserved economic loss and the tenant to **unmerited harassment**."* — the economics sentence absent, *and dispossession* dropped | *"**Many expenses of the landlord continue to accrue whether a tenant pays his rent or not.** Speedy adjudication is desirable to prevent subjecting the landlord to undeserved economic loss and the tenant to unmerited harassment **and dispossession** when his lease or rental agreement gives him the right to peaceful and undisturbed possession of the property."* | L321 restores the economics sentence and *and dispossession*, truncating cleanly at that clause boundary. The case name *Lindsey v. Normet* is **not spoken** (Q-10) | GL-77 | **LOCKED** |
| A12 | L327 → L333 | *"— **giving lip service** to the principle that it is not our responsibility to prescribe the form of service, **and then going on** to do just that."* | *"**The Court gives lipservice** to the principle that '[i]t is not our responsibility to prescribe the form of service **that [Kentucky] should adopt**,' ... **but then goes on** to do just that."* | L333 restores the sentence, *that Kentucky should adopt*, and *but then goes on* | GL-82 | **LOCKED** |
| A13 | L320 → L327 | Paraphrase: *"saying it would not resolve the constitutional question on that basis."* | *"As in Mullane, we decline to resolve the constitutional question based upon the determination whether the particular action is more properly characterized as one in rem or in personam."* | L327 restores the sentence verbatim | GL-69 | **LOCKED** |
| A14 | L310 → L317 | *"as far as **the** door"* | *"as far as **the tenant's** door"* | L317: *the tenant's door* | GL-80 | **LOCKED** |

**Repairs made in the same pass that are not alterations** (recorded so the diff is fully accounted for): the App. 74 witness's exculpatory second half was **added** (L185, *"They always put the writs up high — so we never had any problems with that."*, GL-46 / RAW dissent App. 74); *"The District Court had called the same testimony undisputed."* was added at L305 (GL-32 vs GL-74); the *Mullane* n.6 owner presumption was inserted verbatim before the turn (L267, GL-70); the majority's *"in many or perhaps most instances"* sentence was split for breath at L125 **without changing a word** (GL-55).

---

## 4. Mechanical verbatim sweep of v003 — every quotation, confirmed against RAW

All 53 merged regions, in script order. `Q` = quotation, `ID` = identifier match (a proper name or a term of art, not a quotation). Unless a row says otherwise, the passage was confirmed **verbatim** against the clean copy of the opinion after normalisation.

| # | Line | Words | Passage (opening) | Ledger | Locus in RAW | Type | Verdict |
|---|---|---:|---|---|---|---|---|
| 1 | L41 | 28 | *In 1975 the Housing Authority of Louisville… Linnie Lindsey, Barbara Hodgens and Pamela Ray* | GL-01, GL-03 | Part I | ID | **LOCKED** |
| 2 | L51 | 6 | *a forcible entry and detainer action* | GL-14 | opening ¶ | ID | **LOCKED** |
| 3 | L55 | 23 | *the officer of the court who is charged with serving notice…usually a Jefferson County Deputy* | GL-08 | n.1, Brief for Appellants 3 | Q | **LOCKED** |
| 4 | L61 | 34 | *whether this statute, as applied to tenants in a public housing project, fails to afford…* | GL-48 | opening ¶ | Q | **LOCKED** |
| 5 | L69 | 14 | *The fundamental requisite of due process of law is the opportunity to be heard.* | GL-49 | II-A, quoting *Grannis* 234 U.S. at 394 | Q | **LOCKED** |
| 6 | L69 | 31 | *the right to be heard has little reality or worth unless one is informed…* | GL-50 | II-A, quoting *Mullane* at 314 | Q | **LOCKED** |
| 7 | L75 | 75 | *If the officer directed to serve notice…in a conspicuous place on the premises.* | GL-16 | Part I, § 454.030 | Q | **LOCKED** |
| 8 | L79 | 6 | *member of the defendant's family* | GL-16 | Part I | Q | **LOCKED** |
| 9 | L79 | 6 | *he may explain and leave a* | GL-16 | Part I | Q | **LOCKED** |
| 10 | L83 | 13 | *The notice shall state the time and place of meeting of the court.* | GL-16 | Part I | Q | **LOCKED** |
| 11 | L89 | 24 | *notice took the form of posting a copy of the writ of forcible entry and detainer…* | GL-19 | Part I | Q | **LOCKED** |
| 12 | L99 | 22 | *Posting refers to the practice of placing the writ on the property by use of a thumbtack, adhesive tape, or other means.* | GL-17 | n.1 | Q | **LOCKED** |
| 13 | L105-107 | 98 | *First, the officer goes to the apartment…* / *if no one is at home at the time of that visit, as is apparently true in a good percentage of cases* | GL-18, GL-20 | n.1 (brief) + II-B (Court) | Q | **LOCKED** — attribution flag, §6 FLAG-1 |
| 14 | L111 | 36 | *Neither the statute, nor the practice of the process servers, makes provision for even a second attempt…* | GL-21 | II-B | Q | **LOCKED** |
| 15 | L115 | 6 | *we reject appellants' characterization of the* | GL-22 | II-B | Q | **LOCKED** |
| 16 | L123 | 6 | *in a good percentage of cases* | GL-42 | n.8, App. 76 | Q | **LOCKED** |
| 17 | L125 | 52 | *posting notice on the door of a person's home would, in many or perhaps most instances…* | GL-55 | II-B | Q | **LOCKED** |
| 18 | L131 | 12 | *reasonable to assume that a property owner will maintain superintendence of his* | GL-70 | II-B | Q | **LOCKED** |
| 19 | L143 | 20 | *aware of there being any problem with children ripping the writs off* / *Oh, we had plenty of trouble.* | GL-41 | n.7, App. 82 | Q | **LOCKED** |
| 20 | L147-149 | 100 | *I have seen them take them off of the door…* / *Well, probably a couple of times.* | GL-41, GL-40 | n.7, App. 82 and App. 80 | Q | **LOCKED** |
| 21 | L153 | 44 | *The children — we had problems with children…we, you know, assume — the Housing Authority told us…* | GL-39 | n.7, App. 74 | Q | **LOCKED** |
| 22 | L161 | 35 | *As the process servers were well aware, notices posted on apartment doors…* | GL-43 | II-B | Q | **LOCKED** |
| 23 | L175-177 | 89 | *by Mr. Bacon, Carter Bacon, that he suspected…* / *the six months I was working at it…* | GL-45 | dissent, App. in No. 79-3477 (CA6) 112-113 | Q | **LOCKED** — micro-deviation, §6 FLAG-3 |
| 24 | L183 | 52 | *we always try to put the paper up above where, a, say a small child can't reach it.* | GL-46 | dissent, CA6 p. 74 | Q | **LOCKED** |
| 25 | L185 | 8 | *So we never had any problems with that.* | GL-46 | dissent, App. 74 | Q | **LOCKED** |
| 26 | L191 | 31 | *that they did not learn of the proceedings until they were served with writs of possession…* | GL-24 | Part I — **allegation** | Q | **LOCKED** |
| 27 | L193 | 12 | *appellees claim to have suffered precisely such a failure of actual notice.* | GL-25 | II-B | Q | **LOCKED** |
| 28 | L205 | 6 | *thus without recourse in the state* | GL-26 | Part I | Q | **LOCKED** — but see §6 OPEN-2 (the narrator's word-count around it) |
| 29 | L209 | 17 | *did not satisfy the minimum standards of constitutionally adequate notice described in Mullane…* | GL-29 | Part I | Q | **LOCKED** |
| 30 | L215 | 12 | *On cross-motions for summary judgment, the District Court granted judgment for* | GL-30 | Part I | Q | **LOCKED** |
| 31 | L217 | 36 | *on the ground that it was reasonable for the State to presume that a notice posted on the door…* | GL-31 | Part I (*Weber*) | Q | **LOCKED** |
| 32 | L221 | 19 | *undisputed testimony in this case that notices posted on the apartment doors of tenants are often removed by other* | GL-32 | Part I, App. 41-42 | Q | **LOCKED** |
| 33 | L223 | 15 | *that posting only comes into play after the officer cannot find the defendant on the* | GL-33 | Part I, App. 42 | Q | **LOCKED** |
| 34 | L231-233 | 52 | *there may have been a time when posting provided a surer means…That time has passed. The uncontradicted testimony by process servers themselves **establishes it**.* | GL-35, GL-34 | Part I, 649 F.2d at 428 | Q | **NEEDS SOURCE** — §6 OPEN-6 |
| 35 | L235-237 | 77 | *Requiring Kentucky to provide notice by mail…The court then noted with approval the provisions of the New York counterpart…* | GL-36, GL-37 | n.2 | Q | **LOCKED** — truncated at *"The cost will be minimal."*, a clause boundary; no meaning change |
| 36 | L245 | 20 | *Madway filed a brief for the National Housing Law Project. Lynn Cunningham filed one for the Antioch School of Law* | GL-11 | caption block + note [*] | Q | **LOCKED** |
| 37 | L247 | 7 | *personal service would be required by Kentucky* | GL-72 | II-B, Tr. of Oral Arg. 19-21 | Q | **LOCKED** |
| 38 | L255 | 34 | *An elementary and fundamental requirement of due process in any proceeding which is to be accorded finality…* | GL-51 | II-A, quoting *Mullane* at 314 | Q | **LOCKED** |
| 39 | L259-263 | 75 | *In this case, appellees have been deprived of a significant interest in property…* / *effect must be judged in the light of its practical application…* | GL-52, GL-53, GL-54 | II-B | Q | **LOCKED** — *"A procedure's effect"* supplies the antecedent for the opinion's *"its effect"*; no meaning change |
| 40 | L267-273 | 234 | *The ways of an owner with tangible property…* / *But whatever the efficacy of posting in many cases…* / *cannot be considered a reliable means…* / *hardly suggests that the tenant has abandoned his interest…* | GL-70, GL-56, GL-57, GL-58 | n.6 (*Mullane* at 316) + II-B | Q | **LOCKED** — the film's spine (`FILM_BIBLE` §11) confirmed word for word |
| 41 | L275 | 76 | *provide an efficient and inexpensive means of communication.* / *Particularly where the subject matter of the action also happens to be the mailing address…* | GL-59, GL-60 | II-B | Q | **LOCKED** |
| 42 | L279-285 | 72 | *the State's continued exclusive reliance on an ineffective means of service…* / the holding | GL-61, GL-63 | II-B + Part III | Q | **LOCKED** |
| 43 | L285-289 | 79 | *In light of the findings of the courts below, we hold only that posted notice pursuant to § 454.030 is constitutionally inadequate.* / *It is not our responsibility to prescribe the form of service…* | GL-66, GL-67, GL-68 | n.9 | Q | **LOCKED** |
| 44 | L291 | 14 | *that posted service accompanied by mail service is constitutionally preferable to posted service alone.* | GL-68 | n.9 | Q | **LOCKED** |
| 45 | L295 | 7 | *Linnie Lindsey, Barbara Hodgens and Pamela Ray* | GL-01 | Part I | ID | **LOCKED** |
| 46 | L301-303 | 78 | *Today, the Court holds that the Constitution prefers the use of the Postal Service…* / *the scant and conflicting testimony of a handful of process servers…* | GL-73, GL-74 | dissent, opening | Q | **LOCKED** |
| 47 | L307-311 | 57 | *does not cite a single case, other than the decision below…* / *at least 11 States authorizing notice in summary eviction proceedings…* | GL-79, GL-75 | dissent + dissent n.1 | Q | **LOCKED** |
| 48 | L317 | 32 | *It is no secret, after all, that unattended mailboxes are subject to plunder by thieves.* / *at least gives assurance that the notice has gotten as far as the tenant's door.* | GL-80 | dissent | Q | **LOCKED** — *"Moreover, unlike the use of the mails, posting notice"* compressed to *"Posting, at least,"*; the narration already frames it as the dissent's counter to the mails |
| 49 | L321 | 27 | *Kentucky's forcible entry and detainer action is a summary proceeding for quickly determining…* | GL-76 | dissent | Q | **LOCKED** |
| 50 | L321-323 | 45 | *Many expenses of the landlord continue to accrue…* / *The means chosen for making service of process* | GL-77, GL-76 | dissent, quoting *Normet* 405 U.S. at 72-73 | Q | **LOCKED** — case name deliberately unspoken (Q-10) |
| 51 | L325 | 39 | *From the perspective of the tenant…can be deemed either prompt or certain.* | GL-62 | n.4 | Q | **LOCKED** |
| 52 | L327 | 29 | *As in Mullane, we decline to resolve the constitutional question…in rem or in personam.* | GL-69 | II-B | Q | **LOCKED** |
| 53 | L333-335 | 85 | *seems to forget that we have long since discarded the concept…* / *The Court gives lipservice…* / *The dissent misconstrues the constitutional standard.* | GL-81, GL-82, GL-83 | dissent + n.9 | Q | **LOCKED** |

**Reported speech, checked and accepted.** Where the script converts a deposition question into narration (L143 *"was asked whether he was aware of…"*, L147 *"Asked whether he had ever seen it"*, L183 *"Asked whether he had had complaints…"*), the quoted words inside remain the opinion's. This is the form the opinion itself uses at App. 74 in the dissent, and it is what allows the passages to be spoken without reading "Q." and "A." aloud.

**Bracket restored to the deponent's word.** At L153 the script says *"They would take **them** off"* where the reporter printed *"They would take **[the writs]** off."* The bracket marks the reporter's insertion; the script restores the pronoun the witness said. **LOCKED.**

---

## 5. Non-quotation factual claims

Claims the narrator makes in his own words. Every one traced to a ledger row or to a verified absence.

| # | Line | Claim as the script states it | Ledger | Verdict |
|---|---|---|---|---|
| N01 | L21 | HOOK: Kentucky said a paper taped to a door was service; the men who taped it up were asked, under oath, whether it stayed there | GL-16, GL-17, GL-19, GL-39/40/41 (depositions) | **LOCKED** |
| N02 | L31 | *"Greene is the sheriff. Lindsey is a tenant."* | GL-06, GL-01 | **LOCKED** |
| N03 | L41 | The opinion names the three once; 1975; the Housing Authority of Louisville began proceedings | GL-01, GL-03, GL-13 | **LOCKED** |
| N04 | L43 | *"No ages. No jobs. No families… Three names and a shared address."* | GL-13 (verified absence) | **LOCKED** |
| N05 | L47 | Officer knocks, nobody answers, paper is fixed to the door; once on the door the tenant had been served; the hearing would happen regardless | GL-16, GL-18, GL-19, GL-24 | **LOCKED** |
| N06 | L49 | *"Three tenants said that is exactly what happened to them… That is their account."* | GL-23, GL-24 — allegation, correctly framed | **LOCKED** |
| N07 | L51 | *"Kentucky, **like most States**, wanted these cases resolved in **weeks rather than months**, and built the procedure accordingly."* | — | **NEEDS SOURCE** — §6 OPEN-3 |
| N08 | L53 | Joseph Greene was the Jefferson County Sheriff; his deputies carried the writs; the Housing Authority and public officials were also named | GL-05, GL-06, GL-07 | **LOCKED** |
| N09 | L59 | The landlord was a government body; the men who carried the paper were sworn officers | GL-02, GL-03, GL-04, GL-05 | **LOCKED** |
| N10 | L73 | *"[§ 454.030] is **three sentences long**"* | GL-16 | **QUARANTINED** — §6 OPEN-1 |
| N11 | L77-81 | Three descending steps; the middle step assumes somebody home; the statute tells the officer to explain | GL-16 | **LOCKED** |
| N12 | L89 | *"For all three women it went all the way down. Three doors."* | GL-19 | **LOCKED** |
| N13 | L109 | *"…step three happens, and the officer is **back in the car**."* | — | **NEEDS SOURCE** — §6 OPEN-7 |
| N14 | L121 | *"a good percentage"* is not the Court's estimate; it sits in a footnote pointing at a deposition | GL-42, n.8 | **LOCKED** |
| N15 | L123 | *"The record does not say what time of day the deputies came."* | verified absence (F4 repair) | **LOCKED** |
| N16 | L151 | Two men deposed separately named the same development; the dissent names the second Carter Bacon | GL-09, GL-40, GL-44 | **LOCKED** |
| N17 | L169 | The Court wrote no percentage — *not infrequently*, *a significant number of instances*; there is no count because nobody had counted | GL-43, GL-56, ledger §5 preface | **LOCKED** |
| N18 | L171 | *"The majority did not weigh the servers' testimony against a study, or a survey, or a count. There was nothing else to weigh it against."* | ledger §5 preface (verified absence) | **LOCKED** |
| N19 | L181 | *"That man was Gilbert Brutscher"*; the dissent set his answer against Bacon's | GL-44, GL-45 | **LOCKED** |
| N20 | L185 | *"The majority quoted the first half. The dissent quoted the second."* | GL-39 (App. 74, majority n.7) vs dissent's use of App. 74 | **LOCKED** |
| N21 | L199 | The case arrived on summary judgment; what is established is the practice, what is alleged and never tested is the three apartments | GL-27, GL-30, GL-34 | **LOCKED** |
| N22 | L205 | *"The Court's phrase for their position is **four words long**: thus without recourse in the state courts."* | GL-26 | **QUARANTINED** — §6 OPEN-2 |
| N23 | L207 | *"section 1983 — the **Reconstruction-era** statute that lets a citizen sue a state official…"* | GL-28 covers § 1983; not the characterisation | **NEEDS SOURCE** — §6 OPEN-4 |
| N24 | L217-219 | *Weber*, Sixth Circuit, some seventy years earlier; *"That was 1909."* | GL-31 | **LOCKED** |
| N25 | L241 | Took the appeal in 1981; argued 23 February 1982; decided that May; docket No. 81-341 on screen | GL-12, GL-38 | **LOCKED** |
| N26 | L245 | Hoge for the sheriff and officials; Smith for the tenants; Madway and Cunningham amici | GL-10, GL-11 | **LOCKED** |
| N27 | L255 | *"It came from that 1950 case about **notifying beneficiaries of a trust**"* | GL-51 quotes *Mullane*; the description of *Mullane*'s facts is outside *Greene* | **NEEDS SOURCE** — §6 OPEN-5 |
| N28 | L285-291 | The Court did not ban posting; did not order the mail; went only as far as comparative preference | GL-66, GL-67, GL-68 | **LOCKED** |
| N29 | L295 | Affirmed a reversal and a remand; *"What became of Linnie Lindsey, Barbara Hodgens and Pamela Ray is not in the opinion."* | GL-71, GL-27 | **LOCKED** |
| N30 | L299 | Dissent by O'Connor, joined by the Chief Justice and Rehnquist; *"The opinion prints no tally of the votes on the other side."* | GL-65 · Q-13 respected | **LOCKED** |
| N31 | L311 | *"Eleven States"*, listed on screen, not read aloud | GL-75 | **LOCKED** |
| N32 | L347 | *"the three dissenting Justices said so"*; *"on this record, the only evidence anybody brought"* | GL-65, GL-74, ledger §5 preface | **LOCKED** |
| N33 | L353 | *"Somewhere in Louisville in 1975 a deputy pressed a strip of tape onto a painted door."* | GL-17, GL-19 — reconstruction, hedged by *Somewhere* | **LOCKED** |
| N34 | L157 | *"Not a discovery made by the tenants' lawyers. Not something dragged out of a reluctant witness."* | — | **LOCKED** — attribution flag, §6 FLAG-2 |

---

## 6. Still open — do not render until these are closed

> An honest NEEDS SOURCE is worth more than a confident LOCKED. Every item below survived **both** passes; none of them was in the craft review, and none would have been caught by any machine gate now in the repository.

### QUARANTINED — contradicted by the primary source

**OPEN-1 · L73 — "It is three sentences long."**
§ 454.030 as the opinion prints it is **two** sentences: the long conditional clause ending *"…in a conspicuous place on the premises."*, and *"The notice shall state the time and place of meeting of the court."* The script itself quotes exactly two (L75 and L83) and at L83 introduces the second as *"one more sentence."* Nothing in RAW or in GL-16 supports three.
**Repair:** `three` → `two`. One word. Nothing else in the passage moves.

**OPEN-2 · L205 — "The Court's phrase for their position is four words long: thus without recourse in the state courts."**
The quoted phrase is **seven** words (*thus without recourse in the state courts*), six without *thus*. The script contradicts itself in the same sentence.
**Repair:** drop the count — *"The Court's phrase for their position is six words long: without recourse in the state courts."*, or simply *"The Court has a phrase for their position: thus without recourse in the state courts."* The second option removes the arithmetic entirely and is safer.

### NEEDS SOURCE — no ledger row supports the wording as spoken

**OPEN-3 · L51 — "Kentucky, like most States, wanted these cases resolved in weeks rather than months."**
Neither *most States* nor *weeks rather than months* appears in the opinion. The record supports only that the FED action is a summary proceeding (GL-76) and that the dissent counted *at least 11 States* authorising posting (GL-75) — which is not "most", and is about service, not speed. The claim also sits next to quarantine Q-04 (no national number).
**Repair:** cut to what the record has — *"The proceeding was a forcible entry and detainer action — the summary process a landlord uses to get possession back quickly. Speed is the point of it."* — and stop. Or source *most States* independently and add a ledger row.

**OPEN-4 · L207 — "section 1983 — the Reconstruction-era statute…"**
GL-28 supports the § 1983 class action. *Reconstruction-era* is external knowledge (Civil Rights Act of 1871) and appears nowhere in *Greene*. It is very likely true and very cheap to fix.
**Repair:** either add a ledger row citing 42 U.S.C. § 1983 / Act of April 20, 1871, or say *"the federal statute that lets a citizen sue a state official for violating a constitutional right"* and drop the date.

**OPEN-5 · L255 — "that 1950 case about notifying beneficiaries of a trust."**
Research instruction **GL-R8** is explicit: the film may quote or characterise *Mullane* **only through the passages quoted inside *Greene*** until *Mullane* is read in full. *Greene* never says what *Mullane* was about. The characterisation is accurate to *Mullane* (notice to beneficiaries of a common trust fund) but is not sourced in this packet.
**Repair:** read 339 U.S. 306 and add a ledger row, or say *"that 1950 decision"* and let L209's full case name carry it.

**OPEN-6 · L231 — "The uncontradicted testimony by process servers themselves establishes it."**
The sentence is introduced as the Sixth Circuit's — *"Its line is the sharpest sentence in the whole history of the case"* — and the first two thirds are verbatim (GL-35). The last three words are the narrator's. The court wrote: *"The uncontradicted testimony by process servers themselves **that posted summonses are not infrequently removed by persons other than those served constitutes effective confirmation of the conclusion that notice by posting 'is not reasonably calculated to reach those who could easily be informed by other means at hand.'"***
The meaning is preserved; the words are not. This is the same defect class as F2, and it survived both passes.
**Repair:** end the attributed quotation at *"That time has passed."* and let the narrator's sentence stand separately — *"The record it pointed at was the process servers' own testimony."* — or restore the clause verbatim.

**OPEN-7 · L109 — "and the officer is back in the car."**
There is no vehicle anywhere in the opinion, the footnotes, or the depositions quoted. Minor, but it is invention inside a passage whose whole authority is that it only repeats the record.
**Repair:** *"So step two evaporates, step three happens, and the visit is over."*

### Attribution flags and micro-deviations — no false statement, but fix before the voice record

**FLAG-1 · L105-107 — who is speaking.**
L105 introduces the three-step ladder as *"in the words of the brief filed for the sheriff"* (correct, n.1). L107 then says *"And then the sentence that undoes it"* and delivers *"If no one is at home at the time of that visit, as is apparently true in a good percentage of cases, posting follows forthwith."* — which is the **Court's** sentence in Part II-B (GL-20), not the brief's. A listener will hear it as the next sentence of the brief.
**Repair:** three words — *"And then the Court's own sentence, the one that undoes it."*

**FLAG-2 · L157 — how the testimony was obtained.**
*"Not a discovery made by the tenants' lawyers. Not something dragged out of a reluctant witness."* The opinion does not say who took the depositions or how the witnesses behaved. Nothing false is asserted, but both sentences are outside the record.
**Repair:** delete both; L155-157 lands harder without them.

**FLAG-3 · L175 — a stumble smoothed.**
RAW: *"I had been warned beforehand **that**, by Mr. Bacon, Carter Bacon, that he suspected…"* The script drops the first *that*. This is the same class as F3 (deleting a witness's hesitation), at a much smaller scale.
**Repair:** restore the word, or leave it and record the deviation here — which this row does.

---

## 7. Contract `forbidden_claims` — swept individually against v003

| # | Forbidden claim | Sweep result |
|---|---|---|
| 1 | *"today a landlord can still just tape a paper to your door"* / any present-day claim | **Clear.** The only *today* in v003 is inside the dissent's opening quotation (L301). No present-tense claim about current law anywhere. |
| 2 | *"every State now has to mail eviction notices"* | **Clear.** L289 states the opposite verbatim (GL-67). |
| 3 | *"The Supreme Court banned posting."* | **Clear.** L285: *"The Court did not ban posting."* The word *banned* does not occur. |
| 4 | Any national number | **Clear** of counts. Every number in v003 is from the record: 1975, 1914, 1950, 1909, 1981, 1982, § 454.030, No. 81-341, sixteen, seventy years, six months, eleven States. **But see OPEN-3** — *most States* / *weeks rather than months* is the nearest thing to a violation and is why this packet is not a clean pass. |
| 5 | *"They lost their homes"* / any account of what became of the three | **Clear.** L295 refuses explicitly. |
| 6 | *"She never saw the notice"* as established fact | **Clear.** L191-193 keep the Court's verbs (*claimed*, *stated*, *claim to have suffered*); L199 says the question was never tried. The reserve thumbnail title keeps *They Say*. |
| 7 | Any claim about the landlord's motive | **Clear.** v002's *"The State took more care to find you when it wanted your money than when it wanted your home"* was deleted; L249 keeps only *"Money got a person served. The apartment did not."* (GL-72). |
| 8 | Confusing *Lindsey v. Normet* with appellee Linnie Lindsey | **Clear.** *Normet* does not occur in v003. Its quotation at L321 is attributed as *"the Court's own earlier reasoning"* with no case name (Q-10). |
| 9 | *"The tenants won their case"* | **Clear.** L295: *"Affirmed does not mean three tenants walked out holding a key."* |

---

## 8. Sources

- *Greene v. Lindsey*, 456 U.S. 444 (1982) — full text, both opinions, all footnotes and caption block: `episodes/_planning/measurements/EP62_greene_RAW.md` (CourtListener cluster 110705)
- Facts ledger, 107 rows: `episodes/_planning/EP62_greene_FACTS_LEDGER.v001.md`
- Machine contract: `episodes/PD-2026-062-greene/episode_spec.v001.json`
- Craft review that ordered the second pass: `episodes/_planning/EP62_greene_CRAFT_REVIEW.v001.md`
- Film bible (what the film may and may not say, §12): `episodes/_planning/EP62_greene_FILM_BIBLE.v001.md`

**Not consulted, and not needed for anything above:** *Mullane* 339 U.S. 306, *Lindsey v. Normet* 405 U.S. 56, *Weber* 169 F. 522, 649 F.2d 425. Every reference to them in v003 comes through the *Greene* text. The single place this constrains the script is OPEN-5.

---

## 9. What has to happen before this script goes to voice

1. Close **OPEN-1** and **OPEN-2** (two-word and one-clause fixes; both are contradicted by the script's own quotations).
2. Decide **OPEN-3**, **OPEN-4**, **OPEN-5**, **OPEN-6**, **OPEN-7** — each is either a cut or a new ledger row. None requires rewriting a section.
3. Apply **FLAG-1**, **FLAG-2**, **FLAG-3** in the same batch (`feedback_no_wasted_cycles`: all fixes in one pass, never two).
4. Re-run the sweep in §0 on the resulting v004 and confirm the region count does not fall — a repair that removes a verbatim span is a repair that lost the record.
5. Re-derive `mandatory_stills` only if a `【】` direction changes. None of the fixes above touches one.

*v001 · 2026-08-04 · quotation sweep is mechanical (99 spans / 1,930 words / 53 regions, min 6-word match, normalised); factual rows are hand-traced to the ledger. Self-reported QC is not a verdict — every LOCKED above names the ledger row and the locus in the opinion that supports it.*
