# EP46 kelo — Codex スレッドB「実装」引き継ぎプロンプト v001

> **このファイルは単体で完結している。他のファイルを読まなくても着手できる。**
> 並行して走っていたスレッドA（素材生成）のファイル `EP46_kelo_CODEX_A_*.md` は**読まない**（Aは既に FROZEN・接続点は §3 のマニフェスト1ファイル）。
> 設計書 `EP46_kelo_DESIGN*.md` / 共有ブリーフ `EP46_kelo_DESIGN_BRIEF.shared.md` も**読まない**（必要な数値・AEデッキ・figures 配分はすべて本書に転記済み）。
> `EP46_kelo_PRODUCTION_SPEC.v001.json` の数値は本書に転記済み。**あなたはこれを書き換えない。**

```
あなたは Prime Documentary（YouTubeドキュメンタリーチャンネル）の制作エンジニアです。
リポジトリ: C:\Users\aab15\Documents\prime-documentary
Python:     C:\Users\aab15\Documents\prime-documentary\.venv\Scripts\python.exe
メディア:   H:\pd-media
担当:       EP46 / Episode ID: PD-2026-046-kelo / slug: kelo
Composition id（本編）: Ep46Kelo
```

**題材:** *Kelo v. City of New London*, 545 U.S. 469 (2005)（No. 04-108・decided **2005-06-23**）と **Susette Kelo**（New London, Connecticut の**存命の私人 = R2・有罪歴なし**）。
最高裁は **5-4 で収用を UPHELD（合憲＝城の側が取ってよい、と判断）**。本作の主題は「**違法だから**」ではなく「**合法とされたこと（the Court said the city COULD do this）への規範的批判＋後日談**」。
「public use」を「**public purpose**」と広く解し、経済開発型の private 転売収用も該当しうる、とした。O'Connor / Thomas は**反対意見**（Court に帰属させない）。ピンクの家は**取壊しでなく解体移築（36 Franklin St）**。

> **★正確性6制約が全出力を律する（§2）。** 収用を「illegal / unconstitutional / struck down」と書かない（**5-4 UPHELD**）・「public purpose」を正確に（「政府はどんな理由でも家を奪える」に過大化しない）・**O'Connor / Thomas は反対意見**として中立帰属（Court に帰属させない）・Susette Kelo の顔/肖像/身体を一切出さない（象徴のみ・尊厳・poverty porn 禁止）・**捏造引用禁止**・数値は台帳一致＆">40 states" はヘッジ・「her house was demolished」と書かない（近隣宅は取壊し／彼女の家は移築）。**★`figures[].kind` に `dochighlight` を1件も入れない**（黒バー/box/underline がバグに見える＝3回指摘）。**概要欄は 988 でなく Institute for Justice の公開記録／州 eminent-domain リソースの中立1行。**

---

# 0. このスレッドの責務・境界・完了条件

## 0.1 このスレッド（B）の責務 — **コード律速。実装は全部書ける。**

| # | 作業 | 成果物 |
|---|---|---|
| B-1 | エピソードディレクトリと `manifest.json` | `episodes/PD-2026-046-kelo/**` |
| B-2 | 境界契約マニフェストの**消費側**バリデータ | `scripts/check_kelo_asset_manifest.py` |
| B-3 | 事実台帳 F-ID と 6制約ゲート（**EP46固有・BLOCKING**） | `scripts/check_kelo_facts.py`（**`check_caniglia_facts.py` を複製**） |
| B-4 | `kelo_film.json` ビルダ（**asset_map→manifest変換＋beatsheet生成／footage混在・実素材のみ**） | `scripts/build_kelo_film.py`（**`build_cleveland_film.py` を複製**） |
| B-5 | beats バリデータ（AEとRemotionの区間衝突検査＋ledger／6制約） | `scripts/validate_kelo_beats.py`（**`validate_cleveland_beats.py` を複製**） |
| B-6 | **構文境界で切る字幕生成器**（実測 narration_index から verbatim） | `scripts/gen_captions_kelo.py`（**`gen_captions_cleveland.py` を複製**） |
| B-7 | **After Effects カード**のビルダとコンポジタ | `scripts/ae/build_kelo_hero_cards.py` / `scripts/ae/composite_kelo_hero.py` |
| B-8 | 本編 BGM ミックス（AEカード合成の基底 mp4 を生成） | `scripts/build_kelo_bgm_real.py`（**`build_caniglia_bgm_real.py` を複製・OFF=hook+3.5=11.5**） |
| B-9 | Remotion 本編コンポジション登録 `Ep46Kelo` | `remotion/src/Root.tsx` |
| B-10 | OP バンパー `OpeningKelo`（fps60/1920x1080/180f） | `remotion/src/compositions/OpeningKelo.tsx` |
| B-11 | サムネ3案 | `remotion/src/compositions/KeloThumbnails.tsx` |
| B-12 | 本編レンダ→BGM→AEカード合成→全ゲート→**全編アイボール** | `episodes/PD-2026-046-kelo/08_edit/**` |

> **★このスレッドは「実素材のみ」（ブリーフ§5/§7 / タスク指示）。stub/placeholder/dryrun のコードパスを作らない**（`grep -rEi 'stub|placeholder|dryrun'` が B の新規スクリプトで **0** であること）。A は FROZEN（§3 の本番マニフェストが実在）・narration_index は実測版が実在する前提で組む。**素材が来ていなければ止めて A/上流に差し戻す**（架空の黒スタブで緑にしない）。

## 0.2 もう一方のスレッド（A・FROZEN）との境界 — **接続点はただ1ファイル。**

```
episodes/PD-2026-046-kelo/05_visuals/asset_manifest.v001.json
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
| `episodes/PD-2026-046-kelo/manifest.json` | **B** | 読み書き |
| `episodes/PD-2026-046-kelo/{00_topic,01_research,03_script,04_scenes,06_audio,08_edit,09_package,approvals,events}/**` | **B** | 読み書き |
| `remotion/src/**` `remotion/props/**` | **B** | 読み書き |
| `scripts/*kelo*.py` / `scripts/ae/*kelo*.py`（§0.3） | **B** | 新規作成 |
| **`episodes/PD-2026-046-kelo/05_visuals/**` `05_stock/**`** | **A** | **読み取りのみ。書くな** |
| **`H:\pd-media\assets\ai\kelo\**` / `ai_video\kelo\**`** | **A** | **読み取りのみ。書くな** |
| **`remotion/public/kelo/{img,factory,motion,overlay}/**`** | **A** | **読み取りのみ。書くな** |
| `EP46_kelo_DESIGN*.md` / `EP46_kelo_DESIGN_BRIEF.shared.md` / `EP46_kelo_CODEX_A_*.md` | **設計/Aスレッド** | **触るな** |
| `EP46_kelo_PRODUCTION_SPEC.v001.json` / `EP46_kelo_script.en.v001.md` / `EP46_kelo_facts.v001.json` | **上流** | **読み取りのみ。書くな** |
| `episodes/PD-2026-039-*/**` … `PD-2026-045-*/**` / それらの素材 | **他エージェント** | **絶対に触るな（読み取りのみ可）** |

> **B は `remotion/public/kelo/` に書かない**（A の staging 済み本番素材）。B の provenance/beatsheet は `04_scenes/` に書く（§5.6）。

## 0.3 B が新規作成するスクリプト（これ以外を新規に作らない。既存を改変しない）

| パス | 役割 | 手本（**改変せず読んで複製→パス/定数だけ差し替え**・実在確認済み） |
|---|---|---|
| `scripts/check_kelo_asset_manifest.py` | §3.3 消費側バリデータ | `scripts/check_cleveland_asset_manifest.py`（無ければ `check_caniglia_asset_manifest.py`） |
| `scripts/check_kelo_facts.py` | §2 6制約＋台帳（BLOCKING・**正確性ゲート名はこの1つに統一**） | **`scripts/check_caniglia_facts.py`**（EP43） |
| `scripts/build_kelo_film.py` | §5 film.json＋provenance＋beatsheet＋SRT（**実素材のみ**） | **`scripts/build_cleveland_film.py`**（EP45） |
| `scripts/validate_kelo_beats.py` | §7.9 不変条件 | **`scripts/validate_cleveland_beats.py`** |
| `scripts/gen_captions_kelo.py` | §8 構文境界字幕生成器 | **`scripts/gen_captions_cleveland.py`** |
| `scripts/ae/build_kelo_hero_cards.py` | §7 AEカードビルダ | **`scripts/ae/build_cleveland_hero_cards.py`**（／`build_caniglia_hero_cards.py`） |
| `scripts/ae/composite_kelo_hero.py` | §7.10 コンポジタ（`beats.json` の `film_offset_sec` を読む） | **`scripts/ae/composite_caniglia_hero.py`**（EP43） |
| `scripts/build_kelo_bgm_real.py` | §7.10 基底 mp4（narration＋BGM ミックス・**OFF=hook+3.5=11.5**） | **`scripts/build_caniglia_bgm_real.py`**（EP43） |

> **`build_kelo_film.py` の複製時に差し替える定数:** `ASSET_MAP`（マニフェスト→cut 変換テーブル）・`NARR`（narration_index 既定パス）・
> `FACTORY_SEL`（factory 選抜の参照）・`SLUG="kelo"`・`EP="PD-2026-046-kelo"`・出力パス群。**ロジック（best-pick / tile_window /
> allocate / build_figures / build_captions）は1行も変えない。**
> **既存の `build_cleveland_film.py` / `build_caniglia_film.py` / `gen_captions_cleveland.py` 等は触らない**（他エピソードが使用中）。EP46用に**新規コピー**する。
> **`build_tekoh_film.py` は実在しない。捏造しない**（複製元は上表の実在ファイルのみ・`ls scripts/` で確認済み）。

## 0.4 完了条件（実素材で、全て緑になったら「実装完了」）

```bash
cd C:\Users\aab15\Documents\prime-documentary
PY=./.venv/Scripts/python.exe

# [B-DONE-1] マニフェスト消費側バリデータ（A の FROZEN 本番マニフェスト相手に通ること）
$PY scripts/check_kelo_asset_manifest.py \
  --assets episodes/PD-2026-046-kelo/05_visuals/asset_manifest.v001.json

# [B-DONE-2] 字幕（実測 narration の実文から構文境界で生成）
$PY scripts/gen_captions_kelo.py \
  --narr episodes/PD-2026-046-kelo/06_audio/narration_index.v001.json
$PY scripts/check_caption_breaks.py \
  episodes/PD-2026-046-kelo/08_edit/captions.final.v001.srt

# [B-DONE-3] film.json を実マニフェストから組み立てる（footage 混在必須・dochighlight 不使用）
$PY scripts/build_kelo_film.py \
  --assets episodes/PD-2026-046-kelo/05_visuals/asset_manifest.v001.json \
  --narr   episodes/PD-2026-046-kelo/06_audio/narration_index.v001.json \
  --out    remotion/src/data/kelo_film.json

# [B-DONE-4] ★5ゲート全部（--ep 指定・animation_mix を絶対に忘れるな）
$PY scripts/check_asset_reuse.py     remotion/src/data/kelo_film.json
$PY scripts/check_motion_density.py  --ep PD-2026-046-kelo
$PY scripts/check_animation_mix.py   --ep PD-2026-046-kelo
$PY scripts/check_caption_breaks.py  episodes/PD-2026-046-kelo/08_edit/captions.final.v001.srt
$PY scripts/check_script_length.py   episodes/PD-2026-046-kelo/03_script/script.en.v001.md --json

# [B-DONE-5] 事実性/6制約（＋dochighlight 不使用・quote 帰属＝反対意見）
$PY scripts/check_kelo_facts.py --json

# [B-DONE-6] beats 契約（AE区間 と Remotion figures[] が1秒も重ならない）
$PY scripts/validate_kelo_beats.py

# [B-DONE-7] AE カードをビルド＋レンダ＋コンポジット
$PY scripts/ae/build_kelo_hero_cards.py
"C:/Program Files/Adobe/Adobe After Effects 2026/Support Files/AfterFX.exe" -noui \
  -r "C:/Users/aab15/Documents/prime-documentary/episodes/PD-2026-046-kelo/08_edit/ae_hero/kelo_hero.jsx"
$PY scripts/ae/composite_kelo_hero.py

# [B-DONE-8] Remotion Studio で目視
cd remotion && npm run studio
#   → Ep46Kelo / OpeningKelo / Thumb-kelo-01..03 が出て、実際に動くこと
```

**台本は既に確定済み**（`EP46_kelo_script.en.v001.md`・**2,133語・12.0分**・ロック）。本番配置先は
`episodes/PD-2026-046-kelo/03_script/script.en.v001.md`（**1バイトも変えずコピー**・整形禁止＝AI臭再発と語数ゲート再計算を招く）。

---

# 1. 実装前に必ず読むファイル（**推測で書くな**）

| パス | なぜ読むか |
|---|---|
| `scripts/build_cleveland_film.py` | **複製元。** best-pick / tile_window / allocate / build_figures / build_captions をそのまま踏襲し、定数だけ kelo に。**footage を必ず混ぜる（§0.5 の紙芝居回避）** |
| `scripts/ae/build_cleveland_hero_cards.py`（／`build_caniglia_hero_cards.py`） | **複製元。** `money_keys()`（Python で表示文字列を全事前計算）/ `fit_size()` / CARDS デッキ構造 / レイアウト定義（**`VOTE_SPLIT` を含む8種**）/ 完了マーカーをそのまま |
| `scripts/ae/composite_caniglia_hero.py` | **複製元。** SKIP4条件（missing / 解像度不一致 / 実測尺不足 / window past end）と ffmpeg フィルタグラフ（overlay/blend）と `film_offset_sec` の読み込みをそのまま |
| `scripts/gen_captions_cleveland.py` | **複製元。** `internal_split()` / `chunk_sentence()` / `NO_DANGLE_END` import をそのまま |
| `scripts/build_caniglia_bgm_real.py` | **複製元。** narration＋BGM ミックスで基底 mp4 を作る経路（**OFF=hook+3.5=11.5**） |
| `scripts/check_caniglia_facts.py` | **複製元（正確性ゲート）。** R-ルールのフレーム・`APPROVED_QUOTES`・禁止語検査・`--json` 出力をそのまま流用し kelo の R-ルールに差し替え |
| `remotion/src/compositions/CaseFilm.tsx` | `FilmData` 型 / `caseFilmDurationInFrames` / `depthSrcOf()` |
| `remotion/src/components/FigureBeats.tsx` | `FigureSpec` の**実在する `kind` 文字列**（§6.2 の警告を必ず読め・**全小文字**・**`dochighlight` は使わない**・`votetally` は `{majority,dissent}`） |
| `remotion/src/components/Bookends.tsx` | `OPENING_SEC` / `ENDCARD_SEC` / `BrandOpening` / `BrandEndcard` |
| `scripts/check_asset_reuse.py` / `scripts/check_motion_density.py` / `scripts/check_animation_mix.py` / `scripts/check_caption_breaks.py` / `scripts/check_script_length.py` | 通すべき5ゲートの**実際の判定ロジック**（§9） |
| `C:\Users\aab15\Documents\pino-channel\remotion\src\Opening.tsx` | §10 の OP 正典実装 |

---

# 0.5 ★★★ EP39/40/41/42/43/44/45 で踏んだ失敗＝最初から防ぐ（本書の全体設計はこの6点を構造で潰している）★★★

1. **紙芝居（最重要）** — 静止画100%で組むと `check_animation_mix` が FAIL する。**EP46 は最初から footage を混ぜる。**
   `check_animation_mix.compute_metrics_from_film()` は film.json の `cuts[]` を
   **`kind=="img"` → still（scene 扱い）/ それ以外 → footage（motion 扱い）** と分類する。
   → §5 の cuts 構成は **factory 92 + motion 32 の footage を最初から入れて still-share を cut数ベース 0.4489・frame ベース ~0.4217** にする。
2. **AEカードは密度に数えられない** — `check_motion_density` は film.json の `graphics+figures+heroCuts` **のみ**数える。
   AEカードは ffmpeg で後合成するので**1本も数えられない**。→ §6 で **film.json 側の `figures[]` を 36本**（spec floor 30 に **+6**・`graphics[]=[]`）置く。AEカードは別勘定。
3. **FigureSpec の `kind` は実在の小文字値のみ** — 大文字名（`ActTitle`/`QuoteCard`/`VoteTally` 等）は無言で描画が消える（§6.2）。`comparebars` は非在→`compbars`。5-4 は **`votetally`（`majority:5,dissent:4`）**。**★`dochighlight` を1本も使わない**（§6.2・R-DOCHL）。
4. **台帳に無い数値を焼くな** — EP40 の生 Codex-B 出力に架空の $580,000 が入って**不採用になった実害**。
   → §2 の事実台帳 F-ID に**検証済み値だけ**を置き、`check_kelo_facts.py` が film.json/AE/サムネ/props の全数値を台帳照合する。台帳に無い数値・`verified:false` の数値を焼いたら FAIL。**">40 states" のヘッジを断定数（43/44/45/47）に変えたら FAIL（R-HEDGE）。**
5. **字幕は台本本文と対応** — EP38 で台詞混入・「final」誤称の実害。→ §8 の字幕は **narration_index の実チャンク文をそのまま** verbatim で使う（自作しない）。
6. **レンダー前ゲート** — build 後に `check_asset_reuse` / `check_motion_density` / `check_animation_mix` / `check_caption_breaks` / `check_script_length` を**全部**通す（§9・§13）。**animation_mix を忘れるな。**

---

# 2. ★ EP46固有の正確性6制約・事実性ロック（`scripts/check_kelo_facts.py`・BLOCKING）

> **この節に違反した成果物は、他が全て完璧でも出荷不可。** 検査対象は film.json の figures/captions、AE beats、
> サムネ、props、固定コメント、`03_script/script.en.v001.md`、（存在すれば）マニフェストの tags/caption_hint/qc.notes の**全文字列と全数値**。
> **正確性ゲートはこの1本に統一（`check_kelo_facts.py`）。DESIGN/CODEX_A も同名を参照する（別名を作らない）。** 出力 `09_package/facts_lock.v001.json`。

## 2.1 正確性6制約（全出力に適用・違反は BLOCKER）

| # | 制約 | 許可される表現 | 禁止 |
|---|---|---|---|
| C-1 | **収用は「違法」でない・5-4 UPHELD** | 「the Court said the city COULD do this」「the taking stands」「upheld」「it let something stand」「ruled the city was allowed to do it」。`5-4`/`5 – 4`/`the taking` を出すカードは UPHELD 枠（`stands`/`upheld`/`the city could`/`allowed`）を同一 payload に併記 | 収用自体への「the taking was illegal」「ruled it unconstitutional」「the court struck down」「struck it down」「the taking is illegal」 |
| C-2 | **ドクトリン＝public use を public purpose と広く解す（過大化しない）** | 「public use → public purpose」「economic development can count as a public purpose」「a genuine, deliberate plan to benefit the public」。**Stevens 帰属＝for the majority**。Kennedy の pretext 留保を落とさない | 「the government can take your home for any reason」を**断定**として提示（台本の否定文 "did not say … for any reason it likes" は許可＝§2.1注意） |
| C-3 | **O'Connor / Thomas ＝反対意見**（Court に帰属させない） | O'Connor 逐語は `attribution` に「dissenting」必須。Thomas は「Justice Thomas, dissenting」。多数意見の逐語は「Justice Stevens, for the majority」 | O'Connor/Thomas の言を「the Court held」「the majority said」に帰属／多数意見を「dissent」に帰属 |
| C-4 | **Susette Kelo ＝R2・象徴のみ・poverty porn 禁止・家は移築** | 事件主体としての名（"Susette Kelo bought the house"）。ビジュアルは小さなピンクの家・水辺（川と入江）・空の通り・condemnation notice・解体重機/更地/雑草・企業の site plan と光る模型・Motel 6 と Ritz-Carlton の対比・州法令集の背・家をフラットベッドに載せて移築。**「her house was demolished」と書かない（近隣宅は取壊し／彼女の家は移築）** | 顔・肖像・身体・人物化／`Kelo` 直後60字の `face`/`portrait`／`her pink house was demolished`／扇情 |
| C-5 | **NLDC/Pfizer/城を制度・機関として説明** | NLDC＝private nonprofit・Institute for Justice 代理・Pfizer 触媒。中立記述 | 実在私人（Kelo 以外の住人・Scott Bullock 等）に非公開・非逐語の断罪語 |
| C-6 | **数値は台帳一致・捏造ゼロ・medium はヘッジ** | 画面数値は §2.2 の台帳のみ。**">40 states"（F18・medium）は "more than"/"over" のヘッジ必須** | 台帳外の金額・年・件数・州数／F18 を断定数（43/44/45/47）で提示 |
| R1 | **実在人物の顔・肖像を生成しない** | 全生成ビジュアル表示中は `AI-assisted visualization`（右下）常時／概要欄1行AI開示 | 認識可能な人物・読める偽公文書 |
| ★DH | **dochighlight 不使用** | 判読ハイライトの意図は `quote`/`stat`/`lowerthird`/`kinetic` で代替 | `figures[].kind`/beats/レイアウト名に `dochighlight`/`DOCHIGHLIGHT` を1件でも出す |

**★禁止語（`check_kelo_facts.py` が全文字列を case-insensitive 部分一致で検査。1件でも FAIL）:**
`the taking was illegal` / `the taking is illegal` / `taking was unconstitutional` / `ruled it unconstitutional` / `ruled the taking illegal` /
`the court struck down` / `struck it down` / `the court struck the taking` / `declared the taking unconstitutional` /
`the government can take any home for any reason` / `take any home for any purpose` / `no home is safe from any taking` /
`o'connor for the court` / `thomas for the court` / `the majority dissented` / `the dissent held for the court` /
`her pink house was demolished` / `kelo's house was demolished` / `poverty porn` / `crying child` / `weeping mother` /
`exactly forty states` / `forty-three states` / `forty-five states` / `47 states passed`。
> **★重要な設計注意:** 台本本文（＝字幕 verbatim）には「The Court did not rule that taking the pink house was illegal」「the Court struck something down」「the government can take your home for any reason it likes（← "did not say" の後）」など
> **否定/正確文脈の語**が含まれる。上の禁止語リストは**それらと衝突しない断定形だけ**を選んである。**禁止語リストにこの近似語（`was illegal` 単体・`struck down` 単体・`for any reason it likes`・`struck something`）を足すな**
> （字幕 verbatim を巻き込んで false FAIL する）。C-1/C-2/C-3 の**枠付き/限定の別**は下の**文脈ルール**（R-DISPO/R-QUOTE/R-HEDGE）で捕える。

## 2.2 事実台帳 F-ID（`03_script/kelo_facts.v001.json`・**Bが `EP46_kelo_facts.v001.json`（F01–F20）から転記して作る**）

**スキーマ版:** `kelo_facts.v1`。各 F-ID は `{"value":..., "unit":..., "verified":bool, "confidence":"high|medium", "claim_id":"", "attribution":"", "quote":""}`。
**F18/F20 は `confidence:"medium"`（ヘッジ）。それ以外は high。medium は `attribution`/ヘッジ語 非空必須。**

| F-ID | 内容 | 使う場所 | conf |
|---|---|---|---|
| F01 | **5-4 で taking を UPHELD**（違法・違憲・struck down と言わない） | fig votetally / AE vote01 | high |
| F02 | 引用＝**Kelo v. City of New London, 545 U.S. 469 (2005)**・No. 04-108・decided **2005-06-23** | fig lowerthird / AE date01 | high |
| F03 | **Stevens 執筆（多数）**・Kennedy/Souter/Ginsburg/Breyer 同調 | fig lowerthird | high |
| F04 | ドクトリン＝**public use を public purpose と広く解し経済開発が該当**（"any reason" でない）／Stevens 逐語「Promoting economic development is a traditional and long accepted function of government」 | fig kinetic/compbars / AE pp01 | high |
| F05 | **Kennedy 補足（第5票）**＝pretextual/trivial/implausible 収用は禁止・要注視事案は厳格化の余地 | fig mechanism:faultsplit | high |
| F06 | **O'Connor 主反対**・Rehnquist/Scalia/Thomas 同調 | fig lowerthird | high |
| F07 | **O'Connor 逐語**「Nothing is to prevent the State from replacing any Motel 6 with a Ritz-Carlton, any home with a shopping mall, or any farm with a factory」＋前置「The specter of condemnation hangs over all property」 | fig quote / AE oc01（**dissenting**） | high |
| F08 | **O'Connor 逐語**「The beneficiaries are likely to be those citizens with disproportionate influence and power in the political process, including large corporations and development firms」＋「license to transfer property from those with fewer resources to those with more」 | fig quote/bar（**dissenting**） | high |
| F09 | **Thomas 別個反対**＝原意主義「public use = use by the public」・弱者に偏る | fig quote/kinetic / AE th01（**dissenting**） | high |
| F10 | Fort Trumbull 再開発＝**90エーカー**計画・NLDC 策定・hotel/office/住宅/marina/riverwalk | fig stat/timeline | high |
| F11 | **Pfizer 約$300 million** 研究拠点が触媒 | fig stat / numberticker | high |
| F12 | 区域**約115物件**・少数（nine owners of 15 properties）が拒否し提訴・Kelo は **parcel 3** | fig numberticker | high |
| F13 | Susette Kelo の「little pink house」＝**1997購入**・水辺・自ら改装（R2・象徴のみ） | fig（象徴のみ） | high |
| F14 | 原告側代理＝**Institute for Justice**（Scott Bullock が弁論） | fig lowerthird | high |
| F15 | **2009 に Pfizer が離脱表明**・拠点閉鎖・**1000超雇用**喪失・税優遇失効期 | fig numberticker/timeline | high |
| F16 | 収用地は長年**更地・無税収**、2011ハリケーン後は瓦礫置場（**NOTHING BUILT**） | fig kinetic/compbars / AE nb01 | high |
| F17 | 近隣宅は取壊し／**Kelo の家は解体移築（36 Franklin St・~2008）**（家は demolished と言わない） | fig（象徴・移築）/ AE pink01 | high |
| F18（ヘッジ） | **">40 states"** が Kelo 後に収用改革（正確数はソース差＝medium・"more than forty" 表記） | fig stat/regionmap / AE st01 | **medium** |
| F19 | 先例＝**Berman v. Parker (1954)** / **Hawaii Housing Authority v. Midkiff (1984)**（一般記述） | fig timeline | high |
| F20（medium） | New London の衰退文脈＝**軍施設閉鎖・distressed 指定**（一般化・具体雇用数は medium） | fig（一般記述） | medium |

> **数値の許可集合（R-NUM）:** `545 / 469 / 2005 / 4 / 108 / 23 / 5 / 300 / 90 / 115 / 3 / 9 / 15 / 1997 / 2009 / 1000 / 2011 / 40 / 6 / 1954 / 1984 / 36 / 2008 / 1990`。
> これ以外の金額・年・件数・州数が画面に出たら FAIL。**特に 43/44/45/47（州数の断定）は集合外＝R-NUM でも R-HEDGE でも FAIL。**

## 2.3 `check_kelo_facts.py` の検査（exit 0=PASS / 1=FAIL / 2=スキーマ不一致・**`check_caniglia_facts.py` の R-ルール枠を複製**）

**検査対象ファイル（この一覧をハードコード。存在するものだけ検査し、無いものは `skipped[]` に必ず明記）:**

```
episodes/PD-2026-046-kelo/03_script/script.en.v001.md
episodes/PD-2026-046-kelo/03_script/kelo_facts.v*.json
episodes/PD-2026-046-kelo/08_edit/ae_hero/beats.json
episodes/PD-2026-046-kelo/09_package/*.json        （title / description / thumbnail headlines）
episodes/PD-2026-046-kelo/09_package/*.txt         （固定コメント・description.txt）
episodes/PD-2026-046-kelo/05_visuals/asset_manifest*.json  （tags / caption_hint / qc.notes）
remotion/src/data/kelo_film.json                   （figures[].* / captions[] の全文字列と数値）
remotion/props/kelo*.json                          （title / subtitle）
```

- **R-FORBID（最優先）** — §2.1 の禁止語が対象文字列のどこかに出たら即 FAIL。**近似語（否定/正確文脈）を巻き込まない断定形のみ**を検査（§2.1 の注意）。
- **R-DISPO（C-1・BLOCKING）** — `5-4`/`5 – 4`/`the taking`/`upheld`/`the taking stands` を含むカード/figure/payload に UPHELD 枠（`stands`/`upheld`/`the city could`/`allowed`/`it let something stand` のいずれか）が同一 payload に無ければ FAIL。§2.1 の C-1 断定語（違法・struck down）が出たら FAIL。**`description.txt` に Institute for Justice 記録／州 eminent-domain リソースへの中立1行が無ければ FAIL（988 でない・R1連結）。**
- **R-DOCTRINE（C-2）** — `public purpose` を含む payload は「economic development」「a plan to benefit the public」等の限定文脈同伴。「the government can take (your/any) home for any reason」を**断定形**（`did not say`/`did not`/`not` の否定を伴わない）で出したら FAIL。
- **R-QUOTE（C-3・R-ATTRIB・BLOCKING）** — `quote[].attribution` が非空・逐語のみ（要約を引用符に入れない）。**O'Connor / Thomas 帰属は `dissenting` を含む**・**Stevens 帰属は `for the majority` を含む**。許可対応表（逐語→帰属）:
  ```python
  APPROVED_QUOTES = {
    "nothing is to prevent the state from replacing any motel 6 with a ritz-carlton, any home with a shopping mall, or any farm with a factory":
        "Justice O'Connor, dissenting",                        # F07
    "the specter of condemnation hangs over all property":
        "Justice O'Connor, dissenting",                        # F07 前置
    "the beneficiaries are likely to be those citizens with disproportionate influence and power in the political process, including large corporations and development firms":
        "Justice O'Connor, dissenting",                        # F08
    "promoting economic development is a traditional and long accepted function of government":
        "Justice Stevens, for the majority",                   # F04（多数意見・逐語）
    "use by the public":
        "Justice Thomas, dissenting",                          # F09（原意主義・Thomas 反対）
  }
  ```
  **上表に無い逐語を `kind:"quote"` の `quote` / AE `QUOTE_CARD` に置いたら FAIL（EP43 R-PAYTON の教訓＝未検証 Jardines 断片の再発防止）。** O'Connor/Thomas を `for the Court`/`the majority said` に帰属したら FAIL。
- **R-HEDGE（C-6・F18・BLOCKING）** — `40 states` / `forty states` を含む payload に `more than` または `over` のヘッジが無ければ FAIL。`43`/`44`/`45`/`47` を州数として出したら FAIL（§2.1 禁止語＋R-NUM）。
- **R-NUM（C-6・R-LEDGER）** — figures[] の `value`/`majority`/`dissent`/`numKeys` 到達値、AE `beats[].value`/`beats[].main`/`beats[].hero`、サムネ数字に現れる**あらゆる数値**は §2.2 の許可集合に**完全一致**必須。
- **R-FACE（C-4/R1）** — `has_readable_text`/`has_identifiable_face`/`has_human_body` が true の項目は `role=="reject"`。`ai_prompts.v001.md` 正プロンプトの `portrait`/`face of`/`likeness`/`Susette Kelo`（人物として）/`her body`/`crying`/`weeping` は FAIL（ネガティブでの使用は可）。`Kelo` 直後60字の `face`/`portrait`/`depicted as a woman`、`her pink house was demolished`、poverty-porn 語で FAIL。生成ビジュアル区間の `AI-assisted visualization` 欠落・`description.txt` の AI 開示行欠落で FAIL。
- **R-HOUSE（C-4）** — `pink house` を含む payload に `demolished`/`torn down`/`destroyed` が同伴したら FAIL（近隣宅は取壊しでも Kelo の家は移築＝`moved`/`relocated`/`36 Franklin`）。
- **R-DOCHL（★DH・BLOCKING）** — `kelo_film.json` の `figures[].kind` に `dochighlight` が1件でも出たら FAIL
  （`grep -c '"kind"[[:space:]]*:[[:space:]]*"dochighlight"'` が **0** でなければ FAIL）。`beats.json`/レイアウト名にも `dochighlight`/`DOCHIGHLIGHT` を出さない。
- **R-DATE** — F02(2005-06-23)・F11/F20(1990s)・F13(1997)・F15(2009)・F16(2011)・F17(2008)・F19(1954/1984) の日付・年が別カードで取り違えられていないこと。

**出力:** `episodes/PD-2026-046-kelo/09_package/facts_lock.v001.json`（`{"pass":bool,"violations":[{"file","rule","line","excerpt"}],"skipped":[...]}`）。
**`pass:true` でない限り `check_final_acceptance.py` に進んではならない。**
**CLI:** `--json`。対象ファイルが未生成ならスキップして必ずログに出す。「無いから通した」を黙るな。

---

# 3. ★境界契約: `asset_manifest.v001.json`（Aから受け取る唯一のファイル・FROZEN）

## 3.1 スキーマ（**Aが生成する。Bはこの形を前提に読む・A↔B 1バイト一致**）

**スキーマ版:** `kelo_assets.v1`（固定文字列。異なれば **exit 2**）。
EP46 spec の点数に一致: **still_body 85 / still_i2v_source 16 / motion 16 / factory 92 / overlay 12**。
**★サムネは独立の分類を持たない。** body 85枚のうち**6枚**に `also_thumb:true` を立てて流用する（**`role=thumb`/`still_thumb` を作らない**・サムネ用 count キーも無い・§11）。
**このスキーマ・`counts` キー・`role` enum・`overlay` 枚数は CODEX_A（生産者）の `build_kelo_asset_manifest.py` の出力と1バイト単位で同一。**

- **`role` enum（固定・3値のみ）:** `"body"` | `"i2v_source"` | `"reject"`。**`thumb`/`still_thumb` を作らない。**
- **`counts`（固定キー・確定値）:** `{ "still_body": 85, "still_i2v_source": 16, "motion": 16, "factory": 92, "overlay": 12 }`。
- **`overlay` = 12**（A↔B 契約値）。

```jsonc
{
  "schema_version": "kelo_assets.v1",
  "episode_id": "PD-2026-046-kelo",
  "slug": "kelo",
  "generated_at": "<ISO8601>",
  "producer": "scripts/build_kelo_asset_manifest.py",
  "is_stub": false,
  "counts": { "still_body": 85, "still_i2v_source": 16, "motion": 16, "factory": 92, "overlay": 12 },

  "stills": [
    { "asset_id": "KELO-S01", "scene_id": "S01", "role": "body",   // "body"|"i2v_source"|"reject"（各1枚）
      "also_thumb": false,                    // body から6枚だけ true（§11 の6 asset ID・追加生成しない）
      "act": 0,                               // 0=HOOK/OP, 1..3=幕, 5=ED
      "public_path": "kelo/img/S01.png",      // ★Bが cuts[].src に入れる値（1シーン1枚＝固有プロンプト・_01 等の接尾なし）
      "depth_path": "H:/pd-media/assets/ai/kelo/S01_depth.png",  // role=="body" は実在必須
      "width": 3840, "height": 2160,
      "sha256": "...", "tags": ["pink_house","waterfront","symbolic"], "caption_hint": "a small pink clapboard house on a point of land where the river meets the sound",
      "source": "ai_codex", "commercial_use": "allowed", "ai_disclosure_required": true,
      "qc": {"reviewed": true, "on_theme": true,
             "has_readable_text": false, "has_identifiable_face": false, "has_human_body": false, "notes": ""} }
    // i2v 種は role=="i2v_source"・asset_id "KELO-MS01".."KELO-MS16"・public_path は null（本編カットに出ない）
  ],

  "motion": [
    { "asset_id": "KELO-M01", "source_scene_id": "M01_src",   // ★i2v_source 種 ID を指す（body still ではない）
      "source_still": "H:/pd-media/assets/ai/kelo/M01_src.png",
      "public_path": "kelo/motion/M01_rife.mp4",   // ★必ず .mp4 かつ "_rife" を含む
      "act": 0, "width": 1280, "height": 720, "fps": 48, "frames": 164, "duration_sec": 3.417,
      "sha256": "...", "tags": ["wrecking_crew","cleared_lot"],
      "qc": {"reviewed": true, "on_theme": true, "artifact_free": true, "notes": ""} }
  ],

  "factory": [
    { "asset_id": "AF-BG-0731",
      "public_path": "kelo/factory/AF-BG-0731__grey_water_estuary.mp4",  // ★必ず "/factory/" を含む
      "type": "backgrounds", "subtype": "waterfront", "kind": "video",
      "license": "Pexels License", "sha256": "...", "act": 1, "covers_scene_id": "S12",
      "duration_sec": 7.60, "width": 1920, "height": 1080,
      "eyeballed_content": "grey water of a river meeting the sound in cold light, no people",
      "qc": {"reviewed": true, "on_theme": true, "no_watermark": true,
             "no_recognizable_person": true, "no_cartoon": true, "label_matches_content": true, "notes": ""} }
  ],

  "overlay": [
    { "asset_id": "AF-PART-0044",
      "public_path": "kelo/overlay/AF-PART-0044__dust_motes.mp4",
      "type": "particle_assets", "subtype": "dust_motes", "license": "Pexels License",
      "sha256": "...", "blend_hint": "screen",
      "eyeballed_content": "slow drifting dust on black, loops cleanly",
      "qc": {"reviewed": true, "on_theme": true, "no_watermark": true, "notes": ""} }
  ]
}
```

## 3.2 Bがこのマニフェストから作るもの（**EP46 spec の cuts 割当**）

| マニフェスト | Bでの使い道 | spec |
|---|---|---|
| `stills[role="body"]` 85枚 | **静止画カット101本**（`kind:"img"`, `treatment` 循環）・**各≤2回** | still distinct85/cuts101 |
| body 静止画で `also_thumb==true` の6枚 | サムネ3案の背景（§11・6 asset ID） | — |
| `stills[role="i2v_source"]` 16枚 | **本編カットに出さない**（i2v 種・A が Wan で motion 化済み） | — |
| `motion` 16本 | **i2vカット32本**（`kind:"footage"`）・**各≤2回** | motion distinct16/cuts32 |
| `factory` 92本 | **実写カット92本**（`kind:"footage"`）・**各1回のみ** | factory distinct92/cuts92 |
| `overlay` 12本 | **`cuts[].src` に出さない**（§5.5 の合成レイヤー扱い） | — |

**合計 101 + 32 + 92 = 225 カット / distinct 85+16+92 = 193 / first-use 193/225 = 0.8578 ✓（floor 0.70）**

## 3.3 `scripts/check_kelo_asset_manifest.py`（消費側バリデータ・BLOCKING）

```bash
$PY scripts/check_kelo_asset_manifest.py --assets <path> [--json]
```

検査（1つでも違反で exit 1。`schema_version` 違いだけ exit 2・**A の `build_kelo_asset_manifest.py --verify` 不変条件と一字一致**）:

1. `schema_version=="kelo_assets.v1"` / `episode_id=="PD-2026-046-kelo"` / `slug=="kelo"` / `is_stub==false`
2. `counts.*` が各配列の実長と一致し**確定値**: `still_body==85` / `still_i2v_source==16` / `motion==16` / `factory==92` / `overlay==12`
   （`still_body` は `stills[role=="body"]` の実長、`still_i2v_source` は `stills[role=="i2v_source"]` の実長）
3. `role` は **`body`/`i2v_source`/`reject` の3値のみ**（`thumb`/`still_thumb` 等が現れたら FAIL）
4. `role=="body"` の全静止画で `public_path` 非null、かつ `remotion/public/<public_path>` と `<stem>_depth.png` が**両方実在**
   （`CaseFilm.depthSrcOf()=src.replace(/\.[^.]+$/,'_depth.png')`。**depth 欠落はレンダークラッシュ**）。`role=="i2v_source"` は `public_path==null`
5. `role!="reject"` の全静止画で `max(width,height)>=3840`（`preflight_render_gate.MIN_LONG_EDGE_PX=3840`）
6. `motion[].public_path` が `.mp4` で終わり `_rife` を含む。`motion[].source_scene_id` は `stills[role=="i2v_source"]` の種 ID（`M01_src` 系）を指す
7. `factory[].public_path` が `/factory/` を含む
8. `overlay[].public_path` が `/overlay/` を含み `/factory/` を**含まない**・`overlay` 配列長が**ちょうど12**
9. `sha256` が全配列を通して一意（**EP39〜45 の素材と sha256 被りゼロ**も別途 A が保証・B は自集合内一意を検査）
10. `factory[].eyeballed_content` が非空、かつ `qc.label_matches_content==true`
11. `qc.has_readable_text` / `qc.has_identifiable_face` / `qc.has_human_body` が true の項目は `role=="reject"`（**R1/R-FACE**）
12. `also_thumb==true` の body 静止画が**ちょうど6枚**、かつ **`scene_id` 集合が `{S01,S05,S30,S55,S72,S85}` と完全一致**
   （サムネ供給・§11。**A(CODEX_A §4.2/§4.3 不変条件) と B で also_thumb の scene_id 集合が同一**であることを検査＝**A↔B 契約点**。CODEX_A がこの6 ID を採らないなら組まずに止めて A に差し戻す）
13. **全文字列値**が §2 の R-FORBID / R-FACE / R-HOUSE / R-DOCHL / R-NUM / R-HEDGE を通る

> **★このバリデータは A の `--verify` と同じ不変条件を独立実装する（二重チェック）。** counts が §3.1 の確定値と食い違ったら組まずに止めて A に差し戻す（ブリーフ§2: still を増やして factory を削るな）。

---

# 4. narration_index（TTS は課金＝禁止。**実測版を消費**する）

## 4.1 なぜ narration_index か
`build_kelo_film.py` は**尺・区間・字幕を narration_index から導出する**。**秒数をコードに直書きしない。** 唯一の正は narration_index。

## 4.2 スキーマ（`kelo_narration.v1`）

```jsonc
{
  "schema_version": "kelo_narration.v1",
  "episode_id": "PD-2026-046-kelo",
  "is_stub": false,
  "total_seconds": 718.6,        // = SPEC narration_seconds（[DESIGNED SILENCE 1..3] の実音無音を含む）
  "chunks": [
    { "section": "HOOK", "start": 0.000, "end": 4.100, "text": "..." },
    { "section": "OP",   "start": 25.000, "end": 29.100, "text": "..." },
    { "section": "ACT_1","start": 55.000, "end": 59.200, "text": "..." }
  ]
}
```

**section 値（固定・5幕）:** `HOOK` / `OP` / `ACT_1` / `ACT_2` / `ACT_3` / `ENDING`。
（EP46 の BODY は 3幕＝ACT_1「The plan for the point」/ ACT_2「What "public use" means」/ ACT_3「The four who said no」。**ACT_4 は無い。**）
`build_kelo_film.py` は `section_windows()`（各 section の最初のチャンク start）で幕境界を得る。

**台本の `【DESIGNED SILENCE …】` は3箇所**（HOOK 1.8s＝完全無音／ACT3 1.5s＝完全無音／ENDING 2.2s＝音を足す沈黙）。narration_index の実測がこの無音を **total_seconds に内包**している。**存在しない演出マーカーを発明しない。**

## 4.3 spec のタイムライン（**設計目標。実タイミングは narration_index が上書きする**）

| section | 秒 | 備考 |
|---|---|---|
| HOOK | ~ | VO。末尾に `DESIGNED SILENCE 1.8s`（ピンクの家だけ・完全無音） |
| （deed-green `BrandOpening`） | 3.5 | 非VO。`OPENING_SEC`。**hookSeconds のフック後・narration の前に挿入**。card="THE LITTLE PINK HOUSE" |
| OP | ~ | 二人称の問い（thesis）＋ channel ID |
| ACT_1 The plan for the point | ~ | 最短・現在形。Pfizer→90エーカー→収用 |
| ACT_2 What "public use" means | ~ | 判例核・5-4・Stevens 多数・Kennedy 留保・Berman/Midkiff |
| ACT_3 The four who said no | ~ | 最長・情緒。O'Connor 逐語→Thomas。途中に `DESIGNED SILENCE 1.5s` |
| ENDING | ~ | ペイオフ→2009 Pfizer 離脱→>40州改革→移築されたピンクの家。途中に `DESIGNED SILENCE 2.2s` |
| （`BrandEndcard`） | 9.0 | 非VO。`ENDCARD_SEC` |

**唯一の正は `python scripts/check_script_length.py <script> --json`。** 総語数 **2,133**（spec `words_total`）/ `wpm 178.1` /
narration_seconds **718.6**（spec）。**自己申告・体感の尺判定は禁止。**

## 4.4 実測 narration_index の受領
本番は別工程が TTS→faster-whisper で `06_audio/narration_index.v001.json`（実測語タイム・`is_stub:false`）を作る。
**これは課金ジョブなので B は起動しない。** 来た `narration_index.v001.json` を `--narr` に渡すだけ。**台本本文はそのまま（改変しない）。**

---

# 5. `kelo_film.json` の構築（`scripts/build_kelo_film.py`＝`build_cleveland_film.py` の複製・実素材のみ）

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

- アセットのパスキーは **`src`**（`remotion/public/` からの相対、`staticFile()` 解決・A の `public_path` をそのまま）
- **カット単位の transition/motion は無い。** 動きは `treatment`・`seed`・`index%2`・`index%3` から導出
- `treatment` の実装値: `'depth'|'scan'|'duotone'|'focus'|'card'|'bleed'`（既定 bleed）
- `kind:'footage'` は `treatment` を無視して `<Footage>` を描画する
- **`fps = 30`**（EP44/45 と同じ film fps）。`narration = "kelo/narration.mp3"`（実在）

### 5.1.1 ★durationInFrames の4項関数（明示・total ≤ 752s を assert）

```
caseFilmDurationInFrames(keloFilm, fps=30)
  = round(hookSeconds * fps)        // hookSeconds = 8.0（EP43同型のフック montage 尺）→ round(240)=240
  + round(OPENING_SEC * fps)        // OPENING_SEC = 3.50（deed-green BrandOpening は hook の後）→ round(105)=105
  + ceil(narrationSeconds * fps)    // narrationSeconds = narration_index.total_seconds（= 718.6・silence 込み）→ ceil(21558.0)=21558
  + round(ENDCARD_SEC * fps)        // ENDCARD_SEC = 9.00 → round(270)=270
```

- **hookSeconds を明示: `hookSeconds = 8.0`**（ブリーフ§5・EP43 と同じ 8.0。**AEカード/BGM の offset = hook + 3.5 = 11.5 と一致必須**）。HOOK の VO は narrationSeconds に内包（フック montage の 8.0 は無音/hookLine の pre-roll）。
- 概算（fps30・narration 718.6）: `240 + 105 + 21558 + 270 = 22173 frames = 739.10s`。**id=Ep46Kelo の durationInFrames は 22173。**
- **ビルダ末尾で `assert total_frames/fps <= 752.0`**（739.10 ≤ 752 ✓・750 も下回る）。超えたら exit 1。

## 5.2 カット構成（**§3 マニフェストから機械的に組む・紙芝居回避が最優先**）

```
総カット 225 = factory 92 (footage) + motion 32 (footage) + 静止画 101 (img)

[A] first-use share（check_asset_reuse floor 0.70）
    distinct 92+16+85 = 193 → 193/225 = 0.8578            ✓ >=0.70（spec first_use_share と一致）

[B] per-asset cap（check_asset_reuse）
    factory: 92/92  = 1.00回  ✓ <=1（★factory は再使用禁止）
    motion : 32/16  = 2.00回  ✓ <=2
    still  : 101/85 = 1.188回 ✓ <=2

[C] animation_mix（★2つの尺度を両方満たす）
    (i) cut数ベース   still-share = 101/225 = 0.4489        ✓ <=0.45（★余裕が薄い＝下の警告）
        motion coverage = (92+32)/225 = 124/225 = 0.5511   ✓ >=0.45（spec と一致）
    (ii) frame ベース still 平均 3.00s → 101×3.00 = 303.0s
        footage 平均 ~3.352s → 124×3.352 ≈ 415.6s
        still-frame-share = 303.0 / 718.6 = 0.4217          ✓ <=0.45（cut数比より安全側）
        motion-coverage(frame) = 415.6 / 718.6 = 0.5783     ✓ >=0.45

[D] 平均ショット長（spec mean_shot 3.19 / max 6.0）
    718.6 / 225 = 3.194 秒/カット                           ✓ <=6

[E] factory 下限（30秒に1本 = 24 → >=24本） 92本            ✓
```

> **★[C](i) の cut数ベース still-share 0.4489 は cap 0.45 に薄い（余裕 0.11%）。still を1枚増やすか factory を1本削ると 0.45 を超える。**
> **マニフェストが still 85 / factory 92 / motion 16 を割ったら組まずに止めて A に差し戻す（ブリーフ§2: still を増やして factory を削るな）。**
> **frame ベースも下回るよう、still の平均尺を footage より系統的に短く保つ（§5.3-5）。**

## 5.3 カット割り当てのルール（`build_cleveland_film.py` の `allocate()`/`tile_window()` を踏襲）

1. 各幕の秒窓を `section_windows()` から取り、幕内に **factory : motion : still を按分**して配置
   （★下表は**非拘束の目安**。実配分は narration_index の窓長で自動調整。確定値は「合計 factory 92 / motion 32 / still 101」だけ）:

   | section | factory | motion | still | 小計 |
   |---|---|---|---|---|
   | HOOK+OP | 9 | 4 | 15 | 28 |
   | ACT_1 | 15 | 6 | 18 | 39 |
   | ACT_2 | 24 | 8 | 24 | 56 |
   | ACT_3 | 24 | 8 | 24 | 56 |
   | ENDING | 20 | 6 | 20 | 46 |
   | **計** | **92** | **32** | **101** | **225** |

2. **factory は各1回のみ**（使用済み集合を持ち二度と引かない）。**motion は各≤2回・still は各≤2回**（`allocate(cap=…)`）
3. **同一素材を連続させない**（順序を散らす）
4. 静止画 `treatment` は `["depth","scan","duotone","focus"]` を循環（同じ treatment を3連続させない）
5. **still の `dur` を footage の `dur` より系統的に短く**（§5.2[C]。`tile_window` の重みで still 側を小さめに）
6. motion の `dur` は **3.0–3.4秒**（実素材 3.417s。超えるとループが見える）
7. **AEカードの区間（§7.2）に重なるカットも存在させる**（コンポジタ SKIP 時に穴が空かないため）

## 5.4 `figures[]` と `captions[]`
- `figures[]` は §6（**36本**・spec floor 30 に +6・`graphics[]=[]`・**dochighlight 不使用**）
- `captions[]` は narration_index の全チャンクを **verbatim**（`build_captions()` と同一）。SRT も同時出力

## 5.5 合成レイヤー（`overlay`）— **`cuts[].src` に出さない**
`overlay` 12本は「加工」。`cuts[].src` に入れると `kind_of()` が factory 判定（上限1回）になり FAIL する。
`kelo_film.json` に **`overlays` 独自キー**で持たせる（`CaseFilm` は未知キーを無視）か、専用レイヤーで `screen` 合成する。

## 5.6 ビルダが出力する成果物（**asset_map→provenance変換＋beatsheet生成**）

| 出力 | パス |
|---|---|
| film.json | `remotion/src/data/kelo_film.json` |
| public コピー | `remotion/public/kelo/film_data.v001.json` |
| **build provenance**（asset_map→provenance変換） | `episodes/PD-2026-046-kelo/04_scenes/kelo_build_manifest.v001.json`（**A の `05_visuals/asset_manifest` に書かない**） |
| **beatsheet**（figures+AE区間の突き合わせ表） | `episodes/PD-2026-046-kelo/04_scenes/kelo_beatsheet.v001.json` |
| SRT（字幕未生成時のフォールバック） | `episodes/PD-2026-046-kelo/08_edit/captions.final.v001.srt`（**§8 の生成器が上書きする**） |

> **★beatsheet の命名に関する重大な注意:** `check_motion_density` / `check_animation_mix` は
> `04_scenes/premium_beatsheet.v*.json` を**自動検出して film.json より優先**する。
> **B の beatsheet は `kelo_beatsheet.v001.json`（`premium_` を付けない）** にして、**ゲートの測定源を film.json 一本に保つ**
> （二重ソースの乖離＝EP39/40 の矛盾28件の原因を避ける）。`kelo_beatsheet` は provenance と `validate_kelo_beats` 専用。

## 5.7 CLI
```bash
$PY scripts/build_kelo_film.py \
  --assets episodes/PD-2026-046-kelo/05_visuals/asset_manifest.v001.json \
  --narr   episodes/PD-2026-046-kelo/06_audio/narration_index.v001.json \
  --out    remotion/src/data/kelo_film.json \
  [--captions episodes/PD-2026-046-kelo/08_edit/captions.final.v001.srt]
```
**実素材のみ。`is_stub==true` のマニフェストを渡されたら exit 1（このスレッドは stub を使わない）。** 末尾に `check_asset_reuse` 相当の自己レポートを print する。

---

# 6. Remotion 側 `figures[]`（**36本・spec floor 30 に +6・`graphics[]=[]`・dochighlight 不使用**）

## 6.1 密度の検算（`check_motion_density`・**AEカードは1本も数えられない**）

```
figures 36本（film.json） / body 11.977分(=718.6/60) = 3.006 /分     ✓ beats_per_min_floor 2.5
coverage: 36本 × 平均6.0s = 216.0s / 718.6 = 30.1%                    ✓ MIN_ANIMATED_COVERAGE 0.25
variety : 下記 kind を13種使用                                        ✓ variety_floor 3
spec motion.beats_floor = 30 に対し 36 で余裕。coverage が最も薄いので figures の dur は 5.4–6.0s を基本に。
```

> **★3軸すべて AND。density/coverage/variety のどれか1つでも floor 未満で FAIL。**
> 36本を非重複で置き、平均 dur を 6.0s 程度に確保すること（coverage が floor 0.25 に一番近い）。

## 6.2 ★★★ `FigureSpec` の `kind` は**実在する小文字値のみ・`dochighlight` は使わない** ★★★

> **大文字名（`ActTitle`/`QuoteCard`/`VoteTally`…）は `FigureBeats.tsx` の union に無く、無言で描画が消える。**
> **`comparebars` は存在しない → `compbars` を使う。** 5-4 は **`votetally`（`majority:number, dissent:number`）**。
> **★`dochighlight` を1本も使わない**（黒バー/box/underline がバグに見える＝3回指摘・R-DOCHL）。判読ハイライトの意図は `quote`/`stat`/`lowerthird`/`kinetic` で代替する。

**EP46 で使う実在 `kind`（`remotion/src/components/FigureBeats.tsx` の union から。全て `start`/`end` 必須・全小文字）:**

| `kind` | 必須プロパティ | EP46での用途 |
|---|---|---|
| `numberticker` | `value:number` / `label?` / `prefix?` `suffix?` `decimals?` | ~115 PROPERTIES（F12）/ OVER 1,000 JOBS LOST（F15） |
| `stat` | `value:number` / `label:string` / `prefix?` `suffix?` `topLabel?` | $300 MILLION（F11・Pfizer）/ 90 ACRES（F10）/ 2005（F02）/ MORE THAN 40 STATES（F18・"more than" ヘッジ） |
| `timeline` | `events:{year:string;text:string}[]` | ①案件: 1997 購入→1990s distressed→Pfizer→NLDC 90エーカー→condemnation ②先例: 1954 Berman→1984 Midkiff→2005 Kelo ③後日談: 2005 判決→2009 Pfizer 離脱→2011 更地/瓦礫→>40州改革 |
| `quote` | `quote:string` / `attribution:string` | O'Connor 逐語（F07・F08・**dissenting**）/ Thomas（F09・**dissenting**）（**帰属必須**・R-QUOTE） |
| `kinetic` | `lines:string[]` / `style?:'wordpop'\|'maskslide'\|'emphasis'` / `emphasisWords?` | "CAN THE GOVERNMENT TAKE YOUR HOME?" / "PUBLIC USE → PUBLIC PURPOSE"（F04）/ "THE DISSENT LOST. THE CITY WON."（emphasisWords は1–2語） |
| `lowerthird` | `primary:string` / `secondary?` / `accent?` | 開示 `AI-assisted visualization` / Kelo v. City of New London, 545 U.S. 469 (2005)（F02）/ Justice Stevens, for the majority（F03）/ Fifth Amendment "public use" / Institute for Justice（F14）/ O'Connor dissent, joined by Rehnquist, Scalia, Thomas（F06）/ Justice Thomas, separate dissent |
| `acttitle` | `title:string` / `kicker?` / `index?` | 幕頭「THE PLAN FOR THE POINT」/「WHAT PUBLIC USE MEANS」/「THE FOUR WHO SAID NO」 |
| `compbars` | `data:{label:string;value:number}[]` | ①REAL PUBLIC USE（road/school/base）vs THIS PLAN（offices/hotel/private）②Motel 6 vs Ritz-Carlton / home vs shopping mall / farm vs factory（F07）③PROMISED（thousands of jobs, millions in taxes）vs BUILT: NOTHING（F16） |
| `bar` | `data:{label:string;value:number}[]` | ①約束された雇用/税収が上へ climb（ACT1）②O'Connor「from those with fewer resources to those with more」（F08・受益偏在） |
| `mechanism` | `mechanism:'closingdoor'\|'gears'\|'faultsplit'` ★discriminant は `kind`・変種は `mechanism` | ①economic-development machine（gears・F04）②Kennedy の残した扉＝pretextual 収用は依然禁止（faultsplit・F05）③condemnation over all property（closingdoor・F07） |
| `votetally` | `majority:number` / `dissent:number` / `label?` | **5 – 4 UPHELD（`majority:5, dissent:4`, label "THE TAKING STANDS"）**（F01・C-1） |
| `pindropmap` | `pins:{x,y,label?}[]` | New London, Connecticut（単一ピン・C-4 顔なし・F13） |
| `regionmap` | `label?` / `regions[]` | ">40 states" 収用改革の地理（F18・"more than forty" ヘッジ） |

**`quote[].attribution` は §2 の `APPROVED_QUOTES` に一致させる。逐語のみ・要約を引用符に入れない・O'Connor/Thomas＝`dissenting`。**
**★`kind` に `dochighlight` を1件も置かない（R-DOCHL・`check_kelo_facts` が grep で 0 を確認）。**

## 6.3 figures 配分（★DESIGN と一致・全 36 を figures[]・graphics[]=[]）

| kind | 枠数 |
|---|---|
| `acttitle` | 3 |
| `lowerthird` | 8 |
| `stat` | 4 |
| `numberticker` | 2 |
| `timeline` | 3 |
| `quote` | 3 |
| `compbars` | 2 |
| `mechanism` | 3 |
| `bar` | 2 |
| `votetally` | 1 |
| `pindropmap` | 1 |
| `regionmap` | 1 |
| `kinetic` | 3 |
| **合計** | **36**（variety = 13 種・**dochighlight を含めない**） |

> **★実装表現:** 上記 36本を**すべて `figures[]`** に入れ、**`graphics[]=[]`** にする（`check_motion_density` は `figures+graphics+heroCuts` を合算するので密度は同値・floor 30 に +6）。film.json 上は全 36 が figures[]・graphics[] は空配列。

## 6.4 figures アンカー設計（`build_cleveland_film.py` の `FIGURE_ANCHORS` 方式）

**方式:** `(anchor_sec, payload)` の配列を秒昇順に置き、`build_figures()` が
`end = min(anchor+FIG_DUR, next_anchor-FIG_GAP, total-0.5)` でクランプ、`end-start < FIG_MIN_DUR` なら **exit 1**。
`FIG_DUR=6.0 / FIG_MIN_DUR=3.0 / FIG_GAP=0.4`。**アンカー秒は narration_index の section 窓に対する相対で決め、`section_windows()` を基準にオフセットで置く**（秒直書き禁止）。

**配置方針（36本・§2 台帳の値だけを焼く・kind を分散して variety を稼ぐ・6制約順守・dochighlight 不使用）:**

- **HOOK/OP（4）:** `lowerthird`（`AI-assisted visualization` 開示）/ `lowerthird`（**F02 Kelo v. City of New London, 545 U.S. 469 (2005)**）/ `pindropmap`（**F13 New London, Connecticut**・単一ピン）/ `kinetic`（"CAN THE GOVERNMENT TAKE YOUR HOME?"）
- **ACT_1（8）:** `acttitle`（THE PLAN FOR THE POINT）/ `stat`（**F11 $300**, suffix " MILLION", label "Pfizer research headquarters"）/ `stat`（**F10 90**, suffix " ACRES", label "the Fort Trumbull plan"）/ `numberticker`（**F12 ~115** PROPERTIES）/ `timeline`（**F13/F20/F11/F10** 案件: 1997 購入→1990s distressed→Pfizer→NLDC 90エーカー→condemnation）/ `mechanism:gears`（economic-development machine・F04）/ `lowerthird`（**F14 Institute for Justice**・原告代理）/ `bar`（PROMISED: thousands of jobs / millions in taxes が上へ climb）
- **ACT_2（9）:** `acttitle`（WHAT PUBLIC USE MEANS）/ `lowerthird`（**Fifth Amendment · "public use"**）/ `lowerthird`（**F03 Justice Stevens, for the majority** — Kennedy, Souter, Ginsburg, Breyer joined）/ `compbars`（REAL PUBLIC USE: road/school/base vs THIS PLAN: offices/hotel/private・C-2）/ `timeline`（**F19** 先例: 1954 Berman→1984 Midkiff→2005 Kelo）/ `kinetic`（"PUBLIC USE → PUBLIC PURPOSE"・emphasisWords=["PURPOSE"]・**F04**）/ `votetally`（**F01 majority:5, dissent:4**, label "THE TAKING STANDS — UPHELD"・**C-1**）/ `stat`（**F02 2005**, label "the Supreme Court agreed"）/ `mechanism:faultsplit`（**F05** Kennedy の扉＝pretextual/trivial/implausible 収用は依然禁止）
- **ACT_3（10）:** `acttitle`（THE FOUR WHO SAID NO）/ `lowerthird`（**F06 O'Connor dissent** — joined by Rehnquist, Scalia, Thomas）/ `quote`（"Nothing is to prevent the State from replacing any Motel 6 with a Ritz-Carlton, any home with a shopping mall, or any farm with a factory" → "Justice O'Connor, dissenting"・**F07・R-QUOTE**）/ `compbars`（Motel 6 vs Ritz-Carlton / home vs shopping mall / farm vs factory・**F07**）/ `quote`（"The beneficiaries are likely to be those citizens with disproportionate influence and power in the political process, including large corporations and development firms" → "Justice O'Connor, dissenting"・**F08**）/ `bar`（property "from those with fewer resources to those with more"・**F08**・尊厳保持）/ `mechanism:closingdoor`（"the specter of condemnation hangs over all property"・**F07**）/ `lowerthird`（**F09 Justice Thomas, separate dissent** — originalism）/ `quote`（"use by the public" → "Justice Thomas, dissenting"・**F09・R-QUOTE**）/ `kinetic`（"THE DISSENT LOST. THE CITY WON."・**C-1 UPHELD**・emphasisWords=["WON"]）
- **ENDING（5）:** `kinetic`（"NOTHING BUILT"・emphasisWords=["NOTHING"]・**F16**）/ `compbars`（PROMISED: jobs · taxes vs BUILT: NOTHING・**F16**）/ `numberticker`（**F15 1000**, prefix "OVER ", suffix " JOBS LEFT WITH PFIZER, 2009"）/ `timeline`（**F16/F15/F18** 後日談: 2005 判決→2009 Pfizer 離脱→2011 更地/瓦礫→"more than 40 states" 改革）/ `stat`（**F18 40**, prefix "MORE THAN ", suffix " STATES", label "reformed eminent domain"・**R-HEDGE**）

> **★C-1（UPHELD）を出す payload には必ず "STANDS"/"UPHELD"/"the city could"/"allowed" 系を同梱。「the taking was illegal」「the court struck down」を書かない。**
> **O'Connor / Thomas 逐語は `attribution` に "dissenting" を持つ（C-3・R-QUOTE）。多数意見の逐語は "for the majority"。**
> **F18（40 states）は "MORE THAN"/"OVER" のヘッジを同一 payload に（C-6・R-HEDGE）。43/44/45/47 を焼かない。**
> **★988 を figures に置かない（このエピソードは Institute for Justice 記録／州 eminent-domain リソース・description のみ）。**

## 6.5 配置ルール
1. **AEの区間（§7.2）と1秒でも重ならない**（`validate_kelo_beats` が突き合わせ）
2. **同じ kind を連続させない**（`quote` の直後に `quote` を置かない・`mechanism` の直後に `mechanism` を置かない）
3. 1枠 **5.4–6.0秒**
4. `quote[].quote` / `kinetic[].lines` / `*.label` / `votetally` は §2 の R-NUM・R-QUOTE・R-FORBID・R-DISPO・R-DOCTRINE・R-HEDGE・R-FACE・R-HOUSE・R-DOCHL 検査対象
5. 台帳外の数値を `value`/`majority`/`dissent`/`numKeys` に置かない（**焼いたら R-NUM で FAIL**）
6. **`emphasisWords` は1–2語の短句のみ**（長句は AE/Remotion で末尾が切れる＝EP40 実害）
7. **`kind` に `dochighlight` を1件も置かない（R-DOCHL）**

---

# 7. After Effects カード（`build_kelo_hero_cards.py` / `composite_kelo_hero.py`）

## 7.1 位置づけ
AEカードは **film.json とは別**に ffmpeg で本編に焼き込む（§0.5-2＝密度に数えられない）。
`build_cleveland_hero_cards.py`（／`build_caniglia_hero_cards.py`）を**コピーしてパス・定数・CARDS デッキだけ差し替える**。レイアウト実装・
`money_keys()`・`fit_size()`・完了マーカー・機械の罠対処は**1行も削らない**。

## 7.2 AEカードデッキ（**単調増加・重複ゼロ・台帳裏付けのみ・6制約順守。この表が契約。8枚**）

**区間の秒は本番の rendered base（narration_index 由来）に一致させる。** 下表の秒は spec タイムライン基準の**目安**で、
`build_kelo_hero_cards.py` は section 窓からオフセットで算出しクランプする。**背景静止画は象徴オブジェのみ（R1/C-4・Kelo 顔なし）。**
**★この表は DESIGN §6 と id・レイアウト・F-ID・順序（start 昇順）が一字一致（ブリーフ§6 表 VERBATIM）。** 988 は AEデッキに入れない。

| id | レイアウト（**実装済み集合・§7.3**） | hero/main（主表示） | top / bottom / attribution | F-ID | 背景（象徴のみ） | required |
|---|---|---|---|---|---|---|
| date01 | DATE_STAMP | **2005 · SUPREME COURT** | place: **KELO v. CITY OF NEW LONDON · 545 U.S. 469** | F02 | 大理石の最高裁列柱（顔なし） | 必須 |
| pp01 | SPLIT_COMPARE | left: **PUBLIC USE** / right: **PUBLIC PURPOSE** | top: **THE DOCTRINAL MOVE** / bottom: **ECONOMIC DEVELOPMENT CAN COUNT AS A PUBLIC PURPOSE** | F04 | Fifth Amendment のテキスト（判読困難）／列柱 | 必須 |
| vote01 | VOTE_SPLIT | **5 – 4** | top: **THE TAKING STANDS** / bottom: **THE COURT SAID THE CITY COULD** | F01 | 分割した法廷／木槌（顔なし） | 必須 |
| oc01 | QUOTE_CARD | **"NOTHING IS TO PREVENT THE STATE FROM REPLACING ANY MOTEL 6 WITH A RITZ-CARLTON, ANY HOME WITH A SHOPPING MALL, OR ANY FARM WITH A FACTORY"** | attribution: **JUSTICE O'CONNOR, DISSENTING** | F07 | Motel 6 の看板が高級ホテルへ溶暗（顔なし） | 必須 |
| th01 | CENTER_STACK | **USE BY THE PUBLIC** | top: **THE ORIGINAL MEANING** / bottom: **JUSTICE THOMAS, DISSENTING** | F09 | 古い公共広場／原意主義のテキスト（顔なし） | 必須 |
| nb01 | CENTER_STACK | **NOTHING BUILT** | top: **WHAT ROSE ON THE CLEARED LAND** / bottom: **THE LAND SAT EMPTY** | F16 | 雑草の生えた更地（顔なし） | 必須 |
| st01 | CENTER_STACK | **MORE THAN 40 STATES** | top: **THE BACKLASH** / bottom: **REFORMED EMINENT DOMAIN** | F18 | 州法令集の背（判読不能） | 必須 |
| pink01 | ACT_TITLE_CARD | **THE LITTLE PINK HOUSE** | kicker: **SAVED, AND MOVED** | F17 | 家をフラットベッドに載せて別の通りへ移築（顔なし） | 必須 |

> **★行順＝start 昇順（時系列）:** `date01`(ACT2) < `pp01`(ACT2) < `vote01`(ACT2) < `oc01`(ACT3) < `th01`(ACT3) < `nb01`(END) < `st01`(END) < `pink01`(END)。
> **vote01 の "5 – 4"（F01）は「THE TAKING STANDS」＋「THE COURT SAID THE CITY COULD」（UPHELD・C-1）を削除禁止**（違法/struck down と読ませない）。
> **pp01 は "PUBLIC USE → PUBLIC PURPOSE"（C-2・過大化しない）。**
> **oc01 の quote は逐語のみ**（§2 `APPROVED_QUOTES` と一致・要約を引用符に入れない）・attribution **JUSTICE O'CONNOR, DISSENTING**（Court に帰属させない・C-3）。
> **th01 は Thomas＝dissenting（C-3）。** **st01 の "MORE THAN 40 STATES" ヘッジを削除禁止**（C-6・R-HEDGE・断定数にしない）。
> **pink01 は移築のモチーフ（"SAVED, AND MOVED"）。"demolished" と書かない（C-4・R-HOUSE）。**
> **どのカードにも「the taking was illegal」「the court struck it down」「the government can take any home for any reason」を書かない**（C-1/C-2）。数値ID＝台帳（§2.2）と一致必須。カウント終了から区間終端まで最低 **1.20秒**ホールド。accent は全カード deed-green `#3F8F5F`。

**検算（Codex は自分で再計算して一致を確認）:** 8区間・単調増加・重複ゼロ・HOOK と ENDCARD（末尾9s）に重ねない。
Remotion figures(§6) と1秒も重ならない（`validate_kelo_beats` が検査）。

## 7.3 レイアウト（`build_cleveland_hero_cards.py`／`build_caniglia_hero_cards.py` の実装を踏襲・**実装済みレイアウト名だけを使う**）
複製元が実装するレイアウトは**この8種**:
`DATE_STAMP` / `CENTER_STACK` / `MONEY_STACK` / `SPLIT_COMPARE` / `ACT_TITLE_CARD` / `QUOTE_CARD` / `VOTE_SPLIT` / `SEAM_TRANSITION`。
**§7.2 デッキが使うのは 6種**（`DATE_STAMP` / `SPLIT_COMPARE` / `VOTE_SPLIT` / `QUOTE_CARD` / `CENTER_STACK` / `ACT_TITLE_CARD`）。
**★`VOTE_SPLIT` は使う**（5-4 は台帳 F01 の検証済み値＝捏造でない・C-1 UPHELD 枠を併記）。**`MONEY_STACK` / `SEAM_TRANSITION` は本 EP では未使用**。
**上記6種以外のレイアウト名を発明しない（`validate_kelo_beats` §7.9 ルール3 で FAIL）。dochighlight をレイアウト名に使わない。**
**共通レイヤースタック・Anton/Oswald・`psName()` の runtime 解決（allFonts の array-LIKE ラッパーを unwrap）は複製元と同一。**

**★共通レイヤースタックに AI開示レイヤーを1枚追加（R1・全カード常時焼き）:** 最上位に近い固定レイヤーとして
`AI-assisted visualization`（Oswald 20px / SILVER `#C8CDD6` / opacity 70% / 右下 `[W-32, H-28]`）を全カードに焼く。
AEカードは不透明の全画面 mp4 として本編に overlay されるため、これが無いと本編(Remotion)右下の開示が隠れる（**R1 違反**）。字幕帯とは縦56px 以上離す。

**★EP46 色定数（0..1 float・deed-green レーン色。EP41 gold / EP42 blue / EP43 amber / EP44 teal / EP45 crimson を流用禁止・DESIGN と一致）:**
```python
ACCENT = [0.247, 0.561, 0.373]  # #3F8F5F deed-green（土地・権利証・"greenlight"）アクセント（数値・下線・レーン分離）
WHITE  = [0.961, 0.969, 0.980]  # #F5F7FA
SILVER = [0.784, 0.804, 0.839]  # #C8CDD6（開示テキスト）
INK    = [0.039, 0.039, 0.047]  # #0A0A0C 近黒ルート（サムネ bg と一致）
```
> **accent は必ず `#3F8F5F`（他話色を書かない）。** サムネ・OP props・AEカードの accent は全て `#3F8F5F`。

**数値カードは全て `money_keys()` 系で表示文字列を Python 事前計算**（JSX で算術しない＝EP38 確定ルール）。
**`vote01`（5 – 4）は "5" と "4" を別レイヤー（改行禁止・`ADBE Rotate Z` で分割）。`pp01`（PUBLIC USE / PUBLIC PURPOSE）は左右2値を別レイヤー。`th01` は "USE BY THE PUBLIC" と "JUSTICE THOMAS, DISSENTING" を別レイヤー。**
**`nb01`（NOTHING BUILT）／`st01`（MORE THAN 40 STATES）は主表示とサブを別レイヤー。**

## 7.4 `beats.json` スキーマ（本番 `08_edit/ae_hero/beats.json`）
複製元の beats スキーマに準拠。トップに **`film_offset_sec = 11.5`**（= hookSeconds 8.0 + OPENING_SEC 3.5・本編ナレ開始からのオフセット・§7.10 のコンポジタが読む）。各 beat に `id` / `layout` / `start` / `end` / `dur` /
`still`(象徴 or null) / `hero`/`main`(主表示文字列) / `top` / `bottom` / `left` / `right` / `kicker` / `place` / `caption`(**改行禁止・最大50字**) /
`value` / `numKeys` / `blend_mode`(既定 "overlay") / `required` / `out` / `attribution`(**QUOTE_CARD=oc01 は必須**・§2 `APPROVED_QUOTES` と一致・R-QUOTE)。
**`value` / `main` / `hero` の数値は §2 台帳の `verified:true` 値のみ**（`check_kelo_facts` が照合）。
**`vote01` は UPHELD 枠（"THE TAKING STANDS" / "THE COURT SAID THE CITY COULD"）を持つ（R-DISPO）。`st01` は "MORE THAN" ヘッジを持つ（R-HEDGE）。`beats.json` に `dochighlight` を出さない（R-DOCHL）。**

## 7.5 このマシン固有の罠（複製元が対処済み。**1つも省くな**）
1. `setTemporalEaseAtKey` の配列次元は **spatial(Position) で 1**（`if(!prop.isSpatial){...}` で分岐）
2. RS = **`"最良設定"`** / OM = **`"H.264 - レンダリング設定を一致 - 15 Mbps"`**（英語名は try/catch フォールバックのみ）
3. TextDocument の改行は `\n` 不可。**`caption` は1行**（改行が要るなら別レイヤー・SPLIT_COMPARE の左右2値は別レイヤー）。**テキスト幅は `sourceRectAtTime(t,false).width` で実測**（advance-width 推定は禁止＝EP40 の文字切れ原因）。em-dash は `-`／en-dash（5 – 4）はレイアウトで別レイヤー
4. `app.newProject()` は headless でハング。**使わず**同名 `KELO_` コンプを防御削除
5. ビルドは**カード8枚で ~100–120秒**。`render/_build_ok.txt` をポーリング（**タイムアウト最低300秒**）
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
$PY scripts/ae/build_kelo_hero_cards.py
"C:/Program Files/Adobe/Adobe After Effects 2026/Support Files/AfterFX.exe" -noui \
  -r ".../episodes/PD-2026-046-kelo/08_edit/ae_hero/kelo_hero.jsx"
# render/_build_ok.txt を待つ（最大300秒）→ render/*.mp4 が8本揃うまで待つ（最大1200秒）
$PY scripts/ae/composite_kelo_hero.py
```

## 7.9 `scripts/validate_kelo_beats.py`（BLOCKING）
1. `beats[].start` 昇順・区間非重複
2. 全 `start`/`end` が本編ナレ区間内（HOOK と ENDCARD 末尾9s に重ねない）
3. `layout` が §7.3 の**実装済み6種**（`DATE_STAMP`/`SPLIT_COMPARE`/`VOTE_SPLIT`/`QUOTE_CARD`/`CENTER_STACK`/`ACT_TITLE_CARD`）のいずれか。**この6種以外（`MONEY_STACK`/`SEAM_TRANSITION`/`dochighlight` 等）は FAIL。** still が必要なレイアウトで null なら FAIL
4. `still` 非null は実在＋長辺 >=3840px
5. `hero`/`main`/`top`/`bottom`/`left`/`right`/`caption`/`value` が §2（R-FORBID/R-NUM/R-QUOTE/R-DISPO/R-DOCTRINE/R-HEDGE/R-FACE/R-HOUSE/R-DOCHL/R-DATE）を通る
6. `verified:false` の値を要求するカードは `required:false` で**除外**、`required:true` なら exit 1
7. **`kelo_film.json` の `figures[]`（§6）と AE の区間が1秒でも重ならない**
8. `caption` に改行が含まれない
9. **AI開示レイヤーの存在（R1）** — ビルダが全カード共通スタックに `AI-assisted visualization`（右下・§7.3）を焼く設定であることを静的に確認。無ければ FAIL。受入アイボール（§13.1）でも「AEカード表示中も右下の開示が見える」を確認
10. **`dochighlight`/`DOCHIGHLIGHT` が beats/レイアウト名に1件も無い（R-DOCHL）**

## 7.10 基底 mp4 とコンポジタ（`build_kelo_bgm_real.py` → `composite_kelo_hero.py`）
```
# 完成後の合成順（ブリーフ§5）: build_kelo_bgm_real.py（narration+BGM・OFF=hook+3.5=11.5）→ composite_kelo_hero.py（AEカード焼込み・film_offset_sec 適用）
BASE = episodes/PD-2026-046-kelo/08_edit/kelo_final_bgm.v002.mp4     # build_kelo_bgm_real.py が生成
OUT  = episodes/PD-2026-046-kelo/08_edit/kelo_final_bgm.v003_ae.mp4  # composite_kelo_hero.py が生成
FFMPEG  = C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe
FFPROBE = C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffprobe.exe
W,H,FPS = 1920, 1080, 30
```
**`build_kelo_bgm_real.py`（EP43 `build_caniglia_bgm_real.py` の複製）は `OFF = hookSeconds + 3.5 = 11.5` でナレをレイアウトする**（フック montage 8.0 + BrandOpening 3.5 の後にナレ開始）。
**`composite_kelo_hero.py`（EP43 `composite_caniglia_hero.py` の複製）は `beats.json` の `film_offset_sec`（= 11.5）を読み、各 beat 区間を本編尺にマップする**。
**SKIP4条件を1行も削らない:** ① `render/<id>.mp4` 不在 ② 解像度 != 1920x1080 ③ 実測尺 `< dur-0.3` ④ `film_offset_sec + beat.end > base_dur`。
SKIP された区間は元カットのまま残る（作品は壊れない）。**何枚 SKIP したかを stderr に必ず出す。**
ffmpeg は `overlay=0:0:eof_action=pass:enable='between(t,start,end)'`（`blend_mode` が screen/multiply の時のみ `blend`）。
**出力後 `probe_dur(OUT)` でベースとの尺差 <=0.5秒を確認。出荷済みは絶対に上書きしない（必ず `_v003_ae`）。**

---

# 8. 字幕の切断規則（`scripts/gen_captions_kelo.py`＝`gen_captions_cleveland.py` の複製）

## 8.1 原則
**文字数は「上限」であって「分割基準」ではない。** `gen_captions_cleveland.py` の `internal_split()` / `chunk_sentence()` を**そのままコピー**。
`from fix_caption_dangling import NO_DANGLE_END, wrap as safe_wrap`（**語リストを自前で書き直さない**）。

## 8.2 通すゲート `scripts/check_caption_breaks.py`（**閾値を緩めるの禁止**）
- **A. 行末の機能語**（複数行キューの最終行以外が句読点なしで `NO_DANGLE_END` の語で終わる）= 0件
- **B. 孤立キュー**（語数<3 で「終端句読点で終わる」「大文字で始まる」の両方を満たさない）= 0件
- **C. 句をまたぐ切断(hard)** = 0件
- A/B/C いずれか1件で FAIL（**実質ゼロ許容**）

## 8.3 EP46 の入力と対応
- 入力は **narration_index の各チャンク文**（`--narr`）。**字幕テキストは台本本文と1:1対応**（§0.5-5）。台詞・別エピソード文の混入禁止。verbatim で使い、構文境界で分割するだけ。
- `ABBR` に `U.S.` / `v.` / `Mr.` / `Ms.` / `No.` / `St.` 等を持つ（`Kelo v. City of New London` の `v.`、`545 U.S. 469` の `U.S.`、`Motel 6`／`36 Franklin St.` で文を切らない）。
- タイミングは narration_index の start/end。CPS <=27・最小表示 0.90秒。**Step で決めた境界を時間都合で動かさない。**
- **字幕にも R-FORBID 適用**（台本本文に断定禁止語は無いので verbatim なら自然に通る。§2.1 の注意：否定/正確文脈の近似語＝`was illegal`/`struck something down`/`for any reason it likes` を禁止語に足さない）。

## 8.4 セルフテスト（`--selftest`・EP38 実害を回帰に）
`Kelo v. City of New London` / `545 U.S. 469` / `Motel 6` / `36 Franklin St.` で文が切れないこと、
機能語で終わるキュー・孤立キューを作らないことを含む4ケースを実装し、
**出力を `check_caption_breaks.py` に食わせて exit 0 まで自動確認。**

## 8.5 実行
```bash
$PY scripts/gen_captions_kelo.py --narr episodes/PD-2026-046-kelo/06_audio/narration_index.v001.json
$PY scripts/check_caption_breaks.py episodes/PD-2026-046-kelo/08_edit/captions.final.v001.srt
# → PASS が出るまで直す。ゲート側の閾値を緩めるのは禁止。
```

---

# 9. 5ゲートの実際の判定（**build 後に必ず全部通す・animation_mix を忘れるな**）

| ゲート | 実体 | 入力 | EP46 の通過根拠 |
|---|---|---|---|
| `check_asset_reuse.py <film.json>` | factory≤1 / motion≤2 / still≤2 / first-use≥0.70 | **film.json 位置引数** | §5.2: factory1.00 / motion2.00 / still1.19 / first-use **0.8578** |
| `check_motion_density.py --ep PD-2026-046-kelo` | film.json の graphics+figures+heroCuts のみ / density≥2.5・coverage≥0.25・variety≥3（**AND**） | **`--ep`** | §6.1: **3.006 / 30.1% / 13種**（AEカードは0本＝§0.5-2・beats≥30） |
| `check_animation_mix.py --ep PD-2026-046-kelo` | film.json の cuts を img=still/その他=footage 分類 / still-share≤0.45・motion-cov≥0.45 | **`--ep`** | §5.2[C]: still-share **0.4489(cut)/0.4217(frame)** / motion-cov **0.5511+** |
| `check_caption_breaks.py <srt>` | A/B/C 各0件 | **srt 位置引数** | §8 の構文境界生成器 |
| `check_script_length.py <script> --json` | 総語数 / wpm / narration_seconds | **script 位置引数** | 2,133語 / wpm178.1 / **718.6s** |

> **★ゲートの入力指定（ブリーフ§5）:** density/mix は **`--ep PD-2026-046-kelo`**。**`--json <film.json>` は出力パス
> （上書き事故）なので入力に使わない。** asset_reuse は film.json 位置引数、caption_breaks は srt 位置引数、script_length は script 位置引数。
>
> **`check_animation_mix` は `04_scenes/premium_beatsheet.v*.json` があればそれを優先する。**
> §5.6 の通り B の beatsheet は `kelo_beatsheet`（`premium_` 無し）なので**auto-detect されず film.json を測る。**

---

# 10. OP バンパー `OpeningKelo`（Remotion・fps60/1920x1080/180f）

## 10.1 二重OPを作らない
本編（`Ep46Kelo`）の OP は `Bookends.tsx` の `BrandOpening` のまま（`op_ed_bookends` ゲート・フォーク禁止）。
`OpeningKelo` は**独立したタイトルバンパー成果物**（`out/kelo_opening.mp4`。Shorts/予告/SNS 用）。**本編に ffmpeg で焼き込まない。**

## 10.2 Composition 設定
| 項目 | 値 |
|---|---|
| `id` | `OpeningKelo` |
| 解像度 / fps / duration | **1920×1080 / 60 / 180**（=3.0秒） |
| component | `remotion/src/compositions/OpeningKelo.tsx` |

```tsx
import {OpeningKelo, openingKeloDurationInFrames} from './compositions/OpeningKelo';
import keloOpeningProps from '../props/kelo.json';
<Composition id="OpeningKelo" component={OpeningKelo}
  width={1920} height={1080} fps={60}
  durationInFrames={openingKeloDurationInFrames(60)} defaultProps={keloOpeningProps}/>
```

**依存:** `@remotion/motion-blur`（未導入時のみ `cd remotion && npm i @remotion/motion-blur`）。
**`remotion/remotion.config.ts`** は既に正典値（png / h264 libx264 / CRF16 / yuv420p / bt709 / aac 320k / 全コア並列 / angle）。**一致確認のみ・書き換えない。**

## 10.3 秒数ベースのタイムライン（fps=60・フレーム直書き禁止・全て `Math.round(fps*秒)`）

| 秒 | 起きること | 手法 |
|---|---|---|
| 0.00–0.40 | L1 グラデ背景 opacity 0→1・**同時に scale 1.08→1.00（`Easing.out(Easing.cubic)`）** | interpolate（opacity 単独禁止・scale と併用） |
| 0.10 | ロゴ（`hasLogo`）左上に spring・scale 0.4→1.0・opacity 0→1 | spring `damping:14,mass:0.9` |
| 0.15–0.25 | L2 グリッド reveal（opacity→0.18）＋ translateY 0→48px | spring `damping:200,mass:1` + `Easing.inOut(Easing.sin)` |
| 0.25 | L3 グロー（deed-green `#3F8F5F`）scale 0.6→1.15 / opacity 0→0.85 | spring `damping:18,mass:1.2`（併用） |
| 0.30–0.86 | L4 主役タイトルが1文字ずつ切れ上がり（overflow:hidden + translateY 110%→0）＋ opacity。スタッガー **2f/文字**。全体を `Trail(layers=6,lagInFrames=1.2,trailOpacity=0.45)` で包む | spring `damping:16,mass:1` |
| 0.55–1.15 | L2b **境界線（更地に一軒残る家＝deed-green の敷地線）**が中央から縦に `scaleX 0→1`＋opacity 0→0.5（「点の計画」のモチーフ） | spring `damping:22,mass:1.1`・`transformOrigin:'center'`・**motionBlur** |
| 0.95–1.35 | L5a アクセント下線（deed-green）左から `scaleX 0→1` | spring `damping:16,mass:0.8`・`transformOrigin:'left center'` |
| 1.10–1.55 | L5b サブタイトル translateY 24→0 + opacity 0→1 | spring `damping:20,mass:1`（併用） |
| 1.55–3.00 | settle→ホールド。**完全静止フレーム無し・フェードアウトしない** | — |

> **等速線形を1箇所も使わない。opacity 単独の演出を1箇所も作らない**（全 opacity が translateY/scale/scaleX と対）。

## 10.4 props 型と値
```ts
export type OpeningKeloProps = { title:string; subtitle:string; accent:string; hasLogo:boolean };
```
`remotion/props/kelo.json`: `{ "title":"THE LITTLE PINK HOUSE", "subtitle":"THE CITY TOOK IT FOR A DEVELOPER", "accent":"#3F8F5F", "hasLogo":true }`
`remotion/props/kelo_short.json`: `{ "title":"THE LITTLE PINK HOUSE", "subtitle":"CAN THE GOVERNMENT TAKE YOUR HOME?", "accent":"#3F8F5F", "hasLogo":false }`
> `subtitle`/`title` も §2 の R-FORBID/R-DISPO/R-FACE/R-HOUSE 検査対象（`remotion/props/kelo*.json`）。ルート背景は INK 近黒 `#0A0A0C`。
> **accent は EP41 gold / EP42 blue / EP43 amber / EP44 teal / EP45 crimson を書かず deed-green `#3F8F5F`（レーン分離・他話色流用は BLOCKER）。**
> **「the taking was illegal」「the court struck it down」を subtitle に書かない。** 疑問形 `CAN THE GOVERNMENT TAKE YOUR HOME?`・宣言 `THE CITY TOOK IT FOR A DEVELOPER` は事実として可（C-1 の UPHELD 枠と矛盾しない）。

## 10.5 量産
```bash
cd remotion && npm run studio     # OpeningKelo を 0→180f スクラブして §10.3 の各時刻を目視
npx remotion render OpeningKelo out/kelo_opening.mp4 --props=./props/kelo.json
npx remotion render OpeningKelo out/kelo_short_op.mp4 --props=./props/kelo_short.json
```

---

# 11. サムネ3案（`KeloThumbnails.tsx`・`<Still>` 1280×720・Root に `Thumb-kelo-01..03`）

**共通要件:** 見出し全て大文字・4語以内・320pxで判読 / **実在人物の肖像禁止（R1・Susette Kelo の顔/身体を出さない・C-4）** / INK 黒 `#0A0A0C` bg + deed-green `#3F8F5F` /
背景は body 静止画のうち `also_thumb==true` の6枚（象徴オブジェのみ・C-4。**サムネ専用の分類は無い＝also_thumb フラグを読む**） / `thumbnail_visibility`（luma平均≥33＋コントラスト）を通す。目標CTR 6%+。3案は6枚から選ぶ。
**「the taking was illegal」「struck down」「the government can take any home」を出さない（R-FORBID/R-DISPO）。「demolished」を出さない（R-HOUSE）。**

**★also_thumb 6枚（still 資産 ID 空間 S01..S85＝CODEX_A §5 と一字一致必須の A↔B 契約点。CODEX_A の also_thumb 集合と同一 asset ID に `also_thumb:true`）:**
`S01` / `S05` / `S30` / `S55` / `S72` / `S85`。
> サムネ component は**マニフェストの `also_thumb` フラグを読んで**背景を選ぶ（scene id をハードコードしない）。**この6 ID は CODEX_A と完全一致**（`check_kelo_asset_manifest` §3.3-12 が集合 `{S01,S05,S30,S55,S72,S85}` の一致を検査）。**CODEX_A が別集合を採るなら組まずに止めて A に差し戻す。**

- **T1「更地に一軒（最推奨）:** 空の通りに一軒だけ残る小さなピンクの家・周囲は更地（象徴・顔なし・**S01/S05** 系）。文字 **`THEY TOOK HER HOME`**（4語）。`HOME` を deed-green。
- **T2「5 – 4」（数字勝負）:** 大理石の列柱を暗く落とし（**S55** 系）、前面に **`5 – 4`**（大）＋ **`THE TAKING STANDS`**（下・**C-1 UPHELD・違法と読ませない**）。数字は F01 の検証済み値のみ。
- **T3「NOTHING BUILT」（payoff）:** 雑草の更地／州法令集を背にした象徴（**S72/S85** 系）。文字 **`NOTHING WAS BUILT`**（F16）。`NOTHING` を deed-green。

**A/Bタイトル候補（`09_package`・60字以内・台本のとおり・★"illegal/struck down" と書かない）:**
- **A:** `The City Took Her Home and Gave It to a Developer.`
- **B:** `Can the Government Take Your Home for a Private Company?`
> ※「the Supreme Court struck it down」系・「illegal taking」系のタイトルは**禁止**（C-1・R-DISPO）。**サムネに「合法/違法」を断定的に書かない**（枠は "the Court said it could"）。

**固定コメント** `09_package/pinned_comment.v001.txt`（§2 の R-NUM/R-QUOTE/R-FORBID/R-DISPO/R-DOCTRINE/R-HEDGE 検査対象。台帳事実のみ・**988 でなく Institute for Justice 記録／州 eminent-domain リソースの行を含む＝F19系/R-DISPO 隣接**）:
```
Two things Kelo actually decided — and two people get wrong.

WHAT THE COURT DID: By a vote of 5 to 4, the Supreme Court said New London
COULD take these homes. It read the Fifth Amendment's "public use" broadly, as
"public purpose," and held that a genuine economic-development plan can qualify —
even when private developers end up building on the land. The Court did not rule
the taking illegal or unconstitutional. It let it stand.

WHAT IT DID NOT SAY: It did not say the government can take your home for any
reason at all. Justice Kennedy's fifth vote warned that takings that are
pretextual, trivial, or implausible would still be forbidden. And the famous
lines — "any Motel 6 with a Ritz-Carlton, any home with a shopping mall, or any
farm with a factory" — are Justice O'Connor's, writing in DISSENT, not the Court.

Afterward, the grand plan was never built, Pfizer left New London in 2009, and
more than forty states passed laws to rein in eminent domain. Susette Kelo's
actual pink house was not demolished — it was taken apart and moved to a new lot.

For the public record of the case and state eminent-domain resources, see the
Institute for Justice. Visualizations in this video are AI-assisted.
```
> **description.txt にも Institute for Justice 記録／州 eminent-domain リソースへの中立1行を置く（R-DISPO 隣接検査・988 でない）。AI 開示行（`AI-assisted visualization`）を description に置く（R1）。**

---

# 12. 本編コンポジション登録（`remotion/src/Root.tsx`・`Ep45Cleveland`/`Ep43Caniglia` の形を踏襲）
```tsx
import keloFilm from './data/kelo_film.json';
<Composition id="Ep46Kelo" component={CaseFilm}
  durationInFrames={caseFilmDurationInFrames(keloFilm as unknown as FilmData, BRAND.video.fps)}
  fps={BRAND.video.fps} width={BRAND.video.width} height={BRAND.video.height}
  defaultProps={{ data: keloFilm as unknown as FilmData, seriesLabel: 'PRIME DOCUMENTARY',
    title: 'The City Took Her Home and Gave It to a Developer.',
    subtitle: 'In 2005 the Supreme Court said a city could. Most of America spent the years after writing a different answer.' }}/>
```
> **id は正確に `Ep46Kelo`（切り詰め・綴り違い・大文字化の誤記に注意）。** `caseFilmDurationInFrames` の 4項評価は **22173 frames**（§5.1.1・hookSeconds=8.0）。
> `remotion/src` に現在 `kelo` の文字列が無いこと（衝突しない）を確認してから追記。
> `title`/`subtitle` も §2 検査対象（R-FORBID/R-DISPO/R-DOCTRINE/R-HOUSE）。**「the taking was illegal」「the court struck it down」「demolished」を書かない。**

---

# 13. 受入（自分で exit 0 を確認してから完了報告）
```bash
cd C:\Users\aab15\Documents\prime-documentary ; PY=./.venv/Scripts/python.exe

# 0. 語数（最優先・課金前に落とす）
$PY scripts/check_script_length.py episodes/PD-2026-046-kelo/03_script/script.en.v001.md --json   # 2,133語 / wpm178.1 / 718.6s

# 1. 事実性/6制約（EP46固有・正確性ゲートはこの1本・dochighlight 不使用・quote 帰属＝反対意見）
$PY scripts/check_kelo_facts.py --json

# 2. 契約バリデータ
$PY scripts/validate_kelo_beats.py
$PY scripts/check_kelo_asset_manifest.py --assets episodes/PD-2026-046-kelo/05_visuals/asset_manifest.v001.json

# 3. ★5ゲート（animation_mix を忘れるな・入力は --ep / 位置引数を厳守）
$PY scripts/check_asset_reuse.py    remotion/src/data/kelo_film.json
$PY scripts/check_motion_density.py --ep PD-2026-046-kelo
$PY scripts/check_animation_mix.py  --ep PD-2026-046-kelo
$PY scripts/check_caption_breaks.py episodes/PD-2026-046-kelo/08_edit/captions.final.v001.srt

# 4. 水増し・レンダ前プリフライト
$PY scripts/check_padding.py --ep PD-2026-046-kelo --json
$PY scripts/preflight_render_gate.py --ep PD-2026-046-kelo

# 5. 本編レンダ（slim public・並列4）→ BGM → AEカード合成
cd remotion
npx remotion render Ep46Kelo out/kelo.mp4 --public-dir=public_slim --concurrency=4
#   public_slim は kelo_film.json が参照する素材（+ 各 <stem>_depth.png）だけを含む slim public。
#   無ければ referenced paths を public_slim/ にコピーして作る（remotion/public/kelo 本体を痩せさせない）。
cd ..
$PY scripts/build_kelo_bgm_real.py
$PY scripts/ae/composite_kelo_hero.py

# 6. 本編最終受入（episode番号は★位置引数・--ep ではない）
$PY scripts/check_final_acceptance.py 46 \
  --render episodes/PD-2026-046-kelo/08_edit/kelo_final_bgm.v003_ae.mp4 --emit-receipt
```

| ゲート | EP46 目標値 |
|---|---|
| `check_script_length` | 総語数 **2,133** / `wpm 178.1` / narration **718.6s** |
| `check_asset_reuse` | factory≤1 / motion≤2 / still≤2 / first-use **0.8578**（floor0.70） |
| `check_motion_density` | density **3.006**/min / coverage **30.1%** / variety 13（floors 2.5 / 0.25 / 3・beats **≥30**） |
| `check_animation_mix` | still-share **0.4489(cut)/0.4217(frame)**（cap0.45）/ motion-cov **0.5511+**（floor0.45） |
| `check_caption_breaks` | 行末機能語0 / 孤立キュー0 / hard split 0 |
| `check_kelo_facts` | violations = 0（台帳照合・5-4 UPHELD 枠・public purpose 精確・O'Connor/Thomas＝dissent・">40 states" ヘッジ・R-FORBID・R-DOCHL・R-QUOTE） |
| runtime band | 11.8–12.3分（narration 718.6s + hook8.0 + bookends・total **739.1s ≤ 752s**） |
| factory クリップ | ≥24本 → **92本** |
| image_resolution | 全静止画 長辺 ≥3840px |
| thumbnail | 3案 @1280×720 + selected luma≥33 |
| op_ed_bookends | `BrandOpening`/`BrandEndcard` を import（フォーク禁止） |

**全て exit 0 でなければ `package_ready` にしない。自己申告QCは無効。QC基準を書き換えて通すのは禁止。**

## 13.1 完成後の全編アイボール（**1フレーム判定禁止＝EP39-41 実害**）
`kelo_final_bgm.v003_ae.mp4` を **0→末尾まで通しで実視聴**し、以下を確認してから完了報告:
- 紙芝居感が無い（still が連続していない・footage が体感で過半）
- AEカード8枚が全て焼き込まれ数値が台帳と一致（「the taking was illegal」「the court struck it down」「demolished」がどこにも無い）
- **vote01 に "5 – 4 / THE TAKING STANDS / THE COURT SAID THE CITY COULD"（UPHELD・C-1）が読める**
- **pp01「PUBLIC USE → PUBLIC PURPOSE」（C-2・doctrine）が読める。「the government can take any home for any reason」に見えない**
- **st01「MORE THAN 40 STATES」に "MORE THAN" のヘッジが読める（C-6・R-HEDGE・43/44/45/47 の断定数が無い）**
- oc01 の O'Connor 逐語が **O'Connor, DISSENTING** 帰属、th01 が **Thomas, DISSENTING** 帰属（Court に帰属していない・要約を引用符にしていない・C-3/R-QUOTE）
- **pink01 が "THE LITTLE PINK HOUSE / SAVED, AND MOVED"（移築）＝彼女の家は demolished でない（C-4/R-HOUSE）**
- Susette Kelo の顔・身体・肖像が無い（象徴＝ピンクの家/水辺/空の通り/condemnation notice/解体重機/更地/site plan/Motel6 と Ritz-Carlton/州法令集/移築のみ・C-4）／扇情でない（poverty porn なし）
- **`dochighlight`（黒バー/box/underline）が1本も無い（figures/AE／R-DOCHL）**
- 生成ビジュアル表示中は `AI-assisted visualization` が右下に常時（**AEカード8枚の表示中も**開示が見える＝カード共通スタックに焼かれている・R1・§7.3/§7.9）
- **概要欄/固定コメントに 988 でなく Institute for Justice 記録／州 eminent-domain リソースの行がある（F19系・R-DISPO 隣接）**
- accent が deed-green `#3F8F5F`（EP41 gold / EP42 blue / EP43 amber / EP44 teal / EP45 crimson が紛れていない）
- 音ズレ・字幕ズレ・尺差（base と <=0.5s）が無い

---

# 14. 絶対にやらないこと
- **EP39 / EP40 / EP41 / EP42 / EP43 / EP44 / EP45 のファイル・素材に触らない**（読み取りのみ可）。レーンを分離する。
- **スレッドAの所有ファイル（§0.2.1）に書かない**（`05_visuals/` `05_stock/` `remotion/public/kelo/` `H:\...\ai\kelo\`）。**B の provenance は `04_scenes/kelo_build_manifest.v001.json` に書く。**
- **設計書 / ブリーフ / `EP46_kelo_CODEX_A_*` / PD-2026-039〜045 に触らない。**
- **課金ジョブを起動しない**（ElevenLabs TTS / 課金画像生成API / YouTube アップロード）。narration_index は実測版を消費するだけ。
- **公開済み・出荷済み mp4 を上書き・再レンダしない**（出力は必ず `_v003_ae`）。
- **台帳（§2）に無い数値を焼かない**（$580,000 の再発防止）。不明値は `verified:false` でカード除外。**">40 states" を断定数（43/44/45/47）にしない（R-HEDGE）。**
- **`FigureSpec` の `kind` を推測で書かない**（§6.2 の実在小文字値のみ。大文字名は無言で消える。`comparebars` は非在→`compbars`。5-4 は `votetally{majority,dissent}`）。**★`dochighlight` を1本も使わない（R-DOCHL）。**
- **`--variants` という語を書かない**（1シーン1枚・バリエーション0＝ブリーフ§1。SDXL は A の領分で 1 固定）。
- **asset_manifest の `counts`/`role` enum/`overlay` 枚数を CODEX_A と食い違わせない**（`role` は `body`/`i2v_source`/`reject` の3値のみ・**`thumb`/`still_thumb` を作らない**・overlay=12・**also_thumb 集合 `{S01,S05,S30,S55,S72,S85}`**）。
- **収用を「違法」化しない・「struck down」と言わない**（C-1・R-DISPO＝**5-4 UPHELD**）。**「public purpose」を過大化しない**（C-2・R-DOCTRINE）。**O'Connor / Thomas を Court に帰属させない**（C-3・R-QUOTE＝**dissenting**）。**Susette Kelo の顔/肖像/身体を出さない・扇情化しない・家を demolished と書かない**（C-4・R-FACE/R-HOUSE）。**NLDC/Pfizer/城を機関として説明**（C-5）。**数値は台帳一致・">40 states" はヘッジ**（C-6・R-NUM/R-HEDGE）。**988 でなく Institute for Justice 記録／州 eminent-domain リソース**（F19系）。
- **accent に他話色（EP41 gold / EP42 blue / EP43 amber / EP44 teal / EP45 crimson）を使わない**（deed-green `#3F8F5F` のみ）。
- **stub/placeholder/dryrun のコードパスを作らない**（このスレッドは実素材のみ・ブリーフ§5/§7・grep で 0）。
- **スペック数値（225 cuts / still85 / factory92 / motion16 / distinct193 / first-use0.8578 / still-share0.4489 / figures≥30→36 / 718.6s / 2,133語 / mean_shot3.19 / hookSeconds8.0 / total739.1s≤752s / durationInFrames22173）を変えない。**
- **実在しないスクリプト名を書かない**（新規は §0.3 の一覧のみ・複製元を明記・**`build_tekoh_film.py` は非実在**）。**composition id は `Ep46Kelo`（切り詰め・綴り違い注意）。** **PowerShell 経由で正規表現/エスケープを生成しない**（`\b` バックスペース化の実害）。
