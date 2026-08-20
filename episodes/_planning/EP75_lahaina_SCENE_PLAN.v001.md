# EP75 · LAHAINA — SCENE PLAN v001

**Episode `PD-2026-075-lahaina` · 30 minutes · authored 2026-08-21**

**Contract** `episodes/PD-2026-075-lahaina/episode_spec.v001.json` ·
**Design** `EP75_lahaina_FILM_BIBLE.v001.md` ·
**Script** `EP75_lahaina_script.en.v001.md` ·
**Facts** `EP75_lahaina_FACTS_LEDGER.v001.md` + `.v002.md` ·
**Images** `EP75_lahaina_CODEX_BATCH_A.v001.md` (H001–H132) ·
**Packaging** `EP75_lahaina_thumb_prompts.v001.md`

> **⚠ Every timestamp in this plan is PROJECTED, not measured, and that is the one way it differs
> from EP72's.** EP72's scene plan was written *after* its ElevenLabs master existed and its clock
> came from `06_audio/narration_index.v001.json`. **This episode has no master yet.** What it has is
> a real measurement of one section — `--measure-section ACT_1`, 54 chunks, 808 words, ffprobed
> 259.133 s, **187.1 raw wpm** — and the rest of the clock is that rate applied to the script.
>
> **Re-derive §2 from `narration_index.v001.json` the moment the master exists.** Do not build a
> `film.json` against the numbers below without doing that first. They are good enough to prove the
> contract is satisfiable and to place the kinetic beats; they are not good enough to cut to.

---

## 1. THE ARITHMETIC THIS PLAN HAS TO SATISFY

| | value | where it comes from |
|---|---|---|
| finished runtime band | 1,740–1,920 s | `episode_spec.runtime_seconds` |
| measured pace | **187.1 raw wpm** | `--measure-section ACT_1`, 2026-08-21, ffprobe |
| script, as the TTS extractor reads it | **5,321 words / 349 chunks** | `gen_narration_case.py --dry-run` |
| **projected master** | **≈1,823 s** | 1,706.4 s speech + 117.0 s gaps |
| **projected film** | **≈1,832 s (30:32)** | master + `ENDCARD_SEC` 9.0 |
| average cut | **3.8 s** | `episode_spec.target_cut_sec` |
| cuts at that mean | **≈481** | the section sheet below |
| stills ceiling (32 % of cuts) | **154** | video-share floor |
| commissioned plates | **132** | the image order, H001–H132 |
| distinct video assets | **265** | `episode_spec.distinct_video_assets` |
| video cuts floor (68 %) | **327** | 265 distinct at a mean reuse of **1.23×**, cap 4× |

**132 ≤ 154, and 265 distinct assets cover 327 video cuts at 1.23× reuse.** The contract is
satisfiable with room at both edges.

**Non-narration budget, 9.0 s exactly:** `ENDCARD_SEC` only. **This film declares no scripted
silence.** The held beats in the design — the 4.0 s hold on 16:16, the 3.8 s hold on the gate, the
9.0 s hold on the blank form — sit inside the 1.8 s section gaps and the 0.3 s beat gaps the master
already contains, exactly as EP72's did.

---

## 2. SECTION SHEET — projected

| section | clock | dur | words | cuts | plates | light |
|---|---|---|---|---|---|---|
| HOOK | 0:00.0 – 0:24.0 | 24.0 s | 72 | 6 | H001–H008 (8) | W→S |
| OP | 0:25.8 – 1:06.7 | 40.9 s | 123 | 11 | H009–H014 (6) | O |
| ACT_1 | 1:08.5 – 5:45.4 | 276.9 s | 812 | 73 | H015–H038 (24) | O→W |
| ACT_2 | 5:47.2 – 10:17.0 | 269.8 s | 788 | 71 | H039–H064 (26) | N→W |
| ACT_3 | 10:18.8 – 16:00.7 | 341.8 s | 1,008 | 90 | H065–H088 (24) | W→S |
| ACT_4 | 16:02.5 – 22:30.7 | 388.2 s | 1,146 | 102 | H089–H110 (22) | S→O |
| ACT_5 | 22:32.5 – 27:55.5 | 323.0 s | 953 | 85 | H111–H128 (18) | O |
| ENDING | 27:57.3 – 30:39.5 | 162.2 s | 472 | 43 | H129–H132 (4) | O |
| | | **≈1,840 s** | **5,374** | **481** | **132** | |

**The word total here is 5,374 and the runner's is 5,321 — a 1.0 % difference**, because this sheet
counts with its own tokenizer and the runner counts what its chunk extractor will actually speak.
**The runner's figure is authoritative.** Treat every clock in this table as ±1 %, which at the end
of the film is about eighteen seconds.

### 2.1 Three things the shape of this sheet says, and what the plan does about each

1. **ACT_4 is the longest act (6:28) and it sits at 16:02 — past the halfway line.** That is the
   cheapest place in a film to lose people. The plan answers it the way EP72 did: **tighten the cut
   mean in ACT_4 to 3.4 s** (102 cuts over 388 s stays a 3.8 s mean; going to 3.4 s buys ~114 cuts)
   and put the act's hardest physical beat — the padlocked gate, H093–H099 — at **21:00**, inside the
   last third rather than at its end.
2. **ACT_3 carries the film's centre and is not the longest act.** It gets the *slowest* handling:
   the B2 clock stack builds across the whole act, and **16:16 (B3) holds 4.0 s with the left column
   dimmed to 25 %** — the single longest typographic hold in the film. Density is not pace, and this
   is the one place the film should stop.
3. **The ENDING is 2:42, which is long for an ending, and deliberately.** It is where the film makes
   its argument rather than summarising. The last 9.0 s carry **no typography at all** — H129 held
   with ambient motion only — and the BGM resolves on a phrase without the runtime being extended for
   it (`feedback_pd_craft_directives`).

---

## 3. WHAT CARRIES EACH BLOCK

Every span in the build carries four fields: `asset_type` · `motion` · `transition` ·
`search_keywords`. The defaults below apply unless a beat overrides them.

**Defaults.** `asset_type: plate` for a commissioned still; `motion: MovingImage`, scale 1.000 →
1.055 with y −18 px over 3.8 s, `Easing.out(Easing.cubic)`; `transition: crossfade 0.4 s` with the
Sequences overlapping by that length so no frame goes black and no velocity resets; `Trail` motion
blur only on beats marked fast. `depth` maps on ≥40 % of stills (`feedback_perceptual_motion_and_verify`).

| block | clock | carried by | archive registers to stage | notes |
|---|---|---|---|---|
| HOOK | 0:00–0:24 | H001–H008, roughly one plate per line | `dry_grass_field_wind`, `wildfire_smoke_ridge` — **eyeball both** | Push-in f0→f36 on H001, Trail 6 layers to f18. RECONSTRUCTION label up for the whole hook |
| OP | 0:26–1:07 | H009–H014 | — | `BrandOpening` 3.5 s lands over continuing footage at 0:24. The word *siren* is first spoken at 1:08, not before |
| ACT_1 | 1:08–5:45 | H015–H021 (the hardware and the monthly test), H022–H038 (the town and the forecast) | `dry_grass_field_wind`, `storm_clouds_dramatic` **texture only**, `weather_radar_screen` — **reject anything with legible numerals** | **B1 at 1:35**: four identical framings of the pole cut on 11 frames. F10, the "notice was rare" quote card, at 4:05 |
| ACT_2 | 5:47–10:17 | H039–H050 (before dawn and the morning fire), H051–H064 (the roads, the phones, 14:17) | `power_lines_silhouette`, `utility_pole_repair`, `empty_road_sunset` **used flat, never golden** | F30, the 14:17 clock card, closes the act. The phone, H062, is seeded here and detonates in ACT_3 |
| ACT_3 | 10:19–16:01 | H065–H088 | `wildfire_smoke_ridge`, `smoke_over_road` — **no flame in any staged clip**, no orange grade | **B2 builds across the act. B3 (16:16) at ~14:40, 4.0 s, the film's largest card.** F43, the 15:37 radio quote, at ~13:10 with the bed −6 dB |
| ACT_4 | 16:02–22:31 | H089–H102 (the roads and the gate), H103–H110 (the water and the utility) | `chain_link_fence`, `fire_hydrant_street`, `water_main_trench` — **all three unverified on the shelf, eyeball first** | **B4 (eight ticks to six) at ~18:40.** Cut mean tightens to 3.4 s. The gate sequence H093–H099 runs unbroken at 21:00 |
| ACT_5 | 22:33–27:56 | H111–H117 (the investigation), H118–H128 (the findings and the record) | `office_corridor_empty`, `filing_cabinets`, `server_room_lights` | H118 returns the ACT_1 pole in the identical framing under colder light — **the one deliberate repeat in the film**, and it must read as a repeat |
| ENDING | 27:57–30:40 | H129 held, then H130–H132 | `small_town_street_day` (rebuilt, present day) | **B5: 9.0 s on H129 with no typography**, then `BrandEndcard` |

### 3.1 The register problem this episode has, named before the shot list is committed

**The shelf will offer holiday footage for every query in this film.** Maui is one of the most
photographed holiday destinations on earth and the spec carries 65 `forbidden_subjects`, 25 of them
in the holiday family. `footage_review_required` is `true`. **A labelled contact sheet is opened by a
person before any clip enters a cut** — the factory shelf's labels are known to be wrong
(`pd-factory-shelf-mislabeled`), and "grassland" is exactly the kind of label that returns prairie,
savannah or a cartoon.

**Four registers the shelf probably cannot supply, and which should be assumed commissioned + i2v:**

| register | why the shelf fails | plan |
|---|---|---|
| Outdoor warning sirens | no subtype exists on the shelf at all | **entirely commissioned** — H009–H021, and i2v for any movement |
| Non-native dry grass on a leeward Pacific slope | "grassland" returns prairie, savannah and conifer edge | commissioned + heavily filtered archive, eyeballed |
| A Pacific plantation-era town street | every offered street is mainland US, European or Asian | commissioned; **a mainland main street is the single most likely wrong clip** |
| Grey wind-driven smoke with no flame and no people | fire footage is orange, close, and usually has people in it | commissioned; **no archive fire clip enters this film** |

Of the 265 distinct video assets, **plan for at least 100 to come from i2v on H001–H088** rather
than from the archive.

**Run `check_cross_episode_reuse.py` BEFORE staging, not after.** It identifies by content, not by
filename, so a renamed clip is still caught. EP68 pinto and EP69 hyatt have already spent this
shelf's industrial, engineering and emergency-light registers.

---

## 4. THE FIGURE BEATS AGAINST THE PROJECTED CLOCK

`episode_spec.figure_beats_per_act` is **13–17**. The bible lays out **77 figure beats, F01–F79**
(F-numbers are not contiguous by design; the HOOK's and ENDING's beats are excluded from the per-act
count as the spec intends). Placed against this sheet they fall:

| act | beats | inside 13–17 |
|---|---|---|
| ACT_1 | 14 | ✓ |
| ACT_2 | 16 | ✓ |
| ACT_3 | 17 | ✓ (at the ceiling — do not add one) |
| ACT_4 | 15 | ✓ |
| ACT_5 | 16 | ✓ |

The five kinetic beats, at projected times:

| id | clock | beat | form |
|---|---|---|---|
| B1 | ~1:35 | the monthly test | Four identical framings of the pole cut on 11 frames, light changing; FIRST BUSINESS DAY masks up under the fourth, holds 1.6 s |
| B2 | 11:00–15:00 | the clock | 14:55 / 14:57 / 15:00 / 15:05 / 15:21 / 15:23 / 15:37 stack, each masking up 34 px, 2 frames apart, earlier entries dimming to 40 % but never leaving frame |
| B3 | ~14:40 | **16:16** | The B2 stack still on screen. 16:16 lands **alone, right, at 2.2× scale**; the left column dims to 25 %. 4.0 s. **The film's largest card** |
| B4 | ~18:40 | eight to six | Eight ticks; two extinguish 6 frames apart; the six re-centre, `spring({damping: 14})` |
| B5 | ~30:30 | the blank form | No typography. 9.0 s hold, ambient motion only, then the endcard |

**B2 and B3 are one instrument, not two.** B3 only lands if B2 has been building for four minutes, so
the stack may not be dropped for pacing and re-introduced — it stays on screen, dimmed, across the
whole of ACT_3's middle.

---

## 5. WHAT MUST BE TRUE BEFORE THIS PLAN BECOMES A BUILD

1. **The narration master exists and §2 has been re-derived from `narration_index.v001.json`.**
   Everything above is a projection off one measured section. This is the first item for a reason.
2. `check_cross_episode_reuse.py` is current, and staging excludes clips already burned into EP68 and
   EP69.
3. A labelled contact sheet of the **dry-grass**, **smoke**, **street** and **chain-link/industrial**
   registers has been opened by a person. `footage_review_required` is `true`.
4. The **132 plates exist at 3,840 px long edge** and carry per-plate verdicts bound to their sha256.
   Codex's generator is capped at 1672×941; the sanctioned route to 3840 is the Real-ESRGAN x4 →
   LANCZOS pass. **A recorded REJECT that is still in a cut is now a ship blocker**
   (`pd_ship_policy.plate_verdict_rows`).
5. `preflight_render_gate.py --ep PD-2026-075-lahaina` is **GREEN**. It has failed on 25 of 32
   episodes and been overridden on 10 of them. **This episode does not get rendered behind a BLOCK.**
6. The items in `01_research/fact_recheck.v001.md` are resolved — in particular that **§10 of the
   ledger was re-verified on the day the build is packaged**, not merely on the day the script was
   written, and that **no figure card anywhere in the built `film.json`** carries a number that is not
   a ledger row (⛔-10).
