# EP76 · MORANDI — SCENE PLAN v002 — MEASURED

**Supersedes `EP76_morandi_SCENE_PLAN.v001.md` entirely.** v001 was projected from a rate measured on
one act; this is measured from the delivered master. v001 stays on disk because its projection was
wrong in a way worth keeping (§1.1).

**Episode `PD-2026-076-morandi` · authored 2026-08-21**

**Contract** `episodes/PD-2026-076-morandi/episode_spec.v001.json` ·
**Design** `EP76_morandi_FILM_BIBLE.v001.md` ·
**Script** `EP76_morandi_script.en.v001.md` ·
**Facts** `EP76_morandi_FACTS_LEDGER.v001.md` ·
**Images** `EP76_morandi_CODEX_BATCH_A.v001.md` + `.v002.md` (V001–V120) ·
**Footage** `EP76_morandi_FOOTAGE_PLAN.v001.md`

> **Every timestamp in this plan is MEASURED.** They come from
> `06_audio/narration_index.v001.json`, produced from the delivered ElevenLabs master
> (`E:\pd-media\episodes\PD-2026-076-morandi\06_voice\master\vc_master_v001.mp3`, **329 chunks,
> 0 failed, 1,842.130 s**).

---

## 1. THE ARITHMETIC THIS PLAN HAS TO SATISFY

| | value | where it comes from |
|---|---|---|
| finished runtime band | 1,740–1,920 s | `episode_spec.runtime_seconds` |
| **measured master** | **1,842.130 s** | narration index, ffprobe |
| **finished film** | **1,851.1 s (30:51)** | master + `ENDCARD_SEC` 9.0 |
| speech only | 1,733.2 s | index; the remaining 108.9 s is the gap budget |
| **delivered rate** | **178.4 raw wpm** | 5,154 words over 1,733.2 s of speech |
| average cut | **3.74 s** | 492 cuts over 1,842.1 s; `episode_spec.target_cut_sec` 3.8 |
| stills ceiling (32 % of cuts) | **157** | video-share floor |
| commissioned plates | **120** | the image order |
| distinct video assets | **265** | `episode_spec.distinct_video_assets` |
| video cuts floor (68 %) | **335** | 265 distinct at a mean reuse of **1.26×**, cap 4× |

**120 ≤ 157, and 265 distinct covering 335 video cuts at 1.26× reuse.** The contract holds, with more
headroom than v001 projected, because the film is a minute longer than projected.

**Non-narration budget, 9.0 s exactly:** `ENDCARD_SEC` only. No scripted silence.

### 1.1 The projection was 61 seconds short, and the reason is reusable

v001 sized the film from `--measure-section ACT_1`, which gave **184.0 raw wpm**. The whole script
delivered **178.4**. Where the 61 seconds went:

| section | v001 projected | measured | delta |
|---|---|---|---|
| HOOK | 23.4 s | **22.4 s** | −1.0 |
| OP | 35.1 s | **33.5 s** | −1.6 |
| ACT_1 | 249.8 s | **254.8 s** | +5.0 |
| ACT_2 | 198.6 s | **196.9 s** | −1.7 |
| **ACT_3** | 326.4 s | **372.7 s** | **+46.3** |
| **ACT_4** | 489.2 s | **520.5 s** | **+31.3** |
| ACT_5 | 343.3 s | **356.9 s** | +13.6 |
| ENDING | 77.6 s | **71.7 s** | −5.9 |

**Five of eight sections landed within two seconds. The error is concentrated in ACT_3 and ACT_4** —
the two acts built out of long verbatim quotation from the ministry's report and the judgment. ACT_1,
which was the sample, is short declaratives: the valley, three dates, the dimensions.

**The lesson, for the registry and for the next episode:** sampling ACT_1 alone biases a
quotation-heavy script **fast**. Sample an act that quotes, or add about 3 % when the back half is
verbatim-led. The band absorbed it here — 30:51 against a ceiling of 32:00 — but a tighter band
would not have.

---

## 2. SECTION SHEET — measured

| section | clock | dur | words | chunks | mean cut | cuts | plates | light |
|---|---|---|---|---|---|---|---|---|
| HOOK | 0:00.0 – 0:22.4 | 22.4 s | 69 | 5 | 4.0 s | 6 | V001–V006 (6) | I/U |
| OP | 0:24.2 – 0:57.7 | 33.5 s | 105 | 4 | 4.0 s | 8 | V007–V010 (4) | C→U |
| ACT_1 | 0:59.5 – 5:14.3 | 254.8 s | 727 | 51 | 3.9 s | 65 | V011–V034 (24) | C→U |
| ACT_2 | 5:16.1 – 8:33.0 | 196.9 s | 574 | 51 | **4.2 s** | 47 | V035–V054 (20) | U |
| ACT_3 | 8:34.8 – 14:47.6 | 372.7 s | 971 | 77 | 3.8 s | 98 | V055–V080 (26) | I/U |
| ACT_4 | 14:49.4 – 23:29.8 | **520.5 s** | 1,461 | 74 | **3.4 s** | 153 | V081–V106 (26) | I→C |
| ACT_5 | 23:31.6 – 29:28.6 | 356.9 s | 1,019 | 53 | 3.6 s | 99 | V107–V116 (10) | C/I |
| ENDING | 29:30.4 – 30:42.1 | 71.7 s | 228 | 14 | 4.5 s | 16 | V117–V120 (4) | C |
| | | **1,842.1 s** | **5,154** | **329** | **3.74 s** | **492** | **120** | |

### 2.1 ACT_4 is now 8:41, and the cutting answers it

The bible designed ACT_4 at ~6:15. It is **8:41** — a third of the film in one act. That is where the
evidence is: an assessment owed in 2013 and reported as done in 2017, a project whose stays were
exempted from verification, a committee shown its own authors' work, and then 11:36.

The plan does not cut the act. It gives it **the fastest mean cut in the film, 3.4 s — 153 cuts** —
and breaks it into three felt movements at the two AE beats and the hard cut at 11:36. ACT_2, the
shortest act and the one carrying the mechanism, keeps the slowest mean at 4.2 s.

---

## 3. THE CUT RECIPE, PER SECTION

Unchanged in kind from v001 §3; the cut counts are re-derived from the measured durations.

**Global rules.** No held frame > 2.0 s except the hero holds in §4. No naked hard cut except the one
at 11:36. Default transition is a **0.4 s cross-dissolve with motion carried through**. Every still
cut runs the bible §9 move (scale 1.000→1.055, y +0→−18 px, `Easing.out(Easing.cubic)`), and **≥ 40 %
of image cuts run the depth-parallax pass**.

| section | plate / footage / motion-graphic | transition | factory keywords |
|---|---|---|---|
| HOOK | 5 / 1 / 0 | none in, 0.4 s out | `city aerial` |
| OP | 4 / 3 / 1 | 0.4 s | `road traffic`, `car traffic` |
| ACT_1 | 24 / 35 / 6 | 0.4 s; 0.6 s at the 1967 opening | `city aerial`, `dock`, `cargo ship`, `shipping`, `excavator`, `timelapse` |
| ACT_2 | 20 / 22 / 5 | 0.5 s — the act is slower everywhere | `excavator`, `industrial`, `warehouse`, `dust`, `particle` |
| ACT_3 | 26 / 60 / 12 | 0.4 s; 0.3 s inside the score sequence | `typing`, `writing`, `notebook`, `hands writing`, `library`, `road traffic` |
| ACT_4 | 26 / 108 / 19 | 0.35 s; **one hard cut at 11:36** | `hands typing`, `keyboard`, `library`, `stairs`, `documents`, `car traffic`, `tunnel` |
| ACT_5 | 10 / 78 / 11 | 0.4 s | `night road`, `rainy`, `puddle`, `fog`, `library`, `city aerial` |
| ENDING | 4 / 11 / 1 | 0.6 s into the endcard | `road traffic`, `car traffic`, `urban traffic`, `asphalt road` |
| **total** | **119 / 318 / 55** | | |

**119 plate cuts ≤ 157 ceiling. 318 + 55 = 373 video-and-motion cuts ≥ the 335 floor.** ✓

**The desk register draws from `typing` / `writing` / `notebook` / `hands writing` first**, because
`office desk` and `documents` are already a third spent across previous episodes
(`FOOTAGE_PLAN` §8) and ACT_3 plus ACT_4 are **14:54** of paper.

---

## 4. HERO HOLDS AND KINETIC BEATS — on the measured clock

| # | clock | what | duration |
|---|---|---|---|
| H1 | ~3:45 | **V011 — the sheath in section**, mask wipe along the stay axis | 5.0 s + 1.5 s hold |
| B1 | ~4:30 | **AE — 352 + 112**, split-number card | 3.0 s |
| H2 | ~7:05 | **V042/V043 — the opened stay, severed strands** | 5.0 s |
| B2 | ~8:15 | **AE — only at pier eleven**, three piers, one fills | 4.0 s |
| H3 | ~11:10 | **V057 — the score box**, the number composited | 5.0 s |
| B3 | ~14:05 | **AE — €1,300,000 → €23,000**, bar to 1.8 % over 3.2 s, bed −6 dB | 3.2 s |
| H4 | ~16:30 | **V082 — the empty index tab** | 4.0 s |
| — | **~22:50** | **11:36 — the hard cut.** The only naked cut in the film | — |
| H5 | ~23:15 | **the 43 card**, held longest of any card | 6.0 s |
| B4 | ~28:10 | **AE — 32 / 25**, then *at first instance* masks up beneath | 3.0 s |
| H6 | ~30:30 | **V120 — the road that stops** | 9.0 s, ambient only |

**Re-hook spacing on the measured clock:** 0:59, 3:45, 5:16, 7:05, 8:35, 11:10, 14:05, 14:49, 17:30,
20:00, 22:50, 23:32, 26:00, 28:10, 29:30. **No gap exceeds 2:40.**

---

## 5. WHAT THIS PLAN STILL DOES NOT DECIDE

- **Seven plates are outstanding** (`CODEX_BATCH_A.v002`): V008, V020, V024, V078, V104, V112, V114.
  Until they return, people plates are 20 against a declared 24 and `mandatory_stills` stays empty.
- **No footage is staged.** Cross-episode reuse has been measured (`FOOTAGE_PLAN` §8) but no clip has
  been selected, and a person must open a labelled contact sheet first.
- **The four assembly inputs do not exist**: `03_script/script.annotated.v001.json`,
  `04_scenes/scene_plan.v001.json`, `04_scenes/remotion_plan.v001.json`,
  `05_visuals/asset_selection.v001.json`. The preflight is red on those four and on nothing else.
- **`preflight_render_gate.py --ep PD-2026-076-morandi` must be GREEN before a render starts.**
