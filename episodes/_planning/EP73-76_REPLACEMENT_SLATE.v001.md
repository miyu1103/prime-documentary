# EP73–76 REPLACEMENT SLATE v001 — 51 candidates, all through the rubric

**Built 2026-08-20.** Status: **PROPOSAL.** Nothing approved, nothing scheduled, no build file touched.

## Why this file exists

Three of the five themes the owner approved on 2026-08-19 failed the channel's own demand test the
same night. Measured with `scripts/topic_demand_probe.py`, receipt
`measurements/TOPIC_DEMAND_PROBE_EP72_76_FINALISTS.v001.json`:

| approved theme | median views | ≥100k on N channels | R-36 | verdict |
|---|---|---|---|---|
| Lac-Mégantic | 110,747 | 5 channels | PASS | **kept — EP72** |
| GM ignition switch | **145** | 2 videos, **1 channel** | FAIL | replaced |
| Merrimack Valley | 4,565 | **1 channel** | FAIL | replaced |
| Massachusetts drug lab | **581** | **0 channels** | FAIL | replaced |
| El Faro | not yet probed | — | — | pending |

GM scored 118 (FLAGSHIP) on the rubric and measures at a median of 145 views. That is the third time
this project has recorded the same lesson (`TOPIC_PIPELINE.v005` §1.2: Fierle, Delphi): **the rubric
cannot see demand or incumbents, and a premise that is excellent on paper can have no audience.**

One inference worth carrying: GM's failure is evidence about a *lane*, not only a topic. "Car-defect
scandal" as a documentary genre measured weak here, so Takata, Firestone, CPAP, talc and 3M below are
NOT safe replacements on rubric score alone — they are exactly the rows that must be measured before
anyone believes them.

## The two criteria, and where each candidate stands

1. **Rubric** — `config/pd_planning_os.v002.json` via the same arithmetic as `scripts/score_premise.py`
   (raw of 120 → ×100/120 → +5 per bonus). **All 51 rows below pass**: 9 FLAGSHIP, 35 PRIORITY,
   7 PRODUCTION, zero RESERVE, zero REJECT.
2. **Demand ÷ incumbent** — not yet measured for any row. A one-shot scheduled task
   `PD-SlateProbe-Once` runs every query below at **16:02 JST on 2026-08-20**, two minutes after the
   YouTube quota resets, in batches of 12, writing
   `measurements/TOPIC_DEMAND_PROBE_SLATE50_batch*.json`.

**Quota trade-off, stated rather than hidden:** 51 queries cost 5,151 of the day's 10,000 units. The
16:20 Shorts push sizes itself from what is left, so **today it will publish about 3 Shorts instead of
5**. The Shorts backlog is 58 with the calendar already filled to 2026-08-24, so a one-day slowdown
costs nothing that matters; choosing three episodes wrongly costs weeks.

## Decision rule when the measurements land

Applied in this order, from `TOPIC_PIPELINE.v005` §1:

1. **R-36 two-channel test** — at least two *distinct* channels above 100k views on the topic.
   Absence of competitors is equally evidence of absence of demand (Fierle).
2. **demand ÷ incumbent** — reject where a definitive film exists at 3M+ views, as with Boeing MAX and
   D.B. Cooper. Lac-Mégantic's profile (median 110k, biggest long-form 770k) is the accepted shape;
   Surfside was greenlit at median 347k with a 916k incumbent.
3. Prefer, among survivors, the ones whose 30-minute slot is *empty* — a topic whose biggest long-form
   is a 16-minute explainer has an audience and no documentary.
4. Lane spacing: EP72 is Lac-Mégantic (rail/industrial), so the three replacements should not all be
   industrial disasters.

## The 51 candidates

Ordered by rubric score. None appears in the 71-episode inventory. `query` is written in viewer
language, not ours — the GM probe used our phrasing and may have under-measured it, so GM and the drug
lab are re-queried in the run as a control on the instrument.

| # | score | verdict | series | premise | the contradiction | probe query |
|---|---|---|---|---|---|---|
| 1 | 119 | FLAGSHIP | S03 | **The Airbag Was Built to Save Him. It Fired Metal Into His Neck.** | The device that exists only to prevent injury became the injury, and the company knew before it shipped. | `takata airbag recall deaths documentary` |
| 2 | 116 | FLAGSHIP | S15 | **They Set Fire to the Chemicals to Prevent an Explosion That Was Not Coming.** | The vent-and-burn that poisoned the valley was ordered on the basis of a reading the manufacturer's own experts were never asked about. | `east palestine train derailment documentary` |
| 3 | 114 | FLAGSHIP | S29 | **The Records Said the Pipe Had No Seam. The Seam Is What Failed.** | The utility's own paperwork described a pipe that did not exist under the street. | `san bruno pipeline explosion documentary` |
| 4 | 113 | FLAGSHIP | S31 | **Two Companies Had the Same Data. Each Said It Was the Other's Fault.** | Both firms could see the deaths in their own numbers and each blamed the other's product. | `firestone ford explorer tire scandal documentary` |
| 5 | 112 | FLAGSHIP | S38 | **Everyone Read the Same Impossible Number and Agreed on an Explanation.** | The test that says the well is sealed returned a failure, and eleven people accepted a story instead. | `deepwater horizon negative pressure test documentary` |
| 6 | 110 | FLAGSHIP | S38 | **The Door Plug Left the Aircraft at 16,000 Feet. Four Bolts Were Never Installed.** | There is no paperwork for the removal, so officially the bolts were never taken out -- and the plug still departed the aircraft. | `alaska airlines door plug blowout documentary` |
| 7 | 110 | FLAGSHIP | S29 | **Employees Opened 3.5 Million Accounts Nobody Asked For. The Ones Who Refused Were Fired.** | The bank punished the staff who would not commit the fraud and promoted the ones who did. | `wells fargo fake accounts scandal documentary` |
| 8 | 110 | FLAGSHIP | S17 | **The Sirens Never Sounded. The Island Has the Largest Warning System in the World.** | Hawaii built the world's biggest outdoor siren network and on the day it was needed nobody turned it on. | `lahaina maui wildfire documentary` |
| 9 | 110 | FLAGSHIP | S17 | **The Safety Valve Was Removed in 1979 and Never Replaced.** | A gas well beside a suburb had no way to be shut off underground and nobody was required to notice. | `aliso canyon gas leak documentary` |
| 10 | 109 | PRIORITY | S10 | **One Unapplied Patch Exposed 147 Million People. None of Them Were Customers.** | The people whose lives were exposed had never chosen to have a file at the company that lost it. | `equifax data breach documentary` |
| 11 | 109 | PRIORITY | S11 | **The Truck in the Video Was Rolling Downhill.** | The company's proof that the vehicle worked was a shot of it with no engine running at all. | `nikola trevor milton fraud documentary` |
| 12 | 108 | PRIORITY | S32 | **The Engineers Asked Not to Launch. They Were Told to Take Off Their Engineering Hat.** | The people who said it would fail were overruled by being asked to answer as managers instead. | `challenger disaster o ring documentary` |
| 13 | 108 | PRIORITY | S17 | **The Steel Plates Were Half the Required Thickness From the Day It Opened.** | Forty years of inspections were looking for damage on a bridge that had been wrong since it was drawn. | `i 35w minneapolis bridge collapse documentary` |
| 14 | 108 | PRIORITY | S30 | **The Study Said the Wave Could Reach 15 Metres. The Wall Was Built for 5.7.** | The company's own commissioned estimate of the tsunami was filed and not acted on. | `fukushima daiichi disaster documentary` |
| 15 | 107 | PRIORITY | S15 | **The Refrigeration Was Switched Off to Save $37 a Day.** | The safety systems were all shut down for cost, and each one would have stopped the gas alone. | `bhopal gas disaster documentary` |
| 16 | 107 | PRIORITY | S31 | **The Company Split in Two So One Half Could Go Bankrupt.** | A profitable company created a subsidiary purely to hold the liability and put it into bankruptcy. | `johnson johnson talc lawsuit documentary` |
| 17 | 107 | PRIORITY | S31 | **The Alarm and the Gauge Both Worked. Neither Was Connected to Anything That Would Stop It.** | The refinery's instruments reported the tower was filling and no system existed to act on it. | `texas city refinery explosion 2005 documentary` |
| 18 | 106 | PRIORITY | S38 | **The Regulator Extended the Grease Interval. The Jackscrew Wore Through.** | The maintenance schedule that failed had been lengthened, on paper, by the agency that certifies safety. | `alaska airlines flight 261 crash documentary` |
| 19 | 106 | PRIORITY | S32 | **The Boxes Were Labelled Empty. They Were Full of Live Oxygen Generators.** | A contractor certified the cargo as empty because the form had no box for what was actually inside. | `valujet flight 592 crash documentary` |
| 20 | 106 | PRIORITY | S31 | **The Tanker Had No Double Hull Because the Industry Said It Was Not Needed.** | The spill response plan promised equipment that was buried under snow in a warehouse. | `exxon valdez oil spill documentary` |
| 21 | 106 | PRIORITY | S03 | **The Machine Prescribed to Keep Him Breathing Was Shedding Foam Into the Air.** | The device treating his sleep apnoea was putting particles into the only air he could breathe. | `philips cpap recall foam documentary` |
| 22 | 105 | PRIORITY | S30 | **Two Pilots Earned Less Than the Cabin Crew. The Law Changed Only After 50 Died.** | The industry's answer to fatigue was a rule that took a crash and a decade of families lobbying to write. | `colgan air flight 3407 crash documentary` |
| 23 | 105 | PRIORITY | S38 | **The Pitot Tubes Iced for 30 Seconds. The Aeroplane Fell for Four Minutes.** | The aircraft was flyable the entire way down and the crew never knew which of them was flying it. | `air france 447 crash documentary` |
| 24 | 105 | PRIORITY | S30 | **They Photographed the Wing and Cancelled the Request. Nothing Could Be Done Anyway.** | The decision not to look was justified by the belief that looking would not have helped. | `columbia shuttle foam strike documentary` |
| 25 | 105 | PRIORITY | S17 | **The Software That Prevents Catastrophic Failure Caused One, Worldwide, in 78 Minutes.** | An update meant to protect machines from attack disabled 8.5 million of them at once. | `crowdstrike outage global it failure documentary` |
| 26 | 105 | PRIORITY | S11 | **1.9 Billion Euros Were Missing. The Auditors Had Signed for Years.** | The money had never existed, and the regulator investigated the journalists instead of the company. | `wirecard scandal documentary` |
| 27 | 105 | PRIORITY | S13 | **The App Removed the Buy Button and Left the Sell Button.** | The platform that promised to democratise investing stopped its users buying while professionals continued. | `robinhood gamestop trading halt documentary` |
| 28 | 105 | PRIORITY | S29 | **The Epoxy Was Known to Creep. Three Tons of Ceiling Came Down on a Car.** | The adhesive holding the tunnel roof was the wrong kind for a load that never moves. | `big dig ceiling collapse boston documentary` |
| 29 | 104 | PRIORITY | S17 | **A Slip of Paper Said the Pump Was Safe to Start. 167 Men Died.** | The permit-to-work system that existed to make the platform safe was the mechanism that destroyed it. | `piper alpha disaster documentary` |
| 30 | 104 | PRIORITY | S17 | **The Ship Lost Power Twice Before It Left. The Bridge Had No Modern Protection.** | The pier protection was designed for the ships of 1977 and the ship that hit it was four times heavier. | `baltimore key bridge collapse documentary` |
| 31 | 104 | PRIORITY | S20 | **The Bank Announced It Had Solved the Problem. $42 Billion Left in a Day.** | The disclosure written to reassure depositors is what caused them all to leave at once. | `silicon valley bank collapse documentary` |
| 32 | 104 | PRIORITY | S30 | **He Sent a Text 22 Seconds Before Impact. The Technology to Stop It Existed in 1990.** | The system that would have stopped the train had been recommended for decades and mandated only after 25 died. | `chatsworth metrolink collision documentary` |
| 33 | 104 | PRIORITY | S29 | **The Track Circuit Stopped Seeing the Train That Was Sitting on It.** | The signalling system reported clear track because the failure mode it had was one nobody tested for. | `washington metro fort totten crash documentary` |
| 34 | 104 | PRIORITY | S21 | **97 People Were Unlawfully Killed. It Took 27 Years and 164 Altered Statements to Say So.** | The police who caused the crush wrote the account that blamed the dead for it. | `hillsborough disaster documentary` |
| 35 | 104 | PRIORITY | S25 | **The Course Was Changed for a Gesture. The Evacuation Came an Hour Late.** | The ship was steered off its programmed line to wave at an island, and then nobody ordered abandon ship. | `costa concordia disaster documentary` |
| 36 | 104 | PRIORITY | S17 | **The Plant Stored 30 Tons of Ammonium Nitrate Next to a School.** | The facility was inspected by four agencies and none of them was responsible for the explosive risk. | `west texas fertilizer plant explosion documentary` |
| 37 | 103 | PRIORITY | S15 | **The Owners Were Evacuated. The Shoppers Were Told It Was Safe.** | The people who knew the building was failing left it, and told everyone else to keep working. | `sampoong department store collapse documentary` |
| 38 | 103 | PRIORITY | S32 | **The Announcement Told Them to Stay in Their Cabins. The Crew Left First.** | The instruction that killed the passengers was the standard instruction, given by people already leaving. | `sewol ferry disaster documentary` |
| 39 | 103 | PRIORITY | S17 | **A State Capital Could Not Produce Drinking Water. Every Warning Had Been Filed.** | The plant that failed had been declared failing in writing for years by the people who ran it. | `jackson mississippi water crisis documentary` |
| 40 | 102 | PRIORITY | S29 | **The Computer Said Climb. The Controller Said Descend. Both Were Doing Their Job.** | Two safety systems built to prevent the same collision gave opposite instructions and caused it. | `uberlingen midair collision documentary` |
| 41 | 102 | PRIORITY | S31 | **The Earplug Was Too Short to Seat. The Test That Showed It Was Never Filed.** | The protection issued to soldiers failed in the one condition it was bought for, and the company had measured it. | `3m earplug lawsuit military hearing loss documentary` |
| 42 | 101 | PRIORITY | S32 | **He Said the Fuselage Sections Did Not Fit. He Was Found Dead Before He Finished Testifying.** | The company's answer to the gaps was to record them as within tolerance. | `boeing whistleblower 787 documentary` |
| 43 | 101 | PRIORITY | S21 | **The Doors Were Locked to Stop the Workers Stealing.** | The measure taken to protect the company's property is what prevented its workers from leaving. | `triangle shirtwaist factory fire documentary` |
| 44 | 100 | PRIORITY | S10 | **A Counter Reached 40 Million and Stopped. Nobody Could Call 911 for Six Hours.** | The number that always works stopped working and no one in seven states was told. | `911 outage nationwide failure documentary` |
| 45 | 99 | PRODUCTION | S14 | **The Hotel Was Built Without Sprinklers Because They Were Not Required Above the Casino.** | The building met every code that applied to it and the smoke killed people twenty floors up. | `mgm grand fire las vegas 1980 documentary` |
| 46 | 99 | PRODUCTION | S08 | **A Fragment of Circuit Board the Size of a Fingernail Decided Who Did It.** | The entire case rested on one chip whose provenance is still contested in court. | `lockerbie bombing investigation documentary` |
| 47 | 97 | PRODUCTION | S29 | **Nobody's Job Was to Check the Bow Doors Were Shut.** | Every person assumed the door was someone else's responsibility and the ship sailed open to the sea. | `herald of free enterprise disaster documentary` |
| 48 | 97 | PRODUCTION | S30 | **One Link Failed and the Whole Bridge Went Into the River in 60 Seconds.** | The bridge had no redundancy at all, and no inspection then existing could have found the crack. | `silver bridge collapse 1967 documentary` |
| 49 | 96 | PRODUCTION | S10 | **The Machine Said the Dose Was Zero. It Had Just Delivered a Hundred Times Too Much.** | The interlock that made the machine safe was removed because the software was trusted to do it. | `therac 25 radiation overdose documentary` |
| 50 | 96 | PRODUCTION | S14 | **The Room Held 900. There Were 1,300 Inside and One Way Out.** | The club was inspected and licensed while carrying triple the people its exits could clear. | `beverly hills supper club fire documentary` |
| 51 | 95 | PRODUCTION | S15 | **The Visor Was Found a Kilometre From the Wreck. The Inquiry Was Closed Anyway.** | The physical evidence that would decide the cause was left on the seabed and the site declared a grave. | `estonia ferry sinking documentary` |

## Control rows added to the probe run

Two rows re-measure the instrument rather than a candidate:

- `57 cent part gm recall deaths` — GM under a viewer's phrasing, to test whether the 145-view median
  was the topic or the query.
- `annie dookhan chemist scandal` — the drug lab without the word "documentary".

If either returns a materially different distribution, the failure was the instrument and the
2026-08-19 rejection has to be re-read.
