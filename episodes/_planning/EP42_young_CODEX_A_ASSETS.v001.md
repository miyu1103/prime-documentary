# EP42 young — Codex スレッドA「素材生成」引き継ぎプロンプト v001

> **このファイルは単体で完結している。他のファイルを読まなくても着手できる。**
> 設計書（DESIGN）も実装スレッドB（CODEX_B）のファイルも**読まなくてよい**（必要な数値はすべて本書に転記済み）。
> **唯一の外部真実 = `episodes/_planning/EP42_young_PRODUCTION_SPEC.v001.json`**（機械生成）。本書の数値はそこから転記したものであり、手書きで発明していない。

```
あなたは Prime Documentary（YouTubeドキュメンタリーチャンネル）の制作エンジニアです。
リポジトリ: C:\Users\aab15\Documents\prime-documentary
Python:     C:\Users\aab15\Documents\prime-documentary\.venv\Scripts\python.exe
メディア:   H:\pd-media
担当:       EP42 / Episode ID: PD-2026-042-young / slug: young
```

---

# 0. このスレッド（A）の責務・境界・完了条件

## 0.1 責務（GPU律速・目視律速の長時間ジョブ）

本編で使う「絵」を全部そろえ、1本のマニフェストに書き出すところまで。

| # | 作業 | 成果物 | 目安 |
|---|---|---|---|
| A-1 | SDXL静止画のバッチ生成（**85本の固有プロンプト × 1枚 = 85枚**・バリエーション0） | `H:\pd-media\assets\ai\young\S<NN>.png` | 2–3.5時間（GPU） |
| A-1b | i2v 種画像の生成（**16本の固有プロンプト × 1枚 = 16枚**・バリエーション0） | `H:\pd-media\assets\ai\young\M<NN>_src.png` | 30–50分（GPU） |
| A-2 | 静止画のQCと目視（**目視必須**） | `05_visuals/still_qc.v001.json` + コンタクトシート | 1.5時間 |
| A-3 | depth map 生成（`treatment:"depth"` の必須入力） | `H:\pd-media\assets\ai\young\S<NN>_depth.png` | 20分 |
| A-4 | factory 実写クリップ **93本**の選定と**全点目視QC** | `05_stock/factory_selection.v001.json` / `05_visuals/factory_clip_qc.v001.json` | **2.5時間（うち目視だけで1時間以上）** |
| A-5 | i2v モーション化 **16本**（Wan 2.2 A14B → RIFE 48fps） | `H:\pd-media\assets\ai_video\young\M<NN>_rife.mp4` | 7–19時間（GPU） |
| A-6 | 合成レイヤー（particle/light/vfx）の選定 | `05_stock/overlay_selection.v001.json` | 30分 |
| A-7 | 権利台帳と**境界契約マニフェスト**の出力 | `05_stock/stock_ledger.v001.json` / **`05_visuals/asset_manifest.v001.json`** | 20分 |
| A-8 | Remotion public への staging | `remotion/public/young/{img,factory,motion,overlay}/` | 30分 |

> **★★ 最重要の新前提（EP42で方針転換）: 1シーン1枚・バリエーション0 ★★**
> Codex の画像生成は SDXL より高精度になった。**同一ショットの複数バリエーション（`_02`/`_03`）を作らない。**
> EP41 は「36シーン × 3バリエーション = 108枚」で反復回避を水増ししていた。**EP42 は禁止。**
> 代わりに **distinct still を固有プロンプトで各1枚ずつ生成**する（still 85本＝85行の固有プロンプト、各1枚）。
> `generate_sdxl_4k.py` は **`--variants 1`**（または variants 指定なし）で回す。**`--variants 3` は使わない。**
> **総生成画像 = still 85 + i2v 種 16 = 101枚（各1回）。** factory 93本は生成でなく在庫からの選抜。

## 0.2 スレッドB（実装）との境界＝接続点はただ1ファイル

```
episodes/PD-2026-042-young/05_visuals/asset_manifest.v001.json
   ↑ Aが生成（唯一の生産者）        ↓ Bが消費（唯一の消費者）
```

**Bはこのファイル以外のAの中間生成物を読まない。Aはこのファイル以外のBの成果物に依存しない。** Bはスタブで全パイプラインを完走できるので、Aの完了を待っていない。**A も急がなくてよいが途中経過を壊すな。**

### ファイル所有権（破ると並行作業が壊れる）

| パス | 所有 | Aの権限 |
|---|---|---|
| `H:\pd-media\assets\ai\young\**` / `H:\pd-media\assets\ai_video\young\**` | **A** | 読み書き |
| `episodes/PD-2026-042-young/05_visuals/**` / `05_stock/**` | **A** | 読み書き（`mkdir(parents=True, exist_ok=True)` で自作） |
| `episodes/PD-2026-042-young/04_scenes/ai_prompts.v001.md` | **A**（`generate_sdxl_4k.py` の入力） | 読み書き。B は読むだけ |
| `remotion/public/young/{img,factory,motion,overlay}/**` | **A** | 読み書き |
| `episodes/PD-2026-042-young/manifest.json` `03_script/**` `04_scenes/shotlist*` `08_edit/**` `09_package/**` | **B** | **触るな** |
| `remotion/src/**` `remotion/props/**` `scripts/ae/**` `scripts/build_young_film.py` | **B** | **触るな** |
| `episodes/PD-2026-039-*/**` `episodes/PD-2026-040-*/**` `episodes/PD-2026-041-*/**` および EP39/40/41 の素材 | 別エージェント | **絶対に触るな。読み取りのみ可** |

## 0.3 A が使う／作るスクリプト

**★既存スクリプトをそのまま使う（新規に作らない）:**

| パス | 役割 | 引数 |
|---|---|---|
| `scripts/generate_sdxl_4k.py`（**既存**） | §5 の SDXL 生成（`04_scenes/ai_prompts.v001.md` を `read_prompts()` で読む） | `PD-2026-042-young --variants 1` / `42 --variants 1 --only S07` |
| `scripts/gen_depth_maps.py`（**既存**） | §6.4 の depth map | `--dir "H:/pd-media/assets/ai/young"` |
| `scripts/build_footage_contact_sheet.py`（**既存**） | §6/§7 の全点目視コンタクトシート | `--ep PD-2026-042-young --media image` / `--media video --dir <staging>` |
| `scripts/select_factory_assets.py`（**既存**） | §7 の factory 候補出し | `--kind video --query <kw> --limit 96 --exclude-used --ep PD-2026-042-young --json` |
| `scripts/check_visual_asset_qc.py`（**既存**） | §0.4 の factory 全点目視ゲート | `--ep PD-2026-042-young` |

**★Aが新規作成するスクリプト（EP41 の thompson 版を young 用に複製。これ以外を新規に作らない）:**

| パス | 役割 | 下敷き（複製元・EP41） |
|---|---|---|
| `scripts/qc_young_stills.py` | §6 の静止画QC＋解像度チェック | `scripts/qc_thompson_stills.py` |
| `scripts/select_young_factory.py` | §7 の factory 93本の確定選定・EP39/40/41 sha256 除外検証 | `scripts/select_thompson_factory.py` |
| `scripts/comfy_wan_young.py` | §8 の i2v 16本（Wan 2.2 A14B ドライバ・**パスと SHOTS だけ差し替え**） | `scripts/comfy_wan_thompson.py` |
| `scripts/rife_young.py` | §8.4 の RIFE 4x → 48fps | `scripts/rife_thompson.py` |
| `scripts/build_young_asset_manifest.py` | §4 の境界契約マニフェストを出力・自己検証 | `scripts/build_thompson_asset_manifest.py` |
| `scripts/stage_young_assets.py` | §10 の staging | `scripts/stage_thompson_assets.py` |

> **SDXL 生成スクリプトを新規に作らない。** `generate_sdxl_4k.py` が既にある（`read_prompts()` で `04_scenes/ai_prompts.v001.md` を読む）。あなたは **`ai_prompts.v001.md` を §5.2 の2行形式で書く**だけ。**実在しないスクリプトを捏造しない**（上の複製元が実在することを `ls scripts/` で確認してから複製する）。

## 0.4 完了条件（すべて緑で完了。1つでも赤なら未完了）

```bash
cd C:\Users\aab15\Documents\prime-documentary

# [A-DONE-1] 境界契約マニフェストが自己検証を通る
./.venv/Scripts/python.exe scripts/build_young_asset_manifest.py --verify
#   → exit 0。counts が §3/§4 の確定値以上。全パス実在。sha256 重複ゼロ。

# [A-DONE-2] 反復禁止ゲートが素材点数の観点で通る
./.venv/Scripts/python.exe scripts/build_young_asset_manifest.py --reuse-feasibility
#   → still >=85 / motion >=16 / factory >=93 / distinct 合計 >=194 / first-use >=0.70

# [A-DONE-3] 静止画の解像度ゲート（長辺 >=3840）
./.venv/Scripts/python.exe scripts/qc_young_stills.py --check-resolution

# [A-DONE-4] factory の視覚QCゲート（★全93本を目で見た記録があること）
./.venv/Scripts/python.exe scripts/check_visual_asset_qc.py --ep PD-2026-042-young
#   → exit 0（factory_clip_qc.v001.json が staging 済み全クリップを reviewed:true で網羅）

# [A-DONE-5] EP39/EP40/EP41 との素材被りゼロ
./.venv/Scripts/python.exe scripts/select_young_factory.py --verify-no-prior-overlap
#   → 重複 sha256 = 0（EP39・EP40・EP41 の三つすべてに対して）
```

---

# 1. ★★★ 最優先の絶対条件（R1 ＋ 正確性6制約）★★★

**Hudson v. Michigan は制度説明のためだけに登場し、Anjanette Young は実在の私人。本作の絵は「実在人物の顔・身体・肖像を一切出さない」。象徴オブジェのみ。**

## 1.1 R1（生成ビジュアル全般）

1. **実在人物（Young・Booker T. Hudson・Scalia/Kennedy/Breyer 等の判事・市長・警官・弁護士）の顔・likeness・肖像を作らない。** 人物は必ず後ろ姿・シルエット・顔外し・手元のみ、原則「人を出さない」。
2. **実在の住所・番地・判決文・小切手金額・書類の可読文字を再現しない。** 書類・小切手・投票掲示板は雰囲気のみ（判読不能）。数値（$2.9M・48-0・10-4・5-4・§1983）は**画像に描かない**（AE/figures のタイポで出す＝B の担当）。
3. AI画像は概要欄でAI生成を開示 → マニフェストの `ai_disclosure_required: true` を全静止画・全i2vに立てる。全生成ビジュアル表示中は右下に `AI-assisted visualization` を常時表示（オーバーレイは B が付与）。

## 1.2 ★正確性6制約（Aが書く全文字列＝プロンプト・`tags`・`eyeballed_content`・`caption_hint`・`notes`・ファイル名に適用。違反はBLOCKER）

1. **和解≠責任認定。** 「裁判所が違憲/責任を認定」を描かない・書かない。使えるのは「市が支払いに同意・市議会が承認（と報じられる）」まで。小切手の絵には**過失欄が空白**という象徴を含める。
2. **令状は「有効な search warrant（判事署名）」のみ。** カード/プロンプト/タグ/`eyeballed_content` に **`no-knock`** の語を一切書かない（負プロンプトにも書かない）。
3. **改革は否決。** Anjanette Young Ordinance は2022/11に10-4否決・不成立・現行も合法。**`unconstitutional`・`she changed the law`（法が変わった）を一切書かない。** 否決＝`rejected/voted down/set aside` の象徴のみ。
4. **Hudson の射程を圧縮しない。** knock-and-announce は今も憲法上の "command"。否定されたのは救済としての証拠排除のみ。プロンプトは「still a command」を象徴（壁を走る一条の光・閉じた戸口）で示し、"rule abolished/struck down" 等を書かない。
5. **Booker T. Hudson 本人を主役化しない**（存命・薬物有罪の実在人物）。ビジュアルは人物化せず、**Detroit の戸口/敷居の象徴のみ**。顔・身体・人生・その後を描かない。
6. **Young（実在私人）の着替え中/着衣なしは非グラフィック・象徴のみ**（開いたドア・散らばった書類・手錠・時計・足首モニタのアイコン・脱いだコート・空席・空のバッグ）。**顔・身体・肖像・裸体を一切描かない。**

## 1.3 機械ゲート（`build_young_asset_manifest.py --verify` の内部）

A が書いた全JSONの全文字列値に対し、1件でもヒットで exit 1:

```python
import re
BANNED_PORTRAIT = re.compile(
    r"\bportrait\b|\bmugshot\b|likeness of|face of (young|hudson|scalia|kennedy|breyer|wolinski)|"
    r"recognizable (real )?person|identifiable face|深偽|ディープフェイク", re.IGNORECASE)
BANNED_ACCURACY = re.compile(
    r"no[-\s]?knock|unconstitutional|struck down the law|she changed the law|"
    r"court found (the city|them|the police) liable|ruled her rights (were )?violated", re.IGNORECASE)
```

> `BANNED_ACCURACY` は制約1〜4を機械化したもの。プロンプト・タグ・注記のどこにも該当語を書かない。

---

# 2. 台本の語数と尺の確定値（SPEC から転記・Aが素材点数を積算する根拠）

**★唯一の真実 = `episodes/_planning/EP42_young_PRODUCTION_SPEC.v001.json`。** 古い資料の wpm・語数は使うな。

```
words_total          = 2,140
narration_seconds    = 720.9   （= 12.0分）
wpm_used             = 178.1
総尺（設計）          = 733.4秒 = 12:13（narration 720.9 + BrandOpening 3.5 + BrandEndcard 9.0）
視覚シーン(narrative)  = 48（S01..S48・SPEC derive）
```

**Aにとっての意味は1つ:** > **226カット / distinct 194 / 初出85.84% = still 85 + factory 93 + motion 16。**（§3 で積算）

> **注意（EP41 との命名差）:** SPEC の視覚シーンは S01..S48。しかし **still は 85 本の固有プロンプトを持つ**ため、still の資産 ID は **S01..S85**（1プロンプト＝1枚）で採番する。48 の narrative シーンに 85 枚を配分する（ドクトリン核の ACT3 が最も厚い）。still 資産 ID と narrative シーンコードは別物。

---

# 3. ★素材構成の確定値（SPEC の distinct/cuts をそのまま調達する）

## 3.1 SPEC の内訳（★この値で調達する・勝手に変えない）

| 種別 | distinct | 担当カット | 使用回数(cap) | 調達方法 |
|---|---|---|---|---|
| **SDXL静止画（本編 body）** | **85枚** | 101カット | 1.19回(≤2) | **85本の固有プロンプトで各1枚**（§5・バリエーション0） |
| **factory 実写クリップ** | **93本** | 93カット | **各1回(1)** | 在庫 11,000本超から選抜（§7）・全点目視・EP39/40/41 と sha256 被りゼロ |
| **i2v モーション** | **16本** | 32カット | 各2回(≤2) | 16本の固有種プロンプト→Wan（§8） |
| **合計（カットに出る素材）** | **194点** | **226カット** | | |
| 合成レイヤー（particle/light/vfx） | 10–16本 | — | 重ね掛け | **distinct 素材に数えない**（§9） |

**SDXL の生成バッチ（本編カットに出ない i2v 種を含む）:**

| 用途 | 点数 | 生成 |
|---|---|---|
| body 静止画（`role:"body"`） | **85枚** | 85プロンプト × 1枚（バリエーション0） |
| i2v 種画像（`role:"i2v_source"`・body と別 asset） | **16枚** | 16種プロンプト × 1枚（バリエーション0） |
| **SDXL 生成バッチ合計** | **85 + 16 = 101枚（各1回）** | **`--variants 1`** |

> **サムネは新規生成しない。** 完成後に body 85枚から6枚を `also_thumb:true` で流用選抜（追加生成ゼロ＝1シーン1枚前提を崩さない）。

> **★紙芝居回避（EP40 の最大の失敗）:** EP40 は静止画100%で `check_animation_mix` に FAIL した。EP42 は **still-cut 101 / (factory 93 + i2v 32)=video 125** で **still-share 44.69% ≤45%・motion coverage 55.31% ≥45%** を構造的に保証する（§3.3）。**stillを増やしてfactoryを削るな。factory 93 が still-share≤0.45 を守る下限。**

## 3.2 still 85枚・factory 93本・i2v 16本の幕別配分（目安）

| 区間 | narration秒 | still（S番号） | factory | i2v |
|---|---|---|---|---|
| HOOK | 20.9 | 4（S01–S04） | 6 | 2 |
| OPENING NARRATION | 18.5 | 2（S05–S06） | 3 | 0 |
| ACT1 THE WRONG DOOR | 101.4 | 15（S07–S21） | 16 | 4 |
| ACT2 THE TAPE | 95.0 | 14（S22–S35） | 18 | 2 |
| ACT3 THE COMMAND | 221.3 | 24（S36–S59） | 22 | 4 |
| ACT4 THE REACH | 107.5 | 14（S60–S73） | 16 | 2 |
| ENDING | 111.5 | 12（S74–S85） | 8 | 2 |
| 繋ぎ（covers_scene_id:null） | — | — | 4 | — |
| **合計** | **720.9** | **85** | **93** | **16** |

> ACT3 は他幕の約2倍の尺（ドクトリン核・最も遅く荘厳）なので still も最多の24枚。
> **★幕別の factory 内訳（この表・§7.2・CODEX_B §5.3）は非拘束の目安値**（合計 93 のみ確定・幕割当は柔軟）。ゲートは factory を各1回・合計 93 でしか見ないので、幕別配分の数字が3ドキュメント間で多少ずれても実害はない。**確定値は「合計 factory 93」だけ。**

## 3.3 全体の検算（★Codex は自分で再計算して一致を確認）

```
[1] 総カット数 226 = still 101 + factory 93 + i2v 32
[2] 平均ショット長 = (733.4 − OPENING 3.5 − ENDCARD 9.0) / 226 = 720.9/226 = 3.19秒/カット  ✓ (SPEC mean_shot 3.19・≤6.0)
[3] 静止画占有率(check_animation_mix) = 101/226 = 44.69%  ✓ ≤45%（SPEC still_share 0.4469）
[4] motion coverage = (93+32)/226 = 125/226 = 55.31%     ✓ ≥45%（SPEC 0.553）
[5] per-asset 上限: still 101/85=1.19(≤2) / factory 93/93=1.0(≤1) / motion 32/16=2.0(≤2)  ✓
[6] first-use share = 194/226 = 0.8584                   ✓ ≥0.70（SPEC 一致）
[7] factory 下限: video を 125 カット以上に保たないと still-share が 0.45 を超える。
    i2v 32 は固定なので factory は 93 を下回れない（93+32=125）。→ factory 93 は下限であり水増しではない。
```

> **[3] の余裕は 0.31% しかない。** still が85本を割ったら §6.3 の再生成で回復させ、**still-cut 101 を増やさない**（B側の shotlist が101で固定）。

---

# 4. ★境界契約: `asset_manifest.v001.json`（AとBを繋ぐ唯一のファイル）

**パス:** `episodes/PD-2026-042-young/05_visuals/asset_manifest.v001.json`
**スキーマ版:** `young_assets.v1`（固定文字列）
**生産者:** `scripts/build_young_asset_manifest.py`（**A が実装。他の誰もこのファイルを書かない**）

## 4.1 スキーマ（EP41 の `thompson_assets.v1` と同型。counts を EP42 値に）

```jsonc
{
  "schema_version": "young_assets.v1",
  "episode_id": "PD-2026-042-young",
  "slug": "young",
  "generated_at": "<ISO8601>",
  "producer": "scripts/build_young_asset_manifest.py",
  "is_stub": false,
  "counts": {
    "still_body": 85,          // >=85
    "still_i2v_source": 16,    // >=16
    "motion": 16,              // >=16
    "factory": 93,             // >=93
    "overlay": 12              // >=10（distinct 素材に数えない）
  },
  "stills": [{
    "asset_id": "YOUNG-S01",               // ^YOUNG-S\d{2}$（body 1..85） / i2v種は ^YOUNG-MS\d{2}$
    "scene_id": "S01",                     // still 資産 ID（§5.9 のプロンプト行に対応）
    "role": "body",                        // body|i2v_source|reject（バリエーション概念なし＝各1枚）
    "also_thumb": false,                   // body から6枚だけ true（追加生成しない）
    "act": 0,                              // 0=HOOK/1..4=幕/5=ED
    "path": "H:/pd-media/assets/ai/young/S01.png",
    "depth_path": "H:/pd-media/assets/ai/young/S01_depth.png",   // role=="body" は実在必須
    "public_path": "young/img/S01.png",    // role=="body" のみ非null
    "width": 3840, "height": 2160,         // 長辺>=3840
    "sha256": "<64hex>", "phash": "<16hex>", "mean_luma": 42.7,
    "tags": ["door","splinter","symbolic","night"],
    "caption_hint": "the door caves in",   // check_young_facts 検査対象（制約1-6）
    "seed": 0, "model": "juggernautXL_ragnarokBy",
    "source": "ai_codex", "commercial_use": "allowed", "ai_disclosure_required": true,
    "qc": {"reviewed": true, "on_theme": true, "has_readable_text": false,
           "has_identifiable_face": false, "has_human_body": false, "notes": ""}
  }],
  "motion": [{
    "asset_id": "YOUNG-M01",               // ^YOUNG-M\d{2}$（1..16）
    "source_scene_id": "M01_src",
    "source_still": "H:/pd-media/assets/ai/young/M01_src.png",   // role=="i2v_source" の画像
    "path": "H:/pd-media/assets/ai_video/young/M01_rife.mp4",
    "public_path": "young/motion/M01_rife.mp4",
    "act": 0, "width": 1280, "height": 720, "fps": 48, "frames": 164, "duration_sec": 3.417,
    "sha256": "<64hex>", "tags": ["door","caves_in"],
    "qc": {"reviewed": true, "on_theme": true, "artifact_free": true,
           "has_identifiable_face": false, "notes": ""}
  }],
  "factory": [{
    "asset_id": "AF-BG-0731",              // 棚 assets/asset_manifest.v001.json の id をそのまま
    "path": "H:/pd-media/assets/factory/backgrounds/AF-BG-0731__...mp4",
    "public_path": "young/factory/AF-BG-0731__...mp4",
    "type": "backgrounds", "subtype": "<label>",   // ★ラベル=検索語の記録。中身の保証ではない（§7.5）
    "kind": "video", "license": "Pexels License",  // ALLOWED_LICENSES のいずれか
    "sha256": "<64hex>", "act": 1, "covers_scene_id": "S07",  // §7.3 の割当のみ。繋ぎは null
    "duration_sec": 7.60, "width": 1920, "height": 1080, "mean_luma": 48.3,
    "eyeballed_content": "a Chicago apartment block at night, wide static, lit windows, no people",  // ★必須（§7.5）
    "qc": {"reviewed": true, "on_theme": true, "no_watermark": true,
           "no_recognizable_person": true, "no_cartoon": true, "label_matches_content": true, "notes": ""}
  }],
  "overlay": [{
    "asset_id": "AF-PART-0044", "path": "H:/.../particle_assets/...mp4",
    "public_path": "young/overlay/...mp4", "type": "particle_assets", "subtype": "<label>",
    "license": "Pexels License", "sha256": "<64hex>", "blend_hint": "screen",
    "eyeballed_content": "slow dust motes drifting on black, loops cleanly",
    "qc": {"reviewed": true, "on_theme": true, "no_watermark": true, "notes": ""}
  }]
}
```

## 4.2 `--verify` の不変条件（BLOCKING）

1. `schema_version=="young_assets.v1"` / `episode_id`/`slug` 一致 / `is_stub==false`
2. `counts.*` が各配列の実長と完全一致し §4.1 の下限を満たす
3. 全 `path`/`depth_path`/`public_path` がディスクに実在
4. `sha256` が全配列を通して一意（重複ゼロ）
5. `role!="reject"` の全静止画で `max(width,height)>=3840`
6. `role=="body"` は `depth_path` と `public_path` が非null かつ実在
7. `qc.has_readable_text==true` / `qc.has_identifiable_face==true` / `qc.has_human_body==true` のいずれかは `role=="reject"`
8. `role=="i2v_source"` は `role=="body"` と**同一 asset_id を共有しない**（distinct 分離。i2v_source は `YOUNG-MS\d{2}`）
9. 全JSON文字列が §1.3 の `BANNED_PORTRAIT` **および** `BANNED_ACCURACY` に一致しない
10. `factory[].license`/`overlay[].license` が `ALLOWED_LICENSES`（§7.4）に含まれる
11. `factory[].sha256` が **EP39・EP40・EP41 の staged 素材**と1件も衝突しない（§7.7）
12. `factory[].eyeballed_content` が空でない（＝目視していない本が混じっていない）
13. `factory[].qc.label_matches_content==true`
14. `also_thumb==true` の本数がちょうど6（追加生成ではなく body からの流用）

`--reuse-feasibility` では §3.3 [5][6][7] を再計算し、1つでも割ったら exit 1。

## 4.3 `role` の割り当て（機械的に決める）

```
1. body 85枚（S01..S85）= §5.9 の85プロンプトの生成物。各1枚。
2. i2v_source 16枚（MS01..MS16）= §8.1 の16種プロンプトの生成物。各1枚。body に回さない（不変条件8）。
3. also_thumb : body のうち S05 / S30 / S60 / S63 / S74 / S84 の6枚に true（追加生成しない）
4. reject : QCで落ちたもの（マニフェストに残し理由を qc.notes に）→ 落ちたシーンは §6.3 で同一プロンプト再生成
```

---

# 5. A-1: SDXL 静止画のバッチ生成（85本 × 1枚・バリエーション0）

## 5.1 生成環境（★既存の `generate_sdxl_4k.py` を使う）

```
API:   http://127.0.0.1:7860（ローカル AUTOMATIC1111・課金なし）
モデル: juggernautXL_ragnarokBy（generate_sdxl_4k.py が自動で set_model）
プロンプト元: episodes/PD-2026-042-young/04_scenes/ai_prompts.v001.md   ← A が §5.2 の形式で書く
出力:  H:\pd-media\assets\ai\young\S<NN>.png（+ remotion/public/young/ に自動コピー）
2段パイプライン: txt2img 1536x864 → hires 3072x1728 → extras R-ESRGAN 4x+ → 3840x2160（長辺≥3840・冪等スキップ）
```

**ローカルGPU生成に課金は発生しない。** 禁止は ElevenLabs TTS / 課金画像API / アップロードのみ（§12）。

## 5.2 ★パーサ契約（`read_prompts()` はこの2行形式しか読まない・実装確認済み）

正規表現 `^\s*-\s+` + バッククォート囲みの `<stem>.png` + 次行に `Avoid:` を含む1行:

```
- `S01.png`
<positive prompt> Avoid: <negative>
```

- **1行目:** `` - `S01.png` ``（バッククォート囲み・**行末は `.png` の直後**。プロンプトを同じ行に書かない）
- **2行目:** 正プロンプト → `Avoid:` → 負プロンプト（負は `DEFAULT_NEG` に自動連結される）
- **EP30 等の旧 `01. <prompt>` 形式は read_prompts() で読めない。** 必ず上記形式で書く。
- `ai_prompts.v001.md` は **body 85行（S01..S85）＋ i2v 種 16行（M01_src..M16_src、§8.1）＝ 101 エントリ**を書く。すべて1枚生成。

## 5.3 生成コマンド（★`--variants 1`。`--variants 3` は使わない）

```bash
# まず1枚だけ回して読める行数を確認（★shots=101 でなければ形式が壊れている）
./.venv/Scripts/python.exe scripts/generate_sdxl_4k.py 42 --variants 1 --only S01
#   → ログ "episode=... shots=101 variants=1 ... -> 101 images" の shots が 101 であること

# 全101枚（body 85 + i2v種 16・冪等・長辺>=3840 の既存はスキップ）
./.venv/Scripts/python.exe scripts/generate_sdxl_4k.py PD-2026-042-young --variants 1
#   → 生成 S01.png ... S85.png / M01_src.png ... M16_src.png（各1枚。_02/_03 は作らない）
```

> QC で落ちたシーンの再生成は `--only S37`（**同じプロンプトで別シードを1枚**）。既存の>=3840はスキップ・不足だけ埋まる。**バリエーションを増やして水増ししない。枚数を減らして基準を下げるのも禁止。**

## 5.4 共通スタイル `[STYLE]`（全プロンプト末尾に必ず全文連結）

```
, cinematic still, cold cinematic-documentary grade, deep midnight-blue and charcoal night with a single pool of warm tungsten domestic light, civic spaces in pale cold marble grey, restrained and dignified symbolism, telephoto compression and frontal composition, shallow depth of field, ultra-detailed, photoreal, 4K, 16:9, fine film grain, no text, no watermark, no logo, symbolic still-life, no people, no visible face
```

> **EP39/EP40/EP41 との分離:** `navy`/`electric blue`/`interrogation`（EP39）・`midday sunlight`/`suburban`/`bleached daylight`（EP40）・`prison cell`/`cellblock`/`sodium prison corridor`/`steel death-row`（EP41）を**1語も含めない**。EP42 は夜のシカゴの家庭内＋冷たい市民空間（大理石・法廷・議会）の対比。

## 5.5 共通ネガティブ `[NEG]`（各 `Avoid:` の後に必ず全文付ける）

```
text, words, letters, numbers, captions, watermark, logo, readable document, legible paper, legible check amount, real celebrity, recognizable real person, identifiable face, portrait, mugshot, likeness of a specific person, human face, human body, nude, undressed figure, bare skin, cartoon, illustration, anime, 3d render, low quality, blurry, jpeg artifacts, deformed, extra limbs, gore, blood, prison cell, steel cellblock, sodium prison corridor, navy interrogation room, electric blue, midday suburban daylight
```

> ネガティブにも **`no-knock`・`unconstitutional`・`she changed the law` を書かない**（制約2/3・§1.2）。上のリストにも含めていない。

## 5.6 バリエーション軸（★EP42 では無効）

`generate_sdxl_4k.py` の `--variants 1` は各 stem を**1枚だけ**生成する。**`_02`/`_03` を作らない。** 反復回避は「85本の固有プロンプト＝85の別被写体」で担保する（EP40 指摘「反復感の原因は総枚数ではなくシーン数」を、EP42 は distinct 85 で解決）。

## 5.7 メタJSON

`generate_sdxl_4k.py` は画像を書くが per-image メタJSONは書かない。**A は QC 時に `qc_young_stills.py` で各画像の `sha256`/`phash`/`mean_luma`/`long_edge` を測り `still_qc.v001.json` に記録する**（§6.2）。

## 5.8 プロンプトの絶対ルール（85本すべてに適用）

- **顔なし・身体なし・裸体なし。** 人物は原則出さない。出す場合は遠いシルエット/後ろ姿/影のみ（制約6・R1）。
- **可読文字なし。** 令状・小切手・投票掲示板・条例・判決文は雰囲気のみ（判読不能）。数値は描かない。
- **Young も Hudson も個人として描かない**（制約5/6）。Young＝家庭内の象徴オブジェ。Hudson＝Detroit の無名の戸口/敷居のみ。
- **和解＝責任認定に見せない**（制約1）: 小切手には過失欄が空白という象徴。判決の絵で「誰かが責任を負った」と読めるものを作らない。
- **改革否決**（制約3）: 条例は `set aside / stamped and pushed away` の象徴。「法が変わった」祝祭に見えるものを作らない。
- **Hudson の射程非圧縮**（制約4）: 「still a command」は壁を走る一条の光・閉じた戸口の尊厳で示す。ルールが消えた/廃止された絵を作らない。

## 5.9 確定プロンプト（★`ai_prompts.v001.md` にこの85エントリをそのまま書く・各1枚）

> 各行の `[STYLE]` は §5.4 を、`Avoid:` の後の `[NEG]` は §5.5 を**全文展開**して書く（下記は簡潔表記のマクロ。省略記号ではなく定義済み定数）。全て顔なし・身体なし・象徴・判読不能。

```
- `S01.png`
A wooden front-door frame splintering inward in the dark, cracked jamb and flying splinters frozen mid-break, a bare hallway floor beyond, the violence of an entry with no people shown [STYLE] Avoid: [NEG]
- `S02.png`
A round wall clock in a dark apartment at a late night hour, hands abstract and unreadable, faint warm lamp glow on the wall, the stillness before everything changes, no people [STYLE] Avoid: [NEG]
- `S03.png`
A single open handcuff lying on a bare wooden floor in cold night light, one steel ring swung apart, the object of restraint alone without any wrist, non-graphic and symbolic, no people [STYLE] Avoid: [NEG]
- `S04.png`
A work coat and an ID lanyard draped over the back of a kitchen chair in a dim apartment, just taken off after a long shift, the presence of a person implied only by the empty clothes, no body, no face [STYLE] Avoid: [NEG]
- `S05.png`
A plain residential front door seen straight on in cold hallway light, slightly worn, ordinary and closed, a slow push-in feeling, the everyday door the whole story turns on, no people, no readable number [STYLE] Avoid: [NEG]
- `S06.png`
A front door at the end of a corridor with a faint grid of light lines cast across the walls behind it, cold blue geometry, quiet anticipation, no people, no text [STYLE] Avoid: [NEG]
- `S07.png`
A modest Chicago West-Side apartment building exterior at night, a few warm windows lit among dark ones, wet asphalt reflecting streetlight, quiet and unremarkable, no people [STYLE] Avoid: [NEG]
- `S08.png`
Kitchen cabinet doors standing ajar in a small apartment, contents shifted and disturbed, a single warm bulb overhead, the aftermath of a search on ordinary shelves, no people, no readable labels [STYLE] Avoid: [NEG]
- `S09.png`
Papers scattered across a small apartment floor under cold night light, a life pulled apart, the documents blank and unreadable, quiet disorder, no people [STYLE] Avoid: [NEG]
- `S10.png`
A dark screen showing a stylised city map with a single glowing pin marking an electronic ankle-monitor location elsewhere in the city, cold blue cartography, the tracked man who was never here, abstract map, no readable place names [STYLE] Avoid: [NEG]
- `S11.png`
A folded legal document lying face-down on a table under a lamp, a judge's signature block reduced to an abstract illegible mark, a valid search warrant as a plain object, no readable words, no people [STYLE] Avoid: [NEG]
- `S12.png`
A metal apartment door number plate catching cold light, the digits deliberately blurred into abstraction, the wrong address that started everything, no people, no legible number [STYLE] Avoid: [NEG]
- `S13.png`
The splintered doorway seen from inside the dark apartment, cold light flooding through the broken gap, long hard shadows of unseen figures thrown across the floor, no faces, no bodies [STYLE] Avoid: [NEG]
- `S14.png`
Crossing flashlight beams cutting through the darkness of a small living room, cones of hard light over ordinary furniture, the machinery of a raid rendered as light alone, no people [STYLE] Avoid: [NEG]
- `S15.png`
A single steel handcuff clasped shut and resting on a bare table in cold light, the ring closed on nothing, restraint as a symbol without any person, non-graphic, no body [STYLE] Avoid: [NEG]
- `S16.png`
A close crop of a police body-worn camera clipped to a dark vest, a tiny red recording light glowing, framed at chest level so no face appears, the silent witness that keeps recording, no visible face [STYLE] Avoid: [NEG]
- `S17.png`
An overturned kitchen chair and a dropped shoulder bag on an apartment floor in cold night light, ordinary objects knocked askew, the disorder of an interrupted evening, no people [STYLE] Avoid: [NEG]
- `S18.png`
A coat fallen to the floor beside an open closet in a dim bedroom, the door of the closet ajar, the abrupt undoing of a private moment suggested only by objects, no body, no face [STYLE] Avoid: [NEG]
- `S19.png`
A half-closed office drawer holding a single memory card and a sealed evidence sleeve under cold light, the place a recording is quietly put away, no readable label, no people [STYLE] Avoid: [NEG]
- `S20.png`
A small apartment living room ringed by the tall shadows of standing figures thrown on the walls, only silhouettes and shadow, a person surrounded implied without any body shown, no faces [STYLE] Avoid: [NEG]
- `S21.png`
An apartment front door left standing open after everyone has gone, cold empty hallway light beyond, the quiet wreck of a night, no people [STYLE] Avoid: [NEG]
- `S22.png`
A manila folder sealed shut with a string clasp resting on a dark desk under one lamp, the closed record no one wants opened, no readable text, no people [STYLE] Avoid: [NEG]
- `S23.png`
A long marble courthouse corridor at night, empty and cold, columns receding into shadow, the institution asleep, no people, no readable inscription [STYLE] Avoid: [NEG]
- `S24.png`
A single document lying under cold light with heavy black redaction bars covering the lines, the text beneath completely unreadable, the truth withheld, no legible words, no people [STYLE] Avoid: [NEG]
- `S25.png`
A neat stack of complaint forms squared on a desk beneath a lamp, the printed lines abstract and illegible, the paperwork of asking the system to listen, no readable text, no people [STYLE] Avoid: [NEG]
- `S26.png`
A lawyer's desk at night with an open case file, a pen laid across it and a single lamp, the labour of one person against a city, no face, no legible text [STYLE] Avoid: [NEG]
- `S27.png`
A television set glowing in a dark living room, the screen an abstract field of cold light with no discernible image, the moment a private night becomes public, no people, no text [STYLE] Avoid: [NEG]
- `S28.png`
A remote control resting on the arm of a couch bathed in the flickering blue light of an unseen television, an ordinary room lit by news, no people [STYLE] Avoid: [NEG]
- `S29.png`
A dark room filled edge to edge with the pale grainy glow of a television screen, light spilling over bare walls, the whole country suddenly standing inside one apartment, no discernible image, no people [STYLE] Avoid: [NEG]
- `S30.png`
A wide view of a city block at night with countless lit apartment windows, each a household watching the same screen, cold blue with warm pinpoints, no people [STYLE] Avoid: [NEG]
- `S31.png`
An empty press-conference podium with a cluster of microphones under cold light, the vacant place where an apology is given, no people, no readable signage [STYLE] Avoid: [NEG]
- `S32.png`
A dense bank of news microphones on a stand seen against a dark backdrop, a forest of black metal, the sudden weight of public attention, no people, no logos [STYLE] Avoid: [NEG]
- `S33.png`
A frosted-glass office door of an oversight agency lit from within at night, the lettering on the glass abstract and unreadable, the machinery of an investigation behind it, no legible sign, no people [STYLE] Avoid: [NEG]
- `S34.png`
A wall of stacked evidence and case boxes in a dim records room, dust in a shaft of light, the volume of an investigation, no readable labels, no people [STYLE] Avoid: [NEG]
- `S35.png`
A wall calendar in a dim office with many pages caught mid-turn, dates blurred into abstraction, sixteen months of waiting compressed into one image, cold light, no legible numbers, no people [STYLE] Avoid: [NEG]
- `S36.png`
A single indistinct band of engraved-looking text running as a stripe of pale light across a cold marble wall, the characters abstract and unreadable, a constitutional sentence rendered as light, no legible words, no people [STYLE] Avoid: [NEG]
- `S37.png`
The interior of a grand marble high-court chamber photographed frontally, monumental columns and cold pale stone, solemn and empty, no people, no readable inscription [STYLE] Avoid: [NEG]
- `S38.png`
A long judicial bench with nine tall vacant high-backed seats behind it in cold marble light, monumental and unmoved, the absent deciders, no people [STYLE] Avoid: [NEG]
- `S39.png`
A wooden gavel resting unused on its sound block on an empty bench under cold light, the instrument of a ruling lying still, no people, no text [STYLE] Avoid: [NEG]
- `S40.png`
A generic worn residential doorway and threshold in an old neighbourhood at night, a plain door in a brick wall, an anonymous Detroit entry shown only as a symbolic threshold, no people, no readable number [STYLE] Avoid: [NEG]
- `S41.png`
A closed but unlocked door opened only a hand's width, a sliver of dark room beyond, the fragile pause between a knock and an entry, no people, no text [STYLE] Avoid: [NEG]
- `S42.png`
A clock or stopwatch face marking only a few seconds elapsed, the numerals abstract and unreadable, the three-to-five seconds that were not long enough, cold light, no legible numbers, no people [STYLE] Avoid: [NEG]
- `S43.png`
An old front door standing ajar with only darkness beyond the threshold, cold light along the door edge, the moment of entry held as a quiet symbol, no people [STYLE] Avoid: [NEG]
- `S44.png`
A stark marble surface divided by a single hard line of shadow into a larger and a smaller side, cold light, a division rendered without any faces or numbers, severe and abstract, no people, no text [STYLE] Avoid: [NEG]
- `S45.png`
Macro of the corner of a legal opinion page on a dark desk, one block of unreadable text isolated in a pool of light while the rest falls to shadow, no legible words, no people [STYLE] Avoid: [NEG]
- `S46.png`
An empty judicial bench seen frontally with one lit lectern below it and a stack of pages, the reading of an opinion implied by absence, cold institutional light, no people, no legible text [STYLE] Avoid: [NEG]
- `S47.png`
A set of brass justice scales standing in deep shadow, one pan hanging slightly lower than the other, cold rim light on the metal, balance rendered abstract, no people, no text [STYLE] Avoid: [NEG]
- `S48.png`
A sealed evidence bag left resting on a courtroom table under cold light, deliberately not removed, the thing found inside that stays in the case, contents indistinct, no readable label, no people [STYLE] Avoid: [NEG]
- `S49.png`
A tall courthouse door standing open onto a bright corridor, cold marble, the one door still open, an invitation and a burden both, no people, no readable sign [STYLE] Avoid: [NEG]
- `S50.png`
A single folded banknote lying on a bare dark table under one hard light, denomination illegible, money placed on the table as the only remedy left, no legible numbers, no people [STYLE] Avoid: [NEG]
- `S51.png`
A single high-backed chair set slightly apart from a long empty bench in a marble chamber, one seat standing separate from the row, a concurrence apart from the rest, no people [STYLE] Avoid: [NEG]
- `S52.png`
A small sheaf of pages held slightly apart from a thick closed folder on a dark desk, the dissent set beside the majority, cold light, no legible text, no people [STYLE] Avoid: [NEG]
- `S53.png`
The spine of a heavy old statute volume on a shelf in cold light, the title abstract and unreadable, the single remaining remedy written into law, no legible text, no people [STYLE] Avoid: [NEG]
- `S54.png`
Two case folders laid on a table under one lamp, one labelled abstractly as a criminal matter and one as a civil matter, a hand-width apart, the deterrent moving from one to the other, no legible text, no people [STYLE] Avoid: [NEG]
- `S55.png`
A long cold marble corridor receding toward a single bright doorway far ahead, the narrow remedy that remains at the end of a long walk, no people, no text [STYLE] Avoid: [NEG]
- `S56.png`
A single thin line of pale light on a dark marble wall beginning to fade at one end, a command still present but with little behind it, quiet and severe, no people, no legible text [STYLE] Avoid: [NEG]
- `S57.png`
Weathered constitutional-looking engraving on a slab of pale stone lit from a low angle, the individual characters abstract and unreadable, cold and monumental, no legible words, no people [STYLE] Avoid: [NEG]
- `S58.png`
An empty witness lectern standing alone in a vast cold chamber, a single microphone turned toward it, the burden that falls on the ordinary person, no people, no readable text [STYLE] Avoid: [NEG]
- `S59.png`
A lone leather briefcase set on the marble floor before tall closed chamber doors, cold light, the private citizen who must hire the lawyer, no people, no text [STYLE] Avoid: [NEG]
- `S60.png`
A printed settlement check lying on a polished table under warm-cold mixed light, the amount field deliberately abstract and unreadable, money offered in place of a verdict, no legible numbers, no people [STYLE] Avoid: [NEG]
- `S61.png`
A formal printed page on a desk with a single conspicuously blank line where a finding of fault would be signed, the emptiness where an admission should sit, no legible text, no people [STYLE] Avoid: [NEG]
- `S62.png`
A city council chamber interior with an empty speaker's podium facing rows of vacant seats, cold civic light, the room where a vote is taken, no people, no readable signage [STYLE] Avoid: [NEG]
- `S63.png`
An electronic vote tally board mounted on a chamber wall, the indicator lights and numerals abstract and unreadable, an approval recorded as reported, no legible numbers, no people [STYLE] Avoid: [NEG]
- `S64.png`
A printed ordinance document stamped and set aside at the edge of a desk under cold light, a reform named for a person pushed to one side, the text illegible, no legible words, no people [STYLE] Avoid: [NEG]
- `S65.png`
A rubber stamp resting on its side beside an unread page on a dark desk, ink dried, a decision made and closed, no legible text, no people [STYLE] Avoid: [NEG]
- `S66.png`
Two empty chairs facing each other across a bare settlement table under one lamp, the deal struck in an empty room, quiet and transactional, no people, no text [STYLE] Avoid: [NEG]
- `S67.png`
An empty disciplinary hearing room with a long table and a blank nameplate turned face-down, cold institutional light, a proceeding without any person shown, no legible name, no people [STYLE] Avoid: [NEG]
- `S68.png`
A vacated office chair pushed back from a desk with a police badge left lying on the blotter, cold light, one departure among many who stayed, no face, no legible text [STYLE] Avoid: [NEG]
- `S69.png`
A row of closed personnel folders standing on a shelf in cold light, all kept shut, the many who kept their jobs and pensions, no legible labels, no people [STYLE] Avoid: [NEG]
- `S70.png`
A committee-room table with a gavel and a single rejected page pushed to the far edge, cold civic light, a measure set aside, no legible text, no people [STYLE] Avoid: [NEG]
- `S71.png`
A stamped document lying face-down and unopened on a committee desk, never carried forward, cold light, the reform that never reached the floor, no legible words, no people [STYLE] Avoid: [NEG]
- `S72.png`
A closed ordinance binder standing on a municipal shelf gathering a faint film of dust, the old practice still on the books, cold light, no legible spine text, no people [STYLE] Avoid: [NEG]
- `S73.png`
A quiet municipal hallway at dusk with rows of closed office doors, cold fading light, the machinery of the city gone still, no people, no readable signage [STYLE] Avoid: [NEG]
- `S74.png`
The same modest residential front door from the opening, now closed and quiet in the dark, undisturbed, the story returning to where it began, no people, no readable number [STYLE] Avoid: [NEG]
- `S75.png`
A thin line of warm dawn light glowing along the bottom edge of a closed front door in a dark hallway, morning arriving on the far side, quiet and unresolved, no people [STYLE] Avoid: [NEG]
- `S76.png`
The wall clock again in the grey of very early morning, hands abstract and unreadable, the long night finally over, faint cold light, no people, no legible numbers [STYLE] Avoid: [NEG]
- `S77.png`
A settlement check lying on a table catching the first pale light of dawn, the amount abstract and unreadable, money that admits nothing, no legible numbers, no people [STYLE] Avoid: [NEG]
- `S78.png`
A single sheet of paper on a windowsill at dawn with a blank space where an admission of wrong would be, soft morning light across it, the sentence never written, no legible text, no people [STYLE] Avoid: [NEG]
- `S79.png`
A stamped and set-aside reform page resting on a windowsill in cold dawn light, pushed away and unsigned, the change that did not come, no legible words, no people [STYLE] Avoid: [NEG]
- `S80.png`
A single faint line of light on a bare wall at dawn with deep empty space around it, a rule still standing with almost nothing behind it, quiet and severe, no people, no text [STYLE] Avoid: [NEG]
- `S81.png`
A dark camera lens in close-up reflecting a dim room, cold rim light on the glass, the recording eye that finally made a private truth believed, no face, no people [STYLE] Avoid: [NEG]
- `S82.png`
A single closed door at the far end of a long hall in cold dawn light, unopened, the door that never opened, quiet and final, no people, no text [STYLE] Avoid: [NEG]
- `S83.png`
A residential front-door threshold at first light, the sill catching pale morning, the ordinary boundary of a home restored to quiet, no people, no readable number [STYLE] Avoid: [NEG]
- `S84.png`
A single window with the last deep blue of night shifting to the first grey of dawn over a quiet city skyline, one warm room among many, open-ended, no people, no visible address [STYLE] Avoid: [NEG]
- `S85.png`
A closed residential front door with warm light beginning to return around its edges, a slow pull-back composition, quiet and unresolved, the door of a home at the end of everything, no people, no readable number [STYLE] Avoid: [NEG]
```

**枚数チェック:** 上記 85 エントリ（S01..S85）。§5.3 の `--only S01` ログで `shots=101`（body 85 + i2v種 16）を確認してから本番を回す。

---

# 6. A-2/A-3: 静止画のQC・目視・depth map

## 6.1 機械QC（body 85 + i2v種 16 = 全101枚・`qc_young_stills.py`）

| # | 検査 | 判定 | 落ちたら |
|---|---|---|---|
| Q1 | 解像度 | `max(w,h)>=3840` | reject |
| Q2 | サイズ/開ける | `>1024 bytes` かつ PIL で開ける | reject |
| Q3 | 平均輝度 | `35.0<=mean_luma<=225.0`（EP42は夜のエピソード→黒潰れ側が本命リスク。`check_visual_asset_qc.DARK_LUMA_FLOOR=45.0` を下回りすぎる本に注意） | reject |
| Q4 | 近似重複 | 全ペア phash。類似度 `>=0.90` は片方 reject（`check_visual_asset_qc.NEARDUP_SIM=0.90`）。**バリエーション0なので本来ほぼ衝突しないはず。衝突したらプロンプトが被っている** | 片方 reject＋プロンプト見直し |
| Q5 | 文字の混入 | **目視。** 読める英字・数字・ロゴ・小切手金額・投票数が写っていないか（制約1-3） | `has_readable_text=true`→reject |
| Q6 | 顔の混入 | **目視。** 識別可能な顔が写っていないか（R1・制約5/6） | `has_identifiable_face=true`→reject |
| Q7 | 身体の混入 | **目視。** 人体・裸体が写っていないか（制約6） | `has_human_body=true`→reject |

**Q5/Q6/Q7 は機械で判定しない。** コンタクトシートを出して**全101枚を実際に目視**する:

```bash
./.venv/Scripts/python.exe scripts/build_footage_contact_sheet.py --ep PD-2026-042-young --media image
#   → runs/qc/young_footage_contact_NN.png（20枚/シート）。全シートを開いて1枚ずつ見る
```

> **EP38/EP39-41 の教訓: ファイル名・プロンプトを信じるな。生成物を実際に見ろ。** 「S24 は redacted だからテキストは判読不能のはず」は根拠にならない。SDXL は平気で読める文字・顔・身体を描く。**特に制約6（Young 非グラフィック）・制約5（Hudson 非人物化）は目視でしか守れない。**

## 6.2 出力

```
episodes/PD-2026-042-young/05_visuals/still_qc.v001.json     # 101枚全部の行（reject も残す・sha256/phash/mean_luma/long_edge）
（build_footage_contact_sheet が runs/qc に出す）
```

## 6.3 accepted が101枚に届かなかったとき

```bash
./.venv/Scripts/python.exe scripts/generate_sdxl_4k.py 42 --variants 1 --only S37   # 落ちたシーンだけ同一プロンプトで別シード1枚
./.venv/Scripts/python.exe scripts/qc_young_stills.py
```
accepted body >= 85 かつ i2v_source >= 16 になるまで繰り返す。**基準を下げない・バリエーションを足して水増ししない。**

## 6.4 depth map（★新規スクリプトを作らず既存を使う）

```bash
./.venv/Scripts/python.exe scripts/gen_depth_maps.py --dir "H:/pd-media/assets/ai/young"
```
- モデル `Intel/dpt-large`。出力 `<stem>_depth.png`（同サイズ L グレースケール）。冪等。
- **role が `body` の静止画は depth 必須**（`treatment:"depth"` が隣に `_depth.png` を要求。無いとレンダーがクラッシュ）。i2v 種（`M<NN>_src.png`）は depth 不要。
- staging 後に `remotion/public/young/img/` 側でも同名ペアが揃っていること（§10）。

---

# 7. A-4: factory 実写クリップ 93本の選定と全点目視QC

## 7.1 在庫の実態

```
H:\pd-media\assets\factory\   フラット構成
  backgrounds/     11,000本超（.mp4）  ← ★主力（Chicago夜景・市民建築・法廷/議会・廊下・記録庫・空・繋ぎ）
  light_assets/    …            合成レイヤー（光条）
  particle_assets/ …            合成レイヤー（埃・塵）
  vfx_overlays/    …            合成レイヤー（グレイン・煙）
  texture_assets/  …            紙・石・大理石のテクスチャ
  loops/           …            抽象的な繋ぎ
ファイル名規約: AF-<TYPECODE>-<4桁>__<subtype_slug>.<ext>（TYPECODE = BG|LIGHT|LOOP|PART|TEX|VFX）
棚レジストリ: C:\Users\aab15\Documents\prime-documentary\assets\asset_manifest.v001.json
   （トップキーは schema と assets。★必ず encoding="utf-8" で開く。cp932 既定だと落ちる）
```

## 7.2 選定条件

- **`kind=="video"` のみ。** 静止画 factory は使わない
- **93本ちょうど**（§3.3[7] より 93 は still-share≤0.45 を守る下限。減らせない）
- **各1回しか使わない**（`check_asset_reuse.MAX_USES_FACTORY=1`）
- 幕別割り当て（§3.2）: HOOK=6 / ACT1=16 / ACT2=18 / ACT3=22 / ACT4=16 / ED=8 ＋ 繋ぎ=7 ＝ 93
- **EP39（夜/取調室/青）・EP40（郊外/昼/破壊）・EP41（監獄/鉄/石の独房）の絵柄を選ばない。** EP42 は都市の夜＋家庭内＋市民空間（大理石の法廷・議会・記録庫・夜〜夜明けの街）

**既存の選定ツールで候補出し（新規に検索ロジックを書くな）:**

```bash
./.venv/Scripts/python.exe scripts/select_factory_assets.py --themes   # テーマ一覧と件数
./.venv/Scripts/python.exe scripts/select_factory_assets.py \
    --kind video --query courthouse --limit 96 --exclude-used --ep PD-2026-042-young --json
```
`--exclude-used` は `check_arc_nonrepeat.build_universe()` と同じ指紋集合を使うので出荷ゲート `arc_nonrepeat` と食い違わない。**必ず付ける。**

## 7.3 実写在庫でカバーする代表シーン（`covers_scene_id` を付ける・SDXLで作らない情景）

> **★`covers_scene_id` は still 資産 ID 空間（S01..S85・§2 注記）を指す。narrative シーン（DESIGN の S01..S48）とは別体系。** B はこの値を still 資産 ID として解決し、narrative シーンコードにクロスマップしない。

| covers | 内容 | `--query` 例 | 幕 |
|---|---|---|---|
| S07 | シカゴ西部アパート外観（夜・引き） | `apartment_building_night` / `city_apartment_night` | 1 |
| S23 | 大理石の法廷/裁判所廊下（無人） | `courthouse_interior` / `marble_corridor` | 2 |
| S30 | 夜の街・多数の灯る窓 | `city_windows_night` / `apartment_lights_night` | 2 |
| S33 | 官公庁/監督機関の建物（夜） | `government_building_night` / `office_building_night` | 2 |
| S37 | 最高裁/大法廷ファサード・列柱 | `supreme_court_building` / `marble_columns` | 3 |
| S40 | Detroit の古い戸口/街路（象徴・人物なし） | `old_doorway_night` / `brick_row_house_night` | 3 |
| S55 | 大理石の長い廊下 | `marble_hallway` / `long_corridor_institutional` | 3 |
| S62 | 市議会/公会堂の議場（無人） | `council_chamber` / `assembly_hall_empty` | 4 |
| S73 | 官庁の廊下・閉じたドア（夕） | `office_hallway_dusk` / `government_corridor` | 4 |
| S84 | 夜明けの街のスカイライン | `city_dawn_skyline` / `blue_hour_city` | 5 |

**残り本数は covers を持たない繋ぎ・情景クリップ**（`covers_scene_id:null`）: 市民建築の外観・大理石/石の廊下・空の椅子・記録庫・夜〜夜明けの空・雨のアスファルト・冷たい窓・抽象 `loops`。**暗いクリップに偏りすぎない**（§7.5 の暗側閾値・全体の1/3=約31本まで）。

## 7.4 ライセンス（`ALLOWED_LICENSES` — これ以外選ばない）

```python
ALLOWED_LICENSES = {"cc0","royalty_free","generated_owned","Pexels License","Pixabay Content License"}
```

## 7.5 ★★★ factory のファイル名とサブタイプは信用できない ★★★

> **推測ではなく実際に起きた事故。** EP36: `city_surveillance_camera_dome` が大聖堂。EP38: 牛が `documents_on_desk`。`subtype` は「その検索語で取った」記録であって**中身の保証ではない**。

**選抜93本は例外なく次を経る:**

```bash
# 1) 選定した93本を staging フォルダに集め、ラベル付きコンタクトシートを出す
./.venv/Scripts/python.exe scripts/build_footage_contact_sheet.py \
    --ep PD-2026-042-young --media video --dir "<93本の staging フォルダ>"
#   → runs/qc/young_footage_contact_NN.png（各タイルにファイル名ラベル）
```

2. **コンタクトシートを実際に開き、93本すべてを1本ずつ見る**
3. 各本について `asset_manifest.v001.json` の **`eyeballed_content` に「実際に見た内容」を1文の英語で書く**（ファイル名の言い換え禁止）。`subtype` と食い違ったら `label_matches_content:false` を立てて**選定から外す**
4. 実写シネマティックB-roll（アニメ/CG臭排除）・EP42テーマ（都市の夜/市民空間/家庭内/大理石）・ウォーターマークなし・識別可能な実在人物なし（制約6・R1）を確認
5. `05_visuals/factory_clip_qc.v001.json` を固定タイムスタンプで原子的に書く（冪等）

閾値（`check_visual_asset_qc.py`）: `DARK_LUMA_FLOOR=45.0` / `MAX_DARK_FRACTION=0.40` / `NEARDUP_SIM=0.90` / `MIN_VARIETY=0.60`。
> **EP42 は夜のエピソードなので暗側が本命リスク。** 平均輝度45未満のクリップが全体の40%を超えると FAIL。**暗いクリップは約31本（1/3）までに抑え、街灯や室内実用光がある本を優先する。**

**1フレームで判断がつかない本は VLC/ffplay で再生して確認**（near-still は `check_animation_mix` を落とす）。

## 7.6 出力

```
episodes/PD-2026-042-young/05_stock/factory_selection.v001.json   # 選定理由と幕割り当て
episodes/PD-2026-042-young/05_visuals/factory_clip_qc.v001.json   # ゲートが読む reviewed マニフェスト
```

## 7.7 EP39/EP40/EP41 との重複ゼロ（BLOCKING）

```bash
./.venv/Scripts/python.exe scripts/select_young_factory.py --verify-no-prior-overlap
```
`episodes/PD-2026-039-*/` `episodes/PD-2026-040-*/` `episodes/PD-2026-041-*/` の `05_stock/stock_ledger*.json`（および `05_visuals/asset_manifest*.json` があれば）を**読み取り専用で**開き、`sha256` 集合と EP42 の93本の積集合が**空**であることを確認。1件でも exit 1 で差し替え。**EP39/EP40/EP41 のファイルは読むだけ。書き込み・移動・削除は一切しない。**

---

# 8. A-5: i2v モーション化 16本（Wan 2.2 A14B → RIFE 48fps）

## 8.1 i2v にする16本（動きが意味を持つ絵・各1枚の種プロンプト・バリエーション0）

種画像は §5 と同じ `generate_sdxl_4k.py --variants 1` で `M<NN>_src.png` として生成する（`ai_prompts.v001.md` に下記16行を追加）。**`role:"i2v_source"` として専用確保し body に回さない**（§4.2 不変条件8）。

| # | asset_id | 種画像 | 動きの意味 | act |
|---|---|---|---|---|
| 1 | YOUNG-M01 | M01_src | 戸口が内側へ割れて崩れる | 0 |
| 2 | YOUNG-M02 | M02_src | 深夜の時計の針が進む | 0 |
| 3 | YOUNG-M03 | M03_src | 地図上の足首モニタのピンが脈打つ | 1 |
| 4 | YOUNG-M04 | M04_src | 暗い部屋を懐中電灯の光条が薙ぐ | 1 |
| 5 | YOUNG-M05 | M05_src | ボディカメラの赤い録画ランプが点滅 | 1 |
| 6 | YOUNG-M06 | M06_src | 開いた玄関ドアに冷たい光が差す | 1 |
| 7 | YOUNG-M07 | M07_src | 暗い部屋でテレビの光がちらつく | 2 |
| 8 | YOUNG-M08 | M08_src | 黒塗りバーが文面の上に落ちて覆う | 2 |
| 9 | YOUNG-M09 | M09_src | 大理石の壁を一条の光が横切る（still a command） | 3 |
| 10 | YOUNG-M10 | M10_src | 無人の大法廷に埃が舞う | 3 |
| 11 | YOUNG-M11 | M11_src | 施錠されていない扉が手幅だけ開いて待つ | 3 |
| 12 | YOUNG-M12 | M12_src | テーブル上の紙幣が光を受けて微動 | 3 |
| 13 | YOUNG-M13 | M13_src | 小切手が机に滑り込み、ペンが置かれる | 4 |
| 14 | YOUNG-M14 | M14_src | 投票掲示板の表示が静かに確定する（数値なし） | 4 |
| 15 | YOUNG-M15 | M15_src | 閉じたドアの下に夜明けの光が広がる | 5 |
| 16 | YOUNG-M16 | M16_src | 窓の外の最後の青が夜明けへ移る | 5 |

### 8.1a i2v 種プロンプト（★`ai_prompts.v001.md` の末尾にこの16行を追加・各1枚）

```
- `M01_src.png`
A wooden front-door frame beginning to splinter inward in the dark, a plain hallway beyond, poised at the instant of breaking, no people [STYLE] Avoid: [NEG]
- `M02_src.png`
A round wall clock on a dark apartment wall at a late hour, faint warm lamp glow, the hands abstract, quiet before motion, no people, no legible numbers [STYLE] Avoid: [NEG]
- `M03_src.png`
A dark screen showing a stylised cold-blue city map with a single glowing location pin, abstract cartography, the tracked point elsewhere, no readable place names, no people [STYLE] Avoid: [NEG]
- `M04_src.png`
A dark small living room crossed by hard cones of flashlight light over ordinary furniture, a raid shown as light alone, no people [STYLE] Avoid: [NEG]
- `M05_src.png`
A police body-worn camera clipped to a dark vest with a small red recording light, chest-level crop, no face, the silent witness, no visible face [STYLE] Avoid: [NEG]
- `M06_src.png`
An apartment front door standing open with cold light spilling across a dark floor, the aftermath of an entry, no people [STYLE] Avoid: [NEG]
- `M07_src.png`
A television glowing in a dark living room, an abstract field of cold flickering light with no discernible image, the room lit by news, no people, no text [STYLE] Avoid: [NEG]
- `M08_src.png`
A document under cold light with heavy black redaction bars over its lines, the text beneath unreadable, the truth withheld, no legible words, no people [STYLE] Avoid: [NEG]
- `M09_src.png`
A single thin band of pale light lying across a cold marble wall, abstract and unreadable, a constitutional sentence rendered as light, no legible text, no people [STYLE] Avoid: [NEG]
- `M10_src.png`
The interior of a grand empty marble high-court chamber with soft dust suspended in a cold shaft of light, monumental and still, no people, no text [STYLE] Avoid: [NEG]
- `M11_src.png`
A closed unlocked door opened only a hand's width onto a dark room, the fragile pause before entry, cold light along the edge, no people [STYLE] Avoid: [NEG]
- `M12_src.png`
A single folded banknote resting on a bare dark table under one hard light, denomination illegible, money as the only remedy, no legible numbers, no people [STYLE] Avoid: [NEG]
- `M13_src.png`
A printed settlement check resting on a polished table with a pen laid beside it, the amount field abstract and unreadable, no legible numbers, no people [STYLE] Avoid: [NEG]
- `M14_src.png`
An electronic vote tally board on a chamber wall with abstract unreadable indicator lights, a recorded outcome, no legible numbers, no people [STYLE] Avoid: [NEG]
- `M15_src.png`
A thin line of warm dawn light along the bottom edge of a closed front door in a dark hallway, morning on the far side, no people [STYLE] Avoid: [NEG]
- `M16_src.png`
A single window with the last deep blue of night at the edge of turning to grey dawn over a quiet skyline, one warm room, no people, no visible address [STYLE] Avoid: [NEG]
```

## 8.2 Wan 2.2 A14B の設定（★Known-good・この値を変えるな。`comfy_wan_thompson.py` を下敷きにパスと SHOTS だけ差し替え）

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
STILL_DIR     = H:\pd-media\assets\ai\young          # 種画像 M<NN>_src.png を読む
VIDEO_OUT_DIR = H:\pd-media\assets\ai_video\young
POS_PREFIX = "cinematic documentary shot, subtle natural motion, "
POS_SUFFIX = ", slow deliberate camera move, shallow depth of field, film grain, photoreal, consistent lighting, no sudden changes"
NEG_PROMPT = "static, motionless, blurry, low quality, distorted, deformed, extra limbs, bad anatomy, morphing face, flickering, jitter, warping, text, watermark, identifiable face, real person likeness"
```

**ゲート:** `dry_validate`（length=5 で1回POSTして配線エラーを安く検出）/ `assert_loaded_completely`（部分ロード検出）/ `assert_frame_math`（フレーム計算）。`--run` パスにだけ配線。

## 8.3 実行手順（まず1本で通す）

```bash
py -3.11 scripts/comfy_wan_young.py --build            # グラフだけ（GPU触らない）
py -3.11 scripts/comfy_wan_young.py --run --shot M01   # 1本本番して目視
py -3.11 scripts/comfy_wan_young.py --run-all          # 残り15本（冪等・既存スキップ）
```
1本 24–73 GPU分・16本で 7–19時間。`/queue` `/history` を30秒間隔でポーリング。

## 8.4 RIFE で 48fps 化（`rife_young.py`・`rife_thompson.py` と同手順）

```
RIFE = D:/AI/tools/rife-ncnn-vulkan-20221029-windows/rife-ncnn-vulkan.exe / モデル rife-v4.6
```
1. Wan 出力先頭 **5フレームは length=5 検証プローブなので捨てる**（`DROP_VALIDATE=5`）
2. 残り41を `f0001.png` 連番にリネーム → RIFE 2x を**2回**（=4x）→ **164フレーム**
3. 164/48fps = **3.417秒** → `ffmpeg -framerate 48 -i f%04d.png -c:v libx264 -pix_fmt yuv420p` で `M<NN>_rife.mp4`
4. **フレーム数検証** `n2 >= 4*n0 - 8` でなければ `SHORT?` で記録し reject

## 8.5 i2v の QC

- 顔・身体が生成されていないこと（NEG で抑えているが**必ず目視**・制約5/6）
- モーフィング/ちらつき/ワープが無いこと → あれば別シードで再生成
- 3.417秒あるので B のカット設計では 3.0–3.4秒で使う想定（16本 × 2回 = 32カット）

---

# 9. A-6: 合成レイヤー（distinct 素材に数えない）

| 種別 | 選定 | 用途 |
|---|---|---|
| `particle_assets` | **6本** | 大理石法廷の埃・記録庫の塵。黒背景 drift を screen 合成 |
| `light_assets` | **4本** | 家庭内の実用光・街灯の光条 |
| `vfx_overlays` | **2本** | 微細なグレイン・テレビ光のノイズ |
| **合計** | **12本** | |

**ルール:** 合成レイヤーは `check_asset_reuse` の distinct に数えない → `remotion/public/young/overlay/` に置き、`young_film.json` の `cuts[].src` には**出さない**（出すと factory 判定で1回制限を食う）。同じレイヤーを何度重ねてもよい（素材ではなく加工）。黒背景でループするものを選び `blend_hint` を書く。**§7.5 の目視QC対象**（12本・12分）。

```bash
./.venv/Scripts/python.exe scripts/select_factory_assets.py --kind video --query dust_particles --limit 20 --exclude-used --ep PD-2026-042-young --json
```

---

# 10. A-7/A-8: staging とマニフェスト出力

## 10.1 Remotion public への staging（`scripts/stage_young_assets.py`）

```
remotion/public/young/img/     ← role=body の静止画85枚（+ 同名 _depth.png）
remotion/public/young/factory/ ← 選定 factory .mp4 93本
remotion/public/young/motion/  ← i2v M<NN>_rife.mp4 16本
remotion/public/young/overlay/ ← 合成レイヤー 12本
```
- `public_path` はマニフェストの値と実ファイルが一致すること
- factory 動画は `libx264 crf 16 preset medium -an` で **30fps に conform** してコピー（`import_to_remotion.py` の `conform_video(...,fps=30)` と同じ）
- i2v は 48fps のまま置く
- 既存 sha256 一致ならコピーをスキップ（冪等）

**★命名規則（`check_asset_reuse.kind_of()` がパス文字列で分類する・外すと誤分類）:**
- factory の `public_path` は必ず `young/factory/` の下（`/factory` を含む）
- i2v の `public_path` は必ず `.mp4` で終わり `_rife` を含む
- 静止画の `public_path` は `.png` で `/factory` も `ai_video` も `_rife` も**含めない**
- 合成レイヤーは `young/overlay/` に置き `cuts[].src` に出さない

> **B のレンダは `--public-dir=public_slim`（Root.tsx に `id="Ep42Young"`）を使う想定だが、`public_slim` の構築は B の責務。** A は `remotion/public/young/` に正典を置くところまで（B が slim を派生させる）。

## 10.2 権利台帳 `05_stock/stock_ledger.v001.json`

全静止画・i2v・factory・overlay を1行ずつ: `asset_id`/`path`/`source`（`ai_codex` or `factory`）/`license`/`commercial_use`/`sha256`/`ai_disclosure_required`/`generated_at`。

## 10.3 境界契約マニフェストの出力

```bash
./.venv/Scripts/python.exe scripts/build_young_asset_manifest.py
./.venv/Scripts/python.exe scripts/build_young_asset_manifest.py --verify
./.venv/Scripts/python.exe scripts/build_young_asset_manifest.py --reuse-feasibility
```
この3つが exit 0 で「マニフェストが本番になった」。**Bのファイルを直接書き換えて知らせようとしない。**

---

# 11. 素材反復禁止ゲートの実仕様（`check_asset_reuse.py`）

```python
MAX_USES_FACTORY = 1        # 無料 + 11,000本超 → 繰り返す理由が無い
MAX_USES_MOTION  = 2
MAX_USES_STILL   = 2
MIN_FIRST_USE_SHARE = 0.70
```
種別判定は**パス文字列**（`kind_of()`）: `/factory` or `af-bg-` → factory / `.mp4|.mov|.webm` or `ai_video` or `_rife` → motion / それ以外 → still。§10.1 の命名規則を守る。

EP42 の設計値: still 101/85=1.19(≤2) / factory 93/93=1.0(≤1) / motion 32/16=2.0(≤2) / first-use 194/226=0.8584(≥0.70)。**全て達成可能。**

---

# 12. 絶対にやらないこと

- **EP39（frazier）/EP40（lech）/EP41（thompson）のファイルに一切触らない。** 読み取りのみ可。素材・色・音のレーンも分離。
- **スレッドBの所有ファイル（§0.2）に触らない。** 特に `remotion/src/**` `scripts/ae/**` `scripts/build_young_film.py` `manifest.json` `04_scenes/shotlist*` `figures`。
  - **ただし `04_scenes/ai_prompts.v001.md` は A が書く**（`generate_sdxl_4k.py` の入力・§5.9/§8.1a）。B は読むだけ。
- **図解・トランジション・タイポの素材を探しに行かない。** 在庫が薄い/無いカテゴリは B が自作する。
- **課金ジョブを起動しない**（ElevenLabs TTS / 課金画像API / アップロード）。ローカル A1111・ComfyUI・RIFE は GPU を使うだけで課金なし（オーナー許可済み）。
- **公開済み・出荷済み mp4 を上書き・再レンダしない。**
- **実在人物の肖像・likeness・身体をどこにも作らない**（§1・制約5/6）。
- **`no-knock`・`unconstitutional`・`she changed the law` をプロンプト・タグ・注記・ファイル名のどこにも書かない**（制約2/3・§1.2/§1.3）。**和解を責任認定に見せる絵を作らない**（制約1）。
- **バリエーション（`_02`/`_03`）を作らない・`--variants 3` を使わない。** 1シーン1枚。反復回避は distinct 85 で担保（§0.1・§5.6）。
- **枚数・本数を「だいたい」で決めない。** §3 の確定値（still 85 / factory 93 / i2v 16 / distinct 194 / first-use 0.858）と §3.3 の検算をそのまま使う。合わなければ実装ではなく**本書を疑って報告**。
- **★ファイル名・subtype・プロンプトを根拠に「大丈夫」と判断しない。** EP36は大聖堂を、EP38は牛を通した。**生成物・在庫クリップを実際に見る**（特に制約5/6は目視でしか守れない）。

---

# 13. 完了報告に含めるもの

```
1. accepted 静止画の枚数と内訳（body 85 / i2v_source 16 / also_thumb 6 / reject N）
2. factory 選定 93本のリスト（asset_id / subtype / eyeballed_content）と、subtype と食い違って外した本数
3. EP39/EP40/EP41 重複ゼロの確認結果
4. i2v 16本の frames / duration_sec と、SHORT? の有無
5. 合成レイヤー12本のリスト
6. §0.4 の [A-DONE-1]〜[A-DONE-5] の実行結果（exit code をそのまま貼る）
7. §3.3 の検算 [1]〜[7] を自分で再計算した結果
8. asset_manifest.v001.json の counts ブロック
9. 6制約・1枚前提の自己申告（no-knock/unconstitutional/she changed the law が全出力に皆無・バリエーション0・Young/Hudson非人物化を目視確認）
```

**「動いたと思う」は完了ではない。ゲートが exit 0 を返して初めて完了。自分でQC基準を書き換えて通すのは禁止。**
