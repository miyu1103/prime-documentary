# Shot Recipe System — シーン＝「表示内容」ではなく「レシピ」

> **ステータス: 設計（未実装）**
> 本書は、各シーンを「何を表示するか」ではなく「**どう作るか（レシピ）**」として記述する `ShotRecipe` 型と、20 sceneType ごとの作り方を定義する。型・生成ロジック・レンダラ写像の**実装は Codex が行う**。本書は設計のみ。
>
> **前提・仮定**
> - 上位設計は [video-production-architecture.md](./video-production-architecture.md)。本書はその L3（Scene Plan + Shot Recipe 層）の詳細。
> - Remotion v4 / 1920×1080 @30fps。Brandトークン＝`remotion/src/brand.ts`。
> - 既存 `scene-plan.schema.json`（`visual_mode` 12種）・`shotlist.schema.json`（`suggested_asset_type`5種 / `motion`5種）を**壊さず拡張的に参照**する。ShotRecipe はこれらを**包含する上位レシピ**であり、別schemaの新造ではなく、既存2つの間を埋める導出物。
> - 既存レンダラ＝`RoughCut.tsx`（型 `RoughShot` / `RoughCutData` / `CaptionCue`）。ShotRecipe は最終的に `RoughShot` 群へ写像されてレンダリングされる（§3）。
> - 20 sceneType / 30 motion grammar / 14 Asset Factory カテゴリ は上位アーキテクチャ（CANON）の語彙を用いる。
> - AI動画(Runway)は**見せ場限定**、Lottie は**手動DLのローカルJSONのみ**（API/有料前提なし）。実在人物の肖像は作らない（invariant 11）。

---

## 1. `ShotRecipe` 型

1シーン（= `scene_id=S001`、1つ以上の `script_span_ids`）に対し1つの `ShotRecipe` を持つ。**「表示内容」ではなく「作り方の指示書」**である点が要点。

```ts
// 設計上の型（実装は Codex）。fields は scene-plan/shotlist を包含する。
export type ShotRecipe = {
  sceneId: string;            // 'S001'（scene-plan.scene_id と一致）
  sceneType: SceneType;       // 20種のいずれか（§2）。scene-plan.visual_mode を用途語彙へ上位整理
  durationFrames: number;     // 尺（フレーム）。scene-plan.duration_seconds * 30 から導出
  emotion: string;            // 感情設計。例 'dread' | 'curiosity' | 'awe' | 'relief'（scene-plan.emotional_function 由来）
  informationGoal: string;    // このシーンで視聴者が得る1つの理解（1文）
  visualStrategy: string;     // 画づくりの方針（実写志向/記号/データ可視化 など。docs/06 の visual_mode 準拠）
  assetNeeds: AssetNeed[];    // 必要素材の宣言（カテゴリ＋検索キーワード＋本数＋優先度）
  selectedAssets: string[];   // Manifest から選んだ asset_id / factory_id（AF-<CATEGORY>-NNNN）。空なら未選定
  motionRecipe: MotionStep[]; // 30 motion grammar の並び（時間順）。各 stepに対象部品とパラメータ
  sfx: string[];              // SFX asset_id（AF-SFX-NNNN）。空可
  transitionIn: TransitionName;   // 入りのトランジション（30 motion grammar の *_transition 系 or hard_cut）
  transitionOut: TransitionName;  // 出のトランジション
  qualityTarget: QualityTarget;   // 受入基準（docs/12 Visual/Edit Gate に対応、§品質基準）
  renderNotes: string;        // 人間/Codex向けの仕上げメモ（自由文）
};

export type AssetNeed = {
  category: AssetFactoryCategory;  // 14カテゴリのいずれか
  keywords: string[];              // 検索語（shotlist.search_keywords と同源）
  count: number;                   // 必要本数（長尺shotは複数cutで埋める）
  priority: 'A' | 'B' | 'C';       // scene-plan.priority / shotlist.priority と一致
  aiVideoAllowed: boolean;         // Runway 使用可否（見せ場限定で true）
};

export type MotionStep = {
  grammar: MotionGrammar;          // 30種のいずれか
  component: string;               // 担当する既存部品（'MovingStage' | 'KineticType' | ...）
  fromFrame: number;               // step開始（scene内相対）
  toFrame: number;                 // step終了
  params?: Record<string, number | string | boolean>;
};

export type QualityTarget = {
  minVisualScore: number;          // 0–100（asset.qc.score の下限）
  mustMove: true;                  // 静止禁止（RoughCut の設計目標）。常に true
  captionLegibleAt: 'desktop' | 'mobile';  // 小サイズ可読性（docs/27）
  rightsClear: boolean;            // 使用素材は rights.status='clear'（commercial_use='allowed'）必須
  gate: 'visual' | 'edit' | 'both';// 差し戻し対象 Gate（docs/12）
};
```

> `SceneType` / `MotionGrammar` / `AssetFactoryCategory` / `TransitionName` の enum は上位アーキテクチャの語彙に固定。これらの TypeScript 定義と、`scene-plan`+`shotlist` から `ShotRecipe` を導出する関数は **Codex が作る**（契約・テストつき）。

### フィールドの意味と例

| field | 意味 | 例 |
|---|---|---|
| `sceneId` | scene-plan の `scene_id` | `"S004"` |
| `sceneType` | 20種の用途分類 | `"reenactment"` |
| `durationFrames` | 尺（frames）。`duration_seconds*30` | `255`（8.5s） |
| `emotion` | 感情の狙い | `"dread"` |
| `informationGoal` | 1文の理解目標 | `"取調べで自白が生まれた瞬間を体感させる"` |
| `visualStrategy` | 画づくり方針 | `"記号的reenactment（実写と誤認させない）＋ハードライト"` |
| `assetNeeds` | 必要素材宣言 | `[{category:"ai_video_shots",keywords:["interrogation","lamp"],count:1,priority:"A",aiVideoAllowed:true}]` |
| `selectedAssets` | 選定済み | `["AF-AI_VIDEO_SHOTS-0042"]` |
| `motionRecipe` | 動きの並び | `[{grammar:"slow_push_in",component:"MovingStage",fromFrame:0,toFrame:255}]` |
| `sfx` | 効果音 | `["AF-SFX-0011"]` |
| `transitionIn/Out` | 前後トランジション | `"soft_reveal"` / `"hard_cut"` |
| `qualityTarget` | 受入基準 | `{minVisualScore:80,mustMove:true,captionLegibleAt:"mobile",rightsClear:true,gate:"both"}` |
| `renderNotes` | 仕上げメモ | `"顔は写さない。ランプのフリッカーを強めに。"` |

---

## 2. 20 sceneType 定義表

各 sceneType の「目的 / 推奨尺 / 推奨素材カテゴリ / 推奨motion grammar / 推奨字幕演出 / 推奨SFX / 推奨VFX / 推奨トランジション / 向いている既存コンポーネント / Runway可否 / Lottie可否 / 乱用禁止 / 品質基準」。

> 凡例：素材カテゴリ・motion grammar・コンポーネント名は CANON 語彙。Runway は**見せ場限定**、Lottie は**ローカルJSONのみ**。「乱用禁止」は invariant 11/13・"shoboi"回避・可読性のためのガード。品質基準は docs/12 の Visual/Edit Gate に対応。

### 2.1 opening_hook
- **目的**：冒頭5秒で掴む。パラドックス提示。 | **推奨尺**：8–30s（複数beat）
- **素材**：`backgrounds, ai_video_shots(見せ場のみ), light_assets, particle_assets` | **motion**：`fast_push_in, title_slam, keyword_punch, light_sweep`
- **字幕**：大型キネティック（2行以内） | **SFX**：低音インパクト/ライザー | **VFX**：`light_sweep, particle_drift, ambient_overlay`
- **トランジション**：in=`hard_cut` / out=`flash_transition` | **既存部品**：`ColdOpen`(HookBeat), `BrandOpening`, `KineticType`
- **Runway**：可（フック1カットのみ） | **Lottie**：不可
- **乱用禁止**：説明し過ぎ・3行以上の文字・実写人物 | **品質基準**：5秒以内に主張提示、mustMove、mobile可読、`minVisualScore≥80`

### 2.2 chapter_title
- **目的**：章の区切りを示す。 | **尺**：2–4s
- **素材**：`backgrounds, typography_assets, light_assets` | **motion**：`title_slam, light_sweep, soft_reveal`
- **字幕**：章番号＋章題（gold rule） | **SFX**：短いヒット | **VFX**：`light_sweep`
- **in**=`whip_transition` / **out**=`hard_cut` | **部品**：`Opening`, `KineticType`, `WipeTransition`
- **Runway**：不可 | **Lottie**：可（章番号の軽アニメ） | **乱用禁止**：長文・毎章で違う演出
- **品質基準**：1.5s以内に章題判読、ブランド一貫、mustMove

### 2.3 explanation
- **目的**：因果・仕組みを噛み砕く。本編の主力。 | **尺**：6–14s/shot
- **素材**：`backgrounds, parallax_layers, diagram_assets, ai_video_shots(stock寄り)` | **motion**：`slow_push_in, parallax_depth, diagram_draw, keyword_punch`
- **字幕**：キーワードpunch＋下段caption | **SFX**：控えめ（キーワード時のみ） | **VFX**：`particle_drift, ambient_overlay`
- **in**=`soft_reveal` / **out**=`hard_cut` | **部品**：`MovingStage`, `ImageShot`/`VideoShot`(RoughCut内), `KineticType`, `DiagramFlow`
- **Runway**：原則不可（stock/AI画像で十分） | **Lottie**：可（補助図） | **乱用禁止**：見せ場演出の多用・1shotに情報詰め込み
- **品質基準**：1 informationGoal/shot、mustMove、mobile可読、`minVisualScore≥75`

### 2.4 character_profile
- **目的**：人物の立場・動機を紹介。 | **尺**：6–12s
- **素材**：`backgrounds, parallax_layers, typography_assets`（**実在人物は記号/シルエットで**） | **motion**：`slow_push_in, panel_float, soft_reveal, foreground_blur_pass`
- **字幕**：氏名・肩書のロワーサード | **SFX**：控えめ | **VFX**：`foreground_blur_pass, vignette`
- **in**=`soft_reveal` / **out**=`hard_cut` | **部品**：`SceneArt`(記号), `CitationLowerThird`, `KineticType`
- **Runway**：不可 | **Lottie**：可（肩書バッジ） | **乱用禁止**：**実在人物の生成肖像**（invariant 11）、断定的内面描写
- **品質基準**：氏名/立場が読める、肖像非生成、rightsClear、mustMove

### 2.5 company_profile
- **目的**：組織・企業の性質を示す。 | **尺**：6–12s
- **素材**：`backgrounds, ui_motion_assets, diagram_assets, typography_assets` | **motion**：`card_stack, panel_float, diagram_draw, relationship_connect`
- **字幕**：社名・設立・規模 | **SFX**：UIヒット控えめ | **VFX**：`ambient_overlay`
- **in**=`soft_reveal` / **out**=`hard_cut` | **部品**：`DiagramFlow`, `KineticType`, `GraphicCard`(RoughCut)
- **Runway**：不可 | **Lottie**：可（ロゴ風モーションは商標に注意） | **乱用禁止**：実在ロゴの無断使用、誇張データ
- **品質基準**：主要属性が読める、rightsClear、mustMove

### 2.6 place_intro
- **目的**：場所・舞台を提示。 | **尺**：5–10s
- **素材**：`backgrounds, parallax_layers, ai_video_shots(stock寄り), texture_assets` | **motion**：`cinematic_drift, parallax_depth, map_focus, slow_push_in`
- **字幕**：地名（控えめ） | **SFX**：環境音（ambience寄り） | **VFX**：`ambient_overlay, particle_drift`
- **in**=`soft_reveal` / **out**=`hard_cut` | **部品**：`MovingStage`, `SceneArt`(MapUS), `MovingImage`
- **Runway**：可（広角の"場"カット1つまで） | **Lottie**：不可 | **乱用禁止**：実在の現在地を史実と誤認させる
- **品質基準**：場所が伝わる、mustMove、rightsClear

### 2.7 timeline
- **目的**：時系列で出来事を並べる。 | **尺**：8–16s
- **素材**：`diagram_assets, typography_assets, backgrounds` | **motion**：`timeline_flow, number_countup, relationship_connect, slow_push_in`
- **字幕**：年号＋イベント | **SFX**：刻みヒット | **VFX**：`light_sweep`
- **in**=`soft_reveal` / **out**=`whip_transition` | **部品**：`SceneArt`(Timeline), `DiagramFlow`, `KineticType`
- **Runway**：不可 | **Lottie**：可（マーカー移動） | **乱用禁止**：年号誤り（claim整合必須）、点が多すぎる
- **品質基準**：時系列が誤解なく読める、claim_id整合、mustMove

### 2.8 evidence_board
- **目的**：証拠・出典を並べて見せる。 | **尺**：8–14s
- **素材**：`diagram_assets, texture_assets, typography_assets, backgrounds` | **motion**：`evidence_reveal, card_stack, relationship_connect, keyword_punch`
- **字幕**：出典ラベル＋claim_id | **SFX**：紙/ピンのヒット | **VFX**：`foreground_blur_pass`
- **in**=`hard_cut` / **out**=`hard_cut` | **部品**：`CitationLowerThird`, `GraphicCard`, `DiagramFlow`
- **Runway**：不可 | **Lottie**：可（接続線） | **乱用禁止**：未検証ソースの提示、生成画像を証拠と誤認させる（invariant 11）
- **品質基準**：各証拠に出典/claim_id、rightsClear、mustMove、`gate:both`

### 2.9 comparison
- **目的**：A対Bを対比。 | **尺**：6–12s
- **素材**：`backgrounds, diagram_assets, ui_motion_assets, typography_assets` | **motion**：`panel_float, card_stack, relationship_connect, soft_reveal`
- **字幕**：左右ラベル | **SFX**：切替ヒット | **VFX**：`light_sweep`
- **in**=`soft_reveal` / **out**=`hard_cut` | **部品**：`DiagramFlow`, `Parallax`(分割), `KineticType`
- **Runway**：不可 | **Lottie**：可 | **乱用禁止**：印象操作的な不公平比較
- **品質基準**：対比軸が明確、事実整合、mustMove

### 2.10 data_reveal
- **目的**：数字・統計を印象的に出す。 | **尺**：5–10s
- **素材**：`diagram_assets, typography_assets, backgrounds, ui_motion_assets` | **motion**：`number_countup, data_reveal, keyword_punch, impact_zoom`
- **字幕**：大型数字＋単位＋出典 | **SFX**：カウント/着地ヒット | **VFX**：`light_sweep, particle_drift`
- **in**=`flash_transition` / **out**=`hard_cut` | **部品**：`KineticType`, `DiagramFlow`, `CitationLowerThird`
- **Runway**：不可 | **Lottie**：可（数値アニメ） | **乱用禁止**：出典なし数字、誤誘導スケール
- **品質基準**：数字に出典/claim_id、mustMove、mobile可読、`gate:both`

### 2.11 quote
- **目的**：発言・条文を引用提示。 | **尺**：5–10s
- **素材**：`backgrounds, typography_assets, texture_assets` | **motion**：`quote_typewriter, soft_reveal, slow_push_in, silent_hold`
- **字幕**：引用＋出典帰属 | **SFX**：タイプ音控えめ | **VFX**：`vignette, ambient_overlay`
- **in**=`soft_reveal` / **out**=`hard_cut` | **部品**：`KineticType`, `OpenCaption`, `CitationLowerThird`
- **Runway**：不可 | **Lottie**：不可 | **乱用禁止**：出典不明引用、改変引用
- **品質基準**：原文・帰属明示、可読、mustMove（最低限のドリフト）

### 2.12 turning_point
- **目的**：物語の転換点を強調。 | **尺**：5–10s
- **素材**：`backgrounds, ai_video_shots(見せ場), light_assets, particle_assets` | **motion**：`impact_zoom, fast_push_in, title_slam, flash_transition`
- **字幕**：短い断言1行 | **SFX**：強インパクト | **VFX**：`light_sweep, glitch_transition(控えめ)`
- **in**=`flash_transition` / **out**=`hard_cut` | **部品**：`ColdOpen`系beat, `KineticType`, `WipeTransition`
- **Runway**：可（転換の象徴1カット） | **Lottie**：不可 | **乱用禁止**：glitch多用、毎回同じ強演出
- **品質基準**：転換が一瞬で伝わる、mustMove、`minVisualScore≥80`

### 2.13 reenactment
- **目的**：出来事を記号的に再現。 | **尺**：6–12s
- **素材**：`ai_video_shots(見せ場), backgrounds, texture_assets, light_assets` | **motion**：`cinematic_drift, slow_push_in, foreground_blur_pass, depth_dolly`
- **字幕**：最小（斜体キャプション可） | **SFX**：環境＋動作音 | **VFX**：`grain, vignette, ambient_overlay`
- **in**=`soft_reveal` / **out**=`hard_cut` | **部品**：`SceneArt`(Room/Courtroom), `MovingStage`, `Grain`
- **Runway**：可（再現の象徴カット） | **Lottie**：不可 | **乱用禁止**：**実写と誤認させる/実在人物の顔**（invariant 11）、過度な劇化
- **品質基準**：記号的で誤認させない、顔非生成、mustMove、`gate:both`

### 2.14 emotional_pause
- **目的**：間を作り感情を定着。 | **尺**：3–6s
- **素材**：`backgrounds, texture_assets, light_assets, particle_assets` | **motion**：`silent_hold, cinematic_drift, particle_drift, ambient_overlay`
- **字幕**：なし〜1行 | **SFX**：無音/微かなトーン | **VFX**：`vignette, grain`
- **in**=`soft_reveal` / **out**=`soft_reveal` | **部品**：`MovingStage`, `Grain`
- **Runway**：不可 | **Lottie**：不可 | **乱用禁止**：長すぎる静止（mustMoveは微ドリフトで担保）、情報過多
- **品質基準**：呼吸が生まれる、わずかでも動く、mobile可読（字幕ある場合）

### 2.15 summary
- **目的**：要点を束ねる。 | **尺**：8–14s
- **素材**：`diagram_assets, typography_assets, backgrounds` | **motion**：`card_stack, relationship_connect, keyword_punch, slow_push_in`
- **字幕**：箇条キーワード | **SFX**：控えめ | **VFX**：`light_sweep`
- **in**=`soft_reveal` / **out**=`hard_cut` | **部品**：`DiagramFlow`, `KineticType`
- **Runway**：不可 | **Lottie**：可 | **乱用禁止**：新情報の追加、長文
- **品質基準**：要点が3〜5点で読める、mustMove

### 2.16 ending
- **目的**：締め・余韻・CTA。 | **尺**：6–12s
- **素材**：`backgrounds, light_assets, typography_assets, particle_assets` | **motion**：`pull_out, cinematic_drift, light_sweep, soft_reveal`
- **字幕**：締めの一文＋ブランド | **SFX**：着地トーン | **VFX**：`vignette, particle_drift`
- **in**=`soft_reveal` / **out**=`hard_cut` | **部品**：`BrandOpening`/`Bookends`, `KineticType`
- **Runway**：不可 | **Lottie**：可（ロゴ余韻） | **乱用禁止**：過剰な煽りCTA、唐突な打ち切り
- **品質基準**：余韻＋ブランド提示、mustMove

### 2.17 transition_bridge
- **目的**：シーン間の橋渡し。 | **尺**：1–3s
- **素材**：`transitions, texture_assets, light_assets` | **motion**：`whip_transition, flash_transition, light_sweep, hard_cut`
- **字幕**：なし | **SFX**：ウーシュ | **VFX**：`light_sweep`
- **in**=`hard_cut` / **out**=`whip_transition` | **部品**：`WipeTransition`
- **Runway**：不可 | **Lottie**：可（トランジション素材） | **乱用禁止**：多用して情報を分断、毎回違う種類
- **品質基準**：滑らかに繋ぐ、短い、ブランド一貫

### 2.18 abstract_emotion
- **目的**：抽象的な感情・概念を象徴。 | **尺**：4–8s
- **素材**：`backgrounds, vfx_overlays, light_assets, particle_assets, texture_assets` | **motion**：`cinematic_drift, particle_drift, ambient_overlay, foreground_blur_pass`
- **字幕**：なし〜1語 | **SFX**：トーン/ドローン | **VFX**：`light_sweep, grain, vignette`
- **in**=`soft_reveal` / **out**=`soft_reveal` | **部品**：`MovingStage`, `Parallax`, `Grain`
- **Runway**：可（抽象ループ1つ） | **Lottie**：可（抽象モーション） | **乱用禁止**：意味のないAIっぽさ、長すぎ
- **品質基準**：意図した感情に寄与、mustMove、実写誤認なし

### 2.19 problem_statement
- **目的**：問題・矛盾を提示。 | **尺**：5–10s
- **素材**：`backgrounds, typography_assets, diagram_assets, light_assets` | **motion**：`keyword_punch, slow_push_in, impact_zoom, relationship_connect`
- **字幕**：問い/矛盾を1〜2行 | **SFX**：緊張ヒット | **VFX**：`vignette, ambient_overlay`
- **in**=`hard_cut` / **out**=`soft_reveal` | **部品**：`KineticType`, `DiagramFlow`
- **Runway**：不可 | **Lottie**：可 | **乱用禁止**：誇張・恐怖煽り、未検証の前提
- **品質基準**：問題が一文で伝わる、事実整合、mustMove

### 2.20 solution_reveal
- **目的**：解決・帰結を提示。 | **尺**：6–12s
- **素材**：`backgrounds, diagram_assets, light_assets, typography_assets` | **motion**：`soft_reveal, diagram_draw, light_sweep, number_countup`
- **字幕**：結論＋（必要なら出典） | **SFX**：解決トーン | **VFX**：`light_sweep, particle_drift`
- **in**=`soft_reveal` / **out**=`hard_cut` | **部品**：`DiagramFlow`, `KineticType`, `CitationLowerThird`
- **Runway**：不可 | **Lottie**：可 | **乱用禁止**：因果の飛躍、過剰な楽観化
- **品質基準**：帰結が明確で事実に基づく、claim整合、mustMove

---

## 3. Shot Recipe → 既存 `RoughShot` / `RoughCutData` への写像

ShotRecipe は最終的に既存レンダラ（`RoughCut.tsx`）が解釈できる `RoughShot` に**落とし込まれる**。新レンダラは作らない（invariant 14）。

### 3.1 フィールド写像

| ShotRecipe | → RoughShot（`RoughCut.tsx`） | 写像規則 |
|---|---|---|
| `sceneId` | `spanId`（代表span） | scene-plan の `script_span_ids[0]` を用いる |
| （scene-plan）`chapter_id` | `chapterId` | そのまま（`'opening'` は `BrandOpening` 差し込み） |
| `durationFrames` | `seconds` | `durationFrames / 30` |
| `assetNeeds[].category` + 選定結果 | `assetType` | video系→`stock_video` / AI画像→`ai_image` / 静止→`stock_image` / コード美術→`motion_graphic` / PD保管→`archival_pd` |
| `motionRecipe`（主） | `motion` | `*_push_in/cinematic_drift/...`→`ken_burns`、`parallax_depth/depth_dolly`→`parallax`、video中心→`video_native`、図解/記号→`graphic_anim`、（`static`は使わない＝mustMove） |
| `selectedAssets` | `src` / `clips[]` / `images[]` | 動画は `clips[{src,clipSeconds}]`、複数静止は `images[]`、単一は `src`。未選定→`src:null`→`GraphicCard` 自動表示 |
| （on_screen_text） | `telop[]` | scene-plan/shotlist の `on_screen_text` |
| `assetNeeds[].priority` | `priority`（A/B/C） | そのまま |
| `sfx` / `transitionIn/Out` | （`RoughCutData` 直下では未保持） | 現状 RoughCut は per-shot SFX/transition を持たないため、**Codex が `RoughShot` 拡張（任意フィールド `sfx?`, `transitionIn?/Out?`）を追加**するか、当面は `renderNotes` と Motion System 側で表現。後方互換で追加。 |

### 3.2 motion grammar → 既存部品

`motionRecipe[].component` は §2 の「向いている既存コンポーネント」に従い、`RoughCut` 内の `MovingImage`/`VideoShot`/`ImageShot`/`GraphicCard` か、`Motion.tsx`(`MovingStage`)・`KineticType`・`DiagramFlow`・`SceneArt`・`WipeTransition` のいずれかへ対応づく。RoughCut が現状解さない grammar（例 `quote_typewriter`, `number_countup`）は、**Codex が当該シーンを専用コンポジション断片として合成**するか、`GraphicCard` 相当のブランドカードへフォールバックする（タイムライン常時完成・"shoboi"回避）。

### 3.3 RoughCutData 全体

```
ShotRecipe[]  ──(写像)──▶  RoughCutData {
  episodeId, title, fps:30,
  narrationSrc, bgmSrc,        // 音声は audio 工程から
  captions: CaptionCue[],      // forced alignment 由来
  shots: RoughShot[]           // 上表の per-recipe 写像
}
```

この `RoughCutData` を `scripts/import_to_remotion.py` が `remotion/src/data/<slug>_roughcut.ts` として出力する点は既存通り（[production-workflow.md](./production-workflow.md) §接続）。ShotRecipe の `selectedAssets` を尊重する選定モードの追加は **Codex が作る**。

---

## 4. JSON Shot Recipe 例

### 4.1 opening_hook

```json
{
  "sceneId": "S001",
  "sceneType": "opening_hook",
  "durationFrames": 150,
  "emotion": "unease",
  "informationGoal": "「黙秘権は脚本家が書いたのではない」という矛盾で視聴者を掴む",
  "visualStrategy": "コード製の動く闇＋光のスイープ。実写人物なし。文字主導。",
  "assetNeeds": [
    {"category": "backgrounds", "keywords": ["dark", "void", "tension"], "count": 1, "priority": "A", "aiVideoAllowed": false},
    {"category": "ai_video_shots", "keywords": ["red and blue lights", "night"], "count": 1, "priority": "A", "aiVideoAllowed": true},
    {"category": "light_assets", "keywords": ["sweep", "beam"], "count": 1, "priority": "B", "aiVideoAllowed": false}
  ],
  "selectedAssets": ["AF-BACKGROUNDS-0007", "AF-LIGHT_ASSETS-0003"],
  "motionRecipe": [
    {"grammar": "fast_push_in", "component": "MovingStage", "fromFrame": 0, "toFrame": 90, "params": {"intensity": 1.1}},
    {"grammar": "title_slam", "component": "KineticType", "fromFrame": 30, "toFrame": 150},
    {"grammar": "light_sweep", "component": "MovingStage", "fromFrame": 0, "toFrame": 150}
  ],
  "sfx": ["AF-SFX-0001"],
  "transitionIn": "hard_cut",
  "transitionOut": "flash_transition",
  "qualityTarget": {"minVisualScore": 82, "mustMove": true, "captionLegibleAt": "mobile", "rightsClear": true, "gate": "both"},
  "renderNotes": "Runwayは赤青ライトの1カットのみ。文字は2行以内・Impact。最初の5秒で矛盾を提示。"
}
```

### 4.2 explanation

```json
{
  "sceneId": "S009",
  "sceneType": "explanation",
  "durationFrames": 330,
  "emotion": "curiosity",
  "informationGoal": "なぜ4つの併合事件が1つの判決になったのかを噛み砕く",
  "visualStrategy": "AI静止画を複数Ken Burnsでカット＋A→B→Cのフロー図で因果を可視化",
  "assetNeeds": [
    {"category": "ai_video_shots", "keywords": ["supreme court", "four cases", "exterior"], "count": 2, "priority": "A", "aiVideoAllowed": false},
    {"category": "diagram_assets", "keywords": ["flow", "merge"], "count": 1, "priority": "B", "aiVideoAllowed": false},
    {"category": "backgrounds", "keywords": ["navy", "paper"], "count": 1, "priority": "C", "aiVideoAllowed": false}
  ],
  "selectedAssets": ["AF-AI_VIDEO_SHOTS-0042", "AF-AI_VIDEO_SHOTS-0043"],
  "motionRecipe": [
    {"grammar": "slow_push_in", "component": "ImageShot", "fromFrame": 0, "toFrame": 180},
    {"grammar": "diagram_draw", "component": "DiagramFlow", "fromFrame": 150, "toFrame": 300, "params": {"stagger": 22}},
    {"grammar": "keyword_punch", "component": "KineticType", "fromFrame": 90, "toFrame": 150}
  ],
  "sfx": [],
  "transitionIn": "soft_reveal",
  "transitionOut": "hard_cut",
  "qualityTarget": {"minVisualScore": 76, "mustMove": true, "captionLegibleAt": "mobile", "rightsClear": true, "gate": "visual"},
  "renderNotes": "Runway不使用。静止画は~4.5sごとにカット（ImageShot準拠）して dwell させない。1 shot = 1 理解。"
}
```

---

## 関連ドキュメント
- [video-production-architecture.md](./video-production-architecture.md) — 5層アーキテクチャと既存資産マップ。
- [production-workflow.md](./production-workflow.md) — Shot Recipe を作る運用10ステップと `import_to_remotion.py` 接続。
- `schemas/scene-plan.schema.json` / `shotlist.schema.json` — ShotRecipe が包含する既存契約。
- `remotion/src/compositions/RoughCut.tsx` — 写像先レンダラ（`RoughShot` / `RoughCutData`）。
- `docs/06_VISUAL_SYSTEM_SDXL_AND_CONTINUITY.md` / `docs/12_QUALITY_GATES_AND_ACCEPTANCE.md` — visual_mode・継続性・Gate（壊さない）。
