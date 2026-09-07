# EP48 glover — Codex スレッドB「実装」引き継ぎプロンプト v001

> **このファイルは単体で完結している。他のファイルを読まなくても着手できる。**
> 並行して走っていたスレッドA（素材生成）のファイル `EP48_glover_CODEX_A_*.md` は**読まない**（Aは既に FROZEN・接続点は §3 のマニフェスト1ファイル）。
> 設計書 `EP48_glover_DESIGN*.md` も**読まない**（必要な数値・AEデッキ・figures 配分はすべて本書に転記済み）。
> `EP48_glover_PRODUCTION_SPEC.v001.json` の数値は本書に転記済み。**あなたはこれを書き換えない。**

```
あなたは Prime Documentary（YouTubeドキュメンタリーチャンネル）の制作エンジニアです。
リポジトリ: C:\Users\aab15\Documents\prime-documentary
Python:     C:\Users\aab15\Documents\prime-documentary\.venv\Scripts\python.exe
メディア:   H:\pd-media
担当:       EP48 / Episode ID: PD-2026-048-glover / slug: glover
Composition id（本編）: Ep48Glover
```

**題材:** *Kansas v. Glover*, **589 U.S. ___ (2020)（No. 18-556・decided 2020-04-06）** と **Charles Glover Jr.**（**存命の私人 = R2・免許取消中の運転で有罪**）。
Douglas County, Kansas の保安官補（Deputy Mark Mehrer）が、走行中のピックアップのプレートを照合しただけで、登録者 Glover の免許が **取消（REVOKED）** と分かり、**運転者を一切確認せずに** そのままトラックを停止した。最高裁は **8-1** でその停止を **合憲（UPHELD・第4修正に反しない）** とした。
本作の主題は「**あなたの車・その停止の合法性**」であって、Glover を美化しない。核心は「**登録者が運転していると推認できる情報しかなく、それを打ち消す情報が officer に無い場合、その停止は合理的（reasonable suspicion）**」という**狭い**判示であり、**推認は打ち消す情報があれば消える**（60代の登録者なのに20代が運転＝一目で別人なら推認消滅）。

> **★正確性6制約が全出力を律する（§2）。** 停止を **illegal / unconstitutional / struck down** と**書かない**（合憲＝UPHELD 8-1）・**「警察はどんな車でも停められる／プレート照合だけで誰でも停められる」と書かない**（過大化＝R-OVERCLAIM）・**reasonable suspicion（簡易な捜査的 Terry 級停止）であって probable cause ではない**（R-STANDARD）・票決は **8-1**（Thomas 法廷意見／**Kagan 補足＝Ginsburg 同調**が限界／**Sotomayor 単独反対**）・逐語は**検証済みのみ**で正しく帰属（Sotomayor="Justice Sotomayor, dissenting"／Kagan="Justice Kagan, concurring"／Thomas="Justice Thomas, for the Court"）・**Charles Glover の顔/肖像/身体を一切出さない**（象徴のみ）。**★`figures[].kind` に `dochighlight` を1件も入れない**（黒バー/box/underline がバグに見える＝3回指摘）。

---

# 0. このスレッドの責務・境界・完了条件

## 0.1 このスレッド（B）の責務 — **コード律速。実装は全部書ける。**

| # | 作業 | 成果物 |
|---|---|---|
| B-1 | エピソードディレクトリと `manifest.json` | `episodes/PD-2026-048-glover/**` |
| B-2 | 境界契約マニフェストの**消費側**バリデータ | `scripts/check_glover_asset_manifest.py` |
| B-3 | 事実台帳 G-ID と 6制約ゲート（**EP48固有・BLOCKING**） | `scripts/check_glover_facts.py`（**`check_cleveland_facts.py` を複製**） |
| B-4 | `glover_film.json` ビルダ（**manifest→cuts＋beatsheet／footage混在・実素材のみ**） | `scripts/build_glover_film.py`（**`build_cleveland_film.py` or `build_tlo_film.py` を複製**） |
| B-5 | beats バリデータ（AEとRemotionの区間衝突検査＋ledger／6制約） | `scripts/validate_glover_beats.py`（**`validate_cleveland_beats.py` を複製**） |
| B-6 | **構文境界で切る字幕生成器**（実測 narration_index から verbatim） | `scripts/gen_captions_glover.py`（**`gen_captions_cleveland.py` を複製**） |
| B-7 | **After Effects カード**のビルダとコンポジタ | `scripts/ae/build_glover_hero_cards.py`（**FIXED `build_cleveland_hero_cards.py` 複製**）/ `scripts/ae/composite_glover_hero.py`（**`composite_caniglia_hero.py`=EP43 複製**） |
| B-8 | 本編 BGM ミックス（AEカード合成の基底 mp4 を生成） | `scripts/build_glover_bgm_real.py`（**`build_caniglia_bgm_real.py`=EP43 複製・OFF=11.5**） |
| B-9 | Remotion 本編コンポジション登録 `Ep48Glover` | `remotion/src/Root.tsx` |
| B-10 | OP バンパー `OpeningGlover`（fps60/1920x1080/180f） | `remotion/src/compositions/OpeningGlover.tsx` |
| B-11 | サムネ3案 | `remotion/src/compositions/GloverThumbnails.tsx` |
| B-12 | 本編レンダ→BGM→AEカード合成→全ゲート→**全編アイボール** | `episodes/PD-2026-048-glover/08_edit/**` |

> **★このスレッドは「実素材のみ」（ブリーフ§7）。stub/dryrun/placeholder のコードパスを作らない（`grep -riE 'stub|placeholder|dryrun' scripts/*glover*.py` が 0）。** A は FROZEN（§3 の本番マニフェストが実在）・narration_index は実測版が実在する前提で組む。**素材が来ていなければ止めて A/上流に差し戻す**（架空の黒スタブで緑にしない）。

## 0.2 もう一方のスレッド（A・FROZEN）との境界 — **接続点はただ1ファイル。**

```
episodes/PD-2026-048-glover/05_visuals/asset_manifest.v001.json
   ↑ Aが生成（唯一の生産者・FROZEN）        ↓ Bが消費（唯一の消費者・検証者）
```

**Bはこのファイル以外のAの中間生成物を読まない。** このマニフェストは **A(producer)とB(consumer/validator)で counts / role enum / overlay枚数を1バイト単位で共有**する（§3）。

> **★1シーン1枚・バリエーション0（ブリーフ§1）の B 側での意味:** A は同一ショットの `_01/_02/_03` を**作らない**。
> したがってマニフェストの `stills[role="body"]` は **85本すべてが固有プロンプトの distinct**（`counts.still_body==85`）。
> A の `ai_prompts.v001.md` は **still 85行（S01..S85）＋i2v種 16行 = 総生成画像 101枚**（各1回）。**still カット 101本という数字とは別物**（偶然どちらも 101）。
> B は編集上、still を **各最大2回**まで再使用してカット101本を組む（cap 2 の"再利用"であって"バリエーション"ではない）。
> **B は `--variants` という語をどのコマンド・ログにも書かない**（それは A の SDXL 側の概念で、しかも 1 固定）。

### 0.2.1 ファイル所有権（これを破ると並行作業が壊れる）

| パス | 所有 | Bの権限 |
|---|---|---|
| `episodes/PD-2026-048-glover/manifest.json` | **B** | 読み書き |
| `episodes/PD-2026-048-glover/{00_topic,01_research,03_script,04_scenes,06_audio,08_edit,09_package,approvals,events}/**` | **B** | 読み書き |
| `remotion/src/**` `remotion/props/**` | **B** | 読み書き |
| `scripts/*glover*.py` / `scripts/ae/*glover*.py`（§0.3） | **B** | 新規作成 |
| **`episodes/PD-2026-048-glover/05_visuals/**` `05_stock/**`** | **A** | **読み取りのみ。書くな** |
| **`H:\pd-media\assets\ai\glover\**` / `ai_video\glover\**`** | **A** | **読み取りのみ。書くな** |
| **`remotion/public/glover/{img,factory,motion,overlay}/**`** | **A** | **読み取りのみ。書くな** |
| `EP48_glover_DESIGN*.md` / `EP48_glover_CODEX_A_*.md` | **設計/Aスレッド** | **触るな** |
| `EP48_glover_PRODUCTION_SPEC.v001.json` / `EP48_glover_script.en.v001.md` / `EP48_glover_facts.v001.json` | **上流** | **読み取りのみ。書くな** |
| `episodes/PD-2026-039-*/**` … `PD-2026-047-*/**` / それらの素材 | **他エージェント** | **絶対に触るな（読み取りのみ可）** |

> **B は `remotion/public/glover/` に書かない**（A の staging 済み本番素材）。B の provenance/beatsheet は `04_scenes/` に書く（§5.6）。**render 用の `public_slim` staging（§13）は B が作る。**

## 0.3 B が新規作成するスクリプト（これ以外を新規に作らない。既存を改変しない）

| パス | 役割 | 手本（**改変せず読んで複製→パス/定数だけ差し替え**・実在確認済み） |
|---|---|---|
| `scripts/check_glover_asset_manifest.py` | §3.3 消費側バリデータ | `scripts/check_cleveland_asset_manifest.py` |
| `scripts/check_glover_facts.py` | §2 6制約＋台帳（BLOCKING・**正確性ゲート名はこの1つに統一**） | **`scripts/check_cleveland_facts.py`** |
| `scripts/build_glover_film.py` | §5 film.json＋provenance＋beatsheet＋SRT（**実素材のみ・★factory/motion全読込**） | **`scripts/build_cleveland_film.py`**（or `build_tlo_film.py`） |
| `scripts/validate_glover_beats.py` | §7.9 不変条件 | **`scripts/validate_cleveland_beats.py`** |
| `scripts/gen_captions_glover.py` | §8 構文境界字幕生成器 | **`scripts/gen_captions_cleveland.py`** |
| `scripts/ae/build_glover_hero_cards.py` | §7 AEカードビルダ | **`scripts/ae/build_cleveland_hero_cards.py`（=FIXED版）** |
| `scripts/ae/composite_glover_hero.py` | §7.10 コンポジタ（`beats.json` の `film_offset_sec` を読む） | **`scripts/ae/composite_caniglia_hero.py`（=EP43）** |
| `scripts/build_glover_bgm_real.py` | §7.10 基底 mp4（narration＋BGM ミックス・**OFF=11.5**） | **`scripts/build_caniglia_bgm_real.py`（=EP43）** |

> **`build_glover_film.py` の複製時に差し替える定数:** `SLUG="glover"`・`EP="PD-2026-048-glover"`・`DEFAULT_OUT=remotion/src/data/glover_film.json`・`PUB_FILM=remotion/public/glover/film_data.v001.json`・`SECTION_TARGETS`（§5.3）・出力パス群・`expected={"factory":92,"motion":32,"stills":101}`。**ロジック（`public_items()` / `repeated()` / `take()` / `allocate` / `build_figures` / `build_captions`）は1行も変えない。**
> **既存の `build_cleveland_film.py` / `gen_captions_cleveland.py` 等は触らない**（他エピソードが使用中）。EP48用に**新規コピー**する。
> **実在しない複製元名を捏造しない**（`ls scripts/` で確認済み。複製元は上表の実在ファイルのみ）。

## 0.4 完了条件（実素材で、全て緑になったら「実装完了」）

```bash
cd C:\Users\aab15\Documents\prime-documentary
PY=./.venv/Scripts/python.exe

# [B-DONE-1] マニフェスト消費側バリデータ（A の FROZEN 本番マニフェスト相手に通ること）
$PY scripts/check_glover_asset_manifest.py \
  --assets episodes/PD-2026-048-glover/05_visuals/asset_manifest.v001.json

# [B-DONE-2] 字幕（実測 narration の実文から構文境界で生成）
$PY scripts/gen_captions_glover.py \
  --narr episodes/PD-2026-048-glover/06_audio/narration_index.v001.json
$PY scripts/check_caption_breaks.py \
  episodes/PD-2026-048-glover/08_edit/captions.final.v001.srt

# [B-DONE-3] film.json を実マニフェストから組み立てる（footage 混在必須・dochighlight 不使用・★factory92/motion16 全読込）
$PY scripts/build_glover_film.py \
  --assets episodes/PD-2026-048-glover/05_visuals/asset_manifest.v001.json \
  --narr   episodes/PD-2026-048-glover/06_audio/narration_index.v001.json \
  --out    remotion/src/data/glover_film.json

# [B-DONE-4] ★5ゲート全部（--ep 指定・animation_mix を絶対に忘れるな）
$PY scripts/check_asset_reuse.py     remotion/src/data/glover_film.json
$PY scripts/check_motion_density.py  --ep PD-2026-048-glover
$PY scripts/check_animation_mix.py   --ep PD-2026-048-glover
$PY scripts/check_caption_breaks.py  episodes/PD-2026-048-glover/08_edit/captions.final.v001.srt
$PY scripts/check_script_length.py   episodes/PD-2026-048-glover/03_script/script.en.v001.md --json

# [B-DONE-5] 事実性/6制約（＋dochighlight 不使用・quote 逐語帰属）
$PY scripts/check_glover_facts.py --json

# [B-DONE-6] beats 契約（AE区間 と Remotion figures[] が1秒も重ならない）
$PY scripts/validate_glover_beats.py

# [B-DONE-7] AE カードをビルド（二段構成）＋レンダ＋コンポジット（§7.6）
$PY scripts/ae/build_glover_hero_cards.py
"C:/Program Files/Adobe/Adobe After Effects 2026/Support Files/AfterFX.exe" -noui \
  -r "C:/Users/aab15/Documents/prime-documentary/episodes/PD-2026-048-glover/08_edit/ae_hero/glover_hero.jsx"
# → _build_ok.txt を待つ → .aep mtime>.jsx を assert → aerender -project で描画
"C:/Program Files/Adobe/Adobe After Effects 2026/Support Files/aerender.exe" \
  -project "C:/Users/aab15/Documents/prime-documentary/episodes/PD-2026-048-glover/08_edit/ae_hero/glover_hero.aep"
$PY scripts/ae/composite_glover_hero.py

# [B-DONE-8] Remotion Studio で目視
cd remotion && npm run studio
#   → Ep48Glover / OpeningGlover / Thumb-glover-01..03 が出て、実際に動くこと
```

**台本は既に確定済み**（`EP48_glover_script.en.v001.md`・**2,136語・12.0分**・ロック）。本番配置先は
`episodes/PD-2026-048-glover/03_script/script.en.v001.md`（**1バイトも変えずコピー**・整形禁止＝AI臭再発と語数ゲート再計算を招く）。

---

# 1. 実装前に必ず読むファイル（**推測で書くな**）

| パス | なぜ読むか |
|---|---|
| `scripts/build_cleveland_film.py`（or `build_tlo_film.py`） | **複製元。** `public_items()`/`repeated()`/`take()`/`allocate`/`build_figures`/`build_captions` をそのまま踏襲し定数だけ glover に。**★`public_items(manifest,"factory")`・`public_items(manifest,"motion")` を必ず読む（EP45 は factory/motion 配列が空で紙芝居化した実害＝§0.5-1/§5.2）。** |
| `scripts/ae/build_cleveland_hero_cards.py`（**FIXED版**） | **複製元。** `money_keys()`（Python で表示文字列を全事前計算）/ 実測フィット（`sourceRectAtTime`）/ CARDS デッキ構造 / **実装済み6レイアウト＝§7.3** / **REPO path 出力** / **.aep 保存＋二段 aerender** / 完了マーカーをそのまま |
| `scripts/ae/composite_caniglia_hero.py`（EP43） | **複製元。** SKIP4条件（missing / 解像度不一致 / 実測尺不足 / window past end）と ffmpeg フィルタグラフ（overlay/blend）と `film_offset_sec` の読み込みをそのまま |
| `scripts/gen_captions_cleveland.py` | **複製元。** `internal_split()` / `chunk_sentence()` / `NO_DANGLE_END` import をそのまま |
| `scripts/build_caniglia_bgm_real.py`（EP43） | **複製元。** narration＋BGM ミックスで基底 mp4 を作る経路（**OFF=11.5 に差し替え**） |
| `scripts/check_cleveland_facts.py` | **複製元（正確性ゲート）。** 構造ルールの除外実装（`asset_manifest` を R-NUM から除外・`index`/geometry キー除外・`kind!="acttitle"` 条件＝EP45修正）を**そのまま流用**（§2.3） |
| `remotion/src/compositions/CaseFilm.tsx` | `FilmData` 型 / `caseFilmDurationInFrames`（**4項・§5.1.1**）/ `depthSrcOf()` |
| `remotion/src/components/FigureBeats.tsx` | `FigureSpec` の**実在する `kind` 文字列と必須プロパティ**（§6.2・**全小文字**・**`dochighlight` は union に在るが使わない**） |
| `remotion/src/components/Bookends.tsx` | `OPENING_SEC=3.5` / `ENDCARD_SEC=9` / `BrandOpening` / `BrandEndcard` |
| `scripts/check_asset_reuse.py` / `scripts/check_motion_density.py` / `scripts/check_animation_mix.py` / `scripts/check_caption_breaks.py` / `scripts/check_script_length.py` | 通すべき5ゲートの**実際の判定ロジック**（§9） |
| `C:\Users\aab15\Documents\pino-channel\remotion\src\Opening.tsx` | §10 の OP 正典実装 |

---

# 0.5 ★★★ EP39-47 で踏んだ失敗＝最初から防ぐ（本書の全体設計はこの6点を構造で潰している）★★★

1. **紙芝居（最重要・★EP45 の直接死因）** — 静止画100%で組むと `check_animation_mix` が FAIL する。**EP45 は build が manifest の `factory[]`/`motion[]` を空で受け取り、footage が0本で紙芝居化した。**
   → **`build_glover_film.py` は `public_items(manifest,"factory")` が 92本・`public_items(manifest,"motion")` が 16本を返すことを起動時に assert し、0本 or 数不一致なら exit 1 で A に差し戻す。** `check_animation_mix.compute_metrics_from_film()` は film.json の `cuts[]` を **`kind=="img"` → still / それ以外 → footage** と分類する。§5 の cuts は **factory 92 + motion 32 の footage を最初から入れて still-share を cut数ベース 0.4489・frame ベース ~0.42** にする。
2. **AEカードは密度に数えられない** — `check_motion_density` は film.json の `graphics+figures+heroCuts` **のみ**数える。AEカードは ffmpeg 後合成なので**1本も数えられない**。→ §6 で **film.json 側の `figures[]` を 36本**（spec floor 30 に **+6**・`graphics[]=[]`）置く。AEカードは別勘定。
3. **FigureSpec の `kind` は実在の小文字値のみ・必須プロパティ厳守** — 大文字名（`ActTitle`/`QuoteCard`/`VoteTally` 等）は無言で描画が消える。**不正フィールドは render クラッシュ**（§6.2 で実 union の必須プロパティを全数照合）。**★`dochighlight` は union に在るが1本も使わない**（黒バー/box/underline がバグに見える＝3回指摘・R-DOCHL）。
4. **台帳に無い数値を焼くな** — EP40 の生 Codex-B 出力に架空の $580,000 が入って不採用になった実害。→ §2 の事実台帳 G-ID に**検証済み値だけ**を置き、`check_glover_facts.py` が film.json/AE/サムネ/props の全数値を台帳照合する。台帳外・`confidence:medium`（保安官の氏名以外の詳細・車種・プレート番号・手続経緯）の断定は FAIL。
5. **字幕は台本本文と対応** — EP38 で台詞混入・「final」誤称の実害。→ §8 の字幕は **narration_index の実チャンク文をそのまま** verbatim で使う（自作しない）。
6. **レンダー前ゲート＋public_slim staging** — build 後に5ゲートを**全部**通す（animation_mix を忘れるな）。**★render 前に `public/glover` → `public_slim/glover` へ全メディア（img/factory/motion/audio/overlay）をコピーする**（EP45 は `public_slim` が空でレンダが素材欠落した実害・§13）。**public/glover と public_slim/glover の双方で media 解決0 missing を確認してからレンダ。**

---

# 2. ★ EP48固有の正確性6制約・事実性ロック（`scripts/check_glover_facts.py`・BLOCKING）

> **この節に違反した成果物は、他が全て完璧でも出荷不可。** 検査対象は film.json の figures/captions、AE beats、
> サムネ、props、固定コメント、`03_script/script.en.v001.md`、（存在すれば）マニフェストの tags/caption_hint/qc.notes の**全文字列と全数値**。
> **正確性ゲートはこの1本に統一（`check_glover_facts.py`）。DESIGN/CODEX_A も同名を参照する（別名を作らない）。** 出力 `09_package/facts_lock.v001.json`。

## 2.1 正確性6制約（全出力に適用・違反は BLOCKER）

| # | 制約 | 許可される表現 | 禁止 |
|---|---|---|---|
| C-1 | **停止は合憲＝UPHELD（8-1）。「違法」化しない** | 「the Court UPHELD the stop」「constitutional」「the stop did not violate the Fourth Amendment」「the Court let the stop stand」「the brief stop was allowed」 | 「the stop was illegal」「unconstitutional stop」「the Court struck it down」「the Court banned this」「police can't stop you for that」 |
| C-2 | **推認は打ち消す情報があれば消える（狭い判示）** | 「narrow」「reasonable ONLY absent contrary information」「dissolves the moment the officer can see the driver is not the owner」「a man in his sixties / a woman in her twenties」 | 「police can stop any car at any time」「always reasonable」「the owner is definitely driving」 |
| C-3 | **reasonable suspicion（Terry 級の簡易な捜査的停止）≠ probable cause** | 「reasonable suspicion」「a brief investigative stop」「less than probable cause」「a sensible, fact-based reason to look closer」 | 「probable cause required」「the officer needed probable cause」「proof」「certainty」を停止の要件として書く |
| C-4 | **票決 8-1・中立帰属** | 「eight to one」「8 / 1」「Thomas maj」「Kagan concurrence, joined by Ginsburg」「Sotomayor, the lone dissent」 | 7-2/6-3 等の誤票決／党派断定／反対を法廷意見に混ぜる |
| C-5 | **Charles Glover＝R2・象徴のみ・美化しない** | 事件主体としての名（"Charles Glover was the driver"）。ビジュアルは二車線のカンザスの道・アイドリングするパトカー・通過するピックアップ・ナンバープレート・ダッシュのラップトップに打たれたプレート・REVOKED 画面・点灯するライトバー・免許証（取消の判子）・登録票・天秤・"所有者≠運転者"の60代 vs 20代のシルエット・最高裁列柱/9席 | 顔・肖像・身体・人物化／`Glover` 直後60字の `face`/`portrait`/`likeness`／彼の犯罪性を原被疑事実（免許取消運転）以外に広げる／暴力・crime scene |
| C-6 | **数値は台帳一致・過大化しない・medium はヘッジ** | 画面数値は §2.2 の台帳のみ。`8-1`・`2020`（=判決年 April 6, 2020）・`589 U.S.`・`Fourth (4)`・`No. 18-556`（任意）。**保安官の詳細・車種（1995 Chevy）・プレート番号（295ATJ）・手続経緯は confidence:medium → 画面に断定で出さない** | 台帳外の数字／プレート番号・車種年式を確定カードに焼く／「stop any car」 |
| R1 | **実在人物の顔・肖像を生成しない** | 全生成ビジュアル表示中は `AI-assisted visualization`（右下）常時／概要欄1行AI開示 | 認識可能な人物・読める偽公文書 |
| ★DH | **dochighlight 不使用** | 判読ハイライトの意図は `quote`/`stat`/`lowerthird`/`kinetic` で代替 | `figures[].kind`/beats/レイアウト名に `dochighlight`/`DOCHIGHLIGHT` を1件でも出す |

**★禁止語（`check_glover_facts.py` が全文字列を case-insensitive 部分一致で検査。1件でも FAIL）:**
`the stop was illegal` / `illegal stop` / `unconstitutional stop` / `the stop was unconstitutional` / `the court struck it down` / `struck down the stop` / `the court banned` /
`police can stop any car` / `stop any car at any time` / `police can stop anyone` / `stop any vehicle` / `probable cause required` / `the officer needed probable cause` / `needed probable cause to stop` /
`the majority dissented` / `sotomayor concurred` / `kagan dissented` / `thomas dissented`.
> **★重要な設計注意:** 台本本文（＝字幕 verbatim）には「Never call it illegal or unconstitutional」「it is not the frightening version, where police can stop anyone for anything」「the police can stop your car for no reason at all, remember that it is not quite true」など
> **否定/正確文脈の語**（`illegal`/`unconstitutional`/`stop anyone`/`any car`）が**否定文の中で**含まれる。上の禁止語リストは**それらと衝突しない断定形だけ**（`the stop was illegal`・`police can stop any car`＝主語付き断定）を選んである。**禁止語リストに `illegal`/`unconstitutional`/`any car` の単語単独を足すな**（字幕 verbatim を巻き込んで false FAIL する）。C-1/C-2/C-3 の**枠付き/帰属**は下の**文脈ルール**（R-OVERCLAIM/R-STANDARD/R-QUOTE）で捕える。

## 2.2 事実台帳 G-ID（`03_script/glover_facts.v001.json`・**Bが `EP48_glover_facts.v001.json` の ledger G01–G19 から転記して作る**）

**スキーマ版:** `glover_facts.v1`。各 G-ID は `{"value":..., "unit":..., "verified":bool, "confidence":"high|medium", "claim_id":"", "attribution":"", "quote":""}`。
**ledger に裏付けのある値だけ `verified:true`。confidence:medium（`G02` の保安官氏名以外の車種/プレート詳細・`G06` charge 詳細・`G07` 手続経緯）は `画面に出さない`＝figures/AE/サムネ/props に焼かない（narration verbatim 内のみ許可）。**

| G-ID | 内容 | 使う場所 | claim | conf |
|---|---|---|---|---|
| G01 | Charles Glover Jr.＝**R2 存命私人**・登録者かつ当日の運転者・免許取消中の運転で有罪・**顔/肖像なし・象徴のみ** | fig lowerthird（名のみ）/ AE 背景（象徴） | G01 | high |
| G02 | 保安官補が**ルーティンでプレート照合**（Douglas County, Kansas）・違反は未目撃・随意の行為 | fig routemap/lowerthird（Deputy Mark Mehrer — Douglas County Sheriff）/ AE 背景 | G02 | high（氏名）/ medium（車種・プレート） |
| G03 | 照合ヒット＝登録者の**Kansas 免許 REVOKED**（重大/反復違反後・単なる suspension とは別） | fig kinetic/lowerthird / AE 背景 | G03 | high |
| G04 | 保安官は**運転者を確認せず**・違反も未目撃・**登録者が運転していると推認して停止** | fig mechanism:faultsplit/compbars / caption | G04 | high |
| G05 | 運転者は実際に Glover だった（推認は当たった）が、**停止時点では未確認** | fig compbars / caption | G05 | high |
| G06 | charge＝driving as a habitual violator（免許取消運転）・事実 stipulated・suppression を申立 | narration のみ（medium） | G06 | medium |
| G08 | 争点＝**登録者の免許取消という事実だけ・打ち消す情報が無い状況**で、登録者=運転者と推認するのは合理的か | fig acttitle/compbars / AE od01 | G08 | high |
| G09 | **標準＝reasonable suspicion（brief investigative / Terry stop）・probable cause ではない**。逐語比較 "considerably less than proof of wrongdoing by a preponderance of the evidence, and obviously less than is necessary for probable cause" | fig probablecause/compbars/quote / AE rs01 | G09 | high |
| G10 | **HOLDING（逐語・Thomas）** "When the officer lacks information negating an inference that the owner is driving the vehicle, the stop is reasonable."＝停止は合憲・UPHELD | fig quote / AE（帰属） | G10 | high |
| G11 | 多数意見の論拠＝**commonsense inference**（運転者=登録者は日常的に合理的）・certainty 不要・取消免許が理由 | fig brightline/compbars / AE 背景 | G11 | high |
| G12 | **NARROWNESS（逐語）** "We emphasize the narrow scope of our holding."＋例（60代の登録者なのに20代の運転者なら推認消滅） | fig mechanism:closingdoor / AE od01 | G12 | high |
| G13 | 票決 **8-1**（Thomas maj／**Kagan concurrence + Ginsburg**／**Sotomayor lone dissent**）・中立 | fig votetally/stat/numberticker / AE v01 | G13 | high |
| G14 | **Kagan 補足（逐語）** revoked≠suspended・一目で別人なら推認消滅。"...Consider, for example, if Kansas had suspended rather than revoked Glover's license." 帰属＝**concurring** | AE k01（帰属）/ narration | G14 | high |
| G15 | **Sotomayor 反対（逐語・opening）** "In upholding routine stops of vehicles whose owners have revoked licenses, the Court ignores key foundations of our reasonable-suspicion jurisprudence and impermissibly and unnecessarily reduces the State's burden of proof." 帰属＝**dissenting** | fig quote / AE（帰属） | G15 | high |
| G16 | **Sotomayor 反対（逐語）** "The consequence of the majority's approach is to absolve officers from any responsibility to investigate the identity of a driver where feasible." 帰属＝**dissenting** | narration / quote（任意） | G16 | high |
| G17 | **Sotomayor 反対（逐語）** "The majority today has paved the road to finding reasonable suspicion based on nothing more than a demographic profile." 帰属＝**dissenting** | AE q01 / narration | G17 | high |
| G18 | 引用＝**Kansas v. Glover, 589 U.S. ___ (2020), No. 18-556, decided April 6, 2020**・reversed & remanded | fig lowerthird/numberticker / AE d01 | G18 | high |
| G19 | **NO-OVERCLAIM ロック** reasonable suspicion・狭い・打ち消す情報で消滅・「any car」ではない | fig statemap/kinetic / caption | G19 | high |

> **数値の許可集合（R-NUM・narrative figure のみ対象）:** `4（Fourth）/ 6（April 6）/ 8 / 1（8-1）/ 18 / 556（No. 18-556）/ 589（589 U.S.）/ 2020`。**これ以外の年・件数・金額・車種年式・プレート番号が figures/AE/サムネ/props に出たら FAIL。** `1995`（車種年式・medium）・`295`（プレート・medium）は**画面禁止**（narration には出て来ない）。`60/20` の代わりに **"sixties"/"twenties"（語）** を使う（数字を焼くと R-NUM に当たるため語で書く）。

## 2.3 `check_glover_facts.py` の検査（exit 0=PASS / 1=FAIL / 2=スキーマ不一致）

**★複製元 `check_cleveland_facts.py` の構造除外を1行も削らない（EP45修正）:**
- `asset_manifest*.json` は **R-NUM の対象から除外**（`if not path.name.startswith("asset_manifest")` で構造カウント 85/16/92/12 を巻き込まない）。
- `start/end/dur/fps/width/height/frames/duration_sec/x/y/index` キーは**構造値**として R-NUM スキップ（`acttitle` の `index`・`pins[].x/y`・`compbars`/`bar` の item `value`＝チャート高さ等の幾何）。
- 文脈ルールは `kind != "acttitle"` のとき発火（幕頭タイトルを巻き込まない）。

**検査対象ファイル（この一覧をハードコード。存在するものだけ検査し、無いものは `skipped[]` に必ず明記）:**

```
episodes/PD-2026-048-glover/03_script/script.en.v001.md
episodes/PD-2026-048-glover/03_script/glover_facts.v*.json
episodes/PD-2026-048-glover/08_edit/ae_hero/beats.json
episodes/PD-2026-048-glover/09_package/*.json        （title / description / thumbnail headlines）
episodes/PD-2026-048-glover/09_package/*.txt         （固定コメント・description.txt）
episodes/PD-2026-048-glover/05_visuals/asset_manifest*.json  （tags / caption_hint / qc.notes・★R-NUM 除外）
remotion/src/data/glover_film.json                   （figures[].text / figures[].lines[] / figures[].kind / captions[] の全文字列と数値）
remotion/props/glover*.json                          （title / subtitle）
```

- **R-FORBID（最優先）** — §2.1 の禁止語（主語付き断定形）が対象文字列に出たら即 FAIL。**`illegal`/`unconstitutional`/`any car` の単独単語を禁止語に足さない**（字幕 verbatim を巻き込む・§2.1 注意）。
- **R-OVERCLAIM（C-2/C-6・BLOCKING）** — 停止の射程を語る payload に「police can stop any car / anyone / any vehicle」「always reasonable」「the owner is definitely driving」が出たら FAIL。**「8 / 1」を出すカードは "narrow" もしくは "the stop stands / upheld / constitutional" を同一 payload に持つ**（過大化と読ませない）。judgment を語る payload には "narrow" もしくは限界（"unless the officer knows otherwise" / "dissolves") を伴う。
- **R-STANDARD（C-3・BLOCKING）** — 標準を語る payload（`reasonable suspicion` を含む、または停止の要件を述べる）に `probable cause required` / `needed probable cause` / `proof` / `certainty`（停止の要件として）が出たら FAIL。reasonable suspicion は "less than probable cause" として枠付ける。
- **R-VOTE（C-4）** — 票決を出す payload の数は **8 と 1**（`8-1`/`8 / 1`/`eight to one`）のみ。6-3/7-2 等が出たら FAIL。反対を Court/majority に帰属したら FAIL（`sotomayor` かつ `for the court`/`majority` 帰属で FAIL）。
- **R-QUOTE（C-2/C-4・R-ATTRIB・BLOCKING）** — `quote[].attribution` は非空・逐語のみ（要約を引用符に入れない）。許可対応表:
  ```python
  APPROVED_QUOTES = {
    # G10 HOLDING（多数意見・逐語）
    "when the officer lacks information negating an inference that the owner is driving the vehicle, the stop is reasonable":
        "Justice Thomas, for the Court",
    # G15 Sotomayor 反対（opening・逐語）
    "in upholding routine stops of vehicles whose owners have revoked licenses, the court ignores key foundations of our reasonable-suspicion jurisprudence and impermissibly and unnecessarily reduces the state's burden of proof":
        "Justice Sotomayor, dissenting",
    # G16 Sotomayor 反対（逐語）
    "the consequence of the majority's approach is to absolve officers from any responsibility to investigate the identity of a driver where feasible":
        "Justice Sotomayor, dissenting",
    # G17 Sotomayor 反対（逐語・AE q01）
    "the majority today has paved the road to finding reasonable suspicion based on nothing more than a demographic profile":
        "Justice Sotomayor, dissenting",
    # G14 Kagan 補足（逐語）
    "i would find this a different case if kansas had barred glover from driving on a ground that provided no similar evidence of his penchant for ignoring driving laws. consider, for example, if kansas had suspended rather than revoked glover's license":
        "Justice Kagan, concurring",
  }
  ```
  **Thomas 逐語に `for the court`/`majority` 以外、Sotomayor 逐語に `dissent`/`dissenting` 以外、Kagan 逐語に `concur`/`concurring`/`concurrence` 以外の帰属が付いたら FAIL。** 上表に無い文字列を引用符（`quote`/`main` に "..."）で "verbatim" として出したら FAIL（捏造引用禁止・C-5/BLOCKER5）。
- **R-FACE（C-5/R1）** — `has_readable_text`/`has_identifiable_face`/`has_human_body` が true の項目は `role=="reject"`。`ai_prompts.v001.md` 正プロンプトの `portrait`/`face of`/`likeness`/`Charles Glover`（人物として）/`his body`/`mugshot`/`crime scene` は FAIL（ネガティブでの使用は可）。`Glover` 直後60字の `face`/`portrait`/`likeness` で FAIL。生成ビジュアル区間の `AI-assisted visualization` 欠落・`description.txt` の AI 開示行欠落で FAIL。
- **R-NUM（C-6・narrative のみ）** — figures[] の `value`（`stat`/`numberticker`）到達値、`votetally` の `majority`/`dissent`、`timeline` events[].year、AE `beats[].value`/`beats[].main`/`beats[].hero`、サムネ数字に現れる**あらゆる数値**は §2.2 許可集合 `{4,6,8,1,18,556,589,2020}` に**完全一致**必須。**`1995`（車種年式）・`295`（プレート）が figures/AE/サムネ/props に出たら FAIL**（medium・画面禁止）。**★`asset_manifest*.json` は R-NUM 対象外**（構造カウント 85/16/92/12 の false-positive 回避＝EP45修正）。**★`compbars`/`bar` の item `value`（チャート高さ）と `pins[].x/y` は構造値として R-NUM スキップ**（§2.3 除外）。
- **R-HEDGE（C-6）** — `confidence:medium` の G-ID（G02 の車種/プレート詳細・G06 charge 詳細・G07 手続）を `verified:true` かつ画面焼き込みしたら FAIL。断定可は **8-1（G13）・2020/April 6（G18）・589 U.S. ___ / No. 18-556（G18）・Fourth（G09/G08）** のみ。
- **R-DOCHL（★DH・BLOCKING）** — `glover_film.json` の `figures[].kind` に `dochighlight` が1件でも出たら FAIL
  （`grep -c '"kind"[[:space:]]*:[[:space:]]*"dochighlight"'` が 0 でなければ FAIL）。`beats.json`/レイアウト名にも `dochighlight`/`DOCHIGHLIGHT` を出さない。
- **R-DATE** — 判決日 **2020-04-06** と cite（589 U.S. / No. 18-556）を年として取り違えない。18/556 を年に混同しない。

**出力:** `episodes/PD-2026-048-glover/09_package/facts_lock.v001.json`（`{"pass":bool,"violations":[{"file","rule","line","excerpt"}],"skipped":[...]}`）。
**`pass:true` でない限り `check_final_acceptance.py` に進んではならない。** **CLI:** `--json`。対象ファイル未生成はスキップして必ずログに出す（「無いから通した」を黙るな）。

---

# 3. ★境界契約: `asset_manifest.v001.json`（Aから受け取る唯一のファイル・FROZEN）

## 3.1 スキーマ（**Aが生成する。Bはこの形を前提に読む・A↔B 1バイト一致**）

**スキーマ版:** `glover_assets.v1`（固定文字列。異なれば **exit 2**）。
EP48 spec の点数に一致: **still_body 85 / still_i2v_source 16 / motion 16 / factory 92 / overlay 12**。
**★サムネは独立の分類を持たない。** body 85枚のうち**6枚**に `also_thumb:true` を立てて流用する（**`role=thumb`/`still_thumb` を作らない**・サムネ用 count キーも無い・§11）。
**このスキーマ・`counts` キー・`role` enum・`overlay` 枚数は CODEX_A（生産者）の出力と1バイト単位で同一。**

- **`role` enum（固定・3値のみ）:** `"body"` | `"i2v_source"` | `"reject"`。**`thumb`/`still_thumb` を作らない。**
- **`counts`（固定キー・確定値）:** `{ "still_body": 85, "still_i2v_source": 16, "motion": 16, "factory": 92, "overlay": 12 }`。

```jsonc
{
  "schema_version": "glover_assets.v1",
  "episode_id": "PD-2026-048-glover",
  "slug": "glover",
  "generated_at": "<ISO8601>",
  "producer": "scripts/build_glover_asset_manifest.py",
  "is_stub": false,
  "counts": { "still_body": 85, "still_i2v_source": 16, "motion": 16, "factory": 92, "overlay": 12 },

  "stills": [
    { "asset_id": "GLV-S01", "scene_id": "S01", "role": "body",
      "also_thumb": false,                     // body から6枚だけ true（§11 の6 asset ID・追加生成しない）
      "act": 0,                                // 0=HOOK/OPENING, 1..3=幕, 5=ED
      "public_path": "glover/img/S01.png",     // ★Bが cuts[].src に入れる値（1シーン1枚＝固有プロンプト・_01 等の接尾なし）
      "depth_path": "H:/pd-media/assets/ai/glover/S01_depth.png",  // role=="body" は実在必須
      "width": 3840, "height": 2160,
      "sha256": "...", "tags": ["two_lane_kansas_road","patrol_car","symbolic"], "caption_hint": "a two-lane Kansas road at dusk, a patrol car idling, no people",
      "source": "ai_codex", "commercial_use": "allowed", "ai_disclosure_required": true,
      "qc": {"reviewed": true, "on_theme": true,
             "has_readable_text": false, "has_identifiable_face": false, "has_human_body": false, "notes": ""} }
    // i2v 種は role=="i2v_source"・asset_id "GLV-MS01".."GLV-MS16"・public_path は null（本編カットに出ない）
  ],

  "motion": [   // ★16本。build_glover_film が public_items(manifest,"motion") で全読込（空なら exit 1）
    { "asset_id": "GLV-M01", "source_scene_id": "M01_src",
      "source_still": "H:/pd-media/assets/ai/glover/M01_src.png",
      "public_path": "glover/motion/M01_rife.mp4",   // ★必ず .mp4 かつ "_rife" を含む
      "act": 0, "width": 1280, "height": 720, "fps": 48, "frames": 164, "duration_sec": 3.417,
      "sha256": "...", "tags": ["plate_typed_into_laptop","revoked_screen"],
      "qc": {"reviewed": true, "on_theme": true, "artifact_free": true, "notes": ""} }
  ],

  "factory": [  // ★92本。build_glover_film が public_items(manifest,"factory") で全読込（空なら exit 1）
    { "asset_id": "AF-BG-0731",
      "public_path": "glover/factory/AF-BG-0731__two_lane_kansas_road.mp4",  // ★必ず "/factory/" を含む
      "type": "backgrounds", "subtype": "road", "kind": "video",
      "license": "Pexels License", "sha256": "...", "act": 1, "covers_scene_id": "S04",
      "duration_sec": 7.60, "width": 1920, "height": 1080,
      "eyeballed_content": "a two-lane rural road at dusk, no people, no readable plates",
      "qc": {"reviewed": true, "on_theme": true, "no_watermark": true,
             "no_recognizable_person": true, "no_cartoon": true, "label_matches_content": true, "notes": ""} }
  ],

  "overlay": [  // ちょうど12本。cuts[].src に出さない（§5.5）
    { "asset_id": "AF-PART-0044",
      "public_path": "glover/overlay/AF-PART-0044__headlight_haze.mp4",
      "type": "particle_assets", "subtype": "headlight_haze", "license": "Pexels License",
      "sha256": "...", "blend_hint": "screen",
      "eyeballed_content": "slow drifting light haze on black, loops cleanly",
      "qc": {"reviewed": true, "on_theme": true, "no_watermark": true, "notes": ""} }
  ]
}
```

## 3.2 Bがこのマニフェストから作るもの（**EP48 spec の cuts 割当**）

| マニフェスト | Bでの使い道 | spec |
|---|---|---|
| `stills[role="body"]` 85枚 | **静止画カット101本**（`kind:"img"`, `treatment` 循環）・**各≤2回** | still distinct85/cuts101 |
| body 静止画で `also_thumb==true` の6枚 | サムネ3案の背景（§11・6 asset ID） | — |
| `stills[role="i2v_source"]` 16枚 | **本編カットに出さない**（i2v 種・A が Wan で motion 化済み） | — |
| `motion` 16本 | **i2vカット32本**（`kind:"footage"`）・**各≤2回** | motion distinct16/cuts32 |
| `factory` 92本 | **実写カット92本**（`kind:"footage"`）・**各1回のみ** | factory distinct92/cuts92 |
| `overlay` 12本 | **`cuts[].src` に出さない**（§5.5 の合成レイヤー扱い） | — |

**合計 101 + 32 + 92 = 225 カット / distinct 85+16+92 = 193 / first-use 193/225 = 0.8578 ✓（floor 0.70）**

## 3.3 `scripts/check_glover_asset_manifest.py`（消費側バリデータ・BLOCKING）

```bash
$PY scripts/check_glover_asset_manifest.py --assets <path> [--json]
```

検査（1つでも違反で exit 1。`schema_version` 違いだけ exit 2）:

1. `schema_version=="glover_assets.v1"` / `episode_id=="PD-2026-048-glover"` / `slug=="glover"` / `is_stub==false`
2. `counts.*` が各配列の実長と一致し**確定値**: `still_body==85` / `still_i2v_source==16` / `motion==16` / `factory==92` / `overlay==12`
3. `role` は **`body`/`i2v_source`/`reject` の3値のみ**（`thumb`/`still_thumb` が現れたら FAIL）
4. `role=="body"` の全静止画で `public_path` 非null、かつ `remotion/public/<public_path>` と `<stem>_depth.png` が**両方実在**（`depthSrcOf()=src.replace(/\.[^.]+$/,'_depth.png')`。depth 欠落はレンダークラッシュ）。`role=="i2v_source"` は `public_path==null`
5. `role!="reject"` の全静止画で `max(width,height)>=3840`（`preflight_render_gate.MIN_LONG_EDGE_PX=3840`）
6. `motion[].public_path` が `.mp4` で終わり `_rife` を含む。`motion[].source_scene_id` は `stills[role=="i2v_source"]` の種 ID（`M01_src` 系）を指す
7. `factory[].public_path` が `/factory/` を含む
8. `overlay[].public_path` が `/overlay/` を含み `/factory/` を**含まない**・`overlay` 配列長が**ちょうど12**
9. `sha256` が全配列を通して一意（EP39〜47 の素材と sha256 被りゼロは A が保証・B は自集合内一意を検査）
10. `factory[].eyeballed_content` が非空、かつ `qc.label_matches_content==true`
11. `qc.has_readable_text` / `qc.has_identifiable_face` / `qc.has_human_body` が true の項目は `role=="reject"`（R1）
12. `also_thumb==true` の body 静止画が**ちょうど6枚**、かつ **`scene_id` 集合が §11 の6 ID と完全一致**（A↔B 契約点。**CODEX_A の also_thumb 集合と一字一致**）
13. **全文字列値**が §2 の R-FORBID / R-FACE / R-DOCHL を通る（**R-NUM は asset_manifest を除外**＝§2.3）

> **★このバリデータは A の `--verify` と同じ不変条件を独立実装する（二重チェック）。** counts が §3.1 の確定値と食い違ったら組まずに止めて A に差し戻す（ブリーフ§2: still を増やして factory を削るな）。**★特に `factory==92` と `motion==16` が非0であることを最優先で assert（EP45 空配列事故の直接防止）。**

---

# 4. narration_index（TTS は課金＝禁止。**実測版を消費**する）

## 4.1 なぜ narration_index か
`build_glover_film.py` は**尺・区間・字幕を narration_index から導出する**。**秒数をコードに直書きしない。** 唯一の正は narration_index。

## 4.2 スキーマ（`glover_narration.v1`）

```jsonc
{
  "schema_version": "glover_narration.v1",
  "episode_id": "PD-2026-048-glover",
  "is_stub": false,
  "total_seconds": 719.6,        // = SPEC narration_seconds（[SILENCE 1] の実音無音を含む）
  "chunks": [
    { "section": "HOOK",    "start": 0.000,   "end": 4.100, "text": "..." },
    { "section": "OPENING", "start": 66.000,  "end": 70.100, "text": "..." },
    { "section": "ACT_1",   "start": 114.800, "end": 118.200, "text": "..." }
  ]
}
```

**section 値（固定・6幕・★台本見出しに一致）:** `HOOK` / `OPENING` / `ACT_1` / `ACT_2` / `ACT_3` / `ENDING`。**ACT_4 は無い。**（台本は `## [OPENING]` を使う＝EP47 の `OP` ではない。narration 抽出器の section 値も `OPENING`。）
`build_glover_film.py` は `section_windows()`（各 section の最初のチャンク start）で幕境界を得る。
**台本の `【SILENCE 1 — 1.8s】` は HOOK 内1箇所**（REVOKED 画面ホールド・完全無音）。narration_index の実測がこの無音を **total_seconds に内包**している。**存在しない演出マーカーを発明しない。**

## 4.3 spec のタイムライン（**設計目標。実タイミングは narration_index が上書きする**）

| section | 語数 | 秒（目安） | 備考 |
|---|---|---|---|
| HOOK | 196 | 66.0 | VO。途中に `SILENCE 1 — 1.8s`（REVOKED 画面の残響・完全無音） |
| （gold `BrandOpening`） | 0 | 3.5 | 非VO。`OPENING_SEC`。**HOOK の問いが landした後に resolve**（frame0 ではない） |
| OPENING | 145 | 48.8 | 二人称の thesis ＋ "THE NAME ON THE PLATE" タイトル＋ channel ID |
| ACT_1 The stop | 332 | 111.8 | 最短・抑制。プレート照合→取消判明→運転者未確認で停止 |
| ACT_2 The question | 409 | 137.8 | reasonable suspicion vs probable cause・第4修正・推認 vs stereotype |
| ACT_3 The ruling | 597 | 201.1 | **最も遅く長い**。8-1・Thomas holding・narrowness・Kagan 補足・Sotomayor 反対（逐語） |
| ENDING | 389 | 131.0 | ペイオフ→CTA。"a careful yes, with a hard edge"・"suspicion, not certainty" |
| （`BrandEndcard`） | 0 | 9.0 | 非VO。`ENDCARD_SEC` |

**唯一の正は `python scripts/check_script_length.py <script> --json`。** 総語数 **2,136**（spec `words_total`）/ `wpm 178.1` /
narration_seconds **719.6**（spec）。**自己申告・体感の尺判定は禁止。**

## 4.4 実測 narration_index の受領
本番は別工程が TTS→faster-whisper で `06_audio/narration_index.v001.json`（実測語タイム・`is_stub:false`）を作る。
**これは課金ジョブなので B は起動しない。** 来た `narration_index.v001.json` を `--narr` に渡すだけ。**台本本文はそのまま（改変しない）。**

---

# 5. `glover_film.json` の構築（`scripts/build_glover_film.py`＝`build_cleveland_film.py` の複製・実素材のみ）

## 5.1 `FilmData` 型（`CaseFilm.tsx` から。これに従う）

```ts
export type Cut = {start:number; dur:number; kind:'img'|'footage'; src:string; treatment:string; seed:string};
export type FilmData = {
  fps:number; narration:string; narrationSeconds:number; hookSeconds:number; hookLine:string;
  hook:{start:number;dur:number;kind:string;src:string;seed:string}[];
  cuts:Cut[]; captions:{start:number;end:number;text:string}[];
  graphics:{start:number;end:number;lines:string[]}[];      // 必須フィールド。EP48 は []
  figures?:FigureSpec[]; heroCuts?:{start:number;dur:number;src:string}[];
};
export const caseFilmDurationInFrames = (data, fps) =>
  Math.round((data.hookSeconds||0)*fps) + Math.round(OPENING_SEC*fps)
  + Math.ceil(data.narrationSeconds*fps) + Math.round(ENDCARD_SEC*fps);
```

- アセットのパスキーは **`src`**（`remotion/public/` からの相対・A の `public_path` をそのまま）
- **カット単位の transition/motion は無い。** 動きは `treatment`・`seed`・`index%2`・`index%3` から導出
- `treatment` の実装値: `'depth'|'scan'|'duotone'|'focus'|'card'|'bleed'`（既定 bleed）
- `kind:'footage'` は `treatment` を無視して `<Footage>` を描画する
- **`fps = 30`**（film fps）。`narration = "glover/narration.mp3"`（実在）
- **`hookLine = "A plate. A hit. A stop you never saw coming."`**（★glover専用・他話の流用禁止。EP44/45 の hookSeconds=0＋流用hookLine事故を潰す。台本 HOOK の「A plate. A hit.」モチーフに一致）

### 5.1.1 ★durationInFrames の4項関数（明示・total ≤ 750s を assert）

```
caseFilmDurationInFrames(gloverFilm, fps=30)
  = round(hookSeconds * fps)        // ★hookSeconds = 8.0（ブリーフ§5 明示）→ round(8.0*30)=round(240)   = 240
  + round(OPENING_SEC * fps)        // OPENING_SEC = 3.50（gold BrandOpening は HOOK の後）→ round(105)   = 105
  + ceil(narrationSeconds * fps)    // narrationSeconds = narration_index.total_seconds（= 719.6・silence 込み）→ ceil(21588.0) = 21588
  + round(ENDCARD_SEC * fps)        // ENDCARD_SEC = 9.00 → round(270)                                    = 270
```

- **★hookSeconds を明示: `hookSeconds = 8.0`**（EP48 ブリーフ§5・§7 完了条件。8秒 hook cold-open モンタージュ尺として 8.0s を積む。EP45 の 0.0 と異なる＝**必ず 8.0**）。
- 概算（fps30・narration 719.6）: `240 + 105 + 21588 + 270 = 22203 frames = 740.1s`。**★id=Ep48Glover の durationInFrames は 22203。**
- **ビルダ末尾で `assert total_frames/fps <= 750.0`**（740.1 ≤ 750 ✓）。超えたら exit 1。

## 5.2 カット構成（**§3 マニフェストから機械的に組む・紙芝居回避が最優先**）

```
総カット 225 = factory 92 (footage) + motion 32 (footage) + 静止画 101 (img)

[A] first-use share（check_asset_reuse floor 0.70）
    distinct 92+16+85 = 193 → 193/225 = 0.8578            ✓ >=0.70（spec first_use_share と一致）

[B] per-asset cap（check_asset_reuse）
    factory: 92/92  = 1.00回  ✓ <=1（★factory は再使用禁止）
    motion : 32/16  = 2.00回  ✓ <=2
    still  : 101/85 = 1.19回  ✓ <=2

[C] animation_mix（★2つの尺度を両方満たす）
    (i) cut数ベース   still-share = 101/225 = 0.4489        ✓ <=0.45（★余裕 0.11%＝極薄・下の警告）
        motion coverage = (92+32)/225 = 124/225 = 0.5511   ✓ >=0.45（spec と一致）
    (ii) frame ベース still 平均 3.00s → 101×3.00 = 303.0s
        footage 平均 ~3.36s → 124×3.36 ≈ 416.6s
        still-frame-share = 303.0 / 719.6 = 0.4211          ✓ <=0.45（cut数比より安全側）
        motion-coverage(frame) = 416.6 / 719.6 = 0.5789     ✓ >=0.45

[D] 平均ショット長（spec mean_shot 3.2 / max 6.0）
    719.6 / 225 = 3.198 秒/カット                           ✓ <=6

[E] factory 下限（30秒に1本 = 24 → >=24本） 92本            ✓
```

> **★[C](i) の cut数ベース still-share 0.4489 は cap 0.45 に極めて薄い（余裕 0.11%）。still を1枚増やすか factory を1本削ると即 0.45 超過で FAIL。**
> **マニフェストが still 85 / factory 92 / motion 16 を割ったら組まずに止めて A に差し戻す（ブリーフ§2: still を増やして factory を削るな）。frame ベースも下回るよう still の平均尺を footage より系統的に短く保つ（§5.3-5）。**

## 5.3 カット割り当てのルール（`build_cleveland_film.py` の `allocate()`/`take()`/`repeated()` を踏襲）

1. 各幕の秒窓を `section_windows()` から取り、幕内に **factory : motion : still を按分**（★下表は**非拘束の目安**・実配分は narration_index の窓長で自動調整。確定値は「合計 factory 92 / motion 32 / still 101」だけ）:

   | section | factory | motion | still | 小計 |
   |---|---|---|---|---|
   | HOOK+OPENING | 12 | 5 | 15 | 32 |
   | ACT_1 | 13 | 5 | 16 | 34 |
   | ACT_2 | 18 | 6 | 20 | 44 |
   | ACT_3 | 31 | 10 | 31 | 72 |
   | ENDING | 18 | 6 | 19 | 43 |
   | **計** | **92** | **32** | **101** | **225** |

2. **factory は各1回のみ**（使用済み集合を持ち二度と引かない）。**motion は各≤2回・still は各≤2回**（`repeated(pool, need, cap, key)`）
3. **同一素材を連続させない**（順序を散らす）
4. 静止画 `treatment` は `["depth","scan","duotone","focus"]` を循環（同じ treatment を3連続させない）
5. **still の `dur` を footage の `dur` より系統的に短く**（§5.2[C]・still 側の重みを小さめに）
6. motion の `dur` は **3.0–3.4秒**（実素材 3.417s。超えるとループが見える）
7. **AEカードの区間（§7.2）に重なるカットも存在させる**（コンポジタ SKIP 時に穴が空かないため）

## 5.4 `figures[]` と `captions[]`
- `figures[]` は §6（**36本**・spec floor 30 に +6・`graphics[]=[]`・**dochighlight 不使用**・**実 union の必須プロパティ厳守**）
- `captions[]` は narration_index の全チャンクを **verbatim**（`build_captions()` と同一・**+11.5 film offset は composite/BGM 側で適用**、caption timing 自体は narration_index の start/end）。SRT も同時出力

## 5.5 合成レイヤー（`overlay`）— **`cuts[].src` に出さない**
`overlay` 12本は「加工」。`cuts[].src` に入れると factory 判定（上限1回）になり FAIL する。
`glover_film.json` に **`overlays` 独自キー**で持たせる（`CaseFilm` は未知キーを無視）か、専用レイヤーで `screen` 合成する。

## 5.6 ビルダが出力する成果物

| 出力 | パス |
|---|---|
| film.json | `remotion/src/data/glover_film.json` |
| public コピー | `remotion/public/glover/film_data.v001.json` |
| **build provenance** | `episodes/PD-2026-048-glover/04_scenes/glover_build_manifest.v001.json`（**A の `05_visuals/asset_manifest` に書かない**） |
| **beatsheet**（figures+AE区間の突き合わせ表） | `episodes/PD-2026-048-glover/04_scenes/glover_beatsheet.v001.json` |
| SRT（字幕未生成時のフォールバック） | `episodes/PD-2026-048-glover/08_edit/captions.final.v001.srt`（**§8 の生成器が上書きする**） |

> **★beatsheet の命名に関する重大な注意:** `check_motion_density` / `check_animation_mix` は `04_scenes/premium_beatsheet.v*.json` を**自動検出して film.json より優先**する。
> **B の beatsheet は `glover_beatsheet.v001.json`（`premium_` を付けない）** にして**ゲートの測定源を film.json 一本に保つ**（二重ソース乖離＝EP39/40 の矛盾28件の原因を避ける）。`glover_beatsheet` は provenance と `validate_glover_beats` 専用。

## 5.7 CLI
```bash
$PY scripts/build_glover_film.py \
  --assets episodes/PD-2026-048-glover/05_visuals/asset_manifest.v001.json \
  --narr   episodes/PD-2026-048-glover/06_audio/narration_index.v001.json \
  --out    remotion/src/data/glover_film.json \
  [--captions episodes/PD-2026-048-glover/08_edit/captions.final.v001.srt]
```
**実素材のみ。`is_stub==true` のマニフェストを渡されたら exit 1。★`public_items(manifest,"factory")` が空 or `!=92`、`public_items(manifest,"motion")` が空 or `!=16` なら exit 1（EP45 空配列事故防止）。** 末尾に `check_asset_reuse` 相当の自己レポートを print する。`--json` は出力→入力に使わない（上書き事故）。

---

# 6. Remotion 側 `figures[]`（**36本・spec floor 30 に +6・`graphics[]=[]`・dochighlight 不使用**）

## 6.1 密度の検算（`check_motion_density`・**AEカードは1本も数えられない**）

```
figures 36本（film.json） / body 11.993分(=719.6/60) = 3.00 /分       ✓ beats_per_min_floor 2.5
coverage: 36本 × 平均6.0s = 216.0s / 719.6 = 30.0%                    ✓ MIN_ANIMATED_COVERAGE 0.25
variety : 下記 kind を16種使用                                        ✓ variety_floor 3
spec motion.beats_floor = 30 に対し 36 で余裕。coverage が最も薄いので figures の dur は 5.4–6.0s を基本に。
```

> **★3軸すべて AND。density/coverage/variety のどれか1つでも floor 未満で FAIL。** 36本を非重複で置き平均 dur を 6.0s 程度に確保。

## 6.2 ★★★ `FigureSpec` の `kind` は**実 union の小文字値のみ・必須プロパティ厳守・`dochighlight` は使わない** ★★★

> **大文字名（`ActTitle`/`QuoteCard`/`VoteTally`…）は `FigureBeats.tsx` の union に無く、無言で描画が消える。`comparebars` は非在→`compbars`。** **不正フィールドは render クラッシュ**（下表は `remotion/src/components/FigureBeats.tsx` の実 union から転記した**必須プロパティ**）。**★`dochighlight` は union に在るが1本も使わない**（R-DOCHL）。

**EP48 で使う実在 `kind`（`FigureBeats.tsx` union・全て `start`/`end` 必須・全小文字・★必須プロパティは実 union と一致）:**

| `kind` | ★必須/実プロパティ（union から転記） | EP48での用途 |
|---|---|---|
| `acttitle` | `title:string` / `kicker?:string` / `index?:number` | 幕頭「THE STOP」/「THE QUESTION」/「THE RULING」 |
| `kinetic` | `lines:string[]` / `style?` / `emphasisWords?:string[]` | "THE NAME ON THE PLATE" / "A NAME IS NOT A FACE" / "REASONABLE, NOT CERTAIN" / "SUSPICION, NOT CERTAINTY"（emphasisWords 1–2語） |
| `stat` | `value:number` / `label:string` / `prefix?` `suffix?` `decimals?` `topLabel?` | 8（THE STOP STANDS・topLabel "8-1 — UPHELD"）/ 1（LONE DISSENT）/ 4（THE FOURTH AMENDMENT）/ 2020（DECIDED） |
| `numberticker` | `value:number` / `label?:string` / `prefix?` `suffix?` `decimals?` `topLabel?` | 2020（判決年）/ 8（THE VOTE） |
| `quote` | `quote:string` / `attribution:string` | **Thomas holding（G10・"for the Court"）/ Sotomayor 逐語（G15・"dissenting"）** のみ・§2 `APPROVED_QUOTES` 一致 |
| `lowerthird` | `primary:string` / `secondary?:string` / `accent?:string` | 開示 `AI-assisted visualization` / The Fourth Amendment / reasonable suspicion / Kansas v. Glover, 589 U.S. ___ (2020) / Deputy Mark Mehrer — Douglas County Sheriff |
| `compbars` | `items:{label:string;value:number;accent?:string}[]` | ①WHAT HE KNEW vs WHAT HE DID NOT KNOW（G04）②OWNER vs DRIVER（G05）③KANSAS: commonsense vs GLOVER: stereotype（G11）④MAJORITY vs LIMIT（G12） |
| `votetally` | ★`majority:number` / `dissent:number` / `label?:string`（**実 union＝`majority`+`dissent`**・`for`/`against` ではない） | **8-1**（majority=8 dissent=1・G13・C-4 中立） |
| `timeline` | `events:{year:string;text:string}[]` | 手続: KS courts → **2020** U.S. Supreme Court reversed（G07/G18・年数字は 2020 のみ） |
| `pindropmap` | `pins:{x:number;y:number;label?:string}[]`（★`pins` 必須） | Douglas County, Kansas（単一ピン・C-5 顔なし・G02） |
| `routemap` | `pins?:{x:number;y:number;label?:string}[]` / `label?:string` | cold-open の因果: plate typed → REVOKED → light bar → the stop（G02-G04・象徴） |
| `statemap` | `label?:string` | reasonable suspicion は狭い（「any car」ではない・G19・過大化しない） |
| `brightline` | `mode?:'draw'\|'hold'\|'slam'`（★実 union＝`mode`・`label`/`lines` ではない） | 事件が回る単一の推認線（owner→driver・G11・mode:'draw'） |
| `probablecause` | `outcome?:'stall'\|'cross'`（★実 union＝`outcome`） | reasonable suspicion は probable cause の**下**で止まる（G09・outcome:'stall'） |
| `mechanism` | `mechanism:'closingdoor'\|'gears'\|'faultsplit'`（★discriminant は `kind`・変種は `mechanism`） | ①推認の分岐 owner≠driver(faultsplit・G04) ②推認は打ち消す情報で消滅(closingdoor・G12) |
| `bar` | `data?:{label;value}[]` **or** `items?:{label;value}[]`（★実 union＝`data`/`items`） | 「a spouse, a child, a friend, a mechanic」＝他に運転しうる者（G の stereotype 論・ACT2） |

**`quote[].attribution` は §2 の `APPROVED_QUOTES` に一致させる。逐語のみ・要約を引用符に入れない。**
**★`kind` に `dochighlight` を1件も置かない（R-DOCHL・`check_glover_facts` が grep で 0 を確認）。★`votetally` は `majority`/`dissent`、`brightline` は `mode`、`probablecause` は `outcome`、`bar` は `data`/`items`、`pindropmap`/`routemap` は `pins` ＝実 union のフィールド名を厳守（別名は render クラッシュ）。**

## 6.3 figures 配分（**全 36 を figures[]・graphics[]=[]**）

| kind | 枠数 |
|---|---|
| `acttitle` | 3 |
| `kinetic` | 4 |
| `stat` | 4 |
| `numberticker` | 3 |
| `quote` | 2 |
| `lowerthird` | 6 |
| `compbars` | 4 |
| `votetally` | 1 |
| `timeline` | 1 |
| `pindropmap` | 1 |
| `routemap` | 1 |
| `statemap` | 1 |
| `brightline` | 1 |
| `probablecause` | 1 |
| `mechanism` | 2 |
| `bar` | 1 |
| **合計** | **36**（variety = 16 種・**dochighlight を含めない**） |

> **★実装表現:** 上記 36本を**すべて `figures[]`** に入れ、**`graphics[]=[]`** にする（`check_motion_density` は `figures+graphics+heroCuts` を合算するので密度は同値・floor 30 に +6）。

## 6.4 figures アンカー設計（`build_cleveland_film.py` の `FIGURE_ANCHORS` 方式）

**方式:** `(anchor_sec, payload)` の配列を秒昇順に置き、`build_figures()` が
`end = min(anchor+FIG_DUR, next_anchor-FIG_GAP, total-0.5)` でクランプ、`end-start < FIG_MIN_DUR` なら **exit 1**。
`FIG_DUR=6.0 / FIG_MIN_DUR=3.0 / FIG_GAP=0.4`。**アンカー秒は narration_index の section 窓に対する相対で決め `section_windows()` を基準にオフセットで置く**（秒直書き禁止）。

**配置方針（36本・§2 台帳の値だけ焼く・kind を分散・6制約順守・dochighlight 不使用）:**

- **HOOK（4）:** `lowerthird`（`AI-assisted visualization` 開示）/ `kinetic`（"A NAME IS NOT A FACE"・emphasisWords=["FACE"]）/ `pindropmap`（**G02 Douglas County, Kansas**・単一ピン）/ `routemap`（**G02-04** plate typed → REVOKED → light bar → the stop・象徴）
- **OPENING（2）:** `kinetic`（"THE NAME ON THE PLATE"・title 動機）/ `lowerthird`（**Kansas v. Glover, 589 U.S. ___ (2020)**）
- **ACT_1（6）:** `acttitle`（THE STOP・kicker "DOUGLAS COUNTY, KANSAS"）/ `compbars`（**G04** WHAT HE KNEW: the owner's license is revoked vs WHAT HE DID NOT KNOW: who is driving）/ `lowerthird`（**Deputy Mark Mehrer** — Douglas County Sheriff's Office・G02 帰属）/ `mechanism:faultsplit`（**G04** the assumption: owner treated as driver）/ `compbars`（**G05** THE OWNER vs THE DRIVER — the gap the deputy crossed）/ `brightline`（mode:'draw'・**G11** the single inference the case turns on）
- **ACT_2（9）:** `acttitle`（THE QUESTION）/ `lowerthird`（**The Fourth Amendment** — unreasonable searches and seizures・a stop is a seizure）/ `stat`（**value=4**, label "THE FOURTH AMENDMENT", topLabel "A STOP IS A SEIZURE"）/ `probablecause`（outcome:'stall'・**G09** reasonable suspicion sits BELOW probable cause）/ `lowerthird`（**reasonable suspicion** — a brief investigative stop, less than probable cause・G09）/ `kinetic`（"REASONABLE, NOT CERTAIN"・emphasisWords=["REASONABLE"]）/ `compbars`（**G09** REASONABLE SUSPICION vs PROBABLE CAUSE — a lower bar）/ `bar`（**data**: a spouse / a child / a friend / a mechanic — others who might be driving・G stereotype 論）/ `compbars`（**G11** KANSAS: commonsense inference vs GLOVER: a stereotype about a name）
- **ACT_3（11）:** `acttitle`（THE RULING）/ `timeline`（**events**: the Kansas courts → **2020** the U.S. Supreme Court reversed／★年数字は 2020 のみ・他 event は "the stop"/"the Kansas Supreme Court" 等の語）/ `votetally`（**majority=8 dissent=1**・G13・C-4 中立）/ `stat`（**value=8**, label "THE STOP STANDS — CONSTITUTIONAL", topLabel "8-1 — UPHELD"／**C-1 違法と読ませない**）/ `quote`（**G10 Thomas holding** → "Justice Thomas, for the Court"・逐語）/ `numberticker`（**value=8**, label "TO ONE — THE VOTE"）/ `mechanism:closingdoor`（**G12** the inference dissolves the moment contrary info appears — narrowness）/ `compbars`（**G12** MAJORITY: owner probably driving vs LIMIT: unless the officer can see otherwise）/ `stat`（**value=1**, label "LONE DISSENT — JUSTICE SOTOMAYOR"）/ `quote`（**G15 Sotomayor 反対** → "Justice Sotomayor, dissenting"・逐語・R-QUOTE）/ `numberticker`（**value=2020**, label "APRIL — DECIDED BY THE SUPREME COURT"）
- **ENDING（4）:** `kinetic`（"SUSPICION, NOT CERTAINTY"・emphasisWords=["SUSPICION"]・**C-3**）/ `statemap`（**G19** a narrow rule — not a licence to stop any car）/ `stat`（**value=2020**, label "AFTER THE SPRING OF 2020 — A CAREFUL YES"）/ `lowerthird`（開示 `AI-assisted visualization` 再掲）

> **★停止の処分を出す payload には必ず "narrow / UPHELD / the stop stands / constitutional" と限界（"unless the officer knows otherwise"/"dissolves"）を伴う（C-1/C-2・R-OVERCLAIM）。「illegal stop」「struck down」「police can stop any car」を書かない。**
> **Thomas 逐語（G10）は "for the Court" 帰属。Sotomayor 逐語（G15）は "dissenting" 帰属（Court/majority に帰属させない・C-4）。** **`60`/`20` の代わりに "sixties"/"twenties"（語）。1995（車種）・295（プレート）を `value`/label に焼かない（R-HEDGE/R-NUM）。**

## 6.5 配置ルール
1. **AEの区間（§7.2）と1秒でも重ならない**（`validate_glover_beats` が突き合わせ）
2. **同じ kind を連続させない**（`mechanism` の直後に `mechanism`、`compbars` の直後に `compbars` を置かない）
3. 1枠 **5.4–6.0秒**
4. `quote[].quote` / `kinetic[].lines` / `*.label` は §2 の R-NUM・R-QUOTE・R-FORBID・R-OVERCLAIM・R-STANDARD・R-FACE・R-DOCHL 検査対象
5. 台帳外の数値・`1995`・`295`・`60`/`20`（数字）を `value` に置かない（**焼いたら R-NUM で FAIL**）
6. **`emphasisWords` は1–2語の短句のみ**（長句は末尾切れ＝EP40 実害）
7. **`kind` に `dochighlight` を1件も置かない（R-DOCHL）**・**実 union のフィールド名厳守（§6.2）**

---

# 7. After Effects カード（`build_glover_hero_cards.py` / `composite_glover_hero.py`）

## 7.1 位置づけ
AEカードは **film.json とは別**に ffmpeg で本編に焼き込む（§0.5-2＝密度に数えられない）。
**FIXED `build_cleveland_hero_cards.py` を複製してパス・定数・CARDS デッキだけ差し替える。** レイアウト実装・`money_keys()`・**実測フィット（`sourceRectAtTime`）**・完了マーカー・**REPO path 出力**・**.aep 保存＋二段 aerender**・機械の罠対処は**1行も削らない**。

> **★複製元は実測確認済み（`build_cleveland_hero_cards.py`）:**
> - **(a) REPO path 出力** — カードは REPO（`C:` の `episodes/PD-2026-048-glover/08_edit/ae_hero/render/`）に描画する。AE の H.264 OM は `H:` に書けず失敗した実害があるため、`REPO_BEATS_DIR = ROOT/"episodes"/EP/"08_edit"/"ae_hero"` に出す。
> - **(b) 二段構成レンダ** — JSX（`AfterFX -noui -r`）は **comp をビルドしレンダキューに積み・OM を当て・`app.project.save(<glover_hero.aep>)` で .aep を保存し `_build_ok.txt` を書くまで**（`rq.render()` を JSX 内で呼ばない）。**その後 SEPARATE な `aerender -project <glover_hero.aep>` がキューを描画**する。**呼び出し側は aerender 前に `.aep` mtime > `.jsx` mtime を assert**（stale-aep ガード）。
> - **(c) 実測フィット＋引用折返し** — Python の推定は目安のみ・JSX が `sourceRectAtTime(t,false).width` で**実測して再フィット**（文字切れゼロ・複製元に実装済み）。QUOTE_CARD は引用を実測幅で折り返す。
> - **(d) ACCENT は RGB タプル** — `#5B8DB8` を **`[0.357, 0.553, 0.722]`**（0..1 float）で持つ。**hex コメントだけ変えて float を EP45 crimson のまま残さない**（§7.3）。

## 7.2 AEカードデッキ（**単調増加・重複ゼロ・台帳裏付けのみ・6制約順守。この表が契約。6枚＝ブリーフ§6 VERBATIM**）

**区間の秒は本番の rendered base（narration_index 由来）に一致させる。** 下表の秒は spec タイムライン基準の**目安**で、`build_glover_hero_cards.py` は section 窓からオフセットで算出しクランプする。**背景静止画は象徴オブジェのみ（R1/C-5・Glover 顔なし）。**
**★この表は DESIGN §6 / ブリーフ§6 と id・レイアウト・G-ID・順序（start 昇順）が一字一致。**

| id | レイアウト（**実装済み6種の内・§7.3**） | hero/main（主表示） | top / bottom / left / right / attribution | G-ID | 背景（象徴のみ） | required |
|---|---|---|---|---|---|---|
| rs01 | CENTER_STACK | **REASONABLE SUSPICION** | top: **A LOWER BAR THAN PROBABLE CAUSE** / bottom: **SPECIFIC FACTS, NOT CERTAINTY — A BRIEF INVESTIGATIVE STOP** | G09 | 天秤（hunch vs proof の間・patrol-steel） | 必須 |
| od01 | SPLIT_COMPARE | left: **THE OWNER IS PROBABLY DRIVING** / right: **UNLESS THE OFFICER KNOWS OTHERWISE** | top: **THE COMMONSENSE INFERENCE** / bottom: **REASONABLE ONLY UNTIL THE FACTS SAY NO** | G08/G12 | 左=登録票 / 右=シルエットの運転者 | 必須 |
| d01 | CENTER_STACK | **2020** | top: **SUPREME COURT** / bottom: **KANSAS v. GLOVER — DECIDED APRIL 6** | G18 | 大理石の最高裁列柱（顔なし） | 必須 |
| v01 | VOTE_SPLIT | **8 / 1** | top: **A NARROW RULE** / bottom: **THE STOP STANDS — THOMAS MAJORITY, SOTOMAYOR DISSENT** | G13/G10 | 9席のベンチ（象徴・顔なし） | 必須 |
| q01 | QUOTE_CARD | **"THE MAJORITY TODAY HAS PAVED THE ROAD TO FINDING REASONABLE SUSPICION BASED ON NOTHING MORE THAN A DEMOGRAPHIC PROFILE."** | attribution: **JUSTICE SOTOMAYOR, DISSENTING** | G17 | 夜のハイウェイ/テールランプ（判読困難・顔なし） | 必須 |
| k01 | CENTER_STACK | **REVOCATION, NOT SUSPENSION** | top: **WHAT MADE THIS STOP REASONABLE** / bottom: **A DRIVER WHO KEEPS IGNORING THE LAW — JUSTICE KAGAN, CONCURRING** | G14 | 免許証（REVOKED の判子・判読困難） | 必須 |

> **★行順＝start 昇順（時系列）:** `rs01`(ACT2) < `od01`(ACT2→ACT3) < `d01`(ACT3 open) < `v01`(ACT3 vote) < `q01`(ACT3 Sotomayor) < `k01`(ACT3 Kagan)。
> **★制約:** `v01`（8-1）は "A NARROW RULE" ＋ "THE STOP STANDS" を削除禁止（**C-1/C-2 違法化・過大化と読ませない**）。`od01` は "UNLESS THE OFFICER KNOWS OTHERWISE"（限界）を削除禁止（**C-2**）。`q01`（Sotomayor）の attribution は **"JUSTICE SOTOMAYOR, DISSENTING"**（Court/majority に帰属させない・**C-4**）・quote は §2 `APPROVED_QUOTES`（G17）の逐語のみ。`k01` は **"JUSTICE KAGAN, CONCURRING"**（Kagan＝補足・反対ではない・C-4）。
> **どのカードにも「the stop was illegal」「struck down」「police can stop any car」「probable cause required」「Sotomayor, for the Court」を書かない**（C-1/C-2/C-3/C-4）。**1995・295 を焼かない（R-HEDGE）・`60`/`20` は語で。** 数値ID＝台帳（§2.2）と一致必須。カウント終了から区間終端まで最低 **1.20秒**ホールド。
> **★DATE_STAMP は複製元に未実装。`d01`（2020）は `CENTER_STACK` で組む**（hero="2020" / top="SUPREME COURT" / bottom="…APRIL 6"）。**未実装レイアウト名を発明しない（§7.3）。**

**検算（Codex は自分で再計算して一致を確認）:** 6区間・単調増加・重複ゼロ・HOOK(0–66.0) と ENDCARD(末尾9s) に重ねない。Remotion figures(§6) と1秒も重ならない（`validate_glover_beats`）。

## 7.3 レイアウト（`build_cleveland_hero_cards.py` の実装を踏襲・**実装済みレイアウト名だけを使う**）
複製元（FIXED cleveland）が**実装する**レイアウトは**この6種のみ**（実測確認済み・`else throw new Error("unsupported layout")`）:
`ACT_TITLE_CARD` / `CENTER_STACK` / `MONEY_STACK`（=`buildCenter` に合流） / `SPLIT_COMPARE` / `QUOTE_CARD` / `VOTE_SPLIT`。
**§7.2 デッキが使うのは 4種**（`CENTER_STACK`×3 / `SPLIT_COMPARE` / `QUOTE_CARD` / `VOTE_SPLIT`）。
> **★`DATE_STAMP` と `SEAM_TRANSITION` は複製元に無い（EP47 の記述と異なる・実ファイルで確認）。日付は `CENTER_STACK` で表現する。`MONEY_STACK` は金額が無い本 EP では未使用。`ACT_TITLE_CARD` は幕頭 figures[]`acttitle` で表現。**
> **★EP48 は `VOTE_SPLIT` を使う**（8-1 は台帳 G13 で verified＝捏造でない。EP45 が VOTE_SPLIT を禁じたのは得票が台帳に無かったため。**Glover は 8-1 が確定値なので VOTE_SPLIT 使用が正当**）。
**上記6種以外のレイアウト名を発明しない（`validate_glover_beats` §7.9 ルール3 で FAIL）。dochighlight をレイアウト名に使わない。**
**共通レイヤースタック・Anton/Oswald・`psName()` の runtime 解決（allFonts の array-LIKE ラッパーを unwrap）は複製元と同一。**

**★共通レイヤースタックに AI開示レイヤーを1枚追加（R1・全カード常時焼き）:** 最上位に近い固定レイヤーとして
`AI-assisted visualization`（Oswald 20px / SILVER `#C8CDD6` / opacity 70% / 右下 `[W-32, H-28]`）を全カードに焼く。AEカードは不透明の全画面 mp4 として本編に overlay されるため、これが無いと本編(Remotion)右下の開示が隠れる（R1 違反）。字幕帯とは縦56px 以上離す。

**★EP48 色定数（0..1 float・patrol-steel レーン色。EP41 gold / EP42 blue / EP43 amber / EP44 teal / EP45 crimson / EP46 green / EP47 violet を流用禁止・DESIGN と一致）:**
```python
ACCENT = [0.357, 0.553, 0.722]  # #5B8DB8 patrol-steel（アクセント：数値・下線・レーン分離）
WHITE  = [0.961, 0.969, 0.980]  # #F5F7FA
SILVER = [0.784, 0.804, 0.839]  # #C8CDD6（開示テキスト）
INK    = [0.039, 0.039, 0.047]  # #0A0A0C 近黒ルート（サムネ bg と一致）
```
> **accent は必ず `#5B8DB8`＝RGB `[0.357, 0.553, 0.722]`（他話色を書かない・hex コメントだけ変えて float を残さない）。** サムネ・OP props・AEカードの accent は全て `#5B8DB8`。

**数値カードは全て `money_keys()` 系で表示文字列を Python 事前計算**（JSX で算術しない＝EP38 確定ルール）。
**`d01`（2020）は "2020" を先に、間を置いて "SUPREME COURT" を出す。`od01`（OWNER / UNLESS…）は左右2値を別レイヤー（改行禁止）。`v01`（8-1）は "8" と "1" を別レイヤーで、下段に "A NARROW RULE / THE STOP STANDS"。`q01`（Sotomayor）は引用を実測幅で折り返し、attribution を別レイヤー。**

## 7.4 `beats.json` スキーマ（本番 `08_edit/ae_hero/beats.json`）
`build_cleveland_hero_cards.py` の beats スキーマに準拠。トップに **`film_offset_sec`**（本編ナレ開始からのオフセット＝**hookSeconds(8.0)+OPENING_SEC(3.5)=11.5**・§7.10 のコンポジタが読む）。各 beat に `id` / `layout` / `start` / `end` / `dur` /
`still`(象徴 or null) / `hero`/`main`(主表示文字列) / `top` / `bottom` / `left` / `right` / `kicker` / `date` / `place` / `caption`(**改行禁止・最大50字**) /
`value` / `numKeys` / `blend_mode`(既定 "overlay") / `required` / `out` / `attribution`(**QUOTE_CARD=q01 は必須**・§2 `APPROVED_QUOTES` 一致・R-QUOTE)。
**`value` / `main` / `hero` の数値は §2 台帳の `verified:true` 値のみ**（`check_glover_facts` が照合）。**`1995`・`295`・`60`/`20`（数字）を出さない。**
**`v01` は R-OVERCLAIM を満たす "A NARROW RULE" ＋ "THE STOP STANDS"。`q01`（Sotomayor）は "dissenting" 帰属。`k01` は "concurring" 帰属。`beats.json` に `dochighlight` を出さない（R-DOCHL）。**

## 7.5 このマシン固有の罠（複製元が対処済み。**1つも省くな**）
1. `setTemporalEaseAtKey` の配列次元は **spatial(Position) で 1**（`if(!prop.isSpatial){...}` で分岐）
2. RS = **`"最良設定"`** / OM = **`"H.264 - レンダリング設定を一致 - 15 Mbps"`**（英語名は try/catch フォールバックのみ）
3. TextDocument の改行は `\n` 不可。**`caption` は1行**（改行が要るなら別レイヤー・SPLIT_COMPARE の左右2値・VOTE_SPLIT の 8/1 は別レイヤー）。**テキスト幅は `sourceRectAtTime(t,false).width` で実測**（advance-width 推定は禁止＝EP40 の文字切れ原因）。em-dash は `-`
4. `app.newProject()` は headless でハング。**使わず**同名 `GLOVER_` コンプを防御削除
5. ビルドは**カード6枚で ~90–110秒**。`render/_build_ok.txt` をポーリング（**タイムアウト最低300秒**）。**★ .aep 保存後、SEPARATE な `aerender -project` でキュー描画**（JSX で `rq.render()` を呼ばない＝二段構成・§7.1b）
6. 起動はデタッチ + 出力ポーリング。jsx 末尾で `app.quit()`
7. `comp.motionBlur=true` だけでは無効。**動かすレイヤー個別に `layer.motionBlur=true`**
8. 2Dレイヤー回転は **`"ADBE Rotate Z"`**（`"ADBE Rotation"` は null）
9. `inPoint` と `outPoint` の**両方**を設定
10. 読み込み後 `item.mainSource.conformFrameRate = 30`（忘れると全カードの timing がズレる）
11. 実行パス `C:\Program Files\Adobe\Adobe After Effects 2026\Support Files\AfterFX.exe` ・aerender は同 `Support Files\aerender.exe`（実在確認済み）
12. `proj.gpuAccelType = GpuAccelType.SOFTWARE`（RTX4090 でもソフトレンダ固定・安定優先）
13. **`getFontsByFamilyNameAndStyleName` を使うフォント厳格解決**（miss は **throw**・フォールバック禁止／allFonts[i] ラッパー経由 unwrap）
14. **フォント文字列やラベルを PowerShell 経由の正規表現/エスケープで生成しない**（`\b` がバックスペース化した実害）。Python 側で literal に組む。**Python 先頭に `sys.stdout.reconfigure(encoding="utf-8")`**
15. **aerender 前に `.aep` の mtime > `.jsx` の mtime を assert**（古い .aep を焼く事故防止＝EP39-41 実害・二段構成の要）

## 7.6 実行（★二段構成）
```bash
$PY scripts/ae/build_glover_hero_cards.py     # JSX + beats.json + .aep パス埋込を生成
"C:/Program Files/Adobe/Adobe After Effects 2026/Support Files/AfterFX.exe" -noui \
  -r ".../episodes/PD-2026-048-glover/08_edit/ae_hero/glover_hero.jsx"
# → render/_build_ok.txt を待つ（最大300秒）・glover_hero.aep が保存される
# → ★.aep mtime > .jsx mtime を assert（stale ガード）
"C:/Program Files/Adobe/Adobe After Effects 2026/Support Files/aerender.exe" \
  -project ".../episodes/PD-2026-048-glover/08_edit/ae_hero/glover_hero.aep"
# → render/*.mp4 が6本揃うまで待つ（最大1200秒）
$PY scripts/ae/composite_glover_hero.py
```

## 7.9 `scripts/validate_glover_beats.py`（BLOCKING）
1. `beats[].start` 昇順・区間非重複
2. 全 `start`/`end` が本編ナレ区間内（HOOK 0–66.0 と ENDCARD 末尾9s に重ねない）
3. `layout` が §7.3 の**実装済み6種**（`ACT_TITLE_CARD`/`CENTER_STACK`/`MONEY_STACK`/`SPLIT_COMPARE`/`QUOTE_CARD`/`VOTE_SPLIT`）のいずれか。**この6種以外（`DATE_STAMP`/`SEAM_TRANSITION`/`dochighlight` 等）は FAIL。** still が必要なレイアウトで null なら FAIL
4. `still` 非null は実在＋長辺 >=3840px
5. `hero`/`main`/`top`/`bottom`/`left`/`right`/`caption`/`value` が §2（R-FORBID/R-NUM/R-QUOTE/R-OVERCLAIM/R-STANDARD/R-VOTE/R-FACE/R-DOCHL/R-DATE/R-HEDGE）を通る
6. `verified:false` の値を要求するカードは `required:false` で**除外**、`required:true` なら exit 1
7. **`glover_film.json` の `figures[]`（§6）と AE の区間が1秒でも重ならない**
8. `caption` に改行が含まれない
9. **AI開示レイヤーの存在（R1）** — ビルダが全カード共通スタックに `AI-assisted visualization`（右下・§7.3）を焼く設定であることを静的に確認。無ければ FAIL。受入アイボール（§13.1）でも「AEカード表示中も右下の開示が見える」を確認
10. **`dochighlight`/`DOCHIGHLIGHT` が beats/レイアウト名に1件も無い（R-DOCHL）**
11. **`v01` に "A NARROW RULE"＋"THE STOP STANDS"（R-OVERCLAIM/C-1）／`q01` の attribution が "Justice Sotomayor, dissenting"／`k01` の attribution が "Justice Kagan, concurring"（R-QUOTE/C-4）が有ること**
12. **`film_offset_sec == 11.5`（hookSeconds8.0+OPENING_SEC3.5）**

## 7.10 基底 mp4 とコンポジタ（`build_glover_bgm_real.py` → `composite_glover_hero.py`）
```
# 完成後の合成順（ブリーフ§5）: build_glover_bgm_real.py（narration+BGM・OFF=11.5）→ composite_glover_hero.py（AEカード焼込み・film_offset_sec 適用）
BASE = episodes/PD-2026-048-glover/08_edit/glover_final_bgm.v002.mp4     # build_glover_bgm_real.py が生成
OUT  = episodes/PD-2026-048-glover/08_edit/glover_final_bgm.v003_ae.mp4  # composite_glover_hero.py が生成
FFMPEG  = C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe
FFPROBE = C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffprobe.exe
W,H,FPS = 1920, 1080, 30
```
**`build_glover_bgm_real.py` は EP43 `build_caniglia_bgm_real.py` の複製・定数 `OFF=11.5`（narration に対する BGM オフセット＝hookSeconds8.0+OPENING_SEC3.5）に差し替える。★beats を実発話に再アンカー（film_offset_sec=11.5・秒直書きしない）。**
**`composite_glover_hero.py` は EP43 `composite_caniglia_hero.py` の複製・`beats.json` の `film_offset_sec` を読み各 beat 区間を本編尺にマップする。**
**SKIP4条件を1行も削らない:** ① `render/<id>.mp4` 不在 ② 解像度 != 1920x1080 ③ 実測尺 `< dur-0.3` ④ `film_offset_sec + beat.end > base_dur`。
SKIP された区間は元カットのまま残る（作品は壊れない）。**何枚 SKIP したかを stderr に必ず出す。**
ffmpeg は `overlay=0:0:eof_action=pass:enable='between(t,start,end)'`（`blend_mode` が screen/multiply の時のみ `blend`）。
**出力後 `probe_dur(OUT)` でベースとの尺差 <=0.5秒を確認。出荷済みは絶対に上書きしない（必ず `_v003_ae`）。**

---

# 8. 字幕の切断規則（`scripts/gen_captions_glover.py`＝`gen_captions_cleveland.py` の複製）

## 8.1 原則
**文字数は「上限」であって「分割基準」ではない。** `gen_captions_cleveland.py` の `internal_split()` / `chunk_sentence()` を**そのままコピー**。
`from fix_caption_dangling import NO_DANGLE_END, wrap as safe_wrap`（**語リストを自前で書き直さない**）。

## 8.2 通すゲート `scripts/check_caption_breaks.py`（**閾値を緩めるの禁止**）
- **A. 行末の機能語** = 0件 / **B. 孤立キュー**（語数<3 で終端句読点・大文字始まりの両方を満たさない）= 0件 / **C. 句をまたぐ切断(hard)** = 0件。A/B/C いずれか1件で FAIL（実質ゼロ許容）

## 8.3 EP48 の入力と対応
- 入力は **narration_index の各チャンク文**（`--narr`）。**字幕テキストは台本本文と1:1対応**（§0.5-5）。台詞・別エピソード文の混入禁止。verbatim で使い構文境界で分割するだけ。
- `ABBR` に `U.S.` / `v.` / `Mr.` / `Ms.` / `No.` / `Jr.` を持つ（`Kansas v. Glover` の `v.`、`589 U.S.` の `U.S.`、`No. 18-556` の `No.`、`Charles Glover Junior/Jr.` の `Jr.` で文を切らない）。
- タイミングは narration_index の start/end。CPS <=27・最小表示 0.90秒。**Step で決めた境界を時間都合で動かさない。**
- **字幕にも R-FORBID 適用**（台本本文に主語付き断定の禁止語は無いので verbatim なら自然に通る。§2.1 注意：`illegal`/`unconstitutional`/`any car` 単独を禁止語に足さない＝ENDING/HOOK の否定文脈を巻き込む）。

## 8.4 セルフテスト（`--selftest`・EP38 実害を回帰に）
`Kansas v. Glover` / `589 U.S.` / `No. 18-556` / `Charles Glover Jr.` で文が切れないこと、機能語で終わるキュー・孤立キューを作らないことを含む4ケースを実装し、**出力を `check_caption_breaks.py` に食わせて exit 0 まで自動確認。**

## 8.5 実行
```bash
$PY scripts/gen_captions_glover.py --narr episodes/PD-2026-048-glover/06_audio/narration_index.v001.json
$PY scripts/check_caption_breaks.py episodes/PD-2026-048-glover/08_edit/captions.final.v001.srt
# → PASS が出るまで直す。ゲート側の閾値を緩めるのは禁止。
```

---

# 9. 5ゲートの実際の判定（**build 後に必ず全部通す・animation_mix を忘れるな**）

| ゲート | 実体 | 入力 | EP48 の通過根拠 |
|---|---|---|---|
| `check_asset_reuse.py <film.json>` | factory≤1 / motion≤2 / still≤2 / first-use≥0.70 | **film.json 位置引数** | §5.2: factory1.00 / motion2.00 / still1.19 / first-use **0.8578** |
| `check_motion_density.py --ep PD-2026-048-glover` | film.json の graphics+figures+heroCuts のみ / density≥2.5・coverage≥0.25・variety≥3（**AND**） | **`--ep`** | §6.1: **3.00 / 30.0% / 16種**（AEカードは0本＝§0.5-2・beats≥30） |
| `check_animation_mix.py --ep PD-2026-048-glover` | film.json の cuts を img=still/その他=footage 分類 / still-share≤0.45・motion-cov≥0.45 | **`--ep`** | §5.2[C]: still-share **0.4489(cut)/0.4211(frame)** / motion-cov **0.5511+** |
| `check_caption_breaks.py <srt>` | A/B/C 各0件 | **srt 位置引数** | §8 の構文境界生成器 |
| `check_script_length.py <script> --json` | 総語数 / wpm / narration_seconds | **script 位置引数** | 2,136語 / wpm178.1 / **719.6s** |

> **★ゲートの入力指定（ブリーフ§5）:** density/mix は **`--ep PD-2026-048-glover`**。**`--json <film.json>` は出力パス（上書き事故）なので入力に使わない。** asset_reuse は film.json 位置引数、caption_breaks は srt 位置引数、script_length は script 位置引数。
> **`check_animation_mix` は `04_scenes/premium_beatsheet.v*.json` があればそれを優先する。** §5.6 の通り B の beatsheet は `glover_beatsheet`（`premium_` 無し）なので**auto-detect されず film.json を測る。**
> **★still-share 0.4489 は cap 0.45 に余裕 0.11%（極薄）。build 出力を必ず `check_animation_mix` で確認し、超えたら still を1本 footage に置換して再build（still を増やさない）。**

---

# 10. OP バンパー `OpeningGlover`（Remotion・fps60/1920x1080/180f）

## 10.1 二重OPを作らない
本編（`Ep48Glover`）の OP は `Bookends.tsx` の `BrandOpening` のまま（`op_ed_bookends` ゲート・フォーク禁止）。
`OpeningGlover` は**独立したタイトルバンパー成果物**（`out/glover_opening.mp4`。Shorts/予告/SNS 用）。**本編に ffmpeg で焼き込まない。**

## 10.2 Composition 設定
| 項目 | 値 |
|---|---|
| `id` | `OpeningGlover` |
| 解像度 / fps / duration | **1920×1080 / 60 / 180**（=3.0秒） |
| component | `remotion/src/compositions/OpeningGlover.tsx` |

```tsx
import {OpeningGlover, openingGloverDurationInFrames} from './compositions/OpeningGlover';
import gloverOpeningProps from '../props/glover.json';
<Composition id="OpeningGlover" component={OpeningGlover}
  width={1920} height={1080} fps={60}
  durationInFrames={openingGloverDurationInFrames(60)} defaultProps={gloverOpeningProps}/>
```

**依存:** `@remotion/motion-blur`（未導入時のみ `cd remotion && npm i @remotion/motion-blur`）。
**`remotion/remotion.config.ts`** は既に正典値（png / h264 libx264 / CRF16 / yuv420p / bt709 / aac 320k / 全コア並列 / angle）。**一致確認のみ・書き換えない。**

## 10.3 秒数ベースのタイムライン（fps=60・フレーム直書き禁止・全て `Math.round(fps*秒)`）

| 秒 | 起きること | 手法 |
|---|---|---|
| 0.00–0.40 | L1 グラデ背景 opacity 0→1・**同時に scale 1.08→1.00（`Easing.out(Easing.cubic)`）** | interpolate（opacity 単独禁止・scale と併用） |
| 0.10 | ロゴ（`hasLogo`）左上に spring・scale 0.4→1.0・opacity 0→1 | spring `damping:14,mass:0.9` |
| 0.15–0.25 | L2 グリッド reveal（opacity→0.18）＋ translateY 0→48px | spring `damping:200,mass:1` + `Easing.inOut(Easing.sin)` |
| 0.25 | L3 グロー（patrol-steel `#5B8DB8`）scale 0.6→1.15 / opacity 0→0.85 | spring `damping:18,mass:1.2`（併用） |
| 0.30–0.86 | L4 主役タイトルが1文字ずつ切れ上がり（overflow:hidden + translateY 110%→0）＋ opacity。スタッガー **2f/文字**。全体を `Trail(layers=6,lagInFrames=1.2,trailOpacity=0.45)` で包む | spring `damping:16,mass:1` |
| 0.55–1.15 | L2b **道のセンターライン（patrol-steel）**が中央から横に `scaleX 0→1`＋opacity 0→0.5（「二車線の道」モチーフ） | spring `damping:22,mass:1.1`・`transformOrigin:'center'`・**motionBlur** |
| 0.95–1.35 | L5a アクセント下線（patrol-steel）左から `scaleX 0→1` | spring `damping:16,mass:0.8`・`transformOrigin:'left center'` |
| 1.10–1.55 | L5b サブタイトル translateY 24→0 + opacity 0→1 | spring `damping:20,mass:1`（併用） |
| 1.55–3.00 | settle→ホールド。**完全静止フレーム無し・フェードアウトしない** | — |

> **等速線形を1箇所も使わない。opacity 単独の演出を1箇所も作らない**（全 opacity が translateY/scale/scaleX と対）。

## 10.4 props 型と値
```ts
export type OpeningGloverProps = { title:string; subtitle:string; accent:string; hasLogo:boolean };
```
`remotion/props/glover.json`: `{ "title":"THE NAME ON THE PLATE", "subtitle":"CAN A RECORD STOP YOUR CAR?", "accent":"#5B8DB8", "hasLogo":true }`
`remotion/props/glover_short.json`: `{ "title":"THE NAME ON THE PLATE", "subtitle":"A PLATE. A HIT. A STOP.", "accent":"#5B8DB8", "hasLogo":false }`
> `subtitle`/`title` も §2 の R-FORBID/R-OVERCLAIM/R-STANDARD/R-FACE 検査対象。ルート背景は INK 近黒 `#0A0A0C`。
> **accent は EP41 gold / EP42 blue / EP43 amber / EP44 teal / EP45 crimson / EP46 green / EP47 violet を書かず patrol-steel `#5B8DB8`（レーン分離・他話色流用は BLOCKER）。**
> **「the stop was illegal」「police can stop any car」を subtitle に書かない。** 疑問形 `CAN A RECORD STOP YOUR CAR?` は問題提起として可（過大化しない）。

## 10.5 量産
```bash
cd remotion && npm run studio     # OpeningGlover を 0→180f スクラブして §10.3 の各時刻を目視
npx remotion render OpeningGlover out/glover_opening.mp4 --props=./props/glover.json
npx remotion render OpeningGlover out/glover_short_op.mp4 --props=./props/glover_short.json
```

---

# 11. サムネ3案（`GloverThumbnails.tsx`・`<Still>` 1280×720・Root に `Thumb-glover-01..03`）

**共通要件:** 見出し全て大文字・4語以内・320pxで判読 / **実在人物の肖像禁止（R1・Glover の顔/身体を出さない・C-5）** / INK 黒 `#0A0A0C` bg + patrol-steel `#5B8DB8` /
背景は body 静止画のうち `also_thumb==true` の6枚（象徴オブジェのみ・C-5。**サムネ専用の分類は無い＝also_thumb フラグを読む**） / `thumbnail_visibility`（luma平均≥33＋コントラスト）を通す。目標CTR 6%+。3案は6枚から選ぶ。
**「the stop was illegal」「struck down」「stop any car」を出さない（R-FORBID/R-OVERCLAIM）。1995・295 を出さない（R-HEDGE）。**

**★also_thumb 6枚（still 資産 ID 空間 S01..S85＝CODEX_A §4.3。A のマニフェストと一字一致必須の A↔B 契約点）:**
`S01` / `S07` / `S24` / `S41` / `S60` / `S85`。
> サムネ component は**マニフェストの `also_thumb` フラグを読んで**背景を選ぶ（scene id をハードコードしない）。**この6 ID は CODEX_A §4.3 と完全一致必須**（`check_glover_asset_manifest` §3.3-12 が集合の一致を検査）。**CODEX_A が別集合なら B は自分の6 ID を書き換えず A に合わせる（A が producer）。**

- **T1「プレートの名前」（最推奨）:** ダッシュのラップトップに打たれたプレートと `REVOKED` 画面の接写（象徴・顔なし・**S01/S07** 系）。文字 **`A NAME ON A SCREEN`**（4語）。`NAME` を patrol-steel。**射程を過大化しない。**
- **T2「8-1」（尊厳）:** 大理石の列柱／9席を背にした象徴（**S41/S85** 系）、前面に **`8 – 1`**（大）＋ **`A NARROW RULE`**（下）。数字は G13 の検証済み値のみ。**「違法」に見せない。**
- **T3「あなたの車」（二人称）:** 夜のハイウェイ/テールランプ（**S24/S60** 系）。文字 **`CAN THEY STOP YOUR CAR?`**（疑問・過大化しない）。`YOUR` を patrol-steel。

**A/Bタイトル候補（`09_package`・60字以内・二人称・台本のとおり・★"違法"/"any car"と書かない）:**
- **A:** `A Cop Ran Your Plate and Pulled You Over. He Never Saw You Break a Law.`
- **B:** `Can a Cop Stop Your Car Just Because of Who Owns It?`
> ※「the stop was illegal」「the Court struck it down」「police can stop any car」系のタイトルは**禁止**（C-1/C-2・R-FORBID/R-OVERCLAIM）。

**固定コメント** `09_package/pinned_comment.v001.txt`（§2 の R-NUM/R-QUOTE/R-FORBID/R-OVERCLAIM/R-STANDARD 検査対象・台帳事実のみ）:
```
What this case actually decided -- and what it did not.

WHAT IT DECIDED: In Kansas v. Glover (589 U.S. ___, 2020), the Supreme Court held
8-1 that when an officer has no information negating the inference that a vehicle's
registered owner is the one driving it, and that owner's license is revoked, a
brief investigative stop is reasonable. The stop did not violate the Fourth
Amendment. This is reasonable suspicion for a brief stop -- a lower bar than
probable cause, not certainty.

WHAT IT DID NOT DO: The Court stressed its holding is NARROW. The inference works
only while the officer has nothing cutting against it. The moment he can see the
driver is plainly not the owner -- an owner in his sixties, a driver in her
twenties -- the reason for the stop is gone. Justice Kagan, concurring with Justice
Ginsburg, underlined that it turns on revocation, not a mere suspension. Justice
Sotomayor, in dissent, warned it paves the road to suspicion built on a profile.
Eight votes to one.

This is not a rule that lets police stop any car at any time. Look up your own
state's rules on traffic stops and reasonable suspicion before you need them.
```
> **description.txt にも AI 開示行（`AI-assisted visualization`）を置く（R1）。** 数値は台帳（8-1 / 589 U.S. / 2020）のみ・**1995/295 を出さない**。

---

# 12. 本編コンポジション登録（`remotion/src/Root.tsx`・`Ep47Atwater`/`Ep45Cleveland` の形を踏襲）
```tsx
import gloverFilm from './data/glover_film.json';
<Composition id="Ep48Glover" component={CaseFilm}
  durationInFrames={caseFilmDurationInFrames(gloverFilm as unknown as FilmData, BRAND.video.fps)}
  fps={BRAND.video.fps} width={BRAND.video.width} height={BRAND.video.height}
  defaultProps={{ data: gloverFilm as unknown as FilmData, seriesLabel: 'PRIME DOCUMENTARY',
    title: 'A Cop Ran Your Plate and Pulled You Over. He Never Saw You Break a Law.',
    subtitle: 'A revoked license on the registration, a stop before anyone checked the driver, upheld 8-1 as reasonable suspicion. A narrow rule that dissolves the moment the officer can see he is wrong.' }}/>
```
> **id は正確に `Ep48Glover`（切り詰め・綴り違い・大文字化の誤記に注意）。** `caseFilmDurationInFrames` の 4項評価は **22203 frames**（§5.1.1・hookSeconds=8.0）。
> `gloverFilm` は `import gloverFilm from './data/glover_film.json';`。**import に加え、film の `hookSeconds===8.0` を Root で（or build 側で）確認**（EP44/45 の hookSeconds=0 事故防止）。
> `remotion/src` に現在 `glover` の文字列が無いこと（衝突しない）を確認してから追記。
> `title`/`subtitle` も §2 検査対象（R-FORBID/R-OVERCLAIM/R-STANDARD/R-QUOTE）。**「the stop was illegal」「struck down」「police can stop any car」を書かない。**
> **★追記後 `cd remotion && npx tsc --noEmit`（or `npm run typecheck`）で型検査を通す**（hookSeconds/FilmData 整合）。

---

# 13. 受入（自分で exit 0 を確認してから完了報告）
```bash
cd C:\Users\aab15\Documents\prime-documentary ; PY=./.venv/Scripts/python.exe

# 0. 語数（最優先・課金前に落とす）
$PY scripts/check_script_length.py episodes/PD-2026-048-glover/03_script/script.en.v001.md --json   # 2,136語 / wpm178.1 / 719.6s

# 1. 事実性/6制約（EP48固有・正確性ゲートはこの1本・dochighlight 不使用も検査）
$PY scripts/check_glover_facts.py --json

# 2. 契約バリデータ
$PY scripts/validate_glover_beats.py
$PY scripts/check_glover_asset_manifest.py --assets episodes/PD-2026-048-glover/05_visuals/asset_manifest.v001.json

# 3. ★5ゲート（animation_mix を忘れるな・入力は --ep / 位置引数を厳守）
$PY scripts/check_asset_reuse.py    remotion/src/data/glover_film.json
$PY scripts/check_motion_density.py --ep PD-2026-048-glover
$PY scripts/check_animation_mix.py  --ep PD-2026-048-glover
$PY scripts/check_caption_breaks.py episodes/PD-2026-048-glover/08_edit/captions.final.v001.srt

# 4. 水増し・レンダ前プリフライト
$PY scripts/check_padding.py --ep PD-2026-048-glover --json
$PY scripts/preflight_render_gate.py --ep PD-2026-048-glover

# 5. ★public_slim staging（EP45 空 public_slim 事故防止）→ 本編レンダ（slim public・並列4）→ BGM → AEカード合成
#    public/glover → public_slim/glover へ全メディア（img/factory/motion/audio/overlay + 各 <stem>_depth.png）をコピー
$PY scripts/stage_cleveland_assets.py --ep PD-2026-048-glover 2>/dev/null || {
    mkdir -p remotion/public_slim/glover
    cp -r remotion/public/glover/{img,factory,motion,overlay,audio} remotion/public_slim/glover/ 2>/dev/null
    cp remotion/public/glover/narration.mp3 remotion/public_slim/glover/ 2>/dev/null
}
#   ★glover_film.json が参照する src と各 <stem>_depth.png が public_slim に全て在ることを確認してからレンダ
#   ★public/glover と public_slim/glover の双方で media 解決 0 missing を確認
cd remotion
npx remotion render Ep48Glover out/glover.mp4 --public-dir=public_slim --concurrency=4
cd ..
$PY scripts/build_glover_bgm_real.py     # OFF=11.5
$PY scripts/ae/composite_glover_hero.py

# 6. 本編最終受入（episode番号は★位置引数・--ep ではない）
$PY scripts/check_final_acceptance.py 48 \
  --render episodes/PD-2026-048-glover/08_edit/glover_final_bgm.v003_ae.mp4 --emit-receipt
```

| ゲート | EP48 目標値 |
|---|---|
| `check_script_length` | 総語数 **2,136** / `wpm 178.1` / narration **719.6s** |
| `check_asset_reuse` | factory≤1 / motion≤2 / still≤2 / first-use **0.8578**（floor0.70） |
| `check_motion_density` | density **3.00**/min / coverage **30.0%** / variety 16（floors 2.5 / 0.25 / 3・beats **≥30**） |
| `check_animation_mix` | still-share **0.4489(cut)/0.4211(frame)**（cap0.45・余裕極薄）/ motion-cov **0.5511+**（floor0.45） |
| `check_caption_breaks` | 行末機能語0 / 孤立キュー0 / hard split 0 |
| `check_glover_facts` | violations = 0（台帳照合・UPHELD/narrow 枠・8-1・Thomas maj/Sotomayor dissent/Kagan concur 分離・reasonable suspicion≠PC・R-FORBID・R-OVERCLAIM・R-STANDARD・R-DOCHL・R-QUOTE・R-HEDGE） |
| runtime band | 12.0–12.5分（narration 719.6s + hook8.0 + bookends・total **740.1s ≤ 750s**） |
| factory クリップ | ≥24本 → **92本** |
| image_resolution | 全静止画 長辺 ≥3840px |
| thumbnail | 3案 @1280×720 + selected luma≥33 |
| op_ed_bookends | `BrandOpening`/`BrandEndcard` を import（フォーク禁止） |

**全て exit 0 でなければ `package_ready` にしない。自己申告QCは無効。QC基準を書き換えて通すのは禁止。**

## 13.1 完成後の全編アイボール（★3回・**1フレーム判定禁止＝EP39-41 実害**）
`glover_final_bgm.v003_ae.mp4` を **0→末尾まで通しで実視聴（★3回）**し、以下を確認してから完了報告:
- **★hook ライン "A plate. A hit. A stop you never saw coming." が cold-open に正しく出る（他話の流用でない・hookSeconds=8.0 の 8秒が積まれている）**
- **★VO と字幕・カットが同期（音ズレ・字幕ズレ無し）**
- 紙芝居感が無い（still が連続していない・footage が体感で過半＝EP45 の直接死因を潰せているか）
- **★AEカード6枚が全て焼き込まれ・クリップ（末尾切れ）していない・数値が台帳と一致**（「the stop was illegal」「struck down」「police can stop any car」がどこにも無い）
- **`v01`「8 / 1 / A NARROW RULE / THE STOP STANDS」が読める（C-1/C-2 違法化・過大化と読ませない）**
- **`rs01`「REASONABLE SUSPICION / A LOWER BAR THAN PROBABLE CAUSE」（C-3・probable cause でない）**
- **`od01`「THE OWNER IS PROBABLY DRIVING / UNLESS THE OFFICER KNOWS OTHERWISE」（C-2 限界）**
- **`q01`（Sotomayor 逐語）が "JUSTICE SOTOMAYOR, DISSENTING" 帰属（Court/majority に帰属していない・C-4・要約を引用符にしていない）／`k01` が "JUSTICE KAGAN, CONCURRING"（補足・反対でない）**
- **`d01`「2020 / SUPREME COURT / APRIL 6」が読める。1995・295 がどこにも出ていない（R-HEDGE）**
- Charles Glover の顔・身体・肖像が無い（象徴＝カンザスの道/パトカー/ピックアップ/プレート/ラップトップ/REVOKED画面/ライトバー/免許証/登録票/天秤/60代vs20代のシルエット/列柱9席のみ・C-5）／彼の犯罪性を免許取消運転以外に広げていない
- **`dochighlight`（黒バー/box/underline）が1本も無い（figures/AE／R-DOCHL）**
- 生成ビジュアル表示中は `AI-assisted visualization` が右下に常時（**AEカード6枚の表示中も**開示が見える＝カード共通スタックに焼かれている・R1・§7.3/§7.9）
- **★accent が patrol-steel `#5B8DB8`（EP41 gold / EP42 blue / EP43 amber / EP44 teal / EP45 crimson / EP46 green / EP47 violet が紛れていない）**
- 尺差（base と <=0.5s）が無い

---

# 14. 絶対にやらないこと
- **EP39 / EP40 / … / EP47 のファイル・素材に触らない**（読み取りのみ可）。レーンを分離する。
- **スレッドAの所有ファイル（§0.2.1）に書かない**（`05_visuals/` `05_stock/` `remotion/public/glover/` `H:\...\ai\glover\`）。**B の provenance は `04_scenes/glover_build_manifest.v001.json` に書く。**
- **設計書 / `EP48_glover_CODEX_A_*` / PD-2026-039〜047 に触らない。**
- **課金ジョブを起動しない**（ElevenLabs TTS / 課金画像生成API / YouTube アップロード）。narration_index は実測版を消費するだけ。
- **公開済み・出荷済み mp4 を上書き・再レンダしない**（出力は必ず `_v003_ae`）。
- **台帳（§2）に無い数値を焼かない**（$580,000 の再発防止）。**★`1995`（車種）・`295`（プレート）・保安官の詳細は confidence:medium＝画面禁止（R-HEDGE）。8-1/2020/589 U.S./No. 18-556/Fourth のみ断定。`60`/`20` は語（sixties/twenties）で。**
- **`FigureSpec` の `kind`/フィールド名を推測で書かない**（§6.2 の実 union の小文字値・必須プロパティのみ。大文字名は無言で消え・不正フィールドは render クラッシュ。`comparebars`→`compbars`・`VoteTally`→`votetally`＝`majority`/`dissent`・`brightline`＝`mode`・`probablecause`＝`outcome`・`bar`＝`data`/`items`・map 系＝`pins`）。**★`dochighlight` を1本も使わない（R-DOCHL）。**
- **`--variants` という語を書かない**（1シーン1枚・バリエーション0＝ブリーフ§1。SDXL は A の領分で 1 固定）。
- **asset_manifest の `counts`/`role` enum/`overlay` 枚数を CODEX_A と食い違わせない**（`role` は `body`/`i2v_source`/`reject` の3値のみ・**`thumb`/`still_thumb` を作らない**・overlay=12・also_thumb 6 ID を A と一致）。
- **★「the stop was illegal」化しない・「struck down」と言わない**（C-1＝停止は合憲 UPHELD 8-1）。**「police can stop any car / anyone」と過大化しない**（C-2・R-OVERCLAIM）。**probable cause を要件と書かない**（C-3・reasonable suspicion＝Terry 級）。**Sotomayor 逐語を Court/majority に、Kagan を反対に帰属させない**（C-4・R-QUOTE）。**票決は 8-1**。**Charles Glover の顔/肖像/身体を出さない・免許取消運転以外の犯罪性を出さない**（C-5・R-FACE）。
- **accent に他話色（gold/blue/amber/teal/crimson/green/violet）を使わない**（patrol-steel `#5B8DB8`＝RGB `[0.357,0.553,0.722]` のみ・hex コメントだけ変えて float を残さない）。
- **stub/dryrun/placeholder のコードパスを作らない**（このスレッドは実素材のみ・ブリーフ§7・grep 0）。**★`build_glover_film.py` は manifest の `factory[]`(92)/`motion[]`(16) を `public_path` で全読込し、空 or 数不一致なら exit 1（EP45 空配列＝紙芝居事故の直接防止）。**
- **★render 前に `public_slim/glover` へ全メディアを staging し・public/public_slim 双方で media 解決 0 missing を確認する**（EP45 は空 public_slim でレンダ素材欠落・§13-5）。
- **★AEカードは複製元（FIXED cleveland）の実装済み6レイアウトのみ使う**（`DATE_STAMP`/`SEAM_TRANSITION` は無い＝発明しない）。**REPO path 出力・二段 aerender（.aep保存→aerender -project）・.aep mtime>.jsx assert・実測フィット・ACCENT RGB タプルを1つも省かない。**
- **スペック数値（225 cuts / still85 / factory92 / motion16 / distinct193 / first-use0.8578 / still-share0.4489 / figures≥30→36 / 719.6s / 2,136語 / 48シーン / mean_shot3.2 / total740.1s≤750s / durationInFrames22203 / hookSeconds8.0）を変えない。**
- **composition id は `Ep48Glover`（切り詰め・綴り違い注意）。** **PowerShell 経由で正規表現/エスケープを生成しない**（`\b` バックスペース化の実害）。typecheck を通す。
