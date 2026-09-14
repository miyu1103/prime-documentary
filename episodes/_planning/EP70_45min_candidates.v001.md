# The 45-minute slot — eight candidates, measured

**Written 2026-08-12. Research, measurement and writing only: no render, build, staging or GPU work was
run, per the standing instruction that renders occupy the machine.**

EP70 Oroville has been honestly measured out at ~83 and about thirty minutes of material, and the owner
has decided it is made at thirty. This file answers the separate question: **what goes in the
45-minute slot.**

Everything below is measured, not asserted:

| what | how it was measured | where |
|---|---|---|
| the score | `py -3.11 scripts/score_premise.py --os v002 --score <file> --emit` | `episodes/_planning/premises_45min/*.json` + `*.scored.json` |
| demand and saturation | `py -3.11 scripts/topic_demand_probe.py` (YouTube Data API, 16 queries) | `episodes/_planning/measurements/TOPIC_DEMAND_PROBE_EP70_45MIN.v001.json` |
| producibility | regex sweep of the archive ledger, EP68 method | reproduced in §10 |
| protagonists | CourtListener v4 API and direct retrieval, by this agent | quoted verbatim per candidate |

**Quota spent: 1,616 units estimated (16 × `search.list` @ 100, 16 × `videos.list` @ 1).**
The probe does not self-record, so it was written to the ledger by hand
(`scripts/yt_quota.py` → `record()`), moving today's Pacific total from **5,188 to 6,808 of 10,000**
(reading immediately after recording; a later read showed 6,821, so something else on this machine is
also writing to the ledger). The ledger's own arithmetic booked +1,620 against my estimate of +1,616;
the 4-unit difference is unexplained and is reported rather than smoothed. **~3,180 units remain today;
that is one upload's worth (1,600) plus change, so no further probing should be run before the 16:00
JST reset.** The probe overwrites a fixed output path, so the pre-existing EP60-era
`TOPIC_DEMAND_PROBE.json` was backed up and restored, and this run was written to a new filename.

---

## 0. The answer, first

**Rank on the v002 total, ties broken on measured demand.**

| # | candidate | v002 | verdict | 45 min? | demand median | ≥30 min rivals | producibility (narrow core) | the one reason |
|--:|---|--:|---|---|--:|--:|---|---|
| 1 | **The wrong house** — *Martin v. United States* | **110** | FLAGSHIP | yes | 878,755 | **1** | 0.44 red / 0.36 amber | Highest score, real demand, and only one long-form rival on the whole subject |
| 2 | Social Security overpayments | 103 | PRIORITY | **not yet** | 20,093 | 0 | 0.36 amber | Perfect contradiction and perfect audience fit, but no protagonist with a full arc has been found — the exact defect that sank EP70 |
| 3 | Kevin Strickland — 43 years, $0 | 101 | PRIORITY | yes | **2,189,547** | 1 | **0.81 red** | The largest measured demand on the slate; the 1978 quarter of the film cannot be dressed from this shelf |
| 4 | PG&E Fire Victim Trust | 101 | PRIORITY | yes | 1,110 | 0 | 0.34 amber | Sustains the length easily, and nobody is searching for it |
| 5 | Gerardo Serrano's truck | 100 | PRIORITY | **no — 30 min** | 718 | 1 | **0.82 red** | The channel has already made three forfeiture episodes, and this story ends at thirty minutes |
| 6 | Detroit face-recognition arrests | 97 | PRODUCTION | as a pattern film | 9,487 | 0 | **0.14 green** | The easiest of the eight to dress, but the length has to come from four people, not one |
| 7 | Michigan MiDAS algorithm | 94 | PRODUCTION | yes | **29** | 2 | 0.29 amber | Textbook contradiction with a measured market of essentially zero |
| 8 | Le Roy Torres — burn pits | 92 | PRODUCTION | yes | 14,525 | 0 | 0.21 amber | The cleanest 19-year aftermath spine on the slate and the weakest thumbnail |

*Demand median is the strongest framing measured for each subject; for candidate 3 that is the premise
framing ("wrongfully convicted man receives no compensation from state"), not the case name, which
measures at 11,507. Both figures are reported in §3.4. "≥30 min rivals" counts results of 30 minutes or
longer in the same result set — the long-form slot each candidate would be entering.*

**Recommendation: build candidate 1.** It is the only one that is simultaneously top of the rubric,
top-quartile on measured demand, unoccupied at long form, and carried by a named ordinary family
whose account is quoted verbatim in a Supreme Court opinion that is still unresolved in 2026.

**One structural finding that applies to the whole slate and is worth more than any single pick:**
an aftermath-weighted 45-minute film is *easier* to dress than an incident-weighted one. This shelf
is 93.5% contemporary stock; EP68 measured 26 clips channel-wide naming a year between 1955 and 1985,
and the independent sweep run for this file returns **17** clips whose title carries a 1970s marker
(that is a different regex, not a re-verification of EP68's 26). Aftermath is
contemporary by definition — offices, courthouses, documents, present-day streets. **The brief's
editorial rule and the shelf's actual inventory point the same way.** The only candidate that fails
producibility badly (Strickland) fails precisely on the quarter of the film that is *incident*, not
aftermath.

---

## 1. Candidate 1 — THE WRONG HOUSE · *Martin v. United States* · **110 FLAGSHIP**

`episodes/_planning/premises_45min/A_wronghouse.json` → `A_wronghouse.scored.json`

### 1.1 The contradiction, one sentence

> They were the wrong house, the government admitted it, and for eight years its legal answer was that
> nobody could be held responsible because deciding whether to check the address was a discretionary
> policy choice.

### 1.2 The named ordinary protagonists

**Curtrina Martin, Hilliard Toi Cliatt, and her seven-year-old son (G. W.).**

Source retrieved in full by this agent from the CourtListener v4 API, opinion id **11070040**
(`https://www.courtlistener.com/api/rest/v4/opinions/11070040/`), 56,624 characters of slip-opinion
text — **MARTIN, individually and as parent and next friend of G. W., a minor, et al. v. UNITED STATES
et al.**, No. 24–362, Supreme Court of the United States, argued 29 April 2025, **decided 12 June
2025**, Gorsuch, J., with a concurrence by Sotomayor, J. Verbatim, from the opinion of the Court:

> "In the predawn hours of October 18, 2017, the Federal Bureau of Investigation raided the wrong
> house in suburban Atlanta. Officers meant to execute search and arrest warrants at a suspected gang
> hideout, 3741 Landau Lane. Instead, they stormed a quiet family home, 3756 Denville Trace, occupied
> by Hilliard Toi Cliatt, his partner Curtrina Martin, and her 7-year-old son G. W. … A six-member
> SWAT team, led by FBI Special Agent Lawrence Guerra, breached the front door and detonated a
> flash-bang grenade. Fearing a home invasion, Mr. Cliatt and Ms. Martin hid in a bedroom closet. But
> the SWAT team soon found the couple's hiding spot, dragged Mr. Cliatt from the closet, 'threw [him]
> down on the floor,' handcuffed him, and began 'bombarding [him] with questions.' Meanwhile, another
> officer trained his weapon on Ms. Martin, who was lying on the floor half-naked, having fallen
> inside the closet. Only then did another officer stumble across some mail with the home's address on
> it and realize the team had the wrong house."

And the two facts that make it a film rather than an incident:

> "No one could confirm as much later because Agent Guerra 'threw . . . away' his GPS device 'not long
> after' the raid. And it seems the agents neither noticed the street sign for 'Denville Trace,' nor
> the house number, which was visible on the mailbox at the end of the driveway."
> — same opinion, citing 631 F. Supp. 3d 1281, 1287–88 (N.D. Ga. 2022)

> "Left with personal injuries and property damage—but few explanations and no compensation—Mr. Cliatt
> and Ms. Martin sued the United States."

The "wait, that is allowed?" is in Justice Sotomayor's concurrence, describing the position the United
States actually took:

> "it is hard to see how Guerra's conduct in this case, including his allegedly negligent choice to
> use his personal GPS and his failure to check the street sign or house number on the mailbox before
> breaking down Martin's door and terrorizing the home's occupants, involved the kind of policy
> judgments that the discretionary-function exception was designed to protect."
> — SOTOMAYOR, J., concurring, 605 U. S. ____ (2025), slip op. at 4

The same concurrence hands the film its second act for free — the reason Congress wrote the law in the
first place:

> "In April 1973, Herbert and Evelyn Giglotto awoke in their Collinsville, Illinois, townhouse 'to the
> sound of someone smashing down their door and bursting into their house.' … After 15 state and
> federal officers ransacked the Giglottos' home, tied them up at gunpoint, and threatened to shoot
> Mr. Giglotto if he moved, the officers realized they '"ha[d] the wrong people."' The officers
> eventually moved on to the home of Donald Askew, where they terrorized yet another innocent couple
> before confessing they had acted on a 'bad tip.'"
> — SOTOMAYOR, J., concurring, slip op. at 5, quoting 54 N. C. L. Rev. 497, 500–501 (1976)

Congress amended the FTCA in 1974 *because of* wrong-house raids. Fifty-one years later the Eleventh
Circuit read that amendment in a way that left a wrong-house family with nothing. That is a `WHY
NOBODY FIXED IT` (S30) engine sitting inside a `THE HIDDEN RULE` (S01) film.

### 1.3 Why it sustains 45 minutes

Length here is carried entirely by aftermath. The raid is four minutes of screen time; the eight years
after it are the film.

| act | minutes | what carries it |
|---|--:|---|
| I. The house | 8 | 18 Oct 2017 pre-dawn; the closet; the mail on the floor; the family afterwards; the seven-year-old |
| II. The paperwork years | 9 | administrative claim → suit → the FBI's account → the discovery that the GPS was thrown away → the parked car nobody noticed |
| III. The first no | 8 | 631 F. Supp. 3d 1281 (N.D. Ga. 2022): summary judgment for the government. The Eleventh Circuit affirms. The government's written position: checking the address was a policy judgement |
| IV. Collinsville, 1973 | 8 | the Giglottos and the Askews; the Senate report; why Congress wrote the 1974 amendment; the system's own rationale stated before its failure — the v002 `the_unexpected_rationale` rule |
| V. The argument | 7 | 29 April 2025 — public-domain oral-argument audio, real voices, the Moment of Truth |
| VI. And still no trial | 5 | unanimous reversal 12 June 2025; remand; 2026, nothing decided; the Hidden Rule stated in one line |
| | **45** | |

Six acts, one family, seven documented turns, and the last one has not happened yet. Nothing is padded
and nothing is invented.

### 1.4 Measured demand and saturation

Query `FBI raided the wrong house family lawsuit`, 15 results, long-form (≥3 min) subset = 6:

- **median views 878,755**, max 4,575,210
- **5 results above 100k views, across 5 distinct channels** → two-channel premise test **PASS**
- **≥20 min: 1. ≥30 min: 1. ≥45 min: 0.**

The single long-form rival is *The Civil Rights Lawyer*, "FBI SWAT Raided the Wrong House, Terrorized…",
37 minutes, April 2025, **878,755 views**. Everything else above 100k is a news clip of 3–13 minutes.

**That is the shape the brief asked for: high demand, nearly no long-form supply.** For calibration,
the channel's own two biggest wins measure at median 1,225,933 (Titan, 8 rivals ≥20 min) and 1,401,010
(D. B. Cooper, 10 rivals ≥20 min). This candidate has ~63% of Titan's median demand against **one
eighth** of its long-form competition.

### 1.5 v002 score

RAW 114/120 → normalised **95**, + `real_footage` + `recognizable_institution` + `major_reversal` =
**110 → FLAGSHIP**, exactly on the line. Full per-axis justification is in the premise file; the two
that matter:

- `human_stakes` **11/15**, deliberately not higher. Nobody died, nobody was imprisoned, no house or
  life savings was lost. It is injuries, terror and eight years of no answer. Scoring it 15 would be
  padding.
- `personal_relevance` **15/15**. The contact point is the viewer's own front door at 4 a.m.

**Note honestly: it lands on 110 by exactly zero margin.** Remove any one bonus and it is 105
PRIORITY. It is a flagship on the tool's arithmetic, not by a comfortable margin.

### 1.6 Producibility

- register union (8 buckets): **3,398** distinct playable clips → 400 cuts = **0.118 GREEN**
- **narrow core** (residential front door 139 · tactical police/FBI 190 · courtroom/Supreme Court 37) =
  **366** distinct → 160 narrow cuts = **0.437 RED**, 131 distinct narrow assets = **0.358 AMBER**

Read the narrow number, not the union — that is the whole EP68 lesson. The staging plan the amber band
requires is explicit: the narrow core is **contemporary**, so it is a re-harvest problem, not an
absence problem. There is no era constraint anywhere in this film. The three thin buckets are all
things modern stock genuinely holds (doors, tactical police, court interiors) and the shelf's weakness
is its *titles*, not its stock.

### 1.7 Ban / legal risk

**LOW.** Every fact comes from a published Supreme Court opinion and a published district-court
opinion. The individual agent is named by the Court itself. No living private individual is accused of
a crime. The one discipline: the case is on remand and undecided, so the film says *alleged* and
*according to the record* about the officers' conduct, per `topic_sources.ongoing_cases`.

---

## 2. Candidate 2 — SOCIAL SECURITY OVERPAYMENTS · **103 PRIORITY** · *not yet a 45-minute film*

`episodes/_planning/premises_45min/B_ssa_overpayment.json`

### 2.1 The contradiction

> She did nothing wrong, the government made the mistake, the government kept paying her anyway — and
> the government's remedy was to take her whole income until a five-figure debt she never incurred was
> repaid.

### 2.2 The named protagonist — and this is where it fails

**Justina Worrell**, through her aunt and caregiver **Addie Arnold**. Retrieved by this agent from
KFF Health News' *Overpayment Outrage* hub, `https://kffhealthnews.org/overpayment-outrage/`
(KFF Health News / Cox Media Group investigation; the series won the Goldsmith Awards' inaugural
Government Reporting Prize). The figure demanded of her: **$60,175.90**, and Arnold's own line, that
neither of them has $60,175.90 to repay the government.

The scale, from the same investigation: **more than 2 million people a year** receive overpayment
demands out of roughly 70 million beneficiaries, against **over $23 billion** in outstanding
overpayments.

**That is one name, one number and one snapshot.** It is the Levias problem from EP70 all over again:
a perfect opening beat with no second frame. No court record, no docket, no sworn account, no followed
life.

### 2.3 Why it does NOT sustain 45 minutes — yet

Acts I and II write themselves (the letter, the mechanics of how SSA overpays and then claws back).
Act III is a policy chronology — March 2024, the commissioner ends 100% withholding and calls it
"clawback cruelty"; 2025, full withholding resumes — and a policy chronology is not a third act.
**As the record stands this is a strong 30-minute film.** It becomes a 45-minute film if, and only if,
a beneficiary is found with a documented arc: notice → appeal → waiver denied → withholding →
consequence → outcome. The first place to look is the Social Security Administration's own Office of
Hearings, the OIG reports, and the witness testimony from the 2024 congressional hearings.

### 2.4 Measured demand

Query `social security overpayment clawback demand repay`: median **20,093** views, max 1,321,840
(60 Minutes, 13 min, Nov 2023), 1 channel above 100k, **zero results ≥20 minutes**. Long-form is
completely unoccupied. The 60 Minutes number proves the appetite exists at short length.

### 2.5 Score and producibility

RAW 106 → 88 normalised, + `specific_money_amount` + `recognizable_institution` + `major_reversal` =
**103 PRIORITY**. `story_arc` scored **7/15** — the honest marker of the protagonist gap. `evidence`
scored 8: excellent journalism, no adjudicated record.

Producibility: union 3,441 → 0.116 **green**; narrow core (letter/envelope 87 · older person at home
84 · government counter 287) = 450 → **0.356 amber**. Contemporary throughout.

### 2.6 Risk

**LOW–MEDIUM.** The subject is a live federal policy fight and the film must not become a political
argument; state the agency's own rationale (it is statutorily required to recover overpayments) before
showing the harm. Naming a disabled beneficiary and her caregiver requires care — they are victims,
not litigants, and consent was given to journalists, not to us.

---

## 3. Candidate 3 — KEVIN STRICKLAND · **101 PRIORITY** · highest measured demand

`episodes/_planning/premises_45min/C_strickland.json`

### 3.1 The contradiction

> A Missouri court declared his conviction could not stand after forty-three years, and the same
> state's law then classified him as not innocent enough to be paid a cent, because the evidence that
> freed him was not DNA.

### 3.2 The named protagonist

**Kevin Strickland**, convicted 29 June 1979 for a 1978 triple murder, released **23 November 2021**,
aged 18 at conviction and 62 at exoneration. Retrieved by this agent from KCUR (NPR, Kansas City),
`https://www.kcur.org/news/2021-11-23/kevin-strickland-to-be-freed-from-prison-after-43-years-as-missouri-judge-overturns-his-conviction`.
Judge **James Welsh**, verbatim:

> "The Court's confidence in Strickland's conviction is so undermined that it cannot stand."

Strickland, on release:

> "I didn't think this day was going to come. I mean, not before I got this legal team, I didn't."
> … "I was the easy mark, and the police took advantage of it."

The compensation rule, retrieved by this agent from the Missouri Revisor of Statutes,
`https://revisor.mo.gov/main/OneSection.aspx?section=650.058` — restitution requires that testing
ordered under §547.035 (the DNA statute) or by court order confirm innocence. Strickland's exoneration
rested on a recantation, not DNA. **He received nothing from the State of Missouri.** Roughly $1.7m was
raised for him by strangers instead.

*Not verified in this pass, and flagged rather than assumed:* the 23 November 2021 ruling itself was
not retrieved — no docket number is in hand, and the National Registry of Exonerations
(`exonerationregistry.org/cases/13125` and the Michigan Law mirror) returned **HTTP 403 to both
WebFetch and a browser-UA curl**. `evidence` is scored 8, not 10, for exactly that reason.

### 3.3 Why it sustains 45 minutes

| act | minutes | what carries it |
|---|--:|---|
| I. 1978–79 | 9 | the killings; a nineteen-year-old survivor's identification; a conviction at 18 |
| II. The witness who spent her life trying to take it back | 10 | Cynthia Douglas's recantation attempts — **needs primary-source verification before this act is written** |
| III. Forty-three years | 8 | what the number means in life units; the prosecutor who came to agree with him |
| IV. The state fights the release | 8 | the county prosecutor for him, the attorney general against him |
| V. The bill nobody pays | 7 | §650.058; $0; strangers raise $1.7m; the legislature debates and does not act |
| VI. What he was owed | 3 | the Hidden Rule |
| | **45** | |

### 3.4 Measured demand — the strongest number on the slate

The case name alone measures poorly: `kevin strickland wrongful conviction 43 years` → median 11,507,
zero channels above 100k, **zero results ≥20 min**.

The *premise* framing measures enormously: `wrongfully convicted man receives no compensation from
state` → **median 2,189,547 views**, max 29,203,471, **5 results above 100k across 4 channels**
(two-channel test PASS), and **only 1 result ≥20 minutes** (48 Hours, 42 min, 1,664,619 views).

That gap is itself the lesson: **PD titles the premise, not the case name**, and this premise is where
the audience is.

### 3.5 Producibility — the one real failure on this slate

- union 2,768 → 400 cuts = 0.145 **green** (and that green is a lie, exactly as it was for EP68)
- **narrow core**: period 1970s American street/interior **17 clips** (11 archival) · prison cell/bars
  169 · police lineup/mugshot/interrogation **11** → union 197 → **0.812 RED**

Roughly a quarter of this film must read as 1978 Kansas City. The shelf holds seventeen clips
channel-wide whose titles carry a 1970s marker, and EP68 established that none of them is an American
street, car, interior or courtroom. **This is not a query problem and more searching does not fix it.**
It is buyable — the era-bound quarter is ~100 cuts, which is roughly 3 GPU-hours of i2v off
period-correct stills — but that budget has to be agreed at premise time, not discovered at assembly,
and it must be agreed against the recorded fact that the channel's normal shape is ~0% AI motion.

### 3.6 Risk

**MEDIUM.** A real triple murder with real victims and their families; the actual killers were named in
the proceedings. The v002 brand rule is binding here: sell the failure of the institution, never the
murder (`S04`). Do not restage the killings.

---

## 4. Candidate 4 — THE FIRE VICTIM TRUST · **101 PRIORITY**

`episodes/_planning/premises_45min/E_campfire_trust.json`

### 4.1 The contradiction

> The utility was convicted of manslaughter and the survivors were made shareholders in it, so the
> money they were owed rose and fell with the fortunes of the company that had destroyed them — and
> after eight years it still has not reached 100 cents on the dollar.

### 4.2 What was retrieved

The Trust's own update page, `https://www.firevictimtrust.com/TrustUpdates.aspx`, retrieved by this
agent: **pro rata payment 70%, effective 24 October 2024**; a 13 November 2024 update stating that
payments "have surpassed the total anticipated Trust funding of $13.5 billion"; a Trustee's letter
dated **30 June 2026** discussing Davey Tree settlement funds and the **final** pro rata calculation.
The Trust's own description confirms it was funded through PG&E stock holdings sold in phases — the
2023 and 2024 Business Wire releases raise the pro rata "Based on Recent Stock Sales."

**Named survivors located but NOT yet verified to primary standard:** Sydney Robinson and Carrie Maxx,
both from ABC10 broadcast reporting surfaced in search. **I did not open those pages** and they are
therefore listed as leads, not as evidence. **No named protagonist is established for this candidate.**

### 4.3 Why it sustains 45 minutes

Easily, and it is the purest expression of the brief's own thesis: the fire is 90 minutes of one night
in November 2018 and the aftermath is eight years long — bankruptcy, the guilty plea, a trust
capitalised in the defendant's equity, share sales, pro rata steps from 30% to 45% to 60% to 66% to
70%, and families still in trailers. Acts of roughly 7 / 8 / 8 / 8 / 8 / 6.

### 4.4 Measured demand — and this is why it is fourth, not first

`camp fire pge fire victim trust survivors payments`: median **1,110** views, max 6,242, **zero
channels above 100k**, two-channel test **FAIL**. Broad reframe `wildfire victims still waiting for
settlement money`: median **1,704**, max 6,689, zero above 100k.

There is essentially no measured audience for the aftermath of this disaster. The v002 saturation rule
cuts both ways: an unoccupied slot with no demand is not an opening, it is an empty room. And the
channel has just spent a cycle discovering that a California water-infrastructure disaster does not
carry — Oroville is 150 miles from Paradise.

### 4.5 Producibility

Union 3,930 → **0.102 green**. Narrow core (wildfire 361 · burned town 75 · power line 53) = 476 →
**0.336 amber**. Contemporary, and wildfire is one of the few registers where modern stock is genuinely
abundant.

### 4.6 Risk

**LOW.** PG&E's criminal liability is adjudicated by its own plea. The Trust is a public entity
publishing its own numbers. Avoid asserting motive.

---

## 5. Candidate 5 — GERARDO SERRANO'S TRUCK · **100 PRIORITY** · a 30-minute film

`episodes/_planning/premises_45min/D_serrano.json`

### 5.1 The contradiction

> He was never charged with anything, the government never filed a case against the truck either, and
> for two years the only way to get a hearing about his own property was to pay the government a bond
> first.

### 5.2 The named protagonist

**Gerardo Serrano**, US citizen, resident of Tyner, Kentucky. Retrieved in full by this agent from the
CourtListener v4 API, opinion id **4566032** — *Gerardo Serrano v. Customs and Border Patrol, U.S.
Customs and Border Protection; United States of America; John Doe 1-X; Juan Espinoza; Kevin
McAleenan*, **No. 18-50977, United States Court of Appeals for the Fifth Circuit, filed 16 September
2020**, USDC No. 2:17-CV-48 (W.D. Tex.). Verbatim:

> "On September 21, 2015, Gerardo Serrano, a U.S. citizen and resident of Tyner, Kentucky, was driving
> his 2014 Ford F-250 pickup truck to Mexico to meet with his cousin when he was stopped at the Eagle
> Pass, Texas, Port of Entry. While still in the United States, Serrano began to take pictures of the
> border crossing with his cell phone. Two CBP agents objected … The agents searched his vehicle,
> finding a .380 caliber magazine and five .380 caliber bullets in the truck's center console."

> "While seized, he continued to make monthly loan payments of $672.97, as well as insurance and
> registration payments for a truck that he could not drive. Serrano also spent thousands of dollars
> on rental cars." — footnote 6

> "Ultimately, Serrano was never charged with a crime and his property was returned prior to forfeiture
> proceedings." — footnote 8

And the price of a hearing, from the seizure notice quoted in the opinion:

> "cost bond in the penal sum of $5,000 or 10 percent of the value of the claimed property, whichever
> is less, but in no case shall the amount of the bond be less than $250.00."

### 5.3 Why it is 30 minutes, not 45

The record is finite and the aftermath is procedural: seizure 21 Sept 2015 → notice 1 Oct 2015 → truck
returned after roughly two years → complaint 6 Sept 2017 → dismissal → **AFFIRMED 16 Sept 2020** →
certiorari denied. Four moves and one human. There is no second life to follow and no reversal to
land. **It is a 30-minute film. Recommend it be dropped from the 45-minute shortlist.**

### 5.4 Measured demand, and the decisive fact

`customs border seized truck civil forfeiture bullets`: median **718**, one channel above 100k (the
Institute for Justice's own 3-minute video, 266,150 views). Broad reframe `police seized his car he was
never charged with a crime`: median **884**.

More decisive than the probe: **the channel has already made this film three times.** Verified by
directory listing in this repository — `EP28_forfeiture`, `EP34_rolin` (airport cash seizure) and
`EP35_hinders` (IRS structuring) are all civil-forfeiture episodes. A fourth is a repeat of a lane the
channel has already worked, which the v002 `crossbreed_rule` explicitly warns against: when something
wins, transplant the DNA onto a different system rather than making ten more like it.

*(An earlier draft of this file cited a measured forfeiture demand median of 1,102 against 540,000–
860,000 for wrongful conviction. That figure could not be located anywhere in this repository and has
been removed rather than repeated from memory.)*

### 5.5 Producibility

Union 3,222 → 0.124 green. **Narrow core**: border/port of entry 64 · pickup/impound 107 ·
bullets/magazine **25** → union **196** → **0.816 RED**. A border booth and an impound lot are both
thin on this shelf.

### 5.6 Risk

**LOW.** Published federal opinion; the individual agent is named by the court.

---

## 6. Candidate 6 — THE DETROIT FACE-MATCH ARRESTS · **97 PRODUCTION** · greenest to produce

`episodes/_planning/premises_45min/F_detroit_face.json`

### 6.1 The contradiction

> The software returned a name, no human checked whether the man it named had ever been near the shop,
> and he was arrested in his own driveway for a theft that happened while he was somewhere else.

### 6.2 The named protagonist and the pattern

**Robert Williams.** Retrieved by this agent from the ACLU's case page,
`https://www.aclu.org/cases/williams-v-city-of-detroit-face-recognition-false-arrest`: arrested January
2020 "outside his home, in front of his two young daughters and wife and in plain view of his
neighbors," and "subjected to thirty hours of detention in an overcrowded, dirty cell." Suit filed
**13 April 2021**, U.S. District Court for the Eastern District of Michigan; settled **28 June 2024**
with **$300,000** to Williams and a court-enforceable policy regime.

The pattern is verifiable independently, and this is the strongest thing about the candidate. A
CourtListener RECAP query run by this agent returns **four separate federal wrongful-arrest dockets
against the same city**:

| case | docket | filed | terminated |
|---|---|---|---|
| Burton v. City of Detroit | 2:20-cv-12182 | 2020-08-13 | 2022-02-16 |
| Oliver v. Detroit, City of | 2:20-cv-12711 | 2020-10-06 | 2024-08-22 |
| Williams v. City of Detroit | 2:21-cv-10827 | 2021-04-13 | — |
| **Crutchfield v. Detroit, City of** | **2:25-cv-10514** | **2025-02-21** | **still open** |

That is `THIS KEEPS HAPPENING` (S33) with the docket numbers to prove it, and a live case in 2026.

### 6.3 Length

**45 minutes only as a pattern film** — one person, then "he is not the only one", then four, then the
system. No single one of the four arrests carries 45 minutes; Williams's own loss is 30 hours and
$300,000. Acts of roughly 8 / 8 / 8 / 8 / 8 / 5, with act IV being the settlement audit of every case
since 2017.

### 6.4 Measured demand

`facial recognition wrongful arrest police`: median **9,487**, max 117,738 (ACLU's own 8-minute video),
one channel above 100k, **zero results ≥20 minutes**. Unoccupied at length; modest demand. Per
`audience_reality`, this is an acquisition experiment aimed at an audience PD does not yet have and
must not be judged on the same CTR expectation.

### 6.5 Producibility — the best on the slate

Union **4,989** → 400 cuts = **0.080 green**. **Narrow core** (CCTV 632 · face/biometric 78 · police
station/booking 478) = **1,176** → **0.136 GREEN**. It is the only candidate green on the narrow
reading. Everything it needs is contemporary and abundant.

### 6.6 Risk

**MEDIUM.** Race is unavoidably present in the record and the channel's own rule is evidence first and
no political colour. `Crutchfield` is live, so alleged / according to court records throughout. The
company that supplied the software should be named only as the record names it, with its own account
stated.

---

## 7. Candidate 7 — THE MICHIGAN MiDAS ALGORITHM · **94 PRODUCTION** · no measured market

`episodes/_planning/premises_45min/H_midas.json`

### 7.1 The contradiction

> A machine decided he had committed fraud, the state took his tax refund on the strength of it, the
> state later ruled its own finding null and void — and it still took seven years and the Michigan
> Supreme Court to establish that he was even allowed to sue for it.

### 7.2 The named protagonists

**Grant Bauserman, Karl Williams and Teddy Broe.** Retrieved in full by this agent from the
CourtListener v4 API, opinion id **9400366** (200,848 characters) — *Bauserman v Unemployment Insurance
Agency*, **Docket No. 160813, Supreme Court of Michigan, argued 6 October 2021, decided 26 July 2022**,
Cavanagh, J., before the entire bench. Verbatim:

> "Grant Bauserman separated from employment with Eaton Aeroquip and then collected unemployment
> benefits from September 2013 to March 2014. On December 3, 2014, the Agency issued two notices of
> redetermination—one claiming that Mr. Bauserman had received unemployment benefits for which he was
> ineligible and another claiming that he had intentionally misled the Agency or concealed information
> from it. The Agency assessed penalties and interest and informed Mr. Bauserman that he owed $19,910.
> … on June 16, 2015, the Agency intercepted Mr. Bauserman's tax refund. Eventually, the Agency
> reviewed the information Mr. Bauserman submitted and concluded that its adjudication of fraud was
> incorrect… On September 30, 2015, the Agency issued another redetermination, this one finding that
> the December 3, 2014 redeterminations were 'null and void.'"

> "many claimants never receive the questionnaires because they are sent only to the claimant's
> electronic account with the Agency, without any additional notice via United States mail or e-mail."

And the number the film is built on, from the Court's own footnote:

> "a study conducted by the Agency concluded that, during this same period, approximately 93% of the
> automated system's fraud determinations were incorrect."

### 7.3 Length

45 minutes is reachable but on litigation, not on a life: Bauserman's own money came back within ten
months. The class carries the catastrophe and the class is unnamed. `story_arc` scored 8 for this
reason — the same structural weakness as EP70.

### 7.4 Measured demand — the reason it is seventh

`michigan unemployment fraud algorithm false accusations`: **median 29 views**, max 2,524, **zero
channels above 100k**, two-channel test FAIL, and two results already ≥30 min (2,524 and 126 views).
Broad reframe `computer wrongly accused thousands of fraud government`: median **2,160**, max 21,073,
zero above 100k, **four results ≥30 min**.

Both the specific and the broad framing return no audience. This is not an unoccupied slot; it is a
subject nobody searches for. The `abstract_subject_warning` in the producibility gate applies to the
demand side too.

### 7.5 Producibility

Union 3,221 → 0.124 green. Narrow core (state agency office **43** · server/database 430 ·
letter/envelope 87) = 560 → **0.286 amber**. Dressable; the thumbnail, not the footage, is the problem
(`thumbnail_power` 6/10 — a screen is not an image).

### 7.6 Risk

**LOW.** Published state supreme court opinion; the defendant is a state agency.

---

## 8. Candidate 8 — LE ROY TORRES, BURN PITS · **92 PRODUCTION** · the cleanest aftermath spine

`episodes/_planning/premises_45min/G_torres_burnpits.json`

### 8.1 The contradiction

> The federal law that guarantees a returning soldier his job back was met by his own state employer's
> argument that no soldier could enforce it against a state — and after he won that argument in the
> Supreme Court and then won a jury verdict, an appellate court took the verdict away again in 2026.

### 8.2 The named protagonist

**Le Roy Torres**, Texas state trooper and Army reservist. Retrieved in full by this agent from the
CourtListener v4 API, opinion id **6496180** — *Torres v. Texas Department of Public Safety*, **No.
20–603, Supreme Court of the United States, argued 29 March 2022, decided 29 June 2022**, reported at
597 U.S. 580. Verbatim from the syllabus:

> "Petitioner Le Roy Torres enlisted in the Army Reserves in 1989. In 2007, he was called to active
> duty and deployed to Iraq. While serving, Torres was exposed to toxic burn pits, a method of garbage
> disposal that sets open fire to all manner of trash, human waste, and military equipment. Torres
> received an honorable discharge. But he returned home with constrictive bronchitis, a respiratory
> condition that narrowed his airways and made breathing difficult. These ailments, Torres says, left
> him unable to work his old job as a state trooper. Torres asked his former employer, respondent
> Texas Department of Public Safety (Texas), to accommodate his condition by reemploying him in a
> different role. Texas refused."

And the reason this candidate exists at all — the fight is **still going in 2026**. Also retrieved in
full by this agent, opinion id **11324207**: *Texas Department of Public Safety v. Le Roy Torres*,
**No. 15-24-00089-CV, Fifteenth Court of Appeals of Texas, opinion filed 7 May 2026**, on appeal from
County Court at Law No. 1, Nueces County, Trial Court Cause No. 2017-CCV-61016-1:

> "Because the jury was instructed on an invalid theory of liability, we reverse the trial court's
> judgment."

He won at the Supreme Court of the United States, won at trial, and in May 2026 — nineteen years after
the deployment — the verdict was taken away and the case sent back.

### 8.3 Why it sustains 45 minutes better than anything else here

2007 deployment → 2009 reemployment → deterioration → diagnosis → refusal → 2017 suit → sovereign
immunity → 2022 Supreme Court → jury verdict → **7 May 2026 reversal** → remand. Ten documented moves
on one named man over nineteen years, each with a document. Acts of roughly 8 / 8 / 7 / 8 / 8 / 6.
This is what the brief means by aftermath, in its purest available form.

### 8.4 Measured demand

`burn pits veteran lawsuit denied benefits`: median **14,525**, max 52,291, **zero channels above
100k**, **zero results ≥20 min**. Broad reframe `veteran fought the government for years over
benefits`: median 17,912, max 137,881, one channel above 100k, one result ≥20 min. Low demand,
completely unoccupied at length. The audience fit is unusually good — the base is 92.5% male and 77%
aged 55+ — but that is reach *into* the existing audience, not beyond it.

### 8.5 Producibility

Union 2,164 → 0.185 **amber** (the lowest union on the slate). Narrow core (Iraq deployment 167 with
55 archival · burning pit / smoke 499 · oxygen and lungs 97) = **758** → **0.211 amber**. Iraq-era
military is the one place where the shelf's archival holdings actually help.

### 8.6 Risk

**LOW–MEDIUM.** Live litigation on remand; do not state the outcome. The film must state DPS's own
position, which the Fifteenth Court accepted on the law.

---

## 9. What was NOT verified — so that no absence is later mistaken for a finding

1. **The Kevin Strickland ruling of 23 November 2021 itself.** Not retrieved. No docket number in hand.
   The National Registry of Exonerations returned HTTP 403 to WebFetch and to a browser-UA curl at both
   `exonerationregistry.org/cases/13125` and the Michigan Law mirror. Cynthia Douglas's recantation
   history is asserted nowhere in this file because it was not verified.
2. **Any named Camp Fire survivor.** Sydney Robinson and Carrie Maxx appeared in search summaries; the
   pages were **not opened**, and they are leads, not evidence. Candidate 4 currently has no verified
   protagonist.
3. **The Fire Victim Trust's original capitalisation split** (cash vs. number of PG&E shares). The
   Trust's own page confirms stock holdings sold in phases; the exact share count was not retrieved.
4. **The Detroit settlement agreement text.** The ACLU summary page was fetched but carries only
   metadata; the PDF itself was not opened. The four docket numbers in §6.2 WERE retrieved, from the
   CourtListener RECAP API.
5. **Institute for Justice pages on Serrano** — `ij.org` returned HTTP 403 to both WebFetch and a
   browser-UA curl. Nothing in §5 rests on IJ material; it all comes from the Fifth Circuit opinion.
6. **Justina Worrell's outcome.** Whether the $60,175.90 demand was waived, reduced or collected is
   unknown.
7. **Whether any protagonist named here is alive, traceable or willing to speak.** Out of scope, not
   investigated.
8. **The Martin remand.** No post-June-2025 docket activity was checked. The film's final act is
   currently "nothing has happened yet", and that must be re-verified immediately before scripting.

---

## 10. Producibility — full measurement, reproducible

**Pool.** Built exactly as `EP68_pinto_register_inventory.v001.md` builds it, and it reproduces EP68's
number to the unit:

```
video rows across all stock ledgers, deduped by sha256      26,101 DISTINCT PLAYABLE VIDEO
  withheld: ban-risk quarantine        762
  withheld: sitting in _quarantine   1,326
  withheld: owner-marked unusable    9,547
  withheld: absent from disk         2,682
```

Ledger `H:\pd-media\assets\archive\_ledger\*.jsonl`, excluding `purged.jsonl`,
`ban_risk_quarantine.jsonl`, `shot_feedback.jsonl`, `rejects*`, `*_removed.jsonl`, `*_candidates.jsonl`;
withholding rows in the ban-risk ledger, rows whose path contains `_quarantine`, and (theme, source)
pairs marked `unusable` in `H:\pd-media\assets\archive\_qc\archive_verdicts.jsonl`; subtracting
`absent_index.json`. Match is a word-boundary `re.I` search over the provider title.

**Sizing.** A 45-minute film ≈ **400 video cuts**; at EP68's measured distinct fraction of 0.818 that
is **327 distinct assets**. The **narrow core** — the registers whose frame must read as a specific
thing rather than as an abstraction — is taken at 40% of the film: **160 cuts / 131 distinct assets**.

| candidate | union | util 400 | util 327 | narrow union | narrow util 160 | narrow util 131 |
|---|--:|--:|--:|--:|--:|--:|
| 1 wrong house | 3,398 | 0.118 🟢 | 0.096 🟢 | 366 | **0.437 🔴** | 0.358 🟡 |
| 2 SSA overpayment | 3,441 | 0.116 🟢 | 0.095 🟢 | 450 | 0.356 🟡 | 0.291 🟡 |
| 3 Strickland | 2,768 | 0.145 🟢 | 0.118 🟢 | 197 | **0.812 🔴** | **0.665 🔴** |
| 4 Fire Victim Trust | 3,930 | 0.102 🟢 | 0.083 🟢 | 476 | 0.336 🟡 | 0.275 🟡 |
| 5 Serrano | 3,222 | 0.124 🟢 | 0.102 🟢 | 196 | **0.816 🔴** | **0.668 🔴** |
| 6 Detroit face-match | 4,989 | 0.080 🟢 | 0.066 🟢 | 1,176 | **0.136 🟢** | **0.111 🟢** |
| 7 MiDAS | 3,221 | 0.124 🟢 | 0.102 🟢 | 560 | 0.286 🟡 | 0.234 🟡 |
| 8 Torres | 2,164 | 0.185 🟡 | 0.151 🟡 | 758 | 0.211 🟡 | 0.173 🟡 |

**The union column is green for all eight and it means nothing.** That is EP68's finding restated: a
noun-based measurement returns green while the film cannot be dressed. The binding column is the narrow
one. Two candidates are red on it because their narrow registers are genuinely thin on this shelf
(a border booth; an impound lot; a 1970s American street), and one — Strickland — is red for the EP68
reason exactly: **period**. The 1970s bucket returns **17 clips channel-wide, 11 of them archival**,
and EP68 established by hand review that none of them is an American street, car, interior or
courtroom.

Per-bucket counts are in `episodes/_planning/measurements/EP70_45MIN_REGISTER_INVENTORY.v001.json`.
The bucket regexes are verbatim in the three scripts that produced it, kept beside it so the numbers
can be regenerated exactly: `EP70_45min_pool.py` (builds the 26,101 pool), `EP70_45min_registers.py`
(union), `EP70_45min_registers_narrow.py` (narrow core). Run from that directory with
`py -3.11 EP70_45min_pool.py` first. The scoring inputs and outputs are committed under
`episodes/_planning/premises_45min/`.

---

## 11. Two things the owner should decide

1. **The 45-minute slot.** Candidate 1 is the recommendation, and it is the only candidate that clears
   every gate at once. If the owner wants the largest measured audience instead of the highest score,
   candidate 3 (Strickland, median 2.19m) is the answer, and the price is an agreed AI-motion budget of
   roughly 100 cuts / ~3 GPU-hours for the 1978 quarter, agreed *now* rather than found at assembly.
2. **`score_premise.py` still defaults to v001.** Everything here was scored with `--os v002`
   explicitly. Switching the default is one line (`DEFAULT_OS = "v002"`) and, per the tool's own
   docstring, is the owner's word and not a side effect of this file.
