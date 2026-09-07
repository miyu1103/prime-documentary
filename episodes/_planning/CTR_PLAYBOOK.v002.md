# CTR PLAYBOOK v002 — Prime Documentary packaging (thumbnails + titles)
**Date:** 2026-07-25 · **Supersedes:** v001 (2026-07-23) — v001 stays for provenance; where they conflict, v002 wins.
**Evidence base (all measured this cycle):**
- **Own per-video CTR — first ever** (Studio innertube, 28-day window, all 98 uploads): `scripts/yt_studio_video_ctr.py` → `scripts/_yt_studio_video_ctr.json`. Channel CTR 1.58% / 27,015 impressions.
- **In-lane corpus n=800** (top-400 vs bottom-400 by views/day from the 62,410-row corpus) + top-1% outlier teardown (32 thumbs hand-viewed) — `scratchpad/research/corpus/REPORT.md`.
- **9 competitor channels torn down**, 90 top thumbnails hand-coded — `scratchpad/research/competitors/TEARDOWN.md`.
- **Own retention curves** (17 long-forms with data) — `scratchpad/research/retention/RETENTION.md`.

---

## 0. The headline: our own channel already proves the winning formula

| Our thumbnail | CTR (28d) | What it does |
|---|---|---|
| **carsearch `Sz8zPUoBANM`** | **4.48%** (above target!) | Pitch-dark night, two cop silhouettes at a lit front door, story mid-happening, 2 words ("YOUR DOOR?") |
| **terry `bYcqabvvxak`** | **3.14%** @ 4,070 imp | Dark rainy street, man watched by cop in lit shop window, 2 words ("STILL LEGAL?") |
| theranos `LXFjJqE6vKU` | **0.00%** @ 481 imp | Bright graphics collage: red/yellow banners, arrow, badge, icon, 5+ text elements, no human, no scene |
| florence `SOu4Y1NkGGY` | 0.71% @ 2,260 | Bright stock jail cell, 4 text elements incl. outcome-spoiling "5–4 LEGAL" stamp, no human |
| cotton `5L_HCGJxX_U` | 0.74% @ 1,760 | Eye extreme-closeup + text sandwich, giant red ALLCAPS, twist spoiled ("SHE WAS WRONG.") |
| hinton `Qyad4FejCIc` | 1.35% @ 2,880 | Face filling ~60% of frame (the measured FLOP size), 2-tone caps text |

This within-channel split matches the n=800 corpus, the 90 competitor thumbs, and the outlier teardown point-for-point. The formula is not a guess anymore.

## 1. THUMBNAIL SPEC v002 — "Night story-frame" (the PD franchise shell)

**Scene (the core change):** one cinematic **story-frame caught mid-happening** that enacts the title's irony — not a posed emotion face, not a graphics card. The viewer should feel they interrupted something wrong in progress (cops at a lit door; agents carrying boxes past a crying family; a teen led down a corridor). Calm+wrong beats loud+shock (top-1% signature).
- **DARK: median luma ~45** (our winners comply; brightness was v001's biggest error — measured, dark WINS in this lane).
- One motivated light source (doorway, window, lamp, screen); background tilts **cyan/teal**, never red.
- **Human presence mandatory**, but as a **silhouette or moderate in-scene figure (12–22% of frame height)** — faces ≥35% are 2.4× more common in flops. If a face is visible: eyes on the upper-third line (center-Y ~32%), real candid emotion, clearly illustrative/dramatized (likeness firewall).
- **Withhold the payoff**: never show the verdict/twist/outcome (no "5–4 LEGAL", no "SHE WAS WRONG"). The named object may be obscured (bagged/blurred/behind glass) — withholding is a top-1% signature.
- ★ **Sensitivity rule (hard):** race-charged cases or living real people (hinton, cotton, florence, williams, centralpark, young, …) → **silhouette / back-view / atmospheric** hero, race-neutral where identity is not the story. Exemplar: EP50 `episodes/PD-2026-050-centralpark/09_package/thumbnail.v001.png`. NEVER a photoreal likeness of a real person.
- **Authenticity styling** is welcome (procedural spaces, harsh institutional light) but **NO fake REC/bodycam/timestamp UI** — invariant 11 (no fabricated authentic records). This is where we deliberately diverge from the outlier evidence-frames.

**Text (subtract, don't add):**
- **2–4 words, ONE text element only.** White heavy condensed caps + **at most one emphasized word** (red or yellow) with black stroke — the carsearch/terry shell, kept as our recognizable franchise mark.
- **Kill on sight:** corner badges ("TRUE STORY"), stamps, arrows, second banners, citation bars, icon clip-art, "$X → $0" graphics. Red-accent-heavy frames measure as FLOP signals (25.8% of winners vs 51.5% of flops have >1% red pixels); edge-density (clutter) is a flop signal. The theranos 0.00% collage is the cautionary exemplar.
- Best text = **behavioral paradox / quote-like fragment**, not a topic label. Competitor gold standard: one real spoken line with 1 word emphasized.
- **PD wordmark chip bottom-right** (small, consistent) — franchise shell, aids feed recognition.

**Format:** 1280×720, <2MB, must read at mobile-feed size (~168px wide) — QC every thumb at small size before shipping.

## 2. TITLE SPEC v002 — long-form and shorts are different languages

**Long-form (measured over-indexers):** clean **sentence-case declarative, 6–10 words**, told as a story beat.
- Over-index: "N years later" (9.0×), realize/discover (3.7×), dramatic irony (3.5×), dark adjective (2.2×), family role (1.9×).
- **UNDER-index (anti-signals — stop using):** colon 0.34×, **em-dash/pipe 0.43×** (almost every current PD title uses "—"!), "you" 0.44×, ALLCAPS words 0.45×, questions 0.83×.
- 6 winning concept families (from the top-50 teardown): ①witnessed discovery ②doomed-perp irony ③trusted-role wrongness ④escalation-from-mundane ⑤scale-as-stakes ⑥impossible moral premise.
- Rewrite pattern: `The IRS Seized Her Entire Bank Account — For Following the Rules` → `She Followed the Deposit Rules for 38 Years. Then the IRS Took Everything.`
**Shorts (inverted grammar):** question form 3.1×, second-person "you" positive; shock verbs/numbers UNDER-index. Keep "Can police do X to you?" style for shorts only. Never port one grammar into the other.

## 3. HOOK-PACKAGING CONTRACT (from our retention curves — binds future episodes)
Every measured video loses >50% of viewers by the 10% mark, and the steepest drop is at 11–43s = the brand-OP + thesis block, not the cold open. Rules for new builds (and for judging which catalogue videos deserve packaging spend):
1. The thumbnail scene = the literal first shot; the thumb text is spoken/shown within the first 20s.
2. Delete the 0:30–1:15 thesis block — hook straight into the named, dated scene; doctrine after the first story beat.
3. Never slow-build to a reveal the thumbnail already gave away (the withholding rule protects this).
4. The thumb's tension level must be sustained on screen through minute 1, not just the 8s hook.
5. Sell a concrete unresolved event, not a person/concept (story-shaped beats essay-shaped: 0.17–0.20 end-retention vs 0.04).

## 4. EXECUTION ORDER (impression-weighted; from `priority_by_ctr.json`)
Refresh where impressions already flow but clicks don't (monthly click gain at 4% CTR): **hinton 76, florence 74, titan 68, cotton 57, hinders 51, swartz 47, dbcooper 36, terry* 35, madoff 31, milken 23** … then theranos (481 imp @ 0.00%), riley, gardner, varsityblues, tyler, carpenter, williams, katz, rajaratnam, timbs. (*terry already 3.14% — only touch with an A/B, never blind-replace a proven winner.)
Process: **proof batch of 3 → owner approval → mass-produce in agent batches of ~10 → apply via `apply_thumbnails_v002.py` (publishAt-safe, exact-title match, #Shorts excluded) → re-measure per-video CTR after 2–4 weeks** (`yt_studio_video_ctr.py`; needs a fresh Studio cookie exported immediately before running — tokens rotate within the hour).

## 5. Measurement loop
- Per-video CTR baseline saved 2026-07-25 (`_yt_studio_video_ctr.json`). Re-pull after each refresh wave; kill/redo anything that doesn't move toward 4–6%.
- Playbook is a living doc: update on OUR outlier data first, corpus second (top-1% principle — copy outliers, not medians).
