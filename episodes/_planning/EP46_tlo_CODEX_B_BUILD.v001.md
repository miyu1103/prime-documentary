# EP46 tlo — Codex スレッドB「実装」引き継ぎプロンプト v001

> **このファイルは単体で完結している。他のファイルを読まなくても着手できる。**
> 並行して走っていたスレッドA（素材生成）のファイル `EP46_tlo_CODEX_A_*.md` は**読まない**（Aは既に FROZEN・接続点は §3 のマニフェスト1ファイル）。
> 設計書 `EP46_tlo_DESIGN*.md` も**読まない**（必要な数値・AEデッキ・figures 配分はすべて本書に転記済み）。
> `EP46_tlo_PRODUCTION_SPEC.v001.json` の数値は本書に転記済み。**あなたはこれを書き換えない。**

```
あなたは Prime Documentary（YouTubeドキュメンタリーチャンネル）の制作エンジニアです。
リポジトリ: C:\Users\aab15\Documents\prime-documentary
Python:     C:\Users\aab15\Documents\prime-documentary\.venv\Scripts\python.exe
メディア:   H:\pd-media
担当:       EP46 / Episode ID: PD-2026-046-tlo / slug: tlo
Composition id（本編）: Ep46Tlo
```

**題材:** *New Jersey v. T.L.O.*, **469 U.S. 325 (1985)**（decided **1985-01-15**・docket 83-712）。公立高校のトイレで喫煙を見つかった **14歳の新入生（T.L.O.＝未成年・記録上はイニシャルのみ・R2）** のハンドバッグ捜索。
本作の主題は「**校門を越えても第4修正は生徒に付いてくる（適用される）**が、その基準は**令状不要・相当な理由(probable cause)不要＝合理的疑い(reasonable suspicion)へ引き下げられた**（消滅でなく引き下げ）」。判例核は**二段テスト**（①開始時に正当・②範囲が相当）と **6-3**（White 法廷意見）、そして**警察関与時はより高い基準があり得る（footnote 7 の留保）**。

> **★正確性6制約が全出力を律する（§2）。** 「生徒は無権利/第4修正は学校に適用されない」と書かない・「学校は令状なしで何でも/いつでも捜索できる」と過大化しない・「相当な理由(probable cause)が必要」と誤らせない（＝reasonable suspicion）・票決は **6-3**・White 法廷意見／Brennan・Marshall・Stevens が一部反対を**中立帰属**・**T.L.O.＝未成年の顔/肖像/実名を一切出さない**・薬物は臨床的最小限で非扇情・数値は台帳一致・**引用は White 逐語のみ（attribution "Justice White, for the Court"）**。**★`figures[].kind` に `dochighlight` を1件も入れない**（黒バー/box/underline がバグに見える＝3回指摘）。**概要欄は生徒の権利 explainer への1行＋AI開示。**

---

# 0. このスレッドの責務・境界・完了条件

## 0.1 このスレッド（B）の責務 — **コード律速。実装は全部書ける。**

| # | 作業 | 成果物 |
|---|---|---|
| B-1 | エピソードディレクトリと `manifest.json` | `episodes/PD-2026-046-tlo/**` |
| B-2 | 境界契約マニフェストの**消費側**バリデータ | `scripts/check_tlo_asset_manifest.py` |
| B-3 | 事実台帳 F-ID と 6制約ゲート（**EP46固有・BLOCKING**） | `scripts/check_tlo_facts.py` |
| B-4 | `tlo_film.json` ビルダ（**asset_manifest→cuts変換＋beatsheet生成／footage混在・実素材のみ**） | `scripts/build_tlo_film.py`（**`build_cleveland_film.py` を複製**） |
| B-5 | beats バリデータ（AEとRemotionの区間衝突検査＋ledger／6制約） | `scripts/validate_tlo_beats.py`（**`validate_cleveland_beats.py` を複製**） |
| B-6 | **構文境界で切る字幕生成器**（実測 narration_index から verbatim） | `scripts/gen_captions_tlo.py`（**`gen_captions_cleveland.py` を複製**） |
| B-7 | **After Effects カード**のビルダとコンポジタ | `scripts/ae/build_tlo_hero_cards.py`（**`build_cleveland_hero_cards.py` 複製**）／`scripts/ae/composite_tlo_hero.py`（**`composite_caniglia_hero.py` 複製**） |
| B-8 | 本編 BGM ミックス（AEカード合成の基底 mp4 を生成） | `scripts/build_tlo_bgm_real.py`（**`build_caniglia_bgm_real.py` を複製・OFF=11.5**） |
| B-9 | Remotion 本編コンポジション登録 `Ep46Tlo` | `remotion/src/Root.tsx` |
| B-10 | OP バンパー `OpeningTlo`（fps60/1920x1080/180f） | `remotion/src/compositions/OpeningTlo.tsx` |
| B-11 | サムネ3案 | `remotion/src/compositions/TloThumbnails.tsx` |
| B-12 | 本編レンダ→BGM→AEカード合成→全ゲート→**全編アイボール** | `episodes/PD-2026-046-tlo/08_edit/**` |

> **★このスレッドは「実素材のみ」（ブリーフ§7 / タスク指示）。stub/dryrun/placeholder のコードパスを作らない**（`grep -rniE 'stub|placeholder|dryrun' scripts/*tlo*.py` が 0）。A は FROZEN・narration_index は実測版が実在する前提で組む。**素材が来ていなければ止めて A/上流に差し戻す**（架空の黒スタブで緑にしない）。

## 0.2 もう一方のスレッド（A・FROZEN）との境界 — **接続点はただ1ファイル。**

```
episodes/PD-2026-046-tlo/05_visuals/asset_manifest.v001.json
   ↑ Aが生成（唯一の生産者・FROZEN）        ↓ Bが消費（唯一の消費者・検証者）
```

**Bはこのファイル以外のAの中間生成物を読まない。** このマニフェストは **A(producer)とB(consumer/validator)で counts / role enum / overlay枚数を1バイト単位で共有**する（§3）。

> **★1シーン1枚・バリエーション0（ブリーフ§1）の B 側での意味:** A は同一ショットの `_01/_02/_03` を**作らない**。
> したがってマニフェストの `stills[role="body"]` は **84本すべてが固有プロンプトの distinct**（`counts.still_body==84`）。
> A の `ai_prompts.v001.md` は **still 84行（S01..S84）＋i2v種 16行 = 総生成画像 100枚**。**still カット 100本という数字とは別物**（偶然どちらも 100）。
> B は編集上、still を **各最大2回**まで再使用してカット100本を組む（cap 2 の"再利用"であって"バリエーション"ではない）。**B は `--variants` という語をどのコマンド・ログにも書かない。**

### 0.2.1 ファイル所有権（これを破ると並行作業が壊れる）

| パス | 所有 | Bの権限 |
|---|---|---|
| `episodes/PD-2026-046-tlo/manifest.json` | **B** | 読み書き |
| `episodes/PD-2026-046-tlo/{00_topic,01_research,03_script,04_scenes,06_audio,08_edit,09_package,approvals,events}/**` | **B** | 読み書き |
| `remotion/src/**` `remotion/props/**` | **B** | 読み書き |
| `scripts/*tlo*.py` / `scripts/ae/*tlo*.py`（§0.3） | **B** | 新規作成 |
| **`episodes/PD-2026-046-tlo/05_visuals/**` `05_stock/**`** | **A** | **読み取りのみ。書くな** |
| **`H:\pd-media\assets\ai\tlo\**` / `ai_video\tlo\**`** | **A** | **読み取りのみ。書くな** |
| **`remotion/public/tlo/{img,factory,motion,overlay}/**`** | **A** | **読み取りのみ。書くな** |
| `EP46_tlo_DESIGN*.md` / `EP46_tlo_CODEX_A_*.md` | **設計/Aスレッド** | **触るな** |
| `EP46_tlo_PRODUCTION_SPEC.v001.json` / `EP46_tlo_script.en.v001.md` / `EP46_tlo_facts.v001.json` | **上流** | **読み取りのみ。書くな** |
| `episodes/PD-2026-039-*/**` … `PD-2026-045-*/**` / それらの素材 | **他エージェント** | **絶対に触るな（読み取りのみ可）** |

> **B は `remotion/public/tlo/` に書かない**（A の staging 済み本番素材）。B の provenance/beatsheet は `04_scenes/` に書く（§5.6）。**public_slim への staging コピー（§13-5）は B が作る新規ディレクトリで、`public/tlo` を痩せさせない。**

## 0.3 B が新規作成するスクリプト（これ以外を新規に作らない。既存を改変しない）

| パス | 役割 | 手本（**改変せず読んで複製→パス/定数だけ差し替え**・**実在確認済み**） |
|---|---|---|
| `scripts/check_tlo_asset_manifest.py` | §3.3 消費側バリデータ | `scripts/check_cleveland_asset_manifest.py` |
| `scripts/check_tlo_facts.py` | §2 6制約＋台帳（BLOCKING・**正確性ゲート名はこの1つに統一**） | **`scripts/check_cleveland_facts.py`** |
| `scripts/build_tlo_film.py` | §5 film.json＋provenance＋beatsheet＋SRT（**実素材のみ**） | **`scripts/build_cleveland_film.py`** |
| `scripts/validate_tlo_beats.py` | §7.9 不変条件 | **`scripts/validate_cleveland_beats.py`** |
| `scripts/gen_captions_tlo.py` | §8 構文境界字幕生成器 | **`scripts/gen_captions_cleveland.py`** |
| `scripts/ae/build_tlo_hero_cards.py` | §7 AEカードビルダ（**VOTE_SPLIT 実装を含む**） | **`scripts/ae/build_cleveland_hero_cards.py`** |
| `scripts/ae/composite_tlo_hero.py` | §7.10 コンポジタ（`beats.json` の `film_offset_sec` を読む） | **`scripts/ae/composite_caniglia_hero.py`**（EP43） |
| `scripts/build_tlo_bgm_real.py` | §7.10 基底 mp4（narration＋BGM ミックス・**OFF=11.5**） | **`scripts/build_caniglia_bgm_real.py`**（EP43） |

> **`build_tlo_film.py` の複製時に差し替える定数:** `ASSET_MAP`／`NARR`（narration_index 既定パス）／`FACTORY_SEL`／`SLUG="tlo"`／`EP="PD-2026-046-tlo"`／出力パス群。**ロジック（best-pick / tile_window / allocate / build_figures / build_captions）は1行も変えない。**
> **既存の `build_cleveland_film.py` / `gen_captions_cleveland.py` 等は触らない**（他エピソードが使用中）。EP46用に**新規コピー**する。
> **実在しないスクリプト名を書かない**（複製元は上表の実在ファイルのみ。`ls scripts/` `ls scripts/ae/` で確認済み）。

## 0.4 完了条件（実素材で、全て緑になったら「実装完了」）

```bash
cd C:\Users\aab15\Documents\prime-documentary
PY=./.venv/Scripts/python.exe

# [B-DONE-1] マニフェスト消費側バリデータ（A の FROZEN 本番マニフェスト相手に通ること）
$PY scripts/check_tlo_asset_manifest.py \
  --assets episodes/PD-2026-046-tlo/05_visuals/asset_manifest.v001.json

# [B-DONE-2] 字幕（実測 narration の実文から構文境界で生成）
$PY scripts/gen_captions_tlo.py \
  --narr episodes/PD-2026-046-tlo/06_audio/narration_index.v001.json
$PY scripts/check_caption_breaks.py \
  episodes/PD-2026-046-tlo/08_edit/captions.final.v001.srt

# [B-DONE-3] film.json を実マニフェストから組み立てる（footage 混在必須・dochighlight 不使用・factory92/motion16 全読込）
$PY scripts/build_tlo_film.py \
  --assets episodes/PD-2026-046-tlo/05_visuals/asset_manifest.v001.json \
  --narr   episodes/PD-2026-046-tlo/06_audio/narration_index.v001.json \
  --out    remotion/src/data/tlo_film.json

# [B-DONE-4] ★5ゲート全部（--ep 指定・animation_mix を絶対に忘れるな）
$PY scripts/check_asset_reuse.py     remotion/src/data/tlo_film.json
$PY scripts/check_motion_density.py  --ep PD-2026-046-tlo
$PY scripts/check_animation_mix.py   --ep PD-2026-046-tlo
$PY scripts/check_caption_breaks.py  episodes/PD-2026-046-tlo/08_edit/captions.final.v001.srt
$PY scripts/check_script_length.py   episodes/PD-2026-046-tlo/03_script/script.en.v001.md --json

# [B-DONE-5] 事実性/6制約（＋dochighlight 不使用・White 逐語 attribution）
$PY scripts/check_tlo_facts.py --json

# [B-DONE-6] beats 契約（AE区間 と Remotion figures[] が1秒も重ならない）
$PY scripts/validate_tlo_beats.py

# [B-DONE-7] AE カードをビルド＋レンダ＋コンポジット
$PY scripts/ae/build_tlo_hero_cards.py
"C:/Program Files/Adobe/Adobe After Effects 2026/Support Files/AfterFX.exe" -noui \
  -r "C:/Users/aab15/Documents/prime-documentary/episodes/PD-2026-046-tlo/08_edit/ae_hero/tlo_hero.jsx"
$PY scripts/ae/composite_tlo_hero.py

# [B-DONE-8] Remotion Studio で目視
cd remotion && npm run studio
#   → Ep46Tlo / OpeningTlo / Thumb-tlo-01..03 が出て、実際に動くこと
```

**台本は既に確定済み**（`EP46_tlo_script.en.v001.md`・**2,125語・11.9分**・ロック・3チェック済）。本番配置先は
`episodes/PD-2026-046-tlo/03_script/script.en.v001.md`（**1バイトも変えずコピー**・整形禁止＝AI臭再発と語数ゲート再計算を招く）。

---

# 1. 実装前に必ず読むファイル（**推測で書くな**）

| パス | なぜ読むか |
|---|---|
| `scripts/build_cleveland_film.py` | **複製元。** best-pick / tile_window / allocate / build_figures / build_captions をそのまま踏襲し、定数だけ tlo に。**footage を必ず混ぜる（§0.5 の紙芝居回避）。★`asset_manifest` の `factory`(92) と `motion`(16) 配列を `public_path` で全読込する経路を確認**（EP45 でこの2配列が空で build 失敗した） |
| `scripts/ae/build_cleveland_hero_cards.py` | **複製元。** `money_keys()`（Python で表示文字列を全事前計算）/ `fit_size()` / CARDS デッキ構造 / **VOTE_SPLIT を含む8レイアウト実装** / AI開示レイヤー / 完了マーカーをそのまま |
| `scripts/ae/composite_caniglia_hero.py` | **複製元（EP43）。** SKIP4条件（missing / 解像度不一致 / 実測尺不足 / window past end）と ffmpeg フィルタグラフ（overlay/blend）と `film_offset_sec` の読み込みをそのまま |
| `scripts/gen_captions_cleveland.py` | **複製元。** `internal_split()` / `chunk_sentence()` / `NO_DANGLE_END` import をそのまま |
| `scripts/build_caniglia_bgm_real.py` | **複製元（EP43）。** narration＋BGM ミックスで基底 mp4 を作る経路・**`OFF = 8.0 + 3.5 = 11.5`**（hookSeconds + OPENING_SEC）を踏襲 |
| `remotion/src/compositions/CaseFilm.tsx` | `FilmData` 型 / `caseFilmDurationInFrames`（**4項＝round(hookSeconds*fps)+round(OPENING_SEC*fps)+ceil(narrationSeconds*fps)+round(ENDCARD_SEC*fps)**）/ `depthSrcOf()` |
| `remotion/src/components/FigureBeats.tsx` | `FigureSpec` の**実在する `kind` 文字列**（§6.2・**全小文字**・`votetally` は在・**`dochighlight` は使わない**） |
| `remotion/src/components/Bookends.tsx` | `OPENING_SEC=3.5` / `ENDCARD_SEC=9` / `BrandOpening` / `BrandEndcard` |
| `scripts/check_asset_reuse.py` / `scripts/check_motion_density.py` / `scripts/check_animation_mix.py` / `scripts/check_caption_breaks.py` / `scripts/check_script_length.py` | 通すべき5ゲートの**実際の判定ロジック**（§9） |
| `C:\Users\aab15\Documents\pino-channel\remotion\src\Opening.tsx` | §10 の OP 正典実装 |

---

# 0.5 ★★★ EP39–45 で踏んだ失敗＝最初から防ぐ（本書の全体設計はこの7点を構造で潰している）★★★

1. **紙芝居（最重要）** — 静止画100%で組むと `check_animation_mix` が FAIL する。**EP46 は最初から footage を混ぜる。**
   `check_animation_mix.compute_metrics_from_film()` は film.json の `cuts[]` を
   **`kind=="img"` → still（scene 扱い）/ それ以外 → footage（motion 扱い）** と分類する。
   → §5 の cuts 構成は **factory 92 + motion 32 の footage を最初から入れて still-share を cut数ベース 0.4464・frame ベース ~0.42** にする。
2. **AEカードは密度に数えられない** — `check_motion_density` は film.json の `graphics+figures+heroCuts` **のみ**数える。
   AEカードは ffmpeg で後合成するので**1本も数えられない**。→ §6 で **film.json 側の `figures[]` を 36本**（spec floor 30 に **+6**・`graphics[]=[]`）置く。AEカードは別勘定（§7・7枚）。
3. **FigureSpec の `kind` は実在の小文字値のみ** — 大文字名（`ActTitle`/`QuoteCard`/`VoteTally` 等）は無言で描画が消える（§6.2）。`comparebars` は非在→`compbars`。**★`dochighlight` を1本も使わない**（§6.2・R-DOCHL）。
4. **台帳に無い数値を焼くな** — EP40 の生 Codex-B 出力に架空の金額が入って**不採用になった実害**。
   → §2 の事実台帳 F-ID に**検証済み値だけ**を置き、`check_tlo_facts.py` が film.json/AE/サムネ/props の全数値を台帳照合する（**R-NUM は narrative figure のみ・§2.2 の許可集合**）。台帳に無い数値・`verified:false` の数値を焼いたら FAIL。
5. **字幕は台本本文と対応** — EP38 で台詞混入・「final」誤称の実害。→ §8 の字幕は **narration_index の実チャンク文をそのまま** verbatim で使う（自作しない）。
6. **レンダー前ゲート** — build 後に `check_asset_reuse` / `check_motion_density` / `check_animation_mix` / `check_caption_breaks` / `check_script_length` を**全部**通す（§9・§13）。**animation_mix を忘れるな。**
7. **★public_slim を staging し忘れるな（EP45 の render 不能事故）** — レンダは `--public-dir=public_slim`。**`public/tlo` の全メディア（img/factory/motion/audio）を `public_slim/tlo` へコピーしてから**レンダする（§13-5）。空の public_slim で走らせると素材が解決できず落ちる。

---

# 2. ★ EP46固有の正確性6制約・事実性ロック（`scripts/check_tlo_facts.py`・BLOCKING）

> **この節に違反した成果物は、他が全て完璧でも出荷不可。** 検査対象は film.json の figures/captions、AE beats、サムネ、props、固定コメント、`03_script/script.en.v001.md`、（存在すれば）マニフェストの tags/caption_hint/qc.notes の**全文字列と全数値**。
> **正確性ゲートはこの1本に統一（`check_tlo_facts.py`）。** 出力 `09_package/facts_lock.v001.json`。**`build_tlo_facts.v1` の台帳は `EP46_tlo_facts.v001.json`（F01–F17）から B が転記して作る**（`03_script/tlo_facts.v001.json`）。

## 2.1 正確性6制約（全出力に適用・違反は BLOCKER）

| # | 制約 | 許可される表現 | 禁止 |
|---|---|---|---|
| C-1 | **生徒は無権利ではない（引き下げであって消滅でない）** | 「the Fourth Amendment applies in school」「students do not shed their rights at the schoolhouse door」「a lowered standard, not no standard」「not no rights, not full rights」。`no warrant`/`no probable cause` を出すカードは**「4A は適用される」枠を同一カードに併記** | 「students have no rights」「the Fourth Amendment does not apply in school」「schools can search anything」「search any student at any time」 |
| C-2 | **二段テストを正確に** | inception（正当な開始）＋scope（相当な範囲）を両方。「reasonable grounds … the search will turn up evidence …」逐語 | 「search anything they want」「one prong」「no limit on the search」 |
| C-3 | **基準は reasonable suspicion（probable cause 不要）** | 「no warrant, no probable cause」「reasonable suspicion」「a standard lower than probable cause」 | 「probable cause is required」「requires probable cause」「reasonable suspicion is not enough」 |
| C-4 | **票決 6-3・White 法廷意見・中立帰属** | 「6-3」「Justice White wrote for the majority」「Brennan, Marshall, and Stevens concurred in part and dissented in part」 | 「5-4」「7-2」「9-0」「unanimous」「dissent by O'Connor」等の取り違え |
| C-5 | **T.L.O.＝未成年・象徴のみ・薬物非扇情** | 「a 14-year-old freshman」「her initials, T.L.O.」象徴（トイレ扉・机の上のバッグ・タバコ・巻紙・ロッカー・天秤・列柱）。押収物は臨床的に一列（美化しない） | 顔・肖像・実名・人物化／`T.L.O.` 直後60字の `face`/`portrait`/`likeness`／薬物の扇情・美化 |
| C-6 | **警察関与時はより高い基準があり得る（footnote 7 の留保）** | 「this case is about school officials」「when police are involved, a higher standard can return」「reserved in footnote 7」 | 「the same rule lets police search you」「police need only reasonable suspicion in school」 |
| R1 | **実在人物の顔・肖像を生成しない** | 全生成ビジュアル表示中は `AI-assisted visualization`（右下）常時／概要欄1行AI開示 | 認識可能な人物・読める偽公文書 |
| ★DH | **dochighlight 不使用** | 判読ハイライトの意図は `quote`/`stat`/`lowerthird`/`kinetic` で代替 | `figures[].kind`/beats/レイアウト名に `dochighlight`/`DOCHIGHLIGHT` を1件でも出す |

**★禁止語（`check_tlo_facts.py` が全文字列を case-insensitive 部分一致で検査。1件でも FAIL）:**
`students have no rights` / `students have no fourth amendment rights` / `the fourth amendment does not apply in school` / `schools can search anything` / `search anything they want` / `search any student at any time` / `students lose their rights at the schoolhouse door` /
`probable cause is required` / `requires probable cause` / `schools need probable cause` / `reasonable suspicion is not enough` /
`5-4` / `7-2` / `9-0` / `unanimous` / `unanimously` /
`portrait of t.l.o.` / `her face` / `the girl's face` / `glamorize`。

> **★★★重要な設計注意（EP45 の教訓）:** 台本本文（＝字幕 verbatim）は、**最高裁が退けた2つの極論を"仮定"として声に出す**。したがって字幕には
> `did not apply to them at all` / `carry no privacy` / `empty any student's bag, on any day, for no reason at all` / `students leave their rights at the door`（＝Court が**否定**した文）/ `students simply have no privacy is wrong` / `rights-free zone` /
> `does not need a warrant, and does not need probable cause` / `the police need before they search` / `Not no rights. Not full rights.` / `search you on a whim` / `your school owns you`
> **といった過大化語の"否定形/仮定形/正確文脈"が含まれる。上の禁止語リストは、それらと衝突しない断定形だけを厳選してある。禁止語リストにこれらの近似語を足すな**（字幕 verbatim を巻き込んで false FAIL する）。C-1/C-2/C-3/C-6 の**枠付き/限定の別**は下の**文脈ルール**（R-OVERCLAIM/R-STANDARD/R-VOTE/R-POLICE）で捕える。

## 2.2 事実台帳 F-ID（`03_script/tlo_facts.v001.json`・**B が `EP46_tlo_facts.v001.json`(F01–F17) から転記**）

**スキーマ版:** `tlo_facts.v1`。各 F-ID は `{"value":..., "unit":..., "verified":bool, "confidence":"high|medium", "claim_id":"", "attribution":"", "quote":""}`。
**裏付けのある値だけ `verified:true`。medium（F16 副校長名 Choplick／F17 校名 Piscataway）は `verified:true` だが `screen:false`＝画面に出さない（ヘッジ）。**

| F-ID | 内容 | 使う場所 | conf |
|---|---|---|---|
| F01 | 判例引用 = **New Jersey v. T.L.O., 469 U.S. 325 (1985)**・decided **1985-01-15**・docket 83-712 | fig lowerthird/timeline / AE d01 | high |
| F02 | 主体 = **14歳の新入生**・記録上は**イニシャル T.L.O. のみ**（R2・象徴のみ・顔/実名なし） | fig lowerthird/kinetic | high |
| F03 | 教師が女子トイレで**2名の喫煙**を発見→校則違反→front office | fig timeline/routemap | high |
| F04 | T.L.O. は喫煙を否認（「そもそも吸わない」） | fig kinetic（本文脈のみ） | high |
| F05 | 副校長がバッグを開ける→**タバコ**→取り出す際に**巻紙(rolling papers)を視認**＝捜索継続の hinge | fig mechanism/routemap | high |
| F06 | 更なる捜索で **marijuana・パイプ・空袋・$1札束・債務者名簿・売買を示す2通の手紙**（AD-SAFE＝事実提示のみ・非扇情） | fig routemap/bar（臨床的） | high |
| F07 | 手続: 少年審判で**証拠排除申立→却下→delinquent 認定（1年保護観察・1982-01-08）**。NJ最高裁は排除→米最高裁が **NJ最高裁を破棄** | fig timeline | high |
| F08 | 争点 = **公立学校職員の捜索に第4修正が適用されるか・その基準は何か** | fig lowerthird/acttitle | high |
| F09 | **HOLDING(1): 第4修正は公立学校職員に適用**（州の代理人）。生徒は校門で権利を失わない（★制約1） | fig kinetic/lowerthird / AE v01,n01 | high |
| F10 | **HOLDING(2): 令状不要・probable cause 不要、基準は reasonableness ＝ reasonable suspicion**（★引き下げであって消滅でない・制約3） | fig compbars/stat / AE n01,c01 | high |
| F11 | **二段テスト逐語**（White 執筆）: ①inception「reasonable grounds for suspecting that the search will turn up evidence that the student has violated or is violating either the law or the rules of the school」②scope「reasonably related in scope … reasonably related to the objectives of the search and not excessively intrusive in light of the age and sex of the student and the nature of the infraction」 | fig quote / AE t01,q01 | high |
| F12 | 本件 purse 捜索は**両 prong を満たし reasonable**（各段階が前段の発見に結び付く） | fig mechanism/routemap | high |
| F13 | **票決 6-3**（NJ最高裁を破棄し捜索を reasonable と判断） | fig votetally / AE v01 | high |
| F14 | ラインナップ = **WHITE 法廷意見**／**Brennan・Marshall・Stevens が一部反対**（基準引下げ／本件適用に反対）・中立帰属 | fig quote/lowerthird / AE q01 | high |
| F15 | **footnote 7 の留保** = 法執行機関が関与/主導する場合はより高い基準があり得る（本件は公立学校職員限定・★制約3/C-6） | fig lowerthird/kinetic / AE p01 | high |
| F16 | 捜索者 = **副校長（役職のみ）**（記録上 Theodore Choplick・`screen:false`） | — | medium |
| F17 | 舞台 = **NJ 公立高校**（Piscataway・`screen:false`・校名は非 load-bearing） | fig pindropmap（"New Jersey" のみ） | medium |

> **数値の許可集合（R-NUM・narrative figures のみ）:** `469 / 325 / 1985 / 1984 / 1982 / 15(Jan 15) / 8(Jan 8) / 6 / 3 / 14 / 2(two-part) / 7(footnote 7) / 1(one year)`。**これ以外の年・件数・巻/頁が画面(figures/AE/サムネ)に出たら FAIL。**
> **★R-NUM/構造ルールは narrative figure のみ対象（EP45 の誤検出修正）:** `asset_manifest` の構造カウント（`84/100/92/16/32/12/224`）と `acttitle` の `index`（1/2/3）は**除外**する。

## 2.3 `check_tlo_facts.py` の検査（exit 0=PASS / 1=FAIL / 2=スキーマ不一致）

**検査対象ファイル（この一覧をハードコード。存在するものだけ検査し、無いものは `skipped[]` に必ず明記）:**

```
episodes/PD-2026-046-tlo/03_script/script.en.v001.md
episodes/PD-2026-046-tlo/03_script/tlo_facts.v*.json
episodes/PD-2026-046-tlo/08_edit/ae_hero/beats.json
episodes/PD-2026-046-tlo/09_package/*.json        （title / description / thumbnail headlines）
episodes/PD-2026-046-tlo/09_package/*.txt         （固定コメント・description.txt）
episodes/PD-2026-046-tlo/05_visuals/asset_manifest*.json  （tags / caption_hint / qc.notes）
remotion/src/data/tlo_film.json                   （figures[].text / figures[].lines[] / figures[].kind / captions[] の全文字列と数値）
remotion/props/tlo*.json                          （title / subtitle）
```

- **R-FORBID（最優先）** — §2.1 の禁止語が対象文字列のどこかに出たら即 FAIL。**近似語（否定/仮定/正確文脈）を巻き込まない断定形のみ**を検査（§2.1 の★注意）。
- **R-OVERCLAIM（C-1・BLOCKING）** — `no warrant`/`no probable cause` を含むカード/figure に「4A は適用される」枠（`applies`/`schoolhouse door`/`do not shed`/`still applies`/`not no rights`）が同一 payload に無ければ FAIL。「students have no rights」「search anything」系の断定が出たら FAIL。**`description.txt` に生徒の権利 explainer への1行が無ければ FAIL（R1連結）。**
- **R-STANDARD（C-3・BLOCKING）** — 学校捜索の基準に触れる payload（`reasonable suspicion`/`probable cause`/`warrant` を含む）は「lowered, not eliminated」に射程限定：`probable cause` を**要求**する断定（`probable cause is required`/`requires probable cause`/`schools need probable cause`）が出たら FAIL。`reasonable suspicion is not enough` も FAIL。基準カードは `reasonable suspicion` と `no probable cause`（引き下げ枠）を同伴すること。
- **R-VOTE（C-4・BLOCKING）** — 票決に触れる payload は **`6-3`（または `6 – 3`/`six to three`）** のみ許可。`5-4`/`7-2`/`9-0`/`unanimous` が出たら FAIL。多数=White、一部反対=Brennan/Marshall/Stevens 以外の帰属が票決文脈に出たら FAIL。
- **R-QUOTE / R-ATTRIB（C-2・BLOCKING）** — `quote[].attribution` は非空・逐語のみ（要約を引用符に入れない）。**引用は White 逐語のみ許可**。許可対応表:
  ```python
  APPROVED_QUOTES = {
    "reasonable grounds for suspecting that the search will turn up evidence that the student has violated or is violating either the law or the rules of the school":
        "Justice White, for the Court",   # F11 prong-1 (inception)
    "reasonably related in scope to the circumstances which justified the interference in the first place":
        "Justice White, for the Court",   # F11 prong-2 (scope, twofold-inquiry 節)
    "reasonably related to the objectives of the search and not excessively intrusive in light of the age and sex of the student and the nature of the infraction":
        "Justice White, for the Court",   # F11 prong-2 (scope, 詳細節)
  }
  ```
  引用符付きテキストが上表キーに完全一致しない、または attribution が `Justice White, for the Court` でなければ FAIL（White 以外の帰属を引用に付けない）。
- **R-POLICE（C-6）** — footnote 7 に触れる payload（`police`/`law enforcement`/`footnote 7`）は「higher standard can return / school officials only」を同伴。`police need only reasonable suspicion`/`the same rule lets police search you` 系が出たら FAIL。
- **R-MINOR / R-FACE（C-5・R1）** — `has_readable_text`/`has_identifiable_face`/`has_human_body` が true の項目は `role=="reject"`。`ai_prompts.v001.md` 正プロンプトの `portrait`/`face of`/`likeness`/`T.L.O.`（人物として）/`the girl`/`her body`/`crying`/`14-year-old girl shown` は FAIL（ネガティブでの使用は可）。`T.L.O.` 直後60字の `face`/`portrait`/`depicted as a girl`、薬物扇情語（`glamorize`/`drug haul glorified`/`cool drugs`）で FAIL。生成ビジュアル区間の `AI-assisted visualization` 欠落・`description.txt` の AI 開示行欠落で FAIL。
- **R-NUM（R-LEDGER）** — figures[] の `value`/`numKeys` 到達値、AE `beats[].value`/`beats[].main`/`beats[].hero`、サムネ数字に現れる**あらゆる数値**は §2.2 の許可集合に**完全一致**必須。**★narrative figure のみ対象＝manifest 構造カウント・acttitle index は除外。**
- **R-DOCHL（★DH・BLOCKING）** — `tlo_film.json` の `figures[].kind` に `dochighlight` が1件でも出たら FAIL（`grep -c '"kind"[[:space:]]*:[[:space:]]*"dochighlight"'` が 0 でなければ FAIL）。`beats.json`/レイアウト名にも `dochighlight`/`DOCHIGHLIGHT` を出さない。
- **R-DATE** — F01(1985-01-15) と F07(1982-01-08 delinquent) / F01(1984 argued/reargued) の日付・年が別カードで取り違えられていないこと（`1985`＝decided、`1984`＝argued/reargued、`1982`＝probation）。

**出力:** `episodes/PD-2026-046-tlo/09_package/facts_lock.v001.json`（`{"pass":bool,"violations":[{"file","rule","line","excerpt"}],"skipped":[...]}`）。
**`pass:true` でない限り `check_final_acceptance.py` に進んではならない。** CLI: `--json`。対象ファイルが未生成ならスキップして必ずログに出す。「無いから通した」を黙るな。

---

# 3. ★境界契約: `asset_manifest.v001.json`（Aから受け取る唯一のファイル・FROZEN）

## 3.1 スキーマ（**Aが生成する。Bはこの形を前提に読む・A↔B 1バイト一致**）

**スキーマ版:** `tlo_assets.v1`（固定文字列。異なれば **exit 2**）。
EP46 spec の点数に一致: **still_body 84 / still_i2v_source 16 / motion 16 / factory 92 / overlay 12**。
**★サムネは独立の分類を持たない。** body 84枚のうち**6枚**に `also_thumb:true` を立てて流用する（**`role=thumb`/`still_thumb` を作らない**・§11）。
**このスキーマ・`counts` キー・`role` enum・`overlay` 枚数は CODEX_A（生産者）の `build_tlo_asset_manifest.py` の出力と1バイト単位で同一。**

- **`role` enum（固定・3値のみ）:** `"body"` | `"i2v_source"` | `"reject"`。**`thumb`/`still_thumb` を作らない。**
- **`counts`（固定キー・確定値）:** `{ "still_body": 84, "still_i2v_source": 16, "motion": 16, "factory": 92, "overlay": 12 }`。
- 配列: `stills[]`（body 84＋i2v_source 16）・**`motion[]` 16（`public_path` 必須）**・**`factory[]` 92（`public_path` 必須）**・`overlay[]` 12。
  `stills[role="body"].public_path = "tlo/img/S01.png"`（1シーン1枚）／`depth_path` 実在必須。
  `motion[].public_path = "tlo/motion/M01_rife.mp4"`（`.mp4` かつ `_rife` を含む）。
  `factory[].public_path = "tlo/factory/AF-BG-xxxx__desc.mp4"`（`/factory/` を含む）。
  `overlay[].public_path = "tlo/overlay/..."`（`/overlay/` を含み `/factory/` を含まない）。accent 記述は green 系。

> **★★★ EP45 の build 失敗の核心を繰り返さない:** `build_tlo_film.py` は **`asset_manifest` の `factory`(92) と `motion`(16) 配列を `public_path` で全エントリ読み込む**。この2配列が空/欠落だと footage が入らず紙芝居→`check_animation_mix` FAIL、または cuts が組めず build が落ちる。**マニフェスト受領直後に `len(factory)==92` と `len(motion)==16` を assert し、各要素の `public_path` が `remotion/public/<path>` に実在することを確認**してから cuts を組む（§3.3-6/7）。

## 3.2 Bがこのマニフェストから作るもの（**EP46 spec の cuts 割当**）

| マニフェスト | Bでの使い道 | spec |
|---|---|---|
| `stills[role="body"]` 84枚 | **静止画カット100本**（`kind:"img"`, `treatment` 循環）・**各≤2回** | still distinct84/cuts100 |
| body 静止画で `also_thumb==true` の6枚 | サムネ3案の背景（§11） | — |
| `stills[role="i2v_source"]` 16枚 | **本編カットに出さない**（i2v 種・A が Wan で motion 化済み） | — |
| `motion` 16本 | **i2vカット32本**（`kind:"footage"`）・**各≤2回** | motion distinct16/cuts32 |
| `factory` 92本 | **実写カット92本**（`kind:"footage"`）・**各1回のみ** | factory distinct92/cuts92 |
| `overlay` 12本 | **`cuts[].src` に出さない**（§5.5 の合成レイヤー扱い） | — |

**合計 100 + 32 + 92 = 224 カット / distinct 84+16+92 = 192 / first-use 192/224 = 0.8571 ✓（floor 0.70）**

## 3.3 `scripts/check_tlo_asset_manifest.py`（消費側バリデータ・BLOCKING）

```bash
$PY scripts/check_tlo_asset_manifest.py --assets <path> [--json]
```

検査（1つでも違反で exit 1。`schema_version` 違いだけ exit 2・**A の `--verify` 不変条件と一字一致**）:

1. `schema_version=="tlo_assets.v1"` / `episode_id=="PD-2026-046-tlo"` / `slug=="tlo"` / `is_stub==false`
2. `counts.*` が各配列の実長と一致し**確定値**: `still_body==84` / `still_i2v_source==16` / `motion==16` / `factory==92` / `overlay==12`
3. `role` は **`body`/`i2v_source`/`reject` の3値のみ**（`thumb`/`still_thumb` が現れたら FAIL）
4. `role=="body"` の全静止画で `public_path` 非null、かつ `remotion/public/<public_path>` と `<stem>_depth.png` が**両方実在**（depth 欠落はレンダークラッシュ）。`role=="i2v_source"` は `public_path==null`
5. `role!="reject"` の全静止画で `max(width,height)>=3840`（`preflight_render_gate.MIN_LONG_EDGE_PX=3840`）
6. **`motion[]` 長==16。各 `public_path` が `.mp4` で終わり `_rife` を含み、`remotion/public/<path>` に実在**（★空配列/欠落は即 FAIL）
7. **`factory[]` 長==92。各 `public_path` が `/factory/` を含み、`remotion/public/<path>` に実在**（★空配列/欠落は即 FAIL）／`eyeballed_content` 非空・`qc.label_matches_content==true`
8. `overlay[].public_path` が `/overlay/` を含み `/factory/` を**含まない**・`overlay` 配列長==12
9. `sha256` が全配列を通して一意（EP39〜45 と sha256 被りゼロは A が別途保証・B は自集合内一意を検査）
10. `qc.has_readable_text`/`qc.has_identifiable_face`/`qc.has_human_body` が true の項目は `role=="reject"`（**R1/R-MINOR**）
11. `also_thumb==true` の body 静止画が**ちょうど6枚**、かつ **`scene_id` 集合が CODEX_A §4.3 の6 ID 集合と完全一致**（A↔B 契約点）。**★B は 6 ID を発明しない＝マニフェストの `also_thumb` フラグを読む**（サムネ component も同様・§11）
12. **全文字列値**が §2 の R-FORBID / R-MINOR / R-DOCHL / R-NUM を通る

> **★このバリデータは A の `--verify` と同じ不変条件を独立実装する（二重チェック）。** counts が §3.1 の確定値と食い違ったら組まずに止めて A に差し戻す（ブリーフ§2: still を増やして factory を削るな）。

---

# 4. narration_index（TTS は課金＝禁止。**実測版を消費**する）

## 4.1 なぜ narration_index か
`build_tlo_film.py` は**尺・区間・字幕を narration_index から導出する**。**秒数をコードに直書きしない。** 唯一の正は narration_index。

## 4.2 スキーマ（`tlo_narration.v1`）

```jsonc
{
  "schema_version": "tlo_narration.v1",
  "episode_id": "PD-2026-046-tlo",
  "is_stub": false,
  "total_seconds": 715.9,        // = SPEC narration_seconds（[DESIGNED SILENCE 1..2] の実音無音を含む）
  "chunks": [
    { "section": "HOOK",   "start": 0.000, "end": 4.100, "text": "..." },
    { "section": "OPENING","start": 25.000, "end": 29.100, "text": "..." },
    { "section": "ACT_1",  "start": 55.000, "end": 59.200, "text": "..." }
  ]
}
```

**section 値（固定・台本の機械解析ヘッダに一致）:** `HOOK` / `OPENING` / `ACT_1` / `ACT_2` / `ACT_3` / `ENDING`。**ACT_4 は無い。**
`build_tlo_film.py` は `section_windows()`（各 section の最初のチャンク start）で幕境界を得る。**台本ヘッダ `## [HOOK]/[OPENING]/[ACT_1]/[ACT_2]/[ACT_3]/[ENDING]` を rename しない。**

**台本の `【DESIGNED SILENCE …】` は2箇所**（HOOK 1.8s＝完全無音／ENDING 2.0s＝音を足す沈黙）。narration_index の実測がこの無音を **total_seconds に内包**している。`【beat】` は小ギャップ。**存在しない演出マーカーを発明しない。**

## 4.3 spec のタイムライン（**設計目標。実タイミングは narration_index が上書きする**）

- 総語数 **2,125**（spec `words_total`）/ `wpm 178.1` / narration_seconds **715.9**（spec）。
- **唯一の正は `python scripts/check_script_length.py <script> --json`。自己申告・体感の尺判定は禁止。**
- ACT_3 が**最も長く・最も遅い**（判例核: 6-3・二段テスト逐語・reasonable suspicion・footnote 7 の警察留保）。ACT_1 は最短・抑制（事実提示）。

## 4.4 実測 narration_index の受領
本番は別工程が TTS→faster-whisper で `06_audio/narration_index.v001.json`（実測語タイム・`is_stub:false`）を作る。
**これは課金ジョブなので B は起動しない。** 来た `narration_index.v001.json` を `--narr` に渡すだけ。**台本本文はそのまま（改変しない）。**

---

# 5. `tlo_film.json` の構築（`scripts/build_tlo_film.py`＝`build_cleveland_film.py` の複製・実素材のみ）

## 5.1 `FilmData` 型（`CaseFilm.tsx` から。これに従う）

```ts
export type Cut = {start:number; dur:number; kind:'img'|'footage'; src:string; treatment:string; seed:string};
export type FilmData = {
  fps:number; narration:string; narrationSeconds:number; hookSeconds:number; hookLine:string;
  hook:{start:number;dur:number;kind:string;src:string;seed:string}[];
  cuts:Cut[]; captions:{start:number;end:number;text:string}[];
  graphics:{start:number;end:number;lines:string[]}[];      // 必須フィールド。EP46 は []
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
- **`fps = 30`**。`narration = "tlo/narration.mp3"`（実在）

### 5.1.1 ★durationInFrames の4項関数（明示・total ≤ 750s を assert）

```
caseFilmDurationInFrames(tloFilm, fps=30)
  = round(hookSeconds * fps)        // hookSeconds = 8.0（★EP46 は cold-open hook 尺を frame0 に積む）→ round(240)=240
  + round(OPENING_SEC * fps)        // OPENING_SEC = 3.50（green BrandOpening は HOOK 後）→ round(105)=105
  + ceil(narrationSeconds * fps)    // narrationSeconds = narration_index.total_seconds（= 715.9・silence 込み）→ ceil(21477.0)=21477
  + round(ENDCARD_SEC * fps)        // ENDCARD_SEC = 9.00 → round(270)=270
```

- **hookSeconds を明示: `hookSeconds = 8.0`**（ブリーフ§5・タスク指示。EP43 の `OFF = 8.0 + 3.5 = 11.5` と整合＝AE `film_offset_sec`＝§7.10）。
- 概算（fps30・narration 715.9）: `240 + 105 + 21477 + 270 = 22092 frames = 736.4s`。**id=Ep46Tlo の durationInFrames は 22092。**
- **ビルダ末尾で `assert total_frames/fps <= 750.0`**（736.4 ≤ 750 ✓）。超えたら exit 1。

## 5.2 カット構成（**§3 マニフェストから機械的に組む・紙芝居回避が最優先**）

```
総カット 224 = factory 92 (footage) + motion 32 (footage) + 静止画 100 (img)

[A] first-use share（check_asset_reuse floor 0.70）
    distinct 92+16+84 = 192 → 192/224 = 0.8571            ✓ >=0.70

[B] per-asset cap（check_asset_reuse）
    factory: 92/92  = 1.00回  ✓ <=1（★factory は再使用禁止）
    motion : 32/16  = 2.00回  ✓ <=2
    still  : 100/84 = 1.19回  ✓ <=2

[C] animation_mix（★2つの尺度を両方満たす）
    (i) cut数ベース   still-share = 100/224 = 0.4464        ✓ <=0.45（★余裕が薄い＝下の警告）
        motion coverage = (92+32)/224 = 124/224 = 0.5536   ✓ >=0.45
    (ii) frame ベース still 平均短め → still-frame-share ~0.42 ✓ <=0.45

[D] 平均ショット長（spec mean_shot 3.19 / max 6.0）
    715.9 / 224 = 3.196 秒/カット                          ✓ <=6

[E] factory 下限（30秒に1本 = 24 → >=24本） 92本            ✓
```

> **★[C](i) の cut数ベース still-share 0.4464 は cap 0.45 に薄い。still を1枚増やすか factory を1本削ると 0.45 を超える。マニフェストが still 84 / factory 92 / motion 16 を割ったら組まずに止めて A に差し戻す。**

## 5.3 カット割り当てのルール（`build_cleveland_film.py` の `allocate()`/`tile_window()` を踏襲）

1. 各幕の秒窓を `section_windows()` から取り、幕内に **factory : motion : still を按分**（下表は**非拘束の目安**。実配分は narration_index の窓長で自動調整。確定値は「合計 factory 92 / motion 32 / still 100」だけ）:

   | section | factory | motion | still | 小計 |
   |---|---|---|---|---|
   | HOOK+OPENING | 9 | 4 | 15 | 28 |
   | ACT_1 | 12 | 6 | 14 | 32 |
   | ACT_2 | 19 | 8 | 22 | 49 |
   | ACT_3 | 33 | 8 | 30 | 71 |
   | ENDING | 19 | 6 | 19 | 44 |
   | **計** | **92** | **32** | **100** | **224** |

2. **factory は各1回のみ**（使用済み集合を持ち二度と引かない）。**motion は各≤2回・still は各≤2回**（`allocate(cap=…)`）
3. **同一素材を連続させない**（順序を散らす）
4. 静止画 `treatment` は `["depth","scan","duotone","focus"]` を循環（同じ treatment を3連続させない）
5. **still の `dur` を footage の `dur` より系統的に短く**（§5.2[C]・`tile_window` の重み）
6. motion の `dur` は **3.0–3.4秒**（超えるとループが見える）
7. **AEカードの区間（§7.2）に重なるカットも存在させる**（コンポジタ SKIP 時に穴が空かないため）

## 5.4 `figures[]` と `captions[]`
- `figures[]` は §6（**36本**・spec floor 30 に +6・`graphics[]=[]`・**dochighlight 不使用**）
- `captions[]` は narration_index の全チャンクを **verbatim**（`build_captions()` と同一）。SRT も同時出力

## 5.5 合成レイヤー（`overlay`）— **`cuts[].src` に出さない**
`overlay` 12本を `cuts[].src` に入れると factory 判定（上限1回）になり FAIL する。`tlo_film.json` に **`overlays` 独自キー**で持たせる（`CaseFilm` は未知キーを無視）か、専用レイヤーで `screen` 合成する。

## 5.6 ビルダが出力する成果物

| 出力 | パス |
|---|---|
| film.json | `remotion/src/data/tlo_film.json` |
| public コピー | `remotion/public/tlo/film_data.v001.json` |
| **build provenance** | `episodes/PD-2026-046-tlo/04_scenes/tlo_build_manifest.v001.json`（**A の `05_visuals/` に書かない**） |
| **beatsheet**（figures+AE区間の突き合わせ表） | `episodes/PD-2026-046-tlo/04_scenes/tlo_beatsheet.v001.json` |
| SRT（フォールバック） | `episodes/PD-2026-046-tlo/08_edit/captions.final.v001.srt`（§8 の生成器が上書き） |

> **★beatsheet の命名注意:** `check_motion_density`/`check_animation_mix` は `04_scenes/premium_beatsheet.v*.json` を**自動検出して film.json より優先**する。**B の beatsheet は `tlo_beatsheet.v001.json`（`premium_` を付けない）** にして、ゲートの測定源を film.json 一本に保つ。

## 5.7 CLI
```bash
$PY scripts/build_tlo_film.py \
  --assets episodes/PD-2026-046-tlo/05_visuals/asset_manifest.v001.json \
  --narr   episodes/PD-2026-046-tlo/06_audio/narration_index.v001.json \
  --out    remotion/src/data/tlo_film.json \
  [--captions episodes/PD-2026-046-tlo/08_edit/captions.final.v001.srt]
```
**実素材のみ。`is_stub==true` のマニフェストを渡されたら exit 1。** 末尾に `check_asset_reuse` 相当の自己レポートを print する。

---

# 6. Remotion 側 `figures[]`（**36本・spec floor 30 に +6・`graphics[]=[]`・dochighlight 不使用**）

## 6.1 密度の検算（`check_motion_density`・**AEカードは1本も数えられない**）

```
figures 36本（film.json） / body 11.93分(=715.9/60) = 3.02 /分     ✓ beats_per_min_floor 2.5
coverage: 36本 × 平均6.0s = 216.0s / 715.9 = 30.2%                  ✓ MIN_ANIMATED_COVERAGE 0.25
variety : 下記 kind を13種使用                                      ✓ variety_floor 3
spec motion.beats_floor = 30 に対し 36 で余裕。figures の dur は 5.4–6.0s を基本に。
```

> **★3軸すべて AND。density/coverage/variety のどれか1つでも floor 未満で FAIL。** 36本を非重複で置き、平均 dur ~6.0s を確保。

## 6.2 ★★★ `FigureSpec` の `kind` は**実在する小文字値のみ・`dochighlight` は使わない** ★★★

> **大文字名は無言で描画が消える。`comparebars` は非在→`compbars`。`votetally` は在（6-3 に使う）。**
> **★`dochighlight` を1本も使わない**（黒バー/box/underline がバグに見える＝3回指摘・R-DOCHL）。判読ハイライトの意図は `quote`/`stat`/`lowerthird`/`kinetic` で代替する。

**EP46 で使う実在 `kind`（`FigureBeats.tsx` union から・全小文字・全て `start`/`end` 必須）:**

| `kind` | EP46での用途 |
|---|---|
| `acttitle` | 幕頭「THE SEARCH」/「RIGHTS AT THE SCHOOLHOUSE」/「REASONABLENESS」（`index`=1/2/3・R-NUM 除外） |
| `timeline` | ①手続: トイレ→office→purse→少年審判(排除却下・delinquent)→NJ最高裁 reverse→米最高裁 reverse（F03/F07）②判例日付: 1984 argued → 1985-01-15 decided（F01） |
| `votetally` | **6-3**（F13・White 多数／Brennan・Marshall・Stevens 一部反対・中立帰属） |
| `quote` | White 逐語のみ×3（F11 twofold/inception/scope・attribution "Justice White, for the Court"・R-ATTRIB） |
| `stat` | 469 U.S. 325（F01）/ TWO PRONGS（F11・value 2）/ reasonable suspicion ラベル（F10） |
| `numberticker` | 1985（F01・decided）/ 14（F02・age）/ 6-3 到達（F13） |
| `lowerthird` | 開示 `AI-assisted visualization` / New Jersey v. T.L.O. 469 U.S. 325 (1985)（F01）/ Fourth Amendment applies（F09）/ footnote 7 reservation（F15） |
| `compbars` | ①PROBABLE CAUSE（street）vs REASONABLE SUSPICION（school）＝引き下げ（F10・R-STANDARD）②WARRANT（street）vs NO WARRANT（school・ただし 4A 適用）（F09/F10） |
| `mechanism` | ①巻紙 hinge＝喫煙違反→薬物疑いへ転換（`faultsplit`・F05）②二段の階段 inception→scope（`gears`/`faultsplit`・F11）③トイレ扉（`closingdoor`・HOOK） |
| `kinetic` | 「NOT NO RIGHTS. NOT FULL RIGHTS.」(emphasisWords=["IN-BETWEEN"] 系)/「REASONABLE SUSPICION」/「WHEN POLICE STEP IN」(F15) |
| `pindropmap` | New Jersey（単一ピン・F17・校名 Piscataway は出さない） |
| `routemap` | 捜索の膨張: タバコ→巻紙→marijuana→dealing 証拠（F05/F06・臨床的・非扇情・薬物を美化しない） |
| `bar` | 押収物の段階（臨床的一列・C-5 尊厳/非扇情） |

**`quote[].attribution` は §2 の `APPROVED_QUOTES` に一致（White 逐語のみ）。要約を引用符に入れない。**
**★`kind` に `dochighlight` を1件も置かない（R-DOCHL・grep で 0）。**

## 6.3 figures 配分（33 figures + 3 kinetic-role = **全 36 を figures[]**・graphics[]=[]・variety=13種）

| kind | 枠数 |
|---|---|
| `acttitle` | 3 |
| `timeline` | 3 |
| `votetally` | 1 |
| `quote` | 3 |
| `stat` | 5 |
| `numberticker` | 3 |
| `lowerthird` | 4 |
| `compbars` | 4 |
| `mechanism` | 3 |
| `kinetic` | 3 |
| `pindropmap` | 1 |
| `routemap` | 1 |
| `bar` | 2 |
| **合計** | **36**（variety = 13 種・**dochighlight を含めない**） |

> **★実装表現:** 上記 36本を**すべて `figures[]`** に入れ、**`graphics[]=[]`** にする（`check_motion_density` は `figures+graphics+heroCuts` を合算・floor 30 に +6）。

## 6.4 figures アンカー設計（`build_cleveland_film.py` の `FIGURE_ANCHORS` 方式）

**方式:** `(anchor_sec, payload)` を秒昇順に置き、`build_figures()` が `end = min(anchor+FIG_DUR, next_anchor-FIG_GAP, total-0.5)` でクランプ、`end-start < FIG_MIN_DUR` なら **exit 1**。`FIG_DUR=6.0 / FIG_MIN_DUR=3.0 / FIG_GAP=0.4`。**アンカー秒は `section_windows()` 基準のオフセット**（秒直書き禁止）。

**配置方針（36本・§2 台帳の値だけを焼く・kind を分散・6制約順守・dochighlight 不使用）:**

- **HOOK/OPENING（4）:** `lowerthird`（`AI-assisted visualization` 開示）/ `kinetic`（"THE BAG ON THE DESK"）/ `pindropmap`（**F17 New Jersey**・単一ピン）/ `mechanism:closingdoor`（トイレ扉）
- **ACT_1（8）:** `acttitle`（THE SEARCH・index1）/ `timeline`（**F03/F07** 手続: トイレ→office→purse→少年審判排除却下→delinquent→NJ最高裁 reverse→米最高裁 reverse）/ `lowerthird`（**F02** a 14-year-old freshman · initials T.L.O. only）/ `mechanism:faultsplit`（**F05** 巻紙 hinge＝喫煙違反→薬物疑い）/ `routemap`（**F05/F06** タバコ→巻紙→marijuana→dealing 証拠・臨床的）/ `bar`（**F06** 押収物の段階・非扇情）/ `kinetic`（**F04** "SHE SAID SHE DID NOT SMOKE"・本文脈のみ）/ `numberticker`（**F02** 14・age）
- **ACT_2（9）:** `acttitle`（RIGHTS AT THE SCHOOLHOUSE・index2）/ `lowerthird`（**F08** the question: does the 4A apply, and by what test）/ `compbars`（**F09/F10** WARRANT/PROBABLE CAUSE［street］ vs NO WARRANT/REASONABLE SUSPICION［school］・引き下げ枠）/ `kinetic`（**F09** "THE FOURTH AMENDMENT WALKS IN WITH YOU"）/ `stat`（**F10** REASONABLE SUSPICION・"a standard lower than probable cause"）/ `mechanism:gears`（二つの極論を退けた＝均衡）/ `lowerthird`（**F09** Fourth Amendment applies to school officials）/ `stat`（**F08** two easy answers refused・value 2）/ `compbars`（**F09** not no rights / not full rights・"in-between"）
- **ACT_3（11）:** `acttitle`（REASONABLENESS・index3）/ `votetally`（**F13** 6-3・White 多数・中立帰属）/ `lowerthird`（**F01** New Jersey v. T.L.O., 469 U.S. 325 (1985)）/ `stat`（**F01** 469 U.S. 325）/ `compbars`（**F10** PROBABLE CAUSE → REASONABLE SUSPICION・street→school・引き下げ）/ `quote`（**F11** "reasonable grounds for suspecting that the search will turn up evidence that the student has violated or is violating either the law or the rules of the school" → "Justice White, for the Court"）/ `quote`（**F11** scope 逐語 → "Justice White, for the Court"）/ `stat`（**F11** TWO-PART TEST・value 2）/ `numberticker`（**F01** 1985 decided）/ `mechanism:faultsplit`（**F11/F12** inception→scope の二段・各段が前段に結び付く）/ `timeline`（**F01** 1984 argued/reargued → 1985-01-15 decided） 
- **ENDING（4）:** `kinetic`（**F09/F10** "NOT NO RIGHTS. NOT FULL RIGHTS."・in-between）/ `quote`（**F11** twofold-inquiry 逐語 → "Justice White, for the Court"）/ `lowerthird`（**F15** footnote 7: when police step in, a higher standard can return — school officials only・C-6）/ `lowerthird`（開示 `AI-assisted visualization` 再掲）

> **★C-1 枠付け:** `no warrant`/`no probable cause` を出す payload には必ず「4A は適用される／reasonable suspicion」を同梱。「students have no rights」「search anything」を書かない。
> **★C-3:** 基準 payload は reasonable suspicion（probable cause 不要）＝引き下げ。「probable cause is required」と書かない。**★C-4:** votetally は 6-3 のみ。**★C-6:** footnote 7 payload は「school officials only / police は higher standard」を同梱。**★引用は White 逐語のみ・attribution "Justice White, for the Court"。**

## 6.5 配置ルール
1. **AEの区間（§7.2）と1秒でも重ならない**（`validate_tlo_beats` が突き合わせ）
2. **同じ kind を連続させない**
3. 1枠 **5.4–6.0秒**
4. `quote[].quote`/`kinetic[].lines`/`*.label` は §2 の R-NUM・R-ATTRIB・R-FORBID・R-OVERCLAIM・R-STANDARD・R-VOTE・R-POLICE・R-MINOR・R-DOCHL 検査対象
5. 台帳外の数値を `value`/`numKeys` に置かない（**R-NUM で FAIL**）
6. **`emphasisWords` は1–2語の短句のみ**（長句は末尾が切れる＝EP40 実害）
7. **`kind` に `dochighlight` を1件も置かない（R-DOCHL）**

---

# 7. After Effects カード（`build_tlo_hero_cards.py` / `composite_tlo_hero.py`）

## 7.1 位置づけ
AEカードは **film.json とは別**に ffmpeg で本編に焼き込む（§0.5-2＝密度に数えられない）。
`build_cleveland_hero_cards.py` を**コピーしてパス・定数・CARDS デッキだけ差し替える**。レイアウト実装（**VOTE_SPLIT を含む8種**）・`money_keys()`・`fit_size()`・AI開示レイヤー・完了マーカー・機械の罠対処は**1行も削らない**。

## 7.2 AEカードデッキ（**単調増加・重複ゼロ・台帳裏付けのみ・6制約順守。この表が契約。7枚**）

**区間の秒は本番 rendered base（narration_index 由来）に一致させる。** 下表の秒は spec タイムライン基準の**目安**で、`build_tlo_hero_cards.py` は section 窓からオフセットで算出しクランプする。**背景静止画は象徴オブジェのみ（R1/C-5・未成年の肖像化禁止）。accent は green `#3F8F5F`。**

| id | レイアウト（**実装済み・§7.3**） | hero/main（主表示） | top / bottom / attribution | F-ID | 背景（象徴のみ） | required |
|---|---|---|---|---|---|---|
| v01 | VOTE_SPLIT | **6 – 3** | top: **THE VOTE** / bottom: **THE FOURTH AMENDMENT APPLIES IN SCHOOL** | F13/F09 | 最高裁列柱（顔なし・green） | 必須 |
| d01 | DATE_STAMP | **JANUARY 15, 1985** | place: **NEW JERSEY v. T.L.O. - 469 U.S. 325** | F01 | 大理石の列柱（顔なし） | 必須 |
| n01 | CENTER_STACK | **NO WARRANT · NO PROBABLE CAUSE** | top: **INSIDE A PUBLIC SCHOOL** / bottom: **BUT THE FOURTH AMENDMENT STILL APPLIES** | F10/F09 | ロッカー列（無人） | 必須 |
| c01 | SPLIT_COMPARE | left: **PROBABLE CAUSE** / right: **REASONABLE SUSPICION** | top: **THE STANDARD, LOWERED** / bottom: **STREET → SCHOOLHOUSE** | F10 | 左=街路 / 右=校門（天秤） | 必須 |
| t01 | CENTER_STACK | **TWO-PART TEST** | top: **REASONABLENESS** / bottom: **JUSTIFIED AT INCEPTION · REASONABLE IN SCOPE** | F11 | 二段の階段（象徴） | 必須 |
| q01 | QUOTE_CARD | **"REASONABLE GROUNDS FOR SUSPECTING THAT THE SEARCH WILL TURN UP EVIDENCE THAT THE STUDENT HAS VIOLATED OR IS VIOLATING EITHER THE LAW OR THE RULES OF THE SCHOOL"** | attribution: **JUSTICE WHITE, FOR THE COURT** | F11/F14 | 大理石（判読困難・顔なし） | 必須 |
| p01 | CENTER_STACK | **WHEN POLICE STEP IN** | top: **FOOTNOTE 7 — RESERVED** / bottom: **A DIFFERENT, HIGHER STANDARD CAN RETURN** | F15 | 校門のバッジ／敷居（象徴） | 必須 |

> **★行順＝start 昇順（時系列）:** `v01`(ACT3 冒頭「vote of six to three」) < `d01`(ACT3 引用カード 469) < `n01`/`c01`(基準の引き下げ) < `t01`(二段テスト) < `q01`(White 逐語) < `p01`(ACT3 末尾 footnote 7)。**全7枚は判例核＝ACT_3 の長い窓に配置**（ACT_3 が最長・最遅）。**HOOK(0–hook末) と ENDCARD(末尾9s) に重ねない。**
> **★q01 の hero は §2 `APPROVED_QUOTES` の prong-1 逐語に完全一致**（ブリーフ§6 の `"...EVIDENCE..."` は表示短縮の目安。**焼き込む文字列は逐語全文**で R-QUOTE を通す。改行が要るなら別レイヤー・TextDocument に `\n` を入れない）。attribution は **"Justice White, for the Court"** のみ。
> **★v01 は 6-3 のみ（F13）**＝台帳一致。`5-4`/`7-2`/`9-0`/`unanimous` を書かない（R-VOTE）。**★n01 は "NO PROBABLE CAUSE" と "4A STILL APPLIES" を同一カードに**（C-1/C-3・R-OVERCLAIM/R-STANDARD・削除禁止）。**★c01 は "REASONABLE SUSPICION" 側を必ず併記**（probable cause を要求と読ませない・R-STANDARD）。**★p01 は "school officials only / police は higher standard"（footnote 7）を保持**（C-6・R-POLICE）。
> **どのカードにも「students have no rights」「schools can search anything」「probable cause is required」を書かない。数値ID＝台帳（§2.2）と一致必須。カウント終了から区間終端まで最低 1.20秒ホールド。**

**検算（Codex は自分で再計算して一致を確認）:** 7区間・単調増加・重複ゼロ・HOOK と ENDCARD に重ねない・Remotion figures(§6) と1秒も重ならない（`validate_tlo_beats` が検査）。

## 7.3 レイアウト（`build_cleveland_hero_cards.py` の実装を踏襲・**実装済みレイアウト名だけを使う**）
複製元 `build_cleveland_hero_cards.py` が実装するレイアウトは**この8種**:
`DATE_STAMP` / `CENTER_STACK` / `MONEY_STACK` / `SPLIT_COMPARE` / `ACT_TITLE_CARD` / `QUOTE_CARD` / `VOTE_SPLIT` / `SEAM_TRANSITION`。
**§7.2 デッキが使うのは field スキーマが既知の 5種:** `VOTE_SPLIT` / `DATE_STAMP` / `CENTER_STACK` / `SPLIT_COMPARE` / `QUOTE_CARD`。
**★`MONEY_STACK` / `SEAM_TRANSITION` / `ACT_TITLE_CARD` は本 EP の AE デッキでは未使用**（金額は無く、幕頭は Remotion `acttitle` figure が担う）。
**上記5種以外のレイアウト名を発明しない（`validate_tlo_beats` §7.9 ルール3 で FAIL）。dochighlight をレイアウト名に使わない。**
**共通レイヤースタック・Anton/Oswald・`psName()` の runtime 解決は複製元と同一。**

**★共通レイヤースタックに AI開示レイヤーを維持（R1・全カード常時焼き・複製元が既に持つ）:** 最上位に近い固定レイヤーとして
`AI-assisted visualization`（Oswald 20px / SILVER `#C8CDD6` / opacity 70% / 右下 `[W-32, H-28]`）を全カードに焼く。字幕帯とは縦56px 以上離す。

**★EP46 色定数（0..1 float・schoolhouse-green レーン色。EP41 gold / EP42 blue / EP43 amber / EP44 teal / EP45 crimson を流用禁止・DESIGN と一致）:**
```python
ACCENT = [0.247, 0.561, 0.373]  # #3F8F5F schoolhouse-green（アクセント：数値・下線・レーン分離）
WHITE  = [0.961, 0.969, 0.980]  # #F5F7FA
SILVER = [0.784, 0.804, 0.839]  # #C8CDD6（開示テキスト）
INK    = [0.039, 0.039, 0.047]  # #0A0A0C 近黒ルート（サムネ bg と一致）
```
> **accent は必ず `#3F8F5F`（他話色を書かない）。** サムネ・OP props・AEカードの accent は全て `#3F8F5F`。ビルダ末尾 `beats.json` の `"accent"` 文字列も `#3F8F5F` に。

**数値カードは全て `money_keys()` 系で表示文字列を Python 事前計算**（JSX で算術しない＝EP38 確定ルール）。
**`v01`（6-3）は左右2値を別レイヤー（改行禁止）。`c01`（PC/RS）も左右2値を別レイヤー。`n01`（NO WARRANT · NO PROBABLE CAUSE / 4A STILL APPLIES）は各行を別レイヤー。`q01`（White 逐語）は長文を `fit_size()`＋別レイヤー折り返しで（`\n` 禁止）。**

## 7.4 `beats.json` スキーマ（本番 `08_edit/ae_hero/beats.json`）
`build_cleveland_hero_cards.py` の beats スキーマに準拠。トップに **`film_offset_sec`**（=hookSeconds + OPENING_SEC = **11.5**・§7.10 のコンポジタが読む）。各 beat に `id`/`layout`/`start`/`end`/`dur`/`still`(象徴 or null)/`hero`/`main`/`top`/`bottom`/`left`/`right`/`kicker`/`date`/`place`/`caption`(**改行禁止・最大50字**)/`value`/`numKeys`/`blend_mode`(既定 "overlay")/`required`/`out`/`attribution`(**QUOTE_CARD=q01 は必須**・§2 `APPROVED_QUOTES` と一致・R-ATTRIB)。
**`value`/`main`/`hero` の数値は §2 台帳の `verified:true` 値のみ。`v01` は 6-3（R-VOTE）。`n01`/`c01` は R-STANDARD（reasonable suspicion / no probable cause）と R-OVERCLAIM（4A applies）を満たす。`p01` は footnote 7（R-POLICE）。`beats.json` に `dochighlight` を出さない（R-DOCHL）。**

## 7.5 このマシン固有の罠（複製元が対処済み。**1つも省くな**）
1. `setTemporalEaseAtKey` の配列次元は **spatial(Position) で 1**（`if(!prop.isSpatial){...}` で分岐）
2. RS = **`"最良設定"`** / OM = **`"H.264 - レンダリング設定を一致 - 15 Mbps"`**（英語名は try/catch フォールバックのみ）
3. TextDocument の改行は `\n` 不可。**`caption` は1行**（改行が要るなら別レイヤー）。**テキスト幅は `sourceRectAtTime(t,false).width` で実測**（advance-width 推定は禁止＝EP40 の文字切れ原因）。em-dash は `-`
4. `app.newProject()` は headless でハング。**使わず**同名 `TLO_` コンプを防御削除
5. ビルドは**カード7枚で ~90–110秒**。`render/_build_ok.txt` をポーリング（**タイムアウト最低300秒**）
6. 起動はデタッチ + 出力ポーリング。jsx 末尾で `app.quit()`
7. `comp.motionBlur=true` だけでは無効。**動かすレイヤー個別に `layer.motionBlur=true`**
8. 2Dレイヤー回転は **`"ADBE Rotate Z"`**（`"ADBE Rotation"` は null）
9. `inPoint` と `outPoint` の**両方**を設定
10. 読み込み後 `item.mainSource.conformFrameRate = 30`
11. 実行パス `C:\Program Files\Adobe\Adobe After Effects 2026\Support Files\AfterFX.exe`（実在確認済み）
12. `proj.gpuAccelType = GpuAccelType.SOFTWARE`
13. **`getFontsByFamilyNameAndStyleName` を使うフォント厳格解決**（miss は throw・フォールバック禁止／allFonts[i] ラッパー経由 unwrap）
14. **フォント文字列やラベルを PowerShell 経由の正規表現/エスケープで生成しない**（`\b` がバックスペース化した実害）。Python 側で literal に組む。**Python 先頭に `sys.stdout.reconfigure(encoding="utf-8")`**
15. **aerender 前に `.aep` の mtime > `.jsx` の mtime を assert**（古い .aep を焼く事故防止＝EP39-41 実害）

## 7.6 実行
```bash
$PY scripts/ae/build_tlo_hero_cards.py
"C:/Program Files/Adobe/Adobe After Effects 2026/Support Files/AfterFX.exe" -noui \
  -r ".../episodes/PD-2026-046-tlo/08_edit/ae_hero/tlo_hero.jsx"
# render/_build_ok.txt を待つ（最大300秒）→ render/*.mp4 が7本揃うまで待つ（最大1200秒）
$PY scripts/ae/composite_tlo_hero.py
```

## 7.9 `scripts/validate_tlo_beats.py`（BLOCKING）
1. `beats[].start` 昇順・区間非重複
2. 全 `start`/`end` が本編ナレ区間内（HOOK と ENDCARD 末尾9s に重ねない）
3. `layout` が §7.3 の**実装済み5種**（`VOTE_SPLIT`/`DATE_STAMP`/`CENTER_STACK`/`SPLIT_COMPARE`/`QUOTE_CARD`）のいずれか。**この5種以外（`MONEY_STACK`/`SEAM_TRANSITION`/`ACT_TITLE_CARD`/`dochighlight` 等）は FAIL。** still が必要なレイアウトで null なら FAIL
4. `still` 非null は実在＋長辺 >=3840px
5. `hero`/`main`/`top`/`bottom`/`left`/`right`/`caption`/`value` が §2（R-FORBID/R-NUM/R-ATTRIB/R-OVERCLAIM/R-STANDARD/R-VOTE/R-POLICE/R-MINOR/R-DOCHL/R-DATE）を通る
6. `verified:false` の値を要求するカードは `required:false` で除外、`required:true` なら exit 1
7. **`tlo_film.json` の `figures[]`（§6）と AE の区間が1秒でも重ならない**
8. `caption` に改行が含まれない
9. **AI開示レイヤーの存在（R1）** — ビルダが全カード共通スタックに `AI-assisted visualization`（右下）を焼く設定であることを静的に確認。無ければ FAIL
10. **`dochighlight`/`DOCHIGHLIGHT` が beats/レイアウト名に1件も無い（R-DOCHL）**

## 7.10 基底 mp4 とコンポジタ（`build_tlo_bgm_real.py` → `composite_tlo_hero.py`）
```
# 合成順（ブリーフ§5）: build_tlo_bgm_real.py（narration+BGM）→ composite_tlo_hero.py（AEカード焼込み・film_offset_sec 適用）
BASE = episodes/PD-2026-046-tlo/08_edit/tlo_final_bgm.v002.mp4     # build_tlo_bgm_real.py が生成
OUT  = episodes/PD-2026-046-tlo/08_edit/tlo_final_bgm.v003_ae.mp4  # composite_tlo_hero.py が生成
FFMPEG  = C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe
FFPROBE = C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffprobe.exe
W,H,FPS = 1920, 1080, 30
```
- **`build_tlo_bgm_real.py`（`build_caniglia_bgm_real.py` 複製）は `OFF = 8.0 + 3.5 = 11.5`**（hookSeconds + OPENING_SEC）。section windows は実 narration_index から。
- **`composite_tlo_hero.py`（`composite_caniglia_hero.py` 複製）は `beats.json` の `film_offset_sec`(=11.5) を読み**、各 beat 区間を本編尺にマップ。
- **SKIP4条件を1行も削らない:** ① `render/<id>.mp4` 不在 ② 解像度 != 1920x1080 ③ 実測尺 `< dur-0.3` ④ `film_offset_sec + beat.end > base_dur`。SKIP した区間は元カットのまま残る。**何枚 SKIP したかを stderr に必ず出す。**
- ffmpeg は `overlay=0:0:eof_action=pass:enable='between(t,start,end)'`（`blend_mode` が screen/multiply の時のみ `blend`）。
- **出力後 `probe_dur(OUT)` でベースとの尺差 <=0.5秒を確認。出荷済みは絶対に上書きしない（必ず `_v003_ae`）。**

---

# 8. 字幕の切断規則（`scripts/gen_captions_tlo.py`＝`gen_captions_cleveland.py` の複製）

## 8.1 原則
**文字数は「上限」であって「分割基準」ではない。** `gen_captions_cleveland.py` の `internal_split()`/`chunk_sentence()` を**そのままコピー**。
`from fix_caption_dangling import NO_DANGLE_END, wrap as safe_wrap`（**語リストを自前で書き直さない**）。

## 8.2 通すゲート `scripts/check_caption_breaks.py`（**閾値を緩めるの禁止**）
- **A. 行末の機能語** = 0件 / **B. 孤立キュー** = 0件 / **C. 句をまたぐ切断(hard)** = 0件（A/B/C いずれか1件で FAIL）

## 8.3 EP46 の入力と対応
- 入力は **narration_index の各チャンク文**（`--narr`）。**字幕テキストは台本本文と1:1対応**（§0.5-5）。台詞・別エピソード文の混入禁止。verbatim で使い、構文境界で分割するだけ。
- `ABBR` に `U.S.` / `v.` / `Mr.` / `Ms.` / `No.` / `T.L.O.` を持つ（`New Jersey v. T.L.O.` の `v.` と `T.L.O.`、`469 U.S. 325` の `U.S.` で文を切らない）。
- タイミングは narration_index の start/end。CPS <=27・最小表示 0.90秒。**Step で決めた境界を時間都合で動かさない。**
- **字幕にも R-FORBID 適用**（台本本文の過大化語は"否定/仮定/正確文脈"なので verbatim なら通る。§2.1 の★注意：近似語を禁止語に足さない）。

## 8.4 セルフテスト（`--selftest`）
`New Jersey v. T.L.O.` / `469 U.S. 325` / `T.L.O.` / `Fourth Amendment` で文が切れないこと、機能語で終わるキュー・孤立キューを作らないことを含む4ケースを実装し、**出力を `check_caption_breaks.py` に食わせて exit 0 まで自動確認。**

## 8.5 実行
```bash
$PY scripts/gen_captions_tlo.py --narr episodes/PD-2026-046-tlo/06_audio/narration_index.v001.json
$PY scripts/check_caption_breaks.py episodes/PD-2026-046-tlo/08_edit/captions.final.v001.srt
# → PASS が出るまで直す。ゲート側の閾値を緩めるのは禁止。
```

---

# 9. 5ゲートの実際の判定（**build 後に必ず全部通す・animation_mix を忘れるな**）

| ゲート | 実体 | 入力 | EP46 の通過根拠 |
|---|---|---|---|
| `check_asset_reuse.py <film.json>` | factory≤1 / motion≤2 / still≤2 / first-use≥0.70 | **film.json 位置引数** | §5.2: factory1.00 / motion2.00 / still1.19 / first-use **0.8571** |
| `check_motion_density.py --ep PD-2026-046-tlo` | graphics+figures+heroCuts のみ / density≥2.5・coverage≥0.25・variety≥3（**AND**） | **`--ep`** | §6.1: **3.02 / 30.2% / 13種**（AEカードは0本・beats≥30） |
| `check_animation_mix.py --ep PD-2026-046-tlo` | cuts を img=still/その他=footage 分類 / still-share≤0.45・motion-cov≥0.45 | **`--ep`** | §5.2[C]: still-share **0.4464(cut)/~0.42(frame)** / motion-cov **0.5536+** |
| `check_caption_breaks.py <srt>` | A/B/C 各0件 | **srt 位置引数** | §8 の構文境界生成器 |
| `check_script_length.py <script> --json` | 総語数 / wpm / narration_seconds | **script 位置引数** | 2,125語 / wpm178.1 / **715.9s** |

> **★ゲートの入力指定:** density/mix は **`--ep PD-2026-046-tlo`**。**`--json <film.json>` は出力パス（上書き事故）なので入力に使わない。** asset_reuse は film.json 位置引数、caption_breaks は srt 位置引数、script_length は script 位置引数。
> **`check_animation_mix`/`check_motion_density` は `04_scenes/premium_beatsheet.v*.json` があればそれを優先する。** §5.6 の通り B の beatsheet は `tlo_beatsheet`（`premium_` 無し）なので**auto-detect されず film.json を測る。**

---

# 10. OP バンパー `OpeningTlo`（Remotion・fps60/1920x1080/180f）

## 10.1 二重OPを作らない
本編（`Ep46Tlo`）の OP は `Bookends.tsx` の `BrandOpening` のまま（`op_ed_bookends` ゲート・フォーク禁止）。
`OpeningTlo` は**独立したタイトルバンパー成果物**（`out/tlo_opening.mp4`・Shorts/予告/SNS 用）。**本編に ffmpeg で焼き込まない。**

## 10.2 Composition 設定
| 項目 | 値 |
|---|---|
| `id` | `OpeningTlo` |
| 解像度 / fps / duration | **1920×1080 / 60 / 180**（=3.0秒） |
| component | `remotion/src/compositions/OpeningTlo.tsx` |

```tsx
import {OpeningTlo, openingTloDurationInFrames} from './compositions/OpeningTlo';
import tloOpeningProps from '../props/tlo.json';
<Composition id="OpeningTlo" component={OpeningTlo}
  width={1920} height={1080} fps={60}
  durationInFrames={openingTloDurationInFrames(60)} defaultProps={tloOpeningProps}/>
```

**依存:** `@remotion/motion-blur`（未導入時のみ `cd remotion && npm i @remotion/motion-blur`）。
**`remotion/remotion.config.ts`** は既に正典値（png / h264 libx264 / CRF16 / yuv420p / bt709 / aac 320k / 全コア並列 / angle）。**一致確認のみ・書き換えない。**

## 10.3 秒数ベースのタイムライン（fps=60・フレーム直書き禁止・全て `Math.round(fps*秒)`）

| 秒 | 起きること | 手法 |
|---|---|---|
| 0.00–0.40 | L1 グラデ背景 opacity 0→1・**同時に scale 1.08→1.00（`Easing.out(Easing.cubic)`）** | interpolate（opacity 単独禁止・scale 併用） |
| 0.10 | ロゴ（`hasLogo`）左上に spring・scale 0.4→1.0・opacity 0→1 | spring `damping:14,mass:0.9` |
| 0.15–0.25 | L2 グリッド reveal（opacity→0.18）＋ translateY 0→48px | spring `damping:200,mass:1` + `Easing.inOut(Easing.sin)` |
| 0.25 | L3 グロー（green `#3F8F5F`）scale 0.6→1.15 / opacity 0→0.85 | spring `damping:18,mass:1.2`（併用） |
| 0.30–0.86 | L4 主役タイトルが1文字ずつ切れ上がり（overflow:hidden + translateY 110%→0）＋ opacity。スタッガー **2f/文字**。全体を `Trail(layers=6,lagInFrames=1.2,trailOpacity=0.45)` で包む | spring `damping:16,mass:1` |
| 0.55–1.15 | L2b **ジッパー線（バッグを開けるモチーフ）**が中央から横に `scaleX 0→1`＋opacity 0→0.5（green）・**motionBlur** | spring `damping:22,mass:1.1`・`transformOrigin:'left center'` |
| 0.95–1.35 | L5a アクセント下線（green）左から `scaleX 0→1` | spring `damping:16,mass:0.8`・`transformOrigin:'left center'` |
| 1.10–1.55 | L5b サブタイトル translateY 24→0 + opacity 0→1 | spring `damping:20,mass:1`（併用） |
| 1.55–3.00 | settle→ホールド。**完全静止フレーム無し・フェードアウトしない** | — |

> **等速線形を1箇所も使わない。opacity 単独の演出を1箇所も作らない**（全 opacity が translateY/scale/scaleX と対）。最低3背面レイヤー（L1 グラデ・L2 グリッド・L3 グロー）。

## 10.4 props 型と値
```ts
export type OpeningTloProps = { title:string; subtitle:string; accent:string; hasLogo:boolean };
```
`remotion/props/tlo.json`: `{ "title":"THE BAG ON THE DESK", "subtitle":"DOES THE FOURTH AMENDMENT WALK INTO SCHOOL?", "accent":"#3F8F5F", "hasLogo":true }`
`remotion/props/tlo_short.json`: `{ "title":"THE BAG ON THE DESK", "subtitle":"CAN YOUR SCHOOL SEARCH YOUR BAG?", "accent":"#3F8F5F", "hasLogo":false }`
> `subtitle`/`title` も §2 の R-FORBID/R-OVERCLAIM/R-STANDARD/R-MINOR 検査対象。ルート背景は INK 近黒 `#0A0A0C`。
> **accent は EP41 gold / EP42 blue / EP43 amber / EP44 teal / EP45 crimson を書かず green `#3F8F5F`（レーン分離・他話色流用は BLOCKER）。** 疑問形 subtitle は制約1に反しない（「無権利」と断定しない）。

## 10.5 量産
```bash
cd remotion && npm run studio     # OpeningTlo を 0→180f スクラブして §10.3 の各時刻を目視
npx remotion render OpeningTlo out/tlo_opening.mp4 --props=./props/tlo.json
npx remotion render OpeningTlo out/tlo_short_op.mp4 --props=./props/tlo_short.json
```

---

# 11. サムネ3案（`TloThumbnails.tsx`・`<Still>` 1280×720・Root に `Thumb-tlo-01..03`）

**共通要件:** 見出し全て大文字・4語以内・320pxで判読 / **未成年の肖像禁止（R1/C-5・T.L.O. の顔/身体/実名を出さない）** / INK 黒 `#0A0A0C` bg + green `#3F8F5F` / 背景は body 静止画のうち `also_thumb==true` の6枚（象徴オブジェのみ。**サムネ component はマニフェストの `also_thumb` フラグを読む＝scene id をハードコードしない**） / `thumbnail_visibility`（luma平均≥33＋コントラスト）を通す。目標CTR 6%+。
**「students have no rights」「schools can search anything」「probable cause is required」を出さない（R-FORBID/R-OVERCLAIM/R-STANDARD）。**

- **T1「机の上のバッグ」（最推奨）:** 木製机に伏せたキャンバスのハンドバッグ、口が開き中身が覗く（象徴・顔なし）。文字 **`THE BAG ON THE DESK`**（4語）。`BAG` を green。
- **T2「6-3」（数字勝負）:** 最高裁列柱を暗く落とし、前面に **`6 – 3`**（大）＋ **`THE 4TH APPLIES IN SCHOOL`**（下・制約1）。数字は F13 の検証済み値のみ。
- **T3「校門の権利」（尊厳）:** ロッカー列／校門の象徴。文字 **`SEARCHED AT SCHOOL?`**（疑問形・制約1）。`SCHOOL` を green。**「無権利」に見せない。**

**A/Bタイトル候補（`09_package`・60字以内・ブリーフ§0 のとおり・過大化禁止）:**
- **A:** `A Teacher Searched Her Purse. The Supreme Court Said It Was Fine.`
- **B:** `Can Your School Search Your Bag Without a Warrant?`
> ※「生徒に権利はない/学校は何でも捜索できる」系のタイトルは**禁止**（制約1・R-OVERCLAIM）。

**固定コメント** `09_package/pinned_comment.v001.txt`（§2 の R-NUM/R-ATTRIB/R-FORBID/R-OVERCLAIM/R-STANDARD/R-VOTE/R-POLICE 検査対象。台帳事実のみ・**生徒の権利 explainer への1行を含む**）:
```
Two things New Jersey v. T.L.O. actually settled — and one people keep getting wrong.

SETTLED (6-3, 1985): The Fourth Amendment DOES apply inside a public school.
Students do not shed their rights at the schoolhouse door. But a school official
does not need a warrant and does not need probable cause. The standard is
reasonable suspicion, and the search must stay reasonable in scope — Justice
White's two-part test: justified at its inception, reasonable in scope.

WHAT PEOPLE GET WRONG: This is NOT "students have no rights," and it is NOT the
same power the police have on the street. The Court expressly reserved (footnote 7)
the standard for searches run by or with law enforcement — a higher standard can
apply once police are involved.

If you want to understand your own Fourth Amendment rights at school, look up a
plain-language student-rights explainer from a reputable legal-aid or civil-liberties source.
```
> **description.txt にも生徒の権利 explainer への1行を置く（R-OVERCLAIM 隣接検査）。AI 開示行（`AI-assisted visualization`）を description に置く（R1）。**

---

# 12. 本編コンポジション登録（`remotion/src/Root.tsx`・`Ep45Cleveland`/`Ep43Caniglia` の形を踏襲）
```tsx
import tloFilm from './data/tlo_film.json';
<Composition id="Ep46Tlo" component={CaseFilm}
  durationInFrames={caseFilmDurationInFrames(tloFilm as unknown as FilmData, BRAND.video.fps)}
  fps={BRAND.video.fps} width={BRAND.video.width} height={BRAND.video.height}
  defaultProps={{ data: tloFilm as unknown as FilmData, seriesLabel: 'PRIME DOCUMENTARY',
    title: 'A Teacher Searched Her Purse. The Supreme Court Said It Was Fine.',
    subtitle: 'The Fourth Amendment applies at school — but the bar is reasonable suspicion, not probable cause. 6-3, 1985.' }}/>
```
> **id は正確に `Ep46Tlo`（切り詰め・綴り違い・大文字化の誤記に注意）。** `caseFilmDurationInFrames` の 4項評価は **22092 frames**（§5.1.1・hookSeconds=8.0）。
> **`import tloFilm from './data/tlo_film.json'`。** `remotion/src` に現在 `Ep46Tlo`/`tloFilm` の識別子が無いこと（衝突しない）を確認してから追記（`grep -rn "Ep46Tlo\|tloFilm" remotion/src` = 0）。
> `title`/`subtitle` も §2 検査対象（R-FORBID/R-OVERCLAIM/R-STANDARD/R-VOTE）。「students have no rights」「probable cause is required」を書かない。

---

# 13. 受入（自分で exit 0 を確認してから完了報告）
```bash
cd C:\Users\aab15\Documents\prime-documentary ; PY=./.venv/Scripts/python.exe

# 0. 語数（最優先・課金前に落とす）
$PY scripts/check_script_length.py episodes/PD-2026-046-tlo/03_script/script.en.v001.md --json   # 2,125語 / wpm178.1 / 715.9s

# 1. 事実性/6制約（EP46固有・正確性ゲートはこの1本・dochighlight 不使用・White 逐語 attribution も検査）
$PY scripts/check_tlo_facts.py --json

# 2. 契約バリデータ
$PY scripts/validate_tlo_beats.py
$PY scripts/check_tlo_asset_manifest.py --assets episodes/PD-2026-046-tlo/05_visuals/asset_manifest.v001.json

# 3. ★5ゲート（animation_mix を忘れるな・入力は --ep / 位置引数を厳守）
$PY scripts/check_asset_reuse.py    remotion/src/data/tlo_film.json
$PY scripts/check_motion_density.py --ep PD-2026-046-tlo
$PY scripts/check_animation_mix.py  --ep PD-2026-046-tlo
$PY scripts/check_caption_breaks.py episodes/PD-2026-046-tlo/08_edit/captions.final.v001.srt

# 4. 水増し・レンダ前プリフライト
$PY scripts/check_padding.py --ep PD-2026-046-tlo --json
$PY scripts/preflight_render_gate.py --ep PD-2026-046-tlo

# 5. ★public_slim を staging（EP45 の render 不能事故を防ぐ）→ 本編レンダ（slim public・並列4）→ BGM → AEカード合成
#    public/tlo の全メディア（img + 各 <stem>_depth.png / factory / motion / audio=narration.mp3）を public_slim/tlo にコピー
mkdir -p remotion/public_slim/tlo
cp -r remotion/public/tlo/img remotion/public/tlo/factory remotion/public/tlo/motion remotion/public_slim/tlo/
cp remotion/public/tlo/narration.mp3 remotion/public_slim/tlo/ 2>/dev/null || true
#    （overlay を screen 合成で使うなら overlay もコピー。tlo_film.json が参照する全 src が public_slim 下に在ることを確認）
cd remotion
npx remotion render Ep46Tlo out/tlo.mp4 --public-dir=public_slim --concurrency=4
cd ..
$PY scripts/build_tlo_bgm_real.py
$PY scripts/ae/composite_tlo_hero.py

# 6. 本編最終受入（episode番号は★位置引数・--ep ではない）
$PY scripts/check_final_acceptance.py 46 \
  --render episodes/PD-2026-046-tlo/08_edit/tlo_final_bgm.v003_ae.mp4 --emit-receipt
```

| ゲート | EP46 目標値 |
|---|---|
| `check_script_length` | 総語数 **2,125** / `wpm 178.1` / narration **715.9s** |
| `check_asset_reuse` | factory≤1 / motion≤2 / still≤2 / first-use **0.8571**（floor0.70） |
| `check_motion_density` | density **3.02**/min / coverage **30.2%** / variety 13（floors 2.5 / 0.25 / 3・beats **≥30**） |
| `check_animation_mix` | still-share **0.4464(cut)/~0.42(frame)**（cap0.45）/ motion-cov **0.5536+**（floor0.45） |
| `check_caption_breaks` | 行末機能語0 / 孤立キュー0 / hard split 0 |
| `check_tlo_facts` | violations = 0（台帳照合・引き下げ枠・6-3・White 逐語 attribution・footnote 7・R-FORBID・R-DOCHL・R-MINOR） |
| runtime band | narration 715.9s + bookends（hook8.0+op3.5+end9.0）・total **736.4s ≤ 750s** |
| factory クリップ | ≥24本 → **92本** |
| image_resolution | 全静止画 長辺 ≥3840px |
| thumbnail | 3案 @1280×720 + selected luma≥33 |
| op_ed_bookends | `BrandOpening`/`BrandEndcard` を import（フォーク禁止） |

**全て exit 0 でなければ `package_ready` にしない。自己申告QCは無効。QC基準を書き換えて通すのは禁止。**

## 13.1 完成後の全編アイボール（**1フレーム判定禁止＝EP39-41 実害**）
`tlo_final_bgm.v003_ae.mp4` を **0→末尾まで通しで実視聴**し、以下を確認してから完了報告:
- 紙芝居感が無い（still が連続していない・footage が体感で過半）
- AEカード7枚が全て焼き込まれ数値が台帳と一致（「students have no rights」「schools can search anything」「probable cause is required」がどこにも無い）
- **v01「6 – 3」＋「THE FOURTH AMENDMENT APPLIES IN SCHOOL」が読める（制約1/4）。d01「JANUARY 15, 1985 / 469 U.S. 325」（制約6・R-DATE）**
- **n01「NO WARRANT · NO PROBABLE CAUSE / BUT THE FOURTH AMENDMENT STILL APPLIES」・c01「PROBABLE CAUSE → REASONABLE SUSPICION」が読める（引き下げであって消滅でない・制約3）**
- **t01「TWO-PART TEST / JUSTIFIED AT INCEPTION · REASONABLE IN SCOPE」・q01 が White 逐語＋「JUSTICE WHITE, FOR THE COURT」帰属（要約を引用符にしていない・R-ATTRIB）**
- **p01「WHEN POLICE STEP IN / FOOTNOTE 7 — RESERVED / A HIGHER STANDARD CAN RETURN」が読める（制約6・警察関与の区別）**
- T.L.O. の顔・身体・実名が無い（象徴＝トイレ扉/机の上のバッグ/タバコ/巻紙/ロッカー/天秤/列柱のみ・制約5）／薬物が扇情でない（臨床的・美化なし）
- **`dochighlight`（黒バー/box/underline）が1本も無い（figures/AE／R-DOCHL）**
- 生成ビジュアル表示中は `AI-assisted visualization` が右下に常時（**AEカード7枚の表示中も**開示が見える＝カード共通スタックに焼かれている・R1）
- **概要欄/固定コメントに生徒の権利 explainer への1行がある（R-OVERCLAIM 隣接）**
- accent が green `#3F8F5F`（EP41 gold / EP42 blue / EP43 amber / EP44 teal / EP45 crimson が紛れていない）
- 音ズレ・字幕ズレ・尺差（base と <=0.5s）が無い

---

# 14. 絶対にやらないこと
- **EP39 / EP40 / EP41 / EP42 / EP43 / EP44 / EP45 のファイル・素材に触らない**（読み取りのみ可）。レーンを分離する。
- **スレッドAの所有ファイル（§0.2.1）に書かない**（`05_visuals/` `05_stock/` `remotion/public/tlo/` `H:\...\ai\tlo\`）。**B の provenance は `04_scenes/tlo_build_manifest.v001.json` に書く。**
- **設計書 / `EP46_tlo_CODEX_A_*` / PD-2026-039〜045 に触らない。**
- **課金ジョブを起動しない**（ElevenLabs TTS / 課金画像生成API / YouTube アップロード）。narration_index は実測版を消費するだけ。
- **公開済み・出荷済み mp4 を上書き・再レンダしない**（出力は必ず `_v003_ae`）。
- **台帳（§2）に無い数値を焼かない**（$580,000 型の再発防止）。不明値は `verified:false` でカード除外。**R-NUM は narrative figure のみ（manifest 構造カウント・acttitle index は除外）。**
- **`FigureSpec` の `kind` を推測で書かない**（§6.2 の実在小文字値のみ。大文字名は無言で消える。`comparebars` は非在→`compbars`）。**★`dochighlight` を1本も使わない（R-DOCHL）。**
- **`--variants` という語を書かない**（1シーン1枚・バリエーション0＝ブリーフ§1）。
- **asset_manifest の `factory`(92)/`motion`(16) を空/欠落のまま build しない**（EP45 の build 失敗の核心）。**`counts`/`role` enum/`overlay` 枚数を CODEX_A と食い違わせない**（`role` は `body`/`i2v_source`/`reject` の3値のみ・`thumb`/`still_thumb` を作らない・overlay=12・also_thumb 6枚＝CODEX_A §4.3 と一致）。
- **`public_slim` を staging せずにレンダしない**（EP45 の render 不能事故・§13-5）。
- **「生徒に権利はない/4A は学校に適用されない」と書かない**（制約1・R-OVERCLAIM）。**「probable cause が必要」と誤らせない**（制約3・R-STANDARD＝reasonable suspicion）。**票決を 6-3 以外にしない**（制約4・R-VOTE）。**二段テストを1段に潰さない/「何でも捜索可」に過大化しない**（制約2・C-2）。**T.L.O. の顔/肖像/実名を出さない・薬物を扇情化しない**（制約5・R-MINOR）。**警察関与時の higher standard 留保（footnote 7）を消さない**（制約3/C-6・R-POLICE）。**引用は White 逐語のみ・attribution "Justice White, for the Court"**（R-QUOTE/R-ATTRIB）。**数値は台帳一致**（R-NUM）。
- **accent に他話色を使わない**（green `#3F8F5F` のみ）。
- **stub/dryrun/placeholder のコードパスを作らない**（実素材のみ・grep 0）。
- **スペック数値（224 cuts / still84 / factory92 / motion16 / distinct192 / first-use0.8571 / still-share0.4464 / figures≥30→36 / 715.9s / 2,125語 / mean_shot3.19 / total736.4s≤750s / durationInFrames22092 / hookSeconds8.0）を変えない。**
- **実在しないスクリプト名を書かない**（新規は §0.3 の一覧のみ・複製元を明記）。**composition id は `Ep46Tlo`。** **PowerShell 経由で正規表現/エスケープを生成しない**（`\b` バックスペース化の実害）。
