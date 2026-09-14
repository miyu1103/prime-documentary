# EP47 — THE FIFTY DOLLAR ARREST — 制作設計書（DESIGN 本体・v001・確定台本版）

- Episode ID: `PD-2026-047-atwater` / slug: `atwater` / EP47
- 中心の問い（英語・二人称・★"違法だった"と書かない）: **"For something the law says is worth nothing but a fifty dollar fine, can the police put you in handcuffs and take you to jail?"**（答え＝2001年に最高裁が「できる（合憲）」と言った）
- 判例: **Atwater v. City of Lago Vista, 532 U.S. 318 (2001)**（decided **2001-04-24**・opinion **Justice Souter**・第4修正の令状なし現行犯逮捕）。反対＝**Justice O'Connor**（Stevens・Ginsburg・Breyer 参加）。
- 主役: **Gail Atwater**（Lago Vista, TX・**存命の私人＝R2**・非有罪＝罰金のみ）。**顔・肖像・身体を一切描かない。象徴のみ・尊厳の物語。** 同乗の**子ども2人を扇情化しない**（空のチャイルドシート等の象徴・年齢を強調しない）。Officer Bart Turek も人物化しない。
- 主題: 罰金刑のみの軽罪でも、令状なしの現行犯逮捕は第4修正に反しない、と最高裁は 5-4 で**判断した（＝逮捕は合憲・UPHELD）**。本作は「違法だった／覆された」と決して言わない。**"the Court said police COULD do this"** が背骨。Souter 多数意見は逮捕を **"pointless indignity"**（無意味な屈辱）と認めつつ許容し、救済は**立法に委ねた**。O'Connor 反対がその対抗軸（逐語・反対意見に帰属）。
- Status: **BINDING**。**唯一の真実 = 機械生成済み `EP47_atwater_PRODUCTION_SPEC.v001.json`**。本書のあらゆる数値はそこからの転記で、手書きで発明していない。衝突したら SPEC が勝つ。
- このファイルは**設計パッケージ3分割**（DESIGN / CODEX_A / CODEX_B）の **DESIGN 本体**。共有ブリーフ `EP47_atwater_DESIGN_BRIEF.shared.md` を単一の真実源とする。85本の SDXL プロンプト実体・i2v 16・factory 92 選定は **CODEX_A**、`build_atwater_film.py`・captions・figures 実装・Root.tsx 登録・AEビルダ/コンポジタ・ゲートは **CODEX_B** に属す（本書は各所でポインタのみ示す）。

## ★このエピソードの唯一の真実（手書きで数値を発明するな）

`episodes/_planning/EP47_atwater_PRODUCTION_SPEC.v001.json`（台本から機械生成・`scripts/build_production_spec.py`）。本設計書は SPEC を**人間可読な実装指示に翻訳しただけ**で、新しい数字を作っていない。

```
words_total          = 2,135
narration_seconds    = 719.3   （= 12.0分・[SILENCE 1] の実音無音を含む）@ wpm_used 178.1
scenes               = 48      （S01..S48・確定。増やすな減らすな）
total_cuts           = 225
still  distinct 85 / cuts 101 / mean 1.19 / cap 2   ← ★各1枚生成（バリエーション0）
factory distinct 92 / cuts 92 / mean 1.0  / cap 1   ← 在庫選抜・全点目視QC
motion distinct 16 / cuts 32 / mean 2.0  / cap 2
distinct_total       = 193
first_use_share      = 0.8578  （floor 0.70）
still_share_of_cuts  = 0.4489  （cap 0.45）
motion coverage      = (92+32)/225 = 0.5511  （floor 0.45）
MG beats_floor       = 30      （film.json 側 figures+graphics+heroCuts。AEカードは check_motion_density に数えられない）
beats_per_min_floor  = 2.5   /  variety_floor = 3
mean_shot_seconds    = 3.19   /  max_shot_seconds = 6.0
SPEC 幕秒（発話・語数から機械算出）: HOOK 58.6 / OPENING 64.0 / ACT1 124.3 / ACT2 137.5 / ACT3 189.0 / ENDING 129.0（合計 702.4s）
  ※ SELF-CHECK 130語/43.8s は台本末尾の著者自己点検＝非発話（narration に数えない）
  ※ 発話幕秒合計 702.4 と narration_seconds マスター 719.3 の差 16.9s = 幕間の息継ぎ＋設計無音（SILENCE 1 = 1.8s）を内包する測定マスター。film.json には 719.3 を入れる。
```

## ★★ 最重要の前提: 1シーン1枚・バリエーション0 ★★（ブリーフ§1）

- Codex の画像生成は高精度。**同一ショットの複数バリエーション（`_01/_02/_03`）を作らない。**
- `04_scenes/ai_prompts.v001.md` は **still 85本＝85行の固有プロンプト**（`generate_sdxl_4k.py` の `read_prompts()` 2行形式・各1枚）＋ **i2v 種 16行** ＝ **計101エントリ**（`--only S01` の `shots=` は 101）。**`--variants 3` は使わない**（`--variants 1` または variants 指定なし）。
- **総生成画像 = still 85 + i2v seed 16 = 101枚（各1回）。** **factory 92 は生成ではなく在庫選抜**（全点目視QC・EP39〜46 と sha256 被りゼロ）。
- **still を増やして factory を削るな**（still-share 0.4489 は cap 0.45 に対し余裕 0.11%pt しかない＝EP45（0.36%pt）より薄い）。**still-cut は 101 で固定。**

## ★EP39〜46 で踏んだ失敗＝本書が最初から潰す設計判断

| # | 失敗 | 本書での恒久対策 | 参照 |
|---|---|---|---|
| 1 | **番号ズレ**（別リストを発明） | シーンは **SPEC の S01..S48 に固定**。still 資産 ID は S01..S85（別空間・cross-map 禁止） | §3.2 / §9 |
| 2 | **紙芝居**（still 100% で animation_mix FAIL） | still-cut **101 固定**＋factory実写 **92**＋i2v **32**。still-share 44.89% ≤45% / motion cov 55.11% ≥45% を構造保証 | §5.1 |
| 3 | **バリエーション水増し** | **1シーン1枚・85本を各1枚**。variants 禁止 | §5.3 |
| 4 | **画像プロンプトのパーサ非互換** | `read_prompts()` の**2行形式**。CODEX_A が `--only S01` で拾い数（101）を確認 | §9.1 |
| 5 | **ファイル名を信じた**（牛が documents） | factory 92本を `build_footage_contact_sheet.py` で**全点目視QC**（CODEX_A 必須・BLOCKING） | §5.4 |
| 6 | **AEカードを密度に数えた** | `check_motion_density` は film.json の `figures+graphics+heroCuts` だけ。**film.json 側に MGビート 30本以上**（本書は 36 設計）。AE は composite 後で 0 カウント | §6.1 / §7.1 |
| 7 | **一枚絵で完成判定**（EP39-41/EP3941 の眼球不足） | 全編アイボール必須（§13）。measured > estimated | §13 |
| 8 | **A↔B マニフェスト不整合** | asset_manifest は **A↔B で同一スキーマ・counts/role enum を一字一致**。role=`thumb`/`still_thumb` を作らない。サムネは `also_thumb=true` の body still 6枚 | §5.8 |
| 9 | **dochighlight のバグ見え**（EP40/41/42 で3回指摘） | **`dochighlight` を figures に1件も入れない（grep 0・R-DOCHL）。** 書類/切符/命令は `lowerthird` の説明テキストで表す | §6.2 / §7.3 |
| 10 | **逮捕を"違法/覆された"と誤記**（本作固有の最大リスク） | 逮捕は **UPHELD（5-4・合憲）**。`illegal / unconstitutional / struck down` を逮捕自体に使わない（R-DISPO） | §1.2 |

---

# 0. 環境・Remotion設定（CLAUDE.md §0 準拠）

## 0.1 本編 `Ep47Atwater` の Composition 設定（★本編の正・誤記注意）

| 項目 | 値 |
|---|---|
| `id` | **`Ep47Atwater`**（Root.tsx に `CaseFilm` で登録。ブリーフ§5「composition id Ep47Atwater」。**id の切り詰め・綴り違い・大文字化は誤記＝BLOCKER**） |
| 解像度 | **1920 × 1080** |
| `fps` | **30**（EP44/45/46 と同値を踏襲。フレームは全て `Math.round(30 × 秒)`・直書き禁止） |
| `hookSeconds` | **8.0**（★EP45 は 0 だったが EP47 は **8.0 を明示**＝BrandOpening 前の**無音コールドオープン teaser preroll**。§3.1 参照。durationInFrames 4項関数の第1項に入る） |
| `durationInFrames` | **`caseFilmDurationInFrames(atwaterFilm, 30)` = 22194**（4項の実関数 `round(hookSeconds×30)+round(OPENING_SEC×30)+ceil(narrationSeconds×30)+round(ENDCARD_SEC×30)`・**hookSeconds=8.0**・§3.1[3] で算出。手書きで数値を入れず関数で算出する） |
| component | `remotion/src/compositions/CaseFilm.tsx`（**既存の汎用 `CaseFilm` を再利用**・実在確認済。`Bookends.tsx` の `BrandOpening`/`BrandEndcard` を **import**・fork 禁止） |
| data | `remotion/src/data/atwater_film.json`（`scripts/build_atwater_film.py` で再生成できる状態を保つ＝**git 未追跡**） |

**Root.tsx 登録（★ブリーフ§5・CODEX_B が実装）:**
```tsx
import {atwaterFilm} from './data/atwater_film.json';
import {caseFilmDurationInFrames} from './lib/caseFilmDuration';
// ...
<Composition
  id="Ep47Atwater"
  component={CaseFilm}
  width={1920} height={1080} fps={30}
  durationInFrames={caseFilmDurationInFrames(atwaterFilm, 30)}  // = 22194
  defaultProps={{film: atwaterFilm}}
/>
```
> **id は `Ep47Atwater`**（切り詰め・綴り違い・先頭大文字化などは全て誤記。ブリーフ§5 の render 行 `Ep47Atwater` が正）。`CaseFilm.tsx` は実在（`remotion/src/compositions/CaseFilm.tsx`）。`caseFilmDuration` ヘルパの実体名は CODEX_B が既存実装（tekoh/cleveland と同一）に合わせる。

## 0.2 タイトルバンパー `OpeningAtwater` の Composition 設定（CLAUDE.md 正典部品準拠）

| 項目 | 値 |
|---|---|
| `id` | **`OpeningAtwater`** |
| 解像度 | **1920 × 1080** |
| `fps` | **60**（CLAUDE.md §0 の正典値。OP 単体は 60fps） |
| `durationInFrames` | **180**（= 3.0秒 @ 60fps） |
| component | `remotion/src/compositions/OpeningAtwater.tsx`（§11 全仕様） |

> `OpeningAtwater` は**独立したタイトルバンパー成果物**（`out/atwater_opening.mp4`）。本編内 OP/ED の正典は `Bookends.tsx`（`BrandOpening` 3.50s / `BrandEndcard` 9.00s・不変）。`OpeningAtwater` を本編に ffmpeg で焼き込まない（オーナー承認なしに見え方を変えない）。

## 0.3 必要な依存パッケージ

```bash
cd C:\Users\aab15\Documents\prime-documentary\remotion
npm i @remotion/motion-blur     # CLAUDE.md 必須依存（Trail によるモーションブラー）
```

## 0.4 `remotion.config.ts`（CLAUDE.md §0 正典値・EP41〜46 と同一・書き換えない）

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

**EP47 のパレット（★市民的自由の紫＝civil-violet＋テキサスの午後の道の埃＋冷たい institutional の booking＋淡い大理石の最高裁）:**
```
INK     = #0A0A0C   ルート背景（サムネ bg と一致）
DUST    = #14100C   テキサスの午後の埃・ピックアップ車内の暖い near-black（road/cab 側）
STEEL   = #22242A   booking の冷灰・institutional（無人・鉄格子/独房は描かない）
MARBLE  = #34363B   最高裁の冷たい大理石（ACT3・列柱・9席）
ACCENT  = #7A5CD0   ★civil-violet（市民的自由の一点差し色）。ブランド数値・ライン・下線・グロー・OP/AE/サムネ accent。★EP41 gold / EP42 blue / EP43 amber / EP44 teal / EP45 crimson / EP46 green を流用しない
WHITE   = #F5F7FA
SILVER  = #C8CDD6   （AI開示テキスト）
```
> **レーン分離:** EP41 gold（鋼灰）/ EP42 blue（夜シカゴ）/ EP43 amber（porch灯）/ EP44 teal（clinical hospital）/ EP45 crimson（督促の朱）/ EP46 green `#3F8F5F` と被らないよう、EP47 は **テキサスの埃の暖い near-black `#14100C` ＋ booking の冷灰 `#22242A` ＋ 冷たい大理石 `#34363B` を基調＋唯一の差し色＝civil-violet `#7A5CD0`**。接尾に `porch-amber` `warrant-blue` `teal-green hospital` `sodium prison corridor` `crimson overdue` `forest-green` を含めない。**factory は EP39〜46 の `stock_ledger*.json` の sha256 を除外**（CODEX_A・BLOCKING）。**CODEX_B は OP props / AEカード / サムネ accent を必ず `#7A5CD0` にする（他話色の流用は BLOCKER）。**

---

# 1. 事実の取り扱い（★正確性6制約＝FACTS LOCK / `check_atwater_facts.py`・BLOCKING）

## 1.1 確定台本（唯一の正・1バイトも変えない）

```
C:\Users\aab15\Documents\prime-documentary\episodes\_planning\EP47_atwater_script.en.v001.md
```
**本番配置先:** `episodes/PD-2026-047-atwater/03_script/script.en.v001.md`（上記を1バイトも変えずコピー）。整形も禁止（AI臭再発と語数ゲート再計算を招く）。台本の幕構成（HOOK / OP / ACT1–3 / ENDING）と `【SILENCE 1 — 1.8s】`（**1箇所**）を正典とする。存在しない演出マーカーを発明しない。

## 1.2 ★正確性6制約（全出力＝プロンプト・カード文言・図表・字幕・タイトルに適用。1つでも違反＝BLOCKER）

| # | 制約 | 出力での順守 |
|---|---|---|
| **C1** | **逮捕は合憲＝UPHELD（5-4）。"違法/覆された"と言わない** | 罰金刑のみの軽罪でも令状なし現行犯逮捕は第4修正に反しない、と最高裁は判断（A10）。**`illegal / unconstitutional / struck down / overturned / the Court ruled the arrest wrong` を逮捕自体に使わない。** 枠は **"the Court said police COULD do this"** / "the arrest STANDS" / "constitutional" / "allowed" / "they MAY, not must"。ENDING の不安は「違法だから」ではなく「**許されているから**」に置く |
| **C2** | **Souter 多数意見の nuance を落とさない** | Souter は逮捕を **"pointless indignity"（無意味な屈辱）** と認めつつ許容し、4A を事案ごとの利益衡量に曲げず、**救済は立法に委ねた**（A14/A15）。「Souter が逮捕を良しとした／擁護した」と単純化しない。「無意味な屈辱と認めた、しかし憲法は禁じない、直すのは議会」の3点セットを保つ |
| **C3** | **O'Connor 反対が対抗軸・逐語は反対意見に帰属** | O'Connor 逐語（A17）を **DISSENT** に中立帰属（Court に帰属させない）。attribution 厳格＝`Justice O'Connor, dissenting`。「最高裁が O'Connor の側に立った」等と誤らせない（反対＝負けた側・four votes, not five） |
| **C4** | **票決 5-4・中立帰属** | Souter 多数（Rehnquist・Scalia・Kennedy・Thomas）／O'Connor 反対（Stevens・Ginsburg・Breyer）（A11）。**5-4 を中立に示す**（どちらが「正しい」と画面で断じない）。投票数を発明しない（5-4 は台帳にある＝焼いてよい） |
| **C5** | **Gail Atwater＝R2・象徴のみ／子ども非扇情** | 存命の私人・非有罪（罰金のみ）。**顔・肖像・身体を描かない**。象徴のみ（テキサスの道・空のチャイルドシート2つ・外れたシートベルト・手錠・booking 台/指紋・$50の切符・天秤・最高裁列柱/9席・開いた扉と閉じた扉）。**子ども2人を扇情化しない**（年齢を強調しない・泣く子/怯える子を描かない・空のチャイルドシートで象徴）。Officer Turek も人物化しない |
| **C6** | **数値は台帳一致・捏造ゼロ・medium 値は画面に出さない** | 画面に焼く hard 数値は **$50（罰金上限・high）／$25–$50（TX 法定幅・high）／5-4（票・high）／April 24, 2001（判決日・high）** のみ（§1.4）。**逮捕年 1997・子の年齢（3・5）は confidence:medium＝ヘッジ／画面に出さない**（ブリーフ§3.6・R-HEDGE）。"about an hour" 拘置も画面数値にしない（発話のみ）。捏造引用禁止 |
| **R1** | **実在人物の顔・肖像を生成しない** | 全生成ビジュアル表示中は `AI-assisted visualization`（右下）常時表示。概要欄に1行 AI 開示 |

## 1.3 6制約ゲート `check_atwater_facts.py`（`scripts/check_atwater_facts.py`＝EP46 `check_tlo_facts.py` を atwater 用に複製。exit≠0 で出荷停止・CODEX_B 実装。出力 `facts_lock.v001.json`）

> **★ゲート名は1本に確定:** 6制約の機械ゲートは **`scripts/check_atwater_facts.py`**（出力 `09_package/facts_lock.v001.json`）ただ1つ。**DESIGN / CODEX_A / CODEX_B で同名参照**（別名を作らない）。内部ルール **R-*** に一本化して実装する。**★R-NUM 等の構造ルールは narrative figure のみ対象**（asset_manifest 構造カウント・acttitle index は除外＝EP45 修正済）。

**検査対象:** `03_script/script.en.v001.md` / `remotion/src/data/atwater_film.json` の `figures[].kind`・`figures[].*text*`・`quote`・`attribution`・`lines[]`・`label` / `08_edit/ae_hero/beats.json` の `hero`/`top`/`bottom`/`sub`/`attribution`/`caption` / `09_package/description.txt` / `remotion/props/atwater*.json` の `subtitle`/`title` / `04_scenes/ai_prompts.v001.md`。

| ルール | 内容 |
|---|---|
| **R-DISPO（★EP47 固有・最大リスク）** | 逮捕・判決に対し `illegal` / `unconstitutional` / `struck down` / `overturned` / `the Court (said/ruled) the arrest (was )?(wrong/unlawful/illegal)` / `violated the Fourth Amendment`（Atwater の逮捕を主語に肯定形で）が出たら FAIL。**`5 ?- ?4` を含む payload に `upheld` / `stands` / `constitutional` / `allowed` / `could` / `did not violate` のいずれかが同一 payload に無ければ FAIL**（「5-4 で覆した」誤読の防止） |
| **R-QUOTE（帰属厳格）** | `quote` は §2 `APPROVED_QUOTES` の逐語のみ。**Souter 逐語**（"Atwater's claim to live free of pointless indignity and confinement clearly outweighs anything the City can raise against it specific to her case"）の attribution は `Justice Souter, for the Court` と一致必須。**O'Connor 逐語**（"The Court neglects the Fourth Amendment's express command in the name of administrative ease. In so doing, it cloaks the pointless indignity that Gail Atwater suffered with the mantle of reasonableness."）の attribution は `Justice O'Connor, dissenting` と一致必須。**O'Connor 逐語を Court に帰属させたら FAIL**。要約を引用符に入れたら FAIL。attribution 空なら FAIL |
| **R-FACE / R-CHILD** | `ai_prompts` 正プロンプトに `portrait`/`face of`/`likeness`/`recognizable`/`Gail Atwater`（人物として）/`nude`/`her body` が出たら FAIL（ネガティブ使用は可）。`crying child`/`frightened child`/`weeping kids`/`terrified children`/`child's face` が出たら FAIL（**空のチャイルドシートは可**）。子の年齢（`3`/`5`/`three-year-old`/`five-year-old`）を画面文字列に出したら FAIL |
| **R-HEDGE** | 画面文字列（figures/AE/字幕見出し/props）に **§1.4 の表以外の数値**が出たら FAIL。特に **`1997` を hard 数値カード/stamp/stat に出したら FAIL**（confidence:medium・発話のみ許容）。子の年齢の数値も FAIL。`$50`/`$25`/`5-4`/`2001` を焼く figure/AE は台帳一致必須 |
| **R-DOCHL（★全話共通）** | `figures[].kind == "dochighlight"` が **1件でも**存在したら FAIL（`grep -c '"dochighlight"'` が 0 でないと出荷停止）。`comparebars` も非実在→出たら FAIL（`compbars` が正） |
| **R-DISCLOSE** | `description.txt` に AI 開示1行が無ければ FAIL。全生成ビジュアル区間で右下 `AI-assisted visualization` が焼かれていること（§13 アイボールで確認） |

**出力:** `09_package/facts_lock.v001.json`（`{"pass":bool,"violations":[{"file","rule","line","excerpt"}],"skipped":[...]}`）。`pass:true` でない限り `check_final_acceptance.py` に進まない。

## 1.4 画面に出してよい確定数値（★台本／事実対応表 A01–A19 に存在し confidence:high のものだけ。この表以外を画面に出すな）

| ID | 値 | 台本での表現（claim） | conf | 使用先 |
|---|---|---|---|---|
| N01 | **$50 MAX FINE** | "The most the law can ever do to her is take fifty dollars"（A03） | **high** | AE **m01**（MONEY_STACK）/ figures `stat`（F-STAT1） |
| N02 | **$25–$50**（TX 法定幅） | "No less than twenty five dollars, no more than fifty"（A02） | high | figures `lowerthird`（F-LT seatbelt） |
| N03 | **5 – 4**（THE ARREST STANDS・UPHELD） | "By a vote of five to four … did not violate the Fourth Amendment"（A11/A10） | high | AE **v01**（VOTE_SPLIT・**R-DISPO 対語 "THE ARREST STANDS" 必須**）/ figures `votetally`（F-VOTE） |
| N04 | **APRIL 24, 2001 · SUPREME COURT** | "in April of 2001 the Court gave its answer"（A18・判決日 high） | high | AE **t01**（DATE_STAMP） |
| N05 | **Souter 逐語 "…live free of pointless indignity and confinement clearly outweighs…"** | "a pointless indignity … gratuitous and humiliating"（A14） | high | AE **s01**（QUOTE_CARD・帰属 **Justice Souter, for the Court**）/ figures `quote`（F-QUOTE1） |
| N06 | **O'Connor 逐語 "…it cloaks the pointless indignity … with the mantle of reasonableness"** | "Speaking for the dissent, she wrote …"（A17） | high | AE **q01**（QUOTE_CARD・帰属 **Justice O'Connor, dissenting**）/ figures `quote`（F-QUOTE2） |
| N07 | **FINE-ONLY · NO JAIL** | "Her offense carries no jail time. It cannot."（A02/A10） | high | AE **n01**（CENTER_STACK）/ figures `kinetic:emphasis`（F-KIN NO JAIL） |
| N08 | **42 U.S.C. § 1983 / THE FOURTH AMENDMENT** | 台本 ACT2 lower-third（A08） | high | figures `lowerthird`（F-LT 1983 / F-LT 4A・AEカードにはしない） |

> **★AE カード文言に「illegal / the Court struck it down / overturned / the arrest was wrong」を書かない（C1・R-DISPO）。** **1997・子の年齢は画面に出さない（R-HEDGE・medium）。** 判例番号 `532 U.S. 318` は t01（DATE_STAMP の place）と figures `lowerthird` に退避（本文で読み上げない）。**5-4 は台帳（A11）にあるので焼いてよいが、必ず "THE ARREST STANDS / UPHELD / CONSTITUTIONAL" の対語を同一 payload に持つ（R-DISPO）。** 投票の「正誤」を画面で断じない（C4 中立）。

---

# 2. 視覚・音響レーン分離（EP39〜46 との素材被り回避）

> **EP39〜46 のファイルには一切触れない（読み取りのみ可）。** レーンを機械的に分離する。

| 軸 | EP45 cleveland | **EP47 atwater** |
|---|---|---|
| 舞台 | 台所→booking→大理石 | **テキサスの片側二車線の午後の道→ピックアップ車内（空のチャイルドシート2つ・外れたシートベルトのバックル）→路肩の巡回車→station の扉→booking 台（脱いだ靴・所持品トレー・指紋・撮影）→無人の holding→治安判事のベンチ→$50の切符／no contest 票→第4修正のページ→天秤（citation ↔ handcuffs）→最高裁の大理石列柱と9席→5-4 の投票→古い法律書（Souter の歴史）→開いた扉と閉じた扉（救済は立法へ）→州境地図（protected/not）** |
| 時間帯 | 暖ランプ→冷灰→大理石 | **テキサスの午後の埃光（道・車内）→路肩の斜光→冷灰の booking→冷たい大理石（ドクトリン核）→夜明けの採光（ENDING の開く扉）** |
| 支配的出来事 | 罰金雪だるま→収監 | **シートベルト違反（罰金のみ）→現行犯逮捕→手錠→squad car→booking→$50→§1983 提訴→第4修正 "reasonable"→probable cause 争点→5-4 UPHELD→Souter 歴史＋bright-line＋"pointless indignity" but permitted→救済は立法→O'Connor 反対（逐語）** |
| アクセント色 | crimson `#B23A48` | **civil-violet `#7A5CD0`** |
| ベース色 | crimson + 大理石 + 冷灰 | **テキサスの埃 near-black `#14100C` + booking 冷灰 `#22242A` + 冷たい大理石 `#34363B` + near-black `#0A0A0C`** |
| レンズ感 | — | **HOOK 象徴フラッシュモンタージュ（~2s cut・現在形）／ACT1 最短・抑制（the stop）／ACT2 正対の転回（法理の問い）／ACT3 正対対称・荘厳・最も遅い（the ruling）／ENDING 引き（pull-back・開く扉）** |
| 画像保存先 | `H:\pd-media\assets\ai\cleveland\` | **`H:\pd-media\assets\ai\atwater\`** |
| Remotion データ | `cleveland_film.json` | **`atwater_film.json`** |
| Remotion コンポ | `Ep45Cleveland` | **`Ep47Atwater`** |
| AE 作業ディレクトリ | `…/PD-2026-045-cleveland/08_edit/ae_hero/` | **`…/PD-2026-047-atwater/08_edit/ae_hero/`** |

**素材被り禁止:** EP39〜46 と同一の factory clip / AI画像を1点も使わない。選定前に `episodes/PD-2026-039-*/`〜`…-046-*/` の `05_stock/stock_ledger*.json` を読み sha256 重複を除外（CODEX_A・BLOCKING）。

---

# 3. 尺と構成 — SPEC の値をそのまま使う

## 3.1 全区間タイムライン（★この表が唯一の正・秒は fps=30 から算出しフレーム直書き禁止・0〜719.3s 全区間＋8.0s teaser preroll）

**算出基準:** SPEC の `narration_seconds = 719.3`（マスター）を `atwater_film.json` の `narrationSeconds` に入れる。**手計算で上書きしない。** 各幕秒は SPEC の acts[].seconds（語数から機械算出）を planning アンカーとして使う。フレーム = `Math.round(30 × 秒)`。**hookSeconds=8.0** は BrandOpening の前に置く**無音コールドオープン teaser preroll**（フラッシュモンタージュ・ナレなし・BGM 低弦のみ）。

| # | ブロック | 役割 | 語数 | 幕秒 | 台本指定の沈黙 | 固定尺 | 開始f | 終了f |
|---|---|---|---|---|---|---|---|---|
| 0 | **HOOK TEASER**（無音 preroll） | `hook` | 0 | **8.00**（hookSeconds） | — | 8.00 | 0 | 240 |
| 1 | **HOOK** ナレ | `hook` | 174 | 58.6（SPEC） | **1.8**（"Hold on the loose seatbelt swinging. No music." で保持） | — | 240 | 1998 |
| 2 | **BrandOpening** | `opening` | 0 | — | — | **3.50** | 1998 | 2103 |
| 3 | **OP** ナレ | `opening` | 190 | 64.0（SPEC） | — | — | 2103 | 4023 |
| 4 | **ACT1** The stop | `body` | 369 | 124.3（SPEC・最短） | — | — | 4023 | 7752 |
| 5 | **ACT2** The 1983 question | `body` | 408 | 137.5（SPEC） | — | — | 7752 | 11877 |
| 6 | **ACT3** The ruling | `body` | 561 | 189.0（SPEC・最長・最も遅い） | — | — | 11877 | 17547 |
| 7 | **ENDING**（payoff→CTA） | `ending` | 383 | 129.0（SPEC） | — | — | 17547 | 21417 |
| 8 | **BrandEndcard** | `ending` | 0 | — | — | **9.00** | 21417 | 21687 |

> **フレーム列**は teaser(240f)/BrandOpening(105f)/BrandEndcard(270f) を実尺で挟み、幕秒を順に `round(30×秒)` で積んだ実装用アンカー。**幕秒積算 nominal 21687 と §3.1[3] の `caseFilmDurationInFrames` 出力 22194 の差 507f=16.9s は、narrationSeconds マスター 719.3 と発話幕秒合計 702.4 の差＝息継ぎ＋設計無音（SILENCE 1 = 1.8s）を内包する測定マスター。** film.json には 719.3 を入れる。CODEX_B は `atwater_film.json` の segment 順から再計算し一致を確認。
> **★台本 OPENING の指定＝「Gold BrandOpening resolves HERE, after the hook question」。** よって順序は **HOOK TEASER（無音）→ HOOK ナレ → BrandOpening（gold 解決）→ OP ナレ**。teaser は HOOK と同じ象徴（道・外れたベルト・手錠・booking フラッシュ）を ~1.3s の最速カットで無音提示し、そのあと同じ世界にナレが入る。

### 検算（CODEX_B は必ず自分で再計算して一致を確認）

```
[1] narrationSeconds = 719.3（SPEC マスター。手計算で上書きしない）
    ※ 発話ブロック HOOK..ENDING の幕秒合計 = 58.6+64.0+124.3+137.5+189.0+129.0 = 702.4s。
      SPEC マスター 719.3 との差 16.9s は、幕間の息継ぎ＋設計無音（SILENCE 1 = 1.8s）を内包した測定マスター。
    ※ mean_shot 検算: 719.3 / 225 = 3.197s ＝ SPEC mean_shot_seconds 3.19 一致（225カットは 719.3s 全域に張る）。

[2] 総尺 = hookSeconds 8.00 + BrandOpening(OPENING_SEC) 3.50 + narrationSeconds 719.3 + BrandEndcard(ENDCARD_SEC) 9.00
        = 739.8 秒 = 12:19.8

[3] caseFilmDurationInFrames(atwaterFilm, 30) = 4項の実関数で算出:
      = round(hookSeconds×30) + round(OPENING_SEC×30) + ceil(narrationSeconds×30) + round(ENDCARD_SEC×30)
      = round(8.0×30)=240 + round(3.5×30)=105 + ceil(719.3×30)=ceil(21579.0)=21579 + round(9.0×30)=270
      = 22,194 フレーム
    ※ CODEX_B は atwater_film.json の hookSeconds/narrationSeconds（＋Bookends の OPENING_SEC/ENDCARD_SEC）から
      同関数で再計算し 22194 に一致することを assert する。

[4] runtime_band ≤ 750s の assert（BLOCKING）:
    総尺 = 739.8s = 12:19.8 は band 690–750（11.5–12.5分）の内側（上限 750s に対し 10.2s の余裕）    ✓ PASS
    ※ hookSeconds=8.0 を採用したので余裕は EP45（23.6s）より薄い。narrationSeconds が実測で伸びたら再検算（BLOCKING）。
```
> **VO 実測で確定:** `measure_vo_wpm`（合格帯 168–190 wpm）でナレ実測。実測が SPEC マスターと乖離したら CODEX_B は `narrationSeconds` を実測値で更新（planning は 719.3・final は実測が権威）。190超は破棄・speed 0.95 で再発注（BLOCKING）。総尺 739.8s は ≤750 に対し余裕 10.2s しかない＝**実測が伸びたら endcard/teaser を削らず narration speed を確認**。

## 3.1b 秒×アニメーション・タイムライン（★全区間・各beat の start/end フレーム・移動量・easing・damping・stagger・Trail）

> **フレームは全て `f(sec)=Math.round(30×sec)`。等速線形ゼロ・opacity 単独ゼロ・静止フレームゼロ。** 下表は §3.2 の S01..S48 の主アニメを区間単位で示す。カット境界は `QUANT=f(0.5)=15f` グリッドにスナップ（§10.1）。still は Ken Burns（`scale 1.00→1.08`＋drift ±24px・`Easing.out(Easing.cubic)`）を全長。テキスト見出し/figures は `overflow:hidden` 親＋子 `translateY(110%→0)` の spring 切れ上がり（`damping:16,mass:1`・スタッガー `f(0.04)=2f/文字`）を基本形。★fast move（Trail 対象）は「Trail」列に明記。

| 区間(秒) | 開始f–終了f | シーン | 主アニメ（プロパティ・移動量） | easing / damping | stagger | Trail |
|---|---|---|---|---|---|---|
| 0.0–8.0 | 0–240 | HOOK TEASER（無音・~1.3s 最速カット） | 象徴フラッシュ（道→ベルト→手錠→booking フラッシュ）hard cut・各カット微 KB `scale 1.00→1.03` | `Easing.out(Easing.cubic)` | — | **✓**（手錠/フラッシュ） |
| 8.0–20.0 | 240–600 | S01 テキサス二車線の道（HOOK 開幕） | still Ken Burns `scale 1.00→1.06` / drift +18px 右（陽炎） | `Easing.out(Easing.cubic)` | — | — |
| 20.0–33.5 | 600–1005 | S02 外れたシートベルトのバックル（i2v M01: 揺れる） | i2v native ＋ 追い足し `scale 1.00→1.03` | native + cubic | — | — |
| 33.5–47.0 | 1005–1410 | S03 ピックアップのダッシュ＋空のチャイルドシート2つ | still `scale 1.00→1.07` / drift +20px | `Easing.out(Easing.cubic)` | — | — |
| 47.0–53.0 | 1410–1590 | S04 開く手錠（i2v M02: swing open・**fast**）→SILENCE 1.8s 前半 | i2v native ＋ swing・数値見出しなし | native | — | **✓** |
| 53.0–58.6 | 1590–1758 | S05 booking カメラのフラッシュ／壁時計（静止保持→SILENCE 1.8s） | still `scale 1.00→1.04`・完全無音の画 | `Easing.inOut(Easing.sin)` 微動 | — | — |
| **58.6–62.1** | **1998–2103** | **BrandOpening 3.50**（Bookends・不変・gold 解決） | — | — | — | — |
| 62.1–90.0 | 2103–2700 | S06 Lago Vista の湖畔の小さな町（OP establishing・factory） | factory 内在動き＋微 KB `scale 1.00→1.04` | `Easing.out(Easing.cubic)` | — | — |
| 90.0–110.0 | 2700–3300 | S07 最高裁の淡い大理石列柱（2001 の答え） | still push-in `scale 1.00→1.08` / drift +12px 上 | `Easing.out(Easing.cubic)` | — | — |
| 110.0–126.1 | 3300–3783 | S08 手前に$50の切符・奥に遠い最高裁列柱（距離）＋acttitle | acttitle `THE STOP` 切れ上がり・still KB | spring `damping:16,mass:1` | 2f/文字 | figure reveal **✓** |
| 126.1–150.0 | 3783–4500 | S09 ピックアップ車内・空のチャイルドシート2つ（ACT1・子は象徴のみ） | still KB・`lowerthird` "a seatbelt violation — fine only, no jail"（F-LT） | spring `damping:20,mass:1` | — | — |
| 150.0–175.0 | 4500–5250 | S10 squad car のドアが閉まる（i2v M05: swing shut・**fast**）＋S11 巡回車の影 | i2v swing・`mechanism:closingdoor`（F-MECH1） | native + spring | — | **✓** |
| 175.0–205.0 | 5250–6150 | S12 手錠（フェンス杭/ハンドル上の象徴）＋S13 station の扉 | still KB・`kinetic:emphasis` "NO JAIL. EVER." (["NO"]・F-KIN)・F-LT "Officer Bart Turek" | spring `damping:16` | 2f/文字 | **✓** |
| 205.0–235.0 | 6150–7050 | S14 booking 台（脱いだ靴・所持品トレー）＋S15 指紋/撮影台 | still KB・drift ±24px 交互・stamp/指紋 i2v なし | `Easing.out(Easing.cubic)` | — | — |
| 235.0–262.0 | 7050–7860 | S16 無人の holding（institutional・鉄格子なし）＋S17 治安判事のベンチ/bond 票 | still KB・`mechanism:closingdoor`（能力を問われぬまま閉じる・F-MECH2） | `Easing.out(Easing.cubic)` | — | door **✓** |
| 262.0–275.8 | 7860–8274 | S18 $50の切符／no contest 票（ACT1 締め）・stat F-STAT1 | figure `stat` value 50→settle（prefix "$", label "the entire penalty · no jail"）・count ease-out | `Easing.out(Easing.cubic)` | — | tick **✓** |
| 275.8–310.0 | 8274–9300 | S19 第4修正のページ（判読不能）＋S20 §1983 の法律書・ACT2 幕頭 | acttitle `THE 1983 QUESTION` 切れ上がり・F-LT "42 U.S.C. § 1983" | spring `damping:16` | 2f/文字 | **✓** |
| 310.0–345.0 | 9300–10350 | S21 天秤: citation form ↔ handcuffs＋S22 "reasonable" の語 | `compbars` [{"a fine-only offense",1},{"a full custodial arrest",1}]（F-CMP1）barX `scaleX 0→1` | spring `damping:18` origin left | — | — |
| 345.0–380.0 | 10350–11400 | S23 天秤が傾く（i2v M09: tip・**fast**）＋S24 無人の法廷ベンチ | i2v native ＋ `mechanism:faultsplit`（fine-only ↔ arrest の線・F-MECH3） | native + `Easing.out(Easing.cubic)` | — | line cross **✓** |
| 380.0–412.5 | 11400–12375 | S25 filing stamp＋S26 courthouse 廊下（factory）＋S27 probable cause の視点 | still KB・`lowerthird` "probable cause — undisputed"（F-LT）・F-LT "The Fourth Amendment" | spring `damping:20` | — | stamp **✓** |
| 412.5–437.0 | 12375–13110 | S28 対向する2本の矢印（two clean arguments）＋S29 citation 本 vs cell key | `kinetic` "TWO ARGUMENTS, ONE QUESTION"・still KB | spring `damping:16` | 2f/文字 | **✓** |
| 437.0–455.0 | 13110–13650 | S30 あらゆる運転者/歩行者の道（ACT2 締め・普遍性） | still push-in `scale 1.00→1.06` | `Easing.out(Easing.cubic)` | — | — |
| 455.0–490.0 | 13650–14700 | S31 最高裁の9席のベンチ（ACT3 幕頭・荘厳・最も遅い）＋acttitle | acttitle `THE RULING` 切れ上がり・F-LT "Atwater v. City of Lago Vista, 2001 · 532 U.S. 318" | spring `damping:16` | 2f/文字 | **✓** |
| 490.0–512.0 | 14700–15360 | S32 5-4 の投票（"five" で解決・votetally F-VOTE） | `votetally` 5-4 settle（**"THE ARREST STANDS · UPHELD" 対語・R-DISPO**）・drift +12px | `Easing.out(Easing.cubic)` | — | tick **✓** |
| 512.0–540.0 | 15360–16200 | S33 最高裁列柱（factory establishing）＋S34 古い革表紙の法律書（Souter 歴史） | factory 内在＋微 KB・長ディゾルブ 10f | `Easing.out(Easing.cubic)` | — | — |
| 540.0–566.0 | 16200–16980 | S35 建国期のルールの古い巻＋S36 bright-line（一本の清い線）＋走光 i2v M12 | still push-in `scale 1.00→1.08`＋i2v 光帯 native・長ディゾルブ | native + `Easing.out(Easing.cubic)` | — | — |
| 566.0–592.0 | 16980–17760 | S37 路肩の一瞬の判断（i2v M13: 光が走る・緩）＋S38 開いた意見集: Souter "pointless indignity" 逐語 quote F-QUOTE1 | i2v native ＋ `quote` maskslide（帰属 **Justice Souter, for the Court**） | native + `Easing.out(Easing.cubic)` | 2f/語 | — |
| 592.0–618.0 | 17760–18540 | S39 立法へ開く扉（Souter の救済＝立法・F-MECH4 gears）＋S40 O'Connor 反対の開いた本 | `mechanism:gears`（棚の権利が部屋に入らない）・`kinetic:emphasis` "LEFT TO LEGISLATURES" (["LEGISLATURES"]) | spring `damping:16` | 2f/文字 | **✓** |
| 618.0–644.0 | 18540–19320 | S41 立法へ開く扉 vs 閉じた憲法の扉（i2v M15: 扉・**fast**）＋O'Connor 逐語 quote F-QUOTE2 | i2v swing ＋ `quote` maskslide（帰属 **Justice O'Connor, dissenting**） | native + `Easing.out(Easing.cubic)` | 2f/語 | **✓** |
| 644.0–668.0 | 19320–20040 | S42 four votes（負けた側）＋S43 最高裁が引いた線（ENDING 手前） | `kinetic` "FOUR VOTES, NOT FIVE"・still KB | spring `damping:16` | 2f/文字 | **✓** |
| 668.0–700.0 | 20040–21000 | S44 テキサスの道に戻る＋S45 外れたシートベルト＋S46 州法の条文本（ENDING） | still KB・`kinetic:emphasis` "THEY MAY, NOT MUST" (["MAY"])・F-LT "the remedy: left to legislatures" | spring `damping:16` | 2f/文字 | **✓** |
| 700.0–716.0 | 21000–21480相当 | S47 州境地図（protected / not）＝Atwater の rule なお立つ | `lowerthird` "the rule of Atwater still stands"・still KB drift ±16px | `Easing.out(Easing.cubic)` | — | — |
| 716.0–719.3 | 21480–21417相当 | S48 開く扉→夜明けの採光（i2v M16・pull-back・payoff）→CTA→BrandEndcard 21417 開始 | i2v native ＋ slow `scale 1.00→1.02` pull-back・字幕のみ | native + `Easing.out(Easing.cubic)` | — | — |

> **★背面レイヤーは常に4層以上動く（§8.1）。** 上表の各 0.5s 境界で「動いている要素」が最低1つある（静止区間ゼロ）。Trail 対象（fast move）は **TEASER の手錠/フラッシュ / S04 開く手錠 / S10 squad car ドア closingdoor / S16 booking 扉 / S23 天秤 tip=faultsplit / S25 stamp / votetally・stat の桁 / 幕頭 acttitle・kinetic の切れ上がり**。**S01/S07 の荘厳 push-in・S05/S48 の時計/夜明け・S35–S37 の走光・Ken Burns には Trail をかけない**（無駄な残像・扇情を避ける・C5）。

## 3.2 シーン→幕の割当（★SPEC の S01..S48 を固定・別番号を発明しない・48シーン）

各シーンは narrative beat。225カットを 48シーンに分散（平均 4.69カット/シーン）。`primary` は各シーンの主素材（still=SDXL 各1枚 / factory=実写 / motion=i2v）。ambient/繋ぎは factory を各シーンに撒く（§5.1）。**象徴のみ・6制約順守・Atwater/子ども/Turek 非人物化。絵コンテ級の記述は §9。**

> **★2つの `Sxx` 名前空間は別物（取り違え禁止）:** 本節の **narrative シーンは `S01..S48`**（この表の絵コンテ）。一方 **still 資産 ID は `S01..S85`**（CODEX_A・1プロンプト=1枚で48シーンに85枚を配分）。同じ `Sxx` 表記でも DESIGN §3.2/§9 の Sid（narrative）と CODEX_A/asset_manifest の scene_id（still 資産 ID）は指すものが異なる。横断参照時は「どちらの空間か」を明示し、cross-map しない。

| Sid | 幕 | 内容（象徴・6制約） | primary |
|---|---|---|---|
| S01 | HOOK | テキサスの片側二車線の午後の道・陽炎・車も人もほぼ見えない（現在形の開幕） | still |
| S02 | HOOK | 外れたシートベルトのバックルがぶら下がって揺れる（i2v: 揺れる）＝唯一の"違反" | **motion** |
| S03 | HOOK | ピックアップのダッシュ＋助手席側に空のチャイルドシート2つ（子は象徴のみ・扇情なし） | still |
| S04 | HOOK | 開く手錠（i2v: swing open・切符でなく手錠へ・**fast**）＝反転の瞬間 | **motion** |
| S05 | HOOK | booking カメラのフラッシュ／壁時計（静止保持・SILENCE 1.8s の画・hard cut で BrandOpening へ） | still |
| S06 | OP | オースティン北・湖畔の小さな町 Lago Vista の establishing（factory ambient） | factory |
| S07 | OP | 最高裁の淡い大理石列柱＝2001 に答えた court（正対・荘厳・遠い） | still |
| S08 | OP | 手前に$50の切符1枚・奥に遠い最高裁列柱＝小さな切符から最高裁までの距離 | still |
| S09 | ACT1 | ピックアップ車内・空のチャイルドシート2つ・外れたベルト（罰金のみの違反） | still |
| S10 | ACT1 | 路肩に停まる squad car のドアが閉まる（i2v: swing shut・**fast**） | **motion** |
| S11 | ACT1 | トラックの窓辺に立つ officer の影/後ろ姿（顔なし・指さす影） | still |
| S12 | ACT1 | フェンス杭/ハンドル上に掛かった手錠＝身体を描かず逮捕を象徴 | still |
| S13 | ACT1 | 平凡なレンガの警察署の扉（institutional・入口） | still |
| S14 | ACT1 | booking 台に並ぶ脱いだ靴・所持品トレー（象徴・判読不能） | still |
| S15 | ACT1 | 指紋台と booking カメラ（無人・冷灰） | still |
| S16 | ACT1 | 無人の holding（institutional・鉄格子/独房を描かない・冷灰） | still |
| S17 | ACT1 | 治安判事のベンチと bond の紙（判読不能）＝about an hour ののち解放 | still |
| S18 | ACT1 | 机上の$50の切符／no contest 票（判読不能・stat F-STAT1・罰金のみ） | still |
| S19 | ACT2 | 開いた第4修正のページ（判読不能・"reasonable" が核）＝法理の問い | still |
| S20 | ACT2 | §1983 の連邦法の古い法律書＝普通の人が政府を訴える道具 | still |
| S21 | ACT2 | 天秤の左に citation form・右に手錠（罰金のみ ↔ 全逮捕・compbars F-CMP1） | still |
| S22 | ACT2 | 大きく刻まれた語 "REASONABLE" の抽象（判読不能寄り・4A の判定語） | still |
| S23 | ACT2 | 天秤が傾く（i2v: tip・faultsplit の線・**fast**）＝どちらへ傾くか | **motion** |
| S24 | ACT2 | 無人の法廷ベンチと手すり＝案件が判断される room | still |
| S25 | ACT2 | filing stamp（提訴の押印・無人机） | still |
| S26 | ACT2 | 冷光の長い courthouse 廊下（factory ambient・案件が上がる通路） | factory |
| S27 | ACT2 | 巡回車の窓越しの視点＝probable cause（争いなし）の象徴 | still |
| S28 | ACT2 | 対向する2本の矢印（two clean arguments・判読不能ラベル） | still |
| S29 | ACT2 | citation 本 vs cell key＝切符で帰す道と拘置する道 | still |
| S30 | ACT2 | あらゆる運転者/歩行者が通る空の道＝この問いは全員に触れる（ACT2 締め） | still |
| S31 | ACT3 | 最高裁の9席のベンチ（正対・荘厳・最も遅い・ACT3 幕頭） | still |
| S32 | ACT3 | 5-4 の投票が "five" で解決するバロット（votetally F-VOTE・**UPHELD 対語**） | still |
| S33 | ACT3 | 夜の最高裁の列柱・大理石（factory ambient・establishing） | factory |
| S34 | ACT3 | 暖い机上に閉じた古い革表紙の判例集（Souter の歴史・判読不能） | still |
| S35 | ACT3 | 建国期のルールの古い巻＝令状なし逮捕を禁じる確たる伝統は無い（判読不能） | still |
| S36 | ACT3 | 大理石面に引かれた一本の清い線＝bright-line（明確な規則） | still |
| S37 | ACT3 | 大理石を走る刻印風の光の帯（i2v: 光が走る・緩）＝路肩の一瞬の判断/歴史の収斂 | **motion** |
| S38 | ACT3 | 暖ランプ下に開いた意見集の抽象行＝"pointless indignity" の一節（quote F-QUOTE1・帰属 Souter 多数） | still |
| S39 | ACT3 | 立法府（州議会）へ開く扉＝救済は立法に委ねられた（mechanism gears） | still |
| S40 | ACT3 | 反対意見側に開いた別の意見集＝O'Connor 反対の書 | still |
| S41 | ACT3 | 立法へ開く扉 vs 固く閉じた憲法の扉（i2v: 扉・**fast**）＝right vs remedy（quote F-QUOTE2・帰属 O'Connor 反対） | **motion** |
| S42 | ACT3 | 4票が並ぶが5票に届かない象徴（four votes, not five・負けた側・判読不能） | still |
| S43 | ACT3 | 最高裁が引きなお消していない一本の線（ENDING 手前・the line drawn） | still |
| S44 | ENDING | テキサスの道に戻る＝あなたの車と午後（現在形・payoff の起点） | still |
| S45 | ENDING | 外れたシートベルトのバックル再掲＝最小の違反 | still |
| S46 | ENDING | 州法の条文本＝救済は憲法でなく州の statute にある | still |
| S47 | ENDING | 州境で "protected / not" に分かれる壁地図（判読不能ラベル）＝州次第 | still |
| S48 | ENDING | 夜明けに開く扉から採光が育つ・slow pull-back（i2v: 戸が開き光が育つ・payoff） | **motion** |

**source 集計（scene-primary）:** motion-primary **7**（S02 S04 S10 S23 S37 S41 S48）／factory-primary **3**（S06 S26 S33）／still-primary **38**。**scene-primary はカット全体の一部**で、残りは §5.1 の配分に従い CODEX_B の shotlist が 225 カット（still 101 / factory 92 / motion 32）へ機械展開する。**この表のシーン数・番号は固定（S01..S48）。**

---

# 4. 音の4層設計（ナレ / BGM / SFX / 環境音）

## 4.1 ラウドネス・voice（確定値・EP41〜46 と同一運用）

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

台本の `【SILENCE 1 — 1.8s】` は**ナレの沈黙であって音の沈黙**（台本指定「Hold on the loose seatbelt swinging. No music.」＝完全無音）。EP47 は明示指定が1箇所（HOOK 末）。

| 位置 | 秒 | 対応画 | 鳴らすもの |
|---|---|---|---|
| HOOK 末（"loose seatbelt swinging" で保持→hard cut で BrandOpening へ） | **1.8** | S05（booking フラッシュ／時計・S04 の揺れるベルト） | BGM mute。**完全無音**（room tone も置かない・台本指定「No music」） |

**最長無音候補 1.8秒 << 25秒** ✓ `bgm_present` PASS。加えて **HOOK TEASER preroll（0–8.0s）は BGM 低弦のみ**（ナレなしだがデジタル無音にはしない）。

## 4.3 章ごとの BGM（1章1トラック・`build_atwater_bgm_real.py`＝EP43 系を atwater 用に複製・film_offset 適用・OFF は実測）

| 区間 | 性格 | 楽器 |
|---|---|---|
| HOOK TEASER / HOOK | 低弦の不解決・現在形の緊張・単音が刺す（道・外れたベルト・開く手錠） | 低弦+単音メタル |
| OP | ブランドスティンガー（`BrandOpening` 付属） | — |
| ACT1 | 最短・現在形・抑制。刻みは疎で近い（the stop） | 低弦+疎パーカッション |
| ACT2 | 転回。法理の冷たい正対（reasonable の問い） | ピアノ+弦 |
| ACT3 | 法の荘厳・大理石。**最も遅い**。5-4 の重さと "pointless indignity but permitted" の緊張 | 低弦+弦サステイン |
| ENDING | 解決しない和音 →「daylight」でだけ暖色（採光）に開く（they may, not must の余韻） | ピアノ+弦 |
| ENDCARD | ブランドED（`BrandEndcard` 付属） | — |

## 4.4 SFX（非扇情・C5）

| 種別 | 位置 | 音 |
|---|---|---|
| road ambient | S01/S44 | テキサスの午後の道の風・遠い車・-30 LUFS |
| seatbelt buckle | S02/S45・SILENCE HOOK末 | バックルの軽い金属音・-24 LUFS（沈黙区間は完全無音のため置かない） |
| handcuffs | S04/S12/TEASER | 手錠のラチェット音・-18 LUFS（サイレン/悲鳴/子の声なし・非扇情・C5） |
| squad car door | S10 | 車ドアの institutional な閉・-18 LUFS |
| booking flash / clock | S05/S15 | カメラフラッシュの微音・秒針 tick・-26 LUFS（沈黙区間は tick も置かない） |
| stamp | S25 filing | 押印の一撃・-16 LUFS |
| scale tip | S21/S23 天秤 | 皿が傾く低い軋み・-22 LUFS |
| marble / columns | S07/S31/S33 | 大理石ホールの広いリバーブ・-30 LUFS |
| light band | S37 走光 | 微かな高域の走光音・-26 LUFS |
| door open | S39/S41/S48 | 開く扉の軋み・採光の外気・-18 LUFS |
| impact | AE m01/v01 の数値着地 | 低域インパクト・-12 LUFS |
| tick | votetally/stat の桁変化 | 微細クリック・-24 LUFS |
| room tone | 全編ベッド（道・booking 冷灰・大理石反響） | 広いリバーブ・-30 LUFS（**SILENCE 1 は完全無音**） |

---

# 5. ビジュアル — 素材積算（★紙芝居回避＝factory実写を必ず混ぜる・1シーン1枚）

## 5.1 素材の積算（★SPEC の値をそのまま満たす配分）

```
[0] 絵が必要な区間 = narrationSeconds 719.3（BrandOpening/Endcard/teaser は別レイヤー）
[1] 総カット = 225（SPEC）    719.3 / 225 = 3.197秒/カット  ✓ mean_shot 3.19（≤6.0）
[2] 素材内訳（★SPEC の distinct/cuts をそのまま・1シーン1枚）
    still（SDXL）    85 distinct → 101 カット（16枚が2回・69枚が1回・mean 1.19・cap 2）★各1枚生成
    factory 実写     92 distinct →  92 カット（各1回・cap 1）
    i2v モーション    16 distinct →  32 カット（各2回・cap 2）
    -----------------------------------------------
    distinct 合計   193          → 225 カット
[3] first-use share = 193 / 225 = 0.8578   ✓ ≥0.70（SPEC 一致）
[4] footage_diversity distinct/total = 0.8578   ✓ ≥0.40
[5] 最大使用回数: still 2 / factory 1 / motion 2   ✓ 各 cap 内
[6] 静止画占有率（★紙芝居ゲート）: still-cut 101 / 225 = 0.4489 = 44.89%   ✓ ≤45%（余裕 0.11%pt）
[7] motion coverage: (factory 92 + i2v 32) / 225 = 124/225 = 0.5511   ✓ ≥0.45
[8] factory 下限 = 719.3/30 = 24.0 → ≥24本。設計値 92本   ✓
```
> **[6] の余裕は 0.11%pt しかない（EP45 の 0.36%pt より薄い）。still-cut を1つ増やすと 45% を割る。still-cut は 101 で固定**（16枚だけ2回・残り69枚1回）。QC で still が 85枚を割ったら §9 の**追加は同一シーンの別プロンプト（新規 distinct）**で回復させ、**cut 数は増やさない**。**still を増やして factory を削るな。factory 92 が still-share≤0.45 を守る下限。**

## 5.2 SDXL と実写在庫の振り分け

- **SDXL（still 85・各1枚）= この事件にしか無い固有物**: テキサスの道・外れたベルト・空のチャイルドシート・ダッシュ・開く手錠・booking 台/靴/所持品/指紋台/フラッシュ・holding・治安判事のベンチ・$50の切符/no contest 票・第4修正のページ・§1983 の本・天秤（citation↔手錠）・"reasonable" の語・法廷ベンチ・filing stamp・矢印2本・citation 本 vs cell key・最高裁9席・5-4 バロット・古い判例集/建国期の巻・bright-line・意見集（Souter/O'Connor）・開く扉と閉じた扉・four votes 象徴・州法本・州境地図・夜明けの戸。
- **factory 実写 92 = どこにでもある周辺**: Lago Vista/湖畔の町・courthouse 外観・列柱・大理石テクスチャ・長い廊下・テキサスの道路 ambient・夜明けの街・ambient 繋ぎ。

## 5.3 SDXL 生成量（★バリエーション0・variants 禁止）

- `ai_prompts.v001.md` = **body 85行の固有プロンプト**（still 各1枚）＋ i2v 種 **16行** ＝ **計101エントリ**（`--only S01` の `shots=` は 101）。`generate_sdxl_4k.py PD-2026-047-atwater`（**`--variants 1` または指定なし**）。**`--variants 3` を書かない。**
- i2v-source = **16枚**（動きが意味を持つ絵の固有プロンプト・各1シード）。CODEX_A が Wan 2.2 A14B → RIFE 48fps で 16本生成。
- **総生成 = still 85 + i2v seed 16 = 101枚（各1回）。** factory 92 は生成せず在庫選抜。
- プロンプト実体（85本）・i2v リスト（16）・factory 選定（92）は **CODEX_A** の担当（本書 §9 は絵コンテ級の記述と共通スタイル/ネガティブの契約のみ）。

## 5.4 factory のファイル名を信じない（★必須工程・CODEX_A・BLOCKING）

> EP36: `city_surveillance_camera_dome` が実際は大聖堂。EP38: 牛が `documents_on_desk`。ラベルは検索語の記録であって中身の保証ではない。

選定した **92本すべて**を `scripts/build_footage_contact_sheet.py --ep PD-2026-047-atwater --media video --dir <factory staging>` で1本1フレームのラベル付きコンタクトシートにし**全点目視**。subtype と食い違う本は差し替える。`select_atwater_factory.py --verify-no-prior-overlap` で EP39〜46 の sha256 被りゼロを確認。

## 5.5 共通スタイル接尾（各 SDXL プロンプト末尾に必ず付ける・`[STYLE]`・CODEX_A と同一）

```
, cinematic still, warm-and-cold documentary grade, a dusty two-lane Texas afternoon and a pickup-truck cab under warm hazy daylight where an unbuckled seatbelt hangs loose, set against cold grey institutional booking interiors and pale marble Supreme-Court colonnade in fluorescent and daylight, a single civil-violet accent as the one cool note, restrained and dignified symbolism, telephoto compression and frontal composition, shallow depth of field, ultra-detailed, photoreal, 4K, 16:9, fine film grain, no text, no watermark, no logo, symbolic still-life, no people, no visible face, two empty child seats as symbols only
```
> EP39〜46 との分離: 接尾に `electric blue`（EP39）・`midday suburban`（EP40）・`sodium prison corridor`（EP41）・`warrant-blue`（EP42）・`porch-amber`/`ambulance`（EP43）・`teal-green hospital`（EP44）・`crimson overdue`（EP45）・`forest-green`（EP46）を**1語も含めない**。EP47 の唯一の差し色は **civil-violet `#7A5CD0`**。

## 5.6 共通ネガティブ（各 SDXL プロンプトの `Avoid:` に必ず付ける・`[NEG]`・CODEX_A と同一）

```
text, words, letters, numbers, captions, watermark, logo, readable document, legible ticket, legible citation, legible license number, legible dollar amount, legible date, real celebrity, recognizable real person, identifiable face, portrait, mugshot, likeness of a specific person, human face, human body, child, child's face, crying child, frightened child, weeping family, sensational distress, poverty porn, weapon, gun, blood, gore, violence, nude, bare skin, cartoon, illustration, anime, 3d render, low quality, blurry, jpeg artifacts, deformed, extra limbs, barred cell, steel cellblock, sodium prison corridor, navy interrogation room, electric blue, teal-green hospital corridor, clinical hospital, midday suburban daylight, porch amber house, ambulance, ankle monitor, body-worn camera, crimson overdue notice, forest-green
```
> ネガティブにも **制約違反語（"the arrest was illegal", "struck down", "unconstitutional arrest", poverty porn 語, 子の年齢等）を書かない**（§1.3）。会社/機関ロゴが必要な絵は「blurred into an unreadable smear」で判読不能に。判例番号・日付・金額・票数・1997・子の年齢を画に描かない（AE/figures＝B の担当）。**手錠・booking・holding は institutional で非扇情に**（鉄格子/独房/暴力を描かない・C5）。**子どもは空のチャイルドシートで象徴のみ**（人体を描かない）。

## 5.7 AI開示（強め・毎回・R1）

AI 生成の still・i2v が画面に出ている間、常時右下に **`AI-assisted visualization`**。Oswald 20px / `#C8CDD6` / opacity 70% / 位置 `[W-32, H-28]`。字幕帯と縦 56px 以上離す。概要欄1行: `Some visuals in this film are AI-assisted reconstructions, not photographs of the actual events.`（＋あなたの州の「minor-offense で citation か arrest か」を定める statute を確認する中立の1行）。

## 5.8 ★A↔B 境界契約（asset_manifest スキーマ・EP39〜46 の不整合を最初から潰す）

- **接続点は `episodes/PD-2026-047-atwater/05_visuals/asset_manifest.v001.json` ただ1ファイル**。A(producer)＝CODEX_A が書き、B(consumer/validator)＝CODEX_B が読む。**counts と role enum を A/B で一字一致**させる。
- **スキーマ版:** `atwater_assets.v1`（固定文字列）。
- **マニフェスト配列（★A/B 同一）:** `stills` / `motion` / `factory` / `overlay` の4配列。**★全エントリを記載**（stills85＋factory92＋motion16＋overlay12・public_path 必須＝EP45事故回避）。
- **counts オブジェクト（★このキー・値で固定・A/B 一字一致）:** `{ "still_body": 85, "still_i2v_source": 16, "motion": 16, "factory": 92, "overlay": 12 }`。cuts 展開は still 101 / factory 92 / motion 32。
- **`stills[].role` enum（★この3値のみ・A/B 同一・`thumb`/`still_thumb` を作らない）:** `body` / `i2v_source` / `reject`。asset_id は body `^ATW-S\d{2}$`（S01..S85）/ i2v種 `^ATW-MS\d{2}$` / motion `^ATW-M\d{2}$`。
- **サムネは `role="body"` かつ `also_thumb=true` の body still ちょうど6枚**（別 role を作らない・追加生成しない）。**候補集合（★still 資産 ID 空間・A↔B 契約点）:** **`{S01, S03, S18, S46, S68, S85}`**。A・B は同一6 asset ID に `also_thumb:true` を立てる。
- **overlay 枚数も A/B 一致**（合成レイヤー・distinct 素材に数えない）。本書設計値 **overlay: 12**（particle/light/vfx）。CODEX_A/CODEX_B は共に overlay=12 で書く。
- CODEX_A は manifest を書いた直後 `build_atwater_asset_manifest.py --verify`（複製）で counts / role / also_thumb / overlay を突き合わせ、**A の値と B の期待が一字一致**であることを確認（不一致は BLOCKING）。**`also_thumb==true` の scene_id 集合が `{S01,S03,S18,S46,S68,S85}` で A↔B 同一**であることも検査する。

---

# 6. Remotion MGビート（FigureBeats）— ★密度下限 30 は必ずここで満たす・dochighlight 不使用

## 6.1 密度の設計（`atwater_film.json` の `figures[]`）

`check_motion_density`: 3つを AND。**body-minutes = narrationSeconds/60 = 719.3/60 = 11.988**。

| 指標 | floor | EP47 設計値 |
|---|---|---|
| density | ≥2.5/min | figures **36 beats / 11.988 = 3.00/min** ✓（SPEC beats_floor 30 に +6） |
| coverage | ≥0.25 | 36 beats × 平均 5.4秒 = 194.4秒 / 719.3 = **0.270** ✓ |
| variety | ≥3 distinct forms | **9種**（下記） ✓ |

> **AE の 8枠は film.json に入れない**（composite 後に焼くため gate 非カウント）。**density は Remotion 側 36 beats だけで 30 を超える。** coverage が floor 0.25 に一番近いので figures の dur は 4.8–6.0s を基本にする。

## 6.2 `figures[]` の種類配分（★kind は全部小文字・同一 kind を連続させない・★dochighlight 不使用）

**使用可能 kind（全小文字）:** `numberticker` `stat` `votetally` `timeline` `quote` `kinetic` `lowerthird` `acttitle` `compbars` `mechanism`。**大文字は無音描画になる。** **★`dochighlight` を1件も入れない（R-DOCHL・grep 0）。切符/命令/書類は `lowerthird` の説明テキストで表す。** `comparebars` は非実在→`compbars` が正。

| kind（小文字） | 枠数 | EP47 での用途（6制約適用） |
|---|---|---|
| `acttitle` | 3 | ACT1「THE STOP」/ ACT2「THE 1983 QUESTION」/ ACT3「THE RULING」 |
| `lowerthird` | 14 | 開示 `AI-assisted visualization`（HOOK/ENDING 2回）／"LAGO VISTA, TEXAS"（**1997 は焼かない**・R-HEDGE）／"a seatbelt violation — fine only, no jail"（$25–$50・N02）／"Officer Bart Turek"（人物化せず名のみ）／"42 U.S.C. § 1983"（N08）／"The Fourth Amendment — 'reasonable'"（N08）／"probable cause — undisputed"（A09）／"Atwater v. City of Lago Vista, 2001 · 532 U.S. 318"／"Justice David Souter — for the Court"／"the remedy: left to legislatures"（A15・C2）／"the rule of Atwater still stands"（C1・enforcement 枠でなく「なお有効」）／"many states limit minor-offense arrests by statute"（A15） |
| `kinetic` | 5（うち emphasis 3） | 「THE FIFTY DOLLAR ARREST」／「NO JAIL. EVER.」(["NO"]・N07)／「TWO ARGUMENTS, ONE QUESTION」／「THEY MAY, NOT MUST」(["MAY"]・C1)／「LEFT TO LEGISLATURES」(["LEGISLATURES"]・A15)。**emphasisWords は1–2語＝文字切れ回避** |
| `stat` | 3 | $50（**N01**・prefix "$", label "the entire penalty · no jail"）／$25–$50（TX 法定幅・label "Texas seatbelt fine"・N02）／"5-4"（票を stat 表示する場合の予備・votetally と重複しないよう ACT3 の別秒） |
| `compbars` | 2 | citation（fine-only offense）vs full custodial arrest（**F-CMP1**・天秤の対比・C1 中立）／"a warrantless arrest allowed wherever there is probable cause" vs "case-by-case penalty-weighing"（Souter の bright-line 対比・A13） |
| `quote` | 2 | ①Souter 逐語「Atwater's claim to live free of pointless indignity and confinement clearly outweighs anything the City can raise against it specific to her case」（**帰属 Justice Souter, for the Court**・F-QUOTE1・A14）②O'Connor 逐語「The Court neglects the Fourth Amendment's express command in the name of administrative ease. In so doing, it cloaks the pointless indignity that Gail Atwater suffered with the mantle of reasonableness」（**帰属 Justice O'Connor, dissenting**・F-QUOTE2・A17）。**要約を引用符に入れない・facts_lock で逐語確認・O'Connor を Court に帰属させない** |
| `timeline` | 2 | ①MARCH 1997（the stop・**発話のみ／画面の年は出さず"the stop"表記**）→ APRIL 24, 2001（the ruling・N04）②district court → en banc Fifth Circuit → Supreme Court（affirmed の手続・A20・年は出さない） |
| `votetally` | 1 | **5-4**（Souter 多数 4名参加／O'Connor 反対 3名参加・**F-VOTE**・必ず "THE ARREST STANDS / UPHELD" の対語を伴う・R-DISPO・C4 中立） |
| `mechanism` | 4 | `closingdoor`（squad car ドア・ACT1）／`closingdoor`（能力を問われぬまま閉じる booking の扉・ACT1）／`faultsplit`（天秤: fine-only ↔ full arrest の線・ACT2）／`gears`（棚の上の権利＝救済が立法の部屋へ移る・ACT3） |
| **合計** | **36** | variety = **9 figure-kinds** ✓ ≥3 |

> **★`dochighlight` を1件も置かない（R-DOCHL）。** `graphics[]=[]`（空配列）。density は `figures+graphics+heroCuts` を合算するので figures 36 だけで floor 30 に +6。

## 6.3 配置方針（36本・§1.4 台帳の値だけを焼く・kind を分散・6制約順守・dochighlight 0件・CODEX_B と一致）

- **HOOK/OP（3）:** `kinetic`（"THE FIFTY DOLLAR ARREST"）/ `lowerthird`（`AI-assisted visualization` 開示）/ `lowerthird`（"LAGO VISTA, TEXAS"・**1997 焼かない**）
- **ACT1（6）:** `acttitle`（THE STOP）/ `lowerthird`（"a seatbelt violation — fine only, no jail" / "$25–$50"・N02）/ `lowerthird`（"Officer Bart Turek"）/ `kinetic:emphasis`（"NO JAIL. EVER."・["NO"]・N07）/ `mechanism:closingdoor`（squad car ドア）/ `stat`（**N01** $50・label "the entire penalty · no jail"）＋`mechanism:closingdoor`（能力を問われぬまま閉じる扉）※ACT1 は6枠に closingdoor 2種を分離配置
- **ACT2（9）:** `acttitle`（THE 1983 QUESTION）/ `lowerthird`（"42 U.S.C. § 1983"・N08）/ `lowerthird`（"The Fourth Amendment — 'reasonable'"・N08）/ `compbars`（**F-CMP1** [{"a fine-only offense",1},{"a full custodial arrest",1}]・C1 中立）/ `mechanism:faultsplit`（天秤の線）/ `lowerthird`（"probable cause — undisputed"・A09）/ `kinetic`（"TWO ARGUMENTS, ONE QUESTION"）/ `compbars`（Souter bright-line 予告: [{"probable cause = arrest allowed",1},{"weigh the penalty first",1}]・A13）/ `timeline`（district → Fifth Circuit → Supreme Court・A20・年なし）
- **ACT3（13）:** `acttitle`（THE RULING）/ `lowerthird`（"Atwater v. City of Lago Vista, 2001 · 532 U.S. 318"）/ `votetally`（**F-VOTE 5-4**・"THE ARREST STANDS · UPHELD"・R-DISPO）/ `stat`（"5-4" 補助表示・別秒）/ `lowerthird`（"Justice David Souter — for the Court"）/ `quote`（Souter 逐語 → "Justice Souter, for the Court"・**F-QUOTE1**）/ `timeline`（the stop → APRIL 24, 2001・N04）/ `kinetic:emphasis`（"LEFT TO LEGISLATURES"・["LEGISLATURES"]・A15）/ `lowerthird`（"the remedy: left to legislatures"・C2）/ `mechanism:gears`（救済が立法の部屋へ）/ `quote`（O'Connor 逐語 → "Justice O'Connor, dissenting"・**F-QUOTE2**）/ `lowerthird`（"four votes, not five — the dissent lost"・C3/C4）/ `lowerthird`（"many states limit minor-offense arrests by statute"・A15）
- **ENDING（5）:** `kinetic:emphasis`（"THEY MAY, NOT MUST"・["MAY"]・C1）/ `lowerthird`（"the rule of Atwater still stands"・C1）/ `lowerthird`（開示 `AI-assisted visualization` 再掲）/ `lowerthird`（"protected only as strong as your state's statute"・A15）/ `mechanism`（`gears` の余韻 or `faultsplit` の州境・§9 S47）

## 6.4 配置ルール

1. **AE の 8区間（§7）と1秒でも重ならない**（`validate_atwater_beats.py`＝validate_caniglia_beats.py を複製・両方突き合わせ）。
2. 幕あたり配分: HOOK/OP=3 / ACT1=6 / ACT2=9 / ACT3=13 / ENDING=5（ACT3 が最長 189.0s なので厚め）。
3. **同じ kind を連続させない**（`mechanism` の直後に `mechanism` を置かない・ACT1 の closingdoor 2種は間に stat/kinetic を挟む）。
4. 1枠 **4.8–6.0秒**。
5. ACT3 の説明区間に `votetally`＋`quote`×2＋`timeline`＋`mechanism`＋`lowerthird` を分散し 20秒超の平坦区間をゼロに。
6. `quote` は**逐語のみ**（要約を引用符に入れない・R-QUOTE）。**Souter＝for the Court／O'Connor＝dissenting** を厳格帰属。
7. `figures[].*text*`/`lines[]`/`label`/`quote` は `facts_lock` 検査対象（「illegal/struck down」・1997・子の年齢・台帳外数値・**dochighlight** を出さない）。
8. **5-4 を焼く votetally/stat は同一 payload に "THE ARREST STANDS / UPHELD / CONSTITUTIONAL" を必ず持つ（R-DISPO）。** O'Connor 逐語 payload は必ず attribution "Justice O'Connor, dissenting"（R-QUOTE）。

## 6.5 密度の最終検算

```
Remotion figures 36（film.json 内・graphics 空）
  density  = 36 / 11.988 = 3.00/min   ✓ ≥2.5（SPEC beats_floor 30 → 36 で +6）
  coverage = 194.4s / 719.3 = 0.270    ✓ ≥0.25
  variety  = 9 forms                   ✓ ≥3
  dochighlight count = 0               ✓ R-DOCHL（grep 0）
AE hero 8枠は composite 後・gate 非カウント（上乗せの決め所）
```

---

# 7. After Effects ヒーロービート（8枠）— ★AEカードは密度に数えられない

## 7.1 大原則（★EP39/40 の致命傷を回避）

`check_motion_density` は **film.json の `figures` だけ**を数える。AE の 8枠は本編 mp4 に composite された後に焼き込まれるため gate は 0 カウント。→ **密度下限 30 は §6 の Remotion figures（36本）で満たす。** AE はその上に載る「決め所の数値/引用タイポ」。

## 7.2 パイプライン（EP42/43/44 で measured 済み・atwater 用に複製）

```
[1] Remotion で本編完成 → atwater_final_bgm.v001.mp4（音声ミックス済み・build_atwater_bgm_real.py→film_offset 適用）
[2] scripts/ae/build_atwater_hero_cards.py（＝build_caniglia_hero_cards.py を複製）が beats.json と atwater_hero.jsx を生成
[3] AfterFX -noui -r atwater_hero.jsx → 各ビートを 1920x1080@30fps の不透明 mp4 で書き出し
[4] scripts/ae/composite_atwater_hero.py（＝composite_caniglia_hero.py を複製）が ffmpeg overlay + enable='between(t,start,end)' で焼き込み
[5] 出力 → atwater_final_bgm.v002_ae.mp4（v001 は絶対に上書きしない・film_offset 適用）
```

## 7.3 AEカードデッキ（★8枚・§1.4 の確定数値のみ・6制約適用・数値は台帳照合・accent #7A5CD0）

> **★レイアウトは複製元が実装する8種のみ**（`DATE_STAMP`/`CENTER_STACK`/`MONEY_STACK`/`SPLIT_COMPARE`/`ACT_TITLE_CARD`/`QUOTE_CARD`/`VOTE_SPLIT`/`SEAM_TRANSITION`）。**この表と CODEX_B のデッキは id・レイアウト・N-ID が完全一致**（`validate_atwater_beats` が両方を突き合わせる）。上記8種以外の未実装レイアウト名は使わない。**EP47 は 5-4 が台帳にあるので `VOTE_SPLIT` を使用（EP45 と対照的）。`ACT_TITLE_CARD`（幕頭は Remotion `acttitle` が担う）/ `SEAM_TRANSITION` は §7.3 では未使用。** variety は使用6種で ≥3 を満たす。

| id | レイアウト（実装済み8種） | hero（主表示） | top / sub / bottom / attribution | 数値ID | 背景（象徴のみ・顔なし） | 尺 |
|---|---|---|---|---|---|---|
| **v01** | **VOTE_SPLIT** | **5 – 4** | top: **THE ARREST STANDS** / bottom: **A WARRANTLESS ARREST FOR A FINE-ONLY OFFENSE — UPHELD** | N03 | 最高裁の9席・列柱 | 6.5 |
| **f01** | **SPLIT_COMPARE** | **FINE-ONLY OFFENSE / FULL ARREST** | top: **WHAT THE LAW ALLOWED** / bottom: **PROBABLE CAUSE WAS ENOUGH** | N07 | 左=$50の切符 / 右=手錠 | 7.0 |
| **q01** | **QUOTE_CARD** | **"IT CLOAKS THE POINTLESS INDIGNITY GAIL ATWATER SUFFERED WITH THE MANTLE OF REASONABLENESS"** | attribution: **JUSTICE O'CONNOR, DISSENTING** | N06 | 反対意見側の開いた意見集 | 8.0 |
| **s01** | **QUOTE_CARD** | **"POINTLESS INDIGNITY"** | sub: **THE MAJORITY CALLED IT THIS — AND PERMITTED IT ANYWAY** / attribution: **JUSTICE SOUTER, FOR THE COURT** | N05 | 多数意見の開いた意見集 | 7.5 |
| **m01** | **MONEY_STACK** | **$50 MAX FINE** | top: **THE ENTIRE PENALTY** / bottom: **NO JAIL — EVER** | N01 | $50の切符／no contest 票 | 6.0 |
| **t01** | **DATE_STAMP** | **APRIL 24, 2001** | place: **SUPREME COURT · 532 U.S. 318** | N04 | 大理石の階段（判読困難） | 5.0 |
| **n01** | **CENTER_STACK** | **NO JAIL OFFENSE** | top: **A FINE-ONLY MISDEMEANOR** / bottom: **STILL A FULL CUSTODIAL ARREST** | N07 | 手錠＋切符 | 6.0 |
| **l01** | **SPLIT_COMPARE** | **A RIGHT / A REMEDY** | top: **THE FIX THE COURT LEFT YOU** / bottom: **LEFT TO LEGISLATURES — NOT THE FOURTH AMENDMENT** | N07 | 左=閉じた憲法の扉 / 右=立法へ開く扉 | 7.0 |

> **★行順＝start 昇順（時系列）:** `m01`(ACT1 $50) < `f01`(ACT2 fine↔arrest) < `n01`(ACT2 no-jail) < `v01`(ACT3 5-4) < `t01`(ACT3 判決日) < `s01`(ACT3 Souter 逐語) < `q01`(ACT3 O'Connor 逐語) < `l01`(ENDING 手前・right/remedy)。**start は §7.4 beats.json で section 窓からオフセットで算出しクランプ**するため、**本番 rendered base の秒で単調増加・重複ゼロ**を `validate_atwater_beats` が保証する。**この id・レイアウト・N-ID は CODEX_B デッキと一字一致。**
> **★q01（O'Connor QUOTE_CARD）の attribution は "JUSTICE O'CONNOR, DISSENTING"（R-QUOTE・C3）。逐語（A17）を1字も要約しない。O'Connor を Court に帰属させたら FAIL。** hero は§1.4 N06 の逐語一致（大小無視・表示は全大文字）。
> **★s01（Souter QUOTE_CARD）の attribution は "JUSTICE SOUTER, FOR THE COURT"（R-QUOTE・C2）。** sub に "…AND PERMITTED IT ANYWAY" を入れて「認めつつ許容」の nuance を保つ（C2）。hero は概念 "POINTLESS INDIGNITY"（Souter 逐語 N05 は figures F-QUOTE1 側で全文提示）。
> **★v01（VOTE_SPLIT 5-4）は bottom に "UPHELD"（R-DISPO）を必ず別レイヤーで焼く。「illegal / struck down / overturned」を書かない。** 5-4 を中立に（どちらが正義かを断じない・C4）。
> **どのカードにも「illegal / the Court struck it down / overturned / the arrest was wrong」・1997・子の年齢・dochighlight を書かない。** 数値ID＝台帳（§1.4）と一致必須。カウント終了から区間終端まで最低 1.20秒ホールド。em-dash は本文表示の `—` と異なり **beats.json ラベルでは ASCII `-` に置換**（AE の豆腐回避・§7.6）。

### 検算

```
[1] 8区間・本番 start 単調増加・重複ゼロ（build_atwater_hero_cards.py が section 窓オフセットで算出）
[2] HOOK TEASER(0–8.0) / HOOK(8.0–...) / BrandOpening / BrandEndcard に1秒も重ならない
[3] 合計 = 6.5+7.0+8.0+7.5+6.0+5.0+6.0+7.0 = 53.0秒 / 739.8 = 7.2%   ✓ 過剰でない
[4] レイアウト種類 = VOTE_SPLIT, SPLIT_COMPARE, QUOTE_CARD, MONEY_STACK, DATE_STAMP, CENTER_STACK = 6種（全て実装済み8種内）   ✓ ≥3
[5] figures[] 36枠と1秒でも重ならない（validate_atwater_beats.py が両方突き合わせ）
[6] dochighlight/comparebars レイアウトは存在しない（8種のみ）   ✓ R-DOCHL
[7] R-DISPO: v01 に "UPHELD" / R-QUOTE: s01="for the Court" q01="dissenting"   ✓
```

## 7.4 `beats.json`（`08_edit/ae_hero/beats.json`・`schema_version: "atwater_beats.v1"`）

各 beat に `id` / `layout` / `start` / `end` / `dur` / `still`(象徴 or null) / `hero` / `top` / `bottom` / `sub` / `caption`(**改行禁止・最大50字**) / `value` / `numKeys` / `blend_mode`(既定 "overlay") / `required` / `out` / `attribution`(**QUOTE_CARD=s01/q01 は必須**・§1.4 と一致・R-QUOTE)。**区間の秒は本番 rendered base（narration_index 由来）に一致させ、section 窓からオフセットで算出しクランプ。** 数値カード（$50）は `money_keys()` で表示文字列を Python 事前計算（JSX で算術しない＝EP38 確定ルール）。**5-4 は文字列（"5 - 4"）で焼く（票カウントの count-up はしてよいが二桁化しない）。**

## 7.5 レイアウト定義・色定数（EP43/44 を踏襲・色のみ EP47 値・CODEX_B と一致）

**共通レイヤースタック（下→上）:** L9 黒ソリッド → L8 静止画（scale fill→fill×1.08・drift）→ L7 グレードウォッシュ（**テキサスの埃 near-black** `addSolid([0.078,0.063,0.047])`＝DUST / MULTIPLY / opacity 30）→ L6 羽根付き楕円ビネット → L5 グロー（下中央 civil-violet 差し ADD）→ L4 ライトスイープ（`"ADBE Rotate Z"`=18）→ L3 上ラベル（Oswald）→ L2b アクセントライン（ACCENT violet・scaleX ワイプ・`motionBlur=true`）→ L2 主数値/主文字（Anton・ACCENT・`motionBlur=true`）→ L1b 下ラベル → L1 字幕ロワーサード → **L0b AI開示テキスト（`AI-assisted visualization`・Oswald 20px・SILVER `#C8CDD6`・opacity 70%・右下 `[W-32, H-28]`・全カード常時焼き＝R1）** → L0 黒シームディップ（head/tail 各4フレーム）。

**★EP47 色定数（0..1 float・civil-violet レーン色。EP41 gold / EP42 blue / EP43 amber / EP44 teal / EP45 crimson / EP46 green を流用禁止・CODEX_B と一致）:**
```python
ACCENT = [0.478, 0.361, 0.816]  # #7A5CD0 civil-violet — 数値・下線・唯一の差し色
WHITE  = [0.961, 0.969, 0.980]  # #F5F7FA
SILVER = [0.784, 0.804, 0.839]  # #C8CDD6（開示テキスト）
INK    = [0.039, 0.039, 0.047]  # #0A0A0C 近黒ルート（サムネ bg と一致）
DUST   = [0.078, 0.063, 0.047]  # #14100C テキサスの埃 near-black ウォッシュ
STEEL  = [0.133, 0.141, 0.165]  # #22242A booking 冷灰
MARBLE = [0.204, 0.212, 0.231]  # #34363B 大理石（ACT3）
```
**フォント:** 数値/主文字 = **Anton Regular** / ラベル・字幕 = **Oswald Medium**。`getFontsByFamilyNameAndStyleName` で厳格解決（miss は throw・フォールバック禁止）。テキスト幅は **`sourceRectAtTime(t,false).width` で実測**（advance-width 推定禁止＝EP40 文字切れの原因・ブリーフ§5）。**`m01`（MONEY_STACK）は$50を ACCENT violet、ラベルを WHITE/SILVER。`v01` の "UPHELD"・`s01`/`q01` の attribution・`l01` の "NOT THE FOURTH AMENDMENT" は削除禁止。**

**カウント型:** $50 は `money_keys()` で settle（ease-out cubic）＋ impact SFX。**5-4 は "5 - 4" の文字列（count-up は "0→5" / "0→4" の1桁のみ可）。逮捕を "illegal/struck down" とするラベルを一切作らない（R-DISPO）。**

## 7.6 このマシン固有の罠（★1つ忘れると無言で品質が落ちる・EP42-44 全項を atwater に適用）

フォント解決の例外ラップ（`psName()`・allFonts の array-LIKE ラッパーを unwrap）／spatial ease は配列次元1（`prop.isSpatial ? 1 : ...`）／OM=`"H.264 - レンダリング設定を一致 - 15 Mbps"`・RS=`"最良設定"`（英語名は try/catch フォールバック）／`app.newProject()` を headless で使わない（同名 `ATWATER_` コンプを防御削除）／`layer.motionBlur=true` を動くレイヤー個別に／回転は `"ADBE Rotate Z"`／改行は1行厳守（SPLIT_COMPARE/VOTE_SPLIT の左右2値は別レイヤー・改行禁止）／em-dash は `-`／inPoint と outPoint 両方設定／`item.mainSource.conformFrameRate = 30`／実行パス `C:\Program Files\Adobe\Adobe After Effects 2026\Support Files\AfterFX.exe`／`proj.gpuAccelType = GpuAccelType.SOFTWARE`／ビルド ~100–120秒・完了マーカー `render/_build_ok.txt` をポーリング（タイムアウト≥300秒）・末尾で `app.quit()`／**aerender 前に `.aep` mtime > `.jsx` を assert**（ブリーフ§5・.aep が古いと前ビルドを焼く事故）。

## 7.7 コンポジタ（`scripts/ae/composite_atwater_hero.py`・SKIP 4条件を1つも削らない）

`BASE = atwater_final_bgm.v001.mp4` / `OUT = atwater_final_bgm.v002_ae.mp4`（v001 不変）。SKIP: (1) `render/<id>.mp4` 不在 / (2) 解像度≠1920x1080 / (3) 実測尺 `< dur-0.3` / (4) `beat.end > base_dur`。ffmpeg: `overlay=0:0:eof_action=pass:enable='between(t,start,end)'` / `-c:v libx264 -preset slow -crf 16 -pix_fmt yuv420p -colorspace bt709 -c:a copy`。**出荷済みを絶対に上書きしない。film_offset を適用する。**

---

# 8. レイヤー構成 と ゾーン分離（★主役の裏に最低4層）

## 8.1 本編カットのレイヤー構成（下→上・主役 L4 の裏に L1/L2/L3/L3b = 4層）

| L | 名前 | EP47 の値 |
|---|---|---|
| **L0** | ルート背景 | `#0A0A0C`（INK） |
| **L1** | グラデ背景 | `radial-gradient(120% 120% at 50% 40%, #14100C 0%, #100C0A 45%, #0A0A0C 100%)`（テキサスの埃 near-black。ACT3 のみ大理石寄り `#34363B` にシフト・booking は `#22242A`） |
| **L2** | グリッド/ライン | 縦横 64px の反復線＋放射マスク＋ドリフト。`repeating-linear-gradient(0deg/90deg, #7A5CD018 0px 1px, transparent 1px 64px)`、`translateY 0→48px` / `Easing.inOut(Easing.sin)`（等速禁止） |
| **L3** | グロー | 単一 civil-violet の差し。`radial-gradient(closest-side, #7A5CD066 0%, #7A5CD018 45%, transparent 75%)`、`filter: blur(28px)`。位置は幕で移動（道→手錠→booking→天秤→大理石→夜明けの戸） |
| **L3b** | 大理石の光帯/ビネット | ACT3 は歴史/収斂の光帯（`linear-gradient(100deg, transparent, #7A5CD022, transparent)` を横に slow drift）、他幕は羽根ビネット。`translateX` を `Easing.inOut(Easing.sin)` で微動（静止フレームゼロ） |
| **L4** | 主役（still / i2v / factory） | §10 のモーション（Ken Burns/parallax/i2v） |
| **L5** | テロップゾーン（上/中央・figures） | §8.2 |
| **L6** | 字幕ゾーン（下部帯） | §8.2 |

> **主役（L4）の裏に L1/L2/L3/L3b = 4層**（グラデ背景・グリッド/ライン・グロー・光帯/ビネット）で CLAUDE.md「最低3レイヤー」＋タスク「最低4層」を満たす。**各層は §3.1b の通り常に微動（静止フレームゼロ）。**

## 8.2 ゾーン分離（一度も重ねない）

| ゾーン | 縦位置（1080基準） | スタイル |
|---|---|---|
| テロップ見出し | `y=96–260` | Oswald 64px / `#F5F7FA` / letterSpacing 4 |
| 中央テロップ / figures | `y=420–660` | §6 |
| 出典テロップ（アクセントライン） | `y=742–786` | Oswald 28px / civil-violet `#7A5CD0` 3px 下線 |
| 字幕帯 | `y=872–1010` | 白 `#FFFFFF` + `textShadow:0 0 6px #000,0 2px 4px #000` / 半透明黒帯 `rgba(6,6,8,0.62)` / ≤2行・1行≤42字 / 54px / lineHeight 1.28 |
| AI開示 | `y=1024–1052`（右下） | Oswald 20px / `#C8CDD6` / opacity 70% |

**Caption QC:** ナレ一致 ≥99%（faster-whisper 強制アライン）/ `.srt` カバー ≥95% / キュー 1.0–6.0秒 / CPS ≤17 / 単語割り禁止 / 1語孤立キュー禁止 / ズレ ≤120ms。**【SILENCE 1】区間と HOOK TEASER 無音区間には字幕キューを置かない。**

---

# 9. 絵コンテ（★48シーン・象徴のみ・6制約・Atwater/子ども/Turek 非人物化・CODEX_A が 85本プロンプトへ展開する原図）

## 9.1 パーサ契約（★CODEX_A が `ai_prompts.v001.md` を書くときの形式・`read_prompts()` が読む2行形式）

```
- `S01.png`
<positive prompt> ... [STYLE] Avoid: <negative>
```
- **1行目:** `` - `S01.png` ``（バッククォート囲み・行末は `.png` 直後）。プロンプトを同じ行に書かない。
- **2行目:** 正プロンプト → `[STYLE]`（§5.5）→ `Avoid:` → 負プロンプト（§5.6）。
- 配置先: **`episodes/PD-2026-047-atwater/04_scenes/ai_prompts.v001.md`**。生成: `.venv/Scripts/python.exe scripts/generate_sdxl_4k.py PD-2026-047-atwater`（**variants 指定なし＝1枚**）。
- 出力: `H:\pd-media\assets\ai\atwater\S01.png …` ＋ `remotion/public/atwater/`。長辺 ≥3840 で冪等スキップ。
- **★body 85本＝85行**（still 各1枚）＋ **i2v 種 16行**（M01_src..M16_src）＝ `ai_prompts.v001.md` は計 **101 エントリ**。CODEX_A は書いた直後 `--only S01` で `shots=` が **101** に達しているか（2行形式が壊れていないか）を確認。**プロンプト実体（85本）は CODEX_A が正典**（本節は絵コンテ級の原図）。

## 9.2 絵コンテ級ショット記述（Sid ごと・カメラ/モーション/象徴/制約。CODEX_A はこれを固有プロンプトに翻訳）

> **全ショット共通:** 顔・身体・肖像なし（R1/C5）。Gail Atwater/子ども/Officer Turek を個人として描かない（象徴・物・影のみ）。**子どもは空のチャイルドシートで象徴のみ**（人体・泣き顔を描かない・C5）。読める文字を作らない（redacted/illegible）。判例番号・日付・金額・票数・1997・子の年齢を描かない。テキサスの午後の埃＋冷灰の booking＋冷たい大理石＋唯一の差し色 civil-violet。**「逮捕は違法/覆された」に見える絵を作らない**（C1）。最高裁の列柱/9席＝5-4 UPHELD の場／救済は立法へ開く扉で描く（C2）。天秤は罰金のみ↔全逮捕の中立対比（C4）。

| Sid | カメラ/レンズ | 象徴（動き） | 制約メモ |
|---|---|---|---|
| S01 | 引き・道路 | テキサス片側二車線の午後の道・陽炎 | C5: 人物なし |
| S02 | 接写・車内 | 外れたシートベルトのバックル（i2v: 揺れる） | C1: 唯一の"違反" |
| S03 | 俯瞰・車内 | ダッシュ＋空のチャイルドシート2つ | **C5: 子は象徴のみ・扇情なし** |
| S04 | 正対・寄り | 開く手錠（i2v: swing open） | C5: 身体なし |
| S05 | 正対・静止 | booking フラッシュ／壁時計（SILENCE 1.8s） | 後で S48 と対 |
| S06 | 引き・外 | Lago Vista の湖畔の小さな町（factory） | — |
| S07 | 正対・push-in | 最高裁の淡い大理石列柱＝2001 の答え | C2: 最高裁の場 |
| S08 | 寄り＋奥行き | 手前に$50の切符・奥に遠い最高裁列柱 | 小さな切符→最高裁の距離 |
| S09 | 俯瞰・車内 | ピックアップ車内・空のチャイルドシート2つ・外れたベルト | C5: 罰金のみの違反 |
| S10 | 正対・路肩 | squad car のドアが閉まる（i2v: swing shut） | C5: 非扇情 |
| S11 | 逆光・窓辺 | officer の影/後ろ姿（指さす影・顔なし） | C5: 人物化しない |
| S12 | 接写 | フェンス杭/ハンドル上の手錠 | C5: 身体を描かず逮捕象徴 |
| S13 | 正対・入口 | 平凡なレンガの警察署の扉 | — |
| S14 | 俯瞰・机上 | booking 台の脱いだ靴・所持品トレー（判読不能） | C6: 象徴のみ |
| S15 | 正対 | 指紋台と booking カメラ（無人・冷灰） | C5: 非扇情 |
| S16 | 正対 | 無人の holding（institutional・鉄格子なし） | **C5: 独房/鉄格子を描かない** |
| S17 | 正対 | 治安判事のベンチと bond の紙（判読不能） | C6: about an hour は figures にせず |
| S18 | 接写・机上 | $50の切符／no contest 票（判読不能） | C6: stat F-STAT1・金額は figures |
| S19 | 接写・机上 | 開いた第4修正のページ（判読不能・"reasonable"核） | C6: 4A の判定語 |
| S20 | 接写 | §1983 の連邦法の古い本 | C6: 法番号は figures |
| S21 | 正対・天秤 | 左 citation form・右 手錠の天秤 | **C1/C4: 中立対比・compbars は figures** |
| S22 | 接写・硬光 | 大きな語 "REASONABLE" の抽象 | C6: 判読最小・4A 核 |
| S23 | 正対・天秤 | 天秤が傾く（i2v: tip・faultsplit） | C4: どちらへ傾くか（中立） |
| S24 | 引き・法廷 | 無人の法廷ベンチと手すり | — |
| S25 | 接写・机上 | filing stamp（提訴の押印） | C6: §1983 は figures |
| S26 | 引き・廊下 | 冷光の長い courthouse 廊下（factory） | — |
| S27 | 窓越し | 巡回車の窓越しの視点＝probable cause | C6: "undisputed" は figures |
| S28 | 俯瞰 | 対向する2本の矢印（判読不能ラベル） | two clean arguments |
| S29 | 接写 | citation 本 vs cell key | 切符で帰す/拘置する道 |
| S30 | 引き・道路 | あらゆる運転者が通る空の道 | 普遍性（ACT2 締め） |
| S31 | 正対・対称 | 最高裁の9席のベンチ（荘厳・最も遅い） | C2: 5-4 の場 |
| S32 | 正対 | 5-4 の投票が "five" で解決するバロット | **C1/C4: UPHELD 対語・votetally は figures** |
| S33 | 正対・列柱 | 夜の最高裁の列柱・大理石（factory） | C2: 最高裁の場 |
| S34 | 机上・接写 | 閉じた古い革表紙の判例集（Souter 歴史・判読不能） | C2: 歴史の根拠 |
| S35 | 接写 | 建国期のルールの古い巻（判読不能） | C2: 確たる禁止伝統なし |
| S36 | 大理石面 | 一本の清い線＝bright-line | C1: 明確な規則 |
| S37 | 壁ショット | 大理石を走る刻印風の光の帯（i2v: 光が走る） | C6: 路肩の一瞬/収斂 |
| S38 | 机上 | 暖ランプ下に開いた意見集の抽象行（判読不能） | **C2: Souter "pointless indignity" 逐語は figures F-QUOTE1・帰属 for the Court** |
| S39 | 正対・扉 | 立法府（州議会）へ開く扉 | C2: 救済は立法へ（mechanism gears） |
| S40 | 机上 | 反対意見側に開いた別の意見集 | C3: O'Connor 反対の書 |
| S41 | 正対・扉 | 立法へ開く扉 vs 固く閉じた憲法の扉（i2v: 扉） | **C3: O'Connor 逐語は figures F-QUOTE2・帰属 dissenting** |
| S42 | 俯瞰 | 4票が並ぶが5票に届かない象徴（判読不能） | C3/C4: four votes, not five |
| S43 | 接写・大理石 | 最高裁が引きなお消していない一本の線 | C1: the line drawn |
| S44 | 引き・道路 | テキサスの道に戻る＝あなたの車と午後 | 現在形・payoff 起点 |
| S45 | 接写・車内 | 外れたシートベルトのバックル再掲 | 最小の違反 |
| S46 | 接写 | 州法の条文本 | C1: 救済は州の statute |
| S47 | 地図・引き | 州境で protected/not に分かれる壁地図（判読不能） | C1: 州次第・rule なお立つ |
| S48 | 引き・pull-back | 夜明けに開く扉から採光が育つ（i2v: 戸が開き光が育つ） | C5: 人物なし・payoff |

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
対象（fast move）: **HOOK TEASER の手錠/フラッシュ**、**S04**（開く手錠）、**S10**（squad car ドア closingdoor）、**S16 booking 扉**、**S23**（天秤 tip=faultsplit）、**S25 filing stamp**、**S41**（扉）、および §6 の `votetally`/`stat` 桁変化・幕頭 `acttitle`・`kinetic:emphasis` の切れ上がり。**S01/S07/S31（荘厳 push-in）・S05/S48（時計/夜明け）・S37（光が走る・緩）・S02/S10 の緩い i2v・Ken Burns には Trail をかけない**（無駄な残像・扇情を避ける・C5）。

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

# 11. オープニング（OP）設計 — 完全仕様（`OpeningAtwater`・fps=60・CLAUDE.md §1–5 全項目）

## 11.1 秒数ベースのタイムライン（fps=60・「フレーム」は全て `Math.round(60 × 秒)`・直書き禁止・0.5s 刻み方針で全区間記述）

```ts
const FPS_OP = 60; const F = (s:number)=>Math.round(FPS_OP*s);   // 総 180f = F(3.0)
```

| 秒 | フレーム | 起きること（EP47 signature = テキサスの午後の道に外れたシートベルト＋violet の差し） |
|---|---|---|
| 0.00–0.10 | f0–6 | 画面 `#0A0A0C`。**L1** グラデ opacity 0→1（0.40s）＋ **scale 1.08→1.00** を 180f で（`Easing.out(Easing.cubic)`）。opacity 単独でなく scale 併用 |
| 0.10–0.15 | f6–9 | **L6 ロゴ**（`hasLogo`）左上 `top:64/left:72` に spring 出現。scale 0.4→1.0・opacity 0→1（併用・`damping:14,mass:0.9`） |
| 0.15–0.25 | f9–15 | **L2** グリッドが spring（`{damping:200,mass:1,durationInFrames:F(0.8)=48}`）で reveal。最終 opacity=`gridReveal*0.18`。全体を 180f で `translateY 0→48px`（`Easing.inOut(Easing.sin)`） |
| 0.25–0.30 | f15–18 | **L3** civil-violet のグローが spring（`{damping:18,mass:1.2}`）＝午後の道の差し。scale 0.6→1.15 / opacity 0→0.85（併用）。`filter:blur(28px)` |
| 0.30–0.86 | f18–52 | **L4 主役タイトル**が1文字ずつ切れ上がる（`overflow:hidden` マスク）。各文字 spring（`{damping:16,mass:1}`）で `translateY 110%→0`、opacity=`interpolate(sp,[0,0.25],[0,1])`。**スタッガー=`F(0.04)=2フレーム/文字**。全体を `Trail`（`layers=6,lagInFrames=1.2,trailOpacity=0.45`）で包む |
| 0.55–1.15 | f33–69 | **L2b violet の光ライン**（EP47固有＝紫の帯がタイトル背後を横切る）。中央から `scaleX 0→1`＋`opacity 0→0.55`（spring `{damping:22,mass:1.1}`, `transformOrigin:'center'`）。civil-violet。opacity 単独禁止で scaleX 併用 |
| 0.95–1.35 | f57–81 | **L5a** violet の下線が左から `scaleX 0→1`（spring `{damping:16,mass:0.8}`, `transformOrigin:'left center'`）。240×6px・`boxShadow:0 0 24px #7A5CD0aa` |
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
| L2b violet の光 | scaleX 0→1 / opacity 0→0.55 | spring | `{damping:22,mass:1.1}`・origin center |
| L5a 下線 | scaleX 0→1 | spring | `{damping:16,mass:0.8}`・origin left |
| L5b サブ | translateY 24px→0 / opacity | spring | `{damping:20,mass:1}` |
| L6 ロゴ | scale 0.4→1.0 / opacity | spring | `{damping:14,mass:0.9}` |

> **全 opacity が translateY/scale/scaleX と対。等速線形を1箇所も使わない。**

## 11.3 レイヤー構成（下→上・主役 L4 の裏に L1/L2/L2b/L3 = 4層）

L0 `#0A0A0C` / L1 グラデ（`radial-gradient(120% 120% at 50% 35%, #14100C 0%, #100C0A 45%, #0A0A0C 100%)`）/ L2 グリッド（`${accent}22` 64px・放射マスク）/ L2b violet の光（`linear-gradient(90deg, transparent, ${accent}cc, ${accent}55, ${accent}cc, transparent)`）/ L3 civil-violet グロー（`radial-gradient(closest-side, #7A5CD088, #7A5CD022, transparent)` `blur(28px)`）/ L4 主役タイトル（Trail 包み・`overflow:hidden` span マスク・Anton `fontWeight:800 fontSize:150 letterSpacing:-2 color:#F5F7FA`）/ L5 下線＋サブ（Oswald `fontSize:38 letterSpacing:6 uppercase color:#C8CDD6`）/ L6 ロゴ（`linear-gradient(135deg, ${accent}, #ffffff22)`・`border:2px solid ${accent}`）。

## 11.4 確認方法（CLAUDE.md §5）

```bash
cd C:\Users\aab15\Documents\prime-documentary\remotion
npm run studio     # = remotion studio。OpeningAtwater を 0→180f でスクラブし §11.1 の各時刻を目視
npx remotion render OpeningAtwater out/atwater_opening.mp4 --props=./props/atwater.json
# props 差し替え量産
npx remotion render OpeningAtwater out/atwater_short_op.mp4 --props=./props/atwater_short.json
# 本編
npx remotion render Ep47Atwater out/atwater_final.mp4 --props=./src/data/atwater_film.json --public-dir=public_slim --concurrency=4
```

---

# 12. props 定義と型（CLAUDE.md §4）

```ts
export type OpeningAtwaterProps = {
  title: string;      // 主役タイトル。1文字ずつスタッガーで切れ上がる
  subtitle: string;   // サブタイトル。UPPERCASE 表示（facts_lock 検査対象）
  accent: string;     // アクセント（HEX6桁・"#"込み）。グリッド/violet の光/グロー/下線/ロゴに波及
  hasLogo: boolean;   // true で左上にロゴバッジ
};
```
**EP47 の確定 props（`remotion/props/atwater.json`）:**
```json
{ "title": "THE FIFTY DOLLAR ARREST", "subtitle": "ATWATER V. LAGO VISTA, 2001", "accent": "#7A5CD0", "hasLogo": true }
```
**量産用 `remotion/props/atwater_short.json`:**
```json
{ "title": "ARRESTED OVER A SEATBELT", "subtitle": "THE COURT SAID POLICE COULD", "accent": "#7A5CD0", "hasLogo": false }
```
> `accent` は **`#7A5CD0` 固定**（EP41 gold / EP42 blue / EP43 amber / EP44 teal / EP45 crimson / EP46 green の流用は BLOCKER）。`subtitle`/`title` は `facts_lock` 検査対象（「illegal / struck down / the arrest was wrong」を出さない。`THE COURT SAID POLICE COULD` は制約1の枠と一致・C1）。**サムネ headlines に 1997・子の年齢を出さない**（R-HEDGE）。**5-4 をサムネに使うなら "UPHELD / THE ARREST STANDS" の語を同居**（R-DISPO）。

---

# 13. 受入基準（EP47 の Definition of Done・★語数ゲートが最初・全編アイボール必須）

```bash
cd C:\Users\aab15\Documents\prime-documentary
# 0. 語数（最優先・課金前）
./.venv/Scripts/python.exe scripts/check_script_length.py episodes/PD-2026-047-atwater/03_script/script.en.v001.md --json
# 1. 事実性（EP47固有・§1.3・6制約・dochighlight 0件・R-DISPO/R-QUOTE）
./.venv/Scripts/python.exe scripts/check_atwater_facts.py --json
# 2. ビート契約（AE↔figures 非重複・ledger・6制約・dochighlight 0件）
./.venv/Scripts/python.exe scripts/validate_atwater_beats.py
# 3. 密度（★30 を Remotion 側で満たしていること・--ep 指定／--json は出力パス）
./.venv/Scripts/python.exe scripts/check_motion_density.py --ep PD-2026-047-atwater --json runs/qc/atwater_motion.json
# 4. VO速度（ナレ直後・ミックス前）
./.venv/Scripts/python.exe scripts/measure_vo_wpm.py --ep atwater --json
# 5. 最終受入
./.venv/Scripts/python.exe scripts/check_final_acceptance.py 47 --render episodes/PD-2026-047-atwater/08_edit/atwater_final_bgm.v002_ae.mp4 --emit-receipt
```
> **ゲート入力は `--ep PD-2026-047-atwater`。`--json <film.json>` を入力に使わない**（出力パス＝上書き事故。ブリーフ§5）。

| ゲート | 閾値 | EP47 設計値 |
|---|---|---|
| `check_script_length` | band 内 | 2,135語（SPEC・要 PASS 確認・cap 2,141） |
| `runtime_band` | 690–750s | **739.8s = 12:19.8**（上限 750s に 10.2s 余裕） |
| `motion_density` | ≥2.5/min ∧ cov ≥0.25 ∧ variety ≥3 | **3.00/min / 0.270 / 9種**（film.json 36 beats・AE非依存・floor 30 に +6） |
| `animation_mix`（紙芝居） | still-share ≤45% ∧ motion cov ≥45% | **44.89% / 55.11%** |
| `check_asset_reuse` | first-use ≥0.70・still≤2・factory1・motion≤2 | **0.8578 / 2 / 1 / 2** |
| `footage_diversity` | distinct/total ≥0.40 | **0.8578** |
| `visual_asset_qc` | 全 factory 目視 reviewed | **92本 目視（CODEX_A）** |
| `image_resolution` | 長辺≥3840 | 全 SDXL ≥3840 |
| `bgm_present` | 無音>25秒ゼロ | 最長 1.8秒 |
| `caption_integrity` | 一致≥99%・カバー≥95% | §8.2 |
| `op_ed_bookends` | `BrandOpening`/`BrandEndcard` import・不変 | ✓ |
| `asset_manifest` | A↔B counts/role 一字一致・also_thumb 6（S01/S03/S18/S46/S68/S85）・overlay 12・schema `atwater_assets.v1` | §5.8 |
| `facts_lock`（EP47固有・6制約） | violations=0・**dochighlight 0**・R-DISPO（5-4=UPHELD）・R-QUOTE（Souter=for the Court／O'Connor=dissenting） | §1.2/§1.3 |
| **全編アイボール** | 12:19.8 を通しで目視 | ★1フレーム判定禁止（EP39-41/EP3941 の miss） |

---

# 14. premortem（失敗するとしたらここ）

| # | 失敗モード | 事前対処 |
|---|---|---|
| 1 | **逮捕を"違法/覆された"と誤記**（本作最大リスク） | §1.2 R-DISPO。5-4=UPHELD・"the Court said police COULD"。`illegal/unconstitutional/struck down/overturned` を逮捕主語に使わない。5-4 payload に "UPHELD/STANDS/constitutional" 対語必須 |
| 2 | **引用の帰属ミス**（O'Connor を Court に／Souter を dissent に） | §1.2 R-QUOTE。**Souter="Justice Souter, for the Court"／O'Connor="Justice O'Connor, dissenting"**。逐語のみ・要約を引用符に入れない |
| 3 | **子どもの扇情化 / Atwater 肖像** | §5.6/§9 R-FACE/R-CHILD。空のチャイルドシートで象徴のみ・年齢を画面に出さない・泣き顔/身体を描かない・顔なし |
| 4 | **medium 値の画面焼き**（1997・子の年齢） | §1.4 R-HEDGE。画面 hard 数値は $50/$25–$50/5-4/2001 のみ。1997 は発話のみ |
| 5 | **番号ズレ**（別番号を発明） | シーンは S01..S48 固定（§3.2）。still 資産 ID は S01..S85（別空間・cross-map 禁止） |
| 6 | **紙芝居**（still-share 45%超・余裕 0.11%pt） | §5.1 で still-cut 101 固定・factory 92・i2v 32。still1つ増で 45% 割れ → cut を増やさず同一シーンの新規 distinct で回復 |
| 7 | **バリエーション水増し**（`--variants 3`） | §5.3。variants 指定なし＝1枚。ai_prompts は 85行＝85枚 |
| 8 | **密度 FAIL**（AEカードに頼る） | §6。film.json に 36 beats（30 超）。AE 8枠は composite 後で非カウント |
| 9 | **画像プロンプトが読めない**（0枚生成） | §9.1 の2行形式・`--only S01` で `shots=101`（body 85 + i2v種 16）確認 |
| 10 | **ファイル名信仰**（牛が本編に入る） | §5.4 factory 92本を `build_footage_contact_sheet.py` で全点目視（CODEX_A BLOCKING） |
| 11 | **dochighlight のバグ見え**（3回指摘） | §6.2/§7.3。`dochighlight`/`comparebars` を1件も置かない（R-DOCHL・grep 0） |
| 12 | **FigureBeats kind 大文字で無音描画** | §6.2 kind は全小文字（`compbars`・`comparebars` は非実在） |
| 13 | **AE em-dash 豆腐 / 等速 / OM名英語 / 文字切れ** | §7.6。テキスト幅は `sourceRectAtTime(t,false).width` 実測 |
| 14 | **id 誤り / durationInFrames 手書き**（切り詰め・綴り違い等） | §0.1。`id="Ep47Atwater"`・`caseFilmDurationInFrames(atwaterFilm,30)`=22194（hookSeconds=8.0） |
| 15 | **accent 流用**（他話色を残す） | §0.5/§7.5/§12。OP props/AEカード/サムネ accent は `#7A5CD0` |
| 16 | **A↔B マニフェスト不整合**（role=thumb を作る/counts 不一致/schema 名違い/public_path 欠落） | §5.8。`atwater_assets.v1`・role enum=`body/i2v_source/reject`・also_thumb 6（S01/S03/S18/S46/S68/S85）・overlay 12・全エントリ public_path を A/B 一字一致 |
| 17 | **EP39〜46 と素材被り** | §2 で7つの stock_ledger の sha256 を除外（`select_atwater_factory.py --verify-no-prior-overlap`） |
| 18 | **fast端で 750s 超**（余裕 10.2s） | §4.1 speed 1.0 明示＋`measure_vo_wpm` 168–190・190超は破棄再発注。総尺 739.8s ≤750 の assert（§3.1[4]） |
| 19 | **public→public_slim 未 staging**（EP45事故） | ブリーフ§5。img/factory/motion/audio を public_slim へ全コピーしてからレンダ |

---

# 15. 設計パッケージ接続（DESIGN → CODEX_A / CODEX_B）

- **DESIGN（本書）:** タイムライン（0〜719.3s 全区間＋8.0s teaser・各Act・§3.1/§3.1b）・レイヤー（背面4層・§8）・モーション数値（§10）・48絵コンテ（§3.2/§9・象徴・6制約・子ども非扇情・Atwater 顔なし）・FigureBeats 設計（≥30＝36・小文字kind・変種≥3＝9種・dochighlight 0件・quote 逐語＆帰属厳格・§6）・AEカード表（8枚・accent #7A5CD0・§7.3）・OP 仕様（§11）・asset_manifest スキーマの正（§5.8）。
- **CODEX_A（別ファイル `EP47_atwater_CODEX_A_ASSETS.v001.md`）:** §9 を **85本の固有プロンプト**（1シーン1枚・variants 0・省略禁止で全85本）＋ i2v 16 ＋ factory 92 選定＆**全点目視QC**（`select_atwater_factory.py`・`--exclude-used --ep PD-2026-047-atwater` で EP39〜46 sha256 除外）＋境界契約 `asset_manifest.v001.json`（schema `atwater_assets.v1`・counts を EP47 値 still_body85/still_i2v_source16/motion16/factory92/overlay12・全エントリ public_path・`stills[].role` enum=`body/i2v_source/reject`・also_thumb 6（S01/S03/S18/S46/S68/S85））。
- **CODEX_B（別ファイル `EP47_atwater_CODEX_B_BUILD.v001.md`）:** `build_atwater_film.py`（＝EP46 `build_tlo_film.py` を複製・ASSET_MAP/NARR/FACTORY_SEL/SLUG/EP を atwater に・実素材のみ stub 禁止・manifest factory/motion 全読込）／captions（実測 narration）／figures 36（小文字 kind・dochighlight 0件・quote 逐語＆帰属・§6）／`CaseFilm` を `id="Ep47Atwater"` で Root.tsx 登録（`caseFilmDurationInFrames`＝22194・hookSeconds=8.0）／`OpeningAtwater`／AEビルダ・コンポジタ（accent #7A5CD0・実測幅・ledger 照合・.aep>.jsx assert・レイアウト名は実装済み8種のみ・§7.3 の8カード＝本書 §7.3 と一字一致）・`validate_atwater_beats.py`・`check_atwater_facts.py`（EP46 版を複製・同名）／`build_atwater_bgm_real.py`→`composite_atwater_hero.py`（film_offset 適用）／public_slim staging／レンダ（`--public-dir=public_slim --concurrency=4`）／全ゲート（`--ep PD-2026-047-atwater`）／完成後の全編アイボール。
- **A↔B 接続点は `asset_manifest.v001.json` ただ1ファイル**（schema `atwater_assets.v1`・counts/role enum を A/B 一字一致・§5.8）。
- **複製元（★`ls scripts/` で実在確認・実在しないスクリプトを捏造しない）→ atwater 複製先:** EP46 の tlo 系（`build_tlo_film.py`→`build_atwater_film.py` / `check_tlo_facts.py`→`check_atwater_facts.py`）を第一候補とし、tlo 系が未整備なら実在確認済の EP44/45 系（`build_tekoh_film.py`/`build_cleveland_film.py`・`check_tekoh_facts.py`・`select_cleveland_factory.py`・`validate_caniglia_beats.py`・`composite_caniglia_hero.py`・`build_caniglia_bgm_real.py`）を複製元にする。**共有（複製不要・実在確認済）:** `generate_sdxl_4k.py` / `build_footage_contact_sheet.py` / `check_motion_density.py` / `measure_vo_wpm.py` / `check_script_length.py` / `check_final_acceptance.py`。
