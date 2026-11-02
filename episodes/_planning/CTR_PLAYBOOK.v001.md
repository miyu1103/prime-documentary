# CTR PLAYBOOK v001 — Thumbnails + Titles for Prime Documentary
**Lane:** legal / true-crime / wrongful-conviction / know-your-rights documentary
**Date:** 2026-07-23
**Status:** Evidence-based. Built from a hand-viewed sample of ~69 unique real thumbnails + a programmatic analysis of 205 unique high-view titles in our exact lane.
**Policy update baked in:** The old R2 "no faces on thumbnails" rule has been REMOVED by the owner. Emotive faces are now the PRIMARY recommendation. Current channel CTR ≈ 1%; target ≥ 7%.

> ⚠️ Likeness/legal guardrail that survives the rule change: we do NOT photorealistically depict the actual real defendants/victims — especially living people (Central Park Five / Exonerated Five, Anthony Ray Hinton, Ronald Cotton, Robert Williams, Anjanette Young, etc.). The face on the thumbnail is an **AI-generated, non-real, dramatized generic character** rendered in a clearly illustrative style. This gets us the #1 CTR driver (a human face + emotion) without a likeness/defamation problem.

---

## 0. How this was measured (so you can trust or challenge it)

- **Thumbnails (visual coding):** I opened and looked at ~69 unique real thumbnails — the 48 pre-downloaded top-view thumbnails across 8 genres, plus ~21 additional in-lane thumbnails I pulled fresh from the YouTube Data API (Law By Mike, A&E *Court Cam*, Audit the Audit, Explore With Us, Dr Insanity, LegalEagle, Courtroom, CBS/CNN/NY Post news, plus reaction channels like Justice World / Levi Trumbull / NowThis). Each was coded for: face y/n + count, expression, real-vs-presenter-vs-character, dominant color, focal-color pop, overlay text word-count + color + red-bar, framing gimmick, brightness, arrows/circles/emoji. Visual coding is my judgment call, so treat the percentages as **directional (±~7 pts)**, not lab-precise.
- **Titles (programmatic):** 205 unique video titles (both datasets, de-duplicated), hashtags stripped, analyzed by script for length, second-person, punctuation, numbers, capitalization, and formula patterns. These numbers are exact.

---

## 1. QUANTIFIED FINDINGS (with evidence)

### 1A. Thumbnails — the numbers (n≈69 viewed)

| Pattern | Rate | Read |
|---|---|---|
| **Has a human face** | **~81%** (56/69) | Faces dominate the lane. The no-face thumbnails are mostly explainer/mystery/documentary outliers (CGP Grey near-black jury thumb, Vox/HISTORY maps, wolves-Omegaverse), not our competitors. |
| **Face shows clear emotion** (shock / tears / fear / rage / distress) | **~30% of face thumbnails** (17/56); ~71% show at least a *non-neutral* expression | The strongest performers are high-intensity: crying, mouth-open shock, glaring rage. |
| **Big close-up face** (face ≥ ~40% of frame height) | ~13 of the 56 face thumbnails, and they skew to the emotional winners | Size + emotion is the combo, not either alone. |
| **High-saturation accent color** (red OR yellow pop) | **~35–40%** | See below — **yellow slightly out-numbers red** in the bodycam/audit sublane; red wins in the news/court-reaction sublane. |
| **Prominent RED element** (red bar/text/logo/circle/clothing) | ~13% strong (~20% if you count REC dots + logos) | Red is a *signal*, not a majority. |
| **Deliberate overlay text present** | ~60%; ~40% use NO overlay text (face + title carry it) | Big news/court outlets (A&E, CBS, CNN) often run ZERO overlay text. |
| **Overlay text word-count, when used** | **avg ~3 words, max ~5** | Short. "GETS LAWYERED", "ARREST HIM NOW!", "YOU ARE A DISGRACE!" |
| **Bright vs dark** | Winners are bright + high-contrast; muddy/dark = weak | The 2 weakest I saw (CGP near-black jury thumb; a murky Levi Trumbull night bodycam) prove the counter-case. |
| Arrows / circles / emoji present | ~15% | Red circle to spotlight a detail (Cheater Buster, Justice World tooth); emoji as accent (😬 😳 👮). |

**Framing gimmicks, most→least common in our lane:**
1. **Courtroom** (defendant + judge/lawyer, orange jumpsuit) — dominant in wrongful-conviction & Court Cam. e.g. A&E *Court Cam: Crowd Cheers for Wrongfully Convicted Man* (29.2M) — big crying face.
2. **Split-screen 2-panel** (two faces / before-after) — Courtroom's *Top 7 Reactions Of INNOCENT Convicts Set Free* (20.0M), A&E *Top 5 Most Disrespectful Defendants* (31.8M).
3. **Cutout-on-solid-bg** — the LegalEagle "GETS LAWYERED" system (Suits 13.6M, Better Call Saul 7.9M): show-still face + host face flanking a bold word block.
4. **Bodycam REC UI / doorbell PLAY / dashcam timestamp** — Explore With Us *Cops Discover Bodies in Woman's Trunk* (41.3M) with REC corners + a red-dress focal pop; Dr Insanity *Cops Realize Psycho Daughter's Car Is Filled With Bodies* (16.5M) hand-on-mouth shock over bodycam.
5. **Presenter-to-camera** (talking-head short) — Law By Mike's entire catalog (see 1C).

### 1B. The single biggest evidence-based finding

**An emotive human face is the #1 CTR driver in our lane — and it is exactly what our channel has been missing.** 81% of the top-viewed thumbnails use a face, and every one of the very highest emotional hooks (A&E crying exoneree 29.2M; Explore With Us shock-face bodycam 41.3M; Vsauce's O.J. shock-face + "I DID IT" book 30.4M; the wrongful-conviction single-tear close-ups) is carried by a face at maximum expression. Our films are literally *about* the human moment of exoneration/injustice and we have been hiding the face. That is the gap between ~1% and 7%.

### 1C. Titles — the numbers (n=205 unique)

- **Average length: 8.6 words** (median 8). Front-load the hook — mobile truncates ~ the first 40–50 chars.
- **CAPITALIZATION:** ~79% of words are Title-Cased. Title Case Every Major Word. 8% go further with ≥2 ALLCAPS shock words.
- **Two dominant grammars split the lane:**
  - **(a) Second-person imperative** (rights/explainer): only 9% overall but it *owns* the know-your-rights niche and posts monster numbers. Law By Mike: *"If The Police Pull You Over, Here Is What To Do"* (93.5M), *"Cops Don't Want You To Know This!"* (38.2M), *"You SHOULD Ask Cops This!"* (34.5M), *"Can YOU Arrest A Cop?"* (19.7M), *"Police At Your Home What Should You Do?"* (57.3M).
  - **(b) Third-person narrative present-tense** (case films): **24% of all titles**, and it is the true-crime engine. Formula = **[Subject] + [shock verb] + [disturbing object]**: *"Cops Discover Bodies in Woman's Trunk During Traffic Stop"* (41.3M), *"Mother Catches Son Bringing Chopped Up Body Into Her House"* (12.2M), *"Killer Husband Realizes Wife Is Still Breathing"* (9.7M), *"Wife Discovers Her Husband's Sick Secret"* (13.2M). Shock verbs (realize/discover/catch/find/executed/saves/freed) appear in 15%.
- **Punctuation:** 13% question mark, 13% exclamation. Curiosity/proximal "this/these" 7% ("Cops Don't Want You To Know **This**").
- **Numbers:** 17% ("Top 7 Reactions Of INNOCENT Convicts Set Free" 20.0M; "5 Writs" 4.9M).
- **"Cops/police/officer"** appears in 38% of titles — the word itself is a keyword magnet in this lane.

---

## 2. TOP 10 CTR PRINCIPLES — ranked by strength of evidence

1. **Put a big emotive human face on the thumbnail.** (81% of winners; strongest signal.)
2. **Push the expression to the extreme** — tears, mouth-open shock, dread, rage. Neutral faces underperform emotional ones even within the same channels.
3. **Make the face BIG** — occupy ~40–70% of frame height; crop tight to the eyes/mouth.
4. **Bright + high-contrast, subject rim-lit off a darker/blurred background.** Kill muddy/dark thumbnails.
5. **Front-load a shock/curiosity word in the first 3 words of the title.** Mobile truncates the rest.
6. **Use one of the two winning title grammars** (2nd-person "you" for rights/explainer; 3rd-person "[Subject] [shock-verb] [object]" for case films).
7. **Add a 2–4 word high-contrast text hook in negative space** (red bar OR yellow stroked caps). Never over the eyes.
8. **Leave clean negative space** on one side for that text (rule of thirds: face on one third, text on the other).
9. **A second focal element helps** — face + object (the O.J. "I DID IT" book; LegalEagle's Duracell battery; a redacted document; a courtroom gavel).
10. **Be visually consistent** (repeatable color/font/layout system) so the channel is recognizable in the feed — LegalEagle's "GETS LAWYERED" and Audit the Audit's yellow-caps template are recognizable brands.

---

## 3. TITLE FORMULAS THAT WIN IN OUR LANE (with rewrites of our real episodes)

Our current titles are literary and quiet — they have no shock word, no second person, no curiosity gap. That is a CTR liability. Keep the poetic line as the on-screen subtitle; make the *YouTube title* do the hooking.

| Episode (current title) | Grammar | Rewrite options |
|---|---|---|
| **EP29 Hinton — "Thirty Years in the Dark"** | 3rd-person narrative | "He Spent 30 Years on Death Row for a Murder He Didn't Commit" · "Cops Sent This Innocent Man to Death Row — Then DNA Spoke" |
| **EP30 Cotton — "The Face She Was Sure Of"** | curiosity + 2nd-person | "She Was 100% Sure She Had the Right Man. She Was Wrong." · "The Memory That Sent an Innocent Man to Prison for 11 Years" |
| **EP36 Williams — "THE ALGORITHM SAID IT WAS YOU."** | 2nd-person / tech-dread | "A Computer Said He Was Guilty — So Police Arrested the Wrong Man" · "Facial Recognition Got It Wrong and Cops Arrested Him Anyway" |
| **EP50 — "The Exonerated Five"** | narrative + number | "5 Innocent Teens. One False Confession Each. Decades Stolen." · "How Police Made 5 Innocent Boys Confess to a Crime They Didn't Do" |
| **EP38 — "Kids for Cash"** | shock-verb narrative | "A Judge Was Paid Cash to Send Kids to Prison" · "Thousands of Children Jailed So a Judge Could Get Paid" |

**Reusable templates:**
- `[Innocent Subject] Spent [N] Years in Prison for a Crime They Didn't Commit`
- `Police Were Sure They Had the Killer. They Had the Wrong Man.`
- `A [Judge/Cop/Computer] [Shock Verb] — and an Innocent [Man/Woman] Paid for It`
- `If [Police/ICE] [Do X to You], Here's What To Do` (rights shorts)
- `Cops Don't Want You To Know This About [Right/Search/Stop]` (rights shorts)

---

## 4. TWO THUMBNAIL TEMPLATE SYSTEMS

### 4A. ★ PRIMARY — "EMOTIVE FACE" (new channel default)

The default for every case film. A single AI-generated, **non-real, dramatized** human character at peak emotion.

**Subject & expression**
- ONE face, occupying **50–65% of frame height**, cropped so eyes sit on the **upper-third line** and the chin is near the lower third.
- Expression matched to the beat: **dread / silent tears / mouth-open shock / hollow stare** for the wronged party; **cold rage / smug** for the antagonist (corrupt judge, lying cop).
- **Gaze:** for a *victim/wronged* character → look slightly OFF-camera (caught-in-the-moment). For an *authority/confrontation* character (corrupt judge, cop) → look DIRECTLY at the viewer (the Justice World "YOU ARE A DISGRACE!" glare works because of eye contact). Emotion intensity matters more than gaze.
- **Style it clearly illustrative/dramatized** (semi-painterly, cinematic-render) so it never reads as a real photo of a real defendant. This is our likeness firewall.

**Placement / layout (1280×720)**
- Face pushed to the **right or left third**; the opposite ~40% of width is negative space for text.
- Optional **second focal object** in the lower opposite corner: a redacted document, a gavel, a prison ID, handcuffs, a DNA strip.

**Lighting / color**
- Bright key on the face, **rim/edge light** separating it from a **dark, desaturated, blurred background** (courthouse, cell bars, night street). This is the look that reads as "premium documentary" AND pops in the feed.
- Skin warm; background cool (teal/navy) for contrast.

**Text**
- **2–4 words, max 5.** Two options, pick per video:
  - **Red urgency bar:** solid red rectangle, white bold condensed sans (Anton / Bebas Neue), for "breaking/injustice" beats — mirrors CBS's *"after being set up by police."* red bar.
  - **Yellow stroked caps:** white + one yellow shock word, heavy black outline (the Audit the Audit / Justice World look) — for confrontation beats.
- Font: heavy condensed sans, ALL CAPS, black stroke + soft drop shadow so it survives on any background. **Never place text over the eyes.**
- Optional single **red circle** to spotlight one detail (a document line, a face) — used sparingly.

**Do / Don't**
- ✅ One face, one emotion, one 3-word hook, one accent color.
- ❌ Two competing text blocks, tiny faces, neutral expression, dark muddy mush, photoreal likeness of a real living person.

### 4B. FALLBACK — "NO-FACE / AUTHENTIC DOCUMENT" (documented alternative)

Use when a beat genuinely has no defensible human face, or as the B-side of an A/B test, or for rights/explainer/procedural topics.

- **Base image:** authentic-feeling framing — bodycam **REC-UI corners + timestamp**, a **doorbell PLAY** overlay, a security-cam wide, a courtroom wide, or a **redacted case document / evidence photo**.
- **Focal-color pop:** one saturated element in an otherwise desaturated frame (the red-dress trick from Explore With Us's 41.3M bodycam; a yellow evidence marker; a red REC dot).
- **Big red-bar text:** solid red bar, white condensed caps, **3–5 words** — the "case file / classified" energy. Or yellow stroked caps for the bodycam/audit feel.
- **Bright, high-contrast, uncluttered.** Leave one clean quadrant for text.
- Layout: text top or bottom third; focal pop and framing UI carry the rest.

---

## 5. THE #1 DRIVER, STATED BLUNTLY — and the path from ~1% to 7% CTR

**The #1 CTR driver in our lane is an emotive human face at maximum expression.** For a year the channel banned exactly that. The good news: the ban is lifted, and we can get the driver legally by using **AI-generated non-real dramatized faces** instead of real defendants. There is essentially **no CTR downside** to the face-first approach now — only the likeness rule remains, and the dramatized-illustration style satisfies it.

**Ranked, highest-leverage changes (do them in this order):**

1. **Make the emotive AI-face template (§4A) the default thumbnail for every case film.** Biggest single lever. (Evidence: 81% of winners have faces; every top emotional hook is face-carried.)
2. **Crank the expression + face size.** Tears/shock/dread/rage, face 50–65% of frame. (Emotional faces beat neutral faces within the same channels.)
3. **Rewrite titles to the two winning grammars** and front-load the shock word in the first 3 words. (2nd-person for rights; "[Subject] [shock-verb] [object]" for case films.)
4. **Add a 2–4 word high-contrast hook** (red bar or yellow caps) in clean negative space. (avg winner overlay = ~3 words.)
5. **Brighten + rim-light every thumbnail; ban dark/muddy/text-heavy frames.** (The weakest thumbnails observed were dark or text-dense.)
6. **A/B test face-vs-no-face on the same video**, and log CTR per template so this playbook updates with our own data.
7. **Lock a consistent visual system** (fixed font, accent palette, layout grid) so the channel becomes recognizable in the feed.

**Reality check on the target:** 1%→7% is a 7× lift. Thumbnail+title is the primary lever for it, but CTR also depends on impression context (suggested/browse) and the first-3-seconds retention that YouTube uses to keep serving impressions. Expect the face template to be the big step-change; then iterate with real A/B data. Measure per-video CTR before/after, don't trust a single hero example.

---

### Appendix — evidence index (video · channel · views)
- Law By Mike — *If The Police Pull You Over, Here Is What To Do* — 93.5M (2nd-person, presenter face)
- Explore With Us — *Cops Discover Bodies in Woman's Trunk During Traffic Stop* — 41.3M (bodycam REC + red-dress pop; narrative title)
- Law By Mike — *Cops Don't Want You To Know This!* — 38.2M (secret/2nd-person)
- Law By Mike — *You SHOULD Ask Cops This!* — 34.5M
- Law By Mike — *If The Police Pull You Over, Do This* — 32.7M
- A&E *Court Cam: Top 5 Most Disrespectful Defendants* — 31.8M (split-screen faces)
- Vsauce — *O.J.'s 'Confession'* — 30.4M (shock face + "I DID IT" object)
- A&E *Court Cam: Crowd Cheers for Wrongfully Convicted Man Found NOT Guilty* — 29.2M (big crying face)
- Audit the Audit — *Good Cop Gets Bad Cop Fired and Arrested* — 27.9M (yellow-caps template)
- NowThis — *Man Who Lunged at Judge…* — 25.7M (mouth-open shock face)
- Courtroom — *Top 7 Reactions Of INNOCENT Convicts Set Free* — 20.0M (split faces + number)
- Audit the Audit — *Officer Pulls Guy Over and Seriously Regrets It* — 20.9M
- Dr Insanity — *Cops Realize Psycho Daughter's Car Is Filled With Bodies* — 16.5M (hand-on-mouth shock)
- CBS — *Man freed after 18 years… he did not commit* — 13.5M (RED caption bar)
- LegalEagle — *Real Lawyer Reacts to Suits (GETS LAWYERED)* — 13.6M (cutout + red bar system)
- Justice World — *Judge… "YOU ARE A DISGRACE!"* — 24.5M (AI-painterly rage face + red circle — the reference for our §4A style)
