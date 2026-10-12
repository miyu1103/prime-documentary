# PD ONE-PASS PRODUCTION SPEC & ACCEPTANCE CONTRACT (v3)

**Authored 2026-08-20. Supersedes v2 for all episodes from EP72 onward.** `PD_ONE_PASS_PRODUCTION_SPEC.v2.md`
stays on disk unedited: EP62–EP71 were built against it and their receipts must remain readable
(`.claude/rules/12`). Where v2 and this file disagree, **this file governs from EP72**.

## THE ONE RULE

> A film is done when an **independent script** measures the **real rendered file** and says so.
> Self-certification is not evidence. `skipped` is not a pass.

Final gate:

```
py -3.11 scripts/check_final_acceptance.py <slug|NN> --render <final.mp4> --emit-receipt
```

---

## 0. What v3 changes, and the measurement behind each change

v2 described the gate in prose that had drifted from the code. Everything below was measured on
2026-08-20 from the receipts themselves (`episodes/*/09_package/acceptance_receipt.v*.json`,
newest per episode, n = 32) rather than read from a document.

| # | v2 said | measurement | v3 says |
|---|---|---|---|
| 1 | "check_final_acceptance machine-enforces rows 1,2,3,4,6,8,9,11 … still manual: 13, 15" | The current receipt carries **48 checks**; **50** distinct ids have appeared across 32 episodes. Rows 13 and 15 are no longer manual — `packaging_qc` and `script_craft` run. | §2 carries the full inventory, taken from a receipt, not from prose. |
| 2 | Row 9: hook **voiced from 0:00, written FIRST**; §B.1: hook "written **last**" | Both sentences are in v2. Row 9 carries an owner decision dated 2026-08-10 and binds from EP66; §B.1 is the pre-EP66 text left in place. | **Hook is written FIRST and voiced from 0:00.** §B.1's "written last" is deleted. |
| 3 | Row 13: "Packaging gate: title 59–100 chars" — while the same row's own header still carried "title ≤60" from v1 | PD's CTR under the ≤60 rule is 1.38%; the measured comparator's titles are all 59–100 and its shortest title is its worst performer. | **59–100 characters, third person, no question form.** The ≤60 text is deleted. |
| 4 | `audio_layers` default **2** (`PD_EPISODE_SPEC_STANDARD.v001`) | EP71 declares **4** and the finisher builds a four-layer mix; `sound_layers` passes 11 and fails 17 across 32 episodes. | Declare **4**. The standard's default of 2 is the historical artefact, and §6.4 records the contradiction as a real bug to close. |
| 5 | Every acceptance check read as a ship blocker | `config/ship_policy.v001.json` (owner directive 2026-08-12) limits blocking to **four classes**. | §3 states the four classes inside this manual so the two documents stop disagreeing. |

---

## 1. Duration profiles

| profile | runtime band | narration | words at ~173 wpm |
|---|---|---|---|
| standard | 11:30–12:30 | ~11 min | ~1,900 |
| **mid (default)** | **27:00–33:00** | **~27 min** | **4,600–4,700** |
| feature | 55:00–65:00 | ~55 min | ~9,500 |

An episode declares its own band in `episode_spec.vNNN.json`; the gate reads that file and **fails
rather than falling back** when it is absent. EP72 lacmegantic declares 1,740–1,920 s / 4,600–4,800 words.

---

## 2. The check inventory — what actually runs

**48 checks are emitted today. 50 ids exist historically.** Health measured across the newest receipt
of 32 episodes:

### 2.1 Clean — 15 checks that have never failed

`voice_is_master` · `captions_final` · `caption_narration_match` · `caption_integrity` · `caption_breaks` ·
`render_resolution` · `motion_present` · `motion_energy` · `leveled_animation` · `op_ed_bookends` ·
`thumbnail_ready` · `body_luma` · `script_craft` · `packaging_qc` · `check_packaging_qc`

These are the contract working. Do not touch them.

### 2.2 Noisy but real — measured, sometimes red, mostly informative

`animation_density` (25/7) · `animation_mix` (20/3) · `motion_density` (21/3) · `caption_format` (27/5) ·
`caption_coverage` (24/3) · `caption_sync` (22/2) · `factory_used` (29/3) · `footage_diversity` (31/1) ·
`footage_utilization` (25/2) · `image_cut_luma` (25/2) · `thumb_subject_luma` (25/2) · `bgm_present` (31/1) ·
`loudness` (31/1) · `images_present` (31/1) · `thumbnail_visibility` (31/1) · `script_lint` (26/1) ·
`script_length` (16/5) · `render_freshness` (21/7) · `probe_receipt` (21/7) · `visual_asset_qc` (16/7) ·
`asset_reuse` (11/10) · `arc_nonrepeat` (16/11) · `structure_4part` (18/14)

### 2.3 Chronically red — a gate that is almost always red is not a gate

| check | pass | fail | what to do |
|---|---|---|---|
| `preflight_receipt` | **3** | **25** | Either the preflight is not being run before the render, or the check reads the wrong path. Diagnose before EP72 renders. §6.1 |
| `runtime_band` | 13 | 19 | The single owner-accepted deviation (`upload_schedule_case_v001.py` tolerates it and nothing else). Keep as advisory. |
| `padding` | 10 | 17 | Threshold or instrument unproven. Do not weaken; measure it against a known-good film first. |
| `sound_layers` | 11 | 17 | Directly caused by the 2-vs-4 layer contradiction. §6.4 |
| `retention_cadence` | **5** | **16** | Either the films genuinely lack re-hooks, or the detector cannot see them. This is a craft signal worth repairing, not silencing. §6.3 |

### 2.4 Decoration — ids that have never once been measured

| check | pass | fail | skipped | diagnosis |
|---|---|---|---|---|
| `script_structure` | 0 | 0 | 8 | Looks for an annotated script under `03_script`, which does not exist because the script lives on the media root. **Never once executed.** |
| `check_script_craft` | 0 | 0 | 1 | Crashes: `ValueError: too many values to unpack (expected 2)`. A crash is recorded as `skipped`, which reads like an absence of inputs. |

**A check that has never been shown to fail is decoration** — that rule was already in the handover and
these two are the proof of it. Fix or delete; do not carry.

### 2.5 The rule the legend already states

The receipt's own legend says it: `skipped` means **THE GATE DID NOT MEASURE — not a pass.** On EP67
ramirez, two skipped checks were `declared_hard` (`check_encoder_settings`, `image_resolution`). A
release summary that counts skips as passes is a false green.

---

## 3. What may stop a ship

From `config/ship_policy.v001.json` (owner directive 2026-08-12), restated here so this manual and that
policy cannot drift apart. **Only these four classes hold the door shut:**

1. **`real_person_likeness`** — an identifiable real person, above all a minor, in footage or a generated image.
2. **`rights_and_licence`** — any asset without cleared licence or provenance; any third-party mark.
3. **`factual_support`** — a claim with no source id, or contradicted by the record. **This covers the
   title, the thumbnail text and the description exactly as it covers the narration.**
4. **`fabricated_record`** — AI-generated documents, judgments, newspapers or evidence shown as authentic.

Everything else is **measured, recorded in `09_package/release_deviations.v001.json`, and shipped.**
Advisory findings are decided by the agent doing the work and are not escalated. Nothing here lowers a
threshold: every check still runs and every number is still written down.

**No-rebuild ladder** (a finished master is never rebuilt for a defect measured in seconds):
ship-and-record → fix in the next revision → splice the affected range only → full re-render only for a
blocking defect distributed across the film, with a written reason.

---

## 4. The failure-mode → spec → gate table

Each row is something that went wrong. Build to the SPEC; the GATE is the check id that proves it.
Rows unchanged from v2 in substance are compressed here; the difference is that every row now names a
**real check id**, and rows whose gate does not exist say so.

| # | failure mode | spec (build to this) | gate (check id) |
|---|---|---|---|
| 1 | BGM does not play | Continuous bed, ducked under VO, floor ≈ −22 LUFS, never to silence. One track per chapter. | `bgm_present`, `bgm_ending` |
| 2 | Voice is "different" | Narration master = ElevenLabs `nPczCjzI2devNBz1zQrb`, `eleven_multilingual_v2`, stability ≈0.35, similarity ≈0.80. SAPI is a timing draft and never ships. | `voice_is_master` |
| 3 | Narration ≠ captions | Captions forced-aligned to the rendered audio, verbatim. | `caption_narration_match`, `captions_final`, `caption_coverage` |
| 4 | Captions unreadable | 1 cue = 1 breath group; ≤2 lines, ≤42 chars/line, 1.0–6.0 s, ≤17 cps, no orphan cues. | `caption_format`, `caption_breaks`, `caption_sync`, `caption_integrity` |
| 5 | Images coarse | Hero stills pre-generated, long edge ≥3840, no text, no real-person likeness. | `image_resolution`, `visual_asset_qc` |
| 6 | Not max quality | libx264 `-preset slow -crf ≤17`, yuv420p, bt709, 1920×1080, never NVENC; aac 320k; −16…−12 LUFS. | `render_resolution`, `loudness`, `check_encoder_settings` |
| 7 | Shelf barely used | ≥1 distinct factory clip per ~30 s; no clip reused >3×; b-roll matches the span's keywords. | `factory_used`, `footage_diversity`, `footage_utilization`, `asset_reuse` |
| 8 | Animation weak / 紙芝居 | No static image; no held frame >2 s; no naked hard cut; 0.3–0.5 s designed transitions; mean shot ≤6 s. | `motion_present`, `motion_energy`, `animation_density`, `animation_mix`, `motion_density` |
| 9 | Dead opening | **Hook = 0:00–~0:20, voiced from the first second, written FIRST** with the title and thumbnail. A time, a place, one person doing one thing, ending on something the subject does not know. **Do not summarise the outcome.** Brand OPENING moves off the 10–15 s window. | `hook_added`, `structure_4part` |
| 10 | Not hook/opening/body/ending | Four-part spine, in order; the ending delivers the promised reveal, then one specific ask. | `structure_4part` |
| 11 | No thumbnail | ≥3 variants at 1280×720, one selected, before `package_ready`. | `thumbnail_ready` |
| 12 | Thumbnail not striking | UPPERCASE ≤3–4 words, one idea, huge subject, high contrast, gold `#E5B53A` or `#1F6BFF`, readable at 320 px. No real-person likeness. | `thumbnail_visibility`, `thumb_subject_luma` |
| 13 | Packaging not CTR-max | Title **59–100 chars** (median ~82), third person, no question form, no citation or doctrine, real name as searchable suffix, ≥2 A/B variants. | `packaging_qc` |
| 14 | Off-brand OP/ED, motion written as adjectives | Every motion eased (`spring()` or `Easing.out(Easing.cubic)`), constant-linear forbidden; opacity-alone forbidden; stagger; ≥3 layers behind the subject; seconds derived from fps, never hard-coded frames. **The design document states start frame, end frame, displacement and easing type per motion.** Bookends imported, never forked. | `leveled_animation`, `op_ed_bookends` |
| 15 | Script correct but not gripping | `EPnn_FILM_BIBLE` + annotated script: cold-open question, escalating stakes, human throughline, motif, turn, payoff. Word count from the band in §1. Drama is built on the facts, never by inventing them. | `script_craft`, `script_length`, `script_lint`, `arc_nonrepeat` |
| 16 | Retention decays | Unresolved question opened in the first 8 s and held; open loops closing late; re-hooks every ~2–3 min; no flat stretch >20 s. | `retention_cadence` (see §6.3 — the instrument is unproven) |
| 17 | **A claim with no source** *(new in v3)* | Every factual span links to a claim id in the ledger. Title, thumbnail text and description are claims too. | `onscreen_text_verified`, ship-blocking class `factual_support` |
| 18 | **A person named who was acquitted or never charged** *(new in v3)* | Any living person described in the film carries their legal status in the same breath; `forbidden_claims` in the episode spec is the machine-readable record of what may not be said. | `script_craft.forbidden_claim`, `spec_satisfied` |

Rows 17 and 18 are added because EP72 is the first episode whose central figures were **tried and
acquitted**, and no row in v2 covered it.

---

## 5. The left-process gate — what must exist before Codex renders

1. `EPnn_FILM_BIBLE.vNNN.md` + `script.annotated.vNNN` — hook written FIRST, four roles explicit, word
   count inside the §1 band.
2. `shotlist.vNNN` / `SCENE_PLAN` — every span carries asset_type + motion + transition + factory
   `search_keywords`; mean shot ≤6 s; transitions designed, not defaulted.
3. `ai_prompts.vNNN` — one careful prompt per hero still, upscale target ≥3840 noted.
4. `thumb_prompts.vNNN` + headline/kicker candidates.
5. `fact_recheck.vNNN` packet — facts and quotes locked verbatim, every load-bearing figure sourced.
6. `manifest.target_duration_minutes` set, and `episode_spec.vNNN.json` valid
   (`scripts/check_episode_spec.py --slug <slug>` exits 0).

---

## 6. Broken instruments, in priority order

These are not craft complaints. Each is a measurement that cannot currently be trusted.

**6.1 `preflight_receipt` fails on 25 of 32 episodes — and the check is RIGHT.** Diagnosed 2026-08-20
by looking at what is on disk rather than at the code:

- **19 of 32 episodes have no `04_scenes/preflight_receipt.v*.json` at all** — the preflight was never
  run before the render. That includes EP66–EP69, the four most recently shipped.
- **10 of the 13 that do have one say `verdict: BLOCK`, `render_allowed: false`** — the preflight ran,
  said do not render, and the render happened anyway.
- Only 3 episodes ever rendered behind a GREEN preflight: 032 carsearch, 034 rolin, 035 hinders.

So this is not a broken instrument and not a path bug. It is a step that is skipped, and a refusal that
is overridden. Two live examples, measured the same day on the two episodes waiting to render:

| | EP70 wronghouse | EP71 oroville |
|---|---|---|
| `motion_density` | 0.00 beats/min over 39.8 min, animated coverage **0.0%** | 0.00 beats/min over 27.5 min, **0.0%** |
| `animation_mix` | 0.0% against a 45% floor | 0.0% against a 45% floor |
| `caption_integrity` | film `captions[] = 0` — no burned captions | film `captions[] = 0` |
| `caption_breaks` | 66 lines end on a function word, 70 orphan cues | 37 / 47 |
| `visual_asset_qc` | **64.4% of 160 stills too dark** vs a 40% allowance | PASS (13.6%) |
| `plate_review` | PASS | **117 of 118 plates are 1672×941 against an order that says 3840** — rejected at review, still declared in `mandatory_stills`, still staged in the pool the builder draws from |
| `script_length` | 6,905 words against a declared 55–65 min band | — |

Either render, started today, would have produced a 紙芝居 with no captions — three GPU-hours for a
film the owner would reject on sight. **The preflight is not optional and its BLOCK is not advisory.**
Run `preflight_render_gate.py --ep <EPID>` and clear it before any render is started.

**6.2 Two gates carry two ids each.** `packaging_qc` (8 receipts) and `check_packaging_qc` (13), and
`script_craft` (7) and `check_script_craft` (1), are the same gates renamed mid-history. The rename
silently reset each one's record, so no trend across episodes is comparable. Pick one id per gate and
map the old name to it in the receipt reader.

**6.3 `retention_cadence` passes 5 and fails 16.** Two hypotheses and they are testable: the films
really do lack re-hooks, or the detector cannot see re-hooks written as narration rather than as
structure. Run it against the channel's best-retaining film (053 norfolk, 40.3% of a 28-minute
runtime) before touching either the films or the threshold.

**6.4 `sound_layers` is failing a contradiction, not a defect.** `PD_EPISODE_SPEC_STANDARD.v001`
defaults `audio_layers` to 2 and says so precisely to force this contradiction into the open; the
finisher builds four. Settle it: either the four-layer provenance artefact gets produced, or the check
measures what the mixer actually makes.

**6.5 `script_structure` and `check_script_craft` have never executed.** §2.4. Fix or delete.

**6.6 `check_script_length` counts HTML citation comments as spoken words.** Found 2026-08-20 while
writing EP72. The counter strips `【…】`, `〔…〕`, `[…]`, `(…)`, headings and markdown punctuation —
but not `<!-- … -->`, and every script since EP66 carries one citation comment under every factual
line. Measured inflation, per script:

| script | as the counter reads it | comments removed | inflation |
|---|---|---|---|
| EP69 hyatt v001 | 7,294 | 5,099 | **+2,195** |
| EP68 pinto v002 | 6,769 | 4,971 | +1,798 |
| EP66 openfields v003 | 8,066 | 6,330 | +1,736 |
| EP67 ramirez v002 | 6,716 | 5,151 | +1,565 |
| EP71 oroville v001 | 6,237 | 4,981 | +1,256 |
| EP70 wronghouse v001 | 7,983 | 7,008 | +975 |

The defect is masked once an episode has a voice plan: `spoken_words_from_voice_plan()` reads the
real chunk words and the raw count is not used. It bites **before narration exists** — which is
exactly when a writer is deciding whether the script is long enough. A script that reads 5,751 on
this gate can be 4,876 words of narration, and the difference is four minutes of finished film.

This is a candidate root cause for the chronic runtime shortfall recorded across the back
catalogue. **Fix: strip `<!--.*?-->` before counting, then re-measure every script that has no voice
plan.** Until it is fixed, size a script from `gen_narration_case.py --dry-run`, which reports the
words the TTS extractor will actually speak, and confirm with `--measure-section` before writing to
length.

**6.7 The 171.79 raw-wpm model is not universal.** The narration registry models every episode since
EP66 at 171.79 raw words per minute. EP72 measured **191.1** on its own ACT_1 — 11 % faster — because
its register is short declaratives. **Measure the section, then write to the measurement**; a script
sized on the model would have finished four minutes short.

---

## 7. Definition of done, per episode

1. `episode_spec.vNNN.json` valid, and the film measured against **its** numbers.
2. `check_final_acceptance.py --emit-receipt` run against the exact final file; receipt written with
   `video_sha256`.
3. Every **blocking-class** finding clear. Advisory findings written to
   `09_package/release_deviations.v001.json` with measured value, threshold and reason.
4. No check counted as passing because it was skipped.
5. Uploaded private with `publishAt`, then verified `processed/succeeded` by a live API read — a date
   on an unprocessed video is not a schedule.
