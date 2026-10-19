# Repackaging Wave 2 - the 20 highest-impression films (v001)

**Status: PROPOSAL. Nothing was written to YouTube.** Titles and thumbnails are an owner approval
gate; this document exists to be approved or rejected line by line.

| | |
|---|---|
| authored | 2026-08-12 |
| scope | the **top 20** public long-forms by 28-day thumbnail impressions |
| boundary | rank 20 = `020-gardner` at **712** impressions; rank 21 = `007-riley` at **687**. Clean cut, no tie. The other 37 belong to the sibling agent. |
| rules | `config/pd_planning_os.v002.json` -> `title`, `thumbnail`; `docs/PD_EDITORIAL_DIRECTION.v002.md` |
| measurement | `data/content_genome.v001.jsonl`, captured 2026-08-11 |
| machine form | `runs/repackaging/wave2_top20.v001.json` |

These 20 films hold **48,263 impressions**, **1,557 lifetime views** and **7 subscribers** between them - 
82% of the catalogue's 28-day exposure (48,263 of 58,973), converting at a median CTR of **1.24%**
against a 6% north star.

---

## 0. Read this before approving anything

**A title experiment is running right now, and this wave would destroy it.**

On 2026-08-10, 39 back-catalogue titles were rewritten and verified
(`episodes/_planning/measurements/TITLE_EXPERIMENT_RECEIPT.v001.md`). Two consequences follow, and
neither is optional:

1. **15 of these 20 were retitled on 2026-08-10** - one day before the CTR window closed. The CTR
   quoted against them is the score of the *previous* title. The title now on the page has
   effectively zero days of measurement. Rewriting it now overwrites an unread experiment.
2. **The other 5 are the protected control arm.** `048-glover`, `041-thompson`, `043-caniglia`,
   `034-rolin` and `042-young` are all on the receipt's explicit list: *"Do not retitle any of these
   before 2026-09-07 or the experiment loses its comparison."*

So all twenty are locked, from both ends. The receipt also records that PD's own data has **twice
failed to show that title shape predicts CTR**, and it sets the read date at **2026-09-07** with
pre-declared WIN / NULL / LOSS thresholds.

**Therefore the recommendation is not "apply this wave".** It is:

| | |
|---|---|
| **approve the copy now** | so it is written, fact-checked and ready - this is the part that costs zero production time |
| **apply titles on 2026-09-07** | after the experiment is read, and only for the rows the read does not vindicate |
| **one exception ships today** | `042-young` - thumbnail only, title untouched |

The exception is not my invention. Receipt section 7 designates `042-young` the clean test: a fully
rule-compliant title carrying the **worst CTR of any high-impression long-form (0.43%)**, deliberately
left untouched, with the instruction *"Change only its thumbnail and nothing else; if CTR moves, the
title rules were never the lever."* That experiment has been waiting on a thumbnail nobody has drawn.
Row 15 draws it.

---

## 1. The recurring defect - this matters more than any single rewrite

### 1.1 The thumbnail is used as a second printing of the title

This is the pattern across the twenty. **10 of the 20 thumbnails reuse a content word from their own
title.** The v002 rule says the two must form one sentence and never repeat each other; PD is spending
both slots saying one thing.

The worst are near-verbatim duplicates:

| film | title | thumbnail | overlap |
|---|---|---|---|
| `041-thompson` | They Hid the Evidence That Proved Him Innocent - He Spent 14 Years on Death Row | THEY HID THE PROOF / 14 YEARS ON DEATH ROW | **83%** |
| `043-caniglia` | Police Came for a Welfare Check and Left With His Guns | IT WAS A WELFARE CHECK / THEY TOOK HIS GUNS | **75%** |
| `034-rolin` | They Took His Life Savings at the Airport - No Charges, No Crime | NO CRIME. NO CHARGES. / THEY TOOK HIS $82,000 | **71%** |

**And it tracks with CTR.** Pairing each thumbnail against the title that was *actually live during
the measurement window* - not the one live today, a distinction I got wrong on the first pass:

| group | n | mean CTR | weighted CTR | median |
|---|---|---|---|---|
| thumbnail shares **no** word with the title | 11 | **1.99%** | 1.78% | 1.81% |
| thumbnail repeats a title word | 9 | **1.25%** | 1.26% | 1.15% |

It holds inside both impression halves - 1.99% vs 1.10% in the high half, 1.99% vs 1.37% in the low
half - so it is not an impressions artefact. The ~0.74 pp gap clears the channel's own +/-0.30 pp
noise floor.

**Stated honestly:** n=20, observational, and CTR here is a blend across two title regimes. This is
suggestive, not proven. My first computation used *today's* titles and produced a 1.46 pp gap; that
number was an artefact of measuring a title that was not on the page during the window, and it is not
the number above. The v002 sentence rule is the cheapest thing on this list to test and the only
defect in the set with any supporting signal at all.

### 1.2 Four more defects, each mechanically countable

| # | defect | count | why it costs |
|---|---|---|---|
| D2 | **the contradiction sits below the fold** - 19 of 20 titles are two-clause; the second clause starts at char 44 (median) and titles run 62-86 chars | 19/20 | on mobile browse the expectation violation is truncated away, leaving only the setup |
| D3 | **the title opens on a rule or an institution, not a person** - `047-atwater` ("A Seatbelt Ticket Carried..."), plus `048-glover`, `032-carsearch`, `042-young`, `043-caniglia`, `016-titan` all opening on the institution | 6/20 | v002 inverts this explicitly: person -> abnormal event -> system, never system -> person |
| D4 | **the thumbnail carries a figure the title does not** - `023-swartz` (35), `034-rolin` ($82,000), `042-young` (2019), `047-atwater` ($50), `020-gardner` (36) | 5/20 | exactly backwards from the canon pair, which puts `$86,900` in the title and `0 CHARGES` in the thumbnail; the number is the strongest asset and it is being spent in the smaller slot |
| D5 | **zero evidence-kind thumbnails** - 13 scene, 5 face-reaction, 2 object | **0/20** | the house shift the owner asked for has not started anywhere in the top 20 |

**One thing I could not support.** I expected AI faces to be the drag. They are not, in this data:
face-thumbnail films average 1.27% and non-face 1.87%, but weighted by impressions they are 1.65% vs
1.60% - indistinguishable, and the channel's second-best CTR (`006-terry`, 3.12%) is a face. The move
to evidence thumbnails is a sound editorial directive; it is **not** something PD's numbers currently
demonstrate, and it should not be sold as if it were.

---

## 2. The approval table

Approve, reject or amend per row. `HOLD` means the live copy is better than anything I wrote, or is
protected by the running experiment.

| # | slug | imp | CTR | when | recommended action | recommended title | thumb |
|---|---|---:|---:|---|---|---|---|
| 1 | `035-hinders` | 7,338 | 1.01% | 2026-09-07 | apply Broad + thumb | The IRS Took $32,820 From Her Diner. She Was Never Charged. | **B** WITHOUT PREJUDICE |
| 2 | `037-florence` | 6,341 | 0.74% | 2026-09-07 | apply Broad + thumb | He Had the Receipt in His Hand. He Still Spent Six Days in Jail. | **B** WARRANT NEVER CLEARED |
| 3 | `016-titan` | 4,757 | 2.96% | 2026-09-07 | keep title, new thumb | *(live title kept)* | **B** MINOR TO CATASTROPHIC |
| 4 | `006-terry` | 4,137 | 3.12% | never (protect) | **HOLD** - do not touch | *(live title kept)* | **A** STILL LEGAL? |
| 5 | `048-glover` | 3,266 | 1.81% | 2026-09-07 | apply Broad + thumb | A Deputy Ran a Plate and Pulled Him Over. He Never Saw the Driver. | **B** LICENSE: REVOKED |
| 6 | `029-hinton` | 3,037 | 1.28% | 2026-09-07 | apply Broad + thumb | His Lawyer Thought the State Would Pay Only $1,000. He Lost 30 Years. | **B** THE BULLET NEVER MATCHED |
| 7 | `041-thompson` | 2,871 | 1.15% | 2026-09-07 | apply Broad + thumb | A Jury Gave Him $14 Million. Five Justices Took Every Dollar Back. | **B** AWARD: $0 |
| 8 | `021-dbcooper` | 2,049 | 2.29% | 2026-09-07 | apply Broad + thumb | He Took $200,000, Jumped Out the Back of a 727, and Was Never Identified. | **B** SEWN SHUT |
| 9 | `043-caniglia` | 1,912 | 1.20% | 2026-09-07 | apply Broad + thumb | His Wife Asked Police to Check on Him. They Left With His Guns. | **B** NO WARRANT ISSUED |
| 10 | `030-cotton` | 1,846 | 0.76% | 2026-09-07 | apply Broad + thumb | She Studied His Face So She Could Not Be Wrong. He Lost 11 Years. | **B** 6 PHOTOS |
| 11 | `023-swartz` | 1,506 | 0.80% | 2026-09-07 | apply Broad + thumb | Prosecutors Turned Four Charges Into Thirteen. The Deal Was Six Months. | **C** NO VICTIM ASKED |
| 12 | `005-madoff` | 1,490 | 1.81% | 2026-09-07 | apply Broad + thumb | He Warned the SEC for a Decade. Its Own Watchdog Said the Warnings Were Credible. | **B** RED FLAGS, IN WRITING |
| 13 | `032-carsearch` | 1,318 | 3.95% | 2026-09-07 | keep title, new thumb | *(live title kept)* | **B** UNDER THE TARP |
| 14 | `034-rolin` | 1,165 | 0.86% | 2026-09-07 | apply Broad + thumb | His Daughter Carried His $82,000 Through the Airport. Agents Took It All. | **B** 0 CHARGES |
| 15 | `042-young` | 1,151 | 0.43% | **today** / 09-07 | **thumb NOW**, title 09-07 | Chicago Paid Her $2.9 Million and Never Said Anyone Did Anything Wrong. | **C** A CHECK, NO VERDICT |
| 16 | `047-atwater` | 999 | 0.40% | 2026-09-07 | apply Broad + thumb | The Most She Could Be Fined Was $50. She Was Handcuffed and Booked. | **B** SEAT BELT, FINE ONLY |
| 17 | `022-milken` | 880 | 1.70% | 2026-09-07 | apply Broad + thumb | He Was Charged on 98 Counts and Pleaded to Six. A Pardon Closed the Rest. | **B** 92 DROPPED |
| 18 | `014-lange` | 750 | 4.40% | never (protect) | **HOLD** - do not touch | *(live title kept)* | **A** YOUR DOOR? |
| 19 | `033-tyler` | 738 | 1.22% | 2026-09-07 | apply Broad + thumb | A County Sold a 94-Year-Old's Home Over a $2,300 Debt. | **B** KEPT $40,000 |
| 20 | `020-gardner` | 712 | 1.26% | 2026-09-07 | apply Broad + thumb | Two Men in Police Uniforms Took 13 Paintings in 81 Minutes. | **B** $10M REWARD |

Every recommended title + thumbnail pair was machine-checked for word repetition before this document
was written. Three of my own drafts failed that check and were rewritten.

---

## 3. Film by film

### 1. `035-hinders` - 7,338 impressions at 1.01%

> **Current title:** She Banked Under $10,000 Because That Is What the Till Held. The IRS Took $32,820.  
> **Current thumbnail:** SHE FOLLOWED THE RULES. - *scene*

254 lifetime views | 2 subs | AVD 10.11% | 19 min | TREATED 2026-08-10 - current title has ~0 days of measurement

*The CTR above belongs to the title that was live during the window:* "Following the deposit rule is what made her a suspect"

**What is wrong with it.** The first 46 characters explain the mechanism of her deposits before the title reaches any consequence. On mobile browse the cut lands before 'The IRS Took $32,820', so the contradiction -- the whole reason to click -- is below the fold. Highest impressions on the channel converting at 1.01%.

| | |
|---|---|
| **Core** | The IRS Emptied a 38-Year Diner's Account for Depositing Under $10,000. |
| **Broad** *(recommended shape)* | **The IRS Took $32,820 From Her Diner. She Was Never Charged.** |
| thumb A / human emotion | **SHE FOLLOWED THE RULES** - an older woman standing at the locked door of a small-town diner, keys still in hand |
| thumb B / evidence | **WITHOUT PREJUDICE** - the dismissal order, macro on the two typed words, the rest of the page falling out of focus **<- REC** |
| thumb C / symbolic / minimal | **NO CRIME ALLEGED** - a bank deposit slip and a rubber stamp, nothing else |
| **the one sentence** | The IRS Took $32,820 From Her Diner. She Was Never Charged.  +  WITHOUT PREJUDICE |
| **action** | apply proposed Broad title + selected thumbnail |
| **earliest apply** | 2026-09-07 - treated arm of the running title experiment; overwriting before the 2026-09-07 read destroys the measurement |

**Verified against the episode's own files:**

- $32,820.56 seized from the restaurant account - `episodes/PD-2026-035-hinders/03_script/script.en.v001.md`
  > an account balance ticks to $32,820.56, then hard-cuts to $0.00 with a 'SEIZED' overlay [CLM-0002]
- she was never charged with any crime - `episodes/PD-2026-035-hinders/03_script/script.en.v001.md L42`
  > She was never charged with a crime. Not money laundering, not tax evasion, no allegation that she had done anything with the money except earn it
- 38-year diner - `episodes/PD-2026-035-hinders/03_script/script.en.v001.md L20`
  > For thirty-eight years, a small cash restaurant sat off the lakes country of northwest Iowa.
- the case was dismissed WITHOUT PREJUDICE, conceding nothing - `episodes/PD-2026-035-hinders/03_script/script.en.v001.md L67`
  > It dismissed the case 'without prejudice.' In plain terms, that means it walked away without conceding a thing

### 2. `037-florence` - 6,341 impressions at 0.74%

> **Current title:** He Showed the Officer the Paid Receipt. He Was Jailed and Strip-Searched Twice.  
> **Current thumbnail:** HE ALREADY PAID. - *scene*

71 lifetime views | 0 subs | AVD 21.48% | 9 min | TREATED 2026-08-10 - current title has ~0 days of measurement

*The CTR above belongs to the title that was live during the window:* "He showed the officer the receipt and was arrested anyway"

**What is wrong with it.** 'Strip-Searched Twice' is the least clickable kind of specific -- it reads as a content warning, not a contradiction -- and the paid receipt, the actual expectation violation, is spent in clause one where nothing depends on it. 6,341 impressions at 0.74% is the single largest block of wasted exposure in the catalogue.

| | |
|---|---|
| **Core** | A Warrant Nobody Cleared Put Him in Two Jails. The Court Upheld It 5-4. |
| **Broad** *(recommended shape)* | **He Had the Receipt in His Hand. He Still Spent Six Days in Jail.** |
| thumb A / human emotion | **HE HAD PROOF** - a man's hand holding a folded payment letter at a car window, face out of frame |
| thumb B / evidence | **WARRANT NEVER CLEARED** - a monospaced database row on a patrol-car laptop, the status field lit **<- REC** |
| thumb C / symbolic / minimal | **PAID IN FULL** - a paper receipt alone on black |
| **the one sentence** | He Had the Receipt in His Hand. He Still Spent Six Days in Jail.  +  WARRANT NEVER CLEARED |
| **action** | apply proposed Broad title + selected thumbnail |
| **earliest apply** | 2026-09-07 - treated arm of the running title experiment; overwriting before the 2026-09-07 read destroys the measurement |

**Verified against the episode's own files:**

- he carried written proof the fine was paid and was arrested anyway - `episodes/PD-2026-037-florence/03_script/script.en.v001.md (hook)`
  > He was carrying the receipt. Proof, in his own hand, that the fine had already been paid. He showed it to the officer. He was arrested anyway.
- six days across two jails - `episodes/PD-2026-037-florence/03_script/script.en.v001.md`
  > One traffic stop. Two jails. Two searches. Six days.
- the warrant was never removed from the statewide database - `episodes/PD-2026-037-florence/01_research/research_pack.v001.md item 9`
  > paid the balance within ~a week, but the warrant was never removed from the statewide database (the clerical error)
- the Supreme Court decided it five to four - `episodes/PD-2026-037-florence/03_script/script.en.v001.md`
  > is where the Supreme Court, five to four, decided where that line falls at the jailhouse door

### 3. `016-titan` - 4,757 impressions at 2.96%

> **Current title:** OceanGate Fired the Man Who Wrote the Safety Report in 2018. Five People Dove in 2023.  
> **Current thumbnail:** THEY KNEW. - *scene*

194 lifetime views | 1 subs | AVD 35.09% | 36 min | TREATED 2026-08-10 - current title has ~0 days of measurement

*The CTR above belongs to the title that was live during the window:* "He called safety pure waste and dove anyway"

**What is wrong with it.** Two bare years do the work a consequence should do, and 'Five People Dove' is an action, not an outcome -- the viewer is asked to perform the subtraction themselves. At 2.96% this title is not the problem; the thumbnail is where the gain is.

| | |
|---|---|
| **Core** | OceanGate Never Certified the Hull. It Fired the Man Who Said So. |
| **Broad** *(recommended shape)* | **Three Dozen Experts Wrote 'Catastrophic' in 2018. Five People Died in 2023.** |
| thumb A / human emotion | **THEY KNEW.** - a lone silhouette at a podium, certain, warm key light against a cold hull |
| thumb B / evidence | **MINOR TO CATASTROPHIC** - the 2018 industry letter under a hard lamp, magnifier over the phrase **<- REC** |
| thumb C / symbolic / minimal | **NOT CERTIFIED** - an empty certification seal embossed on blank paper |
| **the one sentence** | OceanGate Fired the Man Who Wrote the Safety Report in 2018. Five People Dove in 2023.  +  MINOR TO CATASTROPHIC |
| **action** | KEEP live title, apply selected thumbnail |
| **earliest apply** | 2026-09-07 - treated arm of the running title experiment; overwriting before the 2026-09-07 read destroys the measurement |

**Verified against the episode's own files:**

- more than three dozen industry experts signed a 2018 letter - `episodes/PD-2026-016-titan/03_script/script.en.v001.md L~136`
  > That same spring, in 2018, an organization of the people who do this for a living -- submersible engineers, scientists, explorers, more than three dozen of them -- sent OceanGate a letter.
- the letter used the words 'from minor to catastrophic' - `episodes/PD-2026-016-titan/03_script/script.en.v001.md`
  > They wrote that the company's 'current experimental approach' could lead to outcomes ranging -- and these are their words -- 'from minor to catastrophic.' [CLM-0006]
- five people descended on 18 June 2023 and were lost - `episodes/PD-2026-016-titan/03_script/script.en.v001.md L205`
  > On the morning of the eighteenth of June, 2023, off the coast of Newfoundland, five people climbed into the Titan and began the descent
- David Lochridge was fired for the 2018 safety report - `episodes/PD-2026-016-titan/03_script/script.en.v001.md`
  > For raising those concerns, David Lochridge was fired. He took his worries to a federal workplace-safety agency. The company sued him. [CLM-0005]

### 4. `006-terry` - 4,137 impressions at 3.12%

> **Current title:** A Detective Watched Two Men Pace a Store Window. The Frisk He Ran Became National Law.  
> **Current thumbnail:** STILL LEGAL? - *scene*, AI face

160 lifetime views | 0 subs | AVD 14.97% | 11 min | TREATED 2026-08-10 - current title has ~0 days of measurement

*The CTR above belongs to the title that was live during the window:* "Police Can Stop and Frisk You Without Arresting You"

**What is wrong with it.** 'Became National Law' is an institutional abstraction where v002 requires a consequence to a person -- nothing in it says this reaches the viewer. But at 3.12% on 4,137 impressions this is the channel's second-best high-volume asset and the running experiment's highest-stakes single data point. Proposal is written; do not apply it.

| | |
|---|---|
| **Core** | Terry v. Ohio Built a Standard Below Probable Cause in 1968. |
| **Broad** *(recommended shape)* | **He Saw No Crime. The Frisk He Ran Made Every Street Stop Legal.** |
| thumb A / human emotion | **STILL LEGAL?** - hands raised against a store window, reflection of a plainclothes figure behind **<- REC** |
| thumb B / evidence | **A DOZEN TRIPS** - a hand-drawn surveillance tally on a detective's notepad |
| thumb C / symbolic / minimal | **NO WARRANT NEEDED** - an empty sidewalk and a single storefront window |
| **the one sentence** | A Detective Watched Two Men Pace a Store Window. The Frisk He Ran Became National Law.  +  STILL LEGAL? |
| **action** | KEEP live title and live thumbnail |
| **earliest apply** | 2026-09-07 - treated arm of the running title experiment; overwriting before the 2026-09-07 read destroys the measurement |

**Verified against the episode's own files:**

- Detective Martin McFadden, Cleveland, October 1963 - `episodes/PD-2026-006-terry/03_script/script.en.v001.md`
  > It is October 1963, in downtown Cleveland, Ohio. A plainclothes detective named Martin McFadden, thirty-nine years on the force [CLM-0005]
- about a dozen trips past the same window - `episodes/PD-2026-006-terry/03_script/script.en.v001.md`
  > Back and forth, the two of them, about a dozen trips in all
- the standard sits below probable cause - `episodes/PD-2026-006-terry/03_script/script.annotated.v001.json`
  > the Supreme Court built a second, lower standard -- 'reasonable suspicion' -- that lets police stop and frisk you without a warrant or probable cause

### 5. `048-glover` - 3,266 impressions at 1.81%

> **Current title:** Police Never Saw the Driver — the Supreme Court Let Them Stop Him Anyway  
> **Current thumbnail:** THEY RAN YOUR PLATE / STOPPED FOR A NAME - *face_reaction*, AI face

116 lifetime views | 0 subs | AVD 39.56% | 12 min | CONTROL - must not be retitled before 2026-09-07

**What is wrong with it.** An em-dash (0.43x in this repo's own CTR playbook), an institution as the subject of both clauses, and no person to attach to. The thumbnail then spends eight words on two competing subjects.

| | |
|---|---|
| **Core** | Kansas v. Glover: a Database Hit Alone Is Enough to Stop You, 8-1. |
| **Broad** *(recommended shape)* | **A Deputy Ran a Plate and Pulled Him Over. He Never Saw the Driver.** |
| thumb A / human emotion | **WHO IS DRIVING?** - a windscreen at dusk, driver's face deliberately unreadable, patrol lights behind |
| thumb B / evidence | **LICENSE: REVOKED** - the dashboard laptop screen, one record returned, cursor blinking **<- REC** |
| thumb C / symbolic / minimal | **A NAME, NO FACE** - a licence plate alone under a sodium lamp |
| **the one sentence** | A Deputy Ran a Plate and Pulled Him Over. He Never Saw the Driver.  +  LICENSE: REVOKED |
| **action** | apply proposed Broad title + selected thumbnail |
| **earliest apply** | 2026-09-07 - protected control arm of the running title experiment |

**Verified against the episode's own files:**

- the deputy ran the plate and never saw the driver - `episodes/PD-2026-048-glover/08_edit/captions.final.v001.srt`
  > The deputy types the truck's license plate into the laptop bolted to his dashboard. ... The deputy has never seen the driver's face.
- the registered owner's licence was revoked - `episodes/PD-2026-048-glover/08_edit/captions.final.v001.srt`
  > And Charles Glover's driver's license has been revoked.
- the Court upheld the stop 8-1 in April 2020 - `episodes/PD-2026-048-glover/08_edit/captions.final.v001.srt`
  > In April of 2020, the Supreme Court sided with Kansas. By a vote of eight to one, it held that the stop did not violate the Fourth Amendment.

> **!** ACCURACY LOCK from the script: the stop was UPHELD. Never call it illegal or unconstitutional in any packaging asset.

### 6. `029-hinton` - 3,037 impressions at 1.28%

> **Current title:** Alabama Held an Execution Date on Him for 30 Years. The Ballistics Were Wrong.  
> **Current thumbnail:** 30 YEARS INNOCENT - *scene*

52 lifetime views | 1 subs | AVD 24.66% | 12 min | TREATED 2026-08-10 - current title has ~0 days of measurement

*The CTR above belongs to the title that was live during the window:* "Alabama kept a date to kill him for 30 years"

**What is wrong with it.** 'Held an Execution Date on Him' is a construction no viewer says out loud, and 'The Ballistics Were Wrong' names a lab result when the story's actual outrage is a poverty mechanism -- a defence that could not buy an expert.

| | |
|---|---|
| **Core** | One Bullet Match Nobody Could Reproduce Held Him on Death Row for 30 Years. |
| **Broad** *(recommended shape)* | **His Lawyer Thought the State Would Pay Only $1,000. He Lost 30 Years.** |
| thumb A / human emotion | **A DATE TO DIE** - a wall calendar in a cell, one square ringed, light from a high slit window |
| thumb B / evidence | **THE BULLET NEVER MATCHED** - a comparison microscope stage, two bullets side by side, striations not aligning **<- REC** |
| thumb C / symbolic / minimal | **ONE EXPERT SHORT** - an empty witness chair |
| **the one sentence** | His Lawyer Thought the State Would Pay Only $1,000. He Lost 30 Years.  +  THE BULLET NEVER MATCHED |
| **action** | apply proposed Broad title + selected thumbnail |
| **earliest apply** | 2026-09-07 - treated arm of the running title experiment; overwriting before the 2026-09-07 read destroys the measurement |

**Verified against the episode's own files:**

- nearly thirty years on Alabama's death row; freed 3 April 2015 - `episodes/PD-2026-029-hinton/03_script/script.en.v001.md`
  > On April 3rd, 2015, Anthony Ray Hinton walked out of prison a free man, after nearly thirty years
- the lawyer WRONGLY BELIEVED a $1,000 cap limited expert funding -- there was no cap - `episodes/PD-2026-029-hinton/03_script/script.annotated.v001.json (thesis); the same lock appears in the script.en.v001.md GUARDRAILS header as the Japanese string '$1,000は弁護士の誤認・上限なし'`
  > convicted on a single junk-ballistics claim his court-appointed lawyer could not rebut because the lawyer wrongly believed a $1,000 cap limited expert funding
- the bullet match could not be reproduced - `episodes/PD-2026-029-hinton/03_script/script.en.v001.md`
  > to undo a one-hour verdict built on a bullet that never matched

> **!** BLOCKING: the $1,000 was the defence lawyer's mistaken belief, not a statutory cap. Any title must say 'thought' / 'believed'. A title reading 'His Lawyer Had $1,000' would be false and is prohibited by the episode's own guardrail.

### 7. `041-thompson` - 2,871 impressions at 1.15%

> **Current title:** They Hid the Evidence That Proved Him Innocent — He Spent 14 Years on Death Row  
> **Current thumbnail:** THEY HID THE PROOF / 14 YEARS ON DEATH ROW - *face_reaction*, AI face

41 lifetime views | 0 subs | AVD 29.03% | 12 min | CONTROL - must not be retitled before 2026-09-07

**What is wrong with it.** The thumbnail is a verbatim second printing of the title -- 83% word overlap, the worst pairing in the twenty. Two slots deliver one sentence twice, and the $14 million reversal, the only fact here a viewer has not seen before, appears in neither.

| | |
|---|---|
| **Core** | Connick v. Thompson: One Buried Report Was Not a 'Pattern', 5-4. |
| **Broad** *(recommended shape)* | **A Jury Gave Him $14 Million. Five Justices Took Every Dollar Back.** |
| thumb A / human emotion | **18 YEARS ERASED** - a man in his late forties at a prison gate, back to camera, morning light |
| thumb B / evidence | **AWARD: $0** - the judgment page, the damages line struck through **<- REC** |
| thumb C / symbolic / minimal | **NOTHING OWED** - a single sheet of lab paper face down |
| **the one sentence** | A Jury Gave Him $14 Million. Five Justices Took Every Dollar Back.  +  AWARD: $0 |
| **action** | apply proposed Broad title + selected thumbnail |
| **earliest apply** | 2026-09-07 - protected control arm of the running title experiment |

**Verified against the episode's own files:**

- a jury awarded him fourteen million dollars - `episodes/PD-2026-041-thompson/08_edit/captions.final.v001.srt L343`
  > They award John Thompson fourteen million dollars, one figure standing in for eighteen stolen years.
- the Supreme Court reversed 5-4 on 29 March 2011 and he received nothing - `episodes/PD-2026-041-thompson/08_edit/captions.final.v001.srt L391`
  > Five to four. The Court reverses. Every dollar, gone.
- fourteen years on death row, eighteen years in prison - `episodes/PD-2026-041-thompson/08_edit/captions.final.v001.srt L207`
  > John Thompson lived that for fourteen years on death row, eighteen behind bars in all.

> **!** FACT RE-CHECK for the film itself, not the packaging: captions L575 says 'eighteen years and fourteen death warrants'. That figure appears exactly once, is corroborated nowhere else in the episode's files, and the commonly reported count is seven execution dates. Do not put it in any title until the episode's own record is settled.

### 8. `021-dbcooper` - 2,049 impressions at 2.29%

> **Current title:** He Jumped Into a Storm With $200,000. Fifty Years On the FBI Cannot Name Him.  
> **Current thumbnail:** HE NEVER LANDED. - *scene*

116 lifetime views | 0 subs | AVD 34.77% | 30 min | TREATED 2026-08-10 - current title has ~0 days of measurement

*The CTR above belongs to the title that was live during the window:* "Fifty years later the FBI still cannot name him"

**What is wrong with it.** 'Fifty Years On' is a stiff literary connective doing the work a verb should do. Separately, the live thumbnail 'HE NEVER LANDED.' asserts an outcome the film explicitly refuses to assert -- its wording lock is unsolved and never found, not dead. That one is a correction, not a preference.

| | |
|---|---|
| **Core** | The FBI Suspended the Only Unsolved Skyjacking in U.S. History in 2016. |
| **Broad** *(recommended shape)* | **He Took $200,000, Jumped Out the Back of a 727, and Was Never Identified.** |
| thumb A / human emotion | **STILL UNNAMED** - an empty aisle seat near the rear stairs, briefcase on the floor |
| thumb B / evidence | **SEWN SHUT** - the training-rig parachute, stitching in macro, an evidence tag beside it **<- REC** |
| thumb C / symbolic / minimal | **CASE SUSPENDED** - an FBI file jacket, closed |
| **the one sentence** | He Took $200,000, Jumped Out the Back of a 727, and Was Never Identified.  +  SEWN SHUT |
| **action** | apply proposed Broad title + selected thumbnail |
| **earliest apply** | 2026-09-07 - treated arm of the running title experiment; overwriting before the 2026-09-07 read destroys the measurement |

**Verified against the episode's own files:**

- $200,000 in twenty-dollar bills and four parachutes - `episodes/PD-2026-021-dbcooper/03_script/script.en.v001.md L46`
  > Two hundred thousand dollars, in twenty-dollar bills. And four parachutes. [CLM-0003]
- Boeing 727, and he was never identified - `episodes/PD-2026-021-dbcooper/03_script/script.en.v001.md (WORDING LOCKS)`
  > UNSOLVED; never say it was solved. The man was never identified.
- the FBI suspended the case in 2016 - `episodes/PD-2026-021-dbcooper/03_script/script.en.v001.md L12`
  > 2016 = FBI SUSPENDED the case (suspended, NOT solved).
- one of the parachutes handed over was a sewn-shut training rig - `episodes/PD-2026-021-dbcooper/03_script/script.en.v001.md L81`
  > One of the parachutes the authorities handed him turned out to be a training rig, sewn shut, useless for a real jump.

> **!** PREMISE, not packaging: the protagonist is the perpetrator, there is no ordinary person and no system the viewer touches. It is the inverse of the v002 centre. It performs anyway on pure mystery (2.29%), so keep it -- but it does not model the format and should not be used as a template.

### 9. `043-caniglia` - 1,912 impressions at 1.20%

> **Current title:** Police Came for a Welfare Check and Left With His Guns — No Warrant  
> **Current thumbnail:** IT WAS A WELFARE CHECK / THEY TOOK HIS GUNS - *face_reaction*, AI face

41 lifetime views | 0 subs | AVD 25.98% | 13 min | CONTROL - must not be retitled before 2026-09-07

**What is wrong with it.** Verbatim duplication again: the title says welfare check and taken guns, and the thumbnail says the same two things in the same words (75% overlap). The trailing em-dash fragment 'No Warrant' is the payoff, tacked on where it cannot be read on mobile.

| | |
|---|---|
| **Core** | Caniglia v. Strom: 9-0, a Home Is Not a Car. |
| **Broad** *(recommended shape)* | **His Wife Asked Police to Check on Him. They Left With His Guns.** |
| thumb A / human emotion | **SHE JUST CALLED** - a phone face-up on a kitchen counter at night, porch light through the window |
| thumb B / evidence | **NO WARRANT ISSUED** - a property receipt on a clipboard, an evidence bag tag beside it **<- REC** |
| thumb C / symbolic / minimal | **TAKEN ANYWAY** - a closed front door, nothing else |
| **the one sentence** | His Wife Asked Police to Check on Him. They Left With His Guns.  +  NO WARRANT ISSUED |
| **action** | apply proposed Broad title + selected thumbnail |
| **earliest apply** | 2026-09-07 - protected control arm of the running title experiment |

**Verified against the episode's own files:**

- the wife called the non-emergency line for a welfare check - `episodes/PD-2026-043-caniglia/08_edit/captions.final.v001.srt`
  > So she calls the Cranston police, not 911, the non-emergency line, and asks them to do a welfare check.
- officers entered and removed his handguns, no arrest, no crime - `episodes/PD-2026-043-caniglia/03_script/script.en.v001.md`
  > how did her phone call end with officers inside his house, his handguns in an evidence bag, no warrant, and no crime?
- the Court was unanimous, nine to nothing - `episodes/PD-2026-043-caniglia/03_script/script.en.v001.md`
  > Justice Clarence Thomas writes for the Court, and the Court is unanimous. Nine to nothing.

### 10. `030-cotton` - 1,846 impressions at 0.76%

> **Current title:** She Memorised His Face on Purpose So She Would Be Certain. She Named the Wrong Man.  
> **Current thumbnail:** SHE WAS CERTAIN. - *scene*, AI face

24 lifetime views | 0 subs | AVD 21.36% | 12 min | TREATED 2026-08-10 - current title has ~0 days of measurement

*The CTR above belongs to the title that was live during the window:* "She memorized her attacker's face to be certain"

**What is wrong with it.** British spelling ('Memorised') on a channel whose audience is 92.5% male and overwhelmingly American; 83 characters before any consequence; and the man who actually lost the eleven years never appears in his own title. Live thumbnail repeated 100% of its content words from the title that was running.

| | |
|---|---|
| **Core** | A Six-Photo Array Turned a Tentative Memory Into Absolute Certainty. |
| **Broad** *(recommended shape)* | **She Studied His Face So She Could Not Be Wrong. He Lost 11 Years.** |
| thumb A / human emotion | **SHE WAS CERTAIN.** - a woman's eyes in courtroom light, absolutely steady |
| thumb B / evidence | **6 PHOTOS** - the photo array laid out on a detective's desk, one card slightly forward **<- REC** |
| thumb C / symbolic / minimal | **WRONG MAN** - a single mugshot card face-up on grey |
| **the one sentence** | She Studied His Face So She Could Not Be Wrong. He Lost 11 Years.  +  6 PHOTOS |
| **action** | apply proposed Broad title + selected thumbnail |
| **earliest apply** | 2026-09-07 - treated arm of the running title experiment; overwriting before the 2026-09-07 read destroys the measurement |

**Verified against the episode's own files:**

- eleven years of an innocent man's life - `episodes/PD-2026-030-cotton/08_edit/captions.final.v001.srt`
  > her certainty -- careful, well-meant, absolute -- had cost an innocent man eleven years of his life
- a six-photo lineup - `episodes/PD-2026-030-cotton/08_edit/captions.final.v001.srt`
  > Detectives laid out a lineup of six photos, and Thompson studied them
- DNA in 1995 cleared him and matched the real attacker - `episodes/PD-2026-030-cotton/03_script/script.annotated.v001.json`
  > DNA in 1995 cleared him and matched the real attacker

### 11. `023-swartz` - 1,506 impressions at 0.80%

> **Current title:** The Site He Downloaded From Dropped It. Prosecutors Filed 13 Felonies Anyway.  
> **Current thumbnail:** 35 YEARS FOR PAPERS. - *scene*

23 lifetime views | 0 subs | AVD 3.97% | 29 min | TREATED 2026-08-10 - current title has ~0 days of measurement

*The CTR above belongs to the title that was live during the window:* "The website he took from never wanted him charged"

**What is wrong with it.** 'The Site He Downloaded From' is a subject with no name and no face. But the packaging is not this film's problem: 3.97% average view duration on a 29-minute runtime is the worst engagement in the twenty by a factor of five, and no title recovers a film nobody stays in.

| | |
|---|---|
| **Core** | JSTOR Settled and Wanted No Charges. The Government Filed Anyway. |
| **Broad** *(recommended shape)* | **Prosecutors Turned Four Charges Into Thirteen. The Deal Was Six Months.** |
| thumb A / human emotion | **HE REFUSED THE DEAL** - a young man's hands on a laptop in a stairwell, face out of frame |
| thumb B / evidence | **4 to 13 COUNTS** - the superseding indictment cover page, count list running off the bottom |
| thumb C / symbolic / minimal | **NO VICTIM ASKED** - a library card catalogue drawer, open, empty **<- REC** |
| **the one sentence** | Prosecutors Turned Four Charges Into Thirteen. The Deal Was Six Months.  +  NO VICTIM ASKED |
| **action** | apply proposed Broad title + selected thumbnail |
| **earliest apply** | 2026-09-07 - treated arm of the running title experiment; overwriting before the 2026-09-07 read destroys the measurement |

**Verified against the episode's own files:**

- the superseding indictment turned four charges into thirteen - `episodes/PD-2026-023-swartz/03_script/script.en.v001.md L82`
  > They filed what is known in the courts as a superseding indictment. With it, the original four charges suddenly became thirteen.
- the plea signal was around six months - `episodes/PD-2026-023-swartz/03_script/script.en.v001.md L86`
  > According to his own defence attorney, Elliot Peters, what the prosecutors actually signaled behind closed doors was a guilty plea, in exchange for a sentence of around six months
- JSTOR settled civilly and did not want charges - `episodes/PD-2026-023-swartz/03_script/script.en.v001.md L63 header locks`
  > He was CHARGED, never tried or convicted. JSTOR settled civilly + did not want charges; MIT neutral.

> **!** ACCURACY BREACH, live now: the thumbnail reads '35 YEARS FOR PAPERS.' The episode's own blocking lock states 'THE 35 YEARS: never unqualified. Always theoretical stacked statutory maximum, paired with the ~6-month plea signal.' The live thumbnail is the unqualified form. Replace it on accuracy grounds whatever the owner decides about titles.
> **!** PREMISE: a tech-history subject for an audience measured at 77% aged 55+ and 92.5% male, at 29 minutes. AVD 3.97%. This is a format and audience mismatch, not a headline problem.

### 12. `005-madoff` - 1,490 impressions at 1.81%

> **Current title:** He Handed the SEC the Arithmetic in 2000. Madoff Kept Running Until 2008.  
> **Current thumbnail:** NO ONE ASKED. - *scene*

57 lifetime views | 1 subs | AVD 20.54% | 12 min | TREATED 2026-08-10 - current title has ~0 days of measurement

*The CTR above belongs to the title that was live during the window:* "He warned regulators about Madoff for nearly ten years"

**What is wrong with it.** 'The Arithmetic' is an abstraction where the film has a concrete object -- a written report handed over and shelved. And see the accuracy flag: the title promises a year the narration never says.

| | |
|---|---|
| **Core** | The $65 Billion Everyone Quotes Was Paper Value, Not Money Stolen. |
| **Broad** *(recommended shape)* | **He Warned the SEC for a Decade. Its Own Watchdog Said the Warnings Were Credible.** |
| thumb A / human emotion | **NOBODY CHECKED** - an analyst alone at a desk of printouts, office dark around him |
| thumb B / evidence | **RED FLAGS, IN WRITING** - the submitted report, red annotations in the margin, page after page **<- REC** |
| thumb C / symbolic / minimal | **A SLEEPING WATCHDOG** - one impossibly straight line on a performance chart |
| **the one sentence** | He Warned the SEC for a Decade. Its Own Watchdog Said the Warnings Were Credible.  +  RED FLAGS, IN WRITING |
| **action** | apply proposed Broad title + selected thumbnail |
| **earliest apply** | 2026-09-07 - treated arm of the running title experiment; overwriting before the 2026-09-07 read destroys the measurement |

**Verified against the episode's own files:**

- he warned repeatedly over roughly a decade, including a detailed written report - `episodes/PD-2026-005-madoff/03_script/script.en.v001.md L104`
  > He warned them. Then he warned them again. Over roughly a decade, he brought his case to the SEC more than once, including a detailed written report laying out the red flags step by step.
- the SEC's own internal watchdog found the warnings were credible and specific - `episodes/PD-2026-005-madoff/03_script/script.en.v001.md L110`
  > they had received credible, specific warnings, for years
- the $65bn figure is paper statement value, not money stolen - `episodes/PD-2026-005-madoff/03_script/script.en.v001.md and 01_research/claims.v001.json CLM-0004`
  > People say Madoff stole sixty-five billion dollars. Not quite. / 'The widely cited $65 billion figure is the total fabricated value reported across customer account statements'

> **!** PACKAGING RUNS AHEAD OF THE FILM: the live title asserts 'in 2000'. The narration never states 2000 -- it says 'over roughly a decade'. The 2000 submission is real and is in 01_research/claims.v002.json, but it is not on screen, so the title promises a specific the film does not pay off. Either fix the title (proposed Broad does) or add the line to the film.

### 13. `032-carsearch` - 1,318 impressions at 3.95%

> **Current title:** Police Searched the Motorcycle in His Driveway. The Court Found the One Line Left.  
> **Current thumbnail:** NO WARRANT NEEDED / SEARCH YOUR CAR? / symbolic reconstruction / PRIME DOCUMENTARY - *scene*

71 lifetime views | 0 subs | AVD 27.68% | 12 min | TREATED 2026-08-10 - current title has ~0 days of measurement

*The CTR above belongs to the title that was live during the window:* "Police Can Search Your Car Without a Warrant — Except One Place"

**What is wrong with it.** The title's second clause, 'The Court Found the One Line Left', names nothing a viewer can picture. But at 3.95% it is the second-best CTR on the channel and should not be touched. The thumbnail is the fixable half: four stacked text elements across two competing subjects with PRIME DOCUMENTARY burned in, against a rule of 2-4 words and one subject.

| | |
|---|---|
| **Core** | The Automobile Exception Has Run Since 1925. Curtilage Is Its Only Edge. |
| **Broad** *(recommended shape)* | **Police Searched the Bike Under the Tarp. The Driveway Is Where It Stopped.** |
| thumb A / human emotion | **TOO CLOSE TO HOME** - a figure at a front window looking down at officers on the drive |
| thumb B / evidence | **UNDER THE TARP** - a tarp lifted at one corner, a wheel and a frame number showing **<- REC** |
| thumb C / symbolic / minimal | **ONE STEP TOO FAR** - a bright line drawn across a driveway at the property edge |
| **the one sentence** | Police Searched the Motorcycle in His Driveway. The Court Found the One Line Left.  +  UNDER THE TARP |
| **action** | KEEP live title, apply selected thumbnail |
| **earliest apply** | 2026-09-07 - treated arm of the running title experiment; overwriting before the 2026-09-07 read destroys the measurement |

**Verified against the episode's own files:**

- a motorcycle under a tarp in a Virginia driveway - `episodes/PD-2026-032-carsearch/03_script/script.en.v001.md`
  > a motorcycle hidden under a tarp in a Virginia driveway
- the Court held 8-1 in 2018 that the car-search power stops at the curtilage - `episodes/PD-2026-032-carsearch/03_script/script.en.v001.md L90`
  > In 2018, by a vote of eight to one, the Court held that the car-search power does not reach onto the ground that belongs to your home. [CLM-0007]
- the automobile exception dates to Carroll, 1925 - `episodes/PD-2026-032-carsearch/03_script/script.annotated.v001.json`
  > For a hundred years police have been able to search your car without a warrant on probable cause (the automobile exception, Carroll 1925)

### 14. `034-rolin` - 1,165 impressions at 0.86%

> **Current title:** They Took His Life Savings at the Airport — No Charges, No Crime  
> **Current thumbnail:** NO CRIME. NO CHARGES. / THEY TOOK HIS $82,000 / SEIZED / PRIME DOCUMENTARY - *object*

29 lifetime views | 0 subs | AVD 18.12% | 19 min | CONTROL - must not be retitled before 2026-09-07

**What is wrong with it.** 'They' has no referent; the strongest asset in the story -- the $82,000 -- sits in the thumbnail instead of the title, which is v002's canonical pairing exactly backwards; and the thumbnail then repeats the title's 'no charges, no crime' word for word (71% overlap) with PRIME DOCUMENTARY burned in on top.

| | |
|---|---|
| **Core** | Civil Forfeiture Runs Against the Money, Not the Person. No Charge Needed. |
| **Broad** *(recommended shape)* | **His Daughter Carried His $82,000 Through the Airport. Agents Took It All.** |
| thumb A / human emotion | **IT WAS ALL LEGAL** - an older man at a kitchen table with an empty bank envelope |
| thumb B / evidence | **0 CHARGES** - a seizure receipt on a counter, the charge field blank **<- REC** |
| thumb C / symbolic / minimal | **HIS OWN CASH** - banded notes in a clear evidence bag |
| **the one sentence** | His Daughter Carried His $82,000 Through the Airport. Agents Took It All.  +  0 CHARGES |
| **action** | apply proposed Broad title + selected thumbnail |
| **earliest apply** | 2026-09-07 - protected control arm of the running title experiment |

**Verified against the episode's own files:**

- about eighty-two thousand dollars, his life savings - `episodes/PD-2026-034-rolin/03_script/script.en.v001.md`
  > A retired railroad worker near Pittsburgh kept his life savings in cash -- about eighty-two thousand dollars.
- his daughter, not he, carried it through the airport - `episodes/PD-2026-034-rolin/03_script/script.en.v001.md`
  > His daughter carried it through an airport to put it in a bank.
- a DEA agent took it and no one was charged - `episodes/PD-2026-034-rolin/03_script/script.en.v001.md and 03_script/script.annotated.v001.json`
  > a federal agent from the Drug Enforcement Administration / 'seize cash from travelers who broke no law and were never charged'

> **!** The live title implies he was at the airport. He was not -- his daughter was carrying it. Minor, but the proposed Broad fixes it and it is more interesting the correct way round.

### 15. `042-young` - 1,151 impressions at 0.43%

> **Current title:** Police Raided the Wrong House and Handcuffed an Innocent Woman  
> **Current thumbnail:** CHICAGO 2019 / WRONG HOUSE - *face_reaction*, AI face

32 lifetime views | 0 subs | AVD 29.56% | 12 min | CONTROL - must not be retitled before 2026-09-07

**What is wrong with it.** 'Wrong house' plus 'innocent woman' is the most-seen headline shape in American local news; there is no expectation left to violate. The violation the film actually delivers -- a city paid $2.9 million while the record says nobody wronged her -- is in neither the title nor the thumbnail. Worst CTR in the twenty at 0.43%.

| | |
|---|---|
| **Core** | Hudson v. Michigan Removed the Remedy. A Wrong-Door Raid Ends in a Check. |
| **Broad** *(recommended shape)* | **Chicago Paid Her $2.9 Million and Never Said Anyone Did Anything Wrong.** |
| thumb A / human emotion | **SHE WAS RIGHT** - a woman alone in a doorway, coat held closed, hallway light behind |
| thumb B / evidence | **48-0, NO FAULT** - the council vote sheet, the tally line and the blank finding-of-fault field |
| thumb C / symbolic / minimal | **A CHECK, NO VERDICT** - a settlement cheque face-up beside an unsigned finding **<- REC** |
| **the one sentence** | Chicago Paid Her $2.9 Million and Never Said Anyone Did Anything Wrong.  +  A CHECK, NO VERDICT |
| **action** | apply selected thumbnail TODAY (title untouched); apply Broad title only after the 2026-09-07 read |
| **earliest apply** | 2026-08-12 - Designated clean thumbnail test in TITLE_EXPERIMENT_RECEIPT.v001.md section 7 - thumbnail only, title untouched |

**Verified against the episode's own files:**

- about twelve officers, wrong address, February 2019 Chicago - `episodes/PD-2026-042-young/08_edit/captions.final.v001.srt and 09_package/youtube_meta.v001.json`
  > Twelve officers, rifles up. / 'In February 2019, about a dozen Chicago police officers executed a search warrant ... They had the wrong address.'
- $2.9 million settlement approved 48-0, with no finding of fault - `episodes/PD-2026-042-young/09_package/youtube_meta.v001.json and 08_edit/captions.final.v001.srt`
  > a $2.9 million settlement, reported approved by the City Council 48-0 in December 2021 ... not a finding that any officer or the city was legally liable
- no court ever found her rights were violated - `episodes/PD-2026-042-young/08_edit/captions.final.v001.srt`
  > no court ever said a single person violated Anjanette Young's rights. The money admitted nothing.

> **!** DO NOT USE '43 times'. It is the widely circulated press figure and it does NOT appear anywhere in this episode. The film deliberately declines to state a count -- 'recording her voice, the number of times she says it, and the silence where an answer should be.' A title carrying 43 would be a fact imported from outside the film.
> **!** THIS IS THE ONE ROW THAT CAN SHIP TODAY. episodes/_planning/measurements/TITLE_EXPERIMENT_RECEIPT.v001.md section 7 designates this video the clean test: a fully rule-compliant title with the worst CTR of any high-impression long-form, deliberately left untouched, with the instruction 'Change only its thumbnail and nothing else; if CTR moves, the title rules were never the lever.' Apply thumbnail C now. Leave the title alone until 2026-09-07.

### 16. `047-atwater` - 999 impressions at 0.40%

> **Current title:** A Seatbelt Ticket Carried No Jail Time. She Was Handcuffed in Front of Her Children.  
> **Current thumbnail:** OVER A $50 FINE / JAILED OVER A SEATBELT - *face_reaction*, AI face

4 lifetime views | 0 subs | AVD 2.00% | 12 min | TREATED 2026-08-10 - current title has ~0 days of measurement

*The CTR above belongs to the title that was live during the window:* "She Was Handcuffed and Jailed Over a $50 Seatbelt Fine"

**What is wrong with it.** It opens on a rule rather than on a person or an event, which is the exact inversion v002 forbids -- person, then abnormal event, then system, never system first. Second-worst CTR in the twenty at 0.40%.

| | |
|---|---|
| **Core** | Atwater v. Lago Vista: a Custodial Arrest for a Fine-Only Offense Is Constitutional. |
| **Broad** *(recommended shape)* | **The Most She Could Be Fined Was $50. She Was Handcuffed and Booked.** |
| thumb A / human emotion | **HER KIDS WATCHED** - two small children at a truck window, roadside, an adult's hands behind her back out of focus |
| thumb B / evidence | **SEAT BELT, FINE ONLY** - the citation form, the penalty box filled in and nothing else **<- REC** |
| thumb C / symbolic / minimal | **STILL LAWFUL** - an open pair of handcuffs on a booking counter |
| **the one sentence** | The Most She Could Be Fined Was $50. She Was Handcuffed and Booked.  +  SEAT BELT, FINE ONLY |
| **action** | apply proposed Broad title + selected thumbnail |
| **earliest apply** | 2026-09-07 - treated arm of the running title experiment; overwriting before the 2026-09-07 read destroys the measurement |

**Verified against the episode's own files:**

- the maximum penalty was a fifty-dollar fine - `episodes/PD-2026-047-atwater/08_edit/captions.final.v001.srt`
  > The most the law can ever do to her is take fifty dollars.
- she was driving with two small children, none belted - `episodes/PD-2026-047-atwater/08_edit/captions.final.v001.srt`
  > a mother at the wheel, her two small children in the cab beside her. None of them is wearing a seatbelt.
- the Court upheld the arrest five to four - `episodes/PD-2026-047-atwater/08_edit/captions.final.v001.srt`
  > By a vote of five to four, the Court held that the arrest of Gail Atwater did not violate the Fourth Amendment.

> **!** ACCURACY LOCK from the script: the Court UPHELD the arrest 5-4; a custodial arrest for a fine-only offence is constitutional. No packaging asset may imply it was struck down.

### 17. `022-milken` - 880 impressions at 1.70%

> **Current title:** One Banker Was Paid $550 Million in a Year. Then the Government Came for Him.  
> **Current thumbnail:** IT WASN'T ENOUGH. - *scene*

22 lifetime views | 0 subs | AVD 16.00% | 28 min | TREATED 2026-08-10 - current title has ~0 days of measurement

*The CTR above belongs to the title that was live during the window:* "One banker was paid $550 million in a single year"

**What is wrong with it.** The title is competent and the CTR is mid-pack. The problem is upstream: the protagonist is a wealthy, powerful individual and the ending is ambiguous -- the inverse of both the v002 centre and the 'ordinary American versus power' editorial line. No headline converts that for this audience.

| | |
|---|---|
| **Core** | The Junk-Bond Market He Built Outlived the Six Felonies He Pleaded To. |
| **Broad** *(recommended shape)* | **He Was Charged on 98 Counts and Pleaded to Six. A Pardon Closed the Rest.** |
| thumb A / human emotion | **PARDONED, NOT CLEARED** - an empty boardroom chair under a single overhead light |
| thumb B / evidence | **92 DROPPED** - the 1989 indictment, the struck counts and the withdrawn RICO caption **<- REC** |
| thumb C / symbolic / minimal | **$600M PENALTY** - a single cheque stub on black |
| **the one sentence** | He Was Charged on 98 Counts and Pleaded to Six. A Pardon Closed the Rest.  +  92 DROPPED |
| **action** | apply proposed Broad title + selected thumbnail |
| **earliest apply** | 2026-09-07 - treated arm of the running title experiment; overwriting before the 2026-09-07 read destroys the measurement |

**Verified against the episode's own files:**

- about $550 million in a single year - `episodes/PD-2026-022-milken/03_script/script.en.v001.md`
  > In a single year, one man was paid about five hundred and fifty million dollars.
- charged on 98 counts in 1989, pleaded guilty to six in 1990 - `episodes/PD-2026-022-milken/03_script/script.en.v001.md (WORDING LOCKS)`
  > Charged in a 98-count indictment (1989) -> pleaded to 6 (1990). Charges != findings; RICO + 92 counts dropped.
- about $600 million: $200m fine plus $400m restitution - `episodes/PD-2026-022-milken/03_script/script.en.v001.md`
  > 'about $600 million' = $200M fine + $400M restitution fund (1990)
- a 2020 presidential pardon that did not erase the guilty plea - `episodes/PD-2026-022-milken/03_script/script.annotated.v001.json`
  > a 2020 presidential pardon forgave the crime without erasing the guilty plea

> **!** ACCURACY LOCK: 'pleaded guilty' -- never 'convicted at trial'. He did not go to trial.
> **!** PREMISE: wealthy-and-powerful protagonist, ambiguous ending, 27 minutes. Off-centre for v002.

### 18. `014-lange` - 750 impressions at 4.40%

> **Current title:** He Honked His Horn and Drove Home. An Officer Followed Him Into His Own Garage.  
> **Current thumbnail:** YOUR DOOR? - *scene*

43 lifetime views | 0 subs | AVD 18.70% | 9 min | TREATED 2026-08-10 - current title has ~0 days of measurement

*The CTR above belongs to the title that was live during the window:* "He Drove Home Honking. The Police Followed Him Inside."

**What is wrong with it.** Nothing is wrong with it. At 4.40% this is the highest CTR on the channel and already sits in the v002 shape -- ordinary person, small act, disproportionate consequence, contradiction visible, thumbnail sharing no word with the title. It is written here for completeness only. The experiment receipt already lists it first among the assets to protect. Do not touch it in this wave.

| | |
|---|---|
| **Core** | Lange v. California: Misdemeanor Flight Does Not Automatically Open Your Door. |
| **Broad** *(recommended shape)* | **He Honked His Horn. An Officer Followed Him Into His Garage.** |
| thumb A / human emotion | **YOUR DOOR?** - a garage door halfway down, a boot in the gap **<- REC** |
| thumb B / evidence | **MUSIC AND A HORN** - the citation, the offence line legible |
| thumb C / symbolic / minimal | **ONE FOOT INSIDE** - the threshold line at the garage lip |
| **the one sentence** | He Honked His Horn and Drove Home. An Officer Followed Him Into His Own Garage.  +  YOUR DOOR? |
| **action** | KEEP live title and live thumbnail |
| **earliest apply** | 2026-09-07 - treated arm of the running title experiment; overwriting before the 2026-09-07 read destroys the measurement |

**Verified against the episode's own files:**

- Arthur Lange, Sonoma County, loud music and a few honks - `episodes/PD-2026-014-lange/03_script/script.en.v001.md`
  > a man named Arthur Lange, in Sonoma County, California. He is doing nothing dramatic -- playing his music loudly and honking his horn a few times.
- the officer followed him into the garage - `episodes/PD-2026-014-lange/03_script/script.en.v001.md`
  > pull into your own garage, and reach for the button to close the door. The officer walks up and sticks...
- 2021, 9-0 in the judgment, vacate and remand - `episodes/PD-2026-014-lange/03_script/script.en.v001.md (header lock)`
  > Vote = 'unanimous in the JUDGMENT (9-0 vacate & remand)', NOT a unanimous opinion.

> **!** ACCURACY LOCK: 9-0 in the JUDGMENT, not a unanimous opinion. Do not compress to 'the Court was unanimous' in packaging.

### 19. `033-tyler` - 738 impressions at 1.22%

> **Current title:** She Owed the County $15,000. It Sold Her Home for $40,000 and Kept All of It.  
> **Current thumbnail:** THEY KEPT THE CHANGE. - *scene*

191 lifetime views | 2 subs | AVD 13.09% | 18 min | TREATED 2026-08-10 - current title has ~0 days of measurement

*The CTR above belongs to the title that was live during the window:* "The county sold her condo and kept the extra $25,000"

**What is wrong with it.** Three dollar figures in one sentence turn a gut-punch into arithmetic -- the reader has to compute $40,000 minus $15,000 before feeling anything. The proposed pair puts one figure in the title and one in the thumbnail, which is the v002 sentence rule working as designed.

| | |
|---|---|
| **Core** | Tyler v. Hennepin County: Keeping the Surplus Is an Unconstitutional Taking, 9-0. |
| **Broad** *(recommended shape)* | **A County Sold a 94-Year-Old's Home Over a $2,300 Debt.** |
| thumb A / human emotion | **SHE OWNED IT OUTRIGHT** - an elderly woman's hands holding a paid-off deed |
| thumb B / evidence | **KEPT $40,000** - the county sale ledger, the surplus line unstruck **<- REC** |
| thumb C / symbolic / minimal | **$0 RETURNED** - a condo key on a blank remittance slip |
| **the one sentence** | A County Sold a 94-Year-Old's Home Over a $2,300 Debt.  +  KEPT $40,000 |
| **action** | apply proposed Broad title + selected thumbnail |
| **earliest apply** | 2026-09-07 - treated arm of the running title experiment; overwriting before the 2026-09-07 read destroys the measurement |

**Verified against the episode's own files:**

- Geraldine Tyler was ninety-four - `episodes/PD-2026-033-tyler/03_script/script.en.v001.md`
  > Her name was Geraldine Tyler, and by the time this story finds its ending, she is ninety-four years old. [CLM-0002]
- the debt began at $2,300 and grew to roughly $15,000 - `episodes/PD-2026-033-tyler/03_script/script.en.v001.md`
  > twenty-three hundred dollars had swollen to roughly fifteen thousand. [CLM-0004]
- the condo sold for $40,000 and the county kept all of it - `episodes/PD-2026-033-tyler/03_script/script.en.v001.md`
  > It sold for forty thousand dollars. [CLM-0005]
- 9-0 for Tyler, 25 May 2023, Roberts writing - `episodes/PD-2026-033-tyler/01_research/claims.v001.json CLM-0010`
  > On May 25, 2023, the Supreme Court ruled 9-0 for Tyler, in an opinion written by Chief Justice Roberts.

> **!** Do not reuse the pre-08-10 title's '$25,000'. It is $40,000 minus $15,000, and the $15,000 is itself 'roughly fifteen thousand' in the film -- a derived figure resting on an approximation. $2,300 and $40,000 are both exact in the record.

### 20. `020-gardner` - 712 impressions at 1.26%

> **Current title:** Two Men in Police Uniforms Emptied a Boston Museum. The Frames Still Hang Empty.  
> **Current thumbnail:** 36 YEARS EMPTY. - *object*

16 lifetime views | 0 subs | AVD 34.19% | 27 min | TREATED 2026-08-10 - current title has ~0 days of measurement

*The CTR above belongs to the title that was live during the window:* "Two men dressed as police emptied a Boston museum"

**What is wrong with it.** 'Emptied a Boston Museum' overstates what happened -- thirteen works were taken from a collection of thousands, and the film's own line is that the frames were emptied, not the museum. Tighten it whatever else is decided.

| | |
|---|---|
| **Core** | The Gardner Heist Is Still Open. Nothing Has Been Recovered Since 1990. |
| **Broad** *(recommended shape)* | **Two Men in Police Uniforms Took 13 Paintings in 81 Minutes.** |
| thumb A / human emotion | **STILL EMPTY** - a gallery bench facing an empty frame on a papered wall |
| thumb B / evidence | **$10M REWARD** - the FBI reward notice, thirteen thumbnails printed down the side **<- REC** |
| thumb C / symbolic / minimal | **36 YEARS OPEN** - one empty frame, straight on |
| **the one sentence** | Two Men in Police Uniforms Took 13 Paintings in 81 Minutes.  +  $10M REWARD |
| **action** | apply proposed Broad title + selected thumbnail |
| **earliest apply** | 2026-09-07 - treated arm of the running title experiment; overwriting before the 2026-09-07 read destroys the measurement |

**Verified against the episode's own files:**

- thirteen works in eighty-one minutes, 1990 - `episodes/PD-2026-020-gardner/03_script/script.en.v001.md`
  > Eighty-one minutes. Thirteen works. And more than thirty years later -- not one has ever been found.
- a ten million dollar reward - `episodes/PD-2026-020-gardner/03_script/script.en.v001.md`
  > more frightened of something than they are tempted by ten million dollars
- the $500 million figure is an estimate - `episodes/PD-2026-020-gardner/03_script/script.en.v001.md (WORDING LOCKS)`
  > '$500 million' is an ESTIMATE (works unsaleable; museum is 'the only buyer').

> **!** PREMISE: no ordinary person and no system the viewer touches. Evergreen mystery, off-centre for v002. Keep, do not template.
> **!** ACCURACY LOCK: suspects were named by journalists, not the FBI. No packaging asset may name one.

---

## 4. Films whose problem is not packaging

`scripts/score_premise.py --os v002` was **not** run against these. No premise file exists for any
published episode - `config/pd_premise_seeds.v001.json` holds forward-looking seeds only, and
`episodes/*/00_topic/premise*.json` returns nothing. The v002 rubric post-dates all twenty films, so
authoring scores for them now would mean inventing the inputs and then calling the output a
measurement. Judged against the rubric's axes in prose instead:

| slug | CTR | AVD | the problem | verdict |
|---|---:|---:|---|---|
| `021-dbcooper` | 2.29% | 34.77% | the protagonist is the perpetrator, there is no ordinary person and no system the viewer touches. It is the inverse of the v002 centre. It performs anyway on pure mystery (2.29%), so keep it -- but it does not model the format and should not be used as a template. | Off-centre for v002 but performing. No rewrite required on premise grounds. |
| `023-swartz` | 0.80% | 3.97% | a tech-history subject for an audience measured at 77% aged 55+ and 92.5% male, at 29 minutes. AVD 3.97%. This is a format and audience mismatch, not a headline problem. | Weak for this audience at this length. Repackaging will not move it; the honest options are a short re-cut or leaving it alone. |
| `022-milken` | 1.70% | 16.00% | wealthy-and-powerful protagonist, ambiguous ending, 27 minutes. Off-centre for v002. | Premise, not packaging. Keep it in the catalogue, do not build more like it. |
| `020-gardner` | 1.26% | 34.19% | no ordinary person and no system the viewer touches. Evergreen mystery, off-centre for v002. Keep, do not template. | Off-centre for v002 but evergreen and low-risk. No premise rework proposed. |

`023-swartz` is the sharpest case: **3.97% average view duration on a 29-minute film** is the worst
engagement in the twenty by a factor of five. Its 0.80% CTR is a symptom, not the disease. No title
recovers a film nobody stays inside, and this one aims a tech-history subject at an audience measured
at 77% aged 55+ and 92.5% male.

---

## 5. Facts I checked and refused to use

Every figure, name and outcome in a proposed title had to be already true of that episode. Four
candidates died on that rule - and four packaging assets **currently live** fail it.

**Rejected from my own drafts:**

| candidate | why it was dropped |
|---|---|
| **"She told them 43 times"** (`042-young`), the widely circulated press figure | Appears **nowhere** in the episode. The film deliberately declines to count: *"recording her voice, the number of times she says it, and the silence where an answer should be."* Importing 43 would be a fact from outside the film. |
| **"His lawyer had $1,000"** (`029-hinton`) | False. The episode's guardrail is explicit: the $1,000 was the lawyer's **mistaken belief** about a funding cap, and **no cap existed**. The proposed title says "thought". |
| **"fourteen death warrants"** (`041-thompson`) | Appears once, in a closing rhetorical line, corroborated nowhere else in the episode; the commonly reported count is seven execution dates. Not used, and flagged for a fact re-check **of the film itself**. |
| **"$25,000 surplus"** (`033-tyler`), used in the pre-08-10 title | Derived: $40,000 - $15,000, where the $15,000 is itself *"roughly fifteen thousand"* in the narration. An approximation resting on an approximation. $2,300 and $40,000 are exact; those are what the proposal uses. |

**Live assets that run ahead of their own films. Fix these regardless of what happens to the wave:**

| asset | breach |
|---|---|
| `023-swartz` thumbnail **"35 YEARS FOR PAPERS."** | Breaks the episode's own blocking lock: *"THE 35 YEARS: never unqualified. Always theoretical stacked statutory maximum, paired with the ~6-month plea signal."* The live thumbnail is the unqualified form. |
| `021-dbcooper` thumbnail **"HE NEVER LANDED."** | Asserts an outcome the film refuses to assert. Its wording lock is *unsolved, never identified* - not dead. |
| `005-madoff` title **"...the Arithmetic in 2000"** | The narration never says 2000; it says *"over roughly a decade."* The 2000 submission is real and sits in `01_research/claims.v002.json`, but it is not on screen, so the title promises a specific the film does not pay off. |
| `020-gardner` title **"Emptied a Boston Museum"** | Overstates. Thirteen works from a collection of thousands; the film's own line is that the *frames* were emptied. |

---

## 6. If approved

```
# today, if row 15 is approved - thumbnail only, title untouched
#   042-young   Enok7A7wGBA   apply thumbnail C "A CHECK, NO VERDICT"

# 2026-09-07 - read the running experiment FIRST
py -3.11 scripts/yt_studio_video_ctr.py          # snapshot the JSON before pulling
#   compare against episodes/_planning/measurements/TITLE_APPLY_39.applied.v001.json
#   WIN  -> keep the 08-10 titles, apply thumbnails only from this wave
#   NULL -> apply this wave's Broad titles; the title lever retires as a hard gate either way
#   LOSS -> roll back via scripts/apply_title_batch.py --rollback, then apply this wave
```

Approved rows are machine-readable at `runs/repackaging/wave2_top20.v001.json`. Each row carries
`proposal.recommended_title`, `thumbnail_recommended`, `apply_gate.earliest_apply_date` and the
verification quotes, so an applier can be pointed at it without re-deriving anything.
