# Factory MJ Prompts（Midjourneyで“今”量産する分）

> **ステータス: 設計／前提・仮定**

## 0. 前提・仮定

- 本書は `docs/asset-factory.md` / `docs/asset-priority-list.md` / `docs/asset-generation-prompts.md` の**実行用プロンプト集**。ストック（Pexels/Pixabay）では「質が出ない／そもそも無い」カテゴリを Midjourney で埋める、**そのまま投げられる1枚=1プロンプトのリスト**。
- **整合チェック済み**: `docs/asset-factory.md`（14カテゴリ・命名・manifest）、`docs/asset-priority-list.md`（数量）、`docs/asset-generation-prompts.md`（プロンプト雛形・共通ブロック）、`episodes/_planning/VIDEO_RULES.md`（美しさ最優先・静止禁止・商用OKのみ・実在人物の肖像なし・画面文字なし・1920×1080/30fps・ブランド配色）、`remotion/src/brand.ts`（配色）。
- **未解決の矛盾（報告事項・rule §5 / 07）**: `CLAUDE.md` §11 は「Midjourney retired — Codex (primary)」と記す。一方、本タスク指示・`docs/asset-factory.md`・`docs/asset-generation-prompts.md` は Midjourney を静止画パーツの量産ツールとして扱う。**本書はプロンプトの内容（被写体・配色・禁止句・構図）を “ツール非依存” に保ち**、`--ar 16:9 --style raw` 等の MJ パラメータは末尾に分離して付す。よって **Codex / SDXL で生成する場合は MJ パラメータ行を無視すれば同一プロンプトがそのまま使える**。最終的なツール採否はオーナー承認に従う（本書はツールを強制しない）。
- 命名・保存・登録は CANON 厳守:
  - Asset ID = `AF-<CAT>-NNNN`（カテゴリ内連番・グローバル一意。採番は manifest index が管理）。
  - 保存先（実体・Git管理外）= `H:\pd-media\assets\factory\<category>\`。
  - ファイル名 = `AF-<CAT>-NNNN__<slug>.<ext>`。生成後に previewPath 生成と manifest 登録（最低フィールド）を必ず行う。
- **下記 ID は提案（候補ID）**。実採番は manifest index が確定する（手動採番は衝突防止のため暫定値）。

## 1. ブランド／品質 共通ブロック（全プロンプトに内蔵済み・再掲）

`docs/asset-generation-prompts.md` の固定句を各プロンプトに織り込み済み。要点:

- **配色**: deep ink black `#0A0A0C` / navy `#0B1A2B` 基調、accent に electric blue `#1F6BFF` と gold `#E5B53A`、silver `#C8CDD6`、off-white `#F5F7FA`。基調は暗いシネマ、アクセントは控えめ。
- **品質**: cinematic, high-end documentary look, very high resolution (long edge ≥ 2048px, ideally 3840px), sharp, professional color grading, filmic contrast。
- **禁止（各プロンプト末尾 `--no` に内蔵）**: text / letters / words / captions / numbers / watermark / logo / UI、**real-person likeness / recognizable real people / celebrity（実在人物の肖像なし）**、low resolution, jpeg artifacts, oversaturation, AI-cartoon look, deformed hands/faces。
- **アスペクト**: 16:9（`--ar 16:9`）。透過/合成パーツは **isolated on pure black background**（Remotion 側で `mixBlendMode: screen/add`）か、孤立被写体指定。
- **MJ パラメータ例**: `--ar 16:9 --style raw --quality 1 --stylize 150 --no text, letters, watermark, logo, people, faces`。光/煙/粒子の黒背景合成系は `--style raw` 推奨（過剰な装飾を避ける）。

---

## 2. backgrounds（AF-BG-NNNN） — mood × シーン

> sceneType: explanation / place_intro / abstract_emotion / problem_statement / opening_hook / company_profile。各 mood（緊張tense / 荘厳solemn / 哀感somber / 中立neutral / 技術technical）で具体プロンプト。各1枚（推奨は同プロンプト2〜3バリエ生成→ベスト選抜）。

### 2.1 シネマ抽象（abstract dark cinematic）

- **AF-BG-1001** | backgrounds | sceneType: opening_hook, abstract_emotion | mood: tense
  `Cinematic abstract dark documentary background, slow swirling volumetric haze in deep ink black and navy, a single faint electric blue light source far in the distance, heavy negative space, oppressive tense atmosphere, filmic contrast, shallow depth of field, photorealistic, no people, no objects, ultra high resolution --ar 16:9 --style raw --no text, letters, numbers, watermark, logo, people, faces, oversaturation`
- **AF-BG-1002** | backgrounds | sceneType: opening_hook, chapter_title | mood: solemn
  `Cinematic abstract dark background, monumental empty void with soft god-ray light beams in navy and deep ink, faint gold rim glow, solemn grand atmosphere, vast scale, filmic grade, photorealistic, no people, ultra high resolution --ar 16:9 --style raw --no text, letters, watermark, logo, people, faces`
- **AF-BG-1003** | backgrounds | sceneType: abstract_emotion, emotional_pause | mood: somber
  `Cinematic abstract background, slow drifting smoke and dust in cold ink-black and muted navy, single dim window of pale off-white light, lonely somber melancholic mood, soft focus, high dynamic range, photorealistic, no people, ultra high resolution --ar 16:9 --style raw --no text, watermark, logo, people, faces, bright colors`
- **AF-BG-1004** | backgrounds | sceneType: explanation, chapter_title | mood: neutral
  `Minimal cinematic dark gradient background, smooth ink-to-navy gradient with subtle film grain, one quiet electric blue accent glow lower third, calm neutral documentary tone, clean, photorealistic, no people, ultra high resolution --ar 16:9 --style raw --no text, watermark, logo, people, faces, clutter`
- **AF-BG-1005** | backgrounds | sceneType: solution_reveal, explanation | mood: technical
  `Cinematic abstract technology background, dark navy field with faint glowing electric blue circuit-like light traces and soft data particles, gold micro-accents, sleek high-tech documentary atmosphere, depth of field, photorealistic, no people, no text, ultra high resolution --ar 16:9 --style raw --no text, letters, numbers, watermark, logo, people, faces, ui`

### 2.2 法廷（courtroom）

- **AF-BG-1006** | backgrounds | sceneType: place_intro, problem_statement | mood: solemn
  `Empty grand courtroom interior at low light, dark wood benches, tall columns, an empty judge's bench, deep ink and navy shadows with a single shaft of pale light, solemn institutional atmosphere, cinematic documentary, shallow depth of field, photorealistic, no people, no flags with insignia, no text, ultra high resolution --ar 16:9 --style raw --no text, letters, watermark, logo, people, faces, recognizable emblems`
- **AF-BG-1007** | backgrounds | sceneType: problem_statement, evidence_board | mood: tense
  `Empty courtroom from the gallery, harsh top-down light over an empty witness stand, long shadows, ink-black and navy palette with faint electric blue cold light, tense unsettling mood, cinematic, photorealistic, no people, no text, ultra high resolution --ar 16:9 --style raw --no text, letters, watermark, logo, people, faces`

### 2.3 オフィス／重役室（office / boardroom）

- **AF-BG-1008** | backgrounds | sceneType: company_profile, reenactment | mood: tense
  `Empty modern corporate boardroom at night, long glass conference table, city lights blurred through floor-to-ceiling windows, ink and navy tones with electric blue window glow and a single warm gold desk lamp, tense corporate atmosphere, cinematic, shallow depth of field, photorealistic, no people, no text, ultra high resolution --ar 16:9 --style raw --no text, letters, watermark, logo, brand names, people, faces`
- **AF-BG-1009** | backgrounds | sceneType: company_profile, explanation | mood: neutral
  `Empty open-plan office at dusk, rows of dark desks and monitors switched off, soft ambient ink-navy lighting with faint electric blue screen glow, quiet neutral documentary tone, cinematic depth, photorealistic, no people, no readable screens, no text, ultra high resolution --ar 16:9 --style raw --no text, letters, watermark, logo, brand names, people, faces, ui`
- **AF-BG-1010** | backgrounds | sceneType: reenactment, company_profile | mood: somber
  `Empty executive office at night, single occupied-looking leather chair turned away, papers scattered on a dark desk, low warm gold lamp against ink-black shadows, somber aftermath mood, cinematic, shallow depth of field, photorealistic, no people, no readable text, ultra high resolution --ar 16:9 --style raw --no text, letters, watermark, logo, people, faces`

### 2.4 技術（technology / lab / device）

- **AF-BG-1011** | backgrounds | sceneType: explanation, solution_reveal | mood: technical
  `Dark high-tech laboratory interior, sleek matte equipment and faint glowing instrument panels, deep ink and navy with electric blue indicator glow and gold micro-accents, clean clinical documentary atmosphere, shallow depth of field, photorealistic, no people, no readable labels, no text, ultra high resolution --ar 16:9 --style raw --no text, letters, numbers, watermark, logo, brand names, people, faces`
- **AF-BG-1012** | backgrounds | sceneType: solution_reveal, abstract_emotion | mood: technical
  `Macro close-up of a dark circuit board, shallow depth of field, faint electric blue traces glowing, gold contact pins catching light, ink-black background, sleek technical documentary mood, photorealistic, ultra high resolution, no text, no logo --ar 16:9 --style raw --no text, letters, numbers, watermark, logo, brand names, people, faces`

### 2.5 捜査ボード（investigative board）

- **AF-BG-1013** | backgrounds | sceneType: evidence_board, problem_statement | mood: tense
  `Dark investigation wall in a dim room, blank pinned cards and blank documents connected by taut red and white string, push-pins, cold side light, ink and navy shadows with faint electric blue, tense investigative mood, cinematic, shallow depth of field, photorealistic, no readable text on cards, no real photos, no faces, ultra high resolution --ar 16:9 --style raw --no text, letters, words, watermark, logo, people, faces, real photographs`
- **AF-BG-1014** | backgrounds | sceneType: evidence_board, explanation | mood: neutral
  `Top-down view of a dark desk covered with blank folders, a magnifying glass, and unmarked paper stacks under a focused desk light, ink-navy palette with gold lamp glow, neutral investigative documentary tone, cinematic, photorealistic, no readable text, ultra high resolution --ar 16:9 --style raw --no text, letters, words, watermark, logo, people, faces`

### 2.6 感情風景（emotional landscape）

- **AF-BG-1015** | backgrounds | sceneType: emotional_pause, ending | mood: somber
  `Lonely empty road at blue hour stretching into fog, cold ink-navy palette with a faint distant gold light, melancholic reflective documentary mood, cinematic wide shot, atmospheric haze, photorealistic, no people, no signs with text, ultra high resolution --ar 16:9 --style raw --no text, letters, watermark, logo, people, faces, readable signs`
- **AF-BG-1016** | backgrounds | sceneType: ending, emotional_pause | mood: solemn
  `Dawn breaking over a vast still landscape, low mist, deep navy sky shifting to pale gold horizon, single beam of hopeful light, solemn uplifting documentary tone, cinematic wide vista, photorealistic, no people, ultra high resolution --ar 16:9 --style raw --no text, watermark, logo, people, faces`
- **AF-BG-1017** | backgrounds | sceneType: place_intro, emotional_pause | mood: neutral
  `Rain on a window overlooking a blurred city at night, bokeh of ink-navy and electric blue lights with faint gold, quiet contemplative documentary mood, shallow depth of field, photorealistic, no people, no readable signs, ultra high resolution --ar 16:9 --style raw --no text, letters, watermark, logo, people, faces, readable signs`

> **backgrounds 小計の目安**: 7サブカテゴリ × 各 mood = **17 プロンプト**（priority-list グループ E の背景系 ~37 枚に対応。各プロンプトを 2〜3 バリエ生成しベスト選抜すると ~35〜50 枚）。

---

## 3. 人物（匿名・顔を出さない）（AF-BG-NNNN / AF-PX-NNNN）

> ドキュメンタリーで汎用に使える**シルエット/後ろ姿/手元/群衆**。**必ず顔を特定させない**（VIDEO_RULES §5 / CANON invariant 11）。parallax で前後分離が要る人物は `AF-PX`、背景一体は `AF-BG`。

- **AF-BG-1101** | backgrounds(人物) | sceneType: character_profile, reenactment | mood: tense
  `A lone businessperson seen strictly from behind, standing at a dark office window overlooking a blurred night city, silhouette, face not visible, dramatic low-key rim light in electric blue, ink and navy tones, cinematic documentary portrait, photorealistic, generic non-identifiable person, ultra high resolution --ar 16:9 --style raw --no recognizable face, real person likeness, celebrity, text, watermark, logo`
- **AF-BG-1102** | backgrounds(人物) | sceneType: reenactment, explanation | mood: neutral
  `Close-up of anonymous hands writing with a pen on blank paper at a dark wooden desk, only hands and forearms visible, no face, warm gold desk-lamp light against ink shadows, cinematic documentary detail, shallow depth of field, photorealistic, ultra high resolution --ar 16:9 --style raw --no face, real person likeness, text, words, watermark, logo`
- **AF-BG-1103** | backgrounds(人物) | sceneType: reenactment, evidence_board | mood: tense
  `Close-up of anonymous hands shuffling blank documents and folders on a desk under a focused light, only hands visible, no face, ink-navy palette with electric blue cold light, tense investigative mood, photorealistic, shallow depth of field, ultra high resolution --ar 16:9 --style raw --no face, real person likeness, readable text, watermark, logo`
- **AF-BG-1104** | backgrounds(人物) | sceneType: character_profile, emotional_pause | mood: somber
  `A solitary figure in silhouette sitting hunched on a chair in an empty dim room, back-lit, face fully hidden in shadow, deep ink and navy, faint cold window light, somber lonely documentary mood, cinematic, photorealistic, generic non-identifiable, ultra high resolution --ar 16:9 --style raw --no recognizable face, real person likeness, celebrity, text, watermark, logo`
- **AF-BG-1105** | backgrounds(人物) | sceneType: place_intro, problem_statement | mood: neutral
  `Anonymous crowd of commuters walking in a dim station concourse, all seen from behind or as motion-blurred silhouettes, no identifiable faces, ink-navy palette with electric blue ambient light, documentary observational tone, cinematic, photorealistic, ultra high resolution --ar 16:9 --style raw --no recognizable faces, real person likeness, text, readable signs, watermark, logo`
- **AF-BG-1106** | backgrounds(人物) | sceneType: reenactment, company_profile | mood: tense
  `Over-the-shoulder view of an anonymous person facing a dark wall of switched-off monitors, only back of head and shoulders visible in silhouette, electric blue screen glow, ink-navy, tense corporate mood, cinematic, photorealistic, generic non-identifiable, ultra high resolution --ar 16:9 --style raw --no face, real person likeness, readable screens, text, watermark, logo`
- **AF-PX-1107** | parallax_layers(人物・near層) | sceneType: opening_hook, place_intro | mood: tense
  `A single anonymous figure in full silhouette, sharp black cut-out shape of a standing person from behind, isolated on pure black background for compositing, no face, no detail, clean edges, soft electric blue rim light only, ultra high resolution --ar 16:9 --style raw --no face, real person likeness, background scene, text, watermark, logo`
- **AF-PX-1108** | parallax_layers(人物・mid層・群衆) | sceneType: place_intro, problem_statement | mood: neutral
  `A row of anonymous standing people as flat dark silhouettes, varied heights, seen from behind, isolated on pure black background for parallax compositing, no faces, no detail, clean separable edges, faint electric blue edge light, ultra high resolution --ar 16:9 --style raw --no faces, real person likeness, background, text, watermark, logo`

> **人物 小計の目安**: **8 プロンプト**（priority-list グループ E「人物」6枚＋parallax 人物層を補強）。

---

## 4. parallax_layers（前景/中景/背景の分離生成）（AF-PX-NNNN）

> 透過 or 黒背景指定で **near / mid / far** を別生成。`AF-PX-NNNN__<slug>__<near|mid|far>.png`。Remotion で奥行きを付けて動かす。

- **AF-PX-1201** | parallax_layers(near) | sceneType: place_intro, opening_hook | mood: neutral
  `Foreground silhouettes of dark window blinds and a desk edge, sharp near-layer cut-out, isolated on pure black background for parallax compositing, ink-black, faint electric blue glints, clean separable edges, ultra high resolution --ar 16:9 --style raw --no background scene, text, people, faces, watermark, logo`
- **AF-PX-1202** | parallax_layers(mid) | sceneType: place_intro, abstract_emotion | mood: somber
  `Mid-ground layer of distant city skyline silhouettes at night, flat dark shapes, isolated on pure black background for parallax, navy and ink with faint electric blue window lights, clean edges, ultra high resolution --ar 16:9 --style raw --no foreground, text, readable signs, people, faces, watermark, logo`
- **AF-PX-1203** | parallax_layers(far) | sceneType: emotional_pause, abstract_emotion | mood: somber
  `Far background layer of a foggy gradient sky, ink-to-navy gradient with a faint distant gold horizon glow, soft, no objects, full-frame backdrop for parallax, ultra high resolution --ar 16:9 --style raw --no foreground, objects, text, people, faces, watermark, logo`
- **AF-PX-1204** | parallax_layers(near・foliage) | sceneType: emotional_pause, place_intro | mood: neutral
  `Out-of-focus foreground foliage and branches as a dark near-layer, heavy bokeh, isolated on pure black background for compositing, ink-navy with soft electric blue glints, clean separable silhouette, ultra high resolution --ar 16:9 --style raw --no sharp focus, background, text, people, faces, watermark, logo`

> **parallax_layers 小計の目安**: **4 プロンプト**（priority-list グループ E「前景ぼかし」4枚＋parallax 分離。人物 parallax は §3 に2点）。

---

## 5. 前景ぼかし（foreground blur）（AF-PX-NNNN）

> 被写界深度の前ボケ。合成前提なら **isolated on pure black background**。

- **AF-PX-1301** | parallax_layers(前ボケ) | sceneType: place_intro, emotional_pause | mood: neutral
  `Out-of-focus foreground desk objects (blurred glassware and papers), heavy bokeh, shallow depth of field, dark cinematic ink-navy tones with soft electric blue glints, isolated on pure black background for compositing, ultra high resolution --ar 16:9 --style raw --no sharp focus, people, faces, text, watermark`
- **AF-PX-1302** | parallax_layers(前ボケ) | sceneType: emotional_pause, abstract_emotion | mood: somber
  `Blurred foreground rain droplets on glass, heavy bokeh, dark ink-navy with electric blue and faint gold light bokeh, isolated on pure black background, dreamy melancholic depth, ultra high resolution --ar 16:9 --style raw --no sharp focus, people, faces, text, watermark`
- **AF-PX-1303** | parallax_layers(前ボケ) | sceneType: company_profile, reenactment | mood: tense
  `Out-of-focus foreground of dark vertical window blinds, heavy bokeh slats, ink-navy, faint electric blue rim, isolated on pure black background for screen-edge framing, ultra high resolution --ar 16:9 --style raw --no sharp focus, people, faces, text, watermark`

> **前景ぼかし 小計の目安**: **3 プロンプト**。

---

## 6. light（光 / レンズフレア / 木漏れ日）（AF-LT-NNNN）

> **pure black background 必須** → Remotion で `mixBlendMode: screen/add` 合成。

- **AF-LT-1401** | light_assets | sceneType: turning_point, opening_hook | mood: tense
  `A horizontal anamorphic lens flare streak in electric blue with a faint gold core, on pure pure black background, high contrast, sharp light only, for screen/add blending, cinematic, no environment, ultra high resolution --ar 16:9 --style raw --no text, people, objects, background, watermark, logo`
- **AF-LT-1402** | light_assets | sceneType: ending, emotional_pause | mood: solemn
  `Soft warm gold light leak bleeding from the upper-right corner, gentle gradient glow, on pure black background, for screen/add compositing, cinematic, no environment, ultra high resolution --ar 16:9 --style raw --no text, people, objects, background, watermark, logo`
- **AF-LT-1403** | light_assets | sceneType: turning_point, solution_reveal | mood: solemn
  `Volumetric god rays beaming diagonally through darkness, pale gold and faint electric blue shafts, on pure black background, dust motes catching light, for screen/add blending, cinematic, ultra high resolution --ar 16:9 --style raw --no text, people, objects, environment, watermark, logo`
- **AF-LT-1404** | light_assets | sceneType: emotional_pause, place_intro | mood: somber
  `Dappled light through leaves (komorebi), soft moving sun spots, warm gold with cool ink shadows, on pure black background for screen blending, gentle cinematic, ultra high resolution --ar 16:9 --style raw --no text, people, objects, sharp foliage, watermark, logo`
- **AF-LT-1405** | light_assets | sceneType: solution_reveal, data_reveal | mood: technical
  `A single focused electric blue spotlight glow with soft falloff, centered, on pure black background, clean, for screen/add compositing, sleek technical mood, ultra high resolution --ar 16:9 --style raw --no text, people, objects, environment, watermark, logo`

> **light 小計の目安**: **5 プロンプト**（priority-list A「light leak 4」＋ E「光 3」を集約）。

---

## 7. smoke（煙 / 霧 / インク）（AF-PT-NNNN / AF-TX-NNNN）

> 黒背景=加算合成（particle）。インクは texture 寄りも可。動かす場合はこの静止を Runway/SDXL で動かす。

- **AF-PT-1501** | particle_assets(煙) | sceneType: turning_point, abstract_emotion | mood: tense
  `Thin wisps of slow drifting smoke, soft and subtle, on pure black background, ink-white with faint electric blue tint, isolated element for screen/add compositing, cinematic, ultra high resolution --ar 16:9 --style raw --no text, people, objects, bright background, watermark`
- **AF-PT-1502** | particle_assets(霧) | sceneType: emotional_pause, abstract_emotion | mood: somber
  `Low rolling fog mist, soft volumetric, on pure black background, cold navy-white tint, slow and atmospheric, isolated for screen compositing, cinematic, ultra high resolution --ar 16:9 --style raw --no text, people, objects, bright background, watermark`
- **AF-TX-1503** | texture_assets(インク) | sceneType: abstract_emotion, turning_point | mood: tense
  `Black ink diffusing and blooming in water, organic tendrils, high contrast, on pure black background (ink in white/electric-blue for screen blending), abstract cinematic, ultra high resolution --ar 16:9 --style raw --no text, people, objects, watermark, logo`
- **AF-PT-1504** | particle_assets(煙・重) | sceneType: opening_hook, turning_point | mood: solemn
  `Dense slow billowing smoke cloud rising, dramatic, on pure black background, ink-white with gold-lit edge, isolated for screen/add compositing, cinematic, ultra high resolution --ar 16:9 --style raw --no text, people, objects, bright background, watermark`

> **smoke/霧/インク 小計の目安**: **4 プロンプト**（priority-list A「smoke 4」＋ E「煙 3」を集約。dust/bokeh 等の他 particle は別途）。

---

## 8. 追加 particle / overlay（共通ベース・任意拡充）（AF-PT / AF-VFX）

> priority-list グループ A の dust / bokeh / particle field / film grain / vignette を MJ 静止で起こす分（動素材化は Runway/SDXL）。

- **AF-PT-1601** | particle_assets(dust) | sceneType: emotional_pause, abstract_emotion | mood: somber
  `Floating dust particles slowly drifting in a shaft of light, on pure black background, faint warm gold and electric blue motes, subtle, isolated for screen/add compositing, cinematic, ultra high resolution --ar 16:9 --style raw --no text, people, objects, bright background, watermark`
- **AF-PT-1602** | particle_assets(bokeh) | sceneType: emotional_pause, abstract_emotion | mood: neutral
  `Soft defocused bokeh orbs of light, ink-navy field with electric blue and gold bokeh circles, on dark background, dreamy cinematic, loopable-friendly even spread, ultra high resolution --ar 16:9 --style raw --no text, people, objects, sharp focus, watermark`
- **AF-PT-1603** | particle_assets(particle field) | sceneType: abstract_emotion, explanation | mood: technical
  `A field of small drifting light particles forming a subtle depth cloud, electric blue and gold points on ink-black background, sleek technical atmosphere, even distribution for looping, ultra high resolution --ar 16:9 --style raw --no text, people, objects, watermark, logo`
- **AF-VFX-1604** | vfx_overlays(film grain) | sceneType: 全（薄く重畳） | mood: neutral
  `Fine 35mm film grain texture, monochrome, even fine noise, on pure black/transparent base for overlay blending, subtle, no pattern banding, ultra high resolution --ar 16:9 --style raw --no text, people, objects, color, watermark, logo`
- **AF-VFX-1605** | vfx_overlays(vignette) | sceneType: 全（薄く重畳） | mood: neutral
  `Soft black vignette frame, dark edges fading to transparent center, smooth gradient, for multiply blending overlay, clean, ultra high resolution --ar 16:9 --style raw --no text, people, objects, color, watermark, logo`

> **追加 particle/overlay 小計の目安**: **5 プロンプト**。

---

## 9. typography_assets / diagram_assets（質感のある枠・バッジのみ）（AF-TY / AF-DG）

> 図解の基本線・矢印・ノードは **SVG/Remotion 描画が第一**（priority-list グループ B）。MJ は**質感のある枠・バッジ**に限定。**枠の中にテキストを入れない**。

- **AF-TY-1701** | typography_assets(章扉枠) | sceneType: chapter_title | mood: solemn
  `An elegant minimal rectangular chapter title frame, thin gold and electric blue accent border with subtle corner ornaments, empty interior, on pure black/transparent background, crisp vector-like edges, no text inside, ultra high resolution --ar 16:9 --style raw --no text, letters, numbers, words, watermark, gradient noise`
- **AF-TY-1702** | typography_assets(下三分枠) | sceneType: character_profile, explanation | mood: neutral
  `A sleek lower-third bar graphic, navy panel with a single gold accent line and small electric blue tick, empty (no text), on transparent background, crisp edges, modern broadcast style, ultra high resolution --ar 16:9 --style raw --no text, letters, numbers, words, watermark`
- **AF-TY-1703** | typography_assets(引用枠) | sceneType: quote | mood: somber
  `A refined quote frame with large open quotation-mark ornaments in gold, dark navy panel, subtle paper texture, empty interior, on transparent background, no text, crisp edges, ultra high resolution --ar 16:9 --style raw --no readable text, letters, words, watermark`
- **AF-DG-1704** | diagram_assets(数字バッジ枠) | sceneType: data_reveal, timeline | mood: technical
  `A clean circular number badge frame, electric blue ring with gold inner accent, empty center (no number), on transparent background, crisp vector-like, ultra high resolution --ar 16:9 --style raw --no text, letters, numbers, words, watermark`
- **AF-DG-1705** | diagram_assets(強調枠) | sceneType: evidence_board, data_reveal | mood: tense
  `A minimal highlight box bracket frame, thin electric blue corners with gold accent, empty interior, on transparent background, crisp edges, for overlay emphasis, ultra high resolution --ar 16:9 --style raw --no text, letters, numbers, words, watermark`

> **typography/diagram 枠 小計の目安**: **5 プロンプト**（残りの枠・図解は SVG/Remotion で生成＝priority-list B/C 本体）。

---

## 10. texture_assets（質感重ね）（AF-TX-NNNN）

- **AF-TX-1801** | texture_assets(紙) | sceneType: quote, evidence_board, chapter_title | mood: neutral
  `Aged off-white paper texture, subtle fibers and soft shadows, even flat lay, tileable, neutral documentary tone, for overlay blending, ultra high resolution --ar 16:9 --style raw --no text, letters, words, people, watermark, logo`
- **AF-TX-1802** | texture_assets(コンクリート) | sceneType: chapter_title, emotional_pause | mood: somber
  `Dark concrete wall texture, ink and navy tones, fine grain and subtle cracks, even flat surface, tileable, cinematic, for background/overlay, ultra high resolution --ar 16:9 --style raw --no text, people, watermark, logo`

> **texture 小計の目安**: **2 プロンプト**（priority-list A「paper 3」＋追加質感。残りは反復生成で枚数確保）。

---

## 11. 合計の目安数

| カテゴリ | プロンプト数 | 推奨生成枚数（各2〜3バリエ→選抜） |
|---|---|---|
| backgrounds（mood×シーン 7群） | 17 | ~35〜50 |
| 人物（匿名） | 8 | ~16〜24 |
| parallax_layers（near/mid/far） | 4 | ~8〜12 |
| 前景ぼかし | 3 | ~6〜9 |
| light（光/フレア/木漏れ日） | 5 | ~10〜15 |
| smoke/霧/インク | 4 | ~8〜12 |
| 追加 particle/overlay | 5 | ~10〜15 |
| typography/diagram 枠 | 5 | ~10〜15 |
| texture | 2 | ~4〜6 |
| **合計** | **53 プロンプト** | **約 107〜158 枚** |

> **目安: 53 プロンプト → 約 60〜100 枚を量産**（各プロンプト 1〜2 枚採用ベースなら ~60〜100、攻めて 2〜3 バリエなら ~110〜158）。priority-list の MJ 静止系（グループ A の静止起こし＋E ~51＋枠系）と整合する規模。
> P0 優先＝backgrounds（シネマ抽象/法廷/オフィス/捜査ボード/感情風景）・人物・light・smoke を先に。typography/texture は P0だが少数精鋭。

## 12. MJ パラメータ補足

- 基本: `--ar 16:9 --style raw`。装飾を抑えたい背景・合成素材で `--style raw` を強く推奨。
- 品質: `--quality 1`（必要に応じ `--quality 2`）。誇張を抑えるため `--stylize 100〜200`。
- 黒背景合成系（light/smoke/particle/枠）: **必ず `on pure black background` を本文に明記** し、`--no background, environment` を付す。
- バリエーション: 良い種は `--seed <n>` 固定で mood 違いを派生（manifest の `seed` に記録）。
- アップスケール後に **長辺 ≥ 2048px（理想 3840px）** を満たすこと（VIDEO_RULES §3）。
- **ツール非依存運用**: Codex/SDXL で出す場合は `--xxx` 行を削除し、本文プロンプトのみ使用（`negativePrompt` には末尾 `--no` の語を移す）。

## 13. 生成後チェック（再掲・必須）

- [ ] 命名 `AF-<CAT>-NNNN__<slug>.<ext>`／正しい H: カテゴリフォルダ保存。
- [ ] previewPath（サムネ）生成。
- [ ] manifest 最低フィールド登録（`compatibleSceneTypes` は20 sceneType語彙、`colorTone` はブランド配色語彙）。
- [ ] **画面文字・実在人物の肖像が入っていない**（再確認）。
- [ ] `rights.commercial_use = allowed`（MJ/自家生成は OK）。
- [ ] 長辺 ≥ 2048px・16:9。

## 参照

- `docs/asset-factory.md` — 14カテゴリ・命名・manifest・運用・importer 接続。
- `docs/asset-priority-list.md` — 数量・優先度。
- `docs/asset-generation-prompts.md` — プロンプト雛形・共通ブロック。
- `episodes/_planning/VIDEO_RULES.md` — 制作ルール（上位制約）。
- `remotion/src/brand.ts` — ブランド配色。
