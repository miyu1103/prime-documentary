# EP69 · THE KANSAS CITY HYATT REGENCY WALKWAYS — FACTS LEDGER v001

**Episode:** EP69 · ID `PD-2026-069-hyatt` · slug `hyatt` · topic `TOP-20260811-069`
**Event:** collapse of the second- and fourth-floor suspended walkways, Hyatt Regency Hotel, Kansas City, Missouri, **17 July 1981, approximately 7:05 p.m.**
**Purpose:** every factual claim the film may make, with its grade and its source.

**Invariant 1: no unsupported factual statement enters an approved script.** A claim graded ○ may not be
spoken, shown, put in a telop, or written into a title until it is upgraded.

**Grades:** ✓ **VERBATIM** = quoted word-for-word from a document retrieved and read by this pass, located by
exact string search · ✓ = established from a source retrieved by this pass · ✓ (arithmetic) = our own
calculation on verbatim figures, **labelled as ours, never attributed to a source** · ○ = research
instruction, **NOT a fact** · ⛔ = quarantined, do not use.

---

## PRIMARY SOURCES — and, for this pass, the ONLY sources

| Tag | Document | Retrieved this pass |
|---|---|---|
| **NBS** | **NBS Building Science Series 143**, *Investigation of the Kansas City Hyatt Regency Walkways Collapse*, Marshall, Pfrang, Leyendecker, Woodward, Reed, Kasen, Shives — U.S. Department of Commerce / National Bureau of Standards, **May 1982**. The federal investigation. Complete, all 12 chapters. | **YES.** `nvlpubs.nist.gov/nistpubs/Legacy/BSS/nbsbuildingscience143.pdf` (27,072,712 bytes, sha256 `5f75a7b2c28883e3…`) → text `SRC-0001_nbs_bss143.txt`, **427,229 chars**, sha256 `713e7e5cfee068da…` |
| **MOCA** | ***Duncan, Gillum and GCE International, Inc. v. Missouri Board for Architects, Professional Engineers and Land Surveyors***, No. 52655, **744 S.W.2d 524** (Mo. Ct. App., E.D., Div. Three, **26 January 1988**). The published appellate record of the state disciplinary decision: the Administrative Hearing Commission's findings, the Board's revocation, and the affirmance. Complete opinion, 19 reporter pages, incl. all 12 footnotes. | **YES.** Harvard Caselaw Access Project static store, `static.case.law/sw2d/744/cases/0524-01.json` (CAP id 9974720, source Harvard, official reporter) → text `SRC-0002_duncan_744sw2d524.txt`, **66,251 chars**, sha256 `51f38fc52d6e6cfb…` |
| **JPCF** | Pfatteicher, S. K. A., **"'The Hyatt Horror': Failure and Responsibility in American Engineering"**, *ASCE Journal of Performance of Constructed Facilities*, **Vol. 14, No. 2, May 2000, pp. 62–66**, Paper No. 21947. Peer-reviewed ASCE; the standard scholarly account of the disciplinary and professional-ethics chain. | **YES.** Open-access copy of the published PDF (48,163 bytes) → text `SRC-0003_pfatteicher_jpcf_14_2_62.txt`, **36,269 chars**, sha256 `664d0f0f8e847fcb…` |

Cached under `episodes/PD-2026-069-hyatt/01_research/sources/`.
Machine verifier: **`verify_quotes.v001.py`** · offsets: `verified_offsets.v001.json`.

**Citation convention.** `@NNNNN` is the **character offset of the first character of the quoted string
inside the cached text file** named in the row. **Every ✓ VERBATIM row was located by exact string search
during this pass, and the verifier re-runs green: 136 of 136, exit 0.** One of my own transcriptions failed
on the first run (`M48` — the reporter breaks *Gillum* across a line as `Gil-lum`) and was corrected against
the source rather than kept.

### Sources I tried and could **not** reach

| Wanted | Result |
|---|---|
| **CourtListener** (task instruction: try the `.env` token) | **Still HTTP 429.** `GET /api/rest/v4/opinions/1529627/` with the 40-char `COURTLISTENER_TOKEN` → `{"detail":"Request was throttled. Rate limit exceeded: 125/day. Expected available in 16888 seconds."}` — i.e. ~4h40m from 2026-08-11. The v3 search endpoint returns 403. The CourtListener **web** page returns HTTP 202 with a zero-byte body (Cloudflare challenge); WebFetch on it returns empty. **The opinion was obtained instead from the Harvard Caselaw Access Project's copy of the official reporter, which is a better source than CourtListener for a 1988 state case.** No fact in this ledger depends on CourtListener. |
| **The Administrative Hearing Commission decision itself** — Deutsch, J. B., *Statement of the Case, Findings of Fact, Conclusions of Law and Decision*, `Missouri Board v. Duncan, Gillum and GCE International`, Case **AR-84-0239**, filed 15 November 1985, **442 pages** | **NOT RETRIEVED (○-01).** Not published in any reporter and not located online this pass. Everything in this ledger about what the Commission found comes from **MOCA quoting and reviewing it**, and from **JPCF quoting Judge Deutsch's page numbers**. That is enough to state the findings; it is **not** enough to narrate the twenty-seven days of hearing. |
| **Missouri Board's own revocation order** (22 January 1986) and its case file | **NOT RETRIEVED (○-02).** Its existence, date and content are established from MOCA @1445 and JPCF @23849 only. |
| ASCE Library full text (Moncarz & Taylor, *Engineering Process Failure — Hyatt Walkway Collapse*, JPCF 14(2):46–50; Luth, *Chronology and Context*, 14(2):51–61) | **NOT RETRIEVED (○-03).** `ascelibrary.org` serves a JavaScript shell with no abstract in the HTML; WebFetch returns 403 on the DOI page. The one JPCF paper obtained is Pfatteicher's. |
| Justia / Leagle / Casetext copies of 744 S.W.2d 524 | 403 / Cloudflare / 410. Irrelevant — the CAP copy is the official reporter text. |
| The original **structural design calculations** for the connection | **They do not exist in the record at all.** ✓ VERBATIM: *"Efforts to obtain copies of the structural design calculations were unsuccessful"* — NBS @41711. NBS also states the Office of the Mayor tried and failed. **This is a fact about the case, not a gap in this pass.** |

---

## ⚠ THE EXTRACTION TRAPS — read this before quoting anything

**Three separate traps. All three are live. All three would produce a "verbatim" quotation that is wrong.**

**1. BSS 143 is a scan-and-OCR document, and the OCR is imperfect in exactly the places the film cares
about.** The PDF NIST serves is a 1982 print scan. Confirmed corruptions in the cached text include
`vjould` for *would* (abstract), `SUE` for `8UE` (§10.2, §11), `celling` for *ceiling*, `flilet` for
*fillet*, `fall` for *fail*, `terras` for *terms*, `sura` for *sum*, `specif ied` for *specified*,
`connect ions` for *connections*, and randomly capitalised `In`/`Is`/`Information`. **Every ✓ VERBATIM row
below was chosen to avoid a corrupted span, and every one was located by exact string search in the cached
file.** A quotation typed from memory of what the sentence "should" say will not match. If a quotation you
want is not in this ledger, run it through `verify_quotes.v001.py` before it goes on screen.

**2. The abstract and the executive summary of BSS 143 differ from each other.** The abstract says the
original arrangement would have given *"the ultimate capacity"* of approximately 60 percent; a later
restatement in the same volume says *"the connection capacity"*. Same meaning, different words. Cite the
one you actually quoted.

**3. `SRC-0003` had its typographic ligatures expanded.** The published JPCF PDF encodes `fi`, `fl`, `ff`
as single Unicode ligature glyphs (U+FB01/FB02/FB00), so `final` extracts as `ﬁnal`. The cached
`SRC-0003_…txt` is the raw extraction with **only** those five ligature code points and U+2010 expanded to
their plain-ASCII equivalents — a lossless typographic expansion, applied so that offsets are stable and
quotations can be retyped. **Nothing else was altered.** JPCF also uses doubled-comma open quotes
(``‘‘`` / ``’’``) — reproduce them exactly or the search will fail.

---

## 0. GATE STATUS

| # | Gate | Status |
|---|---|---|
| 1 | Read the federal investigation (NBS BSS 143) end to end | **DONE.** All 12 chapters. The load arithmetic, the test programme, the occupancy estimate and all nine conclusions are read from the document, not from a retelling. |
| 2 | Retrieve the state disciplinary decision against the engineers of record | **DONE AS FAR AS IT CAN BE.** The **appellate** decision reviewing it (744 S.W.2d 524) is retrieved complete and quotes the Commission's findings extensively. The 442-page Commission decision itself is **○-01**. |
| 3 | ASCE / JPCF on the shop-drawing review chain | **PARTIAL.** Pfatteicher (JPCF 14(2):62–66) retrieved complete. Moncarz & Taylor and Luth in the same issue are **○-03**. **The review chain is nevertheless closed** — MOCA states it on the record, in more detail and with more authority than any journal paper (§7). |
| 4 | Death and injury counts from the official record | **DONE, AND THEY DISAGREE ACROSS TIME.** NBS (May 1982): 111 killed outright, 188 injured, *"Two of the injured subsequently died"* = 113. The Missouri Court of Appeals (1988): **114 died, at least 186 injured**. **Use 114.** The reconciliation between them is **⛔-03** — no retrieved document explains it. |
| 5 | CourtListener | **STILL THROTTLED (HTTP 429).** See the table above. Nothing depends on it. |
| 6 | Rights: third-party broadcast/news footage | **CLOSED BY RULE, NOT BY RESEARCH. NONE MAY BE USED.** ⛔-10. The film is built without it and §12 says what it uses instead. |
| 7 | Depiction: bodies, injured people, the crowded lobby at the moment of collapse | **DECIDED AND WRITTEN DOWN.** ⛔-11 … ⛔-14 and §12. The designer does not have to improvise this. |
| 8 | Named living or possibly-living individuals: **Daniel M. Duncan**, **Jack D. Gillum** | **CONSTRAINED.** ⛔-15 … ⛔-18. Criticism rests on MOCA and NBS, quoted, and nothing past them. |
| 9 | Named victims | **PERMANENTLY CLOSED. The film names no victim.** ⛔-12. Neither NBS nor MOCA names one; nothing has to be decided. |
| 10 | Novelty against EP60 surfside and EP68 pinto | **ANSWERED IN WRITING** in the topic record, `novelty_check`. Same family as EP60. Not a duplicate. Do not schedule adjacently. |

---

## 1. IDENTITY AND POSTURE

| ID | Claim | Grade | Source |
|---|---|---|---|
| ID-01 | The event: ✓ **"On July 17, 1981, at approximately 7:05 p.m., two suspended walkways within the atrium area of the Hyatt Regency Hotel in Kansas City, Mo., collapsed, killing 111 people and injuring 188. Two of the injured subsequently died."** | ✓ VERBATIM | NBS @20732 |
| ID-02 | **The number the film uses is 114.** ✓ **"On July 17, 1981, the second and fourth floor walkways of the Hyatt Regency Hotel in Kansas City collapsed and fell to the floor of the main lobby. Approximately 1500 to 2000 people were in the lobby. The walkways together weighed 142,000 pounds. One hundred and fourteen people died and at least 186 were injured."** | ✓ VERBATIM | MOCA @418 — the Missouri Court of Appeals, 1988, official reporter |
| ID-03 | Independently, in the ASCE literature: ✓ **"The final count of 114 dead and nearly 200 injured led one group of investigators to declare the Hyatt disaster ''the most devastating structural collapse'' in U.S. history"** | ✓ VERBATIM | JPCF @2531 |
| ID-04 | NBS's own characterisation, in its own words: ✓ **"this was the most devastating structural collapse ever to take place in the United States."** | ✓ VERBATIM | NBS @8960 |
| ID-05 | The federal investigation is **NBS Building Science Series 143**, May 1982, produced at the request of the Mayor of Kansas City: ✓ **"On July 22, Mayor Berkley formally requested that the NBS independently ascertain the most probable cause of the collapse of the Hyatt Regency walkways."** Senator Thomas F. Eagleton's office made the first contact on 20 July; Senators Eagleton and Danforth and Congressman Bolling endorsed the request on 24 July. | ✓ VERBATIM (quote) + ✓ | NBS @22496; endorsement at NBS @21900–22600 |
| ID-06 | NBS did not have free access to the evidence: ✓ **"In the early phases of the investigation, NBS involvement was limited by court order to visual and photographic observations and measurements."** Permission to weigh spans and remove specimens came later, by court order, after agreement with litigants. | ✓ VERBATIM | NBS @9748 |
| ID-07 | The disciplinary case: ✓ **"In February 1984, the Missouri Board for Architects, Professional Engineers and Land Surveyors filed its complaint seeking a determination that the engineering certificates of registration of Daniel Duncan and Jack Gillum and the engineering certificate of authority of G.C. E. International were subject to discipline"** | ✓ VERBATIM | MOCA @988 |
| ID-08 | Its outcome: ✓ **"Upon remand for assessment of appropriate disciplinary action, the Board ordered all three certificates revoked. Upon appeal the trial court affirmed. We do likewise."** | ✓ VERBATIM | MOCA @1445 |

**8 rows, 7 with a verbatim quotation.**

---

## 2. THE EVENING

| ID | Claim | Grade | Source |
|---|---|---|---|
| EV-01 | The hotel was **one year old**: ✓ **"At the time of the collapse, the hotel had been in service for approximately 1 year."** | ✓ VERBATIM | NBS @21090 |
| EV-02 | The atrium: ✓ **"The atrium is a large open area approximately 117 ft (36 m) by 145 ft (44 m) in plan and 50 ft (15 m) high."** | ✓ VERBATIM | NBS @21300 |
| EV-03 | ✓ **"Three suspended walkways spanned the atrium at the second, third, and fourth floor levels."** | ✓ VERBATIM | NBS @5959 |
| EV-04 | The event was a weekly tea dance: ✓ **"Between 1,500 and 2,000 area residents chose to escape the heat at the Hyatt Regency Hotel's tea dance, a weekly event featuring big band music and a dance contest."** | ✓ VERBATIM | JPCF @1243 |
| EV-05 | **NBS's own timeline, from the two Kansas City newspapers, in NBS's words.** ✓ **"7:00 PM - Crowd in atrium area is estimated at 1500 to 2000."** | ✓ VERBATIM | NBS @59536 |
| EV-06 | ✓ **"7:04 PM - Band returns from break and begins to play for dance contest."** | ✓ VERBATIM | NBS @59604 |
| EV-07 | ✓ **"7:05 PM - Second and fourth floor walkways collapse."** | ✓ VERBATIM | NBS @59676 |
| EV-08 | ✓ **"4:30 AM - Last survivor removed from debris."** — Saturday 18 July. Between those two lines, in NBS's own timeline: the first call for help at 7:08 PM, the call for cutting tools at 7:19, for a forklift at 7:23, more than 100 firefighters by 7:52, a heavy crane at 8:30 PM, the first walkway span lifted at 3:15 AM. | ✓ VERBATIM (quote) + ✓ (timeline) | NBS @60332; timeline NBS @59676–60400 |
| EV-09 | ✓ **"In the collapse, the second and fourth floor walkways fell to the atrium floor, with the fourth floor walkway coming to rest on top of the lower walkway."** | ✓ VERBATIM | NBS @6394 |
| EV-10 | **Where the dead and injured were.** NBS: *"Most of those killed or injured were either on the atrium first floor level or on the second floor walkway."* — i.e. the fourth-floor walkway fell **onto** the second-floor walkway and then onto the crowd beneath. | ✓ | NBS @21400–21520 (the sentence is broken across a column split in the OCR; **do not quote it verbatim** — paraphrase, or quote the identical statement in the executive summary) |
| EV-11 | **The weight that fell:** ✓ **"The walkways together weighed 142,000 pounds."** | ✓ VERBATIM | MOCA @418 (same sentence as ID-02) |
| EV-12 | **Cross-check on EV-11, ours.** NBS measured *"the dead load prior to collapse averaged 17.8 kips (79 kN) per walkway span"* (@322536) and states each walkway had four spans (@46766). Two walkways × four spans × 17.8 kips = **142.4 kips = 142,400 lb**, which independently reproduces the court's 142,000 lb. **This is our arithmetic on two verbatim figures. Say "about 71 tons" or quote the court; never say "NBS says 142,000 pounds".** | ✓ (arithmetic) | NBS @322536 + NBS @46766 + MOCA @418. See ⛔-06. |

**12 rows, 10 with a verbatim quotation.**

---

## 3. THE WALKWAYS AS THEY WERE DESIGNED

| ID | Claim | Grade | Source |
|---|---|---|---|
| DS-01 | ✓ **"The second floor walkway was suspended from the fourth floor walkway which was directly above it."** | ✓ VERBATIM | NBS @6050 |
| DS-02 | ✓ **"The third floor walkway was offset from the other two and was independently suspended from the roof framing by another set of hanger rods."** — this is why the third-floor walkway did not fall. | ✓ VERBATIM | NBS @6255 |
| DS-03 | ✓ **"Each walkway consisted of four spans made up of W16 x 26 stringers"** | ✓ VERBATIM | NBS @46766 |
| DS-04 | **The box beam — the component the whole film is about.** ✓ **"The box beams were fabricated from MC8 x 8.5 shapes joined toe to toe by continuous longitudinal welds."** Two ordinary 8-inch steel channels, welded into a hollow rectangle. | ✓ VERBATIM | NBS @48056 |
| DS-05 | **The rod.** ✓ **"The walkway hangers were 1 1/4 in (32 mm) diameter rods threaded top and bottom to receive a nut and washer."** | ✓ VERBATIM | NBS @48673 |
| DS-06 | **The original detail, in one sentence.** ✓ **"Under this arrangement each box beam would separately transfer its load directly into the hanger rods."** A single continuous rod ran from the atrium roof, through the fourth-floor box beam, and on down through the second-floor box beam; each beam sat on its own nut and washer on that one rod. | ✓ VERBATIM | NBS @12382 |
| DS-07 | The court's plain-English version: ✓ **"As originally designed the fourth and second floor walkways were to be supported by what is referred to as a 'one rod' design."** Six rods, three a side, 1¼ inch, running from roof to second floor. | ✓ VERBATIM | MOCA @6222 |
| DS-08 | **The design live load the walkways had to carry:** ✓ **"The project design criteria specify a design live load of 100 psf (4.8 kPa) for hotel corridors and lobby areas. This is interpreted by NBS to include the walkways"** | ✓ VERBATIM | NBS @41240 |
| DS-09 | **The code, and the standard underneath it:** ✓ **"The AISC Specification for the Design, Fabrication and Erection of Structural Steel for Buildings forms the basis for the steel design provisions of the Kansas City Building Code."** | ✓ VERBATIM | NBS @41547 |
| DS-10 | **The connection was non-redundant — the single most important structural idea in the episode.** ✓ **"A 'non-redundant' connection which fails will cause collapse of the structure. The box beam-hanger rod connections were 'non-redundant.'"** | ✓ VERBATIM | MOCA @8245 |
| DS-11 | And the Commission classified them accordingly: ✓ **"The Commission found the box beam-hanger rod connections to be special connections."** ✓ **"All connections are the responsibility of the structural engineer."** | ✓ VERBATIM | MOCA @8382, @7076 |
| DS-12 | **The original detail was already illegal.** ✓ **"The hanger rods and the box beam-hanger rod connections shown on the structural drawings did not meet the design specifications of the Kansas City Building Code."** The Commission's finding; **not contested on appeal.** | ✓ VERBATIM | MOCA @9971 |

**12 rows, 12 with a verbatim quotation.**

---

## 4. THE CHANGE — one rod becomes two

| ID | Claim | Grade | Source |
|---|---|---|---|
| CH-01 | ✓ **"However, during construction, shop drawings were prepared by the steel fabricator which called for the use of two sets of hanger rods rather than a single set."** | ✓ VERBATIM | NBS @12485 |
| CH-02 | ✓ **"As actually constructed, two sets of hanger rods were used, one set extending from the fourth floor box beams to the roof framing and another set from the second floor box beams to the fourth floor box beams."** | ✓ VERBATIM | NBS @7487 |
| CH-03 | **What that did to the path the load takes — the mechanism, in NBS's own sentence.** ✓ **"Under this arrangement all of the second floor walkway load was first transferred to the fourth floor box beams, where both that load and the fourth floor walkway load were transmitted through the box beam-hanger rod connections to the ceiling hanger rods."** | ✓ VERBATIM | NBS @12817 |
| CH-04 | The second rod was offset **4 inches** along the axis of the box beam from the upper rod, so that the two rods did not pass through the same hole. | ✓ | NBS @311300–311600 (§10.5) and NBS §3.3 |
| CH-05 | **Who asked for it, and why.** ✓ **"Because of certain fabricating problems Havens proposed to Duncan the use of a 'double rod' system to suspend the second and fourth floor walkways."** | ✓ VERBATIM | MOCA @10195 |
| CH-06 | The fabricator was named and was itself capable of doing the engineering: ✓ **"The steel fabricator on the Hyatt project, Havens Steel Company, had engineers capable of designing simple, complex, or special connections."** | ✓ VERBATIM | MOCA @8466 |
| CH-07 | **Nobody has ever established who first drew the second rod.** ✓ **"The chain of events has never been exactly determined, but two possible scenarios have been proposed in studies of the Hyatt."** — a fabricator unable to obtain rods long enough, or a construction team judging that threading a 30-ft rod along its whole length was impractical. **Both are proposals, neither is a finding.** | ✓ VERBATIM | JPCF @14917. See ⛔-05. |
| CH-08 | **The change was approved by the project engineer.** ✓ **"There was evidence that one of the architects contacted Duncan to verify that the double rod arrangement was structurally sound and was advised by Duncan that it was."** The appellants disputed this on appeal; the court reviewed the record and rejected the dispute. | ✓ VERBATIM | MOCA @10664 |
| CH-09 | ✓ **"It is a reasonable inference from the evidence that Duncan did not make the engineering calculations and tests necessary to determine the structural soundness of the double rod design."** | ✓ VERBATIM | MOCA @11736 |
| CH-10 | **The sentence the film is built to arrive at.** A technician checking the shop drawings raised it: ✓ **"He called to Duncan's attention questions concerning the strength of the rods and the change from one rod to two. Duncan stated to the technician that the change to two rods was 'basically the same as the one rod concept.'"** | ✓ VERBATIM | MOCA @12685 |
| CH-11 | **How many times he was asked.** ✓ **"The board's investigation revealed that project engineer Duncan had been asked about the implications of the design change on at least six separate occasions during construction. Duncan assured each inquirer that replacing the single, long hanger rods with double, offset rods would not compromise the safety of the walkways."** | ✓ VERBATIM | JPCF @15941 — attribute to *the licensing board's investigation as reported in ASCE's journal*, not to NBS. |
| CH-12 | **Information that existed and did not travel.** ✓ **"Certain information concerning loads and other aspects of the box beam-hanger rod connections which appeared on Duncan's preliminary sketches was not included on the final structural drawings sent to the fabricator."** | ✓ VERBATIM | MOCA @9450 |

**12 rows, 11 with a verbatim quotation.**

---

## 5. ⭐ THE LOAD ARITHMETIC — the spine of the episode

**This is the section a wrong number destroys. Every figure below is a verbatim NBS figure or is labelled as
our arithmetic on verbatim NBS figures. A "kip" is 1,000 pounds-force.**

| ID | Claim | Grade | Source |
|---|---|---|---|
| LD-01 | **ORIGINAL DETAIL — the design load at each connection.** ✓ **"For the continuous hanger rod arrangement, the design load to be transferred to each hanger rod at the second and fourth floor levels would have been approximately 20.3 kips (90 kN)"** — the same load at both levels, because each beam sat on its own nut and delivered only its own share into the rod. | ✓ VERBATIM | NBS @319196 (Conclusion 6(a)) |
| LD-02 | Longer form of the same, from §10.5: ✓ **"The design load to be transferred to each hanger rod at the second floor walkway would have been one-half the sum of the dead load and the resultant live load for a single span, or approximately 20.3 kips (90 kN)"** | ✓ VERBATIM | NBS @310719 |
| LD-03 | **AS BUILT — the design load at the fourth-floor connection.** ✓ **"For the interrupted hanger rod arrangement, the design load to be transferred by a fourth floor box beam-hanger rod connection would have been 40.7 kips (181 kN)"** | ✓ VERBATIM | NBS @326658 (Conclusion 6(b)) |
| LD-04 | **The word NBS uses is "doubled", and it uses it as a conclusion, twice.** ✓ **"The change in hanger rod arrangement from a continuous rod to interrupted rods essentially doubled the load to be transferred by the fourth floor box beam-hanger rod connections"** | ✓ VERBATIM | NBS @319014 (Conclusion 6) |
| LD-05 | And in §10.5: ✓ **"However, the load to be transferred from the fourth floor box beam to the upper hanger rod under this arrangement was essentially doubled, thus compounding an already critical condition."** | ✓ VERBATIM | NBS @311940 |
| LD-06 | And the court states the same effect independently: ✓ **"The effect of this change was to double the load on the fourth floor walkway and the box beam-hanger rod connections on that walkway."** | ✓ VERBATIM | MOCA @10530 |
| LD-07 | **20.3 × 2 = 40.6, and NBS states 40.7.** The difference is rounding in NBS's own dead/live load table; **do not present 40.7 as exactly twice 20.3 to the decimal, and do not "correct" NBS to 40.6.** Say: the design load went from about 20 kips to about 41 kips. | ✓ (arithmetic, labelled) | LD-01 + LD-03 |
| LD-08 | **WHAT THE CODE REQUIRED OF THE CONNECTION.** Working-stress design under the AISC Specification carries a factor of safety; the lowest that would govern any part of this connection is **1.67**. ✓ **"It would be expected that the ultimate load capacity of the resulting connection would be at least 1.67 times 40.7, or 68 kips (302 kN)"** | ✓ VERBATIM | NBS @307307 |
| LD-09 | ✓ **"should have been able to support an ultimate load of at least 68 kips (302 kN)"** | ✓ VERBATIM | NBS @307519 |
| LD-10 | **WHAT THE CONNECTIONS ACTUALLY HAD.** ✓ **"Mean ultimate capacities of the fourth floor box beam-hanger rod connections were estimated on the basis of the NBS test series and these capacities ranged from 18.2 kips (81 kN) to 19.3 kips (86 kN) with an average value of 18.6 kips (83 kN)"** | ✓ VERBATIM | NBS @323630 (Conclusion 2(c)) |
| LD-11 | **68 required. 18.6 available.** 18.6 ÷ 68 = **27 percent**. **This percentage is OURS.** NBS states both numbers and does not state this ratio. Say "eighteen and a half kips where the code wanted sixty-eight", or say "about twenty-seven percent — our arithmetic on the NBS figures". **See ⛔-01: this is not the 31 percent figure, and the two must never be swapped.** | ✓ (arithmetic, labelled) | LD-09 + LD-10 |
| LD-12 | **WHAT WAS ACTUALLY ON THE CONNECTION THAT NIGHT.** The maximum estimated dead-plus-live load at a fourth-floor connection was **21.4 kips**. ✓ **"the maximum load on a fourth floor box beam-hanger rod connection at the time of collapse was only 31 percent of the ultimate capacity expected of a connection designed under the Kansas City Building Code."** 21.4 ÷ 68 = 31.5 %. | ✓ VERBATIM | NBS @7860 (abstract) |
| LD-13 | Stated the other way, against the design load rather than the ultimate capacity: ✓ **"Thus the maximum load acting on a fourth floor box beam-hanger rod connection at the time of collapse was 53 percent of what was required for design under the Kansas City Building Code."** 21.4 ÷ 40.7 = 52.6 %. | ✓ VERBATIM | NBS @304076 |
| LD-14 | **HAD THE CHANGE NEVER BEEN MADE, IT STILL WOULD NOT HAVE BEEN LEGAL.** ✓ **"Had this change in hanger rod detail not been made, the ultimate capacity of the box beam-hanger rod connection would still have been far short of that expected of a connection designed in accordance with the AISC Specification."** Required: 1.67 × 20.3 = **33.9 kips**. Available: ✓ **"the mean ultimate capacity of a single-rod connection as detailed on the contract drawings is estimated to be 20.5 kips (91 kN)"**. | ✓ VERBATIM (both) | NBS @312246; NBS @327247 |
| LD-15 | ✓ **"Thus the ultimate capacity actually available using the original connection detail would have been approximately 60 percent of that expected of a connection designed in accordance with the AISC Specification."** 20.5 ÷ 33.9 = 60.5 %. | ✓ VERBATIM | NBS @312767 |
| LD-16 | ✓ **"The box beam-hanger rod connection would not have satisfied the Kansas City Building Code under the original hanger rod detail (continuous rod)."** | ✓ VERBATIM | NBS @326840 (Conclusion 7) |
| LD-17 | **AND YET, WITHOUT THE CHANGE, IT WOULD HAVE HELD THAT NIGHT.** NBS Conclusion 8: under the original arrangement the connections *"would have had the capacity to resist the loads estimated to have been acting at the time of collapse"* — ✓ **"The maximum load (estimated dead load plus upper-bound live load) believed to have been acting on a second floor box beam-hanger rod connection at the time of collapse is 11.5 kips (51 kN)"**, against a single-rod capacity of 20.5 kips. **This is the film's hinge: the original design was illegal but survivable; the change made it lethal.** | ✓ VERBATIM (both) | NBS @15642; NBS @327960 |
| LD-18 | **THE ODDEST FACT IN THE FILE.** ✓ **"Note that, because of the greater dead load and design live load, the third floor walkway connection would have had approximately 53 percent of the expected ultimate capacity. Had the change in hanger rod arrangement not been made, the third floor walkway would have been the most critical of the three."** The walkway that survived was the weakest one — the change is what moved the failure to the fourth floor. | ✓ VERBATIM | NBS @312976 |
| LD-19 | **AND THE THIRD WALKWAY WAS NEVER SAFE EITHER.** ✓ **"The third floor walkway, which did not collapse, had a 'high probability' of failure during the life of the building."** | ✓ VERBATIM | MOCA @56171 |
| LD-20 | **The margin was gone from the first day.** ✓ **"With this change in hanger rod arrangement, the ultimate capacity of the walkways was so significantly reduced that, from the day of construction, they had only minimal capacity to resist their own weight and had virtually no capacity to resist additional loads imposed by people."** | ✓ VERBATIM | NBS @8267 |

**20 rows, 17 with a verbatim quotation, 3 labelled arithmetic.**

### The arithmetic on one line, for the writer

```
                        DESIGN LOAD      CODE-REQUIRED         ACTUAL
                        AT CONNECTION    ULTIMATE CAPACITY     CAPACITY

as drawn (one rod)      20.3 kips        33.9 kips             20.5 kips     -> 60%   (LD-15)
as built  (two rods)    40.7 kips        68   kips             18.6 kips     -> 27%   (ours, LD-11)

                        LOAD ON IT ON THE NIGHT OF 17 JULY 1981:  21.4 kips
                        = 31% of the 68 kips the code expected     (LD-12, NBS's own figure)
                        = 53% of the 40.7 kips design load         (LD-13)

The change did not weaken the steel. It doubled what the same steel was asked to carry.
```

---

## 6. WHAT THE FEDERAL INVESTIGATION CONCLUDED

| ID | Claim | Grade | Source |
|---|---|---|---|
| FN-01 | **The cause.** ✓ **"it is concluded that the most probable cause of failure was insufficient load capacity of the box beam-hanger rod connections."** | ✓ VERBATIM | NBS @6593 |
| FN-02 | **The two contributing factors, in NBS's own words.** ✓ **"Two factors contributed to the collapse: inadequacy of the original design for the box beam-hanger rod connection, which was identical for all three walkways, and a change in hanger rod arrangement during construction that essentially doubled the load on the box beam-hanger rod connections at the fourth floor walkway."** | ✓ VERBATIM | NBS @6934 |
| FN-03 | **Where it started.** ✓ **"Observed distortions of structural components strongly suggest that failure of the walkway system initiated in the box beam-hanger rod connection at location 9UE (east end of middle box beam in fourth floor walkway)"** | ✓ VERBATIM | NBS @14743 |
| FN-04 | **All six were candidates.** ✓ **"it is clear that each of the 6 fourth floor box beam-hanger rod connections had a high probability of failure; each connection was a candidate for initiation of walkway collapse."** | ✓ VERBATIM | NBS @305882 |
| FN-05 | **Why one failure meant total collapse.** ✓ **"Thus, failure of any one connection would have led to complete collapse of the walkway system."** | ✓ VERBATIM | NBS @306333 |
| FN-06 | **As constructed, three separate things violated the code.** ✓ **"the fourth floor to ceiling hanger rods, and the third floor walkway hanger rods did not satisfy the design provisions of the Kansas City Building Code."** (Conclusion 5, whose subject is the box beam-hanger rod connections as well.) | ✓ VERBATIM | NBS @15027 |
| FN-07 | **It was not bad workmanship and it was not bad steel.** ✓ **"Neither the quality of workmanship nor the materials used in the walkway system played a significant role in initiating the collapse"** | ✓ VERBATIM | NBS @15747 (Conclusion 9) |
| FN-08 | **The load that night was far below the legal design load.** NBS Conclusion 1: collapse occurred *"under the action of loads that were substantially less than the design loads specified by the Kansas City Building Code."* (The cached span contains the OCR fault `specif ied` — **paraphrase, or use LD-13, which says the same thing in a clean span.**) | ✓ | NBS @321100–321400. ⚠ not quotable verbatim. |
| FN-09 | **How NBS counted the people.** ✓ **"It is concluded that a total of 63 people represents a credible upper-bound combined occupancy of the second and fourth floor walkways at the time of collapse."** | ✓ VERBATIM | NBS @322318 |
| FN-10 | ✓ **"Based on information obtained from the KMBC TV videotape, it is likely that the second floor walkway was occupied by approximately 40 people shortly before the collapse."** A television crew was filming the dance and was changing batteries when the collapse happened. | ✓ VERBATIM | NBS @66846 |
| FN-11 | **NBS refused to build the story out of witnesses.** ✓ **"In view of the conflicting nature of eyewitness accounts and the availability of videotape showing parts of the walkways a few minutes before the collapse, this investigation did not include any organized effort to interview the injured or to solicit eyewitness accounts of the collapse."** ✓ **"the number of people and their location on the walkways at the time of collapse can only be estimated and will never be"** known with certainty. | ✓ VERBATIM (both) | NBS @63561, @64317 |
| FN-12 | **Dancing did not do it.** ✓ **"Dynamic loads induced by walking or dancing on the walkways would not have been significant in comparison to the static loads."** — the single most persistent myth about this collapse, killed by the federal report's own conclusion 1(c). | ✓ VERBATIM | NBS @296330 |
| FN-13 | The walkways were slightly heavier than drawn: ✓ **"the dead load prior to collapse averaged 17.8 kips (79 kN) per walkway span. This is approximately 8 percent higher than the nominal dead load that would be estimated on the basis of the contract drawings."** | ✓ VERBATIM | NBS @322536 |
| FN-14 | A weld-symbol question exists but is not the cause: ✓ **"the welding symbol used on the shop drawings is interpreted to require a prequalified partial joint penetration groove weld"**, and NBS found the as-built joint geometry did not meet the tolerance for one. **NBS still concluded workmanship did not play a significant role (FN-07).** Do not turn this into "the welds were bad". | ✓ VERBATIM (quote) + ✓ | NBS @315085; §10.6 |

**14 rows, 12 with a verbatim quotation.**

---

## 7. THE REVIEW CHAIN — who checked what, and what each said they believed

**This section is the reason the episode is worth 30 minutes. Every row is from the record.**

| ID | Claim | Grade | Source |
|---|---|---|---|
| RV-01 | **The drawings were stamped by three parties.** ✓ **"As indicated by their stamps, these shop drawings were reviewed by the contractor, structural engineer"** and architect. Havens Steel Company's shop drawings were dated between 7 January and 9 February 1979. | ✓ VERBATIM | NBS @13074 |
| RV-02 | **Who was who.** ✓ **"Gillum-Colaco, Inc., a Texas corporation, contracted with the architects of the Hyatt construction to perform structural engineering services in connection with the erection of that building."** By subcontract G.C.E. International, Inc. assumed all of that work. | ✓ VERBATIM | MOCA @2014 |
| RV-03 | ✓ **"Duncan was the project engineer for the Hyatt construction in direct charge of the actual structural engineering work on the project. He was under the direct supervision of Gillum."** | ✓ VERBATIM | MOCA @2714 |
| RV-04 | ✓ **"His professional seal was utilized on structural engineering plans for the Hyatt."** — Gillum's. | ✓ VERBATIM | MOCA @2632 |
| RV-05 | **The fee for all of it:** ✓ **"G.C.E.'s total fee for the Hyatt was $247,500."** | ✓ VERBATIM | MOCA @61571 (footnote 2) |
| RV-06 | **THE MISUNDERSTANDING, STATED BY THE TRIBUNAL.** ✓ **"The Commission found that the structural drawings (S405.1 Secs. 10 and 11) did not communicate to the fabricator that it was to design the box beam-hanger rod connection, and did communicate to the fabricator that those connections had been designed by the engineer."** | ✓ VERBATIM | MOCA @8960 |
| RV-07 | **AND WHAT EACH SIDE BELIEVED.** ✓ **"Duncan testified that he intended for the fabricator to design the connections. Havens prepared its shop drawings on the basis that the connections shown on the design drawings had been designed by the structural engineer."** **Each believed the other had done it. That sentence is the episode.** | ✓ VERBATIM | MOCA @9227 |
| RV-08 | The same collision, in ASCE's journal: ✓ **"The engineers left the detail unspecified, indicating that the fabricators were to complete the calculations for the design. The fabricators later argued that the connection was not their responsibility."** | ✓ VERBATIM | JPCF @14439 |
| RV-09 | **The firm's own procedure required the check that was not done.** ✓ **"The Commission found, and appellants do not dispute, that its own internal procedures called for a detailed check of all special connections."** | ✓ VERBATIM | MOCA @12224 |
| RV-10 | ✓ **"Duncan did not 'review' the fourth floor box beam connection shown on the Havens shop drawings nor did he, in accord with usual engineering practice, assemble its components to determine what the connection looked like in detail."** | ✓ VERBATIM | MOCA @12908 |
| RV-11 | ✓ **"No review was made nor calculations performed to determine whether the box beam-hanger rod connection shown on the shop drawings met Code requirements."** | ✓ VERBATIM | MOCA @55084 |
| RV-12 | ✓ **"Duncan and Gillum approved the shop drawings."** | ✓ VERBATIM | MOCA @13571 |
| RV-13 | **What the law said the review was.** ✓ **"Under the contract, and under the statute, review and approval of the shop drawings is an engineering function."** ✓ **"Shop drawing review by the engineer is contractually required, universally accepted and always done as part of the design engineer's responsibility."** | ✓ VERBATIM | MOCA @54366, @55236 |
| RV-14 | **The project's shape.** ✓ **"The Hyatt Regency Hotel, to which Gillum assigned Duncan, was a fast-track construction project, meaning that the construction team had begun to build the hotel while the design team was still finalizing the plans."** | ✓ VERBATIM | JPCF @14100 |
| RV-15 | **THE SECOND CHANCE, AND WHAT WAS DONE WITH IT.** ✓ **"While construction of the Hyatt was in progress the atrium roof collapsed. Investigation into that collapse established that the cause was poor construction workmanship."** (October 1979. NBS separately records ✓ **"an investigation conducted by the U.S. Occupational Safety and Health Administration (OSHA) following a fatal construction accident at the Hyatt Regency Hotel in October 1979"**; JPCF records ✓ **"In October 1979, two accidents at the Kansas City Hyatt (one resulting in a death) had brought attention to the hotel's design"**.) | ✓ VERBATIM (all three) | MOCA @13617; NBS @38545; JPCF @16756 |
| RV-16 | After that collapse the owner and architect paid G.C.E. an additional fee to check the whole atrium. ✓ **"Gillum assured the owner's representative that 'he would personally look at every connection in the hotel.'"** | ✓ VERBATIM | MOCA @14252 |
| RV-17 | ✓ **"In their report to the architects, appellants advised 'we then checked the suspended bridges and found them to be satisfactory.'"** | ✓ VERBATIM | MOCA @14547 |
| RV-18 | ✓ **"Appellants did not do a complete check of the design of all steel in the atrium nor a complete check of the suspended bridges."** They checked only the atrium roof steel. | ✓ VERBATIM | MOCA @14820 |
| RV-19 | **And the collapse came about a year later.** ✓ **"The cause of the walkway collapse was the failure of the fourth floor box beam-hanger rod connections."** | ✓ VERBATIM | MOCA @15635 |

**19 rows, 19 with a verbatim quotation.**

---

## 8. THE DISCIPLINE

| ID | Claim | Grade | Source |
|---|---|---|---|
| DC-01 | The complaint was filed in **February 1984** (ID-07), and the hearing went to the Missouri Administrative Hearing Commission. ✓ **"The Commission conducted twenty-seven days of hearing."** | ✓ VERBATIM | MOCA @2895 |
| DC-02 | ✓ **"Its 'Statement of the case, Findings of Fact, Conclusions of Law and Decision' are 442 pages in length."** Ninety-eight pages of findings of fact; 322 pages of conclusions of law; **180 numbered findings**, of which the appellants challenged **five**. | ✓ VERBATIM (quote) + ✓ | MOCA @2950; MOCA @3050–3600 |
| DC-03 | The decision was filed by the administrative law judge on **15 November 1985**: ✓ **"On November 15, 1985, Judge Deutsch filed his decision."** | ✓ VERBATIM | JPCF @23248 |
| DC-04 | **DUNCAN — the findings.** ✓ **"Duncan was found to have been guilty of gross negligence in the preparation and completion of a structural drawing (S405.1, Sections 10 and 11); and in failing to review shop drawings of the Hyatt project"** (in particular Shop Drawing 30 and Erection Drawing E3). | ✓ VERBATIM | MOCA @4189 |
| DC-05 | ✓ **"He was further found guilty of misconduct in misrepresenting to the architects the safety of a connection (the double hanger rod-box beam connection) when he was ignorant of the safety due to a failure to perform engineering tests and calculations to determine such safety."** | ✓ VERBATIM | MOCA @4451 |
| DC-06 | **GILLUM — the findings.** ✓ **"Gil-lum was found vicariously liable and responsible for the acts and omissions of Duncan which liability and responsibility he assumed by affixing his professional engineering seal on the structural drawings."** *(the reporter breaks the name across a line; quoted exactly)* | ✓ VERBATIM | MOCA @4725 |
| DC-07 | ✓ **"He was further found grossly negligent in failing to himself review or assure that someone had reviewed drawing S405.1 before affixing his seal thereto."** | ✓ VERBATIM | MOCA @4960 |
| DC-08 | ✓ **"Gillum was also found to have engaged in unprofessional conduct in failing and refusing to take responsibility for the entire engineering project"** as required by § 327.411.2, RSMo 1978. | ✓ VERBATIM | MOCA @5113 |
| DC-09 | **THE DEFENCE, IN GILLUM'S OWN TESTIMONY, quoted in the opinion's footnote 9.** ✓ **"Because the shop drawings that were prepared under the direction of another engineer have to be the responsibility of the other engineer. They were not prepared under my direction and therefore I cannot accept that responsibility"** | ✓ VERBATIM | MOCA @64621 |
| DC-10 | ✓ **"In essence he placed the responsibility for the improper design of the connections on Havens and took the position that the structural engineer was entitled to rely on Havens' expertise."** | ✓ VERBATIM | MOCA @58914 |
| DC-11 | **THE ANSWER — the seal statute.** ✓ **"By section 327.411.2 the owner of the seal is responsible for the 'whole ... engineering project' when he places his seal on 'any plans' unless he expressly disclaims responsibility and specifies the documents which he disclaims."** | ✓ VERBATIM | MOCA @59515 |
| DC-12 | ✓ **"The responsibility for the structural integrity and safety of the walkway connections was Duncan's and that responsibility was non-delegable."** ✓ **"His reliance upon others to perform that duty serves as no justification for his indifference to his obligations and responsibility."** | ✓ VERBATIM | MOCA @56657, @56917 |
| DC-13 | The administrative law judge's formulation, as quoted in ASCE's journal: ✓ **"while the engineer may properly delegate the work of performing engineering design functions, he cannot delegate the responsibility"** | ✓ VERBATIM | JPCF @21823 |
| DC-14 | **WHAT "GROSS NEGLIGENCE" WAS HELD TO MEAN — the legal heart of the episode.** ✓ **"The Commission defined the phrase in the licensing context as 'an act or course of conduct which demonstrates a conscious indifference to a professional duty.'"** Missouri courts do not otherwise recognise degrees of negligence; no Missouri court had defined the term in a licensing context before this case. | ✓ VERBATIM | MOCA @25081 |
| DC-15 | ✓ **"The structural engineer's duty is to determine that the structural plans which he designs or approves will provide structural safety because if they do not a strong probability of harm exists. Indifference to the duty is indifference to the harm."** | ✓ VERBATIM | MOCA @26181 |
| DC-16 | **The discipline was not for the deaths.** ✓ **"That breach occurred at the latest when their design was incorporated into the building with their approval and they were subject to discipline whether or not any collapse subsequently occurred."** | ✓ VERBATIM | MOCA @28733 |
| DC-17 | **It was the pattern, not any single act.** The Commission's own footnote: ✓ **"it is only after a complete analysis of their overall performance within the system that any judgment of their conduct can be made under the terms of the licensing statute."** The court agrees: ✓ **"It is the combination of a series of acts and omissions which created the structurally unsound walkways."** | ✓ VERBATIM (both) | MOCA @26963, @27159 |
| DC-18 | And the court's footnote 7, which is the sentence to end an act on: ✓ **"the original inadequacies of the structural drawings might not have been critical if a meaningful review of the shop drawings had occurred."** | ✓ VERBATIM | MOCA @63712 |
| DC-19 | **THE OUTCOME.** The Board revoked all three certificates (ID-08). The date: ✓ **"the board carried out the punishment on January 22, 1986, 4 1/2 years after the walkway collapse, and the two Hyatt engineers became the first to lose their licenses for gross negligence"** | ✓ VERBATIM | JPCF @23849 |
| DC-20 | **THE APPEAL.** ✓ **"The finding of misconduct against Gillum arising from the 'atrium design review' is reversed. In all other respects the order of the Commission and the discipline imposed by the Board is affirmed."** — 26 January 1988, Smith, J.; Karohl, P.J., and Kelly, J., concurring. **The reversal is one charge that had not been pleaded in the complaint; the revocations stood.** | ✓ VERBATIM | MOCA @61059 |
| DC-21 | **NO CRIMINAL CASE.** ✓ **"In December 1983, the county prosecutor and the U.S. Attorney announced that they had found insufficient evidence to convict anyone involved in the Hyatt construction with criminal negligence and that no criminal charges would be filed."** | ✓ VERBATIM | JPCF @18162 |
| DC-22 | **THE CIVIL MONEY, BEFORE ANY OF THIS.** ✓ **"By this time, insurance companies had paid out over $78,000,000 to settle civil lawsuits filed by many of the victims and their families, but no one had yet taken responsibility for the collapse"** — as at December 1983. **This is a figure as at a date, not a final total.** ⛔-07. | ✓ VERBATIM | JPCF @18399 |
| DC-23 | **Afterwards.** ✓ **"Although Gillum lost 24 of his 28 state licenses, Ohio never saw fit to revoke his certificate, 3 other states simply never renewed his license, and California granted him reinstatement in July 1994"**; ✓ **"Actually, Duncan has not practiced engineering since his Missouri license was revoked"** (as at January 1995, when the author interviewed him). | ✓ VERBATIM (both) | JPCF @28627, @28490. **Time-sensitive — see ○-06.** |

**23 rows, 23 with a verbatim quotation.**

---

## 9. WHAT THE PROFESSION DID WITH IT

| ID | Claim | Grade | Source |
|---|---|---|---|
| PR-01 | ASCE had rewritten its code of ethics in 1976, and the new Fundamental Canon 1 read: ✓ **"Engineers shall hold paramount the safety, health and welfare of the public in the performance of their professional duties"** | ✓ VERBATIM | JPCF @7430 |
| PR-02 | The Hyatt was the first real test of it. ASCE's Committee on Professional Conduct heard the matter in confidence in the summer of 1986; two members recused themselves — the chair of the Missouri licensing board, and the man who had headed the NBS investigation. | ✓ | JPCF @25400–25800 |
| PR-03 | ✓ **"the committee members concluded unanimously that Gillum should be ''expelled with no privilege ever to rejoin''"** | ✓ VERBATIM | JPCF @25796 |
| PR-04 | The ASCE board of direction did not follow it. ✓ **"They voted to suspend him for just 3 years. Gillum voluntarily relinquished his membership altogether."** | ✓ VERBATIM | JPCF @26225 |
| PR-05 | ✓ **"Duncan was free from any discipline by an ethics committee because he had never been a member of any national society."** | ✓ VERBATIM | JPCF @24905 |
| PR-06 | **The defence that was offered to the profession.** The engineers ✓ **"had told the board the accident was the result of poor communication"**; ✓ **"Duncan and Gillum refused to concede that this made them responsible, particularly as there was no proof as to who had altered the plans."** ✓ **"Duncan later testified that the connection and any changes to it were not his responsibility because the engineers had not designed it in the first place"** | ✓ VERBATIM (all three) | JPCF @20878, @20672, @16267 |
| PR-07 | Context for it: ✓ **"In the 1980s, he held licenses in 28 states, including Missouri."** Gillum was by then engineer of record over 50–100 engineers and specialists. | ✓ VERBATIM (quote) + ✓ | JPCF @13095; @13100–13600 |
| PR-08 | **The building today.** ✓ **"The three walkways were removed"** shortly after the collapse; ✓ **"In their place stands a single span, supported not by delicate, graceful rods, but standing on stout, sturdy columns"** *(as at 2000 — see ○-07)*. | ✓ VERBATIM (both) | JPCF @30399, @30527 |

**8 rows, 7 with a verbatim quotation.**

---

## 10. WHAT THE RECORD DOES **NOT** ESTABLISH

| ID | Not established | Grade | Source |
|---|---|---|---|
| ND-01 | **Who first drew the second rod.** Never determined. CH-07. Two scenarios have been *proposed*; neither is a finding of any tribunal. | ✓ | JPCF @14917 |
| ND-02 | **Whether a telephone call approving the change was made, and by whom.** The record retrieved this pass establishes that the change *"was transmitted to Duncan who approved it"* and that he assured an architect it was sound (CH-08). It does **not** establish the famous disputed phone call between Havens and G.C.E. ⛔-05. | ✓ | MOCA §review; absent from NBS |
| ND-03 | **What the original structural design calculations for the connection said** — because they were never produced. ✓ **"Efforts to obtain copies of the structural design calculations were unsuccessful"**. | ✓ VERBATIM | NBS @41711 |
| ND-04 | **That dancing caused it.** Positively excluded. FN-12. | ✓ | NBS @296330 |
| ND-05 | **That bad welding or bad steel caused it.** Positively excluded. FN-07. | ✓ | NBS @15747 |
| ND-06 | **That the walkways were overloaded.** The opposite: the load that night was about half the legal design load (LD-13). | ✓ | NBS @304076 |
| ND-07 | **Anything about the architect's or the contractor's culpability.** They stamped the shop drawings (RV-01), and they were never charged before the Board: ✓ **"The board had also chosen, for reasons that remain unclear, not to investigate the architects, over whom they also had licensing authority"**. No tribunal retrieved this pass made any finding against the architect, the contractor or the fabricator. ⛔-16. | ✓ VERBATIM | JPCF @19987; absent from MOCA and NBS |
| ND-08 | **Any criminal finding against anyone.** DC-21. | ✓ | JPCF @18162 |
| ND-09 | **Any individual victim's name, story, injury or death.** Neither NBS nor MOCA names a single victim. There is nothing to redact because there is nothing there. | ✓ | NBS, MOCA — absence verified by search |
| ND-10 | **The exact number of injured.** NBS says 188 (of whom two died); the Court of Appeals says "at least 186"; ASCE's journal says "nearly 200". ⛔-04. | ✓ | NBS @20732; MOCA @418; JPCF @2531 |

**10 rows.**

---

## 11. ⛔ FORBIDDEN CLAIMS — a script must never say or show these

### 11a. The engineering

| ID | Forbidden | Why |
|---|---|---|
| ⛔-01 | **"As built, the connection had only 31 percent of the strength the code required."** | **The 31 percent is a LOAD ratio, not a CAPACITY ratio.** NBS's 31 percent is *the load actually on the connection that night* (21.4 kips) as a fraction of *the ultimate capacity the code expected* (68 kips) — LD-12. The as-built **capacity** ratio is 18.6 ÷ 68 = **27 percent**, and **NBS never states that percentage**; it is ours (LD-11). **The Missouri Court of Appeals itself makes exactly this slip**, in footnote 12: ✓ *"The National Bureau of Standards found as originally designed the connection capacity was 60 percent of that required by the Building Code; as ultimately constructed the capacity was 31 percent of Code requirements."* (MOCA @66036). The 60 percent half of that sentence is right (LD-15); the 31 percent half describes a load, not a capacity. **Do not quote MOCA footnote 12 for the engineering.** Use NBS's own sentences. This is the single easiest error to make in this episode and the one the target audience is most likely to catch. |
| ⛔-02 | **"The two-rod change was the cause of the collapse."** stated flatly and alone. | NBS names **two** contributing factors and puts the *inadequacy of the original design* first (FN-02). The original single-rod detail also failed the code (LD-16) and would have given only ~60 percent of the required capacity (LD-15). The honest sentence is NBS's: an already-inadequate connection, and then a change that doubled what it had to carry. **The change is what turned an illegal building into a lethal one (LD-17) — that is a stronger sentence than the false one.** |
| ⛔-03 | **Any explanation of why NBS says 113 dead and the courts say 114** — e.g. "one more victim died later, in 1983", "a survivor died of her injuries years afterwards". | **No document retrieved says.** NBS (May 1982) counts 111 + 2 = 113. The Missouri Court of Appeals (1988) and ASCE (2000) say 114. **Use 114, cite the court, and do not narrate the gap.** ○-04. |
| ⛔-04 | **"216 injured"**, or any injury figure other than the three that are sourced. | The only figures in the retrieved record are **188** (NBS, of whom two died), **"at least 186"** (MOCA), and **"nearly 200"** (JPCF). 216 is a widely repeated number that appears in **none** of them. ND-10. |
| ⛔-05 | **Dramatising "the phone call" — Havens rings G.C.E., someone says yes, and G.C.E. later denies the call happened.** | This is the version taught in engineering-ethics courses. **It is not in the federal report and it is not in the appellate opinion.** What the official record says is RV-06, RV-07, CH-08 and CH-10 — which are better, because they are findings. ND-02. Do not stage a phone call, do not write dialogue for one, do not put a ringing telephone on screen as if it were the moment. |
| ⛔-06 | **Attributing "142,000 pounds" or "71 tons" to NBS.** | 142,000 lb is the **Missouri Court of Appeals'** figure (MOCA @418). Our reconstruction from NBS's measured 17.8 kips/span gives 142,400 lb (EV-12) — **that number is ours.** Cite the court, or say "about seventy-one tons" without a source name. |
| ⛔-07 | **"The victims received $78 million"**, or any figure presented as the final civil recovery. | ✓ *"over $78,000,000"* is what insurers had **paid out as at December 1983** (DC-22). Litigation continued for years afterwards. No retrieved document states a final total. ○-05. |
| ⛔-08 | **"The walkways were crowded with dancers and the dancing shook them down."** | FN-12 kills it with the federal report's own conclusion. NBS's credible upper bound for **both** collapsed walkways combined is **63 people** (FN-09), against a code design live load of 100 psf. |
| ⛔-09 | **Calling the box beam-hanger rod connection "a bolt", "a weld", or "a bracket".** | It is a **1¼-inch threaded rod passing through a hole in a welded box beam made of two 8-inch channels, bearing on a nut and a washer** (DS-04, DS-05, DS-06). The failure mode NBS describes is the rod and its washer **pulling through the box beam**. If the film cannot say that correctly, it cannot show the animation, and the animation is the film. |

### 11b. Rights, footage and depiction

| ID | Forbidden | Why |
|---|---|---|
| ⛔-10 | **ANY third-party broadcast, news, or press footage or photograph. None. Not the KMBC TV videotape, not the Kansas City Star or Kansas City Times photographs, not rescue footage, not a documentary clip, not a frame of it, not "fair use", not blurred, not behind a graphic.** | Standing project prohibition — no unlicensed news footage in any package (`docs/OPERATING_PLAYBOOK.md`; per-asset rights manifest required). **This event is the single most tempting case on the whole slate for a violation**, because the collapse was filmed by a television crew who were in the room, and the footage is everywhere. It is also third-party copyright in a mass-casualty event with living survivors. **The answer is no, and §12 is the plan that makes the answer cost nothing.** |
| ⛔-11 | **Any generated or recreated image depicting a body, a dead person, an injured person, blood, a covered casualty, a rescue in progress, or debris with a person under it.** | Mass-casualty dignity, ad safety, and PD's own EP60 precedent (*"no recovery or rescue footage of bodies; no recreation of any identified person's final moments"*). There is no editorial gain: **the numbers and the empty room do the work.** |
| ⛔-12 | **Any depiction of the crowded lobby at, or in the seconds before, the moment of collapse — from any angle, including from above, including in silhouette, including "abstracted".** | The film may show the room **filling at 3 p.m.** and the room **empty**. It may not show the room **full** and then cut to the fall. That composition is a reconstruction of 114 deaths. §12 gives the substitute shot for every one of these beats. |
| ⛔-13 | **Naming any victim or survivor, or depicting any real person's likeness — victim, survivor, rescuer, witness, juror, judge, board member, or engineer.** | Neither NBS nor MOCA names a victim (ND-09), so no selection problem even arises — **the film names no victim, and that is a decision, not an omission.** For the living or possibly-living: PD invariant 11 and the standing no-real-likeness rule. **People appear as hands, backs, silhouettes, or not at all.** |
| ⛔-14 | **Making any generated image look like an authentic record** — a photograph of drawing S405.1 or Shop Drawing 30, a page of the 442-page Commission decision, a Missouri professional engineer's seal with a real name or the real State of Missouri seal artwork, an NBS test photograph, a newspaper front page, a court exhibit, a hotel document, or a KMBC videotape frame with a timecode. | PD invariant 11: generated visuals are not evidence. Diagrams must read as **PD's own drawings** — clean line work, PD's type, no ageing, no coffee rings, no scan artefacts, no fake stamps with real names. The **content** of a quoted document may be set as a typographic card (that is how EP67 handled the OFAC letter); the **object** may not be forged. |
| ⛔-15 | **Any claim about Duncan's or Gillum's state of mind, motive, character, finances or private life that is not one of DC-04 … DC-18.** Specifically forbidden: "he knew it would fall", "he didn't care", "he was cutting costs", "he was too busy chasing fees", "he lied to save money", any interior monologue, any imagined scene. | **Both men were named publicly, were disciplined by a state board, and may be living.** The retrievable record supports exactly this and no more: the drawings did not communicate what he says he intended (RV-06); he did not do the calculations (CH-09); he told a technician it was *"basically the same as the one rod concept"* (CH-10); he told an architect it was sound (CH-08); he did not review the connection or assemble it (RV-10, RV-11); the firm's own procedure required that check (RV-09); Gillum's seal was on the plans and he denied that this made him responsible (DC-09); the atrium recheck was reported as done and was not done (RV-17, RV-18); a tribunal found **conscious indifference to a professional duty** and a court affirmed it (DC-14, DC-20). **That is a devastating record and it needs no embellishment. Say those things; invent nothing past them, and attribute every one to the tribunal that found it.** |
| ⛔-16 | **Blaming the architect, the contractor, Havens Steel Company, the City of Kansas City, or the hotel owner.** | Havens is a **named company**; the architect and contractor stamped the drawings (RV-01) but **no tribunal retrieved this pass made a finding against any of them**, and the Missouri Board did not investigate the architects at all (ND-07). Havens' position — that it built what the engineer's drawings communicated had already been designed — is itself in the record (RV-07). **The film may lay out the chain; it may not assign fault outside the findings.** |
| ⛔-17 | **Quoting the *Duncan* opinion's summary of a party's argument as if it were the court's own finding**, and above all quoting **Gillum's testimony (DC-09) as narration.** | DC-09 is a quoted answer under cross-examination, reproduced in a footnote. It is superb material — *as testimony, attributed*: "asked whether his seal made him responsible for the fabricator's shop drawings, Gillum answered…". Never in the film's own voice. |
| ⛔-18 | **"The engineers went to prison" / "were convicted" / "were criminally charged".** | **They were not.** No criminal charges were ever filed (DC-21). What happened is rarer and more interesting: a **state licensing board** revoked their licences, and it was **the first time American engineers lost their licences for gross negligence** (DC-19). Getting this wrong throws away the ending. |
| ⛔-19 | **"The ASCE expelled him."** | The ethics committee **recommended** expulsion; the board of direction **suspended him for three years**, and he then relinquished membership himself (PR-03, PR-04). The gap between the recommendation and the vote is the point — do not collapse it. |
| ⛔-20 | **Any statement about what Duncan or Gillum is doing now, where they live, whether they are alive, or what they think today.** | The most recent retrieved information is **1994–95** (DC-23), thirty-one years old at build date. ○-06. **Do not update it from memory.** If the film needs a closing line about them, it must end at the revocation, or the gate must be closed with a document first. |
| ⛔-21 | **Describing NBS BSS 143 as "the NIST report" or dating it to anything but May 1982.** | It is the **National Bureau of Standards**, which became NIST in 1988. The report is 1982 and NBS is what it says on the cover. |

**21 quarantine entries.**

---

## 12. ✅ WHAT THE FILM SHOWS INSTEAD — decided here so the designer does not improvise it

**This is a binding shot vocabulary, not a suggestion. Every prohibited image in §11b has a named
replacement. All of it is buildable with PD's existing toolkit (MOTIONKIT, FigureBeats, depth, 3D) plus the
commercial-cleared archive shelf. None of it requires a single frame of third-party news footage.**

### The five hero objects — the film's entire visual identity

| # | Object | What it does | Where it recurs |
|---|---|---|---|
| **H1** | **THE ROD.** A single 1¼-inch threaded steel rod, macro, slowly rotating on black, hard raking light on the thread. | The cold open and the last shot. One object, one film. | 6–8 returns |
| **H2** | **THE CONNECTION, EXPLODED AND ASSEMBLED.** Two MC8×8.5 channels rotating toe to toe, the longitudinal weld running, the hole, the washer, the nut, the rod through it — assembled on screen, in one continuous 3D move. | **This is the film's best idea and it comes straight out of the record**: the finding was that the engineer *"did not, in accord with usual engineering practice, assemble its components to determine what the connection looked like in detail"* (RV-10). **The film performs, on screen, the act that was not performed.** Do it once at full length in act two, and reprise it in three seconds at the end. | 2 full, 3 short |
| **H3** | **THE TWO DRAWINGS.** PD's own clean line drawing of the one-rod detail beside the two-rod detail, drawn live, the second rod arriving with a single stroke and a 4-inch offset. **PD's line, PD's type — never a facsimile of S405.1 or Shop Drawing 30 (⛔-14).** | The change, every time it is mentioned. | 4 returns |
| **H4** | **THE LOAD BAR.** One horizontal bar, four states, returned to whenever a number is spoken: **20.3 → 40.7 → required 68 → available 18.6**, with the 21.4 marker for the night itself. Consistent colour, consistent position, never redesigned. | The arithmetic of §5 made watchable. Four appearances so the audience learns to read it. | 4–5 returns |
| **H5** | **THE PULL-THROUGH.** The rod, washer and nut travelling downward through the box-beam web in slow motion — the actual failure mode, shown once, as steel deforming, **with nothing else in frame.** | The moment of failure, rendered as an object, not as an event. | 1, at the collapse beat |

### The substitution table — for every forbidden image

| Beat the film must reach | ⛔ What it must not show | ✅ What it shows instead |
|---|---|---|
| The tea dance | The crowd, dancers, the band, faces | An **empty ballroom floor**: one wooden dance floor, one bandstand with no band, one row of chairs, warm 1981 tungsten. Room tone and a distant big-band cue. NBS's own timeline as type: `3:00 PM — People begin to arrive` |
| The lobby filling | The full lobby at 7 p.m. | The **same wide atrium plate at 3:00 p.m., 4:30 p.m. and 7:00 p.m.**, unpeopled, with the timeline card advancing. The audience fills the room themselves; that is stronger and it is safe |
| The moment of collapse | Any depiction of the fall with people; any recreation; any archive frame | **H5 pull-through**, 3 seconds. Then **cut to black and cut the sound.** Hold black for a full beat. Then a single line of type: `7:05 PM` |
| The aftermath | Debris with casualties, rescue, cranes over bodies, hospital | **NBS's own timeline on black**, one line at a time, in NBS's words: `7:08 — first call for help` · `7:19 — call goes out for cutting tools` · `7:23 — call goes out for a forklift` · `8:30 PM — heavy crane arrives` · `4:30 AM — last survivor removed from debris`. **The words are the federal report's; the screen holds nothing but the words.** This is the most powerful two minutes available and it contains no image at all |
| The dead | Any body, any name, any face, any memorial photograph | **One number, held.** `114`. Then, if it earns it, the second number: `1,500–2,000 people were in the lobby` |
| The engineers | Duncan's or Gillum's face or likeness | **Hands only**: a hand rolling a drawing flat; a hand setting a professional seal (generic, no name, no state artwork) onto paper; an empty draughting stool. Three stamps landing on a drawing edge for the contractor, the structural engineer and the architect (RV-01) — three sounds, and the drawing unchanged |
| The hearing | Courtroom recreation, judge, faces, gavel | **An empty administrative hearing room**, one table, one microphone. A stack of paper 442 pages high, in one shot, with the page count as type. Twenty-seven ticks on a calendar |
| The revocation | A person receiving news; a real certificate | **A generic engineering certificate**, face down. Then the date: `22 January 1986` |
| The hotel today | The real building, its logo, its signage | Do not go there. Close on **H1, the rod, alone** — and, if a closing image of the space is wanted, an original wide of a generic atrium in which a **single span rests on two columns** (PR-08, described, never photographed) |

### Real footage: what is allowed

Archive-shelf and licensed stock only, and only **generic, non-event, non-identifying** material:
steel fabrication and welding · threaded rod and fasteners on a bench · a structural test frame and a dial
gauge · draughting tables, parallel rules, pencil on vellum · blueprint tubes and flat files · a big-band
ballroom with no identifiable people · hotel atria that are **not** the Hyatt Regency · Kansas City exteriors
and skyline · steel channel stock in a yard. **Every clip is eyeballed before it is cut in** — the standing
trap is a broadcast logo burned into a frame that the ledger title never mentions. **No clip that contains a
collapse, a rescue, a casualty, a hospital, or a news graphic, ever.**

### Onscreen text rule

Quoted document text may be set as a **typographic card in PD's own type** — that is how the NBS conclusions
and the court's findings should reach the screen, and there is a lot of very good language to use. It must
never be styled as a photograph or scan of the original (⛔-14). Every card carries its source in small type:
`NBS Building Science Series 143 (1982)` or `Duncan v. Missouri Bd., 744 S.W.2d 524 (Mo. App. 1988)`.

---

## 13. ○ OPEN QUESTIONS — what a viewer will ask that this pass cannot answer

**Nothing here may be spoken, shown, or implied until it is upgraded from a source read directly.**

| ID | Question | Why it is here |
|---|---|---|
| ○-01 | **What does the 442-page Commission decision actually say?** Case AR-84-0239, filed 15 Nov 1985. | Not retrieved. Everything about the Commission's findings comes from MOCA reviewing them and JPCF quoting Judge Deutsch's pages. That is enough for the findings; it is **not** enough to narrate the twenty-seven days of hearing, to describe testimony not quoted in MOCA, or to say what any witness said. |
| ○-02 | **The Missouri Board's own revocation order and case file.** | Not retrieved. Date and effect come from MOCA @1445 and JPCF @23849 only. |
| ○-03 | **Moncarz & Taylor, *Engineering Process Failure*, and Luth, *Chronology and Context* (JPCF 14(2), 2000).** | ASCE Library serves a JavaScript shell; WebFetch 403. If the film wants a second scholarly voice on the review chain, retrieve them first. The chain itself is already closed from MOCA (§7). |
| ○-04 | **When and how the toll went from 113 to 114.** | ⛔-03. No retrieved document explains it. |
| ○-05 | **What the civil litigation finally cost, and when it ended.** | Only the December-1983 insurer figure is sourced (DC-22). ⛔-07. |
| ○-06 | **Are Duncan and Gillum living, and what has happened since 1995?** | The freshest retrieved information is JPCF's 1994–95 interviews (DC-23), now **thirty-one years old**. ⛔-20. **This must be checked at script lock, and again at publish, because an R3 episode that criticises named professionals cannot be wrong about whether they are alive.** |
| ○-07 | **What stands in the atrium today?** | PR-08 describes the replacement span **as at 2000**. The hotel has changed hands and names since. Re-verify before any present-tense sentence. |
| ○-08 | **Did the Kansas City Building Code, Missouri licensing law, or AISC/ASCE practice change *because of* this?** | **Nothing retrieved this pass establishes a causal change.** The 1976 ASCE canon predates the collapse (PR-01). Any "and that is why today…" sentence is unsourced. **This is the most tempting unsourced ending in the whole episode.** |
| ○-09 | **How the shop-drawing review process is supposed to work in current practice.** | Outside every document retrieved. Do not generalise from a 1979 project to 2026 practice. |
| ○-10 | **What Havens Steel Company's own engineers said, in their own words.** | MOCA reports what Havens *did* and the basis on which it prepared its drawings (RV-07). No testimony from Havens is quoted. ⛔-16. |
| ○-11 | **The number of people on the fourth-floor walkway.** NBS considered eyewitness estimates of 40–50 an exaggeration and used 3–4 per span. | Genuinely uncertain in the record itself (FN-11). Say what NBS concluded (63 combined, upper bound) and stop. |
| ○-12 | **Whether the demand measurement holds.** The 2026-08-11 `yt-dlp` scan (18 long-form results, median 53,889, 7 channels over 100k, max 1,634,548, best 30-minute-band result 200,154) was supplied by the owner and **was not re-run by this pass**. | Recorded as measurement with attribution, not as this pass's own work. Per the EP60 precedent, saturation must be measured, not inherited — if the runtime band is contested, re-run `scripts/topic_demand_probe.py`. |

**12 open questions.**

---

## THE SHAPE THE FACTS ALREADY HAVE

*Not a claim — a note for the writer.*

```
   WHAT WAS DRAWN                          WHAT WAS BUILT

   roof ═══╤═══                            roof ═══╤═══
           │                                       │
           │  one rod                              │   rod A
   4F ─────┼─────                          4F ─────┴─────      <- carries BOTH walkways
           │      <- 4F sits on its own            ╷              40.7 kips, needing 68,
           │         nut: 20.3 kips                ╷  rod B       having 18.6
   2F ─────┴─────                          2F ─────┴─────
              20.3 kips                              20.3 kips (unchanged)

   Nothing got weaker. One beam was simply asked to carry two.
```

The record hands the film four beats, in order:

1. **1978–79.** A connection is drawn that does not meet the Kansas City Building Code even as drawn — 60
   percent of the required capacity (LD-15, LD-16). Nobody notices, because the calculations that would have
   shown it were never produced and, so far as the record goes, never made (ND-03, CH-09).
2. **January–February 1979.** The fabricator, for fabricating reasons, proposes two rods instead of one
   (CH-05). It is approved (CH-08). The shop drawings are stamped by three parties (RV-01). A technician
   raises it, and is told the two-rod arrangement is *"basically the same as the one rod concept"* (CH-10).
   **The load on the fourth-floor connection has just doubled** (LD-04).
3. **October 1979.** The atrium roof collapses during construction, and the firm is paid to check every
   connection in the hotel. It reports: *"we then checked the suspended bridges and found them to be
   satisfactory"* (RV-17). It had checked the roof steel (RV-18). **This is the second chance, and it is the
   most damning fact in the file, because it happened after the change and before anyone died.**
4. **17 July 1981, 7:05 p.m.** Sixty-three people, at most, on two walkways carrying about half the load the
   code assumed. The connection was never going to be able to say no.

**The hinge is LD-17.** Had the change never been made, the connections — illegal, undersized, uncalculated —
would still have held that night. The film's whole engineering argument fits in one sentence: *the change did
not make the steel weaker; it doubled what the same steel was asked to carry, and the steel was already only
sixty percent of legal.*

**And the honest complication the film owes the viewer** is the one the tribunal itself wrestled with. The
Commission did not find that any single act was grossly negligent; it found that *"it is only after a complete
analysis of their overall performance within the system that any judgment of their conduct can be made"*
(DC-17), and the court's own footnote concedes *"the original inadequacies of the structural drawings might
not have been critical if a meaningful review of the shop drawings had occurred"* (DC-18). Every individual
in this chain did something ordinary. A drawing left a detail to the fabricator. A fabricator solved a
fabrication problem. An engineer answered a question on the phone the way engineers answer questions on the
phone. Three parties stamped a drawing. **A film that makes any one of them a villain will be less true and
less frightening than a film that shows a system in which everybody's ordinary behaviour was, in combination,
lethal — and then lets a state board say, on the record, that responsibility for that combination is
non-delegable** (DC-12, DC-13).

---

*Built 2026-08-11 from three documents retrieved and read this pass: **NBS Building Science Series 143**
(427,229 chars — the federal investigation, all twelve chapters), the **Missouri Court of Appeals' published
opinion in `Duncan v. Missouri Board`, 744 S.W.2d 524** (66,251 chars — the state disciplinary record on
appeal, from the Harvard Caselaw Access Project's copy of the official reporter), and **Pfatteicher, JPCF
14(2):62–66 (2000)** (36,269 chars — peer-reviewed ASCE). **No fact in this ledger comes from memory, from a
secondary retelling, from an engineering-ethics teaching case, or from a subagent's unverified report.**
**138 fact rows** (identity 8, evening 12, design 12, the change 12, load arithmetic 20, findings 14, review
chain 19, discipline 23, profession 8, not-established 10) · **21 quarantine entries** · **12 open
questions** · a **binding substitution table** for every image the film may not show. **136 distinct
quotations are machine-verified ✓ VERBATIM** and re-verifiable with
`episodes/PD-2026-069-hyatt/01_research/sources/verify_quotes.v001.py` (136/136, exit 0). CourtListener
returned **HTTP 429** again and nothing depends on it. **Gate ○-06 (are the named engineers living?) must be
closed before the script locks.** Nothing here has been written into a script.*
