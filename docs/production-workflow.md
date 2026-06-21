# Production Workflow — 素材選択型10ステップ運用手順

> **ステータス: 設計（未実装）**
> 本書は Asset First（素材選択型）制作の**運用手順**を、「誰が / 何を / どのファイル / どのコマンド」で実行するかまで具体化する。新規スクリプト・型・schema拡張の**実装は Codex が行う**（本文で明示）。本書は手順設計のみ。
>
> **前提・仮定**
> - 上位設計＝[video-production-architecture.md](./video-production-architecture.md)、レシピ詳細＝[shot-recipe-system.md](./shot-recipe-system.md)。
> - 既存パイプライン `docs/02_END_TO_END_PIPELINE.md` の stage 12–25 を**置換せず詳細化**する。Quality は `docs/12` の Visual/Edit Gate（Severity S0–S5）に従う。
> - 既存スクリプト：`scripts/import_to_remotion.py`（U4）、`scripts/asset_map.py`、`scripts/fetch_stock.py`、`scripts/plan_scenes.py`、`scripts/validate_episode.py` 等。素材の真実は `episodes/<ep>/...` と Manifest。
> - 重い素材は `H:\pd-media\assets\factory\<category>\`（Git管理外）。Remotion参照は `remotion/public/assets/<category>\` および従来の `remotion/public/<slug>/`（Git管理外、H:から同期）。
> - 役割分担＝Claude（左工程：構造・選定・検証）／ Codex（右工程：生成・実装・仕上げ）。
> - 承認境界（`.claude/rules/16`）・権利チェック（外部素材は商用ライセンス確認、MJ/Suno生成は問題なし）・コスト上限（`.claude/rules/11`）を遵守。

---

## 0. 全体像（素材選択型）

```
[蓄積フェーズ：エピソードに依存しない、継続的]
 S1 大量蓄積  →  S2 Manifest登録（id/rights/qc）

[エピソードフェーズ：1本ごと]
 S3 Scene Plan  →  S4 Shot Recipe  →  S5 既存素材から選ぶ
   →  S6 不足分だけ追加生成  →  S7 import（data生成）
   →  S8 Remotion合成  →  S9 Quality Gate  →  S10 修正→完成
```

「先に貯める → 選ぶ → 足りない差分だけ作る」が肝。生成（S6）はボトルネックなので**最小化**する。

---

## 1. 各ステップ詳細

### S1. 大量蓄積（Asset Factory を太らせる）
- **誰が**：Codex（生成）＋Claude（ジョブ定義・権利/コストの番人）。
- **何を**：14カテゴリ（`backgrounds, parallax_layers, vfx_overlays, loops, transitions, typography_assets, diagram_assets, sfx, ai_video_shots, lottie_assets, ui_motion_assets, texture_assets, light_assets, particle_assets`）の再利用素材を継続的に増やす。
- **どこへ**：`H:\pd-media\assets\factory\<category>\`。ファイル名は `AF-<CATEGORY>-NNNN.<ext>` を基本。
- **ツール**：背景/パーツ=ローカルSDXL/SVD＋Codex、見せ場ループ=Runway（`ai_video_shots` のみ）、SFX=ElevenLabs、Lottie=LottieFiles手動DLのローカルJSON。
- **コマンド（既存ベース／拡張は Codex）**：SDXL系は `scripts/gen_*_sdxl_*.py` の系譜、ストック取得は `scripts/fetch_stock.py`。**Factory蓄積専用のバルク登録は Codex が作る**（`scripts/factory_ingest.py` 想定）。
- **ルール**：実在人物の肖像を作らない（invariant 11）。外部DL素材は商用ライセンス確認（MJ/Suno生成は確認不要）。

### S2. Manifest 登録（台帳化）
- **誰が**：Claude（schema検証・rights/hash検証）＋Codex（候補投入）。
- **何を**：S1の各素材に `asset_id`/`factory_id=AF-<CATEGORY>-NNNN`、`rights`(status/origin/commercial_use/evidence_ref)、`qc`(status/score/findings)、`provenance`、`tags`、`reuse_count` を付与。
- **どこへ**：`asset.schema.json` を**拡張**した Asset Manifest（`factory_category`/`factory_id`/`reuse_count`/`tags` 追加、`schema_version` 繰上げ・migration付き）。**拡張の実装は Codex**。
- **コマンド**：`scripts/validate_manifest.py`（既存）でschema検証、`scripts/verify_rights_hashes.py`（既存）で権利・ハッシュ検証。
- **ゲート**：`rights.status='clear'` かつ `commercial_use='allowed'` のものだけが後段で選定可能（"usable"）。`qc.status` が `fail`/`blocked` は除外。

> S1–S2 はエピソードに依存せず**常時回す**。エピソード開始時には「選べる在庫」が十分ある状態が理想。

### S3. Scene Plan（何を語るシーンか）
- **誰が**：Claude（生成・claim整合・schema検証）。
- **入力**：`script_verified` の注釈付き台本、claim ledger。
- **何を**：各シーン `S001...` に `script_span_ids`/`purpose`/`visual_mode`/`duration_seconds`/`priority`/`required_assets`/`transition_in/out`/`on_screen_text`/`human_review_required` を割当て。
- **どこへ**：`episodes/<ep>/04_scenes/scene-plan.v001.json`（`scene-plan.schema.json` 準拠）。
- **コマンド**：`scripts/plan_scenes.py <episode>`（既存）。
- **ゲート**：`coverage.all_script_spans_mapped=true`、orphan無し。

### S4. Shot Recipe（どう作るか）
- **誰が**：Claude（導出・整合）＋Codex（導出ロジック実装）。
- **入力**：Scene Plan ＋ `shotlist.schema.json`（`SPN-NNNN`/`suggested_asset_type`/`motion`/`search_keywords`）。
- **何を**：各シーンを `ShotRecipe`（[shot-recipe-system.md](./shot-recipe-system.md) §1）に落とす。`sceneType`(20種)/`emotion`/`informationGoal`/`motionRecipe`(30 grammar)/`assetNeeds`/`qualityTarget` を確定。`selectedAssets` は次のS5で埋める（この時点は空）。
- **どこへ**：`episodes/<ep>/04_scenes/shot-recipe.v001.json`（**型・生成・schemaは Codex が作る**。`shotlist`/`scene-plan` を包含する導出物）。
- **コマンド（Codexが作る）**：`scripts/build_shot_recipe.py <episode>`（想定）。
- **ゲート**：全シーンに `informationGoal` 1つ、`mustMove=true`、`sceneType` が妥当。

### S5. 既存素材から選ぶ（Asset First の核心）
- **誰が**：Claude（選定ロジック）。
- **何を**：各 `ShotRecipe.assetNeeds` を**まず Manifest（S2の在庫）から keyword 一致で選ぶ**。選んだ `asset_id`/`factory_id` を `selectedAssets` に書き込み、`reuse_count++`。
- **どこへ**：`shot-recipe.v*.json` を更新、エピソード usable list `episodes/<ep>/05_stock/usable_assets.v001.json`（既存フォーマット）を生成/更新。
- **接続（既存ロジック）**：`scripts/import_to_remotion.py` 内の `pick_videos()` / `pick_asset()`（keyword overlap スコアリング、`used_in_spans` 明示割当を優先）が選定の中核。`scripts/asset_map.py` でspan↔asset対応を管理。
- **規則**：keyword一致が無いものだけが「不足」＝S6の対象。**まず選ぶ、作るのは最後**。

### S6. 不足分だけ追加生成（最小追加生成ルール）
- **誰が**：Codex（生成）＋Claude（差分の特定・権利/コスト番人）。
- **何を**：S5で **selectedAssets が埋まらなかった assetNeeds のみ** を生成対象にする。
- **最小追加生成ルール**：
  1. **priority A の不足を最優先**、C は当面 `GraphicCard`/`SceneArt`（コード美術）で代替して可（タイムラインは常に完成）。
  2. **見せ場（turning_point/opening_hook/reenactment の A）かつ `aiVideoAllowed=true` の時だけ Runway**。それ以外の動きは Remotion Motion System（$0）で作る。
  3. 生成物は**生成後すぐ S1→S2 へ還流**し Factory 在庫化（次回から選べる＝再利用率↑）。
  4. 1エピソードの新規生成上限はコスト計画に従う（超過は停止し日本語で確認）。
- **どこへ**：手作りAI画像は `H:\pd-media\assets\ai\<slug>\<span_id>*.png`（`import_to_remotion.py` の `ai_images_for()` が span 単位で自動採用、stock より優先）。
- **コマンド**：SDXL系 `scripts/gen_*_sdxl_*.py`、ブリーフ `scripts/ai_image_brief.py`。

### S7. import（RoughCutData 生成）
- **誰が**：Claude。
- **何を**：shotlist ＋ usable list から `RoughCutData` を生成し、usable な素材だけを `remotion/public/<slug>/` へコピー（動画は fps 整合のため再エンコード）。素材無しの shot は `src:null`→`GraphicCard` で必ず埋まる。
- **どこへ**：`remotion/src/data/<slug>_roughcut.ts`（export `<SLUG>_ROUGHCUT: RoughCutData`）。
- **コマンド**：
  ```
  .venv/Scripts/python.exe scripts/import_to_remotion.py <episode>            # dry-run
  .venv/Scripts/python.exe scripts/import_to_remotion.py <episode> --write    # 実コピー＋.ts出力
  ```
- **Shot Recipe 連携（Codexが作る）**：既存の自動選定を壊さず、`shot-recipe.v*.json` の `selectedAssets` を尊重する `--from-recipe` モードを追加（後方互換）。
- **登録**：出力後、`remotion/src/Root.tsx` に `<Composition id="RoughCut-<slug>" ...>` を追加（idはハイフンのみ、`_` 不可）。

### S8. Remotion 合成
- **誰が**：Claude（data生成・登録・検証）＋Codex（ビジュアル微調整・最終クオリティ）。
- **何を**：`RoughCut`（Motion.tsx/KineticType/DiagramFlow/SceneArt/Grain/WipeTransition 等を内部利用）でプレビュー。ナレ・BGM・字幕(CaptionCue)を合流。
- **コマンド**：`cd remotion && npx remotion studio`（プレビュー）。
- **検証先行**：新しい motion grammar や Recipe テンプレは、本編前に **MotionDemo（Codexが作る軽量コンポジション。`StyleTest`/`ClipProof` 系譜）で短尺検証**してから本番適用。
- **仕上げ/書き出しはこの Windows PC で・クオリティ最優先・CPU(libx264)**（NVENCに切替えない）。

### S9. Quality Gate
- **誰が**：Claude（自動チェック・差し戻し判定）＋Codex（再生成）。
- **何を**：`docs/12` の **Visual Gate / Edit Gate** を適用。各 `ShotRecipe.qualityTarget`（`minVisualScore`/`mustMove`/`captionLegibleAt`/`rightsClear`/`gate`）を受入基準に照合。
- **Severity**：S0=info / S1=軽微（公開可）/ S2=要修正推奨 / S3=公開前必須修正 / S4=前段へ rework / S5=公開事故・法務・アカウントリスク（blocker）。
- **コマンド**：`scripts/validate_episode.py <episode>`（既存、構造/参照整合）。視覚QCの自動チェックは `docs/06` の Visual QC 系。
- **ゲート**：S4/S5 が無く、必要承認（first-cut 等、`.claude/rules/16`）が揃うこと。

### S10. 修正 → 完成（修正テンプレ）
- **誰が**：差分担当（Claude=構造/選定、Codex=生成/仕上げ）。
- **修正テンプレ**（各修正に必ず記録）：

  ```
  修正ID: FIX-<ep>-NNN
  対象: <scene_id> / <span_id> / <asset_id>
  Gate/Severity: Visual|Edit / S0–S5
  所見(findings): <docs/12 のどのチェックに不合格か>
  原因分類: prompt|seed|composition|continuity|selection|motion|caption
  対応: 再選定(S5へ) | 追加生成(S6へ) | motionRecipe調整(S8) | caption調整
  再生成範囲: この shot のみ（部分再処理。全体再レンダーしない）
  検証: 修正後に再度 S9。mustMove/rightsClear/可読性を再確認
  revision: shot-recipe.vNNN / <slug>_roughcut.ts 再出力
  ```
- **規則**：承認済み artifact は上書きせず**新 revision** を作る（CLAUDE.md invariant 6、`.claude/rules/12`）。claim が変われば依存（script span→scene→asset→voice→edit）を stale 伝播させ再処理（部分再処理）。

---

## 2. 既存スクリプト/データとの接続まとめ

| 工程 | 既存資産 | 役割 | 拡張（Codex） |
|---|---|---|---|
| S2 | `asset.schema.json` / `validate_manifest.py` / `verify_rights_hashes.py` | 素材台帳・権利検証 | Factory拡張フィールド・`factory_ingest.py` |
| S3 | `scene-plan.schema.json` / `plan_scenes.py` | Scene Plan | — |
| S4 | `shotlist.schema.json` | ショットの素材/モーション指定 | `shot-recipe.schema`・`build_shot_recipe.py` |
| S5 | `import_to_remotion.py`(`pick_videos`/`pick_asset`) / `asset_map.py` / `usable_assets.v001.json` | keyword選定・span↔asset | `selectedAssets` 尊重モード |
| S6 | `gen_*_sdxl_*.py` / `ai_image_brief.py` / `fetch_stock.py` / `ai_images_for()` | 追加生成・span画像差し込み | — |
| S7 | `import_to_remotion.py --write` → `<slug>_roughcut.ts` | RoughCutData生成・publicコピー | `--from-recipe` |
| S8 | `RoughCut.tsx` ＋ `Motion.tsx`/`KineticType`/… / `Root.tsx` | 合成・プレビュー | `MotionDemo` |
| S9 | `validate_episode.py` / `docs/12` Gate | 検証・受入 | recipe qualityTarget 自動照合 |

---

## 3. 1エピソードを通す具体例（擬似）

対象：`PD-2025-001-miranda`（slug=`miranda`）。

```
# 前提（蓄積フェーズは常時済み）
S1/S2: Factory に backgrounds/light/ai_video_shots/sfx 等が多数登録済み（rights=clear, qc=pass）

# エピソードフェーズ
S3  Claude:  .venv/Scripts/python.exe scripts/plan_scenes.py miranda
            → episodes/PD-2025-001-miranda/04_scenes/scene-plan.v001.json（S001..S022、coverage OK）

S4  Claude:  scripts/build_shot_recipe.py miranda      （Codex実装後）
            → 04_scenes/shot-recipe.v001.json
              S001=opening_hook / S004=reenactment / S009=explanation / S013=data_reveal ...
              各 informationGoal・motionRecipe・assetNeeds を確定、selectedAssets は空

S5  Claude:  Manifest から keyword 選定（import_to_remotion.py の pick_* ロジック）
            → S001 に AF-BACKGROUNDS-0007 / AF-LIGHT_ASSETS-0003、S009 に AF-AI_VIDEO_SHOTS-0042..43 …
            → 05_stock/usable_assets.v001.json 更新、reuse_count++
            不足: S004(reenactment, A) の見せ場カットが在庫に無い → S6 へ

S6  Codex:   見せ場(reenactment A, aiVideoAllowed=true)のみ生成
            - 取調室の象徴カット: Runway 1カット → AF-AI_VIDEO_SHOTS-0044 として Factory還流(S1→S2)
            - 顔は写さない(invariant 11)。priority C の不足は SceneArt(Room) で代替

S7  Claude:  .venv/Scripts/python.exe scripts/import_to_remotion.py miranda --write
            → remotion/src/data/miranda_roughcut.ts（MIRANDA_ROUGHCUT: RoughCutData）
              + usable素材を remotion/public/miranda/ へコピー(動画はfps整合)
            → Root.tsx に <Composition id="RoughCut-miranda" ...> 追加

S8  Claude/Codex:  cd remotion && npx remotion studio でプレビュー
            新規 motion（例 data_reveal の number_countup）は先に MotionDemo で確認 → 本編適用
            ナレ(ElevenLabs)・BGM(Suno起源ingest)・captions(forced alignment) を合流

S9  Claude:  scripts/validate_episode.py miranda ＋ docs/12 Visual/Edit Gate
            所見例: S013 の数字に出典(claim_id)欠落 = S3(公開前必須修正) → 差し戻し

S10 修正:   FIX-miranda-001 / 対象 S013 / Edit Gate S3 /
            所見=data_reveal に claim_id 未表示 / 対応=CitationLowerThird 追加(S8) /
            再生成範囲=S013 shotのみ / 検証=再S9で pass / revision=shot-recipe.v002 + .ts再出力
            → first-cut 承認(.claude/rules/16) 後、finalizing へ
```

---

## 関連ドキュメント
- [video-production-architecture.md](./video-production-architecture.md) — 5層アーキテクチャと役割分担。
- [shot-recipe-system.md](./shot-recipe-system.md) — `ShotRecipe` 型・20 sceneType・RoughShot 写像。
- `docs/02_END_TO_END_PIPELINE.md` — 32工程の上位パイプライン（本書は stage 12–25 を詳細化）。
- `docs/12_QUALITY_GATES_AND_ACCEPTANCE.md` — Visual/Edit Gate・Severity S0–S5（S9で参照）。
- `scripts/import_to_remotion.py` / `scripts/plan_scenes.py` / `scripts/validate_episode.py` — 接続する既存スクリプト。
