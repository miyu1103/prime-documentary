# Master materials list — PD-2026-002-gideon (v001)

**Purpose:** the single "gather everything before we assemble" sheet (owner request, 2026-06-16).
Derived from the locked script (APR-0001) + `scene_plan.v001.json` (28 scenes) +
`voice_plan.v001.json` (28 chunks). Real-first per decisions/0002 §L; AI stays clearly symbolic
(invariant 11); every real asset gets a `rights_basis` in the rights manifest before publish (§N gate).

**Rule:** assembly does NOT start until every item in §2 (owner-manual) is delivered and §1 (auto) is
generated. One assembly pass (EP1 lesson: no 13× re-cuts).

---

## 0. Who does what (summary)

| Track | Who | Tool | Owner action? |
|---|---|---|---|
| Narration (28 chunks, 抑揚) | **me** | ElevenLabs (Brian) | none |
| SFX (60–100) | **me** | library + ElevenLabs | none |
| Ambience (100%) | **me** | library + ElevenLabs | none |
| Captions (frame-synced) | **me** | TTS timestamps | none |
| Remotion graphics (titles/diagrams/maps/dataviz/callouts/endcard) | **me** | Remotion | none |
| Real public-domain assets (petition, audio, portraits, Constitution, B-roll) | **me** | auto-download + rights record | none (confirm portraits) |
| **Episode still images (symbolic reenactment)** | **owner** | **Midjourney** | **YES — ~18 images** |
| **Hero motion clips** | **owner** | **Runway** (or MJ-animate) | **YES — ~8 clips** |
| **Music tracks (BGM)** | **owner** | **Suno** (reuse library first) | **YES — ~6 cues** |
| Approvals (title/thumbnail; first-cut; publish) | **owner** | — | **YES — 3 gates left** |

---

## 1. AUTOMATIC — I produce these (no owner action)

### 1a. Narration — ElevenLabs, voice Brian `nPczCjzI2devNBz1zQrb`, `eleven_multilingual_v2`
- 28 chunks from `voice_plan.v001.json`, each tagged **calm / building / intense** for expressiveness.
- Pronunciation locked: Gideon, Wainwright, Betts v. Brady, Abe Fortas, Hugo Black.
- In-plan cost (no overage expected). Output → SSD `06_voice/`.

### 1b. SFX — reuse the 22-item library; generate extras via ElevenLabs as needed
- Needed kinds: riser, impact/boom, gavel (x3), pencil-scratch, paper/stack, stone-thud, stone-crumble,
  heartbeat, low-drone, sweep, soft-swell, text-reveal ticks. **Floor: 60–100 SFX placements.**

### 1c. Ambience — continuous, never silent (4-layer audio)
- prison cell tone, courtroom tone, public-defender office tone, neutral room-tone. **100% coverage.**

### 1d. Captions — open captions, brand font, word-for-word the narration, frame-accurate from TTS
  timestamps (NO hand-timing — EP1 lesson). Lower safe-area, 1–2 lines, 5–8 words.

### 1e. Remotion graphics (all `REM-*` assets in the scene plan)
- Kinetic titles & payoff lines, the prosecutor-vs-Gideon imbalance diagram, scales tilt, the
  "Betts wall" motif (build + crumble), the cert-funnel & caseload **data-viz**, the 6th→14th map &
  state-spread map, split-screen "alone vs lawyer", arrows (Gideon→Miranda), callouts/underlines,
  brand end-card + next-episode tease. Reuse EP1 components (`KineticType`, `DiagramFlow`, `SceneArt`,
  `Motion`, brand).

### 1f. Real public-domain assets — I auto-source + record rights (real-first)
| ID | Asset | Source (candidate) | Rights basis | Note |
|---|---|---|---|---|
| PD-petition | **Gideon's actual handwritten petition** | National Archives (NARA) | public_domain (federal record) | Strong real hero asset — use in S009/S010 |
| PD-oral-audio | **Oral-argument audio, Jan 1963** | NARA / archive.org | public_domain (US gov) | Short underlay under S013/S015; avoid CC-NC copies |
| PD-black | Justice Hugo Black portrait | LOC / Wikimedia | public_domain (US gov) | **confirm PD tag** or fall back to MJ symbolic (S015) |
| PD-fortas | Abe Fortas portrait | LOC / Wikimedia | public_domain (US gov) | **confirm PD tag** or fall back to MJ symbolic (S013) |
| PD-constitution | 6th Amendment / Bill of Rights | NARA | public_domain | S016 |
| PD-scotus | SCOTUS exterior + chamber | **reuse from EP1** (`remotion/public/mj/`) | MJ commercial (owner) | S001/S015 |
| PD-courtroom-broll | 1960s courtroom B-roll | Prelinger / Universal Newsreel | public_domain | verify each clip; S004/S007/S020 lead-ins |
| PD-prison-broll | 1960s prison/cell B-roll | Prelinger | public_domain | verify; S002/S009 lead-ins |

> Portraits (Black, Fortas): if PD cannot be confirmed, the scene plan already has MJ symbolic
> fallbacks (no real-likeness issues, invariant 11) — same problem EP1 hit; we will not ship an
> unverified portrait.

---

## 2. OWNER MANUAL — please generate these (the "your hand" list)

### 2a. Midjourney still images — ~18 (brand `--sref`, 16:9, symbolic, NO on-image text)
Generate primary + 1–2 variants each; drop into `remotion/public/mj/`. Prompts are drafts — tweak freely.

| # | Scene | File stem | Prompt (draft) |
|---|---|---|---|
| 1 | S002 | s002_prison_cell | lone man sitting on a bunk in a stark 1960s American prison cell, dim window light, contemplative, cinematic, muted palette, no text --ar 16:9 |
| 2 | S002 | s002_courtroom_request | a poor defendant standing alone before a judge's bench in a 1960s courtroom, asking for help, dramatic side light, no readable text --ar 16:9 |
| 3 | S003 | s003_lone_defendant | a single small figure at a defense table dwarfed by an empty formal courtroom, isolation, cold cinematic light --ar 16:9 |
| 4 | S004 | s004_poolroom | exterior of a small-town Florida poolroom at night, 1961, neon glow, rain-slick street, cinematic, no text --ar 16:9 |
| 5 | S004 | s004_courtroom_1961 | wide 1961 Florida courtroom, wood panelling, jury box, warm institutional light, period-accurate, no text --ar 16:9 |
| 6 | S005 | s005_empty_chair | a single empty wooden chair at a defense table, one hard shaft of cold light, deep shadow, symbolic, cinematic --ar 16:9 |
| 7 | S007 | s007_gideon_defending | a lone middle-aged man in plain clothes standing to address an unseen jury, vulnerable, 1960s courtroom, no text --ar 16:9 |
| 8 | S008/S001 | s008_pencil_closeup | extreme close-up of a worn yellow pencil tip on lined prison paper, shallow depth of field, dramatic light --ar 16:9 |
| 9 | S009 | s009_hand_writing | close-up of a weathered hand carefully hand-printing a letter with a pencil on lined paper, prison cell, warm lamp, no readable text --ar 16:9 |
| 10 | S010 | s010_petition_document | an old hand-written legal petition on lined paper, aged, on a wooden table, shallow focus, no legible text --ar 16:9 |
| 11 | S011 | s011_1942_court | a heavy stone wall motif merged with a dim 1940s Supreme Court interior, oppressive, symbolic obstacle, cold light --ar 16:9 |
| 12 | S013 | s013_fortas_symbolic | dignified silhouette of a 1960s attorney in a suit entering a marble corridor, back-lit, no identifiable face, symbolic --ar 16:9 (fallback if no PD Fortas portrait) |
| 13 | S014 | s014_crowd_silhouettes | many anonymous defendant silhouettes standing in rows, vast, symbolic of every poor defendant, cold palette --ar 16:9 |
| 14 | S015 | s015_scotus_chamber | the interior of the US Supreme Court chamber, empty, dramatic light through high windows, reverent, no text --ar 16:9 (or reuse EP1) |
| 15 | S020 | s020_retrial_filled_chair | a 1963 courtroom defense table where two figures now sit side by side (defendant + lawyer), warmer light, hopeful, no text --ar 16:9 |
| 16 | S021 | s021_defense_attorney | a sharp 1960s defense attorney mid-cross-examination, confident, courtroom, dramatic light, no text --ar 16:9 |
| 17 | S023 | s023_public_defender_office | a modern public defender's office, stacks of case files, fluorescent light, busy, documentary feel, no text --ar 16:9 |
| 18 | S024/S027 | s024_overloaded_desk | a single desk buried under towering stacks of case folders, one tired lamp, symbolic overload, cinematic --ar 16:9 |

Plus the **2 thumbnail backgrounds** (from `09_package/packaging_concept.v001.md`): Concept 2 (pencil +
blurred SCOTUS) and Concept 3 (lone man in immense courthouse).

### 2b. Runway hero motion clips — ~8 (3–6s each, from the MJ stills above or fresh)
Floor: **≥6–10 motion clips.** Brief = subtle, purposeful motion (no gimmicks).

| # | Scene | Clip | Motion brief |
|---|---|---|---|
| 1 | S002 | cell_pushin | slow push-in on the man in the cell, faint dust in light |
| 2 | S005 | chair_light | the shaft of light slowly intensifies on the empty chair |
| 3 | S007 | verdict | subtle rack-focus / slow zoom as the verdict lands |
| 4 | S009 | writing_motion | the hand actually writing, pencil moving across the page |
| 5 | S013 | fortas_walk | the attorney silhouette walking down the marble corridor |
| 6 | S019 | letter_drift | breathing slow drift over the letter on the desk |
| 7 | S020 | retrial_pan | gentle pan across the now-filled defense table |
| 8 | S026 | letter_mailbox | the letter sliding into a mailbox / drifting away, symbolic |

### 2c. Suno music — ~6 cues (REUSE the 21-track library first; only generate gaps)
Master −14 LUFS; bed −18…−22 LUFS, ducked under VO. Briefs:

| Cue | Scenes | Mood brief |
|---|---|---|
| hook_bed | S001–S002 | tense, sparse, curious; quick hook energy |
| opening_bed | S003–S005 | restrained, reflective, "something you assumed is wrong" |
| tension_build | S006–S012 | rising unease; the wall (Betts); long-odds |
| reveal_triumph | S013–S018 | turn + payoff; the unanimous ruling lands (swell) |
| expansion_then_strain | S020–S024 | hopeful expansion → subtle unresolved tension (underfunding) |
| outro | S025–S028 | warm, resolved, forward-looking; brand outro |

---

## 3. Abundance-floor check (decisions/0004 §E2, per 12 min)
| Floor | Target | This plan |
|---|---|---|
| Real-asset inserts | ≥8–12 | 8 real pools (petition, audio, 2 portraits, Constitution, SCOTUS, courtroom & prison B-roll) ✓ |
| AI motion clips | ≥6–10 | 8 Runway clips (§2b) ✓ |
| SFX placements | 60–100 | planned across 28 scenes ✓ |
| Ambience | 100% | 4 ambience beds, continuous ✓ |
| Shots / cuts | 90–150 | 28 scenes × multiple shots (stills + motion + graphics) → target ~110 ✓ |
| Flash-forward hook | 5–8s | S001 = ~9s (trim to 8) ✓ |

## 4. Reuse from EP1 (don't rebuild)
SCOTUS exterior/chamber MJ stills · music (21) + SFX (22) + ambience library · Remotion components
(`KineticType`, `DiagramFlow`, `SceneArt`, `Motion`, `ColdOpen`, brand, `ThumbConcept`).

## 5. Gate before assembly (all must be true)
- [ ] §2a Midjourney stills delivered (~18 + 2 thumbnail bg)
- [ ] §2b Runway clips delivered (~8)
- [ ] §2c Music cues chosen/generated (~6; reuse where possible)
- [ ] §1f real PD assets sourced + rights recorded (portraits confirmed or MJ fallback)
- [ ] Title/thumbnail APR (after thumbnails rendered)
- [ ] Then: I assemble in one pass → first-cut APR → QC + rights manifest → publish gate
