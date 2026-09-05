# EP44 — "The Words They Never Read You" — 制作設計書（DESIGN 本体・v001・確定台本版）

- Episode ID: `PD-2026-044-tekoh` / slug: `tekoh` / EP44
- 中心の問い（英語・二人称・★射程を過大化しない）: **"If an officer never reads you your rights, can you make that officer answer for it, by himself, in a civil suit for money?"**
- 判例（制度説明としてのみ）: **Vega v. Tekoh (2022), No. 21-499**（**6–3**・Alito 法廷意見／Kagan 反対＋Breyer・Sotomayor 同調・SCOTUS が第9巡回区を破棄）
- 主役: **Terence Tekoh**（存命の私人＝**R2**）／**Carlos Vega**（存命の私人＝**R2**）。象徴のみ・尊厳の物語。**顔・肖像・身体を一切描かない。**
- リスク区分: **R2**（Tekoh・Vega ともに存命私人）。判事（Alito / Kagan / Breyer / Sotomayor / Roberts / Thomas / Gorsuch / Kavanaugh / Barrett）も人物化しない。全実在人物の顔・身体・肖像を描かない。
- Status: **BINDING**。**唯一の真実 = 機械生成済み `EP44_tekoh_PRODUCTION_SPEC.v001.json`**。本書のあらゆる数値はそこからの転記で、手書きで発明していない。衝突したら SPEC が勝つ。
- このファイルは**設計パッケージ3分割**（DESIGN / CODEX_A / CODEX_B）の **DESIGN 本体**。共有ブリーフ `EP44_tekoh_DESIGN_BRIEF.shared.md` を単一の真実源とする。85本の SDXL プロンプト実体・i2v 16・factory 93 選定は **CODEX_A**（`EP44_tekoh_CODEX_A_ASSETS.v001.md`・FROZEN）、`build_tekoh_film.py`・captions・figures 実装・Root.tsx 登録・AEビルダ/コンポジタ・ゲートは **CODEX_B** に属す（本書は各所でポインタのみ示す）。EP43 caniglia の DESIGN 構造を踏襲し、内容を EP44 に差し替えた。

## ★このエピソードの唯一の真実（手書きで数値を発明するな）

`episodes/_planning/EP44_tekoh_PRODUCTION_SPEC.v001.json`（台本から機械生成・`scripts/build_production_spec.py`）。本設計書は SPEC を**人間可読な実装指示に翻訳しただけ**で、新しい数字を作っていない。

```
words_total          = 2,139
narration_seconds    = 720.6   （= 12.0分・[SILENCE 1..6] の実音無音を含む）@ wpm_used 178.1
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

- Codex の画像生成は高精度。**同一ショットの複数バリエーション（`_01/_02/_03`）を作らない。**
- `04_scenes/ai_prompts.v001.md` は **still 85本＝85行の固有プロンプト**（`generate_sdxl_4k.py` の `read_prompts()` 2行形式・各1枚）。**`--variants 3` は使わない**（`--variants 1` または variants 指定なし）。
- i2v モーション種は **16枚**（各1シード・これもバリエーション0）。
- 総生成画像 = **still 85 + motion seed 16 = 101枚（各1回）**。**factory 93 は生成ではなく在庫選抜**（全点目視QC・EP39/40/41/42/43 と sha256 被りゼロ）。
- **still を増やして factory を削るな**（still-share 0.4469 は cap 0.45 に対し余裕 0.31%pt しかない）。

## ★EP39/40/41/42/43 で踏んだ失敗＝本書が最初から潰す設計判断

| # | 失敗 | 本書での恒久対策 | 参照 |
|---|---|---|---|
| 1 | **番号ズレ**（別リストを発明） | シーンは **SPEC の S01..S48 に固定**。別番号体系を作らない | §3.2 |
| 2 | **紙芝居**（still 100% で animation_mix FAIL） | still-cut **101 固定**＋factory実写 **93**＋i2v **32**。still-share 44.69% ≤45% / motion cov 55.31% ≥45% を構造保証 | §5.1 |
| 3 | **バリエーション水増し** | **1シーン1枚・85本を各1枚**。variants 禁止 | §5・§9 |
| 4 | **画像プロンプトのパーサ非互換** | `read_prompts()` の**2行形式**。CODEX_A が `--only S01` で拾い数（101）を確認 | §9 |
| 5 | **ファイル名を信じた**（牛が documents、大聖堂が監視カメラ） | factory 93本を `build_footage_contact_sheet.py` で**全点目視QC**（CODEX_A 必須・BLOCKING） | §5.4 |
| 6 | **AEカードを密度に数えた** | `check_motion_density` は film.json の `figures+graphics` だけ。**film.json 側に MGビート 31本以上**（本書は 37 設計）。AE は composite 後で 0 カウント | §6.1 / §7 |
| 7 | **一枚絵で完成判定**（EP39-41/EP39-41 の眼球不足） | 全編アイボール必須（§13）。measured > estimated | §13 |
| 8 | **A↔B マニフェスト不整合** | asset_manifest は **A↔B で同一スキーマ・counts/role enum を一字一致**。role=`thumb`/`still_thumb` を作らない。サムネは `also_thumb=true` の body still 6枚 | §5.8 |
| 9 | **dochighlight で「バグに見える」黒バー**（EP40/41/42 で3回指摘） | **figures[] に `kind:"dochighlight"` を一切入れない**（grep で0確認）。redacted が要れば "REDACTED" を焼いた実 still を使う | §7.2 |

---

# 0. 環境・Remotion設定（CLAUDE.md §0 準拠）

## 0.1 本編 `Ep44Tekoh` の Composition 設定（★本編の正・誤記注意）

| 項目 | 値 |
|---|---|
| `id` | **`Ep44Tekoh`**（Root.tsx に `CaseFilm` で登録。ブリーフ§5「Ep44Tekoh登録」。**id の切り詰め・綴り違い・大文字化は誤記＝BLOCKER**） |
| 解像度 | **1920 × 1080** |
| `fps` | **30**（EP42 young / EP43 caniglia の CaseFilm と同値を踏襲。フレームは全て `Math.round(30 × 秒)`・直書き禁止） |
| `durationInFrames` | **`caseFilmDurationInFrames(tekohFilm, 30)` = 21993**（4項の実関数 `round(hookSeconds×30)+round(OPENING_SEC×30)+ceil(narrationSeconds×30)+round(ENDCARD_SEC×30)`・**hookSeconds=0**・§3.1[3] で算出。手書きで数値を入れず関数で算出する） |
| component | `remotion/src/compositions/CaseFilm.tsx`（既存の汎用 `CaseFilm` を再利用。`Bookends.tsx` の `BrandOpening`/`BrandEndcard` を **import**・fork 禁止） |
| data | `remotion/src/data/tekoh_film.json`（`scripts/build_tekoh_film.py` で再生成できる状態を保つ＝**git 未追跡**） |

**Root.tsx 登録（★ブリーフ§5・CODEX_B が実装）:**
```tsx
import {tekohFilm} from './data/tekoh_film.json';
import {caseFilmDurationInFrames} from './lib/caseFilmDuration';
// ...
<Composition
  id="Ep44Tekoh"
  component={CaseFilm}
  width={1920} height={1080} fps={30}
  durationInFrames={caseFilmDurationInFrames(tekohFilm, 30)}  // = 21993
  defaultProps={{film: tekohFilm}}
/>
```
> **id は `Ep44Tekoh`**（切り詰め・綴り違い・先頭以外の大文字化などは全て誤記。ブリーフ§5 の render 行 `Ep44Tekoh` が正）。

## 0.2 タイトルバンパー `OpeningTekoh` の Composition 設定（CLAUDE.md 正典部品準拠）

| 項目 | 値 |
|---|---|
| `id` | **`OpeningTekoh`** |
| 解像度 | **1920 × 1080** |
| `fps` | **60**（CLAUDE.md §0 の正典値。OP 単体は 60fps） |
| `durationInFrames` | **180**（= 3.0秒 @ 60fps） |
| component | `remotion/src/compositions/OpeningTekoh.tsx`（§11 全仕様） |

> `OpeningTekoh` は**独立したタイトルバンパー成果物**（`out/tekoh_opening.mp4`）。本編内 OP/ED の正典は `Bookends.tsx`（`BrandOpening` 3.50s / `BrandEndcard` 9.00s・不変）。`OpeningTekoh` を本編に ffmpeg で焼き込まない（オーナー承認なしに見え方を変えない）。

## 0.3 必要な依存パッケージ

```bash
cd C:\Users\aab15\Documents\prime-documentary\remotion
npm i @remotion/motion-blur     # CLAUDE.md 必須依存（Trail によるモーションブラー）
```

## 0.4 `remotion.config.ts`（CLAUDE.md §0 正典値・EP41/42/43 と同一）

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

`brand.ts` 実値: ink `#0A0A0C` / navy `#0B1A2B` / electric `#1F6BFF` / silver `#C8CDD6` / white `#F5F7FA`。フォント: display Oswald / number Anton / body Oswald。

**EP44 のパレット（★ダーク/シネマ・冷たいティール病院の夜＋法廷大理石・レーン分離・唯一の暖色＝ランプ下のペンと書面）:**
```
INK    = #0A0A0C   ルート背景
CLINIC = #0C1514   病院の夜（冷たいティール緑の near-black・ACT1 の内側）
MARBLE = #3A3B40   最高裁の冷たい大理石（ACT3）
STEEL  = #26282C   ウォッシュ/ビネット寄り（institutional）
ACCENT = #2FA6A0   ★interrogation-teal（取調のティール＝この事件の色）。ブランド数値・ライン・下線・グロー・OP/AE/サムネ accent。★EP41 gold #E5B53A / EP42 blue #3B7DD8 / EP43 amber #E0913C を流用しない
LAMP   = #E4B87A   ★予備：机上ランプの暖色（ペンと署名欄に落ちる唯一の実用暖色・S02/S03/S15 のグローのみ）。数値・下線には使わない
WHITE  = #F5F7FA
SILVER = #C8CDD6
```
> **レーン分離:** EP39（electric・取調室）/EP40（gold amber・郊外昼光）/EP41（gold・鋼灰institutional）/EP42（warrant-blue・夜のシカゴ）/EP43（porch-amber・RI の一軒家）と被らないよう、EP44 は **冷たいティール緑の病院の夜 `#0C1514` ＋ 冷たい大理石 `#3A3B40` を基調＋唯一の暖色 = ランプ下のペンと署名欄（interrogation-teal `#2FA6A0` がアクセント）**。接尾に `electric blue interrogation` `midday suburban` `steel grey death row` `warrant-blue` `porch-amber` を含めない。**factory は EP39/40/41/42/43 の `stock_ledger*.json` の sha256 を除外**（CODEX_A・BLOCKING）。**CODEX_B は OP props / AEカード / サムネ accent を必ず `#2FA6A0` にする（他話の色の流用は BLOCKER）。**

---

# 1. 事実の取り扱い（★正確性6制約＝FACTS LOCK / `check_tekoh_facts.py`・BLOCKING）

## 1.1 確定台本（唯一の正・1バイトも変えない）

```
C:\Users\aab15\Documents\prime-documentary\episodes\_planning\EP44_tekoh_script.en.v001.md
```
**本番配置先:** `episodes/PD-2026-044-tekoh/03_script/script.en.v001.md`（上記を1バイトも変えずコピー）。整形も禁止（AI臭再発と語数ゲート再計算を招く）。台本の幕構成（HOOK / OP / ACT1–3 / ACT3 payoff / ENDING）と `[SILENCE 1..6]`（**6箇所・最低5**）を正典とする。存在しない演出マーカーを発明しない。**★構造ロック（台本 CRITIQUE-REV2）:** 得票 6-3 は ACT3 まで伏せる（HOOK/OPENING/最初の30秒に出さない）。尺の figure（"twelve minutes"）を音声に出さない。ロードマップ段落を作らない。

## 1.2 ★正確性6制約（全出力＝プロンプト・カード文言・図表・字幕・タイトルに適用。1つでも違反＝BLOCKER）

| # | 制約 | 出力での順守 |
|---|---|---|
| **C1** | **射程を過大化しない** | 否定されたのは「ミランダ違反“単体”を理由に §1983 で警官を民事で訴え金銭賠償を取る」道だけ。ミランダ自体は刑事公判で有効（未告知供述は排除されうる）。**タイトル/サムネ/カード/字幕/プロンプトに「Miranda is dead / no right to remain silent / police need not read rights / 警察は権利を読まなくてよい」を一切書かない**（EP14 Lange型事故）。閉じたのは「賠償の第2の扉」だけ＝「排除の扉」は開いたまま、を象徴で必ず併存（閉じた扉＋開いた扉） |
| **C2** | **6–3 ＝ 分かれた判断** | Alito 法廷意見（多数6）／Kagan 反対（＋Breyer・Sotomayor＝反対3）。**`9-0`/`9 to 0`/`unanimous`/`nine to nothing` を Vega の判決に対して書かない**。多数/反対を中立帰属。6-3 は ACT3 まで画面にもカードにも出さない |
| **C3** | **Miranda(1966)/Dickerson(2000) と Vega を混同しない** | Vega はミランダを覆していない＝§1983救済のみ否定。**`overturned Miranda`/`Miranda overruled/reversed/struck down/killed` を書かない**。Miranda/Dickerson は「無傷で立つ書物」。カードは "MIRANDA STANDS / DICKERSON STANDS" で存続を明示 |
| **C4** | **§1983 の意味を正確に** | 州の役人を憲法違反で民事提訴する連邦法。「刑事免責」と混同しない。**§1983一般論で `no immunity` と断定しない**（qualified immunity がある）。§1983 は「責任を問うための扉」の象徴で示す |
| **C5** | **★広告適合性（最重要級・ad-suitability lock）** | Tekoh の**原被疑事実（疑われた罪の性質・その内容・被害）を一切名指しせず・描写も表示もしない**。タイトル/サムネ/カード/プロンプト/タグ/注記/字幕/概要欄のどこにも罪状の性質・`victim`・`guilty` を出さない。原告は「疑われ、無罪となった私人」として尊厳をもって（象徴：病院の廊下・机上のペンと書面・署名欄・空の取調台・空の陪審席） |
| **C6** | **Tekoh も Vega も存命の私人（R2）** | **顔・肖像・身体を描かない**。象徴のみ。個人として同定できる描写をしない。判事も人物化しない。人物は影/後ろ姿/手元/象徴に限定（原則「人を出さない」） |
| **R1** | **実在人物の顔・肖像を生成しない** | 全生成ビジュアル表示中は `AI-assisted visualization`（右下）常時表示。概要欄に1行 AI 開示 |

## 1.3 6制約ゲート `check_tekoh_facts.py`（`scripts/check_tekoh_facts.py`＝EP43 `check_caniglia_facts.py` を tekoh 用に複製。exit≠0 で出荷停止・CODEX_B 実装。出力 `facts_lock.v001.json`）

> **★ゲート名は1本に確定:** 6制約の機械ゲートは **`scripts/check_tekoh_facts.py`**（出力 `09_package/facts_lock.v001.json`）ただ1つ。**DESIGN / CODEX_A / CODEX_B で同名参照**（`*_accuracy`・`*_facts_check` 等の別名を作らない）。下表の **L-C1..L-C6・L-R1** は内部ルール **R-*** に一本化（対応: L-C1→R-SCOPE / L-C2→R-VOTE / L-C3→R-PRECEDENT / L-C4→R-1983 / L-C5→R-CHARGE / L-C6→R-FACE / L-R1→R-FACE）。

**検査対象:** `03_script/script.en.v001.md` / `remotion/src/data/tekoh_film.json` の `figures[].text`・`figures[].lines[]` / `08_edit/ae_hero/beats.json` の `top`/`bottom`/`main`/`quote`/`attribution`/`left`/`right`/`kicker`/`title`/`date`/`place` / `09_package/description.txt` / `remotion/props/tekoh*.json` の `subtitle`/`title` / `04_scenes/ai_prompts.v001.md`。

| ルール | 内容 |
|---|---|
| **L-C1 射程（R-SCOPE）** | 文字列 `miranda is dead`/`miranda (is )?(dead|abolished|overturned|gone|no longer)`/`no (more )?right to remain silent`/`police (need not|no longer (need|have) to|do ?n.?t (need|have) to) (read|give|recite|warn)`/`stop reading (anyone )?(their )?rights` 等の**無留保の断定**が出たら FAIL。`6-3`/`holding`/`ruling` を含む beat/figure/card に、限定語（`one door`/`exclusion (still\|survives)`/`miranda stands`/`only the (second\|civil)`）が同一デッキに無ければ FAIL。**許容:** `one door closed while exclusion stays open` / `Miranda stands` / `a fence, not the ground` は射程を正しく限定するので合格 |
| **L-C2 得票（R-VOTE）** | `9-0`/`9 to 0`/`nine to (zero\|nothing)`/`unanimous` が Vega 判決に対して出たら FAIL。`6-3`/`6 to 3` を含むカードに `majority`/`dissent`/`alito`/`kagan` の中立帰属が近傍60字に無ければ FAIL。得票文字列が HOOK/OPENING 幕（ACT3 前）に出たら FAIL（構造ロック） |
| **L-C3 判例（R-PRECEDENT）** | `(overturn\|overrule\|reverse\|struck down\|kill\|end) (ed )?miranda`/`miranda (was )?(overturned\|overruled\|struck down\|killed)` が出たら FAIL。`Vega` の近傍60字に `overturned`/`killed`/`ended` が `Miranda`/`Dickerson` を目的語として出たら FAIL。`Dickerson` は「存続する2000年判決」文脈のみ |
| **L-C4 §1983（R-1983）** | `no immunity` の無留保断定が出たら FAIL（qualified immunity の存在）。`Section 1983`/`§ ?1983`/`1983` の近傍に `criminal immunity`/`criminal charge against the officer` の混同が出たら FAIL（§1983 は民事） |
| **L-C5 ★原被疑事実（R-CHARGE・最重要）** | **原被疑事実の性質を示す語が全出力に1件でも出たら FAIL。** 禁止語群（例）: `sexual assault`/`sex crime`/`sex offen`/`rape`/`molest`/`assault victim`/`the victim`/`guilty of`/`actually guilty`/`he did it`/`the crime he committed`/`convicted of` ＋ 罪状カテゴリ名一般。`Tekoh`/`accused`/`charged` の近傍に罪状の性質語が出たら FAIL。**原告は「a private person who was accused and cleared」以外に性質を与えない** |
| **L-C6 肖像（R-FACE）** | `ai_prompts.v001.md` の正プロンプトに `portrait`/`face of`/`likeness`/`recognizable (real )?person`/`identifiable face`/`Terence Tekoh`（人物として）/`Carlos Vega`（人物として）/`nude`/`his body`/`mugshot`/`deepfake` が出たら FAIL（ネガティブでの使用は可）。`Tekoh`/`Vega` の直後60字に `face`/`portrait`/`depicted as a man` が出たら FAIL。判事名（Alito/Kagan/Breyer/Sotomayor/Roberts/Thomas/Gorsuch/Kavanaugh/Barrett）の `face of`/`portrait of` が出たら FAIL |

**出力:** `09_package/facts_lock.v001.json`（`{"pass":bool,"violations":[{"file","rule","line","excerpt"}],"skipped":[...]}`）。`pass:true` でない限り `check_final_acceptance.py` に進まない。

## 1.4 画面に出してよい確定数値（★台本／事実対応表 C01–C24 に存在するものだけ。この表以外を画面に出すな）

> **★台本ロック:** 判例番号（No. 21-499 / 384 U.S. 436 (1966) / 42 U.S.C. § 1983 / Dickerson (2000)）は**画像に描かない・音声で読み上げない**＝AE date/lowerthird のタイポで出す（CODEX_A §1.1 R1・制約2）。ナレは名前と年のみ、docket 文字列を言わない。

| ID | 値 | 台本での表現（claim） | 使用先 |
|---|---|---|---|
| N01 | **2022 · SUPREME COURT** / No. 21-499（June 23, 2022） | ACT3「when the case reached the Supreme Court」/ ENDING「After the summer of 2022」（C01） | AE **d01**（DATE_STAMP・docket は lowerthird）/ figures timeline |
| N02 | **6 / 3** | ACT3「Writing for six of the nine justices」＋「Three justices refused」（C02・**ACT3 まで伏せる**） | AE **v01**（VOTE_SPLIT・"ONE DOOR CLOSED" 枠）/ figures **votetally** |
| N03 | **SECTION 1983** / 42 U.S.C. § 1983 | ACT2「a federal law … known … by nothing more than its number」（C08） | AE **s01**（CENTER_STACK）/ figures **stat**・lowerthird |
| N04 | **MIRANDA v. ARIZONA · 1966** / 384 U.S. 436 (1966) | ACT3「In 1966, in Miranda versus Arizona」（C22） | AE **c01**（SPLIT_COMPARE 左）/ figures lowerthird・stat |
| N05 | **DICKERSON · 2000** | ACT3「In the year 2000, in a ruling called Dickerson」（C23） | AE **c01**（SPLIT_COMPARE 右）/ figures lowerthird・stat |
| N06 | **TWO TRIALS** | ACT2「Twice, federal juries heard his civil case, and twice they sided with the deputy」（C16） | AE **t01**（CENTER_STACK）/ figures **numberticker**・stat |
| N07 | **THREE JUSTICES**（反対） | ACT3「Three justices refused … Kagan, joined by Breyer and Sotomayor」（C04・中立帰属） | figures **numberticker**・stat |
| N08 | **SIX JUSTICES**（多数） | ACT3「Writing for six of the nine justices, Justice Samuel Alito」（C03・中立帰属） | figures stat（votetally と同区間にしない） |
| N09 | **ACQUITTED** | ACT2「They acquitted him … not guilty」（C14） | AE **a01**（CENTER_STACK）/ figures **stat** |
| N10 | **2014** | ACT1「In 2014, inside a medical center in Los Angeles」（C11/C13） | figures timeline・lowerthird |
| N11 | **NINTH CIRCUIT** / court of appeals | ACT2「A federal court of appeals … could support a lawsuit under Section 1983」（C17） | figures lowerthird・timeline |
| N12 | **"...strips … the ability to seek a remedy…"** | Kagan 反対の逐語（C20/C21・中立帰属） | AE **q02**（QUOTE_CARD・Kagan 帰属）/ figures **quote** |
| N13 | **"a fence, not the ground it stands on"** | Alito 法廷意見の prophylactic 比喩（C06・"A fence. Not the ground it stands on."） | AE **q01**（QUOTE_CARD・多数帰属）/ figures **quote** |

> **★AE カード文言に「Miranda is dead」「9-0」「no immunity」「原被疑事実」を書かない。** 数値・引用は AE ledger（§6.4 の `beats.json`）と figures（§7）で一致必須。**判例番号（No. 21-499 / 384 U.S. 436 / § 1983 / Dickerson 2000）は figures lowerthird ＋ description に退避**（本文で読み上げない・台本の音声からは抜いてある）。

---

# 2. 視覚・音響レーン分離（EP39/40/41/42/43 との素材被り回避）

> **EP39/40/41/42/43 のファイルには一切触れない（読み取りのみ可）。** レーンを機械的に分離する。

| 軸 | EP43 caniglia | **EP44 tekoh** |
|---|---|---|
| 舞台 | 夜の Cranston の家→朝のポーチ・救急車→最高裁大理石→夜明けの戸 | **夜の LA の病院の廊下（机上のペンと署名欄）→ 空の取調台 → 法廷・空の陪審席・証拠になった書面 → 最高裁の列柱・9席（6/3の影）・守りの柵→ あなたの椅子・閉じた扉と開いた扉** |
| 時間帯 | 夜→朝日→大理石冷光→夜明け暖色 | **病院の夜（冷たいティール緑）→ 冷たい法廷光 → 大理石の冷光（判例核）→ 夜明けの一室（開いた/閉じた扉）** |
| 支配的出来事 | 安否確認→無令状立ち入り・押収・判例核（9-0/温存例外）・vacate&remand | **警告なしの録取→無罪→民事提訴→§1983→二度の敗訴→第9巡回区→SCOTUS→6-3・prophylactic 柵・Kagan 反対・"賠償の扉"だけ閉鎖** |
| アクセント色 | porch-amber `#E0913C` | **interrogation-teal `#2FA6A0`（取調のティール）** |
| ベース色 | 暖い near-black `#14110E` + 大理石 `#3A3B40` | **冷たいティール緑 `#0C1514` + 冷たい大理石 `#3A3B40` + near-black `#0A0A0C`** |
| レンズ感 | HOOK 象徴モンタージュ／ACT1 抑制／ACT3 正対荘厳／ENDING 引き | **HOOK 象徴モンタージュ（ペン・署名欄）／ACT1 最短・現在形・病院廊下／ACT2 正対の転回／ACT3 正対対称・最も遅く荘厳／ENDING 引き（あなたの椅子・救済なしの余韻）** |
| 画像保存先 | `H:\pd-media\assets\ai\caniglia\` | **`H:\pd-media\assets\ai\tekoh\`** |
| Remotion データ | `caniglia_film.json` | **`tekoh_film.json`** |
| Remotion コンポ | `Ep43Caniglia` | **`Ep44Tekoh`** |
| AE 作業ディレクトリ | `…/PD-2026-043-caniglia/08_edit/ae_hero/` | **`…/PD-2026-044-tekoh/08_edit/ae_hero/`** |

**素材被り禁止:** EP39/40/41/42/43 と同一の factory clip / AI画像を1点も使わない。選定前に `episodes/PD-2026-039-*/` `…-040-*/` `…-041-*/` `…-042-*/` `…-043-*/` の `05_stock/stock_ledger*.json` を読み sha256 重複を除外（CODEX_A・BLOCKING）。

---

# 3. 尺と構成 — SPEC の値をそのまま使う

## 3.1 全区間タイムライン（★この表が唯一の正・秒は fps=30 から算出しフレーム直書き禁止・0〜720.6s 全区間）

**算出基準:** SPEC の `narration_seconds = 720.6`（マスター）を `tekoh_film.json` の `narrationSeconds` に入れる。**手計算で上書きしない。** 幕秒は SPEC の `acts[].seconds` をそのまま使う（台本語数シェアから機械生成済み）。フレーム = `Math.round(30 × 秒)`。**台本の順序上、`BrandOpening` は HOOK ナレの後に解決**（frame zero ではない）。

| # | ブロック | 役割 | 語数 | 幕秒（SPEC） | 台本の沈黙 | 固定尺 | 開始f | 終了f |
|---|---|---|---|---|---|---|---|---|
| 1 | **HOOK** | `hook` | 98 | 33.0 | **SILENCE 1 = 2.0**（ペン上・署名欄で保持） | — | 0 | 990 |
| 2 | **BrandOpening** | `opening` | 0 | — | — | **3.50** | 990 | 1095 |
| 3 | **OPENING** ナレ | `opening` | 137 | 46.2 | **SILENCE 2 = 1.5**（黒・署名の一線） | — | 1095 | 2481 |
| 4 | **ACT1** That night | `body` | 230 | 77.5 | **SILENCE 3 = 2.0**（完成した書面上のペン） | — | 2481 | 4806 |
| 5 | **ACT2** The turn | `body` | 448 | 150.9 | **SILENCE 4 = 2.0**（空の陪審席） | — | 4806 | 9333 |
| 6 | **ACT3** The doctrine | `body` | 631 | 212.6 | **SILENCE 5 = 2.0**（空のベンチ・列柱の光） | — | 9333 | 15711 |
| 7 | **ACT3 payoff** the line-drawing | `body` | 222 | 74.8 | — | — | 15711 | 17955 |
| 8 | **ENDING**（payoff→CTA） | `ending` | 330 | 111.2 | **SILENCE 6 = 1.5**（署名だけが残る書面） | — | 17955 | 21291 |
| 9 | **BrandEndcard** | `ending` | 0 | — | — | **9.00** | 21291 | 21561 |

> **フレーム列**は BrandOpening(105f)/BrandEndcard(270f) を実尺で挟み、幕秒を順に `round(30×秒)` で積んだ実装用アンカー。発話幕秒合計 = 33.0+46.2+77.5+150.9+212.6+74.8+111.2 = **706.2s**。SPEC マスター **720.6s** との差 **14.4s（=432f）** は、幕間の息継ぎ＋設計無音6点（2.0+1.5+2.0+2.0+2.0+1.5 = **11.0s**）を内包した測定マスター。film.json には **720.6** を入れる。**BrandEndcard 終端の nominal 21561 と §3.1[3] の `caseFilmDurationInFrames` 出力 21993 の差 432f はこの 14.4s に一致**。CODEX_B は `tekoh_film.json` の segment 順から再計算し一致を確認。

### 検算（CODEX_B は必ず自分で再計算して一致を確認）

```
[1] narrationSeconds = 720.6（SPEC マスター。手計算で上書きしない）
    ※ 発話ブロック HOOK..ENDING の幕秒合計 = 706.2s。SPEC マスター 720.6 との差 14.4s は、
      幕間の息継ぎ＋設計無音6点（11.0s）を内包した測定マスター。film.json には 720.6 を入れる。
    ※ mean_shot 検算: 720.6 / 226 = 3.188s ＝ SPEC mean_shot_seconds 3.19 一致（226カットは 720.6s 全域に張る）。

[2] 総尺 = hookSeconds 0 + BrandOpening(OPENING_SEC) 3.50 + narrationSeconds 720.6 + BrandEndcard(ENDCARD_SEC) 9.00
        = 733.1 秒 = 12:13.1
    ※ hookSeconds=0（HOOK ナレは narrationSeconds 720.6 に内包・別建ての hook teaser preroll は作らない）。
       台本 OPENING は「BrandOpening は hook の後・frame zero でない」＝HOOK ナレ→BrandOpening→OPENING ナレ の順。

[3] caseFilmDurationInFrames(tekohFilm, 30) = 4項の実関数で算出（round(30×733.1) という単項近似ではない）:
      = round(hookSeconds×30) + round(OPENING_SEC×30) + ceil(narrationSeconds×30) + round(ENDCARD_SEC×30)
      = round(0×30)=0 + round(3.5×30)=105 + ceil(720.6×30)=ceil(21618.0)=21618 + round(9.0×30)=270
      = 21,993 フレーム
    ※ CODEX_B は tekoh_film.json の hookSeconds/narrationSeconds（＋Bookends の OPENING_SEC/ENDCARD_SEC）から
      同関数で再計算し 21993 に一致することを assert する（§5.1・§3.1 検算）。

[4] runtime_band ≤ 750s の assert（BLOCKING）:
    総尺 = hookSeconds 0 + 733.1 = 733.1s = 12:13.1 は band 690–750（11.5–12.5分）の内側（上限 750s に 16.9s の余裕）  ✓ PASS
    ※ hookSeconds を 0 超（teaser 採用）にする場合は round(hookSeconds×30) を [3] に加え、
      総尺 = 733.1 + hookSeconds を再検算して ≤ 750s を再確認すること（BLOCKING）。
```
> **VO 実測で確定:** `measure_vo_wpm`（合格帯 168–190 wpm）でナレ実測。実測が SPEC マスターと乖離したら CODEX_B は `narrationSeconds` を実測値で更新（planning は 720.6・final は実測が権威）。190超は破棄・speed 0.95 で再発注（BLOCKING）。

## 3.2 シーン→幕の割当（★SPEC の S01..S48 を固定・別番号を発明しない・48シーン）

各シーンは narrative beat。226カットを 48シーンに分散（平均 4.71カット/シーン）。`primary` は各シーンの主素材（still=SDXL 各1枚 / factory=実写 / motion=i2v）。ambient/繋ぎは factory を各シーンに撒く（§5.1）。**象徴のみ・6制約順守・Tekoh/Vega/判事 非人物化・原被疑事実の非描写。絵コンテ級の記述は §9。**

> **★2つの `Sxx` 名前空間は別物（取り違え禁止）:** 本節の **narrative シーンは `S01..S48`**（この表の絵コンテ）。一方 **still 資産 ID は `S01..S85`**（CODEX_A §2 注記・1プロンプト=1枚で48シーンに85枚を配分）。同じ `Sxx` 表記でも DESIGN §3.2/§9 の Sid（narrative）と CODEX_A/asset_manifest の scene_id・covers_scene_id（still 資産 ID）は指すものが異なる。横断参照時は「どちらの空間か」を明示し、cross-map しない。

| Sid | 幕 | 内容（象徴・6制約） | primary |
|---|---|---|---|
| S01 | HOOK | 夜の LA の病院の廊下・冷たいティール緑・無人（あの夜の始まった場所） | factory |
| S02 | HOOK | 机上の1本の万年筆と書面・暖色ランプ・下に署名欄（i2v: ランプの光が微かに揺れ、ペンが構えられる）＝すべての中心 | **motion** |
| S03 | HOOK | 署名欄への接写・警告カードは無い・ペンが構えられる（SILENCE 1 の画・保持） | still |
| S04 | HOOK | 空の取調台・紙とペン・録音機は無い（警告が来なかった部屋・hard cut で BrandOpening へ） | still |
| S05 | OP | 暗い中の署名を横切る一条の光（「あなたはこの言葉を知っていると思っている」・SILENCE 2） | still |
| S06 | OP | 最高裁の列柱・冷たい大理石・遠い（署名が運ばれた先の予兆・establishing） | factory |
| S07 | OP | 手前にランプ下の書面、奥に最高裁の列柱が faint＝署名から最高裁までの span | still |
| S08 | ACT1 | フックにかかる病院の職員証（無人・匿名・顔なし・名前なし）＝a hospital employee | still |
| S09 | ACT1 | 夜の病院の廊下・遠くに微かな動き（i2v: 通り過ぎて忘れられる場所） | **motion** |
| S10 | ACT1 | シフト終わりの静かな控室・空の椅子・上着（人物なし） | still |
| S11 | ACT1 | 質問の部屋・2脚の向かい合う椅子・冷たい光（無人・緊張） | still |
| S12 | ACT1 | 卓の中央の1枚の白紙とペン（部屋から出てくる紙）＝待つ | still |
| S13 | ACT1 | ランプ下の半ば埋まった手書きの録取ページ（i2v: 緩いプッシュ・判読不能・手なし） | **motion** |
| S14 | ACT1 | 録音機があるべき場所が空＝部屋から欠けていたもの（不在） | still |
| S15 | ACT1 | 署名欄の上に構えられたペン・警告カードは無い（署名の直前・手なし） | still |
| S16 | ACT1 | 内側から見た閉じた小部屋の扉・下に細い廊下の光（会話が起きた部屋） | still |
| S17 | ACT1 | ペンが横たわる完成した書面（i2v: 緩いプッシュ・SILENCE 3・部屋は静止） | **motion** |
| S18 | ACT1 | 質問の部屋のあと・卓に残された紙とペン（すべての後） | still |
| S19 | ACT1 | 病院の廊下（受け・無人・録取の残り） | factory |
| S20 | ACT2 | 透明な証拠スリーブに入り部屋から運び出される書面＝法廷へ旅する | still |
| S21 | ACT2 | 夜の無人の法廷内観・空のベンチと証言台（紙が運ばれた場所） | still |
| S22 | ACT2 | 証拠スタンプの押された書面（判読不能・i2v: 法廷の光が当たる）＝政府の立証に転じる | **motion** |
| S23 | ACT2 | 空の陪審席・12の空席（12人の見知らぬ人＝空の椅子） | still |
| S24 | ACT2 | 空の陪審席を静止で保持（SILENCE 4・評決前の沈黙） | still |
| S25 | ACT2 | 開いた法廷の扉・奥に淡い昼光・空の傍聴席＝無罪で去る（不在で示す・no guilty） | still |
| S26 | ACT2 | 光の帯の中で武器のように置かれた1枚の書面（i2v: 冷たい光・私人の手が証拠に） | **motion** |
| S27 | ACT2 | 民事裁判所の閉じた扉・冷たい石＝別種の訴え（民事） | still |
| S28 | ACT2 | 空の天秤と畳まれた書式＝刑務所でなく金銭で測られる請求（判読不能） | still |
| S29 | ACT2 | 暖色ランプ下の古い連邦法令の閉じた革表紙＝番号だけで知られる深い根の法（§1983・判読不能） | still |
| S30 | ACT2 | 冷たい大理石の壁の1つの扉が僅かに開く＝役人を責任に問う扉（象徴） | still |
| S31 | ACT2 | 二重に映る法廷ベンチと陪審席＝二度の裁判（一つの反復する無人室） | still |
| S32 | ACT2 | 破棄され脇に置かれた評決書・連邦控訴審の石のファサード＝差戻し→第9巡回区 | factory |
| S33 | ACT3 | 最高裁の列柱・正面・夜（事件が上げられ判断される・establishing） | factory |
| S34 | ACT3 | 冷たい大理石の1つの小さな鍵穴＝ほとんど技術的な一つの狭い問い | still |
| S35 | ACT3 | 大理石棚に無傷で立つ古い1966年の法書＝Miranda はまだ立つ（判読不能） | still |
| S36 | ACT3 | その隣に立つ2000年の静かな法書＝Dickerson・無傷（判読不能） | still |
| S37 | ACT3 | 大理石建築の下に現れる深い礎石＝掃き払えぬほど深く根ざした規則 | still |
| S38 | ACT3 | 一列に並ぶ3つの物＝規則・違反・救済の簡単な等式（算術のような主張） | still |
| S39 | ACT3 | 9つの空席の長い法廷ベンチ・影の帯が大小2群に分ける＝6/3（数字なし・N02 は figures/AE 側・**ACT3 まで保留**） | still |
| S40 | ACT3 | 大理石の台座を囲む低い守りの柵（i2v: 柵が地面に影を落とす・光が移ろう）＝prophylactic の柵 | **motion** |
| S41 | ACT3 | 柵とそれが囲む地面を明確に分けた接写＝「柵であって地面ではない」（fence, not the ground） | still |
| S42 | ACT3 | 冷たい大理石の壁を一条の刻印のような光が横切る（i2v: 光が走る・深い保証＝第5修正・判読不能） | **motion** |
| S43 | ACT3 | 1つの扉が閉じる一方、隣の扉は暖色の光へ開いたまま（i2v: only the second door shut）＝判決の正確な線 | **motion** |
| S44 | ACT3 | 列柱の光が横切る無人の大理石法廷・長いベンチ（SILENCE 5・保持された沈黙） | still |
| S45 | ACT3 | 病院風の卓に引かれた1つの空の椅子＝「あなた自身の椅子」・冷たいティール（匿名） | still |
| S46 | ACT3 | 束の下へ戻る3枚の別々のページ＝反対意見（Kagan＋Breyer＋Sotomayor・中立帰属） | still |
| S47 | ENDING | 署名だけが残る書面への接写（i2v/still: 物語が一線に還る・SILENCE 6 の起点） | still |
| S48 | ENDING | 夜明けへ向かう一室の窓＋端に冷たい光の閉じた扉（i2v: 最後の青が夜明けへ）＝未解決の余韻・CTA 域 | **motion** |

**source 集計（scene-primary）:** motion-primary **9**（S02 S09 S13 S17 S22 S26 S40 S42 S43 ＋ S48＝実質10、下表で S48 を motion に採るなら S26 と入替可の柔軟枠）→ **確定 9**（S02 S09 S13 S17 S22 S26 S40 S42 S43）／factory-primary **5**（S01 S06 S19 S32 S33）／still-primary **34**。**scene-primary はカット全体の一部**で、残りは §5.1 の配分に従い CODEX_B の shotlist が 226 カット（still 101 / factory 93 / motion 32）へ機械展開する。**この表のシーン数・番号は固定（S01..S48）。**

---

# 4. 音の4層設計（ナレ / BGM / SFX / 環境音）

## 4.1 ラウドネス・voice（確定値・EP41/42/43 と同一運用）

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

## 4.2 [SILENCE 1..6] 6箇所の実装（★デジタル無音にしない・`bgm_present` を落とす）

台本の `[SILENCE …]` は**ナレの沈黙であって音の沈黙ではない**。台本には6箇所（最低5・load-bearing）。

| 位置 | 秒 | 対応画 | 鳴らすもの |
|---|---|---|---|
| SILENCE 1（HOOK・ペン上で保持） | **2.0** | S03（署名欄の上のペン） | BGM mute。**SFX 部屋の room-tone のみ**（静まる室内の残響） |
| SILENCE 2（OPENING・黒／署名の光） | **1.5** | S05（署名を横切る一線の光） | BGM mute。**SFX 微細な room-tone のみ** |
| SILENCE 3（ACT1・完成した書面上のペン） | **2.0** | S17（ペンが横たわる完成ページ） | BGM mute。**SFX 静止した部屋の残響のみ** |
| SILENCE 4（ACT2・空の陪審席） | **2.0** | S24（空の陪審席） | BGM mute。**SFX 空の法廷の冷たい反響のみ** |
| SILENCE 5（ACT3・空のベンチ） | **2.0** | S44（列柱の光が横切るベンチ） | BGM mute。**SFX 大理石の広いリバーブのみ** |
| SILENCE 6（ENDING・署名だけ） | **1.5** | S47（署名だけが残る書面） | BGM mute。**SFX 部屋の微かな残響 tail のみ** |

**最長無音候補 2.0秒 << 25秒** ✓ `bgm_present` PASS。6区間ともデジタル無音にせず残響/室内ベッドを残す。**機械逓減にはせず**、感情の核（陪審席・空のベンチ）を 2.0s に保つ。

## 4.3 章ごとの BGM（1章1トラック・`build_tekoh_bgm.py`＝EP42 `build_young_bgm_real.py` を tekoh 用に複製）

| 区間 | 性格 | 楽器 |
|---|---|---|
| HOOK | 低弦の不解決・現在形の緊張・単音が刺す（ペン・署名欄・警告なし） | 低弦+単音メタル |
| OP | ブランドスティンガー（`BrandOpening` 付属） | — |
| ACT1 | 最短・現在形・抑制。刻みは疎で近い（病院廊下・録取） | 低弦+疎パーカッション |
| ACT2 | 転回。無罪→民事提訴→§1983→二度の敗訴の冷たさ | ピアノ+弦 |
| ACT3 | 法の機械性・大理石の荘厳。**最も遅い**。6-3 の重さと prophylactic 柵・Kagan 反対の緊張 | 低弦+弦サステイン |
| ENDING | 解決しない和音 →「dawn」でだけ僅かに暖色に開く（救済なしの余韻） | ピアノ+弦 |
| ENDCARD | ブランドED（`BrandEndcard` 付属） | — |

## 4.4 SFX

| 種別 | 位置 | 音 |
|---|---|---|
| pen on paper | S02/S03/S15/S17 | 万年筆が紙・木卓に触れる微細な硬い音・-20 LUFS（非誇張・C5） |
| room tone hospital | S01/S09/S19 | 夜の病院の廊下の冷たい空調・-30 LUFS |
| stamp | S22 証拠スタンプ | ゴム/木印の一撃・-16 LUFS |
| jury box hold | S23/S24 | 空の法廷の冷たい反響・-28 LUFS |
| door | S16/S43・SILENCE HOOK末/ENDING | 扉の軋み・開閉の残響・-18 LUFS |
| book set | S29/S35/S36 | 革表紙の法書が大理石に触れる低い一撃・-20 LUFS |
| colonnade light | S42/S44 | 大理石の広いリバーブ・光条の無音の移ろい（音は残響のみ）・-30 LUFS |
| impact | AE v01/s01/a01/t01 の数値着地 | 低域インパクト・-12 LUFS |
| tick | numberticker の桁変化 | 微細クリック・-24 LUFS |
| room tone | 全編ベッド（室内・大理石の反響・夜明けの外気） | 広いリバーブ・-30 LUFS |

---

# 5. ビジュアル — 素材積算（★紙芝居回避＝factory実写を必ず混ぜる・1シーン1枚）

## 5.1 素材の積算（★SPEC の値をそのまま満たす配分）

```
[0] 絵が必要な区間 = narrationSeconds 720.6（BrandOpening/Endcard は Bookends が別レイヤー）
[1] 総カット = 226（SPEC）    720.6 / 226 = 3.188秒/カット  ✓ mean_shot 3.19（≤6.0）
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
[8] factory 下限 = 720.6/30 = 24.02 → ≥25本。設計値 93本（still-share≤0.45 を守る下限）   ✓
```
> **[6] の余裕は 0.31%pt しかない。still-cut を1つ増やすと 45% を割る。still-cut は 101 で固定**（16枚だけ2回・残り69枚1回）。QC で still が 85枚を割ったら §9 の**追加は同一シーンの別プロンプト（同一 distinct 別シード）**で回復させ、**cut 数は増やさない**。**still を増やして factory を削るな。**

## 5.2 SDXL と実写在庫の振り分け

- **SDXL（still 85・各1枚）= この事件にしか無い固有物**: ランプ下のペンと書面・署名欄・空の取調台・病院の職員証・質問の部屋・欠けた録音機・証拠スリーブの書面・証拠スタンプ・空の陪審席・開いた法廷の扉・空の天秤・§1983の法令書・責任の扉・二重の法廷・破棄評決・鍵穴・Miranda/Dickerson の法書・礎石・算術の3物・6/3 の影で割れた9席・守りの柵・柵と地面・光条の壁・閉じた扉と開いた扉・あなたの椅子・反対の3ページ・署名だけの書面・夜明けの窓。
- **factory 実写 93 = どこにでもある周辺**: 夜の病院の廊下と外観・冷たい大理石の裁判所/最高裁の外観・列柱・空の法廷/陪審席・連邦控訴審のファサード・夜〜夜明けの街・ambient 繋ぎ。**患者・処置・搬送・救急車・拘束された人・原被疑事実を示唆するクリップを選ばない（制約5）。**

## 5.3 SDXL 生成量（★バリエーション0・variants 禁止）

- `ai_prompts.v001.md` = **body 85行の固有プロンプト**（still 各1枚）＋ i2v 種 **16行** ＝ **計101エントリ**（`--only S01` の `shots=` は 101）。`generate_sdxl_4k.py PD-2026-044-tekoh`（**`--variants 1` または指定なし**）。**`--variants 3` を書かない。**
- i2v-source = **16枚**（動きが意味を持つ絵の固有プロンプト・各1シード）。CODEX_A が Wan 2.2 A14B → RIFE 48fps で 16本生成。
- **総生成 = still 85 + i2v seed 16 = 101枚（各1回）。** factory 93 は生成せず在庫選抜。
- プロンプト実体（85本）・i2v リスト（16）・factory 選定（93）は **CODEX_A**（FROZEN）の担当（本書 §9 は絵コンテ級の記述と共通スタイル/ネガティブの契約のみ）。**CODEX_A の still 資産 ID は S01..S85・i2v は M01..M16／種は M01_src..M16_src。**

## 5.4 factory のファイル名を信じない（★必須工程・CODEX_A・BLOCKING）

> EP36: `city_surveillance_camera_dome` が実際は大聖堂。EP38: 牛が `documents_on_desk`。ラベルは検索語の記録であって中身の保証ではない。

選定した **93本すべて**を `scripts/build_footage_contact_sheet.py --ep PD-2026-044-tekoh --media video --dir <factory staging>` で1本1フレームのラベル付きコンタクトシート（`runs/qc/tekoh_footage_contact_NN.png`）にし**全点目視**。subtype と食い違う本は差し替える。**★病院系クリップは `eyeballed_content` に「an empty corridor, no patients, no people, no medical procedure」を必ず明記（制約5）。判事席に実在の顔が写るニュース映像を使わない（制約6）。**

## 5.5 共通スタイル接尾（各 SDXL プロンプト末尾に必ず付ける・`[STYLE]`＝CODEX_A §5.4 と一字一致）

```
, cinematic still, cold cinematic-documentary grade, deep teal-green and charcoal clinical interior with a single pool of warm tungsten desk-lamp light falling on paper, civic and court spaces in pale cold marble grey, restrained and dignified symbolism, telephoto compression and frontal composition, shallow depth of field, ultra-detailed, photoreal, 4K, 16:9, fine film grain, no text, no watermark, no logo, symbolic still-life, no people, no visible face
```
> EP39/40/41/42/43 との分離: 接尾に `electric blue interrogation`（EP39）・`midday suburban bleached daylight`（EP40）・`steel grey death row cellblock`（EP41）・`warrant-blue night Chicago`（EP42）・`porch-amber house`/`ambulance`（EP43）を**一切含めない**。EP44 の暖色は**ランプ下のペンと書面**のみ、アクセントは **interrogation-teal `#2FA6A0`**。

## 5.6 共通ネガティブ（各 SDXL プロンプトの `Avoid:` に必ず付ける・CODEX_A §5.5 と一字一致）

```
text, words, letters, numbers, captions, watermark, logo, readable document, legible paper, legible case citation, legible docket number, legible date, real celebrity, recognizable real person, identifiable face, portrait, mugshot, likeness of a specific person, human face, human body, patient in a hospital bed, gurney with a person, medical procedure, injury, wound, blood, gore, nude, bare skin, weapon, gun, handgun, cartoon, illustration, anime, 3d render, low quality, blurry, jpeg artifacts, deformed, extra limbs, prison cell, steel cellblock, sodium prison corridor, navy interrogation room, electric blue, midday suburban daylight, bleached sunlight, porch amber house, ambulance, tow truck, ankle monitor
```
> **ネガティブにも制約違反語（"Miranda is dead", "9-0", "no immunity", "overturned Miranda", 原被疑事実語）を書かない**（§1.3）。**原被疑事実・被害・自傷・患者の身体を NEG で明示抑制（制約5・非グラフィック）。病院は「無人の廊下・空室」のみ**、患者・処置・搬送を描かない。

## 5.7 AI開示（強め・毎回・R1）

AI 生成の still・i2v が画面に出ている間、常時右下に **`AI-assisted visualization`**。Oswald 20px / `#C8CDD6` / opacity 70% / 位置 `[W-32, H-28]`。字幕帯と縦 56px 以上離す。概要欄1行: `Some visuals in this film are AI-assisted reconstructions, not photographs of the actual events.`

## 5.8 ★A↔B 境界契約（asset_manifest スキーマ・CODEX_A と一字一致）

- **接続点は `episodes/PD-2026-044-tekoh/05_visuals/asset_manifest.v001.json` ただ1ファイル**。A(producer)＝CODEX_A が書き、B(consumer/validator)＝CODEX_B が読む。**counts と role enum を A/B で一字一致**。
- **スキーマ版:** `tekoh_assets.v1`（固定文字列）。
- **マニフェスト配列（★A/B 同一）:** `stills` / `motion` / `factory` / `overlay` の4配列。
- **counts オブジェクト（★このキー・値で固定・A/B 一字一致）:** `{ "still_body": 85, "still_i2v_source": 16, "motion": 16, "factory": 93, "overlay": 12 }`。cuts 展開は still 101 / factory 93 / motion 32。
- **`stills[].role` enum（★この3値のみ・A/B 同一・`thumb`/`still_thumb` を作らない）:** `body` / `i2v_source` / `reject`。
- **サムネは `role="body"` かつ `also_thumb=true` の body still ちょうど6枚から選ぶ**（別 role を作らない）。**候補（★still 資産 ID 空間 S01..S85＝CODEX_A §5.9・narrative S01..S48 とは別体系）＝ `{S02, S04, S24, S44, S45, S85}`**（CODEX_A §4.3/§4.2 不変条件14 と一字一致）。**A(CODEX_A §4.3)・B(CODEX_B §11) は同一6 asset ID に `also_thumb:true` を立てる。**
- **overlay 枚数も A/B 一致**（合成レイヤー・distinct 素材に数えない）。設計値 **overlay: 12**（particle 6 / light 4 / vfx 2＝CODEX_A §9）。
- CODEX_A は manifest を書いた直後 `build_tekoh_asset_manifest.py --verify` で counts / role / also_thumb / overlay を突き合わせ、**A の値と B の期待が一字一致**であることを確認（不一致は BLOCKING）。**`also_thumb==true` の scene_id 集合が `{S02,S04,S24,S44,S45,S85}` で A↔B 同一**であることも検査（CODEX_A §4.2 不変条件14）。

---

# 6. After Effects ヒーロービート（8枠）— ★AEカードは密度に数えられない

## 6.1 大原則（★EP39/40 の致命傷を回避）

`check_motion_density` は **film.json の `figures+graphics` だけ**を数える。AE の 8枠は本編 mp4 に composite された後に焼き込まれるため gate は 0 カウント。→ **密度下限 31 は §7 の Remotion figures/graphics（37本）で満たす。** AE はその上に載る「決め所の数値タイポ」。

## 6.2 パイプライン（EP38/40/41/42/43 で measured 済み・tekoh 用に複製）

```
[1] Remotion で本編完成 → tekoh_final_bgm.v001.mp4（音声ミックス済み・build_tekoh_bgm.py 適用後）
[2] scripts/ae/build_tekoh_hero_jsx.py（＝build_caniglia_hero_jsx.py を複製）が beats.json と tekoh_hero.jsx を生成
[3] AfterFX -noui -r tekoh_hero.jsx → 各ビートを 1920x1080@30fps の不透明 mp4 で書き出し
[4] scripts/ae/composite_tekoh_hero.py（＝composite_caniglia_hero.py を複製）が ffmpeg overlay + enable='between(t,start,end)' で焼き込み（beats.json の film_offset_sec を +適用）
[5] 出力 → tekoh_final_bgm.v002_ae.mp4（v001 は絶対に上書きしない）
```

## 6.3 スロット確定表（§1.4 の確定数値のみ・8枠・6制約適用・数値は台帳照合）

> **★レイアウトは複製元が実装する8種のみ**（`DATE_STAMP`/`CENTER_STACK`/`MONEY_STACK`/`SPLIT_COMPARE`/`ACT_TITLE_CARD`/`QUOTE_CARD`/`VOTE_SPLIT`/`SEAM_TRANSITION`）。**この表と CODEX_B §7.2 のデッキは id・レイアウト・F-ID・順序が完全一致**（`validate_tekoh_beats` が両方を突き合わせる）。上記8種以外の未実装レイアウト名は使わない。**MONEY_STACK はこの事件に金額が無いため不使用**。**ACT_TITLE_CARD / SEAM_TRANSITION も本デッキでは不使用**（variety は残り5種で ≥3 を満たす）。

| ID | 内容 | 数値ID | F-ID | レイアウト（実装済み8種） | カウント型 | 尺 | 対応台本行 |
|---|---|---|---|---|---|---|---|
| **a01** | 無罪（12人の陪審が有罪にせず） | N09 | F09 | **CENTER_STACK** | なし | 5.5 | "They acquitted him … walked out … not guilty" |
| **s01** | §1983＝民事救済の連邦法 | N03 | F03s | **CENTER_STACK** | なし | 6.0 | "a federal law … known … by nothing more than its number. Section 1983" |
| **t01** | 民事で二度の敗訴 | N06 | F06 | **CENTER_STACK** | なし | 5.5 | "Twice, federal juries heard his civil case, and twice they sided with the deputy" |
| **d01** | 2022・最高裁（date/context） | N01 | F01 | **DATE_STAMP** | なし | 5.0 | "when the case reached the Supreme Court" |
| **v01** | 6–3（限定併記・ONE DOOR CLOSED） | N02 | F02 | **VOTE_SPLIT** | なし | 7.5 | "Writing for six of the nine justices" (vote resolves here) |
| **q01** | prophylactic＝柵であって地面でない（多数） | N13 | F13 | **QUOTE_CARD** | なし | 7.0 | "A fence. Not the ground it stands on." |
| **q02** | Kagan 反対の逐語 | N12 | F12 | **QUOTE_CARD** | なし | 7.5 | "some people whose rights are genuinely broken will be left … with nothing to collect" |
| **c01** | Miranda/Dickerson 存続（払拭の否定） | N04/N05 | F04 | **SPLIT_COMPARE** | なし | 6.5 | "Miranda stands. Dickerson stands." (payoff) |

> **★行順＝start 昇順（時系列）:** `a01`(ACT2 無罪) < `s01`(ACT2 §1983) < `t01`(ACT2 二度敗訴) < `d01`(ACT2末→ACT3 SCOTUS) < `v01`(ACT3 6-3) < `q01`(ACT3 柵) < `q02`(ACT3 Kagan 反対) < `c01`(payoff Miranda/Dickerson stands)。**この id・レイアウト・F-ID・順序は CODEX_B §7.2 デッキと一字一致**（`validate_tekoh_beats` が突き合わせ）。

### 検算

```
[1] 単調増加・重複ゼロ（start は §6.4 beats.json で幕位置に配置・台本行の秒に一致）
[2] HOOK / BrandOpening / 各 SILENCE(最長2.0s) / BrandEndcard に1秒も重ならない
[3] 合計 = 5.5+6.0+5.5+5.0+7.5+7.0+7.5+6.5 = 50.5秒 / 733.1 = 6.9%   ✓ 過剰でない
[4] レイアウト種類 = CENTER_STACK, DATE_STAMP, VOTE_SPLIT, QUOTE_CARD, SPLIT_COMPARE = 5種（全て実装済み8種内）   ✓ ≥3
[5] figures[] 34枠と1秒でも重ならない（validate_tekoh_beats.py が両方突き合わせ・§7.3）
[6] v01(6-3) は ACT3 内に配置＝HOOK/OPENING/最初30秒に得票が出ない（構造ロック・C2）
```

## 6.4 `beats.json`（`08_edit/ae_hero/beats.json`・`schema_version: "tekoh_beats.v1"`・EP43 と同一スキーマ）

**確定ラベル（★ASCII のみ・em-dash 禁止＝`-` に置換・全大文字・6制約適用）:**
```
a01 CENTER_STACK   top="THE VERDICT"  main="ACQUITTED"
        bottom="A JURY REFUSED TO CONVICT"                                     # F09/N09・C5: 罪状を出さない
s01 CENTER_STACK   top="THE CIVIL PATH"  main="SECTION 1983"
        bottom="SUE A STATE OFFICIAL FOR A CONSTITUTIONAL WRONG"               # F03s/N03・C4: 免責断定なし=民事救済の扉
t01 CENTER_STACK   top="THE CIVIL SUIT"  main="2 TRIALS"
        bottom="TWICE THE JURY SIDED WITH THE DEPUTY"                          # F06/N06・二度の敗訴
d01 DATE_STAMP     date="2022"  place="SUPREME COURT OF THE UNITED STATES"     # F01/N01・No. 21-499 は lowerthird
v01 VOTE_SPLIT     top="VEGA v. TEKOH - 2022"  left="6"  right="3"
        bottom="ONE DOOR CLOSED"                                               # F02/N02・C1/C2: 6-3=分割/Miranda廃止に読ませない
q01 QUOTE_CARD     quote="A FENCE, NOT THE GROUND IT STANDS ON"
        attribution="THE MAJORITY, ON MIRANDA'S WARNINGS"                      # F13/N13・C6: prophylactic・中立帰属
q02 QUOTE_CARD     quote="STRIPS ... THE ABILITY TO SEEK A REMEDY"
        attribution="JUSTICE KAGAN, IN DISSENT"                                # F12/N12・C6: 逐語・中立帰属
c01 SPLIT_COMPARE  top="WHAT SURVIVED"  left="MIRANDA STANDS"  right="DICKERSON STANDS"
        bottom="UNWARNED WORDS CAN STILL BE KEPT OUT OF TRIAL"                 # F04/N04/N05・C1/C3: 排除の扉は開いたまま
```
> **v01 の bottom は "ONE DOOR CLOSED"（★"9-0"/"Miranda is dead" 系の文字列を書かない＝R-VOTE/R-SCOPE 一致）**（C1/C2）。**「排除の扉は開いたまま」は c01 の bottom "UNWARNED WORDS CAN STILL BE KEPT OUT OF TRIAL" が担う（削除禁止・C1 温存側の可視化）。** **q01/q02 の quote は逐語のみ**（要約を引用符に入れない・facts_lock R-VOTE 中立帰属で確認）。**s01 の bottom は §1983 を民事救済として説明**（"no immunity" と書かない・C4）。**どのカードにも「police need not read rights」「Miranda is dead」を無留保で書かない**（C1）。**原被疑事実の性質語をどのカードにも出さない**（C5）。数値ID＝台帳（§1.4）と一致必須。カウント終了から区間終端まで最低 1.20秒ホールド。
> **★AI開示レイヤー（R1・全カード常時）:** 共通レイヤースタック（§6.5）に `AI-assisted visualization`（Oswald 20px / SILVER `#C8CDD6` / opacity 70% / 右下 `[W-32, H-28]`）を1枚追加し全カードに焼く。AEカードは不透明の全画面 mp4 として本編に overlay され本編右下の開示を覆うため、これが無いと AI生成 static 背景が開示なしで表示される（R1 違反）。`validate_tekoh_beats` と §13 受入アイボールで「AEカード表示中も開示が見える」を確認。

## 6.5 レイアウト定義（EP43 §6.5 を踏襲・色定数のみ EP44 値）

**共通レイヤースタック（下→上）:** L9 黒ソリッド → L8 静止画（scale fill→fill×1.08・drift）→ L7 グレードウォッシュ（**冷たいティール緑** `addSolid([0.047,0.082,0.078])`＝CLINIC / MULTIPLY / opacity 30）→ L6 羽根付き楕円ビネット → L5 グロー（下中央 interrogation-teal ADD）→ L4 ライトスイープ（`"ADBE Rotate Z"`=18）→ L3 上ラベル（Oswald）→ L2b アクセントライン（ACCENT interrogation-teal・scaleX ワイプ・`motionBlur=true`）→ L2 主数値/主文字（Anton・ACCENT・`motionBlur=true`）→ L1b 下ラベル → L1 字幕ロワーサード → **L0b AI開示テキスト（`AI-assisted visualization`・Oswald 20px・SILVER `#C8CDD6`・opacity 70%・右下 `[W-32, H-28]`・全カード常時焼き＝R1）** → L0 黒シームディップ（head/tail 各4フレーム）。

**色定数（0..1 float）:**
```python
ACCENT = [0.184, 0.651, 0.627]   # #2FA6A0 — interrogation-teal（数値・下線・グロー・OP/AE/サムネ accent）
WHITE  = [0.961, 0.969, 0.980]   # #F5F7FA
SILVER = [0.784, 0.804, 0.839]   # #C8CDD6
CLINIC = [0.047, 0.082, 0.078]   # #0C1514 — 冷たいティール緑 near-black ウォッシュ寄り
MARBLE = [0.227, 0.231, 0.251]   # #3A3B40 — 大理石（ACT3）
LAMP   = [0.894, 0.722, 0.478]   # #E4B87A — 机上ランプの暖色（ペンと書面のグローのみ・数値/下線に使わない）
```
**フォント:** 数値/主文字 = **Anton Regular** / ラベル・字幕 = **Oswald Medium**。`getFontsByFamilyNameAndStyleName` で厳格解決（miss は throw・フォールバック禁止）。テキスト幅は **`sourceRectAtTime(t,false).width` で実測**（advance-width 推定禁止＝EP40 文字切れの原因・ブリーフ§5）。

**カウント型:** この事件は金額が無く、6-3 は得票なのでカウントアニメ不可。→ **本編 AE ではカウントアニメを使わず全て静的タイポ**で settle（ease-out cubic）。数値の「着地」インパクトは L2 の scale/opacity 併用と impact SFX で作る。VOTE_SPLIT の 6/3 は左右2値を別レイヤーで静的着地。

## 6.6 このマシン固有の罠（★1つ忘れると無言で品質が落ちる・EP43 §6.6 全項を tekoh に適用）

フォント解決の例外ラップ（`psName()`）／spatial ease は配列次元1（`prop.isSpatial ? 1 : ...`）／OM=`"H.264 - レンダリング設定を一致 - 15 Mbps"`・RS=`"最良設定"`（英語名は try/catch フォールバック）／`app.newProject()` を headless で使わない（同名 `TEKOH_` コンプを防御削除）／`layer.motionBlur=true` を動くレイヤー個別に／回転は `"ADBE Rotate Z"`／改行は1行厳守（SPLIT_COMPARE/VOTE_SPLIT の左右2値は別レイヤー）／em-dash は `-`／inPoint と outPoint 両方設定／`item.mainSource.conformFrameRate = 30`／実行パス `C:\Program Files\Adobe\Adobe After Effects 2026\Support Files\AfterFX.exe`／`proj.gpuAccelType = GpuAccelType.SOFTWARE`／ビルド ~100–120秒・完了マーカー `render/_build_ok.txt` をポーリング（タイムアウト≥300秒）・末尾で `app.quit()`／**aerender 前に `.aep` mtime > `.jsx` を assert**（ブリーフ§5・.aep が古いと前ビルドを焼く事故）。

## 6.7 コンポジタ（`scripts/ae/composite_tekoh_hero.py`・SKIP 4条件を1つも削らない）

`BASE = tekoh_final_bgm.v001.mp4` / `OUT = tekoh_final_bgm.v002_ae.mp4`（v001 不変）。**beats.json の `film_offset_sec` を +適用**（EP42/EP43 composite と同じ）。SKIP: (1) `render/<id>.mp4` 不在 / (2) 解像度≠1920x1080 / (3) 実測尺 `< dur-0.3` / (4) `beat.end > base_dur`。ffmpeg: `overlay=0:0:eof_action=pass:enable='between(t,start,end)'` / `-c:v libx264 -preset slow -crf 16 -pix_fmt yuv420p -colorspace bt709 -c:a copy`。**出荷済みを絶対に上書きしない。**

---

# 7. Remotion MGビート（FigureBeats）— ★密度下限 31 は必ずここで満たす・★dochighlight 不使用

## 7.1 密度の設計（`tekoh_film.json` の `figures[]` ＋ `graphics[]`）

`check_motion_density`: 3つを AND。**body-minutes = narrationSeconds/60 = 720.6/60 = 12.010**。

| 指標 | floor | EP44 設計値 |
|---|---|---|
| density | ≥2.5/min | figures 34 + graphics 3 = **37 beats / 12.010 = 3.08/min** ✓（SPEC beats_floor 31 に +6） |
| coverage | ≥0.25 | 37 beats × 平均 6.0秒 = 222秒 / 720.6 = **0.308** ✓ |
| variety | ≥3 distinct forms | **10種**（下記） ✓ |

> **AE の 8枠は film.json に入れない**（composite 後に焼くため gate 非カウント）。**density は Remotion 側 37 beats だけで 31 を超える。**

## 7.2 `figures[]` の種類配分（★kind は全部小文字・同一 kind を連続させない・★dochighlight を1枠も使わない・`comparebars` は非実在→`compbars`）

**使用可能 kind（全小文字・ブリーフ§5 の許容集合）:** `numberticker` `stat` `votetally` `timeline` `quote` `kinetic` `lowerthird` `acttitle` `compbars` `mechanism`。**大文字は無音描画になる。★`dochighlight` は使わない（黒バー/box/underline がバグに見える＝EP40/41/42 で3回指摘・ブリーフ§5）。★`comparebars` は存在しない→ `compbars`。**

| kind（小文字） | 枠数 | EP44 での用途（6制約適用） |
|---|---|---|
| `acttitle` | 3 | ACT1「That night」/ ACT2「The turn」/ ACT3「The doctrine」 |
| `timeline` | 5 | ①あの夜: 2014 LA の医療センター→質問→警告なしの録取 ②訴訟: 起訴→公判→無罪→民事提訴→§1983→二度の敗訴→第9巡回区→cert ③判例系譜: Miranda 1966→Dickerson 2000→Vega 2022 ④二度の裁判（第1評決 破棄→再審→Vega 勝訴）⑤二つの扉: 排除（開）vs §1983 賠償（閉） |
| `stat` | 7 | TWO TRIALS（N06）／ACQUITTED（N09）／SECTION 1983（N03）／MIRANDA 1966（N04・存続）／DICKERSON 2000（N05・存続）／SIX JUSTICES（N08・多数・**votetally と別区間**）／THREE JUSTICES（N07・反対） |
| `votetally` | 1 | **6–3 Vega のみ**（F02・majority:6/dissent:3・**"one door closed" ラベル必須**・**ACT3 まで保留**・C1/C2）。**他の数値は votetally に入れない** |
| `quote` | 4 | ①多数逐語「a fence, not the ground it stands on」（**多数帰属**・prophylactic・C6）②Kagan 逐語（**Kagan 帰属**・反対・救済を奪う警告・N12・C6）③payoff「Miranda stands. Dickerson stands.」（存続・C1/C3）④「what the Court closed was only the second door」（賠償の扉のみ閉鎖＝射程限定・C1）。**要約を引用符に入れない・facts_lock で逐語確認** |
| `lowerthird` | 2 | 「Miranda v. Arizona, 384 U.S. 436 (1966)」（N04・帰属）／「Vega v. Tekoh, No. 21-499 (2022)」（N01・帰属・本文で読み上げない） |
| `compbars` | 4 | ①柵（prophylactic 安全装置）vs 地面（第5修正の権利そのもの）（C6・prophylactic）②閉じた扉（§1983 民事賠償）vs 開いた扉（刑事公判の排除）（C1）③Miranda＝憲法規則（Kagan の読み）vs prophylactic 安全装置（多数の読み）（中立帰属）④右と remedy＝権利と救済は別物（ENDING の核・C1） |
| `numberticker` | 4 | TWO TRIALS（N06・AE と別区間）／THREE JUSTICES（N07・反対）／SIX JUSTICES（N08・多数）／2014→2022（N10→N01・年ティッカー） |
| `mechanism` | 4 | ①多数の論理: 警告＝prophylactic 柵 → 権利そのものでない → 未告知は憲法違反でない → §1983 の損害でない → 賠償なし（C1/C4）②Tekoh の主張: 規則→違反→救済（算術のような主張）③Kagan の論理: Miranda は憲法規則 → 執行可能な権利 → 救済のない権利は権利でなくなる（C2 中立帰属）④射程限定: 閉じたのは賠償の第2の扉だけ → 排除の扉は開いたまま（C1） |
| **合計** | **34** | variety = 9 figure-kinds |

`graphics[]`（kinetic typography）3枠: 幕タイトルの語同期切れ上がり・HOOK の問い・payoff「A right and a remedy are not the same thing」（`kinetic`）。→ variety に `kinetic` が加わり **10種** ≥3 ✓。

> **★実装表現（CODEX_B §6）:** CODEX_B は上記 34+3 を **すべて `figures[]` に 37本**入れ、`graphics[]=[]` にする（`check_motion_density` は `figures+graphics+heroCuts` を合算するので密度は同値・floor 31 に +6）。「figures 34/graphics 3」は DESIGN 上の役割分類であり、film.json 上は全 37 が figures[]・graphics[] は空配列。どちらで数えても 37 beats。**★`grep '"kind": "dochighlight"' tekoh_film.json` は 0 件でなければならない（ブリーフ§5・BLOCKING）。`comparebars` も 0 件（正は `compbars`）。**

## 7.3 配置ルール

1. **AE の 8区間（§6.3）と1秒でも重ならない**（`validate_tekoh_beats.py`＝validate_caniglia_beats.py を複製・両方突き合わせ）。
2. 幕あたり配分: HOOK/OP=3 / ACT1=4 / ACT2=8 / ACT3（doctrine+payoff）=17 / ENDING=5（ACT3 が最長 287.4s なので厚め）。
3. **同じ kind を連続させない。**
4. 1枠 4.0–8.0秒。
5. ACT3 の説明区間に `compbars`＋`quote`＋`timeline`＋`mechanism`＋`votetally` を分散し 20秒超の平坦区間をゼロに。
6. `quote` は**逐語のみ**（要約を引用符に入れない・C6）。帰属は 多数 / Kagan に帰属語を伴う（中立・C2）。
7. `figures[].text`/`lines[]` は `facts_lock` 検査対象（「Miranda is dead」「9-0」「no immunity」「overturned Miranda」「原被疑事実」を出さない）。**得票（6-3）は ACT3 前に置かない（構造ロック）。**

## 7.4 密度の最終検算

```
Remotion figures 34 + graphics 3 = 37 kinetic beats（film.json 内）
  density  = 37 / 12.010 = 3.08/min   ✓ ≥2.5（SPEC beats_floor 31 → 37 で +6）
  coverage = 222s / 720.6 = 0.308      ✓ ≥0.25
  variety  = 10 forms                  ✓ ≥3
  dochighlight = 0 / comparebars = 0   ✓（ブリーフ§5）
AE hero 8枠は composite 後・gate 非カウント（上乗せの決め所）
```

---

# 8. レイヤー構成 と ゾーン分離（★主役の裏に最低4層）

## 8.1 本編カットのレイヤー構成（下→上・主役 L4 の裏に L1/L2/L3/L3b = 4層）

| L | 名前 | EP44 の値 |
|---|---|---|
| **L0** | ルート背景 | `#0A0A0C`（INK） |
| **L1** | グラデ背景 | `radial-gradient(120% 120% at 50% 40%, #0C1514 0%, #0A0F0E 45%, #0A0A0C 100%)`（冷たいティール緑の病院の夜。ACT3 のみ大理石寄り `#1A1B1F` にシフト可） |
| **L2** | グリッド/ライン | 縦横 64px の反復線＋放射マスク＋ドリフト。`repeating-linear-gradient(0deg/90deg, #2FA6A018 0px 1px, transparent 1px 64px)`、`translateY 0→48px` / `Easing.inOut(Easing.sin)`（等速禁止） |
| **L3** | グロー | 単一 interrogation-teal のグロー（ペンと書面/取調台/列柱の光条の位置に移動）。`radial-gradient(closest-side, #2FA6A066 0%, #2FA6A018 45%, transparent 75%)`、`filter: blur(28px)`。位置は幕で移動（ペンと署名欄→取調台→陪審席→大理石→閉じた/開いた扉）。ペンと書面のカットは LAMP `#E4B87A` の暖色グローを併置可（数値/下線には使わない） |
| **L3b** | 大理石の光帯/ビネット | ACT3 は第5修正の光帯（`linear-gradient(100deg, transparent, #2FA6A022, transparent)` を横に slow drift）、他幕は羽根ビネット。`translateX` を `Easing.inOut(Easing.sin)` で微動（静止フレームゼロ） |
| **L4** | 主役（still / i2v / factory） | §10 のモーション（Ken Burns/parallax/i2v） |
| **L5** | テロップゾーン（上/中央・figures） | §8.2 |
| **L6** | 字幕ゾーン（下部帯） | §8.2 |

> **主役（L4）の裏に L1/L2/L3/L3b = 4層**（グラデ背景・グリッド/ライン・グロー・光帯/ビネット）で CLAUDE.md「最低3レイヤー」＋タスク「最低4層」を満たす。

## 8.2 ゾーン分離（一度も重ねない）

| ゾーン | 縦位置（1080基準） | スタイル |
|---|---|---|
| テロップ見出し | `y=96–260` | Oswald 64px / `#F5F7FA` / letterSpacing 4 |
| 中央テロップ / figures | `y=420–660` | §7 |
| 出典テロップ（アクセントライン） | `y=742–786` | Oswald 28px / interrogation-teal `#2FA6A0` 3px 下線 |
| 字幕帯 | `y=872–1010` | 白 `#FFFFFF` + `textShadow:0 0 6px #000,0 2px 4px #000` / 半透明黒帯 `rgba(6,6,8,0.62)` / ≤2行・1行≤42字 / 54px / lineHeight 1.28 |
| AI開示 | `y=1024–1052`（右下） | Oswald 20px / `#C8CDD6` / opacity 70% |

**Caption QC:** ナレ一致 ≥99%（faster-whisper 強制アライン）/ `.srt` カバー ≥95% / キュー 1.0–6.0秒 / CPS ≤17 / 単語割り禁止 / 1語孤立キュー禁止 / ズレ ≤120ms。**[SILENCE 1..6] の6区間には字幕キューを置かない。**

---

# 9. 絵コンテ（★48シーン・象徴のみ・6制約・Tekoh/Vega/判事 非人物化・原被疑事実の非描写・CODEX_A が 85本プロンプトへ展開する原図）

## 9.1 パーサ契約（★CODEX_A が `ai_prompts.v001.md` を書くときの形式・`read_prompts()` が読む2行形式）

`read_prompts()` の正規表現は `^\s*-\s+`([^`]+\.png)`\s*$`。つまり:
```
- `S01.png`
<positive prompt> ... [STYLE] Avoid: <negative>
```
- **1行目:** `` - `S01.png` ``（バッククォート囲み・行末は `.png` 直後）。プロンプトを同じ行に書かない。
- **2行目:** 正プロンプト → `[STYLE]`（§5.5）→ `Avoid:` → 負プロンプト（§5.6）。
- 配置先: **`episodes/PD-2026-044-tekoh/04_scenes/ai_prompts.v001.md`**（CODEX_A が書く・B は読むだけ）。生成: `.venv/Scripts/python.exe scripts/generate_sdxl_4k.py PD-2026-044-tekoh`（**variants 指定なし＝1枚**）。
- 出力: `H:\pd-media\assets\ai\tekoh\S01.png …` ＋ `remotion/public/tekoh/`。長辺 ≥3840 で冪等スキップ。
- **★body 85本＝85行**（still 各1枚・CODEX_A §5.9）＋ **i2v 種 16行**（CODEX_A §8.1a）＝ `ai_prompts.v001.md` は計 **101 エントリ**。CODEX_A は書いた直後 `--only S01` で `shots=` が **101**（body 85 + i2v種 16）に達しているか（2行形式が壊れていないか）を確認。

## 9.2 絵コンテ級ショット記述（Sid ごと・カメラ/モーション/象徴/制約。CODEX_A はこれを固有プロンプトに翻訳）

> **全ショット共通:** 顔・身体・肖像なし（R1/C6）。Tekoh も Vega も個人として描かない（象徴・影・後ろ姿・手元のみ）。判事を人物化しない。読める文字を作らない（redacted/illegible）。冷たいティール緑の病院の夜＋冷たい大理石＋唯一の暖色＝ランプ下のペンと書面。「Miranda is dead」「9-0」「全面勝訴」を画に含意させない。**原被疑事実（疑われた罪の性質・被害・患者・処置・搬送・拘束された人）を一切描かない（C5）。** 閉じた扉（§1983 賠償）と開いた扉（刑事公判の排除）を象徴で必ず併存（C1）。1シーン1枚＝各 Sid の主 still は1本。ambient は factory で埋める。

| Sid | カメラ/レンズ | 象徴（動き） | 制約メモ |
|---|---|---|---|
| S01 | 引き・廊下 | 夜の病院の廊下・冷たいティール緑・無人（factory ambient） | C5: 患者/処置なし |
| S02 | 接写・卓上 | ランプ下のペンと書面・下に署名欄（i2v: 光が揺れペンが構えられる） | C6: 手なし・非誇張 |
| S03 | 接写・署名欄 | 署名欄の上のペン・警告カードは無い（SILENCE 1） | C1: 警告の不在 |
| S04 | 正対・静止 | 空の取調台・紙とペン・録音機なし（警告が来なかった部屋） | C5: 人物なし |
| S05 | 接写・暗中 | 署名を横切る一線の光（SILENCE 2） | 中立 |
| S06 | 引き・列柱 | 最高裁の列柱・冷たい大理石（factory ambient） | — |
| S07 | 正対・被写界深度 | 手前に書面・奥に列柱 faint＝署名から最高裁への span | — |
| S08 | 接写・フック | 病院の職員証（無人・匿名・名前なし） | C5/C6: a hospital employee・顔なし |
| S09 | 引き・廊下 | 夜の病院の廊下・遠くに微かな動き（i2v: 通り過ぎる場所） | C5: 識別可能人物なし |
| S10 | 俯瞰・寄り | 静かな控室・空の椅子・上着（人物なし） | C6 |
| S11 | 正対・室内 | 質問の部屋・2脚の向かい合う椅子・冷たい光（無人） | C6: 人物なし |
| S12 | 接写・卓上 | 卓中央の白紙とペン＝部屋から出てくる紙 | facts illegible |
| S13 | 接写・卓上 | 半ば埋まった手書きの録取ページ（i2v: 緩いプッシュ・判読不能） | C5: 内容を描かない |
| S14 | 接写・卓上 | 録音機があるべき空の場所＝欠けていたもの | C1: 警告の不在 |
| S15 | 接写・署名欄 | 署名欄の上に構えられたペン・警告カードなし | C1: 署名の直前・手なし |
| S16 | 正対・室内 | 内側から見た閉じた小部屋の扉・下に廊下の光 | 後で S43 と対 |
| S17 | 接写・push | ペンが横たわる完成した書面（i2v: 緩いプッシュ・SILENCE 3） | 静止した部屋 |
| S18 | 正対 | 質問の部屋のあと・卓に残された紙とペン | — |
| S19 | 引き・廊下 | 病院の廊下（factory ambient・受け・無人） | C5 |
| S20 | 接写 | 証拠スリーブに入り運び出される書面＝法廷へ旅する | C5: 内容を描かない |
| S21 | 正対・法廷 | 夜の無人の法廷内観・空のベンチと証言台 | C6: 人物なし |
| S22 | 接写・push | 証拠スタンプの書面（i2v: 法廷の光・判読不能）＝政府の立証に転じる | C5: illegible |
| S23 | 正対・対称 | 空の陪審席・12の空席（12人＝空の椅子） | C6: 人物なし |
| S24 | 正対・静止 | 空の陪審席を保持（SILENCE 4・評決前） | 沈黙の画・also_thumb 候補 |
| S25 | 正対 | 開いた法廷の扉・奥に淡い昼光・空の傍聴席＝無罪で去る（不在で示す） | C5: no guilty 語なし |
| S26 | 接写・push | 光の帯の中で武器のように置かれた書面（i2v: 冷たい光） | C5: illegible・私人の手が証拠に |
| S27 | 正対・扉 | 民事裁判所の閉じた扉・冷たい石＝別種の訴え（民事） | C4 |
| S28 | 接写・卓上 | 空の天秤と畳まれた書式＝金銭で測られる請求（判読不能） | 象徴 |
| S29 | 接写・卓上 | 暖色ランプ下の古い連邦法令の閉じた革表紙＝番号だけの深い根の法（§1983） | C4: illegible |
| S30 | 正対・扉 | 大理石の壁の1つの扉が僅かに開く＝役人を責任に問う扉 | C4: 免責を断定しない |
| S31 | 正対・二重像 | 二重に映る法廷ベンチと陪審席＝二度の裁判 | — |
| S32 | 引き・外 | 破棄評決＋連邦控訴審のファサード（factory ambient）＝差戻し→第9巡回区 | — |
| S33 | 引き・列柱 | 最高裁の列柱・正面・夜（factory ambient）＝事件が上げられる | — |
| S34 | 接写 | 冷たい大理石の1つの小さな鍵穴＝狭い一つの技術的な問い | 象徴 |
| S35 | 壁/棚ショット | 無傷で立つ古い1966年の法書＝Miranda はまだ立つ（判読不能） | C3: 存続 |
| S36 | 壁/棚ショット | その隣の2000年の静かな法書＝Dickerson・無傷 | C3: 存続 |
| S37 | 象徴・下部 | 大理石建築の下の深い礎石＝掃き払えぬ深く根ざした規則 | 象徴 |
| S38 | 卓上 | 一列の3つの物＝規則・違反・救済の等式（算術のような主張） | facts illegible |
| S39 | 正対・対称 | 9つの空席・影の帯が大小2群に分ける＝6/3（数字なし） | C2: 数字は figures/AE 側・ACT3 保留 |
| S40 | 象徴・接写 | 台座を囲む低い守りの柵（i2v: 柵が地面に影を落とす） | C1: prophylactic の柵 |
| S41 | 象徴・接写 | 柵とそれが囲む地面を明確に分ける＝柵であって地面でない | C1: fence, not the ground |
| S42 | 壁ショット | 大理石の壁を一条の刻印のような光が横切る（i2v: 光が走る・第5修正） | C6: 象徴・逐語は figures |
| S43 | 象徴・正対 | 1つの扉が閉じる一方、隣の扉は開いたまま（i2v: only the second door shut） | C1: 判決の正確な線 |
| S44 | 引き・大理石法廷 | 列柱の光が横切る無人の大理石法廷・長いベンチ（SILENCE 5） | also_thumb 候補・沈黙の画 |
| S45 | 正対・寄り | 病院風の卓に引かれた1つの空の椅子＝「あなた自身の椅子」（冷たいティール） | C6: 匿名・also_thumb 候補 |
| S46 | 卓上 | 束の下へ戻る3枚の別々のページ＝反対意見（Kagan＋Breyer＋Sotomayor） | C2: 中立帰属 |
| S47 | 接写 | 署名だけが残る書面への接写（SILENCE 6 の起点・物語が一線に還る） | C5: illegible |
| S48 | 引き・窓/扉 | 夜明けへ向かう一室の窓＋冷たい光の閉じた扉（i2v: 最後の青が夜明けへ）＝未解決の余韻 | C1: 救済なしの余韻・CTA 域 |

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
**0.5s 刻み方針:** 226カットの境界は **`QUANT`=15フレーム（0.5秒）にスナップ**して配置。各カット長は `CUT_MIN`〜`CUT_MAX`、平均 `CUT_MEAN`。ACT3（doctrine）は最も遅く（長カット寄り・6.0s 近辺を多用）、ACT1 は速く（1.0–2.5s の断片・現在形・病院廊下）。CODEX_B は shotlist の各 span 端を 15f グリッドに丸める。

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
// 速いカット（S02 ペン構え / S22 証拠スタンプ光 / S43 扉が閉じる / numberticker 桁変化 / 幕頭 kinetic / votetally 6-3 着地）
<Trail layers={6} lagInFrames={1.2} trailOpacity={0.45}>
  {/* 主役 or 動く数値/文字 */}
</Trail>
```
対象: **S02**（ペンが構えられる）、**S22**（証拠スタンプに光が当たる）、**S43**（扉が閉じる・もう一つは開く）、および §7 の `numberticker`・幕頭 `kinetic`・`votetally` の 6-3 着地。**S13/S17（書面への緩いプッシュ）・S40（柵の影）・S42（光が走る）・S48（夜明けの窓）は緩なので Trail 不要**（無駄な残像・扇情を避ける・C5）。ゆっくりした Ken Burns には Trail をかけない。

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
- **複数文字・複数要素はスタッガー**: `delay = i * f(0.04)` = 1文字/約1.2フレーム（30fps）。要素群は `delay = i * f(0.06)`。
- 幕タイトル語群・figures の見出しは全てこの `overflow:hidden`＋`translateY` マスク切れ上がりを基本形にする。**等速線形は1箇所も使わない**（spring か `Easing.out(Easing.cubic)`）。

## 10.5 幕別モーション・トーン（0→720.6s の運動設計の要約）

| 幕 | 秒域 | 運動トーン |
|---|---|---|
| HOOK | 0–33.0 | 象徴モンタージュ・~2s カット・hard cut 寄り。ペン/署名欄/廊下/取調台。SILENCE 1 でペン上を保持（動きは L2/L3 の微ドリフトのみ・完全静止ゼロ） |
| OPENING | 33.0–79.2 | やや落ち着く。署名の一線→列柱→span。ディゾルブ 8f。SILENCE 2 は署名の光を保持 |
| ACT1 That night | 79.2–156.7 | 最短・現在形・病院廊下。1.0–2.5s 断片・hard cut。i2v（S09 廊下/S13 録取/S17 完成ページ）。SILENCE 3 で完成ページ保持 |
| ACT2 The turn | 156.7–307.6 | 正対の転回。証拠化→無罪→民事提訴→§1983→二度の敗訴→第9巡回区。中庸カット 3–4s。SILENCE 4 で空の陪審席 2.0s |
| ACT3 The doctrine | 307.6–520.2 | 最も遅く荘厳。長カット 4–6s・長ディゾルブ。鍵穴/法書/礎石/6-3 の影/守りの柵/閉じた扉と開いた扉。SILENCE 5 で空のベンチ 2.0s |
| ACT3 payoff | 520.2–595.0 | 最も遅いビート。閉じた扉と開いた扉の対比を確定。射程限定の核 |
| ENDING | 595.0–706.2 | 引き（pull-back）。あなたの椅子・署名だけ・夜明けの窓。SILENCE 6 で署名 1.5s・救済なしの余韻で終わる |

---

# 11. オープニング（OP）設計 — 完全仕様（`OpeningTekoh`・fps=60・CLAUDE.md §1–5 全項目）

## 11.1 秒数ベースのタイムライン（fps=60・「フレーム」は全て `Math.round(60 × 秒)`・直書き禁止・0.5s 刻み方針で全区間記述）

```ts
const FPS_OP = 60; const F = (s:number)=>Math.round(FPS_OP*s);   // 総 180f = F(3.0)
```

| 秒 | フレーム | 起きること（EP44 signature = ランプ下のペンと署名欄・interrogation-teal のアクセント） |
|---|---|---|
| 0.00–0.10 | f0–6 | 画面 `#0A0A0C`。**L1** グラデ opacity 0→1（0.40s）＋ **scale 1.08→1.00** を 180f で（`Easing.out(Easing.cubic)`）。opacity 単独でなく scale 併用 |
| 0.10–0.15 | f6–9 | **L6 ロゴ**（`hasLogo`）左上 `top:64/left:72` に spring 出現。scale 0.4→1.0・opacity 0→1（併用・`damping:14,mass:0.9`） |
| 0.15–0.25 | f9–15 | **L2** グリッドが spring（`{damping:200,mass:1,durationInFrames:F(0.8)=48}`）で reveal。最終 opacity=`gridReveal*0.18`。全体を 180f で `translateY 0→48px`（`Easing.inOut(Easing.sin)`） |
| 0.25–0.30 | f15–18 | **L3** interrogation-teal グローが spring（`{damping:18,mass:1.2}`）＝署名欄の脇に点る。scale 0.6→1.15 / opacity 0→0.85（併用）。`filter:blur(28px)` |
| 0.30–0.86 | f18–52 | **L4 主役タイトル**が1文字ずつ切れ上がる（`overflow:hidden` マスク）。各文字 spring（`{damping:16,mass:1}`）で `translateY 110%→0`、opacity=`interpolate(sp,[0,0.25],[0,1])`。**スタッガー=`F(0.04)=2フレーム/文字**。全体を `Trail`（`layers=6,lagInFrames=1.2,trailOpacity=0.45`）で包む |
| 0.55–1.15 | f33–69 | **L2b 署名の光ライン**（EP44固有＝ランプの光が署名欄を舐める interrogation-teal の帯）。中央からタイトル背後を横切る光が `scaleX 0→1`＋`opacity 0→0.55`（spring `{damping:22,mass:1.1}`, `transformOrigin:'center'`）。opacity 単独禁止で scaleX 併用 |
| 0.95–1.35 | f57–81 | **L5a** interrogation-teal の下線が左から `scaleX 0→1`（spring `{damping:16,mass:0.8}`, `transformOrigin:'left center'`）。240×6px・`boxShadow:0 0 24px #2FA6A0aa` |
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
| L2b 署名の光 | scaleX 0→1 / opacity 0→0.55 | spring | `{damping:22,mass:1.1}`・origin center |
| L5a 下線 | scaleX 0→1 | spring | `{damping:16,mass:0.8}`・origin left |
| L5b サブ | translateY 24px→0 / opacity | spring | `{damping:20,mass:1}` |
| L6 ロゴ | scale 0.4→1.0 / opacity | spring | `{damping:14,mass:0.9}` |

> **全 opacity が translateY/scale/scaleX と対。等速線形を1箇所も使わない。**

## 11.3 レイヤー構成（下→上・主役 L4 の裏に L1/L2/L2b/L3 = 4層）

L0 `#0A0A0C` / L1 グラデ（`radial-gradient(120% 120% at 50% 35%, #0C1514 0%, #0A0F0E 45%, #0A0A0C 100%)`）/ L2 グリッド（`${accent}22` 64px・放射マスク）/ L2b 署名の光（`linear-gradient(90deg, transparent, ${accent}cc, ${accent}55, ${accent}cc, transparent)`）/ L3 interrogation-teal グロー（`radial-gradient(closest-side, #2FA6A088, #2FA6A022, transparent)` `blur(28px)`）/ L4 主役タイトル（Trail 包み・`overflow:hidden` span マスク・Anton `fontWeight:800 fontSize:150 letterSpacing:-2 color:#F5F7FA`）/ L5 下線＋サブ（Oswald `fontSize:38 letterSpacing:6 uppercase color:#C8CDD6`）/ L6 ロゴ（`linear-gradient(135deg, ${accent}, #ffffff22)`・`border:2px solid ${accent}`）。

## 11.4 確認方法（CLAUDE.md §5）

```bash
cd C:\Users\aab15\Documents\prime-documentary\remotion
npm run studio     # = remotion studio。OpeningTekoh を 0→180f でスクラブし §11.1 の各時刻を目視
npx remotion render OpeningTekoh out/tekoh_opening.mp4 --props=./props/tekoh.json
# props 差し替え量産
npx remotion render OpeningTekoh out/tekoh_short_op.mp4 --props=./props/tekoh_short.json
# 本編
npx remotion render Ep44Tekoh out/tekoh_final.mp4 --props=./src/data/tekoh_film.json --public-dir=public_slim --concurrency=4
```

---

# 12. props 定義と型（CLAUDE.md §4）

```ts
export type OpeningTekohProps = {
  title: string;      // 主役タイトル。1文字ずつスタッガーで切れ上がる
  subtitle: string;   // サブタイトル。UPPERCASE 表示（facts_lock 検査対象）
  accent: string;     // アクセント（HEX6桁・"#"込み）。グリッド/署名の光/グロー/下線/ロゴに波及
  hasLogo: boolean;   // true で左上にロゴバッジ
};
```
**EP44 の確定 props（`remotion/props/tekoh.json`）:**
```json
{ "title": "THE WORDS THEY NEVER READ YOU", "subtitle": "VEGA V. TEKOH", "accent": "#2FA6A0", "hasLogo": true }
```
**量産用 `remotion/props/tekoh_short.json`:**
```json
{ "title": "THE WORDS THEY NEVER READ YOU", "subtitle": "CAN YOU SUE THE OFFICER?", "accent": "#2FA6A0", "hasLogo": false }
```
> `accent` は **`#2FA6A0` 固定**（EP43 amber / EP42 blue / EP41 gold の流用は BLOCKER）。`subtitle`/`title` は `facts_lock` 検査対象（「Miranda is dead」「9-0」「原被疑事実」を出さない。`VEGA V. TEKOH`・疑問形 `CAN YOU SUE THE OFFICER?` は制度説明として可・C1/C5）。

---

# 13. 受入基準（EP44 の Definition of Done・★語数ゲートが最初・全編アイボール必須）

```bash
cd C:\Users\aab15\Documents\prime-documentary
# 0. 語数（最優先・課金前）
./.venv/Scripts/python.exe scripts/check_script_length.py episodes/PD-2026-044-tekoh/03_script/script.en.v001.md --json
# 1. 事実性（EP44固有・§1.3・6制約）
./.venv/Scripts/python.exe scripts/check_tekoh_facts.py --json
# 2. ビート契約（AE↔figures 非重複）
./.venv/Scripts/python.exe scripts/validate_tekoh_beats.py
# 3. 密度（★31 を Remotion 側で満たしていること・--ep 指定／--json は出力パス）
./.venv/Scripts/python.exe scripts/check_motion_density.py --ep PD-2026-044-tekoh --json runs/qc/tekoh_motion.json
# 4. VO速度（ナレ直後・ミックス前）
./.venv/Scripts/python.exe scripts/measure_vo_wpm.py --ep tekoh --json
# 5. 最終受入
./.venv/Scripts/python.exe scripts/check_final_acceptance.py 44 --render episodes/PD-2026-044-tekoh/08_edit/tekoh_final_bgm.v002_ae.mp4 --emit-receipt
```
> **ゲート入力は `--ep PD-2026-044-tekoh`。`--json <film.json>` を入力に使わない**（出力パス＝上書き事故。ブリーフ§5）。

| ゲート | 閾値 | EP44 設計値 |
|---|---|---|
| `check_script_length` | band 内 | 2,139語（SPEC・band 2,100–2,141・要 PASS 確認） |
| `runtime_band` | 690–750s | **733.1s = 12:13.1**（上限 750s に 16.9s 余裕） |
| `motion_density` | ≥2.5/min ∧ cov ≥0.25 ∧ variety ≥3 | **3.08/min / 0.308 / 10種**（film.json 37 beats・AE非依存・floor 31 に +6・**dochighlight 0**） |
| `animation_mix`（紙芝居） | still-share ≤45% ∧ motion cov ≥45% | **44.69% / 55.31%** |
| `check_asset_reuse` | first-use ≥0.70・still≤2・factory1・motion≤2 | **0.8584 / 2 / 1 / 2** |
| `footage_diversity` | distinct/total ≥0.40 | **0.8584** |
| `visual_asset_qc` | 全 factory 目視 reviewed | **93本 目視（CODEX_A）** |
| `image_resolution` | 長辺≥3840 | 全 SDXL ≥3840 |
| `bgm_present` | 無音>25秒ゼロ | 最長 2.0秒 |
| `caption_integrity` | 一致≥99%・カバー≥95% | §8.2 |
| `op_ed_bookends` | `BrandOpening`/`BrandEndcard` import・不変 | ✓ |
| `asset_manifest` | A↔B counts/role 一字一致・also_thumb 6（{S02,S04,S24,S44,S45,S85}）・overlay 12 | §5.8 |
| `facts_lock`（EP44固有・6制約） | violations=0 | §1.2/§1.3 |
| **全編アイボール** | 12:13.1 を通しで目視 | ★1フレーム判定禁止（EP39-41 の miss・原被疑事実の非露出も全編目視で確認） |

---

# 14. premortem（失敗するとしたらここ）

| # | 失敗モード | 事前対処 |
|---|---|---|
| 1 | **番号ズレ**（別番号を発明） | シーンは S01..S48 固定（§3.2）。still 資産 ID S01..S85 と narrative S01..S48 を cross-map しない |
| 2 | **紙芝居**（still-share 45%超・余裕 0.31%pt） | §5.1 で still-cut 101 固定・factory 93・i2v 32。still1つ増で 45% 割れ → cut を増やさず同一シーンの別シードで回復 |
| 3 | **バリエーション水増し**（`--variants 3` を書く） | §5.3。variants 指定なし＝1枚。ai_prompts は 85行＋i2v16＝101 |
| 4 | **密度 FAIL**（AEカードに頼る） | §7。film.json に 37 beats（31 超）。AE 8枠は composite 後で非カウント |
| 5 | **画像プロンプトが読めない**（0枚生成） | §9.1 の2行形式・`--only S01` で `shots=101`（body 85 + i2v種 16）確認 |
| 6 | **ファイル名信仰**（牛が本編に入る） | §5.4 factory 93本を `build_footage_contact_sheet.py` で全点目視（CODEX_A BLOCKING）・病院クリップの患者写り込み目視排除 |
| 7 | **6制約違反**（Miranda廃止断定/9-0化/Vega が Miranda 覆滅/§1983一般 no immunity/★原被疑事実の露出/顔・肖像） | §1.2/§1.3 `check_tekoh_facts.py`。カード・figures・字幕・プロンプト・タイトル・概要欄 全対象 |
| 8 | **★dochighlight で黒バー（バグに見える）／FigureBeats kind 大文字で無音描画／`comparebars` 非実在** | §7.2 kind は全小文字・**dochighlight を1枠も使わない**（grep 0）・`compbars`（`comparebars` は存在しない） |
| 9 | **AE em-dash 豆腐 / 等速 / OM名英語 / 文字切れ** | §6.6。テキスト幅は `sourceRectAtTime(t,false).width` 実測 |
| 10 | **id 誤り**（切り詰め・綴り違い等） | §0.1。`id="Ep44Tekoh"`・`caseFilmDurationInFrames(tekohFilm,30)`=21993 |
| 11 | **accent 流用**（EP43 amber を残す） | §0.5/§12。OP props/AEカード/サムネ accent は `#2FA6A0` |
| 12 | **A↔B マニフェスト不整合**（role=thumb を作る/counts 不一致） | §5.8。`stills[].role` enum=`body/i2v_source/reject`・also_thumb 6（{S02,S04,S24,S44,S45,S85}）・overlay 12 を A/B 一字一致 |
| 13 | **EP39/40/41/42/43 と素材被り** | §2 で5つの stock_ledger の sha256 を除外 |
| 14 | **fast端で 11分台 / 750s 超** | §4.1 speed 1.0 明示＋`measure_vo_wpm` 168–190・190超は破棄再発注。総尺 733.1s ≤750 の assert（§3.1[4]） |
| 15 | **★6-3 を早出し**（HOOK/OPENING に得票） | §1.2 C2 / §7.3.7 / §6.3[6]。得票 6-3 は ACT3 まで画面・カード・figures に出さない（台本構造ロック） |

---

# 15. 設計パッケージ接続（DESIGN → CODEX_A / CODEX_B）

- **DESIGN（本書）:** タイムライン（0〜720.6s 全区間・各Act）・レイヤー（背面4層）・モーション数値・48絵コンテ・FigureBeats 設計（≥31・小文字kind・変種≥3・**dochighlight 不使用**）・AEカード表（accent #2FA6A0・8枠）・OP 仕様・asset_manifest スキーマの正（§5.8）。
- **CODEX_A（別ファイル `EP44_tekoh_CODEX_A_ASSETS.v001.md`・FROZEN）:** §9 を **85本の固有プロンプト**（1シーン1枚・variants 0）＋ i2v 16 ＋ factory 93 選定＆**全点目視QC**（`select_tekoh_factory.py`・`--exclude-used` で EP39/40/41/42/43 sha256 除外）＋境界契約 `asset_manifest.v001.json`（schema `tekoh_assets.v1`・counts still_body85/still_i2v_source16/motion16/factory93/overlay12・`stills[].role` enum=`body/i2v_source/reject`・also_thumb 6（{S02,S04,S24,S44,S45,S85}）・overlay 12）。still 資産 ID S01..S85・i2v M01..M16。
- **CODEX_B（別ファイル `EP44_tekoh_CODEX_B_BUILD.v001.md`）:** `build_tekoh_film.py`（＝`build_caniglia_film.py` を複製・ASSET_MAP/NARR/FACTORY_SEL/SLUG/EP を tekoh に）／captions（実測 narration）／figures 34＋graphics 3（小文字 kind・**dochighlight 不使用**・§7）／`CaseFilm` を `id="Ep44Tekoh"` で Root.tsx 登録（`caseFilmDurationInFrames`＝21993）／`OpeningTekoh`／AEビルダ・コンポジタ（accent #2FA6A0・.aep>.jsx assert・レイアウト名は実装済み8種のみ・§6.3 の8枠デッキと一字一致）・`validate_tekoh_beats.py`・`check_tekoh_facts.py`（EP43 版を複製・同名）／`build_tekoh_bgm.py`→`composite_tekoh_hero.py`（film_offset_sec 適用）／レンダ（`--public-dir=public_slim --concurrency=4`）／全ゲート（`--ep PD-2026-044-tekoh`）／完成後の全編アイボール。
- **A↔B 接続点は `asset_manifest.v001.json` ただ1ファイル**（schema `tekoh_assets.v1`・counts/role enum を A/B 一字一致・§5.8）。
- **複製元（実在・EP43）→ tekoh 複製先:** `build_caniglia_film.py`→`build_tekoh_film.py` / `build_caniglia_bgm.py`→`build_tekoh_bgm.py` / `ae/build_caniglia_hero_jsx.py`→`ae/build_tekoh_hero_jsx.py` / `ae/composite_caniglia_hero.py`→`ae/composite_tekoh_hero.py` / `validate_caniglia_beats.py`→`validate_tekoh_beats.py` / `check_caniglia_facts.py`→`check_tekoh_facts.py`。**共有（複製不要）:** `generate_sdxl_4k.py` / `build_footage_contact_sheet.py` / `check_motion_density.py` / `measure_vo_wpm.py` / `check_script_length.py` / `check_final_acceptance.py`。**実在しないスクリプトを捏造しない。**
