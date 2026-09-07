# EP43 — THE WELFARE CHECK — 制作設計書（DESIGN 本体・v001・確定台本版）

- Episode ID: `PD-2026-043-caniglia` / slug: `caniglia` / EP43
- 中心の問い（英語・二人称・★射程を過大化しない）: **"Can the police cross your threshold without a warrant, just to look after you — and carry out what they find?"**
- 判例（制度説明としてのみ）: **Caniglia v. Strom, 593 U.S. 194 (2021), No. 20-157**（9–0・Thomas 執筆・Roberts+Breyer / Kavanaugh / Alito が別途補足意見・**vacate & remand**）
- 主役: **Edward Caniglia**（存命の私人＝**R2**）。象徴のみ・尊厳の物語。**顔・肖像・身体を一切描かない。**
- リスク区分: **R2**（Caniglia 存命私人）。Cady v. Dombrowski の被告・関係者も人物化しない。全実在人物の顔・身体・肖像を描かない。
- Status: **BINDING**。**唯一の真実 = 機械生成済み `EP43_caniglia_PRODUCTION_SPEC.v001.json`**。本書のあらゆる数値はそこからの転記で、手書きで発明していない。衝突したら SPEC が勝つ。
- このファイルは**設計パッケージ3分割**（DESIGN / CODEX_A / CODEX_B）の **DESIGN 本体**。共有ブリーフ `EP43_caniglia_DESIGN_BRIEF.shared.md` を単一の真実源とする。85本の SDXL プロンプト実体・i2v 16・factory 93 選定は **CODEX_A**、build_caniglia_film.py・captions・figures 実装・Root.tsx 登録・AEビルダ/コンポジタ・ゲートは **CODEX_B** に属す（本書は各所でポインタのみ示す）。

## ★このエピソードの唯一の真実（手書きで数値を発明するな）

`episodes/_planning/EP43_caniglia_PRODUCTION_SPEC.v001.json`（台本から機械生成・`scripts/build_production_spec.py`）。本設計書は SPEC を**人間可読な実装指示に翻訳しただけ**で、新しい数字を作っていない。

```
words_total          = 2,141
narration_seconds    = 721.3   （= 12.0分）@ wpm_used 178.1
scenes               = 48      （S01..S48・確定。増やすな減らすな）
total_cuts           = 226
still  distinct 85 / cuts 101 / mean 1.19 / cap 2   ← ★各1枚生成（バリエーション0）
factory distinct 93 / cuts 93 / mean 1.0  / cap 1   ← 在庫選抜・全点目視QC
motion distinct 16 / cuts 32 / mean 2.0  / cap 2
distinct_total       = 194
first_use_share      = 0.8584  （floor 0.70）
still_share_of_cuts  = 0.4469  （cap 0.45）
motion coverage      = (93+32)/226 = 0.5531  （floor 0.45）
MG beats_floor       = 31      （film.json 側 figures+graphics。AEカードは check_motion_density に数えられない）
beats_per_min_floor  = 2.5   /  variety_floor = 3
mean_shot_seconds    = 3.19   /  max_shot_seconds = 6.0
```

## ★★ 最重要の前提: 1シーン1枚・バリエーション0 ★★（ブリーフ§1）

- Codex の画像生成は SDXL より高精度。**同一ショットの複数バリエーション（`_01/_02/_03`）を作らない。**
- `04_scenes/ai_prompts.v001.md` は **still 85本＝85行の固有プロンプト**（`generate_sdxl_4k.py` の `read_prompts()` 2行形式・各1枚）。**`--variants 3` は使わない**（`--variants 1` または variants 指定なし）。
- i2v モーション種は **16枚**（各1シード・これもバリエーション0）。
- 総生成画像 = **still 85 + motion seed 16 = 101枚（各1回）**。**factory 93 は生成ではなく在庫選抜**（全点目視QC・EP39/40/41/42 と sha256 被りゼロ）。
- **still を増やして factory を削るな**（still-share 0.4469 は cap 0.45 に対し余裕 0.31%pt しかない）。

## ★EP39/40/41/42 で踏んだ失敗＝本書が最初から潰す設計判断

| # | 失敗 | 本書での恒久対策 | 参照 |
|---|---|---|---|
| 1 | **番号ズレ**（別リストを発明） | シーンは **SPEC の S01..S48 に固定**。別番号体系を作らない | §3.2 |
| 2 | **紙芝居**（still 100% で animation_mix FAIL） | still-cut **101 固定**＋factory実写 **93**＋i2v **32**。still-share 44.69% ≤45% / motion cov 55.31% ≥45% を構造保証 | §5.1 |
| 3 | **バリエーション水増し**（36×3=108 で反復回避を偽装） | **1シーン1枚・85本を各1枚**。variants 禁止 | §5・§9 |
| 4 | **画像プロンプトのパーサ非互換** | `read_prompts()` の**2行形式**（`` - `S01.png` `` の次行に `... Avoid: ...`）。CODEX_A が `--only S01` で拾い数（101）を確認 | §9 |
| 5 | **ファイル名を信じた**（牛が documents、大聖堂が監視カメラ） | factory 93本を `build_footage_contact_sheet.py` で**全点目視QC**（CODEX_A 必須・BLOCKING） | §5.4 |
| 6 | **AEカードを密度に数えた** | `check_motion_density` は film.json の `figures+graphics` だけ。**film.json 側に MGビート 31本以上**（本書は 37 設計）。AE は composite 後で 0 カウント | §6.1 / §7 |
| 7 | **一枚絵で完成判定**（EP39-41 の眼球不足） | 全編アイボール必須（§13）。measured > estimated | §13 |
| 8 | **A↔B マニフェスト不整合**（EP42 で3チェックが検出） | asset_manifest は **A↔B で同一スキーマ・counts/role enum を一字一致**。role=`thumb`/`still_thumb` を作らない。サムネは `also_thumb=true` の body still 6枚 | §5.8 |

---

# 0. 環境・Remotion設定（CLAUDE.md §0 準拠）

## 0.1 本編 `Ep43Caniglia` の Composition 設定（★本編の正・誤記注意）

| 項目 | 値 |
|---|---|
| `id` | **`Ep43Caniglia`**（Root.tsx に `CaseFilm` で登録。ブリーフ§5「Ep43Caniglia登録」。**id の切り詰め・綴り違い・大文字化は誤記＝BLOCKER**） |
| 解像度 | **1920 × 1080** |
| `fps` | **30**（EP42 young と同値を踏襲。フレームは全て `Math.round(30 × 秒)`・直書き禁止） |
| `durationInFrames` | **`caseFilmDurationInFrames(canigliaFilm, 30)` = 22014**（4項の実関数 `round(hookSeconds×30)+round(OPENING_SEC×30)+ceil(narrationSeconds×30)+round(ENDCARD_SEC×30)`・**hookSeconds=0**・§3.1[3] で算出。手書きで数値を入れず関数で算出する） |
| component | `remotion/src/compositions/CaseFilm.tsx`（既存の汎用 `CaseFilm` を再利用。`Bookends.tsx` の `BrandOpening`/`BrandEndcard` を **import**・fork 禁止） |
| data | `remotion/src/data/caniglia_film.json`（`scripts/build_caniglia_film.py` で再生成できる状態を保つ＝**git 未追跡**） |

**Root.tsx 登録（★ブリーフ§5・CODEX_B が実装）:**
```tsx
import {canigliaFilm} from './data/caniglia_film.json';
import {caseFilmDurationInFrames} from './lib/caseFilmDuration';
// ...
<Composition
  id="Ep43Caniglia"
  component={CaseFilm}
  width={1920} height={1080} fps={30}
  durationInFrames={caseFilmDurationInFrames(canigliaFilm, 30)}  // = 22014
  defaultProps={{film: canigliaFilm}}
/>
```
> **id は `Ep43Caniglia`**（切り詰め・綴り違い・先頭大文字化などは全て誤記。ブリーフ§5 の render 行 `Ep43Caniglia` が正）。

## 0.2 タイトルバンパー `OpeningCaniglia` の Composition 設定（CLAUDE.md 正典部品準拠）

| 項目 | 値 |
|---|---|
| `id` | **`OpeningCaniglia`** |
| 解像度 | **1920 × 1080** |
| `fps` | **60**（CLAUDE.md §0 の正典値。OP 単体は 60fps） |
| `durationInFrames` | **180**（= 3.0秒 @ 60fps） |
| component | `remotion/src/compositions/OpeningCaniglia.tsx`（§11 全仕様） |

> `OpeningCaniglia` は**独立したタイトルバンパー成果物**（`out/caniglia_opening.mp4`）。本編内 OP/ED の正典は `Bookends.tsx`（`BrandOpening` 3.50s / `BrandEndcard` 9.00s・不変）。`OpeningCaniglia` を本編に ffmpeg で焼き込まない（オーナー承認なしに見え方を変えない）。

## 0.3 必要な依存パッケージ

```bash
cd C:\Users\aab15\Documents\prime-documentary\remotion
npm i @remotion/motion-blur     # CLAUDE.md 必須依存（Trail によるモーションブラー）
```

## 0.4 `remotion.config.ts`（CLAUDE.md §0 正典値・EP41/42 と同一）

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
> レンダーログで `crf 16 / preset slow / yuv420p / bt709 / aac 320k / libx264` を必ず確認。本編レンダは `--public-dir=public_slim --concurrency=4`（ブリーフ§5）。

## 0.5 ブランド（`remotion/src/brand.ts` から import・ハードコード禁止）

`brand.ts` 実値: ink `#0A0A0C` / navy `#0B1A2B` / electric `#1F6BFF` / silver `#C8CDD6` / gold (brand.ts 既定・EP43 未使用) / white `#F5F7FA`。フォント: display Oswald / number Anton / body Oswald。

**EP43 のパレット（★ダーク/シネマ・夜の Cranston の家＋法廷大理石・レーン分離・単一の暖色＝玄関灯）:**
```
INK    = #0A0A0C   ルート背景
NIGHT  = #14110E   Cranston の夜（暖い near-black・家の内側）
MARBLE = #3A3B40   最高裁の冷たい大理石（ACT3）
STEEL  = #26282C   ウォッシュ/ビネット寄り（institutional）
ACCENT = #E0913C   ★porch-amber（誰かのために点けた玄関灯の暖色＝"助けに来た"の皮肉）。ブランド数値・ライン・下線・グロー・OP/AE/サムネ accent。★EP41 gold / EP42 warrant-blue を流用しない
WHITE  = #F5F7FA
SILVER = #C8CDD6
BEACON = #C7503E   ★予備：救急車の赤色灯（S17）のグローのみ。数値・下線には使わない
```
> **レーン分離:** EP39（electric・取調室）/EP40（gold amber・郊外昼光）/EP41（gold・鋼灰institutional）/EP42（warrant-blue・夜のシカゴ）と被らないよう、EP43 は **暖い夜の near-black `#14110E` ＋ 冷たい大理石 `#3A3B40` を基調＋唯一の暖色 porch-amber `#E0913C`**。接尾に `electric blue interrogation` `midday suburban` `steel grey death row` `warrant-blue` を含めない。**factory は EP39/40/41/42 の `stock_ledger*.json` の sha256 を除外**（CODEX_A・BLOCKING）。**CODEX_B は OP props / AEカード / サムネ accent を必ず `#E0913C` にする（EP42 warrant-blue の流用は BLOCKER）。**

---

# 1. 事実の取り扱い（★正確性6制約＝FACTS LOCK / `check_caniglia_facts.py`・BLOCKING）

## 1.1 確定台本（唯一の正・1バイトも変えない）

```
C:\Users\aab15\Documents\prime-documentary\episodes\_planning\EP43_caniglia_script.en.v001.md
```
**本番配置先:** `episodes/PD-2026-043-caniglia/03_script/script.en.v001.md`（上記を1バイトも変えずコピー）。整形も禁止（AI臭再発と語数ゲート再計算を招く）。台本の幕構成（HOOK / OP / ACT1–3 / ENDING）と `【DESIGNED SILENCE …】`（**3箇所**）を正典とする。存在しない演出マーカー（`【OST:】`/`〔CARD:〕`）を発明しない。

## 1.2 ★正確性6制約（全出力＝プロンプト・カード文言・図表・字幕・タイトルに適用。1つでも違反＝BLOCKER）

| # | 制約 | 出力での順守 |
|---|---|---|
| **C1** | **射程を過大化しない** | 判決が否定したのは「community caretaking の“住居”拡張」だけ。exigent circumstances / emergency aid の例外は温存。**タイトル/サムネ/カード/字幕/プロンプトに「警察は令状なしに家に入れない」と断定する文言を出さない**。温存例外（warrant / consent / emergency）を必ず併記できる形にする |
| **C2** | **9–0 ＝ vacate & remand** | 9–0 は「破棄・差戻し」。**Caniglia の全面勝訴/事件終結と断定しない**。カードで "9-0" を出すなら "ONE EXCUSE, CLOSED" 等、限定を同一カードに併記（限定「最終勝訴でない」は別カード r01 の "SENT BACK DOWN - NOT ENDED IN HIS FAVOR" が担う）。**§1.3 L-C2 の統一禁止語リストを出さない** |
| **C3** | **Cady ＝ 警察管理下の自動車** | Cady v. Dombrowski の対象は「警察管理下の自動車」。**住居と混同しない**。Cady カード/プロンプトは車・レッカー・トランクの象徴のみで、家と**別レイヤーに分離**。`Cady` の近傍に `home`/`house` を「同じもの」として置かない |
| **C4** | **Edward Caniglia ＝ R2・象徴のみ** | 存命私人。**顔・肖像・身体を描かない**。象徴のみ（食卓の拳銃・空のポーチ・救急車の赤色灯・玄関・電話・証拠タグ・布の上の2丁）。人物は影/後ろ姿/象徴に限定 |
| **C5** | **メンタルヘルス非扇情** | 手段の描写や内面の憶測をしない。「もう撃ってくれ」は記録事実として**1回のみ**・非演出。仮想の緊急例（銃声・窓辺の shape）は匿名・非グラフィック。**概要欄に 988 Suicide & Crisis Lifeline を記載**（画面の扇情カードにしない） |
| **C6** | **Payton／温存例外を正確に** | 住居＝第4修正の中心・令状なし立ち入りは **presumptively unreasonable**。逐語引用「very core … retreat into his own home」は **Florida v. Jardines** 帰属（Payton には帰属させない）。**「家は絶対に守られる」と誇張しない**（台本の "Not a wall around your home" の否定形は可） |
| **R1** | **実在人物の顔・肖像を生成しない** | 全生成ビジュアル表示中は `AI-assisted visualization`（右下）常時表示。概要欄に1行 AI 開示 |

## 1.3 6制約ゲート `check_caniglia_facts.py`（`scripts/check_caniglia_facts.py`＝EP42 `check_young_facts.py` を caniglia 用に複製。exit≠0 で出荷停止・CODEX_B 実装。出力 `facts_lock.v001.json`）

> **★ゲート名は1本に確定:** 6制約の機械ゲートは **`scripts/check_caniglia_facts.py`**（出力 `09_package/facts_lock.v001.json`）ただ1つ。DESIGN/CODEX_A/CODEX_B で**同名参照**（`*_accuracy`・`*_facts_check` 等の別名を作らない）。下表の **L-C1..L-C6・L-R1** は `check_caniglia_facts.py` の内部ルール **R-*** に一本化して実装する（対応: L-C1→R-SCOPE / L-C2→R-DISPO / L-C3→R-CADY / L-C4→R-FACE / L-C5→R-SENSITIVE / L-C6→R-PAYTON / L-R1→R-FACE）。

**検査対象:** `03_script/script.en.v001.md` / `remotion/src/data/caniglia_film.json` の `figures[].text`・`figures[].lines[]` / `08_edit/ae_hero/beats.json` の `top`/`bottom`/`main`/`quote`/`attribution`/`left`/`right`/`kicker`/`title` / `09_package/description.txt` / `remotion/props/caniglia*.json` の `subtitle`/`title` / `04_scenes/ai_prompts.v001.md`。

| ルール | 内容 |
|---|---|
| **L-C1 射程（R-SCOPE）** | 文字列 `police cannot enter your home` / `never enter your home without a warrant` / `no warrantless entry into homes` 等の**無留保の断定**が出たら FAIL。`9-0`/`unanimous`/`holding` を含む beat/figure/card に、温存例外（`warrant`/`consent`/`emergency`/`exigent`）または限定語（`one excuse`/`caretaking only`）が同一カードに無ければ FAIL |
| **L-C2 disposition（R-DISPO）** | **統一禁止語リスト（★CODEX_B §2.1 R-FORBID と一字一致）:** `full victory` / `total victory` / `complete victory` / `total win` / `won his case` / `won outright` / `case closed` / `case is over` / `case ended in his favor` / `final win` / `warrantless entry is illegal` / `home is absolutely protected` / `police can no longer enter` / `no more welfare checks` のいずれかが出たら FAIL。`9-0`/`9 to 0`/`nine to nothing`/`unanimous` を含むカードに `vacate`/`remand`/`not a final`/`one excuse`/`sent back` が無ければ FAIL。**（否定文脈の近似語＝台本 "did not hand … a final victory" 等を禁止語に足さない＝false FAIL 防止）** |
| **L-C3 Cady（R-CADY）** | `Cady`/`Dombrowski` の近傍60字に `car`/`vehicle`/`tow`/`trunk`/`custody` が無ければ FAIL。同近傍に `home`/`house` が「同一物」として出たら FAIL。`ai_prompts` の Cady シーン（S30/S31）に `home`/`door`/`porch` が正プロンプトに出たら FAIL |
| **L-C4 肖像（R-FACE）** | `ai_prompts.v001.md` の正プロンプトに `portrait`/`face of`/`likeness`/`recognizable`/`Edward Caniglia`（人物として）/`nude`/`his body` が出たら FAIL（ネガティブでの使用は可）。`Caniglia` の直後60字に `face`/`portrait`/`depicted as a man` が出たら FAIL |
| **L-C5 センシティビティ（R-SENSITIVE）** | `shoot`/`suicide`/`kill himself` 系の直近に手段描写・内面憶測語（`method`/`how he would`/`imagining`）が出たら FAIL。`shoot` の出現回数が台本で2回以上・演出誇張語同伴なら FAIL。**`description.txt` に `988` が無ければ FAIL**。**`08_edit/ae_hero/beats.json`（AEデッキ）または `caniglia_film.json` の `figures[]` に `988` が出現したら FAIL**（988 は description.txt / pinned_comment / BrandEndcard のみ・扇情文脈に限らず一律） |
| **L-C6 Payton/引用（R-PAYTON）** | 逐語引用 `retreat into his own home` の帰属が `Payton` になっていたら FAIL（`Jardines` 帰属が正）。`presumptively unreasonable` は `Payton` 帰属で可。`home is absolutely protected`/`a wall around your home`（否定文脈以外）が出たら FAIL |

**出力:** `09_package/facts_lock.v001.json`（`{"pass":bool,"violations":[{"file","rule","line","excerpt"}],"skipped":[...]}`）。`pass:true` でない限り `check_final_acceptance.py` に進まない。

## 1.4 画面に出してよい確定数値（★台本／事実対応表 C01–C25 に存在するものだけ。この表以外を画面に出すな）

| ID | 値 | 台本での表現（claim） | 使用先 |
|---|---|---|---|
| N01 | **AUGUST 2015 · CRANSTON, RI** | "It is August 2015, in a house in Cranston"（C15/C16） | AE **d01**（DATE_STAMP）/ figures timeline・pindropmap |
| N02 | **TWO HANDGUNS** | "the officers go inside his home and take two handguns"（C18） | AE **n01**（CENTER_STACK）/ figures stat・dochighlight |
| N03 | **NO WARRANT** | "No warrant."（C18） | AE **n01** bottom / figures dochighlight |
| N04 | **953 F.3d 112 (2020)** | 台本カード「First Circuit, 953 F.3d 112 (2020)」（C20） | figures **lowerthird**（AEカードにはしない） |
| N05 | **CADY v. DOMBROWSKI, 413 U.S. 433 (1973)** | 台本カード（C13） | figures lowerthird / AE **c01**（SPLIT_COMPARE の左＝車の文脈） |
| N06 | **NEARLY 50 YEARS** | "Nearly fifty years later"（Cady 1973 → 2021・C13） | figures stat・timeline |
| N07 | **MARCH 24, 2021（argued）** | "Argued March 24, 2021"（C03） | figures timeline |
| N08 | **MAY 17, 2021（decided）** | "Decided May 17, 2021"（C02） | figures timeline |
| N09 | **SEVEN WEEKS** | "Seven weeks later"（argued→decided・C02/C03 差） | figures **numberticker** |
| N10 | **9–0** | "Nine to nothing."（C04） | AE **v01**（VOTE_SPLIT・"ONE EXCUSE, CLOSED" 枠）/ figures **votetally** |
| N11 | **593 U.S. 194 (2021), No. 20-157** | 台本カード（C01） | `09_package/description.txt` ＋ figures lowerthird（本文で読み上げない） |
| N12 | **5 CIRCUITS vs 2** | "Fifth, Sixth, Eighth, and Ninth … along with the First … The Third and Seventh had refused"（C25） | figures **compbars**（5拡張 vs 2拒否） |
| N13 | **THREE OPINIONS** | "Three justices wrote separately"（Roberts+Breyer / Kavanaugh / Alito・C09/C10/C11） | figures stat・numberticker |
| N14 | **VACATE & REMAND** | "vacated the decision … and sent the case back down"（C04/C22） | AE **r01**（CENTER_STACK）/ figures dochighlight |
| N15 | **WARRANT · CONSENT · EMERGENCY** | "a valid warrant; your consent; and exigent circumstances"（C08） | AE **s01**（CENTER_STACK）/ figures compbars |
| N16 | **"what is reasonable for vehicles is different from what is reasonable for homes"** | Thomas 逐語（C12） | AE **q01**（QUOTE_CARD・Thomas 帰属）/ figures quote |
| N17 | **988** | センシティビティ配慮（C24） | `09_package/description.txt` ＋ BrandEndcard のみ（**画面の扇情カードにしない**・C5） |

> **★AE カード文言に「令状なしで家に入れない」「全面勝訴」を書かない。** 数値・引用は AE ledger（§6.4 の `beats.json`）と figures（§7）で一致必須。**593 U.S. 194 / 413 U.S. 433 / 953 F.3d 112 / 569 U.S. 1（Jardines）/ No. 20-157 は AE カードにせず figures lowerthird ＋ description に退避**（本文で読み上げない・台本の音声からは抜いてある）。

---

# 2. 視覚・音響レーン分離（EP39/40/41/42 との素材被り回避）

> **EP39/40/41/42 のファイルには一切触れない（読み取りのみ可）。** レーンを機械的に分離する。

| 軸 | EP42 young | **EP43 caniglia** |
|---|---|---|
| 舞台 | 夜のシカゴ西部の室内→法廷大理石→市議会 | **夜の Cranston の家（食卓・玄関）→ 朝のポーチ・救急車・押収 → 最高裁の大理石・空の9席 → 夜明けの開いた戸** |
| 時間帯 | 夜→テレビの光→大理石冷光→夜明け | **夜（食卓の銃・閉じた戸）→ 朝の日光（ポーチ・救急車）→ 大理石の冷光（判例核）→ 夜明けの暖色（開いた戸）** |
| 支配的出来事 | 誤住所への踏み込み・映像秘匿・否決 | **安否確認→無令状の立ち入り・拳銃押収・判例核（Cady=車／9-0／温存例外）・vacate&remand** |
| アクセント色 | warrant-blue（EP42） | **porch-amber `#E0913C`（玄関灯の暖色・唯一の実用光）** |
| ベース色 | 夜の青灰 `#131A24` + 大理石 `#3A4048` | **暖い near-black `#14110E` + 冷たい大理石 `#3A3B40` + near-black `#0A0A0C`** |
| レンズ感 | ACT1 断片／ACT3 正対荘厳／ENDING 引き | **HOOK 象徴モンタージュ／ACT1 最短・現在形・抑制／ACT2 正対の転回／ACT3 正対対称・荘厳／ENDING 引き（pull-back）** |
| 画像保存先 | `H:\pd-media\assets\ai\young\` | **`H:\pd-media\assets\ai\caniglia\`** |
| Remotion データ | `young_film.json` | **`caniglia_film.json`** |
| Remotion コンポ | `Ep42Young` | **`Ep43Caniglia`** |
| AE 作業ディレクトリ | `…/PD-2026-042-young/08_edit/ae_hero/` | **`…/PD-2026-043-caniglia/08_edit/ae_hero/`** |

**素材被り禁止:** EP39/40/41/42 と同一の factory clip / AI画像を1点も使わない。選定前に `episodes/PD-2026-039-*/` `…-040-*/` `…-041-*/` `…-042-*/` の `05_stock/stock_ledger*.json` を読み sha256 重複を除外（CODEX_A・BLOCKING）。

---

# 3. 尺と構成 — SPEC の値をそのまま使う

## 3.1 全区間タイムライン（★この表が唯一の正・秒は fps=30 から算出しフレーム直書き禁止・0〜721.3s 全区間）

**算出基準:** SPEC の `narration_seconds = 721.3`（マスター）を `caniglia_film.json` の `narrationSeconds` に入れる。**手計算で上書きしない。** SPEC は BODY を1ブロック（1,530語 / 515.4s）でのみ与える。ACT1/ACT2/ACT3 の内訳は**確定台本の語数シェアから導出**（下表・BODY 合計は SPEC 値に一致）。フレーム = `Math.round(30 × 秒)`。

| # | ブロック | 役割 | 語数 | 幕秒 | 台本指定の沈黙 | 固定尺 | 開始f | 終了f |
|---|---|---|---|---|---|---|---|---|
| 1 | **HOOK** | `hook` | 69 | 23.2（SPEC） | **1.8**（"still alive" 系末・閉じた戸で保持） | — | 0 | 696 |
| 2 | **BrandOpening** | `opening` | 0 | — | — | **3.50** | 696 | 801 |
| 3 | **OP ナレ** | `opening` | 88 | 29.6（SPEC） | — | — | 801 | 1689 |
| 4 | **ACT1** The night | `body` | 148 | 49.9（導出） | **1.4**（"checks into a hotel." 後・キーカードで保持） | — | 1689 | 3185 |
| 5 | **ACT2** The welfare check | `body` | 382 | 128.7（導出） | — | — | 3185 | 7045 |
| 6 | **ACT3** Where caretaking stops | `body` | 1000 | 336.9（導出） | — | — | 7045 | 17151 |
| 7 | **ENDING**（payoff→CTA） | `ending` | 415 | 139.8（SPEC） | **2.2**（"daylight behind it." ＝開いた戸・payoff の最長沈黙） | — | 17151 | 21345 |
| 8 | **BrandEndcard** | `ending` | 0 | — | — | **9.00** | 21345 | 22014 |

> **BODY 内訳の導出（★語数シェア・SPEC BODY 1,530語 / 515.4s を厳守）:** ACT1 148語→49.9s / ACT2 382語→128.7s / ACT3 1000語→336.9s（合計 1,530語 / 515.5s ≒ SPEC 515.4s・丸め）。ACT3 が最長（doctrinal core・最も遅い）。**この内訳は planning アンカー。final は `measure_vo_wpm` 実測が権威**（CODEX_B は実測秒で `caniglia_film.json` の各 segment 秒を更新）。
> **フレーム列**は BrandOpening(105f)/BrandEndcard(270f) を実尺で挟み、幕秒を順に `round(30×秒)` で積んだ実装用アンカー。**BrandEndcard 終端 22014 は §3.1[3] の `caseFilmDurationInFrames` 出力に一致**（幕秒積算の nominal 21615 との差 399f=13.3s は narrationSeconds マスター 721.3 と発話幕秒合計 708.0 の差＝息継ぎ＋設計無音3点を内包する測定マスター）。CODEX_B は `caniglia_film.json` の segment 順から再計算し一致を確認。

### 検算（CODEX_B は必ず自分で再計算して一致を確認）

```
[1] narrationSeconds = 721.3（SPEC マスター。手計算で上書きしない）
    ※ 発話ブロック HOOK..ENDING の幕秒合計 = 23.2+29.6+515.4+139.8 = 708.0s。
      SPEC マスター 721.3 との差 13.3s は、幕間の息継ぎ＋設計無音3点（1.8+1.4+2.2=5.4s）を内包した測定マスター。
      film.json には 721.3 を入れる。
    ※ mean_shot 検算: 721.3 / 226 = 3.19s ＝ SPEC mean_shot_seconds 一致（226カットは 721.3s 全域に張る）。

[2] 総尺 = hookSeconds 0 + BrandOpening(OPENING_SEC) 3.50 + narrationSeconds 721.3 + BrandEndcard(ENDCARD_SEC) 9.00
        = 733.8 秒 = 12:13.8
    ※ hookSeconds=0（HOOK ナレは narrationSeconds 721.3 に内包・別建ての hook teaser preroll は作らない）。
       台本 OPENING は「Gold BrandOpening after the hook, not at frame zero」＝HOOK ナレ→BrandOpening→OP ナレ の順。

[3] caseFilmDurationInFrames(canigliaFilm, 30) = 4項の実関数で算出（round(30×733.8) という単項近似ではない）:
      = round(hookSeconds×30) + round(OPENING_SEC×30) + ceil(narrationSeconds×30) + round(ENDCARD_SEC×30)
      = round(0×30)=0 + round(3.5×30)=105 + ceil(721.3×30)=ceil(21639.0)=21639 + round(9.0×30)=270
      = 22,014 フレーム
    ※ CODEX_B は caniglia_film.json の hookSeconds/narrationSeconds（＋Bookends の OPENING_SEC/ENDCARD_SEC）から
      同関数で再計算し 22014 に一致することを assert する（§5.1・§3.1 検算）。

[4] runtime_band ≤ 750s の assert（BLOCKING）:
    総尺 = hookSeconds 0 + 733.8 = 733.8s
    → 733.8s = 12:13.8 は band 690–750（11.5–12.5分）の内側（上限 750s に対し 16.2s の余裕）    ✓ PASS
    ※ hookSeconds を 0 超（teaser 採用）にする場合は round(hookSeconds×30) を [3] に加え、
      総尺 = 733.8 + hookSeconds を再検算して **≤ 750s** を再確認すること（BLOCKING）。
```
> **VO 実測で確定:** `measure_vo_wpm`（合格帯 168–190 wpm）でナレ実測。実測が SPEC マスターと乖離したら CODEX_B は `narrationSeconds` を実測値で更新（planning は 721.3・final は実測が権威）。190超は破棄・speed 0.95 で再発注（BLOCKING）。

## 3.2 シーン→幕の割当（★SPEC の S01..S48 を固定・別番号を発明しない・48シーン）

各シーンは narrative beat。226カットを 48シーンに分散（平均 4.71カット/シーン）。`primary` は各シーンの主素材（still=SDXL 各1枚 / factory=実写 / motion=i2v）。ambient/繋ぎは factory を各シーンに撒く（§5.1）。**象徴のみ・6制約順守・Caniglia/Cady 非人物化。絵コンテ級の記述は §9。**

> **★2つの `Sxx` 名前空間は別物（取り違え禁止）:** 本節の **narrative シーンは `S01..S48`**（この表の絵コンテ）。一方 **still 資産 ID は `S01..S85`**（CODEX_A §2 注記・1プロンプト=1枚で48シーンに85枚を配分）。同じ `Sxx` 表記でも DESIGN §3.2/§9 の Sid（narrative）と CODEX_A/asset_manifest の scene_id・covers_scene_id（still 資産 ID）は指すものが異なる。横断参照時は「どちらの空間か」を明示し、cross-map しない。

| Sid | 幕 | 内容（象徴・6制約） | primary |
|---|---|---|---|
| S01 | HOOK | 食卓に平置きされた1丁の拳銃・暖い低照度・手も顔もなし（象徴＝あの夜の核） | still |
| S02 | HOOK | 閉じた玄関ドアの脇に置かれた荷造り済みバッグ・サイド窓から porch-amber の光 | still |
| S03 | HOOK | ナイトスタンドの上で画面が灯る電話（i2v: 不在着信のパルス）＝安否確認の予兆 | **motion** |
| S04 | HOOK | 内側から見た閉じた玄関ドア・静止・暗い（DESIGNED SILENCE 1.8s の画・hard cut で BrandOpening へ） | still |
| S05 | OP | 夜の Cranston の質素な家の外観・1つだけ点る玄関灯（establishing） | factory |
| S06 | OP | 正対の敷居／玄関＝「あなたの問い」・手のひら幅だけ開いた戸・背後にグリッド線 | still |
| S07 | ACT1 | 薄暗い居間・2脚の椅子・冷めない口論の残り（クッションの乱れ・人物なし） | still |
| S08 | ACT1 | 食卓に拳銃が置かれる（i2v: ゆっくり置く・あの夜の定義的行為・手元のみ・顔なし） | **motion** |
| S09 | ACT1 | 裁判記録のページ・最も平坦な言葉・黒塗りの1行だけ淡く光る（"shoot me" の記録事実・非演出・1回） | still |
| S10 | ACT1 | 椅子から取られた上着・持ち上がる一泊バッグ（妻が出る象徴・顔なし） | still |
| S11 | ACT1 | 外から見た玄関ドアが静かに閉じる・玄関灯は点いたまま | still |
| S12 | ACT1 | 見知らぬナイトスタンドのホテルのキーカード（DESIGNED SILENCE 1.4s の画） | still |
| S13 | ACT1 | 翌朝・まだ閉じた玄関ドアの下から差す朝の光＝「everything is about that door」 | still |
| S14 | ACT2 | 非緊急回線（911でない）をダイヤルする電話（i2v: ダイヤル/画面）＝welfare check 要請 | **motion** |
| S15 | ACT2 | 日中の空のポーチ・2つの長い影（警官＋本人＝影のみ・穏やか・顔なし） | still |
| S16 | ACT2 | ポーチの椅子・網戸が開き・マグ＝「alive, on the porch, talking, calm」（人物なし） | still |
| S17 | ACT2 | 私道の救急車・赤色灯が回る（i2v: BEACON の回転掃引）＝精神鑑定へ搬送 | **motion** |
| S18 | ACT2 | 開いたまま立つ玄関ドア・揺れるカーテン＝本人が去った後に家へ入る（無令状の立ち入り） | still |
| S19 | ACT2 | 布の上に並べた拳銃2丁＋証拠タグ＝押収（no warrant・身体なし） | still |
| S20 | ACT2 | 令状の置かれるべき机上が空＝「No warrant」（不在・判読不能な空白） | still |
| S21 | ACT2 | 財産返還を求める裁判書式（自分の銃を取り戻すために提訴）＝判読不能 | still |
| S22 | ACT2 | 証拠袋に入った2丁とタグ（判読不能）＝「the smaller fight」 | still |
| S23 | ACT2 | 再び正対の敷居＝「the real one was about the door itself, who gets to open it」 | still |
| S24 | ACT2 | 静かな住宅街・慎重な家並み＝「for years, this was simply legal」（establishing） | factory |
| S25 | ACT2 | 日中も点いたままの玄関灯＝「concern」の皮肉（唯一の暖色 porch-amber） | still |
| S26 | ACT3 | 大理石に刻まれた第4修正の一節「persons, houses, papers, and effects」（判読困難・象徴） | still |
| S27 | ACT3 | 地裁の冷たい扉＝下級審で敗訴（establishing） | factory |
| S28 | ACT3 | 第1巡回区の意見＝車庫の論理が玄関から内へ滑り込む戸（953 F.3d 112・判読不能） | still |
| S29 | ACT3 | 「for your own good」＝どの戸にも合う鍵（i2v: 鍵が回る・多数の戸に対する1本の鍵＝機序の象徴） | **motion** |
| S30 | ACT3 | **Cady**＝レッカーで私有地へ牽引される車・トランクが半開き（i2v: 牽引が引く）＝**車であって家ではない**（C3・家の象徴を一切入れない） | **motion** |
| S31 | ACT3 | 牽引された車の開いたトランクに拳銃の輪郭＝Cady の実際の事実（警察管理下の車・C3） | still |
| S32 | ACT3 | 合衆国の巡回区を陰影分けした地図＝5拡張 vs 2拒否（分裂・文字は figures 側） | still |
| S33 | ACT3 | 夕暮れの最高裁の列柱・大理石（establishing・cert 受理） | factory |
| S34 | ACT3 | 最高裁の9つの空席・正対対称・冷たい大理石（全員一致の法廷） | still |
| S35 | ACT3 | 置かれたガベル＝5月17日に判決・抑制 | still |
| S36 | ACT3 | 大理石の帯装飾を走る光の帯＝第4修正の「very core」（i2v: 光が走る・碑文的・判読不能） | **motion** |
| S37 | ACT3 | 小さく刻まれた「9-0」＋まだ半分しか閉じない戸＝「headline は罠」（全面勝訴に読ませない・C1/C2） | still |
| S38 | ACT3 | 思考実験の緊急＝灯った窓辺に凭れる shape（匿名・非グラフィック）＝判決が触れない本物の緊急（C5・救助例外の温存） | still |
| S39 | ACT3 | 離して並ぶ3枚のページ＝Roberts+Breyer / Kavanaugh / Alito の補足（象徴・中立帰属） | still |
| S40 | ACT3 | Alito のページ＝「red flag」法・自殺防止押収を「for another day」と刻む（判読不能・未決） | still |
| S41 | ACT3 | 「VACATE & REMAND」と押印され束の下へ戻される案件ファイル（i2v: 押印＋差し戻しのスライド）＝差戻し（C2） | **motion** |
| S42 | ACT3 | 卓から取り除かれた1つの言い訳がある正対の敷居＝「one excuse, off the table」（象徴） | still |
| S43 | ENDING | 再び玄関脇の荷造りバッグ・朝＝冒頭画の回帰（妻の humane な選択・顔なし） | still |
| S44 | ENDING | 返却されたホテルのキー＝かつて共有した家・二度の humane な行為の象徴 | still |
| S45 | ENDING | 大きく開いた戸の奥に warrant / consent / emergency の3つの灯った敷居＝「what stayed open」（C1） | still |
| S46 | ENDING | 玄関ドアが夜明けに開き暖かい porch-amber の日光が育つ・slow pull-back（i2v: 戸が開き光が育つ）（DESIGNED SILENCE 2.2s の画） | **motion** |
| S47 | ENDING | 順番待ちの難問＝並んで閉じた戸の列（Alito が名指しした後回しの事件・象徴） | still |
| S48 | ENDING | 夜明けの住宅街に1つだけ点る玄関灯＝未解決の余韻・CTA 域・概要欄988連動（establishing） | factory |

**source 集計（scene-primary）:** motion-primary **9**（S03 S08 S14 S17 S29 S30 S36 S41 S46）／factory-primary **5**（S05 S24 S27 S33 S48）／still-primary **34**。**scene-primary はカット全体の一部**で、残りは §5.1 の配分に従い CODEX_B の shotlist が 226 カット（still 101 / factory 93 / motion 32）へ機械展開する。**この表のシーン数・番号は固定（S01..S48）。**

---

# 4. 音の4層設計（ナレ / BGM / SFX / 環境音）

## 4.1 ラウドネス・voice（確定値・EP41/42 と同一運用）

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

## 4.2 【DESIGNED SILENCE】3箇所の実装（★デジタル無音にしない・`bgm_present` を落とす）

台本の `【DESIGNED SILENCE …】` は**ナレの沈黙であって音の沈黙ではない**。台本には3箇所（EP42 の4箇所と異なる・機械逓減にしない）。

| 位置 | 秒 | 対応画 | 鳴らすもの |
|---|---|---|---|
| HOOK 末（閉じた戸で保持→hard cut） | **1.8** | S04（閉じた玄関ドア） | BGM mute。**SFX 家の room-tone のみ**（静まる室内の残響）。デジタル無音にしない |
| ACT1 中（"checks into a hotel." 後） | **1.4** | S12（ホテルのキーカード） | BGM mute。**SFX 見知らぬ室内トーンのみ**（不慣れな部屋の空調） |
| ENDING（"daylight behind it." ＝開いた戸・payoff の最長沈黙） | **2.2** | S46（夜明けの開いた戸） | BGM mute。**SFX 朝の外気の微風 tail のみ**。感情最大の末尾を最長に |

**最長無音候補 2.2秒 << 25秒** ✓ `bgm_present` PASS。3区間ともデジタル無音にせず残響/室内ベッドを残す。**機械逓減（1.8→1.5→1.0）にはせず、payoff の ENDING を最長 2.2s にする。**

## 4.3 章ごとの BGM（1章1トラック・`build_caniglia_bgm.py`＝EP42 `build_young_bgm.py` を caniglia 用に複製）

| 区間 | 性格 | 楽器 |
|---|---|---|
| HOOK | 低弦の不解決・現在形の緊張・単音が刺す（食卓の銃・閉じた戸） | 低弦+単音メタル |
| OP | ブランドスティンガー（`BrandOpening` 付属） | — |
| ACT1 | 最短・現在形・抑制。刻みは疎で近い（あの夜） | 低弦+疎パーカッション |
| ACT2 | 転回。ケアが捜索に変わる冷たさ。押収で現在形が張る | ピアノ+弦 |
| ACT3 | 法の機械性・大理石の荘厳。**最も遅い**。全員一致の重さと honesty turn の緊張 | 低弦+弦サステイン |
| ENDING | 解決しない和音 →「dawn light」でだけ暖色（porch-amber）に開く | ピアノ+弦 |
| ENDCARD | ブランドED（`BrandEndcard` 付属） | — |

## 4.4 SFX

| 種別 | 位置 | 音 |
|---|---|---|
| gun set-down | S01/S08 | 金属が木の卓に触れる硬く低い一撃・-16 LUFS（非誇張・C5） |
| phone tone | S03/S14 | 不在着信/ダイヤルの微細トーン・-24 LUFS |
| beacon | S17 救急車の赤色灯 | 回転する赤色灯の低いハム（サイレンは鳴らさない・非扇情）・-26 LUFS |
| door | S18/S46・沈黙 HOOK末/ENDING | 玄関の軋み・開閉の残響・-18 LUFS |
| evidence bag | S19/S22 | 布・ジップ袋の擦れ・-24 LUFS |
| tow | S30 Cady | レッカーのウインチと車の軋み・-18 LUFS（車の文脈のみ・C3） |
| impact | AE v01/n01/r01 の数値着地 | 低域インパクト・-12 LUFS |
| tick | numberticker の桁変化 | 微細クリック・-24 LUFS |
| stamp | S41 `VACATE & REMAND` の押印 | ゴム/木印の一撃・-16 LUFS |
| room tone | 全編ベッド（室内・大理石の反響・朝の外気） | 広いリバーブ・-30 LUFS |

---

# 5. ビジュアル — 素材積算（★紙芝居回避＝factory実写を必ず混ぜる・1シーン1枚）

## 5.1 素材の積算（★SPEC の値をそのまま満たす配分）

```
[0] 絵が必要な区間 = narrationSeconds 721.3（BrandOpening/Endcard は Bookends が別レイヤー）
[1] 総カット = 226（SPEC）    721.3 / 226 = 3.19秒/カット  ✓ mean_shot 3.19（≤6.0）
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
[8] factory 下限 = 721.3/30 = 24.04 → ≥25本。設計値 93本   ✓
```
> **[6] の余裕は 0.31%pt しかない。still-cut を1つ増やすと 45% を割る。still-cut は 101 で固定**（16枚だけ2回・残り69枚1回）。QC で still が 85枚を割ったら §9 の**追加は同一シーンの別プロンプト（新規 distinct）**で回復させ、**cut 数は増やさない**。**still を増やして factory を削るな。**

## 5.2 SDXL と実写在庫の振り分け

- **SDXL（still 85・各1枚）= この事件にしか無い固有物**: 食卓の拳銃・荷造りバッグ・閉じた玄関ドア・裁判記録の黒塗り行・ホテルのキーカード・非緊急回線の電話・空のポーチ・布の上の2丁＋証拠タグ・空の令状机・財産返還書式・敷居・大理石の第4修正・第1巡回区の戸・鍵と多数の戸（機序）・Cady の牽引車/トランク・巡回区地図・9つの空席・ガベル・光の帯・9-0 と半閉の戸・窓辺の shape（匿名）・3枚の補足ページ・Alito の「for another day」・VACATE&REMAND のファイル・開いた戸の夜明け。
- **factory 実写 93 = どこにでもある周辺**: 夜の住宅街・救急車のいる私道の外観・地裁/最高裁の外観・列柱・大理石テクスチャ・住宅街の家並み・夜明けの街・玄関灯・ambient 繋ぎ。

## 5.3 SDXL 生成量（★バリエーション0・variants 禁止）

- `ai_prompts.v001.md` = **body 85行の固有プロンプト**（still 各1枚）＋ i2v 種 **16行** ＝ **計101エントリ**（`--only S01` の `shots=` は 101）。`generate_sdxl_4k.py PD-2026-043-caniglia`（**`--variants 1` または指定なし**）。**`--variants 3` を書かない。**
- i2v-source = **16枚**（動きが意味を持つ絵の固有プロンプト・各1シード）。CODEX_A が Wan 2.2 A14B → RIFE 48fps で 16本生成。
- **総生成 = still 85 + i2v seed 16 = 101枚（各1回）。** factory 93 は生成せず在庫選抜。
- プロンプト実体（85本）・i2v リスト（16）・factory 選定（93）は **CODEX_A** の担当（本書 §9 は絵コンテ級の記述と共通スタイル/ネガティブの契約のみ）。

## 5.4 factory のファイル名を信じない（★必須工程・CODEX_A・BLOCKING）

> EP36: `city_surveillance_camera_dome` が実際は大聖堂。EP38: 牛が `documents_on_desk`。ラベルは検索語の記録であって中身の保証ではない。

選定した **93本すべて**を `scripts/build_footage_contact_sheet.py --ep PD-2026-043-caniglia --media video --dir <factory staging>` で1本1フレームのラベル付きコンタクトシート（`runs/qc/caniglia_footage_contact_NN.png`）にし**全点目視**。subtype と食い違う本は差し替える。

## 5.5 共通スタイル接尾（各 SDXL プロンプト末尾に必ず付ける・`[STYLE]`）

```
, cinematic still, cold desaturated institutional grade, warm near-black domestic night and cold courthouse marble with deep shadows, a single warm amber porch light (or a dawn through a doorway) as the only warmth, faintly cool shadows, deep shadow detail retained, frontal symmetry with restrained telephoto compression, ultra-detailed, photoreal, 4K, 16:9, fine film grain, no text, no watermark, no logo
```
> EP39/40/41/42 との分離: 接尾に `electric blue interrogation`（EP39）・`midday suburban bleached daylight`（EP40）・`steel grey death row cellblock`（EP41）・`warrant-blue night Chicago`（EP42）を**一切含めない**。EP43 の唯一の暖色は **porch-amber `#E0913C`**。

## 5.6 共通ネガティブ（各 SDXL プロンプトの `Avoid:` に必ず付ける）

```
text, words, letters, numbers, captions, watermark, logo, readable document, legible warrant or court paper, real celebrity, recognizable real person, identifiable face, portrait, mugshot, likeness of a specific person, Edward Caniglia as a person, nude, exposed body, self-harm depiction, graphic wound, blood, gore, corpse, cartoon, illustration, 3d render, low quality, blurry, deformed, extra limbs, midday suburban daylight, electric blue interrogation, cellblock death row, warrant-blue
```
> **Cady シーン（S30/S31）の Avoid には追加で `home, house, front door, porch, dwelling` を付ける**（C3・車と家の混同を機械的に排除）。

## 5.7 AI開示（強め・毎回・R1）

AI 生成の still・i2v が画面に出ている間、常時右下に **`AI-assisted visualization`**（立ち入り/押収の再現度が高い画は **`Artistic reconstruction — AI-assisted`**）。Oswald 20px / `#C8CDD6` / opacity 70% / 位置 `[W-32, H-28]`。字幕帯と縦 56px 以上離す。概要欄1行: `Some visuals in this film are AI-assisted reconstructions, not photographs of the actual events.`

## 5.8 ★A↔B 境界契約（asset_manifest スキーマ・EP42 で3チェックが検出した不整合を最初から潰す）

- **接続点は `remotion/src/data/asset_manifest.v001.json` ただ1ファイル**。A(producer)＝CODEX_A が書き、B(consumer/validator)＝CODEX_B が読む。**counts と role enum を A/B で一字一致**させる（本書はスキーマの正を宣言・実体は A/B が同型で書く）。
- **マニフェスト配列（★A/B 同一）:** `stills` / `motion` / `factory` / `overlay` の4配列。
- **counts オブジェクト（★このキー・値で固定・A/B 一字一致）:** `{ "still_body": 85, "still_i2v_source": 16, "motion": 16, "factory": 93, "overlay": 12 }`（still の distinct 85 は本編 body・i2v 種は別 16）。cuts 展開は still 101 / factory 93 / motion 32。
- **`stills[].role` enum（★この3値のみ・A/B 同一・`thumb`/`still_thumb` を作らない）:** `body` / `i2v_source` / `reject`。
- **サムネは `role="body"` かつ `also_thumb=true` の body still **ちょうど6枚**から選ぶ**（別 role を作らない）。**候補（★still 資産 ID 空間 S01..S85＝CODEX_A §5.9・narrative S01..S48 とは別体系）:** `S01`（食卓の銃）/ `S24`（救急車の赤色灯）/ `S28`（布の上の2丁）/ `S30`（朝・開いた戸）/ `S49`（9つの空席）/ `S81`（開いた戸・昼光）。**A(CODEX_A §4.3)・B(CODEX_B §11) は同一6 asset ID に `also_thumb:true` を立てる。**
- **overlay 枚数も A/B 一致**（合成レイヤー・distinct 素材に数えない）。本書設計値 **overlay: 12**（particle 6 / light 4 / vfx 2＝CODEX_A §9）。CODEX_A/CODEX_B は共に overlay=12 で書く。
- CODEX_A は manifest を書いた直後 `validate_caniglia_manifest`（CODEX_B が複製）で counts / role / also_thumb / overlay を突き合わせ、**A の値と B の期待が一字一致**であることを確認（不一致は BLOCKING）。**`also_thumb==true` の scene_id 集合が {S01,S24,S28,S30,S49,S81} で A↔B 同一**であることも検査する。

---

# 6. After Effects ヒーロービート（8枠）— ★AEカードは密度に数えられない

## 6.1 大原則（★EP39/40 の致命傷を回避）

`check_motion_density` は **film.json の `figures+graphics` だけ**を数える。AE の 8枠は本編 mp4 に composite された後に焼き込まれるため gate は 0 カウント。→ **密度下限 31 は §7 の Remotion figures/graphics（37本）で満たす。** AE はその上に載る「決め所の数値タイポ」。

## 6.2 パイプライン（EP38/40/41/42 で measured 済み・caniglia 用に複製）

```
[1] Remotion で本編完成 → caniglia_final_bgm.v001.mp4（音声ミックス済み）
[2] scripts/ae/build_caniglia_hero_jsx.py（＝build_young_hero_jsx.py を複製）が beats.json と caniglia_hero.jsx を生成
[3] AfterFX -noui -r caniglia_hero.jsx → 各ビートを 1920x1080@30fps の不透明 mp4 で書き出し
[4] scripts/ae/composite_caniglia_hero.py（＝composite_young_hero.py を複製）が ffmpeg overlay + enable='between(t,start,end)' で焼き込み
[5] 出力 → caniglia_final_bgm.v002_ae.mp4（v001 は絶対に上書きしない）
```

## 6.3 スロット確定表（§1.4 の確定数値のみ・8枠・6制約適用・数値は台帳照合）

> **★レイアウトは複製元が実装する8種のみ**（`DATE_STAMP`/`CENTER_STACK`/`MONEY_STACK`/`SPLIT_COMPARE`/`ACT_TITLE_CARD`/`QUOTE_CARD`/`VOTE_SPLIT`/`SEAM_TRANSITION`）。**この表と CODEX_B §7.2 のデッキは id・レイアウト・F-ID が完全一致**（`validate_caniglia_beats` が両方を突き合わせる）。上記8種以外の未実装レイアウト名は使わない。MONEY_STACK はこの事件に金額が無いため**不使用**（variety は残り6種で ≥3 を満たす）。

| ID | 内容 | 数値ID | F-ID | レイアウト（実装済み8種） | カウント型 | 尺 | 対応台本行 |
|---|---|---|---|---|---|---|---|
| **d01** | 事件の日付・場所 | N01 | F08 | **DATE_STAMP** | なし | 5.0 | "It is August 2015, in a house in Cranston" |
| **n01** | 押収の事実 | N02/N03 | F09 | **CENTER_STACK** | なし | 6.0 | "the officers go inside his home and take two handguns. No warrant." |
| **t01** | 幕3 判例核の幕頭 | — | — | **ACT_TITLE_CARD** | なし | 5.0 | （ACT3 幕頭「where 'caretaking' came from, and where it stops」） |
| **c01** | Cady＝車であって家でない | N05 | F05 | **SPLIT_COMPARE** | なし | 6.5 | "Cady was about a car … a vehicle is not a house" |
| **q01** | Thomas 逐語（車と家の別） | N16 | F07 | **QUOTE_CARD** | なし | 7.0 | "what is reasonable for vehicles is different from what is reasonable for homes" |
| **v01** | 9–0（限定併記） | N10 | F03 | **VOTE_SPLIT** | なし | 7.5 | "the Court is unanimous. Nine to nothing." |
| **s01** | 温存された例外 | N15 | F17 | **CENTER_STACK** | なし | 6.5 | "a valid warrant; your consent; and exigent circumstances" |
| **r01** | 差戻し（最終決着でない） | N14 | F03 | **CENTER_STACK** | なし | 6.0 | "vacated the decision against him and sent the case back down" |

> **★行順＝start 昇順（時系列）:** `d01`(ACT1 導入) < `n01`(ACT2 押収) < `t01`(ACT3 幕頭) < `c01`/`q01`/`v01`/`s01`/`r01`(ACT3)。**この id・レイアウト・F-ID・順序は CODEX_B §7.2 デッキと一字一致**（`validate_caniglia_beats` が突き合わせ）。

### 検算

```
[1] 単調増加・重複ゼロ（start は §6.4 beats.json で幕位置に配置・台本行の秒に一致）
[2] HOOK / BrandOpening / ENDING payoff の最長沈黙(2.2s) / BrandEndcard に1秒も重ならない
[3] 合計 = 5.0+5.0+6.0+6.5+7.0+7.5+6.5+6.0 = 49.5秒 / 733.8 = 6.7%   ✓ 過剰でない
[4] レイアウト種類 = DATE_STAMP, ACT_TITLE_CARD, CENTER_STACK, SPLIT_COMPARE, QUOTE_CARD, VOTE_SPLIT = 6種（全て実装済み8種内）   ✓ ≥3
[5] figures[] 34枠と1秒でも重ならない（validate_caniglia_beats.py が両方突き合わせ・§7.3）
```

## 6.4 `beats.json`（`08_edit/ae_hero/beats.json`・`schema_version: "caniglia_beats.v1"`・EP42 と同一スキーマ）

**確定ラベル（★ASCII のみ・em-dash 禁止＝`-` に置換・全大文字・6制約適用）:**
```
d01 DATE_STAMP     date="AUGUST 2015"  place="CRANSTON, RHODE ISLAND"          # F08/N01・事件の日付/場所
n01 CENTER_STACK   top="THE SEIZURE"  main="TWO HANDGUNS"
        bottom="NO WARRANT"                                                    # F09/N02/N03・押収の事実
t01 ACT_TITLE_CARD title="WHERE CARETAKING STOPS"  kicker="ACT THREE"          # 幕頭・still=大理石の第4修正
c01 SPLIT_COMPARE  top="WHERE CARETAKING CAME FROM"  left="A CAR IN CUSTODY"  right="NOT A HOME"
        bottom="CADY v. DOMBROWSKI, 1973"                                      # F05/C3: 車であって家でない・Cady 限定
q01 QUOTE_CARD     quote="WHAT IS REASONABLE FOR VEHICLES IS DIFFERENT FROM WHAT IS REASONABLE FOR HOMES"
        attribution="JUSTICE THOMAS, FOR THE COURT"                            # F07/N16・逐語・C3/C6
v01 VOTE_SPLIT     top="CANIGLIA v. STROM - MAY 2021"  left="9"  right="0"
        bottom="ONE EXCUSE, CLOSED"                                            # F03/N10・C1/C2: 全面勝訴に読ませない
s01 CENTER_STACK   top="THE DOORS THAT STAYED OPEN"  main="WARRANT - CONSENT - EMERGENCY"
        bottom="THESE EXCEPTIONS STILL LET POLICE IN"                          # F17/N15・C1: 温存例外の核
r01 CENTER_STACK   top="THE DISPOSITION"  main="VACATE AND REMAND"
        bottom="SENT BACK DOWN - NOT ENDED IN HIS FAVOR"                       # F03/N14・C2: 差戻し=最終勝訴でない（"not a final win" は使わない）
```
> **v01 の bottom は "ONE EXCUSE, CLOSED"（★"final win" 系の文字列を書かない＝R-FORBID 一致）**（C2）。**「最終勝訴でない」限定は別カード r01 の "SENT BACK DOWN - NOT ENDED IN HIS FAVOR" が担う（削除禁止）。s01 の main "WARRANT - CONSENT - EMERGENCY" ＋ bottom は削除禁止**（C1・温存例外の可視化）。**c01 は car/custody 側と home 側を必ず別レイヤーで対比し、`home` を Cady と同一物にしない**（C3）。**q01 の quote は逐語のみ**（要約を引用符に入れない・facts_lock R-PAYTON/中立帰属で確認）。**どのカードにも「police cannot enter your home without a warrant」を無留保で書かない**（C1）。**988 は AE カードにしない**（description/BrandEndcard のみ・C5）。数値ID＝台帳（§1.4）と一致必須。カウント終了から区間終端まで最低 1.20秒ホールド。
> **★AI開示レイヤー（R1・全カード常時）:** 共通レイヤースタック（§6.5）に `AI-assisted visualization`（Oswald 20px / SILVER `#C8CDD6` / opacity 70% / 右下 `[W-32, H-28]`）を1枚追加し全カードに焼く。AEカードは不透明の全画面 mp4 として本編に overlay され本編右下の開示を覆うため、これが無いと AI生成 static 背景が開示なしで表示される（R1 違反）。`validate_caniglia_beats` と §13 受入アイボールで「AEカード表示中も開示が見える」を確認。

## 6.5 レイアウト定義（EP42 §6.5 を踏襲・色定数のみ EP43 値）

**共通レイヤースタック（下→上）:** L9 黒ソリッド → L8 静止画（scale fill→fill×1.08・drift）→ L7 グレードウォッシュ（**暖い near-black** `addSolid([0.078,0.067,0.055])`＝NIGHT / MULTIPLY / opacity 30）→ L6 羽根付き楕円ビネット → L5 グロー（下中央 porch-amber 実用光 ADD）→ L4 ライトスイープ（`"ADBE Rotate Z"`=18）→ L3 上ラベル（Oswald）→ L2b アクセントライン（ACCENT porch-amber・scaleX ワイプ・`motionBlur=true`）→ L2 主数値/主文字（Anton・ACCENT・`motionBlur=true`）→ L1b 下ラベル → L1 字幕ロワーサード → **L0b AI開示テキスト（`AI-assisted visualization`・Oswald 20px・SILVER `#C8CDD6`・opacity 70%・右下 `[W-32, H-28]`・全カード常時焼き＝R1）** → L0 黒シームディップ（head/tail 各4フレーム）。

**色定数（0..1 float）:**
```python
ACCENT = [0.878, 0.569, 0.235]   # #E0913C — porch-amber（数値・下線・唯一の実用光）
WHITE  = [0.961, 0.969, 0.980]   # #F5F7FA
SILVER = [0.784, 0.804, 0.839]   # #C8CDD6
NIGHT  = [0.078, 0.067, 0.055]   # #14110E — 暖い near-black ウォッシュ寄り
MARBLE = [0.227, 0.231, 0.251]   # #3A3B40 — 大理石（ACT3）
BEACON = [0.780, 0.314, 0.243]   # #C7503E — 救急車の赤色灯のグローのみ（数値/下線に使わない）
```
**フォント:** 数値/主文字 = **Anton Regular** / ラベル・字幕 = **Oswald Medium**。`getFontsByFamilyNameAndStyleName` で厳格解決（miss は throw・フォールバック禁止）。テキスト幅は **`sourceRectAtTime(t,false).width` で実測**（advance-width 推定禁止＝EP40 文字切れの原因・ブリーフ§5）。

**カウント型:** この事件は金額が無く、9-0/5-2/9-0 の得票はカウント不可（得票のため）。→ **本編 AE ではカウントアニメを使わず全て静的タイポ**で settle（ease-out cubic）。数値の「着地」インパクトは L2 の scale/opacity 併用と impact SFX で作る。

## 6.6 このマシン固有の罠（★1つ忘れると無言で品質が落ちる・EP42 §6.6 全項を caniglia に適用）

フォント解決の例外ラップ（`psName()`）／spatial ease は配列次元1（`prop.isSpatial ? 1 : ...`）／OM=`"H.264 - レンダリング設定を一致 - 15 Mbps"`・RS=`"最良設定"`（英語名は try/catch フォールバック）／`app.newProject()` を headless で使わない（同名 `CANIGLIA_` コンプを防御削除）／`layer.motionBlur=true` を動くレイヤー個別に／回転は `"ADBE Rotate Z"`／改行は1行厳守（SPLIT_COMPARE の左右2値は別レイヤー）／em-dash は `-`／inPoint と outPoint 両方設定／`item.mainSource.conformFrameRate = 30`／実行パス `C:\Program Files\Adobe\Adobe After Effects 2026\Support Files\AfterFX.exe`／`proj.gpuAccelType = GpuAccelType.SOFTWARE`／ビルド ~100–120秒・完了マーカー `render/_build_ok.txt` をポーリング（タイムアウト≥300秒）・末尾で `app.quit()`／**aerender 前に `.aep` mtime > `.jsx` を assert**（ブリーフ§5・.aep が古いと前ビルドを焼く事故）。

## 6.7 コンポジタ（`scripts/ae/composite_caniglia_hero.py`・SKIP 4条件を1つも削らない）

`BASE = caniglia_final_bgm.v001.mp4` / `OUT = caniglia_final_bgm.v002_ae.mp4`（v001 不変）。SKIP: (1) `render/<id>.mp4` 不在 / (2) 解像度≠1920x1080 / (3) 実測尺 `< dur-0.3` / (4) `beat.end > base_dur`。ffmpeg: `overlay=0:0:eof_action=pass:enable='between(t,start,end)'` / `-c:v libx264 -preset slow -crf 16 -pix_fmt yuv420p -colorspace bt709 -c:a copy`。**出荷済みを絶対に上書きしない。**

---

# 7. Remotion MGビート（FigureBeats）— ★密度下限 31 は必ずここで満たす

## 7.1 密度の設計（`caniglia_film.json` の `figures[]` ＋ `graphics[]`）

`check_motion_density`: 3つを AND。**body-minutes = narrationSeconds/60 = 721.3/60 = 12.022**。

| 指標 | floor | EP43 設計値 |
|---|---|---|
| density | ≥2.5/min | figures 34 + graphics 3 = **37 beats / 12.022 = 3.08/min** ✓（SPEC beats_floor 31 に +6） |
| coverage | ≥0.25 | 37 beats × 平均 6.0秒 = 222秒 / 721.3 = **0.308** ✓ |
| variety | ≥3 distinct forms | **14種**（下記） ✓ |

> **AE の 8枠は film.json に入れない**（composite 後に焼くため gate 非カウント）。**density は Remotion 側 37 beats だけで 31 を超える。**

## 7.2 `figures[]` の種類配分（★kind は全部小文字・同一 kind を連続させない・ブリーフ§5・`comparebars` は非実在→`compbars`）

**使用可能 kind（全小文字）:** `numberticker` `timeline` `bar` `kinetic` `acttitle` `lowerthird` `dochighlight` `routemap` `pindropmap` `regionmap` `compbars`（※`comparebars` は存在しない）`mechanism` `quote` `stat` `votetally`。**大文字は無音描画になる。**

| kind（小文字） | 枠数 | EP43 での用途（6制約適用） |
|---|---|---|
| `acttitle` | 3 | ACT1「The night」/ ACT2「The welfare check」/ ACT3「Where caretaking stops」 |
| `timeline` | 5 | ①事件: 2015/8 口論→翌朝 welfare check→拳銃押収 ②訴訟: 地裁敗訴→第1巡回区 2020→cert→2021/3/24 argued→2021/5/17 decided ③Cady 1973→住居へ drift→2021 で封鎖 ④seven weeks（argued→decided）⑤補足意見3件の並び |
| `stat` | 6 | TWO HANDGUNS（N02）／NO WARRANT（N03）／NEARLY 50 YEARS（N06・Cady→2021）／SEVEN WEEKS（N09）／THREE OPINIONS（N13）／9-0（N10・**votetally と別区間・"one excuse closed" ラベル同梱**） |
| `quote` | 3 | ①Thomas 逐語「what is reasonable for vehicles is different from what is reasonable for homes」（**Court 帰属**・C3）②Jardines 逐語「the right of a man to retreat into his own home and there be free from unreasonable governmental intrusion」（**Jardines 帰属**・C6）③Alito 逐語「for another day」（**Alito 帰属**・red flag/自殺防止押収は未決・C5/C1）。**要約を引用符に入れない・facts_lock で逐語確認** |
| `dochighlight` | 3 | 第4修正「persons, houses, papers, and effects」（判読ハイライト・C6）／holding「no free-standing community-caretaking exception」（住居拡張のみ否定・C1）／disposition「vacated and remanded」（N14・C2） |
| `lowerthird` | 2 | 「First Circuit, 953 F.3d 112 (2020)」（N04・帰属）／「Caniglia v. Strom, 593 U.S. 194 (2021), No. 20-157」（N11・帰属・本文で読み上げない） |
| `compbars` | 3 | 5拡張 vs 2拒否（N12・巡回区分裂）／閉じた1つの言い訳（caretaking）vs 温存3例外（warrant·consent·emergency）（C1）／**Cady（"a car, not a house"）vs a HOME（Cady never reached）**（C3・射程非圧縮・★"not a house" を Cady と同一 payload に明記＝R-CADY 合格） |
| `votetally` | 1 | **9–0 Caniglia のみ**（F-VOTE・unanimous:9/dissent:0・**"vacate & remand - one excuse closed" ラベル必須**・C2）。**他の数値は votetally に入れない** |
| `numberticker` | 2 | SEVEN WEEKS（N09・AE と別区間）／THREE OPINIONS（N13・補足意見3件） |
| `pindropmap` | 1 | Cranston, Rhode Island（事件の家・単一ピン・C15） |
| `regionmap` | 1 | 合衆国の巡回区＝第5/6/8/9/1が住居へ拡張・第3/7が拒否（N12・分裂の地理） |
| `mechanism` | 2 | 危険の機序: 「for your own good」→どんな立ち入りも caretaking と説明できる→any door への鍵（C1）／honesty turn: vacate → remand → 正しい基準で再判断 → 別例外を再主張しうる（C2） |
| `bar` | 2 | 温存例外3つ vs 封鎖1つの重み（C1）／argued→decided の 7週間の時間バー（N09） |
| **合計** | **34** | variety = 13 figure-kinds |

`graphics[]`（kinetic typography）3枠: 幕タイトルの語同期切れ上がり等（`kinetic`）。→ variety に `kinetic` が加わり **14種** ≥3 ✓。

> **★実装表現（CODEX_B §6）:** CODEX_B は上記 34+3 を **すべて `figures[]` に 37本**入れ、`graphics[]=[]` にする（`check_motion_density` は `figures+graphics+heroCuts` を合算するので密度は同値・floor 31 に +6）。「figures 34/graphics 3」は DESIGN 上の役割分類であり、film.json 上は全 37 が figures[]・graphics[] は空配列。どちらで数えても 37 beats。

## 7.3 配置ルール

1. **AE の 8区間（§6.3）と1秒でも重ならない**（`validate_caniglia_beats.py`＝validate_young_beats.py を複製・両方突き合わせ）。
2. 幕あたり配分: HOOK/OP=3 / ACT1=4 / ACT2=7 / ACT3=15 / ENDING=5（ACT3 が最長 336.9s なので厚め）。
3. **同じ kind を連続させない。**
4. 1枠 4.0–8.0秒。
5. ACT3 の説明区間に `compbars`＋`quote`＋`timeline`＋`mechanism`＋`regionmap` を分散し 20秒超の平坦区間をゼロに。
6. `quote` は**逐語のみ**（要約を引用符に入れない・C3/C6）。帰属は Court / Jardines / Alito に帰属語を伴う。
7. `figures[].text`/`lines[]` は `facts_lock` 検査対象（「police cannot enter your home」無留保・「full victory」・Cady=home 混同・988 の扇情配置 を出さない）。

## 7.4 密度の最終検算

```
Remotion figures 34 + graphics 3 = 37 kinetic beats（film.json 内）
  density  = 37 / 12.022 = 3.08/min   ✓ ≥2.5（SPEC beats_floor 31 → 37 で +6）
  coverage = 222s / 721.3 = 0.308      ✓ ≥0.25
  variety  = 14 forms                  ✓ ≥3
AE hero 8枠は composite 後・gate 非カウント（上乗せの決め所）
```

---

# 8. レイヤー構成 と ゾーン分離（★主役の裏に最低4層）

## 8.1 本編カットのレイヤー構成（下→上・主役 L4 の裏に L1/L2/L3/L3b = 4層）

| L | 名前 | EP43 の値 |
|---|---|---|
| **L0** | ルート背景 | `#0A0A0C`（INK） |
| **L1** | グラデ背景 | `radial-gradient(120% 120% at 50% 40%, #14110E 0%, #0F0C0A 45%, #0A0A0C 100%)`（暖い夜の near-black。ACT3 のみ大理石寄り `#1A1B1F` にシフト可） |
| **L2** | グリッド/ライン | 縦横 64px の反復線＋放射マスク＋ドリフト。`repeating-linear-gradient(0deg/90deg, #E0913C18 0px 1px, transparent 1px 64px)`、`translateY 0→48px` / `Easing.inOut(Easing.sin)`（等速禁止） |
| **L3** | グロー | 単一 porch-amber 実用光。`radial-gradient(closest-side, #E0913C66 0%, #E0913C18 45%, transparent 75%)`、`filter: blur(28px)`。位置は幕で移動（食卓の銃→ポーチ→救急車(BEACON差色)→大理石→夜明けの戸） |
| **L3b** | 大理石の光帯/ビネット | ACT3 は第4修正の光帯（`linear-gradient(100deg, transparent, #E0913C22, transparent)` を横に slow drift）、他幕は羽根ビネット。`translateX` を `Easing.inOut(Easing.sin)` で微動（静止フレームゼロ） |
| **L4** | 主役（still / i2v / factory） | §10 のモーション（Ken Burns/parallax/i2v） |
| **L5** | テロップゾーン（上/中央・figures） | §8.2 |
| **L6** | 字幕ゾーン（下部帯） | §8.2 |

> **主役（L4）の裏に L1/L2/L3/L3b = 4層**（グラデ背景・グリッド/ライン・グロー・光帯/ビネット）で CLAUDE.md「最低3レイヤー」＋タスク「最低4層」を満たす。

## 8.2 ゾーン分離（一度も重ねない）

| ゾーン | 縦位置（1080基準） | スタイル |
|---|---|---|
| テロップ見出し | `y=96–260` | Oswald 64px / `#F5F7FA` / letterSpacing 4 |
| 中央テロップ / figures | `y=420–660` | §7 |
| 出典テロップ（アクセントライン） | `y=742–786` | Oswald 28px / porch-amber `#E0913C` 3px 下線 |
| 字幕帯 | `y=872–1010` | 白 `#FFFFFF` + `textShadow:0 0 6px #000,0 2px 4px #000` / 半透明黒帯 `rgba(6,6,8,0.62)` / ≤2行・1行≤42字 / 54px / lineHeight 1.28 |
| AI開示 | `y=1024–1052`（右下） | Oswald 20px / `#C8CDD6` / opacity 70% |

**Caption QC:** ナレ一致 ≥99%（faster-whisper 強制アライン）/ `.srt` カバー ≥95% / キュー 1.0–6.0秒 / CPS ≤17 / 単語割り禁止 / 1語孤立キュー禁止 / ズレ ≤120ms。**【DESIGNED SILENCE】3区間には字幕キューを置かない。**

---

# 9. 絵コンテ（★48シーン・象徴のみ・6制約・Caniglia/Cady 非人物化・CODEX_A が 85本プロンプトへ展開する原図）

## 9.1 パーサ契約（★CODEX_A が `ai_prompts.v001.md` を書くときの形式・`read_prompts()` が読む2行形式）

`read_prompts()` の正規表現は `^\s*-\s+`([^`]+\.png)`\s*$`。つまり:
```
- `S01.png`
<positive prompt> ... [STYLE] Avoid: <negative>
```
- **1行目:** `` - `S01.png` ``（バッククォート囲み・行末は `.png` 直後）。プロンプトを同じ行に書かない。
- **2行目:** 正プロンプト → `[STYLE]`（§5.5）→ `Avoid:` → 負プロンプト（§5.6）。
- 配置先: **`episodes/PD-2026-043-caniglia/04_scenes/ai_prompts.v001.md`**。生成: `.venv/Scripts/python.exe scripts/generate_sdxl_4k.py PD-2026-043-caniglia`（**variants 指定なし＝1枚**）。
- 出力: `H:\pd-media\assets\ai\caniglia\S01.png …` ＋ `remotion/public/caniglia/`。長辺 ≥3840 で冪等スキップ。
- **★body 85本＝85行**（still 各1枚）＋ **i2v 種 16行**（CODEX_A §8.1a）＝ `ai_prompts.v001.md` は計 **101 エントリ**。CODEX_A は書いた直後 `--only S01` で `shots=` が **101**（body 85 + i2v種 16）に達しているか（2行形式が壊れていないか）を確認。

## 9.2 絵コンテ級ショット記述（Sid ごと・カメラ/モーション/象徴/制約。CODEX_A はこれを固有プロンプトに翻訳）

> **全ショット共通:** 顔・身体・肖像なし（R1/C4）。Edward Caniglia を個人として描かない（象徴・影・後ろ姿のみ）。読める文字を作らない（redacted/illegible）。暖い夜の near-black＋冷たい大理石＋唯一の暖色 porch-amber。「police cannot enter your home」「全面勝訴」を画に含意させない。Cady（S30/S31）は車のみで家の象徴を一切入れない（C3）。メンタルヘルスは非扇情（C5）。1シーン1枚＝各 Sid の主 still は1本。ambient は factory で埋める。

| Sid | カメラ/レンズ | 象徴（動き） | 制約メモ |
|---|---|---|---|
| S01 | 俯瞰寄り・接写 | 食卓に平置きの拳銃1丁・暖い低照度・手も顔もなし | C4/C5: 象徴のみ・非誇張 |
| S02 | 正対・寄り | 閉じた玄関脇の荷造りバッグ・サイド窓から porch-amber | C4: 人物なし |
| S03 | 接写・ナイトスタンド | 電話の画面が灯る不在着信（i2v: パルス） | 予兆・扇情なし |
| S04 | 正対・静止 | 内側から見た閉じた玄関ドア（DESIGNED SILENCE 1.8s） | 後で S46 と対 |
| S05 | 引き・外 | 夜の質素な家・1つ点る玄関灯（factory ambient） | — |
| S06 | 正対・slow push-in | 手のひら幅だけ開いた戸＋背後グリッド＝あなたの問い | 中立 |
| S07 | 広め・室内 | 薄暗い居間・2脚の椅子・口論の残り（人物なし） | C4 |
| S08 | 手元接写 | 食卓に拳銃が置かれる（i2v: ゆっくり置く・手元のみ） | C4/C5: 顔なし・非演出 |
| S09 | 接写・机上 | 裁判記録の黒塗り1行が淡く光る（"shoot me" 記録事実・1回） | C5: 非グラフィック・1回のみ |
| S10 | 俯瞰・寄り | 椅子の上着＋持ち上がる一泊バッグ（妻が出る象徴） | C4: 身体なし |
| S11 | 外・寄り | 玄関ドアが静かに閉じる・玄関灯は点いたまま | — |
| S12 | 接写・ナイトスタンド | 見知らぬ部屋のホテルのキーカード（DESIGNED SILENCE 1.4s） | 沈黙の画 |
| S13 | 接写・戸下 | 翌朝・閉じた戸の下から差す光＝「about that door」 | 回帰の起点 |
| S14 | 接写・手元 | 非緊急回線をダイヤルする電話（i2v: 911でない・ダイヤル） | 事実: non-emergency line |
| S15 | 正対・日中 | 空のポーチ・2つの長い影（穏やか・顔なし） | C4: 影のみ |
| S16 | 寄り | 開いた網戸・マグ＝「alive, talking, calm」 | C4: 人物なし |
| S17 | 私道・寄り | 救急車の赤色灯が回る（i2v: BEACON 差色の回転掃引・サイレン鳴らさない） | C5: 非扇情 |
| S18 | 正対 | 開いたまま立つ玄関ドア・揺れるカーテン＝去った後の立ち入り | C1: 無令状の立ち入り |
| S19 | 俯瞰・机上 | 布の上の拳銃2丁＋証拠タグ＝押収 | C4: 身体なし |
| S20 | 接写・机上 | 令状が置かれるべき空の机＝「No warrant」（不在） | C1 |
| S21 | 接写 | 財産返還の裁判書式（判読不能）＝銃を取り戻す提訴 | facts_lock illegible |
| S22 | 接写 | 証拠袋の2丁＋タグ（判読不能）＝「smaller fight」 | — |
| S23 | 正対 | 再び敷居＝「who gets to open it」 | C1: 家/戸のモチーフ |
| S24 | 引き・外 | 静かな住宅街の家並み（factory ambient）＝「simply legal」 | — |
| S25 | 寄り | 日中も点いた玄関灯＝「concern」の皮肉（porch-amber） | 象徴 |
| S26 | 壁ショット | 大理石の第4修正「persons, houses, papers, and effects」（判読困難） | C6: 逐語は figures |
| S27 | 引き・外 | 地裁の冷たい扉（factory ambient）＝下級審敗訴 | — |
| S28 | 象徴・接写 | 車庫の論理が玄関から内へ滑り込む戸（953 F.3d 112・判読不能） | C1: 拡張＝住居 |
| S29 | 象徴 | 多数の戸に対する1本の鍵が回る（i2v: 鍵）＝「for your own good」の機序 | C1: 過大化の危険を象徴 |
| S30 | 象徴・寄り | レッカーで私有地へ牽引される車・トランク半開き（i2v: 牽引が引く） | **C3: 車のみ・家/戸/ポーチを一切入れない** |
| S31 | 接写 | 牽引車の開いたトランクに拳銃の輪郭＝Cady の事実（警察管理下の車） | **C3: home 語を Avoid に追加** |
| S32 | 地図・引き | 合衆国の巡回区を陰影分け＝分裂（文字なし・figures 側で数値） | — |
| S33 | 引き・列柱 | 夕暮れの最高裁の列柱・大理石（factory ambient）＝cert | — |
| S34 | 正対・対称 | 9つの空席・冷たい大理石＝全員一致の法廷 | — |
| S35 | 接写 | 置かれたガベル＝5月17日・抑制 | — |
| S36 | 壁ショット | 大理石の帯を走る光＝「very core」（i2v: 光が走る・碑文的・判読不能） | C6: 象徴・逐語は figures（Jardines 帰属） |
| S37 | 象徴・接写 | 小さく刻まれた「9-0」＋まだ半分しか閉じない戸 | C1/C2: 全面勝訴に読ませない |
| S38 | 象徴・抑制 | 灯った窓辺に凭れる匿名の shape（非グラフィック）＝本物の緊急 | C5: 匿名・非グラフィック・救助例外の温存 |
| S39 | 机上 | 離して並ぶ3枚のページ＝Roberts+Breyer / Kavanaugh / Alito 補足 | 中立帰属 |
| S40 | 接写 | Alito のページ「for another day」＝red flag/自殺防止押収は未決（判読不能） | C5/C1: 未決を象徴 |
| S41 | 机上 | 「VACATE & REMAND」押印＋束の下へ戻るファイル（i2v: 押印＋スライド） | C2: 差戻し |
| S42 | 正対 | 卓から取り除かれた1つの言い訳がある敷居＝「one excuse, off the table」 | C1/C2: 限定 |
| S43 | 正対 | 再び玄関脇の荷造りバッグ・朝＝冒頭の回帰（顔なし） | C4 |
| S44 | 接写 | 返却されたホテルのキー＝かつて共有した家 | 象徴 |
| S45 | 正対 | 大きく開いた戸の奥に warrant/consent/emergency の3つの灯る敷居 | C1: 温存例外 |
| S46 | 引き・pull-back | 夜明けに開く玄関ドアから porch-amber の日光が育つ（i2v: 戸が開き光が育つ）（DESIGNED SILENCE 2.2s） | C4: 人物なし・payoff |
| S47 | 象徴 | 並んで閉じた戸の列＝順番待ちの難問（Alito の後回し事件） | 象徴 |
| S48 | 引き・夜明け | 住宅街に1つ点る玄関灯＝未解決の余韻・988連動（factory ambient） | C5: 概要欄988 |

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
**0.5s 刻み方針:** 226カットの境界は **`QUANT`=15フレーム（0.5秒）にスナップ**して配置する。各カット長は `CUT_MIN`〜`CUT_MAX`、平均 `CUT_MEAN`。ACT3 は最も遅く（長カット寄り・6.0s 近辺を多用）、ACT1 は速く（1.0–2.5s の断片・現在形）。CODEX_B は shotlist の各 span 端を 15f グリッドに丸める。

## 10.2 全カット共通モーション（★静止フレームを1枚も作らない）

| 素材 | 基本モーション | イージング | 数値 |
|---|---|---|---|
| **still** | Ken Burns：`scale 1.00→1.08` を**カット全長**で。加えて `translate` を象徴方向へ ±24px | `Easing.out(Easing.cubic)` | scale 差 +0.08 / drift 24px。**opacity は translate/scale と必ず対**（単独禁止） |
| **i2v** | ネイティブ動き（Wan 2.2 A14B → RIFE 48fps）＋微 `scale 1.00→1.03` | ネイティブ＋`Easing.out(Easing.cubic)` | 追い足しの scale は 0.03 のみ |
| **factory** | 実写の内在動き＋微 Ken Burns `scale 1.00→1.04` | `Easing.out(Easing.cubic)` | 24pxまでの parallax 可 |

**カットイン/アウト:** クロスディゾルブ 6–10f または hard cut。ACT1 のあの夜の断片は hard cut 寄り（現在形・抑制）。ACT3 は長めのディゾルブ（荘厳・最も遅い）。**フェードは opacity 単独にせず、入りは `translateY 12px→0`＋opacity、抜けは `scale 1.00→1.02`＋opacity を対にする。**

## 10.3 速い動きの motion-blur（★@remotion/motion-blur の Trail）

```tsx
import {Trail} from '@remotion/motion-blur';
// 速いカット（S03 電話パルス / S17 救急車の赤色灯回転 / S30 レッカー牽引 / S41 押印スライド / numberticker / 幕頭 kinetic）
<Trail layers={6} lagInFrames={1.2} trailOpacity={0.45}>
  {/* 主役 or 動く数値/文字 */}
</Trail>
```
対象: **S03**（電話パルス）、**S17**（救急車の赤色灯回転）、**S30**（Cady 牽引）、**S41**（VACATE&REMAND 押印）、および §7 の `numberticker`・幕頭 `kinetic`。**S08（食卓に銃を置く）・S46（夜明けの pull-back）・S36（光が走る）は緩なので Trail 不要**（無駄な残像・扇情を避ける・C5）。ゆっくりした Ken Burns には Trail をかけない。

## 10.4 テキストのマスク切れ上がり（★基本形・全 figures / 字幕見出し / 幕タイトル・overflow:hidden＋translateY）

```tsx
// overflow:hidden の親に対し、子を translateY(110% → 0) で spring 切れ上がり
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

# 11. オープニング（OP）設計 — 完全仕様（`OpeningCaniglia`・fps=60・CLAUDE.md §1–5 全項目）

## 11.1 秒数ベースのタイムライン（fps=60・「フレーム」は全て `Math.round(60 × 秒)`・直書き禁止・0.5s 刻み方針で全区間記述）

```ts
const FPS_OP = 60; const F = (s:number)=>Math.round(FPS_OP*s);   // 総 180f = F(3.0)
```

| 秒 | フレーム | 起きること（EP43 signature = 閉じた玄関脇に灯る porch-amber の玄関灯） |
|---|---|---|
| 0.00–0.10 | f0–6 | 画面 `#0A0A0C`。**L1** グラデ opacity 0→1（0.40s）＋ **scale 1.08→1.00** を 180f で（`Easing.out(Easing.cubic)`）。opacity 単独でなく scale 併用 |
| 0.10–0.15 | f6–9 | **L6 ロゴ**（`hasLogo`）左上 `top:64/left:72` に spring 出現。scale 0.4→1.0・opacity 0→1（併用・`damping:14,mass:0.9`） |
| 0.15–0.25 | f9–15 | **L2** グリッドが spring（`{damping:200,mass:1,durationInFrames:F(0.8)=48}`）で reveal。最終 opacity=`gridReveal*0.18`。全体を 180f で `translateY 0→48px`（`Easing.inOut(Easing.sin)`） |
| 0.25–0.30 | f15–18 | **L3** porch-amber の玄関灯グローが spring（`{damping:18,mass:1.2}`）＝閉じた戸の脇に点る。scale 0.6→1.15 / opacity 0→0.85（併用）。`filter:blur(28px)` |
| 0.30–0.86 | f18–52 | **L4 主役タイトル**が1文字ずつ切れ上がる（`overflow:hidden` マスク）。各文字 spring（`{damping:16,mass:1}`）で `translateY 110%→0`、opacity=`interpolate(sp,[0,0.25],[0,1])`。**スタッガー=`F(0.04)=2フレーム/文字**。全体を `Trail`（`layers=6,lagInFrames=1.2,trailOpacity=0.45`）で包む |
| 0.55–1.15 | f33–69 | **L2b 敷居の光ライン**（EP43固有＝玄関灯が戸の縁を舐める暖色の帯）。中央からタイトル背後を横切る光が `scaleX 0→1`＋`opacity 0→0.55`（spring `{damping:22,mass:1.1}`, `transformOrigin:'center'`）。porch-amber。opacity 単独禁止で scaleX 併用 |
| 0.95–1.35 | f57–81 | **L5a** porch-amber の下線が左から `scaleX 0→1`（spring `{damping:16,mass:0.8}`, `transformOrigin:'left center'`）。240×6px・`boxShadow:0 0 24px #E0913Caa` |
| 1.10–1.55 | f66–93 | **L5b** サブタイトルが `translateY 24px→0`＋opacity 0→1（spring `{damping:20,mass:1}`・併用） |
| 1.55–2.20 | f93–132 | 全要素 settle。背景 scale 1.02 付近を減速進行。グリッドのドリフト継続。**完全静止フレームゼロ** |
| 2.20–3.00 | f132–180 | ホールド。背景 scale 1.00 着地、グリッド translateY 48px 着地。**フェードアウトしない** |

> **0.5s 刻み方針:** 上表の各 0.5s 境界（0.0/0.5/1.0/1.5/2.0/2.5/3.0）で「何が動いているか」が必ず1つ以上ある（静止区間ゼロ）。スクラブ確認は §11.4。

## 11.2 イージング・ディレイ・移動量・damping（数値表・等速線形ゼロ・opacity 単独ゼロ）

| 要素 | プロパティ | 種別 | 数値 |
|---|---|---|---|
| L1 背景 | scale 1.08→1.00 | `Easing.out(Easing.cubic)` | 180f |
| L2 グリッド reveal | opacity 0→gridReveal*0.18 | spring | `{damping:200,mass:1,durationInFrames:48}` |
| L2 グリッド drift | translateY 0→48px | `Easing.inOut(Easing.sin)` | 180f |
| L3 グロー | scale 0.6→1.15 / opacity 0→0.85 | spring | `{damping:18,mass:1.2}` |
| L4 各文字 | translateY 110%→0 / opacity | spring | `{damping:16,mass:1}`・スタッガー 2f |
| L4 Trail | 残像 | — | `layers=6,lag=1.2,opacity=0.45` |
| L2b 敷居の光 | scaleX 0→1 / opacity 0→0.55 | spring | `{damping:22,mass:1.1}`・origin center |
| L5a 下線 | scaleX 0→1 | spring | `{damping:16,mass:0.8}`・origin left |
| L5b サブ | translateY 24px→0 / opacity | spring | `{damping:20,mass:1}` |
| L6 ロゴ | scale 0.4→1.0 / opacity | spring | `{damping:14,mass:0.9}` |

> **全 opacity が translateY/scale/scaleX と対。等速線形を1箇所も使わない。**

## 11.3 レイヤー構成（下→上・主役 L4 の裏に L1/L2/L2b/L3 = 4層）

L0 `#0A0A0C` / L1 グラデ（`radial-gradient(120% 120% at 50% 35%, #14110E 0%, #0F0C0A 45%, #0A0A0C 100%)`）/ L2 グリッド（`${accent}22` 64px・放射マスク）/ L2b 敷居の光（`linear-gradient(90deg, transparent, ${accent}cc, ${accent}55, ${accent}cc, transparent)`）/ L3 porch-amber 玄関灯グロー（`radial-gradient(closest-side, #E0913C88, #E0913C22, transparent)` `blur(28px)`）/ L4 主役タイトル（Trail 包み・`overflow:hidden` span マスク・Anton `fontWeight:800 fontSize:150 letterSpacing:-2 color:#F5F7FA`）/ L5 下線＋サブ（Oswald `fontSize:38 letterSpacing:6 uppercase color:#C8CDD6`）/ L6 ロゴ（`linear-gradient(135deg, ${accent}, #ffffff22)`・`border:2px solid ${accent}`）。

## 11.4 確認方法（CLAUDE.md §5）

```bash
cd C:\Users\aab15\Documents\prime-documentary\remotion
npm run studio     # = remotion studio。OpeningCaniglia を 0→180f でスクラブし §11.1 の各時刻を目視
npx remotion render OpeningCaniglia out/caniglia_opening.mp4 --props=./props/caniglia.json
# props 差し替え量産
npx remotion render OpeningCaniglia out/caniglia_short_op.mp4 --props=./props/caniglia_short.json
# 本編
npx remotion render Ep43Caniglia out/caniglia_final.mp4 --props=./src/data/caniglia_film.json --public-dir=public_slim --concurrency=4
```

---

# 12. props 定義と型（CLAUDE.md §4）

```ts
export type OpeningCanigliaProps = {
  title: string;      // 主役タイトル。1文字ずつスタッガーで切れ上がる
  subtitle: string;   // サブタイトル。UPPERCASE 表示（facts_lock 検査対象）
  accent: string;     // アクセント（HEX6桁・"#"込み）。グリッド/敷居の光/グロー/下線/ロゴに波及
  hasLogo: boolean;   // true で左上にロゴバッジ
};
```
**EP43 の確定 props（`remotion/props/caniglia.json`）:**
```json
{ "title": "THE WELFARE CHECK", "subtitle": "CANIGLIA V. STROM", "accent": "#E0913C", "hasLogo": true }
```
**量産用 `remotion/props/caniglia_short.json`:**
```json
{ "title": "THE WELFARE CHECK", "subtitle": "CAN THEY ENTER TO HELP?", "accent": "#E0913C", "hasLogo": false }
```
> `accent` は **`#E0913C` 固定**（EP42 warrant-blue の流用は BLOCKER）。`subtitle`/`title` は `facts_lock` 検査対象（「police cannot enter your home」無留保・「full victory」を出さない。`CANIGLIA V. STROM`・疑問形 `CAN THEY ENTER TO HELP?` は制度説明として可・C1）。

---

# 13. 受入基準（EP43 の Definition of Done・★語数ゲートが最初・全編アイボール必須）

```bash
cd C:\Users\aab15\Documents\prime-documentary
# 0. 語数（最優先・課金前）
./.venv/Scripts/python.exe scripts/check_script_length.py episodes/PD-2026-043-caniglia/03_script/script.en.v001.md --json
# 1. 事実性（EP43固有・§1.3・6制約）
./.venv/Scripts/python.exe scripts/check_caniglia_facts.py --json
# 2. ビート契約（AE↔figures 非重複）
./.venv/Scripts/python.exe scripts/validate_caniglia_beats.py
# 3. 密度（★31 を Remotion 側で満たしていること・--ep 指定／--json は出力パス）
./.venv/Scripts/python.exe scripts/check_motion_density.py --ep PD-2026-043-caniglia --json runs/qc/caniglia_motion.json
# 4. VO速度（ナレ直後・ミックス前）
./.venv/Scripts/python.exe scripts/measure_vo_wpm.py --ep caniglia --json
# 5. 最終受入
./.venv/Scripts/python.exe scripts/check_final_acceptance.py 43 --render episodes/PD-2026-043-caniglia/08_edit/caniglia_final_bgm.v002_ae.mp4 --emit-receipt
```
> **ゲート入力は `--ep PD-2026-043-caniglia`。`--json <film.json>` を入力に使わない**（出力パス＝上書き事故。ブリーフ§5）。

| ゲート | 閾値 | EP43 設計値 |
|---|---|---|
| `check_script_length` | band 内 | 2,141語（SPEC・要 PASS 確認） |
| `runtime_band` | 690–750s | **733.8s = 12:13.8**（上限 750s に 16.2s 余裕） |
| `motion_density` | ≥2.5/min ∧ cov ≥0.25 ∧ variety ≥3 | **3.08/min / 0.308 / 14種**（film.json 37 beats・AE非依存・floor 31 に +6） |
| `animation_mix`（紙芝居） | still-share ≤45% ∧ motion cov ≥45% | **44.69% / 55.31%** |
| `check_asset_reuse` | first-use ≥0.70・still≤2・factory1・motion≤2 | **0.8584 / 2 / 1 / 2** |
| `footage_diversity` | distinct/total ≥0.40 | **0.8584** |
| `visual_asset_qc` | 全 factory 目視 reviewed | **93本 目視（CODEX_A）** |
| `image_resolution` | 長辺≥3840 | 全 SDXL ≥3840 |
| `bgm_present` | 無音>25秒ゼロ | 最長 2.2秒 |
| `caption_integrity` | 一致≥99%・カバー≥95% | §8.2 |
| `op_ed_bookends` | `BrandOpening`/`BrandEndcard` import・不変 | ✓ |
| `asset_manifest` | A↔B counts/role 一字一致・also_thumb 6（S01/S24/S28/S30/S49/S81）・overlay 12 | §5.8 |
| `facts_lock`（EP43固有・6制約） | violations=0 | §1.2/§1.3 |
| **全編アイボール** | 12:13.8 を通しで目視 | ★1フレーム判定禁止（EP39-41 の miss） |

---

# 14. premortem（失敗するとしたらここ）

| # | 失敗モード | 事前対処 |
|---|---|---|
| 1 | **番号ズレ**（別番号を発明） | シーンは S01..S48 固定（§3.2）。プロンプトも S01..S48 の Sid のみ |
| 2 | **紙芝居**（still-share 45%超・余裕 0.31%pt） | §5.1 で still-cut 101 固定・factory 93・i2v 32。still1つ増で 45% 割れ → cut を増やさず同一シーンの新規 distinct で回復 |
| 3 | **バリエーション水増し**（`--variants 3` を書く） | §5.3。variants 指定なし＝1枚。ai_prompts は 85行＝85枚 |
| 4 | **密度 FAIL**（AEカードに頼る） | §7。film.json に 37 beats（31 超）。AE 8枠は composite 後で非カウント |
| 5 | **画像プロンプトが読めない**（0枚生成） | §9.1 の2行形式・`--only S01` で `shots=101`（body 85 + i2v種 16）確認 |
| 6 | **ファイル名信仰**（牛が本編に入る） | §5.4 factory 93本を `build_footage_contact_sheet.py` で全点目視（CODEX_A BLOCKING） |
| 7 | **6制約違反**（令状なし断定/全面勝訴/Cady=家/Caniglia肖像/扇情/988画面扇情） | §1.2/§1.3 `check_caniglia_facts.py`。カード・figures・字幕・プロンプト全対象 |
| 8 | **FigureBeats kind 大文字で無音描画 / `comparebars` 非実在** | §7.2 kind は全小文字（`compbars`・`comparebars` は存在しない） |
| 9 | **AE em-dash 豆腐 / 等速 / OM名英語 / 文字切れ** | §6.6。テキスト幅は `sourceRectAtTime(t,false).width` 実測 |
| 10 | **id 誤り**（切り詰め・綴り違い等） | §0.1。`id="Ep43Caniglia"`・`caseFilmDurationInFrames(canigliaFilm,30)`=22014 |
| 11 | **accent 流用**（EP42 warrant-blue を残す） | §0.5/§12。OP props/AEカード/サムネ accent は `#E0913C` |
| 12 | **A↔B マニフェスト不整合**（role=thumb を作る/counts 不一致） | §5.8。`stills[].role` enum=`body/i2v_source/reject`・also_thumb 6（S01/S24/S28/S30/S49/S81）・overlay 12 を A/B 一字一致 |
| 13 | **EP39/40/41/42 と素材被り** | §2 で4つの stock_ledger の sha256 を除外 |
| 14 | **fast端で 11分台 / 750s 超** | §4.1 speed 1.0 明示＋`measure_vo_wpm` 168–190・190超は破棄再発注。総尺 733.8s ≤750 の assert（§3.1[4]） |

---

# 15. 設計パッケージ接続（DESIGN → CODEX_A / CODEX_B）

- **DESIGN（本書）:** タイムライン（0〜721.3s 全区間・各Act）・レイヤー（背面4層）・モーション数値・48絵コンテ・FigureBeats 設計（≥31・小文字kind・変種≥3）・AEカード表（accent #E0913C）・OP 仕様・asset_manifest スキーマの正（§5.8）。
- **CODEX_A（別ファイル `EP43_caniglia_CODEX_A_ASSETS.v001.md`）:** §9 を **85本の固有プロンプト**（1シーン1枚・variants 0）＋ i2v 16 ＋ factory 93 選定＆**全点目視QC**（`select_caniglia_factory.py`・`--exclude-used` で EP39/40/41/42 sha256 除外）＋境界契約 `asset_manifest.v001.json`（EP42同型・counts を EP43 値 still_body85/still_i2v_source16/factory93/motion16・`stills[].role` enum=`body/i2v_source/reject`・also_thumb 6（S01/S24/S28/S30/S49/S81）・overlay 12）。
- **CODEX_B（別ファイル `EP43_caniglia_CODEX_B_BUILD.v001.md`）:** `build_caniglia_film.py`（＝`build_young_film.py` を複製・ASSET_MAP/NARR/FACTORY_SEL/SLUG/EP を caniglia に）／captions（実測 narration）／figures 34＋graphics 3（小文字 kind・§7）／`CaseFilm` を `id="Ep43Caniglia"` で Root.tsx 登録（`caseFilmDurationInFrames`＝22014）／`OpeningCaniglia`／AEビルダ・コンポジタ（accent #E0913C・.aep>.jsx assert・レイアウト名は実装済み8種のみ）・`validate_caniglia_beats.py`・`check_caniglia_facts.py`（EP42 版を複製・同名）／`build_caniglia_bgm.py`→`composite_caniglia_hero.py`／レンダ（`--public-dir=public_slim --concurrency=4`）／全ゲート（`--ep PD-2026-043-caniglia`）／完成後の全編アイボール。
- **A↔B 接続点は `asset_manifest.v001.json` ただ1ファイル**（EP42 同型・counts/role enum を A/B 一字一致・§5.8）。
- **複製元（実在・EP42）→ caniglia 複製先:** `build_young_film.py`→`build_caniglia_film.py` / `build_young_bgm.py`→`build_caniglia_bgm.py` / `ae/build_young_hero_jsx.py`→`ae/build_caniglia_hero_jsx.py` / `ae/composite_young_hero.py`→`ae/composite_caniglia_hero.py` / `validate_young_beats.py`→`validate_caniglia_beats.py` / `check_young_facts.py`→`check_caniglia_facts.py`。**共有（複製不要）:** `generate_sdxl_4k.py` / `build_footage_contact_sheet.py` / `check_motion_density.py` / `measure_vo_wpm.py` / `check_script_length.py` / `check_final_acceptance.py`。**実在しないスクリプトを捏造しない。**
