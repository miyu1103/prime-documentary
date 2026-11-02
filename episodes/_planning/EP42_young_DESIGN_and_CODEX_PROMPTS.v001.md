# EP42 — THE WRONG HOUSE — 制作設計書（DESIGN 本体・v001・確定台本版）

- Episode ID: `PD-2026-042-young` / slug: `young` / EP42
- 中心の問い（英語・二人称）: **"If armed police break down the wrong door — your door — does the law owe you anything at all?"**
- 判例（制度説明としてのみ）: **Hudson v. Michigan, 547 U.S. 586 (2006)**（5–4・Scalia 執筆・Kennedy 第5票は別途同意）
- 主役: **Anjanette Young**（存命の私人＝**R2**）。象徴のみ・尊厳の物語。
- リスク区分: **R2/R3 混在**。全実在人物の顔・身体・肖像を一切描かない。Booker T. Hudson 本人（存命・薬物有罪＝**R3**）は人物化せず、Detroit の戸口/敷居の象徴のみ。
- Status: **BINDING**。**唯一の真実 = 機械生成済み `EP42_young_PRODUCTION_SPEC.v001.json`**。本書のあらゆる数値はそこからの転記で、手書きで発明していない。衝突したら SPEC が勝つ。
- このファイルは**設計パッケージ3分割**（DESIGN / CODEX_A / CODEX_B）の **DESIGN 本体**。共有ブリーフ `EP42_young_DESIGN_BRIEF.shared.md` を単一の真実源とする。85本の SDXL プロンプト実体・i2v 16・factory 93 選定は **CODEX_A**、build_young_film.py・captions・figures 実装・Root.tsx 登録・AEビルダ/コンポジタ・ゲートは **CODEX_B** に属す（本書は各所でポインタのみ示す）。

## ★このエピソードの唯一の真実（手書きで数値を発明するな）

`episodes/_planning/EP42_young_PRODUCTION_SPEC.v001.json`（台本から機械生成・`scripts/build_production_spec.py`）。本設計書は SPEC を**人間可読な実装指示に翻訳しただけ**で、新しい数字を作っていない。

```
words_total          = 2,140
narration_seconds    = 720.9   （= 12.0分）@ wpm_used 178.1
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

## ★★ 最重要の新前提: 1シーン1枚・バリエーション0 ★★（ブリーフ§1）

- Codex の画像生成は SDXL より高精度。**同一ショットの複数バリエーション（`_01/_02/_03`）を作らない。**
- `04_scenes/ai_prompts.v001.md` は **still 85本＝85行の固有プロンプト**（`generate_sdxl_4k.py` の `read_prompts()` 2行形式・各1枚）。**`--variants 3` は使わない**（`--variants 1` または variants 指定なし）。
- i2v モーション種は **16枚**（各1シード・これもバリエーション0）。
- 総生成画像 = **still 85 + motion seed 16 = 101枚（各1回）**。**factory 93 は生成ではなく在庫選抜**（全点目視QC・EP39/40/41 と sha256 被りゼロ）。
- **still を増やして factory を削るな**（still-share 0.4469 は cap 0.45 に対し余裕 0.31%pt しかない）。

## ★EP39/40/41 で踏んだ失敗＝本書が最初から潰す設計判断

| # | 失敗 | 本書での恒久対策 | 参照 |
|---|---|---|---|
| 1 | **番号ズレ**（別リストを発明） | シーンは **SPEC の S01..S48 に固定**。別番号体系を作らない | §3.2 |
| 2 | **紙芝居**（still 100% で animation_mix FAIL） | still-cut **101 固定**＋factory実写 **93**＋i2v **32**。still-share 44.69% ≤45% / motion cov 55.31% ≥45% を構造保証 | §5.1 |
| 3 | **バリエーション水増し**（36×3=108 で反復回避を偽装） | **1シーン1枚・85本を各1枚**。variants 禁止 | §5・§9 |
| 4 | **画像プロンプトのパーサ非互換** | `read_prompts()` の**2行形式**（`` - `S01.png` `` の次行に `... Avoid: ...`）。CODEX_A が `--only S01` で拾い数を確認 | §9 |
| 5 | **ファイル名を信じた**（牛が documents、大聖堂が監視カメラ） | factory 93本を `build_footage_contact_sheet.py` で**全点目視QC**（CODEX_A 必須・BLOCKING） | §5.4 |
| 6 | **AEカードを密度に数えた** | `check_motion_density` は film.json の `figures+graphics` だけ。**film.json 側に MGビート 31本以上**（本書は 37 設計）。AE は composite 後で 0 カウント | §6.1 / §7 |
| 7 | **一枚絵で完成判定**（EP39-41 の眼球不足） | 全編アイボール必須（§13）。measured > estimated | §13 |

---

# 0. 環境・Remotion設定（CLAUDE.md §0 準拠）

## 0.1 本編 `Ep42Young` の Composition 設定（★本編の正）

| 項目 | 値 |
|---|---|
| `id` | **`Ep42Young`**（Root.tsx に `CaseFilm` で登録。ブリーフ§5「Ep42Young登録」） |
| 解像度 | **1920 × 1080** |
| `fps` | **30**（EP41 thompson と同値を踏襲。フレームは全て `Math.round(30 × 秒)`・直書き禁止） |
| `durationInFrames` | **`caseFilmDurationInFrames(youngFilm, 30)` = 22002**（4項の実関数 `round(hookSeconds×30)+round(OPENING_SEC×30)+ceil(narrationSeconds×30)+round(ENDCARD_SEC×30)`・**hookSeconds=0**・§3.1[3] で算出。手書きで数値を入れず関数で算出する） |
| component | `remotion/src/compositions/CaseFilm.tsx`（既存の汎用 `CaseFilm` を再利用。`Bookends.tsx` の `BrandOpening`/`BrandEndcard` を **import**・fork 禁止） |
| data | `remotion/src/data/young_film.json`（`scripts/build_young_film.py` で再生成できる状態を保つ＝**git 未追跡**） |

**Root.tsx 登録（★ブリーフ§5・CODEX_B が実装）:**
```tsx
import {youngFilm} from './data/young_film.json';
import {caseFilmDurationInFrames} from './lib/caseFilmDuration';
// ...
<Composition
  id="Ep42Young"
  component={CaseFilm}
  width={1920} height={1080} fps={30}
  durationInFrames={caseFilmDurationInFrames(youngFilm, 30)}  // = 22002
  defaultProps={{film: youngFilm}}
/>
```
> **id は `Ep42Young`**（`42` の `4` を落とした形は誤記。ブリーフ§5 の render 行 `id="Ep42Young"` が正）。

## 0.2 タイトルバンパー `OpeningYoung` の Composition 設定（CLAUDE.md 正典部品準拠）

| 項目 | 値 |
|---|---|
| `id` | **`OpeningYoung`** |
| 解像度 | **1920 × 1080** |
| `fps` | **60**（CLAUDE.md §0 の正典値。OP 単体は 60fps） |
| `durationInFrames` | **180**（= 3.0秒 @ 60fps） |
| component | `remotion/src/compositions/OpeningYoung.tsx`（§11 全仕様） |

> `OpeningYoung` は**独立したタイトルバンパー成果物**（`out/young_opening.mp4`）。本編内 OP/ED の正典は `Bookends.tsx`（`BrandOpening` 3.50s / `BrandEndcard` 9.00s・不変）。`OpeningYoung` を本編に ffmpeg で焼き込まない（オーナー承認なしに見え方を変えない）。

## 0.3 必要な依存パッケージ

```bash
cd C:\Users\aab15\Documents\prime-documentary\remotion
npm i @remotion/motion-blur     # CLAUDE.md 必須依存（Trail によるモーションブラー）
```

## 0.4 `remotion.config.ts`（CLAUDE.md §0 正典値・EP41 と同一）

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

`brand.ts` 実値: ink `#0A0A0C` / navy `#0B1A2B` / electric `#1F6BFF` / silver `#C8CDD6` / gold `#E5B53A` / white `#F5F7FA`。フォント: display Oswald / number Anton / body Oswald。

**EP42 のパレット（★ダーク/シネマ・夜のシカゴ西部＋法廷大理石・レーン分離）:**
```
INK    = #0A0A0C   ルート背景
NIGHT  = #131A24   シカゴの夜（青灰ベース）
MARBLE = #3A4048   法廷の冷たい大理石
STEEL  = #2A2E33   ウォッシュ/ビネット寄り
ACCENT = #3B7DD8   warrant-blue（ブランド数値・ライン・グリッド・下線。冷たい制度色）
DAWN   = #C98A3A   ★唯一の暖色（割れる戸口の光・テレビの光・結末の夜明け）。実用光1つだけ
WHITE  = #F5F7FA
SILVER = #C8CDD6
RED    = #C74A3E   ★予備：`10–4 REJECTED` の取り消し／過失欄空白のみ
```
> **レーン分離:** EP39（electric・取調室）/EP40（gold amber・郊外昼光）/EP41（gold・鋼灰institutional）と被らないよう、EP42 は **冷たい warrant-blue `#3B7DD8` を基調＋ドア/夜明けの単一 DAWN 暖色**。接尾に `electric blue interrogation` `midday suburban` `steel grey death row` を含めない。**factory は EP39/40/41 の `stock_ledger*.json` の sha256 を除外**（CODEX_A・BLOCKING）。

---

# 1. 事実の取り扱い（★正確性6制約＝FACTS LOCK / `check_young_facts`・BLOCKING）

## 1.1 確定台本（唯一の正・1バイトも変えない）

```
C:\Users\aab15\Documents\prime-documentary\episodes\_planning\EP42_young_script.en.v001.md
```
**本番配置先:** `episodes/PD-2026-042-young/03_script/script.en.v001.md`（上記を1バイトも変えずコピー）。整形も禁止（AI臭再発と語数ゲート再計算を招く）。台本の幕構成（HOOK / OP / ACT1–4 / ENDING）と `【SILENCE …】`（4箇所）を正典とする。存在しない演出マーカー（`【OST:】`/`〔CARD:〕`）を発明しない。

## 1.2 ★正確性6制約（全出力＝プロンプト・カード文言・図表・字幕・タイトルに適用。1つでも違反＝BLOCKER）

| # | 制約 | 出力での順守 |
|---|---|---|
| **C1** | **和解 ≠ 責任認定** | 「裁判所が違憲/責任を認定」不可。使えるのは「市が **$2.9M** 支払いに同意・市議会が **48–0** で承認（と**報じられる**）」まで。カード・図表に必ず「**no finding of fault / not a verdict**」を併記 |
| **C2** | **no-knock 令状と断定しない** | 令状は「**search warrant（有効・判事署名）**」のみ。**カード/プロンプト/字幕/図表に文字列 `no-knock` を一切出さない**。進入前に「a shout at the door」（告知の存在）を象徴で残す |
| **C3** | **改革は否決・現行も合法** | Anjanette Young Ordinance は 2022/11 に **10–4 否決**・不成立。**文字列 `she changed the law` / 「法が変わった」を出さない**。カードは `REJECTED` / `STILL LEGAL` |
| **C4** | **Hudson の射程を圧縮しない** | knock-and-announce は今も第4修正の **"a command"**。否定されたのは救済としての証拠排除のみ。カードに `STILL A COMMAND` を明示。**文字列 `unconstitutional` を出さない**。Scalia の「民事訴訟で十分」論拠は Part IV=4名のみ・Kennedy は署名せず（figures/カードで「4票のみ」を可視化） |
| **C5** | **Booker Hudson を主役化しない**（R3・存命・薬物有罪） | 人物化せず、**Detroit の戸口/敷居の象徴のみ**。名は制度説明の言及に限定。人生・薬物・心情・その後・肖像に一切触れない |
| **C6** | **Young の着替え中/着衣なしは非グラフィック**（R2・実在私人） | 象徴のみ（開いたドア・散らばった書類・手錠・時計・足首モニタのアイコン・空席）。**顔・身体・肖像を一切描かない** |
| **R1** | **実在人物の顔・肖像を生成しない** | 全生成ビジュアル表示中は `AI-assisted visualization`（右下）常時表示。概要欄に1行 AI 開示 |

## 1.3 6制約ゲート `check_young_facts`（`scripts/check_young_facts.py`＝EP41 `check_thompson_facts.py` を young 用に複製。exit≠0 で出荷停止・CODEX_B 実装。出力 `facts_lock.v001.json`）

> **★ゲート名は1本に確定:** 6制約の機械ゲートは **`scripts/check_young_facts.py`**（出力 `09_package/facts_lock.v001.json`）ただ1つ。旧 EP 由来の別名（`*_accuracy` 系スクリプト・`*_lock` 別名）は一切使わない（DESIGN/CODEX_A/CODEX_B で同名参照）。下表の **L-C1..L-C5・L-R1** は `check_young_facts` の内部ルール **R-* に一本化**して実装する（対応: L-C1→R-SETTLEMENT / L-C2→R-FORBID / L-C3→R-FORBID＋Ordinance文脈 / **L-C4→R-C4**（C4 の "still a command"／Part IV=4／Kennedy 非署名の**積極**検証・CODEX_B §2.3）/ L-C5→R-HUDSON / L-R1→R-FACE/R-DOC）。

**検査対象:** `03_script/script.en.v001.md` / `remotion/src/data/young_film.json` の `figures[].text`・`figures[].lines[]` / `08_edit/ae_hero/beats.json` の `top`/`bottom`/`main`/`caption`/`footnote`/`left`/`right` / `09_package/*` / `remotion/props/young*.json` の `subtitle` / `04_scenes/ai_prompts.v001.md`。

| ルール | 内容 |
|---|---|
| **L-C1 和解帰属** | `settlement`/`$2.9M`/`48-0` を含む beat/figure に `no finding of fault` 系の語が同一カードに無ければ FAIL。「court found the city liable」等の断定語が出たら FAIL |
| **L-C2 no-knock禁止** | 全検査対象に文字列 `no-knock` / `no knock`（大小・ハイフン揺れ）が出たら **即 FAIL**。令状記述は `search warrant` のみ許可 |
| **L-C3 reform** | 文字列 `she changed the law` / `changed the law` / `new law` が出たら FAIL。Ordinance 文脈に `REJECTED` か `voted down` か `still legal` が無ければ FAIL |
| **L-C4 射程（→R-C4）** | 文字列 `unconstitutional` が出たら FAIL。`knock-and-announce` の近傍60字に `still a command` 系が無い×否定文脈 で FAIL。`exclusion` を「the rule itself was struck」と誤読させる語で FAIL。**さらに積極検証（R-C4）:** `still a command`（Scalia 帰属）が figures/AE に存在し、かつ Part IV=4票・Kennedy 非署名（F18 stat）が存在すること。無ければ FAIL |
| **L-C5 Hudson人物化** | `Booker`/`Hudson` の直後60字に `face`/`portrait`/`likeness`/`drug`/`his life`/`depicted as a man` が出たら FAIL |
| **L-R1 肖像** | `ai_prompts.v001.md` の正プロンプトに `portrait`/`face of`/`likeness of`/`recognizable`/`nude`/`undress`/`her body` が出たら FAIL（ネガティブでの使用は可） |

**出力:** `09_package/facts_lock.v001.json`（`{"pass":bool,"violations":[{"file","rule","line","excerpt"}],"skipped":[...]}`）。`pass:true` でない限り `check_final_acceptance.py` に進まない。

## 1.4 画面に出してよい確定数値（★台本に存在するものだけ。この表以外を画面に出すな）

| ID | 値 | 台本での表現（claim） | 使用先 |
|---|---|---|---|
| N01 | **CHICAGO — FEBRUARY 2019** | "February. Chicago."（C10・2019/2/21） | figures timeline（F01・AEカードにはしない） |
| N02 | **12 officers** | "Twelve officers, rifles up"（C13） | AE **n01**（CENTER_STACK）/ figures stat（象徴・拘束数は断定せず） |
| N03 | **~16 months** | "ran for roughly sixteen months"（C18） | AE **c01**（CENTER_STACK）/ figures |
| N04 | **~100 alleged / >12 officers** | "close to one hundred alleged violations … more than a dozen officers"（C18） | AE **c01**（"alleged" 必須） |
| N05 | **DECEMBER 2020** | "in December 2020, a CBS station … obtained"（C17） | figures timeline |
| N06 | **$2.9 million** | "two point nine million dollars"（C19） | AE **m01**（MONEY_STACK） |
| N07 | **DECEMBER 15, 2021** | "on December 15th, 2021, the City Council approved it"（C19） | figures timeline（F04・AEカードにはしない） |
| N08 | **48–0（reported）** | "approved it — reported as forty-eight to nothing"（C19） | figures stat（"reported"・"no finding of fault" 枠・C1・AEカードにはしない） |
| N09 | **5–3** | "fired by the city's Police Board … five to three"（C21・2023夏） | figures stat（Police Board · Wolinski・votetally には入れない＝R-SPLIT） |
| N10 | **10–4** | "voted it down, ten to four"（C22・2022/11） | AE **r01**（SPLIT_COMPARE・"REJECTED"・C3） |
| N11 | **3–5 seconds** | "wait only three to five seconds"（C07・Hudson） | figures numberticker（F16・制度説明・C5・AEカードにはしない） |
| N12 | **DETROIT, AUGUST 1998** | "Detroit, August 1998"（C07・記録/二次帰属） | figures timeline/pindropmap（F17） |
| N13 | **JUNE 2006 / 5–4** | "June 2006. The Court answers, five to four."（C01） | AE **v01**（VOTE_SPLIT） |
| N14 | **SECTION 1983** | "section nineteen eighty-three"（C05） | AE **e01**（CENTER_STACK）/ figures dochighlight/mechanism |
| N15 | **547 U.S. 586 (2006)** | 引用形式 | `09_package/description.txt` のみ（本文で読み上げない） |
| N16 | **"still a command"** | "still a command of the Fourth Amendment"（C04・逐語） | AE **k01**（QUOTE_CARD・Scalia 帰属）/ figures quote |

> **C25 反映（射程非圧縮の補強）:** Scalia の「専門職化・内部規律・民事訴訟で抑止十分」論拠は **Part IV = 4名のみ**賛同。第5票 **Kennedy** は別途同意し Part IV に加わらず「排除法則は疑いない」と明記。→ §7 figures の `votetally`/`compbars` で「4票のみ／Kennedy 署名せず」を可視化し、plurality 論拠を ruling と誤読させない。

---

# 2. 視覚・音響レーン分離（EP39/40/41 との素材被り回避）

> **EP39/40/41 のファイルには一切触れない（読み取りのみ可）。** レーンを機械的に分離する。

| 軸 | EP41 thompson | **EP42 young** |
|---|---|---|
| 舞台 | 独房・死刑囚房・法廷・最高裁 | **夜のシカゴ西部の室内（割れる戸口）→ 法廷の大理石・空の9席・使われないガベル → 市議会** |
| 時間帯 | 夜明け前の灰〜夜 | **夜（踏み込み）→ テレビの光 → 大理石の冷光 → 夜明けの戸口の光（結末）** |
| 支配的出来事 | 不作為・時間の堆積（14年） | **誤住所への踏み込み・映像の秘匿・救済の薄さ・否決** |
| アクセント色 | gold `#E5B53A` | **warrant-blue `#3B7DD8`（制度色）＋ 単一 DAWN `#C98A3A`（戸口/夜明け）** |
| ベース色 | 鋼灰 `#2A2E33`+near-black | **夜の青灰 `#131A24` + 大理石 `#3A4048` + near-black `#0A0A0C`** |
| レンズ感 | 正対・望遠圧縮 | **ACT1 断片・手持ち感／ACT3 正対・対称・荘厳／ENDING 引き（pull-back）** |
| 画像保存先 | `H:\pd-media\assets\ai\thompson\` | **`H:\pd-media\assets\ai\young\`** |
| Remotion データ | `thompson_film.json` | **`young_film.json`** |
| Remotion コンポ | `Ep41Thompson` | **`Ep42Young`** |
| AE 作業ディレクトリ | `…/PD-2026-041-thompson/08_edit/ae_hero/` | **`…/PD-2026-042-young/08_edit/ae_hero/`** |

**素材被り禁止:** EP39/40/41 と同一の factory clip / AI画像を1点も使わない。選定前に `episodes/PD-2026-039-*/` `…-040-*/` `…-041-*/` の `05_stock/stock_ledger*.json` を読み sha256 重複を除外（CODEX_A・BLOCKING）。

---

# 3. 尺と構成 — SPEC の値をそのまま使う

## 3.1 全区間タイムライン（★この表が唯一の正・秒は fps=30 から算出しフレーム直書き禁止）

**算出基準:** SPEC の `narration_seconds = 720.9`（マスター）を `young_film.json` の `narrationSeconds` に入れる。**手計算で上書きしない。** 各幕秒は SPEC `acts` テーブルの実測秒。フレーム = `Math.round(30 × 秒)`。

| # | ブロック | 役割 | 語数 | 幕秒(SPEC) | 台本指定の沈黙 | 固定尺 | 開始f | 終了f |
|---|---|---|---|---|---|---|---|---|
| 1 | **HOOK** | `hook` | 62 | 20.9 | **1.8**（"the wrong house." 後・末尾） | — | 0 | 627 |
| 2 | **BrandOpening** | `opening` | 0 | — | — | **3.50** | 627 | 732 |
| 3 | **OP ナレ** | `opening` | 55 | 18.5 | — | — | 732 | 1287 |
| 4 | **ACT1** The Wrong Door | `body` | 301 | 101.4 | **1.5**（"the next." 後・中） | — | 1287 | 4329 |
| 5 | **ACT2** The Tape | `body` | 282 | 95.0 | **0.9**（"On paper." 直前・末） | — | 4329 | 7179 |
| 6 | **ACT3** The Command | `body` | 657 | 221.3 | — | — | 7179 | 13818 |
| 7 | **ACT4** The Reach | `body` | 319 | 107.5 | — | — | 13818 | 17043 |
| 8 | **ENDING**（payoff→CTA） | `ending` | 331 | 111.5 | **1.0**（"real." 後・中） | — | 17043 | 20388 |
| 9 | **BrandEndcard** | `ending` | 0 | — | — | **9.00** | 20388 | 22002 |

> フレーム列は BrandOpening(105f)/BrandEndcard(270f) を実尺で挟み、幕秒を順に `round(30×秒)` で積んだ実装用アンカー。CODEX_B は `young_film.json` の segment 順から再計算し一致を確認。

### 検算（CODEX_B は必ず自分で再計算して一致を確認）

```
[1] narrationSeconds = 720.9（SPEC マスター。手計算で上書きしない）
    ※ 発話ブロック HOOK..ENDING の SPEC 幕秒合計 = 20.9+18.5+101.4+95.0+221.3+107.5+111.5 = 676.1s。
      SPEC マスター 720.9 との差 44.8s は、台本フロントマター語の配分＋幕間の息継ぎ＋
      設計無音4点（1.8+1.5+0.9+1.0=5.2s）を内包した測定マスター。film.json には 720.9 を入れる。
    ※ mean_shot 検算: 720.9 / 226 = 3.19s ＝ SPEC mean_shot_seconds 一致（226カットは 720.9s 全域に張る）。

[2] 総尺 = hookSeconds 0 + BrandOpening(OPENING_SEC) 3.50 + narrationSeconds 720.9 + BrandEndcard(ENDCARD_SEC) 9.00
        = 733.4 秒 = 12:13.4
    ※ hookSeconds=0（HOOK ナレは narrationSeconds 720.9 に内包・別建ての hook teaser preroll は作らない）。

[3] caseFilmDurationInFrames(youngFilm, 30) = 4項の実関数で算出（round(30×733.4) という単項近似ではない）:
      = round(hookSeconds×30) + round(OPENING_SEC×30) + ceil(narrationSeconds×30) + round(ENDCARD_SEC×30)
      = round(0×30)=0 + round(3.5×30)=105 + ceil(720.9×30)=21627 + round(9.0×30)=270
      = 22,002 フレーム
    ※ CODEX_B は young_film.json の hookSeconds/narrationSeconds（＋Bookends の OPENING_SEC/ENDCARD_SEC）から
      同関数で再計算し 22002 に一致することを assert する（§5.1・§3.1 検算）。

[4] runtime_band: standard 帯（manifest target 12分・band 11.5–12.5分 = 690–750s）
    総尺 = hookSeconds 0 + 733.4 = 733.4s
    → 733.4s = 12:13 は 690–750 の内側（上限 750s に対し 16.6s の余裕）    ✓ PASS
    ※ hookSeconds を 0 超（teaser 採用）にする場合は round(hookSeconds×30) を [3] に加え、
      総尺 = 733.4 + hookSeconds を再検算して **≤ 750s** を再確認すること（BLOCKING）。
```
> **VO 実測で確定:** `measure_vo_wpm`（合格帯 168–190 wpm）でナレ実測。実測が SPEC マスターと乖離したら CODEX_B は `narrationSeconds` を実測値で更新（planning は 720.9・final は実測が権威）。190超は破棄・speed 0.95 で再発注（BLOCKING）。

## 3.2 シーン→幕の割当（★SPEC の S01..S48 を固定・別番号を発明しない・48シーン）

各シーンは narrative beat。226カットを 48シーンに分散（平均 4.71カット/シーン）。`primary` は各シーンの主素材（still=SDXL 各1枚 / factory=実写 / motion=i2v）。ambient/繋ぎは factory を各シーンに撒く（§5.1）。**象徴のみ・6制約順守。絵コンテ級の記述は §9。**

> **★2つの `Sxx` 名前空間は別物（取り違え禁止）:** 本節の **narrative シーンは `S01..S48`**（この表の絵コンテ）。一方 **still 資産 ID は `S01..S85`**（CODEX_A §2 注記・1プロンプト=1枚で48シーンに85枚を配分）。同じ `Sxx` 表記でも DESIGN §3.2/§9 の Sid（narrative）と CODEX_A/asset_manifest の scene_id・covers_scene_id（still 資産 ID）は指すものが異なる。横断参照時は「どちらの空間か」を明示し、cross-map しない。

| Sid | 幕 | 内容（象徴・6制約） | primary |
|---|---|---|---|
| S01 | HOOK | 暗闇で戸口の枠が内側へ割れる／木片・切れるチェーン錠。人物なし | **motion** |
| S02 | HOOK | 素の床に開いた手錠が1つ、上の壁時計が深夜を指す。冷たい夜の青 | still |
| S03 | OP | 素の玄関ドアを正対で／intact・slow push-in・背後にグリッド線 | still |
| S04 | ACT1 | 西部の集合住宅の室内＝象徴空間。半開の戸棚・椅子に掛かった上着・散らばる書類 | still |
| S05 | ACT1 | 画面上の市街地図に足首モニタの光点が**別住所**で光る（本来の対象者の所在） | **motion** |
| S06 | ACT1 | 机上の search warrant（判事署名・判読不能／redacted）＝有効だが誤情報 | still |
| S07 | ACT1 | 夜の住宅街の戸口・冷たい引き（establishing・ambient） | factory |
| S08 | ACT1 | ドアが内側に破れフラッシュライトが走る＝断片・速い・顔なし | **motion** |
| S09 | ACT1 | 落ちた上着と床の手錠1つ＋散らばる書類＝拘束の非グラフィック示唆（身体なし） | still |
| S10 | ACT1 | 胸のボディカメラの録画ランプが点る（機器のみ・顔なし）＝全時間録画 | still |
| S11 | ACT2 | 赤い留め紐で封じたマニラ封筒＝秘匿された映像（判読不能） | still |
| S12 | ACT2 | 無人の法廷回廊・冷たい大理石＝映像秘匿の争い（ambient） | factory |
| S13 | ACT2 | 黒塗りの申立書（弁護士制裁）＝判読不能テキスト（facts_lock） | still |
| S14 | ACT2 | 暗い居間で光るテレビ（2020/12 放映）＝抽象的なグロー・画面に認識可能像なし | **motion** |
| S15 | ACT2 | 多数の暗い窓に1つだけ灯り＝全国が「その部屋の中」に立つ | still |
| S16 | ACT2 | COPA 調査＝案件フォルダの山＋壁時計 ~16か月／`~100 ALLEGED`（疑い・認定でない） | still |
| S17 | ACT2 | 冷光の空の演壇とマイク＝謝罪「on paper」。落差（0.9s 無音へ） | still |
| S18 | ACT3 | 大理石の壁を走る光の帯＝第4修正の一文（碑文的・判読不能・象徴） | **motion** |
| S19 | ACT3 | 無人の最高裁法廷＝9つの空席・正対対称・冷光 | still |
| S20 | ACT3 | 使われず置かれたガベル＝抑制の象徴 | still |
| S21 | ACT3 | Detroit の古い木の敷居/戸口（generic・Hudson 本人は描かない・C5）。有効令状の含意 | still |
| S22 | ACT3 | 敷居に差す光が 3–5秒 のあいだゆっくり動く＝進入前の待機（制度説明・人物なし） | **motion** |
| S23 | ACT3 | 大理石面が硬い影の線で大小2つに割れる＝5–4 の分割（顔・文字なし・抽象） | still |
| S24 | ACT3 | 暗い机上の意見書の一段落が光に浮くが判読不能＝narrow な判示 | still |
| S25 | ACT3 | 壁に彫られた命令が**なお立っている**＝knock-and-announce は今も "a command"（C4・射程非圧縮） | still |
| S26 | ACT3 | 証拠トレイが机に**残る**（証拠は排除されない）＋開いたままの法廷の戸＝救済のみ除去・規則は健在 | still |
| S27 | ACT3 | 天秤＝benefits vs "heavy social costs" の秤量（抽象大理石・文字なし） | still |
| S28 | ACT3 | 4席が灯り・1席だけ離れて灯る＝plurality（Part IV=4）と Kennedy の別票（中立・C25） | still |
| S29 | ACT3 | 無人のベンチに積まれたページ＝反対意見（Breyer 他3名・中立帰属） | still |
| S30 | ACT3 | 暗い大理石の広間に1つだけ開いた戸＝`SECTION 1983`＝残る唯一の救済（民事） | still |
| S31 | ACT3 | 遠い法廷の戸へ向かう匿名のシルエット（顔なし）＝負担を負う本人・弁護士・望み | still |
| S32 | ACT3 | 夕暮れの最高裁の列柱・大理石の石段（establishing・ambient） | factory |
| S33 | ACT4 | 2つの別々の戸口が並ぶ＝Hudson（訴追された被告）と Young（無関係私人）＝同じ戸でない | still |
| S34 | ACT4 | 机上の和解小切手（金額は判読不能）＋隣に過失欄が**空白のまま**のページ（C1） | still |
| S35 | ACT4 | 市議会の投票掲示板が `48–0` に確定（**reported** 枠）＝承認。責任認定でない | **motion** |
| S36 | ACT4 | 無人の議場と演壇＝「静けさを買った、評決ではない」 | still |
| S37 | ACT4 | 警察委員会＝1枚の名札が外れ（Wolinski 解雇 5–3・2023夏）多数の名札は残る（顔なし・中立） | still |
| S38 | ACT4 | 押印され脇に置かれた Anjanette Young Ordinance＝計画書/30秒/子の保護のアイコン（判読不能） | still |
| S39 | ACT4 | 委員会の掲示板が `10–4` に確定＋`REJECTED` の押印モーション＝否決・現行も合法（C3） | **motion** |
| S40 | ACT4 | 脇に置かれた条例が影に沈む＝直そうとした慣行は**今も合法**。戸口モチーフは不変 | still |
| S41 | ENDING | 冒頭(S03)と同じ玄関ドア＝今は閉じて静か・夜明け前 | still |
| S42 | ENDING | 和解小切手を再掲＝「金は受け取れるかもしれない」$2.9M（判読不能） | still |
| S43 | ENDING | 過失欄が空白のページ＝「金は何も認めなかった」（1.0s 無音域・C1） | still |
| S44 | ENDING | S18 の第4修正の光の帯を回帰＝「なお、判所の言葉で "a command"」背後に何もない（C4） | still |
| S45 | ENDING | 壁時計を再掲（HOOK 回帰）＝過ぎた時間・静けさ | still |
| S46 | ENDING | 閉じた玄関ドアの下から暖かい夜明けの光が育つ＋slow pull-back（単一の暖色 DAWN・人物なし） | **motion** |
| S47 | ENDING | 空の椅子/回されたマイク＝「We were wrong, and it was your door.」が言われない席（象徴） | still |
| S48 | ENDING | 夜明けの住宅街に1つ灯る窓＝未解決の余韻・CTA 域（establishing・ambient） | factory |

**source 集計（scene-primary）:** motion-primary **7**（S01 S05 S08 S14 S18 S22 S35 S39 S46 … の代表 9 のうち i2v が意味を持つ核）／factory-primary **4**（S07 S12 S32 S48）／still-primary 残り。**scene-primary はカット全体の一部**で、残りは §5.1 の配分に従い CODEX_B の shotlist が 226 カット（still 101 / factory 93 / motion 32）へ機械展開する。**この表のシーン数・番号は固定（S01..S48）。**

---

# 4. 音の4層設計（ナレ / BGM / SFX / 環境音）

## 4.1 ラウドネス・voice（確定値・EP41 と同一運用）

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

## 4.2 【SILENCE】4箇所の実装（★デジタル無音にしない・`bgm_present` を落とす）

台本の `【SILENCE …】` は**ナレの沈黙であって音の沈黙ではない**。

| 位置 | 秒 | 対応画 | 鳴らすもの |
|---|---|---|---|
| HOOK 末 "the wrong house." 後 | **1.8** | S02（手錠と時計） | BGM mute。**SFX door-frame tail のみ**（割れた戸口の残響）。デジタル無音にしない |
| ACT1 中 "She says it to the next." 後 | **1.5** | S10（ボディカメラの録画） | BGM mute。**SFX bodycam room-tone のみ**（録画が回り続ける室内音） |
| ACT2 末 "On paper." 直前 | **0.9** | S17（空の演壇） | BGM mute。**SFX 微細な室内トーン**。落差で "On paper." を効かせる |
| ENDING 中 "For Anjanette Young, it was real." 後 | **1.0** | S43（空白の過失欄） | BGM mute。**SFX 紙の擦れ tail のみ** |

**最長無音候補 1.8秒 << 25秒** ✓ `bgm_present` PASS。4区間ともデジタル無音にせず残響/室内ベッドを残す。

## 4.3 章ごとの BGM（1章1トラック・8カテゴリ・`build_young_bgm.py`＝EP41 bgm builder を young 用に複製）

| 区間 | 性格 | 楽器 |
|---|---|---|
| HOOK | 低弦の不解決・現在形の緊張。単音が刺す | 低弦+単音メタル |
| OP | ブランドスティンガー（`BrandOpening` 付属） | — |
| ACT1 | 速く・断片的・踏み込みの圧。ドアの木質パーカッション | 低弦+パーカッション |
| ACT2 | テレビの光・秘匿の冷たさ。疎なピアノ | ピアノ+弦 |
| ACT3 | 法の機械性・大理石の荘厳。**最も遅い**。僅差の緊張 | 低弦+弦サステイン |
| ACT4 | 小切手・議会・否決の乾いた射程。室内的で近い | ピアノ+弦 |
| ENDING | 解決しない和音 →「dawn light」でだけ暖色に開く | ピアノ+弦 |
| ENDCARD | ブランドED（`BrandEndcard` 付属） | — |

## 4.4 SFX

| 種別 | 位置 | 音 |
|---|---|---|
| door-frame break | HOOK/S08・【SILENCE】HOOK末 | 戸枠が割れる/残響・-14 LUFS |
| bodycam tone | S10・【SILENCE】ACT1中 | 録画が回る室内音・-28 LUFS |
| impact | AE v01/m01/n01 の数値着地 | 低域インパクト・-12 LUFS |
| tick | カウントアップの桁変化 | 微細クリック・-24 LUFS |
| paper | 封筒・条例・小切手・過失欄のカット | 紙擦れ・-22 LUFS |
| stamp | S39 `REJECTED` の押印 | 木/ゴム印の一撃・-16 LUFS |
| room tone | 全編ベッド（室内・大理石の反響） | 広いリバーブ・-30 LUFS |

---

# 5. ビジュアル — 素材積算（★紙芝居回避＝factory実写を必ず混ぜる・1シーン1枚）

## 5.1 素材の積算（★SPEC の値をそのまま満たす配分）

```
[0] 絵が必要な区間 = narrationSeconds 720.9（BrandOpening/Endcard は Bookends が別レイヤー）
[1] 総カット = 226（SPEC）    720.9 / 226 = 3.19秒/カット  ✓ mean_shot 3.19（≤6.0）
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
[8] factory 下限 = 720.9/30 = 24.03 → ≥25本。設計値 93本   ✓
```
> **[6] の余裕は 0.31%pt しかない。still-cut を1つ増やすと 45% を割る。still-cut は 101 で固定**（16枚だけ2回・残り69枚1回）。QC で still が 85枚を割ったら §9 の**追加は同一シーンの別プロンプト（新規 distinct）**で回復させ、**cut 数は増やさない**。**still を増やして factory を削るな。**

## 5.2 SDXL と実写在庫の振り分け

- **SDXL（still 85・各1枚）= この事件にしか無い固有物**: 割れる戸口・室内の象徴・足首モニタ地図・search warrant（判読不能）・ボディカメラ・封じた封筒・黒塗り申立書・テレビの光・COPA フォルダ・第4修正の光帯・9つの空席・ガベル・Detroit の敷居・5–4 の分割・SECTION 1983 の戸・和解小切手/空白過失欄・投票掲示板・名札・条例・夜明けのドア。
- **factory 実写 93 = どこにでもある周辺**: 夜の住宅街・法廷回廊・大理石外観/列柱/石段・窓と光の移ろい・議場外観・夜明けの街・石とコンクリートのテクスチャ・ambient 繋ぎ。

## 5.3 SDXL 生成量（★バリエーション0・variants 禁止）

- `ai_prompts.v001.md` = **body 85行の固有プロンプト**（still 各1枚）＋ 下記 i2v 種 **16行** ＝ **計101エントリ**（`--only S01` の `shots=` は 101）。`generate_sdxl_4k.py PD-2026-042-young`（**`--variants 1` または指定なし**）。**`--variants 3` を書かない。**
- i2v-source = **16枚**（動きが意味を持つ絵の固有プロンプト・各1シード）。CODEX_A が Wan 2.2 A14B → RIFE 48fps で 16本生成。
- **総生成 = still 85 + i2v seed 16 = 101枚（各1回）。** factory 93 は生成せず在庫選抜。
- プロンプト実体（85本）・i2v リスト（16）・factory 選定（93）は **CODEX_A** の担当（本書 §9 は絵コンテ級の記述と共通スタイル/ネガティブの契約のみ）。

## 5.4 factory のファイル名を信じない（★必須工程・CODEX_A・BLOCKING）

> EP36: `city_surveillance_camera_dome` が実際は大聖堂。EP38: 牛が `documents_on_desk`。ラベルは検索語の記録であって中身の保証ではない。

選定した **93本すべて**を `scripts/build_footage_contact_sheet.py --ep PD-2026-042-young --media video --dir <factory staging>` で1本1フレームのラベル付きコンタクトシート（`runs/qc/young_footage_contact_NN.png`）にし**全点目視**。subtype と食い違う本は差し替える。

## 5.5 共通スタイル接尾（各 SDXL プロンプト末尾に必ず付ける・`[STYLE]`）

```
, cinematic still, cold desaturated institutional grade, Chicago-night blue-grey and cold marble with near-black shadows, a single warm practical light (a doorway or a dawn) as the only warmth, faintly blue cold shadows, deep shadow detail retained, frontal symmetry with restrained telephoto compression, ultra-detailed, photoreal, 4K, 16:9, fine film grain, no text, no watermark, no logo
```
> EP39/40/41 との分離: 接尾に `electric blue interrogation`（EP39）・`midday suburban bleached daylight`（EP40）・`steel grey death row cellblock`（EP41）を**一切含めない**。

## 5.6 共通ネガティブ（各 SDXL プロンプトの `Avoid:` に必ず付ける）

```
text, words, letters, numbers, captions, watermark, logo, readable document, legible warrant or court paper, real celebrity, recognizable real person, identifiable face, portrait, mugshot, likeness of a specific person, nude, undressing, exposed body, cartoon, illustration, 3d render, low quality, blurry, deformed, extra limbs, gore, blood pool, corpse, midday suburban daylight, electric blue interrogation, cellblock death row
```

## 5.7 AI開示（強め・毎回・R1）

AI 生成の still・i2v が画面に出ている間、常時右下に **`AI-assisted visualization`**（破壊/踏み込みの再現度が高い画は **`Artistic reconstruction — AI-assisted`**）。Oswald 20px / `#C8CDD6` / opacity 70% / 位置 `[W-32, H-28]`。字幕帯と縦 56px 以上離す。概要欄1行: `Some visuals in this film are AI-assisted reconstructions, not photographs of the actual events.`

---

# 6. After Effects ヒーロービート（8枠）— ★AEカードは密度に数えられない

## 6.1 大原則（★EP39/40 の致命傷を回避）

`check_motion_density` は **film.json の `figures+graphics` だけ**を数える。AE の 8枠は本編 mp4 に composite された後に焼き込まれるため gate は 0 カウント。→ **密度下限 31 は §7 の Remotion figures/graphics（37本）で満たす。** AE はその上に載る「決め所の数値タイポ」。

## 6.2 パイプライン（EP38/40/41 で measured 済み・young 用に複製）

```
[1] Remotion で本編完成 → young_final_bgm.v001.mp4（音声ミックス済み）
[2] scripts/ae/build_young_hero_jsx.py（＝build_thompson_hero_jsx.py を複製）が beats.json と young_hero.jsx を生成
[3] AfterFX -noui -r young_hero.jsx → 各ビートを 1920x1080@30fps の不透明 mp4 で書き出し
[4] scripts/ae/composite_young_hero.py（＝composite_thompson_hero.py を複製）が ffmpeg overlay + enable='between(t,start,end)' で焼き込み
[5] 出力 → young_final_bgm.v002_ae.mp4（v001 は絶対に上書きしない）
```

## 6.3 スロット確定表（§1.4 の確定数値のみ・8枠・6制約適用・数値は台帳照合）

| ID | 内容 | 数値ID | レイアウト | カウント型 | 尺 | 対応台本行 |
|---|---|---|---|---|---|---|
> **★レイアウトは複製元 `build_young_hero_cards.py` が実装する8種のみ**（`DATE_STAMP`/`CENTER_STACK`/`MONEY_STACK`/`SPLIT_COMPARE`/`ACT_TITLE_CARD`/`QUOTE_CARD`/`VOTE_SPLIT`/`SEAM_TRANSITION`）。**この表と CODEX_B §7.2 のデッキは id・レイアウト・F-ID が完全一致**（`validate_young_beats` が両方を突き合わせる）。上記8種以外の未実装レイアウト名は使わない。

| ID | 内容 | 数値ID | レイアウト（実装済み8種） | カウント型 | 尺 | 対応台本行 |
|---|---|---|---|---|---|---|
| **t01** | 幕1 THE WRONG DOOR | — | **ACT_TITLE_CARD** | なし | 5.0 | （ACT1 幕頭） |
| **n01** | 踏み込み人数 | N02 | **CENTER_STACK** | なし | 6.0 | "Twelve officers, rifles up" |
| **c01** | 監督調査 | N03/N04 | **CENTER_STACK** | なし | 6.0 | "roughly sixteen months … close to one hundred alleged violations" |
| **k01** | なお命令（逐語） | N16 | **QUOTE_CARD** | なし | 7.0 | "still a command of the Fourth Amendment." |
| **v01** | Hudson 判決 5–4 | N13 | **VOTE_SPLIT** | なし | 7.5 | "June 2006. The Court answers, five to four." |
| **e01** | 残る救済 | N14 | **CENTER_STACK** | なし | 6.0 | "section nineteen eighty-three" |
| **m01** | 和解額 | N06 | **MONEY_STACK** | `CT_MONEY` | 7.0 | "two point nine million dollars" |
| **r01** | 条例 否決 | N10 | **SPLIT_COMPARE** | なし | 6.5 | "voted it down, ten to four" |

### 検算

```
[1] 単調増加・重複ゼロ（start は §6.4 beats.json で幕位置に配置・台本行の秒に一致）
[2] HOOK / BrandOpening / ENDING payoff / BrandEndcard に1秒も重ならない
[3] 合計 = 5.0+6.0+6.0+7.0+7.5+6.0+7.0+6.5 = 51.0秒 / 733.4 = 7.0%   ✓ 過剰でない
[4] レイアウト種類 = ACT_TITLE_CARD, CENTER_STACK, QUOTE_CARD, VOTE_SPLIT, MONEY_STACK, SPLIT_COMPARE = 6種（全て実装済み8種内）   ✓ ≥3
[5] figures[] 34枠と1秒でも重ならない（validate_young_beats.py が両方突き合わせ・§7.3）
```

## 6.4 `beats.json`（`08_edit/ae_hero/beats.json`・`schema_version: "young_beats.v1"`・EP41 と同一スキーマ）

**確定ラベル（★ASCII のみ・em-dash 禁止＝`-` に置換・全大文字・6制約適用）:**
```
t01 ACT_TITLE_CARD  title="THE WRONG DOOR"  kicker="ACT ONE"               # 幕頭・still=割れる戸口
n01 CENTER_STACK    top="THE RAID"  main="ABOUT 12 OFFICERS"
        bottom="ONE WRONG ADDRESS"                                        # C2: search warrant のみ・no-knock 語なし
c01 CENTER_STACK    top="THE OVERSIGHT INVESTIGATION"  main="~16 MONTHS"
        bottom="~100 ALLEGED VIOLATIONS - NOT FINDINGS"                   # C1趣旨: alleged・認定でない
k01 QUOTE_CARD      quote="STILL A COMMAND OF THE FOURTH AMENDMENT"
        attribution="JUSTICE SCALIA, FOR THE MAJORITY"                    # C4: 逐語・命令はなお有効・unconstitutional 語なし
v01 VOTE_SPLIT      top="HUDSON v. MICHIGAN - JUNE 2006"  left="5"  right="4"
        bottom="THE REMEDY REMOVED - NOT THE RULE"                        # C4: 射程非圧縮・unconstitutional 語なし
e01 CENTER_STACK    top="THE REMAINING REMEDY"  main="SECTION 1983"
        bottom="A CIVIL SUIT - NOT EXCLUSION"                             # C4/N14: 残る救済＝民事
m01 MONEY_STACK     top="THE CITY AGREED TO PAY"  value=2900000 prefix="$" thousands=true
        bottom="A SETTLEMENT - NO FINDING OF FAULT"                       # C1: 責任認定でない
r01 SPLIT_COMPARE   top="ANJANETTE YOUNG ORDINANCE - NOV 2022"  left="10"  right="4"
        bottom="REJECTED - STILL LEGAL"                                   # C3: 法は変わっていない
```
> **m01 の "NO FINDING OF FAULT" は削除禁止**（C1）。**r01 の "STILL LEGAL" は削除禁止**（C3）。**k01/v01 に `unconstitutional` を入れない**（C4）。**k01 の attribution は §2 `APPROVED_QUOTES` の "still a command"→"Justice Scalia, for the majority" と一致**（R-ATTRIB）。**全カードに文字列 `no-knock` を入れない**（C2）。48–0（N08）と 3–5秒（N11）は AE カードにせず figures 側で扱う（§7.2）。`CT_MONEY` は thousands=true（`$2,900,000`）。カウント終了から区間終端まで最低 1.20秒ホールド。
> **★AI開示レイヤー（R1・全カード常時）:** 共通レイヤースタック（§6.5）に `AI-assisted visualization`（Oswald 20px / SILVER `#C8CDD6` / opacity 70% / 右下 `[W-32, H-28]`）を1枚追加し全カードに焼く。AEカードは不透明の全画面 mp4 として本編に overlay され本編右下の開示を覆うため、これが無いと AI生成 static 背景が開示なしで表示される（R1 違反）。`validate_young_beats` と §13 受入アイボールで「AEカード表示中も開示が見える」を確認。

## 6.5 レイアウト定義（EP41 §6.5 を踏襲・色定数のみ EP42 値）

**共通レイヤースタック（下→上）:** L9 黒ソリッド → L8 静止画（scale fill→fill×1.08・drift）→ L7 グレードウォッシュ（**冷色** `addSolid([0.075,0.102,0.141])`＝NIGHT / MULTIPLY / opacity 30）→ L6 羽根付き楕円ビネット → L5 グロー（下中央 DAWN 実用光 ADD）→ L4 ライトスイープ（`"ADBE Rotate Z"`=18）→ L3 上ラベル（Oswald）→ L2b アクセントライン（ACCENT warrant-blue・scaleX ワイプ・`motionBlur=true`）→ L2 主数値/主文字（Anton・ACCENT・`motionBlur=true`）→ L1b 下ラベル → L1 字幕ロワーサード → **L0b AI開示テキスト（`AI-assisted visualization`・Oswald 20px・SILVER `#C8CDD6`・opacity 70%・右下 `[W-32, H-28]`・全カード常時焼き＝R1）** → L0 黒シームディップ（head/tail 各4フレーム）。

**色定数（0..1 float）:**
```python
ACCENT = [0.231, 0.490, 0.847]   # #3B7DD8 — warrant-blue（数値・下線）
WHITE  = [0.961, 0.969, 0.980]   # #F5F7FA
SILVER = [0.784, 0.804, 0.839]   # #C8CDD6
DAWN   = [0.788, 0.541, 0.227]   # #C98A3A — 単一実用光のグロー
NIGHT  = [0.075, 0.102, 0.141]   # #131A24 — ウォッシュ寄り
RED    = [0.780, 0.290, 0.243]   # #C74A3E — r01 REJECTED の取り消し線のみ
```
**フォント:** 数値/主文字 = **Anton Regular** / ラベル・字幕 = **Oswald Medium**。`getFontsByFamilyNameAndStyleName` で厳格解決（miss は throw・フォールバック禁止）。テキスト幅は **`sourceRectAtTime(t,false).width` で実測**（advance-width 推定禁止＝EP40 文字切れの原因・ブリーフ§5）。

**カウント型:** `CT_MONEY`（thousands true / prefix "$"）のみ本編で使用（**m01**）。ease-out cubic で settle。v01/r01 の `5-4`/`10-4` はカウントせず**静的タイポ**（得票のためカウント不可）。

## 6.6 このマシン固有の罠（★1つ忘れると無言で品質が落ちる・EP41 §6.6 全13件を young に適用）

フォント解決の例外ラップ（`psName()`）／spatial ease は配列次元1（`prop.isSpatial ? 1 : ...`）／OM=`"H.264 - レンダリング設定を一致 - 15 Mbps"`・RS=`"最良設定"`（英語名は try/catch フォールバック）／`app.newProject()` を headless で使わない（同名 `YOUNG_` コンプを防御削除）／`layer.motionBlur=true` を動くレイヤー個別に／回転は `"ADBE Rotate Z"`／改行は1行厳守（COMPARE の2値は別レイヤー）／em-dash は `-`／inPoint と outPoint 両方設定／`item.mainSource.conformFrameRate = 30`／実行パス `C:\Program Files\Adobe\Adobe After Effects 2026\Support Files\AfterFX.exe`／`proj.gpuAccelType = GpuAccelType.SOFTWARE`／ビルド ~100–120秒・完了マーカー `render/_build_ok.txt` をポーリング（タイムアウト≥300秒）・末尾で `app.quit()`／**aerender 前に `.aep` mtime > `.jsx` を assert**（ブリーフ§5）。

## 6.7 コンポジタ（`scripts/ae/composite_young_hero.py`・SKIP 4条件を1つも削らない）

`BASE = young_final_bgm.v001.mp4` / `OUT = young_final_bgm.v002_ae.mp4`（v001 不変）。SKIP: (1) `render/<id>.mp4` 不在 / (2) 解像度≠1920x1080 / (3) 実測尺 `< dur-0.3` / (4) `beat.end > base_dur`。ffmpeg: `overlay=0:0:eof_action=pass:enable='between(t,start,end)'` / `-c:v libx264 -preset slow -crf 16 -pix_fmt yuv420p -colorspace bt709 -c:a copy`。**出荷済みを絶対に上書きしない。**

---

# 7. Remotion MGビート（FigureBeats）— ★密度下限 31 は必ずここで満たす

## 7.1 密度の設計（`young_film.json` の `figures[]` ＋ `graphics[]`）

`check_motion_density`: 3つを AND。**body-minutes = narrationSeconds/60 = 720.9/60 = 12.015**。

| 指標 | floor | EP42 設計値 |
|---|---|---|
| density | ≥2.5/min | figures 34 + graphics 3 = **37 beats / 12.015 = 3.08/min** ✓（SPEC beats_floor 31 に +6） |
| coverage | ≥0.25 | 37 beats × 平均 6.0秒 = 222秒 / 720.9 = **0.308** ✓ |
| variety | ≥3 distinct forms | **12種**（下記） ✓ |

> **AE の 8枠は film.json に入れない**（composite 後に焼くため gate 非カウント）。**density は Remotion 側 37 beats だけで 31 を超える。**

## 7.2 `figures[]` の種類配分（★kind は全部小文字・同一 kind を連続させない・ブリーフ§5）

**使用可能 kind（全小文字）:** `numberticker` `timeline` `bar` `kinetic` `acttitle` `lowerthird` `dochighlight` `routemap` `pindropmap` `regionmap` `compbars`（※`comparebars` は存在しない）`mechanism` `quote` `stat` `votetally`。**大文字は無音描画になる。**

| kind（小文字） | 枠数 | EP42 での用途（6制約適用） |
|---|---|---|
| `acttitle` | 4 | ACT1–4 の幕頭 |
| `timeline` | 5 | 2019/2 踏み込み→2020/12 CBS 放映→~16か月 COPA→2021/12/15 和解／Hudson 1998/8→2006/6／2022/11 否決→2023 Wolinski |
| `stat` | 7 | 12 officers・~16 months・~100 **alleged**・3–5 seconds・**$2.9M（label に "reported · no finding of fault" を同梱＝C1・R-SETTLEMENT）**・"almost two years" 待機・**5–3 Wolinski（Police Board・N09・votetally には入れない）** |
| `quote` | 3 | ①"still a command of the Fourth Amendment"（**逐語・多数意見に中立帰属**）②Kennedy 別途同意「exclusionary rule … not in doubt」（逐語・帰属）③Breyer 反対（逐語・**dissent** 帰属）。**要約を引用符に入れない・facts_lock で逐語確認** |
| `dochighlight` | 3 | search warrant（有効・判事署名・判読不能・C2）／`SECTION 1983`＝残る救済（N14）／過失欄が**空白**のページ（C1） |
| `lowerthird` | 2 | 帰属カード「reported as 48–0」（C1）／「a watchdog finding is not a court ruling」 |
| `compbars` | 3 | 排除（gone）vs 民事訴訟（remains）／Hudson の道 vs Young の道（同一経路でない・C24）／Part IV=4 vs Kennedy 別票（C25・射程非圧縮） |
| `votetally` | 1 | **5–4 Hudson のみ**（F15・majority:5/dissent:4・R-SPLIT）。**48-0/10-4/5-3 は votetally に入れない**（stat/numberticker/compbars で表現） |
| `numberticker` | 2 | 10–4 voted down（N10・C3・AE r01 と別区間）／~100 alleged（AE c01 と別区間） |
| `pindropmap` | 2 | Chicago West Side（誤住所 vs 足首モニタの実所在）／Detroit（Hudson・制度説明） |
| `mechanism` | 2 | knock → announce → wait（進入前の手順・C2/C4）／§1983 の道: file → hire a lawyer → hope a jury agrees |
| **合計** | **34** | variety = 11 figure-kinds |

`graphics[]`（kinetic typography）3枠: 幕タイトルの語同期切れ上がり等（`kinetic`）。→ variety に `kinetic` が加わり **12種** ≥3 ✓。

> **★実装表現（CODEX_B §6）:** CODEX_B は上記 34+3 を **すべて `figures[]` に 37本**入れ、`graphics[]=[]` にする（`check_motion_density` は `figures+graphics+heroCuts` を合算するので密度は同値・floor 31 に +6）。「figures 34/graphics 3」は DESIGN 上の役割分類であり、film.json 上は全 37 が figures[]・graphics[] は空配列。どちらで数えても 37 beats。

## 7.3 配置ルール

1. **AE の 8区間（§6.3）と1秒でも重ならない**（`validate_young_beats.py`＝validate_thompson_beats.py を複製・両方突き合わせ）。
2. 幕あたり配分: ACT1=5 / ACT2=6 / ACT3=13 / ACT4=6 / ENDING=4（ACT3 が最長 221.3s なので厚め）。
3. **同じ kind を連続させない。**
4. 1枠 4.0–8.0秒。
5. ACT3 の説明区間に `compbars`＋`quote`＋`timeline`＋`mechanism` を分散し 20秒超の平坦区間をゼロに。
6. `quote` は**逐語のみ**（要約を引用符に入れない・C4/中立帰属）。争点は多数/反対/Kennedy に帰属語を伴う。
7. `figures[].text`/`lines[]` は `facts_lock` 検査対象（`no-knock`/`unconstitutional`/`she changed the law` を出さない）。

## 7.4 密度の最終検算

```
Remotion figures 34 + graphics 3 = 37 kinetic beats（film.json 内）
  density  = 37 / 12.015 = 3.08/min   ✓ ≥2.5（SPEC beats_floor 31 → 37 で +6）
  coverage = 222s / 720.9 = 0.308      ✓ ≥0.25
  variety  = 12 forms                  ✓ ≥3
AE hero 8枠は composite 後・gate 非カウント（上乗せの決め所）
```

---

# 8. レイヤー構成 と ゾーン分離（★主役の裏に最低4層）

## 8.1 本編カットのレイヤー構成（下→上・主役 L4 の裏に L1/L2/L3/L3b = 4層）

| L | 名前 | EP42 の値 |
|---|---|---|
| **L0** | ルート背景 | `#0A0A0C`（INK） |
| **L1** | グラデ背景 | `radial-gradient(120% 120% at 50% 40%, #131A24 0%, #0C1119 45%, #0A0A0C 100%)`（夜の青灰） |
| **L2** | グリッド/ライン | 縦横 64px の反復線＋放射マスク＋ドリフト。`repeating-linear-gradient(0deg/90deg, #3B7DD818 0px 1px, transparent 1px 64px)`、`translateY 0→48px` / `Easing.inOut(Easing.sin)`（等速禁止） |
| **L3** | グロー | 単一 DAWN 実用光。`radial-gradient(closest-side, #C98A3A66 0%, #C98A3A18 45%, transparent 75%)`、`filter: blur(28px)`。位置は幕で移動（戸口/テレビ/夜明け） |
| **L3b** | 大理石の光帯/ビネット | ACT3 は第4修正の光帯（`linear-gradient(100deg, transparent, #3B7DD822, transparent)` を横に slow drift）、他幕は羽根ビネット。`translateX` を `Easing.inOut(Easing.sin)` で微動（静止フレームゼロ） |
| **L4** | 主役（still / i2v / factory） | §10 のモーション（Ken Burns/parallax/i2v） |
| **L5** | テロップゾーン（上/中央・figures） | §8.2 |
| **L6** | 字幕ゾーン（下部帯） | §8.2 |

> **主役（L4）の裏に L1/L2/L3/L3b = 4層**（グラデ背景・グリッド/ライン・グロー・光帯/ビネット）で CLAUDE.md「最低3レイヤー」＋タスク「最低4層」を満たす。

## 8.2 ゾーン分離（一度も重ねない）

| ゾーン | 縦位置（1080基準） | スタイル |
|---|---|---|
| テロップ見出し | `y=96–260` | Oswald 64px / `#F5F7FA` / letterSpacing 4 |
| 中央テロップ / figures | `y=420–660` | §7 |
| 出典テロップ（アクセントライン） | `y=742–786` | Oswald 28px / warrant-blue `#3B7DD8` 3px 下線 |
| 字幕帯 | `y=872–1010` | 白 `#FFFFFF` + `textShadow:0 0 6px #000,0 2px 4px #000` / 半透明黒帯 `rgba(6,8,12,0.62)` / ≤2行・1行≤42字 / 54px / lineHeight 1.28 |
| AI開示 | `y=1024–1052`（右下） | Oswald 20px / `#C8CDD6` / opacity 70% |

**Caption QC:** ナレ一致 ≥99%（faster-whisper 強制アライン）/ `.srt` カバー ≥95% / キュー 1.0–6.0秒 / CPS ≤17 / 単語割り禁止 / 1語孤立キュー禁止 / ズレ ≤120ms。**【SILENCE】4区間には字幕キューを置かない。**

---

# 9. 絵コンテ（★48シーン・象徴のみ・6制約・CODEX_A が 85本プロンプトへ展開する原図）

## 9.1 パーサ契約（★CODEX_A が `ai_prompts.v001.md` を書くときの形式・`read_prompts()` が読む2行形式）

`read_prompts()` の正規表現は `^\s*-\s+`([^`]+\.png)`\s*$`。つまり:
```
- `S01.png`
<positive prompt> ... [STYLE] Avoid: <negative>
```
- **1行目:** `` - `S01.png` ``（バッククォート囲み・行末は `.png` 直後）。プロンプトを同じ行に書かない。
- **2行目:** 正プロンプト → `[STYLE]`（§5.5）→ `Avoid:` → 負プロンプト（§5.6）。
- 配置先: **`episodes/PD-2026-042-young/04_scenes/ai_prompts.v001.md`**。生成: `.venv/Scripts/python.exe scripts/generate_sdxl_4k.py PD-2026-042-young`（**variants 指定なし＝1枚**）。
- 出力: `H:\pd-media\assets\ai\young\S01.png …` ＋ `remotion/public/young/`。長辺 ≥3840 で冪等スキップ。
- **★body 85本＝85行**（still 各1枚）＋ **i2v 種 16行**（CODEX_A §8.1a）＝ `ai_prompts.v001.md` は計 **101 エントリ**。CODEX_A は書いた直後 `--only S01` で `shots=` が **101**（body 85 + i2v種 16）に達しているか（2行形式が壊れていないか）を確認。

## 9.2 絵コンテ級ショット記述（Sid ごと・カメラ/モーション/象徴/制約。CODEX_A はこれを固有プロンプトに翻訳）

> **全ショット共通:** 顔・身体・肖像なし（R1/C5/C6）。読める文字を作らない（redacted/illegible）。冷たい warrant-blue 基調＋単一 DAWN 暖色。`no-knock`/`unconstitutional`/`she changed the law` を画に含意させない。1シーン1枚＝各 Sid の主 still は1本。ambient は factory で埋める。

| Sid | カメラ/レンズ | 象徴（動き） | 制約メモ |
|---|---|---|---|
| S01 | 正対・寄り | 暗闇で戸枠が内側へ割れる木片・切れるチェーン錠（i2v: 割れる瞬間） | C2: 告知の含意「a shout」を残し no-knock を含意させない |
| S02 | 俯瞰寄り | 素の床の開いた手錠1つ・上の壁時計が深夜 | C6: 身体なし・象徴のみ |
| S03 | 正対・slow push-in | 素の玄関ドア intact・背後にグリッド線 | 中立・後で S41 と対 |
| S04 | 広め・室内 | 半開の戸棚・椅子の上着・散らばる書類（生活が崩れる寸前） | C6: 人物なし |
| S05 | 画面接写 | 市街地図に足首モニタの光点が**別住所**で脈打つ（i2v: 脈動） | 事実: 対象者は別所在・電子監視。本人描かない |
| S06 | 接写・机上 | search warrant（判事署名の含意・判読不能） | C2: search warrant のみ・no-knock 不使用 |
| S07 | 引き・外 | 夜の住宅街の戸口（establishing・factory ambient） | — |
| S08 | 手持ち感・断片 | ドアが破れフラッシュライトが走る（i2v: 速い掃引） | C6: 顔なし・光と影のみ |
| S09 | 俯瞰・寄り | 落ちた上着＋床の手錠＋散らばる書類（拘束の非グラフィック示唆） | C6: 身体・露出なし |
| S10 | 胸元接写 | ボディカメラの録画ランプが点る（機器のみ）＝全時間録画 | 【SILENCE 1.5s】の画 |
| S11 | 接写・机上 | 赤紐で封じたマニラ封筒（秘匿された映像） | 判読不能 |
| S12 | 引き・回廊 | 無人の法廷回廊・冷たい大理石（factory ambient） | — |
| S13 | 接写 | 黒塗りの申立書（弁護士制裁）＝判読不能 | facts_lock illegible |
| S14 | 室内・引き | 暗い居間で光るテレビ（i2v: グローの明滅）＝2020/12 放映 | 画面に認識可能像なし |
| S15 | 引き・夜景 | 多数の暗い窓に1つだけ灯り＝全国が部屋の中に | 象徴 |
| S16 | 俯瞰・机上 | 案件フォルダの山＋壁時計 ~16か月・`~100 ALLEGED`（タリー印） | C1趣旨: alleged・認定でない |
| S17 | 正対 | 冷光の空の演壇とマイク＝謝罪「on paper」 | 【SILENCE 0.9s】直後 |
| S18 | 壁ショット | 大理石の壁を走る光の帯＝第4修正の一文（i2v: 光が走る・碑文的・判読不能） | 象徴・逐語は figures で |
| S19 | 正対・対称 | 無人の最高裁法廷・9つの空席・冷光 | — |
| S20 | 接写 | 使われず置かれたガベル＝抑制 | — |
| S21 | 正対 | Detroit の古い木の敷居/戸口（generic） | C5: Hudson 本人を描かない・敷居のみ |
| S22 | 敷居寄り | 差す光が 3–5秒ゆっくり動く＝進入前の待機（i2v: 光の移動） | C5: 制度説明・人物なし |
| S23 | 抽象・接写 | 大理石面が硬い影で大小2つに割れる＝5–4 | 顔・文字なし |
| S24 | 接写・机上 | 意見書の一段落が光に浮くが判読不能＝narrow な判示 | — |
| S25 | 壁ショット | 壁に彫られた命令が**なお立つ**＝knock-and-announce は今も "a command" | C4: 射程非圧縮・unconstitutional 不使用 |
| S26 | 机＋戸 | 証拠トレイが机に残る＋開いたままの戸＝救済のみ除去・規則健在 | C4 |
| S27 | 抽象 | 天秤＝benefits vs "heavy social costs" | 文字なし |
| S28 | 席ショット | 4席が灯り・1席だけ離れて灯る＝Part IV=4 と Kennedy 別票 | C25: 中立・plurality を ruling と誤読させない |
| S29 | ベンチ | 無人のベンチに積まれたページ＝反対意見 | 中立帰属（dissent） |
| S30 | 広間・戸 | 暗い大理石に1つ開いた戸＝`SECTION 1983`＝残る救済 | N14 |
| S31 | シルエット | 遠い戸へ向かう匿名の後ろ姿＝負担/弁護士/望み | 顔なし |
| S32 | 引き・列柱 | 夕暮れの列柱・大理石の石段（factory ambient） | — |
| S33 | 並置 | 2つの別々の戸口＝Hudson と Young＝同じ戸でない | C24: 直接因果を作らない |
| S34 | 机上 | 和解小切手（金額判読不能）＋過失欄が**空白**のページ | C1: no finding of fault |
| S35 | 掲示板 | 投票掲示板が `48–0` に確定（i2v: 板が確定・**reported** 枠） | C1: 責任認定でない |
| S36 | 引き・議場 | 無人の議場と演壇＝静けさを買った | — |
| S37 | 名札列 | 1枚の名札が外れ（5–3・2023夏）多数は残る | 顔なし・中立 |
| S38 | 机上 | 押印され脇に置かれた条例＝計画書/30秒/子の保護アイコン（判読不能） | C3 |
| S39 | 掲示板 | 掲示板が `10–4` 確定＋`REJECTED` 押印（i2v: 押印の一撃） | C3: 法は変わっていない・still legal |
| S40 | 影 | 脇に置かれた条例が影に沈む＝慣行は今も合法 | C3 |
| S41 | 正対 | S03 と同じドア＝今は閉じて静か・夜明け前 | 回帰 |
| S42 | 机上 | 和解小切手を再掲＝金は受け取れるかも（判読不能） | C1 |
| S43 | 接写 | 過失欄が空白のページ＝金は何も認めなかった | 【SILENCE 1.0s】域・C1 |
| S44 | 壁ショット | S18 の光の帯を回帰＝なお "a command"・背後に何もない | C4 |
| S45 | 接写 | 壁時計を再掲（HOOK 回帰）＝過ぎた時間 | — |
| S46 | 引き・pull-back | 閉じたドアの下から暖かい夜明けが育つ（i2v: 光が育つ・単一 DAWN） | C6: 人物なし |
| S47 | 象徴 | 空の椅子/回されたマイク＝言われない一文の席 | 象徴 |
| S48 | 引き・夜明け | 住宅街に1つ灯る窓＝未解決の余韻・CTA 域（factory ambient） | — |

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
**0.5s 刻み方針:** 226カットの境界は **`QUANT`=15フレーム（0.5秒）にスナップ**して配置する。各カット長は `CUT_MIN`〜`CUT_MAX`、平均 `CUT_MEAN`。ACT3 は最も遅く（長カット寄り・6.0s 近辺を多用）、ACT1 は速く（1.0–2.5s の断片）。CODEX_B は shotlist の各 span 端を 15f グリッドに丸める。

## 10.2 全カット共通モーション（★静止フレームを1枚も作らない）

| 素材 | 基本モーション | イージング | 数値 |
|---|---|---|---|
| **still** | Ken Burns：`scale 1.00→1.08` を**カット全長**で。加えて `translate` を象徴方向へ ±24px | `Easing.out(Easing.cubic)` | scale 差 +0.08 / drift 24px。**opacity は translate/scale と必ず対**（単独禁止） |
| **i2v** | ネイティブ動き（Wan 2.2 A14B → RIFE 48fps）＋微 `scale 1.00→1.03` | ネイティブ＋`Easing.out(Easing.cubic)` | 追い足しの scale は 0.03 のみ |
| **factory** | 実写の内在動き＋微 Ken Burns `scale 1.00→1.04` | `Easing.out(Easing.cubic)` | 24pxまでの parallax 可 |

**カットイン/アウト:** クロスディゾルブ 6–10f または hard cut。ACT1 の踏み込み断片は hard cut 連射。ACT3 は長めのディゾルブ（荘厳）。**フェードは opacity 単独にせず、入りは `translateY 12px→0`＋opacity、抜けは `scale 1.00→1.02`＋opacity を対にする。**

## 10.3 速い動きの motion-blur（★@remotion/motion-blur の Trail）

```tsx
import {Trail} from '@remotion/motion-blur';
// 速いカット（S01 割れる戸口 / S08 フラッシュライト掃引 / S35・S39 掲示板確定・押印 / 幕頭 kinetic）
<Trail layers={6} lagInFrames={1.2} trailOpacity={0.45}>
  {/* 主役 or 動く数値/文字 */}
</Trail>
```
対象: **S01 / S08**（踏み込み）、**S35 / S39**（掲示板・押印）、**S46**（夜明けの pull-back は緩なので Trail 不要）、および §7 の `numberticker`・幕頭 `kinetic`。ゆっくりした Ken Burns には Trail をかけない（無駄な残像を避ける）。

## 10.4 テキストのマスク切れ上がり（★基本形・全 figures / 字幕見出し / 幕タイトル）

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

# 11. オープニング（OP）設計 — 完全仕様（`OpeningYoung`・fps=60・CLAUDE.md §1–5 全項目）

## 11.1 秒数ベースのタイムライン（fps=60・「フレーム」は全て `Math.round(60 × 秒)`・直書き禁止・0.5s 刻み方針で全区間記述）

```ts
const FPS_OP = 60; const F = (s:number)=>Math.round(FPS_OP*s);   // 総 180f = F(3.0)
```

| 秒 | フレーム | 起きること（EP42 signature = 割れる戸口の亀裂） |
|---|---|---|
| 0.00–0.10 | f0–6 | 画面 `#0A0A0C`。**L1** グラデ opacity 0→1（0.40s）＋ **scale 1.08→1.00** を 180f で（`Easing.out(Easing.cubic)`）。opacity 単独でなく scale 併用 |
| 0.10–0.15 | f6–9 | **L6 ロゴ**（`hasLogo`）左上 `top:64/left:72` に spring 出現。scale 0.4→1.0・opacity 0→1（併用・`damping:14,mass:0.9`） |
| 0.15–0.25 | f9–15 | **L2** グリッドが spring（`{damping:200,mass:1,durationInFrames:F(0.8)=48}`）で reveal。最終 opacity=`gridReveal*0.18`。全体を 180f で `translateY 0→48px`（`Easing.inOut(Easing.sin)`） |
| 0.25–0.30 | f15–18 | **L3** DAWN グローが spring（`{damping:18,mass:1.2}`）。scale 0.6→1.15 / opacity 0→0.85（併用）。`filter:blur(28px)` |
| 0.30–0.86 | f18–52 | **L4 主役タイトル**が1文字ずつ切れ上がる（`overflow:hidden` マスク）。各文字 spring（`{damping:16,mass:1}`）で `translateY 110%→0`、opacity=`interpolate(sp,[0,0.25],[0,1])`。**スタッガー=`F(0.04)=2フレーム/文字**。全体を `Trail`（`layers=6,lagInFrames=1.2,trailOpacity=0.45`）で包む |
| 0.55–1.15 | f33–69 | **L2b 戸口の亀裂ライン**（EP42固有＝割れる戸枠）。中央からタイトル背後を横切る亀裂が `scaleX 0→1`＋`opacity 0→0.55`（spring `{damping:22,mass:1.1}`, `transformOrigin:'center'`）。warrant-blue。opacity 単独禁止で scaleX 併用 |
| 0.95–1.35 | f57–81 | **L5a** warrant-blue の下線が左から `scaleX 0→1`（spring `{damping:16,mass:0.8}`, `transformOrigin:'left center'`）。240×6px・`boxShadow:0 0 24px #3B7DD8aa` |
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
| L2b 亀裂 | scaleX 0→1 / opacity 0→0.55 | spring | `{damping:22,mass:1.1}`・origin center |
| L5a 下線 | scaleX 0→1 | spring | `{damping:16,mass:0.8}`・origin left |
| L5b サブ | translateY 24px→0 / opacity | spring | `{damping:20,mass:1}` |
| L6 ロゴ | scale 0.4→1.0 / opacity | spring | `{damping:14,mass:0.9}` |

> **全 opacity が translateY/scale/scaleX と対。等速線形を1箇所も使わない。**

## 11.3 レイヤー構成（下→上・主役 L4 の裏に L1/L2/L2b/L3 = 4層）

L0 `#0A0A0C` / L1 グラデ（`radial-gradient(120% 120% at 50% 35%, #131A24 0%, #0C1119 45%, #0A0A0C 100%)`）/ L2 グリッド（`${accent}22` 64px・放射マスク）/ L2b 戸口の亀裂（`linear-gradient(90deg, transparent, ${accent}cc, ${accent}55, ${accent}cc, transparent)`）/ L3 DAWN グロー（`radial-gradient(closest-side, #C98A3A88, #C98A3A22, transparent)` `blur(28px)`）/ L4 主役タイトル（Trail 包み・`overflow:hidden` span マスク・Anton `fontWeight:800 fontSize:150 letterSpacing:-2 color:#F5F7FA`）/ L5 下線＋サブ（Oswald `fontSize:38 letterSpacing:6 uppercase color:#C8CDD6`）/ L6 ロゴ（`linear-gradient(135deg, ${accent}, #ffffff22)`・`border:2px solid ${accent}`）。

## 11.4 確認方法（CLAUDE.md §5）

```bash
cd C:\Users\aab15\Documents\prime-documentary\remotion
npm run studio     # = remotion studio。OpeningYoung を 0→180f でスクラブし §11.1 の各時刻を目視
npx remotion render OpeningYoung out/young_opening.mp4 --props=./props/young.json
# props 差し替え量産
npx remotion render OpeningYoung out/young_short_op.mp4 --props=./props/young_short.json
# 本編
npx remotion render Ep42Young out/young_final.mp4 --props=./src/data/young_film.json --public-dir=public_slim --concurrency=4
```

---

# 12. props 定義と型（CLAUDE.md §4）

```ts
export type OpeningYoungProps = {
  title: string;      // 主役タイトル。1文字ずつスタッガーで切れ上がる
  subtitle: string;   // サブタイトル。UPPERCASE 表示（facts_lock 検査対象）
  accent: string;     // アクセント（HEX6桁・"#"込み）。グリッド/亀裂/グロー/下線/ロゴに波及
  hasLogo: boolean;   // true で左上にロゴバッジ
};
```
**EP42 の確定 props（`remotion/props/young.json`）:**
```json
{ "title": "THE WRONG HOUSE", "subtitle": "HUDSON V. MICHIGAN", "accent": "#3B7DD8", "hasLogo": true }
```
**量産用 `remotion/props/young_short.json`:**
```json
{ "title": "WRONG DOOR", "subtitle": "WHAT THE LAW OWES YOU", "accent": "#3B7DD8", "hasLogo": false }
```
> `subtitle` は `facts_lock` 検査対象（`no-knock`/`unconstitutional` を出さない。`HUDSON V. MICHIGAN` は制度説明として可）。

---

# 13. 受入基準（EP42 の Definition of Done・★語数ゲートが最初・全編アイボール必須）

```bash
cd C:\Users\aab15\Documents\prime-documentary
# 0. 語数（最優先・課金前）
./.venv/Scripts/python.exe scripts/check_script_length.py episodes/PD-2026-042-young/03_script/script.en.v001.md --json
# 1. 事実性（EP42固有・§1.3）
./.venv/Scripts/python.exe scripts/check_young_facts.py --json
# 2. ビート契約（AE↔figures 非重複）
./.venv/Scripts/python.exe scripts/validate_young_beats.py
# 3. 密度（★31 を Remotion 側で満たしていること・--ep 指定／--json は出力パス）
./.venv/Scripts/python.exe scripts/check_motion_density.py --ep PD-2026-042-young --json runs/qc/young_motion.json
# 4. VO速度（ナレ直後・ミックス前）
./.venv/Scripts/python.exe scripts/measure_vo_wpm.py --ep young --json
# 5. 最終受入
./.venv/Scripts/python.exe scripts/check_final_acceptance.py 42 --render episodes/PD-2026-042-young/08_edit/young_final_bgm.v002_ae.mp4 --emit-receipt
```
> **ゲート入力は `--ep PD-2026-042-young`。`--json <film.json>` を入力に使わない**（出力パス＝上書き事故。ブリーフ§5）。

| ゲート | 閾値 | EP42 設計値 |
|---|---|---|
| `check_script_length` | band 内 | 2,140語（SPEC・要 PASS 確認） |
| `runtime_band` | 690–750s | **733.4s = 12:13** |
| `motion_density` | ≥2.5/min ∧ cov ≥0.25 ∧ variety ≥3 | **3.08/min / 0.308 / 12種**（film.json 37 beats・AE非依存・floor 31 に +6） |
| `animation_mix`（紙芝居） | still-share ≤45% ∧ motion cov ≥45% | **44.69% / 55.31%** |
| `check_asset_reuse` | first-use ≥0.70・still≤2・factory1・motion≤2 | **0.8584 / 2 / 1 / 2** |
| `footage_diversity` | distinct/total ≥0.40 | **0.8584** |
| `visual_asset_qc` | 全 factory 目視 reviewed | **93本 目視（CODEX_A）** |
| `image_resolution` | 長辺≥3840 | 全 SDXL ≥3840 |
| `bgm_present` | 無音>25秒ゼロ | 最長 1.8秒 |
| `caption_integrity` | 一致≥99%・カバー≥95% | §8.2 |
| `op_ed_bookends` | `BrandOpening`/`BrandEndcard` import・不変 | ✓ |
| `facts_lock`（EP42固有・6制約） | violations=0 | §1.2/§1.3 |
| **全編アイボール** | 12:13 を通しで目視 | ★1フレーム判定禁止（EP39-41 の miss） |

---

# 14. premortem（失敗するとしたらここ）

| # | 失敗モード | 事前対処 |
|---|---|---|
| 1 | **番号ズレ**（別番号を発明） | シーンは S01..S48 固定（§3.2）。プロンプトも S01..S48 の Sid のみ |
| 2 | **紙芝居**（still-share 45%超・余裕 0.31%pt） | §5.1 で still-cut 101 固定・factory 93・i2v 32。still1つ増で 45% 割れ → cut を増やさず同一シーンの新規 distinct で回復 |
| 3 | **バリエーション水増し**（`--variants 3` を書く） | §5.3。variants 指定なし＝1枚。ai_prompts は 85行＝85枚 |
| 4 | **密度 FAIL**（AEカードに頼る） | §7。film.json に 37 beats（31 超）。AE 8枠は composite 後で非カウント |
| 5 | **画像プロンプトが読めない**（0枚生成） | §9.1 の2行形式・`--only S01` で `shots=101`（body 85 + i2v種 16）確認 |
| 6 | **牛が本編に入る**（ファイル名信仰） | §5.4 factory 93本を `build_footage_contact_sheet.py` で全点目視（CODEX_A BLOCKING） |
| 7 | **6制約違反**（no-knock/unconstitutional/she changed the law/和解=責任認定） | §1.2/§1.3 `check_young_facts.py`。カード・figures・字幕・プロンプト全対象 |
| 8 | **FigureBeats kind 大文字で無音描画** | §7.2 kind は全小文字（`compbars`・`comparebars` は存在しない） |
| 9 | **AE em-dash 豆腐 / 等速 / OM名英語 / 文字切れ** | §6.6 全13件。テキスト幅は `sourceRectAtTime(t,false).width` 実測 |
| 10 | **id 誤り**（`42` の `4` を落とした形で登録） | §0.1。`id="Ep42Young"`・`caseFilmDurationInFrames(youngFilm,30)`=22002 |
| 11 | **EP39/40/41 と素材被り** | §2 で3つの stock_ledger の sha256 を除外 |
| 12 | **fast端で 11分台** | §4.1 speed 1.0 明示＋`measure_vo_wpm` 168–190・190超は破棄再発注 |

---

# 15. 設計パッケージ接続（DESIGN → CODEX_A / CODEX_B）

- **DESIGN（本書）:** タイムライン・レイヤー・モーション数値・48絵コンテ・FigureBeats 設計・AEカード表・OP 仕様。
- **CODEX_A（別ファイル `EP42_young_CODEX_A_ASSETS.v001.md`）:** §9 を **85本の固有プロンプト**（1シーン1枚・variants 0）＋ i2v 16 ＋ factory 93 選定＆**全点目視QC** ＋ 境界契約 `asset_manifest.v001.json`（counts を EP42 値 still85/factory93/motion16 に）。
- **CODEX_B（別ファイル `EP42_young_CODEX_B_BUILD.v001.md`）:** `build_young_film.py`（＝`build_thompson_film.py` を複製・ASSET_MAP/NARR/FACTORY_SEL を young パスに）／captions（実測 narration）／figures 34＋graphics 3（小文字 kind・§7）／`CaseFilm` を `id="Ep42Young"` で Root.tsx 登録（`caseFilmDurationInFrames`）／`OpeningYoung`／AEビルダ・コンポジタ・`validate_young_beats.py`・`check_young_facts.py`（EP41 版を複製）／レンダ（`--public-dir=public_slim --concurrency=4`）／ゲート。
- **A↔B 接続点は `asset_manifest.v001.json` ただ1ファイル**（EP41 同型・counts を EP42 値に）。
- **複製元（実在・EP41）→ young 複製先:** `build_thompson_film.py`→`build_young_film.py` / `build_thompson_bgm.py`→`build_young_bgm.py` / `ae/build_thompson_hero_jsx.py`→`ae/build_young_hero_jsx.py` / `ae/composite_thompson_hero.py`→`ae/composite_young_hero.py` / `validate_thompson_beats.py`→`validate_young_beats.py` / `check_thompson_facts.py`→`check_young_facts.py`。**共有（複製不要）:** `generate_sdxl_4k.py` / `build_footage_contact_sheet.py` / `check_motion_density.py` / `measure_vo_wpm.py` / `check_script_length.py` / `check_final_acceptance.py`。**実在しないスクリプトを捏造しない。**
