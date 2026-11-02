# EP41 thompson — Codex スレッドA「素材生成」引き継ぎプロンプト v001

> **このファイルは単体で完結している。他のファイルを読まなくても着手できる。**
> 設計書 `EP41_thompson_DESIGN_and_CODEX_PROMPTS.v001.md` も、実装スレッドBのファイルも**読まなくてよい**（必要な数値はすべて本書に転記済み）。
> **唯一の外部真実 = `episodes/_planning/EP41_thompson_PRODUCTION_SPEC.v001.json`**（機械生成）。本書の数値はそこから転記したものであり、手書きで発明していない。

```
あなたは Prime Documentary（YouTubeドキュメンタリーチャンネル）の制作エンジニアです。
リポジトリ: C:\Users\aab15\Documents\prime-documentary
Python:     C:\Users\aab15\Documents\prime-documentary\.venv\Scripts\python.exe
メディア:   H:\pd-media
担当:       EP41 / Episode ID: PD-2026-041-thompson / slug: thompson
```

---

# 0. このスレッド（A）の責務・境界・完了条件

## 0.1 責務（GPU律速・目視律速の長時間ジョブ）

本編で使う「絵」を全部そろえ、1本のマニフェストに書き出すところまで。

| # | 作業 | 成果物 | 目安 |
|---|---|---|---|
| A-1 | SDXL静止画のバッチ生成（**36シーン × 3バリエーション = 108枚**） | `H:\pd-media\assets\ai\thompson\S<NN>[_VV].png` | 2.5–4時間（GPU） |
| A-2 | 静止画のQCと役割別選抜（**目視必須**） | `05_visuals/still_qc.v001.json` + コンタクトシート | 1.5時間 |
| A-3 | depth map 生成（`treatment:"depth"` の必須入力） | `H:\pd-media\assets\ai\thompson\S<NN>[_VV]_depth.png` | 20分 |
| A-4 | factory 実写クリップ **88本**の選定と**全点目視QC** | `05_stock/factory_selection.v001.json` / `05_visuals/factory_clip_qc.v001.json` | **2時間（うち目視だけで1時間以上）** |
| A-5 | i2v モーション化 **15本**（Wan 2.2 A14B → RIFE 48fps） | `H:\pd-media\assets\ai_video\thompson\M<NN>_rife.mp4` | 6.5–18時間（GPU） |
| A-6 | 合成レイヤー（particle/light/vfx）の選定 | `05_stock/overlay_selection.v001.json` | 30分 |
| A-7 | 権利台帳と**境界契約マニフェスト**の出力 | `05_stock/stock_ledger.v001.json` / **`05_visuals/asset_manifest.v001.json`** | 20分 |
| A-8 | Remotion public への staging | `remotion/public/thompson/{img,factory,motion,overlay}/` | 30分 |

## 0.2 スレッドB（実装）との境界＝接続点はただ1ファイル

```
episodes/PD-2026-041-thompson/05_visuals/asset_manifest.v001.json
   ↑ Aが生成（唯一の生産者）        ↓ Bが消費（唯一の消費者）
```

**Bはこのファイル以外のAの中間生成物を読まない。Aはこのファイル以外のBの成果物に依存しない。** Bはスタブで全パイプラインを完走できるので、Aの完了を待っていない。**A も急がなくてよいが途中経過を壊すな。**

### ファイル所有権（破ると並行作業が壊れる）

| パス | 所有 | Aの権限 |
|---|---|---|
| `H:\pd-media\assets\ai\thompson\**` / `H:\pd-media\assets\ai_video\thompson\**` | **A** | 読み書き |
| `episodes/PD-2026-041-thompson/05_visuals/**` / `05_stock/**` | **A** | 読み書き（`mkdir(parents=True, exist_ok=True)` で自作） |
| `remotion/public/thompson/{img,factory,motion,overlay}/**` | **A** | 読み書き |
| `episodes/PD-2026-041-thompson/manifest.json` `03_script/**` `04_scenes/**` `08_edit/**` `09_package/**` | **B** | **触るな** |
| `remotion/src/**` `remotion/props/**` `scripts/ae/**` | **B** | **触るな** |
| `episodes/PD-2026-039-*/**` `episodes/PD-2026-040-*/**` および EP39/EP40 の素材 | 別エージェント | **絶対に触るな。読み取りのみ可** |

## 0.3 A が使う／作るスクリプト

**★既存スクリプトをそのまま使う（新規に作らない）:**

| パス | 役割 | 引数 |
|---|---|---|
| `scripts/generate_sdxl_4k.py`（**既存**） | §5 の SDXL 生成（`04_scenes/ai_prompts.v001.md` を `read_prompts()` で読む） | `PD-2026-041-thompson --variants 3` / `41 --variants 3 --only S07` |
| `scripts/gen_depth_maps.py`（**既存**） | §6.4 の depth map | `--dir "H:/pd-media/assets/ai/thompson"` |
| `scripts/build_footage_contact_sheet.py`（**既存**） | §7 の factory 全点目視コンタクトシート | `--ep PD-2026-041-thompson --media video --dir <staging>` |
| `scripts/select_factory_assets.py`（**既存**） | §7 の factory 候補出し | `--kind video --query <kw> --limit 90 --exclude-used --ep PD-2026-041-thompson --json` |

**★Aが新規作成するスクリプト（これ以外を新規に作らない）:**

| パス | 役割 | 下敷き |
|---|---|---|
| `scripts/qc_thompson_stills.py` | §6 の静止画QC＋役割別選抜（機械QC＋解像度チェック） | — |
| `scripts/select_thompson_factory.py` | §7 の factory 88本の確定選定・EP39/EP40 sha256 除外検証 | — |
| `scripts/comfy_wan_thompson.py` | §8 の i2v 15本（Wan 2.2 A14B ドライバ・**パスと SHOTS だけ差し替え**） | `scripts/comfy_wan_kidsforcash.py` |
| `scripts/rife_thompson.py` | §8.4 の RIFE 4x → 48fps | `scripts/rife_kidsforcash.py` |
| `scripts/build_thompson_asset_manifest.py` | §4 の境界契約マニフェストを出力・自己検証 | — |
| `scripts/stage_thompson_assets.py` | §10 の staging | — |

> **SDXL 生成スクリプトを新規に作らない。** `generate_sdxl_4k.py` が既にある（`read_prompts()` で `04_scenes/ai_prompts.v001.md` を読む）。あなたは **`ai_prompts.v001.md` を §5.9 の2行形式で書く**だけ。

## 0.4 完了条件（すべて緑で完了。1つでも赤なら未完了）

```bash
cd C:\Users\aab15\Documents\prime-documentary

# [A-DONE-1] 境界契約マニフェストが自己検証を通る
./.venv/Scripts/python.exe scripts/build_thompson_asset_manifest.py --verify
#   → exit 0。counts が §3.4 の確定値以上。全パス実在。sha256 重複ゼロ。

# [A-DONE-2] 反復禁止ゲートが素材点数の観点で通る
./.venv/Scripts/python.exe scripts/build_thompson_asset_manifest.py --reuse-feasibility
#   → still >=80 / motion >=15 / factory >=88 / distinct 合計 >=183 / first-use >=0.70

# [A-DONE-3] 静止画の解像度ゲート（長辺 >=3840）
./.venv/Scripts/python.exe scripts/qc_thompson_stills.py --check-resolution

# [A-DONE-4] factory の視覚QCゲート（★全88本を目で見た記録があること）
./.venv/Scripts/python.exe scripts/check_visual_asset_qc.py --ep PD-2026-041-thompson
#   → exit 0（factory_clip_qc.v001.json が staging 済み全クリップを reviewed:true で網羅）

# [A-DONE-5] EP39/EP40 との素材被りゼロ
./.venv/Scripts/python.exe scripts/select_thompson_factory.py --verify-no-prior-overlap
#   → 重複 sha256 = 0（EP39 と EP40 の両方に対して）
```

---

# 1. ★★★ 最優先の絶対条件（R1）★★★

**Connick v. Thompson は最高裁判決（5–4 reversal）。だが本作の絵は「実在人物の顔を一切出さない」。**

## 1.1 Aが書く全文字列にかかる R1 禁止

対象: SDXL プロンプト本文（`ai_prompts.v001.md` / メタJSON）/ `asset_manifest.v001.json` の `tags[]`・`eyeballed_content`・`caption_hint` / `*_qc.v001.json` の全文字列 / `stock_ledger.v001.json` の `notes` / ファイル名。

1. **実在の Thompson・Deegan・Connick・Riehlmann・Liuzza・判事（Thomas/Scalia/Ginsburg 等）の肖像・likeness を作らない。** 人物は必ず後ろ姿・シルエット・顔外し・手元のみ。
2. **実在の住所・番地・判決文・書類の可読文字を再現しない。** 書類は雰囲気のみ（判読不能）。血液型 B/O・$14M・5–4 等の**数値は画像に描かない**（AE/figures のタイポで出す＝B の担当）。
3. **裸の身体検査・流血・遺体を描かない。** 血の布は非グラフィックの象徴に限る。
4. AI画像は概要欄でAI生成を開示 → マニフェストの `ai_disclosure_required: true` を全静止画に立てる。

## 1.2 機械ゲート（`build_thompson_asset_manifest.py --verify` の内部）

A が書いた全JSONの全文字列値に対し、1件でもヒットで exit 1:

```python
import re
BANNED_PORTRAIT = re.compile(
    r"\bportrait\b|\bmugshot\b|likeness of|face of (john|deegan|connick|thomas|scalia|ginsburg)|"
    r"recognizable (real )?person|identifiable face|深偽|ディープフェイク", re.IGNORECASE)
```

> プロンプトで裁判所を出したいときは `a supreme courtroom interior`（§5.9 S30）のように**具体的な実在人物名を書かない**。

---

# 2. 台本の語数と尺の確定値（SPEC から転記・Aが素材点数を積算する根拠）

**★唯一の真実 = `episodes/_planning/EP41_thompson_PRODUCTION_SPEC.v001.json`。** 古い資料の wpm・語数は使うな。

```
words_total          = 2,026
narration_seconds    = 682.5   （= 11.4分）
wpm_used             = 178.1
総尺（設計）          = 695.0秒 = 11:35（narration 682.5 + BrandOpening 3.5 + BrandEndcard 9.0）
```

**Aにとっての意味は1つ:** > **214カット / distinct 183 / 初出85.5% = still 80 + factory 88 + motion 15。**（§3 で積算）

---

# 3. ★素材構成の確定値（SPEC の distinct/cuts をそのまま調達する）

## 3.1 SPEC の内訳（★この値で調達する・勝手に変えない）

| 種別 | distinct | 担当カット | 使用回数(cap) | 調達方法 |
|---|---|---|---|---|
| **SDXL静止画（本編 body）** | **80枚** | 96カット | 1.2回(≤2) | **この作品にしか無い絵だけ**（§3.5） |
| **factory 実写クリップ** | **88本** | 88カット | **各1回(1)** | 在庫 **11,443本**から選抜（§7） |
| **i2v モーション** | **15本** | 30カット | 各2回(≤2) | 上のSDXLから動きが意味を持つものを選抜（§8） |
| **合計（カットに出る素材）** | **183点** | **214カット** | | |
| 合成レイヤー（particle/light/vfx） | 10–16本 | — | 重ね掛け | **distinct 素材に数えない**（§9） |

**SDXL の追加枠（本編カットに出ない分）:**

| 用途 | 点数 |
|---|---|
| i2v の元画像（`role:"i2v_source"`・body と別 asset） | **15枚** |
| サムネ／予備（`role:"thumb"`） | **6枚** |
| **SDXL accepted 合計** | **80 + 15 + 6 = 101枚** |
| **SDXL 生成バッチ** | **36シーン × 3バリエーション = 108枚**（accepted 率 ~94% を見込む） |

> **★紙芝居回避（EP40 の最大の失敗）:** EP40 は静止画100%で `check_animation_mix` に FAIL した。EP41 は **still-cut 96 / (factory 88 + i2v 30) = video 118** で **still-share 44.9% ≤45%・motion coverage 55.1% ≥45%** を構造的に保証する（§3.6）。**SDXL を増やして factory を削るな。**

## 3.5 SDXL と実写在庫の振り分け（どのシーンをどちらで作るか）

- **SDXLで作る = この事件固有物**（§5.9 の 36シーン）: 手が引き抜く1枚・鉄扉・独房内部/天井・空の陪審席/証人席・血の布・ラボ報告書（判読不能）・フォルダ・最高裁法廷内・反対意見のベンチ・朝の光のシルエット。
- **実写在庫で足りる = どこにでもある周辺**（factory・§7.3 の10シーン＋繋ぎ）: New Orleans 夜景・institutional 建物外観・石段・列柱・廊下・記録庫・空の椅子・戸口・空/光・石とコンクリートのテクスチャ。

```
SDXL-primary  = 36シーン（S01 S02 S04-S06 S09-S20 S22-S24 S26 S28 S30-S33 S35-S41 S43 S45 S46）
factory-primary = 10シーン（S03 S07 S08 S21 S25 S27 S29 S34 S42 S44）＋ Sid を持たない繋ぎ 78本
36 + 10 = 46 の視覚シーン（SPEC の S01..S46 に一致）
```

## 3.6 全体の検算（★Codex は自分で再計算して一致を確認）

```
[1] 総カット数 214 = still 96 + factory 88 + i2v 30
[2] 平均ショット長 = (695.0 − OPENING 3.5 − ENDCARD 9.0) / 214 = 682.5/214 = 3.19秒/カット  ✓ (SPEC mean_shot 3.19・≤6.0)
[3] 静止画占有率（check_animation_mix）= 96/214 = 44.86%  ✓ ≤45%（SPEC still_share 0.4486・余裕0.14%）
[4] motion coverage = (88+30)/214 = 55.14%              ✓ ≥45%
[5] per-asset 上限: still 96/80=1.2(≤2) / factory 88/88=1.0(≤1) / motion 30/15=2.0(≤2)  ✓
[6] first-use share = 183/214 = 0.8551                  ✓ ≥0.70（SPEC 一致）
[7] factory 下限 = 695/30 = 23.2 → ≥24本。設計値 88本    ✓（7.90秒に1本）
```

> **[3] の余裕は 0.14% しかない。** still が80枚を割ったら §6.3 の追加生成で回復させ、**still-cut 96 を増やさない**（B側の shotlist が96で固定）。

---

# 4. ★境界契約: `asset_manifest.v001.json`（AとBを繋ぐ唯一のファイル）

**パス:** `episodes/PD-2026-041-thompson/05_visuals/asset_manifest.v001.json`
**スキーマ版:** `thompson_assets.v1`（固定文字列）
**生産者:** `scripts/build_thompson_asset_manifest.py`（**A が実装。他の誰もこのファイルを書かない**）

## 4.1 スキーマ（EP40 の `lech_assets.v1` と同型。counts を EP41 値に）

```jsonc
{
  "schema_version": "thompson_assets.v1",
  "episode_id": "PD-2026-041-thompson",
  "slug": "thompson",
  "generated_at": "<ISO8601>",
  "producer": "scripts/build_thompson_asset_manifest.py",
  "is_stub": false,
  "counts": {
    "still_body": 80,          // >=80
    "still_i2v_source": 15,    // >=15
    "still_thumb": 6,          // >=6
    "motion": 15,              // >=15
    "factory": 88,             // >=88
    "overlay": 10              // >=10（distinct 素材に数えない）
  },
  "stills": [{
    "asset_id": "THOMP-S01-01",            // ^THOMP-S\d{2}-\d{2}$
    "scene_id": "S01",                     // ^S\d{2}$（§5.9 のSDXL担当分）
    "variation": 1, "role": "body",        // body|i2v_source|thumb|reject
    "act": 0,                              // 0=HOOK/1..4=幕/5=ED/9=サムネ専用
    "path": "H:/pd-media/assets/ai/thompson/S01.png",
    "depth_path": "H:/pd-media/assets/ai/thompson/S01_depth.png",  // role!="thumb" は実在必須
    "public_path": "thompson/img/S01.png", // role="body" のみ非null
    "width": 3840, "height": 2160,         // 長辺>=3840（role="thumb" 以外）
    "sha256": "<64hex>", "phash": "<16hex>", "mean_luma": 61.2,
    "tags": ["cell","steel_door","symbolic"],
    "caption_hint": "the hidden page",     // accuracy_lock 検査対象
    "seed": 0, "model": "juggernautXL_ragnarokBy",
    "source": "ai_codex", "commercial_use": "allowed", "ai_disclosure_required": true,
    "qc": {"reviewed": true, "on_theme": true, "has_readable_text": false,
           "has_identifiable_face": false, "notes": ""}
  }],
  "motion": [{
    "asset_id": "THOMP-M01",               // ^THOMP-M\d{2}$
    "source_scene_id": "S17", "source_still": "H:/pd-media/assets/ai/thompson/S17_03.png",
    "path": "H:/pd-media/assets/ai_video/thompson/M01_rife.mp4",
    "public_path": "thompson/motion/M01_rife.mp4",
    "act": 2, "width": 1280, "height": 720, "fps": 48, "frames": 164, "duration_sec": 3.417,
    "sha256": "<64hex>", "tags": ["dawn","ceiling"],
    "qc": {"reviewed": true, "on_theme": true, "artifact_free": true, "notes": ""}
  }],
  "factory": [{
    "asset_id": "AF-BG-0460",              // 棚 assets/asset_manifest.v001.json の id をそのまま
    "path": "H:/pd-media/assets/factory/backgrounds/AF-BG-0460__...mp4",
    "public_path": "thompson/factory/AF-BG-0460__...mp4",
    "type": "backgrounds", "subtype": "<label>",   // ★ラベル=検索語の記録。中身の保証ではない（§7.5）
    "kind": "video", "license": "Pexels License",  // ALLOWED_LICENSES のいずれか
    "sha256": "<64hex>", "act": 1, "covers_scene_id": "S07",  // §7.3 の10シーンのみ。繋ぎは null
    "duration_sec": 8.24, "width": 1920, "height": 1080, "mean_luma": 41.2,
    "eyeballed_content": "a dark New Orleans street at night, wide static, no people",  // ★必須（§7.5）
    "qc": {"reviewed": true, "on_theme": true, "no_watermark": true,
           "no_recognizable_person": true, "no_cartoon": true, "label_matches_content": true, "notes": ""}
  }],
  "overlay": [{
    "asset_id": "AF-PART-0031", "path": "H:/.../particle_assets/...mp4",
    "public_path": "thompson/overlay/...mp4", "type": "particle_assets", "subtype": "<label>",
    "license": "Pexels License", "sha256": "<64hex>", "blend_hint": "screen",
    "eyeballed_content": "slow dust motes on black, loops cleanly",
    "qc": {"reviewed": true, "on_theme": true, "no_watermark": true, "notes": ""}
  }]
}
```

## 4.2 `--verify` の不変条件（BLOCKING）

1. `schema_version=="thompson_assets.v1"` / `episode_id`/`slug` 一致 / `is_stub==false`
2. `counts.*` が各配列の実長と完全一致し §4.1 の下限を満たす
3. 全 `path`/`depth_path`/`public_path` がディスクに実在
4. `sha256` が全配列を通して一意（重複ゼロ）
5. `role!="thumb"` の全静止画で `max(width,height)>=3840`
6. `role=="body"` は `depth_path` と `public_path` が非null かつ実在
7. `qc.has_readable_text==true` または `qc.has_identifiable_face==true` は `role=="reject"`
8. `role=="i2v_source"` は `role=="body"` と**同一 asset_id を共有しない**（distinct 分離）
9. 全JSON文字列が §1.2 の `BANNED_PORTRAIT` に一致しない
10. `factory[].license`/`overlay[].license` が `ALLOWED_LICENSES`（§7.4）に含まれる
11. `factory[].sha256` が **EP39 と EP40 の staged 素材**と1件も衝突しない（§7.7）
12. `factory[].eyeballed_content` が空でない（＝目視していない本が混じっていない）
13. `factory[].qc.label_matches_content==true`

`--reuse-feasibility` では §3.6 [5][6][7] を再計算し、1つでも割ったら exit 1。

## 4.3 `role` の割り当て（機械的に決める）

```
1. accepted 画像を mean_luma と phash で重複除去し scene_id 昇順に並べる
2. i2v_source : §8.1 の15シーンから各1枚（そのシーンの accepted 中 phash が最も他と離れた1枚）
3. thumb      : S24 / S02 / S31 から優先的に6枚
4. body       : 残り全部。最低80枚。80に満たなければ §6.3 の追加バッチを回す
5. reject     : QCで落ちたもの（マニフェストに残し理由を qc.notes に）
```

---

# 5. A-1: SDXL 静止画のバッチ生成（36シーン × 3 = 108枚）

## 5.1 生成環境（★既存の `generate_sdxl_4k.py` を使う）

```
API:   http://127.0.0.1:7860（ローカル AUTOMATIC1111・課金なし）
モデル: juggernautXL_ragnarokBy（generate_sdxl_4k.py が自動で set_model）
プロンプト元: episodes/PD-2026-041-thompson/04_scenes/ai_prompts.v001.md   ← A が §5.9 の形式で書く
出力:  H:\pd-media\assets\ai\thompson\S<NN>[_VV].png（+ remotion/public/thompson/ に自動コピー）
2段パイプライン: txt2img 1536x864 → hires 3072x1728 → extras R-ESRGAN 4x+ → 3840x2160（長辺≥3840・冪等スキップ）
```

**ローカルGPU生成に課金は発生しない。** 禁止は ElevenLabs TTS / 課金画像API / アップロードのみ（§12）。

## 5.2 ★パーサ契約（`read_prompts()` はこの2行形式しか読まない・実装確認済み）

正規表現 `^\s*-\s+`([^`]+\.png)`\s*$` ＋ 次に `Avoid:` を含む行:

```
- `S01.png`
<positive prompt> Avoid: <negative>
```

- **1行目:** `` - `S01.png` `` （バッククォート囲み・**行末は `.png` の直後**。プロンプトを同じ行に書かない）
- **2行目:** 正プロンプト → `Avoid:` → 負プロンプト（負は `DEFAULT_NEG` に自動連結される）
- **EP30 等の旧 `01. <prompt>` 形式は read_prompts() で読めない。** 必ず上記形式で書く。

## 5.3 生成コマンド

```bash
# まず1枚だけ回して読める行数を確認（★shots=36 でなければ形式が壊れている）
./.venv/Scripts/python.exe scripts/generate_sdxl_4k.py 41 --variants 3 --only S01
#   → ログ "episode=... shots=36 variants=3 ... -> 108 images" の shots が 36 であること

# 全108枚（冪等・長辺>=3840 の既存はスキップ）
./.venv/Scripts/python.exe scripts/generate_sdxl_4k.py PD-2026-041-thompson --variants 3
#   → 生成 S01.png / S01_02.png / S01_03.png ... 各シーン3枚
```

> `generate_sdxl_4k.py` は `--only <stem>` で1シーンだけ回せる。QC で落ちたシーンの再生成は `--only S17` を使う（既存の>=3840はスキップ・不足だけ埋まる）。**枚数を減らして基準を下げるのは禁止。**

## 5.4 共通スタイル `[STYLE]`（全プロンプト末尾に必ず連結）

```
, cinematic still, cold desaturated institutional grade, steel grey and concrete with near-black shadows, a single warm sodium practical light as the only warmth, faintly blue-grey cold shadows, deep shadow detail retained, telephoto compression and frontal symmetry, ultra-detailed, photoreal, 4K, 16:9, fine film grain, no text, no watermark, no logo
```

> **EP39/EP40 との分離:** `navy`/`electric blue`/`interrogation`（EP39）・`midday sunlight`/`suburban`/`bleached daylight`（EP40）を**1語も含めない**。

## 5.5 共通ネガティブ `[NEG]`（各 `Avoid:` の後に必ず付ける）

```
text, words, letters, numbers, captions, watermark, logo, readable document, legible court paper, real celebrity, recognizable real person, identifiable face, portrait, mugshot, likeness of a specific person, cartoon, illustration, 3d render, low quality, blurry, deformed, extra limbs, nudity, explicit, gore, blood pool, corpse, midday suburban daylight, electric blue interrogation
```

## 5.6 バリエーション軸（`generate_sdxl_4k.py` はシード違いで `_02`/`_03` を作る）

`_01` = 基準 / `_02` = 別シード（同プロンプト・別の解） / `_03` = 別シード。**同じ被写体の別解**であり、**別の被写体を増やすのは §5.9 のシーン数（36）で担保する**（EP40 指摘「反復感の原因は総枚数ではなくシーン数」）。

## 5.7 SDXL担当シーン数の確認

```
S01 S02 S04 S05 S06 S09 S10 S11 S12 S13 S14 S15 S16 S17 S18 S19 S20 S22 S23 S24
S26 S28 S30 S31 S32 S33 S35 S36 S37 S38 S39 S40 S41 S43 S45 S46
= 36 シーン    ✓  108枚（×3）
factory-primary の S03 S07 S08 S21 S25 S27 S29 S34 S42 S44（10シーン）は SDXLで作らない（§7.3）
```

## 5.8 メタJSON

`generate_sdxl_4k.py` は画像を書くが per-image メタJSONは書かない。**A は QC 時に `qc_thompson_stills.py` で各画像の `sha256`/`phash`/`mean_luma`/`long_edge` を測り `still_qc.v001.json` に記録する**（§6.2）。

## 5.9 確定プロンプト（★`ai_prompts.v001.md` にこの36エントリをそのまま書く）

> 各行の `[STYLE]` は §5.4 を、`Avoid:` の後の `[NEG]` は §5.5 を**全文展開**して書く（下記は簡潔表記）。R1: 全て顔なし・象徴・判読不能。

```
- `S01.png`
Extreme close-up of one anonymous adult hand, cropped at the wrist, pulling a single sheet of paper from a thick aged case file in a cold pool of light, the page text completely illegible, deliberate and quiet, no face [STYLE] Avoid: [NEG]
- `S02.png`
A single closed steel cell door seen head-on in dim institutional light, heavy rivets and a small slot, cold grey metal against near-black, the finality of a lock, no people [STYLE] Avoid: [NEG]
- `S04.png`
An empty prosecutor's office at night, a bare wooden desk and one empty chair under a single sodium lamp, an unopened case file squared on the blotter, impersonal and institutional, no people, no readable text [STYLE] Avoid: [NEG]
- `S05.png`
An empty jury box of twelve vacant wooden seats in a dim courtroom, frontal symmetry, long shadows across the rail, the weight of twelve absent strangers, no people [STYLE] Avoid: [NEG]
- `S06.png`
An empty witness stand beside the judge's bench in cold courtroom light, a microphone turned away, the vacant seat where a voice would go, no people, no readable text [STYLE] Avoid: [NEG]
- `S09.png`
Close-up of anonymous hands and a booking desk, a manila folder and an ink pad in hard side light, the machinery of a record being made, cropped so no face is visible, no legible text [STYLE] Avoid: [NEG]
- `S10.png`
A single folded cloth marked with a dark stain resting in an evidence tray under cold light, non-graphic and symbolic, the object that would decide everything, no people, no readable label [STYLE] Avoid: [NEG]
- `S11.png`
Two case folders laid side by side on a grey table under one lamp, one thicker than the other, a hand withdrawing, the cold arithmetic of trying one case before the other, no face, no legible text [STYLE] Avoid: [NEG]
- `S12.png`
Macro of a crime-lab report form under raking light, the printed characters and a blood-type notation rendered completely illegible and abstract, a paperclip edge, no readable words, no people [STYLE] Avoid: [NEG]
- `S13.png`
The back of a lone figure seated at a defense table in a dim courtroom, seen from behind and unidentifiable, head slightly bowed, the silence of a man who never spoke, no face [STYLE] Avoid: [NEG]
- `S14.png`
A dim cellblock tier receding into shadow with a single steel door standing open at the end, cold institutional geometry, the threshold into death row, no people [STYLE] Avoid: [NEG]
- `S15.png`
The interior of a single prison cell seen head-on, a narrow bunk, a steel toilet, bare concrete walls, one small high window letting in weak grey light, claustrophobic and symmetrical, no people [STYLE] Avoid: [NEG]
- `S16.png`
Extreme close-up of a heavy steel cell lock and bolt mechanism seated shut, scratched metal catching a hard sliver of light, the sound of it implied, no people, no text [STYLE] Avoid: [NEG]
- `S17.png`
The ceiling of a prison cell photographed from the bunk's point of view at dawn, the concrete turning a specific shade of grey as first light arrives, still and endless, no people [STYLE] Avoid: [NEG]
- `S18.png`
A wall calendar in a dim room with pages caught mid-turn, dates blurred and unreadable, the paperwork of a scheduled death moving forward, cold light, no people, no legible numbers [STYLE] Avoid: [NEG]
- `S19.png`
A long empty prison corridor at night lit by a single overhead fixture, a faint human silhouette far down the hall reduced to an outline, cold shadows, the sound of nothing happening, no face [STYLE] Avoid: [NEG]
- `S20.png`
A dim hospital room window at dusk with a bare chair beside an unmade bed, a man dying implied but never shown, only the empty furniture and grey light, no people, no readable text [STYLE] Avoid: [NEG]
- `S22.png`
A calendar page in cold light with two dates isolated in pools of light while the rest falls to shadow, one marked as set and one as the day itself, the numbers abstract and unreadable, no people [STYLE] Avoid: [NEG]
- `S23.png`
Anonymous hands pulling boxes of old files from a records shelf under a bare bulb, dust in the light, the frantic search of an investigator, cropped at the forearms, no face, no legible text [STYLE] Avoid: [NEG]
- `S24.png`
A single sheet of paper held up into a shaft of hard light, the text completely illegible, the proof that had been sitting in the system the entire time, reverent and quiet, no face [STYLE] Avoid: [NEG]
- `S26.png`
An empty jury box with the low gate swung open, cold courtroom light, the seats just vacated after a verdict of minutes, the word not-guilty implied by absence, no people, no text [STYLE] Avoid: [NEG]
- `S28.png`
A cold institutional table with an empty chair and a single closed ledger under a lamp, the symbol of a large verdict without any number shown, restrained and heavy, no people, no legible figures [STYLE] Avoid: [NEG]
- `S30.png`
The interior of a supreme courtroom photographed frontally, a long empty bench with nine vacant high-backed seats in cold marble light, monumental and unmoved, no people, no readable inscription [STYLE] Avoid: [NEG]
- `S31.png`
A stark composition of a marble surface split by a hard line of shadow into a larger and a smaller side, cold light, the visual of a division without any faces or text, abstract and severe, no people [STYLE] Avoid: [NEG]
- `S32.png`
Macro of the corner of a legal opinion page on a dark desk, one block of unreadable text isolated in light while the page falls into shadow, no legible words, no people [STYLE] Avoid: [NEG]
- `S33.png`
A row of identical file folders receding on a shelf under cold light, one pulled slightly proud of the others, the idea of a pattern, no people, no legible labels [STYLE] Avoid: [NEG]
- `S35.png`
An empty appellate courtroom bench in raking cold light, tall and vacant, a single closed folder resting at its center, the seat of a decision, no people, no readable text [STYLE] Avoid: [NEG]
- `S36.png`
A vacant judicial bench seen frontally with one lit lectern below it and a stack of pages, the reading of a dissent implied by absence, cold institutional light, no people, no legible text [STYLE] Avoid: [NEG]
- `S37.png`
Four identical file folders arranged in a cold row under a single lamp, each closed, the weight of four people who knew, above them a faint grey concrete ceiling echoing a cell, no people, no legible labels [STYLE] Avoid: [NEG]
- `S38.png`
A single sheet of paper, a small receipt, and an index card laid on black under one hard light, the symbols of evidence that could set a person free, all text illegible, no people [STYLE] Avoid: [NEG]
- `S39.png`
A dim courtroom composition contrasting a full empty jury box on one side with a single closed office door on the other, the difference between hearing everything and hearing only what one office allows, no people, no text [STYLE] Avoid: [NEG]
- `S40.png`
The view from inside a dark cell looking out through bars toward a distant lit desk with a folder on it, shallow cold light, one page held across an unreachable distance, no face [STYLE] Avoid: [NEG]
- `S41.png`
The silhouette of a well-dressed figure standing at a desk with a folder open under a single lamp, seen against cold light so only the outline exists, no face, the person holding the file, no legible text [STYLE] Avoid: [NEG]
- `S43.png`
The silhouette of a lone figure walking away into soft morning light through an open doorway, seen from far behind, only the outline, quiet and unresolved, no face [STYLE] Avoid: [NEG]
- `S45.png`
An empty witness stand in cold courtroom light with a single microphone now turned toward it, the return of a voice that had been silenced, no people, no readable text [STYLE] Avoid: [NEG]
- `S46.png`
A single lit window in a dark building at dusk, the last blue in the sky, one warm room among many dark ones, quiet and open-ended, no people, no visible address [STYLE] Avoid: [NEG]
```

**枚数チェック:** 上記 36 エントリ。§5.3 の `--only S01` ログで `shots=36` を確認してから本番108枚を回す。

---

# 6. A-2/A-3: 静止画のQC・選抜・depth map

## 6.1 機械QC（全108枚・`qc_thompson_stills.py`）

| # | 検査 | 判定 | 落ちたら |
|---|---|---|---|
| Q1 | 解像度 | `max(w,h)>=3840` | reject |
| Q2 | サイズ/開ける | `>1024 bytes` かつ PIL で開ける | reject |
| Q3 | 平均輝度 | `35.0<=mean_luma<=225.0`（EP41は暗いエピソード→黒潰れ側が本命リスク。`check_visual_asset_qc.DARK_LUMA_FLOOR=45.0` を下回りすぎる本に注意） | reject |
| Q4 | 近似重複 | 全ペア phash。類似度 `>=0.90` は片方 reject（`check_visual_asset_qc.NEARDUP_SIM=0.90`） | 片方 reject |
| Q5 | 文字の混入 | **目視。** 読める英字・数字・ロゴが写っていないか | `has_readable_text=true`→reject |
| Q6 | 顔の混入 | **目視。** 識別可能な顔が写っていないか | `has_identifiable_face=true`→reject |

**Q5/Q6 は機械で判定しない。** コンタクトシートを出して**全108枚を実際に目視**する:

```bash
./.venv/Scripts/python.exe scripts/build_footage_contact_sheet.py --ep PD-2026-041-thompson --media image
#   → runs/qc/thompson_footage_contact_NN.png（20枚/シート）。全シートを開いて1枚ずつ見る
```

> **EP38の教訓: ファイル名・プロンプトを信じるな。生成物を実際に見ろ。** 「S12 は報告書だからテキストは判読不能のはず」は根拠にならない。SDXL は平気で読める文字と顔を描く。

## 6.2 出力

```
episodes/PD-2026-041-thompson/05_visuals/still_qc.v001.json     # 108枚全部の行（reject も残す・sha256/phash/mean_luma/long_edge）
episodes/PD-2026-041-thompson/05_visuals/（build_footage_contact_sheet が runs/qc に出す）
```

## 6.3 accepted が101枚に届かなかったとき

```bash
./.venv/Scripts/python.exe scripts/generate_sdxl_4k.py 41 --variants 3 --only S17   # 落ちたシーンだけ再生成（別シード）
./.venv/Scripts/python.exe scripts/qc_thompson_stills.py
```
accepted >= 101（body 80 + i2v_source 15 + thumb 6）になるまで繰り返す。**基準を下げない。**

## 6.4 depth map（★新規スクリプトを作らず既存を使う）

```bash
./.venv/Scripts/python.exe scripts/gen_depth_maps.py --dir "H:/pd-media/assets/ai/thompson"
```
- モデル `Intel/dpt-large`。出力 `<stem>_depth.png`（同サイズ L グレースケール）。冪等。
- **role が `body` の静止画は depth 必須**（`treatment:"depth"` が隣に `_depth.png` を要求。無いとレンダーがクラッシュ）。`thumb` は不要。
- staging 後に `remotion/public/thompson/img/` 側でも同名ペアが揃っていること（§10）。

---

# 7. A-4: factory 実写クリップ 88本の選定と全点目視QC

## 7.1 在庫の実態

```
H:\pd-media\assets\factory\   フラット構成
  backgrounds/     11,443本（.mp4）  ← ★主力（New Orleans夜景・institutional・廊下・記録庫・空・繋ぎ）
  light_assets/    …            合成レイヤー（光条）
  particle_assets/ …            合成レイヤー（埃・塵）
  vfx_overlays/    …            合成レイヤー（グレイン・煙）
  texture_assets/  …            紙・石・コンクリートのテクスチャ
  loops/           …            抽象的な繋ぎ
ファイル名規約: AF-<TYPECODE>-<4桁>__<subtype_slug>.<ext>（TYPECODE = BG|LIGHT|LOOP|PART|TEX|VFX）
棚レジストリ: C:\Users\aab15\Documents\prime-documentary\assets\asset_manifest.v001.json
   （トップキーは schema と assets。★必ず encoding="utf-8" で開く。cp932 既定だと落ちる）
```

## 7.2 選定条件

- **`kind=="video"` のみ。** 静止画 factory は使わない
- **88本ちょうど**（下限24本。695/30=23.2）
- **各1回しか使わない**（`check_asset_reuse.MAX_USES_FACTORY=1`）
- 幕別割り当て（目安）: 幕1=16 / 幕2=18 / 幕3=24 / 幕4=16 / ED=6 / HOOK=8
- **EP39（夜/取調室/青）・EP40（郊外/昼/破壊）の絵柄を選ばない。** EP41 は institutional・冷たい石と鉄・夜〜夜明け前

**既存の選定ツールで候補出し（新規に検索ロジックを書くな）:**

```bash
./.venv/Scripts/python.exe scripts/select_factory_assets.py --themes   # テーマ一覧と件数
./.venv/Scripts/python.exe scripts/select_factory_assets.py \
    --kind video --query prison --limit 90 --exclude-used --ep PD-2026-041-thompson --json
```
`--exclude-used` は `check_arc_nonrepeat.build_universe()` と同じ指紋集合を使うので出荷ゲート `arc_nonrepeat` と食い違わない。**必ず付ける。**

## 7.3 実写在庫でカバーする10シーン（SDXLで作らない）

| Sid | 内容 | `--query` 例 |
|---|---|---|
| S03 | 最高裁ファサード/列柱 | `courthouse` / `columns` / `supreme_court_building` |
| S07 | New Orleans 1984 夜景（引き） | `new_orleans_night` / `city_night` / `street_night` |
| S08 | 事件現場の象徴（無人街路・回転灯） | `police_lights_night` / `empty_street_night` |
| S21 | 告白が渡る＝2つの空の椅子 | `empty_chairs` / `office_night` |
| S25 | 2003 再審の法廷（無人） | `courtroom_empty` / `courtroom_interior` |
| S27 | Orleans Parish DA の建物 | `government_building` / `courthouse_exterior` |
| S29 | 石段・列柱（最高裁へ上る） | `courthouse_steps` / `marble_columns` |
| S34 | ルイジアナの記録庫 | `archive_shelves` / `file_room` / `records` |
| S42 | 歩き戻る国（institutional 外の街） | `city_dusk` / `sidewalk_walking_back` |
| S44 | Resurrection ＝灯る戸口 | `lit_doorway_night` / `warm_window_night` |

**残り78本は Sid を持たない繋ぎ・情景クリップ**（`covers_scene_id:null`）: institutional 建物・廊下・階段・空の椅子・記録庫・夜〜夜明けの空・石とコンクリートのマクロ・抽象 `loops`。**暗いクリップに偏りすぎない**（§7.5 の暗側閾値に注意・全体の1/3=約29本まで）。

## 7.4 ライセンス（`ALLOWED_LICENSES` — これ以外選ばない）

```python
ALLOWED_LICENSES = {"cc0","royalty_free","generated_owned","Pexels License","Pixabay Content License"}
```

## 7.5 ★★★ factory のファイル名とサブタイプは信用できない ★★★

> **推測ではなく実際に起きた事故。** EP36: `city_surveillance_camera_dome` が大聖堂。EP38: 牛が `documents_on_desk`。`subtype` は「その検索語で取った」記録であって**中身の保証ではない**。

**選抜88本は例外なく次を経る:**

```bash
# 1) 選定した88本を staging フォルダに集め、ラベル付きコンタクトシートを出す
./.venv/Scripts/python.exe scripts/build_footage_contact_sheet.py \
    --ep PD-2026-041-thompson --media video --dir "<88本の staging フォルダ>"
#   → runs/qc/thompson_footage_contact_NN.png（各タイルにファイル名ラベル）
```

2. **コンタクトシートを実際に開き、88本すべてを1本ずつ見る**
3. 各本について `asset_manifest.v001.json` の **`eyeballed_content` に「実際に見た内容」を1文の英語で書く**（ファイル名の言い換え禁止）。`subtype` と食い違ったら `label_matches_content:false` を立てて**選定から外す**
4. 実写シネマティックB-roll（アニメ/CG臭排除）・EP41テーマ（institutional/夜/石と鉄）・ウォーターマークなし・識別可能な実在人物なしを確認
5. `05_visuals/factory_clip_qc.v001.json` を固定タイムスタンプで原子的に書く（冪等）

閾値（`check_visual_asset_qc.py`）: `DARK_LUMA_FLOOR=45.0` / `MAX_DARK_FRACTION=0.40` / `NEARDUP_SIM=0.90` / `MIN_VARIETY=0.60`。
> **EP41 は夜のエピソードなので暗側が本命リスク。** 平均輝度45未満のクリップが全体の40%を超えると FAIL。**暗いクリップは約29本（1/3）までに抑え、institutional の弱い実用光がある本を優先する。**

**1フレームで判断がつかない本は VLC/ffplay で再生して確認**（near-still は `check_animation_mix` を落とす）。

## 7.6 出力

```
episodes/PD-2026-041-thompson/05_stock/factory_selection.v001.json   # 選定理由と幕割り当て
episodes/PD-2026-041-thompson/05_visuals/factory_clip_qc.v001.json   # ゲートが読む reviewed マニフェスト
```

## 7.7 EP39/EP40 との重複ゼロ（BLOCKING）

```bash
./.venv/Scripts/python.exe scripts/select_thompson_factory.py --verify-no-prior-overlap
```
`episodes/PD-2026-039-*/` と `episodes/PD-2026-040-*/` の `05_stock/stock_ledger*.json`（および `05_visuals/asset_manifest*.json` があれば）を**読み取り専用で**開き、`sha256` 集合と EP41 の88本の積集合が**空**であることを確認。1件でも exit 1 で差し替え。**EP39/EP40 のファイルは読むだけ。書き込み・移動・削除は一切しない。**

---

# 8. A-5: i2v モーション化 15本（Wan 2.2 A14B → RIFE 48fps）

## 8.1 i2v にする15シーン（動きが意味を持つ絵）

| # | asset_id | 元シーン | 動きの意味 | act |
|---|---|---|---|---|
| 1 | THOMP-M01 | S01 | 古いファイルから1枚が引き抜かれる | 0 |
| 2 | THOMP-M02 | S16 | 鉄扉のロックが座る | 1 |
| 3 | THOMP-M03 | S17 | 独房天井が夜明けに灰へ変わる | 2 |
| 4 | THOMP-M04 | S18 | カレンダーのページがめくれる | 2 |
| 5 | THOMP-M05 | S19 | 夜の廊下のシルエット（微動） | 2 |
| 6 | THOMP-M06 | S22 | 2つの日付の間で時間が過ぎる | 2 |
| 7 | THOMP-M07 | S23 | ファイルを漁る手 | 2 |
| 8 | THOMP-M08 | S24 | 光の中で1枚が揺れる | 2 |
| 9 | THOMP-M09 | S31 | 分割の影がゆっくり動く | 3 |
| 10 | THOMP-M10 | S32 | 判決ページに埃が降る | 3 |
| 11 | THOMP-M11 | S36 | 反対意見のページがわずかに動く | 3 |
| 12 | THOMP-M12 | S38 | 証拠の紙が並ぶ | 4 |
| 13 | THOMP-M13 | S40 | 遠い机の光が揺れる | 4 |
| 14 | THOMP-M14 | S43 | 朝の光へシルエットが歩く | 5 |
| 15 | THOMP-M15 | S46 | 窓の明かりが灯る | 5 |

**元画像は `role:"i2v_source"` として専用確保し、body に回さない**（§4.2 不変条件8）。各シーンの `_03` を i2v-source に。

## 8.2 Wan 2.2 A14B の設定（★Known-good・この値を変えるな。`comfy_wan_kidsforcash.py` を下敷きにパスと SHOTS だけ差し替え）

```python
HOST = "http://127.0.0.1:8188"                              # ローカル ComfyUI
HIGH = "wan2.2_i2v_high_noise_14B_fp8_scaled.safetensors"
LOW  = "wan2.2_i2v_low_noise_14B_fp8_scaled.safetensors"
VAE  = "wan_2.1_vae.safetensors"       # ★2.1（2.2 ではない・無言の品質劣化の原因）
CLIP = "umt5_xxl_fp8_e4m3fn_scaled.safetensors"
WIDTH, HEIGHT = 1280, 720
FRAMES = 41        # 4090 の全ロード上限@720p（81 で部分ロード=3倍遅い）
STEPS = 40 / SPLIT = 20 / SHIFT = 5.0   # ★SHIFT 5.0（8.0 は 5B からの無言持ち越しでバグ）
CFG = 3.5 / SAMPLER,SCHEDULER = "euler","simple" / FPS = 16
STILL_DIR     = H:\pd-media\assets\ai\thompson
VIDEO_OUT_DIR = H:\pd-media\assets\ai_video\thompson
POS_PREFIX = "cinematic documentary shot, subtle natural motion, "
POS_SUFFIX = ", slow deliberate camera move, shallow depth of field, film grain, photoreal, consistent lighting, no sudden changes"
NEG_PROMPT = "static, motionless, blurry, low quality, distorted, deformed, extra limbs, bad anatomy, morphing face, flickering, jitter, warping, text, watermark, identifiable face, real person likeness"
```

**ゲート:** `dry_validate`（length=5 で1回POSTして配線エラーを安く検出）/ `assert_loaded_completely`（部分ロード検出）/ `assert_frame_math`（フレーム計算）。`--run` パスにだけ配線。

## 8.3 実行手順（まず1本で通す）

```bash
py -3.11 scripts/comfy_wan_thompson.py --build            # グラフだけ（GPU触らない）
py -3.11 scripts/comfy_wan_thompson.py --run --shot S17   # 1本本番して目視
py -3.11 scripts/comfy_wan_thompson.py --run-all          # 残り14本（冪等・既存スキップ）
```
1本 24–73 GPU分・15本で 6.5–18時間。`/queue` `/history` を30秒間隔でポーリング。

## 8.4 RIFE で 48fps 化（`rife_thompson.py`・`rife_kidsforcash.py` と同手順）

```
RIFE = D:/AI/tools/rife-ncnn-vulkan-20221029-windows/rife-ncnn-vulkan.exe / モデル rife-v4.6
```
1. Wan 出力先頭 **5フレームは length=5 検証プローブなので捨てる**（`DROP_VALIDATE=5`）
2. 残り41を `f0001.png` 連番にリネーム → RIFE 2x を**2回**（=4x）→ **164フレーム**
3. 164/48fps = **3.417秒** → `ffmpeg -framerate 48 -i f%04d.png -c:v libx264 -pix_fmt yuv420p` で `M<NN>_rife.mp4`
4. **フレーム数検証** `n2 >= 4*n0 - 8` でなければ `SHORT?` で記録し reject

## 8.5 i2v の QC

- 顔が生成されていないこと（NEG で抑えているが**必ず目視**）
- モーフィング/ちらつき/ワープが無いこと → あれば別シードで再生成
- 3.417秒あるので B のカット設計では 3.0–3.4秒で使う想定

---

# 9. A-6: 合成レイヤー（distinct 素材に数えない）

| 種別 | 選定 | 用途 |
|---|---|---|
| `particle_assets` | **5本** | 独房光の埃・記録庫の塵。黒背景 drift を screen 合成 |
| `light_assets` | **3本** | 単一 sodium 実用光の光条 |
| `vfx_overlays` | **2本** | 微細なグレイン・煙 |
| **合計** | **10本** | |

**ルール:** 合成レイヤーは `check_asset_reuse` の distinct に数えない → `remotion/public/thompson/overlay/` に置き、`thompson_film.json` の `cuts[].src` には**出さない**（出すと factory 判定で1回制限を食う）。同じレイヤーを何度重ねてもよい（素材ではなく加工）。黒背景でループするものを選び `blend_hint` を書く。**§7.5 の目視QC対象**（10本・10分）。

```bash
# select_factory_assets.py の候補から選び、overlay_selection.v001.json に記録
./.venv/Scripts/python.exe scripts/select_factory_assets.py --kind video --query dust_particles --limit 20 --exclude-used --ep PD-2026-041-thompson --json
```

---

# 10. A-7/A-8: staging とマニフェスト出力

## 10.1 Remotion public への staging（`scripts/stage_thompson_assets.py`）

```
remotion/public/thompson/img/     ← role=body の静止画（+ 同名 _depth.png）
remotion/public/thompson/factory/ ← 選定 factory .mp4 88本
remotion/public/thompson/motion/  ← i2v M<NN>_rife.mp4 15本
remotion/public/thompson/overlay/ ← 合成レイヤー 10本
```
- `public_path` はマニフェストの値と実ファイルが一致すること
- factory 動画は `libx264 crf 16 preset medium -an` で **30fps に conform** してコピー（`import_to_remotion.py` の `conform_video(...,fps=30)` と同じ）
- i2v は 48fps のまま置く
- 既存 sha256 一致ならコピーをスキップ（冪等）

**★命名規則（`check_asset_reuse.kind_of()` がパス文字列で分類する・外すと誤分類）:**
- factory の `public_path` は必ず `thompson/factory/` の下（`/factory` を含む）
- i2v の `public_path` は必ず `.mp4` で終わり `_rife` を含む
- 静止画の `public_path` は `.png` で `/factory` も `ai_video` も `_rife` も**含めない**
- 合成レイヤーは `thompson/overlay/` に置き `cuts[].src` に出さない

## 10.2 権利台帳 `05_stock/stock_ledger.v001.json`

全静止画・i2v・factory・overlay を1行ずつ: `asset_id`/`path`/`source`（`ai_codex` or `factory`）/`license`/`commercial_use`/`sha256`/`ai_disclosure_required`/`generated_at`。

## 10.3 境界契約マニフェストの出力

```bash
./.venv/Scripts/python.exe scripts/build_thompson_asset_manifest.py
./.venv/Scripts/python.exe scripts/build_thompson_asset_manifest.py --verify
./.venv/Scripts/python.exe scripts/build_thompson_asset_manifest.py --reuse-feasibility
```
この3つが exit 0 で「マニフェストが本番になった」。**Bのファイルを直接書き換えて知らせようとしない。**

---

# 11. 素材反復禁止ゲートの実仕様（`check_asset_reuse.py`）

```python
MAX_USES_FACTORY = 1        # 無料 + 11,443本 → 繰り返す理由が無い
MAX_USES_MOTION  = 2
MAX_USES_STILL   = 2
MIN_FIRST_USE_SHARE = 0.70
```
種別判定は**パス文字列**（`kind_of()`）: `/factory` or `af-bg-` → factory / `.mp4|.mov|.webm` or `ai_video` or `_rife` → motion / それ以外 → still。§10.1 の命名規則を守る。

EP41 の設計値: still 96/80=1.2(≤2) / factory 88/88=1.0(≤1) / motion 30/15=2.0(≤2) / first-use 183/214=0.855(≥0.70)。**全て達成可能。**

---

# 12. 絶対にやらないこと

- **EP39（frazier）/EP40（lech）のファイルに一切触らない。** 読み取りのみ可。素材・色・音のレーンも分離。
- **スレッドBの所有ファイル（§0.2）に触らない。** 特に `remotion/src/**` `scripts/ae/**` `manifest.json` `04_scenes/shotlist*` `figures`。
  - **ただし `04_scenes/ai_prompts.v001.md` は A が書く**（`generate_sdxl_4k.py` の入力・§5.9）。B は読むだけ。
- **図解・トランジション・タイポの素材を探しに行かない。** 在庫が薄い/無いカテゴリは B が自作する。
- **課金ジョブを起動しない**（ElevenLabs TTS / 課金画像API / アップロード）。ローカル A1111・ComfyUI・RIFE は GPU を使うだけで課金なし（オーナー許可済み）。
- **公開済み・出荷済み mp4 を上書き・再レンダしない。**
- **実在人物の肖像・likeness をどこにも作らない**（§1）。
- **枚数・本数を「だいたい」で決めない。** §3.4 の確定値と §3.6 の検算をそのまま使う。合わなければ実装ではなく**本書を疑って報告**。
- **★ファイル名・subtype・プロンプトを根拠に「大丈夫」と判断しない。** EP36は大聖堂を、EP38は牛を通した。**生成物・在庫クリップを実際に見る。**

---

# 13. 完了報告に含めるもの

```
1. accepted 静止画の枚数と内訳（body 80 / i2v_source 15 / thumb 6 / reject N）
2. factory 選定 88本のリスト（asset_id / subtype / eyeballed_content）と、subtype と食い違って外した本数
3. EP39/EP40 重複ゼロの確認結果
4. i2v 15本の frames / duration_sec と、SHORT? の有無
5. 合成レイヤー10本のリスト
6. §0.4 の [A-DONE-1]〜[A-DONE-5] の実行結果（exit code をそのまま貼る）
7. §3.6 の検算 [1]〜[7] を自分で再計算した結果
8. asset_manifest.v001.json の counts ブロック
```

**「動いたと思う」は完了ではない。ゲートが exit 0 を返して初めて完了。自分でQC基準を書き換えて通すのは禁止。**
