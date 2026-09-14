# LANE GAP ANALYSIS — competitive map for topic selection
**Version:** v001 · **Date:** 2026-07-29 · **Author:** research agent (read-only pass)
**Purpose:** map what is currently winning in PD's adjacent lanes and where the open gaps are, so a sibling process can select topics. **This document does not select topics.**

---

## 0. Method, provenance, and honesty statement

### 0.1 What is MEASURED
All view counts, subscriber counts, runtimes, publish dates and derived multiples in this document were pulled **directly from the YouTube Data API v3** (`search.list`, `videos.list`, `channels.list`, `playlistItems.list`) on **2026-07-29**, using the repo's existing read-only OAuth credentials. No scraping, no estimates, no LLM recall. Three scans:

| Scan | Method | Result |
|---|---|---|
| **Lane scan** | 61 `search.list` queries across 5 adjacent lanes, `publishedAfter=2025-01-01`, `order=viewCount`, long + medium duration passes | **674 unique videos** hydrated with full statistics |
| **Channel scan** | 33 PD-comparable channels resolved by handle → full uploads playlist → per-video statistics | **2,982 videos** with **within-channel outperformance multiples** |
| **White-space scan** | 32 candidate subject areas + 10 saturation probes, supply counted by long-form (≥15 min) video count and max views | supply/demand table per area |

The **primary metric is the within-channel multiple** (`video views ÷ that channel's median video views`). This controls for channel size, format and audience, and is the same metric family PD's own `CTR_GROWTH_REFERENCE.v001.md` settled on. Raw views/day is reported alongside but is **not** the ranking metric.

Raw data retained at `…/scratchpad/lane_scan_raw.json`, `chan_scan.json`, `ws_scan.json` (scratchpad is ephemeral — regenerate with `lane_scan.py` / `chan_scan.py` / `ws_scan.py` / `sat.py` in the same directory). **Note:** the fourth scan (`sat.py`) hit the daily quota mid-run and never wrote `sat.json`; its results for `open_fields`, `occ_licensing` and `rental_inspection` were captured from stderr only, which is why two supply citations in §3 give title + view count without a video ID.

### 0.2 What is INFERRED
Every inference in this document is tagged **[INFERENCE]**. Where I could not measure something, I say so rather than estimating.

### 0.3 Known limitations — read these before acting
1. **The YouTube Data API daily search quota was exhausted** partway through the saturation probes (10,000 units). Saturation was directly verified for `open_fields`, `occ_licensing` and `rental_inspection` only. The other white-space areas' supply figures come from the earlier 32-area scan, which used a single query each — **a single query is weaker evidence than a dedicated saturation probe.** Supply claims marked ⚠ are single-query.
2. **The WebSearch budget was already exhausted (200/200) before this session began.** This is the same recurring constraint logged in `DEEP_RESEARCH_FINDINGS.v001.md`. I therefore have **no independent news-volume or Google-Trends evidence** for any area. All demand evidence in this document is YouTube-internal (view counts on adjacent videos). This is a real weakness: an area could show YouTube demand without broader news salience, or vice versa. **Anything below that says "demand" means "measured YouTube demand", not "search interest" or "news volume".** A sibling with search budget should re-verify the top 3 before greenlight.
3. **`ij.org` returns HTTP 403 to WebFetch**, so IJ's litigation docket could not be read directly. IJ evidence here is entirely their YouTube catalog.
4. Search-based supply counts undercount: YouTube search is relevance-ranked and language-filtered, so "no long-form exists" always means "none surfaced in the top 20–25 for this query", never a census.
5. Subscriber counts are rounded by the API (YouTube publishes 3 significant figures). Multiples using subs are correspondingly coarse.

---

## 1. WINNER TABLE — recent outperformers in adjacent lanes

Ranked by **within-channel multiple** (`mult`), restricted to uploads **2025-05-01 → 2026-07-29**, filtered to PD-adjacent lanes. Bodycam-gore and movie-recap channels were excluded by filter; they dominate raw views but are not PD's lane (see §2.5).

| # | Video | Channel (subs) | Views | mult | Runtime | Uploaded | Format |
|---|---|---|---|---|---|---|---|
| 1 | [James Bulger: Britain's Most Shocking Child Murder Case](https://youtu.be/MQSqm5EP_Q8) | The Crime Agents (23.7k) | 299,734 | **30.18×** | 46m | 2026-05-21 | ex-detective narrative doc |
| 2 | [Teen Smiles in Court, Thinks Family's With Her — Until They Speak](https://youtu.be/eSEgraXrFzg) | Women Of Crime (135k) | 3,371,738 | **23.22×** | 28m | 2025-11-04 | courtroom-footage narrative |
| 3 | [The SHOCKING story of a police officer involved in a GROOMING GANG](https://youtu.be/i2988fuXQY0) | The Crime Agents (23.7k) | 228,329 | **22.99×** | 36m | 2025-12-12 | institutional failure, UK |
| 4 | [It's Just a Box—So Why Is It Illegal to Sell?](https://youtu.be/IIZUmFKirdk) | Institute for Justice (521k) | 1,039,605 | **18.65×** | 3m | 2026-02-05 | occupational licensing |
| 5 | [Mandelson, Epstein & Andrew: Protected By POWER?](https://youtu.be/C-X4HJeWzMU) | The Crime Agents (23.7k) | 167,154 | **16.83×** | 35m | 2026-02-12 | elite-impunity, UK |
| 6 | [Game Wardens Caught Trespassing on Land](https://youtu.be/Je8mOkgMoWk) | Institute for Justice (521k) | 911,006 | **16.34×** | 5m | 2025-05-21 | open-fields doctrine |
| 7 | [Lucy Letby: Guilty or WITCH HUNT?](https://youtu.be/t8aGtOX8Q4Q) | The Crime Agents (23.7k) | 161,517 | **16.26×** | 46m | 2026-02-05 | contested conviction, UK |
| 8 | [Grandma "Kidnapped" by US Marshals (BODYCAM)](https://youtu.be/3J6SBmLyfG8) | Institute for Justice (521k) | 838,434 | **15.04×** | 6m | 2025-06-10 | wrong-person federal raid |
| 9 | [Former Head of Counter-Terror Breaks Down the Ann Widdecombe Investigation](https://youtu.be/biWD_loxJ1c) | The Crime Agents (23.7k) | 116,572 | **11.74×** | 37m | 2026-07-14 | expert-led investigation |
| 10 | [Britain's Illegal Children's Homes EXPOSED](https://youtu.be/k9RpSf6A8zc) | The Crime Agents (23.7k) | 106,766 | **10.75×** | 15m | 2026-04-02 | institutional failure, UK |
| 11 | **[Another Game Warden Caught Spying: "This is a real problem"](https://youtu.be/tyeF77uNjW0)** | Institute for Justice (521k) | 593,978 | **10.66×** | **33m** | 2025-07-22 | **long-form open-fields doc** |
| 12 | [The Horrific School Shooting and the Worst Police Response](https://youtu.be/Dm9GkTYvzs8) | Dire Trip (918k) | 2,787,636 | **9.66×** | 115m | 2025-11-23 | institutional failure (Uvalde) |
| 13 | [LegalEagle — Prosecutor Reacts to Afroman Trial](https://youtu.be/0pvJmxe7LdE) | LegalEagle (3.94M) | 3,725,462 | **6.63×** | 29m | 2026-03-21 | wrong-raid → countersuit |
| 14 | [ARRESTED for Telling Trespasser to Get Off Porch (BOGUS Warrant)](https://youtu.be/0hTQIAsDHX0) | Institute for Justice (521k) | 360,969 | **6.48×** | 35m | 2025-06-20 | bogus-warrant arrest |
| 15 | [City Cops Pull Over Sheriff's Deputy And It Goes TERRIBLY WRONG!](https://youtu.be/ntQTCT6xdYU) | Audit the Audit (2.98M) | 3,223,349 | **5.88×** | 27m | 2025-09-22 | police-vs-police accountability |
| 16 | [BIG WIN: Town Banned from Warrantless Inspections](https://youtu.be/BjztA-fIvXg) | Institute for Justice (521k) | 307,290 | **5.51×** | 28m | 2026-01-22 | warrantless home inspection |
| 17 | [Cop Assaults AN ATTORNEY Then The ENTIRE DEPARTMENT Gets CRUSHED By The Feds](https://youtu.be/TprIsrFtjMs) | Audit the Audit (2.98M) | 2,983,220 | **5.44×** | 33m | 2025-05-15 | villain-punished |
| 18 | [Dystopian Town Sends Lying Cop To Innocent Woman's Home](https://youtu.be/37fp2n6p19Q) | The Civil Rights Lawyer (2.0M) | 5,392,208 | **4.01×** | 14m | 2025-11-05 | present-tense false arrest |
| 19 | **[Blows a ZERO, Passes FSTs, Gets Arrested Anyway — WINS in Court (part 1)](https://youtu.be/NEpbB9BbmMI)** | The Civil Rights Lawyer (2.0M) | 5,037,384 | **3.75×** | **34m** | 2026-05-14 | **sober-DUI false arrest** |
| 20 | [I Help YouTuber Arrested Over Lego Videos (Part 1)](https://youtu.be/Hs3bElrHKUE) | The Civil Rights Lawyer (2.0M) | 4,991,894 | **3.71×** | 57m | 2026-06-02 | serialized present-tense case |
| 21 | **[Blows a ZERO, Gets Arrested Anyway — WINS in Court (part 2)](https://youtu.be/DWCEssxYVC0)** | The Civil Rights Lawyer (2.0M) | 4,728,822 | **3.52×** | **38m** | 2026-05-16 | **sober-DUI, part 2 holds** |
| 22 | [Politician Destroys Mechanic's Livelihood](https://youtu.be/DLKK0A0gZHU) | Institute for Justice (521k) | 198,847 | **3.57×** | 3m | 2025-09-29 | occupational licensing |
| 23 | [Roller Coaster Crash at Full Speed: The Smiler Alton Towers Disaster](https://youtu.be/Z3SxRQe9dDs) | Plainly Difficult (1.1M) | 739,635 | **3.00×** | 19m | 2025-07-26 | cost-cutting disaster |
| 24 | [How Police Around the Country Are Conducting Mass Surveillance](https://youtu.be/4xU5AhwarSs) | Institute for Justice (521k) | 149,469 | **2.68×** | 32m | 2025-10-31 | ALPR / mass surveillance |
| 25 | [A Life-Changing Mistake: The Smiler Crash](https://youtu.be/y-KwjtMMxAg) | Fascinating Horror (1.44M) | 1,001,598 | **2.30×** | 12m | 2026-01-20 | cost-cutting disaster |
| 26 | [Cop's Lies Sent Innocent Girls to Prison…Still Employed.](https://youtu.be/rf_NetF2l9k) | Institute for Justice (521k) | 123,464 | **2.22×** | 44m | 2025-08-25 | villain-**un**punished |

**Non-comparable outlier, flagged for honesty:** [Conviction or Conspiracy: The Trevor Milton Saga](https://youtu.be/B1NOofxXSAc) — 28,202,968 views, 107 min, uploaded 2025-06-10, on a channel with **9,720 subscribers** (views-per-subscriber = 2,901). **[INFERENCE]** A 2,901× views-per-sub ratio is not organically achievable; this is almost certainly paid promotion funded by the documentary's subject, who is a wealthy exonerated/pardoned executive. **Do not treat this as a topic signal.** It is a distribution signal about money, not about subject matter.

---

## 2. ARCHETYPE PERFORMANCE READ

### 2.1 Currently OVER-performing

**A. Present-tense injustice where the villain is still in place, told about an ordinary, non-criminal protagonist.**
This is the strongest and most consistent archetype in the measured set. Evidence:
- IJ's entire top tier is present-tense litigation: game wardens (16.34×, 10.66×), warrantless inspections (5.51×), bogus-warrant arrest (6.48×), wrong-grandma raid (15.04×).
- The Civil Rights Lawyer's top six 2025–26 uploads are all *this-is-happening-now* false-arrest cases (4.01×, 3.75×, 3.71×, 3.52×, 3.01×, 2.93×). [source: channel scan]
- IJ's "[Cop's Lies Sent Innocent Girls to Prison…**Still Employed**](https://youtu.be/rf_NetF2l9k)" at 2.22× / 44 min shows the **unpunished-villain** ending does *not* suppress performance — the unresolved grievance is itself the payload.

**B. The protagonist is a property owner / worker / driver — not a convict.**
Every IJ outperformer's protagonist is someone the 55+ male audience identifies *with*, not someone they judge. Landowner, mechanic, grandma, porch owner, bar owner. **[INFERENCE]** This is the cleanest mechanical explanation for why IJ, at 521k subs, generates 10–18× multiples on subject matter that PD's doctrine-explainer episodes converted at 0.5–0.8% CTR: the doctrine is identical, the *protagonist class* is not.

**C. Institutional child-protection / safeguarding failure (UK-coded).**
The Crime Agents at **23,700 subs** is producing 10–30× multiples on 35–46 min films (grooming gang 22.99×, illegal children's homes 10.75×, Bulger 30.18×). This is the single best size-matched proof in the dataset that **a small channel can win this lane with runtime and rigor rather than scale** — and it is UK-coded, which aligns with PD's measured GB/AU retention strength.

**D. The named cost-cutting decision that killed people.**
Both institutional-failure channels independently top-ranked the same event (The Smiler: 3.00× on Plainly Difficult, 2.30× on Fascinating Horror), and their title grammar is uniform: `$99 Million in Damages`, `One Faulty Weld, 123 Dead`, `A $100 Million Dollar Corner Cut`, `When Extreme Cost Cutting Leads To Disaster`. This satisfies PD's own **two-channel premise test (R-36)** on measured 2025–26 data.

**E. Serialized single case across multiple videos.**
LegalEagle's "Reckless Ben" arc (3.91×, 3.15×, 2.17×) and The Civil Rights Lawyer's two-part sober-DUI film (3.75× **then 3.52×** — part 2 retained 94% of part 1's performance) both show **multi-part does not decay** when the case is live. This is direct evidence for PD's queued **E5 multi-part pilot**.

### 2.2 Currently UNDER-performing / saturated

| Archetype | Measured evidence | Read |
|---|---|---|
| **Historical exoneration, resolved form** | Only 2 resolved-form titles in the 2,982-video within-channel pool: "Conviction Overturned After 8 Years" = **0.59×**, "Murder Conviction Has Been Overturned" = **0.50×** | ⚠ n=2 — **cannot confirm R-38, but nothing contradicts it.** See §6.1 |
| **Immigration / ICE** | On IJ, every immigration item **under**-performs: 0.81×, 0.66×, 0.56×, 0.15× — despite news clips on the same subject drawing 4.4M, 4.3M, 3.1M views | **Demand is political-outrage demand and does not transfer to rights-documentary format.** Strong caution — see §3.9 |
| **Qualified immunity as a titled subject** | IJ "Ending Qualified Immunity Will Improve Policing" = **1.32×**, near-median on its own channel | Doctrine-as-subject is weak even for the doctrine's own litigator |
| **Wrong-house SWAT raid** | IJ 1.21× and 0.29×; PD already shipped EP40 lech + EP42 young; bench holds B4 Malinowski + B5 Martin | **Internally saturated at PD before it is externally saturated** |
| **Civil asset forfeiture** | IJ 2.66×, 1.25×, 2.48× — solid but no longer top-tier for IJ; PD has shipped **four** (EP28, EP33, EP34, EP35) | Externally healthy, **internally exhausted** |
| **Police bodycam gore / interrogation** | Dominates raw views (EWU, Explore With Us, Dr Insanity at 7–20M/video) | Confirmed **most crowded entry point**; consistent with PD's prior finding. Not PD's lane and not recommended |

### 2.3 American vs international
UK-coded institutional failure is over-performing at small scale (The Crime Agents, §2.1C). US-coded property/police cases dominate the high-multiple US set. **No measured evidence either way on whether a US channel can win with UK subject matter** — that is exactly what PD's queued **E2 (EP56 Post Office)** experiment is designed to answer, and this analysis cannot substitute for it.

### 2.4 Single-victim vs systemic-scale
Every outperformer in §1 is **single-victim with systemic implication stated**, not systemic-scale-first. IJ's systemic-framed titles ("96% of PRIVATE land in the US is subject to gov't TRESPASSING", 268k) underperform their single-protagonist framings of the same litigation (911k, 594k). **[INFERENCE]** Scale belongs in Act III, never in the title.

### 2.5 Filter disclosure
The lane scan's raw top-20 by views/day is dominated by bodycam/true-crime-gore channels (EWU Bodycam, Explore With Us, Dr Insanity, Code Blue Cam) at 7–28M views/video. These were **excluded by channel- and title-regex filter** from §1 because they are a different lane with a different audience. This is an editorial judgment, disclosed so it can be reversed: if the sibling wants the gore lane mapped, the raw data is retained.

---

## 3. WHITE SPACE — ranked, with demand and supply evidence

Ranked by (demand evidence strength × supply thinness × PD fit). **Novelty column reflects a grep of all 56 shipped episode directories, their `09_package/youtube_meta*.json`, all episode research/script files, `TOPIC_PIPELINE.v001–v003.md`, and `EP41-43_TOPIC_PROPOSALS_v001.md`.**

---

### WS-1 — Open-fields doctrine: warrantless government entry and hidden cameras on private land ⭐
- **Demand (measured):** IJ has four items on this, all outperforming — [16.34× / 911k](https://youtu.be/Je8mOkgMoWk) (5m), **[10.66× / 594k at 33 min](https://youtu.be/tyeF77uNjW0)**, 998k (2023), 2.52× (13m). Independent channels: Inspector Darkmind, "Cops Trespassing on Private Property", 1,644,558; Attorney Larry Forman, 1,138,459 — both short-form. Dedicated saturation probe run.
- **Supply (measured, dedicated probe):** **2 long-form (≥15 min) videos in the entire top-20 result set.** The best is Steve Lehto, "Wildlife Officers Needed Warrant for Cameras on Private Property", 19 min, 191,446 views, uploaded 2022-10-19 (ID not captured before quota cutoff; findable by exact title). Everything else is 0–6 min clips or local news.
- **Why it's a gap:** the only ≥30-min treatment in existence is IJ's own advocacy piece, and it did **10.66× its channel median**. There is no narrative documentary.
- **PD fit:** protagonist is a landowner (archetype B). Doctrine is *Oliver v. United States* (1984) — a real Supreme Court line, PD's core competency. Live news hook: a Tennessee state ruling that the wildlife agency declined to appeal (2024).
- **Novelty:** ✅ **CLEAN.** Zero hits for "open field", "game warden", or "trespass" across the entire pipeline *and* all 56 shipped episodes.

### WS-2 — False DUI arrest of a provably sober driver / drug-recognition-expert junk science ⭐
- **Demand (measured):** The Civil Rights Lawyer's **two-part 34m + 38m** film is his #2 and #4 video of the last 14 months — [5,037,384 @ 3.75×](https://youtu.be/NEpbB9BbmMI) and [4,728,822 @ 3.52×](https://youtu.be/DWCEssxYVC0). Plus [Law&Crime "‘Dude, I Blew Zero!’: College Athlete Sues Iowa Cops" — 12,576,170, 11m](https://youtu.be/QGWSbAHaHUw), [Audit the Audit "Cop Falsely Arrests Sober College Athlete For DUI" — 3,214,133, 21m](https://youtu.be/mFuVdlKD00s), [LackLuster "100% Sober - Arrested For DUI" — 4,211,812](https://youtu.be/dI3kOu3FLW8), and short-form at [22,773,718](https://youtu.be/cn09ecbA56U) and [10,341,761](https://youtu.be/WBb0nSD3iXo) views.
- **Supply (measured):** 6 long-form ≥15 min surfaced; **all are lawyer-reaction or bodycam-commentary format.** Zero narrative documentaries. No film exists on the *drug recognition expert* certification system itself.
- **Why it's a gap:** demand is proven **at PD's exact runtime** (34–38 min), and part 2 retained 94% of part 1 — the audience will sit through a long version. The format gap is that nobody has made it a *story*.
- **PD fit:** protagonist is an ordinary driver; villain is a certification regime; there is a documented junk-science spine.
- **Novelty:** ✅ **CLEAN.** Zero hits for "DUI", "drug recognition", "breathalyz" anywhere in the pipeline or shipped episodes.

### WS-3 — Warrantless municipal / rental / code-enforcement inspection of homes ⭐
- **Demand (measured):** [IJ "BIG WIN: Town Banned from Warrantless Inspections" — 5.51×, 307,290, 28 min](https://youtu.be/BjztA-fIvXg). Adjacent IJ items: [Cities Use Bogus "Blight" to Steal Americans' Homes — 1.83×/102,015](https://youtu.be/NSoMsQiQOj4), "City tried to CONDEMN property over 2 stray cats" 1.54×/86k, "Courts Refuse To Protect Property Owners From Insane Fines" 1.07×/60k.
- **Supply (measured, dedicated probe):** the only long-form results are Steve Lehto, "City Inspectors Need Warrants Like Anyone Else", 12 min, 105,017 and "Unanimous Supreme Court Limits Home Search Exception", 11 min, 98,519 (IDs not captured before quota cutoff) — both explainer format, both 2021–23. **No narrative long-form exists.**
- **PD fit:** the most literal "the government did this to an ordinary person in their own home" subject available; direct thematic line to *Camara v. Municipal Court*.
- **Novelty:** ✅ **CLEAN** for "rental inspection", "code enforcement", "warrantless inspection". ⚠ **Partial overlap:** "blight" appears in **EP10 kelo** (research, claims, script, scenes). The *blight-designation* sub-angle is partly spent; the *inspection-warrant* angle is not.

### WS-4 — Occupational licensing: the permission slip that ends a livelihood
- **Demand (measured):** IJ's single best-performing video of the period — [18.65×, 1,039,605 views](https://youtu.be/IIZUmFKirdk) — plus [3.57× "Politician Destroys Mechanic's Livelihood"](https://youtu.be/DLKK0A0gZHU), 2.46× "Rename Your Bar…or go to JAIL", 1.46×, 0.62× salon.
- **Supply (measured):** effectively zero long-form documentary; the probe returned business-advice contamination, max on-topic long-form **2,269 views**.
- **⚠ CRITICAL CAVEAT — measured counter-evidence:** IJ published a **38-minute version of the same box story** ([0.95×, 53,004 views](https://youtu.be/ndEgQjxvcIQ)) versus the 3-minute version's **18.65× / 1,039,605**. Same story, same channel, same quarter: **the long version did 5% of the short version's audience.** This is the only case in the dataset where I can directly compare short and long treatments of one story, and **long lost badly.**
- **Read:** demand is real but **may be a short-form-only phenomenon.** Ranked 4th rather than 1st for exactly this reason. If PD builds it, the burden is to prove a 25-min narrative spine exists that the 38-min IJ version lacked.
- **Novelty:** ✅ **CLEAN.** Zero hits for "occupational licens", "licensing", "casket", "hair braid".

### WS-5 — Police mass surveillance of ordinary drivers (ALPR / plate-reader networks)
- **Demand (measured):** [IJ 32-min "How Police Around the Country Are Conducting Mass Surveillance" — 2.68×, 149,469](https://youtu.be/4xU5AhwarSs); [IJ 57-min "Landmark Supreme Court Decision: What It Means for Mass Surveillance" — 2.15×, 119,592, uploaded 2026-07-08](https://youtu.be/Ttgqp0hR1Z8); "Gov't Surveillance Cameras Found in 7 SHOCKING Spots" 1.77×.
- **Supply:** ⚠ single-query. No narrative long-form surfaced; coverage is advocacy and news.
- **PD fit:** strong doctrinal continuity with PD's shipped **EP8 carpenter** (cell-site location), **EP25 kyllo**, **EP26 katz** — but the protagonist class is different (a driver, not a suspect), which per §2.1B is the upgrade.
- **⚠ Risk:** this is the archetype PD's own data says converts worst — doctrine-forward. Must be built protagonist-first.
- **Novelty:** ✅ **CLEAN** for "ALPR", "license plate reader", "Flock". Adjacent doctrine shipped 3×.

### WS-6 — Guardianship predation: the court-appointed guardian who takes an elderly person's life and money
- **Demand:** ⚠ single-query and **contaminated** — the probe's high-view results were unrelated virals. Genuine on-topic long-form supply is thin. **[INFERENCE]** demographic fit with PD's measured 91% aged-55+ audience is the best of any area in this document; that is an inference from audience data, not a measured demand signal.
- **Supply:** thin — no well-made long-form documentary surfaced.
- **Novelty:** 🟡 **ALREADY QUEUED** — this is bench item **B11 (Rebecca Fierle)** in `TOPIC_PIPELINE.v003.md` (5 hits for "guardianship", 4 for "Fierle"). Not new; this analysis **independently corroborates** the bench ranking.

### WS-7 — Forensic pathologist / medical examiner fraud
- **Demand (measured):** the only real long-form demand is broadcast — [48 Hours "Death by Eye Drops" — 2,060,445, 41m](https://youtu.be/V7n4mpFZ8sY), [48 Hours "Addicted to Love" — 1,925,400, 41m](https://youtu.be/R2gSiUOs29s), [60 Minutes Australia "forensic doctor never qualified to be one" — 443,982, 45m](https://youtu.be/pTypFBvx2Ik).
- **Supply:** 16 long-form surfaced but only 4 above 200k, and **all four are network-broadcast**. Independent long-form supply ≈ zero.
- **Read:** demand is proven **only at broadcast-authority level**. Whether an independent channel converts it is unproven. Ranked mid.
- **Novelty:** 🟡 **PARTIALLY QUEUED** — "Fred Zain" and "Joyce Gilchrist" are named in PD's v002 reserve list (1 hit each); "medical examiner" 1 hit. The *area* is on the bench but no case is promoted.

### WS-8 — Prison / jail medical neglect death in custody
- **Demand:** ⚠ single-query; **max long-form 459 views.** Demand is **not demonstrated** by my data.
- **Supply:** essentially zero.
- **Honest read:** this is the one area where I cannot distinguish "white space" from "no demand". Listed because the supply gap is total and the subject sits squarely in PD's thesis, but **the demand evidence is absent, not positive.** Do not treat the empty supply as opportunity without independent demand verification.
- **Novelty:** ✅ CLEAN.

### WS-9 — Field drug-test false positives (roadside kits that read sugar as cocaine)
- **Demand:** ⚠ single-query; one long-form at 3,214,133 (Audit the Audit, shared with WS-2's result set).
- **Supply:** 4 long-form, 1 above 200k.
- **PD fit:** ordinary-driver protagonist, documented junk-science spine, strong "this could be you" transfer. Pairs naturally with WS-2 as a series.
- **Novelty:** ✅ **CLEAN.** Zero hits for "field drug test".

### WS-10 — Jailhouse-informant testimony as a conviction engine
- **Demand:** ⚠ single-query; max long-form 13,864 views — weak.
- **Supply:** near-zero.
- **Novelty:** 🟡 **PARTIALLY SPENT** — "jailhouse informant" already appears in the narration of **EP51 willingham** and **EP54 flowers**. Per the Harpersville precedent (a topic was hard-failed for exactly this), the strongest framing may already be on screen. Verify before building.

### WS-11 — Serialized live case, multi-part (format white space, not subject white space)
- **Demand (measured):** LegalEagle's Reckless Ben arc (3.91× / 3.15× / 2.17×) and The Civil Rights Lawyer's sober-DUI two-parter (3.75× → **3.52×**) both show near-zero decay into part 2.
- **Supply:** no channel in PD's specific lane (historical/legal narrative documentary) is doing this.
- **Novelty:** 🟡 already queued as experiment **E5** in `DEEP_RESEARCH_FINDINGS.v001.md`. This analysis supplies the **first measured justification** for it.

---

## 4. CEILING CASES — where the lane's biggest hits live, and whether PD can compete

| # | Ceiling | Evidence | Can PD compete? |
|---|---|---|---|
| **C-1** | **Network back-catalogue dumping (48 Hours / CBS)** | 48 Hours holds ~12 of the lane's top 40 by views/day; full episodes at 2.78M, 4.82M, 2.81M; 124-minute compilations at 521k–3.4M. 2.5M subs. | **No — and PD shouldn't try.** This is a library-economics play: decades of owned footage re-cut at near-zero marginal cost. PD cannot match supply volume or archive access. **However** — 48 Hours' compilations underperform its singles per-video, and its median AVP is not visible to us. The competitive answer is not to out-produce it. |
| **C-2** | **JCS – Criminal Psychology** (5.6M subs, **17.7M median views** — highest in the lane) | [How To Interrogate a Narcissist, 6,190,358 views, 59m](https://youtu.be/KnyERpdX_0g) | **No.** JCS's moat is (a) primary interrogation footage and (b) a decade of format authority. PD's invariant 11 (no counterfeit authenticity) forbids the imitation route, correctly. |
| **C-3** | **Exclusive-access broadcast moments (7 News Spotlight)** | [Father meets his children's killer — 26,634,027 views, 50m, 22.2× views-per-sub](https://youtu.be/gzc9VAKfCbI) | **No.** The asset is physical access to a maximum-security prison meeting. Unbuyable at PD's scale. **[INFERENCE]** PD's own docs record this at 209–412× channel median; my independent pull confirms the magnitude. |
| **C-4** | **The Civil Rights Lawyer** (2.0M subs, 1.34M median) | Six 2025–26 uploads at 2.9–4.0× on 14–57 min | **Partially — and this is the important one.** His moat is *being the plaintiff's attorney*: he owns discovery, depositions and bodycam nobody else has. PD cannot get that. **But** PD can compete on the cases he cannot take: historical, closed, and out-of-jurisdiction ones, where the archive is public. **[INFERENCE]** His subject selection is constrained by his own docket — that constraint *is* PD's opening. |
| **C-5** | **Paid-distribution outliers** | Trevor Milton, 28.2M views, **9,720 subs** (2,901× views-per-sub) | **Not applicable — this is a spend, not a win.** Flagged so it is not mistaken for a topic signal. |

**Honest summary of the ceiling:** every genuine ceiling case in this lane is locked by an asset PD cannot acquire — an archive, a footage relationship, physical access, or a law license. **None of them is locked by craft or by subject knowledge.** The tier immediately below the ceiling — 20–45 min narrative films at 100k–600k views on 20k–550k-sub channels (The Crime Agents, Institute for Justice) — is **wide open and is where PD's realistic upside lives.**

---

## 5. NOVELTY SANITY-CHECK SUMMARY

| Area | Status | Evidence |
|---|---|---|
| Open fields / game warden | ✅ CLEAN | 0 hits, pipeline + all 56 episodes |
| Sober-DUI / drug recognition | ✅ CLEAN | 0 hits |
| Warrantless rental/code inspection | ✅ CLEAN (⚠ "blight" in EP10 kelo) | 0 hits for inspection terms |
| Occupational licensing | ✅ CLEAN | 0 hits |
| ALPR / plate readers | ✅ CLEAN (adjacent doctrine in EP8/25/26) | 0 hits |
| Field drug test | ✅ CLEAN | 0 hits |
| De-banking | ✅ CLEAN | 0 hits |
| K9 false alert | ✅ CLEAN (adjacent: EP32 carsearch) | hits were false positives |
| Civil commitment | ✅ CLEAN | 0 hits |
| Guardianship / Fierle | 🟡 QUEUED — bench B11 | 5 + 4 hits, v003 |
| Delphi pensions | 🟡 QUEUED — bench B12 | 7 hits |
| Robo-signing | 🟡 QUEUED — bench B8 | 4 hits |
| Malinowski / Hemme / Lejeune / Toforest | 🟡 QUEUED — active slate | 9 / 19 / 21 / 20 hits |
| Shaken baby (Roberson) | 🟡 QUEUED — bench B2, blocked until EP65+ | 1 + 3 hits |
| Bite mark (Duncan) | 🟡 QUEUED — bench B13, owner decision pending | 1 + 3 hits |
| Medical examiner fraud (Zain/Gilchrist) | 🟡 RESERVE, no case promoted | 1 hit each |
| Immigration / citizen detained (Lyttle, Fikre) | 🟡 NAMED, unvetted | 2 hits each |
| **Facial recognition wrongful arrest** | ❌ **SHIPPED — EP36 williams** | topic.json, claims, sources, scene_plan |
| Jailhouse informant | ❌ PARTIALLY SPENT — EP51, EP54 narration | narration_index hits |

---

## 6. WHERE THIS CONTRADICTS OR QUALIFIES PD'S EXISTING RESEARCH

### 6.1 R-38 (resolved-form packaging ban) — **NOT contradicted, but NOT confirmed either**
I attempted a direct test on the 2,982-video within-channel pool. **Only 2 titles matched resolved form** (0.59× and 0.50× — both below channel median, directionally consistent with R-38). **n=2 is far too small to conclude anything.** My regex for the "present-tense/unpunished" counter-class was too noisy to trust (it caught unrelated titles like "Why Hold Music Still Sucks"), so I am reporting **no result** rather than a misleading one. **R-38 should still be treated as resting on PD's original corpus scan, and experiment E3 remains the right way to settle it.**

### 6.2 NEW measured finding — loss-verb framing outperforms
On the same pool, titles containing a **loss verb** (took / seized / stole / destroyed / raided / drained / lost) score **median 1.18× vs 1.00×, delta +0.180, n=47**. This is a *new* lever not in PD's existing title research, and it directly supports the "the government did this to an ordinary person" framing over both the doctrine framing and the exoneration framing.

### 6.3 **Contradiction: immigration/ICE demand does not transfer to documentary format**
PD's unvetted list (`Lyttle`, `Fikre`) sits in the wrongful-detention-of-a-citizen lane, which v003 describes as "mechanism-screened and completely open". My measured data adds an important qualifier: **on the one channel in this lane that has actually tested it, immigration content is the worst-performing category** — IJ scores 0.81×, 0.66×, 0.56×, **0.15×** on immigration items, versus 10–18× on property and policing items, *on the same channel in the same period*. Meanwhile news clips on identical subject matter draw 3–4.4M views. **[INFERENCE]** The demand is real but is political-outrage demand that does not convert to rights-documentary viewing. Given PD's north star of never getting banned, this materially weakens the case for the immigration lane relative to how v003 frames it.

### 6.4 **Qualification: "wrongful conviction is near white-space" is right about supply, but the winning protagonist has changed**
PD's existing finding (126 in-lane long-forms; winners are outrage-clip formats) is corroborated. What my data adds: the channels currently winning this thematic territory have **switched protagonist class** — from *convict later exonerated* to *ordinary person wrongly treated right now*. IJ and The Civil Rights Lawyer generate 3–18× multiples with identical doctrine and a non-convict protagonist. **[INFERENCE]** The gap PD identified may be less a subject gap than a **protagonist-selection** gap.

### 6.5 **Caution against one white-space area: long-form may not convert**
The single cleanest short-vs-long comparison in the dataset (IJ's box story: 3 min = 18.65×/1.04M; 38 min = 0.95×/53k) is a **direct measured warning** that high short-form demand in the government-overreach lane does not automatically survive translation to 30 minutes. This applies to WS-4 most acutely and should temper WS-1 and WS-3 as well.

### 6.6 Could not test
**Thumbnail face-size** (the open disagreement between PD's two internal studies) — I did no computer-vision pass and have **nothing to add**. It remains open.

---

## 7. WHERE PD SHOULD AIM — conclusion

The measured picture is that PD has been competing in the hardest square of its own lane. Every genuine ceiling case — 48 Hours, JCS, 7 News, The Civil Rights Lawyer — is locked by an asset PD cannot buy (an archive, footage relationships, prison access, a law license), but **none is locked by craft, research depth or runtime**, and the tier directly beneath them is being won right now by channels smaller than PD's ambitions by outsiders with 20k–520k subscribers making 28–46 minute films. The strongest repeatable pattern across every one of those winners is not a subject at all — it is a **protagonist swap**: the same Fourth Amendment doctrine that converts at 0.5–0.8% CTR when the protagonist is a convict seeking exoneration converts at 3–18× channel median when the protagonist is a landowner, a driver, a mechanic or a grandmother, the injury is present-tense, and the villain is still holding the badge. PD should therefore aim at **present-tense government-overreach cases against non-criminal protagonists, at 28–40 minutes, with the loss stated as a verb in the title** — and the three areas where measured demand, near-total absence of long-form supply, and a clean novelty record intersect are **open-fields/game-warden surveillance of private land, the false DUI arrest of a provably sober driver, and warrantless municipal inspection of homes**. All three are absent from PD's 56 shipped episodes *and* from every version of the topic pipeline, all three have a Supreme Court spine PD is already expert at rendering, and one of them (open fields) has exactly one long-form treatment in existence — an advocacy piece that did **10.66× its channel's median**. The main risk to carry into selection is §6.5: the one direct short-vs-long comparison available says this lane's short-form demand can collapse at length, so the selection test should be *"does this case have a 30-minute narrative spine?"* rather than *"does this topic get views?"*

---

## 8. Sources

All YouTube figures measured via YouTube Data API v3 on 2026-07-29. Channels:
[Institute for Justice](https://www.youtube.com/@instituteforjustice) · [The Civil Rights Lawyer](https://www.youtube.com/@TheCivilRightsLawyer) · [The Crime Agents](https://www.youtube.com/@TheCrimeAgents) · [LegalEagle](https://www.youtube.com/@LegalEagle) · [Audit the Audit](https://www.youtube.com/@AudittheAudit) · [Dire Trip](https://www.youtube.com/@DireTrip) · [Fascinating Horror](https://www.youtube.com/@FascinatingHorror) · [Plainly Difficult](https://www.youtube.com/@PlainlyDifficult) · [Women Of Crime](https://www.youtube.com/@WomenofCrime) · [48 Hours](https://www.youtube.com/@48hours) · [JCS – Criminal Psychology](https://www.youtube.com/@JCSCriminalPsychology) · [FRONTLINE PBS](https://www.youtube.com/@frontline)

Individual videos are hyperlinked inline in §1 and §3. Internal PD sources built upon (not re-derived): `episodes/_planning/CTR_GROWTH_REFERENCE.v001.md`, `THUMBNAIL_PATTERN_RESEARCH.v001.md`, `DEEP_RESEARCH_FINDINGS.v001.md`, `TOPIC_PIPELINE.v001–v003.md`, `EP41-43_TOPIC_PROPOSALS_v001.md`.
