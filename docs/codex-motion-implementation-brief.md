# Codex 実装指示書 — Phase 1（Motion System 最小エンジン + MotionDemo）

ステータス: 実装指示（未着手）／前提・仮定: Remotionアプリのルートは `remotion/`。新規モーションは `remotion/src/motion/*`。Brandは `remotion/src/brand.ts`。

このPhaseの鉄則：**いきなり本番動画に適用しない。新しい `MotionDemo` コンポジションの上だけで作る。既存の本番Compositionは1行も壊さない。外部有料ツール・新規依存は原則入れない（Phase1は依存追加ゼロで完結する）。**

---

## 0. 実装目的
- 「コードで操作できるMotion System」の**最小エンジン**を、**既存コンポーネントをラップ**する形で立ち上げる。
- 確認用の **`MotionDemo` コンポジション**を作り、各部品が動くことをstudioで見られるようにする。
- 設計書（`docs/code-operable-motion-system.md` / `motion-design-language.md` / `remotion-animation-component-roadmap.md`）の通りに、**presets駆動**で組む。

## 1. 触ってよいファイル（新規作成のみ）
- `remotion/src/motion/presets/` … `motionPresets.ts` `easingPresets.ts` `sceneTypePresets.ts` `sfxPresets.ts` `colorPresets.ts`（純TS・依存なし）
- `remotion/src/motion/camera/CameraRig.tsx` `cameraPresets.ts`（既存 `components/Motion.tsx` の `CameraRig` を内部利用）
- `remotion/src/motion/visual/` … `CinematicImage.tsx`(→`RoughCut`の`MovingImage`発想)・`ParallaxScene.tsx`(→`components/Parallax.tsx`)・`FilmGrain.tsx`(→`components/Grain.tsx`)・`VignetteOverlay.tsx`(→`Motion.tsx`の`Vignette`)・`LightSweep.tsx`(→`Motion.tsx`の`LightSweep`)・`ParticleField.tsx`(→`Motion.tsx`の`Particles`)
- `remotion/src/motion/text/` … `DynamicText.tsx` `ImpactTitle.tsx` `KeywordPunch.tsx`（→既存 `KineticType` を活用）
- `remotion/src/motion/transitions/MotionTransition.tsx`（→既存 `Transition.tsx` の `WipeTransition` を内部利用）
- `remotion/src/motion/audio/` … `SfxCue.tsx` `SfxScheduler.tsx`（`<Audio>` をフレーム指定で鳴らす。素材が無ければ無音でも可）
- `remotion/src/compositions/MotionDemo.tsx`（**新規・確認用**）
- `remotion/src/Root.tsx`（**追記のみ**：`MotionDemo` を1つ登録する。既存登録は触らない）

## 2. 触らないファイル（厳禁）
- 既存の本番Composition：`RoughCut.tsx` / `Opening.tsx` / `ColdOpen.tsx` / `Episode.tsx` / `Animatic.tsx` / `*Premium.tsx` / 各 `*_roughcut.ts` データ。
- 既存 `remotion/src/components/*`（ラップして使うが**中身は変更しない**）。
- `episodes/`・`scripts/`・各話の台本/claims。
- `.env`・鍵・認証情報（読むのも書くのも不要）。

## 3. Phase1で作るコンポーネント（依存追加なし・既存ラップ）
| 新規 | ラップ/活用する既存 | 役割 |
|---|---|---|
| `CameraRig`(motion/camera) | `Motion.tsx` CameraRig | preset名でカメラ寄り引き/パン |
| `CinematicImage` | `MovingImage`発想 | 画像＋motion grammar（slow_push_in等）で必ず動かす |
| `ParallaxScene` | `Parallax.tsx` | 多層パララックスで奥行き |
| `FilmGrain` `VignetteOverlay` `LightSweep` `ParticleField` | `Grain`/`Vignette`/`LightSweep`/`Particles` | 空気感オーバーレイ |
| `DynamicText` `ImpactTitle` `KeywordPunch` | `KineticType` | 意味のある字幕/見出しの動き |
| `MotionTransition` | `WipeTransition` | カット間トランジション |
| `SfxScheduler` `SfxCue` | `<Audio>` | フレーム同期で効果音（素材無ければ無音プレースホルダ） |

- **presetsが単一の真実**：色は `brand.ts` から、動きは `motionPresets`/`easingPresets`、sceneType別の既定は `sceneTypePresets`。各コンポーネントは `preset` か `props` で挙動を変えられること（Claude/Codexが後から数値を直せる）。
- **未導入依存（@remotion/three / lottie / transitions）には触れない**（three/lottie系はPhase2。`LottieMotion.tsx` は既にある非破壊プレースホルダのまま）。

## 4. MotionDemo に並べるもの（確認用シーン）
`Series` で順に：`CinematicImage`(slow_push_in)→`ParallaxScene`→`ImpactTitle`+`KeywordPunch`→`DynamicText`→`MotionTransition`→空気感(`FilmGrain`+`VignetteOverlay`+`LightSweep`+`ParticleField`)→`SfxScheduler`で効果音を1つ同期。各シーン2〜3秒、合計30〜45秒。素材は `remotion/public` の既存画像か単色で可。

## 5. 守ること
- **既存の本番Compositionの見た目・登録を一切変えない。** `MotionDemo` は新規idで追加。
- **TypeScriptエラーを新たに増やさない。** （注意：既存 `MadoffPremium.tsx` に**前からある**型エラーが1件あるが、それは本Phaseの対象外。新規ファイルでエラーを出さないこと。）
- 秘密情報を書かない。実在人物の肖像を作らない。
- preset/propsで後から調整できる構造にする（ハードコード最小）。

## 6. 確認方法
- `cd remotion && npm run typecheck` … 新規分でエラーが増えていないこと。
- `npm run studio` … `MotionDemo` を開き、各部品が動く/字幕が読める/効果音が同期するのを目視。
- （任意）`npm run render MotionDemo out/motion_demo.mp4 --crf=18` で書き出し確認。

## 7. 最後に必ず出すもの
- **変更/新規ファイルの一覧**（パス）。
- typecheck結果（新規エラー0）。
- studioで確認した所感（動いた/字幕可読/SFX同期）。
- 次Phaseに残した項目（three/lottie/高度トランジション=要依存導入）。

---
このPhaseが通ったら、Phase2（Asset Factoryフォルダ整備＋`schemas/asset-manifest.schema.json`実体化＋manifest登録）→ Phase4（リッチ部品・three/lottie）→ Phase5（Scene Plan→素材選択→本番適用）へ進む。詳細は `docs/remotion-animation-component-roadmap.md` と `docs/production-workflow.md`。
