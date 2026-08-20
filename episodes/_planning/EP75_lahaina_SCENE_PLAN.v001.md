# EP75 · LAHAINA — SCENE PLAN v001

**Episode `PD-2026-075-lahaina` · 30 minutes · authored 2026-08-21**

**Contract** `episodes/PD-2026-075-lahaina/episode_spec.v001.json` ·
**Design** `EP75_lahaina_FILM_BIBLE.v001.md` ·
**Script** `EP75_lahaina_script.en.v001.md` ·
**Facts** `EP75_lahaina_FACTS_LEDGER.v001.md` + `.v002.md` ·
**Images** `EP75_lahaina_CODEX_BATCH_A.v001.md` (H001–H132) ·
**Packaging** `EP75_lahaina_thumb_prompts.v001.md`

> **✅ MEASURED 2026-08-21. The projection this plan was first written against has been replaced.**
> The master was delivered the same day — `made=311 skipped=46 failed=0` — and §2 below is now read
> from `06_audio/narration_index.v001.json`, not modelled. The original warning and what the
> projection got wrong are kept in §2.2, because the size of that error is the useful part.

---

## 1. THE ARITHMETIC THIS PLAN HAS TO SATISFY

| | value | where it comes from |
|---|---|---|
| finished runtime band | 1,740–1,920 s | `episode_spec.runtime_seconds` |
| delivered pace | **184.1 wpm end-to-end** | the master itself, 2026-08-21 |
| script, as the TTS extractor read it | **5,338 words / 357 chunks** | `narration_index.v001.json` |
| **measured master** | **1,857.403 s** | narration index, ffprobe |
| **finished film** | **1,866.4 s (31:06)** | master + `ENDCARD_SEC` 9.0 |
| average cut | **3.8 s** | `episode_spec.target_cut_sec` |
| cuts at that mean | **486** | the section sheet below |
| stills ceiling (32 % of cuts) | **156** | video-share floor |
| commissioned plates | **132** | the image order, H001–H132 |
| distinct video assets | **265** | `episode_spec.distinct_video_assets` |
| video cuts floor (68 %) | **330** | 265 distinct at a mean reuse of **1.25×**, cap 4× |

**132 ≤ 156, and 265 distinct assets cover 330 video cuts at 1.25× reuse.** The contract is
satisfiable with room at both edges, **against the delivered master rather than against a
projection**.

**Non-narration budget, 9.0 s exactly:** `ENDCARD_SEC` only. **This film declares no scripted
silence.** The held beats in the design — the 4.0 s hold on 16:16, the 3.8 s hold on the gate, the
9.0 s hold on the blank form — sit inside the 1.8 s section gaps and the 0.3 s beat gaps the master
already contains, exactly as EP72's did.

---

## 2. SECTION SHEET — measured

Read from `narration_index.v001.json`, 357 chunks, master **1,857.403 s**.

| section | clock | dur | words | chunks | cuts | plates | light |
|---|---|---|---|---|---|---|---|
| HOOK | 0:00.0 – 0:20.3 | 20.3 s | 72 | 4 | 5 | H001–H008 (8) | W→S |
| OP | 0:22.1 – 0:56.6 | 34.5 s | 123 | 6 | 9 | H009–H014 (6) | O |
| ACT_1 | 0:58.4 – 5:33.9 | 275.5 s | 807 | 56 | 73 | H015–H038 (24) | O→W |
| ACT_2 | 5:35.7 – 10:09.5 | 273.7 s | 786 | 58 | 72 | H039–H064 (26) | N→W |
| ACT_3 | 10:11.3 – 15:51.7 | 340.4 s | 1,000 | 64 | 90 | H065–H088 (24) | W→S |
| ACT_4 | 15:53.5 – 22:28.1 | 394.7 s | 1,135 | 70 | 104 | H089–H110 (22) | S→O |
| ACT_5 | 22:29.9 – 28:17.4 | 347.4 s | 943 | 62 | 91 | H111–H128 (18) | O |
| ENDING | 28:19.2 – 30:57.4 | 158.3 s | 472 | 37 | 42 | H129–H132 (4) | O |
| | | **1,857.4 s** | **5,338** | **357** | **486** | **132** | |

**Film 1,866.4 s = 31:06** with `ENDCARD_SEC` 9.0, inside `runtime_seconds` [1740, 1920] with
**126 s of headroom at the low edge and 54 s at the high edge.**

**The hook landed at 20.266 s.** The film bible asked for "trim in the edit to land at 0:20 with the
last clause intact." **No trim was needed** — it came out of the voice at 20.3 s as written, and
`filmconfig.hookSeconds` carries that measured number.

### 2.0 The arithmetic, re-checked against the measured clock

| | measured |
|---|---|
| cuts at a 3.8 s mean | **486** |
| stills ceiling, 32 % of cuts | **156** — and 132 plates are ordered, so **132 ≤ 156** holds |
| video cuts floor, 68 % | **330** |
| distinct video assets declared | **265**, giving a mean reuse of **1.25×** against a 4× cap |

Every contract row still holds on the measured clock. Nothing has to be re-scoped.

### 2.2 What the projection got wrong, and by how much

Worth keeping, because it is the only calibration this channel has for sizing a film before its
voice exists.

| | projected | measured | error |
|---|---|---|---|
| pace | 187.1 raw wpm (from ACT_1 alone) | **184.1 end-to-end** | model 1.6 % fast |
| speech | 1,711.9 s | **1,740.1 s** | +28.2 s |
| film | 1,840.3 s (30:40) | **1,866.4 s (31:06)** | **+26.1 s, 1.4 %** |
| hook | "trim to land at 0:20" | **20.266 s, no trim** | — |

**A single measured section predicted a thirty-one-minute film to within 1.4 %.** That is the case
for spending the dollar on `--measure-section` and against trusting the registry's 171.79 model,
which would have put this film at 32:29 of speech alone and sized the script four minutes short.

### 2.1 Three things the shape of this sheet says, and what the plan does about each

1. **ACT_4 is the longest act (6:35 measured) and it starts at 15:53 — past the halfway line.**
   That is the cheapest place in a film to lose people. The plan answers it the way EP72 did:
   **tighten the cut mean in ACT_4 to 3.4 s** (104 cuts over 394.7 s is the 3.8 s mean; 3.4 s buys
   116) and put the act's hardest physical beat — the padlocked gate, H093–H099 — at **21:00**,
   inside the last third rather than at its end.
2. **ACT_3 carries the film's centre and is not the longest act.** It gets the *slowest* handling:
   the B2 clock stack builds across the whole act, and **16:16 (B3) holds 4.0 s with the left column
   dimmed to 25 %** — the single longest typographic hold in the film. Density is not pace, and this
   is the one place the film should stop.
3. **The ENDING is 2:38 measured, which is long for an ending, and deliberately.** It is where the film makes
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
| HOOK | 0:00–0:20 | H001–H008, roughly one plate per line | `dry_grass_field_wind`, `wildfire_smoke_ridge` — **eyeball both** | Push-in f0→f36 on H001, Trail 6 layers to f18. RECONSTRUCTION label up for the whole hook |
| OP | 0:22–0:57 | H009–H014 | — | `BrandOpening` 3.5 s lands over continuing footage at 0:20. The word *siren* is first spoken at 0:58, not before |
| ACT_1 | 0:58–5:34 | H015–H021 (the hardware and the monthly test), H022–H038 (the town and the forecast) | `dry_grass_field_wind`, `storm_clouds_dramatic` **texture only**, `weather_radar_screen` — **reject anything with legible numerals** | **B1 at ~1:25**: four identical framings of the pole cut on 11 frames. F10, the "notice was rare" quote card, at 4:05 |
| ACT_2 | 5:36–10:10 | H039–H050 (before dawn and the morning fire), H051–H064 (the roads, the phones, 14:17) | `power_lines_silhouette`, `utility_pole_repair`, `empty_road_sunset` **used flat, never golden** | F30, the 14:17 clock card, closes the act. The phone, H062, is seeded here and detonates in ACT_3 |
| ACT_3 | 10:11–15:52 | H065–H088 | `wildfire_smoke_ridge`, `smoke_over_road` — **no flame in any staged clip**, no orange grade | **B2 builds across the act. B3 (16:16) at ~14:30, 4.0 s, the film's largest card.** F43, the 15:37 radio quote, at ~13:00 with the bed −6 dB |
| ACT_4 | 15:53–22:28 | H089–H102 (the roads and the gate), H103–H110 (the water and the utility) | `chain_link_fence`, `fire_hydrant_street`, `water_main_trench` — **all three unverified on the shelf, eyeball first** | **B4 (eight ticks to six) at ~18:40.** Cut mean tightens to 3.4 s. The gate sequence H093–H099 runs unbroken at 21:00 |
| ACT_5 | 22:30–28:17 | H111–H117 (the investigation), H118–H128 (the findings and the record) | `office_corridor_empty`, `filing_cabinets`, `server_room_lights` | H118 returns the ACT_1 pole in the identical framing under colder light — **the one deliberate repeat in the film**, and it must read as a repeat |
| ENDING | 28:19–30:57 | H129 held, then H130–H132 | `small_town_street_day` (rebuilt, present day) | **B5: 9.0 s on H129 with no typography**, then `BrandEndcard` |

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
| B1 | ~1:25 | the monthly test | Four identical framings of the pole cut on 11 frames, light changing; FIRST BUSINESS DAY masks up under the fourth, holds 1.6 s |
| B2 | 10:50–14:50 | the clock | 14:55 / 14:57 / 15:00 / 15:05 / 15:21 / 15:23 / 15:37 stack, each masking up 34 px, 2 frames apart, earlier entries dimming to 40 % but never leaving frame |
| B3 | ~14:30 | **16:16** | The B2 stack still on screen. 16:16 lands **alone, right, at 2.2× scale**; the left column dims to 25 %. 4.0 s. **The film's largest card** |
| B4 | ~18:30 | eight to six | Eight ticks; two extinguish 6 frames apart; the six re-centre, `spring({damping: 14})` |
| B5 | ~30:48 | the blank form | No typography. 9.0 s hold, ambient motion only, then the endcard |

**B2 and B3 are one instrument, not two.** B3 only lands if B2 has been building for four minutes, so
the stack may not be dropped for pacing and re-introduced — it stays on screen, dimmed, across the
whole of ACT_3's middle.

---

## 5. WHAT MUST BE TRUE BEFORE THIS PLAN BECOMES A BUILD

1. ~~The narration master exists and §2 has been re-derived.~~ **DONE 2026-08-21.** Master
   1,857.403 s, 357 chunks, `made=311 skipped=46 failed=0`. §2 is measured and §2.2 records what the
   projection got wrong (1.4 %).
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
