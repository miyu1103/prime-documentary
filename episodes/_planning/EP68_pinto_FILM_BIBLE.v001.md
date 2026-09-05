# EP68 · THE FORD PINTO / *GRIMSHAW v. FORD MOTOR CO.* — FILM BIBLE v001

**Episode `PD-2026-068-pinto` · slug `pinto` · 2026-08-11**
**Binding inputs, all read in full before this was written:**
`EP68_pinto_FACTS_LEDGER.v001.md`（107 fact rows・118 machine-verified ✓ VERBATIM・20 quarantine・
14 open questions）／ `EP68_pinto_PACKAGING.v001.md`（承認待ちの前面。タイトル・サムネ・冒頭22.5秒）／
`episodes/PD-2026-068-pinto/episode_spec.v001.json`（機械契約・`check_episode_spec.py` 緑）／
`EP68_pinto_FOOTAGE_PLAN.v001.md`（623クエリの実測）／`docs/PD_ONE_PASS_PRODUCTION_SPEC.v2.md`／
`docs/PD_CANON.md`／`.claude/rules/19-ship-gate.md`。

**着手前に台帳の検証器を回した。** `verify_quotes.v001.py` → **118 checked / 0 failed**。
**そのうえで、台帳が開けたまま残していた出典ゲートを2本閉じた**（§0.5）。この文書に出る引用は
すべて、その118本か、§0.5 の新規取得文書をこのパスが**ページ画像で直接読んで**採ったものである。
**記憶から書いた引用は一つも無い。**

---

## 0. この映画が扱う四つの危険

この題材には、他のどの回にも無い種類の危険が四つ同時にある。**先に書いておく。**

1. **感情の中心が、映せない。** *Grimshaw* の車に乗っていたのは、火傷で亡くなった女性と、
   13歳で生き延びた少年である。Richard Grimshaw は**当時13歳で、生きている可能性がある**。
   彼を描いた画・火傷した子ども・火傷した人・負傷者の記録映像——**一枚も作らず、一秒も使わない**
   （⛔-08）。Lilly Gray も同じ扱いである（⛔-09）。**では何を映すのか**を improvise させないために、
   §3.5 に**拘束力のある差し替え表**を置いた。あれは提案ではなく契約である。
2. **相手が生きている実在の企業である。** Ford Motor Company は今日も営業している。
   批判の一語一語が、**判決の認定か、取得した文書の文言**に載っていなければならない。
   ドキュメンタリー伝承（"Ford は人が焼け死ぬ方が安いと計算した"）は ⛔-02 で全面禁止である。
   **個人を有責として名指ししない**（⛔-10）——この映画がほとんどその報告書の話であるにもかかわらず、
   報告書を書いた二人の技術者を含めて、である。Elkhart の大陪審は
   ✓ *"could have indicted individual Ford executivs, but chose to charge only the corpora-"*（IN-06）。
   **大陪審が止まったところより先へ行かない。**
3. **この映画は、通説を別の通説に置き換える誘惑と隣り合わせである。** 反証側（Schwartz）は、
   同じページで **Pinto は Vega が通ったテストに落ち続けた**（CC-08）と書き、
   **Pinto は車の1.9%で追突火災死の4.1%だった**（CC-06）と書き、
   **Ford 自身の比較メモは Pinto を Vega・Toyota・Mazda・Datsun より悪いと示しており、
   Ford はそれを自分の刑事裁判に出さなかった**（CC-07）と書いている。
   さらに、このパスで読んだ p.1033 で彼はこう書いている——
   ✓ *"Yet even if the general portrayal of the Pinto as a firetrap should be rejected as false, a
   limited core of the firetrap myth seems fair enough."*
   **この一文が無い版は出荷しない。**
4. **数字が論証そのものである。** $11 と $15.30、$200,000 の帰属、11,000,000台と1車種、
   500–900 と 27、$125,000,000 と $3,500,000。**五組すべてが台帳の ⛔ 項目であり、
   五組すべてが「合体させると嘘になる」という形をしている。**だから AE キネティックが7本ある
   （§12.5）。あれは装飾ではなく、間違えないための機構である。

---

## 0.5 このパスで閉じたゲート — 台帳 v002 に取り込むべき新規行

**台帳 v001 は二つの穴を明記して閉じていた。うち一つは完全に、もう一つはほぼ閉じた。**
以下は**このパスが直接取得し、ページ画像で読んだ**新規行である。台帳 v002 でこの節を吸収するまで、
**この表がその行の正典**であり、脚本はここに載っているものしか語れない。

**新出典**

| Tag | Document | Retrieved this pass |
|---|---|---|
| **NH2** | **NHTSA Office of Defects Investigation, INVESTIGATION REPORT PHASE I, C7-38**, "Alleged Fuel Tank and Filler Neck Damage in Rear-End Collision of Subcompact Passenger Cars — 1971-1976 Ford Pinto / 1975-1976 Mercury Bobcat", **May 1978**. Stamped `OFFICIAL USE ONLY`; the cover states `A PORTION OF THIS REPORT HAS BEEN WITHHELD FROM THE PUBLIC FILE PURSUANT TO 5 U.S.C. 552(b)(4).` | **YES.** 1,160,900 bytes, 18 page images extracted, released text runs to report page 10. Cover, pp.2, 3, 4 and 10 **read on the page image by this pass**. `SRC-0008_nhtsa_odi_c7-38_investigation_report_phase1_may1978.pdf`, sha256 `ab3c5866…0dae02` |
| **SW2** | The remaining **44 pages of Schwartz** (1015, 1017–1018, 1020, 1023–1024, 1026–1027, 1033–1068) | **YES.** All read as images. pp.1024, 1033, 1066 and 1067 **re-read independently by this pass** against the transcription; all four matched character for character |
| **LE** | Matthew T. Lee, **"The Ford Pinto Case and the Development of Auto Safety Regulations, 1893–1978"**, *Business and Economic History* **27:2** (Winter 1998), pp. 390–401 — open access from `thebhc.org` | **YES.** 706,759 bytes; p.399 **re-read on the page image by this pass**; both quotations below matched exactly. **Ermann is not an author of this paper** |
| **LEA** | Lee & Ermann, *Social Problems* 46:1 (1999) — **the abstract only** | **PARTIAL.** Genuinely closed access (Unpaywall `oa_status: closed`, no repository copy anywhere). Publisher abstract held via OpenAlex. **Nothing may be attributed to this paper beyond the abstract text** |
| **GC** | ***Granite Construction Co. v. Superior Court*, 149 Cal. App. 3d 465** (Cal. Ct. App., 1 Dec 1983), No. F002297 — **a published court opinion that recites the Indiana prosecution by its filing number** | **YES.** Harvard CAP static archive, `static.case.law/cal-app-3d/149/cases/0465-01.json`, 36,631 bytes, sha256 `091fb519…0b3d071c`. **The footnote was located by exact string search in the opinion body by this pass** |
| **ILR** | **Indiana Law Review**, vol. 14 no. 1 (1981) — the state survey issue, whose products-liability article treats the criminal case | **YES.** Internet Archive full text, 1,983,142 bytes. **All three occurrences of the cause number located by exact string search by this pass** |

**新規行**

| ID | Claim | Grade | Source |
|---|---|---|---|
| NH2-01 | The report's identity, in its own words on the cover: ✓ **"INVESTIGATION REPORT / PHASE I / C7 - 38 / ALLEGED FUEL TANK AND FILLER NECK DAMAGE IN REAR-END COLLISION OF SUBCOMPACT PASSENGER CARS / 1971 - 1976 FORD PINTO / 1975 - 1976 MERCURY BOBCAT"**, `OFFICE OF DEFECTS INVESTIGATION / ENFORCEMENT / NATIONAL HIGHWAY TRAFFIC SAFETY ADMINISTRATION`, **MAY 1978**. | ✓ VERBATIM | NH2 cover, read on the page |
| NH2-02 | ✓ **"Following public release of the article, 'Pinto Madness', the NHTSA initiated, on August 11, 1977, a preliminary evaluation of the alleged safety defect, and on September 13, a formal defect investigation case."** ⚠ Schwartz dates NHTSA's announcement to 13 September 1977 (PM-07); the agency's own report gives **two** dates and the film uses the agency's. | ✓ VERBATIM | NH2 p.2 |
| NH2-03 | What the investigation did, in the agency's list: asked ✓ **"The author of the magazine article, Mark Dowie"** for his documentation and evidence; processed consumer and Congressional letters; had the National Center for Statistics and Analysis search FARS; requested technical and legal data from Ford; worked with the Canadian Ministry of Transport; and ✓ **"A test program of staged vehicle-to-vehicle rear-end collisions was developed and a contract awarded for the performance of these tests."** | ✓ VERBATIM (two clauses) + ✓ | NH2 p.2 |
| NH2-04 | ✓ **"Of the consumer letters and other inquires, only one involved an actual report of a fire occurrence in a Pinto vehicle upon rear-end impact, not previously reported to the NHTSA through other sources."** It was a parked Pinto struck by a 1969 Pontiac Firebird; ✓ **"no bodily injuries and/or fatalities were sustained."** (`inquires` is the report's spelling.) | ✓ VERBATIM | NH2 p.3 |
| **NH2-05** | **THE FILM'S CENTRAL CORRECTIVE, NOW PRIMARY:** ✓ **"In total, the NHTSA is aware of 38 cases in which rear-end collisions of Pinto vehicles have resulted in fuel tank damage, fuel system leakage and/or ensuing fire. These cases have resulted in a total of 27 fatalities sustained by Pinto occupants, of which one is reported to have resulted from impact injuries. In addition, 24 occupants of these Pinto vehicles have sustained non-fatal burn injuries."** ⚠ **The clause "of which one is reported to have resulted from impact injuries" is not in Schwartz and must be spoken.** | ✓ VERBATIM | NH2 p.4 |
| NH2-06 | What **Ford** reported to NHTSA, as the report tabulates it: rear impact / fuel leakage / fire cases **35**; lawsuits and liability claims **29**; injuries including fatalities in all vehicles **107**; in Pinto occupants **57**; total fatalities reported **26**; fatalities sustained by Pinto occupants **25**; burn injuries **23**. Of the 29 claims: ✓ **"Number cases settled out of court or by judgement against Ford/defendants: 8"**, ✓ **"Number cases pending trial: 19"**, ✓ **"Cases settled in favor of Ford/under investigation: 2"**. **This is Ford's own count, given to the regulator, and it independently confirms CC-10.** | ✓ VERBATIM (three lines) + ✓ | NH2 pp.3–4 |
| NH2-07 | **NHTSA's own caveats on the FARS data**, which the film must carry whenever it uses a death number: ✓ **"Fire/explosion is not a standard data element on most police reporting forms"** · ✓ **"If a death due to burns occurred sometime after the crash, it is less likely that it would be reported on the officer's accident report."** · ✓ **"FARS does not record the cause of death, only its fact; it does not distinguish between deaths due to impact and those caused by the fire."** · ✓ **"The FARS cases examined disclosed limited availability of data necessary to establish accurate pre-impact closing speeds."** | ✓ VERBATIM | NH2 p.10 |
| SW2-01 | ✓ **"A design decision was made to place the fuel tank behind the rear axle rather than above that axle. A primary reason for this decision was that if the fuel tank were located above the axle the Pinto would have been left with a very small trunk."** | ✓ VERBATIM | SW p.1015 |
| SW2-02 | ✓ **"One problem was that only nine inches of 'crush space' separated the gas tank and the rear axle. The Pinto's bumper, moreover, was essentially ornamental."** ⚠ The court says **"9 or 10 inches"** (CAR-03). Two sources, two figures; say **"nine or ten inches"** and attribute. | ✓ VERBATIM | SW p.1015 |
| SW2-03 | And immediately, the other side of it, in Schwartz's own footnote: at the criminal trial a **prosecution** witness said in cross-examination that the Pinto's bumper was about the same as the Gremlin's, the Vega's and the Dodge Colt's — ✓ **"I would say they were all bad."** | ✓ VERBATIM | SW p.1015 n.6 |
| SW2-04 | ✓ **"In October 1971, Ford officials decided against incorporating any of these modifications into current Pintos; rather, it would wait until NHTSA clarified its position."** And: ✓ **"In 1973, NHTSA promulgated its fuel-tank standard but ruled that this standard would apply only to 1977 models."** | ✓ VERBATIM | SW p.1018 |
| SW2-05 | ✓ **"In the resulting suits against Ford, the jury—after deliberating for eight hours—awarded the Gray family wrongful death damages of $560,000"** ⚠ **$560,000 is Schwartz rounding. The reporter says $659,680 as awarded and $559,680 as entered (MN-01, MN-02). Use the reporter's figures and do not quote this clause for money.** Quotable only for **"after deliberating for eight hours"**. | ✓ VERBATIM (as scanned) | SW p.1017 |
| SW2-06 | ✓ **"In order to draw attention to the publication of a story that it believed was a political blockbuster, Mother Jones, which is edited in San Francisco, held a press conference in Washington, D.C., at which Mark Dowie, the article's author, was accompanied by Ralph Nader."** ⚠ The next sentence on that page says the article ✓ *"was later awarded a Pulitzer Prize"* — **quarantined, see ⛔-21.** | ✓ VERBATIM | SW p.1017 |
| SW2-07 | ✓ **"In fact, according to a NHTSA official only fifty-three percent of Pinto owners responded to the recall offer extended by Ford in 1978."** ⚠ Sourced by Schwartz to a **telephone interview**, not a document. Attribute it exactly that way. | ✓ VERBATIM | SW p.1042 n.118 |
| SW2-08 | ✓ **"This location, however, was by no means unique to the Pinto; rather, it was a commonplace at the time in American cars."** And: the plaintiffs' principal witness ✓ **"conceded in the latter case that he himself had not actually concluded that the above-the-axle gas tank location was the safer choice until sometime in 1977."** | ✓ VERBATIM | SW p.1027 |
| SW2-09 | **The document's true bibliographic identity:** ✓ **"The Ford report took the form of an attachment to a submission by Ford to NHTSA, dated September 19, 1973, captioned a Petition for Reconsideration of Federal Motor Vehicle Safety Standard No. 301"**. | ✓ VERBATIM | SW p.1020 n.21 |
| **SW2-10** | ✓ **"It was the rollover situation, and not the rear-end-impact situation, that was the subject of the Ford document."** ⚠ Schwartz's own limit, in the same footnote: the document added that analyses of other portions of the proposed regulation would also be examined. **Carry the limit.** | ✓ VERBATIM | SW p.1020 |
| **SW2-11** | **THE HONEST COMPLICATION, AND IT CUTS AGAINST THE FILM'S OWN THESIS:** ✓ **"Contrary, then, to my earlier understanding, in its standard-setting NHTSA was not, in the early 1970's, relying on a $200,000 life-value figure. In setting standards, however, NHTSA was indeed taking both monetary costs and safety benefits into account; in doing so, the agency was essentially finessing the question of the monetary value of life, while at the same time releasing documents that set forth a $200,000 life-value datum."** | ✓ VERBATIM | SW p.1024 |
| **SW2-12** | And, in the same footnote: ✓ **"the report indicated that its $200,000 figure represented the minimum but not the maximum that society should spend in preventing highway fatalities."** followed by ✓ **"The 1973 Ford report can fairly be faulted for not taking account of NHTSA's explanation of the implications of its own figure."** — with Ford's answer, also verbatim: ✓ **"Ford did indicate, however, that it was utilizing the NHTSA figure in part because it was higher than other life-value estimates known to the company."** | ✓ VERBATIM | SW p.1024 n.41 |
| **SW2-13** | **Why the *Grimshaw* judge kept it out:** ✓ **"Indeed, a primary reason given by the trial judge in ruling against the admissibility of the Ford report was that Ford was using the figure that NHTSA itself preferred."** | ✓ VERBATIM | SW p.1023 n.35 |
| SW2-14 | The criminal cause number, verbatim and twice: ✓ **"State v. Ford Motor Co., Cause No. 11-431 (1980)"** (n.11) and ✓ **"Exhibit Y, State v. Ford Motor Co., Cause No. 11-431."** (n.71). **Still not a primary court document — see §7.** | ✓ VERBATIM | SW pp.1017, 1031 |
| **SW2-15** | **The structural fact that explains the acquittal:** ✓ **"Because the reckless homicide statute had been enacted only in 1977, Ford could not be prosecuted for the reckless design of the Pinto; rather, the prosecution needed to show a reckless post-1977 failure by Ford to repair or warn. Largely because of the narrowness of the resulting issue, at trial the prosecution was not able to secure the admission of internal Ford documents on which it had hoped to build its case."** And: ✓ **"In March 1980 the Indiana jury found Ford not guilty."** | ✓ VERBATIM | SW p.1017 |
| **SW2-16** | **Schwartz's own case against Ford, which the film owes the viewer:** ✓ **"According to the evidence, the overall cost of this combination would have been $9; and it makes sense to assume that these items were turned down by Ford in planning the Pinto primarily on account of their monetary costs. It is plausible to believe, then, that because of these costs, Ford decided not to improve the Pinto's design, knowing"** — the sentence completes on the next page — ✓ **"that its decision would increase the chances of the loss of consumer life. Once a variety of misconceptions are stripped away, this limited core of the Pinto story remains."** | ✓ VERBATIM | SW pp.1034–1035 |
| **SW2-17** | ✓ **"Yet even if the general portrayal of the Pinto as a firetrap should be rejected as false, a limited core of the firetrap myth seems fair enough: the Pinto's record in rear-end fire fatalities was not only much worse than the all-car average but was apparently somewhat worse than the record of most (though not all) of its subcompact competitors."** | ✓ VERBATIM · **re-read on the page by this pass** | SW p.1033 |
| **SW2-18** | **THE LAST WORDS OF THE FILM:** ✓ **"From what I have been able to learn, as for safety the Pinto was a car that was neither admirable nor despicable. Its overall fatality rate was roughly in the middle of the subcompact range; its record was better than the subcompact average with respect to fatalities-with-fire; yet for the quite small category of fatalities-with-rear-end-fire, its design features apparently gave it a worse-than-average record. Hence, there was nothing clearly wrong in subjecting Ford to liability for harms resulting from that latter category of fires."** | ✓ VERBATIM · **re-read on the page by this pass** | SW pp.1066–1067 |
| SW2-19 | On Richard Grimshaw, and **the only thing the film may take from that page**: ✓ **"I find it all but impossible to imagine that any jury comprised of ordinary people could have returned from its deliberations to tell Richard that his injuries were rendered lawful and indeed socially appropriate because of the costs that Ford would have needed to incur in order to have avoided his accident."** ⚠ **The rest of that paragraph describes his injuries in detail. It is quarantined at ⛔-08 and is NOT reproduced here.** | ✓ VERBATIM | SW p.1043 |
| **LE-01** | ✓ **"It was written in 1973, three years after the first Pinto was sold, so it cannot be the document upon which design decisions (made in 1967-1969) were based."** | ✓ VERBATIM · **re-read on the page by this pass** | LE p.399 |
| **LE-02** | ✓ **"The dollar figure used in its cost/benefit analysis was actual NHTSA's estimate of the societal value of human life, not the estimated average corporate payout to families of burn victims."** (`actual` is a typo for `actually` in the published original; reproduced as printed. **If spoken, read it as "actually" and say so in the caption note.**) | ✓ VERBATIM · **re-read on the page by this pass** | LE p.399 |
| LE-03 | ✓ **"Although NHTSA was aware, years before Dowie's article was written, that the gas tanks in Pintos and all of the other cars of its class performed badly in rear-end collisions, it forced a recall of only the Pinto."** | ✓ VERBATIM | LE p.400 |
| LEA-01 | The 1999 paper's own abstract, and **nothing else from that paper may be used**: ✓ **"Using original documents and recent interviews, we argue that there never was a 'decision' to market an unsafe vehicle. Instead, the Pinto is better understood as a routine outcome of distinct organizational subunits, embedded in a larger network of interorganizational relationships."** | ✓ VERBATIM (publisher abstract) | LEA |
| **IN2-01** | **A COURT'S OWN RECITATION OF THE INDIANA CASE, IN A PUBLISHED OPINION.** Surveying the dozen corporate-homicide prosecutions then known, the California Court of Appeal wrote: ✓ **"The Pinto case, where a corporation was acquitted. (State v. Ford Motor Co. (1978) No. 5324, Ind. Super. Ct., filed Sept. 13, 1978, and discussed in Note, Corporate Homicide: Stark Realities of Artificial Beings and Legal Fictions, supra, 8 Pepperdine L.Rev. 367.)"** **This is the filing number in Elkhart Superior Court, and it is not 11-431.** | ✓ VERBATIM · **located by exact string search by this pass** | GC @19864 |
| **IN2-02** | **THE CAUSE NUMBER AT JUDGMENT, AFTER THE VENUE CHANGE:** ✓ **"State V. Ford Motor Co., No. 11-431 (Pulaski County Cir. Ct. (Ind.), Mar. 13, 1980)"** — three times in the same volume. ⚠ **5324 is Elkhart Superior at filing; 11-431 is Pulaski County Circuit at judgment. Both are correct and neither may appear on screen without its court.** ⛔-26. | ✓ VERBATIM · **three occurrences located by exact string search by this pass** | ILR @73096, @186335, @217277 |
| **IN2-03** | **WHY NO INDIANA APPELLATE OPINION EXISTS — now proven rather than inferred:** ✓ **"This case was not ap- pealed from the trial level."** (the hyphen break is the scan). | ✓ VERBATIM | ILR @186335 |
| **IN2-04** | **The evidentiary core of the criminal trial, and the jury's own account of it:** ✓ **"the closing speed of the two vehicles was approximately thirty miles per hour and the fuel system vulnerability, the alleged product defect, would therefore be a cause in fact of the enhanced injuries. The defense disputed the prosecution's testimony and the conflicting evidence was permitted to go to the jury, which acquitted Ford."** and ✓ **"interviews with the jury after trial indicated that the issue of closing speed was never resolved by the jury."** ⚠ A law-review survey relying on Strobel and on daily reporting — **attribute it, do not state it as a finding.** | ✓ VERBATIM | ILR @189849 |
| IN2-05 | The same survey's own assessment, **which is an opinion and must be read as one**: ✓ **"Ford's acquittal was justified primarily by an evaluation of its conduct before the accident. Ford's demonstrated good faith efforts to expedite the Pinto recall program was probably decisive."** | ✓ VERBATIM | ILR @189849 |

**新規 ⛔ 項目**

| # | Forbidden | Why |
|---|---|---|
| ⛔-21 | **Saying "Pinto Madness" won a Pulitzer Prize.** | Schwartz writes it at p.1017 and this pass could not confirm it from any prize-awarding body. A film that corrects other people's unsourced claims may not repeat one. Say what is sourced: a Washington press conference with Ralph Nader (SW2-06). |
| ⛔-22 | **Merging the two Ford cost-saving figures.** The opinion's footnote quotes exhibit 125 as ✓ *"A design cost savings $10.9 million (1974-1975)"* (MG-04); Schwartz describes the same April 1971 memorandum as recommending deferrals that would *"realize a design cost savings"* of **$31.6 million** in 1974 and 1975, across several Ford models. | Two different figures from two readings of one document. **The film uses the opinion's $10.9 million, because the opinion is the document that was in evidence, and it does not mention the other figure at all.** |
| ⛔-23 | **Saying that NHTSA valued a life at $200,000 for the purpose of writing standards.** | SW2-11. NHTSA **published** the datum and did **not** rely on it in standard-setting; it also said $200,000 was a **minimum, not a maximum** (SW2-12). The film may say the figure is NHTSA's published figure, that the memo attributes it to NHTSA twice, and that the memo says Ford does not accept or concur — and must then say SW2-11 and SW2-12 in the same breath. |
| ⛔-24 | **Presenting NHTSA's 27 without the clause "of which one is reported to have resulted from impact injuries", or without NHTSA's own FARS caveats.** | NH2-05, NH2-07. The film's whole argument is that people quote a number without its document. It cannot then do the same thing with a better number. |
| ⛔-26 | **Putting `5324` and `11-431` on screen as one number, or either of them without its court.** Also: **do not say the criminal-recklessness count was dropped before trial, and do not name any Indiana judge.** | IN2-01 vs IN2-02: the venue changed from Elkhart Superior to Pulaski County Circuit, which is why there are two numbers. The "dropped count" and the pretrial judge's name came to this pass as a subagent's summary and **were not found in any document this pass read** — they are leads for a later session, not facts (§13 item 15). |
| ⛔-25 | **Using the Elkhart Public Library's photograph of the crashed 1973 Pinto** (`indianamemory` isl4 record 526), or any image of that vehicle, or the van driver's name. | It is the actual car in which three people died; ⛔-08/⛔-09 logic applies with equal force, and the catalogue record names a private individual who was never charged (⛔-11). Retrieved, recorded, **quarantined**. Its catalogue text also miscalls the charges "negligent homicide"; the AP wire says reckless homicide (IN-03). |

---

## 1. CONTROLLING IDEA

> **国が値段を出し、企業がその値段を引用し、雑誌がそのページを刷り、
> 陪審はその紙を一度も見ずに1億2500万ドルを評決した。
> 五十年間、誰もが引用してきたのは、別の話の表である。**

この映画は「Ford は正しかった」映画ではない。**「Ford は殺人者だった」映画でもない。**
形はこうである——**前半は、誰もが知っている話を丁寧に語り直す映画。後半は、その話が
どこで別の文書とすり替わったかを一枚ずつ剥がす映画。**
そして観客が最後に持ち帰るのは無罪でも有罪でもなく、**SW2-17 と SW2-18 の二文**である。

> ✓ *"Yet even if the general portrayal of the Pinto as a firetrap should be rejected as false, a
> limited core of the firetrap myth seems fair enough."*（SW2-17）
>
> ✓ *"as for safety the Pinto was a car that was neither admirable nor despicable … yet for the quite
> small category of fatalities-with-rear-end-fire, its design features apparently gave it a
> worse-than-average record. Hence, there was nothing clearly wrong in subjecting Ford to liability
> for harms resulting from that latter category of fires."*（SW2-18）

**通説は嘘で、しかも真実の方が Ford にとって都合が良いわけではない。**
この二重性がこの映画の全長である。

---

## 2. この映画が抱える問題と、それを構造にする方法

### 問題1：観客はすでに「答え」を知っていると思っている

この視聴者層（実測で93%男性・91%が55歳以上）は、Pinto の話を**当時**聞いている。
「Ford は人命を200,000ドルと計算した」は、彼らの記憶の中では**事実**である。
**その記憶を最初の20秒で否定すると、映画は最後まで疑われる。**

**構造にする方法：** **HOOK は通説を否定しない。**通説の**材料**を、通説より前に置く——
1973年9月、二人の技術者、8ページ、6ページ目の表。そして
「**ほとんど誰も、その表が何についてのものか気づかない**」で止める。
否定ではなく**予告**である。ACT_1〜ACT_3 は通説とほぼ同じ話を、しかし
**判決文と政府文書だけで**語る。剥がし始めるのは 17:40 の TURN からである。

### 問題2：反証が強すぎて、逆向きの嘘になりかける

$11 は Pinto の話ではない。$200,000 は NHTSA の数字である。メモは証拠から排除された。
Ford は刑事で無罪になった。**四つとも本当であり、四つ並べると「Ford は濡れ衣だった」に聞こえる。**
だがそれは、Schwartz 自身が書いていることと違う。

**構造にする方法：** **ACT_5 の後半（A5-11〜A5-14）を、反証への反証にまるごと使う。**
Vega が通ったテストに落ち続けたこと（CC-08）、車の1.9%で追突火災死の4.1%だったこと（CC-06）、
Ford 自身の比較メモを Ford が自分の刑事裁判に出さなかったこと（CC-07）、
そして **$9 の部品群**と Schwartz の結論（SW2-16）。
**しかも A4-13 で、$200,000 についての Schwartz 自身の撤回（SW2-11・SW2-12）を、
それが最も痛い場所で言う**——反証の最強の一手を出した直後に、その一手の限界を自分で出す。
これをやらない版は、この映画がやめさせようとしている振る舞いそのものになる。

### 問題3：見るものが無い、そして最も見たいものは映してはならない

法廷は映さない。書類は偽造できない（⛔-15）。人物は肖像を作れない（invariant 11）。
**そして衝突と火傷は、絶対に映さない**（⛔-08・⛔-09）。

**構造にする方法：** それを**貧しさではなく様式として扱い、しかも記録に根拠を持たせる。**
この映画の視覚の中心は**距離**である——後車軸と燃料タンクのあいだの
**9インチか10インチ**（CAR-03・SW2-02）。それを実寸のスチール定規で一度だけ測って見せ、
以後その画を五回返す。**衝突の代わりに、衝突が起きる空間を映す。**
そして最も強い一手は、**裁判所自身が止まったこと**である——
✓ *"no purpose would be served by further description of the injuries suffered by Grimshaw"*（PP-07）。
**この映画は裁判所が止まったところで止まり、止まったと声に出して言う。**（§3.5）

---

## 3. MOTIF — 五つのヒーロー・オブジェクト

一つの物を何度も、状態を変えて返す。**回るたびに意味が一段ずつ変わる。**
これは「同じ素材の使い回し」ではなく、`footage_diversity` が許す**意味のある反復**であり、
それ以外の被りは禁止である（§10）。

| # | オブジェクト | 何をするか | 回数 |
|---|---|---|---|
| **H1** | **THE GAP.** 車体を持ち上げたリフトの下、後車軸と燃料タンク前面のあいだに、実寸のスチール定規が渡してある。マクロ、下からの硬い作業灯。**目盛りは読めない。**距離だけが見える | この映画の全視覚の中心。衝突は映さず、**衝突が起きる空間**を映す。CAR-03・SW2-02 | 6回 |
| **H2** | **THE FLOAT.** キャブレターのフロートが、燃料色の液体を張ったガラス容器の中で、**沈む**。マクロ、実写速度、一度だけ | ✓ *"the carburetor float had become so saturated with gasoline that it suddenly sank"*（PP-03）。**この映画で唯一、記録が完全に説明している出来事**であり、だから唯一「再現」してよい出来事である。人は映らない | 2回（本編1・ENDING 0.8秒） |
| **H3** | **THE TABLE.** Table 3 を PD のタイポグラフィで一行ずつ組み上げる。180 burn deaths → $200,000 each → 2100 vehicles → $49.5 million → **11,000,000 cars** → $137 million。全部そろったところで**キャプションが上から降りてくる**：`STATIC ROLLOVER TEST PORTION` | 映画の TURN そのもの。**書類の写真ではない。PD の活字で、出典を小さく添えて出す**（⛔-15） | 1回（フル 70秒）＋ 3回（各3秒の再掲） |
| **H4** | **THE TWO PRICES.** 横並びの二枚のカード。左 `$11`、右 `$15.30`。下に出自が一行ずつ | ⛔-17 に対する機構。ACT_1 で右だけ、ACT_4 で左だけ、23:20 で両方 | 3回 |
| **H5** | **THE MIDDLE LANE.** 三車線の高速道路の中央車線を、真上から。空。アスファルトだけが動く | 1972年5月28日。**車も人も衝突も映さない。**車線だけを映して、そこで何が起きたかは判決文の言葉が言う | 4回（ACT_2 に2回、A5-01 に1回、ENDING に1回） |

**H1 と H4 のあいだに、この映画の全論証がある。**距離と値段。9インチと $15.30。
そのどちらも、$11 とは関係が無い。

---

## 3.5 差し替え表 — 映せないものの代わりに何を映すか（**拘束・改変には v002 が要る**）

**⛔-08 と ⛔-09 が禁じるすべての画に、名前の付いた代替がある。**
designer はここを improvise しない。**「代わりの画が無いので薄い記録映像を敷いた」は、
この表がある以上、起きてはならない。**

| 到達すべきビート | ⛔ 映してはならないもの | ✅ 代わりに映すもの |
|---|---|---|
| **1972年5月28日、Anaheim から Barstow へ** | 運転する女性、車内の人物、Lilly Gray として提示される誰か、ドラマ化された道行き | **H5・中央車線を真上から。**そして車の二つの事実だけを活字で：`6 MONTHS OLD` · `APPROXIMATELY 3,000 MILES`（PP-02）。ダッシュボードを撮るなら**運転席は空**で、手はフレーム外 |
| **失速** | 車内のパニック、ハザード、人の反応 | **H2・フロートが沈む。**マクロ。音は室内音とエンジンが落ちる音だけ。**この映画で唯一の「再現」であり、記録がそれを完全に説明しているから許される**（PP-03） |
| **追突そのもの** | いかなる衝突、いかなる後方からの接近ショット、いかなる再現、乗員のいる記録映像 | **何も映さない。**黒へカット、音を切る。**フルビート保持。**その上に一行の活字——判決文の冒頭一文（PP-01）を、出典を添えて。**この映画で最も強い15秒は、画が無い15秒である** |
| **火** | 燃える車、燃える人、火傷、救助、救急、病院 | **無し。**炎は一度も画面に出ない。代わりに**H5 に戻り、中央車線が空である**。ACT_2 のあいだ、この映画に火は一度も映らない |
| **Lilly Gray の死** | ドラマ化、遺影、葬儀、家族 | **黒地に活字一行**、判決文の言葉で：✓ *"Mrs. Gray died a few days later of congestive heart failure as a result of the burns."*（PP-05）。画は無い。次のカットまで2.0秒の無音 |
| **Richard Grimshaw の傷** | 火傷した子ども、火傷した人の顔、皮膚移植、手術、病院、**彼として提示される誰か**、内面の想像 | **裁判所が止まったことを映す。**PP-07 を活字カードで出し、ナレーションがそれを読み、そのうえで**この映画も同じところで止まると声に出して言う。**傷の描写はゼロ。彼の名は原告として一度だけ出る。**これが感情の中心であり、代替ではなく本命である** |
| **1978年8月10日、インディアナの三人** | 三人の写真、名前以上の人物像、事故車、Elkhart Public Library の写真（⛔-25）、バンの運転者 | **8月のインディアナ。**背の高いトウモロコシ、二車線の道、路肩。三人の名前を **AP の記事の言葉で一度だけ**活字で出し（IN-04）、それ以上は何も出さない。事故の描写ゼロ |
| **陪審と法廷（民事・刑事とも）** | 法廷の再現、陪審の顔、判事、木槌、証言台 | 石の外観、閉じた扉、無人の廊下、天井の高い空室。**六か月**を26週のカレンダーで、**8時間の評議**を時計盤一つで。刑事は**10週間**と**4日間の評議**を同じ形で |
| **Ford という会社** | Ford のバッジ、オーバル、実在の社屋、実在の Pinto、ディーラー看板、ナンバープレート | 無銘の1970年代サブコンパクトの**形**、組立ラインの機械、椅子が12脚ある無人の会議室、無地の社内封筒。**車の後部は無銘で、常に無人** |
| **メモそのもの** | メモの画像、複製、スキャンに見える生成物（⛔-15） | **H3。**PD の活字で、出典を小さく添えて。物としては**8枚という事実**だけ——クリップ、厚み、机の上の正方形。**一語も読めない** |
| **技術者たち** | Grush、Saunby、Iacocca、MacDonald、Copp、誰の顔も | **手だけ。**紙をそろえる手、クリップを掛ける手、定規を渡す手。空の製図椅子。**役職名は判決文と報告書が書いたとおりに活字で出し、それ以上は何も言わない**（MG-09・DOC-03・⛔-10） |
| **リコール** | 実在のリコール通知、Ford の手紙 | 郵便物の**量**：仕分け台を流れる無地の封筒。そして NHTSA のリコール記録の**数字だけ**を活字で：`78V143000` · `1,400,000` |

**実写素材で許されるもの：** 1970年代の一般車両と高速道路 · 組立ラインと工場機械 · 製図と道具 ·
無銘の事務所と会議室 · 印刷機と新聞輪転 · 石造の公共建築の外観 · インディアナの農地と小さな町 ·
時計とカレンダー · 群衆（顔は可、特定人物として提示しない） · 天候と薄暮。
**衝突・火災・救助・負傷者・病院・警察・葬儀を含むクリップは、どの時点でも一本も使わない。**
`episode_spec.forbidden_subjects` が題名で機械的に落とし、**人が目視でもう一度落とす。**

---

## 4. ARC — 五幕、二部構成

```
第一部：誰もが知っている話                第二部：その話が別の文書とすり替わった場所
HOOK  0:00.0–0:22.5   机の上の8枚
OP    0:22.9–0:36     見方の規則を一つ置く
ACT_1 0:36–7:10       作られた車（1968–1971）
ACT_2 7:10–12:20      1972年5月28日と、その裁判
ACT_3 12:20–17:40     記事と、役所
                                        ─── TURN 17:40 (60%) ───
                                        ACT_4 17:40–24:10  文書が実際に言っていること
                                        ACT_5 24:10–28:30  Winamac と、それでも残るもの
                                                     ─── RECOGNITION 27:20 (93%) ───
                                        ENDING 28:30–29:22.5  新事実ゼロ
```

**narration 総尺 1,762.5 s ＝ 29:22.5。＋ `ENDCARD_SEC` 9.0 で完成尺 1,771.5 s ＝ 29:31.5。**
契約帯 `runtime_seconds [1560, 1895]` の内側（導出は `episode_spec.notes` と §10）。

### TURN（転回・ペリペテイア）— ACT_3 末尾／ACT_4 冒頭 · **17:40**（全体の 60%）

ここまで観客が見てきたのは、**通説とほぼ同じ話**である。悪くない車ではないが良くもない車、
落ちたテスト、繰り延べを勧めた社内資料、死者、評決、記事、リコール。
転回は「Ford が悪くなかった」ことではない。**見ていた紙が違った**ことである。

**演出上の実装：** 17:40 で音楽を落とし、**2.5秒の無音**を置き、H3 の一枚目のカードを出す——
表の**キャプション**だけ、`BENEFITS AND COSTS RELATING TO FUEL LEAKAGE ASSOCIATED WITH THE
STATIC ROLLOVER TEST PORTION OF FMVSS 208`（DOC-06）。
ナレーションは一言だけ言う。**その表題を、これまで誰も読み上げなかった。**

### RECOGNITION（認知・アナグノリシス）— ACT_5 · **27:20**（全体の 93%）

観客が「そうか」と分かる場所は無罪判決ではない。**A5-13 である**——
Ford 自身の比較メモが Pinto を Vega・Toyota・Mazda・Datsun より悪いと示しており、
**Ford はそれを自分の刑事裁判に出さなかった**（CC-07）。
その直後に H1（距離）を最後にもう一度返し、**説明はしない。**

---

## 5. 声の設計（REGISTER）

- **HOOK と ACT_1 は、記録する声。**形容詞をほとんど使わない。年、寸法、価格、会議の日付。
  ✓ *"Ford's objective was to build a car at or below 2,000 pounds to sell for no more than $2,000."*
  のような文の**強さは事実側にあり、読み方で足すものではない。**
- **ACT_2 は、抑える声。**この幕で最も強いのは**言わないこと**である。判決文の一文を読み、黙る。
  **「悲劇」「痛ましい」「想像を絶する」は一語も使わない。**裁判所が使っていない。
- **ACT_3 は、並べる声。**雑誌が言ったこと → 役所がやったこと → 役所が数えたこと。
  形容せず、順に置く。**ここで対比を説明しない。**カードが二枚並ぶだけで観客は分かる。
- **ACT_4 は、読み上げる声。**この幕の三分の一は文書の原文である。
  **地の文と引用の境目が聞こえなければならない**（§12）。
- **ACT_5 は、譲る声。**反証を出したあとで、反証の限界を自分から出す。
  声を上げない。**Schwartz に上げさせる。**
- **ENDING は、数える声。**新事実ゼロ。数字を三つと、引用を二つ。

**禁止：**感情命令（"think about that", "let that sink in"）、二人称の詰問、
「衝撃の」「驚くべき」の類、そして**「〜だったのだ」型の断定**。
実測で、この視聴者層は感情命令に対して悪く反応する。

---

## 6. THE BEAT MAP — 幕あたり13〜17ビート・全ビートに台帳IDを付す

**契約 `figure_beats_per_act = [13, 17]`。**下の各幕はその帯の中にある。
**ビート＝画が変わり、主張が一つ進む単位**であり、カット数ではない（カットは §10）。
台帳IDの無いビートは**存在してはならない**（invariant 1）。

### HOOK — 0:00.0–0:22.5 · **PACKAGING §3 で承認待ち。ここでは変更しない。**（6ビート）

60語・0:00 から声。承認済みになるまで一語も動かさない。全8節の台帳照合は PACKAGING §3 の表にある。

### OP — 0:22.9–0:36.0 · 見方の規則を一つ置く（約36語・ブランド帯が 22.9–26.4 に重なる）

| # | ビート | 台帳 |
|---|---|---|
| OP-1 | 「8枚のうち2枚は、横転する車について書いてある」——**予告だけ。結論は言わない** | DOC-06（伏せる） |
| OP-2 | **この映画の読み方の規則**：これから引く判決文は、✓ *"the evidence in the light most favorable to the parties prevailing below"* で書かれている。**中立の記録ではない**と最初に言う | ID-06 ✓ ／ ⛔-13 |
| OP-3 | ブランド帯が下から上がり、3.5秒で抜ける。**声は止まらない** | PACKAGING §7 |

### ACT_1 — 0:36–7:10 · **作られた車**（17ビート）

| # | ビート | 台帳 |
|---|---|---|
| A1-01 | 1968年、Ford が新しいサブコンパクトの設計を始める。2,000ポンド以下、2,000ドル以下 | CAR-01 ✓ |
| A1-02 | ✓ *"a rush project, so that styling preceded engineering"* ——**設計がスタイリングに従った** | CAR-02 ✓ |
| A1-03 | タンクを後車軸の**後ろ**に置いた。理由の一つはトランクである | SW2-01 ✓ |
| A1-04 | **H1 初出。**残った潰れ代は**9インチか10インチ**。二つの出典が二つの数字を言う | CAR-03 ✓ ／ SW2-02 ✓ |
| A1-05 | バンパーは ✓ *"essentially ornamental"* ——**そして同じ脚注で、検察側証人が「どれも悪かった」と言っている** | SW2-02・SW2-03 ✓ |
| A1-06 | **その配置は Pinto に固有ではなかった。**当時のアメリカ車では普通だった | SW2-08 ✓ ／ ⛔-12 |
| A1-07 | 衝突試験。✓ *"the Pinto's fuel system as designed could not meet the 20-mile-per-hour proposed standard"* | CAR-04 ✓ |
| A1-08 | 21マイルで、タンクが前へ押され穿孔。給油管が引き抜かれ、デフのボルト頭が刺さった | CAR-04 ✓ |
| A1-09 | **NHTSA 自身の報告書も同じことを書いている**——初期試験で Pinto の成績は悪く、Ford は生産前に後部を一部変更した | NH2-01 · SW p.1018 n.12 ✓ |
| A1-10 | 直せた。価格表がある——側部部材 $2.40、クロスメンバー $1.80、フラックスーツ $4、ブラダー $5.25–$8… | CAR-05 ✓ |
| A1-11 | **$15.30。**強化後部構造・平滑アクスル・改良バンパー・追加潰れ代 —— **AEビート `ep68_kin_1530`** | CAR-06 ✓ ／ ⛔-17 |
| A1-12 | 試験結果は指揮系統を上がり、生産を決めた者たちが知っていた | MG-01 ✓ |
| A1-13 | 1971年4月、MacDonald が議長を務めた製品審査会。**exhibit 125** が配られた | MG-03 ✓ |
| A1-14 | exhibit 125 自身の言葉：✓ *"A design cost savings $10.9 million (1974-1975) can be realized by this delay."* | MG-04 ✓ ／ ⛔-22 |
| A1-15 | 同じ資料：✓ *"Currently there are no plans for forward models to repackage the fuel tanks."* / ✓ *"[s]mallest car line with most difficulty in achieving compliance."* | MG-05 ✓ |
| A1-16 | 1971年10月、Ford は改修を入れず、**NHTSA が態度を決めるまで待つことにした** | SW2-04 ✓ |
| A1-17 | 1973年、NHTSA は基準を出した。**適用は1977年モデルからだった** | SW2-04 ✓ |

### ACT_2 — 7:10–12:20 · **1972年5月28日**（15ビート）

| # | ビート | 台帳 |
|---|---|---|
| A2-01 | ✓ *"On May 28, 1972, Mrs. Gray … set out in the Pinto from Anaheim for Barstow"*。車は6か月落ち、走行約3,000マイル。**H5 初出** | PP-02 ✓ ／ §3.5 |
| A2-02 | **H2。**車線変更のあと、車が失速した。原因はタンクではない——ガソリンを吸ったフロートが沈んだ | PP-03 ✓ |
| A2-03 | 追突。**陪審が採った速度**は 28〜37マイル | PP-04 ✓ |
| A2-04 | **Ford の主張は正反対だった**——Galaxie は減速しておらず、50マイル超で当たった。**判決文はこれに一度も触れない** | CC-02 ✓ ／ PP-04 |
| A2-05 | 【**画が無い15秒**】判決文の冒頭一文を活字で。黒。音を切る | PP-01 ✓ ／ §3.5 |
| A2-06 | ✓ *"Mrs. Gray died a few days later of congestive heart failure as a result of the burns."* 黒地に一行。2.0秒の無音 | PP-05 ✓ |
| A2-07 | 13歳の同乗者は生き延びた。**そして裁判所はそこで説明をやめた**——✓ *"no purpose would be served by further description"*。**この映画も同じところで止まる、と声に出して言う** | PP-06・PP-07 ✓ ／ ⛔-08 |
| A2-08 | 他の被告とは和解し、✓ *"the case went to verdict only against Ford Motor Company."* | ID-08 ✓ |
| A2-09 | 六か月の審理。評議は**8時間** | MN-03 ✓ ／ SW2-05 ✓（金額には使わない） |
| A2-10 | 評決：Grimshaw に $2,841,000 と **$125,000,000**、Gray 家に $659,680 | MN-01 ✓ |
| A2-11 | 先行和解分を差し引いた判決は $2,516,000 と $559,680 | MN-02 ✓ |
| A2-12 | 新裁判の申立に対し、**懲罰的賠償を $3,500,000 まで返上することを条件に**却下 —— **AEビート `ep68_kin_jury_remittitur`** | MN-03・MN-04 ✓ ／ ⛔-06 |
| A2-13 | 判事の理由：Ford の純資産は77億ドルで不均衡ではない、と述べ、**それでも減らした**——補償賠償の44倍だから | MN-06 ✓ |
| A2-14 | そして判事は、**陪審が exhibit 125 を使ったとは言わないと明言した**。$125,000,000 への行き方は誰も知らない | MN-07 ✓ |
| A2-15 | Gray 家に懲罰的賠償は無い（当時のカリフォルニア法）。控訴審は1981年5月29日に**全部を維持**し、9月10日に上告が拒否された。**控訴審は数字を一つも変えていない** | MN-09・MN-05・ID-04 ✓ ／ ⛔-07 |

### ACT_3 — 12:20–17:40 · **記事と、役所**（15ビート）

| # | ビート | 台帳 |
|---|---|---|
| A3-01 | 1977年9/10月号、*Mother Jones*、Mark Dowie、"Pinto Madness" | PM-01 ✓ |
| A3-02 | 見出し文：✓ *"For seven years the Ford Motor Company sold cars in which it knew hundreds of people would needlessly burn to death."* | PM-01 ✓ |
| A3-03 | **500。そして「900に達する可能性がある」** —— **AEビート `ep68_kin_500_to_900`**。**取得した本文に出典が無い** | PM-02 ✓ ／ ⛔-01 |
| A3-04 | ✓ *"Ford waited eight years because its internal 'cost-benefit analysis' … said it wasn't profitable to make the changes sooner."* | PM-04 ✓ |
| A3-05 | ✓ *"This cost-benefit analysis argued that Ford should not make an $11-per-car improvement that would prevent 180 fiery deaths a year."* **この一文が以後五十年の記憶になる** | PM-05 ✓ |
| A3-06 | 雑誌は Washington で記者会見を開き、Dowie の隣に Ralph Nader がいた | SW2-06 ✓ ／ ⛔-21：**受賞歴は言わない** |
| A3-07 | **役所が動く。**NHTSA は**1977年8月11日**に予備評価、**9月13日**に正式な欠陥調査を開始した——**記事の公表を受けて**、と報告書自身が書いている | NH2-02 ✓ |
| A3-08 | 何をしたか：Dowie に根拠資料を求め、900件超の問い合わせを処理し、FARS を検索し、Ford に技術・法務データを求め、カナダ運輸省と連絡し、**追突試験を発注した** | NH2-03 ✓ |
| A3-09 | **消費者の手紙のうち、未知の火災を報告していたのは一件だけだった**——駐車中の Pinto、1969年式 Firebird、負傷者なし | NH2-04 ✓ |
| A3-10 | **Ford が役所に出した自社の数**：35件、訴訟29件、死亡26、うち Pinto 乗員25。29件の内訳は 8 敗訴か和解・19 係属・2 勝訴か調査中 | NH2-06 ✓ ／ CC-10 ✓ |
| A3-11 | **役所自身の総計：38件、27名、うち1名は衝撃による、非致死の火傷24名** —— **AEビート `ep68_kin_38_27_24`** | NH2-05 ✓ ／ ⛔-24 |
| A3-12 | **そして役所自身が付けた注意書き**を、役所の言葉で読む——警察の様式に火災欄は無い、後日の火傷死は載りにくい、FARS は死因を記録しない | NH2-07 ✓ ／ ⛔-24 |
| A3-13 | 1978年5月、欠陥の**初期認定**。6月14日に聴聞が設定された | RC-07 ✓ |
| A3-14 | 6月、リコール **78V143000**、**1,400,000台**。給油管の延長とポリエチレンの盾。**評決の12日後、聴聞の直前** | RC-01〜RC-04・RC-06 ✓ ／ RC-02 |
| A3-15 | **リコールに応じたのは53%だった**——NHTSA 職員が Schwartz に語った数字であり、**文書ではない**と言って出す | SW2-07 ✓ |

### ACT_4 — 17:40–24:10 · **文書が実際に言っていること**（17ビート）

| # | ビート | 台帳 |
|---|---|---|
| A4-01 | 【**TURN・2.5秒の無音**】H3 の一枚目：表のキャプションだけ。**その表題を、これまで誰も読み上げなかった** | DOC-06 ✓ |
| A4-02 | 文書の本当の名前：*Fatalities Associated with Crash Induced Fuel Leakage and Fires*、Ford Environmental and Safety Engineering、"Attachment II" | DOC-03 ✓ ／ ⛔-03 |
| A4-03 | それは何への添付か：**1973年9月19日付、FMVSS 301 の再考申立て**への添付である | SW2-09 ✓ |
| A4-04 | 一段落目が宛先を書いている：✓ *"The NHTSA has issued Notice 2 of Docket 70-20 and Notice 1 of Docket 73-20"* | DOC-04 ✓ |
| A4-05 | ✓ *"The analysis discussed below concerns the static rollover requirement proposed for FMVSS 301."* ⚠ **この紙は自分と矛盾している**——4ページは 301、表3のキャプションは 208。**どちらかを黙って選ばない** | DOC-06 ✓ |
| A4-06 | Schwartz が同じことを一文で：✓ *"It was the rollover situation, and not the rear-end-impact situation, that was the subject of the Ford document."* ⚠ 同じ脚注の限定も読む | SW2-10 ✓ |
| A4-07 | **H3 が組み上がる（1）：**✓ *"Savings - 180 burn deaths, 180 serious burn injuries, 2100 burned vehicles."* | DOC-07 ✓ |
| A4-08 | **（2）：**✓ *"Unit Cost - $200,000 per death, $67,000 per injury, $700 per vehicle."* 合計便益 $49.5 million | DOC-07 ✓ |
| A4-09 | **（3）——ここで表が別のものになる：**✓ *"Sales - 11 million cars, 1.5 million light trucks."* —— **AEビート `ep68_kin_11_million`** | DOC-07 ✓ |
| A4-10 | そして紙自身がこう書いている：✓ *"While these are Ford costs, they have been applied across the industry in this analysis."* **表に「Pinto」の語は無い** | DOC-08 ✓ ／ ⛔-03 |
| A4-11 | 同じ報告書は、**火災問題は政府が言うほど大きくないとも主張している**——24名の標本で。**これは規制当局に対する当事者の主張であり、認定ではない** | DOC-13 ✓ |
| A4-12 | **そして同じ報告書が、政府にこう告げている**——漏洩は追突で26%、正面衝突で3.5%。**Ford が追突火災を無視した証拠として使われる文書が、追突が最悪だと政府に書いていた** | DOC-14 ✓ |
| A4-13 | **$200,000 は NHTSA の数字である** —— **AEビート `ep68_kin_200000`**。紙はそれを二度そう書き、そして ✓ *"their use does not signify that Ford accepts or concurs in the values"* と書いている | DOC-10 ✓ ／ ⛔-04 |
| A4-14 | 【**この映画が自分の一手を弱める場所**】Schwartz は当初これで十分だと考え、**調べ直して撤回した**——NHTSA は基準策定でその数字に依っておらず、$200,000 は**最低であって上限ではない**と自ら書いていた。✓ *"The 1973 Ford report can fairly be faulted for not taking account of NHTSA's explanation of the implications of its own figure."* | SW2-11・SW2-12 ✓ ／ ⛔-23 |
| A4-15 | **そして *Mother Jones* は出自を正しく書いていた**——✓ *"And in a 1972 report the agency decided a human life was worth $200,725."* の二文前に、✓ *"Ford has a better idea: $200,000."* | DOC-12 ✓ |
| A4-16 | **その紙は、陪審に見せられていない。**✓ *"the 'Grush-Saunby Report'—was excluded from evidence"*。**そして排除理由の一つは、Ford が NHTSA 自身が好む数字を使っていたことだった** | DOC-01・DOC-02 ✓ ／ SW2-13 ✓ ／ ⛔-05 |
| A4-17 | **H4 が両方そろう。$11 と $15.30** —— **AEビート `ep68_kin_11_vs_1530`**。片方は横転、全産業、1973年。片方は追突、この一車種、判決文 | DOC-08・CAR-06 ✓ ／ ⛔-17 |

### ACT_5 — 24:10–28:30 · **Winamac と、それでも残るもの**（14ビート）

| # | ビート | 台帳 |
|---|---|---|
| A5-01 | 1978年8月10日、インディアナ。三人が亡くなった。**名前は AP の言葉で一度だけ。画は8月のトウモロコシと二車線の道** | IN-04 ✓ ／ §3.5 ／ ⛔-25 |
| A5-02 | 9月13日、Elkhart の大陪審が起訴。**reckless homicide 3件と criminal recklessness 1件** | IN-01・IN-03 ✓ |
| A5-03 | ✓ *"Maximum penalties would total $36,000 in fines."* | IN-03 ✓ |
| A5-04 | 大陪審は**個人を起訴できたが、しなかった** | IN-06 ✓ ／ ⛔-10 |
| A5-05 | **番号が二つある、というのがこの事件の形である。**Elkhart Superior Court に **No. 5324** として1978年9月13日に提起され——それを書いているのは**カリフォルニアの控訴裁判所の意見書**である——裁判地が移り、判決は **No. 11-431, Pulaski County Circuit Court** で下りた。審理は Winamac で10週間 | IN2-01 ✓ ／ IN2-02 ✓ ／ IN-11 ✓ ／ ⛔-26 |
| A5-06 | **無罪を説明する構造的事実：**その reckless homicide 法は**1977年制定**だったので、**設計は裁けなかった**。裁けるのは1977年より後の修理または警告の懈怠だけだった | SW2-15 ✓ |
| A5-07 | **その狭さのゆえに、検察は当てにしていた Ford の社内文書を法廷に入れられなかった** | SW2-15 ✓ ／ IN-14 ✓ |
| A5-08 | 争点は二つの衝突像だった。弁護側は他車の追突試験フィルムを流した | IN-12・IN-13 ✓ |
| A5-09 | ✓ *"It has just been a matter of David and Goliath when it comes to money."* ——ボランティアの検察団と、Watergate 検事が率いる弁護団 | IN-15 ✓ ／ ⛔-19 |
| A5-10 | **1980年3月13日、無罪。**争点は結局、閉合速度だった——そして**評決後の陪審員への取材では、その閉合速度の争点は陪審の中で決着していなかった**、とインディアナの法律雑誌が翌年書いている。**そしてこの事件は控訴されなかった。**だから州の上級審の判決文は存在しない | IN-09 ✓ ／ IN2-04 ✓ ／ IN2-03 ✓ ／ ⛔-19 |
| A5-11 | **【ここから、反証への反証】**NHTSA の衝突試験で、**Pinto は Vega が通ったテストに落ち続けた** | CC-08 ✓ |
| A5-12 | そして**その刑事裁判で**、検察側の専門家が FARS を追突火災死に絞ったとき——**車の1.9%、追突火災死の4.1%** | CC-06 ✓ |
| A5-13 | 【**RECOGNITION 27:20**】**Ford 自身の比較メモは、Pinto の追突火災死亡率を Vega・Toyota・Mazda・Datsun より上に置いていた。そして Ford はそのメモを自分の刑事裁判に出さなかった** | CC-07 ✓ |
| A5-14 | Schwartz の $9 の部品群と、彼自身の結論——✓ *"It is plausible to believe, then, that because of these costs, Ford decided not to improve the Pinto's design, knowing that its decision would increase the chances of the loss of consumer life. Once a variety of misconceptions are stripped away, this limited core of the Pinto story remains."* | SW2-16 ✓ |

### ENDING — 28:30–29:22.5 · **新事実ゼロ**（6ビート）

| # | ビート | 台帳 |
|---|---|---|
| E-01 | 38。27。24。**NHTSA, May 1978.** もう一度、注意書きごと | NH2-05・NH2-07 ✓（再掲） |
| E-02 | **⟨OQ-06 SLOT⟩** この映画が立っている記録は **1981年9月10日で終わる**。そして Winamac については——**別の州の裁判所が事件番号を書き、州の法律雑誌が判決日を書いた。起訴状そのものは、いまも Elkhart 郡書記官の簿冊の中にある。**取得できていない、とそう言う。§7 | ⛔-16・○-06・IN2-01〜IN2-03 |
| E-03 | $11 と $15.30。**H4 最後の一回** | DOC-08・CAR-06 ✓（再掲） |
| E-04 | ✓ *"a limited core of the firetrap myth seems fair enough"* | SW2-17 ✓ |
| E-05 | **最後の言葉**：✓ *"neither admirable nor despicable … Hence, there was nothing clearly wrong in subjecting Ford to liability for harms resulting from that latter category of fires."* | SW2-18 ✓ |
| E-06 | **H1 最後の一回。**距離だけ。そのあと `BrandEndcard` が 9.0 秒 | §3 |

---

## 7. ⟨OQ-06 SLOT⟩ — Winamac の記録をどこまで取れたか

**取れたものと取れなかったものを、別々に書く。混ぜない。**

### 取れたもの（このパスで閉じた）

1. **裁判所自身による、公表された意見書の中での提示。** *Granite Construction Co. v.
   Superior Court*, **149 Cal. App. 3d 465**（1983年12月1日）が、当時知られていた法人殺人訴追を
   数え上げる脚注でこう書いている——✓ *"The 'Pinto' case, where a corporation was
   acquitted. (State v. Ford Motor Co. (1978) No. 5324, Ind. Super. Ct., filed Sept. 13, 1978…)"*（IN2-01）。
   **裁判所が、事件番号と提起日と結果を書いている。**
2. **州の法律雑誌が、判決時の事件番号を三度書いている。** Indiana Law Review v.14 no.1（1981）——
   ✓ *"State V. Ford Motor Co., No. 11-431 (Pulaski County Cir. Ct. (Ind.), Mar. 13, 1980)"*（IN2-02）。
3. **なぜインディアナの控訴審判決が存在しないのかが、推測ではなく証拠で分かった。**
   ✓ *"This case was not ap- pealed from the trial level."*（IN2-03）。
4. 公判の争点と、**陣審員自身の事後の話**（IN2-04）。
5. 既取得の報道２本（APの起訴報道・CSM の評決報道）と、Schwartz の記述と事件番号（SW2-14）。

**これで、刑事編は「新聞２紙と法学論文１本」から、「裁判所の意見書・州の法律雑誌・報道２紙」になった。**

### 取れなかったもの（開いたまま）

**起訴状、ドケット、命令、評決書、公判調書——一枚も無い。**
CourtListener は前夜 HTTP 429（日次上限）。Indiana Archives の finding aid は
Elkhart County Clerk の **"Indictment Record-- Grand Jury (ledger)" Series-19750**（1868–1984、紙、Open、
1977–1979 を含む容器）の所在までは示すが、**簿冊本体をオンラインで出していない**し、
記載は series レベルであって事件名を持たない。Indiana の MyCase（`public.courts.in.gov`）は
接続拒否で、**内容について何も言えない**。

### だから ACT_5 はこうなっている

- **尺は 4分20秒のままである。** 二つの事件番号と控訴の不存在を得たことで、
  刑事編の**骨格**は固まったが、**中身**（証人、証拠、訴訟指揮）は依然として報道と
  二次資料にしか無い。**尺を伸ばすと、伸ばした分だけ二次資料にもたれかかる。**
- **A5-05 と A5-10 は、裁判所と州の法律雑誌の言葉で語れるように書き換えた**（§6）。
- **E-02 も書き換えた。** 「一枚も無い」ではなく、**何があって何が無いかを一文で言う**——
  別の州の裁判所が番号を書き、州の法律雑誌が判決日を書いた。起訴状はまだ Elkhart の簿冊にある。

**もし残りが閉じたら、変わるのはここだけである：**

| 取れた場合 | 差し替える場所 | 変わらない場所 |
|---|---|---|
| 起訴状の本文（IARA Series-19750 の請求、または Elkhart 郡書記官） | **A5-02 を原文で置換**し、**E-02 の後半を一文で置換**。所要 **+10〜15秒** | A5-06・A5-07（**なぜ検察が負けたか**は Schwartz が説明しており、起訴状で変わらない） |
| ドケットまたは評決書（Pulaski 郡州裁判所） | **A5-10 に一行足すだけ** | A5-11〜A5-14（**反証への反証**は民事記録と法学論文に載っている） |
| 何も取れなかった | **設計どおり。一語も変えない** | すべて |

**A5-02・A5-10・E-02 の三か所だけが差し替え可能な形で書いてある。**
それ以外の場所に Winamac の一次記録を前提にした文を仕込んでいない。これは意図的で、
○-06 が完全に閉じても閉じなくても**再レンダーが1回で済む**ようにするためである。

---

## 8. RETENTION MAP

実測（チャンネル全体）：10秒 87.6% / 15秒 76.9% / 20秒 71.4% / 30秒 60.4%。
**最も急な損失は 10→15秒で毎秒2.13ポイント**——post-60s の6倍。
深掘り調査（`DEEP_RESEARCH_FINDINGS.v001.md`）：**半減42秒**、**80–180秒の説明は禁止**、
**リビール階段は65–92%を保つ**。

| 位置 | 仕掛け | 根拠 |
|---|---|---|
| 0:00.0 | **声が最初のフレームから鳴る。**無音のモンタージュも、無音のカードも無い | PACKAGING §0 |
| 0:08.0–0:12.4 | 最強のビート（「表がある。数を数え、値段を付けている」）が **10→15秒の窓のど真ん中に落ちる** | PACKAGING §3 |
| 0:22.9 | ブランド帯は**問いの上に**乗る。問いの代わりに来ない | PACKAGING §4 |
| 0:36–1:20 | **80–180秒に説明を置かない。**ACT_1 は寸法と価格から入る——2,000ポンド、2,000ドル、9インチ | 深掘り調査 |
| 4:20 | H1（距離）初出。**リビール階段の一段目** | §3 |
| 7分ごと | 新しい問いを立てる（下表・6本） | 行16 |
| 12:20 | 記事が出る。**通説がここで初めて画面に出る**——ここまで一度も言っていない | §2 問題1 |
| 17:40 | **TURN。無音2.5秒 → 表のキャプション** | §4 |
| 19:50 | 登録カード（**声では言わない**・3.0秒） | PACKAGING §5 |
| 27:20 | **RECOGNITION。**Ford が出さなかった Ford のメモ | §4 |

### 立てる問い（7分に最低1回・6本）

1. 0:22 — その表は、何についてのものなのか（HOOK が残す）
2. 3:40 — 直すのに $15.30 だった。**では、なぜ直さなかったのか**（A1-11 → A1-14 が部分的に答える）
3. 9:50 — 陪審は1億2500万ドルをどこから出したのか（A2-14 ／ **答えは無い。判事が「言わない」と言った**）
4. 13:30 — 500から900人。**その数はどこから来たのか**（A3-03 ／ **記事に出典が無い**）
5. 18:40 — 11,000,000台。**この表は誰の話をしているのか**（A4-09 が答える）
6. 25:40 — 通説が全部間違っていたなら、**Ford は何も悪くなかったのか**（A5-11〜A5-14 が答える）

**問い3には答えが無く、それを言う。**「記録はここで止まっている」と言えることは弱さではない。

---

## 9. HOOK — 既に書かれている

`PACKAGING §3`。60語・0:00.0–0:22.5・全語が声。**この文書はそれを変更しない。**
フックが本編に負わせた義務は四つで、すべて §6 に配線済み：

1. 「8ページの報告書」——**A4-02/A4-03 で正式名称と宛先に戻る**
2. 「6ページ目の表」——**A4-07〜A4-09 で一行ずつ組み上げる**（H3）
3. 「4年後に雑誌が刷る」——**A3-01〜A3-05 で刷られる**
4. 「その表が何についてのものか、ほとんど誰も気づかない」——**A4-01 の TURN が答える。
   それが 17:40 であることがこの映画の設計そのものである**

---

## 10. WHAT THE IMAGES MUST CARRY — モーション予算（**紙芝居禁止**）

契約値：**`distinct_video_assets` 265 ／ `mandatory_stills` 104 ／ `target_cut_sec` 3.7 ／
`people_plates_min` 24（`people_plates` = R081–R104）**。
設計中心 1,762.5 s で **総カット 476 ／ 静止カット 152（31.9%）／ 映像カット 324**。
配分は `EP68_pinto_FOOTAGE_PLAN.v001.md` §2。

**尺と語数の導出（`episode_spec.notes` と同一）**
```
pace band (PD_CANON rule 25)                     159.5 .. 169.7 wpm
design word target                                        4,700
writing band script_words                            4,400 .. 5,000
R_lo = 60*4400/169.7 + 9.0 = 1555.7 + 9.0 =              1564.7 s
R_hi = 60*5000/159.5 + 9.0 = 1880.9 + 9.0 =              1889.9 s
declared runtime_seconds                              [1560, 1895]   -> contains both edges
design centre 4,700 words at 160.0 wpm = 1762.5 s narration + 9.0 = 1771.5 s = 29:31.5

DELIVERED DRAFT (script.en.v001, measured by check_script_craft)   4,895 words
  at 169.7 wpm  60*4895/169.7 = 1730.6 s  + 9.0 = 1739.6 s = 28:59.6
  at 160.0 wpm  60*4895/160.0 = 1835.6 s  + 9.0 = 1844.6 s = 30:44.6
  at 159.5 wpm  60*4895/159.5 = 1841.4 s  + 9.0 = 1850.4 s = 30:50.4
  -> inside runtime_seconds [1560, 1895] at BOTH edges
```

**尺の再確認。**設計中心は 4,700 語だったが、実際の初稿は **4,895 語**で入った。契約帯の内側であり、語数バンド [4400, 5000] の内側でもあるので、**設計は変えない**。ただし **§6 と §12.5 の秒数は 4,700 語時の設計目標であり、実尺では約 4% 後ろにずれる**（4,895 / 4,700 = 1.041）。AE ビートの位置も同じだけずれる——6:20→6:35 / 11:25→11:53 / 13:30→14:03 / 16:10→16:50 / 19:40→20:28 / 21:20→22:12 / 23:20→24:17。**これらはいずれも「受け取った ElevenLabs マスタのタイムラインで再導出する」値であって、確定値ではない。**字幕をロックする前にもう一度測る。

**カット予算（契約が満たせることを先に確かめた。EP66 はこれを後回しにして破綻した）**
```
total cuts        1560/3.7 = 421     1762.5/3.7 = 476     1895/3.7 = 512
stills <= 32%                134                  152                163
video cuts available     421-134=287        476-152=324        512-163=349
mandatory_stills 104   -> fits at every edge (104 <= 134)
distinct_video_assets 265 -> fits at every edge (265 <= 287)
```

### 機械フロアと、それを満たす手段

| ゲート | フロア | この映画での満たし方 |
|---|---|---|
| `animation_density` | near-still が尺の **10%以下**・単一ホールド **3.0秒以下** | `target_cut_sec` 3.7。**静止画は必ず depth または i2v で動かす**——Ken Burns のズーム／パンだけは「紙芝居」として却下される（オーナー判断）。**例外は A2-05 の「画が無い15秒」だけ**で、そこは黒であって静止画ではない |
| `motion_density` | **2.5 kinetic beats/分**以上・coverage 0.25以上・variety 3以上 | 図版ビート78本（§6）＋ AEキネティック7本（§12.5）＋ マスク切り上がりのタイポグラフィ引用16本 ＝ **101本 / 29.53分 = 3.42 beats/分** |
| `footage_diversity` | distinct ≥ 0.40・再利用 ≤ 4・汎用象徴 ≤ 2 | 265 / 324 = **0.818**。汎用象徴（天秤・砂時計・握手）は `forbidden_subjects` で**0**にしてある |
| `footage_utilization` | 80%以上 | **300〜330点だけを staging する。**12,040点の screened supply を全部 staging しない（FOOTAGE_PLAN §5） |
| cross-episode 被り | 他話が持つIDは0 | **9,780 ID が既に除外済み**（FOOTAGE_PLAN §1 フィルタ7）。**staging 前に `check_cross_episode_reuse.py --build` を回し直す** |

### 様式（この映画に固有）

- **距離が全編の視覚モチーフである。** H1（9インチ）を6回。**衝突を映さないことが様式であり、
  その様式に judicial な根拠がある**——裁判所自身が説明をやめた（PP-07）。
- **火は一度も画面に出ない。** 燃える車も、炎も、煙の中の人も。R7 レジスタは
  **熱と光の抽象**（作業灯、溶接の火花、炉の口）にだけ使い、**車と同じカットには絶対に置かない**。
- **法廷の内部は一度も映さない。**再現法廷は「この映画が嘘をつく唯一の場所」になる。
  裁判所は外観・石・扉・タイポグラフィだけ（`forbidden_subjects` に `gavel` と `scales`）。
- **読める文字は Remotion のタイポグラフィと MOTIONKIT 図版にしか存在しない。**
  生成プレートに一文字も焼かない。Grush/Saunby 報告書、exhibit 125、NHTSA の報告書、
  Elkhart の起訴状、当時の紙面——**どれも「本物に見える画像」を作らない**（⛔-15・invariant 11）。
  引用は**帰属付きのタイポグラフィカード**として出す。それは記録の言葉であり、記録の写真ではない。
- **車には一切の銘が無い。** バッジ、オーバル、車名スクリプト、グリルのエンブレム、
  ナンバープレート、ディーラー看板——**すべて禁止**。実車の Pinto を提示しない。
- **二つの時代を画で分ける。** 1968–1972 の工場と製図室（暖かいタングステン・機械・金属）と、
  1977–1981 の紙と石（冷たい昼光・活字・石・縦線）。17:40 のカットで観客が体で「移動した」と分かること。
- **人は必要である（§11）。** 手、背中、肩、遠景の人影、そして**顔**——ただし
  **この記録の中の誰かとして提示される顔は一つも無い**。

---

## 11. 人物 — 必須である

**オーナー判断（2026-07-04）：描かれた人物は必須であり歓迎される。禁止されているのは
実在の特定個人の肖像（likeness）だけである**（CLAUDE invariant 11）。EP60 は誰も映っていない映画を
出して、それが間違いだった。

- `people_plates_min` = **24**、`people_plates` = **R081–R104**（契約に列挙済み）。
- **顔は出してよい。** 出してはいけないのは、**この記録の中の誰かとして提示される顔**——
  Richard Grimshaw、Lilly Gray とその家族、Ulrich 姉妹と従姉、バンの運転者、
  そして Ford の従業員（Iacocca・MacDonald・Alexander・Kennedy・Copp・Grush・Saunby・Hromi・
  MacLean・Misch）。**判事・検事・弁護人も同じ**である。
- **意見と証言は署名付きのタイポグラフィとして画面に出る。**それが唯一の描き方である。
- **人物レーン（human-present lane）**の内訳は画像発注書
  `EP68_pinto_CODEX_BATCH_A.v001.md` §3 にあり、`[HSTYLE]` プロンプトレーンとして分離されている。

---

## 12. この映画が言ってはならないこと

契約の `forbidden_claims`（**23項目**）と台帳の ⛔ **全26項目**（v001 の20 ＋ §0.5 の6）がここに拘束する。
実務上とくに五つ：

- **「$11 で Pinto は直せた」と言わない。** $11 は**全産業の横転適合**の数字（DOC-08）。
  判決文の Pinto の数字は **$15.30**（CAR-06）。⛔-17。**この回で最も踏みやすい。**
- **「Ford は人命を200,000ドルと値付けした」と言わない。** ⛔-04。**そして逆に
  「200,000ドルは NHTSA が基準策定に使っていた数字だ」とも言わない。**⛔-23——
  Schwartz が自分でそれを撤回している（SW2-11）。言えるのは「NHTSA が**公表した**数字」までである。
- **死者数を裸で言わない。** ⛔-01・⛔-24。使えるのは **38 / 27 / 24** だけで、
  **「うち1名は衝撃による」**と**NHTSA 自身の FARS 注意書き**を同じ場所で言う。
- **$125,000,000 を Ford が払った額として単独で出さない。** ⛔-06。
  陪審の数字と減額後の数字は**必ず同じ文の中に**ある。
- **無罪を「技術的な抜け穴」と言わない。** ⛔-19。言えるのは、法律が1977年制定だったので
  設計は裁けなかったこと（SW2-15）、そのため社内文書が入らなかったこと、
  検察が資源で劣っていたと**検察自身が言った**こと（IN-15）。**結論は言わない。**

**帰属の規則。** Schwartz と Lee は**二次資料**である。彼らの評価を地の文で言わない——
「Schwartz はこう書いている」「1998年に Matthew Lee はこう書いた」と冠して読む。
CC-01〜CC-12・SW2-*・LE-* のすべてに適用される。**判決文と NHTSA 報告書と Grush/Saunby 報告書
だけが、帰属なしで地の文に入ってよい。**

## 12.5 AFTER EFFECTS キネティック文字 — **7ビート**

2026-08-04 の常設承認は「中盤の数字と転換に1〜2回」だが、オーナー指示（2026-08-11）は
**「AEはガッツリ使ってほしい。とにかく紙芝居をやめたい」**であり、
**この記録は論証が算術そのもの**である（§0-4）。だから7本にする。**約4.2分に1本**、
すべて ACT_1〜ACT_4 の中盤。**HOOK と ENDING には置かない**
（フックは声と実景で持たせる区間、ENDING は新事実ゼロの区間だから）。

実体は **`scripts/ae/jobs_ep68_pinto.json`**、書き出しは **`scripts/ae/render_beats.sh`**、
出来た VP9-alpha WebM を **`remotion/public/pinto/ae/<id>.webm`** に置き、
`pinto_film.json` にカットとして配置する。

| id | 画 | 秒 | 位置 | 乗る台本行 | 台帳 |
|---|---|---|---|---|---|
| `ep68_kin_1530` | **$15.30** ／ PER CAR. THE COURT'S PINTO FIGURE. | 2.4 | **A1-11 · ≈6:20** | 「十五ドル三十セントで、時速34から38マイルの追突に耐えるタンクになった、と裁判所は書いた」 | CAR-06 ✓ |
| `ep68_kin_jury_remittitur` | $125,000,000 THE JURY ／ $3,500,000 AFTER REMITTITUR ／ BOTH AFFIRMED ON APPEAL | 3.2 | **A2-12 · ≈11:25** | 「陪審は一億二千五百万ドルを認め、判事は三百五十万ドルまで返上させ、控訴審は両方を維持した」 | MN-01・MN-03・MN-05 ✓ |
| `ep68_kin_500_to_900` | 500 BURN DEATHS ／ "COULD BE AS HIGH AS 900" ／ NO SOURCE GIVEN IN THE ARTICLE | 3.2 | **A3-03 · ≈13:30** | 「控えめに見積もっても五百人、と記事は書いた。九百人に達する可能性がある」 | PM-02 ✓ |
| `ep68_kin_38_27_24` | 38 CASES ／ 27 FATALITIES ／ NHTSA, INVESTIGATION REPORT C7-38, MAY 1978 | 3.2 | **A3-11 · ≈16:10** | 「合計で、と役所は書いた。三十八件。二十七名。うち一名は衝撃による」 | NH2-05 ✓ |
| `ep68_kin_11_million` | 11,000,000 CARS ／ 1,500,000 LIGHT TRUCKS ／ THE WORD PINTO IS NOT IN THE TABLE | 3.2 | **A4-09 · ≈19:40** | 「販売台数——千百万台の乗用車、百五十万台の小型トラック」 | DOC-07・DOC-08 ✓ |
| `ep68_kin_200000` | **$200,000** ／ NHTSA'S PUBLISHED FIGURE, NOT FORD'S | 2.4 | **A4-13 · ≈21:20** | 「NHTSA は一件の死亡につき二十万ドルという値を算出している——と、その紙自身が書いている」 | DOC-10 ✓ |
| `ep68_kin_11_vs_1530` | $11 ROLLOVER, WHOLE INDUSTRY, 1973 ／ $15.30 REAR IMPACT, THE PINTO, 1972 ／ TWO DIFFERENT DOCUMENTS | 3.2 | **A4-17 · ≈23:20** | 「同じ額ではない。一度も同じだったことはない」 | DOC-08・CAR-06 ✓ |

**この7本が果たす仕事は装飾ではない。**
`ep68_kin_11_vs_1530` は ⛔-17 に対する**機構**であり、
`ep68_kin_jury_remittitur` は ⛔-06 に対する**機構**であり、
`ep68_kin_38_27_24` は ⛔-01/⛔-24 に対する**機構**である。
**数字を画面に出すことが、間違えないための仕掛けになっている。**

**書き出し前に必ず踏む二つの罠（実測済み・jobs ファイルにも書いてある）：**

1. **`scripts/ae/kinetic_beat.jsx` の32行目が `var W = 1080, H = 1920, FPS = 30;` を直書きしている。**
   これはショート（縦）の寸法である。**そのまま回すと縦のオーバーレイが出てきて、
   1920×1080 の本編に置くとピラーボックスになる。** jobs の各エントリには
   `"canvas": {"w":1920,"h":1080}` を持たせてあるので、**jsx にそれを読ませる1行の修正を
   `scripts/pd_edit.py` 経由で先に入れる。** 入れずに `render_beats.sh` を回さない。
2. **EP66 の jobs ファイルは先頭に `style:"note"` の `_meta` オブジェクトを持っている。**
   `kinetic_beat.jsx` は**配列の全要素にコンプを作る**ので、その要素は文字の無いコンプになり、
   ログに `FAILED` が出て `render_beats.sh` はレンダーを拒否する。
   **EP68 の jobs ファイルには note オブジェクトを置いていない。**由来は実ビートの
   `_section` / `_ledger` / `_line` / `_why` / `_note` フィールドに入れてあり、jsx はそれらを無視する。

## 12.6 字幕をどこで切るか

**息継ぎ単位で切る。画面の横幅では切らない。**

- 分割は文法単位（`scripts/polish_captions_srt.py` の `_smart_split`）。
  **前置詞・冠詞・接続詞で行を終わらせない。** `check_caption_breaks.py` は
  **1キュー3語以上**と**文中で切れたキューが5%以下**を要求する。
- 1キュー = **1息継ぎグループ**、最長 **6.8秒**、最短 1.0秒、**2行以内**、
  物理行 **42字以内**、**CPS 17以下**（spec v2 行4）。
- **リードは 0.60秒**（この話の宣言値。`filmconfig` の `captionLeadSeconds` が正典であり、
  house 既定の 0.25 ではない）。リードは**行き先であって加算値ではない**——
  `captions.final.v001.lead.json` が「既に入っている量」を持ち、差分だけを適用する。
- **引用行は絶対に文中で割らない。** この映画の字幕の約三分の一は判決文・NHTSA 報告書・
  Grush/Saunby 報告書の原文であり、
  ✓ *"In total, the NHTSA is aware of 38 cases / in which rear-end collisions"* のような切り方は
  意味を壊す。引用は**1キュー1文**を原則とし、6.8秒を超える引用は**朗読側で間を作って**2キューに分ける。
- **A2-05 の「画が無い15秒」には字幕を出す。**画が無いからこそ、判決文の一文が
  読める形で立っていなければならない。1キュー1文、リードは同じ0.60秒。
- 検査：`check_caption_breaks` ／ `caption_format` ／ `caption_narration_match`（**100%一致**）。

---

## 13. THE LIST — 欲しかったが、記録が持っていないもの

**この節がこの文書で最も価値のあるページである。**以下はいずれも**書かなかった。**

### 台本を止めるもの（着手前に閉じる／閉じた）

| # | 欲しかった事実 | なぜ必要か | 状態 | 取る形 |
|---|---|---|---|---|
| **1** | **NHTSA の1978年調査報告書（○-03）** | 映画の中心的な訂正数字がそこにある | **閉じた。**C7-38, May 1978, 18ページ画像、pp.2/3/4/10 をページで読了 | **NH2-05 を役所の言葉で読む。**注意書き（NH2-07）を同じ場所で言う |
| **2** | **Schwartz の未読44ページ（○-09）** | 反証が一人の著者の12ページに載っていた | **閉じた。**56/56 読了。うち4ページはこのパスが独立に再読 | SW2-01〜SW2-19 を新規行として §0.5 に持つ |
| **3** | **Lee & Ermann 1999（○-10）** | 反証が一人の著者に載っている | **部分的に閉じた。**本文は真に closed access。要旨のみ保持。**同一筆頭著者の1998年 open access 論文を取得しページで読了** | LEA-01 は**要旨の文しか使わない**。LE-01〜LE-03 は *Business and Economic History* 27:2 (1998) として、**Ermann の名を出さずに**帰属する |
| **4** | **Winamac の一次記録（○-06）** | 刑事編の全体がそこに載る | **部分的に閉じた。**カリフォルニア控訴裁判所の公表意見が **No. 5324・1978年9月13日提起・無罪**を書き、インディアナ州の法律雑誌が **No. 11-431・1980年3月13日・控訴なし**を三度書いている。**起訴状・ドケット・評決書・調書は依然として未取得** | ACT_5 を4分20秒に保ち、A5-05/A5-10 を**その二つの文書の言葉で**語り、E-02 で「何があって何が無いか」を一文で言う。§7 |

### 形を変えれば書けるもの

| # | 欲しかった事実 | 記録の状態 | 取る形 |
|---|---|---|---|
| 5 | 「Pinto Madness」の受賞歴 | Schwartz が Pulitzer と書いているが確認できない（⛔-21） | **言わない。**記者会見と Nader の同席だけ（SW2-06） |
| 6 | Ford の Pinto 生産・販売総数 | 一次では未取得。Schwartz は NHTSA 調査報告書を引いて 2,200,000台（1971–76）と書く | **必要なら「NHTSA の調査報告書を引いて Schwartz は220万台と書いている」と、そう名乗って出す。**Ford の数字としては出さない |
| 7 | Ford が実際にいくら払ったか、いつ | どの取得文書にも無い（MN-10） | **言わない。**⛔-06 と ⛔-18 |
| 8 | リコールの完了率 | Schwartz が NHTSA 職員への**電話取材**として53%と書く（SW2-07） | 「NHTSA の職員が語った数字として」と冠して出す。**文書ではないと言う** |
| 9 | 追跡版 Grush 報告書（横転ではなく追突・側突） | Schwartz の脚注だけ。**"copy on file with author"**、公開されていない（○-11・DOC-15） | **存在を一文で言い、取得できていないと言う。**中身の数字は使わない |
| 10 | 1977年モデルの設計変更の中身 | Schwartz の一行（プラスチック盾）とリコール記録だけ | リコール記録の言葉（RC-04）だけを使う |
| 11 | *Grimshaw* の公判調書 | 未取得。Schwartz が RG/PG のページ番号で引く（○-02） | **取得文書の中に載っている引用しか使わない。**調書の直接引用はゼロ |
| 12 | 60 Minutes の放送内容（Mike Wallace / Herbert Misch） | Schwartz が transcript を引くが、transcript 自体は未取得 | **使わない。**Ford の当時の立場は、取得済みの AP 記事（IN-07）で言える |
| 13 | Richard Grimshaw のその後 | **意図的に閉じてある**（○-07） | 調べない。触れない。⛔-08 |
| 14 | 事故車の写真（Elkhart Public Library） | **取得したが隔離**（⛔-25） | 使わない。存在も画面で言わない |
| 15 | 「criminal recklessness の訴因が公判前に取り下げられた」「予審の判事は Donald Jones だった」 | **このパスが読んだどの文書にも無い。**下請けエージェントの要約として届いただけである | **使わない。**⛔-26。次のセッションで一次に当たる価値のある手がかりとしてだけ残す |
| 16 | Pepperdine L. Rev. 8:367 と Notre Dame の1979年ノート | **PDFは取得したが、このパスは読んでいない** | **読むまで一語も使わない。**IN2-01 がその Pepperdine ノートを引いているという事実だけが使える |

---

## 14. HUMAN MUST CONFIRM — ゲートが測らない8項目

`scripts/check_design_doc.py` は最後に「**機械には判定できないオーナー基準8件**」を印字する。
それらは**チェックとして偽装されていない**——だから設計側で引き受ける。以下は、その8件それぞれに
対して**この設計が具体的に何をしているか**であり、「配慮しました」ではない。

| # | ゲートの問い | この設計の答え（場所） | **人が見て決めること** |
|---|---|---|---|
| 1 | フックは結末を伏せているか | PACKAGING §3 末尾に「**この22.5秒に意図的に無いもの**」の列挙——Pinto / メモ / 衝突 / 陪審 / 金額 / リコール / インディアナ / 無罪。0:22 で観客が知っているのは「表が政府に送られた」だけ | **22.5秒を再生して、まだ問いが立っているか。**立っていなければ v002 |
| 2 | AI臭くないか | §5 の声の設計＋script の Register 節。**禁止語彙を挙げる代わりに構文で縛った**——形容詞は記録が持つものだけ、感情命令ゼロ、三連続の並列を各幕1回まで、"delve/moreover/it is worth noting" 型を全面排除。**引用が全体の約三分の一**あり、その部分は書き手の文体が入らない | **声に出して読む。**息が続かない文、書き言葉に聞こえる文を潰す |
| 3 | 画がナレの意味と一致しているか | §3.5 の差し替え表が**禁止画すべてに名前の付いた代替**を与えている。発注書 §8：**ビートを持たないプレートは発注しない** | **コンタクトシートを台本と並べて1周。**汎用素材の流し込みが1カットでもあれば差し戻し |
| 4 | 素材はラベルどおりのものか | FOOTAGE_PLAN §4 の各 register に**実際のタイトル例3件**を出してある（`crash` は波、`court` は求愛ダンス、`arch` は建築）。`footage_review_required: true` | **ラベル付きコンタクトシートを人が開く。**この回はとくに R6/R7/R12 を先に見る |
| 5 | 「動いている」と感じるか | §10 のモーション予算。**静止画は必ず depth か i2v で動かす**（Ken Burns だけは却下）。図版78＋AE 7＋タイポ16 = 3.42 beats/分 | **初回レンダーの 4:00 / 11:00 / 18:00 / 26:00 の4点を各30秒見る。**「止まっている」と感じたら数値が緑でも差し戻し |
| 6 | サムネは押したくなるか／タイトルは誘うか | PACKAGING §1（5案・文字数実測）と §2（ink 実測 214–245px・Anton 経由） | **3案を並べて、スマホサイズで見る。**押したくならなければ帯の中で作り直す |
| 7 | 台帳の事実は本当か | 着手前に `verify_quotes.v001.py` → **118/118 緑**。さらに §0.5 の新規行のうち**10ページ（NHTSA 表紙・p.2・p.3・p.4・p.10、Schwartz 1024・1033・1066・1067、Lee 399）をこのパスが独立にページ画像で再読**し、全部一致した。加えて **IN2-01 の脚注と IN2-02 の3箇所を、取得ファイルに対する完全一致検索でこのパスが自分で位置づけた**（下請けの要約を信じていない） | **一次資料に当たるのは研究であって文字列検索ではない。**公開前に法務目線でもう一度。とくに **Ford が実在の生きた企業である**こと |
| 8 | OP/ED はチャンネルのテイストか | PACKAGING §4・§7 に配置と数値。**部品は正典 `Bookends.tsx` で fork しない** | **配置は測れる。テイストは測れない。**22.9s と 29:22 前後を実際に見る |

---

*Built 2026-08-11. 台帳の検証器は着手前に緑（118/118）。二本の出典ゲート（NHTSA C7-38、Schwartz 44
ページ）をこのパスで閉じ、三本目（Lee & Ermann）を部分的に閉じた。四本目（Winamac の一次記録）は
開いたままであり、§7 がその欠落を隠さずに設計へ組み込んである。素材は623クエリを2ラウンド実測
（15,335 union ／ 12,040 screened ／ 265 required）。
**この文書に書かれていないものは、この映画に入らない。**（PD_CANON：文書に無いものは使われない）*
