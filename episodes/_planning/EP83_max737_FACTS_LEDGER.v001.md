# EP83 `max737` — FACTS LEDGER v001

**Boeing 737 MAX — Lion Air Flight 610 (29 October 2018) and Ethiopian Airlines Flight 302
(10 March 2019).** Compiled 2026-08-25 from primary records. Every row carries the document it
came from and, for the court filings, the page of the filed PDF.

> ## ⛔ R3 — WHAT THIS FILM MAY AND MAY NOT SAY
>
> 1. **The criminal case is over and it ended in a DISMISSAL, not a conviction.** The information
>    charging Boeing was **dismissed on 6 November 2025** (MX-501). The film may never say Boeing
>    was convicted, and may never leave a viewer believing a court found the company guilty.
> 2. **Boeing DID admit the conduct in the Statement of Facts** it signed in 2021 (MX-201…MX-215).
>    That is an admission by agreement, not a verdict. The correct verb throughout is
>    *Boeing admitted*, sourced to the agreement — never *the court found*.
> 3. **The only individual ever tried was ACQUITTED.** Mark Forkner was found **not guilty on all
>    four counts on 23 March 2022** (MX-405). He is not named in this film, is not the villain of
>    it, and no sentence may imply he lied. The DPA's own "Boeing Employee-1 / Employee-2" naming
>    is what this film uses.
> 4. **346 people died.** The number is narrated once, plainly. It does not go in the title
>    (measured: `died/killed/deaths` in a title = 0.06× impressions) and it is never used as a
>    dramatic beat.
> 5. **No real-person likeness.** Not the crash victims, not the families, not the pilots, not any
>    named executive, engineer or regulator. Person-shaped figures are fine; a recognisable real
>    person is a ship blocker (`real_person_likeness`).
> 6. **`⛔` rows below may not be narrated at all** until the flagged source is read line by line.

## Sources

| id | document | date | how it was read |
|---|---|---|---|
| S1 | **Deferred Prosecution Agreement**, *United States v. The Boeing Company*, N.D. Tex. 4:21-cr-00005-O, ECF No. 4 (58 pp, incl. **Attachment A — Statement of Facts**) | 2021-01-07 | **READ IN FULL.** CourtListener RECAP doc 156534429, plain text pulled via the v4 API |
| S2 | **Felony Information**, same case, ECF No. 1 (2 pp) | 2021-01-07 | **READ.** RECAP doc 156534427 |
| S3 | **Memorandum Opinion and Order** granting the Rule 48(a) dismissal, same case, ECF No. 358 (10 pp) | 2025-11-06 | **READ IN FULL.** RECAP doc 457937473 |
| S4 | **Fifth Circuit opinion**, *Naoise Ryan v. United States*, Nos. 25-11253 c/w 25-11254 (mandamus denied) | 2026-03-31 | **READ IN FULL.** CourtListener opinion 11297378 |
| S5 | **Fifth Circuit REVISED opinion + denial of rehearing en banc**, same numbers | 2026-05-22 | **READ IN FULL.** CourtListener opinion 11330977 |
| S6 | House Committee on Transportation & Infrastructure, *The Design, Development & Certification of the Boeing 737 MAX* (final report, 246 pp) | 2020-09 | **READ BY PAGE** (text-extracted, page numbers verified against footers) |
| S7 | DOT Office of Inspector General **AV2023025**, *FAA Has Completed 737 MAX Return to Service Efforts…* | 2023-04-26 | **READ BY PAGE** |
| S8 | KNKT (Indonesia NTSC) Final Report **KNKT.18.10.35.04**, Lion Air JT610 | 2019-10 | **READ BY PAGE** (mirror cited inside S6) |
| S9 | EAIB (Ethiopia) Final Report, ET302 | 2022-12 | **READ BY PAGE** (BEA-hosted copy) |
| S10 | NTSB, *US Comments on Draft Aircraft Accident Investigation Report* (ET302) | 2022-03 | **READ** — ntsb.gov |
| S11 | NTSB, *Response to EAIB final report* | 2023-01-13 | **READ** — ntsb.gov |

**justice.gov returns HTTP 403 to the ordinary fetcher and its Akamai interstitial defeats curl
with a browser user-agent as well.** Everything DOJ said that this film relies on was therefore
taken from the **court's own docket** instead, which is the better source anyway: S1 and S3 are
the filed instruments, not a press release about them.

---

## A. What the airplane did — the two accidents (S1 Statement of Facts)

| id | fact | source |
|---|---|---|
| MX-001 | **On 29 October 2018, Lion Air Flight 610, a Boeing 737 MAX, crashed shortly after takeoff into the Java Sea near Indonesia. All 189 passengers and crew on board died.** | S1 ¶48 (A-14) |
| MX-002 | **On 10 March 2019, Ethiopian Airlines Flight 302, a Boeing 737 MAX, crashed shortly after takeoff near Ejere, Ethiopia. All 157 passengers and crew on board died.** | S1 ¶53 (A-15) |
| MX-003 | **On 13 March 2019 the 737 MAX was officially grounded in the United States**, indefinitely halting further flights of the airplane by any U.S.-based airline. | S1 ¶54 (A-15) |
| MX-004 | Following each crash, the FAA AEG learned that **MCAS activated during the flight and may have played a role in the crash**. | S1 ¶49, ¶53 |
| MX-005 | 189 + 157 = **346**. Arithmetic on MX-001 and MX-002; no source states the sum, so the film either says the two numbers or says 346 as a sum of them. | derived from MX-001, MX-002 |

## B. What MCAS was, and what the regulator was told (S1 Statement of Facts)

| id | fact | source |
|---|---|---|
| MX-101 | Before any U.S. airline could fly a new airplane, the FAA's **Aircraft Evaluation Group (AEG)** had to determine what "differences training" pilots needed, on a scale from **Level A (least intensive) to Level E (most)**. **Level B** generally meant computer-based training; **Level D** generally meant **full-flight simulator training**. | S1 ¶6, ¶9 |
| MX-102 | Boeing's **737 MAX Flight Technical Team** was principally responsible for identifying and providing to the FAA AEG **all information relevant to the AEG's publication of the 737 MAX FSB Report**. | S1 ¶11 |
| MX-103 | The FAA AEG's provisional **Level B** determination rested in part on its understanding that **MCAS could only activate during a high-speed, wind-up turn**. | S1 ¶28 |
| MX-104 | Boeing Employee-1 acknowledged in an email of **about 16 August 2016** that the Level B determination was **"provisional approval […] assuming no significant systems changes to the airplane."** | S1 ¶29 [VERBATIM] |
| MX-105 | In an email of **about 10 November 2016**, Boeing Employee-1 wrote: **"[o]ne of the Program Directives we were given was to not create any differences […]. This is what we sold to the regulators who have already granted us the Level B differences determination. To go back to them now, and tell them there is in fact a difference […] would be a huge threat to that differences training determination."** | S1 ¶30 [VERBATIM] |
| MX-106 | **MCAS's operational scope was changed**: when the airplane registered a high angle of attack, the change **expanded the speed range within which MCAS could activate from approximately Mach 0.6–0.8 to approximately Mach 0.2–0.8** — that is, from only high-speed flight to nearly the entire speed range of the 737 MAX. | S1 (SoF, MCAS scope) |
| MX-107 | **On or about 15 November 2016**, during a **simulator** test flight, Boeing Employee-1 experienced MCAS operating at lower speed and recognised it was **different from what Boeing had briefed and described to the FAA AEG**. | S1 ¶31 |
| MX-108 | The same day, Boeing Employee-1 and Boeing Employee-2 discussed MCAS in an internal chat: **"Oh shocker alerT! [sic] / MCAS is now active down to [Mach] .2 / It's running rampant in the sim on me / at least that's what [a Boeing simulator engineer] thinks is happening" — "Oh great, that means we have to update the speed trim description in vol 2" — "so I basically lied to the regulators (unknowingly)" — "it wasn't a lie, no one told us that was the case."** | S1 ¶32 [VERBATIM — the whole exchange, quoted in the agreement] |
| MX-109 | At that point both employees **recognised the FAA AEG was under the misimpression** that MCAS operated only in a high-speed wind-up turn and could not operate at lower Mach speeds. | S1 ¶33 |
| MX-110 | They **deceived the FAA AEG into believing** that the basis on which the AEG had initially agreed to **remove any information about MCAS from the 737 MAX FSB Report** — that MCAS could only activate in the limited scope of a high-speed wind-up turn — still held. | S1 ¶40 [VERBATIM phrase "deceived the FAA AEG into believing"] |
| MX-111 | **Pilots flying the 737 MAX for Boeing's airline customers were not provided any information about MCAS in their airplane manuals and pilot-training materials.** | S1 (SoF) [VERBATIM] |
| MX-112 | After the Lion Air crash, Boeing Employee-2 told an FAA AEG employee that he had been **previously unaware of MCAS's expanded operational scope**, and **otherwise misled** that employee about his own prior knowledge. | S1 ¶50 |
| MX-113 | Boeing Employee-2 caused Boeing to present to the FAA AEG a presentation representing that Boeing and the AEG had **"discussed and agreed on [the] removal of MCAS"** from the FSB Report. The agreement records this as **misleading**, because the "shocker alert" chat was not disclosed. | S1 ¶51 [VERBATIM of the quoted phrase] |
| MX-114 | **THE COMPANY'S OWN SENTENCE ABOUT ITS OWN KNOWLEDGE.** **"From at least in and around November 2016 through at least in and around December 2018, in the Northern District of Texas and elsewhere, Boeing, through Boeing Employee-1 and Boeing Employee-2, knowingly, and with intent to defraud, conspired to defraud the FAA AEG."** This is the admission that supports the word *knew* — and it is an admission **by agreement**, not a verdict (see R3 note 1). | S1 ¶16 [VERBATIM] |
| MX-115 | **"At all times during the conspiracy, Boeing Employee-1 and Boeing Employee-2 were acting within the scope of their employment and with the intention, at least in part, to benefit Boeing."** | S1 ¶17 [VERBATIM] |

## C. The 2021 agreement — what Boeing paid and what it admitted (S1, S2)

| id | fact | source |
|---|---|---|
| MX-201 | Boeing was charged by **information** with **one count** arising from the conduct in the Statement of Facts, and **waived indictment**. | S2; S1 ¶1 |
| MX-202 | **Total U.S. Criminal Monetary Amount: $2,513,600,000**, comprising: **a criminal monetary penalty of $243,600,000**; **$1,770,000,000 in compensation to Boeing's airline customers**; and **$500,000,000 in additional compensation to the heirs, relatives and/or legal beneficiaries of the crash victims of Lion Air 610 and Ethiopian 302**. | S1 ¶7 [VERBATIM figures] |
| MX-203 | The **base fine of $243,600,000 represents Boeing's cost-savings** — Boeing's own assessment of the cost of implementing **full-flight simulator training** for the 737 MAX. | S1 (Guidelines calculation) [VERBATIM parenthetical] |
| MX-204 | The Fraud Section described the offence conduct as **"two of the Company's 737 MAX Flight Technical Pilots deceiving the Federal Aviation Administration's Aircraft Evaluation Group ('FAA AEG') about an important aircraft part called the Maneuvering Characteristics Augmentation System ('MCAS')…"** | S1 ¶4(a) [VERBATIM] |
| MX-205 | The resolution was a **Deferred Prosecution Agreement**, dated **7 January 2021**. | S1; S3 p.1 |

## D. What happened to the case (S3, S4, S5) — THE ENDING

| id | fact | source |
|---|---|---|
| MX-301 | **On 14 May 2024 the Government notified the Court that Boeing had BREACHED the DPA** — for **"failing to design, implement, and enforce a compliance and ethics program to prevent and detect violations of U.S. fraud laws throughout its operations."** | S3 p.2 [VERBATIM] |
| MX-302 | In **July 2024** the parties submitted a **plea agreement requiring Boeing to plead guilty** and serve a term of probation. | S3 p.2 |
| MX-303 | **On 5 December 2024 the Court REJECTED that plea agreement.** | S3 p.2 |
| MX-304 | **On 29 May 2025 the Government moved under Rule 48(a) to dismiss the information** (ECF No. 312), having entered a **non-prosecution agreement (NPA)** with Boeing. | S3 p.1; S4 |
| MX-305 | The NPA's condition: **Boeing pays $1.1 billion in fines and undertakes remedial actions.** | S4 [VERBATIM figure] |
| MX-306 | The Government stated the NPA **"secures meaningful accountability, delivers substantial and immediate public benefits, and brings finality to a difficult and complex case whose outcome would otherwise be uncertain."** | S3 p.4 [VERBATIM] |
| MX-307 | The families objected that the NPA is **unenforceable because the statute of limitations has run — meaning the Government could not re-file charges even if Boeing breached** — that it **exempts Boeing from any independent monitoring** of its compliance and safety efforts, and that it **does not secure the maximum possible fine**. | S3 pp.3–4 [the objections, as the court records them] |
| MX-308 | **On 6 November 2025 the Court GRANTED the motion and dismissed the case.** | S3 p.10 |
| MX-309 | **On 31 March 2026 the Fifth Circuit DENIED the families' petitions for writ of mandamus**, holding it **"lack[s] jurisdiction under the CVRA to perform a substantive review of the district court's Rule 48 dismissal."** | S4 [VERBATIM] |
| MX-310 | The Fifth Circuit also held the **district court correctly concluded the Department did not violate the CVRA** by failing to confer with the families or by misleading them about the NPA. | S4 |
| MX-311 | The court **declined to read into the CVRA "an unlimited right for victims to appeal the dismissal of criminal prosecutions"**, as inconsistent with the proposition that **nonparties lack a "judicially cognizable interest" in the prosecution of another** (citing *Linda R.S.*, 410 U.S. at 619). | S4 [VERBATIM] |
| MX-312 | **On 22 May 2026 rehearing en banc was DENIED**; no judge requested a poll. A revised panel opinion issued the same day. | S5 [VERBATIM] |
| MX-313 | In February 2023 the district court had found that **the Department violated the CVRA by denying the families' right to confer before agreeing with Boeing**, but **not in bad faith**, and denied the motion to set aside the DPA. | S4 (procedural history) |

## E. The individual prosecution — ACQUITTED (R3 CRITICAL)

| id | fact | source |
|---|---|---|
| MX-405 | **A federal jury in Fort Worth acquitted the former 737 MAX Chief Technical Pilot on all four counts on 23 March 2022, after deliberating less than two hours.** No individual has ever been convicted in connection with these crashes. | ⛔S-news — MUST be re-confirmed against the docket (N.D. Tex. 4:21-cr-00268) before narration. The fact of acquittal is not in dispute; the film needs a primary cite for it. |

## F. The five months between the two crashes — CONFIRMED (S6, S7)

**This is the spine of the film's second half. Every row here was read by page on 2026-08-25.**

| id | fact | source |
|---|---|---|
| MX-601 | The FAA ran a **Transport Airplane Risk Assessment Methodology** analysis (R-TARA) **prepared 3 December 2018**, reviewed by the Seattle ACO's Corrective Action Review Board on **11 December 2018**. | S6 pp.209–210 |
| MX-602 | **"the results of the TARAM analysis indicated that even with the FAA's Emergency AD, but without a fix to MCAS, there could be more than 15 fatal 737 MAX crashes over the estimated 30-year lifetime of the fleet, then estimated to be 4,800 aircraft, resulting in over 2,900 deaths."** | S6 p.210 [VERBATIM] |
| MX-603 | **"Statistically this meant that the FAA was predicting there would be one fatal 737 MAX accident every two years for the next 30 years."** | S6 p.210 [VERBATIM] |
| MX-604 | The analysis assumed only **1 in 100 pilots** would fail to react properly — which the Committee calls **"a gross over estimation."** | S6 p.210 [VERBATIM of the quoted phrase] |
| MX-605 | **"Despite the TARAM analysis, the FAA permitted the 737 MAX aircraft to continue flying."** | S6 p.211 [VERBATIM] |
| MX-606 | **"In those five months, Boeing delivered nearly 150 more aircraft to its customers, increasing the global 737 MAX fleet to 387 aircraft."** | S6 p.211 [VERBATIM] |
| MX-607 | The day after Boeing's bulletin, the **FAA issued Emergency Airworthiness Directive 2018-23-51 (7 November 2018) which, like Boeing's bulletin, did not mention MCAS.** | S6 p.92 n.; S7 p.9 [VERBATIM "did not mention MCAS by name"] |
| MX-608 | FAA officials stated that at the time of the emergency AD **"they were unaware of the full details of MCAS."** | S7 p.9 [VERBATIM] |
| MX-609 | ⚠️ **THE COMPLICATION THE FILM MUST CARRY.** The OIG records that even without the AD, the analysis **"still would not have recommended grounding the aircraft because the control program individual risk of 2.68 fatalities per 1 million flight hours remained below the TARAM guideline of 1 fatality per 100,000 flight hours."** The number that predicted 15 crashes sat inside a rule that said: not enough to ground. | S7 p.9 [VERBATIM] |
| MX-610 | The OIG's own framing of the numbers: **"These should not be viewed as predictive values."** The OIG does **not** use the House's 2,900-deaths figure. | S7 p.8 n.24 [VERBATIM] |
| MX-611 | OIG's uncorrected-fleet figure: **"the uncorrected fleet risk, with the emergency AD in place, still showed a projection of 15 weighted events over the 35-year life of the fleet if the software fix was not implemented."** (House says 30-year life / 4,800 aircraft; OIG says 35-year life. **Both are in the ledger; the film uses one and says whose it is.**) | S7 p.10 [VERBATIM] |
| MX-612 | **Under a contract signed in December 2011 with Southwest Airlines, the launch customer, Boeing was financially obligated to discount each MAX by at least $1 million if the FAA required simulator training** for pilots transitioning from the NG to the MAX. | S6 p.24 [VERBATIM] |
| MX-613 | **"if Boeing failed to obtain Level B (non-simulator) training requirements or less from the FAA it would have owed Southwest between $200 to nearly $400 million."** | S6 p.24 [VERBATIM] |
| MX-614 | **"Boeing permitted MCAS—software designed to automatically push the airplane's nose down in certain conditions—to activate on input from a single angle of attack (AOA) sensor."** In 2015 a Boeing Authorized Representative had asked whether MCAS was **"vulnerable to single AOA sensor failures…."** It shipped that way. | S6 pp.13, 20 [VERBATIM] |
| MX-615 | **"As originally designed, MCAS was only capable of moving the horizontal stabilizer a maximum of 0.6 degrees."** In **March 2016** Boeing redesigned it to activate at lower speeds and to move the stabiliser **a maximum of 2.5 degrees**. | S6 p.103 [VERBATIM] |
| MX-616 | Hours after the redesign approval, Boeing sought and the FAA approved **removal of references to MCAS from the Flight Crew Operations Manual** — and **"the FAA officials who authorized this request remained unaware of the redesign of MCAS until after the crash of the Lion Air flight."** | S6 p.20 [VERBATIM] |
| MX-617 | The Committee's **five central themes**, verbatim: **1) Production Pressures. 2) Faulty Design and Performance Assumptions. 3) Culture of Concealment. 4) Conflicted Representation. 5) Boeing's Influence Over the FAA's Oversight Structure.** | S6 pp.12–14 [VERBATIM] |
| MX-618 | **"Multiple career FAA officials have documented examples where FAA management overruled a determination of the FAA's own technical experts at the behest of Boeing."** | S6 p.14 [VERBATIM] |
| MX-619 | Delegation: in **2013 the FAA delegated 28 of 87 tasks** to Boeing; by **November 2016 — four months before certification — 79 of 91 activities.** DOT OIG data: in 2018 four U.S. manufacturers **"approved about 94 percent of the certification activities for their own aircraft."** | S6 p.60 and n.355 [VERBATIM] |
| MX-620 | **Grounding, 13 March 2019** — the Acting Administrator used 49 U.S.C. §§40113(a), 46105(c); **"FAA's first grounding of a transport airplane fleet since the Agency grounded the Boeing 787 Dreamliner in 2013."** | S7 pp.11–12 [VERBATIM] |
| MX-621 | **"On November 18, 2020, FAA rescinded the grounding order and issued a final airworthiness directive, thus allowing the 737 MAX to return to service."** | S7 p.26 [VERBATIM] |
| MX-622 | **346 dead** — and the report adds one more: **"346 people killed in two separate crashes within five months of each other, as well as one rescue diver who died attempting to recover bodies from the Lion Air crash in the Java Sea."** | S6 p.2 [VERBATIM] |

## G. Lion Air 610 — the flight, and the flight before it (S8, KNKT report KNKT.18.10.35.04)

| id | fact | source |
|---|---|---|
| MX-701 | KNKT states **contributing factors, not a single probable cause** — nine of them. Among them: assumptions about flight-crew response **"turned out to be incorrect"**; **"MCAS was designed to rely on a single AOA sensor, making it vulnerable to erroneous input from that sensor"**; the **AOA DISAGREE alert was not correctly enabled**; **"The replacement AOA sensor that was installed on the accident aircraft had been mis-calibrated during an earlier repair. This mis-calibration was not detected during the repair."**; missing log documentation; and that **"the multiple alerts, repetitive MCAS activations, and distractions related to numerous ATC communications were not able to be effectively managed."** | S8 p.215 §3.2 [VERBATIM] |
| MX-702 | The recorder shows a **difference between the left and right AOA sensors of about 21°, constant, "which continued until the end of recording."** The same ~21° bias was present on the previous flight. | S8 p.19 [VERBATIM] |
| MX-703 | **At rotation the left stick shaker activated "which continued for most of the flight."** Airspeed disagree 9 seconds later; altitude disagree at 23:21:12. | S8 pp.19–20 [VERBATIM] |
| MX-704 | **At 23:22:33, flaps fully retracted, "the automatic AND trim was active for about 10 seconds,"** moving the stabiliser from 6.1 to 3.8 units — the first MCAS activation. Repeated nose-down activations followed, each countered by pilot nose-up trim. | S8 p.21 [VERBATIM] |
| MX-705 | Near the end the first officer was flying and applying **up to 93–103 lb of column force**. **"At 23:31:53 UTC, MCAS activated until the DFDR stopped recording at 23:31:54 UTC and the CVR stopped recording 1 second later."** Airborne about **11 minutes**. | S8 pp.24–27 [VERBATIM] |
| MX-706 | **THE FLIGHT BEFORE.** On the previous flight (Denpasar–Jakarta, 28 October 2018), **"a dead heading crew, first officer of Lion Air Group, rated with Boeing 737-8 (MAX) was seated in the cockpit jump seat."** The stick shaker **"remained active throughout the flight for about 96 minutes until landing."** | S8 p.166 [VERBATIM] |
| MX-707 | **"the dead heading pilot informed to the Captain that the aircraft was diving down."** After three automatic nose-down trim events and the FO reporting the column too heavy, the Captain **"considered the automatic trim inputs as a runaway stabilizer," performed the memory items "and positioned the STAB TRIM CUTOUT switches in the Cut-Out position."** The automatic trim stopped at 14:28:08 UTC. | S8 pp.166–167 [VERBATIM] |
| MX-708 | ⚠️ **THE CORRECTION THE FILM MUST MAKE.** The popular version — *an off-duty pilot in the jump seat told them to flip the switches and saved the plane* — **is not what the report says.** KNKT attributes the cutout decision **to the Captain**. The jump-seat pilot told the Captain the aircraft was diving, asked whether returning to the departure airport would be appropriate, and was asked to monitor the flight path, listen to ATC, check that no checklist item was skipped and calculate Vref/N1. **The film may not say he saved the aeroplane.** | S8 pp.166–176 [VERBATIM of each cited act] |
| MX-709 | KNKT records the previous crew **"was able to successfully land the accident aircraft while experiencing the same conditions as the accident flight."** Same airframe, same fault, different outcome. | S8 p.174 [VERBATIM] |

## H. Ethiopian 302 — and the fight over its report (S9 + NTSB comments)

| id | fact | source |
|---|---|---|
| MX-801 | EAIB probable cause: **"Repetitive and uncommanded airplane-nose-down inputs from the MCAS due to erroneous AOA input, and its unrecoverable activation system which made the airplane dive with the rate of -33,000 ft/min close to the ground was the most probable cause of the accident."** First contributing factor: **"The MCAS design relied on a single AOA sensor, making it vulnerable to erroneous input from the sensor."** | S9 p.255 §3.2 [VERBATIM] |
| MX-802 | Liftoff **05:38:34**; the erroneous left-AOA deviation began **10 seconds later**; recorders stopped about **05:43:44**; **"At 05:44 The Airplane impacted terrain 28 NM South East of Addis Ababa near Ejere."** **About six minutes.** All 157 aboard died. | S9 pp.18, 21, 34 [VERBATIM of the impact line] |
| MX-803 | **THE CREW DID THE PROCEDURE.** **"The F/O then twice suggested 'stab trim cut out?' The Captain replied 'yes yes do it'."** The switches went to cutout about **05:40:38**; a third MCAS command at 05:40:43 produced **"no corresponding motion of the stabilizer."** | S9 pp.26–27 [VERBATIM] |
| MX-804 | Unable to move the stabiliser by hand against the aerodynamic load, the crew **restored the switches to normal at about 05:43:11** — and about **five seconds after the last manual trim-up input, a final automatic nose-down activation** drove the dive. | S9 pp.30, 18 |
| MX-805 | ⚠️ **THE RECORD CONTRADICTS ITSELF AND THE FILM SHOWS IT.** The NTSB's comments on the draft: **"We agree that the uncommanded nose-down inputs from the airplane's MCAS system should be part of the probable cause… However, the draft probable cause indicates that the MCAS alone caused the airplane to be 'unrecoverable,' and we believe that the probable cause also needs to acknowledge that appropriate crew management of the event, per the procedures that existed at the time, would have allowed the crew to recover the airplane…"** NTSB proposed adding **"the flight crew's inadequate use of manual electric trim and management of thrust."** | NTSB, *US Comments on Draft Aircraft Accident Investigation Report* [VERBATIM] |
| MX-806 | **The NTSB's comments were not appended to the final report.** NTSB, 13 January 2023: its comments **"were not appended to the final report, as requested by the NTSB and provided by section 6.3 of Annex 13."** NTSB also rejects the EAIB's electrical theory: the erroneous AOA signals were **"caused by the separation of the AOA sensor vane due to impact with a foreign object, which was most likely a bird."** | NTSB, *Response to EAIB final report*, pp.2, 5 [VERBATIM] |

## I. Traps — numbers and names that will be checked by a viewer

| id | trap | rule |
|---|---|---|
| MX-901 | **The first crash has two dates.** The DPA and KNKT say **29 October 2018** (local time in Indonesia; departure 05:45 LT). The House report says **28 October 2018** (UTC, 22:45 on the 28th). **Both are correct in their own frame.** Say "29 October 2018" with the DPA and KNKT, or avoid the bare date; never present the two as a discrepancy. | derived: S1 ¶48, S8 p.19, S6 p.2 |
| MX-902 | **"15 crashes" belongs to a specific frame.** House: >15 fatal crashes / 30-year life / 4,800 aircraft / >2,900 deaths (MX-602). OIG: 15 weighted events / 35-year life (MX-611), and OIG says the figures **"should not be viewed as predictive values"** (MX-610). Attribute whichever is used. | S6 p.210, S7 pp.8,10 |
| MX-903 | **Do not say "Boeing was convicted."** The case ended in **dismissal** (MX-308) after an admission by agreement (MX-204). | S3 |
| MX-904 | **Do not say the jump-seat pilot saved the aeroplane** (MX-708). | S8 |
| MX-905 | **Do not name the acquitted pilot** (MX-405). The film uses the agreement's own "Boeing Employee-1 / Employee-2". | S1 |

## Open items

1. **MX-405 needs a primary cite** — the judgment of acquittal on docket N.D. Tex. 4:21-cr-00268.
   The fact is not in dispute; the film needs the document, not a news report, before narration.
2. **BEA's comments on the ET302 report** are referenced but not independently read. Any line about
   BEA must wait for the document itself.
3. **The record closes 22 May 2026** (MX-312). Before publication, re-check the docket and the
   Fifth Circuit: this ledger's ending is a court's, and a later filing would change it.
4. S6 and S7 were read by page for sections F–H; **S8 and S9 were read by an agent** working from
   the mirrors cited above, with page numbers recorded per row. Spot-check the load-bearing
   verbatim rows (MX-602, MX-605, MX-612, MX-708, MX-801, MX-805) against the PDFs before the
   script is locked.
