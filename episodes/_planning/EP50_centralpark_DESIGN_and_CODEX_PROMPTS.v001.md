# EP50 — THE EXONERATED FIVE — DESIGN 本体 + CODEX_A/CODEX_B PROMPTS (v001)

### The channel's FIRST 60-minute film. Flagship design package: full second-by-second timeline, 7-act scene-by-scene storyboard, a **GO-HEAVY ~36-moment two-tier AE program** (24 standard cards + 12 bespoke set-pieces), ≥140 in-film figure-beat schedule, CODEX_A/B briefs, and the gate list. Generated FROM `EP50_centralpark_DESIGN_ARCHITECTURE.v001.md` (source of intent) + the locked script + STRUCTURE + verified facts. Where anything conflicts with the ARCHITECTURE on visual intent or quality bar, the architecture wins.

- Episode ID: `PD-2026-050-centralpark` · slug `centralpark` · EP50 · fps 30 · 1920×1080 · Composition id `Ep50Centralpark`
- Case: The Central Park Jogger case / **The Exonerated Five** (1989 attack · 1990 convictions · 2002 vacatur · 2014 & 2016 settlements). NOT a SCOTUS opinion — a 13-year human-justice saga.
- Central promise (the HOOK loop the whole film pays off): *"Five children. A room with the camera switched off. A confession to a crime not one of them committed — and the single strand of DNA that took it all back."*
- Subjects are **living public figures** (the five; Trisha Meili is a living survivor) or an **incarcerated convicted criminal** (Matias Reyes). **R2 (owner-revised, EP50): anonymized, non-identifiable human figures and faces ARE allowed** (dramatized generic stand-ins — CODEX_A §5.11). **Still absolute: NO likeness of any real person** (the five, Meili/the victim, Reyes, Trump, real detectives/judge/prosecutor), **NO victim depiction, the assault is NEVER depicted** and never described beyond "attacked and left for dead," no readable text/fake documents, and the youths are never framed as guilty. No Trump-ad art reproduction. The five and Reyes stay non-identifiable (symbolic silhouettes as default).
- The thesis the film will never violate: **the Five are innocent** (DNA identified Reyes as the sole source; he said he acted alone; all convictions vacated). The 2003 Armstrong Report is only ever a **rejected** counter-narrative — never an open question of guilt.

> **Companion docs (authoritative):** `EP50_centralpark_DESIGN_ARCHITECTURE.v001.md` (intent) · `EP50_centralpark_script.en.v001.md` (locked voice) · `EP50_centralpark_STRUCTURE.v001.md` (7-act map) · `EP50_centralpark_PRODUCTION_SPEC.v001.json` (numbers — **holds 56-min figures; §0.6 below RE-DERIVES the true-60:00 counts and shows both**) · `EP50_centralpark_facts.v001.json` + `..._FACT_VERIFICATION.v001.md` + `..._CITATIONS.v001.md` (the ONLY fact source; `confidence:high` only on-screen, else hedged/omitted).

---

## ★ THE ONE TRUTH OF THIS EPISODE — and the burned lessons this doc pre-empts

Every on-screen number, name, date, and phrase in this document traces to `EP50_centralpark_facts.v001.json` (CP01–CP35). Nothing was invented by hand. Where the SPEC still shows 56-min planning numbers, §0.6 re-derives the true-60:00 counts and states BOTH with the arithmetic.

| # | Prior-episode failure (MEMORY) | How THIS doc kills it up front | Ref |
|---|---|---|---|
| 1 | **`DATE_STAMP` / `SEAM_TRANSITION` crash the AE build** (`else throw "unsupported layout"`) | AE deck uses **only** the 6 layouts the builder implements: `ACT_TITLE_CARD / CENTER_STACK / MONEY_STACK / QUOTE_CARD / VOTE_SPLIT / SPLIT_COMPARE`. **Date cards = `CENTER_STACK`.** 0× DATE_STAMP, 0× SEAM_TRANSITION. Verified against `scripts/ae/build_cleveland_hero_cards.py`. | §3 |
| 2 | **`dochighlight` reads as a rendering bug** (flagged EP40/41/42) | `dochighlight = 0` across the whole film. Documents/lab-reports/signatures are `lowerthird` copy or symbolic stills, never `dochighlight`. | §4 |
| 3 | **Paper-slideshow** (still 100% → animation_mix FAIL) | still-cut share **0.4353 ≤ 0.45**; motion coverage **0.5647 ≥ 0.45**; factory 485 + motion 170 structurally guarantee it. | §5 |
| 4 | **AE cards counted toward density** (EP39/40) | `check_motion_density` counts `figures[]` in `centralpark_film.json` only. In-film design = **165 figure-beats** (floor 140/151). AE's **36 moments** composite AFTER and count 0. | §4 |
| 5 | **Invented numbers/quotes** (EP40 fabricated $580k) | Every burned figure is a `confidence:high` CP-id or is hedged verbatim to the ledger's `screen_phrasing`. **`votetally` and (emitted) `QUOTE_CARD` are not used — no confidence:high jury vote-split and no verified-verbatim quotation exist in the ledger** (a reserved QUOTE_CARD slot activates only if the citation pass locks one — see §3/§4 ★notes). | §3/§4 |
| 6 | **"Done" from one frame** (EP39–41; EP39-41 eyeball) | FULL **60-minute, 3× eyeball** is a hard gate before "done." measured > estimated. | §7 |
| 7 | **56-min numbers silently kept** | §0.6 re-derives the 60:00 counts from the SPEC 5×-arithmetic and shows old→new side by side. | §0.6 |
| 8 | **Phantom AE layouts / wrong-case deck / empty manifest** (crash; Codex build unreliable) | Owner directive = **go heavy on AE (~36 moments, 2 tiers)**. Tier B adds **NEW layouts implemented for real**, each `--dryrun`-proven and added to `check_AE_layouts` allowlist BEFORE use — we IMPLEMENT+PROVE, never reference phantoms. DATE_STAMP/SEAM_TRANSITION still 0. AE deck id/layout/CP-id one-to-one with CODEX_B (`validate_centralpark_beats`). Manifest fully populated with `public_path`. | §3/§6/§7 |
| 9 | **Zero real stock used** (EP48/49 = AI stills + AI-i2v only; downloaded library left unused) | Weave the real stock library (`H:\pd-media\assets\stock` · 74 clips + 155 stills · pexels/pixabay · commercial-OK) into the footage lane **semantically** (courthouse/NYC/precinct/prison/lab/protest/dawn matched to beats) and **prefer real footage over AI-i2v wherever a relevant clip exists** (real footage also avoids i2v warping); AI-i2v reserved for abstract/symbolic beats (R-FACE). Color-match to the AI stills with one neutral grade. **counts unchanged.** | CODEX_B §5.8 / CODEX_A §7.4a |
| 10 | **Milky global wash + scanline over every frame** (EP48/49 rejected: "全体的に画像に曇りがかかってる") | **NO global haze/fog/vignette-wash and NO global scanline/CRT texture.** Image stays clear + high-contrast; any grade minimal + neutral. Overlays are per-beat local accents only; the Act-3 videotape TV-glow scanline is a **local diegetic motif on that beat**, not a global veil. | CODEX_B §5.9 |

---

# §0 — ENVIRONMENT / COMPOSITION / REMOTION SETTINGS (CLAUDE.md §0 準拠)

## 0.1 本編 `Ep50Centralpark` の Composition（★本編の正）

| 項目 | 値 |
|---|---|
| `id` | **`Ep50Centralpark`**（Root.tsx に `CaseFilm` で登録。切り詰め・綴り違い・大文字化は BLOCKER） |
| 解像度 | **1920 × 1080** |
| `fps` | **30**（全フレームは `Math.round(30 × 秒)`・直書き禁止） |
| `hookSeconds` | **8.0**（BrandOpening 前の cold-open。§0.3 の durationInFrames 第1項） |
| `OPENING_SEC` | **3.5**（BrandOpening title・"THE EXONERATED FIVE"） |
| `ENDCARD_SEC` | **9.0**（BrandEndcard） |
| `narrationSeconds` | **3606.0（provisional）** — ★FINAL は測定 TTS / forced-align。§0.3 参照 |
| `durationInFrames` | **`caseFilmDurationInFrames(centralparkFilm, 30)` = 108,795（provisional）** — 4項の実関数で算出（§0.3） |
| component | `remotion/src/compositions/CaseFilm.tsx`（既存の汎用 `CaseFilm` を再利用・`Bookends.tsx` の `BrandOpening`/`BrandEndcard` を import・fork 禁止） |
| data | `remotion/src/data/centralpark_film.json`（`scripts/build_centralpark_film.py` で再生成できる状態＝git 未追跡） |

**Root.tsx 登録（CODEX_B が実装）:**
```tsx
import {centralparkFilm} from './data/centralpark_film.json';
import {caseFilmDurationInFrames} from './lib/caseFilmDuration';
// ...
<Composition
  id="Ep50Centralpark"
  component={CaseFilm}
  width={1920} height={1080} fps={30}
  durationInFrames={caseFilmDurationInFrames(centralparkFilm, 30)}  // = 108795 (provisional)
  defaultProps={{film: centralparkFilm}}
/>
```

## 0.2 依存パッケージ（CLAUDE.md 必須）
```bash
cd C:\Users\aab15\Documents\prime-documentary\remotion
npm i @remotion/motion-blur     # Trail によるモーションブラー（必須）
```

## 0.3 durationInFrames — 4項の実関数（★手書きで数値を入れず関数で算出）

```
durationInFrames = round(hookSeconds·30) + round(OPENING_SEC·30) + ceil(narrationSeconds·30) + round(ENDCARD_SEC·30)

provisional @ narrationSeconds = 3606.0:
  = round(8.0·30)   = 240
  + round(3.5·30)   = 105
  + ceil(3606.0·30) = ceil(108180.0) = 108180
  + round(9.0·30)   = 270
  = 108,795 frames  =  3626.5 s  =  60:26.5 total runtime
```
> ★ **narrationSeconds = 3606.0 は provisional**（10,715 words ÷ 178.3 wpm × 60 = 3605.7 → 3606.0）。**FINAL は VO master が存在してから forced-align で測る実測値**で、SPEC + Root を更新する。3606 と実測が乖離したら CODEX_B は `centralpark_film.json` の `narrationSeconds` を実測で上書きし、同関数で再計算して assert する。**VO onset（最初の発話語）= 11.5s ちょうど**（hookSeconds 8.0 + OPENING 3.5）。hookSeconds が 0 になると全体が 8s desync するので assert（§0.5）。

## 0.4 remotion.config.ts（CLAUDE.md §0 正典値・EP41〜49 と同一・書き換えない）
```ts
import {Config} from '@remotion/cli/config';
import os from 'os';
Config.setVideoImageFormat('png');            // png
Config.setConcurrency(os.cpus().length);      // 全コア並列 concurrency最大
Config.setCodec('h264');                       // H.264 libx264（NVENC 禁止）
Config.setCrf(16);                             // CRF16
Config.setX264Preset('slow');
Config.setPixelFormat('yuv420p');              // yuv420p
Config.setColorSpace('bt709');                 // bt709
Config.setAudioCodec('aac');                   // aac
Config.setAudioBitrate('320k');                // 320k
Config.setChromiumOpenGlRenderer('angle');     // GPU=angle
```
> 本編レンダは `--public-dir=public_slim --concurrency=4`（**public→public_slim へ img/factory/motion/audio 全メディアをコピー staging**＝EP45事故回避）。★60分は ~108,795 フレーム＝multi-hour render。**開始前にマシン状態を確認**（heavy-job preflight）。**public_slim ディスクは 12分エピの ~4–5倍**を先に確保（~1,000 distinct assets：still 430 + factory 485 + motion 85 + overlay）。

## 0.5 タイムアンカー（★全て 11.5s から。desync 防止）
- **VO / captions / BGM VO-OFF ducking / AE `film_offset` = 11.5s ちょうど**（hookSeconds 8.0 + OPENING 3.5）。BGM offset = **11.5**（CODEX_B）。
- 図表(`figures[]`)・AEビートは **body/narration-relative**（narration-relative 0 = 絶対 11.5s）。
- **assert `hookSeconds == 8.0`**（0 になると 8s desync）。

## 0.6 ★60:00 への数値の再導出（SPEC は 56-min のまま — OLD → NEW を両方示す）

SPEC は narration 3,360s(56.0min) の cut。**TARGET は真の 60:00**（script = 10,715 words ≈ 60.1 min）。SPEC の 5×-arithmetic をそのままスケール比 **3606/3360 = 1.0732** で伸ばし、still-share ≤0.45 / first-use ≥0.70 を保つクリーン値に丸める。**silently 56-min を残さない。**

| 軸 | SPEC(56-min, OLD) | **EP50(60:00, NEW)** | 算出 |
|---|---:|---:|---|
| Script words | 9,970 | **10,715** | script v001 実語数（band 10,500–10,900） |
| narrationSeconds | 3,360.0 (56.0min) | **3,606.0 (60.1min)** | 10,715 ÷ 178.3 wpm × 60 = 3605.7 → 3606.0 |
| 総尺 total_mmss | 56:20 | **60:26.5** | 240+105+108180+270 = 108,795 f / 30 |
| durationInFrames | 101,415 | **108,795** | 4項関数（§0.3） |
| total_cuts | 1,080 | **1,160** | 505+485+170（下記） |
| mean_shot | 3.11 s | **3.109 s** | 3606 / 1160 |
| still: distinct / cuts | 400 / 470 | **430 / 505** | 470×1.0732=504.4→505・distinct 400×1.074→430・mean 1.174 ≤ cap2 |
| factory: distinct / cuts | 450 / 450 | **485 / 485** | 450×1.0732=482.9→485・cap1 |
| motion(i2v): distinct / cuts | 80 / 160 | **85 / 170** | 160×1.0732=171.7→170・distinct 80×1.074→85・mean 2.0 ≤ cap2 |
| distinct_total | 930 | **1,000** | 430+485+85 |
| first_use_share | 0.861 | **0.8621** | 1000/1160 ≥ 0.70 floor ✓ |
| still_share_of_cuts | 0.4352 | **0.4353** | 505/1160 ≤ 0.45 cap ✓（余裕 0.15%pt） |
| motion coverage | 0.5648 | **0.5647** | (485+170)/1160 ≥ 0.45 ✓ |
| in-film beats floor | 140 | **151** | ceil(60.1 × 2.5/min) = 151（設計値 **165**・§4） |
| AE moments（owner: GO HEAVY） | ~22 | **36**（Tier A 24 + Tier B 12） | ~22 の punctuation ではなく、bespoke set-piece を含む 2-tier program（§3・"AEをガッツリ"） |
| Render frames | 101,415 | **108,795** | 同上 |

**検算（CODEX_B は自分で再計算して一致を assert）:**
```
cuts:      505(still)+485(factory)+170(motion) = 1,160 = total_cuts ✓
distinct:  430+485+85 = 1,000
first_use: 1000/1160 = 0.8621 ≥ 0.70 ✓
still-share:505/1160 = 0.4353 ≤ 0.45 ✓
motion-cov:(485+170)/1160 = 0.5647 ≥ 0.45 ✓
mean_shot: 3606/1160 = 3.109 s ≤ 7.0 max ✓
```

## 0.7 パレット（`remotion/src/brand.ts` から import・ハードコード禁止・EP41〜49 と被らないレーン）

```
INK      = #0A0A0C  = [0.039, 0.039, 0.047]   ルート背景（サムネ bg と一致・夜の park / institutional gravity）
ACCENT   = #2F9FC4  = [0.184, 0.624, 0.769]   ★cold forensic steel-cyan（lab光・DNAバンド・cursor・cold edge。Acts1–4 は SPARINGLY、Act5 の DNA hinge で FLOOD）
BONE     = #EDEDE8  = [0.929, 0.929, 0.910]   type（bone-white）
DAWN     = #C98A3C  = [0.788, 0.541, 0.235]   ★dawn-amber — ONLY Act6 exoneration & the close。他区間で 1px も使わない（意味を持たせる）
WHITE    = #F5F7FA  = [0.961, 0.969, 0.980]
SILVER   = #C8CDD6  = [0.784, 0.804, 0.839]   AI開示テキスト
```
> レーン分離: EP41 gold / EP42 blue / EP43 amber / EP44 teal / EP45 crimson / EP46 green / EP47 civil-violet / EP48 / EP49 somber-plum を **1px も流用しない**。EP50 の色は cold steel-cyan `#2F9FC4`（hue ~197°・EP44 teal より青く冷たい）＋ 唯一の暖色 dawn-amber `#C98A3C`（Act6/close 限定）。**CODEX_B は OP props / AEカード accent / サムネ accent を必ず `#2F9FC4`**。

---

# §1 — 全区間 SECOND-BY-SECOND TIMELINE（0 → 3626.5s・fps30・per-beat frames/move/easing/damping/stagger/Trail）

**算出基準:** `narrationSeconds = 3606.0`（provisional master・手計算で上書きしない）を `centralpark_film.json` に入れる。フレーム = `Math.round(30 × 秒)`。**等速線形ゼロ・opacity 単独ゼロ・静止フレームゼロ**（4+秒の静止は FAILURE。意図した breath は全編 max 3・各 ≤2.5s）。text 見出し/figures は `overflow:hidden` 親＋子 `translateY(110%→0)` の spring mask 切れ上がり（`damping:16,mass:1`・stagger `f(0.10)=3f/文字` 目安）を基本形。still は Ken Burns（`scale 1.00→1.08`＋drift ±24px・`Easing.out(Easing.cubic)`）を全長。**fast move（Trail 対象）は「Trail」列に明記。**

## 1.0 幕の絶対ウィンドウ（★この表が唯一の正・planning anchor・FINAL は測定 TTS）

| # | ブロック | 役割 | 秒（開始–終了） | 開始f–終了f | 語数(目安) |
|---|---|---|---|---|---|
| 0 | **HOOK cold-open**（SILENT・scored） | `hook` | 0.0 – 8.0 | 0 – 240 | 0（発話なし・type のみ） |
| 1 | **OPENING title** "THE EXONERATED FIVE" | `opening` | 8.0 – 11.5 | 240 – 345 | 0 |
| 2 | **HOOK spoken**（VO onset 11.5s） | `body` | 11.5 – 25.0 | 345 – 750 | ~40 |
| 3 | **ACT 1 — The Night** | `body` | 25.0 – 442.5 | 750 – 13,275 | ~1,250 |
| 4 | **ACT 2 — The Interrogations**（最長・moral engine） | `body` | 442.5 – 1161.0 | 13,275 – 34,830 | ~2,150 |
| 5 | **ACT 3 — The Trials** | `body` | 1161.0 – 1696.0 | 34,830 – 50,880 | ~1,600 |
| 6 | **ACT 4 — The Lost Years** | `body` | 1696.0 – 2264.0 | 50,880 – 67,920 | ~1,700 |
| 7 | **ACT 5 — The Confession & the DNA** | `body` | 2264.0 – 2815.5 | 67,920 – 84,465 | ~1,650 |
| 8 | **ACT 6 — Exoneration & Reckoning** | `body` | 2815.5 – 3300.0 | 84,465 – 99,000 | ~1,450 |
| 9 | **ACT 7 — What a Confession Is Worth**（second-person turn） | `body` | 3300.0 – 3617.5 | 99,000 – 108,525 | ~950 |
| 10 | **BrandEndcard** | `ending` | 3617.5 – 3626.5 | 108,525 – 108,795 | 0 |

> **VO onset = 11.5s ちょうど**（body/figures/AE の offset）。**幕秒は planning anchor**（script 語数を 178.3 wpm で割った値をスケールして 3606s に収めた）。**FINAL は forced-align の実測**で CODEX_B が幕境界を更新する。総尺 108,795f は 4項関数の値。

## 1.1 HOOK cold-open + OPENING（0 – 11.5s / f0 – 345）— 「restraint, promised」

| 区間(秒) | f開始–終了 | 画（象徴のみ・顔なし） | 主アニメ（プロパティ・移動量） | easing / damping | stagger | Trail |
|---|---|---|---|---|---|---|
| 0.0–2.2 | 0–66 | 黒 → 単一の cold-cyan の光が empty chair を見つける | spotlight radial `r 0→0.30`・光量 `opacity 0→70`＋chair still `scale 1.00→1.03` | `Easing.out(Easing.cubic)` | — | — |
| 2.2–4.6 | 66–138 | steel table・読めない壁時計・**OFF の REC ランプ** | REC dot が **一度だけ** tick（`scale 1.0→1.18→1.0`・色は消灯 grey、点かない）＋highlightring が REC を囲む | spring `damping:18` | — | — |
| 4.6–8.0 | 138–240 | 一行の type が mask 切れ上がり："FIVE CHILDREN." | `overflow:hidden`＋`translateY(110%→0)`・BONE・hold | spring `damping:16,mass:1` | 3f/語 | — |
| 8.0–11.5 | 240–345 | **OPENING**："THE EXONERATED FIVE" cold cyan on ink・hold・cut | title mask 切れ上がり＋accent underline `scaleX 0→1`（ワイプ）・cut は hard | spring `damping:16` / `Easing.out(Easing.cubic)` | 3f/語 | underline **✓** |

> HOOK は**発話ゼロ・完全な restraint**（low cello + 単一の metallic tick のみ・§ Audio）。字幕キューを置かない。REC-OFF ランプ＝映画の signature image（Act2 で echo、Act6/7 で ON に反転）。

## 1.2 HOOK spoken（11.5 – 25.0s / f345 – 750）— VO onset

| 区間(秒) | f開始–終了 | 画 | 主アニメ | easing/damping | stagger | Trail |
|---|---|---|---|---|---|---|
| 11.5–17.0 | 345–510 | empty chair から広がる room・OFF REC を再提示 | still push-in `scale 1.00→1.05`／`lowerthird` 開示 `AI-assisted visualization`（右下） | `Easing.out(Easing.cubic)` / spring `damping:20` | — | — |
| 17.0–21.5 | 510–645 | 冷たい lab の cold-cyan の一筋（DNA motif を SPARINGLY 先出し） | 単一 cyan edge が横切る `translateX -40→40px`・KB | `Easing.inOut(Easing.sin)` 微動 | — | — |
| 21.5–25.0 | 645–750 | 五つの descending silhouettes（子供・顔なし）が cold rim light に一瞬 | 5影が下から stagger 立ち上がり `translateY 40→0px`・rim `opacity 0→60` | spring `damping:16` | **4f/影**（5要素スタッガー） | 立ち上がり **✓** |

## 1.3 ACT 1 — THE NIGHT（25.0 – 442.5s / f750 – 13,275）— cold, wide, observational

**モーション性格:** slow push-in、都市を texture として（subway/headlines を abstracted mass に）。one spike＝二つの捜査が一つの file に collide する hard graphic snap。AE `t-a1`（ACT_TITLE_CARD）は 25–33s 付近に composite（body-relative）。

| 区間(秒) | f開始–終了 | 画（象徴・R2・assault は描かない） | 主アニメ | easing/damping | stagger | Trail |
|---|---|---|---|---|---|---|
| 25.0–70 | 750–2100 | 1989春のNY＝braced city。subway car の graffiti を scar tissue の texture に、遠い news の明滅 | 連続カット（mean 3.1s）・各 still KB `scale 1.00→1.07`/drift ±22px・factory の街 ambient を撒く | `Easing.out(Easing.cubic)` | — | — |
| 70–120 | 2100–3600 | 4/19 の夜の park を**抽象**で（treeline・a lamp・cold・crime は描かない）。restless な teenagers の後ろ姿の mass | routemap（park geography・**abstracted, NO crime location**）が薄く draw・silhouettes drift | `Easing.out(Easing.cubic)` / spring `damping:18` | 3f | draw **✓** |
| 120–175 | 3600–5250 | 五人が別々に park にいる＝descending heights の 5影（14/14/15/15/16）・まだ「a group」ではない | `kinetic` name/age stack が 1名ずつ mask 切れ上がり（**AE `c-fivechildren` は別枠**） | spring `damping:16` | **4f/名** | — |
| 175–230 | 5250–6900 | 102nd St cross drive 付近で attack が起きた park の別区画（**現場は描かない・被害者を描かない**）。coma 12日→記憶の空白＝a vacuum | 画面が cold に沈む（grade shift）・空の chair の echo・`stat` "12 DAYS"（CP04 high・coma） | `Easing.inOut(Easing.sin)` / spring `damping:20` | — | — |
| 230–300 | 6900–9000 | precinct が boys と parents で満ちる。二つの捜査が静かに一つになる | **the one spike**：`mechanism:faultsplit`-inverse＝"park trouble" と "the attack" の二線が hard snap で 1本の file に collide（早い） | spring `damping:14` | — | **✓✓**（hard snap） |
| 300–360 | 9000–10,800 | proximity＝唯一の糸。no witness / no description / no physical evidence | `compbars` [{"WITNESSES",0},{"PHYSICAL EVIDENCE",0},{"PROXIMITY",1}]（象徴・中立）barX `scaleX 0→1` origin-left | spring `damping:18` | — | — |
| 360–420 | 10,800–12,600 | the hinge：questioning 開始時、jogger 攻撃に繋がる物証は**ゼロ**。evidence が「作られる」機械の予兆 | still push-in `scale 1.00→1.08`／`lowerthird` "NO PHYSICAL EVIDENCE — AT THE MOMENT OF QUESTIONING"（AE `c-noevidence` は別枠）／cyan cursor が blink | `Easing.out(Easing.cubic)` / spring `damping:16` | — | cursor **✓** |
| 420–442.5 | 12,600–13,275 | 3AM の子供にとっての police station。lab に送られた biological evidence が「返ってくる…match しない」予兆で幕引き（open loop） | cold-cyan の DNA band が一瞬 glimpse され ignored（Act5 の伏線）・`kinetic:emphasis` "IT WILL MATCH NONE OF THEM"（["NONE"]） | spring `damping:16` | 3f/語 | band glint **✓** |

## 1.4 ACT 2 — THE INTERROGATIONS（442.5 – 1161.0s / f13,275 – 34,830）— the engine · 最高密度

**モーション性格:** the tightest, most claustrophobic。close, handheld-feel micro-drift；the clock；story fragments が detective silhouette → child silhouette へ migrate（false-evidence ploy の可視化）。five confession pages が stack、各々が次を cite する house of cards。**この幕が figure-beat 最高密度（~36 beats）。** AE `t-a2`(ACT_TITLE) 443–451s、`c-fivechildren`(CENTER_STACK)、`c-sevenhours`(CENTER_STACK)、`cmp-fedsigned`/`cmp-confdna`(SPLIT_COMPARE) を分散 composite。

| 区間(秒) | f開始–終了 | 画 | 主アニメ | easing/damping | stagger | Trail |
|---|---|---|---|---|---|---|
| 442.5–470 | 13,275–14,100 | 幕頭：the room（general one）。empty chair・windows なし・変わらない光・読めない clock | acttitle 系は AE `t-a2`。room に slow handheld micro-drift `translateX ±10px`（`Easing.inOut(Easing.sin)`・静止ゼロ） | spring `damping:18` | — | — |
| 470–540 | 14,100–16,200 | "You are fourteen." second-person。soda・母は来ない（renewed promise＝a technique） | 読めない clock の hand が imperceptibly 進む・`lowerthird` "AT LEAST SEVEN HOURS — NONE OF IT RECORDED"（CP08 firm high・AE `c-sevenhours` 別枠） | spring `damping:20` | — | — |
| 540–620 | 16,200–18,600 | detective は shouting しない。"on your side"・"the others already talked" | story fragment の type が **detective 影 → child 影へ migrate**（`arrow` from detective to child・`translateX` slide）・`kinetic` "JUST SAY IT" | spring `damping:16` / `Easing.out(Easing.cubic)` | 3f/語 | migrate **✓** |
| 620–700 | 18,600–21,000 | 右答え/誤答が detective の顔に読める＝「the room が yes を作る」 | `mechanism:gears`（the interrogation machine：pressure→yield）・歯車が噛む | spring `damping:16` | — | gears **✓** |
| 700–780 | 21,000–23,400 | the science of false confession（juveniles far more readily） | `stat` "FIVE CHILDREN"（CP05 high）＋`kinetic` "AGES 14 TO 16"（CP05 high・AE `c-fivechildren` 別枠） | spring `damping:16` | 4f | — |
| 780–870 | 23,400–26,100 | 技法①**false-evidence ploy**（嘘が許される）を14歳に | `compbars` [{"WHAT HE COULD CHECK",0},{"WHAT HE WAS TOLD",1}]（象徴・中立）・cyan で | spring `damping:18` | — | — |
| 870–960 | 26,100–28,800 | 技法②**minimization**（"you just held an arm"）＝the gentle trap | `mechanism:closingdoor`（soft admission が full confession に閉じる）・扉が静かに閉じる | spring `damping:16` | — | door **✓** |
| 960–1050 | 28,800–31,500 | multiply by five：各 boy が others を name → "corroboration"。house of cards | five confession pages が stack、各々が次を cite する（`timeline`-風の連鎖・pages が積む `translateY`）＋`kinetic:emphasis` "THE STORY, FED IN"（["FED"]） | spring `damping:14` | **3f/page** | stack **✓** |
| 1050–1110 | 31,500–33,300 | 物証は confession の逆を「file の中で」言い続ける。rape kit・semen が五人を exclude | **the contradiction**：`compbars` [{"CONFESSIONS",5},{"DNA MATCHES",0}]（CP10/CP12 high）・0 が cyan で残る（AE `cmp-confdna` SPLIT_COMPARE 別枠） | spring `damping:18` origin-left | — | — |
| 1110–1161 | 33,300–34,830 | the ghost theory（unknown 6th）で gap を papered over。2002 に ghost が名を告げる予兆（open loop） | `arrow` が「evidence → one unaccounted man」を指す・`kinetic` "THEY SIGNED TO GO HOME"／幕引き cyan sink | spring `damping:16` / `Easing.out(Easing.cubic)` | 3f/語 | — |

> ★Act2 の false-evidence/minimization 区間（780–960s）と confession-vs-DNA（1050–1110s）が figure 最密（`mechanism`×2, `compbars`×2, `arrow`, `kinetic`, `stat`）。20秒超の平坦区間ゼロ。

## 1.5 ACT 3 — THE TRIALS（1161.0 – 1696.0s / f34,830 – 50,880）— the machine of publicity

**モーション性格:** headlines を oppressive kinetic wall に。Trump-ad は **単一の dated context card**（**ad art を絶対に再現しない**）。the scale tips。videotape motif（TV glow・play triangle＝confession performed）。AE `t-a3`(ACT_TITLE) 1161–1169s、`c-papersfirst`(CENTER_STACK)、`c-trumpad`(CENTER_STACK)、`cmp-sentence`(SPLIT_COMPARE) を分散。

| 区間(秒) | f開始–終了 | 画 | 主アニメ | easing/damping | stagger | Trail |
|---|---|---|---|---|---|---|
| 1161–1210 | 34,830–36,300 | 幕頭：the case is tried in the newspapers first | AE `t-a3`。headline mass が oppressive kinetic wall で押し寄せる（`kinetic:maskslide` 複数行）・"wilding"＝**press の label**（CP06 medium・"a word the press seized on"） | spring `damping:16` | 3f/語 | wall **✓** |
| 1210–1270 | 36,300–38,100 | 1989年5月1日 Trump の full-page ad（**art は再現しない**・dated context のみ） | `lowerthird` "MAY 1, 1989 · A FULL-PAGE AD DEMANDED THE DEATH PENALTY · REPORTEDLY ~$85,000 · IT DID NOT NAME THE FIVE"（CP13 high・cost hedged・AE `c-trumpad` CENTER_STACK 別枠） | `Easing.out(Easing.cubic)` / spring `damping:20` | — | — |
| 1270–1360 | 38,100–40,800 | 二つの1990 trial。evidence は astonishingly thin：no eyewitness / no weapon / DNA matches none | `compbars` [{"EYEWITNESS",0},{"WEAPON",0},{"DNA MATCH",0},{"CONFESSIONS",5}] cyan・"1989 · TRIED IN THE PAPERS FIRST"（AE `c-papersfirst` 別枠） | spring `damping:18` origin-left | — | — |
| 1360–1430 | 40,800–42,900 | the tapes：calm teenager が自分の言葉で crime を recite。TV glow・play triangle | videotape motif：TV glow の scanline drift＋play triangle が `scale 0→1` pop（confession performed）・cyan cursor（**★このスキャンラインは videotape の局所モチーフ＝このビート限定。全画面の恒常 scanline/wash にしない＝CODEX_B §5.9**） | spring `damping:16` | — | triangle **✓** |
| 1430–1500 | 42,900–45,000 | defense case（DNA matches no one・contradictions）。doubt loses | the scale が wrong way に tip（`mechanism`-scale：confession 側に傾く・faultsplit 変奏） | spring `damping:16` | — | tip **✓** |
| 1500–1560 | 45,000–46,800 | families never wavered（Harlem の親たち）。moral panic が love を guilt の証拠に変える | 5影の後ろに親影の row（顔なし）・slow push-in・`lowerthird` "THE FAMILIES NEVER WAVERED" | `Easing.out(Easing.cubic)` | 4f | — |
| 1560–1640 | 46,800–49,200 | verdict：guilty（但し acquittals mixed in on the most serious counts） | `lowerthird` "CONVICTED — YET ACQUITTED OF ATTEMPTED MURDER"（CP17 medium→hedged・**votetally は使わない**：jury split は confidence:high に無い） | spring `damping:18` | — | — |
| 1640–1696 | 49,200–50,880 | 四人＝juvenile 5–10yrs／Korey Wise, 16＝tried as an ADULT。a birthday の accident が destroyed life に。Rikers（open loop：who was Korey?） | `cmp-sentence`(SPLIT_COMPARE 別枠) "FOUR: JUVENILE, 5–10 YRS" ↔ "KOREY WISE, 16: AS AN ADULT"（CP18 high）・Korey 影だけ別方向へ | spring `damping:16` / `Easing.out(Easing.cubic)` | — | — |

## 1.6 ACT 4 — THE LOST YEARS（1696.0 – 2264.0s / f50,880 – 67,920）— motion slows, then names, then Korey

**モーション性格:** モーションが SLOW & LENGTHEN（**唯一 hold が 3.5–4s に届く区間・earned・全編の意図的 breath 3回の一部**）。四人の individual portrait で再び quicken、最後に Korey の long, quiet, aging silhouette。solitary＝frame 自体が narrow に。cell window に seasons が横切る（**literal calendar-flip を禁止**）。AE `t-a4`(ACT_TITLE)、`cmp-yearsserved`(SPLIT_COMPARE)。

| 区間(秒) | f開始–終了 | 画 | 主アニメ | easing/damping | stagger | Trail |
|---|---|---|---|---|---|---|
| 1696–1760 | 50,880–52,800 | 幕頭：montage を resist。lost の years に sit する。単一 cell window に seasons が横切る | AE `t-a4`。cell window の光の色温度が季節で slow shift（**calendar-flip 禁止**）・**earned breath**（hold 3.8s×1・≤2.5s ルールの意図的例外＝この幕限定） | `Easing.inOut(Easing.sin)` | — | — |
| 1760–1850 | 52,800–55,500 | 何が奪われたか：a person is assembled する years（school/first job/driving/first love）＝cell で serve | single silhouette が窓辺で imperceptibly aging・`kinetic` "THE YEARS IN WHICH A PERSON IS ASSEMBLED" | `Easing.out(Easing.cubic)` / spring `damping:18` | 3f/語 | — |
| 1850–1930 | 55,500–57,900 | 四人 younger は ~6–7年で home。だが "convicted rapist" の label が every door で先回り | `bar` YEARS-SERVED：4本 ~6–7・cyan（CP19 high・"~"）＋`cmp-yearsserved`(SPLIT_COMPARE 別枠) "FOUR: ~6–7 YRS EACH" ↔ "KOREY WISE: ~13 YRS" | spring `damping:16` origin-left | 4f/本 | — |
| 1930–2010 | 57,900–60,300 | "the four" という語を refuse：Richardson(14)/Santana(14)/McCray(15)/Salaam(15) を individ に | 4影が 1名ずつ step-forward `translateY 30→0`＋各 `lowerthird` の detail（顔なし）・re-quicken | spring `damping:16` | **4f/名** | — |
| 2010–2110 | 60,300–63,300 | そして Korey Wise。adult system に 16歳。beaten・facility 転々・long solitary | Korey 影だけ recurring spine として残る・frame が narrow に（左右 letterbox が寄る＝solitary） | `Easing.out(Easing.cubic)` / spring `damping:20` | — | — |
| 2110–2180 | 63,300–65,400 | parole の remorse を Korey は言わない（did not do it, will not say it）。truth を選び cell に残る | 単一影の hold（**earned breath** 2.4s）→ わずかな aging drift。restraint | `Easing.inOut(Easing.sin)` | — | — |
| 2180–2264 | 65,400–67,920 | 90s→2000s。case は ancient history。upstate で accident が近づく（Korey の近くに 33-to-life の男）。open loop | `timeline` "THAT NIGHT (1989) → … → 2002"（returns/extends・cyan）／`kinetic:emphasis` "ONLY BY ACCIDENT"（["ACCIDENT"]） | spring `damping:16` | 3f/語 | — |

## 1.7 ACT 5 — THE CONFESSION & THE DNA（2264.0 – 2815.5s / f67,920 – 84,465）— the reversal · 最密②

**モーション性格:** Reyes を separate, colder silhouette に。DNA band が **ignite**：the ONE moment the film "raises its voice"＝cold-cyan が frame を FLOOD、ladder が single match に align、numbers with many zeros が resolve。visual climax。**figure 密度 heavy②（~28 beats）。** AE `t-a5`(ACT_TITLE)、`c-dnamatch`(CENTER_STACK)。

| 区間(秒) | f開始–終了 | 画 | 主アニメ | easing/damping | stagger | Trail |
|---|---|---|---|---|---|---|
| 2264–2320 | 67,920–69,600 | 幕頭：Matias Reyes（convicted serial rapist/murderer・33⅓-to-life・**R2 no face**）。paper 上 beyond dispute | AE `t-a5`。Reyes＝separate, colder silhouette（他の 5影と別 lighting・より冷たい cyan rim）・`stat` "33⅓ TO LIFE"（CP21 high） | spring `damping:18` | — | — |
| 2320–2400 | 69,600–72,000 | 攻撃の2日前、同じ park で別の rape＝Reyes（same signature・same ground） | `lowerthird` "APRIL 17, 1989 · TWO DAYS BEFORE · THE SAME PART OF THE PARK · REYES IS BELIEVED TO HAVE ATTACKED THERE"（CP22 medium→hedged "believed to"）・pindropmap の 2点（abstracted・no crime detail） | `Easing.out(Easing.cubic)` / spring `damping:18` | — | pin drop **✓** |
| 2400–2470 | 72,000–74,100 | 10年 Reyes は黙る。2001–2002 に something shifts。Auburn で Korey と path が交わる | `timeline` REYES：1989 crimes → Nov 1991 sentence 33⅓-to-life → 2002 confession（CP21/CP23 high・cyan draw） | spring `damping:16` | 3f | draw **✓** |
| 2470–2540 | 74,100–76,200 | **"Alone."** state の theory（crowd＝5＋mysterious 6th）を one man が壊す | `mechanism:faultsplit`（ghost theory が one-man truth に割れる）・`kinetic:emphasis` "ONE MAN. HIM."（["ONE"]） | spring `damping:14` | 3f/語 | split **✓** |
| 2540–2600 | 76,200–78,000 | Reyes を hero にしない（he is the man who did it）。truth は 1989 から file の中にあった | 冷たい lab report の cyan line（Act1/Act2 の glimpse を回収）・still push-in `scale 1.00→1.06` | `Easing.out(Easing.cubic)` | — | — |
| 2600–2690 | 78,000–80,700 | Morgenthau/Nancy Ryan の reinvestigation。word を lab に持って行った。**それは match した** | **the ignition begins**：DNA ladder が draw、cold-cyan が frame に満ち始める（Acts1–4 で貯めた色の payoff）・`compbars` "MATCHED THE FIVE: 0" → "MATCHED REYES: 1" | spring `damping:16` | — | ladder **✓** |
| 2690–2760 | 80,700–82,800 | **the visual climax**：one in billions・a single match。numbers with many zeros が resolve | **cold-cyan FLOOD**（全 frame・意図した唯一の声上げ）・`numberticker` 0 → 6,000,000,000（CP24 high・"1 IN 6 BILLION"）＋ladder が single band に align（AE `c-dnamatch` CENTER_STACK 別枠） | spring `damping:16` / count `Easing.out(Easing.cubic)` | — | flood + align **✓✓** |
| 2760–2815.5 | 82,800–84,465 | vertigo：全 confession は false、"proved nothing" の DNA が whole truth。ghost は real name を持つ男だった。Korey が truth を見つけた側 | 反転の余韻（cyan hold・**earned breath** 2.5s×1）／`kinetic` "IT HAD ALWAYS BEEN HIS"／open loop：state が「got it wrong」を言う番 | `Easing.inOut(Easing.sin)` / spring `damping:16` | 3f/語 | — |

## 1.8 ACT 6 — EXONERATION & RECKONING（2815.5 – 3300.0s / f84,465 – 99,000）— the signature dissolves; the first dawn

**モーション性格:** signature が dissolve、vacatur card、**最初の dawn-amber**（唯一の暖色がここで初めて）。Armstrong beat は small, dismissed footnote（visually minor・quickly set down）。settlement numbers は heavy & plain。**REC light が finally ON**（reform）。AE `t-a6`(ACT_TITLE)、`c-vacated`(CENTER_STACK date)、`m-41m`(MONEY_STACK)、`c-state39`(CENTER_STACK)、`c-reform`(CENTER_STACK)。

| 区間(秒) | f開始–終了 | 画 | 主アニメ | easing/damping | stagger | Trail |
|---|---|---|---|---|---|---|
| 2815.5–2880 | 84,465–86,400 | 2002年12月19日、Justice Charles Tejada が全 conviction を vacate。**signature が erase/dissolve** | AE `t-a6`。the signature line が page から dissolve（Act2 の署名 motif の反転・particle disperse）・`lowerthird` "DEC 19, 2002 · VACATED — ALL FIVE, ALL COUNTS"（CP27 high・AE `c-vacated` CENTER_STACK date 別枠） | `Easing.out(Easing.cubic)` / spring `damping:18` | — | dissolve **✓** |
| 2880–2950 | 86,400–88,500 | exoneration は movie の約束ではない。years は returned されない。Korey は ~13年 | 冷 cyan から **first dawn-amber** が地平に滲む（唯一の暖色の初出）・still slow `scale 1.00→1.04` | `Easing.inOut(Easing.sin)` | — | — |
| 2950–3010 | 88,500–90,300 | **the Armstrong Report**（2003・rejected）を small footnote に。did NOT prevail・DNA still one man | `lowerthird` "A POLICE PANEL QUESTIONED IT — THE DA AND THE COURTS REJECTED IT · THE CONVICTIONS STAYED VACATED"（CP28 medium→rejected 枠のみ）・visually minor・quickly set down（小さく・短く・fade out） | `Easing.out(Easing.cubic)` | — | — |
| 3010–3090 | 90,300–92,700 | the lawsuit。city は a decade 争う。2014 に ~$41M settle（years に比例＝Korey 最大） | AE `m-41m`(MONEY_STACK) count-up・`numberticker` 0 → 41,000,000（CP30 high・top "ROUGHLY"・bottom "NEW YORK CITY, 2014 — ABOUT $1M PER YEAR LOST") | count `Easing.out(Easing.cubic)` / spring `damping:16` | — | count **✓** |
| 3090–3140 | 92,700–94,200 | later、State と別 settlement で数 million 追加。money は justice ではない（買い戻せない） | `lowerthird` "2016 · NEW YORK STATE · REPORTEDLY ~$3.9 MILLION MORE"（CP31 medium→"reportedly"・AE `c-state39` CENTER_STACK 別枠） | `Easing.out(Easing.cubic)` | — | — |
| 3140–3210 | 94,200–96,300 | repair①：false confession の理解を変えた。record the WHOLE interrogation が law に | **the REC light comes ON**（HOOK の OFF signature の反転・cyan→warm tick で点灯）・`kinetic:emphasis` "TURN THE CAMERA ON AT THE BEGINNING"（["BEGINNING"]・AE `c-reform` 別枠） | spring `damping:16` | 3f/語 | REC-ON **✓** |
| 3210–3260 | 96,300–97,800 | the survivor（Trisha Meili）への obligation。recovered・told her own story・never identified attacker。二つの harm が side by side | dignity-first still（**no depiction**・abstract dawn horizon）・`lowerthird` "A SERIOUS TELLING HOLDS BOTH HARMS"（CP02 high・臨床・no detail） | `Easing.inOut(Easing.sin)` | — | — |
| 3260–3300 | 97,800–99,000 | the men themselves＝advocates。Salaam が 2023 NYC Council に。renamed: THE EXONERATED FIVE。open loop：a conviction can be erased, the years can't | `kinetic` "THE EXONERATED FIVE"／`lowerthird` "YUSEF SALAAM · ELECTED TO THE NYC COUNCIL, 2023"（CP33 high）・dawn-amber accent | spring `damping:16` / `Easing.out(Easing.cubic)` | 3f/語 | — |

## 1.9 ACT 7 — WHAT A CONFESSION IS WORTH（3300.0 – 3617.5s / f99,000 – 108,525）— second-person; strip to essentials

**モーション性格:** back to the chair, the child, the second person。frame を essentials に strip（chair・clock・OFF/ON light・the five names）。names を bone-white で、then the truth line。restraint returns — 映画は始まった時と同じ静けさで終わる。AE `t-a7`(ACT_TITLE) → `c-names`(CENTER_STACK・close)。

| 区間(秒) | f開始–終了 | 画 | 主アニメ | easing/damping | stagger | Trail |
|---|---|---|---|---|---|---|
| 3300–3360 | 99,000–100,800 | "put you back in the room. As the child." 14歳・awake a day・母は来ない | AE `t-a7`。frame が strip down（周辺が dim、chair だけ残る）・単一 cyan light（HOOK の spotlight を回収） | `Easing.inOut(Easing.sin)` / spring `damping:18` | — | — |
| 3360–3450 | 100,800–103,500 | "What would you do?" the science：これらの条件下で人は confess する、child は最も | `mechanism:closingdoor`（the room built to produce a "yes"・静かに）・`kinetic` "THE ROOM PRODUCES A YES" | spring `damping:16` | 3f/語 | door **✓** |
| 3450–3520 | 103,500–105,600 | confession は proof of what happened ではなく proof of what the room can produce | `compbars` [{"WHAT HAPPENED",0},{"WHAT THE ROOM PRODUCED",1}] cyan（象徴・中立） | spring `damping:18` origin-left | — | — |
| 3520–3560 | 105,600–106,800 | 何の価値があったか：13年・五つの childhoods・real attacker が years free だった | `kinetic:emphasis` "THIRTEEN YEARS"（["THIRTEEN"]・CP19 high "roughly"）／scale が plain に沈む | spring `damping:16` | 3f/語 | — |
| 3560–3600 | 106,800–108,000 | the reform（record the whole interrogation・protect the child）＝insultingly simple・minimum decency | **REC light ON**（Act6 の点灯を hold）・chair・clock・OFF→ON の対比を最終提示 | `Easing.out(Easing.cubic)` | — | — |
| 3600–3617.5 | 108,000–108,525 | 五つの名前を bone-white で、then the truth line。restraint returns（**earned final breath** ≤2.5s） | 5名が stagger で mask 切れ上がり（Antron McCray / Kevin Richardson / Yusef Salaam / Raymond Santana / Korey Wise・CP05/CP32 high・AE `c-names` CENTER_STACK 別枠）→ hold → the truth line | spring `damping:16` | **4f/名** | — |
| 3617.5–3626.5 | 108,525–108,795 | **BrandEndcard**（9.0s・不変） | — | — | — | — |

> **★背面レイヤーは常に4層以上動く（§8）。各幕の 0.5s 境界で「動いている要素」が最低1つ（静止フレームゼロ）。** 全編の意図した breath は **3回のみ・各 ≤2.5s**（Act4 の cell-window 3.8s は「the earned hold」＝この幕限定の例外で architecture §2 が許可）。Trail 対象（fast move）：HOOK REC-tick／Act1 の investigations-collide snap・DNA band glint／Act2 の migrate・gears・closingdoor・stack／Act3 の headline wall・play triangle・scale tip／Act5 の pin drop・timeline draw・faultsplit・**DNA flood+align（最強）**／Act6 の signature dissolve・money count・REC-ON／Act7 の closingdoor。**KB・後ろ姿の緩い歩き・earned breath・dawn horizon には Trail をかけない**（無駄な残像・扇情を避ける）。

---

# §2 — SCENE-BY-SCENE STORYBOARD（全7幕・象徴/シルエットのみ・NO faces R2・assault は NEVER depicted）

**全ショット共通契約:** 顔・身体・肖像なし（R2）。五人＝descending heights の silhouettes（子供）。Korey Wise＝recurring taller-but-young spine silhouette。Reyes＝separate, colder silhouette。**被害者は一切描かない・attack は一切描かない・Trump ad art は再現しない。** 読める文字/plate/case-citation を作らない（redacted/illegible smear）。cold-cyan system（`#2F9FC4`）；dawn-amber `#C98A3C` は Act6/close のみ。図表の値・カード文言は §3/§4 と一致（`confidence:high` or hedged）。SDXL 85→**430 distinct** への展開は CODEX_A（§5）；本節は絵コンテ級の原図。

## 2.1 ACT 1 — THE NIGHT（象徴 the establishing vocabulary を建てる）
| Sid | 象徴（動き）・制約 |
|---|---|
| A1-01 | HOOK 回収：empty chair を単一 cold-cyan light が見つける（顔なし・R2） |
| A1-02 | steel table・読めない wall clock・**OFF の REC ランプ**（unrecorded hours の signature） |
| A1-03 | 1989春のNY＝subway car の graffiti を scar tissue の texture に（都市を mass に） |
| A1-04 | 夜の news の明滅（a number, a neighborhood）＝fear is the water |
| A1-05 | 4/19 の park を**抽象**（treeline・a lamp・cold）・crime は描かない |
| A1-06 | teenagers の後ろ姿の restless な mass（30–40人・no single will・顔なし） |
| A1-07 | 五つの descending silhouettes（14/14/15/15/16）・まだ group ではない・別々 |
| A1-08 | 102nd St cross drive 付近の park の別区画（**現場も被害者も描かない**） |
| A1-09 | coma の空白＝empty chair の echo・記憶の a vacuum（cold sink） |
| A1-10 | precinct が boys と parents で満ちる（後ろ姿の群れ・institutional） |
| A1-11 | **the collide**：二つの捜査（"park trouble"／"the attack"）が 1本の file に snap |
| A1-12 | proximity のみ＝no witness / no description の象徴（空の指差し） |
| A1-13 | the hinge：questioning 時、jogger 攻撃への物証ゼロの cursor が blink |
| A1-14 | 3AM の子供にとっての巨大な building（見上げる angle・顔なし） |
| A1-15 | lab に送られる biological evidence の cold-cyan band（Act5 の伏線・ignored） |

## 2.2 ACT 2 — THE INTERROGATIONS（claustrophobic・the machine）
| Sid | 象徴（動き）・制約 |
|---|---|
| A2-01 | the room（general one）：empty chair・windows なし・変わらない光・読めない clock |
| A2-02 | 冷めた soda・来ない母（renewed promise＝a technique の象徴） |
| A2-03 | detective 影（人物化しない）と child 影の対峙（顔なし・後ろ姿） |
| A2-04 | story fragment の type が detective 影 → child 影へ **migrate**（false-evidence ploy） |
| A2-05 | detective の顔に読める右答え/誤答＝「the room が yes を作る」（顔は描かず反応のみ） |
| A2-06 | 技法①**false-evidence ploy**：嘘の "proof" の象徴（判読不能） |
| A2-07 | 技法②**minimization**：soft admission＝"just held an arm" の gentle trap（閉じる扉） |
| A2-08 | the signature：pen が page に line を書く（**pressure 下・Act6 で dissolve**） |
| A2-09 | five confession pages が stack、各々が次を cite する house of cards |
| A2-10 | the rape kit・semen が五人を exclude する lab report（cold-cyan・file の中） |
| A2-11 | the ghost theory＝unknown 6th の empty silhouette（real name は 2002） |
| A2-12 | why detectives did it：men under pressure（monsters ではない・顔なし・機械の比喩） |
| A2-13 | the camera：録画は confession の最後だけ（TV glow が hours の後にだけ点く） |
| A2-14 | boys go home（briefly）・最後の ordinary week・signatures は down |
| A2-15 | machine が次の room（bigger one・flag・jury box）へ移る（open loop） |

## 2.3 ACT 3 — THE TRIALS（publicity の machine・the scale tips）
| Sid | 象徴（動き）・制約 |
|---|---|
| A3-01 | headline mass の oppressive kinetic wall（"wolf pack" は press の label・CP06） |
| A3-02 | "wilding"＝press が seize した語（media/police label・boys の行為として断定しない） |
| A3-03 | 1989/5/1 Trump ad＝**dated context の 1枚**（**ad art 再現禁止**・full-page の空白の枠のみ） |
| A3-04 | jury pool の presumption of innocence が drowned out される象徴（声の chorus） |
| A3-05 | courtroom の thin evidence：no eyewitness / no weapon / DNA matches none |
| A3-06 | the tapes：TV glow・**play triangle**（confession performed・顔は描かない） |
| A3-07 | 三様の confession（parent 同席3・Wise alone・Salaam oral のみ）を flatten する語 "confessed"（CP10 high） |
| A3-08 | defense case：DNA matches no one at the table（cold-cyan の exclusion） |
| A3-09 | the scale が confession 側に wrong way に tip |
| A3-10 | families never wavered：Harlem の親影の row（顔なし・後ろ姿） |
| A3-11 | moral panic が love を guilt の証拠に変える（親の言葉が discount される） |
| A3-12 | verdict：guilty・但し acquittals mixed in（**jury split は焼かない**・votetally 不使用） |
| A3-13 | sentence 二層："FOUR: JUVENILE 5–10 YRS" ↔ "KOREY WISE, 16: AS AN ADULT"（CP18） |
| A3-14 | the birthday の accident＝Korey 影だけ adult prison（Rikers）へ別方向（open loop） |

## 2.4 ACT 4 — THE LOST YEARS（slow・individuals・Korey the spine）
| Sid | 象徴（動き）・制約 |
|---|---|
| A4-01 | 単一 cell window に seasons が横切る（**calendar-flip 禁止**・光の色温度 shift・earned breath） |
| A4-02 | what is taken：a person is assembled する years（school/first job/first love の空席） |
| A4-03 | prison hierarchy の label＝worst possible・daily の danger arithmetic（象徴・非扇情） |
| A4-04 | 四人 younger の released：door left open な smaller cell（parole/registered/unemployable） |
| A4-05 | Kevin Richardson（14・youngest）＝a child asked to account alone |
| A4-06 | Raymond Santana（14）＝conviction met him at every door（後の years の label） |
| A4-07 | Antron McCray（15）＝parent 同席の confession の complicated weight（CP10） |
| A4-08 | Yusef Salaam（15）＝taped confession なし・innocence を held・public arc（CP10） |
| A4-09 | Korey Wise（16）＝adult system・small for the world・difficulty hearing（顔なし・spine 影） |
| A4-10 | beaten・facility 転々（safer を求めて）・**long solitary**（box の中の単一影） |
| A4-11 | parole の remorse を Korey は言わない（truth を選び cell に残る・aging drift） |
| A4-12 | 90s→2000s：case は ancient history・closed file・forgotten |
| A4-13 | upstate の accident が近づく：33-to-life の男が Korey の reach 内に置かれる |
| A4-14 | they cross paths（yard/corridor/recognition・顔なし）・man の中で何かが turn over |

## 2.5 ACT 5 — THE CONFESSION & THE DNA（the reversal・visual climax）
| Sid | 象徴（動き）・制約 |
|---|---|
| A5-01 | Matias Reyes＝separate, colder silhouette（**R2 no face**・convicted・33⅓-to-life・CP21） |
| A5-02 | 4/17/1989＝2日前、同じ park の別 rape（same signature・pindrop abstracted・CP22 hedged） |
| A5-03 | 10年の沈黙 → 2001–2002 の shift（religious conversion・certify しない・CP23） |
| A5-04 | Auburn で Korey と path が交わる（顔なし・二つの影・CP23 high） |
| A5-05 | **"Alone."**＝state の crowd theory（5＋6th）を one man が壊す（faultsplit） |
| A5-06 | Reyes を hero にしない：he is the man who did it（cold・distance） |
| A5-07 | truth は 1989 から file の中に（lab report の cold-cyan line・回収） |
| A5-08 | Morgenthau/Nancy Ryan の reinvestigation：word を lab に持って行く（CP26 high） |
| A5-09 | **it matched**：DNA ladder が draw・cold-cyan が満ち始める（貯めた色の payoff） |
| A5-10 | **the climax**：one in billions・single match・cold-cyan FLOOD（唯一の声上げ・CP24） |
| A5-11 | numbers with many zeros が resolve（1 in 6,000,000,000・ladder が single band に align） |
| A5-12 | vertigo：confession は false・"proved nothing" の DNA が whole truth（反転の余韻） |
| A5-13 | Korey の detail：最も苦しんだ者の presence が Reyes を speak させた（no tidy moral・spine 影） |
| A5-14 | state が「got it wrong」を言う番（open loop・convictions are about to fall） |

## 2.6 ACT 6 — EXONERATION & RECKONING（signature dissolves・first dawn・REC ON）
| Sid | 象徴（動き）・制約 |
|---|---|
| A6-01 | 2002/12/19 Justice Tejada が全 conviction vacate（**signature が dissolve/erase**・CP27） |
| A6-02 | exoneration ≠ movie の約束：years は returned されない（cold・plain） |
| A6-03 | 冷 cyan に **first dawn-amber** が滲む（唯一の暖色の初出・地平線） |
| A6-04 | **Armstrong Report**（2003・rejected）＝small footnote（visually minor・quickly set down・CP28） |
| A6-05 | the lawsuit：city が a decade 争う（institution の抵抗の象徴） |
| A6-06 | 2014 ~$41M settle（years に比例・Korey 最大・CP30・money は justice ではない） |
| A6-07 | 2016 State ~$3.9M（reportedly・別 settlement・CP31 hedged） |
| A6-08 | repair①：false confession の理解を変えた（case が most famous proof に・CP34） |
| A6-09 | **REC light が finally ON**（HOOK の OFF signature の反転・reform の象徴） |
| A6-10 | reform：record the WHOLE interrogation（16 hours を jury が見られる・CP34） |
| A6-11 | the survivor（Trisha Meili）への obligation：recovered・own story・二つの harm（CP02・no depiction） |
| A6-12 | repair②：the men＝advocates（renamed THE EXONERATED FIVE・CP32） |
| A6-13 | Salaam が 2023 NYC Council に（かつて animal と呼んだ city が govern を頼む・CP33） |
| A6-14 | open loop：a conviction can be erased, the years can't（what was it worth?） |

## 2.7 ACT 7 — WHAT A CONFESSION IS WORTH（second-person・strip to essentials）
| Sid | 象徴（動き）・制約 |
|---|---|
| A7-01 | "back in the room. As the child."＝chair だけ残る strip・単一 cyan light（HOOK 回収） |
| A7-02 | 14歳・awake a day・母は来ない・読めない clock（second-person） |
| A7-03 | "What would you do?"＝the room built to produce a "yes"（closingdoor・静か） |
| A7-04 | the science：これらの条件下で人は confess・child は最も（CP34・established consensus） |
| A7-05 | confession = proof of what the room can produce（≠ what happened・compbars 中立） |
| A7-06 | 何の価値だったか：13年・五つの childhoods・real attacker が years free（CP19） |
| A7-07 | the reform（record the whole interrogation・protect the child）＝minimum decency |
| A7-08 | **OFF→ON の REC light の最終対比**（chair・clock・essentials） |
| A7-09 | 五つの名前を bone-white で（Antron McCray / Kevin Richardson / Yusef Salaam / Raymond Santana / Korey Wise・CP05/CP32） |
| A7-10 | the truth line＝a confession is only worth the conditions it was made in（restraint returns・final breath） |

---

# §3 — AE HERO PROGRAM — GO HEAVY（~36 moments・TWO TIERS・owner: "AEをガッツリ効かせて、時間はかかってもいい"）

> **AE is not a garnish** — it carries the film's biggest emotional peaks. **~36 AE moments in two tiers**, composited over the base render (density 非カウント). Time/effort authorized.
> - **Tier A — ~24 standard hero cards** on the **SIX PROVEN layouts only**：`ACT_TITLE_CARD` / `CENTER_STACK` / `MONEY_STACK` / `QUOTE_CARD` / `VOTE_SPLIT` / `SPLIT_COMPARE`（cleveland clone が実装済・§3.1）。
> - **Tier B — ~12 BESPOKE SET-PIECES** = **NEW layouts implemented for real** in `build_centralpark_hero_cards.py`（cleveland clone を EXTEND：6種を残し ADD する）。各 5–10s・各々 **個別に `--dryrun` 検証**し、**使用前に `check_AE_layouts` allowlist に追加**（§3.2）。これが「phantom-layout crash なしで heavy に行く」方法＝存在しない layout を参照せず、IMPLEMENT → PROVE → reference する。
>
> **★★ `DATE_STAMP` と `SEAM_TRANSITION` は今も BANNED**（clone 元 JSX は末尾 `else throw "unsupported layout"`＝参照でクラッシュ・EP48/49 の burned lesson）。日付カードは `CENTER_STACK`。**Tier B の新 layout は「存在しないものを参照」ではなく「実装して dryrun で証明したもの」**＝これが決定的な違い。
>
> **全 AE 共通（両 tier）:** ACCENT tuple `[0.184,0.624,0.769]`（#2F9FC4）を RGB で set。INK `[0.039,0.039,0.047]`。**dawn-amber `[0.788,0.541,0.235]` は exoneration/close の moment のみ**（`SIGNATURE_ERASE` resolve・`REC_LIGHT`-on・`SCALE_TIP`-right・`NAME_WALL` close・`c-vacated`/`m-41m`/`c-state39`/`c-salaam`）。**Measured-fit MANDATORY**（`fit_size()` pre-fit ＋ JSX `sourceRectAtTime(t,false).width` re-fit ＋ quote-wrap・advance-width 推定禁止）。**Two-step AE**（JSX が `.aep` build → **assert `.aep` mtime > `.jsx`** → 別プロセス `aerender -project`・出力 **REPO path on C:**・exFAT H: は 0 mp4）。全 moment 右下 `AI-assisted visualization`（R1）。**film_offset = 11.5**（body-relative→absolute）。**no moment が victim を name/depict しない・Trump ad art を再現しない・no faces**（DNA_LADDER/INTERROGATION_ROOM は abstract）。builder → `08_edit/ae_hero/beats.json`（`schema_version:"centralpark_beats.v1"`）→ `composite_centralpark_hero.py`。

## 3.1 TIER A — 標準ヒーローカード 24枚（6種 proven layout・anchor は body-relative の film-clock 秒）

| id | layout（proven6内） | top copy | hero / sub copy | anchor(s) | dur(s) | fact id（high/hedged） | motif |
|---|---|---|---|---|---:|---|---|
| **t-a1** | ACT_TITLE_CARD | ACT I | THE NIGHT · APRIL 1989 | 27.0 | 5.0 | CP03 high | empty chair / cold light |
| **c-noevidence** | CENTER_STACK | AT THE MOMENT OF QUESTIONING | NO PHYSICAL EVIDENCE | 372.0 | 6.0 | CP08/CP12 high | cyan cursor blink |
| **t-a2** | ACT_TITLE_CARD | ACT II | THE INTERROGATIONS | 452.0 | 5.0 | — (title) | the room / OFF REC |
| **c-roompromise** | CENTER_STACK | A ROOM AND A PROMISE | "YOU CAN GO HOME IF YOU JUST SAY IT" | 560.0 | 6.0 | CP08/CP34 high (paraphrase, not attributed quote) | closing door |
| **c-fivechildren** | CENTER_STACK | FIVE CHILDREN | AGES 14 TO 16 | 720.0 | 6.0 | CP05 high | 5 descending silhouettes |
| **c-sevenhours** | CENTER_STACK | BEFORE THE CAMERAS | AT LEAST SEVEN HOURS · NONE OF IT RECORDED | 505.0 | 6.0 | CP08 firm high | wall clock, OFF REC |
| **cmp-fedsigned** | SPLIT_COMPARE | THE INTERROGATION | left "FED IN" · right "SIGNED" · bottom "THE GENTLENESS WAS THE TRAP" | 905.0 | 6.5 | CP10/CP34 high | migrating type |
| **cmp-confdna** | SPLIT_COMPARE | THE CONTRADICTION | left "5 CONFESSIONS" · right "0 DNA MATCHES" · bottom "THE EVIDENCE POINTED ELSEWHERE" | 1080.0 | 6.5 | CP10/CP12 high | cold-cyan bands |
| **t-a3** | ACT_TITLE_CARD | ACT III | THE TRIALS · 1990 | 1170.0 | 5.0 | CP15/CP16 high | headline wall |
| **c-papersfirst** | CENTER_STACK | 1989 | TRIED IN THE PAPERS FIRST | 1245.0 | 5.5 | CP14 high | kinetic headline mass |
| **c-trumpad** | CENTER_STACK | MAY 1, 1989 | A FULL-PAGE AD DEMANDED THE DEATH PENALTY / REPORTEDLY ~$85,000 · IT DID NOT NAME THE FIVE | 1305.0 | 6.5 | CP13 high (cost hedged) | blank full-page frame (NO ad art) |
| **cmp-verdict** | SPLIT_COMPARE | THE VERDICTS | left "CONVICTED" · right "ACQUITTED OF ATTEMPTED MURDER" · bottom "EVEN THE JURIES HESITATED" | 1600.0 | 6.0 | CP17 medium→hedged | tipped scale echo |
| **cmp-sentence** | SPLIT_COMPARE | THE SENTENCES | left "FOUR: JUVENILE · 5–10 YRS" · right "KOREY WISE, 16: AS AN ADULT" · bottom "A BIRTHDAY MADE THE DIFFERENCE" | 1655.0 | 6.5 | CP18 high | Korey spine splits away |
| **t-a4** | ACT_TITLE_CARD | ACT IV | THE LOST YEARS | 1704.0 | 5.0 | — (title) | cell window / seasons |
| **cmp-yearsserved** | SPLIT_COMPARE | YEARS SERVED | left "FOUR: ~6–7 YRS EACH" · right "KOREY WISE: ~13 YRS" · bottom "TRIED AS AN ADULT AT 16" | 1875.0 | 6.5 | CP19 high (hedged ~) | aging spine silhouette |
| **t-a5** | ACT_TITLE_CARD | ACT V | THE CONFESSION & THE DNA | 2272.0 | 5.0 | — (title) | colder Reyes silhouette |
| **c-twodays** | CENTER_STACK | APRIL 17, 1989 | TWO DAYS BEFORE · THE SAME PART OF THE PARK · REYES IS BELIEVED TO HAVE ATTACKED THERE | 2340.0 | 6.0 | CP22 medium→"believed to" | pindrop (abstract) |
| **q-alone** ★reserved | QUOTE_CARD | MATIAS REYES · 2002 | (activates ONLY if a verified-verbatim Reyes line is locked by the citation pass; **until then renders as CENTER_STACK "HE ACTED ALONE" / "DNA CONFIRMED ONE ATTACKER"**) | 2560.0 | 6.5 | CP24 high | one silhouette, alone |
| **t-a6** | ACT_TITLE_CARD | ACT VI | EXONERATION & RECKONING | 2823.0 | 5.0 | — (title) | dawn-amber (first) |
| **c-vacated** | CENTER_STACK | DEC 19, 2002 | VACATED — ALL FIVE, ALL COUNTS | 2860.0 | 6.0 | CP27 high | pairs w/ SIGNATURE_ERASE |
| **m-41m** | MONEY_STACK | ROUGHLY | $41,000,000 / NEW YORK CITY, 2014 — ABOUT $1M PER YEAR LOST | 3045.0 | 7.0 | CP30 high (hedged ~) | heavy, plain |
| **c-state39** | CENTER_STACK | 2016 · NEW YORK STATE | REPORTEDLY ~$3.9 MILLION MORE | 3115.0 | 5.5 | CP31 medium→"reportedly" | separate settlement |
| **c-salaam** | CENTER_STACK | 2023 | YUSEF SALAAM · ELECTED TO THE NYC COUNCIL | 3270.0 | 5.5 | CP33 high | dawn-amber, lives rebuilt |
| **t-a7** | ACT_TITLE_CARD | (kicker none) | WHAT A CONFESSION IS WORTH | 3308.0 | 5.0 | CP34 high | back to the chair |

**Tier A 合計 = 24枚**（ACT_TITLE_CARD×7, CENTER_STACK×11, SPLIT_COMPARE×5, MONEY_STACK×1, QUOTE_CARD×1 reserved）。尺 ≈ 143s。

## 3.2 TIER B — BESPOKE AE SET-PIECES 12 moments（★NEW layouts・implemented + dryrun + allowlisted・the "gutsy" part）

各 set-piece は `build_centralpark_hero_cards.py` に **新 builder 関数**として追加（cleveland の6種を残して ADD）。**各新 layout は個別に `--dryrun` で単体レンダを通し、`check_AE_layouts` の allowlist に加えてから使用**する（存在しない layout を参照しない＝IMPLEMENT→PROVE→reference）。共通スタック（下→上）は cleveland 準拠：黒 bg → 象徴 still（任意）→ グレードウォッシュ（INK/MULTIPLY）→ 羽根ビネット → グロー（cold-cyan・exoneration系のみ dawn-amber）→ ライトスイープ（`"ADBE Rotate Z"`=18・`motionBlur`）→ 主レイヤー群（`motionBlur` を動くレイヤー個別に）→ `AI-assisted visualization`（R1）→ head/tail 4f 黒ディップ。全 easing は `KeyframeEase`/spatial-ease dim（cleveland `ease()`）＝等速線形ゼロ。

| # | layout（NEW・builder fn） | moment / 幕 | anchor(s) | dur(s) | accent |
|---|---|---|---|---:|---:|
| B1 | **`DNA_LADDER`**（`buildDnaLadder`） | Act5 climax・**the signature comp** | 2695.0 | 10.0 | cyan（FLOOD） |
| B2 | **`STAT_RESOLVE`**（`buildStatResolve`） | Act5・one-in-billions odometer | 2740.0 | 7.0 | cyan |
| B3 | **`CARD_STACK`**（`buildCardStack`） | Act2・five-confession house of cards | 960.0 | 7.0 | cyan |
| B4 | **`REC_LIGHT`**-off（`buildRecLight`, mode "off") | Act2・unrecorded hours | 470.0 | 5.0 | cyan(dim) |
| B5 | **`REC_LIGHT`**-on（`buildRecLight`, mode "on") | Act6 reform・**off→on** | 3165.0 | 6.0 | **dawn-amber** |
| B6 | **`SCALE_TIP`**-wrong（`buildScaleTip`, mode "confession") | Act3・tips the wrong way | 1445.0 | 6.0 | cyan |
| B7 | **`SCALE_TIP`**-right（`buildScaleTip`, mode "evidence") | Act6・rights itself | 2985.0 | 6.0 | **dawn-amber** |
| B8 | **`HERO_TIMELINE`**-intro（`buildHeroTimeline`, phase 1) | Act1・1989 introduced | 120.0 | 7.0 | cyan |
| B9 | **`HERO_TIMELINE`**-resolve（`buildHeroTimeline`, phase 3) | Act6・→2002→2014 resolved | 3020.0 | 9.0 | **dawn-amber** |
| B10 | **`NAME_WALL`**-rise（`buildNameWall`, mode "names") | Act2・five names + ages rise | 700.0 | 7.0 | cyan |
| B11 | **`NAME_WALL`**-close（`buildNameWall`, mode "exonerated") | Act7 close・re-inscribe | 3600.0 | 9.0 | **dawn-amber** |
| B12 | **`SIGNATURE_ERASE`**（`buildSignatureErase`） | Act6 vacatur・**before/after w/ DNA_LADDER** | 2895.0 | 6.0 | **dawn-amber**(resolve) |

> **★8 distinct new layouts implemented** = DNA_LADDER・STAT_RESOLVE・CARD_STACK・REC_LIGHT・SCALE_TIP・HERO_TIMELINE・NAME_WALL・SIGNATURE_ERASE（architecture §3 の named set-pieces と一致）。REC_LIGHT/SCALE_TIP/HERO_TIMELINE/NAME_WALL は 2× 使用で 12 moments。
> **reserve（storyboard が peak を surface したら実装・同じ dryrun+allowlist 手順）:** `HEADLINE_WALL`（Act3 press-storm・~1180s）／`INTERROGATION_ROOM`（hook/Act2 establishing・~445s）／`HERO_TIMELINE`-extend（Act4・~2205s、phase 2）。使う場合のみ実装・dryrun・allowlist 追加。

### 3.2.1 各 set-piece の choreography（layers / keyframes / easing / motion-blur / duration）

**B1 `DNA_LADDER`（Act5 climax・~10s・the film's thesis）** — anchor 2695s.
- L: (1)INK bg (2)冷たい lab scrim (3)**5 lanes**（boys）の gel band ladder：各 lane は縦の rung 群。0.0–2.0s で lane が 1本ずつ `scaleY 0→1`（origin bottom・`stagger 0.18s/lane`・cyan **dim** opacity 40）＝**NO MATCH**（rung が互いに ずれて並ぶ）。(4)0.2s hold。(5)2.5–4.0s **Reyes lane** が右から slide-in（`translateX +260→0px`・`motionBlur`・cyan bright）→ その rung が 5 lane の空きに **snap-align**（`position` key・`ease inf 90`）。(6)4.0–5.5s align した単一 band が pulse（`scale 1.0→1.12→1.0`）。(7)5.5–7.5s **cold-cyan FLOOD**：全画面 cyan solid の `opacity 0→70→24`（ADD blend）＋lane 全体が bright に。(8)7.5–10s sub "1 IN 6 BILLION · A SINGLE MATCH"（measured-fit）が mask 切れ上がり・hold ≥1.2s。
- easing spring/`ease inf 80–90`・snap は最速・FLOOD は eased。motion-blur：Reyes lane slide・snap・pulse・sweep のみ。fact CP24 high。**abstract・no crime imagery.**

**B2 `STAT_RESOLVE`（Act5・~7s・odometer）** — anchor 2740s（DNA_LADDER の直後、重ならない）.
- L: 大きな numeric odometer が **0 → 6,000,000,000**（Python が全表示文字列を precompute・JSX は算術しない・**`group:false` にはしない＝これは桁区切りする数値**）。0.6–2.0s で ease-out-cubic count-up（`motionBlur` on・scale 46→112→100 の overshoot settle）→ 2.0s で "1 IN 6 BILLION" の言い換え label が下段に mask 切れ上がり → hold ≥1.2s。accent cyan。fact CP24 high.
- ★注意：**YEAR を出す figure/card は別途 `group:false`**（§6・NumberTicker のコンマ群化バグ回避）。この STAT_RESOLVE は billions なので群化する。

**B3 `CARD_STACK`（Act2・~7s・house of cards）** — anchor 960s.
- L: 5枚の confession page（判読不能 smear・object のみ）が 0.0–2.5s で 1枚ずつ下から stack（`translateY 80→0`・`rotateZ ±3°` 交互・`stagger 0.35s`・`motionBlur`）。各 page に短い `arrow`（"the others already named you"）が次の page を指す（`scaleX 0→1` draw）。3.0–4.5s **DNA report** が stack の下へ slide-in（`translateY -40`・cyan edge）→ 全 stack が微かに tilt（`rotateZ 0→5°`・ease）＝no foundation。4.5–7s "NO FOUNDATION" label mask 切れ上がり。cyan。fact CP10/CP12 high。

**B4/B5 `REC_LIGHT`（used 2×・off→on の signature）** — B4 off@470s(5s), B5 on@3165s(6s).
- L: 中央に REC dot（circle・ring）＋"REC" label（Oswald）。**mode "off"**：dot は dark grey・0.0–1.0s で一度だけ tick（`scale 1.0→1.15→1.0`・点かない）・sub "THE CAMERA WAS OFF"・cyan(dim)。**mode "on"**：dot が dark→**illuminate**（`fillColor` を dawn-amber へ key＋glow `opacity 0→60`・`scale 1.0→1.2→1.0`・`motionBlur`）・sub "RECORD THE WHOLE INTERROGATION"・**dawn-amber**（reform）。fact CP34 high。HOOK の OFF signature を回収し reform で反転。

**B6/B7 `SCALE_TIP`（used 2×・confession vs evidence）** — B6 wrong@1445s(6s), B7 right@2985s(6s).
- L: 天秤（beam＋2 pan）。**mode "confession"**：0.5–2.5s で beam が confession pan 側へ `rotateZ 0→-14°`（weighted ease＝slow-in fast-settle・`motionBlur`）＝wrong way・cyan。**mode "evidence"**：beam が evidence(DNA) pan 側へ `rotateZ +14→0→-2°` で righting・**dawn-amber**（Act6）。pan の物体は判読不能象徴。label mask 切れ上がり。中立（どちらが正義かを画面で断じない）。

**B8/B9 `HERO_TIMELINE`（recurring spine・intro/resolve）** — B8 intro@120s(7s), B9 resolve@3020s(9s).
- L: 横 spine line が `scaleX 0→1`（origin-left・`ease inf 80`）で draw。node が year で pop（`scale 0→1`・`motionBlur`）。**phase 1 (intro)**：node "1989" のみ点灯・cyan・"THAT NIGHT"。**phase 3 (resolve)**：spine が右へ extend し node **1989 → 2002 → 2014** が stagger で点灯（`stagger 0.5s`）・最後の node が **dawn-amber**・"VACATED · SETTLED"。**★全 year node は `group:false`**（1989/2002/2014 を "1,989" にしない・§6）。fact CP03/CP27/CP30 high。in-film Remotion `timeline` figures とは別物（elevated hero rendition・時刻が重ならない）。

**B10/B11 `NAME_WALL`（used 2×・the renaming）** — B10 rise@700s(7s), B11 close@3600s(9s).
- L: 5行の name＋age。**mode "names"**：0.0–3.0s で 1行ずつ mask 切れ上がり（`translateY 110%→0`・`stagger 0.4s`・Anton・cyan）＝"McCRAY 15 · RICHARDSON 14 · SALAAM 15 · SANTANA 14 · WISE 16"（CP05 high）。**mode "exonerated"**：既存 5 name が hold → 上に "THE EXONERATED FIVE" が **dawn-amber** で mask 切れ上がり＋accent underline `scaleX 0→1` wipe＝renaming。close は bone-white の names → truth line。fact CP05/CP32 high.

**B12 `SIGNATURE_ERASE`（Act6 vacatur・~6s・before/after w/ DNA_LADDER）** — anchor 2895s.
- L: (1)INK bg (2)confession page（判読不能 smear・object のみ） (3)署名の line が既に書かれた状態から **un-write**：0.5–4.0s で stroke 群が末尾→先頭へ 1本ずつ消える（各 stroke を `trimPath end 1→0` 風＝mask reveal 反転・`stagger 0.12s/stroke`・`motionBlur`）＋ ink particle が上へ lift-away（`translateY 0→-40`・`opacity 100→0`）。(4)4.0–5.0s page が blank に。(5)5.0–6.0s "VACATED — ALL FIVE, ALL COUNTS" label が mask 切れ上がり、**dawn-amber へ resolve**（cyan→dawn の色 key＝exoneration の初暖色）・accent underline `scaleX 0→1` wipe。
- easing `ease inf 70–80`・un-write は末尾から eased。**dawn-amber（resolve のみ）**。Act2 の署名 motif（`c-roompromise`/CARD_STACK の pen）の反転。fact CP27 high。
- **（reserve）`INTERROGATION_ROOM`（hook echo / Act2 establishing・6s・~445s）:** empty chair・steel table・読めない clock・OFF REC の establishing・slow push-in `scale 1.00→1.08`＋clock hand の imperceptible drift＋REC dot dark・cyan・abstract/no faces/no crime・sub "A ROOM WITH NO CAMERA ON"（CP08 firm high）。使う場合のみ実装・dryrun・allowlist 追加。

## 3.3 ★VALIDATION LINE（`validate_centralpark_beats` ＋ `check_AE_layouts` が assert）
```
[1] AE moments total = 36  (Tier A 24 + Tier B 12)  ✓
[2] Tier A layout ∀ ∈ {ACT_TITLE_CARD, CENTER_STACK, MONEY_STACK, QUOTE_CARD, VOTE_SPLIT, SPLIT_COMPARE}
      used: ACT_TITLE_CARD×7, CENTER_STACK×11, SPLIT_COMPARE×5, MONEY_STACK×1, QUOTE_CARD×1(reserved)  ✓
[3] check_AE_layouts allowlist = EXACTLY { 6 proven } ∪ { implemented+dryrun-passed Tier-B }
      Tier-B implemented = {DNA_LADDER, STAT_RESOLVE, CARD_STACK, REC_LIGHT, SCALE_TIP,
                            HERO_TIMELINE, NAME_WALL, SIGNATURE_ERASE}  (8 distinct new layouts,
                            = architecture §3 named set-pieces)
      reserve (implement only if used) = {HEADLINE_WALL, INTERROGATION_ROOM}
      DATE_STAMP = 0 · SEAM_TRANSITION = 0 · phantom (referenced-but-not-implemented) = 0  ✓
      ★ every Tier-B layout MUST pass its own `--dryrun` single-comp render BEFORE it enters the allowlist.
[4] VOTE_SPLIT count = 0 — DELIBERATE: no confidence:high jury vote-split in the ledger (would fabricate
      numbers). Verdict beat = SPLIT_COMPARE cmp-verdict (CP17 hedged). VOTE_SPLIT stays in the allowlist
      as a proven layout but is not emitted.
[5] QUOTE_CARD = 1 RESERVED (q-alone) — activates ONLY on a verified-verbatim Reyes line from the citation
      pass; until then renders as CENTER_STACK (no quote marks). No invented quotation ever ships (R-QUOTE).
[6] every burned number = confidence:high CP-id or hedged verbatim to the ledger screen_phrasing:
      CP03,CP05,CP08(firm 7hrs),CP12,CP13(cost "reportedly ~"),CP14,CP15,CP16,CP17(hedged),CP18,CP19("~"),
      CP22("believed to"),CP24(1 in 6 billion),CP27,CP30("roughly"/"~"),CP31("reportedly"),CP32,CP33,CP34.
      0 off-ledger.  ✓
[7] dawn-amber tuple ONLY on exoneration/close moments {REC_LIGHT-on, SCALE_TIP-right, HERO_TIMELINE-resolve,
      NAME_WALL-close, c-vacated, m-41m, c-state39, c-salaam}; every other moment cyan/bone.  ✓
[8] no moment names/depicts the victim; none reproduces the Trump ad art; no faces; assault never referenced.  ✓
[9] YEAR figures/nodes render group:false (1989/2002/2014, NOT "1,989" — the EP46 NumberTicker comma bug). ✓
[10] anchors body-relative, monotonically increasing, AE↔AE and AE↔figures non-overlapping (≥1s),
      +film_offset 11.5 for absolute.  ✓
```

---

# §4 — IN-FILM FIGURE-BEAT SCHEDULE（165 beats・union-valid only・dochighlight 0・stub 0・density engine）

> Rendered inside the Remotion film via the real `remotion/src/components/FigureBeats.tsx` `FigureSpec` union. **全 kind を実 union で検証済（小文字）。** `check_motion_density` は `centralpark_film.json` の `figures[]`（＋graphics/heroCuts）だけを数える（**AE 36 moments（Tier A 24 + Tier B 12）は composite 後で 0 カウント**）。**dochighlight = 0（R-DOCHL・grep 0）。stub = 0。** `quote` と `votetally` は §3 と同じ理由で**不使用**（verified-verbatim/confidence:high 票が無い）。

## 4.1 密度の算出（★arithmetic を見せる）
```
body-minutes = narrationSeconds / 60 = 3606.0 / 60 = 60.10 min
floor(2.5/min) = ceil(60.10 × 2.5) = ceil(150.25) = 151   （SPEC beats_floor 140 の上位）
design = 165 beats
  density  = 165 / 60.10 = 2.745 / min   ✓ ≥ 2.5（floor 151 に +14）
  coverage = 165 beats × 平均 6.0s = 990s / 3606 = 0.2745   ✓ ≥ 0.25
  variety  = 15 distinct kinds           ✓ ≥ 6
  dochighlight = 0 / stub = 0            ✓
  no 30s window figure-less（avg spacing 21.9s・§4.3 の配置で保証）
関連 asset ゲート（§5）: still-share 0.4353 ≤ 0.45 ・ first-use 0.8621 ≥ 0.70
```

## 4.2 幕別配分と kind（★heaviest Act2 & Act5・同一 kind を連続させない）
| 幕 | minutes | beats | 密度/min | 主 kind（union実在） |
|---|---:|---:|---:|---|
| HOOK/OPENING | 0.4 | 3 | — | lowerthird(開示)・kinetic・spotlight |
| ACT1 The Night | 7.0 | 18 | 2.57 | lowerthird・kinetic・routemap・pindropmap・regionmap・stat・compbars・arrow・highlightring |
| **ACT2 Interrogations** | 12.0 | **36** | **3.00** | **mechanism(closingdoor/gears)**・compbars・arrow・kinetic・stat・timeline・lowerthird・acttitle(sub) |
| ACT3 Trials | 9.0 | 23 | 2.56 | kinetic(headline wall)・compbars・lowerthird・mechanism(faultsplit)・timeline・stat・highlightring |
| ACT4 Lost Years | 9.5 | 22 | 2.32 | bar・lowerthird・kinetic・timeline・stat・compbars・acttitle(sub) |
| **ACT5 Confession & DNA** | 9.3 | **28** | **3.01** | **numberticker**・**compbars**・timeline・mechanism(faultsplit)・pindropmap・stat・kinetic・lowerthird・highlightring |
| ACT6 Exoneration | 8.1 | 20 | 2.47 | numberticker・lowerthird・kinetic・mechanism(closingdoor)・stat・compbars・timeline |
| ACT7 What It's Worth | 5.3 | 15 | 2.83 | mechanism(closingdoor)・compbars・kinetic・spotlight・lowerthird・stat |
| **合計** | 60.10 | **165** | **2.745** | **variety 15 kinds ≥ 6** |

## 4.3 kind 別 総数・payload 形（★union 検証・値は §1.4/facts と一致・still-share は §5 で ≤0.45）
| kind（union実在） | 数 | payload shape（union） | 用途（confidence:high or hedged） |
|---|---:|---|---|
| `lowerthird` | 46 | `{primary, secondary?, accent?}` | 開示 `AI-assisted visualization`×2／place・date・doctrine・hedged-fact labels（"AT LEAST SEVEN HOURS"／"MAY 1, 1989 … REPORTEDLY ~$85,000"／"DEC 19, 2002 · VACATED"／Armstrong rejected 枠 等） |
| `kinetic` | 24 | `{lines[], style?, emphasisWords?}` | emphasis 行（"IT WILL MATCH NONE OF THEM"／"THE STORY, FED IN"／"ONE MAN. HIM."／"IT HAD ALWAYS BEEN HIS"／"TURN THE CAMERA ON AT THE BEGINNING"／"THIRTEEN YEARS"／second-person）。emphasisWords は 1–2語（文字切れ回避） |
| `mechanism` | 13 | `{mechanism: closingdoor\|gears\|faultsplit}` | gears＝interrogation machine（Act2）／closingdoor＝minimization trap・the "yes" room（Act2/Act7）／faultsplit＝ghost theory splits from evidence（Act5）・scale tip（Act3） |
| `compbars` | 11 | `{items:[{label,value,accent?}]}` | proximity/no-evidence（Act1）／confessions 5 vs DNA 0（Act2/Act3）／matched-five-0 vs matched-Reyes-1（Act5）／what-happened vs what-the-room-produced（Act7）。**中立** |
| `timeline` | 10 | `{events:[{year,text}]}` | that night → 2002（returns/extends・Act4）／Reyes 1989→Nov1991(33⅓)→2002（Act5）／two-trial 1990（Act3）／procedural 2002→2014→2016（Act6） |
| `stat` | 10 | `{value, prefix?, suffix?, decimals?, label, topLabel?}` | 12（coma days・CP04）／5（children・CP05）／7（"AT LEAST" hours・CP08）／33⅓（Reyes・CP21）／2（days before・CP22 hedged）／13（Wise years "~"・CP19）／その他 high のみ |
| `numberticker` | 6 | `{value, prefix?, suffix?, decimals?, label?}` | 6,000,000,000（DNA・CP24・count-up）／41,000,000（$・CP30）／3,900,000（$・CP31 reportedly）等（大桁の count-up 決め所） |
| `bar` | 6 | `{data?/items?:[{label,value}]}` | YEARS-SERVED：four ~6–7 ×4 ＋ Wise ~13（CP19 high・hedged・Act4） |
| `arrow` | 6 | `{from?, to?, label?}` | story fed detective→child（Act2）／evidence→one unaccounted man（Act2）／DNA→one man（Act5） |
| `highlightring` | 6 | `{cx?, cy?, r?, label?}` | OFF REC light を囲む（HOOK/Act2）／the unread lab line（Act1/Act5） |
| `pindropmap` | 4 | `{pins:[{x,y,label?}]}` | park geography の**abstracted 2–3点**（Act1/Act5・**NO crime location detail**） |
| `routemap` | 3 | `{pins?, label?}` | その夜の drift（abstracted・Act1） |
| `spotlight` | 5 | `{cx?, cy?, r?, dim?}` | 単一 cold light on the chair（HOOK/Act7・restraint） |
| `regionmap` | 2 | `{label?, pattern?}` | 1989 の city（abstracted・Act1） |
| `acttitle` | 3 | `{title, kicker?, index?}` | **intra-act sub-heads のみ**（"THE ROOM"／"THE MACHINE"／"THE LADDER"）・**AE の 7 act-title と 1秒も重ねない**（`validate_centralpark_beats` が enforce・幕頭は AE が担う） |
| **合計** | **165** | | **variety 15・dochighlight 0・stub 0・quote 0・votetally 0** |

> ★lowerthird 46/165 = 27.9%（< ⅓・単一 kind 支配なし）。**同一 kind を連続させない**（compbars の直後に compbars を置かない・quote/votetally は不使用）。各枠 **5.2–6.5s**（coverage 0.2745 を守る）。**AE の 36 moments（Tier A 24 + Tier B 12）と 1秒でも重ならない**（validate 両突き合わせ）。Tier-B set-piece（DNA_LADDER/CARD_STACK/NAME_WALL 等）は同じ物語ビートの in-film figure（DNA compbars・house-of-cards timeline・name kinetic）と **時刻を分離**（AE が elevated hero、figure が別 anchor の density）。**figures[].*text*/lines/label/primary/secondary は `check_centralpark_facts.py` の検査対象**（the-five-were-involved を匂わせない・台帳外数値・**dochighlight**・invented quote を出さない）。

---

# §5 — CODEX_A BRIEF（image/asset generation・60:00 scale・symbols only・no faces）

> **接続点は `episodes/PD-2026-050-centralpark/05_visuals/asset_manifest.v001.json` ただ1ファイル**（A が書き・B が読む・counts/role enum を A/B 一字一致）。schema 版 `centralpark_assets.v1`。**A↔B は manifest のみで接続**（本書 §2/§9-style storyboard は原図）。

## 5.1 生成量（★§0.6 の 60:00 値をそのまま満たす・1シーン1枚・variants 0）
```
[0] 絵が必要な区間 = narrationSeconds 3606.0（BrandOpening/Endcard/hook teaser は別レイヤー）
[1] 総カット = 1,160（§0.6）    3606 / 1160 = 3.109 s/カット  ✓ mean_shot ≤ 7.0
[2] 素材内訳（§0.6 の distinct/cuts をそのまま・1シーン1枚・variants 禁止）
    still（SDXL）  430 distinct → 505 カット（75枚が2回・355枚が1回・mean 1.174・cap 2）★各1枚生成
    factory 実写   485 distinct → 485 カット（各1回・cap 1・全点目視QC）
    i2v モーション  85 distinct → 170 カット（各2回・mean 2.0・cap 2）
    ---------------------------------------------------
    distinct 合計 1,000        → 1,160 カット
[3] first-use share = 1000/1160 = 0.8621 ✓ ≥0.70
[4] still-share     = 505/1160  = 0.4353 ✓ ≤0.45（余裕 0.15%pt → still-cut 505 を固定・増やすな）
[5] motion coverage = (485+170)/1160 = 0.5647 ✓ ≥0.45
[6] factory 下限 = 3606/30 = 120.2 → ≥121本。設計値 485本 ✓
```
- `ai_prompts.v001.md` = **body 430行の固有プロンプト**（still 各1枚・`read_prompts()` の2行形式）＋ **i2v 種 85行**（M01_src..M85_src）＝ 計 **515 エントリ**（`--only` の `shots=` が 515）。生成 `generate_sdxl_4k.py PD-2026-050-centralpark`（**variants 指定なし＝1枚**・`--variants 3` を書かない）。i2v は Wan 2.2 A14B → RIFE 48fps で 85本。**factory 485 は生成せず在庫選抜。**
- **総生成 = still 430 + i2v seed 85 = 515枚（各1回）。** still を増やして factory を削るな（still-share 余裕 0.15%pt）。

## 5.2 SDXL と実写の振り分け（象徴のみ・cold-cyan）
- **SDXL 430（各1枚）= この事件にしか無い固有物:** empty chair・steel table・OFF REC light・読めない clock・five descending silhouettes・Korey spine silhouette・冷たい lab の DNA band・pen と署名の line・cell window with seasons・tipping scale・abstract night-park（treeline/lamp）・dawn horizon・headline mass（判読不能）・full-page 空白枠（**ad art 再現なし**）・Reyes の colder silhouette・記録の壁・the ghost の empty silhouette。
- **factory 485 = どこにでもある周辺:** 1989 NY の街/subway ambient・courthouse 外観・institutional 廊下・冷灰の room・park の abstract 夜景・薄明の街・ambient 繋ぎ。

## 5.3 共通スタイル接尾（各 SDXL 末尾 `[STYLE]`・A/B 同一）

> **★scope（owner 改定・EP50）:** `[STYLE]`（"no people, no visible face…"）と §5.4 `[NEG]` は **象徴 body 430 ＋ 抽象 i2v 種 69 にのみ**適用。**匿名・非識別の人物ビート（CODEX_A §5.11 の H シリーズ 16 i2v 種）は専用 `[HSTYLE]`/`[HNEG]`**（匿名人体は許可・実在 likeness/被害者/暴行/可読テキストは禁止のまま）。R-FACE は「顔・人体ゼロ」から**「匿名・非識別の人物は可／実在人物の likeness は不可」**に改定（DESIGN §1・CODEX_A §1/§5.5/§5.11・CODEX_B §2）。
```
, cinematic still, somber documentary grade, a cold forensic steel-cyan key light as the one recurring cool note, near-black ink institutional gravity, an empty interrogation room of a chair a steel table a wall clock and an unlit REC lamp, abstract night park of treeline and a single lamp never any crime imagery, cold cyan gel-electrophoresis bands as the forensic motif, a single dawn-amber note reserved for the very end, five descending child-height silhouettes and one taller-but-young spine silhouette, restrained dignified symbolism, telephoto compression and frontal composition, shallow depth of field, ultra-detailed, photoreal, 4K, 16:9, fine film grain, no text, no watermark, no logo, symbolic still-life, no people, no visible face, backs and hands and objects only
```
> EP39〜49 の色語（electric blue / midday suburban / sodium prison corridor / warrant-blue / porch-amber / teal-green hospital / crimson overdue / forest-green / civil-violet / somber-plum）を**1語も含めない**。EP50 の色は cold steel-cyan `#2F9FC4` ＋ 末端のみ dawn-amber `#C98A3C`。

## 5.4 共通ネガティブ（各 SDXL `Avoid:` ・A/B 同一）
```
text, words, letters, numbers, captions, watermark, logo, readable document, legible confession, legible lab report, legible newspaper, legible case citation, legible date, license plate, real celebrity, recognizable real person, identifiable face, portrait, mugshot, likeness of a specific person, human face, front-facing person, the five defendants, Trisha Meili, Matias Reyes as a person, victim, assault, rape, violence, blood, gore, injury, weapon, sexual content, nudity, crime scene, re-enactment, Donald Trump ad artwork, newspaper front page reproduction, barred cell interior gore, sensational distress, poverty porn, cartoon, illustration, anime, 3d render, low quality, blurry, jpeg artifacts, deformed, extra limbs, electric blue, sodium prison corridor, porch amber, teal-green hospital, crimson overdue, forest-green, civil-violet, somber-plum
```
> **the-five-were-involved を匂わせる絵を作らない**（innocence 絶対）。**被害者・assault・現場は一切描かない。** 読める confession/lab report/newspaper/case-citation を作らない（"blurred into an unreadable smear"）。Trump ad は**空白の full-page 枠のみ**（headline/art 再現禁止）。手錠/booking/room は institutional・非扇情（鉄格子/独房/暴力を描かない）。silhouettes は後ろ姿/手元/影のみ。

## 5.5 factory のファイル名を信じない（★BLOCKING・EP36/38 の教訓）
485本すべてを `scripts/build_footage_contact_sheet.py --ep PD-2026-050-centralpark --media video` で1本1フレームのラベル付き contact sheet にして**全点目視**。subtype 不一致は差替え。`select_centralpark_factory.py --verify-no-prior-overlap` で EP39〜49 の `stock_ledger*.json` sha256 被りゼロを確認。

## 5.6 AI開示（R1・毎回・強め）
AI 生成 still/i2v が画面に出ている間、常時右下 `AI-assisted visualization`（Oswald 20px / `#C8CDD6` / opacity 70% / `[W-32, H-28]`・字幕帯と縦 56px 以上）。概要欄1行：`Some visuals in this film are AI-assisted reconstructions, not photographs of the actual events. No image depicts any real person's face; the assault is never shown.`

## 5.7 A↔B 境界契約（asset_manifest スキーマ・EP39〜49 の不整合を潰す）
- 配列4本 **`stills` / `motion` / `factory` / `overlay`**（★全エントリ記載・**`public_path` 必須**）。
- `counts`（A/B 一字一致）：`{ "still_body": 430, "still_i2v_source": 85, "motion": 85, "factory": 485, "overlay": 60 }`。cuts 展開は still 505 / factory 485 / motion 170。
- `stills[].role` enum（この3値のみ・`thumb`/`still_thumb` を作らない）：`body` / `i2v_source` / `reject`。asset_id：body `^CPK-S\d{3}$`（S001..S430）／i2v種 `^CPK-MS\d{2}$`／motion `^CPK-M\d{2}$`。
- **also_thumb set（★A↔B 同一・`role="body"` かつ `also_thumb=true` の body still ちょうど 8枚）:** `{CPK-S001(empty chair+cold light), CPK-S018(OFF REC lamp), CPK-S095(five descending silhouettes), CPK-S210(the room / clock), CPK-S268(cold DNA bands), CPK-S331(Korey spine silhouette), CPK-S372(vacatur / dissolving signature), CPK-S408(dawn horizon)}`。thumbnail concept（SCALE_NOTE / STRUCTURE）= 五つの empty chairs、単一 cold-cyan light、**REC ドット OFF**、"NO CAMERA. NO LAWYER. NO MATCH."（no faces・ad-safe）。
- CODEX_A は書いた直後 `build_centralpark_asset_manifest.py --verify` で counts/role/also_thumb/overlay を突き合わせ（不一致 BLOCKING）。

---

# §6 — CODEX_B BRIEF（build_centralpark_film.py + AE + composite + gates + eyeball）

## 6.1 `build_centralpark_film.py`（`atwater/cleveland/strieff` の系を複製・centralpark 用）
- 生成物 `remotion/src/data/centralpark_film.json`（git 未追跡・再生成可能）。**`hookSeconds = 8.0`**・`narrationSeconds = 3606.0`（provisional・**FINAL は forced-align 実測で上書き**）・`OPENING_SEC 3.5`・`ENDCARD_SEC 9.0`。
- **`hookLine` = centralpark の正しい HOOK**（"Five children. A room with the camera switched off. …"・§1.1）。他話の hookLine を流用したら BLOCKER。
- `figures[]` = §4 の **165 beats**（全 kind union-valid・**dochighlight 0・stub 0・quote 0・votetally 0**）。`graphics[]=[]`。density は figures だけで floor 151 を +14 超える。
- shotlist：still 505 / factory 485 / motion 170 = **1,160 cuts** に機械展開（境界を `QUANT=f(0.5)=15f` グリッドにスナップ・mean 3.109s・max ≤7.0s）。
- **manifest fully populated**：`asset_manifest.v001.json` の全 `public_path` を検証し、欠落は BLOCKING（EP38 空マニフェスト回避）。
- Root 登録 **id=`Ep50Centralpark`**・`durationInFrames = caseFilmDurationInFrames(centralparkFilm, 30)` を同関数で再計算し **108,795（provisional）** に一致を assert（実測後は更新）。**`hookSeconds==8.0` を assert**（0 で 8s desync）。

## 6.2 音（EP43系 `build_centralpark_bgm_real.py` を複製・**BGM offset 11.5**）
- ラウドネス：完成 mp4 **-14.0 LUFS**（-16〜-12）・true peak ≤ -1.0 dBTP・VO -18.0・BGM bed（VO下）-22.0・(VO無)-17.0・ambient -30.0・ducking 5.0dB/attack 120ms/release 450ms。
- **VO OFF / film_offset / BGM offset = 11.5**（`measure_vo_wpm` 合格帯 168–190 wpm・190超は破棄→speed 0.95 再発注 BLOCKING）。
- 章 BGM（1章1トラック）：HOOK 低弦の不解決＋単一 metallic tick（**HOOK は完全無音に近い restraint**・digital 無音にはしない）／ACT1 cold・observational／ACT2 claustrophobic ピアノ＋弦／ACT3 oppressive／ACT4 slow・sparse／ACT5 転回→DNA hinge で唯一 raise（cold-cyan swell）／ACT6 解決しない和音→REC-ON/dawn で暖色に開く／ACT7 restraint 回帰。
- 最長無音候補 < 25s（`bgm_present` PASS）。**HOOK 無音区間・意図した breath に字幕キューを置かない。**

## 6.3 AE デッキ（★GO HEAVY・2-tier・~36 moments・cleveland clone を EXTEND・measured-fit・two-step aerender・repo path）
- `scripts/ae/build_centralpark_hero_cards.py` = `build_cleveland_hero_cards.py` を複製し **EXTEND**：cleveland の 6 layout を残したまま、**Tier B の新 builder 関数を ADD**（`buildDnaLadder` / `buildStatResolve` / `buildCardStack` / `buildRecLight` / `buildScaleTip` / `buildHeroTimeline` / `buildNameWall` / `buildSignatureErase`・reserve `buildHeadlineWall` / `buildInterrogationRoom`）。JSX の layout dispatch に各 `else if (spec.layout === "DNA_LADDER") …` を実装し、**末尾 `else throw "unsupported layout"` は保持**（未実装 layout を今後も弾く）。
- **Tier A 24枚**（§3.1・6 proven layout）＋**Tier B 12 moments**（§3.2・new layout）を生成。id/layout/CP-id/anchor が §3 と一字一致（`validate_centralpark_beats` が突き合わせ）。**DATE_STAMP/SEAM_TRANSITION は emit しない。VOTE_SPLIT は emit しない**（§3.2）。**QUOTE_CARD は `q-alone` の reserved 1枠のみ**、verified-verbatim が無い間は CENTER_STACK に fall back。
- **★Tier B の各新 layout は「実装 → 個別 `--dryrun` 単体レンダ通過 → `check_AE_layouts` allowlist に追加」の順**（存在しない layout を参照しない＝phantom-crash 回避の核心）。`build_centralpark_hero_cards.py --dryrun --only DNA_LADDER` 等で 1 comp ずつ `_build_ok.txt` を確認してから本番デッキに入れる。**`check_AE_layouts` の allowlist は EXACTLY { 6 proven } ∪ { dryrun 通過済 Tier-B }**（§7・phantom 0）。
- 色定数（0..1 float）：`ACCENT=[0.184,0.624,0.769]`（#2F9FC4）／`INK=[0.039,0.039,0.047]`／`BONE=[0.929,0.929,0.910]`／`DAWN=[0.788,0.541,0.235]`（**exoneration/close moment のみ**：REC_LIGHT-on・SCALE_TIP-right・HERO_TIMELINE-resolve・NAME_WALL-close・c-vacated・m-41m・c-state39・c-salaam）／`WHITE=[0.961,0.969,0.980]`／`SILVER=[0.784,0.804,0.839]`。フォント Anton（数値/主文字）/ Oswald（label・字幕）を厳格解決（miss は throw）。
- **measured-fit（全 tier）**：`fit_size()` pre-fit ＋ JSX `sourceRectAtTime(t,false).width` re-fit ＋ quote-wrap（advance-width 推定禁止）。**two-step（全 tier）**：JSX が `.aep` build → **assert `.aep` mtime > `.jsx`** → 別プロセス aerender。出力は **REPO path on C:**（`08_edit/ae_hero/render/`・exFAT H: は 0 mp4）。全 moment 右下に `AI-assisted visualization`（R1）。em-dash は beats.json ラベルで ASCII `-`。count-up 終了→区間末まで ≥1.20s ホールド。SPLIT_COMPARE/VOTE_SPLIT/NAME_WALL の複数値は**別レイヤー**（改行禁止）。
- **★YEAR のコンマ群化バグ修正（EP46 で発覚）:** Remotion `NumberTicker`/`FigureBeats` は既定で thousands-comma 群化し、年を "1,985" と描画した。**`group` opt が追加された** → CODEX_B は **YEAR を出す全 figure/AE numeric（1989 / 2002 / 2014 等）に `group:false` を必ず set**（`HERO_TIMELINE` の year node・年を出す `stat`/`numberticker`/`lowerthird` すべて）。**桁区切りが正しい数値（6,000,000,000 / $41,000,000）は `group:true`（既定）**。混同しない。
- machine traps（cleveland §7.6 全項・Tier B の長尺 comp にも適用）：font unwrap＋HARD FAIL・spatial ease dim・`app.newProject()` 不使用（同名 `CENTRALPARK_` コンプ防御削除）・per-layer motionBlur（動くレイヤー個別）・`"ADBE Rotate Z"`・inPoint/outPoint 両設定・`conformFrameRate=30`・単一行 TextDocument・SOFTWARE gpu・localized RS/OM 名優先（`"最良設定"`/`"H.264 - レンダリング設定を一致 - 15 Mbps"`）・完了マーカー `_build_ok.txt` ポーリング（Tier B は長尺なので **≥420s** タイムアウト）・`app.quit()`。Tier B の JSX は算術しない（表示文字列は Python が precompute）。

## 6.4 composite（`composite_centralpark_hero.py` = `composite_caniglia_hero.py` 複製・SKIP 4条件を削らない）
- `BASE = centralpark_final_bgm.v001.mp4`（build_centralpark_bgm_real.py→**film_offset 11.5**）／`OUT = centralpark_final_bgm.v002_ae.mp4`（**v001 を絶対に上書きしない**）。
- SKIP：(1) `render/<id>.mp4` 不在 (2) 解像度≠1920x1080 (3) 実測尺 `< dur-0.3` (4) `beat.end > base_dur`。ffmpeg：`overlay=0:0:eof_action=pass:enable='between(t,start,end)'` / `-c:v libx264 -preset slow -crf 16 -pix_fmt yuv420p -colorspace bt709 -c:a copy`。**film_offset 11.5 を適用**（body-relative→absolute）。

## 6.5 staging & render
- **public_slim staging**：`public → public_slim` へ img/factory/motion/audio 全メディアをコピー（~1,000 distinct assets・**12分エピの ~4–5× ディスク**を先に確保・EP38 50GB-copy trap 回避）。本編 `--public-dir=public_slim --concurrency=4`。
- ★開始前にマシン状態確認（heavy-job preflight）。~108,795 フレーム = multi-hour render。

## 6.6 FULL-60min 3× eyeball（★"done" の前・hard gate）
測定（sampled 1-frame 禁止）で全 ~60分を **3周**：(1) structure/カット (2) caption-text (3) audio-sync。measured > estimated。`check_final_acceptance 50` に進む前に必須（§7）。

---

# §7 — GATE LIST（architecture §6 と一致・全 PASS まで出荷しない・lessons are gates, not promises）

## 7.1 Preflight（before spend）
| gate | 内容 |
|---|---|
| `check_script_length` | **60-min band**（12分 2,141 cap ではない）。`--longform` mode or 明示 cap ≈10,900。script 10,715 words が band 10,500–10,900 内であることを確認 |
| `check_centralpark_facts.py`（`check_strieff_facts.py` を clone・出力 `facts_lock.v001.json`） | 内部ルール **R-INNOCENCE**（five が関与を匂わせない／Armstrong は rejected のみ）・**R-VICTIM**（dignity・no depiction・record 以上に naming しない）・**R-REYES**（established facts のみ・lurid detail 禁止）・**R-NUM**（hedged 数値：interrogation hours・per-person years・per-person $・Trump ad cost・Gonzalez murder month・Wise facilities を断定で焼かない）・**R-FACE**（no faces）・**R-DOCHL**（dochighlight=0・grep 0）・**R-QUOTE**（verified verbatim ＋ attribution のみ・invented quote 禁止） |
| `validate_centralpark_beats` | §3 AE **36 moments**（Tier A 24 + Tier B 12）と §4 figures 165 を突き合わせ：AE↔AE・AE↔figures が1秒も重ならない／Tier A layout ∈ 6 proven／Tier B layout ∈ implemented+dryrun-passed／id・layout・CP-id・anchor が CODEX_B と一字一致／YEAR は group:false |
| `check_centralpark_asset_manifest` | counts/role enum/`public_path`/also_thumb（8枚 set）を A↔B 一字一致で検証 |
| `check_AE_layouts` | **allowlist = EXACTLY { 6 proven: ACT_TITLE_CARD, CENTER_STACK, MONEY_STACK, QUOTE_CARD, VOTE_SPLIT, SPLIT_COMPARE } ∪ { implemented+dryrun-passed Tier-B: DNA_LADDER, STAT_RESOLVE, CARD_STACK, REC_LIGHT, SCALE_TIP, HERO_TIMELINE, NAME_WALL, SIGNATURE_ERASE (+HEADLINE_WALL / INTERROGATION_ROOM if used) }**。**DATE_STAMP / SEAM_TRANSITION = FAIL**（build クラッシュ）。**phantom（allowlist に無い、あるいは builder に実装されていない layout を beats.json が参照）= FAIL**。★各 Tier-B は `--dryrun` 単体レンダ通過が allowlist 入りの前提（gate はその通過ログ `_build_ok.txt` を確認） |
| topic novelty gate | EP1–49 inventory を grep：Central Park jogger / Exonerated Five が slate に新規であることを確認（EP46=Kelo/EP47=Mahanoy dup の再発防止） |

## 7.2 Post-build（before final）
| gate | floor / 内容 |
|---|---|
| `check_motion_density --ep PD-2026-050-centralpark` | figures ≥ **151**（設計 165）・≥2.5/min（設計 2.745）・variety ≥6（設計 15）・**dochighlight=0** |
| `check_animation_mix --ep …` | still-share ≤0.45（設計 0.4353）・motion coverage ≥0.45（設計 0.5647） |
| `check_caption_integrity` | ナレ一致 ≥99%（faster-whisper 強制アライン）・`.srt` カバー ≥95%・cue 1.0–6.0s・CPS ≤17・単語割り禁止・ズレ ≤120ms・**HOOK 無音/意図 breath 区間に cue を置かない** |
| `visual_asset_qc` | 全 still/factory/motion 目視 QC・black frame ゼロ・R2 no-face を全 asset で確認 |
| `check_asset_reuse` | first-use ≥0.70（設計 0.8621）・EP39〜49 と sha256 被りゼロ |
| `preflight_render_gate` | machine state・public_slim ディスク・durationInFrames assert |
| chaptered timestamps | 7幕を YouTube chapters として概要欄に（retention de-risk・tease naming） |

## 7.3 Post-render（before "done"）
- **FULL 60-MINUTE eyeball, 3×**（structure / caption-text / audio-sync・measured, not 1-frame sampled）。
- `check_final_acceptance 50`。

---

## ★ HANDOFF NOTE
本書 = intent の実装指示。CODEX_A（画像/asset 生成・§5）と CODEX_B（build/render/AE/composite/gates・§6）は本書から継承し、**A↔B は `asset_manifest.v001.json` のみで接続**。全数値は SPEC の 5×-arithmetic（§0.6）か facts ledger（CP01–CP35・§3/§4）に traceable で、手書きの発明はゼロ。**AE は GO HEAVY の 2-tier ~36 moments**：Tier A（6 proven layout・`build_cleveland_hero_cards.py` で検証済）＋ Tier B（8 個の**新 layout を実装 → `--dryrun` で単体証明 → `check_AE_layouts` allowlist 追加**してから使用＝phantom-crash なしで heavy に行く方法）。figure kind（15種）は実 `FigureBeats.tsx` union で全数検証済。**emitted QUOTE_CARD・VOTE_SPLIT・dochighlight は fact-discipline により意図的に不使用**（reserved `q-alone` のみ verbatim ロック時に活性・§3.2/§4）。**YEAR は `group:false`**（EP46 の "1,985" コンマバグ回避）。narrationSeconds 3606.0 と durationInFrames 108,795 は provisional で、**FINAL は measured TTS / forced-align**（VO master 後に SPEC + Root を更新）。
