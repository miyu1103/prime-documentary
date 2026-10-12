# CTR & GROWTH REFERENCE v001 — Prime Documentary
**Durable research reference. Consult this before any thumbnail / title / short / growth decision.** Built 2026-07-23 from a 62,527-video corpus + ~69 hand-viewed in-lane thumbnails + 205→38,500-title statistical analysis. Honest, outlier-focused, NOT average best-practice. Living doc — the B/C corpus keeps growing; extend it. Companions: [[pd-monetization-strategy]], `CTR_PLAYBOOK.v001.md` (thumbnail/title templates), `SHORTS_METHOD.v001.md`, `TOPIC_PIPELINE.v001.md` (ranked topic feeder, Phase 3), [[feedback-top-1-percent-not-average]], [[feedback-ctr-evidence-first]]. **Phase 3 (2026-07-24) added below: LENGTH/FORMAT evidence (Part E), theme-outlier mining (Part F), topic pipeline (Part G). Phase 4 (2026-07-25) added: PACKAGING PATTERN LIBRARY at scale with within-channel-controlled lift — the dramatic-irony/time-jump/dark-adjective levers vs the when-clause/2nd-person/quote/colon CARGO-CULT (Part I), series/franchise mechanics (Part J), browse-hook mechanic + honest transcript block (Part K).**

> Channel state that frames everything: CTR ≈ **1%** (target ≥7%), retention FINE (avgViewPercentage ~21%). The bottleneck is packaging (thumbnail+title), not content. Goal (North Star): 2M subs / **1M avg views** — the 1M-avg is the harder half and likely needs format evolution toward faces/emotion/shock + a Shorts engine.

---

## 0. METHODOLOGY (so you can trust or challenge it)
- **Corpus:** 62,527 videos across 683 channels (legal/true-crime/police/rights + adjacent storytelling/documentary/education/news — winners, subs median ~279k, 259 channels ≥1M). Harvested via YouTube Data API (search discovery → full-catalog harvest). Files: `scratchpad/ctr_study/corpus.json` + `corpus2.json`.
- **Outperformance metric:** WITHIN-CHANNEL percentile of **views-per-DAY** (age-controlled) — measures what makes a video beat ITS OWN channel (a packaging proxy that controls for channel size + video age). 38,500 analyzable long-forms (channels ≥8 videos).
- **Thumbnails:** ~69 hand-viewed (visual coding) + 3,422 auto-analyzed via OpenCV (haarcascade face detection + brightness/contrast/saturation/warmth) on within-channel hits vs flops.
- **Honesty:** CTR is NOT directly measurable via the public API (impressions/CTR need a Studio-cookie refresh + `yt_studio_ctr.py`). views/day is a proxy. haarcascade misses stylized/non-frontal faces. Treat magnitudes as directional.

---

## 1. TITLE FINDINGS (honest — most "rules" are cargo-cult)
Age-controlled within-channel analysis of 38,500 long-form titles:
- **Surface features barely predict outperformance.** Lifts (within-channel percentile delta, present vs absent): shock_verb **+0.024** (the ONLY real one), colon +0.009, allcaps +0.006, number +0.003, 2nd-person **−0.012**, question **−0.013**, exclaim −0.004. → **Do NOT cargo-cult "add a colon / a number / ALLCAPS / a question."** They don't move within-channel performance.
- **The one real lever = SHOCK/DRAMA VERBS** (realize / discover / caught / killer / still alive / jailed / exposed). This is the engine of the true-crime title grammar.
- **Word-count sweet spot ≈ 8–9 words** (weak signal, ~+0.03 vs extremes); front-load the hook (mobile truncates ~40–50 chars).
- **Conclusion:** titles win on TOPIC + SPECIFIC CURIOSITY + a shock verb, not mechanical features. The two winning grammars (from the hand-viewed winners): **(a) 2nd-person imperative** for rights/explainer ("If The Police Pull You Over, Here Is What To Do" — Law By Mike 93M), **(b) 3rd-person "[Subject] + [shock verb] + [disturbing object]"** for case films ("Cops Discover Bodies in Woman's Trunk" 41M). Our literary titles ("Thirty Years in the Dark") have NO shock verb / curiosity gap = a CTR liability. See CTR_PLAYBOOK §3 for per-episode rewrites.

## 2. THUMBNAIL FINDINGS (faces are real but not magic)
Auto-analysis, 3,422 thumbnails, within-channel hits vs flops:
- **HAS-FACE: hits 56% vs flops 52% (+4pt); face-COUNT +0.093 (the single biggest visual signal).** Faces ARE a real lever (confirmed by the hand-viewed 81%-of-top-thumbnails-have-faces). → Our emotive-face overhaul is the right direction.
- **Face SIZE +0.013, brightness ±0.00, saturation +0.005, contrast ±0.00 — essentially NO within-channel effect.** → Do NOT cargo-cult "bigger face / brighter / more saturated." They don't differentiate hits within a channel.
- **Conclusion:** measurable-average visual features give only a MODEST edge. The real CTR differentiator is what CV can't measure — the SPECIFIC emotion/expression, the concept, the curiosity, the topic. Faces are **necessary-not-sufficient**. (Caveat: haarcascade undercounts stylized/AI/painterly faces, so the face effect is likely UNDERSTATED.)

## 3. THE #1 HONEST CONCLUSION
**1% → 7% will NOT come from tuning measurable knobs (face size, brightness, colon, word-count).** It comes from: (a) an emotive human FACE + strong EMOTION as the baseline (table stakes we were missing), (b) a CONCEPT-level curiosity gap in the title+thumbnail (the outlier differentiator), and (c) **measuring our OWN per-video CTR and iterating** (the only way into the top tier — see the measurement loop). Study OUTLIERS (specific breakout videos), not averages. Never ship "good enough."

---

## 4. ACTIONABLE SYSTEMS (what to actually do)
- **Thumbnails:** the EMOTIVE-FACE template (`CTR_PLAYBOOK.v001.md` §4A) — AI-generated NON-REAL dramatized emotive face (2-stage recipe: JuggernautXL → DreamShaperXL img2img d0.55 painterly = illustrative, never a real-person likeness), face on one third / eyes upper-third, dark cool blurred bg, warm rim-lit face, 2–4 word red-bar/yellow-caps hook in negative space, second focal object. **Concept first: pick the single most shocking emotion+moment before generating.**
- **Titles:** shock-verb + specific curiosity; the two grammars (§3 CTR_PLAYBOOK); front-load the shock word; keep the literary line as the on-screen subtitle only.
- **Shorts:** `SHORTS_METHOD.v001.md` — 1s hook, loop, open-loop→payoff, 20–40s, muted-first captions, franchise the winning format, sub-conversion CTA+funnel, anonymous persona, cross-platform.
- **Packaging-first:** design title+thumbnail (or short cover+first line) BEFORE producing.

## 5. GROWTH-LEVER STACK (beyond making better videos)
Confirmed with owner (see [[pd-monetization-strategy]]): ① Shorts as the primary reach/subscriber engine (with the sub-conversion fixes), ⑤ packaging-first, ⑥ cross-platform (TikTok/Reels→YouTube; TikTok = fastest new-account reach), ② anonymous persona ("within means" face), ④ trend/news-jack occasionally (needs a trend-radar tool + rapid-response shorts), ⑦ breakout-hunting (optimize for variance — one hit 10x's a channel — not average). ③ Collabs = later. No fake hacks ever.

## 6. THE MEASUREMENT LOOP (the actual path to top 1%)
1. Ship the emotive-face packaging + strong titles + method-shorts.
2. **Measure per-video CTR** (refresh Studio cookies → `scripts/yt_studio_ctr.py`; the public Analytics API does NOT expose impressions/CTR).
3. Read each video's CTR + each short's swipe-away point; kill/redo underperformers; keep winners.
4. A/B where possible; update THIS reference with our OWN outlier data. Top 1% is reached by iteration, not a one-shot.

## 7. LIMITS & NEXT STEPS (how this reference grows — B/C)
- **TODO content-craft track:** fetch transcripts of top in-lane + storytelling videos → analyze HOOKS (first 15–30s), retention devices, narrative structure → feed DESIGN DOCS + SCRIPTS (the owner wants growth-mechanics learning, not just CTR).
- **TODO growth-mechanics teardown:** why specific channels hit 1M+ (format, cadence, shorts-vs-long, niche, series, the "first breakout video") — channel-level analysis on the corpus.
- **TODO outlier teardowns:** dissect specific breakout videos (why THIS one 10x'd its channel).
- **TODO get real CTR** (Studio cookie) to replace the views/day proxy.
- The corpus + this doc are the durable base; extend across quota-days toward the owner's 100k–1M ambition (marginal value = rarer outliers + genre breadth + craft depth; the statistical laws already stabilized here).

## 8. EVIDENCE APPENDIX (top in-lane examples)
Law By Mike "If The Police Pull You Over…" 93.5M (2nd-person, presenter face) · Explore With Us "Cops Discover Bodies in Woman's Trunk" 41.3M (bodycam REC + red-dress pop; shock-verb title) · A&E Court Cam "Crowd Cheers for Wrongfully Convicted Man" 29.2M (big crying face) · Vsauce "O.J.'s Confession" 30.4M (shock face + object) · Audit the Audit (yellow-caps template) · Justice World "YOU ARE A DISGRACE!" 24.5M (AI-painterly rage face + red circle — the §4A style reference). Full corpus + per-thumbnail coding in `scratchpad/ctr_study/`.

---
---

# PHASE 2 — GROWTH MECHANICS, OUTLIER TEARDOWNS, CONTENT CRAFT
*Appended 2026-07-24. Channel-level analysis of the same 62,527-video / 681-channel corpus (merged corpus.json + corpus2.json). Outlier-focused, honest, NOT average. Scripts: `scratchpad/ctr_study/partB.py`, `partB2.py`, `partC.py`. Method caveat that frames everything below: the harvest caps at ~150 recent uploads per channel, so "video count" and "cadence" describe each channel's RECENT posting window, not lifetime — treat cadence as directional, treat median-views/concentration as robust (they're ratios within the sampled window).*

## PART B — GROWTH MECHANICS (why channels hit 1M+)
**681 channels characterized (≥5 sampled videos). Tiers: A = ≥1M subs (n=274), B = 100k–1M (n=282), C = <100k (n=125).** For each channel: subs, shorts ratio (share of sampled uploads ≤90s), cadence (median days between uploads), median & max views, view-concentration (max÷median views), breakout timing.

### B1. THE BIG HONEST FINDING: format mechanics do NOT separate the tiers
The things everyone tells you to optimize — shorts ratio, upload cadence, "go viral / chase breakouts" — are **statistically flat across all three sub tiers**:

| Metric (median) | A ≥1M | B 100k–1M | C <100k | corr w/ log-subs |
|---|---|---|---|---|
| Shorts ratio (≤90s) | 27% | 29% | 33% | **−0.07** |
| Cadence (days between uploads) | 1.0 | 1.0 | 1.0 | −0.09 |
| View-concentration (max÷median) | 22.5 | 21.4 | 25.0 | −0.06 |
| Breakout timing (0=first→1=latest upload) | 0.28 | 0.28 | 0.27 | — |
| **Median views per video** | **79.5k** | **21.0k** | **10.2k** | **+0.385** |

Read that bottom row against all the others. **The ONLY channel-level variable that scales with subscriber count is per-video median views (+0.385).** Big channels are not posting more, not posting faster, not more shorts-heavy, and not more breakout-dependent than small ones. Every tier lives at ~22× max-to-median concentration — i.e. *even ≥1M channels are tail-powered* (one hit is ~22× their typical video). What changes with size is simply that **each upload resonates 4–8× harder** (10k → 21k → 80k median per tier step). That resonance is topic + packaging (Part 1's thesis), not a posting-mechanics hack. → **"Post shorts daily to grow" is not why anyone in this corpus crossed 1M.** Don't cargo-cult cadence or a shorts-spray.

### B2. THE NORTH-STAR CLUB (our actual goal: ~1M *average views*, not just subs)
62 of 681 channels (9.1%) have a **median video ≥1M views**. This is the club we actually want to join (owner's North Star = 1M avg views). What they do differently from the average 1M-sub channel:
- **52% are long-form-dominant (<10% shorts); median shorts ratio just 8%.** Only 27% are shorts-heavy.
- **Cadence ~4.0 days — SLOWER than the corpus median**, not faster.
- **Concentration median = 7** (vs ~22 corpus-wide) — they hit *consistently*, they are NOT living on a single lottery breakout. A high, reliable baseline is the signature of the club.

Within the ≥1M-sub tier, splitting by format makes the trap visible: **long-dominant channels median 242k views/video · shorts-heavy 111k · MIXED (10–60% shorts) just 32k.** The half-and-half channels are the *worst* performers — shorts and long-form appear to fight for the same slot. Shorts-heavy channels win a bigger *max* (viral lottery, e.g. 10.7M) but a lower sustained median. **For a 1M-AVERAGE-views goal, the evidence points at committed long-form, not a mixed or shorts-first strategy.**

### B3. OUR LANE specifically (the model to copy)
17 North-Star-club channels are in our lane (crime/police/court/law). **11 of 17 are long-form-dominant (<20% shorts); median cadence 4.1 days; median concentration 7.** These ARE our format:

| Channel | Subs | Median views | Shorts | Conc |
|---|---|---|---|---|
| Dr Insanity | 5.4M | **9.2M** | 0% | 4 |
| EXPLORE WITH US | 7.5M | **8.8M** | 8% | 5 |
| Courtroom | **0.2M** | **6.3M** | 0% | 3 |
| EWU Crime Storytime | 2.3M | 3.5M | 2% | 7 |
| Rotten Mango | 6.7M | 3.2M | 7% | 4 |
| EWU Bodycam | 3.5M | 2.4M | 11% | 7 |
| Midwest Safety | 4.3M | 1.7M | 0% | 12 |
| Code Blue Cam | 3.3M | 1.2M | 0% | 8 |

**The single most important row is Courtroom: 200k subs but a 6.3M median video and concentration of 3.** That is proof that **views come from browse/suggested via packaging+format, NOT from subscriber count** — you do NOT need a big sub base first; you need every video packaged to win impressions. (Consistent with Part 1: CTR/packaging is the bottleneck, not audience size.) Law By Mike is the lone in-lane shorts-first outlier (86% shorts, 23.7M median) — the exception that proves a *separate*, harder-to-replicate shorts-virality machine exists; it is not the path for a documentary channel.

### B4. Niche crowding (entry-lane warning)
Tier A is 20% education, 11% news, then true-crime 9% / police 8% / legal 5%. But police-bodycam is **21% of B-tier and 32% of C-tier channels** — i.e. the raw-bodycam lane is the most *crowded entry point* (everyone starts there, few break out). Our edge is not "more bodycam" — it's documentary *craft* on top of the footage (the EWU / Rotten Mango / Dr Insanity storytelling layer), which is what carries a channel from the crowded C-tier baseline to the North-Star median.

### B5. TOP-3 GROWTH-MECHANIC TAKEAWAYS FOR US
1. **Stop optimizing posting mechanics.** Shorts-ratio, cadence, and breakout-chasing are flat across every sub tier (corr ≈ −0.07). They are not the lever. The lever is per-video resonance (packaging + topic), the same conclusion as Part 1 — now confirmed at channel scale.
2. **Commit to long-form; the 1M-avg-views club is 52% long-dominant, slower-cadence (~4d), low-concentration (consistent hits).** A mixed shorts+long strategy is empirically the worst quadrant. If we run Shorts, run them as a *separate* top-of-funnel engine (per §5), never as a substitute for the long-form baseline.
3. **Copy the format+packaging discipline of Explore With Us / Dr Insanity / EWU / Rotten Mango, not a sub-count strategy.** Courtroom's 200k-subs / 6.3M-median proves impressions come from packaging into browse/suggested. Build each film to win the impression; subs follow, not lead.

## PART C — OUTLIER TEARDOWNS (the top-1% edge, not the averages)
Method: within-channel views-per-day + high absolute views + ≥8× the channel's own median (a breakout that multiplied its channel). 12 long-form (our format) + 6 shorts, all in-lane; **every thumbnail below was downloaded and visually inspected** (`scratchpad/ctr_study/outliers/`). The differentiator line is the part the crowd misses.

### Long-form breakouts (≥3 min — our format)
1. **7News Spotlight — "Father meets his children's killer" · 26.6M · 1350× ch-median (the biggest multiplier in the set).** Thumb: two ordinary men in plastic chairs in a prison yard, calm, red-box "FACE TO FACE / WITH MY CHILDREN'S KILLER." *Differentiator:* the most emotionally impossible premise on YouTube rendered with total visual RESTRAINT — no gore, no scream, no arrow. The calm is the hook: your brain cannot reconcile "children's killer" with two men sitting peacefully, so you must click to resolve the dissonance.
2. **Ruhi Cenet — "World's Highest-Security Prison: CECOT" · 178.6M · 37×.** Thumb: neutral-faced host standing amid dozens of heavily tattooed inmates, rows of caged prisoners behind. *Differentiator:* SCALE + juxtaposition — an ordinary calm man surrounded by "the most evil," visual overwhelm signalling the stakes. Tension via contrast, not expression.
3. **Cold Trace — "Piers Morgan Meets America's Most Notorious Child Psychopath" · 6.3M · 229×.** Thumb: Piers Morgan hard-staring foreground-right, shaved-head young killer behind prison mesh left. *Differentiator:* BORROWED AUTHORITY (recognizable interrogator) grafted onto a taboo subject; the mesh barrier between the two faces IS the curiosity gap ("what does a child psychopath say?").
4. **Midwest Safety — "100 Officers Hunt Down Armed Cop Killer" · 20.6M · 12×.** Thumb: aerial of a highway packed with ~100 flashing cruisers + a helicopter. *Differentiator:* the thumbnail literally delivers the title's number — SCALE as proof-of-stakes, zero faces needed.
5. **Police Watch — "Husband Laughs After Wife Found Dead Inside His Car" · 1.0M · 11×.** Thumb: bodycam, man mid-laugh (mouth wide) lit in the dark, cops behind. *Differentiator:* EMOTIONAL INCONGRUITY — laughter attached to death; the wrongness is the click.
6. **Law&Crime — "Parents Booked for Murder After 7-Year-Old Dies at 255 Pounds" · 1.2M · 8×.** Thumb: two mugshots (mother/father in jail scrubs) flanking a center inset of the child victim. *Differentiator:* MORAL-OUTRAGE mugshot template + one unbearable specific number ("255 pounds") — guilt (mugshot) vs innocence (child) in one frame.
7. **Solved Files — "Police Hunt Down Teens After Terrifying Shooting Spree" · 6.5M · 12×.** Thumb: surveillance-cam (REC/cam 01) of two armed young men walking a suburban street, hand-drawn arrow + "Dumb KILLERS." *Differentiator:* AUTHENTICITY markers (security-cam framing) + an annotation that adds a curiosity twist ("why *dumb*?").
8. **Police Ride-Alongs — "Entitled New Yorker Learns Florida Trespass Law" · 2.7M · 31×.** Thumb: bodycam of a defiant woman mid-gesture, yellow overlay quote "*Do NOT touch me.*" *Differentiator:* MID-SCENE QUOTE overlay drops you into the confrontation's peak line; entitlement = a schadenfreude hook.
9. **Code Blue Cam — "Woman Tries to Assassinate Cop Driving Her to Jail" · 10.3M · 8×.** Thumb: AXON-timestamped bodycam, handcuffed woman reaching behind her back in the cruiser. *Differentiator:* the crime captured mid-action + the raw AXON timestamp = "this is real, unedited."
10. **Law&Crime Investigates — "High School Prank Kills Mom of Four" · 10.3M · 28×.** Thumb: candid disciplinary-room footage, teens pleading to an official. *Differentiator:* mundane setting vs deadly outcome — "how does a *prank* kill?" is an irresistible causal gap.
11. **Police Insider — "When a Whole Police Station Gets Hijacked" · 10.5M · 35×.** Thumb: bodycam of a full SWAT stack aiming rifles indoors. *Differentiator:* SCALE of force + an absurd-sounding premise (a police station hijacked) = "that can't be real, show me."
12. **JRE Clips — "People Are Disappearing in National Parks: Are Aliens Abducting Them?" · 3.1M · 11×.** Thumb: Rogan + guest two-shot, both intense. *Differentiator:* BORROWED AUTHORITY + an unresolved question in the title; the thumbnail sells the credibility of the conversation, the title carries the mystery.

### Shorts breakouts (the separate engine)
13. **Law By Mike — "Who Can Escape The Bad Guy Fastest" · 196.3M · 8×.** GAMIFIED survival short (face-icon row, live timer, masked "bad guy" creeping in). *Differentiator:* FORMAT INNOVATION — an interactive game loop, not a clip.
14. **SPY Network — "8 Cops VS Giant Ex-Soldier" · 186.0M · 33×.** Bodycam, lone cop vs a huge man, caption "Suspect: 6 deployments." *Differentiator:* David-vs-Goliath framing + a mid-scene stat caption as the hook.
15. **Unit 911 / The Public Services / Cold Footage — police-clip aggregators, 33–62M, 500–750×.** Recurring pattern: vertical raw clip + **dialogue-subtitle overlay** (blue name tag + white quote, e.g. "*Meet me at the dock*", "*makes beat again*") that narrates the scene as a conversation; subjects skew *wholesome/underdog/animal* (beatboxing cops, a police dog jumping a bridge) for broad, low-friction appeal — a different emotional register from the long-form conflict thumbnails.

### The pattern the crowd misses (across all 18)
The biggest breakouts are **not** the loudest graphics. They win on an **unbearable PREMISE** (father meets kids' killer; prank kills a mom; parents starve a child to 255 lbs) shown with **RESTRAINT + AUTHENTICITY** (calm subjects, AXON timestamps, surveillance framing), optionally **borrowing a recognizable authority** (Piers Morgan, Rogan) or **overwhelming SCALE** (100 cruisers, mega-prison rows, SWAT stack). Emotion is delivered by *dissonance and stakes*, not by a screaming face. **Our takeaway: pick the single most impossible-to-ignore true fact of the case and render it calmly + authentically — that beats any amount of thumbnail volume.**

## PART D — CONTENT CRAFT (hooks / structure for our scripts + design docs)
**HONEST DATA STATUS: 0 transcripts obtained.** I attempted the public `timedtext` endpoint (all 37 targets returned empty track lists) AND the modern watch-page method (extracting the signed `captionTracks` baseUrl from `ytInitialPlayerResponse`). The baseUrls exist but every fetch returns **HTTP 200 with an empty body** — YouTube's proof-of-origin (`pot`) token now gates timedtext to real browser sessions and blocks datacenter/script IPs. This cannot be bypassed offline. → **NEEDS TOMORROW'S QUOTA / a cookied browser session** to pull real first-15-30s transcripts (scripts saved: `fetch_tt.py`, `fetch_tt2.py`; re-run inside an authenticated session). The lessons below are therefore built from **(a) the outlier title grammar we DID measure** and **(b) documented, well-known narrative structures of these specific top creators** — labeled as knowledge-based, not transcript-verified.

### D1. Hook structures of the top in-lane storytellers (knowledge-based)
- **JCS – Criminal Psychology:** cold-opens on raw interrogation-room tension with a quiet analytical voiceover; NO throat-clearing intro. Retention = slow forensic escalation of a single interview, "watch this micro-expression" re-hooks.
- **Explore With Us / EWU Crime Storytime:** open on the discovery moment or the eeriest fact, narrator immediately poses the question the video answers, then withholds it ("but what they found inside would change everything").
- **Rotten Mango / Bailey Sarian:** conversational first-person, front-load the most shocking single detail in sentence one, then promise the arc ("and it gets so much worse"). Constant tease-before-reveal.
- **MrBallen:** the canonical 1-sentence cold hook ("This is, without exaggeration, the strangest thing that ever happened in this town"), then a promise, then rewind to the beginning.
- **Wendigoon:** frames a big unresolved mystery up front and stakes ("by the end you'll understand why this terrified researchers"), long-form iceberg escalation.
- **Measured title grammar (Part 1, holds here):** the winning openers are shock-verb + specific curiosity ("realizes / discovers / caught … 45 years later"), concrete numbers/quotes ("255 pounds", "6 deployments"), and 2nd-person for rights/explainer.

### D2. TOP-3 CONTENT-CRAFT LESSONS FOR OUR SCRIPTS
1. **COLD OPEN on the single most disturbing/curious 10 seconds of the case — before any date, name, or context — then hard-cut to the title card.** Our current literary intros ("Thirty Years in the Dark") bury the hook; every top in-lane creator front-loads the peak. Rewrite every script's first 15 seconds to lead with the worst/strangest concrete fact.
2. **Plant ONE open loop in the first 20 seconds and re-hook every ~75 seconds** with a teased-but-delayed reveal ("what the second search warrant turned up doesn't make sense yet — hold that"). Place the single biggest payoff **near the END**, not the middle, so retention has a reason to run to completion.
3. **Narrate in SPECIFICS, not summary** — exact numbers, real quotes, sensory detail (the outliers that broke out all carried one unbearable specific). Where the topic allows, use **second-person framing** ("if you'd been pulled over that night…") to convert browsers, per the measured 2nd-person win for rights/explainer.

### D3. For the DESIGN docs
Choose the thumbnail CONCEPT before the script (packaging-first, Part 1 §4). Build it on **impossible-premise-shown-calmly** or **authenticity-marker** aesthetics (bodycam/AXON timestamp, surveillance framing, mugshot-vs-victim, or SCALE) — NOT a loud graphic. The on-screen literary title stays a subtitle; the packaging title carries the shock verb + specific curiosity gap.

### D4. What still needs quota (Phase 3)
- Real transcripts (first 15–30s verbatim) via an authenticated session → replace D1's knowledge-based structures with measured hook wording + timing.
- Our OWN per-video CTR (Studio cookie → `yt_studio_ctr.py`) to replace the views/day proxy (still the #1 gap, per §6).
- Frame-level retention curves for our shipped films to validate the cold-open/re-hook cadence above.

---
---

# PHASE 3 — LENGTH/FORMAT EVIDENCE, THEME-OUTLIER MINING, TOPIC PIPELINE
*Appended 2026-07-24. Same merged 62,527-video / 1,416-channel corpus (`corpus.json`+`corpus2.json`, both in the session scratchpad `ctr_study/` — NOTE the raw corpus is NOT committed to the repo; it lives in the ephemeral session scratchpad, re-harvest if lost). New offline analysis only — **0 API quota spent this phase** (all from the harvested corpus; no new search.list calls). Scripts: `ctr_study/length_an.py`, `winners_len.py`, `topic_mine.py`, `theme_rate.py`. In-lane = 17,859 videos matched by a crime/police/court/law/rights keyword on title+channel; 9,953 of them are long-form (≥3 min). Honest framing: the corpus measures **views** (and within-channel views/day percentile), NOT retention — reconciled with our live retention data below.*

## PART E — LENGTH / FORMAT (the "12 vs 20 vs longer" question, answered on winner data)

### E1. THE HEADLINE: in-lane, LONGER over-performs — the 12-min ceiling is a local optimum, not a lane law
In-lane long-form, by duration bucket (n=9,953). `medViews` = median absolute views; `wc%` = median **within-channel** views/day percentile (0–1, controls for channel size/age; channels with ≥8 long-forms):

| Bucket | n | medViews | wc% (within-channel) |
|---|---|---|---|
| 3–8 min | 1,018 | 13.4k | 0.47 |
| 8–12 min | 1,311 | 56.9k | **0.45 (worst)** |
| 12–16 min | 1,156 | 89.6k | 0.48 |
| 16–22 min | 1,304 | **140.0k** | 0.50 |
| 22–30 min | 1,469 | **154.3k (peak abs.)** | 0.48 |
| 30–45 min | 1,766 | 116.6k | 0.53 |
| 45–70 min | 1,164 | 99.9k | **0.61 (peak within-ch)** |
| 70 min+ | 765 | 116.0k | 0.58 |

Two independent signals both point the same way: **(a) absolute median views peak at 16–30 min (140–154k), roughly 2.5× the 8–12 min bucket (57k);** **(b) within-channel over-performance is LOWEST at 8–12 min (0.45) and RISES with length** (0.50 at 16–22m, 0.61 at 45–70m). The channel-dominant subset (193 channels that are ≥60% in-lane) reproduces the identical shape (16–22m=130k, 22–30m=148k). → **8–12 min is empirically the WORST long-form length in this lane.** Our house 12-min format sits at the bottom of the resonance curve.

### E2. What the WINNERS actually publish (the club we want to join)
The 11 in-lane channels whose **median video ≥1M views** (the North-Star club, `winners_len.py`) have a **median typical length of 24.4 min**; their per-channel typical lengths are `[9, 12, 13, 16, 16, 24, 26, 28, 34, 42, 47]` — **only 2 of 11 sit at ≤13 min.** The very top:

| Channel | med views | typical len | subs |
|---|---|---|---|
| JCS – Criminal Psychology | 17.7M | **42 min** | 5.6M |
| Dr Insanity | 9.2M | **28 min** | 5.4M |
| EWU Crime Storytime | 3.5M | **34 min** | 2.3M |
| EWU Bodycam | 2.7M | 16 min | 3.5M |
| Unseen | 2.2M | 24 min | 1.4M |
| The Civil Rights Lawyer | 1.3M | 26 min | 2.0M |

The in-lane channels that average ≥1M views are, overwhelmingly, **16–42-minute narrative films**, not 12-min explainers. (Courtroom @ 9.5 min / 6.3M is the lone short exception — a raw full-hearing upload, a different format we don't make.)

### E3. RECONCILING with our own live retention data (the honest tension)
Our `pd-analytics-2026-07` read said "stay at 12 min; 27–36 min finance/heist docs tanked (retention 3.6–4.2%)." That is NOT contradicted — it's **a different axis and a confounded sample**:
- The corpus measures **views**; our analytics measured **retention%**. Watch-time (the actual suggested-feed fuel) = views × length × retention. A 24-min film at 20% retention delivers **4.8 watch-min/view**; a 12-min film at 30% delivers 3.6. **Longer wins watch-time as long as retention doesn't collapse.**
- Our 27–36-min losers were **finance/heist** docs (Swartz/Wall-St/FTX) — the WEAKEST-retaining topic cluster on our channel — and pre-premium-pivot craft. That was a **topic+craft** failure at length, not proof the lane punishes length. Our retention is simultaneously **climbing** (newest-8 long-forms 26.7% vs oldest-8 13.9%) — we have craft headroom to hold a longer runtime.
- **Confidence:** length→views relationship = **MEDIUM-HIGH** (large n, two concordant metrics, replicated on the channel-dominant subset). The causal claim "make ours 20 min and views rise" = **MEDIUM** — gated on holding retention. Still UNMEASURED on our own channel: our per-video retention *curve* at 20+ min.

### E4. FORMAT VERDICT (actionable)
1. **EP51's move to ~20 min is evidence-SUPPORTED, not a risk** — 16–22 min is the abs-views sweet spot and the winner-club's home range. Do NOT retreat to 12 min.
2. **The binding constraint is retention CRAFT at length, not length.** A longer film only pays off if the cold-open + re-hook cadence (Part D) holds attention — so the length push and the hook discipline are the same project. Instrument retention on the first 20-min films (D4) before scaling runtime further toward the 24-min winner median.
3. **Do NOT make 8–12 min your long-form default** — it is the worst-resonating bucket in the lane. If a topic only sustains 12 min of real substance, that's a signal the *topic/angle* is too thin, not that short is safe.
4. Target trajectory: EP51 ~20 min → validate retention → walk toward the **24-min club median** (JCS/Dr Insanity/EWU range) as craft proves out.

## PART F — THEME-OUTLIER MINING (which STORY ENGINES over-index at the top)
Over-indexing of title words in the **top-decile** in-lane long-forms (views ≥1.81M, n=996) vs the in-lane long-form base (`topic_mine.py` / `theme_rate.py`). Lift = top-decile freq ÷ base freq.

**Single words (lift):** `heard` 6.9× · `wronged` 5.3× · `discover` 4.9× · `realizes` 4.7× · `discovers` 4.5× · `horrifying` 3.9× · `predator` 3.1× · `killer` 3.1× (and 20.6% of all top-decile titles contain "killer"). This re-confirms Part 1's **shock/discovery-verb** engine and adds the **injustice word "wronged"** as a top-3 lever — directly our wrongful-conviction lane.

**Story-engine themes (lift · share of top decile):**
| Engine | lift | % of top-decile | read |
|---|---|---|---|
| Confession / interrogation drama | **5.36×** | 3.7% | biggest lift; the JCS "watch him crack" format — high ceiling, low current volume |
| Killer / predator / evil villain | 2.79× | **24.5%** | biggest VOLUME driver — a vivid antagonist |
| Wrongful conviction / exoneration | 1.74× | 3.6% | our lane; "wronged" innocent protagonist |
| Family / relatable victim (mom/dad/son/daughter/child) | 1.64× | **22.4%** | the relatability multiplier |
| Scale / manhunt | 1.37× | 7.9% | 100-cops, SWAT (Part C's SCALE) |
| "Meets / face-to-face / forgives" | 0.77× | 0.3% | rare + huge when it hits (Part C #1), but not a repeatable volume engine |

**The synthesis for OUR lane:** the top of this lane is powered by four stackable engines — **a villain, a confession/interrogation drama, a relatable family victim, and a wronged innocent.** Our best format — the **wrongful-conviction film** — naturally stacks THREE of them (wronged innocent + coerced confession + family victim) and often a villain (the real perpetrator or the corrupt official). Pure doctrine explainers ("Can a cop follow you home?") carry **none** of these engines → that's the structural CTR liability of the SCOTUS-explainer format, independent of thumbnail tuning. **Tilt the slate from doctrine-explainer toward character-driven injustice narratives** (see Part G / the TOPIC_PIPELINE companion).

## PART G — TOPIC PIPELINE (summary; full ranked feeder = `TOPIC_PIPELINE.v001.md`)
Derived by mapping the Part F winning engines onto specific landmark cases/stories in our lane that are **NOT** in the 50-episode inventory (novelty-checked by slug + name-grep across `episodes/`, 2026-07-24). Headline: prioritize **wronged-innocent + confession-drama + family-victim** cases over pure doctrine. Top tier (all novelty-confirmed): **Cameron Todd Willingham** (executed-innocent, arson junk science), **Michael Morton** (wife murdered, real killer kills again, prosecutor hid the proof), **Walter McMillian** (framed, Just Mercy/EJI), **The Norfolk Four** (coerced false confessions — the 5.36× engine), **Scottsboro Boys / Powell v. Alabama** (right-to-counsel landmark + massive human story), **Brown v. Mississippi** (confessions by torture). Full ranked list with per-topic evidence tag, packaging angle, and ad-safety flag in the companion doc.

## PART H — CONFIDENCE & STILL-UNMEASURED (Phase 3 close)
- **MEASURED (corpus, high confidence):** length→views curve (8–12m worst; 16–30m peak); winner-club length (median 24m); theme over-indexing lifts. All from n≥900 in-lane samples, 0 quota.
- **INFERRED (medium):** that lengthening OUR films lifts OUR views — gated on retention holding (our retention trend is favorable but the 20-min curve is unmeasured).
- **STILL BLOCKED (needs quota / cookies), unchanged from Phase 2:** (1) real first-15–30s transcripts (timedtext `pot`-gated — needs an authenticated browser session); (2) our OWN per-video CTR (Studio cookie → `yt_studio_ctr.py`; the #1 gap); (3) frame-level retention curves on shipped films. These three are the remaining path to replacing proxies with our own outlier data.

---
---

# PHASE 4 — PACKAGING PATTERN LIBRARY AT SCALE, SERIES/FRANCHISE MECHANICS, HOOK TEARDOWN
*Appended 2026-07-25. Same offline 62,410-row merged corpus (`merged_rows.json`, rebuilt from `corpus.json`+`corpus2.json` — verified intact this session in the ephemeral scratchpad `ctr_study/`; re-harvest if lost). **0 YouTube Data API quota spent** (all offline). Scripts added: `ctr_study/pack_mine.py`, `pack_mine2.py`, `pack_wc.py`, `exemplars.py`. In-lane long-form set = the same 9,953 videos (crime/police/court/law keyword match, ≥3 min); top-decile = views ≥ 1.80M (n=997). This phase goes DEEP on packaging (the reference's biggest remaining offline gap) and answers a question Phases 1–3 left open: **which title patterns are real packaging levers vs. which are just the house style of channels that were already big.***

## PART I — THE PACKAGING PATTERN LIBRARY (copyable title grammar, measured TWO ways)

### I0. The method upgrade that changes the conclusions — read this first
Phase 1 measured titles one way (within-channel percentile on 38,500 long-forms) and found "features barely predict." This phase measures **two** ways and the gap between them IS the finding:
- **(A) Absolute-view over-index (lift):** how much more often a pattern appears in the 997 top-decile (≥1.8M-view) in-lane titles vs the 9,953 base. This is what a naive "study the winners" pass sees. **It is confounded** — big channels (EWU/Dr Insanity) both use a house grammar AND pull big views, so their grammar looks "winning" when it may just be *theirs*.
- **(B) Within-channel lift (delta):** does a title with the pattern beat the SAME channel's other long-forms (median within-channel views/day percentile, present vs absent)? This **controls for channel size** and isolates the actual packaging lever.
When (A) is high but (B) is ~0 or negative, the pattern is a **channel-brand marker, not a copyable lever** — copying it onto a small channel does nothing. Only patterns positive in BOTH are safe to prescribe. This resolves the apparent Phase-1/"study-winners" tension honestly.

### I1. THE ONE FACTORY TEMPLATE THAT WINS ON BOTH AXES: dramatic irony ("realizes / discovers / doesn't know he's caught")
The single most important discovery of this phase. The **dramatic-irony / perpetrator-POV** construction — the viewer knows the subject is caught before the subject does — is both the highest-volume winning grammar AND survives the within-channel control:
- Absolute over-index: `killer realizes` **7.49×**, `realizes he's` **5.76×**, `cops discover` **5.24×**, `been caught` **4.88×**, `doesn't realize` **4.73×**, `realizes cops` **4.22×**; single words `discover` 4.91×, `realizes` 4.65× (in 82/997 titles), `discovers` 4.47×.
- **Within-channel (the honest test): +0.099 percentile (n=447), the biggest robust lever in the set** — a "realizes/discovers" title beats its own channel's other films by ~10 percentile points. This is NOT a big-channel artifact; it works inside channels.
- Measured exemplars (all in-lane top views): "Mom Realizes Police Discovered Her Horrifying Secret" (32.5M) · "Serial Killer Realizes He's Been Caught 45 Years Later" (24.4M) · "Parents Discover Their Son Is A Wanted Killer" (26.1M) · "Teen Killer Doesn't Realize He's Being Recorded" (18.9M) · "Kidnapper Realizes Cops Found His Victim in a Box" (14.2M).
- **Copyable formula:** `[Perpetrator/Family role] realizes/discovers [law/family/victim] [found/knows the truth]` — optionally + a time-jump (see I2). For OUR wrongful-conviction lane this INVERTS cleanly to the *innocent*-POV: "The Real Killer Thought He Got Away — Until DNA Named Him 20 Years Later" / "He Didn't Know the Prosecutor Was Hiding the File That Proved Him Innocent." Same dramatic-irony engine, our protagonist.

### I2. THE TIME-JUMP REVEAL ("N years later") — highest within-channel lift measured
`\d+ years? later` over-indexes **5.59×** absolute AND scores **+0.340 within-channel** (n=25) — the largest within-channel delta of any pattern tested (small n, so MEDIUM confidence, but both axes and the exemplars agree). It pairs with I1 constantly: "Killer Realizes He's Been Caught **45 Years Later**" (24.4M), "**30 Years Later**" (8.9M), "How Police Captured A Killer **7 Years Later**" (14.3M). The number is a concrete curiosity spike ("*45* years?!") + a resolution promise. **Our lane owns this natively** — exonerations ARE decade-scale time-jumps ("Freed After 39 Years," "Executed. 20 Years Later, the Science Was Fake").

### I3. THE DARK-ADJECTIVE LEVER (twisted / horrifying / disturbing / chilling)
Second-biggest robust within-channel lever: **+0.084 (n=347)**; absolute over-index `twisted` 4.55×, `horrifying` 3.87×, `most twisted` 6.40×, `horrifying secret` 4.99×, `unthinkable` 3.21×. Exemplars: "The Disturbing Case of the House of Horrors Killer" (30.5M), "The Most Twisted Interrogation You'll Ever See" (11.5M), "…Her Horrifying Secret" (recurring, 9–33M). **This is the emotional-register knob we currently under-use** — our literary titles are somber but not *lurid*; a single restrained dark adjective ("The Disturbing Truth About …") is a measured lever, distinct from the shock-verb.

### I4. FAMILY-POSSESSIVE + SHOCK-VERB + CAUGHT/EXPOSED (modest but real, both axes positive)
- **Family possessive** (his wife / her son / their daughter): absolute 1.80×, within-channel **+0.032 (n=227)**. "Husband Discovers His Wife Is A Mass Killer" (14.0M), "Dad Realizes His Daughter Is Actually The Killer" (12.4M). Confirms Part F's family-victim engine at the TITLE level and stacks with I1.
- **Shock/homicide verb** (kill/murder/body): within-channel **+0.030 (n=2001)** — small per-title but the single most COMMON engine (20% of top-decile titles contain "killer"). Table stakes.
- **Caught / busted / exposed:** within-channel **+0.032 (n=435)**. The resolution verb.

### I5. THE CONFIRMED CARGO-CULT (high absolute over-index, but ZERO or NEGATIVE within-channel — do NOT copy)
These look like "what winners do" on axis (A) but are just big-channel house style; on axis (B) they do not help a video beat its own siblings:
| Pattern | Absolute lift | Within-channel delta | Verdict |
|---|---|---|---|
| `when [subject]…` clause | **2.45× (n=148)** | **−0.029** | Big-channel brand (Dr Insanity's "When Cops…" format). NOT a portable lever. |
| 2nd-person (you/your) | 1.40× | **−0.053** | Re-confirms Phase 1. Works only as a whole-channel format (Law By Mike), never as a one-off. |
| quote-marks overlay | 1.37× (n=322) | −0.036 | Channel brand, not a lever. |
| superlative ("most/worst") | 1.34× | −0.030 | Only pays as part of a compilation channel's fixed formula. |
| colon "A: B" | — | −0.015 | Re-confirms Phase 1 (+0.009≈0). |
| "confession/interrogation" *as a title word* | — | −0.046 (n=93) | NOTE: the confession *engine* over-indexes at the CONTENT level (Part F, 5.36×), but literally putting the word in the title doesn't beat siblings. Fire the engine in the STORY, don't just label it. |
**Takeaway:** the winning title is NOT "add a when-clause / a quote / a superlative." It's the dramatic-irony + time-jump + dark-adjective + family stack (I1–I4), which are levers on both axes.

### I6. WINNER-CLUB TITLE FORMULAS (the exact house grammars, for direct study)
In-lane channels with median long-form ≥1M views, their title DNA (measured from their top videos):
- **Dr Insanity** (9.1M median, 103 vids): `[Family/role] Discovers/Realizes [subject] Is A [Killer]` and `When Cops Have To [impossible duty]` and `How Police Captured [superlative] Killer`. The dramatic-irony factory.
- **EXPLORE WITH US / EWU Crime Storytime / EWU Bodycam** (2.7–11M): `[Actor] Realizes/Discovers [law/victim] [found] [Their] Horrifying Secret | Documentary` — dramatic-irony + dark-adjective + a "Documentary" franchise tag.
- **Unseen** (2.2M, 69 vids): `[Dramatic-irony premise, often "…Doesn't Know [victim] Survived"] | The Case of [Victim Name]` — a **franchise wrapper** (every title ends `| The Case of ___`) that brands the series while the front half carries the irony hook. **This is the single best template for us to adapt** (see J2).
- **Midwest Safety** (1.7M, 83 vids): `[Number] Officers [scale verb] [Killer]` — SCALE as proof-of-stakes (Part C), number-led.
- **JCS – Criminal Psychology** (17.7M median — the highest): the **lone literary-title exception** — "What pretending to be crazy looks like," "Jennifer's Solution," "Wrath of Jodi." **Important honest caveat:** JCS proves minimalist/literary titles (like our house style) CAN top the lane — but ONLY on 5.6M subs of brand trust + interrogation-footage content that delivers on curiosity. For a channel still climbing CTR from 1%, the explicit dramatic-irony template (Dr Insanity/EWU) is the lower-variance path; the literary title is a luxury you earn. Our "Thirty Years in the Dark" instinct is the JCS gambit **without JCS's brand** — that's the mismatch.

## PART J — SERIES / FRANCHISE MECHANICS (does serialization compound?)

### J1. Explicit serialization (Part N / Episode N / #N / "|") does NOT lift within-channel
Measured on all long-form with a within-channel percentile (n≈31k): titles carrying a series marker (`Ep/Episode/Part/Pt/#N/Vol/Season/"|"`) are **29.4%** of long-form and score **0.486** within-channel vs **0.503** for non-series — a mild **negative**. Explicitly numbering a video ("Part 3") does not make it beat its siblings; it may even signal "mid-series, skippable" to browse. → **Do not chase a "Part 1/2/3" serialization for CTR.**

### J2. A REPEATED TITLE FORMULA (not a number) is mildly positive — franchise the GRAMMAR, not the episode number
Videos whose title reuses a formula the channel deploys ≥4× (same 3-word opening structure) score **0.519 within-channel vs 0.500** for one-off titles (**+0.019**, n=2,639). Small but positive and directionally opposite to J1. The mechanism is Unseen's `| The Case of ___` and EWU's `…Horrifying Secret | Documentary`: a **recognizable, repeatable packaging shell** that compounds brand recognition on browse WITHOUT the "skippable Part N" penalty. **Actionable for PD:** adopt a fixed franchise wrapper — e.g. every film titled `[dramatic-irony/time-jump hook] | American Injustice` (or similar series mark) — so the slate reads as a franchise and each thumbnail/title reinforces the last, while the hook half stays fresh per episode. This is the compounding-subscriber mechanic the task asked for, and it's cheap to adopt.

### J3. Confidence
Series mechanics = **MEASURED, MEDIUM confidence** (large n, but the +0.019 formula-lift is small and the series-marker regex is coarse). The prescription (adopt a fixed wrapper, avoid Part-N numbering) is low-risk and reversible.

## PART K — HOOK TEARDOWN (the 0-second browse hook is now measured; the on-video hook is still gated)

### K1. What we CAN now say, from data: the title IS the first hook, and its mechanic is dramatic irony
The reference has always treated the first-15–30s on-video hook as the #1 retention lever (Part D). This phase measures the hook that fires **before** that — the **browse/thumbnail-title hook at t=0**, which decides the click. The winning-title grammar above IS that hook, and its dominant mechanic is now identified: **dramatic irony / open-loop resolution.** "Killer Realizes He's Been Caught 45 Years Later" is a complete open loop in seven words — subject, impossible tension (he doesn't know / we do), a number-anchored delay, and an implied payoff. The measured levers (I1 irony verb, I2 time-jump, I3 dark adjective) are all **curiosity-gap generators**, not description. → **Our scripts' cold open should dramatize the exact moment the title promises** (the arrest, the DNA match, the file found), because that is the loop the click opened; opening on context/date breaks the contract the title's dramatic irony just signed.

### K2. What is STILL blocked (honest, unchanged): verbatim on-video first-15–30s wording
This session could not obtain real transcripts. Confirmed blocks: (a) `timedtext` remains `pot`-gated (empty bodies), (b) third-party transcript mirrors return **HTTP 403**, (c) YouTube watch pages are JS-rendered so WebFetch returns only the title, (d) **WebSearch budget was exhausted (200/200) before hook-structure searches could run.** So Part D's on-video hook structures remain **knowledge-based, not transcript-verified** — but they are now *reinforced* by measured title data (K1): the title mechanic (dramatic irony, front-loaded shock) predicts the same cold-open discipline Part D inferred. **To fully close this:** an authenticated browser session (cookies) to pull first-15–30s transcripts of ~15 winners (WLSNPkf8RCU JCS-Lazarus, qzQNFzA01_0 EWU-45yrs, ZubttykEV_8 EWU-Craziest-Interrogation, Mwt35SEeR9w JCS-pretending, and the Part-C outlier IDs in `outliers/`), OR a fresh session with WebSearch budget for creator hook-structure write-ups.

## PART L — PHASE 4 CONFIDENCE & WHAT'S NEW
- **MEASURED (corpus, HIGH confidence, n≥200–2000, 0 quota):** the dramatic-irony verb is a within-channel lever (+0.099); dark adjective (+0.084); family-possessive/caught/shock-verb (+0.03); the cargo-cult list (when-clause/2nd-person/quotes/colon/superlative are channel-brand, NOT within-video levers); explicit serialization is flat-negative; a repeated title *formula* is mildly positive.
- **MEASURED, MEDIUM confidence (small n):** N-years-later time-jump (+0.340, n=25).
- **INFERRED (medium):** that the on-video cold open should dramatize the title's promised moment (follows from K1's measured title-hook mechanic + Part D's knowledge-based structures, mutually reinforcing — not independently transcript-verified).
- **STILL BLOCKED (unchanged, needs cookies/quota):** verbatim first-15–30s transcripts (K2); our OWN per-video CTR (still the #1 gap, §6); frame-level retention curves. **New this session:** WebSearch budget is a per-session cap (200) — reserve it for hooks next time.
- **NET NEW vs Phase 1–3:** Phase 1 said "titles barely predict"; Phase 4 refines that to "*surface features* barely predict, but *dramatic-irony + time-jump + dark-adjective* are real within-channel levers, while the features everyone copies (when/2nd-person/quotes/colon/superlative) are big-channel brand, not levers." That distinction — brand-marker vs portable-lever — is the phase's core contribution and directly rewrites CTR_PLAYBOOK title guidance (see TOPIC_PIPELINE for the per-topic packaging angles updated to this grammar).

---
---

# PHASE 5 — HOOK-TEARDOWN CLOSURE, ENGAGEMENT-BY-LENGTH, WRONGFUL-CONVICTION SUB-LANE
*Appended 2026-07-25 (a second same-day pass, continuing the Phase-4 session that was cut off by a transient API error). Same offline 62,410-row corpus (`merged_rows.json`; in-lane long-form re-derived = 9,740 rows, crime/police/court/law keyword match, ≥3 min). **0 YouTube Data API quota spent.** This pass (a) closes the hook-teardown loop honestly after exhausting the offline+web options, and (b) adds two genuinely NEW offline measurements — engagement (like/view) by length, and the wrongful-conviction SUB-lane exemplar pull — that Phases 1–4 never ran. The `likes` field was sitting unused in the corpus this whole time.*

## PART M — HOOK TEARDOWN: THE ON-VIDEO HOOK IS DEFINITIVELY BLOCKED THIS SESSION (do not keep retrying blind)
The task named the first-10–30s on-video hook the #1 retention lever. I attempted to obtain real verbatim hooks four ways and **all four are dead ends in this environment** — logging so a future session doesn't waste effort:
1. **`timedtext` API** — still `pot`-gated (empty bodies), unchanged from Phases 2–4.
2. **Transcript mirrors** — `youtubetotranscript.com` → **HTTP 403**, `youtubetranscript.com` → **403**, `tactiq.io` → **404**. Datacenter-IP blocked.
3. **WebSearch** — budget **exhausted at 200/200 for the whole session** before a single hook query ran (a per-session cap, shared across all prior phases; not refreshed by a new agent). Could not pull creator hook-structure write-ups.
4. **Corpus fallback** — checked whether `merged_rows.json` carries video **descriptions** (which often contain the first lines / chapter timestamps → a structure proxy). It does **not** — the schema is `title, channel, subs, views, likes, duration, publishedAt, thumb, id, dur, age, vpd`, zero descriptions. So no offline chapter/structure mining is possible either.
→ **Honest status: the verbatim on-video hook remains the single biggest un-closable gap without a cookied browser session** (unchanged conclusion from Part K/D, now *exhaustively* confirmed rather than assumed). The **browse/title hook IS measured** (Part K: dramatic-irony open-loop) and stands as the furthest offline reach. Part D's on-video hook structures stay **knowledge-based, reinforced by the measured title mechanic**, not transcript-verified. Nothing here is fabricated. **Next session with cookies:** pull first-15–30s for the ~15 IDs in Part K2 / `outliers/` — that is the whole remaining hook deliverable.

## PART N — ENGAGEMENT (LIKE/VIEW) BY LENGTH — a NEW measured retention proxy that sharpens Part E
First analysis of the corpus `likes` field. Median like-to-view ratio, in-lane long-form, by duration bucket (n=9,212 with >1k views & likes on):

| Bucket | n | median like/view |
|---|---|---|
| 3–8 min | 851 | 3.00% |
| **8–12 min** | 1,147 | **3.67% (peak)** |
| 12–16 min | 1,061 | 3.45% |
| 16–22 min | 1,224 | 3.12% |
| 22–30 min | 1,401 | 3.12% |
| 30–45 min | 1,673 | 2.36% |
| 45–70 min | 1,111 | 2.10% |
| 70 min+ | 746 | **2.01% (floor)** |

**The finding: like/view PEAKS at 8–12 min (3.67%) and declines monotonically with length to ~2.0% past 45 min — the mirror image of the views/watch-time curve (Part E), where 8–12 min is the WORST and 16–30 min peaks.** Interpretation (honest, MEDIUM confidence — like/view is a coarse proxy, confounded by topic/audience): like/view is partly a **satisfaction/retention proxy** — a viewer must stay engaged and reach the like prompt to convert, and fewer do as runtime grows. So the two curves say complementary things, not contradictory: **short videos win *enthusiasm density per viewer*; long videos win *reach + total watch-time*.** As you extend runtime you are spending engagement-density to buy watch-time.
- **This turns Part E's *inferred* "retention craft is the binding constraint at length" into a *measured* one.** The engagement-density drop is exactly what a slackening cold-open/re-hook cadence would produce. The prescription is unchanged but now evidence-backed: the length push (16–24 min, Part E) only pays if the Part-D hook discipline holds the curve up — the measurable risk of going long is real and now quantified (~1.6pt like/view erosion from the 8–12m peak to 45m+).
- **Actionable nuance:** do NOT read "8–12 min has the best engagement rate" as "go back to 12 min" — 8–12 min still LOSES on views/watch-time (Part E) and reach is the growth goal. Read it as: at 20+ min you must *earn back* the engagement-density you'd otherwise get for free at 12 min, via the cold-open + every-~75s re-hook (Part D). Instrument our own per-video like/view alongside retention on the first 20-min films.

## PART O — THE WRONGFUL-CONVICTION SUB-LANE IS NEAR-WHITE-SPACE (directly arms the TOPIC_PIPELINE)
Pulled every in-lane long-form whose TITLE carries a wrongful-conviction marker (`wrongful|wrongly|exoner|innocent|framed|freed after|DNA…free|death row…innocent|cleared`). **Only 126 videos match** — our EXACT sub-niche is thinly populated at scale. And the ones that DO win big are **not exoneration documentaries** — they're outrage-clip / bodycam formats using "innocent" as an adjective:

| Views | Channel | Title (measured exemplar) |
|---|---|---|
| 22.8M | JCS – Criminal Psychology | *Guilty until proven innocent.* |
| 20.0M | Courtroom | *Top 7 Reactions Of INNOCENT Convicts Set Free* |
| 5.4M | The Civil Rights Lawyer | *Dystopian Town Sends Lying Cop To Innocent Woman's Home* |
| 3.7M | EWU Bodycam | *When AI Gets an Innocent Man Arrested* |
| 2.6M / 2.4M / 1.7M / 1.1M×3 | The Civil Rights Lawyer | *…Arrest Innocent Hunter…* / *Woman Lies, Innocent Man Arrested, 47 DAYS in Jail — LAWSUIT* / *…Innocent Family… Then Realize…* / *…Jail Innocent Grandmother for 6 MONTHS* |

**Two honest reads of the same fact, both actionable:**
1. **White-space / opportunity:** almost nobody in-lane is winning at scale with the *sober exoneration documentary* (our EP51/52 format). That's a differentiation lane with low direct competition — the upside case for the whole pipeline tilt toward wrongful-conviction narratives.
2. **The warning inside it:** the reason may be that the sober-doc framing *under-performs the outrage-clip framing on browse.* The single repeatable WINNING grammar in this keyword space is **The Civil Rights Lawyer's franchise formula — "Cops [wrong] an Innocent [role], Then [outrage / $-lawsuit]"** (5+ videos, 1.1–5.4M each, a fixed shell = Part J franchise mechanic in action) — dramatic-irony + moral-outrage + a resolution, NOT a literary/somber title.
→ **Strategic mandate for the pipeline (sharper than before):** the wrongful-conviction FILM is our white-space, but we must **import the outrage / dramatic-irony / lawsuit-resolution packaging grammar (Part I)** onto the documentary — lead the title with the injustice + the reversal ("They Executed an Innocent Father — 12 Years Later the Science Was Exposed"), never with the literary line. The niche is open; winning it requires the clip-world's packaging aggression on documentary-grade content. This is the exact instruction now baked into TOPIC_PIPELINE's packaging angles.

## PART P — PHASE 5 CONFIDENCE & CLOSURE
- **MEASURED, NEW this pass (0 quota):** engagement/like-view by length (peak 8–12m 3.67% → floor 70m+ 2.01%, monotonic — MEDIUM confidence, coarse proxy); wrongful-conviction sub-lane is only 126 in-lane long-forms and the big winners are outrage-clip not documentary (HIGH confidence it's thin; the *why* is INFERRED).
- **NEWLY HARDENED:** Part E's "retention craft is the binding constraint at length" is now backed by a measured engagement-density decline, not inference alone.
- **DEFINITIVELY BLOCKED this environment (exhaustively verified, stop retrying blind):** verbatim on-video first-15–30s hooks (timedtext pot-gated + mirrors 403/404 + WebSearch 200/200 spent + corpus has no descriptions). Needs a cookied browser session — that is the #1 remaining research deliverable. Also still blocked, unchanged: our OWN per-video CTR (Studio cookie) and frame-level retention curves.
- **NET NEW vs Phase 1–4:** the `likes` signal (engagement-density-falls-with-length, quantified) and the sub-lane white-space map (our niche is open but demands outrage-grade packaging on doc-grade content). Both feed directly into the pipeline and the 20-min length push.
