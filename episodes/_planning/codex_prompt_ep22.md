# CODEX HANDOFF — EP22 Michael Milken: Genius, or the Face of Greed? (PD-2026-022-milken)

> The single design document Codex reads to BUILD the episode. Claude owns the LEFT side
> (topic/research/claims/script) — done and LOCKED. Codex owns the RIGHT side
> (scenes -> images -> narration -> music -> motion -> edit -> render -> thumbnails).
> Build the FIRST render to satisfy the whole acceptance table. Numbers, not adjectives.

## 0. HARD CONSTRAINTS (do not cross) — R3, LIVING + PARDONED
- **LIVING person who PLEADED GUILTY and was later PARDONED.** Strictly record-based and neutral.
  - NEVER say "convicted at trial", "convicted of insider trading", or "convicted of racketeering/RICO." He did
    NOT go to trial; there is no standalone insider-trading or RICO conviction.
  - ALWAYS distinguish **CHARGED** (98-count indictment, 1989, incl. RICO) from **PLEADED** (SIX felony counts,
    April 1990: securities/reporting, conspiracy, mail fraud, tax). Charges are accusations, not findings; the
    RICO charge and the other 92 counts were DROPPED.
  - The **2020 pardon is clemency, NOT innocence/exoneration**: the guilty plea STANDS and the pardon did NOT
    lift the SEC **lifetime industry ban**. (The White House line "pleaded guilty in 1989" is imprecise — the
    plea was April 1990; never repeat the 1989 date as the plea date.)
  - The **genius-vs-greed** debate is **ATTRIBUTED** ("critics argue / defenders argue") — never narrated as
    settled fact, in VO, captions, on-screen text, or thumbnails.
- **No real-person likeness** anywhere (not Milken, Boesky, any official/president/raider/supporter). **No real
  logos or seals** (Drexel/SEC/DOJ/White House/YouTube/presidential). **No readable text in images** (Remotion
  adds all text). **No real artwork/building interior/landmark.** Symbolic reconstruction only; nothing looks
  like authentic footage or an authentic record.
- "~$600 million" = **$200M fine + $400M restitution fund** (1990 criminal resolution); later civil settlements
  are separate — do not fold them in. Sentenced to 10 years, reduced; **served about 2 years**.
- No publish, no external upload, no paid API without owner approval + idempotency + budget check.
- Render LOCAL CPU libx264, quality-first; NEVER NVENC. Heavy media -> H:\pd-media\episodes\PD-2026-022-milken\.

## 1. BINDING SPEC + ACCEPTANCE
- Canonical spec: **docs/PD_ONE_PASS_PRODUCTION_SPEC.v2.md** (binding for EP19+). Build to rows 1-16.
- "Done" = the independent gate exits 0 (not your opinion):
  ```
  ./.venv/Scripts/python.exe scripts/check_final_acceptance.py 22 --json
  ```
- Duration profile: **mid, target 30:00** (runtime band 27-33; narration ~26.8 min at the measured ~173 wpm,
  filled to runtime with the hook montage, OP/ED bookends, music beats, and the CTA hold).

## 2. LOCKED INPUTS (DO NOT REWRITE)
- Script: episodes/PD-2026-022-milken/03_script/script.en.v001.md (~4,637 words; [VO:] only; "#" lines = production notes).
- Annotated: 03_script/script.annotated.v001.json (76 spans, claim_ids + visual_intent).
- Claims (R3 wording locks): 01_research/claims.v001.json (13 claims). Sources: 01_research/sources.v001.json (11).
- **R3 WORDING LOCKS (must hold in every caption / on-screen text / thumbnail):** pleaded guilty (never convicted
  at trial); pleaded to SIX felonies (no insider-trading/RICO conviction); CHARGED (98) vs PLEADED (6), RICO + 92
  dropped; ~$600M = $200M fine + $400M restitution; SEC lifetime ban remains; 2020 pardon = clemency not innocence;
  genius-vs-greed attributed only.

## 3. STRUCTURE & TIMING (per the script timecodes)
- Hook ~0:00-0:08 fast highlight montage (EP22-IMG-001..006, ~2s cuts) -> Opening (The Two-Sided Man) ->
  Body (Act 1 The Idea / Act 2 The Empire / Act 3 The Fall / Act 4 The Reckoning & the Forgiveness) -> Ending
  (Your Verdict) + dedicated CTA beat.
- Gold BrandOpening lands AFTER the hook; BrandEndcard at tail. OP/ED canonical = remotion/src/components/Bookends.tsx
  (OPENING_SEC 3.5 / ENDCARD_SEC 9; DO NOT fork). Drive EP22 through CasePremiumFromRoughCut (register in Root.tsx if needed).

## 4. VOICE (row 2)
- ElevenLabs master, VOICE_ID nPczCjzI2devNBz1zQrb, eleven_multilingual_v2, stability 0.35, similarity 0.80,
  style 0, speaker_boost on. Speak ONLY [VO:] lines; ignore "#" lines; strip [CLM-xxxx]. SAPI/local FORBIDDEN in final.
- HARD BUDGET CAP for narration: $25. Idempotency key per chunk; never double-bill an existing chunk.

## 5. CAPTIONS (rows 3-4)
- Force-align to the rendered ElevenLabs audio (verbatim, NOT pasted from script). 1 cue = 1 breath group. <=2 lines,
  <=42 chars/line, 1.0-6.0s, <=17 cps, >=2-frame gaps, brand font, bottom-safe (lower 10-15%), drop-shadow, coverage >=95%.
- Captions must also honor the R3 locks (e.g. never let an auto-caption read "convicted"; verbatim from the VO, which is clean).

## 6. MUSIC / BGM (row 1)
- Continuous library bed, one track per chapter (8-category set). Duck under VO to a FLOOR ~ -22 LUFS — the bed
  MUST stay audible under narration; never duck to silence. No silent stretch > 25s. Integrated -16..-12 LUFS.

## 7. IMAGES — Codex generation (row 5) — FULL MEGA-PROMPTS IN APPENDIX A (this document)
- **The complete image library (74 numbered MEGA-PROMPTS, EP22-IMG-001..074) is written out in full in
  APPENDIX A at the END of this document** — it is self-contained, so you do not need any other file to generate.
  (An identical mirror also lives at episodes/PD-2026-022-milken/04_scenes/codex_image_prompts.v001.md; if the two
  ever differ, APPENDIX A here is authoritative.)
- **Generate exactly ONE image per prompt (74 total), NOT a candidate pool.** Regenerate ONLY a specific shot that
  fails the Hard Rules (§A.0) or Quality Bar (§A.3). Appendix A's Hard Rules / Style Bible / Universal Negative /
  Quality Bar are binding for every generation.
- Output >= 3840 px long edge, 16:9; brand palette (black/midnight-navy + electric-blue #1F6BFF + gold #E5B53A + silver).
- Reject any still with a face/likeness, a real logo/seal, any readable text, a real artwork/landmark, or anatomy
  errors. Register every used still in the rights manifest (origin=Codex AI, AI-disclosed; no real-person likeness).

## 8. MOTION / EDIT (row 8) — fixes weak animation / stutter / boring stills
- NO static image; NO frame held > 2s; NO naked hard cut. Ken Burns >= 6% / parallax on every still; hero beats
  get SVD/organic motion + ink/particle overlays. Designed transitions 0.3-0.5s crossfade; OVERLAP Sequences by
  the transition length (no 1-frame black/jump); carry motion through the cut (no velocity reset = the "kaku");
  Trail motion blur on fast moves (hook montage, the tower of money, the indictment collapse). Average shot <= ~6s.
- Abundant material (row 7): factory shelf densely — >= 1 distinct clip per ~25-30s; every span >= 1 layer; factory
  layer across >=40% of the timeline; no clip reused > 3x. scripts/select_factory_assets.py --theme finance/legal/crime
  (trading floors, courthouses, money, vaults, 1980s textures, clinical/lab for Act 4).

## 9. DEDICATED SUBSCRIBE+LIKE CTA (~29:10–29:35)
- Build EXACTLY to the "# [PRODUCTION - DEDICATED CTA BEAT ...]" note in the script: gold SUBSCRIBE pill slides up
  from the lower third (spring damping 14 / stiffness 120, ~0.45s) + gold underline wipe (Easing.out(cubic), 0.5s);
  white outline thumbs-up LIKE icon pops in (spring damping 10 / stiffness 140) and, on the spoken word "like",
  FILLS solid gold with one 6% scale pulse + a soft particle spark (Trail motion blur); subtle navy vignette;
  hold ~5s; ease out 0.4s; one soft UI "click" SFX on the like-fill; music dips ~3 dB but the bed stays audible.
  NO real YouTube logo or real-person likeness; PD brand styling. Backdrop = EP22-IMG-074.

## 10. THUMBNAILS (rows 11-13)
- >= 3 variants as Remotion <Still> at 1280x720, backgrounds from the image library (split gold/blue figure /
  X-shaped desk / tower of money / pardon parchment beside the locked padlock — NO face, NO real logo/seal).
  "Loud": UPPERCASE headline <= 3-4 words, huge subject, very high contrast black/navy + gold #E5B53A or electric
  #1F6BFF accent, white/silver text, legible at 320px. Title <= 60 chars; A/B title x thumb.
- Headline ideas (all R3-safe; no "convicted"): "GENIUS OR GREED?" / "$550 MILLION. ONE YEAR." / "PARDONED, NOT
  CLEARED" / "98 CHARGES. 6 PLEAS." Pick a selected; DO NOT upload.

## 11. RETENTION / LIKE-RATE (row 16) — engineered in the script
- Cold-open question (genius or greed?) is paid off in the Ending and is the explicit Like/comment ask in the CTA;
  re-hooks every ~2-3 min (the $550M number, the "highly confident" letter, Boesky, the 98->6 collapse, the cancer
  turn, the pardon-vs-ban split). Keep the edit tight so retention stays flat-to-rising.

## 12. DEFINITION OF DONE (then STOP for owner)
- check_final_acceptance.py 22 exits 0; rows 4,5,7,8,11,12,13,15,16 measured -> 0 violations; check_dynamics.py and
  check_runtime_band.py on the render exit 0.
- First-cut -> title/thumbnail -> pre-publish review -> scheduling = owner gates, in order. Final-script approval
  APR-0001 is currently PENDING. **Before publish (R3): re-confirm the subject is living, and lock verbatim
  White House pardon-statement / court (indictment & plea) / SEC quotes on the live records.** Do not treat the
  script as owner-approved until APR-0001 flips. PUBLISH requires R-level legal review first.

---

# APPENDIX A — IMAGE MEGA-PROMPT PACK (EP22-IMG-001..074) — AUTHORITATIVE

> Self-contained image spec for Codex. **Codex image generation = PRIMARY** (SDXL is fallback only).
> Generate **exactly ONE image per prompt (74 total)** — NOT a pool of candidates. Regenerate ONLY a
> specific shot that fails A.0/A.3. Heavy output -> H:\pd-media\episodes\PD-2026-022-milken\.
> Section numbers below (0-7) are referenced elsewhere in this doc as A.0 .. A.7.

## 0. ABSOLUTE HARD RULES (R3 — read first, apply to EVERY image)
1. **NO real-person face or likeness of ANYONE** — not Milken, not Boesky, not any official, judge, president,
   raider, or supporter. People are anonymous: from behind, cropped at the shoulders, silhouettes, hands only,
   out of focus. No look-alikes. (Milken is alive and was pardoned — likeness risk is real; symbolism only.)
2. **NO real logos, seals, or trademarks** — no real bank/firm logo (no Drexel mark), no real SEC/DOJ/White House
   seal, no real YouTube logo, no presidential seal. Build archetypal equivalents (a blank wax seal, a generic
   government-style crest with no readable text).
3. **NO readable text inside the image** — no letters, numbers, dollar figures, signage, watermarks, readable
   documents/screens/tickers. All numbers, names, dates, citations and UI are added later as Remotion typography.
4. **Symbolic reconstruction only** — nothing looks like authentic 1980s/1990s news footage, a real photograph,
   surveillance, or an authentic court/government document.
5. **No depiction of a real artwork, real building interior, or identifiable landmark.** Use archetypal finance,
   courtroom, and clinical environments.
A face/likeness, a real logo/seal, readable text, or an authentic-looking record = automatic reject and regenerate.

## 1. GLOBAL STYLE BIBLE
- **Genre:** prestige financial-true-crime / character-study noir; "1980s money, power, and consequence."
- **Palette (PD brand, strict):** deep black + midnight-navy base; **electric blue `#1F6BFF`** as the cold
  "law / investigation / consequence" signal; **muted gold `#E5B53A`** as the "money / genius / value" accent;
  silver-grey highlights. Restrained filmic contrast. No candy neon, no teal-orange.
- **Light:** motivated and low-key — a single desk lamp on a trading floor before dawn, sodium streetlight,
  cold courthouse daylight, a clinical overhead, moonlight through tall windows. Real falloff, deep shadow,
  volumetric haze where it earns depth.
- **Texture/material:** brushed brass, aged paper and ledgers, pinstripe wool, marble, frosted glass, vault
  steel, wax, parchment, hospital steel, fine cinematic grain. No plastic AI sheen.
- **Composition:** one clear subject; deliberate negative space for Remotion text; strong fore/mid/background
  depth; built for slow push, parallax, or crop.
- **Output:** 16:9, long edge **>= 3840 px (3840x2160)**, highest quality; compose with upscale crop room.
- **Recurring motifs:** the X-SHAPED TRADING DESK; the GOLD vs SHADOW split figure (builder/convict); the
  closed VAULT door; the rising GOLD yield curve; the single glowing "highly confident" page; the small predator
  vs the whale (the leveraged takeover); the TOWER OF MONEY; the INDICTMENT STACK collapsing to six pages; the
  RICO/long-shadow; the PRISON-CAMP gate; the HEARTBEAT line; the PARDON parchment + blank wax seal beside a
  still-locked PADLOCK; the BALANCED SCALE; the GOLD QUESTION MARK.

## 2. UNIVERSAL NEGATIVE (append to every generation)
`face, facial features, eyes, portrait, recognizable person, celebrity, look-alike, politician, real logo,
brand mark, corporate logo, government seal, presidential seal, YouTube logo, trademark, readable text, letters,
numbers, dollar figures, signage, ticker text, watermark, caption, real document, authentic photograph, news
footage look, surveillance look, distorted hands, extra fingers, mangled anatomy, plastic skin, waxy AI sheen,
overprocessed HDR, halo, cartoon, 3d render look, video-game look, neon candy colors, teal-orange grade,
cluttered frame, stock-photo lighting, real landmark, real building interior.`

## 3. QUALITY BAR (reject unless ALL pass)
- Clear subject + negative space for text; mobile-readable focal point at 320px.
- Motivated, controlled light; cinematic depth; no flat stock look; no black crush.
- Believable materials + grain; no plastic sheen; clean anatomy on any implied figure.
- Narrative duty: locate / explain / build tension / symbolize the exact beat.
- Safety: no face/likeness, no real logo/seal, no readable text, no real artwork/landmark, not authentic-looking.
- Editability: parallax/Ken-Burns friendly, crop room, doesn't fight bottom-safe captions.
- Neighbor fit: distinct from adjacent shots.

## 4. SCENE MAP (74 hero stills, keyed to 76 spans)
- HOOK EP22-IMG-001..006 · OPENING 007..014 · ACT1 The Idea 015..030 · ACT2 The Empire 031..046 ·
  ACT3 The Fall 047..060 · ACT4 The Reckoning & Forgiveness 061..068 · ENDING 069..074.

---

## 5. MEGA-PROMPTS

### HOOK (~0:00–0:08 fast flash-forward montage, ~2s cuts)

**EP22-IMG-001 · hook: the lone king at the X-desk · A · 1**
A vast empty trading floor before dawn, one anonymous figure (from behind, shoulders only, faceless) seated at a
single **X-shaped** trading desk lit by one warm **gold** desk lamp, banks of dark dead screens around him in
deep **navy** shadow; lonely power, the center of a hidden empire; no face, no readable screens, no logo, no text;
cinematic symbolic still, 35mm grain, big dark sky of negative space for a headline.

**EP22-IMG-002 · hook: the tower of money · A · 1**
A towering, slightly unstable column of banded cash and paper bond certificates rising into black, edge-lit in
**gold**, a cold **electric-blue** rim from one side; impossible wealth stacked into the dark; no readable
numbers/text, no logo; museum-grade cinematic still, heavy negative space above.

**EP22-IMG-003 · hook: the gavel and the shadow · A · 1**
A single brass courtroom gavel resting on a marble block, one hard **electric-blue** key light throwing a long
dramatic shadow across pale stone, deep black surround; the law arriving; no text, no seal, no face; tense,
minimal, cinematic macro with negative space right.

**EP22-IMG-004 · hook: the prison-camp gate · A · 1**
A plain chain-link and steel gate of a low minimum-security facility at dusk, one sodium lamp, long fence line
vanishing into **navy** mist, no signage, no people; the fall made concrete; no readable text, no logo;
cinematic wide symbolic still, cold and quiet, negative space sky.

**EP22-IMG-005 · hook: the pardon parchment · A · 1**
A single sheet of heavy cream parchment on black, a deep-red **blank** wax seal and a length of ribbon catching
one warm **gold** light, the rest in shadow; clemency, mercy, a stroke of a pen; absolutely no readable text, no
real seal/crest; elegant cinematic macro, shallow focus, negative space.

**EP22-IMG-006 · hook: genius or greed (the split figure) · A · 1**
A single anonymous suited figure shot dead-center from behind, the left half washed in warm **gold**, the right
half in cold **electric-blue** shadow, hard split down the spine, black void around; the unresolved question of
the whole film; no face, no text, no logo; iconic cinematic still, strong central negative space for a title.

### OPENING — The Two-Sided Man (~0:08–3:00)

**EP22-IMG-007 · opening: a man the world can't decide on · A · 1**
A faceless suited silhouette standing at the exact center of a wide black frame, two opposing soft glows — **gold**
from the left, **electric-blue** from the right — meeting on his shoulders without resolving; ambiguity as a
portrait; no face, no text; cinematic, symmetrical, vast negative space.

**EP22-IMG-008 · opening: the admirers' light · A · 1**
Low angle of an open doorway flooding warm **gold** light into a dark room, an anonymous crowd of small
silhouettes streaming toward it from shadow; the door of capital thrown open, the genius narrative; no faces, no
text, no logo; cinematic, hopeful-but-uneasy, negative space.

**EP22-IMG-009 · opening: the critics' verdict · A · 1**
A cold **electric-blue** spotlight on an empty pinstripe suit jacket hung like a husk on a stand, long shadow,
black surround; greed given an empty shape; no face, no body, no text; stark symbolic still, negative space.

**EP22-IMG-010 · opening: both at once · A · 1**
A single coin spinning on a marble surface, motion-blurred so both faces blur into one ungraspable disc, one
**gold** edge, one **electric-blue** edge, dark fall-off; everything true at the same time; no readable text, no
markings; macro cinematic still with shallow focus, negative space.

**EP22-IMG-011 · opening: a kid from the LA suburbs · A · 1**
A wide, quiet 1960s-style Southern California suburban street at golden hour, palms in silhouette, long empty
sidewalk, warm haze; the ordinary origin of an extraordinary story; no faces, no readable signs, no logos;
cinematic establishing still, soft grain, negative space sky.

**EP22-IMG-012 · opening: the idea no one saw · A · 1**
A single shaft of **gold** light falling on one overlooked page in a heavy stack of grey ledgers in a dark
archive, dust in the beam; a simple insight everyone walked past; no readable text; cinematic macro, shallow
focus, negative space.

**EP22-IMG-013 · opening: the line he crossed · A · 1**
A clean **gold** line painted across a dark polished marble floor, one anonymous dress shoe (cropped, from above)
poised right at its edge, cold **electric-blue** shadow; the moment genius becomes a crime; no text, no face;
tense minimal cinematic still, negative space.

**EP22-IMG-014 · opening: the unanswered question (title card backdrop) · A · 1**
The split gold/blue silhouette from a respectful distance on a dark gallery-clean wall, a faint **gold** question
mark suggested in the negative space (as shape, not text), composed with a large clean lower third for the brand
title; resonant, minimal; no readable text, no logo; cinematic, heavy negative space.

### ACT 1 — The Idea (~3:00–9:00)

**EP22-IMG-015 · act1: what a bond is · A · 1**
Two anonymous hands (only hands) passing a single glowing **gold** paper certificate across a dark desk toward a
small stack of banded cash; a loan, in one clean image; no readable text/numbers, no logo; cinematic macro, warm
key, cold rim, negative space.

**EP22-IMG-016 · act1: the report card of debt · A · 1**
An abstract grid of blank rectangular cards floating in **navy** dark, the top rows glowing clean **gold**
(investment grade), the lower rows fading to cold grey-blue, no letters or numbers on them; the rating ladder;
no readable text; clean cinematic symbolic still, negative space.

**EP22-IMG-017 · act1: the blue chips · A · 1**
A row of tall, identical polished marble columns lit in cool clean light, pristine and untouchable, one
**gold** glow at their base; the established giants everyone trusts; no logos, no text; architectural cinematic
still, deep perspective, negative space.

**EP22-IMG-018 · act1: stamped "junk" · A · 1**
A single bond certificate (blank, no readable text) lying in shadow with a hard rubber-stamp impression of an
abstract mark slammed across it in faded ink, harsh **electric-blue** side light; the cold verdict of the market;
no readable letters/numbers; gritty cinematic macro, negative space.

**EP22-IMG-019 · act1: the closed door · A · 1**
A heavy steel vault-style door, firmly shut, in a dark wall, one small cold light above it, a long empty floor in
front; capital locked away from the shut-out; no signage, no logo, no text; stark cinematic still, deep negative
space.

**EP22-IMG-020 · act1: the label became the reality · A · 1**
A single small struggling sapling in cracked dry earth under a cold **electric-blue** spotlight while, far behind,
out of reach, a warm **gold** glow of water/light; starved of capital by its own label; no text; symbolic
cinematic still, shallow focus, negative space.

**EP22-IMG-021 · act1: the insight (the basket) · A · 1**
A scatter of dull grey bonds gathered into one woven basket where, together, they begin to glow warm **gold** from
within, a few dark ones still among them; the diversified-basket idea — the whole pays more than the few that
fail; no readable text; cinematic macro, dramatic key, negative space.

**EP22-IMG-022 · act1: fear is overpriced · A · 1**
A balance scale where a small **gold** weight clearly outweighs a large, hollow, cracked grey mass labelled only
by its size; risk priced too high; one **electric-blue** rim light, black surround; no text; symbolic cinematic
still, negative space.

**EP22-IMG-023 · act1: the opportunity hiding in plain sight · A · 1**
A dark room full of grey filing drawers, one drawer pulled open spilling warm **gold** light no one else has
noticed; the untapped opportunity; no readable labels/text; cinematic, shallow focus, strong negative space.

**EP22-IMG-024 · act1: opening the door for the shut-out · A · 1**
The heavy vault door from IMG-019 now cracked open, warm **gold** light pouring out across the dark floor toward
small anonymous silhouettes approaching; the closed door opened; no faces, no text, no logo; cinematic, hopeful,
negative space.

**EP22-IMG-025 · act1: the ordinary company · A · 1**
A modest dark factory/warehouse exterior at dawn, shutters down, one hopeful **gold** light in a single window;
the striver business the banks waved away; no readable signage, no logo; cinematic establishing still, soft grain,
negative space.

**EP22-IMG-026 · act1: Drexel, the scrappy outsider · A · 1**
A single mid-tier office tower standing apart from a distant cluster of taller, colder towers, warm **gold** light
in its windows against **navy** dusk; the second-tier firm that tried harder; no logos, no readable text;
cinematic wide still, negative space sky.

**EP22-IMG-027 · act1: across the country to Beverly Hills · A · 1**
A stylized dark map texture with a single glowing **gold** arc sweeping from an east-coast point to a west-coast
point, palms suggested in silhouette at the western end; the move to California; no readable place names/text;
cinematic graphic still, negative space.

**EP22-IMG-028 · act1: the X-shaped desk before dawn · A · 1**
A clean hero shot of the empty **X-shaped** trading desk seen from above, four arms radiating, one warm **gold**
desk lamp at the crux, banks of dark screens around, pre-dawn blue at the windows; the legendary desk; no readable
screens/text, no logo; cinematic, strong geometry, negative space.

**EP22-IMG-029 · act1: a statement of distance · A · 1**
Lone palm trees in **gold**-rimmed silhouette in the foreground, the cold distant glow of an east-coast skyline
tiny on the far horizon across black water; building a rival empire three thousand miles away; no text, no logo;
cinematic wide still, deep negative space.

**EP22-IMG-030 · act1: the money pouring through · A · 1**
A torrent of warm **gold** light and paper streaming through the open vault door into the dark, small silhouettes
catching it; the idea working, capital flowing to the upstarts; no faces, no text; dynamic cinematic still (built
for a push-in), negative space.

### ACT 2 — The Empire (~9:00–15:00)

**EP22-IMG-031 · act2: the kingdom · A · 1**
A single illuminated **gold** desk on a raised dais at the center of a vast dark hall, faint concentric rings of
empty chairs around it; a business that became a kingdom; no face, no text, no logo; cinematic, awe-and-unease,
heavy negative space.

**EP22-IMG-032 · act2: the market explodes · A · 1**
A rising **gold** mountain-range graph line erupting upward out of a small dark base, sparks of light at its peak,
cold **electric-blue** grid behind (no numbers); the high-yield market swelling past a hundred billion; no
readable text/numbers; cinematic graphic still, negative space.

**EP22-IMG-033 · act2: all roads lead to him · A · 1**
A dark aerial of many faint roads/threads converging on one single warm **gold** point of light; if you wanted
serious money, the road ran through Beverly Hills; no text, no labels; cinematic symbolic still, negative space.

**EP22-IMG-034 · act2: the takeover era · A · 1**
A small sleek predator fish lit in cold **electric-blue** circling a vast slow whale-shape in dark water, one
**gold** glint in the predator's wake; the leveraged takeover — small swallows large; no text; cinematic
symbolic still, deep negative space.

**EP22-IMG-035 · act2: changing the math · A · 1**
An abstract balance where a tiny figure on one pan is lifted level with a giant figure on the other by a stream of
**gold** poured underneath it; debt as leverage; faceless, no text; clean cinematic symbolic still, negative
space.

**EP22-IMG-036 · act2: the "highly confident" page · A · 1**
A single sheet of fine paper held in one anonymous hand, glowing as if radioactive with quiet power under a
**gold** light, a boardroom dissolving into shadow behind; the letter the market treated as good as cash; no
readable text on the page; cinematic macro, shallow focus, negative space.

**EP22-IMG-037 · act2: chill in the boardroom · A · 1**
A long empty dark boardroom table with one cold **electric-blue** shaft of light falling on a single empty chair
at its head; executives who suddenly felt hunted; no faces, no logo, no text; cinematic, tense, deep perspective,
negative space.

**EP22-IMG-038 · act2: keys to the neighborhood · A · 1**
An anonymous hand (only the hand) holding out a single **gold** key over a dark scattering of tiny rooftops/towers
below; no company too big to be a target; no text, no logo; cinematic symbolic still, shallow focus, negative
space.

**EP22-IMG-039 · act2: the annual gathering · A · 1**
A grand dark ballroom with a single warm **gold** chandelier glow, faint anonymous silhouettes gathered at the
edges around one bright center; the yearly conference where deals were struck; no faces, no text, no logo;
cinematic, opulent-yet-ominous, negative space.

**EP22-IMG-040 · act2: $550 million in one year · A · 1**
An almost absurd single column of banded cash rising far higher than faint office towers in the **navy**
background, **gold** edge light, the top lost in dark; one man's single-year pay; no readable numbers/text;
cinematic, vertiginous, tall negative space.

**EP22-IMG-041 · act2: more than the companies he financed · A · 1**
A small **gold**-lit desk on one side of a dark scale dramatically outweighing a cluster of whole office buildings
on the other; the scale of his personal fortune; faceless, no text, no logo; cinematic symbolic still, negative
space.

**EP22-IMG-042 · act2: a financial superpower · A · 1**
A lone anonymous figure at the **X-shaped** desk casting a colossal shadow up a dark wall, **gold** key light;
one man, one desk, the power of a nation's capital; no face, no text; cinematic, dramatic, negative space.

**EP22-IMG-043 · act2: it lived in one head · A · 1**
A single warmly lit head-shaped void (an empty illuminated silhouette, no face/features) with fine **gold** threads
of connection radiating out into dark; the web only he fully understood; strictly no face/features, no text;
abstract cinematic still, negative space.

**EP22-IMG-044 · act2: imitators and investigators · A · 1**
Two sets of faint silhouettes flanking one central **gold** glow — one side warm (imitators), one side in cold
**electric-blue** (investigators) — converging; power attracts both at once; no faces, no text, no logo;
symmetrical cinematic still, negative space.

**EP22-IMG-045 · act2: too powerful · A · 1**
A single chess king piece carved from **gold** standing alone and oversized among toppled grey pawns on a dark
board, hard **electric-blue** rim; a man who had become too powerful; no text; cinematic macro, negative space.

**EP22-IMG-046 · act2: the government starts asking · A · 1**
A cold **electric-blue** government-style corridor (archetypal, no seals/signs) with one distant door ajar
spilling hard light; the state beginning to look closely; no readable text, no real seal/logo; cinematic, austere,
deep perspective, negative space.

### ACT 3 — The Fall (~15:00–21:30)

**EP22-IMG-047 · act3: the thread that unravels · A · 1**
A single loose **gold** thread pulled from the dark weave of a pinstripe fabric, the weave beginning to come apart
into black; the one thread that undoes an empire; no text; cinematic macro, shallow focus, negative space.

**EP22-IMG-048 · act3: the informant turns · A · 1**
An anonymous suited silhouette (from behind, faceless) half-turning toward a cold **electric-blue** light, his
long shadow pointing toward a distant warm **gold** desk; a cornered man naming others; no face, no text;
cinematic, tense, negative space.

**EP22-IMG-049 · act3: the hidden room behind the door · A · 1**
The open **gold** vault door from Act 1, but now a second, darker doorway is just visible behind it in cold
shadow; the genius of the open door with a hidden room behind it; no text, no logo; cinematic, ominous, shallow
focus, negative space.

**EP22-IMG-050 · act3: two years of investigation · A · 1**
A dark wall densely strung with faint threads connecting blank cards and blank documents (no readable text), one
cold **electric-blue** lamp; one of the largest securities probes ever; no readable text, no faces; cinematic,
obsessive, negative space.

**EP22-IMG-051 · act3: the 98-count indictment · A · 1**
A single towering stack of plain documents rising into shadow on a courtroom-marble surface under hard
**electric-blue** light, faintly threatening; ninety-eight charges; no readable text/numbers, no seal; cinematic,
imposing, tall negative space.

**EP22-IMG-052 · act3: RICO — a mob law aimed at a financier · A · 1**
A long cold shadow in the shape of a looming statute/column falling across a pristine **gold**-lit pinstripe
sleeve at a desk; a racketeering law built for the mafia, now aimed at Beverly Hills; no text, no seal; cinematic
symbolic still, negative space.

**EP22-IMG-053 · act3: charges are not findings · A · 1**
A single document on a dark table, one half lit warm, one half cold, a faint balance scale reflected in its
surface, nothing resolved; accusations, not a verdict; no readable text; cinematic macro, shallow focus, negative
space.

**EP22-IMG-054 · act3: the pressure of the choice · A · 1**
A lone anonymous suited figure (from behind) seated small at the end of a vast cold **electric-blue** corridor of
shadow, one distant exit of warm light; decades of prison on one side, a plea on the other; no face, no text;
cinematic, oppressive scale, negative space.

**EP22-IMG-055 · act3: he pleaded guilty · A · 1**
An anonymous hand resting flat and still on a closed plain folder on a courtroom-marble table under one solemn
overhead light, deep shadow around; the decision not to fight; no face, no readable text, no seal; cinematic,
quiet, heavy, negative space.

**EP22-IMG-056 · act3: ninety-eight collapses to six · A · 1**
The towering document stack from IMG-051 dramatically reduced to a small, neat pile of just a few pages in a pool
of **gold** light, the rest dissolving into dark; 98 charges, six pleas, the rest dropped; no readable text/numbers;
cinematic symbolic still, negative space.

**EP22-IMG-057 · act3: what is NOT on the list · A · 1**
A short row of a few lit cards on dark marble, with two clearly empty/absent slots beside them rimmed in cold
**electric-blue**; no racketeering, no standalone insider-trading plea; strictly no readable text; clean cinematic
symbolic still, negative space.

**EP22-IMG-058 · act3: the record penalty · A · 1**
A heavy **gold** weight crashing down onto a dark scale, two distinct stacks of banded paper beneath it (one fine,
one a restitution fund) — about six hundred million; no readable numbers/text, no logo; cinematic, weighty,
negative space.

**EP22-IMG-059 · act3: the lifetime ban (padlock) · A · 1**
A single heavy brass padlock snapped shut on a cold steel barred gate, one **electric-blue** light, the warm
**gold** trading-floor glow locked away forever behind it; barred for life from his industry; no text, no logo;
cinematic macro, shallow focus, negative space.

**EP22-IMG-060 · act3: ten years, two served · A · 1**
The minimum-security prison-camp gate (from the hook) at grey dawn, a single anonymous figure (from behind, small)
walking back out toward warm light far sooner than expected; sentenced to ten, served about two; no face, no text,
no signage; cinematic wide still, negative space.

### ACT 4 — The Reckoning, and the Forgiveness (~21:30–27:30)

**EP22-IMG-061 · act4: a death sentence of a different kind · A · 1**
A lone hospital window at night, a faint **electric-blue** heartbeat line implied across the dark glass, a single
warm **gold** light far below in the city; advanced illness, a prognosis of months; no face, no readable monitors/
text; cinematic, fragile, negative space.

**EP22-IMG-062 · act4: turning the drive on the disease · A · 1**
An anonymous hand (only the hand) adjusting a brass microscope under a warm **gold** clinical light, soft research
ribbon shape suggested in the bokeh behind; the financier becoming a medical philanthropist; no readable text, no
logo; cinematic macro, shallow focus, negative space.

**EP22-IMG-063 · act4: the junk-bond insight, repeated · A · 1**
The "overlooked glowing page" motif reborn as a single bright **gold** petri dish / research vial in a dark lab no
one else funded; backing the written-off, now measured in years of life; no readable text; cinematic symbolic
still, negative space.

**EP22-IMG-064 · act4: both, at the same time · A · 1**
A single figure-shaped silhouette filled half with warm **gold** (philanthropist) and half with the cold record of
the felon, the seam glowing; the felon and the philanthropist are the same man; no face, no text; iconic cinematic
still, central negative space.

**EP22-IMG-065 · act4: the pardon · A · 1**
The cream parchment with the blank deep-red wax seal and ribbon (from the hook) now fully lit in warm **gold** on a
dark desk, a fountain pen resting beside it; a full presidential pardon; absolutely no readable text, no real seal/
crest; elegant cinematic macro, negative space.

**EP22-IMG-066 · act4: forgiveness is not innocence · A · 1**
The pardon parchment lit warm on the left, and on the right the same closed brass padlock (the SEC ban) still
locked in cold **electric-blue**, side by side on dark marble; forgiven by a president, still barred by the
regulators; no text, no seal/logo; cinematic symbolic still, balanced negative space.

**EP22-IMG-067 · act4: the roster of supporters · A · 1**
A dark hall lined with many faint anonymous silhouettes all turned toward one warm **gold** parchment glow at the
far end; powerful people who lobbied for years to clear his name; no faces, no text, no logo; cinematic, deep
perspective, negative space.

**EP22-IMG-068 · act4: the same act, read two ways · A · 1**
One single parchment on dark marble, lit warm **gold** from the left and cold **electric-blue** from the right at
once, casting two opposite-colored shadows; two opposite readings of the very same mercy; no readable text;
cinematic symbolic still, central negative space.

### ENDING — Your Verdict (~27:30–30:00)

**EP22-IMG-069 · ending: he won't fit the shape · A · 1**
A clean **gold** silhouette and a cold **electric-blue** silhouette of the same figure overlapping, refusing to
align into one; neither pure villain nor clean genius; no face, no text; iconic cinematic still, heavy negative
space.

**EP22-IMG-070 · ending: the builder and the convict · A · 1**
A single coin standing on edge on dark marble, one face catching warm **gold** (the builder), the other cold
**electric-blue** (the convict), a sharp shadow; you don't get to keep only the half you like; no readable
markings/text; cinematic macro, shallow focus, negative space.

**EP22-IMG-071 · ending: a lesson about us · A · 1**
A large ornate **gold** balance scale on dark marble, perfectly, uneasily level, one pan catching warm light and
one cold; how a society decides who is punished and who is forgiven; no text, no logo; cinematic symbolic still,
negative space.

**EP22-IMG-072 · ending: two endings stacked · A · 1**
A vertical diptych in one frame: warm **gold** above (fortune, comeback, pardon) and cold **electric-blue** below
(fine, ban, prison), the seam glowing; every part of the story has two endings at once; no readable text;
cinematic symbolic still, negative space.

**EP22-IMG-073 · ending: the verdict is yours · A · 1**
A single empty **gold**-rimmed chair (a juror's chair) facing the viewer in a dark, clean space, one warm light
above it, vast negative space; the verdict handed to you; no face, no text, no logo; cinematic, direct, resonant
negative space.

**EP22-IMG-074 · ending: the open question (final / CTA backdrop) · A · 1**
The split gold/blue figure from a respectful distance with a faint **gold** question-mark shape in the negative
space, composed with a large clean lower third and dark center so the dedicated Subscribe+Like CTA animation and
end-card read cleanly on top; minimal, resonant; no real YouTube logo, no readable text, no face; cinematic, heavy
negative space.

---

## 6. LOCAL SDXL FALLBACK (ONLY if a Codex generation is unavailable for a shot — Codex is PRIMARY)
- Model JuggernautXL; DPM++ 2M Karras, 32-40 steps, CFG 4.5-6.5; base 1344x768 -> upscale to long edge >= 3840;
  one locked seed family + per-scene offsets; same Hard Rules (no face/likeness, no real logo/seal, no readable
  text, no real artwork/landmark).

## 7. COVERAGE & HANDOFF NOTES
- 74 hero stills (EP22-IMG-001..074) cover hook + opening + 4 acts + ending, keyed to the 76 locked script spans.
  Generate EXACTLY ONE image per ID (74 total); select per the Quality Bar (§3) and Hard Rules (§0).
- All on-screen figures, names, dates, dollar amounts ($550M, ~$600M = $200M fine + $400M restitution), the
  "98 charged / 6 pleaded" graphic, the SUBSCRIBE/LIKE UI, map labels, and citations are **Remotion graphics/
  typography**, NOT baked into images.
- R3 reminder: a visible face/likeness of anyone, a real logo/seal (Drexel/SEC/DOJ/White House/YouTube/presidential),
  readable real text, a real artwork/landmark, or an authentic-looking record = automatic reject and regenerate.
- Register every selected still in the rights manifest (origin=Codex AI, license, verified_at), disclosed as AI
  symbolic reconstruction; no real-person likeness present.
