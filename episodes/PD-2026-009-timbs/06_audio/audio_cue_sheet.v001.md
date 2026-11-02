# PD-2026-009 Timbs Audio Cue Sheet v0.1

Episode: `PD-2026-009-timbs`
Target composition: `RoughCut-timbs`
Target duration: `12:00.000` / `720.000s`
Status: edit cue sheet, no paid generation performed

## Mix rules

- VO is always the priority layer.
- During VO, duck music by `-8dB` to `-12dB`; keep music mostly below `-18 LUFS short-term`.
- During VO, duck ambience by `-6dB` to `-10dB`; keep ambience mostly around `-30 LUFS short-term`.
- Spot SFX may lead transitions, numbers, document reveals and legal turns, but must not mask key words.
- Final review target: integrated loudness near `-14 LUFS`, true peak at or below `-1 dBTP`.
- Keep the lower subtitle band clear. Do not use audio-reactive graphics that force subtitle/teletext overlap.

## Layer map

1. Narration: generated from approved script only.
2. Music: restrained Suno beds, chapter-specific energy curve.
3. SFX: cuts, reveals, number beats, lower-third/text-entry accents.
4. Ambience: courtroom, street/night, office/institutional room tone.

## Music arc

| Time | Section | Music asset | Mix intent |
|---:|---|---|---|
| `00:00-00:30` | Hook highlights | `artifact://library/music/hook/mus_20260614_hook_glass_air_bed_v2.mp3` | Fast highlight bed, urgent but not trailer-heavy. Add sub drop at first frame, riser into title. |
| `00:30-01:15` | Opening | `artifact://library/music/opening/mus_20260614_opening_measured_arpeggio_v2.mp3` | Existing channel opening style. Keep measured, recognizable, and under title VO. |
| `01:15-03:45` | Act I, the Land Rover and the mismatch | `artifact://library/music/explainer_bed/mus_20260614_explainer_bed_soft_explainer_v2.mp3` | Clear explanatory pulse for facts, car, money and proportionality numbers. |
| `03:45-06:30` | Act II, the hidden forfeiture machine | `artifact://library/music/reveal/mus_20260614_reveal_hidden_system_clicks_v2.mp3` | Mechanical, investigative. Emphasize process, paperwork and incentives. |
| `06:30-09:15` | Act III, old limit becomes national rule | `artifact://library/music/tension_build/mus_20260614_tension_build_courtroom_horizon_v2.mp3` | Build through Supreme Court stakes. Leave air before the 2019 result. |
| `09:15-10:45` | Act IV, what the ruling does and does not solve | `artifact://library/music/somber/mus_20260614_somber_ledger_of_ash_v2.mp3` | Reflective, restrained. Avoid triumphal scoring; the rule is important but incomplete. |
| `10:45-12:00` | Ending and next-case bridge | `artifact://library/music/outro/mus_20260614_outro_last_frame_v2.mp3` | Resolve Timbs, then pivot toward Kelo/public use without sounding sensational. |

## Ambience beds

| Time | Bed asset | Purpose |
|---:|---|---|
| `00:00-00:30` | `artifact://library/ambience/amb_tension_drone.mp3` | Hook pressure under fast montage. Keep very low under VO fragments. |
| `00:30-01:15` | `artifact://library/ambience/amb_empty_hallway.mp3` | Institutional air behind opening and title. |
| `01:15-03:45` | `artifact://library/ambience/amb_night_window.mp3` | Personal-scale night/street tone around the arrest and vehicle material. |
| `03:45-06:30` | `artifact://library/ambience/amb_office_hum.mp3` + `artifact://library/ambience/amb_institutional_drone.mp3` | Paperwork, cash flows, agencies and civil-process atmosphere. |
| `06:30-09:15` | `artifact://library/ambience/amb_courtroom_room_tone.mp3` | Legal argument and court-room gravity. |
| `09:15-10:45` | `artifact://library/ambience/amb_empty_hallway.mp3` | Aftermath, limits and unresolved questions. |
| `10:45-12:00` | `artifact://library/ambience/amb_night_window.mp3` | Closing reflection and next-episode bridge. |

## Spot SFX

| Time | SFX asset | Cue |
|---:|---|---|
| `00:00.0` | `artifact://library/sfx/sfx_sub_drop.mp3` | First hook frame. Very short, low. |
| `00:00.8` | `artifact://library/sfx/sfx_riser_2s.mp3` | Hook acceleration into first highlight stack. |
| `00:04.5` | `artifact://library/sfx/sfx_whoosh_short.mp3` | Fast highlight cut. Repeat only where the visual turn is meaningful. |
| `00:09.0` | `artifact://library/sfx/sfx_data_blip.mp3` | First number/text reveal in hook. |
| `00:15.0` | `artifact://library/sfx/sfx_low_boom.mp3` | Supreme Court / constitutional-stakes hook beat. |
| `00:20.0` | `artifact://library/sfx/sfx_soft_impact.mp3` | Hook-to-opening impact. |
| `00:30.0` | `artifact://library/sfx/sfx_whoosh_medium.mp3` | Opening card transition. |
| `01:15.0` | `artifact://library/sfx/sfx_page_turn.mp3` | Main story begins. |
| `02:10.0` | `artifact://library/sfx/sfx_data_blip.mp3` | Fine / vehicle-value comparison. Keep below VO. |
| `03:17.0` | `artifact://library/sfx/sfx_stamp_seal.mp3` | Proportionality/legal-document reveal. |
| `03:45.0` | `artifact://library/sfx/sfx_binder_lock.mp3` | Act II hidden-system transition. |
| `04:55.0` | `artifact://library/sfx/sfx_paper_rustle.mp3` | Paperwork/civil-process passage. |
| `06:30.0` | `artifact://library/sfx/sfx_gavel_knock.mp3` | Act III court transition. |
| `07:45.0` | `artifact://library/sfx/sfx_clock_tick_loop.mp3` | Incorporation/timeline stretch. Fade under VO. |
| `09:15.0` | `artifact://library/sfx/sfx_soft_impact.mp3` | 2019 ruling / 9-0 result beat. |
| `10:30.0` | `artifact://library/sfx/sfx_dust_swell.mp3` | The ruling creates a limit, not an ending. |
| `10:45.0` | `artifact://library/sfx/sfx_page_turn.mp3` | Ending bridge. |
| `11:30.0` | `artifact://library/sfx/sfx_riser_2s.mp3` | Next case tease, keep subtle. |
| `11:58.0` | `artifact://library/sfx/sfx_ui_tick.mp3` | Final subscribe/end-card UI accent. |

## Ducking and masking notes

- Do not place `sfx_gavel_knock`, `sfx_low_boom` or `sfx_sub_drop` under clause endings that carry legal meaning.
- Number reveals should use `sfx_data_blip` at low level, not arcade-style UI bursts.
- If VO alignment produces dense captions, reduce spot SFX rather than moving captions.
- In the hook, use SFX on only the strongest 5 to 7 cuts; the montage should feel fast, not noisy.
- In the ending, remove ambience if it competes with the final next-episode line.

## Caption and title-safe audio notes

- Captions are synced to forced alignment and stay in the bottom band.
- Text callouts and source labels should not trigger loud SFX if they appear while captions are dense.
- For legal citations, prefer quiet paper/stamp cues over dramatic hits.

## Remaining audio tasks

- Generate approved narration after the paid gate.
- Add `narrationSrc` entries to the Remotion data after audio files exist.
- Run forced alignment against final narration.
- Build the final mix with VO-first ducking.
- Perform loudness and decode QC before first-cut review.
