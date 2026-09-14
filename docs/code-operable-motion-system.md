# Code-Operable Motion System（コード操作可能モーションシステム）

> ステータス: 設計（未実装）。本書は思想とアーキテクチャの設計のみ。コードは未生成。
> 実装は `docs/remotion-animation-component-roadmap.md` の Phase 順で行う。

## 前提・仮定

- Remotion v4 / 1920×1080 @ 30fps。Remotion アプリのルートは本リポジトリの `remotion/`。
  したがって CANON の `src/motion/*` は実体として **`remotion/src/motion/*`** に置く（本書では以後 `src/motion/*` と表記）。
- ブランドトークンは `remotion/src/brand.ts` の `BRAND` が単一の真実。
  ink `#0A0A0C` / navy `#0B1A2B` / electric `#1F6BFF` / silver `#C8CDD6` / gold `#E5B53A` / white `#F5F7FA`、
  display=Impact、body=Trebuchet MS。新規 preset から色を再定義せず、必ず `BRAND` を参照する（仮定: `brand.ts` は不変の真実源）。
- 既存コンポーネントは監査済みで実在する（`remotion/src/components/` と `remotion/src/compositions/`）。
  本書の新コンポーネントはこれらを **ラップ**し、新造・二重実装しない（CLAUDE.md 不変条件 14）。
- 未導入依存（`@remotion/three`, `@remotion/lottie`, `@remotion/transitions`, `three`）は前提にしない。
  これらに依存する要素は「Phase4・導入後に実装」と明記し、今は設計のみ（導入は Codex 担当）。
- AI 動画（Runway 等）は見せ場限定。本編尺の大半はこの Motion System（Remotion・コード）で作る。
- 秘密情報・実トークン・実 `.env` 値は本書に一切含めない。

---

## 1. 思想：Remotion を「編集ツール」から「動画制作エンジン」へ

PD は AI 画像ショーケースではなく、知識駆動のドキュメンタリー制作システム（CLAUDE.md §1）。
その視覚面では、Remotion を「タイムラインを手で並べる編集ツール」として使うのではなく、
**素材・字幕・図解・SFX・カメラ・奥行き・トランジション・品質（グレード/グレイン）を統合して 1 本の映画的映像を出力する制作エンジン**へ格上げする。

要件は次の一点に集約される：

> Claude Code / Codex が **props と preset（コード）だけ**で、映像を生成・修正・量産できること。

つまり「人がタイムラインを触って微調整する」のではなく、「構造化データ（shotlist / scene plan）と preset 名を入力すると、一貫した品質の本編映像が出る」状態を目標にする。これは CLAUDE.md §2 の目的関数（視聴者価値 × 量産性 × 再利用 ÷ 人の判断時間 ÷ 事故リスク）に直結する。人の判断時間を最小化しつつ、編集ボトルネック（§10-8）を下げる。

### 既存資産との関係（壊さない・二重実装しない）

`remotion/src/components/` には既に映画的プリミティブが揃っている：

- `Motion.tsx`: `CameraRig`（シード付き push-in/pan）, `MovingStage`（camera+light+particles+vignette の合成ステージ）, `Particles`, `LightSweep`, `Vignette`。
- `Parallax.tsx`: `Parallax`（2.5D 多層パララックス）, `SymbolicScene`。
- `compositions/RoughCut.tsx`: `RoughCut`、内部に `MovingImage`(ken_burns|parallax) / `VideoShot` / `ImageShot` / `GraphicCard` / `Telop` / `CaptionBand`、型 `RoughShot` / `RoughCutData` / `CaptionCue`、`roughCutDurationInFrames()`。
- 文字/図解/字幕: `KineticType.tsx`(`KineticType`,`KineticLine`), `OpenCaption.tsx`(`OpenCaption`), `DiagramFlow.tsx`(`DiagramFlow`), `CitationLowerThird.tsx`(`CitationLowerThird`)。
- 場面アート: `SceneArt.tsx`(`SceneArt`,`pickArt`; Gavel/Scales/Document/Room/Courtroom/MapUS/Timeline 等のモチーフ)。
- 品質/転換: `Grain.tsx`(`Grain`), `Transition.tsx`(`WipeTransition`)。
- ブランド/構成: `Brand.tsx`(`PdMonogram`,`PdLogoImage`,`Horizon`), `Bookends.tsx`(`BrandOpening`,`BrandEndcard`,`OPENING_SEC`,`ENDCARD_SEC`), `compositions/Opening.tsx`, `compositions/ColdOpen.tsx`, `compositions/Episode.tsx`。

`src/motion/*` の新コンポーネントは、これらの**薄いラッパ**として実装する。新層の役割は「映画的プリミティブを生で並べる」現状を、**preset 名と意味のある props（sceneType / motion grammar）で駆動する宣言的 API** に変えること。プリミティブ本体（カメラ計算・パーティクル・グレイン等）は再利用し、再発明しない。

---

## 2. アーキテクチャ

### 2.1 レイヤ構成

```
入力（構造化データ）
  shotlist / scene plan（pd-scenes が出力）+ sceneType + motion grammar + preset 名
        │
        ▼
presets/  ← 単一の真実（Single Source of Truth）
  motionPresets.ts   30 motion grammar → 具体パラメータ
  easingPresets.ts   bezier/spring 名前付き定義
  sceneTypePresets.ts 20 sceneType → 既定のレイアウト/カメラ/字幕/SFX/尺
  sfxPresets.ts      SFX キュー定義（src/gain/同期点）
  colorPresets.ts    grade/atmosphere の色（BRAND 参照）
        │
        ▼
src/motion/*  ← ラッパ層（preset + props 駆動。意味のある宣言的 API）
  camera/ text/ visual/ layout/ transitions/ audio/ three/ lottie/
        │  各コンポーネントは preset を解決し、props で上書き可能
        ▼
remotion/src/components/*  ← 既存プリミティブ（CameraRig/Particles/Grain/Parallax/…）
        │
        ▼
Remotion レンダラ → 本編映像（libx264, quality-first; メモリ project_render_quality_first 準拠）
```

### 2.2 presets を単一の真実とする

すべての「数値・色・尺・カーブ・SFX」は preset に集約する。コンポーネントは preset を解決し、必要時のみ props で上書きする。これにより：

- Claude/Codex は **preset のキーを変えるだけ**で全話の質感を一括調整できる（量産・統一感）。
- 数値マジックナンバーがコンポーネント本体に散らないため、修正の影響範囲が読める（コード操作性）。
- sceneType を指定すれば「そのシーン種別の標準的な見せ方」が自動で決まる（人の判断削減）。

### 2.3 駆動モデル：`<Motion grammar sceneType preset>`

新層の各コンポーネントは次の優先順位で値を解決する（仮定として規約化する）：

1. 明示 props（最優先・局所上書き）
2. `sceneType` の既定（`sceneTypePresets.ts`）
3. `motion grammar` の既定（`motionPresets.ts`）
4. ブランド/グローバル既定（`BRAND` ほか）

この合成は純粋関数（例: `resolveMotion(grammar, sceneType, overrides)`）で実装し、副作用なし・型安全（戻り値は判別可能な discriminated union）にする。

---

## 3. 9 つの要件をどう満たすか

CANON の狙い「奥行き・緩急・カメラ感・光/空気・意味のある字幕/図解・SFX 同期・統一感・コード操作・量産」を、具体的な実装方針に落とす。

### 3.1 奥行き（depth）
- 既存 `Parallax`（多層 2.5D）と `Motion.tsx` の `CameraRig` の push-in を `visual/ParallaxScene` と `layout/EvidenceBoard` 等が利用。
- Phase4 で `three/DepthStage` / `FloatingPanels3D` を `@remotion/three` 導入後に追加し、真の Z 奥行き（パネル浮遊・depth dolly）を出す。今は 2.5D で代替し、`depth_dolly` / `panel_float` は「導入後に実装」と注記。

### 3.2 緩急（pacing）
- `easingPresets.ts` に名前付きカーブ（例: `cinematicInOut`, `impactSnap`, `slowDrift`, `springSoft`）を定義し、全モーションが共有。
- `sceneTypePresets.ts` が sceneType ごとに推奨尺（frames）を持つ（例: `silent_hold` は長め、`flash_transition` は数フレーム）。緩急はシーン設計レベルで宣言される。

### 3.3 カメラ感（camera）
- `camera/CameraRig.tsx` は既存 `Motion.tsx` の `CameraRig` を内部利用し、`cameraPresets.ts`（slow_push_in / fast_push_in / pull_out / impact_zoom / cinematic_drift / subtle_shake …）で動きを名前指定できるようにする。
- 既存 `CameraRig` の引数は `seed` / `intensity` / `children`。新ラッパは preset 名 → `{intensity, 方向, カーブ}` を解決して既存に渡す（既存シグネチャを壊さない）。

### 3.4 光 / 空気（light / atmosphere）
- `visual/LightSweep` → 既存 `Motion.tsx` `LightSweep`、`visual/ParticleField` → 既存 `Particles`、`visual/VignetteOverlay` → 既存 `Vignette`、`visual/FilmGrain` → 既存 `Grain` をラップ。
- `visual/AtmosphereOverlay` / `visual/ColorGradeOverlay` は `colorPresets.ts` 駆動の新規薄レイヤ（既存 `RoughCut` 内の `grade` グラデーションと同じ手法を共通化）。`ambient_overlay` グラマーに対応。

### 3.5 意味のある字幕 / 図解（meaningful captions / diagrams）
- 字幕は `RoughCut` の `CaptionBand` / `Telop`、`OpenCaption`、`CitationLowerThird` を再利用。`text/LowerThird` は `CitationLowerThird` / `Telop` を活用し、出典・話者・役職を意味付きで出す。
- 図解は `DiagramFlow`（手順フロー）と `SceneArt`（Timeline/Scales/MapUS 等の象徴）を `layout/TimelineReveal` / `layout/RelationshipMap` / `layout/DataReveal` / `layout/MapFocus` がラップ。`diagram_draw` / `relationship_connect` / `timeline_flow` / `data_reveal` / `map_focus` グラマーに対応。
- 「意味のある」= 装飾ではなく、claim / 因果 / 時系列を視覚化する。入力は pd-scenes の構造化データ（数値・関係・年表）であり、デザインは preset が決める。

### 3.6 SFX 同期（sfx sync）
- `audio/SfxCue`（単発）と `audio/SfxScheduler`（複数キューをフレームに同期配置）を新設。`sfxPresets.ts` が grammar ごとの推奨 SFX（impact / whoosh / riser / click / ambience）を持つ。
- 同期点は「モーションのキーフレーム」と同じ frame 値を共有することで、視覚と音を 1 つの真実（preset の frame）から駆動し、ズレない。
- 仮定: SFX 音源は権利クリア済み素材を `remotion/public/sfx/` 配下に置き、`staticFile()` で参照（メモリ feedback_rights_check_before_download 準拠。実値・パスは episode 側に持たせる）。

### 3.7 統一感（consistency）
- すべての色・フォント・グレード・グレインが `BRAND` と preset から来るため、話を跨いでも質感が揃う。
- `layout/ChapterTitle` → `Opening` / `Brand`（`PdMonogram` / `Horizon`）活用、`Bookends`（`BrandOpening` / `BrandEndcard`）で開始終了の枠を統一。

### 3.8 コード操作（code-operability）
- 入力は JSON 的な構造化データ + preset 名。Claude/Codex は preset 値・grammar・sceneType を編集するだけで映像を修正できる。
- 型安全（TypeScript 判別可能 union）で、未知の grammar / sceneType / preset キーはコンパイル時に弾く。これが「壊さずに量産・修正」の土台。

### 3.9 量産（scale）
- `RoughCutData` 互換の入力を受け取り、shot ごとに sceneType と grammar を割り当てれば、1 話分のラフカット〜本編が自動生成される。
- preset を 1 箇所変えると全話に波及するため、シリーズ全体の質感アップデートが安価（メモリ pd-series-ep6-15 のスレート量産と整合）。

---

## 4. 外部 AI 動画の位置づけ（見せ場限定）

CANON のとおり、Runway 等の AI 動画は次の sceneType の**見せ場のみ**に限定する：
`opening_hook` / `turning_point` / `reenactment` / `emotional_pause` / `ending` / `transition_bridge`（一部） / `abstract_emotion`。

それ以外の本編（explanation / timeline / evidence_board / comparison / data_reveal / quote / chapter_title / summary など）は、すべてこの Remotion Motion System（コード）で作る。
AI 動画は `RoughShot` の `assetType` で `stock_video` 相当として取り込み（権利・開示トラッキング必須。CLAUDE.md 不変条件 11: 生成映像は記録ではない＝本物の記録として提示しない）、Motion System のグレード/グレイン/字幕レイヤを上から重ねて全体の統一感に溶け込ませる。

---

## 5. 受け入れ基準（システム全体）

1. **型安全**: grammar / sceneType / preset キーは型で固定。未知値はコンパイルエラー。
2. **preset 駆動**: コンポーネント本体にマジックナンバー・色直書きを残さない（`BRAND`/preset 参照のみ）。
3. **既存を壊さない**: 既存 `components/` と `compositions/` の公開 API・既存合成（RoughCut/Episode/Opening/ColdOpen 等）は無改変で従来どおりレンダーできる。
4. **二重実装しない**: 新層は必ず既存プリミティブをラップ。同等機能の再実装をしない（CLAUDE.md 不変条件 14）。
5. **未導入依存は分離**: `@remotion/three|lottie|transitions` / `three` 依存要素は Phase4 とし、未導入でも他要素のビルド・レンダーが通る。
6. **コード操作で修正可能**: タイムライン手編集なしに、構造化データ + preset 変更だけで見た目を変えられる。

---

## 6. 関連文書

- `docs/motion-design-language.md` — 30 motion grammar の定義表（目的/印象/sceneType/尺/SFX/VFX/素材/コンポーネント/難易度/乱用リスク/品質基準）。
- `docs/remotion-animation-component-roadmap.md` — `src/motion/*` 全コンポーネントの役割/props/ラップ対象/依存/Phase/受け入れ基準、preset 各ファイルの設計。
- `remotion/src/brand.ts` — ブランドトークン（色/フォント/解像度）。
- CLAUDE.md §1,2,10,14 / `.claude/rules/18-no-overengineering.md`（編集ツールの再発明禁止）。
