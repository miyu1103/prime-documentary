# Scene Plan スキーマ設計書（ShotRecipe 拡張 v2）

- **ステータス: 設計（未実装）** — 本書は仕様であり、実 JSON Schema ファイルの作成は Codex Phase に委ねる。コードブロックはそのまま使える完全なドラフト。
- **対象**: 既存 `schemas/scene-plan.schema.json`（`schema_version` `1.0.0`）を**壊さずに**、ShotRecipe / 20 sceneType / 30 motion grammar / `selectedAssets`(AF-id 参照) / sfx / transition / qualityTarget を載せる**拡張 v2**（`schema_version` `2.0.0`）。
- **既存を尊重**: v1 の `scenes[]` 構造・フィールド名は維持し、各 scene に任意の `shotRecipes[]` を**追加**する後方互換拡張とする（既存 v1 文書はそのまま valid のまま運用継続可能）。

---

## 1. 前提・仮定

1. **後方互換**: v1 の `scenes[]` items（`scene_id`,`script_span_ids`,`purpose`,`visual_mode`,`duration_seconds`,`priority`,`required_assets`,`human_review_required` など）はそのまま残す。v2 は scene item に**任意の** `shotRecipes` 配列と `sceneType` を足すだけ。`additionalProperties:false` は維持し、新フィールドを明示追加する。
2. **2 つの ID 体系**（CANON）: `selectedAssets` は Asset Factory 棚 ID `AF-<CATEGORY>-NNNN` を参照する。エピソード生成物 `PD-YYYY-NNN-S001-IMG-001` とは別系統で衝突させない。`sceneId` は ShotRecipe 内で既存 `^S[0-9]{3}$`（`common.schema.json $defs.sceneId`）を流用。
3. **sceneType(20) と既存 `visual_mode`(12) は別軸**: `visual_mode` は「どう映すか」(reenactment/diagram/map…)、`sceneType` は「物語上の役割」(opening_hook/data_reveal…)。両立させ、v1 の `visual_mode` を残したまま `sceneType` を追加する。
4. **motionRecipe** は CANON の 30 motion grammar 語彙の配列。Remotion の `RoughShot.motion`(5 値) より上位の演出語彙で、最終的に 5 値へ縮約される（§5 写像表）。
5. 秘密情報なし。パスは持たず ID 参照のみ（実体パスは Asset Manifest 側）。

## 2. 参照した既存 schema

| ファイル | 参照フィールド | v2 での扱い |
|---|---|---|
| `schemas/scene-plan.schema.json` | `schema_version`,`episode_id`,`revision`,`scenes[]`,`coverage`、scene の `scene_id`/`script_span_ids`/`visual_mode`/`duration_seconds`/`priority`/`transition_in`/`transition_out`/`on_screen_text` | **全て維持**。`schema_version` を `2.0.0` に上げ、scene に `sceneType`+`shotRecipes[]` を追加。`transition_in/out` は ShotRecipe の `transitionIn/Out` の scene 既定値として活用。 |
| `schemas/common.schema.json` | `$defs.sceneId`(`^S[0-9]{3}$`), `$defs.shotId`(`^S[0-9]{3}-SH[0-9]{3}$`), `$defs.revision`, `$defs.episodeId` | ShotRecipe の `sceneId`/`shotId` 形式に流用。 |
| `schemas/shotlist.schema.json` | `motion` enum, `suggested_asset_type` enum, `estimated_seconds`, `on_screen_text` | ShotRecipe→RoughShot 写像の橋渡し。`durationFrames` ↔ `estimated_seconds`。 |
| `schemas/asset.schema.json` | `qc.status`/`qc.score` | `qualityTarget` の語彙整合の参考。 |
| `docs/asset-manifest-schema.md`（本セット） | `id`(`AF-...`), `compatibleSceneTypes`, `type` | `selectedAssets`/`assetNeeds` の参照先。 |
| `remotion/src/compositions/RoughCut.tsx` / `scripts/import_to_remotion.py` | `RoughShot`(spanId,seconds,assetType,motion,src,clips,images,telop,priority), `RoughCutData` | §5 写像表の出力ターゲット。 |

---

## 3. ShotRecipe 型（CANON 14 フィールド）

ShotRecipe は 1 ショット（1 つ以上の script span を映す最小演出単位）の完全レシピ。scene に複数並ぶ。

| フィールド | 型 | 必須 | 値域 | 例 |
|---|---|:--:|---|---|
| `sceneId` | string | ◎ | `^S[0-9]{3}$`（`common.sceneId`） | `"S001"` |
| `shotId` | string | ○ | `^S[0-9]{3}-SH[0-9]{3}$`（`common.shotId`） | `"S001-SH001"` |
| `sceneType` | string(enum) | ◎ | **20 sceneType** | `"opening_hook"` |
| `durationFrames` | integer ≥1 | ◎ | フレーム（fps 既定 30） | `120`（=4s） |
| `emotion` | string | ◎ | 自由文字列（演出感情） | `"unease"` |
| `informationGoal` | string | ◎ | このショットで視聴者に伝える 1 事項 | `"Establish the central question"` |
| `visualStrategy` | string | ◎ | 映像方針（既存 `visual_mode` と整合する自由文 or キーワード） | `"abstract macro + telop"` |
| `assetNeeds` | object[] | ◎ | 下記 **assetNeed** | 棚から必要な素材の要件（カテゴリ/mood 等） |
| `selectedAssets` | string[] | ◎ | `^AF-[A-Z_]+-[0-9]{4}$`（最低 0、確定後 ≥1） | `["AF-BACKGROUNDS-0007"]` |
| `motionRecipe` | string[](enum) | ◎ | **30 motion grammar**（最低 1、順序=適用順） | `["slow_push_in","keyword_punch"]` |
| `sfx` | string[] | ◎ | `^AF-SFX-[0-9]{4}$` or 空配列 | `["AF-SFX-0042"]` |
| `transitionIn` | string(enum) | ◎ | 下記 **transition 値域** | `"soft_reveal"` |
| `transitionOut` | string(enum) | ◎ | 同上 | `"hard_cut"` |
| `qualityTarget` | object | ◎ | 下記 **qualityTarget** | レンダ品質目標 |
| `renderNotes` | string | ◎ | 自由文字列（空可） | `"Keep telop clear of lower third"` |

### 3.1 `assetNeeds[]`（assetNeed オブジェクト）

棚（Asset Manifest）に対する要件。`selectedAssets` 確定前の検索条件。

| サブフィールド | 型 | 必須 | 値域 | 例 |
|---|---|:--:|---|---|
| `category` | string(enum) | ◎ | 14 カテゴリ（Asset Manifest `type` と同一） | `"backgrounds"` |
| `mood` | string | ○ | Asset Manifest `mood` 値域 | `"tense"` |
| `intensity` | string | ○ | `subtle\|moderate\|strong\|extreme` | `"moderate"` |
| `colorTone` | string | ○ | Asset Manifest `colorTone` 値域 | `"cool_blue"` |
| `hasAlpha` | boolean | ○ | 透過要件 | `true` |
| `count` | integer ≥1 | ○ | 必要枚数 | `1` |
| `note` | string | ○ | 補足 | `"loopable underlay"` |

### 3.2 `motionRecipe` — 30 motion grammar enum（CANON）

```
slow_push_in, fast_push_in, pull_out, subtle_shake, impact_zoom,
parallax_depth, keyword_punch, quote_typewriter, number_countup,
evidence_reveal, timeline_flow, map_focus, card_stack, light_sweep,
particle_drift, data_reveal, hard_cut, flash_transition, whip_transition,
glitch_transition, silent_hold, cinematic_drift, foreground_blur_pass,
panel_float, depth_dolly, ambient_overlay, diagram_draw,
relationship_connect, title_slam, soft_reveal
```

### 3.3 `transitionIn`/`transitionOut` 値域

motion grammar のうち遷移系を採用 + `none`:
```
none, hard_cut, flash_transition, whip_transition, glitch_transition,
soft_reveal, light_sweep, foreground_blur_pass
```

### 3.4 `qualityTarget` オブジェクト

| サブフィールド | 型 | 必須 | 値域 | 例 |
|---|---|:--:|---|---|
| `tier` | string(enum) | ◎ | `draft\|review\|final` | `"final"` |
| `resolution` | string(enum) | ◎ | `720p\|1080p\|1440p\|4k` | `"1080p"` |
| `minQcScore` | number 0–100 | ○ | `asset.schema.json qc.score` と整合 | `80` |
| `noRealPersonLikeness` | boolean | ◎ | invariant 11 遵守フラグ | `true` |

### 3.5 `sceneType` enum（CANON 20）

```
opening_hook, chapter_title, explanation, character_profile, company_profile,
place_intro, timeline, evidence_board, comparison, data_reveal, quote,
turning_point, reenactment, emotional_pause, summary, ending,
transition_bridge, abstract_emotion, problem_statement, solution_reveal
```

---

## 4. Scene Plan v2 の構造と JSON Schema ドラフト

Scene Plan = 既存 v1 の集合に、各 scene の `sceneType` と `shotRecipes[]`（ShotRecipe の集合）を追加したもの。トップレベル（`episode_id`/`revision`/`scenes`/`coverage`）は v1 から不変。

> 実ファイルは Codex Phase。新 `schema_version:"2.0.0"`。v1 で既に存在するフィールドは省略表記せず全て保持する（下記は v1 から**増えた差分を中心に**全体を記述）。

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://prime-documentary.local/schemas/scene-plan.schema.json",
  "title": "PD Scene Plan (v2: ShotRecipe extension)",
  "type": "object",
  "additionalProperties": false,
  "required": ["schema_version", "episode_id", "revision", "scenes", "coverage"],
  "properties": {
    "schema_version": { "const": "2.0.0" },
    "episode_id": { "type": "string", "pattern": "^PD-[0-9]{4}-[0-9]{3}-[a-z0-9-]+$" },
    "revision": { "type": "string", "pattern": "^v[0-9]{3}$" },
    "scenes": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": [
          "scene_id", "script_span_ids", "purpose", "visual_mode",
          "duration_seconds", "priority", "required_assets", "human_review_required"
        ],
        "properties": {
          "scene_id": { "type": "string", "pattern": "^S[0-9]{3}$" },
          "script_span_ids": {
            "type": "array", "minItems": 1,
            "items": { "type": "string", "pattern": "^SPN-[0-9]{4}$" }
          },
          "purpose": { "type": "string" },
          "primary_claim_id": { "type": ["string", "null"], "pattern": "^CLM-[0-9]{4}$" },
          "emotional_function": { "type": "string" },
          "visual_mode": {
            "enum": ["reenactment", "location", "object", "archival_illustration",
                     "map", "timeline", "diagram", "data_visualization", "abstract",
                     "typography", "breathing", "transition_texture"]
          },
          "sceneType": {
            "enum": ["opening_hook", "chapter_title", "explanation", "character_profile",
                     "company_profile", "place_intro", "timeline", "evidence_board",
                     "comparison", "data_reveal", "quote", "turning_point", "reenactment",
                     "emotional_pause", "summary", "ending", "transition_bridge",
                     "abstract_emotion", "problem_statement", "solution_reveal"]
          },
          "duration_seconds": { "type": "number", "minimum": 0.5 },
          "priority": { "enum": ["A", "B", "C"] },
          "required_assets": { "type": "array", "items": { "type": "string" } },
          "continuity_refs": { "type": "array", "items": { "type": "string" } },
          "transition_in": { "type": "string" },
          "transition_out": { "type": "string" },
          "on_screen_text": { "type": "array", "items": { "type": "string" } },
          "source_sensitivity": { "enum": ["low", "medium", "high"] },
          "human_review_required": { "type": "boolean" },
          "fallback_visual": { "type": "string" },
          "shotRecipes": {
            "type": "array",
            "items": { "$ref": "#/$defs/shotRecipe" }
          }
        }
      }
    },
    "coverage": {
      "type": "object",
      "required": ["all_script_spans_mapped", "orphan_scenes"],
      "properties": {
        "all_script_spans_mapped": { "type": "boolean" },
        "orphan_scenes": { "type": "array", "items": { "type": "string" } }
      }
    }
  },
  "$defs": {
    "shotRecipe": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "sceneId", "sceneType", "durationFrames", "emotion", "informationGoal",
        "visualStrategy", "assetNeeds", "selectedAssets", "motionRecipe", "sfx",
        "transitionIn", "transitionOut", "qualityTarget", "renderNotes"
      ],
      "properties": {
        "sceneId": { "type": "string", "pattern": "^S[0-9]{3}$" },
        "shotId": { "type": "string", "pattern": "^S[0-9]{3}-SH[0-9]{3}$" },
        "sceneType": { "$ref": "#/properties/scenes/items/properties/sceneType" },
        "durationFrames": { "type": "integer", "minimum": 1 },
        "emotion": { "type": "string" },
        "informationGoal": { "type": "string" },
        "visualStrategy": { "type": "string" },
        "assetNeeds": {
          "type": "array",
          "items": {
            "type": "object",
            "additionalProperties": false,
            "required": ["category"],
            "properties": {
              "category": {
                "enum": ["backgrounds", "parallax_layers", "vfx_overlays", "loops",
                         "transitions", "typography_assets", "diagram_assets", "sfx",
                         "ai_video_shots", "lottie_assets", "ui_motion_assets",
                         "texture_assets", "light_assets", "particle_assets"]
              },
              "mood": { "type": "string" },
              "intensity": { "enum": ["subtle", "moderate", "strong", "extreme"] },
              "colorTone": { "type": "string" },
              "hasAlpha": { "type": "boolean" },
              "count": { "type": "integer", "minimum": 1 },
              "note": { "type": "string" }
            }
          }
        },
        "selectedAssets": {
          "type": "array",
          "items": { "type": "string", "pattern": "^AF-[A-Z_]+-[0-9]{4}$" }
        },
        "motionRecipe": {
          "type": "array",
          "minItems": 1,
          "items": {
            "enum": ["slow_push_in", "fast_push_in", "pull_out", "subtle_shake",
                     "impact_zoom", "parallax_depth", "keyword_punch", "quote_typewriter",
                     "number_countup", "evidence_reveal", "timeline_flow", "map_focus",
                     "card_stack", "light_sweep", "particle_drift", "data_reveal",
                     "hard_cut", "flash_transition", "whip_transition", "glitch_transition",
                     "silent_hold", "cinematic_drift", "foreground_blur_pass", "panel_float",
                     "depth_dolly", "ambient_overlay", "diagram_draw", "relationship_connect",
                     "title_slam", "soft_reveal"]
          }
        },
        "sfx": {
          "type": "array",
          "items": { "type": "string", "pattern": "^AF-SFX-[0-9]{4}$" }
        },
        "transitionIn": {
          "enum": ["none", "hard_cut", "flash_transition", "whip_transition",
                   "glitch_transition", "soft_reveal", "light_sweep", "foreground_blur_pass"]
        },
        "transitionOut": {
          "enum": ["none", "hard_cut", "flash_transition", "whip_transition",
                   "glitch_transition", "soft_reveal", "light_sweep", "foreground_blur_pass"]
        },
        "qualityTarget": {
          "type": "object",
          "additionalProperties": false,
          "required": ["tier", "resolution", "noRealPersonLikeness"],
          "properties": {
            "tier": { "enum": ["draft", "review", "final"] },
            "resolution": { "enum": ["720p", "1080p", "1440p", "4k"] },
            "minQcScore": { "type": "number", "minimum": 0, "maximum": 100 },
            "noRealPersonLikeness": { "type": "boolean" }
          }
        },
        "renderNotes": { "type": "string" }
      }
    }
  }
}
```

---

## 5. Scene Plan の完全な例 JSON（opening_hook / explanation / timeline / data_reveal）

```json
{
  "schema_version": "2.0.0",
  "episode_id": "PD-2026-009-timbs",
  "revision": "v002",
  "scenes": [
    {
      "scene_id": "S001",
      "script_span_ids": ["SPN-0001"],
      "purpose": "Open with the central question that hooks the viewer.",
      "primary_claim_id": null,
      "emotional_function": "unease",
      "visual_mode": "abstract",
      "sceneType": "opening_hook",
      "duration_seconds": 6.0,
      "priority": "A",
      "required_assets": ["AF-BACKGROUNDS-0007"],
      "transition_in": "soft_reveal",
      "transition_out": "hard_cut",
      "on_screen_text": ["How far can the state reach?"],
      "human_review_required": true,
      "shotRecipes": [
        {
          "sceneId": "S001",
          "shotId": "S001-SH001",
          "sceneType": "opening_hook",
          "durationFrames": 180,
          "emotion": "unease",
          "informationGoal": "Pose the central constitutional question.",
          "visualStrategy": "Abstract cool-blue grid under a single punchy telop line.",
          "assetNeeds": [
            { "category": "backgrounds", "mood": "tense", "colorTone": "cool_blue", "hasAlpha": false, "count": 1, "note": "loopable underlay" }
          ],
          "selectedAssets": ["AF-BACKGROUNDS-0007"],
          "motionRecipe": ["slow_push_in", "keyword_punch"],
          "sfx": ["AF-SFX-0042"],
          "transitionIn": "soft_reveal",
          "transitionOut": "hard_cut",
          "qualityTarget": { "tier": "final", "resolution": "1080p", "minQcScore": 80, "noRealPersonLikeness": true },
          "renderNotes": "Keep telop clear of the lower third for captions."
        }
      ]
    },
    {
      "scene_id": "S002",
      "script_span_ids": ["SPN-0002", "SPN-0003"],
      "purpose": "Explain the legal mechanism behind civil forfeiture.",
      "primary_claim_id": "CLM-0004",
      "emotional_function": "clarity",
      "visual_mode": "diagram",
      "sceneType": "explanation",
      "duration_seconds": 12.0,
      "priority": "A",
      "required_assets": ["AF-DIAGRAM_ASSETS-0011", "AF-BACKGROUNDS-0007"],
      "transition_in": "hard_cut",
      "transition_out": "soft_reveal",
      "on_screen_text": ["Civil forfeiture", "Property, not person"],
      "human_review_required": false,
      "shotRecipes": [
        {
          "sceneId": "S002",
          "shotId": "S002-SH001",
          "sceneType": "explanation",
          "durationFrames": 360,
          "emotion": "clarity",
          "informationGoal": "Show that the suit targets the property, not the owner.",
          "visualStrategy": "Animated diagram drawing the property-vs-person split.",
          "assetNeeds": [
            { "category": "diagram_assets", "mood": "clinical", "intensity": "moderate", "count": 1 },
            { "category": "backgrounds", "colorTone": "cool_blue", "count": 1 }
          ],
          "selectedAssets": ["AF-DIAGRAM_ASSETS-0011", "AF-BACKGROUNDS-0007"],
          "motionRecipe": ["diagram_draw", "relationship_connect", "cinematic_drift"],
          "sfx": [],
          "transitionIn": "hard_cut",
          "transitionOut": "soft_reveal",
          "qualityTarget": { "tier": "final", "resolution": "1080p", "minQcScore": 78, "noRealPersonLikeness": true },
          "renderNotes": "Diagram strokes draw in sync with narration beats."
        }
      ]
    },
    {
      "scene_id": "S003",
      "script_span_ids": ["SPN-0004"],
      "purpose": "Lay out the case chronology.",
      "primary_claim_id": "CLM-0007",
      "emotional_function": "momentum",
      "visual_mode": "timeline",
      "sceneType": "timeline",
      "duration_seconds": 9.0,
      "priority": "B",
      "required_assets": ["AF-LOTTIE_ASSETS-0003"],
      "transition_in": "soft_reveal",
      "transition_out": "whip_transition",
      "on_screen_text": ["2013", "2015", "2019"],
      "human_review_required": false,
      "shotRecipes": [
        {
          "sceneId": "S003",
          "shotId": "S003-SH001",
          "sceneType": "timeline",
          "durationFrames": 270,
          "emotion": "momentum",
          "informationGoal": "Walk the viewer from arrest to the Supreme Court ruling.",
          "visualStrategy": "Horizontal timeline flow with year nodes counting up.",
          "assetNeeds": [
            { "category": "lottie_assets", "mood": "neutral", "count": 1, "note": "timeline + countup" }
          ],
          "selectedAssets": ["AF-LOTTIE_ASSETS-0003"],
          "motionRecipe": ["timeline_flow", "number_countup", "panel_float"],
          "sfx": ["AF-SFX-0042"],
          "transitionIn": "soft_reveal",
          "transitionOut": "whip_transition",
          "qualityTarget": { "tier": "final", "resolution": "1080p", "noRealPersonLikeness": true },
          "renderNotes": "Year nodes land on each narration emphasis."
        }
      ]
    },
    {
      "scene_id": "S004",
      "script_span_ids": ["SPN-0005"],
      "purpose": "Reveal the headline statistic of the ruling's impact.",
      "primary_claim_id": "CLM-0009",
      "emotional_function": "weight",
      "visual_mode": "data_visualization",
      "sceneType": "data_reveal",
      "duration_seconds": 7.0,
      "priority": "A",
      "required_assets": ["AF-LOTTIE_ASSETS-0003", "AF-BACKGROUNDS-0007"],
      "transition_in": "whip_transition",
      "transition_out": "hard_cut",
      "on_screen_text": ["$42,000", "seized"],
      "human_review_required": false,
      "shotRecipes": [
        {
          "sceneId": "S004",
          "shotId": "S004-SH001",
          "sceneType": "data_reveal",
          "durationFrames": 210,
          "emotion": "weight",
          "informationGoal": "Anchor the human cost with one number.",
          "visualStrategy": "Number count-up over a tense data-grid background.",
          "assetNeeds": [
            { "category": "lottie_assets", "count": 1, "note": "number_countup" },
            { "category": "backgrounds", "mood": "tense", "colorTone": "cool_blue", "count": 1 }
          ],
          "selectedAssets": ["AF-LOTTIE_ASSETS-0003", "AF-BACKGROUNDS-0007"],
          "motionRecipe": ["data_reveal", "number_countup", "impact_zoom"],
          "sfx": ["AF-SFX-0042"],
          "transitionIn": "whip_transition",
          "transitionOut": "hard_cut",
          "qualityTarget": { "tier": "final", "resolution": "1080p", "minQcScore": 82, "noRealPersonLikeness": true },
          "renderNotes": "Number settles 6 frames before the cut for impact."
        }
      ]
    }
  ],
  "coverage": {
    "all_script_spans_mapped": true,
    "orphan_scenes": []
  }
}
```

---

## 6. Scene Plan → 既存 RoughShot / RoughCutData 写像表

`import_to_remotion.py` 相当（または後継の ShotRecipe-aware importer）が、Scene Plan v2 の各 ShotRecipe を Remotion の `RoughShot` 1 件へ落とす際の変換規則。`RoughShot.assetType`/`motion` は 5 値しかないため、30 motion grammar と 14 カテゴリは下表で縮約する。

### 6.1 ShotRecipe → RoughShot（フィールド対応）

| RoughShot フィールド | 由来（ShotRecipe / 上位 scene） | 変換規則 |
|---|---|---|
| `spanId` | scene `script_span_ids[0]`（または ShotRecipe ごとに割当） | そのまま。`shotId` がある場合は span 単位で分割。 |
| `chapterId` | scene 由来（既存 shotlist `chapter_id` 相当） | scene のチャプタ属性を継承。opening は `"opening"`。 |
| `seconds` | `durationFrames` ÷ fps(30) | `seconds = durationFrames / 30`。 |
| `assetType` | `selectedAssets[0]` の Asset Manifest `type` / `mediaKind` | §6.2 の縮約表で 5 値へ。 |
| `motion` | `motionRecipe`（先頭の支配的グラマー） | §6.3 の縮約表で 5 値へ。 |
| `src` | `selectedAssets[0]` → Asset Manifest `path` → public へコピー後の相対 | 棚 ID を解決し usable のみ取り込み（rights ゲート）。未確定なら `null`（branded card）。 |
| `clips` | `selectedAssets` のうち動画系（複数） | 動画素材が複数なら cut 用に列挙（`probe_seconds` で `clipSeconds`）。 |
| `images` | `selectedAssets` のうち画像系（複数） | 画像が複数なら Ken-Burns cut 用に列挙。 |
| `telop` | scene `on_screen_text`（または ShotRecipe 派生） | そのまま配列で。 |
| `priority` | scene `priority`（A/B/C） | そのまま。 |
| `captions`(RoughCutData) | 別工程（narration align） | ShotRecipe 外。 |
| `narrationSrc`/`bgmSrc`(RoughCutData) | 別工程（audio） | ShotRecipe 外。`sfx`(AF-SFX) は将来 SFX トラックへ。 |

### 6.2 `selectedAssets` カテゴリ → `RoughShot.assetType`（5 値縮約）

| Asset Manifest `type` / mediaKind | RoughShot `assetType` |
|---|---|
| `ai_video_shots`（video） | `ai_image`（生成由来の動く素材）/ 取り込み実体が動画なら `stock_video` 相当に扱う |
| `backgrounds`/`loops`/`light_assets`/`particle_assets`（video, 実写でない） | `motion_graphic` |
| 実写ストック動画（Manifest 由来でない外部 stock） | `stock_video` |
| 実写ストック画像 | `stock_image` |
| `diagram_assets`/`typography_assets`/`lottie_assets`/`ui_motion_assets`/`vfx_overlays`/`transitions`/`texture_assets`/`parallax_layers` | `motion_graphic` |
| アーカイブ（PD 自社・権利確認済） | `archival_pd` |

※ 厳密には Manifest `mediaKind`(image/video/lottie) と `type` の組合せで決まる。生成系映像は `ai_image`、グラフィック系は `motion_graphic`、実写は `stock_*`。

### 6.3 `motionRecipe` → `RoughShot.motion`（5 値縮約）

| RoughShot `motion` | 縮約元の motion grammar（代表） |
|---|---|
| `video_native` | 素材が動画実体のとき（`cinematic_drift`,`ambient_overlay`,`particle_drift`,`light_sweep`,`depth_dolly` 等を内包する動く素材） |
| `ken_burns` | `slow_push_in`, `fast_push_in`, `pull_out`, `impact_zoom` |
| `parallax` | `parallax_depth`, `foreground_blur_pass`, `panel_float` |
| `graphic_anim` | `diagram_draw`, `relationship_connect`, `number_countup`, `data_reveal`, `evidence_reveal`, `timeline_flow`, `map_focus`, `card_stack`, `keyword_punch`, `quote_typewriter`, `title_slam` |
| `static` | `silent_hold` のみ（原則使わない。画像は常に動かす方針＝ shotlist の注記と整合） |

- 遷移系（`hard_cut`,`flash_transition`,`whip_transition`,`glitch_transition`,`soft_reveal`）は `motion` ではなく `transitionIn/Out` 由来。Series の境界演出として扱う。
- 縮約は「先頭の支配的グラマー＋素材実体の種別」で決定し、残りの motion grammar は `renderNotes` 経由で Codex 仕上げ工程へ申し送る（情報を失わない）。

### 6.4 不変条件の保全

- `qualityTarget.noRealPersonLikeness=true` は invariant 11 と一致。importer は実在人物を含む素材を選ばない。
- rights 未確定の `selectedAssets` は取り込まず `src=null`（branded card）。既存 importer の「usable のみコピー」挙動を維持。
- ShotRecipe を持たない v1 scene は、従来どおり shotlist 由来で RoughShot 化される（後方互換）。
