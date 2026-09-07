# EP41 thompson — Codex スレッドB「実装」引き継ぎプロンプト v001

> **このファイルは単体で完結している。他のファイルを読まなくても着手できる。**
> 並行して走っているスレッドA（素材生成）のファイル `EP41_thompson_CODEX_A_*.md` は**読まない**。
> 設計書 `EP41_thompson_DESIGN*.md` も**読まない**（必要な数値はすべて本書に転記済み）。
> `EP41_thompson_PRODUCTION_SPEC.v001.json` の数値は本書に転記済み。**あなたはこれを書き換えない。**

```
あなたは Prime Documentary（YouTubeドキュメンタリーチャンネル）の制作エンジニアです。
リポジトリ: C:\Users\aab15\Documents\prime-documentary
Python:     C:\Users\aab15\Documents\prime-documentary\.venv\Scripts\python.exe
メディア:   H:\pd-media
担当:       EP41 / Episode ID: PD-2026-041-thompson / slug: thompson
```

**題材:** *Connick v. Thompson*, 563 U.S. 51 (2011)。ルイジアナ州が John Thompson を処刑する約1か月前、
調査員が14年間隠されていた1枚の検査報告書（血液型B、Thompson は型O）を発見。隠したのは検察官だった。
再審で無罪、陪審は1,400万ドルの賠償を認めたが、**最高裁が5対4で覆し、1ドルも支払われなかった**。
主役 John Thompson（故人・exoneree）。

> **★EP40 Lech との決定的な違い:** EP40 は「最高裁は関与していない（cert. denied のみ）」だった。
> **EP41 は逆で、最高裁が本案を5対4で判断した実在の最高裁判決である。** `Supreme Court` を禁止語にするな。
> EP41 の R1 は別物（§2）＝**実在の顔を出さない／実在検察官は認定事実のみ／読める偽公文書を作らない／
> 台帳に無い数値を焼かない**。

---

# 0. このスレッドの責務・境界・完了条件

## 0.1 このスレッド（B）の責務 — **コード律速。素材を1点も待たずに全部書ける。**

| # | 作業 | 成果物 |
|---|---|---|
| B-1 | エピソードディレクトリと `manifest.json` | `episodes/PD-2026-041-thompson/**` |
| B-2 | 境界契約マニフェストの**消費側**バリデータ＋スタブ素材生成 | `scripts/check_thompson_asset_manifest.py` / `scripts/make_thompson_stub_assets.py` |
| B-3 | スタブ narration_index 生成器（TTS 不要で通しを回す鍵） | `scripts/make_thompson_stub_narration.py` |
| B-4 | 事実台帳 F-ID とR1ゲート（**EP41固有・BLOCKING**） | `scripts/check_thompson_facts.py` |
| B-5 | `thompson_film.json` ビルダ（**asset_map→manifest変換＋beatsheet生成／footage混在**） | `scripts/build_thompson_film.py` |
| B-6 | beats バリデータ（AEとRemotionの区間衝突検査＋ledger/R1） | `scripts/validate_thompson_beats.py` |
| B-7 | **構文境界で切る字幕生成器** | `scripts/gen_captions_thompson.py` |
| B-8 | **After Effects カード**のビルダとコンポジタ | `scripts/ae/build_thompson_hero_cards.py` / `scripts/ae/composite_thompson_hero.py` |
| B-9 | Remotion 本編コンポジション登録 `Ep41Thompson` | `remotion/src/Root.tsx` |
| B-10 | OP バンパー `OpeningThompson`（fps60/1920x1080/180f） | `remotion/src/compositions/OpeningThompson.tsx` |
| B-11 | サムネ3案 | `remotion/src/compositions/ThompsonThumbnails.tsx` |
| B-12 | **スタブでの通しドライラン** | `episodes/PD-2026-041-thompson/08_edit/_dryrun/**` |

## 0.2 もう一方のスレッド（A）との境界 — **接続点はただ1ファイル。**

```
episodes/PD-2026-041-thompson/05_visuals/asset_manifest.v001.json
   ↑ Aが生成（唯一の生産者）        ↓ Bが消費（唯一の消費者）
```

**Bはこのファイル以外のAの中間生成物を読まない。そして Bはこのファイルが無くても完走できる。**
`make_thompson_stub_assets.py` が**まったく同じスキーマの** `asset_manifest.stub.v001.json` を作るので、
Bはそれで全パイプラインを通す。

> **★絶対条件: スタブと本番でコードパスを分岐させてはならない。**
> `build_thompson_film.py --assets <path>` は渡されたマニフェストを読むだけで、`is_stub` の値によって
> **処理を変えない**（`is_stub` はログと受入判定にだけ使う。カット組み立てロジックには一切使わない）。

### 0.2.1 ファイル所有権（これを破ると並行作業が壊れる）

| パス | 所有 | Bの権限 |
|---|---|---|
| `episodes/PD-2026-041-thompson/manifest.json` | **B** | 読み書き |
| `episodes/PD-2026-041-thompson/{00_topic,01_research,03_script,04_scenes,06_audio,08_edit,09_package,approvals,events}/**` | **B** | 読み書き |
| `remotion/src/**` `remotion/props/**` | **B** | 読み書き |
| `remotion/public/thompson_dryrun/**` | **B** | 読み書き（スタブ素材の staging 先） |
| `scripts/*thompson*.py` / `scripts/ae/*thompson*.py`（§0.3） | **B** | 新規作成 |
| **`episodes/PD-2026-041-thompson/05_visuals/**` `05_stock/**`** | **A** | **読み取りのみ。書くな** |
| **`H:\pd-media\assets\ai\thompson\**` / `ai_video\thompson\**`** | **A** | **読み取りのみ。書くな** |
| **`remotion/public/thompson/{img,factory,motion,overlay}/**`** | **A** | **読み取りのみ。書くな** |
| `EP41_thompson_DESIGN*.md` / `EP41_thompson_CODEX_A_*.md` | **設計/Aスレッド** | **触るな** |
| `EP41_thompson_PRODUCTION_SPEC.v001.json` / `EP41_thompson_script.en.v001.md` | **上流** | **読み取りのみ。書くな** |
| `episodes/PD-2026-039-*/**` / `episodes/PD-2026-040-*/**` / それらの素材 | **他エージェント** | **絶対に触るな** |

> **B は `remotion/public/thompson/` に書かない。** スタブは **`remotion/public/thompson_dryrun/`** に置く。
> 本番マニフェストが来たら `--assets` を差し替えるだけで `thompson/` を参照するようになる。

## 0.3 B が新規作成するスクリプト（これ以外を新規に作らない。既存を改変しない）

| パス | 役割 | 手本（**改変せず読んで踏襲**） |
|---|---|---|
| `scripts/check_thompson_asset_manifest.py` | §3.3 消費側バリデータ | — |
| `scripts/make_thompson_stub_assets.py` | §3.4 スタブ素材＋スタブマニフェスト＋スタブ黒ベース | — |
| `scripts/make_thompson_stub_narration.py` | §4.4 スタブ narration_index | — |
| `scripts/check_thompson_facts.py` | §2 R1＋台帳（BLOCKING） | — |
| `scripts/build_thompson_film.py` | §5 film.json＋manifest＋beatsheet＋SRT | `scripts/build_lech_film.py` |
| `scripts/validate_thompson_beats.py` | §7.9 不変条件 | — |
| `scripts/gen_captions_thompson.py` | §8 構文境界字幕生成器 | `scripts/gen_captions_lech.py` |
| `scripts/ae/build_thompson_hero_cards.py` | §7 AEカードビルダ | `scripts/ae/build_lech_hero_cards.py` |
| `scripts/ae/composite_thompson_hero.py` | §7.10 コンポジタ | `scripts/ae/composite_lech_hero.py` |

> **既存の `scripts/gen_captions_case.py` / `scripts/build_lech_film.py` 等は触らない**（他エピソードが使用中）。
> EP41用に**新規コピーして**パスと定数だけ差し替える。

## 0.4 完了条件（スタブだけで、全て緑になったら「実装完了」）

```bash
cd C:\Users\aab15\Documents\prime-documentary
PY=./.venv/Scripts/python.exe

# [B-DONE-1] スタブ素材・スタブ黒ベース・スタブ narration を揃える
$PY scripts/make_thompson_stub_assets.py
$PY scripts/make_thompson_stub_narration.py

# [B-DONE-2] マニフェスト消費側バリデータ（スタブ相手に通ること）
$PY scripts/check_thompson_asset_manifest.py \
  --assets episodes/PD-2026-041-thompson/05_visuals/asset_manifest.stub.v001.json

# [B-DONE-3] 字幕（スタブ narration の実文から構文境界で生成）
$PY scripts/gen_captions_thompson.py \
  --narr episodes/PD-2026-041-thompson/06_audio/narration_index.stub.v001.json
$PY scripts/check_caption_breaks.py \
  episodes/PD-2026-041-thompson/08_edit/captions.final.v001.srt

# [B-DONE-4] film.json をスタブから組み立てる（footage 混在必須）
$PY scripts/build_thompson_film.py \
  --assets episodes/PD-2026-041-thompson/05_visuals/asset_manifest.stub.v001.json \
  --narr   episodes/PD-2026-041-thompson/06_audio/narration_index.stub.v001.json \
  --out    remotion/src/data/thompson_film.json

# [B-DONE-5] ★4ゲート全部（今日の見落とし = animation_mix を絶対に忘れるな）
$PY scripts/check_asset_reuse.py     remotion/src/data/thompson_film.json
$PY scripts/check_motion_density.py  --ep PD-2026-041-thompson
$PY scripts/check_animation_mix.py   --ep PD-2026-041-thompson
$PY scripts/check_caption_breaks.py  episodes/PD-2026-041-thompson/08_edit/captions.final.v001.srt

# [B-DONE-6] 事実性/R1（スタブの文字列にも適用）
$PY scripts/check_thompson_facts.py --json --dryrun

# [B-DONE-7] beats 契約（AE区間 と Remotion figures[] が1秒も重ならない）
$PY scripts/validate_thompson_beats.py --dryrun

# [B-DONE-8] AE カードをビルド＋レンダ＋コンポジット（ドライラン出力へ）
$PY scripts/ae/build_thompson_hero_cards.py --dryrun
"C:/Program Files/Adobe/Adobe After Effects 2026/Support Files/AfterFX.exe" -noui \
  -r "C:/Users/aab15/Documents/prime-documentary/episodes/PD-2026-041-thompson/08_edit/_dryrun/ae_hero/thompson_hero.jsx"
$PY scripts/ae/composite_thompson_hero.py --dryrun

# [B-DONE-9] Remotion Studio で目視
cd remotion && npm run studio
#   → Ep41Thompson / OpeningThompson / Thumb-thompson-01..03 が出て、実際に動くこと
```

**台本は既に確定済み**（`EP41_thompson_script.en.v001.md`）。したがって本番 narration_index が来たら
`--narr` を差し替え、[B-DONE-3]〜[B-DONE-8] を全部やり直す。**「スタブで通ったから本番も通るはず」は禁止。**

---

# 1. 実装前に必ず読むファイル（**推測で書くな**）

| パス | なぜ読むか |
|---|---|
| `scripts/build_lech_film.py` | **film.json ビルダの唯一の実証実装。** best-pick / tile_window / allocate / build_figures をそのまま踏襲する。**ただし EP40 は静止画100%だった。EP41 は §5 で footage を必ず混ぜる（§0.5 の紙芝居回避）** |
| `scripts/ae/build_lech_hero_cards.py` | **AEカードビルダの唯一の実証実装。** `money_keys()`（Pythonで表示文字列を全事前計算）/ `fit_size()` / CARDS デッキ構造 / レイアウト定義 / 完了マーカーをそのまま踏襲 |
| `scripts/ae/composite_lech_hero.py` | **コンポジタの唯一の実証実装。** SKIP4条件（missing / 解像度不一致 / 実測尺不足 / window past end）と ffmpeg フィルタグラフ（overlay/blend）をそのまま踏襲 |
| `scripts/gen_captions_lech.py` | **構文境界字幕の唯一の実証実装。** `internal_split()` / `chunk_sentence()` / `NO_DANGLE_END` import をそのまま踏襲 |
| `remotion/src/compositions/CaseFilm.tsx` | `FilmData` 型 / `caseFilmDurationInFrames` / `depthSrcOf()` |
| `remotion/src/components/FigureBeats.tsx` | `FigureSpec` の**実在する `kind` 文字列**（§6.2 の警告を必ず読め） |
| `remotion/src/components/Bookends.tsx` | `OPENING_SEC` / `ENDCARD_SEC` / `BrandOpening` / `BrandEndcard` |
| `scripts/check_asset_reuse.py` / `scripts/check_motion_density.py` / `scripts/check_animation_mix.py` / `scripts/check_caption_breaks.py` | 通すべき4ゲートの**実際の判定ロジック**（§9） |
| `C:\Users\aab15\Documents\pino-channel\remotion\src\Opening.tsx` | §10 の OP 正典実装 |

---

# 0.5 ★★★ EP39/40 で踏んだ失敗＝最初から防ぐ（本書の全体設計はこの6点を構造で潰している）★★★

1. **紙芝居（最重要）** — `build_lech_film.py` は**静止画100%**で組んだ結果 `check_animation_mix` が FAIL し、
   後から71本の実写を足して直した。**EP41 は最初から footage を混ぜる。**
   `check_animation_mix.compute_metrics_from_film()` は film.json の `cuts[]` を
   **`kind=="img"` → still（WilliamsScene 扱い）/ それ以外 → footage（motion 扱い）** と分類する。
   したがって **film.json に `kind:"footage"` のカットが十分に無いと still-share > 0.45 で必ず落ちる。**
   → §5 の cuts 構成は **factory 88 + motion 30 の footage を最初から入れて still-share を frame ベースで ≤0.44** にする。
2. **AEカードは密度に数えられない** — `check_motion_density` は film.json の `graphics+figures+heroCuts` **のみ**数える。
   AEカードは ffmpeg で後合成するので**1本も数えられない**。
   → §6 で **film.json 側の `figures[]` を ≥34 本**（spec 下限29の余裕込み）置く。AEカードは別勘定。
3. **FigureSpec の `kind` は実在の小文字値のみ** — 大文字名（`ActTitle`/`QuoteCard` 等）は無言で描画が消える（§6.2）。
4. **台帳に無い数値を焼くな** — EP40 の生 Codex-B 出力に架空の $580,000・捏造間取りが入って**不採用になった実害**。
   → §2 の事実台帳 F-ID に**検証済み値だけ**を置き、`check_thompson_facts.py` が film.json/AE/サムネの
   全数値を台帳照合する。台帳に無い数値・`verified:false` の数値を焼いたら FAIL。
5. **字幕は台本本文と対応** — EP38 で台詞混入・「final」誤称の実害。
   → §8 の字幕は **narration_index の実チャンク文をそのまま** verbatim で使う（自作しない）。
6. **レンダー前ゲート** — build 後に `check_asset_reuse` / `check_motion_density` / `check_animation_mix` /
   `check_caption_breaks` を**全部**通す（§9・§13）。**animation_mix を忘れるな＝今日の見落とし。**

---

# 2. ★ EP41固有のR1・事実性ロック（`scripts/check_thompson_facts.py`・BLOCKING）

> **この節に違反した成果物は、他が全て完璧でも出荷不可。**

## 2.1 EP41 の事実（台本 `EP41_thompson_script.en.v001.md` と事実対応表から確定）

**Connick v. Thompson は実在の最高裁判決。** したがって `Supreme Court` は**禁止語ではない**（EP40 と逆）。
ただし次を厳守する:

| 項目 | 正しい記述 | 禁止 |
|---|---|---|
| 判決 | **合衆国最高裁が5対4で覆した**（`Connick v. Thompson, 563 U.S. 51 (2011)`） | 5-4を「全員一致」等に誤る |
| 判決日 | **2011年3月29日**（口頭弁論 2010年10月） | 別年 |
| 多数意見 | **Thomas 執筆**（Roberts / Scalia / Kennedy / Alito） | 認定外の帰属 |
| 反対意見 | **Ginsburg**（Breyer / Sotomayor / Kagan）／`standard operating procedure` | 反対を多数と混同 |
| 争点評価 | **多数意見/反対意見に中立帰属**（"the majority said…" / "the dissent said…"） | 断定的に一方を正とする |
| 実在人物 | **顔・肖像を出さない**（後ろ姿・シルエット・顔外し）。実在検察官（Connick / Deegan / Riehlmann）は**認定事実のみ** | 顔／認識可能な人物／人格攻撃 |
| 書類 | **読める判決文・報告書を作らない**（雰囲気のみ・illegible）。象徴オブジェのみ | 読める偽公文書 |

## 2.2 事実台帳 F-ID（`03_script/thompson_facts.v001.json`・**Bが台本から転記して作る**）

**スキーマ版:** `thompson_facts.v1`。各 F-ID は `{"value":..., "unit":..., "verified":bool, "claim_id":"", "quote":""}`。
**台本の事実対応表（claim id）に裏付けのある値だけ `verified:true`。裏付け無しは `verified:false`。**

| F-ID | 内容 | 使う場所 | claim |
|---|---|---|---|
| F01 | 報告書が隠されていた年数 = **14** | fig / AE stat | C09/C11 |
| F02 | 死刑囚房での年数 = **14** | fig / AE stat | C13 |
| F03 | 収監合計年数 = **18** | fig / AE stat | C13 |
| F04 | 現場の血液型 = **"B"** ／ Thompson の血液型 = **"O"** | fig compbars / AE SPLIT | C09 |
| F05 | Deegan が秘密を抱えた年数 = **9** | fig / AE stat | C14 |
| F06 | 処刑期日「設定」日 = **1999-04-16** ／ 処刑「予定」日 = **1999-05-20**（**別物・混同禁止**） | AE date / fig timeline | C12 |
| F07 | 陪審の賠償額 = **$14,000,000**（+ 費用 $1M超） | fig money / AE MONEY | C17 |
| F08 | 最高裁の票 = **5 対 4** | fig votetally / AE VOTE | C03 |
| F09 | 判決日 = **2011-03-29** ／ 口頭弁論 = **2010-10** | fig timeline / AE date | C02 |
| F10 | 血の証拠を知っていた検事の数 = **4** | fig stat（Ginsburg箇所） | C15 |
| F11 | 事件前10年のルイジアナでの別種Brady破棄 = **4件** | fig stat（多数意見箇所・帰属明記） | C22 |
| F12 | 殺害 = **1984**（Liuzza）／ 訴追 = **1985** | fig timeline | C07 |
| F13 | 再審無罪 = **2003** | fig timeline / AE date | C16 |
| F14 | 死去 = **2017** ／ Resurrection After Exoneration 設立（**低確度＝`verified:false`**） | fig lowerthird | C26 |

> **F14 は台本で「低確度（企画ブリーフ準拠）」明示。よって `verified:false`。** §5/§7 の不変条件で、
> `verified:false` の値を要求するカードは**静かに出力から除外**する（`required:false`）か、`required:true` なら
> 本番 exit 1（`--dryrun` は警告続行）。**低確度の年を画面に焼かない。**

## 2.3 `check_thompson_facts.py` の検査（exit 0=PASS / 1=FAIL / 2=スキーマ不一致）

**検査対象ファイル（この一覧をハードコード。存在するものだけ検査し、無いものは `skipped[]` に必ず明記）:**

```
episodes/PD-2026-041-thompson/03_script/thompson_facts.v*.json
episodes/PD-2026-041-thompson/08_edit/ae_hero/beats.json
episodes/PD-2026-041-thompson/08_edit/_dryrun/ae_hero/beats.json
episodes/PD-2026-041-thompson/09_package/*.json        （title / description / thumbnail headlines）
episodes/PD-2026-041-thompson/09_package/*.txt         （固定コメント）
episodes/PD-2026-041-thompson/05_visuals/asset_manifest*.json  （tags / caption_hint / qc.notes）
remotion/src/data/thompson_film.json                   （figures[] / captions[] の全文字列と数値）
remotion/props/thompson*.json                          （title / subtitle）
```

**R-LEDGER（台帳照合・最重要）** — film.json の `figures[]`（`value` / `numKeys` の到達値）、AE `beats[].value` /
`beats[].hero`、サムネ数字に現れる**あらゆる数値**は、`thompson_facts.v*.json` に `verified:true` で存在する値に
**完全一致**しなければ FAIL。**台帳に無い数値を焼いた瞬間に落ちる**（EP40 の $580,000 実害の再発防止）。

**R-SPLIT（5対4の帰属）** — `votetally` は `majority:5, dissent:4` のみ許可。それ以外の票は FAIL。

**R-ATTRIB（中立帰属）** — `quote[].attribution` が空でない。多数意見の主張を含む文字列に反対意見の帰属を付ける等の
取り違えを、`attribution` と `quote` の対応表（下記）で照合。

```python
# 許可された引用と帰属（この対応以外の引用は figures/beats に入れない）
APPROVED_QUOTES = {
  "standard operating procedure": "Justice Ginsburg, dissenting",  # C20
  "trained lawyers":              "Majority (Thomas, J.)",         # C18
}
```

**R-FACE / R-DOC（R1の機械可検部分）** — 検査対象の全文字列に対し、次を FAIL とする:
`readable document` を主張する語（`"legible"` / `"actual court filing"` / `"real report"` を肯定文脈で）や、
実在人物のフルネーム＋断定的人格語の同一文共起（例: `Connick` の直後60字以内に `corrupt` / `evil` 等の
非認定形容）。**認定事実の記述（`office` / `did not train` / `hid the report` 等の判決由来語）は許可。**

**R-DATE（日付の分離）** — F06 の 2つの日付が同一カード内で混同されていないこと
（`1999-04-16` を「処刑された日」と書いたら FAIL。設定日=4/16 / 予定日=5/20）。

**出力:** `episodes/PD-2026-041-thompson/09_package/facts_lock.v001.json`（`{"pass":bool,"violations":[...],"skipped":[...]}`）。
**`pass:true` でない限り `check_final_acceptance.py` に進んではならない。**
**CLI:** `--json` / `--dryrun`（`_dryrun/` 配下も対象に含める）。台本確定済みでも対象ファイルが未生成なら
そのファイルをスキップして exit 0。**「無いから通した」を黙るな。必ずログに出す。**

---

# 3. ★境界契約: `asset_manifest.v001.json`（Aから受け取る唯一のファイル）

## 3.1 スキーマ（**Aが生成する。Bはこの形を前提に読む**）

**スキーマ版:** `thompson_assets.v1`（固定文字列。異なれば **exit 2**）。
EP41 spec の点数に一致: **still 80 / factory 88 / motion 15**（+ サムネ用 still ≥3）。

```jsonc
{
  "schema_version": "thompson_assets.v1",
  "episode_id": "PD-2026-041-thompson",
  "slug": "thompson",
  "generated_at": "2026-07-20T12:00:00+09:00",
  "producer": "scripts/build_thompson_asset_manifest.py",
  "is_stub": false,                          // ★ログと受入判定にだけ使う。処理を分岐させない

  "counts": { "still_body": 80, "still_thumb": 3, "motion": 15, "factory": 88, "overlay": 8 },

  "stills": [
    { "asset_id": "THOM-S01-01", "scene_id": "S01", "role": "body",   // "body"|"thumb"|"reject"
      "act": 1,                              // 0=HOOK/OP, 1..4=幕, 5=ED, 9=サムネ専用
      "public_path": "thompson/img/S01_01.png",   // ★Bが cuts[].src に入れる値
      "width": 3840, "height": 2160,
      "sha256": "...", "tags": ["steel door", "cell"], "caption_hint": "the door seats twice a day",
      "source": "ai_codex", "commercial_use": "allowed",
      "qc": {"reviewed": true, "on_theme": true,
             "has_readable_text": false, "has_identifiable_face": false, "notes": ""} }
  ],

  "motion": [
    { "asset_id": "THOM-M01", "source_scene_id": "S18",
      "public_path": "thompson/motion/M01_rife.mp4",   // ★必ず .mp4 かつ "_rife" を含む
      "act": 2, "width": 1280, "height": 720, "fps": 48, "frames": 164, "duration_sec": 3.417,
      "sha256": "...", "tags": ["dawn ceiling"],
      "qc": {"reviewed": true, "on_theme": true, "artifact_free": true, "notes": ""} }
  ],

  "factory": [
    { "asset_id": "AF-BG-0221",
      "public_path": "thompson/factory/AF-BG-0221__empty_courtroom.mp4",  // ★必ず "/factory/" を含む
      "type": "backgrounds", "subtype": "empty_courtroom", "kind": "video",
      "license": "Pexels License", "sha256": "...", "act": 3, "covers_scene_id": "S30",
      "duration_sec": 8.24, "width": 1920, "height": 1080,
      "eyeballed_content": "an empty courtroom, wide static shot, no people",
      "qc": {"reviewed": true, "on_theme": true, "no_watermark": true,
             "no_recognizable_person": true, "no_cartoon": true, "label_matches_content": true, "notes": ""} }
  ],

  "overlay": [
    { "asset_id": "AF-PART-0007",
      "public_path": "thompson/overlay/AF-PART-0007__dust_motes.mp4",
      "type": "particle_assets", "subtype": "dust_motes", "license": "Pexels License",
      "sha256": "...", "blend_hint": "screen",
      "eyeballed_content": "slow drifting dust on black, loops cleanly",
      "qc": {"reviewed": true, "on_theme": true, "no_watermark": true, "notes": ""} }
  ]
}
```

## 3.2 Bがこのマニフェストから作るもの（**EP41 spec の cuts 割当**）

| マニフェスト | Bでの使い道 | spec |
|---|---|---|
| `stills[role="body"]` 80枚 | **静止画カット96本**（`kind:"img"`, `treatment` 循環）・**各≤2回** | still distinct80/cuts96 |
| `stills[role="thumb"]` 3枚 | サムネ3案（§11） | — |
| `motion` 15本 | **i2vカット30本**（`kind:"footage"`）・**各≤2回** | motion distinct15/cuts30 |
| `factory` 88本 | **実写カット88本**（`kind:"footage"`）・**各1回のみ** | factory distinct88/cuts88 |
| `overlay` 8本 | **`cuts[].src` に出さない**（§5.5 の合成レイヤー扱い） | — |

**合計 96 + 30 + 88 = 214 カット / distinct 80+15+88 = 183 / first-use 183/214 = 0.855 ✓（floor 0.70）**

## 3.3 `scripts/check_thompson_asset_manifest.py`（消費側バリデータ・BLOCKING）

```bash
$PY scripts/check_thompson_asset_manifest.py --assets <path> [--json]
```

検査（1つでも違反で exit 1。`schema_version` 違いだけ exit 2）:

1. `schema_version=="thompson_assets.v1"` / `episode_id=="PD-2026-041-thompson"` / `slug=="thompson"`
2. `counts.*` が各配列の実長と一致し**下限**: `still_body>=80` / `still_thumb>=3` / `motion>=15` / `factory>=88` / `overlay>=8`
3. `role in ("body","thumb")` の全静止画で `public_path` 非null、かつ `remotion/public/<public_path>` と
   `remotion/public/<stem>_depth.png` が**両方実在**（`CaseFilm.depthSrcOf()=src.replace(/\.[^.]+$/,'_depth.png')`。**depth 欠落はレンダークラッシュ**）
4. `role!="thumb"` の全静止画で `max(width,height)>=3840`（`preflight_render_gate.MIN_LONG_EDGE_PX=3840`）
5. `motion[].public_path` が `.mp4` で終わり `_rife` を含む（§9 の `kind_of()` 判定用）
6. `factory[].public_path` が `/factory/` を含む
7. `overlay[].public_path` が `/overlay/` を含み `/factory/` を**含まない**
8. `sha256` が全配列を通して一意
9. `factory[].eyeballed_content` が非空、かつ `qc.label_matches_content==true`
10. `qc.has_readable_text` / `qc.has_identifiable_face` が true の項目は `role=="reject"`（**R1**）
11. **全文字列値**が §2 の R-FACE/R-DOC を通る

## 3.4 `scripts/make_thompson_stub_assets.py`（**Aを待たずに完走するための鍵**）

やること:

1. `remotion/public/thompson_dryrun/{img,factory,motion,overlay}/` を作る
2. **静止画スタブ**: PIL で **3840×2160** 単色PNG（`scene_id` と `role` を大書き）＋同名 `_depth.png`
   （**`L` モード**のグラデ。DPTの出力形式に合わせる）。body 80枚 / thumb 3枚 = **83枚 + depth 83枚**
3. **動画スタブ**（ffmpeg `color` フィルタ）:
   - factory 88本: `1920x1080@30fps`・**4.0秒**・`AF-STUB-<NNNN>__stub_clip.mp4`
   - motion 15本: `1280x720@48fps`・**3.417秒**・`M<NN>_rife.mp4`
   - overlay 8本: `1920x1080@30fps`・2.0秒
4. **スタブ黒ベース**: `episodes/PD-2026-041-thompson/08_edit/_dryrun/thompson_final_bgm.v002.mp4` を
   ffmpeg `color=c=black:s=1920x1080:r=30` ＋無音aac で **≈690秒**生成（§7.10 のコンポジタが本番と同じ経路で走れるように）
5. `05_visuals/asset_manifest.stub.v001.json` を **§3.1 と完全に同じスキーマ**で書く
   （`is_stub:true`・`public_path` 先頭を `thompson_dryrun/` に）

**★スタブのパスの罠（外すと `check_asset_reuse.kind_of()` が誤分類して緑になってしまう）:**

```python
p = path.lower().replace("\\", "/")
if "/factory" in p or re.search(r"\baf-bg-", p):                      return "factory"  # 上限1回
if p.endswith((".mp4",".mov",".webm")) or "ai_video" in p or "_rife" in p:  return "motion"  # 上限2回
return "still"                                                                             # 上限2回
```

| 種別 | `public_path` の形 | 満たす条件 |
|---|---|---|
| 静止画 | `thompson_dryrun/img/S01_01.png` | `/factory` を含まない・`.png` |
| factory | `thompson_dryrun/**factory**/AF-STUB-0001__stub_clip.mp4` | **`/factory/` を含む** |
| i2v | `thompson_dryrun/motion/M01**_rife**.mp4` | **`.mp4` かつ `_rife` を含む** |
| overlay | `thompson_dryrun/overlay/...mp4` | **`cuts[].src` に出さない**（出すと factory 判定 = 上限1回で FAIL） |

**スタブの点数は本番と完全に同じ**（body 80 / thumb 3 / motion 15 / factory 88 / overlay 8）。
これで**素材が1枚も無い段階で4ゲート全部の通過を実証できる。**

## 3.5 本番マニフェストへの切り替え — **コードは1行も変えず** `--assets` を差し替えるだけ。
差し替え後、[B-DONE-2]〜[B-DONE-8] を全部やり直す。

---

# 4. narration_index（TTS は課金＝禁止。スタブで着手し、本番で差し替える）

## 4.1 なぜ narration_index か
`build_thompson_film.py` は**尺・区間・字幕を narration_index から導出する**（EP40 `build_lech_film.py` と同じ）。
**秒数をコードに直書きしない。** 唯一の正は narration_index。

## 4.2 スキーマ（`thompson_narration.v1`）

```jsonc
{
  "schema_version": "thompson_narration.v1",
  "episode_id": "PD-2026-041-thompson",
  "is_stub": true,
  "total_seconds": 682.5,
  "chunks": [
    { "section": "HOOK", "start": 0.000, "end": 3.900,
      "text": "A month before the State of Louisiana planned to execute him, an investigator found one sheet of paper." },
    { "section": "OP", "start": 24.500, "end": 28.100, "text": "..." },
    { "section": "ACT_1", "start": 46.400, "end": 50.900, "text": "..." }
  ]
}
```

**section 値（固定）:** `HOOK` / `OP` / `ACT_1` / `ACT_2` / `ACT_3` / `ACT_4` / `ENDING`。
`build_thompson_film.py` は `section_windows()`（各 section の最初のチャンク start）で幕境界を得る。

## 4.3 spec のタイムライン（**設計目標。実タイミングは narration_index が上書きする**）

| section | 語数 | 秒 | 備考 |
|---|---|---|---|
| HOOK | 57 | 19.2 | VO。末尾に `SILENCE 1.8s`（鉄扉残響のみ） |
| （gold `BrandOpening`） | 0 | 3.5 | 非VO。`OPENING_SEC`。**frame0 ではなく HOOK 後に挿入** |
| OP | 65 | 21.9 | thesis + channel ID |
| ACT_1 The Choice | 358 | 120.6 | 逮捕と口を封じられた選択 |
| ACT_2 The Wait | 359 | 120.9 | 14年・死の床の告白。途中に `SILENCE 2.2s` |
| ACT_3 The Verdict | 532 | 179.2 | 無罪・$14M・5対4 |
| ACT_4 The Reach | 259 | 87.3 | Brady・射程 |
| ENDING | 336 | 113.2 | ペイオフ→CTA |
| （`BrandEndcard`） | 0 | 9.0 | 非VO。`ENDCARD_SEC` |

**唯一の正は `python scripts/check_script_length.py <script> --json`。** 総語数 **2,026**（spec `words_total`）/ `wpm 178.1`。
narration_seconds **682.5**（spec）。**自己申告・体感の尺判定は禁止。**

## 4.4 `scripts/make_thompson_stub_narration.py`（**Bはこれで着手できる**）

`EP41_thompson_script.en.v001.md` を読み、**各 section 見出し（`【HOOK】` / `【OP】` / `【BODY 第1幕】`…）配下の
本文を文に割り、178.1 wpm で各文に start/end を割り当てて** `chunks[]` を作る。
`〔SILENCE 1.8s〕` `〔SILENCE 2.2s〕` のト書きは**無音ギャップ**として時間を進める（チャンクにはしない）。
`【OP】` の前に `OPENING_SEC=3.5` の無音を挿入。**F14 の低確度年など台帳外の数値は本文どおり（改変しない）。**
出力: `06_audio/narration_index.stub.v001.json`（`is_stub:true`）。

> **本番:** 別工程が TTS→faster-whisper で `06_audio/narration_index.v001.json`（実測語タイム）を作る。
> **これは課金ジョブなので B は起動しない。** 来たら `--narr` を差し替えるだけ。

---

# 5. `thompson_film.json` の構築（`scripts/build_thompson_film.py`・`build_lech_film.py` に倣う）

## 5.1 `FilmData` 型（`CaseFilm.tsx` から。これに従う）

```ts
export type Cut = {start:number; dur:number; kind:'img'|'footage'; src:string; treatment:string; seed:string};
export type FilmData = {
  fps:number; narration:string; narrationSeconds:number; hookSeconds:number; hookLine:string;
  hook:{start:number;dur:number;kind:string;src:string;seed:string}[];
  cuts:Cut[]; captions:{start:number;end:number;text:string}[];
  graphics:{start:number;end:number;lines:string[]}[];      // 必須フィールド。EP41 は []
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
- `fps = 30`。`narration = "thompson/narration.mp3"`（本番のみ実在）

## 5.2 カット構成（**§3 マニフェストから機械的に組む・紙芝居回避が最優先**）

```
総カット 214 = factory 88 (footage) + motion 30 (footage) + 静止画 96 (img)

[A] first-use share（check_asset_reuse floor 0.70）
    distinct 88+15+80 = 183 → 183/214 = 0.8551            ✓ >=0.70（spec first_use_share と一致）

[B] per-asset cap（check_asset_reuse）
    factory: 88/88 = 1.00回  ✓ <=1（★factory は再使用禁止）
    motion : 30/15 = 2.00回  ✓ <=2
    still  : 96/80 = 1.20回  ✓ <=2

[C] animation_mix（frame ベース。★still-share <= 0.45 / motion-coverage >= 0.45）
    footage 118カット（factory88+motion30）が motion 側。still 96カットが still 側。
    ★still の平均尺を footage より短くして still-frame-share <= 0.44 に収める:
       still  平均 3.05s → 96×3.05 = 292.8s
       footage平均 3.30s → 118×3.30 = 389.4s
       still-share(frame) = 292.8 / (292.8+389.4) = 0.429           ✓ <=0.45（cut数比 96/214=0.4486 より安全側）
       motion-coverage は footage 389.4s + figures ≈ 0.57+          ✓ >=0.45

[D] 平均ショット長（spec mean_shot 3.19 / max 6.0）
    682.5 / 214 = 3.19 秒/カット                                    ✓ <=6

[E] factory 下限（30秒に1本 = 22.7 → >=23本） 88本                  ✓
```

> **[A] の余裕は薄い。still を1枚減らして cuts を増やすと 0.85 を割る方向に動く。**
> **マニフェストが still 80 / factory 88 / motion 15 を割ったら組まずに止めて A に差し戻す。**

## 5.3 カット割り当てのルール（`build_lech_film.py` の `allocate()`/`tile_window()` を踏襲）

1. 各幕の秒窓を `section_windows()` から取り、幕内に **factory : motion : still を按分**して配置
   （目安の幕別カット数。実配分は narration_index の窓長で自動調整）:

   | section | factory | motion | still | 小計 |
   |---|---|---|---|---|
   | HOOK+OP | 6 | 2 | 8 | 16 |
   | ACT_1 | 16 | 5 | 17 | 38 |
   | ACT_2 | 16 | 8 | 17 | 41 |
   | ACT_3 | 24 | 8 | 26 | 58 |
   | ACT_4 | 12 | 5 | 14 | 31 |
   | ENDING | 14 | 2 | 14 | 30 |
   | **計** | **88** | **30** | **96** | **214** |

2. **factory は各1回のみ**（使用済み集合を持ち二度と引かない）。**motion は各≤2回・still は各≤2回**（`allocate(cap=…)`）
3. **同一素材を連続させない**（`build_lech_film.py` と同じく順序を散らす）
4. 静止画 `treatment` は `["depth","scan","duotone","focus"]` を循環（同じ treatment を3連続させない）
5. **still の `dur` を footage の `dur` より系統的に短く**（§5.2[C]。`tile_window` の重みで still 側を小さめに）
6. motion の `dur` は **3.0–3.4秒**（実素材 3.417s。超えるとループが見える）
7. **AEカードの区間（§7.2）に重なるカットも存在させる**（コンポジタ SKIP 時に穴が空かないため）

## 5.4 `figures[]` と `captions[]`
- `figures[]` は §6（**≥34本**・spec 下限29に余裕）
- `captions[]` は narration_index の全チャンクを **verbatim**（`build_captions()` と同一）。SRT も同時出力

## 5.5 合成レイヤー（`overlay`）— **`cuts[].src` に出さない**
`overlay` 8本は「加工」。`cuts[].src` に入れると `kind_of()` が factory 判定（上限1回）になり FAIL する。
`thompson_film.json` に **`overlays` 独自キー**で持たせる（`CaseFilm` は未知キーを無視）か、専用レイヤーで `screen` 合成する。

## 5.6 ビルダが出力する成果物（**asset_map→manifest変換＋beatsheet生成**）
`build_lech_film.py` と同じく、`main()` は次を書く:

| 出力 | パス |
|---|---|
| film.json | `remotion/src/data/thompson_film.json` |
| public コピー | `remotion/public/thompson/film_data.v001.json` |
| **manifest**（asset_map→provenance変換） | `episodes/PD-2026-041-thompson/05_visuals/asset_manifest.v001.json` … **待った。ここは A の所有（§0.2.1）。B は `04_scenes/thompson_build_manifest.v001.json` に書く**（provenance専用・A のファイルに書かない） |
| **beatsheet**（figures+AE区間の突き合わせ表） | `episodes/PD-2026-041-thompson/04_scenes/thompson_beatsheet.v001.json` |
| SRT（字幕未生成時のフォールバック） | `episodes/PD-2026-041-thompson/08_edit/captions.final.v001.srt`（**§8 の生成器が上書きする**） |

> **★beatsheet の命名に関する重大な注意:** `check_motion_density` / `check_animation_mix` は
> `04_scenes/premium_beatsheet.v*.json` を**自動検出して film.json より優先**する。
> **B の beatsheet は `thompson_beatsheet.v001.json`（`premium_` を付けない）** にして、
> **ゲートの測定源を film.json 一本に保つ**（二重ソースの乖離＝EP39/40 の矛盾28件の原因を避ける）。
> `thompson_beatsheet` は provenance と `validate_thompson_beats`（AE↔Remotion 突き合わせ）専用。

## 5.7 CLI
```bash
$PY scripts/build_thompson_film.py \
  --assets <asset_manifest path> \
  --narr   <narration_index path> \
  --out    remotion/src/data/thompson_film.json \
  [--captions episodes/PD-2026-041-thompson/08_edit/captions.final.v001.srt]
```
**`--assets` の `is_stub` によって処理を変えないこと（§0.2）。** 末尾に `check_asset_reuse` 相当の自己レポートを print する。

---

# 6. Remotion 側 `figures[]`（**≥34本・spec 下限29の余裕込み**）

## 6.1 密度の検算（`check_motion_density`・**AEカードは1本も数えられない**）

```
figures 34本（film.json） / body 11.375分(=682.5/60) = 2.99 /分   ✓ MIN_KINETIC_BEATS_PER_MIN 2.5
coverage: 34本 × 平均5.3s = 180.2s / 682.5 = 26.4%               ✓ MIN_ANIMATED_COVERAGE 0.25
variety : 下記 kind を10種以上使用                               ✓ MIN_ANIMATED_VARIETY 3
spec motion.beats_floor = 29 に対し 34 で余裕。coverage が最も薄いので figures の dur は 4.8–6.0s を基本に。
```

> **★3軸すべて AND。density/coverage/variety のどれか1つでも floor 未満で FAIL。**
> 34本を非重複で置き、平均 dur を 5.3s 程度に確保すること（coverage が floor 0.25 に一番近い）。

## 6.2 ★★★ `FigureSpec` の `kind` は**実在する小文字値のみ** ★★★

> **大文字名（`ActTitle`/`QuoteCard`/`VoteTally`…）は `FigureBeats.tsx` の union に無く、無言で描画が消える。**

**EP41 で使う実在 `kind`（`remotion/src/components/FigureBeats.tsx` の union から。全て共通で `start`/`end` 必須）:**

| `kind` | 必須プロパティ | EP41での用途 |
|---|---|---|
| `numberticker` | `value:number` / `label?` / `prefix?` `suffix?` `decimals?` | 14年・18年・$14M・4検事 |
| `stat` | `value:number` / `label:string` / `prefix?` `suffix?` `decimals?` `topLabel?` | 数の提示（numberticker と使い分け） |
| `votetally` | `majority:number` / `dissent:number` / `label?` | **5対4**（F08。EP41の主役ビート） |
| `timeline` | `events:{year:string;text:string}[]` | 事件年表（1984→1985→1994→1999→2003→2011） |
| `quote` | `quote:string` / `attribution:string` | Ginsburg / Thomas / Brady（**帰属必須**） |
| `kinetic` | `lines:string[]` / `style?:'wordpop'\|'maskslide'\|'emphasis'` / `emphasisWords?` | 決め所テキスト |
| `lowerthird` | `primary:string` / `secondary?` / `accent?` | 場所/時期/**"ILLUSTRATIVE RECONSTRUCTION" 開示** |
| `acttitle` | `title:string` / `kicker?` / `index?` | 幕頭（Remotion 側で密度に数える。§7 の AE 幕頭とは別区間） |
| `compbars` | `items:{label:string;value:number;accent?}[]` | **型B vs 型O** / **$14M vs $0** |
| `mechanism` | `mechanism:'closingdoor'\|'gears'\|'faultsplit'` ★discriminant は `kind`・変種は `mechanism` | 鉄扉(closingdoor)・failure-to-train(faultsplit)・司法の論理(gears) |
| `dochighlight` | `rects:{x,y,w,h}[]` / `mode?:'underline'\|'box'\|'redact'` | 隠された報告書（**redact**＝象徴・読ませない） |
| `regionmap` / `pindropmap` | `label?` / `pins:{x,y,label?}[]` | Orleans Parish / Louisiana |

**`votetally` は `majority:5, dissent:4` 固定**（§2 R-SPLIT）。`quote[].attribution` は §2 の `APPROVED_QUOTES` に一致させる。

## 6.3 figures アンカー設計（`build_lech_film.py` の `FIGURE_ANCHORS` 方式）

**方式:** `(anchor_sec, payload)` の配列を秒昇順に置き、`build_figures()` が
`end = min(anchor+FIG_DUR, next_anchor-FIG_GAP, total-0.5)` でクランプ、`end-start < FIG_MIN_DUR` なら **exit 1**。
`FIG_DUR=5.3 / FIG_MIN_DUR=3.0 / FIG_GAP=0.4`。**アンカー秒は narration_index の section 窓に対する相対で決め、
`section_windows()` を基準にオフセットで置く**（秒直書き禁止。窓が動いても追従する）。

**配置方針（34本・§2 台帳の値だけを焼く・kind を分散して variety を稼ぐ）:**

- HOOK/OP: `kinetic`（"HIDDEN 14 YEARS"）/ `lowerthird`（開示）/ `mechanism:closingdoor`（鉄扉）
- ACT_1: `acttitle`（THE CHOICE）/ `timeline`（1984→1985）/ `compbars`（TYPE B vs TYPE O = F04）/
  `numberticker`（F01=14 隠匿年）/ `kinetic`（"THEY TRIED THE ROBBERY FIRST"）/ `dochighlight:redact`（隠された報告書）
- ACT_2: `acttitle`（THE WAIT）/ `numberticker`（F02=14 死刑囚房）/ `stat`（F03=18 収監）/
  `numberticker`（F05=9 Deegan）/ `timeline`（F06: 4/16設定→5/20予定→4月末発見）/ `kinetic`（"NO ONE DID"）/ `mechanism:closingdoor`
- ACT_3: `acttitle`（THE VERDICT）/ `numberticker`（F07=$14,000,000）/ `votetally`（F08=5対4）/
  `timeline`（F09: 2010口頭弁論→2011-03-29判決）/ `quote`（Thomas "trained lawyers"）/ `quote`（Ginsburg "standard operating procedure"）/
  `stat`（F10=4検事）/ `stat`（F11=4件・**帰属"the majority allowed"を label に**）/ `mechanism:faultsplit`（failure-to-train）/ `compbars`（$14M → $0）
- ACT_4: `acttitle`（THE REACH）/ `kinetic`（"BRADY"）/ `mechanism:gears`（rule の射程）/ `lowerthird`（Brady 定義）/ `dochighlight:box`
- ENDING: `kinetic`（"HIS VOICE"）/ `lowerthird`（F14 は **verified:false → 除外**。年を焼かない）/ `timeline`（無罪2003→死去…F14除外時は 2003 のみ）/ `quote`（締め）/ `kinetic:emphasis`（"ALMOST NEVER"）

> **F14（RAE設立・2017死去）は `verified:false`。** ENDING の該当 figure は `check_thompson_facts` の
> R-LEDGER で落ちるので、**値を焼かず**「行為」で締める（台本の "give them away" / "his voice" を kinetic で）。
> 年が本番台帳で `verified:true` になったら追加する。

## 6.4 配置ルール
1. **AEの区間（§7.2）と1秒でも重ならない**（`validate_thompson_beats` が突き合わせ）
2. **同じ kind を連続させない**（`mechanism` の直後に `mechanism` を置かない）
3. 1枠 **4.8–6.0秒**
4. `quote[].quote` / `kinetic[].lines` / `*.label` は §2 の R-LEDGER・R-ATTRIB・R-FACE/R-DOC 検査対象
5. 台帳外の数値を `value`/`numKeys` に置かない（**焼いたら R-LEDGER で FAIL**）

---

# 7. After Effects カード（`build_thompson_hero_cards.py` / `composite_thompson_hero.py`）

## 7.1 位置づけ
AEカードは **film.json とは別**に ffmpeg で本編に焼き込む（§0.5-2＝密度に数えられない）。
`build_lech_hero_cards.py` を**コピーしてパス・定数・CARDS デッキだけ差し替える**。レイアウト実装・
`money_keys()`・`fit_size()`・完了マーカー・機械の罠対処は**1行も削らない**。

## 7.2 AEカードデッキ（**単調増加・重複ゼロ・台帳裏付けのみ。この表が契約**）

**区間の秒は本番の rendered base（narration_index 由来）に一致させる。** 下表の秒は spec タイムライン基準の**目安**で、
`build_thompson_hero_cards.py` は section 窓からオフセットで算出しクランプする。**背景静止画は象徴オブジェのみ（R1）。**

| id | レイアウト | 内容 | F-ID | 背景 | required |
|---|---|---|---|---|---|
| t01 | ACT_TITLE_CARD | 幕1 THE CHOICE | — | 空の証人席 | 必須 |
| c01 | DATE_STAMP | 1984 殺害 / 1985 訴追 | F12 | 新聞の質感(illegible) | 必須 |
| s01 | SPLIT_COMPARE | 血液型 **TYPE B**（現場）vs **TYPE O**（Thompson） | F04 | 血の付いた布(非グラフィック象徴) | 必須 |
| t02 | ACT_TITLE_CARD | 幕2 THE WAIT | — | 独房の天井 | 必須 |
| n01 | CENTER_STACK | 死刑囚房 **14 YEARS** | F02 | 鉄扉 | 必須 |
| n02 | CENTER_STACK | 収監合計 **18 YEARS** | F03 | 廊下シルエット | 必須 |
| d01 | DATE_STAMP | 処刑「設定」4/16 → 「予定」5/20（**別行で分離・R-DATE**） | F06 | めくれるカレンダー | 必須 |
| t03 | ACT_TITLE_CARD | 幕3 THE VERDICT | — | 最高裁列柱 | 必須 |
| c02 | DATE_STAMP | 再審無罪 **2003** | F13 | 空の陪審席 | 必須 |
| m01 | MONEY_STACK | 陪審の賠償 **$14,000,000** | F07 | 黒背景 | 必須 |
| v01 | VOTE_SPLIT | **5 対 4**（Court reverses） | F08 | 分割された9席(顔なし) | 必須 |
| c03 | DATE_STAMP | 口頭弁論 2010-10 / 判決 **2011-03-29** | F09 | 最高裁ファサード | 必須 |
| q01 | QUOTE_CARD | Ginsburg "standard operating procedure" | — | 夜の廊下 | 必須 |
| z01 | MONEY_STACK | 支払われた額 **$0**（$14M からの落差） | F07 | 机の上の空フォルダ | 必須 |
| t04 | ACT_TITLE_CARD | 幕4 THE REACH | — | 一枚の紙 | 必須 |
| s02 | SEAM_TRANSITION | 幕4→ED の余韻 | — | なし | 必須 |

**検算（Codex は自分で再計算して一致を確認）:** 16区間・単調増加・重複ゼロ・HOOK(0–19.2) と ENDCARD(末尾9s) に重ねない。
Remotion figures(§6) と1秒も重ならない（`validate_thompson_beats` が検査）。

## 7.3 レイアウト（`build_lech_hero_cards.py` の実装を踏襲）
`DATE_STAMP` / `CENTER_STACK` / `MONEY_STACK` / `SPLIT_COMPARE` / `ACT_TITLE_CARD` / `QUOTE_CARD` /
`VOTE_SPLIT` / `SEAM_TRANSITION` を実装。**共通レイヤースタック・色定数・Anton/Oswald・`psName()` の
runtime 解決（allFonts の array-LIKE ラッパーを unwrap）は build_lech_hero_cards.py と同一。**

**EP41 色定数（0..1 float・紺/金トーン）:**
```python
GOLD  = [0.898, 0.710, 0.227]   # #E5B53A アクセント
WHITE = [0.961, 0.969, 0.980]
SILVER= [0.588, 0.627, 0.682]
INK   = [0.043, 0.055, 0.102]   # #0B0E1A 紺の黒（サムネ bg と一致）
BLOOD = [0.62, 0.16, 0.14]      # SPLIT_COMPARE の TYPE B 側にだけ弱く
```

**数値カードは全て `money_keys()` 系で表示文字列を Python 事前計算**（JSX で算術しない＝EP38 確定ルール）。
`VOTE_SPLIT` は「5」を先に、間を置いて「4」を出し、`5-4` の緊張を作る（票の色は多数=SILVER・反対=GOLD）。

## 7.4 `beats.json` スキーマ（本番 `08_edit/ae_hero/beats.json` / dryrun `08_edit/_dryrun/ae_hero/beats.json`）
`build_lech_hero_cards.py` の beats スキーマに準拠。各 beat に `id` / `layout` / `start` / `end` / `dur` /
`still`(象徴 or null) / `hero`(主表示文字列) / `top` / `bottom` / `caption`(**改行禁止・最大50字**) /
`value` / `numKeys` / `blend_mode`(既定 "overlay") / `required` / `out`。
**`value` / `hero` の数値は §2 台帳の `verified:true` 値のみ**（`check_thompson_facts` が照合）。

## 7.5 このマシン固有の罠（`build_lech_hero_cards.py` が対処済み。**1つも省くな**）
1. `setTemporalEaseAtKey` の配列次元は **spatial(Position) で 1**（`if(!prop.isSpatial){...}` で分岐）
2. RS = **`"最良設定"`** / OM = **`"H.264 - レンダリング設定を一致 - 15 Mbps"`**（英語名は try/catch フォールバックのみ）
3. TextDocument の改行は `\n` 不可。**`caption` は1行**（改行が要るなら別レイヤー）
4. `app.newProject()` は headless でハング。**使わず**同名コンプを防御削除
5. ビルドは**カード16枚で 200–300秒**。`render/_build_ok.txt` をポーリング（**タイムアウト最低600秒**）
6. 起動はデタッチ + 出力ポーリング。jsx 末尾で `app.quit()`
7. `comp.motionBlur=true` だけでは無効。**動かすレイヤー個別に `layer.motionBlur=true`**
8. 2Dレイヤー回転は **`"ADBE Rotate Z"`**（`"ADBE Rotation"` は null）
9. `inPoint` と `outPoint` の**両方**を設定
10. 読み込み後 `item.mainSource.conformFrameRate = 30`（忘れると全カードの timing がズレる）
11. 実行パス `C:\Program Files\Adobe\Adobe After Effects 2026\Support Files\AfterFX.exe`（実在確認済み）
12. `proj.gpuAccelType = GpuAccelType.SOFTWARE`（RTX4090 でもソフトレンダ固定・安定優先）
13. **`getFontsByFamilyNameAndStyleName` を使うフォント解決**（allFonts[i] ラッパー経由の unwrap）で無言の代替置換を防ぐ
14. **フォント文字列やラベルを PowerShell 経由の正規表現/エスケープで生成しない**（`\b` がバックスペース化した実害）。Python 側で literal に組む。**Python 先頭に `sys.stdout.reconfigure(encoding="utf-8")`**

## 7.6 実行
```bash
$PY scripts/ae/build_thompson_hero_cards.py [--dryrun]
"C:/Program Files/Adobe/Adobe After Effects 2026/Support Files/AfterFX.exe" -noui \
  -r ".../episodes/PD-2026-041-thompson/08_edit/ae_hero/thompson_hero.jsx"
# render/_build_ok.txt を待つ（最大600秒）→ render/*.mp4 が16本揃うまで待つ（最大1200秒）
$PY scripts/ae/composite_thompson_hero.py [--dryrun]
```

## 7.9 `scripts/validate_thompson_beats.py`（BLOCKING）
1. `beats[].start` 昇順・区間非重複
2. 全 `start`/`end` が本編ナレ区間内（HOOK 0–19.2 と ENDCARD 末尾9s に重ねない）
3. `layout` が §7.3 の8種のいずれか。still が必要なレイアウトで null なら FAIL・ベクター系(SEAM)で非null なら FAIL
4. `still` 非null は実在＋長辺 >=3840px
5. `hero`/`top`/`bottom`/`caption`/`value` が §2（R-LEDGER/R-ATTRIB/R-FACE/R-DOC/R-DATE）を通る
6. `verified:false` の値を要求するカードは `required:false` で**除外**、`required:true` なら exit 1（`--dryrun` は警告続行）
7. **`thompson_film.json` の `figures[]`（§6）と AE の区間が1秒でも重ならない**
8. `caption` に改行が含まれない

## 7.10 コンポジタ（`composite_thompson_hero.py`・`composite_lech_hero.py` を踏襲）
```
BASE = episodes/PD-2026-041-thompson/08_edit/thompson_final_bgm.v002.mp4
OUT  = episodes/PD-2026-041-thompson/08_edit/thompson_final_bgm.v003_ae.mp4
FFMPEG  = C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe
FFPROBE = C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffprobe.exe
W,H,FPS = 1920, 1080, 30
```
**SKIP4条件を1行も削らない:** ① `render/<id>.mp4` 不在 ② 解像度 != 1920x1080 ③ 実測尺 `< dur-0.3` ④ `beat.end > base_dur`。
SKIP された区間は元カットのまま残る（作品は壊れない）。**何枚 SKIP したかを stderr に必ず出す。**
ffmpeg は `overlay=0:0:eof_action=pass:enable='between(t,start,end)'`（`blend_mode` が screen/multiply の時のみ `blend`）。
**出力後 `probe_dur(OUT)` でベースとの尺差 <=0.5秒を確認。出荷済みは絶対に上書きしない（必ず `_v003_ae`）。**
**dryrun のベースは §3.4 のスタブ黒ベース `_dryrun/thompson_final_bgm.v002.mp4`。**

---

# 8. 字幕の切断規則（`scripts/gen_captions_thompson.py`・`gen_captions_lech.py` を踏襲）

## 8.1 原則
**文字数は「上限」であって「分割基準」ではない。** 純機械的な7語/42字分割（旧 `gen_captions_case.py`）が
機能語切れ・孤立キューの原因。`gen_captions_lech.py` の `internal_split()` / `chunk_sentence()` を**そのままコピー**する。
`from fix_caption_dangling import NO_DANGLE_END, wrap as safe_wrap`（**語リストを自前で書き直さない**）。

## 8.2 通すゲート `scripts/check_caption_breaks.py`（**閾値を緩めるの禁止**）
- **A. 行末の機能語**（複数行キューの最終行以外が句読点なしで `NO_DANGLE_END` の語で終わる）= 0件
- **B. 孤立キュー**（語数<3 で「終端句読点で終わる」「大文字で始まる」の両方を満たさない）= 0件
- **C. 句をまたぐ切断(hard)** = 0件
- A/B/C いずれか1件で `bad_share` に関係なく FAIL（**実質ゼロ許容**）

## 8.3 EP41 の入力と対応
- 入力は **narration_index の各チャンク文**（`--narr`）。**字幕テキストは台本本文と1:1対応**（§0.5-5）。
  台詞・別エピソード文の混入禁止。narration_index の `text` を verbatim で使い、構文境界で分割するだけ。
- `ABBR` に `U.S.` / `v.` / `Mr.` 等を持つ（`Connick v. Thompson` の `v.` で文を切らない）。
- タイミングは narration_index の start/end を使う（本番は faster-whisper 語タイム、スタブは §4.4 の合成タイム）。
  CPS <=27・最小表示 0.90秒。**Step で決めた境界を時間都合で動かさない。**

## 8.4 セルフテスト（`--selftest`・EP38 実害を回帰に）
`"...ends with a warning and a ride home."` → `"home."` を単独キューにしない、等の4ケースを実装し、
**出力を `check_caption_breaks.py` に食わせて exit 0 まで自動確認。**

## 8.5 実行
```bash
$PY scripts/gen_captions_thompson.py --narr episodes/PD-2026-041-thompson/06_audio/narration_index.stub.v001.json
$PY scripts/check_caption_breaks.py episodes/PD-2026-041-thompson/08_edit/captions.final.v001.srt
# → PASS が出るまで直す。ゲート側の閾値を緩めるのは禁止。
```

---

# 9. 4ゲートの実際の判定（**build 後に必ず全部通す・animation_mix を忘れるな**）

| ゲート | 実体 | EP41 の通過根拠 |
|---|---|---|
| `check_asset_reuse.py <film.json>` | factory≤1 / motion≤2 / still≤2 / first-use≥0.70 | §5.2: factory1.00 / motion2.00 / still1.20 / first-use **0.855** |
| `check_motion_density.py --ep …` | film.json の graphics+figures+heroCuts のみ / density≥2.5・coverage≥0.25・variety≥3（**AND**） | §6.1: **2.99 / 26.4% / 10+種**（AEカードは0本＝§0.5-2） |
| `check_animation_mix.py --ep …` | film.json の cuts を img=still/その他=footage 分類 / still-share≤0.45・motion-cov≥0.45（frame ベース） | §5.2[C]: still-share **0.429** / motion-cov **0.57+**（footage 118本が効く＝§0.5-1） |
| `check_caption_breaks.py <srt>` | A/B/C 各0件 | §8 の構文境界生成器 |

> **`check_animation_mix` は `04_scenes/premium_beatsheet.v*.json` があればそれを優先する。**
> §5.6 の通り B の beatsheet は `thompson_beatsheet`（`premium_` 無し）なので**auto-detect されず film.json を測る。**
> これで「figures を増やしたのに still-heavy の cuts で落ちる」＝紙芝居を frame ベースで確実に検出できる。

---

# 10. OP バンパー `OpeningThompson`（Remotion・fps60/1920x1080/180f）

## 10.1 二重OPを作らない
本編（`Ep41Thompson`）の OP は `Bookends.tsx` の `BrandOpening` のまま（`op_ed_bookends` ゲート・フォーク禁止）。
`OpeningThompson` は**独立したタイトルバンパー成果物**（`out/thompson_opening.mp4`。Shorts/予告/SNS 用）。
**本編に ffmpeg で焼き込まない。**

## 10.2 Composition 設定
| 項目 | 値 |
|---|---|
| `id` | `OpeningThompson` |
| 解像度 / fps / duration | **1920×1080 / 60 / 180**（=3.0秒） |
| component | `remotion/src/compositions/OpeningThompson.tsx` |

```tsx
import {OpeningThompson, openingThompsonDurationInFrames} from './compositions/OpeningThompson';
import thompsonOpeningProps from '../props/thompson.json';
<Composition id="OpeningThompson" component={OpeningThompson}
  width={1920} height={1080} fps={60}
  durationInFrames={openingThompsonDurationInFrames(60)} defaultProps={thompsonOpeningProps}/>
```

**依存:** `@remotion/motion-blur`（`remotion/package.json` に既存確認済み。未導入時のみ `cd remotion && npm i @remotion/motion-blur`）。
**`remotion/remotion.config.ts`** は既に正典値（png / h264 libx264 / CRF16 / yuv420p / bt709 / aac 320k / 全コア並列 / angle）。
**一致確認のみ・書き換えない。**

## 10.3 秒数ベースのタイムライン（fps=60・フレーム直書き禁止・全て `Math.round(fps*秒)`）

| 秒 | 起きること | 手法 |
|---|---|---|
| 0.00–0.40 | L1 グラデ背景 opacity 0→1・**同時に scale 1.08→1.00（180f・`Easing.out(Easing.cubic)`）** | interpolate（opacity 単独禁止・scale と併用） |
| 0.10 | ロゴ（`hasLogo`）左上に spring・scale 0.4→1.0・opacity 0→1 | spring `damping:14,mass:0.9` |
| 0.15–0.25 | L2 グリッド reveal（opacity→0.18）＋ 180f で translateY 0→48px | spring `damping:200,mass:1,duration:round(fps*0.8)` + `Easing.inOut(Easing.sin)` |
| 0.25 | L3 グロー scale 0.6→1.15 / opacity 0→0.85 | spring `damping:18,mass:1.2`（併用） |
| 0.30–0.86 | L4 主役タイトルが1文字ずつ切れ上がり（translateY 110%→0）＋ opacity `interpolate(spring,[0,0.25],[0,1])`。スタッガー **2f/文字**。全体を `Trail(layers=6,lagInFrames=1.2,trailOpacity=0.45)` で包む | spring `damping:16,mass:1` |
| 0.55–1.15 | L2b **鉄扉スリット**（中央から縦の細い光線 `scaleX 0→1`＋opacity 0→0.5・破壊ではなく「閉じる扉」のモチーフ） | spring `damping:22,mass:1.1`・`transformOrigin:'center'`・**motionBlur** |
| 0.95–1.35 | L5a アクセント下線 左から `scaleX 0→1` | spring `damping:16,mass:0.8`・`transformOrigin:'left center'` |
| 1.10–1.55 | L5b サブタイトル translateY 24→0 + opacity 0→1 | spring `damping:20,mass:1`（併用） |
| 1.55–3.00 | settle→ホールド。背景 scale 1.00・グリッド 48px に着地。**完全静止フレーム無し・フェードアウトしない** | — |

> **等速線形を1箇所も使わない。opacity 単独の演出を1箇所も作らない**（全 opacity が translateY/scale/scaleX と対）。

## 10.4 props 型と値
```ts
export type OpeningThompsonProps = { title:string; subtitle:string; accent:string; hasLogo:boolean };
```
`remotion/props/thompson.json`: `{ "title":"THOMPSON", "subtitle":"CONNICK v. THOMPSON", "accent":"#E5B53A", "hasLogo":true }`
`remotion/props/thompson_short.json`: `{ "title":"5–4", "subtitle":"THEY HID THE PROOF", "accent":"#E5B53A", "hasLogo":false }`
> `subtitle` も §2 の R-FACE/R-DOC 検査対象（`remotion/props/thompson*.json`）。ルート背景は紺の黒 `#0B0E1A`。

## 10.5 量産
```bash
cd remotion && npm run studio     # OpeningThompson を 0→180f スクラブして §10.3 の各時刻を目視
npx remotion render OpeningThompson out/thompson_opening.mp4 --props=./props/thompson.json
npx remotion render OpeningThompson out/thompson_short_op.mp4 --props=./props/thompson_short.json
```

---

# 11. サムネ3案（`ThompsonThumbnails.tsx`・`<Still>` 1280×720・Root に `Thumb-thompson-01..03`）

**共通要件:** 見出し全て大文字・4語以内・320pxで判読 / **実在人物の肖像禁止（R1）** / 黒・紺bg + gold `#E5B53A` /
背景は `stills[role="thumb"]`（象徴オブジェのみ） / `thumbnail_visibility`（luma平均≥33＋コントラスト）を通す。目標CTR 6%+。

- **T1「隠された1枚」（最推奨）:** 古いファイルから引き抜かれた1枚の紙（顔なし・書類 illegible）。文字 **`BURIED FOR 14 YEARS`**（3語）。`14 YEARS` を金。
- **T2「5-4」（数字勝負）:** 最高裁列柱を暗く落とし、前面に **`5–4`**（大）＋ **`NO PAYMENT`**（下）。`NO PAYMENT` を金。数字は F08/F07 の検証済み値のみ。
- **T3「鉄扉」（尊厳）:** 独房の鉄扉のシルエットに一条の光。文字 **`THE PROOF THEY HID`**（3語）。`HID` を金。

**A/Bタイトル候補（`09_package`・60字以内・二人称）:** 台本のとおり
- **A:** `Can You Sue a Prosecutor Who Hid the Proof of Your Innocence?`
- **B:** `They Hid the Proof He Was Innocent. Then the Court Said: Tough.`

**固定コメント** `09_package/pinned_comment.v001.txt`（§2 の R-LEDGER/R-ATTRIB 検査対象。台帳事実のみ）:
```
Two things this case turns on:
(1) A crime-lab report showed the blood at the scene was type B. John Thompson is type O.
    It sat in a file for fourteen years.
(2) The Supreme Court reversed his 14-million-dollar award, five to four (2011).
    The majority said one hidden report is not a proven pattern of failure-to-train.

If it were you in that cell — who should answer for the buried page?
```

---

# 12. 本編コンポジション登録（`remotion/src/Root.tsx`・`Ep38KidsForCash` の形を踏襲）
```tsx
import thompsonFilm from './data/thompson_film.json';
<Composition id="Ep41Thompson" component={CaseFilm}
  durationInFrames={caseFilmDurationInFrames(thompsonFilm as unknown as FilmData, BRAND.video.fps)}
  fps={BRAND.video.fps} width={BRAND.video.width} height={BRAND.video.height}
  defaultProps={{ data: thompsonFilm as unknown as FilmData, seriesLabel: 'PRIME DOCUMENTARY',
    title: 'They Hid the Proof He Was Innocent',
    subtitle: 'Fourteen years on death row. Then the Court said: no.' }}/>
```
> `remotion/src` に現在 `thompson` の文字列が無いこと（衝突しない）を確認してから追記。`subtitle` も §2 検査対象。

---

# 13. 受入（自分で exit 0 を確認してから完了報告）
```bash
cd C:\Users\aab15\Documents\prime-documentary ; PY=./.venv/Scripts/python.exe

# 0. 語数（最優先・課金前に落とす）
$PY scripts/check_script_length.py episodes/_planning/EP41_thompson_script.en.v001.md --json   # 2,026語 / wpm178.1

# 1. 事実性/R1（EP41固有）
$PY scripts/check_thompson_facts.py --json

# 2. 契約バリデータ
$PY scripts/validate_thompson_beats.py
$PY scripts/check_thompson_asset_manifest.py --assets episodes/PD-2026-041-thompson/05_visuals/asset_manifest.v001.json

# 3. ★4ゲート（animation_mix を忘れるな）
$PY scripts/check_asset_reuse.py    remotion/src/data/thompson_film.json
$PY scripts/check_motion_density.py --ep PD-2026-041-thompson
$PY scripts/check_animation_mix.py  --ep PD-2026-041-thompson
$PY scripts/check_caption_breaks.py episodes/PD-2026-041-thompson/08_edit/captions.final.v001.srt

# 4. 水増し・レンダ前プリフライト
$PY scripts/check_padding.py --ep PD-2026-041-thompson --json
$PY scripts/preflight_render_gate.py --ep PD-2026-041-thompson

# 5. 本編最終受入（episode番号は★位置引数・--ep ではない）
$PY scripts/check_final_acceptance.py 41 \
  --render episodes/PD-2026-041-thompson/08_edit/thompson_final_bgm.v003_ae.mp4 --emit-receipt
```

| ゲート | EP41 目標値 |
|---|---|
| `check_script_length` | 総語数 **2,026** / `wpm 178.1` / narration **682.5s** |
| `check_asset_reuse` | factory≤1 / motion≤2 / still≤2 / first-use **0.855**（floor0.70） |
| `check_motion_density` | density **2.99**/min / coverage **26.4%** / variety 10+（floors 2.5 / 0.25 / 3） |
| `check_animation_mix` | still-share **0.429**（cap0.45）/ motion-cov **0.57+**（floor0.45） |
| `check_caption_breaks` | 行末機能語0 / 孤立キュー0 / hard split 0 |
| `check_thompson_facts` | violations = 0（台帳照合・5-4・帰属・R1） |
| runtime band | 11.5–12.5分（narration 682.5s + bookends） |
| factory クリップ | ≥23本 → **88本** |
| image_resolution | 全静止画 長辺 ≥3840px |
| thumbnail | 3案 @1280×720 + selected luma≥33 |
| op_ed_bookends | `BrandOpening`/`BrandEndcard` を import（フォーク禁止） |

**全て exit 0 でなければ `package_ready` にしない。自己申告QCは無効。QC基準を書き換えて通すのは禁止。**

---

# 14. 絶対にやらないこと
- **EP39 / EP40 のファイル・素材に触らない**（読み取りのみ可）。レーンを分離する。
- **スレッドAの所有ファイル（§0.2.1）に書かない**（`05_visuals/` `05_stock/` `remotion/public/thompson/` `H:\...\ai\thompson\`）。
  **B の build provenance は `04_scenes/thompson_build_manifest.v001.json` に書く**（A の `asset_manifest` を上書きしない）。
- **設計書 / `EP41_thompson_CODEX_A_*` / PD-2026-039 / PD-2026-040 に触らない。**
- **課金ジョブを起動しない**（ElevenLabs TTS / 課金画像生成API / YouTube アップロード）。narration_index はスタブで着手。
- **公開済み・出荷済み mp4 を上書き・再レンダしない**（出力は必ず `_v003_ae`）。
- **台帳（§2）に無い数値を焼かない**（EP40 の $580,000・捏造間取りの再発防止）。不明値は `verified:false` でカード除外。
- **`FigureSpec` の `kind` を推測で書かない**（§6.2 の実在小文字値のみ。大文字名は無言で消える）。
- **スタブと本番でコードパスを分岐させない**（§0.2）。
- **スペック数値（214 cuts / still80 / factory88 / motion15 / figures≥29 / 682.5s / 2,026語 / 46シーン）を変えない。**
- **実在しないスクリプト名を書かない**（新規は §0.3 の一覧のみ）。**PowerShell 経由で正規表現/エスケープを生成しない**（`\b` バックスペース化の実害）。
