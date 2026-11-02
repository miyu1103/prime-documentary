# EP40 lech — Codex スレッドB「実装」引き継ぎプロンプト v001

> **このファイルは単体で完結している。他のファイルを読まなくても着手できる。**
> 並行して走っているスレッドA（素材生成）のファイル `EP40_lech_CODEX_A_ASSETS.v001.md` は**読まなくてよい**。
> 設計書 `EP40_lech_DESIGN_and_CODEX_PROMPTS.v001.md` も**読まなくてよい**（必要な数値はすべて本書に転記済み）。

```
あなたは Prime Documentary（YouTubeドキュメンタリーチャンネル）の制作エンジニアです。
リポジトリ: C:\Users\aab15\Documents\prime-documentary
Python:     C:\Users\aab15\Documents\prime-documentary\.venv\Scripts\python.exe
メディア:   H:\pd-media
担当:       EP40 / Episode ID: PD-2026-040-lech / slug: lech
```

**題材:** Lech v. Jackson, 791 F. App'x 711 (10th Cir. 2019), cert. denied (2020)。
万引き犯が無関係の一家の家に立てこもり、警察が装甲車と爆薬でその家を全壊させたが、
Takings Clause の「police power」例外により、一家はほぼ何の補償も受けられなかった事件。

---

# 0. このスレッドの責務・境界・完了条件

## 0.1 このスレッド（B）の責務

**コード律速。素材を1点も待たずに、いま全部書ける。**

| # | 作業 | 成果物 |
|---|---|---|
| B-1 | エピソードディレクトリと `manifest.json` | `episodes/PD-2026-040-lech/**` |
| B-2 | 台本スロット契約とバリデータ・スタブ | `scripts/{validate,make}_lech_slots*.py` |
| B-3 | accuracy_lock ゲート（**EP40固有・BLOCKING**） | `scripts/check_lech_accuracy.py` |
| B-4 | 境界契約マニフェストの**消費側**バリデータ＋スタブ素材生成 | `scripts/check_lech_asset_manifest.py` / `scripts/make_lech_stub_assets.py` |
| B-5 | `lech_film.json` ビルダ（226カット・17 figures） | `scripts/build_lech_film_data.py` |
| B-6 | Remotion 本編コンポジション登録 | `remotion/src/Root.tsx` に `Ep40Lech` |
| B-7 | **After Effects カード23枚**のビルダとコンポジタ | `scripts/ae/build_lech_hero_jsx.py` / `composite_lech_hero.py` |
| B-8 | beats バリデータ（AEとRemotionの区間衝突検査） | `scripts/validate_lech_beats.py` |
| B-9 | **構文境界で切る字幕生成器**（文字数分割の置き換え） | `scripts/gen_captions_lech.py` |
| B-10 | OP バンパー `OpeningLech` | `remotion/src/compositions/OpeningLech.tsx` |
| B-11 | サムネ3案 | `remotion/src/compositions/LechThumbnails.tsx` |
| B-12 | **スタブでの通しドライラン** | `episodes/PD-2026-040-lech/08_edit/_dryrun/**` |

## 0.2 もう一方のスレッド（A）との境界

**接続点はただ1ファイル。**

```
episodes/PD-2026-040-lech/05_visuals/asset_manifest.v001.json
   ↑ Aが生成（唯一の生産者）        ↓ Bが消費（唯一の消費者）
```

**Bはこのファイル以外のAの中間生成物を読まない。**
そして **Bはこのファイルが無くても完走できる。** `make_lech_stub_assets.py` が
**まったく同じスキーマの** `asset_manifest.stub.v001.json` を作るので、Bはそれで全パイプラインを通す。

> **★絶対条件: スタブと本番でコードパスを分岐させてはならない。**
> `build_lech_film_data.py --assets <path>` は渡されたマニフェストを読むだけで、
> `is_stub` の値によって**処理を変えない**。分岐したらドライランの意味が消える。
> （`is_stub` はログ出力と受入判定にのみ使う。カットの組み立てロジックには一切使わない。）

### 0.2.1 ファイル所有権（**これを破ると並行作業が壊れる**）

| パス | 所有 | Bの権限 |
|---|---|---|
| `episodes/PD-2026-040-lech/manifest.json` | **B** | 読み書き |
| `episodes/PD-2026-040-lech/{00_topic,01_research,03_script,04_scenes,06_audio,08_edit,09_package,approvals,events}/**` | **B** | 読み書き |
| `remotion/src/**` `remotion/props/**` | **B** | 読み書き |
| `remotion/public/lech_dryrun/**` | **B** | 読み書き（スタブ素材の staging 先） |
| `scripts/ae/**`（新規の lech 用） | **B** | 新規作成 |
| `scripts/*lech*.py`（§0.3 のBスクリプト） | **B** | 新規作成 |
| **`episodes/PD-2026-040-lech/05_visuals/**`** | **A** | **読み取りのみ。書くな** |
| **`episodes/PD-2026-040-lech/05_stock/**`** | **A** | **読み取りのみ。書くな** |
| **`H:\pd-media\assets\ai\lech\**` / `ai_video\lech\**`** | **A** | **読み取りのみ。書くな** |
| **`remotion/public/lech/{img,factory,motion,overlay}/**`** | **A** | **読み取りのみ。書くな** |
| `episodes/PD-2026-039-*/**` / EP39 の素材 | **EP39の別エージェント** | **絶対に触るな。読み取りのみ可** |

> **B は `remotion/public/lech/` に書かない。** スタブは **`remotion/public/lech_dryrun/`** に置く。
> 本番マニフェストが来たら `--assets` を差し替えるだけで `lech/` を参照するようになる。

## 0.3 B が新規作成するスクリプト（これ以外を新規に作らない）

| パス | 役割 |
|---|---|
| `scripts/check_lech_accuracy.py` | §2 の R1–R5（BLOCKING） |
| `scripts/make_lech_slots_stub.py` | §4.4 の台本スロット stub |
| `scripts/validate_lech_slots.py` | §4.3 の契約バリデータ |
| `scripts/check_lech_asset_manifest.py` | §3.3 の消費側バリデータ |
| `scripts/make_lech_stub_assets.py` | §3.4 のスタブ素材生成 |
| `scripts/build_lech_film_data.py` | §5 の `lech_film.json` ビルダ |
| `scripts/validate_lech_beats.py` | §7.9 の不変条件 |
| `scripts/gen_captions_lech.py` | §8 の構文境界字幕生成器 |
| `scripts/ae/build_lech_hero_jsx.py` | §7 のAEカード23枚ビルダ |
| `scripts/ae/composite_lech_hero.py` | §7.10 のコンポジタ |

**既存スクリプトを改変しない。** 特に `scripts/gen_captions_case.py` は他エピソードが使っているので**触らず**、
EP40用に `gen_captions_lech.py` を新規に作る。

## 0.4 完了条件（このスレッドが「終わり」になる条件）

台本が未確定でも、**以下がすべて緑になったら「実装完了」として報告してよい。**

```bash
cd C:\Users\aab15\Documents\prime-documentary

# [B-DONE-1] スタブ素材＋スタブスロットが揃う
./.venv/Scripts/python.exe scripts/make_lech_stub_assets.py
./.venv/Scripts/python.exe scripts/make_lech_slots_stub.py

# [B-DONE-2] マニフェスト消費側バリデータ（スタブ相手に通ること）
./.venv/Scripts/python.exe scripts/check_lech_asset_manifest.py \
  --assets episodes/PD-2026-040-lech/05_visuals/asset_manifest.stub.v001.json

# [B-DONE-3] accuracy_lock（スタブの文字列にも適用される）
./.venv/Scripts/python.exe scripts/check_lech_accuracy.py --json

# [B-DONE-4] film.json をスタブから組み立てる
./.venv/Scripts/python.exe scripts/build_lech_film_data.py \
  --assets episodes/PD-2026-040-lech/05_visuals/asset_manifest.stub.v001.json \
  --slots  episodes/PD-2026-040-lech/03_script/lech_slots.stub.v001.json \
  --out    remotion/src/data/lech_film.json

# [B-DONE-5] 素材反復ゲート（★これがスタブ段階で緑になることが最重要）
./.venv/Scripts/python.exe scripts/check_asset_reuse.py remotion/src/data/lech_film.json
#   → PASS: distinct 171 / 226 cuts, first-use 76%

# [B-DONE-6] beats 契約（AE 23区間 と Remotion 17区間 が1秒も重ならない）
./.venv/Scripts/python.exe scripts/validate_lech_beats.py

# [B-DONE-7] AE 23カードをビルド＋レンダ＋コンポジット（ドライラン出力へ）
./.venv/Scripts/python.exe scripts/ae/build_lech_hero_jsx.py --dryrun
"C:/Program Files/Adobe/Adobe After Effects 2026/Support Files/AfterFX.exe" -noui \
  -r "C:/Users/aab15/Documents/prime-documentary/episodes/PD-2026-040-lech/08_edit/_dryrun/ae_hero/lech_hero.jsx"
./.venv/Scripts/python.exe scripts/ae/composite_lech_hero.py --dryrun

# [B-DONE-8] Remotion Studio で目視
cd remotion && npm run studio
#   → Ep40Lech / OpeningLech / Thumb-lech-01..03 が出て、実際に動くこと
```

**台本確定後に追加で緑にするもの**（§4.5）:

```bash
./.venv/Scripts/python.exe scripts/check_script_length.py \
  episodes/PD-2026-040-lech/03_script/script.en.v003.md --json
./.venv/Scripts/python.exe scripts/validate_lech_slots.py
./.venv/Scripts/python.exe scripts/check_padding.py --ep PD-2026-040-lech --json
./.venv/Scripts/python.exe scripts/check_caption_breaks.py \
  episodes/PD-2026-040-lech/08_edit/captions.final.v001.srt
./.venv/Scripts/python.exe scripts/preflight_render_gate.py --ep PD-2026-040-lech
```

---

# 1. 実装前に必ず読むファイル（**推測で書くな**）

| パス | なぜ読むか |
|---|---|
| `scripts/ae/build_kfc_hero_jsx.py` | **AEビルダの唯一の実証実装。** レイヤースタック・`ease()`・`count_keys()`・`psName()`・レンダキュー登録をそのまま踏襲する |
| `scripts/ae/composite_kfc_hero.py` | **コンポジタの唯一の実証実装。** SKIP 4条件とffmpegフィルタグラフをそのまま踏襲する |
| `remotion/src/compositions/CaseFilm.tsx` | `FilmData` 型と `caseFilmDurationInFrames` |
| `remotion/src/components/FigureBeats.tsx` | `FigureSpec` の**実在する `kind` 文字列**（§6.2 の警告を必ず読め） |
| `remotion/src/components/Bookends.tsx` | `OPENING_SEC = 3.5` / `ENDCARD_SEC = 9` / `BrandOpening` / `BrandEndcard` |
| `remotion/src/data/kidsforcash_film.json` | 実際の film.json の形（cuts / captions / figures の実例） |
| `C:\Users\aab15\Documents\pino-channel\remotion\src\Opening.tsx` | §9 の OP 正典実装 |
| `scripts/check_asset_reuse.py` | §3.5 のパス判定ロジック |
| `scripts/check_caption_breaks.py` / `scripts/fix_caption_dangling.py` | §8 の `NO_DANGLE_END` の実体 |

---

# 2. ★★★ 最優先の絶対条件 — accuracy_lock ★★★

> **この節に違反した成果物は、他が全て完璧でも出荷不可。**

## 2.1 事実

**Lech v. Jackson は最高裁判決ではない。**

| 項目 | 正しい記述 | 禁止される記述 |
|---|---|---|
| 判断した裁判所 | 米国**第10巡回区控訴裁判所**（United States Court of Appeals for the Tenth Circuit） | 「最高裁が」「the Supreme Court ruled / decided / held / upheld / affirmed」 |
| 年 | **2019年**（控訴審判断） | 2020年を「判決の年」として書く |
| 最高裁の関与 | **2020年に上告を受理しなかった（cert. denied）だけ**。中身の判断はしていない | 「最高裁が支持した」「最高裁も同じ結論」 |
| 引用形式 | `Lech v. Jackson, 791 F. App'x 711 (10th Cir. 2019)`（**F. App'x = 未公刊**） | `U.S.` レポーター / `S. Ct.` を付す |

**cert. denied の正しい説明（ナレーションでもこの意味を保て）:**

> "The Supreme Court declined to hear the case. That is not an endorsement — it simply means the Tenth Circuit's decision stands."

**波及範囲:** タイトル・サムネ文字・フックナレ・本編ナレ・**AEカードのラベル**・字幕・
YouTube概要欄・Shorts・OPのサブタイトル・固定コメント — **すべて。**

## 2.2 `scripts/check_lech_accuracy.py`（**Bが実装する・BLOCKING**）

**検査対象ファイル（この一覧をハードコードする）:**

```
episodes/PD-2026-040-lech/03_script/lech_slots.v*.json      （全文字列フィールド）
episodes/PD-2026-040-lech/03_script/lech_slots.stub.v*.json
episodes/PD-2026-040-lech/03_script/script.en.v*.md
episodes/PD-2026-040-lech/08_edit/ae_hero/beats.json        （top / bottom / caption / footnote）
episodes/PD-2026-040-lech/08_edit/_dryrun/ae_hero/beats.json
episodes/PD-2026-040-lech/09_package/*.json                 （title / description / thumbnail headlines）
episodes/PD-2026-040-lech/09_package/*.txt                  （固定コメント）
episodes/PD-2026-040-lech/05_visuals/asset_manifest*.json   （tags / caption_hint / qc.notes）
remotion/src/data/lech_film.json                            （captions[].text / figures[] の全文字列）
remotion/props/lech*.json                                   （title / subtitle）
```

**ルールR1（ゾーン全面禁止）** — 次のフィールドに `supreme court` / `最高裁` / `SCOTUS` が
**部分一致でも1回でも**出たら FAIL:

`title_candidates[]`, `thumb_headlines[]`, `hook.lines[]`, `beats[].top`, `beats[].bottom`,
`ed.cta_line`, `package.title`, `figures[].title`, `figures[].primary`, `figures[].label`,
`props.subtitle`

```python
BANNED_ZONE = re.compile(r"supreme\s*court|最高裁|SCOTUS", re.IGNORECASE)
```

**ルールR2（本文の文脈限定）** — 本編ナレ本文で `Supreme Court` を含む**文**は、
同一文内に次のいずれかを含まねばならない。含まなければ FAIL:

```python
ALLOWED_CONTEXT = re.compile(
    r"declined to hear|refused to hear|denied review|did not take the case|"
    r"cert(iorari)?\s+(was\s+)?denied|let the ruling stand|never ruled on",
    re.IGNORECASE)
```

**ルールR3（肯定的動詞の禁止）** — 本文全体で、`Supreme Court` の後 **60文字以内**に次が現れたら FAIL:

```python
BANNED_VERB = re.compile(r"\b(ruled|held|decided|upheld|affirmed|found|concluded)\b", re.IGNORECASE)
```

**ルールR4（引用形式）** — `script.en.v*.md` に判例引用が現れる場合、正規表現
`Lech v\. Jackson, 791 F\. App'x 711 \(10th Cir\. 2019\)` に完全一致する行が**最低1つ**存在すること。

**ルールR5（裁判所名の明示）** — 本編ナレ本文に `Tenth Circuit` が**最低2回**出現すること
（1回目は幕3の導入、2回目は結論部）。

**出力:** `episodes/PD-2026-040-lech/09_package/accuracy_lock.v001.json`（`{"pass": bool, "violations": [...]}`）。
**このJSONが `pass: true` でない限り、`check_final_acceptance.py` の実行に進んではならない。**

**CLI:** `--json` / `--dryrun`（`_dryrun/` 配下も検査対象に含める）。exit 0 = PASS / 1 = FAIL。

**台本未確定時の挙動:** 対象ファイルが存在しなければ**そのファイルをスキップ**し、
存在するものだけ検査して exit 0 を返す（`skipped` に列挙する）。
**「ファイルが無いから通した」ことを黙るな。必ずログに出す。**

## 2.3 唯一の許容表現（AEカード b08 で使う）

```
footnote = "THE SUPREME COURT DECLINED TO HEAR IT"
```

- これは `beats[].top` / `beats[].bottom` **ではなく専用フィールド `footnote`** に置く（R1のゾーン外）
- `DECLINED TO HEAR` を含むので R2 の文脈規則を通る
- **`footnote` フィールドを beats スキーマに追加すること**（`"footnote": "string|null"`、最大44文字）

---

# 3. ★境界契約: `asset_manifest.v001.json`（Aから受け取る唯一のファイル）

## 3.1 スキーマ（**Aが生成する。Bはこの形を前提に読む**）

**スキーマ版:** `lech_assets.v1`（固定文字列。異なれば **exit 2**）

```jsonc
{
  "schema_version": "lech_assets.v1",
  "episode_id": "PD-2026-040-lech",
  "slug": "lech",
  "generated_at": "2026-07-19T21:00:00+09:00",
  "producer": "scripts/build_lech_asset_manifest.py",
  "is_stub": false,                            // ★ログと受入判定にだけ使う。処理を分岐させない

  "counts": {
    "still_body": 70, "still_ae": 15, "still_i2v_source": 16, "still_thumb": 9,
    "motion": 16, "factory": 85, "overlay": 12
  },

  "stills": [
    { "asset_id": "LECH-S01-01", "scene_id": "S01", "variation": 1,
      "role": "body",                          // "body" | "ae" | "i2v_source" | "thumb" | "reject"
      "act": 1,                                // 0=HOOK / 1..4=幕 / 5=ED / 9=サムネ専用
      "path": "H:/pd-media/assets/ai/lech/S01_01.png",
      "depth_path": "H:/pd-media/assets/ai/lech/S01_01_depth.png",
      "public_path": "lech/img/S01_01.png",    // ★Bが cuts[].src に入れる値
      "width": 3840, "height": 2160,
      "sha256": "...", "mean_luma": 137.2, "phash": "...",
      "tags": ["exterior", "daylight"], "caption_hint": "the house before",
      "prompt_sha256": "...", "seed": 40001001,
      "model": "juggernautXL_ragnarokBy.safetensors",
      "source": "ai_codex", "commercial_use": "allowed", "ai_disclosure_required": true,
      "qc": {"reviewed": true, "on_theme": true,
             "has_readable_text": false, "has_identifiable_face": false, "notes": ""} }
  ],

  "motion": [
    { "asset_id": "LECH-M01", "source_scene_id": "S33",
      "source_still": "H:/pd-media/assets/ai/lech/S33_02.png",
      "path": "H:/pd-media/assets/ai_video/lech/M01_rife.mp4",
      "public_path": "lech/motion/M01_rife.mp4",     // ★必ず .mp4 かつ "_rife" を含む
      "act": 3, "width": 1280, "height": 720,
      "fps": 48, "frames": 164, "duration_sec": 3.417,
      "sha256": "...", "tags": ["dust", "collapse"],
      "qc": {"reviewed": true, "on_theme": true, "artifact_free": true, "notes": ""} }
  ],

  "factory": [
    { "asset_id": "AF-BG-0460",
      "path": "H:/pd-media/assets/factory/backgrounds/AF-BG-0460__office_interior_dark.mp4",
      "public_path": "lech/factory/AF-BG-0460__office_interior_dark.mp4",  // ★必ず "/factory/" を含む
      "type": "backgrounds", "subtype": "office_interior_dark", "kind": "video",
      "license": "Pexels License", "sha256": "...", "act": 2,
      "covers_scene_id": "S53",                 // 特定シーンを代替する本だけ設定。繋ぎは null
      "duration_sec": 8.24, "width": 1920, "height": 1080, "mean_luma": 61.2,
      "eyeballed_content": "an empty municipal lobby, wide static shot, no people",
      "qc": {"reviewed": true, "on_theme": true, "no_watermark": true,
             "no_recognizable_person": true, "no_cartoon": true,
             "label_matches_content": true, "notes": ""} }
  ],

  "overlay": [
    { "asset_id": "AF-PART-0031",
      "path": "H:/pd-media/assets/factory/particle_assets/AF-PART-0031__dust_particles_floating.mp4",
      "public_path": "lech/overlay/AF-PART-0031__dust_particles_floating.mp4",
      "type": "particle_assets", "subtype": "dust_particles_floating",
      "license": "Pexels License", "sha256": "...",
      "blend_hint": "screen",                   // "screen" | "add" | "overlay"
      "eyeballed_content": "slow drifting dust motes on black, loops cleanly",
      "qc": {"reviewed": true, "on_theme": true, "no_watermark": true, "notes": ""} }
  ]
}
```

## 3.2 Bがこのマニフェストから作るもの

| マニフェストの項目 | Bでの使い道 |
|---|---|
| `stills[role="body"]` 70枚 | `lech_film.json` の **静止画カット125本**（`kind:"img"`, `treatment:"depth"`） |
| `stills[role="ae"]` 15枚 | **AEカードの背景**（`beats[].still`）。**本編カットには使わない** |
| `stills[role="thumb"]` 9枚 | サムネ3案（§10） |
| `stills[role="i2v_source"]` 16枚 | **使わない**（Aが動画化済み。静止画としても出さない） |
| `motion` 16本 | `lech_film.json` の **i2vカット16本**（`kind:"footage"`） |
| `factory` 85本 | `lech_film.json` の **実写カット85本**（`kind:"footage"`） |
| `overlay` 12本 | **`cuts[].src` に出さない。** §5.5 の合成レイヤーとして扱う |

## 3.3 `scripts/check_lech_asset_manifest.py`（消費側バリデータ・BLOCKING）

```bash
./.venv/Scripts/python.exe scripts/check_lech_asset_manifest.py --assets <path> [--json]
```

検査項目（1つでも違反したら exit 1。`schema_version` 違いだけ exit 2）:

1. `schema_version == "lech_assets.v1"` / `episode_id == "PD-2026-040-lech"` / `slug == "lech"`
2. `counts.*` が各配列の実長と一致し、**下限**を満たす:
   `still_body>=70` / `still_ae>=15` / `still_i2v_source>=16` / `still_thumb>=9` / `motion>=16` / `factory>=85` / `overlay>=12`
3. `role in ("body","ae")` の全静止画で `public_path` が非null、かつ
   `remotion/public/<public_path>` と `remotion/public/<stem>_depth.png` が**両方実在**
   （`CaseFilm.tsx` の `depthSrcOf()` は `src.replace(/\.[^.]+$/, '_depth.png')`。**depthが無いとレンダーがクラッシュする**）
4. `role != "thumb"` の全静止画で `max(width,height) >= 3840`（`preflight_render_gate.MIN_LONG_EDGE_PX = 3840`）
5. `motion[].public_path` が `.mp4` で終わり、かつ `_rife` を含む（§3.5）
6. `factory[].public_path` が `/factory/` を含む（§3.5）
7. `overlay[].public_path` が `/overlay/` を含み、`/factory/` を**含まない**
8. `sha256` が全配列を通して一意
9. `factory[].eyeballed_content` が空文字でない、かつ `qc.label_matches_content == true`
10. `qc.has_readable_text` / `qc.has_identifiable_face` が true の項目は `role == "reject"`
11. **全文字列値**が §2.2 の `BANNED_ZONE` に一致しない

## 3.4 `scripts/make_lech_stub_assets.py`（**Aを待たずに完走するための鍵**）

**やること:**

1. `remotion/public/lech_dryrun/{img,factory,motion,overlay}/` を作る
2. **静止画スタブ**: PIL で **3840×2160** の単色PNGを生成（`role` ごとに色相を変え、
   中央に `scene_id` と `role` を大書きして目視で識別できるようにする）＋ 同名の `_depth.png`
   （中心から外側へのグラデーション。DPTの出力形式と同じ **`L` モード**）
   - `body` 70枚 / `ae` 15枚 / `thumb` 9枚 / `i2v_source` 16枚 = **110枚 + depth 101枚**
3. **動画スタブ**: ffmpeg の `color` フィルタで
   - factory 85本: `1920x1080 @30fps`、**4.0秒**、ファイル名は `AF-STUB-<NNNN>__stub_clip.mp4`
   - motion 16本: `1280x720 @48fps`、**3.417秒**、ファイル名は `M<NN>_rife.mp4`
   - overlay 12本: `1920x1080 @30fps`、2.0秒
4. `episodes/PD-2026-040-lech/05_visuals/asset_manifest.stub.v001.json` を **§3.1 と完全に同じスキーマ**で書く
   （`is_stub: true`、`public_path` の先頭を `lech_dryrun/` にする）

**★スタブのパスに関する致命的な罠（これを外すと `check_asset_reuse` が素材を誤分類して緑になってしまう）:**

`check_asset_reuse.kind_of()` は**パス文字列だけ**で種別を判定する:

```python
p = path.lower().replace("\\", "/")
if "/factory" in p or re.search(r"\baf-bg-", p):   return "factory"   # 上限1回
if p.endswith((".mp4",".mov",".webm")) or "ai_video" in p or "_rife" in p:  return "motion"  # 上限2回
return "still"                                                                # 上限2回
```

したがってスタブでも:

| 種別 | `public_path` の形 | 満たす条件 |
|---|---|---|
| 静止画 | `lech_dryrun/img/S01_01.png` | `/factory` を含まない・`.png` |
| factory | `lech_dryrun/**factory**/AF-STUB-0001__stub_clip.mp4` | **`/factory/` を含む** |
| i2v | `lech_dryrun/motion/M01_**_rife**.mp4` | **`.mp4` かつ `_rife` を含む** |
| overlay | `lech_dryrun/overlay/...mp4` | **`cuts[].src` に出さない**（出すと factory 判定になる） |

**スタブの点数は本番と完全に同じにする**（body 70 / ae 15 / motion 16 / factory 85 / overlay 12）。
そうすることで、**素材が1枚も無い段階で `check_asset_reuse` と MGビート密度ゲートの通過を実証できる。**

## 3.5 本番マニフェストへの切り替え

Aから「マニフェストが本番になった」と伝えられたら、**コードは1行も変えず**コマンドの `--assets` を差し替えるだけ:

```bash
./.venv/Scripts/python.exe scripts/build_lech_film_data.py \
  --assets episodes/PD-2026-040-lech/05_visuals/asset_manifest.v001.json \
  --slots  episodes/PD-2026-040-lech/03_script/lech_slots.v001.json \
  --out    remotion/src/data/lech_film.json
```

**差し替え後、[B-DONE-2]〜[B-DONE-7] を全部やり直す。**「スタブで通ったから本番も通るはず」は禁止。

---

# 4. 台本スロット契約（台本は別スレッド。Bは空スロットで組み上げる）

## 4.1 台本の品質水準（オーナー指定）

> **「パルムドール級・AI臭なし」。**

台本は別スレッドで制作中。**Bは台本本文を1文字も書かない。**
Bがやることは「値の入る穴」を定義し、**値が未確定なら null で受けてゲートで止める**設計にすること。

## 4.2 語数の確定値（**Bのタイムライン計算の根拠**）

2026-07-19 に **31話分の実TTS音声**を実測した確定値。
**古い資料の「150 wpm」「173 wpm」「1,700〜1,950語」はすべて誤り。使うな。**

```
ナレーション速度  = 178.1 wpm（実測中央値。範囲 163.7 – 237.4）
目標語数          = 2,140語
許容band          = 2,048 – 2,226語
設計総尺          = 741.4秒 = 12:21（band 690–750秒の内側）
```

判定は **`python scripts/check_script_length.py <script> --json` が唯一の正**。
「だいたい12分ぶん書けた」という自己申告・体感による判断は**禁止**。
（実装は `WPM_MEDIAN=178.1 / WPM_SLOW=163.7 / WPM_FAST=237.4`、`DEFAULT_LO_SECONDS=690.0 / DEFAULT_HI_SECONDS=750.0`。
`preflight_render_gate.py` の `checks` 配列の**先頭**に配線済みで、TTSとレンダーへの課金前にブロックする。）

**背景:** 過去38話中**30話**が目標尺に未達で出荷されている。EP38は1,675語で**9.4分**しかなかった。
原因は spec が wpm を更新したのに台本の語数が150wpm時代のまま据え置かれたこと。**声でも構成でもなく、語数の問題。**

**注意（本設計値でゲートを実行して確認済みの挙動）:** 2,140語は PASS するが、ゲートは同時に
「声が速い側（237.4wpm・williams/florenceで実発生）に振れると9.0分になる」と警告を出す。
これへの対処は**声のスピードを固定すること**であって、語数を2,730語まで増やすことではない
（増やすと中央値ペースで band 上限を突き抜ける）。**ナレ生成直後に必ず実尺を測り、9〜10分台なら編集に進む前に差し戻す。**

## 4.3 タイムライン（**この秒数がAEカードと figures の座標系になる**）

| # | ブロック | 語数 | VO秒 | 開始–終了（秒） |
|---|---|---|---|---|
| 0 | HOOK | 24 | 8.1 | 0.0 – 8.1 |
| 1 | OPENING（`BrandOpening` / `OPENING_SEC=3.5` / 非VO） | 0 | — | 8.1 – 11.6 |
| 2 | 幕1 ふつうの家 | 350 | 117.9 | 11.6 – 131.5 |
| 3 | 幕2 侵入と包囲 | 505 | 170.1 | 131.5 – 303.6 |
| 4 | 幕3 破壊 | 510 | 171.8 | 303.6 – 477.4 |
| 5 | 幕4 誰も払わない | 575 | 193.7 | 477.4 – 673.1 |
| 6 | ENDING | 176 | 59.3 | 673.1 – 732.4 |
| 7 | ENDCARD（`BrandEndcard` / `ENDCARD_SEC=9` / 非VO） | 0 | — | 732.4 – 741.4 |

**検算（Codex は必ず自分で再計算して一致を確認すること）:**

```
[1] 24 + 350 + 505 + 510 + 575 + 176 = 2,140語     ✓ band 2,048–2,226 内
[2] VO合計 = 2,140 / 178.1 × 60 = 720.9 秒
[3] 総尺 = 720.9 + OPENING 3.5 + ENDCARD 9.0 + 幕間の余韻 2.0×4
         = 720.9 + 12.5 + 8.0 = 741.4 秒 = 12:21   ✓ band 690–750秒
```

**`lech_film.json` に入る値:**

```
fps               =  30
hookSeconds       =   8.1
OPENING_SEC       =   3.5   （Bookends 定数。変更しない）
narrationSeconds  = 720.8   （= 幕1〜ED の VO 712.8 + 幕間の余韻 8.0）
ENDCARD_SEC       =   9.0   （Bookends 定数。変更しない）
------------------------------------------------
caseFilmDurationInFrames = round(8.1*30) + round(3.5*30) + ceil(720.8*30) + round(9*30)
                         = 243 + 105 + 21624 + 270 = 22,242 フレーム = 741.4 秒
```

**幕間の余韻 2.0秒 × 4** はリビール直後に画と音だけで持たせる**意図的な間**。**必ずセクション境界に置く**。
（`check_padding.py` はセクション境界の間を「良いペーシング」として許容し、**セクション内部**の長い間だけを
水増しとして罰する。**幕の途中に2秒の間を作ってはならない。**）

| 位置 | 秒 | 内容 |
|---|---|---|
| 幕1 → 幕2 | 129.4 – 131.4 | 平穏な家の最後のカット |
| 幕2 → 幕3 | 301.5 – 303.5 | 装甲車が据えられた画 |
| 幕3 → 幕4 | 475.3 – 477.3 | 崩れた家の全景 |
| 幕4 → ED | 671.0 – 673.0 | 空き地の画 |

## 4.4 スロット契約ファイル

**パス:** `episodes/PD-2026-040-lech/03_script/lech_slots.v001.json`
**スキーマ版:** `lech_slots.v1`
**生成者:** 台本スレッド（Claude）／未確定時は `scripts/make_lech_slots_stub.py`
**消費者:** `build_lech_film_data.py` / `scripts/ae/build_lech_hero_jsx.py` / `LechThumbnails.tsx` / `check_lech_accuracy.py`

```jsonc
{
  "schema_version": "lech_slots.v1",          // 固定文字列。異なれば全ツールが exit 2
  "episode_id": "PD-2026-040-lech",
  "slug": "lech",

  "accuracy_lock": {                          // 全フィールド必須・固定値
    "court": "United States Court of Appeals for the Tenth Circuit",
    "court_short": "Tenth Circuit",
    "decision_year": 2019,
    "citation": "Lech v. Jackson, 791 F. App'x 711 (10th Cir. 2019)",
    "cert_denied_year": 2020,
    "is_supreme_court_decision": false        // 必ず false。true なら即 FAIL
  },

  "title_candidates": [                       // 長さ = ちょうど 2（A/Bテスト）
    {"text": "string", "variant": "A"}        // 1..60文字。二人称必須（"you"/"your" を含む）
  ],

  "thumb_headlines": [                        // 長さ = ちょうど 3（§10 の3案に1:1対応）
    {"concept_id": "T1", "text": "string"}    // 全て大文字。単語数 1..4
  ],

  "hook": {
    "seconds": 8.1,                           // 6.0 <= x <= 10.0
    "lines": ["string"],                      // 長さ 2..4。合計語数 23..31
    "source_cut_ids": ["string"]              // 長さ 3..4。本編 cuts[].id を参照（新規制作禁止）
  },

  "acts": [                                   // 長さ = ちょうど 4
    {"act": 1, "title_ja": "string", "title_card": "string",  // title_card はAEの t01..t04 に出る（大文字・1..28文字）
     "start_sec": 11.6, "narration": "string",
     "rehook_sec": [0.0], "open_loop_close": ["L1"]}
  ],

  "narration_total_words": 2140,              // 2048 <= x <= 2226
  "wpm_assumed": 178.1,                       // 固定 178.1
  "act_word_targets": [350, 505, 510, 575],   // 各 ±8%。合計は総語数と整合必須
  "ed_word_target": 176,

  "beats": [ /* §7.3 の BeatSlot。長さ = 23 */ ],
  "figures": [ /* §6.3 の FigureSlot。長さ = 17 */ ],

  "ed": {
    "payoff_line": "string",                  // 1..180文字
    "cta_line": "string",                     // 1..140文字
    "question_line": "string",                // 1..120文字。必ず "?" で終わる
    "next_hook": "string"                     // 1..120文字
  },

  "facts": {                                  // F01..F09 すべてのキーが存在すること
    "F01": {"value": null, "unit": "hours", "verified": false, "source_url": "", "quote": ""}
  }
}
```

**F-ID の一覧（§7.3 のAEカードに直結する）:**

| ID | 内容 | AEカード |
|---|---|---|
| F01 | 立てこもり時間（時間単位） | b02 |
| F02 | 万引きの被害額（ドル） | b03 左辺 |
| F03 | 家の損害額（ドル）※一家の主張額と市の評価額を**区別して**記録 | b03 右辺 / b05 |
| F04 | 市が支払った額（ドル） | b06 |
| F05 | 補償率（= F04 ÷ F03 × 100）**計算値であることを画面に明記** | b07 |
| F06 | 破壊手段の回数 | b04 |
| F07 | 事件発生日 | b01 |
| F08 | 家にいた人数と無事に脱出したこと | 幕1ナレ |
| F09 | 上告不受理の年 | b08 |

> **「一家の主張額」と「公的に認定された額」は別物。** 混同したら R2 リスク（実在私人の名誉）。
> ナレとAEラベルでは必ず帰属する。OK: `"The family said rebuilding would cost about X."`／
> NG: `"The house was worth X."`

## 4.5 `scripts/validate_lech_slots.py`（BLOCKING）

上記の型・長さ・範囲・単調増加をすべて検査し、違反を
`{"field": "...", "rule": "...", "actual": "..."}` の配列で出力して exit 1。

**加えて次の2つの既存ゲートを内部から呼び、すべて pass で exit 0:**

| 呼ぶゲート | コマンド | 落ちる条件 |
|---|---|---|
| **語数** | `scripts/check_script_length.py <script> --json` | 総語数が **2,048–2,226** の外 |
| **事実性** | `scripts/check_lech_accuracy.py --json` | §2.2 の R1–R5 に違反 |

**自身が検査すること:**

- `narration_total_words` が `hook.lines` + `acts[].narration` + `ed.*` の**実測語数の合計と一致**する
  （宣言だけ2,140にして中身が1,700語、を防ぐ）
- `wpm_assumed == 178.1`
- `sum(act_word_targets) + ed_word_target + hook語数 == narration_total_words`
- 各幕の実語数が `act_word_targets` の **±8%** 以内
- `acts[].start_sec` が §4.3 の値と一致し、単調増加

## 4.6 台本未確定時の動作（**Bはこれで着手できる**）

`scripts/make_lech_slots_stub.py` が **契約と同じ形の stub** を
`03_script/lech_slots.stub.v001.json` に生成する:

- 文字列フィールドは `"[[SLOT:hook.lines[0]]]"` のようなマーカー文字列
- **数値は範囲の中央値**
- `facts.*.value` は **`null`**、`facts.*.verified` は**全て `false`**
- `beats[]` は **23個すべて**、`figures[]` は **17個すべて**を、
  **区間と layout/kind だけ本番と同一・テキストはマーカー**で埋める
  → **MGビート密度ゲートの通過を台本確定前に実証できる**

**`facts[F].verified == false` のときのAEカードの扱い（§7.9 の不変条件）:**

| `required` | `verified` | 動作 |
|---|---|---|
| `false` | `false` | そのカードを**静かに出力から除外**（コンポジタがSKIPするので作品は壊れない） |
| `true` | `false` | **exit 1**（台本工程に差し戻し）。**ただし `--dryrun` のときは警告にして続行** |
| — | `true` | 通常どおり出力 |

**ドライランの出力は `episodes/PD-2026-040-lech/08_edit/_dryrun/` 配下に置き、本番ファイル名を使わない。**

---

# 5. `lech_film.json` の構築（`scripts/build_lech_film_data.py`）

## 5.1 `FilmData` 型（`remotion/src/compositions/CaseFilm.tsx` から。**これに従う**）

```ts
export type Cut = {start: number; dur: number; kind: 'img' | 'footage'; src: string; treatment: string; seed: string};
export type Caption = {start: number; end: number; text: string};
export type HookCut = {start: number; dur: number; kind: string; src: string; seed: string};
export type Beat = {start: number; end: number; lines: string[]};
export type FilmData = {
  fps: number;
  narration: string;
  narrationSeconds: number;
  hookSeconds: number;
  hookLine: string;
  hook: HookCut[];
  cuts: Cut[];
  captions: Caption[];
  graphics: Beat[];
  figures?: FigureSpec[];
  heroCuts?: {start: number; dur: number; src: string}[];
};

export const caseFilmDurationInFrames = (data: FilmData, fps: number) =>
  Math.round((data.hookSeconds || 0) * fps) +
  Math.round(OPENING_SEC * fps) +
  Math.ceil(data.narrationSeconds * fps) +
  Math.round(ENDCARD_SEC * fps);
```

**重要な事実（`kidsforcash_film.json` で確認済み）:**

- **アセットのパスキーは `src`**。`remotion/public/` からの相対パス（`staticFile()` で解決）
- **カットごとの transition / motion フィールドは存在しない。** 動きは全部導出される:
  `treatment` が静止画のレンダラを選び、`seed` がパーティクルを駆動し、
  パン方向は `index % 2`、入りの型は `index % 3` から計算される。**カット単位でトランジションを指定できない**
- `treatment` の実装済みの値: `'depth'` / `'scan'` / `'duotone'` / `'focus'` / `'card'` / `'bleed'`（既定は bleed）
- `kind: 'footage'` は `treatment` を無視して `<Footage>` を描画する
- `graphics` は必須フィールドだが、最近のエピソードは `[]`（kinetic は `figures` に移った）
- `cuts[i].start` は **body 相対**の絶対秒（body は `hookSeconds + OPENING_SEC` から始まる）

## 5.2 カット構成（**§3 のマニフェストから機械的に組む**）

```
総カット 226 = factory 85 + i2v 16 + 静止画 125

[1] 平均ショット長
    絵が必要な区間 = 741.4 − 3.5 − 9.0 = 728.9 秒
    728.9 / 226 = 3.225 秒/カット                      ✓ <=6秒

[2] 静止画占有率（check_animation_mix の MAX_STILL_SHARE = 0.45）
    125本 × 平均 2.05秒 = 256.3 秒 → 256.3 / 741.4 = 34.6%   ✓ <=45%
    動画（factory+i2v）= 728.9 − 256.3 = 472.6 秒
    101カットで 472.6秒 = 平均 4.68秒/カット             ✓ <=6秒

[3] check_asset_reuse
    factory : 85カット / 85本  = 1.00回  ✓ <=1（★factoryは再使用禁止）
    motion  : 16カット / 16本  = 1.00回  ✓ <=2
    still   : 125カット / 70枚 = 1.79回  ✓ <=2
    distinct 合計 = 70 + 16 + 85 = 171 → 171/226 = 0.7566  ✓ >=0.70

[4] factory 下限（30秒に1本 = 24.7 → >=25本）
    85本 >= 25本                                       ✓
```

> **[3] の first-use share の余裕は13カット分しかない。**
> 静止画を1枚減らすと 0.752 に落ちる。**マニフェストが 70枚を割ったら組まずに止めて A に差し戻す。**

## 5.3 カット割り当てのルール（機械的に決める）

1. `stills[role="body"]` を `act` 昇順・`scene_id` 昇順に並べる
2. 各幕で **factory : i2v : 静止画 の比を 85 : 16 : 125 で按分**して幕内のカット数を決める
   - 幕1（11.6–131.5 / 119.9秒）: factory 14 / i2v 2 / 静止画 21 = 37カット
   - 幕2（131.5–303.6 / 172.1秒）: factory 24 / i2v 3 / 静止画 26 = 53カット
   - 幕3（303.6–477.4 / 173.8秒）: factory 20 / i2v 8 / 静止画 26 = 54カット
   - 幕4（477.4–673.1 / 195.7秒）: factory 23 / i2v 3 / 静止画 36 = 62カット
   - ED（673.1–732.4 / 59.3秒）: factory 4 / i2v 0 / 静止画 16 = 20カット
   - **合計 85 / 16 / 125 = 226カット** ✓
3. **同一素材が連続しない**ように配置する（`check_asset_reuse` は連続を検出しないが、視聴体験のため）
4. 静止画は `treatment: "depth"` を既定にし、**同じ treatment を3連続させない**
   （`"depth"` → `"scan"` → `"focus"` を循環させて MGの見た目の変化を出す）
5. **factory は各1回しか出せない。** 使用済み集合を持って二度と引かない
6. i2v の `dur` は **3.0–3.4秒**（実素材が 3.417秒しかない。超えるとループが見える）
7. **AEカードの23区間（§7.2）に重なるカットは、AEが上から完全置換する。**
   それでもカットは存在させる（コンポジタがSKIPしたときに穴が空かないため）

## 5.4 `figures[]` と `captions[]`

- `figures[]` は §6 の17枠
- `captions[]` は §8 の `gen_captions_lech.py` が生成した SRT から流し込む
  （台本未確定時は `hook.lines` と `acts[].narration` のマーカー文字列を機械分割したもの）

## 5.5 合成レイヤー（`overlay`）の扱い — **`cuts[].src` に出さない**

`overlay` の12本は「素材」ではなく「加工」。**`cuts[].src` に入れてはならない。**
入れると `check_asset_reuse.kind_of()` が `/factory` を見て **factory（上限1回）判定**になり、
何度も重ねた時点で FAIL する。

**代わりの扱い:** `remotion/src/compositions/Ep40LechOverlay.tsx` のような**専用レイヤー**として
`CaseFilm` の上に重ねるか、幕ごとに固定の1本を `screen` 合成する。
**`lech_film.json` には `overlays` という独自キーで持たせる**（`FilmData` の optional 拡張。
`CaseFilm` は知らないキーを無視するので既存エピソードに影響しない）。

## 5.6 CLI

```bash
./.venv/Scripts/python.exe scripts/build_lech_film_data.py \
  --assets <asset_manifest path> \
  --slots  <lech_slots path> \
  --out    remotion/src/data/lech_film.json \
  [--captions episodes/PD-2026-040-lech/08_edit/captions.final.v001.srt]
```

**`--assets` に渡されたファイルの `is_stub` によって処理を変えないこと**（§0.2）。

---

# 6. Remotion 側 `figures[]` 17枠

## 6.1 MGビート密度の検算

```
AEカード（§7）           23
Remotion FigureBeats     17
--------------------------
合計                     40 枠

40 / 12.36分 = 3.24 /分      ✓ check_motion_density.MIN_KINETIC_BEATS_PER_MIN = 2.5
種類 = AE 9レイアウト + Remotion 7 kind = 16種  ✓ >=3種
```

## 6.2 ★★★ `FigureSpec` の `kind` は**実在する文字列でなければならない** ★★★

> **旧設計書は存在しない kind 名を書いていた。**
> `ActTitle` / `MechanismReveal` / `QuoteCard` / `ComparisonBars` / `RouteMap` / `PinDropMap` は
> **`FigureBeats.tsx` に存在しない。そのまま書くと描画されない（無言で消える）。**

**実在する `kind` 文字列（`remotion/src/components/FigureBeats.tsx` の union から。EP40で使う7種）:**

| 使う `kind` | 必須プロパティ |
|---|---|
| `lowerthird` | `primary: string` / `secondary?: string` / `accent?: string` |
| `stat` | `value: number` / `label: string` / `prefix?` `suffix?` `decimals?` `topLabel?` |
| `quote` | `quote: string` / `attribution: string` |
| `mechanism` | `mechanism: 'closingdoor' \| 'gears' \| 'faultsplit'` ★discriminant は `kind`、変種は `mechanism` |
| `compbars` | `items: {label: string; value: number; accent?: string}[]` |
| `routemap` | `pins: {x: number; y: number; label?: string}[]`（x/y は 0..1 の画面比） |
| `kinetic` | `lines: string[]` / `style?: 'wordpop' \| 'maskslide' \| 'emphasis'` / `emphasisWords?: string[]` |

全 variant に共通で `start: number` / `end: number` が必要。

> **`acttitle` も実在する**（`{kind:'acttitle'; title: string; kicker?: string; index?: number}`）が、
> **EP40では幕頭タイトルを After Effects 側（§7.4 レイアウトE）で作る**ので Remotion では使わない。
> 「Remotionでやると安っぽくなる箇所をAEに寄せる」というオーナー指示への対応。

## 6.3 17枠の配置（**AEの23区間と1秒も重ならない**）

| # | id | 秒 | dur | kind | 内容 |
|---|---|---|---|---|---|
| 1 | f01 | 20.0–25.0 | 5.0 | `lowerthird` | 場所と時期の提示 |
| 2 | f02 | 55.0–60.0 | 5.0 | `stat` | 一家の人数（F08） |
| 3 | f03 | 92.0–97.0 | 5.0 | `lowerthird` | 家の築年・ローン残の文脈 |
| 4 | f04 | 150.0–157.0 | 7.0 | `routemap` | 逃走経路と家の位置関係 |
| 5 | f05 | 175.0–180.0 | 5.0 | `lowerthird` | 通報から現着までの時刻 |
| 6 | f06 | 215.0–221.0 | 6.0 | `quote` | 警察無線／報告の逐語 |
| 7 | f07 | 265.0–270.0 | 5.0 | `stat` | 動員された車輌数／人数 |
| 8 | f08 | 330.0–336.0 | 6.0 | `kinetic` | 「壊す判断は、誰がしたのか」（`style: 'emphasis'`） |
| 9 | f09 | 360.0–366.0 | 6.0 | `compbars` | 使われた手段の内訳 |
| 10 | f10 | 385.0–390.0 | 5.0 | `stat` | 事件が終わるまでの経過時間 |
| 11 | f11 | 455.0–461.0 | 6.0 | `quote` | 現場指揮の判断の逐語 |
| 12 | f12 | 500.0–507.0 | 7.0 | `mechanism`（`faultsplit`） | **Takings Clause と police power 例外の分岐**（EP40のドクトリン説明の主役） |
| 13 | f13 | 535.0–541.0 | 6.0 | `quote` | 市の回答の逐語 |
| 14 | f14 | 575.0–582.0 | 7.0 | `mechanism`（`closingdoor`） | 限定免責が閉じる扉 |
| 15 | f15 | 590.0–596.0 | 6.0 | `compbars` | 市の評価額 vs 一家の主張額（F03） |
| 16 | f16 | 645.0–652.0 | 7.0 | `mechanism`（`gears`） | 第10巡回区の論理と反対の論理 |
| 17 | f17 | 700.0–705.0 | 5.0 | `lowerthird` | ED の締め（判例引用） |

**配置ルール:**

1. **AEの23区間（§7.2）と1秒でも重ならないこと。** `validate_lech_beats.py` が両方を突き合わせて検査する
2. **同じ kind を連続させない**（`mechanism` の直後に `mechanism` は不可 → f12/f14/f16 は間に別 kind を挟んでいる）
3. 1枠の長さは **5.0–7.0秒**
4. `quote` の引用文は **§2.2 の accuracy_lock 検査対象**（`figures[].quote` を対象パスに含めること）
5. **台本未確定時は区間と kind だけ本番と同一で、テキストは `[[SLOT:...]]` マーカー**にする

---

# 7. ★After Effects の守備範囲を広げる（オーナー指示への対応）

## 7.1 なぜ広げるか

> オーナー指示: **「After Effects をもっと効果的に使え。データカードだけでなく、
> 転換部のタイトルカード、書類提示、立てこもりの時系列可視化、家の見取り図と破壊箇所の図解、
> 幕間のトランジションなど、Remotionでやると安っぽくなる箇所をAEに寄せろ。」**

**在庫の裏付け（`H:\pd-media\assets\factory`）:** `diagram_assets` / `transitions` / `typography_assets` /
`parallax_layers` / `lottie_assets` は**すべて0本**。
**図解・トランジション・タイポは在庫が無い＝自作するしかない。** その自作先が After Effects。

**旧設計はAEカード8枚だった。EP40では23枚に広げる。**

## 7.2 AEカード23枚の配置（**単調増加・重複ゼロ。この表が契約**）

| id | レイアウト | 内容 | F-ID | 背景静止画 | start | end | dur | 必須 |
|---|---|---|---|---|---|---|---|---|
| **t01** | E ACT_TITLE_CARD | 幕1 タイトル | — | S01 | 11.600 | 15.100 | 3.5 | 必須 |
| **h01** | H HOUSE_PLAN | 家の見取り図（破壊前） | — | **なし（ベクター）** | 118.000 | 124.000 | 6.0 | 必須 |
| **s01** | I SEAM_TRANSITION | 幕1→幕2 の余韻 | — | **なし** | 129.400 | 131.400 | 2.0 | 必須 |
| **t02** | E ACT_TITLE_CARD | 幕2 タイトル | — | S13 | 131.500 | 135.000 | 3.5 | 必須 |
| **b01** | C DATE_STAMP | 事件が起きた年 | F07 | S09 | 136.000 | 141.000 | 5.0 | 必須 |
| **d01** | F DOCUMENT_CARD | 警察報告書の提示 | — | S55 | 200.000 | 206.000 | 6.0 | 必須 |
| **b02** | A CENTER_STACK | 立てこもり時間 | F01 | S21 | 252.000 | 258.000 | 6.0 | 必須 |
| **g01** | G SIEGE_TIMELINE | 立てこもりの時系列 | F01 | **なし（ベクター）** | 280.000 | 288.000 | 8.0 | 必須 |
| **s02** | I SEAM_TRANSITION | 幕2→幕3 の余韻 | — | **なし** | 301.500 | 303.500 | 2.0 | 必須 |
| **t03** | E ACT_TITLE_CARD | 幕3 タイトル | — | S23 | 303.600 | 307.100 | 3.5 | 必須 |
| **b03** | B SPLIT_COMPARE | 万引き被害額 vs 家の損害額 | F02+F03 | S44 | 312.000 | 319.000 | 7.0 | 必須 |
| **b04** | A CENTER_STACK | 破壊手段の回数 | F06 | S31 | 412.000 | 417.500 | 5.5 | **条件付き** |
| **h02** | H HOUSE_PLAN | 破壊箇所の図解（同じ図に穴を重ねる） | — | **なし（ベクター）** | 440.000 | 447.000 | 7.0 | 必須 |
| **s03** | I SEAM_TRANSITION | 幕3→幕4 の余韻 | — | **なし** | 475.300 | 477.300 | 2.0 | 必須 |
| **t04** | E ACT_TITLE_CARD | 幕4 タイトル | — | S48 | 477.400 | 480.900 | 3.5 | 必須 |
| **b05** | A CENTER_STACK | 家の損害額 | F03 | S43 | 492.000 | 498.000 | 6.0 | 必須 |
| **d02** | F DOCUMENT_CARD | 市の回答書の提示 | — | S56 | 520.000 | 526.500 | 6.5 | 必須 |
| **d03** | F DOCUMENT_CARD | 一家の見積書／請求書 | F03 | S57 | 560.000 | 566.000 | 6.0 | **条件付き** |
| **b06** | A CENTER_STACK / COUNTDOWN | 一家が受け取った額（**L1のペイオフ**） | F04 | S45 | 605.000 | 611.500 | 6.5 | 必須 |
| **b07** | D RATIO_BAR | 補償率（計算値・%） | F05 | S62 | 620.000 | 626.000 | 6.0 | **条件付き** |
| **g02** | G CASE_TIMELINE | 訴訟の経過（提訴→地裁→第10巡回区→上告不受理） | F09 | **なし（ベクター）** | 630.000 | 638.000 | 8.0 | 必須 |
| **b08** | C DATE_STAMP | 判断した裁判所と年（**L3のペイオフ**） | F09 | S63 | 655.000 | 661.000 | 6.0 | 必須 |
| **s04** | I SEAM_TRANSITION | 幕4→ED の余韻 | — | **なし** | 671.000 | 673.000 | 2.0 | 必須 |

**条件付きの意味:** `required: false`。`facts[F-ID].verified == false` なら**静かに出力から除外**する。

**検算（Codex は必ず自分で再計算して一致を確認すること）:**

```
[1] 単調増加・重複ゼロ
    11.6<15.1 < 118.0<124.0 < 129.4<131.4 < 131.5<135.0 < 136.0<141.0
  < 200.0<206.0 < 252.0<258.0 < 280.0<288.0 < 301.5<303.5 < 303.6<307.1
  < 312.0<319.0 < 412.0<417.5 < 440.0<447.0 < 475.3<477.3 < 477.4<480.9
  < 492.0<498.0 < 520.0<526.5 < 560.0<566.0 < 605.0<611.5 < 620.0<626.0
  < 630.0<638.0 < 655.0<661.0 < 671.0<673.0                         ✓ 23区間・重複ゼロ

[2] HOOK(0–8.1) と ENDCARD(732.4–741.4) に重ねない
    最小 11.600 > 11.6（幕1開始と同時）  ✓
    最大 673.000 < 673.1（ED開始）        ✓ ED のペイオフに図版をかぶせない

[3] 合計時間
    3.5+6+2+3.5+5+6+6+8+2+3.5+7+5.5+7+2+3.5+6+6.5+6+6.5+6+8+6+2 = 117.5 秒
    117.5 / 741.4 = 15.85%
    （旧設計の8枚48秒=6.5%から拡大。オーナー指示の「AEに寄せる」への対応）

[4] Remotion figures 17枠（§6.3）と1秒も重ならないこと → validate_lech_beats.py が検査
```

## 7.3 `beats.json` のスキーマ

**パス（本番）:** `episodes/PD-2026-040-lech/08_edit/ae_hero/beats.json`
**パス（ドライラン）:** `episodes/PD-2026-040-lech/08_edit/_dryrun/ae_hero/beats.json`
**生成者:** `scripts/ae/build_lech_hero_jsx.py`
**消費者:** `lech_hero.jsx`（AE）と `scripts/ae/composite_lech_hero.py`

```jsonc
{
  "schema_version": "lech_beats.v1",
  "episode_id": "PD-2026-040-lech",
  "fps": 30,                                  // 固定 30。本編 mp4 と一致必須
  "width": 1920, "height": 1080,
  "beats": [
    {
      "id": "b01",                            // ^(b0[1-8]|t0[1-4]|d0[1-3]|g0[1-2]|h0[1-2]|s0[1-4])$
      "layout": "DATE_STAMP",                 // "CENTER_STACK"|"SPLIT_COMPARE"|"DATE_STAMP"|"RATIO_BAR"
                                              // |"ACT_TITLE_CARD"|"DOCUMENT_CARD"|"SIEGE_TIMELINE"
                                              // |"CASE_TIMELINE"|"HOUSE_PLAN"|"SEAM_TRANSITION"
      "count_type": "CT_DATE",                // §7.5。数値を出さないレイアウトは "CT_NONE"
      "fact_id": "F07",                       // null 可（t/s/h 系）
      "required": true,

      "start": 136.000,                       // 本編mp4上の絶対秒。小数第3位まで。単調増加・重複禁止
      "end": 141.000,
      "dur": 5.000,                           // = round(end-start, 3)

      "still": "H:/pd-media/assets/ai/lech/S09_02.png",  // ベクター系は null
      "top": "GREENWOOD VILLAGE",             // 1..24文字・全て大文字。R1検査対象
      "bottom": "AN ORDINARY AFTERNOON",      // 1..28文字・全て大文字。R1検査対象
      "caption": "string",                    // ★改行を含めないこと（AE制約）。最大50文字
      "footnote": null,                       // string|null。最大44文字。b08 のみ使う（§2.3）

      "value": 2019, "value_b": null,
      "decimals": 0, "thousands": false,      // CT_DATE は thousands 必須 false
      "prefix": "", "suffix": "",
      "label_a": null, "label_b": null, "ratio_note": null,

      "numKeys": [[0.55, "0"], [0.61, "312"]],// Python で全事前計算した (時刻, 表示文字列) のホールドキー
      "numKeys_b": null,                      // JS 側で数値整形を一切しないこと（EP38の確定ルール）
      "numReveal": 0.45,
      "head": 0.1333, "tail": 0.1333,         // = 4/30。頭と尻の黒シーム

      // --- レイアウト別の追加ペイロード（該当しないものは null）---
      "act_index": null,                      // ACT_TITLE_CARD: 1..4
      "act_title": null,                      // ACT_TITLE_CARD: 大文字 1..28文字
      "doc_lines": null,                      // DOCUMENT_CARD: string[]（1..3行・各 1..46文字・大文字）
      "timeline_events": null,                // SIEGE/CASE_TIMELINE: [{"t":"14:20","text":"..."}] 3..6件
      "plan_rooms": null,                     // HOUSE_PLAN: [{"x":0.2,"y":0.3,"w":0.25,"h":0.2,"label":"KITCHEN"}]
      "plan_breaches": null,                  // HOUSE_PLAN: [{"x":0.42,"y":0.28,"r":0.05}] 破壊箇所
      "seam_mode": null,                      // SEAM_TRANSITION: "dip" | "wipe" | "grain"

      "out": "C:/.../08_edit/ae_hero/render/b01.mp4"
    }
  ]
}
```

## 7.4 レイアウト定義（**9種**）

**共通レイヤースタック（下 → 上）。`build_kfc_hero_jsx.py` で動作実証済みの構成を踏襲する:**

| L | 内容 | 実装 |
|---|---|---|
| L9 | 黒ソリッド背景 | `comp.layers.addSolid([0,0,0], "bg", W, H, 1.0)` |
| L8 | 静止画（fill + イーズ付きプッシュイン + ドリフト） | scale `fill → fill*1.08`（0→dur・ease 25）、position `[W/2-18, H/2+10] → [W/2+18, H/2-10]`（ease 20）。**ベクター系レイアウトではこのレイヤーを作らない** |
| L7 | グレードウォッシュ | **EP40は暖色**: `addSolid([0.14,0.11,0.06])` / MULTIPLY / opacity **30** |
| L6 | 羽根付き楕円ビネット | 黒ソリッド + SUBTRACT マスク・feather `[260,260]`・opacity 62 |
| L5 | グロー（下中央からのADDランプ） | Ramp start `[W/2, H*0.42]` GOLD → end `[W/2, H*0.95]` 黒 / `ADBE Ramp-0005` = 2（radial）/ opacity 0→22→14 |
| L4 | ライトスイープ | 白ソリッド 360×H*1.6 / ADD / **`"ADBE Rotate Z"` = 18** / position `-300 → W+300`（0.5s→1.25s・ease 45）/ opacity 0→18→0 |
| L3 | 上ラベル（Oswald） | レイアウト別の座標 |
| L2b | アクセントライン（GOLD・scaleX ワイプ） | `[0,100] → [100,100]`（0.55s→1.05s・ease 90）/ **`layer.motionBlur = true`** |
| L2 | 主数値（Anton・GOLD） | §7.5 のカウントアップ / **`layer.motionBlur = true`** |
| L1b | 下ラベル（Oswald・WHITE） | reveal 1.15s |
| L1 | 字幕ロワーサード | バー `[0.02,0.04,0.08]` W×130 / opacity 0→64→0 |
| L0 | 黒シームディップ（head/tail 各4フレーム） | opacity 100→0（head）/ 0→100（tail）・ease 40 |

**色定数（0..1 float・EP40）:**

```python
GOLD   = [0.898, 0.710, 0.227]   # #E5B53A — EP40 アクセント（EP39 の #1F6BFF と分離）
WHITE  = [0.961, 0.969, 0.980]
SILVER = [0.588, 0.627, 0.682]
DUST   = [0.827, 0.769, 0.667]   # SPLIT_COMPARE の左辺・弱い側
PAPER  = [0.902, 0.878, 0.827]   # DOCUMENT_CARD の紙面
```

**フォント:** 数値 = **Anton Regular** / ラベル・字幕 = **Oswald Medium**
（`C:\Users\aab15\AppData\Local\Microsoft\Windows\Fonts\Anton.ttf` / `Oswald.ttf` に**実在を確認済み**）
必ず `build_kfc_hero_jsx.py` と同じ **`psName()` ランタイム解決**を使い、無言の代替フォント置換を防ぐ。

---

### 7.4.1 LAYOUT A — CENTER_STACK（b02 / b04 / b05 / b06）

| 要素 | 位置 | フォント/サイズ | トラッキング | 色 |
|---|---|---|---|---|
| 上ラベル | `[W/2, H*0.205]` | Oswald 44 | 340 | SILVER |
| アクセントライン | `[W/2, H*0.485]`・460×6 | — | — | GOLD |
| 主数値 | `[W/2, H*0.42]` | Anton **250** | 0 | GOLD |
| 下ラベル | `[W/2, H*0.60]` | Oswald 64 | 120 | WHITE |
| 字幕バー | `[W/2, H*0.90]`・W×130 | Oswald 42 | 20 | WHITE |

### 7.4.2 LAYOUT B — SPLIT_COMPARE（b03 のみ）

**「万引きの被害額」対「家の損害額」の桁違いを1画面で殴る。EP40で最も重要な1枚。**

| 要素 | 位置 | フォント/サイズ | 色 |
|---|---|---|---|
| 上ラベル | `[W/2, H*0.16]` | Oswald 40 / tracking 340 | SILVER |
| 縦の分割線 | `[W/2, H*0.50]`・4×H*0.42 | — | SILVER opacity 40 |
| 左ラベル `label_a` | `[W*0.27, H*0.31]` | Oswald 38 / tracking 180 | SILVER |
| 左数値（万引き額） | `[W*0.27, H*0.46]` | Anton **150** | **DUST** |
| 右ラベル `label_b` | `[W*0.73, H*0.31]` | Oswald 38 / tracking 180 | SILVER |
| 右数値（家の損害額） | `[W*0.73, H*0.46]` | Anton **210** | **GOLD** |
| 下ラベル | `[W/2, H*0.66]` | Oswald 56 / tracking 120 | WHITE |

**タイミング（区間長 7.0s）:**
- 0.15s 上ラベル reveal ／ 0.35–0.85s 縦分割線 `scaleY [0,100]→[100,100]`（ease 85）
- **0.50–1.30s 左（小さい額）を先に**カウント → 0.20s の「間」
- **1.50–2.50s 右（大きい額）**を**より長い時間かけて**カウント = 桁違いの体感
- 2.70s 下ラベル reveal
- **左数値は右のカウント開始と同時に opacity 100→55**（0.15s・ease 60）= 主役の切替

### 7.4.3 LAYOUT C — DATE_STAMP（b01 / b08）

| 要素 | 位置 | フォント/サイズ | 色 |
|---|---|---|---|
| 上ラベル | `[W/2, H*0.30]` | Oswald 44 / tracking 340 | SILVER |
| 年（主数値） | `[W/2, H*0.46]` | Anton **190** | GOLD |
| 横罫 | `[W/2, H*0.545]`・620×4 | — | GOLD opacity 92 |
| 下ラベル | `[W/2, H*0.63]` | Oswald 52 / tracking 120 | WHITE |

**b08 のラベル確定値（accuracy_lock 準拠。この文字列を使う）:**

```
top      = "THE TENTH CIRCUIT"
value    = 2019
bottom   = "NO COMPENSATION OWED"
footnote = "THE SUPREME COURT DECLINED TO HEAR IT"
```

`footnote` は同一コンプ内 **3.6s 地点**に `[W/2, H*0.72]` / Oswald 34 / tracking 90 / SILVER /
opacity 0→88（3.6→3.9s・ease 70）で出す。

### 7.4.4 LAYOUT D — RATIO_BAR（b07）

| 要素 | 位置 | サイズ/色 |
|---|---|---|
| 上ラベル | `[W/2, H*0.22]` / Oswald 44 / tracking 340 / SILVER |
| 棒の「全体」枠 | `[W/2, H*0.44]`・1200×26 / SILVER outline opacity 45 |
| 棒の「支払われた分」 | 枠の左端から / GOLD / **幅 = 1200 × (value/100)** |
| 主数値（%） | `[W/2, H*0.58]` / Anton **160** / GOLD |
| 下ラベル | `[W/2, H*0.70]` / Oswald 52 / tracking 120 / WHITE |
| `ratio_note` | `[W/2, H*0.78]` / Oswald 28 / tracking 60 / SILVER opacity 75 |

**タイミング（6.0s）:** 0.20s 上ラベル ／ 0.45–1.05s 枠 `scaleX [0,100]→[100,100]`（ease 90）／
1.15–2.15s GOLD の棒が `scaleX 0 → (value/100)*100`（**アンカーポイントを左端に置く**）＋ 数値が同期してカウント ／
2.45s 下ラベル ／ 2.75s `ratio_note`

**`ratio_note` は必須。** 計算値であることを画面上で明示しないと事実性違反になる。
確定文字列: `"CALCULATED FROM THE TWO FIGURES ABOVE"`

### 7.4.5 LAYOUT E — ACT_TITLE_CARD（t01–t04）★新規

**幕頭のタイトルを Remotion の `acttitle` ではなく AE で作る**（オーナー指示「Remotionでやると安っぽくなる箇所をAEに寄せろ」）。

| 要素 | 位置 | フォント/サイズ | 色 |
|---|---|---|---|
| 静止画 L8 | 全面 | — | **opacity 55 に落とす**（文字を主役にする） |
| 幕番号（`act_index`） | `[W/2, H*0.34]` | Anton **120** | GOLD opacity 70 |
| 幕タイトル（`act_title`） | `[W/2, H*0.50]` | Oswald **86** / tracking 180 | WHITE |
| 横罫（タイトルの下） | `[W/2, H*0.60]`・520×5 | — | GOLD |

**タイミング（3.5s）:**

```
0.00–0.13  head 黒ディップ
0.20       幕番号が scale [140,140] → [100,100] + opacity 0→70（0.20→0.62s・ease 80）
0.45       幕タイトルが「マスク切れ上がり」:
           位置 [W/2, H*0.50+64] → [W/2, H*0.50]（0.45→1.05s・ease 88）
           opacity 0→100（0.45→0.90s・ease 70）
           ★opacity 単独ではなく position と必ず対で動かす
0.90–1.45  横罫 scaleX [0,100] → [100,100]（ease 90）・アンカーは左端・motionBlur = true
1.45–3.37  ホールド。静止画のプッシュインだけが継続する（完全静止フレームを作らない）
3.37–3.50  tail 黒ディップ
```

### 7.4.6 LAYOUT F — DOCUMENT_CARD（d01 / d02 / d03）★新規

**警察報告書・市の回答書・請求書の「提示」。** 判読不能の書類写真の上に、
**AEで打った読める1〜3行だけ**を重ねる。「読める箇所」を制御することで、
「読めそうで読めない書類」の不気味さと「決定的な1行」の対比を作る。

| 要素 | 位置 | フォント/サイズ | 色 |
|---|---|---|---|
| 静止画 L8 | 全面 | — | opacity 100・プッシュインは弱め（`fill → fill*1.04`） |
| 紙面のハイライト矩形 | `[W/2, H*0.50]`・W*0.62 × H*0.44 | — | PAPER opacity 12 / ADD |
| 上ラベル（書類の種別） | `[W/2, H*0.20]` | Oswald 40 / tracking 340 | SILVER |
| `doc_lines[0..2]` | `[W*0.28, H*0.40 + i*76]`・**左寄せ** | Oswald **52** / tracking 40 | WHITE |
| 各行の下線（GOLD） | 行の下 8px・行幅×4 | — | GOLD opacity 85 |
| 下ラベル | `[W/2, H*0.76]` | Oswald 44 / tracking 120 | WHITE |

**タイミング（6.0–6.5s）:**

```
0.20       上ラベル revealUp
0.55       紙面ハイライトが opacity 0→12 + scale [104,104]→[100,100]（0.55→1.05s・ease 70）
0.85 + i×0.45   doc_lines[i] が1行ずつ:
           x位置 [W*0.28-40] → [W*0.28]（0.55s・ease 82）+ opacity 0→100（0.40s）
           ★スタガー 0.45秒。3行なら 0.85 / 1.30 / 1.75s
1.15 + i×0.45   その行の下線が scaleX 0→1（アンカー左端・0.40s・ease 90）・motionBlur = true
2.60       下ラベル revealUp
2.60–dur-0.13  ホールド
```

**`doc_lines` の制約:** 各行 **1..46文字・全て大文字・改行禁止**。**R1の検査対象に含めること。**

### 7.4.7 LAYOUT G — SIEGE_TIMELINE / CASE_TIMELINE（g01 / g02）★新規

**静止画を使わない。純ベクター。** 黒背景 + グラデーションの上に横一直線のタイムラインを引き、
イベントマーカーを左から順に立てる。

| 要素 | 位置 | 仕様 |
|---|---|---|
| 背景 | 全面 | 黒 + 下から GOLD の ADD ランプ（L5 と同じ） |
| 上ラベル | `[W/2, H*0.18]` | Oswald 44 / tracking 340 / SILVER |
| 主軸線 | `[W/2, H*0.52]`・(W*0.76)×4 | SILVER opacity 55 |
| イベントマーカー | 軸上の等間隔 `x_i = W*0.12 + i*(W*0.76)/(n-1)` | GOLD の円（直径28）+ 上に時刻テキスト・下に説明テキスト |
| 時刻（`t`） | `[x_i, H*0.44]` | Anton 46 / GOLD |
| 説明（`text`） | `[x_i, H*0.62]` | Oswald 30 / tracking 40 / WHITE / **1行・最大24文字** |

**タイミング（8.0s・イベント3〜6件）:**

```
0.20       上ラベル revealUp
0.50–1.30  主軸線が scaleX 0→1（アンカー左端・ease 88）・motionBlur = true
1.40 + i×0.62  マーカー i が:
           円: scale [0,0] → [130,130] → [100,100]（0.35s・ease 80）
           時刻: 位置 y-32 → y + opacity 0→100（0.30s・ease 70）
           説明: 位置 y+28 → y + opacity 0→100（0.30s・0.10s遅らせる）
           ★4件なら 1.40 / 2.02 / 2.64 / 3.26s
最後のマーカーの後 1.20秒以上のホールドを確保する（§7.6）
```

**g02（CASE_TIMELINE）の確定イベント（accuracy_lock 準拠）:**

```json
[{"t":"2015","text":"THE SIEGE"},
 {"t":"2016","text":"THE FAMILY SUES"},
 {"t":"2019","text":"TENTH CIRCUIT RULES"},
 {"t":"2020","text":"REVIEW DECLINED"}]
```

> **`"REVIEW DECLINED"` と書く。`"SUPREME COURT DENIES"` と書いてはならない**（R1違反）。

### 7.4.8 LAYOUT H — HOUSE_PLAN（h01 / h02）★新規

**家の見取り図と破壊箇所の図解。静止画を使わない純ベクター。**
**h01 と h02 は同じ間取りを描き、h02 だけ破壊箇所（`plan_breaches`）を重ねる。**
この「同じ図に穴が開く」ことが視覚的な主張になる。

| 要素 | 仕様 |
|---|---|
| 背景 | 黒 + 微細なグリッド（`ADBE Grid` エフェクトではなく、細いソリッドを並べて作る） |
| 上ラベル | `[W/2, H*0.14]` / Oswald 40 / tracking 340 / SILVER |
| 部屋の矩形（`plan_rooms`） | 各 `{x,y,w,h,label}` は **0..1 の画面比**。実座標 = `[x*W*0.62 + W*0.19, y*H*0.60 + H*0.24]`。線幅4・SILVER opacity 70・塗りなし（マスクで抜く） |
| 部屋ラベル | 矩形の中心 / Oswald 26 / tracking 60 / SILVER opacity 80 |
| 破壊箇所（`plan_breaches`） | 各 `{x,y,r}` に GOLD の円（塗り）+ 外側に GOLD のリング（opacity 45）|

**タイミング（h01 = 6.0s / h02 = 7.0s）:**

```
0.20       上ラベル revealUp
0.50 + i×0.18  部屋 i の矩形が scaleX 0→1 → scaleY 0→1 の2段（各0.28s・ease 85）
               ★部屋数6なら 0.50 〜 1.40s で全部出る
1.60 + i×0.10  部屋ラベルが opacity 0→80 + scale [92,92]→[100,100]（0.25s）

--- h02 のみ ---
2.60 + i×0.35  破壊箇所 i:
               リング: scale [0,0] → [180,180]、opacity 60→0（0.55s・ease 40）= 衝撃波
               円:     scale [0,0] → [100,100]、opacity 0→100（0.30s・ease 75）
               ★同時に該当する部屋の矩形の色を SILVER → GOLD に切り替える
                 （色のキーフレームではなく、GOLD版の矩形レイヤーを重ねて opacity で入れ替える）
最後の要素の後 1.20秒以上のホールドを確保する
```

### 7.4.9 LAYOUT I — SEAM_TRANSITION（s01–s04）★新規

**幕間の余韻 2.0秒に重ねるトランジション。**
**静止画も文字も出さない。** 本編の画の上に、光と粒子だけをかける。

| `seam_mode` | 使う位置 | 仕様 |
|---|---|---|
| `"dip"` | s01（幕1→幕2） | 黒ソリッドの opacity 0→38→0（0→1.0→2.0s・ease 55）。**完全な黒にはしない**（画を殺さない） |
| `"wipe"` | s02（幕2→幕3）／ s03（幕3→幕4） | GOLD の細い縦バー（幅18×H*1.4・Rotate Z = 12）が `x: -200 → W+200`（0.15→1.45s・ease 62）。ADD・opacity 0→34→0。**`layer.motionBlur = true`** |
| `"grain"` | s04（幕4→ED） | 白ソリッド + `ADBE Fractal Noise` の代わりに、細かいドットのソリッドを scale 0.98→1.06 でゆっくり動かし、ADD・opacity 0→14→0 |

> **SEAM は「本編の画を消さない」ことが要件。** opacity の最大値を 38 / 34 / 14 に抑えているのはそのため。
> `head` / `tail` の黒ディップは **SEAM では使わない**（`head = tail = 0.0`）。
> 黒ディップを入れると幕間が二重に暗くなって「切れた」ように見える。

## 7.5 カウントアップ型（すべて Python 側で全キーを事前計算）

`build_kfc_hero_jsx.py` の `count_keys()` を踏襲（ease-out cubic・最後に正確値へ settle）。

| 型ID | 用途 | decimals | thousands | prefix | suffix | キー数 | 窓 |
|---|---|---|---|---|---|---|---|
| `CT_INT` | 時間・回数 | 0 | false | "" | `" HOURS"` / `" ROUNDS"` 等 | 18 | 0.55→1.55s |
| `CT_MONEY` | ドル（大） | 0 | **true** | `"$"` | "" | **24** | 0.55→1.85s |
| `CT_MONEY_M` | ドル（百万単位） | 1 | false | `"$"` | `"M"` | 18 | 0.55→1.55s |
| `CT_PCT` | 率 | 1 | false | "" | `"%"` | 18 | 1.15→2.15s |
| `CT_DATE` | 年 | 0 | **false** | "" | "" | **12** | 0.55→1.25s |
| `CT_COUNTDOWN` | **b06 専用** | 0 | true | `"$"` | "" | **28** | 0.55→2.35s |
| `CT_NONE` | 数値を出さない（t / d / g / h / s 系） | — | — | — | — | 0 | — |

**`CT_DATE` の注意:** `thousands=false` 必須。`2,019` と出たら即バグ。

**`CT_COUNTDOWN`（b06・EP40の感情のピーク）の仕様:**

- **b05 で表示した損害額（F03）から出発し、一家が受け取った額（F04）まで減っていく**
- ease は `ease_out_cubic` ではなく **`ease_in_out_cubic`** を使う（急落してから減速 = 落下の体感）:

```python
def ease_in_out_cubic(p): return 4*p**3 if p < 0.5 else 1 - ((-2*p+2)**3)/2
```

- 到達後 **0.35s のホールド**を挟み、下ラベルを reveal（この間、画面はほぼ静止 = 沈黙の演出）
- 数値の色は GOLD → **到達の 0.10s 後に WHITE へ切り替え**
  （**別レイヤーを重ねて opacity で入れ替える**。AE の TextDocument で色をアニメすると不安定）
- **`bottom` の確定文字列 = `"WHAT THE FAMILY RECEIVED"`**（帰属を保つ。「補償額」と断定しない）

## 7.6 カウント窓と区間の関係（**必ず守る**）

```
0.000                      dur
|--head--|--reveal--|--count--|--hold--|--tail--|
  4/30s              §7.5の窓          >=1.20s   4/30s
```

**カウント／最後のアニメーション終了から区間終端まで最低 1.20 秒のホールドを確保する。**
これが無いと読めない。`dur < (anim_end + 1.20 + tail)` になったら
`build_lech_hero_jsx.py` は **exit 1**（黙って詰めない）。

## 7.7 ★このマシン固有の罠（EP38で実際に踏んで潰した12件。1つでも忘れると無言で品質が落ちる）

| # | 罠 | 正しい対処 |
|---|---|---|
| 1 | **イーズが無言で効かず等速になる** | `setTemporalEaseAtKey` の配列次元は spatial プロパティ（Position）では**1個**。`var dim = 1; if (!prop.isSpatial) { var v0 = prop.value; dim = (v0 instanceof Array) ? v0.length : 1; }` |
| 2 | **テンプレート名が英語だと失敗する** | AE 2026・日本語ロケール。RS = **`"最良設定"`** / OM = **`"H.264 - レンダリング設定を一致 - 15 Mbps"`**。英語名（`"Best Settings"` / `"H.264 - Match Render Settings - 15 Mbps"`）は try/catch のフォールバックに置くだけ |
| 3 | **字幕に `\n` を入れると literal で表示される** | AE の TextDocument の改行は `\n` ではない。**`caption` は1行に保つ**（最大50文字・改行禁止）。どうしても必要なら `\r` |
| 4 | **`app.newProject()` が headless でハングする** | `-noui` では保存プロンプトで固まる。**使うな。** 代わりに既存の同名コンプを防御的に削除: `for (var ri = proj.numItems; ri >= 1; ri--) { var itx = proj.item(ri); if (itx instanceof CompItem && String(itx.name).indexOf("LECH_") === 0) itx.remove(); }` |
| 5 | **ビルドが遅く、早期killしてしまう** | ビルド ~100–120秒（**カードが23枚なので EP38 の6枚より長い。250–350秒を見込む**）／レンダは速い。**jsx 末尾が書く完了マーカー `render/_build_ok.txt` をポーリングせよ。タイムアウトは最低 600秒** |
| 6 | **AfterFX/aerender の起動がブロックする** | **デタッチ起動 + 出力ファイルのポーリング**。jsx の末尾で必ず `app.quit()` |
| 7 | **モーションブラーが効かない** | `comp.motionBlur = true` **だけでは無効**。動かすレイヤー個別に `layer.motionBlur = true`（数値・アクセントライン・分割線・棒・軸線・SEAMのワイプバー） |
| 8 | **`"ADBE Rotation"` が null を返す** | 2Dレイヤーの回転は **`"ADBE Rotate Z"`** |
| 9 | **レイヤーの outPoint がコンプ末尾に残る** | `inPoint` だけ設定すると尻が残る。**inPoint と outPoint の両方を設定する** |
| 10 | **画像シーケンスの fps が 30 にならない** | 読み込み後に必ず `item.mainSource.conformFrameRate = 30;`。忘れると**全カードの timing が無言でズレる** |
| 11 | 実行パス | `C:\Program Files\Adobe\Adobe After Effects 2026\Support Files\AfterFX.exe` / `aerender.exe`（**実在を確認済み**） |
| 12 | GPU | RTX4090 だが**ソフトウェアレンダで固定**（`proj.gpuAccelType = GpuAccelType.SOFTWARE`）。安定性優先。EP38で実証 |

## 7.8 実行コマンド

```bash
# [1] beats.json と jsx を生成（--dryrun で _dryrun/ 配下に出す）
"C:/Users/aab15/Documents/prime-documentary/.venv/Scripts/python.exe" \
  "C:/Users/aab15/Documents/prime-documentary/scripts/ae/build_lech_hero_jsx.py" [--dryrun]

# [2] AE でビルド＋レンダ（デタッチ起動。マーカーをポーリングする）
"C:/Program Files/Adobe/Adobe After Effects 2026/Support Files/AfterFX.exe" -noui \
  -r "C:/Users/aab15/Documents/prime-documentary/episodes/PD-2026-040-lech/08_edit/ae_hero/lech_hero.jsx"
# → render/_build_ok.txt が出るまで待つ（最大600秒）
# → 続いて render/*.mp4 が23本揃うまで待つ（最大1200秒）

# [3] 本編に焼き込み（v002 は不変・v003_ae を新規作成）
"C:/Users/aab15/Documents/prime-documentary/.venv/Scripts/python.exe" \
  "C:/Users/aab15/Documents/prime-documentary/scripts/ae/composite_lech_hero.py" [--dryrun]
```

## 7.9 `scripts/validate_lech_beats.py`（BLOCKING）

1. `beats[].start` は昇順で、区間同士が**重ならない**
2. すべての `start`/`end` が本編ナレーション区間内（**HOOK 0–8.1 と ENDCARD 732.4–741.4 には絶対に重ねない**）
3. `end <= hookSeconds + OPENING_SEC + narrationSeconds`（= 8.1 + 3.5 + 720.8 = 732.4）
4. `layout` が §7.4 の9種のいずれか。`still` が必要なレイアウトで `still` が null なら FAIL、
   ベクター系（`SIEGE_TIMELINE` / `CASE_TIMELINE` / `HOUSE_PLAN` / `SEAM_TRANSITION`）で `still` が非null なら FAIL
5. `still` が実在し、**長辺 >= 3840px**
6. `top` / `bottom` / `caption` / `footnote` / `act_title` / `doc_lines[]` / `timeline_events[].text` が
   §2.2 の accuracy_lock を通る
7. `facts[fact_id].verified == false` かつ `required == false` → そのカードを出力から**除外**
8. `facts[fact_id].verified == false` かつ `required == true` → **exit 1**（`--dryrun` では警告にして続行）
9. **`lech_film.json` の `figures[]` 17枠と AE の23区間が1秒でも重ならないこと**
10. `dur >= anim_end + 1.20 + tail`（§7.6）
11. `caption` に改行が含まれていない（罠#3）

## 7.10 コンポジタ（`scripts/ae/composite_lech_hero.py`）

`composite_kfc_hero.py` をベースに、**パスと定数のみ差し替える。SKIPロジックは1行も削らない。**

```
BASE = episodes/PD-2026-040-lech/08_edit/lech_final_bgm.v002.mp4
OUT  = episodes/PD-2026-040-lech/08_edit/lech_final_bgm.v003_ae.mp4
FFMPEG   = C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe
FFPROBE  = C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffprobe.exe
W, H, FPS = 1920, 1080, 30
```

**SKIP条件（この4つを必ず実装する。1つでも欠けると作品が壊れる）:**

1. `render/<id>.mp4` が存在しない → SKIP
2. 解像度が `1920x1080` でない → SKIP
3. 実測尺 `< dur - 0.3` → SKIP
4. `beat.end > base_dur` → SKIP

**SKIPされた区間は元のカットのまま残る。作品は壊れない。**
23枚のうち何枚SKIPされたかを stderr に必ず出す。

**ffmpeg 呼び出し（実証済みの形）:**

```
[k:v] setpts=PTS-STARTPTS+<start>/TB, format=yuv420p [bk]
[prev][bk] overlay=0:0:eof_action=pass:enable='between(t,<start>,<end>)' [vk]
-map [vN] -map 0:a -r 30 -c:v libx264 -preset medium -crf 16 -pix_fmt yuv420p -c:a copy
```

> **★23本のオーバーレイを1本のフィルタグラフに積むと ffmpeg のコマンドラインが長くなり、
> メモリも食う。** 23入力なら問題ない範囲だが、**出力後に必ず `probe_dur(OUT)` で
> ベースとの尺の差が 0.5秒以内であることを確認する**（`composite_kfc_hero.py` と同じ検証）。

**出荷済みファイルを絶対に上書きしない。** 出力は必ず `_v003_ae` サフィックス。

---

# 8. ★字幕の切断規則（`scripts/gen_captions_lech.py`）

## 8.1 何が問題か

オーナー指摘: 「字幕がいつも変なところで途切れていた」。**実測で現行全話が14〜32%不正。**

**原因は生成器にある。** `scripts/gen_captions_case.py` の

```python
MAX_WORDS, MAX_CHARS = 7, 42
```

という**純粋に機械的な語数／文字数分割**に構文の認識がない。EP38 の出荷済みSRTでの実害:

```
24  "...ends with a warning and a ride"
25  "home."                                  <- 孤立キュー・句の分断
27  "A child was handed a form giving up the right"
28  "to a lawyer -"                          <- "the right | to a lawyer" が割れた
33  "...taught to trust the adults"
34  "in the room, signed away..."            <- "the adults | in the room" が割れた
```

## 8.2 機械ゲート `scripts/check_caption_breaks.py` が落とす3クラス

```python
MIN_CUE_WORDS = 3            # これ未満は「文として完結」していない限り孤立キュー
TERMINAL_PUNCT = ".?!—-:;"   # キューはここで終わってよい
SOFT_END = TERMINAL_PUNCT + ","
MAX_BAD_SHARE = 0.05         # 全キューの5%まで
```

| クラス | 検出条件 |
|---|---|
| **A. 行末の機能語** | 複数行キューの**最終行以外**が、句読点なしで `NO_DANGLE_END` の語で終わる |
| **B. 孤立キュー** | 語数 < 3 で、かつ「終端句読点で終わる」「大文字で始まる」の**両方**を満たさない |
| **C. 句をまたぐ切断（hard）** | キューが `SOFT_END` 以外で終わり、**次のキューが小文字で始まり**、かつ末尾語が `NO_DANGLE_END` にある |

**`ok` の条件:** A・B・C(hard) が**すべて0件**で、かつ `bad_share <= 0.05`。
（A/B/C が1件でもあれば `bad_share` に関係なく FAIL する。**実質ゼロ許容。**）

## 8.3 `NO_DANGLE_END`（`scripts/fix_caption_dangling.py` の実体。**再定義せず import する**）

```python
from fix_caption_dangling import NO_DANGLE_END
# {"a","an","the","of","to","in","on","at","for","with","from","by","as","into","onto",
#  "over","under","than","up","out","off","about","against","between","through",
#  "and","or","but","nor","so","yet",
#  "is","are","was","were","be","been","being","am","has","have","had","do","does","did",
#  "will","would","can","could","shall","should","may","might","must",
#  "my","your","his","her","its","our","their",
#  "that","this","these","those","who","which","whose","whom",
#  "if","when","because","while","after","before","since","until","unless",
#  "although","though","whether","no","not"}
```

> **絶対に自前で語リストを書き直さない。** ゲートとドリフトした瞬間に「通ったのに直っていない」が起きる。

## 8.4 ★構文境界で切る実装（`gen_captions_lech.py` の中核）

**設計の原則: 文字数は「上限」であって「分割基準」ではない。**

```
[Step 1] 文に割る
    終端句読点 . ? ! — : ; で文を切る。略語（Mr. / U.S. / No.）は切らない例外リストを持つ。

[Step 2] 各文を「構文単位（chunk）」に割る。優先度の高い境界から:
    P1  等位接続（", and" / ", but" / ", so" / ", or" / ", yet" / ", nor"）の **カンマの直後**
    P2  従属接続詞・関係詞の **直前**
        （because / while / when / after / before / since / until / unless / although /
          though / whether / if / that / which / who / whose / whom）
    P3  前置詞句の **直前**（その前置詞句が3語以上のとき）
        （of / to / in / on / at / for / with / from / by / into / over / under /
          against / between / through / about）
    P4  その他のカンマの直後
    P5  不定詞 "to + 動詞" の **直前**

[Step 3] chunk を1キューに割り当てる。ただし
    - 語数 < MIN_CUE_WORDS(3) の chunk は、**必ず隣の chunk に併合する**
      （直前が同じ文なら前へ、そうでなければ後ろへ）
    - 併合しても語数が 3 未満なら、さらに隣へ併合する
      ★これで「"home." が単独キュー」が構造的に発生しなくなる

[Step 4] 上限を超える chunk だけをさらに割る
    語数 > 7 または 文字数 > 42 のとき:
      - Step 2 の P1..P5 で「その chunk の内部にある最も優先度の高い境界」を探して割る
      - 内部に境界が1つも無ければ、**末尾語が NO_DANGLE_END に無い位置**のうち
        中央に最も近いところで割る
      - どこで割っても末尾が NO_DANGLE_END になるなら **割らない**
        （42文字を超えることを許容する。★機能語で切るより長いほうがマシ）

[Step 5] 2行への折り返し（wrap）
    1キューが42文字を超えるときのみ2行にする。
    折り返し位置は fix_caption_dangling.wrap() と同じ規則:
      - 各行 <=50文字
      - **1行目が NO_DANGLE_END の語で終わってはならない**
      - 句読点の直後を優先する
    条件を満たす分割点が無ければ **1行のまま**にする（3行にはしない）

[Step 6] タイミング
    faster-whisper の語タイムスタンプ（word_timestamps=True）を使い、
    キューの開始 = 最初の語の start / 終了 = 最後の語の end。
    - CPS <= 27 を満たすまでキューを後ろに伸ばす（次のキュー開始 - 0.03秒 が上限）
    - 最小表示時間 0.90秒
    - **ここで語数を再調整してはならない**（Step 4 で決めた境界を時間の都合で動かさない）
```

## 8.5 セルフテスト（**実装したら必ず走らせる**）

`gen_captions_lech.py --selftest` を実装し、次の入力で**期待どおりに切れることを確認する**
（EP38 の実害をそのまま回帰テストにする）:

| 入力 | 期待 |
|---|---|
| `"...ends with a warning and a ride home."` | `"home."` が単独キューにならない（Step 3で併合） |
| `"A child was handed a form giving up the right to a lawyer."` | `"the right"` / `"to a lawyer"` に割れない（P3で `to a lawyer` の直前が境界になるが、`the right` が3語未満なら併合される） |
| `"...taught to trust the adults in the room, signed away..."` | `"the adults"` / `"in the room"` に割れない |
| 単語1つの文（`"Nothing."`） | 前のキューに併合される |

**出力を `check_caption_breaks.py` に食わせて exit 0 になることまで自動で確認する。**

## 8.6 実行

```bash
py -3.11 scripts/gen_captions_lech.py --ep PD-2026-040-lech
#   出力: episodes/PD-2026-040-lech/08_edit/captions.final.v001.srt

./.venv/Scripts/python.exe scripts/check_caption_breaks.py \
  episodes/PD-2026-040-lech/08_edit/captions.final.v001.srt
#   → PASS が出るまで直す。ゲート側の閾値を緩めるのは禁止。
```

**台本未確定時:** スロットのマーカー文字列は英文ではないので構文分割ができない。
**ドライランではダミーの英文段落**（`lorem`ではなく、実際の英語の文章。
たとえば `acts[].narration` のマーカーを「文法的に正しい placeholder 英文」にする）を使い、
**分割器が動くことを実証する**。

---

# 9. OP バンパー `OpeningLech`（Remotion）

## 9.1 【重要】二重OPを作らない

`docs/PD_ONE_PASS_PRODUCTION_SPEC.v2.md` row14 は
「本編内のOP/EDの正典は `remotion/src/components/Bookends.tsx`（`BrandOpening` / `OPENING_SEC=3.5`）」と定め、
フォークを禁止している（invariant 14）。

**したがって:**

- **本編（`Ep40Lech`）のOPは `BrandOpening` のまま。変更しない。**（`op_ed_bookends` ゲートを通すため）
- 本節の `OpeningLech` は**独立したタイトルバンパー成果物**（`out/lech_opening.mp4`）。
  用途は (a) 品質ルールを満たす再利用可能部品、(b) Shorts / 予告 / SNS 用の頭
- **`OpeningLech` を本編に ffmpeg で焼き込んではならない**（オーナー承認なしに row14 の見え方を変えない）

## 9.2 Composition 設定

| 項目 | 値 |
|---|---|
| `id` | **`OpeningLech`** |
| 解像度 | **1920 × 1080** |
| `fps` | **60** |
| `durationInFrames` | **180**（= 3.0秒 @60fps） |
| component | `OpeningLech`（`remotion/src/compositions/OpeningLech.tsx`） |

```tsx
import {OpeningLech, openingLechDurationInFrames} from './compositions/OpeningLech';
import lechOpeningProps from '../props/lech.json';

<Composition
  id="OpeningLech"
  component={OpeningLech}
  width={1920}
  height={1080}
  fps={60}
  durationInFrames={openingLechDurationInFrames(60)}
  defaultProps={lechOpeningProps}
/>
```

**依存パッケージ:** `@remotion/motion-blur`。
**確認済み:** `remotion/package.json` に `"@remotion/motion-blur": "^4.0.476"` が既に存在し、
`node_modules/@remotion/motion-blur` も実在する。**未導入時のみ** `cd remotion && npm i @remotion/motion-blur`。

**`remotion/remotion.config.ts`:** 既に下記の正典値。**一致していることを確認するだけでよく、書き換えてはならない。**

```ts
Config.setVideoImageFormat('png');            // 中間フレームはロスレスPNG
Config.setCodec('h264');                      // H.264 / libx264（CPU）
Config.setCrf(16);                            // CRF 16
Config.setX264Preset('slow');
Config.setPixelFormat('yuv420p');
Config.setColorSpace('bt709');
Config.setAudioCodec('aac');
Config.setAudioBitrate('320k');
Config.setConcurrency(os.cpus().length);      // 全CPUコア = 最大並列
Config.setChromiumOpenGlRenderer('angle');
Config.setOverwriteOutput(true);
```

## 9.3 秒数ベースのタイムライン（全区間）

**fps = 60。フレームは全て `Math.round(fps * 秒)` で算出する。コード内にフレーム数を直書きしてはならない。**

| 秒 | フレーム | 起きること |
|---|---|---|
| **0.00–0.10** | f0–f6 | 画面は `#0d0b08`。**L1** グラデ背景の opacity が 0→1（0.40秒）、同時に scale 1.08 が180フレームかけて 1.00 へ（`Easing.out(Easing.cubic)`）。**opacity 単独ではなく scale と併用** |
| **0.10–0.15** | f6–f9 | **ロゴ**（`hasLogo` が true のとき）が左上 `top:64 / left:72` に spring で出現。scale 0.4→1.0・opacity 0→1（**併用**） |
| **0.15–0.25** | f9–f15 | **L2** グリッドが spring（`damping:200, mass:1`, `durationInFrames = round(fps*0.8) = 48`）で reveal。最終 opacity = `gridReveal * 0.18`。同時にグリッド全体が180フレームで `translateY 0→48px`（`Easing.inOut(Easing.sin)`）でドリフト |
| **0.25–0.30** | f15–f18 | **L3** グローが spring（`damping:18, mass:1.2`）で立ち上がる。scale 0.6→1.15 / opacity 0→0.85（**併用**）。サイズ `width*0.62 × height*0.36`、`filter: blur(28px)` |
| **0.30–0.86** | f18–f52 | **L4 主役タイトル**が1文字ずつ切れ上がる。各文字 spring（`damping:16, mass:1`）で `translateY 110% → 0`、`opacity` は `interpolate(springVal, [0,0.25], [0,1])` clamp。**スタッガー = `Math.max(1, round(fps*0.04)) = 2フレーム/文字**。`title="LECH"`（4文字）なら最終文字の開始は f18+3×2 = **f24**、収束は約 f52。全体を `Trail`（`layers=6, lagInFrames=1.2, trailOpacity=0.45`）で包む |
| **0.55–1.15** | f33–f69 | **L2b フラクチャーライン**。画面中央からタイトル背後を横切る細い亀裂状の線が `scaleX 0→1` + `opacity 0→0.55`（spring `damping:22, mass:1.1`、`transformOrigin:'center'`）。**破壊のモチーフ** |
| **0.95–1.35** | f57–f81 | **L5a** アクセント下線が左から `scaleX 0→1`（spring `damping:16, mass:0.8`、`transformOrigin:'left center'`）。幅240px・高さ6px・`boxShadow: 0 0 24px ${accent}aa` |
| **1.10–1.55** | f66–f93 | **L5b** サブタイトルが `translateY 24px→0` + `opacity 0→1`（spring `damping:20, mass:1`・**併用**） |
| **1.55–2.20** | f93–f132 | 全要素が settle。背景 scale は依然 1.02 付近を緩やかに進行中。グリッドのドリフトも継続。**完全な静止フレームが1枚も無いこと** |
| **2.20–3.00** | f132–f180 | ホールド。背景 scale が 1.00 に着地、グリッド translateY が 48px に着地。**フェードアウトはしない** |

## 9.4 タイミング定数（**フレーム直書き禁止**）

```ts
const T = {
  bgIn:        0.00,
  logoIn:      0.10,
  gridIn:      0.15,
  glowIn:      0.25,
  titleIn:     0.30,
  charStagger: 0.04,  // 60fps で 2フレーム
  fractureIn:  0.55,
  accentIn:    0.95,
  subIn:       1.10,
} as const;

const sec = (fps: number, s: number) => Math.round(fps * s);
export const openingLechDurationInFrames = (fps: number) => Math.round(fps * 3.0);  // = 180 @60fps
```

| 要素 | 開始 | 終了 | 手法 | 移動量 | パラメータ |
|---|---|---|---|---|---|
| 背景 scale | f0 | f180 | `interpolate` | **1.08 → 1.00** | `Easing.out(Easing.cubic)`・両端 clamp |
| 背景 opacity | f0 | f24 | `interpolate` | 0 → 1 | clamp（**scale と併用**） |
| グリッド translateY | f0 | f180 | `interpolate` | **0 → 48px** | `Easing.inOut(Easing.sin)` |
| グリッド reveal | f9 | f57 | `spring` | opacity 0 → **0.18** | `damping:200, mass:1`, `durationInFrames: sec(fps, 0.8)` |
| グロー scale | f15 | — | `spring` | **0.6 → 1.15** | `damping:18, mass:1.2` |
| グロー opacity | f15 | — | 同 spring | 0 → **0.85** | （**scale と併用**） |
| タイトル各文字 translateY | f18 + i×2 | — | `spring` | **110% → 0** | `damping:16, mass:1` |
| タイトル各文字 opacity | 同上 | — | `interpolate(springVal,[0,0.25],[0,1])` | 0 → 1 | clamp（**translateY と併用**） |
| タイトル Trail | 全域 | — | `@remotion/motion-blur` `Trail` | — | `layers={6} lagInFrames={1.2} trailOpacity={0.45}` |
| フラクチャー scaleX | f33 | — | `spring` | **0 → 1** | `damping:22, mass:1.1`・`transformOrigin:'center'` |
| フラクチャー opacity | f33 | — | 同 spring | 0 → **0.55** | （**scaleX と併用**） |
| アクセント下線 scaleX | f57 | — | `spring` | **0 → 1** | `damping:16, mass:0.8`・`transformOrigin:'left center'` |
| サブタイトル translateY | f66 | — | `spring` | **24px → 0** | `damping:20, mass:1` |
| サブタイトル opacity | f66 | — | 同 spring | 0 → 1 | （**translateY と併用**） |
| ロゴ scale | f6 | — | `spring` | **0.4 → 1.0** | `damping:14, mass:0.9` |
| ロゴ opacity | f6 | — | 同 spring | 0 → 1 | （**scale と併用**） |

> **等速線形は1箇所も使わない。** すべて `spring` か `Easing.out(Easing.cubic)` / `Easing.inOut(Easing.sin)`。
> **opacity 単独の演出は1箇所も無い。** 全ての opacity が translateY / scale / scaleX と対になっている。

## 9.5 レイヤー構成（下 → 上）

| L | 名前 | EP40 の値 |
|---|---|---|
| **L0** | ルート背景 | `backgroundColor: '#0d0b08'`（暖色寄りの黒。EP39 の `#05070d` 系と分離） |
| **L1** | グラデ背景 | `radial-gradient(120% 120% at 50% 35%, #3a2f1c 0%, #1c1710 45%, #0d0b08 100%)` |
| **L2** | グリッド/ライン | `repeating-linear-gradient(0deg / 90deg, ${accent}22 0px 1px, transparent 1px 64px)`、`maskImage: radial-gradient(120% 90% at 50% 45%, black 35%, transparent 80%)` |
| **L2b** | フラクチャーライン | 幅 `width*0.78` / 高さ 3px / `background: linear-gradient(90deg, transparent 0%, ${accent}00 8%, ${accent}cc 34%, ${accent}55 52%, ${accent}cc 71%, ${accent}00 92%, transparent 100%)` / `transform: translateY(-6px) scaleX(...)` |
| **L3** | グロー | `width*0.62 × height*0.36`、`radial-gradient(closest-side, ${accent}88 0%, ${accent}22 45%, transparent 75%)`、`filter: blur(28px)` |
| **L4** | 主役タイトル | `fontFamily: 'Inter, system-ui, sans-serif'` / `fontWeight: 800` / **`fontSize: 150`** / `letterSpacing: -2` / `color: '#ffffff'` / `lineHeight: 1.05` / 外側 `transform: translateY(-70px)` / 各 span に `paddingBottom: '0.12em'` |
| **L5** | アクセント下線 + サブタイトル | 縦並び（`flexDirection:'column'`, `gap:18`）、`transform: translateY(55px)`。下線 240×6・`borderRadius:3`。サブタイトル `fontWeight:500` / `fontSize:38` / `letterSpacing:6` / `textTransform:'uppercase'` / `color:'#c8d2e6'` |
| **L6** | ロゴ（`hasLogo` 時のみ） | `top:64 / left:72 / 84×84 / borderRadius:20`、`background: linear-gradient(135deg, ${accent}, #ffffff22)`、`border: 2px solid ${accent}`、`boxShadow: 0 0 30px ${accent}66` |

> **主役（L4）の裏に最低3レイヤー**という要件: L1 / L2 / L2b / L3 = **4レイヤー**で満たす。

**テキストのマスク切れ上がり（基本形。必ずこの構造）:**

```tsx
<span style={{display:'inline-block', overflow:'hidden', paddingBottom:'0.12em'}}>
  <span style={{display:'inline-block', transform:`translateY(${y}%)`, opacity:charOpacity, whiteSpace:'pre'}}>
    {ch}
  </span>
</span>
```

## 9.6 props 定義と型

```ts
export type OpeningLechProps = {
  title: string;      // 主役タイトル。1文字ずつスタッガー。推奨 3–8文字（fontSize 150 前提）
  subtitle: string;   // サブタイトル。UPPERCASE 表示（CSSで変換）
  accent: string;     // アクセントカラー（HEX 6桁・"#" 込み）
  hasLogo: boolean;   // true のとき左上にロゴバッジ
};
```

**`remotion/props/lech.json`:**

```json
{ "title": "LECH", "subtitle": "POLICE POWER", "accent": "#E5B53A", "hasLogo": true }
```

> `accent` の `#E5B53A` は **EP40専用**（gold/amber）。**EP39 は `#1F6BFF`。`props/` でファイルを分けるので衝突しない。**
> `subtitle` に入れる文字列も **§2.2 の accuracy_lock 検査対象**（`remotion/props/lech*.json` を対象パスに含める）。

## 9.7 確認と量産

```bash
cd C:\Users\aab15\Documents\prime-documentary\remotion
npm run studio
#   → composition OpeningLech を選び、0→180フレームをスクラブして
#     §9.3 の各時刻に指定の動きが起きていることを目視確認する

npx remotion render OpeningLech out/lech_opening.mp4  --props=./props/lech.json
npx remotion render OpeningLech out/lech_short_op.mp4 --props=./props/lech_short.json
npx remotion render OpeningLech out/lech_teaser.mp4   --props=./props/lech_teaser.json
```

`remotion/props/lech_short.json`:

```json
{ "title": "LECH", "subtitle": "THE TENTH CIRCUIT", "accent": "#E5B53A", "hasLogo": false }
```

---

# 10. サムネイル3案（CTR 2.31% → 目標 4%）

**共通要件:**

- Remotion `<Still>` で **1280×720** レンダ。`remotion/src/compositions/LechThumbnails.tsx` に3案を実装
- Root.tsx に `Thumb-lech-01` / `Thumb-lech-02` / `Thumb-lech-03` として3つ登録
- **見出しは全て大文字・4語以内**・320px で判読可能
- **実在人物の肖像は使わない**
- **「最高裁 / Supreme Court / SCOTUS」を書かない**（§2.2 R1）
- `thumbnail_visibility` ゲート（selected の luma 平均 ≥ 33 + コントラスト下限）を通す
  → **EP40は昼のシーンなので luma は余裕がある。むしろ白飛びに注意し、ハイライトを 245 以下に抑える**
- 背景画像は `stills[role="thumb"]` から取る

## T1 — 「穴の空いた家」（最推奨・情報量最小）

| 項目 | 内容 |
|---|---|
| 主被写体 | 郊外の一軒家の**壁に開いた巨大な穴**を、家の全体が入る引きで。穴の中は暗く、周囲は白飛び寸前の昼光 |
| 構図 | 家は**画面の右60%**。左40%に文字。穴が画面のほぼ中心 |
| 文字 | **`YOUR HOUSE. THEIR CALL.`**（4語） |
| 文字スタイル | Anton・白 `#F5F7FA`・下端に `#E5B53A` の太い下線。文字高 = 画面高の19% |
| 狙い | 「家に穴」という説明不要の異常。二人称の "YOUR" で自分事化 |

## T2 — 「額の対比」（数字勝負）

| 項目 | 内容 |
|---|---|
| 主被写体 | 崩れた家を背景に暗く落とし、前面に**2つの数字**（左＝万引きの被害額 / 右＝家の損害額） |
| 構図 | 左右分割。中央に細い金の縦線。右の数字が左の**2.2倍の文字高** |
| 文字 | **`STOLEN vs DESTROYED`**（3語） |
| 数字 | F02 と F03 の**検証済み値**。**未検証ならこの案は使用しない**（T1/T3 から選ぶ） |
| 色 | 背景を輝度25%まで落とし、数字を白 + 右だけ金。**最も明るい点が数字**になるようにする |

## T3 — 「請求書ゼロ」（怒りのトリガー）

| 項目 | 内容 |
|---|---|
| 主被写体 | 瓦礫の上に置かれた**1枚の紙**（文字は判読不能）。紙の上にだけ強い日光、周囲は影 |
| 構図 | 紙は画面下1/3・中央。上2/3に破壊された家のシルエットと空 |
| 文字 | **`THEY PAID NOTHING`**（3語）。`NOTHING` だけ `#E5B53A` の金 |

**A/Bタイトル候補（`title_candidates` に入れる。60字以内・二人称必須）:**

- **A:** `Police Destroyed Their House. Nobody Paid For It.`（50字）
- **B:** `Can Police Destroy Your Home And Pay You Nothing?`（49字）

**ED の確定文言（`ed` スロットに入れる）:**

```
payoff_line   = "The family did nothing wrong. A stranger chose their house.
                 And when it was over, the law said the loss was theirs to carry."
cta_line      = "If this changed how you think about who pays when the state breaks something
                 — hit like. That's how these cases find people."
question_line = "So here's the question we want you to answer:
                 if it were your house, who should pay — the city, or you?"
```

`question_line` の必須条件: **二択にする / "your house" と言う / 問いは1つだけ /
CTAより後・エンドカードより前に置く / 画面には中央〜上部のテロップゾーンに焼く**（下部の字幕帯と分離）。

**固定コメント** `episodes/PD-2026-040-lech/09_package/pinned_comment.v001.txt`:

```
Two things this case turns on, and neither is obvious:
(1) The Tenth Circuit held this was an exercise of police power, not a taking —
    so the Takings Clause never kicks in.
(2) The Supreme Court declined to hear the appeal in 2020.
    That is not agreement; it just means the ruling stands.

If it were your house — should the city pay, or should you?
```

> この文面も §2.2 の accuracy_lock 検査対象（`09_package/*.txt` を対象パスに含める）。
> **(2) は R2 の `declined to hear` を含むので通る。** 書き換えるな。

---

# 11. Remotion 本編コンポジションの登録

`remotion/src/Root.tsx` に追記する（既存の `Ep38KidsForCash` の形をそのまま踏襲する）:

```tsx
import lechFilm from './data/lech_film.json';

<Composition
  id="Ep40Lech"
  component={CaseFilm}
  durationInFrames={caseFilmDurationInFrames(lechFilm as unknown as FilmData, BRAND.video.fps)}
  fps={BRAND.video.fps}
  width={BRAND.video.width}
  height={BRAND.video.height}
  defaultProps={{
    data: lechFilm as unknown as FilmData,
    seriesLabel: 'PRIME DOCUMENTARY',
    title: 'They Destroyed Their House',
    subtitle: 'A stranger ran inside. The family paid for it.',
  }}
/>
```

> **確認済み: `remotion/src` に `lech` / `frazier` の文字列は現在1件も存在しない。** 衝突しない。
> **`subtitle` も accuracy_lock 検査対象。** 「最高裁」を含めない。

---

# 12. 絶対にやらないこと

- **EP39（frazier）のファイルに一切触らない。** 読み取りのみ可。レーンも分離する。
  - EP39 = 取調室 / 夜 / 密室 / electric blue `#1F6BFF`
  - EP40 = 郊外の一軒家 / 昼 / 破壊 / gold-amber `#E5B53A`
- **スレッドAの所有ファイル（§0.2.1）に書かない。** 特に `05_visuals/` `05_stock/` `remotion/public/lech/` `H:\pd-media\assets\ai\lech\`。
- **`scripts/gen_captions_case.py` を改変しない**（他エピソードが使っている）。EP40用に新規作成する。
- **課金ジョブを起動しない。** ElevenLabs TTS / 課金画像生成API / YouTubeアップロード。
- **公開済み・出荷済みの mp4 を上書き・再レンダリングしない。** 出力は必ず `_v003_ae`。
- **「最高裁が判断した」という趣旨の記述をどこにも書かない**（§2）。
- **設計書に無い数値を自分で決めない。** 不明な数値は `facts[F-ID].verified = false` として扱い、
  該当カードを除外する。
- **尺・語数・素材点数・AEカードの区間を「だいたいこのくらい」で決めない。**
  §4.3 / §5.2 / §7.2 の検算をそのまま使う。自分で計算し直して合わなければ、
  実装ではなく**本書の側を疑って報告する**。
- **`FigureSpec` の `kind` を推測で書かない。** §6.2 の実在する文字列だけを使う。
- **スタブと本番でコードパスを分岐させない**（§0.2）。

---

# 13. 受入（自分で走らせて exit 0 を確認してから完了報告すること）

```bash
cd C:\Users\aab15\Documents\prime-documentary

# 0. ★語数ゲート（最優先。TTSとレンダーに課金する前にここで落とす）
./.venv/Scripts/python.exe scripts/check_script_length.py \
  episodes/PD-2026-040-lech/03_script/script.en.v003.md --json

# 1. 水増しゲート（★--ep には完全なエピソードフォルダ名を渡す。短いslugは不可）
./.venv/Scripts/python.exe scripts/check_padding.py --ep PD-2026-040-lech --json

# 2. 事実性ゲート（EP40固有）
./.venv/Scripts/python.exe scripts/check_lech_accuracy.py --json

# 3. 契約バリデータ（内部で 0 と 2 を再実行する）
./.venv/Scripts/python.exe scripts/validate_lech_slots.py
./.venv/Scripts/python.exe scripts/validate_lech_beats.py
./.venv/Scripts/python.exe scripts/check_lech_asset_manifest.py \
  --assets episodes/PD-2026-040-lech/05_visuals/asset_manifest.v001.json

# 4. 素材反復・字幕
./.venv/Scripts/python.exe scripts/check_asset_reuse.py remotion/src/data/lech_film.json
./.venv/Scripts/python.exe scripts/check_caption_breaks.py \
  episodes/PD-2026-040-lech/08_edit/captions.final.v001.srt

# 5. レンダ前プリフライト
#    （checks 配列の順: script_length → motion_budget → assets_exist → coverage →
#      film_crosscheck → premium_motion(motion_density) → animation_mix →
#      asset_reuse → caption_integrity → caption_breaks → visual_asset_qc）
./.venv/Scripts/python.exe scripts/preflight_render_gate.py --ep PD-2026-040-lech

# 6. 本編の最終受入（episode番号は★位置引数。--ep ではない）
./.venv/Scripts/python.exe scripts/check_final_acceptance.py 40 \
  --render episodes/PD-2026-040-lech/08_edit/lech_final_bgm.v003_ae.mp4 --emit-receipt
```

**全て exit 0 でなければ `package_ready` にしない。自己申告のQCは無効。**

| ゲート | EP40 での目標値 |
|---|---|
| **`check_script_length`（★最優先）** | 総語数 **2,048–2,226**（目標2,140）／`wpm_assumed` 178.1 |
| **`check_padding`** | dead air / 言い換え反復の violation = 0。**幕内部に2秒超の間を作らない** |
| **`check_asset_reuse`** | factory ≤1回 / motion ≤2回 / still ≤2回 / first-use share **≥0.70**（設計値 **0.7566**） |
| **`check_caption_breaks`** | 行末機能語 0 / 孤立キュー 0 / hard split 0 |
| `runtime_band` | 11.5–12.5分。設計値 **741.4秒 = 12:21** |
| **MGビート密度**（`check_motion_density.MIN_KINETIC_BEATS_PER_MIN = 2.5`） | 設計値 **40枠 / 3.24per分 / 16種** |
| `animation_mix` | `MAX_STILL_SHARE = 0.45` → 設計値 **34.6%**／`LONG_HOLD_SECONDS=5.0` の長止め ≤8箇所 |
| **factory クリップ** | ≥25本 → 設計値 **85本** |
| `image_resolution` | 全使用静止画 長辺 **≥3840px** |
| `caption_narration_match` | ≥99% |
| `thumbnail_present` / `thumbnail_visibility` | 3案 @1280×720 + selected・luma平均 ≥33 |
| `op_ed_bookends` | `BrandOpening` / `BrandEndcard` を import（フォークしない） |
| `structure_4part` | hook / opening / body / ending が順に存在 |
| loudness | -16〜-12 LUFS |
| **`accuracy_lock`（EP40固有）** | **violations = 0** |

**「動いたと思う」は完了ではない。ゲートが exit 0 を返して初めて完了。**
**自分でQC基準を書き換えて通すことは禁止。**
