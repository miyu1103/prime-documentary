# EP74 · ITAEWON — SCENE PLAN v003 — MEASURED

**Episode `PD-2026-074-itaewon` · authored 2026-08-21 · supersedes v002 entirely**

**Contract** `episodes/PD-2026-074-itaewon/episode_spec.v002.json` ·
**Design** `EP74_itaewon_FILM_BIBLE.v002.md` · **Script** `EP74_itaewon_script.en.v007.md` ·
**Facts** `EP74_itaewon_FACTS_LEDGER.v001`–`.v005.md` ·
**Images** `EP74_itaewon_CODEX_BATCH_A.v001.md` + `_BATCH_B.v001.md` ·
**Packaging** `EP74_itaewon_thumb_prompts.v002.md`

> **Every timestamp in this plan is MEASURED.** They come from
> `06_audio/narration_index.v001.json`, produced from the delivered ElevenLabs master
> (`E:/pd-media/episodes/PD-2026-074-itaewon/06_voice/master/vc_master_v001.mp3`, **343 chunks,
> 1,886.8 s, 184.8 wpm, 229 made / 114 cached / 0 failed**). v001 and v002 were projections and said
> so; this is the film.

---

## 1. WHAT THE MEASUREMENT COST, AND WHY IT IS IN THE PLAN

The first master, from script v006, measured **1,964.8 s and 184.3 wpm** — a **32:54** film against a
**32:00** ceiling. The projection had said 198.4 wpm, taken from `--measure-section ACT_1`.

**Measured per section, and this is the whole lesson:**

| section | wpm | | section | wpm |
|---|---|---|---|---|
| HOOK | 212.4 | | ACT_3 | 183.3 |
| OP | 205.0 | | ACT_4 | 182.7 |
| **ACT_1** | **195.5** | | **ACT_5** | **174.8** |
| ACT_2 | 193.8 | | ENDING | 184.5 |

**ACT_1 is the third-fastest section in the film and runs 5.8 % ahead of the whole.** Measuring one
early act and extrapolating over-estimates any film whose register slows as it argues — and this one
slows by 21 wpm between its first act and its fifth.

**Rule for the next episode: measure ACT_1 AND the longest late act, and size from the mean.**

Script v007 removed 220 words, most from ACT_5 at 0.344 s per word. No sourced fact was cut.

---

## 2. THE ARITHMETIC

| | value | source |
|---|---|---|
| runtime band | 1,740–1,920 s | `episode_spec.runtime_seconds` |
| narration words | **5,464** | v007 |
| **measured rate** | **184.8 wpm** | the master, ffprobe |
| speech | 1,773.7 s | index |
| gaps | 115.2 s | 342 beat gaps @0.30 + 7 section gaps @1.8 |
| **measured master** | **1,886.8 s** | |
| **finished film** | **1,898.2 s — 31:38** | master + `ENDCARD_SEC` 9.0 |
| headroom to the ceiling | **21.8 s** | |
| cut mean | **3.60 s** — 3.8 s everywhere, **3.2 s in ACT_5** | `target_cut_sec` 3.8, tightened per bible §4.5 |
| cuts | **526** | section sheet |
| stills ceiling (32 %) | **168** | video-share floor |
| plates on disk | **114** — 54 under the ceiling | six of 120 rejected at review and retired |
| video cuts floor (68 %) | **357** | 265 distinct at **1.35× mean reuse**, cap 4 |

**Non-narration budget, 10.5 s:** `ENDCARD_SEC` 9.0 plus the 1.5 s designed silence in ACT_5 before
"And then, in the summer of 2025, both appeals stopped."

---

## 3. SECTION SHEET — measured

| section | clock | dur | words | chunks | cuts | mean | plates | light |
|---|---|---|---|---|---|---|---|---|
| HOOK | 0:00.0 – 0:21.5 | 21.5 s | 72 | 4 | 6 | 3.6 s | I001, I052, I054, I014, I007 | A |
| OP | 0:21.5 – 1:39.5 | 78.0 s | 248 | 12 | 21 | 3.7 s | I002, I003, I015 | A |
| ACT_1 | 1:39.5 – 5:57.9 | 258.3 s | 780 | 57 | 68 | 3.8 s | I001–I024, I029–I034, I055–I059 | B→A |
| ACT_2 | 5:57.9 – 9:35.9 | 218.1 s | 654 | 46 | 57 | 3.8 s | I035–I051, I071–I080 | A |
| ACT_3 | 9:35.9 – 15:14.1 | 338.2 s | 971 | 62 | 89 | 3.8 s | I016–I024, I061, I062, I097–I104 | A→B |
| ACT_4 | 15:14.1 – 20:15.4 | 301.3 s | 860 | 57 | 79 | 3.8 s | I071–I080, I087–I096 | A/B |
| ACT_5 | 20:15.4 – 29:25.0 | **549.6 s** | 1,523 | 83 | **172** | **3.2 s** | I081–I104 | B |
| ENDING | 29:25.0 – 31:29.2 | 124.2 s | 356 | 22 | 33 | 3.8 s | I105–I120 | A/B |
| ENDCARD | 31:29.2 – 31:38.2 | 9.0 s | — | — | 1 | — | — | — |
| **total** | | **1,898.2 s** | **5,464** | **343** | **526** | **3.60 s** | **114** | |

**Two shifts from v002's projection, both real:** ACT_4 came in at **5:01** against 4:42 projected,
and ACT_3 at **5:38** against 5:17. Both are slow-register acts and both were under-projected by the
same bias. ACT_5 is **9:10** and remains the structural debt recorded in bible §4.5, answered with
pace rather than surgery.

**I025–I028 are absent from the plate column.** The Hamilton Hotel terrace group was rejected at
review and is being re-ordered as BATCH B. **ACT_1's terrace beat at roughly 3:10 currently has no
picture** and must be cut from footage or held on the width figure until BATCH B lands.

---

## 4. MEASURED BEAT TIMES

Taken from the master, not from a model. These are the frames the builder must hit.

| beat | measured | section |
|---|---|---|
| **81,573 → 31,878** — AE beat 3 | **4:44** | ACT_1 |
| **ELEVEN** — AE beat 1 | **8:14** | ACT_2 |
| **FOUR** — AE beat 2 | **8:16** | ACT_2 |
| **thirteen minutes** — figure card | **12:13** | ACT_3 |
| **159** — the longest card in the film, held 5.0 s | **12:51** | ACT_3 |
| **137** — AE beat 4 | **15:14** | ACT_4 |
| **34 → 921** — AE beat 5 | **16:33** | ACT_4 |
| **the acquittal's reason** — the largest quote card, held 6.0 s | **21:42** | ACT_5 |
| **Article 66-11** — second-largest quote card, held 6.0 s | **23:06** | ACT_5 |
| **STOPPED** — AE beat 6, the 1.5 s silence lands immediately before | **26:35** | ACT_5 |
| the barrier, the ending's hero | **29:24** | ENDING |

**ELEVEN and FOUR are two seconds apart.** That is not a defect — it is the act's hinge, and the two
cards must read as one gesture: eleven fills, four fills gold, seven stay outline.

---

## 5. WHAT CARRIES EACH BLOCK

Unchanged from v002 §3 in substance; the clocks are now measured. Defaults: `asset_type: plate`;
`motion: MovingImage`, scale 1.000 → 1.055, y 0 → −18 px over 3.8 s, `Easing.out(Easing.cubic)`;
`transition: crossfade 0.4 s` with the Sequences overlapping so no frame goes black and no velocity
resets; `Trail` only on spans marked **fast**; no still held over 2.0 s without motion; no naked hard
cut anywhere.

| block | clock | carried by | archive registers | notes |
|---|---|---|---|---|
| HOOK | 0:00–0:22 | I001 → I052 → I054 → I014 → I007 | `narrow alley` **REMOVED — see §6**, use `seoul night`, `street night`, `wet reflection` | Push-in f0→f36 on I001, Trail 6 layers to f18. **fast.** No crowd yet |
| OP | 0:22–1:40 | I002, I003, I015 + the width-line figure | `city street`, `empty street` | `BrandOpening` 3.5 s at 0:22. Width line f0→f45 |
| ACT_1 | 1:40–5:58 | I001–I024, I029–I034, then I055–I059 for the count | `seoul`, `subway`, `escalator`, `roller shutter`, `air conditioner` | **HERO: the width line to 3.2.** Slope drawn with **no numeral**. **The terrace beat at ~3:10 has no plate until BATCH B.** AE beat 3 at **4:44** |
| ACT_2 | 5:58–9:36 | the call-log figure over I023, I035–I051, I071–I080 | `crowd`, `people walking`, `police`, `torch beam` | **HERO: the log.** Four rows fill; seven stay outline-only. AE beats 1–2 at **8:14** and **8:16** |
| ACT_3 | 9:36–15:14 | I016–I024, I097–I104, the density figure | `empty street`, `morning street`, `documents` — **no crowd stock in this act at all** | Light change A→B lands here on the empty alley. **159 held 5.0 s at 12:51.** ⛔-02 is enforced by the plan: nothing staged here contains people |
| ACT_4 | 15:14–20:15 | the Yongsan map, I071–I080, I087–I096 | `city map`, `government`, `corridor`, `empty chairs` | **HERO: the map.** AE beats 4–5 at **15:14** and **16:33**. The Constitutional Court card cuts directly against the audit card, same framing, same size |
| ACT_5 | 20:15–29:25 | I081–I104 | `corridor`, `files`, `empty chairs`, `book` — **no courtroom, no gavel** | Cut mean **3.2 s**. Largest card at **21:42**, second at **23:06**, silence + **STOPPED at 26:35** |
| ENDING | 29:25–31:29 | I105–I120 | `barrier`, `cctv`, `fence`, `korea` | **HERO: the barrier at 29:24.** I119 used once, 2.5 s, never as a thumbnail. BGM resolves on a cadence |
| ENDCARD | 31:29–31:38 | `BrandEndcard` | — | 9.0 s. **The subscribe and comment ask lives HERE and nowhere else** — `check_script_craft.SPOKEN_CTA` is a hard gate |

---

## 6. THE FOOTAGE LANE — what the frames said that the counts did not

Measured 2026-08-21 by opening the candidate contact sheets rather than reading hit counts.

| query | measured hits | what it actually returns | action |
|---|---|---|---|
| `alley` | 10 | **Avenues of trees** in parks and boulevards — the botanical sense. Plus a **green-screen** brick corridor and a **cartoon** street | **REMOVED** |
| `train station` | — | **Eastern European passenger platforms**, with a fully identifiable woman across six frames | **REMOVED** |
| `seoul` | 15 | A real **Seoul subway tunnel**. Exactly the film | **ADDED** |

**Supply, measured across three passes:** 307 candidates → 403 → **470**, and the reviewable set
173 → 242 → **294**, against **265 distinct required**. `--per-query 14` returns the same pool as 6,
so the lever is probed queries, not the cap. The set is now 119 queries, every one built from a term
measured on this shelf.

**294 is above 265 for the first time, and it is not enough yet.** EP71 measured a 70-clip sample at
**50 % off-register**, and a human pass has not run here. Expect to need another round of queries
after it.

**Deliberately unused:** `sunset` (546 rows) and `sunrise` (202) are the largest untapped blocks on
the shelf and both are banned by `era_setting`. This film has no golden hour in it.

## 7. BEFORE A RENDER

1. **BATCH B** — six plates plus the thumbnail background. ACT_1's terrace beat has no picture until
   they land.
2. **The footage content pass**: 101 sheets in `runs/qc/prestage_frames/itaewon`, then
   `prestage_footage_review.py --slug itaewon --decide <json> --stage`. Nothing is staged yet, by
   design: a reject costs a line in a json instead of a copy and a move back out.
3. `filmconfig` and a `Ep74` composition in `Root.tsx`.
4. `preflight_render_gate.py --ep PD-2026-074-itaewon` **GREEN.** Not advisory: 25 of 32 episodes
   failed it and 10 rendered anyway.
5. **`AB-11` on the day of publish**: has either suspended appeal restarted? It rewrites the last act.
