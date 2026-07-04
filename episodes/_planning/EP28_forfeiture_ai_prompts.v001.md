# EP28 `ai_prompts.v001` — Codex ヒーロー静止画プロンプト集（民事没収）

**Episode:** `PD-2026-028-forfeiture`  ·  **一発1画像**（section E：1画像=1自己完結プロンプト）
**並行可**：本パックは**匿名の人物・雰囲気ショットのみ**。特定の未確定事実に依存しないので、**fact_recheck を待たず今すぐ Codex で生成してよい**。
**共通仕様（全プロンプトに適用済み）**：16:9・**長辺 ≥ 3840px**（生成が小さければ upscale+denoise）・シネマティックなドキュメンタリー写真・実写フォト調・35mm・浅い被写界深度・**寒色グレーディング（深いネイビーの影＋1灯だけ暖色の実用光）**・微フィルムグレイン・ハイダイナミックレンジ・落ち着いた重厚。
**人物ルール（不変項11＋オーナー2026-07-04）**：**人物の姿はOK＝ただし匿名**。顔は付随的に（横向き/影/ソフトフォーカス）＝**実在の誰か・有名人に似せない・特定できる顔にしない**。
**共通ネガティブ（全プロンプト末尾に付与）**：`no readable text or lettering, no logos, no watermark, no captions, no specific real person or celebrity likeness, no recognizable identifiable face, no distorted hands, no extra fingers, no bad anatomy, no cartoon, no illustration, no 3d render look, no oversaturation, no lens-flare spam`

> 使い方：各番号のプロンプトを**そのまま1枚ずつ**Codexに投げる。出力は `PD-2026-028-S###-IMG-001` 系のIDで保存し、長辺≥3840を確認（`image_resolution` ゲート）。

---

## ACT I — 家 / 普通の一家と$40の逮捕

**IMG-01 敷居の父（フック4カット目・主役）**
> A middle-aged father stands on the front steps of a modest brick row house at night, seen from behind and slightly to the side so his face is not identifiable, shoulders tense, hands at his sides. A single warm porch light above him; the street beyond falls into deep navy shadow. Cinematic documentary photography, 35mm, shallow depth of field, cold desaturated grade, subtle grain, restrained and ominous. 16:9, long edge ≥3840. [+共通ネガティブ]

**IMG-02 窓越しの家族の夕食**
> A modest family of four seen from outside through a kitchen window at night, gathered around a small dinner table, faces soft and turned away (anonymous), warm interior light glowing against the cold blue night outside. Intimacy about to be threatened. Cinematic documentary photography, shallow DOF, cold exterior / warm interior contrast, film grain. 16:9, long edge ≥3840. [+共通ネガティブ]

**IMG-03 $40（引き金・マクロ）**
> Extreme close-up of two twenty-dollar bills held in a young man's hand on a dark street at night, shallow focus, city bokeh behind, no face visible. The small sum that triggered everything. Cinematic macro, cold grade with a faint sodium-vapor warmth, grain. 16:9, long edge ≥3840. [+共通ネガティブ]

**IMG-04 夜のパトランプ（連棟住宅）**
> A police cruiser's red-and-blue lights washing across a row of brick townhouses on a narrow night street, wet asphalt reflecting the glow, no officers' faces visible. Tense, cinematic, documentary. Deep navy base with red/blue accents only from the lights. 16:9, long edge ≥3840. [+共通ネガティブ]

## ACT II — 機械 / 民事没収の仕組み

**IMG-05 玄関の没収告知（文字なし）**
> Macro of an official-looking legal notice taped to a scuffed front door, the paper embossed and slightly curled but the text intentionally blurred and unreadable, harsh cold daylight raking across it. Bureaucratic dread. Cinematic, shallow DOF, desaturated. 16:9, long edge ≥3840. [+共通ネガティブ]

**IMG-06 冷たい空の法廷（Courtroom 478）**
> An empty, cold institutional courtroom: rows of worn wooden benches, a raised bench in shadow, hard fluorescent overhead light, dust in the air, no people. Impersonal machinery of the state. Cinematic wide, desaturated navy-grey, grain. 16:9, long edge ≥3840. [+共通ネガティブ]

**IMG-07 待たされる所有者たち（匿名の群衆）**
> A bleak government corridor lined with benches where anonymous ordinary people wait — faces soft, turned, or shadowed so none is identifiable — under flat fluorescent light, worn linoleum floor. Quiet powerlessness. Documentary photography, cold grade, shallow DOF on the nearest waiting hands. 16:9, long edge ≥3840. [+共通ネガティブ]

**IMG-08 没収ファイルの山**
> A towering stack of manila case folders and legal documents on a metal shelf, dramatic low side light, dust motes, the sheer volume implying an industrial process. No readable text on the files. Cinematic still-life, cold desaturated grade, grain. 16:9, long edge ≥3840. [+共通ネガティブ]

## ACT III — 抵抗 / 集団訴訟と規模

**IMG-09 弁護士の後ろ姿と証拠箱の壁**
> A lone attorney figure (anonymous, seen from behind) standing before a floor-to-ceiling wall of banker's boxes of case files, small against the scale of it, a single overhead work light. Determination against a vast machine. Cinematic, cold grade, shallow DOF. 16:9, long edge ≥3840. [+共通ネガティブ]

**IMG-10 押収物件の帳簿（データは非可読）**
> A long printed ledger / spreadsheet of seized property entries spread across a table, rows and columns implied but text and numbers unreadable/abstract, an angled desk lamp pooling warm light on cold paper. The scale of the seizures. Cinematic macro-to-mid, desaturated. 16:9, long edge ≥3840. [+共通ネガティブ]

**IMG-11 施錠された住宅ドア（差押えの威圧）**
> A heavy padlock and chain across the door of an ordinary residential home, institutional and ominous, cold morning light, paint worn around the lock. Home turned into a seized asset. No readable text. Cinematic close, deep navy shadow, grain. 16:9, long edge ≥3840. [+共通ネガティブ]

## ACT IV — 決着 / ペイオフ

**IMG-12 鍵を回す手（払暁・救い＝フック回収）**
> Close-up of a family member's hand turning a key in the lock of their own front door at dawn, warm first light breaking across the brass and the worn door, a sense of relief and return. Anonymous, no face. Cinematic macro, cold-to-warm grade as dawn arrives, gentle grain. 16:9, long edge ≥3840. [+共通ネガティブ]

**IMG-13 夜明けの連棟住宅（解決）**
> A quiet street of brick row houses at sunrise, warm gold light breaking over the rooftops and burning off the navy of night, calm and resolved. No people. Cinematic wide establishing shot, cold shadows with a warm gold horizon, subtle grain. 16:9, long edge ≥3840. [+共通ネガティブ]

---

### 生成後チェック（Codex→Claude）
- 全画像 **長辺≥3840**（`image_resolution` ハードゲート）／ぼやけ・破綻・**可読テキスト・実在人物の顔**がないこと（reject 条件）。
- グレーディングが統一（寒色ネイビー＋1灯暖色）＝Remotionで暗め＋ネイビー寄せに馴染む。
- これらは **`bleed`(2.5Dパララックス)/`scan`/`duotone`/`focus`** で動かして使う（静止画のまま貼らない・row8）。
