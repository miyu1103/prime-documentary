# Video Production Architecture — Asset-First Motion System

> **ステータス: 設計（未実装）**
> 本書は Prime Documentary（PD）の映像制作の全体像を定義する上位設計書である。
> ここで新しいコンポーネントやスクリプトを実装するのではなく、**既存資産（docs / remotion / schemas / scripts）の上に「どの層に何が乗るか」を地図化**する。実装が必要な箇所は本文中で「**Codexが作る**」と明示し、本書では設計のみを行う。
>
> **前提・仮定**
> - Remotion v4 / 1920×1080 @30fps（サムネ 1280×720）。Brandトークンは `remotion/src/brand.ts`（ink #0A0A0C, navy #0B1A2B, electric #1F6BFF, silver #C8CDD6, gold #E5B53A, white #F5F7FA / display=Impact, body=Trebuchet MS）。
> - 既存の `docs/02_END_TO_END_PIPELINE.md`・`06_VISUAL_SYSTEM_SDXL_AND_CONTINUITY.md`・`08_EDITING_DAVINCI_AUTOMATION.md`（CLAUDE.md によりRemotion運用に置換済み）・`12_QUALITY_GATES_AND_ACCEPTANCE.md` を**壊さず**、本書はそれらを束ねる上位概念として参照する。
> - 既存schema（`scene-plan.schema.json`, `asset.schema.json`, `shotlist.schema.json`, `visual-motif.schema.json`）は**拡張対象**であり、別物を新造しない。
> - ツール役割（CLAUDE.md §11 準拠）: 画像/パーツ=Codex(主)＋ローカルSDXL/SVD、見せ場動画のみ=Runway、ナレ+SFX=ElevenLabs、BGM=SUNO起源を素材としてingest、LottieFiles=手動DLのローカルJSONのみ（API/有料前提なし）。追加有料ツールは前提にしない。
> - 重い素材は `H:\pd-media\assets\factory\<category>\`（Git管理外）に置き、Remotion は `remotion/public/assets/<category>\`（Git管理外、H:から同期）から参照する。
> - 本書は自然言語の設計であり、schema/ADR と矛盾する場合は schema/ADR が優先する（CLAUDE.md §5）。矛盾を見つけたら報告する。

---

## 1. 制作思想 — Asset First

PD は「AI画像の見本市」ではなく、**知識駆動のドキュメンタリー番組**である。映像の強さは、毎回ゼロから生成することではなく、**再利用可能な素材を大量に蓄積し、台本の意図に合わせてそこから選ぶ**ことで生まれる。

中核思想（最重要）：

```
台本(verified script)
  → Scene Plan（何を語るシーンか）
  → Shot Recipe（各シーンを"どう作るか"のレシピ）
  → Asset Manifest（必要素材の宣言）
  → 素材選定（まず既存ストックから選ぶ）
  → 不足分だけ追加生成
  → Remotion 合成（Motion System）
  → Quality Gate
  → 修正
  → 最終
```

**Asset First の定義**：先に大量の再利用素材を Asset Factory に貯め、`manifest` で管理し、Shot Recipe からは**まずそこを検索して選ぶ**。新規生成は「選べる素材が無い差分だけ」。これにより、

- 1本あたりの生成コストと人手判断時間が下がる（CLAUDE.md §2 の目的関数：再利用率↑・人間判断時間↓）。
- ブランド一貫性が上がる（同じトークン・同じモーション語彙で作る）。
- AI動画（Runway）は**見せ場限定**。本編の動きは Remotion Motion System（純コード・$0）で作る。

> AI動画・AI画像は invariant 11 に従い「本物の記録ではない」前提で扱う（実在人物の肖像を作らない、出所・権利を追跡）。

---

## 2. レイヤ構成（5層）

本システムを5層で捉える。各層は「責務 / 入力 / 出力 / 既存資産との対応」を持つ。下に行くほど具体（フレーム）に近づく。

```
┌─────────────────────────────────────────────────────────────┐
│ L1  Asset Factory 層   再利用素材を大量に貯める（14カテゴリ）      │
├─────────────────────────────────────────────────────────────┤
│ L2  Manifest 層        素材を id/rights/qc 付きで台帳管理         │
├─────────────────────────────────────────────────────────────┤
│ L3  Scene Plan + Shot Recipe 層   "何を語るか"→"どう作るか"        │
├─────────────────────────────────────────────────────────────┤
│ L4  Motion System (Remotion) 層   レシピ→実際の動く映像へ合成      │
├─────────────────────────────────────────────────────────────┤
│ L5  Quality Gate 層    Visual/Edit Gate で usable を判定・修正    │
└─────────────────────────────────────────────────────────────┘
```

### L1 — Asset Factory 層

- **責務**：番組横断で再利用できる素材を、14カテゴリで継続的に蓄積する。
- **入力**：ブランド方針、過去エピソードの不足素材、視覚モチーフ（`visual-motif.schema.json`）。
- **出力**：`H:\pd-media\assets\factory\<category>\` 配下の素材ファイル群。
- **14カテゴリ**：`backgrounds, parallax_layers, vfx_overlays, loops, transitions, typography_assets, diagram_assets, sfx, ai_video_shots, lottie_assets, ui_motion_assets, texture_assets, light_assets, particle_assets`。
- **Asset id 形式**：`AF-<CATEGORY>-NNNN`（例：`AF-BACKGROUNDS-0007`）。これはエピソード内の `PD-YYYY-NNN-S001-IMG-001`（CLAUDE.md §8）とは別系統の**ファクトリ横断ID**であり、片方向で manifest が両者を関連付ける。
- **生成元ツール**：背景/パーツ=Codex＋ローカルSDXL/SVD、見せ場ループ=Runway（`ai_video_shots` のみ）、SFX=ElevenLabs、`lottie_assets`=LottieFiles手動DLのローカルJSON。
- **既存対応**：現状の `remotion/public/<slug>/` への素材コピー（`import_to_remotion.py`）はエピソード単位。Factory 層はその**上流**に位置し、エピソードを跨いだ恒久ストックを提供する。Factory→public の同期は **Codexが作る**（後述 §6）。

### L2 — Manifest 層

- **責務**：Factory の各素材に id/出所/権利/QC/再利用回数を付与し、検索可能にする。
- **入力**：L1 の素材ファイル。
- **出力**：Asset Manifest（台帳）。既存 `asset.schema.json` を**拡張**して表現する（別schemaを新造しない）。
- **既存対応**：
  - `asset.schema.json`：`asset_type`(image/video/diagram/map/audio/music/...), `status`(raw/candidate/approved/...), `rights`(status/origin/commercial_use/evidence_ref), `qc`(status/score/findings), `provenance` を既に持つ。**Factory横断素材を表すための追加フィールド**（`factory_category`, `factory_id=AF-<CATEGORY>-NNNN`, `reuse_count`, `tags`）は schema 拡張として **Codexが作る**（後方互換・`schema_version` を上げる、`.claude/rules/02` 準拠）。
  - `visual-motif.schema.json`：再利用モチーフ（`motif_id=MOT-NNNN`, `reuse_count`, `last_used_episode`, `rights_basis`）は既に再利用台帳の発想を持つ。Factory の概念モデルはこれを継承する。
  - エピソード単位の素材選定結果は既存 `episodes/<ep>/05_stock/usable_assets.v001.json`（rights-gated usable list）。Manifest 層は「Factory台帳」と「エピソードusable list」の2段で、後者は前者の部分集合を指す。

### L3 — Scene Plan + Shot Recipe 層

- **責務**：検証済み台本を「**何を語るシーンか（Scene Plan）**」と「**各シーンをどう作るかのレシピ（Shot Recipe）**」に落とす。
- **入力**：`script_verified` の注釈付き台本、claim ledger、Manifest（選べる素材の在庫）。
- **出力**：
  - Scene Plan：既存 `scene-plan.schema.json`（`scene_id=S001`, `script_span_ids`, `purpose`, `visual_mode`, `duration_seconds`, `priority`, `required_assets`, `transition_in/out`, `on_screen_text`, `human_review_required` …）。
  - Shot Recipe：本アーキテクチャで新設する**設計概念**。各シーンの emotion / informationGoal / visualStrategy / assetNeeds / selectedAssets / motionRecipe / sfx / transition / qualityTarget を持つ。詳細仕様は **[shot-recipe-system.md](./shot-recipe-system.md)**。型と生成ロジックは **Codexが作る**。
  - Shotlist：既存 `shotlist.schema.json`（`span_id=SPN-NNNN`, `suggested_asset_type`, `motion`, `priority`, `search_keywords`, `on_screen_text`）。Shot Recipe は shotlist を**包含・上位化**する関係（§5）。
- **20 sceneType**（Shot Recipe の分類軸。`scene-plan` の `visual_mode` 12種を**用途語彙として上位整理**したもの。schema enum を置換しない）：
  `opening_hook, chapter_title, explanation, character_profile, company_profile, place_intro, timeline, evidence_board, comparison, data_reveal, quote, turning_point, reenactment, emotional_pause, summary, ending, transition_bridge, abstract_emotion, problem_statement, solution_reveal`。
- **30 motion grammar**（`motionRecipe` の語彙。shotlist の `motion` 5種＝video_native/ken_burns/parallax/graphic_anim/static を**演出語彙として上位整理**）：
  `slow_push_in, fast_push_in, pull_out, subtle_shake, impact_zoom, parallax_depth, keyword_punch, quote_typewriter, number_countup, evidence_reveal, timeline_flow, map_focus, card_stack, light_sweep, particle_drift, data_reveal, hard_cut, flash_transition, whip_transition, glitch_transition, silent_hold, cinematic_drift, foreground_blur_pass, panel_float, depth_dolly, ambient_overlay, diagram_draw, relationship_connect, title_slam, soft_reveal`。

### L4 — Motion System (Remotion) 層

- **責務**：Shot Recipe を、実際に動く映像へ合成する。**何も静止させない（"shoboi" 禁止、`RoughCut.tsx` の設計目標）**。
- **入力**：Shot Recipe / RoughCutData / 素材（`remotion/public/...`）/ ナレ・BGM・字幕。
- **出力**：Remotion コンポジション（プレビュー〜最終レンダー）。
- **既存の再利用部品（新規作成せず再利用 / ラップする）**：

| 部品 | 場所 | 役割 |
|---|---|---|
| `MovingStage`, `CameraRig`, `MovingStage` 内 `Particles` / `LightSweep` / `Vignette` | `remotion/src/components/Motion.tsx` | カメラ移動・粒子・光・周辺減光の「動くステージ」。slow_push_in / particle_drift / light_sweep の土台。 |
| `Parallax`（+`SymbolicScene`） | `remotion/src/components/Parallax.tsx` | 2.5D 視差。parallax_depth / depth_dolly。 |
| `RoughCut` 内部の `MovingImage`(ken_burns\|parallax), `VideoShot`, `ImageShot`, `MovingVideo`, `VideoSegment`, `GraphicCard`, `Telop`, `CaptionBand` | `remotion/src/compositions/RoughCut.tsx` | 1台本spanあたり1ショットを timed に並べる本編ラフカット。型 `RoughShot` / `RoughCutData` / `CaptionCue`。 |
| `KineticType`（型 `KineticLine`） | `remotion/src/components/KineticType.tsx` | キネティックタイポ。keyword_punch / title_slam。 |
| `OpenCaption` | `remotion/src/components/OpenCaption.tsx` | 語単位の焼き込み字幕（small-size legible）。 |
| `DiagramFlow` | `remotion/src/components/DiagramFlow.tsx` | A→B→C のフロー図。diagram_draw / relationship_connect。 |
| `CitationLowerThird` | `remotion/src/components/CitationLowerThird.tsx` | claim_id 連動の出典ロワーサード。evidence_reveal 補助。 |
| `SceneArt`（`Gavel/Scales/Document/Room/Courtroom/MapUS/Timeline` + `pickArt`） | `remotion/src/components/SceneArt.tsx` | 素材未生成時の記号的コード美術（$0・実写と誤認させない）。 |
| `Grain` | `remotion/src/components/Grain.tsx` | フィルムグレイン。ambient_overlay。 |
| `WipeTransition` | `remotion/src/components/Transition.tsx` | ゴールドバーのワイプ。whip_transition / flash_transition の土台。 |
| `BrandOpening`（`Bookends.tsx`） / `Opening`（`compositions/Opening.tsx`） | `remotion/src/components/Bookends.tsx` / `compositions/Opening.tsx` | 番組オープニング。opening_hook / chapter_title。 |
| `ColdOpen`（型 `HookBeat` / `HookLine`） | `remotion/src/compositions/ColdOpen.tsx` | 冒頭5秒フック。opening_hook。 |
| `Episode`（`TEMPLATE_12MIN`） | `remotion/src/compositions/Episode.tsx` | 12分骨格スケルトン。 |
| `Animatic`（型 `AnimaticScene`） | `remotion/src/compositions/Animatic.tsx` | アニマティック（レビュー用）。 |

> **二重実装禁止（CLAUDE.md invariant 14, `.claude/rules/00`）**：上表の機能を別名で作り直さない。新しい motion grammar は**既存部品の合成（ラップ／パラメータ化）**として実現するのが原則。どうしても無い場合のみ「Codexが新規primitiveを作る」と明示する。

### L5 — Quality Gate 層

- **責務**：合成結果が usable か判定し、不合格は前段へ差し戻す。「Generated successfully ≠ usable」（CLAUDE.md invariant 13）。
- **入力**：合成プレビュー／レンダー、素材の `qc`/`rights`。
- **出力**：Gate 判定（Severity S0–S5）と修正指示。
- **既存対応**：`12_QUALITY_GATES_AND_ACCEPTANCE.md` の **Visual Gate / Edit Gate** をそのまま使う。Shot Recipe の `qualityTarget` は各 Gate のチェック項目に対応する受入基準を持つ（[shot-recipe-system.md](./shot-recipe-system.md) §品質基準）。Severity と差し戻し（S4=前段へ rework / S5=blocker）は既存定義に従う。

---

## 3. 既存資産マップ（どこに何が乗るか）

```
台本 (05_*, script_verified)
     │
     ▼
[L3] Scene Plan ── scene-plan.schema.json ──┐         docs/06_VISUAL_SYSTEM が visual_mode/継続性を規定
     │                                       │
     ▼                                       ▼
[L3] Shot Recipe (NEW, Codex) ◀── 包含 ── shotlist.schema.json (SPN-NNNN, suggested_asset_type, motion)
     │                                       │
     │                                       ▼
[L1/L2] Asset Factory + Manifest ── asset.schema.json(拡張) / visual-motif.schema.json
     │     H:\pd-media\assets\factory\<category>\  →(sync)→  remotion/public/assets/<category>\
     │                                       │
     ▼                                       ▼
       scripts/import_to_remotion.py  ──▶  remotion/src/data/<slug>_roughcut.ts (RoughCutData)
     │                                       │
     ▼                                       ▼
[L4] Remotion Motion System ── RoughCut.tsx / Motion.tsx / KineticType / DiagramFlow / SceneArt / ...
     │                                       │
     ▼                                       ▼
[L5] Quality Gate ── docs/12 Visual Gate / Edit Gate (S0–S5)
     │
     ▼
   最終レンダー (libx264, crf16, quality-first CPU)  ──▶  docs/02 stage 23–25 / 上位 docs/08(→Remotion)
```

- **docs/02（End-to-End Pipeline）**：32工程の全体時系列。本書の5層は 02 の stage 12–25（scene→visual→motion→assembly→render）に**重なる**。02 を置換せず、02 の「scene/visual/edit」領域を Asset First の観点で詳細化したものが本書である。
- **docs/06（Visual System / SDXL / Continuity）**：`visual_mode`・継続性・候補数・Visual QC を規定。本書 L3 の sceneType と L1 の Factory は 06 の visual_mode/継続性ルールを**踏襲**する（矛盾させない）。
- **docs/08（Editing）**：CLAUDE.md により DaVinci → **Remotion + FFmpeg** に置換済み。本書 L4 がその実体。
- **docs/12（Quality Gates）**：本書 L5 がそのまま参照する。

---

## 4. Claude Code と Codex の役割分担

PD は左工程＝Claude（構造・検証・オーケストレーション）、右工程＝Codex（生成・実装・ビジュアル仕上げ）で分担する（memory: PD episode recipe）。

| 領域 | Claude Code | Codex |
|---|---|---|
| 台本→Scene Plan→Shotlist | ◎ 生成・schema検証・claim整合 | △ レビュー |
| Shot Recipe 型・生成ロジックの**実装** | ○ 設計・契約・テスト定義 | ◎ **実装（本書で言う「Codexが作る」）** |
| Asset Factory への素材**生成** | △ ジョブ定義・権利チェック起動 | ◎ SDXL/SVD/Runway/Lottie取り込み |
| Manifest 登録・QC・rights gate | ◎ schema検証・rights/hash検証 | ○ 候補投入 |
| 素材選定（既存から選ぶ） | ◎ `import_to_remotion.py` 系の選定ロジック | ○ 手作りAI画像の差し込み（`assets/ai/<slug>/`） |
| Remotion 合成・最終仕上げ | ○ data生成・登録・検証 | ◎ ビジュアル微調整・最終クオリティ |
| Quality Gate 判定 | ◎ 自動チェック・差し戻し | ○ 再生成（targeted fix） |
| 公開・アップロード | ◎ 承認境界の遵守（`.claude/rules/16`） | — |

> **MotionDemo で先に検証してから本番**：新しい motion grammar / Shot Recipe テンプレを本編へ入れる前に、**まず `MotionDemo`（Codexが作る軽量コンポジション。`StyleTest`/`ClipProof` の系譜）で短尺検証**し、ブランド・可読性・"動いて見える"ことを確認してから本編に適用する。検証なしに本編へ新演出を投入しない（CLAUDE.md §6 vertical slice、`.claude/rules/18` 過剰実装禁止）。

---

## 5. 長尺(RoughCut)とショート(Shorts)の関係

PD には2つの出力フォーマットがあり、**Motion System(L4) と Asset First(L1/L2) を共有**しつつ、コンポジションは別物として並立する。

| | 長尺 本編 | ショート |
|---|---|---|
| コンポジション | `RoughCut.tsx`（型 `RoughCutData` / `RoughShot`） | `Short.tsx`（型 `ShortData` / `ShortBeat`、**Codexが作る**） |
| 仕様書 | docs/02・本書・[shot-recipe-system.md](./shot-recipe-system.md) | `episodes/_planning/SHORTS_REMOTION_SPEC.md` |
| 解像度 | 1920×1080 @30fps | 1080×1920 @30fps / 35–45秒 |
| data生成 | `scripts/import_to_remotion.py` → `<slug>_roughcut.ts` | `build_short_data.py shortNN` → `shortNN.ts`（Codexが作る） |
| 素材源 | Asset Factory + エピsoード usable list | `H:\pd-media\assets\ai\shorts\shortNN\` ＋ Factory再利用 |
| 共有部品 | `Motion.tsx` / `KineticType` / `Grain` / brandトークン / Telop・Caption の発想 | 同左（ゾーニングはショート専用、左右安全域・UI回避） |

ショートは長尺の素材・モーション語彙・ブランドを**再利用**する（Asset First の効用がフォーマット横断で効く）。Shot Recipe の motion grammar はショートの `motion`(kenburns/parallax/pushin/video) と語彙整合する。詳細なゾーニング・音声4層ミックス・受入基準は `SHORTS_REMOTION_SPEC.md` を正とする。

---

## 6. 未実装サマリ（Codexが作る箇所）

本書は設計のみ。以下は別途、契約・テストとともに **Codexが実装**する（各々 vertical slice で MotionDemo 検証→本番）：

1. **Shot Recipe 型と生成ロジック**（`scene-plan` + `shotlist` から Shot Recipe を導出）。仕様＝[shot-recipe-system.md](./shot-recipe-system.md)。
2. **`asset.schema.json` の Factory 拡張**（`factory_category` / `factory_id=AF-<CATEGORY>-NNNN` / `reuse_count` / `tags`、`schema_version` 繰上げ・migration付き）。
3. **Factory→public 同期**（`H:\pd-media\assets\factory\<category>\` → `remotion/public/assets/<category>\`、checksum検証・atomic、`.claude/rules/14` 準拠）。
4. **`import_to_remotion.py` の Shot Recipe 連携拡張**（既存の selection ロジックを壊さず、Shot Recipe の `selectedAssets` を尊重するモードを追加）。詳細＝[production-workflow.md](./production-workflow.md)。
5. **MotionDemo コンポジション**（新 motion grammar の事前検証用、軽量）。
6. **ショート `Short.tsx` / `build_short_data.py`**（`SHORTS_REMOTION_SPEC.md` 準拠）。

---

## 関連ドキュメント

- [shot-recipe-system.md](./shot-recipe-system.md) — Shot Recipe 型・20 sceneType 定義表・既存レンダラへの写像。
- [production-workflow.md](./production-workflow.md) — 素材選択型10ステップの運用手順。
- `docs/02_END_TO_END_PIPELINE.md` / `06_VISUAL_SYSTEM_SDXL_AND_CONTINUITY.md` / `12_QUALITY_GATES_AND_ACCEPTANCE.md` — 上位統合の対象（壊さない）。
- `episodes/_planning/SHORTS_REMOTION_SPEC.md` — ショート仕様（正）。
