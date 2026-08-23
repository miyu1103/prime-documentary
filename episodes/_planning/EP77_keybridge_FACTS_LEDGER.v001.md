# EP77 `keybridge` — FACTS LEDGER v001

**Francis Scott Key Bridge / MV *Dali* — Baltimore, 26 March 2024.**
Compiled 2026-08-23 from primary records only. Every row carries the document it came from.

> ## ⛔ R3 — THIS IS A LIVE CRIMINAL CASE
>
> An indictment was **unsealed on 12 May 2026**. **An indictment is merely an accusation and all
> defendants are presumed innocent until proven guilty beyond a reasonable doubt in a court of
> law** — the Department of Justice's own words, quoted in full at KB-501.
>
> **Nothing in the `[ALLEGED]` block may be narrated as fact.** Every sentence built on those
> rows must carry *the indictment alleges*, *the United States says*, or *prosecutors charge*.
> The `forbidden_claims` list in `episode_spec.v001.json` is generated from this section and the
> script is checked against it.

## Sources

| id | document | date | url |
|---|---|---|---|
| S1 | NTSB Marine Investigation **Preliminary Report** DCA24MM031 | 2024-05 | https://www.ntsb.gov/investigations/Documents/DCA24MM031_PreliminaryReport%203.pdf |
| S2 | NTSB press release NR20251118, *Loose Wire on Containership Dali Leads to Blackouts…* | 2025-11-18 | https://www.ntsb.gov/news/press-releases/Pages/NR20251118.aspx |
| S3 | NTSB Board Summary, *Contact of Containership Dali with Francis Scott Key Bridge* | 2025-11-18 | https://www.ntsb.gov/investigations/Documents/Board%20Summary%20Contact%20of%20Containership%20Dali%20with%20Francis%20Scott%20Key%20Bridge.pdf |
| S4 | DOJ Office of Public Affairs, press release **26-476**, *Foreign Operators and Technical Superintendent of M/V Dali Indicted* | 2026-05-12 | https://www.justice.gov/opa/pr/foreign-operators-and-technical-superintendent-mv-dali-indicted-roles-key-bridge-crash |
| S5 | DOJ, *U.S. Reaches Settlement for Over $100M in Civil Lawsuit* | 2024-10 | https://www.justice.gov/archives/opa/pr/us-reaches-settlement-over-100m-civil-lawsuit-against-owner-and-operator-vessel-destroyed |
| S6 | US District Court, D. Md. — *In the Matter of the Petition of Grace Ocean Private Limited et al for Exoneration from or Limitation of Liability* | filed 2024-04-01 | https://www.mdd.uscourts.gov/news/matter-petition-grace-ocean-private-limited-et-al-exoneration-or-limitation-liability-2024-04 |
| S7 | NTSB Marine Investigation Report MIR-25-10, *Need for Vulnerability Assessment and Risk Reduction* | 2025-03-20 | https://www.ntsb.gov/investigations/AccidentReports/Reports/MIR2510.pdf |

**S1, S2, S4 and S5 were fetched and read for this ledger. S3, S6 and S7 are cited from the
titles and figures quoted inside S2 and S4 and have NOT been opened line by line — every row
that rests on them is marked `[UNREAD SOURCE]` and must be confirmed before it is narrated.**
`justice.gov` returns HTTP 403 to the ordinary fetcher; it was read with `curl` and a browser
user-agent. Note that for whoever reads this next.

---

## A. The night — established by the NTSB (S1)

| id | fact | source |
|---|---|---|
| KB-001 | The vessel is the **Dali**, a Neo-Panamax containership, **Singapore-flagged**, **IMO 9697428** | S1 p.1 |
| KB-002 | Contact occurred **26 March 2024, about 01:29 eastern daylight time** | S1 p.1 |
| KB-003 | **Injuries: 8, of which 6 fatal** | S1 p.1 |
| KB-004 | The people on the bridge were **a seven-person road maintenance crew and one inspector**. Six of the road crew died | S2 |
| KB-005 | The ship struck **pier no. 17**, the southern pier supporting the main span | S1 p.1, p.10 |
| KB-006 | The Dali reached the US on **19 March 2024**, called at **Newark 19–21 March** and **Norfolk 22–23 March**, and moored at **Seagirt Marine Terminal, Baltimore, 23 March at 02:36** | S1 §2.2 |
| KB-007 | Main propulsion was a single **55,626 hp (41,480 kW)** diesel engine driving one propeller, **independent of the four diesel generators** | S1 p.9, p.10 |
| KB-008 | About **00:45** the senior pilot ordered "dead slow ahead"; about **01:07**, once in the channel, the tugboats were released per normal practice | S1 §1.3 |

## B. Four blackouts — and exactly where each one happened

**⚠ The two on 25 March were in port. The two on 26 March were under way.**
A line that puts all four before departure is **false**. Recorded here because a draft title
did exactly that.

| id | fact | source |
|---|---|---|
| KB-101 | **In port, 25 March, about 10 hours before departure — blackout 1.** A crewmember working on the exhaust scrubber system **mistakenly closed an inline engine exhaust damper** on the only online generator (no. 2), blocking its exhaust | S1 §2.2.1 |
| KB-102 | **In port, 25 March — blackout 2.** Related to **insufficient fuel pressure** for the online generator; breaker DGR3 opened | S1 §2.2.1 |
| KB-103 | Recovering from the second in-port blackout, the crew **switched the bus configuration from breakers HR2/LR2 and transformer TR2 — in use for several months — to HR1/LR1 and TR1** | S1 §2.2.1 |
| KB-104 | **TR1 with HR1 and LR1 was the configuration in use when the ship sailed on 26 March** | S1 §2.2.1 |
| KB-105 | **Under way, 01:25 — blackout 3 (the first of the voyage).** The Dali was **0.6 miles, three ship lengths,** from the bridge when **HR1 and LR1 opened unexpectedly**, killing lighting, the **main engine cooling water pumps** and the **steering gear pumps**. Generators 3 and 4 kept feeding the HV bus | S1 §1.3 |
| KB-106 | The emergency generator started and connected to the emergency bus shortly after power was lost; **the NTSB was still investigating the exact time** | S1 p.11 |
| KB-107 | The crew **manually closed HR1 and LR1**, restoring power to the whole vessel | S1 p.11 |
| KB-108 | **01:26:39** — the pilots called for tug assist. The **Eric McAllister** was **3 miles away**, answered immediately, and **did not reach the Dali** | S1 p.11 |
| KB-109 | The pilots' dispatcher **notified the Coast Guard** that the Dali had lost power | S1 p.11 |
| KB-110 | **Under way, 0.2 miles from the bridge — blackout 4.** Breakers **DGR3 and DGR4** opened, cutting generators 3 and 4 from the HV bus: total loss of HV and LV power | S1 p.11 |
| KB-111 | **01:27:25** — a pilot broadcast a VHF warning to all waterborne traffic | S1 p.12 |
| KB-112 | **01:27:32, about 31 seconds after the second under-way blackout**, the crew manually closed **HR2 and LR2**, restoring the LV bus from generator no. 2. **Power came back before the ship struck the pier. Propulsion did not** | S1 p.12 |
| KB-113 | **01:27:53** — the **MDTA duty officer ordered the units stationed at the ends of the bridge** to act. Contact followed at about 01:29 | S1 p.12, KB-002 |

**KB-113 → KB-002 is 67 seconds.** That interval is the spine of the film and it is arithmetic
on two sourced timestamps, not an estimate.

| id | fact | source |
|---|---|---|
| KB-114 | The bridge's piers were protected by **"dolphins" — sheet pile and concrete structures**. Two of them are labelled in the NTSB's own figure of the Dali's final track | S1 p.10, figure 7 |
| KB-115 | The Dali was **loaded**, not in ballast, when she departed | S1, main engine manoeuvring table |
| KB-116 | The vessel is required to carry a **voyage data recorder**: IMO rules apply to ships of **3,000 gross tons and above built after 1 July 2014** on international voyages. **Bridge audio continued to be captured** through the blackouts | S1 §2.3.1 |
| KB-117 | Steering pump no. 3, when running alone on emergency power, was **designed to turn the rudder more slowly** than with all pumps — and **without the propeller turning the rudder would have been less effective** | S1 p.11 |

**⚠ KB-118 is NOT established and must not be narrated.** The film's ending drafted a line about
how long the bridge had stood. **No opening date for the Francis Scott Key Bridge has been taken
from a primary source in this ledger.** Either source it or say nothing.

## C. Cause, as determined by the Board (S2)

| id | fact | source |
|---|---|---|
| KB-201 | The NTSB held its board meeting and determined probable cause on **18 November 2025** | S2 |
| KB-202 | **Probable cause:** loss of electrical power **due to a loose signal wire connection to a terminal block, stemming from the improper installation of wire-label banding**, resulting in loss of propulsion and steering close to the bridge | S2 |
| KB-203 | The mechanism, in the Board's words: **wire-label banding prevented the wire from being fully inserted into a terminal block spring-clamp gate, causing an inadequate connection** | S2 |
| KB-204 | **Contributing:** the absence of countermeasures to reduce the bridge's vulnerability to collapse from a vessel strike, which **could have been implemented had the Maryland Transportation Authority conducted a vulnerability assessment** | S2 |
| KB-205 | AASHTO guidance recommending such assessments is **longstanding**, and the Board found the authority **were likely unaware of the potential risk** | S2 |
| KB-206 | On **20 March 2025** the NTSB identified **68 bridges** in the United States for which it recommended a vulnerability evaluation | S2, and S7 `[UNREAD SOURCE]` |
| KB-207 | At the 18 November 2025 meeting the Board stated the **complete report would follow in the coming weeks**. **Whether it has since been published is NOT established here — check before narrating** | S2 |

## D. The money, in civil court

| id | fact | source |
|---|---|---|
| KB-301 | **Grace Ocean Private Limited** (owner) and **Synergy Marine Private Limited** (manager) filed for **exoneration from, or limitation of, liability** in the District of Maryland, **1 April 2024** | S6 `[UNREAD SOURCE]`, S5 |
| KB-302 | They sought to limit their liability to **approximately $43.7 million** | S5 |
| KB-303 | The United States claimed **$103,078,056** under the **Rivers and Harbors Act, the Oil Pollution Act and general maritime law** | S5 |
| KB-304 | The companies agreed to pay **$101,980,000** to resolve the United States' civil claim | S5 |
| KB-305 | A settlement of a civil claim is **not** a finding of criminal liability and **not** an admission. Do not narrate it as either | — |

## E. `[ALLEGED]` — the criminal indictment, unsealed 12 May 2026 (S4)

**Every row in this section is an allegation. Narrate with attribution or not at all.**

| id | allegation | source |
|---|---|---|
| KB-401 | Charged: **Synergy Marine Pte Ltd** (Singapore), **Synergy Maritime Pte Ltd** (Chennai, India), and **Radhakrishnan Karthik Nair, 47**, an Indian national who worked for both companies as the **Technical Superintendent** for the Dali | S4 |
| KB-402 | Counts: **conspiracy to defraud the United States**; **willfully failing to immediately inform the U.S. Coast Guard of a known hazardous condition**; **obstruction of an agency proceeding**; **false statements** | S4 |
| KB-403 | The two corporations are also charged with **misdemeanour** violations of the **Clean Water Act, Oil Pollution Act and Refuse Act** for discharge into the Patapsco River — containers and their contents, oil, **and the bridge itself** | S4 |
| KB-404 | The indictment alleges the economic loss is **at least $5 billion** | S4 |
| KB-405 | **The mechanism alleged.** The Dali **lost power twice in a four-minute span** leaving the Port of Baltimore. A **loose wire in a high-voltage switchboard likely caused the first** loss | S4 |
| KB-406 | Critical systems were **originally designed with reliable redundancies and automatic restart**, so the ship could recover quickly from a blackout | S4 |
| KB-407 | **The defendants allegedly altered the ship and relied on a flushing pump to supply fuel to two of the Dali's four generators.** The flushing pump **was not designed to automatically restart after a blackout**, and the generators could not run without fuel — so the second blackout followed | S4 |
| KB-408 | **The indictment alleges that with the proper fuel supply pumps the vessel would have regained power in time to navigate safely under the Key Bridge** | S4 |
| KB-409 | The obstruction counts relate, among other things, to **Nair's statements to the NTSB that he was unaware the Dali was using the flushing pump to fuel the generators** | S4 |
| KB-410 | Investigating: **FBI, Coast Guard Investigative Service, EPA Criminal Investigation Division**. Prosecuting: AUSAs **Matthew Phelps, Bijon Mostoufi, Kimberly Phillips** (D. Md.) and Trial Attorney **Leigh Rendé** (ENRD Environmental Crimes) | S4 |
| KB-411 | FBI Baltimore SAC **Jimmy Paul**: investigative teams "worked diligently over the last two years" | S4 |

| id | verbatim, and it governs the whole script | source |
|---|---|---|
| **KB-501** | **"An indictment is merely an accusation. All defendants are presumed innocent until proven guilty beyond a reasonable doubt in a court of law."** | S4 |

## E2. NOT alleged — **admitted**. The chief engineer's deferred prosecution agreement

**Added 2026-08-23 after a second research pass. This is the single most important block in the
ledger, and it is a different legal animal from section E.** These are not charges. They are
things a participant **acknowledged** in a written agreement with the United States.

| id | fact | source |
|---|---|---|
| KB-701 | **United States v. Karthikeyan Deenadayalan**, No. **1:26-CR-00197** (District of Maryland) | S8 |
| KB-702 | On **18 June 2026** Deenadayalan entered into a **Deferred Prosecution Agreement** | S8 |
| KB-703 | He was the **chief engineer of the M/V Dali** and was aboard on 26 March 2024. An Indian national | S8 |
| KB-704 | He **admitted failing to report a hazardous condition**, in violation of the **Ports and Waterways Safety Act, 46 U.S.C. § 70036(b)** | S8 |
| KB-705 | **The flushing pump was not used on one ship.** He had also served as chief engineer on the Dali's sister vessels **M/V Maersk Saltoro** and **M/V Cezanne**, and **knew that all three used an unsafe fuel supply pump** | S8 |
| KB-706 | He **acknowledged that the flushing pump lacked redundancy**, which compromised the vessels' safe navigation and their **ability to recover from a loss of power** | S8 |
| KB-707 | He **knew that an inability to recover from a loss of power could adversely affect the safety of the vessel itself, and of any bridge, structure or shore area** | S8 |
| KB-708 | He **spoke and corresponded with Synergy personnel, including co-defendant Nair, about using the flushing pump** | S8 |
| KB-709 | **`[HIS ACCOUNT, NOT A FINDING]`** Deenadayalan **said that Nair directed him to send a "convincing" email to the Dali's charterer** so the charterer would not ask further questions about fuel consumption and discover the use of the flushing pump | S8 |

**How to narrate the difference, because the whole R3 posture turns on it.**

- KB-704 to KB-708 are **admissions by the man who made them**. They may be stated as what he
  admitted — *the chief engineer admitted…*, *he acknowledged…* — never as a finding against
  anyone else.
- **KB-709 is his account of another man's conduct.** Nair is a charged defendant who has not
  been tried. It must be attributed twice over: *the chief engineer said that Nair directed
  him…*, and the presumption of innocence must be restated in the same passage (KB-501).

## E3. Case posture as of 2026-08-23 — **check this again before publication**

| id | fact | source |
|---|---|---|
| KB-801 | The indictment was **returned by a grand jury on 8 April 2026** and **unsealed 12 May 2026**. It runs to **18 counts** | S9 `[SECONDARY]` |
| KB-802 | The US Attorney for Maryland is **Kelly O. Hayes**; prosecutors are AUSAs Phelps, Mostoufi and Phillips with ECS Trial Attorney Leigh Rendé | S4, S8 |
| KB-803 | **No arraignment, plea or trial date for the three indicted defendants has been established by any primary source read for this ledger.** Reporting indicates Nair is believed to be **in India** | S9 `[SECONDARY]` |
| KB-804 | **Synergy Marine Group issued a statement on 13 May 2026 calling the charges baseless and disputing the characterisation of the flushing pump.** **The defence position must appear in the film** | S9 `[SECONDARY — get Synergy's own words from Synergy before broadcasting them]` |
| KB-805 | The NTSB's full report is **MIR-25-40**, and the bridge-vulnerability companion is **MIR-25-10**, both dated **18 November 2025**. This **answers KB-207**: the complete report exists | S10 |
| KB-806 | The Port of Baltimore was closed for **77 days** | S9 `[SECONDARY — confirm against a federal source]` |

## Sources added 2026-08-23

| id | document | date | url |
|---|---|---|---|
| S8 | DOJ ENRD **Environmental Crimes Bulletin — June 2026** (published 24 July 2026), entry *United States v. Karthikeyan Deenadayalan* | 2026-06/07 | https://www.justice.gov/enrd/blog/environmental-crimes-bulletin-june-2026 |
| S9 | Press reporting (Daily Record, The Banner, MinnLawyer, Environment+Energy Leader) | 2026-05/06 | **secondary — every row citing S9 is marked and must be re-sourced** |
| S10 | NTSB investigation page DCA24MM031, listing MIR-25-40 and MIR-25-10 | 2025-11-18 | https://www.ntsb.gov/investigations/Pages/DCA24MM031.aspx |

**Fetching trap, recorded for the next session.** `justice.gov/opa/*` can be read with `curl`
and a browser user-agent. **`justice.gov/usao-*` cannot** — it returns an Akamai `bm-verify`
interstitial instead of the page, and the DPA press release lives there. The ENRD monthly
bulletin carried the same facts and was readable.

## F. Contradictions between official sources — do not silently pick one

| id | the conflict | resolution |
|---|---|---|
| KB-601 | **The ship's length is given three ways by three official documents**: **947 feet** (S1, NTSB preliminary), **984 feet** (S2, NTSB press release), **900 feet** (S4, DOJ indictment release) | **Do not state a length.** If one is needed, cite the document with it. This is exactly the kind of number a viewer checks |
| KB-602 | S1 (2024) says the NTSB was **still investigating** the electrical configuration after the first in-port blackout and its effect on the accident voyage. S2 (2025) states a probable cause | The preliminary report is superseded on cause. **Use S1 for the timeline, S2 for the cause.** Never quote S1 as the Board's conclusion |
| KB-603 | S2's probable cause is **a loose signal wire on a terminal block, from wire-label banding**. S4's allegation is **a loose wire in a high-voltage switchboard** for the first loss, and a **flushing-pump alteration** for the second | These are **not the same claim**. The Board explains the first blackout; the indictment adds an allegation about why the ship did not recover. **Keep them apart in the script** |

## G. `forbidden_claims` — the exact sentences this film may not say

Copied verbatim into `episode_spec.v001.json`.

1. That Synergy Marine, Synergy Maritime or Radhakrishnan Karthik Nair **caused** the collapse. Charged is not convicted (KB-501)
2. That anyone **lied** to the NTSB. The charge is false statements and obstruction; a charge is not a finding (KB-402, KB-409, KB-501)
3. That the ship **would** have cleared the bridge with the proper pumps. The indictment **alleges** it (KB-408)
4. That the settlement was an **admission** of anything (KB-305)
5. That the Maryland Transportation Authority **knew** the bridge was vulnerable. The Board found the opposite — that they were **likely unaware** (KB-205)
6. Any **length in feet** for the Dali stated as fact (KB-601)
7. That the **four blackouts** all happened before the ship sailed. Two were in port on 25 March, two under way on 26 March (KB-101…KB-113)
8. That the **complete NTSB report** has been published, unless that is checked first (KB-207)
9. Any cause of death, injury detail, or identification of the six men beyond what an official record states

## H. Still to do before the script is final

- [ ] Open **S3** (Board Summary), **S6** (limitation docket) and **S7** (MIR-25-10) line by line and clear every `[UNREAD SOURCE]`
- [ ] Establish whether the **complete NTSB report** was published after 18 November 2025 (KB-207)
- [ ] Establish the **current posture of the criminal case** — arraignment, pleas, trial date, or any dismissal since 12 May 2026. **A live case can move between writing and publication; this is the ⛔-11 risk the channel has hit before**
- [ ] Decide, as an owner call, **whether the six men are named**. They were real people and their families are alive. The channel's rule bars their likeness; naming is a separate decision and is not made here
- [ ] Confirm the **MDTA duty officer's order at 01:27:53** — what exactly was ordered, and whether the bridge was closed to traffic before contact
