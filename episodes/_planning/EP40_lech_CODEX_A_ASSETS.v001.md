# EP40 lech — Codex スレッドA「素材生成」引き継ぎプロンプト v001

> **このファイルは単体で完結している。他のファイルを読まなくても着手できる。**
> 並行して走っているスレッドB（実装）のファイル `EP40_lech_CODEX_B_BUILD.v001.md` は**読まなくてよい**。
> 設計書 `EP40_lech_DESIGN_and_CODEX_PROMPTS.v001.md` も**読まなくてよい**（必要な数値はすべて本書に転記済み）。

```
あなたは Prime Documentary（YouTubeドキュメンタリーチャンネル）の制作エンジニアです。
リポジトリ: C:\Users\aab15\Documents\prime-documentary
Python:     C:\Users\aab15\Documents\prime-documentary\.venv\Scripts\python.exe
メディア:   H:\pd-media
担当:       EP40 / Episode ID: PD-2026-040-lech / slug: lech
```

---

# 0. このスレッドの責務・境界・完了条件

## 0.1 このスレッド（A）の責務

**GPU律速・目視律速の長時間ジョブ。** 本編で使う「絵」を全部そろえ、1本のマニフェストに書き出すところまで。

| # | 作業 | 成果物 | 所要目安 |
|---|---|---|---|
| A-1 | SDXL静止画のバッチ生成（**50シーン × 3バリエーション = 150枚**） | `H:\pd-media\assets\ai\lech\S<NN>_<VV>.png` | 3.5–5時間（GPU） |
| A-2 | 静止画のQCと役割別選抜（**目視必須**） | `05_visuals/still_qc.v001.json` + コンタクトシート | 1.5時間 |
| A-3 | depth map 生成（`treatment:"depth"` の必須入力） | `H:\pd-media\assets\ai\lech\S<NN>_<VV>_depth.png` | 20分 |
| A-4 | factory 実写クリップ **85本**の選定と**全点目視QC** | `05_stock/factory_selection.v001.json` / `05_visuals/factory_clip_qc.v001.json` | **2時間（うち目視だけで1時間以上）** |
| A-5 | i2v モーション化 **16本**（Wan 2.2 A14B → RIFE 48fps） | `H:\pd-media\assets\ai_video\lech\M<NN>_rife.mp4` | 7–20時間（GPU） |
| A-6 | 合成レイヤー（light / particle / vfx）の選定 | `05_stock/overlay_selection.v001.json` | 30分 |
| A-7 | 権利台帳と**境界契約マニフェスト**の出力 | `05_stock/stock_ledger.v001.json` / **`05_visuals/asset_manifest.v001.json`** | 20分 |
| A-8 | Remotion public への staging | `remotion/public/lech/{img,factory,motion,overlay}/` | 30分 |

## 0.2 もう一方のスレッド（B）との境界

**接続点はただ1ファイル。**

```
episodes/PD-2026-040-lech/05_visuals/asset_manifest.v001.json
   ↑ Aが生成（唯一の生産者）        ↓ Bが消費（唯一の消費者）
```

**Bはこのファイル以外のAの中間生成物を読まない。Aはこのファイル以外のBの成果物に依存しない。**
Bは**スタブ素材**（同じスキーマの `asset_manifest.stub.v001.json`）で全パイプラインを完走できる設計になっているので、
**Aの完了を待っていない。Aも急がなくてよいが、途中経過を壊すな。**

### 0.2.1 ファイル所有権（**これを破ると並行作業が壊れる**）

| パス | 所有 | Aの権限 |
|---|---|---|
| `H:\pd-media\assets\ai\lech\**` | **A** | 読み書き |
| `H:\pd-media\assets\ai_video\lech\**` | **A** | 読み書き |
| `episodes/PD-2026-040-lech/05_visuals/**` | **A** | 読み書き |
| `episodes/PD-2026-040-lech/05_stock/**` | **A** | 読み書き |
| `remotion/public/lech/{img,factory,motion,overlay}/**` | **A** | 読み書き |
| `scripts/gen_lech_sdxl_batch.py` ほか §0.3 のAスクリプト | **A** | 新規作成 |
| `episodes/PD-2026-040-lech/manifest.json` | **B** | **触るな** |
| `episodes/PD-2026-040-lech/03_script/**` `04_scenes/**` `08_edit/**` `09_package/**` | **B** | **触るな** |
| `remotion/src/**` `remotion/props/**` `remotion/public/lech_dryrun/**` | **B** | **触るな** |
| `scripts/ae/**` | **B** | **触るな**（読むのも不要） |
| `episodes/PD-2026-039-*/**` および EP39 の素材 | **EP39の別エージェント** | **絶対に触るな。読み取りのみ可** |

> `episodes/PD-2026-040-lech/05_visuals/` と `05_stock/` は **A が `mkdir(parents=True, exist_ok=True)` で自分で作る**。
> B が同じ親ディレクトリを作っても衝突しない（両者とも `exist_ok=True`）。**A は `manifest.json` を書かない。**

## 0.3 A が新規作成するスクリプト（これ以外を新規に作らない）

| パス | 役割 |
|---|---|
| `scripts/gen_lech_sdxl_batch.py` | §5 の50シーン×3を冪等バッチ生成（ローカルA1111） |
| `scripts/qc_lech_stills.py` | §6 の静止画QC＋役割別選抜 |
| `scripts/select_lech_factory.py` | §7 の factory 85本選定（EP39 sha256 除外） |
| `scripts/build_lech_factory_qc.py` | §7.6 の factory_clip_qc マニフェスト＋コンタクトシート |
| `scripts/comfy_wan_lech.py` | §8 の i2v 16本（Wan 2.2 A14B ドライバ） |
| `scripts/rife_lech.py` | §8.4 の RIFE 4x → 48fps |
| `scripts/select_lech_overlays.py` | §9 の合成レイヤー選定 |
| `scripts/stage_lech_assets.py` | §10.1 の remotion/public/lech への staging |
| `scripts/build_lech_asset_manifest.py` | §4 の境界契約マニフェストを出力 |

**depth map は新規スクリプトを作るな。** 既存の `scripts/gen_depth_maps.py --dir <フォルダ>` をそのまま使う（§6.4）。

## 0.4 完了条件（このスレッドが「終わり」になる条件）

以下が**すべて緑**になったら完了報告してよい。1つでも赤なら未完了。

```bash
cd C:\Users\aab15\Documents\prime-documentary

# [A-DONE-1] 境界契約マニフェストが自己検証を通る
./.venv/Scripts/python.exe scripts/build_lech_asset_manifest.py --verify
#   → exit 0。counts が §3.4 の確定値以上。全パスが実在。sha256 重複ゼロ。

# [A-DONE-2] 素材の反復禁止ゲートが「素材点数の観点で」通ることを机上で確認
./.venv/Scripts/python.exe scripts/build_lech_asset_manifest.py --reuse-feasibility
#   → distinct 静止画 >= 70 / i2v >= 16 / factory >= 85 / 合計 distinct >= 171
#     かつ first-use share >= 0.70 を満たすこと

# [A-DONE-3] 静止画の解像度ゲート（preflight の MIN_LONG_EDGE_PX = 3840）
./.venv/Scripts/python.exe scripts/qc_lech_stills.py --check-resolution
#   → 本編で使う全静止画の長辺 >= 3840px

# [A-DONE-4] factory の視覚QCゲート（★全85本を目で見た記録があること）
./.venv/Scripts/python.exe scripts/check_visual_asset_qc.py --ep PD-2026-040-lech
#   → exit 0（`05_visuals/factory_clip_qc.v001.json` が staging 済みの全クリップを
#     reviewed:true で網羅していること。ファイル名は信用されない — §7.5）

# [A-DONE-5] EP39との素材被りゼロ
./.venv/Scripts/python.exe scripts/select_lech_factory.py --verify-no-ep39-overlap
#   → 重複 sha256 = 0
```

---

# 1. ★★★ 最優先の絶対条件（accuracy_lock）★★★

**Lech v. Jackson は「最高裁判決」ではない。**

| 項目 | 正しい記述 | 禁止される記述 |
|---|---|---|
| 判断した裁判所 | 米国**第10巡回区控訴裁判所**（United States Court of Appeals for the Tenth Circuit） | 「最高裁が」「the Supreme Court ruled / decided / held / upheld / affirmed」 |
| 年 | **2019年**（控訴審） | 2020年を「判決の年」として書く |
| 最高裁の関与 | **2020年に上告を受理しなかった（cert. denied）だけ**。中身の判断はしていない | 「最高裁が支持した」「最高裁も同じ結論」 |
| 引用形式 | `Lech v. Jackson, 791 F. App'x 711 (10th Cir. 2019)`（**F. App'x = 未公刊**） | `U.S.` レポーター / `S. Ct.` を付す |

## 1.1 このスレッド（A）における適用範囲

Aは台本を書かないが、**Aが書く文字列にも同じ禁止がかかる**。対象は:

- SDXL プロンプト本文（`prompt` / `negative_prompt`）
- `asset_manifest.v001.json` の `tags[]` / `qc.notes` / `caption_hint`
- `still_qc.v001.json` / `factory_clip_qc.v001.json` / `factory_selection.v001.json` / `overlay_selection.v001.json` の全文字列
- `stock_ledger.v001.json` の `notes`
- ファイル名・ディレクトリ名

## 1.2 機械ゲート（**Aが自分のファイルに対して実行する**）

`scripts/build_lech_asset_manifest.py --verify` の内部で、A が書いた**全JSONの全文字列値**に対して次を実行し、
1件でもヒットしたら exit 1:

```python
import re
BANNED_ZONE = re.compile(r"supreme\s*court|最高裁|SCOTUS", re.IGNORECASE)
```

> **Aのファイルには例外を設けない（全面禁止）。** A は「cert. denied を説明する文脈」を書く必要がないため、
> 文脈許可（スレッドBのR2ルール）は適用しない。プロンプトに裁判所を出したいときは
> `a stone federal appellate courthouse facade`（§5.9 S59）のように**具体名を書かない**。

## 1.3 R2（実在私人が主役）の安全ルール — **画像生成の絶対条件**

1. **実在の Lech 一家・逃走した男・個々の警察官の肖像を作らない。** 人物は必ず後ろ姿・シルエット・顔の外れた構図・手元のみ。
2. **実在の住所を再現しない。** 番地・表札・道路標識・郵便受けの文字を生成しない。
3. **読める公文書・判決文を作らない。** 書類は雰囲気のみ（文字は判読不能）。
4. **流血・遺体・生々しい暴力を描かない。** 破壊は**建物に対してのみ**描く。
5. AI画像は概要欄でAI生成であることを開示する → マニフェストの `ai_disclosure_required: true` を全静止画に立てる。

---

# 2. 台本の語数と尺の確定値（Aが素材点数を積算する根拠）

2026-07-19 に **31話分の実TTS音声**（`H:\pd-media\episodes\*\06_voice\draft\VC-*.mp3` の実時間合計）と
台本語数を突き合わせて実測した確定値。**古い資料の「150 wpm」「173 wpm」「1,700〜1,950語」はすべて誤り。使うな。**

```
ナレーション速度  = 178.1 wpm（実測中央値。範囲 163.7 – 237.4）
目標語数          = 2,140語
許容band          = 2,048 – 2,226語
設計総尺          = 741.4秒 = 12:21（band 690–750秒の内側）
```

判定は `python scripts/check_script_length.py <script> --json` が**唯一の正**。自己申告・体感による判断は禁止。
（実装は `scripts/check_script_length.py`。`WPM_MEDIAN = 178.1 / WPM_SLOW = 163.7 / WPM_FAST = 237.4`、
`DEFAULT_LO_SECONDS = 690.0 / DEFAULT_HI_SECONDS = 750.0`。`preflight_render_gate.py` の **checks 配列の先頭**に配線済みで、
ElevenLabs の TTS と Remotion レンダーに課金する前にブロックする。）

**台本本体はスレッドB／別スレッドの担当。Aは台本を書かないし待たない。**
Aにとってこの数値の意味は1つだけ:

> **741.4秒 = 226カット = 初出70%以上 = 最低155点の異なる素材。**（§3 で積算する）

---

# 3. ★素材構成の確定値（オーナー指摘 2026-07-19 で**2回**改訂済み）

## 3.1 経緯（**どちらの指摘も本節に反映済み。旧数値を使うな**）

**指摘1「20枚じゃ足りない」**

> 旧設計は「22シーン × 6バリエーション = 132枚 / 本編使用 distinct 60枚」。
> 総枚数は132あっても、**視聴者が見る「別の被写体」は22種類しかない**。
> 同じ壊れた家を6アングルで見せても、観る側には同じ家。**反復感の原因は総枚数ではなくシーン数。**
> → バリエーションは「同じ被写体の別アングル」ではなく、**別の被写体を増やす方向**に使う。1シーン2〜3枚に抑える。

**指摘2「全て画像じゃなくてもいいんだよ。大量の素材があるからね」**

> 指摘1への対応でSDXL生成に寄せすぎた（静止画120枚案）。**在庫の実写クリップが11,623本ある。**
> → **SDXLは「この作品にしか無い絵」だけに使う。周辺・情景・繋ぎは実写在庫で足りる。**

## 3.2 在庫の実測（`H:\pd-media\assets`・2026-07-19）

| カテゴリ | 実測本数 | EP40での使い道 |
|---|---|---|
| `factory/backgrounds` | **11,623** | **主力。** 郊外の街並み、警察車輌、夜の住宅地、制度側の建物、空気・情景・繋ぎ |
| `factory/light_assets` | 1,401 | 合成レイヤー（光条・レンズフレア） |
| `factory/particle_assets` | 1,225 | 合成レイヤー（粉塵・埃） |
| `factory/vfx_overlays` | 1,196 | 合成レイヤー（煙・グレイン） |
| `factory/loops` | 454 | 抽象的な繋ぎ |
| `factory/texture_assets` | 3,911 | 紙・木材のテクスチャ（書類カードの下地） |
| `ai`（既存生成物・他エピソード） | 1,287 | **使わない**（EP40の絵柄と合わない・重複リスク） |
| `stock` | 235 | 予備 |

**空フォルダ（中身0本）:** `diagram_assets` / `transitions` / `typography_assets` / `parallax_layers` /
`lottie_assets` / `ai_video_shots` / `sfx`

> **★重要:** EP40は設計に**家の見取り図**と**破壊箇所の図解**と**幕間トランジション**を含むが、
> これらの在庫は **0本**。**在庫が無い＝After Effects / Remotion で自作するしかない。**
> **これはスレッドBの担当。Aは図解素材を探しに行かないこと**（見つからない探索に時間を溶かすな）。

## 3.3 静止画の使用回数と判定（`check_asset_reuse.py` の上限は **2回**）

| 静止画 distinct | 1枚あたり使用回数 | 判定 |
|---|---|---|
| 39枚 | 4.0回 | 旧仕様の上限。**反復が露骨に見える** |
| 60枚 | 2.08回 | **上限2回をわずかに超過＝FAIL** |
| 63枚 | 1.98回 | ゲート最低ライン（余裕ゼロ） |
| **70枚** | **1.79回** | **確定値。QCの脱落を吸収できる余裕がある** |
| 125枚 | 1.0回 | 完全に反復なし（余力があればここへ） |

## 3.4 EP40 の素材構成（**確定値。これで調達する**）

| 種別 | distinct 点数 | 担当カット数 | 使用回数 | 調達方法 |
|---|---|---|---|---|
| **SDXL静止画（本編 body）** | **70枚** | 125カット | **1.79回** | **この作品にしか無い絵だけ**（§3.5） |
| **factory 実写クリップ** | **85本** | 85カット | **各1回** | 在庫11,623本から選抜（§7） |
| **i2v モーション** | **16本** | 16カット | **各1回** | 上のSDXLから動きが意味を持つものを選抜（§8） |
| **合計（カットに出る素材）** | **171点** | **226カット** | | |
| 合成レイヤー（light/particle/vfx） | 12–20本 | — | 重ね掛け | **distinct 素材に数えない**（§9） |

**SDXL の追加枠（本編カットに出ない分）:**

| 用途 | 点数 | 用途 |
|---|---|---|
| AEカードの背景静止画（`role: "ae"`） | **15枚** | §4.4。Bが要求する背景。body には回さない |
| i2v の元画像（`role: "i2v_source"`） | **16枚** | §8.1。静止画としては使わない専用枠 |
| サムネ／Shorts 予備（`role: "thumb"`） | **9枚** | 本編では使わない |
| **SDXL 必要 accepted 合計** | **70 + 15 + 16 + 9 = 110枚** | |
| **SDXL 生成バッチ** | **50シーン × 3バリエーション = 150枚** | accepted 率 73% を見込む |

## 3.5 SDXL と実写在庫の振り分け（**どのシーンをどちらで作るか**）

**原則:**

- **SDXLで作る = この事件にしか存在しない固有物。** 壊れた家の各面・各部屋、瓦礫の細部、
  破壊前の**同じ**家（before/after の対応が要るので実写では代替不能）、一家の匿名再現、書類。
- **実写在庫で足りる = どこにでもある周辺。** 郊外の街並み、パトカー、封鎖、夜の住宅地、
  近隣の視点、市庁舎・法廷などの制度側、空気・情景・繋ぎ。

| 区分 | シーン数 | 内訳 |
|---|---|---|
| **SDXL 必須** | **50シーン** | §5.9 の S01–S09 / S11–S13 / S15 / S21 / S23–S26 / S28–S52 / S55–S57 / S61–S64 |
| **実写在庫でカバー** | **14シーン** | §7.3 の S10 / S14 / S16 / S17 / S18 / S19 / S20 / S22 / S27 / S53 / S54 / S58 / S59 / S60 |
| | | ＋ Sid を持たない繋ぎ・情景クリップ **71本** |

> **50 + 14 = 64 の視覚シーン。うちSDXLが50シーン**（オーナー確定の 48–50 シーンに一致）。
> factory 85本 = 上の14シーンをカバーする14本 + 繋ぎ・情景の71本。

## 3.6 全体の検算（**Codex は自分で再計算して一致を確認すること**）

```
[1] 総カット数
    226 = factory 85 + i2v 16 + 静止画カット 125

[2] 平均ショット長（v2 row8: <=6秒）
    絵が必要な区間 = 741.4 − OPENING 3.5 − ENDCARD 9.0 = 728.9 秒
    728.9 / 226 = 3.225 秒/カット                       ✓ <=6秒

[3] 静止画占有率（check_animation_mix の MAX_STILL_SHARE = 0.45）
    静止画カット 125本 × 平均 2.05秒 = 256.3 秒
    256.3 / 741.4 = 34.6%                               ✓ <=45%（旧案43.1%より大幅に改善）
    → 動画（factory+i2v）が 728.9 − 256.3 = 472.6 秒
    → 101カットで 472.6秒 = 平均 4.68秒/カット          ✓ <=6秒

[4] check_asset_reuse の per-asset 上限
    factory : 85カット / 85本  = 1.00回  ✓ <=1
    motion  : 16カット / 16本  = 1.00回  ✓ <=2
    still   : 125カット / 70枚 = 1.79回  ✓ <=2

[5] check_asset_reuse の MIN_FIRST_USE_SHARE = 0.70
    distinct 合計 = 70 + 16 + 85 = 171
    171 / 226 = 0.7566                                  ✓ >=0.70（余裕 13カット分）

[6] factory 下限（30秒に1本 = 741.4/30 = 24.7 → >=25本）
    85本 >= 25本                                        ✓
    741.4 / 85 = 8.7秒に1本
```

> **[5] の余裕は13カット分しかない。** 静止画を1枚減らすと first-use share が 0.752 に落ちる。
> **QCで静止画が70枚を割ったら、減らしたまま進まず §6.3 の追加生成を回すこと。**

---

# 4. ★境界契約: `asset_manifest.v001.json`（AとBを繋ぐ唯一のファイル）

**パス:** `episodes/PD-2026-040-lech/05_visuals/asset_manifest.v001.json`
**スキーマ版:** `lech_assets.v1`（固定文字列。異なれば B 側の全ツールが exit 2）
**生産者:** `scripts/build_lech_asset_manifest.py`（**A が実装する。他の誰もこのファイルを書かない**）
**消費者:** B の `build_lech_film_data.py` / `check_lech_asset_manifest.py` / `scripts/ae/build_lech_hero_jsx.py`

## 4.1 スキーマ（厳密。1フィールドも省略しない）

```jsonc
{
  "schema_version": "lech_assets.v1",          // 固定文字列
  "episode_id": "PD-2026-040-lech",            // 固定文字列
  "slug": "lech",                              // 固定文字列
  "generated_at": "2026-07-19T21:00:00+09:00", // ISO8601
  "producer": "scripts/build_lech_asset_manifest.py",
  "is_stub": false,                            // A の出力は必ず false。B のスタブだけ true

  "counts": {                                  // 実配列長と一致必須（不一致なら exit 1）
    "still_body": 70,                          // >=70
    "still_ae": 15,                            // >=15
    "still_i2v_source": 16,                    // >=16
    "still_thumb": 9,                          // >=9
    "motion": 16,                              // >=16
    "factory": 85,                             // >=85
    "overlay": 12                              // >=12（distinct 素材には数えない・§9）
  },

  "stills": [
    {
      "asset_id": "LECH-S01-01",               // ^LECH-S\d{2}-\d{2}$
      "scene_id": "S01",                       // ^S\d{2}$（§5.9 の S01..S64 のうちSDXL担当分）
      "variation": 1,                          // 1..6
      "role": "body",                          // "body" | "ae" | "i2v_source" | "thumb" | "reject"
      "act": 1,                                // 0=HOOK / 1..4=幕 / 5=ED / 9=サムネ専用
      "path": "H:/pd-media/assets/ai/lech/S01_01.png",       // 絶対パス・スラッシュ区切り・実在必須
      "depth_path": "H:/pd-media/assets/ai/lech/S01_01_depth.png", // role!="thumb" は実在必須。thumbはnull可
      "public_path": "lech/img/S01_01.png",    // remotion/public 相対。role が body|ae のみ非null
      "width": 3840, "height": 2160,           // 長辺 >=3840 必須（role="thumb" 以外）
      "sha256": "e3b0c442...",                 // 64桁hex（"sha256:" 接頭辞を付けない）
      "mean_luma": 137.2,                      // 0..255。PIL 'L' 変換の平均
      "phash": "a1b2c3d4e5f60718",             // 16桁hex（近似重複検出用）
      "tags": ["exterior", "daylight", "intact_house"],
      "caption_hint": "the house before",      // Bのscene_plan補助。空文字可。accuracy_lock検査対象
      "prompt_sha256": "9f86d081...",
      "seed": 40001001,
      "model": "juggernautXL_ragnarokBy.safetensors",
      "source": "ai_codex",
      "commercial_use": "allowed",
      "ai_disclosure_required": true,
      "qc": {
        "reviewed": true,                      // role!="reject" は必ず true
        "on_theme": true,
        "has_readable_text": false,            // true なら role="reject" 必須
        "has_identifiable_face": false,        // true なら role="reject" 必須
        "notes": ""
      }
    }
  ],

  "motion": [
    {
      "asset_id": "LECH-M01",                  // ^LECH-M\d{2}$
      "source_scene_id": "S33",
      "source_still": "H:/pd-media/assets/ai/lech/S33_02.png",
      "path": "H:/pd-media/assets/ai_video/lech/M01_rife.mp4",
      "public_path": "lech/motion/M01_rife.mp4",
      "act": 3,
      "width": 1280, "height": 720,
      "fps": 48, "frames": 164, "duration_sec": 3.417,
      "sha256": "...",
      "tags": ["dust", "collapse"],
      "qc": {"reviewed": true, "on_theme": true, "artifact_free": true, "notes": ""}
    }
  ],

  "factory": [
    {
      "asset_id": "AF-BG-0460",                // assets/asset_manifest.v001.json の id をそのまま使う
      "path": "H:/pd-media/assets/factory/backgrounds/AF-BG-0460__office_interior_dark.mp4",
      "public_path": "lech/factory/AF-BG-0460__office_interior_dark.mp4",
      "type": "backgrounds",
      "subtype": "office_interior_dark",        // ★ラベルであって内容の保証ではない（§7.5）
      "kind": "video",                          // 必ず "video"
      "license": "Pexels License",              // ALLOWED_LICENSES のいずれか（§7.4）
      "sha256": "7b7641cf...",                  // shelf manifest の "sha256:" 接頭辞を外した64桁hex
      "act": 2,
      "covers_scene_id": "S53",                 // §3.5 の14シーンをカバーする本だけ設定。繋ぎは null
      "duration_sec": 8.24,
      "width": 1920, "height": 1080,
      "mean_luma": 61.2,
      "eyeballed_content": "an empty municipal lobby, wide static shot, no people",
      //  ↑ ★必須。ファイル名ではなく「実際に見た内容」を1文で書く（§7.5）
      "qc": {"reviewed": true, "on_theme": true, "no_watermark": true,
             "no_recognizable_person": true, "no_cartoon": true,
             "label_matches_content": true, "notes": ""}
    }
  ],

  "overlay": [
    {
      "asset_id": "AF-PART-0031",
      "path": "H:/pd-media/assets/factory/particle_assets/AF-PART-0031__dust_particles_floating.mp4",
      "public_path": "lech/overlay/AF-PART-0031__dust_particles_floating.mp4",
      "type": "particle_assets",
      "subtype": "dust_particles_floating",
      "license": "Pexels License",
      "sha256": "...",
      "blend_hint": "screen",                   // "screen" | "add" | "overlay"
      "eyeballed_content": "slow drifting dust motes on black, loops cleanly",
      "qc": {"reviewed": true, "on_theme": true, "no_watermark": true, "notes": ""}
    }
  ]
}
```

## 4.2 `build_lech_asset_manifest.py` が自己検証する不変条件（BLOCKING）

`--verify` で以下を全部検査し、違反を `{"field":..., "rule":..., "actual":...}` の配列で出力して exit 1:

1. `schema_version == "lech_assets.v1"` / `episode_id == "PD-2026-040-lech"` / `slug == "lech"` / `is_stub == false`
2. `counts.*` が各配列の実長と**完全一致**し、かつ §4.1 の下限を満たす
3. 全 `path` / `depth_path` / `public_path` の実体がディスク上に存在する
4. `sha256` が **全配列を通して一意**（重複ゼロ）
5. `role != "thumb"` の全静止画で `max(width, height) >= 3840`
6. `role in ("body","ae")` の静止画は `depth_path` と `public_path` が非null かつ実在
7. `qc.has_readable_text == true` または `qc.has_identifiable_face == true` の項目は `role == "reject"`
8. `role == "i2v_source"` の静止画は、`role == "body"` の静止画と**同一 asset_id を共有しない**
9. **全JSON文字列値**が §1.2 の `BANNED_ZONE` に一致しない
10. `factory[].license` / `overlay[].license` が §7.4 の `ALLOWED_LICENSES` に含まれる
11. `factory[].sha256` が EP39 の staged 素材と1件も衝突しない（§7.7）
12. **`factory[].eyeballed_content` が空文字でない**（＝目視していない本が混じっていない・§7.5）
13. `factory[].qc.label_matches_content` が `true`（`false` の本は選定から外す）

`--reuse-feasibility` では §3.6 の [4][5][6] を再計算し、1つでも割ったら exit 1。

## 4.3 `role` の割り当てルール（機械的に決める・恣意的に決めない）

```
1. QCを通った accepted 画像を、mean_luma と phash で重複を除いたうえで scene_id 昇順に並べる
2. i2v_source : §8.1 の16シーンから各1枚（そのシーンの accepted 中 phash が最も他と離れた1枚）
3. ae         : §4.4 の15枠に指定された scene_id から各1枚
4. thumb      : S34 / S36 / S44 / S56 / S62 から優先的に9枚
5. body       : 残り全部。ただし最低70枚。70に満たなければ §6.3 の追加バッチを回す
6. reject     : QCで落ちたもの（マニフェストには残す。理由を qc.notes に書く）
```

## 4.4 AE用静止画15枠（**スレッドBが要求する背景**。scene_id をここで固定する）

Bは After Effects のカードを23枚ビルドするが、そのうち**背景静止画を必要とするのは15枚**。
A は下表の scene_id から各1枚を `role: "ae"` として確保し、**同じ画像を body に回さない**。

| AEビートID | 内容 | 必要な scene_id |
|---|---|---|
| b01 | 事件が起きた年（DATE_STAMP） | **S09** |
| b02 | 立てこもり時間（CENTER_STACK） | **S21** |
| b03 | 万引き被害額 vs 家の損害額（SPLIT_COMPARE） | **S44** |
| b04 | 破壊手段の回数（CENTER_STACK） | **S31** |
| b05 | 家の損害額（CENTER_STACK） | **S43** |
| b06 | 一家が受け取った額（CENTER_STACK / COUNTDOWN） | **S45** |
| b07 | 補償率（RATIO_BAR） | **S62** |
| b08 | 判断した裁判所と年（DATE_STAMP） | **S63** |
| t01 | 幕1タイトルカード | **S01** |
| t02 | 幕2タイトルカード | **S13** |
| t03 | 幕3タイトルカード | **S23** |
| t04 | 幕4タイトルカード | **S48** |
| d01 | 警察報告書の提示 | **S55** |
| d02 | 市の回答書の提示 | **S56** |
| d03 | 一家の見積書／請求書の提示 | **S57** |

> `g01/g02`（時系列可視化）・`h01/h02`（家の見取り図と破壊箇所の図解）・`s01–s04`（幕間トランジション）は
> **在庫が0本のカテゴリ**（§3.2）であり、**AE側でベクター描画して自作する**。**Aは静止画を用意しなくてよい。**

---

# 5. A-1: SDXL 静止画のバッチ生成（50シーン × 3 = 150枚）

## 5.1 生成環境

```
API:   http://127.0.0.1:7860/sdapi/v1/txt2img            （ローカル AUTOMATIC1111）
       http://127.0.0.1:7860/sdapi/v1/extra-single-image （2段目のアップスケール）
       http://127.0.0.1:7860/sdapi/v1/interrupt          （タイムアウト時の中断）
モデル: juggernautXL_ragnarokBy.safetensors
出力:  H:\pd-media\assets\ai\lech\S<NN>_<VV>.png       （例: S01_01.png ... S64_03.png）
メタ:  H:\pd-media\assets\ai\lech\S<NN>_<VV>.json      （画像1枚につき1ファイル）
```

**ローカルGPU生成に課金は発生しない。オーナーは大量生成を明示的に許可済み。**
（禁止されているのは ElevenLabs TTS / 課金画像API / YouTubeアップロードだけ。§12）

> **注意:** シーン番号は S01–S64 の連番を維持するが、**SDXLで生成するのは §3.5 の50シーンだけ**。
> 実写在庫でカバーする14シーン（S10 / S14 / S16 / S17 / S18 / S19 / S20 / S22 / S27 / S53 / S54 / S58 / S59 / S60）は
> **SDXLで生成しない**（生成しても捨てるだけ。GPU時間の無駄）。

## 5.2 生成パラメータ（2段構成。長辺3840pxを確実に満たすため）

**Stage 1 — txt2img:**

```python
payload = {
    "prompt": f"{scene_core}{COMMON_STYLE}",
    "negative_prompt": COMMON_NEG,
    "seed": seed,                     # §5.5 の決定的シード
    "subseed": seed + 777,
    "subseed_strength": 0.10,
    "sampler_name": "DPM++ 2M",
    "scheduler": "Karras",
    "steps": 60,
    "cfg_scale": 6.2,
    "width": 1536, "height": 864,     # 16:9
    "batch_size": 1, "n_iter": 1,
    "enable_hr": True,
    "hr_resize_x": 3072, "hr_resize_y": 1728,
    "hr_second_pass_steps": 24,
    "denoising_strength": 0.30,
    "hr_upscaler": "R-ESRGAN 4x+",
    "restore_faces": False,
    "do_not_save_samples": True,
    "do_not_save_grid": True,
}
```

**Stage 2 — extra-single-image（Stage 1 の出力を 3840×2160 へ）:**

```python
payload2 = {
    "image": <stage1 base64>,
    "upscaling_resize_w": 3840,
    "upscaling_resize_h": 2160,
    "upscaling_crop": True,
    "upscaler_1": "R-ESRGAN 4x+",
    "upscaler_2": "None",
    "extras_upscaler_2_visibility": 0.0,
}
```

> **なぜ2段なのか:** `hr_resize` を直接 3840×2160 にすると SDXL の第2パスが 4090 の24GBを食い潰して
> 無言でOOM／極端に遅くなる。3072×1728 までを潜在空間の第2パスで作り、最後だけ純アップスケーラで
> 3840×2160 に伸ばす。`preflight_render_gate.MIN_LONG_EDGE_PX = 3840` はこれで確実に満たせる。
>
> **保存前に必ず PIL で `im.size` を検証し、`max(size) < 3840` なら FAIL 扱いにして再試行する。**
> 「たぶん3840になっているはず」は禁止。

**所要時間の目安:** 1枚あたり 80–110秒 → 150枚で **約3.5–4.5時間**。

## 5.3 共通スタイル接尾（`COMMON_STYLE` — 全プロンプトの末尾に必ず付ける）

```
, cinematic still, harsh midday sunlight and airborne dust, wide-angle sense of open suburban space, bleached daylight whites with concrete grey, splintered pale wood and warm amber dust motes, faintly green-grey outdoor shadows, deep shadow detail retained, shallow-to-medium depth of field, ultra-detailed, photoreal, 4K, 16:9, fine film grain, no text, no watermark, no logo
```

> **EP39（frazier）との分離:** この接尾に `navy` / `electric blue` / `night` / `interrogation` / `low-key` を**一切含めない**。
> EP39 のプロンプト接尾と**1語も共有しない**。EP40 は「郊外の一軒家 / 昼 / 物理的破壊 / gold-amber `#E5B53A`」、
> EP39 は「取調室 / 夜 / 密室 / electric blue `#1F6BFF`」。

## 5.4 共通ネガティブ（`COMMON_NEG` — 全プロンプトに必ず付ける）

```
text, words, letters, numbers, captions, watermark, logo, street address, house number, license plate, real celebrity, recognizable real person, identifiable face, portrait, mugshot, cartoon, illustration, low quality, blurry, deformed, extra limbs, gore, blood, corpse, night scene, dark navy interior, interrogation room
```

## 5.5 シード（決定的・冪等）

```python
def seed_for(scene_index: int, variation: int) -> int:
    # scene_index: 1..64（S01→1）, variation: 1..6
    return 40_000_000 + scene_index * 1_000 + variation
```

**S01_01 = 40001001 / S64_03 = 40064003。** 同じ入力なら常に同じ画像。

## 5.6 バリエーション軸（**同じ被写体の別アングルにしない**）

- `_01` = 基準。記載どおりの光と距離
- `_02` = **一段引く**（wider framing, more surrounding context, lower camera）
- `_03` = **光を変える**（late afternoon low sun, long raking shadows／または overcast diffuse light）

## 5.7 冪等バッチ設計（**中断・再開できること。これは必須要件**）

```
for scene in SDXL担当の50シーン:
    for variation in 1..3:
        out = H:/pd-media/assets/ai/lech/S<NN>_<VV>.png
        meta = out.with_suffix(".json")

        # [SKIP条件] 3つ全部を満たしたら生成せずスキップ
        if out.exists() and out.stat().st_size > 1024 and meta.exists():
            m = json.loads(meta.read_text("utf-8"))
            if m.get("prompt_sha256") == sha256(prompt) and m.get("long_edge", 0) >= 3840:
                skipped += 1; continue
            # プロンプトが変わった／解像度が足りない → 再生成する

        生成 → PILで解像度検証 → PNG保存 → メタJSONを**画像保存の後に**書く
```

**設計上の必須条件:**

1. **メタJSONは画像の後に書く。** 逆にすると、途中killでメタだけ残り「生成済み」と誤判定する。
2. **`--max-new N`** を実装し、1回の実行で生成する新規枚数に上限をかけられるようにする。
3. **`--scene S33`** / **`--scenes S30-S44`** で範囲指定できるようにする。
4. **`--extra-variations S12,S33`** で、指定シーンだけ `_04` `_05` `_06` を追加生成できるようにする（§6.3）。
5. **強い絵から先に生成する。** 途中で止まっても使える状態を保つ:
   - 優先度1: S33 S34 S36 S38 S39 S43 S44 S23 S29 S45 S62 S63 S64 S01 S13（AE枠とサムネ枠を含む）
   - 優先度2: 残りの幕3・幕4シーン
   - 優先度3: 幕1・幕2の平穏なシーン
6. 8枚ごとに `H:/pd-media/assets/ai/lech/_batch_progress.json` を更新する（生成済み一覧・失敗一覧）。
7. API がタイムアウト／接続エラーになったら `/sdapi/v1/interrupt` を叩いて次へ進み、失敗を記録して**止まらない**。
   最後に `failed` が1件でもあれば exit 1 にして、再実行で拾えるようにする。

## 5.8 メタJSON（`S<NN>_<VV>.json`）の中身

```jsonc
{
  "asset_id": "LECH-S01-01",
  "scene_id": "S01", "variation": 1, "scene_index": 1,
  "seed": 40001001,
  "prompt": "<フルプロンプト（COMMON_STYLE込み）>",
  "negative_prompt": "<COMMON_NEG>",
  "prompt_sha256": "<sha256(prompt)>",
  "model": "juggernautXL_ragnarokBy.safetensors",
  "sampler": "DPM++ 2M", "scheduler": "Karras",
  "steps": 60, "cfg_scale": 6.2,
  "stage1": {"width": 1536, "height": 864, "hr_resize": [3072, 1728], "hr_upscaler": "R-ESRGAN 4x+"},
  "stage2": {"upscaler": "R-ESRGAN 4x+", "resize": [3840, 2160]},
  "width": 3840, "height": 2160, "long_edge": 3840,
  "sha256": "<画像バイト列のsha256・64桁hex>",
  "generated_at": "2026-07-19T21:34:00+09:00",
  "source": "ai_codex", "commercial_use": "allowed", "ai_disclosure_required": true,
  "rights_origin": "AI-generated local SDXL symbolic reconstruction"
}
```

## 5.9 シーンプロンプト（**SDXLで生成する50シーン**）

各行の本文が `scene_core`。末尾に**必ず `COMMON_STYLE` を連結**し、`COMMON_NEG` をネガティブに入れる。
**`[FACTORY]` と記した番号は SDXLで生成しない**（§7.3 で実写在庫から調達する）。

---

### GROUP 1 — 破壊前の家（幕1 / act=1）S01–S09 ＋ [FACTORY] S10

> **この家は「破壊後」と同一物として認識される必要がある**（before/after の対応）。**実写では代替不能＝SDXL必須。**

**S01** — An ordinary two-story American suburban house on a quiet residential street in warm late-morning light, neat lawn, a basketball hoop over the garage, a bicycle lying on its side, utterly peaceful and lived-in, generic architecture with no visible address, no people

**S02** — The back of a suburban family house seen from the rear yard in bright daylight, a wooden deck with two empty chairs, a garden hose coiled on the grass, a screen door slightly ajar, ordinary and unremarkable, no people

**S03** — The side elevation of a suburban house and its concrete driveway in flat midday sun, a gate to the back yard, trash bins neatly aligned, a narrow strip of grass, mundane domestic geometry, no people

**S04** — Close view of a suburban front porch in warm light, a doormat worn thin, a pair of small shoes left by the door, a hanging plant, the ordinary threshold of a family home, no readable text, no people

**S05** — Interior of a lived-in family kitchen in soft daylight through a window, a table with an unfinished breakfast, a child's drawing taped to the fridge, worn cabinets, ordinary life interrupted mid-moment, no people, no readable text

**S06** — A family living room in gentle afternoon light, a sagging couch with a folded blanket, a television off, toys pushed into a corner, framed pictures turned away from camera, deeply ordinary, no faces, no people

**S07** — A child's bedroom in bright daylight, a small bed with rumpled sheets, drawings pinned to the wall with the images unreadable, a stuffed animal on the floor, sunlight falling across the carpet, no people

**S08** — An adult bedroom in soft morning light, an unmade bed, a bedside lamp and a paperback, curtains half drawn, a wardrobe door open, quiet and private, no people, no faces

**S09** — An interior hallway and staircase of a two-story family home in daylight from an upstairs window, a runner rug, family photographs on the wall with faces turned away or blurred beyond recognition, no people

**S10** — `[FACTORY]` 平穏な郊外の通り（引き）→ §7.3

### GROUP 2 — 侵入と初動（幕2 / act=2）S11–S13 / S15 / S21 ＋ [FACTORY] S14 S16–S20 S22

**S11** — A distant anonymous figure in a hooded jacket running across a sunlit suburban lawn, seen from far behind, motion blur on the figure, faceless and unidentifiable, sudden intrusion into calm

**S12** — A residential back door standing open with the frame splintered near the lock, bright daylight flooding into a dim interior, a single overturned potted plant, the tension of a violated threshold, no people

**S13** — A suburban front door left wide open onto an empty hallway, seen from the lawn in hard midday light, nothing visible inside but shadow, the wrongness of an open door with nobody there, no people

**S14** — `[FACTORY]` 最初のパトカー → §7.3
**S15** — A wide high-angle view of a suburban block with many police vehicles converging from several directions, yellow tape stretched across lawns, neighbouring houses looking on, small human silhouettes at a distance, faces unreadable
**S16–S20** — `[FACTORY]` 封鎖テープ／ブラインド越しの視点／バリケード／無線機の手元／装備の脚元 → §7.3

**S21** — A suburban street in the golden hour of a very long day, long stretched shadows from parked emergency vehicles, an abandoned coffee cup on a car hood, the exhaustion of many hours passing, no people

**S22** — `[FACTORY]` 夜の投光器と住宅地 → §7.3

### GROUP 3 — 投入された機材・装甲車（幕2末〜幕3 / act=2,3）S23–S26 / S28–S32 ＋ [FACTORY] S27

**S23** — A heavy armored police vehicle parked on a residential lawn under a bright afternoon sky, its bulk absurdly out of scale against a family house and a mailbox, dust hanging in the air, no people visible

**S24** — Close detail of the hydraulic ram arm on the front of an armored vehicle in hard sunlight, scratched steel and hydraulic lines, a machine built to open buildings, no people, no readable markings

**S25** — Close-up of anonymous gloved hands loading a chemical-agent launcher, seen from behind and above so no face is visible, bright outdoor light, matte black equipment, no readable markings

**S26** — A canister trailing thick pale smoke landing and skidding across a sunlit suburban lawn, the smoke plume just beginning to spread, sharp grass and hard shadow, no people

**S27** — `[FACTORY]` ドローン → §7.3

**S28** — A line of anonymous silhouetted figures assembled behind the bulk of an armored vehicle in harsh backlight, entirely reduced to dark shapes, no faces, no readable insignia

**S29** — The moment an armored vehicle's ram makes contact with an exterior house wall, siding buckling and a first burst of pale dust, violent and structural, no people, no blood

**S30** — Deep tracked vehicle ruts gouged across a suburban front lawn in flat daylight, torn turf and exposed soil, a garden ornament knocked flat, the ground itself damaged, no people

**S31** — Spent canisters and shell casings scattered across sunlit grass beside a suburban walkway, dozens of small metal objects on green, a count made visible, no people, no readable stamps

**S32** — A wide low-angle shot placing an armored vehicle directly beside a small residential mailbox and a tricycle, the scale collision absurd and frightening, hard afternoon light, no people

### GROUP 4 — 破壊（幕3 / act=3）S33–S44 ★**全てSDXL必須。EP40の主役**

**S33** — An exterior house wall being torn open, splintered timber and drywall bursting outward in a cloud of pale dust, harsh sunlight cutting through the new opening, violent and structural, no people, no blood

**S34** — A residential roof with a large ragged hole punched through it, shingles scattered across the lawn, bright sky visible through the breach, seen from a slight low angle, no people

**S35** — A gaping hole torn through the second-floor exterior wall of a suburban house seen from directly below, insulation hanging out, a bedroom's private interior exposed to the street, no people

**S36** — The front elevation of a suburban house with every window blown out, empty black rectangles in a bleached daylight facade, curtains hanging through the frames, no people

**S37** — The entrance side of a suburban house partially collapsed, the porch roof sagging onto broken supports, the front door hanging from one hinge, harsh sun and deep shadow, no people

**S38** — A dense cloud of pale construction dust hanging in a shaft of hard sunlight inside a wrecked room, particles suspended and glowing amber, abstract and beautiful and terrible, no people

**S39** — Interior view from inside a destroyed living room looking out through a wall that is no longer there, blinding daylight where the wall used to be, a sofa covered in debris, devastating and quiet, no people

**S40** — A family kitchen with the ceiling collapsed onto the counters, cabinets torn open, plaster dust over everything, daylight entering from above through the broken structure, no people

**S41** — An interior hallway with the staircase broken away mid-flight, treads hanging into open air, dust in a hard beam of light, a route through a home that no longer connects, no people

**S42** — A child's bedroom reduced to debris, the small bed crushed under fallen plaster, drawings torn and greyed with dust, a shaft of daylight through the broken wall, no people, no blood

**S43** — A cutaway view of a suburban house with its side wall gone, all the rooms exposed like a doll's house in flat afternoon light, furniture still in place inside, no people

**S44** — Wide establishing shot of a suburban house reduced to a partially collapsed shell in flat afternoon light, walls open to the air, the neighbouring houses untouched and pristine on both sides, brutal contrast, no people

### GROUP 5 — 瓦礫と私物（幕3末〜幕4 / act=3,4）S45–S52 ★**全てSDXL必須**

**S45** — Close-up of ordinary personal belongings half-buried in household debris, a framed photograph lying face-down, a shoe, a coffee mug, covered in white dust, sunlight raking across, deeply human, no faces, no readable text

**S46** — A child's stuffed toy lying in grey plaster dust among broken drywall, one strong shaft of daylight across it, the softness of it against the rubble, no people

**S47** — Shattered dishes and a dining table crushed under fallen ceiling material, a chair on its side, dust settled over everything, hard daylight from a broken wall, no people

**S48** — Two adult silhouettes standing at a distance with their backs to camera, looking at a wrecked house across a lawn in late-afternoon light, small against the damage, entirely unidentifiable, no faces

**S49** — A pile of soaked books and papers in a wrecked room, pages swollen and grey, the print entirely illegible, daylight through a hole in the wall, no people, no readable text

**S50** — A refrigerator tilted against a broken kitchen wall with its door hanging open, a framed picture fallen face-down beside it, plaster dust across the floor, harsh daylight, no people

**S51** — A front doormat and a splintered door lying flat on a debris-covered floor, sunlight through the empty doorway, the entrance to a home reduced to wreckage, no readable text, no people

**S52** — Anonymous hands lifting a dusty cardboard box out of household rubble, framed to show only forearms and hands, hard daylight, salvage after the fact, no faces

### GROUP 6 — 制度の側・書類（幕4 / act=4）S55–S57 ＋ [FACTORY] S53 S54 S58 S59 S60

> **書類の3枚はSDXL必須**（判読不能であることを制御する必要があるため。実写在庫では読める文字が写り込む）。
> **建物・部屋は実写在庫で足りる。**

**S53–S54** — `[FACTORY]` 市庁舎の外観／空の会議室 → §7.3

**S55** — Macro of an official-looking report form on a grey desk in hard side light, the printed lines and typed characters entirely illegible and abstract, a paperclip and a stapler edge, no readable text, no people

**S56** — Close-up of a folded municipal letter on a wooden table in a single beam of daylight, the letterhead and body text completely unreadable and blurred into texture, deliberately impersonal, no readable text, no people

**S57** — Macro of a contractor's estimate sheet with a printed grid of figures rendered completely illegible, a pen resting across it, harsh raking light, the shape of a large number without any number being readable, no readable text

**S58–S60** — `[FACTORY]` 郵便受け／裁判所ファサード／空の法廷 → §7.3

### GROUP 7 — 時間経過と現在（幕4末〜ED / act=4,5）S61–S64 ★**全てSDXL必須**

**S61** — A yellow excavator arm poised over the remains of a suburban house against a wide pale sky, the finality of demolition, dust and shadow, no people

**S62** — An empty flat lot of bare dirt between two intact suburban houses under a wide bright sky, a concrete foundation outline still visible, the absence where a home was, no people

**S63** — The same empty lot at dusk, the concrete foundation outline catching the last low light, the neighbouring houses lit and intact on both sides, a hole in the row of homes, no people

**S64** — A new house frame of raw timber standing on an empty lot in warm low evening sun, unfinished and skeletal against a wide sky, quiet and open-ended, hopeful and unresolved, no people

---

**SDXL生成対象のシーン数を数える:**

```
S01–S09  =  9
S11–S13  =  3
S15      =  1
S21      =  1
S23–S26  =  4
S28–S32  =  5
S33–S44  = 12
S45–S52  =  8
S55–S57  =  3
S61–S64  =  4
--------------
合計       50 シーン    ✓ オーナー確定の 48–50 シーンに一致
50 × 3バリエーション = 150枚
```

---

# 6. A-2/A-3: 静止画のQC・選抜・depth map

## 6.1 機械QC（全150枚に対して必ず実行）

| # | 検査 | 判定 | 落ちたら |
|---|---|---|---|
| Q1 | 解像度 | `max(width, height) >= 3840` | reject |
| Q2 | ファイルサイズ | `> 1024 bytes` かつ PIL で開ける | reject |
| Q3 | 平均輝度 | `45.0 <= mean_luma <= 235.0` | reject。**EP40は昼のエピソードなので白飛び側（>235）が本命のリスク**。`check_visual_asset_qc.DARK_LUMA_FLOOR = 45.0` が暗側の根拠 |
| Q4 | ハイライトのクリップ | 輝度250以上の画素が全体の**3%未満** | reject（昼景の白飛び対策） |
| Q5 | 近似重複 | 全ペアの phash。`check_visual_asset_qc.NEARDUP_SIM = 0.90` に合わせ、**類似度0.90以上のペアは片方を reject** | 片方 reject |
| Q6 | 文字の混入 | **目視。** 読める英字・数字・ロゴが写っていないか | `qc.has_readable_text = true` → reject |
| Q7 | 顔の混入 | **目視。** 識別可能な顔が写っていないか | `qc.has_identifiable_face = true` → reject |

**Q6/Q7 は機械で判定しない。** `--contact-sheet` でコンタクトシートを
`episodes/PD-2026-040-lech/05_visuals/still_contactsheet.png` に出力し、**全150枚を実際に目視すること。**

> **EP38の教訓（記録済み）: ファイル名やプロンプトを信用するな。生成物を実際に見ろ。**
> 「S55 は書類のシーンだからテキストは判読不能のはず」は根拠にならない。SDXL は平気で読める文字を描く。

## 6.2 出力

```
episodes/PD-2026-040-lech/05_visuals/still_qc.v001.json        # 150枚全部の行（rejectも残す）
episodes/PD-2026-040-lech/05_visuals/still_contactsheet.png
```

## 6.3 accepted が110枚に届かなかったとき

```bash
# 落ちた scene だけ _04.._06 を追加生成（冪等・既存はスキップ）
./.venv/Scripts/python.exe scripts/gen_lech_sdxl_batch.py --extra-variations S12,S33,S49
./.venv/Scripts/python.exe scripts/qc_lech_stills.py
```

これを accepted >= 110（body 70 + ae 15 + i2v_source 16 + thumb 9）になるまで繰り返す。
**枚数を減らして基準を下げるのは禁止。**

## 6.4 depth map の生成

`remotion/src/compositions/CaseFilm.tsx` の `treatment: "depth"` は、画像 `<stem>.png` の隣に
`<stem>_depth.png` が**無いとレンダーがクラッシュする**（`Could not load .../<stem>_depth.png`）。

**新規スクリプトを作らず、既存のものを使う:**

```bash
./.venv/Scripts/python.exe scripts/gen_depth_maps.py --dir "H:/pd-media/assets/ai/lech"
```

- モデル: `Intel/dpt-large`（初回は約1.4GBのダウンロード）
- 出力: 入力と同サイズのグレースケール `L` PNG、`<stem>_depth.png`
- `*_depth.png` は入力から自動的に除外される。既存の `_depth` はスキップされる（冪等）
- **role が `body` / `ae` の静止画は depth map が必須。** `thumb` は不要
- staging 後に `remotion/public/lech/img/` 側でも同じペアが揃っていること（§10.1）

---

# 7. A-4: factory 実写クリップ 85本の選定と全点目視QC

## 7.1 在庫の実態（確認済み）

```
H:\pd-media\assets\factory\      フラット構成（エピソード別の入れ子は無い）
  backgrounds/       11,623本（.mp4）  ← ★主力
  light_assets/       1,401
  particle_assets/    1,225
  vfx_overlays/       1,196
  texture_assets/     3,911
  loops/                454
  （ai_video_shots / diagram_assets / lottie_assets / parallax_layers /
    sfx / transitions / typography_assets は空）

ファイル名規約: AF-<TYPECODE>-<4桁連番>__<subtype_slug>.<ext>
  例: H:\pd-media\assets\factory\backgrounds\AF-BG-0460__office_interior_dark.mp4
  TYPECODE = BG | LIGHT | LOOP | PART | TEX | VFX
```

**棚のレジストリ:** `C:\Users\aab15\Documents\prime-documentary\assets\asset_manifest.v001.json`
（トップレベルキーは `schema` と `assets` の2つだけ。`assets` は 88,850 件。**必ず `encoding="utf-8"` で開く**。
Windows の cp932 既定で開くと落ちる。）

> **重要な制約:** バルクのストックエントリは `durationFrames` / `fps` / `width` / `height` / `mood` /
> `intensity` / `colorTone` / `compatibleSceneTypes` が **すべて null または空**。
> 使える選定シグナルは **`type` / `subtype` / `tags` / `sourcePrompt` / `kind`** の5つだけ。
> `path` は `H:\pd-media\assets\` からの相対パス。

## 7.2 選定条件

- **`kind == "video"` のみ。** 静止画の factory は使わない
- **85本ちょうど**（下限は25本。`741.4 / 30 = 24.7`）
- **各1回しか使わない**（`check_asset_reuse.MAX_USES_FACTORY = 1`）
- 幕別の割り当て: 幕1 = 14本 / 幕2 = 24本 / 幕3 = 20本 / 幕4 = 23本 / ED = 4本
- **EP39（夜 / 取調室 / 密室 / 青）の絵柄を選ばない。** 暗い室内・青い照明・クローズドな空間は避ける

**既存の選定ツールを使う（新規に検索ロジックを書くな）:**

```bash
# テーマ一覧と件数
./.venv/Scripts/python.exe scripts/select_factory_assets.py --themes

# 動画だけ・他エピソードで使用済みを除外して候補を出す
./.venv/Scripts/python.exe scripts/select_factory_assets.py \
    --kind video --query suburban --limit 80 --exclude-used --ep PD-2026-040-lech --json
```

`--exclude-used` は `check_arc_nonrepeat.build_universe()` と**同じ**クロスエピソード指紋の集合を使うので、
出荷ゲート `arc_nonrepeat` と食い違わない。**必ず付けること。**

## 7.3 実写在庫でカバーする14シーン（**SDXLで作らない**）

| Sid | 内容 | 検索キーワード例（`--query`） |
|---|---|---|
| S10 | 平穏な郊外の通り（引き） | `suburban` / `residential_street` / `neighborhood` |
| S14 | 最初のパトカー | `police` / `patrol_car` / `emergency_lights` |
| S16 | 封鎖テープ | `police_tape` / `barrier` / `crime_scene` |
| S17 | ブラインド越しの視点 | `window_blinds` / `looking_through_window` |
| S18 | 通りの封鎖（バリケード） | `roadblock` / `barrier` / `cordon` |
| S19 | 無線機の手元 | `radio` / `hands_holding` / `walkie_talkie` |
| S20 | 装備の脚元 | `tactical` / `boots` / `police_gear` |
| S22 | 夜の投光器と住宅地 | `night_street` / `floodlight` / `residential_night` |
| S27 | ドローン | `drone` / `quadcopter` / `aerial` |
| S53 | 市庁舎の外観 | `government_building` / `city_hall` / `municipal` |
| S54 | 空の会議室 | `meeting_room` / `conference_room_empty` |
| S58 | 郵便受け | `mailbox` / `letterbox` |
| S59 | 裁判所ファサード | `courthouse` / `courthouse_steps` / `columns` |
| S60 | 空の法廷 | `courtroom` / `courtroom_interior` |

**残り71本は Sid を持たない繋ぎ・情景クリップ**（`covers_scene_id: null`）。用途:

- 郊外・住宅地の空撮／地上の引き（幕1・幕2の呼吸）
- 空・雲・光の移ろい（幕間の余韻）
- 木材・コンクリート・ガラスのマクロ（破壊の質感の繋ぎ）
- 制度側の建物・廊下・階段（幕4の呼吸）
- 抽象的な `loops`（ドクトリン説明の下地）

## 7.4 ライセンス（`ALLOWED_LICENSES` — これ以外は選ばない）

```python
ALLOWED_LICENSES = {"cc0", "royalty_free", "generated_owned",
                    "Pexels License", "Pixabay Content License"}
```

## 7.5 ★★★ factory のファイル名とサブタイプは信用できない ★★★

> **これは推測ではなく、実際に起きた事故である。**
>
> - **EP36:** `city_surveillance_camera_dome` という名のクリップが、実際には**ベオグラードの大聖堂**だった。
> - **EP38:** **牛の映像**が `documents_on_desk` というラベルで入っていた。
>
> `subtype` は「そういう検索語で取ってきた」という記録であって、**中身の保証ではない。**
> `check_visual_asset_qc.py` がファイル名を信用しない設計になっているのは、この事故が理由。

**したがって、選抜した85本は例外なく次を経ること:**

1. `scripts/build_lech_factory_qc.py` が **1クリップ1フレーム**を ffmpeg で抽出し、
   `episodes/PD-2026-040-lech/05_visuals/factory_contactsheet.png` にコンタクトシートを出力する
2. **あなたがコンタクトシートを実際に開いて、85本すべてを1本ずつ見る**
3. 各本について、`asset_manifest.v001.json` の **`eyeballed_content` に「実際に見た内容」を1文の英語で書く**
   （例: `"an empty municipal lobby, wide static shot, no people"`）。
   **ファイル名を言い換えただけの記述は禁止。** `subtype` と食い違ったら `label_matches_content: false` を立てて**選定から外す**
4. 同時に次を確認して `qc` に記録する:
   - 実写のシネマティックB-rollであること（アニメ・イラスト・CG臭を排除）
   - EP40のテーマ（郊外・昼・破壊・埃・木材・制度）に合っていること
   - ウォーターマーク・ロゴが無いこと
   - 識別可能な実在人物が写っていないこと
5. `05_visuals/factory_clip_qc.v001.json` を**固定タイムスタンプ**で原子的に書く（冪等）

> **★工程時間の見込み:** 85本の抽出とコンタクトシート生成が15分。
> **目視と `eyeballed_content` の記述で最低1時間。** 差し替えが発生すれば再選定＋再目視でさらに30–45分。
> **合計2時間を工程に見込むこと。** ここを飛ばすと、牛が本編に入る。

**1フレームで判断がつかないクリップは、`ffplay` か VLC で**実際に再生して確認する。
静止フレームは「動いていること」を保証しない — near-still なクリップは `check_animation_mix` を落とす。

閾値（`check_visual_asset_qc.py` の実定数）:

```python
DARK_LUMA_FLOOR = 45.0        # 平均輝度がこれ未満のクリップが
MAX_DARK_FRACTION = 0.40      # 全体の40%を超えたら FAIL
NEARDUP_SIM = 0.90            # phash 類似度がこれ以上なら近似重複
MIN_VARIETY = 0.60            # 多様性の下限
```

> **EP40は昼のエピソードなので `DARK_LUMA_FLOOR` は本来余裕がある。**
> ただし夜のシーン（S22）に暗いクリップを寄せすぎると 40% を超えうる。**暗いクリップは全体の3分の1（28本）までに抑える。**

## 7.6 出力

```
episodes/PD-2026-040-lech/05_stock/factory_selection.v001.json   # 選定理由と幕割り当て
episodes/PD-2026-040-lech/05_visuals/factory_clip_qc.v001.json   # ゲートが読む reviewed マニフェスト
episodes/PD-2026-040-lech/05_visuals/factory_contactsheet.png
```

## 7.7 EP39との重複ゼロ（**BLOCKING**）

```bash
./.venv/Scripts/python.exe scripts/select_lech_factory.py --verify-no-ep39-overlap
```

`episodes/PD-2026-039-*/05_stock/stock_ledger*.json` と
`episodes/PD-2026-039-*/05_visuals/asset_manifest*.json`（存在すれば）を**読み取り専用で**開き、
`sha256` の集合と EP40 の選定85本の `sha256` の**積集合が空**であることを確認する。1件でもあれば exit 1 して差し替える。

> **EP39 のファイルは読むだけ。書き込み・移動・削除は一切するな。** EP39は別エージェントが同時に作業している。

---

# 8. A-5: i2v モーション化 16本（Wan 2.2 A14B → RIFE 48fps）

## 8.1 i2v にする16シーン（**動きが意味を持つ絵だけを選ぶ**）

| # | asset_id | 元シーン | 動きの意味 | act |
|---|---|---|---|---|
| 1 | LECH-M01 | S12 | 開いたドアの奥で光が揺れる | 2 |
| 2 | LECH-M02 | S21 | 影が伸びていく（時間経過） | 2 |
| 3 | LECH-M03 | S26 | 発煙缶の煙が広がる | 2 |
| 4 | LECH-M04 | S29 | 装甲車が壁に食い込む | 3 |
| 5 | LECH-M05 | S31 | 落ちた薬莢の上を風が渡る | 3 |
| 6 | LECH-M06 | S33 | 壁が裂けて破片が飛ぶ | 3 |
| 7 | LECH-M07 | S34 | 屋根の穴から光と埃が落ちる | 3 |
| 8 | LECH-M08 | S36 | 窓枠のカーテンが風にあおられる | 3 |
| 9 | LECH-M09 | S38 | 光の柱の中で粉塵が舞う | 3 |
| 10 | LECH-M10 | S39 | 壊れた壁の外を雲が流れる | 3 |
| 11 | LECH-M11 | S43 | 露出した断面に埃が降る | 3 |
| 12 | LECH-M12 | S44 | 崩れた家の上を光が移動する | 3 |
| 13 | LECH-M13 | S45 | 埃が私物の上にゆっくり降る | 4 |
| 14 | LECH-M14 | S49 | 濡れた紙のページがわずかに動く | 4 |
| 15 | LECH-M15 | S61 | 重機のアームが動く | 4 |
| 16 | LECH-M16 | S64 | 夕日が骨組みの上を移動する | 5 |

**元画像は `role: "i2v_source"` として専用に確保し、静止画カットには使わない**（§4.2 の不変条件8）。

## 8.2 Wan 2.2 A14B の設定（**Known-good レジストリ。この値を変えるな**）

`scripts/comfy_wan_lech.py` は既存の `scripts/comfy_wan_kidsforcash.py` を下敷きにし、
**パスと SHOTS だけ差し替える。ノード配線と設定値は1つも変えない。**

```python
HOST   = "http://127.0.0.1:8188"              # ローカル ComfyUI

HIGH   = "wan2.2_i2v_high_noise_14B_fp8_scaled.safetensors"
LOW    = "wan2.2_i2v_low_noise_14B_fp8_scaled.safetensors"
VAE    = "wan_2.1_vae.safetensors"            # ★2.1。2.2 ではない（無言の品質劣化の原因）
CLIP   = "umt5_xxl_fp8_e4m3fn_scaled.safetensors"

WIDTH, HEIGHT = 1280, 720
FRAMES = 41        # 4090 の全ロード上限 @720p。81 にすると部分ロードになり3倍遅くなる
STEPS  = 40
SPLIT  = 20        # 50%で low-noise エキスパートに交代（two-expert MoE）
SHIFT  = 5.0       # ★A14B の値。8.0 は 5B からの無言の持ち越しでバグ
CFG    = 3.5
SAMPLER, SCHEDULER = "euler", "simple"
FPS    = 16        # フレーム計算の会計用

STILL_DIR     = Path(r"H:\pd-media\assets\ai\lech")
VIDEO_OUT_DIR = Path(r"H:\pd-media\assets\ai_video\lech")
GRAPH_DIR     = ROOT / "episodes/PD-2026-040-lech/05_stock/wan_graphs"
CONFORM_DIR   = ROOT / "episodes/PD-2026-040-lech/05_stock/wan_input"
```

**プロンプト:**

```python
POS_PREFIX = "cinematic documentary shot, subtle natural motion, "
POS_SUFFIX = (", slow deliberate camera move, shallow depth of field, film grain, "
              "photoreal, consistent lighting, no sudden changes")
NEG_PROMPT = ("static, motionless, blurry, low quality, distorted, deformed, extra limbs, "
              "bad anatomy, morphing face, flickering, jitter, warping, text, watermark, "
              "identifiable face, real person likeness")
```

**ゲート（`--run` パスにだけ配線し、`--build` / `--dry-run` では実行しない）:**

- `dry_validate`（G-GEN-2）: 本番投入の前に `length=5` で1回POSTして配線エラーを安く検出する
- `assert_loaded_completely`（G-CAP-1）: 部分ロードになっていないこと
- `assert_frame_math`（G-TIME-1）: フレーム数の計算が合っていること

## 8.3 実行手順（**まず1本で通してから残りを回す**）

```bash
# [1] グラフだけ作る（ネットワークもGPUも触らない）
py -3.11 scripts/comfy_wan_lech.py --build

# [2] 1本だけ本番実行して結果を目で確認する
py -3.11 scripts/comfy_wan_lech.py --run --shot S33

# [3] 残り15本をキューに積んで、キューが空になるまでポーリング
py -3.11 scripts/comfy_wan_lech.py --run-all
```

**1本あたり 24–73 GPU分。16本で 6.5–19.5時間。** 進捗は `/queue` と `/history/<prompt_id>` を30秒間隔でポーリングする。
`--run-all` は**すでに出力が存在するショットをスキップ**すること（冪等）。

## 8.4 RIFE で 48fps 化（`scripts/rife_lech.py`）

既存の `scripts/rife_kidsforcash.py` と同じ手順:

```
RIFE = D:/AI/tools/rife-ncnn-vulkan-20221029-windows/rife-ncnn-vulkan.exe
モデル = rife-v4.6
```

1. Wan の出力ディレクトリの先頭 **5フレームは `length=5` の検証プローブなので捨てる**（`DROP_VALIDATE = 5`）
2. 残り41フレームを `f0001.png` 連番にリネームしてステージング
3. RIFE 2x を**2回**（= 4x）→ **164フレーム**
4. 164 / 48fps = **3.417秒**
5. `ffmpeg -framerate 48 -i f%04d.png -c:v libx264 -pix_fmt yuv420p` で
   `H:/pd-media/assets/ai_video/lech/M<NN>_rife.mp4` を書く
6. **フレーム数を検証する。** `n2 >= 4 * n0 - 8` でなければ `SHORT?` として記録し、そのクリップを reject する

## 8.5 i2v の QC

- 顔が生成されていないこと（`NEG_PROMPT` で抑えているが、**必ず目で見る**）
- モーフィング・ちらつき・ワープが無いこと → あれば別シードで再生成
- 3.417秒あるので、Bのカット設計では **1カット 3.0–3.4秒**で使う想定

---

# 9. A-6: 合成レイヤー（distinct 素材に数えない）

**目的:** 静止画カット125本を「止まった絵」にしないための重ね素材。
粉塵・光条・グレインを重ねることで、Ken Burns だけに頼らずに動きを足す。

| 種別 | 在庫 | 選定本数 | 用途 |
|---|---|---|---|
| `particle_assets` | 1,225 | **6本** | 破壊シーンの粉塵。黒背景の drift を screen 合成 |
| `light_assets` | 1,401 | **4本** | 昼光の光条・レンズフレア。壊れた壁からの光に重ねる |
| `vfx_overlays` | 1,196 | **2本** | 微細なグレイン・煙 |
| **合計** | | **12本** | |

**重要なルール:**

1. **合成レイヤーは `check_asset_reuse` の distinct 素材に数えない。** そのため
   `remotion/public/lech/overlay/` に置き、**`lech_film.json` の `cuts[].src` には出さない**。
   （Bが `figures` や専用レイヤーとして扱う。`cuts[].src` に入れると factory 扱いになって1回制限を食う）
2. **同じレイヤーを何度重ねてもよい。** これは「素材」ではなく「加工」である。
3. 黒背景でループするものを選ぶ（screen / add 合成で使うため）。`blend_hint` をマニフェストに書く。
4. **これも §7.5 の目視QC対象。** 12本なので10分で済む。

```bash
./.venv/Scripts/python.exe scripts/select_lech_overlays.py --json
# 出力: episodes/PD-2026-040-lech/05_stock/overlay_selection.v001.json
```

---

# 10. A-7/A-8: staging とマニフェスト出力

## 10.1 Remotion public への staging（`scripts/stage_lech_assets.py`）

```
remotion/public/lech/img/     ← role が body|ae の静止画（+ 同名の _depth.png）
remotion/public/lech/factory/ ← 選定した factory .mp4 85本
remotion/public/lech/motion/  ← i2v の M<NN>_rife.mp4 16本
remotion/public/lech/overlay/ ← 合成レイヤー 12本
```

- `public_path` は `remotion/public/` からの相対パスで、**マニフェストに書く値と実ファイルが一致**すること
- factory の動画は `libx264 crf 16 preset medium -an` で **30fps に conform** してからコピーする
  （`import_to_remotion.py` の `conform_video(..., fps=30)` と同じ扱い）
- i2v は 48fps のまま置く（Bのコンポジションが吸収する）
- **既存ファイルがあり sha256 が一致するならコピーをスキップ**（冪等）

## 10.2 権利台帳 `05_stock/stock_ledger.v001.json`

全静止画・全i2v・全factory・全overlayの1行ずつに:
`asset_id` / `path` / `source`（`ai_codex` または `factory`）/ `license` / `commercial_use` / `sha256` /
`ai_disclosure_required` / `generated_at`。

## 10.3 境界契約マニフェストの出力

```bash
./.venv/Scripts/python.exe scripts/build_lech_asset_manifest.py
./.venv/Scripts/python.exe scripts/build_lech_asset_manifest.py --verify
./.venv/Scripts/python.exe scripts/build_lech_asset_manifest.py --reuse-feasibility
```

**この3つが exit 0 になったら、スレッドBに「マニフェストが本番になった」と伝えてよい。**
Bはそれまでスタブで動いている。**Bのファイルを直接書き換えて知らせようとするな。**

---

# 11. 素材反復禁止ゲートの実仕様（`scripts/check_asset_reuse.py`・確認済み）

```python
MAX_USES_FACTORY = 1        # 無料 + 11,623本ある → 繰り返す理由が無い
MAX_USES_MOTION  = 2        # i2v は1本あたり 24–73 GPU分
MAX_USES_STILL   = 2        # SDXL静止画
MIN_FIRST_USE_SHARE = 0.70  # 全カットの70%以上が「その素材の初出」であること
```

**素材の種別判定は「パス文字列」で行われる**（`kind_of()`）:

```python
p = path.lower().replace("\\", "/")
if "/factory" in p or re.search(r"\baf-bg-", p):   return "factory"
if p.endswith((".mp4", ".mov", ".webm")) or "ai_video" in p or "_rife" in p:  return "motion"
return "still"
```

> **★Aが必ず守るべき命名規則（これを外すとゲートが素材を誤分類する）:**
> - factory の `public_path` は必ず **`lech/factory/`** の下に置く（`/factory` を含む）
> - i2v の `public_path` は必ず **`.mp4`** で終わり、ファイル名に **`_rife`** を含める
> - 静止画の `public_path` は **`.png`** で、パスに `/factory` も `ai_video` も `_rife` も**含めない**
> - 合成レイヤーは `lech/overlay/` に置き、**`cuts[].src` に出さない**（出すと factory 判定になる）

**実測した現状（2026-07-19・全13本がこの基準でFAIL）:**
rodriguez は62枚を188カットに回して平均 **3.03回**、williams は73素材で344カット = 平均 **4.71回**、EP38は平均 **2.12回**。
連続分割はゼロ = すべて「別の絵を挟んで同じ絵が戻ってくる」真の再登場であり、これが「AIスライドショー感」の正体。
最良の rolin は factory 188本を全て1回使用でクリアしており、**この基準は達成可能**。

---

# 12. 字幕の切断規則（**実装はスレッドB。Aは知っておくだけ**）

オーナー指摘: 「字幕がいつも変なところで途切れていた」。**実測で現行全話が14〜32%不正。**
機械ゲート `python scripts/check_caption_breaks.py <captions.srt>` を通すことが出荷条件。

**禁止される3クラス:**

- **A. 行末の機能語** — 行末・キュー末を `the / a / an / to / and / who / that / of / is / for / with ...` で終わらせない
- **B. 孤立キュー** — 1〜2語だけのキューを作らない
  （EP38の実例: `"home."` `"principal."` `"the door."` が単独キューになっていた）
- **C. 句をまたぐ切断** — 悪例: `"...and a ride"` | `"home."` ／ `"the right"` | `"to a lawyer"`

**原因:** `scripts/gen_captions_case.py` の `MAX_WORDS, MAX_CHARS = 7, 42` という**文字数ベースの機械分割**。
→ **構文境界（句・節）で切る実装に置き換える。文字数は上限であって分割基準ではない。**

**Aへの影響:** 無い（Aは字幕を作らない）。ただし **A が i2v / factory のカット長を 3.0秒未満に詰めると、
Bが構文境界で切った字幕がカットに収まらなくなる。** §8.4 の 3.417秒を守ること。

---

# 13. 絶対にやらないこと

- **EP39（frazier）のファイルに一切触らない。** 読み取りのみ可。素材・色・音のレーンも分離する。
  - EP39 = 取調室 / 夜 / 密室 / electric blue `#1F6BFF`
  - EP40 = 郊外の一軒家 / 昼 / 破壊 / gold-amber `#E5B53A`
- **スレッドBの所有ファイル（§0.2.1）に触らない。** 特に `remotion/src/**` と `scripts/ae/**` と `manifest.json`。
- **図解・トランジション・タイポの素材を探しに行かない。** 在庫は0本（§3.2）。**Bが自作する。**
- **課金ジョブを起動しない。** ElevenLabs TTS / 課金画像生成API / YouTubeアップロード。
  ローカルの A1111・ComfyUI・RIFE は**GPUを使うだけで課金は発生しない**ので実行してよい（オーナー許可済み）。
- **公開済み・出荷済みの mp4 を上書き・再レンダリングしない。**
- **「最高裁が判断した」という趣旨の記述をどこにも書かない**（§1）。
- **枚数・本数を「だいたいこのくらい」で決めない。** §3.4 の確定値と §3.6 の検算をそのまま使う。
  自分で計算し直して合わなければ、実装ではなく**本書の側を疑って報告する**。
- **QCを通らなかった素材を「まあ大丈夫だろう」で通さない。** 落ちたら追加生成／再選定する。
- **★ファイル名・subtype・プロンプトを根拠に「この素材は大丈夫」と判断しない。**
  EP36は大聖堂を監視カメラとして、EP38は牛を書類として通した。**生成物・在庫クリップを実際に見ること。**

---

# 14. 完了報告に含めるもの

```
1. accepted 静止画の枚数と内訳（body 70 / ae 15 / i2v_source 16 / thumb 9 / reject N）
2. factory 選定 85本のリスト（asset_id / subtype / eyeballed_content）と
   subtype と中身が食い違って外した本数
3. EP39 重複ゼロの確認結果
4. i2v 16本の frames / duration_sec と、SHORT? になったものの有無
5. 合成レイヤー12本のリスト
6. §0.4 の [A-DONE-1]〜[A-DONE-5] の実行結果（exit code をそのまま貼る）
7. §3.6 の検算 [1]〜[6] を自分で再計算した結果
8. asset_manifest.v001.json の counts ブロック
```

**「動いたと思う」は完了ではない。ゲートが exit 0 を返して初めて完了。**
**自分でQC基準を書き換えて通すことは禁止。**
