# EP76 · MORANDI — SCENE PLAN v001

**Episode `PD-2026-076-morandi` · 30 minutes · authored 2026-08-21**

**Contract** `episodes/PD-2026-076-morandi/episode_spec.v001.json` ·
**Design** `EP76_morandi_FILM_BIBLE.v001.md` ·
**Script** `EP76_morandi_script.en.v001.md` ·
**Facts** `EP76_morandi_FACTS_LEDGER.v001.md` ·
**Images** `EP76_morandi_CODEX_BATCH_A.v001.md` (V001–V120) ·
**Footage** `EP76_morandi_FOOTAGE_PLAN.v001.md`

> **PROJECTED, and it says so.** Unlike EP72's plan, this one is written **before** the narration
> master exists. It rests on one real measurement — `--measure-section ACT_1` delivered
> **184.0 raw wpm** on this script at the pinned voice settings — and on the extractor's own chunk
> count. **It is superseded by a v002 written from `06_audio/narration_index.v001.json` the moment
> that master exists**, and no cut list is committed until then.

---

## 1. THE ARITHMETIC THIS PLAN HAS TO SATISFY

| | value | where it comes from |
|---|---|---|
| finished runtime band | 1,740–1,920 s | `episode_spec.runtime_seconds` |
| measured narration rate | **184.0 raw wpm** | `--measure-section ACT_1`, 46 chunks / 650 words / 211.906 s |
| script | **329 chunks / 5,154 words** | `gen_narration_case --dry-run` |
| **projected master** | **1,756–1,790 s** | section arithmetic below / the registry's whole-script figure |
| **projected film** | **1,765–1,799 s (29:24–29:59)** | master + `ENDCARD_SEC` 9.0 |
| average cut | **3.75 s** | 468 cuts over 1,756 s; `episode_spec.target_cut_sec` 3.8 |
| stills ceiling (32 % of cuts) | **150** | video-share floor |
| commissioned plates | **120** | the image order, V001–V120 |
| distinct video assets | **265** | `episode_spec.distinct_video_assets` |
| video cuts floor (68 %) | **318** | 265 distinct at a mean reuse of **1.20×**, cap 4× |

**120 ≤ 150, and 265 distinct covering 318 video cuts at 1.20× reuse.** The contract is satisfiable.

**Non-narration budget, 9.0 s exactly:** `ENDCARD_SEC` only. This film declares **no scripted
silence**; the held beats in the design sit inside the 1.8 s section gaps and 0.3 s beat gaps the
master already contains.

---

## 2. SECTION SHEET — projected

| section | clock | dur | words | chunks | mean cut | cuts | plates | light |
|---|---|---|---|---|---|---|---|---|
| HOOK | 0:00.0 – 0:23.4 | 23.4 s | 68 | 5 | 4.0 s | 6 | V001–V006 (6) | I/U |
| OP | 0:25.2 – 1:00.3 | 35.1 s | 105 | 4 | 4.0 s | 9 | V007–V010 (4) | C→U |
| ACT_1 | 1:02.1 – 5:11.9 | 249.8 s | 720 | 51 | 3.9 s | 64 | V011–V034 (24) | C→U |
| ACT_2 | 5:13.7 – 8:32.3 | 198.6 s | 563 | 51 | **4.2 s** | 47 | V035–V054 (20) | U |
| ACT_3 | 8:34.1 – 14:00.5 | 326.4 s | 931 | 77 | 3.8 s | 86 | V055–V080 (26) | I/U |
| ACT_4 | 14:02.3 – 22:11.5 | **489.2 s** | 1,433 | 74 | **3.4 s** | 144 | V081–V106 (26) | I→C |
| ACT_5 | 22:13.3 – 27:56.6 | 343.3 s | 1,005 | 53 | 3.6 s | 95 | V107–V116 (10) | C/I |
| ENDING | 27:58.4 – 29:16.0 | 77.6 s | 226 | 14 | 4.5 s | 17 | V117–V120 (4) | C |
| | | **1,756.0 s** | **5,051** | **329** | **3.75 s** | **468** | **120** | |

*The per-section word total is 103 short of the extractor's 5,154 because this sheet counts only
lines the section splitter sees; the extractor is authoritative and the difference is inside a
second of runtime per act.*

### 2.1 Three deviations from the film bible's ARC, measured rather than assumed

The bible designed ACT_2 at ~5:45 and ACT_4 at ~6:15. **Measured from the script: ACT_2 is 3:19 and
ACT_4 is 8:09.** The weight of the film moved into ACT_4 when the safety assessment, the project
verification, the committee and 11:36 all landed in one act.

| act | designed | projected | delta |
|---|---|---|---|
| ACT_1 | 4:51 | 4:10 | −41 s |
| ACT_2 | 5:45 | **3:19** | **−146 s** |
| ACT_3 | 6:00 | 5:26 | −34 s |
| ACT_4 | 6:15 | **8:09** | **+114 s** |
| ACT_5 | 5:15 | 5:43 | +28 s |
| ENDING | 0:53 | 1:18 | +25 s |

**The script is not being cut to fit the bible's table.** ACT_4 is the film's turn and its densest
evidence, and the material in it — an assessment owed in 2013 and reported as done in 2017, a
project whose stays were exempted from verification, a committee shown its own authors' work, and
then 11:36 — is the reason this episode exists. The plan answers the shape rather than fighting it:

1. **ACT_4 gets the fastest mean cut in the film, 3.4 s**, so eight minutes never sit still, and it
   is broken into three felt movements by the two AE beats and the hard cut at 11:36 (§4).
2. **ACT_2 gets the slowest, 4.2 s.** It is the shortest act and it carries the mechanism — what was
   found inside a stay when somebody finally cut into one. It is allowed to breathe.
3. **The bible's §4 ARC table is corrected to these timings in the same commit**, so the two
   documents cannot disagree.

---

## 3. THE CUT RECIPE, PER SECTION

Manual §5.2 requires every span to carry asset type, motion, transition and factory keywords.
Rather than 468 rows, this is stated per section as a recipe the builder applies; the span-level
table is generated into `filmconfig` from the narration index in v002.

**Global rules.** No held frame > 2.0 s except the declared hero holds in §4. No naked hard cut
except the one at 11:36. Default transition is a **0.4 s cross-dissolve with motion carried through**
— velocity is never reset at the cut. Every still cut runs the default Ken-Burns-plus-depth move
from the bible §9 (scale 1.000→1.055, y +0→−18 px, `Easing.out(Easing.cubic)`), and **≥ 40 % of
image cuts run the depth-parallax pass** (`D` flag on the plate).

| section | asset mix (plate / footage / motion-graphic) | motion | transition | factory keywords |
|---|---|---|---|---|
| HOOK | 5 / 1 / 0 | push-in f0→f36 scale 1.06→1.00 + Trail 6 layers to f18 | none in, 0.4 s dissolve out | `city aerial` |
| OP | 4 / 4 / 1 | slow depth drift, ±0.06 z | 0.4 s dissolve | `road traffic`, `car traffic` |
| ACT_1 | 24 / 34 / 6 | default + the sheath mask-wipe hero | 0.4 s dissolve; 0.6 s at the 1967 opening | `city aerial`, `dock`, `shipping`, `cargo ship`, `excavator`, `industrial`, `timelapse` |
| ACT_2 | 20 / 22 / 5 | default, slowed; long holds on the opened stay | 0.5 s dissolve — the act is slower everywhere | `excavator`, `industrial`, `warehouse`, `dust`, `particle` |
| ACT_3 | 26 / 50 / 10 | default + score-box fill spring; money-decay bar | 0.4 s dissolve; 0.3 s inside the score sequence | `office desk`, `typing`, `writing`, `hands writing`, `notebook`, `documents`, `library`, `road traffic` |
| ACT_4 | 26 / 100 / 18 | default, tightened; two AE beats | 0.35 s dissolve; **one hard cut at 11:36** | `documents`, `office desk`, `keyboard`, `hands typing`, `library`, `stairs`, `car traffic`, `highway traffic`, `tunnel` |
| ACT_5 | 10 / 74 / 11 | default; the barrier hero | 0.4 s dissolve | `night road`, `rainy`, `puddle`, `fog`, `documents`, `library`, `city aerial` |
| ENDING | 4 / 12 / 1 | 9.0 s hero hold, ambient motion only | 0.6 s dissolve into the endcard | `road traffic`, `car traffic`, `urban traffic`, `asphalt road` |
| **total** | **119 / 297 / 52** | | | |

**119 plate cuts ≤ the 150 ceiling. 297 footage cuts ≥ the 318 floor is NOT met by footage alone** —
the floor counts footage **and** motion assets as video, so 297 + 52 = **349 ≥ 318**. ✓

---

## 4. HERO HOLDS AND KINETIC BEATS — where the film is allowed to stop

| # | clock (projected) | what | duration | rule |
|---|---|---|---|---|
| H1 | ~3:40 | **V011 hero — the sheath in section**, mask wipe along the stay axis | 5.0 s wipe + 1.5 s hold | the only hold in ACT_1 |
| H2 | ~7:05 | **V042/V043 — the opened stay, severed strands** | 5.0 s | ACT_2's centre; ambient bed only |
| B1 | ~4:25 | **AE — 352 + 112**, split-number card | 3.0 s | bible §12.5 B1 |
| B2 | ~8:10 | **AE — only at pier eleven**, three piers, one fills | 4.0 s | B2 |
| H3 | ~10:50 | **V057 hero — the score box**, the number composited | 5.0 s | ACT_3 |
| B3 | ~13:30 | **AE — €1,300,000 → €23,000**, bar falls to 1.8 % over 3.2 s, ambient −6 dB | 3.2 s | B3; **nothing else moves during it** |
| H4 | ~15:40 | **V082 hero — the empty index tab** | 4.0 s | ACT_4 |
| — | **~21:20** | **11:36 — the hard cut.** The only naked cut in the film | — | ACT_4's turn |
| H5 | ~21:45 | **the 43 card**, held longest of any card | 6.0 s | F62; ambient only |
| B4 | ~26:40 | **AE — 32 / 25**, then *at first instance* masks up beneath | 3.0 s | B4 |
| H6 | ~29:00 | **V120 — the road that stops** | 9.0 s, ambient motion only, no typography | B5, then endcard |

**Re-hook spacing**, against the bible §7 retention map and the projected clock: 1:02, 3:40, 5:14,
7:05, 8:34, 10:50, 13:30, 14:02, 16:30, 19:00, 21:20, 22:13, 24:30, 26:40, 27:58. **No gap exceeds
2:30**, and the longest flat stretch in the plan is the 9.0 s ending hold, which is deliberate.

---

## 5. PLATE ALLOCATION — every one of the 120 is placed

| plates | section | note |
|---|---|---|
| V001–V006 | HOOK | 6 |
| V007–V010 | OP | 4 |
| V011–V034 | ACT_1 | 24 — the design, the valley, the stay |
| V035–V054 | ACT_2 | 20 — 1981–1996, pier 11 |
| V055–V080 | ACT_3 | 26 — the scores, the money |
| V081–V106 | ACT_4 | 26 — the paperwork, the committee, 11:36 |
| V107–V116 | ACT_5 | 10 — the gap, the court |
| V117–V120 | ENDING | 4 |

**`mandatory_stills` stays empty in `episode_spec` until the plates exist on disk.** The moment
V001–V120 are delivered and upscaled, every one of them is listed there, because EP54's fourteen
purpose-made stills were silently dropped by a surplus-trimming rule and then retired as
unreferenced. That is the failure this field exists to prevent.

---

## 6. WHAT THIS PLAN DOES NOT DECIDE

- **The cut list.** No span-level table is committed until the narration master exists and v002 is
  written from `narration_index.v001.json`. Every timestamp above moves.
- **Which clip goes where.** `check_cross_episode_reuse.py` runs first, then a person opens a
  labelled contact sheet. `footage_review_required` is `true` and no gate in this pipeline looks at
  an image.
- **Anything about the render.** `preflight_render_gate.py --ep PD-2026-076-morandi` must be green
  before a render starts. It has failed on 25 of 32 episodes and been overridden on 10.
