# ANALYTICS REFRESH — 2026-07-29 (v001)

**Purpose:** evidence brief for the topic-selection agents. This file does not pick topics; it says what the numbers support.
**Author:** analytics pass, 2026-07-29. No commits made by this pass.

## 0. Provenance and what "fresh" actually means

| file | mtime | window it actually covers | usable? |
|---|---|---|---|
| `scripts/_yt_analytics.json` | 2026-07-29 01:34 | daily rows **2026-06-01 .. 2026-07-25** (55 days) | YES |
| `scripts/_yt_retention_curves.json` | 2026-07-29 01:35 | declared 2026-06-01 .. 2026-07-29; **21 of 49** videos returned rows (`ok:official_api`), 28 returned `no_rows` | YES (n=21) |
| `scripts/_yt_studio_ctr_summary.json` | 2026-07-28 00:56 | studio-default 28d, channel level, HTTP 200 | YES |
| `scripts/_yt_studio_video_ctr.json` | 2026-07-28 01:30 | **106 of 106 rows are `HTTP 401`. Zero rows carry impressions.** | **NO — unusable** |
| `scripts/_yt_hook_health.json` | 2026-07-13 | 16 days stale | superseded by §1.6 below |
| `episodes/_planning/measurements/ctr_baseline_20260725.reconstructed.md` | verified 7/25 baseline | 28d ending 2026-07-25 | YES — the only per-video CTR we have |

Two provenance facts that constrain every conclusion below:

1. **The "fresh" analytics pull is 4 days stale.** `yt_analytics_probe.py` defaults `endDate` to `date.today()`, so the query asked for data through 7/29 and YouTube returned rows only through **7/25**. This is the Analytics reporting lag, not a query error. Consequence: **the packaging refresh applied on 7/25 has ~1 day of representation in this data.** Nothing in this file measures the refresh.
2. **The channel is six weeks old.** Per `DISTRIBUTION_STATE.v001.json` (measured 7/27): **6 subscribers, 3,531 lifetime views, 74 public videos.** First long-form published **2026-06-16**. The 55-day window (3,502 views) is therefore ~99% of the channel's entire life. There is no back-catalogue, no seasonality, and no cohort to compare against. Every number below is a first observation.

---

## 1. What changed since the 7/22–7/23 reads

Prior figures are taken from `DEEP_RESEARCH_FINDINGS.v001.md` (dated 7/26, built on the 7/22–7/23 pulls) and memory `pd-deep-research-2026-07`.

### 1.1 Headline recomputation

| metric | prior read | fresh (6/1–7/25) | verdict |
|---|---|---|---|
| channel views | 3,354 | **3,502** | +148 (+4.4%) in the interval |
| watch-minutes | not stated | **4,405** | — |
| AVD / AVP | ~19% AVP cited | **145 s / 24.82%** | AVP measured higher; prior "~19%" was a long-form-only figure |
| subscribers gained / lost | — | **+7 / −0** | lifetime total is still **6** |
| likes / comments / shares | comments 0 external | **70 / 0 / 7** | comments still **0** |
| retention half-life (median) | **42 s** (n=19) | **44 s** (n=21) | HOLDS — unchanged |
| residual @30s / 60s / 120s / 240s / 480s | 62 / 40 / 32 / 22 / 18 % | **62.3 / 43.6 / 30.0 / 25.2 / 18.2 %** | HOLDS — statistically identical |
| decay after 120 s | 1.0–1.4 pt/min in good builds | median **1.62 pt/min** (n=21) | HOLDS |
| Shorts share of views | 65.3% | **71.5%** (2,501 / 3,496) | Shorts dependence INCREASED |
| Suggested (RELATED_VIDEO) share of watch-minutes | 44.5% | **38.1%** (1,678 / 4,399) | WEAKENED |
| PLAYLIST min/view | 19.6 | **22.24** (34 views → 756 min) | HOLDS and strengthened |
| GB / AU / NL / CA AVP | 60.0 / 67.4 / 63.2 / 57.5 | **60.02 / 67.43 / 63.23 / 57.51** | IDENTICAL — see §4 |
| audience 93.4% male / 90.9% 55+ | signed-in sample | **not re-pulled** | UNTESTED — see §1.7 |

### 1.2 Prior conclusion: "wrongful-conviction/exoneration is the highest-retention cluster" → **CONTRADICTED, but the replacement is also unsupportable**

Fresh long-form medians by archetype (full table in §2):

- wrongful_conviction (n=3): median AVP **22.23%**, median half-life **35 s**, impression-weighted CTR **1.13%** on 5,030 impressions.
- It ranks **3rd of 7 on AVP, 5th of 7 on half-life, 5th of 7 on watch-minutes per video, and last-but-one on CTR.**
- The clusters above it on retention are disaster (n=**1**) and heist_mystery (n=**2**).

So the specific claim is not supported by current numbers. But the honest statement is stronger than a reversal: **with 3 videos and 82 total views, the wrongful-conviction bucket cannot be ranked at all**, and neither can the buckets that displaced it. See §2.4.

### 1.3 Prior conclusion: "doctrine explainers collapse" → **CONTRADICTED as stated; the real failure is upstream of retention**

Splitting the 8 served police-power long-forms into case-law-led explainers (Terry, Katz, Riley, Carpenter, Rodriguez, car-search; n=6) vs narrative police cases (Lange, Florence; n=2):

| sub-group | n | median AVP | median half-life | median CTR | watch-min/video |
|---|---|---|---|---|---|
| doctrine explainer | 6 | **22.73%** | **44 s** | **2.29%** | 91.8 |
| narrative police case | 2 | 19.91% | 29.5 s | 2.60% | 68.0 |

Doctrine explainers are **the highest impression-weighted CTR archetype on the channel: 2.45% across 10,040 impressions (n=8)** — the largest impression base of any bucket, and ~2.2× the wrongful-conviction bucket's 1.13%. They do not collapse on retention either (median AVP 22.7% vs channel long-form median 20.8%).

What *does* collapse is a different population: **the abstract rights-explainer back-catalogue that never gets served at all** (§1.5). Terry-style doctrine with a named person and a physical scene performs; "Read Rights or It's Out | Miranda v. Arizona" (lifetime **2 views**) does not. The prior conclusion conflated the two.

### 1.4 Prior conclusion: "subs come only from long-form" → **WEAKENED to the point of being unmeasurable**

| | subs | views | subs/1k | 95% CI on the count (Poisson) |
|---|---|---|---|---|
| long-form | 4 | 847 | **4.72** | [1.1, 10.2] |
| Shorts | **2** | 2,467 | 0.81 | [0.2, 7.2] |
| channel | 7 | 3,502 | 2.00 | [2.8, 14.4] |

Shorts produced **2 of 7** subscribers (both from `Ri1hlCBOjhc`, 801 views) — so "only from long-form" is factually false. The per-view rate still favours long-form 5.8×, but with 4 and 2 events the confidence intervals overlap almost completely. **7 subscriber events cannot support any ranking.** One of the 7 is unattributed in the per-video table (4 + 2 = 6).

### 1.5 NEW, and the largest structural finding: 43% of the published long-form catalogue is never served

`DISTRIBUTION_STATE.v001.json` + per-video analytics:

- 49 long-forms exist; **42 are public**, 7 are private/scheduled (publishing 7/28 – 8/03).
- **18 of the 42 public long-forms (43%) took ZERO views in the 55-day window.** Their *lifetime* view counts are 0–12 each.
- 14 of those 18 appear in the 7/25 CTR baseline: **2,082 impressions at 0.77% weighted CTR**, versus **1.90% weighted CTR** across the 24 served long-forms. Six of them sit at exactly **0.00% CTR** (56–481 impressions each).
- Impression supply is concentrated: the **top 6 long-forms hold 17,117 of 31,746 long-form impressions (53.9%)**.
- Watch-minutes are even more concentrated: **Titan alone = 1,648 of 3,678 long-form watch-minutes (44.8%)**; Titan + D.B. Cooper = **56.0%**.

Cadence context: 42 public long-forms were published between 6/16 and 7/27 — roughly **one long-form per day**. Nearly half were never served. The binding constraint on this channel is not retention craft; it is that **YouTube is not distributing most of what we publish.**

Caveat: 5 of the 18 published on 7/23–7/27 and are partly explained by recency. The other 13, published 6/16 – 7/19, are not.

### 1.6 NEW: the opening deficit is unanimous, not a majority

Prior: "12/19 videos below peer median by 6–7 s". Recomputed length-matched (median `rel_perf` over the first 5% of runtime, so long and short films are comparable):

- **21 of 21 videos are below peer median. Median rel_perf = 0.191.** Best on the channel is `5Jap-0h43A4` at 0.448; worst is `FTm1icKgycU` at 0.044.
- Not one video on the channel has ever opened at or above its peer median.

This is the single most sample-robust result in the dataset (unanimous, n=21) and it supersedes the stale `_yt_hook_health.json` (7/13). It is a build finding, not a topic finding — but it caps what any topic choice can deliver, so topic agents should treat "can this premise be opened with an in-progress scene in the first 10 seconds?" as a selection filter.

### 1.7 NEW: "suggested is the traffic engine" → WEAKENED; owned surfaces are now roughly tied with it

| source | views | % views | watch-min | % watch-min | min/view |
|---|---|---|---|---|---|
| SHORTS | 2,501 | 71.5% | 615 | 14.0% | 0.25 |
| RELATED_VIDEO (suggested) | 416 | 11.9% | **1,678** | **38.1%** | 4.03 |
| SUBSCRIBER | 263 | 7.5% | 805 | 18.3% | 3.06 |
| YT_SEARCH | 185 | 5.3% | 376 | 8.5% | 2.03 |
| **PLAYLIST** | **34** | **1.0%** | **756** | **17.2%** | **22.24** |
| everything else | 97 | 2.8% | 169 | 3.8% | — |

Suggested is still the largest single source of watch-time (38.1%) but **owned surfaces — PLAYLIST + SUBSCRIBER + YT_CHANNEL + NOTIFICATION — now deliver 1,566 minutes, 35.6% of channel watch-time, from 8.8% of views.** The prior read reported suggested at 44.5% and did not enumerate SUBSCRIBER, so I cannot cleanly attribute how much of this is growth versus a reporting-scope difference; treat the direction as established and the magnitude of the change as unverified.

**PLAYLIST is the standout number on the channel: 7 videos in 2 playlists generate 17.2% of all watch-minutes at 22.24 min/view — 5.5× the min/view of suggested and 89× that of the Shorts feed.** Per the 7/27 distribution state the session machine is still almost entirely unbuilt: 2 playlists, 7 of 42 long-forms in a playlist, **0 long-forms linking another video**, 4 linking a playlist, and only 7 of 42 with valid chapters.

### 1.8 Demographics were NOT re-pulled

The fresh `_yt_analytics.json` contains `channel_total`, `per_video`, `traffic`, `device`, `country`, `daily`, `sharing`. **There is no age or gender dimension in this pull.** The "93.4% male / 90.9% 55+" conclusion is therefore **untested by this refresh** — neither confirmed nor weakened. It still rests on the earlier signed-in sample on a channel that has taken 3,531 lifetime views. Device mix did come through and is consistent with an older/TV-inclusive audience: MOBILE 69.6%, DESKTOP 14.0%, TABLET 9.8%, **TV 6.6%** (n=3,501).

---

## 2. Topic-level evidence

### 2.1 Archetype table (long-form only; 24 served videos)

CTR is impression-weighted from the verified 7/25 baseline. Half-life is from the 21 real curves. AVP/AVD/subs are from the fresh 6/1–7/25 analytics.

| archetype | n | views | watch-min | **watch-min / video** | med AVP | med AVD | med half-life | wtd CTR | impressions | subs | subs/1k |
|---|---|---|---|---|---|---|---|---|---|---|---|
| disaster | **1** | 157 | 1,648 | **1,648.0** | 28.98% | 630 s | 129 s | 2.42% | 4,292 | 1 | 6.37 |
| heist_mystery | **2** | 62 | 477 | **238.5** | 24.54% | 421 s | 93.5 s | 1.33% | 1,962 | 0 | 0.00 |
| police_power | 8 | 324 | 687 | **85.9** | 21.35% | 126 s | 42 s | **2.45%** | **10,040** | 0 | 0.00 |
| financial_fraud | 6 | 127 | 450 | **75.0** | 18.43% | 240 s | 52 s | 1.86% | 3,930 | 1 | 7.87 |
| wrongful_conviction | 3 | 82 | 218 | **72.7** | 22.23% | 158 s | 35 s | 1.13% | 5,030 | 1 | 12.20 |
| property_seizure | 3 | 72 | 172 | **57.3** | 16.82% | 121 s | 30 s | 1.60% | 2,942 | 1 | 13.89 |
| prosecution_overreach | **1** | 23 | 26 | **26.0** | 3.97% | 69 s | 34 s | 0.82% | 1,468 | 0 | 0.00 |

Bucketing note: the six archetypes named in the brief did not partition the catalogue cleanly. `rights-explainer` on this channel *is* `police_power` (Terry/Katz/Riley/Carpenter/Rodriguez are doctrine explainers) — I kept it as one bucket and split it in §1.3. I added `property_seizure` (the EP33–35 civil-forfeiture arc: Tyler, Hinders, Timbs) because folding it into rights-explainer would have destroyed the signal, and `prosecution_overreach` (Aaron Swartz, n=1) because it fits nowhere.

### 2.2 Publish-date normalised view (removes the "older videos had more days" bias)

| archetype | n | median watch-min **per day live** | median days live |
|---|---|---|---|
| disaster | 1 | **65.92** | 25 |
| heist_mystery | 2 | **11.85** | 20 |
| property_seizure | 3 | **8.67** | 8 |
| wrongful_conviction | 3 | **5.45** | 11 |
| financial_fraud | 6 | 3.08 | 22 |
| police_power | 8 | 3.01 | 21 |
| prosecution_overreach | 1 | 1.44 | 18 |

**The two normalisations disagree.** Raw watch-min/video ranks police_power 3rd and property_seizure 6th; per-day-live ranks property_seizure 3rd and police_power 6th. The reason is that property_seizure videos are the newest (median 8 days live) and new videos get an initial serving burst. Neither metric is clean: raw favours old videos, per-day favours new ones. **With 1–8 videos per bucket, publish-date confounding is larger than the archetype effect.**

### 2.3 Ranked by what actually earns watch-time (the requested ranking, with confidence)

1. **disaster / engineering-failure** — 1,648 watch-min/video, AVP 28.98%, half-life 129 s, CTR 2.42%. **n=1. Confidence: none statistically; weight: enormous** — this single video is 44.8% of all long-form watch-minutes.
2. **heist_mystery (famous unsolved)** — 238.5 watch-min/video, AVP 24.54%, half-life 93.5 s. **n=2.** Best retention of any multi-video bucket. Weak but the most consistent non-singleton signal.
3. **police_power / rights doctrine** — 85.9 watch-min/video, AVP 21.35%, half-life 42 s, **CTR 2.45% on 10,040 impressions**. **n=8 — the only bucket with a usable sample.** Best entry rate on the channel by a wide margin; mid-pack retention.
4. **financial_fraud** — 75.0 watch-min/video, AVP 18.43%, half-life 52 s, CTR 1.86%. **n=6.** Second-largest sample. Consistently mid.
5. **wrongful_conviction** — 72.7 watch-min/video, AVP 22.23%, half-life 35 s, CTR 1.13% on 5,030 impressions. **n=3.** Retention is fine; **entry is the problem** — it has the second-largest impression base and nearly the worst click rate.
6. **property_seizure** — 57.3 watch-min/video, AVP 16.82%, half-life 30 s, CTR 1.60%. **n=3.** Worst AVP and half-life of any multi-video bucket. Ranks 3rd on the per-day-live metric purely because it is newest.
7. **prosecution_overreach** — 26.0 watch-min/video, AVP 3.97%, half-life 34 s, CTR 0.82%. **n=1.** The worst long-form on the channel.

### 2.4 Where the data cannot support a conclusion — stated plainly

- **Subscriber ranking by archetype is noise.** Every non-zero bucket has exactly **1** subscriber event. The subs/1k column in §2.1 is arithmetic on single events and must not be used to rank anything.
- **Buckets with n=1 or n=2 (disaster, heist_mystery, prosecution_overreach) are anecdotes.** Titan's 1,648 minutes is the biggest fact on the channel and also a sample of one.
- **22 of 24 served long-forms have fewer than 100 views; 15 of 24 have fewer than 30.** Median long-form views in the window is **21**. AVP computed on 7–20 views (j8U8c4BB_GQ: 7 views; XWYWAgkExH4: 8; gR_nzXIyIlk: 8) is not a stable estimate of anything.
- **Entry CTR barely predicts outcome here:** Spearman ρ(CTR, watch-minutes) = **0.266**, Pearson r = **0.131** (n=24). Videos at ≥2.0% CTR earn a median 74 watch-minutes vs 60 for those below — a real but small gap. Impression *supply*, not click rate, is what separates winners from the dead catalogue.
- **A data-integrity discrepancy:** per-video impressions in the 7/25 baseline sum to ~31,746 for long-forms alone, which exceeds the channel-level figure of 27,015 for the same date. The two metrics are not the same aggregation. I therefore used only *within-long-form* impression shares and avoided any "% of channel impressions" claim.

---

## 3. Runtime evidence — does "longer wins" survive on OUR channel?

### 3.1 By band (long-form, 24 served videos)

| band | n | views | watch-min | **watch-min/video** | min/view | med AVP | med half-life | med CTR | subs |
|---|---|---|---|---|---|---|---|---|---|
| 09–13 min | 13 | 482 | 1,083 | **83.3** | 2.25 | **21.13%** | 36 s | 1.85% | 2 |
| 16–24 min | 4 | 89 | 246 | **61.5** | 2.76 | **14.54%** | 53 s | 2.41% | 1 |
| 24–36 min | 6 | 119 | 701 | **116.8** | 5.89 | 20.98% | 80 s | 1.19% | 0 |
| 36 min+ | **1** | 157 | 1,648 | **1,648.0** | 10.50 | 28.98% | 129 s | 2.42% | 1 |

(There are no long-forms in the 13–16 min band.)

### 3.2 The same bands with each band's single biggest video removed

| band | n | watch-min/video | top video removed | that video's share of its band |
|---|---|---|---|---|
| 09–13 min | 12 | **67.7** | Terry (271 min) | 25% |
| 16–24 min | 3 | **54.7** | Tyler (82 min) | 33% |
| 24–36 min | 5 | **58.0** | D.B. Cooper (411 min) | **59%** |
| 36 min+ | 0 | — | Titan (1,648 min) | **100%** |

### 3.3 Verdict: **"longer wins" does NOT survive on our channel.**

- **Minutes per view rises monotonically with length** — 2.25 → 2.76 → 5.89 → 10.50, a 4.7× spread. That part is real and is just arithmetic: a longer film at similar AVP yields more minutes per viewer.
- **Minutes per episode slot does not.** Once each band's single outlier is removed, the 24–36 min band earns **58.0** watch-minutes per video versus **67.7** for the 9–13 min band. Longer films acquire proportionally fewer views, and the two effects cancel.
- **The entire "long wins" case on this channel is two videos.** Titan (36 min+, 44.8% of all long-form watch-minutes) and Cooper (24–36 min, 11.2%) are 56.0% of the total. Both won on **premise** — a news-attached engineering disaster and the most famous unsolved hijacking in America — not on runtime. The other four videos in the 24–36 min band (Milken, Rajaratnam, Varsity Blues, Swartz) averaged **58.0** minutes each on 7–23 views apiece.
- **The 16–24 min band is the worst band on the channel: median AVP 14.54%** versus 21.13% at 9–13 min. This is the band the current civil-forfeiture arc occupies (OneCoin 15.9%, Flash Crash 13.1%, Hinders **6.67%**, Tyler 37.2%).
- The prior corrected rule — "length is earned by narrative density, keep doctrine explainers at 11–12 min" — **survives in direction but the bar should be raised from a density judgement to a premise test**: the only two long films that paid off had independently famous or news-attached subjects. Density was not what distinguished them from Milken and Rajaratnam.

**Practical default: 10–13 min. Go to 24–36 min only for premises that carry their own external demand (§6, P1/P2). Avoid 16–24 min entirely — it has the worst AVP and no compensating min/view advantage (2.76 vs 2.25).**

Sample-size honesty: bands hold 1, 4, 6 and 13 videos on 11–157 views each. This is a directional read, not a fitted curve.

---

## 4. Geography and audience

### 4.1 The GB/AU-vs-US gap, recomputed

| country | views | % of geo-known | AVP |
|---|---|---|---|
| US | 1,243 | 86.5% | **24.48%** |
| GB | 110 | 7.7% | **60.02%** |
| CA | 39 | 2.7% | 57.51% |
| NL | 23 | 1.6% | 63.23% |
| AU | 22 | 1.5% | 67.43% |

Non-US (GB+CA+NL+AU) combined: **194 views at a view-weighted 60.74% AVP = 2.48× the US figure.** The prior read gave 2.4–2.8×. **The ratio holds exactly.**

### 4.2 But no new evidence has accumulated, and the metric is confounded

Two things must be said before this number is used to justify anything:

1. **The non-US sample did not grow between reads.** GB 60.0→60.02, AU 67.4→67.43, NL 63.2→63.23, CA 57.5→57.51 — these are the same underlying values at different rounding. US moved (86%→86.5% of geo-known, 24.2%→24.48% AVP), so the pull did refresh; **the non-US countries simply took ~0 additional views.** The geography evidence is exactly as strong as it was a week ago and no stronger.
2. **Country AVP is not format-controlled, and the confound is large enough to explain the entire gap.** Only **1,437 of 3,502 views (41.0%) carry a country**; 2,065 views (59.0%) have no geo attribution. Meanwhile **Shorts have a median AVP of 52.1% (n=25) and long-forms 20.8% (n=24)** — a 2.5× gap that happens to be the same size as the US/GB gap. The geo-known set contains at least 590 Shorts views. If GB's 110 views skew toward Shorts and the US's 1,243 skew toward long-form, the "GB retains 2.5× better" finding is a **format-mix artifact with no audience meaning at all.** The current pull cannot separate these; it needs a country × `creatorContentType` (or country × video) query.

### 4.3 Read for the EP56 UK pilot

**There is no read yet, and there will not be one from this data.** EP56 (Post Office/Horizon) does not appear in the catalogue, the analytics, or the retention curves — it is unpublished. The evidence that motivated the pilot is **110 GB views**, unchanged since the last read, on a metric that is **not format-controlled**. That is enough to justify the single-episode bet already agreed (one slot, low cost) and nothing more. Before treating it as a lane:

- run the country × format query to kill or confirm the confound (cheap, one API call);
- hold the pre-registered gate from the prior plan: **GB views ≥300 with AVP ≥45% on the pilot itself.**

Confidence on the underlying gap: **low.** 110 / 39 / 23 / 22 views per country, no growth, and a plausible confound of exactly the observed magnitude.

---

## 5. The 8/8 CTR question

### 5.1 The per-video pull is dead and says nothing

`scripts/_yt_studio_video_ctr.json` (7/28 01:30) contains **106 rows, 106 of them `HTTP 401`, 0 rows carrying impressions.** This is the cookie rotation documented in `ctr_baseline_20260725.reconstructed.md`. The file is not a degraded measurement — it is an empty one. **Any per-video CTR claim must come from the 7/25 reconstructed baseline**, which is what §2 uses.

The mechanism fixes named in that incident record are **still outstanding** and are a hard blocker on the 8/8 read: the script must (a) refuse to overwrite when every row lacks impressions, (b) write to a dated filename with a `latest` pointer, and (c) the runbook must snapshot+commit before any new pull. Without (a) the 8/8 pull can destroy the 7/25 baseline the same way.

### 5.2 Channel-level CTR is valid and currently flat

| date | impressions | CTR | Shorts feed VTR | avg watch from impressions |
|---|---|---|---|---|
| 2026-07-25 | 27,015 | **1.58%** | 32.90% | 269 s |
| 2026-07-28 | 30,265 | **1.57%** | 34.35% | 284 s |

+3,250 impressions in 3 days with CTR flat at 1.57–1.58%. **This is the expected null**, not a failed refresh — see the window arithmetic.

### 5.3 How much of the window is post-refresh

The packaging refresh (19 thumbnails + 17 titles) went live **2026-07-25**.

| pull date | 28-day window | post-refresh days | share of window |
|---|---|---|---|
| 2026-07-28 (the pull we have) | 07-01 .. 07-28 | 4 | **14.3%** |
| 2026-07-29 (today) | 07-02 .. 07-29 | 5 | **17.9%** |
| **2026-08-08 (scheduled read)** | 07-12 .. 08-08 | **15** | **53.6%** |
| 2026-08-22 | 07-26 .. 08-22 | 28 | **100%** |

**Answer: ~18% of the current 28-day window is post-refresh. The current per-video CTR says nothing — first because 82% of the window predates the change, and second because the file is empty.** 8/8 is the first pull where a majority (53.6%) of the window is post-refresh, so it supports a **directional** read only. **8/22 is the first fully-post-refresh window and is the clean read.**

### 5.4 A confound that will land inside the 8/8 window

Seven long-forms are scheduled to publish **7/28 – 8/03** (`yRwxBfrOY5o`, `GGW1SIAAgkY`, `AxOlQ2NIaBU`, `bSnyfsulna8`, `2pLWw_vhfI8`, `hC5KE6IqmhM`, `i95peRcdtz4`). New uploads draw a disproportionate share of fresh impressions, and they carry new packaging by default. The 8/8 channel-level CTR will therefore mix **"did the refresh lift the 19 old thumbnails"** with **"how did 7 brand-new episodes package."** Separating them **requires the per-video pull to work**, which makes the cookie/overwrite fix a prerequisite for the 8/8 measurement rather than a nice-to-have. The pre-registered comparison — each refreshed video's CTR versus its 7/25 row, weighted by impressions, with terry/riley/timbs as untouched controls — is still the right test.

---

## 6. What to make next — prioritized brief for the topic agents

Every statement carries its number and its sample size. Statements are ordered by evidential weight, not by effect size.

### Prefer

**P1. Prefer premises that already carry external demand — a news-attached disaster, a famous unsolved case, an event people are searching for.**
Titan produced **1,648 of 3,678 long-form watch-minutes (44.8%)** from 157 views; D.B. Cooper added **411 (11.2%)**. **Two videos are 56% of everything the channel has earned.** *(n=2; no statistical confidence, maximum practical weight — this is the only thing that has ever worked at scale here.)*

**P2. Prefer police-power / rights-doctrine cases built around a named person and a physical scene, as the reliable core of the slate.**
Highest impression-weighted CTR on the channel: **2.45% across 10,040 impressions, n=8** — the only bucket with a usable sample, and ~2.2× wrongful conviction's 1.13% on 5,030 impressions. Median AVP 21.35%, above the long-form median of 20.8%. *(n=8 — the strongest topic-level evidence available.)*

**P3. Prefer 10–13 minutes as the default runtime.**
9–13 min earns **83.3 watch-minutes per video (67.7 excluding Terry)** versus **116.8 (58.0 excluding Cooper)** at 24–36 min, and has the best median AVP of any multi-video band at **21.13%**. *(n=13 vs n=6.)*

**P4. Prefer 24–36 min only when the premise passes P1.**
The 24–36 min band's result is **59% one video**. The other five averaged 58.0 watch-minutes on 7–23 views each. Length did not distinguish Cooper from Milken; fame did. *(n=6.)*

**P5. Prefer topics that extend an existing playlist rail over topics that stand alone.**
**7 videos in 2 playlists generated 756 watch-minutes — 17.2% of all channel watch-time — at 22.24 min/view**, 5.5× suggested (4.03) and 89× the Shorts feed (0.25). 0 of 42 long-forms link another video; 7 of 42 sit in a playlist. *(n=34 playlist views — small, but the min/view gap is an order of magnitude and has held across two reads.)*

**P6. Prefer premises whose first 10 seconds can be an in-progress scene; reject premises that need setup.**
**21 of 21 measured videos open below peer median (median rel_perf 0.191 over the first 5% of runtime).** The channel has never cleared this bar on any topic. Median half-life is **44 s** and the median residual at 2:00 is **30.0%**. *(n=21, unanimous — the most robust finding in the dataset.)*

**P7. Prefer topics with a stakes gap that survives being stated as a thumbnail question.**
Among served long-forms, entry CTR ranges 0.71%–4.48% on the same production pipeline. The top four (Lange 4.48%, car-search 3.85%, Flash Crash 3.32%, OneCoin 3.27%) are all trivial-cause → catastrophic-outcome framings. *(n=24; note Spearman ρ(CTR, watch-min) is only 0.266, so treat CTR as an entry gate, not an outcome predictor.)*

**P8. Do not select topics on subscriber conversion.**
Total subscribers gained in 55 days = **7** (95% CI on the count [2.8, 14.4]); lifetime channel subscribers = **6**. Every archetype's subs/1k rests on **one** event. *(Unmeasurable — this is a "do not use" instruction, not a preference.)*

### Anti-patterns

**A1. Do not commission abstract rights-explainers with no named victim and no scene** ("Read Rights or It's Out | Miranda v. Arizona", "Your Home for a Developer? The Kelo Supreme Court Case", "Can Your School Punish You for a Post You Made Off Campus?").
**18 of 42 public long-forms (43%) took zero views in 55 days; their lifetime totals are 0–12 views each.** The 14 with impression data drew **2,082 impressions at 0.77% weighted CTR**, versus **1.90%** for the 24 served videos, with **six at exactly 0.00%**. This is the largest measured failure on the channel. *(n=18.)*

**A2. Do not build in the 16–24 minute band.**
Median AVP **14.54% (n=4)** — the worst of any band — against 21.13% at 9–13 min, with only a trivial min/view gain (2.76 vs 2.25). The two worst AVP results on the whole channel sit here: Hinders **6.67%** and Flash Crash 13.1%. *(n=4 — thin, but it is the worst band on both the AVP and the watch-min/video metric.)*

**A3. Do not commission tech-policy or prosecutorial-overreach abstractions without a physical victim narrative.**
Aaron Swartz: **AVP 3.97%, half-life 34 s, CTR 0.82% on 1,468 impressions, 26 watch-minutes from 23 views** — the worst long-form on the channel on every metric simultaneously, and the worst opening measured (rel_perf 0.044). *(n=1 — but it is the floor of the entire catalogue, and its impression base was large enough that the failure is a click/hold failure, not a supply failure.)*

### The constraint topic selection cannot fix

Topic choice is being asked to solve a problem it does not control. **42 public long-forms were published in 42 days and 43% of them were never served.** Impression supply is concentrated in 6 videos (53.9% of long-form impressions), watch-time in 2 (56.0%). Until distribution improves — playlists (P5), interlinks (0 of 42 today), chapters (7 of 42 valid), and the opening deficit (P6) — a better topic slate will mostly produce better videos that nobody is shown. The cheapest measured lever on the board remains **PLAYLIST at 22.24 min/view**, currently applied to 7 of 42 long-forms.

---

## Appendix: served long-forms, full detail (6/1–7/25)

| id | archetype | len | pub | views | watch-min | AVP | AVD | half-life | r@30s | r@120s | CTR (7/25) | subs |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| marQjsCagh0 | disaster | 2174 s | 07-01 | 157 | 1,648 | 28.98% | 630 s | 129 s | 86% | 52% | 2.42% | 1 |
| tt7U1XgjCU4 | heist_mystery | 1782 s | 07-06 | 51 | 411 | 27.16% | 483 s | 80 s | 85% | 47% | 1.39% | 0 |
| bYcqabvvxak | police_power | 682 s | 06-21 | 159 | 271 | 15.03% | 102 s | 36 s | 57% | 22% | 3.14% | 0 |
| bXATF9ZnKLE | police_power | 697 s | 07-17 | 43 | 149 | 29.99% | 209 s | 45 s | 57% | 37% | 3.85% | 0 |
| Qyad4FejCIc | wrongful_conviction | 698 s | 07-14 | 51 | 148 | 25.08% | 175 s | 47 s | 64% | 30% | 1.35% | 1 |
| sphERPA4gAc | financial_fraud | 721 s | 06-20 | 57 | 140 | 20.54% | 148 s | 30 s | 50% | 28% | 1.85% | 1 |
| mj9qEKPRatE | financial_fraud | 1659 s | 07-07 | 17 | 94 | 20.06% | 332 s | 87 s | 71% | 41% | 1.21% | 0 |
| rU2vk9XL4vY | property_seizure | 1107 s | 07-18 | 12 | 82 | 37.22% | 412 s | 133 s | 92% | 58% | 1.54% | 0 |
| vikfOBHullI | financial_fraud | 1210 s | 07-02 | 25 | 80 | 15.94% | 192 s | 33 s | 56% | 24% | 3.27% | 0 |
| Sz8zPUoBANM | police_power | 554 s | 06-29 | 43 | 74 | 18.70% | 103 s | 42 s | 62% | 24% | 4.48% | 0 |
| 1h267U6PY0I | heist_mystery | 1644 s | 07-05 | 11 | 66 | 21.91% | 360 s | 107 s | 70% | 45% | 1.18% | 0 |
| SOu4Y1NkGGY | police_power | 552 s | 07-22 | 32 | 62 | 21.13% | 116 s | 17 s | 32% | 31% | 0.71% | 0 |
| 5L_HCGJxX_U | wrongful_conviction | 711 s | 07-15 | 23 | 60 | 22.23% | 158 s | 23 s | 39% | 39% | 0.74% | 0 |
| j8U8c4BB_GQ | financial_fraud | 1661 s | 07-04 | 7 | 56 | 28.96% | 480 s | — | — | — | 1.17% | 0 |
| Xc_PxdC_75c | property_seizure | 1156 s | 07-20 | 41 | 52 | 6.67% | 77 s | 30 s | 49% | 15% | 1.24% | 1 |
| zE3nCUlUmLY | police_power | 679 s | 06-23 | 18 | 48 | 23.88% | 162 s | 20 s | 44% | 28% | 2.24% | 0 |
| rYV4rxtQCV0 | financial_fraud | 1717 s | 07-09 | 10 | 48 | 16.81% | 288 s | 52 s | 73% | 30% | 1.36% | 0 |
| tpAKfHKuwqY | police_power | 648 s | 07-12 | 11 | 46 | 38.98% | 252 s | 55 s | 74% | 45% | 2.35% | 0 |
| m-uWzgWHGPg | property_seizure | 720 s | 06-24 | 19 | 38 | 16.82% | 121 s | 27 s | 46% | 26% | 2.69% | 0 |
| 5Jap-0h43A4 | financial_fraud | 1336 s | 07-03 | 11 | 32 | 13.14% | 175 s | 73 s | 93% | 45% | 3.32% | 0 |
| FTm1icKgycU | prosecution_overreach | 1743 s | 07-08 | 23 | 26 | 3.97% | 69 s | 34 s | 56% | 5% | 0.82% | 0 |
| 68oWZRiOnB8 | police_power | 632 s | 07-11 | 10 | 22 | 21.58% | 136 s | 44 s | 80% | 30% | 1.74% | 0 |
| XWYWAgkExH4 | police_power | 647 s | 06-22 | 8 | 15 | 17.91% | 115 s | — | — | — | 1.02% | 0 |
| gR_nzXIyIlk | wrongful_conviction | 714 s | 07-21 | 8 | 10 | 10.78% | 76 s | — | — | — | 1.28% | 0 |

### Public long-forms with ZERO views in the window (18 of 42)

`ch2hQ5jhDmQ` (06-16, lifetime 5) · `An0to4U0hJQ` (06-17, 2) · `waA4XJ9bYcE` (06-19, 5) · `cQFql7tT1fE` (06-23, 2) · `89SQoRgAD7U` (06-25, 2) · `cSfe3iGnBBM` (06-26, 2) · `1pox44KsaV8` (06-27, 5) · `g5yFmDt48oU` (06-28, 1) · `LXFjJqE6vKU` (06-30, **0**) · `rrftLmSVivk` (07-10, 1) · `YhEJHK279f8` (07-13, 5) · `YQIhk2dKZHU` (07-16, 5) · `6ozsIfwqrP0` (07-19, 7) · `Pmh6h5SfWw4` (07-23, 6) · `X40EbUw5kzQ` (07-24, 2) · `4uuY6G0LmHo` (07-25, 2) · `tYZuE76Hwdc` (07-26, 12) · `Enok7A7wGBA` (07-27, 5)

The last five published 07-23 or later and are partly explained by recency. The other thirteen are not.
