# EP43 caniglia — Codex スレッドB「実装」引き継ぎプロンプト v001

> **このファイルは単体で完結している。他のファイルを読まなくても着手できる。**
> 並行して走っているスレッドA（素材生成）のファイル `EP43_caniglia_CODEX_A_*.md` は**読まない**。
> 設計書 `EP43_caniglia_DESIGN*.md` も**読まない**（必要な数値はすべて本書に転記済み）。
> `EP43_caniglia_PRODUCTION_SPEC.v001.json` の数値は本書に転記済み。**あなたはこれを書き換えない。**

```
あなたは Prime Documentary（YouTubeドキュメンタリーチャンネル）の制作エンジニアです。
リポジトリ: C:\Users\aab15\Documents\prime-documentary
Python:     C:\Users\aab15\Documents\prime-documentary\.venv\Scripts\python.exe
メディア:   H:\pd-media
担当:       EP43 / Episode ID: PD-2026-043-caniglia / slug: caniglia
```

**題材:** *Caniglia v. Strom*, 593 U.S. 194 (2021), No. 20-157（argued 2021-03-24 / decided 2021-05-17）。
合衆国最高裁が**全員一致 9対0**で、「community caretaking（地域見守り）」に**住居へ入る独立した無令状例外はない**と判示し、
第1巡回区の判断を**破棄・差戻し（vacate & remand）**した実在の最高裁判決（**制度説明としてのみ**扱う）。
主題人物は **Edward Caniglia**（Cranston, RI の**存命の私人 = R2**）。2015年8月の口論の翌日、妻の要請で警察が
**非緊急回線の安否確認（welfare check）**に訪れ、本人が精神鑑定へ搬送された後、警官が**無令状で拳銃2丁を押収**した。
最高裁はこの押収の根拠だった caretaking 論を住居について封鎖したが、**Caniglia の全面勝訴でも事件終結でもない（差戻し）。**

> **★EP42 young / EP41 Thompson との決定的な違い:** EP41 は「隠された報告書＋最高裁が5-4で賠償を覆した」、EP42 は「誤住所踏み込み（Young）＋ Hudson が救済を薄くした射程」。
> **EP43 は「一晩の私的危機（Caniglia）＋『助けに来た』が無令状の押収に化けた」を、閉じた玄関ドアと温存された緊急の扉という二枚の戸で接続する。**
> `Supreme Court` / `Fourth Amendment` は禁止語ではない（Caniglia は実在の本案判決）。だが **§2 の正確性6制約が全出力を律する。**
> **「警察は令状なしに家に入れない」断定・「全面勝訴／事件終結」断定・Cady=家 の混同・メンタルヘルスの扇情・Edward Caniglia の顔/肖像/身体 を一切出さない（プロンプト・カード・図表・タイトル・字幕・props すべて）。988 を概要欄に入れる。**

---

# 0. このスレッドの責務・境界・完了条件

## 0.1 このスレッド（B）の責務 — **コード律速。素材を1点も待たずに全部書ける。**

| # | 作業 | 成果物 |
|---|---|---|
| B-1 | エピソードディレクトリと `manifest.json` | `episodes/PD-2026-043-caniglia/**` |
| B-2 | 境界契約マニフェストの**消費側**バリデータ＋スタブ素材生成 | `scripts/check_caniglia_asset_manifest.py` / `scripts/make_caniglia_stub_assets.py` |
| B-3 | スタブ narration_index 生成器（TTS 不要で通しを回す鍵） | `scripts/make_caniglia_stub_narration.py` |
| B-4 | 事実台帳 F-ID と 6制約ゲート（**EP43固有・BLOCKING**） | `scripts/check_caniglia_facts.py` |
| B-5 | `caniglia_film.json` ビルダ（**asset_map→manifest変換＋beatsheet生成／footage混在**） | `scripts/build_caniglia_film.py`（**`build_young_film.py` を複製**） |
| B-6 | beats バリデータ（AEとRemotionの区間衝突検査＋ledger／6制約） | `scripts/validate_caniglia_beats.py` |
| B-7 | **構文境界で切る字幕生成器** | `scripts/gen_captions_caniglia.py`（**`gen_captions_young.py` を複製**） |
| B-8 | **After Effects カード**のビルダとコンポジタ | `scripts/ae/build_caniglia_hero_cards.py` / `scripts/ae/composite_caniglia_hero.py`（**`*_young_*` を複製**） |
| B-9 | 本編 BGM ミックス（AEカード合成の基底 mp4 を生成） | `scripts/build_caniglia_bgm.py`（**`build_young_bgm.py` を複製**） |
| B-10 | Remotion 本編コンポジション登録 `Ep43Caniglia` | `remotion/src/Root.tsx` |
| B-11 | OP バンパー `OpeningCaniglia`（fps60/1920x1080/180f） | `remotion/src/compositions/OpeningCaniglia.tsx` |
| B-12 | サムネ3案 | `remotion/src/compositions/CanigliaThumbnails.tsx` |
| B-13 | **スタブでの通しドライラン** | `episodes/PD-2026-043-caniglia/08_edit/_dryrun/**` |

## 0.2 もう一方のスレッド（A）との境界 — **接続点はただ1ファイル。**

```
episodes/PD-2026-043-caniglia/05_visuals/asset_manifest.v001.json
   ↑ Aが生成（唯一の生産者）        ↓ Bが消費（唯一の消費者）
```

**Bはこのファイル以外のAの中間生成物を読まない。そして Bはこのファイルが無くても完走できる。**
`make_caniglia_stub_assets.py` が**まったく同じスキーマの** `asset_manifest.stub.v001.json` を作るので、
Bはそれで全パイプラインを通す。

> **★絶対条件: スタブと本番でコードパスを分岐させてはならない。**
> `build_caniglia_film.py --assets <path>` は渡されたマニフェストを読むだけで、`is_stub` の値によって
> **処理を変えない**（`is_stub` はログと受入判定にだけ使う。カット組み立てロジックには一切使わない）。

> **★1シーン1枚・バリエーション0（ブリーフ§1）の B 側での意味:** A は同一ショットの `_01/_02/_03` を**作らない**。
> したがってマニフェストの `stills[]` は **85本すべてが固有プロンプトの distinct**（`counts.still_body>=85`）。
> A の `ai_prompts.v001.md` は **still 85行＋i2v種 16行 = 総生成画像 101枚**（各1回）。**still カット 101本という数字とは別物**（偶然どちらも 101）。
> B は編集上、still を **各最大2回**まで再使用してカット101本を組む（cap 2 の"再利用"であって"バリエーション"ではない）。
> **B は `--variants` という語をどのコマンド・ログにも書かない**（それは A の SDXL 側の概念で、しかも 1 固定）。

### 0.2.1 ファイル所有権（これを破ると並行作業が壊れる）

| パス | 所有 | Bの権限 |
|---|---|---|
| `episodes/PD-2026-043-caniglia/manifest.json` | **B** | 読み書き |
| `episodes/PD-2026-043-caniglia/{00_topic,01_research,03_script,04_scenes,06_audio,08_edit,09_package,approvals,events}/**` | **B** | 読み書き |
| `remotion/src/**` `remotion/props/**` | **B** | 読み書き |
| `remotion/public/caniglia_dryrun/**` | **B** | 読み書き（スタブ素材の staging 先） |
| `scripts/*caniglia*.py` / `scripts/ae/*caniglia*.py`（§0.3） | **B** | 新規作成 |
| **`episodes/PD-2026-043-caniglia/05_visuals/**` `05_stock/**`** | **A** | **読み取りのみ。書くな** |
| **`H:\pd-media\assets\ai\caniglia\**` / `ai_video\caniglia\**`** | **A** | **読み取りのみ。書くな** |
| **`remotion/public/caniglia/{img,factory,motion,overlay}/**`** | **A** | **読み取りのみ。書くな** |
| `EP43_caniglia_DESIGN*.md` / `EP43_caniglia_CODEX_A_*.md` | **設計/Aスレッド** | **触るな** |
| `EP43_caniglia_PRODUCTION_SPEC.v001.json` / `EP43_caniglia_script.en.v001.md` | **上流** | **読み取りのみ。書くな** |
| `episodes/PD-2026-039-*/**` … `PD-2026-042-*/**` / それらの素材 | **他エージェント** | **絶対に触るな** |

> **B は `remotion/public/caniglia/` に書かない。** スタブは **`remotion/public/caniglia_dryrun/`** に置く。
> 本番マニフェストが来たら `--assets` を差し替えるだけで `caniglia/` を参照するようになる。

## 0.3 B が新規作成するスクリプト（これ以外を新規に作らない。既存を改変しない）

| パス | 役割 | 手本（**改変せず読んで複製→パス/定数だけ差し替え**） |
|---|---|---|
| `scripts/check_caniglia_asset_manifest.py` | §3.3 消費側バリデータ | `scripts/check_young_asset_manifest.py` |
| `scripts/make_caniglia_stub_assets.py` | §3.4 スタブ素材＋スタブマニフェスト＋スタブ黒ベース | `scripts/make_young_stub_assets.py` |
| `scripts/make_caniglia_stub_narration.py` | §4.4 スタブ narration_index | `scripts/make_young_stub_narration.py` |
| `scripts/check_caniglia_facts.py` | §2 6制約＋台帳（BLOCKING・**正確性ゲート名はこの1つに統一**） | `scripts/check_young_facts.py` |
| `scripts/build_caniglia_film.py` | §5 film.json＋manifest＋beatsheet＋SRT | **`scripts/build_young_film.py`** |
| `scripts/validate_caniglia_beats.py` | §7.9 不変条件 | `scripts/validate_young_beats.py` |
| `scripts/gen_captions_caniglia.py` | §8 構文境界字幕生成器 | **`scripts/gen_captions_young.py`** |
| `scripts/ae/build_caniglia_hero_cards.py` | §7 AEカードビルダ | **`scripts/ae/build_young_hero_cards.py`** |
| `scripts/ae/composite_caniglia_hero.py` | §7.10 コンポジタ | **`scripts/ae/composite_young_hero.py`** |
| `scripts/build_caniglia_bgm.py` | §7.10 基底 mp4（narration＋BGM ミックス） | `scripts/build_young_bgm.py` |

> **`build_caniglia_film.py` の複製時に差し替える定数:** `ASSET_MAP`（マニフェスト→cut 変換テーブル）・`NARR`（narration_index 既定パス）・
> `FACTORY_SEL`（factory 選抜の参照）・`SLUG="caniglia"`・`EP="PD-2026-043-caniglia"`・出力パス群。**ロジック（best-pick / tile_window /
> allocate / build_figures / build_captions）は1行も変えない。**
> **既存の `scripts/gen_captions_young.py` / `build_young_film.py` 等は触らない**（他エピソードが使用中）。EP43用に**新規コピー**する。

## 0.4 完了条件（スタブだけで、全て緑になったら「実装完了」）

```bash
cd C:\Users\aab15\Documents\prime-documentary
PY=./.venv/Scripts/python.exe

# [B-DONE-1] スタブ素材・スタブ黒ベース・スタブ narration を揃える
$PY scripts/make_caniglia_stub_assets.py
$PY scripts/make_caniglia_stub_narration.py

# [B-DONE-2] マニフェスト消費側バリデータ（スタブ相手に通ること）
$PY scripts/check_caniglia_asset_manifest.py \
  --assets episodes/PD-2026-043-caniglia/05_visuals/asset_manifest.stub.v001.json

# [B-DONE-3] 字幕（スタブ narration の実文から構文境界で生成）
$PY scripts/gen_captions_caniglia.py \
  --narr episodes/PD-2026-043-caniglia/06_audio/narration_index.stub.v001.json
$PY scripts/check_caption_breaks.py \
  episodes/PD-2026-043-caniglia/08_edit/captions.final.v001.srt

# [B-DONE-4] film.json をスタブから組み立てる（footage 混在必須）
$PY scripts/build_caniglia_film.py \
  --assets episodes/PD-2026-043-caniglia/05_visuals/asset_manifest.stub.v001.json \
  --narr   episodes/PD-2026-043-caniglia/06_audio/narration_index.stub.v001.json \
  --out    remotion/src/data/caniglia_film.json

# [B-DONE-5] ★5ゲート全部（--ep 指定・animation_mix を絶対に忘れるな）
$PY scripts/check_asset_reuse.py     remotion/src/data/caniglia_film.json
$PY scripts/check_motion_density.py  --ep PD-2026-043-caniglia
$PY scripts/check_animation_mix.py   --ep PD-2026-043-caniglia
$PY scripts/check_caption_breaks.py  episodes/PD-2026-043-caniglia/08_edit/captions.final.v001.srt
$PY scripts/check_script_length.py   episodes/_planning/EP43_caniglia_script.en.v001.md --json

# [B-DONE-6] 事実性/6制約（スタブの文字列にも適用）
$PY scripts/check_caniglia_facts.py --json --dryrun

# [B-DONE-7] beats 契約（AE区間 と Remotion figures[] が1秒も重ならない）
$PY scripts/validate_caniglia_beats.py --dryrun

# [B-DONE-8] AE カードをビルド＋レンダ＋コンポジット（ドライラン出力へ）
$PY scripts/ae/build_caniglia_hero_cards.py --dryrun
"C:/Program Files/Adobe/Adobe After Effects 2026/Support Files/AfterFX.exe" -noui \
  -r "C:/Users/aab15/Documents/prime-documentary/episodes/PD-2026-043-caniglia/08_edit/_dryrun/ae_hero/caniglia_hero.jsx"
$PY scripts/ae/composite_caniglia_hero.py --dryrun

# [B-DONE-9] Remotion Studio で目視
cd remotion && npm run studio
#   → Ep43Caniglia / OpeningCaniglia / Thumb-caniglia-01..03 が出て、実際に動くこと
```

**台本は既に確定済み**（`EP43_caniglia_script.en.v001.md`・2,141語・12.0分・ロック）。したがって本番 narration_index が来たら
`--narr` を差し替え、[B-DONE-3]〜[B-DONE-8] を全部やり直す。**「スタブで通ったから本番も通るはず」は禁止。**

---

# 1. 実装前に必ず読むファイル（**推測で書くな**）

| パス | なぜ読むか |
|---|---|
| `scripts/build_young_film.py` | **複製元。** best-pick / tile_window / allocate / build_figures / build_captions をそのまま踏襲し、定数だけ caniglia に。**footage を必ず混ぜる（§0.5 の紙芝居回避）** |
| `scripts/ae/build_young_hero_cards.py` | **複製元。** `money_keys()`（Python で表示文字列を全事前計算）/ `fit_size()` / CARDS デッキ構造 / レイアウト定義 / 完了マーカーをそのまま |
| `scripts/ae/composite_young_hero.py` | **複製元。** SKIP4条件（missing / 解像度不一致 / 実測尺不足 / window past end）と ffmpeg フィルタグラフ（overlay/blend）をそのまま |
| `scripts/gen_captions_young.py` | **複製元。** `internal_split()` / `chunk_sentence()` / `NO_DANGLE_END` import をそのまま |
| `scripts/build_young_bgm.py` | **複製元。** narration＋BGM ミックスで基底 mp4 を作る経路 |
| `remotion/src/compositions/CaseFilm.tsx` | `FilmData` 型 / `caseFilmDurationInFrames` / `depthSrcOf()` |
| `remotion/src/components/FigureBeats.tsx` | `FigureSpec` の**実在する `kind` 文字列**（§6.2 の警告を必ず読め・**全小文字**） |
| `remotion/src/components/Bookends.tsx` | `OPENING_SEC` / `ENDCARD_SEC` / `BrandOpening` / `BrandEndcard` |
| `scripts/check_asset_reuse.py` / `scripts/check_motion_density.py` / `scripts/check_animation_mix.py` / `scripts/check_caption_breaks.py` / `scripts/check_script_length.py` | 通すべき5ゲートの**実際の判定ロジック**（§9） |
| `C:\Users\aab15\Documents\pino-channel\remotion\src\Opening.tsx` | §10 の OP 正典実装 |

---

# 0.5 ★★★ EP39/40/41/42 で踏んだ失敗＝最初から防ぐ（本書の全体設計はこの6点を構造で潰している）★★★

1. **紙芝居（最重要）** — 静止画100%で組むと `check_animation_mix` が FAIL する。**EP43 は最初から footage を混ぜる。**
   `check_animation_mix.compute_metrics_from_film()` は film.json の `cuts[]` を
   **`kind=="img"` → still（scene 扱い）/ それ以外 → footage（motion 扱い）** と分類する。
   → §5 の cuts 構成は **factory 93 + motion 32 の footage を最初から入れて still-share を frame ベースで ≤0.42、cut数ベースで 0.4469** にする。
2. **AEカードは密度に数えられない** — `check_motion_density` は film.json の `graphics+figures+heroCuts` **のみ**数える。
   AEカードは ffmpeg で後合成するので**1本も数えられない**。→ §6 で **film.json 側の `figures[]` を 37本**（spec floor 31 に **+6**・`graphics[]=[]`）置く。AEカードは別勘定。
3. **FigureSpec の `kind` は実在の小文字値のみ** — 大文字名（`ActTitle`/`QuoteCard`/`VoteTally` 等）は無言で描画が消える（§6.2）。`comparebars` は非在→`compbars`。
4. **台帳に無い数値を焼くな** — EP40 の生 Codex-B 出力に架空の $580,000 が入って**不採用になった実害**。
   → §2 の事実台帳 F-ID に**検証済み値だけ**を置き、`check_caniglia_facts.py` が film.json/AE/サムネ/props の全数値を台帳照合する。台帳に無い数値・`verified:false` の数値を焼いたら FAIL。
5. **字幕は台本本文と対応** — EP38 で台詞混入・「final」誤称の実害。→ §8 の字幕は **narration_index の実チャンク文をそのまま** verbatim で使う（自作しない）。
6. **レンダー前ゲート** — build 後に `check_asset_reuse` / `check_motion_density` / `check_animation_mix` / `check_caption_breaks` / `check_script_length` を**全部**通す（§9・§13）。**animation_mix を忘れるな。**

---

# 2. ★ EP43固有の正確性6制約・事実性ロック（`scripts/check_caniglia_facts.py`・BLOCKING）

> **この節に違反した成果物は、他が全て完璧でも出荷不可。** 検査対象は film.json の figures/captions、AE beats、
> サムネ、props、固定コメント、（存在すれば）マニフェストの tags/caption_hint/qc.notes の**全文字列と全数値**。
> **正確性ゲートはこの1本に統一（`check_caniglia_facts.py`）。DESIGN/CODEX_A も同名を参照する。**

## 2.1 正確性6制約（全出力に適用・違反は BLOCKER）

| # | 制約 | 許可される表現 | 禁止 |
|---|---|---|---|
| C-1 | **射程を過大化しない** | 「否定されたのは *community caretaking* の**住居**拡張だけ」「exigent circumstances / emergency aid の例外は**温存**（STILL OPEN）」「WARRANT · CONSENT · EMERGENCY」 | 「警察は令状なしに家に入れない」と**断定**する文言（カード/サムネ/字幕/props/タイトル） |
| C-2 | **9-0 ＝ 破棄・差戻し** | 「9-0」を出すなら同一カード内に限定併記「ONE EXCUSE, CLOSED」「VACATE & REMAND」「not a final victory」 | 「全面勝訴」「事件終結」「Caniglia が勝った(outright)」 |
| C-3 | **Cady ＝ 警察管理下の自動車** | 「A CAR, NOT A HOME」「a vehicle is not a house」「Cady v. Dombrowski (1973) は車・レッカー・トランクの話」 | Cady を住居の事案として提示／家と車の混同 |
| C-4 | **Edward Caniglia ＝ R2・象徴のみ** | 事件主体としての名（"Edward Caniglia sued" / "for Edward Caniglia"）。ビジュアルは食卓の拳銃・空のポーチ・救急車の赤色灯・玄関・電話・証拠タグ | 顔・肖像・身体・人物化・内面の憶測 |
| C-5 | **メンタルヘルス非扇情** | 「shoot him」は記録事実として**1回のみ・非演出**。危機は抑制。**概要欄に 988 Suicide & Crisis Lifeline** | 手段の描写・自殺念慮の内面憶測・演出的誇張 |
| C-6 | **Payton／温存例外を正確に** | 「Payton v. New York (1980)：住居への無令状立入りは **presumptively unreasonable**」「the very core … the right of a man to retreat into his own home」は **Jardines 帰属** | 「家は絶対に守られる」「a wall around your home」と**断定**／逐語引用を Payton に帰属 |
| R1 | **実在人物の顔・肖像を生成しない** | 全生成ビジュアル表示中は `AI-assisted visualization`（右下）／概要欄1行AI開示 | 認識可能な人物・読める偽公文書 |

**★禁止語（`check_caniglia_facts.py` が全文字列を case-insensitive 部分一致で検査。1件でも FAIL）:**
`full victory` / `total victory` / `complete victory` / `total win` / `won his case` / `won outright` / `case closed` / `case is over` / `case ended in his favor` / `final win` /
`warrantless entry is illegal` / `home is absolutely protected` / `police can no longer enter` / `no more welfare checks`。
> **★重要な設計注意:** 台本本文（＝字幕 verbatim）には「can never enter your home」「Not a wall around your home」など
> **否定文脈の近似語**が含まれる。上の禁止語リストは**それらと衝突しない断定形だけ**を選んである。**禁止語リストにこの近似語を足すな**
> （字幕 verbatim を巻き込んで false FAIL する）。射程・9-0・Payton の**否定/断定の別**は下の**文脈ルール**（R-SCOPE/R-VOTE99/R-PAYTON）で捕える。

## 2.2 事実台帳 F-ID（`03_script/caniglia_facts.v001.json`・**Bが台本の事実対応表から転記して作る**）

**スキーマ版:** `caniglia_facts.v1`。各 F-ID は `{"value":..., "unit":..., "verified":bool, "claim_id":"", "quote":""}`。
**台本の事実対応表（claim id C01–C25）に裏付けのある値だけ `verified:true`。裏付け無しは `verified:false`。**

| F-ID | 内容 | 使う場所 | claim |
|---|---|---|---|
| F01 | 判決日 = **2021-05-17** | fig timeline / AE date | C02 |
| F02 | 口頭弁論 = **2021-03-24** | fig timeline | C03 |
| F03 | 判決 = **9 – 0（全員一致）**・処分 = **vacate & remand** | fig votetally / AE VOTE_SPLIT（**限定併記必須・C-2**） | C04 |
| F04 | 判例引用 = **Caniglia v. Strom, 593 U.S. 194 (2021), No. 20-157** | fig lowerthird | C01 |
| F05 | 起源 = **Cady v. Dombrowski, 413 U.S. 433 (1973)**（**警察管理下の自動車**・C-3） | fig lowerthird / AE SPLIT_COMPARE | C13 |
| F06 | 下級審 = **First Circuit, 953 F.3d 112 (2020)** | fig lowerthird | C20 |
| F07 | 法廷意見執筆 = **Justice Thomas** | fig quote / AE QUOTE_CARD | C05 |
| F08 | 事件 = **August 2015 · Cranston, RI** | fig timeline / AE DATE_STAMP | C15/C16 |
| F09 | 押収 = **拳銃 2丁・無令状（no warrant）** | fig stat / AE CENTER_STACK | C18 |
| F10 | 補足 = **Roberts, joined by Breyer**（救助に令状不要） | fig stat（帰属） | C09 |
| F11 | 補足 = **Kavanaugh**（緊急救助での無令状立入は存続） | fig stat（帰属） | C11 |
| F12 | 補足 = **Alito**（red flag 法・自殺防止押収は**未決＝将来課題**） | fig lowerthird | C10/C23 |
| F13 | 巡回区分裂 = **1・5・6・8・9 が住居へ拡張／3・7 が拒否** | fig compbars | C25 |
| F14 | **Payton v. New York (1980)**＝住居への無令状立入は **presumptively unreasonable** | fig lowerthird | C14 |
| F15 | 逐語 = **Florida v. Jardines, 569 U.S. 1, 6 (2013)**（"the right of a man to retreat into his own home"） | fig quote（**Jardines 帰属・C-6/C07**） | C07 |
| F16 | **988 Suicide & Crisis Lifeline**（概要欄・endcard 連動・C-5） | endcard / 概要欄(description.txt) / 固定コメント のみ（★figures・AEカードにしない＝R-988） | C24 |
| F17 | 温存例外 = **warrant · consent · exigent circumstances (emergency aid)** | fig lowerthird / AE（STILL OPEN・C-1） | C08 |
| F18 | 別途の補足意見 = **3人が別記（Roberts+Breyer / Kavanaugh / Alito）** | fig stat（value 3・帰属） | C09/C10/C11 |

> **F03（9-0）は "VACATE & REMAND" / "ONE EXCUSE, CLOSED" 等の限定ラベルと**同一カード/payload内**で提示する（C-2）。
> 単独の勝利数として焼かない。** `check_caniglia_facts` の R-VOTE99 が照合（§2.3）。
> **F15 の逐語は Jardines 帰属（Thomas が Jardines を引用）。Payton に帰属させたら FAIL（R-JARDINES）。**

## 2.3 `check_caniglia_facts.py` の検査（exit 0=PASS / 1=FAIL / 2=スキーマ不一致）

**検査対象ファイル（この一覧をハードコード。存在するものだけ検査し、無いものは `skipped[]` に必ず明記）:**

```
episodes/PD-2026-043-caniglia/03_script/caniglia_facts.v*.json
episodes/PD-2026-043-caniglia/08_edit/ae_hero/beats.json
episodes/PD-2026-043-caniglia/08_edit/_dryrun/ae_hero/beats.json
episodes/PD-2026-043-caniglia/09_package/*.json        （title / description / thumbnail headlines）
episodes/PD-2026-043-caniglia/09_package/*.txt         （固定コメント）
episodes/PD-2026-043-caniglia/05_visuals/asset_manifest*.json  （tags / caption_hint / qc.notes）
remotion/src/data/caniglia_film.json                   （figures[] / captions[] の全文字列と数値）
remotion/props/caniglia*.json                          （title / subtitle）
```

- **R-FORBID（最優先）** — §2.1 の禁止語が対象文字列のどこかに出たら即 FAIL。**近似語（否定文脈）を巻き込まない断定形のみ**を検査（§2.1 の注意）。
- **R-LEDGER** — figures[] の `value`/`numKeys` 到達値、AE `beats[].value`/`beats[].hero`、サムネ数字に現れる**あらゆる数値**は、
  `caniglia_facts.v*.json` に `verified:true` で存在する値に**完全一致**しなければ FAIL（$580,000 実害の再発防止）。日付は年/月/日に分解して照合（F01/F02/F08 の 2015/2020/2021/1973/1980/2013、識別子 593/194/413/433/953/112/569/1/6/20-157、投票 9/0、押収 2、補足 3、988 が許可集合）。
- **R-VOTE99（C-2）** — `9-0`/`9 – 0`/`nine to nothing`/`unanimous` を含むカード・figure は、**同一 payload 内**に限定修飾
  `{"vacate","remand","one excuse","sent back","not a final","did not end his case","narrow"}` のいずれかを**必ず含む**こと。
  かつ全面勝訴語（§2.1 R-FORBID の `full victory`/`won outright`/`case closed`/`case is over` 等）と同一 payload で共起したら FAIL。
  `votetally` は **`majority:9, dissent:0`（SCOTUS の 9-0 のみ）** 許可。巡回区の分裂（5/6/8/9 vs 3/7）は `votetally` に入れず `compbars`/`stat` で表現し `label` に主体明記（R-SPLIT）。
- **R-SCOPE（C-1・積極検証・BLOCKING）** — 射程非圧縮の**肯定**検出。次を全て満たさなければ FAIL:
  (1) 温存例外の核 `exigent`/`emergency` と `warrant`・`consent` を含む「STILL OPEN」系の payload が figures か AE に**存在する**（例：F17 lowerthird / AEカード s01）。
  (2) caretaking の否定を語る payload は「住居／home／caretaking／community caretaking」に**スコープされている**（無限定に「無令状立入りが禁止された」と読める payload があれば FAIL）。
  (3) `WARRANT`・`CONSENT`・`EMERGENCY` の3語が近接（120字内）で温存側に並ぶ表現がどこかに存在する。
- **R-CADY（C-3）** — `Cady`/`Dombrowski`/`413 U.S. 433` を含む payload は、車マーカー `{"car","vehicle","automobile","tow","trunk"}` の
  いずれかと共起し、かつ「not a home」/「is not a house」系の肯定を含むこと。Cady の対象を home/house と提示したら FAIL。
- **R-ATTRIB（C-6/C07）** — `quote[].attribution` が非空。要約を引用符に入れない（逐語のみ）。許可対応表:
  ```python
  APPROVED_QUOTES = {
    "what is reasonable for vehicles is different from what is reasonable for homes":
        "Justice Thomas, for the Court",                       # C06/F07（多数意見・逐語）
    "the right of a man to retreat into his own home":
        "Justice Thomas, quoting Florida v. Jardines",         # C07/F15（Jardines 帰属）
    "no warrant is needed to help a person who is seriously injured or threatened with injury":
        "Chief Justice Roberts, joined by Justice Breyer",     # C09/F10（補足・逐語）
  }
  ```
- **R-JARDINES（C-6/C07・BLOCKING）** — `the right of a man to retreat into his own home` 系の逐語が対象に存在する場合、
  その attribution が **Jardines / Thomas が Jardines を引用** であること。近傍80字に `Payton` を**帰属元として**置いたら FAIL。
  かつ **`presumptively unreasonable` が Payton 文脈で別 payload に存在**すること（Payton は別命題として引用・R-PAYTON と一本化）。
- **R-PAYTON（C-6）** — `presumptively unreasonable` が figures/AE いずれかに存在（肯定検出）。`home is absolutely protected` 等の断定は
  R-FORBID で捕捉済み。Payton 引用年が **1980**（F14）であること。
- **R-CANIGLIA（C-4）／R-FACE／R-DOC（R1）** — `has_readable_text`/`has_identifiable_face`/`has_human_body` が true の項目は `role=="reject"`。
  `Edward Caniglia`/`Caniglia`（人名文脈）と人物化語（`face`/`portrait`/`likeness`/`appearance`/`his body`/`the man's eyes` 等・心情/内面語）の
  同一文共起を FAIL。事件主体語（"Edward Caniglia sued" / "for Edward Caniglia" / "the man they were worried about"）は許可。
  読める偽公文書の主張語（`legible`/`actual court filing`/`real report` を肯定文脈で）を FAIL。
  象徴オブジェ語（handgun on a table / empty porch / ambulance lights / front door / evidence tag / phone / two handguns on a cloth）は許可。
- **R-CRISIS（C-5）** — 手段/方法の描写語・内面憶測語を FAIL（グラフィックな自殺手段語のブラックリスト）。
  記録事実「shoot him／shoot me」系は figures/カード全体で**最大1回**（2回目の出現で FAIL・演出的反復の防止）。
  `09_package` の description（`*.json`/`*.txt`）に **`988`** が存在すること（R-988・無ければ FAIL）。
  **かつ `988` が `08_edit/ae_hero/beats.json`（AEデッキ）または `caniglia_film.json` の `figures[]` に出現したら FAIL**（988 は description.txt / pinned_comment / BrandEndcard のみ・画面カードに置かない・DESIGN L-C5 と一致）。
- **R-DATE** — F01/F02/F08 と F05(1973)/F06(2020)/F14(1980)/F15(2013) の日付・年が別カードで取り違えられていないこと。

**出力:** `episodes/PD-2026-043-caniglia/09_package/facts_lock.v001.json`（`{"pass":bool,"violations":[...],"skipped":[...]}`）。
**`pass:true` でない限り `check_final_acceptance.py` に進んではならない。**
**CLI:** `--json` / `--dryrun`（`_dryrun/` 配下も対象に含める）。対象ファイルが未生成ならスキップして必ずログに出す。「無いから通した」を黙るな。

---

# 3. ★境界契約: `asset_manifest.v001.json`（Aから受け取る唯一のファイル）

## 3.1 スキーマ（**Aが生成する。Bはこの形を前提に読む・A↔B一字一致**）

**スキーマ版:** `caniglia_assets.v1`（固定文字列。異なれば **exit 2**）。
EP43 spec の点数に一致: **still_body 85 / still_i2v_source 16 / motion 16 / factory 93 / overlay 12**。
**★サムネは独立の分類を持たない。** body 85枚のうち**6枚**に `also_thumb:true` を立てて流用する（**`role=thumb`/`still_thumb` を作らない**・サムネ用 count キーも無い・§11）。
**このスキーマ・`counts` キー・`role` enum・`overlay` 枚数は CODEX_A（生産者）の `build_caniglia_asset_manifest.py` の出力と1バイト単位で同一。**

- **`role` enum（固定・3値のみ）:** `"body"` | `"i2v_source"` | `"reject"`。**`thumb`/`still_thumb` を作らない。**
- **`counts`（固定キー・下限値）:** `{ "still_body": 85, "still_i2v_source": 16, "motion": 16, "factory": 93, "overlay": 12 }`。
- **`overlay` = 12**（A↔B 契約値・SPEC は overlay を規定しないので EP42 と同じ 12 を採用。A も 12 を宣言する）。

```jsonc
{
  "schema_version": "caniglia_assets.v1",
  "episode_id": "PD-2026-043-caniglia",
  "slug": "caniglia",
  "generated_at": "2026-07-21T12:00:00+09:00",
  "producer": "scripts/build_caniglia_asset_manifest.py",
  "is_stub": false,                          // ★ログと受入判定にだけ使う。処理を分岐させない

  "counts": { "still_body": 85, "still_i2v_source": 16, "motion": 16, "factory": 93, "overlay": 12 },

  "stills": [
    { "asset_id": "CAN-S01", "scene_id": "S01", "role": "body",   // "body"|"i2v_source"|"reject"（バリエーション概念なし＝各1枚）
      "also_thumb": false,                   // body から6枚だけ true（§11 の6シーン・追加生成しない）
      "act": 0,                              // 0=HOOK/OP, 1..3=幕, 5=ED
      "public_path": "caniglia/img/S01.png", // ★Bが cuts[].src に入れる値（1シーン1枚＝固有プロンプト・_01 等の接尾なし）
      "depth_path": "H:/pd-media/assets/ai/caniglia/S01_depth.png",  // role=="body" は実在必須
      "width": 3840, "height": 2160,
      "sha256": "...", "tags": ["handgun flat on a dining table", "closed front door"], "caption_hint": "the door stays closed",
      "source": "ai_codex", "commercial_use": "allowed",
      "qc": {"reviewed": true, "on_theme": true,
             "has_readable_text": false, "has_identifiable_face": false, "has_human_body": false, "notes": ""} }
    // i2v 種は role=="i2v_source"・asset_id "CAN-MS01".."CAN-MS16"・public_path は null（本編カットに出ない）
  ],

  "motion": [
    { "asset_id": "CAN-M01", "source_scene_id": "M01_src",   // ★i2v_source 種 ID を指す（body still ではない）
      "source_still": "H:/pd-media/assets/ai/caniglia/M01_src.png",
      "public_path": "caniglia/motion/M01_rife.mp4",   // ★必ず .mp4 かつ "_rife" を含む
      "act": 1, "width": 1280, "height": 720, "fps": 48, "frames": 164, "duration_sec": 3.417,
      "sha256": "...", "tags": ["ambulance lights sweeping a porch at dawn"],
      "qc": {"reviewed": true, "on_theme": true, "artifact_free": true, "notes": ""} }
  ],

  "factory": [
    { "asset_id": "AF-BG-0221",
      "public_path": "caniglia/factory/AF-BG-0221__empty_marble_chamber.mp4",  // ★必ず "/factory/" を含む
      "type": "backgrounds", "subtype": "empty_chamber", "kind": "video",
      "license": "Pexels License", "sha256": "...", "act": 3, "covers_scene_id": "S31",
      "duration_sec": 8.24, "width": 1920, "height": 1080,
      "eyeballed_content": "an empty marble chamber, wide static shot, no people",
      "qc": {"reviewed": true, "on_theme": true, "no_watermark": true,
             "no_recognizable_person": true, "no_cartoon": true, "label_matches_content": true, "notes": ""} }
  ],

  "overlay": [
    { "asset_id": "AF-PART-0007",
      "public_path": "caniglia/overlay/AF-PART-0007__dust_motes.mp4",
      "type": "particle_assets", "subtype": "dust_motes", "license": "Pexels License",
      "sha256": "...", "blend_hint": "screen",
      "eyeballed_content": "slow drifting dust on black, loops cleanly",
      "qc": {"reviewed": true, "on_theme": true, "no_watermark": true, "notes": ""} }
  ]
}
```

## 3.2 Bがこのマニフェストから作るもの（**EP43 spec の cuts 割当**）

| マニフェスト | Bでの使い道 | spec |
|---|---|---|
| `stills[role="body"]` 85枚 | **静止画カット101本**（`kind:"img"`, `treatment` 循環）・**各≤2回** | still distinct85/cuts101 |
| body 静止画で `also_thumb==true` の6枚 | サムネ3案の背景（§11・6シーン） | — |
| `stills[role="i2v_source"]` 16枚 | **本編カットに出さない**（i2v 種・A が Wan で motion 化済み） | — |
| `motion` 16本 | **i2vカット32本**（`kind:"footage"`）・**各≤2回** | motion distinct16/cuts32 |
| `factory` 93本 | **実写カット93本**（`kind:"footage"`）・**各1回のみ** | factory distinct93/cuts93 |
| `overlay` 12本 | **`cuts[].src` に出さない**（§5.5 の合成レイヤー扱い） | — |

**合計 101 + 32 + 93 = 226 カット / distinct 85+16+93 = 194 / first-use 194/226 = 0.8584 ✓（floor 0.70）**

## 3.3 `scripts/check_caniglia_asset_manifest.py`（消費側バリデータ・BLOCKING）

```bash
$PY scripts/check_caniglia_asset_manifest.py --assets <path> [--json]
```

検査（1つでも違反で exit 1。`schema_version` 違いだけ exit 2）:

1. `schema_version=="caniglia_assets.v1"` / `episode_id=="PD-2026-043-caniglia"` / `slug=="caniglia"`
2. `counts.*` が各配列の実長と一致し**下限**: `still_body>=85` / `still_i2v_source>=16` / `motion>=16` / `factory>=93` / `overlay>=12`
   （`still_body` は `stills[role=="body"]` の実長、`still_i2v_source` は `stills[role=="i2v_source"]` の実長）
3. `role` は **`body`/`i2v_source`/`reject` の3値のみ**（`thumb`/`still_thumb` 等が現れたら FAIL）
4. `role=="body"` の全静止画で `public_path` 非null、かつ `remotion/public/<public_path>` と
   `remotion/public/<stem>_depth.png` が**両方実在**（`CaseFilm.depthSrcOf()=src.replace(/\.[^.]+$/,'_depth.png')`。**depth 欠落はレンダークラッシュ**）。`role=="i2v_source"` は `public_path==null`
5. `role!="reject"` の全静止画で `max(width,height)>=3840`（`preflight_render_gate.MIN_LONG_EDGE_PX=3840`）
6. `motion[].public_path` が `.mp4` で終わり `_rife` を含む。`motion[].source_scene_id` は `stills[role=="i2v_source"]` の種 ID（`M01_src` 系）を指す
7. `factory[].public_path` が `/factory/` を含む
8. `overlay[].public_path` が `/overlay/` を含み `/factory/` を**含まない**
9. `sha256` が全配列を通して一意（**EP39/40/41/42 の素材と sha256 被りゼロ** も別途 A が保証・B は自集合内一意を検査）
10. `factory[].eyeballed_content` が非空、かつ `qc.label_matches_content==true`
11. `qc.has_readable_text` / `qc.has_identifiable_face` / `qc.has_human_body` が true の項目は `role=="reject"`（**R1**）
12. `also_thumb==true` の body 静止画が**ちょうど6枚**、かつ **`scene_id` 集合が `{S01,S24,S28,S30,S49,S81}` と完全一致**（サムネ供給・§11。**A(CODEX_A §4.3) と B で also_thumb の scene_id 集合が同一**であることを検査＝A↔B 契約点）
13. **全文字列値**が §2 の R-FORBID / R-CANIGLIA / R-FACE / R-DOC / R-CADY を通る

## 3.4 `scripts/make_caniglia_stub_assets.py`（**Aを待たずに完走するための鍵**）

やること:

1. `remotion/public/caniglia_dryrun/{img,factory,motion,overlay}/` を作る
2. **静止画スタブ**: PIL で **3840×2160** 単色PNG（`scene_id` と `role` を大書き）＋同名 `_depth.png`
   （**`L` モード**のグラデ）。body **85枚 + depth 85枚**（うち6枚に `also_thumb:true`＝§11 の6シーン）。
   i2v_source 16件はマニフェストにエントリだけ作る（`public_path==null`・本編に出ないので画像ファイル不要）
3. **動画スタブ**（ffmpeg `color` フィルタ）:
   - factory **93本**: `1920x1080@30fps`・**4.0秒**・`AF-STUB-<NNNN>__stub_clip.mp4`
   - motion **16本**: `1280x720@48fps`・**3.417秒**・`M<NN>_rife.mp4`
   - overlay 12本: `1920x1080@30fps`・2.0秒
4. **スタブ黒ベース**: `episodes/PD-2026-043-caniglia/08_edit/_dryrun/caniglia_final_bgm.v002.mp4` を
   ffmpeg `color=c=black:s=1920x1080:r=30` ＋無音aac で **≈735秒**生成（§7.10 のコンポジタが本番と同じ経路で走れるように）
5. `05_visuals/asset_manifest.stub.v001.json` を **§3.1 と完全に同じスキーマ**で書く
   （`is_stub:true`・`public_path` 先頭を `caniglia_dryrun/` に・`counts`/`role`/`overlay`=12 は本番と同一）

**★スタブのパスの罠（外すと `check_asset_reuse.kind_of()` が誤分類して緑になってしまう）:**

```python
p = path.lower().replace("\\", "/")
if "/factory" in p or re.search(r"\baf-bg-", p):                            return "factory"  # 上限1回
if p.endswith((".mp4",".mov",".webm")) or "ai_video" in p or "_rife" in p: return "motion"   # 上限2回
return "still"                                                                                # 上限2回
```

| 種別 | `public_path` の形 | 満たす条件 |
|---|---|---|
| 静止画 | `caniglia_dryrun/img/S01.png` | `/factory` を含まない・`.png`・`_01` 等の接尾なし |
| factory | `caniglia_dryrun/**factory**/AF-STUB-0001__stub_clip.mp4` | **`/factory/` を含む** |
| i2v | `caniglia_dryrun/motion/M01**_rife**.mp4` | **`.mp4` かつ `_rife` を含む** |
| overlay | `caniglia_dryrun/overlay/...mp4` | **`cuts[].src` に出さない** |

**スタブの点数は本番と完全に同じ**（body 85〈うち also_thumb 6〉/ i2v_source 16 / motion 16 / factory 93 / overlay 12）。
これで**素材が1枚も無い段階で全ゲート通過を実証できる。**

## 3.5 本番マニフェストへの切り替え — **コードは1行も変えず** `--assets` を差し替えるだけ。
差し替え後、[B-DONE-2]〜[B-DONE-8] を全部やり直す。

---

# 4. narration_index（TTS は課金＝禁止。スタブで着手し、本番で差し替える）

## 4.1 なぜ narration_index か
`build_caniglia_film.py` は**尺・区間・字幕を narration_index から導出する**。**秒数をコードに直書きしない。** 唯一の正は narration_index。

## 4.2 スキーマ（`caniglia_narration.v1`）

```jsonc
{
  "schema_version": "caniglia_narration.v1",
  "episode_id": "PD-2026-043-caniglia",
  "is_stub": true,
  "total_seconds": 726.7,
  "chunks": [
    { "section": "HOOK", "start": 0.000, "end": 4.100,
      "text": "He set a gun on the dining table, and then he spoke." },
    { "section": "OP",   "start": 25.000, "end": 29.100, "text": "..." },
    { "section": "ACT_1","start": 55.000, "end": 59.200, "text": "..." }
  ]
}
```

**section 値（固定・5幕）:** `HOOK` / `OP` / `ACT_1` / `ACT_2` / `ACT_3` / `ENDING`。
（EP43 の BODY は 3幕＝ACT_1「その夜」/ ACT_2「安否確認」/ ACT_3「caretaking の起源と限界」。**ACT_4 は無い。**）
`build_caniglia_film.py` は `section_windows()`（各 section の最初のチャンク start）で幕境界を得る。

## 4.3 spec のタイムライン（**設計目標。実タイミングは narration_index が上書きする**）

| section | 語数 | 秒 | 備考 |
|---|---|---|---|
| HOOK | 69 | 23.2 | VO。末尾に `DESIGNED SILENCE 1.8s`（閉じた玄関ドアの残響のみ） |
| （gold `BrandOpening`） | 0 | 3.5 | 非VO。`OPENING_SEC`。**frame0 ではなく HOOK 後に挿入** |
| OP | 88 | 29.6 | 二人称の問い（thesis）＋ channel ID |
| ACT_1 The night | ~230 | ~77.5 | 最短・現在形・抑制。途中に `DESIGNED SILENCE 1.4s`（ホテルのキーカード） |
| ACT_2 The welfare check | ~430 | ~144.9 | 電話→ポーチ→救急車→無令状押収。途中に `beat` |
| ACT_3 Where caretaking stops | ~870 | ~293.0 | 判例核。**最も遅く長い**。Cady=車 / 9-0 / headlineは罠 / 補足意見 / vacate&remand |
| ENDING | 415 | 139.8 | ペイオフ→CTA。途中に `DESIGNED SILENCE 2.2s`（開いた玄関ドア・夜明け） |
| （`BrandEndcard`） | 0 | 9.0 | 非VO。`ENDCARD_SEC` |

**唯一の正は `python scripts/check_script_length.py <script> --json`。** 総語数 **2,141**（spec `words_total`）/ `wpm 178.1` /
narration_seconds **721.3**（spec・純発話）。**自己申告・体感の尺判定は禁止。**

## 4.4 `scripts/make_caniglia_stub_narration.py`（**Bはこれで着手できる**）

`EP43_caniglia_script.en.v001.md` を読み、各 section 見出し配下の本文を文に割り、178.1 wpm で各文に start/end を割り当てて
`chunks[]` を作る。ト書きの **`【DESIGNED SILENCE 1.8s …】` / `【DESIGNED SILENCE 1.4s …】` / `【DESIGNED SILENCE 2.2s …】`** は
**無音ギャップ**として時間を進める（チャンクにはしない・正規表現は `DESIGNED SILENCE\s+([\d.]+)s` で秒を拾う）。`【beat】` は ~0.6s の小ギャップ。
`【…】/〔…〕/[…]/(…)` の apparatus は全て非発話として除外。`OPENING` 本文の前に `OPENING_SEC=3.5` の無音を挿入。
台本本文はそのまま（改変しない）。出力: `06_audio/narration_index.stub.v001.json`（`is_stub:true`）。

> **本番:** 別工程が TTS→faster-whisper で `06_audio/narration_index.v001.json`（実測語タイム）を作る。
> **これは課金ジョブなので B は起動しない。** 来たら `--narr` を差し替えるだけ。

---

# 5. `caniglia_film.json` の構築（`scripts/build_caniglia_film.py`＝`build_young_film.py` の複製）

## 5.1 `FilmData` 型（`CaseFilm.tsx` から。これに従う）

```ts
export type Cut = {start:number; dur:number; kind:'img'|'footage'; src:string; treatment:string; seed:string};
export type FilmData = {
  fps:number; narration:string; narrationSeconds:number; hookSeconds:number; hookLine:string;
  hook:{start:number;dur:number;kind:string;src:string;seed:string}[];
  cuts:Cut[]; captions:{start:number;end:number;text:string}[];
  graphics:{start:number;end:number;lines:string[]}[];      // 必須フィールド。EP43 は []
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
- **`fps = 30`**（EP42 と同じ film fps）。`narration = "caniglia/narration.mp3"`（本番のみ実在）

### 5.1.1 ★durationInFrames の4項関数（明示・total ≤ 750s を assert）

```
caseFilmDurationInFrames(canigliaFilm, fps=30)
  = round(hookSeconds * fps)        // hookSeconds = 0.0（HOOK の VO は narrationSeconds に含む。frame0 に別 hook 尺を積まない）
  + round(OPENING_SEC * fps)        // OPENING_SEC = 3.50（gold BrandOpening は HOOK の後）
  + ceil(narrationSeconds * fps)    // narrationSeconds = narration_index.total_seconds（≈726.7・silence 込み）
  + round(ENDCARD_SEC * fps)        // ENDCARD_SEC = 9.00
```

- **hookSeconds を明示: `hookSeconds = 0.0`**（HOOK ナレは narrationSeconds に内包・§4.2 の section=HOOK。frame0 に独立 hook モンタージュ尺を積まない）。
- 概算（fps30・narration≈726.7）: `0 + 105 + ceil(21801) + 270 = 22176 frames = 739.2s`。
- **ビルダ末尾で `assert total_seconds_of_frames <= 750.0`**（`total_frames/fps <= 750`）。超えたら exit 1。

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
        footage 平均 ~3.35s → 125×3.35 ≈ 418.3s
        still-frame-share = 303.0 / 721.3 = 0.4201          ✓ <=0.45（cut数比より安全側）
        motion-coverage(frame) = 418.3 / 721.3 = 0.5799     ✓ >=0.45

[D] 平均ショット長（spec mean_shot 3.19 / max 6.0）
    721.3 / 226 = 3.19 秒/カット                            ✓ <=6

[E] factory 下限（30秒に1本 = 24 → >=24本） 93本            ✓
```

> **★[C](i) の cut数ベース still-share 0.4469 は cap 0.45 に薄い。still を1枚増やすか factory を1本削ると 0.45 を超える。**
> **マニフェストが still 85 / factory 93 / motion 16 を割ったら組まずに止めて A に差し戻す（ブリーフ§2: still を増やして factory を削るな）。**
> **frame ベースも下回るよう、still の平均尺を footage より系統的に短く保つ（§5.3-5）。**

## 5.3 カット割り当てのルール（`build_young_film.py` の `allocate()`/`tile_window()` を踏襲）

1. 各幕の秒窓を `section_windows()` から取り、幕内に **factory : motion : still を按分**して配置
   （目安の幕別カット数。実配分は narration_index の窓長で自動調整）:

   | section | factory | motion | still | 小計 |
   |---|---|---|---|---|
   | HOOK+OP | 7 | 2 | 8 | 17 |
   | ACT_1 | 10 | 3 | 11 | 24 |
   | ACT_2 | 19 | 6 | 20 | 45 |
   | ACT_3 | 38 | 13 | 41 | 92 |
   | ENDING | 19 | 8 | 21 | 48 |
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
`caniglia_film.json` に **`overlays` 独自キー**で持たせる（`CaseFilm` は未知キーを無視）か、専用レイヤーで `screen` 合成する。

## 5.6 ビルダが出力する成果物（**asset_map→manifest変換＋beatsheet生成**）

| 出力 | パス |
|---|---|
| film.json | `remotion/src/data/caniglia_film.json` |
| public コピー | `remotion/public/caniglia/film_data.v001.json` |
| **build provenance**（asset_map→provenance変換） | `episodes/PD-2026-043-caniglia/04_scenes/caniglia_build_manifest.v001.json`（**A の `05_visuals/asset_manifest` に書かない**） |
| **beatsheet**（figures+AE区間の突き合わせ表） | `episodes/PD-2026-043-caniglia/04_scenes/caniglia_beatsheet.v001.json` |
| SRT（字幕未生成時のフォールバック） | `episodes/PD-2026-043-caniglia/08_edit/captions.final.v001.srt`（**§8 の生成器が上書きする**） |

> **★beatsheet の命名に関する重大な注意:** `check_motion_density` / `check_animation_mix` は
> `04_scenes/premium_beatsheet.v*.json` を**自動検出して film.json より優先**する。
> **B の beatsheet は `caniglia_beatsheet.v001.json`（`premium_` を付けない）** にして、**ゲートの測定源を film.json 一本に保つ**
> （二重ソースの乖離＝EP39/40 の矛盾28件の原因を避ける）。`caniglia_beatsheet` は provenance と `validate_caniglia_beats` 専用。

## 5.7 CLI
```bash
$PY scripts/build_caniglia_film.py \
  --assets <asset_manifest path> \
  --narr   <narration_index path> \
  --out    remotion/src/data/caniglia_film.json \
  [--captions episodes/PD-2026-043-caniglia/08_edit/captions.final.v001.srt]
```
**`--assets` の `is_stub` によって処理を変えないこと（§0.2）。** 末尾に `check_asset_reuse` 相当の自己レポートを print する。

---

# 6. Remotion 側 `figures[]`（**37本・spec floor 31 に +6・`graphics[]=[]`**）

## 6.1 密度の検算（`check_motion_density`・**AEカードは1本も数えられない**）

```
figures 37本（film.json） / body 12.02分(=721.3/60) = 3.08 /分    ✓ beats_per_min_floor 2.5
coverage: 37本 × 平均5.4s = 199.8s / 721.3 = 27.7%                 ✓ MIN_ANIMATED_COVERAGE 0.25
variety : 下記 kind を12種以上使用                                ✓ variety_floor 3
spec motion.beats_floor = 31 に対し 37 で余裕。coverage が最も薄いので figures の dur は 4.8–6.0s を基本に。
```

> **★3軸すべて AND。density/coverage/variety のどれか1つでも floor 未満で FAIL。**
> 37本を非重複で置き、平均 dur を 5.4s 程度に確保すること（coverage が floor 0.25 に一番近い）。

## 6.2 ★★★ `FigureSpec` の `kind` は**実在する小文字値のみ** ★★★

> **大文字名（`ActTitle`/`QuoteCard`/`VoteTally`…）は `FigureBeats.tsx` の union に無く、無言で描画が消える。**
> **`comparebars` は存在しない → `compbars` を使う。`routemap` 系も union を確認してから使う（無ければ `pindropmap`）。**

**EP43 で使う実在 `kind`（`remotion/src/components/FigureBeats.tsx` の union から。全て `start`/`end` 必須・全小文字）:**

| `kind` | 必須プロパティ | EP43での用途 |
|---|---|---|
| `numberticker` | `value:number` / `label?` / `prefix?` `suffix?` `decimals?` | 拳銃2丁・待機時間等 |
| `stat` | `value:number` / `label:string` / `prefix?` `suffix?` `decimals?` `topLabel?` | 2 handguns・補足3人（帰属） |
| `votetally` | `majority:number` / `dissent:number` / `label?` | **9対0（SCOTUS のみ）**（F03・R-VOTE99・label に限定併記） |
| `timeline` | `events:{year:string;text:string}[]` | 2015→2020→2021 / 1973→2020→2021 |
| `quote` | `quote:string` / `attribution:string` | Thomas 逐語 / Jardines 逐語 / Roberts+Breyer（**帰属必須**・R-ATTRIB） |
| `kinetic` | `lines:string[]` / `style?:'wordpop'\|'maskslide'\|'emphasis'` / `emphasisWords?` | 決め所テキスト（**emphasisWords は1–2語=文字切れ回避**） |
| `lowerthird` | `primary:string` / `secondary?` / `accent?` | 開示 `AI-assisted visualization` / 判例引用 / 温存例外 / Alito「another day」（★988 は figures に置かない＝R-988） |
| `acttitle` | `title:string` / `kicker?` / `index?` | 幕頭（Remotion 側で密度に数える。§7 の AE 幕頭とは別区間） |
| `compbars` | `items:{label:string;value:number;accent?}[]` | 巡回区分裂（5/6/8/9 拡張 vs 3/7 拒否）／CAR vs HOME（★label に "a car, not a house" を明記＝R-CADY・※`comparebars` は存在しない） |
| `mechanism` | `mechanism:'closingdoor'\|'gears'\|'faultsplit'` ★discriminant は `kind`・変種は `mechanism` | 閉じる/開く玄関(closingdoor)・救済/論拠の移動(gears)・射程の線(faultsplit) |
| `dochighlight` | `rects:{x,y,w,h}[]` / `mode?:'underline'\|'box'\|'redact'` | 証拠タグ/書類（**redact**＝象徴・読ませない・R1/C-4） |
| `regionmap` / `pindropmap` | `label?` / `pins:{x,y,label?}[]` | Cranston, RI の戸口（象徴・顔なし） |

**`votetally` は `majority:9, dissent:0` 固定（SCOTUS の 9-0 のみ・§2 R-VOTE99）。巡回区 5/6/8/9 vs 3/7 は votetally に入れない（compbars/stat）。**
`quote[].attribution` は §2 の `APPROVED_QUOTES` に一致させる。**逐語のみ・要約を引用符に入れない。**

## 6.3 figures アンカー設計（`build_young_film.py` の `FIGURE_ANCHORS` 方式）

**方式:** `(anchor_sec, payload)` の配列を秒昇順に置き、`build_figures()` が
`end = min(anchor+FIG_DUR, next_anchor-FIG_GAP, total-0.5)` でクランプ、`end-start < FIG_MIN_DUR` なら **exit 1**。
`FIG_DUR=5.4 / FIG_MIN_DUR=3.0 / FIG_GAP=0.4`。**アンカー秒は narration_index の section 窓に対する相対で決め、
`section_windows()` を基準にオフセットで置く**（秒直書き禁止）。

**配置方針（37本・§2 台帳の値だけを焼く・kind を分散して variety を稼ぐ・6制約順守）:**

- **HOOK/OP（3）:** `kinetic`（"THE WELFARE CHECK"）/ `lowerthird`（`AI-assisted visualization` 開示）/ `mechanism:closingdoor`（閉じた玄関ドア）
- **ACT_1（6）:** `acttitle`（THE NIGHT）/ `timeline`（F08 August 2015・Cranston, RI）/ `pindropmap`（Cranston, RI・象徴の戸口）/ `kinetic`（"A PRIVATE CRISIS"・emphasisWords=["PRIVATE"]）/ `lowerthird`（"a handgun on the dining table"＝象徴描写・C-4/C-5）/ `mechanism:closingdoor`（朝も戸は閉じたまま）
- **ACT_2（8）:** `acttitle`（THE WELFARE CHECK）/ `lowerthird`（"the non-emergency line"＝安否確認要請）/ `kinetic`（"MAKE SURE HE'S OK"）/ `stat`（**F09 2 handguns**, label "seized · no warrant"／C-1 の趣旨）/ `kinetic:emphasis`（"NO WARRANT"・emphasisWords=["WARRANT"]）/ `mechanism:faultsplit`（見守り→捜索へ化ける転回）/ `lowerthird`（"they agreed, he says"＝条件・ヘッジ付）/ `dochighlight:redact`（証拠タグ＝読ませない・R1/C-4）
- **ACT_3（15）:** `acttitle`（WHERE CARETAKING STOPS）/ `lowerthird`（**F06 First Circuit, 953 F.3d 112 (2020)**）/ `timeline`（1973 Cady → 2020 First Circuit → 2021 SCOTUS）/ `lowerthird`（**F05 Cady v. Dombrowski, 413 U.S. 433 (1973)**, secondary "a car, not a home"／C-3）/ `compbars`（CAR vs HOME・items=[{label:"CADY · a car, not a house",value:1},{label:"a HOME — where Cady never reached",value:1}]／**C-3・"not a house" を Cady と同一 payload に置く＝R-CADY**）/ `mechanism:gears`（車庫の論理が玄関へ流れる）/ `lowerthird`（**F04 Caniglia v. Strom, 593 U.S. 194 (2021), No. 20-157**）/ `timeline`（argued **F02 2021-03-24** → decided **F01 2021-05-17**）/ `votetally`（**F03 9対0**, label "vacate & remand · one excuse closed"／**C-2・R-VOTE99**）/ `quote`（"what is reasonable for vehicles is different from what is reasonable for homes" → "Justice Thomas, for the Court"／**C-3/R-ATTRIB**）/ `quote`（"the right of a man to retreat into his own home" → "Justice Thomas, quoting Florida v. Jardines"／**C-6/C07/R-JARDINES**）/ `lowerthird`（**F14 Payton v. New York (1980)**, secondary "presumptively unreasonable"／C-6）/ `kinetic:emphasis`（"A HEADLINE IS A TRAP"・emphasisWords=["TRAP"]）/ `stat`（**F18 3**, label "concurrences · Roberts+Breyer / Kavanaugh / Alito"／C-1）/ `mechanism:faultsplit`（射程＝住居の caretaking 拡張だけを否定）
- **ENDING（5）:** `kinetic`（"ONE EXCUSE, OFF THE TABLE"・emphasisWords=["EXCUSE"]／C-1/C-2）/ `lowerthird`（**F17 STILL OPEN**, secondary "WARRANT · CONSENT · EMERGENCY"／**C-1・R-SCOPE**）/ `lowerthird`（開示 `AI-assisted visualization` 再掲）/ `lowerthird`（**F12 Justice Alito, concurring**, secondary "red-flag gun laws — a question for another day"／C-1/C-5・★988 は figures に置かない＝R-988。988 は概要欄/固定コメント/BrandEndcard のみ）/ `mechanism:closingdoor`（夜明けに**開いた**玄関ドア）

> **9-0（F03）を figure に焼くときは必ず `votetally` の `label` に "vacate & remand · one excuse closed" を付ける（R-VOTE99）。
> 単独の勝利数として出さない。** 巡回区分裂（F13）は `compbars` で「1/5/6/8/9 が拡張 vs 3/7 が拒否」を示し `votetally` に入れない（R-SPLIT）。

## 6.4 配置ルール
1. **AEの区間（§7.2）と1秒でも重ならない**（`validate_caniglia_beats` が突き合わせ）
2. **同じ kind を連続させない**（`mechanism` の直後に `mechanism` を置かない）
3. 1枠 **4.8–6.0秒**
4. `quote[].quote` / `kinetic[].lines` / `*.label` は §2 の R-LEDGER・R-ATTRIB・R-FORBID・R-VOTE99・R-SCOPE・R-CADY・R-JARDINES・R-CANIGLIA 検査対象
5. 台帳外の数値を `value`/`numKeys` に置かない（**焼いたら R-LEDGER で FAIL**）
6. **`emphasisWords` は1–2語の短句のみ**（長句は AE/Remotion で末尾が切れる＝EP40 実害。§7.5-3 と同趣旨）

---

# 7. After Effects カード（`build_caniglia_hero_cards.py` / `composite_caniglia_hero.py`）

## 7.1 位置づけ
AEカードは **film.json とは別**に ffmpeg で本編に焼き込む（§0.5-2＝密度に数えられない）。
`build_young_hero_cards.py` を**コピーしてパス・定数・CARDS デッキだけ差し替える**。レイアウト実装・
`money_keys()`・`fit_size()`・完了マーカー・機械の罠対処は**1行も削らない**。

## 7.2 AEカードデッキ（**単調増加・重複ゼロ・台帳裏付けのみ・6制約順守。この表が契約。8枚**）

**区間の秒は本番の rendered base（narration_index 由来）に一致させる。** 下表の秒は spec タイムライン基準の**目安**で、
`build_caniglia_hero_cards.py` は section 窓からオフセットで算出しクランプする。**背景静止画は象徴オブジェのみ（R1/C-4）。**
**この表は DESIGN §（AEカード）と一字一致（ブリーフ§6 の候補8本を採用）。レイアウト名は §7.3 の実装済み8種のみ。**

**★id・レイアウト・F-ID・順序は DESIGN §6.3/§6.4 と一字一致（time-order＝start 昇順）。988 は AEデッキに入れない（R-988）。**

| id | レイアウト（**実装済み8種のみ・§7.3**） | hero（主表示） | top / sub / bottom / attribution | F-ID | 背景（象徴のみ） | required |
|---|---|---|---|---|---|---|
| d01 | DATE_STAMP | **AUGUST 2015** | place: **CRANSTON, RHODE ISLAND** | F08 | 夜の空のポーチ（顔なし） | 必須 |
| n01 | CENTER_STACK | **TWO HANDGUNS** | top: **THE SEIZURE** / bottom: **NO WARRANT** | F09 | 布の上の拳銃2丁・証拠タグ | 必須 |
| t01 | ACT_TITLE_CARD | **WHERE CARETAKING STOPS** | kicker: **ACT THREE** | — | 大理石の第4修正（判読困難） | 必須 |
| c01 | SPLIT_COMPARE | **A CAR IN CUSTODY / NOT A HOME** | top: **WHERE CARETAKING CAME FROM** / bottom: **CADY v. DOMBROWSKI, 1973** | F05 | 左=車＋レッカー / 右=玄関ドア | 必須 |
| q01 | QUOTE_CARD | **"what is reasonable for vehicles is different from what is reasonable for homes"** | attribution: **JUSTICE THOMAS, FOR THE COURT** | F07 | 大理石の列柱（顔なし） | 必須 |
| v01 | VOTE_SPLIT | **9 – 0** | top: **CANIGLIA v. STROM - MAY 2021** / bottom: **ONE EXCUSE, CLOSED** | F03 | 空の9席（顔なし） | 必須 |
| s01 | CENTER_STACK | **WARRANT - CONSENT - EMERGENCY** | top: **THE DOORS THAT STAYED OPEN** / bottom: **THESE EXCEPTIONS STILL LET POLICE IN** | F17 | 左=閉じた戸 / 右=開いた戸（温存例外の象徴） | 必須 |
| r01 | CENTER_STACK | **VACATE AND REMAND** | top: **THE DISPOSITION** / bottom: **SENT BACK DOWN - NOT ENDED IN HIS FAVOR** | F03 | 大理石の階段・差し戻される案件 | 必須 |

> **★q01 の QUOTE_CARD は逐語（R-ATTRIB）。** ブリーフ§6 の略記 `"vehicles ≠ homes"` は**引用符の中に入れない**（要約を quote にすると R-ATTRIB で FAIL）。
> `≠` の記号モチーフを使うなら QUOTE_CARD の hero ではなく非引用の装飾として。quote 文字列は §2 `APPROVED_QUOTES` と一致（大小無視・DESIGN §6.4 は全大文字表示）。**DESIGN §6.4 q01 と一字一致。**
> **v01 の bottom は "ONE EXCUSE, CLOSED"（★"final win" 系を書かない＝R-FORBID）。「最終勝訴でない」限定は r01 の "SENT BACK DOWN - NOT ENDED IN HIS FAVOR" が担う（C-2）。**
> **988 カードは作らない（R-988）。** 温存例外は s01（STILL OPEN）が担う。どのカードにも「令状なしで家に入れない」断定・「全面勝訴」を書かない（R-FORBID/R-VOTE99/R-SCOPE）。

**検算（Codex は自分で再計算して一致を確認）:** 8区間・単調増加・重複ゼロ・HOOK(0–23.2) と ENDCARD(末尾9s) に重ねない。
Remotion figures(§6) と1秒も重ならない（`validate_caniglia_beats` が検査）。

## 7.3 レイアウト（`build_young_hero_cards.py` の実装を踏襲・**実装済みレイアウト名だけを使う**）
複製元 `build_young_hero_cards.py` が実装するレイアウトは**この8種のみ**:
`DATE_STAMP` / `CENTER_STACK` / `MONEY_STACK` / `SPLIT_COMPARE` / `ACT_TITLE_CARD` / `QUOTE_CARD` / `VOTE_SPLIT` / `SEAM_TRANSITION`。
**§7.2 デッキはこの8種の名前しか使わない**（上記以外の独自レイアウト名を発明しない＝`validate_caniglia_beats` §7.9 ルール3 で FAIL する）。
**EP43 は MONEY_STACK / SEAM_TRANSITION を §7.2 では未使用**（この案件に金額は無い＝MONEY_STACK を無理に使わない）。**ACT_TITLE_CARD は t01（ACT3 幕頭）で使用。**
**共通レイヤースタック・Anton/Oswald・`psName()` の runtime 解決（allFonts の array-LIKE ラッパーを unwrap）は複製元と同一。**

**★共通レイヤースタックに AI開示レイヤーを1枚追加（R1・全カード常時焼き）:** 最上位に近い固定レイヤーとして
`AI-assisted visualization`（Oswald 20px / SILVER `#C8CDD6` / opacity 70% / 右下 `[W-32, H-28]`）を全カードに焼く。
AEカードは不透明の全画面 mp4 として本編に overlay されるため、これが無いと本編(Remotion)右下の開示が隠れ、
AI生成 static 背景が開示なしで表示される（**R1 違反**）。字幕帯とは縦56px 以上離す。

**★EP43 色定数（0..1 float・porch-amber レーン色。EP41 gold / EP42 warrant-blue を流用禁止・DESIGN と一致）:**
```python
ACCENT = [0.878, 0.569, 0.235]  # #E0913C porch-amber アクセント（数値・下線・"助けに来た"暖色＝レーン分離）
WHITE  = [0.961, 0.969, 0.980]  # #F5F7FA
SILVER = [0.784, 0.804, 0.839]  # #C8CDD6（開示テキスト）
INK    = [0.039, 0.039, 0.047]  # #0A0A0C 近黒ルート（サムネ bg と一致）
```
> **accent は必ず `#E0913C`（EP41 gold / EP42 warrant-blue を書かない）。** サムネ・OP props・AEカードの accent は全て `#E0913C`。

**数値カードは全て `money_keys()` 系で表示文字列を Python 事前計算**（JSX で算術しない＝EP38 確定ルール）。
`VOTE_SPLIT`（v01）は「9」を先に、間を置いて「0」を出し 9-0 の重みを作る（多数=WHITE/SILVER・0=ACCENT porch-amber）。
**`v01`（9-0）は同一カード内に限定サブ "ONE EXCUSE, CLOSED"、`r01`（差戻し）は "SENT BACK DOWN - NOT ENDED IN HIS FAVOR" を別レイヤーで出す（C-2/R-VOTE99・"final win" 系は書かない）。**
**`c01`（Cady）は左=車＋レッカー、右=玄関ドアの SPLIT_COMPARE で「a car, not a home」を視覚化（C-3・車と家を分離）。**

## 7.4 `beats.json` スキーマ（本番 `08_edit/ae_hero/beats.json` / dryrun `08_edit/_dryrun/ae_hero/beats.json`）
`build_young_hero_cards.py` の beats スキーマに準拠。各 beat に `id` / `layout` / `start` / `end` / `dur` /
`still`(象徴 or null) / `hero`(主表示文字列) / `top` / `bottom` / `caption`(**改行禁止・最大50字**) /
`value` / `numKeys` / `blend_mode`(既定 "overlay") / `required` / `out` / `attribution`(**QUOTE_CARD=q01 は必須**・§2 `APPROVED_QUOTES` と一致・R-ATTRIB)。
**`value` / `hero` の数値は §2 台帳の `verified:true` 値のみ**（`check_caniglia_facts` が照合）。
**`v01`/`r01` は R-VOTE99 を満たす限定サブ文字列（"one excuse"/"vacate"/"remand"/"sent back"/"not ended in his favor"）を `bottom` か `caption` に持つ。`c01` は R-CADY を満たす車マーカー＋"not a home"を持つ。**

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
$PY scripts/ae/build_caniglia_hero_cards.py [--dryrun]
"C:/Program Files/Adobe/Adobe After Effects 2026/Support Files/AfterFX.exe" -noui \
  -r ".../episodes/PD-2026-043-caniglia/08_edit/ae_hero/caniglia_hero.jsx"
# render/_build_ok.txt を待つ（最大600秒）→ render/*.mp4 が8本揃うまで待つ（最大1200秒）
$PY scripts/ae/composite_caniglia_hero.py [--dryrun]
```

## 7.9 `scripts/validate_caniglia_beats.py`（BLOCKING）
1. `beats[].start` 昇順・区間非重複
2. 全 `start`/`end` が本編ナレ区間内（HOOK 0–23.2 と ENDCARD 末尾9s に重ねない）
3. `layout` が §7.3 の**実装済み8種**（`DATE_STAMP`/`CENTER_STACK`/`MONEY_STACK`/`SPLIT_COMPARE`/`ACT_TITLE_CARD`/`QUOTE_CARD`/`VOTE_SPLIT`/`SEAM_TRANSITION`）のいずれか。**この8種以外のレイアウト名は FAIL。** still が必要なレイアウトで null なら FAIL・ベクター系(SEAM)で非null なら FAIL
4. `still` 非null は実在＋長辺 >=3840px
5. `hero`/`top`/`bottom`/`caption`/`value` が §2（R-FORBID/R-LEDGER/R-ATTRIB/R-VOTE99/R-SCOPE/R-CADY/R-JARDINES/R-PAYTON/R-CANIGLIA/R-FACE/R-DOC/R-DATE）を通る
6. `verified:false` の値を要求するカードは `required:false` で**除外**、`required:true` なら exit 1（`--dryrun` は警告続行）
7. **`caniglia_film.json` の `figures[]`（§6）と AE の区間が1秒でも重ならない**
8. `caption` に改行が含まれない
9. **AI開示レイヤーの存在（R1）** — ビルダが全カード共通スタックに `AI-assisted visualization`（右下・§7.3）を焼く設定であること
   （`build_caniglia_hero_cards.py` の共通スタック定義に開示レイヤーが1枚あることを静的に確認）。無ければ FAIL。
   受入アイボール（§13.1）でも「AEカード表示中も右下の開示が見える」を確認する。

## 7.10 基底 mp4 とコンポジタ（`build_caniglia_bgm.py` → `composite_caniglia_hero.py`）
```
# 完成後の合成順（ブリーフ§5）: build_caniglia_bgm.py（narration+BGM）→ composite_caniglia_hero.py（AEカード焼込み）
BASE = episodes/PD-2026-043-caniglia/08_edit/caniglia_final_bgm.v002.mp4     # build_caniglia_bgm.py が生成
OUT  = episodes/PD-2026-043-caniglia/08_edit/caniglia_final_bgm.v003_ae.mp4  # composite_caniglia_hero.py が生成
FFMPEG  = C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe
FFPROBE = C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffprobe.exe
W,H,FPS = 1920, 1080, 30
```
**SKIP4条件を1行も削らない:** ① `render/<id>.mp4` 不在 ② 解像度 != 1920x1080 ③ 実測尺 `< dur-0.3` ④ `beat.end > base_dur`。
SKIP された区間は元カットのまま残る（作品は壊れない）。**何枚 SKIP したかを stderr に必ず出す。**
ffmpeg は `overlay=0:0:eof_action=pass:enable='between(t,start,end)'`（`blend_mode` が screen/multiply の時のみ `blend`）。
**出力後 `probe_dur(OUT)` でベースとの尺差 <=0.5秒を確認。出荷済みは絶対に上書きしない（必ず `_v003_ae`）。**
**dryrun のベースは §3.4 のスタブ黒ベース `_dryrun/caniglia_final_bgm.v002.mp4`。**

---

# 8. 字幕の切断規則（`scripts/gen_captions_caniglia.py`＝`gen_captions_young.py` の複製）

## 8.1 原則
**文字数は「上限」であって「分割基準」ではない。** `gen_captions_young.py` の `internal_split()` / `chunk_sentence()` を**そのままコピー**。
`from fix_caption_dangling import NO_DANGLE_END, wrap as safe_wrap`（**語リストを自前で書き直さない**）。

## 8.2 通すゲート `scripts/check_caption_breaks.py`（**閾値を緩めるの禁止**）
- **A. 行末の機能語**（複数行キューの最終行以外が句読点なしで `NO_DANGLE_END` の語で終わる）= 0件
- **B. 孤立キュー**（語数<3 で「終端句読点で終わる」「大文字で始まる」の両方を満たさない）= 0件
- **C. 句をまたぐ切断(hard)** = 0件
- A/B/C いずれか1件で FAIL（**実質ゼロ許容**）

## 8.3 EP43 の入力と対応
- 入力は **narration_index の各チャンク文**（`--narr`）。**字幕テキストは台本本文と1:1対応**（§0.5-5）。台詞・別エピソード文の混入禁止。verbatim で使い、構文境界で分割するだけ。
- `ABBR` に `U.S.` / `v.` / `Mr.` / `F.3d` / `No.` 等を持つ（`Caniglia v. Strom` の `v.`、`593 U.S. 194` の `U.S.`、`953 F.3d 112` の `F.3d`、`No. 20-157` の `No.` で文を切らない）。
- タイミングは narration_index の start/end。CPS <=27・最小表示 0.90秒。**Step で決めた境界を時間都合で動かさない。**
- **字幕にも R-FORBID 適用**（台本本文に禁止語は無いので verbatim なら自然に通るが、`check_caniglia_facts` の対象でもある。§2.1 の注意：否定文脈の近似語を禁止語に足さない）。

## 8.4 セルフテスト（`--selftest`・EP38 実害を回帰に）
`"...the same officers he had asked to leave them alone."` → `"alone."` を単独キューにしない等の4ケースを実装し、
`Caniglia v. Strom` / `593 U.S. 194` / `953 F.3d 112` / `No. 20-157` で文が切れないことを含め、
**出力を `check_caption_breaks.py` に食わせて exit 0 まで自動確認。**

## 8.5 実行
```bash
$PY scripts/gen_captions_caniglia.py --narr episodes/PD-2026-043-caniglia/06_audio/narration_index.stub.v001.json
$PY scripts/check_caption_breaks.py episodes/PD-2026-043-caniglia/08_edit/captions.final.v001.srt
# → PASS が出るまで直す。ゲート側の閾値を緩めるのは禁止。
```

---

# 9. 5ゲートの実際の判定（**build 後に必ず全部通す・animation_mix を忘れるな**）

| ゲート | 実体 | 入力 | EP43 の通過根拠 |
|---|---|---|---|
| `check_asset_reuse.py <film.json>` | factory≤1 / motion≤2 / still≤2 / first-use≥0.70 | **film.json 位置引数** | §5.2: factory1.00 / motion2.00 / still1.19 / first-use **0.8584** |
| `check_motion_density.py --ep PD-2026-043-caniglia` | film.json の graphics+figures+heroCuts のみ / density≥2.5・coverage≥0.25・variety≥3（**AND**） | **`--ep`** | §6.1: **3.08 / 27.7% / 12+種**（AEカードは0本＝§0.5-2・beats≥31） |
| `check_animation_mix.py --ep PD-2026-043-caniglia` | film.json の cuts を img=still/その他=footage 分類 / still-share≤0.45・motion-cov≥0.45 | **`--ep`** | §5.2[C]: still-share **0.4469(cut)/0.4201(frame)** / motion-cov **0.5531+** |
| `check_caption_breaks.py <srt>` | A/B/C 各0件 | **srt 位置引数** | §8 の構文境界生成器 |
| `check_script_length.py <script> --json` | 総語数 / wpm / narration_seconds | **script 位置引数** | 2,141語 / wpm178.1 / **721.3s** |

> **★ゲートの入力指定（ブリーフ§5）:** density/mix は **`--ep PD-2026-043-caniglia`**。**`--json <film.json>` は出力パス
> （上書き事故）なので入力に使わない。** asset_reuse は film.json 位置引数、caption_breaks は srt 位置引数、script_length は script 位置引数。
>
> **`check_animation_mix` は `04_scenes/premium_beatsheet.v*.json` があればそれを優先する。**
> §5.6 の通り B の beatsheet は `caniglia_beatsheet`（`premium_` 無し）なので**auto-detect されず film.json を測る。**

---

# 10. OP バンパー `OpeningCaniglia`（Remotion・fps60/1920x1080/180f）

## 10.1 二重OPを作らない
本編（`Ep43Caniglia`）の OP は `Bookends.tsx` の `BrandOpening` のまま（`op_ed_bookends` ゲート・フォーク禁止）。
`OpeningCaniglia` は**独立したタイトルバンパー成果物**（`out/caniglia_opening.mp4`。Shorts/予告/SNS 用）。**本編に ffmpeg で焼き込まない。**

## 10.2 Composition 設定
| 項目 | 値 |
|---|---|
| `id` | `OpeningCaniglia` |
| 解像度 / fps / duration | **1920×1080 / 60 / 180**（=3.0秒） |
| component | `remotion/src/compositions/OpeningCaniglia.tsx` |

```tsx
import {OpeningCaniglia, openingCanigliaDurationInFrames} from './compositions/OpeningCaniglia';
import canigliaOpeningProps from '../props/caniglia.json';
<Composition id="OpeningCaniglia" component={OpeningCaniglia}
  width={1920} height={1080} fps={60}
  durationInFrames={openingCanigliaDurationInFrames(60)} defaultProps={canigliaOpeningProps}/>
```

**依存:** `@remotion/motion-blur`（未導入時のみ `cd remotion && npm i @remotion/motion-blur`）。
**`remotion/remotion.config.ts`** は既に正典値（png / h264 libx264 / CRF16 / yuv420p / bt709 / aac 320k / 全コア並列 / angle）。**一致確認のみ・書き換えない。**

## 10.3 秒数ベースのタイムライン（fps=60・フレーム直書き禁止・全て `Math.round(fps*秒)`）

| 秒 | 起きること | 手法 |
|---|---|---|
| 0.00–0.40 | L1 グラデ背景 opacity 0→1・**同時に scale 1.08→1.00（`Easing.out(Easing.cubic)`）** | interpolate（opacity 単独禁止・scale と併用） |
| 0.10 | ロゴ（`hasLogo`）左上に spring・scale 0.4→1.0・opacity 0→1 | spring `damping:14,mass:0.9` |
| 0.15–0.25 | L2 グリッド reveal（opacity→0.18）＋ translateY 0→48px | spring `damping:200,mass:1` + `Easing.inOut(Easing.sin)` |
| 0.25 | L3 グロー（porch-amber `#E0913C`）scale 0.6→1.15 / opacity 0→0.85 | spring `damping:18,mass:1.2`（併用） |
| 0.30–0.86 | L4 主役タイトルが1文字ずつ切れ上がり（translateY 110%→0）＋ opacity。スタッガー **2f/文字**。全体を `Trail(layers=6,lagInFrames=1.2,trailOpacity=0.45)` で包む | spring `damping:16,mass:1` |
| 0.55–1.15 | L2b **玄関ドアのスリット**（中央から縦の細い暖色光 `scaleX 0→1`＋opacity 0→0.5・「閉じた戸→開く戸」のモチーフ） | spring `damping:22,mass:1.1`・`transformOrigin:'center'`・**motionBlur** |
| 0.95–1.35 | L5a アクセント下線（porch-amber）左から `scaleX 0→1` | spring `damping:16,mass:0.8`・`transformOrigin:'left center'` |
| 1.10–1.55 | L5b サブタイトル translateY 24→0 + opacity 0→1 | spring `damping:20,mass:1`（併用） |
| 1.55–3.00 | settle→ホールド。**完全静止フレーム無し・フェードアウトしない** | — |

> **等速線形を1箇所も使わない。opacity 単独の演出を1箇所も作らない**（全 opacity が translateY/scale/scaleX と対）。

## 10.4 props 型と値
```ts
export type OpeningCanigliaProps = { title:string; subtitle:string; accent:string; hasLogo:boolean };
```
`remotion/props/caniglia.json`: `{ "title":"THE WELFARE CHECK", "subtitle":"CANIGLIA V. STROM", "accent":"#E0913C", "hasLogo":true }`
`remotion/props/caniglia_short.json`: `{ "title":"AT YOUR DOOR", "subtitle":"WHAT THE LAW ALLOWS", "accent":"#E0913C", "hasLogo":false }`
> `subtitle`/`title` も §2 の R-FORBID/R-FACE/R-DOC 検査対象（`remotion/props/caniglia*.json`）。ルート背景は INK 近黒 `#0A0A0C`。
> **accent は EP41 gold / EP42 blue を書かず porch-amber `#E0913C`（レーン分離）。**
> **「令状なしに家に入れない」断定・「全面勝訴」を subtitle に書かない（C-1/C-2）。**

## 10.5 量産
```bash
cd remotion && npm run studio     # OpeningCaniglia を 0→180f スクラブして §10.3 の各時刻を目視
npx remotion render OpeningCaniglia out/caniglia_opening.mp4 --props=./props/caniglia.json
npx remotion render OpeningCaniglia out/caniglia_short_op.mp4 --props=./props/caniglia_short.json
```

---

# 11. サムネ3案（`CanigliaThumbnails.tsx`・`<Still>` 1280×720・Root に `Thumb-caniglia-01..03`）

**共通要件:** 見出し全て大文字・4語以内・320pxで判読 / **実在人物の肖像禁止（R1・Caniglia の顔/身体を出さない・C-4）** / INK 黒 `#0A0A0C` bg + porch-amber `#E0913C` /
背景は body 静止画のうち `also_thumb==true` の6枚（象徴オブジェのみ・C-4/C-5。**サムネ専用の分類は無い＝also_thumb フラグを読む**） / `thumbnail_visibility`（luma平均≥33＋コントラスト）を通す。目標CTR 6%+。3案は6枚から選ぶ。
**「令状なしに家に入れない」断定・「全面勝訴」を出さない（R-FORBID/R-SCOPE/R-VOTE99）。**

**★also_thumb 6枚（still 資産 ID 空間 S01..S85＝CODEX_A §5.9。B のスタブが立てる・A のマニフェストと**一字一致必須**の A↔B 契約点。CODEX_A §4.3 と同一6 asset ID に `also_thumb:true`）:**
`S01`（食卓の拳銃1丁）/ `S24`（一軒家前の救急車・赤色灯）/ `S28`（布の上の拳銃2丁）/ `S30`（朝・大きく開いた玄関ドア）/ `S49`（大理石の9つの空席）/ `S81`（昼光を背にした開いた玄関ドア）。
> サムネ component は**マニフェストの `also_thumb` フラグを読んで**背景を選ぶ（scene id をハードコードしない）。スタブ生成器はこの6 asset ID に立てる。**この6 ID は CODEX_A §4.3・§13 の also_thumb と完全一致**（`check_caniglia_asset_manifest` §3.3-12 が集合一致を検査）。

- **T1「布の上の2丁」（最推奨）:** 布の上の拳銃2丁（顔なし・**S28** 系）。文字 **`THEY TOOK HIS GUNS`**（4語）。`TOOK` を porch-amber。**"no warrant" の視覚化＝C-1（射程は過大化しない）。**
- **T2「9–0」（数字勝負）:** 大理石の空の9席を暗く落とし（**S49** 系）、前面に **`9–0`**（大）＋ **`ONE EXCUSE, CLOSED`**（下・**C-2 の限定併記必須**）。数字は F03 の検証済み値のみ。
- **T3「開いた戸」（尊厳）:** 昼光を背にした開いた玄関ドア（**S81** 系）。文字 **`AT YOUR DOOR`**（3語）。`YOUR` を porch-amber。温存された緊急の扉のモチーフ（C-1）。

**A/Bタイトル候補（`09_package`・60字以内・二人称・台本のとおり）:**
- **A:** `Police Came for a Welfare Check. They Left With His Guns.`
- **B:** `Can Police Enter Your Home to "Help" — and Take What They Find?`
> ※「警察は令状なしに家に入れないと最高裁が決めた」系のタイトルは**禁止**（C-1/R-SCOPE）。

**固定コメント** `09_package/pinned_comment.v001.txt`（§2 の R-LEDGER/R-ATTRIB/R-FORBID/R-VOTE99/R-SCOPE/R-CADY 検査対象。台帳事実のみ・**988 を含む＝R-988**）:
```
Two things this case actually decided — and two it did not.

DECIDED: There is no free-standing "community caretaking" exception that lets police
enter your HOME without a warrant. Cady v. Dombrowski (1973) was about a CAR in police
custody, not a house. The Court was unanimous, 9-0, but the ruling is narrow: it vacated
the decision below and sent the case back — not a final victory for Edward Caniglia.

LEFT OPEN: A valid warrant, your consent, and a genuine emergency (exigent circumstances,
including rushing in to help someone seriously hurt) all still let officers cross the
threshold. Justice Alito flagged red-flag gun laws and suicide-prevention seizures as
questions for another day.

If you or someone you know is in crisis, call or text 988 (Suicide & Crisis Lifeline).
```

---

# 12. 本編コンポジション登録（`remotion/src/Root.tsx`・`Ep42Young`/`Ep38KidsForCash` の形を踏襲）
```tsx
import canigliaFilm from './data/caniglia_film.json';
<Composition id="Ep43Caniglia" component={CaseFilm}
  durationInFrames={caseFilmDurationInFrames(canigliaFilm as unknown as FilmData, BRAND.video.fps)}
  fps={BRAND.video.fps} width={BRAND.video.width} height={BRAND.video.height}
  defaultProps={{ data: canigliaFilm as unknown as FilmData, seriesLabel: 'PRIME DOCUMENTARY',
    title: 'Police Came for a Welfare Check. They Left With His Guns.',
    subtitle: 'One excuse, taken off the table. The warrant, your consent, and every real emergency still stand.' }}/>
```
> **id は正確に `Ep43Caniglia`（切り詰め・綴り違い・大文字化の誤記に注意）。** `remotion/src` に現在 `caniglia` の文字列が無いこと（衝突しない）を確認してから追記。
> `title`/`subtitle` も §2 検査対象（R-FORBID/R-VOTE99/R-SCOPE）。**「全面勝訴」「令状なしに家に入れない」断定を書かない。**

---

# 13. 受入（自分で exit 0 を確認してから完了報告）
```bash
cd C:\Users\aab15\Documents\prime-documentary ; PY=./.venv/Scripts/python.exe

# 0. 語数（最優先・課金前に落とす）
$PY scripts/check_script_length.py episodes/_planning/EP43_caniglia_script.en.v001.md --json   # 2,141語 / wpm178.1 / 721.3s

# 1. 事実性/6制約（EP43固有・正確性ゲートはこの1本）
$PY scripts/check_caniglia_facts.py --json

# 2. 契約バリデータ
$PY scripts/validate_caniglia_beats.py
$PY scripts/check_caniglia_asset_manifest.py --assets episodes/PD-2026-043-caniglia/05_visuals/asset_manifest.v001.json

# 3. ★5ゲート（animation_mix を忘れるな・入力は --ep / 位置引数を厳守）
$PY scripts/check_asset_reuse.py    remotion/src/data/caniglia_film.json
$PY scripts/check_motion_density.py --ep PD-2026-043-caniglia
$PY scripts/check_animation_mix.py  --ep PD-2026-043-caniglia
$PY scripts/check_caption_breaks.py episodes/PD-2026-043-caniglia/08_edit/captions.final.v001.srt

# 4. 水増し・レンダ前プリフライト
$PY scripts/check_padding.py --ep PD-2026-043-caniglia --json
$PY scripts/preflight_render_gate.py --ep PD-2026-043-caniglia

# 5. 本編レンダ（slim public・並列4）→ BGM → AEカード合成
cd remotion
npx remotion render Ep43Caniglia out/caniglia.mp4 --public-dir=public_slim --concurrency=4
#   public_slim は caniglia_film.json が参照する素材（+ 各 <stem>_depth.png）だけを含む slim public。
#   無ければ referenced paths を public_slim/ にコピーして作る（remotion/public/caniglia 本体を痩せさせない）。
cd ..
$PY scripts/build_caniglia_bgm.py
$PY scripts/ae/composite_caniglia_hero.py

# 6. 本編最終受入（episode番号は★位置引数・--ep ではない）
$PY scripts/check_final_acceptance.py 43 \
  --render episodes/PD-2026-043-caniglia/08_edit/caniglia_final_bgm.v003_ae.mp4 --emit-receipt
```

| ゲート | EP43 目標値 |
|---|---|
| `check_script_length` | 総語数 **2,141** / `wpm 178.1` / narration **721.3s** |
| `check_asset_reuse` | factory≤1 / motion≤2 / still≤2 / first-use **0.8584**（floor0.70） |
| `check_motion_density` | density **3.08**/min / coverage **27.7%** / variety 12+（floors 2.5 / 0.25 / 3・beats **≥31**） |
| `check_animation_mix` | still-share **0.4469(cut)/0.4201(frame)**（cap0.45）/ motion-cov **0.5531+**（floor0.45） |
| `check_caption_breaks` | 行末機能語0 / 孤立キュー0 / hard split 0 |
| `check_caniglia_facts` | violations = 0（台帳照合・9-0限定・帰属・6制約・R-FORBID・R-VOTE99・R-SCOPE・R-CADY・R-JARDINES） |
| runtime band | 11.5–12.5分（narration 721.3s + bookends・total≤750s） |
| factory クリップ | ≥24本 → **93本** |
| image_resolution | 全静止画 長辺 ≥3840px |
| thumbnail | 3案 @1280×720 + selected luma≥33 |
| op_ed_bookends | `BrandOpening`/`BrandEndcard` を import（フォーク禁止） |

**全て exit 0 でなければ `package_ready` にしない。自己申告QCは無効。QC基準を書き換えて通すのは禁止。**

## 13.1 完成後の全編アイボール（**1フレーム判定禁止＝EP39-41 実害**）
`caniglia_final_bgm.v003_ae.mp4` を **0→末尾まで通しで実視聴**し、以下を確認してから完了報告:
- 紙芝居感が無い（still が連続していない・footage が体感で過半）
- AEカード8枚が全て焼き込まれ数値が台帳と一致（「令状なしに家に入れない」断定・「全面勝訴」がどこにも無い）
- **9-0 のカード v01 に "ONE EXCUSE, CLOSED"、差戻し r01 に "VACATE AND REMAND / SENT BACK DOWN - NOT ENDED IN HIS FAVOR" が読める（C-2・"final win" 系はどこにも無い）**
- **c01 が「A CAR IN CUSTODY / NOT A HOME」で車と家を分離、Cady を住居事案として描いていない（C-3）**
- **s01/ENDING に "WARRANT - CONSENT - EMERGENCY — STILL OPEN"（温存例外・C-1）が読める。988 は画面カード（AEデッキ/figures）に無く、概要欄/固定コメント/BrandEndcard のみ（R-988）**
- Thomas 逐語が Thomas 帰属、"the right of a man to retreat into his own home" が **Jardines 帰属**（Payton ではない・C-6/C07）
- Payton は "presumptively unreasonable"（1980）で別命題として提示（C-6）
- Edward Caniglia の顔・身体・肖像が無い（象徴＝食卓の拳銃/空のポーチ/救急車の赤色灯/玄関/電話/証拠タグのみ・C-4）
- メンタルヘルスが非扇情（"shoot him" は1回・手段描写なし）／**988 が endcard/概要欄にある（C-5）**
- 生成ビジュアル表示中は `AI-assisted visualization` が右下に常時（**AEカード8枚の表示中も**開示が見える＝カード共通スタックに焼かれている・R1・§7.3/§7.9）
- accent が porch-amber `#E0913C`（EP41 gold / EP42 blue が紛れていない）
- 音ズレ・字幕ズレ・尺差（base と <=0.5s）が無い

---

# 14. 絶対にやらないこと
- **EP39 / EP40 / EP41 / EP42 のファイル・素材に触らない**（読み取りのみ可）。レーンを分離する。
- **スレッドAの所有ファイル（§0.2.1）に書かない**（`05_visuals/` `05_stock/` `remotion/public/caniglia/` `H:\...\ai\caniglia\`）。**B の provenance は `04_scenes/caniglia_build_manifest.v001.json` に書く。**
- **設計書 / `EP43_caniglia_CODEX_A_*` / PD-2026-039〜042 に触らない。**
- **課金ジョブを起動しない**（ElevenLabs TTS / 課金画像生成API / YouTube アップロード）。narration_index はスタブで着手。
- **公開済み・出荷済み mp4 を上書き・再レンダしない**（出力は必ず `_v003_ae`）。
- **台帳（§2）に無い数値を焼かない**（$580,000 の再発防止）。不明値は `verified:false` でカード除外。
- **`FigureSpec` の `kind` を推測で書かない**（§6.2 の実在小文字値のみ。大文字名は無言で消える。`comparebars` は非在→`compbars`）。
- **`--variants` という語を書かない**（1シーン1枚・バリエーション0＝ブリーフ§1。SDXL は A の領分で 1 固定）。
- **asset_manifest の `counts`/`role` enum/`overlay` 枚数を CODEX_A と食い違わせない**（`role` は `body`/`i2v_source`/`reject` の3値のみ・**`thumb`/`still_thumb` を作らない**・overlay=12）。
- **「令状なしに家に入れない」「全面勝訴／事件終結」を断定しない**（C-1/C-2・R-SCOPE/R-VOTE99）。**Cady を家の事案にしない**（C-3・R-CADY）。**メンタルヘルスを扇情化しない・988 を落とさない**（C-5・R-CRISIS/R-988）。**Edward Caniglia の顔/肖像/身体を出さない**（C-4・R-CANIGLIA/R-FACE）。
- **accent に EP41 gold / EP42 warrant-blue を使わない**（porch-amber `#E0913C` のみ）。
- **スタブと本番でコードパスを分岐させない**（§0.2）。
- **スペック数値（226 cuts / still85 / factory93 / motion16 / distinct194 / first-use0.8584 / still-share0.4469 / figures≥31 / 721.3s / 2,141語 / 48シーン / mean_shot3.19 / total≤750s）を変えない。**
- **実在しないスクリプト名を書かない**（新規は §0.3 の一覧のみ・複製元を明記）。**composition id は `Ep43Caniglia`（切り詰め・綴り違い注意）。** **PowerShell 経由で正規表現/エスケープを生成しない**（`\b` バックスペース化の実害）。
