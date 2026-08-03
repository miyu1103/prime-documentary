# PD episode spec — the channel standard (v001, 2026-08-02)

## What this is

Every PD design document is prose: it tells a writer and Codex what the film should feel like.
Nothing in it is machine-readable, so nothing in it can be enforced. This file fixes the
**numbers** an episode commits to, and `schemas/episode_spec.v001.json` fixes their shape. Each
episode carries its own `episode_spec.v001.json`; every tool reads that file and nothing else.

Prose design documents do not change. This is a second layer, not a replacement.

## The rule that makes it work

> **An undeclared value is an error. Nothing is inferred.**

This is the whole point. On 2026-08-02 the acceptance gate contained exactly this fallback:

```python
t = manifest.get("target_duration_minutes")
if not t:
    return RUNTIME_LO, RUNTIME_HI      # silently: 690-750s, an 11.5 minute film
```

None of EP50–EP59 carried a manifest, so every 29-minute episode was measured against a
12-minute band and failed. Six checks failed on eight or nine of nine episodes. A gate that is
always red is not a gate — and three real defects (a rubber-stamp footage QC, a duplicate-upload
guard that never executed, a probe receipt from a different render) sat inside that red for
months without being seen.

So: no silent defaults, anywhere. If the spec does not say it, the tool stops and says so.

## The standard, from measurement

Measured across EP54–EP59 on 2026-08-02:

| | flowers | burge | postoffice | fieldtest | lejeune | robosigning |
|---|---|---|---|---|---|---|
| runtime | 1732s | 1770s | 1786s | 1656s | — | — |
| script words | 6,214 | 6,385 | 7,229 | 7,413 | 8,020 | 8,146 |
| beats per act | 17–19 | 14–22 | 13–17 | 13–17 | 14–17 | 14–17 |
| acts | 4 | 4 | 5 | 5 | 5 | 5 |
| distinct video | 188 | 259 | 177 | 191 | 142 | 139 |
| people plates | 15 | 16 | 15 | 14 | 8 | 7 |

The word counts include each script's front-matter and appendix; the narration itself measures
4,673–4,750 words, which is the number the band below refers to.

### Channel defaults — a new episode inherits these unless its own spec overrides them

| field | value | why this number |
|---|---|---|
| `runtime_seconds` | **[1620, 1920]** | 27–32 min. Covers every measured master (1656–1786s) with margin. The old 690–750 band described a format the channel stopped making. |
| `script_words` | **[4400, 4900]** | Narration only. Measured 4,673–4,750 at 172–178 wpm. |
| `figure_beats_per_act` | **[13, 17]** | EP52–EP56 sit at 13–24; 13 is the floor below which `motion_density` starts failing, 17 keeps an act from becoming a slide deck. |
| `distinct_video_assets` | **runtime × 0.65 ÷ 4.5** | Footage cuts, NOT cuts ÷ reuse-cap. At 29 min that is ≈ 250. EP54 shipped 188 against 253 footage cuts and 65 clips ran twice. |
| `people_plates_min` | **8** | Siblings carry 7–16. EP57 carried 2 and EP60 carried 0. |
| `thumbnail_candidates_min` | **3** | What `thumbnail_ready` requires. A single Codex face plate yields one, so variants are mandatory. |
| `footage_review_required` | **true** | 683 of 1,094 staged clips across five episodes were wrong for their story once someone actually looked. |
| `audio_layers` | **2** | The truth of this pipeline: a BGM bed plus the master VO. `sound_layers` demands a four-layer provenance artifact that no step produces — declaring 2 forces that contradiction to be settled rather than waived on every episode. |
| `section_vocabulary` | per episode | EP54/EP55 are four-act, EP56+ are five-act. `structure_4part` failed 9 of 9 looking for an `OPENING` section that these scripts do not have. |

`mandatory_stills` has no default: it is empty unless stills were generated **for** this episode
to cover a gap, in which case every one of them is listed. EP54's fourteen courtroom stills were
generated precisely because the archive holds no courtroom footage, and were then dropped by a
surplus-trimming rule and retired as unreferenced. Listing them makes that impossible.

## How it is enforced

1. `scripts/check_episode_spec.py --slug <slug>` — the spec exists, validates, and every
   required field is present. **No field, no build.**
2. `scripts/check_episode_inputs.py --slug <slug>` runs it first, then checks the pool, the
   beats and the images against the spec's own numbers instead of against constants.
3. `scripts/check_final_acceptance.py` reads the band from the spec. When the spec is absent it
   **fails** rather than falling back.

## What this does not fix

Nothing here judges whether a clip suits the story, whether the writing is good, or whether
anyone will watch. It removes one class of failure completely: the class where the intent
existed, was written down in prose, and no machine could read it.
