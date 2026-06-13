# 08 — Editing and DaVinci Automation

## 1. 結論

編集を完全に手作業の創作とみなすと、PDはスケールしない。

編集を以下へ分解する。

- deterministic assembly
- rule-based motion
- template-based graphics
- machine-detectable QC
- human creative exceptions

## 2. Editing Layers

### 2.1 Assembly Edit

- 素材取り込み
- bin作成
- ナレーション配置
- シーン尺確定
- primary visuals配置
- 基本モーション
- BGM
- SFX
- 字幕
- lower thirds
- 引用・出典
- 基本トランジション
- 章マーカー

高率で自動化する。

### 2.2 Creative Finish

- テンポ微調整
- 強調
- 高度なFusion処理
- カラー
- ミックス
- 問題箇所の差替え
- 意図的な間
- 冒頭と結論の磨き込み

テンプレートと修正指示で短縮する。

## 3. Project Template

標準テンプレート：

- timeline settings
- bins
- tracks
- buses
- title templates
- subtitle style
- lower thirds
- adjustment clips
- color management
- render presets
- audio routing
- chapter markers
- source/citation overlay
- AI visualization disclosure
- end screen
- brand sting

## 4. Track Convention

例：

- V1：primary visual
- V2：secondary/overlay
- V3：maps/graphics
- V4：titles/lower thirds
- V5：citations/disclosure
- A1：narration
- A2：narration repair
- A3：music
- A4：ambience
- A5：SFX
- A6：room tone/utility

設定で変更可能にする。

## 5. Timeline Plan

- timeline_start
- fps
- resolution
- scene ranges
- clip refs
- in/out
- crop
- transform keyframes
- transition
- overlays
- text
- audio levels
- ducking
- markers
- issue flags
- source labels
- motion template ID
- render profile

## 6. Assembly Algorithm

1. プロジェクト作成またはテンプレート複製
2. media pool bins作成
3. assets import
4. narration assembly
5. narrationからscene timing確定
6. primary visuals配置
7. secondary visuals/graphics配置
8. motion template適用
9. music cues
10. SFX/ambience
11. subtitle import
12. lower thirds/citations
13. markers
14. missing media check
15. review render
16. QC report

## 7. Timing Heuristics

- semantic beatにcutを合わせる。
- 固有名詞紹介直後に対象を見せる。
- 数字は比較視覚を伴う。
- 一枚を長く見せる場合は情報または感情の理由が必要。
- 短すぎる切替を連発しない。
- 章転換で視覚文法を変える。
- 結論は過剰に忙しくしない。
- 冒頭30秒は視覚の重複を最小化。
- 抽象説明が続く場合、図解または具体例へ切替。

## 8. Motion Template IDs

- M001 slow_push_center
- M002 slow_pull_reveal
- M003 pan_left_to_subject
- M004 pan_right_to_subject
- M005 vertical_architecture
- M006 depth_parallax
- M007 map_route
- M008 detail_to_wide
- M009 text_callout
- M010 static_hold
- M011 split_compare
- M012 timeline_progress

隣接シーンで同じmotion IDを反復し過ぎない。

## 9. Static Image Motion Rules

- push-in
- pull-out
- horizontal pan
- vertical pan
- parallax
- masked depth
- rack-focus simulation
- crop reveal
- split composition
- text callout
- map route
- timeline progress

同じKen Burnsを連続させない。動きはナレーションの意味に合わせる。

## 10. Review Markers

- RED：blocker
- ORANGE：high-risk fact/right
- YELLOW：low confidence
- BLUE：creative option
- GREEN：approved anchor
- PURPLE：thumbnail candidate

markerにissue IDと推奨修正を持たせる。

## 11. Edit QC

- ナレーションと映像の意味不一致
- シーン切替の遅れ
- 同一画像の過剰使用
- 類似構図連続
- black frame
- offline media
- 音切れ
- BGMが台詞を覆う
- 字幕欠落
- 字幕と音声の不一致
- 章マーカー不一致
- frame rate / resolution
- peak / loudness
- 不自然なtransition
- 誤った時代・人物・地図
- source表示漏れ
- brand要素欠落

## 12. Render Profiles

- review_low
- review_high
- final_master
- youtube_upload
- audio_only
- thumbnail_frame_export
- short_clip_preview

実パラメータはconfigへ置く。

## 13. DaVinci Integration Priority

1. native scripting API
2. importable timeline format / EDL / FCPXML等
3. generated media + project template
4. operator checklist
5. UI automationは最後の手段

UI座標操作をコアにしない。

## 14. Missing Capability Fallback

DaVinci APIでできない操作は、無理に不安定な自動化をせず、次を生成する。

- exact operator instructions
- marker
- target timestamp
- source/target parameter
- before/after screenshot reference if available
- estimated manual time

人間作業も構造化し、将来自動化候補として計測する。

## 15. Editing Bottleneck Reduction

最優先：

- 素材命名の自動化
- sceneとassetの紐付け
- narration基準の尺確定
- timeline assembly
- motion template
- subtitles
- source overlays
- issue markers
- selective relink
- review差分

高度な演出より、ゼロから並べる作業を消す。
