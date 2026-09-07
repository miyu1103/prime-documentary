# EP46 — THE BAG ON THE DESK — 制作設計書（DESIGN 本体・v001・確定台本版）

- Episode ID: `PD-2026-046-tlo` / slug: `tlo` / EP46
- 中心の問い（英語・二人称・★過大化しない）: **"Inside your own school, does the Fourth Amendment walk in with you — or wait out at the curb?"**
- 判例（制度説明としてのみ）: **New Jersey v. T.L.O., 469 U.S. 325 (1985)**（decided 1985-01-15・docket 83-712・opinion **Justice Byron White**・6-3）。先行系譜 **Tinker**（生徒は校門で憲法を捨てない）。
- 主役: **T.L.O.**（当時14歳の新入生・**未成年＝R2**）。**顔・肖像・身体・実名を一切描かない**（公開記録のイニシャル T.L.O. のみ・象徴/物/手元/影のみ）。副校長（Theodore Choplick）・White判事・反対の各判事も人物化しない。
- 主題: 公立学校職員の捜索にも第4修正は**適用される**。ただし基準を**令状不要・相当な理由(probable cause)不要＝合理的疑い(reasonable suspicion)へ引き下げた**（消滅ではなく引き下げ）。二段テスト（inception＋scope）が判例核。警察関与時はより高い基準があり得る（footnote 7 留保）。**"生徒に権利がない/学校は何でも捜索できる"は誤り**が背骨。
- Status: **BINDING**。**唯一の真実 = 機械生成済み `EP46_tlo_PRODUCTION_SPEC.v001.json`**。本書のあらゆる数値はそこからの転記で、手書きで発明していない。衝突したら SPEC が勝つ。
- このファイルは**設計パッケージ3分割**（DESIGN / CODEX_A / CODEX_B）の **DESIGN 本体**。共有ブリーフ `EP46_tlo_DESIGN_BRIEF.shared.md` を単一の真実源とする。84本の SDXL プロンプト実体・i2v 16・factory 92 選定は **CODEX_A**、`build_tlo_film.py`・captions・figures 実装・Root.tsx 登録・AEビルダ/コンポジタ・ゲートは **CODEX_B** に属す（本書は各所でポインタのみ示す）。

## ★このエピソードの唯一の真実（手書きで数値を発明するな）

`episodes/_planning/EP46_tlo_PRODUCTION_SPEC.v001.json`（台本から機械生成・`scripts/build_production_spec.py`）。本設計書は SPEC を**人間可読な実装指示に翻訳しただけ**で、新しい数字を作っていない。

```
words_total          = 2,125
narration_seconds    = 715.9   （= 11.9分・[DESIGNED SILENCE 1..2] の実音無音を含む）@ wpm_used 178.1
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
mean_shot_seconds    = 3.2    /  max_shot_seconds = 6.0
acts(秒)             = HOOK 48.5 / OPENING 43.5 / ACT1 121.3 / ACT2 109.2 / ACT3 253.7 / ENDING 115.6
```

## ★★ 最重要の前提: 1シーン1枚・バリエーション0 ★★（ブリーフ§1）

- Codex の画像生成は高精度。**同一ショットの複数バリエーション（`_01/_02/_03`）を作らない。**
- `04_scenes/ai_prompts.v001.md` は **still 84本＝84行の固有プロンプト**（`generate_sdxl_4k.py` の `read_prompts()` 2行形式・各1枚）。**`--variants 3` は使わない**（`--variants 1` または variants 指定なし）。
- i2v モーション種は **16枚**（各1シード・これもバリエーション0）。
- 総生成画像 = **still 84 + motion seed 16 = 100枚（各1回）**。**factory 92 は生成ではなく在庫選抜**（全点目視QC・EP39〜45 と sha256 被りゼロ）。
- **still を増やして factory を削るな**（still-share 0.4464 は cap 0.45 に対し余裕 0.36%pt しかない）。

## ★EP39〜45 で踏んだ失敗＝本書が最初から潰す設計判断

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
| 9 | **dochighlight のバグ見え**（3回指摘・EP40/41/42） | **`dochighlight` を figures に1件も入れない（grep 0・R-DOCHL）。** 書類/証拠は `lowerthird` で表す | §6.2/§7.3 |
| 10 | **未成年の肖像化・薬物の扇情化** | T.L.O.（14歳）は象徴のみ・顔なし。原事案の薬物は臨床的最小限（押収物を並べた机・封）。**美化/煽情ゼロ**（R-MINOR） | §1.2/§9 |

---

# 0. 環境・Remotion設定（CLAUDE.md §0 準拠）

## 0.1 本編 `Ep46Tlo` の Composition 設定（★本編の正・誤記注意）

| 項目 | 値 |
|---|---|
| `id` | **`Ep46Tlo`**（Root.tsx に `CaseFilm` で登録。ブリーフ§5「composition id Ep46Tlo」。**id の切り詰め・綴り違い・大文字化は誤記＝BLOCKER**） |
| 解像度 | **1920 × 1080** |
| `fps` | **30**（EP44/45 と同値を踏襲。フレームは全て `Math.round(30 × 秒)`・直書き禁止） |
| `hookSeconds` | **8.0**（★EP45 は 0 だったが EP46 は 8.0＝冒頭のコールドティザー preroll を明示。`tlo_film.json` に `hookSeconds:8.0` を必ず持たせる） |
| `durationInFrames` | **`caseFilmDurationInFrames(tloFilm, 30)` = 22092**（4項の実関数 `round(hookSeconds×30)+round(OPENING_SEC×30)+ceil(narrationSeconds×30)+round(ENDCARD_SEC×30)`・§3.1[3] で算出。手書きで数値を入れず関数で算出する） |
| component | `remotion/src/compositions/CaseFilm.tsx`（既存の汎用 `CaseFilm` を再利用。`Bookends.tsx` の `BrandOpening`/`BrandEndcard` を **import**・fork 禁止） |
| data | `remotion/src/data/tlo_film.json`（`scripts/build_tlo_film.py` で再生成できる状態を保つ＝**git 未追跡**） |

**Root.tsx 登録（★ブリーフ§5・CODEX_B が実装）:**
```tsx
import {tloFilm} from './data/tlo_film.json';
import {caseFilmDurationInFrames} from './lib/caseFilmDuration';
// ...
<Composition
  id="Ep46Tlo"
  component={CaseFilm}
  width={1920} height={1080} fps={30}
  durationInFrames={caseFilmDurationInFrames(tloFilm, 30)}  // = 22092（hookSeconds=8.0）
  defaultProps={{film: tloFilm}}
/>
```
> **id は `Ep46Tlo`**（切り詰め・綴り違い・先頭大文字化などは全て誤記。ブリーフ§5 の render 行 `Ep46Tlo` が正）。**`tloFilm.hookSeconds` は 8.0**（0 にすると duration が 240f 短くなり尺が崩れる）。

## 0.2 タイトルバンパー `OpeningTlo` の Composition 設定（CLAUDE.md 正典部品準拠）

| 項目 | 値 |
|---|---|
| `id` | **`OpeningTlo`** |
| 解像度 | **1920 × 1080** |
| `fps` | **60**（CLAUDE.md §0 の正典値。OP 単体は 60fps） |
| `durationInFrames` | **180**（= 3.0秒 @ 60fps） |
| component | `remotion/src/compositions/OpeningTlo.tsx`（§11 全仕様） |

> `OpeningTlo` は**独立したタイトルバンパー成果物**（`out/tlo_opening.mp4`）。本編内 OP/ED の正典は `Bookends.tsx`（`BrandOpening` 3.50s / `BrandEndcard` 9.00s・不変）。`OpeningTlo` を本編に ffmpeg で焼き込まない（オーナー承認なしに見え方を変えない）。

## 0.3 必要な依存パッケージ

```bash
cd C:\Users\aab15\Documents\prime-documentary\remotion
npm i @remotion/motion-blur     # CLAUDE.md 必須依存（Trail によるモーションブラー）
```

## 0.4 `remotion.config.ts`（CLAUDE.md §0 正典値・EP41〜45 と同一・書き換えない）

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

**EP46 のパレット（★schoolhouse-green ＝ 温い事務灯の下の机の上のハンドバッグ（木目）＋冷たい institutional の廊下/ロッカー＋淡い最高裁大理石＋黒板グリーンの空き教室・レーン分離）:**
```
INK    = #0A0A0C   ルート背景（サムネ bg と一致）
DESK   = #171310   温いタングステンの事務机（warm near-black・机の上のバッグ／押収物が並ぶ側）
SLATE  = #14201B   黒板グリーンの空き教室 near-black（学校の内側・schoolhouse）
LOCKER = #22262A   冷灰の institutional 廊下/ロッカー（無人）
MARBLE = #34363B   最高裁の冷たい大理石（ACT3・列柱）
ACCENT = #3F8F5F   ★schoolhouse-green（校門/黒板の一点差し色）。ブランド数値・ライン・下線・グロー・OP/AE/サムネ accent。★EP41 gold / EP42 blue / EP43 amber / EP44 teal / EP45 crimson を流用しない
WHITE  = #F5F7FA
SILVER = #C8CDD6   （AI開示テキスト）
```
> **レーン分離:** EP41 gold（鋼灰institutional）/ EP42 blue（夜のシカゴ）/ EP43 amber（porch-amber）/ EP44 teal（clinical hospital）/ EP45 crimson（督促の朱）と被らないよう、EP46 は **温い事務灯の机 near-black `#171310` ＋ 黒板グリーンの空き教室 `#14201B` ＋ 冷灰のロッカー廊下 `#22262A` ＋ 冷たい大理石 `#34363B` を基調＋唯一の一点差し＝schoolhouse-green `#3F8F5F`**。接尾に `porch-amber` `warrant-blue` `teal-green hospital` `sodium prison corridor` `overdue crimson` を含めない。**factory は EP39〜45 の `stock_ledger*.json` の sha256 を除外**（CODEX_A・BLOCKING）。**CODEX_B は OP props / AEカード / サムネ accent を必ず `#3F8F5F` にする（他話色の流用は BLOCKER）。**

---

# 1. 事実の取り扱い（★正確性6制約＝FACTS LOCK / `check_tlo_facts.py`・BLOCKING）

## 1.1 確定台本（唯一の正・1バイトも変えない）

```
C:\Users\aab15\Documents\prime-documentary\episodes\_planning\EP46_tlo_script.en.v001.md
```
**本番配置先:** `episodes/PD-2026-046-tlo/03_script/script.en.v001.md`（上記を1バイトも変えずコピー）。整形も禁止（AI臭再発と語数ゲート再計算を招く）。台本の幕構成（HOOK / OPENING / ACT_1 / ACT_2 / ACT_3 / ENDING）と `【DESIGNED SILENCE …】`（**2箇所**）を正典とする。存在しない演出マーカーを発明しない。台本の `〔CARD: … confidence: high〕` 注記は数値のヘッジ根拠であって画面カードの命令ではない。

## 1.2 ★正確性6制約（全出力＝プロンプト・カード文言・図表・字幕・タイトルに適用。1つでも違反＝BLOCKER）

| # | 制約 | 出力での順守 |
|---|---|---|
| **C1** | **生徒は無権利ではない（4Aは学校でも適用・基準は引き下げ）** | 最高裁は「公立学校職員による捜索にも第4修正は適用される」と明言（F09）。ただし基準を**令状不要・相当な理由不要＝reasonable suspicion へ引き下げた**（F10・消滅でなく引き下げ）。**「students have no rights」「the 4th doesn't apply in school」「the school can search anything / anytime / for no reason」「students leave their rights at the door」を断定として出さない**（反論される立場としての引用は可）。**「学校の捜索には warrant / probable cause が必要」も誤り**（引き下げられた）。許容: "the Fourth Amendment applies in school" / "the standard is lowered, not eliminated" / "reasonable suspicion" |
| **C2** | **二段テストを正確に（逐語）** | 判例核＝二段テスト: ①**justified at inception**（生徒が法or校則に違反した証拠が出ると疑う reasonable grounds）②**reasonable in scope**（年齢・性別・違反の性質に照らし過度に侵襲的でない）。White 逐語で提示（F11）。**「probable cause required」に誤らせない。「何でも捜索できる」に過大化しない**（scope 制約を落とさない） |
| **C3** | **公立学校職員 vs 警察（footnote 7 の留保）** | 本判決の基準は**公立学校職員**のもの。**警察が関与/主導する場合はより高い基準があり得る**（footnote 7 で留保・F15）。この区別を必ず明記。**「police can search students on reasonable suspicion」と一般化しない** |
| **C4** | **票決 6-3・中立帰属** | 6-3（F13）。**White 法廷意見**（F14）。**Brennan・Marshall・Stevens** が一部反対（合理性への引き下げ／本件適用に反対）。多数/反対を**中立**に帰属。**別の票数・"unanimous"・別の執筆者を出さない** |
| **C5** | **T.L.O.＝未成年・R2・薬物は臨床的最小限** | 当時14歳。**顔・肖像・身体・実名なし**（公開イニシャル T.L.O. のみ・象徴/物/手元/影）。原事案に薬物（所持・売買の証拠）が含まれるが**4A＝生徒の権利の物語**として枠付け。**薬物を扇情化/美化しない**＝押収物を机に並べた臨床的・封のかかった最小限描写。原被疑事実でサムネ/タイトルを煽らない |
| **C6** | **数値・引用は原典一致・medium はヘッジ** | 469 U.S. 325 (1985)・1985-01-15・二段テスト逐語・"reasonable grounds"・White 執筆は原典一致。**confidence:medium（校名 Piscataway・副校長名 Choplick）は画面に出さない**（役職 "an assistant vice principal" と "a public high school in New Jersey" に留める） |
| **R1** | **実在人物の顔・肖像を生成しない** | 全生成ビジュアル表示中は `AI-assisted visualization`（右下）常時表示。概要欄に1行 AI 開示 |

## 1.3 6制約ゲート `check_tlo_facts.py`（`scripts/check_tlo_facts.py`＝EP45 `check_cleveland_facts.py` を tlo 用に複製。exit≠0 で出荷停止・CODEX_B 実装。出力 `facts_lock.v001.json`）

> **★ゲート名は1本に確定:** 6制約の機械ゲートは **`scripts/check_tlo_facts.py`**（出力 `09_package/facts_lock.v001.json`）ただ1つ。**DESIGN / CODEX_A / CODEX_B で同名参照**（別名を作らない）。下表の **L-C1..L-C6・L-R1** は内部ルール **R-*** に一本化して実装（対応: L-C1→R-OVERCLAIM / L-C2→R-STANDARD / L-C3→R-POLICE / L-C4→R-VOTE / L-C5→R-MINOR / L-C6→R-HEDGE、加えて **R-QUOTE・R-DOCHL**）。

**検査対象:** `03_script/script.en.v001.md` / `remotion/src/data/tlo_film.json` の `figures[].kind`・`figures[].*text*`・`quote`・`attribution`・`lines[]`・`label` / `08_edit/ae_hero/beats.json` の `hero`/`top`/`bottom`/`sub`/`attribution`/`caption` / `09_package/description.txt` / `remotion/props/tlo*.json` の `subtitle`/`title` / `04_scenes/ai_prompts.v001.md`。

| ルール | 内容 |
|---|---|
| **R-OVERCLAIM（C1）** | `students? (have\|has) no (rights\|privacy)` / `(the )?(4th\|fourth amendment) (does ?n'?t\|does not) apply (in\|at) school` / `students? leave (their )?rights at the (school ?house )?door`（断定形）/ `(school\|they) can search (anything\|any bag\|anytime\|whenever\|for no reason)` が出たら FAIL。**`warrant`/`probable cause` を「学校の捜索に必要」とする払下げは FAIL**（引き下げられた）。`4A applies` を含む payload に `no rights`/`no privacy` が同一 payload にあれば FAIL |
| **R-STANDARD（C1/C2）** | 学校捜索の基準を `probable cause` または `warrant` と記す payload は FAIL（holding は **no warrant · no probable cause → reasonable suspicion**）。`reasonable suspicion` を「4A が消滅した」と結びつけたら FAIL。二段テスト文言は §2 `APPROVED_QUOTES` の逐語一致（inception/scope を落としたら FAIL） |
| **R-POLICE（C3）** | `police (can\|may) search students? on reasonable suspicion` / footnote 7 を無視して「reasonable suspicion が警察にも及ぶ」と一般化したら FAIL。警察関与の payload には `higher standard`/`reserved`/`footnote 7`/`not decided` のいずれかが必要 |
| **R-VOTE（C4）** | 票数は `6 ?- ?3` のみ許容。他の split・`unanimous` は FAIL。多数の執筆者は `White` のみ。反対一部は `Brennan`/`Marshall`/`Stevens`。中立でない帰属（例「White が生徒の権利を奪った」）は FAIL |
| **R-QUOTE（C6・★EP43 R-PAYTON 事故）** | `quote` は逐語のみ。`quote[].attribution` が空、または §2 `APPROVED_QUOTES` の帰属（**`Justice White, for the Court`**）と不一致なら FAIL。要約を引用符に入れたら FAIL。White 逐語文字列は ledger と大小無視で一致必須 |
| **R-MINOR（C5）** | `ai_prompts` 正プロンプトに `portrait`/`face of`/`likeness`/`the girl`/`a 14 ?year ?old girl`/`T\.?L\.?O\.?`（人物として）/`child's face`/`nude`/`her body` が出たら FAIL（ネガティブ使用は可）。`glamor(ous)? drugs`/`drug party`/`smoking a joint`/`getting high`/`close-up of marijuana being used` 等の扇情語が出たら FAIL。薬物は `sealed evidence`/`laid out clinically`/`muted` のみ |
| **R-HEDGE（C6）** | 画面文字列に `Piscataway` / `Choplick` が出たら FAIL（medium・非 load-bearing）。数値は §1.4 の表以外を画面に出したら FAIL |
| **R-DOCHL（★EP46 固有）** | `figures[].kind == "dochighlight"` が **1件でも**存在したら FAIL（`grep -c '"dochighlight"'` が 0 でないと出荷停止）。`comparebars` も非実在→出たら FAIL（`compbars` が正） |
| **L-R1 開示（R-DISCLOSE）** | `description.txt` に AI 開示1行が無ければ FAIL。全生成ビジュアル区間で右下 `AI-assisted visualization` が焼かれていること（§13 アイボールで確認） |

**出力:** `09_package/facts_lock.v001.json`（`{"pass":bool,"violations":[{"file","rule","line","excerpt"}],"skipped":[...]}`）。`pass:true` でない限り `check_final_acceptance.py` に進まない。

## 1.4 画面に出してよい確定数値／固定語（★台帳 F01–F17 に存在するものだけ。この表以外を画面に出すな）

| ID | 値／文言 | 台本での表現（claim） | conf | 使用先 |
|---|---|---|---|---|
| N01 | **6 – 3** | "a vote of six to three"（F13） | high | AE **v01**（VOTE_SPLIT）/ figures `votetally`（F13/F14・中立帰属） |
| N02 | **NEW JERSEY v. T.L.O., 469 U.S. 325 · JANUARY 1985** | 台本カード（F01）／"in the middle of the nineteen-eighties" | high | AE **t01**（DATE_STAMP）/ figures `lowerthird`/`timeline`（F01） |
| N03 | **NO WARRANT · NO PROBABLE CAUSE** | "does not need a warrant, and does not need probable cause"（F10） | high | AE **n01**（CENTER_STACK・**"the 4th still applies" 併記**）/ figures `kinetic:emphasis`（F10） |
| N04 | **PROBABLE CAUSE → REASONABLE SUSPICION** | "probable cause … reasonableness … reasonable suspicion"（F10） | high | AE **p01**（SPLIT_COMPARE・引き下げ）/ figures `compbars`（F10） |
| N05 | **TWO-PART TEST**（JUSTIFIED AT INCEPTION · REASONABLE IN SCOPE） | "a two-part test … justified at its inception … reasonably related in scope"（F11） | high | AE **x01**（CENTER_STACK）/ figures `lowerthird`（F11） |
| N06 | **White 逐語 prong-1** "…there must be reasonable grounds for suspecting that the search will turn up evidence that the student has violated or is violating either the law or the rules of the school" | 台本 ACT3（F11） | high | AE **q01**（QUOTE_CARD・帰属 White）/ figures `quote`（F11） |
| N07 | **WHEN POLICE STEP IN**（A HIGHER STANDARD CAN APPLY） | "When the police get involved … a different and higher standard can come back"（F15） | high | AE **b01**（CENTER_STACK・footnote 7）/ figures `mechanism:faultsplit`/`lowerthird`（F15） |
| N08 | **THE 4TH APPLIES IN SCHOOL** | "The Fourth Amendment travels with you into a public school"（F09） | high | AE **v01** sub / figures `lowerthird`（F09） |

> **★AE カード文言・figures に「no rights / search anything / probable cause required（学校の基準として）/ 別の票数 / 学校名 Piscataway / 副校長名 Choplick / 薬物の扇情語」を書かない（C1–C6）。** quote は §2 `APPROVED_QUOTES` の White 逐語のみ・帰属 **"Justice White, for the Court"**（R-QUOTE）。**14歳・薬物の押収物は figures/AE の数値にしない**（未成年＝象徴のみ・薬物＝臨床的最小限。数字カード化＝扇情の入口）。

---

# 2. 視覚・音響レーン分離（EP39〜45 との素材被り回避）＋ APPROVED_QUOTES

> **EP39〜45 のファイルには一切触れない（読み取りのみ可）。** レーンを機械的に分離する。

| 軸 | EP45 cleveland | **EP46 tlo** |
|---|---|---|
| 舞台 | 温いランプの台所→冷灰 booking→大理石 | **温い事務灯の机の上のハンドバッグ（木目）→ 学校の廊下/ロッカー・空の教室・トイレのドア → 天秤（probable cause↔reasonable suspicion）→ 校門/校旗（schoolhouse gate）→ 淡い最高裁列柱・二段の階段（inception→scope）→ 警官のバッジ（footnote 7）→ 夜明けのロッカー廊下** |
| 支配的出来事 | 罰金の雪だるま→収監→JCS | **トイレの喫煙→机の上のバッグ捜索（タバコ→巻紙 plain view→更なる押収）→ 校門の権利（4Aは適用）→ reasonableness と二段テスト・6-3・footnote 7 警察留保** |
| アクセント色 | crimson | **schoolhouse-green `#3F8F5F`** |
| ベース色 | 温 near-black + 大理石 + 冷灰 | **温い机 `#171310` + 黒板グリーン `#14201B` + 冷灰ロッカー `#22262A` + 大理石 `#34363B` + near-black `#0A0A0C`** |
| レンズ感 | — | **HOOK 象徴モンタージュ（~2s cut・現在形）／ACT1 最短・抑制（その捜索）／ACT2 正対の転回（校門の権利・二つの easy answer を却下）／ACT3 正対対称・荘厳・最も遅い（reasonableness・二段テスト・6-3・footnote 7）／ENDING 引き（pull-back・ロッカー廊下）** |
| 画像保存先 | `H:\pd-media\assets\ai\cleveland\` | **`H:\pd-media\assets\ai\tlo\`** |
| Remotion データ | `cleveland_film.json` | **`tlo_film.json`** |
| Remotion コンポ | `Ep45Cleveland` | **`Ep46Tlo`** |
| AE 作業ディレクトリ | `…/PD-2026-045-cleveland/08_edit/ae_hero/` | **`…/PD-2026-046-tlo/08_edit/ae_hero/`** |

**素材被り禁止:** EP39〜45 と同一の factory clip / AI画像を1点も使わない。選定前に `episodes/PD-2026-039-*/`〜`…-045-*/` の `05_stock/stock_ledger*.json` を読み sha256 重複を除外（CODEX_A・BLOCKING）。

## 2.1 `APPROVED_QUOTES`（★逐語のみ・帰属固定・R-QUOTE / figures `quote` / AE `q01` はこの3本からのみ）

いずれも **attribution = `Justice White, for the Court`**（表示は全大文字可）。要約を引用符に入れたら FAIL。

```
Q-TWOFOLD:
"Determining the reasonableness of any search involves a twofold inquiry: first, one must
consider whether the ... action was justified at its inception; second, one must determine
whether the search as actually conducted was reasonably related in scope to the circumstances
which justified the interference in the first place."

Q-PRONG1（★AE q01 の本文・N06）:
"there must be reasonable grounds for suspecting that the search will turn up evidence that the
student has violated or is violating either the law or the rules of the school."

Q-PRONG2:
"the measures adopted are reasonably related to the objectives of the search and not excessively
intrusive in light of the age and sex of the student and the nature of the infraction."
```

---

# 3. 尺と構成 — SPEC の値をそのまま使う

## 3.1 全区間タイムライン（★この表が唯一の正・秒は fps=30 から算出しフレーム直書き禁止・0〜715.9s 全区間）

**算出基準:** SPEC の `narration_seconds = 715.9`（マスター）を `tlo_film.json` の `narrationSeconds` に入れる。**手計算で上書きしない。** 幕秒は SPEC `acts[]` の値をそのまま使う（HOOK 48.5 / OPENING 43.5 / ACT1 121.3 / ACT2 109.2 / ACT3 253.7 / ENDING 115.6・SELF-CHECK 9.1 は台本 apparatus ＝ナレ非対象で除外）。フレーム = `Math.round(30 × 秒)`。

> **★構成順（EP46 は preroll モデル・EP45 と異なる）:** `hookSeconds=8.0` のコールドティザー（無音/sound-forward の flash-forward・S01–S04 象徴）→ `BrandOpening` 3.50 → 以降ナレ本編（HOOK→OPENING→ACT1–3→ENDING）→ `BrandEndcard` 9.00。**ティザー 8.0 ＋ BrandOpening 3.50 ＝ 11.5s が preroll**＝BGM/AE の `film_offset OFF=11.5`（§4.3/§7.7）と一致。台本 HOOK 注記「gold BrandOpening が hook question 後に resolve」は、**ティザーが cold-open を担い→BrandOpening resolve→ナレ本編（HOOK ナレ）開始**という preroll 実装で実現する（この1点のみ台本の文中順序より SPEC/ブリーフの hookSeconds=8.0・OFF=11.5 を優先＝CODEX_B は本モデルで統一）。

| # | ブロック | 役割 | 語数 | 幕秒 | 台本指定の沈黙 | 固定尺 | 開始f(絶対) | 終了f(絶対) |
|---|---|---|---|---|---|---|---|---|
| 1 | **HOOK teaser（cold open）** | `hook` | 0 | — | — | **8.00**（hookSeconds） | 0 | 240 |
| 2 | **BrandOpening** | `opening` | 0 | — | — | **3.50** | 240 | 345 |
| 3 | **HOOK** ナレ | `body(narration)` | 144 | 48.5（SPEC） | **1.8**（"hold on the open purse"→hard cut・fully silent） | — | 345 | 1800 |
| 4 | **OPENING** ナレ | `body(narration)` | 129 | 43.5（SPEC） | — | — | 1800 | 3105 |
| 5 | **ACT1** The search（その捜索） | `body` | 360 | 121.3（SPEC） | — | — | 3105 | 6744 |
| 6 | **ACT2** Rights at the schoolhouse gate | `body` | 324 | 109.2（SPEC） | — | — | 6744 | 10020 |
| 7 | **ACT3** Reasonableness（判例核・最長・最も遅い） | `body` | 753 | 253.7（SPEC） | — | — | 10020 | 17631 |
| 8 | **ENDING**（payoff→CTA） | `ending` | 343 | 115.6（SPEC） | **2.0**（"a hallway of lockers, a distant bell"＝sound-forward） | — | 17631 | 21099 |
| 9 | **BrandEndcard** | `ending` | 0 | — | — | **9.00** | 21099 | 21369 |

> **ナレ base（narration-local frame=0）は絶対 frame 345（=11.5s）。** §3.1b の frame 列は **narration-local**（0＝HOOK ナレ開始）。絶対 frame = narration-local + 345。**film_offset = 11.5**（BGM/AE composite）。
> **幕秒積算 nominal（絶対 21369f）と §3.1[3] の `caseFilmDurationInFrames` 出力 22092 の差 723f=24.1s は、narrationSeconds マスター 715.9 と発話幕秒合計 691.8 の差＝息継ぎ＋設計無音2点（1.8+2.0=3.8s）を内包する測定マスター。** film.json には 715.9 を入れる。CODEX_B は `tlo_film.json` の segment 順から再計算し一致を確認。

### 検算（CODEX_B は必ず自分で再計算して一致を確認）

```
[1] narrationSeconds = 715.9（SPEC マスター。手計算で上書きしない）
    ※ 発話ブロック HOOK..ENDING の幕秒合計 = 48.5+43.5+121.3+109.2+253.7+115.6 = 691.8s。
      SPEC マスター 715.9 との差 24.1s は、幕間の息継ぎ＋設計無音2点（1.8+2.0=3.8s）を内包した測定マスター。
    ※ mean_shot 検算: 715.9 / 224 = 3.196s ＝ SPEC mean_shot_seconds 3.2 一致（224カットは 715.9s 全域に張る）。

[2] 総尺 = hookSeconds 8.0 + BrandOpening(OPENING_SEC) 3.50 + narrationSeconds 715.9 + BrandEndcard(ENDCARD_SEC) 9.00
        = 736.4 秒 = 12:16.4
    ※ hookSeconds=8.0（EP45 は 0）。ティザー 8.0 + BrandOpening 3.5 = 11.5 が preroll＝film_offset OFF=11.5。

[3] caseFilmDurationInFrames(tloFilm, 30) = 4項の実関数で算出（round(30×736.4) の単項近似ではない）:
      = round(hookSeconds×30) + round(OPENING_SEC×30) + ceil(narrationSeconds×30) + round(ENDCARD_SEC×30)
      = round(8.0×30)=240 + round(3.5×30)=105 + ceil(715.9×30)=ceil(21477.0)=21477 + round(9.0×30)=270
      = 22,092 フレーム
    ※ CODEX_B は tlo_film.json の hookSeconds/narrationSeconds（＋Bookends の OPENING_SEC/ENDCARD_SEC）から
      同関数で再計算し 22092 に一致することを assert する。

[4] runtime_band ≤ 750s の assert（BLOCKING）:
    総尺 = 736.4s = 12:16.4 は band 690–750（11.5–12.5分）の内側（上限 750s に対し 13.6s の余裕）    ✓ PASS
```
> **VO 実測で確定:** `measure_vo_wpm`（合格帯 168–190 wpm）でナレ実測。実測が SPEC マスターと乖離したら CODEX_B は `narrationSeconds` を実測値で更新（planning は 715.9・final は実測が権威）。190超は破棄・speed 0.95 で再発注（BLOCKING）。

## 3.1b 秒×アニメーション・タイムライン（★0→715.9s 全区間・各beat の start/end フレーム（narration-local）・移動量・easing・damping・stagger・Trail）

> **フレームは全て `f(sec)=Math.round(30×sec)`（narration-local・絶対は +345f）。等速線形ゼロ・opacity 単独ゼロ・静止フレームゼロ。** 下表は各 narrative シーン（§3.2 の S01..S48）の主アニメ。カット境界は `QUANT=f(0.5)=15f` グリッドにスナップ（§10.1）。still は Ken Burns（`scale 1.00→1.08`＋drift ±24px・`Easing.out(Easing.cubic)`）を全長。テキスト見出し/figures は `overflow:hidden` 親＋子 `translateY(110%→0)` の spring 切れ上がり（`damping:16,mass:1`・スタッガー `f(0.04)=2f/文字`）を基本形。★fast move（Trail 対象）は「Trail」列に明記。

| 区間(秒) | 開始f–終了f | シーン | 主アニメ（プロパティ・移動量） | easing / damping | stagger | Trail |
|---|---|---|---|---|---|---|
| 0.0–9.0 | 0–270 | S01 机の上のハンドバッグ（HOOK・~2s cut） | still Ken Burns `scale 1.00→1.06` / drift +18px | `Easing.out(Easing.cubic)` | — | — |
| 9.0–18.0 | 270–540 | S02 バッグを開けるジッパー（i2v・手元のみ） | i2v native ＋ `scale 1.00→1.03` | native + cubic | — | **✓** |
| 18.0–27.0 | 540–810 | S03 洗面台の上の薄い煙（臨床・無人） | still `scale 1.00→1.07` / drift +20px | `Easing.out(Easing.cubic)` | — | — |
| 27.0–36.0 | 810–1080 | S04 トイレのドアが閉じる（i2v・**fast**） | i2v swing・数値見出しなし | native | — | **✓** |
| 36.0–46.7 | 1080–1401 | S05 開いたバッグ・タバコが覗く（静止保持） | still `scale 1.00→1.04` 微動 | `Easing.inOut(Easing.sin)` | — | — |
| 46.7–48.5 | 1401–1455 | DESIGNED SILENCE 1.8s（開いたバッグを保持→hard cut・fully silent） | still 微動・BGM mute・完全無音 | `Easing.inOut(Easing.sin)` | — | — |
| **48.5–52.0** | **1455–1560** | **BrandOpening を挟まず OPENING へ hard cut**（gold は preroll 済・§3.1 注） | — | — | — | — |
| 52.0–66.0 | 1560–1980 | S06 公立高校の外観・校旗（OPENING・factory） | factory 内在動き＋微 KB `scale 1.00→1.04` | `Easing.out(Easing.cubic)` | — | — |
| 66.0–80.0 | 1980–2400 | S07 バックパックとロッカー（自分の bag）・kinetic "THE BAG ON THE DESK" | still KB＋kinetic 切れ上がり | spring `damping:16,mass:1` | 2f/文字 | **✓** |
| 80.0–95.5 | 2400–2865 | S08 校門＋遠景に最高裁列柱（最高裁への距離） | still push-in `scale 1.00→1.08` / drift +12px | `Easing.out(Easing.cubic)` | — | — |
| 95.5–120.0 | 2865–3600 | S09–S10 ACT1: 洗面台のタバコ→前office・acttitle "THE SEARCH" | still KB＋acttitle 切れ上がり | spring `damping:16` | 2f/文字 | **✓** |
| 120.0–150.0 | 3600–4500 | S11–S12 バッグを一つずつ→事務室のドアが閉じる（i2v・**fast**）・kinetic "ONE ITEM AT A TIME" | still KB＋i2v door＋kinetic | spring `damping:16` / native | 2f/文字 | **✓** |
| 150.0–175.0 | 4500–5250 | S13–S15 タバコ→巻紙(plain view)→押収物を臨床的に並べる・lowerthird（F05/F06・臨床） | still KB drift ±24 交互・lowerthird `translateY 24px→0`＋opacity | `Easing.out(Easing.cubic)` / spring `damping:20` | — | — |
| 175.0–200.0 | 5250–6000 | S16–S17 名簿/2通の手紙(判読不能)→排除申立(judged) | still KB・lowerthird | `Easing.out(Easing.cubic)` | — | — |
| 200.0–216.8 | 6000–6504 | S18 court by court へ積み上がる書類・timeline F07（手続史） | `timeline` events settle | `Easing.out(Easing.cubic)` | — | — |
| 216.8–245.0 | 6504–7350 | S19–S20 ACT2: 空の教室→校門/校旗（i2v・緩）・acttitle "RIGHTS AT THE SCHOOLHOUSE GATE" | still KB＋i2v gate＋acttitle | spring `damping:16` / native | 2f/文字 | — |
| 245.0–280.0 | 7350–8400 | S21–S22 in loco parentis の机 vs 令状/ガベル・compbars F08（二つの easy answer を却下） | `compbars` barX `scaleX 0→1` origin left | spring `damping:18` | — | — |
| 280.0–305.0 | 8400–9150 | S23–S24 ロッカーが半開き／未署名の令状・kinetic:emphasis "NOT RIGHTLESS"(["NOT"])＋lowerthird F09 | `kinetic:emphasis` 切れ上がり・lowerthird | spring `damping:16` | 2f/文字 | **✓** |
| 305.0–326.0 | 9150–9780 | S25–S26 ロッカー廊下（factory）→校門を4Aが通る・lowerthird F09 "travels with you" | factory KB・lowerthird | `Easing.out(Easing.cubic)` | — | — |
| 326.0–345.0 | 9780–10350 | S27–S28 ACT3: 最高裁列柱（factory→still push-in）・acttitle "REASONABLENESS"＋votetally 6–3 | acttitle 切れ上がり・`votetally` count settle | spring `damping:16` | 2f/文字 / 2f/tally | **✓** |
| 345.0–360.0 | 10350–10800 | S29 U.S. Reports 巻・lowerthird F01(469 U.S. 325 · White)＋timeline F01(1984→1985) | lowerthird・`timeline` settle | `Easing.out(Easing.cubic)` | — | — |
| 360.0–385.0 | 10800–11550 | S30–S31 天秤(静止)→天秤が傾く(i2v・緩)・lowerthird F09 holding-1(4A applies) | still KB＋i2v balance・lowerthird | native + cubic / spring | — | — |
| 385.0–410.0 | 11550–12300 | S32 no warrant / no probable cause・kinetic:emphasis "NO WARRANT"(["NO"])＋compbars F10(PC vs RS) | `kinetic:emphasis`・`compbars` scaleX | spring `damping:16/18` | 2f/文字 | **✓** |
| 410.0–430.0 | 12300–12900 | S33 開いた意見集(White)・lowerthird F10 "lowered, not eliminated" | lowerthird `translateY 24px→0`＋opacity | spring `damping:20` | — | — |
| 430.0–470.0 | 12900–14100 | S33–S34 二段テスト→二段の階段・quote Q-TWOFOLD(→ White) | `quote` maskslide＋attribution fade | `Easing.out(Easing.cubic)` | 2f/語 | — |
| 470.0–505.0 | 14100–15150 | S34–S35 inception→scope・光が階段を昇る(i2v・緩)・quote Q-PRONG1＋Q-PRONG2(→ White) | `quote` maskslide・i2v light | `Easing.out(Easing.cubic)` / native | 2f/語 | — |
| 505.0–528.0 | 15150–15840 | S36 バッグの各物が線で連なる→mechanism gears(test governs)・lowerthird F12(both prongs) | `mechanism:gears`・lowerthird | spring `damping:16` | — | **✓** |
| 528.0–550.0 | 15840–16500 | S37 1本のタバコ vs 空にされたバッグ・kinetic:emphasis "SCOPE CAN OUTGROW ITS EXCUSE"(["OUTGROW"]) | `kinetic:emphasis` 切れ上がり | spring `damping:16` | 2f/文字 | **✓** |
| 550.0–566.0 | 16500–16980 | S38–S39 少し離れた3脚の椅子（反対）・lowerthird F14（Brennan/Marshall/Stevens・中立） | lowerthird・still KB | `Easing.out(Easing.cubic)` / spring | — | — |
| 566.0–579.7 | 16980–17391 | S40–S43 警官のバッジ→断層線(footnote 7)・mechanism:faultsplit F15 | `mechanism:faultsplit` line | `Easing.out(Easing.cubic)` | — | **✓** |
| 579.7–600.0 | 17391–18000 | S44 ENDING: バッグへ回帰・kinetic "DOES THE FOURTH AMENDMENT WALK IN WITH YOU?" | `kinetic` maskslide | spring `damping:16` | 2f/文字 | **✓** |
| 600.0–640.0 | 18000–19200 | S45–S46 ロッカー/バックパック→夜明けの校門・lowerthird F10 answer("reasonable suspicion, in proportion") | still KB・lowerthird | `Easing.out(Easing.cubic)` / spring | — | — |
| 640.0–675.0 | 19200–20250 | S47 reasonable suspicion の天秤・kinetic:emphasis "A THIRD THING"(["THIRD"])＋lowerthird F15 reminder | `kinetic:emphasis`・lowerthird | spring `damping:16` | 2f/文字 | **✓** |
| 675.0–693.3 | 20250–20799 | S48 ロッカー廊下・遠い鐘・開くドア(i2v・pull-back)・DESIGNED SILENCE 2.0s・sound-forward | i2v native ＋ slow `scale 1.00→1.02` pull-back・BGM mute | native + `Easing.out(Easing.cubic)` | — | — |
| 693.3–715.9 | 20799–21099相当 | CTA（"worth a like"）→ BrandEndcard 9.00 開始（絶対 21099） | 字幕のみ・**沈黙区間に字幕キューを置かない** | — | — | — |

> **★背面レイヤーは常に4層以上動く（§8.1）。** 上表の各 0.5s 境界で「動いている要素」が最低1つある（静止区間ゼロ）。Trail 対象（fast move）は **S02 ジッパー / S04 トイレのドア swing / S12 事務室のドア closingdoor / 幕頭 acttitle・kinetic・emphasis の切れ上がり / votetally の count / mechanism gears の噛み合い / faultsplit の線割れ**。**S05/S31 天秤・S35 階段の走光・S20 校門・S48 ロッカー廊下 pull-back・Ken Burns には Trail をかけない**（無駄な残像・扇情を避ける・C5）。

## 3.2 シーン→幕の割当（★SPEC の S01..S48 を固定・別番号を発明しない・48シーン）

各シーンは narrative beat。224カットを 48シーンに分散（平均 4.67カット/シーン）。`primary` は各シーンの主素材（still=SDXL 各1枚 / factory=実写 / motion=i2v）。ambient/繋ぎは factory を各シーンに撒く（§5.1）。**象徴のみ・6制約順守・未成年の肖像化禁止・薬物は臨床的最小限。絵コンテ級の記述は §9。**

> **★2つの `Sxx` 名前空間は別物（取り違え禁止）:** 本節の **narrative シーンは `S01..S48`**（この表の絵コンテ）。一方 **still 資産 ID は `S01..S84`**（CODEX_A §2 注記・1プロンプト=1枚で48シーンに84枚を配分）。同じ `Sxx` 表記でも DESIGN §3.2/§9 の Sid（narrative）と CODEX_A/asset_manifest の scene_id・covers_scene_id（still 資産 ID）は指すものが異なる。横断参照時は「どちらの空間か」を明示し、cross-map しない。

| Sid | 幕 | 内容（象徴・6制約） | primary |
|---|---|---|---|
| S01 | HOOK | 事務机の上に置かれた閉じたキャンバスのハンドバッグ・温い事務灯（机の上のバッグ＝物語の起点） | still |
| S02 | HOOK | バッグを開けるジッパー（i2v・手元のみ・顔なし） | **motion** |
| S03 | HOOK | 学校のトイレの洗面台の上の薄い煙（臨床・無人・非扇情） | still |
| S04 | HOOK | 学校のトイレのドアが閉じる（i2v: swing shut・**fast**） | **motion** |
| S05 | HOOK | 開いたバッグからタバコが覗く（静止保持・DESIGNED SILENCE 1.8s の画・hard cut へ） | still |
| S06 | OPENING | ありふれた公立高校の外観・校旗（establishing・factory） | factory |
| S07 | OPENING | 生徒のバックパックと閉じたロッカー（＝あなた自身の bag／locker） | still |
| S08 | OPENING | 校門・遠景に淡い最高裁列柱＝小さな捜索から最高裁までの距離 | still |
| S09 | ACT1 | トイレの洗面台の縁に置かれた2本のタバコ・薄い煙（校則違反・臨床・無人） | still |
| S10 | ACT1 | 学校の前office のカウンター（無人・institutional） | still |
| S11 | ACT1 | 机の上でバッグの中身が一つずつ取り出される（象徴・手元まで） | still |
| S12 | ACT1 | 副校長室のドアが閉じる（i2v: closingdoor・**fast**） | **motion** |
| S13 | ACT1 | 開いたバッグの上に乗った1箱のタバコ | still |
| S14 | ACT1 | タバコの脇に巻紙(rolling papers)が plain view で覗く＝捜索継続の hinge（臨床） | still |
| S15 | ACT1 | 机に臨床的に並べられた押収物: 少量のマリファナ(封)・パイプ・空の小袋・1ドル札の束・名簿カード・2通の手紙＝evidence 陳列（**美化しない・非扇情**） | still |
| S16 | ACT1 | 名簿カードと2通の手紙（名前は判読不能）＝売買を示す・事実提示のみ | still |
| S17 | ACT1 | 少年審判の証拠排除申立の書類(判読不能)＝purse を throw out の申立 | still |
| S18 | ACT1 | court by court へ積み上がる court 書類＝Washington へ climb | still |
| S19 | ACT2 | 机と椅子が整列した空の教室＝schoolhouse（象徴） | still |
| S20 | ACT2 | 校門/校旗（i2v: 門が開き 4A が通る・緩）＝生徒は校門で権利を捨てない | **motion** |
| S21 | ACT2 | 校長机のネームプレート(判読不能)＝in loco parentis（学校の easy answer） | still |
| S22 | ACT2 | 令状フォームとガベル(判読不能)＝police standard（もう一つの easy answer） | still |
| S23 | ACT2 | 半開きのロッカーの列＝any bag を empty できる（学校の答えの危うさ） | still |
| S24 | ACT2 | 教室の机に置かれた物＋未署名の令状＝千人の校舎は paperwork で回らない（警察の答えの危うさ） | still |
| S25 | ACT2 | 冷灰のロッカー廊下（factory ambient）＝学校という場 | factory |
| S26 | ACT2 | 光の差す開いた校門＝4A は校内で real（travels with you） | still |
| S27 | ACT3 | 夕暮れの最高裁の外観列柱（factory ambient・establishing）＝最高裁 | factory |
| S28 | ACT3 | 淡い大理石の最高裁列柱・正対・荘厳＝Court が線を引く | still |
| S29 | ACT3 | 閉じた U.S. Reports の1巻(判読不能の背)＝469 U.S. 325 | still |
| S30 | ACT3 | 静止した天秤（一皿 probable cause・他皿 reasonable suspicion）＝Court が weigh した balance | still |
| S31 | ACT3 | 天秤が probable cause から reasonable suspicion へ傾く（i2v: 傾く・緩）＝引き下げ（消滅でない） | **motion** |
| S32 | ACT3 | 脇に退けられた令状フォーム＋薄れる "probable cause"＝no warrant · no probable cause（象徴・判読不能） | still |
| S33 | ACT3 | 温い灯の下に開いた意見集・抽象行(判読不能)＝White が二段テストを書く | still |
| S34 | ACT3 | 二段の階段: 一段目 inception・二段目 scope＝二段テスト（段に読める文字は置かない） | still |
| S35 | ACT3 | 二段の階段を昇る刻印風の光(i2v: 光が昇る・緩)＝inception→scope | **motion** |
| S36 | ACT3 | 机の上のバッグ・各押収物が細い線で連なる＝each step tied to the last・両 prong を満たす | still |
| S37 | ACT3 | 1本のタバコ vs 空にされたバッグの対比＝scope は excuse を outgrow し得る（噂の1本で全部は取れない） | still |
| S38 | ACT3 | 多数の席から少し離れた3脚の空席＝Brennan/Marshall/Stevens 一部反対（顔なし・中立） | still |
| S39 | ACT3 | 水平に保たれた天秤＝2世紀 probable cause が守った（反対意見の見方・中立） | still |
| S40 | ACT3 | 机に置かれた警官のバッジ・冷光＝footnote 7: 警察が step in（顔なし） | still |
| S41 | ACT3 | "school official" 側と "police" 側を分ける断層線(i2v の faultsplit は figures 側)＝留保された higher standard | still |
| S42 | ACT3 | 一方に校舎・他方にパトの灯・間に引かれた線＝引き下げは educator 用で law enforcement 用でない | still |
| S43 | ACT3 | 最高裁の大理石の段・引かれた線（ACT3→ENDING 繋ぎ・荘厳） | still |
| S44 | ENDING | 机の上のバッグへ回帰＝冒頭の問いへ戻る（go back to that purse） | still |
| S45 | ENDING | ロッカーとバックパック・ありふれた朝＝彼女の後に来た全ての locker と backpack | still |
| S46 | ENDING | 夜明けの校門を bag が越える＝4A は校内に walk in する・yes（人物なし） | still |
| S47 | ENDING | reasonable suspicion で釣り合った天秤＝a third thing, in between（比例で保つ） | still |
| S48 | ENDING | 長いロッカー廊下・遠い鐘・開くドアと光・slow pull-back（i2v: DESIGNED SILENCE 2.0s・sound-forward） | **motion** |

**source 集計（scene-primary）:** motion-primary **7**（S02 S04 S12 S20 S31 S35 S48）／factory-primary **3**（S06 S25 S27）／still-primary **38**。**scene-primary はカット全体の一部**で、残りは §5.1 の配分に従い CODEX_B の shotlist が 224 カット（still 100 / factory 92 / motion 32）へ機械展開する。**この表のシーン数・番号は固定（S01..S48）。**

---

# 4. 音の4層設計（ナレ / BGM / SFX / 環境音）

## 4.1 ラウドネス・voice（確定値・EP41〜45 と同一運用）

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

## 4.2 【DESIGNED SILENCE】2箇所の実装（★デジタル無音にしない・`bgm_present` を落とす）

台本の `【DESIGNED SILENCE …】` は**ナレの沈黙であって音の沈黙ではない**。台本には2箇所（**同一楽器化しない**＝HOOK は完全無音、ENDING のみ音を足す sound-forward・台本準拠）。

| 位置 | 秒 | 対応画 | 鳴らすもの |
|---|---|---|---|
| HOOK 末（"hold on the open purse"→hard cut） | **1.8** | S05（開いたバッグ・タバコが覗く） | BGM mute。**完全無音**（room tone も置かない・台本指定「fully silent」） |
| ENDING（"a hallway of lockers, a distant bell"＝payoff の sound-forward 沈黙） | **2.0** | S48（ロッカー廊下・開くドア） | BGM mute。**SFX を push**（廊下の低いハム→遠い学校の鐘→静けさ）。**この沈黙は音を運ぶ**（HOOK との対比） |

**最長無音 2.0秒 << 25秒** ✓ `bgm_present` PASS。**機械逓減にはせず**、HOOK を完全無音、payoff の ENDING を「音を足す沈黙」2.0s にして対比を作る。

## 4.3 章ごとの BGM（1章1トラック・`build_tlo_bgm_real.py`＝EP43 版を tlo 用に複製・`film_offset OFF=11.5` 適用）

| 区間 | 性格 | 楽器 |
|---|---|---|
| HOOK teaser | 低弦の不解決・単音が刺す cold open（トイレのドア・机の上のバッグ） | 低弦+単音メタル |
| BrandOpening | ブランドスティンガー（`BrandOpening` 付属） | — |
| HOOK ナレ | 現在形の緊張・抑制（一つずつ取り出す） | 低弦+疎パーカッション |
| OPENING | 転入部・二人称（あなたの bag／locker） | ピアノ+弦 |
| ACT1 | 最短・現在形・抑制（その捜索・巻紙 hinge） | 低弦+疎パーカッション |
| ACT2 | 校門の権利・二つの easy answer を却下する転回 | ピアノ+弦 |
| ACT3 | 法の荘厳・大理石。**最も遅い**。reasonableness・二段テスト・6-3・footnote 7 | 低弦+弦サステイン |
| ENDING | 解決しない和音 →「daylight/hallway」でだけ淡い緑（採光）に開く | ピアノ+弦 |
| ENDCARD | ブランドED（`BrandEndcard` 付属） | — |

> **`film_offset OFF=11.5`**（ティザー 8.0 ＋ BrandOpening 3.5）＝ナレ base が絶対 11.5s から始まる。BGM/SFX/字幕は全て OFF=11.5 を適用して整列（§3.1 検算）。

## 4.4 SFX

| 種別 | 位置 | 音 |
|---|---|---|
| zipper | S02 バッグを開ける | ジッパーの擦れ・-20 LUFS |
| restroom door | S04・HOOK teaser | 学校のドアの閉・軽い残響・-18 LUFS（サイレン/悲鳴なし・非扇情・C5） |
| office door | S12 副校長室 | institutional ドアの閉・-18 LUFS |
| paper/evidence | S15/S16 押収物 | 紙・小袋の擦れ・-24 LUFS（**扇情化しない**・臨床） |
| gavel/court | S17/S18 | 木槌の一撃・書類の擦れ・-16 LUFS |
| balance | S30/S31 天秤 | 金属の微かな軋み・-26 LUFS |
| light band | S35 二段の階段 | 微かな高域の走光音・-26 LUFS |
| corridor hum / bell | S25/S48 | 廊下の低いハム＋遠い学校の鐘（ENDING 2.0s で sound-forward）・-30→-24 LUFS |
| impact | AE 数値/カード着地（v01 の 6-3 count 等） | 低域インパクト・-12 LUFS |
| tick | votetally の count | 微細クリック・-24 LUFS |
| room tone | 全編ベッド（教室・大理石反響・ロッカー廊下） | 広いリバーブ・-30 LUFS（**沈黙 HOOK は完全無音**） |

---

# 5. ビジュアル — 素材積算（★紙芝居回避＝factory実写を必ず混ぜる・1シーン1枚）

## 5.1 素材の積算（★SPEC の値をそのまま満たす配分）

```
[0] 絵が必要な区間 = narrationSeconds 715.9（BrandOpening/Endcard/teaser は別レイヤー）
[1] 総カット = 224（SPEC）    715.9 / 224 = 3.196秒/カット  ✓ mean_shot 3.2（≤6.0）
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
[8] factory 下限 = 715.9/30 = 23.9 → ≥24本。設計値 92本   ✓
```
> **[6] の余裕は 0.36%pt しかない。still-cut を1つ増やすと 45% を割る。still-cut は 100 で固定**（16枚だけ2回・残り68枚1回）。QC で still が 84枚を割ったら §9 の**追加は同一シーンの別プロンプト（新規 distinct）**で回復させ、**cut 数は増やさない**。**still を増やして factory を削るな。factory 92 が still-share≤0.45 を守る下限。**

## 5.2 SDXL と実写在庫の振り分け

- **SDXL（still 84・各1枚）= この事件にしか無い固有物**: 机の上のハンドバッグ・トイレのドア/洗面台の煙・開いたバッグ/タバコ/巻紙・押収物の陳列・名簿/2通の手紙・空の教室・校門/校旗・ロッカー・令状フォーム/ガベル・天秤・U.S. Reports 巻・意見集・二段の階段・警官のバッジ・断層線・夜明けの校門。
- **factory 実写 92 = どこにでもある周辺**: 公立高校の外観・校旗・最高裁の外観/列柱・大理石テクスチャ・長い institutional 廊下・ロッカー廊下・空の教室 ambient・繋ぎ。

## 5.3 SDXL 生成量（★バリエーション0・variants 禁止）

- `ai_prompts.v001.md` = **body 84行の固有プロンプト**（still 各1枚）＋ i2v 種 **16行** ＝ **計100エントリ**（`--only S01` の `shots=` は 100）。`generate_sdxl_4k.py PD-2026-046-tlo`（**`--variants 1` または指定なし**）。**`--variants 3` を書かない。**
- i2v-source = **16枚**（動きが意味を持つ絵の固有プロンプト・各1シード）。CODEX_A が Wan 2.2 A14B → RIFE 48fps で 16本生成。
- **総生成 = still 84 + i2v seed 16 = 100枚（各1回）。** factory 92 は生成せず在庫選抜。
- プロンプト実体（84本）・i2v リスト（16）・factory 選定（92）は **CODEX_A** の担当（本書 §9 は絵コンテ級の記述と共通スタイル/ネガティブの契約のみ）。

## 5.4 factory のファイル名を信じない（★必須工程・CODEX_A・BLOCKING）

> EP36: `city_surveillance_camera_dome` が実際は大聖堂。EP38: 牛が `documents_on_desk`。ラベルは検索語の記録であって中身の保証ではない。

選定した **92本すべて**を `scripts/build_footage_contact_sheet.py --ep PD-2026-046-tlo --media video --dir <factory staging>` で1本1フレームのラベル付きコンタクトシート（`runs/qc/tlo_footage_contact_NN.png`）にし**全点目視**。subtype と食い違う本は差し替える。`select_tlo_factory.py --verify-no-prior-overlap`（`--exclude-used --ep PD-2026-046-tlo`）で EP39〜45 の sha256 被りゼロを確認。

## 5.5 共通スタイル接尾（各 SDXL プロンプト末尾に必ず付ける・`[STYLE]`・CODEX_A §5.4 と同一）

```
, cinematic still, cool-and-warm documentary grade, an ordinary American public-school world: a
canvas handbag on a wooden administrator's desk under warm office lamplight, cool grey
institutional hallways and lockers, an empty classroom and a restroom door, pale marble Supreme
Court columns, a set of scales and a two-step staircase, a single schoolhouse-green accent as the
one color note, restrained and dignified symbolism, telephoto compression and frontal
composition, shallow depth of field, ultra-detailed, photoreal, 4K, 16:9, fine film grain, no
text, no watermark, no logo, symbolic still-life, no people, no visible face, no minor, no child
```
> EP39〜45 との分離: 接尾に `electric blue`（EP39）・`midday suburban`（EP40）・`sodium prison corridor`（EP41）・`ankle monitor`/`warrant-blue`（EP42）・`porch-amber`/`ambulance`（EP43）・`teal-green hospital corridor`（EP44）・`overdue crimson`/`county-jail booking`（EP45）を**1語も含めない**。EP46 の唯一の一点差しは **schoolhouse-green `#3F8F5F`**。

## 5.6 共通ネガティブ（各 SDXL プロンプトの `Avoid:` に必ず付ける・`[NEG]`・CODEX_A §5.5 と同一）

```
text, words, letters, numbers, captions, watermark, logo, readable document, legible paper,
legible citation, legible date, real celebrity, recognizable real person, identifiable face,
portrait, mugshot, likeness of a specific person, human face, human body, child, teenager, girl,
minor, student's face, crying person, sensational distress, glamorous drugs, drug party, smoking
a joint, getting high, close-up of drug use, weapon, gun, blood, gore, nude, bare skin, cartoon,
illustration, anime, 3d render, low quality, blurry, jpeg artifacts, deformed, extra limbs,
prison cell, barred cell, sodium prison corridor, electric blue, teal-green hospital corridor,
clinical hospital, midday suburban daylight, porch amber house, ankle monitor, overdue crimson,
county-jail booking
```
> ネガティブにも **制約違反語（"students have no rights", "the 4th doesn't apply in school", "search anything", "probable cause required in school", 未成年の肖像語, 薬物扇情語 等）を書かない**（§1.3）。会社/学校ロゴが必要な絵は「blurred into an unreadable smear」で判読不能に。判例番号・日付・校名・人名を画に描かない（AE/figures＝B の担当）。**押収物（薬物）は sealed evidence を机に flat に並べた臨床描写のみ・美化しない。**

## 5.7 AI開示（強め・毎回・R1）

AI 生成の still・i2v が画面に出ている間、常時右下に **`AI-assisted visualization`**。Oswald 20px / `#C8CDD6` / opacity 70% / 位置 `[W-32, H-28]`。字幕帯と縦 56px 以上離す。概要欄1行: `Some visuals in this film are AI-assisted reconstructions, not photographs of the actual events.`（＋ローカルの student-rights / know-your-rights の1行。988 は出さない＝本作は生徒の第4修正権テーマ）。

## 5.8 ★A↔B 境界契約（asset_manifest スキーマ・EP39〜45 の不整合を最初から潰す）

- **接続点は `episodes/PD-2026-046-tlo/05_visuals/asset_manifest.v001.json` ただ1ファイル**。A(producer)＝CODEX_A が書き、B(consumer/validator)＝CODEX_B が読む。**counts と role enum を A/B で一字一致**させる。
- **スキーマ版:** `tlo_assets.v1`（固定文字列）。
- **マニフェスト配列（★A/B 同一）:** `stills` / `motion` / `factory` / `overlay` の4配列。**★factory 92・motion 16 も全エントリ記載**（public_path 必須。EP45 で factory/motion 空欠落→build 失敗の事故）。
- **counts オブジェクト（★このキー・値で固定・A/B 一字一致）:** `{ "still_body": 84, "still_i2v_source": 16, "motion": 16, "factory": 92, "overlay": 12 }`。cuts 展開は still 100 / factory 92 / motion 32。
- **`stills[].role` enum（★この3値のみ・A/B 同一・`thumb`/`still_thumb` を作らない）:** `body` / `i2v_source` / `reject`。asset_id は body `^TLO-S\d{2}$`（S01..S84）/ i2v種 `^TLO-MS\d{2}$` / motion `^TLO-M\d{2}$`。
- **サムネは `role="body"` かつ `also_thumb=true` の body still ちょうど6枚**（別 role を作らない・追加生成しない）。**候補集合（★still 資産 ID 空間・CODEX_A §4.3 と一字一致の A↔B 契約点）:** **`{S01, S07, S26, S46, S64, S82}`**。A・B は同一6 asset ID に `also_thumb:true` を立てる。**サムネに未成年・薬物・生数値を出さない（C5）。**
- **overlay 枚数も A/B 一致**（合成レイヤー・distinct 素材に数えない）。本書設計値 **overlay: 12**（particle/light/vfx）。
- CODEX_A は manifest を書いた直後 `build_tlo_asset_manifest.py --verify` で counts / role / also_thumb / overlay を突き合わせ、**A の値と B の期待が一字一致**であることを確認（不一致は BLOCKING）。**`also_thumb==true` の scene_id 集合が `{S01,S07,S26,S46,S64,S82}` で A↔B 同一**であることも検査する。

---

# 6. Remotion MGビート（FigureBeats）— ★密度下限 30 は必ずここで満たす・dochighlight 不使用

## 6.1 密度の設計（`tlo_film.json` の `figures[]`）

`check_motion_density`: 3つを AND。**body-minutes = narrationSeconds/60 = 715.9/60 = 11.932**。

| 指標 | floor | EP46 設計値 |
|---|---|---|
| density | ≥2.5/min | figures **36 beats / 11.932 = 3.02/min** ✓（SPEC beats_floor 30 に +6） |
| coverage | ≥0.25 | 36 beats × 平均 5.4秒 = 194.4秒 / 715.9 = **0.272** ✓ |
| variety | ≥3 distinct forms | **8種**（下記） ✓ |

> **AE の 7枠は film.json に入れない**（composite 後に焼くため gate 非カウント）。**density は Remotion 側 36 beats だけで 30 を超える。** coverage が floor 0.25 に一番近いので figures の dur は 4.8–6.0s を基本にする。

## 6.2 `figures[]` の種類配分（★kind は全部小文字・同一 kind を連続させない・★dochighlight 不使用）

**使用可能 kind（全小文字）:** `numberticker` `stat` `votetally` `timeline` `quote` `kinetic` `lowerthird` `acttitle` `compbars`（※`comparebars` は非実在）`mechanism`。**大文字は無音描画になる。** **★`dochighlight` を1件も入れない（R-DOCHL・grep 0）。証拠タグ/書類/押収物は `lowerthird` の説明テキストで表す。**
**★`mechanism` の subtype は実装済み3種のみ:** `closingdoor` / `gears` / `faultsplit`（`remotion/src/components/motionkit/presets/MechanismReveal.presets.ts` で確認済）。**`scales`/`twostep` という mechanism subtype は存在しない**→天秤・二段の階段は **still/i2v の scene art（S30/S31/S34/S35）＋AE カード（p01/x01）** で表現し、mechanism には渡さない。

| kind（小文字） | 枠数 | EP46 での用途（6制約適用） |
|---|---|---|
| `acttitle` | 3 | ACT1「THE SEARCH」/ ACT2「RIGHTS AT THE SCHOOLHOUSE GATE」/ ACT3「REASONABLENESS」 |
| `lowerthird` | 14 | 開示 `AI-assisted visualization`（HOOK/ENDING 2回）／押収物の臨床説明「a pack of cigarettes, then rolling papers in plain view」(F05)／findings 臨床列挙(F06)／F09「school officials are agents of the State」「the Fourth Amendment travels with you into a public school」／F01 判例(469 U.S. 325・White)／F10「lowered, not eliminated · reasonable suspicion」／F12「both prongs cleared」／F14「Brennan · Marshall · Stevens — concurring in part, dissenting in part」(中立)／F15「footnote 7 — school officials, not police」／ENDING の answer「reasonable suspicion, kept in proportion」。**校名/人名/薬物数値は出さない** |
| `kinetic` | 7（うち emphasis 4） | HOOK/OP「THE BAG ON THE DESK」／ACT1「ONE ITEM AT A TIME」／ACT2「NOT RIGHTLESS」(["NOT"]・F09)／ACT3「NO WARRANT」(["NO"]・F10)／ACT3「SCOPE CAN OUTGROW ITS EXCUSE」(["OUTGROW"])／ENDING「DOES THE FOURTH AMENDMENT WALK IN WITH YOU?」／ENDING「A THIRD THING」(["THIRD"])。**emphasisWords は1–2語＝文字切れ回避** |
| `quote` | 3 | Q-TWOFOLD／Q-PRONG1／Q-PRONG2（**全て帰属 Justice White, for the Court**・§2.1 逐語）。**要約を引用符に入れない・facts_lock で逐語確認** |
| `timeline` | 2 | ①手続史 F07: juvenile court denies suppression → adjudicated delinquent → NJ Supreme Court reverses → U.S. Supreme Court reverses ②F01: argued Mar 1984 → reargued Oct 1984 → decided Jan 15 1985 |
| `votetally` | 1 | 6 – 3・White for the Court・three dissenting in part（F13/F14・**中立帰属**・R-VOTE） |
| `compbars` | 2 | ①二つの easy answer を却下 F08: 「school: the 4th doesn't apply」vs「police standard: get a warrant / probable cause」＝both refused ②F10: 「probable cause (on the street)」vs「reasonable suspicion (in school)」＝lowered, not eliminated |
| `mechanism` | 4 | `closingdoor`（トイレのドア・HOOK）／`closingdoor`（副校長室のドア・ACT1）／`gears`（二段テストが still governs・ACT3）／`faultsplit`（footnote 7 の警察/学校職員の線・ACT3） |
| **合計** | **36** | variety = **8 figure-kinds** ✓ ≥3 |

> **★`dochighlight` / `comparebars` を1件も置かない（R-DOCHL）。** `graphics[]=[]`（空配列）。density は `figures+graphics+heroCuts` を合算するので figures 36 だけで floor 30 に +6。**（オプション）** テーマ的には `probablecause`(ProbableCauseMeter) や `burdenflip`(BurdenFlipScale＝天秤) も実装済で使えるが、本設計はブリーフ§5 の vetted-safe セット（上表8種）で 36 を満たす。Codex が採用する場合も 36 の総数と variety を崩さないこと。

## 6.3 配置方針（36本・§1.4 台帳の値だけを焼く・kind を分散・6制約順守・dochighlight 0件・CODEX_B §6.3 と一致）

- **HOOK/OP（3）:** `mechanism:closingdoor`（トイレのドア）/ `kinetic`（"THE BAG ON THE DESK"）/ `lowerthird`（`AI-assisted visualization` 開示）
- **ACT1（6）:** `acttitle`（THE SEARCH）/ `lowerthird`（"a pack of cigarettes, then rolling papers in plain view"・F05・臨床）/ `kinetic`（"ONE ITEM AT A TIME"）/ `lowerthird`（findings 臨床列挙・F06・**非扇情**）/ `mechanism:closingdoor`（副校長室のドア）/ `timeline`（手続史・F07）
- **ACT2（6）:** `acttitle`（RIGHTS AT THE SCHOOLHOUSE GATE）/ `compbars`（**F08** 二つの easy answer 却下）/ `lowerthird`（**F09** "agents of the State, not mere surrogates for parents"）/ `kinetic:emphasis`（"NOT RIGHTLESS"・["NOT"]・F09）/ `lowerthird`（**F09** "the Fourth Amendment travels with you into a public school"）/ `lowerthird`（"not whether you're protected — but how much, and by what test"）
- **ACT3（16）:** `acttitle`（REASONABLENESS）/ `votetally`（**F13/F14** 6 – 3・White for the Court・three dissenting in part・中立）/ `lowerthird`（**F01** New Jersey v. T.L.O., 469 U.S. 325 (1985)・opinion by Justice White）/ `timeline`（**F01** argued 1984 → reargued Oct 1984 → decided Jan 15 1985）/ `lowerthird`（**F09** holding-1: "the Fourth Amendment applies to school officials"）/ `kinetic:emphasis`（"NO WARRANT"・["NO"]・F10・hero は "NO WARRANT · NO PROBABLE CAUSE"）/ `compbars`（**F10** probable cause [street] vs reasonable suspicion [school]・lowered）/ `lowerthird`（**F10** "the standard is lowered, not eliminated"）/ `quote`（**Q-TWOFOLD** → White）/ `quote`（**Q-PRONG1** → White）/ `quote`（**Q-PRONG2** → White）/ `mechanism:gears`（二段テストが still governs）/ `lowerthird`（**F12** "each step tied to the last — both prongs cleared"）/ `kinetic:emphasis`（"SCOPE CAN OUTGROW ITS EXCUSE"・["OUTGROW"]）/ `lowerthird`（**F14** "Brennan, Marshall, Stevens — concurring in part, dissenting in part"・中立）/ `mechanism:faultsplit`（**F15** footnote 7 の警察/学校職員の線）
- **ENDING（5）:** `kinetic`（"DOES THE FOURTH AMENDMENT WALK IN WITH YOU?"）/ `lowerthird`（**F10** answer: "reasonable suspicion, tied to a real reason, kept in proportion"）/ `lowerthird`（**F15** reminder: "school officials — not police (footnote 7)"）/ `kinetic:emphasis`（"A THIRD THING"・["THIRD"]）/ `lowerthird`（開示 `AI-assisted visualization` 再掲）

## 6.4 配置ルール

1. **AE の 7区間（§7）と1秒でも重ならない**（`validate_tlo_beats.py`＝EP45 validate を複製・両方突き合わせ）。
2. 幕あたり配分: HOOK/OP=3 / ACT1=6 / ACT2=6 / ACT3=16 / ENDING=5（ACT3 が最長 253.7s なので厚め）。
3. **同じ kind を連続させない**（`mechanism` の直後に `mechanism` を置かない。closingdoor は HOOK/ACT1 で離す）。
4. 1枠 **4.8–6.0秒**。
5. ACT3 の説明区間に `quote`×3＋`compbars`＋`votetally`＋`mechanism`＋`lowerthird` を分散し 20秒超の平坦区間をゼロに。
6. `quote` は**逐語のみ**（要約を引用符に入れない・R-QUOTE）。帰属は3本とも "Justice White, for the Court"。
7. `figures[].*text*`/`lines[]`/`label`/`quote` は `facts_lock` 検査対象（過大化・probable-cause 誤り・別票数・校名/人名・薬物扇情・台帳外数値・**dochighlight**を出さない）。
8. `votetally` は 6-3 のみ・中立帰属（R-VOTE）。

## 6.5 密度の最終検算

```
Remotion figures 36（film.json 内・graphics 空）
  density  = 36 / 11.932 = 3.02/min   ✓ ≥2.5（SPEC beats_floor 30 → 36 で +6）
  coverage = 194.4s / 715.9 = 0.272    ✓ ≥0.25
  variety  = 8 forms                   ✓ ≥3
  dochighlight count = 0               ✓ R-DOCHL（grep 0）
AE hero 7枠は composite 後・gate 非カウント（上乗せの決め所）
```

---

# 7. After Effects ヒーロービート（7枠）— ★AEカードは密度に数えられない

## 7.1 大原則（★EP39/40 の致命傷を回避）

`check_motion_density` は **film.json の `figures` だけ**を数える。AE の 7枠は本編 mp4 に composite された後に焼き込まれるため gate は 0 カウント。→ **密度下限 30 は §6 の Remotion figures（36本）で満たす。** AE はその上に載る「決め所の数値タイポ」。

## 7.2 パイプライン（EP42/43/44/45 で measured 済み・tlo 用に複製）

```
[1] Remotion で本編完成 → tlo_final_bgm.v001.mp4（音声ミックス済み・build_tlo_bgm_real.py→film_offset OFF=11.5 適用）
[2] scripts/ae/build_tlo_hero_cards.py（＝build_cleveland_hero_cards.py を複製）が beats.json と tlo_hero.jsx を生成
[3] AfterFX -noui -r tlo_hero.jsx → 各ビートを 1920x1080@30fps の不透明 mp4 で書き出し
[4] scripts/ae/composite_tlo_hero.py（＝composite_cleveland_hero.py を複製）が ffmpeg overlay + enable='between(t,start,end)' で焼き込み
[5] 出力 → tlo_final_bgm.v002_ae.mp4（v001 は絶対に上書きしない・film_offset OFF=11.5 適用）
```

## 7.3 AEカードデッキ（★7枚・§1.4 の確定数値のみ・6制約適用・数値は台帳照合・accent #3F8F5F）

> **★レイアウトは複製元が実装する8種のみ**（`DATE_STAMP`/`CENTER_STACK`/`MONEY_STACK`/`SPLIT_COMPARE`/`ACT_TITLE_CARD`/`QUOTE_CARD`/`VOTE_SPLIT`/`SEAM_TRANSITION`）。**この表と CODEX_B §7.2 のデッキは id・レイアウト・F-ID が完全一致**（`validate_tlo_beats` が両方を突き合わせる）。上記8種以外の未実装レイアウト名は使わない。**EP46 は `VOTE_SPLIT`（6-3 が台帳にある）を使用。`MONEY_STACK`（金額が主役でない）/ `ACT_TITLE_CARD`（幕頭は Remotion `acttitle`）/ `SEAM_TRANSITION` は未使用。** variety は使用5種（VOTE_SPLIT/DATE_STAMP/CENTER_STACK/SPLIT_COMPARE/QUOTE_CARD）で ≥3 を満たす。

| id | レイアウト（実装済み8種） | hero（主表示） | top / sub / bottom / attribution | 数値ID | F-ID | 背景（象徴のみ・顔なし・未成年なし） | 尺 |
|---|---|---|---|---|---|---|---|
| **v01** | **VOTE_SPLIT** | **6 – 3** | top: **THE VOTE** / sub: **THE 4TH APPLIES IN SCHOOL** / bottom: **WHITE FOR THE COURT · THREE DISSENTING IN PART** | N01/N08 | **F13/F14/F09** | 最高裁列柱 | 6.5 |
| **t01** | **DATE_STAMP** | **1985 · SUPREME COURT** | place: **NEW JERSEY v. T.L.O., 469 U.S. 325** | N02 | **F01** | 大理石の段（判読困難） | 5.0 |
| **n01** | **CENTER_STACK** | **NO WARRANT · NO PROBABLE CAUSE** | top: **THE STANDARD, LOWERED** / bottom: **THE FOURTH AMENDMENT STILL APPLIES** | N03 | **F10/F09** | 脇に退けた令状フォーム＋校門 | 6.0 |
| **p01** | **SPLIT_COMPARE** | **PROBABLE CAUSE → REASONABLE SUSPICION** | top: **THE BAR THE COURT SET** / bottom: **LOWERED FOR SCHOOLS, NOT ELIMINATED** | N04 | **F10** | 左=street の天秤 / 右=schoolhouse の天秤 | 6.5 |
| **x01** | **CENTER_STACK** | **TWO-PART TEST** | top: **HOW REASONABLENESS IS MEASURED** / bottom: **JUSTIFIED AT INCEPTION · REASONABLE IN SCOPE** | N05 | **F11** | 二段の階段 | 6.0 |
| **q01** | **QUOTE_CARD** | **"...there must be reasonable grounds for suspecting that the search will turn up evidence that the student has violated or is violating either the law or the rules of the school"** | attribution: **JUSTICE WHITE, FOR THE COURT** | N06 | **F11** | 開いた意見集 | 7.5 |
| **b01** | **CENTER_STACK** | **WHEN POLICE STEP IN** | top: **FOOTNOTE 7** / bottom: **A DIFFERENT, HIGHER STANDARD CAN APPLY** | N07 | **F15** | 警官のバッジ（顔なし） | 6.0 |

> **★行順＝start 昇順（時系列・全て ACT3 内）:** `v01`(6-3・holding-1) < `t01`(判例日付) < `n01`(no warrant/no PC) < `p01`(PC→RS) < `x01`(two-part test) < `q01`(White 逐語 prong-1) < `b01`(footnote 7・警察)。**start は §7.4 beats.json で section 窓からオフセットで算出しクランプ**（rendered base の秒で単調増加・重複ゼロ）。**この id・レイアウト・F-ID は CODEX_B §7.2 デッキと一字一致。**
> **★q01 の QUOTE_CARD は逐語（R-QUOTE）。** 文字列は §2.1 `Q-PRONG1` と一致（大小無視・表示は全大文字）。**要約・言い換えを入れると R-QUOTE で FAIL。** 帰属は必ず **"JUSTICE WHITE, FOR THE COURT"**。
> **v01（VOTE_SPLIT）は 6-3 のみ・sub に "THE 4TH APPLIES IN SCHOOL"（C1＝無権利と読ませない）・bottom に "WHITE FOR THE COURT · THREE DISSENTING IN PART"（中立・R-VOTE）。別票数・"White が権利を奪った"式の帰属を書かない。**
> **n01 の hero "NO WARRANT · NO PROBABLE CAUSE" は bottom "THE FOURTH AMENDMENT STILL APPLIES" と必ず対（C1・R-OVERCLAIM）。「学校は何でも捜索できる」を書かない。**
> **p01 の bottom は "LOWERED FOR SCHOOLS, NOT ELIMINATED"（C1）。** 「probable cause required」式に誤読させない。
> **b01（footnote 7）は "WHEN POLICE STEP IN → A DIFFERENT, HIGHER STANDARD CAN APPLY"（C3）。「police can search students on reasonable suspicion」と一般化しない。**
> **どのカードにも「no rights / search anything / probable cause required（学校基準として）/ 別票数 / 校名 Piscataway / 副校長名 Choplick / 薬物の数値・扇情語」を書かない。** 数値ID＝台帳（§1.4）と一致必須。カウント/リビール終了から区間終端まで最低 1.20秒ホールド。em-dash は本文表示の `—` と異なり **beats.json ラベルでは ASCII `-` に置換**（AE の豆腐回避・§7.6）。

### 検算

```
[1] 7区間・本番 start 単調増加・重複ゼロ（build_tlo_hero_cards.py が section 窓オフセットで算出）
[2] HOOK teaser / BrandOpening / HOOK ナレ / ENDING payoff の沈黙(2.0s) / BrandEndcard に1秒も重ならない（全て ACT3 内に配置）
[3] 合計 = 6.5+5.0+6.0+6.5+6.0+7.5+6.0 = 43.5秒 / 736.4 = 5.9%   ✓ 過剰でない
[4] レイアウト種類 = VOTE_SPLIT, DATE_STAMP, CENTER_STACK, SPLIT_COMPARE, QUOTE_CARD = 5種（全て実装済み8種内）   ✓ ≥3
[5] figures[] 36枠と1秒でも重ならない（validate_tlo_beats.py が両方突き合わせ）
[6] dochighlight/comparebars レイアウトは存在しない（8種のみ）   ✓ R-DOCHL
```

## 7.4 `beats.json`（`08_edit/ae_hero/beats.json`・`schema_version: "tlo_beats.v1"`）

各 beat に `id` / `layout` / `start` / `end` / `dur` / `still`(象徴 or null) / `hero` / `top` / `bottom` / `sub` / `caption`(**改行禁止・最大50字**) / `value` / `numKeys` / `blend_mode`(既定 "overlay") / `required` / `out` / `attribution`(**QUOTE_CARD=q01 は必須**・§2.1 `Q-PRONG1` 帰属と一致・R-QUOTE)。**区間の秒は本番 rendered base（narration_index 由来・film_offset OFF=11.5 適用）に一致させ、section 窓からオフセットで算出しクランプ。** `v01` の 6→3 count は `count_keys()` 系で表示文字列を Python 事前計算（JSX で算術しない＝EP38 確定ルール）。

## 7.5 レイアウト定義・色定数（EP43/44/45 を踏襲・色のみ EP46 値・CODEX_B §7.3 と一致）

**共通レイヤースタック（下→上）:** L9 黒ソリッド → L8 静止画（scale fill→fill×1.08・drift）→ L7 グレードウォッシュ（**黒板グリーン near-black** `addSolid([0.078,0.125,0.106])`＝SLATE / MULTIPLY / opacity 30）→ L6 羽根付き楕円ビネット → L5 グロー（下中央 schoolhouse-green 一点差し ADD）→ L4 ライトスイープ（`"ADBE Rotate Z"`=18）→ L3 上ラベル（Oswald）→ L2b アクセントライン（ACCENT green・scaleX ワイプ・`motionBlur=true`）→ L2 主数値/主文字（Anton・ACCENT・`motionBlur=true`）→ L1b 下ラベル → L1 字幕ロワーサード → **L0b AI開示テキスト（`AI-assisted visualization`・Oswald 20px・SILVER `#C8CDD6`・opacity 70%・右下 `[W-32, H-28]`・全カード常時焼き＝R1）** → L0 黒シームディップ（head/tail 各4フレーム）。

**★EP46 色定数（0..1 float・schoolhouse-green レーン色。EP41 gold / EP42 blue / EP43 amber / EP44 teal / EP45 crimson を流用禁止・CODEX_B §7.3 と一致）:**
```python
ACCENT = [0.247, 0.561, 0.373]  # #3F8F5F schoolhouse-green — 数値・下線・唯一の一点差し
WHITE  = [0.961, 0.969, 0.980]  # #F5F7FA
SILVER = [0.784, 0.804, 0.839]  # #C8CDD6（開示テキスト）
INK    = [0.039, 0.039, 0.047]  # #0A0A0C 近黒ルート（サムネ bg と一致）
DESK   = [0.090, 0.075, 0.063]  # #171310 温い事務机 near-black ウォッシュ
SLATE  = [0.078, 0.125, 0.106]  # #14201B 黒板グリーン（schoolhouse ウォッシュ）
MARBLE = [0.204, 0.212, 0.231]  # #34363B 大理石（ACT3）
```
**フォント:** 数値/主文字 = **Anton Regular** / ラベル・字幕 = **Oswald Medium**。`getFontsByFamilyNameAndStyleName` で厳格解決（miss は throw・フォールバック禁止）。テキスト幅は **`sourceRectAtTime(t,false).width` で実測**（advance-width 推定禁止＝EP40 文字切れの原因・ブリーフ§5）。**`v01` の 6-3 を ACCENT green、ラベルを WHITE/SILVER。`n01` の "THE FOURTH AMENDMENT STILL APPLIES" と `p01` の "LOWERED ... NOT ELIMINATED" と `b01` の footnote 7 文言は削除禁止。**

**カウント型:** `v01` の 6→3 は `count_keys()` で桁を事前計算し settle（ease-out cubic）＋ impact SFX。**未成年の年齢・薬物の量を数値カードにしない（C5）。**

## 7.6 このマシン固有の罠（★1つ忘れると無言で品質が落ちる・EP42-45 §7.6 全項を tlo に適用）

フォント解決の例外ラップ（`psName()`・allFonts の array-LIKE ラッパーを unwrap）／spatial ease は配列次元1（`prop.isSpatial ? 1 : ...`）／OM=`"H.264 - レンダリング設定を一致 - 15 Mbps"`・RS=`"最良設定"`（英語名は try/catch フォールバック）／`app.newProject()` を headless で使わない（同名 `TLO_` コンプを防御削除）／`layer.motionBlur=true` を動くレイヤー個別に／回転は `"ADBE Rotate Z"`／改行は1行厳守（SPLIT_COMPARE の左右2値は別レイヤー・改行禁止）／em-dash は `-`／inPoint と outPoint 両方設定／`item.mainSource.conformFrameRate = 30`／実行パス `C:\Program Files\Adobe\Adobe After Effects 2026\Support Files\AfterFX.exe`／`proj.gpuAccelType = GpuAccelType.SOFTWARE`／ビルド ~100–120秒・完了マーカー `render/_build_ok.txt` をポーリング（タイムアウト≥300秒）・末尾で `app.quit()`／**aerender 前に `.aep` mtime > `.jsx` を assert**（ブリーフ§5・.aep が古いと前ビルドを焼く事故）。

## 7.7 コンポジタ（`scripts/ae/composite_tlo_hero.py`・SKIP 4条件を1つも削らない）

`BASE = tlo_final_bgm.v001.mp4` / `OUT = tlo_final_bgm.v002_ae.mp4`（v001 不変）。SKIP: (1) `render/<id>.mp4` 不在 / (2) 解像度≠1920x1080 / (3) 実測尺 `< dur-0.3` / (4) `beat.end > base_dur`。ffmpeg: `overlay=0:0:eof_action=pass:enable='between(t,start,end)'` / `-c:v libx264 -preset slow -crf 16 -pix_fmt yuv420p -colorspace bt709 -c:a copy`。**出荷済みを絶対に上書きしない。film_offset OFF=11.5 を適用する。**

---

# 8. レイヤー構成 と ゾーン分離（★主役の裏に最低4層）

## 8.1 本編カットのレイヤー構成（下→上・主役 L4 の裏に L1/L2/L3/L3b = 4層）

| L | 名前 | EP46 の値 |
|---|---|---|
| **L0** | ルート背景 | `#0A0A0C`（INK） |
| **L1** | グラデ背景 | `radial-gradient(120% 120% at 50% 40%, #171310 0%, #10120E 45%, #0A0A0C 100%)`（HOOK/ACT1 は温い事務机。ACT2 は黒板グリーン `#14201B`／ロッカーは冷灰 `#22262A`。ACT3 は大理石寄り `#34363B` にシフト） |
| **L2** | グリッド/ライン | 縦横 64px の反復線＋放射マスク＋ドリフト。`repeating-linear-gradient(0deg/90deg, #3F8F5F18 0px 1px, transparent 1px 64px)`、`translateY 0→48px` / `Easing.inOut(Easing.sin)`（等速禁止） |
| **L3** | グロー | 単一 schoolhouse-green の一点差し。`radial-gradient(closest-side, #3F8F5F66 0%, #3F8F5F18 45%, transparent 75%)`、`filter: blur(28px)`。位置は幕で移動（机の上のバッグ→トイレのドア→校門→大理石→夜明けのロッカー廊下） |
| **L3b** | 大理石の光帯/ビネット | ACT3 は列柱の光帯（`linear-gradient(100deg, transparent, #3F8F5F22, transparent)` を横に slow drift）、他幕は羽根ビネット。`translateX` を `Easing.inOut(Easing.sin)` で微動（静止フレームゼロ） |
| **L4** | 主役（still / i2v / factory） | §10 のモーション（Ken Burns/parallax/i2v） |
| **L5** | テロップゾーン（上/中央・figures） | §8.2 |
| **L6** | 字幕ゾーン（下部帯） | §8.2 |

> **主役（L4）の裏に L1/L2/L3/L3b = 4層**（グラデ背景・グリッド/ライン・グロー・光帯/ビネット）で CLAUDE.md「最低3レイヤー」＋タスク「最低4層」を満たす。**各層は §3.1b の通り常に微動（静止フレームゼロ）。**

## 8.2 ゾーン分離（一度も重ねない）

| ゾーン | 縦位置（1080基準） | スタイル |
|---|---|---|
| テロップ見出し | `y=96–260` | Oswald 64px / `#F5F7FA` / letterSpacing 4 |
| 中央テロップ / figures | `y=420–660` | §6 |
| 出典テロップ（アクセントライン） | `y=742–786` | Oswald 28px / green `#3F8F5F` 3px 下線 |
| 字幕帯 | `y=872–1010` | 白 `#FFFFFF` + `textShadow:0 0 6px #000,0 2px 4px #000` / 半透明黒帯 `rgba(6,6,8,0.62)` / ≤2行・1行≤42字 / 54px / lineHeight 1.28 |
| AI開示 | `y=1024–1052`（右下） | Oswald 20px / `#C8CDD6` / opacity 70% |

**Caption QC:** ナレ一致 ≥99%（faster-whisper 強制アライン）/ `.srt` カバー ≥95% / キュー 1.0–6.0秒 / CPS ≤17 / 単語割り禁止 / 1語孤立キュー禁止 / ズレ ≤120ms。**【DESIGNED SILENCE】2区間には字幕キューを置かない。film_offset OFF=11.5 で整列。**

---

# 9. 絵コンテ（★48シーン・象徴のみ・6制約・未成年の肖像化禁止・薬物非扇情・CODEX_A が 84本プロンプトへ展開する原図）

## 9.1 パーサ契約（★CODEX_A が `ai_prompts.v001.md` を書くときの形式・`read_prompts()` が読む2行形式）

```
- `S01.png`
<positive prompt> ... [STYLE] Avoid: <negative>
```
- **1行目:** `` - `S01.png` ``（バッククォート囲み・行末は `.png` 直後）。プロンプトを同じ行に書かない。
- **2行目:** 正プロンプト → `[STYLE]`（§5.5）→ `Avoid:` → 負プロンプト（§5.6）。
- 配置先: **`episodes/PD-2026-046-tlo/04_scenes/ai_prompts.v001.md`**。生成: `.venv/Scripts/python.exe scripts/generate_sdxl_4k.py PD-2026-046-tlo`（**variants 指定なし＝1枚**）。
- 出力: `H:\pd-media\assets\ai\tlo\S01.png …` ＋ `remotion/public/tlo/`。長辺 ≥3840 で冪等スキップ。
- **★body 84本＝84行**（still 各1枚）＋ **i2v 種 16行**（M01_src..M16_src）＝ `ai_prompts.v001.md` は計 **100 エントリ**。CODEX_A は書いた直後 `--only S01` で `shots=` が **100** に達しているか（2行形式が壊れていないか）を確認。**プロンプト実体（84本）は CODEX_A §5.9 が正典**（本節は絵コンテ級の原図）。

## 9.2 絵コンテ級ショット記述（Sid ごと・カメラ/モーション/象徴/制約。CODEX_A はこれを固有プロンプトに翻訳）

> **全ショット共通:** 顔・身体・肖像なし（R1/C5）。**T.L.O.（未成年）を人として描かない**（象徴・物・手元・影のみ）。読める文字を作らない（redacted/illegible）。判例番号・日付・校名・人名を描かない。温い事務机＋黒板グリーンの教室＋冷灰のロッカー廊下＋淡い大理石＋唯一の一点差し schoolhouse-green。**押収物（薬物）は sealed evidence を机に flat に並べた臨床描写のみ・美化/煽情ゼロ（C5）。**「生徒に権利がない/学校が何でも捜索できる」に見える絵を作らない（C1）。最高裁列柱＝Court の線／二段の階段＝二段テスト（inception→scope）／天秤＝probable cause↔reasonable suspicion／警官のバッジ＝footnote 7 の警察境界（C3）。

| Sid | カメラ/レンズ | 象徴（動き） | 制約メモ |
|---|---|---|---|
| S01 | 俯瞰寄り・接写 | 事務机の上の閉じたハンドバッグ・温い事務灯 | C5: 象徴のみ・人物なし |
| S02 | 接写・手元 | バッグを開けるジッパー（i2v: 開く） | C5: 手元のみ・顔なし |
| S03 | 正対・接写 | 洗面台の上の薄い煙（臨床・無人） | C5: 非扇情 |
| S04 | 正対・寄り | 学校のトイレのドアが閉じる（i2v: swing shut） | C5: 人物なし |
| S05 | 正対・静止 | 開いたバッグ・タバコが覗く（DESIGNED SILENCE 1.8s） | 後で S44 と対 |
| S06 | 引き・外 | 公立高校の外観・校旗（factory ambient） | — |
| S07 | 接写 | バックパックと閉じたロッカー | 二人称「あなたの bag」 |
| S08 | 寄り＋奥行き | 校門・遠景に淡い最高裁列柱 | 捜索→最高裁の距離 |
| S09 | 接写 | 洗面台の縁の2本のタバコ・薄い煙 | C5: 臨床・無人 |
| S10 | 正対 | 学校の前office カウンター（無人） | — |
| S11 | 接写・机上 | バッグの中身が一つずつ出される（手元まで） | C5: 顔なし |
| S12 | 正対・寄り | 副校長室のドアが閉じる（i2v: closingdoor） | C5: 人物なし |
| S13 | 接写 | 開いたバッグの上の1箱のタバコ | 臨床 |
| S14 | 接写 | タバコ脇の巻紙が plain view＝hinge | C5: 臨床・美化しない |
| S15 | 俯瞰・接写 | 机に並ぶ押収物: 封のマリファナ・パイプ・空袋・1ドル束・名簿・2通の手紙 | **C5: sealed/flat/muted・非扇情** |
| S16 | 接写 | 名簿カードと2通の手紙（名前判読不能） | C5/C6: 事実提示のみ |
| S17 | 接写・机上 | 証拠排除申立の書類（判読不能） | C6: purse を throw out |
| S18 | 引き | court by court へ積み上がる court 書類 | Washington へ climb |
| S19 | 引き・教室 | 机と椅子が整列した空の教室 | schoolhouse 象徴 |
| S20 | 正対・門 | 校門/校旗（i2v: 門が開く・4A が通る） | C1: 権利を捨てない |
| S21 | 接写・机上 | 校長机のネームプレート（判読不能） | in loco parentis の easy answer |
| S22 | 接写 | 令状フォームとガベル（判読不能） | police standard の easy answer |
| S23 | 引き・ロッカー | 半開きのロッカーの列 | any bag を empty の危うさ |
| S24 | 引き・教室 | 教室の机の物＋未署名の令状 | paperwork で校舎は回らない |
| S25 | 引き・廊下 | 冷灰のロッカー廊下（factory ambient） | — |
| S26 | 正対・門 | 光の差す開いた校門 | C1: 4A は校内で real |
| S27 | 正対・列柱 | 夕暮れの最高裁外観列柱（factory ambient） | 最高裁 |
| S28 | 正対・push-in | 淡い大理石の最高裁列柱・荘厳 | Court が線を引く |
| S29 | 接写 | 閉じた U.S. Reports 巻（判読不能の背） | C6: 469 U.S. 325 |
| S30 | 正対 | 静止した天秤（PC↔RS） | C2: Court が weigh した balance |
| S31 | 正対 | 天秤が PC→RS へ傾く（i2v: 傾く・緩） | C1: 引き下げ（消滅でない） |
| S32 | 接写 | 脇に退けた令状＋薄れる "probable cause"（判読不能） | C1: no warrant · no PC |
| S33 | 机上・接写 | 温い灯の開いた意見集・抽象行（判読不能） | C2: White の二段テスト |
| S34 | 正対 | 二段の階段（inception／scope・段に文字なし） | C2: 二段テスト |
| S35 | 正対 | 二段の階段を昇る光（i2v: 光が昇る・緩） | C2: inception→scope |
| S36 | 接写・机上 | 机のバッグ・各押収物が細い線で連なる | C2: each step tied |
| S37 | 接写 | 1本のタバコ vs 空にされたバッグの対比 | C2: scope は excuse を outgrow |
| S38 | 引き | 多数席から少し離れた3脚の空席 | C4: 反対（顔なし・中立） |
| S39 | 正対 | 水平に保たれた天秤 | C4: 反対意見の見方・中立 |
| S40 | 接写 | 机の上の警官のバッジ・冷光 | C3: footnote 7・顔なし |
| S41 | 正対 | school official 側と police 側を分ける線 | C3: 留保された higher standard |
| S42 | 引き | 一方に校舎・他方にパトの灯・間に線 | C3: educator 用で law enforcement 用でない |
| S43 | 正対・段 | 最高裁の大理石の段・引かれた線 | ACT3→ENDING 繋ぎ |
| S44 | 接写 | 机の上のバッグへ回帰 | 冒頭の問いへ戻る |
| S45 | 接写 | ロッカーとバックパック・ありふれた朝 | 後に来た全ての locker/backpack |
| S46 | 引き・門 | 夜明けの校門を bag が越える | C1: 4A は walk in する・人物なし |
| S47 | 正対 | RS で釣り合った天秤 | a third thing, in between |
| S48 | 引き・pull-back | ロッカー廊下・遠い鐘・開くドアと光（i2v: DESIGNED SILENCE 2.0s） | C5: 人物なし・payoff |

---

# 10. 本編カットのモーション仕様（★等速線形禁止・opacity 単独禁止・fps=30 で定数化）

## 10.1 秒→フレーム定数（★フレーム直書き禁止・全て `Math.round(fps × 秒)`）

```ts
const FPS = 30;
const f = (sec: number) => Math.round(FPS * sec);
const CUT_MEAN = f(3.196);  // ≈ 96f  平均ショット
const CUT_MIN  = f(1.0);    // = 30f  最短
const CUT_MAX  = f(6.0);    // = 180f 最長（SPEC cap）
const QUANT    = f(0.5);    // = 15f  ★カット境界の量子化単位（0.5s 刻み方針）
const FILM_OFFSET = f(11.5);// = 345f ★ナレ base の絶対開始（ティザー8.0＋BrandOpening3.5）
```
**0.5s 刻み方針:** 224カットの境界は **`QUANT`=15フレーム（0.5秒）にスナップ**して配置する。各カット長は `CUT_MIN`〜`CUT_MAX`、平均 `CUT_MEAN`。ACT3 は最も遅く（長カット寄り・6.0s 近辺を多用・荘厳）、ACT1/HOOK は速く（1.0–2.5s の断片・現在形・~2s cut）。CODEX_B は shotlist の各 span 端を 15f グリッドに丸める。

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
対象（fast move）: **S02**（ジッパー）、**S04**（トイレのドア swing）、**S12**（副校長室のドア closingdoor）、および §6 の `votetally` の count・`mechanism:gears`/`faultsplit`・幕頭 `acttitle`/`kinetic`/`kinetic:emphasis` の切れ上がり。**S05（開いたバッグ静止）・S30/S31（天秤）・S34/S35（二段の階段・走光）・S20（校門・緩）・S48（ロッカー廊下 pull-back）・Ken Burns には Trail をかけない**（無駄な残像・扇情を避ける・C5）。

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

# 11. オープニング（OP）設計 — 完全仕様（`OpeningTlo`・fps=60・CLAUDE.md §1–5 全項目）

## 11.1 秒数ベースのタイムライン（fps=60・「フレーム」は全て `Math.round(60 × 秒)`・直書き禁止・0.5s 刻み方針で全区間記述）

```ts
const FPS_OP = 60; const F = (s:number)=>Math.round(FPS_OP*s);   // 総 180f = F(3.0)
```

| 秒 | フレーム | 起きること（EP46 signature = 温い事務灯の下の机の上のハンドバッグ＋schoolhouse-green の差し） |
|---|---|---|
| 0.00–0.10 | f0–6 | 画面 `#0A0A0C`。**L1** グラデ opacity 0→1（0.40s）＋ **scale 1.08→1.00** を 180f で（`Easing.out(Easing.cubic)`）。opacity 単独でなく scale 併用 |
| 0.10–0.15 | f6–9 | **L6 ロゴ**（`hasLogo`）左上 `top:64/left:72` に spring 出現。scale 0.4→1.0・opacity 0→1（併用・`damping:14,mass:0.9`） |
| 0.15–0.25 | f9–15 | **L2** グリッドが spring（`{damping:200,mass:1,durationInFrames:F(0.8)=48}`）で reveal。最終 opacity=`gridReveal*0.18`。全体を 180f で `translateY 0→48px`（`Easing.inOut(Easing.sin)`） |
| 0.25–0.30 | f15–18 | **L3** schoolhouse-green のグローが spring（`{damping:18,mass:1.2}`）＝黒板/校門の差し。scale 0.6→1.15 / opacity 0→0.85（併用）。`filter:blur(28px)` |
| 0.30–0.86 | f18–52 | **L4 主役タイトル**が1文字ずつ切れ上がる（`overflow:hidden` マスク）。各文字 spring（`{damping:16,mass:1}`）で `translateY 110%→0`、opacity=`interpolate(sp,[0,0.25],[0,1])`。**スタッガー=`F(0.04)=2フレーム/文字**。全体を `Trail`（`layers=6,lagInFrames=1.2,trailOpacity=0.45`）で包む |
| 0.55–1.15 | f33–69 | **L2b 校門の光ライン**（EP46固有＝緑の帯がタイトル背後を横切る）。中央から `scaleX 0→1`＋`opacity 0→0.55`（spring `{damping:22,mass:1.1}`, `transformOrigin:'center'`）。green。opacity 単独禁止で scaleX 併用 |
| 0.95–1.35 | f57–81 | **L5a** green の下線が左から `scaleX 0→1`（spring `{damping:16,mass:0.8}`, `transformOrigin:'left center'`）。240×6px・`boxShadow:0 0 24px #3F8F5Faa` |
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
| L2b 校門の光 | scaleX 0→1 / opacity 0→0.55 | spring | `{damping:22,mass:1.1}`・origin center |
| L5a 下線 | scaleX 0→1 | spring | `{damping:16,mass:0.8}`・origin left |
| L5b サブ | translateY 24px→0 / opacity | spring | `{damping:20,mass:1}` |
| L6 ロゴ | scale 0.4→1.0 / opacity | spring | `{damping:14,mass:0.9}` |

> **全 opacity が translateY/scale/scaleX と対。等速線形を1箇所も使わない。**

## 11.3 レイヤー構成（下→上・主役 L4 の裏に L1/L2/L2b/L3 = 4層）

L0 `#0A0A0C` / L1 グラデ（`radial-gradient(120% 120% at 50% 35%, #171310 0%, #10120E 45%, #0A0A0C 100%)`）/ L2 グリッド（`${accent}22` 64px・放射マスク）/ L2b 校門の光（`linear-gradient(90deg, transparent, ${accent}cc, ${accent}55, ${accent}cc, transparent)`）/ L3 green グロー（`radial-gradient(closest-side, #3F8F5F88, #3F8F5F22, transparent)` `blur(28px)`）/ L4 主役タイトル（Trail 包み・`overflow:hidden` span マスク・Anton `fontWeight:800 fontSize:150 letterSpacing:-2 color:#F5F7FA`）/ L5 下線＋サブ（Oswald `fontSize:38 letterSpacing:6 uppercase color:#C8CDD6`）/ L6 ロゴ（`linear-gradient(135deg, ${accent}, #ffffff22)`・`border:2px solid ${accent}`）。

## 11.4 確認方法（CLAUDE.md §5）

```bash
cd C:\Users\aab15\Documents\prime-documentary\remotion
npm run studio     # = remotion studio。OpeningTlo を 0→180f でスクラブし §11.1 の各時刻を目視
npx remotion render OpeningTlo out/tlo_opening.mp4 --props=./props/tlo.json
# props 差し替え量産
npx remotion render OpeningTlo out/tlo_short_op.mp4 --props=./props/tlo_short.json
# 本編
npx remotion render Ep46Tlo out/tlo_final.mp4 --props=./src/data/tlo_film.json --public-dir=public_slim --concurrency=4
```

---

# 12. props 定義と型（CLAUDE.md §4）

```ts
export type OpeningTloProps = {
  title: string;      // 主役タイトル。1文字ずつスタッガーで切れ上がる
  subtitle: string;   // サブタイトル。UPPERCASE 表示（facts_lock 検査対象）
  accent: string;     // アクセント（HEX6桁・"#"込み）。グリッド/校門の光/グロー/下線/ロゴに波及
  hasLogo: boolean;   // true で左上にロゴバッジ
};
```
**EP46 の確定 props（`remotion/props/tlo.json`）:**
```json
{ "title": "THE BAG ON THE DESK", "subtitle": "NEW JERSEY V. T.L.O., 1985", "accent": "#3F8F5F", "hasLogo": true }
```
**量産用 `remotion/props/tlo_short.json`:**
```json
{ "title": "SEARCHED AT SCHOOL", "subtitle": "DO YOU HAVE RIGHTS?", "accent": "#3F8F5F", "hasLogo": false }
```
> `accent` は **`#3F8F5F` 固定**（EP41 gold / EP42 blue / EP43 amber / EP44 teal / EP45 crimson の流用は BLOCKER）。`subtitle`/`title` は `facts_lock` 検査対象（「students have no rights」「search anything」「probable cause required」を出さない。`NEW JERSEY V. T.L.O., 1985`・疑問形 `DO YOU HAVE RIGHTS?` は制度説明として可・C1）。**T.L.O. は公開記録のイニシャル＝許容（未成年の顔/実名ではない）。サムネ headlines に未成年・薬物・生数値を出さない。**

---

# 13. 受入基準（EP46 の Definition of Done・★語数ゲートが最初・全編アイボール必須）

```bash
cd C:\Users\aab15\Documents\prime-documentary
# 0. 語数（最優先・課金前）
./.venv/Scripts/python.exe scripts/check_script_length.py episodes/PD-2026-046-tlo/03_script/script.en.v001.md --json
# 1. 事実性（EP46固有・§1.3・6制約・dochighlight 0件）
./.venv/Scripts/python.exe scripts/check_tlo_facts.py --json
# 2. ビート契約（AE↔figures 非重複・ledger・6制約・dochighlight 0件）
./.venv/Scripts/python.exe scripts/validate_tlo_beats.py
# 3. 密度（★30 を Remotion 側で満たしていること・--ep 指定／--json は出力パス）
./.venv/Scripts/python.exe scripts/check_motion_density.py --ep PD-2026-046-tlo --json runs/qc/tlo_motion.json
# 4. VO速度（ナレ直後・ミックス前）
./.venv/Scripts/python.exe scripts/measure_vo_wpm.py --ep tlo --json
# 5. 最終受入
./.venv/Scripts/python.exe scripts/check_final_acceptance.py 46 --render episodes/PD-2026-046-tlo/08_edit/tlo_final_bgm.v002_ae.mp4 --emit-receipt
```
> **ゲート入力は `--ep PD-2026-046-tlo`。`--json <film.json>` を入力に使わない**（出力パス＝上書き事故。ブリーフ§5）。

| ゲート | 閾値 | EP46 設計値 |
|---|---|---|
| `check_script_length` | band 内 | 2,125語（SPEC・要 PASS 確認・cap 2,141） |
| `runtime_band` | 690–750s | **736.4s = 12:16.4**（上限 750s に 13.6s 余裕） |
| `motion_density` | ≥2.5/min ∧ cov ≥0.25 ∧ variety ≥3 | **3.02/min / 0.272 / 8種**（film.json 36 beats・AE非依存・floor 30 に +6） |
| `animation_mix`（紙芝居） | still-share ≤45% ∧ motion cov ≥45% | **44.64% / 55.36%** |
| `check_asset_reuse` | first-use ≥0.70・still≤2・factory1・motion≤2 | **0.8571 / 2 / 1 / 2** |
| `footage_diversity` | distinct/total ≥0.40 | **0.8571** |
| `visual_asset_qc` | 全 factory 目視 reviewed | **92本 目視（CODEX_A）** |
| `image_resolution` | 長辺≥3840 | 全 SDXL ≥3840 |
| `bgm_present` | 無音>25秒ゼロ | 最長 2.0秒 |
| `caption_integrity` | 一致≥99%・カバー≥95% | §8.2（film_offset OFF=11.5） |
| `op_ed_bookends` | `BrandOpening`/`BrandEndcard` import・不変 | ✓ |
| `asset_manifest` | A↔B counts/role 一字一致・also_thumb 6（S01/S07/S26/S46/S64/S82）・overlay 12・schema `tlo_assets.v1`・factory/motion 全エントリ | §5.8 |
| `facts_lock`（EP46固有・6制約） | violations=0・**dochighlight 0**・White 逐語帰属・過大化ゼロ | §1.2/§1.3 |
| `duration` | `caseFilmDurationInFrames(tloFilm,30)`=22092・hookSeconds=8.0 | §0.1/§3.1 |
| **全編アイボール** | 12:16.4 を通しで目視 | ★1フレーム判定禁止（EP39-41/EP3941 の miss） |

---

# 14. premortem（失敗するとしたらここ）

| # | 失敗モード | 事前対処 |
|---|---|---|
| 1 | **番号ズレ**（別番号を発明） | シーンは S01..S48 固定（§3.2）。still 資産 ID は S01..S84（別空間・cross-map 禁止） |
| 2 | **紙芝居**（still-share 45%超・余裕 0.36%pt） | §5.1 で still-cut 100 固定・factory 92・i2v 32。still1つ増で 45% 割れ → cut を増やさず同一シーンの新規 distinct で回復 |
| 3 | **バリエーション水増し**（`--variants 3`） | §5.3。variants 指定なし＝1枚。ai_prompts は 84行＝84枚 |
| 4 | **密度 FAIL**（AEカードに頼る） | §6。film.json に 36 beats（30 超）。AE 7枠は composite 後で非カウント |
| 5 | **画像プロンプトが読めない**（0枚生成） | §9.1 の2行形式・`--only S01` で `shots=100`（body 84 + i2v種 16）確認 |
| 6 | **ファイル名信仰**（牛が本編に入る） | §5.4 factory 92本を `build_footage_contact_sheet.py` で全点目視（CODEX_A BLOCKING） |
| 7 | **6制約違反**（無権利断定/probable-cause 誤り/警察一般化/別票数/未成年肖像/薬物扇情/校名人名/台帳外数値） | §1.2/§1.3 `check_tlo_facts.py`。カード・figures・字幕・プロンプト全対象 |
| 8 | **dochighlight のバグ見え**（3回指摘） | §6.2/§7.3。`dochighlight`/`comparebars` を1件も置かない（R-DOCHL・grep 0） |
| 9 | **FigureBeats kind 大文字で無音描画 / 非実在 mechanism subtype** | §6.2 kind は全小文字。mechanism subtype は **closingdoor/gears/faultsplit の3種のみ**（scales/twostep は非実在→still/i2v/AEで表現） |
| 10 | **quote が要約・帰属ズレ**（EP43 R-PAYTON 事故） | §2.1 `APPROVED_QUOTES` の3本のみ逐語・帰属は全て "Justice White, for the Court"（R-QUOTE） |
| 11 | **AE em-dash 豆腐 / 等速 / OM名英語 / 文字切れ** | §7.6。テキスト幅は `sourceRectAtTime(t,false).width` 実測 |
| 12 | **id 誤り / hookSeconds を 0 に**（duration 崩れ） | §0.1。`id="Ep46Tlo"`・`hookSeconds=8.0`・`caseFilmDurationInFrames(tloFilm,30)`=22092 |
| 13 | **accent 流用**（他話色を残す） | §0.5/§7.5/§12。OP props/AEカード/サムネ accent は `#3F8F5F` |
| 14 | **A↔B マニフェスト不整合**（role=thumb を作る/counts 不一致/factory・motion 空欠落/schema 名違い） | §5.8。`tlo_assets.v1`・role enum=`body/i2v_source/reject`・also_thumb 6・overlay 12・**factory92/motion16 全エントリ**を A/B 一字一致 |
| 15 | **EP39〜45 と素材被り** | §2 で7つの stock_ledger の sha256 を除外（`select_tlo_factory.py --verify-no-prior-overlap`） |
| 16 | **film_offset 不整合**（BGM/AE/字幕がズレる） | §3.1/§4.3/§7.7。OFF=11.5（ティザー8.0＋BrandOpening3.5）を BGM/composite/caption に一貫適用 |
| 17 | **public_slim 未staging→render 不能**（EP45 事故） | レンダ前に public→public_slim へ全メディア（img/factory/motion/audio）をコピー staging（§15） |
| 18 | **fast端で 11分台 / 750s 超** | §4.1 speed 1.0 明示＋`measure_vo_wpm` 168–190・190超は破棄再発注。総尺 736.4s ≤750 の assert（§3.1[4]） |

---

# 15. 設計パッケージ接続（DESIGN → CODEX_A / CODEX_B）

- **DESIGN（本書）:** タイムライン（0〜715.9s 全区間・各Act・§3.1/§3.1b）・レイヤー（背面4層・§8）・モーション数値（§10）・48絵コンテ（§3.2/§9・象徴・6制約・未成年肖像化なし・薬物非扇情）・FigureBeats 設計（≥30＝36・小文字kind・変種≥3＝8種・dochighlight 0件・§6）・AEカード表（7枚・accent #3F8F5F・§7.3）・OP 仕様（§11）・asset_manifest スキーマの正（§5.8）・Composition（1920x1080/fps30/id=Ep46Tlo/hookSeconds8.0/durationInFrames 22092）。
- **CODEX_A（別ファイル `EP46_tlo_CODEX_A_ASSETS.v001.md`）:** §9 を **84本の固有プロンプト**（1シーン1枚・variants 0・**省略禁止で全84本**）＋ i2v 16 ＋ factory 92 選定＆**全点目視QC**（`select_tlo_factory.py`・`--exclude-used --ep PD-2026-046-tlo` で EP39〜45 sha256 除外）＋境界契約 `asset_manifest.v001.json`（schema `tlo_assets.v1`・counts を EP46 値 still_body84/still_i2v_source16/motion16/factory92/overlay12・`stills[].role` enum=`body/i2v_source/reject`・**stills84＋factory92＋motion16＋overlay12 を全エントリ記載**・also_thumb 6（S01/S07/S26/S46/S64/S82））。
- **CODEX_B（別ファイル `EP46_tlo_CODEX_B_BUILD.v001.md`）:** `build_tlo_film.py`（＝`build_cleveland_film.py` を複製・ASSET_MAP/NARR/FACTORY_SEL/SLUG/EP を tlo に・**実素材のみ stub 禁止**・manifest の factory/motion 全読込・grep で stub/placeholder/dryrun=0）／captions（実測 narration・+offset 11.5）／figures 36（小文字 kind・dochighlight 0件・§6）／`CaseFilm` を `id="Ep46Tlo"` で Root.tsx 登録（`caseFilmDurationInFrames`＝22092・hookSeconds=8.0）／`OpeningTlo`／AEビルダ・コンポジタ（accent #3F8F5F・.aep>.jsx assert・レイアウト名は実装済み8種のみ・§7.3 の7カード＝本書 §7.3 と一字一致・White 逐語 q01）・`validate_tlo_beats.py`・`check_tlo_facts.py`（EP45 版を複製・同名・R-OVERCLAIM/R-STANDARD/R-POLICE/R-VOTE/R-QUOTE/R-MINOR/R-DOCHL）／`build_tlo_bgm_real.py`→`composite_tlo_hero.py`（film_offset OFF=11.5 適用）／**public→public_slim staging**／レンダ（`--public-dir=public_slim --concurrency=4`）／全ゲート（`--ep PD-2026-046-tlo`）／完成後の**全編アイボール**。
- **A↔B 接続点は `asset_manifest.v001.json` ただ1ファイル**（schema `tlo_assets.v1`・counts/role enum を A/B 一字一致・§5.8）。
- **複製元（実在・EP43/45）→ tlo 複製先:** `build_cleveland_film.py`→`build_tlo_film.py` / `build_*_bgm_real.py`(EP43)→`build_tlo_bgm_real.py` / `ae/build_cleveland_hero_cards.py`→`ae/build_tlo_hero_cards.py` / `ae/composite_cleveland_hero.py`→`ae/composite_tlo_hero.py`（film_offset OFF=11.5）/ `validate_cleveland_beats.py`→`validate_tlo_beats.py` / `check_cleveland_facts.py`→`check_tlo_facts.py`。**共有（複製不要）:** `generate_sdxl_4k.py` / `build_footage_contact_sheet.py` / `check_motion_density.py` / `measure_vo_wpm.py` / `check_script_length.py` / `check_final_acceptance.py`。**実在しないスクリプトを捏造しない（`ls scripts/` で複製元の実在を確認）。**
