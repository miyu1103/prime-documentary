# EP42 young — Codex スレッドB「実装」引き継ぎプロンプト v001

> **このファイルは単体で完結している。他のファイルを読まなくても着手できる。**
> 並行して走っているスレッドA（素材生成）のファイル `EP42_young_CODEX_A_*.md` は**読まない**。
> 設計書 `EP42_young_DESIGN*.md` も**読まない**（必要な数値はすべて本書に転記済み）。
> `EP42_young_PRODUCTION_SPEC.v001.json` の数値は本書に転記済み。**あなたはこれを書き換えない。**

```
あなたは Prime Documentary（YouTubeドキュメンタリーチャンネル）の制作エンジニアです。
リポジトリ: C:\Users\aab15\Documents\prime-documentary
Python:     C:\Users\aab15\Documents\prime-documentary\.venv\Scripts\python.exe
メディア:   H:\pd-media
担当:       EP42 / Episode ID: PD-2026-042-young / slug: young
```

**題材:** *Hudson v. Michigan*, 547 U.S. 586 (2006)。合衆国最高裁が5対4で、knock-and-announce 違反があっても
証拠排除（exclusionary rule）は要求されないと判示した実在の最高裁判決（**制度説明としてのみ**扱う）。
主題人物は **Anjanette Young**（シカゴのソーシャルワーカー・**存命の私人 = R2**）。2019年、住所取り違えで
彼女宅に有効な捜索令状が執行され、約12名の警官が踏み込み、着替え中の彼女が手錠を掛けられた。市は290万ドルの
和解に同意したが、**どの裁判所も誰の責任も認定していない。** Booker T. Hudson 本人は**主役化しない**
（存命・薬物有罪の私人 = **R3・制約5**。人物化せず Detroit の戸口/敷居の象徴のみ）。

> **★EP41 Thompson との決定的な違い:** EP41 は「隠された報告書＋最高裁が5-4で賠償を覆した」だった。
> **EP42 は「誤住所の踏み込み（Young）＋ Hudson が救済を薄くした射程」を二つの戸口として接続する。**
> `Supreme Court` は禁止語ではない（Hudson は実在の本案判決）。だが **§2 の正確性6制約が全出力を律する。**
> **`no-knock` / `unconstitutional` / `she changed the law` を一切書かない（プロンプト・カード・図表・タイトル・字幕・props すべて）。**
> **和解は責任認定ではない**（$2.9M・48-0 は「reported」枠＋「no finding of fault」でのみ提示）。

---

# 0. このスレッドの責務・境界・完了条件

## 0.1 このスレッド（B）の責務 — **コード律速。素材を1点も待たずに全部書ける。**

| # | 作業 | 成果物 |
|---|---|---|
| B-1 | エピソードディレクトリと `manifest.json` | `episodes/PD-2026-042-young/**` |
| B-2 | 境界契約マニフェストの**消費側**バリデータ＋スタブ素材生成 | `scripts/check_young_asset_manifest.py` / `scripts/make_young_stub_assets.py` |
| B-3 | スタブ narration_index 生成器（TTS 不要で通しを回す鍵） | `scripts/make_young_stub_narration.py` |
| B-4 | 事実台帳 F-ID と 6制約ゲート（**EP42固有・BLOCKING**） | `scripts/check_young_facts.py` |
| B-5 | `young_film.json` ビルダ（**asset_map→manifest変換＋beatsheet生成／footage混在**） | `scripts/build_young_film.py`（**`build_thompson_film.py` を複製**） |
| B-6 | beats バリデータ（AEとRemotionの区間衝突検査＋ledger／6制約） | `scripts/validate_young_beats.py` |
| B-7 | **構文境界で切る字幕生成器** | `scripts/gen_captions_young.py`（**`gen_captions_thompson.py` を複製**） |
| B-8 | **After Effects カード**のビルダとコンポジタ | `scripts/ae/build_young_hero_cards.py` / `scripts/ae/composite_young_hero.py`（**`*_thompson_*` を複製**） |
| B-9 | 本編 BGM ミックス（AEカード合成の基底 mp4 を生成） | `scripts/build_young_bgm.py`（**`build_thompson_bgm.py` を複製**） |
| B-10 | Remotion 本編コンポジション登録 `Ep42Young` | `remotion/src/Root.tsx` |
| B-11 | OP バンパー `OpeningYoung`（fps60/1920x1080/180f） | `remotion/src/compositions/OpeningYoung.tsx` |
| B-12 | サムネ3案 | `remotion/src/compositions/YoungThumbnails.tsx` |
| B-13 | **スタブでの通しドライラン** | `episodes/PD-2026-042-young/08_edit/_dryrun/**` |

## 0.2 もう一方のスレッド（A）との境界 — **接続点はただ1ファイル。**

```
episodes/PD-2026-042-young/05_visuals/asset_manifest.v001.json
   ↑ Aが生成（唯一の生産者）        ↓ Bが消費（唯一の消費者）
```

**Bはこのファイル以外のAの中間生成物を読まない。そして Bはこのファイルが無くても完走できる。**
`make_young_stub_assets.py` が**まったく同じスキーマの** `asset_manifest.stub.v001.json` を作るので、
Bはそれで全パイプラインを通す。

> **★絶対条件: スタブと本番でコードパスを分岐させてはならない。**
> `build_young_film.py --assets <path>` は渡されたマニフェストを読むだけで、`is_stub` の値によって
> **処理を変えない**（`is_stub` はログと受入判定にだけ使う。カット組み立てロジックには一切使わない）。

> **★1シーン1枚・バリエーション0（ブリーフ§1）の B 側での意味:** A は同一ショットの `_01/_02/_03` を**作らない**。
> したがってマニフェストの `stills[]` は **85本すべてが固有プロンプトの distinct**（`counts.still_body>=85`）。
> B は編集上、still を **各最大2回**まで再使用してカット101本を組む（cap 2 の"再利用"であって"バリエーション"ではない）。
> **B は `--variants` という語をどのコマンド・ログにも書かない**（それは A の SDXL 側の概念で、しかも 1 固定）。

### 0.2.1 ファイル所有権（これを破ると並行作業が壊れる）

| パス | 所有 | Bの権限 |
|---|---|---|
| `episodes/PD-2026-042-young/manifest.json` | **B** | 読み書き |
| `episodes/PD-2026-042-young/{00_topic,01_research,03_script,04_scenes,06_audio,08_edit,09_package,approvals,events}/**` | **B** | 読み書き |
| `remotion/src/**` `remotion/props/**` | **B** | 読み書き |
| `remotion/public/young_dryrun/**` | **B** | 読み書き（スタブ素材の staging 先） |
| `scripts/*young*.py` / `scripts/ae/*young*.py`（§0.3） | **B** | 新規作成 |
| **`episodes/PD-2026-042-young/05_visuals/**` `05_stock/**`** | **A** | **読み取りのみ。書くな** |
| **`H:\pd-media\assets\ai\young\**` / `ai_video\young\**`** | **A** | **読み取りのみ。書くな** |
| **`remotion/public/young/{img,factory,motion,overlay}/**`** | **A** | **読み取りのみ。書くな** |
| `EP42_young_DESIGN*.md` / `EP42_young_CODEX_A_*.md` | **設計/Aスレッド** | **触るな** |
| `EP42_young_PRODUCTION_SPEC.v001.json` / `EP42_young_script.en.v001.md` | **上流** | **読み取りのみ。書くな** |
| `episodes/PD-2026-039-*/**` … `PD-2026-041-*/**` / それらの素材 | **他エージェント** | **絶対に触るな** |

> **B は `remotion/public/young/` に書かない。** スタブは **`remotion/public/young_dryrun/`** に置く。
> 本番マニフェストが来たら `--assets` を差し替えるだけで `young/` を参照するようになる。

## 0.3 B が新規作成するスクリプト（これ以外を新規に作らない。既存を改変しない）

| パス | 役割 | 手本（**改変せず読んで複製→パス/定数だけ差し替え**） |
|---|---|---|
| `scripts/check_young_asset_manifest.py` | §3.3 消費側バリデータ | `scripts/check_thompson_asset_manifest.py` |
| `scripts/make_young_stub_assets.py` | §3.4 スタブ素材＋スタブマニフェスト＋スタブ黒ベース | `scripts/make_thompson_stub_assets.py` |
| `scripts/make_young_stub_narration.py` | §4.4 スタブ narration_index | `scripts/make_thompson_stub_narration.py` |
| `scripts/check_young_facts.py` | §2 6制約＋台帳（BLOCKING） | `scripts/check_thompson_facts.py` |
| `scripts/build_young_film.py` | §5 film.json＋manifest＋beatsheet＋SRT | **`scripts/build_thompson_film.py`** |
| `scripts/validate_young_beats.py` | §7.9 不変条件 | `scripts/validate_thompson_beats.py` |
| `scripts/gen_captions_young.py` | §8 構文境界字幕生成器 | **`scripts/gen_captions_thompson.py`** |
| `scripts/ae/build_young_hero_cards.py` | §7 AEカードビルダ | **`scripts/ae/build_thompson_hero_cards.py`** |
| `scripts/ae/composite_young_hero.py` | §7.10 コンポジタ | **`scripts/ae/composite_thompson_hero.py`** |
| `scripts/build_young_bgm.py` | §7.10 基底 mp4（narration＋BGM ミックス） | `scripts/build_thompson_bgm.py` |

> **`build_young_film.py` の複製時に差し替える定数:** `ASSET_MAP`（マニフェスト→cut 変換テーブル）・`NARR`（narration_index 既定パス）・
> `FACTORY_SEL`（factory 選抜の参照）・`SLUG="young"`・`EP="PD-2026-042-young"`・出力パス群。**ロジック（best-pick / tile_window /
> allocate / build_figures / build_captions）は1行も変えない。**
> **既存の `scripts/gen_captions_case.py` / `build_thompson_film.py` 等は触らない**（他エピソードが使用中）。EP42用に**新規コピー**する。

## 0.4 完了条件（スタブだけで、全て緑になったら「実装完了」）

```bash
cd C:\Users\aab15\Documents\prime-documentary
PY=./.venv/Scripts/python.exe

# [B-DONE-1] スタブ素材・スタブ黒ベース・スタブ narration を揃える
$PY scripts/make_young_stub_assets.py
$PY scripts/make_young_stub_narration.py

# [B-DONE-2] マニフェスト消費側バリデータ（スタブ相手に通ること）
$PY scripts/check_young_asset_manifest.py \
  --assets episodes/PD-2026-042-young/05_visuals/asset_manifest.stub.v001.json

# [B-DONE-3] 字幕（スタブ narration の実文から構文境界で生成）
$PY scripts/gen_captions_young.py \
  --narr episodes/PD-2026-042-young/06_audio/narration_index.stub.v001.json
$PY scripts/check_caption_breaks.py \
  episodes/PD-2026-042-young/08_edit/captions.final.v001.srt

# [B-DONE-4] film.json をスタブから組み立てる（footage 混在必須）
$PY scripts/build_young_film.py \
  --assets episodes/PD-2026-042-young/05_visuals/asset_manifest.stub.v001.json \
  --narr   episodes/PD-2026-042-young/06_audio/narration_index.stub.v001.json \
  --out    remotion/src/data/young_film.json

# [B-DONE-5] ★5ゲート全部（--ep 指定・animation_mix を絶対に忘れるな）
$PY scripts/check_asset_reuse.py     remotion/src/data/young_film.json
$PY scripts/check_motion_density.py  --ep PD-2026-042-young
$PY scripts/check_animation_mix.py   --ep PD-2026-042-young
$PY scripts/check_caption_breaks.py  episodes/PD-2026-042-young/08_edit/captions.final.v001.srt
$PY scripts/check_script_length.py   episodes/_planning/EP42_young_script.en.v001.md --json

# [B-DONE-6] 事実性/6制約（スタブの文字列にも適用）
$PY scripts/check_young_facts.py --json --dryrun

# [B-DONE-7] beats 契約（AE区間 と Remotion figures[] が1秒も重ならない）
$PY scripts/validate_young_beats.py --dryrun

# [B-DONE-8] AE カードをビルド＋レンダ＋コンポジット（ドライラン出力へ）
$PY scripts/ae/build_young_hero_cards.py --dryrun
"C:/Program Files/Adobe/Adobe After Effects 2026/Support Files/AfterFX.exe" -noui \
  -r "C:/Users/aab15/Documents/prime-documentary/episodes/PD-2026-042-young/08_edit/_dryrun/ae_hero/young_hero.jsx"
$PY scripts/ae/composite_young_hero.py --dryrun

# [B-DONE-9] Remotion Studio で目視
cd remotion && npm run studio
#   → Ep42Young / OpeningYoung / Thumb-young-01..03 が出て、実際に動くこと
```

**台本は既に確定済み**（`EP42_young_script.en.v001.md`）。したがって本番 narration_index が来たら
`--narr` を差し替え、[B-DONE-3]〜[B-DONE-8] を全部やり直す。**「スタブで通ったから本番も通るはず」は禁止。**

---

# 1. 実装前に必ず読むファイル（**推測で書くな**）

| パス | なぜ読むか |
|---|---|
| `scripts/build_thompson_film.py` | **複製元。** best-pick / tile_window / allocate / build_figures / build_captions をそのまま踏襲し、定数だけ young に。**EP41 と同じく footage を必ず混ぜる（§0.5 の紙芝居回避）** |
| `scripts/ae/build_thompson_hero_cards.py` | **複製元。** `money_keys()`（Python で表示文字列を全事前計算）/ `fit_size()` / CARDS デッキ構造 / レイアウト定義 / 完了マーカーをそのまま |
| `scripts/ae/composite_thompson_hero.py` | **複製元。** SKIP4条件（missing / 解像度不一致 / 実測尺不足 / window past end）と ffmpeg フィルタグラフ（overlay/blend）をそのまま |
| `scripts/gen_captions_thompson.py` | **複製元。** `internal_split()` / `chunk_sentence()` / `NO_DANGLE_END` import をそのまま |
| `scripts/build_thompson_bgm.py` | **複製元。** narration＋BGM ミックスで基底 mp4 を作る経路 |
| `remotion/src/compositions/CaseFilm.tsx` | `FilmData` 型 / `caseFilmDurationInFrames` / `depthSrcOf()` |
| `remotion/src/components/FigureBeats.tsx` | `FigureSpec` の**実在する `kind` 文字列**（§6.2 の警告を必ず読め・**全小文字**） |
| `remotion/src/components/Bookends.tsx` | `OPENING_SEC` / `ENDCARD_SEC` / `BrandOpening` / `BrandEndcard` |
| `scripts/check_asset_reuse.py` / `scripts/check_motion_density.py` / `scripts/check_animation_mix.py` / `scripts/check_caption_breaks.py` / `scripts/check_script_length.py` | 通すべき5ゲートの**実際の判定ロジック**（§9） |
| `C:\Users\aab15\Documents\pino-channel\remotion\src\Opening.tsx` | §10 の OP 正典実装 |

---

# 0.5 ★★★ EP39/40/41 で踏んだ失敗＝最初から防ぐ（本書の全体設計はこの6点を構造で潰している）★★★

1. **紙芝居（最重要）** — 静止画100%で組むと `check_animation_mix` が FAIL する。**EP42 は最初から footage を混ぜる。**
   `check_animation_mix.compute_metrics_from_film()` は film.json の `cuts[]` を
   **`kind=="img"` → still（scene 扱い）/ それ以外 → footage（motion 扱い）** と分類する。
   → §5 の cuts 構成は **factory 93 + motion 32 の footage を最初から入れて still-share を frame ベースで ≤0.42、cut数ベースで 0.4469** にする。
2. **AEカードは密度に数えられない** — `check_motion_density` は film.json の `graphics+figures+heroCuts` **のみ**数える。
   AEカードは ffmpeg で後合成するので**1本も数えられない**。→ §6 で **film.json 側の `figures[]` を 37本**（spec floor 31 に **+6**・`graphics[]=[]`）置く。AEカードは別勘定。
3. **FigureSpec の `kind` は実在の小文字値のみ** — 大文字名（`ActTitle`/`QuoteCard`/`VoteTally` 等）は無言で描画が消える（§6.2）。
4. **台帳に無い数値を焼くな** — EP40 の生 Codex-B 出力に架空の $580,000 が入って**不採用になった実害**。
   → §2 の事実台帳 F-ID に**検証済み値だけ**を置き、`check_young_facts.py` が film.json/AE/サムネ/props の全数値を台帳照合する。台帳に無い数値・`verified:false` の数値を焼いたら FAIL。
5. **字幕は台本本文と対応** — EP38 で台詞混入・「final」誤称の実害。→ §8 の字幕は **narration_index の実チャンク文をそのまま** verbatim で使う（自作しない）。
6. **レンダー前ゲート** — build 後に `check_asset_reuse` / `check_motion_density` / `check_animation_mix` / `check_caption_breaks` / `check_script_length` を**全部**通す（§9・§13）。**animation_mix を忘れるな。**

---

# 2. ★ EP42固有の正確性6制約・事実性ロック（`scripts/check_young_facts.py`・BLOCKING）

> **この節に違反した成果物は、他が全て完璧でも出荷不可。** 検査対象は film.json の figures/captions、AE beats、
> サムネ、props、固定コメント、（存在すれば）マニフェストの tags/caption_hint/qc.notes の**全文字列と全数値**。

## 2.1 正確性6制約（全出力に適用・違反は BLOCKER）

| # | 制約 | 許可される表現 | 禁止 |
|---|---|---|---|
| C-1 | **和解 ≠ 責任認定** | 「市が290万ドル支払いに同意」「市議会が承認（**reported as 48-0**）」「**no finding of fault**」「No court found …」 | 「裁判所が違憲/責任を認定」「the court ruled the city liable」 |
| C-2 | **令状は有効な search warrant のみ** | 「search warrant（有効・判事署名）」 | **`no-knock`** をカード/プロンプト/字幕/props に一切出さない |
| C-3 | **改革は否決・現行も合法** | 「voted it down, ten to four」「**still legal**」「never reached the floor」 | 「法が変わった」「**she changed the law**」 |
| C-4 | **Hudson の射程を圧縮しない** | 「knock-and-announce は今も **a command** of the Fourth Amendment」「否定されたのは救済としての証拠排除のみ」「Scalia の民事訴訟論拠は **Part IV = 4票のみ**・**Kennedy は署名せず**」 | knock-and-announce 自体が廃止された、と読める記述 |
| C-5 | **Booker Hudson を主役化しない** | 制度説明としての名（"a man named Booker Hudson"）／ ACT4 "a convicted man" のみ。ビジュアルは Detroit の戸口/敷居の象徴 | 人物化・肖像・薬物/人生/心情/その後・顔 |
| C-6 | **Young は非グラフィック象徴のみ** | 開いたドア・散らばった書類・手錠・時計・足首モニタ・空席のアイコン | 顔・身体・肖像・着衣なし描写 |
| R1 | **実在人物の顔・肖像を生成しない** | 全生成ビジュアル表示中は `AI-assisted visualization`（右下）／概要欄1行AI開示 | 認識可能な人物・読める偽公文書 |

**★禁止語（`check_young_facts.py` が全文字列を case-insensitive 部分一致で検査。1件でも FAIL）:**
`no-knock` / `no knock` / `unconstitutional` / `she changed the law` / `changed the law`。

## 2.2 事実台帳 F-ID（`03_script/young_facts.v001.json`・**Bが台本の事実対応表から転記して作る**）

**スキーマ版:** `young_facts.v1`。各 F-ID は `{"value":..., "unit":..., "verified":bool, "claim_id":"", "quote":""}`。
**台本の事実対応表（claim id）に裏付けのある値だけ `verified:true`。裏付け無しは `verified:false`。**

| F-ID | 内容 | 使う場所 | claim |
|---|---|---|---|
| F01 | 踏み込み日 = **2019-02-21** | fig timeline / AE date | C10 |
| F02 | 警官数 ≈ **12**（"about twelve"） | fig stat / AE stat | C13 |
| F03 | 和解額 = **$2,900,000**（サブ必須「no finding of fault」） | fig stat / AE MONEY | C19 |
| F04 | 市議会承認日 = **2021-12-15** | fig timeline / AE date | C19 |
| F05 | 市議会票（**reported**）= **48 – 0** | fig / AE（reported枠・C-1） | C19 |
| F06 | CBS映像放映 = **December 2020** | fig timeline | C17 |
| F07 | COPA調査期間 ≈ **16 months** | fig numberticker | C18 |
| F08 | COPA違反疑い ≈ **100 alleged**（"alleged" 必須） | fig numberticker | C18 |
| F09 | 関与警官 = **more than a dozen（12+）** | fig stat | C18 |
| F10 | Wolinski 解雇年 = **2023** | fig timeline / AE | C21 |
| F11 | Police Board 票（Wolinski）= **5 – 3** | fig stat | C21 |
| F12 | Anjanette Young Ordinance 委員会票 = **10 – 4（voted down）** | fig numberticker / AE | C22 |
| F13 | Ordinance 否決時期 = **November 2022** | fig timeline | C22 |
| F14 | 判例引用 = **Hudson v. Michigan, 547 U.S. 586 (2006)** | fig lowerthird | C01 |
| F15 | 判決 = **June 2006 / 5 – 4** | fig votetally / AE VOTE | C01 |
| F16 | Hudson 進入待機 = **3 – 5 seconds** | fig numberticker / AE | C07 |
| F17 | Hudson 進入 = **August 1998** | fig timeline | C07 |
| F18 | Scalia の民事訴訟論拠（Part IV）= **4票のみ**・Kennedy 不参加 | fig stat（C-4） | C25 |
| F19 | 残る救済 = **section 1983**（民事） | fig lowerthird / AE | C05 |

> **F05（48-0）と F03（$2.9M）は "reported"／"no finding of fault" のサブラベルと**同一カード内**で提示する
> （C-1）。単独の勝利数として焼かない。** `check_young_facts` の R-SETTLEMENT が照合（§2.3）。

## 2.3 `check_young_facts.py` の検査（exit 0=PASS / 1=FAIL / 2=スキーマ不一致）

**検査対象ファイル（この一覧をハードコード。存在するものだけ検査し、無いものは `skipped[]` に必ず明記）:**

```
episodes/PD-2026-042-young/03_script/young_facts.v*.json
episodes/PD-2026-042-young/08_edit/ae_hero/beats.json
episodes/PD-2026-042-young/08_edit/_dryrun/ae_hero/beats.json
episodes/PD-2026-042-young/09_package/*.json        （title / description / thumbnail headlines）
episodes/PD-2026-042-young/09_package/*.txt         （固定コメント）
episodes/PD-2026-042-young/05_visuals/asset_manifest*.json  （tags / caption_hint / qc.notes）
remotion/src/data/young_film.json                   （figures[] / captions[] の全文字列と数値）
remotion/props/young*.json                          （title / subtitle）
```

- **R-FORBID（最優先）** — §2.1 の禁止語（`no-knock`/`no knock`/`unconstitutional`/`she changed the law`/`changed the law`）が
  対象文字列のどこかに出たら即 FAIL。
- **R-LEDGER** — figures[] の `value`/`numKeys` 到達値、AE `beats[].value`/`beats[].hero`、サムネ数字に現れる**あらゆる数値**は、
  `young_facts.v*.json` に `verified:true` で存在する値に**完全一致**しなければ FAIL（$580,000 実害の再発防止）。
- **R-SPLIT** — 裁判所票の `votetally` は **`majority:5, dissent:4`（Hudson）のみ**許可。48-0/10-4/5-3 は立法・委員会・委員会票なので
  `votetally` に入れない（`stat`/`numberticker`/`compbars` で表現し、`label` に主体を明記）。
- **R-SETTLEMENT（C-1）** — `$2.9M`/`2,900,000`/`48-0`/`48 – 0` を含むカード・figure は、同一 payload 内に許可修飾
  `{"reported","no finding of fault","no court found","a settlement, not a finding"}` のいずれかを**必ず含む**こと。
  かつ責任認定語（`liable`/`found the city ...`/`violated her rights`）と同一 payload で共起したら FAIL。
- **R-ATTRIB（C-4）** — `quote[].attribution` が非空。許可対応表（DESIGN §7.2 の quote 3本＋§6 lowerthird と一致。逐語は syllabus/opinion 原文で照合）:
  ```python
  APPROVED_QUOTES = {
    "still a command":            "Justice Scalia, for the majority",         # C04（多数意見）
    "exclusionary rule":          "Justice Kennedy, concurring in the judgment", # C04（第5票・Part IV に署名せず「排除法則は疑いない」）
    "not in doubt":               "Justice Kennedy, concurring in the judgment",
    "section 1983":               "Majority opinion",                          # C05
    "the value of deterrence":    "Justice Breyer, dissenting",                # C04（反対意見・逐語）
  }
  ```
  > Kennedy/Breyer の逐語を焼いても R-ATTRIB を通す（DESIGN §7.2 の quote×3 と整合）。要約を引用符に入れない。
- **R-C4（C-4 射程非圧縮の**積極**検証・BLOCKING）** — C-4 の核となる文言が対象出力に**存在すること**を assert する
  （否定検出だけでなく肯定検出）。次を全て満たさなければ FAIL:
  (1) `still a command` が figures/AE いずれかに存在し、Scalia 帰属である。
  (2) Part IV=4票 / Kennedy 不参加を示す文言（`Part IV`＋`4` かつ `Kennedy did not join`／`Kennedy, concurring` 等）が
      figures（F18 stat）に存在する。
  (3) `knock-and-announce` の近傍60字に `still a command` 系があり、かつ否定文脈（`abolished`/`struck down`/`no longer`）でない。
  （DESIGN §1.3 の L-C4 をここに一本化・同名 `R-C4` で両ドキュメントから参照する。）
- **R-HUDSON（C-5）** — 対象文字列で `Booker`/`Hudson`（人名文脈）と人物化語（`drug`/`convicted felon` を超える属性・心情語・
  肖像指示）の同一文共起を FAIL。制度説明語（"a man named Booker Hudson" / ACT4 "a convicted man"）は許可。
- **R-YOUNG（C-6）／R-FACE／R-DOC（R1）** — `has_readable_text`/`has_identifiable_face` が true の項目、
  読める偽公文書の主張語（`legible`/`actual court filing`/`real report` を肯定文脈で）、Young の身体・顔・着衣なし描写語を FAIL。
  象徴オブジェ語（open door/scattered papers/handcuffs/clock/ankle monitor/empty seats）は許可。
- **R-DATE** — F01/F04/F06/F10/F13/F17 の日付が別カードで取り違えられていないこと。

**出力:** `episodes/PD-2026-042-young/09_package/facts_lock.v001.json`（`{"pass":bool,"violations":[...],"skipped":[...]}`）。
**`pass:true` でない限り `check_final_acceptance.py` に進んではならない。**
**CLI:** `--json` / `--dryrun`（`_dryrun/` 配下も対象に含める）。対象ファイルが未生成なら**スキップして必ずログに出す**。「無いから通した」を黙るな。

---

# 3. ★境界契約: `asset_manifest.v001.json`（Aから受け取る唯一のファイル）

## 3.1 スキーマ（**Aが生成する。Bはこの形を前提に読む**）

**スキーマ版:** `young_assets.v1`（固定文字列。異なれば **exit 2**）。
EP42 spec の点数に一致: **still_body 85 / still_i2v_source 16 / motion 16 / factory 93 / overlay 12**。
**★サムネは独立の分類を持たない。** body 85枚のうち6枚に `also_thumb:true` を立てて流用する（サムネ専用の分類やサムネ用 count キーは無い・§11）。**このスキーマは CODEX_A（生産者）の `build_young_asset_manifest.py` の出力と1バイト単位で同一。**

```jsonc
{
  "schema_version": "young_assets.v1",
  "episode_id": "PD-2026-042-young",
  "slug": "young",
  "generated_at": "2026-07-21T12:00:00+09:00",
  "producer": "scripts/build_young_asset_manifest.py",
  "is_stub": false,                          // ★ログと受入判定にだけ使う。処理を分岐させない

  "counts": { "still_body": 85, "still_i2v_source": 16, "motion": 16, "factory": 93, "overlay": 12 },

  "stills": [
    { "asset_id": "YOUNG-S01", "scene_id": "S01", "role": "body",   // "body"|"i2v_source"|"reject"（バリエーション概念なし＝各1枚）
      "also_thumb": false,                   // body から6枚だけ true（S05/S30/S60/S63/S74/S84・追加生成しない）
      "act": 1,                              // 0=HOOK/OP, 1..4=幕, 5=ED
      "public_path": "young/img/S01.png",    // ★Bが cuts[].src に入れる値（1シーン1枚＝固有プロンプト・_01 等の接尾なし）
      "depth_path": "H:/pd-media/assets/ai/young/S01_depth.png",   // role=="body" は実在必須
      "width": 3840, "height": 2160,
      "sha256": "...", "tags": ["splintered door frame", "bare floor"], "caption_hint": "the door caves in",
      "source": "ai_codex", "commercial_use": "allowed",
      "qc": {"reviewed": true, "on_theme": true,
             "has_readable_text": false, "has_identifiable_face": false, "has_human_body": false, "notes": ""} }
    // i2v 種は role=="i2v_source"・asset_id "YOUNG-MS01".."YOUNG-MS16"・public_path は null（本編カットに出ない）
  ],

  "motion": [
    { "asset_id": "YOUNG-M01", "source_scene_id": "M01_src",   // ★i2v_source 種 ID を指す（body still ではない）
      "source_still": "H:/pd-media/assets/ai/young/M01_src.png",
      "public_path": "young/motion/M01_rife.mp4",   // ★必ず .mp4 かつ "_rife" を含む
      "act": 1, "width": 1280, "height": 720, "fps": 48, "frames": 164, "duration_sec": 3.417,
      "sha256": "...", "tags": ["dawn under a closed door"],
      "qc": {"reviewed": true, "on_theme": true, "artifact_free": true, "notes": ""} }
  ],

  "factory": [
    { "asset_id": "AF-BG-0221",
      "public_path": "young/factory/AF-BG-0221__empty_marble_chamber.mp4",  // ★必ず "/factory/" を含む
      "type": "backgrounds", "subtype": "empty_chamber", "kind": "video",
      "license": "Pexels License", "sha256": "...", "act": 3, "covers_scene_id": "S30",
      "duration_sec": 8.24, "width": 1920, "height": 1080,
      "eyeballed_content": "an empty marble chamber, wide static shot, no people",
      "qc": {"reviewed": true, "on_theme": true, "no_watermark": true,
             "no_recognizable_person": true, "no_cartoon": true, "label_matches_content": true, "notes": ""} }
  ],

  "overlay": [
    { "asset_id": "AF-PART-0007",
      "public_path": "young/overlay/AF-PART-0007__dust_motes.mp4",
      "type": "particle_assets", "subtype": "dust_motes", "license": "Pexels License",
      "sha256": "...", "blend_hint": "screen",
      "eyeballed_content": "slow drifting dust on black, loops cleanly",
      "qc": {"reviewed": true, "on_theme": true, "no_watermark": true, "notes": ""} }
  ]
}
```

## 3.2 Bがこのマニフェストから作るもの（**EP42 spec の cuts 割当**）

| マニフェスト | Bでの使い道 | spec |
|---|---|---|
| `stills[role="body"]` 85枚 | **静止画カット101本**（`kind:"img"`, `treatment` 循環）・**各≤2回** | still distinct85/cuts101 |
| body 静止画で `also_thumb==true` の6枚 | サムネ3案の背景（§11・S05/S30/S60/S63/S74/S84） | — |
| `stills[role="i2v_source"]` 16枚 | **本編カットに出さない**（i2v 種・A が Wan で motion 化済み） | — |
| `motion` 16本 | **i2vカット32本**（`kind:"footage"`）・**各≤2回** | motion distinct16/cuts32 |
| `factory` 93本 | **実写カット93本**（`kind:"footage"`）・**各1回のみ** | factory distinct93/cuts93 |
| `overlay` 12本 | **`cuts[].src` に出さない**（§5.5 の合成レイヤー扱い） | — |

**合計 101 + 32 + 93 = 226 カット / distinct 85+16+93 = 194 / first-use 194/226 = 0.8584 ✓（floor 0.70）**

## 3.3 `scripts/check_young_asset_manifest.py`（消費側バリデータ・BLOCKING）

```bash
$PY scripts/check_young_asset_manifest.py --assets <path> [--json]
```

検査（1つでも違反で exit 1。`schema_version` 違いだけ exit 2）:

1. `schema_version=="young_assets.v1"` / `episode_id=="PD-2026-042-young"` / `slug=="young"`
2. `counts.*` が各配列の実長と一致し**下限**: `still_body>=85` / `still_i2v_source>=16` / `motion>=16` / `factory>=93` / `overlay>=12`
   （`still_body` は `stills[role=="body"]` の実長、`still_i2v_source` は `stills[role=="i2v_source"]` の実長）
3. `role=="body"` の全静止画で `public_path` 非null、かつ `remotion/public/<public_path>` と
   `remotion/public/<stem>_depth.png` が**両方実在**（`CaseFilm.depthSrcOf()=src.replace(/\.[^.]+$/,'_depth.png')`。**depth 欠落はレンダークラッシュ**）。`role=="i2v_source"` は `public_path==null`（本編カットに出ない）
4. `role!="reject"` の全静止画で `max(width,height)>=3840`（`preflight_render_gate.MIN_LONG_EDGE_PX=3840`）
5. `motion[].public_path` が `.mp4` で終わり `_rife` を含む（§9 の `kind_of()` 判定用）。`motion[].source_scene_id` は `stills[role=="i2v_source"]` の種 ID（`M01_src` 系）を指す
6. `factory[].public_path` が `/factory/` を含む
7. `overlay[].public_path` が `/overlay/` を含み `/factory/` を**含まない**
8. `sha256` が全配列を通して一意（**EP39/40/41 の素材と sha256 被りゼロ** も別途 A が保証・B は自集合内一意を検査）
9. `factory[].eyeballed_content` が非空、かつ `qc.label_matches_content==true`
10. `qc.has_readable_text` / `qc.has_identifiable_face` / `qc.has_human_body` が true の項目は `role=="reject"`（**R1**）
11. `also_thumb==true` の body 静止画がちょうど6枚（サムネ供給・§11。CODEX_A 不変条件14 と一致）
12. **全文字列値**が §2 の R-FORBID / R-FACE / R-DOC / R-YOUNG / R-HUDSON を通る

## 3.4 `scripts/make_young_stub_assets.py`（**Aを待たずに完走するための鍵**）

やること:

1. `remotion/public/young_dryrun/{img,factory,motion,overlay}/` を作る
2. **静止画スタブ**: PIL で **3840×2160** 単色PNG（`scene_id` と `role` を大書き）＋同名 `_depth.png`
   （**`L` モード**のグラデ）。body **85枚 + depth 85枚**（うち6枚に `also_thumb:true`＝S05/S30/S60/S63/S74/S84）。
   i2v_source 16件はマニフェストにエントリだけ作る（`public_path==null`・本編に出ないので画像ファイル不要）
3. **動画スタブ**（ffmpeg `color` フィルタ）:
   - factory **93本**: `1920x1080@30fps`・**4.0秒**・`AF-STUB-<NNNN>__stub_clip.mp4`
   - motion **16本**: `1280x720@48fps`・**3.417秒**・`M<NN>_rife.mp4`
   - overlay 12本: `1920x1080@30fps`・2.0秒
4. **スタブ黒ベース**: `episodes/PD-2026-042-young/08_edit/_dryrun/young_final_bgm.v002.mp4` を
   ffmpeg `color=c=black:s=1920x1080:r=30` ＋無音aac で **≈730秒**生成（§7.10 のコンポジタが本番と同じ経路で走れるように）
5. `05_visuals/asset_manifest.stub.v001.json` を **§3.1 と完全に同じスキーマ**で書く
   （`is_stub:true`・`public_path` 先頭を `young_dryrun/` に）

**★スタブのパスの罠（外すと `check_asset_reuse.kind_of()` が誤分類して緑になってしまう）:**

```python
p = path.lower().replace("\\", "/")
if "/factory" in p or re.search(r"\baf-bg-", p):                            return "factory"  # 上限1回
if p.endswith((".mp4",".mov",".webm")) or "ai_video" in p or "_rife" in p: return "motion"   # 上限2回
return "still"                                                                                # 上限2回
```

| 種別 | `public_path` の形 | 満たす条件 |
|---|---|---|
| 静止画 | `young_dryrun/img/S01.png` | `/factory` を含まない・`.png`・`_01` 等の接尾なし |
| factory | `young_dryrun/**factory**/AF-STUB-0001__stub_clip.mp4` | **`/factory/` を含む** |
| i2v | `young_dryrun/motion/M01**_rife**.mp4` | **`.mp4` かつ `_rife` を含む** |
| overlay | `young_dryrun/overlay/...mp4` | **`cuts[].src` に出さない** |

**スタブの点数は本番と完全に同じ**（body 85〈うち also_thumb 6〉/ i2v_source 16 / motion 16 / factory 93 / overlay 12）。
これで**素材が1枚も無い段階で全ゲート通過を実証できる。**

## 3.5 本番マニフェストへの切り替え — **コードは1行も変えず** `--assets` を差し替えるだけ。
差し替え後、[B-DONE-2]〜[B-DONE-8] を全部やり直す。

---

# 4. narration_index（TTS は課金＝禁止。スタブで着手し、本番で差し替える）

## 4.1 なぜ narration_index か
`build_young_film.py` は**尺・区間・字幕を narration_index から導出する**。**秒数をコードに直書きしない。** 唯一の正は narration_index。

## 4.2 スキーマ（`young_narration.v1`）

```jsonc
{
  "schema_version": "young_narration.v1",
  "episode_id": "PD-2026-042-young",
  "is_stub": true,
  "total_seconds": 720.9,
  "chunks": [
    { "section": "HOOK", "start": 0.000, "end": 4.100,
      "text": "February. Chicago. After a long shift, a social worker is changing out of her work clothes." },
    { "section": "OP",   "start": 24.400, "end": 28.100, "text": "..." },
    { "section": "ACT_1","start": 46.900, "end": 51.200, "text": "..." }
  ]
}
```

**section 値（固定）:** `HOOK` / `OP` / `ACT_1` / `ACT_2` / `ACT_3` / `ACT_4` / `ENDING`。
`build_young_film.py` は `section_windows()`（各 section の最初のチャンク start）で幕境界を得る。

## 4.3 spec のタイムライン（**設計目標。実タイミングは narration_index が上書きする**）

| section | 語数 | 秒 | 備考 |
|---|---|---|---|
| HOOK | 62 | 20.9 | VO。末尾に `SILENCE 1.8s`（戸口の残響のみ） |
| （gold `BrandOpening`） | 0 | 3.5 | 非VO。`OPENING_SEC`。**frame0 ではなく HOOK 後に挿入** |
| OP | 55 | 18.5 | 二人称の問い（thesis）＋ channel ID |
| ACT_1 The Wrong Door | 301 | 101.4 | 踏み込み。途中に `SILENCE 1.5s — the body camera keeps recording` |
| ACT_2 The Tape | 282 | 95.0 | 映像秘匿→放映→COPA。末尾に `SILENCE 0.9s` |
| ACT_3 The Command | 657 | 221.3 | 判例核。**最も遅く長い**。5-4・still a command・Part IV=4票 |
| ACT_4 The Reach | 319 | 107.5 | $2.9M・48-0(reported)・10-4 否決 |
| ENDING | 331 | 111.5 | ペイオフ→CTA。途中に `SILENCE 1.0s` |
| （`BrandEndcard`） | 0 | 9.0 | 非VO。`ENDCARD_SEC` |

**唯一の正は `python scripts/check_script_length.py <script> --json`。** 総語数 **2,140**（spec `words_total`）/ `wpm 178.1` /
narration_seconds **720.9**（spec）。**自己申告・体感の尺判定は禁止。**

## 4.4 `scripts/make_young_stub_narration.py`（**Bはこれで着手できる**）

`EP42_young_script.en.v001.md` を読み、各 section 見出し配下の本文を文に割り、178.1 wpm で各文に start/end を割り当てて
`chunks[]` を作る。`【SILENCE 1.8s】` `【SILENCE 1.5s …】` `【SILENCE 0.9s】` `【SILENCE 1.0s】` のト書きは
**無音ギャップ**として時間を進める（チャンクにはしない）。`【OP】`（OPENING NARRATION）の前に `OPENING_SEC=3.5` の無音を挿入。
台本本文はそのまま（改変しない）。出力: `06_audio/narration_index.stub.v001.json`（`is_stub:true`）。

> **本番:** 別工程が TTS→faster-whisper で `06_audio/narration_index.v001.json`（実測語タイム）を作る。
> **これは課金ジョブなので B は起動しない。** 来たら `--narr` を差し替えるだけ。

---

# 5. `young_film.json` の構築（`scripts/build_young_film.py`＝`build_thompson_film.py` の複製）

## 5.1 `FilmData` 型（`CaseFilm.tsx` から。これに従う）

```ts
export type Cut = {start:number; dur:number; kind:'img'|'footage'; src:string; treatment:string; seed:string};
export type FilmData = {
  fps:number; narration:string; narrationSeconds:number; hookSeconds:number; hookLine:string;
  hook:{start:number;dur:number;kind:string;src:string;seed:string}[];
  cuts:Cut[]; captions:{start:number;end:number;text:string}[];
  graphics:{start:number;end:number;lines:string[]}[];      // 必須フィールド。EP42 は []
  figures?:FigureSpec[]; heroCuts?:{start:number;dur:number;src:string}[];
};
export const caseFilmDurationInFrames = (data, fps) =>
  Math.round((data.hookSeconds||0)*fps) + Math.round(OPENING_SEC*fps)
  + Math.ceil(data.narrationSeconds*fps) + Math.round(ENDCARD_SEC*fps);
```

- アセットのパスキーは **`src`**（`remotion/public/` からの相対、`staticFile()` 解決）
- **カット単位の transition/motion は無い。** 動きは `treatment`・`seed`・`index%2`・`index%3` から導出
- `treatment` の実装値: `'depth'|'scan'|'duotone'|'focus'|'card'|'bleed'`（既定 bleed）
- `kind:'footage'` は `treatment` を無視して `<Footage>` を描画する
- `fps = 30`。`narration = "young/narration.mp3"`（本番のみ実在）

## 5.2 カット構成（**§3 マニフェストから機械的に組む・紙芝居回避が最優先**）

```
総カット 226 = factory 93 (footage) + motion 32 (footage) + 静止画 101 (img)

[A] first-use share（check_asset_reuse floor 0.70）
    distinct 93+16+85 = 194 → 194/226 = 0.8584            ✓ >=0.70（spec first_use_share と一致）

[B] per-asset cap（check_asset_reuse）
    factory: 93/93  = 1.00回  ✓ <=1（★factory は再使用禁止）
    motion : 32/16  = 2.00回  ✓ <=2
    still  : 101/85 = 1.19回  ✓ <=2

[C] animation_mix（★2つの尺度を両方満たす）
    (i) cut数ベース   still-share = 101/226 = 0.4469        ✓ <=0.45（★余裕が薄い＝§下の警告）
        motion coverage = (93+32)/226 = 125/226 = 0.5531    ✓ >=0.45（spec と一致）
    (ii) frame ベース still 平均 3.00s → 101×3.00 = 303.0s
        footage 平均 3.343s → 125×3.343 = 417.9s
        still-frame-share = 303.0 / 720.9 = 0.4203          ✓ <=0.45（cut数比より安全側）
        motion-coverage(frame) = 417.9 / 720.9 = 0.5797     ✓ >=0.45

[D] 平均ショット長（spec mean_shot 3.19 / max 6.0）
    720.9 / 226 = 3.19 秒/カット                            ✓ <=6

[E] factory 下限（30秒に1本 = 24 → >=24本） 93本            ✓
```

> **★[C](i) の cut数ベース still-share 0.4469 は cap 0.45 に薄い。still を1枚増やすか factory を1本削ると 0.45 を割る（超える）。**
> **マニフェストが still 85 / factory 93 / motion 16 を割ったら組まずに止めて A に差し戻す（ブリーフ§2: still を増やして factory を削るな）。**
> **frame ベースも下回るよう、still の平均尺を footage より系統的に短く保つ（§5.3-5）。**

## 5.3 カット割り当てのルール（`build_thompson_film.py` の `allocate()`/`tile_window()` を踏襲）

1. 各幕の秒窓を `section_windows()` から取り、幕内に **factory : motion : still を按分**して配置
   （目安の幕別カット数。実配分は narration_index の窓長で自動調整）:

   | section | factory | motion | still | 小計 |
   |---|---|---|---|---|
   | HOOK+OP | 5 | 2 | 6 | 13 |
   | ACT_1 | 14 | 4 | 15 | 33 |
   | ACT_2 | 12 | 5 | 13 | 30 |
   | ACT_3 | 28 | 10 | 31 | 69 |
   | ACT_4 | 16 | 5 | 16 | 37 |
   | ENDING | 18 | 6 | 20 | 44 |
   | **計** | **93** | **32** | **101** | **226** |

2. **factory は各1回のみ**（使用済み集合を持ち二度と引かない）。**motion は各≤2回・still は各≤2回**（`allocate(cap=…)`）
3. **同一素材を連続させない**（順序を散らす）
4. 静止画 `treatment` は `["depth","scan","duotone","focus"]` を循環（同じ treatment を3連続させない）
5. **still の `dur` を footage の `dur` より系統的に短く**（§5.2[C]。`tile_window` の重みで still 側を小さめに）
6. motion の `dur` は **3.0–3.4秒**（実素材 3.417s。超えるとループが見える）
7. **AEカードの区間（§7.2）に重なるカットも存在させる**（コンポジタ SKIP 時に穴が空かないため）

## 5.4 `figures[]` と `captions[]`
- `figures[]` は §6（**37本**・spec floor 31 に +6 の余裕・`graphics[]=[]`）
- `captions[]` は narration_index の全チャンクを **verbatim**（`build_captions()` と同一）。SRT も同時出力

## 5.5 合成レイヤー（`overlay`）— **`cuts[].src` に出さない**
`overlay` 12本は「加工」。`cuts[].src` に入れると `kind_of()` が factory 判定（上限1回）になり FAIL する。
`young_film.json` に **`overlays` 独自キー**で持たせる（`CaseFilm` は未知キーを無視）か、専用レイヤーで `screen` 合成する。

## 5.6 ビルダが出力する成果物（**asset_map→manifest変換＋beatsheet生成**）

| 出力 | パス |
|---|---|
| film.json | `remotion/src/data/young_film.json` |
| public コピー | `remotion/public/young/film_data.v001.json` |
| **build provenance**（asset_map→provenance変換） | `episodes/PD-2026-042-young/04_scenes/young_build_manifest.v001.json`（**A の `05_visuals/asset_manifest` に書かない**） |
| **beatsheet**（figures+AE区間の突き合わせ表） | `episodes/PD-2026-042-young/04_scenes/young_beatsheet.v001.json` |
| SRT（字幕未生成時のフォールバック） | `episodes/PD-2026-042-young/08_edit/captions.final.v001.srt`（**§8 の生成器が上書きする**） |

> **★beatsheet の命名に関する重大な注意:** `check_motion_density` / `check_animation_mix` は
> `04_scenes/premium_beatsheet.v*.json` を**自動検出して film.json より優先**する。
> **B の beatsheet は `young_beatsheet.v001.json`（`premium_` を付けない）** にして、**ゲートの測定源を film.json 一本に保つ**
> （二重ソースの乖離＝EP39/40 の矛盾28件の原因を避ける）。`young_beatsheet` は provenance と `validate_young_beats` 専用。

## 5.7 CLI
```bash
$PY scripts/build_young_film.py \
  --assets <asset_manifest path> \
  --narr   <narration_index path> \
  --out    remotion/src/data/young_film.json \
  [--captions episodes/PD-2026-042-young/08_edit/captions.final.v001.srt]
```
**`--assets` の `is_stub` によって処理を変えないこと（§0.2）。** 末尾に `check_asset_reuse` 相当の自己レポートを print する。

---

# 6. Remotion 側 `figures[]`（**37本・spec floor 31 に +6・`graphics[]=[]`**）

## 6.1 密度の検算（`check_motion_density`・**AEカードは1本も数えられない**）

```
figures 37本（film.json） / body 12.015分(=720.9/60) = 3.08 /分    ✓ beats_per_min_floor 2.5
coverage: 37本 × 平均5.4s = 199.8s / 720.9 = 27.7%                  ✓ MIN_ANIMATED_COVERAGE 0.25
variety : 下記 kind を12種以上使用                                 ✓ variety_floor 3
spec motion.beats_floor = 31 に対し 37 で余裕。coverage が最も薄いので figures の dur は 4.8–6.0s を基本に。
```

> **★3軸すべて AND。density/coverage/variety のどれか1つでも floor 未満で FAIL。**
> 37本を非重複で置き、平均 dur を 5.4s 程度に確保すること（coverage が floor 0.25 に一番近い）。

## 6.2 ★★★ `FigureSpec` の `kind` は**実在する小文字値のみ** ★★★

> **大文字名（`ActTitle`/`QuoteCard`/`VoteTally`…）は `FigureBeats.tsx` の union に無く、無言で描画が消える。**

**EP42 で使う実在 `kind`（`remotion/src/components/FigureBeats.tsx` の union から。全て共通で `start`/`end` 必須・全小文字）:**

| `kind` | 必須プロパティ | EP42での用途 |
|---|---|---|
| `numberticker` | `value:number` / `label?` / `prefix?` `suffix?` `decimals?` | 3–5 秒・~16か月・~100件・10–4 |
| `stat` | `value:number` / `label:string` / `prefix?` `suffix?` `decimals?` `topLabel?` | ≈12警官・$2.9M・4票のみ・5–3 |
| `votetally` | `majority:number` / `dissent:number` / `label?` | **5対4（Hudson のみ）**（F15・R-SPLIT） |
| `timeline` | `events:{year:string;text:string}[]` | 2019→2020→2021→2022 / 1998→2006 |
| `quote` | `quote:string` / `attribution:string` | Scalia "still a command" / "section 1983"（**帰属必須**） |
| `kinetic` | `lines:string[]` / `style?:'wordpop'\|'maskslide'\|'emphasis'` / `emphasisWords?` | 決め所テキスト（**emphasisWords は短く=文字切れ回避**） |
| `lowerthird` | `primary:string` / `secondary?` / `accent?` | 開示 `AI-assisted visualization` / SECTION 1983 定義 / 令状 |
| `acttitle` | `title:string` / `kicker?` / `index?` | 幕頭（Remotion 側で密度に数える。§7 の AE 幕頭とは別区間） |
| `compbars` | `items:{label:string;value:number;accent?}[]` | 「sorry vs liable」等の対比（※`comparebars` は存在しない） |
| `mechanism` | `mechanism:'closingdoor'\|'gears'\|'faultsplit'` ★discriminant は `kind`・変種は `mechanism` | 割れる/閉じる戸口(closingdoor)・救済の移動(gears)・射程(faultsplit) |
| `dochighlight` | `rects:{x,y,w,h}[]` / `mode?:'underline'\|'box'\|'redact'` | 令状/書類（**redact**＝象徴・読ませない・R1/C-6） |
| `regionmap` / `pindropmap` | `label?` / `pins:{x,y,label?}[]` | Chicago West Side / Detroit の戸口 |

**`votetally` は `majority:5, dissent:4` 固定（Hudson のみ・§2 R-SPLIT）。48-0/10-4/5-3 は votetally に入れない。**
`quote[].attribution` は §2 の `APPROVED_QUOTES` に一致させる。

## 6.3 figures アンカー設計（`build_thompson_film.py` の `FIGURE_ANCHORS` 方式）

**方式:** `(anchor_sec, payload)` の配列を秒昇順に置き、`build_figures()` が
`end = min(anchor+FIG_DUR, next_anchor-FIG_GAP, total-0.5)` でクランプ、`end-start < FIG_MIN_DUR` なら **exit 1**。
`FIG_DUR=5.4 / FIG_MIN_DUR=3.0 / FIG_GAP=0.4`。**アンカー秒は narration_index の section 窓に対する相対で決め、
`section_windows()` を基準にオフセットで置く**（秒直書き禁止）。

**配置方針（37本・§2 台帳の値だけを焼く・kind を分散して variety を稼ぐ・6制約順守）:**

- **HOOK/OP（3）:** `kinetic`（"THE WRONG HOUSE"）/ `lowerthird`（`AI-assisted visualization` 開示）/ `mechanism:closingdoor`（割れる戸口）
- **ACT_1（7）:** `acttitle`（THE WRONG DOOR）/ `stat`（F02 ≈12 OFFICERS）/ `lowerthird`（"a search warrant, signed by a judge" ← **C-2: no-knock 語を出さない**）/ `kinetic`（"THE WRONG HOUSE"・彼女の言葉/emphasisWords=["WRONG"]）/ `dochighlight:redact`（令状=読ませない）/ `mechanism:closingdoor` / `timeline`（F01 Feb 2019）
- **ACT_2（6）:** `acttitle`（THE TAPE）/ `timeline`（F06 Dec 2020 映像放映）/ `numberticker`（F07 ≈16 months, label "COPA"）/ `numberticker`（F08 ≈100, suffix " ALLEGED"）/ `kinetic`（"ALLEGED — NOT PROVEN"・emphasisWords=["ALLEGED"]／C-1 の趣旨）/ `lowerthird`（"police-oversight investigation"）
- **ACT_3（11）:** `acttitle`（THE COMMAND）/ `dochighlight`（第4修正の一文=光）/ `timeline`（F17 Aug 1998 → F15 June 2006）/ `numberticker`（F16 3–5 seconds）/ `votetally`（**F15 5対4**, label "Supreme Court · 2006"）/ `quote`（"still a command" → attribution "Justice Scalia, for the majority"／**C-4**）/ `stat`（**F18 4票のみ**, label "Part IV · Kennedy did not join"／C-4）/ `kinetic:emphasis`（"STILL A COMMAND"）/ `lowerthird`（**F19 SECTION 1983**, secondary "the civil remedy"）/ `mechanism:gears`（救済が刑事→民事へ移動）/ `mechanism:faultsplit`（射程＝排除のみ否定）
- **ACT_4（6）:** `acttitle`（THE REACH）/ `stat`（**F03 $2.9M**, label "reported · no finding of fault"／**C-1・R-SETTLEMENT**）/ `kinetic`（"A SETTLEMENT, NOT A FINDING"）/ `numberticker`（**F12 10–4**, label "voted down"／**C-3**）/ `stat`（F11 5–3, label "Police Board · Wolinski"）/ `dochighlight:box`（過失欄=空白）
- **ENDING（4）:** `kinetic`（"STILL LEGAL"・emphasisWords=["LEGAL"]／**C-3**）/ `lowerthird`（開示 再掲）/ `kinetic:emphasis`（"IT WAS YOUR DOOR"）/ `mechanism:closingdoor`（閉じた静かなドア・夜明け）

> **48-0（F05）を figure に焼く場合は必ず `stat` で `label:"reported · a settlement, not a finding"` を付ける（R-SETTLEMENT）。
> 単独の勝利数として出さない。** 上記37本には含めていない（AE カード s? 側で "reported" 枠で扱う／§7.2）。

## 6.4 配置ルール
1. **AEの区間（§7.2）と1秒でも重ならない**（`validate_young_beats` が突き合わせ）
2. **同じ kind を連続させない**（`mechanism` の直後に `mechanism` を置かない）
3. 1枠 **4.8–6.0秒**
4. `quote[].quote` / `kinetic[].lines` / `*.label` は §2 の R-LEDGER・R-ATTRIB・R-FORBID・R-FACE/R-DOC・R-SETTLEMENT 検査対象
5. 台帳外の数値を `value`/`numKeys` に置かない（**焼いたら R-LEDGER で FAIL**）
6. **`emphasisWords` は1–2語の短句のみ**（長句は AE/Remotion で末尾が切れる＝EP40 実害。§7.5-3 と同趣旨）

---

# 7. After Effects カード（`build_young_hero_cards.py` / `composite_young_hero.py`）

## 7.1 位置づけ
AEカードは **film.json とは別**に ffmpeg で本編に焼き込む（§0.5-2＝密度に数えられない）。
`build_thompson_hero_cards.py` を**コピーしてパス・定数・CARDS デッキだけ差し替える**。レイアウト実装・
`money_keys()`・`fit_size()`・完了マーカー・機械の罠対処は**1行も削らない**。

## 7.2 AEカードデッキ（**単調増加・重複ゼロ・台帳裏付けのみ・6制約順守。この表が契約。8枚**）

**区間の秒は本番の rendered base（narration_index 由来）に一致させる。** 下表の秒は spec タイムライン基準の**目安**で、
`build_young_hero_cards.py` は section 窓からオフセットで算出しクランプする。**背景静止画は象徴オブジェのみ（R1/C-5/C-6）。**

| id | レイアウト（**実装済み8種のみ・§7.3**） | 内容 | F-ID | 背景（象徴のみ） | required |
|---|---|---|---|---|---|
| t01 | ACT_TITLE_CARD | 幕1 THE WRONG DOOR | — | 割れる戸口 | 必須 |
| n01 | CENTER_STACK | **ABOUT 12 OFFICERS** | F02 | 散らばった書類 | 必須 |
| c01 | CENTER_STACK | **~16 MONTHS** / **~100 ALLEGED** | F07/F08 | 封をされたマニラ封筒(illegible) | 必須 |
| k01 | QUOTE_CARD | **STILL A COMMAND OF THE FOURTH AMENDMENT**（attribution: JUSTICE SCALIA, FOR THE MAJORITY） | — (quote) | 壁を走る第4修正の光 | 必須 |
| v01 | VOTE_SPLIT | **5 TO 4**（Supreme Court · 2006） | F15 | 空の9席(顔なし) | 必須 |
| e01 | CENTER_STACK | **SECTION 1983**（the civil remedy） | F19 | 使われないガベル | 必須 |
| m01 | MONEY_STACK | **$2.9M** ／ sub: **reported · no finding of fault** | F03 | 机の上の小切手・空白の過失欄 | 必須 |
| r01 | SPLIT_COMPARE | **10 – 4** ／ **REJECTED · STILL LEGAL** | F12 | 脇に置かれた印刷条例 | 必須 |

> **代替候補（差し替え可・ブリーフ§6・実装済みレイアウトのみ）:** `48–0`（MONEY_STACK・sub "reported · a settlement, not a finding"／R-SETTLEMENT）、
> `3–5 SECONDS`（CENTER_STACK・F16）。**採用時も 8枚・単調増加・重複ゼロを保ち、レイアウトは §7.3 の実装済み8種から選ぶ。** どのカードにも
> `no-knock`/`unconstitutional`/`she changed the law` を書かない（R-FORBID）。

**検算（Codex は自分で再計算して一致を確認）:** 8区間・単調増加・重複ゼロ・HOOK(0–20.9) と ENDCARD(末尾9s) に重ねない。
Remotion figures(§6) と1秒も重ならない（`validate_young_beats` が検査）。

## 7.3 レイアウト（`build_thompson_hero_cards.py` の実装を踏襲・**実装済みレイアウト名だけを使う**）
複製元 `build_thompson_hero_cards.py` が実装するレイアウトは**この8種のみ**:
`DATE_STAMP` / `CENTER_STACK` / `MONEY_STACK` / `SPLIT_COMPARE` / `ACT_TITLE_CARD` / `QUOTE_CARD` / `VOTE_SPLIT` / `SEAM_TRANSITION`。
**§7.2 デッキはこの8種の名前しか使わない**（上記以外の独自レイアウト名を発明しない＝`validate_young_beats` §7.9 ルール3 で FAIL する）。
**共通レイヤースタック・色定数・Anton/Oswald・`psName()` の runtime 解決（allFonts の array-LIKE ラッパーを unwrap）は複製元と同一。**

**★共通レイヤースタックに AI開示レイヤーを1枚追加（R1・全カード常時焼き）:** 最上位に近い固定レイヤーとして
`AI-assisted visualization`（Oswald 20px / SILVER `#C8CDD6` / opacity 70% / 右下 `[W-32, H-28]`）を全カードに焼く。
AEカードは不透明の全画面 mp4 として本編に overlay されるため、これが無いと本編(Remotion)右下の開示が隠れ、
AI生成 static 背景が開示なしで表示される（**R1 違反**）。字幕帯とは縦56px 以上離す。

**EP42 色定数（0..1 float・夜のシカゴ西部＋法廷大理石トーン・DESIGN §0.5 と一致）:**
```python
ACCENT = [0.231, 0.490, 0.847]  # #3B7DD8 warrant-blue アクセント（数値・下線・EP41 gold と分離＝レーン分離）
WHITE  = [0.961, 0.969, 0.980]  # #F5F7FA
SILVER = [0.784, 0.804, 0.839]  # #C8CDD6（開示テキスト）
INK    = [0.039, 0.039, 0.047]  # #0A0A0C 近黒ルート（サムネ bg と一致）
DAWN   = [0.788, 0.541, 0.227]  # #C98A3A 戸口/夜明けの単一暖色（象徴のみ）
RED    = [0.780, 0.290, 0.243]  # #C74A3E r01 REJECTED の取り消しのみ
```

**数値カードは全て `money_keys()` 系で表示文字列を Python 事前計算**（JSX で算術しない＝EP38 確定ルール）。
`VOTE_SPLIT` は「5」を先に、間を置いて「4」を出し `5-4` の緊張を作る（多数=SILVER・反対=ACCENT warrant-blue）。
**`m01`/`r01` は数値の下に必ず sub ラベル（"reported · no finding of fault" / "voted down"）を別レイヤーで出す（C-1/C-3）。**

## 7.4 `beats.json` スキーマ（本番 `08_edit/ae_hero/beats.json` / dryrun `08_edit/_dryrun/ae_hero/beats.json`）
`build_thompson_hero_cards.py` の beats スキーマに準拠。各 beat に `id` / `layout` / `start` / `end` / `dur` /
`still`(象徴 or null) / `hero`(主表示文字列) / `top` / `bottom` / `caption`(**改行禁止・最大50字**) /
`value` / `numKeys` / `blend_mode`(既定 "overlay") / `required` / `out` / `attribution`(**QUOTE_CARD=k01 は必須**・§2 `APPROVED_QUOTES` と一致・R-ATTRIB)。
**`value` / `hero` の数値は §2 台帳の `verified:true` 値のみ**（`check_young_facts` が照合）。
**`m01`/`r01`/`48-0` 系は R-SETTLEMENT を満たすサブ文字列を `bottom` か `caption` に持つ。**

## 7.5 このマシン固有の罠（複製元が対処済み。**1つも省くな**）
1. `setTemporalEaseAtKey` の配列次元は **spatial(Position) で 1**（`if(!prop.isSpatial){...}` で分岐）
2. RS = **`"最良設定"`** / OM = **`"H.264 - レンダリング設定を一致 - 15 Mbps"`**（英語名は try/catch フォールバックのみ）
3. TextDocument の改行は `\n` 不可。**`caption` は1行**（改行が要るなら別レイヤー）。**テキスト幅は `sourceRectAtTime(t,false).width` で実測**（advance-width 推定は禁止＝EP40 の文字切れ原因）
4. `app.newProject()` は headless でハング。**使わず**同名コンプを防御削除
5. ビルドは**カード8枚で 120–200秒**。`render/_build_ok.txt` をポーリング（**タイムアウト最低600秒**）
6. 起動はデタッチ + 出力ポーリング。jsx 末尾で `app.quit()`
7. `comp.motionBlur=true` だけでは無効。**動かすレイヤー個別に `layer.motionBlur=true`**
8. 2Dレイヤー回転は **`"ADBE Rotate Z"`**（`"ADBE Rotation"` は null）
9. `inPoint` と `outPoint` の**両方**を設定
10. 読み込み後 `item.mainSource.conformFrameRate = 30`（忘れると全カードの timing がズレる）
11. 実行パス `C:\Program Files\Adobe\Adobe After Effects 2026\Support Files\AfterFX.exe`（実在確認済み）
12. `proj.gpuAccelType = GpuAccelType.SOFTWARE`（RTX4090 でもソフトレンダ固定・安定優先）
13. **`getFontsByFamilyNameAndStyleName` を使うフォント厳格解決**（miss は throw・フォールバック禁止／allFonts[i] ラッパー経由 unwrap）
14. **フォント文字列やラベルを PowerShell 経由の正規表現/エスケープで生成しない**（`\b` がバックスペース化した実害）。Python 側で literal に組む。**Python 先頭に `sys.stdout.reconfigure(encoding="utf-8")`**
15. **aerender 前に `.aep` の mtime > `.jsx` の mtime を assert**（古い .aep を焼く事故防止＝EP39-41 実害）

## 7.6 実行
```bash
$PY scripts/ae/build_young_hero_cards.py [--dryrun]
"C:/Program Files/Adobe/Adobe After Effects 2026/Support Files/AfterFX.exe" -noui \
  -r ".../episodes/PD-2026-042-young/08_edit/ae_hero/young_hero.jsx"
# render/_build_ok.txt を待つ（最大600秒）→ render/*.mp4 が8本揃うまで待つ（最大1200秒）
$PY scripts/ae/composite_young_hero.py [--dryrun]
```

## 7.9 `scripts/validate_young_beats.py`（BLOCKING）
1. `beats[].start` 昇順・区間非重複
2. 全 `start`/`end` が本編ナレ区間内（HOOK 0–20.9 と ENDCARD 末尾9s に重ねない）
3. `layout` が §7.3 の**実装済み8種**（`DATE_STAMP`/`CENTER_STACK`/`MONEY_STACK`/`SPLIT_COMPARE`/`ACT_TITLE_CARD`/`QUOTE_CARD`/`VOTE_SPLIT`/`SEAM_TRANSITION`）のいずれか。**この8種以外のレイアウト名は FAIL。** still が必要なレイアウトで null なら FAIL・ベクター系(SEAM)で非null なら FAIL
4. `still` 非null は実在＋長辺 >=3840px
5. `hero`/`top`/`bottom`/`caption`/`value` が §2（R-FORBID/R-LEDGER/R-ATTRIB/R-SETTLEMENT/R-HUDSON/R-FACE/R-DOC/R-DATE/**R-C4**）を通る
6. `verified:false` の値を要求するカードは `required:false` で**除外**、`required:true` なら exit 1（`--dryrun` は警告続行）
7. **`young_film.json` の `figures[]`（§6）と AE の区間が1秒でも重ならない**
8. `caption` に改行が含まれない
9. **AI開示レイヤーの存在（R1）** — ビルダが全カード共通スタックに `AI-assisted visualization`（右下・§7.3）を焼く設定であること
   （`build_young_hero_cards.py` の共通スタック定義に開示レイヤーが1枚あることを静的に確認）。無ければ FAIL。
   受入アイボール（§13.1）でも「AEカード表示中も右下の開示が見える」を確認する。

## 7.10 基底 mp4 とコンポジタ（`build_young_bgm.py` → `composite_young_hero.py`）
```
# 完成後の合成順（ブリーフ§5）: build_young_bgm.py（narration+BGM）→ composite_young_hero.py（AEカード焼込み）
BASE = episodes/PD-2026-042-young/08_edit/young_final_bgm.v002.mp4     # build_young_bgm.py が生成
OUT  = episodes/PD-2026-042-young/08_edit/young_final_bgm.v003_ae.mp4  # composite_young_hero.py が生成
FFMPEG  = C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe
FFPROBE = C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffprobe.exe
W,H,FPS = 1920, 1080, 30
```
**SKIP4条件を1行も削らない:** ① `render/<id>.mp4` 不在 ② 解像度 != 1920x1080 ③ 実測尺 `< dur-0.3` ④ `beat.end > base_dur`。
SKIP された区間は元カットのまま残る（作品は壊れない）。**何枚 SKIP したかを stderr に必ず出す。**
ffmpeg は `overlay=0:0:eof_action=pass:enable='between(t,start,end)'`（`blend_mode` が screen/multiply の時のみ `blend`）。
**出力後 `probe_dur(OUT)` でベースとの尺差 <=0.5秒を確認。出荷済みは絶対に上書きしない（必ず `_v003_ae`）。**
**dryrun のベースは §3.4 のスタブ黒ベース `_dryrun/young_final_bgm.v002.mp4`。**

---

# 8. 字幕の切断規則（`scripts/gen_captions_young.py`＝`gen_captions_thompson.py` の複製）

## 8.1 原則
**文字数は「上限」であって「分割基準」ではない。** `gen_captions_thompson.py` の `internal_split()` / `chunk_sentence()` を**そのままコピー**。
`from fix_caption_dangling import NO_DANGLE_END, wrap as safe_wrap`（**語リストを自前で書き直さない**）。

## 8.2 通すゲート `scripts/check_caption_breaks.py`（**閾値を緩めるの禁止**）
- **A. 行末の機能語**（複数行キューの最終行以外が句読点なしで `NO_DANGLE_END` の語で終わる）= 0件
- **B. 孤立キュー**（語数<3 で「終端句読点で終わる」「大文字で始まる」の両方を満たさない）= 0件
- **C. 句をまたぐ切断(hard)** = 0件
- A/B/C いずれか1件で FAIL（**実質ゼロ許容**）

## 8.3 EP42 の入力と対応
- 入力は **narration_index の各チャンク文**（`--narr`）。**字幕テキストは台本本文と1:1対応**（§0.5-5）。台詞・別エピソード文の混入禁止。verbatim で使い、構文境界で分割するだけ。
- `ABBR` に `U.S.` / `v.` / `Mr.` / `Sgt.` 等を持つ（`Hudson v. Michigan` の `v.`、`U.S. 586` の `U.S.` で文を切らない）。
- タイミングは narration_index の start/end。CPS <=27・最小表示 0.90秒。**Step で決めた境界を時間都合で動かさない。**
- **字幕にも R-FORBID 適用**（台本本文に禁止語は無いので verbatim なら自然に通るが、`check_young_facts` の対象でもある）。

## 8.4 セルフテスト（`--selftest`・EP38 実害を回帰に）
`"...before she can cover herself."` → `"herself."` を単独キューにしない等の4ケースを実装し、
**出力を `check_caption_breaks.py` に食わせて exit 0 まで自動確認。**

## 8.5 実行
```bash
$PY scripts/gen_captions_young.py --narr episodes/PD-2026-042-young/06_audio/narration_index.stub.v001.json
$PY scripts/check_caption_breaks.py episodes/PD-2026-042-young/08_edit/captions.final.v001.srt
# → PASS が出るまで直す。ゲート側の閾値を緩めるのは禁止。
```

---

# 9. 5ゲートの実際の判定（**build 後に必ず全部通す・animation_mix を忘れるな**）

| ゲート | 実体 | 入力 | EP42 の通過根拠 |
|---|---|---|---|
| `check_asset_reuse.py <film.json>` | factory≤1 / motion≤2 / still≤2 / first-use≥0.70 | **film.json 位置引数** | §5.2: factory1.00 / motion2.00 / still1.19 / first-use **0.8584** |
| `check_motion_density.py --ep PD-2026-042-young` | film.json の graphics+figures+heroCuts のみ / density≥2.5・coverage≥0.25・variety≥3（**AND**） | **`--ep`** | §6.1: **3.08 / 27.7% / 12+種**（AEカードは0本＝§0.5-2） |
| `check_animation_mix.py --ep PD-2026-042-young` | film.json の cuts を img=still/その他=footage 分類 / still-share≤0.45・motion-cov≥0.45 | **`--ep`** | §5.2[C]: still-share **0.4469(cut)/0.4203(frame)** / motion-cov **0.5531+** |
| `check_caption_breaks.py <srt>` | A/B/C 各0件 | **srt 位置引数** | §8 の構文境界生成器 |
| `check_script_length.py <script> --json` | 総語数 / wpm / narration_seconds | **script 位置引数** | 2,140語 / wpm178.1 / **720.9s** |

> **★ゲートの入力指定（ブリーフ§5）:** density/mix は **`--ep PD-2026-042-young`**。**`--json <film.json>` は出力パス
> （上書き事故）なので入力に使わない。** asset_reuse は film.json 位置引数、caption_breaks は srt 位置引数、script_length は script 位置引数。
>
> **`check_animation_mix` は `04_scenes/premium_beatsheet.v*.json` があればそれを優先する。**
> §5.6 の通り B の beatsheet は `young_beatsheet`（`premium_` 無し）なので**auto-detect されず film.json を測る。**

---

# 10. OP バンパー `OpeningYoung`（Remotion・fps60/1920x1080/180f）

## 10.1 二重OPを作らない
本編（`Ep42Young`）の OP は `Bookends.tsx` の `BrandOpening` のまま（`op_ed_bookends` ゲート・フォーク禁止）。
`OpeningYoung` は**独立したタイトルバンパー成果物**（`out/young_opening.mp4`。Shorts/予告/SNS 用）。**本編に ffmpeg で焼き込まない。**

## 10.2 Composition 設定
| 項目 | 値 |
|---|---|
| `id` | `OpeningYoung` |
| 解像度 / fps / duration | **1920×1080 / 60 / 180**（=3.0秒） |
| component | `remotion/src/compositions/OpeningYoung.tsx` |

```tsx
import {OpeningYoung, openingYoungDurationInFrames} from './compositions/OpeningYoung';
import youngOpeningProps from '../props/young.json';
<Composition id="OpeningYoung" component={OpeningYoung}
  width={1920} height={1080} fps={60}
  durationInFrames={openingYoungDurationInFrames(60)} defaultProps={youngOpeningProps}/>
```

**依存:** `@remotion/motion-blur`（未導入時のみ `cd remotion && npm i @remotion/motion-blur`）。
**`remotion/remotion.config.ts`** は既に正典値（png / h264 libx264 / CRF16 / yuv420p / bt709 / aac 320k / 全コア並列 / angle）。**一致確認のみ・書き換えない。**

## 10.3 秒数ベースのタイムライン（fps=60・フレーム直書き禁止・全て `Math.round(fps*秒)`）

| 秒 | 起きること | 手法 |
|---|---|---|
| 0.00–0.40 | L1 グラデ背景 opacity 0→1・**同時に scale 1.08→1.00（`Easing.out(Easing.cubic)`）** | interpolate（opacity 単独禁止・scale と併用） |
| 0.10 | ロゴ（`hasLogo`）左上に spring・scale 0.4→1.0・opacity 0→1 | spring `damping:14,mass:0.9` |
| 0.15–0.25 | L2 グリッド reveal（opacity→0.18）＋ translateY 0→48px | spring `damping:200,mass:1` + `Easing.inOut(Easing.sin)` |
| 0.25 | L3 グロー scale 0.6→1.15 / opacity 0→0.85 | spring `damping:18,mass:1.2`（併用） |
| 0.30–0.86 | L4 主役タイトルが1文字ずつ切れ上がり（translateY 110%→0）＋ opacity。スタッガー **2f/文字**。全体を `Trail(layers=6,lagInFrames=1.2,trailOpacity=0.45)` で包む | spring `damping:16,mass:1` |
| 0.55–1.15 | L2b **戸口のスリット**（中央から縦の細い光線 `scaleX 0→1`＋opacity 0→0.5・「割れる→閉じる扉」のモチーフ） | spring `damping:22,mass:1.1`・`transformOrigin:'center'`・**motionBlur** |
| 0.95–1.35 | L5a アクセント下線 左から `scaleX 0→1` | spring `damping:16,mass:0.8`・`transformOrigin:'left center'` |
| 1.10–1.55 | L5b サブタイトル translateY 24→0 + opacity 0→1 | spring `damping:20,mass:1`（併用） |
| 1.55–3.00 | settle→ホールド。**完全静止フレーム無し・フェードアウトしない** | — |

> **等速線形を1箇所も使わない。opacity 単独の演出を1箇所も作らない**（全 opacity が translateY/scale/scaleX と対）。

## 10.4 props 型と値
```ts
export type OpeningYoungProps = { title:string; subtitle:string; accent:string; hasLogo:boolean };
```
`remotion/props/young.json`: `{ "title":"THE WRONG HOUSE", "subtitle":"HUDSON V. MICHIGAN", "accent":"#3B7DD8", "hasLogo":true }`
`remotion/props/young_short.json`: `{ "title":"WRONG DOOR", "subtitle":"WHAT THE LAW OWES YOU", "accent":"#3B7DD8", "hasLogo":false }`
> `subtitle`/`title` も §2 の R-FORBID/R-FACE/R-DOC 検査対象（`remotion/props/young*.json`）。ルート背景は INK 近黒 `#0A0A0C`。accent は EP41 の gold 系と分離した warrant-blue `#3B7DD8`（DESIGN §12・レーン分離）。
> **`no-knock` を subtitle に書かない（C-2）。**

## 10.5 量産
```bash
cd remotion && npm run studio     # OpeningYoung を 0→180f スクラブして §10.3 の各時刻を目視
npx remotion render OpeningYoung out/young_opening.mp4 --props=./props/young.json
npx remotion render OpeningYoung out/young_short_op.mp4 --props=./props/young_short.json
```

---

# 11. サムネ3案（`YoungThumbnails.tsx`・`<Still>` 1280×720・Root に `Thumb-young-01..03`）

**共通要件:** 見出し全て大文字・4語以内・320pxで判読 / **実在人物の肖像禁止（R1）** / INK 黒 `#0A0A0C` bg + warrant-blue `#3B7DD8` /
背景は body 静止画のうち `also_thumb==true` の6枚（S05/S30/S60/S63/S74/S84・象徴オブジェのみ・C-5/C-6。**サムネ専用の分類は無い**） / `thumbnail_visibility`（luma平均≥33＋コントラスト）を通す。目標CTR 6%+。3案は6枚から選ぶ。
**禁止語（no-knock/unconstitutional/she changed the law）を出さない（R-FORBID）。**

- **T1「割れた戸口」（最推奨）:** 割れる戸口＋一条の光（顔なし・S05 系）。文字 **`THE WRONG HOUSE`**（3語）。`WRONG` を warrant-blue。
- **T2「5-4」（数字勝負）:** 大理石の列柱を暗く落とし（S60 系）、前面に **`5–4`**（大）＋ **`STILL A COMMAND`**（下）。数字は F15 の検証済み値のみ。
- **T3「小切手」（尊厳）:** 机上の小切手＋空白の過失欄（illegible・S74 系）。文字 **`PAID. NOT ANSWERED.`**（3語）。`NOT` を warrant-blue。**"no finding of fault" の視覚化＝C-1。**

**A/Bタイトル候補（`09_package`・60字以内・二人称）:** 台本のとおり
- **A:** `Police Raided the Wrong House. What Does the Law Owe You?`
- **B:** `They Broke Down Her Door by Mistake. The Law Shrugged.`

**固定コメント** `09_package/pinned_comment.v001.txt`（§2 の R-LEDGER/R-ATTRIB/R-FORBID/R-SETTLEMENT 検査対象。台帳事実のみ）:
```
Two things this case turns on:
(1) Police executed a valid search warrant at the wrong address. The man they wanted
    lived elsewhere, on a court-ordered ankle monitor. She said "the wrong house" again and again.
(2) In Hudson v. Michigan (2006), the Supreme Court held 5-4 that a knock-and-announce
    violation does not get evidence thrown out. Knock-and-announce is still a command of the
    Fourth Amendment; the remaining remedy is a civil suit under Section 1983.

The city paid 2.9 million dollars, reported approved 48-0 — a settlement, not a finding of fault.
If it were your door — what should the law owe you?
```

---

# 12. 本編コンポジション登録（`remotion/src/Root.tsx`・`Ep38KidsForCash` の形を踏襲）
```tsx
import youngFilm from './data/young_film.json';
<Composition id="Ep42Young" component={CaseFilm}
  durationInFrames={caseFilmDurationInFrames(youngFilm as unknown as FilmData, BRAND.video.fps)}
  fps={BRAND.video.fps} width={BRAND.video.width} height={BRAND.video.height}
  defaultProps={{ data: youngFilm as unknown as FilmData, seriesLabel: 'PRIME DOCUMENTARY',
    title: 'Police Raided the Wrong House',
    subtitle: 'What does the law owe you? Almost nothing it has to.' }}/>
```
> `remotion/src` に現在 `young` の文字列が無いこと（衝突しない）を確認してから追記。`title`/`subtitle` も §2 検査対象（R-FORBID）。

---

# 13. 受入（自分で exit 0 を確認してから完了報告）
```bash
cd C:\Users\aab15\Documents\prime-documentary ; PY=./.venv/Scripts/python.exe

# 0. 語数（最優先・課金前に落とす）
$PY scripts/check_script_length.py episodes/_planning/EP42_young_script.en.v001.md --json   # 2,140語 / wpm178.1

# 1. 事実性/6制約（EP42固有）
$PY scripts/check_young_facts.py --json

# 2. 契約バリデータ
$PY scripts/validate_young_beats.py
$PY scripts/check_young_asset_manifest.py --assets episodes/PD-2026-042-young/05_visuals/asset_manifest.v001.json

# 3. ★5ゲート（animation_mix を忘れるな・入力は --ep / 位置引数を厳守）
$PY scripts/check_asset_reuse.py    remotion/src/data/young_film.json
$PY scripts/check_motion_density.py --ep PD-2026-042-young
$PY scripts/check_animation_mix.py  --ep PD-2026-042-young
$PY scripts/check_caption_breaks.py episodes/PD-2026-042-young/08_edit/captions.final.v001.srt

# 4. 水増し・レンダ前プリフライト
$PY scripts/check_padding.py --ep PD-2026-042-young --json
$PY scripts/preflight_render_gate.py --ep PD-2026-042-young

# 5. 本編レンダ（slim public・並列4）→ BGM → AEカード合成
cd remotion
npx remotion render Ep42Young out/young.mp4 --public-dir=public_slim --concurrency=4
#   public_slim は young_film.json が参照する素材（+ 各 <stem>_depth.png）だけを含む slim public。
#   無ければ referenced paths を public_slim/ にコピーして作る（remotion/public/young 本体を痩せさせない）。
cd ..
$PY scripts/build_young_bgm.py
$PY scripts/ae/composite_young_hero.py

# 6. 本編最終受入（episode番号は★位置引数・--ep ではない）
$PY scripts/check_final_acceptance.py 42 \
  --render episodes/PD-2026-042-young/08_edit/young_final_bgm.v003_ae.mp4 --emit-receipt
```

| ゲート | EP42 目標値 |
|---|---|
| `check_script_length` | 総語数 **2,140** / `wpm 178.1` / narration **720.9s** |
| `check_asset_reuse` | factory≤1 / motion≤2 / still≤2 / first-use **0.8584**（floor0.70） |
| `check_motion_density` | density **3.08**/min / coverage **27.7%** / variety 12+（floors 2.5 / 0.25 / 3・beats **≥31**） |
| `check_animation_mix` | still-share **0.4469(cut)/0.4203(frame)**（cap0.45）/ motion-cov **0.5531+**（floor0.45） |
| `check_caption_breaks` | 行末機能語0 / 孤立キュー0 / hard split 0 |
| `check_young_facts` | violations = 0（台帳照合・5-4・帰属・6制約・R-FORBID・R-SETTLEMENT） |
| runtime band | 11.5–12.5分（narration 720.9s + bookends） |
| factory クリップ | ≥24本 → **93本** |
| image_resolution | 全静止画 長辺 ≥3840px |
| thumbnail | 3案 @1280×720 + selected luma≥33 |
| op_ed_bookends | `BrandOpening`/`BrandEndcard` を import（フォーク禁止） |

**全て exit 0 でなければ `package_ready` にしない。自己申告QCは無効。QC基準を書き換えて通すのは禁止。**

## 13.1 完成後の全編アイボール（**1フレーム判定禁止＝EP39-41 実害**）
`young_final_bgm.v003_ae.mp4` を **0→末尾まで通しで実視聴**し、以下を確認してから完了報告:
- 紙芝居感が無い（still が連続していない・footage が体感で過半）
- AEカード8枚が全て焼き込まれ数値が台帳と一致（`no-knock`/`unconstitutional`/`she changed the law` がどこにも無い）
- $2.9M・48-0 のカードに "reported"/"no finding of fault" が読める（C-1）
- 10–4 に "voted down/rejected"、ENDING に "still legal"（C-3）
- 5-4 は Supreme Court に正しく帰属、"still a command" が Scalia 帰属（C-4）、Part IV=4票の注記あり
- Young の顔・身体・着衣なし描写が無い（象徴のみ・C-6）／ Booker Hudson が人物化されていない（C-5）
- 生成ビジュアル表示中は `AI-assisted visualization` が右下に常時（**AEカード8枚の表示中も**開示が見える＝カード共通スタックに焼かれている・R1・§7.3/§7.9）
- 音ズレ・字幕ズレ・尺差（base と <=0.5s）が無い

---

# 14. 絶対にやらないこと
- **EP39 / EP40 / EP41 のファイル・素材に触らない**（読み取りのみ可）。レーンを分離する。
- **スレッドAの所有ファイル（§0.2.1）に書かない**（`05_visuals/` `05_stock/` `remotion/public/young/` `H:\...\ai\young\`）。**B の provenance は `04_scenes/young_build_manifest.v001.json` に書く。**
- **設計書 / `EP42_young_CODEX_A_*` / PD-2026-039〜041 に触らない。**
- **課金ジョブを起動しない**（ElevenLabs TTS / 課金画像生成API / YouTube アップロード）。narration_index はスタブで着手。
- **公開済み・出荷済み mp4 を上書き・再レンダしない**（出力は必ず `_v003_ae`）。
- **台帳（§2）に無い数値を焼かない**（$580,000 の再発防止）。不明値は `verified:false` でカード除外。
- **`FigureSpec` の `kind` を推測で書かない**（§6.2 の実在小文字値のみ。大文字名は無言で消える。`comparebars` は存在しない）。
- **`--variants` という語を書かない**（1シーン1枚・バリエーション0＝ブリーフ§1。SDXL は A の領分で 1 固定）。
- **`no-knock` / `unconstitutional` / `she changed the law` をどの出力にも書かない**（C-2/C-3・R-FORBID）。**和解を責任認定として提示しない**（C-1・R-SETTLEMENT）。
- **スタブと本番でコードパスを分岐させない**（§0.2）。
- **スペック数値（226 cuts / still85 / factory93 / motion16 / distinct194 / first-use0.8584 / still-share0.4469 / figures≥31 / 720.9s / 2,140語 / 48シーン）を変えない。**
- **実在しないスクリプト名を書かない**（新規は §0.3 の一覧のみ・複製元を明記）。**PowerShell 経由で正規表現/エスケープを生成しない**（`\b` バックスペース化の実害）。
