# Asset Generation Prompts（カテゴリ別 生成プロンプト雛形）

ステータス: **設計（未実装）**

## 前提・仮定

- 本書は `docs/asset-factory.md` / `docs/asset-priority-list.md` の付随書。**各ツールで素材を量産するためのプロンプト雛形**を定義する。
- CANON のツール役割を厳守: Midjourney=静止画パーツ（分解的）/ Runway=見せ場動画のみ / ElevenLabs=SFX・ambience・ナレ / SUNO=BGM / LottieFiles=手動DLのローカル JSON のみ。**追加の有料ツール・素材サブスクは前提にしない。**
- `episodes/_planning/VIDEO_RULES.md` と矛盾しないこと（美しさ最優先・最高画質・長辺2048px以上・静止禁止＝必ず動かす前提・商用OKのみ・実在人物の肖像なし・AIはAIと開示・画面文字なし・1920×1080/30fps・ブランド配色）。
- 雛形中の `{...}` は差し込み変数。生成後は `docs/asset-factory.md` の命名 `AF-<CAT>-NNNN__<slug>` と manifest 登録を必ず行う。

## ブランド／品質 共通ブロック（全プロンプトに内蔵する固定句）

すべての**画像/動画**プロンプトに、次の意図を必ず織り込む（言い回しは調整可、内容は固定）:

- **配色**: ink (#0A0A0C) / navy (#0B1A2B) / electric blue (#1F6BFF) accent / silver (#C8CDD6) / gold (#E5B53A) / off-white (#F5F7FA)。基調は暗いシネマ、アクセントに electric blue と gold。
- **品質**: cinematic, high-end documentary look, very high resolution（**long edge ≥ 2048px, 可能なら 3840px**）, sharp, clean, professional color grading, filmic contrast, shallow depth of field where relevant。
- **禁止（共通ネガティブの考え方）**: **no real-person likeness / no recognizable real people（実在人物の肖像なし）**, **no text, no letters, no words, no captions, no watermark, no logo, no UI（画面文字なし＝テキストは Remotion 側で重畳）**, no low resolution, no blur artifacts, no jpeg artifacts, no oversaturation, no AI-cartoon look, no deformed hands/faces。
- **アスペクト**: 16:9（`--ar 16:9`）。透過パーツは透過/黒背景指定（後述）。

> ネガティブの考え方: 「**入れたくないもの**」だけでなく「**ブランドを壊すもの**（過度な彩度・文字・実在人物・チープな3D/イラスト調）」を恒常的に弾く。MJ は `--no <...>`、Runway は否定文、ElevenLabs は SFX 指示文で「不要な要素を含めない」と明記。

---

## 1. Midjourney（静止画・分解的レイヤー）

**思想**: 1枚で完成画を狙わず、**背景・人物・前景・光・煙をパーツに分解**して作る。Remotion 側で重ね・動かし（Ken Burns / parallax / 合成）するのが前提。透過が要る前景・光・煙は **alpha 前提なら被写体を孤立**させ、合成用の動き素材は **純黒背景**で出して screen/add 合成する。

### 1.1 背景（backgrounds）

```
{scene description, e.g. "empty modern corporate boardroom at night"}, cinematic documentary background,
dark moody atmosphere, color palette deep ink black and navy with subtle electric blue and gold accents,
filmic lighting, shallow depth of field, photorealistic, extremely detailed, high resolution,
no people, empty space, --ar 16:9 --style raw --no text, letters, watermark, logo, people, faces
```
- 用途: explanation / company_profile / place_intro / problem_statement の下地。
- mood を変えて複数生成（dark / tense / hopeful / somber）。

### 1.2 人物（character / parallax_layers）— 肖像にしない

```
{role, e.g. "a businessperson seen from behind"}, anonymous, face not visible (back view / silhouette /
hands only / over-the-shoulder), cinematic documentary portrait, dramatic low-key lighting,
ink and navy tones with electric blue rim light, photorealistic, high resolution,
generic non-identifiable person, --ar 16:9 --style raw
--no recognizable face, real person likeness, celebrity, text, watermark, logo
```
- **必ず顔を特定させない**（後ろ姿・シルエット・手元・逆光）。実在人物の肖像は禁止（CANON / VIDEO_RULES §5）。
- 前後分離が要る時は被写体を孤立させ、背景は別生成（parallax 用 near/mid/far）。

### 1.3 前景ぼかし（parallax_layers / 前ボケ）

```
out-of-focus foreground elements ({e.g. "blurred desk objects" / "window blinds" / "foliage"}),
heavy bokeh, shallow depth of field, dark cinematic tones, navy and ink with soft electric blue glints,
isolated on plain background for compositing, high resolution
--ar 16:9 --no text, sharp focus, people, faces, watermark
```
- 透過合成を狙う場合は「isolated on plain/black background」を明示。

### 1.4 光（light_assets）— 合成前提・黒背景

```
{light type: "light leak" / "lens flare" / "god rays" / "soft glow"}, warm gold and electric blue light,
on pure black background, high contrast, for screen/add blending, cinematic, high resolution,
no environment, just the light --ar 16:9 --no text, people, objects, watermark
```
- **pure black background** を必ず指定 → Remotion で `mixBlendMode: screen/add` 合成。

### 1.5 煙 / 粒子（particle_assets / texture）— 合成前提・黒背景

```
{"thin drifting smoke" / "floating dust particles" / "embers"}, on pure black background,
soft, subtle, slow, cinematic, ink and faint electric blue tint, high resolution, isolated element
--ar 16:9 --no text, people, bright background, watermark
```
- 動かす場合はこの静止を Runway/SDXL で動かす、もしくは最初から動素材を作る（§2.最後）。

### 1.6 図解パーツ / 装飾枠（diagram_assets / typography_assets）

- 図解の基本線・矢印・ノードは **SVG / Remotion 描画を第一**にし、MJ は質感のある枠やバッジ等に限定。
```
{"minimal clean frame" / "number badge" / "lower-third bar"} graphic element,
flat minimal design, navy and ink with gold/electric blue accent line, on transparent or pure black background,
crisp edges, vector-like, no text inside, high resolution
--ar 16:9 --no text, letters, numbers, words, watermark, gradient noise
```
- **枠の中にテキストを入れない**（テキストは Remotion で重畳＝CANON「画面文字なし」）。

---

## 2. Runway（見せ場動画のみ）

**思想**: 高コストなので **opening_hook / turning_point / reenactment / emotional_pause / ending / abstract_emotion の決め所だけ**（CANON）。原則は MJ 静止画を **image-to-video** で動かす（再現性・品質が安定）。尺は **4〜10 秒**、書き出し 1920×1080 / 30fps 前提。

### 2.1 共通指示

- 動きは**ゆっくり・上品**（slow push-in / slow parallax / gentle drift）。激しい手ブレ・チラつきは禁止（VIDEO_RULES §3）。
- 文字・実在人物を出さない。ブランド配色を維持。
- ループが要る背景（loops/particle）は **シームレスループ**を指示。

### 2.2 雛形（image-to-video 推奨）

```
{input: AF-... 静止画}. Subtle cinematic motion: slow {push-in / pull-out / parallax drift},
gentle atmospheric movement (dust/light), stable camera, no shake, documentary tone,
ink/navy palette with electric blue and gold accents, 16:9, ~{4-8}s, high quality.
Avoid: text, on-screen letters, real-person faces, fast jitter, warping.
```

### 2.3 sceneType 別の動かし方

| sceneType | 動きの方向性 | 尺 |
|---|---|---|
| opening_hook | 力強い slow push-in＋光のフレア立ち上がり | 4–6s |
| turning_point | カメラがわずかに傾く/光が差す（緊張→転換） | 5–8s |
| reenactment | 手元・物・空間の静かな動き（顔は出さない） | 5–8s |
| emotional_pause | ごく緩やかな drift＋bokeh の漂い | 6–10s（loop可） |
| ending | 引き／フェード／光が満ちる | 5–8s |
| abstract_emotion | 抽象的な煙・粒子・光の流動 | 6–10s（loop可） |

### 2.4 合成用 動素材（particle/light/loops）

```
Seamless looping {drifting smoke / floating particles / light leak} on pure black background,
slow, subtle, for screen/add compositing, 16:9, ~6s loop, no text, no objects, high quality.
```

---

## 3. ElevenLabs（SFX / ambience / riser）

**思想**: SFX は **短く・要所のみ**（VIDEO_RULES §11）。1音 = 1ファイル、48k/24bit 推奨。指示文は「**何の音か・長さ・質感・不要素**」を明記。

### 3.1 雛形（SFX 生成指示文）

```
A short {whoosh / impact hit / pop / tick / riser / sweep} sound effect for a premium documentary.
Character: {clean and cinematic / deep and heavy / soft and subtle}. Length: {0.2-1.5}s.
Use: {scene transition / number reveal / telop appear / build tension}.
No music, no voice, no melody, dry/minimal reverb, broadcast-clean.
```

### 3.2 種類別の指示ポイント

| SFX | 指示の要点 |
|---|---|
| whoosh / fast / soft whoosh | air-movement, transition, 長さで速さを出す。melody なし |
| hit / low hit | impact, weight。low hit は sub-bass を強調 |
| pop | short, clean, UI-like reveal。耳に痛くない |
| tick | clock/counter, crisp, short |
| riser | rising tension, build-up, 2–4s, 終端で hit に繋げる |
| ambience dark / office / city | **loopable bed**, 薄く敷く環境音, no foreground events, 10–30s |
| paper slide / camera click | foley 質感, dry, single event |
| glitch / sweep / bass accent | accent, 要所のみ, 過剰にしない |

- ambience は **ナレ下のベッド**前提（ダッキングで下げる）。前景イベント音を含めない。
- ナレーション（master）は ElevenLabs だが本書の対象外（課金前承認ゲートあり＝VIDEO_RULES §8）。

---

## 4. SUNO（BGM）

- BGM は SUNO 由来トラックを**素材として取り込む**（プログラム生成は前提にしない＝CLAUDE.md §11）。本書では雛形のみ示し、量産対象は SFX/画像優先。
```
Instrumental documentary score, {tense / hopeful / somber / neutral}, cinematic, restrained,
low-key, slow build, no vocals, no lyrics, supports narration (stays in background), loopable sections.
```
- ナレ中は控えめ・フック/盛り上がりで上げる前提（VIDEO_RULES §11）。商用利用・権利を素材として記録。

---

## 5. LottieFiles（手動DL・ローカル JSON のみ）

**思想**: **API も有料も使わない**。LottieFiles サイトで無料・商用利用可のアニメを**手動検索→手動DL**し、ローカル JSON として保存する。CANON / 権利ルール厳守。

### 5.1 検索キーワード（カテゴリ → 例）

| 用途 | 検索キーワード例 |
|---|---|
| arrow | "arrow", "arrow animation", "pointer" |
| line draw | "line draw", "underline", "drawing line" |
| loading | "loading", "spinner", "progress" |
| check | "check", "success check", "tick" |
| warning | "warning", "alert", "caution" |
| map pin | "map pin", "location pin", "marker drop" |
| chart | "bar chart", "line chart", "graph animation" |
| business icon | "business icon", "finance icon", "growth" |
| UI accent | "scan", "focus", "ui motion" |
| chapter decoration | "frame", "divider", "decoration" |

### 5.2 選定基準

- **ライセンスが商用利用可**であることをサイト上で確認（VIDEO_RULES §5 / メモ「権利確認」）。不明・有料のみのものは使わない。
- ブランド配色に**色変更できる**（単色/少色で塗り替え可能な）シンプルなものを優先。Lottie は色を JSON/Remotion 側で上書きしてブランド配色に寄せる。
- テキスト入りアニメは避ける（画面文字なし）。

### 5.3 ローカル保存手順（手動）

1. LottieFiles で検索 → 商用可を確認 → **Lottie JSON をダウンロード**。
2. `H:\pd-media\assets\factory\lottie_assets\` に保存し、**小さい JSON は `remotion/public/assets/lottie/` にも配置**（CANON 例外で直置き可）。
3. 命名 `AF-LOT-NNNN__<slug>.json`。
4. manifest 登録: `sourceTool = lottiefiles`、`rights.commercial_use = allowed`、出典URL・作者・取得日を `rights.origin` / `notes` に記録。
5. Remotion で `@remotion/lottie` 等から `staticFile("assets/lottie/AF-LOT-NNNN__<slug>.json")` を参照。

---

## 6. 生成後の共通チェック（全ツール共通）

- [ ] 命名 `AF-<CAT>-NNNN__<slug>.<ext>` に従ったか。
- [ ] H: の正しいカテゴリフォルダに保存したか。
- [ ] previewPath（サムネ）を作ったか。
- [ ] manifest に最低フィールド（id/type/subtype/path/previewPath/sourceTool/.../tags/sourcePrompt/negativePrompt/seed/license/createdAt/notes）を登録したか。
- [ ] `compatibleSceneTypes` は 20 sceneType の語彙か。`colorTone` はブランド配色語彙か。
- [ ] 画面文字・実在人物の肖像が入っていないか（再確認）。
- [ ] `rights.commercial_use = allowed` か。
- [ ] 1920×1080/30fps・長辺2048px以上の品質要件を満たすか。

---

## 参照

- `docs/asset-factory.md` — カテゴリ・命名・manifest・運用・importer 接続。
- `docs/asset-priority-list.md` — 何をどれだけ先に作るか。
- `episodes/_planning/VIDEO_RULES.md` — 制作ルール（本書はこれと矛盾しない）。
- `schemas/asset.schema.json` — manifest の土台 schema。
