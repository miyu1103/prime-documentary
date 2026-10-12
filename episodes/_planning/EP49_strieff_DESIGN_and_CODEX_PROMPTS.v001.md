# EP49 — THE WARRANT IN YOUR POCKET — 制作設計書（DESIGN 本体・v001・確定台本版）

- Episode ID: `PD-2026-049-strieff` / slug: `strieff` / EP49
- 中心の問い（英語・二人称・★"停止は合法だった"と書かない）: **"If an officer stops you on the street for no reason at all, and then runs your name, can everything he finds after that be used against you in court?"**（答え＝2016年に最高裁が「使える（証拠は許容）」と言った。ただし停止は**違法**のまま。証拠が生き残るのは**先在する令状が違法な停止と発見の因果を attenuate（希釈/遮断）したから**という一点のみ）
- 判例: **Utah v. Strieff, 579 U.S. 232 (2016)**（docket 14-1373・decided **2016-06-20**・opinion **Justice Clarence Thomas**・第4修正/排除法則/attenuation doctrine）。**票決 5-3**（Thomas 多数＝Roberts・Kennedy・Breyer・Alito／**Sotomayor 反対**・**Kagan 反対**）。**Scalia 死去で空席＝8名構成**。
- 主役: **Edward Strieff**（**存命の私人・本件後に薬物所持で有罪＝R2**）。**顔・肖像・身体を一切描かない。象徴のみ・尊厳の物語。** 薬物は臨床的最小限（1回だけ・非扇情）。Detective Fackrell も人物化しない。
- 主題: 停止は**違法**（州が合理的疑い不在を CONCEDE・最高裁も前提）。にもかかわらず、**先在する有効な令状**が違法停止と証拠発見の因果を **attenuate（遮断）** したため証拠は**許容**され、有罪は維持された。排除法則は**廃止でなく"狭められた"**。本作は「停止は合法だった／排除法則は廃止された」と決して言わない。**"the stop was illegal, but the evidence stayed — because the warrant broke the chain"** が背骨。Sotomayor / Kagan 反対がその対抗軸（逐語・反対意見に中立帰属）。
- Status: **BINDING**。**唯一の真実 = 機械生成済み `EP49_strieff_PRODUCTION_SPEC.v001.json`**。本書のあらゆる数値はそこからの転記で、手書きで発明していない。衝突したら SPEC が勝つ。
- このファイルは**設計パッケージ3分割**（DESIGN / CODEX_A / CODEX_B）の **DESIGN 本体**。共有ブリーフ `EP49_strieff_DESIGN_BRIEF.shared.md` を単一の真実源とする。85本の SDXL プロンプト実体・i2v 16・factory 93 選定は **CODEX_A**、`build_strieff_film.py`・captions・figures 実装・Root.tsx 登録・AEビルダ/コンポジタ・ゲートは **CODEX_B** に属す（本書は各所でポインタのみ示す）。

## ★このエピソードの唯一の真実（手書きで数値を発明するな）

`episodes/_planning/EP49_strieff_PRODUCTION_SPEC.v001.json`（台本から機械生成・`scripts/build_production_spec.py`）。本設計書は SPEC を**人間可読な実装指示に翻訳しただけ**で、新しい数字を作っていない。

```
words_total          = 2,139
narration_seconds    = 720.6   （= 12.0分・[SILENCE 1] の実音無音を含む）@ wpm_used 178.1
scenes               = 48      （S01..S48・確定。増やすな減らすな）
total_cuts           = 226
still  distinct 85 / cuts 101 / mean 1.19 / cap 2   ← ★各1枚生成（バリエーション0）
factory distinct 93 / cuts 93 / mean 1.0  / cap 1   ← 在庫選抜・全点目視QC
motion distinct 16 / cuts 32 / mean 2.0  / cap 2
distinct_total       = 194
first_use_share      = 0.8584  （floor 0.70）
still_share_of_cuts  = 0.4469  （cap 0.45）
motion coverage      = (93+32)/226 = 0.5531  （floor 0.45）
MG beats_floor       = 31      （film.json 側 figures+graphics+heroCuts。AEカードは check_motion_density に数えられない）
beats_per_min_floor  = 2.5   /  variety_floor = 3
mean_shot_seconds    = 3.19   /  max_shot_seconds = 6.0
SPEC 幕秒（発話・語数から機械算出）: HOOK 65.7 / OPENING 59.6 / ACT1 131.0 / ACT2 129.0 / ACT3 186.3 / ENDING 120.9（合計 692.5s）
  ※ SELF-CHECK 241語/81.2s は台本末尾の著者自己点検＝非発話（narration に数えない）
  ※ 発話幕秒合計 692.5 と narration_seconds マスター 720.6 の差 28.1s = 幕間の息継ぎ＋設計無音（SILENCE 1 = 1.8s）を内包する測定マスター。film.json には 720.6 を入れる。
```

## ★★ 最重要の前提: 1シーン1枚・バリエーション0 ★★（ブリーフ§1）

- Codex の画像生成は高精度。**同一ショットの複数バリエーション（`_01/_02/_03`）を作らない。**
- `04_scenes/ai_prompts.v001.md` は **still 85本＝85行の固有プロンプト**（`generate_sdxl_4k.py` の `read_prompts()` 2行形式・各1枚）＋ **i2v 種 16行** ＝ **計101エントリ**（`--only S01` の `shots=` は 101）。**`--variants 3` は使わない**（`--variants 1` または variants 指定なし）。
- **総生成画像 = still 85 + i2v seed 16 = 101枚（各1回）。** **factory 93 は生成ではなく在庫選抜**（全点目視QC・EP39〜48 と sha256 被りゼロ）。
- **still を増やして factory を削るな**（still-share 0.4469 は cap 0.45 に対し余裕 0.31%pt しかない）。**still-cut は 101 で固定。**

## ★EP39〜48 で踏んだ失敗＝本書が最初から潰す設計判断

| # | 失敗 | 本書での恒久対策 | 参照 |
|---|---|---|---|
| 1 | **番号ズレ**（別リストを発明） | シーンは **SPEC の S01..S48 に固定**。still 資産 ID は S01..S85（別空間・cross-map 禁止） | §3.2 / §9 |
| 2 | **紙芝居**（still 100% で animation_mix FAIL） | still-cut **101 固定**＋factory実写 **93**＋i2v **32**。still-share 44.69% ≤45% / motion cov 55.31% ≥45% を構造保証 | §5.1 |
| 3 | **バリエーション水増し** | **1シーン1枚・85本を各1枚**。variants 禁止 | §5.3 |
| 4 | **画像プロンプトのパーサ非互換** | `read_prompts()` の**2行形式**。CODEX_A が `--only S01` で拾い数（101）を確認 | §9.1 |
| 5 | **ファイル名を信じた**（牛が documents） | factory 93本を `build_footage_contact_sheet.py` で**全点目視QC**（CODEX_A 必須・BLOCKING） | §5.4 |
| 6 | **AEカードを密度に数えた** | `check_motion_density` は film.json の `figures+graphics+heroCuts` だけ。**film.json 側に MGビート 31本以上**（本書は 34 設計）。AE は composite 後で 0 カウント | §6.1 / §7.1 |
| 7 | **一枚絵で完成判定**（EP39-41/EP3941 の眼球不足） | 全編アイボール必須（§13）。measured > estimated | §13 |
| 8 | **A↔B マニフェスト不整合** | asset_manifest は **A↔B で同一スキーマ・counts/role enum を一字一致**。role=`thumb`/`still_thumb` を作らない。サムネは `also_thumb=true` の body still 6枚 | §5.8 |
| 9 | **dochighlight のバグ見え**（EP40/41/42 で3回指摘） | **`dochighlight` を figures に1件も入れない（grep 0・R-DOCHL）。** 書類/令状/画面は `lowerthird` の説明テキストで表す | §6.2 / §7.3 |
| 10 | **停止を"合法"と誤記／排除法則を"廃止"と誤記**（本作固有の最大リスク） | 停止は **ILLEGAL**（州が譲歩・最高裁も認定）。証拠は **attenuation 経由でのみ**許容。排除法則は **NARROWED, NOT ABOLISHED**。`the stop was legal / exclusionary rule abolished` を書かない（R-LEGAL） | §1.2 |
| 11 | **票決の誤記**（"6-3" 混入） | **5-3・Scalia 空席で 8名**。多数=5・反対=3。自動要約が言う "6-3" は誤り（R-VOTE） | §1.2 |
| 12 | **"we are all harmed" を逐語引用**（非逐語） | **"we are all harmed" は逐語でない＝一切引用しない**。皆が害される論点は Sotomayor 逐語 "anyone's dignity can be violated in this manner" か地の文で（R-QUOTE） | §1.2 |

---

# 0. 環境・Remotion設定（CLAUDE.md §0 準拠）

## 0.1 本編 `Ep49Strieff` の Composition 設定（★本編の正・誤記注意）

| 項目 | 値 |
|---|---|
| `id` | **`Ep49Strieff`**（Root.tsx に `CaseFilm` で登録。ブリーフ§5「id Ep49Strieff」。**id の切り詰め・綴り違い・大文字化は誤記＝BLOCKER**） |
| 解像度 | **1920 × 1080** |
| `fps` | **30**（EP44〜48 と同値。フレームは全て `Math.round(30 × 秒)`・直書き禁止） |
| `hookSeconds` | **8.0**（★BrandOpening 前の**無音コールドオープン teaser preroll**＝フラッシュモンタージュ。§3.1 参照。durationInFrames 4項関数の第1項に入る） |
| `durationInFrames` | **`caseFilmDurationInFrames(strieffFilm, 30)` = 22233**（4項の実関数 `round(hookSeconds×30)+round(OPENING_SEC×30)+ceil(narrationSeconds×30)+round(ENDCARD_SEC×30)`・**hookSeconds=8.0**・§3.1[3] で算出。手書きで数値を入れず関数で算出する） |
| component | `remotion/src/compositions/CaseFilm.tsx`（**既存の汎用 `CaseFilm` を再利用**・実在確認済。`Bookends.tsx` の `BrandOpening`/`BrandEndcard` を **import**・fork 禁止） |
| data | `remotion/src/data/strieff_film.json`（`scripts/build_strieff_film.py` で再生成できる状態を保つ＝**git 未追跡**） |

**Root.tsx 登録（★ブリーフ§5・CODEX_B が実装）:**
```tsx
import {strieffFilm} from './data/strieff_film.json';
import {caseFilmDurationInFrames} from './lib/caseFilmDuration';
// ...
<Composition
  id="Ep49Strieff"
  component={CaseFilm}
  width={1920} height={1080} fps={30}
  durationInFrames={caseFilmDurationInFrames(strieffFilm, 30)}  // = 22233
  defaultProps={{film: strieffFilm}}
/>
```
> **id は `Ep49Strieff`**（切り詰め・綴り違い・先頭大文字化などは全て誤記。ブリーフ§5 の render 行 `Ep49Strieff` が正）。`CaseFilm.tsx` は実在。`caseFilmDuration` ヘルパの実体名は CODEX_B が既存実装（atwater/cleveland と同一）に合わせる。

## 0.2 タイトルバンパー `OpeningStrieff` の Composition 設定（CLAUDE.md 正典部品準拠）

| 項目 | 値 |
|---|---|
| `id` | **`OpeningStrieff`** |
| 解像度 | **1920 × 1080** |
| `fps` | **60**（CLAUDE.md §0 の正典値。OP 単体は 60fps） |
| `durationInFrames` | **180**（= 3.0秒 @ 60fps） |
| component | `remotion/src/compositions/OpeningStrieff.tsx`（§11 全仕様） |

> `OpeningStrieff` は**独立したタイトルバンパー成果物**（`out/strieff_opening.mp4`）。本編内 OP/ED の正典は `Bookends.tsx`（`BrandOpening` 3.50s / `BrandEndcard` 9.00s・不変）。`OpeningStrieff` を本編に ffmpeg で焼き込まない（オーナー承認なしに見え方を変えない）。

## 0.3 必要な依存パッケージ

```bash
cd C:\Users\aab15\Documents\prime-documentary\remotion
npm i @remotion/motion-blur     # CLAUDE.md 必須依存（Trail によるモーションブラー）
```

## 0.4 `remotion.config.ts`（CLAUDE.md §0 正典値・EP41〜48 と同一・書き換えない）

```ts
import {Config} from '@remotion/cli/config';
import os from 'os';

Config.setVideoImageFormat('png');               // png
Config.setConcurrency(os.cpus().length);         // 全コア並列 concurrency最大
Config.setCodec('h264');                          // H.264 libx264（NVENC 禁止）
Config.setCrf(16);                                // CRF16
Config.setX264Preset('slow');
Config.setPixelFormat('yuv420p');                 // pixelFormat yuv420p
Config.setColorSpace('bt709');                    // colorSpace bt709
Config.setAudioCodec('aac');                      // 音声 aac
Config.setAudioBitrate('320k');                   // 320k
Config.setChromiumOpenGlRenderer('angle');        // GPU=angle
```
> レンダーログで `crf 16 / preset slow / yuv420p / bt709 / aac 320k / libx264` を必ず確認。本編レンダは `--public-dir=public_slim --concurrency=4`（ブリーフ§5・**public→public_slim へ img/factory/motion/audio 全メディアをコピー staging**＝EP45事故回避）。

## 0.5 ブランド／レーン色（`remotion/src/brand.ts` から import・ハードコード禁止）

**EP49 のパレット（★ユタの夜の駐車場＋冷たい institutional の database/booking＋淡い大理石の最高裁＋唯一の差し色 somber-plum）:**
```
INK     = #0A0A0C   ルート背景（サムネ bg と一致）
NIGHT   = #0E0B12   ユタの夜・家の前・駐車場の plum を帯びた near-black（HOOK/ACT1 側）
STEEL   = #1C1E24   database/booking の冷灰・institutional（無人・鉄格子/独房は描かない）
MARBLE  = #33313A   最高裁の冷たい大理石（ACT3・列柱・空席）
ACCENT  = #9C6BAA   ★somber-plum（尊厳と喪失の一点差し色）。ブランド数値・ライン・下線・グロー・OP/AE/サムネ accent。★EP41 gold / EP42 blue / EP43 amber / EP44 teal / EP45 crimson / EP46 green / EP47 civil-violet #7A5CD0 / EP48 を流用しない
WHITE   = #F5F7FA
SILVER  = #C8CDD6   （AI開示テキスト）
```
> **レーン分離:** EP41 gold / EP42 blue / EP43 amber / EP44 teal / EP45 crimson / EP46 green `#3F8F5F` / EP47 civil-violet `#7A5CD0` と被らないよう、EP49 は **ユタの夜の plum near-black `#0E0B12` ＋ database 冷灰 `#1C1E24` ＋ 冷たい大理石 `#33313A` を基調＋唯一の差し色＝somber-plum `#9C6BAA`**。接尾に `porch-amber` `warrant-blue` `teal-green hospital` `crimson overdue` `forest-green` `civil-violet` を含めない。**factory は EP39〜48 の `stock_ledger*.json` の sha256 を除外**（CODEX_A・BLOCKING）。**CODEX_B は OP props / AEカード / サムネ accent を必ず `#9C6BAA` にする（他話色の流用は BLOCKER）。**

---

# 1. 事実の取り扱い（★正確性6制約＝FACTS LOCK / `check_strieff_facts.py`・BLOCKING）

## 1.1 確定台本（唯一の正・1バイトも変えない）

```
C:\Users\aab15\Documents\prime-documentary\episodes\_planning\EP49_strieff_script.en.v001.md
```
**本番配置先:** `episodes/PD-2026-049-strieff/03_script/script.en.v001.md`（上記を1バイトも変えずコピー）。整形も禁止（AI臭再発と語数ゲート再計算を招く）。台本の幕構成（HOOK / OPENING / ACT_1 / ACT_2 / ACT_3 / ENDING）と `【SILENCE 1 — 1.8s】`（**1箇所**）を正典とする。存在しない演出マーカーを発明しない。

## 1.2 ★正確性6制約（全出力＝プロンプト・カード文言・図表・字幕・タイトルに適用。1つでも違反＝BLOCKER）

| # | 制約 | 出力での順守 |
|---|---|---|
| **C1** | **停止は違法（ILLEGAL）。"合法"と言わない。証拠が生き残るのは attenuation 経由のみ** | 州が合理的疑い不在を CONCEDE・最高裁も前提（S03）。**`the stop was legal / lawful stop / valid stop`（本件停止を主語に）を使わない。** 枠は **"the stop was illegal / unlawful / broke the rules" ＋ "but the evidence stayed — via attenuation"**。ENDING の不安は「停止が合法だから」ではなく「**違法な停止が令状に救われて対価を生むから**」に置く |
| **C2** | **排除法則は狭められた（NARROWED）、廃止ではない（NOT ABOLISHED）。attenuation は例外** | 排除法則＝通常は違法捜索の証拠を排除（fruit of the poisonous tree）。attenuation はその**例外**（S07）。**`exclusionary rule abolished / struck down / eliminated / gone` を使わない。** 枠は "narrowed / weakened / a new exception / carved out"。3要素（S09）を正確に: ①時間的近接（数分＝**抑制寄り**・州が負けた）②**介在事情＝先在する有効な令状**（州寄り・**決定的**・鎖を断つ）③目的/悪質性（flagrancy）（州寄り・**せいぜい過失、悪質でない**）。②③が①を上回った |
| **C3** | **票決 5-3・Scalia 空席で 8名・中立帰属** | Thomas 多数（Roberts・Kennedy・Breyer・Alito 参加）／**Sotomayor 反対**（Ginsburg が I-III 同調・Part IV "carceral state" は単独）／**Kagan 反対**（Ginsburg 同調）（S10–S12）。**5-3 を中立に示す**（どちらが「正しい」と画面で断じない）。**"6-3" と書いたら FAIL**（自動要約の既知エラー）。Scalia の空席＝8名を明示 |
| **C4** | **反対意見の逐語は DISSENT に中立帰属・"we are all harmed" は使わない** | Sotomayor "carceral state"（S13）・"anyone's dignity"（S14）・Kagan incentive（S16）を **DISSENT** に中立帰属（Court に帰属させない）。attribution 厳格＝`Justice Sotomayor, dissenting` / `Justice Kagan, dissenting`。**★"we are all harmed" は逐語でない＝1箇所も引用しない**（S15・R-QUOTE）。要約を引用符に入れたら FAIL |
| **C5** | **Edward Strieff＝R2・象徴のみ／薬物は臨床的最小限** | 存命の私人・本件後に薬物有罪。**顔・肖像・身体を描かない**。象徴のみ（夜の家・後ろ姿・駐車場・パトカーのライト・ID・無線・令状ヒットの画面・手錠・小さな証拠袋・断ち切られた鎖・空席・天秤・最高裁列柱・ファイルの壁）。**薬物は臨床的最小限**（メタンフェタミン言及は1回・非扇情・血/暴力/現場を描かない）。Detective Fackrell も人物化しない。Strieff を美化しない |
| **C6** | **数値・引用は原典一致・捏造ゼロ・medium 値は画面に断定で出さない** | 画面に焼く hard 数値は **5-3（票・high）／2016 · SUPREME COURT（判決日 high）／579 U.S. 232（cite・high）／8 JUSTICES · SCALIA'S SEAT VACANT（high）／3 FACTORS（Brown v. Illinois・high）／South Salt Lake City, Utah · 2006（★台本 ACT_1 apparatus が指定したカード）** のみ（§1.4）。**confidence:medium（Fackrell 名・"about a week" 監視期間・手続経緯）はヘッジ＝画面に断定で出さない**（発話のみ許容・R-HEDGE）。捏造引用禁止 |
| **R1** | **実在人物の顔・肖像を生成しない** | 全生成ビジュアル表示中は `AI-assisted visualization`（右下）常時表示。概要欄に1行 AI 開示 |

## 1.3 6制約ゲート `check_strieff_facts.py`（`scripts/check_strieff_facts.py`＝EP45 `check_cleveland_facts.py` を strieff 用に複製。exit≠0 で出荷停止・CODEX_B 実装。出力 `facts_lock.v001.json`）

> **★ゲート名は1本に確定:** 6制約の機械ゲートは **`scripts/check_strieff_facts.py`**（出力 `09_package/facts_lock.v001.json`）ただ1つ。**DESIGN / CODEX_A / CODEX_B で同名参照**（別名を作らない）。内部ルール **R-*** に一本化して実装する。**★R-NUM 等の構造ルールは narrative figure のみ対象**（asset_manifest 構造カウント・acttitle index は除外＝EP45 修正済を継承）。

**検査対象:** `03_script/script.en.v001.md` / `remotion/src/data/strieff_film.json` の `figures[].kind`・`figures[].*text*`・`quote`・`attribution`・`lines[]`・`label`・`primary`・`secondary` / `08_edit/ae_hero/beats.json` の `hero`/`top`/`bottom`/`sub`/`attribution`/`caption` / `09_package/description.txt` / `remotion/props/strieff*.json` の `subtitle`/`title` / `04_scenes/ai_prompts.v001.md`。

| ルール | 内容 |
|---|---|
| **R-LEGAL（★EP49 固有・最大リスク）** | 本件停止を主語に `the stop was legal` / `lawful stop` / `valid stop` / `legal stop` が出たら FAIL。`exclusionary rule (was )?(abolished\|struck down\|eliminated\|gone\|overturned)` が出たら FAIL。**"illegal / unlawful / broke the rules / no reasonable suspicion" の枠が停止の描写に無いまま停止を肯定的に描いたら FAIL。** 証拠許容の payload には `attenuat` / `warrant broke the chain` / `intervening` のいずれかが同一 payload に必要（「合法だから証拠 OK」誤読の防止） |
| **R-ATTEN** | 3要素を扱う payload は Brown 由来の枠を保つ: `time / temporal` は **suppression 寄り**、`warrant / intervening` は **State 寄り・decisive**、`flagran / negligent / purpose` は **State 寄り・at most negligent**。②③が①を上回った、という帰結を反転させたら FAIL。`attenuation` を「停止を合法化した」と説明したら FAIL（attenuation は違法を消さず因果を断つ） |
| **R-VOTE** | `5 ?- ?3` 以外の票（特に `6 ?- ?3`）が Strieff の判決票として出たら FAIL。5-3 を焼く payload に `evidence (stayed\|admissible\|came in)` / `conviction stood` / `upheld` / `Scalia` / `eight justices` のいずれかが同一 payload に無ければ FAIL。多数を "abolished/struck down" と結ばない |
| **R-QUOTE（帰属厳格）** | `quote` は §2 `APPROVED_QUOTES` の逐語のみ。**Sotomayor "carceral state"**（S13 全文）の attribution は `Justice Sotomayor, dissenting` と一致必須。**Sotomayor "anyone's dignity"**（S14）も `Justice Sotomayor, dissenting`。**Kagan incentive**（S16）は `Justice Kagan, dissenting` と一致必須。**反対逐語を Court/majority に帰属させたら FAIL**。**★`we are all harmed` が引用符内 or `quote` に出たら FAIL**（非逐語・S15）。要約を引用符に入れたら FAIL。attribution 空なら FAIL |
| **R-FACE / R-DRUG** | `ai_prompts` 正プロンプトに `portrait`/`face of`/`likeness`/`recognizable`/`Edward Strieff`（人物として）/`mugshot`/`his body` が出たら FAIL（ネガティブ使用は可）。`drug use`/`needle`/`smoking meth`/`overdose`/`addict`/`crime scene`/`blood` が正プロンプトに出たら FAIL（**閉じた小さな証拠袋の象徴は可**）。薬物名の画面文字列化は不可（発話1回のみ・臨床） |
| **R-HEDGE** | 画面文字列（figures/AE/字幕見出し/props）に **§1.4 の表以外の数値/固有名**が出たら FAIL。特に **`Fackrell` を hard nameplate/stat に出したら FAIL**（confidence:medium・発話のみ許容）。`about a week` を数値カードにしたら FAIL。`5-3`/`2016`/`579 U.S. 232`/`2006` を焼く figure/AE は台帳一致必須 |
| **R-DOCHL（★全話共通）** | `figures[].kind == "dochighlight"` が **1件でも**存在したら FAIL（`grep -c '"dochighlight"'` が 0 でないと出荷停止）。`comparebars` も非実在→出たら FAIL（`compbars` が正） |
| **R-DISCLOSE** | `description.txt` に AI 開示1行が無ければ FAIL。全生成ビジュアル区間で右下 `AI-assisted visualization` が焼かれていること（§13 アイボールで確認） |

**出力:** `09_package/facts_lock.v001.json`（`{"pass":bool,"violations":[{"file","rule","line","excerpt"}],"skipped":[...]}`）。`pass:true` でない限り `check_final_acceptance.py` に進まない。

## 1.4 画面に出してよい確定数値（★台本／事実台帳 S00–S19 に存在し confidence:high のものだけ。この表以外を画面に出すな）

| ID | 値 | 台本／台帳での根拠（claim） | conf | 使用先 |
|---|---|---|---|---|
| N01 | **5 – 3**（THE EVIDENCE STAYED・ADMISSIBLE） | "By a vote of five to three … the methamphetamine was admissible … conviction stood"（ACT3・S10） | **high** | AE **v01**（VOTE_SPLIT・**R-VOTE 対語 "THE EVIDENCE STAYED / ADMISSIBLE" 必須**）/ figures `votetally`（F-VOTE） |
| N02 | **8 JUSTICES · SCALIA'S SEAT VACANT** | "only eight justices that term … Scalia had died … his seat was still empty"（ACT3・S10） | high | AE **v01**（VOTE_SPLIT の sub）/ figures `stat`（F-STAT 8）/ `lowerthird` |
| N03 | **2016 · SUPREME COURT**（decided June 20, 2016） | "decided in 2016"（OPENING・S00） | high | AE **t01**（CENTER_STACK） |
| N04 | **579 U.S. 232** | Utah v. Strieff, 579 U.S. 232 (2016)（S00） | high | AE **t01**（CENTER_STACK の下段テキスト）/ figures `lowerthird`（本文で読み上げない） |
| N05 | **3 FACTORS**（Brown v. Illinois） | "three factors: time, intervening events, and how bad the police behavior was"（ACT2・S09） | high | figures `stat`（F-STAT 3・label "the attenuation test"）/ `lowerthird` |
| N06 | **SOUTH SALT LAKE CITY, UTAH · 2006** | 台本 ACT_1 apparatus 指定カード（S02） | high | figures `lowerthird`（F-LT place） |
| N07 | **Sotomayor 逐語 "…you are not a citizen of a democracy but the subject of a carceral state, just waiting to be cataloged"** | ACT3・S13（Part IV） | high | AE **q01**（QUOTE_CARD・帰属 **Justice Sotomayor, dissenting**）/ figures `quote`（F-QUOTE1） |
| N08 | **Sotomayor 逐語 "The white defendant in this case shows that anyone's dignity can be violated in this manner"** | ACT3・S14 | high | figures `quote`（F-QUOTE2・帰属 **Justice Sotomayor, dissenting**） |
| N09 | **Kagan 逐語 "The officer's incentive to violate the Constitution thus increases…"** | ACT3・S16 | high | AE **k01**（QUOTE_CARD・帰属 **Justice Kagan, dissenting**）/ figures `quote`（F-QUOTE3） |

> **★AE/figures 文言に「the stop was legal / exclusionary rule abolished / we are all harmed / 6-3」を書かない（C1/C2/C3/C4・R-LEGAL/R-VOTE/R-QUOTE）。** **Fackrell 名・"about a week" は画面に出さない（R-HEDGE・medium）。** docket `14-1373` は t01（place）と figures `lowerthird` に退避（本文で読み上げない）。**5-3 は台帳（S10）にあるので焼いてよいが、必ず "THE EVIDENCE STAYED / ADMISSIBLE / CONVICTION STOOD / 8 JUSTICES" の対語を同一 payload に持つ（R-VOTE）。** 投票の「正誤」を画面で断じない（C3 中立）。

---

# 2. 視覚・音響レーン分離（EP39〜48 との素材被り回避）

> **EP39〜48 のファイルには一切触れない（読み取りのみ可）。** レーンを機械的に分離する。

| 軸 | EP47 atwater | **EP49 strieff** |
|---|---|---|
| 舞台 | テキサスの道→booking→大理石 | **ユタの夜の家の前→駐車場（後ろ姿の人影）→路肩の刑事の車（パトカーのライト）→ID の照会→無線→令状ヒットの画面→手錠→逮捕に伴う捜索（小さな証拠袋・臨床）→courthouse 扉→毒の実る木（fruit of the poisonous tree）→一本の弱い環のある鎖（attenuation）→時間/介在/悪質性の天秤（3要素）→最高裁の大理石列柱＋空席（Scalia＝8席）→5-3 の投票→Thomas 多数の意見集→断ち切られる鎖→反対意見の2冊→ファイル/記録の壁（"cataloged"）→incentive の歯車（Kagan）→開いたままの扉** |
| 時間帯 | 午後の埃→冷灰→大理石 | **ユタの夜（plum を帯びた near-black・家/駐車場）→路肩の斜めのパトライト→冷灰の database/booking→冷たい大理石（ドクトリン核）→ENDING は夜明け前の薄明が開いた扉から入る（they may / it can now の余韻）** |
| 支配的出来事 | 罰金→現行犯逮捕→5-4 UPHELD | **理由なき停止（違法・州が譲歩）→ID 照会→先在する交通令状のヒット→令状での逮捕→捜索でメタンフェタミン（臨床）→ユタ州最高裁が排除→合衆国最高裁が破棄→排除法則 vs attenuation の例外→3要素（①時間=抑制寄り／②令状=決定的／③悪質性=過失止まり）→5-3 で証拠許容→Thomas 多数→Sotomayor/Kagan 反対（逐語）** |
| アクセント色 | civil-violet `#7A5CD0` | **somber-plum `#9C6BAA`** |
| ベース色 | 埃 `#14100C` + 冷灰 + 大理石 | **ユタの夜 plum `#0E0B12` + database 冷灰 `#1C1E24` + 大理石 `#33313A` + near-black `#0A0A0C`** |
| レンズ感 | — | **HOOK 象徴フラッシュモンタージュ（~2s cut・現在形・夜）／ACT1 最短・抑制（the stop）／ACT2 正対の転回（法理の問い・毒の木/鎖）／ACT3 正対対称・荘厳・最も遅い（the ruling・空席と反対）／ENDING 引き（pull-back・開いたままの扉）** |
| 画像保存先 | `H:\pd-media\assets\ai\atwater\` | **`H:\pd-media\assets\ai\strieff\`** |
| Remotion データ | `atwater_film.json` | **`strieff_film.json`** |
| Remotion コンポ | `Ep47Atwater` | **`Ep49Strieff`** |
| AE 作業ディレクトリ | `…/PD-2026-047-atwater/08_edit/ae_hero/` | **`…/PD-2026-049-strieff/08_edit/ae_hero/`** |

**素材被り禁止:** EP39〜48 と同一の factory clip / AI画像を1点も使わない。選定前に `episodes/PD-2026-039-*/`〜`…-048-*/` の `05_stock/stock_ledger*.json` を読み sha256 重複を除外（CODEX_A・BLOCKING）。

---

# 3. 尺と構成 — SPEC の値をそのまま使う

## 3.1 全区間タイムライン（★この表が唯一の正・秒は fps=30 から算出しフレーム直書き禁止・0〜720.6s 全区間＋8.0s teaser preroll）

**算出基準:** SPEC の `narration_seconds = 720.6`（マスター）を `strieff_film.json` の `narrationSeconds` に入れる。**手計算で上書きしない。** 各幕秒は SPEC の acts[].seconds（語数から機械算出）を planning アンカーとして使う。フレーム = `Math.round(30 × 秒)`。**hookSeconds=8.0** は BrandOpening の前に置く**無音コールドオープン teaser preroll**（フラッシュモンタージュ・ナレなし・BGM 低弦のみ）。

| # | ブロック | 役割 | 語数 | 幕秒 | 台本指定の沈黙 | 固定尺 | 開始f | 終了f |
|---|---|---|---|---|---|---|---|---|
| 0 | **HOOK TEASER**（無音 preroll） | `hook` | 0 | **8.00**（hookSeconds） | — | 8.00 | 0 | 240 |
| 1 | **HOOK** ナレ | `hook` | 195 | 65.7（SPEC） | **1.8**（"Hold on the man's back, mid-stride. No music." で保持） | — | 240 | 2211 |
| 2 | **BrandOpening** | `opening` | 0 | — | — | **3.50** | 2211 | 2316 |
| 3 | **OPENING** ナレ | `opening` | 177 | 59.6（SPEC） | — | — | 2316 | 4104 |
| 4 | **ACT_1** The stop | `body` | 389 | 131.0（SPEC・最短/最速） | — | — | 4104 | 8034 |
| 5 | **ACT_2** Exclusionary rule & the exception | `body` | 383 | 129.0（SPEC） | — | — | 8034 | 11904 |
| 6 | **ACT_3** The 5-3 & the dissent | `body` | 553 | 186.3（SPEC・最長・最も遅い） | — | — | 11904 | 17493 |
| 7 | **ENDING**（payoff→CTA） | `ending` | 359 | 120.9（SPEC） | — | — | 17493 | 21120 |
| 8 | **BrandEndcard** | `ending` | 0 | — | — | **9.00** | 21120 | 21390 |

> **フレーム列**は teaser(240f)/BrandOpening(105f)/BrandEndcard(270f) を実尺で挟み、幕秒を順に `round(30×秒)` で積んだ実装用アンカー。**幕秒積算 nominal 21390 と §3.1[3] の `caseFilmDurationInFrames` 出力 22233 の差 843f=28.1s は、narrationSeconds マスター 720.6 と発話幕秒合計 692.5 の差＝息継ぎ＋設計無音（SILENCE 1 = 1.8s）を内包する測定マスター。** film.json には 720.6 を入れる。CODEX_B は `strieff_film.json` の segment 順から再計算し一致を確認。
> **★台本 OPENING の指定＝「Gold BrandOpening resolves HERE, after the hook question」。** よって順序は **HOOK TEASER（無音）→ HOOK ナレ → BrandOpening（gold 解決）→ OPENING ナレ**。teaser は HOOK と同じ象徴（夜の家の扉・後ろ姿・パトライト・ID・令状ヒット）を ~1.3s の最速カットで無音提示し、そのあと同じ世界にナレが入る。

### 検算（CODEX_B は必ず自分で再計算して一致を確認）

```
[1] narrationSeconds = 720.6（SPEC マスター。手計算で上書きしない）
    ※ 発話ブロック HOOK..ENDING の幕秒合計 = 65.7+59.6+131.0+129.0+186.3+120.9 = 692.5s。
      SPEC マスター 720.6 との差 28.1s は、幕間の息継ぎ＋設計無音（SILENCE 1 = 1.8s）を内包した測定マスター。
    ※ mean_shot 検算: 720.6 / 226 = 3.189s ＝ SPEC mean_shot_seconds 3.19 一致（226カットは 720.6s 全域に張る）。

[2] 総尺 = hookSeconds 8.00 + BrandOpening(OPENING_SEC) 3.50 + narrationSeconds 720.6 + BrandEndcard(ENDCARD_SEC) 9.00
        = 741.1 秒 = 12:21.1

[3] caseFilmDurationInFrames(strieffFilm, 30) = 4項の実関数で算出:
      = round(hookSeconds×30) + round(OPENING_SEC×30) + ceil(narrationSeconds×30) + round(ENDCARD_SEC×30)
      = round(8.0×30)=240 + round(3.5×30)=105 + ceil(720.6×30)=ceil(21618.0)=21618 + round(9.0×30)=270
      = 22,233 フレーム
    ※ CODEX_B は strieff_film.json の hookSeconds/narrationSeconds（＋Bookends の OPENING_SEC/ENDCARD_SEC）から
      同関数で再計算し 22233 に一致することを assert する。

[4] runtime_band ≤ 750s の assert（BLOCKING）:
    総尺 = 741.1s = 12:21.1 は band 690–750（11.5–12.5分）の内側（上限 750s に対し 8.9s の余裕）    ✓ PASS
    ※ hookSeconds=8.0 を採用。narrationSeconds が実測で伸びたら再検算（BLOCKING）。
```
> **VO 実測で確定:** `measure_vo_wpm`（合格帯 168–190 wpm）でナレ実測。実測が SPEC マスターと乖離したら CODEX_B は `narrationSeconds` を実測値で更新（planning は 720.6・final は実測が権威）。190超は破棄・speed 0.95 で再発注（BLOCKING）。総尺 741.1s は ≤750 に対し余裕 8.9s しかない＝**実測が伸びたら endcard/teaser を削らず narration speed を確認**。

## 3.1b 秒×アニメーション・タイムライン（★全区間・各beat の start/end フレーム・移動量・easing・damping・stagger・Trail）

> **フレームは全て `f(sec)=Math.round(30×sec)`。等速線形ゼロ・opacity 単独ゼロ・静止フレームゼロ。** 下表は §3.2 の S01..S48 の主アニメを区間単位で示す（film-clock 秒＝teaser 0–8.0・以降ナレ・BrandOpening を 73.7–77.2 に挿入）。カット境界は `QUANT=f(0.5)=15f` グリッドにスナップ（§10.1）。still は Ken Burns（`scale 1.00→1.08`＋drift ±24px・`Easing.out(Easing.cubic)`）を全長。テキスト見出し/figures は `overflow:hidden` 親＋子 `translateY(110%→0)` の spring 切れ上がり（`damping:16,mass:1`・スタッガー `f(0.04)=2f/文字`）を基本形。★fast move（Trail 対象）は「Trail」列に明記。

| 区間(秒) | 開始f–終了f | シーン | 主アニメ（プロパティ・移動量） | easing / damping | stagger | Trail |
|---|---|---|---|---|---|---|
| 0.0–8.0 | 0–240 | HOOK TEASER（無音・~1.3s 最速カット） | 象徴フラッシュ（夜の家の扉→後ろ姿→パトライト→ID→令状ヒット画面）hard cut・各カット微 KB `scale 1.00→1.03` | `Easing.out(Easing.cubic)` | — | **✓**（パトライト/令状フラッシュ） |
| 8.0–22.0 | 240–660 | S01 ユタの夜・家の前の扉が開き暖光が漏れる（後ろ姿・HOOK 開幕） | still Ken Burns `scale 1.00→1.06` / drift +18px（plum の夜） | `Easing.out(Easing.cubic)` | — | — |
| 22.0–38.0 | 660–1140 | S02 後ろ姿が駐車場を横切る（i2v M01: 歩き・後ろ姿）＝SILENCE 1.8s を保持 | i2v native ＋ 追い足し `scale 1.00→1.03`・完全無音の画 | native + `Easing.inOut(Easing.sin)` 微動 | — | — |
| 38.0–52.0 | 1140–1560 | S03 駐車場の向こうの刑事の無人車（パトライトの plum 反射） | still `scale 1.00→1.07` / drift +20px | `Easing.out(Easing.cubic)` | — | — |
| 52.0–63.0 | 1560–1890 | S04 手渡される ID カード・無線マイク（理由なき停止） | still KB・`lowerthird` 開示 `AI-assisted visualization`（F-LT） | spring `damping:20,mass:1` | — | — |
| 63.0–73.7 | 1890–2211 | S05 画面に令状フラグが解決する（i2v M02: ライン→フラグ・**fast**） | i2v native ＋ フラグ点灯・数値見出しなし | native + cubic | — | **✓** |
| **73.7–77.2** | **2211–2316** | **BrandOpening 3.50**（Bookends・不変・gold 解決） | — | — | — | — |
| 77.2–100.0 | 2316–3000 | S06 最高裁の淡い大理石列柱（OPENING establishing・2016 に答えた court・factory） | factory 内在動き＋微 KB `scale 1.00→1.04` | `Easing.out(Easing.cubic)` | — | — |
| 100.0–120.0 | 3000–3600 | S07 排除法則＝違法に得た証拠が棚から外される象徴＋`kinetic` "THE WARRANT IN YOUR POCKET" | still push-in `scale 1.00→1.08`・kinetic 切れ上がり | spring `damping:16,mass:1` | 2f/文字 | figure reveal **✓** |
| 120.0–136.8 | 3600–4104 | S08 一本の弱い環のある鎖＋"ATTENUATION" の語が形になる | still KB・`lowerthird` "the attenuation doctrine"（F-LT） | spring `damping:20,mass:1` | — | — |
| 136.8–150.0 | 4104–4500 | S09 監視下の家（ACT1 幕頭）＋acttitle `THE STOP` | acttitle 切れ上がり・still KB・F-LT "SOUTH SALT LAKE CITY, UTAH · 2006"（N06） | spring `damping:16,mass:1` | 2f/文字 | figure reveal **✓** |
| 150.0–172.0 | 4500–5160 | S10 短時間の出入りを繰り返す訪問者（i2v M03: 後ろ姿の往来・**fast**）＋S11 Strieff が駐車場を横切る後ろ姿 | i2v swing ＋ still KB・`kinetic:emphasis` "NO GOOD REASON"（["NO"]） | native + spring | 2f/文字 | **✓** |
| 172.0–205.0 | 5160–6150 | S12 路肩のパトライト＝理由なき停止＋S13 手渡される ID | still KB・`lowerthird` "the stop was illegal — no reasonable suspicion"（C1・F-LT）・drift ±24px 交互 | spring `damping:18` | — | — |
| 205.0–232.0 | 6150–6960 | S14 無線でのディスパッチャ照会＋S15 令状ヒットの画面（i2v M05: フラグ点灯・**fast**） | still KB ＋ i2v native・`lowerthird` "an outstanding warrant — an old traffic matter"（S04・F-LT） | spring `damping:16` | — | **✓** |
| 232.0–255.0 | 6960–7650 | S16 令状での逮捕＝手錠（i2v M06: 手錠が閉じる・**fast**）＋S17 捜索に伴う小さな証拠袋（臨床） | i2v swing ＋ `mechanism:closingdoor`（逮捕の確定・F-MECH1） | native + spring | — | **✓** |
| 255.0–267.8 | 7650–8034 | S18 courthouse の扉＝ユタ州最高裁が排除→合衆国最高裁へ（ACT1 締め） | still KB・`lowerthird` "Utah Supreme Court suppressed → up to Washington"（S18・hedge 名なし） | `Easing.out(Easing.cubic)` | — | door **✓** |
| 267.8–285.0 | 8034–8550 | S19 毒の実る木（fruit of the poisonous tree・ACT2 幕頭）＋acttitle `THE EXCLUSIONARY RULE` | acttitle 切れ上がり・still KB・`lowerthird` "the exclusionary rule"（C2・F-LT） | spring `damping:16` | 2f/文字 | **✓** |
| 285.0–312.0 | 8550–9360 | S20 停止＝毒の木・薬物＝その実（compbars 対比）＋S21 例外が刻まれた規則書 | `compbars` [{"the illegal stop (the tree)",1},{"the drugs (the fruit)",1}]（F-CMP1）barX `scaleX 0→1` | spring `damping:18` origin left | — | — |
| 312.0–340.0 | 9360–10200 | S22 attenuation＝鎖が引き伸ばされ薄くなる（i2v M08: 鎖が伸びる・緩）＋S23 鎖が保つか断つか | i2v native ＋ `lowerthird` "attenuated: so thinned the connection barely holds"（C2） | native + `Easing.out(Easing.cubic)` | — | — |
| 340.0–367.0 | 10200–11010 | S24 factor① 時計＝数分（抑制寄り）＋S25 factor② 令状が鎖に割り込む（介在事情） | still KB・`timeline` events[{"①","time — favored suppression"},{"②","the warrant — intervening"},{"③","flagrancy — at most negligent"}]（F-TL1） | spring `damping:16` | — | tick **✓** |
| 367.0–396.8 | 11010–11904 | S26 factor③ 天秤が警察の行為を量る＋S27 3要素の三面天秤（ACT2 締め・stat 3） | `stat` value 3（label "the attenuation test · Brown v. Illinois"・N05）・count ease-out | `Easing.out(Easing.cubic)` | — | tick **✓** |
| 396.8–415.0 | 11904–12450 | S28 最高裁の列柱・正対（ACT3 幕頭・荘厳・最も遅い）＋acttitle `THE RULING` | acttitle 切れ上がり・still push-in `scale 1.00→1.08`・F-LT "Utah v. Strieff, 2016 · 579 U.S. 232"（N04） | spring `damping:16` | 2f/文字 | **✓** |
| 415.0–437.0 | 12450–13110 | S29 5-3 の投票が "five" で解決するバロット（votetally F-VOTE） | `votetally` majority 5 / dissent 3 settle（**"THE EVIDENCE STAYED · ADMISSIBLE" 対語・R-VOTE**）・drift +12px | `Easing.out(Easing.cubic)` | — | tick **✓** |
| 437.0–460.0 | 13110–13800 | S30 空席＝Scalia の椅子・8席（stat 8）＋S31 Thomas 多数の意見集 | still KB・`stat` value 8（label "an eight-justice court · Scalia's seat vacant"・N02）＋`lowerthird` "Justice Clarence Thomas — for the Court" | spring `damping:18` | — | tick **✓** |
| 460.0–487.0 | 13800–14610 | S32 factor① 時間で州が負けた（数分）＋S33 令状が浮上する（i2v M11: フラグ surfacing・決定的） | still KB ＋ i2v native・`lowerthird` "the warrant existed before the stop — the intervening circumstance"（C2） | spring `damping:16` | — | flag **✓** |
| 487.0–512.0 | 14610–15360 | S34 flagrancy＝せいぜい過失・悪質でない＋S35 鎖が断ち切られる（i2v M12: 環が壊れる・**fast**） | i2v swing ＋ `mechanism:faultsplit`（違法停止 ↔ 証拠を断つ線＝attenuation・F-MECH2） | native + `Easing.out(Easing.cubic)` | — | link break **✓** |
| 512.0–528.0 | 15360–15840 | S35b 因果が断たれる余韻＋`kinetic:emphasis` "THE WARRANT BROKE THE CHAIN"（["CHAIN"]） | kinetic 切れ上がり・still KB | spring `damping:16` | 2f/文字 | **✓** |
| 528.0–548.0 | 15840–16440 | S36 反対意見の2冊が開く（Sotomayor / Kagan）＋長ディゾルブ 10f | still push-in `scale 1.00→1.06`・`lowerthird` "the dissents" | `Easing.out(Easing.cubic)` | — | — |
| 548.0–566.0 | 16440–16980 | S37 記録/ファイルの壁＝"cataloged"（Sotomayor "carceral state" 逐語 quote F-QUOTE1） | `quote` maskslide（帰属 **Justice Sotomayor, dissenting**・N07） | `Easing.out(Easing.cubic)` | 2f/語 | — |
| 566.0–572.0 | 16980–17160 | S38 白人被告の一節＝誰の尊厳も（Sotomayor "anyone's dignity" 逐語 quote F-QUOTE2） | `quote` maskslide（帰属 **Justice Sotomayor, dissenting**・N08） | `Easing.out(Easing.cubic)` | 2f/語 | — |
| 572.0–583.1 | 17160–17493 | S39 incentive の歯車（Kagan 逐語 quote F-QUOTE3・mechanism gears）＋S40 3票、5票に届かず | `mechanism:gears`（違法停止を促す誘因・F-MECH3）＋`quote`（帰属 **Justice Kagan, dissenting**・N09） | spring `damping:16` + cubic | 2f/語 | **✓** |
| 583.1–605.0 | 17493–18150 | S41 駐車場に戻る・後ろ姿（ENDING・payoff の起点）＋S42 画面に再び令状フラグ | still KB・`kinetic:emphasis` "THE EVIDENCE STAYED"（["STAYED"]） | spring `damping:16` | 2f/文字 | **✓** |
| 605.0–635.0 | 18150–19050 | S43 消えなかった不正＝薄れる違法停止＋S44 多くの人が持つ小さな令状（多数のフラグ） | still KB・`lowerthird` "the illegal stop becomes almost free"（C1） | `Easing.out(Easing.cubic)` | — | — |
| 635.0–665.0 | 19050–19950 | S45 一本だけ薄くなった環の鎖（i2v M15: 環が痩せる・緩）＋S46 弱まった第4修正 | i2v native ＋ `lowerthird` "the exclusionary rule: narrowed, not abolished"（C2） | native + `Easing.out(Easing.cubic)` | — | — |
| 665.0–695.0 | 19950–20850 | S47 開いたままの扉（i2v M16: 扉が保持・plum の薄明）＋`lowerthird` "a door held open" | i2v native ＋ slow `scale 1.00→1.02`・`lowerthird` "the dissent lost — three votes, not five"（C3） | native + `Easing.out(Easing.cubic)` | — | door **✓** |
| 695.0–704.0 | 20850–21120相当 | S48 駐車場の後ろ姿へ pull-back（i2v M16 再掲）→CTA→BrandEndcard 21120 開始 | i2v native ＋ slow pull-back・字幕のみ | native + `Easing.out(Easing.cubic)` | — | — |

> **★背面レイヤーは常に4層以上動く（§8.1）。** 上表の各 0.5s 境界で「動いている要素」が最低1つある（静止区間ゼロ）。Trail 対象（fast move）は **TEASER のパトライト/令状フラッシュ / S05 令状フラグ / S09 acttitle / S10 訪問者の往来 / S15 令状ヒット / S16 手錠 closingdoor / S18 courthouse 扉 / S29 votetally / S30–S31 stat 桁 / S33 令状 surfacing / S35 鎖 faultsplit / S35b・S41 kinetic 切れ上がり / S39 gears**。**S01/S06/S28 の荘厳 push-in・S02（後ろ姿の緩い歩き）・S22/S45 の緩い i2v・S47/S48 の扉/pull-back・Ken Burns には Trail をかけない**（無駄な残像・扇情を避ける・C5）。

## 3.2 シーン→幕の割当（★SPEC の S01..S48 を固定・別番号を発明しない・48シーン）

各シーンは narrative beat。226カットを 48シーンに分散（平均 4.71カット/シーン）。`primary` は各シーンの主素材（still=SDXL 各1枚 / factory=実写 / motion=i2v）。ambient/繋ぎは factory を各シーンに撒く（§5.1）。**象徴のみ・6制約順守・Strieff/Fackrell 非人物化・薬物は臨床最小限。絵コンテ級の記述は §9。**

> **★2つの `Sxx` 名前空間は別物（取り違え禁止）:** 本節の **narrative シーンは `S01..S48`**（この表の絵コンテ）。一方 **still 資産 ID は `S01..S85`**（CODEX_A・1プロンプト=1枚で48シーンに85枚を配分）。同じ `Sxx` 表記でも DESIGN §3.2/§9 の Sid（narrative）と CODEX_A/asset_manifest の scene_id（still 資産 ID）は指すものが異なる。横断参照時は「どちらの空間か」を明示し、cross-map しない。

| Sid | 幕 | 内容（象徴・6制約） | primary |
|---|---|---|---|
| S01 | HOOK | ユタの夜・家の前の扉が開き暖光が漏れる・後ろ姿の人影が出てくる（顔なし・R2） | still |
| S02 | HOOK | 後ろ姿が駐車場を横切る（i2v: 歩き・後ろ姿）＝SILENCE 1.8s を保持 | **motion** |
| S03 | HOOK | 駐車場の向こうに停まる刑事の無人車・plum のパトライトの反射（理由なき監視） | still |
| S04 | HOOK | 手渡される ID カードと無線マイク（照会の始まり・顔なし） | still |
| S05 | HOOK | database の画面に令状フラグが解決する（i2v: ライン→フラグ・fast） | **motion** |
| S06 | OPENING | 最高裁の淡い大理石列柱＝2016 に答えた court（正対・荘厳・遠い・factory establishing） | factory |
| S07 | OPENING | 排除法則＝違法に得た証拠が棚/証拠台から外される象徴（本来は捨てられる） | still |
| S08 | OPENING | 一本の弱い環のある鎖＋"ATTENUATION" の語が形になる（重い名前の narrow な考え） | still |
| S09 | ACT1 | 通報で断続監視される家（ACT1 幕頭・夜・plum） | still |
| S10 | ACT1 | 短時間の出入りを繰り返す訪問者の後ろ姿の往来（i2v: 往来・fast・顔なし） | **motion** |
| S11 | ACT1 | Edward Strieff が駐車場を横切る後ろ姿（R2・顔なし・象徴のみ） | still |
| S12 | ACT1 | 路肩に差すパトライト＝理由なき停止（違法・州が譲歩） | still |
| S13 | ACT1 | 手渡される ID カード（照会される私人・顔なし） | still |
| S14 | ACT1 | 無線でのディスパッチャ照会（冷灰の database・institutional） | still |
| S15 | ACT1 | 令状ヒットの画面＝古い小さな交通令状フラグ（i2v: フラグ点灯・fast） | **motion** |
| S16 | ACT1 | 令状での逮捕＝閉じる手錠（i2v: 手錠が閉じる・fast・身体を描かず象徴） | **motion** |
| S17 | ACT1 | 捜索に伴う閉じた小さな証拠袋（臨床最小限・薬物名なし・非扇情） | still |
| S18 | ACT1 | courthouse の扉＝ユタ州最高裁が排除→合衆国最高裁へ（ACT1 締め） | still |
| S19 | ACT2 | 毒の実る木（fruit of the poisonous tree・ACT2 幕頭・lowerthird motif） | still |
| S20 | ACT2 | 停止＝毒の木／薬物＝その実（compbars 対比・判読不能） | still |
| S21 | ACT2 | 例外が刻まれた古い規則書＝排除法則は絶対ではない（判読不能） | still |
| S22 | ACT2 | attenuation＝鎖が引き伸ばされ薄くなる（i2v: 鎖が伸びる・緩） | **motion** |
| S23 | ACT2 | 鎖が保つか断つか＝本件の争点（still・判読不能） | still |
| S24 | ACT2 | factor① 時計＝数分（抑制寄り・時間的近接） | still |
| S25 | ACT2 | factor② 令状が鎖に割り込む（介在事情＝先在する有効な令状） | still |
| S26 | ACT2 | factor③ 警察の行為を量る天秤（目的/悪質性） | still |
| S27 | ACT2 | 3要素の三面天秤＝attenuation test（ACT2 締め・stat 3） | still |
| S28 | ACT3 | 最高裁の列柱・正対（ACT3 幕頭・荘厳・最も遅い・factory establishing） | factory |
| S29 | ACT3 | 5-3 の投票が "five" で解決するバロット（votetally F-VOTE・**ADMISSIBLE 対語**） | still |
| S30 | ACT3 | 空席＝Scalia の椅子・8席のベンチ（8名構成） | still |
| S31 | ACT3 | Thomas 多数の開いた意見集（判読不能・for the Court） | still |
| S32 | ACT3 | factor① 時間で州が負けた（数分・抑制寄り・判読不能） | still |
| S33 | ACT3 | 令状が浮上する＝停止の前から存在した介在事情（i2v: フラグ surfacing・決定的） | **motion** |
| S34 | ACT3 | flagrancy＝せいぜい過失・悪質でない（天秤が州寄りに・判読不能） | still |
| S35 | ACT3 | 鎖が断ち切られる＝attenuation（i2v: 環が壊れる・fast・因果の遮断） | **motion** |
| S36 | ACT3 | 反対意見の2冊が開く（Sotomayor / Kagan・判読不能） | still |
| S37 | ACT3 | 記録/ファイルの壁＝"cataloged"（Sotomayor "carceral state" 逐語・帰属 dissenting） | still |
| S38 | ACT3 | 白人被告の一節＝誰の尊厳も侵されうる（Sotomayor "anyone's dignity" 逐語・帰属 dissenting） | still |
| S39 | ACT3 | incentive の歯車＝違法停止を促す誘因（Kagan 逐語・帰属 dissenting・mechanism gears） | still |
| S40 | ACT3 | 3票が並ぶが5票に届かない象徴（three votes, not five・負けた側・判読不能） | still |
| S41 | ENDING | 駐車場に戻る後ろ姿＝あなたの通りと午後（現在形・payoff 起点） | still |
| S42 | ENDING | database の画面に再び令状フラグが解決する（あなたの名前） | still |
| S43 | ENDING | 消えなかった不正＝薄れる違法停止（wrong が問題でなくなった） | still |
| S44 | ENDING | 多くの人が持つ小さな令状＝多数のフラグ（未払い罰金/古い切符） | still |
| S45 | ENDING | 一本だけ薄くなった環の鎖（i2v: 環が痩せる・緩＝almost free） | **motion** |
| S46 | ENDING | 弱まった第4修正＝規則を破っても勝てる断層線（判読不能） | still |
| S47 | ENDING | 開いたままの扉＝違法停止が令状に救われる（i2v: 扉が保持・plum の薄明） | **motion** |
| S48 | ENDING | 駐車場の後ろ姿へ slow pull-back（i2v: 引き・payoff・CTA） | **motion** |

**source 集計（scene-primary）:** motion-primary **11**（S02 S05 S10 S15 S16 S22 S33 S35 S45 S47 S48）／factory-primary **2**（S06 S28）／残り still-primary **35**。**scene-primary はカット全体の一部**で、残りは §5.1 の配分に従い CODEX_B の shotlist が 226 カット（still 101 / factory 93 / motion 32）へ機械展開する。**この表のシーン数・番号は固定（S01..S48）。**

---

# 4. 音の4層設計（ナレ / BGM / SFX / 環境音）

## 4.1 ラウドネス・voice（確定値・EP41〜48 と同一運用）

| 項目 | 確定値 |
|---|---|
| 統合ラウドネス（完成 mp4） | **-14.0 LUFS**（許容 -16〜-12） |
| True peak | **≤ -1.0 dBTP** |
| ナレ（VO）単体 | -18.0 LUFS 目標 |
| BGM ベッド（VO下・ダッキング後） | **-22.0 LUFS**（無音まで落とさない） |
| BGM ベッド（VO無し区間） | -17.0 LUFS |
| 環境音ベッド | -30.0 LUFS |
| ダッキング | リダクション 5.0 dB / attack 120ms / release 450ms |
| **VOICE_ID** | ElevenLabs `nPczCjzI2devNBz1zQrb` / model `eleven_multilingual_v2` / stability **0.35** / similarity_boost **0.80** / style **0** / speaker_boost **on** / **speed 1.0（明示）** |
| VO実測合格帯 | `measure_vo_wpm` で **168.0–190.0 wpm**。190超は破棄・speed 0.95 で再発注（BLOCKING） |

## 4.2 【SILENCE 1】の実装（★デジタル無音にしない・`bgm_present` を落とす）

台本の `【SILENCE 1 — 1.8s】` は**ナレの沈黙であって音の沈黙**（台本指定「Hold on the man's back, mid-stride. No music.」＝完全無音）。EP49 は明示指定が1箇所（HOOK 内）。

| 位置 | 秒 | 対応画 | 鳴らすもの |
|---|---|---|---|
| HOOK（"He walks over anyway and tells him to stop." の直後→後ろ姿を保持） | **1.8** | S02（後ろ姿が駐車場を横切る・mid-stride） | BGM mute。**完全無音**（room tone も置かない・台本指定「No music」） |

**最長無音候補 1.8秒 << 25秒** ✓ `bgm_present` PASS。加えて **HOOK TEASER preroll（0–8.0s）は BGM 低弦のみ**（ナレなしだがデジタル無音にはしない）。

## 4.3 章ごとの BGM（1章1トラック・`build_strieff_bgm_real.py`＝EP43 系を strieff 用に複製・film_offset 適用・OFF は実測。ブリーフ§5 OFF=11.5）

| 区間 | 性格 | 楽器 |
|---|---|---|
| HOOK TEASER / HOOK | 低弦の不解決・夜の緊張・単音が刺す（家の扉・後ろ姿・パトライト・令状フラグ） | 低弦+単音メタル |
| OPENING | ブランドスティンガー（`BrandOpening` 付属） | — |
| ACT1 | 最短・現在形・抑制。刻みは疎で近い（the stop） | 低弦+疎パーカッション |
| ACT2 | 転回。法理の冷たい正対（毒の木・鎖・3要素） | ピアノ+弦 |
| ACT3 | 法の荘厳・大理石。**最も遅い**。5-3 の重さと空席・反対の緊張 | 低弦+弦サステイン |
| ENDING | 解決しない和音 →「a door held open」でだけ薄明の暖色に開く（it can now の余韻） | ピアノ+弦 |
| ENDCARD | ブランドED（`BrandEndcard` 付属） | — |

## 4.4 SFX（非扇情・C5）

| 種別 | 位置 | 音 |
|---|---|---|
| night ambient | S01/S41 | 夜の駐車場の遠い風・遠い車・-30 LUFS |
| footsteps | S02/S11 | 舗装を歩く控えめな足音・-26 LUFS（沈黙区間は完全無音のため置かない） |
| patrol light | S03/S12/TEASER | パトライトの回転の低いハム・-24 LUFS（サイレン/悲鳴なし・非扇情・C5） |
| radio / dispatch | S04/S14 | 無線のスケルチ・低い交信・-24 LUFS |
| database hit | S05/S15/S42 | 画面のフラグ点灯の電子音・-22 LUFS |
| handcuffs | S16 | 手錠のラチェット音・-18 LUFS（身体音/悲鳴なし・非扇情） |
| chain | S22/S35/S45 | 鎖の低い金属音・S35 で環が断つ一撃・-20 LUFS |
| marble / columns | S06/S28/S30 | 大理石ホールの広いリバーブ・-30 LUFS |
| ballot tick | S29 votetally/stat の桁変化 | 微細クリック・-24 LUFS |
| door open | S47/S48 | 開いたままの扉の軋み・薄明の外気・-18 LUFS |
| impact | AE v01/q01 の着地 | 低域インパクト・-12 LUFS |
| room tone | 全編ベッド（夜・database 冷灰・大理石反響） | 広いリバーブ・-30 LUFS（**SILENCE 1 は完全無音**） |

---

# 5. ビジュアル — 素材積算（★紙芝居回避＝factory実写を必ず混ぜる・1シーン1枚）

## 5.1 素材の積算（★SPEC の値をそのまま満たす配分）

```
[0] 絵が必要な区間 = narrationSeconds 720.6（BrandOpening/Endcard/teaser は別レイヤー）
[1] 総カット = 226（SPEC）    720.6 / 226 = 3.189秒/カット  ✓ mean_shot 3.19（≤6.0）
[2] 素材内訳（★SPEC の distinct/cuts をそのまま・1シーン1枚）
    still（SDXL）    85 distinct → 101 カット（16枚が2回・69枚が1回・mean 1.19・cap 2）★各1枚生成
    factory 実写     93 distinct →  93 カット（各1回・cap 1）
    i2v モーション    16 distinct →  32 カット（各2回・cap 2）
    -----------------------------------------------
    distinct 合計   194          → 226 カット
[3] first-use share = 194 / 226 = 0.8584   ✓ ≥0.70（SPEC 一致）
[4] footage_diversity distinct/total = 0.8584   ✓ ≥0.40
[5] 最大使用回数: still 2 / factory 1 / motion 2   ✓ 各 cap 内
[6] 静止画占有率（★紙芝居ゲート）: still-cut 101 / 226 = 0.4469 = 44.69%   ✓ ≤45%（余裕 0.31%pt）
[7] motion coverage: (factory 93 + i2v 32) / 226 = 125/226 = 0.5531   ✓ ≥0.45
[8] factory 下限 = 720.6/30 = 24.0 → ≥24本。設計値 93本   ✓
```
> **[6] の余裕は 0.31%pt。still-cut を1つ増やすと 45% に近づく。still-cut は 101 で固定**（16枚だけ2回・残り69枚1回）。QC で still が 85枚を割ったら §9 の**追加は同一シーンの別プロンプト（新規 distinct）**で回復させ、**cut 数は増やさない**。**still を増やして factory を削るな。factory 93 が still-share≤0.45 を守る下限。**

## 5.2 SDXL と実写在庫の振り分け

- **SDXL（still 85・各1枚）= この事件にしか無い固有物**: 夜の家の扉/後ろ姿・駐車場・刑事の車/パトライト・ID/無線・令状ヒットの画面・手錠・小さな証拠袋・courthouse 扉・毒の実る木・弱い環の鎖・時計/令状/天秤（3要素）・最高裁列柱/空席の椅子・5-3 バロット・Thomas/反対の意見集・断ち切られる鎖・ファイルの壁（cataloged）・incentive の歯車・多数の令状フラグ・開いたままの扉。
- **factory 実写 93 = どこにでもある周辺**: 夜のユタの街/駐車場 ambient・courthouse 外観・最高裁列柱・大理石テクスチャ・冷たい廊下・database ルームの institutional・薄明の街・ambient 繋ぎ。

## 5.3 SDXL 生成量（★バリエーション0・variants 禁止）

- `ai_prompts.v001.md` = **body 85行の固有プロンプト**（still 各1枚）＋ i2v 種 **16行** ＝ **計101エントリ**（`--only S01` の `shots=` は 101）。`generate_sdxl_4k.py PD-2026-049-strieff`（**`--variants 1` または指定なし**）。**`--variants 3` を書かない。**
- i2v-source = **16枚**（動きが意味を持つ絵の固有プロンプト・各1シード）。CODEX_A が Wan 2.2 A14B → RIFE 48fps で 16本生成。
- **総生成 = still 85 + i2v seed 16 = 101枚（各1回）。** factory 93 は生成せず在庫選抜。
- プロンプト実体（85本）・i2v リスト（16）・factory 選定（93）は **CODEX_A** の担当（本書 §9 は絵コンテ級の記述と共通スタイル/ネガティブの契約のみ）。

## 5.4 factory のファイル名を信じない（★必須工程・CODEX_A・BLOCKING）

> EP36: `city_surveillance_camera_dome` が実際は大聖堂。EP38: 牛が `documents_on_desk`。ラベルは検索語の記録であって中身の保証ではない。

選定した **93本すべて**を `scripts/build_footage_contact_sheet.py --ep PD-2026-049-strieff --media video --dir <factory staging>` で1本1フレームのラベル付きコンタクトシートにし**全点目視**。subtype と食い違う本は差し替える。`select_strieff_factory.py --verify-no-prior-overlap` で EP39〜48 の sha256 被りゼロを確認。

## 5.5 共通スタイル接尾（各 SDXL プロンプト末尾に必ず付ける・`[STYLE]`・CODEX_A と同一）

```
, cinematic still, somber documentary grade, a plum-tinted Utah night of a front door and a parking lot, cold grey institutional database and booking interiors, pale marble Supreme-Court colonnade in fluorescent and thin dawn light, a single somber-plum accent as the one cool note, restrained and dignified symbolism, telephoto compression and frontal composition, shallow depth of field, ultra-detailed, photoreal, 4K, 16:9, fine film grain, no text, no watermark, no logo, symbolic still-life, no people, no visible face, backs and hands and objects only
```
> EP39〜48 との分離: 接尾に `electric blue`（EP39）・`midday suburban`（EP40）・`sodium prison corridor`（EP41）・`warrant-blue`（EP42）・`porch-amber`/`ambulance`（EP43）・`teal-green hospital`（EP44）・`crimson overdue`（EP45）・`forest-green`（EP46）・`civil-violet`（EP47）を**1語も含めない**。EP49 の唯一の差し色は **somber-plum `#9C6BAA`**。

## 5.6 共通ネガティブ（各 SDXL プロンプトの `Avoid:` に必ず付ける・`[NEG]`・CODEX_A と同一）

```
text, words, letters, numbers, captions, watermark, logo, readable document, legible warrant, legible ID, legible license number, legible date, real celebrity, recognizable real person, identifiable face, portrait, mugshot, likeness of a specific person, human face, front-facing person, Edward Strieff, nude, bare skin, drug use, needle, smoking, pipe, powder, overdose, addict, crime scene, blood, gore, violence, weapon, gun, sensational distress, poverty porn, cartoon, illustration, anime, 3d render, low quality, blurry, jpeg artifacts, deformed, extra limbs, barred cell, steel cellblock, sodium prison corridor, electric blue, teal-green hospital corridor, porch amber, ambulance, crimson overdue notice, forest-green, civil-violet
```
> ネガティブにも **制約違反語（"the stop was legal", "exclusionary rule abolished", "we are all harmed", 薬物扇情語等）を書かない**（§1.3）。会社/機関ロゴや読める書類が必要な絵は「blurred into an unreadable smear」で判読不能に。判例番号・日付・票数・Fackrell 名を画に描かない（AE/figures＝B の担当）。**手錠・database・booking は institutional で非扇情に**（鉄格子/独房/暴力を描かない・C5）。**Strieff は後ろ姿/手元/象徴のみ**（人体/顔を描かない）。**薬物は閉じた小さな証拠袋の象徴のみ**（粉/器具/使用を描かない・C5）。

## 5.7 AI開示（強め・毎回・R1）

AI 生成の still・i2v が画面に出ている間、常時右下に **`AI-assisted visualization`**。Oswald 20px / `#C8CDD6` / opacity 70% / 位置 `[W-32, H-28]`。字幕帯と縦 56px 以上離す。概要欄1行: `Some visuals in this film are AI-assisted reconstructions, not photographs of the actual events.`（＋あなたの州の「an illegal stop plus an outstanding warrant」がどう扱われるか＝排除法則と attenuation 例外を確認する中立の1行）。

## 5.8 ★A↔B 境界契約（asset_manifest スキーマ・EP39〜48 の不整合を最初から潰す）

- **接続点は `episodes/PD-2026-049-strieff/05_visuals/asset_manifest.v001.json` ただ1ファイル**。A(producer)＝CODEX_A が書き、B(consumer/validator)＝CODEX_B が読む。**counts と role enum を A/B で一字一致**させる。
- **スキーマ版:** `strieff_assets.v1`（固定文字列）。
- **マニフェスト配列（★A/B 同一）:** `stills` / `motion` / `factory` / `overlay` の4配列。**★全エントリを記載**（stills85＋factory93＋motion16＋overlay12・public_path 必須＝EP45事故回避）。
- **counts オブジェクト（★このキー・値で固定・A/B 一字一致）:** `{ "still_body": 85, "still_i2v_source": 16, "motion": 16, "factory": 93, "overlay": 12 }`。cuts 展開は still 101 / factory 93 / motion 32。
- **`stills[].role` enum（★この3値のみ・A/B 同一・`thumb`/`still_thumb` を作らない）:** `body` / `i2v_source` / `reject`。asset_id は body `^STR-S\d{2}$`（S01..S85）/ i2v種 `^STR-MS\d{2}$` / motion `^STR-M\d{2}$`。
- **サムネは `role="body"` かつ `also_thumb=true` の body still ちょうど6枚**（別 role を作らない・追加生成しない）。**候補集合（★still 資産 ID 空間・A↔B 契約点）:** **`{S01, S05, S15, S30, S37, S47}`**（夜の扉・令状フラグ・令状ヒット・空席・ファイルの壁・開いたままの扉）。A・B は同一6 asset ID に `also_thumb:true` を立てる。
- **overlay 枚数も A/B 一致**（合成レイヤー・distinct 素材に数えない）。本書設計値 **overlay: 12**（particle/light/vfx）。CODEX_A/CODEX_B は共に overlay=12 で書く。
- CODEX_A は manifest を書いた直後 `build_strieff_asset_manifest.py --verify`（複製）で counts / role / also_thumb / overlay を突き合わせ、**A の値と B の期待が一字一致**であることを確認（不一致は BLOCKING）。**`also_thumb==true` の scene_id 集合が `{S01,S05,S15,S30,S37,S47}` で A↔B 同一**であることも検査する。

---

# 6. Remotion MGビート（FigureBeats）— ★密度下限 31 は必ずここで満たす・dochighlight 不使用

## 6.1 密度の設計（`strieff_film.json` の `figures[]`）

`check_motion_density`: 3つを AND。**body-minutes = narrationSeconds/60 = 720.6/60 = 12.01**。

| 指標 | floor | EP49 設計値 |
|---|---|---|
| density | ≥2.5/min | figures **34 beats / 12.01 = 2.83/min** ✓（SPEC beats_floor 31 に +3） |
| coverage | ≥0.25 | 34 beats × 平均 5.6秒 = 190.4秒 / 720.6 = **0.264** ✓ |
| variety | ≥3 distinct forms | **9種**（下記） ✓ |

> **AE の 6枠は film.json に入れない**（composite 後に焼くため gate 非カウント）。**density は Remotion 側 34 beats だけで 31 を超える。** coverage が floor 0.25 に一番近いので figures の dur は 5.2–6.0s を基本にする。

## 6.2 `figures[]` の種類配分（★kind は全部小文字・同一 kind を連続させない・★dochighlight 不使用・★実 FigureBeats.tsx union で全数検証済）

**★実 union（`remotion/src/components/FigureBeats.tsx` の `FigureSpec`）で検証済の使用 kind（全小文字）:** `acttitle` `lowerthird` `kinetic` `stat` `compbars` `quote` `timeline` `votetally` `mechanism`。**いずれも union に実在**（`timeline`→events[]・`compbars`→items[]・`quote`→quote+attribution・`votetally`→majority+dissent・`mechanism`→{closingdoor,gears,faultsplit}・`stat`→value/prefix/label・`kinetic`→lines[]+emphasisWords[]・`acttitle`→title+kicker+index・`lowerthird`→primary+secondary）。**大文字 kind は無音描画になる。** **★`dochighlight` を1件も入れない（R-DOCHL・grep 0）。令状/画面/書類は `lowerthird` の説明テキストで表す。** `comparebars` は非実在→`compbars` が正。

| kind（小文字・union実在） | 枠数 | EP49 での用途（6制約適用） |
|---|---|---|
| `acttitle` | 3 | ACT1「THE STOP」/ ACT2「THE EXCLUSIONARY RULE」/ ACT3「THE RULING」 |
| `lowerthird` | 13 | 開示 `AI-assisted visualization`（HOOK/ENDING 2回）／"SOUTH SALT LAKE CITY, UTAH · 2006"（N06）／"the attenuation doctrine"／"the stop was illegal — no reasonable suspicion"（C1）／"an outstanding warrant — an old traffic matter"／"the exclusionary rule"（C2）／"Utah v. Strieff, 2016 · 579 U.S. 232"（N04）／"Justice Clarence Thomas — for the Court"／"the warrant existed before the stop — the intervening circumstance"（C2）／"the exclusionary rule: narrowed, not abolished"（C2）／"the dissent lost — three votes, not five"（C3） |
| `kinetic` | 5（うち emphasis 3） | 「THE WARRANT IN YOUR POCKET」／「NO GOOD REASON」(["NO"]・C1)／「THE WARRANT BROKE THE CHAIN」(["CHAIN"]・C2)／「THE EVIDENCE STAYED」(["STAYED"]・C1)／「THREE VOTES, NOT FIVE」(["NOT"]・C3)。**emphasisWords は1–2語＝文字切れ回避** |
| `stat` | 2 | **3**（N05・label "the attenuation test · Brown v. Illinois"）／**8**（N02・label "an eight-justice court · Scalia's seat vacant"・topLabel "the term Strieff was decided"） |
| `compbars` | 2 | fruit-of-the-poisonous-tree 対比 [{"the illegal stop (the tree)",1},{"the drugs (the fruit)",1}]（**F-CMP1**・C2 中立）／attenuation 対比 [{"the chain holds → evidence out",1},{"the warrant snaps it → evidence in",1}]（**F-CMP2**・C1/C2 中立） |
| `quote` | 3 | ①Sotomayor "carceral state"（**帰属 Justice Sotomayor, dissenting**・F-QUOTE1・N07）②Sotomayor "anyone's dignity"（**帰属 Justice Sotomayor, dissenting**・F-QUOTE2・N08）③Kagan incentive（**帰属 Justice Kagan, dissenting**・F-QUOTE3・N09）。**要約を引用符に入れない・facts_lock で逐語確認・反対を Court に帰属させない・"we are all harmed" は使わない** |
| `timeline` | 2 | ①3要素 events[{"①","time — favored suppression"},{"②","the warrant — intervening (decisive)"},{"③","flagrancy — at most negligent"}]（**F-TL1**・year欄は丸数字ラベル）②手続 events[{"2006","the illegal stop"},{"—","Utah Supreme Court suppressed"},{"2016","U.S. Supreme Court: evidence admissible"}]（**F-TL2**・S18） |
| `votetally` | 1 | **5-3**（Thomas 多数 5／反対 3・**F-VOTE**・必ず "THE EVIDENCE STAYED / ADMISSIBLE" の対語を伴う・R-VOTE・C3 中立・label 経由） |
| `mechanism` | 3 | `closingdoor`（令状での逮捕の確定・ACT1）／`faultsplit`（鎖が断たれる＝attenuation・違法停止↔証拠の線・ACT3）／`gears`（incentive の機械＝Kagan の誘因・ACT3） |
| **合計** | **34** | variety = **9 figure-kinds** ✓ ≥3 |

> **★`dochighlight` を1件も置かない（R-DOCHL）。** `graphics[]=[]`（空配列）。density は `figures+graphics+heroCuts` を合算するので figures 34 だけで floor 31 に +3。

## 6.3 配置方針（34本・§1.4 台帳の値だけを焼く・kind を分散・6制約順守・dochighlight 0件・CODEX_B と一致）

- **HOOK/OPENING（3）:** `lowerthird`（`AI-assisted visualization` 開示）/ `kinetic`（"THE WARRANT IN YOUR POCKET"）/ `lowerthird`（"the attenuation doctrine"）
- **ACT1（6）:** `acttitle`（THE STOP）/ `lowerthird`（"SOUTH SALT LAKE CITY, UTAH · 2006"・N06）/ `kinetic:emphasis`（"NO GOOD REASON"・["NO"]・C1）/ `lowerthird`（"the stop was illegal — no reasonable suspicion"・C1）/ `lowerthird`（"an outstanding warrant — an old traffic matter"）/ `mechanism:closingdoor`（令状での逮捕）
- **ACT2（8）:** `acttitle`（THE EXCLUSIONARY RULE）/ `lowerthird`（"the exclusionary rule"・C2）/ `compbars`（**F-CMP1** tree↔fruit・C2 中立）/ `compbars`（**F-CMP2** chain holds↔warrant snaps・C1/C2 中立）※間に別 kind を挟む/ `lowerthird`（"attenuated: so thinned the connection barely holds"・C2）/ `timeline`（**F-TL1** 3要素）/ `stat`（**3**・N05）/ `kinetic`（"FRUIT OF THE POISONOUS TREE"）
- **ACT3（12）:** `acttitle`（THE RULING）/ `lowerthird`（"Utah v. Strieff, 2016 · 579 U.S. 232"・N04）/ `votetally`（**F-VOTE 5-3**・"THE EVIDENCE STAYED · ADMISSIBLE"・R-VOTE）/ `stat`（**8**・N02）/ `lowerthird`（"Justice Clarence Thomas — for the Court"）/ `lowerthird`（"the warrant existed before the stop — the intervening circumstance"・C2）/ `mechanism:faultsplit`（鎖が断たれる＝attenuation）/ `kinetic:emphasis`（"THE WARRANT BROKE THE CHAIN"・["CHAIN"]・C2）/ `quote`（Sotomayor "carceral state" → "Justice Sotomayor, dissenting"・**F-QUOTE1**）/ `quote`（Sotomayor "anyone's dignity" → "Justice Sotomayor, dissenting"・**F-QUOTE2**）/ `mechanism:gears`（Kagan incentive の機械）/ `quote`（Kagan incentive → "Justice Kagan, dissenting"・**F-QUOTE3**）
- **ENDING（5）:** `kinetic:emphasis`（"THE EVIDENCE STAYED"・["STAYED"]・C1）/ `timeline`（**F-TL2** 2006→2016 手続・S18）/ `lowerthird`（"the exclusionary rule: narrowed, not abolished"・C2）/ `kinetic:emphasis`（"THREE VOTES, NOT FIVE"・["NOT"]・C3）/ `lowerthird`（開示 `AI-assisted visualization` 再掲）

## 6.4 配置ルール

1. **AE の 6区間（§7）と1秒でも重ならない**（`validate_strieff_beats.py`＝validate_caniglia_beats.py を複製・両方突き合わせ）。
2. 幕あたり配分: HOOK/OPENING=3 / ACT1=6 / ACT2=8 / ACT3=12 / ENDING=5（ACT3 が最長 186.3s なので厚め）。
3. **同じ kind を連続させない**（`compbars` の直後に `compbars` を置かない・`quote`×3 の間に `mechanism`/`lowerthird` を挟む）。
4. 1枠 **5.2–6.0秒**（coverage 0.264 を守る）。
5. ACT3 の説明区間に `votetally`＋`quote`×3＋`mechanism`×2＋`stat`＋`lowerthird` を分散し 20秒超の平坦区間をゼロに。
6. `quote` は**逐語のみ**（要約を引用符に入れない・R-QUOTE）。**Sotomayor / Kagan＝dissenting** を厳格帰属。**"we are all harmed" を使わない**（S15）。
7. `figures[].*text*`/`lines[]`/`label`/`quote`/`primary`/`secondary` は `facts_lock` 検査対象（「the stop was legal / exclusionary rule abolished / 6-3 / we are all harmed」・Fackrell 名・台帳外数値・**dochighlight** を出さない）。
8. **5-3 を焼く votetally は同一 payload に "THE EVIDENCE STAYED / ADMISSIBLE / 8 JUSTICES" を必ず持つ（R-VOTE）。** 反対 quote payload は必ず attribution "Justice Sotomayor/Kagan, dissenting"（R-QUOTE）。

## 6.5 密度の最終検算

```
Remotion figures 34（film.json 内・graphics 空）
  density  = 34 / 12.01 = 2.83/min   ✓ ≥2.5（SPEC beats_floor 31 → 34 で +3）
  coverage = 190.4s / 720.6 = 0.264    ✓ ≥0.25
  variety  = 9 forms                   ✓ ≥3
  dochighlight count = 0               ✓ R-DOCHL（grep 0）
  ★全 kind が実 FigureBeats.tsx union に実在（acttitle/lowerthird/kinetic/stat/compbars/quote/timeline/votetally/mechanism）
AE hero 6枠は composite 後・gate 非カウント（上乗せの決め所）
```

---

# 7. After Effects ヒーロービート（6枠）— ★AEカードは密度に数えられない

## 7.1 大原則（★EP39/40 の致命傷を回避）

`check_motion_density` は **film.json の `figures` だけ**を数える。AE の 6枠は本編 mp4 に composite された後に焼き込まれるため gate は 0 カウント。→ **密度下限 31 は §6 の Remotion figures（34本）で満たす。** AE はその上に載る「決め所の数値/引用タイポ」。

## 7.2 パイプライン（EP42/43/44/45/47 で measured 済み・cleveland修正版を strieff 用に複製）

```
[1] Remotion で本編完成 → strieff_final_bgm.v001.mp4（音声ミックス済み・build_strieff_bgm_real.py→film_offset 適用・OFF=11.5）
[2] scripts/ae/build_strieff_hero_cards.py（＝cleveland修正版を複製＝実測フィット＋引用折返し＋repo path出力＋aerender二段構成）が beats.json と strieff_hero.jsx を生成
[3] AfterFX -noui -r strieff_hero.jsx → 各ビートを 1920x1080@30fps の不透明 mp4 で書き出し
[4] scripts/ae/composite_strieff_hero.py（＝composite_caniglia_hero.py を複製）が ffmpeg overlay + enable='between(t,start,end)' で焼き込み
[5] 出力 → strieff_final_bgm.v002_ae.mp4（v001 は絶対に上書きしない・film_offset 適用）
```
> **offset = hookSeconds(8.0) + 3.5 = 11.5**（ブリーフ§5）。beats を実発話に再アンカーし、section 窓からオフセットで算出しクランプ。

## 7.3 AEカードデッキ（★6枚・ブリーフ§6 VERBATIM・§1.4 の確定数値のみ・6制約適用・数値は台帳照合・accent #9C6BAA）

> **★レイアウトは複製元 `build_cleveland_hero_cards.py` が実装する6種のみ**（`ACT_TITLE_CARD`/`CENTER_STACK`/`MONEY_STACK`/`SPLIT_COMPARE`/`QUOTE_CARD`/`VOTE_SPLIT`）。**★`DATE_STAMP` と `SEAM_TRANSITION` は実装に存在しない（JSX は `else throw "unsupported layout"`）＝使うと AE ビルド即クラッシュ。日付カードは `CENTER_STACK`（下段テキストに `579 U.S. 232` / `SUPREME COURT`）で表現する（CODEX_B が正典）。** **この表と CODEX_B のデッキは id・レイアウト・N-ID が完全一致**（`validate_strieff_beats` が両方を突き合わせる）。上記6種以外は使わない。**EP49 は 5-3 が台帳にあるので `VOTE_SPLIT` を使用。`ACT_TITLE_CARD`（幕頭は Remotion `acttitle` が担う）/ `MONEY_STACK` は §7.3 では未使用。** variety は使用4種で ≥3 を満たす。

| id | レイアウト（実装済み8種） | hero（主表示） | top / sub / bottom / attribution | 数値ID | 背景（象徴のみ・顔なし） | 尺 |
|---|---|---|---|---|---|---|
| **c01** | **CENTER_STACK** | **THE STOP WAS ILLEGAL** | top: **NO REASONABLE SUSPICION** / bottom: **BUT THE EVIDENCE STAYED** | — | 路肩のパトライト（顔なし・plum） | 6.5 |
| **a01** | **SPLIT_COMPARE** | **THE ILLEGAL STOP / THE EVIDENCE** | top: **ATTENUATION** / bottom: **THE WARRANT BROKE THE CHAIN** | — | 断ち切られた鎖の一本の環 | 7.0 |
| **v01** | **VOTE_SPLIT** | **5 – 3** | top: **THE EVIDENCE WAS ADMISSIBLE** / bottom: **AN 8-JUSTICE COURT · SCALIA'S SEAT EMPTY** | N01/N02 | 最高裁の空席・列柱 | 6.5 |
| **t01** | **CENTER_STACK** | **2016 · SUPREME COURT** | 下段: **UTAH V. STRIEFF · 579 U.S. 232** | N03/N04 | 大理石の階段（判読困難） | 5.0 |
| **q01** | **QUOTE_CARD** | **"YOU ARE NOT A CITIZEN OF A DEMOCRACY BUT THE SUBJECT OF A CARCERAL STATE, JUST WAITING TO BE CATALOGED"** | attribution: **JUSTICE SOTOMAYOR, DISSENTING** | N07 | 記録/ファイルの壁 | 8.5 |
| **k01** | **QUOTE_CARD**（任意・尺が許せば） | **"THE OFFICER'S INCENTIVE TO VIOLATE THE CONSTITUTION THUS INCREASES"** | attribution: **JUSTICE KAGAN, DISSENTING** | N09 | incentive の歯車 | 7.5 |

> **★行順＝start 昇順（時系列）:** `c01`(ACT1 stop illegal) < `a01`(ACT2 attenuation) < `v01`(ACT3 5-3) < `t01`(ACT3 date) < `q01`(ACT3 Sotomayor) < `k01`(ACT3 Kagan・任意)。**start は §7.4 beats.json で section 窓からオフセットで算出しクランプ**するため、**本番 rendered base の秒で単調増加・重複ゼロ**を `validate_strieff_beats` が保証する。**この id・レイアウト・N-ID は CODEX_B デッキと一字一致。**
> **★c01（CENTER_STACK）は hero "THE STOP WAS ILLEGAL"（C1・停止は違法）＋ bottom "BUT THE EVIDENCE STAYED"（証拠は残った）を必ず別レイヤーで焼く。「the stop was legal」を書いたら FAIL（R-LEGAL）。**
> **★a01（SPLIT_COMPARE）は top "ATTENUATION" / bottom "THE WARRANT BROKE THE CHAIN"。attenuation を「停止を合法化した」と読ませる語を書かない（因果を断つのであって違法を消さない・R-ATTEN）。**
> **★v01（VOTE_SPLIT 5-3）は top に "THE EVIDENCE WAS ADMISSIBLE"（R-VOTE 対語）・bottom に "AN 8-JUSTICE COURT · SCALIA'S SEAT EMPTY"（N02）を必ず別レイヤーで焼く。「6-3 / exclusionary rule abolished / illegal → struck down」を書かない。** 5-3 を中立に（どちらが正義かを断じない・C3）。
> **★q01（Sotomayor QUOTE_CARD）の attribution は "JUSTICE SOTOMAYOR, DISSENTING"（R-QUOTE・C4）。逐語 N07 の substring（末尾の "…the subject of a carceral state, just waiting to be cataloged" を含む・ellipsis 可）を1字も改変しない。Court に帰属させたら FAIL。** **k01（Kagan QUOTE_CARD）の attribution は "JUSTICE KAGAN, DISSENTING"。hero は N09 の逐語 clean-sentence。**
> **どのカードにも「the stop was legal / exclusionary rule abolished / we are all harmed / 6-3」・Fackrell 名・dochighlight を書かない。** 数値ID＝台帳（§1.4）と一致必須。カウント終了から区間終端まで最低 1.20秒ホールド。em-dash は本文表示の `—` と異なり **beats.json ラベルでは ASCII `-` に置換**（AE の豆腐回避・§7.6）。

### 検算

```
[1] 6区間（k01 任意）・本番 start 単調増加・重複ゼロ（build_strieff_hero_cards.py が section 窓オフセットで算出）
[2] HOOK TEASER(0–8.0) / HOOK(8.0–...) / BrandOpening / BrandEndcard に1秒も重ならない
[3] 合計 = 6.5+7.0+6.5+5.0+8.5+7.5 = 41.0秒 / 741.1 = 5.5%   ✓ 過剰でない
[4] レイアウト種類 = CENTER_STACK, SPLIT_COMPARE, VOTE_SPLIT, QUOTE_CARD = 4種（全て実装済み6種内）   ✓ ≥3
[5] figures[] 34枠と1秒でも重ならない（validate_strieff_beats.py が両方突き合わせ）
[6] dochighlight/comparebars レイアウトは存在しない（8種のみ）   ✓ R-DOCHL
[7] R-LEGAL: c01 "THE STOP WAS ILLEGAL" / R-VOTE: v01 "ADMISSIBLE"+"8-JUSTICE" / R-QUOTE: q01="Sotomayor, dissenting" k01="Kagan, dissenting"   ✓
```

## 7.4 `beats.json`（`08_edit/ae_hero/beats.json`・`schema_version: "strieff_beats.v1"`）

各 beat に `id` / `layout` / `start` / `end` / `dur` / `still`(象徴 or null) / `hero` / `top` / `bottom` / `sub` / `caption`(**改行禁止・最大50字**) / `value` / `numKeys` / `blend_mode`(既定 "overlay") / `required` / `out` / `attribution`(**QUOTE_CARD=q01/k01 は必須**・§1.4 と一致・R-QUOTE)。**区間の秒は本番 rendered base（narration_index 由来）に一致させ、section 窓からオフセットで算出しクランプ（offset=11.5）。** 数値カード（5-3 の票）は文字列（"5 - 3"）で焼く（票カウントの count-up は "0→5"/"0→3" の1桁のみ可・二桁化しない）。JSX で算術しない（EP38 確定ルール）。

## 7.5 レイアウト定義・色定数（EP43/44/45/47 を踏襲・色のみ EP49 値・CODEX_B と一致）

**共通レイヤースタック（下→上）:** L9 黒ソリッド → L8 静止画（scale fill→fill×1.08・drift）→ L7 グレードウォッシュ（**ユタの夜 plum near-black** `addSolid([0.055,0.043,0.071])`＝NIGHT / MULTIPLY / opacity 30）→ L6 羽根付き楕円ビネット → L5 グロー（下中央 somber-plum 差し ADD）→ L4 ライトスイープ（`"ADBE Rotate Z"`=18）→ L3 上ラベル（Oswald）→ L2b アクセントライン（ACCENT plum・scaleX ワイプ・`motionBlur=true`）→ L2 主数値/主文字（Anton・ACCENT・`motionBlur=true`）→ L1b 下ラベル → L1 字幕ロワーサード → **L0b AI開示テキスト（`AI-assisted visualization`・Oswald 20px・SILVER `#C8CDD6`・opacity 70%・右下 `[W-32, H-28]`・全カード常時焼き＝R1）** → L0 黒シームディップ（head/tail 各4フレーム）。

**★EP49 色定数（0..1 float・somber-plum レーン色。EP41〜48 の他話色を流用禁止・CODEX_B と一致）:**
```python
ACCENT = [0.612, 0.420, 0.667]  # #9C6BAA somber-plum — 数値・下線・唯一の差し色
WHITE  = [0.961, 0.969, 0.980]  # #F5F7FA
SILVER = [0.784, 0.804, 0.839]  # #C8CDD6（開示テキスト）
INK    = [0.039, 0.039, 0.047]  # #0A0A0C 近黒ルート（サムネ bg と一致）
NIGHT  = [0.055, 0.043, 0.071]  # #0E0B12 ユタの夜 plum near-black ウォッシュ
STEEL  = [0.110, 0.118, 0.141]  # #1C1E24 database/booking 冷灰
MARBLE = [0.200, 0.192, 0.227]  # #33313A 大理石（ACT3）
```
**フォント:** 数値/主文字 = **Anton Regular** / ラベル・字幕 = **Oswald Medium**。`getFontsByFamilyNameAndStyleName` で厳格解決（miss は throw・フォールバック禁止）。テキスト幅は **`sourceRectAtTime(t,false).width` で実測**（advance-width 推定禁止＝EP40 文字切れの原因・ブリーフ§5）。**`v01` の "5 - 3" を ACCENT plum、ラベルを WHITE/SILVER。`v01` の "ADMISSIBLE"/"8-JUSTICE"・`q01`/`k01` の attribution・`a01` の "THE WARRANT BROKE THE CHAIN"・`c01` の "THE STOP WAS ILLEGAL" は削除禁止。**

**カウント型:** 5-3 は "5 - 3" の文字列（count-up は "0→5" / "0→3" の1桁のみ可）。**停止を "legal"・排除法則を "abolished" とするラベルを一切作らない（R-LEGAL）。QUOTE_CARD は逐語のみ・"we are all harmed" を作らない（R-QUOTE）。**

## 7.6 このマシン固有の罠（★1つ忘れると無言で品質が落ちる・EP42-45/47 全項を strieff に適用）

フォント解決の例外ラップ（`psName()`・allFonts の array-LIKE ラッパーを unwrap）／spatial ease は配列次元1（`prop.isSpatial ? 1 : ...`）／OM=`"H.264 - レンダリング設定を一致 - 15 Mbps"`・RS=`"最良設定"`（英語名は try/catch フォールバック）／`app.newProject()` を headless で使わない（同名 `STRIEFF_` コンプを防御削除）／`layer.motionBlur=true` を動くレイヤー個別に／回転は `"ADBE Rotate Z"`／改行は1行厳守（SPLIT_COMPARE/VOTE_SPLIT の左右2値は別レイヤー・改行禁止）／em-dash は `-`／inPoint と outPoint 両方設定／`item.mainSource.conformFrameRate = 30`／実行パス `C:\Program Files\Adobe\Adobe After Effects 2026\Support Files\AfterFX.exe`／`proj.gpuAccelType = GpuAccelType.SOFTWARE`／ビルド ~100–120秒・完了マーカー `render/_build_ok.txt` をポーリング（タイムアウト≥300秒）・末尾で `app.quit()`／**aerender 前に `.aep` mtime > `.jsx` を assert**（ブリーフ§5・.aep が古いと前ビルドを焼く事故）／**repo path 出力＋aerender 二段構成**（cleveland修正版の要点）。q01 の長い逐語は **引用折返し**（実測幅で複数行に安全に割る）。

## 7.7 コンポジタ（`scripts/ae/composite_strieff_hero.py`・SKIP 4条件を1つも削らない）

`BASE = strieff_final_bgm.v001.mp4` / `OUT = strieff_final_bgm.v002_ae.mp4`（v001 不変）。SKIP: (1) `render/<id>.mp4` 不在 / (2) 解像度≠1920x1080 / (3) 実測尺 `< dur-0.3` / (4) `beat.end > base_dur`。ffmpeg: `overlay=0:0:eof_action=pass:enable='between(t,start,end)'` / `-c:v libx264 -preset slow -crf 16 -pix_fmt yuv420p -colorspace bt709 -c:a copy`。**出荷済みを絶対に上書きしない。film_offset（11.5）を適用する。**

---

# 8. レイヤー構成 と ゾーン分離（★主役の裏に最低4層）

## 8.1 本編カットのレイヤー構成（下→上・主役 L4 の裏に L1/L2/L3/L3b = 4層）

| L | 名前 | EP49 の値 |
|---|---|---|
| **L0** | ルート背景 | `#0A0A0C`（INK） |
| **L1** | グラデ背景 | `radial-gradient(120% 120% at 50% 40%, #0E0B12 0%, #0B0910 45%, #0A0A0C 100%)`（ユタの夜 plum near-black。ACT3 のみ大理石寄り `#33313A` にシフト・database は `#1C1E24`） |
| **L2** | グリッド/ライン | 縦横 64px の反復線＋放射マスク＋ドリフト。`repeating-linear-gradient(0deg/90deg, #9C6BAA18 0px 1px, transparent 1px 64px)`、`translateY 0→48px` / `Easing.inOut(Easing.sin)`（等速禁止） |
| **L3** | グロー | 単一 somber-plum の差し。`radial-gradient(closest-side, #9C6BAA66 0%, #9C6BAA18 45%, transparent 75%)`、`filter: blur(28px)`。位置は幕で移動（家/駐車場→パトライト→database→毒の木/鎖→大理石/空席→開いた扉） |
| **L3b** | 大理石の光帯/ビネット | ACT3 は歴史/収斂の光帯（`linear-gradient(100deg, transparent, #9C6BAA22, transparent)` を横に slow drift）、他幕は羽根ビネット。`translateX` を `Easing.inOut(Easing.sin)` で微動（静止フレームゼロ） |
| **L4** | 主役（still / i2v / factory） | §10 のモーション（Ken Burns/parallax/i2v） |
| **L5** | テロップゾーン（上/中央・figures） | §8.2 |
| **L6** | 字幕ゾーン（下部帯） | §8.2 |

> **主役（L4）の裏に L1/L2/L3/L3b = 4層**（グラデ背景・グリッド/ライン・グロー・光帯/ビネット）で CLAUDE.md「最低3レイヤー」＋タスク「最低4層」を満たす。**各層は §3.1b の通り常に微動（静止フレームゼロ）。**

## 8.2 ゾーン分離（一度も重ねない）

| ゾーン | 縦位置（1080基準） | スタイル |
|---|---|---|
| テロップ見出し | `y=96–260` | Oswald 64px / `#F5F7FA` / letterSpacing 4 |
| 中央テロップ / figures | `y=420–660` | §6 |
| 出典テロップ（アクセントライン） | `y=742–786` | Oswald 28px / somber-plum `#9C6BAA` 3px 下線 |
| 字幕帯 | `y=872–1010` | 白 `#FFFFFF` + `textShadow:0 0 6px #000,0 2px 4px #000` / 半透明黒帯 `rgba(6,6,8,0.62)` / ≤2行・1行≤42字 / 54px / lineHeight 1.28 |
| AI開示 | `y=1024–1052`（右下） | Oswald 20px / `#C8CDD6` / opacity 70% |

**Caption QC:** ナレ一致 ≥99%（faster-whisper 強制アライン）/ `.srt` カバー ≥95% / キュー 1.0–6.0秒 / CPS ≤17 / 単語割り禁止 / 1語孤立キュー禁止 / ズレ ≤120ms。**【SILENCE 1】区間と HOOK TEASER 無音区間には字幕キューを置かない。**

---

# 9. 絵コンテ（★48シーン・象徴のみ・6制約・Strieff/Fackrell 非人物化・薬物臨床最小限・CODEX_A が 85本プロンプトへ展開する原図）

## 9.1 パーサ契約（★CODEX_A が `ai_prompts.v001.md` を書くときの形式・`read_prompts()` が読む2行形式）

```
- `S01.png`
<positive prompt> ... [STYLE] Avoid: <negative>
```
- **1行目:** `` - `S01.png` ``（バッククォート囲み・行末は `.png` 直後）。プロンプトを同じ行に書かない。
- **2行目:** 正プロンプト → `[STYLE]`（§5.5）→ `Avoid:` → 負プロンプト（§5.6）。
- 配置先: **`episodes/PD-2026-049-strieff/04_scenes/ai_prompts.v001.md`**。生成: `.venv/Scripts/python.exe scripts/generate_sdxl_4k.py PD-2026-049-strieff`（**variants 指定なし＝1枚**）。
- 出力: `H:\pd-media\assets\ai\strieff\S01.png …` ＋ `remotion/public/strieff/`。長辺 ≥3840 で冪等スキップ。
- **★body 85本＝85行**（still 各1枚）＋ **i2v 種 16行**（M01_src..M16_src）＝ `ai_prompts.v001.md` は計 **101 エントリ**。CODEX_A は書いた直後 `--only S01` で `shots=` が **101** に達しているか（2行形式が壊れていないか）を確認。**プロンプト実体（85本）は CODEX_A が正典**（本節は絵コンテ級の原図）。

## 9.2 絵コンテ級ショット記述（Sid ごと・カメラ/モーション/象徴/制約。CODEX_A はこれを固有プロンプトに翻訳）

> **全ショット共通:** 顔・身体・肖像なし（R1/C5）。Edward Strieff/Detective Fackrell を個人として描かない（象徴・物・後ろ姿・手元・影のみ）。**Strieff は後ろ姿/手元/象徴のみ**（顔・正面・身体を描かない）。**薬物は閉じた小さな証拠袋の象徴のみ**（粉/器具/使用/血/現場を描かない・C5）。読める文字を作らない（redacted/illegible）。判例番号・日付・票数・Fackrell 名を描かない。ユタの夜 plum＋database 冷灰＋冷たい大理石＋唯一の差し色 somber-plum。**「停止は合法/排除法則は廃止」に見える絵を作らない**（C1/C2）。最高裁の列柱/空席＝5-3・8名の場／attenuation は断ち切られた鎖で描く。天秤は3要素の中立対比（C3）。

| Sid | カメラ/レンズ | 象徴（動き） | 制約メモ |
|---|---|---|---|
| S01 | 引き・夜 | ユタの夜・家の前の扉が開き暖光・後ろ姿が出る | C5: 顔なし・R2 |
| S02 | 追い・後方 | 後ろ姿が駐車場を横切る（i2v: 歩き）＝SILENCE | C5: 後ろ姿のみ |
| S03 | 引き・夜 | 向こうに停まる刑事の無人車・plum パトライト反射 | C5: 人物なし |
| S04 | 接写・手元 | 手渡される ID カードと無線マイク | C5: 手元のみ・顔なし |
| S05 | 正対・画面 | database の画面に令状フラグが解決（i2v: フラグ） | C6: 令状の文字は判読不能 |
| S06 | 正対・push-in | 最高裁の淡い大理石列柱＝2016 の答え（factory） | C3: 最高裁の場 |
| S07 | 正対 | 違法に得た証拠が棚/証拠台から外される象徴 | C2: 本来は捨てられる |
| S08 | 接写 | 一本の弱い環のある鎖＋"ATTENUATION" 形成 | C2: 因果を断つ narrow な考え |
| S09 | 引き・夜 | 通報で断続監視される家（ACT1 幕頭） | C5: 人物なし |
| S10 | 引き・往来 | 短時間の出入りを繰り返す訪問者の後ろ姿（i2v） | C5: 顔なし・後ろ姿 |
| S11 | 追い・後方 | Strieff が駐車場を横切る後ろ姿 | **C5: R2・顔/身体なし** |
| S12 | 路肩・斜光 | 路肩に差すパトライト＝理由なき停止 | **C1: 違法な停止・州が譲歩** |
| S13 | 接写・手元 | 手渡される ID カード | C5: 手元のみ |
| S14 | 正対・冷灰 | 無線でのディスパッチャ照会（database） | C5: institutional 非扇情 |
| S15 | 正対・画面 | 令状ヒットの画面＝古い交通令状フラグ（i2v） | C6: 令状文字は判読不能 |
| S16 | 接写・寄り | 令状での逮捕＝閉じる手錠（i2v: 手錠が閉じる） | **C5: 身体を描かず象徴** |
| S17 | 接写・机上 | 捜索に伴う閉じた小さな証拠袋 | **C5: 薬物臨床最小限・粉/器具なし** |
| S18 | 正対・入口 | courthouse の扉＝ユタ最高裁→合衆国最高裁 | C6: 手続・名前なし |
| S19 | 引き・逆光 | 毒の実る木（fruit of the poisonous tree） | C2: 排除法則の比喩 |
| S20 | 俯瞰 | 停止＝毒の木／薬物＝その実（compbars 素地） | C2: 中立対比・判読不能 |
| S21 | 接写・机上 | 例外が刻まれた古い規則書（判読不能） | C2: 絶対ではない |
| S22 | 接写 | attenuation＝鎖が引き伸ばされ薄くなる（i2v） | C2: 因果を断つ・薄れる |
| S23 | 正対 | 鎖が保つか断つか＝本件の争点 | C2: 争点は違法性でなく連結 |
| S24 | 接写 | factor① 時計＝数分（抑制寄り） | C2: 時間的近接=州が負けた |
| S25 | 正対 | factor② 令状が鎖に割り込む（介在事情） | C2: 決定的・州寄り |
| S26 | 正対・天秤 | factor③ 天秤が警察の行為を量る | C2: 悪質性・過失止まり |
| S27 | 正対・天秤 | 3要素の三面天秤＝attenuation test（stat 3） | C6: 3 は figures |
| S28 | 正対・対称 | 最高裁の列柱（ACT3 幕頭・荘厳・最も遅い・factory） | C3: 5-3 の場 |
| S29 | 正対 | 5-3 の投票が "five" で解決するバロット | **C1/C3: ADMISSIBLE 対語・votetally は figures** |
| S30 | 正対・対称 | 空席＝Scalia の椅子・8席のベンチ | **C3: 8名・空席** |
| S31 | 机上・接写 | Thomas 多数の開いた意見集（判読不能） | C3: for the Court |
| S32 | 接写 | factor① 時間で州が負けた（数分・判読不能） | C2: 抑制寄り |
| S33 | 正対・画面 | 令状が浮上する＝停止の前から存在（i2v: surfacing） | C2: 介在事情・決定的 |
| S34 | 正対・天秤 | flagrancy＝せいぜい過失・悪質でない | C2: 州寄り |
| S35 | 接写 | 鎖が断ち切られる＝attenuation（i2v: 環が壊れる） | **C2: 因果の遮断・違法は消えない** |
| S36 | 机上 | 反対意見の2冊が開く（Sotomayor / Kagan） | C4: 反対＝負けた側 |
| S37 | 引き・壁 | 記録/ファイルの壁＝"cataloged" | **C4: Sotomayor "carceral state" 逐語は figures・帰属 dissenting** |
| S38 | 接写 | 白人被告の一節＝誰の尊厳も（判読不能） | **C4: Sotomayor "anyone's dignity" 逐語は figures・帰属 dissenting** |
| S39 | 正対・機械 | incentive の歯車＝違法停止を促す誘因 | **C4: Kagan 逐語は figures・帰属 dissenting・mechanism gears** |
| S40 | 俯瞰 | 3票が並ぶが5票に届かない象徴（判読不能） | C3/C4: three votes, not five |
| S41 | 追い・後方 | 駐車場に戻る後ろ姿＝あなたの通り | 現在形・payoff 起点・C5 |
| S42 | 正対・画面 | database に再び令状フラグ（あなたの名前） | C6: 判読不能 |
| S43 | 接写 | 消えなかった不正＝薄れる違法停止 | C1: wrong が問題でなくなった |
| S44 | 俯瞰 | 多くの人が持つ小さな令状＝多数のフラグ | C6: 未払い/古い切符・数値なし |
| S45 | 接写 | 一本だけ薄くなった環の鎖（i2v: 環が痩せる） | C1: almost free |
| S46 | 接写 | 弱まった第4修正＝断層線（判読不能） | C2: 規則が弱まる・廃止でない |
| S47 | 正対・扉 | 開いたままの扉＝違法停止が令状に救われる（i2v） | C1: plum の薄明・payoff |
| S48 | 引き・pull-back | 駐車場の後ろ姿へ slow pull-back（i2v） | C5: 顔なし・CTA |

---

# 10. 本編カットのモーション仕様（★等速線形禁止・opacity 単独禁止・fps=30 で定数化）

## 10.1 秒→フレーム定数（★フレーム直書き禁止・全て `Math.round(fps × 秒)`）

```ts
const FPS = 30;
const f = (sec: number) => Math.round(FPS * sec);
const CUT_MEAN = f(3.19);   // = 96f  平均ショット
const CUT_MIN  = f(1.0);    // = 30f  最短
const CUT_MAX  = f(6.0);    // = 180f 最長（SPEC cap）
const QUANT    = f(0.5);    // = 15f  ★カット境界の量子化単位（0.5s 刻み方針）
```
**0.5s 刻み方針:** 226カットの境界は **`QUANT`=15フレーム（0.5秒）にスナップ**して配置する。各カット長は `CUT_MIN`〜`CUT_MAX`、平均 `CUT_MEAN`。ACT3 は最も遅く（長カット寄り・6.0s 近辺を多用）、ACT1 は速く（1.0–2.5s の断片・現在形）、HOOK TEASER は最速（~1.3s cut）。CODEX_B は shotlist の各 span 端を 15f グリッドに丸める。

## 10.2 全カット共通モーション（★静止フレームを1枚も作らない）

| 素材 | 基本モーション | イージング | 数値 |
|---|---|---|---|
| **still** | Ken Burns：`scale 1.00→1.08` を**カット全長**で。加えて `translate` を象徴方向へ ±24px | `Easing.out(Easing.cubic)` | scale 差 +0.08 / drift 24px。**opacity は translate/scale と必ず対**（単独禁止） |
| **i2v** | ネイティブ動き（Wan 2.2 A14B → RIFE 48fps）＋微 `scale 1.00→1.03` | ネイティブ＋`Easing.out(Easing.cubic)` | 追い足しの scale は 0.03 のみ |
| **factory** | 実写の内在動き＋微 Ken Burns `scale 1.00→1.04` | `Easing.out(Easing.cubic)` | 24pxまでの parallax 可 |

**カットイン/アウト:** クロスディゾルブ 6–10f または hard cut。HOOK TEASER/HOOK/ACT1 の断片は hard cut 寄り（現在形・抑制）。ACT3 は長めのディゾルブ（荘厳・最も遅い）。**フェードは opacity 単独にせず、入りは `translateY 12px→0`＋opacity、抜けは `scale 1.00→1.02`＋opacity を対にする。**

## 10.3 速い動きの motion-blur（★@remotion/motion-blur の Trail）

```tsx
import {Trail} from '@remotion/motion-blur';
<Trail layers={6} lagInFrames={1.2} trailOpacity={0.45}>
  {/* 主役 or 動く数値/文字 */}
</Trail>
```
対象（fast move）: **HOOK TEASER のパトライト/令状フラッシュ**、**S05**（令状フラグ）、**S10**（訪問者の往来）、**S15**（令状ヒット）、**S16**（手錠 closingdoor）、**S18 courthouse 扉**、**S33**（令状 surfacing）、**S35**（鎖 faultsplit）、および §6 の `votetally`/`stat` 桁変化・幕頭 `acttitle`・`kinetic:emphasis` の切れ上がり。**S01/S06/S28（荘厳 push-in）・S02（後ろ姿の緩い歩き）・S22/S45（緩い i2v）・S47/S48（扉/pull-back）・Ken Burns には Trail をかけない**（無駄な残像・扇情を避ける・C5）。

## 10.4 テキストのマスク切れ上がり（★基本形・全 figures / 字幕見出し / 幕タイトル・overflow:hidden＋translateY）

```tsx
<span style={{display:'inline-block', overflow:'hidden'}}>
  <span style={{
    display:'inline-block',
    transform:`translateY(${interpolate(sp,[0,1],[110,0])}%)`,
    opacity: interpolate(sp,[0,0.25],[0,1]),   // ★translateY と対（単独禁止）
  }}>{char}</span>
</span>
```
- `sp = spring({frame: frame - delay, fps, config:{damping:16, mass:1}})`
- **複数文字・複数要素はスタッガー**: `delay = i * f(0.04)` = 1文字/2フレーム（30fps）。
- 幕タイトル語群・figures の見出しは全てこの `overflow:hidden`＋`translateY` マスク切れ上がりを基本形にする。**等速線形は1箇所も使わない**（spring か `Easing.out(Easing.cubic)`）。

---

# 11. オープニング（OP）設計 — 完全仕様（`OpeningStrieff`・fps=60・CLAUDE.md §1–5 全項目）

## 11.1 秒数ベースのタイムライン（fps=60・「フレーム」は全て `Math.round(60 × 秒)`・直書き禁止・0.5s 刻み方針で全区間記述）

```ts
const FPS_OP = 60; const F = (s:number)=>Math.round(FPS_OP*s);   // 総 180f = F(3.0)
```

| 秒 | フレーム | 起きること（EP49 signature = ユタの夜の駐車場に後ろ姿＋plum のパトライトの差し） |
|---|---|---|
| 0.00–0.10 | f0–6 | 画面 `#0A0A0C`。**L1** グラデ opacity 0→1（0.40s）＋ **scale 1.08→1.00** を 180f で（`Easing.out(Easing.cubic)`）。opacity 単独でなく scale 併用 |
| 0.10–0.15 | f6–9 | **L6 ロゴ**（`hasLogo`）左上 `top:64/left:72` に spring 出現。scale 0.4→1.0・opacity 0→1（併用・`damping:14,mass:0.9`） |
| 0.15–0.25 | f9–15 | **L2** グリッドが spring（`{damping:200,mass:1,durationInFrames:F(0.8)=48}`）で reveal。最終 opacity=`gridReveal*0.18`。全体を 180f で `translateY 0→48px`（`Easing.inOut(Easing.sin)`） |
| 0.25–0.30 | f15–18 | **L3** somber-plum のグローが spring（`{damping:18,mass:1.2}`）＝夜のパトライトの差し。scale 0.6→1.15 / opacity 0→0.85（併用）。`filter:blur(28px)` |
| 0.30–0.86 | f18–52 | **L4 主役タイトル**が1文字ずつ切れ上がる（`overflow:hidden` マスク）。各文字 spring（`{damping:16,mass:1}`）で `translateY 110%→0`、opacity=`interpolate(sp,[0,0.25],[0,1])`。**スタッガー=`F(0.04)=2フレーム/文字**。全体を `Trail`（`layers=6,lagInFrames=1.2,trailOpacity=0.45`）で包む |
| 0.55–1.15 | f33–69 | **L2b plum の光ライン**（EP49固有＝紫の帯がタイトル背後を横切る）。中央から `scaleX 0→1`＋`opacity 0→0.55`（spring `{damping:22,mass:1.1}`, `transformOrigin:'center'`）。somber-plum。opacity 単独禁止で scaleX 併用 |
| 0.95–1.35 | f57–81 | **L5a** plum の下線が左から `scaleX 0→1`（spring `{damping:16,mass:0.8}`, `transformOrigin:'left center'`）。240×6px・`boxShadow:0 0 24px #9C6BAAaa` |
| 1.10–1.55 | f66–93 | **L5b** サブタイトルが `translateY 24px→0`＋opacity 0→1（spring `{damping:20,mass:1}`・併用） |
| 1.55–2.20 | f93–132 | 全要素 settle。背景 scale 1.02 付近を減速進行。グリッドのドリフト継続。**完全静止フレームゼロ** |
| 2.20–3.00 | f132–180 | ホールド。背景 scale 1.00 着地、グリッド translateY 48px 着地。**フェードアウトしない** |

> **0.5s 刻み方針:** 上表の各 0.5s 境界（0.0/0.5/1.0/1.5/2.0/2.5/3.0）で「何が動いているか」が必ず1つ以上ある（静止区間ゼロ）。

## 11.2 イージング・ディレイ・移動量・damping（数値表・等速線形ゼロ・opacity 単独ゼロ）

| 要素 | プロパティ | 種別 | 数値 |
|---|---|---|---|
| L1 背景 | scale 1.08→1.00 | `Easing.out(Easing.cubic)` | 180f |
| L2 グリッド reveal | opacity 0→gridReveal*0.18 | spring | `{damping:200,mass:1,durationInFrames:48}` |
| L2 グリッド drift | translateY 0→48px | `Easing.inOut(Easing.sin)` | 180f |
| L3 グロー | scale 0.6→1.15 / opacity 0→0.85 | spring | `{damping:18,mass:1.2}` |
| L4 各文字 | translateY 110%→0 / opacity | spring | `{damping:16,mass:1}`・スタッガー 2f |
| L4 Trail | 残像 | — | `layers=6,lag=1.2,opacity=0.45` |
| L2b plum の光 | scaleX 0→1 / opacity 0→0.55 | spring | `{damping:22,mass:1.1}`・origin center |
| L5a 下線 | scaleX 0→1 | spring | `{damping:16,mass:0.8}`・origin left |
| L5b サブ | translateY 24px→0 / opacity | spring | `{damping:20,mass:1}` |
| L6 ロゴ | scale 0.4→1.0 / opacity | spring | `{damping:14,mass:0.9}` |

> **全 opacity が translateY/scale/scaleX と対。等速線形を1箇所も使わない。**

## 11.3 レイヤー構成（下→上・主役 L4 の裏に L1/L2/L2b/L3 = 4層）

L0 `#0A0A0C` / L1 グラデ（`radial-gradient(120% 120% at 50% 35%, #0E0B12 0%, #0B0910 45%, #0A0A0C 100%)`）/ L2 グリッド（`${accent}22` 64px・放射マスク）/ L2b plum の光（`linear-gradient(90deg, transparent, ${accent}cc, ${accent}55, ${accent}cc, transparent)`）/ L3 somber-plum グロー（`radial-gradient(closest-side, #9C6BAA88, #9C6BAA22, transparent)` `blur(28px)`）/ L4 主役タイトル（Trail 包み・`overflow:hidden` span マスク・Anton `fontWeight:800 fontSize:150 letterSpacing:-2 color:#F5F7FA`）/ L5 下線＋サブ（Oswald `fontSize:38 letterSpacing:6 uppercase color:#C8CDD6`）/ L6 ロゴ（`linear-gradient(135deg, ${accent}, #ffffff22)`・`border:2px solid ${accent}`）。

## 11.4 確認方法（CLAUDE.md §5）

```bash
cd C:\Users\aab15\Documents\prime-documentary\remotion
npm run studio     # = remotion studio。OpeningStrieff を 0→180f でスクラブし §11.1 の各時刻を目視
npx remotion render OpeningStrieff out/strieff_opening.mp4 --props=./props/strieff.json
# props 差し替え量産
npx remotion render OpeningStrieff out/strieff_short_op.mp4 --props=./props/strieff_short.json
# 本編
npx remotion render Ep49Strieff out/strieff_final.mp4 --props=./src/data/strieff_film.json --public-dir=public_slim --concurrency=4
```

---

# 12. props 定義と型（CLAUDE.md §4）

```ts
export type OpeningStrieffProps = {
  title: string;      // 主役タイトル。1文字ずつスタッガーで切れ上がる
  subtitle: string;   // サブタイトル。UPPERCASE 表示（facts_lock 検査対象）
  accent: string;     // アクセント（HEX6桁・"#"込み）。グリッド/plum の光/グロー/下線/ロゴに波及
  hasLogo: boolean;   // true で左上にロゴバッジ
};
```
**EP49 の確定 props（`remotion/props/strieff.json`）:**
```json
{ "title": "THE WARRANT IN YOUR POCKET", "subtitle": "UTAH V. STRIEFF, 2016", "accent": "#9C6BAA", "hasLogo": true }
```
**量産用 `remotion/props/strieff_short.json`:**
```json
{ "title": "AN ILLEGAL STOP, ADMISSIBLE", "subtitle": "THE WARRANT BROKE THE CHAIN", "accent": "#9C6BAA", "hasLogo": false }
```
> `accent` は **`#9C6BAA` 固定**（EP41 gold / EP42 blue / EP43 amber / EP44 teal / EP45 crimson / EP46 green / EP47 civil-violet の流用は BLOCKER）。`subtitle`/`title` は `facts_lock` 検査対象（「the stop was legal / exclusionary rule abolished / we are all harmed / 6-3」を出さない。`AN ILLEGAL STOP, ADMISSIBLE` は制約1の枠と一致・C1）。**サムネ headlines に Fackrell 名・"about a week" を出さない**（R-HEDGE）。**5-3 をサムネに使うなら "THE EVIDENCE STAYED / ADMISSIBLE / 8 JUSTICES" の語を同居**（R-VOTE）。

---

# 13. 受入基準（EP49 の Definition of Done・★語数ゲートが最初・全編アイボール必須）

```bash
cd C:\Users\aab15\Documents\prime-documentary
# 0. 語数（最優先・課金前）
./.venv/Scripts/python.exe scripts/check_script_length.py episodes/PD-2026-049-strieff/03_script/script.en.v001.md --json
# 1. 事実性（EP49固有・§1.3・6制約・dochighlight 0件・R-LEGAL/R-VOTE/R-QUOTE）
./.venv/Scripts/python.exe scripts/check_strieff_facts.py --json
# 2. ビート契約（AE↔figures 非重複・ledger・6制約・dochighlight 0件）
./.venv/Scripts/python.exe scripts/validate_strieff_beats.py
# 3. 密度（★31 を Remotion 側で満たしていること・--ep 指定／--json は出力パス）
./.venv/Scripts/python.exe scripts/check_motion_density.py --ep PD-2026-049-strieff --json runs/qc/strieff_motion.json
# 4. VO速度（ナレ直後・ミックス前）
./.venv/Scripts/python.exe scripts/measure_vo_wpm.py --ep strieff --json
# 5. 最終受入
./.venv/Scripts/python.exe scripts/check_final_acceptance.py 49 --render episodes/PD-2026-049-strieff/08_edit/strieff_final_bgm.v002_ae.mp4 --emit-receipt
```
> **ゲート入力は `--ep PD-2026-049-strieff`。`--json <film.json>` を入力に使わない**（出力パス＝上書き事故。ブリーフ§5）。

| ゲート | 閾値 | EP49 設計値 |
|---|---|---|
| `check_script_length` | band 内 | 2,139語（SPEC・要 PASS 確認・cap 2,141） |
| `runtime_band` | 690–750s | **741.1s = 12:21.1**（上限 750s に 8.9s 余裕） |
| `motion_density` | ≥2.5/min ∧ cov ≥0.25 ∧ variety ≥3 | **2.83/min / 0.264 / 9種**（film.json 34 beats・AE非依存・floor 31 に +3） |
| `animation_mix`（紙芝居） | still-share ≤45% ∧ motion cov ≥45% | **44.69% / 55.31%** |
| `check_asset_reuse` | first-use ≥0.70・still≤2・factory1・motion≤2 | **0.8584 / 2 / 1 / 2** |
| `footage_diversity` | distinct/total ≥0.40 | **0.8584** |
| `visual_asset_qc` | 全 factory 目視 reviewed | **93本 目視（CODEX_A）** |
| `image_resolution` | 長辺≥3840 | 全 SDXL ≥3840 |
| `bgm_present` | 無音>25秒ゼロ | 最長 1.8秒 |
| `caption_integrity` | 一致≥99%・カバー≥95% | §8.2 |
| `op_ed_bookends` | `BrandOpening`/`BrandEndcard` import・不変 | ✓ |
| `asset_manifest` | A↔B counts/role 一字一致・also_thumb 6（S01/S05/S15/S30/S37/S47）・overlay 12・schema `strieff_assets.v1` | §5.8 |
| `facts_lock`（EP49固有・6制約） | violations=0・**dochighlight 0**・R-LEGAL（停止=illegal・排除法則=narrowed）・R-VOTE（5-3=ADMISSIBLE・8名）・R-QUOTE（Sotomayor/Kagan=dissenting・"we are all harmed" 不使用） | §1.2/§1.3 |
| **全編アイボール** | 12:21.1 を通しで目視 | ★1フレーム判定禁止（EP39-41/EP3941 の miss） |

---

# 14. premortem（失敗するとしたらここ）

| # | 失敗モード | 事前対処 |
|---|---|---|
| 1 | **停止を"合法"と誤記／排除法則を"廃止"と誤記**（本作最大リスク） | §1.2 R-LEGAL。停止=ILLEGAL（州が譲歩）。証拠は attenuation 経由のみ。排除法則=NARROWED, NOT ABOLISHED。`the stop was legal / exclusionary rule abolished` を使わない。証拠許容 payload に `attenuat/warrant broke the chain/intervening` 必須 |
| 2 | **票決の誤記（6-3 混入）** | §1.2 R-VOTE。**5-3・Scalia 空席で 8名**。自動要約の "6-3" は誤り。5-3 payload に "ADMISSIBLE/STAYED/8 JUSTICES" 対語必須 |
| 3 | **"we are all harmed" を逐語引用**（非逐語・S15） | §1.2 R-QUOTE。**1箇所も引用しない**。皆が害される論点は Sotomayor 逐語 "anyone's dignity can be violated in this manner"（N08）か地の文で |
| 4 | **引用の帰属ミス**（反対を Court/majority に） | §1.2 R-QUOTE。**Sotomayor/Kagan="dissenting"**。逐語のみ・要約を引用符に入れない |
| 5 | **Strieff 肖像 / 薬物扇情** | §5.6/§9 R-FACE/R-DRUG。後ろ姿/手元/象徴のみ・顔/身体なし・R2。薬物は閉じた小さな証拠袋の象徴のみ（粉/器具/使用/血/現場なし・臨床） |
| 6 | **medium 値の画面焼き**（Fackrell 名・"about a week"） | §1.4 R-HEDGE。画面 hard 数値は 5-3/2016/579 U.S. 232/8 JUSTICES/3 FACTORS/2006 のみ。Fackrell 名は発話のみ |
| 7 | **番号ズレ**（別番号を発明） | シーンは S01..S48 固定（§3.2）。still 資産 ID は S01..S85（別空間・cross-map 禁止） |
| 8 | **紙芝居**（still-share 45%超・余裕 0.31%pt） | §5.1 で still-cut 101 固定・factory 93・i2v 32。still1つ増で 45% に近づく → cut を増やさず同一シーンの新規 distinct で回復 |
| 9 | **バリエーション水増し**（`--variants 3`） | §5.3。variants 指定なし＝1枚。ai_prompts は 85行＝85枚 |
| 10 | **密度 FAIL**（AEカードに頼る） | §6。film.json に 34 beats（31 超）。AE 6枠は composite 後で非カウント |
| 11 | **画像プロンプトが読めない**（0枚生成） | §9.1 の2行形式・`--only S01` で `shots=101`（body 85 + i2v種 16）確認 |
| 12 | **ファイル名信仰**（牛が本編に入る） | §5.4 factory 93本を `build_footage_contact_sheet.py` で全点目視（CODEX_A BLOCKING） |
| 13 | **dochighlight のバグ見え**（3回指摘） | §6.2/§7.3。`dochighlight`/`comparebars` を1件も置かない（R-DOCHL・grep 0）。**全 kind は実 FigureBeats.tsx union で検証済** |
| 14 | **FigureBeats kind 大文字で無音描画 / 非実在 kind** | §6.2 kind は全小文字・実 union 準拠（`compbars`・`comparebars` は非実在） |
| 15 | **AE em-dash 豆腐 / 等速 / OM名英語 / 文字切れ / 長い逐語の折返し失敗** | §7.6。テキスト幅は `sourceRectAtTime(t,false).width` 実測。q01 の Sotomayor 逐語は実測幅で複数行に折返し |
| 16 | **id 誤り / durationInFrames 手書き**（切り詰め・綴り違い等） | §0.1。`id="Ep49Strieff"`・`caseFilmDurationInFrames(strieffFilm,30)`=22233（hookSeconds=8.0） |
| 17 | **accent 流用**（他話色を残す） | §0.5/§7.5/§12。OP props/AEカード/サムネ accent は `#9C6BAA`（RGB [0.612,0.420,0.667]） |
| 18 | **A↔B マニフェスト不整合**（role=thumb/counts 不一致/schema 名違い/public_path 欠落） | §5.8。`strieff_assets.v1`・role enum=`body/i2v_source/reject`・also_thumb 6（S01/S05/S15/S30/S37/S47）・overlay 12・全エントリ public_path を A/B 一字一致 |
| 19 | **EP39〜48 と素材被り** | §2 で10の stock_ledger の sha256 を除外（`select_strieff_factory.py --verify-no-prior-overlap`） |
| 20 | **fast端で 750s 超**（余裕 8.9s） | §4.1 speed 1.0 明示＋`measure_vo_wpm` 168–190・190超は破棄再発注。総尺 741.1s ≤750 の assert（§3.1[4]） |
| 21 | **public→public_slim 未 staging**（EP45事故） | ブリーフ§5。img/factory/motion/audio を public_slim へ全コピーしてからレンダ |

---

# 15. 設計パッケージ接続（DESIGN → CODEX_A / CODEX_B）

- **DESIGN（本書）:** タイムライン（0〜720.6s 全区間＋8.0s teaser・各Act・§3.1/§3.1b）・レイヤー（背面4層・§8）・モーション数値（§10）・48絵コンテ（§3.2/§9・象徴・6制約・Strieff 顔なし・薬物臨床最小限）・FigureBeats 設計（≥31＝34・小文字kind・変種≥3＝9種・**実 FigureBeats.tsx union 準拠**・dochighlight 0件・quote 逐語＆帰属厳格・"we are all harmed" 不使用・§6）・AEカード表（6枚・accent #9C6BAA・§7.3）・OP 仕様（§11）・asset_manifest スキーマの正（§5.8）。
- **CODEX_A（別ファイル `EP49_strieff_CODEX_A_ASSETS.v001.md`）:** §9 を **85本の固有プロンプト**（1シーン1枚・variants 0・省略禁止で全85本）＋ i2v 16 ＋ factory 93 選定＆**全点目視QC**（`select_strieff_factory.py`・`--exclude-used --ep PD-2026-049-strieff` で EP39〜48 sha256 除外）＋境界契約 `asset_manifest.v001.json`（schema `strieff_assets.v1`・counts を EP49 値 still_body85/still_i2v_source16/motion16/factory93/overlay12・全エントリ public_path・`stills[].role` enum=`body/i2v_source/reject`・also_thumb 6（S01/S05/S15/S30/S37/S47））。
- **CODEX_B（別ファイル `EP49_strieff_CODEX_B_BUILD.v001.md`）:** `build_strieff_film.py`（＝EP48 `build_glover_film.py` or `build_cleveland_film.py` を複製・ASSET_MAP/NARR/FACTORY_SEL/SLUG/EP を strieff に・hookSeconds8.0・正しい hookLine（例「A stop with no reason. A warrant. A search the law now allows.」）・実素材のみ stub 禁止・manifest factory/motion 全読込）／captions（実測 narration）／figures 34（小文字 kind・実 union 準拠・dochighlight 0件・quote 逐語＆帰属・§6）／`CaseFilm` を `id="Ep49Strieff"` で Root.tsx 登録（`caseFilmDurationInFrames`＝22233・hookSeconds=8.0）／`OpeningStrieff`／AEビルダ・コンポジタ（cleveland修正版複製・accent #9C6BAA=[0.612,0.420,0.667]・実測幅・引用折返し・repo path・aerender二段・ledger 照合・.aep>.jsx assert・レイアウト名は実装済み8種のみ・§7.3 の6カード＝本書 §7.3 と一字一致・offset=11.5）・`validate_strieff_beats.py`・`check_strieff_facts.py`（EP45 版を複製・同名・R-NUM asset_manifest除外＋indexキーskip・acttitle除外を継承）／`build_strieff_bgm_real.py`→`composite_strieff_hero.py`（film_offset 11.5 適用）／public_slim staging／レンダ（`--public-dir=public_slim --concurrency=4`）／全ゲート（`--ep PD-2026-049-strieff`）／完成後の全編3回アイボール。
- **A↔B 接続点は `asset_manifest.v001.json` ただ1ファイル**（schema `strieff_assets.v1`・counts/role enum を A/B 一字一致・§5.8）。
- **複製元（★`ls scripts/` で実在確認・実在しないスクリプトを捏造しない）→ strieff 複製先:** EP48 の glover 系（`build_glover_film.py`→`build_strieff_film.py`）or EP45 の cleveland 系（`build_cleveland_film.py`・`check_cleveland_facts.py`→`check_strieff_facts.py`・`select_cleveland_factory.py`→`select_strieff_factory.py`・`validate_caniglia_beats.py`→`validate_strieff_beats.py`・`composite_caniglia_hero.py`→`composite_strieff_hero.py`・`build_caniglia_bgm_real.py`→`build_strieff_bgm_real.py`）を複製元にする。**AEビルダは cleveland 修正版**（`build_cleveland_hero_cards.py`→`build_strieff_hero_cards.py`・実測フィット＋引用折返し＋repo path＋aerender二段）。**共有（複製不要・実在確認済）:** `generate_sdxl_4k.py` / `build_footage_contact_sheet.py` / `check_motion_density.py` / `measure_vo_wpm.py` / `check_script_length.py` / `check_final_acceptance.py`。
