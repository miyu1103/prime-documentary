# Pre-render acceptance forecast — EP62 greene / EP63 correa

**GREENE SAFE TO START: yes — CORREA SAFE TO START: yes**

Produced 2026-08-12 00:12–00:45 JST, while EP65 marmet was rendering. Read-only: no render was
started, no film.json was rebuilt, no episode `.srt` was written. The two caption polishes below
were run on **copies** in the scratchpad; both episode srts are byte-unchanged (mtimes verified
before and after).

Nothing in either episode needs an owner decision **before** the render starts. Every predicted
failure either self-clears inside `_finish_episode.sh` or is already covered by an approved APR,
with one exception (correa `visual_asset_qc`) that is a stale bookkeeping copy, does not touch a
single pixel, and can be fixed at any point before acceptance — including while the render runs.

---

## 1. The finding that matters most

**The current on-disk `.srt` is not the file that gets burned.** `_finish_episode.sh` step [4/7]
rebuilds `film.json` via `build_case_film_generic.py`, whose `write_srt` regenerates the entire
`captions.final.v001.srt` from `narration_index.v001.json` at **raw chunk timings**, and only then
does step [4b] polish it. So the four caption checks that `predict_acceptance.py` reports red are
measuring an intermediate artefact. Measured, not assumed:

| | greene now | greene post-polish | correa now | correa post-polish |
|---|---|---|---|---|
| lead measured in the srt | 0.0 s | 0.25 s | 0.0 s | 0.25 s |
| orphan cues | 39 | **0** | 35 | **0** |
| dangling breaks | 93 | **0** | 88 | **0** |
| lag p50 | +0.000 s | −0.250 s | +0.000 s | −0.250 s |
| lag p75 | — | −0.168 s | — | −0.210 s |
| **lag p90 (gate +0.35 s)** | pass | **+0.127 s** | **+0.368 s FAIL** | **+0.093 s** |
| `check_caption_breaks` | FAIL | **PASS** (0.0 % bad, cap 5 %) | FAIL | **PASS** (0.0 % bad) |
| `verify_caption_sync` | FAIL | **PASS** | FAIL | **PASS** |

correa's `+0.368 s` p90 — the second of last night's two defects — is real in the file as it sits,
and is removed by the 0.25 s lead step [4b] applies. Neither filmconfig declares
`captionLeadSeconds`, so both resolve to the house default 0.25 s.

---

## 2. Last night's two defects, checked specifically

### (i) Does the filmconfig `captions` key point at the revision matching the current narration master?

**Yes, both.** This is the EP67-ramirez defect (a filmconfig pointing at a v001 written before the
script was extended, which would burn captions 152.8 s out of sync). Neither episode has it.

- `EP62_greene_filmconfig.v001.json` → `episodes/PD-2026-062-greene/08_edit/captions.final.v001.srt`
- `EP63_correa_filmconfig.v001.json` → `episodes/PD-2026-063-correa/08_edit/captions.final.v001.srt`
- `v001` is the **only** `captions.final.v*.srt` revision on disk for either episode, so there is no
  wrong revision available to pick.

Four independent confirmations that these srts belong to these narration masters:

1. `polish_captions_srt.measure_lead` — the guard written to catch exactly the ramirez case —
   lines up **280 of 383** greene chunks and **268 of 364** correa chunks with a cue start, far
   above its `MIN_LEAD_MATCHES=8` / `MIN_LEAD_MATCH_FRACTION=0.25` floors, and the offset is a
   constant 0.0 s rather than a staircase.
2. `caption_narration_match`: **100.0 %** token match both ways (greene 5256 w / 5256 w;
   correa 5171 w / 5171 w).
3. `verify_caption_sync` matched **498/498** greene cues and **509/510** correa cues against a
   whisper transcription of the real master
   (`H:\pd-media\episodes\PD-2026-06*-*\06_voice\master\vc_master_v001.mp3`).
4. `caption_coverage`: every narration chunk captioned, no dropped captions, both episodes.

### (ii) Does the caption lead in the srt itself sit inside the +0.35 s p90 gate?

- **As the files sit now:** greene yes; **correa NO, +0.368 s.**
- **As they will be burned (after step [4b]):** greene **+0.127 s**, correa **+0.093 s.** Both pass
  with margin, both with p50 at −0.250 s (leading the word, which the gate treats as good up to
  `LEAD_OK = 0.80`).

---

## 3. greene — every predicted failure, classified

`py -3.11 scripts/predict_acceptance.py --slug greene`
→ predicted runtime **1861.5 s = 31.03 min** (band 1620–1980 s, PASS); 8 will fail, 0 carryover
(no `greene_film.rendered.json` snapshot), 13 need pixels, 4 undecided.

| # | check | class | evidence |
|---|---|---|---|
| 1 | `caption_breaks` — 39 orphans, 86 mid-phrase splits | **(a) self-clears** | step **[4b]** `polish_captions_srt.py`. Measured on a scratch copy: 565→498 cues, orphans 39→0, dangling 93→0; `check_caption_breaks` then exits **0** ("bad share 0.0 %, cap 5 %"). [4b] would `die` if it did not clear, so this cannot silently ship. |
| 2 | `caption_format` — 298 violations (58/67/83/84 ch lines) | **(a) self-clears**, and APR'd anyway | The violations are line lengths against `MAX_LINE_CHARS = 50` on an **unwrapped** srt. [4b] wraps every cue to ≤2×50 ch, ≤84 ch/cue, ≤6.8 s, ≤27 cps. Also listed in APR-0002. |
| 3 | `caption_sync` — 93 dangling breaks | **(a) self-clears** | Post-polish: 0 dangling, p90 +0.127 s → `RESULT: PASS`. |
| 4 | `footage_utilization` — 1 of 74 staged clips unreferenced (`AR-6041714__video_of_not_working_television.mp4`) | **(a) self-clears** | step **[4c]** `retire_unused_pool_clips.py --slug greene`, which runs after the film is built and retires exactly what no cut references. |
| 5 | `probe_receipt` — `probe_receipt.v002.json` film_sha `ee7dc668…` ≠ current `4434bf92…` | **(a) self-clears** | step **[5b]** `probe_before_render.sh` renders a fresh 60 s slice and calls `check_final_acceptance.py greene --probe …`, which stamps the **current** film sha. That is the binding the gate looks for. |
| 6 | `preflight_receipt` — `verdict=BLOCK render_allowed=False` | **(d) owner-accepted** | APR-0002 (`target_type=edit`, `decision=approved`) lists `preflight_receipt`. Note it does **not** self-clear: the finisher never re-runs `preflight_render_gate.py`. Root cause is that `04_scenes/remotion_plan.v001.json`, `scene_plan.v001.json` and the annotated script do not exist for this episode — the same absence that leaves `script_structure` and `onscreen_text_verified` UNDECIDED. Producing a green preflight would mean authoring that whole lane, not fixing a number. |
| 7 | `asset_reuse` — 28 assets over cap (all `2x>1`) | **(d) owner-accepted** | APR-0002 lists `asset_reuse`. No asset is used more than **twice**; `footage_diversity` independently PASSES at 313/389 distinct (0.80), max reuse 2. |
| 8 | `padding` — 24 seven-word phrases repeating >4 | **(d) owner-accepted** | APR-0002 lists `padding`. |

**Scheduler paperwork:** `final_delivery.v*.json` "none written" — post-render artefact, written
after acceptance. Not a render blocker. Everything else (youtube_meta 87 ch title / 4221 ch
description / 18 tags, thumbnail v010 1280×720 1.03 MB, captions sidecar, not-already-scheduled)
is green.

**Already green and worth naming**, because these are the ones that historically cost re-renders:
`animation_mix` (stills 27.8 %, motion 80.0 %, 0 lingering stills), `motion_density`
(3.13 beats/min, 96 kinetic beats), `arc_nonrepeat` (313 cut assets unique vs 119 other episodes),
`op_ed_bookends` (opening card 8.00–11.50 s, end-card 1852.51–1861.51 s), `visual_asset_qc`,
`thumb_subject_luma`, `retention_cadence`, `script_craft`, `script_lint`, `runtime_band`.

---

## 4. correa — every predicted failure, classified

`py -3.11 scripts/predict_acceptance.py --slug correa`
→ predicted runtime **1903.7 s = 31.73 min** (PASS); 7 will fail, 0 carryover ("the film json has
changed since the last render"), 13 need pixels, 4 undecided.

| # | check | class | evidence |
|---|---|---|---|
| 1 | `caption_breaks` — 35 orphans, 84 mid-phrase splits | **(a) self-clears** | [4b]: 557→510 cues, orphans 35→0, dangling 88→0; `check_caption_breaks` exits **0**. |
| 2 | `caption_format` — 316 violations | **(a) self-clears**, and APR'd | Same mechanism as greene. |
| 3 | `caption_sync` — **p90 +0.368 s > +0.35 s**, 87 dangling | **(a) self-clears** | [4b] applies the 0.25 s lead to a file measured at 0.0 s → p90 **+0.093 s**, 0 dangling, `RESULT: PASS`. This is the one genuine timing defect in either episode and the finisher removes it. |
| 4 | `footage_utilization` — 7 of 58 staged clips unreferenced | **(a) self-clears** | step [4c] `retire_unused_pool_clips.py`. |
| 5 | `probe_receipt` — probe sha `06aaeac3…` ≠ current `e356c354…` | **(a) self-clears** | step [5b], as greene. |
| 6 | `preflight_receipt` — `verdict=BLOCK` | **(d) owner-accepted** | APR-0002 lists `preflight_receipt`; same missing-plan-lane root cause. |
| 7 | `visual_asset_qc` — 27 staged clips not in the manifest | **(b) fixable now, no rebuild — the only hand-fix in either episode** | See below. |

`asset_reuse` and `padding` both **PASS** on correa (unlike greene).

### correa `visual_asset_qc` — the one thing to actually do

`check_visual_asset_qc` reads the latest `episodes/<ep>/05_visuals/factory_clip_qc.v*.json`. correa's
only revision is **v001, dated 2026-08-10 13:45** — which predates the round-3 prestage review of
the re-staged pool.

The review that covers the current pool **already exists**:
`runs/qc/correa_clip_verdicts.v001.json`, written **2026-08-11 20:36**, carrying a
`pool_frame_review` block with `reviewer = "claude (prestage content review round 3, EP63 correa)"`,
`reviewed_at = 2026-08-11` and an exact `pool_id_sha256` binding. **All 58 currently staged clips
appear in it** (verified 58/58 by name and by stem). `check_episode_inputs.py` reads that file and
reports `binding=exact` for correa.

So the gap is a **stale copy**, not a missing review. Measured overlap with the film:

- 27 staged clips are absent from the stale `05_visuals/factory_clip_qc.v001.json`;
- **24 of those 27 are referenced by cuts** in `correa_film.json`, so step [4c] retires only 3
  (`AR-6830138__people_playing_domino.mp4`, `AR-9498288__an_escalator_is_moving_up_and_down_in_a_subway.mp4`,
  `AR-v_46821__puerto_rico_flag_wind_roofs.mp4`);
- therefore this does **not** self-clear, and no APR covers `visual_asset_qc` for correa.

**Fix:** transcribe the existing round-3 verdicts into
`episodes/PD-2026-063-correa/05_visuals/factory_clip_qc.v002.json`, carrying through the original
reviewer, `reviewed_at` and `pool_id_sha256` as provenance. That is a mechanical copy of a review
somebody actually performed — it must **not** be written as a fresh attestation by anyone who has
not looked at the frames. It touches no pixel, needs no rebuild, needs no GPU, and can be done at
any point before the acceptance run, including during the render. If the owner would rather not
touch it, the alternative is a one-line APR addition.

---

## 5. Item (d) re-verified: correa's `distinct_video_assets: 234`

The previous session's judgement was to accept it at mean reuse 1.36×. **Re-derived against today's
numbers, the judgement holds — and the framing in the brief needs two corrections.**

**Correction 1 — the declaration is arithmetically impossible, so no rebuild can rescue it.**
correa's staged video pool is 58 factory + 128 motion = **186** clips. Declaring 234 distinct video
assets cannot be met even if every clip were used exactly once. `check_spec_satisfied` measures
**179 distinct across 279 video cuts — 55 short**. This is a wrong number in `episode_spec`, not a
defective film. Restaging ~50 more reviewed clips and rebuilding the film is the only way to satisfy
it literally, which is hours of pool work plus a rebuild that cannot happen while the render is
live.

**Correction 2 — greene has the same failure, and the brief did not mention it.**
`check_spec_satisfied --slug greene` also FAILs: **196 distinct across 272 video cuts against a
declared 234 — 38 short**. Unlike correa, greene's pool (74 factory + 193 motion = **267**) *could*
support 234, so greene's declaration is reachable in principle — but only by rebuilding the film.
**Classification (c) for greene: flag to the owner as a decision, do not act.** It is not urgent:
see below.

**Why neither blocks anything tonight:**

- `distinct_video_assets` is **not an acceptance check**. It never appears in a receipt and cannot
  make the ship gate red.
- It does **not** stop the finisher. Step [4a] only dies when the output matches
  `mandatory_stills|forbidden_subjects`; both episodes report `distinct_video_assets` as their sole
  problem. (The summary lines read `mandatory=224` / `forbidden_keywords=9`, which do not match
  those patterns — verified against the literal grep in the finisher.)
- The pre-flight at [0/7] is invoked by `queue_unattended.sh` with
  `--allow-video-diversity-deviation`, and `check_episode_inputs.py` exits **0** for both episodes
  under exactly those arguments.
- **The acceptance gate independently says the reuse is fine.** correa `asset_reuse`: *"278 distinct
  over 378 cuts (mean 1.36×, first-use 74 %)"* — **PASS**. correa `footage_diversity`: 278/378
  distinct (0.74), **max reuse 2** — PASS. greene: 313/389 (0.80), max reuse 2 — PASS. No asset in
  either film is on screen more than twice.

So the 1.36× reasoning survives contact with the current numbers: the ceiling that matters to a
viewer is *how often the same clip comes back*, and that is 2 at worst in both films.

---

## 6. Hard stop-points inside the finisher — all cleared in advance

`_finish_episode.sh` `die`s at eight places. Each was checked without spending the GPU:

| step | die condition | greene | correa |
|---|---|---|---|
| [0/7] | `check_episode_inputs.py` non-zero | **exit 0** — "READY to build" | **exit 0** — "READY to build" |
| [2b] | blocklist prune fails | no scoped rejection → no-op | no-op |
| [4/7] | `build_case_film_generic.py` fails | config present (`EP62_greene_filmconfig.v001.json`) | config present |
| [4a] | output matches `mandatory_stills\|forbidden_subjects` | only `distinct_video_assets` → **no die** | only `distinct_video_assets` → **no die** |
| [4b] | `polish_captions_srt` or `check_caption_breaks` fails | polish OK, breaks **PASS** | polish OK, breaks **PASS** |
| [4d] | 4-layer mix density gate | `density: sfx/min=3.253 (floor 2.0), distinct_beds=7 (floor 4), coverage=0.989 (floor 0.85) -> PASS`, **exit 0** | `density: sfx/min=2.393 (floor 2.0), distinct_beds=7, coverage=0.989 -> PASS`, **exit 0** |
| [5b] | 60 s probe shows black/frozen | not testable without the GPU | not testable without the GPU |
| [6/7], [7/7] | render / mux / post-gate | needs the render | needs the render |

The queue will in fact pick both up: it skips an episode whose master is newer than its film.json,
and for both the film.json is newer (greene film 08-11 01:46 vs master 08-10 17:15; correa film
08-11 20:57 vs master 08-10 22:17).

---

## 7. Recommendation

**Let greene start on schedule. Let correa follow.** No owner decision is required before either
render begins.

Two things to put in front of the owner, neither of them urgent and neither of them a reason to
hold the queue:

1. **correa `visual_asset_qc`** — do the manifest transcription (§4) during the render, or add it to
   an APR. It is the only predicted failure in either episode that will still be red at acceptance
   and is not already approved.
2. **`distinct_video_assets` declared 234** — impossible for correa (pool ceiling 186), reachable
   but unbuilt for greene (196 of 234 with a 267-clip pool). Neither blocks the render or the ship
   gate, and the reuse the viewer actually sees is capped at 2×. The decision is whether to correct
   the two `episode_spec` declarations to match the pools, or to restage and rebuild later.

Residual risk that no pre-render forecast can retire: the 13 pixel checks
(`animation_density`, `motion_energy`, `body_luma`, `images_present`, `motion_present`, `loudness`,
`bgm_present`, `bgm_ending`, `image_cut_luma`, `render_resolution`, `render_freshness`,
`check_encoder_settings`, `sound_layers` PART 1). Neither episode has a
`<slug>_film.rendered.json` snapshot matching its current film.json, so there is **no carryover
evidence** for any of them — they are genuinely unknown until the mp4 exists. `animation_density` is
already APR'd on both (APR-0003) against the single-span limit.

---

### Commands run (all read-only; full output in the session transcript)

```
py -3.11 scripts/predict_acceptance.py --slug greene
py -3.11 scripts/predict_acceptance.py --slug correa
py -3.11 scripts/check_episode_inputs.py --slug {greene,correa} --allow-video-diversity-deviation --no-forecast
py -3.11 scripts/check_spec_satisfied.py --slug {greene,correa}
py -3.11 scripts/polish_captions_srt.py --srt <SCRATCH>/{greene,correa}_polished.srt --lead 0.25 \
     --narr episodes/PD-2026-06{2,3}-{greene,correa}/06_audio/narration_index.v001.json
py -3.11 scripts/verify_caption_sync.py --ep PD-2026-06{2,3}-{greene,correa} --srt <SCRATCH>/..._polished.srt
py -3.11 scripts/check_caption_breaks.py <SCRATCH>/{greene,correa}_polished.srt
py -3.11 scripts/build_case_film_audio.py --ep PD-2026-06{2,3}-... --out out_qc/_predict_..._audio_dryrun.json --dry-run
```

Not run, deliberately: `build_case_film_generic.py`, any render, anything touching the queue or
`_finish_episode.sh`. The scratch srts live in the session scratchpad and can be deleted.
