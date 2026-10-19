# Repackaging Wave 2 — the tail (ranks 21–57 by impressions)

**Proposal only.** PROPOSAL ONLY. Titles and thumbnails are an owner approval gate (CLAUDE.md s3, .claude/rules/16). Nothing was changed on YouTube.
Authored 2026-08-12. Machine record: `runs/repackaging/wave2_tail.v001.json`.

**Boundary, so it is unambiguous.** Rank = descending `performance.ctr_impressions` in `data/content_genome.v001.jsonl`. **This document covers ranks 21 through 57 — all 37 films.** Rank 20 is `PD-2026-020-gardner` (712 impressions) and belongs to the sibling agent; rank 21 is `PD-2026-007-riley` (687 impressions) and is the first film here. Every one of the 37 appears in exactly one bucket below, and the count is asserted in the JSON.

---

## 1. The one number that reorders this half

`ctr_impressions` is Studio's **rolling 28-day** window. A film published two days ago has had two days to earn it. Ranking the tail on raw impressions therefore confuses *age* with *rejection* — and in this half that confusion is total, because the newest films are the 28–30 minute ones published in the last week.

So the working metric here is **impressions per day** = `ctr_impressions / clamp(age_in_fractional_days, 0.5, 28)`. Fractional days on purpose: flooring to whole days would inflate the newest films' rate by up to 2×, and the newest films are exactly the group this analysis is about to promote.

Re-sorted that way, the six highest-exposure films in my half are the six most recent. Their catalogue-wide positions on impressions/day are 4th, 11th, 12th, 17th, 22nd and 23rd of 57, against a catalogue median of 25.4/day — so all six are being served at or above the median rate, and the top three are being served hard:

| episode | rank by raw impressions | impressions/day | CTR |
|---|---|---|---|
| `PD-2026-053-norfolk` | 33 | **176.5** | 1.52% |
| `PD-2026-055-burge` | 35 | **99.3** | 1.05% |
| `PD-2026-056-postoffice` | 36 | **77.4** | 0.7% |
| `PD-2026-054-flowers` | 39 | **55.9** | 0.49% |
| `PD-2026-060-surfside` | 45 | **42.6** | 0.61% |
| `PD-2026-059-robosigning` | 40 | **41.3** | 0.5% |

For scale, the top-20 half's leader `PD-2026-035-hinders` runs 320.8/day. `PD-2026-053-norfolk` runs **176.5/day** — fourth in the entire catalogue, behind only hinders, florence and glover — and converts at 1.52%. It is the single most valuable repackaging target in the tail, and it is still inside its launch window, where a title change is still cheap and still gets seen.

Targets used below: **3.0%** as the planning target, because this channel has already demonstrated it (carsearch 3.95, fieldtest 4.55, onecoin 3.76, terry 3.12); **6.0%** as the owner's stated north star, shown as an upper bound.

---

## 2. The answer to "which of these are worth repackaging at all"

Not most of them. The 37 split five ways, and only 15 justify an owner approval cycle.

| bucket | n | what it means |
|---|---|---|
| **(a) rewrite** | 15 | Good film, bad packaging. Live exposure, CTR below the demonstrated band. |
| **(a2) rewrite if a batch is already open** | 2 | Real defects, exposure too thin to open a cycle for. |
| **hold — packaging already works** | 9 | Live exposure at **3.39% weighted CTR**, 2.6× the catalogue median. Touching these risks a regression for no measured reason. |
| **(b) weak premise** | 2 | No title saves them. Both have live exposure, so distribution is not the excuse. |
| **(c) below the view floor** | 9 | Under ~6 impressions/day. Named, then set aside. |

**The whole (c) bucket, honestly priced.** Nine films, 1029 forward-28d impressions between them, 13.1 clicks. Perfect titles on all nine return about **18 extra clicks a month**. That is the argument for not reading further about them.

**The (a) bucket, priced the same way.** 15 films, 19,271 forward-28d impressions, **+382 clicks at 3%** (+960 at 6%). The top six by return carry **72%** of it. If only one batch happens, it is those six.

*Caveat, stated rather than buried:* Impressions are assumed to hold at the current daily rate for 28 days. For the six newest films that is optimistic: launch-window impressions decay. Treat these as upper bounds on a 28-day horizon, not forecasts.

---

## 3. Rules every pair below satisfies (checked mechanically, not by eye)

- Title is **Subject + Verb + Consequence**, built on a verb from the `pd_planning_os.v002` list (took / lost / found / hid / refused / vanished / changed / cost / locked / failed / knew / never / wrong).
- No *how*, *history*, *explained*, *understanding*, *framework*, *legal implications*.
- **Core** and **Broad** written for every film; **Broad is recommended** in all fifteen.
- Three thumbnail concepts per film across human emotion / evidence / symbolic-minimal, with the house shift toward **evidence** — a document, a figure, a form.
- Thumbnail text is 2–4 words, one subject.
- **Title and thumbnail share no content word.** The build script fails and writes nothing if any recommended pair repeats itself; it caught one 5-word thumbnail and one repeat before this file existed.
- The contradiction is visible in the title, not deferred to the thumbnail.

**Fact discipline.** Every figure, name and outcome below was located in that episode's own script, captions or facts ledger *before* it was used, and the location is cited under each film. Nothing was inherited from a live title on trust — the `$1,554` in the current cleveland title was re-confirmed against `cleveland_facts.v001.json` F04 rather than assumed, and the `~$300,000 settlement` and `~$3,800 theft` figures in the williams film are marked grade-B in its own script and are therefore **excluded** from every proposed thumbnail.

---

## 4. (a) Rewrite — 15 films, in order of expected return

### 1. `PD-2026-053-norfolk` · rank 33 · H8j_K1x9Dog

> **Now:** 4 Sailors Confess to One Murder. The DNA Clears Each One. The Detective Finds Another.

`330` impressions over 1.87d → **176.5/day** · CTR **1.52%** · views unavailable · AVD unavailable · runtime 28m · published 2026-08-10

**+73.1 clicks/28d at 3%** (+221.4 at 6%)

**Why it is losing the click.** Highest live exposure in this half and fourth in the whole catalogue (176 impressions/day, behind hinders, florence and glover). Three sentences, all present tense, and the consequence never lands on a person. 'Confess' is not a consequence verb.

- **Core:** Seven Sailors Signed Confessions. The DNA Matched None of Them.
- **Broad (recommended):** Every Time the DNA Cleared a Man, the Detective Found Another One.  ·  verb *found*

| | kind | text | note |
|---|---|---|---|
| **A** | human emotion | **HOUR ELEVEN** | The first confession broke at hour eleven of the night; the film names the hour repeatedly. |
| **B** ★ | evidence | **7 CHARGED 0 MATCHES** | The film's own on-screen text card. A lab tally, not a face. |
| **C** | symbolic / minimal | **I ACTED ALONE** | Ballard's sworn words, verbatim, twice on the record. |

**Ship pair:** *Every Time the DNA Cleared a Man, the Detective Found Another One.*  +  **7 CHARGED 0 MATCHES**

<details><summary>verified against</summary>

- `episodes/PD-2026-053-norfolk/03_script/script.en.v001.md L59 (seven sailors charged, one attacker)`
- `…L61 ('all seven charged men, every single one, excluded by DNA')`
- `…L64 (OST: 7 CHARGED / 0 DNA MATCHES / 1 ATTACKER)`
- `…L86 (OST: BALLARD: THE ONLY DNA MATCH / 'I ACTED ALONE')`
- `…L49 ('when the DNA cleared the man who confessed… he went out and found a new one')`

</details>

### 2. `PD-2026-055-burge` · rank 35 · Iw-EPUD2nHg

> **Now:** A Doctor Reports Police Torture in 1982. The Letter Is Buried for 33 Years.

`285` impressions over 2.87d → **99.3/day** · CTR **1.05%** · views 1 · AVD 0.63% · runtime 29m · published 2026-08-09

**+54.2 clicks/28d at 3%** (+137.6 at 6%)

**Why it is losing the click.** Second highest live exposure in this half at 99/day, and a 1.05% CTR against it. The current title makes a letter the subject and asks the viewer to care about an archival delay. The film's actual contradiction — the only thing the law could jail him for was lying about it — is absent.

- **Core:** A Doctor Wrote It Down in 1982. Chicago Buried the Letter for 33 Years.
- **Broad (recommended):** Chicago Never Charged Him With Torture. It Jailed Him for Lying About It.  ·  verb *never*

| | kind | text | note |
|---|---|---|---|
| **A** | human emotion | **NOBODY LISTENED** | Anthony Holmes' own words at sentencing: 'it fell on deaf ears'. |
| **B** ★ | evidence | **54 MONTHS** | The sentence, as a figure on a docket. The film states it as 54 months on purpose. |
| **C** | symbolic / minimal | **PENSION PAID** | The 4-4 tie let him keep it until he died — the insult the film ends on. |

**Ship pair:** *Chicago Never Charged Him With Torture. It Jailed Him for Lying About It.*  +  **54 MONTHS**

<details><summary>verified against</summary>

- `episodes/PD-2026-055-burge/03_script/script.en.v001.md L14 ('Jon Burge was never charged with torture… he died a convicted felon')`
- `…L82-84 ('sentenced Jon Burge to four and a half years'; 'fifty-four months, for lying about it')`
- `…L86 (pension board 4-4 tie, paid until the day he died)`
- `…L10 (February 1982 doctor's letter), L98 (thirty-three years)`

</details>

### 3. `PD-2026-056-postoffice` · rank 36 · 4FlCaOVpln0

> **Now:** A Computer Invents a £2,000 Debt. Her Own Employer Prosecutes Her. 236 Go to Prison.

`284` impressions over 3.67d → **77.4/day** · CTR **0.7%** · views unavailable · AVD unavailable · runtime 29m · published 2026-08-08

**+49.8 clicks/28d at 3%** (+114.8 at 6%)

**Why it is losing the click.** 77 impressions/day at 0.70% CTR. Three sentences, present tense, and it opens on a £ figure — PD's measured audience is American, and a foreign currency symbol is a click cost paid in the first half-second. The strongest fact in the film (they knew, in writing) is not in the title at all.

- **Core:** The Post Office Knew Its Computer Was Lying. It Prosecuted 700 of Its Own Anyway.
- **Broad (recommended):** Their Employer Knew the Computer Was Wrong. It Sent 236 of Them to Prison.  ·  verb *knew*

| | kind | text | note |
|---|---|---|---|
| **A** | human emotion | **SHE PAID IT BACK** | Jo Hamilton remortgaged her house to cover money that never existed. |
| **B** ★ | evidence | **0 CONVICTED** | The running count the film keeps to the last line: Post Office and Fujitsu staff convicted of anything = zero. The title cannot carry this; the thumbnail can. |
| **C** | symbolic / minimal | **THE SCREEN LIED** | Least specific of the three; use only if A and B both test poorly. |

**Ship pair:** *Their Employer Knew the Computer Was Wrong. It Sent 236 of Them to Prison.*  +  **0 CONVICTED**

<details><summary>verified against</summary>

- `episodes/PD-2026-056-postoffice/03_script/script.en.v001.md L43 ('roughly seven hundred sub-postmasters were prosecuted by the Post Office itself')`
- `…L101 ('By the BBC's count, two hundred and thirty-six of them went to prison'; 'the number of human beings convicted of any crime for doing this to them… is still zero')`
- `…L13 (Jo Hamilton, two thousand pounds, remortgaged her house, prosecuted for theft)`

</details>

### 4. `PD-2026-054-flowers` · rank 39 · PfdEpNQyaQQ

> **Now:** 6 Trials. 4 Death Sentences. 23 Years. The Same Prosecutor Every Time.

`205` impressions over 3.67d → **55.9/day** · CTR **0.49%** · views 2 · AVD 50.88% · runtime 28m · published 2026-08-08

**+39.3 clicks/28d at 3%** (+86.2 at 6%)

**Why it is losing the click.** Lowest CTR in this half at meaningful exposure: 0.49% on 56 impressions/day. The current title is four number fragments with no subject and no verb — it reads as a statistics line, not a sentence. There is nobody in it.

- **Core:** One Prosecutor Tried the Same Man Six Times. He Was Never Punished for It.
- **Broad (recommended):** He Spent 23 Years on Trial for Four Murders. The State Never Had a Weapon.  ·  verb *never*

| | kind | text | note |
|---|---|---|---|
| **A** | human emotion | **TRIED SIX TIMES** | Plain, and it survives at phone size. |
| **B** ★ | evidence | **41 OF 42 STRUCK** | The Supreme Court's own count of jurors struck across the six trials, quoted verbatim in a 7-2 opinion. OWNER CALL: this is a racial-strike figure. §9 of the editorial direction says evidence first and no political colour — quoting the Court's arithmetic is evidence, but the owner should decide, not me. C is the neutral alternative. |
| **C** | symbolic / minimal | **0 CONVICTIONS** | Mississippi dropped every charge with prejudice in 2020, without a conviction to its name. |

**Ship pair:** *He Spent 23 Years on Trial for Four Murders. The State Never Had a Weapon.*  +  **41 OF 42 STRUCK**

<details><summary>verified against</summary>

- `episodes/PD-2026-054-flowers/03_script/script.en.v001.md L10 ('Six trials. Four death sentences. Twenty-three years. One man.')`
- `…L24 ('There was no murder weapon — none was ever found. There was no eyewitness… no fingerprint… no confession')`
- `…L84 (SCOTUS verbatim: struck '41 of the 42 black prospective jurors that it could have struck')`
- `…L88 ('the state dropped every charge — dismissed with prejudice… without a conviction to its name')`
- `…L90 ('he was never charged with anything. Never disciplined by the bar.')`

</details>

### 5. `PD-2026-059-robosigning` · rank 40 · Wo-SvvGsv8g

> **Now:** He Paid $139,000 Cash. There Was No Mortgage. The Bank Padlocked the Door.

`201` impressions over 4.87d → **41.3/day** · CTR **0.5%** · views 3 · AVD 0.8100000000000002% · runtime 27m · published 2026-08-07

**+28.9 clicks/28d at 3%** (+63.6 at 6%)

**Why it is losing the click.** 43 impressions/day at 0.50%. Three clauses; the middle one ('There Was No Mortgage') is the contradiction but arrives second, after a figure. Bank of America — a name the whole audience knows, worth a +5 recognisable-institution bonus at the premise stage — is not in the title.

- **Core:** He Paid Cash. Bank of America Foreclosed Anyway.
- **Broad (recommended):** He Had No Mortgage. Bank of America Locked Him Out of His Own House.  ·  verb *locked*

| | kind | text | note |
|---|---|---|---|
| **A** ★ | evidence | **PAID IN FULL** | A receipt stamp. Reads instantly and is literally the document at issue. |
| **B** | evidence | **8,000 A MONTH** | A bank officer deposed that she signed seven to eight thousand foreclosure documents a month without reading them. Stronger idea, but needs the film to unpack it — test second. |
| **C** | symbolic / minimal | **$139,000 CASH** | What he paid, five years before the padlocks. |

**Ship pair:** *He Had No Mortgage. Bank of America Locked Him Out of His Own House.*  +  **PAID IN FULL**

> ⚠ AVD is 0.81% (13 seconds average view). No title fixes that. Repackage AND diagnose the first 30 seconds.

<details><summary>verified against</summary>

- `episodes/PD-2026-059-robosigning/03_script/script.en.fromcaptions.v001.md L7, L29 ('a hundred and thirty-nine thousand dollars for it, in cash')`
- `…L11 ('Bank of America's crews had emptied it… and when the bank's own agent told them they had the wrong house, they carried on anyway')`
- `…L37 ('When the Cardosos paid cash, no lender was involved'), L55, L85 (padlocked)`
- `…L359 ('she signed seven to eight thousand foreclosure documents a month without reading them')`

</details>

### 6. `PD-2026-060-surfside` · rank 45 · dNhu-IJUc5k

> **Now:** The Repair Money Was Due July 1. The Building Fell June 24. 98 Died.

`165` impressions over 3.87d → **42.6/day** · CTR **0.61%** · views 2 · AVD 102.24% · runtime 35m · published 2026-08-08

**+28.5 clicks/28d at 3%** (+64.3 at 6%)

**Why it is losing the click.** 45 impressions/day at 0.61%. The title is date arithmetic the viewer has to perform before feeling anything, and its subject is 'The Repair Money'. The film's real contradiction is that it was all written down, three years early.

- **Core:** An Engineer Wrote It Down in 2018. The Building Came Down in 2021.
- **Broad (recommended):** They Knew the Garage Was Failing for Three Years. 98 People Were Asleep Inside.  ·  verb *knew*

| | kind | text | note |
|---|---|---|---|
| **A** | human emotion | **1:22 AM** | The hour it came down, on people asleep. |
| **B** ★ | evidence | **DUE JULY 1** | A date on an assessment notice. The building fell June 24 — the thumbnail supplies the seven days the title deliberately withholds. |
| **C** | symbolic / minimal | **$9.1M TO $15M** | What two and a half years of discussion did to the repair estimate. |

**Ship pair:** *They Knew the Garage Was Failing for Three Years. 98 People Were Asleep Inside.*  +  **DUE JULY 1**

<details><summary>verified against</summary>

- `episodes/PD-2026-060-surfside/03_script/script.en.v003.md L11 ('Ninety-eight of them died'; 'about half past one in the morning')`
- `…L109-115 (Morabito, October 2018, 'major' structural damage, 'abundant concrete cracking and spalling')`
- `…L202 ('Two and a half years had turned nine point one million into fifteen')`
- `…L231 (April 2021 board letter: 'has gotten significantly worse')`
- `…L235 ('Owners had until the first of July'), L255 ('The building came down on the twenty-fourth of June')`

</details>

### 7. `PD-2026-049-strieff` · rank 31 · 2pLWw_vhfI8

> **Now:** The Stop Was Illegal — the Supreme Court Kept the Evidence Anyway

`441` impressions over 10.87d → **40.6/day** · CTR **1.36%** · views 5 · AVD 29.5% · runtime 11m · published 2026-08-01

**+18.6 clicks/28d at 3%** (+52.7 at 6%)

**Why it is losing the click.** 41 impressions/day at 1.36%. The subject of the sentence is 'The Stop'. There is no person and no consequence, and the em-dash costs a clause break on a phone.

- **Core:** Utah Admitted the Stop Was Illegal. The Evidence Stayed In.
- **Broad (recommended):** Police Had No Reason to Stop Him. He Lost the Case Anyway.  ·  verb *lost*

| | kind | text | note |
|---|---|---|---|
| **A** | human emotion | **HE WAS WALKING** | All he did was leave a house and cross a parking lot. |
| **B** ★ | evidence | **ONE OLD WARRANT** | A database line for an unpaid traffic matter — the entire mechanism, as a record. |
| **C** | symbolic / minimal | **ILLEGAL BUT ADMITTED** | Reads as legalese at thumbnail size; keep as a fallback only. |

**Ship pair:** *Police Had No Reason to Stop Him. He Lost the Case Anyway.*  +  **ONE OLD WARRANT**

<details><summary>verified against</summary>

- `episodes/PD-2026-049-strieff/03_script/script.en.v001.md L45 ('He could not point to a single fact about Strieff himself. Later, in court, the state of Utah admitted it.')`
- `…L47 ('Strieff had an outstanding arrest warrant. Not for anything dramatic. It was a small wa[rrant]')`
- `…L8 (5-3; Thomas majority; Sotomayor and Kagan dissents)`

</details>

### 8. `PD-2026-039-frazier` · rank 30 · X40EbUw5kzQ

> **Now:** Detectives Told Him His Cousin Had Confessed. It Was a Lie, and the Court Allowed It.

`444` impressions over 18.87d → **23.5/day** · CTR **0.45%** · views 4 · AVD 31.47% · runtime 12m · published 2026-07-24

**+16.8 clicks/28d at 3%** (+36.6 at 6%)

**Why it is losing the click.** THE CLEAREST PACKAGING ERROR IN THIS HALF. The title sells Frazier v. Cupp — the cousin-confessed lie, a doctrine case. The film's emotional spine is Barry Laughman: IQ 70, the comprehension of a ten-year-old, told his fingerprints were at the scene when there were none, sixteen years, in at twenty-five and out at forty. The title is selling the footnote and hiding the man. 0.45% CTR.

- **Core:** Police Told Him His Fingerprints Were at the Scene. There Were No Fingerprints.
- **Broad (recommended):** Police Told Him a Lie He Could Not Check. He Lost 16 Years.  ·  verb *lost*

| | kind | text | note |
|---|---|---|---|
| **A** | human emotion | **IN 25 OUT 40** | The two ages, side by side. |
| **B** ★ | evidence | **NO FINGERPRINTS** | Two words, verbatim from the film's fourth line. The title names a lie; the thumbnail names it exactly. |
| **C** | symbolic / minimal | **IQ 70** | Blunt. Use only if the owner is comfortable leading with it. |

**Ship pair:** *Police Told Him a Lie He Could Not Check. He Lost 16 Years.*  +  **NO FINGERPRINTS**

<details><summary>verified against</summary>

- `episodes/PD-2026-039-frazier/08_edit/captions.final.v001.srt cues 4-6 ('What they had told him was that his fingerprints were at the scene. There were no fingerprints.')`
- `…cues 29-31 ('A twenty-four-year-old man who lived nearby, with an IQ of 70, who functioned… at roughly the level of a ten-year-old child')`
- `…cues 154-155 ('Sixteen years. He had gone in at twenty-five and come out at forty.')`
- `…cues 93-97 (Frazier v. Cupp: the cousin Jerry Lee Rawls lie — the doctrine, not the protagonist)`

</details>

### 9. `PD-2026-036-williams` · rank 25 · gR_nzXIyIlk

> **Now:** A Computer Picked His Face Out of a Blurry Still. He Spent 30 Hours in a Cell.

`575` impressions over 21.87d → **26.3/day** · CTR **1.04%** · views 10 · AVD 9.9% · runtime 11m · published 2026-07-21

**+14.4 clicks/28d at 3%** (+36.5 at 6%)

**Why it is losing the click.** 26 impressions/day at 1.04%. 'A Computer Picked His Face' is abstract where the film is not: he was taken off his own lawn while his daughters watched. The emerging-category bet (algorithms) is worth protecting with a better sentence.

- **Core:** Face-Matching Software Named an Innocent Man. Detroit Arrested Him on His Own Lawn.
- **Broad (recommended):** A Computer Was Wrong About His Face. Police Arrested Him in Front of His Daughters.  ·  verb *wrong*

| | kind | text | note |
|---|---|---|---|
| **A** | human emotion | **ON HIS LAWN** | Where it happened, and who saw it. |
| **B** ★ | evidence | **30 HOURS** | Time in a cell, as a booking figure. Title drops the number so the thumbnail can carry it. |
| **C** | symbolic / minimal | **A BLURRY FRAME** | The single piece of evidence the whole arrest rested on. |

**Ship pair:** *A Computer Was Wrong About His Face. Police Arrested Him in Front of His Daughters.*  +  **30 HOURS**

> ⚠ AVD is 9.9% (70 seconds). The packaging is not the only problem; the opening is losing people.

<details><summary>verified against</summary>

- `episodes/PD-2026-036-williams/03_script/script.en.v001.md L24 ('the better part of two days inside it — about thirty hours')`
- `…L31 (2018 downtown watch shop theft; the only witness was a camera)`
- `…L64 ('the look on his daughters' faces on that lawn')`
- `…L74 (grade-B figures hedged and kept off-screen: ~$3,800 theft, ~$300,000 settlement — do not put either on a thumbnail)`

</details>

### 10. `PD-2026-015-theranos` · rank 28 · LXFjJqE6vKU

> **Now:** The Machine Never Worked. The Company Was Valued at $9 Billion Anyway.

`479` impressions over 28.0d → **17.1/day** · CTR **0%** · views unavailable · AVD unavailable · runtime 12m · published 2026-06-30

**+14.4 clicks/28d at 3%** (+28.7 at 6%)

**Why it is losing the click.** MEASURE BEFORE REWRITING. Studio reports 0.00% CTR on 479 impressions, but this row's views, AVD and subscriber fields are all 'unavailable' — that pattern reads as a Studio data gap, not a real zero. The title already uses house grammar and the 'never' verb. Confirm the number is real before spending an owner approval on it.

- **Core:** Theranos Was Valued at $9 Billion. The Edison Never Ran the Tests It Promised.
- **Broad (recommended):** Investors Put In Hundreds of Millions. The Machine Never Worked.  ·  verb *never*

| | kind | text | note |
|---|---|---|---|
| **A** | human emotion | **EVERYONE BELIEVED HER** | The rise, not the fall. |
| **B** ★ | evidence | **4 COUNTS 11 YEARS** | Verdict and sentence as a docket line. |
| **C** | symbolic / minimal | **$9 BILLION** | Peak valuation; the title drops it so the thumbnail can hold it. |

**Ship pair:** *Investors Put In Hundreds of Millions. The Machine Never Worked.*  +  **4 COUNTS 11 YEARS**

> ⚠ Verify the 0.00% CTR in Studio first. If it is a reporting gap, this film drops out of the batch.

<details><summary>verified against</summary>

- `episodes/PD-2026-015-theranos/03_script/script.en.v001.md L19 ('valued at roughly nine billion dollars')`
- `…L12 ('the investors who put in hundreds of millions')`
- `…L43 ('four counts of fraud against investors'), L49 ('about eleven years and three months in federal prison')`
- `…L17 (the device, called the Edison)`

</details>

### 11. `PD-2026-007-riley` · rank 21 · XWYWAgkExH4

> **Now:** Police Took His Phone at Arrest and Opened It. The Supreme Court Said 9-0: Get a Warrant.

`687` impressions over 28.0d → **24.5/day** · CTR **1.02%** · views 8 · AVD 17.91% · runtime 10m · published 2026-06-22

**+13.6 clicks/28d at 3%** (+34.2 at 6%)

**Why it is losing the click.** 24.5 impressions/day at 1.02%. The payoff clause is '9-0: Get a Warrant' — a procedural score and an instruction to police. Neither is a consequence for the viewer.

- **Core:** Police Opened His Phone at Arrest. Not One Justice Said They Could.
- **Broad (recommended):** Police Took His Phone and Read Everything on It. Then Every Justice Said No.  ·  verb *took*

| | kind | text | note |
|---|---|---|---|
| **A** | human emotion | **STRAIGHT FROM HIS POCKET** | What the officer physically did. |
| **B** ★ | evidence | **WARRANT NONE** | A blank field on a form. The house evidence look, and it does not repeat a word of the title. |
| **C** | symbolic / minimal | **9 TO 0** | Already used by the current title; keep only as a control variant. |

**Ship pair:** *Police Took His Phone and Read Everything on It. Then Every Justice Said No.*  +  **WARRANT NONE**

<details><summary>verified against</summary>

- `episodes/PD-2026-007-riley/03_script/script.en.v001.md L15 ('an officer takes the smartphone out of his pocket')`
- `…L17 (photos, videos, contacts read at the scene and again at the station)`
- `…L37 ('In 2014, the Supreme Court ruled, and not one justice dissented')`

</details>

### 12. `PD-2026-019-varsityblues` · rank 24 · j8U8c4BB_GQ

> **Now:** He Sold a Side Door Into America's Best Universities. 33 Parents Walked Through It.

`575` impressions over 28.0d → **20.5/day** · CTR **1.22%** · views 8 · AVD 25.53% · runtime 27m · published 2026-07-04

**+10.2 clicks/28d at 3%** (+27.5 at 6%)

**Why it is losing the click.** 20 impressions/day at 1.22%. 'Side Door' is the film's own coinage and means nothing before you have watched it — the title spends its first four words on an in-joke. The money is absent.

- **Core:** One Man Sold a Side Door Into Elite Admissions. Fifty People Were Arrested in a Single Morning.
- **Broad (recommended):** Their Children Never Earned Those Places. Their Parents Paid $25 Million for Them.  ·  verb *never*

| | kind | text | note |
|---|---|---|---|
| **A** | human emotion | **THE FBI KNOCKED** | The morning it ended. |
| **B** ★ | evidence | **50 ARRESTED** | One morning, one figure, an arrest log. |
| **C** | symbolic / minimal | **33 PARENTS** | The count charged in the initial case. |

**Ship pair:** *Their Children Never Earned Those Places. Their Parents Paid $25 Million for Them.*  +  **50 ARRESTED**

<details><summary>verified against</summary>

- `episodes/PD-2026-019-varsityblues/03_script/script.en.v001.md L27 ('Wealthy parents paid Singer about twenty-five million dollars')`
- `…L58 ('Prosecutors traced roughly twenty-five million dollars flowing to Singer from parents')`
- `…L29, L145 ('fifty people were arrested at once')`
- `…L112 ('in the initial case alone, thirty-three of them')`

</details>

### 13. `PD-2026-050-centralpark` · rank 53 · _8DaMu8_yFw

> **Now:** Five Children Confessed to a Crime They Didn't Commit. There Was No Evidence.

`107` impressions over 7.87d → **13.6/day** · CTR **0.93%** · views 1 · AVD 1.45% · runtime 61m · published 2026-08-04

**+7.9 clicks/28d at 3%** (+19.3 at 6%)

**Why it is losing the click.** 14 impressions/day at 0.93% and the largest external-feed potential in this half — the one premise here that other channels already link to. The current title states the outcome twice ('a crime they didn't commit' / 'there was no evidence') and leaves no gap for the thumbnail.

- **Core:** Five Boys Confessed on Camera. The DNA Named One Man Who Was Not Among Them.
- **Broad (recommended):** Five Children Confessed and Every Word Was Wrong. The DNA Named One Man.  ·  verb *wrong*

| | kind | text | note |
|---|---|---|---|
| **A** ★ | evidence | **THE CAMERA WAS OFF** | The film's own closing instruction to the viewer, and it is a record: the hours that produced the confessions were the hours nobody taped. Recommended over B because it supplies the mechanism the title withholds. |
| **B** | evidence | **13 YEARS $41M** | Years served and the 2014 settlement, as a ledger line. |
| **C** | symbolic / minimal | **AGED 14 TO 16** | The five ages. |

**Ship pair:** *Five Children Confessed and Every Word Was Wrong. The DNA Named One Man.*  +  **THE CAMERA WAS OFF**

> ⚠ 61-minute runtime. Repackaging cannot carry a film that long to a cold audience; treat the title as one lever of two.

<details><summary>verified against</summary>

- `episodes/PD-2026-050-centralpark/03_script/script.en.v001.md L45 (Richardson 14, Santana 14, McCray 15, Salaam 15, Wise 16)`
- `…L91 ('words that were fed to him off-camera over the hours the tape does not [show]'), L221 ('Remember the camera that was off')`
- `…L119-121 ('They will not be believed for thirteen years')`
- `…L185 ('The convictions stayed vacated. The DNA still said one man.')`
- `…L187 ('in 2014 that the city settles, for a sum of about forty-one million dollars')`

</details>

### 14. `PD-2026-045-cleveland` · rank 42 · AxOlQ2NIaBU

> **Now:** She Owed $1,554 in Traffic Fines. Alabama Jailed Her Until She Had Sat It Off.

`193` impressions over 12.87d → **15.0/day** · CTR **1.55%** · views 13 · AVD 48.2% · runtime 11m · published 2026-07-30

**+6.1 clicks/28d at 3%** (+18.7 at 6%)

**Why it is losing the click.** 15 impressions/day at 1.55% — already above the catalogue median, so this is the lowest-urgency rewrite in the batch. The reason to do it is that the title omits the hidden system: a private for-profit probation company took its supervision fee out of her payments before the fine.

- **Core:** She Owed $1,554 in Traffic Fines. A Private Company Took Its Cut First.
- **Broad (recommended):** A Private Company Took Its Fee Before Her Fine. Alabama Jailed Her for the Rest.  ·  verb *took*

| | kind | text | note |
|---|---|---|---|
| **A** | human emotion | **JAILED FOR BEING POOR** | Close to the current thumbnail; do not ship both. |
| **B** | evidence | **$40 A MONTH** | The supervision fee, as a line on a payment schedule. |
| **C** ★ | evidence | **$1,554 31 DAYS** | The debt and the sentence, together, as a court record. Strongest single artefact. |

**Ship pair:** *A Private Company Took Its Fee Before Her Fine. Alabama Jailed Her for the Rest.*  +  **$1,554 31 DAYS**

<details><summary>verified against</summary>

- `episodes/PD-2026-045-cleveland/03_script/cleveland_facts.v001.json F04 (jailed over fines and fees totalling about $1,554; verified, high)`
- `…F05 (roughly 31 days to sit out the debt, no ability-to-pay hearing; verified, high)`
- `…F06 (Judicial Correction Services added a ~$40/month supervision fee; verified, high)`
- `…F07 (~$200 monthly payments split so a portion went to JCS before the fine; verified, medium — hedge if used on screen)`
- `episodes/PD-2026-045-cleveland/03_script/script.en.v001.md L126 ('those thirty-one days were only ever a punishment for what Harriet Cleveland did not have')`

</details>

### 15. `PD-2026-024-rajaratnam` · rank 32 · rYV4rxtQCV0

> **Now:** A Billionaire Heard His Own Voice on an FBI Tape Built for the Mafia.

`396` impressions over 28.0d → **14.1/day** · CTR **1.52%** · views 11 · AVD 15.289999999999997% · runtime 28m · published 2026-07-09

**+5.9 clicks/28d at 3%** (+17.7 at 6%)

**Why it is losing the click.** LOWEST PRIORITY OF THE FIFTEEN. 13 impressions/day at 1.52%, and the protagonist is a billionaire — v002's centre is an ordinary person meeting an invisible system, and there is no daily contact point here. Rewrite it only if the batch is already open. One sentence, no consequence, no figure.

- **Core:** The FBI Used Mob Wiretaps on Wall Street. A Billionaire Got Eleven Years.
- **Broad (recommended):** He Ran a $7 Billion Fund. His Own Voice Cost Him Eleven Years.  ·  verb *cost*

| | kind | text | note |
|---|---|---|---|
| **A** | human emotion | **THEY PRESSED PLAY** | The grey room, the recorder, the moment. |
| **B** ★ | evidence | **29 CHARGED** | The wider Galleon sweep, as a charging figure. |
| **C** | symbolic / minimal | **A MOB WIRETAP** | Names the method: a power that for decades had been pointed at organized crime, not at a trading desk. |

**Ship pair:** *He Ran a $7 Billion Fund. His Own Voice Cost Him Eleven Years.*  +  **29 CHARGED**

<details><summary>verified against</summary>

- `episodes/PD-2026-024-rajaratnam/03_script/script.en.v001.md L22 ('a hedge fund called Galleon. At its peak it managed about seven billion dollars. He was a billionaire.')`
- `…L208 ('on October thirteenth, 2011… Eleven years in federal prison')`
- `…L216 ('charges against twenty-nine people and firms across the wider Galleon investigation')`
- `…L149 (wiretap application), L226 (2013 appeals court upheld the wiretaps)`

</details>

---

## 5. (a2) Rewrite only if a batch is already open — 2 films

*Real packaging defects, but the exposure does not justify opening an approval cycle for them alone.*

- **`PD-2026-028-forfeiture`** · rank 38 · 8.2/day · CTR 0.43% — Strong premise (a paid-off house seized after a $40 sale by the son, parents never charged) wearing a 0.43% title that never says the house was paid off. Worth a rewrite if a batch is already open — 8.2 impressions/day does not justify opening one.
- **`PD-2026-011-mahanoy`** · rank 41 · 7.0/day · CTR 0.51% — 0.51% at 7 impressions/day. A cheerleader's Snapchat is a real contradiction but the stake is a place on a squad, which is the smallest human stake in the whole catalogue.

---

## 6. Hold — packaging is not the binding constraint — 9 films

Weighted CTR **3.39%** against a catalogue median of 1.28%. These are the counter-evidence to "the tail is a packaging failure": they are packaged well and still starved of views. **Recommendation: change nothing.** Their constraint is distribution, which is the other half of the owner's problem.

| episode | rank | imp/day | CTR | why hold |
|---|---|---|---|---|
| `PD-2026-057-fieldtest` | 56 | 75.9 | **4.55%** | 4.55% — the highest CTR in this half and the second highest in the catalogue. One day old. |
| `PD-2026-017-onecoin` | 26 | 19.9 | **3.76%** | 3.76% on 558 impressions. Rewriting this risks a regression for no measured reason. |
| `PD-2026-038-kidsforcash` | 43 | 8.7 | **2.89%** | 2.89%. Packaging works; 9 impressions/day is the constraint. |
| `PD-2026-044-tekoh` | 37 | 20.0 | **2.88%** | 2.88% on 278 impressions in 13 days. |
| `PD-2026-018-flashcrash` | 34 | 10.2 | **2.79%** | 2.79%. Exposure, not packaging. |
| `PD-2026-009-timbs` | 22 | 22.8 | **2.51%** | 2.51% on 638 impressions — the best-performing old film in this half. |
| `PD-2026-008-carpenter` | 23 | 22.3 | **2.24%** | 2.24% on 625 impressions. |
| `PD-2026-027-rodriguez` | 29 | 16.3 | **2.19%** | 2.19% on 457 impressions. |
| `PD-2026-040-lech` | 48 | 7.9 | **2.13%** | 2.13%, but only 141 impressions in 17 days. |

---

## 7. (b) Weak premise — no title will save it — 2 films

*No title will save these. Both have live exposure, so the failure is not distribution.*

### `PD-2026-046-tlo` · rank 46 · 16.1/day · CTR 1.89% · v002 score **54** — REJECT

The student was in fact carrying what the search found, so the reversal the format needs never arrives; and a school-search doctrine aims at parents of teenagers, a demographic PD does not have (measured audience 92.5% male, 77% aged 55+). Its 1.89% CTR is already above median — the premise, not the packaging, is the ceiling.

### `PD-2026-026-katz` · rank 27 · 18.2/day · CTR 1.77% · v002 not scored

Not scored: a 1965 phone booth is a museum object, and the contradiction is doctrinal — the trespass rule, not a person's loss. 1.77% CTR at 18 impressions/day means the packaging is already doing more than the premise deserves. Do not make more of these.

---

## 8. (c) Below the view floor — named, then set aside — 9 films

*Under ~6 impressions/day. YouTube has effectively stopped serving them. Named here and then set aside.*

| episode | rank | imp/day | CTR | v002 | note |
|---|---|---|---|---|---|
| `PD-2026-002-gideon` | 57 | 2.3 | 0% | **67** REJECT | Scored REJECT 67. Outcome is uplifting, which drains the expectation gap. |
| `PD-2026-025-kyllo` | 55 | 2.5 | 1.45% | — | 2.4 impressions/day. Doctrine-first selection; no ordinary loss. |
| `PD-2026-003-mapp` | 54 | 3.1 | 0% | — | 3.1 impressions/day, 0.00% CTR. Landmark case, chosen system-first. |
| `PD-2026-012-arbitration` | 52 | 4.1 | 2.63% | **63** REJECT | Scored REJECT 63. Highest personal relevance in this group (14/15) and the lowest story arc (3/10): nothing happens to anybody. |
| `PD-2026-004-ftx` | 51 | 4.2 | 2.54% | — | 4.2 impressions/day. Famous premise, but 118 impressions is not an audience. |
| `PD-2026-013-king` | 49 | 4.8 | 0% | **57** REJECT | Scored REJECT 57. The viewer sides with the police: the swab caught a rapist. |
| `PD-2026-031-unlock` | 50 | 4.7 | 2.36% | **50** REJECT | Scored REJECT 50, the lowest in this half. genome protagonist_type = no_single_protagonist — there is no person in the film at all. |
| `PD-2026-010-kelo` | 47 | 5.2 | 0.69% | — | 5.2 impressions/day. Good bleak premise, no exposure left to convert. |
| `PD-2026-001-miranda` | 44 | 5.9 | 1.21% | — | 5.9 impressions/day. Everyone already knows the warning; there is no gap to open. |

Seven of these nine share one shape: they were selected **system-first** — a landmark doctrine, then a person found to illustrate it. That is precisely the selection rule `PD_EDITORIAL_DIRECTION.v002` §1 inverts (`person → abnormal event → why? → system`, never `system → person`). The tail of this catalogue is, in large part, the record of the old selection rule. Nothing in this bucket needs an owner decision; it needs to not be repeated.

---

## 9. Premise scoring — what the numbers are and are not

No published episode has a premise file on disk -- config/pd_premise_seeds.v001.json holds forward-looking seeds only. The five scores above were produced by writing a premise JSON reconstructed from that film's genome record and script and running scripts/score_premise.py --os v002. The axis scores are my judgement, not a measurement; the rubric arithmetic, normalisation and gate are the tool's. Scored as a control, PD-2026-053-norfolk returns 108 (PRIORITY), so the rubric does separate these films rather than rejecting everything.

Reconstructed premise JSONs were written to a scratch directory, not to the repository, because they are my reading of a finished film rather than an artefact any episode declared. Re-runnable with `py -3.11 scripts/score_premise.py --os v002 --score <premise>.json`.

---

## 10. One repository conflict, reported not fixed

docs/PD_EDITORIAL_DIRECTION.v002.md s3 says the v002 rubric 'is NOT yet the default gate'. scripts/score_premise.py --help states v002 IS the default and binding gate, switched by the owner on 2026-08-12. Per CLAUDE.md s5 the running code is the operative source; the document should be corrected rather than the code changed. Reported, not fixed.

---

## 11. What I did not do

- **Nothing was changed on YouTube.** No title, no thumbnail, no description, no metadata call of any kind.
- No render, build, GPU or upload was run; `topic_demand_probe.py` was not run and no quota was spent.
- No thumbnail image was generated. Section 4 specifies text and concept; the image is a separate production step.
- `_finish_episode.sh` and `queue_unattended.sh` were not touched.

**Next decision the owner owns:** approve or amend the six-film first batch (norfolk, burge, postoffice, flowers, robosigning, surfside), which is 72% of the available return and the only part of this proposal with a deadline — those films are in their launch window now.
