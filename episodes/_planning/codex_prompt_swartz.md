# CODEX HANDOFF — EP23 "The Internet's Own Boy" / Aaron Swartz (PD-2026-023-swartz)

> The single design document Codex reads to BUILD the episode. Claude owns the LEFT side
> (topic/research/claims/script) — done and LOCKED. Codex owns the RIGHT side
> (scenes -> images -> narration -> music -> motion -> edit -> render -> thumbnails).
> Build the FIRST render to satisfy the whole acceptance table. Numbers, not adjectives.

## 0. HARD CONSTRAINTS (do not cross)
- **R3 + SENSITIVE — death by suicide.** SAFE-HANDLING IS ABSOLUTE:
  - The death is stated in narration ONCE, with the locked wording ("died by suicide on January 11, 2013, at
    age 26"). NEVER add it anywhere else. NEVER "committed suicide." NO method, NO location, NO note, NO scene,
    NO reenactment in audio, caption, image, thumbnail, or metadata.
  - **NO single-cause narrative.** Do NOT state, in any caption / on-screen text / thumbnail / description, that
    the prosecution (or MIT, or any person) "caused" his death. Causation language belongs only to the family's
    attributed statement, exactly as written in the script. Foreground systemic issues, not one villain.
  - The **988 Suicide & Crisis Lifeline — call or text 988** lower-third appears on-screen at the marked beats
    and in the description (localize per region). The CTA is QUIET and respectful — this episode ends on a death.
- **No real-person likeness** anywhere — above all no likeness of Aaron Swartz, and none of any prosecutor,
  judge, official, or family member. People are anonymous (behind/cropped/silhouette/hands).
- **No real logos/seals/buildings** (Reddit, MIT, JSTOR, Creative Commons, YouTube, Wikipedia, DOJ/court seals,
  real Capitol/courthouse/MIT campus). Build archetypal equivalents. **No readable text** baked into any image.
- **No self-harm/death imagery** of any kind in any still or thumbnail (see 04_scenes §0). Symbolic only.
- WORDING LOCKS (must hold in every caption / on-screen text / thumbnail): co-authored RSS 1.0 as a teenager
  (NOT invented RSS); KEY COLLABORATOR on Markdown (NOT co-created); helped build the technical layer of
  Creative Commons (NOT founded); Reddit CO-OWNER via the Infogami merger (co-founder DISPUTED); he was CHARGED,
  never tried or convicted; JSTOR settled CIVILLY and did NOT want charges; MIT "neutral"; Carmen Ortiz's
  "Stealing is stealing..." is the prosecution's ATTRIBUTED position; "Aaron's Law" was proposed and NEVER
  passed; the CFAA was not meaningfully reformed.
- **THE "35 YEARS":** never show it unqualified. It is the THEORETICAL stacked statutory maximum, always paired
  on-screen and in narration with the ~6-month plea signal (per attorney Elliot Peters) and the scholarly
  critique (Orin Kerr) that the maximum wildly overstates realistic exposure.
- No publish, no external upload, no paid API beyond the narration cap without owner approval + idempotency +
  budget check. Render LOCAL CPU libx264, quality-first; NEVER NVENC. Heavy media ->
  H:\pd-media\episodes\PD-2026-023-swartz\ .

## 1. BINDING SPEC + ACCEPTANCE
- Canonical spec: **docs/PD_ONE_PASS_PRODUCTION_SPEC.v2.md** (binding). Build to rows 1-16.
- "Done" = the independent gate exits 0 (not your opinion):
  ```
  ./.venv/Scripts/python.exe scripts/check_final_acceptance.py 23 --json
  ```
- Duration profile: **mid, target ~30:00** (runtime band 27-33; narration ~28-29 min at the ElevenLabs pace).

## 2. LOCKED INPUTS (DO NOT REWRITE)
- Script: episodes/PD-2026-023-swartz/03_script/script.en.v001.md (~4,889 words; [VO:] only; "#" lines = production notes).
- Annotated: 03_script/script.annotated.v001.json (49 spans, 7 chapters, claim_ids + visual_intent).
- Claims (R3 wording + safe-handling locks): 01_research/claims.v001.json (18 claims). Sources: 01_research/sources.v001.json (14).
- Image library: 04_scenes/codex_image_prompts.v001.md (54 MEGA-PROMPTS; its Hard Rules / Style Bible /
  Universal Negative / Quality Bar are binding).

## 3. STRUCTURE & TIMING
- Hook ~0:00-0:08 fast symbolic flash-forward (EP23-IMG-001..006, ~1.3s cuts) -> rest of hook (the question) ->
  Opening (the gap, thesis + promise + the 988 content note) -> Body (Act 1 The Builder / Act 2 The Activist /
  Act 3 The Download / Act 4 The Weight) -> Ending (The Open Door) + the dedicated quiet Subscribe+Like CTA,
  per the script timecodes.
- Gold BrandOpening lands AFTER the hook (not frame 0); BrandEndcard at tail. OP/ED canonical =
  remotion/src/components/Bookends.tsx (OPENING_SEC 3.5 / ENDCARD_SEC 9; do NOT fork). Drive EP23 through
  CasePremiumFromRoughCut (register in Root.tsx if needed). The final endcard holds the 988 line + "In memory of
  Aaron Swartz, 1986-2013."

## 4. VOICE (row 2)
- ElevenLabs master, VOICE_ID nPczCjzI2devNBz1zQrb, eleven_multilingual_v2, stability 0.35, similarity 0.80,
  style 0, speaker_boost on. Speak ONLY [VO:] lines; ignore "#" lines; strip [CLM-xxxx]. SAPI/local FORBIDDEN in
  the final. Deliver the death line and the ending unhurried and gentle; do not dramatize.

## 5. CAPTIONS (rows 3-4)
- Force-align to the rendered ElevenLabs audio (verbatim). 1 cue = 1 breath group. <=2 lines, <=42 chars/line,
  1.0-6.0s, <=17 cps, >=2-frame gaps, brand font, bottom-safe (lower 10-15%, never centered/high), drop-shadow,
  coverage >=95%. The 988 lower-third must never be occluded by a caption at the marked beats.

## 6. MUSIC / BGM (row 1)
- Continuous library bed, one track per chapter. Duck under VO to an AUDIBLE FLOOR ~ -22 LUFS — the bed MUST
  stay audible under narration; never duck to silence. No silent stretch > 25s. Integrated -16..-12 LUFS. The
  ending track is restrained and warm, not maudlin; lift gently into the "and yet" hope beat (IMG-051..053).

## 7. IMAGES — Codex generation (row 5) — FULL PROMPTS INLINE IN **APPENDIX A** (below)
- This design doc is self-contained for image generation: the complete §0 Hard Rules, §1 Style Bible,
  §2 Universal Negative, §3 Quality Bar, §4 Scene Map, and all **54 MEGA-PROMPTS (EP23-IMG-001..054)** are
  written out in **Appendix A** at the end of this file. Generate straight from there; no other file needed.
  (Appendix A is the working copy; the canonical artifact is episodes/PD-2026-023-swartz/04_scenes/
  codex_image_prompts.v001.md — they are identical. If you ever change one, change both.)
- **Generate every numbered MEGA-PROMPT, exactly ONE image per prompt** (NO candidate pool); regenerate only a
  specific shot that fails Appendix A §0/§3. Output >= 3840 px long edge, 16:9; brand palette (black/navy +
  electric-blue #1F6BFF + gold #E5B53A + silver). Append Appendix A §2 Universal Negative to every generation.
- Reject any still with a face/likeness, ANY self-harm/death imagery, a real logo/seal/building, readable text,
  or anatomy errors. Register every used still in the rights manifest (origin=Codex AI, AI-disclosed, no-likeness).
- Output stills to H:\pd-media\episodes\PD-2026-023-swartz\05_visuals\selected\EP23-IMG-001.png … EP23-IMG-054.png.

## 8. MOTION / EDIT (row 8) — fixes weak animation / stutter / boring stills
- NO static image; NO frame held > 2s; NO naked hard cut. Ken Burns >= 6% / parallax on EVERY still; hero beats
  get SVD/organic motion + light/particle overlays (the feeds-of-light and locked-vs-open-archive motifs).
  Designed transitions 0.3-0.5s crossfade; OVERLAP Sequences by the transition length (no 1-frame black/jump);
  carry motion through the cut (no velocity reset = the "kaku"); Trail motion blur on fast moves (hook montage,
  the download streams). Average shot <= ~6s, but let the ending breathe (slower, longer holds, still <=2s freeze
  rule via slow continuous Ken Burns).
- Abundant material (row 7): factory shelf densely — >= 1 distinct clip per ~30s; every span >= 1 layer; no clip
  reused > 3x. scripts/select_factory_assets.py --theme tech/legal/crime/finance (use what fits a justice/tech
  elegy: servers, courtrooms-generic, libraries, code-abstract, city-night).

## 9. DEDICATED SUBSCRIBE+LIKE CTA (~29:20-29:50) — QUIET (ends on a death)
- Build exactly to the "# [PRODUCTION - DEDICATED SUBSCRIBE+LIKE CTA BEAT ...]" note in the script: gold
  SUBSCRIBE pill spring d14/s120 0.45s; gold underline wipe under "remembered" Easing.out(cubic) 0.5s; white
  LIKE thumb pop spring d10/s140, FILLS gold on the word "like" with a gentle 6% pulse + soft spark/Trail; soft
  navy vignette; hold ~5s; ease out 0.4s; very soft click SFX; music dips ~3 dB but the bed stays audible. NO
  real YouTube logo. Keep it understated and warm. Keep the 988 line present in the description card.

## 10. THUMBNAILS (rows 11-13) — loud but NEVER morbid or exploitative
- >= 3 variants as Remotion <Still> at 1280x720, backgrounds from the image library (locked vs open archive /
  open door / feeds-of-light — NO face, NO real logo/seal/building, NO self-harm/death imagery, NO readable
  baked text). "Loud" via contrast and a short UPPERCASE headline <= 3-4 words, gold #E5B53A or electric #1F6BFF
  accent, white/silver text, legible at 320px. Title <= 60 chars; A/B title x thumb. Headline ideas (respectful):
  "WHO OWNS KNOWLEDGE?" / "13 FELONIES" / "THE OPEN DOOR" / "HE TRIED TO FREE IT". AVOID anything that sensationalizes
  the death. Pick a selected; DO NOT upload.

## 11. RETENTION / LIKE-RATE (row 16) — engineered in the script
- Cold-open question ("who owns knowledge?" / "both true at once") is paid off in the Ending (the open door /
  "all of us"). Re-hooks ~every 2-3 min (the builder montage, the SOPA win, the closet, the "was this
  proportional?" turn). Earned, quiet Like ask in the CTA ("more people should sit with what happened"). Keep
  the edit tight so retention stays flat-to-rising; let only the ending slow down.

## 12. DEFINITION OF DONE (then STOP for owner)
- check_final_acceptance.py 23 exits 0; rows 4,5,7,8,11,12,13,15,16 measured -> 0 violations; check_dynamics.py
  and check_runtime_band.py on the render exit 0.
- First-cut -> title/thumbnail -> pre-publish review -> scheduling = owner gates, in order. Final-script approval
  APR-0001 is currently PENDING. Before publish, complete the DEDICATED R3 legal/rights + safe-handling review,
  compute durable source content_hash, re-verify facts, and confirm the safe-handling and 35-years locks hold in
  the rendered file. Do NOT treat the script as owner-approved until APR-0001 flips.

---

# APPENDIX A — IMAGE MEGA-PROMPT PACK (EP23-IMG-001..054) — generate straight from here

> One image per prompt (54 total). NO candidate pool. Regenerate only a shot that fails §A0/§A3.
> 16:9, long edge >= 3840 px. Remotion adds ALL text, the 988 lower-third, names/dates, and the bookends —
> never bake text into a still. Output -> H:\pd-media\episodes\PD-2026-023-swartz\05_visuals\selected\.

## A0. ABSOLUTE HARD RULES (R3 + SENSITIVE — apply to EVERY image)
1. **NO real-person face or likeness of anyone** — above all NO likeness of Aaron Swartz, and none of any
   prosecutor, judge, official, family member, or named figure. People are anonymous: from behind, cropped at
   the shoulders, silhouettes, hands only, far/out of focus. No look-alikes.
2. **NOTHING depicting self-harm, a method, a death scene, a body, a note, blood, a rope, pills, a window/ledge,
   or any reenactment of the death.** The death is handled by narration ONCE and a restrained memorial tone only.
   The ending imagery is hopeful-melancholy (an empty chair, a door ajar, light), never morbid.
3. **NO real logos, brands, seals, or identifiable buildings** — no Reddit, MIT, JSTOR, Creative Commons,
   YouTube, Wikipedia, US-government/DOJ seal, no real Capitol/courthouse/MIT campus. Build ARCHETYPAL generic
   equivalents (a generic dome-and-columns silhouette, an anonymous server hall, an unbranded library).
4. **NO readable text** inside the image — no letters, numbers, code that resolves, signs, logos, watermarks,
   readable documents or screens. Abstract glyph-like light only.
5. **Symbolic reconstruction only** — nothing looks like an authentic photo, news footage, or surveillance.
A face/likeness, any self-harm or death imagery, a real logo/seal/building, or readable text = automatic reject.

## A1. GLOBAL STYLE BIBLE
- **Genre:** museum-grade cinematic symbolic documentary; "prestige tech-tragedy / justice elegy."
- **Palette (PD brand, strict):** deep black + midnight-navy base; **electric blue `#1F6BFF`** = "open knowledge /
  network / cold institution"; **muted gold `#E5B53A`** = "human warmth / memory / the thing worth protecting";
  silver-grey highlights. Restrained filmic contrast. No candy neon, no teal-orange grade.
- **Light:** motivated, low-key — a single late desk lamp, one screen-glow on a shadowed face, cold server-hall
  rows, moonlight through tall windows, one warm picture-light. Real falloff, deep shadow, volumetric haze.
- **Texture:** worn desk wood, cool metal racks, cable, dust in a beam, old paper, rain on glass, fine grain.
  No plastic AI sheen, no waxy skin, no HDR halos.
- **Composition:** one clear subject; negative space for Remotion text and bottom-safe captions / the 988
  lower-third; strong fore/mid/background depth; works for slow push, parallax, or crop.
- **Output:** 16:9, long edge **>= 3840 px (3840x2160)**, highest quality; compose with upscale crop room.
- **Recurring motifs:** LOCKED ARCHIVE vs OPEN DOOR; rivers/feeds of light (knowledge moving freely); a single
  anonymous young figure at a glowing keyboard, always from behind or in shadow; a closed institutional corridor;
  stacked document-towers as a wall; an empty chair under warm light; a door left ajar with light beyond.

## A2. UNIVERSAL NEGATIVE (append to EVERY generation)
`face, facial features, eyes, portrait, recognizable person, celebrity, look-alike, real person likeness,
Aaron Swartz likeness, self-harm, suicide imagery, rope, noose, pills, blood, body, death scene, window ledge,
real logo, Reddit logo, MIT logo, JSTOR logo, Creative Commons logo, YouTube logo, Wikipedia logo, government
seal, court seal, real building, real Capitol, real courthouse, readable text, letters, numbers, real code,
signage, watermark, caption, distorted hands, extra fingers, mangled anatomy, plastic skin, waxy AI sheen,
overprocessed HDR, halo, cartoon, 3d render look, video-game look, neon candy colors, teal-orange grade,
cluttered frame, stock-photo lighting, fake documentary authenticity.`

## A3. QUALITY BAR (reject unless ALL pass)
Clear subject + negative space for text, mobile-readable at 320px · motivated controlled light, cinematic depth,
no flat stock look, no black crush · believable materials + grain, clean or no anatomy · narrative duty: locate /
explain / build tension / symbolize the exact beat · safety: no face/likeness, no self-harm-death imagery, no
real logo/seal/building, no readable text, not authentic-looking · editability: parallax/Ken-Burns friendly,
crop room, doesn't fight captions or the 988 lower-third · neighbor fit: distinct from adjacent shots; the ending
stills read restrained, not morbid.

## A4. SCENE MAP (54 hero stills)
HOOK montage 001..006 · HOOK beats 007..009 · OPENING 010..012 · ACT1 (builder) 013..020 · ACT2 (activist)
021..026 · ACT3 (the download) 027..034 · ACT4 (the weight) 035..042 · ENDING (the open door) 043..054.

## A5. MEGA-PROMPTS

### HOOK (~0:00–1:30) — fast 8s symbolic flash-forward, then the question

**EP23-IMG-001 · hook: the locked archive**
A vast dark library/server hall seen as an endless wall of faintly glowing knowledge boxes, every one sealed
behind a cold **electric-blue** padlock-shape of light, receding into **navy** black; one warm **gold** spark
trapped behind the glass; awe and confinement at once; no real logos, no text; cinematic wide, deep perspective,
35mm grain, negative space top for headline.

**EP23-IMG-002 · hook: the blinking cursor**
Extreme dark close-up of a single blinking cursor-block of soft **electric-blue** light hovering in a black void,
a faint **gold** reflection beneath it, dust motes drifting; the smallest possible spark of a human will; no
letters, no readable code, no text; cinematic macro, shallow depth, grain.

**EP23-IMG-003 · hook: the empty courtroom bench**
An archetypal, generic courtroom rendered in shadow — a single empty wooden bench/seat under one cold shaft of
**electric-blue** window light, vast dark panelled emptiness around it (NOT a real courthouse, no seal, no
flag); quiet dread; no people, no text, no seal; cinematic, low angle, heavy negative space.

**EP23-IMG-004 · hook: the late desk lamp**
A lone desk lamp burning warm **gold** in a dark room, pooling light on a worn wooden desk with an out-of-focus
glowing screen edge; a young person's silhouette implied only by an empty chair pushed back; lonely, human,
late; no face, no readable screen, no text; cinematic, warm-vs-navy, soft grain.

**EP23-IMG-005 · hook: feeds of light set free**
Abstract rivers of small **gold** and **electric-blue** light-particles streaming upward and outward from an
opening dark box, like knowledge escaping into the air; motion-blur trails for speed; hopeful, fast; no text,
no logos; cinematic, dynamic diagonal, deep black background for a headline.

**EP23-IMG-006 · hook: the weight closing in**
Towers of dark, featureless document-stacks rising like canyon walls around one tiny warm **gold** point of
light at the bottom, cold **electric-blue** rim light along the edges; scale and pressure; no text, no readable
pages; cinematic, oppressive verticals, grain, negative space center.

**EP23-IMG-007 · hook: who owns knowledge**
A single ornate **gold** key-shape of light hovering before an enormous dark locked door inlaid with faint
**electric-blue** circuitry-like filigree (abstract, unreadable); the central question made visual; no text, no
real seal; cinematic, centered, reverent, heavy negative space.

**EP23-IMG-008 · hook: the suburban Chicago boy (anonymous)**
A small anonymous child-sized silhouette from behind, sitting cross-legged in the warm **gold** glow of an old
boxy monitor in a dim suburban bedroom, curtains drawn against afternoon light, a galaxy of dust in the beam;
tender, solitary genius; no face, no readable screen, no text; cinematic, behind-the-shoulder, soft grain.

**EP23-IMG-009 · hook: a name you have touched**
Abstract: countless tiny warm **gold** dots (people/devices) all faintly connected by thin **electric-blue**
threads to one slightly brighter origin point off-center; the quiet ubiquity of one person's work; no text, no
faces; cinematic, dark field, parallax-friendly, negative space.

### OPENING (~1:30–3:30) — The Gap

**EP23-IMG-010 · opening: the gap between two worlds**
A single composition split by a dark vertical chasm: on one side warm **gold** open shelves spilling light, on
the other a cold **electric-blue** institutional corridor of identical closed doors; a thin figure-shadow stands
at the edge of the gap, from behind; the law vs its purpose; no text, no logos; cinematic, symmetrical, depth.

**EP23-IMG-011 · opening: the builder and the defendant**
One anonymous young silhouette reflected twice in a dark glass — on the left lit warm **gold** at a glowing
keyboard, on the right lit cold **electric-blue** standing alone in an empty institutional hall; same person,
two fates; no face, no text; cinematic, mirrored, shallow depth, grain.

**EP23-IMG-012 · opening: a calm hand of help (988 beat)**
A very quiet, warm still: two open, anonymous hands cupped around a small steady **gold** flame of light in deep
**navy** darkness, calm and protective, lots of empty bottom space for the 988 lower-third; reassurance, not
alarm; no faces, no text; cinematic macro, soft warm light, gentle grain.

### ACT 1 (~3:30–9:30) — The Boy Who Wanted To Give It Away

**EP23-IMG-013 · act1: born into the early web**
A dim 1990s suburban room at dawn, an old boxy computer waking with a soft **electric-blue** glow, a child-sized
empty chair before it, warm **gold** sunrise edging the curtain; the world coming online; no face, no readable
screen, no text; cinematic, quiet, deep depth, grain.

**EP23-IMG-014 · act1: fourteen at the engineers' table**
A dark conference table ringed by tall adult silhouettes (faceless, from behind), and one much smaller silhouette
among them lit warm **gold** by a laptop; a child treated as an equal; abstract **electric-blue** feed-streams
rise from the small laptop; no faces, no logos, no text; cinematic, low angle, depth.

**EP23-IMG-015 · act1: RSS — the web syndicating itself**
Abstract hero: a hundred dark distant windows of light all sending thin **electric-blue** ribbons of data toward
one gathering point that glows warm **gold**; the invisible machinery of feeds; fast, elegant, motion-blur
trails; no text, no logos; cinematic, dynamic, deep black, negative space.

**EP23-IMG-016 · act1: Markdown — plain human writing**
Macro of a worn keyboard in warm **gold** lamp light, a few soft **electric-blue** symbol-glyphs (abstract,
unreadable) lifting off the keys and turning into clean ribbons of formatted light; tools that belong to
ordinary people; no readable text, no logos; cinematic, shallow depth, tactile, grain.

**EP23-IMG-017 · act1: Creative Commons — machinery for sharing**
A symbolic open hand releasing a small glowing **gold** object that splits into many copies streaming out on
**electric-blue** light to distant dark hands; giving work away on purpose; NO real CC logo (use an abstract
open-circle-of-light motif instead); no text; cinematic, generous gesture, depth, negative space.

**EP23-IMG-018 · act1: the merger into a giant (Reddit, symbolic)**
Two small glowing **gold** orbs merging into one, which then blooms into a vast dark constellation of countless
faint blue points (a huge community), one young silhouette watching from the foreground, from behind; growth he
didn't chase; NO real logo, no text; cinematic, scale, parallax-friendly.

**EP23-IMG-019 · act1: money never the point**
A dim desk where a loose scatter of abstract **gold** value-tokens (unbranded coins of light) sits ignored and
dusty, while the same warm light is turned instead toward an open glowing book; values made visual; no faces,
no text, no real currency; cinematic still-life, warm-vs-navy, grain.

**EP23-IMG-020 · act1: the believer (manifesto)**
A young anonymous figure from behind, haloed by the warm **gold** glow of a single screen in a dark room, one
fist resting on the desk with quiet conviction; abstract **electric-blue** sparks of ideas rising; principled,
not zealous; no face, no readable screen, no text; cinematic, behind-the-shoulder, grain, negative space.

### ACT 2 (~9:30–15:00) — The Man Who Learned He Could Win

**EP23-IMG-021 · act2: freeing public records**
A symbolic dark vault of identical locked drawers glowing cold **electric-blue**, one drawer sliding open to
release a warm **gold** stream of documents-as-light into open air; public files set free; NO real seal, no
text; cinematic, depth, parallax-friendly, negative space.

**EP23-IMG-022 · act2: code is law**
An archetypal, generic legislative dome-and-columns silhouette (NOT the real Capitol) rendered as cold **navy**
stone, with thin **electric-blue** circuit-lines tracing through it like veins; the realization that law is the
real code; no flag, no seal, no text; cinematic, monumental, low angle, haze.

**EP23-IMG-023 · act2: the quiet bill almost passes**
A vast dim chamber of empty identical seats (generic, not real) with a single cold **electric-blue** spotlight
on a distant podium-shape, almost no one watching; danger moving in silence; no people's faces, no seal, no
text; cinematic, wide, lonely, deep perspective.

**EP23-IMG-024 · act2: the coalition wakes up**
A dark map-like field where thousands of tiny **gold** points of light ignite in a spreading wave and connect
with **electric-blue** threads into one growing network; ordinary people mobilizing; fast, hopeful, motion
trails; no real borders/labels, no text; cinematic, dynamic, negative space.

**EP23-IMG-025 · act2: the blackout day**
A grid of many dark screens/windows all going BLACK in unison across a city-of-light, leaving one defiant warm
**gold** glow; the internet protesting; symbolic, no real logos or sites, no readable text; cinematic, graphic,
high-contrast navy-and-gold, parallax-friendly.

**EP23-IMG-026 · act2: he learned he could win**
An anonymous lone silhouette from behind, small against a huge dark hall, lifting a hand as a wave of warm
**gold** light rises to meet it; improbable victory; quiet triumph, not bombast; no face, no text, no logos;
cinematic, scale, backlight, grain, negative space top.

### ACT 3 (~15:00–20:30) — The Download

**EP23-IMG-027 · act3: a closet and a library**
A cramped dark basement wiring closet, racks of cool **electric-blue** server light, one anonymous laptop glow
warm **gold** on the floor, cables everywhere; intimate and clandestine but ordinary; no face, no readable
screen, no logos, no text; cinematic, claustrophobic depth, grain.

**EP23-IMG-028 · act3: what JSTOR is**
An immense dark archive of glowing journal-shapes stretching to vanishing point, each sealed behind a faint
cold **electric-blue** paywall-glass; scholarship locked away; NO real JSTOR branding, no readable text;
cinematic, deep one-point perspective, awe, negative space.

**EP23-IMG-029 · act3: the public pays twice**
A symbolic scale/turnstile of light where the same warm **gold** coin must pass twice through a cold
**electric-blue** gate to reach a single glowing paper; the double toll on public knowledge; no real currency,
no text, no logos; cinematic, clean graphic still, depth.

**EP23-IMG-030 · act3: an open network**
An archetypal university quad at night (generic, NOT real MIT), warm **gold** windows and one open archway
glowing invitingly, a faint **electric-blue** mesh of an open wireless network drawn in light over it; openness
by design; no real building, no logo, no text; cinematic, wide, atmospheric haze, negative space.

**EP23-IMG-031 · act3: the download begins**
A single warm **gold** laptop in the dark pulling a torrent of small **electric-blue** article-cards toward it
in fast motion-blur streaks, the cards stacking onto a glowing drive; relentless, automatic; no face, no
readable text, no logos; cinematic, dynamic diagonal, trail blur, grain.

**EP23-IMG-032 · act3: most of a library, copied**
A hard-drive-shaped vessel of light slowly filling with a galaxy of millions of tiny **electric-blue** points
while a few warm **gold** ones glow through; the staggering scale of 4.8 million; abstract, no text, no logos;
cinematic, macro-to-cosmic, negative space, parallax-friendly.

**EP23-IMG-033 · act3: noticed, and it stops**
The same closet now still and cooling, the laptop glow fading to a last warm **gold** ember, the **electric-blue**
server light steady again; the quiet after; no face, no text, no logos; cinematic, calm, shallow depth, grain.

**EP23-IMG-034 · act3: the victim walks away**
Two abstract glowing hands lowering a cold **electric-blue** sword/shield of light and turning away from a small
warm **gold** figure-spark; a settlement, a stepping-back; symbolic reconciliation; no faces, no text, no logos;
cinematic, restrained, negative space.

### ACT 4 (~20:30–27:00) — The Weight

**EP23-IMG-035 · act4: the charges**
A towering cold **electric-blue** wall of identical dark document-slabs slamming into place around a tiny warm
**gold** light at its base; the indictment as a closing wall; no readable text, no seal, no logos; cinematic,
oppressive scale, low angle, grain, negative space.

**EP23-IMG-036 · act4: an old, sweeping law**
A massive aged stone statute-block, cracked and cold, lit hard from one side in **electric-blue**, its surface
covered in abstract unreadable engraving-light; a 1980s law stretched too far; NO readable text, no seal;
cinematic, monumental still, heavy shadow, depth.

**EP23-IMG-037 · act4: the prosecutor's framing (attributed)**
A symbolic balance: on one pan a glowing **gold** open book, on the other a cold **electric-blue** crowbar-shape
of light, the scale tilting hard toward the crowbar; "stealing is stealing" made visual as a contested equation;
no face, no text, no logos; cinematic, clean graphic, negative space.

**EP23-IMG-038 · act4: four counts become thirteen**
A small cluster of four cold **electric-blue** light-shards multiplying into thirteen, hardening into a denser
cage around one warm **gold** point; escalation; abstract, no numbers rendered as readable text; cinematic,
dynamic, grain, negative space.

**EP23-IMG-039 · act4: the misleading number**
A huge cold **electric-blue** looming shadow-number shape (deliberately blurred/unreadable, NOT legible) cast
over a tiny warm **gold** figure-spark, while behind it a much smaller true shape hides; a frightening headline
that overstates reality; NO readable digits, no text; cinematic, forced perspective, negative space.

**EP23-IMG-040 · act4: he would not say the word**
An anonymous young silhouette from behind, standing very still before a cold **electric-blue** institutional
doorway, refusing to step through; a warm **gold** rim holds along his shoulders; principled refusal; no face,
no text, no logos; cinematic, backlit, quiet tension, negative space.

**EP23-IMG-041 · act4: the process as punishment**
A lone warm **gold** desk lamp and an empty chair in a dark room slowly being crowded by cold **electric-blue**
stacks of paperwork and long thin clock-shadows; years eaten by waiting; no face, no readable text; cinematic,
melancholy still-life, deep navy, grain.

**EP23-IMG-042 · act4: was this proportional?**
A stark symbolic still: an enormous cold **electric-blue** institutional weight/anvil of light suspended over a
single small warm **gold** open book on a bare floor; the question of proportion in one frame; no text, no
seal, no logos; cinematic, high contrast, lots of empty space, parallax-friendly.

### ENDING (~27:00–30:00) — The Open Door (restrained, never morbid)

**EP23-IMG-043 · ending: the empty chair (memorial, not morbid)**
A single empty wooden chair beside a quiet desk, bathed in soft warm **gold** light in a calm **navy** room, a
faint **electric-blue** dawn at the window; absence held with dignity and gentleness; NO body, no death imagery,
no text; cinematic, restrained, soft grain, generous negative space.

**EP23-IMG-044 · ending: leave it there, gently (988 beat)**
A very calm wide still: a still dark room with one steady warm **gold** light and a large empty lower third of
soft **navy** for the 988 lower-third; tender, safe, unhurried; no faces, no death imagery, no text; cinematic,
quiet, minimal, bottom negative space.

**EP23-IMG-045 · ending: the family's words (attributed)**
A symbolic huddle of a few anonymous warm **gold** silhouettes (from behind, close together) facing a cold
**electric-blue** institutional facade across an empty plaza; grief facing the system; no faces, no real
building, no seal, no text; cinematic, wide, restrained, depth.

**EP23-IMG-046 · ending: no single cause**
An abstract still of many faint converging **electric-blue** threads passing through a single soft **gold**
point and continuing on — no one thread brighter than the rest; the truth that a life has no single cause;
contemplative, no faces, no text; cinematic, delicate, negative space.

**EP23-IMG-047 · ending: a friend asks if it was proportional (Lessig, attributed)**
A lone anonymous figure-silhouette standing at a lectern-shape of warm **gold** light addressing a dark empty
hall lit cold **electric-blue**; a principled public question; no face, no real seal/room, no text; cinematic,
backlit, solemn, negative space.

**EP23-IMG-048 · ending: the institution looks at itself**
A cold **electric-blue** mirror-like glass facade of a generic institution reflecting a single small warm
**gold** light back at itself; self-examination, "missed an opportunity," the rejected word "neutral"; NO real
building, no logo, no text; cinematic, reflective, restrained, depth.

**EP23-IMG-049 · ending: a law named for him**
A single warm **gold** candle-flame of light placed before a vast cold **electric-blue** stone statute-wall, a
small bright hope set against an immovable mass; a reform bill offered up; NO readable text, no seal; cinematic,
intimate-vs-monumental, negative space.

**EP23-IMG-050 · ending: it never passed**
The same generic stone statute-wall, unchanged and cold **electric-blue**, the small **gold** flame from the
prior shot now guttered to a thin wisp of smoke; the door still shut; melancholy but NOT morbid (no death
imagery); no text, no seal; cinematic, still, deep shadow, negative space.

**EP23-IMG-051 · ending: and yet — the world he wanted, partly here**
A dark archive wall like IMG-001, but now many of the locked boxes stand OPEN, warm **gold** light spilling
freely out of them into the air; quiet, earned hope; the locks defeated one by one; no text, no logos;
cinematic, luminous, deep perspective, negative space top.

**EP23-IMG-052 · ending: who owns knowledge — all of us**
A wide field of countless anonymous warm **gold** hands (from behind/below, no faces) all reaching up toward a
shared rising sphere of open **electric-blue**-and-gold light; collective ownership of knowledge; no text, no
logos; cinematic, uplifting, symmetrical, parallax-friendly.

**EP23-IMG-053 · ending: the open door (payoff of the hook)**
The enormous dark locked door from IMG-007, now standing AJAR, a warm **gold** wedge of light pouring through
into the black foreground; the door he died trying to open, finally open in spirit; reverent, hopeful; no text,
no seal; cinematic, centered, glowing, heavy negative space.

**EP23-IMG-054 · ending: in memory (endcard plate, restrained)**
A calm near-black plate with a single soft **gold** point of light high and a wide clean **navy** lower area for
the Remotion endcard text / 988 line / "In memory" dedication; dignified, minimal, never morbid; no faces, no
text baked in; cinematic, quiet, maximal negative space for overlays.

## A6. USAGE NOTES
- Generate EP23-IMG-001..054 once each (54 stills), long edge >= 3840 px, 16:9. Register every used still in the
  rights manifest as origin=Codex AI generation (AI-disclosed), no real-person likeness, no real logo/seal.
- Reuse motifs for payoff: IMG-001 -> IMG-051 (locked vs freed archive); IMG-007 -> IMG-053 (locked -> open
  door); IMG-012 / 044 / 054 reserve clean bottom space for the 988 lower-third.
- Re-generate ONLY a specific failed shot against §A0/§A3. Do NOT build a candidate pool.
- All on-screen text, the 988 lower-third, names, dates, the dedication, and the bookends are added in Remotion,
  never baked into the still.
