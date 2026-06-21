# Remotion Animation Component Roadmap（`src/motion/*` 実装ロードマップ）

> ステータス: 設計（未実装）。本書は配置・props・ラップ対象・Phase・受け入れ基準・preset 設計のみ。コードは未生成。

## 前提・仮定

- Remotion v4 / 1920×1080 @ 30fps。新層の物理配置は **`remotion/src/motion/*`**（CANON の `src/motion/*` を Remotion アプリルート `remotion/` 配下に解決。以後 `src/motion/*` と表記）。
- 既存プリミティブ（`remotion/src/components/*`, `remotion/src/compositions/*`）は監査済み・実在。新層はこれらを**ラップ**し、二重実装しない（CLAUDE.md 不変条件 14）。
- ブランドは `remotion/src/brand.ts` `BRAND`。color/font の再定義禁止。
- 未導入依存 `@remotion/three` / `@remotion/lottie` / `@remotion/transitions` / `three` は **Phase4・導入後**。導入は Codex 担当。未導入でも他要素のビルド・レンダーが通ること。
- 実装難易度: 低 / 中 / 高。Phase: 3（最小エンジン）/ 4（リッチ）。
- SFX/素材は権利クリア済み前提。実パス・実 `.env` 値は本書に含めない。

---

## 1. ビルド順（Phase3 → Phase4）

### Phase 3 — 最小エンジン（依存追加なし・既存ラップ中心）
目的: 「構造化データ + preset 名」で本編の大半（explanation/timeline/evidence/quote/data/comparison/chapter）が作れる状態。
順序:
1. `presets/`（easingPresets → motionPresets → colorPresets → sceneTypePresets → sfxPresets）と `resolveMotion()` 純粋関数。
2. `camera/`（CameraRig, cameraPresets）。
3. `visual/`（FilmGrain, VignetteOverlay, LightSweep, ParticleField, ParallaxScene, CinematicImage, ColorGradeOverlay, AtmosphereOverlay）。
4. `text/`（DynamicText, ImpactTitle, KeywordPunch, QuoteReveal, NumberCounter, LowerThird）。
5. `layout/`（MotionCard, ChapterTitle, EvidenceBoard, TimelineReveal, DataReveal, MapFocus, ComparisonFrame）。
6. `transitions/`（MotionTransition, FlashTransition, DarkFadeTransition; WhipTransition は新規ロジック版なら Phase3 可）。
7. `audio/`（SfxCue, SfxScheduler）。

### Phase 4 — リッチ（依存導入後・高難度）
順序:
1. 依存導入（Codex）: `@remotion/transitions`, `@remotion/three`, `three`, `@remotion/lottie`。
2. `transitions/`（GlitchTransition, FilmBurnTransition, WhipTransition の transitions 版）。
3. `layout/RelationshipMap`（新規・高難度。依存不要だが Phase4 でリッチ化）。
4. `three/`（ThreeCameraScene, FloatingPanels3D, DepthStage）。
5. `lottie/LottieMotion`。

各 Phase 完了時、既存合成（RoughCut/Episode/Opening/ColdOpen/Premium 各種）が無改変でレンダーできることを回帰確認する。

---

## 2. コンポーネント一覧（役割 / props / ラップ対象 / 依存 / grammar / sceneType / Phase / 難易度）

> props は「主要なもの」。全コンポーネント共通で任意の `seed?: string`（決定論用）と preset 上書き props を受ける想定。

### camera/

| コンポーネント | 役割 | 主要 props | ラップする既存 | 依存 | 対応 grammar | 対応 sceneType | Phase | 難易度 |
|---|---|---|---|---|---|---|---|---|
| CameraRig | preset 名でカメラ運動を駆動 | `preset`(cameraPresets キー), `intensity?`, `seed?`, `children` | Motion.tsx `CameraRig` | — | slow_push_in, fast_push_in, pull_out, impact_zoom, subtle_shake, cinematic_drift, depth_dolly(代替) | 全般 | 3 | 低 |
| cameraPresets.ts | カメラ運動の名前付き定義 | （データ） | — | — | 上記すべて | — | 3 | 低 |

### text/

| コンポーネント | 役割 | 主要 props | ラップする既存 | 依存 | 対応 grammar | 対応 sceneType | Phase | 難易度 |
|---|---|---|---|---|---|---|---|---|
| DynamicText | 汎用テキスト出現（reveal 基盤） | `text`, `preset`, `style?` | KineticType | — | soft_reveal, keyword_punch | explanation, summary, quote | 3 | 低 |
| ImpactTitle | 章題/タイトルの強打着地 | `title`, `subtitle?`, `slam?` | KineticType + camera/CameraRig | — | title_slam, impact_zoom, light_sweep | chapter_title, opening_hook | 3 | 中 |
| KeywordPunch | 重要語の強調パンチ | `words[]`, `sfx?` | KineticType | — | keyword_punch | explanation, problem_statement | 3 | 低 |
| QuoteReveal | 引用のタイプライタ開示 | `quote`, `attribution?`, `speed?` | OpenCaption (+ CitationLowerThird) | — | quote_typewriter, silent_hold | quote, turning_point | 3 | 低 |
| NumberCounter | 数値の countup | `to`, `from?`, `format?`, `unit?` | （新規・interpolate）| — | number_countup | data_reveal, company_profile | 3 | 中 |
| LowerThird | 出典/話者/役職の下/上三分 | `name`, `role?`, `source?`, `variant?` | CitationLowerThird / RoughCut `Telop` | — | evidence_reveal, quote_typewriter | quote, evidence_board, character_profile | 3 | 低 |

### visual/

| コンポーネント | 役割 | 主要 props | ラップする既存 | 依存 | 対応 grammar | 対応 sceneType | Phase | 難易度 |
|---|---|---|---|---|---|---|---|---|
| CinematicImage | 写真/AI 画像に Ken-Burns/parallax | `src`, `motion?`(ken_burns\|parallax), `seed?` | RoughCut `MovingImage` | — | slow_push_in, parallax_depth, cinematic_drift | explanation, place_intro, character_profile | 3 | 低 |
| ParallaxScene | 多層 2.5D 奥行き | `layers[]`(depth+node), `amount?` | Parallax | — | parallax_depth | place_intro, chapter_title, abstract_emotion | 3 | 低 |
| LightSweep | 走る光のオーバーレイ | `color?`, `seed?` | Motion.tsx `LightSweep` | — | light_sweep | chapter_title, opening_hook, ending | 3 | 低 |
| ParticleField | 漂う塵/光粒 | `count?`, `color?`, `seed?` | Motion.tsx `Particles` | — | particle_drift | emotional_pause, abstract_emotion | 3 | 低 |
| VignetteOverlay | ビネット | `strength?` | Motion.tsx `Vignette` | — | ambient_overlay | 全般 | 3 | 低 |
| FilmGrain | フィルムグレイン | `opacity?` | Grain | — | ambient_overlay | 全般 | 3 | 低 |
| ColorGradeOverlay | カラーグレード | `preset`(colorPresets キー) | （新規・grade 共通化）| — | ambient_overlay | 全般 | 3 | 低 |
| AtmosphereOverlay | 霧/色被り空気感 | `preset`, `strength?` | （新規）| — | ambient_overlay | place_intro, emotional_pause | 3 | 低 |

> 注: `ColorGradeOverlay` は `compositions/RoughCut.tsx` 内のローカル `grade` グラデーションを共通化したもの。RoughCut 側は当面無改変のまま（重複は許容、後日 RoughCut が新コンポーネントを利用する形へ収斂）。

### layout/

| コンポーネント | 役割 | 主要 props | ラップする既存 | 依存 | 対応 grammar | 対応 sceneType | Phase | 難易度 |
|---|---|---|---|---|---|---|---|---|
| MotionCard | 単体カード（影/出現） | `children`, `preset?` | （新規・基盤）| — | card_stack, soft_reveal | comparison, explanation | 3 | 低 |
| EvidenceBoard | 証拠の段階開示 | `items[]`(src/quote/source), `order?` | SceneArt(Document/Scales) + LowerThird | — | evidence_reveal | evidence_board, turning_point | 3 | 中 |
| TimelineReveal | 年表の流れ開示 | `nodes[]`(date,label) | SceneArt(Timeline) | — | timeline_flow | timeline, summary | 3 | 中 |
| DataReveal | グラフ/比率の段階開示 | `series[]`, `axis?`, `unit?` | NumberCounter 連携（新規）| — | data_reveal, number_countup | data_reveal, comparison | 3 | 高 |
| MapFocus | 地図フォーカス/ピン | `region`, `pins[]` | SceneArt(MapUS) | — | map_focus | place_intro, timeline | 3 | 中 |
| ComparisonFrame | 二項/多項比較レイアウト | `left`, `right`(or `items[]`) | MotionCard | — | card_stack, data_reveal | comparison | 3 | 中 |
| ChapterTitle | 章扉（ブランド枠） | `title`, `chapterNo?`, `subtitle?` | Opening / Brand(`PdMonogram`,`Horizon`) / Bookends(`BrandOpening`) | — | title_slam, light_sweep | chapter_title | 3 | 中 |
| RelationshipMap | 人物/組織の関係図 | `nodes[]`, `edges[]` | DiagramFlow（部分）+ 新規 | — | relationship_connect, diagram_draw | character_profile, company_profile | 4 | 高 |

### transitions/

| コンポーネント | 役割 | 主要 props | ラップする既存 | 依存 | 対応 grammar | 対応 sceneType | Phase | 難易度 |
|---|---|---|---|---|---|---|---|---|
| MotionTransition | 転換の統一入口（preset で種別選択） | `kind`(hard_cut\|wipe\|flash\|whip\|...), `durationFrames?` | Transition.tsx `WipeTransition` | — | hard_cut, flash_transition, whip_transition | transition_bridge ほか | 3 | 中 |
| FlashTransition | 白フラッシュ転換 | `durationFrames?`, `color?` | （新規・依存不要）| — | flash_transition | turning_point, opening_hook | 3 | 低 |
| DarkFadeTransition | 暗転フェード | `durationFrames?` | （新規・依存不要）| — | soft_reveal, silent_hold | emotional_pause, ending | 3 | 低 |
| WhipTransition | ホイップ（ブラー）転換 | `durationFrames?`, `direction?` | （新規ロジック / または @remotion/transitions）| (@remotion/transitions) | whip_transition | transition_bridge | 3（新規版）/4（transitions 版） | 中 |
| GlitchTransition | グリッチ転換 | `durationFrames?`, `intensity?` | （新規）| — | glitch_transition | turning_point, problem_statement | 4 | 高 |
| FilmBurnTransition | フィルムバーン転換 | `durationFrames?` | （新規 or @remotion/transitions）| (@remotion/transitions) | flash_transition(類) | transition_bridge, ending | 4 | 中 |

### audio/

| コンポーネント | 役割 | 主要 props | ラップする既存 | 依存 | 対応 grammar | 対応 sceneType | Phase | 難易度 |
|---|---|---|---|---|---|---|---|---|
| SfxCue | 単発 SFX をフレーム発火 | `cue`(sfxPresets キー), `atFrame`, `volume?` | Remotion `Audio` | — | impact_zoom, title_slam, keyword_punch | 全般 | 3 | 低 |
| SfxScheduler | 複数キューをまとめて同期配置 | `cues[]`(cue+atFrame) | SfxCue | — | 全般（同期管理）, silent_hold(無音) | 全般 | 3 | 中 |

### three/（Phase4・導入後）

| コンポーネント | 役割 | 主要 props | ラップする既存 | 依存 | 対応 grammar | 対応 sceneType | Phase | 難易度 |
|---|---|---|---|---|---|---|---|---|
| ThreeCameraScene | 3D シーンの基盤（カメラ/ライト） | `children`, `cameraPreset` | — | @remotion/three, three | depth_dolly, panel_float | abstract_emotion, opening_hook | 4 | 高 |
| FloatingPanels3D | パネルの 3D 浮遊配置 | `panels[]` | ThreeCameraScene | @remotion/three, three | panel_float | data_reveal, company_profile | 4 | 高 |
| DepthStage | Z 軸ドリー奥行きステージ | `layers[]`(z), `dolly?` | ThreeCameraScene | @remotion/three, three | depth_dolly | opening_hook, transition_bridge | 4 | 高 |

### lottie/（Phase4・導入後）

| コンポーネント | 役割 | 主要 props | ラップする既存 | 依存 | 対応 grammar | 対応 sceneType | Phase | 難易度 |
|---|---|---|---|---|---|---|---|---|
| LottieMotion | Lottie アニメ再生 | `src`, `loop?`, `speed?` | — | @remotion/lottie | diagram_draw, soft_reveal | explanation, solution_reveal | 4 | 中 |

---

## 3. presets 設計（各ファイルの中身：キー例）

`presets/` は**単一の真実**。すべての数値・色・尺・カーブ・SFX をここに集約し、コンポーネントは preset を解決して props で上書きする。型は判別可能 union を用い、未知キーをコンパイル時に弾く。

### easingPresets.ts
名前付きカーブ（cubic-bezier / spring 設定）。

| キー | 用途 | 概略 |
|---|---|---|
| `cinematicInOut` | 一般の滑らかな出入り | 緩やかな ease-in-out |
| `impactSnap` | 強打着地（title_slam/impact_zoom） | 速→急停止 |
| `slowDrift` | cinematic_drift/silent_hold | 極低速・ほぼ線形 |
| `springSoft` | soft_reveal/card_stack | 軽いオーバーシュート無し spring |
| `springPop` | keyword_punch | 小オーバーシュート spring |
| `linear` | countup/進行系 | 線形 |

### motionPresets.ts
30 grammar → 具体パラメータ（尺・カーブ参照・強度・方向・推奨 SFX/VFX 参照）。`resolveMotion(grammar, sceneType, overrides)` がこれを読む。

| キー（grammar） | 主パラメータ例 |
|---|---|
| `slow_push_in` | `{ durationFrames: 180, easing: 'cinematicInOut', scaleFrom: 1.05, scaleTo: 1.15 }` |
| `impact_zoom` | `{ durationFrames: 12, easing: 'impactSnap', scaleTo: 1.25, sfx: 'impact_low' }` |
| `keyword_punch` | `{ perWordFrames: 12, easing: 'springPop', underline: 'gold', sfx: 'click_soft' }` |
| `number_countup` | `{ durationFrames: 36, easing: 'linear', endSfx: 'tick_end' }` |
| `flash_transition` | `{ durationFrames: 8, color: 'white', sfx: 'impact_riser' }` |
| `silent_hold` | `{ durationFrames: 60, mute: true, drift: 'cinematic_drift' }` |
| … | （30 grammar 全キーを同形式で定義） |

> マジックナンバーはここに集約し、コンポーネント本体に直書きしない。色参照はキー名（'gold' 等）で持ち、解決時に `BRAND` を引く。

### sceneTypePresets.ts
20 sceneType → 既定の {カメラ grammar, レイアウト, 字幕方針, SFX セット, 推奨尺レンジ, 既定トランジション}。

| キー（sceneType） | 既定の組み合わせ例 |
|---|---|
| `opening_hook` | `{ camera: 'fast_push_in', transitionIn: 'flash_transition', sfx: 'riser', allowAIVideo: true }` |
| `chapter_title` | `{ layout: 'ChapterTitle', grammar: 'title_slam', vfx: ['light_sweep'] }` |
| `explanation` | `{ camera: 'slow_push_in', text: 'KeywordPunch', overlay: 'ambient_overlay' }` |
| `evidence_board` | `{ layout: 'EvidenceBoard', grammar: 'evidence_reveal' }` |
| `timeline` | `{ layout: 'TimelineReveal', grammar: 'timeline_flow' }` |
| `data_reveal` | `{ layout: 'DataReveal', grammar: ['data_reveal','number_countup'] }` |
| `quote` | `{ text: 'QuoteReveal', grammar: 'quote_typewriter', lowerThird: true }` |
| `turning_point` | `{ camera: 'impact_zoom', transitionIn: 'flash_transition', allowAIVideo: true }` |
| `emotional_pause` | `{ grammar: 'silent_hold', vfx: ['particle_drift'], allowAIVideo: true }` |
| `ending` | `{ layout: 'BrandEndcard 連携', grammar: 'pull_out', allowAIVideo: true }` |
| … | （20 sceneType 全キーを同形式で定義。`allowAIVideo` で外部 AI 動画許可シーンを宣言: opening_hook/turning_point/reenactment/emotional_pause/ending/transition_bridge/abstract_emotion のみ true） |

### sfxPresets.ts
SFX キュー定義（論理名 → 相対 src / gain / フェード）。実音源は権利クリア済みを `remotion/public/sfx/` 配下に置き `staticFile()` で参照（実パスは episode 側）。

| キー | 用途 | 概略 |
|---|---|---|
| `impact_low` | 強打/着地 | 低音ドン |
| `impact_riser` | フラッシュ転換前後 | riser+hit |
| `whoosh` | whip/pull_out | 通過音 |
| `click_soft` | keyword_punch | クリック |
| `tick`/`tick_end` | countup | カチカチ＋終端 |
| `glitch` | glitch_transition | デジタルノイズ |
| `ambient_room` | 環境ベッド | 持続アンビエンス |

### colorPresets.ts
grade / atmosphere の色組（すべて `BRAND` 参照）。

| キー | 用途 | 概略 |
|---|---|---|
| `neutralDoc` | 標準ドキュメンタリー | navy↘ink の縦グラデ + 弱ビネット |
| `coldTension` | 緊張/不穏 | electric 寄りの寒色被り |
| `warmHuman` | 人物/情感 | gold 微量の暖色被り |
| `archival` | 資料/過去 | 彩度低・グレイン強め |
| `nightAmbient` | 夜/抽象 | ink 主体・粒子映え |

---

## 4. 受け入れ基準（コンポーネント共通）

各コンポーネントは次を満たして初めて「done」とする（CLAUDE.md §7 に整合）：

1. **型安全**: props・preset キー・grammar・sceneType は TypeScript で固定。未知値はコンパイルエラー。`tsc --noEmit`（`npm run typecheck`）が通る。
2. **preset 駆動**: 数値・色・尺・カーブ・SFX はコンポーネント本体に直書きせず、preset または `BRAND` を参照。明示 props で局所上書き可能。
3. **既存を壊さない**: ラップ対象の既存コンポーネントは無改変。既存合成（RoughCut/Episode/Opening/ColdOpen/各 Premium/Thumbnails）が従来どおりレンダーできる（回帰確認）。
4. **二重実装しない**: 同等機能を再実装せず、必ず既存プリミティブをラップ（CLAUDE.md 不変条件 14）。
5. **決定論**: 乱数は `seed` から決定論的に。同一入力で同一フレーム出力。
6. **依存分離**: `@remotion/three|lottie|transitions` / `three` に依存する要素（three/*, lottie/*, 一部 transitions/*）は Phase4 とし、未導入環境でも他要素のビルド・レンダーが成功する（import を Phase4 まで持ち込まない）。
7. **コード操作**: 構造化データ + preset 名のみで見た目を変更できる（タイムライン手編集不要）。
8. **権利/開示**: 外部 AI 動画・SFX・素材は権利クリア済みのみ配線。生成映像を本物の記録として提示しない（CLAUDE.md 不変条件 11）。

## 5. 関連文書
- `docs/code-operable-motion-system.md` — 思想・アーキテクチャ・9 要件の充足方針。
- `docs/motion-design-language.md` — 30 grammar の定義表と実装状態。
- `remotion/src/brand.ts` — ブランドトークン。
- 既存実装: `remotion/src/components/*`, `remotion/src/compositions/*`（ラップ対象）。
