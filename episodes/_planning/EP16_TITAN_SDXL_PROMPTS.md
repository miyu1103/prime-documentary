# EP16 「TITAN」 — Full SDXL Prompt Pack (全シーン・Codex事前生成用)

> 連携先: `EP16_TITAN_DESIGN_BIBLE.md`
> 生成: Codex / A1111 :7860 / **juggernautXL_ragnarokBy**
> 出力: `H:\pd-media\episodes\PD-2026-016-titan\05_stock\hero\` → QC(`pd-generate-assets`) → usableのみ manifest登録(license/sourceTool=sdxl/hash)
> ワークスペース作成後、本ファイルは `04_scenes/ai_prompts.v001.md` へ移設。

---

## 生成ルール（全カット共通）

**BASE_SUFFIX**（各プロンプト末尾にCodexが付与）:
`, cinematic documentary still, dramatic chiaroscuro lighting, deep navy and black palette with electric blue and gold rim light, photorealistic, ultra detailed, volumetric light, atmospheric haze, subtle film grain, shallow depth of field, anamorphic, masterpiece, ultra high resolution, 16:9`

**NEG**（全カット固定）:
`text, letters, words, watermark, logo, signature, caption, brand markings, identifiable face, recognizable real person, celebrity likeness, portrait of a specific person, deformed, mutated, extra fingers, extra limbs, bad anatomy, bad hands, low quality, lowres, blurry, jpeg artifacts, cartoon, anime, illustration, 3d render look, oversaturated, cluttered, ugly`

**Params（推奨）**: size `1344x768`(SDXL 16:9) / steps `34` / cfg `5.5` / sampler `DPM++ 2M Karras` / per prompt **6 variations** → QCで採用1–2。
**鉄則**: 顔の特定なし・実在人物/実物そのものとして提示しない・ブランド非特定・画面内テキストなし（テロップはRemotion側）。各カットに **Motion**（Codexが付けるKen Burns/parallax方向）を併記。

---

## 0. COLD OPEN (0:00–1:30)

**T-IMG-001 / hatch sealing** — Motion: slow push-in
`a heavy circular deep-sea hatch being sealed from the outside, rows of cold steel bolts, a single overhead industrial light, claustrophobic confined steel chamber, condensation on metal, tense silence`

**T-IMG-002 / bolt macro** — Motion: static→tiny drift
`extreme macro of a single steel bolt being tightened on a thick metal flange, cold blue rim light, oil-streaked threads, ominous finality, dust motes in the beam`

**T-IMG-003 / empty capsule interior** — Motion: slow dolly
`interior of a cramped windowless carbon-composite pressure capsule, bare curved walls, a single small porthole, cold blue light, oppressive emptiness, no people`

**T-IMG-004 / porthole into black** — Motion: push-in to black
`view through a small thick acrylic porthole into total black ocean water, faint reflection of a blue interior light on the glass, nothing visible beyond, dread`

**T-IMG-005 / title backdrop abyss** — Motion: very slow rise
`an immense empty black ocean abyss with one faint shaft of pale blue light dissolving into darkness from above, vast scale, lonely, negative space for title`

---

## 1. THE DREAM (1:30–13:00) — awe / wonder（暖色金の畏怖を混ぜる）

**T-IMG-006 / the calling sea** — Motion: slow pan R
`a vast calm moody ocean at golden dusk seen from a high cliff, endless horizon, warm gold light meeting deep navy water, romantic and dangerous, sense of a calling`

**T-IMG-007 / Titanic myth, vintage** — Motion: Ken Burns in
`a colossal early-20th-century ocean liner silhouette leaving harbor under golden smoke and steam, illustrative period mood, the proud myth of an unsinkable ship, aged cinematic tone`

**T-IMG-008 / the unsinkable headline era** — Motion: drift
`a vintage shipyard at dawn, towering riveted steel hull under construction, sparks and gold light, human figures dwarfed as tiny silhouettes, hubris of engineering`

**T-IMG-009 / the disruptor archetype** — Motion: slow push-in
`lone backlit silhouette of a confident man standing before a wall of bright glass and blueprints in a dark modern workshop, electric blue glow, visionary posture, no face visible`

**T-IMG-010 / the prototype workshop** — Motion: dolly L
`a sleek experimental deep-sea submersible prototype in a dim industrial workshop, exposed carbon-fiber and titanium, work lights, ambitious and unfinished, cold blue and gold`

**T-IMG-011 / carbon fiber winding** — Motion: macro drift
`extreme close-up of black carbon-fiber filament being wound around a cylindrical mold, glossy resin sheen, precise and beautiful, faint warning of fragility, blue rim light`

**T-IMG-012 / Silicon Valley creed** — Motion: parallax
`a dark minimalist boardroom at night, a single glowing screen, empty leather chairs, a city skyline beyond glass, the cold confidence of disruption, navy and electric blue`

**T-IMG-013 / the $250k ticket / wealth** — Motion: push-in
`stacks of crisp hundred-dollar bills and a single titanium briefcase on dark marble, a faint gold spotlight, the price of access, opulent and cold`

**T-IMG-014 / private explorers' world** — Motion: slow rise
`a luxury expedition yacht alone on a dark sea under a dramatic sky, warm cabin lights, privilege and adventure, tiny against the vastness`

**T-IMG-015 / the deep as frontier** — Motion: descend
`a glowing bathymetric map of a deep ocean trench on a dark screen, contour lines like a target, the last frontier, electric blue data glow`

**T-IMG-016 / Titanic wreck allure (symbolic)** — Motion: Ken Burns in
`the ghostly bow of a vast sunken ocean liner emerging from cold blue gloom, encrusted railings, ethereal illustrative quality, a monument 3800 meters down, reverent`

**T-IMG-017 / dreamers at the edge** — Motion: drift
`silhouettes of small human figures standing at the stern rail of a ship gazing at a vast dark ocean at dusk, awe and smallness, gold horizon line, no faces`

**T-IMG-018 / the first doubt (foreshadow)** — Motion: slow push
`a hairline crack beginning in a smooth dark carbon-composite surface, extreme macro, a single cold light raking across, beautiful and ominous, the first flaw`

---

## 2. THE WARNINGS (13:00–28:00) — cold institutional（青白・無機質）

**T-IMG-019 / the whistleblower** — Motion: push-in
`a lone silhouette of a man in a dim engineering office turning away from glowing monitors, papers in hand, isolation and conscience, cold blue light, no face`

**T-IMG-020 / the warning letter** — Motion: macro drift
`a formal printed warning letter on a desk under a hard desk lamp, dense paragraphs blurred unreadable, a magnifying glass resting on it, gravity and dread, no legible text`

**T-IMG-021 / stamped 'not certified' (symbolic)** — Motion: static→drift
`an official document on dark wood with an empty space where a certification seal should be, a red wax-seal absent, bureaucratic cold light, implication of refusal`

**T-IMG-022 / carbon fatigue diagram-hero** — Motion: parallax
`a cross-section of a cylindrical carbon-fiber hull wall with microscopic fractures spreading through the layers, scientific yet cinematic, electric blue glow on the cracks, fragility`

**T-IMG-023 / pressure vs. material** — Motion: push-in
`abstract visualization of immense water pressure as converging blue arrows crushing a thin curved wall, dark void, scientific tension, no text`

**T-IMG-024 / doubling down (the podium)** — Motion: slow push
`a confident lone silhouette gesturing before a small audience in a dim hall, a single spotlight, certainty bordering on arrogance, backlit, no face`

**T-IMG-025 / the game controller** — Motion: static→tiny drift
`a generic black wireless game controller resting in shadow on a brushed-metal surface, a single cold overhead light, mundane object made ominous, shallow focus`

**T-IMG-026 / THE WAIVER (signature device)** — Motion: macro slow pan
`a multi-page legal waiver lying on dark wood under a hard lamp, a fountain pen across it, ink half-dry, solemn and final, blurred body text, no legible words`

**T-IMG-027 / 'death' highlighted (symbolic)** — Motion: push-in
`extreme macro of a printed legal page with one stark word area circled in faint ink, the rest blurred, a cold raking light, foreboding, no readable text`

**T-IMG-028 / Mr. Titanic's diving past** — Motion: drift
`a worn deep-sea diving suit and an old brass diving helmet displayed in a dim study, decades of expeditions implied, reverent gold accent light, a life given to the deep`

**T-IMG-029 / Mr. Titanic's hands** — Motion: macro
`close-up of elderly weathered hands holding a small piece of rusted metal artifact in cold light, lifetime of experience, no face, tender and grave`

**T-IMG-030 / the father's watch** — Motion: macro drift
`an elegant heirloom wristwatch resting on dark fabric, warm gold reflection, the weight of family and legacy, intimate, shallow focus`

**T-IMG-031 / the boy's Rubik's cube (intro)** — Motion: static→drift
`a Rubik's cube sitting on a teenager's cluttered desk near a packed travel bag, soft window light, youth and ordinary life about to change, gentle and quiet`

**T-IMG-032 / the boy's fear** — Motion: very slow push
`an empty teenager's bedroom at dusk, a half-packed bag on the bed, a single lamp, the silence of reluctance, tender melancholy, no people`

**T-IMG-033 / billionaire explorer's memorabilia** — Motion: drift
`a shelf of expedition trophies, a worn flag and adventure medals in a dim wood-paneled room, a life chasing records, gold accent, no faces`

**T-IMG-034 / the five gather (boarding)** — Motion: slow dolly
`five distant silhouettes walking single-file along a wet harbor jetty at grey dawn toward a waiting vessel, mist, fateful and quiet, no faces, cold light`

**T-IMG-035 / the launch platform** — Motion: rise
`a floating launch-and-recovery platform holding a small submersible on a grey choppy sea at dawn, cold utilitarian, anticipation, navy palette`

---

## 3. THE DIVE (28:00–40:00) — fading light into black（光が消える）

**T-IMG-036 / the sealing, callback** — Motion: push-in
`a circular hatch closing from outside over a confined capsule, the last sliver of grey daylight narrowing to black, rows of bolts, point of no return`

**T-IMG-037 / lowered into the sea** — Motion: descend
`a small submersible being lowered by crane into a cold grey ocean, foam and spray, the surface swallowing it, lonely and small`

**T-IMG-038 / surface light zone** — Motion: descend
`a tiny submersible silhouette just below the ocean surface, shimmering god rays from above, blue-green sunlit water, the last brightness`

**T-IMG-039 / the twilight zone** — Motion: descend
`a lone submersible descending through deep blue twilight water, light dimming, suspended particles drifting up like snow, increasing pressure, isolation`

**T-IMG-040 / the midnight zone** — Motion: descend slow
`a faint submersible silhouette in near-total black water, a single weak external light, crushing darkness closing in, immense depth, dread`

**T-IMG-041 / interior, the controller in hand** — Motion: static→drift
`gloved hands resting on a game controller inside a cramped dim capsule lit by one screen's glow, tense focus, no face, claustrophobic intimacy`

**T-IMG-042 / the comms screen** — Motion: push-in
`a small dim text-message screen glowing in a dark capsule showing faint indistinct message bubbles, cold blue, the last thread to the surface, no legible text`

**T-IMG-043 / support ship sonar tracking** — Motion: parallax
`a dark ship operations room, green sonar and tracking screens glowing, a single descending blip, rain on a porthole, focused tension, no faces`

**T-IMG-044 / depth gauge falling** — Motion: macro
`an analog depth indicator needle sweeping past deep numbers in cold light, condensation, mechanical dread, no readable specifics`

**T-IMG-045 / ink in water (deep abstraction)** — Motion: slow bloom
`black ink billowing and unfurling through deep blue water in slow motion, organic and beautiful and ominous, abyssal, electric blue edge light`

**T-IMG-046 / the last signal** — Motion: static→flicker
`a single faint blip on a dark sonar screen beginning to fade, grain and static creeping in, the moment before loss, cold green glow`

**T-IMG-047 / contact lost (silence)** — Motion: hold black
`an almost entirely black frame with one tiny dissolving mote of blue light at the center, profound emptiness, the silence after a signal dies`

**T-IMG-048 / the indifferent deep** — Motion: very slow drift
`an endless black ocean void with faint suspended particles, no light source, total pressure and silence, the sea that does not answer`

---

## 4. THE SEARCH (40:00–52:00) — cold green/searchlight（捜索・哀悼）

**T-IMG-049 / ships gather** — Motion: rise
`several search vessels scattered across a vast grey North Atlantic under a heavy sky, sweeping searchlights, urgency and futility, cold desolate scale`

**T-IMG-050 / searchlights on black water** — Motion: pan
`powerful searchlight beams sweeping across dark choppy night ocean from a ship, fog catching the light, frantic hope, navy and cold white`

**T-IMG-051 / the world watches (newsroom glow)** — Motion: parallax
`a dark room of glowing screens all showing the same dim ocean scene, blue television light on empty chairs, the world holding its breath, no faces`

**T-IMG-052 / global attention map** — Motion: slow zoom
`a dark glowing world map with countless converging light points focused on one spot in the North Atlantic, electric blue data lines, collective gaze`

**T-IMG-053 / aircraft and sonar buoys** — Motion: drift
`a search aircraft silhouette over a vast dark ocean dropping a sonar buoy, ripples spreading, methodical desperation, cold dawn light`

**T-IMG-054 / the 'banging' sonar pulse** — Motion: pulse
`abstract concentric sonar rings pulsing outward across a dark green screen, a rhythmic faint signal, false hope visualized, grain`

**T-IMG-055 / the 96-hour clock** — Motion: macro slow
`extreme macro of a clock mechanism in cold light, hands and gears, relentless time, condensation, a countdown that already means nothing, ominous`

**T-IMG-056 / the mother waiting** — Motion: very slow push
`a lone female silhouette from behind on a ship's deck at grey dawn, wrapped against the wind, staring at an empty horizon, unbearable patience, no face`

**T-IMG-057 / ROV descends to search** — Motion: descend
`a robotic deep-sea ROV with bright lights descending into black water trailing a tether, mechanical and lonely, the last hope sent down`

**T-IMG-058 / crowds before screens** — Motion: drift
`silhouetted strangers gathered watching a glowing public screen at night, faces turned away, shared anxiety of millions, cold blue light`

**T-IMG-059 / a candle, an empty chair** — Motion: slow push
`a single candle burning beside an empty chair in a dark room, soft warm flame against deep navy, vigil and dread, intimate and still`

**T-IMG-060 / the debris field found (sonar)** — Motion: push-in
`a sonar screen revealing scattered fragments on a dark seabed near a vast wreck, the cold confirmation, green glow dimming, the search ending`

---

## 5. THE TRUTH (52:00–58:00) — near-black（真実・無音）

**T-IMG-061 / debris near the Titanic** — Motion: very slow drift
`scattered pale fragments of wreckage resting on a silty dark seabed within sight of the towering ghostly hull of a sunken liner, cold blue gloom, profound silence`

**T-IMG-062 / implosion as collapsing light (NOT gore)** — Motion: snap-in then black
`abstract: a sphere of blue light violently collapsing inward to a single point in black water, no debris no bodies, instantaneous and silent, conceptual, restrained`

**T-IMG-063 / pressure, the unforgiving physics** — Motion: push-in
`abstract immense converging force compressing a dark void to a point, deep blue energy lines, the physics that does not negotiate, clean and cold`

**T-IMG-064 / they died on day one (time reversed)** — Motion: hold
`a countdown clock frozen at zero in cold light, dust settled on it, the cruel truth that time had already run out, still and final`

**T-IMG-065 / the warnings echo** — Motion: montage drift
`a faint overlapping collage of formal documents and warning letters fading in dark space, unreadable, the chorus of ignored voices, blue gloom, no legible text`

**T-IMG-066 / the Rubik's cube returns** — Motion: very slow push
`a single Rubik's cube resting alone in cold blue darkness, soft rim light catching its edges, unbearable tenderness, the boy who was nineteen, shallow focus`

**T-IMG-067 / Mr. Titanic's hands, stilled** — Motion: hold
`weathered elderly hands resting open and still in cold blue light near a faint rusted railing, a lifetime returned to the deep, reverent, no face`

**T-IMG-068 / five empty chairs** — Motion: slow dolly
`five empty chairs arranged in a cold dark void under a single soft light, absence made visible, no people, mournful and clean`

**T-IMG-069 / the waiver, 'death' three times** — Motion: macro push
`a legal waiver page in cold raking light with three faint ink-circled blank zones down the page, the rest blurred, grim irony, no readable text`

**T-IMG-070 / the man who said it** — Motion: slow push
`a lone backlit silhouette dissolving into deep shadow, a faint cold rim light, certainty undone, tragic and human, no face`

---

## 6. CODA (58:00–60:00) — dawn, indifferent（余韻）

**T-IMG-071 / the mother at the window** — Motion: very slow push
`a lone female silhouette standing at a tall window at pale dawn looking out to a distant calm sea, soft grey-gold light, grief and endurance, no face`

**T-IMG-072 / the Titanic bow, 111 years** — Motion: Ken Burns in
`the ghostly bow of the sunken liner in cold blue gloom, encrusted and eternal, a monument to a century of the same hubris, reverent and still`

**T-IMG-073 / two wrecks in the gloom (symbolic)** — Motion: very slow drift
`a vast ancient sunken hull and, faintly nearby, a small scattered debris field on the dark seabed, two monuments to the same lesson, cold blue, silent`

**T-IMG-074 / the indifferent sea at dawn** — Motion: slow rise
`a vast calm ocean at first light, soft gold breaking over endless navy water, utterly serene and indifferent, the sea that always wins, lonely beauty`

**T-IMG-075 / one shaft of light** — Motion: descend
`a single pale shaft of dawn light penetrating just below a calm ocean surface and fading into deep blue, fragile and hopeful and final`

**T-IMG-076 / final black plate** — Motion: hold
`an almost pure black frame with the faintest residual blue glow at the lower edge, total stillness, space for a closing line, the end`

---

## 補遺：意味グラフィック（Remotion code側＝SDXL不要）
- 深度ゲージ 0→3,800m と Titanic 深度の対照アニメ
- 96:00:00 → 00:00:00 カウントダウン（最後に「Day 1で既に0」と反転）
- 警告タイムライン（2018 …）
- 「炭素繊維 × 水圧」疲労破壊の1枚図解
これらはコードで生成（T-IMGには含めない）。

---

## カット総数・運用
- **SDXL生成 76カット**（T-IMG-001〜076）。各6 variations → 概算 **456枚生成 → QC採用 ~90–120枚**（章内で複数画像カッティング想定、ImageShotで~4.5s毎差し替え）。
- factory b-roll（ink_in_water / ocean / sonar 等）と**三層**で重ねる（DESIGN_BIBLE §4）。
- 生成→`pd-generate-assets`でQC→usableのみ manifest登録（hash/sourceTool=sdxl/license=generated, disclosure必須・実物提示禁止）。
- 採用後、`shotlist.v001.json` の各spanへ割当（Claude左工程で確定）→ Codexが `TitanFeature` composition に配線。
