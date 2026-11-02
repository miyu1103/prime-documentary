# EP48 — THE NAME ON THE PLATE — 制作設計書（DESIGN 本体・v001・確定台本版）

- Episode ID: `PD-2026-048-glover` / slug: `glover` / EP48
- 中心の問い（英語・二人称・★"違法だった／どんな車でも停められる"と書かない）: **"If the police run your plate and something on your record comes back, can they stop the car on that alone — before they have checked who is actually driving it?"**（答え＝2020年に最高裁が「できる（合憲・ただし NARROW）」と言った）
- 判例: **Kansas v. Glover, 589 U.S. ___ (2020), No. 18-556**（decided **2020-04-06**・opinion **Justice Thomas**・第4修正の investigative（Terry級）stop）。**8-1**。**Kagan 補足（Ginsburg 同調）＝限界を強調**／**Sotomayor 単独反対**（逐語・反対意見に帰属）。
- 主役: **Charles Glover Jr.**（Kansas・**存命の私人＝R2**・免許取消中の運転で有罪）。**顔・肖像・身体を一切描かない。象徴のみ・尊厳の物語。** 物語は「**あなたの車・停止の合法性**」であって彼を美化しない。原被疑事実（免許取消運転）以外の犯罪性を出さない。Deputy（保安官補）も人物化しない。
- 主題: 登録者の免許が取消（revoked）で、officer に「所有者が運転していない」と示す情報が何も無いとき、officer は「所有者が運転している」と推認して車を停止してよい（＝**その停止は reasonable suspicion があり合憲・UPHELD**）、と最高裁は **8-1 で判断した**。本作は「違法だった／覆された」と決して言わない。**背骨＝"a careful yes, with a hard edge on it"**：推認は打ち消す情報があれば消える／これは reasonable suspicion であって probable cause ではない／「どんな車でも停められる」ではない。
- Status: **BINDING**。**唯一の真実 = 機械生成済み `EP48_glover_PRODUCTION_SPEC.v001.json`**。本書のあらゆる数値はそこ／ブリーフ §2 からの転記で、手書きで発明していない。衝突したら SPEC が勝つ。
- このファイルは**設計パッケージ3分割**（DESIGN / CODEX_A / CODEX_B）の **DESIGN 本体**。共有ブリーフ `EP48_glover_DESIGN_BRIEF.shared.md` を単一の真実源とする。85本の SDXL プロンプト実体・i2v 16・factory 92 選定は **CODEX_A**、`build_glover_film.py`・captions・figures 実装・Root.tsx 登録・AEビルダ/コンポジタ・ゲートは **CODEX_B** に属す（本書は各所でポインタのみ示す）。

## ★このエピソードの唯一の真実（手書きで数値を発明するな）

`episodes/_planning/EP48_glover_PRODUCTION_SPEC.v001.json`（台本から機械生成・`scripts/build_production_spec.py`）＋ ブリーフ §2。本設計書は SPEC/ブリーフを**人間可読な実装指示に翻訳しただけ**で、新しい数字を作っていない。

```
words_total          = 2,136
narration_seconds    = 719.6   （= 12.0分・[SILENCE 1] の実音無音を含む）@ wpm_used 178.1
scenes               = 48      （S01..S48・確定。増やすな減らすな）
total_cuts           = 225
still  distinct 85 / cuts 101 / mean 1.19 / cap 2   ← ★各1枚生成（バリエーション0）
factory distinct 92 / cuts 92 / mean 1.0  / cap 1   ← 在庫選抜・全点目視QC
motion distinct 16 / cuts 32 / mean 2.0  / cap 2
distinct_total       = 193          → 225 カット
first_use_share      = 0.858   （floor 0.70）
still_share_of_cuts  = 0.449   （cap 0.45）
motion coverage      = (92+32)/225 = 0.5511  （floor 0.45）
MG beats_floor       = 30      （film.json 側 figures+graphics+heroCuts。AEカードは check_motion_density に数えられない）
beats_per_min_floor  = 2.5   /  variety_floor = 3
mean_shot_seconds    = 3.19   /  max_shot_seconds = 6.0
幕秒（発話・語数から機械算出／本書 §3 で planning アンカーに使用）:
  HOOK 66.0 / OPENING 49.2 / ACT1 111.8 / ACT2 137.8 / ACT3 201.5 / ENDING 131.4（発話幕秒合計 697.7s）
  ※ 発話幕秒合計 697.7 と narration_seconds マスター 719.6 の差 21.9s = 幕間の息継ぎ＋設計無音（SILENCE 1 = 1.8s）を内包する測定マスター。film.json には 719.6 を入れる。
```

## ★★ 最重要の前提: 1シーン1枚・バリエーション0 ★★（ブリーフ§1）

- Codex の画像生成は高精度。**同一ショットの複数バリエーション（`_01/_02/_03`）を作らない。**
- `04_scenes/ai_prompts.v001.md` は **still 85本＝85行の固有プロンプト**（`generate_sdxl_4k.py` の `read_prompts()` 2行形式・各1枚）＋ **i2v 種 16行** ＝ **計101エントリ**（`--only S01` の `shots=` は 101）。**`--variants 3` は使わない**（`--variants 1` または指定なし）。
- **総生成画像 = still 85 + i2v seed 16 = 101枚（各1回）。** **factory 92 は生成ではなく在庫選抜**（全点目視QC・EP39〜47 と sha256 被りゼロ）。
- **still を増やして factory を削るな**（still-share 0.449 は cap 0.45 に対し余裕 0.1%pt しかない）。**still-cut は 101 で固定。**

## ★EP39〜47 で踏んだ失敗＝本書が最初から潰す設計判断

| # | 失敗 | 本書での恒久対策 | 参照 |
|---|---|---|---|
| 1 | **番号ズレ**（別リストを発明） | シーンは **S01..S48 に固定**。still 資産 ID は S01..S85（別空間・cross-map 禁止） | §3.2 / §9 |
| 2 | **紙芝居**（still 100% で animation_mix FAIL） | still-cut **101 固定**＋factory実写 **92**＋i2v **32**。still-share 44.9% ≤45% / motion cov 55.11% ≥45% を構造保証 | §5.1 |
| 3 | **バリエーション水増し** | **1シーン1枚・85本を各1枚**。variants 禁止 | §5.3 |
| 4 | **画像プロンプトのパーサ非互換** | `read_prompts()` の**2行形式**。CODEX_A が `--only S01` で拾い数（101）を確認 | §9.1 |
| 5 | **ファイル名を信じた**（牛が documents） | factory 92本を `build_footage_contact_sheet.py` で**全点目視QC**（CODEX_A 必須・BLOCKING） | §5.4 |
| 6 | **AEカードを密度に数えた** | `check_motion_density` は film.json の `figures+graphics+heroCuts` だけ。**film.json 側に MGビート 30本以上**（本書は 36 設計）。AE は composite 後で 0 カウント | §6.1 / §7.1 |
| 7 | **一枚絵で完成判定**（EP39-41/EP3941 の眼球不足） | 全編アイボール必須（§13）。measured > estimated | §13 |
| 8 | **A↔B マニフェスト不整合** | asset_manifest は **A↔B で同一スキーマ・counts/role enum を一字一致**。role=`thumb`/`still_thumb` を作らない。サムネは `also_thumb=true` の body still 6枚 | §5.8 |
| 9 | **dochighlight のバグ見え**（EP40/41/42 で3回指摘） | **`dochighlight` を figures に1件も入れない（grep 0・R-DOCHL）。** 書類/免許/登録票/切符は `lowerthird` の説明テキストで表す | §6.2 / §7.3 |
| 10 | **判示の過大化／取り違え**（本作固有の最大リスク） | 停止は **UPHELD（8-1・reasonable suspicion・NARROW）**。`illegal/unconstitutional/struck down` を停止に使わない。「stop any car」「probable cause required」を書かない。**reasonable suspicion ≠ probable cause** を厳格区別（R-OVERCLAIM/R-STANDARD） | §1.2 |
| 11 | **引用の帰属ミス／捏造** | quote は検証済逐語のみ。**Sotomayor="Justice Sotomayor, dissenting"／Kagan="Justice Kagan, concurring"／Thomas="Justice Thomas, for the Court"**（R-QUOTE） | §1.2/§6.2 |
| 12 | **Glover 肖像／顔** | R2・象徴のみ・顔なし（R-FACE）。全ショット人物なし・影/手元/シルエットのみ | §5.6/§9 |

---

# 0. 環境・Remotion設定（CLAUDE.md §0 準拠）

## 0.1 本編 `Ep48Glover` の Composition 設定（★本編の正・誤記注意）

| 項目 | 値 |
|---|---|
| `id` | **`Ep48Glover`**（Root.tsx に `CaseFilm` で登録。ブリーフ§5「id=Ep48Glover」。**id の切り詰め・綴り違い・小文字化は誤記＝BLOCKER**） |
| 解像度 | **1920 × 1080** |
| `fps` | **30**（EP44〜47 と同値。フレームは全て `Math.round(30 × 秒)`・直書き禁止） |
| `hookSeconds` | **8.0**（★BrandOpening 前に置く**無音コールドオープン teaser preroll**＝フラッシュモンタージュ・ナレなし・BGM 低弦のみ。§3.1 参照。durationInFrames 4項関数の第1項に入る。**EP44/45 の hookSeconds=0＋流用hookLine 事故を回避**） |
| `hookLine` | **glover 専用（他話流用禁止）。例: `"A plate. A hit. A stop you never saw coming."`**（film builder に焼く・ブリーフ§5） |
| `durationInFrames` | **`caseFilmDurationInFrames(gloverFilm, 30)` = 22203**（4項の実関数 `round(hookSeconds×30)+round(OPENING_SEC×30)+ceil(narrationSeconds×30)+round(ENDCARD_SEC×30)`・**hookSeconds=8.0**・§3.1[3] で算出。手書きで数値を入れず関数で算出する） |
| component | `remotion/src/compositions/CaseFilm.tsx`（**既存の汎用 `CaseFilm` を再利用**・実在確認済。`Bookends.tsx` の `BrandOpening`/`BrandEndcard` を **import**・fork 禁止） |
| data | `remotion/src/data/glover_film.json`（`scripts/build_glover_film.py` で再生成できる状態を保つ＝**git 未追跡**） |

**Root.tsx 登録（★ブリーフ§5・CODEX_B が実装）:**
```tsx
import {gloverFilm} from './data/glover_film.json';
import {caseFilmDurationInFrames} from './lib/caseFilmDuration';
// ...
<Composition
  id="Ep48Glover"
  component={CaseFilm}
  width={1920} height={1080} fps={30}
  durationInFrames={caseFilmDurationInFrames(gloverFilm, 30)}  // = 22203
  defaultProps={{film: gloverFilm}}
/>
```
> **id は `Ep48Glover`**（切り詰め・綴り違い・小文字化は全て誤記。ブリーフ§5 の render 行 `Ep48Glover` が正）。`CaseFilm.tsx` は実在。`caseFilmDuration` ヘルパの実体名は CODEX_B が既存実装（atwater/cleveland と同一）に合わせる。

## 0.2 タイトルバンパー `OpeningGlover` の Composition 設定（CLAUDE.md 正典部品準拠）

| 項目 | 値 |
|---|---|
| `id` | **`OpeningGlover`** |
| 解像度 | **1920 × 1080** |
| `fps` | **60**（CLAUDE.md §0 の正典値。OP 単体は 60fps） |
| `durationInFrames` | **180**（= 3.0秒 @ 60fps） |
| component | `remotion/src/compositions/OpeningGlover.tsx`（§11 全仕様） |

> `OpeningGlover` は**独立したタイトルバンパー成果物**（`out/glover_opening.mp4`）。本編内 OP/ED の正典は `Bookends.tsx`（`BrandOpening` 3.50s / `BrandEndcard` 9.00s・不変）。`OpeningGlover` を本編に ffmpeg で焼き込まない（オーナー承認なしに見え方を変えない）。

## 0.3 必要な依存パッケージ

```bash
cd C:\Users\aab15\Documents\prime-documentary\remotion
npm i @remotion/motion-blur     # CLAUDE.md 必須依存（Trail によるモーションブラー）
```

## 0.4 `remotion.config.ts`（CLAUDE.md §0 正典値・EP41〜47 と同一・書き換えない）

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
> レンダーログで `crf 16 / preset slow / yuv420p / bt709 / aac 320k / libx264` を必ず確認。本編レンダは `--public-dir=public_slim --concurrency=4`（ブリーフ§5・**public→public_slim へ img/factory/motion/audio 全メディアをコピー staging**＝EP45事故回避・全media解決0確認）。

## 0.5 ブランド／レーン色（`remotion/src/brand.ts` から import・ハードコード禁止）

**EP48 のパレット（★夜のハイウェイの冷たい near-black ＋ パトカー車内の冷灰 ＋ 淡い大理石の最高裁 ＋ 唯一の差し色＝patrol-steel）:**
```
INK    = #0A0A0C   ルート背景（サムネ bg と一致）
NIGHT  = #0C1014   夜のハイウェイの冷たい near-black（road/taillights 側の地）
STEEL  = #1A2028   パトカー車内・ラップトップ光の冷灰（squad interior 側）
MARBLE = #34363B   最高裁の冷たい大理石（ACT3・列柱・9席）
ACCENT = #5B8DB8   ★patrol-steel（一点差し色）。ブランド数値・ライン・下線・グロー・OP/AE/サムネ accent。★EP41 gold / EP42 warrant-blue / EP43 amber / EP44 teal / EP45 crimson / EP46 green / EP47 civil-violet を流用しない
WHITE  = #F5F7FA
SILVER = #C8CDD6   （AI開示テキスト）
```
> **レーン分離:** EP42 warrant-blue（濃紺・尋問室）と EP48 patrol-steel は**別物**。EP48 は **navy interrogation / electric blue を使わず**、夜のハイウェイの near-black `#0C1014` ＋ パトカーの冷灰 `#1A2028` ＋ 冷たい大理石 `#34363B` を地に、唯一の差し色を **patrol-steel `#5B8DB8`**（ラップトップ画面と light bar の冷たい青）に置く。接尾に `warrant-blue` `navy interrogation` `electric blue` `porch-amber` `teal-green hospital` `crimson overdue` `forest-green` `civil-violet` を含めない。**factory は EP39〜47 の `stock_ledger*.json` の sha256 を除外**（CODEX_A・BLOCKING）。**CODEX_B は OP props / AEカード / サムネ accent を必ず `#5B8DB8` にする（他話色の流用は BLOCKER）。**

---

# 1. 事実の取り扱い（★正確性6制約＝FACTS LOCK / `check_glover_facts.py`・BLOCKING）

## 1.1 確定台本（唯一の正・1バイトも変えない）

```
C:\Users\aab15\Documents\prime-documentary\episodes\_planning\EP48_glover_script.en.v001.md
```
**本番配置先:** `episodes/PD-2026-048-glover/03_script/script.en.v001.md`（上記を1バイトも変えずコピー）。整形も禁止。台本の幕構成（HOOK / OPENING / ACT_1 / ACT_2 / ACT_3 / ENDING）と `【SILENCE 1 — 1.8s】`（**1箇所**・HOOK 内・"Hold on the screen reading REVOKED. No music."）を正典とする。存在しない演出マーカーを発明しない。

## 1.2 ★正確性6制約（全出力＝プロンプト・カード文言・図表・字幕・タイトルに適用。1つでも違反＝BLOCKER）

| # | 制約 | 出力での順守 |
|---|---|---|
| **C1** | **判示は NARROW・過大化しない** | 判示は「officer に『所有者が運転していない』と示す情報が無いとき、所有者が運転していると推認して停止するのは reasonable」というもの（G10/G12/G19）。**推認は打ち消す情報があれば消える**（例：60代の所有者なのに20代が運転しているのが見える＝推認消滅・G12）。**`the police can stop any car` / `stop any car at any time` / `a plate check alone lets police stop anyone` を書かない**（R-OVERCLAIM）。枠は **"a careful yes, with a hard edge on it"** / "narrow" / "dissolves the moment the officer can see he is wrong"。 |
| **C2** | **reasonable suspicion であって probable cause ではない** | 停止は investigative（Terry級）stop の **reasonable suspicion**（G09）。**probable cause / certainty ではない。** `probable cause required/needed`（この停止の基準として）を書いたら FAIL（R-STANDARD）。逐語比較（G09）"considerably less than … probable cause" を保つ。 |
| **C3** | **停止は UPHELD（8-1）・"違法/覆された"と言わない** | 停止は第4修正に反しない＝合憲・UPHELD（G10/G13）。**`illegal / unconstitutional / struck down / overturned / the Court ruled the stop wrong / violated the Fourth Amendment`（Glover の停止を主語に肯定形で）を使わない**（R-VOTE/R-DISPO）。8-1 payload に `upheld / reasonable / the stop stands / did not violate / a narrow rule` のいずれかを同居させる。 |
| **C4** | **票決 8-1・中立帰属** | Thomas 法廷意見／**Kagan 補足（Ginsburg 同調）＝限界を強調**（revocation≠suspension・一目で別人なら推認消滅）／**Sotomayor 単独反対**（G13/G14/G15-17）。逐語は反対/補足として**中立帰属**（Court に帰属させない）。どちらが「正しい」と画面で断じない。 |
| **C5** | **Charles Glover＝R2・象徴のみ／広告安全** | 存命の私人（免許取消運転で有罪）。**顔・肖像・身体を描かない。象徴のみ**（プレート・ラップトップのヒット画面・夜のハイウェイ/テールランプ・免許証の取消判子・登録票・天秤・所有者≠運転者のシルエット対比・最高裁列柱/9席）。原被疑事実以外の犯罪性を出さない。Deputy も人物化しない。交通停止・4A の物語として枠付け＝**完全に広告安全**（暴力・犯罪現場なし）。 |
| **C6** | **数値は台帳一致・捏造ゼロ・medium 値は画面に出さない** | 画面に焼く hard 数値は **8-1（票・high）／APRIL 6, 2020（判決日・high）／589 U.S. ___（引用・high・lowerthird 退避）** のみ（§1.4）。**Deputy の氏名（Mehrer）・郡（Douglas）・プレート番号・車種（1995 Chevy）・"about an hour" 等は confidence:medium＝ヘッジ／画面に断定で出さない**（ブリーフ§3.6・R-HEDGE）。捏造引用禁止。 |
| **R1** | **実在人物の顔・肖像を生成しない** | 全生成ビジュアル表示中は `AI-assisted visualization`（右下）常時表示。概要欄に1行 AI 開示。 |

## 1.3 6制約ゲート `check_glover_facts.py`（`scripts/check_glover_facts.py`＝EP45 `check_cleveland_facts.py` を glover 用に複製。exit≠0 で出荷停止・CODEX_B 実装。出力 `facts_lock.v001.json`）

> **★ゲート名は1本に確定:** 6制約の機械ゲートは **`scripts/check_glover_facts.py`**（出力 `09_package/facts_lock.v001.json`）ただ1つ。**DESIGN / CODEX_A / CODEX_B で同名参照**（別名を作らない）。内部ルール **R-*** に一本化。**★R-NUM 等の構造ルールは narrative figure のみ対象**（asset_manifest 構造カウント・acttitle index は除外＝EP45 修正済／R-NUM は asset_manifest 除外＋index キー skip・acttitle 除外を継承）。

**検査対象:** `03_script/script.en.v001.md` / `remotion/src/data/glover_film.json` の `figures[].kind`・`figures[].*text*`／`primary`／`secondary`／`quote`・`attribution`・`lines[]`・`label` / `08_edit/ae_hero/beats.json` の `hero`/`top`/`bottom`/`sub`/`attribution`/`caption` / `09_package/description.txt` / `remotion/props/glover*.json` の `subtitle`/`title` / `04_scenes/ai_prompts.v001.md`。

| ルール | 内容 |
|---|---|
| **R-OVERCLAIM（★EP48 固有・最大リスク）** | `police can stop any car` / `stop any car` / `stop anyone` / `any car at any time` / `pull over any vehicle` / `a plate check (alone )?lets? (the )?police stop` / `stop your car for no reason` を**肯定形**で出したら FAIL（台本 ENDING の否定文脈「it is not quite true」「not a rule that lets police stop any car」は許容＝否定近傍の検出でスキップ）。 |
| **R-STANDARD** | 停止の基準として `probable cause` を**必要／基準**として肯定した payload（`probable cause (is )?(required|needed|the standard)`）は FAIL。停止基準の payload には `reasonable suspicion` が現れること（正の検査）。逐語比較 G09 の "less than … probable cause" は許容。 |
| **R-VOTE / R-DISPO** | 停止・判決に対し `illegal` / `unconstitutional` / `struck down` / `overturned` / `the Court (said/ruled) the stop (was )?(wrong/unlawful/illegal)` / `violated the Fourth Amendment`（Glover の停止を主語に肯定形で）が出たら FAIL。**`8 ?- ?1` を含む payload に `upheld` / `reasonable` / `stands` / `did not violate` / `a narrow rule` のいずれかが無ければ FAIL**（「8-1 で覆した」誤読の防止）。 |
| **R-QUOTE（帰属厳格）** | `quote` は §1.5 `APPROVED_QUOTES` の逐語のみ。**Sotomayor 逐語**（G15/G16/G17）の attribution は `Justice Sotomayor, dissenting` と一致必須。**Kagan 逐語**（G14）は `Justice Kagan, concurring` 必須。**Thomas 逐語**（G09/G10/G12）は `Justice Thomas, for the Court` 必須。**Sotomayor/Kagan を Court に帰属させたら FAIL。** 要約を引用符に入れたら FAIL。attribution 空なら FAIL。 |
| **R-FACE** | `ai_prompts` 正プロンプトに `portrait`/`face of`/`likeness`/`recognizable`/`Charles Glover`（人物として）/`mugshot`/`his body`/`human face` が出たら FAIL（ネガティブ使用は可）。全ショット人物なし（影/後ろ姿/手元/シルエットのみ）。 |
| **R-HEDGE** | 画面文字列（figures/AE/字幕見出し/props）に **§1.4 の表以外の数値・medium 事実**が出たら FAIL。特に **Deputy 氏名（`Mehrer`）・郡名（`Douglas`）・プレート番号・車種（`1995`/`Chevy`）を hard カード/stamp/stat/lowerthird に出したら FAIL**（confidence:medium・発話のみ許容）。`8-1`/`2020`/`589` を焼く figure/AE は台帳一致必須。 |
| **R-DOCHL（★全話共通）** | `figures[].kind == "dochighlight"` が **1件でも**存在したら FAIL（`grep -c '"dochighlight"'` が 0 でないと出荷停止）。`comparebars` も非実在→出たら FAIL（`compbars` が正）。stub=0。 |
| **R-DISCLOSE** | `description.txt` に AI 開示1行が無ければ FAIL。全生成ビジュアル区間で右下 `AI-assisted visualization` が焼かれていること（§13 アイボールで確認）。 |

**出力:** `09_package/facts_lock.v001.json`（`{"pass":bool,"violations":[{"file","rule","line","excerpt"}],"skipped":[...]}`）。`pass:true` でない限り `check_final_acceptance.py` に進まない。**ALLOWED_NUMBERS = {8, 1, "8-1", 2020, "April 6, 2020", 589}**（Deputy 氏名・郡・プレート・車種・年齢の生数値は含めない）。

## 1.4 画面に出してよい確定数値（★台本／事実対応表 G01–G19 に存在し confidence:high のものだけ。この表以外を画面に出すな）

| ID | 値 | 台本での表現（claim） | conf | 使用先 |
|---|---|---|---|---|
| N01 | **8 – 1**（THE STOP UPHELD・A NARROW RULE） | "By a vote of eight to one … did not violate the Fourth Amendment"（G13/G10） | **high** | AE **v01**（VOTE_SPLIT・**"A NARROW RULE / UPHELD" 対語必須**・R-VOTE）/ figures `votetally`（F-VOTE majority 8 / dissent 1） |
| N02 | **APRIL 6, 2020 · SUPREME COURT** | "In April of 2020, the Court gave its answer"（G18・判決日 high） | high | AE **t01**（CENTER_STACK）/ figures `timeline`（F-TL: the stop → 2020） |
| N03 | **589 U.S. ___**（引用・退避） | 台本本文で読み上げない | high | figures `lowerthird`（"Kansas v. Glover · 2020 · 589 U.S. ___"）・AE t01 place |
| N04 | **REASONABLE SUSPICION（NOT PROBABLE CAUSE）** | "the name for that standard is reasonable suspicion … clearly less than what is needed for probable cause"（G09） | high | AE **c01**（CENTER_STACK）/ figures `probablecause`（outcome "stall"）/ `lowerthird`（"reasonable suspicion — not probable cause"） |
| N05 | **Thomas 逐語 HOLDING**（"When the officer lacks information negating an inference that the owner is driving the vehicle, the stop is reasonable."） | ACT3（G10） | high | figures `quote`（帰属 **Justice Thomas, for the Court**・F-QUOTE-H） |
| N06 | **Sotomayor 逐語**（"…paved the road to finding reasonable suspicion based on nothing more than a demographic profile"） | ACT3（G17） | high | AE **q01**（QUOTE_CARD・帰属 **Justice Sotomayor, dissenting**）/ figures `quote`（F-QUOTE-S2） |
| N07 | **THE OWNER IS PROBABLY DRIVING → UNLESS THE OFFICER KNOWS OTHERWISE**（narrow の対比） | ACT3（G11/G12） | high | AE **f01**（SPLIT_COMPARE）/ figures `compbars`（F-CMP owner vs someone else） |
| N08 | **REVOCATION, NOT SUSPENSION**（Kagan 限界） | ACT3（G14・Kagan concurring） | high | AE **k01**（SPLIT_COMPARE・任意）/ figures `mechanism:faultsplit`（revoked ↔ suspended）/ `lowerthird`（"Justice Kagan, concurring — revocation, not suspension"） |

> **★AE カード文言に「illegal / the Court struck it down / overturned / the stop was wrong / stop any car / probable cause required」を書かない（C1/C2/C3・R-OVERCLAIM/R-STANDARD/R-VOTE）。** **Deputy 氏名・郡・プレート・車種は画面に出さない（R-HEDGE・medium）。** 判例番号 `589 U.S. ___` は t01（CENTER_STACK の下段テキスト）と figures `lowerthird` に退避（本文で読み上げない）。**8-1 は台帳（G13）にあるので焼いてよいが、必ず "A NARROW RULE / UPHELD / REASONABLE" の対語を同一 payload に持つ（R-VOTE）。** 投票の「正誤」を画面で断じない（C4 中立）。

---

# 2. 視覚・音響レーン分離（EP39〜47 との素材被り回避）

> **EP39〜47 のファイルには一切触れない（読み取りのみ可）。** レーンを機械的に分離する。

| 軸 | EP47 atwater | **EP48 glover** |
|---|---|---|
| 舞台 | テキサスの道→booking→大理石 | **夜のカンザスの片側二車線→パトカー車内（ダッシュのラップトップ）→プレート番号の打鍵→照合ヒット画面 REVOKED→light bar→夜のハイウェイ/テールランプ→免許証（取消判子）→登録票→第4修正のページ→天秤（推認 vs 個別的疑い）→免許の上の magnifying glass→"reasonable suspicion" の語→所有者≠運転者のシルエット対比（60代 vs 20代）→最高裁列柱/9席→8-1 の投票→開いた意見集（Thomas 多数／Kagan 補足／Sotomayor 反対）→州境地図→夜明けのハイウェイ** |
| 時間帯 | 午後の埃→冷灰→大理石 | **夜のハイウェイの冷たい闇（道・テールランプ）→パトカー車内のラップトップ冷光→冷灰の路肩→冷たい大理石（ドクトリン核）→夜明けの採光（ENDING）** |
| 支配的出来事 | 罰金のみ→現行犯逮捕→5-4 UPHELD | **プレート照合→取消判明→運転者未確認で停止→第4修正 "unreasonable seizure"→reasonable suspicion（≠probable cause）→登録者=運転者の推認（commonsense）→8-1 UPHELD（NARROW）→打ち消す情報で推認消滅→Kagan 補足（revocation≠suspension）→Sotomayor 反対（逐語）** |
| アクセント色 | civil-violet #7A5CD0 | **patrol-steel #5B8DB8** |
| ベース色 | 埃 near-black + 冷灰 + 大理石 | **夜のハイウェイ near-black #0C1014 + パトカー冷灰 #1A2028 + 冷たい大理石 #34363B + near-black #0A0A0C** |
| レンズ感 | 埃の午後 | **HOOK 夜の象徴フラッシュ（~2s cut・現在形）／ACT1 最短・抑制（the stop）／ACT2 正対の転回（the inference の論理）／ACT3 正対対称・荘厳・最も遅い（the limit）／ENDING 引き（pull-back・夜明け）** |
| 画像保存先 | `H:\pd-media\assets\ai\atwater\` | **`H:\pd-media\assets\ai\glover\`** |
| Remotion データ | `atwater_film.json` | **`glover_film.json`** |
| Remotion コンポ | `Ep47Atwater` | **`Ep48Glover`** |
| AE 作業ディレクトリ | `…/PD-2026-047-atwater/08_edit/ae_hero/` | **`…/PD-2026-048-glover/08_edit/ae_hero/`** |

**素材被り禁止:** EP39〜47 と同一の factory clip / AI画像を1点も使わない。選定前に `episodes/PD-2026-039-*/`〜`…-047-*/` の `05_stock/stock_ledger*.json` を読み sha256 重複を除外（CODEX_A・BLOCKING・`select_glover_factory.py --verify-no-prior-overlap`）。

---

# 3. 尺と構成 — SPEC の値をそのまま使う

## 3.1 全区間タイムライン（★この表が唯一の正・秒は fps=30 から算出しフレーム直書き禁止・0〜719.6s 全区間＋8.0s teaser preroll）

**算出基準:** SPEC の `narration_seconds = 719.6`（マスター）を `glover_film.json` の `narrationSeconds` に入れる。**手計算で上書きしない。** 各幕秒は語数から機械算出した planning アンカー。フレーム = `Math.round(30 × 秒)`。**hookSeconds=8.0** は BrandOpening の前に置く**無音コールドオープン teaser preroll**（フラッシュモンタージュ・ナレなし・BGM 低弦のみ）。

| # | ブロック | 役割 | 語数 | 幕秒 | 台本指定の沈黙 | 固定尺 | 開始f | 終了f |
|---|---|---|---|---|---|---|---|---|
| 0 | **HOOK TEASER**（無音 preroll） | `hook` | 0 | **8.00**（hookSeconds） | — | 8.00 | 0 | 240 |
| 1 | **HOOK** ナレ | `hook` | 196 | 66.0 | **1.8**（"Hold on the screen reading REVOKED. No music." で保持） | — | 240 | 2220 |
| 2 | **BrandOpening** | `opening` | 0 | — | — | **3.50** | 2220 | 2325 |
| 3 | **OPENING** ナレ | `opening` | 146 | 49.2 | — | — | 2325 | 3801 |
| 4 | **ACT1** The stop | `body` | 332 | 111.8（最短） | — | — | 3801 | 7155 |
| 5 | **ACT2** The inference | `body` | 409 | 137.8 | — | — | 7155 | 11289 |
| 6 | **ACT3** The limit | `body` | 598 | 201.5（最長・最も遅い） | — | — | 11289 | 17334 |
| 7 | **ENDING**（payoff→CTA） | `ending` | 390 | 131.4 | — | — | 17334 | 21276 |
| 8 | **BrandEndcard** | `ending` | 0 | — | — | **9.00** | 21276 | 21546 |

> **フレーム列**は teaser(240f)/BrandOpening(105f)/BrandEndcard(270f) を実尺で挟み、幕秒を順に `round(30×秒)` で積んだ実装用アンカー。**幕秒積算 nominal 21546 と §3.1[3] の `caseFilmDurationInFrames` 出力 22203 の差 657f=21.9s は、narrationSeconds マスター 719.6 と発話幕秒合計 697.7 の差＝息継ぎ＋設計無音（SILENCE 1 = 1.8s）を内包する測定マスター。** film.json には 719.6 を入れる。CODEX_B は `glover_film.json` の segment 順から再計算し一致を確認。
> **★台本 OPENING の指定＝「Gold BrandOpening resolves HERE, after the hook question」。** よって順序は **HOOK TEASER（無音）→ HOOK ナレ → BrandOpening（gold 解決）→ OPENING ナレ**。teaser は HOOK と同じ象徴（夜の道・プレート打鍵・ヒット画面 REVOKED・light bar）を ~1.3s の最速カットで無音提示し、そのあと同じ世界にナレが入る。

### 検算（CODEX_B は必ず自分で再計算して一致を確認）

```
[1] narrationSeconds = 719.6（SPEC マスター。手計算で上書きしない）
    ※ 発話ブロック HOOK..ENDING の幕秒合計 = 66.0+49.2+111.8+137.8+201.5+131.4 = 697.7s。
      SPEC マスター 719.6 との差 21.9s は、幕間の息継ぎ＋設計無音（SILENCE 1 = 1.8s）を内包した測定マスター。
    ※ mean_shot 検算: 719.6 / 225 = 3.198s ＝ SPEC mean_shot_seconds 3.19 一致（225カットは 719.6s 全域に張る）。

[2] 総尺 = hookSeconds 8.00 + BrandOpening(OPENING_SEC) 3.50 + narrationSeconds 719.6 + BrandEndcard(ENDCARD_SEC) 9.00
        = 740.1 秒 = 12:20.1

[3] caseFilmDurationInFrames(gloverFilm, 30) = 4項の実関数で算出:
      = round(hookSeconds×30) + round(OPENING_SEC×30) + ceil(narrationSeconds×30) + round(ENDCARD_SEC×30)
      = round(8.0×30)=240 + round(3.5×30)=105 + ceil(719.6×30)=ceil(21588.0)=21588 + round(9.0×30)=270
      = 22,203 フレーム
    ※ CODEX_B は glover_film.json の hookSeconds/narrationSeconds（＋Bookends の OPENING_SEC/ENDCARD_SEC）から
      同関数で再計算し 22203 に一致することを assert する。

[4] runtime_band ≤ 750s の assert（BLOCKING）:
    総尺 = 740.1s = 12:20.1 は band 690–750（11.5–12.5分）の内側（上限 750s に対し 9.9s の余裕）    ✓ PASS
    ※ hookSeconds=8.0 を採用したので余裕は薄い。narrationSeconds が実測で伸びたら再検算（BLOCKING）。
```
> **VO 実測で確定:** `measure_vo_wpm`（合格帯 168–190 wpm）でナレ実測。実測が SPEC マスターと乖離したら CODEX_B は `narrationSeconds` を実測値で更新（planning は 719.6・final は実測が権威）。190超は破棄・speed 0.95 で再発注（BLOCKING）。総尺 740.1s は ≤750 に対し余裕 9.9s しかない＝**実測が伸びたら endcard/teaser を削らず narration speed を確認**。

## 3.1b 秒×アニメーション・タイムライン（★全区間・各beat の start/end フレーム・移動量・easing・damping・stagger・Trail）

> **フレームは全て `f(sec)=Math.round(30×sec)`。等速線形ゼロ・opacity 単独ゼロ・静止フレームゼロ。** 下表は §3.2 の S01..S48 の主アニメを区間単位で示す。カット境界は `QUANT=f(0.5)=15f` グリッドにスナップ（§10.1）。still は Ken Burns（`scale 1.00→1.08`＋drift ±24px・`Easing.out(Easing.cubic)`）を全長。テキスト見出し/figures は `overflow:hidden` 親＋子 `translateY(110%→0)` の spring 切れ上がり（`damping:16,mass:1`・スタッガー `f(0.04)=2f/文字`）を基本形。★fast move（Trail 対象）は「Trail」列に明記。

| 区間(秒) | 開始f–終了f | シーン | 主アニメ（プロパティ・移動量） | easing / damping | stagger | Trail |
|---|---|---|---|---|---|---|
| 0.0–8.0 | 0–240 | HOOK TEASER（無音・~1.3s 最速カット） | 象徴フラッシュ（夜の道→プレート打鍵→ヒット REVOKED→light bar）hard cut・各カット微 KB `scale 1.00→1.03` | `Easing.out(Easing.cubic)` | — | **✓**（light bar/フラッシュ） |
| 8.0–20.0 | 240–600 | S01 夜のカンザス二車線の道（HOOK 開幕） | still Ken Burns `scale 1.00→1.06` / drift +18px（ヘッドライトの流れ） | `Easing.out(Easing.cubic)` | — | — |
| 20.0–33.0 | 600–990 | S02 プレート番号がラップトップに打鍵（i2v M01: cursor/keys） | i2v native ＋ 追い足し `scale 1.00→1.03` | native + cubic | — | — |
| 33.0–46.0 | 990–1380 | S03 通り過ぎるピックアップのテールランプ（違反なし） | still `scale 1.00→1.07` / drift +20px | `Easing.out(Easing.cubic)` | — | — |
| 46.0–54.0 | 1380–1620 | S04 ヒット画面が REVOKED に解決（i2v M02: 文字確定・**fast**）→SILENCE 1.8s 前半 | i2v native ＋ 数値見出しなし・画面のみ | native | — | **✓** |
| 54.0–66.0 | 1620–2220 | S05 light bar（静止保持→SILENCE 1.8s 完全無音）→hard cut で BrandOpening | still `scale 1.00→1.04`・完全無音の画 | `Easing.inOut(Easing.sin)` 微動 | — | — |
| **73.4–77.0** | **2220–2325** | **BrandOpening 3.50**（Bookends・不変・gold 解決） | — | — | — | — |
| 77.0–100.0 | 2325–3000 | S06 小さなカンザスの町・二車線ハイウェイ（OP establishing・factory） | factory 内在動き＋微 KB `scale 1.00→1.04` | `Easing.out(Easing.cubic)` | — | — |
| 100.0–115.0 | 3000–3450 | S07 最高裁の淡い大理石列柱（2020 の答え） | still push-in `scale 1.00→1.08` / drift +12px 上 | `Easing.out(Easing.cubic)` | — | — |
| 115.0–126.7 | 3450–3801 | S08 手前にプレート・奥に遠い最高裁列柱（距離）＋acttitle | acttitle `THE STOP` 切れ上がり・still KB | spring `damping:16,mass:1` | 2f/文字 | figure reveal **✓** |
| 126.7–150.0 | 3801–4500 | S09 ピックアップ車内・運転者は影・顔なし（ACT1） | still KB・`lowerthird` "no traffic violation observed"（F-LT） | spring `damping:20,mass:1` | — | — |
| 150.0–175.0 | 4500–5250 | S10 夜のハイウェイ・後方に付くパトカー light bar 点灯（i2v M05・**fast**）＋S11 ラップトップの登録票 | i2v swing・`mechanism:closingdoor`（F-MECH1 the stop is made） | native + spring | — | **✓** |
| 175.0–205.0 | 5250–6150 | S12 免許証の REVOKED 判子＋S13 カンザスのプレート接写 | still KB・`kinetic:emphasis` "HE NEVER SAW THE DRIVER" (["NEVER"]・F-KIN)・F-LT "a revoked license — not a suspension" | spring `damping:16` | 2f/文字 | **✓** |
| 205.0–235.0 | 6150–7050 | S14 officer の窓辺のシルエット（顔なし）＋S15 courthouse の扉 | still KB・drift ±24px 交互・`lowerthird` "the driver's identity — unconfirmed" | `Easing.out(Easing.cubic)` | — | — |
| 235.0–258.9 | 7050–7767 | S16 suppression motion の紙＋S17 stipulated facts の署名頁＋S18 停止の凍結（light bar の路面グロー・ACT1 締め） | still KB・mechanism は間に stat/kinetic を挟む | `Easing.out(Easing.cubic)` | — | — |
| 258.9–290.0 | 7767–8700 | S19 第4修正のページ＋acttitle・ACT2 幕頭 | acttitle `THE INFERENCE` 切れ上がり・F-LT "The Fourth Amendment — 'unreasonable searches and seizures'" | spring `damping:16` | 2f/文字 | **✓** |
| 290.0–325.0 | 8700–9750 | S20 天秤 a hunch↔proof＋S21 免許の上の magnifying glass | `quote`（Thomas 標準 G09・**for the Court**）・`probablecause` outcome "stall"（reasonable suspicion は probable cause 未満） | spring `damping:18` + native | — | tick **✓** |
| 325.0–360.0 | 9750–10800 | S22 "REASONABLE SUSPICION" の語＋S23 天秤が傾く（i2v M09: tip・**fast**） | `lowerthird` "reasonable suspicion — not probable cause"・i2v native ＋ `mechanism:gears`（推認エンジン owner→driver・F-MECH2） | native + `Easing.out(Easing.cubic)` | — | tip **✓** |
| 360.0–376.5 | 10800–11289 | S24 二閾値＋S25 登録票（所有者名欄・ぼかし）＋S26-S30（compbars/kinetic/carkeylock を ACT2 窓内に再アンカー） | `compbars` [{"the registered owner",1},{"a spouse · child · friend · mechanic",1}]（F-CMP・C4 中立）・`kinetic` "A PROBABILITY, OR A FACT?"・`carkeylock`（F-KEY） | spring `damping:18` origin left | 2f/文字 | — |
| 376.5–410.0 | 11289–12300 | S31 最高裁の9席のベンチ（ACT3 幕頭・荘厳・最も遅い）＋acttitle | acttitle `THE LIMIT` 切れ上がり・F-LT "Kansas v. Glover · 2020 · 589 U.S. ___" | spring `damping:16` | 2f/文字 | **✓** |
| 410.0–435.0 | 12300–13050 | S32 8-1 の投票（"one" で解決・votetally F-VOTE） | `votetally` majority 8 / dissent 1 settle（**"A NARROW RULE · UPHELD" 対語・R-VOTE**）・drift +12px | `Easing.out(Easing.cubic)` | — | tick **✓** |
| 435.0–465.0 | 13050–13950 | S33 夜の最高裁の列柱（factory）＋S34 開いた意見集: Thomas HOLDING 逐語 | factory 内在＋`quote`（Thomas G10 HOLDING・**for the Court**・F-QUOTE-H）長ディゾルブ 10f | native + `Easing.out(Easing.cubic)` | 2f/語 | — |
| 465.0–495.0 | 13950–14850 | S35 commonsense inference（キー環と wheel）＋S36 一本の清い線＝narrow rule | still push-in `scale 1.00→1.08`＋`brightline` mode "draw"（F-BL） | native + `Easing.out(Easing.cubic)` | — | line **✓** |
| 495.0–525.0 | 14850–15750 | S37 所有者≠運転者のシルエット対比（60代 vs 20代・i2v M13・**fast**）＋narrow の限界 | i2v native ＋ `kinetic:emphasis` "A NARROW RULE" (["NARROW"])・F-LT "owner in his sixties · driver in her twenties → suspicion dissolves" | native + spring | 2f/文字 | **✓** |
| 525.0–555.0 | 15750–16650 | S38 Kagan 補足の意見集＋S39 REVOKED↔SUSPENDED の判子対比 | `quote`（Kagan G14・**concurring**・F-QUOTE-K）→ `mechanism:faultsplit`（revoked↔suspended・F-MECH3） | maskslide + spring | 2f/語 | line **✓** |
| 555.0–590.0 | 16650–17700 | S40 Sotomayor 反対の意見集＋S41 一目で推認が消える（i2v M15・**fast**） | `quote`（Sotomayor G15・**dissenting**・F-QUOTE-S1）→ `lowerthird` "Justice Sotomayor — the lone dissent" → `quote`（Sotomayor G17 'paved the road'・**dissenting**・F-QUOTE-S2） | maskslide + native | 2f/語 | **✓** |
| 590.0–578.0※ | 17700–17334 | S42/S43（lone dissent・the line drawn）は ACT3 窓内へ再アンカー | `timeline`（the stop → APRIL 6, 2020・F-TL・N02）・still KB | `Easing.out(Easing.cubic)` | — | tick **✓** |
| 578.0–610.0 | 17334–18300 | S44 あなたの車に戻る（ENDING）＋S45 プレートが再び打鍵 | still KB・`kinetic:emphasis` "SUSPICION, NOT CERTAINTY" (["SUSPICION"]) | spring `damping:16` | 2f/文字 | **✓** |
| 610.0–650.0 | 18300–19500 | S46 影の運転者が見えてくる＝the limit＋S47 天秤 settle・州境地図 | still KB・`lowerthird` "not 'any car' — a sensible inference, until the facts say otherwise"・`statemap` "your state · reasonable suspicion" | `Easing.out(Easing.cubic)` | — | — |
| 650.0–706.0 | 19500–21180 | S47 続き＋`brightline` mode "hold"（the line the Court drew）＋disclosure 再掲 | `brightline` hold・`lowerthird` "AI-assisted visualization"・still KB drift ±16px | `Easing.out(Easing.cubic)` | — | — |
| 706.0–719.6 | 21180–21276 | S48 夜明けのハイウェイへ pull-back（i2v M16・payoff）→CTA→BrandEndcard 21276 開始 | i2v native ＋ slow `scale 1.00→1.02` pull-back・字幕のみ | native + `Easing.out(Easing.cubic)` | — | — |

> **★背面レイヤーは常に4層以上動く（§8.1）。** 各 0.5s 境界で「動いている要素」が最低1つある（静止区間ゼロ）。Trail 対象（fast move）は **TEASER の light bar/フラッシュ / S04 ヒット確定 / S10 light bar 点灯 / S23 天秤 tip / S36 bright line draw / S37 シルエット対比 / S41 推認消滅 / votetally・timeline の桁 / 幕頭 acttitle・kinetic の切れ上がり**。**S01/S07/S31 の荘厳 push-in・S05/S48 の light bar/夜明け・Ken Burns には Trail をかけない**（無駄な残像・扇情を避ける・C5）。
> ※印の区間は幕秒窓と scene 割当の丸めで前後する箇所。**CODEX_B は §3.2 の scene→幕割当を正とし、各 scene を自幕の秒窓（§3.1）内に再アンカーする**（窓外にはみ出さない）。

## 3.2 シーン→幕の割当（★S01..S48 を固定・別番号を発明しない・48シーン）

各シーンは narrative beat。225カットを 48シーンに分散（平均 4.69カット/シーン）。`primary` は各シーンの主素材（still=SDXL 各1枚 / factory=実写 / motion=i2v）。ambient/繋ぎは factory を各シーンに撒く（§5.1）。**象徴のみ・6制約順守・Glover/Deputy 非人物化・顔なし。絵コンテ級の記述は §9。**

> **★2つの `Sxx` 名前空間は別物（取り違え禁止）:** 本節の **narrative シーンは `S01..S48`**。一方 **still 資産 ID は `S01..S85`**（CODEX_A・1プロンプト=1枚で48シーンに85枚を配分）。横断参照時は「どちらの空間か」を明示し、cross-map しない。

| Sid | 幕 | 内容（象徴・6制約・顔なし） | primary |
|---|---|---|---|
| S01 | HOOK | 夜のカンザス片側二車線の道・ヘッドライトの流れ・車も人もほぼ見えない（現在形の開幕） | still |
| S02 | HOOK | パトカーのダッシュのラップトップにプレート番号が打鍵される（i2v: cursor/keys） | **motion** |
| S03 | HOOK | 通り過ぎるピックアップのテールランプ＝何も違反していない | still |
| S04 | HOOK | 照合ヒット画面が REVOKED に解決（i2v: 文字が確定・**fast**）＝反転の瞬間 | **motion** |
| S05 | HOOK | パトカーの light bar（静止保持・SILENCE 1.8s の画・hard cut で BrandOpening へ） | still |
| S06 | OP | カンザスの小さな町・二車線ハイウェイの establishing（factory ambient） | factory |
| S07 | OP | 最高裁の淡い大理石列柱＝2020 に答えた court（正対・荘厳・遠い） | still |
| S08 | OP | 手前にプレート1枚・奥に遠い最高裁列柱＝小さなプレートから最高裁までの距離 | still |
| S09 | ACT1 | ピックアップ車内・運転者は影・ハンドル上の手元のみ（顔なし・違反なし） | still |
| S10 | ACT1 | 夜のハイウェイ・後方に付くパトカーの light bar が点く（i2v: 点灯・**fast**） | **motion** |
| S11 | ACT1 | ラップトップ画面の登録票/プレート照合（判読不能・所有者名欄はぼかし） | still |
| S12 | ACT1 | 免許証の REVOKED の判子＝取消（suspension ではない） | still |
| S13 | ACT1 | カンザスのプレート接写・夜露 | still |
| S14 | ACT1 | トラックの窓辺に立つ officer の影/後ろ姿（顔なし・手元のみ） | still |
| S15 | ACT1 | 平凡なレンガの courthouse の扉（institutional・入口） | still |
| S16 | ACT1 | 机上の suppression motion の紙（判読不能）＝停止を争う | still |
| S17 | ACT1 | 両者合意の stipulated facts の署名頁（判読不能） | still |
| S18 | ACT1 | 停止の凍結＝路面に落ちる light bar のグロー（ACT1 締め） | still |
| S19 | ACT2 | 開いた第4修正のページ（判読不能・"unreasonable searches and seizures" が核） | still |
| S20 | ACT2 | 天秤の左に a hunch・右に proof＝基準の重さ | still |
| S21 | ACT2 | 免許証の上の magnifying glass＝運転者を確かめる/確かめない | still |
| S22 | ACT2 | 大きく刻まれた語 "REASONABLE SUSPICION" の抽象（中間地点） | still |
| S23 | ACT2 | 天秤が傾く（i2v: tip・**fast**）＝どちらへ傾くか（中立） | **motion** |
| S24 | ACT2 | probable cause ↔ reasonable suspicion の二つの閾値（判読不能ラベル） | still |
| S25 | ACT2 | 登録票の所有者名欄（判読不能・ぼかし）＝名前 vs 人 | still |
| S26 | ACT2 | 冷光の長い courthouse 廊下（factory ambient・案件が上がる通路） | factory |
| S27 | ACT2 | citation form ↔ 画面の名前＝プレートの確率 vs 運転者の事実 | still |
| S28 | ACT2 | 所有者以外の運転者候補（配偶者・子・友人・整備士）の空のシルエット/複数の鍵 | still |
| S29 | ACT2 | 手から手へ渡される車の鍵＝誰が実際に運転するか | still |
| S30 | ACT2 | あらゆる運転者が通る空の夜の道＝この推認は全員に触れる（ACT2 締め） | still |
| S31 | ACT3 | 最高裁の9席のベンチ（正対・荘厳・最も遅い・ACT3 幕頭・8-1 の場） | still |
| S32 | ACT3 | 8-1 の投票が "one" で解決するバロット（votetally F-VOTE・**UPHELD/NARROW 対語**） | still |
| S33 | ACT3 | 夜の最高裁の列柱・大理石（factory ambient・establishing） | factory |
| S34 | ACT3 | 暖い机上に開いた意見集＝Thomas HOLDING の逐語行（判読不能・quote は figures） | still |
| S35 | ACT3 | commonsense inference＝キー環と wheel（所有者が運転する日常の推認） | still |
| S36 | ACT3 | 大理石面に引かれた一本の清い線＝narrow rule（bright line） | still |
| S37 | ACT3 | 所有者≠運転者のシルエット対比（60代 vs 20代・i2v: 対比が立つ・**fast**・顔なし） | **motion** |
| S38 | ACT3 | Kagan 補足の開いた意見集＝revocation≠suspension（quote F-QUOTE-K・帰属 concurring） | still |
| S39 | ACT3 | REVOKED の判子 ↔ SUSPENDED の判子の対比＝限界の分岐（mechanism faultsplit） | still |
| S40 | ACT3 | Sotomayor 反対の開いた意見集（quote F-QUOTE-S1/S2・帰属 dissenting） | still |
| S41 | ACT3 | 一目で運転者が見え、推認が消える（i2v: 影が晴れる・**fast**・顔は出さずシルエットのみ） | **motion** |
| S42 | ACT3 | 8票に1票が届かない象徴＝lone dissent（負けた側・判読不能） | still |
| S43 | ACT3 | 最高裁が引きなお消していない一本の線（ENDING 手前・the line drawn） | still |
| S44 | ENDING | 自分の車の夜のドライブウェイに戻る＝あなたの車（現在形・payoff の起点） | still |
| S45 | ENDING | プレートが再びラップトップに打鍵される＝あなたのプレート | still |
| S46 | ENDING | 影の運転者が徐々に見えてくる＝the limit（推認が消える瞬間） | still |
| S47 | ENDING | 天秤が settle・州境で protected/not に分かれる壁地図（判読不能ラベル）＝rule なお立つ | still |
| S48 | ENDING | 夜明けのハイウェイへ slow pull-back（i2v: 夜が明け光が育つ・payoff） | **motion** |

**source 集計（scene-primary）:** motion-primary **7**（S02 S04 S10 S23 S37 S41 S48）／factory-primary **3**（S06 S26 S33）／still-primary **38**。**scene-primary はカット全体の一部**で、残りは §5.1 の配分に従い CODEX_B の shotlist が 225 カット（still 101 / factory 92 / motion 32）へ機械展開する。**この表のシーン数・番号は固定（S01..S48）。**

---

# 4. 音の4層設計（ナレ / BGM / SFX / 環境音）

## 4.1 ラウドネス・voice（確定値・EP41〜47 と同一運用）

| 項目 | 確定値 |
|---|---|
| 統合ラウドネス（完成 mp4） | **-14.0 LUFS**（許容 -16〜-12） |
| True peak | **≤ -1.0 dBTP** |
| ナレ（VO）単体 | -18.0 LUFS 目標 |
| BGM ベッド（VO下・ダッキング後） | **-22.0 LUFS** |
| BGM ベッド（VO無し区間） | -17.0 LUFS |
| 環境音ベッド | -30.0 LUFS |
| ダッキング | リダクション 5.0 dB / attack 120ms / release 450ms |
| **VOICE_ID** | ElevenLabs `nPczCjzI2devNBz1zQrb` / model `eleven_multilingual_v2` / stability **0.35** / similarity_boost **0.80** / style **0** / speaker_boost **on** / **speed 1.0（明示）** |
| VO実測合格帯 | `measure_vo_wpm` で **168.0–190.0 wpm**。190超は破棄・speed 0.95 で再発注（BLOCKING） |

## 4.2 【SILENCE 1】の実装（★デジタル無音にしない・`bgm_present` を落とす）

台本の `【SILENCE 1 — 1.8s】` は**ナレの沈黙であって音の沈黙**（台本指定「Hold on the screen reading REVOKED. No music.」＝完全無音）。EP48 は明示指定が1箇所（HOOK 内）。

| 位置 | 秒 | 対応画 | 鳴らすもの |
|---|---|---|---|
| HOOK 中（"screen reading REVOKED" で保持） | **1.8** | S04→S05（ヒット画面 REVOKED／light bar） | BGM mute。**完全無音**（room tone も置かない・台本指定「No music」） |

**最長無音候補 1.8秒 << 25秒** ✓ `bgm_present` PASS。加えて **HOOK TEASER preroll（0–8.0s）は BGM 低弦のみ**（ナレなしだがデジタル無音にはしない）。

## 4.3 章ごとの BGM（1章1トラック・`build_glover_bgm_real.py`＝EP43 系を glover 用に複製・film_offset 適用・OFF=11.5）

| 区間 | 性格 | 楽器 |
|---|---|---|
| HOOK TEASER / HOOK | 低弦の不解決・夜の緊張・単音が刺す（道・打鍵・ヒット・light bar） | 低弦+単音メタル |
| OP | ブランドスティンガー（`BrandOpening` 付属） | — |
| ACT1 | 最短・現在形・抑制。刻みは疎で近い（the stop） | 低弦+疎パーカッション |
| ACT2 | 転回。法理の冷たい正対（reasonable suspicion の問い） | ピアノ+弦 |
| ACT3 | 法の荘厳・大理石。**最も遅い**。8-1 の重さと "narrow" の緊張 | 低弦+弦サステイン |
| ENDING | 解決しない和音 →「daylight」でだけ暖色（採光）に開く（a careful yes の余韻） | ピアノ+弦 |
| ENDCARD | ブランドED（`BrandEndcard` 付属） | — |

> **BGM OFF=11.5**（hookSeconds 8.0 + OPENING_SEC 3.5）＝BGM の章割り原点。`build_glover_bgm_real.py`→`composite_glover_hero.py` は film_offset 11.5 を適用（EP43 系を複製）。

## 4.4 SFX（非扇情・C5・広告安全）

| 種別 | 位置 | 音 |
|---|---|---|
| road / night highway | S01/S03/S44/S48 | 夜のハイウェイの風・遠いタイヤ・-30 LUFS |
| keystroke / cursor | S02/S45・TEASER | ラップトップのキー/カーソルの微音・-24 LUFS |
| hit / screen chime | S04・TEASER | 照合ヒットの短いチャイム・-22 LUFS（沈黙区間 S04→S05 は完全無音のため置かない） |
| light bar | S05/S10/S18/TEASER | light bar 点灯の低いブザー・-18 LUFS（サイレン鳴らしっぱなしにしない・非扇情） |
| stamp | S12/S39 | REVOKED/SUSPENDED 判子の一撃・-16 LUFS |
| scale tip | S20/S23 天秤 | 皿が傾く低い軋み・-22 LUFS |
| marble / columns | S07/S31/S33 | 大理石ホールの広いリバーブ・-30 LUFS |
| glance / reveal | S37/S41 | シルエット対比/影が晴れる微かな高域・-26 LUFS |
| dawn open | S48 | 夜明けの外気・鳥の遠音・-26 LUFS |
| impact | AE v01/t01 の数値着地 | 低域インパクト・-12 LUFS |
| tick | votetally/timeline の桁変化 | 微細クリック・-24 LUFS |
| room tone | 全編ベッド（夜の道・パトカー冷灰・大理石反響） | 広いリバーブ・-30 LUFS（**SILENCE 1 は完全無音**） |

---

# 5. ビジュアル — 素材積算（★紙芝居回避＝factory実写を必ず混ぜる・1シーン1枚）

## 5.1 素材の積算（★SPEC の値をそのまま満たす配分）

```
[0] 絵が必要な区間 = narrationSeconds 719.6（BrandOpening/Endcard/teaser は別レイヤー）
[1] 総カット = 225（SPEC）    719.6 / 225 = 3.198秒/カット  ✓ mean_shot 3.19（≤6.0）
[2] 素材内訳（★SPEC の distinct/cuts をそのまま・1シーン1枚）
    still（SDXL）    85 distinct → 101 カット（16枚が2回・69枚が1回・mean 1.19・cap 2）★各1枚生成
    factory 実写     92 distinct →  92 カット（各1回・cap 1）
    i2v モーション    16 distinct →  32 カット（各2回・cap 2）
    -----------------------------------------------
    distinct 合計   193          → 225 カット
[3] first-use share = 193 / 225 = 0.858   ✓ ≥0.70（SPEC 一致）
[4] footage_diversity distinct/total = 0.858   ✓ ≥0.40
[5] 最大使用回数: still 2 / factory 1 / motion 2   ✓ 各 cap 内
[6] 静止画占有率（★紙芝居ゲート）: still-cut 101 / 225 = 0.4489 = 44.9%   ✓ ≤45%（余裕 0.1%pt）
[7] motion coverage: (factory 92 + i2v 32) / 225 = 124/225 = 0.5511   ✓ ≥0.45
[8] factory 下限 = 719.6/30 = 24.0 → ≥24本。設計値 92本   ✓
```
> **[6] の余裕は 0.1%pt しかない。still-cut を1つ増やすと 45% を割る。still-cut は 101 で固定**（16枚だけ2回・残り69枚1回）。QC で still が 85枚を割ったら §9 の**追加は同一シーンの別プロンプト（新規 distinct）**で回復させ、**cut 数は増やさない**。**still を増やして factory を削るな。factory 92 が still-share≤0.45 を守る下限。**

## 5.2 SDXL と実写在庫の振り分け

- **SDXL（still 85・各1枚）= この事件にしか無い固有物**: 夜の道・ラップトップの打鍵/ヒット画面 REVOKED・light bar・ピックアップ車内（影の運転者）・登録票/プレート照合画面・免許証の REVOKED 判子・カンザスのプレート・officer の窓辺シルエット・courthouse の扉・suppression motion／stipulated facts の頁・第4修正のページ・天秤（a hunch↔proof）・magnifying glass over a license・"REASONABLE SUSPICION" の語・二閾値・車の鍵/複数候補シルエット・最高裁9席・8-1 バロット・意見集（Thomas/Kagan/Sotomayor）・commonsense inference のキー環・bright line・所有者≠運転者のシルエット対比・REVOKED↔SUSPENDED 判子対比・州境地図・夜明けのハイウェイ。
- **factory 実写 92 = どこにでもある周辺**: カンザスの小さな町・夜のハイウェイ ambient・courthouse 外観・列柱・大理石テクスチャ・長い廊下・夜明けの街・ambient 繋ぎ。

## 5.3 SDXL 生成量（★バリエーション0・variants 禁止）

- `ai_prompts.v001.md` = **body 85行の固有プロンプト**（still 各1枚）＋ i2v 種 **16行** ＝ **計101エントリ**（`--only S01` の `shots=` は 101）。`generate_sdxl_4k.py PD-2026-048-glover`（**`--variants 1` または指定なし**）。**`--variants 3` を書かない。**
- i2v-source = **16枚**（動きが意味を持つ絵の固有プロンプト・各1シード）。CODEX_A が Wan 2.2 A14B → RIFE 48fps で 16本生成。
- **総生成 = still 85 + i2v seed 16 = 101枚（各1回）。** factory 92 は生成せず在庫選抜。
- プロンプト実体（85本）・i2v リスト（16）・factory 選定（92）は **CODEX_A** の担当（本書 §9 は絵コンテ級の記述と共通スタイル/ネガティブの契約のみ）。

## 5.4 factory のファイル名を信じない（★必須工程・CODEX_A・BLOCKING）

> EP36: `city_surveillance_camera_dome` が実際は大聖堂。EP38: 牛が `documents_on_desk`。ラベルは検索語の記録であって中身の保証ではない。

選定した **92本すべて**を `scripts/build_footage_contact_sheet.py --ep PD-2026-048-glover --media video --dir <factory staging>` で1本1フレームのラベル付きコンタクトシートにし**全点目視**。subtype と食い違う本は差し替える。`select_glover_factory.py --verify-no-prior-overlap` で EP39〜47 の sha256 被りゼロを確認。

## 5.5 共通スタイル接尾（各 SDXL プロンプト末尾に必ず付ける・`[STYLE]`・CODEX_A と同一）

```
, cinematic still, cold nocturnal documentary grade, a dark two-lane Kansas highway at night with streaking taillights and a patrol-car dashboard laptop glowing cold, set against cold grey institutional interiors and pale marble Supreme-Court colonnade, a single patrol-steel blue accent as the one cool note, restrained and dignified symbolism, telephoto compression and frontal composition, shallow depth of field, ultra-detailed, photoreal, 4K, 16:9, fine film grain, no text, no watermark, no logo, symbolic still-life, no people, no visible face, drivers only ever as shadow or silhouette
```
> EP39〜47 との分離: 接尾に `electric blue`（EP39）・`midday suburban`（EP40）・`sodium prison corridor`（EP41）・`warrant-blue`/`navy interrogation`（EP42）・`porch-amber`/`ambulance`（EP43）・`teal-green hospital`（EP44）・`crimson overdue`（EP45）・`forest-green`（EP46）・`civil-violet`/`Texas dust`（EP47）を**1語も含めない**。EP48 の唯一の差し色は **patrol-steel `#5B8DB8`**。

## 5.6 共通ネガティブ（各 SDXL プロンプトの `Avoid:` に必ず付ける・`[NEG]`・CODEX_A と同一）

```
text, words, letters, numbers, captions, watermark, logo, readable document, legible license number, legible plate number, legible registration, legible date, real celebrity, recognizable real person, identifiable face, portrait, mugshot, likeness of a specific person, human face, Charles Glover, driver's face, human body, crying, distress, sensational, poverty porn, weapon, gun, blood, gore, violence, arrest struggle, handcuffed person, nude, bare skin, cartoon, illustration, anime, 3d render, low quality, blurry, jpeg artifacts, deformed, extra limbs, siren flare, navy interrogation room, electric blue, warrant-blue, teal-green hospital corridor, midday suburban daylight, porch amber house, ambulance, crimson overdue notice, forest-green, civil-violet, Texas dust
```
> ネガティブにも **制約違反語（"the stop was illegal", "struck down", "unconstitutional stop", "stop any car", poverty porn 語等）を書かない**（§1.3）。会社/機関ロゴが必要な絵は「blurred into an unreadable smear」で判読不能に。判例番号・日付・票数・プレート番号・氏名・年齢を画に描かない（AE/figures＝B の担当）。**運転者は影/シルエットのみ・顔なし**（C5）。**逮捕の身体的暴力・手錠された人を描かない**（広告安全・C5）。「停止は違法/覆された」に見える絵を作らない（C3）。

## 5.7 AI開示（強め・毎回・R1）

AI 生成の still・i2v が画面に出ている間、常時右下に **`AI-assisted visualization`**。Oswald 20px / `#C8CDD6` / opacity 70% / 位置 `[W-32, H-28]`。字幕帯と縦 56px 以上離す。概要欄1行: `Some visuals in this film are AI-assisted reconstructions, not photographs of the actual events.`（＋あなたの州の「plate-check に基づく交通停止と reasonable suspicion」を定めるルールを確認する中立の1行）。

## 5.8 ★A↔B 境界契約（asset_manifest スキーマ・EP39〜47 の不整合を最初から潰す）

- **接続点は `episodes/PD-2026-048-glover/05_visuals/asset_manifest.v001.json` ただ1ファイル**。A(producer)＝CODEX_A が書き、B(consumer/validator)＝CODEX_B が読む。**counts と role enum を A/B で一字一致**させる。
- **スキーマ版:** `glover_assets.v1`（固定文字列）。
- **マニフェスト配列（★A/B 同一・全エントリ public_path 必須）:** `stills` / `motion` / `factory` / `overlay` の4配列。**★全エントリを記載**（stills85＋factory92＋motion16＋overlay12・public_path 必須＝EP45事故回避）。
- **counts オブジェクト（★このキー・値で固定・A/B 一字一致）:** `{ "still_body": 85, "still_i2v_source": 16, "motion": 16, "factory": 92, "overlay": 12 }`。cuts 展開は still 101 / factory 92 / motion 32。
- **`stills[].role` enum（★この3値のみ・A/B 同一・`thumb`/`still_thumb` を作らない）:** `body` / `i2v_source` / `reject`。asset_id は body `^GLV-S\d{2}$`（S01..S85）/ i2v種 `^GLV-MS\d{2}$` / motion `^GLV-M\d{2}$`。
- **サムネは `role="body"` かつ `also_thumb=true` の body still ちょうど6枚**（別 role を作らない・追加生成しない）。**候補集合（★still 資産 ID 空間・A↔B 契約点）:** **`{S01, S04, S12, S32, S37, S48}`**（夜の道・ヒット REVOKED・免許取消判子・8-1 バロット・所有者≠運転者対比・夜明け）。A・B は同一6 asset ID に `also_thumb:true` を立てる。
- **overlay 枚数も A/B 一致**（合成レイヤー・distinct 素材に数えない）。本書設計値 **overlay: 12**（particle/light/vfx）。
- CODEX_A は manifest を書いた直後 `build_glover_asset_manifest.py --verify`（複製）で counts / role / also_thumb / overlay を突き合わせ、**A の値と B の期待が一字一致**であることを確認（不一致は BLOCKING）。**`also_thumb==true` の scene_id 集合が `{S01,S04,S12,S32,S37,S48}` で A↔B 同一**であることも検査する。

---

# 6. Remotion MGビート（FigureBeats）— ★密度下限 30 は必ずここで満たす・dochighlight 不使用・実union準拠

## 6.1 密度の設計（`glover_film.json` の `figures[]`）

`check_motion_density`: 3つを AND。**body-minutes = narrationSeconds/60 = 719.6/60 = 11.993**。

| 指標 | floor | EP48 設計値 |
|---|---|---|
| density | ≥2.5/min | figures **36 beats / 11.993 = 3.00/min** ✓（SPEC beats_floor 30 に +6） |
| coverage | ≥0.25 | 36 beats × 平均 5.4秒 = 194.4秒 / 719.6 = **0.270** ✓ |
| variety | ≥3 distinct forms | **12種**（下記） ✓ |

> **AE の 6枠は film.json に入れない**（composite 後に焼くため gate 非カウント）。**density は Remotion 側 36 beats だけで 30 を超える。** coverage が floor 0.25 に一番近いので figures の dur は 4.8–6.0s を基本にする。

## 6.2 `figures[]` の種類配分（★kind は全部小文字・同一 kind を連続させない・★dochighlight 不使用・実 FigureBeats.tsx union 準拠）

**★実 `remotion/src/components/FigureBeats.tsx` の `FigureSpec` union に実在する kind だけを使う（本書は全数照合済）。使用する12 kind（全小文字）:** `acttitle` `lowerthird` `kinetic` `votetally` `quote` `compbars` `mechanism` `probablecause` `brightline` `statemap` `carkeylock` `timeline`。**大文字は無音描画になる。** **★`dochighlight` を1件も入れない（R-DOCHL・grep 0）。免許/登録票/切符/命令は `lowerthird` の説明テキストで表す。** `comparebars` は非実在→`compbars` が正。**各 kind の必須フィールドは実 union に一致（下記）:**

- `acttitle` → `{title, kicker?, index?}`
- `lowerthird` → `{primary, secondary?, accent?}`
- `kinetic` → `{lines[], style?: 'wordpop'|'maskslide'|'emphasis', emphasisWords?[]}`
- `votetally` → `{majority, dissent, label?}`（**8-1 は `majority:8, dissent:1`**）
- `quote` → `{quote, attribution}`
- `compbars` → `{items:[{label,value,accent?}]}`
- `mechanism` → `{mechanism:'closingdoor'|'gears'|'faultsplit'}`
- `probablecause` → `{outcome?:'stall'|'cross'}`（reasonable suspicion は probable cause 未満＝**outcome "stall"** を使う）
- `brightline` → `{mode?:'draw'|'hold'|'slam'}`
- `statemap` → `{label?}`
- `carkeylock` → `{}`（プロップなし）
- `timeline` → `{events:[{year,text}]}`

| kind（小文字） | 枠数 | EP48 での用途（6制約適用） |
|---|---|---|
| `acttitle` | 3 | ACT1「THE STOP」/ ACT2「THE INFERENCE」/ ACT3「THE LIMIT」 |
| `lowerthird` | 12 | 開示 `AI-assisted visualization`（HOOK/ENDING 2回）／"KANSAS · a routine plate check"／"no traffic violation observed"／"a revoked license — not a suspension"／"the driver's identity — unconfirmed"／"The Fourth Amendment — 'unreasonable searches and seizures'"／"reasonable suspicion — not probable cause"（N04）／"owner in his sixties · driver in her twenties → suspicion dissolves"（G12・narrow）／"Kansas v. Glover · 2020 · 589 U.S. ___"（N03）／"Justice Kagan, concurring — revocation, not suspension"（N08）／"Justice Sotomayor — the lone dissent"（C4）／"not 'any car' — a sensible inference, until the facts say otherwise"（C1）／"the rule of Glover still stands" |
| `kinetic` | 4（うち emphasis 3） | 「THE NAME ON THE PLATE」／「HE NEVER SAW THE DRIVER」(["NEVER"])／「A NARROW RULE」(["NARROW"]・C1)／「SUSPICION, NOT CERTAINTY」(["SUSPICION"]・C1/C2)。**emphasisWords は1–2語＝文字切れ回避** |
| `votetally` | 1 | **8-1**（majority 8 / dissent 1・**F-VOTE**・必ず label "A NARROW RULE · THE STOP UPHELD"・R-VOTE・C4 中立） |
| `quote` | 5 | ①Thomas 標準 G09（**for the Court**・F-Q-STD）②Thomas HOLDING G10（**for the Court**・F-QUOTE-H）③Kagan G14（**concurring**・F-QUOTE-K）④Sotomayor G15（**dissenting**・F-QUOTE-S1）⑤Sotomayor G17（**dissenting**・F-QUOTE-S2）。**§1.5 APPROVED_QUOTES の逐語のみ・要約を引用符に入れない・R-QUOTE で帰属厳格** |
| `compbars` | 2 | ①owner vs others（[{"the registered owner",1},{"a spouse · child · friend · mechanic",1}]・**F-CMP**・C4 中立）②reasonable suspicion vs probable cause の閾値説明（[{"reasonable suspicion — a brief stop",1},{"probable cause — arrest or search",1}]・C2） |
| `probablecause` | 1 | outcome **"stall"**（reasonable suspicion は probable cause の閾値まで届かない＝Terry 級・N04・C2） |
| `mechanism` | 3 | `closingdoor`（the stop is made・ACT1）／`gears`（推認エンジン owner→driver・ACT2）／`faultsplit`（revoked ↔ suspended の分岐・ACT3・Kagan 限界） |
| `brightline` | 2 | `draw`（narrow rule の一本線・ACT3）／`hold`（the line the Court drew・ENDING） |
| `statemap` | 1 | label "your state · reasonable suspicion"（ENDING・州次第・C1） |
| `carkeylock` | 1 | 誰が実際に鍵を握り運転するか（ACT2・所有者≠運転者の可能性・C1/C4） |
| `timeline` | 1 | the stop → APRIL 6, 2020（F-TL・N02・年は 2020 のみ hard 表示） |
| **合計** | **36** | variety = **12 figure-kinds** ✓ ≥3 |

> **★`dochighlight` を1件も置かない（R-DOCHL）。** `graphics[]=[]`（空配列）。density は `figures+graphics+heroCuts` を合算するので figures 36 だけで floor 30 に +6。

## 6.3 配置方針（36本・§1.4 台帳の値だけを焼く・kind を分散・6制約順守・dochighlight 0件・CODEX_B と一致）

- **HOOK/OP（3）:** `kinetic`（"THE NAME ON THE PLATE"）/ `lowerthird`（`AI-assisted visualization` 開示）/ `lowerthird`（"KANSAS · a routine plate check"・**Deputy 氏名/郡は焼かない**・R-HEDGE）
- **ACT1（6）:** `acttitle`（THE STOP）/ `lowerthird`（"a revoked license — not a suspension"）/ `kinetic:emphasis`（"HE NEVER SAW THE DRIVER"・["NEVER"]）/ `lowerthird`（"no traffic violation observed"）/ `mechanism:closingdoor`（the stop is made）/ `lowerthird`（"the driver's identity — unconfirmed"）
- **ACT2（9）:** `acttitle`（THE INFERENCE）/ `lowerthird`（"The Fourth Amendment — 'unreasonable searches and seizures'"）/ `quote`（Thomas 標準 G09 → "Justice Thomas, for the Court"・F-Q-STD）/ `probablecause`（outcome "stall"・N04）/ `lowerthird`（"reasonable suspicion — not probable cause"・N04）/ `compbars`（owner vs others・F-CMP・C4）/ `mechanism:gears`（推認エンジン）/ `kinetic`（"A PROBABILITY, OR A FACT?" ※emphasis なし wordpop）/ `carkeylock`（誰が鍵を握るか・F-KEY）
- **ACT3（13）:** `acttitle`（THE LIMIT）/ `lowerthird`（"Kansas v. Glover · 2020 · 589 U.S. ___"・N03）/ `votetally`（**F-VOTE 8-1**・label "A NARROW RULE · THE STOP UPHELD"・R-VOTE）/ `quote`（Thomas HOLDING G10 → "Justice Thomas, for the Court"・F-QUOTE-H）/ `brightline`（"draw"・narrow rule）/ `lowerthird`（"owner in his sixties · driver in her twenties → suspicion dissolves"・G12）/ `kinetic:emphasis`（"A NARROW RULE"・["NARROW"]・C1）/ `quote`（Kagan G14 → "Justice Kagan, concurring"・F-QUOTE-K）/ `mechanism:faultsplit`（revoked ↔ suspended）/ `quote`（Sotomayor G15 → "Justice Sotomayor, dissenting"・F-QUOTE-S1）/ `lowerthird`（"Justice Sotomayor — the lone dissent"・C4）/ `quote`（Sotomayor G17 'paved the road' → "Justice Sotomayor, dissenting"・F-QUOTE-S2）/ `timeline`（the stop → APRIL 6, 2020・F-TL・N02）
- **ENDING（5）:** `kinetic:emphasis`（"SUSPICION, NOT CERTAINTY"・["SUSPICION"]・C1/C2）/ `lowerthird`（"not 'any car' — a sensible inference, until the facts say otherwise"・C1）/ `statemap`（"your state · reasonable suspicion"・C1）/ `brightline`（"hold"・the line the Court drew）/ `lowerthird`（開示 `AI-assisted visualization` 再掲）

> **compbars 2枠が §6.2 の②（閾値説明）を含む。②は ACT2 の `compbars`（owner vs others）と別秒に置き、同一 kind を連続させない**（②は ACT2 の probable-cause 説明区間、または ACT3 の narrow 説明の直前に配置。CODEX_B は 20秒超の平坦区間ゼロになるよう分散）。

## 6.4 配置ルール

1. **AE の 6区間（§7）と1秒でも重ならない**（`validate_glover_beats.py`＝validate_caniglia_beats.py を複製・両方突き合わせ）。
2. 幕あたり配分: HOOK/OP=3 / ACT1=6 / ACT2=9 / ACT3=13 / ENDING=5（ACT3 が最長 201.5s なので厚め）。
3. **同じ kind を連続させない**（`quote` の直後に `quote` を置かない＝ACT3 は quote の間に brightline/lowerthird/kinetic/mechanism を挟む）。
4. 1枠 **4.8–6.0秒**。
5. ACT3 の説明区間に `votetally`＋`quote`×4＋`timeline`＋`mechanism`＋`brightline`＋`lowerthird` を分散し 20秒超の平坦区間をゼロに。
6. `quote` は**逐語のみ**（要約を引用符に入れない・R-QUOTE）。**Thomas＝for the Court／Kagan＝concurring／Sotomayor＝dissenting** を厳格帰属。
7. `figures[].*text*`/`lines[]`/`label`/`quote`/`primary`/`secondary` は `facts_lock` 検査対象（「illegal/struck down/stop any car/probable cause required」・Deputy 氏名/郡/プレート/車種・台帳外数値・**dochighlight** を出さない）。
8. **8-1 を焼く votetally は同一 payload に "A NARROW RULE / UPHELD / REASONABLE" を必ず持つ（R-VOTE）。** Sotomayor/Kagan 逐語 payload は必ず attribution "dissenting"/"concurring"（R-QUOTE）。

## 6.5 密度の最終検算

```
Remotion figures 36（film.json 内・graphics 空）
  density  = 36 / 11.993 = 3.00/min   ✓ ≥2.5（SPEC beats_floor 30 → 36 で +6）
  coverage = 194.4s / 719.6 = 0.270    ✓ ≥0.25
  variety  = 12 forms                  ✓ ≥3
  dochighlight count = 0               ✓ R-DOCHL（grep 0）
  全 kind は実 FigureBeats.tsx union に実在（acttitle/lowerthird/kinetic/votetally/quote/compbars/mechanism/probablecause/brightline/statemap/carkeylock/timeline） ✓
AE hero 6枠は composite 後・gate 非カウント（上乗せの決め所）
```

---

# 7. After Effects ヒーロービート（6枠）— ★AEカードは密度に数えられない

## 7.1 大原則（★EP39/40 の致命傷を回避）

`check_motion_density` は **film.json の `figures` だけ**を数える。AE の 6枠は本編 mp4 に composite された後に焼き込まれるため gate は 0 カウント。→ **密度下限 30 は §6 の Remotion figures（36本）で満たす。** AE はその上に載る「決め所の数値/引用タイポ」。

## 7.2 パイプライン（EP45 cleveland 修正版を glover 用に複製・実測済み）

```
[1] Remotion で本編完成 → glover_final_bgm.v001.mp4（音声ミックス済み・build_glover_bgm_real.py→film_offset 11.5 適用）
[2] scripts/ae/build_glover_hero_cards.py（＝build_cleveland_hero_cards.py の修正版を複製・repo path 出力・実測フィット・引用折返し）が beats.json と glover_hero.jsx を生成
[3] AfterFX -noui -r glover_hero.jsx → 各ビートを 1920x1080@30fps の不透明 mp4 で書き出し（aerender 二段構成: AfterFX で .aep 構築 → aerender で描画）
[4] scripts/ae/composite_glover_hero.py（＝composite_cleveland_hero.py を複製）が ffmpeg overlay + enable='between(t,start,end)' で焼き込み（film_offset 適用）
[5] 出力 → glover_final_bgm.v002_ae.mp4（v001 は絶対に上書きしない）
```

## 7.3 AEカードデッキ（★6枚＝ブリーフ§6 VERBATIM・§1.4 の確定数値のみ・6制約適用・accent #5B8DB8）

> **★レイアウトは複製元 `build_cleveland_hero_cards.py` が実装する6種のみ**（`ACT_TITLE_CARD`/`CENTER_STACK`/`MONEY_STACK`/`SPLIT_COMPARE`/`QUOTE_CARD`/`VOTE_SPLIT`）。**★`DATE_STAMP` と `SEAM_TRANSITION` は実装に存在しない（JSX は `else throw "unsupported layout"`）＝使うと AE ビルド即クラッシュ。日付カードは `CENTER_STACK`（下段テキストに `589 U.S. ___` / `SUPREME COURT`）で表現する（CODEX_B が正典）。** **この表と CODEX_B のデッキは id・レイアウト・N-ID が完全一致**（`validate_glover_beats` が両方を突き合わせる）。上記6種以外は使わない。**EP48 は 8-1 が台帳にあるので `VOTE_SPLIT` を使用。`ACT_TITLE_CARD`（幕頭は Remotion `acttitle` が担う）/ `MONEY_STACK`（金額なし） は §7.3 では未使用。** variety は使用4レイアウト（VOTE_SPLIT / CENTER_STACK / SPLIT_COMPARE / QUOTE_CARD＝4種）で ≥3 を満たす。

| id | レイアウト（実装済み8種） | hero（主表示） | top / sub / bottom / place / attribution | 数値ID | 背景（象徴のみ・顔なし） | 尺 |
|---|---|---|---|---|---|---|
| **c01** | **CENTER_STACK** | **REASONABLE SUSPICION** | top: **THE STANDARD FOR A BRIEF STOP** / bottom: **NOT PROBABLE CAUSE, NOT CERTAINTY** | N04 | 第4修正のページ／天秤 | 6.0 |
| **f01** | **SPLIT_COMPARE** | **THE OWNER IS PROBABLY DRIVING / UNLESS THE OFFICER KNOWS OTHERWISE** | top: **A COMMONSENSE INFERENCE** / bottom: **IT DISSOLVES WITH CONTRARY INFORMATION** | N07 | 左=登録票 / 右=所有者≠運転者のシルエット対比 | 7.0 |
| **v01** | **VOTE_SPLIT** | **8 – 1** | top: **THE STOP WAS REASONABLE** / bottom: **A NARROW RULE — UPHELD 8-1** | N01 | 最高裁の9席・列柱 | 6.5 |
| **t01** | **CENTER_STACK** | **APRIL 6, 2020** | 下段: **SUPREME COURT · 589 U.S. ___** | N02/N03 | 大理石の階段（判読困難） | 5.0 |
| **q01** | **QUOTE_CARD** | **"...PAVED THE ROAD TO FINDING REASONABLE SUSPICION BASED ON NOTHING MORE THAN A DEMOGRAPHIC PROFILE"** | attribution: **JUSTICE SOTOMAYOR, DISSENTING** | N06 | 反対意見側の開いた意見集 | 8.0 |
| **k01** | **SPLIT_COMPARE**（任意） | **REVOCATION, NOT SUSPENSION** | top: **WHAT MADE THE INFERENCE REASONABLE** / bottom: **JUSTICE KAGAN, CONCURRING** | N08 | 左=REVOKED 判子 / 右=SUSPENDED 判子 | 6.5 |

> **★行順＝start 昇順（時系列）:** `c01`(ACT2 reasonable suspicion) < `f01`(ACT2/3 owner probably driving) < `v01`(ACT3 8-1) < `t01`(ACT3 判決日) < `q01`(ACT3 Sotomayor 逐語) < `k01`(ACT3 Kagan 限界)。**start は §7.4 beats.json で section 窓からオフセットで算出しクランプ**するため、**本番 rendered base の秒で単調増加・重複ゼロ**を `validate_glover_beats` が保証する。**この id・レイアウト・N-ID は CODEX_B デッキと一字一致。**
> **★q01（Sotomayor QUOTE_CARD）の attribution は "JUSTICE SOTOMAYOR, DISSENTING"（R-QUOTE・C4）。逐語（G17）を1字も要約しない。Sotomayor を Court に帰属させたら FAIL。** hero は§1.4 N06 の逐語一致（大小無視・表示は全大文字）。
> **★v01（VOTE_SPLIT 8-1）は bottom に "UPHELD" と "A NARROW RULE"（R-VOTE/C1）を必ず別レイヤーで焼く。「illegal / struck down / overturned / stop any car」を書かない。** 8-1 を中立に（どちらが正義かを断じない・C4）。
> **★f01 の bottom "IT DISSOLVES WITH CONTRARY INFORMATION" と hero 下段 "UNLESS THE OFFICER KNOWS OTHERWISE" が narrow を保証（C1）。「THE OWNER IS PROBABLY DRIVING」を単独で焼かない（必ず限界の対語を同居）。**
> **★c01 は "NOT PROBABLE CAUSE" を必ず焼く（C2・R-STANDARD）。probable cause を「必要」と読める文言にしない。**
> **どのカードにも「illegal / struck down / overturned / the stop was wrong / stop any car / probable cause required」・Deputy 氏名/郡/プレート/車種・dochighlight を書かない。** 数値ID＝台帳（§1.4）と一致必須。カウント終了から区間終端まで最低 1.20秒ホールド。em-dash は本文表示の `—` と異なり **beats.json ラベルでは ASCII `-` に置換**（AE の豆腐回避・§7.6）。

### 検算

```
[1] 6区間・本番 start 単調増加・重複ゼロ（build_glover_hero_cards.py が section 窓オフセットで算出）
[2] HOOK TEASER(0–8.0) / HOOK(8.0–...) / BrandOpening / BrandEndcard に1秒も重ならない
[3] 合計 = 6.0+7.0+6.5+5.0+8.0+6.5 = 39.0秒 / 740.1 = 5.3%   ✓ 過剰でない
[4] レイアウト種類 = CENTER_STACK, SPLIT_COMPARE, VOTE_SPLIT, QUOTE_CARD = 4種（全て実装済み6種内）   ✓ ≥3
[5] figures[] 36枠と1秒でも重ならない（validate_glover_beats.py が両方突き合わせ）
[6] dochighlight/comparebars レイアウトは存在しない（8種のみ）   ✓ R-DOCHL
[7] R-VOTE: v01 に "UPHELD/A NARROW RULE" / R-STANDARD: c01="NOT PROBABLE CAUSE" / R-QUOTE: q01="dissenting" k01 bottom="concurring"   ✓
```

## 7.4 `beats.json`（`08_edit/ae_hero/beats.json`・`schema_version: "glover_beats.v1"`）

各 beat に `id` / `layout` / `start` / `end` / `dur` / `still`(象徴 or null) / `hero` / `top` / `bottom` / `sub` / `place` / `caption`(**改行禁止・最大50字**) / `value` / `numKeys` / `blend_mode`(既定 "overlay") / `required` / `out` / `attribution`(**QUOTE_CARD=q01 は必須**・§1.4 と一致・R-QUOTE)。**区間の秒は本番 rendered base（narration_index 由来）に一致させ、section 窓からオフセットで算出しクランプ。offset は hookSeconds(8.0)+3.5=11.5。beats を実発話に再アンカー。** **8-1 は文字列（"8 - 1"）で焼く（票カウントの count-up は "0→8" / "0→1" の1桁のみ可）。**

## 7.5 レイアウト定義・色定数（EP45/47 を踏襲・色のみ EP48 値・CODEX_B と一致）

**共通レイヤースタック（下→上）:** L9 黒ソリッド → L8 静止画（scale fill→fill×1.08・drift）→ L7 グレードウォッシュ（**夜のハイウェイ near-black** `addSolid([0.047,0.063,0.078])`＝NIGHT / MULTIPLY / opacity 30）→ L6 羽根付き楕円ビネット → L5 グロー（下中央 patrol-steel 差し ADD）→ L4 ライトスイープ（`"ADBE Rotate Z"`=18）→ L3 上ラベル（Oswald）→ L2b アクセントライン（ACCENT steel・scaleX ワイプ・`motionBlur=true`）→ L2 主数値/主文字（Anton・ACCENT・`motionBlur=true`）→ L1b 下ラベル → L1 字幕ロワーサード → **L0b AI開示テキスト（`AI-assisted visualization`・Oswald 20px・SILVER `#C8CDD6`・opacity 70%・右下 `[W-32, H-28]`・全カード常時焼き＝R1）** → L0 黒シームディップ（head/tail 各4フレーム）。

**★EP48 色定数（0..1 float・patrol-steel レーン色。EP41 gold / EP42 warrant-blue / EP43 amber / EP44 teal / EP45 crimson / EP46 green / EP47 civil-violet を流用禁止・CODEX_B と一致。★ACCENT は RGB タプルで指定＝hex コメントだけ変えない）:**
```python
ACCENT = [0.357, 0.553, 0.722]  # #5B8DB8 patrol-steel — 数値・下線・唯一の差し色
WHITE  = [0.961, 0.969, 0.980]  # #F5F7FA
SILVER = [0.784, 0.804, 0.839]  # #C8CDD6（開示テキスト）
INK    = [0.039, 0.039, 0.047]  # #0A0A0C 近黒ルート（サムネ bg と一致）
NIGHT  = [0.047, 0.063, 0.078]  # #0C1014 夜のハイウェイ near-black ウォッシュ
STEEL  = [0.102, 0.125, 0.157]  # #1A2028 パトカー冷灰
MARBLE = [0.204, 0.212, 0.231]  # #34363B 大理石（ACT3）
```
**フォント:** 数値/主文字 = **Anton Regular** / ラベル・字幕 = **Oswald Medium**。`getFontsByFamilyNameAndStyleName` で厳格解決（miss は throw・フォールバック禁止）。テキスト幅は **`sourceRectAtTime(t,false).width` で実測**（advance-width 推定禁止＝EP40 文字切れの原因・ブリーフ§5）。**`v01` の "8 - 1" を ACCENT steel、"UPHELD/A NARROW RULE" を WHITE。`v01` の "UPHELD"・`q01` の attribution・`c01` の "NOT PROBABLE CAUSE"・`f01` の "UNLESS THE OFFICER KNOWS OTHERWISE" は削除禁止。**

**カウント型:** 8-1 は "8 - 1" の文字列（count-up は "0→8" / "0→1" の1桁のみ可）＋ impact SFX。**停止を "illegal/struck down" とするラベルを一切作らない（R-VOTE）。probable cause を「必要」と読めるラベルを作らない（R-STANDARD）。**

## 7.6 このマシン固有の罠（★1つ忘れると無言で品質が落ちる・EP42-45 全項を glover に適用）

フォント解決の例外ラップ（`psName()`・allFonts の array-LIKE ラッパーを unwrap）／spatial ease は配列次元1（`prop.isSpatial ? 1 : ...`）／OM=`"H.264 - レンダリング設定を一致 - 15 Mbps"`・RS=`"最良設定"`（英語名は try/catch フォールバック）／`app.newProject()` を headless で使わない（同名 `GLOVER_` コンプを防御削除）／`layer.motionBlur=true` を動くレイヤー個別に／回転は `"ADBE Rotate Z"`／改行は1行厳守（SPLIT_COMPARE/VOTE_SPLIT の左右2値は別レイヤー・改行禁止・引用は折返しヘルパで複数行）／em-dash は `-`／inPoint と outPoint 両方設定／`item.mainSource.conformFrameRate = 30`／実行パス `C:\Program Files\Adobe\Adobe After Effects 2026\Support Files\AfterFX.exe`／`proj.gpuAccelType = GpuAccelType.SOFTWARE`／ビルド ~100–120秒・完了マーカー `render/_build_ok.txt` をポーリング（タイムアウト≥300秒）・末尾で `app.quit()`／**aerender 前に `.aep` mtime > `.jsx` を assert**（ブリーフ§5・.aep が古いと前ビルドを焼く事故）。

## 7.7 コンポジタ（`scripts/ae/composite_glover_hero.py`・SKIP 4条件を1つも削らない）

`BASE = glover_final_bgm.v001.mp4` / `OUT = glover_final_bgm.v002_ae.mp4`（v001 不変）。SKIP: (1) `render/<id>.mp4` 不在 / (2) 解像度≠1920x1080 / (3) 実測尺 `< dur-0.3` / (4) `beat.end > base_dur`。ffmpeg: `overlay=0:0:eof_action=pass:enable='between(t,start,end)'` / `-c:v libx264 -preset slow -crf 16 -pix_fmt yuv420p -colorspace bt709 -c:a copy`。**出荷済みを絶対に上書きしない。film_offset 11.5 を適用する。**

---

# 8. レイヤー構成 と ゾーン分離（★主役の裏に最低4層）

## 8.1 本編カットのレイヤー構成（下→上・主役 L4 の裏に L1/L2/L3/L3b = 4層）

| L | 名前 | EP48 の値 |
|---|---|---|
| **L0** | ルート背景 | `#0A0A0C`（INK） |
| **L1** | グラデ背景 | `radial-gradient(120% 120% at 50% 40%, #0C1014 0%, #0B0E12 45%, #0A0A0C 100%)`（夜のハイウェイ near-black。ACT3 のみ大理石寄り `#34363B` にシフト・パトカー車内は `#1A2028`） |
| **L2** | グリッド/ライン | 縦横 64px の反復線＋放射マスク＋ドリフト。`repeating-linear-gradient(0deg/90deg, #5B8DB818 0px 1px, transparent 1px 64px)`、`translateY 0→48px` / `Easing.inOut(Easing.sin)`（等速禁止） |
| **L3** | グロー | 単一 patrol-steel の差し。`radial-gradient(closest-side, #5B8DB866 0%, #5B8DB818 45%, transparent 75%)`、`filter: blur(28px)`。位置は幕で移動（道→ラップトップ→light bar→天秤→大理石→夜明け） |
| **L3b** | 大理石の光帯/ビネット | ACT3 は歴史/収斂の光帯（`linear-gradient(100deg, transparent, #5B8DB822, transparent)` を横に slow drift）、他幕は羽根ビネット。`translateX` を `Easing.inOut(Easing.sin)` で微動（静止フレームゼロ） |
| **L4** | 主役（still / i2v / factory） | §10 のモーション（Ken Burns/parallax/i2v） |
| **L5** | テロップゾーン（上/中央・figures） | §8.2 |
| **L6** | 字幕ゾーン（下部帯） | §8.2 |

> **主役（L4）の裏に L1/L2/L3/L3b = 4層**（グラデ背景・グリッド/ライン・グロー・光帯/ビネット）で CLAUDE.md「最低3レイヤー」＋タスク「最低4層」を満たす。**各層は §3.1b の通り常に微動（静止フレームゼロ）。**

## 8.2 ゾーン分離（一度も重ねない）

| ゾーン | 縦位置（1080基準） | スタイル |
|---|---|---|
| テロップ見出し | `y=96–260` | Oswald 64px / `#F5F7FA` / letterSpacing 4 |
| 中央テロップ / figures | `y=420–660` | §6 |
| 出典テロップ（アクセントライン） | `y=742–786` | Oswald 28px / patrol-steel `#5B8DB8` 3px 下線 |
| 字幕帯 | `y=872–1010` | 白 `#FFFFFF` + `textShadow:0 0 6px #000,0 2px 4px #000` / 半透明黒帯 `rgba(6,8,10,0.62)` / ≤2行・1行≤42字 / 54px / lineHeight 1.28 |
| AI開示 | `y=1024–1052`（右下） | Oswald 20px / `#C8CDD6` / opacity 70% |

**Caption QC:** ナレ一致 ≥99%（faster-whisper 強制アライン）/ `.srt` カバー ≥95% / キュー 1.0–6.0秒 / CPS ≤17 / 単語割り禁止 / 1語孤立キュー禁止 / ズレ ≤120ms。**【SILENCE 1】区間と HOOK TEASER 無音区間には字幕キューを置かない。**

---

# 1.5 APPROVED_QUOTES（★逐語ロック・R-QUOTE の参照表・`facts_lock` はこの表の逐語のみ許容）

> **すべて Cornell LII 18-556 一次照合済（facts G09/G10/G12/G14/G15/G16/G17）。1字も改変・要約しない。表示は全大文字化してよいが語順・語は不変。帰属は下記固定。** AE は q01 に P-S2 を、figures は 5 quote に P-STD/P-H/P-K/P-S1/P-S2 を使う。

| quote id | 逐語（VERBATIM・引用符内） | attribution（固定） | 出典 | 使用先 |
|---|---|---|---|---|
| **P-STD** | considerably less than proof of wrongdoing by a preponderance of the evidence, and obviously less than is necessary for probable cause | **Justice Thomas, for the Court** | G09 | figures F-Q-STD（ACT2） |
| **P-H** | When the officer lacks information negating an inference that the owner is driving the vehicle, the stop is reasonable. | **Justice Thomas, for the Court** | G10 | figures F-QUOTE-H（ACT3） |
| **P-K** | Consider, for example, if Kansas had suspended rather than revoked Glover's license. | **Justice Kagan, concurring** | G14 | figures F-QUOTE-K（ACT3） |
| **P-S1** | In upholding routine stops of vehicles whose owners have revoked licenses, the Court ignores key foundations of our reasonable-suspicion jurisprudence and impermissibly and unnecessarily reduces the State's burden of proof. | **Justice Sotomayor, dissenting** | G15 | figures F-QUOTE-S1（ACT3） |
| **P-S2** | The majority today has paved the road to finding reasonable suspicion based on nothing more than a demographic profile. | **Justice Sotomayor, dissenting** | G17 | figures F-QUOTE-S2（ACT3）／AE q01（"…paved the road…" 断片・先頭省略記号可） |

> **★帰属の厳格性（R-QUOTE・C4）:** Sotomayor/Kagan の逐語を **Court（多数意見）に帰属させたら FAIL**。Thomas の逐語は "for the Court"。**AE q01 の hero は P-S2 の "...paved the road to finding reasonable suspicion based on nothing more than a demographic profile"（先頭 "..." の省略は可・以降は逐語）。** 要約を引用符に入れたら FAIL。

---

# 9. 絵コンテ（★48シーン・象徴のみ・6制約・Glover/Deputy 非人物化・顔なし・CODEX_A が 85本プロンプトへ展開する原図）

## 9.1 パーサ契約（★CODEX_A が `ai_prompts.v001.md` を書くときの形式・`read_prompts()` が読む2行形式）

```
- `S01.png`
<positive prompt> ... [STYLE] Avoid: <negative>
```
- **1行目:** `` - `S01.png` ``（バッククォート囲み・行末は `.png` 直後）。プロンプトを同じ行に書かない。
- **2行目:** 正プロンプト → `[STYLE]`（§5.5）→ `Avoid:` → 負プロンプト（§5.6）。
- 配置先: **`episodes/PD-2026-048-glover/04_scenes/ai_prompts.v001.md`**。生成: `.venv/Scripts/python.exe scripts/generate_sdxl_4k.py PD-2026-048-glover`（**variants 指定なし＝1枚**）。
- 出力: `H:\pd-media\assets\ai\glover\S01.png …` ＋ `remotion/public/glover/`。長辺 ≥3840 で冪等スキップ。
- **★body 85本＝85行**（still 各1枚）＋ **i2v 種 16行**（M01_src..M16_src）＝ `ai_prompts.v001.md` は計 **101 エントリ**。CODEX_A は書いた直後 `--only S01` で `shots=` が **101** に達しているか（2行形式が壊れていないか）を確認。**プロンプト実体（85本）は CODEX_A が正典**（本節は絵コンテ級の原図）。

## 9.2 絵コンテ級ショット記述（Sid ごと・カメラ/モーション/象徴/制約。CODEX_A はこれを固有プロンプトに翻訳）

> **全ショット共通:** 顔・身体・肖像なし（R1/C5）。Charles Glover/Deputy を個人として描かない（象徴・物・影・シルエットのみ）。**運転者は必ず影 or シルエット**（顔を出さない）。読める文字を作らない（redacted/illegible）。判例番号・日付・票数・プレート番号・氏名・年齢を描かない。夜のハイウェイの冷たい闇＋パトカーの冷灰＋冷たい大理石＋唯一の差し色 patrol-steel。**「停止は違法/覆された」に見える絵を作らない**（C3）。**「どんな車でも停められる」に見える威圧的な絵を作らない**（C1）。最高裁の列柱/9席＝8-1 UPHELD（NARROW）の場。天秤は推認 vs 個別的疑いの中立対比（C4）。**逮捕の身体的暴力・手錠された人を描かない**（広告安全・C5）。

| Sid | カメラ/レンズ | 象徴（動き） | 制約メモ |
|---|---|---|---|
| S01 | 引き・夜の道路 | カンザス片側二車線の夜の道・ヘッドライトの流れ | C5: 人物なし |
| S02 | 接写・車内 | ラップトップにプレート番号が打鍵（i2v: cursor/keys） | C6: 番号は判読不能 |
| S03 | 引き・道路 | 通り過ぎるピックアップのテールランプ | C1: 違反なし |
| S04 | 正対・画面 | ヒット画面が REVOKED に解決（i2v: 文字確定） | C3/C6: 反転の瞬間・番号ぼかし |
| S05 | 正対・静止 | パトカーの light bar（SILENCE 1.8s） | 後で S48 と対 |
| S06 | 引き・外 | カンザスの小さな町・二車線ハイウェイ（factory） | — |
| S07 | 正対・push-in | 最高裁の淡い大理石列柱＝2020 の答え | C3: 最高裁の場 |
| S08 | 寄り＋奥行き | 手前にプレート・奥に遠い最高裁列柱 | 小さなプレート→最高裁の距離 |
| S09 | 俯瞰・車内 | ピックアップ車内・運転者は影・手元のみ | **C5: 運転者は影・顔なし** |
| S10 | 正対・夜路肩 | 後方に付くパトカーの light bar 点灯（i2v: 点灯） | C5: 非扇情・サイレン鳴らしっぱなしにしない |
| S11 | 接写・画面 | ラップトップの登録票/プレート照合（所有者名欄ぼかし） | C6: 判読不能 |
| S12 | 接写・机上 | 免許証の REVOKED の判子 | C1: 取消（suspension でない） |
| S13 | 接写 | カンザスのプレート接写・夜露 | C6: 番号ぼかし |
| S14 | 逆光・窓辺 | officer の影/後ろ姿（手元のみ・顔なし） | C5: 人物化しない |
| S15 | 正対・入口 | 平凡なレンガの courthouse の扉 | — |
| S16 | 俯瞰・机上 | suppression motion の紙（判読不能） | C6: 停止を争う |
| S17 | 俯瞰・机上 | stipulated facts の署名頁（判読不能） | C6: 両者合意 |
| S18 | 正対・路面 | 路面に落ちる light bar のグロー（停止の凍結） | ACT1 締め |
| S19 | 接写・机上 | 開いた第4修正のページ（"unreasonable…" 核・判読最小） | C6: 4A の判定 |
| S20 | 正対・天秤 | 天秤の左に a hunch・右に proof | **C2/C4: 基準の重さ・中立** |
| S21 | 接写 | 免許証の上の magnifying glass | C2: 運転者を確かめる/確かめない |
| S22 | 接写・硬光 | 大きな語 "REASONABLE SUSPICION" の抽象 | C2: 中間地点（probable cause でない） |
| S23 | 正対・天秤 | 天秤が傾く（i2v: tip） | C4: どちらへ傾くか（中立） |
| S24 | 俯瞰 | probable cause ↔ reasonable suspicion の二閾値（判読不能ラベル） | C2: 二つの閾値 |
| S25 | 接写・机上 | 登録票の所有者名欄（ぼかし） | C6: 名前 vs 人 |
| S26 | 引き・廊下 | 冷光の長い courthouse 廊下（factory） | — |
| S27 | 俯瞰 | citation form ↔ 画面の名前 | プレートの確率 vs 運転者の事実 |
| S28 | 俯瞰 | 運転者候補の空のシルエット/複数の鍵（配偶者・子・友人・整備士） | **C1: 所有者以外の可能性・顔なし** |
| S29 | 接写 | 手から手へ渡される車の鍵 | 誰が実際に運転するか |
| S30 | 引き・道路 | あらゆる運転者が通る空の夜の道 | 普遍性（ACT2 締め） |
| S31 | 正対・対称 | 最高裁の9席のベンチ（荘厳・最も遅い） | C3: 8-1 の場 |
| S32 | 正対 | 8-1 の投票が "one" で解決するバロット | **C1/C3/C4: UPHELD/NARROW 対語・votetally は figures** |
| S33 | 正対・列柱 | 夜の最高裁の列柱・大理石（factory） | C3: 最高裁の場 |
| S34 | 机上・接写 | 開いた意見集の逐語行（Thomas HOLDING・判読不能） | C3: 逐語は figures F-QUOTE-H・帰属 for the Court |
| S35 | 接写 | commonsense inference＝キー環と wheel | C1: 所有者が運転する日常の推認 |
| S36 | 大理石面 | 一本の清い線＝narrow rule（bright line） | C1: 明確だが狭い規則 |
| S37 | 正対・対比 | 所有者≠運転者のシルエット対比（60代 vs 20代・i2v: 対比が立つ） | **C1/C5: 顔なし・推認消滅の象徴** |
| S38 | 机上 | Kagan 補足の開いた意見集（判読不能） | **C4: Kagan 逐語は figures F-QUOTE-K・帰属 concurring** |
| S39 | 接写・机上 | REVOKED の判子 ↔ SUSPENDED の判子の対比 | C1: 限界の分岐（mechanism faultsplit） |
| S40 | 机上 | Sotomayor 反対の開いた意見集（判読不能） | **C4: Sotomayor 逐語は figures F-QUOTE-S1/S2・帰属 dissenting** |
| S41 | 正対・寄り | 一目で運転者が見え推認が消える（i2v: 影が晴れる・シルエットのみ） | **C1/C5: 顔は出さない・推認消滅** |
| S42 | 俯瞰 | 8票に1票が届かない象徴（判読不能） | C4: lone dissent・負けた側 |
| S43 | 接写・大理石 | 最高裁が引きなお消していない一本の線 | C1: the line drawn |
| S44 | 引き・夜のドライブウェイ | 自分の車に戻る＝あなたの車 | 現在形・payoff 起点 |
| S45 | 接写・車内 | プレートが再びラップトップに打鍵される | あなたのプレート |
| S46 | 正対・寄り | 影の運転者が徐々に見えてくる＝the limit | **C1/C5: 顔なし・推認が消える瞬間** |
| S47 | 地図・引き | 天秤 settle・州境で protected/not に分かれる壁地図（判読不能） | C1: 州次第・rule なお立つ |
| S48 | 引き・pull-back | 夜明けのハイウェイへ光が育つ（i2v: 夜が明ける） | C5: 人物なし・payoff |

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
**0.5s 刻み方針:** 225カットの境界は **`QUANT`=15フレーム（0.5秒）にスナップ**して配置する。各カット長は `CUT_MIN`〜`CUT_MAX`、平均 `CUT_MEAN`。ACT3 は最も遅く（長カット寄り・6.0s 近辺を多用）、ACT1 は速く（1.0–2.5s の断片・現在形）、HOOK TEASER は最速（~1.3s cut）。CODEX_B は shotlist の各 span 端を 15f グリッドに丸める。

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
対象（fast move）: **HOOK TEASER の light bar/フラッシュ**、**S04**（ヒット画面 REVOKED 確定）、**S10**（light bar 点灯）、**S23**（天秤 tip）、**S36**（bright line draw）、**S37**（所有者≠運転者シルエット対比）、**S41**（推認消滅）、および §6 の `votetally`/`timeline` 桁変化・幕頭 `acttitle`・`kinetic:emphasis` の切れ上がり。**S01/S07/S31（荘厳 push-in）・S05/S48（light bar/夜明け）・Ken Burns には Trail をかけない**（無駄な残像・扇情を避ける・C5）。

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

# 11. オープニング（OP）設計 — 完全仕様（`OpeningGlover`・fps=60・CLAUDE.md §1–5 全項目）

## 11.1 秒数ベースのタイムライン（fps=60・「フレーム」は全て `Math.round(60 × 秒)`・直書き禁止・0.5s 刻み方針で全区間記述）

```ts
const FPS_OP = 60; const F = (s:number)=>Math.round(FPS_OP*s);   // 総 180f = F(3.0)
```

| 秒 | フレーム | 起きること（EP48 signature = 夜のハイウェイにプレート照合＋patrol-steel の差し） |
|---|---|---|
| 0.00–0.10 | f0–6 | 画面 `#0A0A0C`。**L1** グラデ opacity 0→1（0.40s）＋ **scale 1.08→1.00** を 180f で（`Easing.out(Easing.cubic)`）。opacity 単独でなく scale 併用 |
| 0.10–0.15 | f6–9 | **L6 ロゴ**（`hasLogo`）左上 `top:64/left:72` に spring 出現。scale 0.4→1.0・opacity 0→1（併用・`damping:14,mass:0.9`） |
| 0.15–0.25 | f9–15 | **L2** グリッドが spring（`{damping:200,mass:1,durationInFrames:F(0.8)=48}`）で reveal。最終 opacity=`gridReveal*0.18`。全体を 180f で `translateY 0→48px`（`Easing.inOut(Easing.sin)`） |
| 0.25–0.30 | f15–18 | **L3** patrol-steel のグローが spring（`{damping:18,mass:1.2}`）＝ラップトップ/light bar の差し。scale 0.6→1.15 / opacity 0→0.85（併用）。`filter:blur(28px)` |
| 0.30–0.86 | f18–52 | **L4 主役タイトル**が1文字ずつ切れ上がる（`overflow:hidden` マスク）。各文字 spring（`{damping:16,mass:1}`）で `translateY 110%→0`、opacity=`interpolate(sp,[0,0.25],[0,1])`。**スタッガー=`F(0.04)=2フレーム/文字**。全体を `Trail`（`layers=6,lagInFrames=1.2,trailOpacity=0.45`）で包む |
| 0.55–1.15 | f33–69 | **L2b steel の光ライン**（EP48固有＝青の帯がタイトル背後を横切る＝light bar）。中央から `scaleX 0→1`＋`opacity 0→0.55`（spring `{damping:22,mass:1.1}`, `transformOrigin:'center'`）。patrol-steel。opacity 単独禁止で scaleX 併用 |
| 0.95–1.35 | f57–81 | **L5a** steel の下線が左から `scaleX 0→1`（spring `{damping:16,mass:0.8}`, `transformOrigin:'left center'`）。240×6px・`boxShadow:0 0 24px #5B8DB8aa` |
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
| L2b steel の光 | scaleX 0→1 / opacity 0→0.55 | spring | `{damping:22,mass:1.1}`・origin center |
| L5a 下線 | scaleX 0→1 | spring | `{damping:16,mass:0.8}`・origin left |
| L5b サブ | translateY 24px→0 / opacity | spring | `{damping:20,mass:1}` |
| L6 ロゴ | scale 0.4→1.0 / opacity | spring | `{damping:14,mass:0.9}` |

> **全 opacity が translateY/scale/scaleX と対。等速線形を1箇所も使わない。**

## 11.3 レイヤー構成（下→上・主役 L4 の裏に L1/L2/L2b/L3 = 4層）

L0 `#0A0A0C` / L1 グラデ（`radial-gradient(120% 120% at 50% 35%, #0C1014 0%, #0B0E12 45%, #0A0A0C 100%)`）/ L2 グリッド（`${accent}22` 64px・放射マスク）/ L2b steel の光（`linear-gradient(90deg, transparent, ${accent}cc, ${accent}55, ${accent}cc, transparent)`）/ L3 patrol-steel グロー（`radial-gradient(closest-side, #5B8DB888, #5B8DB822, transparent)` `blur(28px)`）/ L4 主役タイトル（Trail 包み・`overflow:hidden` span マスク・Anton `fontWeight:800 fontSize:150 letterSpacing:-2 color:#F5F7FA`）/ L5 下線＋サブ（Oswald `fontSize:38 letterSpacing:6 uppercase color:#C8CDD6`）/ L6 ロゴ（`linear-gradient(135deg, ${accent}, #ffffff22)`・`border:2px solid ${accent}`）。

## 11.4 確認方法（CLAUDE.md §5）

```bash
cd C:\Users\aab15\Documents\prime-documentary\remotion
npm run studio     # = remotion studio。OpeningGlover を 0→180f でスクラブし §11.1 の各時刻を目視
npx remotion render OpeningGlover out/glover_opening.mp4 --props=./props/glover.json
# props 差し替え量産
npx remotion render OpeningGlover out/glover_short_op.mp4 --props=./props/glover_short.json
# 本編
npx remotion render Ep48Glover out/glover_final.mp4 --props=./src/data/glover_film.json --public-dir=public_slim --concurrency=4
```

---

# 12. props 定義と型（CLAUDE.md §4）

```ts
export type OpeningGloverProps = {
  title: string;      // 主役タイトル。1文字ずつスタッガーで切れ上がる
  subtitle: string;   // サブタイトル。UPPERCASE 表示（facts_lock 検査対象）
  accent: string;     // アクセント（HEX6桁・"#"込み）。グリッド/steel の光/グロー/下線/ロゴに波及
  hasLogo: boolean;   // true で左上にロゴバッジ
};
```
**EP48 の確定 props（`remotion/props/glover.json`）:**
```json
{ "title": "THE NAME ON THE PLATE", "subtitle": "KANSAS V. GLOVER, 2020", "accent": "#5B8DB8", "hasLogo": true }
```
**量産用 `remotion/props/glover_short.json`:**
```json
{ "title": "HE RAN YOUR PLATE", "subtitle": "THEN PULLED YOU OVER", "accent": "#5B8DB8", "hasLogo": false }
```
> `accent` は **`#5B8DB8` 固定**（EP41 gold / EP42 warrant-blue / EP43 amber / EP44 teal / EP45 crimson / EP46 green / EP47 civil-violet の流用は BLOCKER）。`subtitle`/`title` は `facts_lock` 検査対象（「illegal / struck down / the stop was wrong / stop any car / probable cause required」を出さない）。**サムネ headlines に Deputy 氏名/郡/プレート/車種/年齢を出さない**（R-HEDGE）。**8-1 をサムネに使うなら "UPHELD / A NARROW RULE" の語を同居**（R-VOTE）。過大化タイトル（"police can stop any car"）を作らない（C1）。

---

# 13. 受入基準（EP48 の Definition of Done・★語数ゲートが最初・全編アイボール必須）

```bash
cd C:\Users\aab15\Documents\prime-documentary
# 0. 語数（最優先・課金前）
./.venv/Scripts/python.exe scripts/check_script_length.py episodes/PD-2026-048-glover/03_script/script.en.v001.md --json
# 1. 事実性（EP48固有・§1.3・6制約・dochighlight 0件・R-OVERCLAIM/R-STANDARD/R-VOTE/R-QUOTE）
./.venv/Scripts/python.exe scripts/check_glover_facts.py --json
# 2. ビート契約（AE↔figures 非重複・ledger・6制約・dochighlight 0件）
./.venv/Scripts/python.exe scripts/validate_glover_beats.py
# 3. 密度（★30 を Remotion 側で満たしていること・--ep 指定／--json は出力パス）
./.venv/Scripts/python.exe scripts/check_motion_density.py --ep PD-2026-048-glover --json runs/qc/glover_motion.json
# 4. VO速度（ナレ直後・ミックス前）
./.venv/Scripts/python.exe scripts/measure_vo_wpm.py --ep glover --json
# 5. 最終受入
./.venv/Scripts/python.exe scripts/check_final_acceptance.py 48 --render episodes/PD-2026-048-glover/08_edit/glover_final_bgm.v002_ae.mp4 --emit-receipt
```
> **ゲート入力は `--ep PD-2026-048-glover`。`--json <film.json>` を入力に使わない**（出力パス＝上書き事故。ブリーフ§5）。

| ゲート | 閾値 | EP48 設計値 |
|---|---|---|
| `check_script_length` | band 内 | 2,136語（SPEC・要 PASS 確認・cap 2,141） |
| `runtime_band` | 690–750s | **740.1s = 12:20.1**（上限 750s に 9.9s 余裕） |
| `motion_density` | ≥2.5/min ∧ cov ≥0.25 ∧ variety ≥3 | **3.00/min / 0.270 / 12種**（film.json 36 beats・AE非依存・floor 30 に +6） |
| `animation_mix`（紙芝居） | still-share ≤45% ∧ motion cov ≥45% | **44.9% / 55.11%** |
| `check_asset_reuse` | first-use ≥0.70・still≤2・factory1・motion≤2 | **0.858 / 2 / 1 / 2** |
| `footage_diversity` | distinct/total ≥0.40 | **0.858** |
| `visual_asset_qc` | 全 factory 目視 reviewed | **92本 目視（CODEX_A）** |
| `image_resolution` | 長辺≥3840 | 全 SDXL ≥3840 |
| `bgm_present` | 無音>25秒ゼロ | 最長 1.8秒 |
| `caption_integrity` | 一致≥99%・カバー≥95% | §8.2 |
| `op_ed_bookends` | `BrandOpening`/`BrandEndcard` import・不変 | ✓ |
| `asset_manifest` | A↔B counts/role 一字一致・also_thumb 6（S01/S04/S12/S32/S37/S48）・overlay 12・schema `glover_assets.v1` | §5.8 |
| `facts_lock`（EP48固有・6制約） | violations=0・**dochighlight 0**・R-OVERCLAIM（stop any car 0）・R-STANDARD（reasonable suspicion≠probable cause）・R-VOTE（8-1=UPHELD/NARROW）・R-QUOTE（Sotomayor=dissenting／Kagan=concurring／Thomas=for the Court） | §1.2/§1.3 |
| **全編アイボール** | 12:20.1 を通しで目視 | ★1フレーム判定禁止（EP39-41/EP3941 の miss）。本編・AEカード・VO同期・hookライン を3回チェック |

---

# 14. premortem（失敗するとしたらここ）

| # | 失敗モード | 事前対処 |
|---|---|---|
| 1 | **判示の過大化**（"police can stop any car"） | §1.2 R-OVERCLAIM。判示は NARROW・推認は打ち消す情報で消える。"a careful yes, with a hard edge on it"。stop any car / probable cause required を書かない |
| 2 | **reasonable suspicion と probable cause の混同** | §1.2 R-STANDARD。停止は reasonable suspicion（Terry 級）＝probable cause でない。c01 に "NOT PROBABLE CAUSE"・probablecause outcome "stall" |
| 3 | **停止を"違法/覆された"と誤記** | §1.2 R-VOTE。停止は 8-1 UPHELD・第4修正に反しない。`illegal/unconstitutional/struck down/overturned` を停止主語に使わない。8-1 payload に "UPHELD/A NARROW RULE/reasonable" 対語必須 |
| 4 | **引用の帰属ミス**（Sotomayor/Kagan を Court に） | §1.5/§1.2 R-QUOTE。**Sotomayor="Justice Sotomayor, dissenting"／Kagan="Justice Kagan, concurring"／Thomas="Justice Thomas, for the Court"**。逐語のみ・要約を引用符に入れない |
| 5 | **Glover 肖像 / 顔** | §5.6/§9 R-FACE。運転者は影/シルエットのみ・顔なし・全ショット人物なし。逮捕の暴力を描かない（広告安全） |
| 6 | **medium 値の画面焼き**（Deputy 氏名・郡・プレート・車種・年齢） | §1.4 R-HEDGE。画面 hard 数値は 8-1/2020/589 のみ。Mehrer/Douglas/プレート/1995 Chevy は発話のみ |
| 7 | **番号ズレ**（別番号を発明） | シーンは S01..S48 固定（§3.2）。still 資産 ID は S01..S85（別空間・cross-map 禁止） |
| 8 | **紙芝居**（still-share 45%超・余裕 0.1%pt） | §5.1 で still-cut 101 固定・factory 92・i2v 32。still1つ増で 45% 割れ → cut を増やさず同一シーンの新規 distinct で回復 |
| 9 | **バリエーション水増し**（`--variants 3`） | §5.3。variants 指定なし＝1枚。ai_prompts は 85行＝85枚 |
| 10 | **密度 FAIL**（AEカードに頼る） | §6。film.json に 36 beats（30 超）。AE 6枠は composite 後で非カウント |
| 11 | **画像プロンプトが読めない**（0枚生成） | §9.1 の2行形式・`--only S01` で `shots=101`（body 85 + i2v種 16）確認 |
| 12 | **ファイル名信仰**（牛が本編に入る） | §5.4 factory 92本を `build_footage_contact_sheet.py` で全点目視（CODEX_A BLOCKING） |
| 13 | **dochighlight のバグ見え**（3回指摘） | §6.2/§7.3。`dochighlight`/`comparebars` を1件も置かない（R-DOCHL・grep 0） |
| 14 | **FigureBeats kind が実union非在/大文字**（無音描画・render クラッシュ） | §6.2 は実 FigureBeats.tsx union で全数照合済（12 kind 全実在・小文字）。votetally=majority/dissent・compbars=items[]・mechanism=closingdoor/gears/faultsplit・probablecause=outcome・timeline=events[] |
| 15 | **id 誤り / durationInFrames 手書き** | §0.1。`id="Ep48Glover"`・`caseFilmDurationInFrames(gloverFilm,30)`=22203（hookSeconds=8.0） |
| 16 | **hookSeconds=0 / hookLine 流用**（EP44/45事故） | §0.1。hookSeconds=8.0・glover 専用 hookLine（他話流用禁止）を film builder に焼く |
| 17 | **accent 流用**（他話色を残す） | §0.5/§7.5/§12。OP props/AEカード/サムネ accent は `#5B8DB8`（RGB [0.357,0.553,0.722]） |
| 18 | **A↔B マニフェスト不整合** | §5.8。`glover_assets.v1`・role enum=`body/i2v_source/reject`・also_thumb 6（S01/S04/S12/S32/S37/S48）・overlay 12・全エントリ public_path を A/B 一字一致 |
| 19 | **EP39〜47 と素材被り** | §2 で stock_ledger の sha256 を除外（`select_glover_factory.py --verify-no-prior-overlap`） |
| 20 | **fast端で 750s 超**（余裕 9.9s） | §4.1 speed 1.0 明示＋`measure_vo_wpm` 168–190・190超は破棄再発注。総尺 740.1s ≤750 の assert（§3.1[4]） |
| 21 | **public→public_slim 未 staging**（EP45事故） | ブリーフ§5。img/factory/motion/audio を public_slim へ全コピー＋全media解決0確認してからレンダ |

---

# 15. 設計パッケージ接続（DESIGN → CODEX_A / CODEX_B）

- **DESIGN（本書）:** タイムライン（0〜719.6s 全区間＋8.0s teaser・各Act・§3.1/§3.1b）・レイヤー（背面4層・§8）・モーション数値（§10）・48絵コンテ（§3.2/§9・象徴・6制約・Glover 顔なし）・FigureBeats 設計（≥30＝36・小文字kind・変種≥3＝12種・**実 union 準拠**・dochighlight 0件・quote 逐語＆帰属厳格・§6/§1.5）・AEカード表（6枚・accent #5B8DB8・§7.3）・OP 仕様（§11）・asset_manifest スキーマの正（§5.8）。
- **CODEX_A（別ファイル `EP48_glover_CODEX_A_ASSETS.v001.md`）:** §9 を **85本の固有プロンプト**（1シーン1枚・variants 0・省略禁止で全85本）＋ i2v 16 ＋ factory 92 選定＆**全点目視QC**（`select_glover_factory.py`・`--exclude-used --ep PD-2026-048-glover` で EP39〜47 sha256 除外）＋境界契約 `asset_manifest.v001.json`（schema `glover_assets.v1`・counts を EP48 値 still_body85/still_i2v_source16/motion16/factory92/overlay12・全エントリ public_path・`stills[].role` enum=`body/i2v_source/reject`・also_thumb 6（S01/S04/S12/S32/S37/S48））。
- **CODEX_B（別ファイル `EP48_glover_CODEX_B_BUILD.v001.md`）:** `build_glover_film.py`（＝EP45 `build_cleveland_film.py` or EP46 `build_tlo_film.py` を複製・ASSET_MAP/NARR/FACTORY_SEL/SLUG/EP を glover に・実素材のみ stub 禁止・hookSeconds8.0・正しい hookLine・manifest factory/motion 全読込）／captions（実測 narration）／figures 36（小文字 kind・実 union 準拠・dochighlight 0件・quote 逐語＆帰属・§6/§1.5）／`CaseFilm` を `id="Ep48Glover"` で Root.tsx 登録（`caseFilmDurationInFrames`＝22203・hookSeconds=8.0）・typecheck／`OpeningGlover`／AEビルダ・コンポジタ（cleveland 修正版複製・repo path・aerender 二段・accent RGB #5B8DB8=[0.357,0.553,0.722]・実測フィット・ledger 照合・.aep>.jsx assert・レイアウト名は実装済み8種のみ・§7.3 の6カード＝本書 §7.3 と一字一致）・`validate_glover_beats.py`・`check_glover_facts.py`（EP45 `check_cleveland_facts.py` を複製・同名・R-NUM は asset_manifest 除外＋index skip・acttitle 除外を継承）／`build_glover_bgm_real.py`→`composite_glover_hero.py`（film_offset 11.5 適用）／public_slim staging＋全media解決0確認／レンダ（`--public-dir=public_slim --concurrency=4`）／全ゲート（`--ep PD-2026-048-glover`）／完成後の全編3回チェック（本編・AEカード・VO同期・hookライン）。
- **A↔B 接続点は `asset_manifest.v001.json` ただ1ファイル**（schema `glover_assets.v1`・counts/role enum を A/B 一字一致・§5.8）。
- **複製元（★`ls scripts/` で実在確認・実在しないスクリプトを捏造しない）→ glover 複製先:** EP45 の cleveland 系（`build_cleveland_film.py`→`build_glover_film.py` / `check_cleveland_facts.py`→`check_glover_facts.py` / `select_cleveland_factory.py`→`select_glover_factory.py` / AE は cleveland 修正版 `build_cleveland_hero_cards.py`→`build_glover_hero_cards.py`・`composite_cleveland_hero.py`→`composite_glover_hero.py`）を第一候補、なければ EP46 tlo 系。`validate_caniglia_beats.py`→`validate_glover_beats.py`・`build_caniglia_bgm_real.py`（or EP43 系）→`build_glover_bgm_real.py`。**共有（複製不要・実在確認済）:** `generate_sdxl_4k.py` / `build_footage_contact_sheet.py` / `check_motion_density.py` / `measure_vo_wpm.py` / `check_script_length.py` / `check_final_acceptance.py`。
