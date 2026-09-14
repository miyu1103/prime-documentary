# EP44 tekoh — Codex スレッドB「実装」引き継ぎプロンプト v001

> **このファイルは単体で完結している。他のファイルを読まなくても着手できる。**
> 並行して走っていたスレッドA（素材生成）は**凍結（FROZEN）済み**。その成果物 `05_visuals/asset_manifest.v001.json` は**実在する**。
> あなたはその **asset_manifest の唯一の消費者／検証者**である。CODEX_A の中間生成物は読まない（`asset_manifest.v001.json` だけを読む）。
> 設計ブリーフ `EP44_tekoh_DESIGN_BRIEF.shared.md` の数値は本書に転記済み。`EP44_tekoh_PRODUCTION_SPEC.v001.json` の数値も転記済み。**あなたはこれらを書き換えない。**

```
あなたは Prime Documentary（YouTubeドキュメンタリーチャンネル）の制作エンジニアです。
リポジトリ: C:\Users\aab15\Documents\prime-documentary
Python:     C:\Users\aab15\Documents\prime-documentary\.venv\Scripts\python.exe
メディア:   H:\pd-media
担当:       EP44 / Episode ID: PD-2026-044-tekoh / slug: tekoh
Composition id: Ep44Tekoh
```

**題材:** *Vega v. Tekoh*, 597 U.S. 134 (2022), No. 21-499（decided June 23, 2022）。
合衆国最高裁が **6対3**（Alito 法廷意見／Kagan 反対＋Breyer・Sotomayor）で、
「ミランダ警告を怠ったこと“単体”を理由に、その警官を **§1983 の民事**で訴えて金銭賠償を取る道」だけを否定した実在の最高裁判決（**制度説明としてのみ**扱う）。
主題人物は **Terence Tekoh**（LA の医療機関の被用者・**存命の私人 = R2**）。2014年、保安官助手 **Carlos Vega**（存命私人・R2）が
苦情について本人を聴取し、**警告なしに**本人自筆の供述書が作られた。刑事公判で本人は**無罪（陪審が有罪にせず）**。その後、§1983 で二度の民事敗訴、第9巡回区が破棄・差戻し、最高裁が介入した。

> **★決定的な射程（全出力を律する）:** 閉じたのは「§1983 の**賠償**の第2の扉」だけ。**ミランダ自体は存続**し、**未告知供述は刑事公判で排除されうる（排除の扉は開いたまま）。**
> `Supreme Court` / `Fifth Amendment` / `Section 1983` は禁止語ではない（実在の本案判決）。だが **§2 の正確性6制約が全出力を律する。**
> **「Miranda is dead / 黙秘権消滅 / 警察は権利を読まなくてよい」断定・「9-0／全会一致」・「Vega が Miranda を覆した」・§1983一般で「no immunity」断定・Tekoh/Vega の顔/肖像/身体・そして★原被疑事実（疑われた罪の性質）を一切出さない**（プロンプト・カード・図表・タイトル・字幕・props・概要欄すべて）。
> **★このエピソードに `dochighlight` figure は一切使わない（EP40/41/42 で3回バグ指摘・grep で 0 を確認）。**

---

# 0. このスレッドの責務・境界・完了条件

## 0.1 このスレッド（B）の責務 — **コード律速。実素材（A の凍結マニフェスト）を消費して全部書く。**

| # | 作業 | 成果物 |
|---|---|---|
| B-1 | エピソードディレクトリと `manifest.json` | `episodes/PD-2026-044-tekoh/**` |
| B-2 | 境界契約マニフェストの**消費側**バリデータ（★A の §4.2 不変条件と一字一致） | `scripts/check_tekoh_asset_manifest.py` |
| B-3 | 事実台帳 F-ID と 6制約ゲート（**EP44固有・BLOCKING・正確性ゲートはこの1本**） | `scripts/check_tekoh_facts.py` |
| B-4 | `tekoh_film.json` ビルダ（**asset_map→manifest変換＋beatsheet生成／footage混在／実素材のみ**） | `scripts/build_tekoh_film.py`（**`build_caniglia_film.py` を複製**） |
| B-5 | beats バリデータ（AEとRemotionの区間衝突検査＋ledger／6制約） | `scripts/validate_tekoh_beats.py`（**`validate_caniglia_beats.py` を複製**） |
| B-6 | **構文境界で切る字幕生成器** | `scripts/gen_captions_tekoh.py`（**`gen_captions_caniglia.py` を複製**） |
| B-7 | **After Effects カード**のビルダとコンポジタ | `scripts/ae/build_tekoh_hero_cards.py`（**`build_young_hero_cards.py`/`build_thompson_hero_cards.py` を複製**） / `scripts/ae/composite_tekoh_hero.py`（**`composite_young_hero.py` を複製**） |
| B-8 | 本編 BGM ミックス（AEカード合成の基底 mp4 を生成・**実装版**） | `scripts/build_tekoh_bgm.py`（**`build_young_bgm_real.py`＝REAL builder を複製・stub 版ではない**） |
| B-9 | Remotion 本編コンポジション登録 `Ep44Tekoh` | `remotion/src/Root.tsx` |
| B-10 | OP バンパー `OpeningTekoh`（fps60/1920x1080/180f） | `remotion/src/compositions/OpeningTekoh.tsx` |
| B-11 | サムネ3案 | `remotion/src/compositions/TekohThumbnails.tsx` |

> **★★ 最重要の設計転換（EP44 の明示要件）: REAL アセットのみ・stub/dryrun パスを作らない ★★**
> EP43 では A を待たずに走るためのスタブ機構（`make_*_stub_assets` / `make_*_stub_narration` / `_dryrun/`）を持っていた。
> **EP44 では A が凍結済み＝実マニフェストが存在するので、スタブ機構を一切作らない。**
> `build_tekoh_film.py --assets` が読むのは **`05_visuals/asset_manifest.v001.json`（実素材・`is_stub==false`）ただ一つ。**
> `check_tekoh_facts.py` にも `--dryrun` の別コードパスを設けない（`_dryrun/` を対象に含めない）。**実素材で緑になって初めて完了。**

## 0.2 もう一方のスレッド（A・凍結）との境界 — **接続点はただ1ファイル。**

```
episodes/PD-2026-044-tekoh/05_visuals/asset_manifest.v001.json
   ↑ Aが生成（唯一の生産者・凍結済み）        ↓ Bが消費／検証（唯一の消費者・検証者）
```

**Bはこのファイル以外のAの中間生成物を読まない。** A は §4 の 16 不変条件を満たすマニフェストを既に凍結出力している。
**B は同じ 16 不変条件を `check_tekoh_asset_manifest.py` で再検証してから消費する**（A↔B で一字一致・§3.3）。

> **★1シーン1枚・バリエーション0（ブリーフ§1）の B 側での意味:** A は同一ショットの `_01/_02/_03` を**作っていない**。
> マニフェストの `stills[role=="body"]` は **85本すべてが固有プロンプトの distinct**（`counts.still_body==85`）。
> B は編集上、still を **各最大2回**まで再使用してカット101本を組む（cap 2 の"再利用"であって"バリエーション"ではない）。
> **B は `--variants` という語をどのコマンド・ログにも書かない**（A の SDXL 側の概念で 1 固定）。

### 0.2.1 ファイル所有権（これを破ると並行作業が壊れる）

| パス | 所有 | Bの権限 |
|---|---|---|
| `episodes/PD-2026-044-tekoh/manifest.json` | **B** | 読み書き |
| `episodes/PD-2026-044-tekoh/{00_topic,01_research,03_script,04_scenes,06_audio,08_edit,09_package,approvals,events}/**` | **B** | 読み書き |
| `remotion/src/**` `remotion/props/**` | **B** | 読み書き |
| `scripts/*tekoh*.py` / `scripts/ae/*tekoh*.py`（§0.3） | **B** | 新規作成 |
| **`episodes/PD-2026-044-tekoh/05_visuals/**` `05_stock/**`** | **A** | **読み取りのみ。書くな** |
| **`H:\pd-media\assets\ai\tekoh\**` / `ai_video\tekoh\**`** | **A** | **読み取りのみ。書くな** |
| **`remotion/public/tekoh/{img,factory,motion,overlay}/**`** | **A** | **読み取りのみ。書くな**（B は `public_slim` を派生させる・§13） |
| `episodes/PD-2026-044-tekoh/04_scenes/ai_prompts.v001.md` | **A** | **読み取りのみ。書くな** |
| `EP44_tekoh_DESIGN_BRIEF.shared.md` / `EP44_tekoh_CODEX_A_ASSETS.v001.md` | **設計/Aスレッド** | **触るな** |
| `EP44_tekoh_PRODUCTION_SPEC.v001.json` / `EP44_tekoh_script.en.v001.md` | **上流** | **読み取りのみ。書くな** |
| `episodes/PD-2026-039-*/**` … `PD-2026-043-*/**` / それらの素材 | **他エージェント** | **絶対に触るな** |

## 0.3 B が新規作成するスクリプト（これ以外を新規に作らない。既存を改変しない）

| パス | 役割 | 手本（**改変せず読んで複製→パス/定数/デッキだけ差し替え**） |
|---|---|---|
| `scripts/check_tekoh_asset_manifest.py` | §3.3 消費側バリデータ（A §4.2 と一字一致） | `scripts/check_caniglia_asset_manifest.py` |
| `scripts/check_tekoh_facts.py` | §2 6制約＋台帳（BLOCKING・**正確性ゲート名はこの1つに統一・DESIGN/A/B 同名**） | `scripts/check_caniglia_facts.py` |
| `scripts/build_tekoh_film.py` | §5 film.json＋manifest＋beatsheet＋SRT（**実素材のみ**） | **`scripts/build_caniglia_film.py`** |
| `scripts/validate_tekoh_beats.py` | §7.9 不変条件 | `scripts/validate_caniglia_beats.py` |
| `scripts/gen_captions_tekoh.py` | §8 構文境界字幕生成器 | **`scripts/gen_captions_caniglia.py`** |
| `scripts/ae/build_tekoh_hero_cards.py` | §7 AEカードビルダ | **`scripts/ae/build_young_hero_cards.py`**（＝`build_thompson_hero_cards.py` 系） |
| `scripts/ae/composite_tekoh_hero.py` | §7.10 コンポジタ（`beats.json` の `film_offset_sec` を読んで**加算**する） | **`scripts/ae/composite_young_hero.py`** |
| `scripts/build_tekoh_bgm.py` | §7.10 基底 mp4（narration＋BGM ミックス・**REAL 実装版**） | **`scripts/build_young_bgm_real.py`**（★stub 版 `build_young_bgm.py` ではない） |

> **`build_tekoh_film.py` の複製時に差し替える定数:** `ASSET_MAP`（マニフェスト→cut 変換テーブル）・`NARR`（narration_index 既定パス）・
> `FACTORY_SEL`（factory 参照）・`SLUG="tekoh"`・`EP="PD-2026-044-tekoh"`・出力パス群。**ロジック（best-pick / tile_window /
> allocate / build_figures / build_captions）は1行も変えない。** ただし §6 の `figures[]` に **`dochighlight` を一切生成しない**（`build_figures()` の payload 定義から dochighlight を外す）。
> **`build_tekoh_bgm.py` の section マップは young の `ACT_1..ACT_4`（4幕）を tekoh の `ACT_1..ACT_3`（3幕）に縮める**（§4.2）。ミックス経路・ゲイン・ダッキングは変えない。
> **既存の `scripts/*caniglia*.py` / `*young*.py` / `*thompson*.py` は触らない**（他エピソードが使用中）。EP44用に**新規コピー**する。

## 0.4 完了条件（**実素材で**全て緑になったら「実装完了」）

```bash
cd C:\Users\aab15\Documents\prime-documentary
PY=./.venv/Scripts/python.exe

# [B-DONE-1] A の凍結マニフェストを 16 不変条件で再検証（消費前の必須ゲート）
$PY scripts/check_tekoh_asset_manifest.py \
  --assets episodes/PD-2026-044-tekoh/05_visuals/asset_manifest.v001.json

# [B-DONE-2] 実測 narration_index から字幕を構文境界で生成
$PY scripts/gen_captions_tekoh.py \
  --narr episodes/PD-2026-044-tekoh/06_audio/narration_index.v001.json
$PY scripts/check_caption_breaks.py \
  episodes/PD-2026-044-tekoh/08_edit/captions.final.v001.srt

# [B-DONE-3] film.json を実マニフェストから組み立てる（footage 混在必須・stub 分岐なし）
$PY scripts/build_tekoh_film.py \
  --assets episodes/PD-2026-044-tekoh/05_visuals/asset_manifest.v001.json \
  --narr   episodes/PD-2026-044-tekoh/06_audio/narration_index.v001.json \
  --out    remotion/src/data/tekoh_film.json

# [B-DONE-4] ★5ゲート全部（--ep 指定・animation_mix を絶対に忘れるな）
$PY scripts/check_asset_reuse.py     remotion/src/data/tekoh_film.json
$PY scripts/check_motion_density.py  --ep PD-2026-044-tekoh
$PY scripts/check_animation_mix.py   --ep PD-2026-044-tekoh
$PY scripts/check_caption_breaks.py  episodes/PD-2026-044-tekoh/08_edit/captions.final.v001.srt
$PY scripts/check_script_length.py   episodes/_planning/EP44_tekoh_script.en.v001.md --json

# [B-DONE-5] 事実性/6制約（EP44固有・正確性ゲートはこの1本・dochighlight=0 も検査）
$PY scripts/check_tekoh_facts.py --json

# [B-DONE-6] beats 契約（AE区間 と Remotion figures[] が1秒も重ならない）
$PY scripts/validate_tekoh_beats.py

# [B-DONE-7] dochighlight が film.json / beats.json のどこにも無い（grep で 0）
grep -rin '"kind"[[:space:]]*:[[:space:]]*"dochighlight"' remotion/src/data/tekoh_film.json \
  episodes/PD-2026-044-tekoh/08_edit/ae_hero/beats.json   # → ヒット0

# [B-DONE-8] AE カードをビルド＋レンダ＋コンポジット（本番出力へ・dryrun なし）
$PY scripts/ae/build_tekoh_hero_cards.py
"C:/Program Files/Adobe/Adobe After Effects 2026/Support Files/AfterFX.exe" -noui \
  -r "C:/Users/aab15/Documents/prime-documentary/episodes/PD-2026-044-tekoh/08_edit/ae_hero/tekoh_hero.jsx"
$PY scripts/ae/composite_tekoh_hero.py

# [B-DONE-9] Remotion Studio で目視
cd remotion && npm run studio
#   → Ep44Tekoh / OpeningTekoh / Thumb-tekoh-01..03 が出て、実際に動くこと
```

**台本は既に確定済み**（`EP44_tekoh_script.en.v001.md`・2,139語・12.0分・ロック）。**「一部だけ通ったから残りも通るはず」は禁止。** 全ゲート exit 0 を自分で確認する。

---

# 1. 実装前に必ず読むファイル（**推測で書くな**）

| パス | なぜ読むか |
|---|---|
| `scripts/build_caniglia_film.py` | **複製元。** best-pick / tile_window / allocate / build_figures / build_captions をそのまま踏襲し、定数だけ tekoh に。**footage を必ず混ぜる（§0.5 の紙芝居回避）・figures に dochighlight を作らない** |
| `scripts/ae/build_young_hero_cards.py`（`build_thompson_hero_cards.py`） | **複製元。** `money_keys()`（Python で表示文字列を全事前計算）/ `fit_size()` / CARDS デッキ構造 / レイアウト定義 / 完了マーカーをそのまま |
| `scripts/ae/composite_young_hero.py` | **複製元。** SKIP4条件と ffmpeg フィルタグラフ／**`beats.json` の `film_offset_sec` を読んで加算する経路**をそのまま |
| `scripts/gen_captions_caniglia.py` | **複製元。** `internal_split()` / `chunk_sentence()` / `NO_DANGLE_END` import をそのまま |
| `scripts/build_young_bgm_real.py` | **複製元。** narration＋BGM ミックスで基底 mp4 を作る**実装版**の経路（stub 版と取り違えない） |
| `scripts/check_caniglia_facts.py` | §2 の複製元（ルール骨格）。EP44 は禁止語・台帳・6制約を tekoh に差し替える |
| `remotion/src/compositions/CaseFilm.tsx` | `FilmData` 型 / `caseFilmDurationInFrames` / `depthSrcOf()` |
| `remotion/src/components/FigureBeats.tsx` | `FigureSpec` の**実在する `kind` 文字列**（§6.2・**全小文字**・`comparebars` は非在→`compbars`・**dochighlight は使わない**） |
| `remotion/src/components/Bookends.tsx` | `OPENING_SEC` / `ENDCARD_SEC` / `BrandOpening` / `BrandEndcard` |
| `scripts/check_asset_reuse.py` / `scripts/check_motion_density.py` / `scripts/check_animation_mix.py` / `scripts/check_caption_breaks.py` / `scripts/check_script_length.py` | 通すべき5ゲートの**実際の判定ロジック**（§9） |
| `C:\Users\aab15\Documents\pino-channel\remotion\src\Opening.tsx` | §10 の OP 正典実装 |

---

# 0.5 ★★★ EP39/40/41/42/43 で踏んだ失敗＝最初から防ぐ（本書の全体設計はこの6点を構造で潰している）★★★

1. **紙芝居（最重要）** — 静止画100%で組むと `check_animation_mix` が FAIL する。**EP44 は最初から footage を混ぜる。**
   `check_animation_mix.compute_metrics_from_film()` は film.json の `cuts[]` を
   **`kind=="img"` → still（scene 扱い）/ それ以外 → footage（motion 扱い）** と分類する。
   → §5 の cuts 構成は **factory 93 + motion 32 の footage を最初から入れて still-share を cut数ベース 0.4469（cap0.45）・frame ベース ≤0.42** にする。
2. **AEカードは密度に数えられない** — `check_motion_density` は film.json の `graphics+figures+heroCuts` **のみ**数える。
   AEカードは ffmpeg で後合成するので**1本も数えられない**。→ §6 で **film.json 側の `figures[]` を 37本**（spec floor **31** に **+6**・`graphics[]=[]`）置く。AEカードは別勘定。
3. **FigureSpec の `kind` は実在の小文字値のみ** — 大文字名（`ActTitle`/`QuoteCard`/`VoteTally` 等）は無言で描画が消える（§6.2）。**`comparebars` は非在→`compbars`。`dochighlight` は本作で使わない。**
4. **台帳に無い数値を焼くな** — EP40 で架空の $580,000 が入って**不採用になった実害**。
   → §2 の事実台帳 F-ID に**検証済み値だけ**を置き、`check_tekoh_facts.py` が film.json/AE/サムネ/props の全数値を台帳照合する。台帳に無い数値・`verified:false` の数値を焼いたら FAIL。
5. **字幕は台本本文と対応** — EP38 で台詞混入・「final」誤称の実害。→ §8 の字幕は **narration_index の実チャンク文をそのまま** verbatim で使う（自作しない）。
6. **レンダー前ゲート** — build 後に `check_asset_reuse` / `check_motion_density` / `check_animation_mix` / `check_caption_breaks` / `check_script_length` を**全部**通す（§9・§13）。**animation_mix を忘れるな。**

---

# 2. ★ EP44固有の正確性6制約・事実性ロック（`scripts/check_tekoh_facts.py`・BLOCKING）

> **この節に違反した成果物は、他が全て完璧でも出荷不可。** 検査対象は film.json の figures/captions、AE beats、
> サムネ、props、固定コメント、（存在すれば）マニフェストの tags/caption_hint/qc.notes の**全文字列と全数値**。
> **正確性ゲートはこの1本に統一（`check_tekoh_facts.py`）。DESIGN/CODEX_A も同名を参照する。**

## 2.1 正確性6制約（全出力に適用・違反は BLOCKER）

| # | 制約 | 許可される表現 | 禁止 |
|---|---|---|---|
| C-1 | **射程を過大化しない** | 「否定されたのは *§1983 の賠償*“単体”の道だけ」「排除の扉は開いたまま（EXCLUSION STAYS OPEN）」「ONE DOOR CLOSED」「Miranda stands / Dickerson stands」 | 「Miranda is dead / 黙秘権消滅 / 警察は権利を読まなくてよい」の**断定**（カード/サムネ/字幕/props/タイトル） |
| C-2 | **6-3（中立帰属）** | 「6-3」を出すなら同一カード内に限定併記「ONE DOOR CLOSED」「EXCLUSION STAYS OPEN」。Alito 多数／Kagan 反対＋Breyer・Sotomayor | **「9-0」「9 to 0」「unanimous」を Vega の判決に付す** |
| C-3 | **Miranda(1966)/Dickerson(2000) 非混同・非覆滅** | 「MIRANDA STANDS / DICKERSON STANDS」「Vega はミランダを覆していない＝§1983救済のみ否定」 | `overturned Miranda`/`Miranda overruled/reversed/struck down/killed` |
| C-4 | **§1983 の意味を正確に** | 「州の役人を憲法違反で民事提訴する連邦法」「責任を問う扉」 | §1983一般論で **`no immunity` と断定**（qualified immunity がある） |
| C-5 | **★広告適合性（最重要級）** | 原告は「疑われ、無罪となった私人」。象徴：病院の廊下・ペンと署名欄・空の取調台・空の陪審席・列柱・守りの柵・閉じた扉/開いた扉 | **原被疑事実（疑われた罪の性質・被害・"victim"・"guilty"）を描写も表示もしない**（英語 AND 日本語）。★§2.3 CHARGE_BLOCK |
| C-6 | **Tekoh も Vega も R2・象徴のみ** | 事件主体としての名（"Terence Tekoh sued" / "Deputy Carlos Vega"）。顔なし・身体なし | 顔・肖像・身体・人物化・内面の憶測 |
| R1 | **実在人物の顔・肖像を生成しない** | 全生成ビジュアル表示中は `AI-assisted visualization`（右下）／概要欄1行AI開示 | 認識可能な人物・読める偽公文書 |

**★禁止語（`check_tekoh_facts.py` が対象文字列を case-insensitive 部分一致で検査。1件でも FAIL）:**
`miranda is dead` / `miranda (is )?(abolished|overturned|overruled|gone|struck down)` /
`(overturn|overturned|overrule|overruled|reverse|reversed|struck down|kill|killed|end|ended) miranda` /
`police (need not|no longer (need|have) to|do ?n.?t (need|have) to) (read|give|recite|warn)` /
`no (need|longer need) to read (you )?(your )?rights` /
`\b9-0\b` / `9 to 0` / `nine to (zero|nothing)` / `\bunanimous\b` /
`no immunity` / `full victory` / `total victory` / `won outright` / `case closed` / `case is over`。

> **★★重大な設計注意（EP43 と同型・EP44 は衝突がより近い）★★**
> 台本本文（＝字幕 verbatim）には**否定文脈の近似語**が含まれる:
> - `"This is not the death of the right to remain silent"`
> - `"it is not permission for police to stop reading anyone their rights"`
> **上の禁止語リストはこれらと衝突しない“断定形”だけを選んである。**
> 具体的に、**`stop reading ... rights` / `death of the right to remain silent` を禁止語リストに足すな**（字幕 verbatim を巻き込んで false FAIL する）。
> `police (need not|no longer ...|don't need/have to) (read|warn)` は台本の `"police to stop reading"` と語順が違うのでヒットしない。
> 射程・6-3・Miranda 存続の**否定/断定の別**は下の**文脈ルール**（R-SCOPE / R-VOTE63 / R-MIRANDA）で捕える。

## 2.2 事実台帳 F-ID（`03_script/tekoh_facts.v001.json`・**Bが台本の事実対応表(C01–C24)から転記して作る**）

**スキーマ版:** `tekoh_facts.v1`。各 F-ID は `{"value":..., "unit":..., "verified":bool, "claim_id":"", "quote":""}`。
**台本の事実対応表に裏付けのある値だけ `verified:true`。裏付け無しは `verified:false`（カードから除外）。**

| F-ID | 内容 | 使う場所 | claim |
|---|---|---|---|
| F01 | 判決日 = **June 23, 2022**（2022-06-23） | fig timeline / AE DATE_STAMP（**カードのみ・音声で docket を読まない**） | C01 |
| F02 | 判例引用 = **Vega v. Tekoh, 597 U.S. 134 (2022), No. 21-499** | fig lowerthird（**カードのみ**） | C01 |
| F03 | 判決 = **6 – 3**・処分 = **第9巡回区を破棄・差戻し（reversed & remanded）** | fig votetally / AE VOTE_SPLIT（**限定併記必須・C-2**） | C02/C10 |
| F04 | 法廷意見執筆 = **Justice Samuel Alito**（Roberts・Thomas・Gorsuch・Kavanaugh・Barrett） | fig stat（帰属） / AE q01 attribution 基準 | C03 |
| F05 | 反対 = **Justice Elena Kagan, joined by Breyer and Sotomayor**（＝3人） | fig stat（value 3・帰属） / AE q01 attribution | C04 |
| F06 | **Miranda v. Arizona, 384 U.S. 436 (1966)** | fig lowerthird / AE SPLIT_COMPARE m01（**存続・C-3**） | C22 |
| F07 | **Dickerson v. United States (2000)** | fig lowerthird / AE SPLIT_COMPARE m01（**存続・C-3**） | C23 |
| F08 | 連邦法 = **42 U.S.C. § 1983**（民事救済の扉・**"no immunity" と書かない**・C-4） | fig lowerthird / AE CENTER_STACK s01 | C08 |
| F09 | 事件 = **2014 · medical center, Los Angeles**（Tekoh = 病院被用者） | fig timeline / AE（象徴） | C11/C13 |
| F10 | 聴取officer = **LA County sheriff's deputy Carlos Vega** | fig lowerthird（事件主体・象徴） | C12 |
| F11 | 民事 = **二度の陪審審理・いずれも Vega 勝訴／第1審は説示の瑕疵で破棄** | fig stat（value 2） / AE CENTER_STACK t01「2 TRIALS」 | C16 |
| F12 | **無罪（陪審が有罪にせず）** | fig kinetic / AE CENTER_STACK a01「ACQUITTED」 | C14 |
| F13 | 第9巡回区 = **破棄・差戻し（未告知供述が §1983 を支えうると判断）** | fig timeline / lowerthird | C17 |
| F14 | prophylactic = **「a fence, not the ground」**（柵は権利そのものではない・警告は右を囲う守り） | fig mechanism / AE CENTER_STACK f01 | C06/C24 |
| F15 | 判旨 = **ミランダ違反“単体”は §1983 賠償の根拠にならない** | fig kinetic / AE（射程限定・C-1） | C05/C07 |
| F16 | **Kagan 反対の逐語**（"…strips … the ability to seek a remedy…" 系・★slip opinion の**正確な逐語**を転記して `verified:true`。逐語が確定できなければ `verified:false` で q01 を `required:false`） | AE QUOTE_CARD q01（**Kagan 帰属・R-ATTRIB**） | C20/C21 |

> **F03（6-3）は "ONE DOOR CLOSED" / "EXCLUSION STAYS OPEN" 等の限定ラベルと**同一カード/payload内**で提示する（C-2）。単独の勝利数として焼かない。** `check_tekoh_facts` の R-VOTE63 が照合。
> **F16 の逐語は Kagan 帰属。要約を引用符に入れない（R-ATTRIB）。逐語が primary source で確定できない場合は捏造せず `verified:false`＝q01 を `required:false` で除外**（$580,000 実害の再発防止）。

## 2.3 `check_tekoh_facts.py` の検査（exit 0=PASS / 1=FAIL / 2=スキーマ不一致）

**検査対象ファイル（この一覧をハードコード。存在するものだけ検査し、無いものは `skipped[]` に必ず明記）:**

```
episodes/PD-2026-044-tekoh/03_script/tekoh_facts.v*.json
episodes/PD-2026-044-tekoh/08_edit/ae_hero/beats.json
episodes/PD-2026-044-tekoh/09_package/*.json        （title / description / thumbnail headlines）
episodes/PD-2026-044-tekoh/09_package/*.txt         （固定コメント）
episodes/PD-2026-044-tekoh/05_visuals/asset_manifest*.json  （tags / caption_hint / qc.notes）
remotion/src/data/tekoh_film.json                   （figures[] / captions[] の全文字列と数値）
remotion/props/tekoh*.json                          （title / subtitle）
```

- **R-FORBID（最優先）** — §2.1 の禁止語が対象文字列のどこかに出たら即 FAIL。**近似語（否定文脈）を巻き込まない断定形のみ**を検査（§2.1 の注意）。
- **★R-CHARGE（C-5・最重要級・英語 AND 日本語・BLOCKING）** — 原被疑事実（疑われた罪の性質）語が**どの対象にも**出たら FAIL。CHARGE_BLOCK:
  ```python
  CHARGE_BLOCK = re.compile(
      r"sexual assault|sex crime|sex offen|\brape\b|molest|assault victim|\bthe victim\b|\bvictim\b|"
      r"guilty of|actually guilty|he did it|the crime he committed|"
      r"性的暴行|性犯罪|わいせつ|強制わいせつ|レイプ|被害者",
      re.IGNORECASE)
  ```
  ＝英語（sexual assault / rape 等）と日本語（性的暴行 / 性犯罪 / わいせつ）の両方を必ず含む。台本 verbatim は「suspected of something serious」「accused of a crime」で罪状を名指さないので自然に通る。
- **R-LEDGER** — figures[] の `value`/`numKeys` 到達値、AE `beats[].value`/`beats[].hero`、サムネ数字に現れる**あらゆる数値**は、
  `tekoh_facts.v*.json` に `verified:true` で存在する値に**完全一致**しなければ FAIL。日付は年/月/日に分解して照合（2014 / 2022-06-23 / 1966 / 2000、識別子 597/134/21-499/384/436/1983、投票 6/3、民事審理 2、反対 3 が許可集合）。
- **R-VOTE63（C-2）** — `6-3`/`6 – 3`/`six to three`/`6 to 3` を含むカード・figure は、**同一 payload 内**に限定修飾
  `{"one door closed","exclusion stays open","reversed","remanded","narrow","not the death of miranda","miranda stands"}` のいずれかを**必ず含む**こと。
  かつ `\b9-0\b`/`9 to 0`/`unanimous` を Vega の判決に付したら FAIL。`votetally` は **`majority:6, dissent:3`** のみ許可。
- **R-SCOPE（C-1・積極検証・BLOCKING）** — 射程非圧縮の**肯定**検出。次を全て満たさなければ FAIL:
  (1) 「排除の扉は開いたまま」系の payload が figures か AE に**存在する**（例：F06/F07 の「MIRANDA STANDS / DICKERSON STANDS」・AE m01・ENDING の "EXCLUSION STAYS OPEN"）。
  (2) 閉扉を語る payload は「§1983／civil damages／sue the officer for money」に**スコープされている**（無限定に「権利を読まなくてよくなった」と読める payload があれば FAIL）。
  (3) 「閉じた扉（§1983賠償）」と「開いた扉（刑事公判の排除）」の**両方**がどこかの payload で近接して並ぶ表現が存在する。
- **R-MIRANDA（C-3・BLOCKING）** — `Miranda`/`Dickerson` を含む payload に対し、`overturned/overruled/struck down/killed/reversed miranda` 系（覆滅の断定）が出たら FAIL。逆に "MIRANDA STANDS" / "DICKERSON STANDS" / "still good law" は許可（存続の肯定）。
- **R-1983（C-4）** — `Section 1983`/`§ 1983`/`42 U.S.C.` を含む payload に `no immunity` が共起したら FAIL。§1983 は「民事救済の扉／責任を問う扉」の趣旨で提示されていること。
- **R-ATTRIB（R-ATTRIB）** — `quote[].attribution` が非空。要約を引用符に入れない（逐語のみ）。許可対応表:
  ```python
  APPROVED_QUOTES = {
    # ★slip opinion の正確な逐語をここに1行で置く。確定できなければ q01 を required:false にして本表を空のままにする。
    "<KAGAN_DISSENT_VERBATIM>": "Justice Kagan, dissenting (joined by Justices Breyer and Sotomayor)",
  }
  ```
  逐語が確定できない間は q01 を `required:false`（`validate_tekoh_beats` が除外・§7.9-6）。**捏造した“逐語”を引用符に入れたら R-ATTRIB/R-LEDGER で FAIL。**
- **R-PERSON（C-6）／R-FACE／R-DOC（R1）** — `qc.has_readable_text`/`qc.has_identifiable_face`/`qc.has_human_body` が true の項目は `role=="reject"`。
  `Terence Tekoh`/`Tekoh`/`Carlos Vega`/`Vega`（人名文脈）と人物化語（`face`/`portrait`/`likeness`/`appearance`/`his body`/`the man's eyes` 等・内面語）の同一文共起を FAIL。
  事件主体語（"Terence Tekoh sued" / "Deputy Carlos Vega" / "a private person who was accused and cleared"）は許可。読める偽公文書の主張語（`legible`/`actual court filing`/`real report` を肯定文脈で）を FAIL。
- **★R-DOCHILITE（EP44固有・BLOCKING）** — `tekoh_film.json` の `figures[]` および `08_edit/ae_hero/beats.json` の全 payload に `"kind":"dochighlight"`（またはレイアウトに dochighlight 相当）が**1件でも**あれば FAIL。**redacted 表現が要るなら象徴 still（守りの柵・閉じた扉）で代替し、dochighlight を使わない。**
- **R-DATE** — F01(2022-06-23) / F09(2014) / F06(1966) / F07(2000) の日付・年が別カードで取り違えられていないこと。

**出力:** `episodes/PD-2026-044-tekoh/09_package/facts_lock.v001.json`（`{"pass":bool,"violations":[...],"skipped":[...]}`）。
**`pass:true` でない限り `check_final_acceptance.py` に進んではならない。**
**CLI:** `--json`（★`--dryrun` の別コードパスは作らない・EP44 は実素材のみ）。対象ファイルが未生成ならスキップして必ずログに出す。「無いから通した」を黙るな。

---

# 3. ★境界契約: `asset_manifest.v001.json`（Aから受け取る唯一のファイル・A↔B一字一致）

## 3.1 スキーマ（**Aが生成する。Bはこの形を前提に読む**）

**スキーマ版:** `tekoh_assets.v1`（固定文字列。異なれば **exit 2**）。
EP44 spec の点数に**厳密一致**: **still_body 85 / still_i2v_source 16 / motion 16 / factory 93 / overlay 12**。
**★サムネは独立の分類を持たない。** body 85枚のうち**6枚**に `also_thumb:true` を立てて流用する（**`role=thumb`/`still_thumb` を作らない**・サムネ用 count キーも無い・§11）。
**このスキーマ・`counts` キー・`role` enum・`overlay` 枚数は CODEX_A（生産者）の `build_tekoh_asset_manifest.py` の出力と1バイト単位で同一。**

- **`role` enum（固定・3値のみ）:** `"body"` | `"i2v_source"` | `"reject"`。**`thumb`/`still_thumb` を作らない。**
- **`counts`（固定キー・厳密値）:** `{ "still_body": 85, "still_i2v_source": 16, "motion": 16, "factory": 93, "overlay": 12 }`。
- **`is_stub`:** 本番は **`false`**（EP44 は実素材のみ・stub を受け付けない）。
- **asset_id パターン:** body `^TEKOH-S\d{2}$`（S01..S85）／ i2v_source `^TEKOH-MS\d{2}$`（MS01..MS16・種画像 M01_src..M16_src）／ motion `^TEKOH-M\d{2}$`（M01..M16）。
- **`overlay` = 12**（A↔B 契約値）。

```jsonc
{
  "schema_version": "tekoh_assets.v1",
  "episode_id": "PD-2026-044-tekoh",
  "slug": "tekoh",
  "generated_at": "<ISO8601>",
  "producer": "scripts/build_tekoh_asset_manifest.py",
  "is_stub": false,
  "counts": { "still_body": 85, "still_i2v_source": 16, "motion": 16, "factory": 93, "overlay": 12 },

  "stills": [
    { "asset_id": "TEKOH-S01", "scene_id": "S01", "role": "body",   // body|i2v_source|reject（各1枚）
      "also_thumb": false,                   // body から6枚だけ true（§11 の6シーン・追加生成しない）
      "act": 0,                              // 0=HOOK/OP, 1..3=幕, 5=ED
      "public_path": "tekoh/img/S01.png",    // ★Bが cuts[].src に入れる値（1シーン1枚・接尾なし）
      "depth_path": "H:/pd-media/assets/ai/tekoh/S01_depth.png",  // role=="body" は実在必須
      "width": 3840, "height": 2160,
      "sha256": "...", "tags": ["hospital_corridor","pen","signature_line","symbolic","night"],
      "caption_hint": "a pen resting on a written page above a blank signature line",
      "source": "ai_codex", "commercial_use": "allowed", "ai_disclosure_required": true,
      "qc": {"reviewed": true, "on_theme": true,
             "has_readable_text": false, "has_identifiable_face": false, "has_human_body": false, "notes": ""} }
    // i2v 種は role=="i2v_source"・asset_id "TEKOH-MS01".."TEKOH-MS16"・public_path は null（本編カットに出ない）
  ],
  "motion": [
    { "asset_id": "TEKOH-M01", "source_scene_id": "M01_src",   // ★i2v_source 種 ID を指す（body still ではない）
      "source_still": "H:/pd-media/assets/ai/tekoh/M01_src.png",
      "public_path": "tekoh/motion/M01_rife.mp4",   // ★必ず .mp4 かつ "_rife" を含む
      "act": 0, "width": 1280, "height": 720, "fps": 48, "frames": 164, "duration_sec": 3.417,
      "sha256": "...", "tags": ["pen","signature_line"],
      "qc": {"reviewed": true, "on_theme": true, "artifact_free": true, "notes": ""} }
  ],
  "factory": [
    { "asset_id": "AF-BG-0731",
      "public_path": "tekoh/factory/AF-BG-0731__empty_jury_box.mp4",  // ★必ず "/factory/" を含む
      "type": "backgrounds", "subtype": "empty_jury_box", "kind": "video",
      "license": "Pexels License", "sha256": "...", "act": 2, "covers_scene_id": "S24",
      "duration_sec": 7.60, "width": 1920, "height": 1080, "mean_luma": 48.3,
      "eyeballed_content": "an empty jury box of twelve wooden seats in cold light, no people",
      "qc": {"reviewed": true, "on_theme": true, "no_watermark": true,
             "no_recognizable_person": true, "no_cartoon": true, "label_matches_content": true, "notes": ""} }
  ],
  "overlay": [
    { "asset_id": "AF-PART-0044",
      "public_path": "tekoh/overlay/AF-PART-0044__dust_motes.mp4",
      "type": "particle_assets", "subtype": "dust_motes", "license": "Pexels License",
      "sha256": "...", "blend_hint": "screen",
      "eyeballed_content": "slow dust motes drifting on black, loops cleanly",
      "qc": {"reviewed": true, "on_theme": true, "no_watermark": true, "notes": ""} }
  ]
}
```

## 3.2 Bがこのマニフェストから作るもの（**EP44 spec の cuts 割当**）

| マニフェスト | Bでの使い道 | spec |
|---|---|---|
| `stills[role="body"]` 85枚 | **静止画カット101本**（`kind:"img"`, `treatment` 循環）・**各≤2回** | still distinct85/cuts101 |
| body 静止画で `also_thumb==true` の6枚 | サムネ3案の背景（§11・6シーン `{S02,S04,S24,S44,S45,S85}`） | — |
| `stills[role="i2v_source"]` 16枚 | **本編カットに出さない**（i2v 種・A が Wan で motion 化済み） | — |
| `motion` 16本 | **i2vカット32本**（`kind:"footage"`）・**各≤2回** | motion distinct16/cuts32 |
| `factory` 93本 | **実写カット93本**（`kind:"footage"`）・**各1回のみ** | factory distinct93/cuts93 |
| `overlay` 12本 | **`cuts[].src` に出さない**（§5.5 の合成レイヤー扱い） | — |

**合計 101 + 32 + 93 = 226 カット / distinct 85+16+93 = 194 / first-use 194/226 = 0.8584 ✓（floor 0.70）**

## 3.3 `scripts/check_tekoh_asset_manifest.py`（消費側バリデータ・BLOCKING・★A §4.2 と一字一致の16不変条件）

```bash
$PY scripts/check_tekoh_asset_manifest.py --assets <path> [--json]
```

検査（1つでも違反で exit 1。`schema_version` 違いだけ exit 2）。**この16項は CODEX_A §4.2 と一字一致:**

1. `schema_version=="tekoh_assets.v1"` / `episode_id=="PD-2026-044-tekoh"` / `slug=="tekoh"` / **`is_stub==false`**
2. `counts.*` が各配列の実長と**完全一致**し §3.1 の値（body **85** / i2v_source **16** / motion **16** / factory **93** / overlay **12**）に**一致**（`still_body` は `stills[role=="body"]` の実長、`still_i2v_source` は `stills[role=="i2v_source"]` の実長）
3. 全 `path`/`depth_path`/`public_path` がディスクに実在
4. `sha256` が全配列を通して一意（重複ゼロ）
5. `role!="reject"` の全静止画で `max(width,height)>=3840`
6. `role=="body"` は `depth_path` と `public_path` が非null かつ実在（`CaseFilm.depthSrcOf()=src.replace(/\.[^.]+$/,'_depth.png')`。depth 欠落はレンダークラッシュ）
7. `qc.has_readable_text==true` / `qc.has_identifiable_face==true` / `qc.has_human_body==true` のいずれかは `role=="reject"`（R1）
8. `role=="i2v_source"` は `role=="body"` と**同一 asset_id を共有しない**（`^TEKOH-MS\d{2}$`）
9. 全JSON文字列が `BANNED_PORTRAIT` **および** `BANNED_ACCURACY`（§2.1 相当）に一致しない
10. `factory[].license`/`overlay[].license` が `ALLOWED_LICENSES`（§3.1 の集合）に含まれる
11. `factory[].sha256` が **EP39・EP40・EP41・EP42・EP43 の staged 素材**と1件も衝突しない（A 保証・B は自集合内一意を検査）
12. `factory[].eyeballed_content` が空でない
13. `factory[].qc.label_matches_content==true`
14. **`also_thumb==true` の本数が**ちょうど6**、かつ `scene_id` 集合が `{S02,S04,S24,S44,S45,S85}` と完全一致**（追加生成でなく body からの流用。**この集合は CODEX_A §4.3／§11 と一字一致必須の A↔B 契約点**）
15. `role` に `thumb`/`still_thumb` が存在しない（enum は body|i2v_source|reject のみ）
16. `overlay` 配列長が**ちょうど12**

> **★このバリデータは A の凍結マニフェストが上記16を満たすことを消費前に再確認するもの。** 1つでも落ちたら組まずに止めて報告する（A に差し戻す・自分でマニフェストを書き換えない）。
> `also_thumb` の scene_id 集合 `{S02,S04,S24,S44,S45,S85}`・`counts`・`role` enum・`overlay=12` を A と食い違わせない（§11・§14）。

## 3.4 本番マニフェスト（**stub を作らない**）
EP44 は実素材のみ。`05_visuals/asset_manifest.v001.json`（A が凍結出力・`is_stub==false`）を `--assets` に渡す。
**`make_*_stub_assets.py` / `asset_manifest.stub.*.json` / `_dryrun/` は作らない**（§0.1 の設計転換）。

---

# 4. narration_index（TTS は課金＝Bは起動しない。**実測 index を消費する**）

## 4.1 なぜ narration_index か
`build_tekoh_film.py` は**尺・区間・字幕を narration_index から導出する**。**秒数をコードに直書きしない。** 唯一の正は narration_index。

## 4.2 スキーマ（`tekoh_narration.v1`）

```jsonc
{
  "schema_version": "tekoh_narration.v1",
  "episode_id": "PD-2026-044-tekoh",
  "is_stub": false,
  "total_seconds": 720.6,
  "chunks": [
    { "section": "HOOK", "start": 0.000, "end": 4.100,
      "text": "A hospital hallway in Los Angeles, late at night." },
    { "section": "OP",   "start": 25.0, "end": 29.1, "text": "..." },
    { "section": "ACT_1","start": 79.2, "end": 83.4, "text": "..." }
  ]
}
```

**section 値（固定・6区間）:** `HOOK` / `OP` / `ACT_1` / `ACT_2` / `ACT_3` / `ENDING`。
（EP44 の BODY は 3幕＝ACT_1「That night」/ ACT_2「The turn」/ ACT_3「The doctrine」＋payoff。**ACT_4 は無い。**）
`build_tekoh_film.py` は `section_windows()`（各 section の最初のチャンク start）で幕境界を得る。
**台本の `[SILENCE 1..6]`（実音無音・最低6箇所）は無音ギャップとして時間を進める**（実測 index に既に反映されている）。

## 4.3 spec のタイムライン（**設計目標。実タイミングは narration_index が上書きする**）

| section | 語数 | 秒（SPEC） | 備考 |
|---|---|---|---|
| HOOK | 98 | 33.0 | VO。`[SILENCE 1] 2s`（ペン上の署名欄）を含む。**6-3・"6/3" カードは出さない** |
| （teal `BrandOpening`） | 0 | 3.50 | 非VO。`OPENING_SEC`。**HOOK の問いの後**に resolve |
| OP | 137 | 46.2 | 二人称の問い（thesis）＋ channel ID。`[SILENCE 2] 1.5s` |
| ACT_1 That night | 230 | 77.5 | 最短・現在形・抑制。`[SILENCE 3] 2s`（ペンが横たわる完成ページ） |
| ACT_2 The turn | 448 | 150.9 | 無罪→民事提訴→§1983→二度の敗訴→第9巡回区。`[SILENCE 4] 2s`（空の陪審席） |
| ACT_3 The doctrine ＋payoff | 631 + 222 = 853 | 212.6 + 74.8 = 287.4 | 判例核。**最も遅く長い**。6-3 は**ここで初めて**開示。`[SILENCE 5] 2s`（空ベンチ・列柱光） |
| ENDING | 330 | 111.2 | ペイオフ→CTA。`[SILENCE 6] 1.5s`（署名だけのページ） |
| （`BrandEndcard`） | 0 | 9.00 | 非VO。`ENDCARD_SEC` |

**唯一の正は `python scripts/check_script_length.py <script> --json`。** 総語数 **2,139**（spec `words_total`）/ `wpm 178.1` /
narration_seconds **720.6**（spec・純発話＋設計無音）。**自己申告・体感の尺判定は禁止。**

## 4.4 実測 index の入手（**Bは課金 TTS を起動しない**）
別工程が TTS→faster-whisper で `06_audio/narration_index.v001.json`（実測語タイム・`is_stub:false`）を作る。
**これは課金ジョブなので B は起動しない。** 来ている前提で `--narr` に渡す。台本本文はそのまま（改変しない）。
`【…】/〔…〕/[…]/(…)` の apparatus・ト書きは非発話として除外済みであること（`>` 行のみ計上）。

---

# 5. `tekoh_film.json` の構築（`scripts/build_tekoh_film.py`＝`build_caniglia_film.py` の複製）

## 5.1 `FilmData` 型（`CaseFilm.tsx` から。これに従う）

```ts
export type Cut = {start:number; dur:number; kind:'img'|'footage'; src:string; treatment:string; seed:string};
export type FilmData = {
  fps:number; narration:string; narrationSeconds:number; hookSeconds:number; hookLine:string;
  hook:{start:number;dur:number;kind:string;src:string;seed:string}[];
  cuts:Cut[]; captions:{start:number;end:number;text:string}[];
  graphics:{start:number;end:number;lines:string[]}[];      // 必須フィールド。EP44 は []
  figures?:FigureSpec[]; heroCuts?:{start:number;dur:number;src:string}[];
};
export const caseFilmDurationInFrames = (data, fps) =>
  Math.round((data.hookSeconds||0)*fps) + Math.round(OPENING_SEC*fps)
  + Math.ceil(data.narrationSeconds*fps) + Math.round(ENDCARD_SEC*fps);
```

- アセットのパスキーは **`src`**（`remotion/public/` からの相対、`staticFile()` 解決）
- 動きは `treatment`・`seed`・`index%2`・`index%3` から導出。`treatment` 実装値: `'depth'|'scan'|'duotone'|'focus'|'card'|'bleed'`（既定 bleed）
- `kind:'footage'` は `treatment` を無視して `<Footage>` を描画する
- **`fps = 30`**（EP42/43 と同じ film fps）。`narration = "tekoh/narration.mp3"`（本番のみ実在）

### 5.1.1 ★durationInFrames の4項関数（明示・total ≤ 750s を assert）

```
caseFilmDurationInFrames(tekohFilm, fps=30)
  = round(hookSeconds * fps)        // hookSeconds = 0.0（HOOK の VO は narrationSeconds に含む。frame0 に別 hook 尺を積まない）
  + round(OPENING_SEC * fps)        // OPENING_SEC = 3.50（teal BrandOpening は HOOK の後）
  + ceil(narrationSeconds * fps)    // narrationSeconds = narration_index.total_seconds（≈720.6・silence 込み）
  + round(ENDCARD_SEC * fps)        // ENDCARD_SEC = 9.00
```

- **hookSeconds を明示: `hookSeconds = 0.0`**（HOOK ナレは narrationSeconds に内包・§4.2 の section=HOOK）。
- 概算（fps30・narration≈720.6）: `0 + 105 + ceil(21618) + 270 = 21993 frames = 733.1s`。
- **ビルダ末尾で `assert total_frames/fps <= 750.0`**。超えたら exit 1。

## 5.2 カット構成（**§3 マニフェストから機械的に組む・紙芝居回避が最優先**）

```
総カット 226 = factory 93 (footage) + motion 32 (footage) + 静止画 101 (img)

[A] first-use share（check_asset_reuse floor 0.70）
    distinct 93+16+85 = 194 → 194/226 = 0.8584            ✓ >=0.70

[B] per-asset cap（check_asset_reuse）
    factory: 93/93  = 1.00回  ✓ <=1（★factory は再使用禁止）
    motion : 32/16  = 2.00回  ✓ <=2
    still  : 101/85 = 1.19回  ✓ <=2

[C] animation_mix（★2つの尺度を両方満たす）
    (i) cut数ベース   still-share = 101/226 = 0.4469        ✓ <=0.45（★余裕が薄い＝§下の警告）
        motion coverage = (93+32)/226 = 125/226 = 0.5531    ✓ >=0.45
    (ii) frame ベース still 平均 ~3.00s → 101×3.00 = 303.0s
        footage 平均 ~3.35s → 125×3.35 ≈ 418.3s
        still-frame-share = 303.0 / 720.6 = 0.4205          ✓ <=0.45（cut数比より安全側）

[D] 平均ショット長（spec mean_shot 3.19 / max 6.0）
    720.6 / 226 = 3.188 秒/カット                          ✓ <=6

[E] factory 下限（30秒に1本 = 24 → >=24本） 93本            ✓
```

> **★[C](i) の cut数ベース still-share 0.4469 は cap 0.45 に薄い。still を1枚増やすか factory を1本削ると 0.45 を超える。**
> **マニフェストが still 85 / factory 93 / motion 16 を割ったら組まずに止めて A に差し戻す（still を増やして factory を削るな）。**
> **frame ベースも下回るよう、still の平均尺を footage より系統的に短く保つ（§5.3-5）。**

## 5.3 カット割り当てのルール（`build_caniglia_film.py` の `allocate()`/`tile_window()` を踏襲）

1. 各幕の秒窓を `section_windows()` から取り、幕内に **factory : motion : still を按分**して配置（目安・実配分は窓長で自動調整）:

   | section | factory | motion | still | 小計 |
   |---|---|---|---|---|
   | HOOK+OP | 9 | 2 | 11 | 22 |
   | ACT_1 | 12 | 3 | 12 | 27 |
   | ACT_2 | 16 | 3 | 16 | 35 |
   | ACT_3 ＋payoff | 44 | 16 | 41 | 101 |
   | ENDING | 12 | 8 | 21 | 41 |
   | **計** | **93** | **32** | **101** | **226** |

2. **factory は各1回のみ**（使用済み集合を持ち二度と引かない）。**motion は各≤2回・still は各≤2回**（`allocate(cap=…)`）
3. **同一素材を連続させない**（順序を散らす）
4. 静止画 `treatment` は `["depth","scan","duotone","focus"]` を循環（同じ treatment を3連続させない）
5. **still の `dur` を footage の `dur` より系統的に短く**（§5.2[C]・`tile_window` の重みで still 側を小さめに）
6. motion の `dur` は **3.0–3.4秒**（実素材 3.417s。超えるとループが見える）
7. **AEカードの区間（§7.2）に重なるカットも存在させる**（コンポジタ SKIP 時に穴が空かないため）

## 5.4 `figures[]` と `captions[]`
- `figures[]` は §6（**37本**・spec floor **31** に +6・`graphics[]=[]`・**dochighlight を1本も生成しない**）
- `captions[]` は narration_index の全チャンクを **verbatim**（`build_captions()` と同一）。SRT も同時出力

## 5.5 合成レイヤー（`overlay`）— **`cuts[].src` に出さない**
`overlay` 12本は「加工」。`cuts[].src` に入れると `kind_of()` が factory 判定（上限1回）になり FAIL する。
`tekoh_film.json` に **`overlays` 独自キー**で持たせる（`CaseFilm` は未知キーを無視）か、専用レイヤーで `screen` 合成する。**発色は accent `#2FA6A0` 側に寄せる。**

## 5.6 ビルダが出力する成果物

| 出力 | パス |
|---|---|
| film.json | `remotion/src/data/tekoh_film.json` |
| public コピー | `remotion/public/tekoh/film_data.v001.json` |
| **build provenance** | `episodes/PD-2026-044-tekoh/04_scenes/tekoh_build_manifest.v001.json`（**A の `05_visuals/asset_manifest` に書かない**） |
| **beatsheet**（figures+AE区間の突き合わせ表） | `episodes/PD-2026-044-tekoh/04_scenes/tekoh_beatsheet.v001.json` |
| SRT（字幕未生成時のフォールバック） | `episodes/PD-2026-044-tekoh/08_edit/captions.final.v001.srt`（**§8 の生成器が上書きする**） |

> **★beatsheet の命名に関する重大な注意:** `check_motion_density` / `check_animation_mix` は
> `04_scenes/premium_beatsheet.v*.json` を**自動検出して film.json より優先**する。
> **B の beatsheet は `tekoh_beatsheet.v001.json`（`premium_` を付けない）** にして、**ゲートの測定源を film.json 一本に保つ。**

## 5.7 CLI
```bash
$PY scripts/build_tekoh_film.py \
  --assets episodes/PD-2026-044-tekoh/05_visuals/asset_manifest.v001.json \
  --narr   episodes/PD-2026-044-tekoh/06_audio/narration_index.v001.json \
  --out    remotion/src/data/tekoh_film.json \
  [--captions episodes/PD-2026-044-tekoh/08_edit/captions.final.v001.srt]
```
**実素材のみ・`is_stub` による分岐を作らない（§0.1）。** 末尾に `check_asset_reuse` 相当の自己レポートを print する。

---

# 6. Remotion 側 `figures[]`（**37本・spec floor 31 に +6・`graphics[]=[]`・dochighlight ゼロ**）

## 6.1 密度の検算（`check_motion_density`・**AEカードは1本も数えられない**）

```
figures 37本（film.json） / body 12.01分(=720.6/60) = 3.08 /分    ✓ beats_per_min_floor 2.5
coverage: 37本 × 平均5.4s = 199.8s / 720.6 = 27.7%                 ✓ MIN_ANIMATED_COVERAGE 0.25
variety : 下記 kind を12種以上使用                                ✓ variety_floor 3
spec motion.beats_floor = 31 に対し 37 で余裕。coverage が最も薄いので figures の dur は 4.8–6.0s を基本に。
```

> **★3軸すべて AND。density/coverage/variety のどれか1つでも floor 未満で FAIL。** 37本を非重複で置き、平均 dur を 5.4s 程度に確保。

## 6.2 ★★★ `FigureSpec` の `kind` は**実在する小文字値のみ** ★★★

> **大文字名は無言で描画が消える。`comparebars` は非在→`compbars`。★`dochighlight` は本作で1本も使わない（R-DOCHILITE）。**

**EP44 で使う実在 `kind`（`FigureBeats.tsx` の union から。全て `start`/`end` 必須・全小文字）:**

| `kind` | 必須プロパティ | EP44での用途 |
|---|---|---|
| `numberticker` | `value:number` / `label?` / `prefix?` `suffix?` `decimals?` | 二度の民事審理・年 |
| `stat` | `value:number` / `label:string` / `topLabel?` | **2 TRIALS**（F11）・反対3人（F05・帰属） |
| `votetally` | `majority:number` / `dissent:number` / `label?` | **6対3**（F03・R-VOTE63・label に限定併記） |
| `timeline` | `events:{year:string;text:string}[]` | 2014→acquittal→§1983→2022 / 1966 Miranda→2000 Dickerson→2022 |
| `quote` | `quote:string` / `attribution:string` | Kagan 逐語（**帰属必須**・R-ATTRIB・逐語のみ・§2.2 F16） |
| `kinetic` | `lines:string[]` / `style?:'wordpop'\|'maskslide'\|'emphasis'` / `emphasisWords?` | 決め所テキスト（**emphasisWords は1–2語**） |
| `lowerthird` | `primary:string` / `secondary?` / `accent?` | 開示 `AI-assisted visualization` / 判例引用 / §1983 / MIRANDA STANDS |
| `acttitle` | `title:string` / `kicker?` / `index?` | 幕頭（Remotion 側で密度に数える。§7 の AE 幕頭とは別区間） |
| `compbars` | `items:{label:string;value:number;accent?}[]` | 「a fence」vs「the ground」／閉扉 vs 開扉（★`comparebars` は非在） |
| `mechanism` | `mechanism:'closingdoor'\|'gears'\|'faultsplit'` ★discriminant は `kind`・変種は `mechanism` | 閉じる第2の扉／開いたままの排除の扉(closingdoor)・rule→broken→remedy の論理(gears)・prophylactic の線(faultsplit) |
| `regionmap` / `pindropmap` | `label?` / `pins:{x,y,label?}[]` | Los Angeles（象徴・顔なし） |

**`votetally` は `majority:6, dissent:3` 固定（Vega v. Tekoh の 6-3・§2 R-VOTE63・label に限定併記）。**
`quote[].attribution` は §2 の `APPROVED_QUOTES` に一致（Kagan 帰属）。**逐語のみ・要約を引用符に入れない。**
**★`dochighlight` を payload に一切作らない（R-DOCHILITE で FAIL）。**

## 6.3 figures アンカー設計（`build_caniglia_film.py` の `FIGURE_ANCHORS` 方式）

**方式:** `(anchor_sec, payload)` を秒昇順に置き、`build_figures()` が
`end = min(anchor+FIG_DUR, next_anchor-FIG_GAP, total-0.5)` でクランプ、`end-start < FIG_MIN_DUR` なら **exit 1**。
`FIG_DUR=5.4 / FIG_MIN_DUR=3.0 / FIG_GAP=0.4`。**アンカー秒は `section_windows()` 基準のオフセットで置く**（秒直書き禁止）。

**配置方針（37本・§2 台帳の値だけを焼く・kind を分散して variety を稼ぐ・6制約順守・dochighlight ゼロ）:**

- **HOOK/OP（3）:** `kinetic`（"THE WORDS THEY NEVER READ YOU"）/ `lowerthird`（`AI-assisted visualization` 開示）/ `mechanism:closingdoor`（署名欄・警告なし＝閉じかけの扉。★6-3 は出さない）
- **ACT_1（6）:** `acttitle`（THAT NIGHT）/ `timeline`（**F09 2014 · medical center, Los Angeles**）/ `pindropmap`（LOS ANGELES・象徴）/ `kinetic`（"NO WARNING CAME"・emphasisWords=["WARNING"]）/ `lowerthird`（**F10 Deputy Carlos Vega**＝事件主体・象徴描写・C-6）/ `mechanism:closingdoor`（ペンが横たわる完成ページ）
- **ACT_2（8）:** `acttitle`（THE TURN）/ `kinetic`（"THEY ACQUITTED HIM"／**F12**・emphasisWords=["ACQUITTED"]）/ `lowerthird`（**F08 42 U.S.C. § 1983**, secondary "a door to hold him to account"／C-4・**no immunity と書かない**）/ `stat`（**F11 2**, label "civil trials · twice for the deputy"）/ `timeline`（**F13** acquittal → §1983 suit → Ninth Circuit reversed & remanded）/ `kinetic:emphasis`（"A CIVIL CLAIM FOR MONEY"・emphasisWords=["MONEY"]）/ `mechanism:gears`（見守り→責任追及の民事へ）/ `lowerthird`（"a private person, accused and cleared"／C-5・**罪状を名指さない**）
- **ACT_3（15）:** `acttitle`（THE DOCTRINE）/ `lowerthird`（**F06 Miranda v. Arizona, 384 U.S. 436 (1966)**, secondary "STILL GOOD LAW"／C-3）/ `lowerthird`（**F07 Dickerson v. United States (2000)**, secondary "MIRANDA STANDS"／C-3）/ `timeline`（1966 Miranda → 2000 Dickerson → **F01 2022** Vega v. Tekoh）/ `lowerthird`（**F02 Vega v. Tekoh, 597 U.S. 134 (2022), No. 21-499**）/ `votetally`（**F03 6対3**, label "one door closed · exclusion stays open"／**C-2・R-VOTE63**）/ `stat`（**F04**／"Alito, for six of nine"・帰属）/ `mechanism:faultsplit`（prophylactic の線＝柵と地面）/ `compbars`（**F14** items=[{label:"THE WARNING — a fence",value:1},{label:"THE FIFTH AMENDMENT — the ground it stands on",value:1}]／"a fence, not the ground"）/ `kinetic`（"RULE · BROKEN · REMEDY"）/ `kinetic:emphasis`（"THE MAJORITY DID NOT SEE IT AS SIMPLE"・emphasisWords=["SIMPLE"]）/ `lowerthird`（**F15** "a Miranda violation, standing alone, is no §1983 damages"／C-1）/ `stat`（**F05 3**, label "in dissent · Kagan, Breyer, Sotomayor"・帰属）/ `quote`（**F16 Kagan 逐語** → "Justice Kagan, dissenting"／R-ATTRIB・逐語未確定なら除外）/ `mechanism:closingdoor`（第2の扉が閉じる一方、排除の扉は開いたまま）
- **ENDING（5）:** `kinetic`（"A RIGHT AND A REMEDY ARE NOT THE SAME"・emphasisWords=["REMEDY"]／C-1）/ `lowerthird`（"EXCLUSION STAYS OPEN", secondary "your unwarned words can still be kept out"／**C-1・R-SCOPE**）/ `lowerthird`（開示 `AI-assisted visualization` 再掲）/ `compbars`（items=[{label:"THE SHIELD — still raised for you",value:1},{label:"THE PAYMENT — for a warning skipped, not there to take",value:1}]／C-1）/ `mechanism:closingdoor`（夜明け・開いたままの排除の扉と閉じた §1983 の扉）

> **6-3（F03）を figure に焼くときは必ず `votetally` の `label` に "one door closed · exclusion stays open" を付ける（R-VOTE63）。単独の勝利数として出さない。**
> **どの payload にも「9-0／unanimous」「Miranda overturned」「no immunity」「原被疑事実語（EN/JP）」を出さない。dochighlight を作らない。**

## 6.4 配置ルール
1. **AEの区間（§7.2）と1秒でも重ならない**（`validate_tekoh_beats` が突き合わせ）
2. **同じ kind を連続させない**（`mechanism` の直後に `mechanism` を置かない）
3. 1枠 **4.8–6.0秒**
4. `quote[].quote` / `kinetic[].lines` / `*.label` は §2 の R-LEDGER・R-ATTRIB・R-FORBID・R-CHARGE・R-VOTE63・R-SCOPE・R-MIRANDA・R-1983・R-PERSON 検査対象
5. 台帳外の数値を `value`/`numKeys` に置かない（R-LEDGER で FAIL）
6. **`emphasisWords` は1–2語の短句のみ**（長句は末尾が切れる＝EP40 実害）

---

# 7. After Effects カード（`build_tekoh_hero_cards.py` / `composite_tekoh_hero.py`）

## 7.1 位置づけ
AEカードは **film.json とは別**に ffmpeg で本編に焼き込む（§0.5-2＝密度に数えられない）。
`build_young_hero_cards.py`（＝`build_thompson_hero_cards.py` 系）を**コピーしてパス・定数・CARDS デッキだけ差し替える**。
レイアウト実装・`money_keys()`・`fit_size()`・完了マーカー・機械の罠対処は**1行も削らない**。

## 7.2 AEカードデッキ（**単調増加・重複ゼロ・台帳裏付けのみ・6制約順守。この表が契約。8枚**）

**★id・レイアウト・label（hero）・順序は DESIGN §6（ブリーフ§6 の候補8本）と一字一致。** 下表は **start 昇順（time-order）**。
**レイアウト名は §7.3 の実装済み8種のみ。背景静止画は象徴オブジェのみ（R1/C-5/C-6）。988 系・crisis 系は本作に無い。**

| id | レイアウト（**実装済み8種のみ・§7.3**） | hero（主表示・DESIGN §6 label） | top / sub / bottom / attribution | F-ID | 背景（象徴のみ） | required |
|---|---|---|---|---|---|---|
| a01 | CENTER_STACK | **ACQUITTED** | top: **THE VERDICT** / bottom: **A JURY HEARD IT ALL AND LET HIM GO** | F12 | S24 空の陪審席 | 必須 |
| s01 | CENTER_STACK | **SECTION 1983** | top: **THE CIVIL DOOR** / bottom: **SUE A STATE OFFICIAL FOR A CONSTITUTIONAL WRONG** | F08 | S31/S32 連邦法の書物・開いた扉 | 必須 |
| t01 | CENTER_STACK | **2 TRIALS** | top: **THE CIVIL SUIT** / bottom: **TWICE TRIED · TWICE FOR THE DEPUTY** | F11 | S33 二重像のベンチ | 必須 |
| d01 | DATE_STAMP | **2022** | place/sub: **SUPREME COURT OF THE UNITED STATES** | F01 | S36 最高裁の列柱 | 必須 |
| m01 | SPLIT_COMPARE | **MIRANDA STANDS / DICKERSON STANDS** | top: **WHAT THE RULING DID NOT TOUCH** / bottom: **1966 · 2000 — STILL GOOD LAW** | F06/F07 | 左=S38 1966の書物 / 右=S40 2000の書物 | 必須 |
| f01 | CENTER_STACK | **A FENCE, NOT THE GROUND** | top: **THE PROPHYLACTIC LINE** / bottom: **THE WARNING GUARDS THE RIGHT — IT IS NOT THE RIGHT** | F14 | S45 守りの柵 | 必須 |
| v01 | VOTE_SPLIT | **6 – 3** | top: **VEGA v. TEKOH — 2022** / bottom: **ONE DOOR CLOSED · EXCLUSION STAYS OPEN** | F03 | S44 9席・影で分割 | 必須 |
| q01 | QUOTE_CARD | **"<Kagan 逐語・F16>"** | attribution: **JUSTICE KAGAN, IN DISSENT** | F16 | S65 列柱の光条 | F16 verified 時のみ |

> **★q01 の QUOTE_CARD は逐語（R-ATTRIB）。** ブリーフ§6 の略記や要約を**引用符の中に入れない**。quote 文字列は §2 `APPROVED_QUOTES`＝slip opinion の逐語と一致必須。**逐語が確定できない間は `required:false`（`validate_tekoh_beats §7.9-6` が除外）＝捏造しない。**
> **v01 の bottom は "ONE DOOR CLOSED · EXCLUSION STAYS OPEN"（C-2・R-VOTE63）。9-0／全会一致／full victory を書かない。**
> **f01「A FENCE, NOT THE GROUND」は逐語ではないので QUOTE_CARD にしない（要約を引用符に入れると R-ATTRIB で FAIL）＝CENTER_STACK。**
> **m01 は「Miranda/Dickerson は存続」を明示（C-3・R-MIRANDA）。s01 に "no immunity" を書かない（C-4・R-1983）。どのカードにも原被疑事実（EN/JP）を出さない（C-5・R-CHARGE）。dochighlight レイアウトは使わない。**

**検算（Codex は自分で再計算して一致を確認）:** 8区間・単調増加・重複ゼロ・HOOK(0–33.0) と ENDCARD(末尾9s) に重ねない。
Remotion figures(§6) と1秒も重ならない（`validate_tekoh_beats` が検査）。**a01/s01/t01 は ACT_2、d01/m01/f01/v01/q01 は ACT_3 の窓に置く（start 昇順）。**

## 7.3 レイアウト（`build_young_hero_cards.py` の実装を踏襲・**実装済みレイアウト名だけを使う**）
複製元が実装するレイアウトは**この8種のみ**:
`DATE_STAMP` / `CENTER_STACK` / `MONEY_STACK` / `SPLIT_COMPARE` / `ACT_TITLE_CARD` / `QUOTE_CARD` / `VOTE_SPLIT` / `SEAM_TRANSITION`。
**§7.2 デッキはこの8種の名前しか使わない**（上記以外の独自レイアウト名を発明しない＝`validate_tekoh_beats` §7.9 ルール3 で FAIL）。
**EP44 は MONEY_STACK / ACT_TITLE_CARD / SEAM_TRANSITION を §7.2 では未使用**（この案件に金額は無く、幕頭は Remotion 側 `acttitle` が担う）。
**共通レイヤースタック・Anton/Oswald・`psName()` の runtime 解決（allFonts の array-LIKE ラッパーを unwrap）は複製元と同一。**

**★共通レイヤースタックに AI開示レイヤーを1枚追加（R1・全カード常時焼き）:** 最上位に近い固定レイヤーとして
`AI-assisted visualization`（Oswald 20px / SILVER `#C8CDD6` / opacity 70% / 右下 `[W-32, H-28]`）を全カードに焼く。
AEカードは不透明の全画面 mp4 として本編に overlay されるため、これが無いと本編(Remotion)右下の開示が隠れる（R1違反）。字幕帯とは縦56px 以上離す。

**★EP44 色定数（0..1 float・interrogation-teal レーン色。EP41 gold / EP42 blue / EP43 amber を流用禁止・DESIGN と一致）:**
```python
ACCENT = [0.184, 0.651, 0.627]  # #2FA6A0 interrogation-teal アクセント（数値・下線・レーン分離）
WHITE  = [0.961, 0.969, 0.980]  # #F5F7FA
SILVER = [0.784, 0.804, 0.839]  # #C8CDD6（開示テキスト）
INK    = [0.039, 0.039, 0.047]  # #0A0A0C 近黒ルート（サムネ bg と一致）
```
> **accent は必ず `#2FA6A0`（EP41 gold #E5B53A / EP42 blue #3B7DD8 / EP43 amber #E0913C を1つも書かない）。** サムネ・OP props・AEカードの accent は全て `#2FA6A0`。

**数値カードは全て `money_keys()` 系で表示文字列を Python 事前計算**（JSX で算術しない＝EP38 確定ルール）。
`VOTE_SPLIT`（v01）は「6」を先に、間を置いて「3」を出し 6-3 の重みを作る（多数=WHITE/SILVER・少数=ACCENT teal）。
**`v01`（6-3）は同一カード内に限定サブ "ONE DOOR CLOSED · EXCLUSION STAYS OPEN" を別レイヤーで出す（C-2/R-VOTE63・9-0/full victory を書かない）。**
**`m01` は左=1966 Miranda・右=2000 Dickerson の SPLIT_COMPARE で「両者存続」を視覚化（C-3・覆滅に見せない）。**

## 7.4 `beats.json` スキーマ（本番 `08_edit/ae_hero/beats.json`・**dryrun 版は作らない**）
`build_young_hero_cards.py` の beats スキーマに準拠。各 beat に `id` / `layout` / `start` / `end` / `dur` /
`still`(象徴 or null) / `hero`(主表示文字列) / `top` / `bottom` / `caption`(**改行禁止・最大50字**) /
`value` / `numKeys` / `blend_mode`(既定 "overlay") / `required` / `out` / `attribution`(**QUOTE_CARD=q01 は必須**・§2 `APPROVED_QUOTES` と一致・R-ATTRIB)。
**`film_offset_sec`**（コンポジタが加算する本編開始オフセット・複製元 young と同じフィールド）をトップに持たせる。
**`value` / `hero` の数値は §2 台帳の `verified:true` 値のみ**（`check_tekoh_facts` が照合）。
**`v01` は "one door closed"/"exclusion stays open"/"reversed"/"remanded" のいずれかを `bottom` か `caption` に持つ（R-VOTE63）。`m01` は "MIRANDA STANDS"/"DICKERSON STANDS"/"still good law" を持つ（R-MIRANDA）。**

## 7.5 このマシン固有の罠（複製元が対処済み。**1つも省くな**）
1. `setTemporalEaseAtKey` の配列次元は **spatial(Position) で 1**（`if(!prop.isSpatial){...}` で分岐）
2. RS = **`"最良設定"`** / OM = **`"H.264 - レンダリング設定を一致 - 15 Mbps"`**（英語名は try/catch フォールバックのみ・ローカライズ名優先）
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
$PY scripts/ae/build_tekoh_hero_cards.py
"C:/Program Files/Adobe/Adobe After Effects 2026/Support Files/AfterFX.exe" -noui \
  -r ".../episodes/PD-2026-044-tekoh/08_edit/ae_hero/tekoh_hero.jsx"
# render/_build_ok.txt を待つ（最大600秒）→ render/*.mp4 が最大8本揃うまで待つ（最大1200秒）
$PY scripts/ae/composite_tekoh_hero.py
```

## 7.9 `scripts/validate_tekoh_beats.py`（BLOCKING）
1. `beats[].start` 昇順・区間非重複
2. 全 `start`/`end` が本編ナレ区間内（HOOK 0–33.0 と ENDCARD 末尾9s に重ねない）
3. `layout` が §7.3 の**実装済み8種**のいずれか。**この8種以外のレイアウト名は FAIL。** still が必要なレイアウトで null なら FAIL・ベクター系(SEAM)で非null なら FAIL
4. `still` 非null は実在＋長辺 >=3840px
5. `hero`/`top`/`bottom`/`caption`/`value` が §2（R-FORBID/R-CHARGE/R-LEDGER/R-ATTRIB/R-VOTE63/R-SCOPE/R-MIRANDA/R-1983/R-PERSON/R-DATE）を通る
6. `verified:false` の値を要求するカードは `required:false` で**除外**、`required:true` なら exit 1（**q01 の逐語が未確定なら required:false**）
7. **`tekoh_film.json` の `figures[]`（§6）と AE の区間が1秒でも重ならない**
8. `caption` に改行が含まれない
9. **AI開示レイヤーの存在（R1）** — ビルダが全カード共通スタックに `AI-assisted visualization`（右下・§7.3）を焼く設定であること（静的確認）。無ければ FAIL
10. **★dochighlight レイアウトが1枚も無い（R-DOCHILITE）**

## 7.10 基底 mp4 とコンポジタ（`build_tekoh_bgm.py` → `composite_tekoh_hero.py`）
```
# 完成後の合成順（ブリーフ§5）: build_tekoh_bgm.py（narration+BGM・REAL 実装版）→ composite_tekoh_hero.py（AEカード焼込み）
BASE = episodes/PD-2026-044-tekoh/08_edit/tekoh_final_bgm.v002.mp4     # build_tekoh_bgm.py が生成
OUT  = episodes/PD-2026-044-tekoh/08_edit/tekoh_final_bgm.v003_ae.mp4  # composite_tekoh_hero.py が生成
FFMPEG  = C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe
FFPROBE = C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffprobe.exe
W,H,FPS = 1920, 1080, 30
```
**`build_tekoh_bgm.py` は `build_young_bgm_real.py`（REAL）の複製。** young の section マップ `ACT_1..ACT_4` を tekoh の `ACT_1..ACT_3` に縮める（§4.2）。ミックス・ダッキングは変えない。
**`composite_tekoh_hero.py` は `beats.json` の `film_offset_sec` を読んで各 beat の start/end に加算する**（複製元 composite_young_hero.py と同じ）。
**SKIP4条件を1行も削らない:** ① `render/<id>.mp4` 不在 ② 解像度 != 1920x1080 ③ 実測尺 `< dur-0.3` ④ `beat.end > base_dur`。
SKIP された区間は元カットのまま残る。**何枚 SKIP したかを stderr に必ず出す。**
ffmpeg は `overlay=0:0:eof_action=pass:enable='between(t,start,end)'`（`blend_mode` が screen/multiply の時のみ `blend`）。
**出力後 `probe_dur(OUT)` でベースとの尺差 <=0.5秒を確認。出荷済みは絶対に上書きしない（必ず `_v003_ae`）。**

---

# 8. 字幕の切断規則（`scripts/gen_captions_tekoh.py`＝`gen_captions_caniglia.py` の複製）

## 8.1 原則
**文字数は「上限」であって「分割基準」ではない。** `gen_captions_caniglia.py` の `internal_split()` / `chunk_sentence()` を**そのままコピー**。
`from fix_caption_dangling import NO_DANGLE_END, wrap as safe_wrap`（**語リストを自前で書き直さない**）。

## 8.2 通すゲート `scripts/check_caption_breaks.py`（**閾値を緩めるの禁止**）
- **A. 行末の機能語**（複数行キューの最終行以外が句読点なしで `NO_DANGLE_END` の語で終わる）= 0件
- **B. 孤立キュー**（語数<3 で「終端句読点で終わる」「大文字で始まる」の両方を満たさない）= 0件
- **C. 句をまたぐ切断(hard)** = 0件
- A/B/C いずれか1件で FAIL（**実質ゼロ許容**）

## 8.3 EP44 の入力と対応
- 入力は **narration_index の各チャンク文**（`--narr`）。**字幕テキストは台本本文と1:1対応**（§0.5-5）。台詞・別エピソード文の混入禁止。verbatim で使い、構文境界で分割するだけ。
- `ABBR` に `U.S.` / `v.` / `Mr.` / `No.` / `U.S.C.` 等を持つ（`Vega v. Tekoh` の `v.`、`597 U.S. 134` の `U.S.`、`42 U.S.C.` の `U.S.C.`、`No. 21-499` の `No.` で文を切らない）。
- タイミングは narration_index の start/end。CPS <=27・最小表示 0.90秒。**Step で決めた境界を時間都合で動かさない。**
- **字幕にも R-FORBID/R-CHARGE 適用**（台本本文に禁止語・罪状語は無いので verbatim なら自然に通る。§2.1 の注意：`stop reading ... rights` / `death of the right to remain silent` を禁止語に足さない）。

## 8.4 セルフテスト（`--selftest`・EP38 実害を回帰に）
台本の代表文で「孤立キュー」を作らないこと、`Vega v. Tekoh` / `597 U.S. 134` / `42 U.S.C. § 1983` / `No. 21-499` で文が切れないこと、
**否定文脈の verbatim（"This is not the death of the right to remain silent" / "it is not permission for police to stop reading anyone their rights"）が `check_tekoh_facts` で false FAIL しないこと**を含め、
**出力を `check_caption_breaks.py` に食わせて exit 0 まで自動確認。**

## 8.5 実行
```bash
$PY scripts/gen_captions_tekoh.py --narr episodes/PD-2026-044-tekoh/06_audio/narration_index.v001.json
$PY scripts/check_caption_breaks.py episodes/PD-2026-044-tekoh/08_edit/captions.final.v001.srt
# → PASS が出るまで直す。ゲート側の閾値を緩めるのは禁止。
```

---

# 9. 5ゲートの実際の判定（**build 後に必ず全部通す・animation_mix を忘れるな**）

| ゲート | 実体 | 入力 | EP44 の通過根拠 |
|---|---|---|---|
| `check_asset_reuse.py <film.json>` | factory≤1 / motion≤2 / still≤2 / first-use≥0.70 | **film.json 位置引数** | §5.2: factory1.00 / motion2.00 / still1.19 / first-use **0.8584** |
| `check_motion_density.py --ep PD-2026-044-tekoh` | film.json の graphics+figures+heroCuts のみ / density≥2.5・coverage≥0.25・variety≥3（**AND**） | **`--ep`** | §6.1: **3.08 / 27.7% / 12+種**（AEカードは0本＝§0.5-2・beats≥31） |
| `check_animation_mix.py --ep PD-2026-044-tekoh` | film.json の cuts を img=still/その他=footage 分類 / still-share≤0.45・motion-cov≥0.45 | **`--ep`** | §5.2[C]: still-share **0.4469(cut)/0.4205(frame)** / motion-cov **0.5531+** |
| `check_caption_breaks.py <srt>` | A/B/C 各0件 | **srt 位置引数** | §8 の構文境界生成器 |
| `check_script_length.py <script> --json` | 総語数 / wpm / narration_seconds | **script 位置引数** | 2,139語 / wpm178.1 / **720.6s** |

> **★ゲートの入力指定（ブリーフ§5）:** density/mix は **`--ep PD-2026-044-tekoh`**。**`--json <film.json>` は出力パスなので入力に使わない。**
> asset_reuse は film.json 位置引数、caption_breaks は srt 位置引数、script_length は script 位置引数。
> **`check_animation_mix` は `04_scenes/premium_beatsheet.v*.json` があればそれを優先する。** §5.6 の通り B の beatsheet は `tekoh_beatsheet`（`premium_` 無し）なので**auto-detect されず film.json を測る。**

---

# 10. OP バンパー `OpeningTekoh`（Remotion・fps60/1920x1080/180f）

## 10.1 二重OPを作らない
本編（`Ep44Tekoh`）の OP は `Bookends.tsx` の `BrandOpening` のまま（`op_ed_bookends` ゲート・フォーク禁止）。
`OpeningTekoh` は**独立したタイトルバンパー成果物**（`out/tekoh_opening.mp4`。Shorts/予告/SNS 用）。**本編に ffmpeg で焼き込まない。**

## 10.2 Composition 設定
| 項目 | 値 |
|---|---|
| `id` | `OpeningTekoh` |
| 解像度 / fps / duration | **1920×1080 / 60 / 180**（=3.0秒） |
| component | `remotion/src/compositions/OpeningTekoh.tsx` |

```tsx
import {OpeningTekoh, openingTekohDurationInFrames} from './compositions/OpeningTekoh';
import tekohOpeningProps from '../props/tekoh.json';
<Composition id="OpeningTekoh" component={OpeningTekoh}
  width={1920} height={1080} fps={60}
  durationInFrames={openingTekohDurationInFrames(60)} defaultProps={tekohOpeningProps}/>
```

**依存:** `@remotion/motion-blur`（未導入時のみ `cd remotion && npm i @remotion/motion-blur`）。
**`remotion/remotion.config.ts`** は既に正典値（png / h264 libx264 / CRF16 / yuv420p / bt709 / aac 320k / 全コア並列 / angle）。**一致確認のみ・書き換えない。**

## 10.3 秒数ベースのタイムライン（fps=60・フレーム直書き禁止・全て `Math.round(fps*秒)`）

| 秒 | 起きること | 手法 |
|---|---|---|
| 0.00–0.40 | L1 グラデ背景 opacity 0→1・**同時に scale 1.08→1.00（`Easing.out(Easing.cubic)`）** | interpolate（opacity 単独禁止・scale と併用） |
| 0.10 | ロゴ（`hasLogo`）左上に spring・scale 0.4→1.0・opacity 0→1 | spring `damping:14,mass:0.9` |
| 0.15–0.25 | L2 グリッド reveal（opacity→0.18）＋ translateY 0→48px | spring `damping:200,mass:1` + `Easing.inOut(Easing.sin)` |
| 0.25 | L3 グロー（interrogation-teal `#2FA6A0`）scale 0.6→1.15 / opacity 0→0.85 | spring `damping:18,mass:1.2`（併用） |
| 0.30–0.86 | L4 主役タイトルが1文字ずつ切れ上がり（translateY 110%→0）＋ opacity。スタッガー **2f/文字**。全体を `Trail(layers=6,lagInFrames=1.2,trailOpacity=0.45)` で包む | spring `damping:16,mass:1` |
| 0.55–1.15 | L2b **署名欄の細い暖色光スリット**（中央から縦に `scaleX 0→1`＋opacity 0→0.5・「警告なしに書かれた線」のモチーフ） | spring `damping:22,mass:1.1`・`transformOrigin:'center'`・**motionBlur** |
| 0.95–1.35 | L5a アクセント下線（teal）左から `scaleX 0→1` | spring `damping:16,mass:0.8`・`transformOrigin:'left center'` |
| 1.10–1.55 | L5b サブタイトル translateY 24→0 + opacity 0→1 | spring `damping:20,mass:1`（併用） |
| 1.55–3.00 | settle→ホールド。**完全静止フレーム無し・フェードアウトしない** | — |

> **等速線形を1箇所も使わない。opacity 単独の演出を1箇所も作らない**（全 opacity が translateY/scale/scaleX と対）。

## 10.4 props 型と値
```ts
export type OpeningTekohProps = { title:string; subtitle:string; accent:string; hasLogo:boolean };
```
`remotion/props/tekoh.json`: `{ "title":"THE WORDS THEY NEVER READ YOU", "subtitle":"VEGA V. TEKOH", "accent":"#2FA6A0", "hasLogo":true }`
`remotion/props/tekoh_short.json`: `{ "title":"NO WARNING CAME", "subtitle":"WHAT THE LAW STILL PROTECTS", "accent":"#2FA6A0", "hasLogo":false }`
> `subtitle`/`title` も §2 の R-FORBID/R-CHARGE/R-PERSON 検査対象（`remotion/props/tekoh*.json`）。ルート背景は INK 近黒 `#0A0A0C`。
> **accent は EP41 gold / EP42 blue / EP43 amber を書かず interrogation-teal `#2FA6A0`（レーン分離）。**
> **「Miranda is dead／権利を読まなくてよい」断定・原被疑事実を subtitle に書かない（C-1/C-5）。**

## 10.5 量産
```bash
cd remotion && npm run studio     # OpeningTekoh を 0→180f スクラブして §10.3 の各時刻を目視
npx remotion render OpeningTekoh out/tekoh_opening.mp4 --props=./props/tekoh.json
npx remotion render OpeningTekoh out/tekoh_short_op.mp4 --props=./props/tekoh_short.json
```

---

# 11. サムネ3案（`TekohThumbnails.tsx`・`<Still>` 1280×720・Root に `Thumb-tekoh-01..03`）

**共通要件:** 見出し全て大文字・4語以内・320pxで判読 / **実在人物の肖像禁止（R1・Tekoh/Vega の顔/身体を出さない・C-6）** / INK 黒 `#0A0A0C` bg + interrogation-teal `#2FA6A0` /
背景は body 静止画のうち `also_thumb==true` の6枚（象徴オブジェのみ・C-5/C-6。**サムネ専用の分類は無い＝also_thumb フラグを読む**） / `thumbnail_visibility`（luma平均≥33＋コントラスト）を通す。目標CTR 6%+。3案は6枚から選ぶ。
**原被疑事実（EN/JP）・「Miranda is dead」断定・9-0 を出さない（R-FORBID/R-CHARGE/R-VOTE63）。**

**★also_thumb 6枚（still 資産 ID 空間 S01..S85＝CODEX_A §5.9。A のマニフェストと**一字一致必須**の A↔B 契約点。CODEX_A §4.3 と同一6 asset ID に `also_thumb:true`）:**
`S02`（ランプ下のペンと書面＝物語の中心）/ `S04`（空の取調台・録音機なし・警告が来なかった部屋）/ `S24`（12席の空の陪審席）/ `S44`（9席のベンチが影で大小に分割＝分かれた判断）/ `S45`（守りの柵＝prophylactic）/ `S85`（縁に冷光の細線が走る閉じたドア＝最後の残像）。
> サムネ component は**マニフェストの `also_thumb` フラグを読んで**背景を選ぶ（scene id をハードコードしない）。**この6 ID は CODEX_A §4.3・§13 の also_thumb と完全一致**（`check_tekoh_asset_manifest` §3.3-14 が集合一致を検査）。

- **T1「6–3」（数字勝負・最推奨）:** S44 の 9席分割ベンチを暗く落とし、前面に **`6–3`**（大）＋ **`ONE DOOR CLOSED`**（下・**C-2 の限定併記必須**）。数字は F03 の検証済み値のみ。`ONE` を teal。
- **T2「守りの柵」（教義）:** S45 の守りの柵。文字 **`A FENCE, NOT THE GROUND`**（→4語超なので **`A FENCE — NOT A RIGHT`**（4語）に短縮）。`FENCE` を teal。prophylactic のモチーフ（C-1）。
- **T3「警告なしの署名」（尊厳）:** S02 のペンと署名欄。文字 **`THEY NEVER READ IT`**（4語・原被疑事実を出さない）。`NEVER` を teal。閉じた §1983 の扉と開いた排除の扉のモチーフ（C-1）。

**A/Bタイトル候補（`09_package`・60字以内・二人称・ブリーフのとおり・原被疑事実を出さない）:**
- **A:** `If Police Skip Your Rights, Can You Sue the Officer? The Court Said No.`
- **B:** `They Used the Statement You Wrote With No Warning. You Can't Sue.`
> ※「ミランダ廃止／黙秘権消滅／警察は権利を読まなくてよくなった」系のタイトルは**禁止**（C-1/R-SCOPE）。**罪状の性質を1語も出さない（C-5/R-CHARGE）。**

**固定コメント** `09_package/pinned_comment.v001.txt`（§2 の R-LEDGER/R-ATTRIB/R-FORBID/R-CHARGE/R-VOTE63/R-SCOPE/R-MIRANDA 検査対象。台帳事実のみ）:
```
Two things this case actually decided — and two it did not.

DECIDED: For the failure to give Miranda warnings, standing alone, you cannot sue the
officer for civil money damages under Section 1983 (42 U.S.C. 1983). The Court split
6-3, with Justice Alito writing for six and Justice Kagan in dissent, joined by Justices
Breyer and Sotomayor.

LEFT OPEN: Miranda still stands, and so does Dickerson (2000). If police question you
today without the warning, your unwarned words can still be kept out of your criminal
trial. What closed was one door — the civil-damages suit against the officer for a
warning skipped — and only that one.

A jury heard the full case against the man at the center of this story and refused to
convict him; he is a private person who was accused and then cleared, and nothing here
describes what he was accused of. A right and a remedy are not the same thing.
```

---

# 12. 本編コンポジション登録（`remotion/src/Root.tsx`・`Ep43Caniglia`/`Ep42Young` の形を踏襲）
```tsx
import tekohFilm from './data/tekoh_film.json';
<Composition id="Ep44Tekoh" component={CaseFilm}
  durationInFrames={caseFilmDurationInFrames(tekohFilm as unknown as FilmData, BRAND.video.fps)}
  fps={BRAND.video.fps} width={BRAND.video.width} height={BRAND.video.height}
  defaultProps={{ data: tekohFilm as unknown as FilmData, seriesLabel: 'PRIME DOCUMENTARY',
    title: 'If Police Skip Your Rights, Can You Sue the Officer? The Court Said No.',
    subtitle: 'One door closed — the civil-damages suit for a skipped warning. Miranda still stands, and your unwarned words can still be kept out of your trial.' }}/>
```
> **id は正確に `Ep44Tekoh`（切り詰め・綴り違い・大文字化の誤記に注意）。** `remotion/src` に現在 `tekoh` の文字列が無いこと（衝突しない）を確認してから追記。
> `durationInFrames` は **`caseFilmDurationInFrames(tekohFilm, fps)`（4項関数・§5.1.1）**。`title`/`subtitle` も §2 検査対象（R-FORBID/R-CHARGE/R-VOTE63/R-SCOPE）。**「Miranda is dead」「full victory」断定・原被疑事実を書かない。**

---

# 13. 受入（自分で exit 0 を確認してから完了報告）
```bash
cd C:\Users\aab15\Documents\prime-documentary ; PY=./.venv/Scripts/python.exe

# 0. 語数（最優先・課金前に落とす）
$PY scripts/check_script_length.py episodes/_planning/EP44_tekoh_script.en.v001.md --json   # 2,139語 / wpm178.1 / 720.6s

# 1. 事実性/6制約（EP44固有・正確性ゲートはこの1本・dochighlight=0 も検査）
$PY scripts/check_tekoh_facts.py --json

# 2. 契約バリデータ
$PY scripts/validate_tekoh_beats.py
$PY scripts/check_tekoh_asset_manifest.py --assets episodes/PD-2026-044-tekoh/05_visuals/asset_manifest.v001.json

# 3. ★5ゲート（animation_mix を忘れるな・入力は --ep / 位置引数を厳守）
$PY scripts/check_asset_reuse.py    remotion/src/data/tekoh_film.json
$PY scripts/check_motion_density.py --ep PD-2026-044-tekoh
$PY scripts/check_animation_mix.py  --ep PD-2026-044-tekoh
$PY scripts/check_caption_breaks.py episodes/PD-2026-044-tekoh/08_edit/captions.final.v001.srt

# 4. 水増し・レンダ前プリフライト
$PY scripts/check_padding.py --ep PD-2026-044-tekoh --json
$PY scripts/preflight_render_gate.py --ep PD-2026-044-tekoh

# 5. 本編レンダ（slim public・並列4）→ BGM → AEカード合成
cd remotion
npx remotion render Ep44Tekoh out/tekoh.mp4 --public-dir=public_slim --concurrency=4
#   public_slim は tekoh_film.json が参照する素材（+ 各 <stem>_depth.png）だけを含む slim public。
#   無ければ referenced paths を public_slim/ にコピーして作る（remotion/public/tekoh 本体を痩せさせない）。
cd ..
$PY scripts/build_tekoh_bgm.py
$PY scripts/ae/composite_tekoh_hero.py

# 6. 本編最終受入（episode番号は★位置引数・--ep ではない）
$PY scripts/check_final_acceptance.py 44 \
  --render episodes/PD-2026-044-tekoh/08_edit/tekoh_final_bgm.v003_ae.mp4 --emit-receipt
```

| ゲート | EP44 目標値 |
|---|---|
| `check_script_length` | 総語数 **2,139** / `wpm 178.1` / narration **720.6s** |
| `check_asset_reuse` | factory≤1 / motion≤2 / still≤2 / first-use **0.8584**（floor0.70） |
| `check_motion_density` | density **3.08**/min / coverage **27.7%** / variety 12+（floors 2.5 / 0.25 / 3・beats **≥31**） |
| `check_animation_mix` | still-share **0.4469(cut)/0.4205(frame)**（cap0.45）/ motion-cov **0.5531+**（floor0.45） |
| `check_caption_breaks` | 行末機能語0 / 孤立キュー0 / hard split 0 |
| `check_tekoh_facts` | violations = 0（台帳照合・6-3限定・Kagan帰属・6制約・R-CHARGE〈EN/JP〉・R-VOTE63・R-SCOPE・R-MIRANDA・R-1983・**R-DOCHILITE**） |
| runtime band | 11.5–12.5分（narration 720.6s + bookends・total≤750s／733.1s） |
| factory クリップ | ≥24本 → **93本** |
| image_resolution | 全静止画 長辺 ≥3840px |
| thumbnail | 3案 @1280×720 + selected luma≥33 |
| op_ed_bookends | `BrandOpening`/`BrandEndcard` を import（フォーク禁止） |

**全て exit 0 でなければ `package_ready` にしない。自己申告QCは無効。QC基準を書き換えて通すのは禁止。**

## 13.1 完成後の全編アイボール（**1フレーム判定禁止＝EP39-41 実害**）
`tekoh_final_bgm.v003_ae.mp4` を **0→末尾まで通しで実視聴**（サンプル ~30秒ごと）し、以下を確認してから完了報告:
- 紙芝居感が無い（still が連続していない・footage が体感で過半）
- AEカード（最大8枚）が全て焼き込まれ数値が台帳と一致（「Miranda is dead」「full victory」「9-0」がどこにも無い）
- **6-3 のカード v01 に "ONE DOOR CLOSED · EXCLUSION STAYS OPEN" が読める（C-2・9-0/full victory はどこにも無い）**
- **m01 が「MIRANDA STANDS / DICKERSON STANDS」で両者存続を示し、Vega が Miranda を覆したように描いていない（C-3・R-MIRANDA）**
- **s01 の §1983 に "no immunity" が無い（C-4・R-1983）。f01 が「a fence, not the ground」で prophylactic を示す（C-1）**
- **ENDING/どこかに「排除の扉は開いたまま（EXCLUSION STAYS OPEN）」が読める（C-1・R-SCOPE）**
- Kagan 逐語が Kagan 帰属（要約を引用符に入れていない・逐語未確定なら q01 が出ていない・R-ATTRIB）
- **★原被疑事実（疑われた罪の性質・被害・victim・guilty）が英語でも日本語でも画面・字幕・概要欄のどこにも無い（C-5・R-CHARGE）**
- Terence Tekoh / Carlos Vega の顔・身体・肖像が無い（象徴＝病院の廊下/ペンと署名欄/空の取調台/空の陪審席/列柱/守りの柵/閉じた扉・開いた扉のみ・C-6）
- **★`dochighlight` の黒バー/box/underline がどのカット・カードにも出ない（R-DOCHILITE・grep 0 と目視の両方）**
- 生成ビジュアル表示中は `AI-assisted visualization` が右下に常時（**AEカード表示中も**開示が見える＝カード共通スタックに焼かれている・R1・§7.3/§7.9）
- accent が interrogation-teal `#2FA6A0`（EP41 gold / EP42 blue / EP43 amber が紛れていない）
- テキストの切れ（末尾クリップ）が無い・実写が本物（near-still でない）・音ズレ・字幕ズレ・尺差（base と <=0.5s）が無い

---

# 14. 絶対にやらないこと
- **EP39 / EP40 / EP41 / EP42 / EP43 のファイル・素材に触らない**（読み取りのみ可）。レーンを分離する。
- **スレッドAの所有ファイル（§0.2.1）に書かない**（`05_visuals/` `05_stock/` `remotion/public/tekoh/` `H:\...\ai\tekoh\` `04_scenes/ai_prompts.v001.md`）。**B の provenance は `04_scenes/tekoh_build_manifest.v001.json` に書く。**
- **設計ブリーフ / `EP44_tekoh_CODEX_A_*` / PD-2026-039〜043 に触らない。**
- **★stub / dryrun のコードパスを作らない**（EP44 は実素材のみ・§0.1）。`make_*_stub_assets` / `make_*_stub_narration` / `asset_manifest.stub.*` / `_dryrun/` を作らない。
- **課金ジョブを起動しない**（ElevenLabs TTS / 課金画像生成API / YouTube アップロード）。narration_index は実測を消費（Bは TTS を起動しない）。
- **公開済み・出荷済み mp4 を上書き・再レンダしない**（出力は必ず `_v003_ae`）。
- **台帳（§2）に無い数値を焼かない**（$580,000 の再発防止）。不明値・未確定逐語は `verified:false` でカード除外（q01 は required:false）。
- **`FigureSpec` の `kind` を推測で書かない**（§6.2 の実在小文字値のみ。大文字名は無言で消える。`comparebars` は非在→`compbars`）。**★`dochighlight` を figures/beats に1本も作らない（R-DOCHILITE）。**
- **`--variants` という語を書かない**（1シーン1枚・バリエーション0＝ブリーフ§1。SDXL は A の領分で 1 固定）。
- **asset_manifest の `counts`/`role` enum/`overlay` 枚数/`also_thumb` 集合を CODEX_A と食い違わせない**（`role` は `body`/`i2v_source`/`reject` の3値のみ・**`thumb`/`still_thumb` を作らない**・overlay=12・also_thumb=`{S02,S04,S24,S44,S45,S85}`）。
- **「Miranda is dead／権利を読まなくてよい」「full victory」を断定しない**（C-1/C-2・R-SCOPE/R-VOTE63）。**「9-0／全会一致」を書かない**（C-2）。**Vega が Miranda/Dickerson を覆したと書かない**（C-3・R-MIRANDA）。**§1983一般で「no immunity」と断定しない**（C-4・R-1983）。**★原被疑事実（疑われた罪の性質・被害・victim・guilty・性的暴行/性犯罪/わいせつ 等 EN/JP）を一切出さない**（C-5・R-CHARGE）。**Tekoh/Vega の顔/肖像/身体を出さない**（C-6・R-PERSON）。
- **accent に EP41 gold / EP42 blue / EP43 amber を使わない**（interrogation-teal `#2FA6A0` のみ）。
- **スペック数値（226 cuts / still85 / factory93 / motion16 / distinct194 / first-use0.8584 / still-share0.4469 / figures≥31 / 720.6s / 2,139語 / 48シーン / mean_shot3.19 / total≤750s）を変えない。**
- **実在しないスクリプト名を書かない**（新規は §0.3 の一覧のみ・複製元を明記）。**composition id は `Ep44Tekoh`（切り詰め・綴り違い注意）。** **PowerShell 経由で正規表現/エスケープを生成しない**（`\b` バックスペース化の実害）。
