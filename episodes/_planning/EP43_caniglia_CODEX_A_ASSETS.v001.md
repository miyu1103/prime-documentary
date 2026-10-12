# EP43 caniglia — Codex スレッドA「素材生成」引き継ぎプロンプト v001

> **このファイルは単体で完結している。他のファイルを読まなくても着手できる。**
> 設計書（DESIGN）も実装スレッドB（CODEX_B）のファイルも**読まなくてよい**（必要な数値はすべて本書に転記済み）。
> **唯一の外部真実 = `episodes/_planning/EP43_caniglia_PRODUCTION_SPEC.v001.json`**（機械生成）。本書の数値はそこから転記したものであり、手書きで発明していない。

```
あなたは Prime Documentary（YouTubeドキュメンタリーチャンネル）の制作エンジニアです。
リポジトリ: C:\Users\aab15\Documents\prime-documentary
Python:     C:\Users\aab15\Documents\prime-documentary\.venv\Scripts\python.exe
メディア:   H:\pd-media
担当:       EP43 / Episode ID: PD-2026-043-caniglia / slug: caniglia
Composition id: Ep43Caniglia（B が Root.tsx に登録・A は staging まで）
```

---

# 0. このスレッド（A）の責務・境界・完了条件

## 0.1 責務（GPU律速・目視律速の長時間ジョブ）

本編で使う「絵」を全部そろえ、1本のマニフェストに書き出すところまで。

| # | 作業 | 成果物 | 目安 |
|---|---|---|---|
| A-1 | SDXL静止画のバッチ生成（**85本の固有プロンプト × 1枚 = 85枚**・バリエーション0） | `H:\pd-media\assets\ai\caniglia\S<NN>.png` | 2–3.5時間（GPU） |
| A-1b | i2v 種画像の生成（**16本の固有プロンプト × 1枚 = 16枚**・バリエーション0） | `H:\pd-media\assets\ai\caniglia\M<NN>_src.png` | 30–50分（GPU） |
| A-2 | 静止画のQCと目視（**目視必須**） | `05_visuals/still_qc.v001.json` + コンタクトシート | 1.5時間 |
| A-3 | depth map 生成（`treatment:"depth"` の必須入力） | `H:\pd-media\assets\ai\caniglia\S<NN>_depth.png` | 20分 |
| A-4 | factory 実写クリップ **93本**の選定と**全点目視QC** | `05_stock/factory_selection.v001.json` / `05_visuals/factory_clip_qc.v001.json` | **2.5時間（うち目視だけで1時間以上）** |
| A-5 | i2v モーション化 **16本**（Wan 2.2 A14B → RIFE 48fps） | `H:\pd-media\assets\ai_video\caniglia\M<NN>_rife.mp4` | 7–19時間（GPU） |
| A-6 | 合成レイヤー（particle/light/vfx）の選定 | `05_stock/overlay_selection.v001.json` | 30分 |
| A-7 | 権利台帳と**境界契約マニフェスト**の出力 | `05_stock/stock_ledger.v001.json` / **`05_visuals/asset_manifest.v001.json`** | 20分 |
| A-8 | Remotion public への staging | `remotion/public/caniglia/{img,factory,motion,overlay}/` | 30分 |

> **★★ 最重要の前提（EP42 から継続）: 1シーン1枚・バリエーション0 ★★**
> Codex の画像生成は高精度。**同一ショットの複数バリエーション（`_02`/`_03`）を作らない。**
> **distinct still を固有プロンプトで各1枚ずつ生成**する（still 85本＝85行の固有プロンプト、各1枚）。
> `generate_sdxl_4k.py` は **`--variants 1`**（または variants 指定なし）で回す。**`--variants 3` は使わない。**
> **総生成画像 = still 85 + i2v 種 16 = 101枚（各1回）。** factory 93本は生成でなく在庫からの選抜。

## 0.2 スレッドB（実装）との境界＝接続点はただ1ファイル

```
episodes/PD-2026-043-caniglia/05_visuals/asset_manifest.v001.json
   ↑ Aが生成（唯一の生産者）        ↓ Bが消費（唯一の消費者・検証者）
```

**Bはこのファイル以外のAの中間生成物を読まない。Aはこのファイル以外のBの成果物に依存しない。** Bはスタブで全パイプラインを完走できるので、Aの完了を待っていない。**A も急がなくてよいが途中経過を壊すな。** このマニフェストは **A(producer)とB(consumer/validator)で counts / role enum を一字一致**で共有する（§4）。

### ファイル所有権（破ると並行作業が壊れる）

| パス | 所有 | Aの権限 |
|---|---|---|
| `H:\pd-media\assets\ai\caniglia\**` / `H:\pd-media\assets\ai_video\caniglia\**` | **A** | 読み書き |
| `episodes/PD-2026-043-caniglia/05_visuals/**` / `05_stock/**` | **A** | 読み書き（`mkdir(parents=True, exist_ok=True)` で自作） |
| `episodes/PD-2026-043-caniglia/04_scenes/ai_prompts.v001.md` | **A**（`generate_sdxl_4k.py` の入力） | 読み書き。B は読むだけ |
| `remotion/public/caniglia/{img,factory,motion,overlay}/**` | **A** | 読み書き |
| `episodes/PD-2026-043-caniglia/manifest.json` `03_script/**` `04_scenes/shotlist*` `08_edit/**` `09_package/**` | **B** | **触るな** |
| `remotion/src/**` `remotion/props/**` `scripts/ae/**` `scripts/build_caniglia_film.py` | **B** | **触るな** |
| `episodes/PD-2026-039-*/**` `episodes/PD-2026-040-*/**` `episodes/PD-2026-041-*/**` `episodes/PD-2026-042-*/**` および EP39/40/41/42 の素材 | 別エージェント | **絶対に触るな。読み取りのみ可** |

## 0.3 A が使う／作るスクリプト

**★既存スクリプトをそのまま使う（新規に作らない）:**

| パス | 役割 | 引数 |
|---|---|---|
| `scripts/generate_sdxl_4k.py`（**既存**） | §5 の SDXL 生成（`04_scenes/ai_prompts.v001.md` を `read_prompts()` で読む） | `PD-2026-043-caniglia --variants 1` / `43 --variants 1 --only S07` |
| `scripts/gen_depth_maps.py`（**既存**） | §6.4 の depth map | `--dir "H:/pd-media/assets/ai/caniglia"` |
| `scripts/build_footage_contact_sheet.py`（**既存**） | §6/§7 の全点目視コンタクトシート | `--ep PD-2026-043-caniglia --media image` / `--media video --dir <staging>` |
| `scripts/select_factory_assets.py`（**既存**） | §7 の factory 候補出し | `--kind video --query <kw> --limit 96 --exclude-used --ep PD-2026-043-caniglia --json` |
| `scripts/check_visual_asset_qc.py`（**既存**） | §0.4 の factory 全点目視ゲート | `--ep PD-2026-043-caniglia` |

**★Aが新規作成するスクリプト（EP42 の young 版を caniglia 用に複製。これ以外を新規に作らない）:**

| パス | 役割 | 下敷き（複製元・EP42） |
|---|---|---|
| `scripts/qc_caniglia_stills.py` | §6 の静止画QC＋解像度チェック | `scripts/qc_young_stills.py` |
| `scripts/select_caniglia_factory.py` | §7 の factory 93本の確定選定・EP39/40/41/42 sha256 除外検証 | `scripts/select_young_factory.py` |
| `scripts/comfy_wan_caniglia.py` | §8 の i2v 16本（Wan 2.2 A14B ドライバ・**パスと SHOTS だけ差し替え**） | `scripts/comfy_wan_young.py` |
| `scripts/rife_caniglia.py` | §8.4 の RIFE 4x → 48fps | `scripts/rife_young.py` |
| `scripts/build_caniglia_asset_manifest.py` | §4 の境界契約マニフェストを出力・自己検証 | `scripts/build_young_asset_manifest.py` |
| `scripts/stage_caniglia_assets.py` | §10 の staging | `scripts/stage_young_assets.py` |

> **SDXL 生成スクリプトを新規に作らない。** `generate_sdxl_4k.py` が既にある（`read_prompts()` で `04_scenes/ai_prompts.v001.md` を読む）。あなたは **`ai_prompts.v001.md` を §5.2 の2行形式で書く**だけ。**実在しないスクリプトを捏造しない**（上の複製元が実在することを `ls scripts/` で確認してから複製する）。
> **正確性ゲートは `check_caniglia_facts.py`（B が実装・DESIGN/A/B で同名）。** A が書く全文字列（プロンプト・`tags`・`caption_hint`・`eyeballed_content`・`notes`）は §1.2 の6制約に一致し、`check_caniglia_facts.py` を将来通せる文言でなければならない。

## 0.4 完了条件（すべて緑で完了。1つでも赤なら未完了）

```bash
cd C:\Users\aab15\Documents\prime-documentary

# [A-DONE-1] 境界契約マニフェストが自己検証を通る
./.venv/Scripts/python.exe scripts/build_caniglia_asset_manifest.py --verify
#   → exit 0。counts が §3/§4 の確定値以上。全パス実在。sha256 重複ゼロ。

# [A-DONE-2] 反復禁止ゲートが素材点数の観点で通る
./.venv/Scripts/python.exe scripts/build_caniglia_asset_manifest.py --reuse-feasibility
#   → still >=85 / motion >=16 / factory >=93 / distinct 合計 >=194 / first-use >=0.70

# [A-DONE-3] 静止画の解像度ゲート（長辺 >=3840）
./.venv/Scripts/python.exe scripts/qc_caniglia_stills.py --check-resolution

# [A-DONE-4] factory の視覚QCゲート（★全93本を目で見た記録があること）
./.venv/Scripts/python.exe scripts/check_visual_asset_qc.py --ep PD-2026-043-caniglia
#   → exit 0（factory_clip_qc.v001.json が staging 済み全クリップを reviewed:true で網羅）

# [A-DONE-5] EP39/EP40/EP41/EP42 との素材被りゼロ
./.venv/Scripts/python.exe scripts/select_caniglia_factory.py --verify-no-prior-overlap
#   → 重複 sha256 = 0（EP39・EP40・EP41・EP42 の四つすべてに対して）
```

---

# 1. ★★★ 最優先の絶対条件（R1 ＋ 正確性6制約）★★★

**Caniglia v. Strom は welfare check からの令状なし立ち入り・押収と、そこに引かれた線の物語。本作の絵は「実在人物の顔・身体・肖像を一切出さない」。象徴オブジェのみ。**

## 1.1 R1（生成ビジュアル全般）

1. **実在人物の顔・likeness・肖像を作らない。** Edward Caniglia（存命私人・R2）、その妻、Cranston の警官、判事（Thomas / Roberts / Breyer / Kavanaugh / Alito）を**顔・身体・肖像として描かない**。人物は必ず後ろ姿・遠いシルエット・顔外し・手元のみ、原則「人を出さない」。
2. **実在の住所・番地・判決文・判例番号・条文の可読文字を再現しない。** 書類・令状・意見書・カレンダー・投票掲示板は雰囲気のみ（判読不能）。判例番号（593 U.S. 194 / 413 U.S. 433 / 953 F.3d 112）・日付・"9-0" は**画像に描かない**（AE/figures のタイポで出す＝B の担当）。
3. AI画像は概要欄でAI生成を開示 → マニフェストの `ai_disclosure_required: true` を全静止画・全i2vに立てる。全生成ビジュアル表示中は右下に `AI-assisted visualization` を常時表示（オーバーレイは B が付与）。

## 1.2 ★正確性6制約（Aが書く全文字列＝プロンプト・`tags`・`caption_hint`・`eyeballed_content`・`notes`・ファイル名に適用。違反はBLOCKER）

1. **射程を過大化しない。** 判決が否定したのは「community caretaking の“住居”拡張」だけ。exigent circumstances / emergency aid の例外は温存。**「警察は令状なしに家に入れない」と断定する文言・絵を作らない**（"police can never enter your home", "warrantless entry is now illegal/banned" 等を書かない）。温存例外（令状・同意・緊急救助）を開いた戸口の象徴で必ず併存させる。
2. **9-0は「破棄・差戻し(vacate & remand)」。** Caniglia の全面勝訴／事件終結と断定しない。**"full victory", "won his case", "case closed/over/ended" を書かない・そう読める祝祭の絵を作らない。** 差戻し＝下級審へ戻す象徴（下の戸口へ返る書類）で示す。
3. **Cady v. Dombrowski の対象は「警察管理下の自動車」。** 住居と混同しない。Cady のプロンプト／タグ／`eyeballed_content` は**車・レッカー・トランク・公道**の象徴のみで、**家と明確に分離**する（"a vehicle is not a house" を絵で示す）。**"cady was a home/house", "a car is a home" を一切書かない。**
4. **Edward Caniglia は R2（存命私人）。** 顔・肖像・身体を描かない。象徴のみ（食卓の拳銃・空のポーチ・救急車の赤色灯・玄関ドア・電話・証拠タグ・布の上の2丁）。個人として同定できる描写をしない。
5. **メンタルヘルス/自殺念慮は非グラフィック・非扇情。** 手段の描写・内面の憶測・自傷の視覚化をしない。危機の一瞬は抑制し、匿名化した象徴（窓に寄りかかる不定形の影）でのみ示す。血・傷・自傷・人に向けた銃口を描かない（§5.5 NEG で抑制）。概要欄に 988 Suicide & Crisis Lifeline を記載（B の package 担当・A は絵で扇情化しないことだけ守る）。
6. **Payton（住居＝第4修正の中心・令状なし立ち入りは presumptively unreasonable）と温存例外を正確に。** 「家は絶対に守られる」と誇張しない（"home is now absolutely protected/safe/off-limits" を書かない）。住居を中心に据えつつ、温存された緊急・同意・令状の戸口を必ず併存させる。

## 1.3 機械ゲート（`build_caniglia_asset_manifest.py --verify` の内部）

A が書いた全JSONの全文字列値に対し、1件でもヒットで exit 1:

```python
import re
BANNED_PORTRAIT = re.compile(
    r"\bportrait\b|\bmugshot\b|likeness of|"
    r"face of (caniglia|edward|thomas|roberts|breyer|kavanaugh|alito|strom)|"
    r"recognizable (real )?person|identifiable face|deepfake|深偽|ディープフェイク",
    re.IGNORECASE)
BANNED_ACCURACY = re.compile(
    r"police (can ?not|can never|are barred from|may never) enter|"
    r"never enter (your|a) home without a warrant|"
    r"warrantless entry (is )?(now )?(illegal|banned|abolished|forbidden|unconstitutional)|"
    r"home is (now )?(absolutely |always )?(protected|safe|off[- ]limits)|"
    r"full (and final )?victory|final victory|won his case|caniglia won|"
    r"case (closed|is over|ended|dismissed)|"
    r"cady was (about )?a (home|house)|a (car|vehicle|automobile) is a (home|house)|"
    r"struck down (the )?(community )?caretaking",
    re.IGNORECASE)
```

> `BANNED_ACCURACY` は制約1〜3・6を機械化したもの。プロンプト・タグ・`caption_hint`・注記のどこにも該当語を書かない。**"a vehicle and a home"／"a vehicle is not a house" は許容（区別を示す・制約3）。禁止は "a vehicle IS a home" 系の混同だけ。**

---

# 2. 台本の語数と尺の確定値（SPEC から転記・Aが素材点数を積算する根拠）

**★唯一の真実 = `episodes/_planning/EP43_caniglia_PRODUCTION_SPEC.v001.json`。** 古い資料の wpm・語数は使うな。

```
words_total          = 2,141
narration_seconds    = 721.3   （= 12.0分）
wpm_used             = 178.1
総尺（設計）          = 733.8秒 = 12:14（narration 721.3 + BrandOpening 3.5 + BrandEndcard 9.0）  ≤ 750s
視覚シーン(narrative)  = 48（S01..S48・SPEC derive）
Act 構成（SPEC）: HOOK 23.2s / OPENING 29.6s / BODY 515.4s（ACT1 The night＋ACT2 The welfare check＋ACT3 The command）/ ENDING 139.8s
```

**Aにとっての意味は1つ:** > **226カット / distinct 194 / 初出85.84% = still 85 + factory 93 + motion 16。**（§3 で積算）

> **注意（命名差）:** SPEC の視覚シーンは S01..S48。しかし **still は 85 本の固有プロンプトを持つ**ため、still の資産 ID は **S01..S85**（1プロンプト＝1枚）で採番する。48 の narrative シーンに 85 枚を配分する（ドクトリン核の ACT3 が最も厚い）。**still 資産 ID（S01..S85）と narrative シーンコード（S01..S48）は別物。** `covers_scene_id` は still 資産 ID 空間を指す（§7.3）。

---

# 3. ★素材構成の確定値（SPEC の distinct/cuts をそのまま調達する）

## 3.1 SPEC の内訳（★この値で調達する・勝手に変えない）

| 種別 | distinct | 担当カット | 使用回数(cap) | 調達方法 |
|---|---|---|---|---|
| **SDXL静止画（本編 body）** | **85枚** | 101カット | 1.19回(≤2) | **85本の固有プロンプトで各1枚**（§5・バリエーション0） |
| **factory 実写クリップ** | **93本** | 93カット | **各1回(1)** | 在庫 11,000本超から選抜（§7）・全点目視・EP39/40/41/42 と sha256 被りゼロ |
| **i2v モーション** | **16本** | 32カット | 各2回(≤2) | 16本の固有種プロンプト→Wan（§8） |
| **合計（カットに出る素材）** | **194点** | **226カット** | | |
| 合成レイヤー（particle/light/vfx） | 12本 | — | 重ね掛け | **distinct 素材に数えない**（§9） |

**SDXL の生成バッチ（本編カットに出ない i2v 種を含む）:**

| 用途 | 点数 | 生成 |
|---|---|---|
| body 静止画（`role:"body"`） | **85枚** | 85プロンプト × 1枚（バリエーション0） |
| i2v 種画像（`role:"i2v_source"`・body と別 asset） | **16枚** | 16種プロンプト × 1枚（バリエーション0） |
| **SDXL 生成バッチ合計** | **85 + 16 = 101枚（各1回）** | **`--variants 1`** |

> **サムネは新規生成しない。** 完成後に body 85枚から6枚を `also_thumb:true` で流用選抜（追加生成ゼロ＝1シーン1枚前提を崩さない）。**role=thumb / still_thumb を作らない。**

> **★紙芝居回避（EP40 の最大の失敗）:** **still-cut 101 / (factory 93 + i2v 32)=video 125** で **still-share 44.69% ≤45%・motion coverage 55.31% ≥45%** を構造的に保証する（§3.3）。**stillを増やしてfactoryを削るな。factory 93 が still-share≤0.45 を守る下限。**

## 3.2 still 85枚・factory 93本・i2v 16本の幕別配分（目安）

| 区間 | narration秒 | still（S番号） | factory | i2v |
|---|---|---|---|---|
| HOOK | 23.2 | 4（S01–S04） | 6 | 2 |
| OPENING | 29.6 | 3（S05–S07） | 3 | 0 |
| ACT1 The night | ~120 | 12（S08–S19） | 12 | 3 |
| ACT2 The welfare check | ~150 | 16（S20–S35） | 16 | 3 |
| ACT3 The command | ~245 | 30（S36–S65） | 24 | 5 |
| ENDING | 139.8 | 20（S66–S85） | 12 | 3 |
| 繋ぎ（covers_scene_id:null） | — | — | 20 | — |
| **合計** | **721.3** | **85** | **93** | **16** |

> ACT3 は他幕の約2倍の尺（ドクトリン核・最も遅く荘厳）なので still も最多の30枚。
> **★幕別の factory 内訳（この表・§7.2・CODEX_B）は非拘束の目安値**（合計 93 のみ確定・幕割当は柔軟）。ゲートは factory を各1回・合計 93 でしか見ない。**確定値は「合計 factory 93」だけ。**

## 3.3 全体の検算（★Codex は自分で再計算して一致を確認）

```
[1] 総カット数 226 = still 101 + factory 93 + i2v 32
[2] 平均ショット長 = (733.8 − OPENING 3.5 − ENDCARD 9.0) / 226 = 721.3/226 = 3.19秒/カット  ✓ (SPEC mean_shot 3.19・≤6.0)
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

**パス:** `episodes/PD-2026-043-caniglia/05_visuals/asset_manifest.v001.json`
**スキーマ版:** `caniglia_assets.v1`（固定文字列）
**生産者:** `scripts/build_caniglia_asset_manifest.py`（**A が実装。他の誰もこのファイルを書かない**）
**★A(producer)とB(consumer/validator)で counts / role enum を一字一致。** role enum は **`body | i2v_source | reject` のみ**（`thumb`/`still_thumb` を作らない）。サムネは `also_thumb:true` の body still **ちょうど6枚**。overlay は **ちょうど12本**。

## 4.1 スキーマ（EP42 の `young_assets.v1` と同型。counts を EP43 値に）

```jsonc
{
  "schema_version": "caniglia_assets.v1",
  "episode_id": "PD-2026-043-caniglia",
  "slug": "caniglia",
  "generated_at": "<ISO8601>",
  "producer": "scripts/build_caniglia_asset_manifest.py",
  "is_stub": false,
  "counts": {
    "still_body": 85,          // ==85
    "still_i2v_source": 16,    // ==16
    "motion": 16,              // ==16
    "factory": 93,             // ==93
    "overlay": 12              // ==12（distinct 素材に数えない）
  },
  "stills": [{
    "asset_id": "CANIGLIA-S01",            // body: ^CANIGLIA-S\d{2}$（1..85） / i2v種: ^CANIGLIA-MS\d{2}$
    "scene_id": "S01",                     // still 資産 ID（§5.9 のプロンプト行に対応・S01..S85 空間）
    "role": "body",                        // body|i2v_source|reject（バリエーション概念なし＝各1枚）
    "also_thumb": false,                   // body から6枚だけ true（追加生成しない）
    "act": 0,                              // 0=HOOK/OPENING, 1=ACT1, 2=ACT2, 3=ACT3, 5=ENDING
    "path": "H:/pd-media/assets/ai/caniglia/S01.png",
    "depth_path": "H:/pd-media/assets/ai/caniglia/S01_depth.png",   // role=="body" は実在必須
    "public_path": "caniglia/img/S01.png", // role=="body" のみ非null
    "width": 3840, "height": 2160,         // 長辺>=3840
    "sha256": "<64hex>", "phash": "<16hex>", "mean_luma": 42.7,
    "tags": ["dining_table","handgun","symbolic","night"],
    "caption_hint": "a handgun rests flat on a dining table",  // check_caniglia_facts 検査対象（制約1-6）
    "seed": 0, "model": "juggernautXL_ragnarokBy",
    "source": "ai_codex", "commercial_use": "allowed", "ai_disclosure_required": true,
    "qc": {"reviewed": true, "on_theme": true, "has_readable_text": false,
           "has_identifiable_face": false, "has_human_body": false, "notes": ""}
  }],
  "motion": [{
    "asset_id": "CANIGLIA-M01",            // ^CANIGLIA-M\d{2}$（1..16）
    "source_scene_id": "M01_src",
    "source_still": "H:/pd-media/assets/ai/caniglia/M01_src.png",   // role=="i2v_source" の画像
    "path": "H:/pd-media/assets/ai_video/caniglia/M01_rife.mp4",
    "public_path": "caniglia/motion/M01_rife.mp4",
    "act": 0, "width": 1280, "height": 720, "fps": 48, "frames": 164, "duration_sec": 3.417,
    "sha256": "<64hex>", "tags": ["handgun","dining_table"],
    "qc": {"reviewed": true, "on_theme": true, "artifact_free": true,
           "has_identifiable_face": false, "notes": ""}
  }],
  "factory": [{
    "asset_id": "AF-BG-0731",              // 棚 assets/asset_manifest.v001.json の id をそのまま
    "path": "H:/pd-media/assets/factory/backgrounds/AF-BG-0731__...mp4",
    "public_path": "caniglia/factory/AF-BG-0731__...mp4",
    "type": "backgrounds", "subtype": "<label>",   // ★ラベル=検索語の記録。中身の保証ではない（§7.5）
    "kind": "video", "license": "Pexels License",  // ALLOWED_LICENSES のいずれか
    "sha256": "<64hex>", "act": 2, "covers_scene_id": "S24",  // §7.3 の割当のみ。繋ぎは null
    "duration_sec": 7.60, "width": 1920, "height": 1080, "mean_luma": 48.3,
    "eyeballed_content": "an ambulance parked outside a suburban house at dawn, red lights turning, no people",  // ★必須（§7.5）
    "qc": {"reviewed": true, "on_theme": true, "no_watermark": true,
           "no_recognizable_person": true, "no_cartoon": true, "label_matches_content": true, "notes": ""}
  }],
  "overlay": [{
    "asset_id": "AF-PART-0044", "path": "H:/.../particle_assets/...mp4",
    "public_path": "caniglia/overlay/...mp4", "type": "particle_assets", "subtype": "<label>",
    "license": "Pexels License", "sha256": "<64hex>", "blend_hint": "screen",
    "eyeballed_content": "slow dust motes drifting on black, loops cleanly",
    "qc": {"reviewed": true, "on_theme": true, "no_watermark": true, "notes": ""}
  }]
}
```

## 4.2 `--verify` の不変条件（BLOCKING・B の validator と一字一致）

1. `schema_version=="caniglia_assets.v1"` / `episode_id`/`slug` 一致 / `is_stub==false`
2. `counts.*` が各配列の実長と完全一致し §4.1 の値（body 85 / i2v_source 16 / motion 16 / factory 93 / overlay 12）に**一致**
3. 全 `path`/`depth_path`/`public_path` がディスクに実在
4. `sha256` が全配列を通して一意（重複ゼロ）
5. `role!="reject"` の全静止画で `max(width,height)>=3840`
6. `role=="body"` は `depth_path` と `public_path` が非null かつ実在
7. `qc.has_readable_text==true` / `qc.has_identifiable_face==true` / `qc.has_human_body==true` のいずれかは `role=="reject"`
8. `role=="i2v_source"` は `role=="body"` と**同一 asset_id を共有しない**（distinct 分離。i2v_source は `CANIGLIA-MS\d{2}`）
9. 全JSON文字列が §1.3 の `BANNED_PORTRAIT` **および** `BANNED_ACCURACY` に一致しない
10. `factory[].license`/`overlay[].license` が `ALLOWED_LICENSES`（§7.4）に含まれる
11. `factory[].sha256` が **EP39・EP40・EP41・EP42 の staged 素材**と1件も衝突しない（§7.7）
12. `factory[].eyeballed_content` が空でない（＝目視していない本が混じっていない）
13. `factory[].qc.label_matches_content==true`
14. `also_thumb==true` の本数が**ちょうど6**、かつ **`scene_id` 集合が `{S01,S24,S28,S30,S49,S81}`（§4.3）と完全一致**（追加生成ではなく body からの流用。**この集合は CODEX_B §11 と一字一致必須の A↔B 契約点**）
15. `role` に `thumb`/`still_thumb` が存在しない（enum は body|i2v_source|reject のみ）
16. `overlay` 配列長が**ちょうど12**

`--reuse-feasibility` では §3.3 [5][6][7] を再計算し、1つでも割ったら exit 1。

## 4.3 `role` の割り当て（機械的に決める）

```
1. body 85枚（S01..S85）= §5.9 の85プロンプトの生成物。各1枚。
2. i2v_source 16枚（MS01..MS16 / 種画像 M01_src..M16_src）= §8.1 の16種プロンプトの生成物。各1枚。body に回さない（不変条件8）。
3. also_thumb : body のうち S01 / S24 / S28 / S30 / S49 / S81 の6枚に true（追加生成しない）
4. reject : QCで落ちたもの（マニフェストに残し理由を qc.notes に）→ 落ちたシーンは §6.3 で同一プロンプト再生成
```

---

# 5. A-1: SDXL 静止画のバッチ生成（85本 × 1枚・バリエーション0）

## 5.1 生成環境（★既存の `generate_sdxl_4k.py` を使う）

```
API:   http://127.0.0.1:7860（ローカル AUTOMATIC1111・課金なし）
モデル: juggernautXL_ragnarokBy（generate_sdxl_4k.py が自動で set_model）
プロンプト元: episodes/PD-2026-043-caniglia/04_scenes/ai_prompts.v001.md   ← A が §5.2 の形式で書く
出力:  H:\pd-media\assets\ai\caniglia\S<NN>.png（+ remotion/public/caniglia/ に自動コピー）
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
- `ai_prompts.v001.md` は **body 85行（S01..S85）＋ i2v 種 16行（M01_src..M16_src、§8.1a）＝ 101 エントリ**を書く。すべて1枚生成。

## 5.3 生成コマンド（★`--variants 1`。`--variants 3` は使わない）

```bash
# まず1枚だけ回して読める行数を確認（★shots=101 でなければ形式が壊れている）
./.venv/Scripts/python.exe scripts/generate_sdxl_4k.py 43 --variants 1 --only S01
#   → ログ "episode=... shots=101 variants=1 ... -> 101 images" の shots が 101 であること

# 全101枚（body 85 + i2v種 16・冪等・長辺>=3840 の既存はスキップ）
./.venv/Scripts/python.exe scripts/generate_sdxl_4k.py PD-2026-043-caniglia --variants 1
#   → 生成 S01.png ... S85.png / M01_src.png ... M16_src.png（各1枚。_02/_03 は作らない）
```

> QC で落ちたシーンの再生成は `--only S37`（**同じプロンプトで別シードを1枚**）。既存の>=3840はスキップ・不足だけ埋まる。**バリエーションを増やして水増ししない。枚数を減らして基準を下げるのも禁止。**

## 5.4 共通スタイル `[STYLE]`（全プロンプト末尾に必ず全文連結）

```
, cinematic still, cold cinematic-documentary grade, deep night-blue and charcoal exterior with a single pool of warm porch-amber and domestic tungsten light, civic and court spaces in pale cold marble grey, restrained and dignified symbolism, telephoto compression and frontal composition, shallow depth of field, ultra-detailed, photoreal, 4K, 16:9, fine film grain, no text, no watermark, no logo, symbolic still-life, no people, no visible face
```

> **EP39/EP40/EP41/EP42 との分離:** `navy`/`electric blue`/`interrogation`（EP39）・`midday sunlight`/`suburban demolition`/`bleached daylight`（EP40）・`prison cell`/`cellblock`/`sodium prison corridor`/`steel death-row`（EP41）・`Chicago apartment`/`ankle monitor`/`body-worn camera vest`（EP42）を**1語も含めない**。EP43 は Rhode Island の一軒家（夜〜夜明け・porch-amber）＋救急車の赤色灯＋Cady の車（レッカー・公道・トランク・家と分離）＋冷たい大理石の裁判所の対比。

## 5.5 共通ネガティブ `[NEG]`（各 `Avoid:` の後に必ず全文付ける）

```
text, words, letters, numbers, captions, watermark, logo, readable document, legible paper, legible case citation, legible docket number, legible date, real celebrity, recognizable real person, identifiable face, portrait, mugshot, likeness of a specific person, human face, human body, nude, bare skin, gore, blood, wound, self-harm, weapon pointed at a person, cartoon, illustration, anime, 3d render, low quality, blurry, jpeg artifacts, deformed, extra limbs, prison cell, steel cellblock, sodium prison corridor, navy interrogation room, electric blue, midday suburban daylight, bleached sunlight
```

> ネガティブにも **制約違反語（"police can never enter", "warrantless entry banned", "full victory", "a car is a home" 等）を書かない**（§1.3）。上のリストにも含めていない。**血・傷・自傷・人に向けた銃口を NEG で抑制**（制約5・非グラフィック）。

## 5.6 バリエーション軸（★EP43 では無効）

`generate_sdxl_4k.py` の `--variants 1` は各 stem を**1枚だけ**生成する。**`_02`/`_03` を作らない。** 反復回避は「85本の固有プロンプト＝85の別被写体」で担保する。

## 5.7 メタJSON

`generate_sdxl_4k.py` は画像を書くが per-image メタJSONは書かない。**A は QC 時に `qc_caniglia_stills.py` で各画像の `sha256`/`phash`/`mean_luma`/`long_edge` を測り `still_qc.v001.json` に記録する**（§6.2）。

## 5.8 プロンプトの絶対ルール（85本すべてに適用）

- **顔なし・身体なし・裸体なし。** 人物は原則出さない。出す場合は遠いシルエット/後ろ姿/影のみ（制約4・R1）。
- **可読文字なし。** 令状・意見書・判例番号・カレンダー・投票掲示板は雰囲気のみ（判読不能）。日付・数値は描かない。
- **Edward Caniglia を個人として描かない**（制約4）。象徴オブジェのみ（食卓の拳銃・空のポーチ・救急車・玄関・電話・証拠タグ）。
- **射程を過大化しない**（制約1）: 温存例外を「開いた戸口」で必ず併存させる。「令状なしに家に入れない」祝祭に見えるものを作らない。
- **9-0＝差戻し**（制約2）: 「全面勝訴」に見せない。差戻しは「下級審へ返る書類」で示す。
- **Cady＝車**（制約3）: レッカー・公道・トランクの象徴で、**家と明確に分離**。車を家と混同させる絵を作らない。
- **メンタルヘルス非扇情**（制約5）: 危機は匿名の影・抑制で示し、自傷・血・手段を描かない。

## 5.9 確定プロンプト（★`ai_prompts.v001.md` にこの85エントリをそのまま書く・各1枚）

> 各行の `[STYLE]` は §5.4 を、`Avoid:` の後の `[NEG]` は §5.5 を**全文展開**して書く（下記は簡潔表記のマクロ。省略記号ではなく定義済み定数）。全て顔なし・身体なし・象徴・判読不能。

```
- `S01.png`
A single handgun lying flat on a dark wooden dining table under a warm low lamp in a dim room, the object still and cold, the quiet center of everything, non-graphic and symbolic, no people, no hand [STYLE] Avoid: [NEG]
- `S02.png`
A packed overnight bag set down beside a closed front door in a dim hallway, a folded coat resting on top, someone about to leave implied only by the objects, no body, no face [STYLE] Avoid: [NEG]
- `S03.png`
Two distant faint silhouettes standing apart on a dark porch at night seen from across the street, only vague shapes against a single amber doorway light, no faces, no detail, symbolic [STYLE] Avoid: [NEG]
- `S04.png`
A small paper evidence tag tied to the handle of a sealed bag on a dark surface, the writing on it abstract and unreadable, the moment an ordinary object becomes evidence, no legible text, no people [STYLE] Avoid: [NEG]
- `S05.png`
A plain single-family house front door in a New England neighbourhood seen straight on at night, an ordinary porch light glowing warm amber, closed and unremarkable, the everyday door the whole story turns on, no people, no readable number [STYLE] Avoid: [NEG]
- `S06.png`
The pale marble facade and tall columns of a supreme high court at night, cold stone lit from below, monumental and distant, the far place a private night was dragged to, no people, no readable inscription [STYLE] Avoid: [NEG]
- `S07.png`
A residential front door at the end of a dark hallway with a faint grid of cold light lines cast across the walls, quiet anticipation, the threshold before the question, no people, no text [STYLE] Avoid: [NEG]
- `S08.png`
A dining table left after an argument that has gone cold, two chairs with one pushed back at an angle, a single warm lamp, tension abandoned in an empty room, no people [STYLE] Avoid: [NEG]
- `S09.png`
A handgun resting flat on a dining table beside a folded newspaper under warm tungsten light, simply set down and untouched, a record fact rendered without any drama, non-graphic, no people, no hand [STYLE] Avoid: [NEG]
- `S10.png`
A landline phone and a mobile phone lying dark on a kitchen counter at night, no glow on either screen, the calls not yet made, quiet, no people, no readable screen [STYLE] Avoid: [NEG]
- `S11.png`
A woman's coat lifted from the back of a chair and a half-packed overnight bag on a bed in a dim bedroom, a careful decision to leave shown only by clothes and luggage, no body, no face [STYLE] Avoid: [NEG]
- `S12.png`
A front door seen from inside a dark house as it closes, a thin blade of hallway light narrowing toward nothing, someone walking out implied only by the shrinking gap, no people [STYLE] Avoid: [NEG]
- `S13.png`
A hotel key card lying on an unfamiliar nightstand beside a switched-off lamp at night, a strange room, safety found somewhere that is not home, no people, no readable text [STYLE] Avoid: [NEG]
- `S14.png`
An anonymous hotel room at night lit by one bedside lamp, a made bed and a drawn curtain, the impersonal place a night is spent, quiet and unfamiliar, no people [STYLE] Avoid: [NEG]
- `S15.png`
Grey first light falling on a closed residential front door from outside, the amber porch light still burning into the morning, nothing yet disturbed, no people, no readable number [STYLE] Avoid: [NEG]
- `S16.png`
The same dining table in cold early-morning light, the lamp now off and the surface quiet, the night receded, the ordinary room after everything, no people, no legible objects [STYLE] Avoid: [NEG]
- `S17.png`
A wall calendar in a dim kitchen turned to a late-summer month, the dates abstract and unreadable, August of a single year, cold morning light, no legible numbers, no people [STYLE] Avoid: [NEG]
- `S18.png`
A quiet suburban house exterior at dawn with the front door closed and the porch light fading against a brightening sky, ordinary and still, the crisis mostly passed, no people [STYLE] Avoid: [NEG]
- `S19.png`
A mobile phone resting on a nightstand at morning showing a blank unlit screen, a call that goes unanswered, no glow, no readable text, no people [STYLE] Avoid: [NEG]
- `S20.png`
A close view of a phone lying on a table mid-call, the screen an abstract soft glow with no readable text, a non-emergency call being placed, quiet worry, no people, no legible screen [STYLE] Avoid: [NEG]
- `S21.png`
A police non-emergency dispatch desk at night with a dim console and a single lamp, an ordinary welfare-check request logged without alarm, no people, no readable screen, no legible text [STYLE] Avoid: [NEG]
- `S22.png`
A police patrol car parked at the curb outside a modest house at first light, its roof lights dark, an unhurried arrival for a welfare check, no people, no readable markings [STYLE] Avoid: [NEG]
- `S23.png`
An empty residential porch in the grey morning with a single chair and an open screen door, the calm place a conversation happened, the man found alive and talking implied only by absence, no people [STYLE] Avoid: [NEG]
- `S24.png`
An ambulance parked outside a suburban house at dawn with its red emergency lights turning, the red glow washing across the pale siding, a quiet non-crisis departure, no people, no readable text [STYLE] Avoid: [NEG]
- `S25.png`
Red ambulance light sweeping across the amber-lit wall and drawn curtains of a house at dawn, alternating warm and cold, the moment the man is taken to be evaluated, non-graphic, no people [STYLE] Avoid: [NEG]
- `S26.png`
The empty porch again after the ambulance has gone, a screen door left ajar, the morning settling back into quiet, no people [STYLE] Avoid: [NEG]
- `S27.png`
A hospital entrance canopy seen from a distance at morning, cold institutional light over an empty drive, the place a voluntary evaluation happens, no people, no readable signage [STYLE] Avoid: [NEG]
- `S28.png`
Two handguns laid side by side on a folded cloth on a dark table, cold light on the metal, lawfully owned property about to be carried out of a home, non-graphic, no people, no hand [STYLE] Avoid: [NEG]
- `S29.png`
A clear sealed evidence bag holding two handguns resting on a table under cold light, the firearms taken from a house, no legible label, no people [STYLE] Avoid: [NEG]
- `S30.png`
An ordinary residential front door standing wide open onto a dark interior in the morning, no one there, the threshold crossed while the owner was already gone, no people, no readable number [STYLE] Avoid: [NEG]
- `S31.png`
An open bedroom drawer and a disturbed closet shelf in a dim house where firearms had been stored, the private interior entered, no people, no legible objects [STYLE] Avoid: [NEG]
- `S32.png`
A paper evidence tag tied to the handle of a sealed bag under cold light, the handwriting abstract and unreadable, two lawful objects reclassified, no legible text, no people [STYLE] Avoid: [NEG]
- `S33.png`
A quiet county courthouse exterior at dusk, cold stone steps and closed doors, the place a man later went just to get his own property back, no people, no readable sign [STYLE] Avoid: [NEG]
- `S34.png`
An extreme close view of a residential front-door edge and its brass strike plate in cold light, the boundary itself, the question of who gets to open it, no people, no text [STYLE] Avoid: [NEG]
- `S35.png`
A single handgun resting on a cloth beside a folded property-return form on a dark desk, the smaller fight over lawful property, the form's text abstract and unreadable, non-graphic, no legible words, no people [STYLE] Avoid: [NEG]
- `S36.png`
A federal district courthouse corridor at night in cold marble, closed chamber doors receding into shadow, the first ruling that went against him, no people, no readable inscription [STYLE] Avoid: [NEG]
- `S37.png`
The cold stone facade of a federal court of appeals building lit at night, tall and institutional, the appellate court that reached further, no people, no readable sign [STYLE] Avoid: [NEG]
- `S38.png`
A folded court opinion resting face-up under a desk lamp with its printed lines reduced to abstract illegible marks, a lower-court decision as a plain object, no legible text, no people [STYLE] Avoid: [NEG]
- `S39.png`
A single skeleton key hovering just above a residential front-door lock in cold light, the idea that a caretaking rationale could open any door, symbolic and abstract, no people, no text [STYLE] Avoid: [NEG]
- `S40.png`
A long row of identical closed front doors down a dark corridor, any one of them openable by the same excuse, the reach of a free-floating power rendered abstractly, no people, no readable numbers [STYLE] Avoid: [NEG]
- `S41.png`
A private automobile loaded onto a tow-truck flatbed under a sodium lot light at night, a car taken into police custody, clearly a vehicle and not a home, no people, no readable plate [STYLE] Avoid: [NEG]
- `S42.png`
An open car trunk in a dark impound lot with a flashlight beam reaching inside it, an automobile being searched, the car-lot origin of a rule, plainly a vehicle and never a house, no people, no readable text [STYLE] Avoid: [NEG]
- `S43.png`
A single car stopped on the shoulder of an empty public highway at night, headlights spilling on the asphalt, a vehicle on a public road, unmistakably not a home, no people, no readable plate [STYLE] Avoid: [NEG]
- `S44.png`
A tow truck hauling a wrecked car along a dark highway, red tail lights receding, the routine non-criminal business of clearing a road, a car and never a home, no people [STYLE] Avoid: [NEG]
- `S45.png`
A cold marble surface split by one hard line of shadow, a small toy-scale car resting on one side and a solid house-shaped block on the other, the plain difference between a vehicle and a home rendered abstractly, no people, no text [STYLE] Avoid: [NEG]
- `S46.png`
A stark abstract map of many regions in cold light, some doorways marked open and others marked closed, the lower courts that had split over the question, no readable names, no people [STYLE] Avoid: [NEG]
- `S47.png`
Tall closed bronze doors of a high court seen frontally in cold marble light, the case carried up to be decided, monumental and shut, no people, no readable inscription [STYLE] Avoid: [NEG]
- `S48.png`
The interior of a grand marble high-court chamber photographed frontally, monumental columns and cold pale stone, solemn and empty, no people, no readable inscription [STYLE] Avoid: [NEG]
- `S49.png`
A long judicial bench with nine tall vacant high-backed seats aligned behind it in cold marble light, a unanimous court rendered as empty chairs, no people, no text [STYLE] Avoid: [NEG]
- `S50.png`
A wooden gavel resting unused on its sound block on an empty bench under cold light, the instrument of a narrow ruling lying still, no people, no text [STYLE] Avoid: [NEG]
- `S51.png`
A single fountain pen laid across a blank sheet on a marble bench under one light, the writing of the Court's opinion implied by absence, no legible text, no face, no people [STYLE] Avoid: [NEG]
- `S52.png`
A single thin band of pale engraved-looking light running across a cold marble wall, the very core of a guarantee rendered as light, the characters abstract and unreadable, no legible words, no people [STYLE] Avoid: [NEG]
- `S53.png`
A plain residential front-door threshold rendered in warm amber light set inside a cold marble frame, the home placed at the center of the law, no people, no readable number [STYLE] Avoid: [NEG]
- `S54.png`
A closed residential front door with a faint presumptive seal of cold light around its edges, guarded as a rule yet not without exception, quiet and severe, no people, no text [STYLE] Avoid: [NEG]
- `S55.png`
A folded newspaper lying under a desk lamp with an abstract unreadable banner headline, the unanimous headline that turns out to be a trap, no legible words, no people [STYLE] Avoid: [NEG]
- `S56.png`
Three doors along a marble wall standing open in warm light while a fourth is sealed cold, the exceptions that remained open beside the one excuse that closed, no people, no text [STYLE] Avoid: [NEG]
- `S57.png`
A folded legal document with an abstract illegible signature block resting on a table under one lamp, a valid warrant as a plain object, one door still open, no legible words, no people [STYLE] Avoid: [NEG]
- `S58.png`
A residential front door opened from the inside a careful hand's width onto warm light, consent given at the threshold, one door still open, no people, no face [STYLE] Avoid: [NEG]
- `S59.png`
An indistinct shape slumped against a lit window seen from outside a dark house, a genuine emergency judged from the porch, deliberately anonymous and non-graphic, no face, no visible body detail [STYLE] Avoid: [NEG]
- `S60.png`
Three separate short stacks of pages set slightly apart from a thick closed folder on a dark bench, three justices writing separately, cold light, no legible text, no people [STYLE] Avoid: [NEG]
- `S61.png`
A single sheet held slightly apart under warm light with a faint symbol of a helping hand reaching toward a threshold, the point that a genuine rescue needs no warrant, abstract, no legible words, no people [STYLE] Avoid: [NEG]
- `S62.png`
A porch light left burning beside an unanswered door for a missing elderly neighbour at dusk, the ordinary emergencies the ruling leaves untouched, symbolic and restrained, no people, no text [STYLE] Avoid: [NEG]
- `S63.png`
A single ordinance-looking page stamped and set to one side of a marble desk, the hard questions about firearm-removal laws marked for another day, the text abstract and unreadable, no legible words, no people [STYLE] Avoid: [NEG]
- `S64.png`
A case folder lifted off a marble bench and turned back toward a lower doorway, the decision vacated and sent back down rather than ended, cold light, no legible text, no people [STYLE] Avoid: [NEG]
- `S65.png`
A single blank index card lifted and removed from a row of standing cards on a dark table, one excuse taken off the table while the rest are left standing, no legible text, no people [STYLE] Avoid: [NEG]
- `S66.png`
An overnight bag set down again beside a quiet front door in soft morning light, the woman who did the humane thing returning to the frame, no body, no face [STYLE] Avoid: [NEG]
- `S67.png`
An anonymous hotel room in pale morning light with the curtain half-drawn, the safe place a night was spent, quiet and impersonal, no people [STYLE] Avoid: [NEG]
- `S68.png`
A phone lying on a kitchen counter in warm morning light just after a call, the humane request that set everything in motion, no glow, no readable screen, no people [STYLE] Avoid: [NEG]
- `S69.png`
A sealed bag of two handguns being carried out through an open front door into daylight, lawful property leaving a shared home, non-graphic, no face, no visible body [STYLE] Avoid: [NEG]
- `S70.png`
A single house key resting in the amber pool of a porch light beside a front door, a kindness that arrived carrying a key, quiet and ambiguous, no people, no text [STYLE] Avoid: [NEG]
- `S71.png`
A residential front door standing open with warm helpful light pouring out onto the step, the hardest reason to refuse, the offer of help at the threshold, no people, no readable number [STYLE] Avoid: [NEG]
- `S72.png`
A calendar page turned to a late-spring month in cold court light, the month the Court gave its answer, the numbers abstract and unreadable, no legible date, no people [STYLE] Avoid: [NEG]
- `S73.png`
A skeleton key held against a residential lock that no longer turns for it, the caretaking excuse that can no longer open this door, symbolic and abstract, no people, no text [STYLE] Avoid: [NEG]
- `S74.png`
A residential front door standing wide open onto bright daylight, the emergency door left deliberately wide, an opening the law still allows, no people, no readable number [STYLE] Avoid: [NEG]
- `S75.png`
A row of stamped pages waiting in line along a marble desk, the harder questions postponed rather than answered, the text abstract and unreadable, no legible words, no people [STYLE] Avoid: [NEG]
- `S76.png`
A dark screen showing an abstract flagged marker over a stylised cold-blue map, a firearm-removal question rendered coldly and without people, no readable place names, no people [STYLE] Avoid: [NEG]
- `S77.png`
A single porch light left burning at dusk beside a neighbour's closed door, the hardest case of a person feared for, restrained and non-graphic, symbolic only, no people, no text [STYLE] Avoid: [NEG]
- `S78.png`
A row of small lower-court chambers with lit windows below one great dark courthouse, the arguments being written in the courts below, cold light, no people, no readable signage [STYLE] Avoid: [NEG]
- `S79.png`
Nine tall vacant seats aligned behind a marble bench in cold light, the nine who agreed on one narrow thing, unanimous and still, no people, no text [STYLE] Avoid: [NEG]
- `S80.png`
Three doorways standing wide open in warm light along a long marble wall, what the ruling left standing beside it, the warrant and the consent and every real emergency, no people, no text [STYLE] Avoid: [NEG]
- `S81.png`
A residential front door standing open with clear daylight behind it, the held final image, quiet resolution without triumph, no people, no readable number [STYLE] Avoid: [NEG]
- `S82.png`
Warm dawn light spilling through an open front door across a dark hallway floor, morning arriving on the far side of the threshold, quiet, no people [STYLE] Avoid: [NEG]
- `S83.png`
A residential front-door threshold and worn sill catching the first pale light of morning, the ordinary boundary of a home at rest, no people, no readable number [STYLE] Avoid: [NEG]
- `S84.png`
A single lit window with the last deep blue of night turning to grey dawn over a quiet residential skyline, one warm room among many, open-ended, no people, no visible address [STYLE] Avoid: [NEG]
- `S85.png`
A closed residential front door with warm porch-amber light returning around its edges at dawn, a slow pull-back composition, quiet and unresolved, the door of a home at the end of everything, no people, no readable number [STYLE] Avoid: [NEG]
```

**枚数チェック:** 上記 85 エントリ（S01..S85）。§5.3 の `--only S01` ログで `shots=101`（body 85 + i2v種 16）を確認してから本番を回す。

---

# 6. A-2/A-3: 静止画のQC・目視・depth map

## 6.1 機械QC（body 85 + i2v種 16 = 全101枚・`qc_caniglia_stills.py`）

| # | 検査 | 判定 | 落ちたら |
|---|---|---|---|
| Q1 | 解像度 | `max(w,h)>=3840` | reject |
| Q2 | サイズ/開ける | `>1024 bytes` かつ PIL で開ける | reject |
| Q3 | 平均輝度 | `35.0<=mean_luma<=225.0`（EP43は夜〜夜明けのエピソード→黒潰れ側が本命リスク。`check_visual_asset_qc.DARK_LUMA_FLOOR=45.0` を下回りすぎる本に注意） | reject |
| Q4 | 近似重複 | 全ペア phash。類似度 `>=0.90` は片方 reject（`check_visual_asset_qc.NEARDUP_SIM=0.90`）。**バリエーション0なので本来ほぼ衝突しないはず。衝突したらプロンプトが被っている**（特に多数ある「玄関ドア」「大理石」系に注意） | 片方 reject＋プロンプト見直し |
| Q5 | 文字の混入 | **目視。** 読める英字・数字・判例番号・日付・ロゴが写っていないか（R1・制約2） | `has_readable_text=true`→reject |
| Q6 | 顔の混入 | **目視。** 識別可能な顔が写っていないか（R1・制約4） | `has_identifiable_face=true`→reject |
| Q7 | 身体の混入 | **目視。** 人体・裸体・自傷が写っていないか（制約4/5） | `has_human_body=true`→reject |

**Q5/Q6/Q7 は機械で判定しない。** コンタクトシートを出して**全101枚を実際に目視**する:

```bash
./.venv/Scripts/python.exe scripts/build_footage_contact_sheet.py --ep PD-2026-043-caniglia --media image
#   → runs/qc/caniglia_footage_contact_NN.png（20枚/シート）。全シートを開いて1枚ずつ見る
```

> **EP38/EP39-42 の教訓: ファイル名・プロンプトを信じるな。生成物を実際に見ろ。** SDXL は平気で読める文字・顔・身体を描く。**特に制約4（Caniglia 非人物化）・制約5（自傷/危機の非グラフィック）は目視でしか守れない。** S59・S77 のような危機の象徴は、血・傷・手段・人体が写っていないことを必ず目で確認する。S01/S09/S28/S29/S35/S69 の拳銃は**人に向いていない・手が写っていない**ことを確認（制約5・NEG "weapon pointed at a person"）。

## 6.2 出力

```
episodes/PD-2026-043-caniglia/05_visuals/still_qc.v001.json     # 101枚全部の行（reject も残す・sha256/phash/mean_luma/long_edge）
（build_footage_contact_sheet が runs/qc に出す）
```

## 6.3 accepted が101枚に届かなかったとき

```bash
./.venv/Scripts/python.exe scripts/generate_sdxl_4k.py 43 --variants 1 --only S37   # 落ちたシーンだけ同一プロンプトで別シード1枚
./.venv/Scripts/python.exe scripts/qc_caniglia_stills.py
```
accepted body >= 85 かつ i2v_source >= 16 になるまで繰り返す。**基準を下げない・バリエーションを足して水増ししない。**

## 6.4 depth map（★新規スクリプトを作らず既存を使う）

```bash
./.venv/Scripts/python.exe scripts/gen_depth_maps.py --dir "H:/pd-media/assets/ai/caniglia"
```
- モデル `Intel/dpt-large`。出力 `<stem>_depth.png`（同サイズ L グレースケール）。冪等。
- **role が `body` の静止画は depth 必須**（`treatment:"depth"` が隣に `_depth.png` を要求。無いとレンダーがクラッシュ）。i2v 種（`M<NN>_src.png`）は depth 不要。
- staging 後に `remotion/public/caniglia/img/` 側でも同名ペアが揃っていること（§10）。

---

# 7. A-4: factory 実写クリップ 93本の選定と全点目視QC

## 7.1 在庫の実態

```
H:\pd-media\assets\factory\   フラット構成
  backgrounds/     11,000本超（.mp4）  ← ★主力（RI 住宅街夜景・porch・玄関・救急車・警察車・裁判所/大理石・廊下・公道/レッカー・夜明け・繋ぎ）
  light_assets/    …            合成レイヤー（光条・porch amber・救急赤）
  particle_assets/ …            合成レイヤー（埃・塵）
  vfx_overlays/    …            合成レイヤー（グレイン・光ノイズ）
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
- 幕別割り当て（§3.2）: HOOK=6 / OPENING=3 / ACT1=12 / ACT2=16 / ACT3=24 / ED=12 ＋ 繋ぎ=20 ＝ 93
- **EP39（夜/取調室/青）・EP40（郊外/昼/破壊）・EP41（監獄/鉄/石の独房）・EP42（シカゴのアパート/足首モニタ）の絵柄を選ばない。** EP43 は RI の一軒家（夜〜夜明け・porch-amber）＋救急車の赤色灯＋Cady の車（レッカー/公道/トランク・家と分離）＋冷たい大理石の裁判所

**既存の選定ツールで候補出し（新規に検索ロジックを書くな）:**

```bash
./.venv/Scripts/python.exe scripts/select_factory_assets.py --themes   # テーマ一覧と件数
./.venv/Scripts/python.exe scripts/select_factory_assets.py \
    --kind video --query courthouse --limit 96 --exclude-used --ep PD-2026-043-caniglia --json
```
`--exclude-used` は `check_arc_nonrepeat.build_universe()` と同じ指紋集合を使うので出荷ゲート `arc_nonrepeat` と食い違わない。**必ず付ける。**

## 7.3 実写在庫でカバーする代表シーン（`covers_scene_id` を付ける・SDXLで作らない情景）

> **★`covers_scene_id` は still 資産 ID 空間（S01..S85・§2 注記）を指す。narrative シーン（DESIGN の S01..S48）とは別体系。** B はこの値を still 資産 ID として解決し、narrative シーンコードにクロスマップしない。

| covers | 内容 | `--query` 例 | 幕(act) |
|---|---|---|---|
| S05 | RI 一軒家の玄関/外観（夜・porch light） | `residential_house_night` / `suburban_house_exterior_night` | 0 |
| S06 | 最高裁/大法廷ファサード・列柱 | `supreme_court_building` / `marble_columns` | 3 |
| S22 | 住宅街に停まる警察車（welfare check・無人） | `police_car_residential_night` / `patrol_car_street` | 2 |
| S24 | 一軒家前の救急車・赤色灯 | `ambulance_night` / `ambulance_lights_house` | 2 |
| S27 | 病院入口キャノピー（無人） | `hospital_entrance_night` / `hospital_exterior` | 2 |
| S33 | 郡裁判所の外観（夕・無人） | `courthouse_exterior` / `courthouse_night` | 2 |
| S37 | 連邦控訴審の建物ファサード | `court_building_facade` / `federal_courthouse` | 3 |
| S43 | 夜の公道に停まる車（Cady・家と分離） | `empty_highway_night` / `car_highway_shoulder` | 3 |
| S48 | 大理石の大法廷内観（無人） | `courtroom_interior` / `marble_chamber` | 3 |
| S78 | 下級審の法廷（無人） | `empty_courtroom` / `court_chamber` | 5 |
| S84 | 夜明けの住宅街スカイライン | `dawn_skyline` / `blue_hour_neighborhood` | 5 |

**残り本数は covers を持たない繋ぎ・情景クリップ**（`covers_scene_id:null`）: 住宅街の夜道・porch と玄関・大理石/石の廊下・電話/dispatch 卓・レッカー/impound（**Cady 用＝車のみ・家を写さない**）・夜〜夜明けの空・雨のアスファルト・冷たい窓・抽象 `loops`。**暗いクリップに偏りすぎない**（§7.5 の暗側閾値・全体の1/3=約31本まで。porch light / 街灯 / 夜明け側を優先）。

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
    --ep PD-2026-043-caniglia --media video --dir "<93本の staging フォルダ>"
#   → runs/qc/caniglia_footage_contact_NN.png（各タイルにファイル名ラベル）
```

2. **コンタクトシートを実際に開き、93本すべてを1本ずつ見る**
3. 各本について `asset_manifest.v001.json` の **`eyeballed_content` に「実際に見た内容」を1文の英語で書く**（ファイル名の言い換え禁止）。`subtype` と食い違ったら `label_matches_content:false` を立てて**選定から外す**
4. 実写シネマティックB-roll（アニメ/CG臭排除）・EP43テーマ（RI 住宅の夜〜夜明け/救急車/警察車/裁判所/公道の車）・ウォーターマークなし・識別可能な実在人物なし（制約4・R1）を確認
5. **★制約3の目視:** Cady 用クリップ（S41/S43/S44 系・レッカー/公道/トランク）は **`eyeballed_content` に「a vehicle, no house in frame」を必ず明記**。家が同フレームに写る車クリップは Cady に使わない（車と家の混同を作らない）
6. `05_visuals/factory_clip_qc.v001.json` を固定タイムスタンプで原子的に書く（冪等）

閾値（`check_visual_asset_qc.py`）: `DARK_LUMA_FLOOR=45.0` / `MAX_DARK_FRACTION=0.40` / `NEARDUP_SIM=0.90` / `MIN_VARIETY=0.60`。
> **EP43 は夜〜夜明けのエピソードなので暗側が本命リスク。** 平均輝度45未満のクリップが全体の40%を超えると FAIL。**暗いクリップは約31本（1/3）までに抑え、porch light・街灯・救急赤・夜明けの実用光がある本を優先する。**

**1フレームで判断がつかない本は VLC/ffplay で再生して確認**（near-still は `check_animation_mix` を落とす）。

## 7.6 出力

```
episodes/PD-2026-043-caniglia/05_stock/factory_selection.v001.json   # 選定理由と幕割り当て
episodes/PD-2026-043-caniglia/05_visuals/factory_clip_qc.v001.json   # ゲートが読む reviewed マニフェスト
```

## 7.7 EP39/EP40/EP41/EP42 との重複ゼロ（BLOCKING）

```bash
./.venv/Scripts/python.exe scripts/select_caniglia_factory.py --verify-no-prior-overlap
```
`episodes/PD-2026-039-*/` `episodes/PD-2026-040-*/` `episodes/PD-2026-041-*/` `episodes/PD-2026-042-*/` の `05_stock/stock_ledger*.json`（および `05_visuals/asset_manifest*.json` があれば）を**読み取り専用で**開き、`sha256` 集合と EP43 の93本の積集合が**空**であることを確認。1件でも exit 1 で差し替え。**EP39/EP40/EP41/EP42 のファイルは読むだけ。書き込み・移動・削除は一切しない。**

---

# 8. A-5: i2v モーション化 16本（Wan 2.2 A14B → RIFE 48fps）

## 8.1 i2v にする16本（動きが意味を持つ絵・各1枚の種プロンプト・バリエーション0）

種画像は §5 と同じ `generate_sdxl_4k.py --variants 1` で `M<NN>_src.png` として生成する（`ai_prompts.v001.md` に下記16行を追加）。**`role:"i2v_source"` として専用確保し body に回さない**（§4.2 不変条件8）。i2v_source の asset_id は `CANIGLIA-MS01..MS16`、モーション成果物の asset_id は `CANIGLIA-M01..M16`。

| # | asset_id | 種画像 | 動きの意味 | act |
|---|---|---|---|---|
| 1 | CANIGLIA-M01 | M01_src | 食卓の拳銃・ランプの光が微かに揺れる | 0 |
| 2 | CANIGLIA-M02 | M02_src | 閉じた玄関ドアへの緩いプッシュイン | 0 |
| 3 | CANIGLIA-M03 | M03_src | 見知らぬナイトスタンドのホテルキーカード | 1 |
| 4 | CANIGLIA-M04 | M04_src | 閉じたドアの下に夜明けの光が滲む | 1 |
| 5 | CANIGLIA-M05 | M05_src | 応答のない携帯（暗い画面） | 1 |
| 6 | CANIGLIA-M06 | M06_src | 一軒家の壁に救急車の赤色灯が回る | 2 |
| 7 | CANIGLIA-M07 | M07_src | 開いた玄関ドアに冷たい光が差す | 2 |
| 8 | CANIGLIA-M08 | M08_src | 布の上の拳銃2丁（静止・押収） | 2 |
| 9 | CANIGLIA-M09 | M09_src | レッカーの荷台に載る車（Cady・家と分離） | 3 |
| 10 | CANIGLIA-M10 | M10_src | 無人の大法廷に埃が舞う | 3 |
| 11 | CANIGLIA-M11 | M11_src | 大理石の壁を一条の光が横切る（very core） | 3 |
| 12 | CANIGLIA-M12 | M12_src | 施錠されていない扉が手幅だけ開いて待つ（緊急救助の間） | 3 |
| 13 | CANIGLIA-M13 | M13_src | 机の脇に置かれるスタンプ済みの1枚（差戻し/別命題） | 3 |
| 14 | CANIGLIA-M14 | M14_src | 開いた玄関ドアの向こうに昼光 | 5 |
| 15 | CANIGLIA-M15 | M15_src | 閉じたドアの下に夜明けの光が広がる | 5 |
| 16 | CANIGLIA-M16 | M16_src | 窓の外の最後の青が夜明けへ移る | 5 |

### 8.1a i2v 種プロンプト（★`ai_prompts.v001.md` の末尾にこの16行を追加・各1枚）

```
- `M01_src.png`
A single handgun lying flat on a dark wooden dining table under a warm low lamp, the room still, poised before any motion, non-graphic and symbolic, no people, no hand [STYLE] Avoid: [NEG]
- `M02_src.png`
A closed residential front door in cold night light with a warm porch-amber glow at its edge, framed for a slow push-in, quiet and unremarkable, no people, no readable number [STYLE] Avoid: [NEG]
- `M03_src.png`
A hotel key card lying on an unfamiliar nightstand beside a dim lamp at night, a strange safe room, poised and still, no people, no readable text [STYLE] Avoid: [NEG]
- `M04_src.png`
Grey first light along the bottom edge of a closed residential front door in a dark hallway, morning gathering on the far side, no people [STYLE] Avoid: [NEG]
- `M05_src.png`
A mobile phone lying dark on a nightstand at morning with a blank unlit screen, a call about to go unanswered, no glow, no readable text, no people [STYLE] Avoid: [NEG]
- `M06_src.png`
An ambulance parked outside a suburban house at dawn with red emergency lights beginning to turn, red glow on the amber-lit siding, non-graphic, no people, no readable text [STYLE] Avoid: [NEG]
- `M07_src.png`
An ordinary residential front door standing open onto a dark interior with cold morning light spilling across the floor, the threshold crossed, no people, no readable number [STYLE] Avoid: [NEG]
- `M08_src.png`
Two handguns laid side by side on a folded cloth on a dark table under cold light, lawful property still and waiting, non-graphic, no people, no hand [STYLE] Avoid: [NEG]
- `M09_src.png`
A private automobile loaded on a tow-truck flatbed under a sodium lot light at night, a car in custody, plainly a vehicle and not a home, no people, no readable plate [STYLE] Avoid: [NEG]
- `M10_src.png`
The interior of a grand empty marble high-court chamber with soft dust suspended in a cold shaft of light, monumental and still, no people, no text [STYLE] Avoid: [NEG]
- `M11_src.png`
A single thin band of pale light lying across a cold marble wall, abstract and unreadable, the very core of a guarantee rendered as light, no legible text, no people [STYLE] Avoid: [NEG]
- `M12_src.png`
A closed unlocked residential door opened only a hand's width onto warm light, the fragile pause before a lawful emergency entry, no people, no face [STYLE] Avoid: [NEG]
- `M13_src.png`
A single stamped page set to one side of a marble desk in cold light, a hard question marked for another day, the text abstract and unreadable, no legible words, no people [STYLE] Avoid: [NEG]
- `M14_src.png`
A residential front door standing wide open onto bright daylight, the emergency door left deliberately wide, no people, no readable number [STYLE] Avoid: [NEG]
- `M15_src.png`
A thin line of warm dawn light spreading along the bottom edge of a closed front door in a dark hallway, morning on the far side, no people [STYLE] Avoid: [NEG]
- `M16_src.png`
A single lit window with the last deep blue of night turning to grey dawn over a quiet residential skyline, one warm room, no people, no visible address [STYLE] Avoid: [NEG]
```

## 8.2 Wan 2.2 A14B の設定（★Known-good・この値を変えるな。`comfy_wan_young.py` を下敷きにパスと SHOTS だけ差し替え）

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
STILL_DIR     = H:\pd-media\assets\ai\caniglia          # 種画像 M<NN>_src.png を読む
VIDEO_OUT_DIR = H:\pd-media\assets\ai_video\caniglia
POS_PREFIX = "cinematic documentary shot, subtle natural motion, "
POS_SUFFIX = ", slow deliberate camera move, shallow depth of field, film grain, photoreal, consistent lighting, no sudden changes"
NEG_PROMPT = "static, motionless, blurry, low quality, distorted, deformed, extra limbs, bad anatomy, morphing face, flickering, jitter, warping, text, watermark, identifiable face, real person likeness, gore, blood, self-harm"
```

**ゲート:** `dry_validate`（length=5 で1回POSTして配線エラーを安く検出）/ `assert_loaded_completely`（部分ロード検出）/ `assert_frame_math`（フレーム計算）。`--run` パスにだけ配線。

## 8.3 実行手順（まず1本で通す）

```bash
py -3.11 scripts/comfy_wan_caniglia.py --build            # グラフだけ（GPU触らない）
py -3.11 scripts/comfy_wan_caniglia.py --run --shot M01   # 1本本番して目視
py -3.11 scripts/comfy_wan_caniglia.py --run-all          # 残り15本（冪等・既存スキップ）
```
1本 24–73 GPU分・16本で 7–19時間。`/queue` `/history` を30秒間隔でポーリング。

## 8.4 RIFE で 48fps 化（`rife_caniglia.py`・`rife_young.py` と同手順）

```
RIFE = D:/AI/tools/rife-ncnn-vulkan-20221029-windows/rife-ncnn-vulkan.exe / モデル rife-v4.6
```
1. Wan 出力先頭 **5フレームは length=5 検証プローブなので捨てる**（`DROP_VALIDATE=5`）
2. 残り41を `f0001.png` 連番にリネーム → RIFE 2x を**2回**（=4x）→ **164フレーム**
3. 164/48fps = **3.417秒** → `ffmpeg -framerate 48 -i f%04d.png -c:v libx264 -pix_fmt yuv420p` で `M<NN>_rife.mp4`
4. **フレーム数検証** `n2 >= 4*n0 - 8` でなければ `SHORT?` で記録し reject

## 8.5 i2v の QC

- 顔・身体・自傷が生成されていないこと（NEG で抑えているが**必ず目視**・制約4/5）
- モーフィング/ちらつき/ワープが無いこと → あれば別シードで再生成
- Cady 用 M09 は**車のみ・家が写り込んでいない**こと（制約3）
- 3.417秒あるので B のカット設計では 3.0–3.4秒で使う想定（16本 × 2回 = 32カット）

---

# 9. A-6: 合成レイヤー（distinct 素材に数えない・ちょうど12本）

| 種別 | 選定 | 用途 |
|---|---|---|
| `particle_assets` | **6本** | 大理石法廷の埃・記録庫の塵。黒背景 drift を screen 合成 |
| `light_assets` | **4本** | porch-amber の暖色・家庭内実用光・救急赤・街灯の光条 |
| `vfx_overlays` | **2本** | 微細なグレイン・救急赤の光ノイズ |
| **合計** | **12本** | |

**ルール:** 合成レイヤーは `check_asset_reuse` の distinct に数えない → `remotion/public/caniglia/overlay/` に置き、`caniglia_film.json` の `cuts[].src` には**出さない**（出すと factory 判定で1回制限を食う）。同じレイヤーを何度重ねてもよい（素材ではなく加工）。黒背景でループするものを選び `blend_hint` を書く。**§7.5 の目視QC対象**（12本・12分）。

```bash
./.venv/Scripts/python.exe scripts/select_factory_assets.py --kind video --query dust_particles --limit 20 --exclude-used --ep PD-2026-043-caniglia --json
```

---

# 10. A-7/A-8: staging とマニフェスト出力

## 10.1 Remotion public への staging（`scripts/stage_caniglia_assets.py`）

```
remotion/public/caniglia/img/     ← role=body の静止画85枚（+ 同名 _depth.png）
remotion/public/caniglia/factory/ ← 選定 factory .mp4 93本
remotion/public/caniglia/motion/  ← i2v M<NN>_rife.mp4 16本
remotion/public/caniglia/overlay/ ← 合成レイヤー 12本
```
- `public_path` はマニフェストの値と実ファイルが一致すること
- factory 動画は `libx264 crf 16 preset medium -an` で **30fps に conform** してコピー（`import_to_remotion.py` の `conform_video(...,fps=30)` と同じ）
- i2v は 48fps のまま置く
- 既存 sha256 一致ならコピーをスキップ（冪等）

**★命名規則（`check_asset_reuse.kind_of()` がパス文字列で分類する・外すと誤分類）:**
- factory の `public_path` は必ず `caniglia/factory/` の下（`/factory` を含む）
- i2v の `public_path` は必ず `.mp4` で終わり `_rife` を含む
- 静止画の `public_path` は `.png` で `/factory` も `ai_video` も `_rife` も**含めない**
- 合成レイヤーは `caniglia/overlay/` に置き `cuts[].src` に出さない

> **B のレンダは `--public-dir=public_slim`（Root.tsx に `id="Ep43Caniglia"`）を使う想定だが、`public_slim` の構築は B の責務。** A は `remotion/public/caniglia/` に正典を置くところまで（B が slim を派生させる）。

## 10.2 権利台帳 `05_stock/stock_ledger.v001.json`

全静止画・i2v・factory・overlay を1行ずつ: `asset_id`/`path`/`source`（`ai_codex` or `factory`）/`license`/`commercial_use`/`sha256`/`ai_disclosure_required`/`generated_at`。

## 10.3 境界契約マニフェストの出力

```bash
./.venv/Scripts/python.exe scripts/build_caniglia_asset_manifest.py
./.venv/Scripts/python.exe scripts/build_caniglia_asset_manifest.py --verify
./.venv/Scripts/python.exe scripts/build_caniglia_asset_manifest.py --reuse-feasibility
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

EP43 の設計値: still 101/85=1.19(≤2) / factory 93/93=1.0(≤1) / motion 32/16=2.0(≤2) / first-use 194/226=0.8584(≥0.70)。**全て達成可能。**

---

# 12. 絶対にやらないこと

- **EP39（frazier）/EP40（lech）/EP41（thompson）/EP42（young）のファイルに一切触らない。** 読み取りのみ可。素材・色（EP41 gold / EP42 blue）・音のレーンも分離。EP43 の accent は **porch-amber #E0913C**（B が OP/AEカード/サムネで使用・A は絵で流用色を作らない）。
- **スレッドBの所有ファイル（§0.2）に触らない。** 特に `remotion/src/**` `scripts/ae/**` `scripts/build_caniglia_film.py` `manifest.json` `04_scenes/shotlist*` `figures`。
  - **ただし `04_scenes/ai_prompts.v001.md` は A が書く**（`generate_sdxl_4k.py` の入力・§5.9/§8.1a）。B は読むだけ。
- **図解・トランジション・タイポの素材を探しに行かない。** 在庫が薄い/無いカテゴリは B が自作する。
- **課金ジョブを起動しない**（ElevenLabs TTS / 課金画像API / アップロード）。ローカル A1111・ComfyUI・RIFE は GPU を使うだけで課金なし（オーナー許可済み）。
- **公開済み・出荷済み mp4 を上書き・再レンダしない。**
- **実在人物の肖像・likeness・身体をどこにも作らない**（§1・制約4）。特に **Edward Caniglia を個人として描かない**。
- **6制約に反する文言・絵をプロンプト・タグ・注記・ファイル名のどこにも作らない**（§1.2/§1.3）:
  - 「令状なしに家に入れない」断定（制約1）／「全面勝訴・事件終結」（制約2）／Cady を家と混同（制約3）／自傷・血・手段の描写（制約5）／「家は絶対に守られる」誇張（制約6）。
- **バリエーション（`_02`/`_03`）を作らない・`--variants 3` を使わない。** 1シーン1枚。反復回避は distinct 85 で担保（§0.1・§5.6）。
- **role=thumb / still_thumb を作らない・overlay を12本以外にしない。** サムネは also_thumb=true の body 6枚（§4.3）。
- **枚数・本数を「だいたい」で決めない。** §3 の確定値（still 85 / factory 93 / i2v 16 / distinct 194 / first-use 0.8584 / still-share 0.4469 / MG≥31 / 12.0分）と §3.3 の検算をそのまま使う。合わなければ実装ではなく**本書を疑って報告**。
- **★ファイル名・subtype・プロンプトを根拠に「大丈夫」と判断しない。** EP36は大聖堂を、EP38は牛を通した。**生成物・在庫クリップを実際に見る**（特に制約4/5は目視でしか守れない・Cady 車クリップの家写り込みも目視で排除）。

---

# 13. 完了報告に含めるもの

```
1. accepted 静止画の枚数と内訳（body 85 / i2v_source 16 / also_thumb 6 [S01/S24/S28/S30/S49/S81] / reject N）
2. factory 選定 93本のリスト（asset_id / subtype / eyeballed_content）と、subtype と食い違って外した本数、Cady 車クリップの「no house in frame」確認
3. EP39/EP40/EP41/EP42 重複ゼロの確認結果
4. i2v 16本の frames / duration_sec と、SHORT? の有無
5. 合成レイヤー12本のリスト
6. §0.4 の [A-DONE-1]〜[A-DONE-5] の実行結果（exit code をそのまま貼る）
7. §3.3 の検算 [1]〜[7] を自分で再計算した結果
8. asset_manifest.v001.json の counts ブロック（still_body 85 / still_i2v_source 16 / motion 16 / factory 93 / overlay 12）
9. 6制約・1枚前提の自己申告（令状なし断定/全面勝訴/Cady=家混同/自傷描写/家は絶対保護 が全出力に皆無・バリエーション0・Caniglia非人物化を目視確認・A↔B同一スキーマ [schema caniglia_assets.v1 / role enum body|i2v_source|reject / counts]）
```

**「動いたと思う」は完了ではない。ゲートが exit 0 を返して初めて完了。自分でQC基準を書き換えて通すのは禁止。**
</content>
</invoke>
