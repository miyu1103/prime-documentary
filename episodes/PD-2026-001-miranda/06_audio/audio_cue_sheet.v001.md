# Audio cue sheet — PD-2026-001-miranda (v001)

Four-layer sound design so the episode is **never silent** (owner note 2026-06-14). Drives the
final Remotion mix. Track families come from `prompts/11_music_library_briefs.md`; actual
`MUS-*/SFX-*` IDs are bound after the library is generated (ElevenLabs, automated, in-plan).

**Mix targets:** VO (narration) on top and always intelligible; music bed **−18…−22 LUFS** under VO;
ambience near-subliminal (**≈−30 LUFS**, glues cuts); SFX punctuate transitions/reveals. Master
≈ **−14 LUFS** (YouTube). Music ducks ~3–4 dB under VO (sidechain).

| Scene | Emotion | Music family | Ambience bed | SFX hits |
|---|---|---|---|---|
| S001 | curiosity_tension | **hook** | tense low drone | UI ticks on text; **sub-drop** at hook end |
| S002 | orientation | **opening** | room tone | soft impact on "A repair" |
| S003 | grounding | explainer_bed | room tone | map-pin tick; camera-shutter (still) |
| S004 | unease | tension_build (low) | **interrogation drone** | lamp hum; low boom |
| S005 | tension_build | tension_build | drone | data blips (diagram) |
| S006 | doubt | explainer_bed | drone | UI tick on the question |
| S007 | weight | somber / tension | courtroom room tone | **gavel knock**; camera-shutter |
| S008 | escalation | tension_build | drone | paper rustle; stamp/seal |
| S009 | scale | explainer_bed | room tone | UI ticks ×4 (case names); page-turn |
| S010 | insight | explainer_bed | drone | data blips (4→1 converge) |
| S011 | anticipation | tension_build | dust/air swell | **riser** begins |
| S012 | payoff | **reveal** | ambience swell | riser→**reveal sting**; low boom (date card) |
| S013 | clarity | explainer_bed | room tone | UI tick per numbered point ×4 |
| S014 | authority | explainer_bed | room tone | page-turn (Constitution); soft impact |
| S015 | counterpoint | somber | drone | subtle (no big hit) |
| S016 | recognition | explainer_bed | room tone | stamp/seal (card); camera-shutter |
| S017 | insight | reveal (soft) | drone | data blips; soft reveal swell |
| S018 | twist | tension_build → somber | drone | gavel knock; **low boom** (the twist) |
| S019 | understanding | explainer_bed | room tone | data blips |
| S020 | settle | — (ambience only) | dust/air | soft whoosh (breather) |
| S021 | resolution | outro-ish / explainer | warm bed | soft impact |
| S022 | poignancy | **somber** | sparse room tone + distant | subtle; light dust |
| S023 | invitation | **outro** | resolved bed | soft sub; end-card boom |

**Global:**
- A continuous **room-tone/ambience bed** runs under the entire episode (no dead air), swapped for a
  tenser drone in interrogation/tension scenes.
- Every **wipe/transition** gets a short whoosh; every **on-screen-text reveal** a light UI tick/impact.
- Reuse-first: all cues are library tracks (reusable across episodes), auto-selected by family;
  the mix layout is generated from this sheet.

> Binding to real `MUS-*/SFX-*` IDs happens after `library/music` + `library/sfx` + `library/ambience`
> are generated and registered (rights_basis recorded per asset; decision §L/§N).
