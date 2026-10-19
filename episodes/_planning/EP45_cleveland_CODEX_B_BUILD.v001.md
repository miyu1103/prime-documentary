# EP45 cleveland — Codex スレッドB「実装」引き継ぎプロンプト v001

> **このファイルは単体で完結している。他のファイルを読まなくても着手できる。**
> 並行して走っていたスレッドA（素材生成）のファイル `EP45_cleveland_CODEX_A_*.md` は**読まない**（Aは既に FROZEN・接続点は §3 のマニフェスト1ファイル）。
> 設計書 `EP45_cleveland_DESIGN*.md` も**読まない**（必要な数値・AEデッキ・figures 配分はすべて本書に転記済み）。
> `EP45_cleveland_PRODUCTION_SPEC.v001.json` の数値は本書に転記済み。**あなたはこれを書き換えない。**

```
あなたは Prime Documentary（YouTubeドキュメンタリーチャンネル）の制作エンジニアです。
リポジトリ: C:\Users\aab15\Documents\prime-documentary
Python:     C:\Users\aab15\Documents\prime-documentary\.venv\Scripts\python.exe
メディア:   H:\pd-media
担当:       EP45 / Episode ID: PD-2026-045-cleveland / slug: cleveland
Composition id（本編）: Ep45Cleveland
```

**題材:** *Bearden v. Georgia*, 461 U.S. 660 (1983)（decided **1983-05-24**）と **Harriet Cleveland**（Montgomery, Alabama の**存命の私人 = R2**）。
払えない罰金を理由とする投獄は **Bearden(1983) 以降 憲法違反（違法）**。本作の主題は「**1983以降 違憲なのに実務で続いた（enforcement failure）**」。
Bearden＝**最高裁の線**。Harriet Cleveland の救済は**下級審の訴訟＋2014和解**であって最高裁判決ではない。Bearden は罰金・手数料・賠償そのものを禁じてはいない（**能力審査なしの収監だけ**を禁じた）。

> **★正確性6制約が全出力を律する（§2）。** 「合法(legal/lawful)」と書かない・「最高裁が Cleveland を救った」（Bearden↔Cleveland 混同）を書かない・「全罰金違憲」に過大化しない・Harriet Cleveland の顔/肖像/身体を一切出さない（尊厳・poverty porn 禁止）・JCS＝制度として説明（個人攻撃しない）・数値は台帳一致。**★`figures[].kind` に `dochighlight` を1件も入れない**（黒バー/box/underline がバグに見える＝3回指摘）。**概要欄は 988 でなく local legal-aid / ability-to-pay 権利の1行。**

---

# 0. このスレッドの責務・境界・完了条件

## 0.1 このスレッド（B）の責務 — **コード律速。実装は全部書ける。**

| # | 作業 | 成果物 |
|---|---|---|
| B-1 | エピソードディレクトリと `manifest.json` | `episodes/PD-2026-045-cleveland/**` |
| B-2 | 境界契約マニフェストの**消費側**バリデータ | `scripts/check_cleveland_asset_manifest.py` |
| B-3 | 事実台帳 F-ID と 6制約ゲート（**EP45固有・BLOCKING**） | `scripts/check_cleveland_facts.py` |
| B-4 | `cleveland_film.json` ビルダ（**asset_map→manifest変換＋beatsheet生成／footage混在・実素材のみ**） | `scripts/build_cleveland_film.py`（**`build_caniglia_film.py` を複製**） |
| B-5 | beats バリデータ（AEとRemotionの区間衝突検査＋ledger／6制約） | `scripts/validate_cleveland_beats.py`（**`validate_caniglia_beats.py` を複製**） |
| B-6 | **構文境界で切る字幕生成器**（実測 narration_index から verbatim） | `scripts/gen_captions_cleveland.py`（**`gen_captions_caniglia.py` を複製**） |
| B-7 | **After Effects カード**のビルダとコンポジタ | `scripts/ae/build_cleveland_hero_cards.py` / `scripts/ae/composite_cleveland_hero.py` |
| B-8 | 本編 BGM ミックス（AEカード合成の基底 mp4 を生成） | `scripts/build_cleveland_bgm.py`（**`build_young_bgm_real.py` を複製**） |
| B-9 | Remotion 本編コンポジション登録 `Ep45Cleveland` | `remotion/src/Root.tsx` |
| B-10 | OP バンパー `OpeningCleveland`（fps60/1920x1080/180f） | `remotion/src/compositions/OpeningCleveland.tsx` |
| B-11 | サムネ3案 | `remotion/src/compositions/ClevelandThumbnails.tsx` |
| B-12 | 本編レンダ→BGM→AEカード合成→全ゲート→**全編アイボール** | `episodes/PD-2026-045-cleveland/08_edit/**` |

> **★このスレッドは「実素材のみ」（ブリーフ§7 / タスク指示）。stub/dryrun のコードパスを作らない。** A は FROZEN（§3 の本番マニフェストが実在）・narration_index は実測版が実在する前提で組む。**素材が来ていなければ止めて A/上流に差し戻す**（架空の黒スタブで緑にしない）。

## 0.2 もう一方のスレッド（A・FROZEN）との境界 — **接続点はただ1ファイル。**

```
episodes/PD-2026-045-cleveland/05_visuals/asset_manifest.v001.json
   ↑ Aが生成（唯一の生産者・FROZEN）        ↓ Bが消費（唯一の消費者・検証者）
```

**Bはこのファイル以外のAの中間生成物を読まない。** このマニフェストは **A(producer)とB(consumer/validator)で counts / role enum / overlay枚数を1バイト単位で共有**する（§3）。

> **★1シーン1枚・バリエーション0（ブリーフ§1）の B 側での意味:** A は同一ショットの `_01/_02/_03` を**作らない**。
> したがってマニフェストの `stills[role="body"]` は **84本すべてが固有プロンプトの distinct**（`counts.still_body==84`）。
> A の `ai_prompts.v001.md` は **still 84行（S01..S84）＋i2v種 16行 = 総生成画像 100枚**（各1回）。**still カット 100本という数字とは別物**（偶然どちらも 100）。
> B は編集上、still を **各最大2回**まで再使用してカット100本を組む（cap 2 の"再利用"であって"バリエーション"ではない）。
> **B は `--variants` という語をどのコマンド・ログにも書かない**（それは A の SDXL 側の概念で、しかも 1 固定）。

### 0.2.1 ファイル所有権（これを破ると並行作業が壊れる）

| パス | 所有 | Bの権限 |
|---|---|---|
| `episodes/PD-2026-045-cleveland/manifest.json` | **B** | 読み書き |
| `episodes/PD-2026-045-cleveland/{00_topic,01_research,03_script,04_scenes,06_audio,08_edit,09_package,approvals,events}/**` | **B** | 読み書き |
| `remotion/src/**` `remotion/props/**` | **B** | 読み書き |
| `scripts/*cleveland*.py` / `scripts/ae/*cleveland*.py`（§0.3） | **B** | 新規作成 |
| **`episodes/PD-2026-045-cleveland/05_visuals/**` `05_stock/**`** | **A** | **読み取りのみ。書くな** |
| **`H:\pd-media\assets\ai\cleveland\**` / `ai_video\cleveland\**`** | **A** | **読み取りのみ。書くな** |
| **`remotion/public/cleveland/{img,factory,motion,overlay}/**`** | **A** | **読み取りのみ。書くな** |
| `EP45_cleveland_DESIGN*.md` / `EP45_cleveland_CODEX_A_*.md` | **設計/Aスレッド** | **触るな** |
| `EP45_cleveland_PRODUCTION_SPEC.v001.json` / `EP45_cleveland_script.en.v001.md` | **上流** | **読み取りのみ。書くな** |
| `episodes/PD-2026-039-*/**` … `PD-2026-044-*/**` / それらの素材 | **他エージェント** | **絶対に触るな（読み取りのみ可）** |

> **B は `remotion/public/cleveland/` に書かない**（A の staging 済み本番素材）。B の provenance/beatsheet は `04_scenes/` に書く（§5.6）。

## 0.3 B が新規作成するスクリプト（これ以外を新規に作らない。既存を改変しない）

| パス | 役割 | 手本（**改変せず読んで複製→パス/定数だけ差し替え**・実在確認済み） |
|---|---|---|
| `scripts/check_cleveland_asset_manifest.py` | §3.3 消費側バリデータ | `scripts/check_caniglia_asset_manifest.py`（無ければ `check_young_asset_manifest.py`） |
| `scripts/check_cleveland_facts.py` | §2 6制約＋台帳（BLOCKING・**正確性ゲート名はこの1つに統一**） | **`scripts/check_caniglia_facts.py`**（／`check_young_facts.py`） |
| `scripts/build_cleveland_film.py` | §5 film.json＋provenance＋beatsheet＋SRT（**実素材のみ**） | **`scripts/build_caniglia_film.py`**（＝`build_young_film.py` と同一ロジック系） |
| `scripts/validate_cleveland_beats.py` | §7.9 不変条件 | **`scripts/validate_caniglia_beats.py`** |
| `scripts/gen_captions_cleveland.py` | §8 構文境界字幕生成器 | **`scripts/gen_captions_caniglia.py`** |
| `scripts/ae/build_cleveland_hero_cards.py` | §7 AEカードビルダ | **`scripts/ae/build_young_hero_cards.py`**（／`build_thompson_hero_cards.py`） |
| `scripts/ae/composite_cleveland_hero.py` | §7.10 コンポジタ（`beats.json` の `film_offset_sec` を読む） | **`scripts/ae/composite_young_hero.py`** |
| `scripts/build_cleveland_bgm.py` | §7.10 基底 mp4（narration＋BGM ミックス） | **`scripts/build_young_bgm_real.py`** |

> **`build_cleveland_film.py` の複製時に差し替える定数:** `ASSET_MAP`（マニフェスト→cut 変換テーブル）・`NARR`（narration_index 既定パス）・
> `FACTORY_SEL`（factory 選抜の参照）・`SLUG="cleveland"`・`EP="PD-2026-045-cleveland"`・出力パス群。**ロジック（best-pick / tile_window /
> allocate / build_figures / build_captions）は1行も変えない。**
> **既存の `build_caniglia_film.py` / `gen_captions_caniglia.py` 等は触らない**（他エピソードが使用中）。EP45用に**新規コピー**する。
> **`build_tekoh_film.py` は実在しない。捏造しない**（`ls scripts/` で確認済み。複製元は上表の実在ファイルのみ）。

## 0.4 完了条件（実素材で、全て緑になったら「実装完了」）

```bash
cd C:\Users\aab15\Documents\prime-documentary
PY=./.venv/Scripts/python.exe

# [B-DONE-1] マニフェスト消費側バリデータ（A の FROZEN 本番マニフェスト相手に通ること）
$PY scripts/check_cleveland_asset_manifest.py \
  --assets episodes/PD-2026-045-cleveland/05_visuals/asset_manifest.v001.json

# [B-DONE-2] 字幕（実測 narration の実文から構文境界で生成）
$PY scripts/gen_captions_cleveland.py \
  --narr episodes/PD-2026-045-cleveland/06_audio/narration_index.v001.json
$PY scripts/check_caption_breaks.py \
  episodes/PD-2026-045-cleveland/08_edit/captions.final.v001.srt

# [B-DONE-3] film.json を実マニフェストから組み立てる（footage 混在必須・dochighlight 不使用）
$PY scripts/build_cleveland_film.py \
  --assets episodes/PD-2026-045-cleveland/05_visuals/asset_manifest.v001.json \
  --narr   episodes/PD-2026-045-cleveland/06_audio/narration_index.v001.json \
  --out    remotion/src/data/cleveland_film.json

# [B-DONE-4] ★5ゲート全部（--ep 指定・animation_mix を絶対に忘れるな）
$PY scripts/check_asset_reuse.py     remotion/src/data/cleveland_film.json
$PY scripts/check_motion_density.py  --ep PD-2026-045-cleveland
$PY scripts/check_animation_mix.py   --ep PD-2026-045-cleveland
$PY scripts/check_caption_breaks.py  episodes/PD-2026-045-cleveland/08_edit/captions.final.v001.srt
$PY scripts/check_script_length.py   episodes/PD-2026-045-cleveland/03_script/script.en.v001.md --json

# [B-DONE-5] 事実性/6制約（＋dochighlight 不使用）
$PY scripts/check_cleveland_facts.py --json

# [B-DONE-6] beats 契約（AE区間 と Remotion figures[] が1秒も重ならない）
$PY scripts/validate_cleveland_beats.py

# [B-DONE-7] AE カードをビルド＋レンダ＋コンポジット
$PY scripts/ae/build_cleveland_hero_cards.py
"C:/Program Files/Adobe/Adobe After Effects 2026/Support Files/AfterFX.exe" -noui \
  -r "C:/Users/aab15/Documents/prime-documentary/episodes/PD-2026-045-cleveland/08_edit/ae_hero/cleveland_hero.jsx"
$PY scripts/ae/composite_cleveland_hero.py

# [B-DONE-8] Remotion Studio で目視
cd remotion && npm run studio
#   → Ep45Cleveland / OpeningCleveland / Thumb-cleveland-01..03 が出て、実際に動くこと
```

**台本は既に確定済み**（`EP45_cleveland_script.en.v001.md`・**2,119語・11.9分**・ロック）。本番配置先は
`episodes/PD-2026-045-cleveland/03_script/script.en.v001.md`（**1バイトも変えずコピー**・整形禁止＝AI臭再発と語数ゲート再計算を招く）。

---

# 1. 実装前に必ず読むファイル（**推測で書くな**）

| パス | なぜ読むか |
|---|---|
| `scripts/build_caniglia_film.py` | **複製元。** best-pick / tile_window / allocate / build_figures / build_captions をそのまま踏襲し、定数だけ cleveland に。**footage を必ず混ぜる（§0.5 の紙芝居回避）** |
| `scripts/ae/build_young_hero_cards.py` | **複製元。** `money_keys()`（Python で表示文字列を全事前計算）/ `fit_size()` / CARDS デッキ構造 / レイアウト定義 / 完了マーカーをそのまま |
| `scripts/ae/composite_young_hero.py` | **複製元。** SKIP4条件（missing / 解像度不一致 / 実測尺不足 / window past end）と ffmpeg フィルタグラフ（overlay/blend）と `film_offset_sec` の読み込みをそのまま |
| `scripts/gen_captions_caniglia.py` | **複製元。** `internal_split()` / `chunk_sentence()` / `NO_DANGLE_END` import をそのまま |
| `scripts/build_young_bgm_real.py` | **複製元。** narration＋BGM ミックスで基底 mp4 を作る経路 |
| `remotion/src/compositions/CaseFilm.tsx` | `FilmData` 型 / `caseFilmDurationInFrames` / `depthSrcOf()` |
| `remotion/src/components/FigureBeats.tsx` | `FigureSpec` の**実在する `kind` 文字列**（§6.2 の警告を必ず読め・**全小文字**・**`dochighlight` は使わない**） |
| `remotion/src/components/Bookends.tsx` | `OPENING_SEC` / `ENDCARD_SEC` / `BrandOpening` / `BrandEndcard` |
| `scripts/check_asset_reuse.py` / `scripts/check_motion_density.py` / `scripts/check_animation_mix.py` / `scripts/check_caption_breaks.py` / `scripts/check_script_length.py` | 通すべき5ゲートの**実際の判定ロジック**（§9） |
| `C:\Users\aab15\Documents\pino-channel\remotion\src\Opening.tsx` | §10 の OP 正典実装 |

---

# 0.5 ★★★ EP39/40/41/42/43/44 で踏んだ失敗＝最初から防ぐ（本書の全体設計はこの6点を構造で潰している）★★★

1. **紙芝居（最重要）** — 静止画100%で組むと `check_animation_mix` が FAIL する。**EP45 は最初から footage を混ぜる。**
   `check_animation_mix.compute_metrics_from_film()` は film.json の `cuts[]` を
   **`kind=="img"` → still（scene 扱い）/ それ以外 → footage（motion 扱い）** と分類する。
   → §5 の cuts 構成は **factory 92 + motion 32 の footage を最初から入れて still-share を cut数ベース 0.4464・frame ベース ~0.42** にする。
2. **AEカードは密度に数えられない** — `check_motion_density` は film.json の `graphics+figures+heroCuts` **のみ**数える。
   AEカードは ffmpeg で後合成するので**1本も数えられない**。→ §6 で **film.json 側の `figures[]` を 36本**（spec floor 30 に **+6**・`graphics[]=[]`）置く。AEカードは別勘定。
3. **FigureSpec の `kind` は実在の小文字値のみ** — 大文字名（`ActTitle`/`QuoteCard`/`VoteTally` 等）は無言で描画が消える（§6.2）。`comparebars` は非在→`compbars`。**★`dochighlight` を1本も使わない**（§6.2・R-DOCHL）。
4. **台帳に無い数値を焼くな** — EP40 の生 Codex-B 出力に架空の $580,000 が入って**不採用になった実害**。
   → §2 の事実台帳 F-ID に**検証済み値だけ**を置き、`check_cleveland_facts.py` が film.json/AE/サムネ/props の全数値を台帳照合する。台帳に無い数値・`verified:false` の数値を焼いたら FAIL。
5. **字幕は台本本文と対応** — EP38 で台詞混入・「final」誤称の実害。→ §8 の字幕は **narration_index の実チャンク文をそのまま** verbatim で使う（自作しない）。
6. **レンダー前ゲート** — build 後に `check_asset_reuse` / `check_motion_density` / `check_animation_mix` / `check_caption_breaks` / `check_script_length` を**全部**通す（§9・§13）。**animation_mix を忘れるな。**

---

# 2. ★ EP45固有の正確性6制約・事実性ロック（`scripts/check_cleveland_facts.py`・BLOCKING）

> **この節に違反した成果物は、他が全て完璧でも出荷不可。** 検査対象は film.json の figures/captions、AE beats、
> サムネ、props、固定コメント、`03_script/script.en.v001.md`、（存在すれば）マニフェストの tags/caption_hint/qc.notes の**全文字列と全数値**。
> **正確性ゲートはこの1本に統一（`check_cleveland_facts.py`）。DESIGN/CODEX_A も同名を参照する（別名を作らない）。** 出力 `09_package/facts_lock.v001.json`。

## 2.1 正確性6制約（全出力に適用・違反は BLOCKER）

| # | 制約 | 許可される表現 | 禁止 |
|---|---|---|---|
| C-1 | **「合法」化しない・enforcement failure** | 「unconstitutional since 1983」「yet it continued」「the rule held, the enforcement failed」「still happening」。`1983`/`unconstitutional`/`Bearden` を出すカードは enforcement-failure 枠を同一カードに併記 | 「it is legal」「debtors' prison is legal」「lawful to jail」「no longer exists / completely abolished / fully ended」 |
| C-2 | **Bearden＝最高裁 / Cleveland＝下級審和解** | 「a lower court, not the Supreme Court」「a settlement, announced in late 2014」。`SETTLED 2014`/`settlement`/`Cleveland v.` を含むカードに「lower court」「not the Supreme Court」を同一カードに併記 | 「Supreme Court saved/freed Cleveland」「SCOTUS ruled for Cleveland」「Cleveland reached the Supreme Court」 |
| C-3 | **holding を正確に・過大化しない** | 「ability to pay」「without an ability-to-pay inquiry」「no hearing」に射程を限定。「Bearden did not abolish fines」。**compbars では "fines still allowed" 側を必ず併記** | 「all fines unconstitutional」「Bearden banned fines」「fines are illegal」「every fine is unconstitutional」 |
| C-4 | **Harriet Cleveland＝R2・象徴のみ・poverty porn 禁止** | 事件主体としての名（"Harriet Cleveland was jailed"）。ビジュアルは督促状の束・停止された免許証・空の財布・裁判所の長い廊下・留置扉・booking の時計・支払台帳/請求書（ロゴぼかし）・バス停・空の弁護人席 | 顔・肖像・身体・人物化／`Cleveland` 直後60字の `face`/`portrait`／子ども・泣く人・困窮の煽情 |
| C-5 | **制度を説明・個人攻撃しない** | JCS＝offender-funded probation を制度として説明。Judge **Hub Harrington** の公開判決逐語「a judicially sanctioned extortion racket」は**帰属明記**で可 | JCS 社員/判事の実名に非公開・非逐語の断罪語を付す |
| C-6 | **数値は台帳一致・捏造ゼロ・medium はヘッジ** | 画面数値は §2.2 の台帳のみ。medium（$1,554-31日・$200-$40）は帰属 `Fines & Fees Justice Center`（略記 `FFJC` 可）を同一カード or 近傍に維持 | 台帳外の金額・年・件数・州数／medium の無帰属提示 |
| R1 | **実在人物の顔・肖像を生成しない** | 全生成ビジュアル表示中は `AI-assisted visualization`（右下）常時／概要欄1行AI開示 | 認識可能な人物・読める偽公文書 |
| ★DH | **dochighlight 不使用** | 判読ハイライトの意図は `quote`/`stat`/`lowerthird`/`kinetic` で代替 | `figures[].kind`/beats/レイアウト名に `dochighlight`/`DOCHIGHLIGHT` を1件でも出す |

**★禁止語（`check_cleveland_facts.py` が全文字列を case-insensitive 部分一致で検査。1件でも FAIL）:**
`it is legal` / `legally jailed` / `lawful to jail` / `debtors' prison is legal` / `perfectly legal` / `no longer exists` / `completely abolished` / `fully ended` /
`supreme court saved cleveland` / `scotus ruled for cleveland` / `cleveland reached the supreme court` / `supreme court freed her` /
`all fines unconstitutional` / `bearden banned fines` / `fines are illegal` / `no more fines` / `every fine is unconstitutional` /
`poverty porn` / `starving child` / `crying child` / `weeping mother`。
> **★重要な設計注意:** 台本本文（＝字幕 verbatim）には「declared unconstitutional in 1983」「never reached the Supreme Court」など
> **否定/正確文脈の語**が含まれる。上の禁止語リストは**それらと衝突しない断定形だけ**を選んである。**禁止語リストにこの近似語を足すな**
> （字幕 verbatim を巻き込んで false FAIL する）。C-1/C-2/C-3 の**枠付き/限定の別**は下の**文脈ルール**（R-LEGAL/R-SCOTUS/R-HOLDING）で捕える。

## 2.2 事実台帳 F-ID（`03_script/cleveland_facts.v001.json`・**Bが台本の事実対応表 C01–C26 から転記して作る**）

**スキーマ版:** `cleveland_facts.v1`。各 F-ID は `{"value":..., "unit":..., "verified":bool, "confidence":"high|medium", "claim_id":"", "attribution":"", "quote":""}`。
**台本の事実対応表（claim id C01–C26）に裏付けのある値だけ `verified:true`。裏付け無しは `verified:false`。medium は `attribution` 非空必須。**

| F-ID | 内容 | 使う場所 | claim | conf |
|---|---|---|---|---|
| F01 | 判例引用 = **Bearden v. Georgia, 461 U.S. 660 (1983)**・decided **1983-05-24** | fig lowerthird/timeline / AE d01(place) | C01 | high |
| F02 | holding = 収監前に「支払い能力（willful refusal か genuine inability）」＋「代替手段」を検討する義務（**能力なしだけの審問なし収監のみを閉じた**） | fig compbars/quote | C02/C03/C06 | high |
| F03 | Cleveland 救済 = **下級審の訴訟＋2014和解**（最高裁判決でない） | fig timeline/stat / AE r01 | C18 | high |
| F04 | **能力審問なしで収監**（NO ABILITY-TO-PAY HEARING before jail）＝Bearden 違反の核 | fig stat / AE h01 | C04/C14 | medium |
| F05 | JCS offender-funded = **$200/月**のうち **$40が会社**（の取分） | fig compbars/bar / AE j01 | C15/C21 | medium・FFJC |
| F06 | JCS 規模（**2013**）= **~38,000人・4州・100+ Alabama 裁判所** | fig stat/numberticker/regionmap / AE s01 | C22 | high |
| F07 | 法廷意見執筆 = **Justice O'Connor**・逐語「it is fundamentally unfair to revoke his probation automatically, without even considering whether an adequate alternative to prison exists」 | fig quote / AE q01 | C08/C09 | high |
| F08 | Bearden 判決日 = **MAY 24, 1983** | AE d01(date) / fig timeline | C01 | high |
| F09 | 裁判所命令 = **$1,554 or 31日**（能力審問なし） | fig stat/numberticker / AE m01 | C13 | medium・FFJC |
| F10 | **Williams v. Illinois, 399 U.S. 235 (1970)** | fig lowerthird/timeline | C10 | high |
| F11 | **Tate v. Short, 401 U.S. 395 (1971)** | fig lowerthird/timeline | C11 | high |
| F12 | Bearden の事実 = **$500 罰金 + $250 賠償** | fig compbars（Bearden 文脈のみ） | C07 | high |
| F13 | JCS = **2001設立・Georgia・offender-funded** | fig lowerthird/timeline | C20 | high |
| F14 | **Harpersville · 2012** / Judge **Hub Harrington** 逐語「a judicially sanctioned extortion racket」 | fig quote/timeline（Harrington 帰属） | C23 | high |
| F15 | **SPLC RICO 2015-03 → JCS が AL 全事業閉鎖 2015** | fig timeline | C24/C25 | high |
| F16 | **Harriet Cleveland ＝ R2・Montgomery, AL**（象徴のみ） | fig pindropmap | C12 | high |
| F17 | **第14修正** = due process ＋ equal protection の収斂 | fig lowerthird | C05 | high |
| F18 | 2014 settlement 逐語「No person shall be incarcerated for their inability to pay fines and fees」（settlement 帰属） | fig quote | C18 | high |
| F19 | 概要欄の **local legal-aid / ability-to-pay 権利の1行**（★988 でない） | description.txt / pinned_comment のみ（figures/AE カードにしない） | C-4系 | — |

> **F03/F09/F14 は同一カード/payload 内で限定ラベルを併記する（C-2/C-6/C-5）:** F03（SETTLED 2014）は "a lower court, not the Supreme Court" を、
> F09/F05（$1,554・$200/$40）は "PER FINES & FEES JUSTICE CENTER" を、F14（extortion racket）は "Judge Harrington said" を**削除禁止**。
> **数値の許可集合（R-NUM）:** `1554 / 31 / 200 / 40 / 38000 / 4 / 100 / 461 / 660 / 1983 / 24(May 24) / 399 / 235 / 1970 / 401 / 395 / 1971 / 500 / 250 / 2001 / 2012 / 2013 / 2014 / 2015`。これ以外の金額・年・件数・州数が画面に出たら FAIL。

## 2.3 `check_cleveland_facts.py` の検査（exit 0=PASS / 1=FAIL / 2=スキーマ不一致）

**検査対象ファイル（この一覧をハードコード。存在するものだけ検査し、無いものは `skipped[]` に必ず明記）:**

```
episodes/PD-2026-045-cleveland/03_script/script.en.v001.md
episodes/PD-2026-045-cleveland/03_script/cleveland_facts.v*.json
episodes/PD-2026-045-cleveland/08_edit/ae_hero/beats.json
episodes/PD-2026-045-cleveland/09_package/*.json        （title / description / thumbnail headlines）
episodes/PD-2026-045-cleveland/09_package/*.txt         （固定コメント・description.txt）
episodes/PD-2026-045-cleveland/05_visuals/asset_manifest*.json  （tags / caption_hint / qc.notes）
remotion/src/data/cleveland_film.json                   （figures[].text / figures[].lines[] / figures[].kind / captions[] の全文字列と数値）
remotion/props/cleveland*.json                          （title / subtitle）
```

- **R-FORBID（最優先）** — §2.1 の禁止語が対象文字列のどこかに出たら即 FAIL。**近似語（否定/正確文脈）を巻き込まない断定形のみ**を検査（§2.1 の注意）。
- **R-LEGAL（C-1）** — `1983`/`unconstitutional`/`Bearden` を含むカード/figure に enforcement-failure 枠（`yet it continued`/`the rule held`/`still happening`/`enforcement failed`）が同一 payload に無ければ FAIL。**`description.txt` に `legal aid` かつ `ability to pay` の1行が無ければ FAIL（988 でない・R1連結）。**
- **R-SCOTUS（C-2）** — `SETTLED 2014`/`settlement`/`Cleveland v.` を含む payload に `lower court` かつ `not the Supreme Court` が無ければ FAIL。§2.1 の SCOTUS 断定語が出たら FAIL。
- **R-HOLDING（C-3・BLOCKING）** — `Bearden`/`holding` を含む payload は「inability without an ability-to-pay inquiry」に射程限定（`without asking`/`ability to pay`/`no hearing` のいずれか同伴）。§2.1 の過大化語が出たら FAIL。**Bearden 文脈の `compbars` は "fines/fees/restitution still allowed" 側を必ず併記**（能力なしだけの審問なし収監のみが閉じた＝過大化しない）。
- **R-NUM（C-6・R-LEDGER）** — figures[] の `value`/`numKeys` 到達値、AE `beats[].value`/`beats[].main`/`beats[].hero`、サムネ数字に現れる**あらゆる数値**は §2.2 の許可集合に**完全一致**必須。`$1,554`/`$200`/`$40` を含むカードに `Fines & Fees Justice Center`（`FFJC` 可）が同一カード or 近傍に無ければ FAIL（medium ヘッジ）。
- **R-FACE（C-4/R1）** — `has_readable_text`/`has_identifiable_face`/`has_human_body` が true の項目は `role=="reject"`。`ai_prompts.v001.md` 正プロンプトの `portrait`/`face of`/`likeness`/`Harriet Cleveland`（人物として）/`her body`/`her children`/`crying child`/`weeping mother` は FAIL（ネガティブでの使用は可）。`Cleveland` 直後60字の `face`/`portrait`/`depicted as a woman`、poverty-porn 語（`squalor`/`filthy home`/`destitute children`）で FAIL。生成ビジュアル区間の `AI-assisted visualization` 欠落・`description.txt` の AI 開示行欠落で FAIL。
- **R-ATTACK（C-5）** — JCS 社員・判事の実名に非公開・非逐語の断罪語を付したら FAIL。`Hub Harrington`/`Harrington` は**逐語 `judicially sanctioned extortion racket` の帰属としてのみ**可（帰属語 `Judge`/`said`/`called it` 同伴必須）。
- **R-ATTRIB** — `quote[].attribution` が非空・逐語のみ（要約を引用符に入れない）。許可対応表:
  ```python
  APPROVED_QUOTES = {
    "it is fundamentally unfair to revoke his probation automatically, without even considering whether an adequate alternative to prison exists":
        "Justice O'Connor, for the Court",                     # F07/C08/C09（多数意見・逐語）
    "a judicially sanctioned extortion racket":
        "Judge Hub Harrington",                                # F14/C23（公開判決・逐語・帰属必須）
    "no person shall be incarcerated for their inability to pay fines and fees":
        "the 2014 settlement",                                 # F18/C18（和解条項・逐語）
  }
  ```
- **R-DOCHL（★DH・BLOCKING）** — `cleveland_film.json` の `figures[].kind` に `dochighlight` が1件でも出たら FAIL
  （`grep -c '"kind"[[:space:]]*:[[:space:]]*"dochighlight"'` が 0 でなければ FAIL）。`beats.json`/レイアウト名にも `dochighlight`/`DOCHIGHLIGHT` を出さない。
- **R-DATE** — F01/F08(1983-05-24) と F10(1970)/F11(1971)/F13(2001)/F14(2012)/F03(2014)/F15(2015) の日付・年が別カードで取り違えられていないこと。

**出力:** `episodes/PD-2026-045-cleveland/09_package/facts_lock.v001.json`（`{"pass":bool,"violations":[{"file","rule","line","excerpt"}],"skipped":[...]}`）。
**`pass:true` でない限り `check_final_acceptance.py` に進んではならない。**
**CLI:** `--json`。対象ファイルが未生成ならスキップして必ずログに出す。「無いから通した」を黙るな。

---

# 3. ★境界契約: `asset_manifest.v001.json`（Aから受け取る唯一のファイル・FROZEN）

## 3.1 スキーマ（**Aが生成する。Bはこの形を前提に読む・A↔B 1バイト一致**）

**スキーマ版:** `cleveland_assets.v1`（固定文字列。異なれば **exit 2**）。
EP45 spec の点数に一致: **still_body 84 / still_i2v_source 16 / motion 16 / factory 92 / overlay 12**。
**★サムネは独立の分類を持たない。** body 84枚のうち**6枚**に `also_thumb:true` を立てて流用する（**`role=thumb`/`still_thumb` を作らない**・サムネ用 count キーも無い・§11）。
**このスキーマ・`counts` キー・`role` enum・`overlay` 枚数は CODEX_A（生産者）の `build_cleveland_asset_manifest.py` の出力と1バイト単位で同一。**

- **`role` enum（固定・3値のみ）:** `"body"` | `"i2v_source"` | `"reject"`。**`thumb`/`still_thumb` を作らない。**
- **`counts`（固定キー・確定値）:** `{ "still_body": 84, "still_i2v_source": 16, "motion": 16, "factory": 92, "overlay": 12 }`。
- **`overlay` = 12**（A↔B 契約値）。

```jsonc
{
  "schema_version": "cleveland_assets.v1",
  "episode_id": "PD-2026-045-cleveland",
  "slug": "cleveland",
  "generated_at": "<ISO8601>",
  "producer": "scripts/build_cleveland_asset_manifest.py",
  "is_stub": false,
  "counts": { "still_body": 84, "still_i2v_source": 16, "motion": 16, "factory": 92, "overlay": 12 },

  "stills": [
    { "asset_id": "CLEV-S01", "scene_id": "S01", "role": "body",   // "body"|"i2v_source"|"reject"（各1枚）
      "also_thumb": false,                    // body から6枚だけ true（§11 の6 asset ID・追加生成しない）
      "act": 0,                               // 0=HOOK/OP, 1..3=幕, 5=ED
      "public_path": "cleveland/img/S01.png", // ★Bが cuts[].src に入れる値（1シーン1枚＝固有プロンプト・_01 等の接尾なし）
      "depth_path": "H:/pd-media/assets/ai/cleveland/S01_depth.png",  // role=="body" は実在必須
      "width": 3840, "height": 2160,
      "sha256": "...", "tags": ["citation_stack","rubber_band","symbolic"], "caption_hint": "a thick stack of unpaid citations bound with a rubber band",
      "source": "ai_codex", "commercial_use": "allowed", "ai_disclosure_required": true,
      "qc": {"reviewed": true, "on_theme": true,
             "has_readable_text": false, "has_identifiable_face": false, "has_human_body": false, "notes": ""} }
    // i2v 種は role=="i2v_source"・asset_id "CLEV-MS01".."CLEV-MS16"・public_path は null（本編カットに出ない）
  ],

  "motion": [
    { "asset_id": "CLEV-M01", "source_scene_id": "M01_src",   // ★i2v_source 種 ID を指す（body still ではない）
      "source_still": "H:/pd-media/assets/ai/cleveland/M01_src.png",
      "public_path": "cleveland/motion/M01_rife.mp4",   // ★必ず .mp4 かつ "_rife" を含む
      "act": 0, "width": 1280, "height": 720, "fps": 48, "frames": 164, "duration_sec": 3.417,
      "sha256": "...", "tags": ["jail_door","booking"],
      "qc": {"reviewed": true, "on_theme": true, "artifact_free": true, "notes": ""} }
  ],

  "factory": [
    { "asset_id": "AF-BG-0731",
      "public_path": "cleveland/factory/AF-BG-0731__long_courthouse_corridor.mp4",  // ★必ず "/factory/" を含む
      "type": "backgrounds", "subtype": "corridor", "kind": "video",
      "license": "Pexels License", "sha256": "...", "act": 2, "covers_scene_id": "S24",
      "duration_sec": 7.60, "width": 1920, "height": 1080,
      "eyeballed_content": "a long empty courthouse corridor in cold light, no people",
      "qc": {"reviewed": true, "on_theme": true, "no_watermark": true,
             "no_recognizable_person": true, "no_cartoon": true, "label_matches_content": true, "notes": ""} }
  ],

  "overlay": [
    { "asset_id": "AF-PART-0044",
      "public_path": "cleveland/overlay/AF-PART-0044__dust_motes.mp4",
      "type": "particle_assets", "subtype": "dust_motes", "license": "Pexels License",
      "sha256": "...", "blend_hint": "screen",
      "eyeballed_content": "slow drifting dust on black, loops cleanly",
      "qc": {"reviewed": true, "on_theme": true, "no_watermark": true, "notes": ""} }
  ]
}
```

## 3.2 Bがこのマニフェストから作るもの（**EP45 spec の cuts 割当**）

| マニフェスト | Bでの使い道 | spec |
|---|---|---|
| `stills[role="body"]` 84枚 | **静止画カット100本**（`kind:"img"`, `treatment` 循環）・**各≤2回** | still distinct84/cuts100 |
| body 静止画で `also_thumb==true` の6枚 | サムネ3案の背景（§11・6 asset ID） | — |
| `stills[role="i2v_source"]` 16枚 | **本編カットに出さない**（i2v 種・A が Wan で motion 化済み） | — |
| `motion` 16本 | **i2vカット32本**（`kind:"footage"`）・**各≤2回** | motion distinct16/cuts32 |
| `factory` 92本 | **実写カット92本**（`kind:"footage"`）・**各1回のみ** | factory distinct92/cuts92 |
| `overlay` 12本 | **`cuts[].src` に出さない**（§5.5 の合成レイヤー扱い） | — |

**合計 100 + 32 + 92 = 224 カット / distinct 84+16+92 = 192 / first-use 192/224 = 0.8571 ✓（floor 0.70）**

## 3.3 `scripts/check_cleveland_asset_manifest.py`（消費側バリデータ・BLOCKING）

```bash
$PY scripts/check_cleveland_asset_manifest.py --assets <path> [--json]
```

検査（1つでも違反で exit 1。`schema_version` 違いだけ exit 2・**A の `build_cleveland_asset_manifest.py --verify` 不変条件と一字一致**）:

1. `schema_version=="cleveland_assets.v1"` / `episode_id=="PD-2026-045-cleveland"` / `slug=="cleveland"` / `is_stub==false`
2. `counts.*` が各配列の実長と一致し**確定値**: `still_body==84` / `still_i2v_source==16` / `motion==16` / `factory==92` / `overlay==12`
   （`still_body` は `stills[role=="body"]` の実長、`still_i2v_source` は `stills[role=="i2v_source"]` の実長）
3. `role` は **`body`/`i2v_source`/`reject` の3値のみ**（`thumb`/`still_thumb` 等が現れたら FAIL）
4. `role=="body"` の全静止画で `public_path` 非null、かつ `remotion/public/<public_path>` と `<stem>_depth.png` が**両方実在**
   （`CaseFilm.depthSrcOf()=src.replace(/\.[^.]+$/,'_depth.png')`。**depth 欠落はレンダークラッシュ**）。`role=="i2v_source"` は `public_path==null`
5. `role!="reject"` の全静止画で `max(width,height)>=3840`（`preflight_render_gate.MIN_LONG_EDGE_PX=3840`）
6. `motion[].public_path` が `.mp4` で終わり `_rife` を含む。`motion[].source_scene_id` は `stills[role=="i2v_source"]` の種 ID（`M01_src` 系）を指す
7. `factory[].public_path` が `/factory/` を含む
8. `overlay[].public_path` が `/overlay/` を含み `/factory/` を**含まない**・`overlay` 配列長が**ちょうど12**
9. `sha256` が全配列を通して一意（**EP39〜44 の素材と sha256 被りゼロ**も別途 A が保証・B は自集合内一意を検査）
10. `factory[].eyeballed_content` が非空、かつ `qc.label_matches_content==true`
11. `qc.has_readable_text` / `qc.has_identifiable_face` / `qc.has_human_body` が true の項目は `role=="reject"`（**R1**）
12. `also_thumb==true` の body 静止画が**ちょうど6枚**、かつ **`scene_id` 集合が `{S01,S03,S18,S46,S68,S84}` と完全一致**
   （サムネ供給・§11。**A(CODEX_A §4.2 不変条件14 / §4.3) と B で also_thumb の scene_id 集合が同一**であることを検査＝**A↔B 契約点**）
13. **全文字列値**が §2 の R-FORBID / R-FACE / R-DOCHL / R-NUM を通る

> **★このバリデータは A の `--verify` と同じ不変条件を独立実装する（二重チェック）。** counts が §3.1 の確定値と食い違ったら組まずに止めて A に差し戻す（ブリーフ§2: still を増やして factory を削るな）。

---

# 4. narration_index（TTS は課金＝禁止。**実測版を消費**する）

## 4.1 なぜ narration_index か
`build_cleveland_film.py` は**尺・区間・字幕を narration_index から導出する**。**秒数をコードに直書きしない。** 唯一の正は narration_index。

## 4.2 スキーマ（`cleveland_narration.v1`）

```jsonc
{
  "schema_version": "cleveland_narration.v1",
  "episode_id": "PD-2026-045-cleveland",
  "is_stub": false,
  "total_seconds": 713.9,        // = SPEC narration_seconds（[DESIGNED SILENCE 1..3] の実音無音を含む）
  "chunks": [
    { "section": "HOOK", "start": 0.000, "end": 4.100, "text": "..." },
    { "section": "OP",   "start": 25.000, "end": 29.100, "text": "..." },
    { "section": "ACT_1","start": 55.000, "end": 59.200, "text": "..." }
  ]
}
```

**section 値（固定・5幕）:** `HOOK` / `OP` / `ACT_1` / `ACT_2` / `ACT_3` / `ENDING`。
（EP45 の BODY は 3幕＝ACT_1「The road that ends at a cell」/ ACT_2「The machine that turns a debt into a sentence」/ ACT_3「Bearden, and the difference between a right and a remedy」。**ACT_4 は無い。**）
`build_cleveland_film.py` は `section_windows()`（各 section の最初のチャンク start）で幕境界を得る。

**台本の `【DESIGNED SILENCE …】` は3箇所**（HOOK 1.8s／ACT1 1.5s＝完全無音／ENDING 2.2s＝音を足す沈黙）。narration_index の実測がこの無音を **total_seconds に内包**している。`【beat】` は小ギャップ。**存在しない演出マーカーを発明しない。**

## 4.3 spec のタイムライン（**設計目標。実タイミングは narration_index が上書きする**）

| section | 語数 | 秒 | 備考 |
|---|---|---|---|
| HOOK | 73 | 24.6 | VO。末尾に `DESIGNED SILENCE 1.8s`（閉じた留置扉の残響のみ・完全無音） |
| （crimson `BrandOpening`） | 0 | 3.5 | 非VO。`OPENING_SEC`。**frame0 ではなく HOOK 後に挿入** |
| OP | 64 | 21.6 | 二人称の問い（thesis）＋ channel ID |
| ACT_1 The road that ends at a cell | ~ | ~ | 最短・抑制。途中に `DESIGNED SILENCE 1.5s`（booking の時計・完全無音） |
| ACT_2 The machine | ~ | ~ | JCS・$200/$40 skim・counsel 不在・~38,000/4州 |
| ACT_3 Bearden | ~ | ~ | 判例核。**最も遅く長い**。Williams/Tate→Bearden / O'Connor 逐語 / holding の限定 / 下級審の 2014 和解 |
| ENDING | 412 | 138.8 | ペイオフ→CTA。途中に `DESIGNED SILENCE 2.2s`（廊下のハム→ドアの採光・音を足す沈黙） |
| （`BrandEndcard`） | 0 | 9.0 | 非VO。`ENDCARD_SEC` |

**唯一の正は `python scripts/check_script_length.py <script> --json`。** 総語数 **2,119**（spec `words_total`）/ `wpm 178.1` /
narration_seconds **713.9**（spec）。**自己申告・体感の尺判定は禁止。**

## 4.4 実測 narration_index の受領
本番は別工程が TTS→faster-whisper で `06_audio/narration_index.v001.json`（実測語タイム・`is_stub:false`）を作る。
**これは課金ジョブなので B は起動しない。** 来た `narration_index.v001.json` を `--narr` に渡すだけ。**台本本文はそのまま（改変しない）。**

---

# 5. `cleveland_film.json` の構築（`scripts/build_cleveland_film.py`＝`build_caniglia_film.py` の複製・実素材のみ）

## 5.1 `FilmData` 型（`CaseFilm.tsx` から。これに従う）

```ts
export type Cut = {start:number; dur:number; kind:'img'|'footage'; src:string; treatment:string; seed:string};
export type FilmData = {
  fps:number; narration:string; narrationSeconds:number; hookSeconds:number; hookLine:string;
  hook:{start:number;dur:number;kind:string;src:string;seed:string}[];
  cuts:Cut[]; captions:{start:number;end:number;text:string}[];
  graphics:{start:number;end:number;lines:string[]}[];      // 必須フィールド。EP45 は []
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
- **`fps = 30`**（EP44 と同じ film fps）。`narration = "cleveland/narration.mp3"`（実在）

### 5.1.1 ★durationInFrames の4項関数（明示・total ≤ 750s を assert）

```
caseFilmDurationInFrames(clevelandFilm, fps=30)
  = round(hookSeconds * fps)        // hookSeconds = 0.0（HOOK の VO は narrationSeconds に含む。frame0 に別 hook 尺を積まない）
  + round(OPENING_SEC * fps)        // OPENING_SEC = 3.50（crimson BrandOpening は HOOK の後）→ 105
  + ceil(narrationSeconds * fps)    // narrationSeconds = narration_index.total_seconds（= 713.9・silence 込み）→ ceil(21417)=21417
  + round(ENDCARD_SEC * fps)        // ENDCARD_SEC = 9.00 → 270
```

- **hookSeconds を明示: `hookSeconds = 0.0`**（HOOK ナレは narrationSeconds に内包・§4.2 の section=HOOK。frame0 に独立 hook モンタージュ尺を積まない）。
- 概算（fps30・narration 713.9）: `0 + 105 + 21417 + 270 = 21792 frames = 726.4s`。**id=Ep45Cleveland の durationInFrames は 21792。**
- **ビルダ末尾で `assert total_frames/fps <= 750.0`**（726.4 ≤ 750 ✓）。超えたら exit 1。

## 5.2 カット構成（**§3 マニフェストから機械的に組む・紙芝居回避が最優先**）

```
総カット 224 = factory 92 (footage) + motion 32 (footage) + 静止画 100 (img)

[A] first-use share（check_asset_reuse floor 0.70）
    distinct 92+16+84 = 192 → 192/224 = 0.8571            ✓ >=0.70（spec first_use_share と一致）

[B] per-asset cap（check_asset_reuse）
    factory: 92/92  = 1.00回  ✓ <=1（★factory は再使用禁止）
    motion : 32/16  = 2.00回  ✓ <=2
    still  : 100/84 = 1.19回  ✓ <=2

[C] animation_mix（★2つの尺度を両方満たす）
    (i) cut数ベース   still-share = 100/224 = 0.4464        ✓ <=0.45（★余裕が薄い＝下の警告）
        motion coverage = (92+32)/224 = 124/224 = 0.5536   ✓ >=0.45（spec と一致）
    (ii) frame ベース still 平均 3.00s → 100×3.00 = 300.0s
        footage 平均 ~3.34s → 124×3.34 ≈ 414.2s
        still-frame-share = 300.0 / 713.9 = 0.4202          ✓ <=0.45（cut数比より安全側）
        motion-coverage(frame) = 414.2 / 713.9 = 0.5802     ✓ >=0.45

[D] 平均ショット長（spec mean_shot 3.19 / max 6.0）
    713.9 / 224 = 3.187 秒/カット                           ✓ <=6

[E] factory 下限（30秒に1本 = 24 → >=24本） 92本            ✓
```

> **★[C](i) の cut数ベース still-share 0.4464 は cap 0.45 に薄い（余裕 0.36%）。still を1枚増やすか factory を1本削ると 0.45 を超える。**
> **マニフェストが still 84 / factory 92 / motion 16 を割ったら組まずに止めて A に差し戻す（ブリーフ§2: still を増やして factory を削るな）。**
> **frame ベースも下回るよう、still の平均尺を footage より系統的に短く保つ（§5.3-5）。**

## 5.3 カット割り当てのルール（`build_caniglia_film.py` の `allocate()`/`tile_window()` を踏襲）

1. 各幕の秒窓を `section_windows()` から取り、幕内に **factory : motion : still を按分**して配置
   （★下表は**非拘束の目安**。実配分は narration_index の窓長で自動調整。確定値は「合計 factory 92 / motion 32 / still 100」だけ）:

   | section | factory | motion | still | 小計 |
   |---|---|---|---|---|
   | HOOK+OP | 9 | 4 | 15 | 28 |
   | ACT_1 | 12 | 6 | 14 | 32 |
   | ACT_2 | 19 | 8 | 22 | 49 |
   | ACT_3 | 33 | 8 | 30 | 71 |
   | ENDING | 19 | 6 | 19 | 44 |
   | **計** | **92** | **32** | **100** | **224** |

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
`cleveland_film.json` に **`overlays` 独自キー**で持たせる（`CaseFilm` は未知キーを無視）か、専用レイヤーで `screen` 合成する。

## 5.6 ビルダが出力する成果物（**asset_map→provenance変換＋beatsheet生成**）

| 出力 | パス |
|---|---|
| film.json | `remotion/src/data/cleveland_film.json` |
| public コピー | `remotion/public/cleveland/film_data.v001.json` |
| **build provenance**（asset_map→provenance変換） | `episodes/PD-2026-045-cleveland/04_scenes/cleveland_build_manifest.v001.json`（**A の `05_visuals/asset_manifest` に書かない**） |
| **beatsheet**（figures+AE区間の突き合わせ表） | `episodes/PD-2026-045-cleveland/04_scenes/cleveland_beatsheet.v001.json` |
| SRT（字幕未生成時のフォールバック） | `episodes/PD-2026-045-cleveland/08_edit/captions.final.v001.srt`（**§8 の生成器が上書きする**） |

> **★beatsheet の命名に関する重大な注意:** `check_motion_density` / `check_animation_mix` は
> `04_scenes/premium_beatsheet.v*.json` を**自動検出して film.json より優先**する。
> **B の beatsheet は `cleveland_beatsheet.v001.json`（`premium_` を付けない）** にして、**ゲートの測定源を film.json 一本に保つ**
> （二重ソースの乖離＝EP39/40 の矛盾28件の原因を避ける）。`cleveland_beatsheet` は provenance と `validate_cleveland_beats` 専用。

## 5.7 CLI
```bash
$PY scripts/build_cleveland_film.py \
  --assets episodes/PD-2026-045-cleveland/05_visuals/asset_manifest.v001.json \
  --narr   episodes/PD-2026-045-cleveland/06_audio/narration_index.v001.json \
  --out    remotion/src/data/cleveland_film.json \
  [--captions episodes/PD-2026-045-cleveland/08_edit/captions.final.v001.srt]
```
**実素材のみ。`is_stub==true` のマニフェストを渡されたら exit 1（このスレッドは stub を使わない）。** 末尾に `check_asset_reuse` 相当の自己レポートを print する。

---

# 6. Remotion 側 `figures[]`（**36本・spec floor 30 に +6・`graphics[]=[]`・dochighlight 不使用**）

## 6.1 密度の検算（`check_motion_density`・**AEカードは1本も数えられない**）

```
figures 36本（film.json） / body 11.898分(=713.9/60) = 3.03 /分     ✓ beats_per_min_floor 2.5
coverage: 36本 × 平均6.0s = 216.0s / 713.9 = 30.3%                  ✓ MIN_ANIMATED_COVERAGE 0.25
variety : 下記 kind を13種使用                                      ✓ variety_floor 3
spec motion.beats_floor = 30 に対し 36 で余裕。coverage が最も薄いので figures の dur は 5.4–6.0s を基本に。
```

> **★3軸すべて AND。density/coverage/variety のどれか1つでも floor 未満で FAIL。**
> 36本を非重複で置き、平均 dur を 6.0s 程度に確保すること（coverage が floor 0.25 に一番近い）。

## 6.2 ★★★ `FigureSpec` の `kind` は**実在する小文字値のみ・`dochighlight` は使わない** ★★★

> **大文字名（`ActTitle`/`QuoteCard`/`VoteTally`…）は `FigureBeats.tsx` の union に無く、無言で描画が消える。**
> **`comparebars` は存在しない → `compbars` を使う。**
> **★`dochighlight` を1本も使わない**（黒バー/box/underline がバグに見える＝3回指摘・R-DOCHL）。判読ハイライトの意図は `quote`/`stat`/`lowerthird`/`kinetic` で代替する。

**EP45 で使う実在 `kind`（`remotion/src/components/FigureBeats.tsx` の union から。全て `start`/`end` 必須・全小文字）:**

| `kind` | 必須プロパティ | EP45での用途 |
|---|---|---|
| `numberticker` | `value:number` / `label?` / `prefix?` `suffix?` `decimals?` | ~38,000（N05・別区間）/ 31 DAYS（N01）/ SETTLED 2014（N14） |
| `stat` | `value:number` / `label:string` / `prefix?` `suffix?` `topLabel?` | $1,554 OR 31 DAYS（FFJC 帰属）/ NO ABILITY-TO-PAY HEARING / $200 A MONTH / ~38,000 / 100+ AL COURTS / SETTLED 2014-LOWER COURT |
| `timeline` | `events:{year:string;text:string}[]` | ①Cleveland 雪だるま ②JCS: 2001→2012 Harpersville→2013→2015 SPLC→2015 閉鎖 ③判例: 1970 Williams→1971 Tate→1983 Bearden ④救済: 収監→下級審提訴→late 2014 和解（★最高裁でない・C-2） |
| `quote` | `quote:string` / `attribution:string` | O'Connor 逐語（F07）/ Harrington 逐語（F14）/ 和解条項 逐語（F18）（**帰属必須**・R-ATTRIB） |
| `kinetic` | `lines:string[]` / `style?:'wordpop'\|'maskslide'\|'emphasis'` / `emphasisWords?` | 決め所テキスト（**emphasisWords は1–2語=文字切れ回避**） |
| `lowerthird` | `primary:string` / `secondary?` / `accent?` | 開示 `AI-assisted visualization` / Bearden 461 U.S. 660 / Williams / Tate / JCS 2001 Georgia / 第14修正 |
| `acttitle` | `title:string` / `kicker?` / `index?` | 幕頭「The road that ends at a cell」/「The machine」/「Bearden」 |
| `compbars` | `items:{label:string;value:number;accent?}[]` | ①$200 vs $40 skim（N03/N04・帰属）②罰金 sits→grows ③**Bearden で閉じたもの（能力なしだけの審問なし収監）vs 許されるもの（罰金・手数料・賠償）**（C-3・"fines still allowed" 側を必ず併記＝R-HOLDING） |
| `bar` | `items` or `value` | ①$40/月 skim の累積 ②免許停止→無職→債務が上へ climb（ENDING の cruelty・C-4 尊厳保持） |
| `mechanism` | `mechanism:'closingdoor'\|'gears'\|'faultsplit'` ★discriminant は `kind`・変種は `mechanism` | ①offender-funded ループ(gears)②利益相反(gears)③counsel 不在＝空席(faultsplit)／留置扉(closingdoor) |
| `pindropmap` | `pins:{x,y,label?}[]` | Montgomery, Alabama（単一ピン・C-4 顔なし・F16） |
| `regionmap` | `label?` / `regions[]` | JCS 4州（N06・"across four states" の限定・過大化しない） |
| `routemap` | `label?` / `pins:{x,y,label?}[]` | 「the road that ends at a cell」＝免許停止→運転継続→追加切符→命令→留置（ACT1 の因果の道・象徴） |

**`quote[].attribution` は §2 の `APPROVED_QUOTES` に一致させる。逐語のみ・要約を引用符に入れない。**
**★`kind` に `dochighlight` を1件も置かない（R-DOCHL・`check_cleveland_facts` が grep で 0 を確認）。**

## 6.3 figures 配分（★DESIGN §7.2 と一致・33 figures + 3 graphics-role = **全 36 を figures[]**・graphics[]=[]）

| kind | 枠数 |
|---|---|
| `acttitle` | 3 |
| `timeline` | 4 |
| `stat` | 6 |
| `quote` | 3 |
| `lowerthird` | 3 |
| `compbars` | 3 |
| `mechanism` | 3 |
| `bar` | 2 |
| `pindropmap` | 1 |
| `regionmap` | 1 |
| `routemap` | 1 |
| `numberticker` | 3 |
| `kinetic`（DESIGN 上 graphics-role 3枠を figures[] に統合） | 3 |
| **合計** | **36**（variety = 13 種・**dochighlight を含めない**） |

> **★実装表現:** 上記 36本を**すべて `figures[]`** に入れ、**`graphics[]=[]`** にする（`check_motion_density` は `figures+graphics+heroCuts` を合算するので密度は同値・floor 30 に +6）。「figures 33/graphics 3」は DESIGN 上の役割分類であり、film.json 上は全 36 が figures[]・graphics[] は空配列。

## 6.4 figures アンカー設計（`build_caniglia_film.py` の `FIGURE_ANCHORS` 方式）

**方式:** `(anchor_sec, payload)` の配列を秒昇順に置き、`build_figures()` が
`end = min(anchor+FIG_DUR, next_anchor-FIG_GAP, total-0.5)` でクランプ、`end-start < FIG_MIN_DUR` なら **exit 1**。
`FIG_DUR=6.0 / FIG_MIN_DUR=3.0 / FIG_GAP=0.4`。**アンカー秒は narration_index の section 窓に対する相対で決め、`section_windows()` を基準にオフセットで置く**（秒直書き禁止）。

**配置方針（36本・§2 台帳の値だけを焼く・kind を分散して variety を稼ぐ・6制約順守・dochighlight 不使用）:**

- **HOOK/OP（4）:** `lowerthird`（`AI-assisted visualization` 開示）/ `kinetic`（"THE PRICE OF BEING POOR"）/ `pindropmap`（**F16 Montgomery, Alabama**・単一ピン）/ `mechanism:closingdoor`（閉じた留置扉）
- **ACT_1（8）:** `acttitle`（THE ROAD THAT ENDS AT A CELL）/ `routemap`（免許停止→運転→追加切符→命令→留置）/ `stat`（**F09 $1,554**, suffix "OR 31 DAYS", topLabel "PER FINES & FEES JUSTICE CENTER"／C-6 medium ヘッジ）/ `numberticker`（**F09 31** DAYS・AE m01 と別区間）/ `stat`（**F04 NO ABILITY-TO-PAY HEARING**, label "before jail — Could she pay?"／C-3 の核）/ `compbars`（罰金 sits→grows vs 変わらない・雪だるまの重み）/ `timeline`（Cleveland 雪だるま: 切符→免許停止→無免許運転→$1,554→収監）/ `bar`（免許停止→無職→債務が上へ climb・C-4 尊厳）
- **ACT_2（10）:** `acttitle`（THE MACHINE）/ `lowerthird`（**F13 JCS · founded 2001 · Georgia** offender-funded）/ `compbars`（**F05 $200 / MONTH vs $40 TO THE COMPANY**, topLabel "PER FINES & FEES JUSTICE CENTER"／C-6）/ `bar`（$40/月 skim の累積）/ `mechanism:gears`（offender-funded ループ court→company→$40 skim）/ `mechanism:gears`（利益相反: ability-to-pay 判断を会社従業員に委任・HRW・C-5 制度批判）/ `stat`（**F06 ~38,000**, label "people · across four states"／C-6 "four states" 限定を削除禁止）/ `regionmap`（**F06 four states**・限定の地理）/ `stat`（**F06 100+**, label "Alabama courts, by 2013"）/ `quote`（"a judicially sanctioned extortion racket" → "Judge Hub Harrington"／**F14・C-5・R-ATTRIB・R-ATTACK**）
- **ACT_3（9）:** `acttitle`（BEARDEN）/ `timeline`（**F10 1970 Williams → F11 1971 Tate → F01 1983 Bearden**）/ `lowerthird`（**F01 Bearden v. Georgia, 461 U.S. 660 (1983)**）/ `lowerthird`（**F10 Williams v. Illinois, 399 U.S. 235 (1970)** ／ **F11 Tate v. Short, 401 U.S. 395 (1971)** を2行で）/ `quote`（"it is fundamentally unfair to revoke his probation automatically, without even considering whether an adequate alternative to prison exists" → "Justice O'Connor, for the Court"／**F07・C-3・R-ATTRIB**）/ `compbars`（**F02 CLOSED: jail for inability with no hearing** vs **STILL ALLOWED: fines · fees · restitution / willful refusal**／**C-3・R-HOLDING・"fines still allowed" 側を併記**）/ `lowerthird`（**F17 Fourteenth Amendment** — due process ＋ equal protection converge）/ `compbars`（**F12 $500 fine + $250 restitution**・Bearden の事実文脈のみ）/ `mechanism:faultsplit`（counsel 不在＝空席の弁護人席・"could she pay?" の声が卓に不在・C-4/C-3）
- **ENDING（5）:** `kinetic`（"UNCONSTITUTIONAL SINCE 1983 — YET IT CONTINUED"・emphasisWords=["CONTINUED"]／**C-1 enforcement failure**）/ `stat`（**F03 SETTLED 2014**, label "a lower court, not the Supreme Court"／**C-2 限定同梱**）/ `timeline`（**F03/F15** 救済: 収監→下級審提訴→late 2014 和解→契約終了／2015 SPLC RICO→JCS AL 全事業閉鎖・★最高裁でない・C-2）/ `numberticker`（**F03 2014** SETTLED・下級審ラベル同梱・C-2）/ `lowerthird`（開示 `AI-assisted visualization` 再掲）

> **★enforcement failure（C-1）を出す ENDING の payload には必ず "YET IT CONTINUED"/"the rule held" 系を同梱。「it is legal」「no longer exists」を書かない。**
> **SETTLED 2014（F03）は "a lower court, not the Supreme Court" を同一 payload に（C-2・R-SCOTUS）。** **Bearden の compbars は "fines · fees · restitution STILL ALLOWED" 側を必ず併記（C-3・R-HOLDING）。**
> **★988 を figures に置かない（このエピソードは 988 でなく legal-aid・description のみ）。**

## 6.5 配置ルール
1. **AEの区間（§7.2）と1秒でも重ならない**（`validate_cleveland_beats` が突き合わせ）
2. **同じ kind を連続させない**（`mechanism` の直後に `mechanism` を置かない）
3. 1枠 **5.4–6.0秒**
4. `quote[].quote` / `kinetic[].lines` / `*.label` は §2 の R-LEDGER(R-NUM)・R-ATTRIB・R-FORBID・R-LEGAL・R-SCOTUS・R-HOLDING・R-ATTACK・R-FACE・R-DOCHL 検査対象
5. 台帳外の数値を `value`/`numKeys` に置かない（**焼いたら R-NUM で FAIL**）
6. **`emphasisWords` は1–2語の短句のみ**（長句は AE/Remotion で末尾が切れる＝EP40 実害）
7. **`kind` に `dochighlight` を1件も置かない（R-DOCHL）**

---

# 7. After Effects カード（`build_cleveland_hero_cards.py` / `composite_cleveland_hero.py`）

## 7.1 位置づけ
AEカードは **film.json とは別**に ffmpeg で本編に焼き込む（§0.5-2＝密度に数えられない）。
`build_young_hero_cards.py` を**コピーしてパス・定数・CARDS デッキだけ差し替える**。レイアウト実装・
`money_keys()`・`fit_size()`・完了マーカー・機械の罠対処は**1行も削らない**。

## 7.2 AEカードデッキ（**単調増加・重複ゼロ・台帳裏付けのみ・6制約順守。この表が契約。8枚**）

**区間の秒は本番の rendered base（narration_index 由来）に一致させる。** 下表の秒は spec タイムライン基準の**目安**で、
`build_cleveland_hero_cards.py` は section 窓からオフセットで算出しクランプする。**背景静止画は象徴オブジェのみ（R1/C-4）。**
**★この表は DESIGN §6.3/§6.4 と id・レイアウト・F-ID・順序（start 昇順）が一字一致。** 988 は AEデッキに入れない（このエピソードは legal-aid）。

| id | レイアウト（**実装済み・§7.3・本EPは5種のみ**） | hero/main（主表示） | top / bottom / attribution | F-ID | 背景（象徴のみ） | required |
|---|---|---|---|---|---|---|
| m01 | CENTER_STACK | **$1,554** | top: **THE COURT ORDER** / bottom: **OR 31 DAYS - PER FINES & FEES JUSTICE CENTER** | F09 | 裁判所命令の書面（判読不能・crimson） | 必須 |
| h01 | CENTER_STACK | **COULD SHE PAY?** | top: **THE QUESTION NEVER ASKED** / bottom: **NO ABILITY-TO-PAY HEARING BEFORE JAIL** | F04 | 空の弁護人席／閉じる留置扉 | 必須 |
| t01 | ACT_TITLE_CARD | **THE MACHINE** | kicker: **ACT TWO** | — | 支払台帳／請求書（ロゴぼかし） | 必須 |
| j01 | SPLIT_COMPARE | left: **$200 / MONTH** / right: **$40 TO THE COMPANY** | top: **OFFENDER-FUNDED PROBATION** / bottom: **JUDICIAL CORRECTION SERVICES - PER FINES & FEES JUSTICE CENTER** | F05 | 左=支払窓口 / 右=会社の取分の封筒 | 必須 |
| s01 | CENTER_STACK | **~38,000 PEOPLE** | top: **ONE COMPANY, BY 2013** / bottom: **ACROSS FOUR STATES** | F06 | 4州の地図片（判読不能） | 必須 |
| d01 | DATE_STAMP | **MAY 24, 1983** | place: **BEARDEN v. GEORGIA - 461 U.S. 660** | F08 | 大理石の最高裁列柱（顔なし） | 必須 |
| q01 | QUOTE_CARD | **"IT IS FUNDAMENTALLY UNFAIR TO REVOKE HIS PROBATION AUTOMATICALLY, WITHOUT EVEN CONSIDERING WHETHER AN ADEQUATE ALTERNATIVE TO PRISON EXISTS"** | attribution: **JUSTICE O'CONNOR, FOR THE COURT** | F07 | 大理石の第14修正（判読困難・顔なし） | 必須 |
| r01 | CENTER_STACK | **YET IT CONTINUED** | top: **UNCONSTITUTIONAL SINCE 1983** / bottom: **CLEVELAND SETTLED 2014 - A LOWER COURT, NOT THE SUPREME COURT** | F03 | 大理石／折り畳まれた和解書（2014） | 必須 |

> **★行順＝start 昇順（時系列）:** `m01`(ACT1) < `h01`(ACT1) < `t01`(ACT2 幕頭) < `j01`/`s01`(ACT2) < `d01`/`q01`(ACT3) < `r01`(ACT3→END)。
> **m01/j01 は "PER FINES & FEES JUSTICE CENTER" を削除禁止**（C-6・medium ヘッジ）。**s01 の "ACROSS FOUR STATES" 限定を削除禁止**（C-6・過大化しない）。
> **q01 の quote は逐語のみ**（§2 `APPROVED_QUOTES` と一致・要約を引用符に入れない・C-3）。
> **r01 の "YET IT CONTINUED"（enforcement failure・C-1）＋ "A LOWER COURT, NOT THE SUPREME COURT"（C-2）を削除禁止。**
> **どのカードにも「it is legal」「Supreme Court saved Cleveland」「all fines unconstitutional」を書かない**（C-1/C-2/C-3）。**988 を AE カードにしない。** 数値ID＝台帳（§2.2）と一致必須。カウント終了から区間終端まで最低 **1.20秒**ホールド。

**検算（Codex は自分で再計算して一致を確認）:** 8区間・単調増加・重複ゼロ・HOOK(0–24.6) と ENDCARD(末尾9s) に重ねない。
Remotion figures(§6) と1秒も重ならない（`validate_cleveland_beats` が検査）。

## 7.3 レイアウト（`build_young_hero_cards.py` の実装を踏襲・**実装済みレイアウト名だけを使う**）
複製元 `build_young_hero_cards.py` が実装するレイアウトは**この8種**:
`DATE_STAMP` / `CENTER_STACK` / `MONEY_STACK` / `SPLIT_COMPARE` / `ACT_TITLE_CARD` / `QUOTE_CARD` / `VOTE_SPLIT` / `SEAM_TRANSITION`。
**§7.2 デッキが使うのは field スキーマが既知の 5種のみ**（`CENTER_STACK` / `SPLIT_COMPARE` / `DATE_STAMP` / `ACT_TITLE_CARD` / `QUOTE_CARD`）。
**★`VOTE_SPLIT` は使わない**（Bearden の得票は台帳に無い＝捏造禁止・C-6）。**`MONEY_STACK` / `SEAM_TRANSITION` も本 EP では未使用**（金額は `CENTER_STACK`/`SPLIT_COMPARE` で表現）。
**上記5種以外のレイアウト名を発明しない（`validate_cleveland_beats` §7.9 ルール3 で FAIL）。dochighlight をレイアウト名に使わない。**
**共通レイヤースタック・Anton/Oswald・`psName()` の runtime 解決（allFonts の array-LIKE ラッパーを unwrap）は複製元と同一。**

**★共通レイヤースタックに AI開示レイヤーを1枚追加（R1・全カード常時焼き）:** 最上位に近い固定レイヤーとして
`AI-assisted visualization`（Oswald 20px / SILVER `#C8CDD6` / opacity 70% / 右下 `[W-32, H-28]`）を全カードに焼く。
AEカードは不透明の全画面 mp4 として本編に overlay されるため、これが無いと本編(Remotion)右下の開示が隠れる（**R1 違反**）。字幕帯とは縦56px 以上離す。

**★EP45 色定数（0..1 float・crimson レーン色。EP41 gold / EP42 blue / EP43 amber / EP44 teal を流用禁止・DESIGN と一致）:**
```python
ACCENT = [0.698, 0.227, 0.282]  # #B23A48 crimson（督促の朱）アクセント（数値・下線・レーン分離）
WHITE  = [0.961, 0.969, 0.980]  # #F5F7FA
SILVER = [0.784, 0.804, 0.839]  # #C8CDD6（開示テキスト）
INK    = [0.039, 0.039, 0.047]  # #0A0A0C 近黒ルート（サムネ bg と一致）
```
> **accent は必ず `#B23A48`（他話色を書かない）。** サムネ・OP props・AEカードの accent は全て `#B23A48`。

**数値カードは全て `money_keys()` 系で表示文字列を Python 事前計算**（JSX で算術しない＝EP38 確定ルール）。
**`m01`（$1,554）は数字を先に、間を置いて "OR 31 DAYS" を出す。`j01`（$200/$40）は左右2値を別レイヤー（改行禁止）。`s01` は "~38,000" と "ACROSS FOUR STATES" を別レイヤー。**
**`r01`（enforcement failure）は "UNCONSTITUTIONAL SINCE 1983" → "YET IT CONTINUED" → "A LOWER COURT, NOT THE SUPREME COURT" を別レイヤーで（C-1/C-2）。**

## 7.4 `beats.json` スキーマ（本番 `08_edit/ae_hero/beats.json`）
`build_young_hero_cards.py` の beats スキーマに準拠。トップに **`film_offset_sec`**（本編ナレ開始からのオフセット・§7.10 のコンポジタが読む）。各 beat に `id` / `layout` / `start` / `end` / `dur` /
`still`(象徴 or null) / `hero`/`main`(主表示文字列) / `top` / `bottom` / `left` / `right` / `kicker` / `date` / `place` / `caption`(**改行禁止・最大50字**) /
`value` / `numKeys` / `blend_mode`(既定 "overlay") / `required` / `out` / `attribution`(**QUOTE_CARD=q01 は必須**・§2 `APPROVED_QUOTES` と一致・R-ATTRIB)。
**`value` / `main` / `hero` の数値は §2 台帳の `verified:true` 値のみ**（`check_cleveland_facts` が照合）。
**`r01` は R-SCOTUS を満たす "lower court" ＋ "not the Supreme Court" を持つ。Bearden 文脈のカードは holding 限定語を持つ（R-HOLDING）。`beats.json` に `dochighlight` を出さない（R-DOCHL）。**

## 7.5 このマシン固有の罠（複製元が対処済み。**1つも省くな**）
1. `setTemporalEaseAtKey` の配列次元は **spatial(Position) で 1**（`if(!prop.isSpatial){...}` で分岐）
2. RS = **`"最良設定"`** / OM = **`"H.264 - レンダリング設定を一致 - 15 Mbps"`**（英語名は try/catch フォールバックのみ）
3. TextDocument の改行は `\n` 不可。**`caption` は1行**（改行が要るなら別レイヤー・SPLIT_COMPARE の左右2値は別レイヤー）。**テキスト幅は `sourceRectAtTime(t,false).width` で実測**（advance-width 推定は禁止＝EP40 の文字切れ原因）。em-dash は `-`
4. `app.newProject()` は headless でハング。**使わず**同名 `CLEVELAND_` コンプを防御削除
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
$PY scripts/ae/build_cleveland_hero_cards.py
"C:/Program Files/Adobe/Adobe After Effects 2026/Support Files/AfterFX.exe" -noui \
  -r ".../episodes/PD-2026-045-cleveland/08_edit/ae_hero/cleveland_hero.jsx"
# render/_build_ok.txt を待つ（最大300秒）→ render/*.mp4 が8本揃うまで待つ（最大1200秒）
$PY scripts/ae/composite_cleveland_hero.py
```

## 7.9 `scripts/validate_cleveland_beats.py`（BLOCKING）
1. `beats[].start` 昇順・区間非重複
2. 全 `start`/`end` が本編ナレ区間内（HOOK 0–24.6 と ENDCARD 末尾9s に重ねない）
3. `layout` が §7.3 の**実装済み5種**（`CENTER_STACK`/`SPLIT_COMPARE`/`DATE_STAMP`/`ACT_TITLE_CARD`/`QUOTE_CARD`）のいずれか。**この5種以外（`VOTE_SPLIT`/`MONEY_STACK`/`SEAM_TRANSITION`/`dochighlight` 等）は FAIL。** still が必要なレイアウトで null なら FAIL
4. `still` 非null は実在＋長辺 >=3840px
5. `hero`/`main`/`top`/`bottom`/`left`/`right`/`caption`/`value` が §2（R-FORBID/R-NUM/R-ATTRIB/R-LEGAL/R-SCOTUS/R-HOLDING/R-ATTACK/R-FACE/R-DOCHL/R-DATE）を通る
6. `verified:false` の値を要求するカードは `required:false` で**除外**、`required:true` なら exit 1
7. **`cleveland_film.json` の `figures[]`（§6）と AE の区間が1秒でも重ならない**
8. `caption` に改行が含まれない
9. **AI開示レイヤーの存在（R1）** — ビルダが全カード共通スタックに `AI-assisted visualization`（右下・§7.3）を焼く設定であることを静的に確認。無ければ FAIL。受入アイボール（§13.1）でも「AEカード表示中も右下の開示が見える」を確認
10. **`dochighlight`/`DOCHIGHLIGHT` が beats/レイアウト名に1件も無い（R-DOCHL）**

## 7.10 基底 mp4 とコンポジタ（`build_cleveland_bgm.py` → `composite_cleveland_hero.py`）
```
# 完成後の合成順（ブリーフ§5）: build_cleveland_bgm.py（narration+BGM）→ composite_cleveland_hero.py（AEカード焼込み・film_offset_sec 適用）
BASE = episodes/PD-2026-045-cleveland/08_edit/cleveland_final_bgm.v002.mp4     # build_cleveland_bgm.py が生成
OUT  = episodes/PD-2026-045-cleveland/08_edit/cleveland_final_bgm.v003_ae.mp4  # composite_cleveland_hero.py が生成
FFMPEG  = C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe
FFPROBE = C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffprobe.exe
W,H,FPS = 1920, 1080, 30
```
**`composite_cleveland_hero.py` は `beats.json` の `film_offset_sec` を読み、各 beat 区間を本編尺にマップする**（`composite_young_hero.py` と同経路）。
**SKIP4条件を1行も削らない:** ① `render/<id>.mp4` 不在 ② 解像度 != 1920x1080 ③ 実測尺 `< dur-0.3` ④ `film_offset_sec + beat.end > base_dur`。
SKIP された区間は元カットのまま残る（作品は壊れない）。**何枚 SKIP したかを stderr に必ず出す。**
ffmpeg は `overlay=0:0:eof_action=pass:enable='between(t,start,end)'`（`blend_mode` が screen/multiply の時のみ `blend`）。
**出力後 `probe_dur(OUT)` でベースとの尺差 <=0.5秒を確認。出荷済みは絶対に上書きしない（必ず `_v003_ae`）。**

---

# 8. 字幕の切断規則（`scripts/gen_captions_cleveland.py`＝`gen_captions_caniglia.py` の複製）

## 8.1 原則
**文字数は「上限」であって「分割基準」ではない。** `gen_captions_caniglia.py` の `internal_split()` / `chunk_sentence()` を**そのままコピー**。
`from fix_caption_dangling import NO_DANGLE_END, wrap as safe_wrap`（**語リストを自前で書き直さない**）。

## 8.2 通すゲート `scripts/check_caption_breaks.py`（**閾値を緩めるの禁止**）
- **A. 行末の機能語**（複数行キューの最終行以外が句読点なしで `NO_DANGLE_END` の語で終わる）= 0件
- **B. 孤立キュー**（語数<3 で「終端句読点で終わる」「大文字で始まる」の両方を満たさない）= 0件
- **C. 句をまたぐ切断(hard)** = 0件
- A/B/C いずれか1件で FAIL（**実質ゼロ許容**）

## 8.3 EP45 の入力と対応
- 入力は **narration_index の各チャンク文**（`--narr`）。**字幕テキストは台本本文と1:1対応**（§0.5-5）。台詞・別エピソード文の混入禁止。verbatim で使い、構文境界で分割するだけ。
- `ABBR` に `U.S.` / `v.` / `Mr.` / `Ms.` / `No.` 等を持つ（`Bearden v. Georgia` の `v.`、`461 U.S. 660` の `U.S.`、`399 U.S. 235` / `401 U.S. 395` の `U.S.` で文を切らない）。
- タイミングは narration_index の start/end。CPS <=27・最小表示 0.90秒。**Step で決めた境界を時間都合で動かさない。**
- **字幕にも R-FORBID 適用**（台本本文に禁止語は無いので verbatim なら自然に通るが、`check_cleveland_facts` の対象でもある。§2.1 の注意：否定/正確文脈の近似語を禁止語に足さない）。

## 8.4 セルフテスト（`--selftest`・EP38 実害を回帰に）
`Bearden v. Georgia` / `461 U.S. 660` / `399 U.S. 235` / `401 U.S. 395` で文が切れないこと、
機能語で終わるキュー・孤立キューを作らないことを含む4ケースを実装し、
**出力を `check_caption_breaks.py` に食わせて exit 0 まで自動確認。**

## 8.5 実行
```bash
$PY scripts/gen_captions_cleveland.py --narr episodes/PD-2026-045-cleveland/06_audio/narration_index.v001.json
$PY scripts/check_caption_breaks.py episodes/PD-2026-045-cleveland/08_edit/captions.final.v001.srt
# → PASS が出るまで直す。ゲート側の閾値を緩めるのは禁止。
```

---

# 9. 5ゲートの実際の判定（**build 後に必ず全部通す・animation_mix を忘れるな**）

| ゲート | 実体 | 入力 | EP45 の通過根拠 |
|---|---|---|---|
| `check_asset_reuse.py <film.json>` | factory≤1 / motion≤2 / still≤2 / first-use≥0.70 | **film.json 位置引数** | §5.2: factory1.00 / motion2.00 / still1.19 / first-use **0.8571** |
| `check_motion_density.py --ep PD-2026-045-cleveland` | film.json の graphics+figures+heroCuts のみ / density≥2.5・coverage≥0.25・variety≥3（**AND**） | **`--ep`** | §6.1: **3.03 / 30.3% / 13種**（AEカードは0本＝§0.5-2・beats≥30） |
| `check_animation_mix.py --ep PD-2026-045-cleveland` | film.json の cuts を img=still/その他=footage 分類 / still-share≤0.45・motion-cov≥0.45 | **`--ep`** | §5.2[C]: still-share **0.4464(cut)/0.4202(frame)** / motion-cov **0.5536+** |
| `check_caption_breaks.py <srt>` | A/B/C 各0件 | **srt 位置引数** | §8 の構文境界生成器 |
| `check_script_length.py <script> --json` | 総語数 / wpm / narration_seconds | **script 位置引数** | 2,119語 / wpm178.1 / **713.9s** |

> **★ゲートの入力指定（ブリーフ§5）:** density/mix は **`--ep PD-2026-045-cleveland`**。**`--json <film.json>` は出力パス
> （上書き事故）なので入力に使わない。** asset_reuse は film.json 位置引数、caption_breaks は srt 位置引数、script_length は script 位置引数。
>
> **`check_animation_mix` は `04_scenes/premium_beatsheet.v*.json` があればそれを優先する。**
> §5.6 の通り B の beatsheet は `cleveland_beatsheet`（`premium_` 無し）なので**auto-detect されず film.json を測る。**

---

# 10. OP バンパー `OpeningCleveland`（Remotion・fps60/1920x1080/180f）

## 10.1 二重OPを作らない
本編（`Ep45Cleveland`）の OP は `Bookends.tsx` の `BrandOpening` のまま（`op_ed_bookends` ゲート・フォーク禁止）。
`OpeningCleveland` は**独立したタイトルバンパー成果物**（`out/cleveland_opening.mp4`。Shorts/予告/SNS 用）。**本編に ffmpeg で焼き込まない。**

## 10.2 Composition 設定
| 項目 | 値 |
|---|---|
| `id` | `OpeningCleveland` |
| 解像度 / fps / duration | **1920×1080 / 60 / 180**（=3.0秒） |
| component | `remotion/src/compositions/OpeningCleveland.tsx` |

```tsx
import {OpeningCleveland, openingClevelandDurationInFrames} from './compositions/OpeningCleveland';
import clevelandOpeningProps from '../props/cleveland.json';
<Composition id="OpeningCleveland" component={OpeningCleveland}
  width={1920} height={1080} fps={60}
  durationInFrames={openingClevelandDurationInFrames(60)} defaultProps={clevelandOpeningProps}/>
```

**依存:** `@remotion/motion-blur`（未導入時のみ `cd remotion && npm i @remotion/motion-blur`）。
**`remotion/remotion.config.ts`** は既に正典値（png / h264 libx264 / CRF16 / yuv420p / bt709 / aac 320k / 全コア並列 / angle）。**一致確認のみ・書き換えない。**

## 10.3 秒数ベースのタイムライン（fps=60・フレーム直書き禁止・全て `Math.round(fps*秒)`）

| 秒 | 起きること | 手法 |
|---|---|---|
| 0.00–0.40 | L1 グラデ背景 opacity 0→1・**同時に scale 1.08→1.00（`Easing.out(Easing.cubic)`）** | interpolate（opacity 単独禁止・scale と併用） |
| 0.10 | ロゴ（`hasLogo`）左上に spring・scale 0.4→1.0・opacity 0→1 | spring `damping:14,mass:0.9` |
| 0.15–0.25 | L2 グリッド reveal（opacity→0.18）＋ translateY 0→48px | spring `damping:200,mass:1` + `Easing.inOut(Easing.sin)` |
| 0.25 | L3 グロー（crimson `#B23A48`）scale 0.6→1.15 / opacity 0→0.85 | spring `damping:18,mass:1.2`（併用） |
| 0.30–0.86 | L4 主役タイトルが1文字ずつ切れ上がり（overflow:hidden + translateY 110%→0）＋ opacity。スタッガー **2f/文字**。全体を `Trail(layers=6,lagInFrames=1.2,trailOpacity=0.45)` で包む | spring `damping:16,mass:1` |
| 0.55–1.15 | L2b **督促帯（past-due の朱線）**が中央から縦に `scaleX 0→1`＋opacity 0→0.5（crimson・「督促→留置」のモチーフ） | spring `damping:22,mass:1.1`・`transformOrigin:'center'`・**motionBlur** |
| 0.95–1.35 | L5a アクセント下線（crimson）左から `scaleX 0→1` | spring `damping:16,mass:0.8`・`transformOrigin:'left center'` |
| 1.10–1.55 | L5b サブタイトル translateY 24→0 + opacity 0→1 | spring `damping:20,mass:1`（併用） |
| 1.55–3.00 | settle→ホールド。**完全静止フレーム無し・フェードアウトしない** | — |

> **等速線形を1箇所も使わない。opacity 単独の演出を1箇所も作らない**（全 opacity が translateY/scale/scaleX と対）。

## 10.4 props 型と値
```ts
export type OpeningClevelandProps = { title:string; subtitle:string; accent:string; hasLogo:boolean };
```
`remotion/props/cleveland.json`: `{ "title":"THE PRICE OF BEING POOR", "subtitle":"UNCONSTITUTIONAL SINCE 1983", "accent":"#B23A48", "hasLogo":true }`
`remotion/props/cleveland_short.json`: `{ "title":"THE PRICE OF BEING POOR", "subtitle":"CAN THEY JAIL YOU FOR BEING POOR?", "accent":"#B23A48", "hasLogo":false }`
> `subtitle`/`title` も §2 の R-FORBID/R-LEGAL/R-SCOTUS/R-FACE 検査対象（`remotion/props/cleveland*.json`）。ルート背景は INK 近黒 `#0A0A0C`。
> **accent は EP41 gold / EP42 blue / EP43 amber / EP44 teal を書かず crimson `#B23A48`（レーン分離・他話色流用は BLOCKER）。**
> **「it is legal」無留保・「Supreme Court saved Cleveland」を subtitle に書かない。** `UNCONSTITUTIONAL SINCE 1983`（実際に違憲・C-1）・疑問形 `CAN THEY JAIL YOU FOR BEING POOR?` は制度説明として可。

## 10.5 量産
```bash
cd remotion && npm run studio     # OpeningCleveland を 0→180f スクラブして §10.3 の各時刻を目視
npx remotion render OpeningCleveland out/cleveland_opening.mp4 --props=./props/cleveland.json
npx remotion render OpeningCleveland out/cleveland_short_op.mp4 --props=./props/cleveland_short.json
```

---

# 11. サムネ3案（`ClevelandThumbnails.tsx`・`<Still>` 1280×720・Root に `Thumb-cleveland-01..03`）

**共通要件:** 見出し全て大文字・4語以内・320pxで判読 / **実在人物の肖像禁止（R1・Harriet Cleveland の顔/身体を出さない・C-4）** / INK 黒 `#0A0A0C` bg + crimson `#B23A48` /
背景は body 静止画のうち `also_thumb==true` の6枚（象徴オブジェのみ・C-4。**サムネ専用の分類は無い＝also_thumb フラグを読む**） / `thumbnail_visibility`（luma平均≥33＋コントラスト）を通す。目標CTR 6%+。3案は6枚から選ぶ。
**「it is legal」「Supreme Court saved Cleveland」「all fines unconstitutional」を出さない（R-FORBID/R-LEGAL/R-SCOTUS/R-HOLDING）。**

**★also_thumb 6枚（still 資産 ID 空間 S01..S84＝CODEX_A §5.9。A のマニフェストと**一字一致必須**の A↔B 契約点。CODEX_A §4.2 不変条件14 / §4.3 と同一6 asset ID に `also_thumb:true`）:**
`S01` / `S03` / `S18` / `S46` / `S68` / `S84`。
> サムネ component は**マニフェストの `also_thumb` フラグを読んで**背景を選ぶ（scene id をハードコードしない）。**この6 ID は CODEX_A §4.3 と完全一致**（`check_cleveland_asset_manifest` §3.3-12 が集合 `{S01,S03,S18,S46,S68,S84}` の一致を検査）。

- **T1「督促の束」（最推奨）:** 輪ゴムで束ねた督促状の山（象徴・顔なし・**S01/S03** 系）。文字 **`JAILED FOR BEING POOR`**（4語）。`POOR` を crimson。**enforcement failure（C-1）＝射程を過大化しない。**
- **T2「$1,554 or 31日」（数字勝負）:** 裁判所命令の書面を暗く落とし（**S18** 系）、前面に **`$1,554`**（大）＋ **`OR 31 DAYS`**（下・**FFJC 帰属を近傍に・C-6**）。数字は F09 の検証済み値のみ。
- **T3「1983 の線」（尊厳）:** 大理石の列柱／採光を背にした象徴（**S46/S84** 系）。文字 **`UNCONSTITUTIONAL SINCE 1983`**（enforcement failure・C-1）。`1983` を crimson。**「もう無くなった」に見せない。**

**A/Bタイトル候補（`09_package`・60字以内・二人称・台本のとおり・★"合法"と書かない）:**
- **A:** `Jailed for Being Too Poor to Pay a Fine. It's Unconstitutional.`
- **B:** `The Supreme Court Banned Debtors' Prisons in 1983. This City Kept One.`
> ※「最高裁が Cleveland を救った」系・「全罰金違憲」系のタイトルは**禁止**（C-2/C-3・R-SCOTUS/R-HOLDING）。

**固定コメント** `09_package/pinned_comment.v001.txt`（§2 の R-NUM/R-ATTRIB/R-FORBID/R-LEGAL/R-SCOTUS/R-HOLDING/R-ATTACK 検査対象。台帳事実のみ・**988 でなく legal-aid / ability-to-pay の行を含む＝F19/R-LEGAL 隣接**）:
```
Two things this case actually settled — and two it did not.

SETTLED IN 1983: Under Bearden v. Georgia (461 U.S. 660), a court cannot jail
someone simply for being unable to pay a fine without first asking whether they
could pay and whether an alternative to jail would work. That rule has stood since
1983 — yet the practice kept happening. That is an enforcement failure, not a
loophole, and not something that is legal.

WHAT IT DID NOT DO: Bearden did not abolish fines, fees, or restitution — those
still stand. And Harriet Cleveland's case never reached the Supreme Court. Her
relief came from an ordinary lawsuit and a settlement announced in late 2014 —
a lower court, not the Supreme Court.

If you are being told to pay court fines or fees you cannot afford, you have a
right to an ability-to-pay determination. Contact your local legal aid office.
```
> **description.txt にも `legal aid` かつ `ability to pay` の1行を置く（R-LEGAL 隣接検査・988 でない）。AI 開示行（`AI-assisted visualization`）を description に置く（R1）。**

---

# 12. 本編コンポジション登録（`remotion/src/Root.tsx`・`Ep43Caniglia`/`Ep42Young` の形を踏襲）
```tsx
import clevelandFilm from './data/cleveland_film.json';
<Composition id="Ep45Cleveland" component={CaseFilm}
  durationInFrames={caseFilmDurationInFrames(clevelandFilm as unknown as FilmData, BRAND.video.fps)}
  fps={BRAND.video.fps} width={BRAND.video.width} height={BRAND.video.height}
  defaultProps={{ data: clevelandFilm as unknown as FilmData, seriesLabel: 'PRIME DOCUMENTARY',
    title: "Jailed for Being Too Poor to Pay a Fine. It's Unconstitutional.",
    subtitle: 'Unconstitutional since 1983 — yet it kept happening. A lower court, not the Supreme Court, ended this one.' }}/>
```
> **id は正確に `Ep45Cleveland`（切り詰め・綴り違い・大文字化の誤記に注意）。** `caseFilmDurationInFrames` の 4項評価は **21792 frames**（§5.1.1）。
> `remotion/src` に現在 `cleveland` の文字列が無いこと（衝突しない）を確認してから追記。
> `title`/`subtitle` も §2 検査対象（R-FORBID/R-LEGAL/R-SCOTUS/R-HOLDING）。**「it is legal」「Supreme Court saved Cleveland」「all fines unconstitutional」を書かない。**

---

# 13. 受入（自分で exit 0 を確認してから完了報告）
```bash
cd C:\Users\aab15\Documents\prime-documentary ; PY=./.venv/Scripts/python.exe

# 0. 語数（最優先・課金前に落とす）
$PY scripts/check_script_length.py episodes/PD-2026-045-cleveland/03_script/script.en.v001.md --json   # 2,119語 / wpm178.1 / 713.9s

# 1. 事実性/6制約（EP45固有・正確性ゲートはこの1本・dochighlight 不使用も検査）
$PY scripts/check_cleveland_facts.py --json

# 2. 契約バリデータ
$PY scripts/validate_cleveland_beats.py
$PY scripts/check_cleveland_asset_manifest.py --assets episodes/PD-2026-045-cleveland/05_visuals/asset_manifest.v001.json

# 3. ★5ゲート（animation_mix を忘れるな・入力は --ep / 位置引数を厳守）
$PY scripts/check_asset_reuse.py    remotion/src/data/cleveland_film.json
$PY scripts/check_motion_density.py --ep PD-2026-045-cleveland
$PY scripts/check_animation_mix.py  --ep PD-2026-045-cleveland
$PY scripts/check_caption_breaks.py episodes/PD-2026-045-cleveland/08_edit/captions.final.v001.srt

# 4. 水増し・レンダ前プリフライト
$PY scripts/check_padding.py --ep PD-2026-045-cleveland --json
$PY scripts/preflight_render_gate.py --ep PD-2026-045-cleveland

# 5. 本編レンダ（slim public・並列4）→ BGM → AEカード合成
cd remotion
npx remotion render Ep45Cleveland out/cleveland.mp4 --public-dir=public_slim --concurrency=4
#   public_slim は cleveland_film.json が参照する素材（+ 各 <stem>_depth.png）だけを含む slim public。
#   無ければ referenced paths を public_slim/ にコピーして作る（remotion/public/cleveland 本体を痩せさせない）。
cd ..
$PY scripts/build_cleveland_bgm.py
$PY scripts/ae/composite_cleveland_hero.py

# 6. 本編最終受入（episode番号は★位置引数・--ep ではない）
$PY scripts/check_final_acceptance.py 45 \
  --render episodes/PD-2026-045-cleveland/08_edit/cleveland_final_bgm.v003_ae.mp4 --emit-receipt
```

| ゲート | EP45 目標値 |
|---|---|
| `check_script_length` | 総語数 **2,119** / `wpm 178.1` / narration **713.9s** |
| `check_asset_reuse` | factory≤1 / motion≤2 / still≤2 / first-use **0.8571**（floor0.70） |
| `check_motion_density` | density **3.03**/min / coverage **30.3%** / variety 13（floors 2.5 / 0.25 / 3・beats **≥30**） |
| `check_animation_mix` | still-share **0.4464(cut)/0.4202(frame)**（cap0.45）/ motion-cov **0.5536+**（floor0.45） |
| `check_caption_breaks` | 行末機能語0 / 孤立キュー0 / hard split 0 |
| `check_cleveland_facts` | violations = 0（台帳照合・enforcement failure 枠・下級審/最高裁分離・holding 限定・R-FORBID・R-DOCHL・帰属） |
| runtime band | 11.5–12.5分（narration 713.9s + bookends・total **726.4s ≤ 750s**） |
| factory クリップ | ≥24本 → **92本** |
| image_resolution | 全静止画 長辺 ≥3840px |
| thumbnail | 3案 @1280×720 + selected luma≥33 |
| op_ed_bookends | `BrandOpening`/`BrandEndcard` を import（フォーク禁止） |

**全て exit 0 でなければ `package_ready` にしない。自己申告QCは無効。QC基準を書き換えて通すのは禁止。**

## 13.1 完成後の全編アイボール（**1フレーム判定禁止＝EP39-41 実害**）
`cleveland_final_bgm.v003_ae.mp4` を **0→末尾まで通しで実視聴**し、以下を確認してから完了報告:
- 紙芝居感が無い（still が連続していない・footage が体感で過半）
- AEカード8枚が全て焼き込まれ数値が台帳と一致（「it is legal」「Supreme Court saved Cleveland」「all fines unconstitutional」がどこにも無い）
- **r01 に "UNCONSTITUTIONAL SINCE 1983 / YET IT CONTINUED"（enforcement failure・C-1）＋ "A LOWER COURT, NOT THE SUPREME COURT"（C-2）が読める**
- **m01「$1,554 / OR 31 DAYS」・j01「$200 / MONTH — $40 TO THE COMPANY」に "PER FINES & FEES JUSTICE CENTER" が読める（C-6 medium ヘッジ）。s01「~38,000 PEOPLE / ACROSS FOUR STATES」の限定が読める（C-6・過大化しない）**
- **Bearden 関連 figure/カードが holding を限定（能力なしだけの審問なし収監のみ／罰金・手数料・賠償は STILL ALLOWED）＝全罰金違憲に見えない（C-3）**
- O'Connor 逐語が O'Connor 帰属、Harrington 逐語が Judge Harrington 帰属、和解条項が 2014 settlement 帰属（要約を引用符にしていない・R-ATTRIB）
- Harriet Cleveland の顔・身体・肖像が無い（象徴＝督促の束/免許/空の財布/廊下/留置扉/booking 時計/支払台帳/バス停/空席の弁護人席のみ・C-4）／扇情でない（poverty porn なし）
- **`dochighlight`（黒バー/box/underline）が1本も無い（figures/AE／R-DOCHL）**
- 生成ビジュアル表示中は `AI-assisted visualization` が右下に常時（**AEカード8枚の表示中も**開示が見える＝カード共通スタックに焼かれている・R1・§7.3/§7.9）
- **概要欄/固定コメントに 988 でなく local legal-aid / ability-to-pay の行がある（F19・R-LEGAL 隣接）**
- accent が crimson `#B23A48`（EP41 gold / EP42 blue / EP43 amber / EP44 teal が紛れていない）
- 音ズレ・字幕ズレ・尺差（base と <=0.5s）が無い

---

# 14. 絶対にやらないこと
- **EP39 / EP40 / EP41 / EP42 / EP43 / EP44 のファイル・素材に触らない**（読み取りのみ可）。レーンを分離する。
- **スレッドAの所有ファイル（§0.2.1）に書かない**（`05_visuals/` `05_stock/` `remotion/public/cleveland/` `H:\...\ai\cleveland\`）。**B の provenance は `04_scenes/cleveland_build_manifest.v001.json` に書く。**
- **設計書 / `EP45_cleveland_CODEX_A_*` / PD-2026-039〜044 に触らない。**
- **課金ジョブを起動しない**（ElevenLabs TTS / 課金画像生成API / YouTube アップロード）。narration_index は実測版を消費するだけ。
- **公開済み・出荷済み mp4 を上書き・再レンダしない**（出力は必ず `_v003_ae`）。
- **台帳（§2）に無い数値を焼かない**（$580,000 の再発防止）。不明値は `verified:false` でカード除外。
- **`FigureSpec` の `kind` を推測で書かない**（§6.2 の実在小文字値のみ。大文字名は無言で消える。`comparebars` は非在→`compbars`）。**★`dochighlight` を1本も使わない（R-DOCHL）。**
- **`--variants` という語を書かない**（1シーン1枚・バリエーション0＝ブリーフ§1。SDXL は A の領分で 1 固定）。
- **asset_manifest の `counts`/`role` enum/`overlay` 枚数を CODEX_A と食い違わせない**（`role` は `body`/`i2v_source`/`reject` の3値のみ・**`thumb`/`still_thumb` を作らない**・overlay=12・**also_thumb 集合 `{S01,S03,S18,S46,S68,S84}`**）。
- **「it is legal」化しない・「もう無くなった」と言わない**（C-1・R-LEGAL）。**「最高裁が Cleveland を救った」と書かない**（C-2・R-SCOTUS）。**「全罰金違憲」に過大化しない**（C-3・R-HOLDING）。**Harriet Cleveland の顔/肖像/身体を出さない・扇情化しない**（C-4・R-FACE）。**JCS/制度を説明し個人攻撃しない**（C-5・R-ATTACK）。**数値は台帳一致**（C-6・R-NUM）。**988 でなく legal-aid**（F19）。
- **accent に他話色（EP41 gold / EP42 blue / EP43 amber / EP44 teal）を使わない**（crimson `#B23A48` のみ）。
- **stub/dryrun のコードパスを作らない**（このスレッドは実素材のみ・ブリーフ§7）。
- **スペック数値（224 cuts / still84 / factory92 / motion16 / distinct192 / first-use0.8571 / still-share0.4464 / figures≥30→36 / 713.9s / 2,119語 / 48シーン / mean_shot3.19 / total726.4s≤750s / durationInFrames21792）を変えない。**
- **実在しないスクリプト名を書かない**（新規は §0.3 の一覧のみ・複製元を明記・**`build_tekoh_film.py` は非実在**）。**composition id は `Ep45Cleveland`（切り詰め・綴り違い注意）。** **PowerShell 経由で正規表現/エスケープを生成しない**（`\b` バックスペース化の実害）。
