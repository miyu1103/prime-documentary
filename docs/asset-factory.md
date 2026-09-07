# Asset Factory（再利用素材ファクトリー）設計書

ステータス: **設計（未実装）**

## 前提・仮定

- 本書は Prime Documentary（PD）の **Asset Factory** の設計書である。実装はまだ無い。
- 最重要思想 = **「先に大量の再利用素材を用意し、カテゴリ整理・manifest管理し、そこから Scene ごとに選ぶ」**。
  1話ごとに素材を作り捨てるのではなく、**棚（factory）に貯めて使い回す**ことを前提にする。
- CANON（ブランド配色・14カテゴリ・20 sceneType・ツール役割・保存場所・命名・manifest最低フィールド）に厳守する。本書内の語彙はすべて CANON と統一する。
- 既存 `schemas/asset.schema.json`（`schema_version: "1.0.0"`）が真実の源。**Asset Manifest はこの schema の拡張**として扱い、別物を新造しない（後述「Manifest 設計」参照）。
- 既存運用ルール `episodes/_planning/VIDEO_RULES.md`（美しさ最優先・静止禁止・30fps・商用利用OKのみ・実在人物の肖像なし・画面文字なし）と矛盾しないこと。
- 既存スクリプト `scripts/import_to_remotion.py`（U4: shotlist + usable_assets から Remotion 取り込み）の選定ロジックと接続できる形にする。
- 保存場所の仮定:
  - 重い素材の実体 = `H:\pd-media\assets\factory\<category>\`（**Git 管理外**）。
  - Remotion 参照 = `remotion/public/assets/<category>\`（**Git 管理外**、H: から同期）。
  - 小さい Lottie JSON のみ `remotion/public/assets/lottie/` に直接置いてよい（軽量・差分が見えるため）。
- 数量・初期目標は別書 `docs/asset-priority-list.md` に集約する。本書は「構造とルール」を定義する。

---

## 1. 全体像

```
                作る（生成ツール）                  貯める（棚）                参照する             選ぶ
 Midjourney / Runway / ElevenLabs / SUNO  ->  H:\pd-media\assets\factory\  ->  remotion/public  ->  Scene Plan
 / LottieFiles(手動DL)                          + Asset Manifest(JSON)          \assets\<cat>\       が候補から選定
```

- **作る**: CANON のツール役割に従い、分解的に大量生成（背景・人物・前景・光・煙などはパーツ単位）。
- **貯める**: 14カテゴリのフォルダに置き、1点ずつ Manifest に登録する。**登録されていない素材は「無い」のと同じ**。
- **参照する**: Remotion は `remotion/public/assets/<category>/` を `staticFile()` で参照する。H: から同期する。
- **選ぶ**: Scene Plan / `import_to_remotion.py` が、Manifest の `compatibleSceneTypes` / `useCases` / `tags` / `mood` で候補を絞り、Scene ごとに割り当てる。

---

## 2. 14カテゴリ仕様表

凡例:
- alpha = 透過の有無（パーツ系は透過必須が多い）。
- 尺/ループ = 動く素材の尺と、ループ可否。静止画は「—」。
- 優先度 = ファクトリーとして先に貯める優先度（P0 最優先 / P1 / P2）。詳細数量は priority-list 参照。
- 保存場所はすべて H: に実体、`remotion/public/assets/<category>/` に同期参照。
- manifest の `type` は asset.schema.json の `asset_type`（既存 enum）に写像、`subtype` は本ファクトリー独自の細分。

| # | category | 用途 | 形式（拡張子・alpha・尺/ループ） | 命名規則 | 優先度 | 想定 sceneType | 生成ツール | manifest type / subtype |
|---|---|---|---|---|---|---|---|---|
| 1 | **backgrounds** | 各 Scene の下地。ドキュメンタリー背景・暗いシネマ・抽象 | `.png`/`.jpg`、alpha なし、静止（—） | `AF-BG-NNNN__<slug>.png` | P0 | explanation, place_intro, abstract_emotion, problem_statement, opening_hook | Midjourney | image / background |
| 2 | **parallax_layers** | 背景を前後レイヤーに分解し横/奥行きの動きを作る | `.png`、alpha **あり**（前景・中景は透過）、静止素材を Remotion で動かす | `AF-PX-NNNN__<slug>__<near\|mid\|far>.png` | P1 | place_intro, opening_hook, emotional_pause, abstract_emotion | Midjourney | image / parallax_layer |
| 3 | **vfx_overlays** | 画面に重ねる効果（film grain, vignette, light leak, dust, scanline） | `.mov`(ProRes4444)/`.webm`、alpha **あり**または黒背景(加算/スクリーン合成)、ループ可 2–8s | `AF-VFX-NNNN__<slug>.mov` | P0 | （全 sceneType に薄く重畳） | Midjourney(静止)＋Runway(動)／合成 | video / vfx_overlay |
| 4 | **loops** | 背景として無限ループする動き（atmosphere, smoke, bokeh, particle field） | `.mp4`/`.webm`、alpha なし可、**loopable=true**、4–10s シームレス | `AF-LOOP-NNNN__<slug>.mp4` | P1 | explanation, emotional_pause, abstract_emotion, chapter_title | Runway／SDXL動 | video / loop |
| 5 | **transitions** | カット間のつなぎ（whip, light sweep, glitch, paper slide） | `.mov`/`.webm`、alpha **あり**または黒、ループ不可、0.3–1.5s | `AF-TR-NNNN__<slug>.mov` | P1 | transition_bridge（＋全カット境界） | Runway／合成 | video / transition |
| 6 | **typography_assets** | 章タイトル枠・下三分・キーワード枠・引用枠などの装飾（テキストは入れない＝CANON「画面文字なし」素材として枠のみ） | `.png`(静止枠)/`.mov`(出現アニメ枠), alpha **あり** | `AF-TY-NNNN__<slug>.png` | P0 | chapter_title, quote, character_profile, summary | Midjourney(枠)／Remotion合成 | image / typography_asset |
| 7 | **diagram_assets** | 図解パーツ（arrow, line, bracket, node, label, map pin, highlight box, chart accent, badge） | `.png`/`.svg`、alpha **あり**、静止（Remotion で描画アニメ） | `AF-DG-NNNN__<slug>.png` | P0 | timeline, evidence_board, comparison, data_reveal, solution_reveal, problem_statement | Midjourney／SVG手起こし | diagram / diagram_part |
| 8 | **sfx** | 効果音（whoosh, hit, pop, tick, riser, paper, camera, glitch, sweep） | `.wav`(48k/24bit) または `.mp3`、0.1–3s | `AF-SFX-NNNN__<slug>.wav` | P0 | （リビール/カット/テロップ出現で全般） | ElevenLabs | audio / sfx |
| 9 | **ai_video_shots** | 見せ場の AI 動画（opening_hook/turning_point/reenactment/emotional_pause/ending/abstract_emotion 限定） | `.mp4`(h264/30fps)、alpha なし、4–10s | `AF-AV-NNNN__<slug>.mp4` | P1 | opening_hook, turning_point, reenactment, emotional_pause, ending, abstract_emotion | Runway | video / ai_video_shot |
| 10 | **lottie_assets** | ベクターUIアニメ（arrow draw, line draw, loading, check, warning, map pin, chart, business icon） | `.json`(Lottie/Bodymovin)、軽量、ループ可/不可は素材依存 | `AF-LOT-NNNN__<slug>.json` | P1 | data_reveal, evidence_board, solution_reveal, ui_motion 系 | LottieFiles（手動DL・ローカル JSON のみ） | other / lottie |
| 11 | **ui_motion_assets** | 画面UI風モーション（cursor, scan line, focus box, loading bar, blink）。調査/技術系演出 | `.mov`/`.webm`(alphaあり) または `.json`(Lottie) | `AF-UI-NNNN__<slug>.mov` | P2 | reenactment, evidence_board, data_reveal, abstract_emotion | LottieFiles／Remotion合成 | video / ui_motion |
| 12 | **texture_assets** | 質感重ね（paper, concrete, noise, fabric, fingerprint, ink） | `.png`/`.jpg`、alpha 任意、静止、タイル可 | `AF-TX-NNNN__<slug>.png` | P1 | quote, evidence_board, chapter_title, emotional_pause | Midjourney | texture / texture |
| 13 | **light_assets** | 光素材（light leak, lens flare, god ray, glow, spotlight） | `.png`(静止)/`.mov`(動・黒背景=加算合成)、alpha または黒 | `AF-LT-NNNN__<slug>.png` | P1 | turning_point, ending, emotional_pause, opening_hook, solution_reveal | Midjourney(静)／合成(動) | image|video / light |
| 14 | **particle_assets** | 粒子素材（dust, smoke, ember, snow, spark, bokeh particle） | `.mov`/`.webm`(黒背景=加算)、ループ可 3–8s | `AF-PT-NNNN__<slug>.mov` | P1 | abstract_emotion, emotional_pause, turning_point, opening_hook | Midjourney(静)／Runway(動) | particle / particle |

> 注（黒背景合成）: CANON では Runway は見せ場動画のみ。煙・光・粒子の **動く透過っぽい素材**は、原則 **黒背景で生成し、Remotion 側で screen/add 合成**する考え方を採る（真の alpha 動画が作れない場合の代替）。ProRes4444 で本当の alpha を持てる場合はそちらを優先。

> 注（asset_type 写像）: 既存 `asset.schema.json` の `asset_type` enum は `image, video, diagram, map, audio, music, subtitle, thumbnail, render, project, other`。ファクトリー素材は基本 `image / video / diagram / audio / other` に収まる。`particle / texture / light / parallax` などファクトリー固有の粒度は **`subtype`** で表現し、`type`(=asset_type) は上表に従って既存 enum へ写像する（schema を勝手に拡張しない）。

---

## 3. Manifest 設計（asset.schema.json の拡張）

### 3.1 方針

- ファクトリー素材も **1点 = 1 manifest レコード**。既存 `asset.schema.json` を土台にする。
- ただしファクトリー素材は **特定 episode/scene に属さない再利用前提**。既存 schema は `episode_id` / `scene_id` を required にしているため、ファクトリー素材は次のいずれかで扱う（実装時に決定。仮定として後者を推奨）:
  - (a) 予約値を入れる: `episode_id = "PD-0000-000-factory"`, `scene_id = "S000"`（「どの話にも属さない共有棚」を表す sentinel）。
  - (b) schema を後方互換で拡張し、`schema_version` を上げて factory 用にこれらを optional 化する（migration 必須）。**推奨は (a)**（schema 改変なし・移行不要）。
- CANON が要求する **Manifest 最低フィールド**を、既存フィールドに次のように対応・追加する。追加分は asset.schema.json のトップレベル `factory` オブジェクト（拡張）にまとめる想定（schema 拡張時）。実装まではドキュメント上の論理フィールドとして定義する。

### 3.2 フィールド対応表（CANON 最低フィールド → 格納先）

| CANON フィールド | 格納先（既存 or 拡張） | 説明 |
|---|---|---|
| id | `asset_id` = `AF-<CAT>-NNNN` | ファクトリー ID。例 `AF-VFX-0007` |
| type | `asset_type`（既存 enum へ写像） | 上表「type」列 |
| subtype | `factory.subtype` | 上表「subtype」列 |
| path | `uri`（logical, `artifact://` 推奨） | 実体は H:。OS 絶対パスを真実にしない（rule 14） |
| previewPath | `factory.previewPath` | 軽量サムネ/プレビュー（必須・棚の見える化） |
| sourceTool | `provenance.provider` | midjourney/runway/elevenlabs/suno/lottiefiles |
| durationFrames | `factory.durationFrames` | 静止は null |
| fps | `factory.fps` | 既定 30 |
| width / height | `factory.width` / `factory.height` | px |
| hasAlpha | `factory.hasAlpha` | bool |
| loopable | `factory.loopable` | bool |
| mood | `factory.mood` | 例: dark, tense, hopeful, neutral, somber |
| intensity | `factory.intensity` | 例: subtle / medium / strong |
| useCases | `factory.useCases[]` | 例: "reveal a number", "scene transition" |
| compatibleSceneTypes | `factory.compatibleSceneTypes[]` | **20 sceneType の語彙のみ**許可 |
| colorTone | `factory.colorTone` | ブランド配色語彙（ink/navy/electric/silver/gold/white/mixed） |
| tags | `factory.tags[]` | 検索用キーワード（必須） |
| sourcePrompt | `provenance.prompt_ref` ＋ `factory.sourcePrompt` | 生成プロンプト本文/参照 |
| negativePrompt | `factory.negativePrompt` | ネガティブ |
| seed | `provenance.seed` | 再現用 |
| license | `rights`（既存 object: status/origin/commercial_use） | **commercial_use = allowed 必須** |
| createdAt | `factory.createdAt`（timezone-aware ISO8601） | — |
| notes | `factory.notes` | 自由記述 |

> `compatibleSceneTypes` と `colorTone` は **enum で固定**する（CANON の 20 sceneType と 6 ブランド色のみ）。未知値はバリデーションで弾く（rule 02 enum 設計、rule 15 出力検証）。

### 3.3 Manifest ファイル配置（仮定）

- 単一の巨大ファイルにしない。**カテゴリ別 manifest** に分割:
  - `assets/factory/manifest/<category>.manifest.json`（配列 or `{ "assets": [...] }`）。
  - ルート索引 `assets/factory/manifest/index.json`（カテゴリ→件数・最終更新）。
- これらは **軽量 JSON なので Git 管理してよい**（素材実体は H: で Git 管理外）。manifest だけ版管理されることで「棚の状態」が追える。

---

## 4. 「ゴミ素材置き場にしない」運用

ファクトリーが膨れて使えない素材の山にならないための強制ルール。

### 4.1 登録時の必須条件（これが無いと棚入り不可）

1. **previewPath 必須** — プレビューの無い素材は選定 UI で見えず死蔵する。サムネ自動生成を登録パイプラインに組み込む。
2. **tags 必須（最低3個）** — 無タグは検索不能 = 実質ゴミ。
3. **useCases 必須（最低1個）** — 「何のために使うか」言語化されていない素材は入れない。
4. **compatibleSceneTypes 必須** — 20 sceneType のどれにも紐づかない素材は用途不明として入れない。
5. **rights.commercial_use = allowed** — VIDEO_RULES §5 に従い、商用OK以外は棚に入れない（MJ/Suno/自家生成は OK、外部DLは権利確認後）。
6. **preview/実体の checksum** — 既存 schema の `checksum` 必須を踏襲。

### 4.2 重複回避

- 登録前に **知覚ハッシュ（画像/動画）／音響フィンガープリント（SFX）** で近似重複を検出し、近すぎる素材は登録拒否 or バリアント束ね（`factory.variantOf`）。
- 同一 `sourcePrompt` + `seed` の重複生成を弾く（provenance で検出）。

### 4.3 棚卸し（定期メンテ）

- 四半期ごと（仮定）に「**使用回数 0 かつ 登録から N か月**（仮定: 6 か月）」の素材を **`status = stale` 候補**として抽出（削除はしない＝rule 05/12: 監査可能に残す）。
- 使用回数は Scene Plan / import_to_remotion からの参照ログで集計（`factory.useCount` を集計値として持つ想定）。
- 各カテゴリの **過剰生成上限**（priority-list の目標数に対する倍率）を設け、超過は P2 へ降格して生成を止める。

### 4.4 命名・ID の一意性

- `AF-<CAT>-NNNN` は**カテゴリ内連番でグローバル一意**。採番は manifest index が管理（手動採番禁止＝衝突防止）。
- ファイル名は `AF-<CAT>-NNNN__<slug>.<ext>`。`<slug>` は内容を表す英小文字・ハイフン区切り。

---

## 5. Remotion からの参照と Scene Plan / importer 接続

### 5.1 同期（H: → public）

- 実体は `H:\pd-media\assets\factory\<category>\`。Remotion は public 配下しか `staticFile()` で読めないため、**選定された素材だけ** `remotion/public/assets/<category>/` に同期コピーする（全件コピーしない＝public を太らせない）。
- 小さい Lottie JSON は例外として `remotion/public/assets/lottie/` に直接置いてよい。
- 同期は atomic（temp→rename）＋ checksum 照合（rule 14）。

### 5.2 参照方法（Remotion 側）

- 取り込み済み素材は `staticFile("assets/<category>/AF-<CAT>-NNNN__<slug>.<ext>")` で参照。
- 黒背景の光/煙/粒子は Remotion 側で `mixBlendMode: "screen"` 等の加算合成、alpha 素材はそのまま重畳。

### 5.3 Scene Plan / import_to_remotion.py との接続

既存 `import_to_remotion.py` は episode の `shotlist.v001.json` と `usable_assets.v001.json`（episode 取得分のプール）からキーワード一致で選定している。ファクトリーは **この「プール」を拡張する第2の供給源**として接続する:

1. **候補供給**: 各 Scene/Shot の `sceneType` と `search_keywords` から、ファクトリー manifest を検索して候補を出す。
   - フィルタ = `compatibleSceneTypes ∋ sceneType` かつ `tags/useCases` がキーワードと重なる。
   - `mood` / `intensity` / `colorTone` で更に絞る。
2. **選定**: 既存 importer の `pick_asset` / `pick_videos` と同じ「キーワード重なりスコア」方式に乗せる。ファクトリー素材は `used_in_spans` に相当する明示割当があればスコア加点（既存ロジック踏襲）。
3. **同期**: 選ばれた素材だけ public に同期コピーし、`<slug>_roughcut.ts` の `src`/`images`/`clips` に入れる。
4. **記録**: 使用したら Scene 側の asset 記録（episode manifest）に `asset_id` を残し、ファクトリー側 `useCount` を加算（棚卸しの根拠）。

> 接続点の実装仮定: importer に `--factory` モードか、`usable_assets` プールにファクトリー候補をマージする小関数を足す（既存選定ロジックを置換せず**拡張**する＝CLAUDE.md 不変条件14）。背景・overlay・diagram・transition・sfx といった「episode 横断の汎用素材」は、ほぼ常にファクトリーから供給される想定。

---

## 6. 参照ドキュメント

- CANON（本タスク指示）— 14カテゴリ・20 sceneType・ツール役割・配色・命名・manifest最低フィールド。
- `schemas/asset.schema.json` — Manifest の土台 schema。
- `episodes/_planning/VIDEO_RULES.md` — 美しさ最優先・静止禁止・30fps・商用OKのみ・実在人物の肖像なし・画面文字なし。
- `scripts/import_to_remotion.py` — Scene への素材割当の既存実装（拡張対象）。
- `docs/asset-priority-list.md` — 先に作る素材の優先度・数量・初期目標。
- `docs/asset-generation-prompts.md` — カテゴリ別生成プロンプト雛形。
