# 06 — Visual System, SDXL and Continuity

## 1. Visual Objective

画像は「きれい」であることより、次のいずれかを担うことが重要。

- identify：誰・何かを認識させる
- locate：どこかを理解させる
- explain：仕組みを説明する
- compare：違いを比較する
- sequence：順序を示す
- quantify：規模を感じさせる
- humanize：人間的な具体を与える
- tension：緊張を作る
- atmosphere：空気を作る
- reset attention：注意を更新する
- symbolize：慎重に象徴化する

役割を説明できない画像は不要。

## 2. Visual Modes

- documentary-realistic reenactment
- location/environment
- object/detail
- archival-style illustration
- map
- timeline
- diagram
- data visualization
- abstract conceptual
- typography
- negative-space breathing shot
- transition texture

全シーンを映画的な人物画像へしない。説明に最適な視覚形式を選ぶ。

## 3. Visual Bible

### 3.1 Channel-level

- aspect ratio
- realism level
- contrast
- saturation
- film grain
- lighting tendencies
- typography
- map style
- diagram style
- lower thirds
- citation style
- AI reconstruction label
- transition language
- thumbnail-safe area

### 3.2 Episode-level

- era
- geography
- palette
- recurring subjects
- recurring locations
- wardrobe
- materials
- weather
- visual motifs
- prohibited anachronisms
- emotional arc

## 4. Scene Specification

各scene：

- scene_id
- script_span_ids
- scene_purpose
- primary_claim_id
- emotional_function
- visual_mode
- duration_estimate
- required_assets
- continuity_refs
- transition_in
- transition_out
- on_screen_text
- source_sensitivity
- regeneration_priority
- human_review_required

## 5. Shot Diversity

隣接ショットで以下を管理。

- scale：wide / medium / close / macro
- angle：eye / high / low / overhead
- motion：static / pan / push / pull / parallax
- composition：center / thirds / leading lines / negative space
- brightness
- subject count
- information density
- visual mode

変化のための変化ではなく、理解と注意維持のために使う。

## 6. Character Continuity

### 6.1 実在人物

- 肖像・名誉・誤認リスクを先に評価。
- 本人の未確認行動を映像で断定しない。
- 顔が確定しない時代人物を写真のように確定描写しない。
- 必要に応じて背面、遠景、手元、シルエット、図解へ逃がす。

### 6.2 再現人物

- character_id
- age band
- gender presentation
- historically supported ethnicity where relevant
- face reference
- hair
- clothing
- body type
- accessories
- allowed variations
- prohibited variations
- seed/reference embeddings

同一人物を必要以上に顔アップで使わず、連続性負荷を下げる。

## 7. Location Continuity

- architecture
- terrain
- vegetation
- season
- time of day
- weather
- material culture
- signage
- transport
- interior layout
- light direction

## 8. Prompt Compiler

プロンプトは自由作文ではなく構造から組み立てる。

```yaml
visual_intent:
subject:
action:
setting:
time_period:
geography:
wardrobe_material:
camera:
lens:
composition:
lighting:
color_mood:
atmosphere:
realism:
continuity_refs:
style_profile:
negative_constraints:
aspect_ratio:
seed_policy:
model_profile:
lora_control_refs:
candidate_count:
qc_profile:
```

## 9. Negative Constraints

- malformed anatomy
- extra limbs/fingers
- duplicated people
- floating objects
- unreadable text
- watermark/logo
- modern object in historical scene
- wrong architecture/wardrobe
- plastic skin
- overprocessed HDR
- inconsistent age/identity
- accidental gore
- UI elements
- frame/border
- distorted perspective
- impossible shadows

## 10. Candidate Count by Priority

- hero shot：4〜8候補
- Tier A：4候補
- Tier B：2〜3候補
- Tier C：1〜2候補
- continuity-critical：基準画像＋派生
- diagram/map：専用レンダラー優先

候補数は固定せず、採用率とコストから学習する。

## 11. Automated Visual QC

- file corruption
- resolution / aspect ratio
- NSFW
- face/hand anomaly
- text/watermark
- exact/near duplicate
- semantic match
- anachronism signal
- continuity embedding distance
- exposure
- blur
- crop safety
- subject placement
- editability
- neighboring shot similarity

重要シーンは自動点数だけで最終採用しない。

## 12. Candidate Selection Score

- semantic match
- factual plausibility
- composition
- continuity
- technical quality
- emotional function
- editability
- crop safety
- novelty relative to neighbors
- brand fit
- rights/safety

## 13. Regeneration Strategy

全体を再生成しない。

- prompt defect：prompt修正
- seed defect：seed変更
- model defect：checkpoint/LoRA変更
- composition defect：control/reference変更
- continuity defect：reference強度変更
- semantic defect：scene intent再解釈
- repeated failure：visual mode変更
- rights risk：非人物・図解へ変更

## 14. Generated Text

SDXL画像内に説明文字を生成させない。文字は編集工程で正確に載せる。

## 15. Maps and Diagrams

地図、年表、図解、数値表示はSVG/HTML/専用レンダラーを優先。

理由：

- 正確な文字
- 再編集
- 色とブランド統一
- 数値の正確性
- アニメーション
- 多言語化

## 16. Image Reuse

同一画像の再使用は許可するが管理する。

- exact reuse count
- transformed reuse
- scene distance
- prominence
- viewer detectability
- narrative justification

冒頭・転換点・結論で目立つ再利用は避ける。

## 17. Visual Safety Flags

- accidental logo
- copyrighted character
- public figure impersonation
- graphic violence
- misleading evidence portrayal
- sensitive location
- minors
- medical imagery
- extremist symbols
- political persuasion context
- sexual content
- private information
