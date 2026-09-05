# EP50 centralpark — Codex スレッドB「実装 + レンダ」引き継ぎプロンプト v001

> **このファイルは単体で完結している。他のファイルを読まなくても着手できる。**
> これはチャンネル初の **60分尺（long-form）** 作品 *The Exonerated Five（Central Park Five）* の BUILD/RENDER 実行プロンプト。
> 設計 `EP50_centralpark_DESIGN_and_CODEX_PROMPTS.v001.md` / `EP50_centralpark_DESIGN_ARCHITECTURE.v001.md` の **§6 CODEX_B ブリーフを本書に全展開済み**（読み直し不要・数値は転記済）。
> スレッドA（素材生成）の `EP50_centralpark_CODEX_A_*.md` は**読まない**（Aは FROZEN・接続点は §3 のマニフェスト1ファイル）。
> `EP50_centralpark_PRODUCTION_SPEC.v001.json` の数値は本書に転記済み。**あなたはこれを書き換えない**（★ただし durationInFrames/narrationSeconds は **実測 TTS 後に SPEC と Root を更新**する＝§5.1.1）。

```
あなたは Prime Documentary（YouTubeドキュメンタリーチャンネル）の制作エンジニアです。
リポジトリ: C:\Users\aab15\Documents\prime-documentary
Python:     C:\Users\aab15\Documents\prime-documentary\.venv\Scripts\python.exe
メディア:   H:\pd-media
担当:       EP50 / Episode ID: PD-2026-050-centralpark / slug: centralpark
Composition id（本編）: Ep50Centralpark
フォーマット: long_form_60min（チャンネル初の60分尺・~108,795フレーム・レンダは数時間＝想定内・許可済）
```

**題材:** 1989年の Central Park jogger 事件で、5人の黒人・ラテン系の**少年（14〜16歳）**——Antron McCray, Kevin Richardson, Yusef Salaam, Raymond Santana, Korey Wise——が**強要された虚偽自白**により 1990年に不当有罪となり、数年間服役。2002年、**Matias Reyes** が単独犯だと自白し **DNA が彼一人に一致**、全員の有罪が **2002-12-19（Tejada 判事）に取消（vacated）**、2014年に約$41M・2016年に約$3.9M で和解。彼らは **The Exonerated Five（無罪が確定した5人）**。
本作の主題は「**部屋、約束、そしてカメラの止まった数時間**」——**少年に対する取調べと虚偽自白の科学、冤罪、そして名誉回復**。事件（暴行）は主題ではなく context。**暴行は臨床的・非描写的にのみ扱う**。

> **★正確性7制約が全出力を律する（§2・`check_centralpark_facts.py`）。**
> **R-INNOCENCE**（5人が事件に関与したと**匂わせない**・DNA は Reyes 単独・全有罪取消／Armstrong 報告は**却下された反対説としてのみ**）・
> **R-VICTIM**（被害者 Trisha Meili は存命の生存者＝尊厳・描写や記録以上の naming をしない）・
> **R-REYES**（Reyes は established facts のみ・扇情的詳細禁止）・
> **R-NUM**（hedged 数値は断定で焼かない）・
> **R-FACE（owner 改定）**（**匿名・非識別の人物は可**＝ドラマ化スタンドイン／**実在人物の likeness は不可**＝5人・Meili・Reyes・Trump・実在の刑事/判事/検事を似せない・被害者の描写と暴行 imagery は一切なし）・
> **R-DOCHL**（`dochighlight` を1件も使わない＝黒バー/box/underline がバグに見える・3回指摘済）・
> **R-QUOTE**（検証済み逐語＋帰属のみ・**発明した引用を1件も出さない**）。

---

# 0. このスレッドの責務・境界・完了条件

## 0.1 このスレッド（B）の責務 — **コード律速。実装は全部書ける。**

| # | 作業 | 成果物 |
|---|---|---|
| B-1 | エピソードディレクトリと `manifest.json` | `episodes/PD-2026-050-centralpark/**` |
| B-2 | マニフェスト**消費側**バリデータ | `scripts/check_centralpark_asset_manifest.py`（**`check_cleveland_asset_manifest.py` を複製**） |
| B-3 | 事実台帳 CP-ID と 7制約ゲート（**EP50固有・BLOCKING**） | `scripts/check_centralpark_facts.py`（**`check_cleveland_facts.py` を複製**） |
| B-4 | `centralpark_film.json` ビルダ（**manifest→1,160 cuts＋165 figures＋captions／実素材のみ**） | `scripts/build_centralpark_film.py`（**`build_cleveland_film.py` を複製**） |
| B-5 | beats バリデータ（AE 36 moments ↔ figures 165 の区間衝突／年 group:false／layout allowlist） | `scripts/validate_centralpark_beats.py`（**`validate_cleveland_beats.py` を複製**） |
| B-6 | **AE layout allowlist ゲート**（新規・{6 proven}∪{dryrun済 Tier-B} のみ許可） | `scripts/check_AE_layouts.py`（**新規作成**・§7.7） |
| B-7 | 構文境界字幕生成器（実測 narration_index から verbatim） | `scripts/gen_captions_centralpark.py`（**`gen_captions_cleveland.py` を複製**） |
| B-8 | **After Effects カード**のビルダ（**★2-tier・6種を残し8新 layout を ADD**）とコンポジタ | `scripts/ae/build_centralpark_hero_cards.py`（**`build_cleveland_hero_cards.py` を複製→EXTEND**）/ `scripts/ae/composite_centralpark_hero.py`（**`composite_caniglia_hero.py` を複製**） |
| B-9 | 本編 BGM ミックス（AEカード合成の基底 mp4 を生成・**VO OFF=11.5**） | `scripts/build_centralpark_bgm_real.py`（**`build_caniglia_bgm_real.py` を複製・OFF=11.5**） |
| B-10 | 本編 Remotion コンポジション登録 `Ep50Centralpark` | `remotion/src/Root.tsx` |
| B-11 | OP バンパー `OpeningCentralpark`（fps60/1920x1080/180f） | `remotion/src/compositions/OpeningCentralpark.tsx` |
| B-12 | サムネ3案 | `remotion/src/compositions/CentralparkThumbnails.tsx` |
| B-13 | 本編レンダ→BGM→AEカード合成→全ゲート→**全編アイボール3回（FULL 60分）** | `episodes/PD-2026-050-centralpark/08_edit/**` |

> **★このスレッドは「実素材のみ」。stub/dryrun/placeholder のコードパスを作らない**（`grep -riE 'stub|placeholder' scripts/*centralpark*.py` が 0）。ただし **AE Tier-B の `--dryrun` 単体レンダは正規の実装検証手順**（§7.5）＝これは placeholder ではなく「実装した新 layout を1コンプずつ証明する」工程。
> **★clone 元は実在ファイルのみ**（`ls scripts/` で確認済）。**`check_strieff_facts.py` 等 EP49 系のスクリプトは未生成（EP49 の build がまだ走っていない）＝複製元にしない。EP50 は全て `*cleveland*` / `*caniglia*` の実在監査済ファイルを複製元にする**（§0.3）。

## 0.2 もう一方のスレッド（A・FROZEN）との境界 — **接続点はただ1ファイル。**

```
episodes/PD-2026-050-centralpark/05_visuals/asset_manifest.v001.json
   ↑ Aが生成（唯一の生産者・FROZEN）        ↓ Bが消費（唯一の消費者・検証者）
```

**Bはこのファイル以外のAの中間生成物を読まない。** counts / role enum / overlay枚数 / also_thumb 集合は A(producer)↔B(consumer) で**1バイト単位で共有**（§3）。

### 0.2.1 ファイル所有権（これを破ると並行作業が壊れる）

| パス | 所有 | Bの権限 |
|---|---|---|
| `episodes/PD-2026-050-centralpark/{manifest.json,00_topic,01_research,03_script,04_scenes,06_audio,08_edit,09_package,approvals,events}/**` | **B** | 読み書き |
| `remotion/src/**` `remotion/props/**` | **B** | 読み書き |
| `scripts/*centralpark*.py` / `scripts/ae/*centralpark*.py` / `scripts/check_AE_layouts.py` | **B** | 新規作成 |
| **`episodes/PD-2026-050-centralpark/05_visuals/**` `05_stock/**`** | **A** | **読み取りのみ。書くな** |
| **`H:\pd-media\assets\ai\centralpark\**` / `ai_video\centralpark\**`** | **A** | **読み取りのみ。書くな** |
| **`remotion/public/centralpark/{img,factory,motion,overlay,audio}/**`** | **A** | **読み取りのみ。書くな**（B の `public_slim` staging は §12 で B が作る） |
| `EP50_centralpark_DESIGN*.md` / `EP50_centralpark_CODEX_A_*.md` / `..._facts.v001.json` / `..._script.en.v001.md` / `..._PRODUCTION_SPEC.v001.json` | **設計/上流** | **読み取りのみ。書くな**（★SPEC の durationInFrames は実測後に B が更新可＝§5.1.1 の唯一の例外） |
| `episodes/PD-2026-0{01..49}-*/**` / それらの素材 / `scripts/*{他slug}*.py` | **他エージェント** | **絶対に触るな（読み取り可）。レーンを分離する** |

## 0.3 B が新規作成するスクリプト（これ以外を新規に作らない。既存を改変しない）

| パス | 役割 | 手本（**改変せず読んで複製→パス/定数だけ差し替え**・実在確認済み） |
|---|---|---|
| `scripts/check_centralpark_asset_manifest.py` | §3.3 消費側バリデータ | `scripts/check_cleveland_asset_manifest.py` |
| `scripts/check_centralpark_facts.py` | §2 7制約＋台帳（BLOCKING・正確性ゲート名はこの1つに統一） | **`scripts/check_cleveland_facts.py`** |
| `scripts/build_centralpark_film.py` | §5 film.json＋provenance＋beatsheet＋SRT（実素材・**factory/motion 全読込**・**年 group:false**） | **`scripts/build_cleveland_film.py`** |
| `scripts/validate_centralpark_beats.py` | §7.6 不変条件（AE↔figures／layout allowlist／年 group:false） | **`scripts/validate_cleveland_beats.py`** |
| `scripts/check_AE_layouts.py` | §7.7 AE layout allowlist ゲート（**新規**・複製元なし・小さな独立ゲート） | **新規作成**（既存 `check_year_grouping.py` の CLI/exit 規約を手本にする） |
| `scripts/gen_captions_centralpark.py` | §8 構文境界字幕生成器 | **`scripts/gen_captions_cleveland.py`** |
| `scripts/ae/build_centralpark_hero_cards.py` | §7 AEカードビルダ（**cleveland を複製→6種を残し8新 layout を ADD**） | **`scripts/ae/build_cleveland_hero_cards.py`** |
| `scripts/ae/composite_centralpark_hero.py` | §7.9 コンポジタ（`beats.json` の `film_offset_sec` を読む） | **`scripts/ae/composite_caniglia_hero.py`** |
| `scripts/build_centralpark_bgm_real.py` | §7.9 基底 mp4（narration＋BGM ミックス・**OFF=11.5**） | **`scripts/build_caniglia_bgm_real.py`** |

> **`build_centralpark_film.py` 複製時に差し替える定数:** `SLUG="centralpark"`・`EP="PD-2026-050-centralpark"`・`DEFAULT_OUT=remotion/src/data/centralpark_film.json`・`PUB_FILM=remotion/public/centralpark/film_data.v001.json`・出力パス群・`expected={"still":505,"factory":485,"motion":170}`（**distinct: still430/factory485/motion85**）。**ロジック（`public_items()`/`repeated()`/`take()`/`allocate`/`build_figures`/`build_captions`）は1行も変えない。**
> **既存の `*cleveland*` / `*caniglia*` を触らない**（他エピソードが使用中）。EP50用に**新規コピー**する。

## 0.4 完了条件（実素材で、全て緑になったら「実装完了」）— コマンドは §10・§13 に集約。要旨:
1. マニフェスト消費側バリデータが A の FROZEN 本番マニフェスト相手に PASS（§3.3）
2. 字幕を実測 narration から構文境界で生成し `check_caption_breaks` / `check_caption_integrity` PASS（§8）
3. film.json を実マニフェストから組む（footage 混在・**factory485/motion85 全読込**・dochighlight 0・**年 group:false**・§5）
4. **全ゲート PASS**（§10・script_length は **LONGFORM cap ≈10,900**・animation_mix を忘れるな・**check_year_grouping**・**check_AE_layouts**・**check_centralpark_facts**）
5. AE 36 moments（Tier A 24 + Tier B 12）をビルド（**Tier-B は実装→dryrun→allowlist→本番の順**）→ 二段 aerender → composite（§7）
6. 本編レンダ（`--public-dir=public_slim --concurrency=4`・**数時間・想定内**）→ BGM → AE合成 → `check_final_acceptance 50`（§10）
7. **完成 mp4 を 0→末尾まで FULL 60分・3周アイボール**（§13.1・1フレーム判定禁止）

**台本は既に確定済み**（`EP50_centralpark_script.en.v001.md`・**10,715語・LOCKED・3チェック済**）。本番配置先 `episodes/PD-2026-050-centralpark/03_script/script.en.v001.md`（**1バイトも変えずコピー**・整形禁止＝AI臭再発と語数ゲート再計算を招く）。

---

# 0.5 ★★★ EP38–49 で踏んだ失敗＝最初から防ぐ（本書はこの7点を構造で潰す）★★★

1. **紙芝居（★EP45 の直接死因）** — 静止画100%で組むと `check_animation_mix` が FAIL。**EP45 は build が manifest の `factory[]`/`motion[]` を空で受け取り footage 0本で紙芝居化した。**
   → **`build_centralpark_film.py` は `public_items(manifest,"factory")` が 485本・`public_items(manifest,"motion")` が 85本を返すことを起動時に assert し、0本 or 期待数不一致なら exit 1 で A に差し戻す。** cuts に factory485 + motion170 の footage を最初から入れ still-share を cut数ベース **0.4353**（cap 0.45）に収める（§5.2）。
2. **AEカードは密度に数えられない** — `check_motion_density` は film.json の `graphics+figures+heroCuts` **のみ**数える。**AE 36 moments は ffmpeg 後合成なので1本も数えられない**。→ §6 で **`figures[]` を 165本**（floor 151 に +14・`graphics[]=[]`）置く。AE は別勘定。
3. **FigureSpec の `kind` は実在の小文字値のみ** — 大文字名（`ActTitle`/`QuoteCard`…）は無言で描画が消える。**★`dochighlight` は union に在るが1本も使わない**（R-DOCHL・3回指摘）。**`comparebars`→`compbars`／`VoteTally`→`votetally`。**（§6.2）
4. **台帳に無い数値を焼くな** — EP40 の架空 $580,000 の実害。→ §2 の CP-ID 台帳に**検証済み値だけ**を置き、`check_centralpark_facts.py` が film.json/AE/サムネ/props の全数値を台帳照合。hedged（CP13/17/19/22/28/31/35）は断定表示で FAIL。
5. **★YEAR のコンマ群化バグ（EP46/EP47 の実害＝"2,001"/"1,985"）** — Remotion `NumberTicker`/`FigureBeats` は既定で thousands-comma 群化し、年を "1,989" と描画した。**`group` opt が追加済（EP46 以降・`FigureBeats.tsx` の numberticker union に `group?:boolean` 実在）。** → **YEAR を出す全 figure/AE numeric（1989/1990/1991/2002/2014/2016/2023 等）に `group:false` を必ず set。** 桁区切りが正しい数値（6,000,000,000／$41,000,000）は既定 `group:true`。**`check_year_grouping.py` が enforce**（§9）。
6. **字幕は台本本文と対応** — EP38 の台詞混入・「final」誤称の実害。→ §8 の字幕は narration_index の実チャンク文を verbatim。
7. **★phantom-layout crash（EP48/49 の burned lesson）** — 複製元 JSX は末尾 `else throw "unsupported layout"`。**存在しない layout を beats が参照するとビルドがクラッシュする。`DATE_STAMP` と `SEAM_TRANSITION` は複製元に非実装＝BANNED**（日付カードは `CENTER_STACK`）。EP50 は Tier-B で **8個の新 layout を「実装 → 個別 `--dryrun` 単体レンダ通過 → `check_AE_layouts` allowlist 追加 → 本番デッキで参照」の順**で扱う（§7.5）。**存在しないものを参照せず、実装して証明してから参照する。**

---

# 1. 実装前に必ず読むファイル（**推測で書くな**）

| パス | なぜ読むか |
|---|---|
| `scripts/build_cleveland_film.py` | **複製元。** `public_items()`/`repeated()`/`take()`/`allocate`/`build_figures`/`build_captions` を踏襲し定数だけ centralpark に。**★`public_items(manifest,"factory")`(485)・`public_items(manifest,"motion")`(85) を必ず読む**（EP45 空配列＝紙芝居事故防止） |
| `scripts/ae/build_cleveland_hero_cards.py` | **複製元（FIXED版）。** `fit_size()`／`count_keys()`／DECK 構造／**REPO path 出力（H: に書かない）**／**JSXが.aep保存→呼び出し側が .aep mtime>.jsx を assert してから aerender（二段）**／実装済み6 layout（`buildActTitle`/`buildCenter`(CENTER_STACK+MONEY_STACK)/`buildQuote`/`buildVote`/`buildCompare`）／`else throw "unsupported layout"`／完了マーカー `render/_build_ok.txt` をそのまま。**ここに Tier-B の 8新 layout dispatch と builder を ADD する（§7.4）** |
| `scripts/ae/composite_caniglia_hero.py` | **複製元。** SKIP4条件（missing/解像度不一致/実測尺不足/window past end）と ffmpeg フィルタグラフ（overlay/blend）と `film_offset_sec` 読み込みをそのまま |
| `scripts/gen_captions_cleveland.py` | **複製元。** `internal_split()`/`chunk_sentence()`/`NO_DANGLE_END` import をそのまま |
| `scripts/build_caniglia_bgm_real.py` | **複製元。** narration＋BGM ミックスで基底 mp4（**OFF=11.5 に差し替え**） |
| `scripts/check_cleveland_facts.py` | **複製元（正確性ゲート）。** 構造除外（`asset_manifest` を R-NUM から除外・geometry/index キー除外・`kind!="acttitle"` 条件）を**そのまま流用**（§2.3） |
| `scripts/check_year_grouping.py` | **既存ゲート（実在）。** 年 figure の `group:false` を検査するロジックと CLI/exit 規約（新規 `check_AE_layouts.py` の手本にもする）（§9） |
| `remotion/src/components/CaseFilm.tsx` | `FilmData` 型 / `caseFilmDurationInFrames`（4項・§5.1.1）/ `depthSrcOf()` |
| `remotion/src/components/FigureBeats.tsx` | `FigureSpec` の**実在 `kind`**（§6.2・全小文字・**`dochighlight` は union に在るが使わない**）。**★`numberticker` は `{value; label?; prefix?; suffix?; decimals?; topLabel?; group?}`＝`group?:boolean` が実在（年 group:false の受け皿）／`votetally` は `{majority; dissent; label?}`／`compbars` は `items[]`／`timeline` は `events[]`／`bar` は `data?[]｜items?[]`／`routemap`/`pindropmap` は `pins[]`／`kinetic` は `lines[]`／`mechanism` は `{mechanism:'closingdoor'｜'gears'｜'faultsplit'}`（discriminant は `kind`）** |
| `remotion/src/components/Bookends.tsx` | `OPENING_SEC=3.5` / `ENDCARD_SEC=9` / `BrandOpening` / `BrandEndcard` |
| `scripts/check_asset_reuse.py` / `check_motion_density.py` / `check_animation_mix.py` / `check_caption_breaks.py` / `check_caption_integrity.py` / `check_script_length.py` / `check_visual_asset_qc.py` / `preflight_render_gate.py` / `check_final_acceptance.py` | 通すべきゲートの**実際の判定ロジック**（§10） |
| `C:\Users\aab15\Documents\pino-channel\remotion\src\Opening.tsx` | §11 の OP 正典実装 |

---

# 2. ★ EP50固有の正確性7制約・事実性ロック（`scripts/check_centralpark_facts.py`・BLOCKING）

> **この節に違反した成果物は、他が全て完璧でも出荷不可。** 検査対象は `centralpark_film.json` の figures/captions、AE beats、サムネ、props、固定コメント、`03_script/script.en.v001.md`、`09_package/*`、（存在すれば）マニフェストの tags/caption_hint/qc.notes の**全文字列と全数値**。
> **正確性ゲートはこの1本に統一（`check_centralpark_facts.py`）。** 出力 `09_package/facts_lock.v001.json`。**`pass:true` でない限り `check_final_acceptance.py` に進んではならない。** 対象ファイル未生成はスキップして必ず `skipped[]` にログ（「無いから通した」を黙るな）。

## 2.1 正確性7制約（全出力に適用・違反は BLOCKER）

| # | 制約 | 許可 | 禁止 |
|---|---|---|---|
| **R-INNOCENCE** | **5人の無実。関与を匂わせない** | 「coerced false confessions」「wrongfully convicted」「DNA matched Matias Reyes alone」「he acted alone」「all convictions vacated」「the Exonerated Five」。Armstrong は**却下された反対説としてのみ**（"a police panel questioned … but the DA and the courts rejected that view") | 5人が事件に関与した/実行したと**断定または示唆**する任意の表現／Armstrong を「5人がまだ有罪かもしれない証拠」として提示／「the five attacked」「they were there」「possibly guilty」 |
| **R-VICTIM** | **被害者 Trisha Meili＝存命の生存者・尊厳・記録以上に naming/描写しない** | 「the jogger」「Trisha Meili」（平叙）／「she was attacked and left for dead」「she survived but could not remember」（臨床・CP03/CP04 上限） | 負傷の詳細・再現・扇情語／被害者の imagery・肖像／記録以上の個人情報 |
| **R-REYES** | **Reyes＝established facts のみ** | 「a convicted serial rapist and murderer」「DNA matched him」「he confessed he acted alone」「sentenced 33⅓ years to life」／CP22 は "believed to have raped … two days before"（hedged） | Lourdes Gonzalez 殺害の**正確な月**の断定／記録外の犯行詳細／扇情的描写 |
| **R-NUM** | **数値は台帳一致・hedged は断定禁止** | §2.2 の allowed set のみ。hedged 値は `~`/`roughly`/`reportedly`/`at least`/`about` を伴う | 台帳外の年/件数/金額／`~$85,000`（CP13）・`~$3.9M`（CP31）・`~13 yrs`（CP19）・`~$41M`（CP30）を **hedge 語なしで断定表示**／"30 hours"（累計取調べ時間の断定・firm は "at least seven hours"） |
| **R-FACE（owner 改定・R2）** | **匿名・非識別の人物は可／実在人物の likeness は不可** | 匿名の一般人（実在の誰にも似せない・顔は背向き/影/ソフトで非識別）＝§CODEX_A 5.11 の H シリーズ人物ビート／5つの descending silhouettes（子供）・手・背中・うなじ・コート・靴紐／empty chair・steel table・読めない壁時計・OFF/ON の REC ランプ／confession page（判読不能 smear）／署名の pen/line／cold-cyan DNA bands／cell window に seasons／天秤／dawn の park（abstract）／`AI-assisted visualization`（右下常時） | **実在人物の likeness/顔**（5人・Meili・Reyes・Trump・実在の刑事/判事/検事）・mugshot of a real person・deepfake／**被害者の描写・暴行の imagery/再現**／読める偽公文書／Trump ad art の再現／crime location detail／少年を有罪/加害に見せる framing |
| **R-DOCHL** | **dochighlight 不使用** | 判読ハイライトの意図は `kinetic`/`stat`/`lowerthird`/`highlightring` で代替 | `figures[].kind`/beats/layout 名に `dochighlight`/`DOCHIGHLIGHT` を1件でも出す |
| **R-QUOTE** | **検証済み逐語＋帰属のみ・発明した引用を出さない** | 引用符に入れるのは citation pass で verbatim ロックされた行のみ（+ 非空 attribution）。無い間は**引用符を使わず paraphrase を narration/label に**（`q-alone` は CENTER_STACK に fall back＝§7.2） | 自白/取調べ台詞/未検証の名言を引用符で焼く／attribution 欠落 |

**★禁止語（`check_centralpark_facts.py` が全文字列を case-insensitive 部分一致で検査。1件でも FAIL）:**
`the five were involved` / `they were involved` / `the boys attacked` / `the five attacked` / `possibly guilty` / `may still be guilty` / `the teens did it` / `guilty after all`（R-INNOCENCE）、
`30 hours`（累計取調べの断定・R-NUM）、`wilding`（**断定として**＝媒体/警察のラベルとしてのみ許可・R-VICTIM/CP06 は attribute のこと。※台本本文が "police called it 'wilding'" 等の帰属文脈で使う場合と衝突しないよう、**帰属枠なしの断定 `they were wilding` 系だけを禁止語にする**）。
> **★重要な設計注意:** 台本本文（＝字幕 verbatim）には `confession`/`attacked`/`rape`/`Reyes` 等の語が正当な文脈で含まれる。**上の禁止語は主語付き断定形だけ**（`the five attacked` 等）を選んである。**`attacked`/`confession`/`rape` の単語単独を禁止語に足すな**（字幕 verbatim を巻き込んで false FAIL する）。文脈は下の R-INNOCENCE/R-REYES の payload ルールで捕える。

## 2.2 事実台帳 CP-ID（`03_script/centralpark_facts.v001.json`・**B が `EP50_centralpark_facts.v001.json` の ledger CP01–CP35 から転記して作る**）

**スキーマ版:** `centralpark_facts.v1`。各 CP-ID は `{"claim":..., "value":..., "unit":..., "verified":bool, "confidence":"high|medium", "screen_phrasing":"", "attribution":"", "quote":""}`。
**ledger に裏付けのある値だけ `verified:true`。confidence:medium は `screen_phrasing` の hedge 文言のまま以外は画面に出さない**（断定焼き込み禁止＝R-NUM/R-HEDGE）。

| CP-ID | 内容（screen で使う要点） | conf | 画面での扱い |
|---|---|---|---|
| CP01 | 5人（McCray/Richardson/Salaam/Santana/Wise）強要虚偽自白→1990不当有罪→2002 exonerated | high | R2 象徴のみ |
| CP03 | 暴行の日付 **April 19, 1989**・Central Park（臨床・非描写） | high | year 断定可（**group:false**） |
| CP04 | coma **12** days（May 1 1989 意識回復）・記憶なし | high | `12` 断定可 |
| CP05 | 5人の1989年齢: McCray **15**/Richardson **14**/Salaam **15**/Santana **14**/Wise **16**（load-bearing） | high | ages 断定可 |
| CP06 | "wilding"＝**媒体/警察のラベル**（起源 disputed）・5人の行為の事実ではない | medium | **帰属枠でのみ**（断定禁止） |
| CP08 | 撮影前に**少なくとも7時間** custody・**録画なし**（累計はより大きいが hedged） | high(firm 7) | `7` は "AT LEAST SEVEN HOURS"・**"30 hours" 断定禁止** |
| CP12 | 公判時 **DNA 一致 0**（証拠は自白のみ） | high | `0` 断定可 |
| CP13 | **May 1, 1989** Trump 全面広告・**reportedly ~$85,000**・**5人を名指ししていない** | high(cost hedged) | year/広告存在は断定・**$85,000 は "reportedly ~"**・ad art 再現禁止 |
| CP14/15/16 | 1990 二つの公判・Wise は**成人として**裁かれた | high | year 断定（group:false） |
| CP17 | 重罪で有罪だが**最上位 attempted murder は無罪**（件数を人別に列挙しない） | medium | "acquitted of attempted murder"・**hedged** |
| CP18 | 量刑: 少年 **5–10年**・Wise 成人 **5–15年** | high | 断定可 |
| CP19 | 実服役: 4人 各**約6–7年**・Wise **約13年**（2002釈放） | high(hedged ~) | **"roughly/about"・~13**（断定 "13 years" 単独は避け hedge 併記） |
| CP21 | Reyes＝真犯人・**33⅓ years to life**（Nov 1991 別件） | high | `33 1/3` 断定可 |
| CP22 | Reyes は暴行の**2日前**に同じ公園で別女性を暴行したと **believed to** | medium | "believed to"・Gonzalez 殺害の月を断定しない |
| CP24 | **DNA が Reyes 一人に一致・単独犯**・**1 in 6 billion**（6,000,000,000） | high | `6,000,000,000` は桁区切り可（**group:true**） |
| CP27 | 有罪 **VACATED — December 19, 2002**（Justice Tejada） | high | date 断定（year **group:false**） |
| CP28 | Armstrong 報告＝**却下された反対説のみ**（DA/裁判所は不採用） | medium | R-INNOCENCE 枠でのみ・使わないのが既定 |
| CP30 | **2014 NYC 和解 ~$41,000,000**（4人 各~$7.1M・Wise ~$12.2M） | high(hedged ~) | "roughly $41 million"（**group:true**） |
| CP31 | **2016 NY State 和解 reportedly ~$3.9M**（single-origin） | medium | **"reportedly ~"**・断定禁止 |
| CP32 | **The Exonerated Five**（旧 "Central Park Five"） | high | 名称 |
| CP33 | 2023 Yusef Salaam が NYC Council に当選 等 | high | year 断定（group:false） |
| CP34 | 主題＝少年取調べ・false-confession science・"record the whole interrogation" | high | 主題ライン |
| CP35 | 6人目 Steve Lopez（2022 vacatur）＝**peripheral**・"the Five" に含めない | medium | 任意・周辺 |

> **数値の許可集合（R-NUM・narrative figure/AE/thumb/props のみ対象）:**
> years `{1989, 1990, 1991, 2002, 2014, 2016, 2023}`（**全て group:false**）／ages `{14, 15, 16}`／`5`（five children）／`12`（coma days）／`7`（at least hours）／`0`（DNA matches at trial）／`33 1/3`（Reyes）／`6,000,000,000`（DNA・group:true）／`41,000,000`（$・~・group:true）／`3,900,000`（$・reportedly ~・group:true）／`85,000`（$・reportedly ~・group:true）／`7,100,000`・`12,200,000`（$・per-person ~）／`13`・`6`・`7`（服役年・hedged ~）。**これ以外の数値が figures/AE/サムネ/props に出たら FAIL。** narration verbatim（script.md）は R-NUM 対象外（字幕 verbatim 例外）。

## 2.3 `check_centralpark_facts.py` の検査（exit 0=PASS / 1=FAIL / 2=スキーマ不一致）

**★複製元 `check_cleveland_facts.py` の構造除外を1行も削らない（EP45修正）:**
- `asset_manifest*.json` は **R-NUM 対象外**（構造カウントを巻き込まない）。
- `start/end/dur/fps/width/height/frames/duration_sec/x/y/index` キーは**構造値**として R-NUM スキップ。
- 文脈ルールは `kind != "acttitle"` のとき発火。

**検査対象ファイル（ハードコード。存在するものだけ検査し、無いものは `skipped[]` に明記）:**
```
episodes/PD-2026-050-centralpark/03_script/script.en.v001.md
episodes/PD-2026-050-centralpark/03_script/centralpark_facts.v*.json
episodes/PD-2026-050-centralpark/08_edit/ae_hero/beats.json
episodes/PD-2026-050-centralpark/09_package/*.json / *.txt
episodes/PD-2026-050-centralpark/05_visuals/asset_manifest*.json   （tags/caption_hint/qc.notes・★R-NUM 除外）
remotion/src/data/centralpark_film.json                            （figures[].* の全文字列と数値）
remotion/props/centralpark*.json                                   （title/subtitle）
```

- **R-FORBID（最優先）** — §2.1 の禁止語（主語付き断定形）が対象文字列に出たら即 FAIL。**`attacked`/`confession`/`rape`/`wilding` の単独単語を禁止語に足さない**（字幕 verbatim を巻き込む・§2.1 注意）。
- **R-INNOCENCE（BLOCKING）** — 5人を語る payload（`the five`/`the boys`/`the teens`/名前）に `attacked`/`did it`/`guilty` が**帰属なし断定**で付いたら FAIL。`Armstrong` を含む payload は "rejected"/"did not adopt"/"convictions stayed vacated" のいずれかを同伴（無ければ FAIL）。
- **R-VICTIM（BLOCKING）** — `Meili`/`jogger` を含む payload に負傷詳細・扇情語・imagery 指示があれば FAIL。臨床枠（"attacked and left for dead"/"survived but could not remember"）のみ許可。
- **R-REYES（BLOCKING）** — `Reyes` payload は established facts のみ（`Gonzalez` の月断定・記録外詳細で FAIL）。CP22 は "believed to" 帰属必須。
- **R-NUM（narrative のみ）** — figures[] の `value`/`majority`/`dissent`/`numKeys` 到達値、AE `beats[].value`/`hero`/`left`/`right`、サムネ数字が §2.2 allowed set に**完全一致**必須。**hedged 値（$85,000/$3.9M/$41M/~13yr）が hedge 語（`~`/`reportedly`/`roughly`/`about`/`at least`）なしで断定表示されたら FAIL。** `asset_manifest*.json` は R-NUM 対象外。
- **R-HEDGE** — `confidence:medium` の CP-ID（CP06/CP17/CP22/CP28/CP31/CP35・CP13cost・CP19years・CP20facility）を `verified:true` かつ hedge なし画面焼きで FAIL。
- **R-FACE（R2・owner 改定）** — `has_readable_text==true` **または** `has_identifiable_real_person==true`（実在人物に識別可能）の項目は `role=="reject"`。**`has_human_body==true` は reject しない**（匿名人体は可）。正プロンプトに **実在 likeness 語**（`likeness of <the five/Meili/Reyes/Trump/a real detective・judge・prosecutor>`／`face of <それらの名>`／`recognizable real person`／`mugshot of a real person`／`deepfake`）があれば FAIL（ネガティブは可）。**汎用の `portrait`/`human face`/`person` だけでは FAIL しない**（匿名スタンドインを巻き込まない）。被害者の描写・暴行 imagery があれば FAIL。生成ビジュアル区間の `AI-assisted visualization` 欠落・`description.txt` の AI 開示行欠落で FAIL。
- **R-DOCHL（BLOCKING）** — `centralpark_film.json` の `figures[].kind` に `dochighlight` が1件でも出たら FAIL（`grep -c` が 0 でなければ FAIL）。`beats.json`/layout 名にも出さない。
- **R-QUOTE（BLOCKING）** — 引用符に入る文字列は `APPROVED_QUOTES`（citation pass で verbatim ロックされた行のみ）に一致＋非空 attribution。**ロック行が無ければ引用符ゼロ**（`q-alone` は CENTER_STACK に fall back）。発明した引用・attribution 欠落で FAIL。
- **R-DATE** — `April 19, 1989`（暴行）/`December 19, 2002`（vacatur）/`2014`/`2016` を取り違えない。年は全て `group:false`（§9）。

**出力:** `09_package/facts_lock.v001.json`（`{"pass":bool,"violations":[{"file","rule","line","excerpt"}],"skipped":[...]}`）。**CLI:** `--json`。

---

# 3. ★境界契約: `asset_manifest.v001.json`（Aから受け取る唯一のファイル・FROZEN）

## 3.1 スキーマ（**Aが生成する。Bはこの形を前提に読む・A↔B 1バイト一致**）

**スキーマ版:** `centralpark_assets.v1`（固定。異なれば **exit 2**）。EP50 spec の点数に一致:
**still_body 430 / still_i2v_source 85 / motion 85 / factory 485 / overlay（Aの固定値・§3.3-8）。**
**★サムネは独立分類を持たない。** body のうち **8枚**に `also_thumb:true`（`role=thumb`/`still_thumb` を作らない）。
**`role` enum（固定・3値）:** `"body"` | `"i2v_source"` | `"reject"`。
**`counts`（固定キー・確定値）:** `{ "still_body": 430, "still_i2v_source": 85, "motion": 85, "factory": 485, "overlay": <A固定> }`。

- `stills[]`: `asset_id`/`scene_id`/`role`/`also_thumb`/`act`(0..7)/`public_path`(`centralpark/img/S###.png`)/`depth_path`(role=body は実在必須)/`width>=3840`/`sha256`/`tags`/`caption_hint`/`qc{...}`。i2v 種は `role=="i2v_source"`・`public_path==null`。
- `motion[]`: **85本**。`public_path` は `.mp4` かつ `_rife` を含む。`source_scene_id` は i2v 種 ID を指す。`build_centralpark_film` が `public_items(manifest,"motion")` で全読込（**0本 or ≠85 なら exit 1**）。
- `factory[]`: **485本**。`public_path` は `/factory/` を含む。`eyeballed_content` 非空・`qc.label_matches_content==true`。`build_centralpark_film` が全読込（**0本 or ≠485 なら exit 1**）。
- `overlay[]`: `cuts[].src` に出さない（§5.5 の合成レイヤー扱い）。`public_path` は `/overlay/` を含み `/factory/` を含まない。

## 3.2 Bがこのマニフェストから作るもの（**EP50 spec の cuts 割当**）

| マニフェスト | Bでの使い道 | spec |
|---|---|---|
| `stills[role="body"]` 430枚 | **静止画カット505本**（`kind:"img"`・`treatment` 循環・**各≤2回**） | still distinct430/cuts505 |
| body で `also_thumb==true` の8枚 | サムネ3案の背景（§12・8 asset ID・A↔B 一字一致） | — |
| `stills[role="i2v_source"]` 85枚 | **本編カットに出さない**（i2v 種・A が Wan で motion 化済み） | — |
| `motion` 85本 | **i2vカット170本**（`kind:"footage"`・**各≤2回**） | motion distinct85/cuts170 |
| `factory` 485本 | **実写カット485本**（`kind:"footage"`・**各1回のみ**） | factory distinct485/cuts485 |
| `overlay` | **`cuts[].src` に出さない**（§5.5） | — |

**合計 505 + 170 + 485 = 1,160 カット / distinct 430+85+485 = 1,000 / first-use 1000/1160 = 0.8621 ✓（floor 0.70）／still-share 505/1160 = 0.4353 ✓（cap 0.45）**

## 3.3 `scripts/check_centralpark_asset_manifest.py`（消費側バリデータ・BLOCKING）

```bash
$PY scripts/check_centralpark_asset_manifest.py --assets <path> [--json]
```
検査（1違反で exit 1・`schema_version` 違いだけ exit 2）:
1. `schema_version=="centralpark_assets.v1"` / `episode_id=="PD-2026-050-centralpark"` / `slug=="centralpark"` / `is_stub==false`
2. `counts.*` が各配列の実長と一致し確定値: `still_body==430` / `still_i2v_source==85` / `motion==85` / `factory==485` / `overlay==<A固定>`
3. `role` は `body`/`i2v_source`/`reject` の3値のみ（`thumb`/`still_thumb` で FAIL）
4. `role=="body"` 全 still で `public_path` 非null・`remotion/public/<public_path>` と `<stem>_depth.png` が**両方実在**（`depthSrcOf()=src.replace(/\.[^.]+$/,'_depth.png')`・depth 欠落はレンダークラッシュ）。`role=="i2v_source"` は `public_path==null`
5. `role!="reject"` 全 still で `max(width,height)>=3840`（`preflight_render_gate.MIN_LONG_EDGE_PX=3840`）
6. `motion[].public_path` が `.mp4` で終わり `_rife` を含む
7. `factory[].public_path` が `/factory/` を含む
8. `overlay[].public_path` が `/overlay/` を含み `/factory/` を含まない・overlay 長が A 固定値
9. `sha256` が全配列を通して一意（**EP1〜49 の素材と被りゼロは A が保証・B は自集合内一意を検査**）
10. `factory[].eyeballed_content` 非空・`qc.label_matches_content==true`
11. **★owner 改定:** `qc.has_readable_text==true` **または** `qc.has_identifiable_real_person==true` の項目は `role=="reject"`（R-FACE/R2）。**`qc.has_human_body==true` は reject 条件でない**（匿名人体は可）・`has_identifiable_face` は「実在人物として識別可能な顔」の意に再定義（匿名・非識別顔は可）
12. `also_thumb==true` の body が**ちょうど8枚**・`scene_id` 集合が §12 の8 ID と完全一致（**CODEX_A の also_thumb 集合と一字一致**）
13. 全文字列値が §2 の R-FORBID/R-FACE/R-DOCHL を通る（R-NUM は asset_manifest 除外）

> **★このバリデータは A の `--verify` と同じ不変条件を独立実装（二重チェック）。** counts が確定値と食い違ったら組まず A に差し戻す。**特に `factory==485` と `motion==85` が非0であることを最優先で assert（EP45 空配列事故の直接防止）。**

---

# 4. narration_index（TTS は課金＝B は起動しない。**実測版を消費**する）

## 4.1 なぜ narration_index か
`build_centralpark_film.py` は**尺・区間・字幕を narration_index から導出**する。**秒数をコードに直書きしない。** 唯一の正は narration_index。

## 4.2 スキーマ（`centralpark_narration.v1`）
```jsonc
{
  "schema_version": "centralpark_narration.v1",
  "episode_id": "PD-2026-050-centralpark",
  "is_stub": false,
  "total_seconds": 3606.0,         // ★provisional。FINAL は forced-align 実測が上書き
  "chunks": [ { "section": "HOOK", "start": 0.0, "end": 5.5, "text": "..." } ]
}
```
**section 値（固定・9区）:** `HOOK` / `OP` / `ACT_1` / `ACT_2` / `ACT_3` / `ACT_4` / `ACT_5` / `ACT_6` / `ACT_7`。
`build_centralpark_film.py` は `section_windows()`（各 section 最初のチャンク start）で幕境界を得る。**存在しない演出マーカーを発明しない。**

## 4.3 spec のタイムライン（**設計目標。実タイミングは narration_index が上書きする**）
7幕・語数配分（PRODUCTION_SPEC §acts_plan）: ACT1 ~1240 / **ACT2 ~2250（最長・engine）** / ACT3 ~1750 / ACT4 ~1900 / ACT5 ~1730 / ACT6 ~1900 / ACT7 ~945 語。**総語数 10,715**。
**唯一の正は `python scripts/check_script_length.py <script> --longform --json`**（cap ≈10,900）。**自己申告・体感の尺判定は禁止。**

## 4.4 実測 narration_index の受領
本番は別工程が TTS→faster-whisper で `06_audio/narration_index.v001.json`（実測語タイム・`is_stub:false`・`measure_vo_wpm` 合格帯 **168–190 wpm**・190超は破棄→speed 0.95 再発注＝BLOCKING）を作る。**課金ジョブなので B は起動しない。** 来た json を `--narr` に渡すだけ。**台本本文はそのまま。**

---

# 5. `centralpark_film.json` の構築（`scripts/build_centralpark_film.py`＝`build_cleveland_film.py` の複製・実素材のみ）

## 5.1 `FilmData` 型（`CaseFilm.tsx` から）
```ts
export type Cut = {start:number; dur:number; kind:'img'|'footage'; src:string; treatment:string; seed:string};
export type FilmData = {
  fps:number; narration:string; narrationSeconds:number; hookSeconds:number; hookLine:string;
  hook:{...}[]; cuts:Cut[]; captions:{start:number;end:number;text:string}[];
  graphics:{start:number;end:number;lines:string[]}[];   // 必須。EP50 は []
  figures?:FigureSpec[]; heroCuts?:{start:number;dur:number;src:string}[];
};
```
- `fps = 30`（film fps）。`narration = "centralpark/narration.mp3"`。
- **★`hookSeconds = 8.0`**（8s の flash-forward モンタージュ尺。**0 だと全体が 8s desync**＝ビルダ末尾で `assert film["hookSeconds"]==8.0`）。
- **★`hookLine` = centralpark 固有（流用禁止・§1.1 HOOK "restraint, promised" 由来）:**
  ```
  "Five children. A room with the camera switched off. And a confession the evidence would erase."
  ```
  （**別エピソードの hookLine を焼いたら BLOCKER。** R-INNOCENCE/R-QUOTE 整合＝5人・録画されない部屋・証拠が消す自白）。

### 5.1.1 ★durationInFrames の4項関数（provisional・実測後に更新）
```
caseFilmDurationInFrames(centralparkFilm, fps=30)
  = round(hookSeconds*fps)     // 8.0*30 = 240
  + round(OPENING_SEC*fps)     // 3.5*30 = 105
  + ceil(narrationSeconds*fps) // 3606.0*30 = 108,180（provisional）
  + round(ENDCARD_SEC*fps)     // 9.0*30 = 270
  = 240 + 105 + 108,180 + 270 = 108,795 frames = 3626.5s = 60:27（provisional）
```
> **★`narrationSeconds = 3606.0` と `durationInFrames = 108,795` は PROVISIONAL**（10,715語 / 178.3 wpm の推定）。**FINAL は測定 TTS narration の forced-align から来る。** VO master 生成後、ビルダは `narration_index.total_seconds` を `narrationSeconds` に入れて durationInFrames を**同関数で再計算**し、**`EP50_centralpark_PRODUCTION_SPEC.v001.json` の `runtime_plan` と `Root.tsx` の登録値を実測値に更新する**（これが SPEC を書き換えてよい唯一の例外）。**`total_seconds/fps` の上限 assert は置かない**（60分尺・cleveland の 750s assert は複製後に削除する。ただし measured が推定の ±3% を超えたら stderr で警告）。

## 5.2 カット構成（**§3 マニフェストから機械的に組む・紙芝居回避が最優先**）
```
総カット 1,160 = factory 485 (footage) + motion 170 (footage) + 静止画 505 (img)
[A] first-use share  distinct 485+85+430 = 1000 → 1000/1160 = 0.8621   ✓ ≥0.70
[B] per-asset cap    factory 485/485=1.00 ✓≤1 ／ motion 170/85=2.00 ✓≤2 ／ still 505/430=1.18 ✓≤2
[C] animation_mix    still-share(cut) = 505/1160 = 0.4353 ✓≤0.45 ／ motion-cov = (485+170)/1160 = 0.5647 ✓≥0.45
                     frame ベースも still の dur を footage より系統的に短く保ち ≤0.45
[D] 平均ショット長   3606 / 1160 = 3.109 s/カット ✓≤7.0（max）
[E] factory 下限     30秒に1本 = ~120 → 485本 ✓
```
> **★マニフェストが still430/factory485/motion85 を割ったら組まず A に差し戻す**（still を増やして factory を削るな）。**境界は `QUANT=f(0.5)=15f` グリッドにスナップ**（mean 3.109s・max ≤7.0s）。

## 5.3 割り当てルール（`build_cleveland_film.py` の `allocate()`/`take()`/`repeated()` を踏襲）
1. 各幕の秒窓を `section_windows()` から取り factory:motion:still を按分（確定値は「合計 factory485/motion170/still505」だけ・**最密は ACT2・ACT5**）
2. **factory は各1回のみ**・**motion/still は各≤2回**（`repeated(pool,need,cap,key)`）
3. 同一素材を連続させない・still `treatment` は `["depth","scan","duotone","focus"]` 循環（同 treatment を3連続させない）
4. **still の `dur` を footage より系統的に短く**（§5.2[C]）・motion の `dur` は 3.0–3.4秒
5. **AEカードの区間（§7.2）に重なるカットも存在させる**（コンポジタ SKIP 時に穴が空かない）
6. **★実写優先 & 意味マッピング（§5.8）:** footage カットは narration ビートの内容に一致する実写を優先配置し（courthouse→評決／NYC street→その夜／precinct→取調べ／prison→lost years／lab→DNA 等）、**意味の合う実写がある所は AI-i2v ではなく実写を使う**。AI-i2v は抽象/象徴ビート専用に温存。**物語に合わない実写を無理に差し込まない。**

## 5.4 `figures[]` と `captions[]`
- `figures[]` は §6（**165本**・floor 151 に +14・`graphics[]=[]`・**dochighlight 0**・**年 group:false**）
- `captions[]` は narration_index 全チャンクを verbatim（`build_captions()` と同一）・SRT 同時出力

## 5.5 合成レイヤー（`overlay`）— **`cuts[].src` に出さない**（factory 判定＝上限1回で FAIL する）。`centralpark_film.json` に `overlays` 独自キーで持たせる（`CaseFilm` は未知キーを無視）か専用レイヤーで `screen` 合成。**★overlay は特定カットに疎に乗せる per-beat アクセントのみ＝全編に常駐する持続レイヤーにしない（§5.9）。`subtle_vignette_*`/`tv_scanline_glow_*` は局所モチーフ（例: ACT3 videotape ビート）であって全画面 wash ではない。**

## 5.6 ビルダ出力
| 出力 | パス |
|---|---|
| film.json | `remotion/src/data/centralpark_film.json` |
| public コピー | `remotion/public/centralpark/film_data.v001.json` |
| build provenance | `episodes/PD-2026-050-centralpark/04_scenes/centralpark_build_manifest.v001.json` |
| beatsheet（figures+AE 突き合わせ） | `episodes/PD-2026-050-centralpark/04_scenes/centralpark_beatsheet.v001.json` |
| SRT フォールバック | `episodes/PD-2026-050-centralpark/08_edit/captions.final.v001.srt`（§8 の生成器が上書き） |

> **★beatsheet 命名の重大注意:** `check_motion_density`/`check_animation_mix` は `04_scenes/premium_beatsheet.v*.json` を**自動検出して film.json より優先**する。**B の beatsheet は `centralpark_beatsheet.v001.json`（`premium_` を付けない）**にしてゲート測定源を film.json 一本に保つ。

## 5.7 CLI
```bash
$PY scripts/build_centralpark_film.py \
  --assets episodes/PD-2026-050-centralpark/05_visuals/asset_manifest.v001.json \
  --narr   episodes/PD-2026-050-centralpark/06_audio/narration_index.v001.json \
  --out    remotion/src/data/centralpark_film.json
```
**実素材のみ。`is_stub==true` を渡されたら exit 1。★`public_items(manifest,"factory")` が空 or ≠485、`public_items(manifest,"motion")` が空 or ≠85 なら exit 1。** 末尾に `check_asset_reuse` 相当の自己レポートを print。

## 5.8 ★実写ストック優先ポリシー（EP48/49 の burned lesson＝実写ストック0本を潰す）

> **owner directive（EP48/49 retro）:** 「せっかくたくさんダウンロードしたんだから意味のある所に使ってほしい」。EP48/49 は本編を **AI still 100% ＋ AI-i2v** で組み、**実写ストックライブラリを1本も使わなかった**。60分尺の本作ではこれを構造で潰す。**実写フッテージは AI-i2v より優先**する（実写は i2v の warping も回避できる）。**ただし物語に合わない素材を無理に差し込まない。**

**★ストックライブラリの実体（A↔B 契約・B はこれが manifest に載っている前提で消費する）:**
`H:\pd-media\assets\stock`（マニフェスト `H:\pd-media\assets\stock\STOCK_MANIFEST.json`・**動画 74本 ＋ 静止 155本**・pexels/pixabay・**商用可**＝`ALLOWED_LICENSES` の `Pexels License`/`Pixabay Content License` に既に含まれる）。**この 74本の実写動画クリップを factory 485レーンの調達源に必ず含める**（従来の `H:\pd-media\assets\factory` 在庫だけで埋めない）。**A の factory 選定がこれを取り込む（§CODEX_A 7.4a）＝B は manifest の `factory[]` に実写ストック由来クリップが載っていることを前提に allocate する。**

1. **(a) 意味マッピング（semantic mapping・必須）:** footage カットは narration ビートの**内容に一致**させる。ストック/実写の被写体カテゴリ → 幕/ビート:
   - courthouse / columns / gavel / courtroom → 評決・判決・vacatur（ACT3・ACT6）
   - NYC の街 / Central Park / city streets / subway → その夜・都市（ACT1）
   - police / precinct / institutional interior → 取調べ（ACT2・**顔なし・後ろ姿/遠景のみ**）
   - prison / correctional 外観 / fence / corridor → lost years（ACT4・非扇情）
   - documents / paperwork / files（判読不能） → 記録・lab report（ACT2・ACT5）
   - news-broadcast / newsprint / press texture → publicity・trials（ACT3・**headline は判読不能**）
   - protest / crowd / demonstration → reckoning（ACT6）
   - lab / evidence / forensic → DNA（ACT5）
   - dawn / sky / horizon → exoneration（ACT6）
   実装: `allocate()` は **footage カットの `covers_scene_id`/manifest の `eyeballed_content` が当該ビートのカテゴリと一致するもの**を優先配置する。**一致しない実写を無理に置かない**（irrelevant clip の強制配置は §5.3 の同一素材連続禁止と同様に避ける）。
2. **(b) 実写 > AI-i2v の優先:** あるビートに**意味の合う実写クリップが存在するなら、AI-i2v ではなく実写を使う**。AI-i2v（motion 85本）は **実写に置き換えられない抽象/象徴ビート専用**に温存する＝DNA bands の点火・five descending child silhouettes・interrogation-room の抽象・signature の dissolve・cold-cyan flood・scale の傾き（＝§CODEX_A 4.5 の i2v storyboard 群・**R-FACE / no-crime-imagery 上、実写が使えない/使うべきでない絵**）。**具体的な現実世界のビートは実写、抽象/象徴のビートは AI＝この線引きが owner 意図と R-FACE の両方を満たす。**
3. **(c) 実写のスクリーンタイム目標（★counts は固定・レーン内の調達品質で達成）:**
   - motion スクリーンタイムの内訳: 実写 factory 485カット / (factory 485 + i2v 170) = **74.0%** が実写、AI-i2v は 26.0%。**この比率を下回らせない**（factory を still に振り替えて実写を痩せさせない＝§5.2 の逆流禁止）。
   - **factory 485レーンのうち、`H:\pd-media\assets\stock` の 74本から意味・QC・R-FACE を通る限り**（目標: 通過する全 74本を採用・無理な水増しはしない）**を採り、残りを `H:\pd-media\assets\factory` 在庫で埋める。** どの factory エントリが stock ライブラリ由来かは A の ledger に記録され、B は `check_centralpark_asset_manifest` で `factory[]` の非空・実在・意味ラベルを検証する（§3.3-10）。
   - **ストック静止（155本）は本編 body still レーン（AI 430本）に混ぜない**（body は 1シーン1 AI プロンプトの固定モデル・R-FACE パイプライン）。ストック静止を使う場合は **顔・可読テキストを目視で除外した face-free/text-free のもののみ**、factory/情景レーンの扱いに限る。**被害者・暴行・実在人物を写した実写は使わない（R-VICTIM/R-FACE/§CODEX_A 7.5）。**
4. **(d) カラーマッチ（実写を AI still に一致させる neutral grade）:** pexels/pixabay の実写は発色がバラつく。**footage カットに一貫した neutral な cold-steel-cyan グレード**（INK ベース `#0A0A0C`・cyan キー `#2F9FC4`・bone ハイライト `#EDEDE8`）を掛け、AI still と**一枚の palette に読めるように統一**する。グレードは **conform 時（§CODEX_A 10.1 の libx264 conform）または footage `treatment` として最小限・neutral に**適用。**milky wash にしない**（§5.9・低コントラスト曇りは禁止）。他話色（gold/blue/amber/teal/crimson/green/violet/plum）に寄せない。

> **★検証:** 実写ストックが意味のあるビートに載っているか・実写比率 74% を割っていないか・カラーマッチが取れているかは **§13.1 の FULL-60分アイボール（周1 structure）と `visual_asset_qc`** で確認する（§10）。**「AI だけで組んだ」を再発させない。**

## 5.9 ★NO 全画面ヘイズ/フォグ/スキャンライン（EP48/49 の burned lesson＝画像全体の曇りを潰す）

> **owner directive（EP48/49 retro）:** 「全体的に画像に曇りがかかってる…改善して」。EP48/49 は **milky で低コントラストな wash ＋ 斜めスキャンラインのテクスチャを毎フレームに乗せて**出荷し、owner に却下された。本作はこれを**明示的に禁止**する。

1. **全画面 wash 禁止:** 本編ベース合成に **全編（full-timeline）に渡る haze/fog/mist/曇り/vignette-wash レイヤーを乗せない。** **全フレームに渡る scanline/CRT/斜めテクスチャのレイヤーも乗せない。** 画像は**クリアで高コントラスト**に保つ。
2. **グレードは最小・neutral:** どのグレードも **最小限かつ neutral**（cold-steel-cyan の palette 統一＝§5.8(d)）。**低コントラストな milky veil を作らない。** EP48/49 の曇り wash を1フレームも再現しない。
3. **overlay は per-beat の疎なアクセントのみ（§5.5）:** 60本の合成レイヤー（`particle`/`light`/`vfx`）は**特定カットに `screen`/`multiply` で疎に**乗せる per-beat アクセント。**全編に常駐する持続レイヤーにしない。** ライブラリ内の `subtle_vignette_*` / `tv_scanline_glow_*` は**局所モチーフ**（例: ACT3 の videotape「confession performed」ビート ~1360–1430s の TV-glow scanline drift＝そのビート限定・§DESIGN 1.5 の該当行）であって、**全画面の恒常 wash ではない**。局所モチーフとして1〜数ビートに置くのは可、毎フレーム化は禁止。
4. **still `treatment` の "scan"（§5.3 循環）:** subtle な局所テクスチャに留める。**全画面 scanline veil 化・全体のコントラスト低下を招かない**（milky にしない）。
5. **AE 36カード内部のグレード:** §7.4 の共通スタックの「グレードウォッシュ(INK/MULTIPLY)＋羽根ビネット」は**各カード内部（36 moments 限定・局所）**なので許容だが、**最小・neutral に保ち**、これも milky wash に読めるほど強くしない。
6. **composite で全画面ヘイズを注入しない（§7.9）。** ffmpeg 合成で全編に渡る blur/haze/scanline フィルタを足さない。

> **★検証:** §13.1 の FULL-60分アイボールで **どのフレームにも全画面の曇り/スキャンラインが無い・画像がクリアで高コントラスト**であることを確認する（周1）。1フレーム判定禁止。**DESIGN §1（VISUAL LANGUAGE）がこの「clear・high-contrast」を統べる＝ここに反する wash は VISUAL INTENT 違反。**

---

# 6. Remotion 側 `figures[]`（**165本・floor 151 に +14・`graphics[]=[]`・dochighlight 0・年 group:false**）

## 6.1 密度の検算（`check_motion_density`・**AE 36 moments は1本も数えられない**）
```
body-minutes = 3606.0/60 = 60.10 min
floor(2.5/min) = ceil(60.10×2.5) = 151     （SPEC beats_floor 140/151 の上位）
design = 165 beats → density 165/60.10 = 2.745/min ✓≥2.5
coverage 165×平均6.0s = 990s / 3606 = 0.2745 ✓≥0.25 ／ variety 15 kinds ✓≥6
dochighlight 0 ／ stub 0 ／ quote 0 ／ votetally 0 ／ no 30s window figure-less
```
> **★3軸すべて AND。** 各枠 dur **5.2–6.5s** を基本に。

## 6.2 ★★★ `FigureSpec` の `kind` は**実在する小文字値のみ・`dochighlight` は使わない** ★★★
> 大文字名は union に無く無言で消える。`comparebars`→`compbars`／`VoteTally`→`votetally`。**`dochighlight` は union に在るが1本も使わない（R-DOCHL）。** **quote/votetally は不使用**（verified-verbatim/confidence:high 票が無い＝fact discipline）。

**§4.3 kind 別 総数・payload（`remotion/src/components/FigureBeats.tsx` の union で全数検証済・全 `start`/`end` 必須・全小文字）:**

| kind | 数 | payload（実 union） | 用途（confidence:high or hedged） |
|---|---:|---|---|
| `lowerthird` | 46 | `{primary; secondary?; accent?}` | 開示 `AI-assisted visualization`×2／place・date・doctrine・hedged-fact labels |
| `kinetic` | 24 | `{lines[]; style?; emphasisWords?}` | emphasis 行（"IT WILL MATCH NONE OF THEM"／"THE STORY, FED IN"／"ONE MAN. HIM."／second-person）・emphasisWords 1–2語 |
| `mechanism` | 13 | `{mechanism:'closingdoor'\|'gears'\|'faultsplit'}` | gears＝interrogation machine／closingdoor＝minimization trap／faultsplit＝ghost theory splits from evidence |
| `compbars` | 11 | `{items:[{label; value; accent?}]}` | confessions 5 vs DNA 0／matched-Reyes-1 vs matched-five-0（**中立**） |
| `timeline` | 10 | `{events:[{year; text}]}` | that night→2002／Reyes 1989→Nov1991→2002／procedural 2002→2014→2016（**年テキストは group:false 相当の literal 文字列**＝下記注） |
| `stat` | 10 | `{value; label; prefix?; suffix?; decimals?; topLabel?}` | 12(coma・CP04)／5(children・CP05)／7("AT LEAST" hours・CP08)／33⅓(Reyes・CP21)／13(Wise "~"・CP19) |
| `numberticker` | 6 | `{value; label?; prefix?; suffix?; decimals?; group?}` | 6,000,000,000(DNA・CP24・**group:true**)／41,000,000($・CP30・**group:true**)／3,900,000($・CP31 reportedly・group:true)。**年を出す numberticker は `group:false`** |
| `bar` | 6 | `{data?/items?:[{label; value}]}` | YEARS-SERVED: four ~6–7 ×4 ＋ Wise ~13（CP19・hedged） |
| `arrow` | 6 | `{from?; to?; label?}` | story fed detective→child／DNA→one man |
| `highlightring` | 6 | `{cx?; cy?; r?; label?}` | OFF REC light を囲む／the unread lab line |
| `pindropmap` | 4 | `{pins:[{x; y; label?}]}` | park geography **abstracted 2–3点**（**NO crime location detail**） |
| `routemap` | 3 | `{pins?; label?}` | その夜の drift（abstracted） |
| `spotlight` | 5 | `{cx?; cy?; r?; dim?}` | 単一 cold light on the chair（HOOK/Act7・restraint） |
| `regionmap` | 2 | `{label?; pattern?}` | 1989 の city（abstracted） |
| `acttitle` | 3 | `{title; kicker?; index?}` | **intra-act sub-heads のみ**（"THE ROOM"／"THE MACHINE"／"THE LADDER"）・**AE の 7 act-title と1秒も重ねない**（幕頭は AE が担う） |
| **合計** | **165** | | **variety 15・dochighlight 0・stub 0・quote 0・votetally 0** |

> **★年 group:false（EP46/47 の "1,985" バグ回避・§9）:** `numberticker`/`stat`/`lowerthird` が YEAR（1989/1990/1991/2002/2014/2016/2023）を数値として出す場合は `group:false` を必ず set。`timeline` の `events[].year` は文字列なのでコンマ群化しないが、**"1989" を "1,989" と書かない**（literal 文字列で置く）。**桁区切りが正しい 6,000,000,000／$41,000,000／$3,900,000 は既定 `group:true`。** `check_year_grouping.py` が enforce。

## 6.3 配置方針（§4.2 幕別配分・§2 台帳の値だけ焼く・kind を分散・7制約順守・dochighlight 0）
| 幕 | beats | 主 kind |
|---|---:|---|
| HOOK/OP | 3 | lowerthird(開示)・kinetic・spotlight |
| ACT1 The Night | 18 | lowerthird・kinetic・routemap・pindropmap・regionmap・stat・compbars・arrow・highlightring |
| **ACT2 Interrogations** | **36** | **mechanism(closingdoor/gears)**・compbars・arrow・kinetic・stat・timeline・lowerthird・acttitle(sub) |
| ACT3 Trials | 23 | kinetic(headline)・compbars・lowerthird・mechanism(faultsplit)・timeline・stat・highlightring |
| ACT4 Lost Years | 22 | bar・lowerthird・kinetic・timeline・stat・compbars・acttitle(sub) |
| **ACT5 Confession & DNA** | **28** | **numberticker**・**compbars**・timeline・mechanism(faultsplit)・pindropmap・stat・kinetic・lowerthird・highlightring |
| ACT6 Exoneration | 20 | numberticker・lowerthird・kinetic・mechanism(closingdoor)・stat・compbars・timeline |
| ACT7 What It's Worth | 15 | mechanism(closingdoor)・compbars・kinetic・spotlight・lowerthird・stat |
| **計** | **165** | variety 15 |

## 6.4 figures アンカー設計（`build_cleveland_film.py` の `FIGURE_ANCHORS` 方式）
`(anchor_sec, payload)` を秒昇順、`build_figures()` が `end = min(anchor+FIG_DUR, next_anchor-FIG_GAP, total-0.5)` でクランプ、`end-start < FIG_MIN_DUR` なら exit 1。`FIG_DUR=6.0 / FIG_MIN_DUR=3.0 / FIG_GAP=0.4`。**アンカー秒は narration_index の section 窓に対する相対で置く**（秒直書き禁止）。

## 6.5 配置ルール
1. **AE の 36 moments（§7.2）と1秒でも重ならない**（`validate_centralpark_beats` が突き合わせ・Tier-B set-piece と同じ物語ビートの in-film figure は時刻を分離）
2. **同じ kind を連続させない**（compbars の直後に compbars を置かない）・lowerthird 46/165=27.9%（単一 kind 支配なし）
3. 1枠 5.2–6.5秒
4. `kinetic[].lines`/`*.label`/`primary`/`secondary` は §2（R-INNOCENCE/R-VICTIM/R-REYES/R-NUM/R-FACE/R-DOCHL/R-QUOTE）検査対象
5. 台帳外の数値・hedged 断定を `value`/`numKeys` に置かない・**年は `group:false`**
6. `emphasisWords` は1–2語のみ・**`kind` に `dochighlight` を1件も置かない**

---

# 7. After Effects — ★GO HEAVY・2-tier・36 moments（`build_centralpark_hero_cards.py` / `composite_centralpark_hero.py`）

> **owner directive: "AEをガッツリ効かせて、時間はかかってもいい"。** AE は garnish ではなく本作最大の感情ピークを担う bespoke set-piece。**36 moments = Tier A 24 + Tier B 12**。時間/労力は明示的に許可されている。AE は film.json とは別に ffmpeg で本編に焼き込む（§0.5-2＝密度に数えられない）。

## 7.1 位置づけ・共通ルール（両 tier）
`build_cleveland_hero_cards.py`（FIXED版）を**複製し EXTEND**：cleveland の**6種 layout（`buildActTitle`/`buildCenter`=CENTER_STACK+MONEY_STACK/`buildQuote`/`buildVote`/`buildCompare`）を1行も削らず残し**、Tier-B の**8新 builder を ADD**する。`fit_size()`/`count_keys()`/REPO path 出力/二段レンダ/完了マーカー/機械の罠対処は**1行も削らない**。**末尾 `else throw "unsupported layout"` は保持**（未実装 layout を今後も弾く）。

**★AE 色定数（0..1 float・cold forensic steel-cyan レーン。EP41 gold / 42 blue / 43 amber / 44 teal / 45 crimson / 46 green / 47 violet / 48 / 49 plum を流用禁止）:**
```python
ACCENT = [0.184, 0.624, 0.769]  # #2F9FC4 cold steel-cyan（数値・下線・DNA・lane 分離）
INK    = [0.039, 0.039, 0.047]  # #0A0A0C 近黒ルート
BONE   = [0.929, 0.929, 0.910]  # #EDEDE8 type
DAWN   = [0.788, 0.541, 0.235]  # #C98A3C dawn-amber（★exoneration/close moment のみ）
WHITE  = [0.961, 0.969, 0.980]  # #F5F7FA
SILVER = [0.784, 0.804, 0.839]  # #C8CDD6（開示テキスト）
```
> **★複製元の `ACCENT=[0.698,0.227,0.282]`（EP45 crimson）を必ず `[0.184,0.624,0.769]` に置換。** **dawn-amber `[0.788,0.541,0.235]` は exoneration/close moment のみ**（`REC_LIGHT`-on・`SCALE_TIP`-right・`HERO_TIMELINE`-resolve・`NAME_WALL`-close・`SIGNATURE_ERASE` resolve・`c-vacated`・`m-41m`・`c-state39`・`c-salaam`）。他は全て cyan/bone。
> **measured-fit MANDATORY（全 tier）:** `fit_size()` Python 事前フィット＋JSX `sourceRectAtTime(t,false).width` 実測再フィット＋quote-wrap（advance-width 推定禁止＝EP40 文字切れ原因）。
> **全 moment 右下に `AI-assisted visualization`（R1・Oswald 20px/SILVER/opacity70/`[W-32,H-28]`）を焼く**（AE は不透明の全画面 mp4 として overlay されるため、無いと本編右下の開示が隠れる）。字幕帯とは縦56px 以上離す。
> **★どの moment も被害者を name/depict しない・Trump ad art を再現しない・no faces**（DNA_LADDER/INTERROGATION_ROOM は abstract・no crime imagery）。

## 7.2 AE デッキ（**この表が契約・id/layout/CP-id/anchor は DESIGN §3 と一字一致・`validate_centralpark_beats` が突き合わせ**）

**★DATE_STAMP / SEAM_TRANSITION は emit しない（複製元非実装＝クラッシュ）。VOTE_SPLIT は emit しない（confidence:high の jury 票割れが台帳に無い＝捏造回避）。QUOTE_CARD は `q-alone` の reserved 1枠のみ**（verified-verbatim ロックまで CENTER_STACK に fall back）。

### Tier A — 標準ヒーローカード 24枚（6 proven layout・anchor は body-relative 秒）
ACT_TITLE_CARD×7 / CENTER_STACK×11 / SPLIT_COMPARE×5 / MONEY_STACK×1 / QUOTE_CARD×1(reserved)。尺 ≈143s。

| id | layout | 主表示 / copy | anchor(s) | dur | CP-id | accent |
|---|---|---|---:|---:|---|---|
| t-a1 | ACT_TITLE_CARD | ACT I / THE NIGHT · APRIL 1989 | 27.0 | 5.0 | CP03 high | cyan |
| c-noevidence | CENTER_STACK | AT THE MOMENT OF QUESTIONING / NO PHYSICAL EVIDENCE | 372.0 | 6.0 | CP08/CP12 high | cyan |
| t-a2 | ACT_TITLE_CARD | ACT II / THE INTERROGATIONS | 452.0 | 5.0 | — | cyan |
| c-roompromise | CENTER_STACK | A ROOM AND A PROMISE / "YOU CAN GO HOME IF YOU JUST SAY IT" | 560.0 | 6.0 | CP08/CP34 high(paraphrase, not attributed quote) | cyan |
| c-fivechildren | CENTER_STACK | FIVE CHILDREN / AGES 14 TO 16 | 720.0 | 6.0 | CP05 high | cyan |
| c-sevenhours | CENTER_STACK | BEFORE THE CAMERAS / AT LEAST SEVEN HOURS · NONE OF IT RECORDED | 505.0 | 6.0 | CP08 firm high | cyan |
| cmp-fedsigned | SPLIT_COMPARE | THE INTERROGATION / "FED IN" ↔ "SIGNED" / "THE GENTLENESS WAS THE TRAP" | 905.0 | 6.5 | CP10/CP34 high | cyan |
| cmp-confdna | SPLIT_COMPARE | THE CONTRADICTION / "5 CONFESSIONS" ↔ "0 DNA MATCHES" / "THE EVIDENCE POINTED ELSEWHERE" | 1080.0 | 6.5 | CP10/CP12 high | cyan |
| t-a3 | ACT_TITLE_CARD | ACT III / THE TRIALS · 1990 | 1170.0 | 5.0 | CP15/CP16 high | cyan |
| c-papersfirst | CENTER_STACK | 1989 / TRIED IN THE PAPERS FIRST | 1245.0 | 5.5 | CP14 high | cyan |
| c-trumpad | CENTER_STACK | MAY 1, 1989 / A FULL-PAGE AD DEMANDED THE DEATH PENALTY · REPORTEDLY ~$85,000 · IT DID NOT NAME THE FIVE | 1305.0 | 6.5 | CP13 high(cost hedged) | cyan（**blank full-page frame・NO ad art**） |
| cmp-verdict | SPLIT_COMPARE | THE VERDICTS / "CONVICTED" ↔ "ACQUITTED OF ATTEMPTED MURDER" / "EVEN THE JURIES HESITATED" | 1600.0 | 6.0 | CP17 hedged | cyan |
| cmp-sentence | SPLIT_COMPARE | THE SENTENCES / "FOUR: JUVENILE · 5–10 YRS" ↔ "KOREY WISE, 16: AS AN ADULT" / "A BIRTHDAY MADE THE DIFFERENCE" | 1655.0 | 6.5 | CP18 high | cyan |
| t-a4 | ACT_TITLE_CARD | ACT IV / THE LOST YEARS | 1704.0 | 5.0 | — | cyan |
| cmp-yearsserved | SPLIT_COMPARE | YEARS SERVED / "FOUR: ~6–7 YRS EACH" ↔ "KOREY WISE: ~13 YRS" / "TRIED AS AN ADULT AT 16" | 1875.0 | 6.5 | CP19 high(hedged ~) | cyan |
| t-a5 | ACT_TITLE_CARD | ACT V / THE CONFESSION & THE DNA | 2272.0 | 5.0 | — | cyan |
| c-twodays | CENTER_STACK | APRIL 17, 1989 / TWO DAYS BEFORE · THE SAME PART OF THE PARK · REYES IS BELIEVED TO HAVE ATTACKED THERE | 2340.0 | 6.0 | CP22 medium→"believed to" | cyan |
| q-alone ★reserved | QUOTE_CARD | MATIAS REYES · 2002（**verified-verbatim ロック時のみ活性・それまで CENTER_STACK "HE ACTED ALONE" / "DNA CONFIRMED ONE ATTACKER"**） | 2560.0 | 6.5 | CP24 high | cyan |
| t-a6 | ACT_TITLE_CARD | ACT VI / EXONERATION & RECKONING | 2823.0 | 5.0 | — | **dawn-amber(first)** |
| c-vacated | CENTER_STACK | DEC 19, 2002 / VACATED — ALL FIVE, ALL COUNTS | 2860.0 | 6.0 | CP27 high | **dawn-amber** |
| m-41m | MONEY_STACK | ROUGHLY / $41,000,000 / NEW YORK CITY, 2014 — ABOUT $1M PER YEAR LOST | 3045.0 | 7.0 | CP30 high(hedged ~) | **dawn-amber** |
| c-state39 | CENTER_STACK | 2016 · NEW YORK STATE / REPORTEDLY ~$3.9 MILLION MORE | 3115.0 | 5.5 | CP31 medium→"reportedly" | **dawn-amber** |
| c-salaam | CENTER_STACK | 2023 / YUSEF SALAAM · ELECTED TO THE NYC COUNCIL | 3270.0 | 5.5 | CP33 high | **dawn-amber** |
| t-a7 | ACT_TITLE_CARD | WHAT A CONFESSION IS WORTH | 3308.0 | 5.0 | CP34 high | cyan/bone |

### Tier B — BESPOKE AE SET-PIECES 12 moments（★NEW layouts・implemented + dryrun + allowlisted）
**8 distinct 新 layout**（REC_LIGHT/SCALE_TIP/HERO_TIMELINE/NAME_WALL は 2× 使用で 12 moments）。各 5–10s・choreography は §7.3。

| # | layout（builder fn） | moment / 幕 | anchor(s) | dur | accent |
|---|---|---|---:|---:|---|
| B1 | `DNA_LADDER`（`buildDnaLadder`） | Act5 climax・**the signature comp** | 2695.0 | 10.0 | cyan（FLOOD） |
| B2 | `STAT_RESOLVE`（`buildStatResolve`） | Act5・one-in-billions odometer | 2740.0 | 7.0 | cyan |
| B3 | `CARD_STACK`（`buildCardStack`） | Act2・five-confession house of cards | 960.0 | 7.0 | cyan |
| B4 | `REC_LIGHT`-off（`buildRecLight`,"off"） | Act2・unrecorded hours | 470.0 | 5.0 | cyan(dim) |
| B5 | `REC_LIGHT`-on（`buildRecLight`,"on"） | Act6 reform・**off→on** | 3165.0 | 6.0 | **dawn-amber** |
| B6 | `SCALE_TIP`-wrong（`buildScaleTip`,"confession"） | Act3・tips wrong way | 1445.0 | 6.0 | cyan |
| B7 | `SCALE_TIP`-right（`buildScaleTip`,"evidence"） | Act6・rights itself | 2985.0 | 6.0 | **dawn-amber** |
| B8 | `HERO_TIMELINE`-intro（`buildHeroTimeline`,phase1） | Act1・1989 introduced | 120.0 | 7.0 | cyan |
| B9 | `HERO_TIMELINE`-resolve（`buildHeroTimeline`,phase3） | Act6・→2002→2014 resolved | 3020.0 | 9.0 | **dawn-amber** |
| B10 | `NAME_WALL`-rise（`buildNameWall`,"names"） | Act2・five names+ages rise | 700.0 | 7.0 | cyan |
| B11 | `NAME_WALL`-close（`buildNameWall`,"exonerated"） | Act7 close・re-inscribe | 3600.0 | 9.0 | **dawn-amber** |
| B12 | `SIGNATURE_ERASE`（`buildSignatureErase`） | Act6 vacatur・**before/after w/ DNA_LADDER** | 2895.0 | 6.0 | **dawn-amber**(resolve) |

> **reserve（storyboard が peak を surface したら同じ dryrun+allowlist 手順で実装）:** `HEADLINE_WALL`（Act3・~1180s）／`INTERROGATION_ROOM`（hook/Act2 establishing・~445s）／`HERO_TIMELINE`-extend（Act4・~2205s・phase2）。使う場合のみ実装・dryrun・allowlist 追加。
> **★anchor は body-relative・単調増加・AE↔AE と AE↔figures が1秒も重ならない**（HERO_TIMELINE の in-film `timeline` figures とは時刻を分離）。DNA_LADDER(B1 2695–2705)・STAT_RESOLVE(B2 2740–2747) は重ならない。

## 7.3 Tier-B set-piece の choreography（DESIGN §3.2.1 と一致・layers/keyframes/easing/motion-blur）

**B1 `DNA_LADDER`（~10s・the film's thesis）** — (1)INK bg (2)冷たい lab scrim (3)**5 lanes**（boys）の gel band ladder：各 lane 縦の rung 群、0.0–2.0s で 1本ずつ `scaleY 0→1`（origin bottom・stagger 0.18s/lane・cyan **dim** op40）＝**NO MATCH**（rung がずれる）(4)0.2s hold (5)2.5–4.0s **Reyes lane** が右から slide-in（`translateX +260→0`・`motionBlur`・cyan bright）→ 5 lane の空きに **snap-align**（`position` key・`ease inf 90`）(6)4.0–5.5s 単一 band が pulse（`scale 1.0→1.12→1.0`）(7)5.5–7.5s **cold-cyan FLOOD**（全画面 cyan solid `opacity 0→70→24`・ADD blend）(8)7.5–10s sub "1 IN 6 BILLION · A SINGLE MATCH"（measured-fit）mask 切れ上がり・hold ≥1.2s。CP24 high・abstract・no crime imagery。

**B2 `STAT_RESOLVE`（~7s・odometer）** — 大 numeric odometer `0 → 6,000,000,000`（Python が全表示文字列 precompute・JSX は算術しない・**`group:true`＝桁区切りする**）。0.6–2.0s ease-out-cubic count-up（`motionBlur`・scale 46→112→100 overshoot settle）→2.0s "1 IN 6 BILLION" label mask 切れ上がり→hold ≥1.2s。cyan・CP24。**★これは billions＝群化する（`group:true`）。YEAR を出す card だけ `group:false`**（§9）。

**B3 `CARD_STACK`（~7s・house of cards）** — 5枚 confession page（判読不能 smear・object）が 0.0–2.5s で 1枚ずつ下から stack（`translateY 80→0`・`rotateZ ±3°` 交互・stagger 0.35s・`motionBlur`）。各 page に短い `arrow`（"the others already named you"）が次を指す（`scaleX 0→1` draw）。3.0–4.5s **DNA report** が stack 下へ slide-in（cyan edge）→全 stack 微 tilt（`rotateZ 0→5°`）＝no foundation。4.5–7s "NO FOUNDATION" label。cyan・CP10/CP12。

**B4/B5 `REC_LIGHT`（used 2×・off→on）** — 中央に REC dot（circle+ring）＋"REC" label（Oswald）。**off**：dark grey・0.0–1.0s 一度 tick（`scale 1.0→1.15→1.0`・点かない）・sub "THE CAMERA WAS OFF"・cyan(dim)。**on**：dot dark→**illuminate**（`fillColor` を dawn-amber へ key＋glow `opacity 0→60`・`motionBlur`）・sub "RECORD THE WHOLE INTERROGATION"・**dawn-amber**。CP34。HOOK の OFF signature を reform で反転。

**B6/B7 `SCALE_TIP`（used 2×・confession vs evidence）** — 天秤（beam+2 pan）。**confession**：0.5–2.5s beam が confession pan 側へ `rotateZ 0→-14°`（weighted ease・`motionBlur`）＝wrong way・cyan。**evidence**：beam が DNA pan 側へ `rotateZ +14→0→-2°` で righting・**dawn-amber**。pan の物体は判読不能象徴・**中立**（どちらが正義かを断じない）。

**B8/B9 `HERO_TIMELINE`（recurring spine）** — 横 spine line `scaleX 0→1`（origin-left・`ease inf 80`）draw、node が year で pop（`scale 0→1`・`motionBlur`）。**intro**：node "1989" のみ点灯・cyan・"THAT NIGHT"。**resolve**：spine 右へ extend、node **1989 → 2002 → 2014** が stagger 0.5s で点灯・最後が **dawn-amber**・"VACATED · SETTLED"。**★全 year node は `group:false`**（"1,989" にしない）。CP03/CP27/CP30。in-film `timeline` figures とは別物・時刻分離。

**B10/B11 `NAME_WALL`（used 2×・the renaming）** — 5行の name+age。**names**：0.0–3.0s 1行ずつ mask 切れ上がり（`translateY 110%→0`・stagger 0.4s・Anton・cyan）＝"McCRAY 15 · RICHARDSON 14 · SALAAM 15 · SANTANA 14 · WISE 16"（CP05）。**exonerated**：既存 5 name hold→上に "THE EXONERATED FIVE" が **dawn-amber** で mask 切れ上がり＋accent underline `scaleX 0→1` wipe＝renaming。CP05/CP32。**複数値は別レイヤー（改行禁止）。**

**B12 `SIGNATURE_ERASE`（~6s・vacatur）** — (1)INK bg (2)confession page（判読不能 smear） (3)署名 line を **un-write**：0.5–4.0s stroke 群が末尾→先頭へ 1本ずつ消える（`trimPath` 風 mask reveal 反転・stagger 0.12s/stroke・`motionBlur`）＋ink particle が上へ lift-away (4)4.0–5.0s page blank (5)5.0–6.0s "VACATED — ALL FIVE, ALL COUNTS" label mask 切れ上がり・**cyan→dawn-amber へ色 key**（exoneration の初暖色）・accent underline wipe。CP27。Act2 署名 motif の反転。

## 7.4 JSX layout dispatch（複製元に ADD）
複製元 `build(spec)` の dispatch に各 `else if (spec.layout === "DNA_LADDER") buildDnaLadder(comp, spec);` … を **8種 ADD**、**末尾 `else throw new Error("unsupported layout " + spec.layout ...)` は保持**。共通スタック（下→上）は cleveland 準拠：黒 bg → 象徴 still（任意）→ グレードウォッシュ(INK/MULTIPLY) → 羽根ビネット → グロー(cyan・exoneration系のみ dawn-amber) → ライトスイープ(`"ADBE Rotate Z"`=18・`motionBlur`) → 主レイヤー群(`motionBlur` を動くレイヤー個別) → `AI-assisted visualization`(R1) → head/tail 4f 黒ディップ。**★このグレードウォッシュ+羽根ビネットは各 AE カード内部（36 moments 限定・局所）のみ。最小・neutral に保ち、milky な低コントラスト wash に読めるほど強くしない（§5.9）。本編ベースへは全画面 wash を一切足さない。****全 easing は `KeyframeEase`/spatial-ease dim（cleveland `ease()`）＝等速線形ゼロ。JSX は算術しない（表示文字列は Python precompute）。**

## 7.5 ★Tier-B の実装シーケンス（CRITICAL・phantom-crash 回避の核心）
**各新 layout は必ずこの順で扱う（存在しないものを参照せず、実装して証明してから参照する）:**
```
FOR each Tier-B layout L in {DNA_LADDER, STAT_RESOLVE, CARD_STACK, REC_LIGHT, SCALE_TIP, HERO_TIMELINE, NAME_WALL, SIGNATURE_ERASE}:
  1. builder fn（buildXxx）を build_centralpark_hero_cards.py に実装し、JSX dispatch に else if を追加
  2. --dryrun で L を単体レンダ:
       $PY scripts/ae/build_centralpark_hero_cards.py --dryrun --only L
       AfterFX -noui -r <dryrun jsx>  → render/_build_ok.txt を待つ → aerender で L の1コンプを焼く
  3. 焼けた mp4 を確認（解像度1920x1080・尺一致・黒でない・文字が切れていない）
  4. check_AE_layouts の allowlist に L を追加
  5. ここで初めて 本番デッキ（§7.2）で L を参照してよい
```
> **★本番デッキ生成前に 8種すべてが allowlist 入りしていること。** allowlist に無い layout を beats.json が参照したら `check_AE_layouts` が FAIL（§7.7）。**DATE_STAMP/SEAM_TRANSITION は実装しない＝allowlist に入らない＝参照しない。**

## 7.6 `scripts/validate_centralpark_beats.py`（BLOCKING・`validate_cleveland_beats.py` 複製）
1. `beats[].start` 昇順・区間非重複
2. 全 `start`/`end` が本編ナレ区間内（HOOK 0–11.5 と ENDCARD 末尾9s に重ねない）
3. `layout` が **{6 proven} ∪ {implemented+dryrun-passed Tier-B}** のいずれか（`check_AE_layouts` allowlist と同一集合）。**DATE_STAMP/SEAM_TRANSITION は FAIL。** still 必須 layout で null なら FAIL
4. `still` 非null は実在＋長辺 ≥3840px
5. 全表示文字列が §2（R-INNOCENCE/R-VICTIM/R-REYES/R-NUM/R-FACE/R-DOCHL/R-QUOTE/R-DATE/R-HEDGE）を通る
6. `verified:false` の値を要求するカードは `required:false` で除外・`required:true` なら exit 1
7. **`centralpark_film.json` の `figures[]`（§6）と AE の 36 区間が1秒でも重ならない**
8. `caption`/label に改行が含まれない
9. **AI開示レイヤーの存在（R1）** — 全カード共通スタックに `AI-assisted visualization` を焼く設定を静的確認。無ければ FAIL
10. **`dochighlight`/`DOCHIGHLIGHT`・発明引用が beats/layout 名に1件も無い（R-DOCHL/R-QUOTE）**
11. **id/layout/CP-id/anchor が §7.2 デッキと一字一致**（DESIGN §3 とも一致）
12. **年 node（HERO_TIMELINE・年 card）が `group:false`**（§9）・AE moments total = 36（Tier A 24 + Tier B 12）

## 7.7 `scripts/check_AE_layouts.py`（新規・BLOCKING）
```bash
$PY scripts/check_AE_layouts.py --ep PD-2026-050-centralpark [--json]
```
- **allowlist = EXACTLY** `{ACT_TITLE_CARD, CENTER_STACK, MONEY_STACK, QUOTE_CARD, VOTE_SPLIT, SPLIT_COMPARE}`（6 proven）`∪`（`--dryrun` 単体レンダを `_build_ok.txt` で通過済の Tier-B: `DNA_LADDER, STAT_RESOLVE, CARD_STACK, REC_LIGHT, SCALE_TIP, HERO_TIMELINE, NAME_WALL, SIGNATURE_ERASE`）。
- `beats.json` の全 `layout` が allowlist に属すこと。**allowlist 外（＝未実装 or dryrun 未通過）を参照したら FAIL（phantom）。** **`DATE_STAMP`/`SEAM_TRANSITION` が現れたら FAIL。**
- builder ソース（`build_centralpark_hero_cards.py`）に各 Tier-B layout の `else if (spec.layout === "…")` dispatch が実在することを静的確認（grep）。dispatch 無し layout を allowlist に入れない。
- 実装済み判定の根拠に **各 Tier-B の `render/_build_ok.txt`（dryrun 通過ログ）** を確認。無ければその layout は allowlist に入れない。

## 7.8 このマシン固有の罠（複製元＝FIXED版が対処済み。**1つも省くな**・Tier-B の長尺 comp にも適用）
1. `setTemporalEaseAtKey` の配列次元は spatial(Position) で 1（`if(!prop.isSpatial){...}` 分岐）
2. RS = `"最良設定"` / OM = `"H.264 - レンダリング設定を一致 - 15 Mbps"`（英語名は try/catch フォールバック）
3. TextDocument の改行は `\n` 不可。`caption`/複数値は1行・別レイヤー（SPLIT_COMPARE 左右／NAME_WALL 各行）。**幅は `sourceRectAtTime(t,false).width` 実測。** em-dash は `-`
4. `app.newProject()` は headless でハング。同名 `CENTRALPARK_` コンプを防御削除
5. ビルドは Tier-B 長尺のため **`render/_build_ok.txt` ポーリングは ≥420秒**
6. jsx 末尾で `.aep` 保存し `app.quit()`
7. `comp.motionBlur=true` だけでは無効。**動くレイヤー個別に `layer.motionBlur=true`**
8. 2Dレイヤー回転は `"ADBE Rotate Z"`（`"ADBE Rotation"` は null）
9. `inPoint` と `outPoint` の両方を設定
10. 読み込み後 `item.mainSource.conformFrameRate = 30`
11. 実行パス `C:\Program Files\Adobe\Adobe After Effects 2026\Support Files\AfterFX.exe`（実在確認済）
12. `proj.gpuAccelType = GpuAccelType.SOFTWARE`（RTX4090 でもソフトレンダ固定）
13. `getFontsByFamilyNameAndStyleName` を使うフォント厳格解決（miss は throw・allFonts[i] ラッパー unwrap）
14. **フォント文字列を PowerShell 経由の正規表現/エスケープで生成しない**（`\b` バックスペース化の実害）。Python 側で literal。**Python 先頭に `sys.stdout.reconfigure(encoding="utf-8")`**
15. **★二段レンダ（FIXED版の核）:** JSX は AfterFX `-noui -r` で `.aep` を保存し `render/_build_ok.txt` を書くだけ（H.264 OM を exFAT H: に書くと queue=N でも 0 mp4＝**REPO path C: に出力**）。**mp4 実レンダは別工程 `aerender` で各コンプ個別。aerender 前に `.aep` mtime > `.jsx` mtime を assert。**

## 7.9 実行（★二段・36 comps）
```bash
# 段0: Tier-B 8種を実装→個別 dryrun→allowlist（§7.5）。8種すべて allowlist 入りを確認
# 段1: 本番デッキ（36 comps）の JSX 生成＋AfterFX で .aep 保存（mp4 はまだ焼かない）
$PY scripts/ae/build_centralpark_hero_cards.py
"C:/Program Files/Adobe/Adobe After Effects 2026/Support Files/AfterFX.exe" -noui \
  -r ".../episodes/PD-2026-050-centralpark/08_edit/ae_hero/centralpark_hero.jsx"
# render/_build_ok.txt を待つ（≥420秒）→ .aep mtime > .jsx mtime を assert
# 段2: aerender で 36 comps を個別レンダ（複製元の render ループを踏襲・長時間）
"C:/Program Files/Adobe/Adobe After Effects 2026/Support Files/aerender.exe" \
  -project ".../08_edit/ae_hero/centralpark_hero.aep" -comp "<id>" -output ".../render/<id>.mp4"   # 各カード
# 段3: 基底 mp4（narration+BGM・OFF=11.5）→ AEカード合成
$PY scripts/build_centralpark_bgm_real.py     # OFF=11.5
$PY scripts/ae/composite_centralpark_hero.py
```

**コンポジタ（`composite_centralpark_hero.py`＝`composite_caniglia_hero.py` 複製）:**
- `BASE = 08_edit/centralpark_final_bgm.v001.mp4`（`build_centralpark_bgm_real.py` が生成・**film_offset 11.5**）／`OUT = 08_edit/centralpark_final_bgm.v002_ae.mp4`（**v001 を絶対に上書きしない**）。
- **SKIP4条件を1行も削らない:** (1)`render/<id>.mp4` 不在 (2)解像度≠1920x1080 (3)実測尺 `< dur-0.3` (4)`film_offset_sec + beat.end > base_dur`。**何枚 SKIP したかを stderr に必ず出す。**
- ffmpeg `overlay=0:0:eof_action=pass:enable='between(t,start,end)'`（blend_mode が screen/multiply の時のみ `blend`）／`-c:v libx264 -preset slow -crf 16 -pix_fmt yuv420p -colorspace bt709 -c:a copy`。**film_offset 11.5 を適用**（body-relative→absolute）。
- **★合成で全編に渡る haze/fog/blur/scanline フィルタを一切足さない（§5.9）。** AE カードは指定区間にだけ overlay され、全画面 wash を持ち込まない。実写ストックの neutral カラーマッチ（§5.8(d)）は conform 時（§CODEX_A 10.1）or footage `treatment` で適用済みとし、composite では追加の全画面グレードを掛けない。
- 出力後 `probe_dur(OUT)` でベースとの尺差 ≤0.5秒を確認。

**BGM（`build_centralpark_bgm_real.py`＝`build_caniglia_bgm_real.py` 複製・OFF=11.5）:** 完成 mp4 **-14.0 LUFS**（-16〜-12）・true peak ≤-1.0 dBTP・VO -18.0・BGM(VO下) -22.0・(VO無) -17.0・ambient -30.0・ducking 5.0dB/attack120ms/release450ms。章 BGM は 1章1トラック（HOOK 低弦の不解決＋単一 metallic tick＝完全無音に近い restraint・digital 無音にはしない／ACT5 DNA hinge で唯一 raise／ACT6 REC-ON/dawn で暖色に開く）。最長無音 <25s（`bgm_present`）。**HOOK 無音・意図 breath 区間に字幕キューを置かない。**

---

# 8. 字幕（`scripts/gen_captions_centralpark.py`＝`gen_captions_cleveland.py` 複製）
- `internal_split()`/`chunk_sentence()`/`from fix_caption_dangling import NO_DANGLE_END, wrap as safe_wrap` を**そのままコピー**（語リストを書き直さない）。
- 入力は **narration_index の各チャンク文**（`--narr`）。**字幕テキストは台本本文と1:1対応**・verbatim・構文境界で分割するだけ。**タイミングは narration_index の start/end のまま**（コンポジタ側で offset）。
- `ABBR` に `U.S.`/`v.`/`Mr.`/`Ms.`/`No.`/`Dec.`/`Apr.` 等（`Dec. 19, 2002`・`Apr. 19, 1989` で文を切らない）。
- 通すゲート `check_caption_breaks.py`（A 行末機能語0 / B 孤立キュー0 / C 句またぎ hard 0・**閾値を緩めるの禁止**）＋ `check_caption_integrity`（§10）。
- **字幕にも R-FORBID 適用**（台本 verbatim なら通る・§2.1 注意：`attacked`/`confession`/`rape`/`wilding` 単独を禁止語に足さない）。
```bash
$PY scripts/gen_captions_centralpark.py --narr episodes/PD-2026-050-centralpark/06_audio/narration_index.v001.json
$PY scripts/check_caption_breaks.py episodes/PD-2026-050-centralpark/08_edit/captions.final.v001.srt
```

---

# 9. ★年 group:false ゲート（`scripts/check_year_grouping.py`・実在・BLOCKING）
```bash
$PY scripts/check_year_grouping.py --ep PD-2026-050-centralpark [--json]
```
- **YEAR 値（1989/1990/1991/2002/2014/2016/2023 等 1000–2100 の年）を出す全 `numberticker`/`stat`/`lowerthird`（figures）と AE numeric（HERO_TIMELINE year node・年 card）は `group:false` を必ず持つ。** 無ければ FAIL（＝"1,989"/"2,001" のコンマ群化バグ・EP46/EP47 の直接実害）。
- **桁区切りが正しい大桁（6,000,000,000 / 41,000,000 / 3,900,000 / 85,000）は `group:true`（既定）**＝ここに `group:false` を付けると "6000000000" になるので付けない。
- `check_year_grouping.py` が figures[] と beats.json の両方を走査する（無ければ本ゲート実装時に beats.json 走査を追加）。

---

# 10. 全ゲート（**build 後に必ず全部・レンダ前 preflight・各コマンド明記**）

```bash
cd C:\Users\aab15\Documents\prime-documentary ; PY=./.venv/Scripts/python.exe

# --- Preflight（課金・レンダ前） ---
# 0. 語数（★LONGFORM・12分 2,141 cap ではない・cap ≈10,900）
$PY scripts/check_script_length.py episodes/PD-2026-050-centralpark/03_script/script.en.v001.md --longform --json
#    → 10,715 語が band [10,500, 10,900] 内（--longform 未実装なら --cap 10900 相当を渡す）
# 1. 事実性/7制約（EP50固有・正確性ゲートはこの1本）
$PY scripts/check_centralpark_facts.py --json
# 2. 契約バリデータ
$PY scripts/validate_centralpark_beats.py
$PY scripts/check_centralpark_asset_manifest.py --assets episodes/PD-2026-050-centralpark/05_visuals/asset_manifest.v001.json
$PY scripts/check_AE_layouts.py --ep PD-2026-050-centralpark
# 3. 年 group:false
$PY scripts/check_year_grouping.py --ep PD-2026-050-centralpark

# --- Post-build（final 前） ---
$PY scripts/check_asset_reuse.py     remotion/src/data/centralpark_film.json    # factory≤1/motion≤2/still≤2/first-use≥0.70（設計0.8621）
$PY scripts/check_motion_density.py  --ep PD-2026-050-centralpark                # ≥151 beats/≥2.5min/variety≥6/dochighlight=0（設計165/2.745/15）
$PY scripts/check_animation_mix.py   --ep PD-2026-050-centralpark                # still-share≤0.45（設計0.4353）/motion-cov≥0.45（設計0.5647）
$PY scripts/check_caption_breaks.py  episodes/PD-2026-050-centralpark/08_edit/captions.final.v001.srt
$PY scripts/check_caption_integrity.py --ep PD-2026-050-centralpark              # ナレ一致≥99%/カバー≥95%/CPS≤17/ズレ≤120ms
$PY scripts/check_visual_asset_qc.py --ep PD-2026-050-centralpark                # 全 still/factory/motion 目視QC・black frame 0・R2 no-face
$PY scripts/check_padding.py         --ep PD-2026-050-centralpark --json
$PY scripts/preflight_render_gate.py --ep PD-2026-050-centralpark                # machine state・public_slim ディスク・durationInFrames assert

# --- Render（LONG・数時間・想定内） → BGM → AE 合成 ---（§12）
# --- 本編最終受入（episode番号は★位置引数・--ep ではない） ---
$PY scripts/check_final_acceptance.py 50 \
  --render episodes/PD-2026-050-centralpark/08_edit/centralpark_final_bgm.v002_ae.mp4 --emit-receipt
```

> **★ゲート入力規約:** density/mix/年/AE_layouts/caption_integrity/visual_qc/padding/preflight は **`--ep PD-2026-050-centralpark`**。asset_reuse は film.json 位置引数、caption_breaks は srt 位置引数、script_length は script 位置引数。**`check_animation_mix` は `04_scenes/premium_beatsheet.v*.json` を優先するので B の beatsheet に `premium_` を付けない（§5.6）。**
> **全て exit 0 でなければ `package_ready` にしない。自己申告QCは無効。QC基準を書き換えて通すのは禁止。**

| ゲート | EP50 目標値 |
|---|---|
| `check_script_length`（LONGFORM） | 10,715 語 ∈ [10,500, 10,900]（12分 2,141 cap ではない） |
| `check_centralpark_facts` | violations 0（R-INNOCENCE/R-VICTIM/R-REYES/R-NUM/R-FACE/R-DOCHL/R-QUOTE・hedged 断定なし） |
| `check_asset_reuse` | factory≤1/motion≤2/still≤2・first-use **0.8621** |
| `check_motion_density` | **165** beats / **2.745**/min / variety **15**（floor 151/2.5/6・dochighlight 0） |
| `check_animation_mix` | still-share **0.4353**（cap0.45）/ motion-cov **0.5647**（floor0.45） |
| `check_AE_layouts` | 全 layout ∈ {6 proven}∪{8 dryrun済 Tier-B}・phantom 0・DATE_STAMP/SEAM_TRANSITION 0 |
| `check_year_grouping` | 年 figure/AE すべて `group:false`（"1,989" 0件） |
| `validate_centralpark_beats` | AE 36（TierA24+TierB12）↔ figures 165 非重複・id/layout/CP-id/anchor 一致 |
| `check_caption_breaks`/`check_caption_integrity` | 行末機能語0/孤立0/hard0・ナレ一致≥99%・CPS≤17・ズレ≤120ms |
| runtime | ~60:27（provisional 108,795f・**FINAL は実測 TTS**） |

---

# 11. OP バンパー `OpeningCentralpark`（独立成果物・fps60/1920x1080/180f）
本編（`Ep50Centralpark`）の OP は `Bookends.tsx` の `BrandOpening` のまま（フォーク禁止）。`OpeningCentralpark` は独立タイトルバンパー（`out/centralpark_opening.mp4`・Shorts/予告用・本編に焼き込まない）。
- Composition: `id="OpeningCentralpark"` / 1920×1080 / fps60 / 180f（=3.0秒）/ component `remotion/src/compositions/OpeningCentralpark.tsx`。
- **依存 `@remotion/motion-blur`**（未導入時のみ `cd remotion && npm i @remotion/motion-blur`）。`remotion.config.ts` は正典値（png/h264 libx264/CRF16/yuv420p/bt709/aac320k/全コア並列/angle）＝**一致確認のみ・書き換えない**。
- **秒数ベース（fps60・フレーム直書き禁止・全て `Math.round(fps*秒)`）・等速線形1箇所も禁止・opacity 単独禁止**（全 opacity が translateY/scale/scaleX と対）・複数要素は 2–4f スタッガー・速い動きは `Trail` でモーションブラー・テキストは `overflow:hidden`+translateY マスク切れ上がり・主役裏に最低3レイヤー（グラデ背景/グリッド/グロー）。
- props: `{ title:string; subtitle:string; accent:string; hasLogo:boolean }`。`remotion/props/centralpark.json` = `{ "title":"THE EXONERATED FIVE", "subtitle":"FIVE CHILDREN. A ROOM. A CONFESSION THE DNA ERASED.", "accent":"#2F9FC4", "hasLogo":true }`。
- **accent は必ず `#2F9FC4`**（他話色流用は BLOCKER）。ルート bg は INK `#0A0A0C`。title/subtitle も §2 検査対象（R-INNOCENCE/R-VICTIM/R-FACE）。
```bash
cd remotion && npm run studio      # OpeningCentralpark を 0→180f スクラブ目視
npx remotion render OpeningCentralpark out/centralpark_opening.mp4 --props=./props/centralpark.json
```

---

# 12. staging & render（★EP45 空 public_slim / EP38 50GB-copy trap の防止）
```bash
# public/centralpark → public_slim/centralpark へ全メディア（img/factory/motion/audio/overlay + 各 <stem>_depth.png）をコピー
#   ~1,000 distinct assets = 12分エピの ~4–5× ディスク。事前にディスクを確保。
$PY scripts/stage_cleveland_assets.py --ep PD-2026-050-centralpark 2>/dev/null || {
    mkdir -p remotion/public_slim/centralpark
    cp -r remotion/public/centralpark/{img,factory,motion,overlay,audio} remotion/public_slim/centralpark/ 2>/dev/null
    cp remotion/public/centralpark/narration.mp3 remotion/public_slim/centralpark/ 2>/dev/null
}
#   ★centralpark_film.json が参照する src と各 <stem>_depth.png が public_slim に全て在ることを両ディレクトリで確認（0-missing）
#   ★C: ENOSPC 回避：public_slim は EP50 のみに剪定（他話 slug のディレクトリを public_slim から除く）
#   ★開始前にマシン状態確認（heavy-job preflight）。~108,795 フレーム = multi-hour render（想定内・許可済）
cd remotion
npx remotion render Ep50Centralpark out/centralpark.mp4 --public-dir=public_slim --concurrency=4
cd ..
```
Root.tsx 登録（`Ep47Atwater`/`Ep45Cleveland` の形）:
```tsx
import centralparkFilm from './data/centralpark_film.json';
<Composition id="Ep50Centralpark" component={CaseFilm}
  durationInFrames={caseFilmDurationInFrames(centralparkFilm as unknown as FilmData, BRAND.video.fps)}
  fps={BRAND.video.fps} width={BRAND.video.width} height={BRAND.video.height}
  defaultProps={{ data: centralparkFilm as unknown as FilmData, seriesLabel: 'PRIME DOCUMENTARY',
    title: 'The Exonerated Five', subtitle: '...' }}/>
```
> **id は正確に `Ep50Centralpark`。** `hookSeconds==8.0` を assert（0 で 8s desync）。durationInFrames は 4項関数で再計算し **108,795（provisional）** に一致 assert（実測後に更新）。**追記後 `cd remotion && npx tsc --noEmit`（typecheck）緑を確認。** `remotion/src` に既存 `centralpark` 文字列が無い（衝突しない）ことを確認してから追記。

---

# 13. 受入（自分で exit 0 を確認してから完了報告）
§10 の全ゲートを exit 0 まで通し、`check_final_acceptance.py 50 --render .../centralpark_final_bgm.v002_ae.mp4 --emit-receipt` を PASS させる。

## 13.1 ★完成後の FULL 60分 3回アイボール（1フレーム判定禁止＝EP39-41/EP47 実害）
`centralpark_final_bgm.v002_ae.mp4` を **0→末尾まで通しで3周**実視聴（**measured across the WHOLE ~60分・sampled 1-frame 禁止**）:
- **周1 structure/カット:** 紙芝居感が無い（still 連続なし・footage 過半＝EP45 死因を潰せているか）・幕構成・AE 36 moments が全て焼き込まれている・**実写ストックが意味のあるビートに載っている（§5.8・courthouse/NYC/precinct/prison/lab 等が内容一致）・実写比率が motion の 74% を割っていない・実写と AI still が一枚の palette に読める（カラーマッチ）**・**どのフレームにも全画面の曇り/ヘイズ/スキャンラインが無い＝画像がクリアで高コントラスト（§5.9・EP48/49 の milky wash 再発なし）**
- **周2 caption-text:** 全字幕テキストが台本と一致・機能語末/孤立/hard split なし・年が "1,989"/"2,001" になっていない（**全 numberticker/stat/年 card を目視・EP47 "2,001" の再発防止**）
- **周3 audio-sync:** VO onset = **11.5s ちょうど**・hook 8.0s・BGM ducking・endcard 9s・音ズレ/字幕ズレ/尺差（base と ≤0.5s）なし
- **全周共通で必ず確認:**
  - **各 AE set-piece を1つずつ:** DNA_LADDER の cyan FLOOD と single match／STAT_RESOLVE の `6,000,000,000`（"1 IN 6 BILLION"）／SIGNATURE_ERASE の un-write→dawn-amber／CARD_STACK の house of cards／REC_LIGHT off→on／SCALE_TIP wrong→right／HERO_TIMELINE 1989→2002→2014（年が群化していない）／NAME_WALL 5名→THE EXONERATED FIVE
  - **各 numberticker/stat の年が group:false で正しく描画**（1989 が "1,989" でない・§9）
  - **R-INNOCENCE:** 5人が事件に関与したと匂わせる画面/字幕がどこにも無い・Armstrong は却下枠のみ（or 不使用）
  - **R-VICTIM/R-REYES:** 被害者の imagery/naming が記録以上に無い・暴行が描写/再現されていない・Reyes が established facts のみ
  - **R-FACE（owner 改定）:** 匿名・非識別の人物（H シリーズ・顔は背向き/影/ソフト）は可だが、**5人・Meili・Reyes・Trump・実在の刑事/判事/検事に「似た」顔/肖像が1つも無い**・被害者の描写と暴行 imagery が1つも無い・少年が有罪/加害に見える画がない・Trump ad art が再現されていない
  - **R-DOCHL:** `dochighlight`（黒バー/box/underline）が figures/AE に1本も無い
  - **R-QUOTE:** 引用符に入っているのは検証済み逐語＋帰属のみ（発明引用ゼロ・`q-alone` は verbatim ロック時のみ活性）
  - 生成ビジュアル表示中は `AI-assisted visualization` が右下常時（**AE 36 moments の表示中も**開示が見える・R1）
  - accent が cold cyan `#2F9FC4`（dawn-amber は exoneration/close のみ・他話色が紛れていない）

---

# 14. 絶対にやらないこと
- **EP1〜49 のファイル・素材・`scripts/*{他slug}*.py` に触らない**（読み取り可）。レーンを分離する。**accent に他話色を使わない**（cyan `#2F9FC4`＝`[0.184,0.624,0.769]` / dawn-amber は exoneration/close のみ）。
- **スレッドAの所有ファイル（§0.2.1）に書かない**（`05_visuals/` `05_stock/` `remotion/public/centralpark/` `H:\...\ai\centralpark\`）。B の provenance は `04_scenes/` に書く。
- **課金ジョブを起動しない**（TTS / 課金画像API / YouTube アップロード）。narration_index は実測版を消費するだけ。
- **公開済み・出荷済み mp4 を上書き・再レンダしない**（AE 合成出力は必ず `v002_ae`・base は `v001`）。
- **台帳（§2）に無い数値を焼かない**（$580,000 再発防止）。**hedged（$85,000/$3.9M/$41M/~13yr/CP17 verdict/CP22）を hedge 語なしで断定表示しない。**
- **`FigureSpec` の `kind` を推測で書かない**（§6.2 実在小文字値のみ・`comparebars`→`compbars`・`VoteTally`→`votetally`）。**`dochighlight` を1本も使わない（R-DOCHL）。quote/votetally は不使用。**
- **★DATE_STAMP / SEAM_TRANSITION を emit/実装しない**（複製元非実装＝`else throw` でクラッシュ）。**Tier-B 新 layout は「実装→dryrun→allowlist→参照」の順以外で参照しない**（phantom-crash 回避）。
- **★年を `group:false` にし忘れない**（1989/2002/2014 が "1,989"/"2,001" になる＝EP46/EP47 実害・§9）。桁区切り数値（6B/$41M）は `group:true`。
- **★build_centralpark_film.py は manifest の `factory[]`(485)/`motion[]`(85) を `public_path` で全読込し、空 or 期待数違いなら exit 1**（EP45 紙芝居事故防止）。
- **★AEカードは二段レンダ（AfterFX が .aep 保存→別工程 aerender が mp4 を焼く）で REPO path(C:) 出力**（H: 直書きは queue>0 でも 0 mp4）。**aerender 前に .aep mtime > .jsx mtime を assert。**
- **★render 前に `public_slim/centralpark` へ全メディアを staging・EP50 のみに剪定**（C: ENOSPC 回避・両ディレクトリ 0-missing）。
- **R-INNOCENCE/R-VICTIM/R-REYES/R-FACE/R-QUOTE を破らない**（5人の関与を匂わせない・被害者/Reyes を記録以上に扱わない・**実在人物の likeness ゼロ**＝匿名の一般人は可だが 5人/Meili/Reyes/Trump/実在の刑事・判事・検事に似せない・被害者の描写と暴行 imagery なし・発明引用ゼロ・Armstrong は却下枠のみ）。
- **★実写ストックライブラリ（`H:\pd-media\assets\stock`・74動画+155静止）を放置して AI だけで組まない（§5.8・EP48/49 の burned lesson）。** 意味の合うビートに実写を優先（AI-i2v より優先）。ただし物語に合わない実写を無理に差し込まない。ストック静止を body(AI 430) レーンに混ぜない・被害者/実在人物/可読テキストを含む実写を使わない。
- **★全画面の haze/fog/曇り/vignette-wash・全フレーム scanline/CRT テクスチャを乗せない（§5.9・EP48/49 で却下された milky wash）。** 画像はクリア・高コントラスト。グレードは最小・neutral。overlay は per-beat の局所アクセントのみ。
- **スペック数値（1,160 cuts / still430/factory485/motion85 / distinct1000 / first-use0.8621 / still-share0.4353 / figures165(floor151) / AE 36(TierA24+TierB12) / hookSeconds8.0 / narrationSeconds3606.0 provisional / durationInFrames108,795 provisional）を勝手に変えない**（durationInFrames/narrationSeconds は**実測 TTS 後のみ**更新・§5.1.1）。
- **composition id は `Ep50Centralpark`**・typecheck 緑を確認。**PowerShell 経由で正規表現/エスケープを生成しない**（`\b` バックスペース化の実害）。
```
