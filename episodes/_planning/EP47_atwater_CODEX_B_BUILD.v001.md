# EP47 atwater — Codex スレッドB「実装」引き継ぎプロンプト v001

> **このファイルは単体で完結している。他のファイルを読まなくても着手できる。**
> 並行して走っていたスレッドA（素材生成）のファイル `EP47_atwater_CODEX_A_*.md` は**読まない**（Aは既に FROZEN・接続点は §3 のマニフェスト1ファイル）。
> 設計書 `EP47_atwater_DESIGN*.md` も**読まない**（必要な数値・AEデッキ・figures 配分はすべて本書に転記済み）。
> `EP47_atwater_PRODUCTION_SPEC.v001.json` の数値は本書に転記済み。**あなたはこれを書き換えない。**

```
あなたは Prime Documentary（YouTubeドキュメンタリーチャンネル）の制作エンジニアです。
リポジトリ: C:\Users\aab15\Documents\prime-documentary
Python:     C:\Users\aab15\Documents\prime-documentary\.venv\Scripts\python.exe
メディア:   H:\pd-media
担当:       EP47 / Episode ID: PD-2026-047-atwater / slug: atwater
Composition id（本編）: Ep47Atwater
```

**題材:** *Atwater v. City of Lago Vista*, **532 U.S. 318 (2001)**（decided **2001-04-24**）と **Gail Atwater**（Lago Vista, Texas の**存命の私人 = R2・有罪歴なし＝罰金のみ**）。
シートベルト（罰金刑のみ・投獄不能の軽罪）で**令状なし現行犯逮捕**された母親。最高裁は **5-4** でその逮捕を**合憲（UPHELD）**と判断した。
本作の主題は「**逮捕は違法だったのではない。合憲だった＝許されていた**」という不快さ（constitutional, not illegal）。Souter 多数意見は逮捕を "pointless indignity" と**認めつつ許容**し、救済を**立法に委ねた**。O'Connor は**反対意見**の対抗軸。

> **★正確性6制約が全出力を律する（§2）。** 「illegal / unconstitutional / struck down」を逮捕自体に**書かない**（合憲＝UPHELD）・Souter 逐語は**多数意見**帰属・O'Connor 逐語は**反対意見**帰属（Court に帰属させない）・票決は **5-4**・Gail Atwater の顔/肖像/身体を一切出さない（象徴のみ）・**同乗の子ども2人を扇情化しない**（"two young children" のみ・年齢を出さない）・数値は台帳一致（**$50/2001 のみ断定**・1997/子の年齢はヘッジして画面に出さない）。**★`figures[].kind` に `dochighlight` を1件も入れない**（黒バー/box/underline がバグに見える＝3回指摘）。

---

# 0. このスレッドの責務・境界・完了条件

## 0.1 このスレッド（B）の責務 — **コード律速。実装は全部書ける。**

| # | 作業 | 成果物 |
|---|---|---|
| B-1 | エピソードディレクトリと `manifest.json` | `episodes/PD-2026-047-atwater/**` |
| B-2 | 境界契約マニフェストの**消費側**バリデータ | `scripts/check_atwater_asset_manifest.py` |
| B-3 | 事実台帳 A-ID と 6制約ゲート（**EP47固有・BLOCKING**） | `scripts/check_atwater_facts.py`（**`check_cleveland_facts.py` を複製**） |
| B-4 | `atwater_film.json` ビルダ（**manifest→cuts＋beatsheet／footage混在・実素材のみ**） | `scripts/build_atwater_film.py`（**`build_cleveland_film.py` を複製**） |
| B-5 | beats バリデータ（AEとRemotionの区間衝突検査＋ledger／6制約） | `scripts/validate_atwater_beats.py`（**`validate_cleveland_beats.py` を複製**） |
| B-6 | **構文境界で切る字幕生成器**（実測 narration_index から verbatim） | `scripts/gen_captions_atwater.py`（**`gen_captions_cleveland.py` を複製**） |
| B-7 | **After Effects カード**のビルダとコンポジタ | `scripts/ae/build_atwater_hero_cards.py`（**`build_cleveland_hero_cards.py` 複製**）/ `scripts/ae/composite_atwater_hero.py`（**`composite_caniglia_hero.py`=EP43 複製**） |
| B-8 | 本編 BGM ミックス（AEカード合成の基底 mp4 を生成） | `scripts/build_atwater_bgm_real.py`（**`build_caniglia_bgm_real.py`=EP43 複製・OFF=11.5**） |
| B-9 | Remotion 本編コンポジション登録 `Ep47Atwater` | `remotion/src/Root.tsx` |
| B-10 | OP バンパー `OpeningAtwater`（fps60/1920x1080/180f） | `remotion/src/compositions/OpeningAtwater.tsx` |
| B-11 | サムネ3案 | `remotion/src/compositions/AtwaterThumbnails.tsx` |
| B-12 | 本編レンダ→BGM→AEカード合成→全ゲート→**全編アイボール** | `episodes/PD-2026-047-atwater/08_edit/**` |

> **★このスレッドは「実素材のみ」（ブリーフ§7）。stub/dryrun/placeholder のコードパスを作らない（`grep -riE 'stub|placeholder|dryrun' scripts/*atwater*.py` が 0）。** A は FROZEN（§3 の本番マニフェストが実在）・narration_index は実測版が実在する前提で組む。**素材が来ていなければ止めて A/上流に差し戻す**（架空の黒スタブで緑にしない）。

## 0.2 もう一方のスレッド（A・FROZEN）との境界 — **接続点はただ1ファイル。**

```
episodes/PD-2026-047-atwater/05_visuals/asset_manifest.v001.json
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
| `episodes/PD-2026-047-atwater/manifest.json` | **B** | 読み書き |
| `episodes/PD-2026-047-atwater/{00_topic,01_research,03_script,04_scenes,06_audio,08_edit,09_package,approvals,events}/**` | **B** | 読み書き |
| `remotion/src/**` `remotion/props/**` | **B** | 読み書き |
| `scripts/*atwater*.py` / `scripts/ae/*atwater*.py`（§0.3） | **B** | 新規作成 |
| **`episodes/PD-2026-047-atwater/05_visuals/**` `05_stock/**`** | **A** | **読み取りのみ。書くな** |
| **`H:\pd-media\assets\ai\atwater\**` / `ai_video\atwater\**`** | **A** | **読み取りのみ。書くな** |
| **`remotion/public/atwater/{img,factory,motion,overlay}/**`** | **A** | **読み取りのみ。書くな** |
| `EP47_atwater_DESIGN*.md` / `EP47_atwater_CODEX_A_*.md` | **設計/Aスレッド** | **触るな** |
| `EP47_atwater_PRODUCTION_SPEC.v001.json` / `EP47_atwater_script.en.v001.md` / `EP47_atwater_facts.v001.json` | **上流** | **読み取りのみ。書くな** |
| `episodes/PD-2026-039-*/**` … `PD-2026-046-*/**` / それらの素材 | **他エージェント** | **絶対に触るな（読み取りのみ可）** |

> **B は `remotion/public/atwater/` に書かない**（A の staging 済み本番素材）。B の provenance/beatsheet は `04_scenes/` に書く（§5.6）。**render 用の `public_slim` staging（§13）は B が作る。**

## 0.3 B が新規作成するスクリプト（これ以外を新規に作らない。既存を改変しない）

| パス | 役割 | 手本（**改変せず読んで複製→パス/定数だけ差し替え**・実在確認済み） |
|---|---|---|
| `scripts/check_atwater_asset_manifest.py` | §3.3 消費側バリデータ | `scripts/check_cleveland_asset_manifest.py` |
| `scripts/check_atwater_facts.py` | §2 6制約＋台帳（BLOCKING・**正確性ゲート名はこの1つに統一**） | **`scripts/check_cleveland_facts.py`** |
| `scripts/build_atwater_film.py` | §5 film.json＋provenance＋beatsheet＋SRT（**実素材のみ・★factory/motion全読込**） | **`scripts/build_cleveland_film.py`** |
| `scripts/validate_atwater_beats.py` | §7.9 不変条件 | **`scripts/validate_cleveland_beats.py`** |
| `scripts/gen_captions_atwater.py` | §8 構文境界字幕生成器 | **`scripts/gen_captions_cleveland.py`** |
| `scripts/ae/build_atwater_hero_cards.py` | §7 AEカードビルダ | **`scripts/ae/build_cleveland_hero_cards.py`** |
| `scripts/ae/composite_atwater_hero.py` | §7.10 コンポジタ（`beats.json` の `film_offset_sec` を読む） | **`scripts/ae/composite_caniglia_hero.py`（=EP43）** |
| `scripts/build_atwater_bgm_real.py` | §7.10 基底 mp4（narration＋BGM ミックス・**OFF=11.5**） | **`scripts/build_caniglia_bgm_real.py`（=EP43）** |

> **`build_atwater_film.py` の複製時に差し替える定数:** `SLUG="atwater"`・`EP="PD-2026-047-atwater"`・`DEFAULT_OUT=remotion/src/data/atwater_film.json`・`PUB_FILM=remotion/public/atwater/film_data.v001.json`・`SECTION_TARGETS`（§5.3）・出力パス群・`expected={"factory":92,"motion":32,"stills":101}`。**ロジック（`public_items()` / `repeated()` / `take()` / `allocate` / `build_figures` / `build_captions`）は1行も変えない。**
> **既存の `build_cleveland_film.py` / `gen_captions_cleveland.py` 等は触らない**（他エピソードが使用中）。EP47用に**新規コピー**する。
> **実在しない複製元名を捏造しない**（`ls scripts/` で確認済み。複製元は上表の実在ファイルのみ。`build_atwater_film.py` の複製元は `build_cleveland_film.py`）。

## 0.4 完了条件（実素材で、全て緑になったら「実装完了」）

```bash
cd C:\Users\aab15\Documents\prime-documentary
PY=./.venv/Scripts/python.exe

# [B-DONE-1] マニフェスト消費側バリデータ（A の FROZEN 本番マニフェスト相手に通ること）
$PY scripts/check_atwater_asset_manifest.py \
  --assets episodes/PD-2026-047-atwater/05_visuals/asset_manifest.v001.json

# [B-DONE-2] 字幕（実測 narration の実文から構文境界で生成）
$PY scripts/gen_captions_atwater.py \
  --narr episodes/PD-2026-047-atwater/06_audio/narration_index.v001.json
$PY scripts/check_caption_breaks.py \
  episodes/PD-2026-047-atwater/08_edit/captions.final.v001.srt

# [B-DONE-3] film.json を実マニフェストから組み立てる（footage 混在必須・dochighlight 不使用・★factory92/motion16 全読込）
$PY scripts/build_atwater_film.py \
  --assets episodes/PD-2026-047-atwater/05_visuals/asset_manifest.v001.json \
  --narr   episodes/PD-2026-047-atwater/06_audio/narration_index.v001.json \
  --out    remotion/src/data/atwater_film.json

# [B-DONE-4] ★5ゲート全部（--ep 指定・animation_mix を絶対に忘れるな）
$PY scripts/check_asset_reuse.py     remotion/src/data/atwater_film.json
$PY scripts/check_motion_density.py  --ep PD-2026-047-atwater
$PY scripts/check_animation_mix.py   --ep PD-2026-047-atwater
$PY scripts/check_caption_breaks.py  episodes/PD-2026-047-atwater/08_edit/captions.final.v001.srt
$PY scripts/check_script_length.py   episodes/PD-2026-047-atwater/03_script/script.en.v001.md --json

# [B-DONE-5] 事実性/6制約（＋dochighlight 不使用・quote 逐語帰属）
$PY scripts/check_atwater_facts.py --json

# [B-DONE-6] beats 契約（AE区間 と Remotion figures[] が1秒も重ならない）
$PY scripts/validate_atwater_beats.py

# [B-DONE-7] AE カードをビルド＋レンダ＋コンポジット
$PY scripts/ae/build_atwater_hero_cards.py
"C:/Program Files/Adobe/Adobe After Effects 2026/Support Files/AfterFX.exe" -noui \
  -r "C:/Users/aab15/Documents/prime-documentary/episodes/PD-2026-047-atwater/08_edit/ae_hero/atwater_hero.jsx"
$PY scripts/ae/composite_atwater_hero.py

# [B-DONE-8] Remotion Studio で目視
cd remotion && npm run studio
#   → Ep47Atwater / OpeningAtwater / Thumb-atwater-01..03 が出て、実際に動くこと
```

**台本は既に確定済み**（`EP47_atwater_script.en.v001.md`・**2,135語・12.0分**・ロック）。本番配置先は
`episodes/PD-2026-047-atwater/03_script/script.en.v001.md`（**1バイトも変えずコピー**・整形禁止＝AI臭再発と語数ゲート再計算を招く）。

---

# 1. 実装前に必ず読むファイル（**推測で書くな**）

| パス | なぜ読むか |
|---|---|
| `scripts/build_cleveland_film.py` | **複製元。** `public_items()`/`repeated()`/`take()`/`allocate`/`build_figures`/`build_captions` をそのまま踏襲し定数だけ atwater に。**★`public_items(manifest,"factory")`・`public_items(manifest,"motion")` を必ず読む（EP45 は factory/motion 配列が空で紙芝居化した実害＝§0.5-1/§5.2）。** |
| `scripts/ae/build_cleveland_hero_cards.py` | **複製元。** `money_keys()`（Python で表示文字列を全事前計算）/ `fit_size()` / CARDS デッキ構造 / レイアウト定義（**実装済み8種＝§7.3**）/ 完了マーカーをそのまま |
| `scripts/ae/composite_caniglia_hero.py`（EP43） | **複製元。** SKIP4条件（missing / 解像度不一致 / 実測尺不足 / window past end）と ffmpeg フィルタグラフ（overlay/blend）と `film_offset_sec` の読み込みをそのまま |
| `scripts/gen_captions_cleveland.py` | **複製元。** `internal_split()` / `chunk_sentence()` / `NO_DANGLE_END` import をそのまま |
| `scripts/build_caniglia_bgm_real.py`（EP43） | **複製元。** narration＋BGM ミックスで基底 mp4 を作る経路（**OFF=11.5 に差し替え**） |
| `scripts/check_cleveland_facts.py` | **複製元（正確性ゲート）。** 構造ルールの除外実装（`asset_manifest` を R-NUM から除外・`index`/geometry キー除外・`kind!="acttitle"` 条件＝EP45修正）を**そのまま流用**（§2.3） |
| `remotion/src/compositions/CaseFilm.tsx` | `FilmData` 型 / `caseFilmDurationInFrames`（**4項・§5.1.1**）/ `depthSrcOf()` |
| `remotion/src/components/FigureBeats.tsx` | `FigureSpec` の**実在する `kind` 文字列**（§6.2・**全小文字**・**`dochighlight` は union に在るが使わない**） |
| `remotion/src/components/Bookends.tsx` | `OPENING_SEC=3.5` / `ENDCARD_SEC=9` / `BrandOpening` / `BrandEndcard` |
| `scripts/check_asset_reuse.py` / `scripts/check_motion_density.py` / `scripts/check_animation_mix.py` / `scripts/check_caption_breaks.py` / `scripts/check_script_length.py` | 通すべき5ゲートの**実際の判定ロジック**（§9） |
| `C:\Users\aab15\Documents\pino-channel\remotion\src\Opening.tsx` | §10 の OP 正典実装 |

---

# 0.5 ★★★ EP39-46 で踏んだ失敗＝最初から防ぐ（本書の全体設計はこの6点を構造で潰している）★★★

1. **紙芝居（最重要・★EP45 の直接死因）** — 静止画100%で組むと `check_animation_mix` が FAIL する。**EP45 は build_cleveland_film が manifest の `factory[]`/`motion[]` を空で受け取り、footage が0本で紙芝居化した。**
   → **`build_atwater_film.py` は `public_items(manifest,"factory")` が 92本・`public_items(manifest,"motion")` が 16本を返すことを起動時に assert し、0本なら exit 1 で A に差し戻す。** `check_animation_mix.compute_metrics_from_film()` は film.json の `cuts[]` を **`kind=="img"` → still / それ以外 → footage** と分類する。§5 の cuts は **factory 92 + motion 32 の footage を最初から入れて still-share を cut数ベース 0.4489・frame ベース ~0.42** にする。
2. **AEカードは密度に数えられない** — `check_motion_density` は film.json の `graphics+figures+heroCuts` **のみ**数える。AEカードは ffmpeg 後合成なので**1本も数えられない**。→ §6 で **film.json 側の `figures[]` を 36本**（spec floor 30 に **+6**・`graphics[]=[]`）置く。AEカードは別勘定。
3. **FigureSpec の `kind` は実在の小文字値のみ** — 大文字名（`ActTitle`/`QuoteCard`/`VoteTally` 等）は無言で描画が消える（§6.2）。**★`dochighlight` は union に在るが1本も使わない**（黒バー/box/underline がバグに見える＝3回指摘・R-DOCHL）。
4. **台帳に無い数値を焼くな** — EP40 の生 Codex-B 出力に架空の $580,000 が入って不採用になった実害。→ §2 の事実台帳 A-ID に**検証済み値だけ**を置き、`check_atwater_facts.py` が film.json/AE/サムネ/props の全数値を台帳照合する。台帳外・`confidence:medium` の断定は FAIL（**$50/2001 のみ断定・1997/子の年齢はヘッジ**）。
5. **字幕は台本本文と対応** — EP38 で台詞混入・「final」誤称の実害。→ §8 の字幕は **narration_index の実チャンク文をそのまま** verbatim で使う（自作しない）。
6. **レンダー前ゲート＋public_slim staging** — build 後に5ゲートを**全部**通す（animation_mix を忘れるな）。**★render 前に `public/atwater` → `public_slim/atwater` へ全メディア（img/factory/motion/audio/overlay）をコピーする**（EP45 は `public_slim` が空でレンダが素材欠落した実害・§13）。

---

# 2. ★ EP47固有の正確性6制約・事実性ロック（`scripts/check_atwater_facts.py`・BLOCKING）

> **この節に違反した成果物は、他が全て完璧でも出荷不可。** 検査対象は film.json の figures/captions、AE beats、
> サムネ、props、固定コメント、`03_script/script.en.v001.md`、（存在すれば）マニフェストの tags/caption_hint/qc.notes の**全文字列と全数値**。
> **正確性ゲートはこの1本に統一（`check_atwater_facts.py`）。DESIGN/CODEX_A も同名を参照する（別名を作らない）。** 出力 `09_package/facts_lock.v001.json`。

## 2.1 正確性6制約（全出力に適用・違反は BLOCKER）

| # | 制約 | 許可される表現 | 禁止 |
|---|---|---|---|
| C-1 | **逮捕は合憲＝UPHELD（5-4）。「違法」化しない** | 「the Court UPHELD the arrest」「constitutional」「the police COULD do this」「allowed, not required」「the arrest stands」。逮捕を語るカードは "constitutional/upheld/allowed" 枠 | 「the arrest was illegal」「unconstitutional arrest」「the Court struck it down」「the Court banned this」「police can't arrest you for a ticket」 |
| C-2 | **Souter 多数意見＝concession＋立法救済** | 「Justice Souter, for the Court」「a pointless indignity, yet permitted」「the fix belongs to legislatures」「many states have legislated limits」。`pointless indignity` を含む Souter カードに「yet allowed / permitted」枠を同一 payload に併記 | 「Souter dissented」「the Court said the arrest was wrong」「Souter struck it down」 |
| C-3 | **O'Connor＝反対意見（対抗軸）・中立帰属** | 「Justice O'Connor, dissenting」「the dissent argued」「four votes, not five」。O'Connor 逐語は**反対意見**として帰属 | O'Connor 逐語を **Court/majority** に帰属／「O'Connor wrote for the Court」／`dissent` を落として引用 |
| C-4 | **票決 5-4・中立** | 「five to four」「5 / 4」「Souter maj: Rehnquist, Scalia, Kennedy, Thomas」「O'Connor diss: Stevens, Ginsburg, Breyer」 | 6-3/7-2 等の誤票決／党派断定 |
| C-5 | **Gail Atwater＝R2・象徴のみ・子ども非扇情** | 事件主体としての名（"Gail Atwater was arrested"）。ビジュアルは二車線の道・ピックアップ車内・空のチャイルドシート2つ・外れたシートベルトのバックル・手錠・留置のブッキング台/booking カメラのフラッシュ・$50の罰金票・天秤・最高裁列柱/9席・開いた扉と閉じた扉（救済は立法へ） | 顔・肖像・身体・人物化／`Atwater` 直後60字の `face`/`portrait`／泣く子・困窮の煽情／**子どもの年齢を画面に出す** |
| C-6 | **数値は台帳一致・$50/2001 のみ断定・medium はヘッジ** | 画面数値は §2.2 の台帳のみ。`$50`（罰金上限・high）・`2001`（判決年・high）・`532 U.S. 318`（cite・high）・`5-4`（high）。逮捕年 **1997** と子の年齢は confidence:medium → **画面に出さない**（narration verbatim 内は可） | 台帳外の金額・年・件数／`1997` を確定カードに焼く／子の年齢（`3`/`5` 歳）を焼く |
| R1 | **実在人物の顔・肖像を生成しない** | 全生成ビジュアル表示中は `AI-assisted visualization`（右下）常時／概要欄1行AI開示 | 認識可能な人物・読める偽公文書 |
| ★DH | **dochighlight 不使用** | 判読ハイライトの意図は `quote`/`stat`/`lowerthird`/`kinetic` で代替 | `figures[].kind`/beats/レイアウト名に `dochighlight`/`DOCHIGHLIGHT` を1件でも出す |

**★禁止語（`check_atwater_facts.py` が全文字列を case-insensitive 部分一致で検査。1件でも FAIL）:**
`the arrest was illegal` / `illegal arrest` / `unconstitutional arrest` / `the arrest was unconstitutional` / `the court struck it down` / `struck down the arrest` / `the court banned` / `police cannot arrest you` / `police can't arrest you for a ticket` /
`souter dissented` / `o'connor wrote for the court` / `o'connor, for the court` / `the majority dissented` /
`poverty porn` / `crying child` / `weeping mother` / `starving child`.
> **★重要な設計注意:** 台本本文（＝字幕 verbatim）には「is not that it was illegal. It is that it was allowed」「call it unconstitutional at least gives you somewhere to go」など
> **否定/正確文脈の語**（`illegal`/`unconstitutional`）が含まれる。上の禁止語リストは**それらと衝突しない断定形だけ**（`the arrest was illegal` 等の主語付き断定）を選んである。**禁止語リストに `illegal`/`unconstitutional` の単語単独を足すな**（字幕 verbatim を巻き込んで false FAIL する）。C-1/C-2/C-3 の**枠付き/帰属**は下の**文脈ルール**（R-DISPO/R-QUOTE）で捕える。

## 2.2 事実台帳 A-ID（`03_script/atwater_facts.v001.json`・**Bが `EP47_atwater_facts.v001.json` の ledger A01–A20 から転記して作る**）

**スキーマ版:** `atwater_facts.v1`。各 A-ID は `{"value":..., "unit":..., "verified":bool, "confidence":"high|medium", "claim_id":"", "attribution":"", "quote":""}`。
**ledger に裏付けのある値だけ `verified:true`。confidence:medium（`A18` 逮捕年1997・`A19` 子の年齢・`A20` 手続履歴）は `画面に出さない`＝figures/AE/サムネ/props に焼かない（narration verbatim 内のみ許可）。**

| A-ID | 内容 | 使う場所 | claim | conf |
|---|---|---|---|---|
| A01 | Gail Atwater・Lago Vista, TX・**R2 存命私人・非有罪（罰金のみ）**・子ども2人（象徴のみ） | fig pindropmap/lowerthird / AE 背景 | A01 | high |
| A02 | シートベルト違反＝軽罪・**罰金刑のみ・投獄不能**（TX $25-$50） | fig compbars/stat / AE c01/n01 | A02 | high |
| A03 | **罰金上限 $50**（no contest で $50 支払）＝逮捕は刑罰ではない | fig stat/numberticker / AE s01 | A03 | high |
| A04 | 逮捕officer＝**Bart Turek**（Lago Vista PD） | fig lowerthird（帰属） | A04 | high |
| A05 | 逮捕＝**手錠（後ろ手）・パトカー・署へ**・子は隣人が保護 | fig routemap / caption | A05 | high |
| A06 | ブッキング＝靴/所持品・撮影・**約1時間留置**→保釈 | fig stat（"about an hour" は語で） | A06 | high |
| A07 | **no contest→$50 罰金支払**・逮捕は刑罰でない | fig stat / caption | A07 | high |
| A08 | **42 U.S.C. § 1983** 提訴（市/署/Turek）・**第4修正**不合理押収 | fig lowerthird ×2 | A08 | high |
| A09 | **probable cause は争いなし**（PC 単独で十分かが争点） | fig probablecause | A09 | high |
| A10 | **HOLDING＝合憲（UPHELD）**：PC があれば軽罪でも令状なし逮捕は第4修正に反しない | fig stat/compbars / AE c01 | A10 | high |
| A11 | 票決 **5-4**（Souter maj: Rehnquist/Scalia/Kennedy/Thomas ／ O'Connor diss: Stevens/Ginsburg/Breyer） | fig votetally/stat / AE v01 | A11 | high |
| A12 | 法廷意見執筆＝**Justice David Souter** | fig lowerthird/quote 帰属 | A12 | high |
| A13 | Souter 論拠＝**コモンロー史＋bright-line rule** | fig brightline/mechanism | A13 | high |
| A14 | Souter 逐語（**多数意見・concession**）"Atwater's claim to live free of pointless indignity and confinement clearly outweighs anything the City can raise against it specific to her case." | fig quote / AE q02 | A14 | high |
| A15 | Souter＝**救済は立法へ**（多くの州が制定済み） | fig mechanism/kinetic / AE l01 | A15 | high |
| A16 | O'Connor 反対の核＝**PC 単独では不十分・reasonableness balancing・罰金のみは citation を原則** | fig compbars / AE 背景 | A16 | high |
| A17 | O'Connor 逐語（**反対意見**）"The Court neglects the Fourth Amendment's express command in the name of administrative ease. In so doing, it cloaks the pointless indignity that Gail Atwater suffered with the mantle of reasonableness." | fig quote / AE q01 | A17 | high |
| A18 | 逮捕年 **1997**（medium・**画面に出さない**）／判決日 **2001-04-24**（high） | 2001 のみ fig/AE 可 | A18 | mixed |
| A19 | 子ども2人＝young（**年齢を画面に出さない**・medium） | narration のみ | A19 | medium |
| A20 | 手続＝地裁→第5巡回 en banc→最高裁 affirmed（medium・任意） | fig timeline（任意・年数字を焼かない） | A20 | medium |

> **数値の許可集合（R-NUM・narrative figure のみ対象）:** `4（Fourth）/ 5 / 25 / 42（§1983）/ 50 / 318 / 532 / 1983（＝§1983 の条番号・年ではない）/ 2001`。**これ以外の金額・年・件数が figures/AE/サムネ/props に出たら FAIL。** `1997`（逮捕年・A18 medium）と子の年齢は**画面禁止**（narration verbatim 内は R-NUM 対象外＝§2.3 の構造除外と別に script.md は verbatim 例外）。

## 2.3 `check_atwater_facts.py` の検査（exit 0=PASS / 1=FAIL / 2=スキーマ不一致）

**★複製元 `check_cleveland_facts.py` の構造除外を1行も削らない（EP45修正）:**
- `asset_manifest*.json` は **R-NUM の対象から除外**（`if not path.name.startswith("asset_manifest")` で構造カウント 85/16/92/12 を巻き込まない）。
- `start/end/dur/fps/width/height/frames/duration_sec/x/y/index` キーは**構造値**として R-NUM スキップ（`acttitle` の `index` 等）。
- 文脈ルールは `kind != "acttitle"` のとき発火（幕頭タイトルを巻き込まない）。

**検査対象ファイル（この一覧をハードコード。存在するものだけ検査し、無いものは `skipped[]` に必ず明記）:**

```
episodes/PD-2026-047-atwater/03_script/script.en.v001.md
episodes/PD-2026-047-atwater/03_script/atwater_facts.v*.json
episodes/PD-2026-047-atwater/08_edit/ae_hero/beats.json
episodes/PD-2026-047-atwater/09_package/*.json        （title / description / thumbnail headlines）
episodes/PD-2026-047-atwater/09_package/*.txt         （固定コメント・description.txt）
episodes/PD-2026-047-atwater/05_visuals/asset_manifest*.json  （tags / caption_hint / qc.notes・★R-NUM 除外）
remotion/src/data/atwater_film.json                   （figures[].text / figures[].lines[] / figures[].kind / captions[] の全文字列と数値）
remotion/props/atwater*.json                          （title / subtitle）
```

- **R-FORBID（最優先）** — §2.1 の禁止語（主語付き断定形）が対象文字列に出たら即 FAIL。**`illegal`/`unconstitutional` の単独単語を禁止語に足さない**（字幕 verbatim を巻き込む・§2.1 注意）。
- **R-DISPO（C-1・BLOCKING）** — 逮捕の処分を語る payload（`arrest` かつ `court`/`held`/`ruling` を含む）は「upheld / constitutional / allowed / could / stands」のいずれかを同伴。§2.1 の C-1 断定禁止語（`the court struck it down` 等）が出たら FAIL。**「5-4」を出すカードは "UPHELD/THE ARREST STANDS/constitutional" を同一 payload に持つ**（違法と読ませない）。
- **R-QUOTE（C-2/C-3・R-ATTRIB・BLOCKING）** — `quote[].attribution` は非空・逐語のみ（要約を引用符に入れない）。許可対応表:
  ```python
  APPROVED_QUOTES = {
    "atwater's claim to live free of pointless indignity and confinement clearly outweighs anything the city can raise against it specific to her case":
        "Justice Souter, for the Court",                       # A14（多数意見・concession・逐語）
    "the court neglects the fourth amendment's express command in the name of administrative ease. in so doing, it cloaks the pointless indignity that gail atwater suffered with the mantle of reasonableness":
        "Justice O'Connor, dissenting",                        # A17（反対意見・逐語）
  }
  ```
  **Souter 逐語に `for the court`/`majority` 以外の帰属、O'Connor 逐語に `dissent`/`dissenting` 以外の帰属が付いたら FAIL。** `pointless indignity` を含む Souter payload に `yet`/`permitted`/`allowed`/`still` の concession-then-permit 枠が無ければ FAIL（C-2）。
- **R-FACE（C-5/R1）** — `has_readable_text`/`has_identifiable_face`/`has_human_body` が true の項目は `role=="reject"`。`ai_prompts.v001.md` 正プロンプトの `portrait`/`face of`/`likeness`/`Gail Atwater`（人物として）/`her body`/`her children`（描写として）/`crying child`/`weeping mother` は FAIL（ネガティブでの使用は可）。`Atwater` 直後60字の `face`/`portrait`、子の年齢語（`3-year-old`/`5-year-old`/`aged 3`/`aged 5`）で FAIL。生成ビジュアル区間の `AI-assisted visualization` 欠落・`description.txt` の AI 開示行欠落で FAIL。
- **R-NUM（C-6・narrative のみ）** — figures[] の `value`/`numKeys` 到達値、AE `beats[].value`/`beats[].main`/`beats[].hero`、サムネ数字に現れる**あらゆる数値**は §2.2 許可集合 `{4,5,25,42,50,318,532,1983,2001}` に**完全一致**必須。**`1997` と子の年齢が figures/AE/サムネ/props に出たら FAIL**（A18/A19 は medium・画面禁止）。**★`asset_manifest*.json` は R-NUM 対象外**（構造カウント 85/16/92/12 の false-positive 回避＝EP45修正）。
- **R-HEDGE（C-6）** — `confidence:medium` の A-ID（A18 逮捕年1997・A19 子の年齢・A20 手続）を `verified:true` かつ画面焼き込みしたら FAIL。断定可は **$50（A03）・2001（A18 の判決日部分）・532 U.S. 318・5-4** のみ。
- **R-DOCHL（★DH・BLOCKING）** — `atwater_film.json` の `figures[].kind` に `dochighlight` が1件でも出たら FAIL
  （`grep -c '"kind"[[:space:]]*:[[:space:]]*"dochighlight"'` が 0 でなければ FAIL）。`beats.json`/レイアウト名にも `dochighlight`/`DOCHIGHLIGHT` を出さない。
- **R-DATE** — 判決日 **2001-04-24** と §1983（条番号）を年として取り違えない。1997 を判決年に混同しない。

**出力:** `episodes/PD-2026-047-atwater/09_package/facts_lock.v001.json`（`{"pass":bool,"violations":[{"file","rule","line","excerpt"}],"skipped":[...]}`）。
**`pass:true` でない限り `check_final_acceptance.py` に進んではならない。** **CLI:** `--json`。対象ファイル未生成はスキップして必ずログに出す（「無いから通した」を黙るな）。

---

# 3. ★境界契約: `asset_manifest.v001.json`（Aから受け取る唯一のファイル・FROZEN）

## 3.1 スキーマ（**Aが生成する。Bはこの形を前提に読む・A↔B 1バイト一致**）

**スキーマ版:** `atwater_assets.v1`（固定文字列。異なれば **exit 2**）。
EP47 spec の点数に一致: **still_body 85 / still_i2v_source 16 / motion 16 / factory 92 / overlay 12**。
**★サムネは独立の分類を持たない。** body 85枚のうち**6枚**に `also_thumb:true` を立てて流用する（**`role=thumb`/`still_thumb` を作らない**・サムネ用 count キーも無い・§11）。
**このスキーマ・`counts` キー・`role` enum・`overlay` 枚数は CODEX_A（生産者）の出力と1バイト単位で同一。**

- **`role` enum（固定・3値のみ）:** `"body"` | `"i2v_source"` | `"reject"`。**`thumb`/`still_thumb` を作らない。**
- **`counts`（固定キー・確定値）:** `{ "still_body": 85, "still_i2v_source": 16, "motion": 16, "factory": 92, "overlay": 12 }`。

```jsonc
{
  "schema_version": "atwater_assets.v1",
  "episode_id": "PD-2026-047-atwater",
  "slug": "atwater",
  "generated_at": "<ISO8601>",
  "producer": "scripts/build_atwater_asset_manifest.py",
  "is_stub": false,
  "counts": { "still_body": 85, "still_i2v_source": 16, "motion": 16, "factory": 92, "overlay": 12 },

  "stills": [
    { "asset_id": "ATW-S01", "scene_id": "S01", "role": "body",
      "also_thumb": false,                     // body から6枚だけ true（§11 の6 asset ID・追加生成しない）
      "act": 0,                                // 0=HOOK/OP, 1..3=幕, 5=ED
      "public_path": "atwater/img/S01.png",    // ★Bが cuts[].src に入れる値（1シーン1枚＝固有プロンプト・_01 等の接尾なし）
      "depth_path": "H:/pd-media/assets/ai/atwater/S01_depth.png",  // role=="body" は実在必須
      "width": 3840, "height": 2160,
      "sha256": "...", "tags": ["two_lane_road","texas","symbolic"], "caption_hint": "a two-lane Texas road in afternoon light, no people",
      "source": "ai_codex", "commercial_use": "allowed", "ai_disclosure_required": true,
      "qc": {"reviewed": true, "on_theme": true,
             "has_readable_text": false, "has_identifiable_face": false, "has_human_body": false, "notes": ""} }
    // i2v 種は role=="i2v_source"・asset_id "ATW-MS01".."ATW-MS16"・public_path は null（本編カットに出ない）
  ],

  "motion": [   // ★16本。build_atwater_film が public_items(manifest,"motion") で全読込（空なら exit 1）
    { "asset_id": "ATW-M01", "source_scene_id": "M01_src",
      "source_still": "H:/pd-media/assets/ai/atwater/M01_src.png",
      "public_path": "atwater/motion/M01_rife.mp4",   // ★必ず .mp4 かつ "_rife" を含む
      "act": 0, "width": 1280, "height": 720, "fps": 48, "frames": 164, "duration_sec": 3.417,
      "sha256": "...", "tags": ["unbuckled_seatbelt","pickup_cab"],
      "qc": {"reviewed": true, "on_theme": true, "artifact_free": true, "notes": ""} }
  ],

  "factory": [  // ★92本。build_atwater_film が public_items(manifest,"factory") で全読込（空なら exit 1）
    { "asset_id": "AF-BG-0731",
      "public_path": "atwater/factory/AF-BG-0731__two_lane_texas_road.mp4",  // ★必ず "/factory/" を含む
      "type": "backgrounds", "subtype": "road", "kind": "video",
      "license": "Pexels License", "sha256": "...", "act": 1, "covers_scene_id": "S04",
      "duration_sec": 7.60, "width": 1920, "height": 1080,
      "eyeballed_content": "a two-lane rural road in cold afternoon light, no people, no readable plates",
      "qc": {"reviewed": true, "on_theme": true, "no_watermark": true,
             "no_recognizable_person": true, "no_cartoon": true, "label_matches_content": true, "notes": ""} }
  ],

  "overlay": [  // ちょうど12本。cuts[].src に出さない（§5.5）
    { "asset_id": "AF-PART-0044",
      "public_path": "atwater/overlay/AF-PART-0044__dust_motes.mp4",
      "type": "particle_assets", "subtype": "dust_motes", "license": "Pexels License",
      "sha256": "...", "blend_hint": "screen",
      "eyeballed_content": "slow drifting dust on black, loops cleanly",
      "qc": {"reviewed": true, "on_theme": true, "no_watermark": true, "notes": ""} }
  ]
}
```

## 3.2 Bがこのマニフェストから作るもの（**EP47 spec の cuts 割当**）

| マニフェスト | Bでの使い道 | spec |
|---|---|---|
| `stills[role="body"]` 85枚 | **静止画カット101本**（`kind:"img"`, `treatment` 循環）・**各≤2回** | still distinct85/cuts101 |
| body 静止画で `also_thumb==true` の6枚 | サムネ3案の背景（§11・6 asset ID） | — |
| `stills[role="i2v_source"]` 16枚 | **本編カットに出さない**（i2v 種・A が Wan で motion 化済み） | — |
| `motion` 16本 | **i2vカット32本**（`kind:"footage"`）・**各≤2回** | motion distinct16/cuts32 |
| `factory` 92本 | **実写カット92本**（`kind:"footage"`）・**各1回のみ** | factory distinct92/cuts92 |
| `overlay` 12本 | **`cuts[].src` に出さない**（§5.5 の合成レイヤー扱い） | — |

**合計 101 + 32 + 92 = 225 カット / distinct 85+16+92 = 193 / first-use 193/225 = 0.8578 ✓（floor 0.70）**

## 3.3 `scripts/check_atwater_asset_manifest.py`（消費側バリデータ・BLOCKING）

```bash
$PY scripts/check_atwater_asset_manifest.py --assets <path> [--json]
```

検査（1つでも違反で exit 1。`schema_version` 違いだけ exit 2）:

1. `schema_version=="atwater_assets.v1"` / `episode_id=="PD-2026-047-atwater"` / `slug=="atwater"` / `is_stub==false`
2. `counts.*` が各配列の実長と一致し**確定値**: `still_body==85` / `still_i2v_source==16` / `motion==16` / `factory==92` / `overlay==12`
3. `role` は **`body`/`i2v_source`/`reject` の3値のみ**（`thumb`/`still_thumb` が現れたら FAIL）
4. `role=="body"` の全静止画で `public_path` 非null、かつ `remotion/public/<public_path>` と `<stem>_depth.png` が**両方実在**（`depthSrcOf()=src.replace(/\.[^.]+$/,'_depth.png')`。depth 欠落はレンダークラッシュ）。`role=="i2v_source"` は `public_path==null`
5. `role!="reject"` の全静止画で `max(width,height)>=3840`（`preflight_render_gate.MIN_LONG_EDGE_PX=3840`）
6. `motion[].public_path` が `.mp4` で終わり `_rife` を含む。`motion[].source_scene_id` は `stills[role=="i2v_source"]` の種 ID（`M01_src` 系）を指す
7. `factory[].public_path` が `/factory/` を含む
8. `overlay[].public_path` が `/overlay/` を含み `/factory/` を**含まない**・`overlay` 配列長が**ちょうど12**
9. `sha256` が全配列を通して一意（EP39〜46 の素材と sha256 被りゼロは A が保証・B は自集合内一意を検査）
10. `factory[].eyeballed_content` が非空、かつ `qc.label_matches_content==true`
11. `qc.has_readable_text` / `qc.has_identifiable_face` / `qc.has_human_body` が true の項目は `role=="reject"`（R1）
12. `also_thumb==true` の body 静止画が**ちょうど6枚**、かつ **`scene_id` 集合が §11 の6 ID と完全一致**（A↔B 契約点。**CODEX_A の also_thumb 集合と一字一致**）
13. **全文字列値**が §2 の R-FORBID / R-FACE / R-DOCHL を通る（**R-NUM は asset_manifest を除外**＝§2.3）

> **★このバリデータは A の `--verify` と同じ不変条件を独立実装する（二重チェック）。** counts が §3.1 の確定値と食い違ったら組まずに止めて A に差し戻す（ブリーフ§2: still を増やして factory を削るな）。**★特に `factory==92` と `motion==16` が非0であることを最優先で assert（EP45 空配列事故の直接防止）。**

---

# 4. narration_index（TTS は課金＝禁止。**実測版を消費**する）

## 4.1 なぜ narration_index か
`build_atwater_film.py` は**尺・区間・字幕を narration_index から導出する**。**秒数をコードに直書きしない。** 唯一の正は narration_index。

## 4.2 スキーマ（`atwater_narration.v1`）

```jsonc
{
  "schema_version": "atwater_narration.v1",
  "episode_id": "PD-2026-047-atwater",
  "is_stub": false,
  "total_seconds": 719.3,        // = SPEC narration_seconds（[SILENCE 1] の実音無音を含む）
  "chunks": [
    { "section": "HOOK", "start": 0.000, "end": 4.100, "text": "..." },
    { "section": "OP",   "start": 60.000, "end": 64.100, "text": "..." },
    { "section": "ACT_1","start": 124.000, "end": 128.200, "text": "..." }
  ]
}
```

**section 値（固定・6幕）:** `HOOK` / `OP` / `ACT_1` / `ACT_2` / `ACT_3` / `ENDING`。**ACT_4 は無い。**
`build_atwater_film.py` は `section_windows()`（各 section の最初のチャンク start）で幕境界を得る。
**台本の `【SILENCE 1 — 1.8s】` は HOOK 内1箇所**（外れたシートベルトのホールド・完全無音）。narration_index の実測がこの無音を **total_seconds に内包**している。**存在しない演出マーカーを発明しない。**

## 4.3 spec のタイムライン（**設計目標。実タイミングは narration_index が上書きする**）

| section | 語数 | 秒（目安） | 備考 |
|---|---|---|---|
| HOOK | 174 | 58.6 | VO。途中に `SILENCE 1 — 1.8s`（外れたシートベルトの残響・完全無音） |
| （gold `BrandOpening`） | 0 | 3.5 | 非VO。`OPENING_SEC`。**HOOK の問いが landした後に resolve**（frame0 ではない） |
| OP | 190 | 64.0 | 二人称の thesis ＋ "THE FIFTY DOLLAR ARREST" タイトル＋ channel ID |
| ACT_1 The stop | 369 | 124.3 | 最短・抑制。シートベルト→手錠→ブッキング→$50 |
| ACT_2 The § 1983 question | 408 | 137.5 | 罰金のみの逮捕は不合理な押収か・第4修正・probable cause 争いなし |
| ACT_3 The ruling | 561 | 189.0 | **最も遅く長い**。5-4・Souter 史/bright-line/concession/立法救済・O'Connor 逐語（反対） |
| ENDING | 383 | 129.0 | ペイオフ→CTA。"they may, not must"・"allowed, not illegal"・立法に委ねられた不満 |
| （`BrandEndcard`） | 0 | 9.0 | 非VO。`ENDCARD_SEC` |

**唯一の正は `python scripts/check_script_length.py <script> --json`。** 総語数 **2,135**（spec `words_total`）/ `wpm 178.1` /
narration_seconds **719.3**（spec）。**自己申告・体感の尺判定は禁止。**

## 4.4 実測 narration_index の受領
本番は別工程が TTS→faster-whisper で `06_audio/narration_index.v001.json`（実測語タイム・`is_stub:false`）を作る。
**これは課金ジョブなので B は起動しない。** 来た `narration_index.v001.json` を `--narr` に渡すだけ。**台本本文はそのまま（改変しない）。**

---

# 5. `atwater_film.json` の構築（`scripts/build_atwater_film.py`＝`build_cleveland_film.py` の複製・実素材のみ）

## 5.1 `FilmData` 型（`CaseFilm.tsx` から。これに従う）

```ts
export type Cut = {start:number; dur:number; kind:'img'|'footage'; src:string; treatment:string; seed:string};
export type FilmData = {
  fps:number; narration:string; narrationSeconds:number; hookSeconds:number; hookLine:string;
  hook:{start:number;dur:number;kind:string;src:string;seed:string}[];
  cuts:Cut[]; captions:{start:number;end:number;text:string}[];
  graphics:{start:number;end:number;lines:string[]}[];      // 必須フィールド。EP47 は []
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
- **`fps = 30`**（film fps）。`narration = "atwater/narration.mp3"`（実在）

### 5.1.1 ★durationInFrames の4項関数（明示・total ≤ 750s を assert）

```
caseFilmDurationInFrames(atwaterFilm, fps=30)
  = round(hookSeconds * fps)        // ★hookSeconds = 8.0（ブリーフ§5 明示）→ round(240) = 240
  + round(OPENING_SEC * fps)        // OPENING_SEC = 3.50（gold BrandOpening は HOOK の後）→ round(105) = 105
  + ceil(narrationSeconds * fps)    // narrationSeconds = narration_index.total_seconds（= 719.3・silence 込み）→ ceil(21579.0) = 21579
  + round(ENDCARD_SEC * fps)        // ENDCARD_SEC = 9.00 → round(270) = 270
```

- **★hookSeconds を明示: `hookSeconds = 8.0`**（EP47 ブリーフ§5・§7 完了条件。frame0 の flash-forward モンタージュ尺として 8.0s を積む。EP45 の 0.0 と異なる＝**必ず 8.0**）。
- 概算（fps30・narration 719.3）: `240 + 105 + 21579 + 270 = 22194 frames = 739.8s`。**★id=Ep47Atwater の durationInFrames は 22194。**
- **ビルダ末尾で `assert total_frames/fps <= 750.0`**（739.8 ≤ 750 ✓）。超えたら exit 1。

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
        still-frame-share = 303.0 / 719.3 = 0.4213          ✓ <=0.45（cut数比より安全側）
        motion-coverage(frame) = 416.6 / 719.3 = 0.5792     ✓ >=0.45

[D] 平均ショット長（spec mean_shot 3.2 / max 6.0）
    719.3 / 225 = 3.197 秒/カット                           ✓ <=6

[E] factory 下限（30秒に1本 = 24 → >=24本） 92本            ✓
```

> **★[C](i) の cut数ベース still-share 0.4489 は cap 0.45 に極めて薄い（余裕 0.11%＝EP45 の 0.36% より更に薄い）。still を1枚増やすか factory を1本削ると即 0.45 超過で FAIL。**
> **マニフェストが still 85 / factory 92 / motion 16 を割ったら組まずに止めて A に差し戻す（ブリーフ§2: still を増やして factory を削るな）。frame ベースも下回るよう still の平均尺を footage より系統的に短く保つ（§5.3-5）。**

## 5.3 カット割り当てのルール（`build_cleveland_film.py` の `allocate()`/`take()`/`repeated()` を踏襲）

1. 各幕の秒窓を `section_windows()` から取り、幕内に **factory : motion : still を按分**（★下表は**非拘束の目安**・実配分は narration_index の窓長で自動調整。確定値は「合計 factory 92 / motion 32 / still 101」だけ）:

   | section | factory | motion | still | 小計 |
   |---|---|---|---|---|
   | HOOK+OP | 12 | 5 | 15 | 32 |
   | ACT_1 | 14 | 5 | 17 | 36 |
   | ACT_2 | 18 | 6 | 20 | 44 |
   | ACT_3 | 30 | 10 | 30 | 70 |
   | ENDING | 18 | 6 | 19 | 43 |
   | **計** | **92** | **32** | **101** | **225** |

2. **factory は各1回のみ**（使用済み集合を持ち二度と引かない）。**motion は各≤2回・still は各≤2回**（`repeated(pool, need, cap, key)`）
3. **同一素材を連続させない**（順序を散らす）
4. 静止画 `treatment` は `["depth","scan","duotone","focus"]` を循環（同じ treatment を3連続させない）
5. **still の `dur` を footage の `dur` より系統的に短く**（§5.2[C]・still 側の重みを小さめに）
6. motion の `dur` は **3.0–3.4秒**（実素材 3.417s。超えるとループが見える）
7. **AEカードの区間（§7.2）に重なるカットも存在させる**（コンポジタ SKIP 時に穴が空かないため）

## 5.4 `figures[]` と `captions[]`
- `figures[]` は §6（**36本**・spec floor 30 に +6・`graphics[]=[]`・**dochighlight 不使用**）
- `captions[]` は narration_index の全チャンクを **verbatim**（`build_captions()` と同一）。SRT も同時出力

## 5.5 合成レイヤー（`overlay`）— **`cuts[].src` に出さない**
`overlay` 12本は「加工」。`cuts[].src` に入れると factory 判定（上限1回）になり FAIL する。
`atwater_film.json` に **`overlays` 独自キー**で持たせる（`CaseFilm` は未知キーを無視）か、専用レイヤーで `screen` 合成する。

## 5.6 ビルダが出力する成果物

| 出力 | パス |
|---|---|
| film.json | `remotion/src/data/atwater_film.json` |
| public コピー | `remotion/public/atwater/film_data.v001.json` |
| **build provenance** | `episodes/PD-2026-047-atwater/04_scenes/atwater_build_manifest.v001.json`（**A の `05_visuals/asset_manifest` に書かない**） |
| **beatsheet**（figures+AE区間の突き合わせ表） | `episodes/PD-2026-047-atwater/04_scenes/atwater_beatsheet.v001.json` |
| SRT（字幕未生成時のフォールバック） | `episodes/PD-2026-047-atwater/08_edit/captions.final.v001.srt`（**§8 の生成器が上書きする**） |

> **★beatsheet の命名に関する重大な注意:** `check_motion_density` / `check_animation_mix` は `04_scenes/premium_beatsheet.v*.json` を**自動検出して film.json より優先**する。
> **B の beatsheet は `atwater_beatsheet.v001.json`（`premium_` を付けない）** にして**ゲートの測定源を film.json 一本に保つ**（二重ソース乖離＝EP39/40 の矛盾28件の原因を避ける）。`atwater_beatsheet` は provenance と `validate_atwater_beats` 専用。

## 5.7 CLI
```bash
$PY scripts/build_atwater_film.py \
  --assets episodes/PD-2026-047-atwater/05_visuals/asset_manifest.v001.json \
  --narr   episodes/PD-2026-047-atwater/06_audio/narration_index.v001.json \
  --out    remotion/src/data/atwater_film.json \
  [--captions episodes/PD-2026-047-atwater/08_edit/captions.final.v001.srt]
```
**実素材のみ。`is_stub==true` のマニフェストを渡されたら exit 1。★`public_items(manifest,"factory")` が空 or `!=92`、`public_items(manifest,"motion")` が空 or `!=16` なら exit 1（EP45 空配列事故防止）。** 末尾に `check_asset_reuse` 相当の自己レポートを print する。

---

# 6. Remotion 側 `figures[]`（**36本・spec floor 30 に +6・`graphics[]=[]`・dochighlight 不使用**）

## 6.1 密度の検算（`check_motion_density`・**AEカードは1本も数えられない**）

```
figures 36本（film.json） / body 11.988分(=719.3/60) = 3.00 /分       ✓ beats_per_min_floor 2.5
coverage: 36本 × 平均6.0s = 216.0s / 719.3 = 30.0%                    ✓ MIN_ANIMATED_COVERAGE 0.25
variety : 下記 kind を16種使用                                        ✓ variety_floor 3
spec motion.beats_floor = 30 に対し 36 で余裕。coverage が最も薄いので figures の dur は 5.4–6.0s を基本に。
```

> **★3軸すべて AND。density/coverage/variety のどれか1つでも floor 未満で FAIL。** 36本を非重複で置き平均 dur を 6.0s 程度に確保。

## 6.2 ★★★ `FigureSpec` の `kind` は**実在する小文字値のみ・`dochighlight` は使わない** ★★★

> **大文字名（`ActTitle`/`QuoteCard`/`VoteTally`…）は `FigureBeats.tsx` の union に無く、無言で描画が消える。`comparebars` は非在→`compbars`。** **★`dochighlight` は union に在るが1本も使わない**（R-DOCHL）。

**EP47 で使う実在 `kind`（`remotion/src/components/FigureBeats.tsx` の union から確認済み・全て `start`/`end` 必須・全小文字）:**

| `kind` | 必須プロパティ | EP47での用途 |
|---|---|---|
| `acttitle` | `title:string` / `kicker?` / `index?` | 幕頭「THE STOP」/「THE QUESTION」/「THE RULING」 |
| `kinetic` | `lines:string[]` / `style?:'wordpop'\|'maskslide'\|'emphasis'` / `emphasisWords?` | "THE FIFTY DOLLAR ARREST" / "ALLOWED, NOT ILLEGAL" / "THEY MAY, NOT MUST"（emphasisWords 1–2語） |
| `stat` | `value:number` / `label:string` / `prefix?` `suffix?` `topLabel?` | $50 MAX FINE（A03）/ NO JAIL（A02）/ 5-4 UPHELD（A11/A10）/ ~1 HOUR は語で |
| `numberticker` | `value:number` / `label?` / `prefix?` `suffix?` `decimals?` | $50（A03）/ 2001（A18 判決年）/ 5-4 |
| `quote` | `quote:string` / `attribution:string` | **Souter 逐語（A14・"for the Court"）/ O'Connor 逐語（A17・"dissenting"）** のみ・§2 `APPROVED_QUOTES` 一致 |
| `lowerthird` | `primary:string` / `secondary?` / `accent?` | 開示 `AI-assisted visualization` / Fourth Amendment / 42 U.S.C. § 1983 / Atwater v. City of Lago Vista, 532 U.S. 318 / Officer Bart Turek（A04 帰属） |
| `compbars` | `items:{label:string;value:number;accent?}[]` | ①FINE-ONLY OFFENSE vs FULL ARREST（A02/A10）②majority: PC enough vs dissent: balance（A16）③citation vs custodial arrest |
| `votetally` | `for?`/`against?`/`labels?`（実在 kind＝`votetally`・**`VoteTally` ではない**） | **5-4**（Souter maj / O'Connor diss・A11・C-4 中立） |
| `timeline` | `events:{year:string;text:string}[]` | 手続: stop → 提訴 → 最高裁 2001 affirmed（A20・年数字を焼くのは 2001 のみ） |
| `pindropmap` | `pins:{x,y,label?}[]` | Lago Vista, Texas（単一ピン・C-5 顔なし・A01） |
| `routemap` | `label?` / `pins:{x,y,label?}[]` | ACT1 の因果の道: stop → handcuffs → squad car → station → cell → magistrate（A05・象徴） |
| `statemap` | `label?` / `states?` | 「some states legislate limits, not the Constitution」（A15・立法救済の地理・過大化しない） |
| `brightline` | `label?` / `lines?` | Souter の bright-line rule（PC があれば逮捕可・A13/A10） |
| `probablecause` | `label?` | probable cause は争いなし（A09） |
| `mechanism` | `mechanism:'closingdoor'\|'gears'\|'faultsplit'` ★discriminant は `kind`・変種は `mechanism` | ①bright-line vs case-by-case(faultsplit)②救済は立法へ＝開いた扉/閉じた扉(closingdoor)(A15) |
| `bar` | `items` or `value` | 「covered only by statute across much of the country」（ENDING・A15） |

**`quote[].attribution` は §2 の `APPROVED_QUOTES` に一致させる。逐語のみ・要約を引用符に入れない。**
**★`kind` に `dochighlight` を1件も置かない（R-DOCHL・`check_atwater_facts` が grep で 0 を確認）。**

## 6.3 figures 配分（**全 36 を figures[]・graphics[]=[]**）

| kind | 枠数 |
|---|---|
| `acttitle` | 3 |
| `kinetic` | 4 |
| `stat` | 6 |
| `numberticker` | 3 |
| `quote` | 2 |
| `lowerthird` | 4 |
| `compbars` | 3 |
| `votetally` | 1 |
| `timeline` | 2 |
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

- **HOOK/OP（6）:** `lowerthird`（`AI-assisted visualization` 開示）/ `kinetic`（"THE FIFTY DOLLAR ARREST"）/ `pindropmap`（**A01 Lago Vista, Texas**・単一ピン）/ `stat`（**A03 $50**, label "MAXIMUM FINE — NO JAIL"）/ `kinetic`（"HANDCUFFS FOR FIFTY DOLLARS?"・emphasisWords=["FIFTY"]）/ `lowerthird`（**Atwater v. City of Lago Vista, 532 U.S. 318**）
- **ACT_1（7）:** `acttitle`（THE STOP）/ `routemap`（stop→handcuffs→squad car→station→cell→magistrate・A05）/ `lowerthird`（**Officer Bart Turek** — Lago Vista PD・A04 帰属）/ `stat`（**A02 NO JAIL**, label "the entire penalty is a fine"）/ `numberticker`（**A03 $50**, label "no contest — fine paid"）/ `compbars`（**$50 fine（the sentence）vs handcuffs+cell+booking（before any verdict）**・A02/A07）/ `stat`（**A06** booking, label "shoes, possessions, about an hour in a cell"／数字は語で "about an hour"）
- **ACT_2（8）:** `acttitle`（THE QUESTION）/ `lowerthird`（**The Fourth Amendment** — unreasonable searches and seizures・A08）/ `lowerthird`（**42 U.S.C. § 1983** — sue an official for a constitutional violation・A08）/ `probablecause`（**A09** probable cause conceded — the fight is what it justifies）/ `compbars`（**Atwater: fine-only → write a citation** vs **City: probable cause → full arrest**・A16/A10）/ `brightline`（**A13** the city's rule: PC for any offense = arrest allowed）/ `kinetic`（"IS PROBABLE CAUSE ENOUGH?"）/ `stat`（**A02** fine-only offense, label "no jail time exists for this crime"）
- **ACT_3（10）:** `acttitle`（THE RULING）/ `timeline`（**A20** the stop → the § 1983 suit → the Supreme Court, **2001** affirmed／★年数字は 2001 のみ・1997 を焼かない）/ `votetally`（**5-4**・A11・for=5 against=4・C-4 中立）/ `stat`（**A10/A11 5-4**, label "THE ARREST STANDS — constitutional"・topLabel "UPHELD"／**C-1 違法と読ませない**）/ `quote`（Souter 逐語 A14 → "Justice Souter, for the Court"／**concession**・C-2）/ `mechanism:faultsplit`（**A13** bright-line rule vs case-by-case balancing）/ `compbars`（**A16** majority: PC is enough vs dissent: reasonableness must balance）/ `quote`（O'Connor 逐語 A17 → "Justice O'Connor, dissenting"／**反対**・C-3・R-QUOTE）/ `numberticker`（**A18 2001**, label "decided — Supreme Court"）/ `mechanism:closingdoor`（**A15** the fix belongs to legislatures — a door left to the states）
- **ENDING（5）:** `kinetic`（"ALLOWED, NOT ILLEGAL"・emphasisWords=["ALLOWED"]／**C-1**）/ `stat`（**A03 $50**, label "the whole penalty — yet the arrest was allowed"）/ `statemap`（**A15** some states legislate limits — the Constitution does not）/ `bar`（**A15** across much of the country, covered only by statute — not the Fourth Amendment）/ `lowerthird`（開示 `AI-assisted visualization` 再掲）

> **★逮捕の処分を出す payload には必ず "UPHELD/THE ARREST STANDS/constitutional/allowed"（C-1・R-DISPO）。「illegal arrest」「struck down」を書かない。**
> **Souter 逐語（A14）は "for the Court" 帰属＋concession（pointless indignity, yet permitted）。O'Connor 逐語（A17）は "dissenting" 帰属（Court に帰属させない・C-3）。** **1997・子の年齢を `value`/`numKeys`/label に焼かない（R-HEDGE/R-NUM）。**

## 6.5 配置ルール
1. **AEの区間（§7.2）と1秒でも重ならない**（`validate_atwater_beats` が突き合わせ）
2. **同じ kind を連続させない**（`mechanism` の直後に `mechanism` を置かない）
3. 1枠 **5.4–6.0秒**
4. `quote[].quote` / `kinetic[].lines` / `*.label` は §2 の R-NUM・R-QUOTE・R-FORBID・R-DISPO・R-FACE・R-DOCHL 検査対象
5. 台帳外の数値・`1997`・子の年齢を `value`/`numKeys` に置かない（**焼いたら R-NUM/R-HEDGE で FAIL**）
6. **`emphasisWords` は1–2語の短句のみ**（長句は末尾切れ＝EP40 実害）
7. **`kind` に `dochighlight` を1件も置かない（R-DOCHL）**

---

# 7. After Effects カード（`build_atwater_hero_cards.py` / `composite_atwater_hero.py`）

## 7.1 位置づけ
AEカードは **film.json とは別**に ffmpeg で本編に焼き込む（§0.5-2＝密度に数えられない）。
`build_cleveland_hero_cards.py` を**コピーしてパス・定数・CARDS デッキだけ差し替える**。レイアウト実装・`money_keys()`・`fit_size()`・完了マーカー・機械の罠対処は**1行も削らない**。

## 7.2 AEカードデッキ（**単調増加・重複ゼロ・台帳裏付けのみ・6制約順守。この表が契約。8枚＝ブリーフ§6 VERBATIM**）

**区間の秒は本番の rendered base（narration_index 由来）に一致させる。** 下表の秒は spec タイムライン基準の**目安**で、`build_atwater_hero_cards.py` は section 窓からオフセットで算出しクランプする。**背景静止画は象徴オブジェのみ（R1/C-5）。**
**★この表は DESIGN §6 と id・レイアウト・A-ID・順序（start 昇順）が一字一致。**

| id | レイアウト（**実装済み8種の内・§7.3**） | hero/main（主表示） | top / bottom / left / right / attribution | A-ID | 背景（象徴のみ） | required |
|---|---|---|---|---|---|---|
| s01 | CENTER_STACK | **$50** | top: **MAXIMUM FINE** / bottom: **NO JAIL — THIS IS THE ENTIRE PENALTY** | A03 | $50の罰金票（判読不能・violet） | 必須 |
| n01 | CENTER_STACK | **NO JAIL OFFENSE** | top: **A FINE-ONLY MISDEMEANOR** / bottom: **THE MOST THE LAW CAN DO IS TAKE FIFTY DOLLARS** | A02 | 外れたシートベルトのバックル | 必須 |
| c01 | SPLIT_COMPARE | left: **FINE-ONLY OFFENSE** / right: **FULL ARREST** | top: **WHAT THE COURT ALLOWED** / bottom: **PROBABLE CAUSE WAS ENOUGH** | A10/A02 | 左=citation 票 / 右=手錠 | 必須 |
| d01 | DATE_STAMP | **APRIL 24, 2001** | place: **ATWATER v. CITY OF LAGO VISTA — 532 U.S. 318** | A18 | 大理石の最高裁列柱（顔なし） | 必須 |
| v01 | VOTE_SPLIT | **5 / 4** | top: **THE ARREST STANDS** / bottom: **CONSTITUTIONAL — SOUTER MAJORITY, O'CONNOR DISSENT** | A11/A10 | 9席のベンチ（象徴・顔なし） | 必須 |
| q02 | CENTER_STACK | **POINTLESS INDIGNITY** | top: **THE MAJORITY CALLED IT THIS** / bottom: **JUSTICE SOUTER, FOR THE COURT — YET PERMITTED IT** | A14 | 手錠＋$50票（concession） | 必須 |
| q01 | QUOTE_CARD | **"THE COURT NEGLECTS THE FOURTH AMENDMENT'S EXPRESS COMMAND IN THE NAME OF ADMINISTRATIVE EASE. IN SO DOING, IT CLOAKS THE POINTLESS INDIGNITY THAT GAIL ATWATER SUFFERED WITH THE MANTLE OF REASONABLENESS."** | attribution: **JUSTICE O'CONNOR, DISSENTING** | A17 | 大理石の第4修正（判読困難・顔なし） | 必須 |
| l01 | CENTER_STACK | **LEFT TO LEGISLATURES** | top: **THE MAJORITY'S REMEDY** / bottom: **NOT THE FOURTH AMENDMENT — A DOOR LEFT TO THE STATES** | A15 | 開いた扉と閉じた扉 | 必須 |

> **★行順＝start 昇順（時系列）:** `s01`(ACT1) < `n01`(ACT1) < `c01`(ACT2) < `d01`(ACT3 open) < `v01`(ACT3 vote) < `q02`(ACT3 Souter) < `q01`(ACT3 O'Connor) < `l01`(ACT3→END)。
> **★制約:** `v01`（5-4）は "THE ARREST STANDS / CONSTITUTIONAL" を削除禁止（**C-1 違法と読ませない**）。`q02`（Souter）は "FOR THE COURT — YET PERMITTED IT" を削除禁止（**C-2 concession-then-permit・多数意見帰属**）。`q01`（O'Connor）の attribution は **"JUSTICE O'CONNOR, DISSENTING"**（Court に帰属させない・**C-3**）・quote は §2 `APPROVED_QUOTES` の逐語のみ（要約を引用符に入れない）。
> **どのカードにも「the arrest was illegal」「the Court struck it down」「O'Connor, for the Court」を書かない**（C-1/C-3）。**1997・子の年齢を焼かない（R-HEDGE）。** 数値ID＝台帳（§2.2）と一致必須。カウント終了から区間終端まで最低 **1.20秒**ホールド。

**検算（Codex は自分で再計算して一致を確認）:** 8区間・単調増加・重複ゼロ・HOOK(0–58.6) と ENDCARD(末尾9s) に重ねない。Remotion figures(§6) と1秒も重ならない（`validate_atwater_beats`）。

## 7.3 レイアウト（`build_cleveland_hero_cards.py` の実装を踏襲・**実装済みレイアウト名だけを使う**）
複製元が実装するレイアウトは**この8種**:
`DATE_STAMP` / `CENTER_STACK` / `MONEY_STACK` / `SPLIT_COMPARE` / `ACT_TITLE_CARD` / `QUOTE_CARD` / `VOTE_SPLIT` / `SEAM_TRANSITION`。
**§7.2 デッキが使うのは 5種**（`CENTER_STACK` / `SPLIT_COMPARE` / `DATE_STAMP` / `VOTE_SPLIT` / `QUOTE_CARD`）。
> **★EP47 は `VOTE_SPLIT` を使う**（5-4 は台帳 A11 で verified＝捏造でない。EP45 が VOTE_SPLIT を禁じたのは Bearden の得票が台帳に無かったため。**Atwater は 5-4 が確定値なので VOTE_SPLIT 使用が正当**）。**`MONEY_STACK` / `SEAM_TRANSITION` / `ACT_TITLE_CARD` は本 EP 未使用**（金額は `CENTER_STACK`/`SPLIT_COMPARE`・幕頭は figures[]`acttitle` で表現）。
**上記5種以外のレイアウト名を発明しない（`validate_atwater_beats` §7.9 ルール3 で FAIL）。dochighlight をレイアウト名に使わない。**
**共通レイヤースタック・Anton/Oswald・`psName()` の runtime 解決（allFonts の array-LIKE ラッパーを unwrap）は複製元と同一。**

**★共通レイヤースタックに AI開示レイヤーを1枚追加（R1・全カード常時焼き）:** 最上位に近い固定レイヤーとして
`AI-assisted visualization`（Oswald 20px / SILVER `#C8CDD6` / opacity 70% / 右下 `[W-32, H-28]`）を全カードに焼く。AEカードは不透明の全画面 mp4 として本編に overlay されるため、これが無いと本編(Remotion)右下の開示が隠れる（R1 違反）。字幕帯とは縦56px 以上離す。

**★EP47 色定数（0..1 float・civil-violet レーン色。EP41 gold / EP42 blue / EP43 amber / EP44 teal / EP45 crimson / EP46 green を流用禁止・DESIGN と一致）:**
```python
ACCENT = [0.478, 0.361, 0.816]  # #7A5CD0 civil-violet（アクセント：数値・下線・レーン分離）
WHITE  = [0.961, 0.969, 0.980]  # #F5F7FA
SILVER = [0.784, 0.804, 0.839]  # #C8CDD6（開示テキスト）
INK    = [0.039, 0.039, 0.047]  # #0A0A0C 近黒ルート（サムネ bg と一致）
```
> **accent は必ず `#7A5CD0`（他話色を書かない）。** サムネ・OP props・AEカードの accent は全て `#7A5CD0`。

**数値カードは全て `money_keys()` 系で表示文字列を Python 事前計算**（JSX で算術しない＝EP38 確定ルール）。
**`s01`（$50）は数字を先に、間を置いて "NO JAIL" を出す。`c01`（FINE-ONLY / FULL ARREST）は左右2値を別レイヤー（改行禁止）。`v01`（5-4）は "5" と "4" を別レイヤーで、下段に "THE ARREST STANDS"。`q02`（Souter concession）は "POINTLESS INDIGNITY" → "FOR THE COURT — YET PERMITTED IT" を別レイヤー。**

## 7.4 `beats.json` スキーマ（本番 `08_edit/ae_hero/beats.json`）
`build_cleveland_hero_cards.py` の beats スキーマに準拠。トップに **`film_offset_sec`**（本編ナレ開始からのオフセット・§7.10 のコンポジタが読む）。各 beat に `id` / `layout` / `start` / `end` / `dur` /
`still`(象徴 or null) / `hero`/`main`(主表示文字列) / `top` / `bottom` / `left` / `right` / `kicker` / `date` / `place` / `caption`(**改行禁止・最大50字**) /
`value` / `numKeys` / `blend_mode`(既定 "overlay") / `required` / `out` / `attribution`(**QUOTE_CARD=q01 は必須**・§2 `APPROVED_QUOTES` 一致・R-QUOTE)。
**`value` / `main` / `hero` の数値は §2 台帳の `verified:true` 値のみ**（`check_atwater_facts` が照合）。**`1997`・子の年齢を出さない。**
**`v01` は R-DISPO を満たす "THE ARREST STANDS" ＋ "CONSTITUTIONAL"。`q02`（Souter）は "for the Court" 帰属＋"yet permitted"。`q01`（O'Connor）は "dissenting" 帰属。`beats.json` に `dochighlight` を出さない（R-DOCHL）。**

## 7.5 このマシン固有の罠（複製元が対処済み。**1つも省くな**）
1. `setTemporalEaseAtKey` の配列次元は **spatial(Position) で 1**（`if(!prop.isSpatial){...}` で分岐）
2. RS = **`"最良設定"`** / OM = **`"H.264 - レンダリング設定を一致 - 15 Mbps"`**（英語名は try/catch フォールバックのみ）
3. TextDocument の改行は `\n` 不可。**`caption` は1行**（改行が要るなら別レイヤー・SPLIT_COMPARE の左右2値・VOTE_SPLIT の 5/4 は別レイヤー）。**テキスト幅は `sourceRectAtTime(t,false).width` で実測**（advance-width 推定は禁止＝EP40 の文字切れ原因）。em-dash は `-`
4. `app.newProject()` は headless でハング。**使わず**同名 `ATWATER_` コンプを防御削除
5. ビルドは**カード8枚で ~100–120秒**。`render/_build_ok.txt` をポーリング（**タイムアウト最低300秒**）
6. 起動はデタッチ + 出力ポーリング。jsx 末尾で `app.quit()`
7. `comp.motionBlur=true` だけでは無効。**動かすレイヤー個別に `layer.motionBlur=true`**
8. 2Dレイヤー回転は **`"ADBE Rotate Z"`**（`"ADBE Rotation"` は null）
9. `inPoint` と `outPoint` の**両方**を設定
10. 読み込み後 `item.mainSource.conformFrameRate = 30`（忘れると全カードの timing がズレる）
11. 実行パス `C:\Program Files\Adobe\Adobe After Effects 2026\Support Files\AfterFX.exe`（実在確認済み）
12. `proj.gpuAccelType = GpuAccelType.SOFTWARE`（RTX4090 でもソフトレンダ固定・安定優先）
13. **`getFontsByFamilyNameAndStyleName` を使うフォント厳格解決**（miss は **throw**・フォールバック禁止／allFonts[i] ラッパー経由 unwrap）
14. **フォント文字列やラベルを PowerShell 経由の正規表現/エスケープで生成しない**（`\b` がバックスペース化した実害）。Python 側で literal に組む。**Python 先頭に `sys.stdout.reconfigure(encoding="utf-8")`**
15. **aerender 前に `.aep` の mtime > `.jsx` の mtime を assert**（古い .aep を焼く事故防止＝EP39-41 実害）

## 7.6 実行
```bash
$PY scripts/ae/build_atwater_hero_cards.py
"C:/Program Files/Adobe/Adobe After Effects 2026/Support Files/AfterFX.exe" -noui \
  -r ".../episodes/PD-2026-047-atwater/08_edit/ae_hero/atwater_hero.jsx"
# render/_build_ok.txt を待つ（最大300秒）→ render/*.mp4 が8本揃うまで待つ（最大1200秒）
$PY scripts/ae/composite_atwater_hero.py
```

## 7.9 `scripts/validate_atwater_beats.py`（BLOCKING）
1. `beats[].start` 昇順・区間非重複
2. 全 `start`/`end` が本編ナレ区間内（HOOK 0–58.6 と ENDCARD 末尾9s に重ねない）
3. `layout` が §7.3 の**実装済み5種**（`CENTER_STACK`/`SPLIT_COMPARE`/`DATE_STAMP`/`VOTE_SPLIT`/`QUOTE_CARD`）のいずれか。**この5種以外（`MONEY_STACK`/`SEAM_TRANSITION`/`ACT_TITLE_CARD`/`dochighlight` 等）は FAIL。** still が必要なレイアウトで null なら FAIL
4. `still` 非null は実在＋長辺 >=3840px
5. `hero`/`main`/`top`/`bottom`/`left`/`right`/`caption`/`value` が §2（R-FORBID/R-NUM/R-QUOTE/R-DISPO/R-FACE/R-DOCHL/R-DATE/R-HEDGE）を通る
6. `verified:false` の値を要求するカードは `required:false` で**除外**、`required:true` なら exit 1
7. **`atwater_film.json` の `figures[]`（§6）と AE の区間が1秒でも重ならない**
8. `caption` に改行が含まれない
9. **AI開示レイヤーの存在（R1）** — ビルダが全カード共通スタックに `AI-assisted visualization`（右下・§7.3）を焼く設定であることを静的に確認。無ければ FAIL。受入アイボール（§13.1）でも「AEカード表示中も右下の開示が見える」を確認
10. **`dochighlight`/`DOCHIGHLIGHT` が beats/レイアウト名に1件も無い（R-DOCHL）**
11. **`v01` に "THE ARREST STANDS"＋"CONSTITUTIONAL"（R-DISPO）／`q01` の attribution が "Justice O'Connor, dissenting"／`q02` が "for the Court" 帰属（R-QUOTE）が有ること**

## 7.10 基底 mp4 とコンポジタ（`build_atwater_bgm_real.py` → `composite_atwater_hero.py`）
```
# 完成後の合成順（ブリーフ§5）: build_atwater_bgm_real.py（narration+BGM・OFF=11.5）→ composite_atwater_hero.py（AEカード焼込み・film_offset_sec 適用）
BASE = episodes/PD-2026-047-atwater/08_edit/atwater_final_bgm.v002.mp4     # build_atwater_bgm_real.py が生成
OUT  = episodes/PD-2026-047-atwater/08_edit/atwater_final_bgm.v003_ae.mp4  # composite_atwater_hero.py が生成
FFMPEG  = C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe
FFPROBE = C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffprobe.exe
W,H,FPS = 1920, 1080, 30
```
**`build_atwater_bgm_real.py` は EP43 `build_caniglia_bgm_real.py` の複製・定数 `OFF=11.5`（narration に対する BGM オフセット）に差し替える。**
**`composite_atwater_hero.py` は EP43 `composite_caniglia_hero.py` の複製・`beats.json` の `film_offset_sec` を読み各 beat 区間を本編尺にマップする。**
**SKIP4条件を1行も削らない:** ① `render/<id>.mp4` 不在 ② 解像度 != 1920x1080 ③ 実測尺 `< dur-0.3` ④ `film_offset_sec + beat.end > base_dur`。
SKIP された区間は元カットのまま残る（作品は壊れない）。**何枚 SKIP したかを stderr に必ず出す。**
ffmpeg は `overlay=0:0:eof_action=pass:enable='between(t,start,end)'`（`blend_mode` が screen/multiply の時のみ `blend`）。
**出力後 `probe_dur(OUT)` でベースとの尺差 <=0.5秒を確認。出荷済みは絶対に上書きしない（必ず `_v003_ae`）。**

---

# 8. 字幕の切断規則（`scripts/gen_captions_atwater.py`＝`gen_captions_cleveland.py` の複製）

## 8.1 原則
**文字数は「上限」であって「分割基準」ではない。** `gen_captions_cleveland.py` の `internal_split()` / `chunk_sentence()` を**そのままコピー**。
`from fix_caption_dangling import NO_DANGLE_END, wrap as safe_wrap`（**語リストを自前で書き直さない**）。

## 8.2 通すゲート `scripts/check_caption_breaks.py`（**閾値を緩めるの禁止**）
- **A. 行末の機能語** = 0件 / **B. 孤立キュー**（語数<3 で終端句読点・大文字始まりの両方を満たさない）= 0件 / **C. 句をまたぐ切断(hard)** = 0件。A/B/C いずれか1件で FAIL（実質ゼロ許容）

## 8.3 EP47 の入力と対応
- 入力は **narration_index の各チャンク文**（`--narr`）。**字幕テキストは台本本文と1:1対応**（§0.5-5）。台詞・別エピソード文の混入禁止。verbatim で使い構文境界で分割するだけ。
- `ABBR` に `U.S.` / `v.` / `Mr.` / `Ms.` / `No.` / `U.S.C.` を持つ（`Atwater v. City of Lago Vista` の `v.`、`532 U.S. 318` の `U.S.`、`42 U.S.C. § 1983` の `U.S.C.` で文を切らない）。
- タイミングは narration_index の start/end。CPS <=27・最小表示 0.90秒。**Step で決めた境界を時間都合で動かさない。**
- **字幕にも R-FORBID 適用**（台本本文に主語付き断定の禁止語は無いので verbatim なら自然に通る。§2.1 注意：`illegal`/`unconstitutional` 単独を禁止語に足さない＝ENDING の「is not that it was illegal」を巻き込む）。

## 8.4 セルフテスト（`--selftest`・EP38 実害を回帰に）
`Atwater v. City of Lago Vista` / `532 U.S. 318` / `42 U.S.C. § 1983` で文が切れないこと、機能語で終わるキュー・孤立キューを作らないことを含む4ケースを実装し、**出力を `check_caption_breaks.py` に食わせて exit 0 まで自動確認。**

## 8.5 実行
```bash
$PY scripts/gen_captions_atwater.py --narr episodes/PD-2026-047-atwater/06_audio/narration_index.v001.json
$PY scripts/check_caption_breaks.py episodes/PD-2026-047-atwater/08_edit/captions.final.v001.srt
# → PASS が出るまで直す。ゲート側の閾値を緩めるのは禁止。
```

---

# 9. 5ゲートの実際の判定（**build 後に必ず全部通す・animation_mix を忘れるな**）

| ゲート | 実体 | 入力 | EP47 の通過根拠 |
|---|---|---|---|
| `check_asset_reuse.py <film.json>` | factory≤1 / motion≤2 / still≤2 / first-use≥0.70 | **film.json 位置引数** | §5.2: factory1.00 / motion2.00 / still1.19 / first-use **0.8578** |
| `check_motion_density.py --ep PD-2026-047-atwater` | film.json の graphics+figures+heroCuts のみ / density≥2.5・coverage≥0.25・variety≥3（**AND**） | **`--ep`** | §6.1: **3.00 / 30.0% / 16種**（AEカードは0本＝§0.5-2・beats≥30） |
| `check_animation_mix.py --ep PD-2026-047-atwater` | film.json の cuts を img=still/その他=footage 分類 / still-share≤0.45・motion-cov≥0.45 | **`--ep`** | §5.2[C]: still-share **0.4489(cut)/0.4213(frame)** / motion-cov **0.5511+** |
| `check_caption_breaks.py <srt>` | A/B/C 各0件 | **srt 位置引数** | §8 の構文境界生成器 |
| `check_script_length.py <script> --json` | 総語数 / wpm / narration_seconds | **script 位置引数** | 2,135語 / wpm178.1 / **719.3s** |

> **★ゲートの入力指定（ブリーフ§5）:** density/mix は **`--ep PD-2026-047-atwater`**。**`--json <film.json>` は出力パス（上書き事故）なので入力に使わない。** asset_reuse は film.json 位置引数、caption_breaks は srt 位置引数、script_length は script 位置引数。
> **`check_animation_mix` は `04_scenes/premium_beatsheet.v*.json` があればそれを優先する。** §5.6 の通り B の beatsheet は `atwater_beatsheet`（`premium_` 無し）なので**auto-detect されず film.json を測る。**
> **★still-share 0.4489 は cap 0.45 に余裕 0.11%（極薄）。build 出力を必ず `check_animation_mix` で確認し、超えたら still を1本 footage に置換して再build（still を増やさない）。**

---

# 10. OP バンパー `OpeningAtwater`（Remotion・fps60/1920x1080/180f）

## 10.1 二重OPを作らない
本編（`Ep47Atwater`）の OP は `Bookends.tsx` の `BrandOpening` のまま（`op_ed_bookends` ゲート・フォーク禁止）。
`OpeningAtwater` は**独立したタイトルバンパー成果物**（`out/atwater_opening.mp4`。Shorts/予告/SNS 用）。**本編に ffmpeg で焼き込まない。**

## 10.2 Composition 設定
| 項目 | 値 |
|---|---|
| `id` | `OpeningAtwater` |
| 解像度 / fps / duration | **1920×1080 / 60 / 180**（=3.0秒） |
| component | `remotion/src/compositions/OpeningAtwater.tsx` |

```tsx
import {OpeningAtwater, openingAtwaterDurationInFrames} from './compositions/OpeningAtwater';
import atwaterOpeningProps from '../props/atwater.json';
<Composition id="OpeningAtwater" component={OpeningAtwater}
  width={1920} height={1080} fps={60}
  durationInFrames={openingAtwaterDurationInFrames(60)} defaultProps={atwaterOpeningProps}/>
```

**依存:** `@remotion/motion-blur`（未導入時のみ `cd remotion && npm i @remotion/motion-blur`）。
**`remotion/remotion.config.ts`** は既に正典値（png / h264 libx264 / CRF16 / yuv420p / bt709 / aac 320k / 全コア並列 / angle）。**一致確認のみ・書き換えない。**

## 10.3 秒数ベースのタイムライン（fps=60・フレーム直書き禁止・全て `Math.round(fps*秒)`）

| 秒 | 起きること | 手法 |
|---|---|---|
| 0.00–0.40 | L1 グラデ背景 opacity 0→1・**同時に scale 1.08→1.00（`Easing.out(Easing.cubic)`）** | interpolate（opacity 単独禁止・scale と併用） |
| 0.10 | ロゴ（`hasLogo`）左上に spring・scale 0.4→1.0・opacity 0→1 | spring `damping:14,mass:0.9` |
| 0.15–0.25 | L2 グリッド reveal（opacity→0.18）＋ translateY 0→48px | spring `damping:200,mass:1` + `Easing.inOut(Easing.sin)` |
| 0.25 | L3 グロー（violet `#7A5CD0`）scale 0.6→1.15 / opacity 0→0.85 | spring `damping:18,mass:1.2`（併用） |
| 0.30–0.86 | L4 主役タイトルが1文字ずつ切れ上がり（overflow:hidden + translateY 110%→0）＋ opacity。スタッガー **2f/文字**。全体を `Trail(layers=6,lagInFrames=1.2,trailOpacity=0.45)` で包む | spring `damping:16,mass:1` |
| 0.55–1.15 | L2b **道のセンターライン（violet）**が中央から横に `scaleX 0→1`＋opacity 0→0.5（「二車線の道」モチーフ） | spring `damping:22,mass:1.1`・`transformOrigin:'center'`・**motionBlur** |
| 0.95–1.35 | L5a アクセント下線（violet）左から `scaleX 0→1` | spring `damping:16,mass:0.8`・`transformOrigin:'left center'` |
| 1.10–1.55 | L5b サブタイトル translateY 24→0 + opacity 0→1 | spring `damping:20,mass:1`（併用） |
| 1.55–3.00 | settle→ホールド。**完全静止フレーム無し・フェードアウトしない** | — |

> **等速線形を1箇所も使わない。opacity 単独の演出を1箇所も作らない**（全 opacity が translateY/scale/scaleX と対）。

## 10.4 props 型と値
```ts
export type OpeningAtwaterProps = { title:string; subtitle:string; accent:string; hasLogo:boolean };
```
`remotion/props/atwater.json`: `{ "title":"THE FIFTY DOLLAR ARREST", "subtitle":"THE COURT SAID POLICE COULD", "accent":"#7A5CD0", "hasLogo":true }`
`remotion/props/atwater_short.json`: `{ "title":"THE FIFTY DOLLAR ARREST", "subtitle":"CAN POLICE JAIL YOU OVER A TICKET?", "accent":"#7A5CD0", "hasLogo":false }`
> `subtitle`/`title` も §2 の R-FORBID/R-DISPO/R-FACE 検査対象。ルート背景は INK 近黒 `#0A0A0C`。
> **accent は EP41 gold / EP42 blue / EP43 amber / EP44 teal / EP45 crimson / EP46 green を書かず violet `#7A5CD0`（レーン分離・他話色流用は BLOCKER）。**
> **「the arrest was illegal」を subtitle に書かない。** `THE COURT SAID POLICE COULD`（合憲＝許された・C-1）・疑問形 `CAN POLICE JAIL YOU OVER A TICKET?` は問題提起として可。

## 10.5 量産
```bash
cd remotion && npm run studio     # OpeningAtwater を 0→180f スクラブして §10.3 の各時刻を目視
npx remotion render OpeningAtwater out/atwater_opening.mp4 --props=./props/atwater.json
npx remotion render OpeningAtwater out/atwater_short_op.mp4 --props=./props/atwater_short.json
```

---

# 11. サムネ3案（`AtwaterThumbnails.tsx`・`<Still>` 1280×720・Root に `Thumb-atwater-01..03`）

**共通要件:** 見出し全て大文字・4語以内・320pxで判読 / **実在人物の肖像禁止（R1・Gail Atwater の顔/身体を出さない・C-5）** / INK 黒 `#0A0A0C` bg + violet `#7A5CD0` /
背景は body 静止画のうち `also_thumb==true` の6枚（象徴オブジェのみ・C-5。**サムネ専用の分類は無い＝also_thumb フラグを読む**） / `thumbnail_visibility`（luma平均≥33＋コントラスト）を通す。目標CTR 6%+。3案は6枚から選ぶ。
**「the arrest was illegal」「struck down」を出さない（R-FORBID/R-DISPO）。1997・子の年齢を出さない（R-HEDGE）。**

**★also_thumb 6枚（still 資産 ID 空間 S01..S85＝CODEX_A §4.3。A のマニフェストと**一字一致必須**の A↔B 契約点）:**
`S01` / `S06` / `S22` / `S40` / `S60` / `S85`。
> サムネ component は**マニフェストの `also_thumb` フラグを読んで**背景を選ぶ（scene id をハードコードしない）。**この6 ID は CODEX_A §4.3 と完全一致必須**（`check_atwater_asset_manifest` §3.3-12 が集合の一致を検査）。**CODEX_A が別集合なら B は自分の6 ID を書き換えず A に合わせる（A が producer）。**

- **T1「外れたシートベルト」（最推奨）:** 外れたシートベルトのバックルの接写（象徴・顔なし・**S01/S06** 系）。文字 **`ARRESTED OVER A SEATBELT`**（4語）。`SEATBELT` を violet。**合憲＝射程を過大化しない。**
- **T2「$50 の逮捕」（数字勝負）:** $50 の罰金票を暗く落とし（**S22** 系）、前面に **`$50`**（大）＋ **`AND HANDCUFFS`**（下）。数字は A03 の検証済み値のみ。
- **T3「5-4 の線」（尊厳）:** 大理石の列柱／9席を背にした象徴（**S40/S85** 系）。文字 **`THE COURT SAID POLICE COULD`**（合憲・C-1）。`COULD` を violet。**「違法」に見せない。**

**A/Bタイトル候補（`09_package`・60字以内・二人称・台本のとおり・★"違法"と書かない）:**
- **A:** `Arrested Over a Seatbelt. The Supreme Court Said Police Could.`
- **B:** `Police Can Arrest You for a Ticket-Only Offense. Legally.`
> ※「the arrest was illegal」「the Court struck it down」系のタイトルは**禁止**（C-1・R-DISPO）。

**固定コメント** `09_package/pinned_comment.v001.txt`（§2 の R-NUM/R-QUOTE/R-FORBID/R-DISPO 検査対象・台帳事実のみ）:
```
What this case actually decided — and what it did not.

WHAT IT DECIDED: In Atwater v. City of Lago Vista (532 U.S. 318, 2001), the
Supreme Court held 5-4 that if an officer has probable cause to believe you have
committed even a fine-only offense in his presence, he may make a full custodial
arrest without violating the Fourth Amendment. The arrest of Gail Atwater was
upheld as constitutional. It was not illegal. It was allowed.

WHAT IT DID NOT DO: The majority, written by Justice Souter, called her arrest a
pointless indignity and still permitted it, saying the fix belongs to legislatures,
not the Fourth Amendment. Justice O'Connor, in dissent, argued probable cause
alone should not justify jailing someone over a fine. Four votes, not five.

Some states have passed laws telling officers to write a citation for minor
offenses instead of arresting. Where those laws exist, you are protected by them,
not by the Constitution. Look up your own state's rule before you need it.
```
> **description.txt にも AI 開示行（`AI-assisted visualization`）を置く（R1）。** 数値は台帳（$50 / 532 U.S. 318 / 2001 / 5-4）のみ・**1997/子の年齢を出さない**。

---

# 12. 本編コンポジション登録（`remotion/src/Root.tsx`・`Ep45Cleveland`/`Ep43Caniglia` の形を踏襲）
```tsx
import atwaterFilm from './data/atwater_film.json';
<Composition id="Ep47Atwater" component={CaseFilm}
  durationInFrames={caseFilmDurationInFrames(atwaterFilm as unknown as FilmData, BRAND.video.fps)}
  fps={BRAND.video.fps} width={BRAND.video.width} height={BRAND.video.height}
  defaultProps={{ data: atwaterFilm as unknown as FilmData, seriesLabel: 'PRIME DOCUMENTARY',
    title: 'Arrested Over a Seatbelt. The Supreme Court Said Police Could.',
    subtitle: 'A fine-only offense, a full custodial arrest, upheld 5-4 as constitutional. The remedy the Court left you is a legislature, not the Fourth Amendment.' }}/>
```
> **id は正確に `Ep47Atwater`（切り詰め・綴り違い・大文字化の誤記に注意）。** `caseFilmDurationInFrames` の 4項評価は **22194 frames**（§5.1.1・hookSeconds=8.0）。
> `atwaterFilm` は `import atwaterFilm from './data/atwater_film.json';`（EP45 の `clevelandFilm` に相当）。
> `remotion/src` に現在 `atwater` の文字列が無いこと（衝突しない）を確認してから追記。
> `title`/`subtitle` も §2 検査対象（R-FORBID/R-DISPO/R-QUOTE）。**「the arrest was illegal」「the Court struck it down」を書かない。**

---

# 13. 受入（自分で exit 0 を確認してから完了報告）
```bash
cd C:\Users\aab15\Documents\prime-documentary ; PY=./.venv/Scripts/python.exe

# 0. 語数（最優先・課金前に落とす）
$PY scripts/check_script_length.py episodes/PD-2026-047-atwater/03_script/script.en.v001.md --json   # 2,135語 / wpm178.1 / 719.3s

# 1. 事実性/6制約（EP47固有・正確性ゲートはこの1本・dochighlight 不使用も検査）
$PY scripts/check_atwater_facts.py --json

# 2. 契約バリデータ
$PY scripts/validate_atwater_beats.py
$PY scripts/check_atwater_asset_manifest.py --assets episodes/PD-2026-047-atwater/05_visuals/asset_manifest.v001.json

# 3. ★5ゲート（animation_mix を忘れるな・入力は --ep / 位置引数を厳守）
$PY scripts/check_asset_reuse.py    remotion/src/data/atwater_film.json
$PY scripts/check_motion_density.py --ep PD-2026-047-atwater
$PY scripts/check_animation_mix.py  --ep PD-2026-047-atwater
$PY scripts/check_caption_breaks.py episodes/PD-2026-047-atwater/08_edit/captions.final.v001.srt

# 4. 水増し・レンダ前プリフライト
$PY scripts/check_padding.py --ep PD-2026-047-atwater --json
$PY scripts/preflight_render_gate.py --ep PD-2026-047-atwater

# 5. ★public_slim staging（EP45 空 public_slim 事故防止）→ 本編レンダ（slim public・並列4）→ BGM → AEカード合成
#    public/atwater → public_slim/atwater へ全メディア（img/factory/motion/audio/overlay + 各 <stem>_depth.png）をコピー
$PY scripts/stage_cleveland_assets.py --ep PD-2026-047-atwater 2>/dev/null || {
    mkdir -p remotion/public_slim/atwater
    cp -r remotion/public/atwater/{img,factory,motion,overlay,audio} remotion/public_slim/atwater/ 2>/dev/null
    cp remotion/public/atwater/narration.mp3 remotion/public_slim/atwater/ 2>/dev/null
}
#   ★atwater_film.json が参照する src と各 <stem>_depth.png が public_slim に全て在ることを確認してからレンダ
cd remotion
npx remotion render Ep47Atwater out/atwater.mp4 --public-dir=public_slim --concurrency=4
cd ..
$PY scripts/build_atwater_bgm_real.py     # OFF=11.5
$PY scripts/ae/composite_atwater_hero.py

# 6. 本編最終受入（episode番号は★位置引数・--ep ではない）
$PY scripts/check_final_acceptance.py 47 \
  --render episodes/PD-2026-047-atwater/08_edit/atwater_final_bgm.v003_ae.mp4 --emit-receipt
```

| ゲート | EP47 目標値 |
|---|---|
| `check_script_length` | 総語数 **2,135** / `wpm 178.1` / narration **719.3s** |
| `check_asset_reuse` | factory≤1 / motion≤2 / still≤2 / first-use **0.8578**（floor0.70） |
| `check_motion_density` | density **3.00**/min / coverage **30.0%** / variety 16（floors 2.5 / 0.25 / 3・beats **≥30**） |
| `check_animation_mix` | still-share **0.4489(cut)/0.4213(frame)**（cap0.45・余裕極薄）/ motion-cov **0.5511+**（floor0.45） |
| `check_caption_breaks` | 行末機能語0 / 孤立キュー0 / hard split 0 |
| `check_atwater_facts` | violations = 0（台帳照合・UPHELD 枠・Souter多数/O'Connor反対分離・5-4・R-FORBID・R-DOCHL・R-QUOTE・R-HEDGE） |
| runtime band | 12.0–12.5分（narration 719.3s + hook8.0 + bookends・total **739.8s ≤ 750s**） |
| factory クリップ | ≥24本 → **92本** |
| image_resolution | 全静止画 長辺 ≥3840px |
| thumbnail | 3案 @1280×720 + selected luma≥33 |
| op_ed_bookends | `BrandOpening`/`BrandEndcard` を import（フォーク禁止） |

**全て exit 0 でなければ `package_ready` にしない。自己申告QCは無効。QC基準を書き換えて通すのは禁止。**

## 13.1 完成後の全編アイボール（**1フレーム判定禁止＝EP39-41 実害**）
`atwater_final_bgm.v003_ae.mp4` を **0→末尾まで通しで実視聴**し、以下を確認してから完了報告:
- 紙芝居感が無い（still が連続していない・footage が体感で過半＝EP45 の直接死因を潰せているか）
- AEカード8枚が全て焼き込まれ数値が台帳と一致（「the arrest was illegal」「struck down」がどこにも無い）
- **`v01`「5 / 4 / THE ARREST STANDS / CONSTITUTIONAL」が読める（C-1 違法と読ませない）**
- **`q02`（Souter）が "POINTLESS INDIGNITY / JUSTICE SOUTER, FOR THE COURT — YET PERMITTED IT"（多数意見の concession＋許容・C-2）**
- **`q01`（O'Connor 逐語）が "JUSTICE O'CONNOR, DISSENTING" 帰属（Court に帰属していない・C-3・要約を引用符にしていない）**
- **`s01`「$50 / MAXIMUM FINE / NO JAIL」・`c01`「FINE-ONLY OFFENSE → FULL ARREST」が読める。1997・子の年齢がどこにも出ていない（R-HEDGE）**
- Gail Atwater の顔・身体・肖像が無い（象徴＝道/ピックアップ車内/空のチャイルドシート/外れたシートベルト/手錠/booking 台/$50票/天秤/列柱9席/開いた扉と閉じた扉のみ・C-5）／**子どもを扇情化していない**（"two young children" 以上に踏み込まない）
- **`dochighlight`（黒バー/box/underline）が1本も無い（figures/AE／R-DOCHL）**
- 生成ビジュアル表示中は `AI-assisted visualization` が右下に常時（**AEカード8枚の表示中も**開示が見える＝カード共通スタックに焼かれている・R1・§7.3/§7.9）
- accent が violet `#7A5CD0`（EP41 gold / EP42 blue / EP43 amber / EP44 teal / EP45 crimson / EP46 green が紛れていない）
- 音ズレ・字幕ズレ・尺差（base と <=0.5s）が無い

---

# 14. 絶対にやらないこと
- **EP39 / EP40 / EP41 / EP42 / EP43 / EP44 / EP45 / EP46 のファイル・素材に触らない**（読み取りのみ可）。レーンを分離する。
- **スレッドAの所有ファイル（§0.2.1）に書かない**（`05_visuals/` `05_stock/` `remotion/public/atwater/` `H:\...\ai\atwater\`）。**B の provenance は `04_scenes/atwater_build_manifest.v001.json` に書く。**
- **設計書 / `EP47_atwater_CODEX_A_*` / PD-2026-039〜046 に触らない。**
- **課金ジョブを起動しない**（ElevenLabs TTS / 課金画像生成API / YouTube アップロード）。narration_index は実測版を消費するだけ。
- **公開済み・出荷済み mp4 を上書き・再レンダしない**（出力は必ず `_v003_ae`）。
- **台帳（§2）に無い数値を焼かない**（$580,000 の再発防止）。**★`1997`・子の年齢は confidence:medium＝画面禁止（R-HEDGE）。$50/2001/532 U.S. 318/5-4 のみ断定。**
- **`FigureSpec` の `kind` を推測で書かない**（§6.2 の実在小文字値のみ。大文字名は無言で消える。`comparebars` は非在→`compbars`・`VoteTally` は非在→`votetally`）。**★`dochighlight` を1本も使わない（R-DOCHL）。**
- **`--variants` という語を書かない**（1シーン1枚・バリエーション0＝ブリーフ§1。SDXL は A の領分で 1 固定）。
- **asset_manifest の `counts`/`role` enum/`overlay` 枚数を CODEX_A と食い違わせない**（`role` は `body`/`i2v_source`/`reject` の3値のみ・**`thumb`/`still_thumb` を作らない**・overlay=12・also_thumb 6 ID を A と一致）。
- **★「the arrest was illegal」化しない・「struck down」と言わない**（C-1・R-DISPO＝逮捕は合憲 UPHELD 5-4）。**Souter 逐語を反対意見/Court 以外に、O'Connor 逐語を Court/多数意見に帰属させない**（C-2/C-3・R-QUOTE）。**票決は 5-4**（C-4）。**Gail Atwater の顔/肖像/身体を出さない・子どもを扇情化しない**（C-5・R-FACE）。
- **accent に他話色（gold/blue/amber/teal/crimson/green）を使わない**（violet `#7A5CD0` のみ）。
- **stub/dryrun/placeholder のコードパスを作らない**（このスレッドは実素材のみ・ブリーフ§7・grep 0）。**★`build_atwater_film.py` は manifest の `factory[]`(92)/`motion[]`(16) を `public_path` で全読込し、空なら exit 1（EP45 空配列＝紙芝居事故の直接防止）。**
- **★render 前に `public_slim/atwater` へ全メディアを staging する**（EP45 は空 public_slim でレンダ素材欠落・§13-5）。
- **スペック数値（225 cuts / still85 / factory92 / motion16 / distinct193 / first-use0.8578 / still-share0.4489 / figures≥30→36 / 719.3s / 2,135語 / 48シーン / mean_shot3.2 / total739.8s≤750s / durationInFrames22194 / hookSeconds8.0）を変えない。**
- **composition id は `Ep47Atwater`（切り詰め・綴り違い注意）。** **PowerShell 経由で正規表現/エスケープを生成しない**（`\b` バックスペース化の実害）。
