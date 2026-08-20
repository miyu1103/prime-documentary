# EP74 · ITAEWON — SCENE PLAN v002

**Episode `PD-2026-074-itaewon` · authored 2026-08-21 · supersedes v001 entirely**

**Contract** `episodes/PD-2026-074-itaewon/episode_spec.v001.json` ·
**Design** `EP74_itaewon_FILM_BIBLE.v002.md` (amends v001 §4, §6, §7, §8, §12.5; all other sections
of v001 stand) · **Script** `EP74_itaewon_script.en.v005.md` ·
**Facts** `EP74_itaewon_FACTS_LEDGER.v001`–`.v004.md` ·
**Images** `EP74_itaewon_CODEX_BATCH_A.v001.md` (I001–I120) ·
**Packaging** `EP74_itaewon_thumb_prompts.v001.md`

**Why v002.** v001 §2.5 measured the acts and found ENDING at **4:10** against a designed 1:00.
That defect is fixed in script v005 and **ENDING is now 2:02**. In the same pass `AB-02` resolved —
both appeals were suspended rather than undecided — and ACT_5 gained the film's recognition.

> **Timestamps are still PROJECTED, and still say so.** No narration master exists. What they rest
> on is measured: `--measure-section ACT_1` ffprobed **222.025 s over 734 words = 198.4 raw wpm**,
> this episode's own voice at its own settings, applied to the v005 dry run's real per-section word
> and chunk counts. **A v003 written from `06_audio/narration_index.v001.json` supersedes this file
> entirely** once the master exists. Nothing downstream may treat a clock here as final.
>
> Clocks below are accurate to about ±4 s, the difference between per-section and whole-film gap
> accounting.

---

## 1. THE ARITHMETIC

| | value | source |
|---|---|---|
| finished runtime band | 1,740–1,920 s | `episode_spec.runtime_seconds` |
| narration words | **5,711** | v005 dry run, 341 chunks |
| measured rate | **198.4 raw wpm** | `--measure-section ACT_1`, ffprobe |
| speech | 1,727.1 s | 5,711 / 198.4 × 60 |
| gaps | 114.6 s | 340 beat gaps @0.30 + 7 section gaps @1.8 |
| projected master | **1,841.7 s** | |
| **projected film** | **1,850.7 s (30:51)** | master + `ENDCARD_SEC` 9.0 |
| **tolerance** | **in band down to 192 wpm** | at 192 the film is 1,908 s; at 195, 1,881 s |
| cut mean | **3.61 s** overall — 3.8 s everywhere, **3.2 s in ACT_5** | `episode_spec.target_cut_sec` 3.8, tightened per bible §4.5 |
| cuts | **510** | section sheet below |
| stills ceiling (32 %) | **164** | video-share floor |
| commissioned plates | **120** | I001–I120 — 44 under the ceiling |
| distinct video assets | **265** | `episode_spec` |
| video cuts floor (68 %) | **348** | 265 distinct at **1.31× mean reuse**, cap 4 |

**Non-narration budget, 10.5 s:** `ENDCARD_SEC` 9.0 plus the film's one designed silence — the 1.5 s
of black in ACT_5 before "And then, in the summer of 2025, both appeals stopped." Declared here
because the narration registry does not carry it and a hold that exists only in a direction block
does not survive extraction.

---

## 2. SECTION SHEET

| section | clock | dur | words | chunks | cuts | mean | plates | light |
|---|---|---|---|---|---|---|---|---|
| HOOK | 0:00 – 0:24 | 24 s | 72 | 4 | 6 | 3.8 s | I001, I052, I054, I014, I007 | A |
| OP | 0:24 – 1:44 | 80 s | 248 | 12 | 21 | 3.8 s | I002, I003, I005, I015 | A |
| ACT_1 | 1:44 – 5:58 | 254 s | 782 | 54 | 67 | 3.8 s | I001–I034, I055–I059 | B→A |
| ACT_2 | 5:58 – 9:34 | 216 s | 664 | 47 | 57 | 3.8 s | I035–I051, I071–I080 | A |
| ACT_3 | 9:34 – 14:51 | 317 s | 983 | 61 | 83 | 3.8 s | I016–I024, I061, I062, I097–I104 | A→B |
| ACT_4 | 14:51 – 19:33 | 282 s | 874 | 57 | 74 | 3.8 s | I071–I080, I087–I096 | A/B |
| ACT_5 | 19:33 – 28:36 | **543 s** | **1,709** | **85** | **170** | **3.2 s** | I081–I104 | B |
| ENDING | 28:36 – 30:38 | 122 s | 379 | 21 | 32 | 3.8 s | I105–I120 | A/B |
| ENDCARD | 30:38 – 30:47 | 9 s | — | — | 1 | — | — | — |
| **total** | | **1,850.7 s** | **5,711** | **341** | **510** | **3.61 s** | **120** | |

**Mean shot 3.61 s against a ceiling of 6.0 s.** No section exceeds 3.8.

**The one structural debt, carried forward from bible §4.5:** ACT_5 is 9:03, 29 % of the film in one
section. Accepted, not fixed, and answered with pace — a 3.2 s cut mean and three of the film's six
AE beats. The split point, if a later reader disagrees, is after the decree, and it costs a spec
revision because `section_vocabulary` declares eight sections.

**What v001 got wrong, for the record.** v001's sheet had ACT_2 at 3:41, ACT_4 at 3:05, ACT_5 at
7:28 and ENDING at 4:10. v002's sheet is the same film with the blocks in the right containers:
ACT_4 gains the minister and the 2026 testimony, ACT_5 gains the decree and the stopping, ENDING
loses everything that was not an ending.

---

## 3. WHAT CARRIES EACH BLOCK

Every span carries `asset_type` · `motion` · `transition` · `search_keywords`.

**Defaults.** `asset_type: plate` for a commissioned still. `motion: MovingImage`, scale 1.000 →
1.055, y 0 → −18 px over 3.8 s, `Easing.out(Easing.cubic)`. `transition: crossfade 0.4 s`, Sequences
overlapping by that length so no frame goes black and no velocity resets. `Trail` only on spans
marked **fast**. No still held over 2.0 s without motion. No naked hard cut anywhere.

| block | clock | carried by | archive registers to stage | notes |
|---|---|---|---|---|
| HOOK | 0:00–0:24 | I001 → I052 → I054 → I014 → I007 | `narrow_alley_night`, `phone_screen_hand_dark`, `wet_asphalt_reflection_night` | Push-in f0→f36 on I001. Trail 6 layers to f18. **fast.** No crowd yet |
| OP | 0:24–1:44 | I002, I003, I005, I015 + the width-line figure | `city_street_plan_topdown` — reject anything with legible labels | `BrandOpening` 3.5 s at 0:24. Width line draws f0→f45 |
| ACT_1 | 1:44–5:58 | I001–I006, I025–I034, then I055–I059 for the count | `korean_street_night_neon`, `roller_shutter_shopfront`, `subway_ticket_gates_crowd`, `escalator_crowd_behind` | **HERO: the width line to 3.2.** Slope draws with **no numeral**. **AE beat 3 (81,573 → 31,878) at 4:20**, ticker on the hourly curve |
| ACT_2 | 5:58–9:34 | the call-log figure over I023, I035–I051, I071–I080 | `crowd_walking_night_motion_blur`, `police_hi_vis_distance`, `torch_beam_wall_night` | **HERO: the log.** Four rows fill; **seven stay outline-only, 1 px, 42 %.** AE beats 1–2 at 8:05 and 8:15 |
| ACT_3 | 9:34–14:51 | I016–I024, I097–I104, the density figure | `empty_alley_dawn`, `street_cleaning_hose`, `medical_folder_blank` — **no crowd stock at all in this act** | **The film's only light change, A→B, lands here on the empty alley.** "159" holds 5.0 s. **⛔-02 is enforced by the plan: nothing staged here contains people** |
| ACT_4 | 14:51–19:33 | the Yongsan map, I071–I080, then I087–I096 for the court and the hearing | `city_map_dark_abstract`, `government_building_exterior_angle`, `conference_room_empty_chairs` | **HERO: the map.** AE beats 4–5 at 15:10 and 17:20. **The Constitutional Court quote card at 18:40 is cut directly against the audit card at 17:50 — same framing, same size, two years apart.** The hearing block at 19:10 uses a nameplate turned away, blank |
| ACT_5 | 19:33–28:36 | I081–I096 (rooms), I097–I104 (blanks) | `corridor_institutional`, `files_stacked`, `empty_chairs_row` — **no courtroom, no gavel** | Cut mean **3.2 s**. Largest quote card — the acquittal's reason — at 23:00, held 6.0 s. Second-largest — Article 66-11 — at 25:30, held 6.0 s. **The 1.5 s designed silence at 26:55. AE beat 6, STOPPED, at 27:00** |
| ENDING | 28:36–30:38 | I105–I120 | `pedestrian_barrier_street`, `cctv_camera_pole`, `korean_street_evening_calm` | **HERO: the barrier**, low in frame. I119 (flowers) used **once**, 2.5 s, never as a thumbnail. BGM resolves on a cadence, not a cut |
| ENDCARD | 30:38–30:47 | `BrandEndcard` | — | 9.0 s, imported, never forked |

---

## 4. THE RULES THIS PLAN ENFORCES THAT NO GATE MEASURES

1. **ACT_3 stages no footage containing people.** A plan-level constraint, because ⛔-02 is the one
   failure the channel cannot recover from and the shelf's labels are known to be wrong.
2. **No clip runs more than 3×**, against a spec cap of 4. 265 distinct over 348 video cuts is 1.31×.
3. **No plate reappears inside 90 s.** The alley has 24 plates so the film can return to it
   constantly without the viewer seeing the same frame twice.
4. **Every span whose narration names an outlet gets an on-screen attribution card** (⛔-11): PLOS One
   at 2:20 and 10:15, the Korea Times at 2:50 and 17:50, SCMP at 6:25, Al Jazeera at 7:40 and 15:10,
   Seoul Transportation Corporation at 4:20, the Constitutional Court at 18:40, MBC at 26:30, the
   Seoul High Court at 27:10, the Korea Law Information Center at 25:30.
5. **The width line and the slope line are the only recurring graphics**, returning silent at 9:20,
   10:00 and 23:15, with no numeral on the slope, ever.
6. **`⛔-16` is a cutting instruction as well as a writing one.** Under Lee Im-jae's 2026 testimony
   the picture stays on the empty hearing room and the blank nameplate. **No cut to the map, no cut
   to the presidential office, nothing that stages his counterfactual as the film's conclusion.**

## 5. WHAT HAS TO HAPPEN BEFORE A RENDER IS STARTED

1. ~~Resolve `AB-02`~~ — **done**, ledger v004. It is no longer a blocker.
2. ~~FILM_BIBLE v002 + script v005~~ — **done**.
3. Narration master, then **SCENE_PLAN v003 measured from `narration_index`**, superseding this file.
4. Codex generates I001–I120; labelled contact sheet opened **by a person**; verdicts recorded in
   `runs/qc/itaewon_plate_verdicts.v001.json`.
5. `preflight_render_gate.py --ep PD-2026-074-itaewon` **must be GREEN.** Not advisory: 25 of 32
   episodes failed it and 10 rendered anyway.
6. **`AB-11` re-checked on the day of publish**: whether either suspended appeal has restarted.
