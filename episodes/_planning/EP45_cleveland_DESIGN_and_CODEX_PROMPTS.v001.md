# EP45 — THE PRICE OF BEING POOR — 制作設計書（DESIGN 本体・v001・確定台本版）

- Episode ID: `PD-2026-045-cleveland` / slug: `cleveland` / EP45
- 中心の問い（英語・二人称・★"合法"と書かない）: **"Can they lock you inside a cell for the one reason that you do not have the money?"**
- 判例（制度説明としてのみ）: **Bearden v. Georgia, 461 U.S. 660 (1983)**（decided 1983-05-24・opinion **Justice O'Connor**・第14修正 due process＋equal protection の収斂）。先行線 **Williams v. Illinois, 399 U.S. 235 (1970)** / **Tate v. Short, 401 U.S. 395 (1971)**。
- 主役: **Harriet Cleveland**（Montgomery, AL・存命の私人＝**R2**）。象徴のみ・尊厳の物語。**顔・肖像・身体を一切描かない。** Bearden 本人・Hub Harrington 判事・O'Connor も人物化しない。
- 主題: 払えない罰金を理由とする投獄は Bearden(1983)以降 **憲法違反（違法）**。本作は「合法だ」と決して言わない。**"1983以降 違憲なのに実務で続いた（enforcement failure）"** が背骨。**Bearden＝最高裁の線。Cleveland の救済は下級審の訴訟＋2014和解であって最高裁判決ではない。**
- Status: **BINDING**。**唯一の真実 = 機械生成済み `EP45_cleveland_PRODUCTION_SPEC.v001.json`**。本書のあらゆる数値はそこからの転記で、手書きで発明していない。衝突したら SPEC が勝つ。
- このファイルは**設計パッケージ3分割**（DESIGN / CODEX_A / CODEX_B）の **DESIGN 本体**。共有ブリーフ `EP45_cleveland_DESIGN_BRIEF.shared.md` を単一の真実源とする。84本の SDXL プロンプト実体・i2v 16・factory 92 選定は **CODEX_A**、`build_cleveland_film.py`・captions・figures 実装・Root.tsx 登録・AEビルダ/コンポジタ・ゲートは **CODEX_B** に属す（本書は各所でポインタのみ示す）。

## ★このエピソードの唯一の真実（手書きで数値を発明するな）

`episodes/_planning/EP45_cleveland_PRODUCTION_SPEC.v001.json`（台本から機械生成・`scripts/build_production_spec.py`）。本設計書は SPEC を**人間可読な実装指示に翻訳しただけ**で、新しい数字を作っていない。

```
words_total          = 2,119
narration_seconds    = 713.9   （= 11.9分・[DESIGNED SILENCE 1..3] の実音無音を含む）@ wpm_used 178.1
scenes               = 48      （S01..S48・確定。増やすな減らすな）
total_cuts           = 224
still  distinct 84 / cuts 100 / mean 1.19 / cap 2   ← ★各1枚生成（バリエーション0）
factory distinct 92 / cuts 92 / mean 1.0  / cap 1   ← 在庫選抜・全点目視QC
motion distinct 16 / cuts 32 / mean 2.0  / cap 2
distinct_total       = 192
first_use_share      = 0.8571  （floor 0.70）
still_share_of_cuts  = 0.4464  （cap 0.45）
motion coverage      = (92+32)/224 = 0.5536  （floor 0.45）
MG beats_floor       = 30      （film.json 側 figures+graphics。AEカードは check_motion_density に数えられない）
beats_per_min_floor  = 2.5   /  variety_floor = 3
mean_shot_seconds    = 3.19   /  max_shot_seconds = 6.0
```

## ★★ 最重要の前提: 1シーン1枚・バリエーション0 ★★（ブリーフ§1）

- Codex の画像生成は高精度。**同一ショットの複数バリエーション（`_01/_02/_03`）を作らない。**
- `04_scenes/ai_prompts.v001.md` は **still 84本＝84行の固有プロンプト**（`generate_sdxl_4k.py` の `read_prompts()` 2行形式・各1枚）。**`--variants 3` は使わない**（`--variants 1` または variants 指定なし）。
- i2v モーション種は **16枚**（各1シード・これもバリエーション0）。
- 総生成画像 = **still 84 + motion seed 16 = 100枚（各1回）**。**factory 92 は生成ではなく在庫選抜**（全点目視QC・EP39〜44 と sha256 被りゼロ）。
- **still を増やして factory を削るな**（still-share 0.4464 は cap 0.45 に対し余裕 0.36%pt しかない）。

## ★EP39〜44 で踏んだ失敗＝本書が最初から潰す設計判断

| # | 失敗 | 本書での恒久対策 | 参照 |
|---|---|---|---|
| 1 | **番号ズレ**（別リストを発明） | シーンは **SPEC の S01..S48 に固定**。別番号体系を作らない | §3.2 |
| 2 | **紙芝居**（still 100% で animation_mix FAIL） | still-cut **100 固定**＋factory実写 **92**＋i2v **32**。still-share 44.64% ≤45% / motion cov 55.36% ≥45% を構造保証 | §5.1 |
| 3 | **バリエーション水増し** | **1シーン1枚・84本を各1枚**。variants 禁止 | §5・§9 |
| 4 | **画像プロンプトのパーサ非互換** | `read_prompts()` の**2行形式**。CODEX_A が `--only S01` で拾い数（100）を確認 | §9 |
| 5 | **ファイル名を信じた**（牛が documents） | factory 92本を `build_footage_contact_sheet.py` で**全点目視QC**（CODEX_A 必須・BLOCKING） | §5.4 |
| 6 | **AEカードを密度に数えた** | `check_motion_density` は film.json の `figures+graphics` だけ。**film.json 側に MGビート 30本以上**（本書は 36 設計）。AE は composite 後で 0 カウント | §6.1 / §7 |
| 7 | **一枚絵で完成判定**（EP39-41/EP3941 の眼球不足） | 全編アイボール必須（§13）。measured > estimated | §13 |
| 8 | **A↔B マニフェスト不整合** | asset_manifest は **A↔B で同一スキーマ・counts/role enum を一字一致**。role=`thumb`/`still_thumb` を作らない。サムネは `also_thumb=true` の body still 6枚 | §5.8 |
| 9 | **dochighlight のバグ見え**（3回指摘） | **`dochighlight` を figures に1件も入れない（grep 0・R-DOCHL）。** 書類/証拠は `lowerthird` で表す | §6.2/§7.3 |

---

# 0. 環境・Remotion設定（CLAUDE.md §0 準拠）

## 0.1 本編 `Ep45Cleveland` の Composition 設定（★本編の正・誤記注意）

| 項目 | 値 |
|---|---|
| `id` | **`Ep45Cleveland`**（Root.tsx に `CaseFilm` で登録。ブリーフ§5「composition id Ep45Cleveland」。**id の切り詰め・綴り違い・大文字化は誤記＝BLOCKER**） |
| 解像度 | **1920 × 1080** |
| `fps` | **30**（EP44 tekoh と同値を踏襲。フレームは全て `Math.round(30 × 秒)`・直書き禁止） |
| `durationInFrames` | **`caseFilmDurationInFrames(clevelandFilm, 30)` = 21792**（4項の実関数 `round(hookSeconds×30)+round(OPENING_SEC×30)+ceil(narrationSeconds×30)+round(ENDCARD_SEC×30)`・**hookSeconds=0**・§3.1[3] で算出。手書きで数値を入れず関数で算出する） |
| component | `remotion/src/compositions/CaseFilm.tsx`（既存の汎用 `CaseFilm` を再利用。`Bookends.tsx` の `BrandOpening`/`BrandEndcard` を **import**・fork 禁止） |
| data | `remotion/src/data/cleveland_film.json`（`scripts/build_cleveland_film.py` で再生成できる状態を保つ＝**git 未追跡**） |

**Root.tsx 登録（★ブリーフ§5・CODEX_B が実装）:**
```tsx
import {clevelandFilm} from './data/cleveland_film.json';
import {caseFilmDurationInFrames} from './lib/caseFilmDuration';
// ...
<Composition
  id="Ep45Cleveland"
  component={CaseFilm}
  width={1920} height={1080} fps={30}
  durationInFrames={caseFilmDurationInFrames(clevelandFilm, 30)}  // = 21792
  defaultProps={{film: clevelandFilm}}
/>
```
> **id は `Ep45Cleveland`**（切り詰め・綴り違い・先頭大文字化などは全て誤記。ブリーフ§5 の render 行 `Ep45Cleveland` が正）。

## 0.2 タイトルバンパー `OpeningCleveland` の Composition 設定（CLAUDE.md 正典部品準拠）

| 項目 | 値 |
|---|---|
| `id` | **`OpeningCleveland`** |
| 解像度 | **1920 × 1080** |
| `fps` | **60**（CLAUDE.md §0 の正典値。OP 単体は 60fps） |
| `durationInFrames` | **180**（= 3.0秒 @ 60fps） |
| component | `remotion/src/compositions/OpeningCleveland.tsx`（§11 全仕様） |

> `OpeningCleveland` は**独立したタイトルバンパー成果物**（`out/cleveland_opening.mp4`）。本編内 OP/ED の正典は `Bookends.tsx`（`BrandOpening` 3.50s / `BrandEndcard` 9.00s・不変）。`OpeningCleveland` を本編に ffmpeg で焼き込まない（オーナー承認なしに見え方を変えない）。

## 0.3 必要な依存パッケージ

```bash
cd C:\Users\aab15\Documents\prime-documentary\remotion
npm i @remotion/motion-blur     # CLAUDE.md 必須依存（Trail によるモーションブラー）
```

## 0.4 `remotion.config.ts`（CLAUDE.md §0 正典値・EP41〜44 と同一・書き換えない）

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

## 0.5 ブランド／レーン色（`remotion/src/brand.ts` から import・ハードコード禁止）

**EP45 のパレット（★督促の朱＝crimson・暖色ランプの労働者階級の台所＋冷たい灰色の郡拘置所 booking＋淡い大理石の裁判所・レーン分離）:**
```
INK    = #0A0A0C   ルート背景（サムネ bg と一致）
LAMP   = #17120E   暖いタングステンの台所（warm near-black・ordinary paper が積もる側）
MARBLE = #34363B   最高裁の冷たい大理石（ACT3・Bearden の線）
STEEL  = #24262A   booking の冷灰・institutional（無人）
ACCENT = #B23A48   ★crimson（督促状の朱／overdue の一点差し色）。ブランド数値・ライン・下線・グロー・OP/AE/サムネ accent。★EP41 gold / EP42 blue / EP43 amber / EP44 teal を流用しない
WHITE  = #F5F7FA
SILVER = #C8CDD6   （AI開示テキスト）
```
> **レーン分離:** EP41 gold（鋼灰institutional）/ EP42 blue（夜のシカゴ）/ EP43 amber（porch-amber の玄関灯）/ EP44 teal（clinical hospital）と被らないよう、EP45 は **暖いランプ下の台所 near-black `#17120E` ＋ 冷たい大理石 `#34363B` ＋ booking の冷灰 `#24262A` を基調＋唯一の暖色差し＝督促の朱 crimson `#B23A48`**。接尾に `porch-amber` `warrant-blue` `teal-green hospital` `sodium prison corridor` を含めない。**factory は EP39〜44 の `stock_ledger*.json` の sha256 を除外**（CODEX_A・BLOCKING）。**CODEX_B は OP props / AEカード / サムネ accent を必ず `#B23A48` にする（他話色の流用は BLOCKER）。**

---

# 1. 事実の取り扱い（★正確性6制約＝FACTS LOCK / `check_cleveland_facts.py`・BLOCKING）

## 1.1 確定台本（唯一の正・1バイトも変えない）

```
C:\Users\aab15\Documents\prime-documentary\episodes\_planning\EP45_cleveland_script.en.v001.md
```
**本番配置先:** `episodes/PD-2026-045-cleveland/03_script/script.en.v001.md`（上記を1バイトも変えずコピー）。整形も禁止（AI臭再発と語数ゲート再計算を招く）。台本の幕構成（HOOK / OP / ACT1–3 / ENDING）と `【DESIGNED SILENCE …】`（**3箇所**）を正典とする。存在しない演出マーカー（`【OST:】`）を発明しない。台本の `〔CARD: … confidence: medium〕` 注記は数値のヘッジ根拠であって画面カードの命令ではない。

## 1.2 ★正確性6制約（全出力＝プロンプト・カード文言・図表・字幕・タイトルに適用。1つでも違反＝BLOCKER）

| # | 制約 | 出力での順守 |
|---|---|---|
| **C1** | **「合法(legal/lawful)」と言わない** | 払えないだけの投獄は Bearden(1983)以降 違憲（違法）。主題は "違法なのに実務で続く(enforcement failure)"。**「debtors' prison is legal/lawful」「jailing the poor is legal」を出さない。** 同時に**「もう完全に無くなった／どこでも廃止された(gone/abolished everywhere/no longer exists)」も禁止**（誤り）。許容: "unconstitutional since 1983" / "yet it continued" / "the rule held" / "still stands" / "enforcement failure" / "a lower-court settlement in 2014" |
| **C2** | **Bearden＝最高裁の線 / Cleveland＝下級審和解** | Bearden(1983)は最高裁。Cleveland の救済は**下級審の訴訟＋2014和解**であって最高裁判決でない。**「Supreme Court saved/freed/rescued Cleveland」「Cleveland won/reached the Supreme Court」を書かない。** Cleveland の救済は "a lower court / an ordinary lawsuit / a settlement announced in late 2014" と表す |
| **C3** | **Bearden の holding を正確に** | 収監前に「支払い能力（willful refusal か genuine inability か）」と「代替手段（punishment short of a cell）」を検討する義務。Bearden は罰金・手数料・賠償**そのものを禁じていない**。**「all/every/any fines are unconstitutional」「banned all fines」に過大化しない。** 閉じたのは「能力がないだけでの収監」だけ |
| **C4** | **Harriet Cleveland ＝ R2・象徴のみ** | 存命の私人。**顔・肖像・身体を描かない**。象徴のみ（督促状の束・伏せた免許証・空の財布・留置場の扉/booking の時計・支払台帳・請求書・裁判所の長い廊下・バス停・空席の弁護人席）。**家庭・子どもを扇情化しない・尊厳をもって（poverty porn 禁止）。** 泣く人・嘆く家族・困窮の煽情描写を作らない |
| **C5** | **制度・営利保護観察(JCS)を説明・特定個人を攻撃しない** | JCS（Judicial Correction Services）は制度として象徴で示す（台帳・請求書・ゴム印・skim）。Harrington 判事の公開判決の逐語引用は可（AE カード＝B の担当）だが、**画像で個人を攻撃・同定しない** |
| **C6** | **数値は台帳一致・捏造ゼロ** | $1,554 / 31日 / $200月 / $40がJCS / 約38,000人・4州 は原典一致。confidence:medium のもの（$1,554・31日・$200/$40・能力審問なし・免許停止の連鎖・弁護人告知なし）は **FFJC 帰属＋ヘッジを維持**。**投票数（票割れ）を発明しない**（Bearden の票数は台帳に無い＝votetally 不使用） |
| **R1** | **実在人物の顔・肖像を生成しない** | 全生成ビジュアル表示中は `AI-assisted visualization`（右下）常時表示。概要欄に1行 AI 開示 |

## 1.3 6制約ゲート `check_cleveland_facts.py`（`scripts/check_cleveland_facts.py`＝EP44 `check_tekoh_facts.py` を cleveland 用に複製。exit≠0 で出荷停止・CODEX_B 実装。出力 `facts_lock.v001.json`）

> **★ゲート名は1本に確定:** 6制約の機械ゲートは **`scripts/check_cleveland_facts.py`**（出力 `09_package/facts_lock.v001.json`）ただ1つ。**DESIGN / CODEX_A / CODEX_B で同名参照**（`*_accuracy`・`*_facts_check` 等の別名を作らない）。下表の **L-C1..L-C6・L-R1** は内部ルール **R-*** に一本化して実装する（対応: L-C1→R-LEGAL/R-FORBID / L-C2→R-SCOTUS-SPLIT / L-C3→R-BEARDEN-SCOPE / L-C4→R-FACE/R-CLEVELAND / L-C5→R-ATTRIB / L-C6→R-LEDGER/R-HEDGE、加えて **R-DOCHL**）。

**検査対象:** `03_script/script.en.v001.md` / `remotion/src/data/cleveland_film.json` の `figures[].kind`・`figures[].*text*`・`quote`・`attribution`・`lines[]`・`label` / `08_edit/ae_hero/beats.json` の `hero`/`top`/`bottom`/`sub`/`attribution`/`caption` / `09_package/description.txt` / `remotion/props/cleveland*.json` の `subtitle`/`title` / `04_scenes/ai_prompts.v001.md`。

| ルール | 内容 |
|---|---|
| **L-C1 合法化禁止（R-LEGAL / R-FORBID）** | `debtors'? prison (is/are/was) (legal/lawful)` / `(legal/lawful) to (jail/imprison/lock ?up)` / `jailing the poor is (legal/lawful)` / `(all/every/any) fines? (are/is/were) unconstitutional` / `banned all fines` / `gone/abolished everywhere/no longer exists/a thing of the past/completely (ended/eradicated)` が出たら FAIL。**`unconstitutional` を含む payload には `yet it continued`/`still`/`the rule held`/`enforcement` のいずれかが同一 payload に無ければ FAIL** |
| **L-C2 SCOTUS 分離（R-SCOTUS-SPLIT）** | `(supreme court/scotus/nine justices) (saved/freed/rescued/ruled for) (harriet )?cleveland` / `cleveland (won/reached/went to) the supreme court` が出たら FAIL。`Cleveland` の relief 記述の近傍に `lower court`/`settlement`/`2014`/`not the Supreme Court` のいずれかが無ければ FAIL |
| **L-C3 Bearden 射程（R-BEARDEN-SCOPE）** | `Bearden` の近傍に `banned all fines`/`all fines unconstitutional`/`fines themselves are unconstitutional` が出たら FAIL。`won't pay` と `can't pay` を対比する payload に**両方**が無い（片方だけで断ずる）と WARN→FAIL |
| **L-C4 肖像／Cleveland 尊厳（R-FACE / R-CLEVELAND）** | `ai_prompts` 正プロンプトに `portrait`/`face of`/`likeness`/`recognizable`/`Harriet Cleveland`（人物として）/`nude`/`her body` が出たら FAIL（ネガティブ使用は可）。`poverty ?porn`/`starving child`/`crying child`/`weeping family` が出たら FAIL。`Cleveland` の直後60字に `face`/`portrait`/`depicted as a woman` が出たら FAIL |
| **L-C5 帰属（R-ATTRIB）** | `quote` は逐語のみ。`quote[].attribution` が空、または §2 `APPROVED_QUOTES` の帰属（`Justice O'Connor, for the Court` / `Judge Hub Harrington, 2012`）と不一致なら FAIL。要約を引用符に入れたら FAIL |
| **L-C6 台帳／ヘッジ（R-LEDGER / R-HEDGE）** | 画面文字列に §1.4 の表以外の数値（例 `$580,000`）が出たら FAIL。`$1,554`/`31`/`$200`/`$40` を含む payload に `Fines and Fees`/`FFJC` の帰属が同一 payload に無ければ FAIL。**投票数（`\d ?- ?\d` の得票形）が figures/AE に出たら FAIL（台帳に無い）** |
| **R-DOCHL（★EP45 固有）** | `figures[].kind == "dochighlight"` が **1件でも**存在したら FAIL（`grep -c '"dochighlight"'` が 0 でないと出荷停止）。`comparebars` も非実在→出たら FAIL（`compbars` が正） |
| **L-R1 開示（R-DISCLOSE）** | `description.txt` に AI 開示1行が無ければ FAIL。全生成ビジュアル区間で右下 `AI-assisted visualization` が焼かれていること（§13 アイボールで確認） |

**出力:** `09_package/facts_lock.v001.json`（`{"pass":bool,"violations":[{"file","rule","line","excerpt"}],"skipped":[...]}`）。`pass:true` でない限り `check_final_acceptance.py` に進まない。

## 1.4 画面に出してよい確定数値（★台本／事実対応表 C01–C26 に存在するものだけ。この表以外を画面に出すな）

| ID | 値 | 台本での表現（claim） | conf | 使用先 |
|---|---|---|---|---|
| N01 | **$1,554 OR 31 DAYS** | "Pay one thousand five hundred and fifty-four dollars, or serve thirty-one days"（C13） | **medium** | AE **d01**（MONEY_STACK・**FFJC 帰属必須**）/ figures `stat`（F11） |
| N02 | **NO HEARING** | "There was no hearing on what she had"（C14） | medium | AE **n01**（CENTER_STACK）/ figures `kinetic:emphasis`（F12） |
| N03 | **BEARDEN v. GEORGIA, 461 U.S. 660 · MAY 24, 1983** | 台本カード（C01）／"in 1983 the Court ruled in his favor" | high | AE **t01**（DATE_STAMP）/ figures `lowerthird`/`timeline`（F01） |
| N04 | **O'Connor 逐語** "…it may not thereafter imprison a person solely because he lacked the resources to pay it" | "Justice O'Connor wrote the opinion"（C08/C09） | high | AE **q01**（QUOTE_CARD・帰属 O'Connor）/ figures `quote`（F07） |
| N05 | **$200 / MONTH → $40 TO JCS** | "two hundred dollars a month. Of that … forty dollars … to the company"（C15） | **medium** | AE **c01**（MONEY_STACK・**FFJC 帰属必須**）/ figures `compbars`/`stat`（F13/F19） |
| N06 | **~38,000 · 4 STATES** | "roughly thirty-eight thousand people were on that company's rolls across four states"（C22） | high | AE **s01**（CENTER_STACK）/ figures `stat`（F20） |
| N07 | **UNCONSTITUTIONAL SINCE 1983**（+sub "YET IT CONTINUED"） | "declared unconstitutional in 1983 … The rule held"（C19） | medium | AE **u01**（CENTER_STACK）/ figures `lowerthird`（F17） |
| N08 | **SETTLED 2014**（A RIGHT / A REMEDY・sub: 下級審・最高裁でない） | "a settlement, announced in late 2014 … never reached the Supreme Court"（C18） | high | AE **w01**（SPLIT_COMPARE）/ figures `lowerthird`/`timeline`（F16） |
| N09 | **WILLIAMS 1970 · TATE 1971** | 台本カード（C10/C11） | high | figures `timeline`（F08/F09・AEカードにはしない） |
| N10 | **JCS · founded 2001 · Georgia** | 台本カード（C20） | high | figures `lowerthird`（F18・AEカードにはしない） |
| N11 | **"a judicially sanctioned extortion racket"** | Hub Harrington 逐語（C23） | high | figures `quote`（F21・帰属 Harrington 2012） |
| N12 | **$500 FINE + $250 RESTITUTION**（Bearden 事実） | "a five hundred dollar fine and two hundred and fifty dollars in restitution"（C07） | high | figures `lowerthird`（F06・AEカードにはしない） |

> **★AE カード文言に「合法だった」「全罰金違憲」「最高裁が Cleveland を救った」を書かない（C1/C2/C3）。** `$1,554/$200/$40` を焼く AE/figures は**同一 payload に "PER THE FINES AND FEES JUSTICE CENTER"（FFJC）帰属を必ず持つ**（R-HEDGE・medium 単一出典）。**461 U.S. 660 / 399 U.S. 235 / 401 U.S. 395 の判例番号は t01（DATE_STAMP の place）と figures `lowerthird` に退避**（本文で読み上げない・台本の音声からは抜いてある）。**投票数を発明しない・988 は出さない（本作は自殺配慮テーマでなく債務投獄・R-NO988）。**

---

# 2. 視覚・音響レーン分離（EP39〜44 との素材被り回避）

> **EP39〜44 のファイルには一切触れない（読み取りのみ可）。** レーンを機械的に分離する。

| 軸 | EP44 tekoh | **EP45 cleveland** |
|---|---|---|
| 舞台 | clinical hospital corridor → 法廷 | **暖いランプ下の労働者階級の台所（督促状の束・伏せた免許証・空の財布）→ 冷灰の郡拘置所 booking（無人・鉄格子/独房を描かない）→ 淡い大理石の裁判所の長い廊下・空席の弁護人席 → アラバマの陽炎の空き道路とバス停 → 夜明けの採光** |
| 時間帯 | teal 冷光 | **暖いタングステン（台所）→ 冷灰の booking → 冷たい大理石（ドクトリン核）→ 陽炎の日中（車社会の孤立）→ 夜明けの採光** |
| 支配的出来事 | Miranda/自白 | **罰金の雪だるま→能力審査なしの収監・営利保護観察JCS の $40 skim・counsel 不在・Bearden 判例核・下級審和解(2014)・SPLC RICO 提訴→JCS 閉鎖** |
| アクセント色 | teal（EP44） | **crimson `#B23A48`（督促状の朱・唯一の暖色差し）** |
| ベース色 | teal + 大理石 | **暖い near-black `#17120E` + 冷たい大理石 `#34363B` + booking 冷灰 `#24262A` + near-black `#0A0A0C`** |
| レンズ感 | — | **HOOK 象徴モンタージュ（~2s cut）／ACT1 最短・現在形・抑制／ACT2 正対の転回（制度）／ACT3 正対対称・荘厳・最も遅い／ENDING 引き（pull-back）** |
| 画像保存先 | `H:\pd-media\assets\ai\tekoh\` | **`H:\pd-media\assets\ai\cleveland\`** |
| Remotion データ | `tekoh_film.json` | **`cleveland_film.json`** |
| Remotion コンポ | `Ep44Tekoh` | **`Ep45Cleveland`** |
| AE 作業ディレクトリ | `…/PD-2026-044-tekoh/08_edit/ae_hero/` | **`…/PD-2026-045-cleveland/08_edit/ae_hero/`** |

**素材被り禁止:** EP39〜44 と同一の factory clip / AI画像を1点も使わない。選定前に `episodes/PD-2026-039-*/`〜`…-044-*/` の `05_stock/stock_ledger*.json` を読み sha256 重複を除外（CODEX_A・BLOCKING）。

---

# 3. 尺と構成 — SPEC の値をそのまま使う

## 3.1 全区間タイムライン（★この表が唯一の正・秒は fps=30 から算出しフレーム直書き禁止・0〜713.9s 全区間）

**算出基準:** SPEC の `narration_seconds = 713.9`（マスター）を `cleveland_film.json` の `narrationSeconds` に入れる。**手計算で上書きしない。** SPEC は BODY を1ブロック（1,511語 / 509.0s）でのみ与える。ACT1/ACT2/ACT3 の内訳は**確定台本の語数シェアから導出**（下表・BODY 合計は SPEC 値に一致）。フレーム = `Math.round(30 × 秒)`。

| # | ブロック | 役割 | 語数 | 幕秒 | 台本指定の沈黙 | 固定尺 | 開始f | 終了f |
|---|---|---|---|---|---|---|---|---|
| 1 | **HOOK** | `hook` | 73 | 24.6（SPEC） | **1.8**（"door standing shut" で保持→hard cut） | — | 0 | 738 |
| 2 | **BrandOpening** | `opening` | 0 | — | — | **3.50** | 738 | 843 |
| 3 | **OP ナレ** | `opening` | 64 | 21.6（SPEC） | — | — | 843 | 1491 |
| 4 | **ACT1** The road that ends at a cell | `body` | 386 | 130.0（導出） | **1.5**（"booking clock, second hand moving" で保持） | — | 1491 | 5391 |
| 5 | **ACT2** The machine that turns a debt into a sentence | `body` | 594 | 200.0（導出） | — | — | 5391 | 11391 |
| 6 | **ACT3** Bearden, right vs remedy | `body` | 531 | 179.0（導出） | — | — | 11391 | 16761 |
| 7 | **ENDING**（payoff→CTA） | `ending` | 412 | 138.8（SPEC） | **2.2**（"a door opening onto daylight" ＝sound-forward の最長沈黙） | — | 16761 | 20925 |
| 8 | **BrandEndcard** | `ending` | 0 | — | — | **9.00** | 20925 | 21195 |

> **BODY 内訳の導出（★語数シェア・SPEC BODY 1,511語 / 509.0s を厳守）:** ACT1 386語→130.0s / ACT2 594語→200.0s / ACT3 531語→179.0s（合計 1,511語 / 509.0s）。ACT3 が最も遅い（doctrinal core・Bearden の荘厳）。**この内訳は planning アンカー。final は `measure_vo_wpm` 実測が権威**（CODEX_B は実測秒で `cleveland_film.json` の各 segment 秒を更新）。
> **フレーム列**は BrandOpening(105f)/BrandEndcard(270f) を実尺で挟み、幕秒を順に `round(30×秒)` で積んだ実装用アンカー。**幕秒積算 nominal 21195 と §3.1[3] の `caseFilmDurationInFrames` 出力 21792 の差 597f=19.9s は、narrationSeconds マスター 713.9 と発話幕秒合計 694.0 の差＝息継ぎ＋設計無音3点（1.8+1.5+2.2=5.5s）を内包する測定マスター。** film.json には 713.9 を入れる。CODEX_B は `cleveland_film.json` の segment 順から再計算し一致を確認。

### 検算（CODEX_B は必ず自分で再計算して一致を確認）

```
[1] narrationSeconds = 713.9（SPEC マスター。手計算で上書きしない）
    ※ 発話ブロック HOOK..ENDING の幕秒合計 = 24.6+21.6+509.0+138.8 = 694.0s。
      SPEC マスター 713.9 との差 19.9s は、幕間の息継ぎ＋設計無音3点（1.8+1.5+2.2=5.5s）を内包した測定マスター。
    ※ mean_shot 検算: 713.9 / 224 = 3.187s ＝ SPEC mean_shot_seconds 3.19 一致（224カットは 713.9s 全域に張る）。

[2] 総尺 = hookSeconds 0 + BrandOpening(OPENING_SEC) 3.50 + narrationSeconds 713.9 + BrandEndcard(ENDCARD_SEC) 9.00
        = 726.4 秒 = 12:06.4
    ※ hookSeconds=0（HOOK ナレは narrationSeconds 713.9 に内包・別建ての hook teaser preroll は作らない）。
       台本 OPENING は「Gold BrandOpening after the hook, not at frame zero」＝HOOK ナレ→BrandOpening→OP ナレ の順。

[3] caseFilmDurationInFrames(clevelandFilm, 30) = 4項の実関数で算出（round(30×726.4) という単項近似ではない）:
      = round(hookSeconds×30) + round(OPENING_SEC×30) + ceil(narrationSeconds×30) + round(ENDCARD_SEC×30)
      = round(0×30)=0 + round(3.5×30)=105 + ceil(713.9×30)=ceil(21417.0)=21417 + round(9.0×30)=270
      = 21,792 フレーム
    ※ CODEX_B は cleveland_film.json の hookSeconds/narrationSeconds（＋Bookends の OPENING_SEC/ENDCARD_SEC）から
      同関数で再計算し 21792 に一致することを assert する（§5.1・§3.1 検算）。

[4] runtime_band ≤ 750s の assert（BLOCKING）:
    総尺 = hookSeconds 0 + 726.4 = 726.4s
    → 726.4s = 12:06.4 は band 690–750（11.5–12.5分）の内側（上限 750s に対し 23.6s の余裕）    ✓ PASS
    ※ hookSeconds を 0 超（teaser 採用）にする場合は round(hookSeconds×30) を [3] に加え、
      総尺 = 726.4 + hookSeconds を再検算して **≤ 750s** を再確認すること（BLOCKING）。
```
> **VO 実測で確定:** `measure_vo_wpm`（合格帯 168–190 wpm）でナレ実測。実測が SPEC マスターと乖離したら CODEX_B は `narrationSeconds` を実測値で更新（planning は 713.9・final は実測が権威）。190超は破棄・speed 0.95 で再発注（BLOCKING）。

## 3.1b 秒×アニメーション・タイムライン（★0→713.9s 全区間・各beat の start/end フレーム・移動量・easing・damping・stagger・Trail）

> **フレームは全て `f(sec)=Math.round(30×sec)`。等速線形ゼロ・opacity 単独ゼロ・静止フレームゼロ。** 下表は各 narrative シーン（§3.2 の S01..S48）の主アニメを示す。カット境界は `QUANT=f(0.5)=15f` グリッドにスナップ（§10.1）。still は Ken Burns（`scale 1.00→1.08`＋drift ±24px・`Easing.out(Easing.cubic)`）を全長。テキスト見出し/figures は `overflow:hidden` 親＋子 `translateY(110%→0)` の spring 切れ上がり（`damping:16,mass:1`・スタッガー `f(0.04)=2f/文字`）を基本形。★fast move（Trail 対象）は「Trail」列に明記。

| 区間(秒) | 開始f–終了f | シーン | 主アニメ（プロパティ・移動量） | easing / damping | stagger | Trail |
|---|---|---|---|---|---|---|
| 0.0–4.5 | 0–135 | S01 督促状の束（HOOK 開幕・~2s cut） | still Ken Burns `scale 1.00→1.06` / drift +18px 右 | `Easing.out(Easing.cubic)` | — | — |
| 4.5–9.0 | 135–270 | S02 伏せた免許証（i2v M01: ゆっくり裏返る） | i2v native ＋ 追い足し `scale 1.00→1.03` | native + cubic | — | — |
| 9.0–13.5 | 270–405 | S03 空の財布（開いて空） | still `scale 1.00→1.07` / drift +20px | `Easing.out(Easing.cubic)` | — | — |
| 13.5–18.0 | 405–540 | S04 留置扉が閉じる（i2v M02: swing shut・**fast**） | i2v native ＋ 扉 swing・数値見出しなし | native | — | **✓** |
| 18.0–24.6 | 540–738 | S05 booking の壁時計（静止保持→沈黙 1.8s） | still `scale 1.00→1.04`・秒針は静止画の含意 | `Easing.inOut(Easing.sin)` 微動 | — | — |
| **24.6–28.1** | **738–843** | **BrandOpening 3.50**（Bookends・不変） | — | — | — | — |
| 28.1–39.3 | 843–1179 | S06 Montgomery の質素な通り（OP establishing・factory） | factory 内在動き＋微 KB `scale 1.00→1.04` | `Easing.out(Easing.cubic)` | — | — |
| 39.3–49.7 | 1179–1491 | S07 最高裁の大理石列柱（1983 の答え） | still push-in `scale 1.00→1.08` / drift +12px 上 | `Easing.out(Easing.cubic)` | — | — |
| 49.7–66.0 | 1491–1980 | S08–S09 ACT1: 平凡な切符→積もる束 | still KB・acttitle `THE ROAD THAT ENDS AT A CELL` 切れ上がり | spring `damping:16,mass:1` | 2f/文字 | figure kinetic reveal **✓** |
| 66.0–92.0 | 1980–2760 | S10–S13 免許停止→陽炎の空き道路→バス停 | still KB・"A FINE THAT SITS GROWS"（emphasisWords=["GROWS"]） | spring `damping:16` | 2f/文字 | numberticker桁 **✓** |
| 92.0–120.0 | 2760–3600 | S14–S15 車の鍵→保険→雪だるまの束 | still KB・drift ±24px 交互 | `Easing.out(Easing.cubic)` | — | — |
| 120.0–140.0 | 3600–4200 | S16 命令書（$1,554 or 31日）・stat F11 | figure `stat` value 1554→settle（**FFJC 帰属併記**）・count は ease-out | `Easing.out(Easing.cubic)` | — | tick **✓** |
| 140.0–150.0 | 4200–4500 | S17 空の弁護人席／能力審問なし・"NO HEARING" | `kinetic:emphasis` "NO HEARING" 切れ上がり（F12） | spring `damping:16` | 2f/文字 | **✓** |
| 150.0–153.0 | 4500–4590 | booking 扉が閉じる（i2v M05・**fast**）→沈黙 1.5s | i2v swing・`mechanism:closingdoor` | native | — | **✓** |
| 153.0–158.0 | 4590–4740 | S18 booking の時計（静止保持・沈黙 1.5s 実装） | still `scale 1.00→1.03` 微動・BGM mute | `Easing.inOut(Easing.sin)` | — | — |
| 158.0–200.0 | 4740–6000 | S19–S22 ACT2: 支払台帳・請求書（ロゴぼかし）・ゴム印 | acttitle `A DEBT BECOMES A SENTENCE`・still KB | spring `damping:16` | 2f/文字 | stamp i2v **✓** |
| 200.0–245.0 | 6000–7350 | S23–S24 offender-funded・$40 skim（compbars F13） | `compbars` items[$200,$40→JCS]（**FFJC label**）barX `scaleX 0→1` | spring `damping:18` origin left | — | — |
| 245.0–300.0 | 7350–9000 | S25–S27 counsel 不在（空席）・HRW 利益相反 | `lowerthird` primary/secondary `translateY 24px→0`＋opacity | spring `damping:20,mass:1` | — | — |
| 300.0–345.0 | 9000–10350 | S28–S29 約38,000・4州（stat F20）・100裁判所 | `stat` value 38000→settle・drift +16px | `Easing.out(Easing.cubic)` | — | tick **✓** |
| 345.0–358.0 | 10350–10740 | S30–S31 Harrington 逐語 "extortion racket"（quote F21） | `quote` maskslide＋attribution fade（帰属 Harrington 2012） | `Easing.out(Easing.cubic)` | 2f/語 | — |
| 358.0–375.0 | 10740–11250 | ACT2→ACT3 繋ぎ（factory ambient・長廊下） | factory 内在動き＋微 KB | `Easing.out(Easing.cubic)` | — | — |
| 375.0–390.0 | 11250–11700 | S32 ACT3 幕頭・古い法律書（Bearden） | acttitle `BEARDEN — A RIGHT AND A REMEDY` 切れ上がり | spring `damping:16` | 2f/文字 | **✓** |
| 390.0–430.0 | 11700–12900 | S33–S35 最高裁列柱・借入封筒（荘厳・最も遅い） | still push-in `scale 1.00→1.08`・長ディゾルブ 10f | `Easing.out(Easing.cubic)` | — | — |
| 430.0–470.0 | 12900–14100 | S36 Bearden 事実（$500+$250・F06）→O'Connor 逐語 quote F07 | `lowerthird`＋`quote`（帰属 O'Connor・逐語） | `Easing.out(Easing.cubic)` | 2f/語 | — |
| 470.0–500.0 | 14100–15000 | S37–S38 第14修正の光帯（i2v M12: 光が走る・緩）＋timeline 1970→1971→1983 | i2v native ＋ `scale 1.00→1.03`・`timeline` settle | native + cubic | — | — |
| 500.0–530.0 | 15000–15900 | S39–S40 "BEARDEN DID NOT ABOLISH FINES"（F05・compbars won't/can't） | `kinetic:emphasis`（emphasisWords=["NOT"]）＋`compbars` | spring `damping:16` | 2f/文字 | **✓** |
| 530.0–554.0 | 15900–16620 | S41–S42 Cleveland の命令が越えた線（faultsplit）→和解2014（F16・最高裁でない） | `mechanism:faultsplit`＋`lowerthird`（"not the Supreme Court"） | `Easing.out(Easing.cubic)` | — | line cross **✓** |
| 554.0–558.4 | 16620–16761 | S43 SPLC RICO→JCS 閉鎖（timeline 2014→2015・F16/F23） | `timeline` events settle | `Easing.out(Easing.cubic)` | — | — |
| 558.4–600.0 | 16761–18000 | S44 ENDING: 数字への回帰 "GO BACK TO THE NUMBER" | `kinetic`（emphasisWords=["NUMBER"]・数値は焼かず echo） | spring `damping:16` | 2f/文字 | **✓** |
| 600.0–660.0 | 18000–19800 | S45–S46 right vs remedy・"UNCONSTITUTIONAL SINCE 1983 / YET IT CONTINUED"（F17） | `lowerthird`（R-LEGAL 対語必須）・still KB | `Easing.out(Easing.cubic)` | — | — |
| 660.0–695.0 | 19800–20850 | S47 "THE RULE HELD"（enforcement failure）・棚の権利が部屋に入らない | `kinetic:emphasis`（["HELD"]）＋`mechanism:gears` | spring `damping:16` | 2f/文字 | **✓** |
| 695.0–697.2 | 20850–20916 | S48 開くドア→採光（i2v M16・pull-back・沈黙 2.2s・sound-forward） | i2v native ＋ slow `scale 1.00→1.02` pull-back・BGM mute | native + `Easing.out(Easing.cubic)` | — | — |
| 697.2–713.9 | 20916–21195相当 | CTA（"worth a like"）→ BrandEndcard 9.00 開始 20925 | 字幕のみ・**沈黙区間に字幕キューを置かない** | — | — | — |

> **★背面レイヤーは常に4層以上動く（§8.1）。** 上表の各 0.5s 境界で「動いている要素」が最低1つある（静止区間ゼロ）。Trail 対象（fast move）は **S04 留置扉 swing / booking 扉 closingdoor / ゴム印 stamp / numberticker・stat の桁 / faultsplit の線越え / 幕頭 kinetic・emphasis の切れ上がり**。**S05/S18 の時計・S33–S35 の荘厳 push-in・S37 の走光・S48 の夜明け pull-back・Ken Burns には Trail をかけない**（無駄な残像・扇情を避ける・C4）。

## 3.2 シーン→幕の割当（★SPEC の S01..S48 を固定・別番号を発明しない・48シーン）

各シーンは narrative beat。224カットを 48シーンに分散（平均 4.67カット/シーン）。`primary` は各シーンの主素材（still=SDXL 各1枚 / factory=実写 / motion=i2v）。ambient/繋ぎは factory を各シーンに撒く（§5.1）。**象徴のみ・6制約順守・Cleveland/JCS 非人物化。絵コンテ級の記述は §9。**

> **★2つの `Sxx` 名前空間は別物（取り違え禁止）:** 本節の **narrative シーンは `S01..S48`**（この表の絵コンテ）。一方 **still 資産 ID は `S01..S84`**（CODEX_A §2 注記・1プロンプト=1枚で48シーンに84枚を配分）。同じ `Sxx` 表記でも DESIGN §3.2/§9 の Sid（narrative）と CODEX_A/asset_manifest の scene_id・covers_scene_id（still 資産 ID）は指すものが異なる。横断参照時は「どちらの空間か」を明示し、cross-map しない。

| Sid | 幕 | 内容（象徴・6制約） | primary |
|---|---|---|---|
| S01 | HOOK | 輪ゴムで束ねた督促状の分厚い束・暖いランプ・手も顔もなし（積もる紙＝刑期の象徴） | still |
| S02 | HOOK | 台所に伏せて置かれた免許証（i2v: ゆっくり裏返る）＝仕事を探す手段を奪われる | **motion** |
| S03 | HOOK | 平置きで空の財布・中に何もない・暖いランプ | still |
| S04 | HOOK | 冷灰の booking で閉じる institutional の扉（i2v: swing shut・鉄格子/独房なし・**fast**） | **motion** |
| S05 | HOOK | booking の壁時計（静止保持・DESIGNED SILENCE 1.8s の画・hard cut で BrandOpening へ） | still |
| S06 | OP | 夜の Montgomery の質素な通り・小さな債務が始まった場所（establishing） | factory |
| S07 | OP | 最高裁の淡い大理石列柱・1983 に答えた court（正対・荘厳・遠い） | still |
| S08 | OP | 手前に朱の督促1通・奥に遠い最高裁列柱＝小さな債務から最高裁までの距離 | still |
| S09 | ACT1 | ワイパーに挟まった1枚の平凡な切符・紙の縁が朱（最もありふれた種類） | still |
| S10 | ACT1 | 束が太り新しい輪ゴムで再束＝座る債務が育つ（i2v: 束が増える・緩） | **motion** |
| S11 | ACT1 | 停止された免許証＋伏せた停止通知（判読不能・no face） | still |
| S12 | ACT1 | 陽炎に揺れるアラバマの二車線の空き道路・バスもライドも見えない | still |
| S13 | ACT1 | 空き路肩の孤立したバス停ポール・来ないバス＝仕事に届かない交通 | still |
| S14 | ACT1 | 車のダッシュに空の財布と1本の鍵＝運転だけが残った手段 | still |
| S15 | ACT1 | 台所に扇状に広がる切符と手数料票＝どの修理も直した物より高くつく（朱の縁） | still |
| S16 | ACT1 | 裁判所の机上の署名済み命令・ペンとガベル（判読不能）＝1ページで sum と cell が決まる（stat F11） | still |
| S17 | ACT1 | 空席の弁護人席・冷光＝能力を問う声が不在（NO HEARING・F12） | still |
| S18 | ACT1 | booking の時計（静止保持・DESIGNED SILENCE 1.5s の画・秒針の含意） | still |
| S19 | ACT2 | 事務机に開いた支払台帳・判読不能の抽象数字＝債務が簿記の行になる | still |
| S20 | ACT2 | 会社ロゴをぼかした月次請求書＝営利企業が punishment を billing（ロゴ判読不能） | still |
| S21 | ACT2 | 保護観察事務所の机のゴム印＝人を revenue に処理する小さな機械 | still |
| S22 | ACT2 | 冷光の長い裁判所の廊下＝案件が手渡される通路（establishing） | factory |
| S23 | ACT2 | 月次封筒の列・1つだけ脇に離す＝罰金に触れる前に skim される company の取分 | still |
| S24 | ACT2 | 机で不均等に分かれた紙幣状の紙2山（判読不能）＝大きい方が罰金・小share が skim（$200/$40・compbars F13） | still |
| S25 | ACT2 | 空席の弁護人席に引き寄せた椅子＝話すはずの1席が空のまま | still |
| S26 | ACT2 | 事務壁に留めた抽象数字のスプレッドシート＝人が数字の行に還元される | still |
| S27 | ACT2 | 顔を伏せたネームプレート＋空の椅子＝company 従業員は物のみで暗示（HRW 利益相反） | still |
| S28 | ACT2 | 冷光の事務棚に後退する匿名の案件フォルダの列＝約38,000人が紙として綴じられる（stat F20） | still |
| S29 | ACT2 | 小ピンを刺したアラバマの壁地図（判読不能ラベル）＝100超裁判所へ伸びる1社 | still |
| S30 | ACT2 | 冷光の小さな法廷のベンチと手すり（無人）＝debt が tally された ordinary な room | still |
| S31 | ACT2 | 硬い光の中に1枚の審問記録＝判事が permanent record に入れた語（quote F21・帰属 Harrington） | still |
| S32 | ACT3 | 暖いランプ下に閉じた古い革表紙の判例集＝1983 の約束を book として（ACT3 幕頭・判読不能） | still |
| S33 | ACT3 | 夜の最高裁の列柱・大理石（factory ambient）＝案件が上へ運ばれる（establishing） | factory |
| S34 | ACT3 | 古い台帳ページ＝抽象的な支払スケジュール（Bearden 事実・F06・判読不能） | still |
| S35 | ACT3 | 半分空の借入封筒＋折り畳んだ支払スケジュール＝最初の$200 を借り残額不可能に | still |
| S36 | ACT3 | 暖いランプ下に開いた意見集・抽象行（判読不能）＝narrow な rule が書かれる（O'Connor 逐語 F07） | still |
| S37 | ACT3 | 冷たい大理石を走る刻印風の光の帯＝due process と equal protection の収斂（第14修正・i2v: 光が走る・緩） | **motion** |
| S38 | ACT3 | 大理石棚に並ぶ2冊の古い判例集＋新しい1冊＝1970/1971 の先行線と capstone（timeline・判読不能） | still |
| S39 | ACT3 | 大理石面に無傷で立つ罰金・手数料・賠償のオブジェの列＝ruling が untouched に残したもの（F05・過大化しない） | still |
| S40 | ACT3 | 満杯の財布＋固く閉じた institutional の扉＝金があり払わぬ者は依然 answerable（won't-pay 側） | still |
| S41 | ACT3 | 空の財布と同じ扉＝払えぬ理由だけで、誰も問わずに収監（can't-pay 側・faultsplit の線・i2v: 線が引かれる・**fast**） | **motion** |
| S42 | ACT3 | 硬い光の線を跨ぐ署名済み命令＝問わず線を越えた order | still |
| S43 | ACT3 | 平凡なレンガの郡裁判所＋折り畳んだ和解書（2014）＝救済は下級審・最高裁でない（i2v M13: 扉が開く・緩・C2） | **motion** |
| S44 | ENDING | 暖いランプ下に単独で置かれた署名済み命令＝数字への回帰（"GO BACK TO THE NUMBER"・数値は焼かず） | still |
| S45 | ENDING | 小切手帳とペン＋開いた扉と淡い日光＝金がある者には choice ですらなかった | still |
| S46 | ENDING | 同じ命令書の背後に固く閉じた冷たい扉＝払えぬ者だけに存在した cell | still |
| S47 | ENDING | 冷光の棚に手つかずで立つ古い判例集＝30年変わらなかった法（"THE RULE HELD"・enforcement failure） | still |
| S48 | ENDING | 夜明けに開く扉から採光が育つ・slow pull-back（i2v M16: 戸が開き光が育つ・DESIGNED SILENCE 2.2s・sound-forward） | **motion** |

**source 集計（scene-primary）:** motion-primary **7**（S02 S04 S10 S37 S41 S43 S48）／factory-primary **3**（S06 S22 S33）／still-primary **38**。**scene-primary はカット全体の一部**で、残りは §5.1 の配分に従い CODEX_B の shotlist が 224 カット（still 100 / factory 92 / motion 32）へ機械展開する。**この表のシーン数・番号は固定（S01..S48）。**

---

# 4. 音の4層設計（ナレ / BGM / SFX / 環境音）

## 4.1 ラウドネス・voice（確定値・EP41〜44 と同一運用）

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

台本の `【DESIGNED SILENCE …】` は**ナレの沈黙であって音の沈黙ではない**。台本には3箇所（**同一楽器化しない**＝HOOK/ACT1 は完全無音、ENDING のみ音を足す沈黙・台本改稿ログ準拠）。

| 位置 | 秒 | 対応画 | 鳴らすもの |
|---|---|---|---|
| HOOK 末（"door standing shut" で保持→hard cut） | **1.8** | S05（留置扉が閉じた画／時計） | BGM mute。**完全無音**（room tone も置かない・台本指定「fully silent」） |
| ACT1 末（"booking clock, second hand moving"） | **1.5** | S18（booking の時計） | BGM mute。**完全無音**（台本指定「fully silent, no room tone」） |
| ENDING（"a door opening onto daylight" ＝payoff の最長沈黙・sound-forward） | **2.2** | S48（夜明けの開く戸） | BGM mute。**SFX を push**（廊下の低いハム rising → 開く扉→採光）。**この沈黙は音を運ぶ**（他2つとの対比） |

**最長無音候補 2.2秒 << 25秒** ✓ `bgm_present` PASS。**機械逓減（1.8→1.5→1.0）にはせず**、HOOK/ACT1 を完全無音、payoff の ENDING を「音を足す沈黙」2.2s にして対比を作る（台本改稿ログ「沈黙設計」に一致）。

## 4.3 章ごとの BGM（1章1トラック・`build_cleveland_bgm.py`＝EP42 `build_young_bgm_real.py` を cleveland 用に複製・film_offset 適用）

| 区間 | 性格 | 楽器 |
|---|---|---|
| HOOK | 低弦の不解決・現在形の緊張・単音が刺す（督促の束・閉じる留置扉） | 低弦+単音メタル |
| OP | ブランドスティンガー（`BrandOpening` 付属） | — |
| ACT1 | 最短・現在形・抑制。刻みは疎で近い（罰金の雪だるま） | 低弦+疎パーカッション |
| ACT2 | 転回。ケアが徴収に変わる冷たさ。$40 skim で現在形が張る | ピアノ+弦 |
| ACT3 | 法の荘厳・大理石。**最も遅い**。Bearden の重さと honesty turn（"did not abolish fines"）の緊張 | 低弦+弦サステイン |
| ENDING | 解決しない和音 →「daylight」でだけ暖色（採光）に開く | ピアノ+弦 |
| ENDCARD | ブランドED（`BrandEndcard` 付属） | — |

## 4.4 SFX

| 種別 | 位置 | 音 |
|---|---|---|
| paper stack | S01/S10/S15 | 紙束のこすれ・輪ゴムの張り・-22 LUFS |
| jail door | S04/booking・沈黙 HOOK末 | 重い institutional 扉の閉・残響・-18 LUFS（サイレン/悲鳴なし・非扇情・C4） |
| booking clock | S05/S18・沈黙 ACT1末 | 秒針の微細な tick・-26 LUFS（沈黙区間は完全無音のため tick も置かない） |
| stamp | S21 ゴム印 | ゴム/木印の一撃・-16 LUFS |
| coin/skim | S23/S24 $40 skim | 紙幣の擦れ・封筒を脇へ引く音・-24 LUFS |
| corridor hum | S22/ENDING 沈黙 | 長い裁判所廊下の低いハム（ENDING 2.2s で rising・sound-forward）・-30→-24 LUFS |
| light band | S37 第14修正 | 微かな高域の走光音・-26 LUFS |
| door open | S43/S48 | 開く扉の軋み・採光の外気・-18 LUFS |
| impact | AE d01/c01/s01 の数値着地 | 低域インパクト・-12 LUFS |
| tick | numberticker/stat の桁変化 | 微細クリック・-24 LUFS |
| room tone | 全編ベッド（台所・大理石反響・booking 冷灰） | 広いリバーブ・-30 LUFS（**沈黙 HOOK/ACT1 は完全無音**） |

---

# 5. ビジュアル — 素材積算（★紙芝居回避＝factory実写を必ず混ぜる・1シーン1枚）

## 5.1 素材の積算（★SPEC の値をそのまま満たす配分）

```
[0] 絵が必要な区間 = narrationSeconds 713.9（BrandOpening/Endcard は Bookends が別レイヤー）
[1] 総カット = 224（SPEC）    713.9 / 224 = 3.19秒/カット  ✓ mean_shot 3.19（≤6.0）
[2] 素材内訳（★SPEC の distinct/cuts をそのまま・1シーン1枚）
    still（SDXL）    84 distinct → 100 カット（16枚が2回・68枚が1回・mean 1.19・cap 2）★各1枚生成
    factory 実写     92 distinct →  92 カット（各1回・cap 1）
    i2v モーション    16 distinct →  32 カット（各2回・cap 2）
    -----------------------------------------------
    distinct 合計   192          → 224 カット
[3] first-use share = 192 / 224 = 0.8571   ✓ ≥0.70（SPEC 一致）
[4] footage_diversity distinct/total = 0.8571   ✓ ≥0.40
[5] 最大使用回数: still 2 / factory 1 / motion 2   ✓ 各 cap 内
[6] 静止画占有率（★紙芝居ゲート）: still-cut 100 / 224 = 0.4464 = 44.64%   ✓ ≤45%（余裕 0.36%pt）
[7] motion coverage: (factory 92 + i2v 32) / 224 = 124/224 = 0.5536   ✓ ≥0.45
[8] factory 下限 = 713.9/30 = 23.8 → ≥24本。設計値 92本   ✓（video を 124 カット以上に保たないと still-share が 0.45 を超える）
```
> **[6] の余裕は 0.36%pt しかない。still-cut を1つ増やすと 45% を割る。still-cut は 100 で固定**（16枚だけ2回・残り68枚1回）。QC で still が 84枚を割ったら §9 の**追加は同一シーンの別プロンプト（新規 distinct）**で回復させ、**cut 数は増やさない**。**still を増やして factory を削るな。factory 92 が still-share≤0.45 を守る下限。**

## 5.2 SDXL と実写在庫の振り分け

- **SDXL（still 84・各1枚）= この事件にしか無い固有物**: 督促状の束・伏せた免許証・空の財布・留置扉/booking の時計・支払台帳・請求書（ロゴぼかし）・ゴム印・空席の弁護人席・スプレッドシート・案件フォルダ・アラバマ地図・小法廷・審問記録・古い判例集・最高裁列柱・古い台帳・借入封筒・意見集・第14修正の光帯・won't/can't の財布と扉・faultsplit の線・和解書・小切手帳・開く戸の夜明け。
- **factory 実写 92 = どこにでもある周辺**: 夜の Montgomery の通り・裁判所の外観・列柱・大理石テクスチャ・長い廊下・住宅街・バス停周辺・陽炎の道路・夜明けの街・ambient 繋ぎ。

## 5.3 SDXL 生成量（★バリエーション0・variants 禁止）

- `ai_prompts.v001.md` = **body 84行の固有プロンプト**（still 各1枚）＋ i2v 種 **16行** ＝ **計100エントリ**（`--only S01` の `shots=` は 100）。`generate_sdxl_4k.py PD-2026-045-cleveland`（**`--variants 1` または指定なし**）。**`--variants 3` を書かない。**
- i2v-source = **16枚**（動きが意味を持つ絵の固有プロンプト・各1シード）。CODEX_A が Wan 2.2 A14B → RIFE 48fps で 16本生成。
- **総生成 = still 84 + i2v seed 16 = 100枚（各1回）。** factory 92 は生成せず在庫選抜。
- プロンプト実体（84本）・i2v リスト（16）・factory 選定（92）は **CODEX_A** の担当（本書 §9 は絵コンテ級の記述と共通スタイル/ネガティブの契約のみ）。

## 5.4 factory のファイル名を信じない（★必須工程・CODEX_A・BLOCKING）

> EP36: `city_surveillance_camera_dome` が実際は大聖堂。EP38: 牛が `documents_on_desk`。ラベルは検索語の記録であって中身の保証ではない。

選定した **92本すべて**を `scripts/build_footage_contact_sheet.py --ep PD-2026-045-cleveland --media video --dir <factory staging>` で1本1フレームのラベル付きコンタクトシート（`runs/qc/cleveland_footage_contact_NN.png`）にし**全点目視**。subtype と食い違う本は差し替える。`select_cleveland_factory.py --verify-no-prior-overlap` で EP39〜44 の sha256 被りゼロを確認。

## 5.5 共通スタイル接尾（各 SDXL プロンプト末尾に必ず付ける・`[STYLE]`・CODEX_A §5.4 と同一）

```
, cinematic still, cold-and-warm documentary grade, a worn working-class Alabama kitchen table under warm tungsten lamplight where ordinary paper piles up, set against cold grey institutional county-jail and courthouse interiors in pale marble and fluorescent light, a single overdue-notice crimson accent as the one warm-red note, restrained and dignified symbolism, telephoto compression and frontal composition, shallow depth of field, ultra-detailed, photoreal, 4K, 16:9, fine film grain, no text, no watermark, no logo, symbolic still-life, no people, no visible face
```
> EP39〜44 との分離: 接尾に `electric blue`（EP39）・`midday suburban`（EP40）・`sodium prison corridor`（EP41）・`ankle monitor`/`warrant-blue`（EP42）・`porch-amber`/`ambulance`（EP43）・`teal-green hospital corridor`（EP44）を**1語も含めない**。EP45 の唯一の暖色差しは **督促の朱 crimson `#B23A48`**。

## 5.6 共通ネガティブ（各 SDXL プロンプトの `Avoid:` に必ず付ける・`[NEG]`・CODEX_A §5.5 と同一）

```
text, words, letters, numbers, captions, watermark, logo, readable document, legible paper, legible citation, legible license number, legible dollar amount, legible date, real celebrity, recognizable real person, identifiable face, portrait, mugshot, likeness of a specific person, human face, human body, child, crying person, weeping family, sensational distress, poverty porn, weapon, gun, blood, gore, nude, bare skin, cartoon, illustration, anime, 3d render, low quality, blurry, jpeg artifacts, deformed, extra limbs, prison cell, steel cellblock, barred cell, sodium prison corridor, navy interrogation room, electric blue, teal-green hospital corridor, clinical hospital, hospital bed, midday suburban daylight, suburban demolition, tow truck, ambulance, porch amber house, ankle monitor, body-worn camera
```
> ネガティブにも **制約違反語（"debtors' prison is legal", "all fines unconstitutional", "supreme court saved cleveland", "gone / abolished everywhere", poverty porn 語 等）を書かない**（§1.3）。会社ロゴが必要な絵（請求書・契約）は「blurred into an unreadable smear」で判読不能にする。判例番号・日付・金額・人数を画に描かない（AE/figures＝B の担当）。

## 5.7 AI開示（強め・毎回・R1）

AI 生成の still・i2v が画面に出ている間、常時右下に **`AI-assisted visualization`**。Oswald 20px / `#C8CDD6` / opacity 70% / 位置 `[W-32, H-28]`。字幕帯と縦 56px 以上離す。概要欄1行: `Some visuals in this film are AI-assisted reconstructions, not photographs of the actual events.`（＋ローカルの legal-aid / ability-to-pay resources の1行。988 は出さない＝本作は債務投獄テーマ）。

## 5.8 ★A↔B 境界契約（asset_manifest スキーマ・EP39〜44 の不整合を最初から潰す）

- **接続点は `episodes/PD-2026-045-cleveland/05_visuals/asset_manifest.v001.json` ただ1ファイル**。A(producer)＝CODEX_A が書き、B(consumer/validator)＝CODEX_B が読む。**counts と role enum を A/B で一字一致**させる。
- **スキーマ版:** `cleveland_assets.v1`（固定文字列）。
- **マニフェスト配列（★A/B 同一）:** `stills` / `motion` / `factory` / `overlay` の4配列。
- **counts オブジェクト（★このキー・値で固定・A/B 一字一致）:** `{ "still_body": 84, "still_i2v_source": 16, "motion": 16, "factory": 92, "overlay": 12 }`。cuts 展開は still 100 / factory 92 / motion 32。
- **`stills[].role` enum（★この3値のみ・A/B 同一・`thumb`/`still_thumb` を作らない）:** `body` / `i2v_source` / `reject`。asset_id は body `^CLEV-S\d{2}$`（S01..S84）/ i2v種 `^CLEV-MS\d{2}$` / motion `^CLEV-M\d{2}$`。
- **サムネは `role="body"` かつ `also_thumb=true` の body still ちょうど6枚**（別 role を作らない・追加生成しない）。**候補集合（★still 資産 ID 空間・CODEX_A §4.3 と一字一致の A↔B 契約点）:** **`{S01, S03, S18, S46, S68, S84}`**。A(CODEX_A)・B(CODEX_B §11) は同一6 asset ID に `also_thumb:true` を立てる。
- **overlay 枚数も A/B 一致**（合成レイヤー・distinct 素材に数えない）。本書設計値 **overlay: 12**（particle/light/vfx）。CODEX_A/CODEX_B は共に overlay=12 で書く。
- CODEX_A は manifest を書いた直後 `build_cleveland_asset_manifest.py --verify` で counts / role / also_thumb / overlay を突き合わせ、**A の値と B の期待が一字一致**であることを確認（不一致は BLOCKING）。**`also_thumb==true` の scene_id 集合が `{S01,S03,S18,S46,S68,S84}` で A↔B 同一**であることも検査する。

---

# 6. Remotion MGビート（FigureBeats）— ★密度下限 30 は必ずここで満たす・dochighlight 不使用

## 6.1 密度の設計（`cleveland_film.json` の `figures[]`）

`check_motion_density`: 3つを AND。**body-minutes = narrationSeconds/60 = 713.9/60 = 11.898**。

| 指標 | floor | EP45 設計値 |
|---|---|---|
| density | ≥2.5/min | figures **36 beats / 11.898 = 3.02/min** ✓（SPEC beats_floor 30 に +6） |
| coverage | ≥0.25 | 36 beats × 平均 5.4秒 = 194.4秒 / 713.9 = **0.272** ✓ |
| variety | ≥3 distinct forms | **8種**（下記） ✓ |

> **AE の 8枠は film.json に入れない**（composite 後に焼くため gate 非カウント）。**density は Remotion 側 36 beats だけで 30 を超える。** coverage が floor 0.25 に一番近いので figures の dur は 4.8–6.0s を基本にする。

## 6.2 `figures[]` の種類配分（★kind は全部小文字・同一 kind を連続させない・★dochighlight 不使用）

**使用可能 kind（全小文字）:** `numberticker` `stat` `votetally`(※本作未使用) `timeline` `quote` `kinetic` `lowerthird` `acttitle` `compbars`（※`comparebars` は非実在）`mechanism`。**大文字は無音描画になる。** **★`dochighlight` を1件も入れない（R-DOCHL・grep 0）。証拠タグ/書類/督促状は `lowerthird` の説明テキストで表す。** **`votetally` も不使用**（Bearden の票割れは台帳に無い＝発明しない・C6）。

| kind（小文字） | 枠数 | EP45 での用途（6制約適用） |
|---|---|---|
| `acttitle` | 3 | ACT1「THE ROAD THAT ENDS AT A CELL」/ ACT2「A DEBT BECOMES A SENTENCE」/ ACT3「BEARDEN — A RIGHT AND A REMEDY」 |
| `lowerthird` | 13 | 開示 `AI-assisted visualization`（HOOK/ENDING 2回）／象徴説明「a suspended license, a stack of unpaid citations」（C4）／JCS 説明（F18・2001設立）／HRW 利益相反（F24）／counsel 不在（F15・medium ヘッジ）／Bearden 判例（F01・461 U.S. 660）／Bearden 事実 $500+$250（F06）／第14修正（F04）／和解2014＝最高裁でない（F16・R-SCOTUS-SPLIT）／SPLC RICO 2015（F22）／「unconstitutional since 1983 · yet it continued」（F17・R-LEGAL・2回）。**判例番号は本文で読み上げない** |
| `kinetic` | 5（うち emphasis 3） | 「THE PRICE OF BEING POOR」／「A FINE THAT SITS GROWS」(["GROWS"])／「NO HEARING」(["NO"]・F12)／「BEARDEN DID NOT ABOLISH FINES」(["NOT"]・F05)／ENDING「GO BACK TO THE NUMBER」(["NUMBER"])＋「THE RULE HELD」(["HELD"])。**emphasisWords は1–2語＝文字切れ回避** |
| `stat` | 3 | $1,554（F11・**FFJC 帰属**・"or 31 days"）／$40 skim/mo（F19・"to the company, per FFJC"）／~38,000・4州・2013（F20・"rolls across four states" の限定・C3） |
| `compbars` | 2 | $200 monthly vs $40 skimmed by JCS（F13・**FFJC を label に**）／won't-pay（still punishable）vs can't-pay（cannot be jailed for that alone）（F05・R-BEARDEN-SCOPE の線・C3） |
| `quote` | 2 | ①O'Connor 逐語「…it may not thereafter imprison a person solely because he lacked the resources to pay it」（**帰属 Justice O'Connor, for the Court**・F07）②Harrington 逐語「a judicially sanctioned extortion racket」（**帰属 Judge Hub Harrington, 2012**・F21）。**要約を引用符に入れない・facts_lock で逐語確認** |
| `timeline` | 2 | ①1970 Williams v. Illinois → 1971 Tate v. Short → 1983 Bearden（先行線と capstone・F08/F09/F01）②2014 settlement → 2015 JCS closes its Alabama operations（F16/F23・救済は下級審・C2） |
| `mechanism` | 4 | `closingdoor`（閉じる留置扉・HOOK）／`closingdoor`（能力を問われないまま扉が閉じる・ACT1）／`faultsplit`（Cleveland の命令が越えた線・ACT3）／`gears`（棚の上の権利が、名前が呼ばれた部屋へ入らなかった・ENDING） |
| **合計** | **36** | variety = **8 figure-kinds** ✓ ≥3 |

> **★`dochighlight` / `votetally` / `comparebars` を1件も置かない（R-DOCHL・C6）。** `graphics[]=[]`（空配列）。density は `figures+graphics+heroCuts` を合算するので figures 36 だけで floor 30 に +6。

## 6.3 配置方針（36本・§1.4 台帳の値だけを焼く・kind を分散・6制約順守・dochighlight 0件・CODEX_B §6.3 と一致）

- **HOOK/OP（3）:** `kinetic`（"THE PRICE OF BEING POOR"）/ `lowerthird`（`AI-assisted visualization` 開示）/ `mechanism:closingdoor`（閉じる留置扉）
- **ACT1（6）:** `acttitle`（THE ROAD THAT ENDS AT A CELL）/ `lowerthird`（"a suspended license, a stack of unpaid citations"・C4）/ `kinetic`（"A FINE THAT SITS GROWS"・["GROWS"]）/ `stat`（**F11 1554**, prefix "$", label "or 31 days · per the Fines and Fees Justice Center"・**R-HEDGE**）/ `kinetic:emphasis`（"NO HEARING"・["NO"]・F12）/ `mechanism:closingdoor`（能力を問われないまま扉が閉じる）
- **ACT2（9）:** `acttitle`（A DEBT BECOMES A SENTENCE）/ `lowerthird`（**F18** Judicial Correction Services · for-profit probation · founded 2001）/ `kinetic`（"OFFENDER-FUNDED PROBATION"・["FUNDED"]）/ `compbars`（**F13** [{"$200 monthly payment",200},{"$40 skimmed by the company · FFJC",40}]・R-HEDGE）/ `stat`（**F19 40**, prefix "$", suffix "/mo", label "to the company, per FFJC"）/ `lowerthird`（**F24** Human Rights Watch, "ability-to-pay handed to company employees — a conflict of interest"）/ `lowerthird`（**F15** "no right to a lawyer was announced" / "counsel's seat sat empty"・medium）/ `stat`（**F20 38000**, label "on the company's rolls · four states · 2013"・C3）/ `quote`（"a judicially sanctioned extortion racket" → "Judge Hub Harrington, 2012"・**F21**）
- **ACT3（13）:** `acttitle`（BEARDEN — A RIGHT AND A REMEDY）/ `lowerthird`（**F01** Bearden v. Georgia, 461 U.S. 660 (1983) / "opinion by Justice O'Connor"）/ `timeline`（**F08** 1970 Williams → **F09** 1971 Tate → **F01** 1983 Bearden）/ `lowerthird`（**F06** "$500 fine + $250 restitution" / "then he was laid off"）/ `quote`（O'Connor 逐語 → "Justice O'Connor, for the Court"・**F07**）/ `lowerthird`（**F04** Fourteenth Amendment / "due process and equal protection converge"）/ `kinetic:emphasis`（"BEARDEN DID NOT ABOLISH FINES"・["NOT"]・**F05**）/ `compbars`（**F05** [{"a person who WON'T pay — still punishable",1},{"a person who CAN'T pay — cannot be jailed for that alone",1}]・C3）/ `mechanism:faultsplit`（Cleveland の命令が越えた線）/ `lowerthird`（**F16** "Cleveland's relief: a lower-court settlement, 2014" / "not the Supreme Court"・**R-SCOTUS-SPLIT**）/ `timeline`（**F16** 2014 settlement → **F23** 2015 JCS closes）/ `lowerthird`（**F22** Southern Poverty Law Center / "sued under a federal racketeering statute · 2015"）/ `lowerthird`（**F17** "unconstitutional since 1983" / "yet it continued, county after county"・**R-LEGAL**）
- **ENDING（5）:** `kinetic`（"GO BACK TO THE NUMBER"・["NUMBER"]・数値は焼かず echo）/ `lowerthird`（**F17** "UNCONSTITUTIONAL SINCE 1983" / "the rule held — enforcing it kept failing"・R-LEGAL）/ `lowerthird`（開示 `AI-assisted visualization` 再掲）/ `kinetic:emphasis`（"THE RULE HELD"・["HELD"]・C1 enforcement failure）/ `mechanism:gears`（棚の上の権利が、名前が呼ばれた部屋へ入らなかった）

## 6.4 配置ルール

1. **AE の 8区間（§7）と1秒でも重ならない**（`validate_cleveland_beats.py`＝validate_caniglia_beats.py を複製・両方突き合わせ）。
2. 幕あたり配分: HOOK/OP=3 / ACT1=6 / ACT2=9 / ACT3=13 / ENDING=5（ACT3 が最長 179.0s なので厚め）。
3. **同じ kind を連続させない**（`mechanism` の直後に `mechanism` を置かない）。
4. 1枠 **4.8–6.0秒**。
5. ACT3 の説明区間に `compbars`＋`quote`＋`timeline`＋`mechanism`＋`lowerthird` を分散し 20秒超の平坦区間をゼロに。
6. `quote` は**逐語のみ**（要約を引用符に入れない・R-ATTRIB）。帰属は O'Connor / Harrington に帰属語を伴う。
7. `figures[].*text*`/`lines[]`/`label`/`quote` は `facts_lock` 検査対象（「合法」断定・「全罰金違憲」・「最高裁が Cleveland を救った」・台帳外数値・投票数・**dochighlight**・988 を出さない）。
8. **$1,554/$200/$40 を焼く figure は同一 payload/label に "Fines and Fees"/"FFJC" を必ず持つ（R-HEDGE）。** "unconstitutional" 系 payload は必ず "yet it continued / still / the rule held / enforcement" と対で置く（R-LEGAL）。

## 6.5 密度の最終検算

```
Remotion figures 36（film.json 内・graphics 空）
  density  = 36 / 11.898 = 3.02/min   ✓ ≥2.5（SPEC beats_floor 30 → 36 で +6）
  coverage = 194.4s / 713.9 = 0.272    ✓ ≥0.25
  variety  = 8 forms                   ✓ ≥3
  dochighlight count = 0               ✓ R-DOCHL（grep 0）
AE hero 8枠は composite 後・gate 非カウント（上乗せの決め所）
```

---

# 7. After Effects ヒーロービート（8枠）— ★AEカードは密度に数えられない

## 7.1 大原則（★EP39/40 の致命傷を回避）

`check_motion_density` は **film.json の `figures` だけ**を数える。AE の 8枠は本編 mp4 に composite された後に焼き込まれるため gate は 0 カウント。→ **密度下限 30 は §6 の Remotion figures（36本）で満たす。** AE はその上に載る「決め所の数値タイポ」。

## 7.2 パイプライン（EP42/43/44 で measured 済み・cleveland 用に複製）

```
[1] Remotion で本編完成 → cleveland_final_bgm.v001.mp4（音声ミックス済み・build_cleveland_bgm.py→film_offset 適用）
[2] scripts/ae/build_cleveland_hero_cards.py（＝build_caniglia_hero_cards.py を複製）が beats.json と cleveland_hero.jsx を生成
[3] AfterFX -noui -r cleveland_hero.jsx → 各ビートを 1920x1080@30fps の不透明 mp4 で書き出し
[4] scripts/ae/composite_cleveland_hero.py（＝composite_caniglia_hero.py を複製）が ffmpeg overlay + enable='between(t,start,end)' で焼き込み
[5] 出力 → cleveland_final_bgm.v002_ae.mp4（v001 は絶対に上書きしない・film_offset 適用）
```

## 7.3 AEカードデッキ（★8枚・§1.4 の確定数値のみ・6制約適用・数値は台帳照合・accent #B23A48）

> **★レイアウトは複製元が実装する8種のみ**（`DATE_STAMP`/`CENTER_STACK`/`MONEY_STACK`/`SPLIT_COMPARE`/`ACT_TITLE_CARD`/`QUOTE_CARD`/`VOTE_SPLIT`/`SEAM_TRANSITION`）。**この表と CODEX_B §7.2 のデッキは id・レイアウト・F-ID が完全一致**（`validate_cleveland_beats` が両方を突き合わせる）。上記8種以外の未実装レイアウト名は使わない。**EP45 は `VOTE_SPLIT`（投票数が台帳に無い）/ `ACT_TITLE_CARD`（幕頭は Remotion `acttitle` が担う）/ `SEAM_TRANSITION` を §7.3 では未使用。`MONEY_STACK` は d01/c01 で使用（この案件は金額が主役）。** variety は使用5種（MONEY_STACK/CENTER_STACK/DATE_STAMP/QUOTE_CARD/SPLIT_COMPARE）で ≥3 を満たす。

| id | レイアウト（実装済み8種） | hero（主表示） | top / sub / bottom / attribution | 数値ID | F-ID | 背景（象徴のみ・顔なし） | 尺 |
|---|---|---|---|---|---|---|---|
| **d01** | **MONEY_STACK** | **$1,554 OR 31 DAYS** | top: **THE COURT ORDER** / bottom: **PER THE FINES AND FEES JUSTICE CENTER** | N01 | **F11** | 伏せ置きの免許証＋督促の束 | 6.0 |
| **n01** | **CENTER_STACK** | **NO HEARING** | top: **BEFORE THE CELL** / bottom: **NO ONE ASKED IF SHE COULD PAY** | N02 | **F12** | 空席の弁護人席・裁判所廊下 | 6.0 |
| **t01** | **DATE_STAMP** | **MAY 24, 1983** | place: **BEARDEN v. GEORGIA, 461 U.S. 660** | N03 | **F01** | 大理石の階段（判読困難） | 5.0 |
| **q01** | **QUOTE_CARD** | **"...it may not thereafter imprison a person solely because he lacked the resources to pay it"** | attribution: **JUSTICE O'CONNOR, FOR THE COURT** | N04 | **F07** | 棚の上の法典 | 7.5 |
| **c01** | **MONEY_STACK** | **$200 / MONTH → $40 TO JCS** | top: **OFFENDER-FUNDED PROBATION** / bottom: **PER THE FINES AND FEES JUSTICE CENTER** | N05 | **F13** | 支払台帳・請求書（ロゴぼかし） | 6.5 |
| **s01** | **CENTER_STACK** | **~38,000 · 4 STATES** | top: **ON THE COMPANY'S ROLLS, 2013** / bottom: **ONE COMPANY, A HUNDRED ALABAMA COURTS** | N06 | **F20** | スプレッドシート・長い廊下 | 6.5 |
| **u01** | **CENTER_STACK** | **UNCONSTITUTIONAL SINCE 1983** | top: **THE RULE HELD** / bottom: **YET IT CONTINUED, COUNTY AFTER COUNTY** | N07 | **F17** | 閉じた留置扉・時計 | 6.5 |
| **w01** | **SPLIT_COMPARE** | **A RIGHT / A REMEDY** | top: **HOW HER FREEDOM CAME** / bottom: **A LOWER-COURT SETTLEMENT, 2014 — NOT THE SUPREME COURT** | N08 | **F16** | 左=書棚の権利 / 右=開く裁判所の扉 | 7.0 |

> **★行順＝start 昇順（時系列）:** `d01`(ACT1 命令) < `n01`(ACT1 能力審問なし) < `c01`(ACT2 $200/$40) < `s01`(ACT2 規模) < `t01`(ACT3 Bearden 日付) < `q01`(ACT3 O'Connor 逐語) < `w01`(ACT3 和解2014・最高裁でない) < `u01`(ENDING 手前・unconstitutional since 1983)。**start は §7.4 beats.json で section 窓からオフセットで算出しクランプ**するため、**本番 rendered base の秒で単調増加・重複ゼロ**を `validate_cleveland_beats` が保証する。**この id・レイアウト・F-ID は CODEX_B §7.2 デッキと一字一致。**
> **★q01 の QUOTE_CARD は逐語（R-ATTRIB）。** ブリーフ§6 の略記 `"...ability to pay..."` は**引用符の中に入れない**（要約を quote にすると R-ATTRIB で FAIL）。quote 文字列は §2 `APPROVED_QUOTES` の O'Connor 逐語（461 U.S. 667-68 相当）と一致（大小無視・表示は全大文字）。
> **d01 / c01（$1,554・$200・$40）は bottom に "PER THE FINES AND FEES JUSTICE CENTER"（FFJC）を必ず別レイヤーで焼く（R-HEDGE・medium 単一出典）。** 金額は ACCENT crimson、ラベルは WHITE/SILVER。
> **u01 の bottom は "YET IT CONTINUED …"（enforcement failure・R-LEGAL）。「合法だった」を書かない。** hero を WHITE、bottom を ACCENT で強調。
> **w01 の bottom は "A LOWER-COURT SETTLEMENT, 2014 — NOT THE SUPREME COURT"（C2・R-SCOTUS-SPLIT）。「最高裁が Cleveland を救った」を書かない。** 左右2カラムで right と remedy を分離。
> **どのカードにも「合法」断定・「全罰金違憲」・投票数（発明値）・988・dochighlight を書かない。** 数値ID＝台帳（§1.4）と一致必須。カウント終了から区間終端まで最低 1.20秒ホールド。em-dash は本文表示の `—` と異なり **beats.json ラベルでは ASCII `-` に置換**（AE の豆腐回避・§7.6）。

### 検算

```
[1] 8区間・本番 start 単調増加・重複ゼロ（build_cleveland_hero_cards.py が section 窓オフセットで算出）
[2] HOOK(0–24.6) / BrandOpening / ENDING payoff の最長沈黙(2.2s) / BrandEndcard に1秒も重ならない
[3] 合計 = 6.0+6.0+5.0+7.5+6.5+6.5+6.5+7.0 = 51.0秒 / 726.4 = 7.0%   ✓ 過剰でない
[4] レイアウト種類 = MONEY_STACK, CENTER_STACK, DATE_STAMP, QUOTE_CARD, SPLIT_COMPARE = 5種（全て実装済み8種内）   ✓ ≥3
[5] figures[] 36枠と1秒でも重ならない（validate_cleveland_beats.py が両方突き合わせ）
[6] dochighlight/votetally/comparebars レイアウトは存在しない（8種のみ）   ✓ R-DOCHL
```

## 7.4 `beats.json`（`08_edit/ae_hero/beats.json`・`schema_version: "cleveland_beats.v1"`）

各 beat に `id` / `layout` / `start` / `end` / `dur` / `still`(象徴 or null) / `hero` / `top` / `bottom` / `sub` / `caption`(**改行禁止・最大50字**) / `value` / `numKeys` / `blend_mode`(既定 "overlay") / `required` / `out` / `attribution`(**QUOTE_CARD=q01 は必須**・§2 `APPROVED_QUOTES` と一致・R-ATTRIB)。**区間の秒は本番 rendered base（narration_index 由来）に一致させ、section 窓からオフセットで算出しクランプ。** 数値カードは全て `money_keys()` 系で表示文字列を Python 事前計算（JSX で算術しない＝EP38 確定ルール）。

## 7.5 レイアウト定義・色定数（EP43/44 を踏襲・色のみ EP45 値・CODEX_B §7.3 と一致）

**共通レイヤースタック（下→上）:** L9 黒ソリッド → L8 静止画（scale fill→fill×1.08・drift）→ L7 グレードウォッシュ（**暖い near-black** `addSolid([0.090,0.071,0.055])`＝LAMP / MULTIPLY / opacity 30）→ L6 羽根付き楕円ビネット → L5 グロー（下中央 crimson 実用差し ADD）→ L4 ライトスイープ（`"ADBE Rotate Z"`=18）→ L3 上ラベル（Oswald）→ L2b アクセントライン（ACCENT crimson・scaleX ワイプ・`motionBlur=true`）→ L2 主数値/主文字（Anton・ACCENT・`motionBlur=true`）→ L1b 下ラベル → L1 字幕ロワーサード → **L0b AI開示テキスト（`AI-assisted visualization`・Oswald 20px・SILVER `#C8CDD6`・opacity 70%・右下 `[W-32, H-28]`・全カード常時焼き＝R1）** → L0 黒シームディップ（head/tail 各4フレーム）。

**★EP45 色定数（0..1 float・crimson レーン色。EP41 gold / EP42 blue / EP43 amber / EP44 teal を流用禁止・CODEX_B §7.3 と一致）:**
```python
ACCENT = [0.698, 0.227, 0.282]  # #B23A48 crimson（督促の朱）— 数値・下線・唯一の暖色差し
WHITE  = [0.961, 0.969, 0.980]  # #F5F7FA
SILVER = [0.784, 0.804, 0.839]  # #C8CDD6（開示テキスト）
INK    = [0.039, 0.039, 0.047]  # #0A0A0C 近黒ルート（サムネ bg と一致）
LAMP   = [0.090, 0.071, 0.055]  # #17120E 暖いランプ near-black ウォッシュ
MARBLE = [0.204, 0.212, 0.231]  # #34363B 大理石（ACT3）
```
**フォント:** 数値/主文字 = **Anton Regular** / ラベル・字幕 = **Oswald Medium**。`getFontsByFamilyNameAndStyleName` で厳格解決（miss は throw・フォールバック禁止）。テキスト幅は **`sourceRectAtTime(t,false).width` で実測**（advance-width 推定禁止＝EP40 文字切れの原因・ブリーフ§5）。**`d01`/`c01`（MONEY_STACK）は金額を ACCENT crimson、ラベルを WHITE/SILVER。bottom に "PER THE FINES AND FEES JUSTICE CENTER"（R-HEDGE）を別レイヤーで焼く。`u01` の "YET IT CONTINUED" と `w01` の bottom は削除禁止。**

**カウント型:** $1,554 / $200 / $40 / 38,000 は `money_keys()` で桁を事前計算し settle（ease-out cubic）＋ impact SFX。**投票数（得票カウント）は台帳に無いので使わない。**

## 7.6 このマシン固有の罠（★1つ忘れると無言で品質が落ちる・EP42-44 §6.6 全項を cleveland に適用）

フォント解決の例外ラップ（`psName()`・allFonts の array-LIKE ラッパーを unwrap）／spatial ease は配列次元1（`prop.isSpatial ? 1 : ...`）／OM=`"H.264 - レンダリング設定を一致 - 15 Mbps"`・RS=`"最良設定"`（英語名は try/catch フォールバック）／`app.newProject()` を headless で使わない（同名 `CLEVELAND_` コンプを防御削除）／`layer.motionBlur=true` を動くレイヤー個別に／回転は `"ADBE Rotate Z"`／改行は1行厳守（SPLIT_COMPARE の左右2値は別レイヤー・改行禁止）／em-dash は `-`／inPoint と outPoint 両方設定／`item.mainSource.conformFrameRate = 30`／実行パス `C:\Program Files\Adobe\Adobe After Effects 2026\Support Files\AfterFX.exe`／`proj.gpuAccelType = GpuAccelType.SOFTWARE`／ビルド ~100–120秒・完了マーカー `render/_build_ok.txt` をポーリング（タイムアウト≥300秒）・末尾で `app.quit()`／**aerender 前に `.aep` mtime > `.jsx` を assert**（ブリーフ§5・.aep が古いと前ビルドを焼く事故）。

## 7.7 コンポジタ（`scripts/ae/composite_cleveland_hero.py`・SKIP 4条件を1つも削らない）

`BASE = cleveland_final_bgm.v001.mp4` / `OUT = cleveland_final_bgm.v002_ae.mp4`（v001 不変）。SKIP: (1) `render/<id>.mp4` 不在 / (2) 解像度≠1920x1080 / (3) 実測尺 `< dur-0.3` / (4) `beat.end > base_dur`。ffmpeg: `overlay=0:0:eof_action=pass:enable='between(t,start,end)'` / `-c:v libx264 -preset slow -crf 16 -pix_fmt yuv420p -colorspace bt709 -c:a copy`。**出荷済みを絶対に上書きしない。film_offset を適用する。**

---

# 8. レイヤー構成 と ゾーン分離（★主役の裏に最低4層）

## 8.1 本編カットのレイヤー構成（下→上・主役 L4 の裏に L1/L2/L3/L3b = 4層）

| L | 名前 | EP45 の値 |
|---|---|---|
| **L0** | ルート背景 | `#0A0A0C`（INK） |
| **L1** | グラデ背景 | `radial-gradient(120% 120% at 50% 40%, #17120E 0%, #100C0A 45%, #0A0A0C 100%)`（暖いランプ near-black。ACT3 のみ大理石寄り `#34363B` にシフト・booking は `#24262A`） |
| **L2** | グリッド/ライン | 縦横 64px の反復線＋放射マスク＋ドリフト。`repeating-linear-gradient(0deg/90deg, #B23A4818 0px 1px, transparent 1px 64px)`、`translateY 0→48px` / `Easing.inOut(Easing.sin)`（等速禁止） |
| **L3** | グロー | 単一 crimson の督促差し。`radial-gradient(closest-side, #B23A4866 0%, #B23A4818 45%, transparent 75%)`、`filter: blur(28px)`。位置は幕で移動（督促の束→booking の扉→支払台帳→大理石→夜明けの戸） |
| **L3b** | 大理石の光帯/ビネット | ACT3 は第14修正の光帯（`linear-gradient(100deg, transparent, #B23A4822, transparent)` を横に slow drift）、他幕は羽根ビネット。`translateX` を `Easing.inOut(Easing.sin)` で微動（静止フレームゼロ） |
| **L4** | 主役（still / i2v / factory） | §10 のモーション（Ken Burns/parallax/i2v） |
| **L5** | テロップゾーン（上/中央・figures） | §8.2 |
| **L6** | 字幕ゾーン（下部帯） | §8.2 |

> **主役（L4）の裏に L1/L2/L3/L3b = 4層**（グラデ背景・グリッド/ライン・グロー・光帯/ビネット）で CLAUDE.md「最低3レイヤー」＋タスク「最低4層」を満たす。**各層は §3.1b の通り常に微動（静止フレームゼロ）。**

## 8.2 ゾーン分離（一度も重ねない）

| ゾーン | 縦位置（1080基準） | スタイル |
|---|---|---|
| テロップ見出し | `y=96–260` | Oswald 64px / `#F5F7FA` / letterSpacing 4 |
| 中央テロップ / figures | `y=420–660` | §6 |
| 出典テロップ（アクセントライン） | `y=742–786` | Oswald 28px / crimson `#B23A48` 3px 下線 |
| 字幕帯 | `y=872–1010` | 白 `#FFFFFF` + `textShadow:0 0 6px #000,0 2px 4px #000` / 半透明黒帯 `rgba(6,6,8,0.62)` / ≤2行・1行≤42字 / 54px / lineHeight 1.28 |
| AI開示 | `y=1024–1052`（右下） | Oswald 20px / `#C8CDD6` / opacity 70% |

**Caption QC:** ナレ一致 ≥99%（faster-whisper 強制アライン）/ `.srt` カバー ≥95% / キュー 1.0–6.0秒 / CPS ≤17 / 単語割り禁止 / 1語孤立キュー禁止 / ズレ ≤120ms。**【DESIGNED SILENCE】3区間には字幕キューを置かない。**

---

# 9. 絵コンテ（★48シーン・象徴のみ・6制約・Cleveland/JCS 非人物化・CODEX_A が 84本プロンプトへ展開する原図）

## 9.1 パーサ契約（★CODEX_A が `ai_prompts.v001.md` を書くときの形式・`read_prompts()` が読む2行形式）

```
- `S01.png`
<positive prompt> ... [STYLE] Avoid: <negative>
```
- **1行目:** `` - `S01.png` ``（バッククォート囲み・行末は `.png` 直後）。プロンプトを同じ行に書かない。
- **2行目:** 正プロンプト → `[STYLE]`（§5.5）→ `Avoid:` → 負プロンプト（§5.6）。
- 配置先: **`episodes/PD-2026-045-cleveland/04_scenes/ai_prompts.v001.md`**。生成: `.venv/Scripts/python.exe scripts/generate_sdxl_4k.py PD-2026-045-cleveland`（**variants 指定なし＝1枚**）。
- 出力: `H:\pd-media\assets\ai\cleveland\S01.png …` ＋ `remotion/public/cleveland/`。長辺 ≥3840 で冪等スキップ。
- **★body 84本＝84行**（still 各1枚）＋ **i2v 種 16行**（M01_src..M16_src）＝ `ai_prompts.v001.md` は計 **100 エントリ**。CODEX_A は書いた直後 `--only S01` で `shots=` が **100** に達しているか（2行形式が壊れていないか）を確認。**プロンプト実体（84本）は CODEX_A §5.9 が正典**（本節は絵コンテ級の原図）。

## 9.2 絵コンテ級ショット記述（Sid ごと・カメラ/モーション/象徴/制約。CODEX_A はこれを固有プロンプトに翻訳）

> **全ショット共通:** 顔・身体・肖像なし（R1/C4）。Harriet Cleveland を個人として描かない（象徴・物・影のみ）。読める文字を作らない（redacted/illegible）。判例番号・日付・金額・人数・会社ロゴを描かない（ロゴはぼかす）。暖いランプの台所＋冷灰の booking＋冷たい大理石＋唯一の暖色差し crimson。「投獄は合法/正当」に見える絵を作らない（C1）。最高裁の列柱＝Bearden の線／Cleveland の救済は modest county courthouse＋折り畳んだ和解書で下級審として描く（C2）。罰金・手数料の物は untouched に立つ象徴で（C3）。扇情化しない（C4・poverty porn 禁止）。

| Sid | カメラ/レンズ | 象徴（動き） | 制約メモ |
|---|---|---|---|
| S01 | 俯瞰寄り・接写 | 輪ゴムで束ねた督促状の分厚い束・暖いランプ | C4/C6: 象徴のみ・判読不能 |
| S02 | 接写・台所 | 伏せた免許証（i2v: ゆっくり裏返る） | C4: 顔なし |
| S03 | 俯瞰・寄り | 平置きで空の財布・中に何もない | C4: 尊厳・非扇情 |
| S04 | 正対・寄り | booking の institutional 扉が閉じる（i2v: swing shut） | C4: 鉄格子/独房なし |
| S05 | 正対・静止 | booking の壁時計（DESIGNED SILENCE 1.8s） | 後で S48 と対 |
| S06 | 引き・外 | 夜の Montgomery の質素な通り（factory ambient） | — |
| S07 | 正対・push-in | 最高裁の淡い大理石列柱＝1983 の答え | C2: 最高裁の線 |
| S08 | 寄り＋奥行き | 手前に朱の督促1通・奥に遠い最高裁列柱 | 小さな債務→最高裁の距離 |
| S09 | 接写 | ワイパーの1枚の平凡な切符（朱の縁） | C6: 判読不能 |
| S10 | 俯瞰・寄り | 束が太り再束（i2v: 束が増える） | 座る債務が育つ |
| S11 | 接写 | 停止された免許証＋伏せた停止通知（判読不能） | C4/C6: 顔なし |
| S12 | 引き・道路 | 陽炎のアラバマ二車線の空き道路 | 車社会の孤立 |
| S13 | 引き・路肩 | 孤立したバス停ポール・来ないバス | 仕事に届かない交通 |
| S14 | 接写・車内 | ダッシュの空の財布と1本の鍵 | 運転だけが残る |
| S15 | 俯瞰・接写 | 台所に扇状の切符と手数料票（朱の縁） | どの修理も高くつく |
| S16 | 接写・机上 | 署名済み命令・ペンとガベル（判読不能） | C6: stat F11・金額は figures |
| S17 | 正対 | 空席の弁護人席（冷光）＝能力を問う声が不在 | C1: NO HEARING・F12 |
| S18 | 正対・静止 | booking の時計（DESIGNED SILENCE 1.5s） | 沈黙の画 |
| S19 | 接写・机上 | 開いた支払台帳・抽象数字（判読不能） | C5/C6: 制度象徴 |
| S20 | 接写 | 会社ロゴをぼかした月次請求書 | C5: ロゴ判読不能 |
| S21 | 接写 | 保護観察事務所のゴム印 | C5: 人を revenue に処理 |
| S22 | 引き・廊下 | 冷光の長い裁判所の廊下（factory ambient） | — |
| S23 | 俯瞰・机上 | 月次封筒の列・1つ脇に離す＝skim | C5: $200/$40 は figures |
| S24 | 接写 | 不均等な紙幣状の紙2山（判読不能）＝skim | C6: compbars F13・数値は figures |
| S25 | 正対 | 空席の弁護人席に引き寄せた椅子 | C1: counsel 不在 |
| S26 | 壁ショット | 抽象数字のスプレッドシート（判読不能） | C5: 人が数字の行に |
| S27 | 接写 | 顔を伏せたネームプレート＋空の椅子 | C5: 従業員は物で暗示 |
| S28 | 引き・棚 | 匿名の案件フォルダの列 | C6: ~38,000 は figures |
| S29 | 地図・引き | 小ピンを刺したアラバマの壁地図（判読不能） | 100超裁判所の1社 |
| S30 | 引き・法廷 | 冷光の小法廷のベンチと手すり（無人） | — |
| S31 | 接写・硬光 | 1枚の審問記録＝permanent record の語 | C5: quote F21 は figures・帰属 Harrington |
| S32 | 机上・接写 | 暖いランプ下に閉じた古い判例集（ACT3 幕頭・判読不能） | C2: 1983 の約束 |
| S33 | 正対・列柱 | 夜の最高裁の列柱・大理石（factory ambient） | C2: 最高裁の線 |
| S34 | 接写・机上 | 古い台帳ページ＝抽象的な支払スケジュール（判読不能） | C6: Bearden 事実は figures F06 |
| S35 | 接写 | 半分空の借入封筒＋折り畳んだ支払スケジュール | 最初の$200 を借り残額不可能 |
| S36 | 机上 | 暖いランプ下に開いた意見集・抽象行（判読不能） | C3: O'Connor 逐語は figures F07 |
| S37 | 壁ショット | 大理石を走る刻印風の光の帯（i2v: 光が走る） | C6: 第14修正・逐語は figures |
| S38 | 大理石棚 | 2冊の古い判例集＋新しい1冊（判読不能） | C2: 1970/1971 と capstone |
| S39 | 大理石面 | 無傷で立つ罰金・手数料・賠償のオブジェの列 | **C3: untouched・全罰金違憲化しない** |
| S40 | 正対 | 満杯の財布＋固く閉じた扉＝won't-pay 側 | C3: 依然 answerable |
| S41 | 正対 | 空の財布＋同じ扉＝can't-pay 側（i2v: 線が引かれる） | C3: faultsplit の線 |
| S42 | 接写・床 | 硬い光の線を跨ぐ署名済み命令 | C1: 問わず線を越えた order |
| S43 | 引き＋接写 | 平凡なレンガの郡裁判所＋折り畳んだ和解書2014（i2v: 扉が開く） | **C2: 下級審・最高裁でない** |
| S44 | 接写 | 単独で置かれた署名済み命令＝数字への回帰 | 数値は焼かず echo |
| S45 | 接写 | 小切手帳とペン＋開いた扉と淡い日光 | 金がある者には choice でない |
| S46 | 正対 | 同じ命令書の背後に固く閉じた冷たい扉 | C4: 払えぬ者だけの cell |
| S47 | 引き・棚 | 手つかずで立つ古い判例集＝30年変わらぬ法 | C1: THE RULE HELD・enforcement failure |
| S48 | 引き・pull-back | 夜明けに開く扉から採光が育つ（i2v: 戸が開き光が育つ・DESIGNED SILENCE 2.2s） | C4: 人物なし・payoff |

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
**0.5s 刻み方針:** 224カットの境界は **`QUANT`=15フレーム（0.5秒）にスナップ**して配置する。各カット長は `CUT_MIN`〜`CUT_MAX`、平均 `CUT_MEAN`。ACT3 は最も遅く（長カット寄り・6.0s 近辺を多用）、ACT1 は速く（1.0–2.5s の断片・現在形・HOOK は ~2s cut）。CODEX_B は shotlist の各 span 端を 15f グリッドに丸める。

## 10.2 全カット共通モーション（★静止フレームを1枚も作らない）

| 素材 | 基本モーション | イージング | 数値 |
|---|---|---|---|
| **still** | Ken Burns：`scale 1.00→1.08` を**カット全長**で。加えて `translate` を象徴方向へ ±24px | `Easing.out(Easing.cubic)` | scale 差 +0.08 / drift 24px。**opacity は translate/scale と必ず対**（単独禁止） |
| **i2v** | ネイティブ動き（Wan 2.2 A14B → RIFE 48fps）＋微 `scale 1.00→1.03` | ネイティブ＋`Easing.out(Easing.cubic)` | 追い足しの scale は 0.03 のみ |
| **factory** | 実写の内在動き＋微 Ken Burns `scale 1.00→1.04` | `Easing.out(Easing.cubic)` | 24pxまでの parallax 可 |

**カットイン/アウト:** クロスディゾルブ 6–10f または hard cut。HOOK/ACT1 の断片は hard cut 寄り（現在形・抑制）。ACT3 は長めのディゾルブ（荘厳・最も遅い）。**フェードは opacity 単独にせず、入りは `translateY 12px→0`＋opacity、抜けは `scale 1.00→1.02`＋opacity を対にする。**

## 10.3 速い動きの motion-blur（★@remotion/motion-blur の Trail）

```tsx
import {Trail} from '@remotion/motion-blur';
<Trail layers={6} lagInFrames={1.2} trailOpacity={0.45}>
  {/* 主役 or 動く数値/文字 */}
</Trail>
```
対象（fast move）: **S04**（留置扉 swing shut）、**booking 扉 closingdoor**、**S21 ゴム印 stamp**、**S41**（faultsplit の線越え）、および §6 の `numberticker`/`stat` 桁変化・幕頭 `kinetic`・`kinetic:emphasis` の切れ上がり。**S05/S18（時計）・S33–S35（荘厳 push-in）・S37（光が走る・緩）・S48（夜明けの pull-back）・S10/S43（緩い i2v）・Ken Burns には Trail をかけない**（無駄な残像・扇情を避ける・C4）。

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

# 11. オープニング（OP）設計 — 完全仕様（`OpeningCleveland`・fps=60・CLAUDE.md §1–5 全項目）

## 11.1 秒数ベースのタイムライン（fps=60・「フレーム」は全て `Math.round(60 × 秒)`・直書き禁止・0.5s 刻み方針で全区間記述）

```ts
const FPS_OP = 60; const F = (s:number)=>Math.round(FPS_OP*s);   // 総 180f = F(3.0)
```

| 秒 | フレーム | 起きること（EP45 signature = 暖いランプ下に積もる督促の束＋朱の差し） |
|---|---|---|
| 0.00–0.10 | f0–6 | 画面 `#0A0A0C`。**L1** グラデ opacity 0→1（0.40s）＋ **scale 1.08→1.00** を 180f で（`Easing.out(Easing.cubic)`）。opacity 単独でなく scale 併用 |
| 0.10–0.15 | f6–9 | **L6 ロゴ**（`hasLogo`）左上 `top:64/left:72` に spring 出現。scale 0.4→1.0・opacity 0→1（併用・`damping:14,mass:0.9`） |
| 0.15–0.25 | f9–15 | **L2** グリッドが spring（`{damping:200,mass:1,durationInFrames:F(0.8)=48}`）で reveal。最終 opacity=`gridReveal*0.18`。全体を 180f で `translateY 0→48px`（`Easing.inOut(Easing.sin)`） |
| 0.25–0.30 | f15–18 | **L3** crimson の督促グローが spring（`{damping:18,mass:1.2}`）＝暖いランプの差し。scale 0.6→1.15 / opacity 0→0.85（併用）。`filter:blur(28px)` |
| 0.30–0.86 | f18–52 | **L4 主役タイトル**が1文字ずつ切れ上がる（`overflow:hidden` マスク）。各文字 spring（`{damping:16,mass:1}`）で `translateY 110%→0`、opacity=`interpolate(sp,[0,0.25],[0,1])`。**スタッガー=`F(0.04)=2フレーム/文字**。全体を `Trail`（`layers=6,lagInFrames=1.2,trailOpacity=0.45`）で包む |
| 0.55–1.15 | f33–69 | **L2b 督促の光ライン**（EP45固有＝朱の帯がタイトル背後を横切る）。中央から `scaleX 0→1`＋`opacity 0→0.55`（spring `{damping:22,mass:1.1}`, `transformOrigin:'center'`）。crimson。opacity 単独禁止で scaleX 併用 |
| 0.95–1.35 | f57–81 | **L5a** crimson の下線が左から `scaleX 0→1`（spring `{damping:16,mass:0.8}`, `transformOrigin:'left center'`）。240×6px・`boxShadow:0 0 24px #B23A48aa` |
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
| L2b 督促の光 | scaleX 0→1 / opacity 0→0.55 | spring | `{damping:22,mass:1.1}`・origin center |
| L5a 下線 | scaleX 0→1 | spring | `{damping:16,mass:0.8}`・origin left |
| L5b サブ | translateY 24px→0 / opacity | spring | `{damping:20,mass:1}` |
| L6 ロゴ | scale 0.4→1.0 / opacity | spring | `{damping:14,mass:0.9}` |

> **全 opacity が translateY/scale/scaleX と対。等速線形を1箇所も使わない。**

## 11.3 レイヤー構成（下→上・主役 L4 の裏に L1/L2/L2b/L3 = 4層）

L0 `#0A0A0C` / L1 グラデ（`radial-gradient(120% 120% at 50% 35%, #17120E 0%, #100C0A 45%, #0A0A0C 100%)`）/ L2 グリッド（`${accent}22` 64px・放射マスク）/ L2b 督促の光（`linear-gradient(90deg, transparent, ${accent}cc, ${accent}55, ${accent}cc, transparent)`）/ L3 crimson 督促グロー（`radial-gradient(closest-side, #B23A4888, #B23A4822, transparent)` `blur(28px)`）/ L4 主役タイトル（Trail 包み・`overflow:hidden` span マスク・Anton `fontWeight:800 fontSize:150 letterSpacing:-2 color:#F5F7FA`）/ L5 下線＋サブ（Oswald `fontSize:38 letterSpacing:6 uppercase color:#C8CDD6`）/ L6 ロゴ（`linear-gradient(135deg, ${accent}, #ffffff22)`・`border:2px solid ${accent}`）。

## 11.4 確認方法（CLAUDE.md §5）

```bash
cd C:\Users\aab15\Documents\prime-documentary\remotion
npm run studio     # = remotion studio。OpeningCleveland を 0→180f でスクラブし §11.1 の各時刻を目視
npx remotion render OpeningCleveland out/cleveland_opening.mp4 --props=./props/cleveland.json
# props 差し替え量産
npx remotion render OpeningCleveland out/cleveland_short_op.mp4 --props=./props/cleveland_short.json
# 本編
npx remotion render Ep45Cleveland out/cleveland_final.mp4 --props=./src/data/cleveland_film.json --public-dir=public_slim --concurrency=4
```

---

# 12. props 定義と型（CLAUDE.md §4）

```ts
export type OpeningClevelandProps = {
  title: string;      // 主役タイトル。1文字ずつスタッガーで切れ上がる
  subtitle: string;   // サブタイトル。UPPERCASE 表示（facts_lock 検査対象）
  accent: string;     // アクセント（HEX6桁・"#"込み）。グリッド/督促の光/グロー/下線/ロゴに波及
  hasLogo: boolean;   // true で左上にロゴバッジ
};
```
**EP45 の確定 props（`remotion/props/cleveland.json`）:**
```json
{ "title": "THE PRICE OF BEING POOR", "subtitle": "BEARDEN V. GEORGIA, 1983", "accent": "#B23A48", "hasLogo": true }
```
**量産用 `remotion/props/cleveland_short.json`:**
```json
{ "title": "TOO POOR TO PAY", "subtitle": "JAILED FOR A FINE?", "accent": "#B23A48", "hasLogo": false }
```
> `accent` は **`#B23A48` 固定**（EP41 gold / EP42 blue / EP43 amber / EP44 teal の流用は BLOCKER）。`subtitle`/`title` は `facts_lock` 検査対象（「合法」断定・「全罰金違憲」・「最高裁が Cleveland を救った」を出さない。`BEARDEN V. GEORGIA, 1983`・疑問形 `JAILED FOR A FINE?` は制度説明として可・C1）。**サムネ headlines には F11/F13 の生数値（$1,554/$200/$40）を出さない**（帰属を焼けない＝R-HEDGE）。

---

# 13. 受入基準（EP45 の Definition of Done・★語数ゲートが最初・全編アイボール必須）

```bash
cd C:\Users\aab15\Documents\prime-documentary
# 0. 語数（最優先・課金前）
./.venv/Scripts/python.exe scripts/check_script_length.py episodes/PD-2026-045-cleveland/03_script/script.en.v001.md --json
# 1. 事実性（EP45固有・§1.3・6制約・dochighlight 0件）
./.venv/Scripts/python.exe scripts/check_cleveland_facts.py --json
# 2. ビート契約（AE↔figures 非重複・ledger・6制約・dochighlight 0件）
./.venv/Scripts/python.exe scripts/validate_cleveland_beats.py
# 3. 密度（★30 を Remotion 側で満たしていること・--ep 指定／--json は出力パス）
./.venv/Scripts/python.exe scripts/check_motion_density.py --ep PD-2026-045-cleveland --json runs/qc/cleveland_motion.json
# 4. VO速度（ナレ直後・ミックス前）
./.venv/Scripts/python.exe scripts/measure_vo_wpm.py --ep cleveland --json
# 5. 最終受入
./.venv/Scripts/python.exe scripts/check_final_acceptance.py 45 --render episodes/PD-2026-045-cleveland/08_edit/cleveland_final_bgm.v002_ae.mp4 --emit-receipt
```
> **ゲート入力は `--ep PD-2026-045-cleveland`。`--json <film.json>` を入力に使わない**（出力パス＝上書き事故。ブリーフ§5）。

| ゲート | 閾値 | EP45 設計値 |
|---|---|---|
| `check_script_length` | band 内 | 2,119語（SPEC・要 PASS 確認） |
| `runtime_band` | 690–750s | **726.4s = 12:06.4**（上限 750s に 23.6s 余裕） |
| `motion_density` | ≥2.5/min ∧ cov ≥0.25 ∧ variety ≥3 | **3.02/min / 0.272 / 8種**（film.json 36 beats・AE非依存・floor 30 に +6） |
| `animation_mix`（紙芝居） | still-share ≤45% ∧ motion cov ≥45% | **44.64% / 55.36%** |
| `check_asset_reuse` | first-use ≥0.70・still≤2・factory1・motion≤2 | **0.8571 / 2 / 1 / 2** |
| `footage_diversity` | distinct/total ≥0.40 | **0.8571** |
| `visual_asset_qc` | 全 factory 目視 reviewed | **92本 目視（CODEX_A）** |
| `image_resolution` | 長辺≥3840 | 全 SDXL ≥3840 |
| `bgm_present` | 無音>25秒ゼロ | 最長 2.2秒 |
| `caption_integrity` | 一致≥99%・カバー≥95% | §8.2 |
| `op_ed_bookends` | `BrandOpening`/`BrandEndcard` import・不変 | ✓ |
| `asset_manifest` | A↔B counts/role 一字一致・also_thumb 6（S01/S03/S18/S46/S68/S84）・overlay 12・schema `cleveland_assets.v1` | §5.8 |
| `facts_lock`（EP45固有・6制約） | violations=0・**dochighlight 0** | §1.2/§1.3 |
| **全編アイボール** | 12:06.4 を通しで目視 | ★1フレーム判定禁止（EP39-41/EP3941 の miss） |

---

# 14. premortem（失敗するとしたらここ）

| # | 失敗モード | 事前対処 |
|---|---|---|
| 1 | **番号ズレ**（別番号を発明） | シーンは S01..S48 固定（§3.2）。still 資産 ID は S01..S84（別空間・cross-map 禁止） |
| 2 | **紙芝居**（still-share 45%超・余裕 0.36%pt） | §5.1 で still-cut 100 固定・factory 92・i2v 32。still1つ増で 45% 割れ → cut を増やさず同一シーンの新規 distinct で回復 |
| 3 | **バリエーション水増し**（`--variants 3`） | §5.3。variants 指定なし＝1枚。ai_prompts は 84行＝84枚 |
| 4 | **密度 FAIL**（AEカードに頼る） | §6。film.json に 36 beats（30 超）。AE 8枠は composite 後で非カウント |
| 5 | **画像プロンプトが読めない**（0枚生成） | §9.1 の2行形式・`--only S01` で `shots=100`（body 84 + i2v種 16）確認 |
| 6 | **ファイル名信仰**（牛が本編に入る） | §5.4 factory 92本を `build_footage_contact_sheet.py` で全点目視（CODEX_A BLOCKING） |
| 7 | **6制約違反**（合法断定/全罰金違憲/最高裁が救った/Cleveland肖像/扇情/台帳外数値/投票数発明） | §1.2/§1.3 `check_cleveland_facts.py`。カード・figures・字幕・プロンプト全対象 |
| 8 | **dochighlight のバグ見え**（3回指摘） | §6.2/§7.3。`dochighlight`/`votetally`/`comparebars` を1件も置かない（R-DOCHL・grep 0） |
| 9 | **FigureBeats kind 大文字で無音描画** | §6.2 kind は全小文字（`compbars`・`comparebars` は非実在） |
| 10 | **AE em-dash 豆腐 / 等速 / OM名英語 / 文字切れ** | §7.6。テキスト幅は `sourceRectAtTime(t,false).width` 実測 |
| 11 | **id 誤り**（切り詰め・綴り違い等） | §0.1。`id="Ep45Cleveland"`・`caseFilmDurationInFrames(clevelandFilm,30)`=21792 |
| 12 | **accent 流用**（他話色を残す） | §0.5/§7.5/§12。OP props/AEカード/サムネ accent は `#B23A48` |
| 13 | **A↔B マニフェスト不整合**（role=thumb を作る/counts 不一致/schema 名違い） | §5.8。`cleveland_assets.v1`・role enum=`body/i2v_source/reject`・also_thumb 6（S01/S03/S18/S46/S68/S84）・overlay 12 を A/B 一字一致 |
| 14 | **EP39〜44 と素材被り** | §2 で6つの stock_ledger の sha256 を除外（`select_cleveland_factory.py --verify-no-prior-overlap`） |
| 15 | **fast端で 11分台 / 750s 超** | §4.1 speed 1.0 明示＋`measure_vo_wpm` 168–190・190超は破棄再発注。総尺 726.4s ≤750 の assert（§3.1[4]） |
| 16 | **AE ledger と figures の数値ズレ** | 数値は §1.4 台帳のみ。$1,554/$200/$40 は同一 payload に FFJC 帰属（R-HEDGE）。Bearden(最高裁) と Cleveland(2014和解) を同一 payload で直結しない（R-SCOTUS-SPLIT） |

---

# 15. 設計パッケージ接続（DESIGN → CODEX_A / CODEX_B）

- **DESIGN（本書）:** タイムライン（0〜713.9s 全区間・各Act・§3.1/§3.1b）・レイヤー（背面4層・§8）・モーション数値（§10）・48絵コンテ（§3.2/§9・象徴・6制約・扇情なし）・FigureBeats 設計（≥30＝36・小文字kind・変種≥3＝8種・dochighlight 0件・§6）・AEカード表（8枚・accent #B23A48・§7.3）・OP 仕様（§11）・asset_manifest スキーマの正（§5.8）。
- **CODEX_A（別ファイル `EP45_cleveland_CODEX_A_ASSETS.v001.md`）:** §9 を **84本の固有プロンプト**（1シーン1枚・variants 0）＋ i2v 16 ＋ factory 92 選定＆**全点目視QC**（`select_cleveland_factory.py`・`--exclude-used --ep PD-2026-045-cleveland` で EP39〜44 sha256 除外）＋境界契約 `asset_manifest.v001.json`（schema `cleveland_assets.v1`・counts を EP45 値 still_body84/still_i2v_source16/motion16/factory92・`stills[].role` enum=`body/i2v_source/reject`・also_thumb 6（S01/S03/S18/S46/S68/S84）・overlay 12）。
- **CODEX_B（別ファイル `EP45_cleveland_CODEX_B_BUILD.v001.md`）:** `build_cleveland_film.py`（＝`build_tekoh_film.py` を複製・ASSET_MAP/NARR/FACTORY_SEL/SLUG/EP を cleveland に・実素材のみ stub 禁止）／captions（実測 narration）／figures 36（小文字 kind・dochighlight 0件・§6）／`CaseFilm` を `id="Ep45Cleveland"` で Root.tsx 登録（`caseFilmDurationInFrames`＝21792）／`OpeningCleveland`／AEビルダ・コンポジタ（accent #B23A48・.aep>.jsx assert・レイアウト名は実装済み8種のみ・§7.3 の8カード＝本書 §7.3 と一字一致）・`validate_cleveland_beats.py`・`check_cleveland_facts.py`（EP44 版を複製・同名）／`build_cleveland_bgm.py`→`composite_cleveland_hero.py`（film_offset 適用）／レンダ（`--public-dir=public_slim --concurrency=4`）／全ゲート（`--ep PD-2026-045-cleveland`）／完成後の全編アイボール。
- **A↔B 接続点は `asset_manifest.v001.json` ただ1ファイル**（schema `cleveland_assets.v1`・counts/role enum を A/B 一字一致・§5.8）。
- **複製元（実在・EP42/44）→ cleveland 複製先:** `build_tekoh_film.py`→`build_cleveland_film.py` / `build_young_bgm_real.py`→`build_cleveland_bgm.py` / `ae/build_caniglia_hero_cards.py`→`ae/build_cleveland_hero_cards.py` / `ae/composite_caniglia_hero.py`→`ae/composite_cleveland_hero.py`（film_offset）/ `validate_caniglia_beats.py`→`validate_cleveland_beats.py` / `check_tekoh_facts.py`→`check_cleveland_facts.py`。**共有（複製不要）:** `generate_sdxl_4k.py` / `build_footage_contact_sheet.py` / `check_motion_density.py` / `measure_vo_wpm.py` / `check_script_length.py` / `check_final_acceptance.py`。**実在しないスクリプトを捏造しない（`ls scripts/` で複製元の実在を確認）。**
