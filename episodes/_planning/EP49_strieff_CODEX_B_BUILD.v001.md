# EP49 strieff — Codex スレッドB「実装」引き継ぎプロンプト v001

> **このファイルは単体で完結している。他のファイルを読まなくても着手できる。**
> 並行して走っていたスレッドA（素材生成）のファイル `EP49_strieff_CODEX_A_*.md` は**読まない**（Aは既に FROZEN・接続点は §3 のマニフェスト1ファイル）。
> 設計書 `EP49_strieff_DESIGN*.md` も**読まない**（必要な数値・AEデッキ・figures 配分はすべて本書に転記済み）。
> `EP49_strieff_PRODUCTION_SPEC.v001.json` の数値は本書に転記済み。**あなたはこれを書き換えない。**

```
あなたは Prime Documentary（YouTubeドキュメンタリーチャンネル）の制作エンジニアです。
リポジトリ: C:\Users\aab15\Documents\prime-documentary
Python:     C:\Users\aab15\Documents\prime-documentary\.venv\Scripts\python.exe
メディア:   H:\pd-media
担当:       EP49 / Episode ID: PD-2026-049-strieff / slug: strieff
Composition id（本編）: Ep49Strieff
```

**題材:** *Utah v. Strieff*, **579 U.S. 232 (2016)**（docket 14-1373・decided **2016-06-20**）と **Edward Joseph Strieff, Jr.**（South Salt Lake City, Utah の**存命の私人 = R2・本件後に薬物所持で有罪**）。
匿名通報→約1週間の断続監視の後、**理由なく（reasonable suspicion 無しで）路上停止**され、ID照会で**先在する小さな交通違反の逮捕状**が判明、その令状で逮捕・付随捜索でメタンフェタミンが発見された。最高裁は **5-3**（Scalia死去で**空席＝8名**）で、その証拠は**排除法則の下でも許容される**と判断した。
本作の主題は「**停止は違法だった。誰もそれは争っていない。それでも証拠は残った**」という不快さ（*illegal, yet the evidence counts*）。多数意見（Thomas）は、**先在する有効な令状が違法な停止と証拠の因果を "attenuate"（希釈・遮断）した**という一点だけで証拠を救った。排除法則は**廃止でなく"狭められた"**。Sotomayor / Kagan の反対が対抗軸。

> **★正確性6制約が全出力を律する（§2）。** 「the stop was legal」「exclusionary rule abolished」を**書かない**（停止は違法・排除法則は狭められただけ）・attenuation（3要素）でしか証拠は入らない・票決は **5-3・Scalia空席で8名**・Sotomayor / Kagan 逐語は**反対意見（dissent）**に中立帰属（Court に帰属させない）・**"we are all harmed" は逐語でない＝1件も引用しない**（「everyone is harmed」の趣旨は逐語 "anyone's dignity can be violated in this manner" か narration で）・**Edward Strieff の顔/肖像/身体を一切出さない（象徴のみ）・薬物は臨床的最小限**・数値は台帳一致。**★`figures[].kind` に `dochighlight` を1件も入れない**（黒バー/box/underline がバグに見える＝3回指摘）。

---

# 0. このスレッドの責務・境界・完了条件

## 0.1 このスレッド（B）の責務 — **コード律速。実装は全部書ける。**

| # | 作業 | 成果物 |
|---|---|---|
| B-1 | エピソードディレクトリと `manifest.json` | `episodes/PD-2026-049-strieff/**` |
| B-2 | 境界契約マニフェストの**消費側**バリデータ | `scripts/check_strieff_asset_manifest.py`（**`check_cleveland_asset_manifest.py` を複製**） |
| B-3 | 事実台帳 S-ID と 6制約ゲート（**EP49固有・BLOCKING**） | `scripts/check_strieff_facts.py`（**`check_cleveland_facts.py` を複製**） |
| B-4 | `strieff_film.json` ビルダ（**manifest→cuts＋beatsheet／footage混在・実素材のみ**） | `scripts/build_strieff_film.py`（**`build_cleveland_film.py`（または EP46 `build_tlo_film.py`）を複製**） |
| B-5 | beats バリデータ（AEとRemotionの区間衝突検査＋ledger／6制約） | `scripts/validate_strieff_beats.py`（**`validate_cleveland_beats.py` を複製**） |
| B-6 | **構文境界で切る字幕生成器**（実測 narration_index から verbatim・**+11.5 offset**） | `scripts/gen_captions_strieff.py`（**`gen_captions_cleveland.py` を複製**） |
| B-7 | **After Effects カード**のビルダとコンポジタ | `scripts/ae/build_strieff_hero_cards.py`（**`build_cleveland_hero_cards.py`＝FIXED版 複製**）/ `scripts/ae/composite_strieff_hero.py`（**`composite_caniglia_hero.py`=EP43 複製**） |
| B-8 | 本編 BGM ミックス（AEカード合成の基底 mp4 を生成） | `scripts/build_strieff_bgm_real.py`（**`build_caniglia_bgm_real.py`=EP43 複製・OFF=11.5**） |
| B-9 | 本編 Remotion コンポジション登録 `Ep49Strieff` | `remotion/src/Root.tsx` |
| B-10 | OP バンパー `OpeningStrieff`（fps60/1920x1080/180f） | `remotion/src/compositions/OpeningStrieff.tsx` |
| B-11 | サムネ3案 | `remotion/src/compositions/StrieffThumbnails.tsx` |
| B-12 | 本編レンダ→BGM→AEカード合成→全ゲート→**全編アイボール3回** | `episodes/PD-2026-049-strieff/08_edit/**` |

> **★このスレッドは「実素材のみ」（ブリーフ§7）。stub/dryrun/placeholder のコードパスを作らない（`grep -riE 'stub|placeholder|dryrun' scripts/*strieff*.py` が 0）。** A は FROZEN（§3 の本番マニフェストが実在）・narration_index は実測版が実在する前提で組む。**素材が来ていなければ止めて A/上流に差し戻す**（架空の黒スタブで緑にしない）。

## 0.2 もう一方のスレッド（A・FROZEN）との境界 — **接続点はただ1ファイル。**

```
episodes/PD-2026-049-strieff/05_visuals/asset_manifest.v001.json
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
| `episodes/PD-2026-049-strieff/manifest.json` | **B** | 読み書き |
| `episodes/PD-2026-049-strieff/{00_topic,01_research,03_script,04_scenes,06_audio,08_edit,09_package,approvals,events}/**` | **B** | 読み書き |
| `remotion/src/**` `remotion/props/**` | **B** | 読み書き |
| `scripts/*strieff*.py` / `scripts/ae/*strieff*.py`（§0.3） | **B** | 新規作成 |
| **`episodes/PD-2026-049-strieff/05_visuals/**` `05_stock/**`** | **A** | **読み取りのみ。書くな** |
| **`H:\pd-media\assets\ai\strieff\**` / `ai_video\strieff\**`** | **A** | **読み取りのみ。書くな** |
| **`remotion/public/strieff/{img,factory,motion,overlay}/**`** | **A** | **読み取りのみ。書くな** |
| `EP49_strieff_DESIGN*.md` / `EP49_strieff_CODEX_A_*.md` | **設計/Aスレッド** | **触るな** |
| `EP49_strieff_PRODUCTION_SPEC.v001.json` / `EP49_strieff_script.en.v001.md` / `EP49_strieff_facts.v001.json` | **上流** | **読み取りのみ。書くな** |
| `episodes/PD-2026-039-*/**` … `PD-2026-048-*/**` / それらの素材 | **他エージェント** | **絶対に触るな（読み取りのみ可）** |

> **B は `remotion/public/strieff/` に書かない**（A の staging 済み本番素材）。B の provenance/beatsheet は `04_scenes/` に書く（§5.6）。**render 用の `public_slim` staging（§13）は B が作る。**

## 0.3 B が新規作成するスクリプト（これ以外を新規に作らない。既存を改変しない）

| パス | 役割 | 手本（**改変せず読んで複製→パス/定数だけ差し替え**・実在確認済み） |
|---|---|---|
| `scripts/check_strieff_asset_manifest.py` | §3.3 消費側バリデータ | `scripts/check_cleveland_asset_manifest.py` |
| `scripts/check_strieff_facts.py` | §2 6制約＋台帳（BLOCKING・**正確性ゲート名はこの1つに統一**） | **`scripts/check_cleveland_facts.py`** |
| `scripts/build_strieff_film.py` | §5 film.json＋provenance＋beatsheet＋SRT（**実素材のみ・★factory/motion全読込**） | **`scripts/build_cleveland_film.py`**（EP46 `scripts/build_tlo_film.py` も同ロジック） |
| `scripts/validate_strieff_beats.py` | §7.9 不変条件 | **`scripts/validate_cleveland_beats.py`** |
| `scripts/gen_captions_strieff.py` | §8 構文境界字幕生成器 | **`scripts/gen_captions_cleveland.py`** |
| `scripts/ae/build_strieff_hero_cards.py` | §7 AEカードビルダ（**FIXED版＝repo path＋aerender二段＋実測フィット**） | **`scripts/ae/build_cleveland_hero_cards.py`** |
| `scripts/ae/composite_strieff_hero.py` | §7.10 コンポジタ（`beats.json` の `film_offset_sec` を読む） | **`scripts/ae/composite_caniglia_hero.py`（=EP43）** |
| `scripts/build_strieff_bgm_real.py` | §7.10 基底 mp4（narration＋BGM ミックス・**OFF=11.5**） | **`scripts/build_caniglia_bgm_real.py`（=EP43）** |

> **`build_strieff_film.py` の複製時に差し替える定数:** `SLUG="strieff"`・`EP="PD-2026-049-strieff"`・`DEFAULT_OUT=remotion/src/data/strieff_film.json`・`PUB_FILM=remotion/public/strieff/film_data.v001.json`・`SECTION_TARGETS`（§5.3）・出力パス群・`expected={"factory":93,"motion":32,"stills":101}`（**★factory は 93**）。**ロジック（`public_items()` / `repeated()` / `take()` / `allocate` / `build_figures` / `build_captions`）は1行も変えない。**
> **既存の `build_cleveland_film.py` / `gen_captions_cleveland.py` 等は触らない**（他エピソードが使用中）。EP49用に**新規コピー**する。
> **実在しない複製元名を捏造しない**（`ls scripts/` で確認済み。複製元は上表の実在ファイルのみ）。

## 0.4 完了条件（実素材で、全て緑になったら「実装完了」）

```bash
cd C:\Users\aab15\Documents\prime-documentary
PY=./.venv/Scripts/python.exe

# [B-DONE-1] マニフェスト消費側バリデータ（A の FROZEN 本番マニフェスト相手に通ること）
$PY scripts/check_strieff_asset_manifest.py \
  --assets episodes/PD-2026-049-strieff/05_visuals/asset_manifest.v001.json

# [B-DONE-2] 字幕（実測 narration の実文から構文境界で生成）
$PY scripts/gen_captions_strieff.py \
  --narr episodes/PD-2026-049-strieff/06_audio/narration_index.v001.json
$PY scripts/check_caption_breaks.py \
  episodes/PD-2026-049-strieff/08_edit/captions.final.v001.srt

# [B-DONE-3] film.json を実マニフェストから組み立てる（footage 混在必須・dochighlight 不使用・★factory93/motion16 全読込）
$PY scripts/build_strieff_film.py \
  --assets episodes/PD-2026-049-strieff/05_visuals/asset_manifest.v001.json \
  --narr   episodes/PD-2026-049-strieff/06_audio/narration_index.v001.json \
  --out    remotion/src/data/strieff_film.json

# [B-DONE-4] ★5ゲート全部（--ep 指定・animation_mix を絶対に忘れるな）
$PY scripts/check_asset_reuse.py     remotion/src/data/strieff_film.json
$PY scripts/check_motion_density.py  --ep PD-2026-049-strieff
$PY scripts/check_animation_mix.py   --ep PD-2026-049-strieff
$PY scripts/check_caption_breaks.py  episodes/PD-2026-049-strieff/08_edit/captions.final.v001.srt
$PY scripts/check_script_length.py   episodes/PD-2026-049-strieff/03_script/script.en.v001.md --json

# [B-DONE-5] 事実性/6制約（＋dochighlight 不使用・quote 逐語帰属・5-3/Scalia空席・attenuation）
$PY scripts/check_strieff_facts.py --json

# [B-DONE-6] beats 契約（AE区間 と Remotion figures[] が1秒も重ならない）
$PY scripts/validate_strieff_beats.py

# [B-DONE-7] AE カードをビルド（JSXが.aep保存）→ ★aerender で別工程レンダ → コンポジット（§7.6 二段）
$PY scripts/ae/build_strieff_hero_cards.py
"C:/Program Files/Adobe/Adobe After Effects 2026/Support Files/AfterFX.exe" -noui \
  -r "C:/Users/aab15/Documents/prime-documentary/episodes/PD-2026-049-strieff/08_edit/ae_hero/strieff_hero.jsx"
#   → render/_build_ok.txt を待つ → .aep mtime > .jsx mtime を assert → aerender で各コンプを個別レンダ
"C:/Program Files/Adobe/Adobe After Effects 2026/Support Files/aerender.exe" \
  -project ".../08_edit/ae_hero/strieff_hero.aep" -comp <id> -output ".../render/<id>.mp4"   # 各カード
$PY scripts/ae/composite_strieff_hero.py

# [B-DONE-8] Remotion Studio で目視
cd remotion && npm run studio
#   → Ep49Strieff / OpeningStrieff / Thumb-strieff-01..03 が出て、実際に動くこと
```

**台本は既に確定済み**（`EP49_strieff_script.en.v001.md`・**2,139語・12.0分**・3チェック済・ロック）。本番配置先は
`episodes/PD-2026-049-strieff/03_script/script.en.v001.md`（**1バイトも変えずコピー**・整形禁止＝AI臭再発と語数ゲート再計算を招く）。

---

# 1. 実装前に必ず読むファイル（**推測で書くな**）

| パス | なぜ読むか |
|---|---|
| `scripts/build_cleveland_film.py`（EP46 `scripts/build_tlo_film.py` も可） | **複製元。** `public_items()`/`repeated()`/`take()`/`allocate`/`build_figures`/`build_captions` をそのまま踏襲し定数だけ strieff に。**★`public_items(manifest,"factory")`・`public_items(manifest,"motion")` を必ず読む（EP45 は factory/motion 配列が空で紙芝居化した実害＝§0.5-1/§5.2）。** |
| `scripts/ae/build_cleveland_hero_cards.py` | **複製元（FIXED版）。** `fit_size()`（Python 事前フィット）/ `count_keys()` / DECK 構造 / **REPO path 出力（H: に書かない）** / **JSXが.aep保存→呼び出し側が .aep mtime>.jsx を assert してから aerender（二段）** / 実装済みレイアウト（**§7.3の6種**）/ 完了マーカー `render/_build_ok.txt` をそのまま |
| `scripts/ae/composite_caniglia_hero.py`（EP43） | **複製元。** SKIP4条件（missing / 解像度不一致 / 実測尺不足 / window past end）と ffmpeg フィルタグラフ（overlay/blend）と `film_offset_sec` の読み込みをそのまま |
| `scripts/gen_captions_cleveland.py` | **複製元。** `internal_split()` / `chunk_sentence()` / `NO_DANGLE_END` import をそのまま |
| `scripts/build_caniglia_bgm_real.py`（EP43） | **複製元。** narration＋BGM ミックスで基底 mp4 を作る経路（**OFF=11.5 に差し替え**） |
| `scripts/check_cleveland_facts.py` | **複製元（正確性ゲート）。** 構造ルールの除外実装（`asset_manifest` を R-NUM から除外・`index`/geometry キー除外・`kind!="acttitle"` 条件＝EP45修正）を**そのまま流用**（§2.3） |
| `remotion/src/components/CaseFilm.tsx` | `FilmData` 型 / `caseFilmDurationInFrames`（**4項・§5.1.1**）/ `depthSrcOf()` |
| `remotion/src/components/FigureBeats.tsx` | `FigureSpec` の**実在する `kind` 文字列**（§6.2・**全小文字**・**`dochighlight` は union に在るが使わない**）。**★votetally は `{majority:number; dissent:number; label?}`／bar は `{data?[]｜items?[]}`／timeline は `events[]`／compbars は `items[]`／routemap・pindropmap は `pins[]`／kinetic は `lines[]`／mechanism は `{mechanism:'closingdoor'｜'gears'｜'faultsplit'}`（discriminant は `kind`）** |
| `remotion/src/components/Bookends.tsx` | `OPENING_SEC=3.5` / `ENDCARD_SEC=9` / `BrandOpening` / `BrandEndcard`（実在確認済） |
| `scripts/check_asset_reuse.py` / `scripts/check_motion_density.py` / `scripts/check_animation_mix.py` / `scripts/check_caption_breaks.py` / `scripts/check_script_length.py` | 通すべき5ゲートの**実際の判定ロジック**（§9） |
| `C:\Users\aab15\Documents\pino-channel\remotion\src\Opening.tsx` | §10 の OP 正典実装 |

---

# 0.5 ★★★ EP39-48 で踏んだ失敗＝最初から防ぐ（本書の全体設計はこの6点を構造で潰している）★★★

1. **紙芝居（最重要・★EP45 の直接死因）** — 静止画100%で組むと `check_animation_mix` が FAIL する。**EP45 は build_cleveland_film が manifest の `factory[]`/`motion[]` を空で受け取り、footage が0本で紙芝居化した。**
   → **`build_strieff_film.py` は `public_items(manifest,"factory")` が 93本・`public_items(manifest,"motion")` が 16本を返すことを起動時に assert し、0本なら exit 1 で A に差し戻す。** `check_animation_mix.compute_metrics_from_film()` は film.json の `cuts[]` を **`kind=="img"` → still / それ以外 → footage** と分類する。§5 の cuts は **factory 93 + motion 32 の footage を最初から入れて still-share を cut数ベース 0.4469・frame ベース ~0.42** にする。
2. **AEカードは密度に数えられない** — `check_motion_density` は film.json の `graphics+figures+heroCuts` **のみ**数える。AEカードは ffmpeg 後合成なので**1本も数えられない**。→ §6 で **film.json 側の `figures[]` を 37本**（spec floor 31 に **+6**・`graphics[]=[]`）置く。AEカードは別勘定。
3. **FigureSpec の `kind` は実在の小文字値のみ** — 大文字名（`ActTitle`/`QuoteCard`/`VoteTally` 等）は無言で描画が消える（§6.2）。**★`dochighlight` は union に在るが1本も使わない**（黒バー/box/underline がバグに見える＝3回指摘・R-DOCHL）。
4. **台帳に無い数値を焼くな** — EP40 の生 Codex-B 出力に架空の $580,000 が入って不採用になった実害。→ §2 の事実台帳 S-ID に**検証済み値だけ**を置き、`check_strieff_facts.py` が film.json/AE/サムネ/props の全数値を台帳照合する。台帳外・`confidence:medium` の断定は FAIL（**5-3/8/2016/579 U.S. 232 のみ断定・2006年/Fackrell名/監視期間/手続経緯はヘッジ＝画面に出さない**）。
5. **字幕は台本本文と対応** — EP38 で台詞混入・「final」誤称の実害。→ §8 の字幕は **narration_index の実チャンク文をそのまま** verbatim で使う（自作しない）。
6. **レンダー前ゲート＋public_slim staging** — build 後に5ゲートを**全部**通す（animation_mix を忘れるな）。**★render 前に `public/strieff` → `public_slim/strieff` へ全メディア（img/factory/motion/audio/overlay + 各 `<stem>_depth.png`）をコピーする**（EP45 は `public_slim` が空でレンダが素材欠落した実害・§13。**media 解決 0-missing を両ディレクトリで確認**）。

---

# 2. ★ EP49固有の正確性6制約・事実性ロック（`scripts/check_strieff_facts.py`・BLOCKING）

> **この節に違反した成果物は、他が全て完璧でも出荷不可。** 検査対象は film.json の figures/captions、AE beats、
> サムネ、props、固定コメント、`03_script/script.en.v001.md`、（存在すれば）マニフェストの tags/caption_hint/qc.notes の**全文字列と全数値**。
> **正確性ゲートはこの1本に統一（`check_strieff_facts.py`）。DESIGN/CODEX_A も同名を参照する（別名を作らない）。** 出力 `09_package/facts_lock.v001.json`。

## 2.1 正確性6制約（全出力に適用・違反は BLOCKER）

| # | 制約 | 許可される表現 | 禁止 |
|---|---|---|---|
| C-1 | **停止は違法だった（州が譲歩・法廷も認定）。「合法」化しない** | 「the stop was illegal」「the State conceded there was no reasonable suspicion」「everyone agreed the stop should never have happened」「the evidence came in ONLY because of attenuation」 | 「the stop was legal」「a lawful stop」「the police were allowed to stop him」「reasonable suspicion existed」 |
| C-2 | **証拠が入るのは attenuation の一点のみ／排除法則は"狭められた"** | 「the warrant broke the chain」「the attenuation doctrine (an exception)」「the exclusionary rule normally suppresses this」「the rule was narrowed, not abolished」 | 「the exclusionary rule was abolished」「the exclusionary rule was struck down」「the rule no longer exists」「the search was legal because the stop was legal」 |
| C-3 | **attenuation 3要素を正確に（Brown v. Illinois）** | ①temporal proximity＝数分＝**抑制寄り**（州が負けた要素）②intervening circumstance＝**先在する有効な令状**（多数の決め手・鎖を断つ）③purpose/flagrancy＝**せいぜい過失・悪質でない**（州寄り）。②③が①を上回った | 「時間的近接が州に有利」「令状は関係ない」「悪質だった」等の取り違え／3要素を落として holding だけ出す |
| C-4 | **票決 5-3・Scalia空席で8名・逐語は反対に中立帰属** | 「five to three」「5 / 3」「only eight justices — Scalia's seat was vacant」「Thomas majority (Roberts, Kennedy, Breyer, Alito)」「Justice Sotomayor, dissenting」「Justice Kagan, dissenting」 | **6-3**／7-2 等の誤票決／`8-3`/`8 justices voted`／Sotomayor・Kagan 逐語を **Court/majority** に帰属／`Sotomayor, for the Court` |
| C-5 | **Edward Strieff＝R2・存命私人・象徴のみ・薬物臨床最小限** | 事件主体としての名（"Edward Strieff was stopped"）。ビジュアルは玄関の扉・駐車場・後ろ姿・パトカーのライト・ID カード・無線マイク・データベースが令状フラグに解決・手錠・小さな証拠袋・"断ち切られた鎖"・空席（8席）・天秤（3要素）・列柱 | 顔・肖像・身体・人物化／`Strieff` 直後60字の `face`/`portrait`／薬物の扇情（量・使用の描写・注射器等）／犯罪美化 |
| C-6 | **数値は台帳一致・5-3/8/2016/579 U.S. 232 のみ断定・medium はヘッジ** | 画面数値は §2.2 の台帳のみ。`5`/`3`（票決・high）・`8`（着席判事・high）・`2016`（判決年・high）・`579 U.S. 232`（cite・high）・`4`（Fourth Amendment・high）・`3`（Brown 3要素・high） | 台帳外の年/件数／**`2006`（停止年・medium）を確定カードに焼く**／`14-1373`（docket）や監視「1週間」を数字で焼く／Fackrell の名を断定表示 |
| R1 | **実在人物の顔・肖像を生成しない** | 全生成ビジュアル表示中は `AI-assisted visualization`（右下）常時／概要欄1行AI開示 | 認識可能な人物・読める偽公文書 |
| ★DH | **dochighlight 不使用** | 判読ハイライトの意図は `quote`/`stat`/`lowerthird`/`kinetic` で代替 | `figures[].kind`/beats/レイアウト名に `dochighlight`/`DOCHIGHLIGHT` を1件でも出す |

**★禁止語（`check_strieff_facts.py` が全文字列を case-insensitive 部分一致で検査。1件でも FAIL）:**
`the stop was legal` / `a lawful stop` / `lawful stop` / `legal stop` / `the stop was lawful` / `reasonable suspicion existed` / `the police were allowed to stop` /
`exclusionary rule was abolished` / `exclusionary rule abolished` / `abolished the exclusionary rule` / `struck down the exclusionary rule` / `exclusionary rule was struck down` / `the exclusionary rule no longer` /
`sotomayor, for the court` / `kagan, for the court` / `the majority dissented` / `we are all harmed` /
`6-3` / `six to three` / `eight to three` / `8-3`.
> **★重要な設計注意:** 台本本文（＝字幕 verbatim）には「That stop is the whole case」「the stop was not legal」「the drugs were the fruit」など
> **否定/正確文脈の語**（`legal`/`illegal`/`exclusionary rule`）が含まれる。上の禁止語リストは**それらと衝突しない断定形だけ**（`the stop was legal` 等の主語付き断定）を選んである。**禁止語リストに `legal`/`illegal`/`exclusionary rule` の単語単独を足すな**（字幕 verbatim を巻き込んで false FAIL する）。C-1/C-2/C-4 の**枠付き/帰属**は下の**文脈ルール**（R-LEGAL/R-ATTEN/R-VOTE/R-QUOTE）で捕える。

## 2.2 事実台帳 S-ID（`03_script/strieff_facts.v001.json`・**Bが `EP49_strieff_facts.v001.json` の ledger S00–S19 から転記して作る**）

**スキーマ版:** `strieff_facts.v1`。各 S-ID は `{"value":..., "unit":..., "verified":bool, "confidence":"high|medium", "claim_id":"", "attribution":"", "quote":""}`。
**ledger に裏付けのある値だけ `verified:true`。confidence:medium（`S17` Fackrell名・`S18` 手続履歴・`S19` 監視期間・**停止年2006**）は `画面に出さない`＝figures/AE/サムネ/props に焼かない（narration verbatim 内のみ許可）。**

| S-ID | 内容 | 使う場所 | claim | conf |
|---|---|---|---|---|
| S00 | Utah v. Strieff・**579 U.S. 232 (2016)**・docket 14-1373・decided 2016-06-20・attenuation 事件 | fig lowerthird / AE d01 | S00 | high |
| S01 | Edward Strieff・**R2 存命私人・本件後に薬物有罪**・顔なし・薬物臨床最小限・非美化 | fig lowerthird（象徴）/ caption | S01 | high |
| S02 | 匿名通報→Fackrell が約1週間断続監視→短時間の出入りを売買と読む（**期間は medium**） | fig routemap / caption | S02 | high |
| S03 | **停止は違法（州が CONCEDE・reasonable suspicion 不在・法廷も前提）** | fig kinetic/lowerthird / AE c01 | S03 | high |
| S04 | 停止中のID照会→**先在する有効な小さな交通違反逮捕状**＝intervening circumstance | fig routemap / mechanism | S04 | high |
| S05 | 逮捕状で逮捕→付随捜索でメタンフェタミン（**臨床最小限**） | fig routemap / caption | S05 | high |
| S06 | 争点＝排除法則で排除か、令状が違法停止との連結を attenuate したか | fig acttitle/kinetic | S06 | high |
| S07 | 排除法則＝通常は違法捜索の証拠を排除（fruit of the poisonous tree）／attenuation は**例外** | fig lowerthird/mechanism / AE a02 | S07 | high |
| S08 | **HOLDING＝証拠は許容**：先在の有効令状が違法停止と証拠の連結を attenuate＝令状が鎖を断った。**停止は依然違法** | fig stat/mechanism / AE v01 | S08 | high |
| S09 | **3要素**: ①temporal proximity＝数分＝抑制寄り ②intervening＝令状＝州寄り・決定的 ③flagrancy＝過失止まり＝州寄り。②③＞① | fig compbars/brightline | S09 | high |
| S10 | 票決 **5-3**・**Scalia死去で空席＝着席8名** | fig votetally/stat / AE v01 | S10 | high |
| S11 | 法廷意見＝**Justice Clarence Thomas**（Roberts・Kennedy・Breyer・Alito 加入） | fig lowerthird（帰属）/ AE 背景 | S11 | high |
| S12 | 反対＝**Sotomayor**（Ginsburg が I-III 加入・Part IV 単独）／**Kagan**（Ginsburg 加入）。中立帰属 | fig lowerthird / AE q01/q02 帰属 | S12 | high |
| S13 | Sotomayor 逐語（Part IV・**"carceral state" 感情核**）"...you are not a citizen of a democracy but the subject of a carceral state, just waiting to be cataloged." | fig quote / AE q01 | S13 | high |
| S14 | Sotomayor 逐語 "The white defendant in this case shows that anyone's dignity can be violated in this manner." | fig quote | S14 | high |
| S15 | **"we are all harmed" は逐語でない＝使わない**（NOT PRESENT 確認済） | （不使用） | S15 | high |
| S16 | Kagan 逐語 "The officer's incentive to violate the Constitution thus increases..." | fig quote / AE q02 | S16 | high |
| S17 | 刑事＝South Salt Lake City の **Fackrell**（名 Douglas は非 load-bearing・medium） | fig lowerthird（任意・名は焼かない） | S17 | medium |
| S18 | 手続＝ユタ州最高裁が排除→合衆国最高裁が破棄（許容）。medium | fig timeline（任意・年数字を焼かない） | S18 | medium |
| S19 | 監視期間・通報文言は概略（約1週間・medium） | narration のみ | S19 | medium |

> **数値の許可集合（R-NUM・narrative figure のみ対象）:** `3（Brown 3要素）/ 4（Fourth Amendment）/ 5 / 8（着席判事）/ 232 / 579 / 2016`。**これ以外の年・件数・票決が figures/AE/サムネ/props に出たら FAIL。** `2006`（停止年・S 台帳では停止の年・medium）・`14-1373`（docket）・監視「1週間」は**画面禁止**（narration verbatim 内は R-NUM 対象外＝§2.3 の構造除外と別に script.md は verbatim 例外）。**★`6`（"6-3" 誤票決）は R-VOTE で明示 FAIL。**

## 2.3 `check_strieff_facts.py` の検査（exit 0=PASS / 1=FAIL / 2=スキーマ不一致）

**★複製元 `check_cleveland_facts.py` の構造除外を1行も削らない（EP45修正）:**
- `asset_manifest*.json` は **R-NUM の対象から除外**（`if not path.name.startswith("asset_manifest")` で構造カウント 85/16/93/12 を巻き込まない）。
- `start/end/dur/fps/width/height/frames/duration_sec/x/y/index` キーは**構造値**として R-NUM スキップ（`acttitle` の `index` 等）。
- 文脈ルールは `kind != "acttitle"` のとき発火（幕頭タイトルを巻き込まない）。

**検査対象ファイル（この一覧をハードコード。存在するものだけ検査し、無いものは `skipped[]` に必ず明記）:**

```
episodes/PD-2026-049-strieff/03_script/script.en.v001.md
episodes/PD-2026-049-strieff/03_script/strieff_facts.v*.json
episodes/PD-2026-049-strieff/08_edit/ae_hero/beats.json
episodes/PD-2026-049-strieff/09_package/*.json        （title / description / thumbnail headlines）
episodes/PD-2026-049-strieff/09_package/*.txt         （固定コメント・description.txt）
episodes/PD-2026-049-strieff/05_visuals/asset_manifest*.json  （tags / caption_hint / qc.notes・★R-NUM 除外）
remotion/src/data/strieff_film.json                   （figures[].text / figures[].lines[] / figures[].kind / captions[] の全文字列と数値）
remotion/props/strieff*.json                          （title / subtitle）
```

- **R-FORBID（最優先）** — §2.1 の禁止語（主語付き断定形）が対象文字列に出たら即 FAIL。**`legal`/`illegal`/`exclusionary rule` の単独単語を禁止語に足さない**（字幕 verbatim を巻き込む・§2.1 注意）。
- **R-LEGAL（C-1/C-2・BLOCKING）** — 停止の合法性を語る payload（`stop` かつ `legal`/`lawful`/`suspicion` を含む・`kind!="acttitle"`）は「illegal / conceded / no reasonable suspicion / should never have happened」のいずれかを同伴。§2.1 の断定禁止語（`the stop was legal` 等）が出たら FAIL。排除法則を語る payload（`exclusionary rule` を含む）に `abolished`/`struck down`/`no longer` が付いたら FAIL（**"narrowed"/"an exception"/"attenuation" 枠は可**）。
- **R-ATTEN（C-3・BLOCKING）** — attenuation/holding を語る payload（`attenuat`/`warrant broke`/`intervening`/`the evidence stays` を含む）は、**証拠が入る理由を令状（intervening circumstance）に帰す**こと。3要素を出すカード（compbars/brightline）は ①temporal＝**suppress 寄り** ②warrant＝**admit/state 寄り** ③flagrancy＝**negligent/admit 寄り** の向きを保持（逆向きは FAIL）。「the search was legal because the stop was legal」は FAIL。
- **R-VOTE（C-4・BLOCKING）** — 票決を出す payload は `5`＋`3`（or `five`＋`three`）で、`8` を出す文脈は「eight justices / Scalia's seat vacant」枠。**`6`/`six`/`8-3`/`eight to three` を票決値として出したら FAIL**（fetch 要約の "6-3" 誤り再発防止）。`votetally` は `{majority:5, dissent:3}`（実在 union・**`for`/`against` ではない**）。
- **R-QUOTE（C-4・R-ATTRIB・BLOCKING）** — `quote[].attribution` は非空・逐語のみ（要約を引用符に入れない）。許可対応表:
  ```python
  APPROVED_QUOTES = {
    # S13 Sotomayor "carceral state"（Part IV・逐語の連続部分列を許可）
    "it implies that you are not a citizen of a democracy but the subject of a carceral state, just waiting to be cataloged":
        "Justice Sotomayor, dissenting",
    # S14 Sotomayor "anyone's dignity"（"everyone is harmed" 論点の正確な逐語版）
    "the white defendant in this case shows that anyone's dignity can be violated in this manner":
        "Justice Sotomayor, dissenting",
    # S16 Kagan incentive（逐語の連続部分列を許可）
    "the officer's incentive to violate the constitution thus increases":
        "Justice Kagan, dissenting",
  }
  ```
  **Sotomayor / Kagan 逐語に `dissenting` 以外の帰属（`for the Court`/`majority`/`the Court`）が付いたら FAIL。** **★`"we are all harmed"` が対象文字列（quote/hero/caption/thumb/props）に1件でも出たら FAIL**（S15＝逐語でない）。要約を引用符に入れたら FAIL。
- **R-FACE（C-5/R1）** — `has_readable_text`/`has_identifiable_face`/`has_human_body` が true の項目は `role=="reject"`。`ai_prompts.v001.md` 正プロンプトの `portrait`/`face of`/`likeness`/`Edward Strieff`（人物として）/`his face`/`mugshot`/薬物扇情語（`injecting`/`needle`/`drug use`/`overdose`）は FAIL（ネガティブでの使用は可）。`Strieff` 直後60字の `face`/`portrait` で FAIL。生成ビジュアル区間の `AI-assisted visualization` 欠落・`description.txt` の AI 開示行欠落で FAIL。
- **R-NUM（C-6・narrative のみ）** — figures[] の `value`/`majority`/`dissent`/`numKeys` 到達値、AE `beats[].value`/`beats[].hero`/`beats[].left`/`beats[].right`、サムネ数字に現れる**あらゆる数値**は §2.2 許可集合 `{3,4,5,8,232,579,2016}` に**完全一致**必須。**`2006`（停止年・S 台帳 medium）・`14`/`1373`（docket）・監視「1週間」が figures/AE/サムネ/props に出たら FAIL**。**★`asset_manifest*.json` は R-NUM 対象外**（構造カウント 85/16/93/12 の false-positive 回避＝EP45修正）。
- **R-HEDGE（C-6）** — `confidence:medium` の S-ID（S17 Fackrell名・S18 手続・S19 監視期間・停止年2006）を `verified:true` かつ画面焼き込みしたら FAIL。断定可は **5-3（S10）・8（S10）・2016（S00）・579 U.S. 232（S00）** のみ。
- **R-DOCHL（★DH・BLOCKING）** — `strieff_film.json` の `figures[].kind` に `dochighlight` が1件でも出たら FAIL
  （`grep -c '"kind"[[:space:]]*:[[:space:]]*"dochighlight"'` が 0 でなければ FAIL）。`beats.json`/レイアウト名にも `dochighlight`/`DOCHIGHLIGHT` を出さない。
- **R-DATE** — 判決日 **2016-06-20** と cite（579 U.S. 232）を取り違えない。停止年 2006 を判決年 2016 に混同しない。

**出力:** `episodes/PD-2026-049-strieff/09_package/facts_lock.v001.json`（`{"pass":bool,"violations":[{"file","rule","line","excerpt"}],"skipped":[...]}`）。
**`pass:true` でない限り `check_final_acceptance.py` に進んではならない。** **CLI:** `--json`。対象ファイル未生成はスキップして必ずログに出す（「無いから通した」を黙るな）。

---

# 3. ★境界契約: `asset_manifest.v001.json`（Aから受け取る唯一のファイル・FROZEN）

## 3.1 スキーマ（**Aが生成する。Bはこの形を前提に読む・A↔B 1バイト一致**）

**スキーマ版:** `strieff_assets.v1`（固定文字列。異なれば **exit 2**）。
EP49 spec の点数に一致: **still_body 85 / still_i2v_source 16 / motion 16 / factory 93 / overlay 12**。
**★サムネは独立の分類を持たない。** body 85枚のうち**6枚**に `also_thumb:true` を立てて流用する（**`role=thumb`/`still_thumb` を作らない**・サムネ用 count キーも無い・§11）。
**このスキーマ・`counts` キー・`role` enum・`overlay` 枚数は CODEX_A（生産者）の出力と1バイト単位で同一。**

- **`role` enum（固定・3値のみ）:** `"body"` | `"i2v_source"` | `"reject"`。**`thumb`/`still_thumb` を作らない。**
- **`counts`（固定キー・確定値）:** `{ "still_body": 85, "still_i2v_source": 16, "motion": 16, "factory": 93, "overlay": 12 }`。

```jsonc
{
  "schema_version": "strieff_assets.v1",
  "episode_id": "PD-2026-049-strieff",
  "slug": "strieff",
  "generated_at": "<ISO8601>",
  "producer": "scripts/build_strieff_asset_manifest.py",
  "is_stub": false,
  "counts": { "still_body": 85, "still_i2v_source": 16, "motion": 16, "factory": 93, "overlay": 12 },

  "stills": [
    { "asset_id": "STR-S01", "scene_id": "S01", "role": "body",
      "also_thumb": false,                     // body から6枚だけ true（§11 の6 asset ID・追加生成しない）
      "act": 0,                                // 0=HOOK/OP, 1..3=幕, 5=ED
      "public_path": "strieff/img/S01.png",    // ★Bが cuts[].src に入れる値（1シーン1枚＝固有プロンプト・_01 等の接尾なし）
      "depth_path": "H:/pd-media/assets/ai/strieff/S01_depth.png",  // role=="body" は実在必須
      "width": 3840, "height": 2160,
      "sha256": "...", "tags": ["front_door","parking_lot","symbolic"], "caption_hint": "a front door of a house at dusk, no people",
      "source": "ai_codex", "commercial_use": "allowed", "ai_disclosure_required": true,
      "qc": {"reviewed": true, "on_theme": true,
             "has_readable_text": false, "has_identifiable_face": false, "has_human_body": false, "notes": ""} }
    // i2v 種は role=="i2v_source"・asset_id "STR-MS01".."STR-MS16"・public_path は null（本編カットに出ない）
  ],

  "motion": [   // ★16本。build_strieff_film が public_items(manifest,"motion") で全読込（空なら exit 1）
    { "asset_id": "STR-M01", "source_scene_id": "M01_src",
      "source_still": "H:/pd-media/assets/ai/strieff/M01_src.png",
      "public_path": "strieff/motion/M01_rife.mp4",   // ★必ず .mp4 かつ "_rife" を含む
      "act": 0, "width": 1280, "height": 720, "fps": 48, "frames": 164, "duration_sec": 3.417,
      "sha256": "...", "tags": ["database_line","warrant_flag"],
      "qc": {"reviewed": true, "on_theme": true, "artifact_free": true, "notes": ""} }
  ],

  "factory": [  // ★93本。build_strieff_film が public_items(manifest,"factory") で全読込（空なら exit 1）
    { "asset_id": "AF-BG-0731",
      "public_path": "strieff/factory/AF-BG-0731__parking_lot_night.mp4",  // ★必ず "/factory/" を含む
      "type": "backgrounds", "subtype": "parking_lot", "kind": "video",
      "license": "Pexels License", "sha256": "...", "act": 1, "covers_scene_id": "S04",
      "duration_sec": 7.60, "width": 1920, "height": 1080,
      "eyeballed_content": "an empty parking lot at night, patrol light glow, no people, no readable plates",
      "qc": {"reviewed": true, "on_theme": true, "no_watermark": true,
             "no_recognizable_person": true, "no_cartoon": true, "label_matches_content": true, "notes": ""} }
  ],

  "overlay": [  // ちょうど12本。cuts[].src に出さない（§5.5）
    { "asset_id": "AF-PART-0044",
      "public_path": "strieff/overlay/AF-PART-0044__dust_motes.mp4",
      "type": "particle_assets", "subtype": "dust_motes", "license": "Pexels License",
      "sha256": "...", "blend_hint": "screen",
      "eyeballed_content": "slow drifting dust on black, loops cleanly",
      "qc": {"reviewed": true, "on_theme": true, "no_watermark": true, "notes": ""} }
  ]
}
```

## 3.2 Bがこのマニフェストから作るもの（**EP49 spec の cuts 割当**）

| マニフェスト | Bでの使い道 | spec |
|---|---|---|
| `stills[role="body"]` 85枚 | **静止画カット101本**（`kind:"img"`, `treatment` 循環）・**各≤2回** | still distinct85/cuts101 |
| body 静止画で `also_thumb==true` の6枚 | サムネ3案の背景（§11・6 asset ID） | — |
| `stills[role="i2v_source"]` 16枚 | **本編カットに出さない**（i2v 種・A が Wan で motion 化済み） | — |
| `motion` 16本 | **i2vカット32本**（`kind:"footage"`）・**各≤2回** | motion distinct16/cuts32 |
| `factory` 93本 | **実写カット93本**（`kind:"footage"`）・**各1回のみ** | factory distinct93/cuts93 |
| `overlay` 12本 | **`cuts[].src` に出さない**（§5.5 の合成レイヤー扱い） | — |

**合計 101 + 32 + 93 = 226 カット / distinct 85+16+93 = 194 / first-use 194/226 = 0.8584 ✓（floor 0.70）**

## 3.3 `scripts/check_strieff_asset_manifest.py`（消費側バリデータ・BLOCKING）

```bash
$PY scripts/check_strieff_asset_manifest.py --assets <path> [--json]
```

検査（1つでも違反で exit 1。`schema_version` 違いだけ exit 2）:

1. `schema_version=="strieff_assets.v1"` / `episode_id=="PD-2026-049-strieff"` / `slug=="strieff"` / `is_stub==false`
2. `counts.*` が各配列の実長と一致し**確定値**: `still_body==85` / `still_i2v_source==16` / `motion==16` / `factory==93` / `overlay==12`
3. `role` は **`body`/`i2v_source`/`reject` の3値のみ**（`thumb`/`still_thumb` が現れたら FAIL）
4. `role=="body"` の全静止画で `public_path` 非null、かつ `remotion/public/<public_path>` と `<stem>_depth.png` が**両方実在**（`depthSrcOf()=src.replace(/\.[^.]+$/,'_depth.png')`。depth 欠落はレンダークラッシュ）。`role=="i2v_source"` は `public_path==null`
5. `role!="reject"` の全静止画で `max(width,height)>=3840`（`preflight_render_gate.MIN_LONG_EDGE_PX=3840`）
6. `motion[].public_path` が `.mp4` で終わり `_rife` を含む。`motion[].source_scene_id` は `stills[role=="i2v_source"]` の種 ID（`M01_src` 系）を指す
7. `factory[].public_path` が `/factory/` を含む
8. `overlay[].public_path` が `/overlay/` を含み `/factory/` を**含まない**・`overlay` 配列長が**ちょうど12**
9. `sha256` が全配列を通して一意（EP39〜48 の素材と sha256 被りゼロは A が保証・B は自集合内一意を検査）
10. `factory[].eyeballed_content` が非空、かつ `qc.label_matches_content==true`
11. `qc.has_readable_text` / `qc.has_identifiable_face` / `qc.has_human_body` が true の項目は `role=="reject"`（R1）
12. `also_thumb==true` の body 静止画が**ちょうど6枚**、かつ **`scene_id` 集合が §11 の6 ID と完全一致**（A↔B 契約点。**CODEX_A の also_thumb 集合と一字一致**）
13. **全文字列値**が §2 の R-FORBID / R-FACE / R-DOCHL を通る（**R-NUM は asset_manifest を除外**＝§2.3）

> **★このバリデータは A の `--verify` と同じ不変条件を独立実装する（二重チェック）。** counts が §3.1 の確定値と食い違ったら組まずに止めて A に差し戻す（ブリーフ§2: still を増やして factory を削るな）。**★特に `factory==93` と `motion==16` が非0であることを最優先で assert（EP45 空配列事故の直接防止）。**

---

# 4. narration_index（TTS は課金＝禁止。**実測版を消費**する）

## 4.1 なぜ narration_index か
`build_strieff_film.py` は**尺・区間・字幕を narration_index から導出する**。**秒数をコードに直書きしない。** 唯一の正は narration_index。

## 4.2 スキーマ（`strieff_narration.v1`）

```jsonc
{
  "schema_version": "strieff_narration.v1",
  "episode_id": "PD-2026-049-strieff",
  "is_stub": false,
  "total_seconds": 720.6,        // = SPEC narration_seconds（[SILENCE 1] の実音無音を含む）
  "chunks": [
    { "section": "HOOK", "start": 0.000, "end": 4.100, "text": "..." },
    { "section": "OP",   "start": 65.700, "end": 69.800, "text": "..." },
    { "section": "ACT_1","start": 125.300, "end": 129.400, "text": "..." }
  ]
}
```

**section 値（固定・6幕）:** `HOOK` / `OP` / `ACT_1` / `ACT_2` / `ACT_3` / `ENDING`。**ACT_4 は無い。**
`build_strieff_film.py` は `section_windows()`（各 section の最初のチャンク start）で幕境界を得る。
**台本の `【SILENCE 1 — 1.8s】` は HOOK 内1箇所**（man's back のホールド・完全無音）。narration_index の実測がこの無音を **total_seconds に内包**している。**存在しない演出マーカーを発明しない。**

## 4.3 spec のタイムライン（**設計目標。実タイミングは narration_index が上書きする**）

| section | 語数 | 秒（目安） | 備考 |
|---|---|---|---|
| HOOK | 195 | 65.7 | VO。途中に `SILENCE 1 — 1.8s`（man's back・完全無音） |
| （gold `BrandOpening`） | 0 | 3.5 | 非VO。`OPENING_SEC`。**HOOK の問いが landした後に resolve**（frame0 ではない） |
| OP | 177 | 59.6 | 二人称の thesis ＋ "THE WARRANT IN YOUR POCKET" タイトル＋ channel ID |
| ACT_1 The stop | 389 | 131.0 | 最短・抑制。監視→違法停止→令状→逮捕→捜索→メタンフェタミン→ユタ州最高裁が排除 |
| ACT_2 The exclusionary rule | 383 | 129.0 | 排除法則・fruit of the poisonous tree・attenuation（例外）・3要素の set up |
| ACT_3 The ruling | 553 | 186.3 | **最も遅く長い**。5-3・Scalia空席・3要素の適用・Sotomayor "carceral state"・Kagan incentive |
| ENDING | 359 | 120.9 | ペイオフ→CTA。"the illegal stop becomes almost free"・排除法則が狭まった余韻 |
| （`BrandEndcard`） | 0 | 9.0 | 非VO。`ENDCARD_SEC` |

**唯一の正は `python scripts/check_script_length.py <script> --json`。** 総語数 **2,139**（spec `words_total`）/ `wpm 178.1` /
narration_seconds **720.6**（spec）。**自己申告・体感の尺判定は禁止。**

## 4.4 実測 narration_index の受領
本番は別工程が TTS→faster-whisper で `06_audio/narration_index.v001.json`（実測語タイム・`is_stub:false`）を作る。
**これは課金ジョブなので B は起動しない。** 来た `narration_index.v001.json` を `--narr` に渡すだけ。**台本本文はそのまま（改変しない）。**

---

# 5. `strieff_film.json` の構築（`scripts/build_strieff_film.py`＝`build_cleveland_film.py` の複製・実素材のみ）

## 5.1 `FilmData` 型（`CaseFilm.tsx` から。これに従う）

```ts
export type Cut = {start:number; dur:number; kind:'img'|'footage'; src:string; treatment:string; seed:string};
export type FilmData = {
  fps:number; narration:string; narrationSeconds:number; hookSeconds:number; hookLine:string;
  hook:{start:number;dur:number;kind:string;src:string;seed:string}[];
  cuts:Cut[]; captions:{start:number;end:number;text:string}[];
  graphics:{start:number;end:number;lines:string[]}[];      // 必須フィールド。EP49 は []
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
- **`fps = 30`**（film fps）。`narration = "strieff/narration.mp3"`（実在）
- **★`hookSeconds = 8.0`**（ブリーフ§5 明示）／**★`hookLine`＝strieff固有**（下記・流用禁止）:
  ```
  "A stop with no reason. A warrant. A search the law now lets count."
  ```
  （**別エピソードの hookLine を焼かない**。停止は理由なし＝違法／令状／証拠が counts する、を1行で。C-1/C-2 と整合）

### 5.1.1 ★durationInFrames の4項関数（明示・total ≤ 750s を assert）

```
caseFilmDurationInFrames(strieffFilm, fps=30)
  = round(hookSeconds * fps)        // ★hookSeconds = 8.0（ブリーフ§5 明示）→ round(240) = 240
  + round(OPENING_SEC * fps)        // OPENING_SEC = 3.50（gold BrandOpening は HOOK の後）→ round(105) = 105
  + ceil(narrationSeconds * fps)    // narrationSeconds = narration_index.total_seconds（= 720.6・silence 込み）→ ceil(21618.0) = 21618
  + round(ENDCARD_SEC * fps)        // ENDCARD_SEC = 9.00 → round(270) = 270
```

- **★hookSeconds を明示: `hookSeconds = 8.0`**（EP49 ブリーフ§5・§7 完了条件。frame0 の flash-forward モンタージュ尺として 8.0s を積む。EP45 の 0.0 と異なる＝**必ず 8.0**）。
- 概算（fps30・narration 720.6）: `240 + 105 + 21618 + 270 = 22233 frames = 741.1s`。**★id=Ep49Strieff の durationInFrames は 22233。**
- **ビルダ末尾で `assert total_frames/fps <= 750.0`**（741.1 ≤ 750 ✓）。超えたら exit 1。

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
    (i) cut数ベース   still-share = 101/226 = 0.4469        ✓ <=0.45（★余裕 0.31%＝極薄・下の警告）
        motion coverage = (93+32)/226 = 125/226 = 0.5531   ✓ >=0.45（spec と一致）
    (ii) frame ベース still 平均 3.00s → 101×3.00 = 303.0s
        footage 平均 ~3.34s → 125×3.34 ≈ 417.6s
        still-frame-share = 303.0 / 720.6 = 0.4205          ✓ <=0.45（cut数比より安全側）
        motion-coverage(frame) = 417.6 / 720.6 = 0.5795     ✓ >=0.45

[D] 平均ショット長（spec mean_shot 3.19 / max 6.0）
    720.6 / 226 = 3.189 秒/カット                           ✓ <=6

[E] factory 下限（30秒に1本 = 24 → >=24本） 93本            ✓
```

> **★[C](i) の cut数ベース still-share 0.4469 は cap 0.45 に極めて薄い（余裕 0.31%）。still を1枚増やすか factory を1本削ると即 0.45 超過で FAIL。**
> **マニフェストが still 85 / factory 93 / motion 16 を割ったら組まずに止めて A に差し戻す（ブリーフ§2: still を増やして factory を削るな）。frame ベースも下回るよう still の平均尺を footage より系統的に短く保つ（§5.3-5）。**

## 5.3 カット割り当てのルール（`build_cleveland_film.py` の `allocate()`/`take()`/`repeated()` を踏襲）

1. 各幕の秒窓を `section_windows()` から取り、幕内に **factory : motion : still を按分**（★下表は**非拘束の目安**・実配分は narration_index の窓長で自動調整。確定値は「合計 factory 93 / motion 32 / still 101」だけ）:

   | section | factory | motion | still | 小計 |
   |---|---|---|---|---|
   | HOOK+OP | 13 | 5 | 15 | 33 |
   | ACT_1 | 15 | 5 | 17 | 37 |
   | ACT_2 | 17 | 6 | 20 | 43 |
   | ACT_3 | 30 | 10 | 30 | 70 |
   | ENDING | 18 | 6 | 19 | 43 |
   | **計** | **93** | **32** | **101** | **226** |

2. **factory は各1回のみ**（使用済み集合を持ち二度と引かない）。**motion は各≤2回・still は各≤2回**（`repeated(pool, need, cap, key)`）
3. **同一素材を連続させない**（順序を散らす）
4. 静止画 `treatment` は `["depth","scan","duotone","focus"]` を循環（同じ treatment を3連続させない）
5. **still の `dur` を footage の `dur` より系統的に短く**（§5.2[C]・still 側の重みを小さめに）
6. motion の `dur` は **3.0–3.4秒**（実素材 3.417s。超えるとループが見える）
7. **AEカードの区間（§7.2）に重なるカットも存在させる**（コンポジタ SKIP 時に穴が空かないため）

## 5.4 `figures[]` と `captions[]`
- `figures[]` は §6（**37本**・spec floor 31 に +6・`graphics[]=[]`・**dochighlight 不使用**）
- `captions[]` は narration_index の全チャンクを **verbatim**（`build_captions()` と同一）。SRT も同時出力

## 5.5 合成レイヤー（`overlay`）— **`cuts[].src` に出さない**
`overlay` 12本は「加工」。`cuts[].src` に入れると factory 判定（上限1回）になり FAIL する。
`strieff_film.json` に **`overlays` 独自キー**で持たせる（`CaseFilm` は未知キーを無視）か、専用レイヤーで `screen` 合成する。

## 5.6 ビルダが出力する成果物

| 出力 | パス |
|---|---|
| film.json | `remotion/src/data/strieff_film.json` |
| public コピー | `remotion/public/strieff/film_data.v001.json` |
| **build provenance** | `episodes/PD-2026-049-strieff/04_scenes/strieff_build_manifest.v001.json`（**A の `05_visuals/asset_manifest` に書かない**） |
| **beatsheet**（figures+AE区間の突き合わせ表） | `episodes/PD-2026-049-strieff/04_scenes/strieff_beatsheet.v001.json` |
| SRT（字幕未生成時のフォールバック） | `episodes/PD-2026-049-strieff/08_edit/captions.final.v001.srt`（**§8 の生成器が上書きする**） |

> **★beatsheet の命名に関する重大な注意:** `check_motion_density` / `check_animation_mix` は `04_scenes/premium_beatsheet.v*.json` を**自動検出して film.json より優先**する。
> **B の beatsheet は `strieff_beatsheet.v001.json`（`premium_` を付けない）** にして**ゲートの測定源を film.json 一本に保つ**（二重ソース乖離＝EP39/40 の矛盾28件の原因を避ける）。`strieff_beatsheet` は provenance と `validate_strieff_beats` 専用。

## 5.7 CLI
```bash
$PY scripts/build_strieff_film.py \
  --assets episodes/PD-2026-049-strieff/05_visuals/asset_manifest.v001.json \
  --narr   episodes/PD-2026-049-strieff/06_audio/narration_index.v001.json \
  --out    remotion/src/data/strieff_film.json \
  [--captions episodes/PD-2026-049-strieff/08_edit/captions.final.v001.srt]
```
**実素材のみ。`is_stub==true` のマニフェストを渡されたら exit 1。★`public_items(manifest,"factory")` が空 or `!=93`、`public_items(manifest,"motion")` が空 or `!=16` なら exit 1（EP45 空配列事故防止）。** 末尾に `check_asset_reuse` 相当の自己レポートを print する。

---

# 6. Remotion 側 `figures[]`（**37本・spec floor 31 に +6・`graphics[]=[]`・dochighlight 不使用**）

## 6.1 密度の検算（`check_motion_density`・**AEカードは1本も数えられない**）

```
figures 37本（film.json） / body 12.01分(=720.6/60) = 3.08 /分       ✓ beats_per_min_floor 2.5
coverage: 37本 × 平均6.0s = 222.0s / 720.6 = 30.8%                    ✓ MIN_ANIMATED_COVERAGE 0.25
variety : 下記 kind を15種使用                                        ✓ variety_floor 3
spec motion.beats_floor = 31 に対し 37 で余裕。coverage が最も薄いので figures の dur は 5.4–6.0s を基本に。
```

> **★3軸すべて AND。density/coverage/variety のどれか1つでも floor 未満で FAIL。** 37本を非重複で置き平均 dur を 6.0s 程度に確保。

## 6.2 ★★★ `FigureSpec` の `kind` は**実在する小文字値のみ・`dochighlight` は使わない** ★★★

> **大文字名（`ActTitle`/`QuoteCard`/`VoteTally`…）は `FigureBeats.tsx` の union に無く、無言で描画が消える。`comparebars` は非在→`compbars`。** **★`dochighlight` は union に在るが1本も使わない**（R-DOCHL）。

**EP49 で使う実在 `kind`（`remotion/src/components/FigureBeats.tsx` の union から確認済み・全て `start`/`end` 必須・全小文字）:**

| `kind` | 必須プロパティ（**実 union**） | EP49での用途 |
|---|---|---|
| `acttitle` | `title:string` / `kicker?` / `index?` | 幕頭「THE ILLEGAL STOP」/「THE EXCLUSIONARY RULE」/「THE RULING」 |
| `kinetic` | `lines:string[]` / `style?:'wordpop'\|'maskslide'\|'emphasis'` / `emphasisWords?` | "THE WARRANT IN YOUR POCKET" / "THE STOP WAS ILLEGAL" / "ATTENUATION" / "THE ILLEGAL STOP BECOMES ALMOST FREE"（emphasisWords 1–2語） |
| `stat` | `value:number` / `label:string` / `prefix?` `suffix?` `topLabel?` | **3** BROWN FACTORS / **8** JUSTICES — SCALIA'S SEAT EMPTY / **5**–**3**（votetally 併用） |
| `numberticker` | `value:number` / `label?` / `prefix?` `suffix?` `decimals?` | **2016** DECIDED / **579** (U.S. 232) |
| `quote` | `quote:string` / `attribution:string` | **Sotomayor 逐語 S13/S14・Kagan 逐語 S16** のみ・§2 `APPROVED_QUOTES` 一致・attribution `"Justice … , dissenting"` |
| `lowerthird` | `primary:string` / `secondary?` / `accent?` | 開示 `AI-assisted visualization` / The Fourth Amendment / Utah v. Strieff, 579 U.S. 232 / The exclusionary rule / Detective Fackrell — South Salt Lake City（名を焼かない・任意） |
| `compbars` | `items:{label:string;value:number;accent?}[]` | ①TIME → SUPPRESS vs WARRANT → ADMIT（S09）②majority: attenuated vs dissent: incentive（S12/S16）③3要素の weight |
| `votetally` | **`majority:number` / `dissent:number` / `label?`**（実在 kind＝`votetally`・**`for`/`against` ではない**） | **5-3**（majority=5, dissent=3・S10・C-4 中立） |
| `timeline` | `events:{year:string;text:string}[]` | 手続: the stop → the search → **2016** the ruling（S18・年数字を焼くのは 2016 のみ・2006 を焼かない） |
| `pindropmap` | `pins:{x,y,label?}[]` | South Salt Lake City, Utah（単一ピン・C-5 顔なし・S02） |
| `routemap` | `pins:{x,y,label?}[]` / `label?` | ACT1 の因果の鎖: stop → ID check → warrant hit → arrest → search → evidence bag（S03-S05・象徴） |
| `statemap` | `label?` / `states?` | ENDING「outstanding warrants exist across the country」（S 論点・過大化しない・数を焼かない） |
| `brightline` | `mode?:'draw'\|'hold'\|'slam'` | 排除法則の原則 vs attenuation 例外（S07・S09） |
| `mechanism` | `mechanism:'closingdoor'\|'gears'\|'faultsplit'` ★discriminant は `kind`・変種は `mechanism` | ①warrant が鎖を断つ(faultsplit)＝attenuation の視覚(S04/S08)②ENDING「a door held open」＝unlawful stop が pay off(closingdoor)(S… ENDING) |
| `bar` | `data?[]` or `items?[]` | ①「three factors weighed」の重み比較（qualitative・数値は台帳内 3 のみ） |

**`quote[].attribution` は §2 の `APPROVED_QUOTES` に一致させる（`"Justice Sotomayor, dissenting"` / `"Justice Kagan, dissenting"`）。逐語のみ・要約を引用符に入れない・"we are all harmed" を書かない。**
**★`kind` に `dochighlight` を1件も置かない（R-DOCHL・`check_strieff_facts` が grep で 0 を確認）。**

## 6.3 figures 配分（**全 37 を figures[]・graphics[]=[]**）

| kind | 枠数 |
|---|---|
| `acttitle` | 4 |
| `kinetic` | 5 |
| `stat` | 4 |
| `numberticker` | 2 |
| `quote` | 3 |
| `lowerthird` | 6 |
| `compbars` | 3 |
| `votetally` | 1 |
| `timeline` | 2 |
| `pindropmap` | 1 |
| `routemap` | 1 |
| `statemap` | 1 |
| `brightline` | 1 |
| `mechanism` | 2 |
| `bar` | 1 |
| **合計** | **37**（variety = 15 種・**dochighlight を含めない**） |

> **★実装表現:** 上記 37本を**すべて `figures[]`** に入れ、**`graphics[]=[]`** にする（`check_motion_density` は `figures+graphics+heroCuts` を合算するので密度は同値・floor 31 に +6）。

## 6.4 figures アンカー設計（`build_cleveland_film.py` の `FIGURE_ANCHORS` 方式）

**方式:** `(anchor_sec, payload)` の配列を秒昇順に置き、`build_figures()` が
`end = min(anchor+FIG_DUR, next_anchor-FIG_GAP, total-0.5)` でクランプ、`end-start < FIG_MIN_DUR` なら **exit 1**。
`FIG_DUR=6.0 / FIG_MIN_DUR=3.0 / FIG_GAP=0.4`。**アンカー秒は narration_index の section 窓に対する相対で決め `section_windows()` を基準にオフセットで置く**（秒直書き禁止）。

**配置方針（37本・§2 台帳の値だけ焼く・kind を分散・6制約順守・dochighlight 不使用）:**

- **HOOK/OP（7）:** `lowerthird`（`AI-assisted visualization` 開示）/ `kinetic`（"THE WARRANT IN YOUR POCKET"）/ `pindropmap`（**S02 South Salt Lake City, Utah**・単一ピン）/ `kinetic`（"A STOP WITH NO REASON"・emphasisWords=["NO REASON"]）/ `lowerthird`（**The exclusionary rule** — illegal searches are normally thrown out・S07）/ `acttitle`（THE ILLEGAL STOP）/ `lowerthird`（**Utah v. Strieff, 579 U.S. 232**・S00）
- **ACT_1（8）:** `acttitle`（THE STOP）/ `routemap`（stop→ID check→warrant hit→arrest→search→evidence bag・S03-S05）/ `kinetic`（"THE STOP WAS ILLEGAL"・emphasisWords=["ILLEGAL"]・**S03 州が CONCEDE**）/ `lowerthird`（**No reasonable suspicion** — the State conceded・S03）/ `mechanism:faultsplit`（**S04** the pre-existing warrant surfaces — the intervening circumstance）/ `stat`（**4** label "THE FOURTH AMENDMENT — unreasonable searches and seizures"・S07）/ `lowerthird`（**Detective Fackrell** — South Salt Lake City・S17／**名 Douglas を焼かない**・任意）/ `bar`（**S09** three factors weighed・qualitative）
- **ACT_2（8）:** `acttitle`（THE EXCLUSIONARY RULE）/ `brightline`（**S07** normally: illegal stop → evidence suppressed）/ `lowerthird`（**Fruit of the poisonous tree** — the stop poisons what grows from it・S07）/ `kinetic`（"ATTENUATION"・style maskslide・**S06 the exception**）/ `compbars`（**S09** ① time → suppress vs ② the warrant → admit）/ `stat`（**3** label "BROWN v. ILLINOIS FACTORS"・S09）/ `mechanism:faultsplit`（**S06** did the warrant snap the chain?）/ `kinetic`（"DID THE WARRANT BREAK THE CHAIN?"）
- **ACT_3（10）:** `acttitle`（THE RULING）/ `numberticker`（**S00 2016**, label "decided — Supreme Court"）/ `votetally`（**5-3**・majority=5 dissent=3・S10・C-4 中立）/ `stat`（**8**, label "JUSTICES SAT — SCALIA'S SEAT WAS EMPTY"・topLabel "5–3"・S10／**C-4 8-3 と読ませない**）/ `lowerthird`（**Justice Clarence Thomas** — for the majority・S11）/ `compbars`（**S09** ③ flagrancy: at most negligent → admit — the majority's view）/ `mechanism:faultsplit`（**S08** the warrant broke the chain — the evidence stays）/ `quote`（**S13** Sotomayor "carceral state" → "Justice Sotomayor, dissenting"）/ `quote`（**S16** Kagan incentive → "Justice Kagan, dissenting"）/ `quote`（**S14** Sotomayor "anyone's dignity" → "Justice Sotomayor, dissenting"）
- **ENDING（4）:** `kinetic`（"THE ILLEGAL STOP BECOMES ALMOST FREE"・emphasisWords=["FREE"]／**C-1/C-2**）/ `statemap`（**S** outstanding warrants exist across the country — often for something small・数を焼かない）/ `mechanism:closingdoor`（**ENDING** a door held open — an unlawful stop pays off when a warrant is waiting）/ `lowerthird`（開示 `AI-assisted visualization` 再掲）

> **★停止を語る payload には必ず "illegal / conceded / no reasonable suspicion"（C-1・R-LEGAL）。「the stop was legal」を書かない。attenuation/holding を語る payload は令状（intervening circumstance）に証拠許容を帰す（C-3・R-ATTEN）。**
> **Sotomayor / Kagan 逐語は "dissenting" 帰属（Court/majority に帰属させない・C-4・R-QUOTE）。"we are all harmed" を1件も書かない。** **2006・docket・監視期間を `value`/`numKeys`/label に焼かない（R-HEDGE/R-NUM）。票決は 5-3・8名（6-3/8-3 を書かない・R-VOTE）。**

## 6.5 配置ルール
1. **AEの区間（§7.2）と1秒でも重ならない**（`validate_strieff_beats` が突き合わせ）
2. **同じ kind を連続させない**（`mechanism` の直後に `mechanism` を置かない・`quote` 3本を分散）
3. 1枠 **5.4–6.0秒**
4. `quote[].quote` / `kinetic[].lines` / `*.label` は §2 の R-NUM・R-QUOTE・R-FORBID・R-LEGAL・R-ATTEN・R-VOTE・R-FACE・R-DOCHL 検査対象
5. 台帳外の数値・`2006`・docket・監視期間を `value`/`numKeys`/`majority`/`dissent` に置かない（**焼いたら R-NUM/R-HEDGE で FAIL**）
6. **`emphasisWords` は1–2語の短句のみ**（長句は末尾切れ＝EP40 実害）
7. **`kind` に `dochighlight` を1件も置かない（R-DOCHL）**

---

# 7. After Effects カード（`build_strieff_hero_cards.py` / `composite_strieff_hero.py`）

## 7.1 位置づけ
AEカードは **film.json とは別**に ffmpeg で本編に焼き込む（§0.5-2＝密度に数えられない）。
`build_cleveland_hero_cards.py`（**FIXED版**）を**コピーしてパス・定数・DECK だけ差し替える**。レイアウト実装・`fit_size()`・`count_keys()`・**REPO path 出力**・**二段レンダ（JSXが.aep保存→呼び出し側が aerender）**・完了マーカー・機械の罠対処は**1行も削らない**。

## 7.2 AEカードデッキ（**単調増加・重複ゼロ・台帳裏付けのみ・6制約順守。この表が契約。8枚＝ブリーフ§6 VERBATIM**）

**区間の秒は本番の rendered base（narration_index 由来）に一致させる。** 下表の秒は spec タイムライン基準の**目安**で、`build_strieff_hero_cards.py` は section 窓からオフセットで算出しクランプする。**背景静止画は象徴オブジェのみ（R1/C-5・Strieff 顔なし）。**
**★この表は DESIGN §6 と id・レイアウト・S-ID・順序（start 昇順）が一字一致。**

| id | レイアウト（**実装済み6種の内・§7.3**） | hero/main（主表示） | top / bottom / left / right / attribution | S-ID | 背景（象徴のみ） | required |
|---|---|---|---|---|---|---|
| a01 | ACT_TITLE_CARD | **THE ILLEGAL STOP** | kicker: **UTAH v. STRIEFF** | S06 | 夜の駐車場・パトカーのライト（顔なし） | 必須 |
| c01 | CENTER_STACK (CT_TEXT) | **THE STOP WAS ILLEGAL** | top: **EVERYONE AGREED** / bottom: **THE STATE CONCEDED THERE WAS NO REASONABLE SUSPICION** | S03 | ID カードが手渡される手元（顔なし・violet-plum） | 必須 |
| a02 | CENTER_STACK (CT_TEXT) | **ATTENUATION** | top: **THE EXCEPTION TO THE RULE** / bottom: **THE WARRANT BROKE THE CHAIN — THE EVIDENCE STAYED** | S07/S08 | 断ち切られた鎖の一環（象徴） | 必須 |
| cmp01 | SPLIT_COMPARE | left: **AN ILLEGAL STOP** / right: **EVIDENCE ADMITTED** | top: **WHAT THE COURT ALLOWED** / bottom: **ONLY BECAUSE A WARRANT BROKE THE CHAIN** | S08 | 左=令状フラグ画面 / 右=小さな証拠袋 | 必須 |
| v01 | VOTE_SPLIT | **5 / 3** | top: **THE EVIDENCE STAYS** / bottom: **AN 8-JUSTICE COURT — SCALIA'S SEAT EMPTY** | S10 | 8席のベンチ・空席1（象徴・顔なし） | 必須 |
| q01 | QUOTE_CARD | **"IT IMPLIES THAT YOU ARE NOT A CITIZEN OF A DEMOCRACY BUT THE SUBJECT OF A CARCERAL STATE, JUST WAITING TO BE CATALOGED."** | attribution: **JUSTICE SOTOMAYOR, DISSENTING** | S13 | 記録の壁／ファイル棚（カタログ化の比喩・顔なし） | 必須 |
| q02 | QUOTE_CARD | **"THE OFFICER'S INCENTIVE TO VIOLATE THE CONSTITUTION THUS INCREASES."** | attribution: **JUSTICE KAGAN, DISSENTING** | S16 | 大理石の第4修正（判読困難・顔なし） | 必須 |
| d01 | CENTER_STACK (CT_TEXT) | **2016** | top: **DECIDED** / bottom: **UTAH v. STRIEFF — 579 U.S. 232** | S00 | 大理石の最高裁列柱（顔なし） | 必須 |

> **★行順＝start 昇順（時系列）:** `a01`(OP/ACT1) < `c01`(ACT1) < `a02`(ACT2) < `cmp01`(ACT2→3) < `v01`(ACT3 vote) < `q01`(ACT3 Sotomayor) < `q02`(ACT3 Kagan) < `d01`(ACT3→END date)。
> **★制約:** `c01` は "THE STOP WAS ILLEGAL / CONCEDED / NO REASONABLE SUSPICION" を削除禁止（**C-1 停止は違法・R-LEGAL**）。`a02`/`cmp01` は証拠許容の理由を**令状（chain broke）**に帰す（**C-2/C-3・R-ATTEN**・"exclusionary rule abolished" を書かない）。`v01`（5/3）は "AN 8-JUSTICE COURT — SCALIA'S SEAT EMPTY" を削除禁止（**C-4・8-3 と読ませない・R-VOTE**）。`q01`/`q02` の attribution は **"JUSTICE …, DISSENTING"**（Court/majority に帰属させない・**C-4・R-QUOTE**）・quote は §2 `APPROVED_QUOTES` の逐語のみ（要約を引用符に入れない）。
> **どのカードにも「the stop was legal」「exclusionary rule abolished」「we are all harmed」「6-3」を書かない**（C-1/C-2/C-4）。**2006・docket・監視期間を焼かない（R-HEDGE/R-NUM）。** 数値ID＝台帳（§2.2）と一致必須。カウント終了から区間終端まで最低 **1.20秒**ホールド（`count_type=CT_TEXT` は count-up 無しなので該当せず）。

**検算（Codex は自分で再計算して一致を確認）:** 8区間・単調増加・重複ゼロ・HOOK(0–65.7) と ENDCARD(末尾9s) に重ねない。Remotion figures(§6) と1秒も重ならない（`validate_strieff_beats`）。

## 7.3 レイアウト（`build_cleveland_hero_cards.py`（FIXED）の実装を踏襲・**実装済みレイアウト名だけを使う**）
複製元が実装するレイアウトは**この6種**（`buildActTitle`/`buildCenter`（=CENTER_STACK と MONEY_STACK 兼用）/`buildQuote`/`buildVote`/`buildCompare` の5関数）:
`ACT_TITLE_CARD` / `CENTER_STACK` / `MONEY_STACK` / `QUOTE_CARD` / `VOTE_SPLIT` / `SPLIT_COMPARE`。
**§7.2 デッキが使うのは 4種**（`ACT_TITLE_CARD` / `CENTER_STACK` / `VOTE_SPLIT` / `QUOTE_CARD` / `SPLIT_COMPARE`＝5種のうち MONEY_STACK 不使用）。
> **★EP49 は `VOTE_SPLIT` を使う**（5-3 は台帳 S10 で verified＝捏造でない）。**日付は `DATE_STAMP` レイアウトが複製元に無いので `CENTER_STACK`（CT_TEXT・hero="2016"）で表現する**（`d01`）。**`MONEY_STACK` は本 EP 未使用**（金額なし）。
**上記6種以外のレイアウト名を発明しない（`validate_strieff_beats` §7.9 ルール3 で FAIL）。`DATE_STAMP`/`SEAM_TRANSITION`/`dochighlight` をレイアウト名に使わない（複製元に非実装）。**
**共通レイヤースタック・Anton/Oswald・`psName()` の runtime 解決（`getFontsByFamilyNameAndStyleName` + allFonts の array-LIKE ラッパーを unwrap・miss は throw）は複製元と同一。**

**★共通レイヤースタックに AI開示レイヤーを1枚（R1・全カード常時焼き）:** 最上位に近い固定レイヤーとして
`AI-assisted visualization`（Oswald 20px / SILVER `#C8CDD6` / opacity 70% / 右下 `[W-32, H-28]`）を全カードに焼く（複製元が既に実装）。AEカードは不透明の全画面 mp4 として本編に overlay されるため、これが無いと本編(Remotion)右下の開示が隠れる（R1 違反）。字幕帯とは縦56px 以上離す。

**★EP49 色定数（0..1 float・somber-plum レーン色。EP41 gold / EP42 blue / EP43 amber / EP44 teal / EP45 crimson / EP46 green / EP47 violet / EP48 を流用禁止・DESIGN と一致）:**
```python
ACCENT = [0.612, 0.420, 0.667]  # #9C6BAA somber-plum（アクセント：数値・下線・レーン分離）
WHITE  = [0.961, 0.969, 0.980]  # #F5F7FA
SILVER = [0.784, 0.804, 0.839]  # #C8CDD6（開示テキスト）
INK    = [0.039, 0.039, 0.047]  # #0A0A0C 近黒ルート（サムネ bg と一致）
```
> **accent は必ず `#9C6BAA`（他話色を書かない）。** サムネ・OP props・AEカードの accent は全て `#9C6BAA`。**★複製元の `ACCENT=[0.698,0.227,0.282]`（EP45 crimson）を必ず `[0.612,0.420,0.667]` に置換する**（16進 #9C6BAA を 0..1 に正規化: 156/255=0.612, 107/255=0.420, 170/255=0.667）。

**数値・文字カードは全て `fit_size()`（Python 事前フィット）で表示文字列を計算し、JSX 側は `sourceRectAtTime(t,false).width` で実測再フィット**（advance-width 推定は禁止＝EP40 の文字切れ原因）。
**`v01`（5/3）は "5" と "3" を別レイヤーで、下段に "AN 8-JUSTICE COURT — SCALIA'S SEAT EMPTY"。`cmp01`（AN ILLEGAL STOP / EVIDENCE ADMITTED）は左右2値を別レイヤー（改行禁止）。`c01`/`a02`/`d01` は CENTER_STACK CT_TEXT（count-up 無し）。**

## 7.4 `beats.json` スキーマ（本番 `08_edit/ae_hero/beats.json`）
`build_cleveland_hero_cards.py` の beats スキーマ（`cleveland_ae_beats.v1`→`strieff_ae_beats.v1`）に準拠。トップに **`film_offset_sec`**（本編ナレ開始からのオフセット＝`round(hookSeconds(8.0)+OPENING_SEC(3.5),3)=11.5`・§7.10 のコンポジタが読む）。各 beat に `id` / `layout` / `count_type` / `start` / `end` / `dur` /
`still`(象徴 or null) / `hero`/`heroText`/`main`(主表示文字列) / `top` / `bottom` / `left` / `right` / `caption`(**改行禁止・最大50字**) /
`value`(数値カードのみ) / `numKeys` / `blend_mode`(既定 "overlay") / `required` / `out` / `attribution`(**QUOTE_CARD=q01/q02 は必須**・§2 `APPROVED_QUOTES` 一致・R-QUOTE)。
**`value` / `hero` / `left` / `right` の数値は §2 台帳の `verified:true` 値のみ**（`check_strieff_facts` が照合）。**`2006`・docket・監視期間を出さない。**
**`v01` は R-VOTE を満たす "5"/"3"＋"8-JUSTICE / SCALIA'S SEAT EMPTY"。`q01`/`q02` は "dissenting" 帰属。`c01` は "illegal/conceded"、`a02`/`cmp01` は "warrant broke the chain"。`beats.json` に `dochighlight`/"we are all harmed"/"6-3" を出さない。**
**★ledger gate（複製元と同一）: `beats` の全 `nums`（S-ID, 値）を `strieff_facts` で照合し verified:false は exit(1)。FORBIDDEN gate: §2.1 禁止語を全カード文字列で assert absent（build 時）。**

## 7.5 このマシン固有の罠（複製元＝FIXED版が対処済み。**1つも省くな**）
1. `setTemporalEaseAtKey` の配列次元は **spatial(Position) で 1**（`if(!prop.isSpatial){...}` で分岐）
2. RS = **`"最良設定"`** / OM = **`"H.264 - レンダリング設定を一致 - 15 Mbps"`**（英語名は try/catch フォールバックのみ）
3. TextDocument の改行は `\n` 不可。**`caption` は1行**（改行が要るなら別レイヤー・SPLIT_COMPARE の左右2値・VOTE_SPLIT の 5/3 は別レイヤー）。**テキスト幅は `sourceRectAtTime(t,false).width` で実測**（advance-width 推定は禁止＝EP40 の文字切れ原因）。em-dash は `-`
4. `app.newProject()` は headless でハング。**使わず**同名 `STRIEFF_`/`strieff_hero` コンプを防御削除
5. ビルドは**カード8枚で ~100–120秒**。`render/_build_ok.txt` をポーリング（**タイムアウト最低300秒**）
6. 起動はデタッチ + 出力ポーリング。jsx 末尾で **`.aep` を保存**し `app.quit()`
7. `comp.motionBlur=true` だけでは無効。**動かすレイヤー個別に `layer.motionBlur=true`**
8. 2Dレイヤー回転は **`"ADBE Rotate Z"`**（`"ADBE Rotation"` は null）
9. `inPoint` と `outPoint` の**両方**を設定
10. 読み込み後 `item.mainSource.conformFrameRate = 30`（忘れると全カードの timing がズレる）
11. 実行パス `C:\Program Files\Adobe\Adobe After Effects 2026\Support Files\AfterFX.exe`（実在確認済み）
12. `proj.gpuAccelType = GpuAccelType.SOFTWARE`（RTX4090 でもソフトレンダ固定・安定優先）
13. **`getFontsByFamilyNameAndStyleName` を使うフォント厳格解決**（miss は **throw**・フォールバック禁止／allFonts[i] ラッパー経由 unwrap）
14. **フォント文字列やラベルを PowerShell 経由の正規表現/エスケープで生成しない**（`\b` がバックスペース化した実害）。Python 側で literal に組む。**Python 先頭に `sys.stdout.reconfigure(encoding="utf-8")`**
15. **★二段レンダ（FIXED版の核）:** JSX は AfterFX `-noui -r` で開き、**`.aep` を保存**して `render/_build_ok.txt` を書くだけ（H.264 の OM を **exFAT の H: に書くと queue=N でも 0 mp4** になる実害＝**REPO path（C:）に出力**）。**mp4 の実レンダは別工程 `aerender`** で各コンプを個別に焼く。**aerender 前に `.aep` mtime > `.jsx` mtime を assert**（古い .aep を焼く事故防止＝EP39-41 実害・複製元が実装済み）。

## 7.6 実行（★二段）
```bash
# 段1: JSX 生成＋AfterFX で .aep 保存（mp4 はまだ焼かない）
$PY scripts/ae/build_strieff_hero_cards.py
"C:/Program Files/Adobe/Adobe After Effects 2026/Support Files/AfterFX.exe" -noui \
  -r ".../episodes/PD-2026-049-strieff/08_edit/ae_hero/strieff_hero.jsx"
# render/_build_ok.txt を待つ（最大300秒）→ .aep mtime > .jsx mtime を assert
# 段2: aerender で各カードを個別レンダ（8本揃うまで最大1200秒）
"C:/Program Files/Adobe/Adobe After Effects 2026/Support Files/aerender.exe" \
  -project ".../08_edit/ae_hero/strieff_hero.aep" -comp "a01" -output ".../render/a01.mp4"
#   … c01 / a02 / cmp01 / v01 / q01 / q02 / d01 も同様（複製元の render ループを踏襲）
$PY scripts/ae/composite_strieff_hero.py
```

## 7.9 `scripts/validate_strieff_beats.py`（BLOCKING）
1. `beats[].start` 昇順・区間非重複
2. 全 `start`/`end` が本編ナレ区間内（HOOK 0–65.7 と ENDCARD 末尾9s に重ねない）
3. `layout` が §7.3 の**実装済み6種**（`ACT_TITLE_CARD`/`CENTER_STACK`/`MONEY_STACK`/`QUOTE_CARD`/`VOTE_SPLIT`/`SPLIT_COMPARE`）のいずれか。**この6種以外（`DATE_STAMP`/`SEAM_TRANSITION`/`dochighlight` 等）は FAIL。** still が必要なレイアウトで null なら FAIL
4. `still` 非null は実在＋長辺 >=3840px
5. `hero`/`main`/`top`/`bottom`/`left`/`right`/`caption`/`value` が §2（R-FORBID/R-LEGAL/R-ATTEN/R-VOTE/R-NUM/R-QUOTE/R-FACE/R-DOCHL/R-DATE/R-HEDGE）を通る
6. `verified:false` の値を要求するカードは `required:false` で**除外**、`required:true` なら exit 1
7. **`strieff_film.json` の `figures[]`（§6）と AE の区間が1秒でも重ならない**
8. `caption` に改行が含まれない
9. **AI開示レイヤーの存在（R1）** — ビルダが全カード共通スタックに `AI-assisted visualization`（右下・§7.3）を焼く設定であることを静的に確認。無ければ FAIL。受入アイボール（§13.1）でも「AEカード表示中も右下の開示が見える」を確認
10. **`dochighlight`/`DOCHIGHLIGHT`・"we are all harmed"・"6-3" が beats/レイアウト名に1件も無い（R-DOCHL/R-QUOTE/R-VOTE）**
11. **`c01` に "ILLEGAL"＋"CONCEDED"（R-LEGAL）／`a02`・`cmp01` に "warrant"＋"chain"（R-ATTEN）／`v01` に "8-JUSTICE"＋"SCALIA'S SEAT EMPTY"（R-VOTE）／`q01`・`q02` の attribution が "Justice … , dissenting"（R-QUOTE）が有ること**

## 7.10 基底 mp4 とコンポジタ（`build_strieff_bgm_real.py` → `composite_strieff_hero.py`）
```
# 完成後の合成順（ブリーフ§5）: build_strieff_bgm_real.py（narration+BGM・OFF=11.5）→ composite_strieff_hero.py（AEカード焼込み・film_offset_sec 適用）
BASE = episodes/PD-2026-049-strieff/08_edit/strieff_final_bgm.v002.mp4     # build_strieff_bgm_real.py が生成
OUT  = episodes/PD-2026-049-strieff/08_edit/strieff_final_bgm.v003_ae.mp4  # composite_strieff_hero.py が生成
FFMPEG  = C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe
FFPROBE = C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffprobe.exe
W,H,FPS = 1920, 1080, 30
```
**`build_strieff_bgm_real.py` は EP43 `build_caniglia_bgm_real.py` の複製・定数 `OFF=11.5`（narration に対する BGM オフセット）に差し替える。**
**`composite_strieff_hero.py` は EP43 `composite_caniglia_hero.py` の複製・`beats.json` の `film_offset_sec`（=11.5）を読み各 beat 区間を本編尺にマップする。★beats は実発話（narration_index）に再アンカーされた `start/end` を使う。**
**SKIP4条件を1行も削らない:** ① `render/<id>.mp4` 不在 ② 解像度 != 1920x1080 ③ 実測尺 `< dur-0.3` ④ `film_offset_sec + beat.end > base_dur`。
SKIP された区間は元カットのまま残る（作品は壊れない）。**何枚 SKIP したかを stderr に必ず出す。**
ffmpeg は `overlay=0:0:eof_action=pass:enable='between(t,start,end)'`（`blend_mode` が screen/multiply の時のみ `blend`）。
**出力後 `probe_dur(OUT)` でベースとの尺差 <=0.5秒を確認。出荷済みは絶対に上書きしない（必ず `_v003_ae`）。**

---

# 8. 字幕の切断規則（`scripts/gen_captions_strieff.py`＝`gen_captions_cleveland.py` の複製）

## 8.1 原則
**文字数は「上限」であって「分割基準」ではない。** `gen_captions_cleveland.py` の `internal_split()` / `chunk_sentence()` を**そのままコピー**。
`from fix_caption_dangling import NO_DANGLE_END, wrap as safe_wrap`（**語リストを自前で書き直さない**）。

## 8.2 通すゲート `scripts/check_caption_breaks.py`（**閾値を緩めるの禁止**）
- **A. 行末の機能語** = 0件 / **B. 孤立キュー**（語数<3 で終端句読点・大文字始まりの両方を満たさない）= 0件 / **C. 句をまたぐ切断(hard)** = 0件。A/B/C いずれか1件で FAIL（実質ゼロ許容）

## 8.3 EP49 の入力と対応
- 入力は **narration_index の各チャンク文**（`--narr`）。**字幕テキストは台本本文と1:1対応**（§0.5-5）。台詞・別エピソード文の混入禁止。verbatim で使い構文境界で分割するだけ。**タイミングは narration_index の start/end に +11.5 を加えず**（字幕は narration 相対でよい・コンポジタ側で offset を持つ）。※本編 Remotion は narration を bookend 後に配置するため、字幕 start は film 内 narration 相対のままでよい（複製元と同一挙動）。
- `ABBR` に `U.S.` / `v.` / `Mr.` / `Ms.` / `No.` / `U.S.C.` を持つ（`Utah v. Strieff` の `v.`、`579 U.S. 232` の `U.S.` で文を切らない）。
- CPS <=27・最小表示 0.90秒。**Step で決めた境界を時間都合で動かさない。**
- **字幕にも R-FORBID 適用**（台本本文に主語付き断定の禁止語は無いので verbatim なら自然に通る。§2.1 注意：`legal`/`illegal`/`exclusionary rule` 単独を禁止語に足さない＝HOOK/ACT の「the stop was not legal」「fruit of the poisonous tree」を巻き込む）。

## 8.4 セルフテスト（`--selftest`・EP38 実害を回帰に）
`Utah v. Strieff` / `579 U.S. 232` で文が切れないこと、機能語で終わるキュー・孤立キューを作らないことを含む4ケースを実装し、**出力を `check_caption_breaks.py` に食わせて exit 0 まで自動確認。**

## 8.5 実行
```bash
$PY scripts/gen_captions_strieff.py --narr episodes/PD-2026-049-strieff/06_audio/narration_index.v001.json
$PY scripts/check_caption_breaks.py episodes/PD-2026-049-strieff/08_edit/captions.final.v001.srt
# → PASS が出るまで直す。ゲート側の閾値を緩めるのは禁止。
```

---

# 9. 5ゲートの実際の判定（**build 後に必ず全部通す・animation_mix を忘れるな**）

| ゲート | 実体 | 入力 | EP49 の通過根拠 |
|---|---|---|---|
| `check_asset_reuse.py <film.json>` | factory≤1 / motion≤2 / still≤2 / first-use≥0.70 | **film.json 位置引数** | §5.2: factory1.00 / motion2.00 / still1.19 / first-use **0.8584** |
| `check_motion_density.py --ep PD-2026-049-strieff` | film.json の graphics+figures+heroCuts のみ / density≥2.5・coverage≥0.25・variety≥3（**AND**） | **`--ep`** | §6.1: **3.08 / 30.8% / 15種**（AEカードは0本＝§0.5-2・beats≥31） |
| `check_animation_mix.py --ep PD-2026-049-strieff` | film.json の cuts を img=still/その他=footage 分類 / still-share≤0.45・motion-cov≥0.45 | **`--ep`** | §5.2[C]: still-share **0.4469(cut)/0.4205(frame)** / motion-cov **0.5531+** |
| `check_caption_breaks.py <srt>` | A/B/C 各0件 | **srt 位置引数** | §8 の構文境界生成器 |
| `check_script_length.py <script> --json` | 総語数 / wpm / narration_seconds | **script 位置引数** | 2,139語 / wpm178.1 / **720.6s** |

> **★ゲートの入力指定（ブリーフ§5）:** density/mix は **`--ep PD-2026-049-strieff`**。**`--json <film.json>` は出力パス（上書き事故）なので入力に使わない。** asset_reuse は film.json 位置引数、caption_breaks は srt 位置引数、script_length は script 位置引数。
> **`check_animation_mix` は `04_scenes/premium_beatsheet.v*.json` があればそれを優先する。** §5.6 の通り B の beatsheet は `strieff_beatsheet`（`premium_` 無し）なので**auto-detect されず film.json を測る。**
> **★still-share 0.4469 は cap 0.45 に余裕 0.31%（極薄）。build 出力を必ず `check_animation_mix` で確認し、超えたら still を1本 footage に置換して再build（still を増やさない）。**

---

# 10. OP バンパー `OpeningStrieff`（Remotion・fps60/1920x1080/180f）

## 10.1 二重OPを作らない
本編（`Ep49Strieff`）の OP は `Bookends.tsx` の `BrandOpening` のまま（`op_ed_bookends` ゲート・フォーク禁止）。
`OpeningStrieff` は**独立したタイトルバンパー成果物**（`out/strieff_opening.mp4`。Shorts/予告/SNS 用）。**本編に ffmpeg で焼き込まない。**

## 10.2 Composition 設定
| 項目 | 値 |
|---|---|
| `id` | `OpeningStrieff` |
| 解像度 / fps / duration | **1920×1080 / 60 / 180**（=3.0秒） |
| component | `remotion/src/compositions/OpeningStrieff.tsx` |

```tsx
import {OpeningStrieff, openingStrieffDurationInFrames} from './compositions/OpeningStrieff';
import strieffOpeningProps from '../props/strieff.json';
<Composition id="OpeningStrieff" component={OpeningStrieff}
  width={1920} height={1080} fps={60}
  durationInFrames={openingStrieffDurationInFrames(60)} defaultProps={strieffOpeningProps}/>
```

**依存:** `@remotion/motion-blur`（未導入時のみ `cd remotion && npm i @remotion/motion-blur`）。
**`remotion/remotion.config.ts`** は既に正典値（png / h264 libx264 / CRF16 / yuv420p / bt709 / aac 320k / 全コア並列 / angle）。**一致確認のみ・書き換えない。**

## 10.3 秒数ベースのタイムライン（fps=60・フレーム直書き禁止・全て `Math.round(fps*秒)`）

| 秒 | 起きること | 手法 |
|---|---|---|
| 0.00–0.40 | L1 グラデ背景 opacity 0→1・**同時に scale 1.08→1.00（`Easing.out(Easing.cubic)`）** | interpolate（opacity 単独禁止・scale と併用） |
| 0.10 | ロゴ（`hasLogo`）左上に spring・scale 0.4→1.0・opacity 0→1 | spring `damping:14,mass:0.9` |
| 0.15–0.25 | L2 グリッド reveal（opacity→0.18）＋ translateY 0→48px | spring `damping:200,mass:1` + `Easing.inOut(Easing.sin)` |
| 0.25 | L3 グロー（plum `#9C6BAA`）scale 0.6→1.15 / opacity 0→0.85 | spring `damping:18,mass:1.2`（併用） |
| 0.30–0.86 | L4 主役タイトルが1文字ずつ切れ上がり（overflow:hidden + translateY 110%→0）＋ opacity。スタッガー **2f/文字**。全体を `Trail(layers=6,lagInFrames=1.2,trailOpacity=0.45)` で包む | spring `damping:16,mass:1` |
| 0.55–1.15 | L2b **令状フラグの走査線（plum）**が中央から横に `scaleX 0→1`＋opacity 0→0.5（「データベースが令状に解決」モチーフ） | spring `damping:22,mass:1.1`・`transformOrigin:'center'`・**motionBlur** |
| 0.95–1.35 | L5a アクセント下線（plum）左から `scaleX 0→1` | spring `damping:16,mass:0.8`・`transformOrigin:'left center'` |
| 1.10–1.55 | L5b サブタイトル translateY 24→0 + opacity 0→1 | spring `damping:20,mass:1`（併用） |
| 1.55–3.00 | settle→ホールド。**完全静止フレーム無し・フェードアウトしない** | — |

> **等速線形を1箇所も使わない。opacity 単独の演出を1箇所も作らない**（全 opacity が translateY/scale/scaleX と対）。

## 10.4 props 型と値
```ts
export type OpeningStrieffProps = { title:string; subtitle:string; accent:string; hasLogo:boolean };
```
`remotion/props/strieff.json`: `{ "title":"THE WARRANT IN YOUR POCKET", "subtitle":"AN ILLEGAL STOP THE COURT LET COUNT", "accent":"#9C6BAA", "hasLogo":true }`
`remotion/props/strieff_short.json`: `{ "title":"THE WARRANT IN YOUR POCKET", "subtitle":"A STOP WITH NO REASON. NOW WHAT?", "accent":"#9C6BAA", "hasLogo":false }`
> `subtitle`/`title` も §2 の R-FORBID/R-LEGAL/R-FACE 検査対象。ルート背景は INK 近黒 `#0A0A0C`。
> **accent は EP41 gold / EP42 blue / EP43 amber / EP44 teal / EP45 crimson / EP46 green / EP47 violet を書かず plum `#9C6BAA`（レーン分離・他話色流用は BLOCKER）。**
> **「the stop was legal」「exclusionary rule abolished」を subtitle に書かない。** `AN ILLEGAL STOP THE COURT LET COUNT`（違法だが証拠は counts＝C-1/C-2）・疑問形 `A STOP WITH NO REASON. NOW WHAT?` は問題提起として可。

## 10.5 量産
```bash
cd remotion && npm run studio     # OpeningStrieff を 0→180f スクラブして §10.3 の各時刻を目視
npx remotion render OpeningStrieff out/strieff_opening.mp4 --props=./props/strieff.json
npx remotion render OpeningStrieff out/strieff_short_op.mp4 --props=./props/strieff_short.json
```

---

# 11. サムネ3案（`StrieffThumbnails.tsx`・`<Still>` 1280×720・Root に `Thumb-strieff-01..03`）

**共通要件:** 見出し全て大文字・4語以内・320pxで判読 / **実在人物の肖像禁止（R1・Edward Strieff の顔/身体を出さない・C-5）** / INK 黒 `#0A0A0C` bg + plum `#9C6BAA` /
背景は body 静止画のうち `also_thumb==true` の6枚（象徴オブジェのみ・C-5。**サムネ専用の分類は無い＝also_thumb フラグを読む**） / `thumbnail_visibility`（luma平均≥33＋コントラスト）を通す。目標CTR 6%+。3案は6枚から選ぶ。
**「the stop was legal」「exclusionary rule abolished」を出さない（R-FORBID/R-LEGAL）。2006・docket を出さない（R-HEDGE）。**

**★also_thumb 6枚（still 資産 ID 空間 S01..S85＝CODEX_A §4.3。A のマニフェストと**一字一致必須**の A↔B 契約点）:**
`S01` / `S07` / `S24` / `S41` / `S60` / `S85`。
> サムネ component は**マニフェストの `also_thumb` フラグを読んで**背景を選ぶ（scene id をハードコードしない）。**この6 ID は CODEX_A §4.3 と完全一致必須**（`check_strieff_asset_manifest` §3.3-12 が集合の一致を検査）。**CODEX_A が別集合なら B は自分の6 ID を書き換えず A に合わせる（A が producer）。**

- **T1「理由なき停止」（最推奨）:** 夜の駐車場・後ろ姿・パトカーのライト（象徴・顔なし・**S01/S07** 系）。文字 **`AN ILLEGAL STOP`**（2語）＋ **`THAT STILL COUNTS`**（下）。`COUNTS` を plum。**停止は違法・射程を過大化しない。**
- **T2「5-3」（数字勝負）:** 8席のベンチ・空席1を暗く落とし（**S41/S85** 系）、前面に **`5-3`**（大）＋ **`THE EVIDENCE STAYS`**（下）。数字は S10 の検証済み値のみ（**8-3 と書かない**）。
- **T3「令状ヒット」（尊厳）:** データベース行が令状フラグに解決する画面（**S24/S60** 系）。文字 **`THEY SEARCHED YOU ANYWAY`**（3語）。`ANYWAY` を plum。**「合法」に見せない。**

**A/Bタイトル候補（`09_package`・二人称・台本のとおり・★"合法"と書かない）:**
- **A:** `The Stop Was Illegal. They Searched You Anyway. The Court Said It Counts.`
- **B:** `A Cop Stops You for No Reason, Then Finds a Warrant. Now What?`
> ※「the stop was legal」「exclusionary rule abolished」系のタイトルは**禁止**（C-1/C-2・R-LEGAL）。

**固定コメント** `09_package/pinned_comment.v001.txt`（§2 の R-NUM/R-QUOTE/R-FORBID/R-LEGAL/R-ATTEN/R-VOTE 検査対象・台帳事実のみ）:
```
What this case actually decided - and what it did not.

WHAT IT DECIDED: In Utah v. Strieff (579 U.S. 232, 2016), the Supreme Court held
5-3 that when an officer makes an illegal stop, learns of a valid, pre-existing
arrest warrant, arrests on that warrant and searches, the evidence found is
admissible. The discovery of the warrant attenuated - broke - the connection
between the unlawful stop and the evidence. The stop was still illegal. Everyone
agreed on that. The evidence came in only because of the attenuation doctrine.

WHAT IT DID NOT DO: It did not make the stop legal, and it did not abolish the
exclusionary rule. It narrowed it, by treating a pre-existing warrant as an
intervening circumstance under the three Brown v. Illinois factors. Only eight
justices sat - Justice Scalia's seat was vacant. Justice Thomas wrote for the
majority. Justice Sotomayor and Justice Kagan dissented. Three votes, not five.

Sotomayor, in dissent, warned that this ruling tells everyone their body can be
subject to invasion while courts excuse the violation of their rights. Kagan, in
dissent, warned that it raises an officer's incentive to make stops the law does
not allow. A very large number of Americans have some kind of outstanding
warrant, often for something small. Know how the exclusionary rule and its
attenuation exception work before the afternoon you need them.
```
> **description.txt にも AI 開示行（`AI-assisted visualization`）を置く（R1）。** 数値は台帳（5-3 / 8 / 579 U.S. 232 / 2016）のみ・**2006/docket/監視期間を出さない**。**"we are all harmed" を書かない・"6-3" を書かない。**

---

# 12. 本編コンポジション登録（`remotion/src/Root.tsx`・`Ep47Atwater`/`Ep45Cleveland` の形を踏襲）
```tsx
import strieffFilm from './data/strieff_film.json';
<Composition id="Ep49Strieff" component={CaseFilm}
  durationInFrames={caseFilmDurationInFrames(strieffFilm as unknown as FilmData, BRAND.video.fps)}
  fps={BRAND.video.fps} width={BRAND.video.width} height={BRAND.video.height}
  defaultProps={{ data: strieffFilm as unknown as FilmData, seriesLabel: 'PRIME DOCUMENTARY',
    title: 'The Stop Was Illegal. They Searched You Anyway. The Court Said It Counts.',
    subtitle: 'An unlawful stop, a pre-existing warrant, and evidence the Court let stand 5-3. Not because the stop was legal, but because the warrant attenuated the chain.' }}/>
```
> **id は正確に `Ep49Strieff`（切り詰め・綴り違い・大文字化の誤記に注意）。** `caseFilmDurationInFrames` の 4項評価は **22233 frames**（§5.1.1・hookSeconds=8.0）。
> `strieffFilm` は `import strieffFilm from './data/strieff_film.json';`（EP45 の `clevelandFilm` に相当）。
> `remotion/src` に現在 `strieff` の文字列が無いこと（衝突しない）を確認してから追記。**追記後 `cd remotion && npx tsc --noEmit`（typecheck）で緑を確認。**
> `title`/`subtitle` も §2 検査対象（R-FORBID/R-LEGAL/R-ATTEN/R-VOTE/R-QUOTE）。**「the stop was legal」「exclusionary rule abolished」を書かない。**

---

# 13. 受入（自分で exit 0 を確認してから完了報告）
```bash
cd C:\Users\aab15\Documents\prime-documentary ; PY=./.venv/Scripts/python.exe

# 0. 語数（最優先・課金前に落とす）
$PY scripts/check_script_length.py episodes/PD-2026-049-strieff/03_script/script.en.v001.md --json   # 2,139語 / wpm178.1 / 720.6s

# 1. 事実性/6制約（EP49固有・正確性ゲートはこの1本・dochighlight/we-are-all-harmed/6-3 も検査）
$PY scripts/check_strieff_facts.py --json

# 2. 契約バリデータ
$PY scripts/validate_strieff_beats.py
$PY scripts/check_strieff_asset_manifest.py --assets episodes/PD-2026-049-strieff/05_visuals/asset_manifest.v001.json

# 3. ★5ゲート（animation_mix を忘れるな・入力は --ep / 位置引数を厳守）
$PY scripts/check_asset_reuse.py    remotion/src/data/strieff_film.json
$PY scripts/check_motion_density.py --ep PD-2026-049-strieff
$PY scripts/check_animation_mix.py  --ep PD-2026-049-strieff
$PY scripts/check_caption_breaks.py episodes/PD-2026-049-strieff/08_edit/captions.final.v001.srt

# 4. 水増し・レンダ前プリフライト
$PY scripts/check_padding.py --ep PD-2026-049-strieff --json
$PY scripts/preflight_render_gate.py --ep PD-2026-049-strieff

# 5. ★public_slim staging（EP45 空 public_slim 事故防止）→ 本編レンダ（slim public・並列4）→ BGM → AEカード合成
#    public/strieff → public_slim/strieff へ全メディア（img/factory/motion/audio/overlay + 各 <stem>_depth.png）をコピー
$PY scripts/stage_cleveland_assets.py --ep PD-2026-049-strieff 2>/dev/null || {
    mkdir -p remotion/public_slim/strieff
    cp -r remotion/public/strieff/{img,factory,motion,overlay,audio} remotion/public_slim/strieff/ 2>/dev/null
    cp remotion/public/strieff/narration.mp3 remotion/public_slim/strieff/ 2>/dev/null
}
#   ★strieff_film.json が参照する src と各 <stem>_depth.png が public_slim に全て在ることを確認してからレンダ（両ディレクトリで media 解決 0-missing）
cd remotion
npx remotion render Ep49Strieff out/strieff.mp4 --public-dir=public_slim --concurrency=4
cd ..
$PY scripts/build_strieff_bgm_real.py     # OFF=11.5
$PY scripts/ae/composite_strieff_hero.py

# 6. 本編最終受入（episode番号は★位置引数・--ep ではない）
$PY scripts/check_final_acceptance.py 49 \
  --render episodes/PD-2026-049-strieff/08_edit/strieff_final_bgm.v003_ae.mp4 --emit-receipt
```

| ゲート | EP49 目標値 |
|---|---|
| `check_script_length` | 総語数 **2,139** / `wpm 178.1` / narration **720.6s** |
| `check_asset_reuse` | factory≤1 / motion≤2 / still≤2 / first-use **0.8584**（floor0.70） |
| `check_motion_density` | density **3.08**/min / coverage **30.8%** / variety 15（floors 2.5 / 0.25 / 3・beats **≥31**） |
| `check_animation_mix` | still-share **0.4469(cut)/0.4205(frame)**（cap0.45・余裕極薄）/ motion-cov **0.5531+**（floor0.45） |
| `check_caption_breaks` | 行末機能語0 / 孤立キュー0 / hard split 0 |
| `check_strieff_facts` | violations = 0（台帳照合・停止違法・attenuation・5-3/Scalia空席8名・Sotomayor/Kagan 反対帰属・R-FORBID・R-DOCHL・R-QUOTE・R-VOTE・R-HEDGE・"we are all harmed"不在） |
| runtime band | 12.0–12.5分（narration 720.6s + hook8.0 + bookends・total **741.1s ≤ 750s**） |
| factory クリップ | ≥24本 → **93本** |
| image_resolution | 全静止画 長辺 ≥3840px |
| thumbnail | 3案 @1280×720 + selected luma≥33 |
| op_ed_bookends | `BrandOpening`/`BrandEndcard` を import（フォーク禁止） |

**全て exit 0 でなければ `package_ready` にしない。自己申告QCは無効。QC基準を書き換えて通すのは禁止。**

## 13.1 完成後の全編アイボール（**★FULL-RUNTIME 3回・1フレーム判定禁止＝EP39-41/EP39-41 実害**）
`strieff_final_bgm.v003_ae.mp4` を **0→末尾まで通しで3回実視聴**し、以下を確認してから完了報告:
- 紙芝居感が無い（still が連続していない・footage が体感で過半＝EP45 の直接死因を潰せているか）
- AEカード8枚が全て焼き込まれ数値が台帳と一致（「the stop was legal」「exclusionary rule abolished」がどこにも無い）
- **`c01`「THE STOP WAS ILLEGAL / EVERYONE AGREED / THE STATE CONCEDED ... NO REASONABLE SUSPICION」が読める（C-1 違法だと明言）**
- **`a02`/`cmp01`「ATTENUATION / THE WARRANT BROKE THE CHAIN / EVIDENCE ADMITTED」が読める（C-2/C-3 令状が鎖を断った・排除法則は廃止でなく狭められた）**
- **`v01`「5 / 3 / AN 8-JUSTICE COURT — SCALIA'S SEAT EMPTY」が読める（C-4・6-3/8-3 と読ませない）**
- **`q01`（Sotomayor 逐語）が "...THE SUBJECT OF A CARCERAL STATE, JUST WAITING TO BE CATALOGED / JUSTICE SOTOMAYOR, DISSENTING"（反対帰属・要約でない・C-4）**
- **`q02`（Kagan 逐語）が "THE OFFICER'S INCENTIVE TO VIOLATE THE CONSTITUTION THUS INCREASES / JUSTICE KAGAN, DISSENTING"（反対帰属・C-4）**
- **どこにも "we are all harmed"（逐語でない）が出ていない・"6-3" が出ていない（S15/R-VOTE）**
- Edward Strieff の顔・身体・肖像が無い（象徴＝玄関の扉/駐車場/後ろ姿/パトカーのライト/ID カード/無線/データベース→令状フラグ/手錠/小さな証拠袋/断ち切られた鎖/空席8席/天秤/列柱のみ・C-5）／**薬物が扇情化されていない**（メタンフェタミンは臨床言及のみ・量/使用の描写なし）
- **`dochighlight`（黒バー/box/underline）が1本も無い（figures/AE／R-DOCHL）**
- 生成ビジュアル表示中は `AI-assisted visualization` が右下に常時（**AEカード8枚の表示中も**開示が見える＝カード共通スタックに焼かれている・R1・§7.3/§7.9）
- accent が plum `#9C6BAA`（EP41 gold / EP42 blue / EP43 amber / EP44 teal / EP45 crimson / EP46 green / EP47 violet が紛れていない）
- 音ズレ・字幕ズレ・尺差（base と <=0.5s）が無い

---

# 14. 絶対にやらないこと
- **EP39 / … / EP48 のファイル・素材に触らない**（読み取りのみ可）。レーンを分離する。
- **スレッドAの所有ファイル（§0.2.1）に書かない**（`05_visuals/` `05_stock/` `remotion/public/strieff/` `H:\...\ai\strieff\`）。**B の provenance は `04_scenes/strieff_build_manifest.v001.json` に書く。**
- **設計書 / `EP49_strieff_CODEX_A_*` / PD-2026-039〜048 に触らない。**
- **課金ジョブを起動しない**（ElevenLabs TTS / 課金画像生成API / YouTube アップロード）。narration_index は実測版を消費するだけ。
- **公開済み・出荷済み mp4 を上書き・再レンダしない**（出力は必ず `_v003_ae`）。
- **台帳（§2）に無い数値を焼かない**（$580,000 の再発防止）。**★`2006`（停止年・medium）・docket 14-1373・監視期間は画面禁止（R-HEDGE）。5-3/8/2016/579 U.S. 232 のみ断定。**
- **`FigureSpec` の `kind` を推測で書かない**（§6.2 の実在小文字値のみ。大文字名は無言で消える。`comparebars` は非在→`compbars`・`VoteTally` は非在→`votetally`＝`{majority,dissent}`）。**★`dochighlight` を1本も使わない（R-DOCHL）。**
- **`--variants` という語を書かない**（1シーン1枚・バリエーション0＝ブリーフ§1。SDXL は A の領分で 1 固定）。
- **asset_manifest の `counts`/`role` enum/`overlay` 枚数を CODEX_A と食い違わせない**（`role` は `body`/`i2v_source`/`reject` の3値のみ・**`thumb`/`still_thumb` を作らない**・overlay=12・factory=93・also_thumb 6 ID を A と一致）。
- **★「the stop was legal」化しない・「exclusionary rule abolished」と言わない**（C-1/C-2・R-LEGAL＝停止は違法・排除法則は狭められただけ・証拠は attenuation でのみ入る）。**Sotomayor / Kagan 逐語を Court/majority に帰属させない**（C-4・R-QUOTE）。**票決は 5-3・Scalia空席で8名**（C-4・R-VOTE＝6-3/8-3 を書かない）。**"we are all harmed" を1件も引用しない**（S15）。**Edward Strieff の顔/肖像/身体を出さない・薬物を扇情化しない**（C-5・R-FACE）。
- **accent に他話色（gold/blue/amber/teal/crimson/green/violet）を使わない**（plum `#9C6BAA`＝`[0.612,0.420,0.667]` のみ）。
- **stub/dryrun/placeholder のコードパスを作らない**（このスレッドは実素材のみ・ブリーフ§7・grep 0）。**★`build_strieff_film.py` は manifest の `factory[]`(93)/`motion[]`(16) を `public_path` で全読込し、空なら exit 1（EP45 空配列＝紙芝居事故の直接防止）。**
- **★AEカードは二段レンダ（AfterFX が .aep 保存→別工程 aerender が mp4 を焼く）で REPO path(C:) 出力**（H: 直書きは queue>0 でも 0 mp4 になる実害）。**aerender 前に .aep mtime > .jsx mtime を assert。**
- **★render 前に `public_slim/strieff` へ全メディアを staging する**（EP45 は空 public_slim でレンダ素材欠落・§13-5・両ディレクトリで 0-missing）。
- **スペック数値（226 cuts / still85 / factory93 / motion16 / distinct194 / first-use0.8584 / still-share0.4469 / figures≥31→37 / 720.6s / 2,139語 / 48シーン / mean_shot3.19 / total741.1s≤750s / durationInFrames22233 / hookSeconds8.0）を変えない。**
- **composition id は `Ep49Strieff`（切り詰め・綴り違い注意）・typecheck 緑を確認。** **PowerShell 経由で正規表現/エスケープを生成しない**（`\b` バックスペース化の実害）。
