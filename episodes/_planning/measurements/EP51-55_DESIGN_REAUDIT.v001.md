# EP51–EP55 DESIGN RE-AUDIT v001 — every defect class discovered 2026-07-27/28

**Date:** 2026-07-28 · **Scope:** `episodes/_planning/EP{51_willingham,52_morton,53_norfolk,54_flowers,55_burge}_*`
**Method:** independent re-measurement. Nothing here is self-reported. Every number was re-derived from the locked script, the `voice_plan.v001.json`/`narration_index.v001.json` on disk, and `ffprobe` on the real masters on `H:`. No rendered media, build output, EP50/EP56 file, or TTS run was touched.
**Trigger:** EP56 was the first 5-act film and `gen_narration_case.py` mapped only ACT I–IV — 34 chunks would have been dropped silently while the coverage gate passed. This audit asks whether EP51–55 carry that defect or its siblings. EP51/EP52 were built by an earlier session and had never been through the gates EP53–56 went through; they are treated as highest-risk and that judgement was correct.

---

## 0. MEASURED GROUND TRUTH (the basis for everything below)

| | EP51 willingham | EP52 morton | EP53 norfolk | EP54 flowers | EP55 burge |
|---|---|---|---|---|---|
| Script acts | **3** (I/II/III) | 4 | 4 | 4 | 4 |
| Narration runner | `gen_narration_willingham.py` (bespoke) | `gen_narration_morton.py` (bespoke) | `gen_narration_case.py` | `gen_narration_case.py` | `gen_narration_case.py` |
| voice_plan chunks | 218 | 319 | 304 | 313 | 292 |
| Narration words (measured) | 3,593 | 5,350 | 4,762 | 4,821 | 4,861 |
| Master (ffprobe) | **1,208.845 s** | **1,785.803 s** | **1,673.888 s** | **1,711.093 s** | **1,749.561 s** |
| Speech / in-master gaps | 1,136.253 / 72.592 | 1,681.404 / 104.399 | 1,573.990 / 99.898 | 1,608.485 / 102.608 | 1,653.264 / 96.297 |
| Measured pace | 189.7 wpm | 190.9 wpm | 181.5 wpm | 179.8 wpm | 176.4 wpm |
| Drift vs DESIGN model | +5.4 s | −9.5 s | +9.1 s | +29.2 s | **+71.2 s** |

Per-section measured words (this is the table CODEX_A §2 is supposed to carry):

| section | EP51 | EP52 | EP53 | EP54 | EP55 |
|---|---|---|---|---|---|
| HOOK | 108 | 117 | 110 | 146 | 163 |
| OP | 97 | 140 | 163 | 184 | 178 |
| ACT_1 | 645 | 1,144 | 950 | 1,081 | 836 |
| ACT_2 | 853 | 1,190 | 1,038 | 975 | 1,234 |
| ACT_3 | 1,352 | 936 | 968 | 1,012 | 945 |
| ACT_4 | — | 1,462 | 1,233 | 1,102 | 1,251 |
| ENDING | 538 | 361 | 300 | 321 | 254 |
| **total** | **3,593** | **5,350** | **4,762** | **4,821** | **4,861** |

---

## 1. DEFECT CLASS 1 — act-count / section-mapping drop

**Method:** an independent parser (not the runners') walked each locked script, mapped every heading, collected every line a human would call narration, and checked each line's normalised text against the concatenated `voice_plan` spoken text. It also collected prose sitting under a heading with no section mapping (the EP56 `BRAND STING` failure mode).

| | EP51 | EP52 | EP53 | EP54 | EP55 | EP56 (control) |
|---|---|---|---|---|---|---|
| Script narration headings mapped | HOOK/OP/ACT_1/2/3/ENDING | +ACT_4 | +ACT_4 | +ACT_4 | +ACT_4 | +ACT_4/ACT_5 |
| voice_plan section order == script order | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Prose lines in narration body | 47 | 64 | 48 | 42 | 42 | 40 |
| **Prose lines absent from voice_plan** | **0** | **0** | **0** | **0** | **0** | **0** |
| **Prose under an unmapped heading** | **0** | **0** | **0** | **0** | **0** | **0** |

**Verdict: OK for all five. Zero dropped narration anywhere.** EP53/54/55 are confirmed independently, not just byte-identical-after-the-fix. EP51/EP52 predate the generic runner entirely and were voiced by bespoke per-episode runners whose section maps are correct (`gen_narration_willingham.py` declares a 3-act `SECTION_ORDER`; `gen_narration_morton.py` a 4-act one).

**Latent finding (DOC-ONLY, but it is the EP56 defect's mirror image):** EP51 is a **3-act** film and is **not registered** in `gen_narration_case.py`'s `EPISODES` dict. If EP51 were ever re-voiced through the now-canonical runner, `assert_clean()`'s default `SECTION_ORDER` demands `ACT_4` and would **refuse to generate** — a *safe* failure (money not spent, nothing dropped), not a silent drop. The `SECTION_ORDER_5ACT` escape hatch added for EP56 has no 3-act counterpart. Recorded in EP51 DESIGN §5.

**Related and NOT harmless — EP51's phantom ACT IV (see class 3).** The narration has no ACT_4 and never will, but EP51's *asset and AE* documents allocate a full `ACT_4 "The Reckoning"` block. That is a real cross-document mapping defect and is scored under class 3.

---

## 2. DEFECT CLASS 2 — measured-VO re-lock never performed

All five masters exist on disk and were ffprobed. The re-lock each DESIGN §5/§6 mandates for itself had been performed on **EP55 only**.

| | Model in DESIGN | Provisional | MEASURED re-lock | Absorbable without re-lock? | Status found |
|---|---|---|---|---|---|
| **EP51** | `ceil(narr·30) + 105 + 270`, narr = master | narr 1,203.4 → 36,477 f | narr **1,208.845** → **36,641 f** = **1,221.367 s = 20:21.4**, ratio **1.0749** | **NO** — no gap budget exists to absorb into | ❗ never re-locked |
| **EP52** | `ceil(narr·30) + 270`, narr = master | narr 1,795.3 → 54,129 f | narr **1,785.803** → **53,845 f** = **1,794.833 s = 29:54.8**, ratio **1.0675** | **NO** — stale value leaves ~9.5 s of picture with no audio | ❗ never re-locked |
| **EP53** | `total = narr × 1.150` | narr 1,564.9 → total 1,799.6 → 53,988 f | speech **1,573.99**; total holds 1,799.6, frames hold 53,988, realised ratio **1.1434** | **YES** (+9.1 s) | ⚠ measured value never recorded |
| **EP54** | `total = narr + 195 + 9` | narr 1,579.3 → total 1,783.3 → 53,499 f | speech **1,608.485**; pause budget **195.0 → 165.8**; total holds 1,783.3, frames hold 53,499, ratio **1.1087** | **YES** (+29.2 s) | ⚠ measured value never recorded; pause map must be re-cut |
| **EP55** | `total = narr + gap + 9` | narr 1,582.1 / gap 199.9 → 1,791.0 → 53,730 f | narr **1,653.3** / gap **179.7** → **1,842.0 s = 30:42** → **55,260 f**, ratio **1.114** | n/a | ✅ **re-lock performed and arithmetically correct** — but CODEX_A §2 was left on the stale provisional numbers |

All re-locked totals sit inside 1740–1860 s and all speech ratios inside the measured 1.04–1.30 band — **except EP51**, which is a deliberate 20-minute film at 1,221 s and therefore outside the channel's 30-min band entirely (see verdicts).

**EP55's own review log (R3+++) already states "EP53 (+9.1 s) and EP54 (+29.2 s) absorbed by their own gap budgets without re-lock" — that call is arithmetically correct and is confirmed here.** The defect for EP53/54 is that neither DESIGN nor CODEX_A carried the measured number, so a builder reading only those docs would still believe the VO is unmeasured.

---

## 3. DEFECT CLASS 3 — internal numeric contradictions

Every table in all five DESIGNs and CODEX_As was re-added.

### What is arithmetically CLEAN (verified, no action)
- **§3.3 checksum blocks, all five files, every line:** EP51 [1]–[7], EP52/53/54/55 [1]–[8] all re-computed and agree (cut sums, still-share, motion coverage, per-asset caps, first-use share, avg-uses/source, factory floor). Independently confirmed by a second pass.
- **Per-act motif sums == §3.3 still-body totals, all five:** EP51 16+30+34+32+38 = 150 ✓ · EP52 15+45+55+40+45+15 = 215 ✓ · EP53 15+45+45+40+45+15 = 205 ✓ · EP54 15+45+50+45+40+15 = 210 ✓ · EP55 15+42+50+42+46+15 = 210 ✓. §3.2 factory/i2v re-adds also clean in all five.
- **CODEX_A §2's "= still + factory + motion" sum is the DISTINCT count, not total cuts, in all five** (EP51 150+165+30 = 345 = distinct ✓, matching the EP52–55 convention). Not a defect; noted because it reads like one.
- **AE deck arithmetic:** EP52 4+9+2+1+1 = 17 ✓ · EP53 4+9+2+1+1 = 17 with all 17 enumerated ✓ · EP55 4+9+2+1+1+1 = 18 ✓ (the R3 off-by-one fix holds; the signature list does enumerate 9 CENTER_STACKs).
- **EP52 figure density** 82 / 29.91 min = 2.74/min ✓ exactly as written. **EP53** 84 / 30.0 min = 2.80/min ✓ as written.

### Contradictions FOUND

| ID | Ep | Contradiction | Severity |
|---|---|---|---|
| **C-1** | **EP51** | **CODEX_A §2 `durationInFrames = 36,717 (= 240 + 105 + 36102 + 270)` vs DESIGN §6 `36,477 = ceil(narr·30) + 105 + 270`.** The CODEX_A value is the OLD 4-term formula **including a 240-frame (8.0 s) silent hook runway** that DESIGN §6 explicitly says is REPLACED. Building to CODEX_A puts 8 s of voiceless film in front of the cold open. | **FIX-BEFORE-BUILD** |
| **C-2** | **EP51** | **Phantom ACT IV.** Script has 3 acts. CODEX_A §2 declares `visual acts = 4 … ACT_4 The Reckoning`; §3.2 allocates **38 stills (S113–S150, 25 % of the still budget) + 33 factory + 7 i2v to `ACT_4`**; DESIGN §5 says beats are "heaviest in ACT III and **ACT IV**"; CODEX_B §7.2 emits an `ACT_TITLE_CARD` reading **"ACT IV / THE RECKONING" at t = 830.0 s**. There is no ACT IV narration section and never will be. Anything mapping by act *name* finds nothing. | **FIX-BEFORE-BUILD** |
| **C-3** | **EP51** | DESIGN §4 declares `SPLIT_COMPARE (×3)` but then says "**The two** SPLIT_COMPAREs carry the reversal" and applies the cold accent to "**both** SPLIT_COMPAREs' right pane". CODEX_B §7.2 has three (`cmp-pillars` framing, ember↔ember; `cmp-flashover` and `cmp-glass` reversal, ember↔cold). | DOC-ONLY |
| **C-4** | **EP51** | DESIGN §5 quotes density 2.89/min against the 20.06 min provisional; at the re-locked 20:21.4 it is **2.85/min**. Still ≥2.5 ✓. | DOC-ONLY |
| **C-5** | **EP52** | **Per-act word table over-states the body by ~518 words** and names the wrong densest act. `ACT1 ~1250 / ACT2 ~1500 (engine·最密) / ACT3 ~1000 / ACT4 ~1500` = 5,250 for the acts alone (5,868 with hook/OP/ending) against a 5,350-word body. Measured: ACT2 is **1,190** (not 1,500) and **ACT_4 is the densest at 1,462 w / 477.4 s**. This is the EP56 defect class exactly. | **FIX-BEFORE-BUILD** |
| **C-6** | **EP52** | `words_total = 5,326` vs measured 5,350 (−24). | DOC-ONLY |
| **C-7** | **EP54** | **Per-act word table is labelled 実測 (MEASURED) and is not.** `ACT1 ~1220 / ACT2 ~1180 / ACT3 ~1100 / ACT4 ~1120 (+ COLD/OPEN/ENDING ~1050)` = **5,670** against a **4,821**-word body — over by **+849 (+17.6 %)**, every act over-stated, ACT II by +205. A false "measured" label is worse than a provisional one because it stops anyone re-checking. | **FIX-BEFORE-BUILD** |
| **C-8** | **EP54** | AE deck sums to **18** ("Total = 4+7+3+1+2+1 = 18") under a heading that says "~17 cards", resolved only by a deferred instruction to "trim to 17 at CODEX_B lock by merging the two TRIAL center-stacks". **CODEX_B does not exist for EP54.** The card count is genuinely unresolved. | FIX-BEFORE-BUILD (at CODEX_B authoring) |
| **C-9** | **EP54** | §4 quotes 2.85/min; 84 / 29.72 min = **2.83**. | DOC-ONLY |
| **C-10** | **EP55** | **The "199 vs 181.8" class, confirmed:** DESIGN §5 was re-locked to `gap 179.7 / total 1,842.0 / 55,260 f`, but **CODEX_A §2 still carried `designed_gap_seconds = 199.9 / total 1,791.0 / durationInFrames 53,730 / mean_shot 3.166`**, and §3.3 [2][8] were still keyed to the superseded `picture 1782.0`. Two governing documents, two different runtimes. | **FIX-BEFORE-BUILD** |
| **C-11** | **EP55** | §4 quotes 2.75/min against the superseded 1,791.0 s; at the re-locked 1,842.0 s it is **2.67/min**. Still ≥82 beats and ≥2.5/min ✓. | DOC-ONLY |
| **C-12** | **EP55** | Per-act word table 4,990 vs measured 4,861 (+2.7 %); "ACT2 最密" is not quite right — ACT_4 (1,251 w) edges ACT_2 (1,234 w). | DOC-ONLY |
| **C-13** | **EP53** | Per-act table 4,650 vs measured 4,762 — accurate to 2.4 %; only ACT IV understated (1,100 planned vs 1,233 actual). | DOC-ONLY |
| **C-14** | EP51/52/55 | **Stale numbers persist in `CODEX_B_BUILD` and `bgm_plan`** (out of this audit's edit scope): EP51 CODEX_B carries `1203.4 / 36,477` at 8 places; EP52 CODEX_B carries `1795.3 / 54,129` at 9 places; EP55 `bgm_plan.v001.md` header still reads "≈ 1,791 s = ナレ1,582.1 + 199.9 + 9". | **build-stage action** |

---

## 4. DEFECT CLASS 4 — CODEX_A prompt-table integrity

`python scripts/check_prompt_diversity.py <file>` — **all five RESULT: PASS (0 dup-pairs, 0 generic)**. Full output in §7. But the gate only measures prompts that exist, and on EP51/EP52 it measures almost none.

| | EP51 | EP52 | EP53 | EP54 | EP55 |
|---|---|---|---|---|---|
| S-numbers gap-free to the stated count | ❌ **30 ids, max S143** (stated 150) | ❌ **21 ids, max S198** (stated 215) | ✅ S001–S205 | ✅ S001–S210 | ✅ S001–S210 |
| Literal prompts — body stills | **30 / 150** | **21 / 215** | 205 / 205 | 210 / 210 | 210 / 210 |
| Literal prompts — i2v seeds (M) | **20 / 30** | **23 / 43** | 42 / 42 | 44 / 44 | 42 / 42 |
| Literal prompts — thumb (T) | n/a | 3 / 3 | 3 / 3 | 3 / 3 | 3 / 3 |
| Literal prompts — face (F) | **0 / 12** | **0 / 12** | **0 / 12** | 12 / 12 | 12 / 12 |
| `[HSTYLE]` rows: stated → actual | 55 → **19** | 76 → **28** | 103 → **103** ✅ | 103 → **103** ✅ | 103 → **103** ✅ |
| Gate: prompts extracted / total assets | **36 / 180 (20 %)** | **30 / 261 (11 %)** | 232 / 250 | 239 / 257 | **267 / 267** |
| Gate RESULT | PASS *(vacuous)* | PASS *(vacuous)* | PASS | PASS | **PASS (meaningful)** |

**EP55 is the only file where the diversity PASS means anything** — 267 extracted = 210 stills + 42 motion + 3 thumb + 12 face = every single asset. The "EP55 had only 33 literal rows" state is gone and did not regress.

**BLOCKERs found:**
- **EP52 — 226 of 261 assets have no literal prompt** (194 body stills + 20 i2v seeds + 12 F). §8.1a says outright "下記は代表6例。残り37行は §4.5 の各 storyboard/tags を…SDXL 化". Codex improvises 87 % of the film's imagery.
- **EP51 — 142 of 180 assets have no literal prompt** (120 body stills + 10 i2v seeds + 12 F). §5.2 is an explicit "write the assigned number of unique prompts yourself" template instruction. Missing S144–S150 entirely.
- Both files additionally carry **mutually exclusive instructions for the same seed**: EP51 `M11` (§5.11 maps H006→M11 human `[HSTYLE]`; §8.1a gives M11 an abstract `[STYLE]` prompt) and EP52 `M35` (same pattern with H017). EP51 also has a flat contradiction between §5.2 ("All body 150 are face-free / person-free… anonymized people appear only in the §5.11 H-series") and §5.6a (which mandates 40 human-present body stills with `[HSTYLE]`) — opposite orders for the same 40 S numbers.
- **EP53 — F001–F012 (§5.13) are prose beats with no literal prompts**, and are declared "additive", absent from §3.1/§3.3 counts: 12 undeclared, improvised assets. Same undeclared-F pattern is present in EP51/EP52.

**Non-blocking but worth knowing:** EP53 and EP54 each have 18 `M##_src.png` marker lines with trailing commentary (`- \`M04_src.png\`  (= H001 · §5.11 …)`), which defeats the gate's `MARK` regex. The prompts *do* exist in full (content coverage 42/42 and 44/44), but the near-duplicate check is blind to those 18 seeds and their text bleeds into the preceding row. Cosmetic in effect, real if you rely on the gate. The duplicate `S001` in all five files is the §5.9 parser-contract example — harmless (first-occurrence-wins, and it is under the 40-char floor).

---

## 5. DEFECT CLASS 5 — deep-research rules retrofit gap (EP51 / EP52 only)

Both scripts predate `DEEP_RESEARCH_FINDINGS.v001.md` and were written to the retired canon: **cold open ~22 s → full ~10 s gold BrandOpening → thesis-paragraph OPENING** — the exact structure R-c/R-d retired. Scored against the MUSTs, with word→second conversion at each episode's ffprobe-measured pace.

| MUST | EP51 (189.7 wpm) | EP52 (190.9 wpm) |
|---|---|---|
| R-7 VO from frame 0 | PASS | PASS |
| R-8 first sentence declarative + named person + hard specific | **FAIL** — protagonist is "a man", unnamed | **FAIL** — "There was a three-year-old boy…"; no name, no date, no place |
| R-9 protagonist named ≤0:15 | **FAIL** — "Cameron Todd Willingham" at word 111 = **35.1 s** VO (≈45 s wall-clock, post-brand) | **FAIL** — "Michael Morton" at word 120 = **37.7 s** VO (≈48 s wall-clock) |
| R-9 opposing force ≤0:28 | PASS (13.9 s) | PASS (11.9 s) |
| R-10 BUT-loop before the sting | PASS w/ caveat — loop at 22.5–34.2 s but *spends its resolution* at 32.3 s | PASS — best-executed loop of the two (36.1 s, content withheld) |
| R-11 sting ≤5 s, fused title line | **FAIL** — full ~10 s-class gold BrandOpening | **FAIL** — same |
| R-12 post-brand = ONE escalating sentence + date/place anchor | **FAIL** — 97 w / **30.7 s** / 7 sentences, no anchor | **FAIL (worst)** — 140 w / **44.0 s** / 9 sentences; anchor arrives 47 s later, inside Act I; contains "is not just the story of… It's the story of…" self-description |
| R-13 first-45 s bans | **FAIL** — 3 consecutive concrete-free sentences at 44.6–49.3 s, then 2 more | **PARTIAL FAIL** — 51.9–63.5 s and 72.6–80.8 s are story self-description |
| **R-2** no ≥20 s person-action-free block in 60–180 s | **PASS (marginal)** — worst 11.1 s | **FAIL (hard)** — **20.8 s** block at 60.0–80.8 s (full run 28.9 s): the post-brand thesis paragraph IS the explanation block |
| R-14 mid reveal 45–60 % | PASS (54.7 %) | **FAIL (advisory)** — mid reveal lands at 38.8 % |
| R-14 primary reveal 65–85 % | PASS (74.4 %) | PASS (65.9 %) |
| R-14 resolves ≤92 % | **FAIL (marginal)** — new causal content at 91.2–92.1 % | PASS (91.4 %, 0.4 pt inside) |
| R-14 nothing new after 92 % | (same line as above) | **FAIL (minor)** — new biographical fact at 96.4 % |
| R-14 cold-open callback 70–90 % | **FAIL** — callbacks bracket the window at 63.8 % and 97.5 %, nothing inside | PASS (77.3 %) |
| **R-19** zero emotion-command imperatives | **FAIL — 7 hits** (`Hold on to that gap`, `Hold that thought`, `should frighten every single one of us`, `you need to see`, `Put it together`, `Sit with`, `Think about`) | **FAIL — 9 hits** (`once you understand`, `Now sit inside`, `I want you to really see`, `Imagine` ×2, `Think about the`, `feel the full weight of it`, `Do you see`, `understand what it represented`) + a format self-reference (`the show doesn't work if I pretend…`) + 4 narrator imperatives against a ≤2 cap |
| R-21 ≥5 specifics/min | PASS — **7.4/min** (EP56 = 14.4) | PASS — **8.1/min** |
| R-21 no >90 s without number/name/date | PASS — worst **71.8 s** (arson-indicator lecture, 289–360 s); numbers-only instrument 88.9 s, **1.1 s of margin** | **BORDERLINE FAIL** — worst 89.9 s (646–735 s); on the numbers/dates-only instrument **96.5 s at 815–911 s (48–54 %)**, over the cap, sitting exactly in the mid-video dip |
| R-3 / R-15 / R-24 | PASS / PASS / PASS | PASS / PASS / PASS |

**Root cause is shared and singular:** the retired thesis-paragraph OPENING is simultaneously the R-12 violation, the R-13 ban violation, the reason the protagonist is named 30+ s late, and (in EP52) the R-2 explanation block itself.

**Prioritized fix list — not applied (these are script rewrites, not documentation defects, and a script edit invalidates the paid VO under invariant 12).**

*EP51 — 8 MUST failures → 1 (callback) after fixes 1+2:*
1. **Rewrite lines 9–15** into COLD OPEN (~33 s, name at word 11 = 3.5 s, loop at 25.6 s) → `## BRAND STING (≤5 s, fused title line)` → `## OPENING (POST-BRAND)` = one escalating sentence + "Corsicana, Texas, December 1991." Net ≈ −58 words. Clears R-8/R-9/R-11/R-12/R-13.
2. **Delete all 7 emotion commands** (L14, L26, L34, L40, L44, L50, L74) with declarative replacements; keep exactly 2 narrator imperatives (L18, L96) and the L48 loop-bookkeeping line.
3. **Insert a cold-open callback at ≈80.5 %** (end of L92) — the "screaming in a Corsicana front yard" line.
4. **Break the 71.8 s specificity gap at 289–360 s** by attaching the indicators to named people and dated acts (Vasquez / Fogg / "his 1991 walk-through" / "indicator eleven").
5. **Move the 92.1 % new fact** (space heater / faulty wiring / a child with a match) back to ≈63 %.

*EP52 — 8 MUST failures → 2 (specificity zones, late new fact) after fixes 1+2:*
1. **Rewrite lines 9–15** the same way (name at word 14 = 4.4 s, "Michael Morton" at 23.3 s, loop at 25.5 s withholding content, post-brand one sentence + "Williamson County, Texas, August 13th, 1986."). Net ≈ −110 words. **This single edit also deletes R-2 Block A outright.** Companion edit required at L18/L20 (the anchor is now duplicated).
2. **Delete all 9 emotion commands** (L32, L42, L74, L86 ×2, L98, L122, L124, L136) + the L136 format self-reference; cut 2 of the 4 narrator imperatives (L44, L142) to reach the ≤2 cap.
3. **Break the two specificity dead zones** — insert dated/named anchors at L68/L70 (646–735 s) and L86 (815–911 s). ⚠ The suggested filing dates (1990/1993/1997) at L86 are **illustrative and must be verified against `EP52_morton_FACTS_LEDGER.v001` or replaced with ledger-backed dates before applying — invariant 1.**
4. **Remove the new biographical fact at 96.4 %** (L146) or re-seat the remarriage at ≈90 % (L138).
5. *(lowest priority, most invasive)* Pull the mid reveal from 38.8 % into 45–60 % by planting the withheld half of Anderson's instruction at ≈50 % (head of L86).

Applying fix 1 to either script changes narration word count and section topology, so **DESIGN timing and `durationInFrames` must be re-locked afterwards and the VO re-generated** — same procedure EP56 used in its R3+++ re-lock.

---

## 6. DEFECT CLASS 6 — `check_planning_package.py`

```
$ python scripts/check_planning_package.py 51 willingham
FAIL MISSING review: EP51_willingham_review_log.v001.md
RESULT: FAIL (1 blocking)

$ python scripts/check_planning_package.py 52 morton
FAIL MISSING review: EP52_morton_review_log.v001.md
RESULT: FAIL (1 blocking)

$ python scripts/check_planning_package.py 53 norfolk --require-r3
ok   F1 script_length gate PASS (1740-1860s)
ok   F2 narration body is CJK-free
ok   F3 hook->OP->acts structure markers present
ok   F5 'dochighlight' absent or explicitly banned
ok   F6 'DATE_STAMP' absent or explicitly banned
ok   F7 DESIGN carries figure-beat density budget
ok   F8 CODEX_A carries 1-scene-1-image / no-variants rule
ok   F9 CODEX_A carries the real-person likeness ban
ok   F10 review log has R1+R2
ok   F10 review log has substantive R3
ok   thumb: CODEX_A includes emotive-face thumbnail stills
info word-ish count (latin tokens): 5768
RESULT: PASS (0 warn)

$ python scripts/check_planning_package.py 54 flowers --require-r3
[all 11 ok lines identical]  info word-ish count (latin tokens): 6021
RESULT: PASS (0 warn)

$ python scripts/check_planning_package.py 55 burge --require-r3
[all 11 ok lines identical]  info word-ish count (latin tokens): 6076
RESULT: PASS (0 warn)
```

**EP51 and EP52 abort at the existence check — they have never run a single one of F1–F10.** No `--require-r3` run is possible; there is no review log at all. To find out what else is broken, the same F1–F9 logic was run against them directly (existence check bypassed, review log treated as absent — **no review log was fabricated**):

| | EP51 @ 20-min band (1140–1260 s) | EP51 @ default band | EP52 @ default band |
|---|---|---|---|
| F1 script_length | **FAIL** — 4,030 words, need 2,603–3,596, "LONG by 434" | PASS *(spurious — a 20-min film measured against the 30-min band)* | **FAIL** — 5,797 words, need 3,973–5,309, "LONG by 488" |
| F2 CJK-free | PASS | PASS | PASS |
| F3 structure markers | PASS | PASS | PASS |
| F5 dochighlight | PASS | PASS | PASS |
| F6 DATE_STAMP | **FAIL → fixed → PASS** (see below) | same | PASS |
| F7 figure-beat + AE hero | PASS | PASS | PASS |
| F8 / F9 / thumb | PASS / PASS / PASS | — | PASS / PASS / PASS |
| **F10 review rounds** | **FAIL — file does not exist** | — | **FAIL — file does not exist** |

Notes on the F1 failures, honestly stated:
- **EP51 @ 20-min band:** the gate counts 4,030 *file-level* words (narration body is 3,593; the rest is appendix). The **measured** film is 1,221.4 s = 20:21.4, inside a 19:00–21:00 band. This is a word-count-model over-prediction, not a real overrun.
- **EP52:** gate says "LONG by 488"; the **measured** film is 1,794.8 s = 29:54.8, inside 1740–1860. Same over-prediction.
- In both cases the correct disposition is a recorded **measured-overrides-model deviation** — *not* cutting the script (the VO is already paid and measured in band) and *not* loosening the gate.
- **EP51's F6 failure was real and is now fixed as a documentation defect.** DESIGN §4 stated the ban with the words "forbidden" and "no `DATE_STAMP`", neither of which is in the gate's prohibitive-context vocabulary, so the gate read the mentions as permissive. The prohibition itself was already present in six places across DESIGN and CODEX_B; the wording was changed to "BANNED — do not emit, do not implement". **This restates an existing prohibition in the canonical vocabulary; it does not weaken the check** (rule: no silently weakening validation).

---

## 7. `check_prompt_diversity.py` — full gate output

```
############ EP51_willingham
info prompts extracted: 36 | boilerplate tokens dropped: 9 (df>30%)
ok   no same-series pair reaches Jaccard 0.5
WARN 1 cross-series twin(s) (still/motion pairs are often intentional — eyeball them):
  0.53  M22 ~ S107   shared: bare, body, chamber, empty, gurney, restraint, shaft, straps
RESULT: PASS (0 dup-pairs, 0 generic)

############ EP52_morton
info prompts extracted: 30 | boilerplate tokens dropped: 15 (df>30%)
ok   no same-series pair reaches Jaccard 0.5
WARN 2 cross-series twin(s) (still/motion pairs are often intentional — eyeball them):
  0.78  M33 ~ S180   shared: absence, austin, empty, home, interior, life, lost, man
  0.50  M15 ~ S060   shared: bandana, bloody, blue, cloth, dark, drawer, edge, evidence
RESULT: PASS (0 dup-pairs, 0 generic)

############ EP53_norfolk
info prompts extracted: 232 | boilerplate tokens dropped: 12 (df>30%)
ok   no same-series pair reaches Jaccard 0.5
WARN 1 cross-series twin(s) (still/motion pairs are often intentional — eyeball them):
  0.51  M33 ~ S163   shared: asphalt, conditional, dawn, exactly, flat, free, gate, gray
RESULT: PASS (0 dup-pairs, 0 generic)

############ EP54_flowers
info prompts extracted: 239 | boilerplate tokens dropped: 10 (df>30%)
ok   no same-series pair reaches Jaccard 0.5
WARN 1 cross-series twin(s) (still/motion pairs are often intentional — eyeball them):
  0.55  M44 ~ S210   shared: abstract, dark, dust, fine, gold, last, macro, morning
RESULT: PASS (0 dup-pairs, 0 generic)

############ EP55_burge
info prompts extracted: 267 | boilerplate tokens dropped: 12 (df>30%)
ok   no same-series pair reaches Jaccard 0.5
WARN 3 cross-series twin(s) (still/motion pairs are often intentional — eyeball them):
  0.64  M09 ~ S054   shared: backlit, black, composed, dignified, distress, face, institutional, man
  0.59  M21 ~ S128   shared: clock, dial, dissolving, edge, fluorescent, hands, institutional, large
  0.50  M33 ~ S160   shared: black, calm, composed, dignified, face, federal, man, seen
RESULT: PASS (0 dup-pairs, 0 generic)
```

---

## 8. FIXES APPLIED IN THIS AUDIT (documentation only)

| File | Change |
|---|---|
| `EP51_willingham_DESIGN_ARCHITECTURE.v001.md` | §6: added **★ MEASURED-VO RE-LOCK** block (narrationSeconds 1,208.845 / durationInFrames **36,641** / total 1,221.367 s / ratio 1.0749 / mean_shot 3.060 / factory floor 41) + explicit runtime-band deviation notice requiring an APR. §5: added **ACT-COUNT NOTE** (3-act script vs 4 visual acts; no `ACT_4` narration section; `gen_narration_case.py` would refuse EP51) and corrected density 2.89 → 2.85/min. §4: SPLIT_COMPARE ×3 clarified (1 framing + 2 reversal). §0 and §4: DATE_STAMP/SEAM_TRANSITION prohibition restated as "BANNED" so F6 reads it (F6 now PASSes). |
| `EP51_willingham_CODEX_A_ASSETS.v001.md` | §2 re-locked to measured values; the 4-term `36,717` formula explicitly marked **SUPERSEDED — do not use** with the reason (8 s silent runway); measured per-section words added; ACT-COUNT WARNING added; "= still+factory+motion is the DISTINCT count" convention noted. §3.3 [2] 3.046 → **3.060**, [7] floor 40.1 → **40.3**, plus a re-check note that [1][3][4][5][6] are count ratios and unchanged. |
| `EP52_morton_DESIGN_ARCHITECTURE.v001.md` | §5: added **★ MEASURED-VO RE-LOCK** block (1,785.803 / **53,845 f** / 1,794.833 s / ratio 1.0675 / mean_shot 3.100), the "stale 54,129 = 9.5 s of picture with no audio" warning, measured per-act words with the ACT_4-is-densest correction, and an honest record of the F1 gate failure vs the measured in-band runtime. |
| `EP52_morton_CODEX_A_ASSETS.v001.md` | §2 re-locked; words 5,326 → **5,350 measured**; wpm 178 → **190.9 measured**; per-act table replaced with measured values + explanation of the +518-word over-statement and the wrong densest act. §3.3 [2] 3.117 → **3.100**, [8] 59.8 → **59.5**, + re-check note. |
| `EP53_norfolk_DESIGN_ARCHITECTURE.v001.md` | §5: added **★ MEASURED-VO CHECK** — measured 1,573.99 s speech, +9.1 s absorbed, total/frames explicitly unchanged (1,799.6 / 53,988), realised ratio 1.1434, density re-check 2.80/min ✓, measured per-act words. |
| `EP53_norfolk_CODEX_A_ASSETS.v001.md` | §2 per-act table updated to measured; TTS-measured block added stating no re-lock required. |
| `EP54_flowers_DESIGN_ARCHITECTURE.v001.md` | §5: added **★ MEASURED-VO CHECK** — measured 1,608.485 s, **pause budget 195.0 → 165.8**, total/frames unchanged, ratio 1.1087, density 2.83/min, and the **CORRECTION** that the CODEX_A per-act table labelled 実測 is over by +849 words. Instruction added that the 29.2 s comes off the distributed micro-pauses, not the act-turn breaths or ending ambience. |
| `EP54_flowers_CODEX_A_ASSETS.v001.md` | §2 per-act table replaced with measured values, with the false-実測 defect stated explicitly; TTS-measured block added. |
| `EP55_burge_CODEX_A_ASSETS.v001.md` | §2 aligned to the DESIGN's already-performed re-lock (gap 199.9 → **179.7**, total 1,791.0 → **1,842.0**, frames 53,730 → **55,260**, mean_shot 3.166 → **3.256**, wpm 178.1 → **170.4 measured**, words → 4,861 measured, per-act table → measured). §3.3 [2] and [8] re-derived from picture 1,833.0 + re-check note. |
| `EP55_burge_DESIGN_ARCHITECTURE.v001.md` | §4 density 2.75 → **2.67/min** at the re-locked runtime. |

**Deliberately NOT done:**
- No review log was created for EP51/EP52. Writing one would be exactly the F10 "review theater" failure the gate exists to catch. R1/R2/R3 must be genuinely performed.
- No script text was edited. The class-5 fixes are script rewrites that invalidate the paid VO (invariant 12) and need an owner decision first.
- No `CODEX_B_BUILD` or `bgm_plan` file was edited (outside the stated scope) — their stale numbers are logged as C-14 build-stage actions.
- No rendered media, build output, EP50/EP56 file was touched; no TTS was run.

---

## 9. NEEDS A BUILD-STAGE ACTION (cannot be closed in documentation)

| # | Episode | Action |
|---|---|---|
| B-1 | EP51 | Write literal prompts for the missing **120 body stills + 10 i2v seeds + 12 F**, resolve the M11 double-instruction and the §5.2-vs-§5.6a person/no-person contradiction, then re-run `check_prompt_diversity` (extracted count must ≈ 180). |
| B-2 | EP52 | Write literal prompts for the missing **194 body stills + 20 i2v seeds + 12 F**, resolve M35, then re-run the gate (extracted ≈ 261). |
| B-3 | EP51/EP52 | Perform real R1/R2/R3 reviews and produce the review logs; re-run `check_planning_package … --require-r3`. |
| B-4 | EP51/EP52 | Record the measured-overrides-model F1 deviation (measured runtime in band, word-count model out of band) as an explicit APR rather than cutting the script. |
| B-5 | EP51 | Runtime-band APR for a 1,221 s film against the 1740–1860 s ship gate. |
| B-6 | EP51 | Decide and document how the phantom `ACT_4` maps at build (visual act index vs script heading) for `validate_willingham_beats`, chapter markers, and the `t-a4` ACT_TITLE_CARD at t = 830.0 s. |
| B-7 | EP52/EP55 | Re-weight per-act asset density that was derived from the wrong act tables (EP52 ACT II over-provisioned; EP55 ACT_2/ACT_4 near-parity). |
| B-8 | EP54 | Re-cut the pause map to 165.8 s. Resolve the 18-vs-17 AE card count when CODEX_B is authored. |
| B-9 | EP53 | Declare F001–F012 in §3.1/§3.3 or drop them; write their literal prompts. |
| B-10 | EP51/52/55 | Propagate re-locked numbers into `CODEX_B_BUILD` (EP51 8 sites, EP52 9 sites) and `EP55_burge_bgm_plan.v001.md` (header). |
| B-11 | EP53/EP54 | Reformat the 18 `M##_src.png (= H0xx …)` marker lines so the diversity gate can see those seeds. |

---

## 10. VERDICT PER EPISODE

| Ep | Verdict |
|---|---|
| **EP51 willingham** | **NOT build-safe.** Two BLOCKERs (142/180 assets have no literal prompt; no review log = F10 never satisfied) plus a build-breaking frame-count contradiction and a phantom ACT IV threaded through asset, beat and AE docs. Re-lock and the doc contradictions are now fixed; the prompt package and the review are not. |
| **EP52 morton** | **NOT build-safe — worst file in the slate.** 226/261 assets would be improvised by Codex, no review log, and the stale `54,129` would have shipped 9.5 s of picture with no audio. Docs re-locked and corrected; the prompt package and the review remain. |
| **EP53 norfolk** | **Build-safe with one caveat.** Gates PASS with `--require-r3`, narration coverage clean, all checksums clean, VO drift absorbed correctly. Caveat: the 12 undeclared F-assets (B-9). |
| **EP54 flowers** | **Build-safe with two caveats.** Gates PASS, coverage clean, checksums clean, VO drift absorbed. Caveats: re-cut the pause map to 165.8 s (B-8) and resolve the 18-vs-17 AE deck at CODEX_B authoring. |
| **EP55 burge** | **Build-safe.** The only episode with a correct measured-VO re-lock already in place, the only one whose prompt-diversity PASS covers 100 % of assets (267/267), gates PASS with `--require-r3`. The CODEX_A/DESIGN runtime split (C-10) is now closed. |

## 11. WHAT WOULD HAVE SHIPPED BROKEN

1. **EP52: 194 of 215 body stills and 20 of 43 i2v seeds improvised by Codex** with no literal prompt — 87 % of the film's imagery unspecified, while `check_prompt_diversity` returned a green PASS on the 30 prompts that happened to exist.
2. **EP51: 120 of 150 body stills + 10 i2v seeds** the same way, plus S144–S150 absent entirely; the gate PASSed on 36 of 180.
3. **EP51 built to `durationInFrames = 36,717`** — 8 seconds of silent, voiceless film in front of the cold open, the exact defect the HOOK-AUDIO standard exists to prevent.
4. **EP52 built to `durationInFrames = 54,129`** — 9.5 seconds of picture with no audio before the endcard.
5. **EP55 built to two different runtimes** depending on which document the builder read (DESIGN 1,842.0 s / 55,260 f vs CODEX_A 1,791.0 s / 53,730 f — a 51-second, 1,530-frame divergence).
6. **EP54's asset density derived from a per-act word table labelled "measured" that over-stated the script by 849 words (17.6 %)**, over-provisioning every act and ACT II most.
7. **EP51 and EP52 shipped without a single review round** — F1–F10 never ran on either, because `check_planning_package` aborts on the missing review log and nobody had run it.
8. **EP51's `DATE_STAMP` ban invisible to the F6 gate** (stated as "forbidden", a word the gate does not recognise as prohibitive) — the ban was real but unenforced.
9. **EP51/EP52 opening on the retired pre-FINDINGS structure** — protagonist unnamed for 35–38 s of voice, a ~10 s brand OP instead of a ≤5 s sting, a 30–44 s thesis paragraph, and 7/9 emotion-command imperatives; EP52's post-brand thesis paragraph is itself the R-2 explanation block.
