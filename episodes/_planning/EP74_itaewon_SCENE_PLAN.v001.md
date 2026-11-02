# EP74 · ITAEWON — SCENE PLAN v001

**Episode `PD-2026-074-itaewon` · 30 minutes · authored 2026-08-21**

**Contract** `episodes/PD-2026-074-itaewon/episode_spec.v001.json` ·
**Design** `EP74_itaewon_FILM_BIBLE.v001.md` ·
**Script** `EP74_itaewon_script.en.v004.md` ·
**Facts** `EP74_itaewon_FACTS_LEDGER.v001/.v002/.v003.md` ·
**Images** `EP74_itaewon_CODEX_BATCH_A.v001.md` (I001–I120) ·
**Packaging** `EP74_itaewon_thumb_prompts.v001.md`

> **Every timestamp in this plan is PROJECTED, and says so.** EP72's plan was the first written
> *after* the narration master, from `narration_index`. EP74 has **no master yet**, and deliberately:
> `AB-02` is unresolved, and if the Seoul High Court judgment surfaces, ACT_5 is rewritten and any
> master generated now is thrown away with it.
>
> What the projection rests on is **not** a model. `--measure-section ACT_1` generated 49 chunks /
> 734 words and ffprobed **222.025 s = 198.4 raw wpm** — this episode's own voice at its own
> settings. Every duration below is that measured rate applied to the v004 dry run's real per-section
> word and chunk counts. **ACT_1's row is a measurement, not a projection**; the other seven are the
> measurement extended.
>
> **A v002 written from `06_audio/narration_index.v001.json` supersedes this file entirely** once the
> master exists. Nothing downstream may treat a clock time here as final.

---

## 1. THE ARITHMETIC THIS PLAN HAS TO SATISFY

| | value | where it comes from |
|---|---|---|
| finished runtime band | 1,740–1,920 s | `episode_spec.runtime_seconds` |
| narration words | **5,511** | v004 dry run, 327 chunks |
| measured rate | **198.4 raw wpm** | `--measure-section ACT_1`, ffprobe |
| projected master | **1,776.7 s** | 1,666.6 s speech + 326 beat gaps @0.30 + 7 section gaps @1.8 |
| **projected film** | **1,785.7 s (29:45)** | master + `ENDCARD_SEC` 9.0 |
| average cut | **3.8 s** | `episode_spec.target_cut_sec` |
| cuts at that mean | **468** | sum of the section sheet below |
| stills ceiling (32 % of cuts) | **149** | video-share floor |
| commissioned plates | **120** | the image order, I001–I120 |
| distinct video assets | **265** | `episode_spec.distinct_video_assets` |
| video cuts floor (68 %) | **318** | 265 distinct covering 318 cuts = **1.20× mean reuse**, cap 4 |

**120 ≤ 149, and 265 distinct assets cover 318 video cuts at 1.20× mean reuse.** The contract is
satisfiable by arithmetic, at the measured rate.

**Non-narration budget, 10.5 s:** `ENDCARD_SEC` 9.0, plus the film's **one designed silence** — the
1.5 s of black in ACT_5 before "here this film stops". It is declared here because the narration
registry does not carry it, and a hold that exists only in a direction block is a hold that does not
survive extraction (the EP69 failure).

---

## 2. SECTION SHEET — words and chunks measured, clock projected

| section | clock | dur | words | chunks | cuts | mean cut | plates | light |
|---|---|---|---|---|---|---|---|---|
| HOOK | 0:00.0 – 0:23.7 | 23.7 s | 72 | 4 | 6 | 3.9 s | I001, I007, I052, I054, I014 | A |
| OP | 0:23.7 – 1:43.8 | 80.1 s | 248 | 12 | 21 | 3.8 s | I002, I003, I005, I015 | A |
| ACT_1 | 1:43.8 – 5:42.0 | **238.2 s** | **734** | **49** | 63 | 3.8 s | I001–I034 | B→A |
| ACT_2 | 5:42.0 – 9:23.2 | 221.2 s | 679 | 48 | 58 | 3.8 s | I035–I062, I071–I080 | A |
| ACT_3 | 9:23.2 – 14:53.3 | 330.1 s | 1,024 | 63 | 87 | 3.8 s | I016–I024, I061, I062, I097–I104 | A→B |
| ACT_4 | 14:53.3 – 17:58.0 | 184.7 s | 568 | 38 | 49 | 3.8 s | I071–I080, I092, I097 | A/B |
| ACT_5 | 17:58.0 – 25:26.0 | **448.0 s** | **1,406** | **71** | 118 | **3.4 s** | I081–I104 | B |
| ENDING | 25:26.0 – 29:36.0 | **250.0 s** | **780** | **42** | 66 | 3.8 s | I105–I120 | A/B |
| ENDCARD | 29:36.0 – 29:45.0 | 9.0 s | — | — | 1 | — | — | — |
| **total** | | **1,785.7 s** | **5,511** | **327** | **468** | **3.8 s** | **120** | |

**Mean shot 3.8 s against a ceiling of 6.0 s.** ACT_5 tightens to 3.4 s — 118 cuts over 448 s — for
the same reason EP72 did it: that is the point in a 30-minute film where attrition is cheapest, and
it carries the payoff.

---

## 2.5 ⚠️ WHAT THE MEASUREMENT FOUND, AND IT IS A DEFECT

**The bible planned a one-minute ending. The script has a four-minute-ten one.**

| section | bible §4 | measured | delta |
|---|---|---|---|
| ACT_2 | 6:30 | 3:41 | **−2:49** |
| ACT_4 | 6:30 | 3:05 | **−3:25** |
| ACT_5 | 5:30 | 7:28 | **+1:58** |
| ENDING | 1:00 | **4:10** | **+3:10** |

The cause is traceable and it is mine: every research region added in ledger v002 and v003 — the
909 cameras, the statute, the enforcement decree, the penalty bill — was written into whichever
section it thematically touched, and they all touched the present day, so they all landed in
`ENDING`. **Four minutes is not an ending. It is an act wearing an ending's label**, and
`structure_4part` and `retention_cadence` both read section names.

**The fix, specified rather than performed.** Two block moves, both with exact anchors in
`script.en.v004`:

1. **The minister block → ACT_4.** From "The first was the Constitutional Court." to "They are about
   the same night." (≈300 words). ACT_4 is *where the state examines itself*, and the Constitutional
   Court's "not significantly deficient" belongs beside the audit that contradicts it.
   ACT_4 → ≈4:40, ACT_5 → ≈5:55.
2. **The statute and decree block → ACT_5.** From "The act says who has to write the plan." to
   "…and who is responsible." (≈380 words), plus the penalty-bill block. ACT_5 → ≈7:55,
   ENDING → ≈2:10, which is an ending.

**This is a design change, not a text move**, and that is why this plan specifies it instead of doing
it: it invalidates the bible's §6 beat map for ACT_4 and ACT_5, its §7 retention map, and the timing
of AE beats 4 and 5. It needs **FILM_BIBLE v002 + script v005**, then this plan is re-measured.
**Do it before the narration master, not after.**

---

## 3. WHAT CARRIES EACH BLOCK

Every span in the build carries four fields: `asset_type` · `motion` · `transition` ·
`search_keywords`.

**Defaults.** `asset_type: plate` for a commissioned still. `motion: MovingImage`, scale 1.000 →
1.055 with y 0 → −18 px over 3.8 s, `Easing.out(Easing.cubic)`. `transition: crossfade 0.4 s`, the
Sequences overlapping by that length so no frame goes black and no velocity resets at a cut.
`Trail` motion blur only on spans marked **fast**. No span holds a still longer than 2.0 s without
motion, and no span uses a naked hard cut.

| block | clock | carried by | archive registers to stage | notes |
|---|---|---|---|---|
| HOOK | 0:00–0:24 | I001 → I052 → I054 → I014 → I007 | `narrow_alley_night`, `phone_screen_hand_dark`, `wet_asphalt_reflection_night` | Push-in f0→f36 on I001, scale 1.06→1.00. Trail 6 layers to f18. **fast.** No crowd yet |
| OP | 0:24–1:44 | I002, I003, I005, I015 + the width-line figure | `city_street_plan_topdown` — **reject anything with legible labels** | `BrandOpening` 3.5 s over continuing footage at 0:24. Width line draws f0→f45 |
| ACT_1 | 1:44–5:42 | I001–I006 (empty), I025–I034 (hotel), I007–I015 (dusk fill) | `korean_street_night_neon`, `roller_shutter_shopfront`, `air_conditioner_wall_units`, `granite_kerb_wet` | **HERO: the width line completes to 3.2, held longest in the act.** Slope draws f0→f60 with **no numeral** (AB-01) |
| ACT_2 | 5:42–9:23 | the call-log figure (Remotion) over I023, I035–I046, I071–I080 | `crowd_walking_night_motion_blur`, `police_hi_vis_distance`, `torch_beam_wall_night` | **HERO: the log.** Four rows fill (8 f, stagger 4 f); **seven stay outline-only, 1 px, 42 %.** AE beats 1–3 land at ≈8:35, ≈8:45, ≈9:00 |
| ACT_3 | 9:23–14:53 | I016–I024, I097–I104, the density figure (Remotion) | `empty_alley_dawn`, `street_cleaning_hose`, `medical_folder_blank` — **no crowd stock at all in this act** | **The film's only light change, A→B, lands here on the empty alley.** "159" holds 5.0 s, the longest card in the film. **⛔-02 is enforced by the plan itself: the archive registers staged here contain no people** |
| ACT_4 | 14:53–17:58 | the Yongsan map (Remotion), I071–I080, I092, I097 | `city_map_dark_abstract`, `government_building_exterior_angle` — **eyeball first, most skew Western** | **HERO: the map.** Pins drop f0→f21, 9 f apart. AE beats 4–5 at ≈15:10 and ≈16:40 |
| ACT_5 | 17:58–25:26 | I081–I096 (rooms), I097–I104 (blanks) | `corridor_institutional`, `files_stacked`, `empty_chairs_row` — **no courtroom, no gavel** | Cut mean tightens to **3.4 s**. The largest quote card in the film — the acquittal's reason — at ≈22:30, held 6.0 s. **The 1.5 s designed silence sits at ≈24:10** |
| ENDING | 25:26–29:36 | I105–I120 | `pedestrian_barrier_street`, `cctv_camera_pole`, `korean_street_evening_calm` | **HERO: the barrier**, low in frame. I119 (flowers) is used **once**, 2.5 s, and never as a thumbnail. BGM resolves on a cadence, not a cut |
| ENDCARD | 29:36–29:45 | `BrandEndcard` | — | 9.0 s, imported, never forked |

---

## 4. THE RULES THIS PLAN ENFORCES THAT NO GATE MEASURES

1. **ACT_3 stages no footage containing people.** Not a preference — a plan-level constraint, because
   ⛔-02 is the one failure the channel cannot recover from and the archive's labels are known to be
   wrong (`pd-factory-shelf-mislabeled`).
2. **No clip runs more than 3×**, against a spec cap of 4, so `asset_reuse` has headroom. 265
   distinct over 318 video cuts is 1.20× mean.
3. **No plate reappears inside 90 s.** The alley has 24 plates precisely so that the film can return
   to it constantly without the viewer seeing the same frame twice.
4. **Every span whose narration names an outlet gets an on-screen attribution card**, not a
   voice-only credit (⛔-11): SCMP at ≈6:10, Al Jazeera at ≈7:20 and ≈15:05, the Korea Times at
   ≈2:50 and ≈16:20, PLOS One at ≈2:20 and ≈10:15, MBC at ≈24:00, the Korea Law Information Center
   at ≈27:00.
5. **The width line and the slope line are the only two recurring graphics.** They return silent, at
   ≈8:55, ≈9:40 and ≈22:45, with no numeral on the slope, ever.

## 5. WHAT HAS TO HAPPEN BEFORE A RENDER IS STARTED

1. **Resolve `AB-02`.** Everything else is downstream of it.
2. **FILM_BIBLE v002 + script v005** — the two block moves in §2.5.
3. Narration master, then **SCENE_PLAN v002 measured from `narration_index`**, superseding this file.
4. Codex generates I001–I120; labelled contact sheet opened **by a person**; verdicts recorded in
   `runs/qc/itaewon_plate_verdicts.v001.json`.
5. `preflight_render_gate.py --ep PD-2026-074-itaewon` **must be GREEN.** It is not advisory: 25 of
   32 episodes failed it and 10 rendered anyway, and on 2026-08-20 EP70 and EP71 were three GPU-hours
   from a captionless slideshow.
