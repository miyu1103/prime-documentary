# EP70 · THE WRONG HOUSE — FACTS LEDGER v001

**Episode:** EP70 · ID `PD-2026-070-wronghouse` · slug `wronghouse` · topic `TOP-20260812-001`
**Event:** FBI SWAT execution of a search and arrest warrant at **3756 Denville Trace SW, Atlanta, Georgia**,
**18 October 2017, at or about 5:00 a.m.** — the wrong house. And the eight years, ten months and counting
that followed it.
**Written:** 2026-08-12. **Research and writing only. No render, build, GPU or upload was run.**
**Purpose:** every factual claim the film may make, with its grade and its source.

**Invariant 1: no unsupported factual statement enters an approved script.** A claim graded ○ may not be
spoken, shown, put in a telop, or written into a title until it is upgraded.

**Grades:** ✓ **VERBATIM** = quoted word-for-word from a document retrieved and read by this pass, located by
exact string search and re-locatable by the verifier · ✓ = established from a source retrieved by this pass ·
✓ (arithmetic) = our own calculation on verbatim figures, **labelled as ours, never attributed to a source** ·
○ = research instruction, **NOT a fact** · ⛔ = quarantined, do not use.

**The standard this pass was held to:** *you opened it or it does not exist.* Every source in the table below
was fetched by this session and persisted to disk. Nothing here rests on a search-engine snippet, a summary,
an unopened URL or a model's memory. The reason is on the record: a previous PD agent fabricated ten of
fifteen citations (`feedback_subagent_fabrication`).

---

## 1. PRIMARY SOURCES — retrieved, hashed, persisted

All cached under `episodes/PD-2026-070-wronghouse/01_research/sources/`.
Raw originals keep their `RAW_`/`RECAP_`/`NEWS_` names; the `SRC-000N` files are the normalised texts the
verifier searches. The normalisation is described in the header of `build_sources.v001.py` and changes no
word: it deletes page furniture (CM/ECF footer stamps, slip-opinion running heads, transcript line numbers)
and collapses whitespace so that a sentence lies on one line.

| Tag | Document | How it was retrieved | Cached |
|---|---|---|---|
| **SC** | ***Martin v. United States***, No. 24–362, **605 U. S. 395**, 145 S. Ct. 1689, **decided 12 June 2025**. Gorsuch, J., for a unanimous Court; Sotomayor, J., concurring, joined by Jackson, J. Slip opinion, 28 pages. | CourtListener API v4, opinion id **11070040** (`/api/rest/v4/opinions/11070040/`), authenticated with `COURTLISTENER_TOKEN`; `plain_text` field, 59,172 chars. Cluster **10603452**; the API's own `download_url` is `supremecourt.gov/opinions/24pdf/24-362_mjn0.pdf`. | `SRC-0001_scotus_martin_slipop.txt` · 54,442 chars · sha256 `b715ce17bed79734…` |
| **DCT** | **N.D. Ga. order granting in part and denying in part summary judgment**, *Martin v. United States*, No. 1:19-cv-04106-JPB (consol. with 1:19-cv-04180), **ECF 124, filed 23 September 2022**, Boulee, J. — the opinion published at **631 F. Supp. 3d 1281**. 38 pages. | RECAP archive PDF, `storage.courtlistener.com/recap/gov.uscourts.gand.268470/gov.uscourts.gand.268470.124.0.pdf` (337,873 bytes), text extracted locally with pymupdf. | `SRC-0002_ndga_sj_order_ecf124.txt` · 53,827 chars · sha256 `7cb19cdbb530fb82…` |
| **RECON** | **N.D. Ga. order on cross-motions for reconsideration**, same case, **ECF 141, filed 30 December 2022**, Boulee, J. 12 pages. **This is the order that ended the case in the district court**, and it is not the order the Supreme Court's narrative summary describes. | RECAP, `…268470.141.0.pdf` (265,536 bytes), pymupdf. | `SRC-0003_ndga_recon_order_ecf141.txt` · 15,123 chars · sha256 `4a550a915dc9c9c5…` |
| **CA11** | **Eleventh Circuit opinion**, *Curtrina Martin v. USA*, **No. 23-10062**, **filed 22 April 2024**, **[DO NOT PUBLISH]**, Non-Argument Calendar, per curiam, before **Lagoa, Brasher and Abudu**, Circuit Judges. 18 pages. (Cited in the concurrence as 2024 WL 1716235.) | RECAP, `…268470.147.0.pdf` (257,569 bytes), pymupdf. | `SRC-0004_ca11_opinion_20240422.txt` · 28,047 chars · sha256 `7b20b9ed09368103…` |
| **CMPL** | **Complaint**, *Martin, individually and as parent and next friend of G.W. v. United States, Lawrence Guerra, and Six Unknown FBI Agents*, N.D. Ga., **ECF 1, filed 11 September 2019**. 16 pages. **The family's own sworn account**, and the only document in this ledger written from inside the house. | RECAP, `…268470.1.0.pdf` (178,665 bytes), pymupdf. | `SRC-0005_complaint_ecf1.txt` · 17,461 chars · sha256 `2eee359809823123…` |
| **OA** | **Transcript of oral argument**, Supreme Court of the United States, No. 24-362, **29 April 2025**. 66 pages. For petitioners **Patrick M. Jaicomo**; for respondents **Frederick Liu**, Assistant to the Solicitor General; for the Court-appointed amicus **Christopher E. Mills**. | `supremecourt.gov/oral_arguments/argument_transcripts/2024/24-362_m7i2.pdf` (390,572 bytes), filename located from the Court's own 2024-term transcript index, pymupdf. **A US Government work.** | `SRC-0006_scotus_oral_argument_20250429.txt` · 91,290 chars · sha256 `37c3af379641b659…` |
| **SDKT** | **Supreme Court docket, No. 24-362**, complete, from the extension application of 18 July 2024 to "Record returned to the United States District Court for the Northern District of Georgia" on 5 August 2025. | `supremecourt.gov/search.aspx?filename=/docket/docketfiles/html/public/24-362.html`, 114,446 bytes. WebFetch returns 403 on this host; a browser user-agent via curl returns 200. | `SRC-0007_scotus_docket_24-362.txt` · 11,757 chars · sha256 `4d77bf1d901ad827…` |
| **ADKT** | **Eleventh Circuit docket entries on remand**, No. 23-10062, **75 entries**, through the last entry of record. | CourtListener API v4 `/docket-entries/?docket=69035802`, paginated, authenticated. | `SRC-0008_ca11_docket_23-10062.txt` · 17,971 chars · sha256 `8aa0d586c3bc1575…` |
| **CNS** | **Courthouse News Service**, Megan Butler, **"11th Circuit takes fresh look at FBI raid of wrong Atlanta home"**, **25 March 2026** — a first-hand report of the remand argument, filed the day it was heard. | `courthousenews.com/11th-circuit-takes-fresh-look-at-fbi-raid-of-wrong-atlanta-home/`, 107,753 bytes. WebFetch 403; browser-UA curl 200. | `SRC-0009_courthousenews_20260325.txt` · 10,790 chars · sha256 `613b33ce378c1eba…` |
| **IJ** | **Institute for Justice case page, *Martin v. United States***, retrieved 2026-08-12. **This is the plaintiffs' own counsel speaking.** It is a party account, never a finding, and every row drawn from it is graded and labelled as such. | `ij.org/case/martin-v-united-states/`, 304,899 bytes. (`ij.org/case/atlanta-wrong-house-raid/` is a 404; the working slug was found from the page itself.) | `SRC-0010_ij_case_page.txt` · 20,421 chars · sha256 `0a03cd51937a5514…` |
| **DDKT** | **N.D. Ga. docket entries**, No. 1:19-cv-04106, **223 entries**, 11 September 2019 to 29 August 2025. | CourtListener API v4 `/docket-entries/?docket=16321544`, paginated, authenticated. | `SRC-0011_ndga_docket_1-19-cv-04106.txt` · 49,724 chars · sha256 `77960e39c92de08a…` |

Also persisted, not quoted: `RECAP_gand_268470_140.0.pdf` (transcript of the 27 April 2022 summary-judgment
hearing, 50 pages) and `RAW_docket_gand_1_19cv4180_cliatt.json` (Cliatt's separately filed, later
consolidated case, No. 1:19-cv-04180, filed 18 September 2019, terminated 2 May 2022).

**Machine verifier: `verify_quotes.v001.py` · offsets: `verified_offsets.v001.json`.**
**It re-runs green: 94 of 94, exit 0.** Six of my own transcriptions failed on the first run and were
corrected against the source rather than kept — the slip opinion sets nested quotation marks with a space
(`“ ‘bad tip.’ ”`), the district court puts *precautionary measures* in quotation marks, the transcript
carries a soft hyphen (U+00AD) inside `but -­ but`, and D15 is a block quotation that opens `[t]he`.
**A quotation typed from memory of what a sentence "should" say will not match. If a quotation you want is
not in this ledger, run it through the verifier before it goes on screen.**

### Sources tried and not reached

| Wanted | Result |
|---|---|
| **WSB-TV Atlanta** (local reporting on the family, incl. the post-SCOTUS interview) | **HTTP 451.** `wsbtv.com` geo-blocks: *"It appears you are attempting to access this website from a country outside of the United States, therefore access cannot be granted at this time."* This machine is outside the US. |
| **11Alive (WXIA)** | **HTTP 403** to a browser-UA curl. |
| **CourtListener web pages and the SCOTUS docket page via WebFetch** | **HTTP 403** on both. Both were obtained instead — the docket by browser-UA curl, the court documents through the authenticated v4 API and the RECAP storage host. |
| **S. Rep. No. 93–588 (1973)** itself | **NOT RETRIEVED (○-01).** Everything this film says about what the Senate committee found and intended comes from **the concurrence quoting it** (S21, S22) and is attributed that way on screen. |
| **Boger, Gitenstein & Verkuil, 54 N. C. L. Rev. 497 (1976)** — the Collinsville account | **NOT RETRIEVED (○-02).** Same treatment: the film quotes the concurrence quoting the article, and says so. |
| **The administrative tort claim of 25 October 2018** and any sum certain in it | **NOT RETRIEVED (○-03).** Its existence and date are established from the complaint (C01). **No dollar figure for this case exists anywhere in this ledger**, and none may be spoken (⛔-13). |
| **The FBI's Operation Order, the SWAT Addendum, Guerra's tactical notes, the site-survey photographs, the geolocation exhibits** | **NOT RETRIEVED (○-04).** They are described in DCT and were sealed in part — the district docket records four envelopes of sealed exhibits going to the Supreme Court and coming back on 29 August 2025 (N03). Everything the film says about them is DCT's description of them. |
| **Any FBI recording of the raid** | **It does not exist in the record.** IJ, whose own media page publishes the Atlanta Police Department body-camera footage of officers staged *outside* the house, states there is **"No footage from the FBI SWAT team available"** (J02). This is a fact about the case, not a gap in this pass. |
| **Rights clearance for the IJ body-camera footage** | ○-05. IJ's media page states *"Video assets are free to use. Credit 'Institute for Justice' if necessary."* **That sentence was read but the licence was not run through the rights gate.** No frame of it enters a cut until `09_package/rights_prescreen` says so. |

---

## 2. ⚠ THE TRAPS — read before writing a line

**1. THE RECORD CONTAINS TWO INCOMPATIBLE ACCOUNTS OF THE SAME FIVE MINUTES, AND BOTH ARE PRIMARY.**
The family swore that an agent held Curtrina Martin at gunpoint **"for approximately one hour"** and that
G.W. was detained apart from his mother for approximately one hour (C05). The district court found, on the
summary-judgment record, that **"The agents were in the home for no more than five minutes"** and that
**"No agent touched Martin"** (D07, D08). Both are in this ledger. **Neither may be spoken in the film's own
voice.** Every reference is attributed — *the family swore* / *the court found* — and the gap between them is
a scene, not an error to be smoothed. This is the single largest integrity hazard in the episode and it is
also its best five minutes of television.

**2. THE SUPREME COURT'S SUMMARY OF THE PROCEDURAL HISTORY IS TRUE AND INCOMPLETE.** It says "the district
court rejected each of the plaintiffs' claims and granted summary judgment to the government." That is the
net result of **two** orders fifteen weeks apart. On **23 September 2022** the court dismissed Counts III, IV,
V and VI and **denied** the government summary judgment on Counts I and II (D14) — the family had two claims
alive. Mediation was ordered (D17), held on **1 November 2022**, and **"Case did not settle"** (N01). The
government then moved for reconsideration on the strength of *Kordash*, decided about a month after the
order (R02), and on **30 December 2022** the same judge dismissed Counts I and II and closed the case (R01,
R06). **A film that says "they lost at summary judgment" throws away the true shape of the story.**

**3. "NO-KNOCK" IS CONTESTED IN THE SAME RECORD.** The complaint pleads a **"no-knock warrant"** and the
Eleventh Circuit's opinion calls it a **"no-knock search warrant"** (A-source language). The district court
found that Guerra **knocked and announced** and that the team waited **"ten to twenty seconds"** before
breaching (D06). Attribute; never assert.

**4. TWO DIFFERENT TIMES OF DAY.** The complaint says approximately **4:00–4:30 a.m.** (CMPL ¶10). Every court
document says the team entered **at or about 5:00 a.m.**, and the warrants were scheduled for 5:00 a.m. (D02,
D06). **The film uses 5:00 a.m.**, because it is the finding and because the warrant's own schedule
corroborates it. The complaint's earlier time is not used at all.

**5. THE INSTITUTE FOR JUSTICE PAGE CONTAINS AN ADDRESS ERROR.** It writes that Guerra *"had input 3731
Landau Lane."* Every court document, including the Supreme Court's, says **3741 Landau Lane**. **3741 is the
address. 3731 does not appear in this film.** IJ is counsel for one side; this ledger uses it only for
matters no court decided, and each such row is labelled.

**6. THERE IS A SEVEN-YEAR-OLD AT THE CENTRE OF THIS STORY AND HE IS A REAL PERSON WHO IS NOW ABOUT SIXTEEN.**
The courts call him **G. W.** His own counsel names him. **This film does not.** It does not depict him, does
not name him, does not state his age today, does not say where he lives or goes to school, and does not
invent a single interior thought for him. What the film may say about him is exactly the four sentences the
complaint gives (C06, C07, C08, C11) and the one line the Supreme Court gives. The machine half of that
decision is the `child`-family block in `forbidden_subjects` and rows ⛔-11 and ⛔-18 below.

**7. NOBODY HAS BEEN FOUND LIABLE FOR ANYTHING, AND THE CASE IS NOT OVER.** As of **12 August 2026** the
Eleventh Circuit heard argument on remand on **25 March 2026** (T04) and, on the record retrieved, **has not
ruled**. Agent Guerra has not been found to have violated the Fourth Amendment — the courts held the
opposite (R04, A03). No damages have been awarded. **The film is written in the present tense of an open
case**, and every characterisation of the officers' conduct is *alleged*, *the family swore*, or *the court
found*.

---

## 3. THE RAID — 18 October 2017

| ID | Claim | Grade | Source |
|---|---|---|---|
| F-01 | *"In the predawn hours of October 18, 2017, the Federal Bureau of Investigation raided the wrong house in suburban Atlanta."* | ✓ VERBATIM | SC · S01 |
| F-02 | *"Officers meant to execute search and arrest warrants at a suspected gang hideout, 3741 Landau Lane. Instead, they stormed a quiet family home, 3756 Denville Trace, occupied by Hilliard Toi Cliatt, his partner Curtrina Martin, and her 7-year-old son G. W."* | ✓ VERBATIM | SC · S02 |
| F-03 | *"A six-member SWAT team, led by FBI Special Agent Lawrence Guerra, breached the front door and detonated a flash-bang grenade."* | ✓ VERBATIM | SC · S03 |
| F-04 | *"Fearing a home invasion, Mr. Cliatt and Ms. Martin hid in a bedroom closet."* | ✓ VERBATIM | SC · S04 |
| F-05 | *"But the SWAT team soon found the couple's hiding spot, dragged Mr. Cliatt from the closet, 'threw [him] down on the floor,' handcuffed him, and began 'bombarding [him] with questions.'"* | ✓ VERBATIM | SC · S05 |
| F-06 | *"Meanwhile, another officer trained his weapon on Ms. Martin, who was lying on the floor half-naked, having fallen inside the closet."* | ✓ VERBATIM | SC · S06 |
| F-07 | *"Only then did another officer stumble across some mail with the home's address on it and realize the team had the wrong house."* | ✓ VERBATIM | SC · S07 |
| F-08 | The team entered at or about 5:00 a.m., after Guerra knocked, announced, and the team waited *"ten to twenty seconds"*. **Court finding, attributed.** | ✓ VERBATIM | DCT · D06 |
| F-09 | *"The agents were in the home for no more than five minutes."* **Court finding, attributed. Never spoken as the film's own account — see trap 1.** | ✓ VERBATIM | DCT · D08 |
| F-10 | *"The agents removed Cliatt from the closet, dragged him to the bedroom floor and handcuffed him. No agent touched Martin."* **Court finding, attributed.** | ✓ VERBATIM | DCT · D07 |
| F-11 | *"At or about 5:07 a.m., Guerra and the team executed the warrants at 3741 Landau. Guerra thereafter returned to Plaintiffs' home and apologized for the error. He provided his business card and took photographs of the damage caused by the forced entry."* | ✓ VERBATIM | DCT · D09 |
| F-12 | The family's sworn account: *"Ms. Martin was screaming 'no – I have to get [G.W.].' But Mr. Cliatt pulled her through the bathroom into the adjacent closet and closed the door. She kept repeating that she had to get her child."* | ✓ VERBATIM | CMPL · C02 |
| F-13 | *"Mr. Cliatt took her to the closet because that is where he keeps his shotgun – he planned on defending them against the unknown invaders."* | ✓ VERBATIM | CMPL · C03 |
| F-14 | *"Luckily, the agents opened the closet doors before Mr. Cliatt reached his firearm."* **The near-miss. This is the sentence the whole film hangs on and it is the family's own.** | ✓ VERBATIM | CMPL · C04 |
| F-15 | *"An agent held Ms. Martin at gunpoint in the corner of the closet for approximately one hour."* **Family's sworn allegation, attributed. Contradicted by F-09.** | ✓ VERBATIM | CMPL · C05 |
| F-16 | *"G.W. woke up terrified from the sounds of ramming the door open and the loud bangs from the flash grenades."* | ✓ VERBATIM | CMPL · C06 |
| F-17 | *"G.W. pulled the covers over his head hoping whoever was busting into the home would not see him."* | ✓ VERBATIM | CMPL · C07 |
| F-18 | *"G.W. was so afraid that he thought he was going to die."* | ✓ VERBATIM | CMPL · C08 |
| F-19 | *"The Plaintiffs had no idea why the agents were in their home."* | ✓ VERBATIM | CMPL · C12 |
| F-20 | IJ's account of the turn: *"Agents angrily shouted questions at Toi, but when he told them his address, the room went silent."* **Counsel's account, attributed if used, never the film's own voice.** | ✓ (party account) | IJ · J04 |

---

## 4. WHY IT HAPPENED — the preparation, and what could not be checked afterwards

| ID | Claim | Grade | Source |
|---|---|---|---|
| G-01 | *"In 2015, the FBI initiated an operation concerning violent gang activity in Georgia. The operation ultimately resulted in criminal indictments against thirty individuals, including Joseph Riley"* | ✓ VERBATIM | DCT · D01 |
| G-02 | The operation's name: *"In 2015, the FBI initiated Operation Red Tape—an operation concerning violent gang activity in Georgia."* | ✓ VERBATIM | CA11 · A01 |
| G-03 | *"the Operation Order provided that seven search warrants and seventeen arrest warrants, including warrants for Riley's arrest and the search of his home located at 3741 Landau Lane SW, Atlanta, Georgia ('3741 Landau'), would be executed simultaneously on October 18, 2017, at 5:00 a.m."* | ✓ VERBATIM | DCT · D02 |
| G-04 | *"But, he says, when he used his personal GPS to navigate to 3741 Landau Lane on the day of the raid, it led him to 3756 Denville Trace."* | ✓ VERBATIM | SC · S08 |
| G-05 | *"And it seems the agents neither noticed the street sign for 'Denville Trace,' nor the house number, which was visible on the mailbox at the end of the driveway."* | ✓ VERBATIM | SC · S10 |
| G-06 | *"Plaintiffs' home, which also faces Landau Lane, is three or four houses down from 3741 Landau. The address of 3756 Denville is not affixed to the front of the home or anywhere else on the building. It is posted on the mailbox at the end of the driveway on the side of the house located on Denville Trace."* **The detail that makes the mistake comprehensible and the failure to check it worse.** | ✓ VERBATIM | DCT · D05 |
| G-07 | *"Guerra and Lemoine both testified that they observed a black Camaro car in the driveway of the home, which Guerra noted as a future reference point."* | ✓ VERBATIM | DCT · D03 |
| G-08 | *"Riley was not known to operate a black Camaro car or associate with anyone who did."* **The landmark the team navigated by belonged to the wrong house.** | ✓ VERBATIM | DCT · D04 |
| G-09 | *"Apparently, too, Agent Guerra failed to appreciate that a different car was parked in the driveway, one 'not present . . . during [his] previous visit.'"* | ✓ VERBATIM | SC · S11 |
| G-10 | *"No one could confirm as much later because Agent Guerra 'threw . . . away' his GPS device 'not long after' the raid."* | ✓ VERBATIM | SC · S09 |
| G-11 | *"Guerra testified that he stopped using his personal GPS device after the incident, and he threw it away not long after that. The device was therefore not available for Plaintiffs' inspection during discovery or for corroboration of Guerra's testimony."* | ✓ VERBATIM | DCT · D10 |
| G-12 | *"However, no FBI policy or procedure dictates how to locate or navigate to the target, whether to use a GPS device or what type of GPS device must be used, whether or how to conduct a site survey or drive-by of a target location or how long to wait before entering after knocking and announcing."* **The FBI's own agency representative. This is the System Map's centre: there was no rule to break.** | ✓ VERBATIM | DCT · D11 |
| G-13 | *"the FBI was unable to find geo location data for seven of the sixteen FBI personnel who participated in the warrant executions"* | ✓ VERBATIM | DCT · D12 |
| G-14 | *"Despite taking several precautionary measures to ensure proper execution of the search warrant, Guerra and the FBI agents inadvertently executed the search warrant at the wrong house."* **The appellate court's framing, and the film must state it as fairly as it states the family's.** | ✓ VERBATIM | CA11 · A02 |
| G-15 | *"The Court considers Guerra's overall preplanning to constitute significant 'precautionary measures' to avoid mistake."* | ✓ VERBATIM | DCT · D16 |
| G-16 | IJ's account: *"the team used a black Camaro as a landmark even though neither the drug dealer nor his associates drove one."* **Counsel's account; the underlying fact is independently established at G-07/G-08.** | ✓ (party account) | IJ · J03 |

---

## 5. THE AFTERMATH — what the raid cost, and the paperwork years

| ID | Claim | Grade | Source |
|---|---|---|---|
| H-01 | *"Left with personal injuries and property damage—but few explanations and no compensation—Mr. Cliatt and Ms. Martin sued the United States."* | ✓ VERBATIM | SC · S12 |
| H-02 | *"The Plaintiffs required long-term counseling to deal with the severe emotional distress stemming from the erroneous warrant execution."* | ✓ VERBATIM | CMPL · C09 |
| H-03 | *"Plaintiff Martin was forced to take approximately seven months of leave from her job due to her emotional distress."* | ✓ VERBATIM | CMPL · C10 |
| H-04 | *"Plaintiff G.W. was forced to change schools on two occasions due to his emotional state."* | ✓ VERBATIM | CMPL · C11 |
| H-05 | *"Plaintiffs provided Defendant United States' Federal Bureau of Investigation (FBI) detailed tort claims notices on October 25, 2018."* **The first paper. One year and one week after the raid.** | ✓ VERBATIM | CMPL · C01 |
| H-06 | Martin and G.W. filed suit on **11 September 2019** (ECF 1); Cliatt filed separately on **18 September 2019** (No. 1:19-cv-04180); the cases were consolidated. | ✓ | DDKT, `RAW_docket_gand_1_19cv4180_cliatt.json`, DCT n.1 |
| H-07 | IJ's account of the money: *"Insurance in this case covered the physical damage to the house, but it didn't cover the monetary damage of the couple's lost wages due to trauma or the therapy Gabe needed because of post-traumatic stress."* **Counsel's account, attributed. This is the only statement in the whole ledger about what anybody was actually paid, and it is not a payment by the government.** | ✓ (party account) | IJ · J01 |
| H-08 | ✓ (arithmetic, **ours**) From the raid (18 Oct 2017) to the remand argument (25 Mar 2026) is **8 years, 5 months and 7 days**. To the writing of this ledger (12 Aug 2026), **8 years, 9 months and 25 days**. To the filing of the tort claim (25 Oct 2018), **1 year and 7 days**. Stated as our arithmetic, never attributed. | ✓ (arithmetic) | ours, on F-01, H-05, T04 |

---

## 6. THE LAW — what the case was actually about

| ID | Claim | Grade | Source |
|---|---|---|---|
| L-01 | *"If federal officers raid the wrong house, causing property damage and assaulting innocent occupants, may the homeowners sue the government for damages? The answer is not as obvious as it might be."* — the Court's own opening sentence. | ✓ VERBATIM | SC · S13 |
| L-02 | *"But the statute's waiver is subject to 13 exceptions that claw back the government's immunity in certain circumstances."* | ✓ VERBATIM | SC · S16 |
| L-03 | The five FTCA counts: *"false arrest/false imprisonment (Count I), assault and battery (Count II), trespass/interference with private property (Count III), negligent/intentional infliction of emotional distress (Count IV) and negligence (Count V)."* Count VI was the *Bivens* claim against Guerra personally. | ✓ VERBATIM | DCT · D13 |
| L-04 | The Eleventh Circuit precedent that decided the negligence claims before anyone looked at the facts: *"[t]he decision as to how to locate and identify the subject of an arrest warrant prior to service of the warrant is susceptible to policy analysis."* — *Mesa v. United States*, 123 F.3d 1435 (11th Cir. 1997), quoted by the district court. | ✓ VERBATIM | DCT · D15 |
| L-05 | 23 Sept 2022: *"the Court GRANTS Defendants' Motion (ECF No. 83) as to Counts III, IV, V and VI of the complaints and DENIES the Motion as to Counts I and II."* | ✓ VERBATIM | DCT · D14 |
| L-06 | The court then ordered mediation: *"the parties are DIRECTED to mediate the remaining claims in this matter before a neutral third party within forty-five days of the date of this Order."* | ✓ VERBATIM | DCT · D17 |
| L-07 | 1 November 2022: *"Mediation held on 11/1/2022. Case did not settle."* | ✓ VERBATIM | DDKT · N01 |
| L-08 | The government's ground for reconsideration: *"it argues that the Eleventh Circuit Court of Appeals' opinion in Kordash v. United States, 51 F.4th 1289 (11th Cir. 2022), which was issued approximately one month after this Court issued its Order, is an intervening development in controlling law that requires dismissal of Plaintiffs' FTCA claims."* | ✓ VERBATIM | RECON · R02 |
| L-09 | The court's own concession: *"The Court acknowledges that the United States could have possibly raised its Supremacy Clause argument earlier."* | ✓ VERBATIM | RECON · R03 |
| L-10 | 30 December 2022: *"the Supremacy Clause bars Plaintiffs' state law claims brought pursuant to the FTCA, and Counts I and II of the complaints are dismissed."* | ✓ VERBATIM | RECON · R01 |
| L-11 | *"As a result, Counts I and II of Plaintiffs' complaints are DISMISSED. Since these dismissals resolve the only remaining claims in this matter, the Clerk is DIRECTED to close the case."* | ✓ VERBATIM | RECON · R06 |
| L-12 | Why Guerra personally walked: *"The Court found that the law was not clearly established at the time of the incident such that Guerra would have known that his actions in this case would be deemed unreasonable and violative of the law."* | ✓ VERBATIM | RECON · R04 |
| L-13 | On the destroyed GPS: *"the Court acknowledged and contended with the consequence of the unavailable GPS data and still found that Guerra was entitled to qualified immunity."* | ✓ VERBATIM | RECON · R05 |
| L-14 | 22 April 2024, Eleventh Circuit, unpublished, no argument, panel of **Lagoa, Brasher and Abudu**: *"we AFFIRM the district court's grant of summary judgment based on qualified immunity in favor of Guerra and dismissal of the FTCA claims against the United States on the grounds that the Supremacy Clause and the discretionary function exception bar those claims."* | ✓ VERBATIM | CA11 · A03, A04 |
| L-15 | 27 January 2025, cert granted, limited to two questions, the first being *"Whether the Constitution's Supremacy Clause bars claims under the Federal Tort Claims Act when the negligent or wrongful acts of federal employees have some nexus with furthering federal policy and can reasonably be characterized as complying with the full range of federal law."* | ✓ VERBATIM | SDKT · K01 |
| L-16 | 29 April 2025: *"Argued. For petitioners: Patrick M. Jaicomo, Arlington, Va. For respondents: Frederick Liu, Assistant to the Solicitor General, Department of Justice, Washington, D. C."* | ✓ VERBATIM | SDKT · K02 |
| L-17 | 12 June 2025: *"Judgment VACATED and case REMANDED."* / *"GORSUCH, J., delivered the opinion for a unanimous Court. SOTOMAYOR, J., filed a concurring opinion, in which JACKSON, J., joined."* | ✓ VERBATIM | SDKT · K03; SC · S15 |
| L-18 | *"The Supremacy Clause does not afford the United States a defense in FTCA suits."* | ✓ VERBATIM | SC · S27 |
| L-19 | *"The judgment of the Eleventh Circuit is vacated, and the case is remanded for further proceedings consistent with this opinion."* | ✓ VERBATIM | SC · S14 |
| L-20 | **What the Court did NOT decide** — the sentence that keeps the film honest: *"Remaining questions surrounding whether and under what circumstances the discretionary-function exception may ever foreclose a suit like this one lie well beyond the two questions the Court granted certiorari to address"*. | ✓ VERBATIM | SC · S25 |
| L-21 | And the Court's answer to the family's best argument: *"Legislative history suggesting Congress intended to address wrong-house raids broadly cannot displace what the law's terms clearly direct, as legislative history is not the law"*. **The film states this. A film that only quotes Sotomayor is an advocacy film.** | ✓ VERBATIM | SC · S26 |

---

## 7. THE ORAL ARGUMENT — 29 April 2025 · real recorded voices, public domain

**This is the Moment of Truth.** A US Government work; the audio is published by the Court.

| ID | Claim | Grade | Source |
|---|---|---|---|
| Q-01 | JUSTICE SOTOMAYOR: *"Oh, he had it identified. He got the right target. He just had the wrong house."* | ✓ VERBATIM | OA · O04 |
| Q-02 | JUSTICE SOTOMAYOR: *"I'm talking about a wrong-house raid. He has the right target, the right house, but -- but breaks into the wrong one."* | ✓ VERBATIM | OA · O05 |
| Q-03 | JUSTICE SOTOMAYOR: *"So I don't understand how the act of going into a wrong house can be discretionary."* | ✓ VERBATIM | OA · O06 |
| Q-04 | MR. LIU: *"Well, we understand the discretion here to be the discretion as to how to identify the target of a search warrant."* | ✓ VERBATIM | OA · O07 |
| Q-05 | JUSTICE GORSUCH: *"Yeah, you might look at the address of the house before you knock down the door."* | ✓ VERBATIM | OA · O01 |
| Q-06 | MR. LIU: *"-- number at the end of the driveway means exposing the agents to potential lines of fire from the windows"* — the government's stated reason why checking the house number is a policy judgement. **State it fully and fairly; it is the system's own rationale and §9 of the editorial direction requires it before the failure is shown.** | ✓ VERBATIM | OA · O02 |
| Q-07 | JUSTICE GORSUCH: *"How about making sure you're on the right street?"* | ✓ VERBATIM | OA · O03 |

---

## 8. COLLINSVILLE, APRIL 1973 — why the law exists at all

**Every row here is the concurrence quoting a law-review article and a Senate report. The film says so.**

| ID | Claim | Grade | Source |
|---|---|---|---|
| E-01 | *"In April 1973, Herbert and Evelyn Giglotto awoke in their Collinsville, Illinois, townhouse 'to the sound of someone smashing down their door and bursting into their house.'"* | ✓ VERBATIM (as quoted in SC) | SC · S18 |
| E-02 | *"After 15 state and federal officers ransacked the Giglottos' home, tied them up at gunpoint, and threatened to shoot Mr. Giglotto if he moved, the officers realized they 'ha[d] the wrong people.'"* | ✓ VERBATIM (as quoted in SC) | SC · S19 |
| E-03 | *"The officers eventually moved on to the home of Donald Askew, where they terrorized yet another innocent couple before confessing they had acted on a 'bad tip.'"* | ✓ VERBATIM (as quoted in SC) | SC · S20 |
| E-04 | *"Noting that '[t]here [was] no effective legal remedy against the Federal Government for the actual physical damage, much less the pain, suffering and humiliation to which the Collinsville families ha[d] been subjected,' the Senate Committee on Government Operations proposed an amendment to the FTCA."* | ✓ VERBATIM (as quoted in SC) | SC · S21 |
| E-05 | *"The Committee designed the proviso to ensure 'innocent individuals who are subjected to raids of the type conducted in Collinsville, Illinois, will have a cause of action against the individual Federal agents [and] the Federal Government'."* | ✓ VERBATIM (as quoted in SC) | SC · S22 |
| E-06 | *"Whatever else is true of that exception, any interpretation should allow for liability in the very cases Congress amended the FTCA to remedy."* | ✓ VERBATIM | SC · S24 |
| E-07 | *"It has been 34 years since this Court last weighed in on the discretionary-function exception"* (i.e. since *Gaubert*, 1991). | ✓ VERBATIM | SC · S23 |
| E-08 | ✓ (arithmetic, **ours**) The Collinsville raids were in **April 1973**; the raid on 3756 Denville Trace was in **October 2017**. **Forty-four years and six months.** Stated as our arithmetic. | ✓ (arithmetic) | ours, on E-01, F-01 |

---

## 9. WHERE IT STANDS TODAY — 12 August 2026

**This section was re-verified last, immediately before the spec was written, because it is the only part of
the film that can go stale between now and publication. Re-verify it again before the render and again
before the schedule.**

| ID | Claim | Grade | Source |
|---|---|---|---|
| N-01 | 12 June 2025, on the Eleventh Circuit's own docket: *"Writ of Certiorari filed as to Appellant Curtrina Martin is GRANTED. The judgment of the Eleventh Circuit is VACATED and the case is REMANDED to the Eleventh Circuit."* | ✓ VERBATIM | ADKT · T01 |
| N-02 | 29 August 2025, on the district court's docket: *"Appeal Record Returned from USSC"* — one box, four envelopes of sealed exhibits, back where it started. **This is the last entry on the district docket.** | ✓ VERBATIM | DDKT · N03 |
| N-03 | 22 September 2025: *"Appellant's Supplemental Brief filed by Appellants Hilliard Toi Cliatt, G.W. and Curtrina Martin."* Appellee's supplemental brief 21 November 2025; appellants' supplemental reply 12 December 2025. | ✓ VERBATIM (T02) + ✓ (ADKT entries 62, 67) | ADKT |
| N-04 | 23 January 2026: *"Oral argument scheduled. Argument Date: Wednesday, 03/25/2026 Argument Location: Atlanta Courtroom: Atlanta 339."* | ✓ VERBATIM | ADKT · T03 |
| N-05 | 25 March 2026: *"Oral argument held this date. Oral Argument presented by Patrick M. Jaicomo for Appellants Curtrina Martin, G.W. and Hilliard Toi Cliatt and Aaron Ross for Appellees USA and Lawrence Guerra."* **This is the last entry of record on the appellate docket.** | ✓ VERBATIM | ADKT · T04 |
| N-06 | *"It marks the second time the botched raid case has come before the federal appeals court"*. | ✓ VERBATIM | CNS · W07 |
| N-07 | The panel on remand, and the state of play: *"Jordan was joined on the panel by U.S. Circuit Judge Jill Pryor, a fellow Obama appointee, and U.S. Circuit Judge Embry Kidd, a Joe Biden appointee. They did not signal when they intend to release a ruling, as they may request supplemental briefing from the parties on the case."* | ✓ VERBATIM | CNS · W06 |
| N-08 | Judge Adalberto Jordan, from the bench: *"We have over 60 published cases since 1990 on the discretionary function exemption and they are all over the place"*. | ✓ VERBATIM | CNS · W01 |
| N-09 | Judge Jordan again: *"You can only execute a warrant, a search or arrest warrant, at the place described in the warrant"* / *"There's no level of discretion involved there."* | ✓ VERBATIM | CNS · W02, W03 |
| N-10 | Patrick Jaicomo, for the family: *"Actions are still legal or illegal regardless whether you're an FBI agent or a private person"* / *"We should not ignore the elephant in the room here that Congress amended the FTCA to prevent wrong home raids."* | ✓ VERBATIM | CNS · W04, W05 |
| N-11 | **No decision has issued.** Established four ways, all by this pass: the appellate docket's last entry is the 25 March 2026 argument (T04); the CourtListener docket record carries `date_last_filing` 2026-03-25; a CourtListener opinion search restricted to `court=ca11, filed_after=2025-06-13` for *Cliatt*, *"Denville Trace"* and *Guerra wrong house* returns **0**; and a web search for a 2026 Eleventh Circuit ruling returns nothing later than the argument. | ✓ (four independent negatives) | ADKT, CourtListener API, web search |
| ○-06 | **What the panel will do is unknown and unknowable.** No prediction, no "expected to rule", no "likely". The film ends on the open question because that is the truth on 12 August 2026. | ○ | — |

---

## 10. ⛔ QUARANTINE — the sentences this film may never say

These are the machine half of the same decision. Each is carried into
`episodes/PD-2026-070-wronghouse/episode_spec.v001.json` `forbidden_claims`, so a tool can check for them.

| ID | Barred | Why |
|---|---|---|
| ⛔-01 | *"She was held at gunpoint for an hour"* in the film's own voice — or *"the agents were only in the house five minutes"* in the film's own voice. | Both are in the record, from opposite sides, and they cannot both be true (trap 1). Attribution is mandatory: *the family swore* / *the court found*. |
| ⛔-02 | Any statement that Guerra, or the FBI, **lied**, **covered up**, **destroyed evidence**, or threw the GPS away **in order to** destroy evidence. | The district court expressly declined to decide spoliation because the plaintiffs deferred it (RECON §3). No tribunal has found it. The film may state exactly what the Supreme Court states (G-10) and stop. |
| ⛔-03 | Any statement that Guerra was found liable, disciplined, suspended, fired, prosecuted, or found to have violated the Fourth Amendment. | The opposite is on the record: qualified immunity, and an express finding that his actions did not violate the Fourth Amendment (L-12, R04). Nothing about any employment consequence exists in this ledger. |
| ⛔-04 | Any statement that the family **won**, was **paid**, **recovered damages**, or **received compensation from the government**. | As of 12 August 2026 they have recovered nothing under the FTCA. The only payment anywhere in this ledger is a private insurer covering physical damage to the house, and that is counsel's account (H-07). |
| ⛔-05 | Any statement that the Supreme Court held the family should win, that it found the FBI liable, or that it "ruled for the family" without saying what it actually decided. | It decided two legal questions, vacated, and expressly left the deciding question open (L-19, L-20). |
| ⛔-06 | Any statement that the case is **over**, **decided**, **finished**, or that the Eleventh Circuit has ruled — and any prediction of what it will do. | N-11, ○-06. |
| ⛔-07 | *"No-knock raid"* asserted as fact in the film's own voice. | Contested inside the record (trap 3). Attribute to the pleading or to the appellate opinion's language. |
| ⛔-08 | *"3731 Landau Lane"*, or any address other than **3741 Landau Lane** and **3756 Denville Trace**. | IJ's page carries the error (trap 5). |
| ⛔-09 | Any characterisation of **Joseph Riley** beyond what the opinions say — that warrants were issued for his arrest and for the search of his home at 3741 Landau, and that the FBI determined he posed a high risk of violence. Never *convicted*, never *the drug dealer* in the film's own voice, never depicted. | He is a real named person and this film made no findings about him. |
| ⛔-10 | Any dollar figure attached to this case: what was claimed, what was demanded, what was offered at mediation, what the house cost to repair, what the therapy cost. | ○-03. Nothing was retrieved. The absence is itself a line the film can speak — *no number was ever put on it, because no court ever got that far* — but no number may be invented. |
| ⛔-11 | The child's surname, his age today, his school, his town, his current condition, any invented thought, any dramatised moment beyond F-16/F-17/F-18, and any image of a child at all. | Trap 6. |
| ⛔-12 | Any statement about whether Curtrina Martin and Toi Cliatt are still together, or any causal claim about their relationship. | Not in any retrieved document, and not the film's business. |
| ⛔-13 | *"The FBI refused to pay"* in the film's own voice. | That is IJ's headline, not a retrieved fact. The United States litigated immunity; no refusal-to-pay document was retrieved. Attribute to counsel or drop. |
| ⛔-14 | Any count, rate or trend of wrong-house raids — *"this happens X times a year"*, *"hundreds"*, *"it keeps happening"* with a number attached. | Nothing in this ledger supports a number. The pattern the film may show is the named one: Collinsville 1973 (E-01…E-03), *Mesa* 1997 (L-04), and the fact that the Eleventh Circuit had already applied the exception to a wrong-home warrant service (DCT's citation of *Vivas*). Named cases only. |
| ⛔-15 | Any Collinsville detail beyond E-01…E-05, and any statement that all fifteen officers were federal. | ○-02. The concurrence's quotation is the whole of our knowledge. |
| ⛔-16 | Any statement that FBI body-camera or surveillance footage of the raid exists, or presenting the Atlanta Police Department footage as footage of the raid itself. | J02: it is footage of officers staged **outside** the house, and there is none from the SWAT team. |
| ⛔-17 | *"The government said checking the address was optional"* — the working-title shorthand — as a quotation. | The government's actual position is Q-06 and it is more specific and more interesting than the paraphrase. Paraphrase only outside quotation marks, and only next to the real words. |
| ⛔-18 | Any generated image presented as an authentic record: the warrant, the Operation Order, the SWAT Addendum, a photograph of either house, the GPS device, a page of the court file, a docket sheet, a newspaper front page, body-camera footage, or a likeness of Curtrina Martin, Toi Cliatt, the child, Lawrence Guerra, Joseph Riley, any agent, any judge, any justice or any lawyer. | CLAUDE invariant 11 and the standing no-real-likeness rule. Illustration is allowed; evidence is not manufactured. |
| ⛔-19 | Any political framing — an administration, a party, a movement, a president's name, an election — attached to this raid, this agency or these courts. | Editorial direction §9. The panel's appointing presidents are in CNS (W06) and are **not** used: naming them would import exactly the colour the brand forbids. |
| ⛔-20 | *"4 a.m."* as the time of the raid. | Trap 4. The film uses 5:00 a.m. |

---

## 11. What this ledger does not contain, stated so no absence is later mistaken for a finding

1. **Anything either family member has said publicly since June 2025.** Curtrina Martin is widely quoted
   saying the ruling *"is a victory for us but also for everyone who is fighting for accountability and
   justice"* — that quotation appears in a SCOTUSblog piece this pass fetched, and in reporting this pass
   could **not** reach (WSB-TV geo-blocked, 11Alive 403). **It is therefore not in the ledger and may not be
   used.** If it is wanted, retrieve the original.
2. **What happened at the 1 November 2022 mediation.** Confidential. Only "did not settle" (L-07).
3. **What the sealed exhibits contain.** Four envelopes, never opened by anyone outside the case.
4. **Whether Agent Guerra is still with the FBI**, and anything else about any individual agent's life.
5. **The Eleventh Circuit's audio of the 25 March 2026 argument.** The docket says it is published on the
   court's website (ADKT entry 75). **It was not downloaded this pass.** If the film wants that voice, it is
   a retrieval task, not an assumption — and it is the single highest-value open lead in this file.
6. **Any 2026 development after 25 March.** Re-verify §9 before render and again before scheduling.
