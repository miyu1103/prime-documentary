# EP72 · LAC-MÉGANTIC — SCENE PLAN v001

**Episode `PD-2026-072-lacmegantic` · 30 minutes · authored 2026-08-21**

**Contract** `episodes/PD-2026-072-lacmegantic/episode_spec.v001.json` ·
**Design** `EP72_lacmegantic_FILM_BIBLE.v001.md` ·
**Script** `EP72_lacmegantic_script.en.v003.md` ·
**Facts** `EP72_lacmegantic_FACTS_LEDGER.v001/.v002/.v003.md` ·
**Images** `EP72_lacmegantic_CODEX_BATCH_A.v001.md` (L001–L120) ·
**Packaging** `EP72_lacmegantic_thumb_prompts.v001.md`

> **Every timestamp in this plan is MEASURED, not modelled.** They come from
> `06_audio/narration_index.v001.json`, produced from the delivered ElevenLabs master
> (`06_voice/master/vc_master_v001.mp3`, 378 chunks, 1,774.792 s, 191.7 wpm). This is the first PD
> scene plan written after the narration rather than before it, and the reason is
> `PD_ONE_PASS_PRODUCTION_SPEC.v3` §6.6: the word-count gate that sizes scripts before narration
> exists counts citation comments as speech and has been over-reporting every script since EP66.

---

## 1. THE ARITHMETIC THIS PLAN HAS TO SATISFY

| | value | where it comes from |
|---|---|---|
| finished runtime band | 1,740–1,920 s | `episode_spec.runtime_seconds` |
| **measured master** | **1,774.792 s** | narration index, ffprobe |
| **finished film** | **1,783.8 s (29:44)** | master + `ENDCARD_SEC` 9.0 |
| average cut | **3.8 s** | `episode_spec.target_cut_sec` |
| cuts at that mean | **463** | sum of the section sheet below |
| stills ceiling (32 % of cuts) | **150** | video-share floor |
| commissioned plates | **120** | the image order, L001–L120 |
| distinct video assets | **265** | `episode_spec.distinct_video_assets` |
| video cuts floor (68 %) | **319** | 265 distinct at a mean reuse of 1.20, cap 4× |

**120 ≤ 150 and 265 distinct covering 319 video cuts at 1.20× reuse.** The contract is satisfiable,
by arithmetic against the measured master rather than against a projection.

**Non-narration budget, 9.0 s exactly:** `ENDCARD_SEC` only. This film declares **no scripted
silence** — the two held beats in the design (the 12-frame hold before "What the regulator did is a
separate fact", and the 10-frame hold after "Not one hand brake…") sit inside the 1.8 s section
gaps and the 0.3 s beat gaps the narration master already contains.

---

## 2. SECTION SHEET — measured

| section | clock | dur | words | chunks | cuts | plates | light |
|---|---|---|---|---|---|---|---|
| HOOK | 0:00.0 – 0:25.3 | 25.3 s | 77 | 4 | 7 | L001–L006 (6) | A |
| OP | 0:27.1 – 1:13.1 | 46.0 s | 140 | 9 | 12 | L007–L010 (4) | A→B |
| ACT_1 | 1:14.9 – 4:10.5 | 175.6 s | 523 | 39 | 46 | L011–L030 (20) | B |
| ACT_2 | 4:12.3 – 9:19.7 | 307.4 s | 967 | 74 | 81 | L031–L055 (25) | A |
| ACT_3 | 9:21.5 – 14:02.5 | 281.0 s | 825 | 60 | 74 | L056–L085 (30) | A |
| ACT_4 | 14:04.3 – 20:36.8 | 392.5 s | 1,153 | 82 | 103 | L086–L105 (20) | B |
| ACT_5 | 20:38.6 – 27:30.6 | 412.0 s | 1,226 | 80 | 108 | L106–L120 (15) | B |
| ENDING | 27:32.4 – 29:34.8 | 122.4 s | 365 | 30 | 32 | L114/L115 held | B |
| | | **1,762.2 s** | **5,276** | **378** | **463** | **120** | |

### 2.1 Two deviations from the film bible's design targets, and what they cost

The bible modelled ACT_2 and ACT_3 at about six minutes each and ACT_5 at five and a half. Measured,
**ACT_2 is 5:07, ACT_3 is 4:41, ACT_4 is 6:33 and ACT_5 is 6:52.** The back half grew when v002 and
v003 added the trial, the federal pleas, the recommendations and the town-now material.

1. **ACT_5 is now the longest act, at the point in the film where attrition is cheapest.** The plan
   answers it by tightening the cut mean there to **3.4 s** (108 cuts over 412 s) and by putting the
   film's largest kinetic card — B4, ACQUITTED — at 26:10, inside the last third rather than at its
   end.
2. **ACT_3 is the shortest act and carries the film's centre.** It gets the *slowest* mean, 3.8 s,
   and the single longest hold in the film: the gauge, B2, seven seconds with no narration over it.
   Density is not the same thing as pace, and this is the one place the film should breathe.

---

## 3. WHAT CARRIES EACH BLOCK

Every span in the build carries four fields: `asset_type` · `motion` · `transition` ·
`search_keywords`. The defaults below apply unless a beat overrides them.

**Defaults.** `asset_type: plate` for a commissioned still; `motion: MovingImage`, scale 1.000 →
1.055 with y −18 px over 3.8 s, `Easing.out(Easing.cubic)`; `transition: crossfade 0.4 s` with the
Sequences overlapping by that length so no frame goes black and no velocity resets; `Trail` motion
blur only on beats marked fast.

| block | clock | carried by | archive registers to stage | notes |
|---|---|---|---|---|
| HOOK | 0:00–0:25 | L001–L006, one plate per line | `small_town_main_street` (night), `highway_night_long_exposure` | Push-in f0→f36 on L002. RECONSTRUCTION label up for the whole hook |
| OP | 0:27–1:13 | L007–L010 + the grade figure | — | `BrandOpening` 3.5 s lands over continuing footage at 0:27 |
| ACT_1 | 1:15–4:10 | L011–L018 (the shop), L019–L030 (the run) | `lone_tree_in_field`, `empty_road_sunset`, `soft_golden_light` **used flat, not golden** | F09 number ticker at 3:31. The polymer patch, L008, returns here as the act's hero |
| ACT_2 | 4:12–9:20 | L031–L055 | `highway_night_long_exposure`, `storm_clouds_dramatic` (texture only), `small_town_main_street` | B1 (7 / 9 / 17–26) at 6:05. The brake wheel gets three angles and none is reused inside 90 s |
| ACT_3 | 9:21–14:02 | L056–L085 | `police_car_lights_night` (distance only, no insignia), `rain_on_city_street_neon` **rejected — reads as city** | B2, the gauge, at 12:20, 7.0 s, ambient bed −6 dB, no narration |
| ACT_4 | 14:04–20:37 | L086–L105 | `foggy_forest`, `misty_mountain_valley` — **eyeball first, both skew European** | B3, the count to eighteen, at 17:05. F49, the number 47, holds 5.0 s at 14:04 |
| ACT_5 | 20:39–27:31 | L106–L120 | `small_town_main_street` (day), `lone_tree_in_field` | B4, ACQUITTED, at 26:10. Cut mean tightens to 3.4 s |
| ENDING | 27:32–29:35 | L114 then L115, held | — | 9.0 s hold on the chair with ambient motion only, then `BrandEndcard` |

### 3.1 The register problem this episode has, named before the shot list is committed

**The shelf cannot supply the rail material.** Its rail subtypes are `train_platform_night`,
`subway_train_motion_blur` and `subway_tunnel_empty` — passenger, urban, and mostly not North
American. There is no freight subtype. **Assume the entire rail register is commissioned plates plus
i2v motion derived from them**, and budget accordingly: of the 265 distinct video assets, plan for
**at least 90 to come from i2v on L001–L055** rather than from the archive.

**The signage trap is the inverse of EP71's.** Quebec is francophone. A north-European street reads
closer to Estrie than a Los Angeles freeway does, so the shelf's European bias is *less* fatal here —
but **any English-only shopfront, US route shield or EU number plate is wrong**, and
`forbidden_subjects` in the spec catches them on a filename only if the filename says so. A human
opens the contact sheet.

**Run `check_cross_episode_reuse.py` before staging.** EP68 pinto and EP69 hyatt have already spent
this shelf's industrial, engineering and emergency-light registers.

---

## 4. THE FIGURE BEATS AGAINST THE MEASURED CLOCK

`episode_spec.figure_beats_per_act` is 13–17. The bible lays out 76 figure beats, F01–F76. Placed
against the measured index they fall 13, 15, 17, 15, 15 across ACT_1 to ACT_5 — inside the band at
both edges, with the HOOK's and the ENDING's beats excluded from the per-act count as the spec
intends.

The five kinetic beats, at measured times:

| id | clock | beat | form |
|---|---|---|---|
| B1 | 6:05 | 7 applied / 9 by the railway's rule / a minimum of 17 and possibly 26 | Split-number card, staggered 6 frames, spring damping 14. **Never resolves to one number** (⛔-04) |
| B2 | 12:20 | the compressor stops | Gauge needle, 7.0 s, −4° → −38°, `Easing.inOut(Easing.quad)`, bed −6 dB |
| B3 | 17:05 | eighteen | Count-up 1→18 over 24 frames, each factor a line that does not stay |
| B4 | 26:10 | acquitted | Three blank name-plates rise; ACQUITTED masks up beneath all three; 4.0 s. **The film's largest card** (⛔-01) |
| B5 | 29:12 | the empty chair | No typography. 9.0 s hold, ambient motion only |

---

## 5. WHAT MUST BE TRUE BEFORE THIS PLAN BECOMES A BUILD

1. `check_cross_episode_reuse.py --build` is current, and staging excludes clips already burned in
   EP68 and EP69.
2. A labelled contact sheet of the **rail**, **yard-at-night**, **wreck-site** and **town-now**
   registers has been opened by a person. `footage_review_required` is `true`.
3. The 120 plates exist at **3,840 px long edge** and carry per-plate verdicts bound to their
   sha256. Codex's generator is capped at 1672×941 (measured 2026-08-20); the sanctioned route to
   3840 is the Real-ESRGAN x4 → LANCZOS pass proven on EP71 the same day.
4. `preflight_render_gate.py --ep PD-2026-072-lacmegantic` is **GREEN**. It has failed on 25 of 32
   episodes and been overridden on 10 of them; this episode does not get rendered behind a BLOCK.
5. The four items in `01_research/fact_recheck.v001.md` §2 are resolved — in particular that no
   figure card carries a minute for the 911 call, and that the acquittal appears wherever any of the
   three men is described **in the built `film.json`**, not merely in the script.
