# EP67 · TRANSUNION LLC v. RAMIREZ — FACTS LEDGER v001

**Episode:** EP67 · ID `PD-2026-067-ramirez` · slug `ramirez` · working title「あなたの名前が、テロリストのリストと一致した」
**Case:** *TransUnion LLC v. Sergio L. Ramirez*, No. 20–297, **594 U.S. 413 (2021)**, decided **25 June 2021**.
**Purpose:** every factual claim the film may make, with its grade and its source.

**Invariant 1: no unsupported factual statement enters an approved script.** A claim graded ○ may not be
spoken, shown, put in a telop, or written into a title until it is upgraded.

**Grades:** ✓ **VERBATIM** = quoted word-for-word from a document retrieved and read by this pass, located
by exact string search · ✓ = established from a primary source retrieved by this pass · ○ = research
instruction, **NOT a fact** · ⛔ = quarantined, do not use.

---

## PRIMARY SOURCES — and, for this pass, the ONLY sources

| Tag | Document | Retrieved this pass |
|---|---|---|
| **TU** | *TransUnion LLC v. Ramirez*, No. 20–297, **slip opinion**, Supreme Court of the United States, 25 June 2021 (majority, Thomas dissent, Kagan dissent — complete) | **YES.** `supremecourt.gov/opinions/20pdf/20-297_4g25.pdf` → 108,182 chars |
| **CA9** | *Ramirez v. TransUnion LLC*, No. 17-17244, **951 F.3d 1008** (9th Cir., filed 27 Feb 2020) — the opinion below, carrying the trial record | **YES.** `cdn.ca9.uscourts.gov/datastore/opinions/2020/02/27/17-17244.pdf` → 99,274 chars |
| **OFAC** | Eight U.S. Treasury / OFAC pages (FAQ 5, FAQ topics 1631 / 1636 / 1646 / 1516 / 1591, Sanctions List Search, SDN data specification) | **YES.** Saved as HTML, tag-stripped to `.txt` |
| **SDN.CSV** | OFAC's published SDN data file, `treasury.gov/ofac/downloads/sdn.csv`, `Last-Modified: Fri, 07 Aug 2026` | **YES.** 5,632,887 bytes |

Cached under `episodes/PD-2026-067-ramirez/01_research/sources/`:
`SRC-0001_scotus_20-297_slip.txt` (sha256 `e68aec27c6d6f514…`) ·
`SRC-0002_ca9_17-17244.txt` (sha256 `2dab73f9ef0a6117…`) · `ofac/*.txt`
Machine verifier: `verify_quotes.v001.py` · offsets: `verified_offsets.v001.json`

**Citation convention.** `@NNNNN` is the **character offset of the first character of the quoted string
inside the cached text file** named in the row. **Every ✓ VERBATIM row in this ledger was located by exact
string search during this pass and the verifier re-runs green (74/74).** A quotation that could not be
located that way is not in this ledger — two of my own transcriptions failed the verifier on the first run
and were corrected against the source rather than kept.

---

## ⚠ THE EXTRACTION TRAP — read this before quoting anything

**The text cache inherited by this pass was corrupt in a way that is invisible unless you look for it.**
It was extracted from the official *preliminary print* PDF (`594us2r59_197d.pdf`), and **that PDF's font
has no Unicode mapping for the `fi` ligature, so every `fi` was silently dropped**:

| In the real opinion | In the inherited cache | count |
|---|---|---|
| `files` | `fles` | 34 |
| `first` | `frst` | 17 |
| `find` | `fnd` | 4 |
| `specific` | `specifc` | 6 |

`files`, `first` and `find` each occurred **zero** times in that cache. Both `pdftotext` and `pypdf`
reproduce the fault, because the fault is in the PDF. A "verbatim" quotation taken from it would have
been misspelled — and the phrase at the centre of this episode, ***credit files***, is one of the
casualties.

**Fix applied:** the **slip opinion** (`20-297_4g25.pdf`) is a different typesetting of the same text and
extracts cleanly (`files` 36, `first` 17). It was cross-checked against the preliminary print on every
load-bearing figure — `8,185` (13 vs 13), `1,853` (17 vs 17), `6,332` (22 vs 22), `OFAC` (70 vs 70) — and
is substantively identical. **The slip opinion is the quotation base for this ledger.** For the official
U.S. Reports pagination, cite **594 U.S. 413 (2021)**; the slip's internal page numbers are not U.S.
Reports pages. Do not re-introduce the preliminary-print cache.

---

## 0. GATE STATUS

| # | Gate | Status |
|---|---|---|
| 1 | Read the Supreme Court majority end to end | **DONE.** |
| 2 | Read the Thomas dissent end to end | **DONE.** 19 slip pages. |
| 3 | Read the Kagan dissent end to end | **DONE.** 3 slip pages. |
| 4 | Retrieve the Ninth Circuit opinion below (the trial record, the jury award) | **DONE.** Full text. |
| 5 | OFAC SDN mechanics from official Treasury sources | **DONE.** 8 pages + the SDN data file. Independently re-verified by exact string search against the saved files, not taken on the researcher's word. |
| 6 | Judge McKeown's partial dissent in the Ninth Circuit | **PARTIAL (○-01).** Its holding is recorded from the court-staff summary and from the majority's citations. The separate opinion itself was **not read line by line** this pass. |
| 7 | The district court opinions (301 F.R.D. 408; 2016 WL 6070490) | **NOT RETRIEVED (○-02).** Known only as the Supreme Court and Ninth Circuit describe them. |
| 8 | *Cortez v. Trans Union, LLC*, 617 F.3d 688 (3d Cir. 2010) — the prior warning | **NOT RETRIEVED (○-03).** Everything recorded about it comes from TU and CA9 describing it. That is enough to say TransUnion was warned; it is not enough to narrate Cortez's own story. |
| 9 | What happened **on remand** after 25 June 2021 | **OPEN (○-04).** Not in either document. **CourtListener returned HTTP 429 (quota exceeded) on this pass** — see ⛔-12. |
| 10 | Living, named parties: **TransUnion LLC** (corporation), **Sergio L. Ramirez** (private individual) | **CONSTRAINED.** Rules at ⛔-05 through ⛔-09. |
| 11 | The unnamed Nissan salesman / dealership employee | **PERMANENTLY CLOSED.** Never named, never characterised. ⛔-08. |

---

## 1. IDENTITY AND POSTURE

| ID | Claim | Grade | Source |
|---|---|---|---|
| ID-01 | The case is *TransUnion LLC, Petitioner v. Sergio L. Ramirez*, **No. 20–297**, on writ of certiorari to the United States Court of Appeals for the Ninth Circuit, decided **[June 25, 2021]**. Official citation **594 U.S. 413 (2021)**. | ✓ | TU @9450 (`[June 25, 2021]`), caption block @9200–9470 |
| ID-02 | ✓ **"JUSTICE KAVANAUGH delivered the opinion of the Court."** | ✓ VERBATIM | TU @9466 |
| ID-03 | **The lineup, in full:** ✓ **"KAVANAUGH, J., delivered the opinion of the Court, in which ROBERTS, C. J., and ALITO, GORSUCH, and BARRETT, JJ., joined. THOMAS, J., filed a dissenting opinion, in which BREYER, SOTOMAYOR, and KAGAN, JJ., joined. KAGAN, J., filed a dissenting opinion, in which BREYER and SOTOMAYOR, JJ., joined."** | ✓ VERBATIM | TU @8511 |
| ID-04 | **Therefore the decision was 5–4, not 6–3.** Five justices in the majority (Kavanaugh, Roberts, Alito, Gorsuch, Barrett); four in dissent (Thomas, Breyer, Sotomayor, Kagan). Thomas's own closing counts them: ✓ **"four Members of this Court."** | ✓ | Arithmetic on ID-03 + TU @102152. See ⛔-01. |
| ID-05 | The judgment below was **951 F. 3d 1008, reversed and remanded**. | ✓ VERBATIM | TU @8472 |
| ID-06 | The Ninth Circuit opinion was ✓ **"Filed February 27, 2020"**, before ✓ **"M. Margaret McKeown, William A. Fletcher, and Mary H. Murguia, Circuit Judges."** | ✓ VERBATIM | CA9 @402, @426 |
| ID-07 | ✓ **"Opinion by Judge Murguia; Partial Concurrence and Partial Dissent by"** Judge McKeown. The Ninth Circuit was therefore **not unanimous**. | ✓ VERBATIM | CA9 @513 |
| ID-08 | Ramirez sued in **February 2012**; the class was certified by the U.S. District Court for the Northern District of California, **301 F. R. D. 408 (2014)**; the District Court ruled all 8,185 had standing, **2016 WL 6070490 (Oct. 17, 2016)**. | ✓ | TU @18100–18400 |

**8 rows, 5 with a verbatim quotation.**

---

## 2. THE LIST, AND THE PRODUCT BUILT ON TOP OF IT

### 2a. What OFAC's list is — Treasury's own words

| ID | Claim | Grade | Source |
|---|---|---|---|
| LS-01 | ✓ **"As part of its enforcement efforts, OFAC publishes a list of individuals and companies owned or controlled by, or acting for or on behalf of, targeted countries. It also lists individuals, groups, and entities, such as terrorists and narcotics traffickers designated under programs that are not country-specific. Collectively, such individuals and companies are called 'Specially Designated Nationals' or 'SDNs.'"** | ✓ VERBATIM | `ofac/ofac_faqs_topic_1631_sdn.txt` @1919 · ofac.treasury.gov/faqs/topic/1631 |
| LS-02 | ✓ **"Their assets are blocked and U.S. persons are generally prohibited from dealing with them."** | ✓ VERBATIM | same file @2332 |
| LS-03 | ✓ **"U.S. persons are prohibited from engaging in any transactions with SDNs and must block any property in their possession or under their control in which an SDN has an interest."** | ✓ VERBATIM | same file @4723 |
| LS-04 | **The Supreme Court's own description**, which the film may prefer for economy: ✓ **"OFAC maintains a list of 'specially designated nationals' who threaten America's national security. Individuals on the OFAC list are terrorists, drug traffickers, or other serious criminals. It is generally unlawful to transact business with any person on the list."** | ✓ VERBATIM | TU @14119 |
| LS-05 | **How big the list is.** Treasury states **no current entry count** on any page retrieved. The only official figure obtained is from the 2021 Sanctions Review — ✓ **"the over 12,000 OFAC designations"** — which is a **2021 cumulative designations** figure, not a live list size. A count of Treasury's own published `sdn.csv` of **7 August 2026** yields **19,199 records** (7,479 `individual`, 1,524 `vessel`, 342 `aircraft`, 9,854 entities), **independently reproduced by this pass**. | ✓ (quote) + ✓ (own arithmetic, labelled) | `ofac/treasury_2021_sanctions_review.txt` @6908 · `ofac_sdn.csv`. **See ⛔-11 — the 19,199 is our count of Treasury's file, never "Treasury says".** |

### 2b. What OFAC says a screener must do — the pivot of the episode

| ID | Claim | Grade | Source |
|---|---|---|---|
| LS-06 | **OFAC's own procedure says a name-only match is not a match.** ✓ **"Step 3. How much of the listed entry's name is matching against the name in your transaction? Is just one of two or more names matching (i.e., just the last name)? If yes, you do not have a valid match."** | ✓ VERBATIM | `ofac/ofac_faq_5.txt` @3864 · ofac.treasury.gov/faqs/5 |
| LS-07 | ✓ **"Step 4. Compare the complete sanctions list entry with all of the information you have on the matching name in your transaction."** … ✓ **"Are you missing a lot of this information for the name in your transaction? If yes, go back and get more information and then compare your complete information against the entry."** | ✓ VERBATIM | same file @4103 |
| LS-08 | **What OFAC publishes for each entry — the identifiers that were available to be compared:** ✓ **"An entry often will have, for example, a full name, address, nationality, passport, tax ID or cedula number, place of birth, date of birth, former names and aliases."** | ✓ VERBATIM | same file @4232 |
| LS-09 | ✓ **"A 'weak AKA' is a term for a relatively broad or generic alias that may generate a large volume of false hits when such names are run through a computer-based screening system."** — OFAC's own acknowledgement that name screening produces false hits. | ✓ VERBATIM | `ofac/ofac_faqs_topic_1646_weak_alias.txt` @1850 |
| LS-10 | **OFAC's guidance written for the consumer whose credit report carries an alert:** ✓ **"It is merely a reminder to the person checking your credit that he or she should verify whether you are the individual on one of OFAC's sanctions lists by comparing your information to the OFAC information. If you are not the individual on the sanctions list, the person checking your credit should disregard the OFAC alert."** | ✓ VERBATIM | `ofac/ofac_faqs_topic_1516_credit_report.txt` @2547 |
| LS-11 | OFAC's own search tool carries a disclaimer: ✓ **"use of Sanctions List Search is not a substitute for undertaking appropriate due diligence."** It ✓ **"uses approximate string matching"**, and its scoring runs on ✓ **"Jaro-Winkler, a string difference algorithm, and Soundex, a phonetic algorithm."** | ✓ VERBATIM | `ofac/ofac_sanctions_search.txt` @1632, @742 · `ofac/ofac_faqs_topic_1636_search.txt` @4146 |
| LS-12 | OFAC's data release is **three linked tables** — a main SDN file, **a file of addresses**, and **a file of alternate names** — i.e. the identifiers are published as structured, machine-readable fields, not buried in prose. | ✓ | `ofac/ofac_sdn_dat_spec.txt` (the sentence contains internal line breaks; search `consist of three`) |

### 2c. TransUnion's product

| ID | Claim | Grade | Source |
|---|---|---|---|
| LS-13 | ✓ **"Beginning in 2002, TransUnion introduced an add-on product called OFAC Name Screen Alert."** | ✓ VERBATIM | TU @1162 |
| LS-14 | ✓ **"If the consumer's first and last name matched the first and last name of an individual on OFAC's list, then TransUnion would place an alert on the credit report indicating that the consumer's name was a 'potential match' to a name on the OFAC list. TransUnion did not compare any data other than first and last names."** | ✓ VERBATIM | TU @14871 |
| LS-15 | ✓ **"Unsurprisingly, TransUnion's Name Screen product generated many false positives. Thousands of law-abiding Americans happen to share a first and last name with one of the terrorists, drug traffickers, or serious criminals on OFAC's list of specially designated nationals."** | ✓ VERBATIM | TU @15189 |
| LS-16 | **The matching software, named:** ✓ **"Accuity's software conducted a 'name-only' search, running a consumer's first and last name against the names on the OFAC list. A search would result in a match if the consumer's first and last name were either identical or similar to a name on the OFAC list (e.g., 'Cortez' would match with 'Cortes')."** | ✓ VERBATIM | CA9 @16677 |
| LS-17 | **The comparison that decides the case, from the Ninth Circuit's footnote 2:** ✓ **"In collecting other types of data for use on consumer reports—such as tax liens or bankruptcy judgments—TransUnion used at least one additional identifier other than the consumer's name (e.g., address, date of birth, or social security number). OFAC information was the only consumer-report data that TransUnion collected using name alone."** | ✓ VERBATIM | CA9 @17528 |
| LS-18 | **Thomas, on the same point:** ✓ **"TransUnion did not compare birth dates, middle initials, Social Security numbers, or any other available identifier routinely used to collect and verify credit-report data."** and ✓ **"to flag was rather rudimentary. It compared only the consumer's first and last name with the names on the OFAC list."** | ✓ VERBATIM | TU @66048, @65657 |
| LS-19 | **From the Ninth Circuit's footnote 4:** ✓ **"TransUnion presented no data showing that any of its name matches through OFAC Advisor were correct. In other words, TransUnion could not confirm that a single OFAC alert sold to its customers was accurate."** | ✓ VERBATIM | CA9 @24648 |
| LS-20 | ✓ **"When TransUnion first began offering the OFAC Advisor product, it determined that the OFAC alerts being placed on consumer credit reports were exempt from the FCRA"** — the company's own legal position, as the Ninth Circuit records it. | ✓ VERBATIM | CA9 @16981 |
| LS-21 | ✓ **"In July 2011, TransUnion finally stopped sending OFAC Letters and began including OFAC alerts directly on the credit reports it sent to consumers."** | ✓ VERBATIM | CA9 @24902 |

**21 rows, 20 with a verbatim quotation.**

---

## 3. SERGIO RAMIREZ — the record, and only the record

| ID | Claim | Grade | Source |
|---|---|---|---|
| SR-01 | ✓ **"Sergio Ramirez learned the hard way that he is one such individual. On February 27, 2011, Ramirez visited a Nissan dealership in Dublin, California, seeking to buy a Nissan Maxima. Ramirez was accompanied by his wife and his father-in-law."** | ✓ VERBATIM | TU @15460 |
| SR-02 | ✓ **"Ramirez's credit report, produced by TransUnion, contained the following alert: '***OFAC ADVISOR ALERT - INPUT NAME MATCHES NAME ON THE OFAC DATABASE.'"** | ✓ VERBATIM | TU @15832 |
| SR-03 | ✓ **"A Nissan salesman told Ramirez that Nissan would not sell the car to him because his name was on a ' "terrorist list." '"** — quoting the record at App. 333. **The salesman is not named anywhere in either opinion.** ⛔-08. | ✓ VERBATIM | TU @15993 |
| SR-04 | ✓ **"Ramirez's wife had to purchase the car in her own name."** | ✓ VERBATIM | TU @16127 |
| SR-05 | **The two mailings.** The day after the dealership, Ramirez requested his credit file. TransUnion sent it the same day with the CFPB summary of rights, and **that mailing did not mention the OFAC alert**. The following day TransUnion sent a second mailing — the "OFAC Letter" — telling him his name was a potential match, **without an additional copy of the summary of rights**. | ✓ | TU @16473 (credit-file mailing omits the alert), @16687 (second mailing omits the summary of rights) |
| SR-06 | **The OFAC Letter, quoted from the record:** ✓ **"the name that appears on your TransUnion credit file 'SERGIO L RAMIREZ' is considered a potential match to information listed on the United States Department of Treasury's Office of Foreign Asset Control ('OFAC') Database."** | ✓ VERBATIM | CA9 @12967 |
| SR-07 | **The letter's own instruction — the film's central irony, fully sourced:** ✓ **"Financial institutions are required to check customers' names against the OFAC Database, and if a potential name match is found, to verify whether their potential customer is the person on the OFAC Database. For this reason, some financial institutions may ask for your date of birth, or they may ask to a see a copy of a governmentissued form of identification"** (the run-together "governmentissued" is a line-break artefact of the source PDF). | ✓ VERBATIM | CA9 @13387 |
| SR-08 | **And TransUnion enclosed the identifiers it had not itself compared.** The Ninth Circuit's bracketed description of the letter's enclosure: ✓ **"[OFAC records for the two prohibited SDNs who purportedly matched Ramirez, which include first, middle, and last names, dates of birth, and passport information]"** ⚠ **This is the court's summary in brackets, not the letter's own words — never present it as a quotation from the letter.** | ✓ VERBATIM (as the court's bracketed description) | CA9 @14093 |
| SR-09 | ✓ **"Ramirez testified that he was confused by the two mailings."** ✓ **"The lack of any OFAC information in the creditreport mailing suggested the alert had been removed, but the OFAC Letter mailing suggested otherwise."** | ✓ VERBATIM | CA9 @14604, @14664 |
| SR-10 | ✓ **"Ramirez also did not know how to remedy the issue because the OFAC Letter did not include instructions for initiating a dispute. Concerned about possible consequences of the OFAC match, Ramirez canceled an international vacation he had planned with his family."** | ✓ VERBATIM | CA9 @14812 |
| SR-11 | The Supreme Court records the same episode more tersely, and names the destination: ✓ **"Concerned about the mailings, Ramirez consulted a lawyer and ultimately canceled a planned trip to Mexico. TransUnion eventually removed the OFAC alert from Ramirez's file."** ⚠ **TU says "Mexico"; CA9 says "an international vacation … with his family". Both are the record. Do not merge them into a detail neither states.** | ✓ VERBATIM | TU @16767 |
| SR-12 | **What made Ramirez's own case stronger than the class's**, in the Ninth Circuit's words: ✓ **"Ramirez's credit report with the false OFAC alert was sent to a third party; Ramirez's alert stated that he was a match instead of a potential match; Ramirez was denied credit because of the alert; he canceled a vacation because of the alert; and he spent significant time and energy trying to remove the alert, including hiring a lawyer."** | ✓ VERBATIM | CA9 @68241 |
| SR-13 | ✓ **"TransUnion sent the same OFAC Letter to 8,184 other consumers who also requested copies of their credit reports between January 2011 and July 2011."** | ✓ VERBATIM | CA9 @15400 |
| SR-14 | **The limit of the record as to everyone else:** ✓ **"only a quarter of the other class members had their credit reports sent to a third party during the class period, and there was no evidence regarding whether other class members had experiences similar to Ramirez's as a result of the alerts."** | ✓ VERBATIM | CA9 @68593 |
| SR-15 | ✓ **"At trial, Ramirez testified about his experience at the Nissan dealership. But Ramirez did not present evidence about the experiences of other members of the class."** | ✓ VERBATIM | TU @18688 |

**15 rows, 13 with a verbatim quotation.**

---

## 4. THE CLASS, THE TRIAL, AND THE MONEY — keep these numbers apart

| ID | Claim | Grade | Source |
|---|---|---|---|
| MN-01 | **The class definition:** ✓ **"all natural persons in the United States and its Territories to whom TransUnion sent a letter similar in form to the March 1, 2011 [OFAC Letter] TransUnion sent to [Ramirez] . . . from January 1, 2011-July 26, 2011."** | ✓ VERBATIM | CA9 @25411 |
| MN-02 | ✓ **"Before trial, the parties stipulated that the class contained 8,185 members, including Ramirez. The parties also stipulated that only 1,853 members of the class (including Ramirez) had their credit reports disseminated by"** ✓ **"TransUnion to potential creditors during the period from January 1, 2011, to July 26, 2011."** (One sentence, split by a page break in the source.) | ✓ VERBATIM | TU @18204 + @18479 |
| MN-03 | The remaining **6,332** had OFAC alerts in their internal credit files that were **not** provided to any third party in the class period. **8,185 − 1,853 = 6,332**, and the opinion states all three numbers itself. | ✓ | TU @5606, @62988 |
| MN-04 | **The jury verdict:** ✓ **"After six days of trial, the jury returned a verdict for the plaintiffs. The jury awarded each class member $984.22 in statutory damages and $6,353.08 in punitive damages for a total award of more than $60 million."** | ✓ VERBATIM | TU @18853 |
| MN-05 | The Ninth Circuit gives the same award classwide: ✓ **"The jury found in favor of the class on all three claims and awarded each class member $984.22 in statutory damages (about $8 million classwide) and $6,353.08 in punitive damages (about $52 million classwide)."** | ✓ VERBATIM | CA9 @27136 |
| MN-06 | **The Ninth Circuit cut the punitive award before the case ever reached the Supreme Court:** ✓ **"We reduce the punitive-damages award from $6,353.08 per class member to $3,936.88 per class member, but otherwise affirm the verdict and judgment."** Because ✓ **"the panel held that the punitive damages award was excessive in violation of constitutional due process."** | ✓ VERBATIM | CA9 @9043, @3459 |
| MN-07 | **⚠ ARITHMETIC, NOT A COURT FIGURE.** $984.22 + $6,353.08 = **$7,337.30** per member × 8,185 = **$60,055,800.50** (the Court's "more than $60 million"). After the Ninth Circuit's reduction: $984.22 + $3,936.88 = **$4,921.10** × 8,185 ≈ **$40.3 million**. **No court states that $40.3M figure.** If the film uses it, it must be shown as our arithmetic on MN-04 and MN-06, or cut. | ✓ (arithmetic on verbatim rows), **NOT a quotation** | derived from MN-04, MN-06 |
| MN-08 | **The three FCRA claims**, as the Ninth Circuit lists them: **(1)** willful failure to follow reasonable procedures to assure accuracy, **15 U.S.C. § 1681e(b)**; **(2)** willful failure to disclose the entire credit report by excluding the alerts, **§ 1681g(a)(1)**; **(3)** willful failure to provide a summary of rights, **§ 1681g(c)(2)**. | ✓ | CA9 @1220 |
| MN-09 | ✓ **"In 1970, Congress passed and President Nixon signed the Fair Credit Reporting Act."** It requires agencies to ✓ **"follow reasonable procedures to assure maximum possible accuracy"** in consumer reports. | ✓ VERBATIM | TU @11893, @12546 |
| MN-10 | ✓ **"Ramirez and the class pursued only a willfulness theory for each of their three claims, presumably because statutory and punitive damages are available for willful, but not negligent, FCRA violations."** | ✓ VERBATIM | CA9 @60748 |
| MN-11 | **What the Supreme Court did NOT do to the money.** The majority states **no dollar figure of its own** beyond quoting the verdict at MN-04; it did not remit, recalculate, or apportion anything. It removed **6,332** members from the reasonable-procedures claim and **all but Ramirez** from the two formatting claims, and remanded. **Any final per-person recovery is unstated in every document retrieved.** ⛔-04. | ✓ | TU @62988–63960; `willful` appears in the majority **once**, only inside a quotation of the statute (TU @13243) |

**11 rows, 7 with a verbatim quotation, 1 explicitly labelled as arithmetic.**

---

## 5. WHAT THE SUPREME COURT HELD — the actual holding

**This section is the spine. Prefer these quotations over any paraphrase.**

| ID | Claim | Grade | Source |
|---|---|---|---|
| HD-01 | **The first lines of the opinion, and the sentence the case is remembered by:** ✓ **"To have Article III standing to sue in federal court, plaintiffs must demonstrate, among other things, that they suffered a concrete harm. No concrete harm, no standing."** | ✓ VERBATIM | TU @9520 |
| HD-02 | **The holding as the syllabus states it:** ✓ **"Only plaintiffs concretely harmed by a defendant's statutory violation have Article III standing to seek damages against that private defendant in federal court."** | ✓ VERBATIM | TU @2980 |
| HD-03 | **The holding applied, stated up front:** ✓ **"only 1,853 class members have standing for the reasonable-procedures claim and (ii) only Ramirez himself has standing for the two formatting claims relating to the mailings"** | ✓ VERBATIM | TU @11598 |
| HD-04 | **The epigram of the whole doctrine:** ✓ **"An injury in law is not an injury in fact."** | ✓ VERBATIM | TU @4407 |
| HD-05 | ✓ **"Article III standing requires a concrete injury even in the context of a statutory violation."** (quoting *Spokeo, Inc. v. Robins*, 578 U.S. 330, 341 (2016)). | ✓ VERBATIM | TU @4056 |
| HD-06 | **The distinction the case turns on:** ✓ **"The standing inquiry in this case thus distinguishes between (i) credit files that consumer reporting agencies maintain internally and (ii) the consumer credit reports that consumer reporting agencies disseminate to thirdparty creditors."** | ✓ VERBATIM | TU @45963 |
| HD-07 | ✓ **"The mere presence of an inaccuracy in an internal credit file, if it is not disclosed to a third party, causes no concrete harm."** | ✓ VERBATIM | TU @46201 |
| HD-08 | **The image the majority chose:** ✓ **"the plaintiffs' harm is roughly the same, legally speaking, as if someone wrote a defamatory letter and then stored it in her desk drawer. A letter that is not sent does not harm anyone, no matter how insulting the letter is. So too here."** | ✓ VERBATIM | TU @46434 |
| HD-09 | **On risk of future dissemination:** the Court held the risk identified by the 6,332 — ✓ **"the risk of dissemination to third parties— was too speculative to support Article III standing"** (the em-dash spacing is the source's). | ✓ VERBATIM | TU @54103 |
| HD-10 | **The majority's sharpest point against the absent class:** ✓ **"the plaintiffs did not present any evidence that the 6,332 class members even knew that there were OFAC alerts in their internal TransUnion credit files. If those plaintiffs prevailed in this case, many of them would first learn that they were 'injured' when they received a check compensating them for their supposed 'injury.'"** | ✓ VERBATIM | TU @55055 |
| HD-11 | **The disposition, in full:** ✓ **"No concrete harm, no standing. The 1,853 class members whose credit reports were provided to third-party businesses suffered a concrete harm and thus have standing as to the reasonable-procedures claim. The 6,332 class members whose credit reports were not provided to third-party businesses did not suffer a concrete harm and thus do not have standing as to the reasonable-procedures claim. As for the claims pertaining to the format of TransUnion's mailings, none of the 8,185 class members other than the named plaintiff Ramirez suffered a concrete harm."** | ✓ VERBATIM | TU @62988 |
| HD-12 | ✓ **"We reverse the judgment of the U. S. Court of Appeals for the Ninth Circuit and remand the case for further proceedings consistent with this opinion."** | ✓ VERBATIM | TU @63546 |
| HD-13 | **The case was NOT ended:** ✓ **"On remand, the Ninth Circuit may consider in the first instance whether class certification is appropriate in light of our conclusion about standing."** The Court also expressly declined to decide the Rule 23 typicality question. | ✓ VERBATIM | TU @63850 |
| HD-14 | **PLAIN-ENGLISH GLOSS — recorded as a gloss, not as a quotation.** *A federal court may only hear your case if you were actually hurt. Congress writing a law that says a company owed you something, and the company breaking that law, is not by itself enough — you must show the breach did something to you in the real world. For 1,853 people TransUnion had handed the false terrorist flag to an outside business, so they were hurt. For 6,332 people the false flag sat inside TransUnion's own computers and never went anywhere, so, the Court held, nothing had yet happened to them.* **This gloss may be spoken in the film's own voice. It may never be presented as words of the Court.** | ○ **GLOSS** | derived from HD-01…HD-11 |

**14 rows, 13 with a verbatim quotation, 1 explicitly a gloss.**

---

## 6. THE THOMAS DISSENT — the counter-voice, and the third act

| ID | Claim | Grade | Source |
|---|---|---|---|
| TH-01 | **Opening:** ✓ **"TransUnion generated credit reports that erroneously flagged many law-abiding people as potential terrorists and drug traffickers."** | ✓ VERBATIM | TU @64404 |
| TH-02 | ✓ **"Yet despite Congress' judgment that such misdeeds deserve redress, the majority decides that TransUnion's actions are so insignificant that the Constitution prohibits consumers from vindicating their rights in federal court. The Constitution does no such thing."** | ✓ VERBATIM | TU @64782 |
| TH-03 | ✓ **"The system TransUnion used to decide which individuals"** ✓ **"to flag was rather rudimentary."** (One sentence, split by a page break.) | ✓ VERBATIM | TU @65547 + @65657 |
| TH-04 | **The prior case, as Thomas recounts it:** in 2005 a consumer sued; TransUnion had sold an OFAC credit report about her to a car dealership. ✓ **"The report flagged her—Sandra Jean Cortez, born in May 1944—as a match for a person on the OFAC list: Sandra Cortes Quintero, born in June 1971."** TransUnion withheld the alert from the report Cortez requested and kept it in place for years. A jury found for her; **$50,000 actual and $750,000 punitive damages**. *Cortez v. Trans Union, LLC*, 617 F.3d 688 (3d Cir. 2010). | ✓ VERBATIM (the flagged-her sentence) | TU @66241 (✓ "In 2005, a consumer sued."), @66350 (the quoted sentence), @67115 (✓ "The jury awarded $50,000 in actual damages and $750,000 in punitive damages"). **○-03: the Cortez opinion itself was not retrieved.** |
| TH-05 | **The line the film's third act is built on:** ✓ **"one need only tap into common sense to know that receiving a letter identifying you as a potential drug trafficker or terrorist is harmful. All the more so when the information comes in the context of a credit report, the entire purpose of which is to demonstrate that a person can be trusted."** | ✓ VERBATIM | TU @98211 |
| TH-06 | Thomas quoting the Ninth Circuit's footnote 4: ✓ **"TransUnion could not confirm that a single OFAC alert sold to its customers was accurate."** | ✓ VERBATIM | TU @100922 (quoting CA9 @24648) |
| TH-07 | ✓ **"Yet thanks to this Court, it may well be in a position to keep much of its ill-gotten gains."** ⚠ **This is a dissenting justice's characterisation. Always attributed to Thomas, never in the film's own voice.** ⛔-06. | ✓ VERBATIM | TU @101040 |
| TH-08 | **The consequence Thomas predicts:** the decision ✓ **"may leave state courts—which 'are not bound by the limitations of a case or controversy or other federal rules of justiciability even when they address issues of federal law,'"** as the sole forum, with defendants unable to remove to federal court. He calls it a possible ✓ **"pyrrhic victory for TransUnion."** | ✓ VERBATIM | TU @101441, @101243 |
| TH-09 | **The closing, and the best ending line available in any document:** ✓ **"Who could possibly think that a person is harmed when he requests and is sent an incomplete credit report, or is sent a suspicious notice informing him that he may be a designated drug trafficker or terrorist, or is not sent anything informing him of how to remove this inaccurate red flag? The answer is, of course, legion: Congress, the President, the jury, the District Court, the Ninth Circuit, and four Members of this Court."** | ✓ VERBATIM | TU @102152 |

**9 rows, 9 with a verbatim quotation.**

---

## 7. THE KAGAN DISSENT — the plainest statement of what the 6,332 lost

| ID | Claim | Grade | Source |
|---|---|---|---|
| KG-01 | ✓ **"The Court here transforms standing law from a doctrine of judicial modesty into a tool of judicial aggrandizement. It holds, for the first time, that a specific class of plaintiffs whom Congress allowed to bring a lawsuit cannot do so under Article III."** | ✓ VERBATIM | TU @103699 |
| KG-02 | ✓ **"TransUnion willfully violated that statute's provisions by preparing credit files that falsely called the plaintiffs potential terrorists, and by obscuring that fact when the plaintiffs requested copies of their files."** ⚠ **A dissent's characterisation. Attribute it.** | ✓ VERBATIM | TU @104737 |
| KG-03 | ✓ **"To say, as the majority does, that the resulting injuries did not ' "exist" in the real world' is to inhabit a world I don't know."** | ✓ VERBATIM | TU @104956 |
| KG-04 | **The single most quotable sentence in the case:** ✓ **"But why is it so speculative that a company in the business of selling credit reports to third parties will in fact sell a credit report to a third party?"** | ✓ VERBATIM | TU @105612 |
| KG-05 | ✓ **"Congress is better suited than courts to determine when something causes a harm or risk of harm in the real world."** | ✓ VERBATIM | TU @107724 |
| KG-06 | Kagan notes Thomas's observation that ✓ **"nearly 25% of the class"** already had false reports ✓ **"sent to potential creditors"**. (1,853 ÷ 8,185 = 22.6%; the phrase in the opinions is "nearly 25%" and "only a quarter" — **quote the phrase, do not substitute the percentage**.) | ✓ VERBATIM | TU @105827; cf. CA9 @68593 |

**6 rows, 6 with a verbatim quotation.**

---

## 8. THE NINTH CIRCUIT BELOW — willfulness, and the warning TransUnion had

**This section exists because the Supreme Court never reached these questions, and a script will otherwise
either invent them or wrongly assume the Supreme Court erased them.**

| ID | Claim | Grade | Source |
|---|---|---|---|
| N9-01 | **The evidence of the prior warning:** ✓ **"Plaintiffs presented evidence that—despite being told in 2010 by another circuit court that OFAC alerts were covered by the FCRA and subject to § 1681e(b)'s reasonable procedures requirement—TransUnion continued to utilize name-only searches to produce OFAC 'matches.'"** | ✓ VERBATIM | CA9 @61593 |
| N9-02 | ✓ **"Most notably, the Third Circuit specifically reprimanded TransUnion for failing to use an additional identifier such as date of birth to verify the accuracy of OFAC matches."** | ✓ VERBATIM | CA9 @61862 |
| N9-03 | **The willfulness conclusion:** ✓ **"Despite this warning, TransUnion continued to use problematic matching technology and to treat OFAC information as separate from other types of information on consumer reports. In doing so, it ran an unjustifiably high risk of error. The jury's verdict is consistent with the law and supported by substantial evidence."** | ✓ VERBATIM | CA9 @66727 |
| N9-04 | **⚠ THE SUPREME COURT DID NOT DISTURB THIS, AND DID NOT ENDORSE IT EITHER.** The word `willful` appears in the **majority exactly once**, inside a quotation of § 1681n — never in analysis. The Court decided **standing**, and remanded. The willfulness holding was simply not before it. | ✓ | TU: single `willful` at @13243 (verified by exhaustive count over the majority span @9484–@64307) |
| N9-05 | **⛔ TRAP — the phrase "aware that its practice was unlawful".** The Ninth Circuit's headnote reads ✓ **"TransUnion, aware that its practice was unlawful, incorrectly placed terrorist alerts on the front page of the consumers' credit reports"** — **but that text is the court-staff summary**, which says of itself: ✓ **"This summary constitutes no part of the opinion of the court. It has been prepared by court staff for the convenience of the reader."** **It is not a judicial finding and must never be quoted as one.** Use N9-01 → N9-03 instead. | ✓ VERBATIM (both) | CA9 @892 and @2041 |
| N9-06 | Judge McKeown concurred in part and dissented in part: she agreed all class members need standing and that the punitive award was excessive, but would have held that **only** the 1,853 (plus Ramirez) had standing on the reasonable-procedures claim and **only Ramirez** on the other two — i.e. she reached substantially the result the Supreme Court later reached. **Recorded from the court-staff summary and the majority's citations; her separate opinion was not read line by line (○-01).** | ✓ | CA9 @3744; her opinion cited by TU @54200 and @55000 (✓ "951 F. 3d, at 1040 (opinion of McKeown, J.)") |

**6 rows, 5 with a verbatim quotation.**

---

## 9. WHAT THE COURT EXPRESSLY DID **NOT** DECIDE

| ID | The Court did NOT decide | Grade | Source |
|---|---|---|---|
| ND-01 | **Whether TransUnion violated the FCRA.** The judgment turned entirely on **who may sue in federal court**, not on whether the conduct was lawful. The 1,853 keep their claim. | ✓ | HD-02, HD-11 |
| ND-02 | **Whether the FCRA violations were willful.** Not addressed (N9-04). | ✓ | N9-04 |
| ND-03 | **Whether the class was properly certified.** ✓ **"On remand, the Ninth Circuit may consider in the first instance whether class certification is appropriate in light of our conclusion about standing."** | ✓ VERBATIM | TU @63850 |
| ND-04 | **Whether the 6,332 could sue in STATE court.** The Court held only that **federal** courts lack jurisdiction. Thomas expressly flags state court as the remaining forum (TH-08). The majority does not decide it. | ✓ | TH-08 |
| ND-05 | **Whether the 6,332 would have standing for INJUNCTIVE relief.** The Court's risk-of-future-harm discussion expressly reserves this: material risk of future harm can satisfy concreteness ✓ **"in the context of a claim for injunctive relief to prevent the harm from occurring"** — this was a **damages** suit. | ✓ VERBATIM | TU @6289 (syllabus) |
| ND-06 | **What any class member ultimately received.** No document retrieved states a final recovery. ⛔-04, ○-04. | ✓ | MN-11 |
| ND-07 | **Anything about Equifax, Experian, credit scores, or credit reporting generally.** The case is about one add-on product at one company. | ✓ | LS-13; no such discussion in TU or CA9 |
| ND-08 | **Whether the Nissan dealership or its salesman did anything wrong.** Neither was a party. Neither opinion evaluates their conduct. | ✓ | SR-03; no such holding in TU or CA9 |

**8 rows.**

---

## 10. ⛔ FORBIDDEN CLAIMS — a script must never say these

| ID | Forbidden | Why |
|---|---|---|
| ⛔-01 | **"The Supreme Court ruled 6–3."** | **It was 5–4.** Kavanaugh + Roberts, Alito, Gorsuch, Barrett = five. Thomas, Breyer, Sotomayor, Kagan = four. ID-03, ID-04. Thomas's own closing says ✓ "four Members of this Court." This is the single easiest factual error to make in this episode and the easiest for a viewer to catch. |
| ⛔-02 | **"The Supreme Court said TransUnion did nothing wrong."** / "TransUnion won." / "The Court threw the case out." | Exactly wrong on all three. The Court decided **standing only** (ND-01), **1,853 people kept their claim** including Ramirez, Ramirez kept **all three** of his claims, and the case was **remanded, not dismissed** (HD-12, HD-13). TransUnion won a large partial victory; it did not win the case, and it was not exonerated. |
| ⛔-03 | **"The Supreme Court took the money away from the victims."** stated flatly. | Two things it flattens. First, **the Ninth Circuit had already cut the punitive award** from $6,353.08 to $3,936.88 per member (MN-06) before the Supreme Court touched it. Second, the Supreme Court set **no dollar figure at all** (MN-11); it removed plaintiffs from claims and remanded. Say what happened to the **class**, not to a number the Court never wrote. |
| ⛔-04 | **Any per-person figure for what a class member finally received**, and **any total after the Supreme Court's ruling** (e.g. "$40 million", "$8 million", "they each got $X in the end"). | The record retrieved stops at the Ninth Circuit's judgment. What survived remand is **unretrieved** (○-04; CourtListener HTTP 429 this pass). The only per-person figures any document states are **$984.22**, **$6,353.08** and **$3,936.88** — all **as awarded or as ordered reduced**, none as received. MN-07's ≈$40.3M is **our arithmetic** and must be labelled as such or cut. |
| ⛔-05 | **Any claim about TransUnion's state of mind, intent, motive, or corporate culture that is not one of N9-01 → N9-03.** Specifically forbidden: "TransUnion knew it was ruining lives", "TransUnion didn't care", "TransUnion deliberately labelled innocent people terrorists", "TransUnion decided profit was worth it." | TransUnion LLC is a **living, named corporation**. The retrievable record supports exactly this and no more: it used name-only matching (LS-14, LS-16); it used an additional identifier for every **other** data type (LS-17); it took the legal position that OFAC alerts were FCRA-exempt (LS-20); it could not confirm a single alert was accurate (LS-19); in 2010 the Third Circuit reprimanded it for not comparing dates of birth and **it continued** name-only matching (N9-01, N9-02); a jury found the violations willful and the Ninth Circuit affirmed on substantial evidence (N9-03); it changed the practice in **July 2011** (LS-21). **That is a devastating record and it does not need embellishment.** Say those things; invent nothing past them. |
| ⛔-06 | **Quoting "ill-gotten gains" (TH-07), "willfully violated" (KG-02), or "erroneously flagged many law-abiding people" (TH-01) in the film's own voice.** | These are **dissenting** characterisations by justices who **lost**. They are quotable — they are excellent — but only as *"Justice Thomas wrote…"* / *"in dissent, Justice Kagan…"*, always attributed, never as the Court's finding or the narrator's assertion. |
| ⛔-07 | **Anything about Sergio Ramirez's life, character, occupation, finances, immigration status, family, or feelings beyond SR-01 → SR-12.** No invented interior monologue, no "he must have felt", no scene at home. | He is a **living private individual** described sympathetically in a published opinion. The record gives: the dealership visit with his wife and father-in-law (SR-01); the alert (SR-02); the salesman's statement (SR-03); his wife buying the car (SR-04); two mailings and his confusion (SR-05, SR-09); no dispute instructions (SR-10); a cancelled international trip / trip to Mexico (SR-10, SR-11); consulting a lawyer (SR-10); being denied credit (SR-12); his testimony (SR-15). **Nothing else exists in any document retrieved.** ○-05. |
| ⛔-08 | **Naming, depicting identifiably, characterising, or scripting dialogue for the Nissan salesman or any dealership employee.** | **Neither opinion names them.** They were not parties, were never heard, and are private individuals who cannot answer. The only permissible statement is the record one: ✓ *"A Nissan salesman told Ramirez that Nissan would not sell the car to him because his name was on a 'terrorist list.'"* (SR-03) — and not one word past it. No "the salesman smirked", no reconstructed conversation, no invented name. |
| ⛔-09 | **Naming, or building a scene around, "the two prohibited SDNs who purportedly matched Ramirez."** | CA9 @14093 describes the enclosure but **does not print their names**, and this ledger did not retrieve them. They are real people on a sanctions list and are not the subject of this film. Refer to them only as the record does. |
| ⛔-10 | **"You need a warrant"-style overstatement of the holding**, e.g. "the Supreme Court ruled that credit bureaus can lie about you", "companies can now put anything in your file", "it is legal to call you a terrorist." | The holding is jurisdictional (HD-02). The FCRA still applies; the conduct was still found willful below; the 1,853 still had a claim; **state courts remain open** (ND-04, TH-08). Every sentence describing the holding must contain the idea of *who may sue in federal court*, or be cut. |
| ⛔-11 | **Presenting the 19,199 SDN-record count, or any list size, as a Treasury statement.** | Treasury publishes **no current count** on any page retrieved (LS-05). 19,199 is **our count of Treasury's own published `sdn.csv` dated 7 August 2026**, and must be attributed exactly that way. The "over 12,000" figure is Treasury's, but it is a **2021 cumulative designations** number and is not the size of the list today. |
| ⛔-12 | **Stating what happened after 25 June 2021** — the remand, any settlement, any later certification ruling, TransUnion's current practices, or Sergio Ramirez's life since. | ○-04. **Not in any document retrieved.** CourtListener returned **HTTP 429** (daily quota exceeded) on this pass and the docket could not be checked. The film must end where the record ends, or the gate must be closed first. |
| ⛔-13 | **Any dramatised or AI-generated image presented as** Sergio Ramirez, a real TransUnion credit report, the actual OFAC Letter, a real OFAC list entry, the Dublin dealership, or any court record. | PD invariant 11. This case turns on **identifiable living people and an identifiable real corporation**. Generated visuals are illustration, never evidence. The OFAC Letter's *text* may be set as a typographic card because it is quoted in a published opinion (SR-06, SR-07) — but it must not be styled to look like a photograph of the original document. |
| ⛔-14 | **Quoting the Ninth Circuit's court-staff summary as the court's words** — above all ✓ "TransUnion, aware that its practice was unlawful". | N9-05. The document says of itself that the summary ✓ **"constitutes no part of the opinion of the court."** Quoting it as a judicial finding is the most inviting error in the whole record, because it is the most quotable sentence in the file and it sits at the very top. |
| ⛔-15 | **Merging TU's "a planned trip to Mexico" with CA9's "an international vacation he had planned with his family"** into a single invented detail (e.g. "a family holiday in Mexico"). | SR-11. Two courts describe the same cancelled trip at different levels of detail. Pick one source and cite it, or say "a planned international trip". Do not synthesise a third version that neither wrote. |
| ⛔-16 | **"Article III" explained as "a technicality."** | It is the holding (HD-02) and it is the film's subject. Calling it a technicality tells the viewer the last twenty minutes did not matter. HD-14 is the approved plain-English gloss; use it. |

**16 quarantine entries.**

---

## 11. ○ OPEN QUESTIONS — what a viewer will ask that the record cannot answer

**Nothing here may be spoken, shown, or implied until it is upgraded from a source read directly.**

| ID | Question | Why it is here |
|---|---|---|
| ○-01 | **What exactly did Judge McKeown write?** | N9-06 records her result from the court-staff summary and the majority's two citations to her opinion. Her reasoning was **not read line by line**. She is a striking figure — the judge below who called it the way the Supreme Court later did — and if the film uses her that way, her opinion must be read first. |
| ○-02 | **What did the district court say?** 301 F.R.D. 408 (2014); 2016 WL 6070490. | Not retrieved. Anything about Judge Corley's reasoning, the six-day trial, or the courtroom is unsourced. |
| ○-03 | **The full story of Sandra Jean Cortez.** | TH-04 is everything this pass has, and it comes from Thomas summarising *Cortez*, not from *Cortez*. It supports "TransUnion had been warned". It does **not** support narrating her case as a scene. Retrieve 617 F.3d 688 before giving her more than a sentence. |
| ○-04 | **What happened on remand?** Did the 1,853 ever recover? Was the class recertified? Did the parties settle? What is TransUnion's OFAC matching practice today? | **The single most important open gate.** No document retrieved goes past 25 June 2021. **CourtListener returned HTTP 429** (125/day exceeded, reset ~10h) on this pass, so the docket could not be checked. **This must be closed before a single word of the ending is written** — the film currently has no ending, only a holding. |
| ○-05 | **Who is Sergio Ramirez as a person?** Age, work, family, what the years of litigation cost him, where he is now. | The opinions give a car, a wife, a father-in-law, a cancelled trip, a lawyer, and testimony. Everything else is invention. ⛔-07. |
| ○-06 | **How many of the 8,185 were, like Ramirez, refused something?** | Expressly absent: ✓ "there was no evidence regarding whether other class members had experiences similar to Ramirez's" (SR-14). The film may not imply thousands of denied car loans. **The absence of that evidence is itself a fact the majority relied on** (HD-10) and the film should say so. |
| ○-07 | **What is a "false positive" rate for name-only OFAC screening?** | No such figure in any document retrieved. LS-15 ("many false positives") and LS-19 ("could not confirm that a single OFAC alert … was accurate") are the only quantitative-sounding statements available, and neither is a rate. Do not invent one. |
| ○-08 | **Has Congress or the CFPB responded to this decision?** | Outside every document retrieved. |
| ○-09 | **How has *TransUnion v. Ramirez* been applied since 2021?** | It is a heavily cited standing case; this pass retrieved **no** subsequent authority. Any "since then, courts have…" line is unsourced. |
| ○-10 | **The names and identifying details of the two SDNs Ramirez matched.** | Not in the retrieved record (⛔-09). Deliberately left closed — retrieving them would create a new rights and privacy problem, not solve one. |

**10 open questions.**

---

## THE SHAPE THE FACTS ALREADY HAVE

*Not a claim — a note for the writer.*

```
WHAT THE MACHINE COMPARED              WHAT WAS AVAILABLE TO COMPARE

first name                             full name
last name                              address
                                       nationality
                                       passport number
— that is the entire list —            tax ID / cedula number
  (LS-14, LS-18)                       place of birth
                                       DATE OF BIRTH
                                       former names and aliases
                                          (LS-08, OFAC's own enumeration)

"Cortez" would match with "Cortes."    And for tax liens, and for bankruptcies,
              (LS-16)                  TransUnion DID use a second identifier.
                                       OFAC data was the only kind it matched
                                       on name alone.              (LS-17)
```

The three beats the record hands the film, in order:

1. **2010.** The Third Circuit reprimands TransUnion for not comparing dates of birth. Sandra Jean Cortez, born May 1944, had been matched to Sandra Cortes Quintero, born June 1971. (TH-04, N9-02)
2. **27 February 2011.** Sergio Ramirez cannot buy a car. His wife buys it in her own name. (SR-01, SR-04)
3. **1 March 2011.** TransUnion mails him a letter explaining that institutions should verify a name match by asking for a **date of birth** — and encloses the SDN records, which contain **dates of birth**. (SR-07, SR-08)

Then the reversal. A jury of his peers awards more than $60 million. The Ninth Circuit affirms the verdict
and trims the punitive award. And the Supreme Court holds that **6,332 of the 8,185 were never allowed to
be in a federal courtroom at all** — not because they were not lied about, but because the lie had not yet
left the building. ✓ *"A letter that is not sent does not harm anyone, no matter how insulting the letter
is."* (HD-08)

**HD-08 is the hinge and KG-04 is the answer to it.** Open on the desk-drawer letter. Close on Kagan:
✓ *"But why is it so speculative that a company in the business of selling credit reports to third parties
will in fact sell a credit report to a third party?"* Between them sits the thing the film is actually
about — that **the 6,332 mostly never knew**, and the majority said so out loud: ✓ *"many of them would
first learn that they were 'injured' when they received a check compensating them for their supposed
'injury.'"* (HD-10)

**And the honest complication the film owes the viewer:** that sentence is *not stupid*. The strongest
version of this episode takes HD-10 seriously — a person who never learned of a file entry that never
moved has a real problem showing what it did to them — and then answers it with LS-19: **TransUnion could
not confirm that a single one of the alerts it sold was accurate.** A film that makes the majority sound
foolish will lose the half of the audience that can see the point. A film that states the majority's best
argument and then answers it earns the ending.

---

*Built 2026-08-10 from two court opinions retrieved and read end to end this pass — the Supreme Court slip
opinion in No. 20–297 (108,182 chars) and the Ninth Circuit opinion in No. 17-17244 (99,274 chars) — plus
eight official Treasury/OFAC pages and Treasury's published SDN data file. **No fact in this ledger comes
from memory, from a secondary source, or from a subagent's unverified report;** the OFAC research was
returned by a subagent and every one of its quotations was independently re-located by exact string search
in the files it saved before being written here. **90 fact rows** (identity 8, list-and-product 21,
Ramirez 15, class-trial-money 11, holding 14, Thomas 9, Kagan 6, Ninth Circuit 6 — less the 1 gloss and
the 1 arithmetic row, which are labelled) · **8 not-decided rows** · **16 quarantine entries** ·
**10 open questions**. **74 distinct quotations are machine-verified ✓ VERBATIM** and re-verifiable with
`verify_quotes.v001.py`. **Gate ○-04 must be closed before the film can have an ending.** Nothing here has
been written into a script.*
