# Asset Manifest スキーマ設計書（素材棚レジストリ）

- **ステータス: 設計（未実装）** — 本書は仕様であり、実 JSON Schema ファイルおよびレジストリ実体の作成は Codex Phase に委ねる。本書内のコードブロックはそのまま使える完全なドラフトとして提示する。
- **対象**: 再利用可能な「素材棚（Asset Factory）」のレジストリ 1 件 1 件を表す **Asset Manifest** スキーマ。
- **新規 schema は別物ではなく拡張**: 既存 `schemas/asset.schema.json`（エピソード単位の生成物 1 個を表す）とは別レイヤだが、ID 体系・enum・provenance/rights/qc の語彙は既存と矛盾しないよう揃える（CLAUDE.md invariant 14）。

---

## 1. 前提・仮定

1. **2 つの ID 体系を衝突させない**（CANON 厳守）。
   - **Asset Factory 棚素材**: `AF-<CATEGORY>-NNNN`（例 `AF-BACKGROUNDS-0007`）。エピソードに依存しない、再利用前提の汎用素材。本書が定義する Asset Manifest の `id` はこれ。
   - **エピソード生成物**: `PD-YYYY-NNN-S001-IMG-001`（CLAUDE.md §8）。エピソード固有。既存 `schemas/asset.schema.json` の `asset_id` がこれを指す。
   - 両者はプレフィックス（`AF-` / `PD-`）で完全に分離され、衝突しない。
2. Asset Manifest は「棚レジストリ」であり、**承認成果物ではない**。`schemas/asset.schema.json` の `status`（raw/candidate/approved/…）のようなエピソード進行ステートは持たず、棚としての可用性に絞る。
3. 価格・APIキー・トークン等の秘密情報はレジストリに一切含めない（CLAUDE.md invariant 3）。`sourcePrompt`/`negativePrompt`/`seed` は再現用メタデータであり、秘密ではない。
4. パスは論理 URI を優先（`.claude/rules/14-cross-platform-paths.md`）。Windows 絶対パスを真実にしない。`previewPath` を含むパスは `artifact://` か repo 相対、または `<media>/...` 相対で格納する。
5. `durationFrames`/`fps`/`width`/`height` は最終的に Remotion の `RoughShot`/`RoughCutData`（`fps`, `seconds`, `durationInFrames`）へ落ちることを意識した数値。

## 2. 参照した既存 schema

| ファイル | 参照したフィールド・語彙 | 本書での扱い |
|---|---|---|
| `schemas/asset.schema.json` | `provenance{created_by,provider,provider_request_id,model_profile,prompt_ref,seed,input_hash}`, `rights{status,origin,commercial_use,evidence_ref,notes}`, `qc{status,score,findings}`, `asset_type` enum | provenance/rights の語彙を継承。manifest は薄い provenance（`sourceTool`,`sourcePrompt`,`negativePrompt`,`seed`）+ `license` に圧縮。`asset_type`(image/video/...) は本書の 14 カテゴリ `type` とは別軸なので `mediaKind` に対応付け。 |
| `schemas/shotlist.schema.json` | `motion` enum(`video_native\|ken_burns\|parallax\|graphic_anim\|static`), `suggested_asset_type` enum | `compatibleSceneTypes` 連携の参考。manifest の `loopable`/`hasAlpha` が motion 適性を補助。 |
| `schemas/scene-plan.schema.json` | `visual_mode` enum（reenactment/location/diagram/...）, `scene_id` `^S[0-9]{3}$` | `compatibleSceneTypes` は CANON の 20 sceneType を採用（visual_mode より粒度が細かい上位語彙）。 |
| `schemas/common.schema.json` | `$defs.timestamp`(date-time), `$defs.revision`(`^v[0-9]{3}$`), `rights_status`/`qc_status` enum | `createdAt` は `timestamp`、ライセンス/権利語彙を整合。 |
| `remotion/src/compositions/RoughCut.tsx` | `RoughShot.assetType`/`motion`、`fps`, `seconds` | 棚素材が最終的にどの `assetType`/`motion` に落ちうるかの整合確認に使用。 |

---

## 3. レジストリの場所と構造

- **レジストリ実体（提案）**: `assets/asset_manifest.v001.json`
  - revision は `v001`,`v002`,…（CLAUDE.md §8、`common.schema.json $defs.revision`）。承認境界が変わる破壊的変更では新 revision を作る（`.claude/rules/12`, `02`）。
- **素材ファイル本体**: SSD メディア配下（例 `<media>/assets/<category>/...`）。レジストリには論理 URI を格納し、Windows 絶対パスは入れない。
- レジストリは「カテゴリ別の棚」であり、トップレベルは `schema_version` + `entries[]`（Asset Manifest の配列）とする。

```jsonc
{
  "schema_version": "1.0.0",
  "generated_at": "2026-06-21T00:00:00Z",
  "entries": [ /* Asset Manifest オブジェクトの配列（下記スキーマ） */ ]
}
```

---

## 4. フィールド仕様（Asset Manifest 1 エントリ）

凡例: ◎=必須 / ○=任意。

| フィールド | 型 | 必須 | 値域 / enum | 説明・例 |
|---|---|:--:|---|---|
| `id` | string | ◎ | `^AF-[A-Z_]+-[0-9]{4}$` | Asset Factory ID。例 `AF-BACKGROUNDS-0007`。`PD-...` とは別系統。 |
| `type` | string(enum) | ◎ | 下記 **14 カテゴリ** | 素材棚のカテゴリ。例 `backgrounds`。 |
| `subtype` | string | ◎ | 自由文字列（カテゴリ内の細分） | 例 `abstract_data_grid`, `paper_tear`, `whoosh_low`。 |
| `path` | string(uri) | ◎ | 論理 URI（`artifact://` / repo 相対 / `<media>` 相対） | 素材本体。例 `artifact://assets/backgrounds/AF-BACKGROUNDS-0007.mp4`。 |
| `previewPath` | string(uri) | ◎ | 同上 | サムネ/プレビュー。例 `artifact://assets/backgrounds/AF-BACKGROUNDS-0007.preview.jpg`。 |
| `sourceTool` | string(enum) | ◎ | `midjourney\|runway\|elevenlabs\|suno\|lottie\|local\|sdxl\|codex` | 生成元ツール。`asset.schema.json` の `provenance.provider` 相当を棚向けに固定 enum 化。 |
| `durationFrames` | integer ≥0 | ◎ | 0 = 静止画 | 動画/ループ/SFX の尺（フレーム）。静止画は `0`。Remotion `seconds×fps` と整合。 |
| `fps` | number | ◎ | >0（静止画は 30 を既定で格納） | フレームレート。Remotion 既定 30。 |
| `width` | integer ≥1 | ◎ | px | 例 `1920`。SFX 等の非映像は `0` 可。 |
| `height` | integer ≥1 | ◎ | px | 例 `1080`。 |
| `hasAlpha` | boolean | ◎ | true/false | 透過の有無（overlay/vfx/particle に重要）。 |
| `loopable` | boolean | ◎ | true/false | シームレスループ可否（loops/ambient に重要）。 |
| `mood` | string(enum) | ◎ | 下記 **mood 値域** | 例 `tense`。 |
| `intensity` | string(enum) | ◎ | `subtle\|moderate\|strong\|extreme` | 演出強度。 |
| `useCases` | string[] | ◎ | 自由文字列（最低 1） | 例 `["evidence_board","data_reveal underlay"]`。 |
| `compatibleSceneTypes` | string[](enum) | ◎ | **20 sceneType** のいずれか（最低 1） | 例 `["data_reveal","evidence_board"]`。 |
| `colorTone` | string(enum) | ◎ | 下記 **colorTone 値域** | 例 `cool_blue`。 |
| `tags` | string[] | ◎ | 自由文字列 | 検索用。例 `["grid","cyan","slow"]`。 |
| `sourcePrompt` | string \| null | ◎ | 再現用 | 生成プロンプト（秘密でない）。非生成素材は `null`。 |
| `negativePrompt` | string \| null | ◎ | 再現用 | ネガティブプロンプト。無ければ `null`。 |
| `seed` | integer \| null | ◎ | 再現用 | 生成シード。`asset.schema.json provenance.seed` 同義。無ければ `null`。 |
| `license` | string(enum) | ◎ | 下記 **license 値域** | 権利区分。`asset.schema.json rights` と整合。 |
| `createdAt` | string(date-time) | ◎ | `common.schema.json $defs.timestamp` | 例 `2026-06-21T00:00:00Z`。 |
| `notes` | string | ◎ | 自由文字列（空文字可） | 補足。 |
| `mediaKind` | string(enum) | ○ | `image\|video\|audio\|lottie\|other` | 既存 `asset.schema.json asset_type` への橋渡し。任意（`type` から導出可）。 |
| `checksum` | string \| null | ○ | `sha256:...` 推奨 | 完全性確認（`.claude/rules/14`）。 |
| `last_verified_at` | string(date-time) \| null | ○ | timestamp | 棚の可用性最終確認（provider 能力の時効対策, CLAUDE.md §11）。 |

### 4.1 `type` — 14 カテゴリ enum（CANON）

```
backgrounds, parallax_layers, vfx_overlays, loops, transitions,
typography_assets, diagram_assets, sfx, ai_video_shots, lottie_assets,
ui_motion_assets, texture_assets, light_assets, particle_assets
```

### 4.2 `sourceTool` enum

```
midjourney, runway, elevenlabs, suno, lottie, local, sdxl, codex
```

### 4.3 値域定義

- **`license`**: `cc0`, `royalty_free`, `generated_owned`, `licensed`, `editorial_only`, `unknown`
  （`generated_owned` = Codex/SDXL/Suno 生成で自社帰属。`asset.schema.json rights.commercial_use` と対応: cc0/royalty_free/generated_owned → allowed、licensed/editorial_only → restricted、unknown → unknown）。
- **`colorTone`**: `neutral`, `warm`, `cool_blue`, `cool_teal`, `monochrome`, `high_contrast`, `desaturated`, `vibrant`, `dark`, `bright`
- **`mood`**: `neutral`, `tense`, `somber`, `hopeful`, `triumphant`, `mysterious`, `urgent`, `calm`, `clinical`, `nostalgic`
- **`intensity`**: `subtle`, `moderate`, `strong`, `extreme`

### 4.4 `compatibleSceneTypes` — 20 sceneType enum（CANON）

```
opening_hook, chapter_title, explanation, character_profile, company_profile,
place_intro, timeline, evidence_board, comparison, data_reveal, quote,
turning_point, reenactment, emotional_pause, summary, ending,
transition_bridge, abstract_emotion, problem_statement, solution_reveal
```

---

## 5. JSON Schema ドラフト（提案 `schemas/asset-manifest.schema.json`）

> 本ドラフトは完成形。実ファイル作成は Codex Phase。`common.schema.json` の `$defs.timestamp`/`$defs.revision` を `$ref` 参照する想定（ローカル `$id` 解決）。

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://prime-documentary.local/schemas/asset-manifest.schema.json",
  "title": "PD Asset Manifest (Asset Factory shelf registry)",
  "description": "Reusable, episode-independent asset shelf. Distinct from schemas/asset.schema.json (per-episode generated artifacts). Extension layer; never a second implementation of asset.schema.json.",
  "type": "object",
  "additionalProperties": false,
  "required": ["schema_version", "entries"],
  "properties": {
    "schema_version": { "const": "1.0.0" },
    "generated_at": { "type": "string", "format": "date-time" },
    "entries": {
      "type": "array",
      "items": { "$ref": "#/$defs/assetManifest" }
    }
  },
  "$defs": {
    "assetManifest": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "id", "type", "subtype", "path", "previewPath", "sourceTool",
        "durationFrames", "fps", "width", "height", "hasAlpha", "loopable",
        "mood", "intensity", "useCases", "compatibleSceneTypes", "colorTone",
        "tags", "sourcePrompt", "negativePrompt", "seed", "license",
        "createdAt", "notes"
      ],
      "properties": {
        "id": { "type": "string", "pattern": "^AF-[A-Z_]+-[0-9]{4}$" },
        "type": {
          "enum": [
            "backgrounds", "parallax_layers", "vfx_overlays", "loops",
            "transitions", "typography_assets", "diagram_assets", "sfx",
            "ai_video_shots", "lottie_assets", "ui_motion_assets",
            "texture_assets", "light_assets", "particle_assets"
          ]
        },
        "subtype": { "type": "string", "minLength": 1 },
        "path": { "type": "string", "minLength": 1 },
        "previewPath": { "type": "string", "minLength": 1 },
        "sourceTool": {
          "enum": ["midjourney", "runway", "elevenlabs", "suno", "lottie", "local", "sdxl", "codex"]
        },
        "mediaKind": { "enum": ["image", "video", "audio", "lottie", "other"] },
        "durationFrames": { "type": "integer", "minimum": 0 },
        "fps": { "type": "number", "exclusiveMinimum": 0 },
        "width": { "type": "integer", "minimum": 0 },
        "height": { "type": "integer", "minimum": 0 },
        "hasAlpha": { "type": "boolean" },
        "loopable": { "type": "boolean" },
        "mood": {
          "enum": ["neutral", "tense", "somber", "hopeful", "triumphant",
                   "mysterious", "urgent", "calm", "clinical", "nostalgic"]
        },
        "intensity": { "enum": ["subtle", "moderate", "strong", "extreme"] },
        "useCases": { "type": "array", "items": { "type": "string" }, "minItems": 1 },
        "compatibleSceneTypes": {
          "type": "array",
          "minItems": 1,
          "items": {
            "enum": [
              "opening_hook", "chapter_title", "explanation", "character_profile",
              "company_profile", "place_intro", "timeline", "evidence_board",
              "comparison", "data_reveal", "quote", "turning_point", "reenactment",
              "emotional_pause", "summary", "ending", "transition_bridge",
              "abstract_emotion", "problem_statement", "solution_reveal"
            ]
          }
        },
        "colorTone": {
          "enum": ["neutral", "warm", "cool_blue", "cool_teal", "monochrome",
                   "high_contrast", "desaturated", "vibrant", "dark", "bright"]
        },
        "tags": { "type": "array", "items": { "type": "string" } },
        "sourcePrompt": { "type": ["string", "null"] },
        "negativePrompt": { "type": ["string", "null"] },
        "seed": { "type": ["integer", "null"] },
        "license": {
          "enum": ["cc0", "royalty_free", "generated_owned", "licensed", "editorial_only", "unknown"]
        },
        "createdAt": { "type": "string", "format": "date-time" },
        "notes": { "type": "string" },
        "checksum": { "type": ["string", "null"] },
        "last_verified_at": { "type": ["string", "null"], "format": "date-time" }
      }
    }
  }
}
```

---

## 6. 完全な例エントリ（backgrounds / sfx / lottie 各 1）

```json
{
  "id": "AF-BACKGROUNDS-0007",
  "type": "backgrounds",
  "subtype": "abstract_data_grid",
  "path": "artifact://assets/backgrounds/AF-BACKGROUNDS-0007.mp4",
  "previewPath": "artifact://assets/backgrounds/AF-BACKGROUNDS-0007.preview.jpg",
  "sourceTool": "sdxl",
  "mediaKind": "video",
  "durationFrames": 300,
  "fps": 30,
  "width": 1920,
  "height": 1080,
  "hasAlpha": false,
  "loopable": true,
  "mood": "tense",
  "intensity": "moderate",
  "useCases": ["data_reveal underlay", "evidence_board backdrop"],
  "compatibleSceneTypes": ["data_reveal", "evidence_board", "problem_statement"],
  "colorTone": "cool_blue",
  "tags": ["grid", "cyan", "slow", "tech"],
  "sourcePrompt": "abstract dark blue data grid, slow drifting nodes, cinematic depth, subtle parallax, 16:9",
  "negativePrompt": "text, logo, watermark, people, faces",
  "seed": 884213,
  "license": "generated_owned",
  "createdAt": "2026-06-21T00:00:00Z",
  "notes": "Loops seamlessly; safe under telop. No real-person likeness (invariant 11).",
  "checksum": "sha256:0000000000000000000000000000000000000000000000000000000000000000",
  "last_verified_at": "2026-06-21T00:00:00Z"
}
```

```json
{
  "id": "AF-SFX-0042",
  "type": "sfx",
  "subtype": "whoosh_low",
  "path": "artifact://assets/sfx/AF-SFX-0042.wav",
  "previewPath": "artifact://assets/sfx/AF-SFX-0042.preview.mp3",
  "sourceTool": "local",
  "mediaKind": "audio",
  "durationFrames": 18,
  "fps": 30,
  "width": 0,
  "height": 0,
  "hasAlpha": false,
  "loopable": false,
  "mood": "urgent",
  "intensity": "strong",
  "useCases": ["whip_transition accent", "impact_zoom hit"],
  "compatibleSceneTypes": ["turning_point", "transition_bridge", "opening_hook"],
  "colorTone": "neutral",
  "tags": ["whoosh", "transition", "low", "impact"],
  "sourcePrompt": null,
  "negativePrompt": null,
  "seed": null,
  "license": "royalty_free",
  "createdAt": "2026-06-21T00:00:00Z",
  "notes": "0.6s at 30fps. width/height 0 (non-visual). Pair with whip_transition motion.",
  "checksum": "sha256:1111111111111111111111111111111111111111111111111111111111111111",
  "last_verified_at": "2026-06-21T00:00:00Z"
}
```

```json
{
  "id": "AF-LOTTIE_ASSETS-0003",
  "type": "lottie_assets",
  "subtype": "number_countup",
  "path": "artifact://assets/lottie/AF-LOTTIE_ASSETS-0003.json",
  "previewPath": "artifact://assets/lottie/AF-LOTTIE_ASSETS-0003.preview.gif",
  "sourceTool": "lottie",
  "mediaKind": "lottie",
  "durationFrames": 90,
  "fps": 30,
  "width": 1080,
  "height": 1080,
  "hasAlpha": true,
  "loopable": false,
  "mood": "clinical",
  "intensity": "moderate",
  "useCases": ["data_reveal number countup", "comparison metric"],
  "compatibleSceneTypes": ["data_reveal", "comparison", "summary"],
  "colorTone": "high_contrast",
  "tags": ["lottie", "number", "countup", "ui"],
  "sourcePrompt": null,
  "negativePrompt": null,
  "seed": null,
  "license": "generated_owned",
  "createdAt": "2026-06-21T00:00:00Z",
  "notes": "Alpha Lottie; recolorable to brand palette. Drives number_countup motion grammar.",
  "checksum": "sha256:2222222222222222222222222222222222222222222222222222222222222222",
  "last_verified_at": "2026-06-21T00:00:00Z"
}
```

---

## 7. 既存 `schemas/asset.schema.json` との関係（拡張 / 別レイヤ）

- **別レイヤ**: `asset.schema.json` は **エピソード進行の成果物 1 個**（`PD-...` ID、`episode_id`/`scene_id`/`status`/`checksum`/`provenance`/`rights`/`qc`）。Asset Manifest は **エピソード非依存の再利用棚 1 個**（`AF-...` ID）。二重実装ではなく、上流（棚）→ 下流（エピソード採用）の関係。
- **語彙の整合（拡張として尊重）**:
  - `sourceTool`(manifest) ⊂ `provenance.provider`(asset) の固定 enum 版。
  - `license`(manifest) → `rights.status`/`rights.commercial_use`(asset) へ写像可能（§4.3）。
  - `seed`/`sourcePrompt`/`negativePrompt` は `provenance.seed`/`prompt_ref` と同義の再現メタ。
- **採用フロー**: 棚素材（`AF-...`）がエピソードに採用されると、ShotRecipe の `selectedAssets` に `AF-...` ID で参照され、コピー/取り込み時に必要なら `PD-...` のエピソード asset レコード（`asset.schema.json`）が新規発番される。Manifest はその際 `provenance` の入力（origin）になる。
- **invariant 14 遵守**: 既存 `asset.schema.json` を拡張・参照する形でのみ新スキーマを足し、機能を二重化しない。
