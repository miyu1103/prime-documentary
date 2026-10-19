# サムネ ヒーローショット & タイトル — EP77〜EP82 ＋ EP35再作成（Codex生成用）

ステータス: 設計。**Codexアプリで下のヒーロープレートを生成 → オーナーが各話1枚選択 → `ThumbnailFrame` / `ThumbConcept` でタイトルを重ねて 1280×720 書き出し。**

**保存先**: `E:\pd-media\05_visuals\thumbs\<slug>\` にファイル名 `THUMB-01.png`〜。
（**`H:\pd-media` は死んでいます。** 2026-08-17 に `config/storage.local.json` が `E:\pd-media` へ張り替え済み。古い設計書の H: パスをそのまま使わないこと）

**全プレート共通の絶対条件**
- **文字を画像に入れない。** タイトルは Remotion 側で重ねる。AI が描いた文字は必ず崩れる
- **実在人物の肖像を出さない**（`CLAUDE.md` 不変条件11）。人体は匿名のシルエット・手・後ろ姿まで
- **読める書類・判決文・新聞・警察文書を生成しない**（不変条件11）。書類を写す場合は必ず白紙か、文字が解像しない距離で
- **死者・遺体・被災者の苦痛を写さない。** この6話は全部、人が死んだ事故です。**事故の瞬間も惨状も出しません**
- 16:9・最高画質・**片側に大きな暗い余白**（そこへ文字が乗る）

---

## 0. なぜこの形なのか（実測 2026-08-23）

出荷済みサムネ59本を動画IDとCTRに突き合わせて測りました。

**明るさやコントラスト単体では説明できません**（暗い面積 r=+0.19 / 平均輝度 r=−0.18 / コントラスト r=−0.12）。
**強いのは両端の絵の作りです。**

| | CTR | 実際の画 |
|---|---|---|
| `016-titan` | **3.14 %** | 黒地・文字は2行だけ・潜水艇のシルエット1つ |
| `017-onecoin` | **3.71 %** | 黒と金・短い3行・**穴の空いたコイン**＝物そのものが矛盾 |
| `035-hinders` | **1.00 %**（表示 **7,436**） | 文字要素**5つが重なる**。縮小すると灰色の塊。**チャンネル最大の取りこぼし** |
| `047-atwater` | **0.39 %** | 裁判所ドームの**きれいな写真**。縮小すると「紫の建物」 |
| `015-theranos` | **0.00 %** | 明るい灰色地・要素5つ・疑問符 |

**したがって守るルール**

1. **物を1つ。シルエットで。その物だけで矛盾が伝わること。**
   説明文が要る物は、選んだ物が間違っています。穴の空いたコインがやったことです
2. **文字は2ブロック。多くて3。重ねない**
3. **文字は片側半分、物は反対側。両方埋めない、両方空けない**
4. **黒地＋アクセント1色**（弱い相関しかないので断定はしません。既定値として使います）
5. **死者数・疑問符・いちばん大きい行のドル記号は入れない**
6. **サムネの文字も `check_packaging_claims.py` の検査対象**（rule 19）。書けない主張は載せない

**候補は各話4案です**（家の標準は6案）。測って分かったのは「物が間違っていると致命的」なので、**関係ない案を増やすより、矛盾を運ぶ物の変奏を4つ**にしました。

---

## ⛔ タイトルは全部「未検証の仮説」です

`config/pd_premise_seeds.v001.json` と同じ扱い。**数字・人名・結末は、一次資料に当たるまで仮置き**です。
台本を書く前に必ず差し替えてください（`CLAUDE.md` 不変条件1）。各話の「要検証」に何を確かめるか書いてあります。

---

# EP78 — 福島第一（2011） · slug `fukushima`

**要検証**: 津波試算の高さと年次／防潮堤の設計高／刑事無罪の判決日と理由／2022年の株主代表訴訟の命令額と被告

**本編タイトル**
- **A（中核）**: `The Study Said the Wave Could Reach Fifteen Metres. Fukushima Was Built for Five.`
- **B（広め）**: `They Filed the Tsunami Study and Built the Wall for Five Metres.`

**サムネ文字**
- 本命: `BUILT FOR` / **`FIVE METRES`**
- 代案: `THE STUDY SAID` / **`FIFTEEN`**

**プレート**
- `THUMB-01.png`
    A long concrete sea wall in silhouette seen from the shore at night, and the crest of a black wave standing higher than the top of the wall behind it, the height difference unmistakable, cold moonlight rim on the concrete edge, vast empty dark negative space on the left for a title, ultra high resolution 8K, masterpiece quality, hyper-detailed, razor-sharp focus, dramatic cinematic key-art lighting, bold high-contrast composition, a single powerful focal subject, deep navy-and-black palette with cold blue and pale gold rim light, photorealistic, volumetric light, shallow depth of field, 16:9 thumbnail hero shot, scroll-stopping. Avoid: no on-screen text, no letters, no watermark, no logo, no identifiable real person, no bodies, no destruction, no fire, no distorted anatomy, no low-resolution.
- `THUMB-02.png`
    A weathered concrete tide-height marker post standing alone on a dark shoreline, the water surface far above the highest mark on the post, no numbers or letters anywhere on the post, cold overcast dawn, vast empty dark negative space on one side for a title, ultra high resolution 8K, masterpiece quality, hyper-detailed, razor-sharp focus, dramatic cinematic key-art lighting, bold high-contrast composition, a single powerful focal subject, deep navy-and-black palette with cold blue rim light, photorealistic, volumetric light, shallow depth of field, 16:9 thumbnail hero shot, scroll-stopping. Avoid: no on-screen text, no letters, no numerals, no watermark, no logo, no identifiable real person, no bodies, no destruction, no low-resolution.
- `THUMB-03.png`
    An empty coastal town street at dusk seen down its centre line, one traffic signal still blinking amber above the deserted road, grass growing through the asphalt, shutters closed, absolutely no people and no vehicles, vast empty dark negative space on the left for a title, ultra high resolution 8K, masterpiece quality, hyper-detailed, razor-sharp focus, dramatic cinematic key-art lighting, bold high-contrast composition, a single powerful focal subject, deep navy-and-black palette with amber and cold blue accents, photorealistic, volumetric light, shallow depth of field, 16:9 thumbnail hero shot, scroll-stopping. Avoid: no on-screen text, no letters, no signage lettering, no watermark, no logo, no identifiable real person, no bodies, no ruins, no low-resolution.
- `THUMB-04.png`
    A closed grey archive box sitting alone on a steel shelf in a dark records room, a single hard shaft of light across its lid, thick dust, the box completely unlabelled and blank, vast empty dark negative space on one side for a title, ultra high resolution 8K, masterpiece quality, hyper-detailed, razor-sharp focus, dramatic cinematic key-art lighting, bold high-contrast composition, a single powerful focal subject, deep navy-and-black palette with pale gold rim light, photorealistic, volumetric light, shallow depth of field, 16:9 thumbnail hero shot, scroll-stopping. Avoid: no on-screen text, no letters, no labels, no readable documents, no watermark, no logo, no identifiable real person, no low-resolution.

---

# EP79 — アラスカ航空261便（2000） · slug `alaska261`

**要検証**: 給油間隔の延長がいつ誰の認可で行われたか／ジャッキスクリューとナットの摩耗の実測値／民事和解の内容

**本編タイトル**
- **A**: `The FAA Approved a Longer Grease Interval. Alaska 261 Flew on the Worn Jackscrew.`
- **B**: `The Airline Asked to Grease It Less Often. The Regulator Said Yes.`

**サムネ文字**
- 本命: `APPROVED` / **`LONGER`**
- 代案: `LESS OFTEN` / **`APPROVED`**

**プレート**
- `THUMB-01.png`
    Extreme macro of a large steel acme-threaded jackscrew lying on black velvet, the threads crisp and sharp at one end and worn completely smooth and rounded at the other end so the difference is obvious at a glance, a thin gold rim light tracing the metal, vast empty black negative space on the left for a title, ultra high resolution 8K, masterpiece quality, hyper-detailed, razor-sharp focus, dramatic cinematic key-art lighting, bold high-contrast composition, a single powerful focal subject, deep black palette with cold steel-blue and gold rim light, photorealistic, volumetric light, shallow depth of field, 16:9 thumbnail hero shot, scroll-stopping. Avoid: no on-screen text, no letters, no watermark, no logo, no identifiable real person, no aircraft in distress, no wreckage, no low-resolution.
- `THUMB-02.png`
    A single grease gun standing upright on the oil-stained concrete floor of a vast empty aircraft hangar at night, one work lamp above it, the hangar disappearing into blackness behind, vast empty dark negative space on one side for a title, ultra high resolution 8K, masterpiece quality, hyper-detailed, razor-sharp focus, dramatic cinematic key-art lighting, bold high-contrast composition, a single powerful focal subject, deep navy-and-black palette with warm work-lamp light and cold blue fill, photorealistic, volumetric light, shallow depth of field, 16:9 thumbnail hero shot, scroll-stopping. Avoid: no on-screen text, no letters, no watermark, no logo, no identifiable real person, no wreckage, no low-resolution.
- `THUMB-03.png`
    A blank paper maintenance tag hanging from a wire loop on a heavy machined aircraft component, the tag completely empty and wordless, gently swinging, hard raking sidelight, deep shadow behind, vast empty dark negative space on one side for a title, ultra high resolution 8K, masterpiece quality, hyper-detailed, razor-sharp focus, dramatic cinematic key-art lighting, bold high-contrast composition, a single powerful focal subject, deep black palette with cold steel-blue and pale gold accents, photorealistic, volumetric light, shallow depth of field, 16:9 thumbnail hero shot, scroll-stopping. Avoid: no on-screen text, no letters, no handwriting, no readable documents, no watermark, no logo, no identifiable real person, no low-resolution.
- `THUMB-04.png`
    A cold empty Pacific ocean surface photographed from high altitude at dusk, a single set of concentric ripple rings on otherwise flat water, no boats, no aircraft, no people, absolute stillness, vast empty dark negative space on the left for a title, ultra high resolution 8K, masterpiece quality, hyper-detailed, razor-sharp focus, dramatic cinematic key-art lighting, bold high-contrast composition, a single powerful focal subject, deep navy-and-black palette with a single cold blue highlight, photorealistic, volumetric light, 16:9 thumbnail hero shot, scroll-stopping. Avoid: no on-screen text, no letters, no watermark, no logo, no identifiable real person, no debris, no wreckage, no bodies, no low-resolution.

---

# EP80 — コスタ・コンコルディア（2012） · slug `concordia`

**要検証**: 船長の量刑と確定年／沿岸警備隊の通信の日時と内容／乗客が船内に残っていた時刻との前後関係

**本編タイトル**
- **A**: `The Captain of the Costa Concordia Was Ashore Before His Passengers Were.`
- **B**: `The Coastguard Ordered Him Back Aboard. He Did Not Go.`

**サムネ文字**
- 本命: `HE WAS` / **`ASHORE FIRST`**
- 代案: `GET BACK` / **`ON BOARD`**

**プレート**
- `THUMB-01.png`
    A vast white cruise ship hull lying on its side in shallow water at night, floodlit from the shore, the horizon line kept perfectly level across the frame so the ship itself reads as wrong, cold moonlight, absolutely no people anywhere, vast empty dark negative space on the left for a title, ultra high resolution 8K, masterpiece quality, hyper-detailed, razor-sharp focus, dramatic cinematic key-art lighting, bold high-contrast composition, a single powerful focal subject, deep navy-and-black palette with cold white floodlight and gold shore light, photorealistic, volumetric light, shallow depth of field, 16:9 thumbnail hero shot, scroll-stopping. Avoid: no on-screen text, no letters, no ship name lettering, no watermark, no logo, no identifiable real person, no people in the water, no lifeboats in use, no bodies, no low-resolution.
- `THUMB-02.png`
    The interior of a formal ship dining room tilted about thirty degrees, chairs and glassware sliding across white tablecloths, a chandelier hanging at an impossible angle against the ceiling, warm lamps still lit, absolutely no people, vast empty dark negative space on one side for a title, ultra high resolution 8K, masterpiece quality, hyper-detailed, razor-sharp focus, dramatic cinematic key-art lighting, bold high-contrast composition, a single powerful focal subject, warm gold interior light against deep black shadow, photorealistic, volumetric light, shallow depth of field, 16:9 thumbnail hero shot, scroll-stopping. Avoid: no on-screen text, no letters, no watermark, no logo, no identifiable real person, no panic, no injuries, no bodies, no low-resolution.
- `THUMB-03.png`
    A single empty lifeboat hanging from its davit at a useless sideways angle against a towering steel hull at night, one floodlight raking across it, ropes slack, nobody aboard, vast empty dark negative space on one side for a title, ultra high resolution 8K, masterpiece quality, hyper-detailed, razor-sharp focus, dramatic cinematic key-art lighting, bold high-contrast composition, a single powerful focal subject, deep black palette with cold floodlight and orange hull accent, photorealistic, volumetric light, shallow depth of field, 16:9 thumbnail hero shot, scroll-stopping. Avoid: no on-screen text, no letters, no watermark, no logo, no identifiable real person, no evacuation crowd, no bodies, no low-resolution.
- `THUMB-04.png`
    A darkened ship's bridge seen from behind, one instrument lamp still glowing on the console, the captain's chair empty and turned away, black sea through the forward windows, vast empty dark negative space on one side for a title, ultra high resolution 8K, masterpiece quality, hyper-detailed, razor-sharp focus, dramatic cinematic key-art lighting, bold high-contrast composition, a single powerful focal subject, deep black palette with a single warm instrument glow, photorealistic, volumetric light, shallow depth of field, 16:9 thumbnail hero shot, scroll-stopping. Avoid: no on-screen text, no letters, no readable instrument labels, no watermark, no logo, no identifiable real person, no low-resolution.

---

# EP77 — ボルチモア橋崩落（2024） · slug `keybridge`

> **⚠ この話だけ、2026-08-23 に一次資料で裏取り済みです。** 事実は
> `episodes/_planning/EP77_keybridge_FACTS_LEDGER.v001.md` にあり、台本も書き上がっています。
> 下の案はもう仮説ではなく、**行IDのついた記録**に載っています。

**⛔ 削除した旧案（絶対に使わないこと）**
`The Ship Lost Power Four Times Before It Left Baltimore.` — **これは事実と違います。**
NTSB暫定報告では、停電は**停泊中に2回（3月25日）**と**航行中に2回（3月26日）**。
「出港前に4回」は誤りで、台帳の `forbidden_claims` 7番で永久に禁止しました。

**⚠ 係争中です。** 2026年5月12日に**刑事起訴**が開封されました（被告3者）。**有罪を断定する語は一切使えません。**
司法省自身の言葉：「起訴は単なる告発にすぎない。全被告は有罪が証明されるまで無罪と推定される」。

**本編タイトル**（すべて台帳の行に紐づく）
- **A（本命・台本の題）**: `The Ship Got Its Lights Back Thirty-One Seconds Before the Bridge. Not Its Propeller.` <!-- KB-112 -->
- **B（広め）**: `Sixty-Seven Seconds After the Order to Stop the Traffic, the Bridge Was in the River.` <!-- KB-113, KB-002 -->
- **C（原因を前に出す）**: `A Band of Label on One Wire. Six Men on the Deck at Half Past One.` <!-- KB-203, KB-004 -->

**サムネ文字**
- 本命: `SIX MEN` / **`WERE UP THERE`** <!-- KB-004 -->
- 代案A: `LIGHTS BACK` / **`NOT THE PROPELLER`** <!-- KB-112 -->
- 代案B: `ONE WIRE` / **`ONE LABEL`** <!-- KB-203 -->

**⛔ サムネに載せてはいけない語**: `GUILTY` / `THEY LIED` / `COVER-UP` / 被告の社名・人名。
また**死者数を数字で置かない**（`SIX MEN` は人数ではなく主語として使う。数として強調しない）。

**プレート**
- `THUMB-01.png`
    A single orange traffic cone standing alone on an empty highway bridge deck in the middle of the night, sodium lamps receding into the distance, the steel span vanishing into darkness behind it, wet asphalt reflections, absolutely no people and no vehicles, vast empty dark negative space on the left for a title, ultra high resolution 8K, masterpiece quality, hyper-detailed, razor-sharp focus, dramatic cinematic key-art lighting, bold high-contrast composition, a single powerful focal subject, deep navy-and-black palette with warm sodium orange and cold blue, photorealistic, volumetric light, shallow depth of field, 16:9 thumbnail hero shot, scroll-stopping. Avoid: no on-screen text, no letters, no road signage lettering, no watermark, no logo, no identifiable real person, no ship, no collapse, no low-resolution.
- `THUMB-02.png`
    A worn hard hat resting upside down on a concrete highway barrier at night, one work light throwing a long shadow, the empty road stretching away behind, absolutely no people, vast empty dark negative space on one side for a title, ultra high resolution 8K, masterpiece quality, hyper-detailed, razor-sharp focus, dramatic cinematic key-art lighting, bold high-contrast composition, a single powerful focal subject, deep black palette with warm work light and cold blue fill, photorealistic, volumetric light, shallow depth of field, 16:9 thumbnail hero shot, scroll-stopping. Avoid: no on-screen text, no letters, no watermark, no logo, no identifiable real person, no ship, no collapse, no low-resolution.
- `THUMB-03.png`
    A battered steel thermos flask and a folded work jacket left on a bridge parapet at night, black water far below, harbour lights small and distant on the far shore, nobody present, vast empty dark negative space on one side for a title, ultra high resolution 8K, masterpiece quality, hyper-detailed, razor-sharp focus, dramatic cinematic key-art lighting, bold high-contrast composition, a single powerful focal subject, deep navy-and-black palette with distant warm harbour light, photorealistic, volumetric light, shallow depth of field, 16:9 thumbnail hero shot, scroll-stopping. Avoid: no on-screen text, no letters, no watermark, no logo, no identifiable real person, no ship, no collapse, no low-resolution.
- `THUMB-04.png`
    A steel truss bridge span photographed from water level at night, one pier lit from below and the rest of the structure in silhouette against a starless sky, still black water, no vessels of any kind, vast empty dark negative space on the left for a title, ultra high resolution 8K, masterpiece quality, hyper-detailed, razor-sharp focus, dramatic cinematic key-art lighting, bold high-contrast composition, a single powerful focal subject, deep black palette with a single cold blue-white uplight, photorealistic, volumetric light, 16:9 thumbnail hero shot, scroll-stopping. Avoid: on-screen text, letters, watermark, logo, identifiable real person, ship, impact, collapse, low-resolution.
- `THUMB-05.png`  ← **本命候補。物そのものが矛盾を語る型（OneCoinがやったこと）**
    Extreme macro of an industrial electrical terminal block, one thick insulated wire held just short of its spring-clamp gate because a band of plastic labelling wrapped around the wire is too thick to pass through, the gap between wire and clamp clearly visible, the label band completely blank with no printing on it, hard raking light, everything else falling to pure black, vast empty black negative space on the left for a title, ultra high resolution 8K, masterpiece quality, hyper-detailed, razor-sharp focus, dramatic cinematic key-art lighting, bold high-contrast composition, a single powerful focal subject, deep black palette with cold steel-blue and a thin gold rim, photorealistic, volumetric light, shallow depth of field, 16:9 thumbnail hero shot, scroll-stopping. Avoid: on-screen text, letters, printing on the label, watermark, logo, identifiable real person, ship, bridge, collapse, low-resolution.
    <!-- KB-203。NTSBが認定した機構そのもの：ラベルの帯が邪魔で電線が奥まで入らない。
         これが「穴の空いたコイン」に相当する。説明文なしで矛盾が伝わる唯一の物。 -->
- `THUMB-06.png`
    A ship's engine-room switchboard seen straight on in near darkness, one small green indicator lamp lit among dozens of dark ones, brushed steel panels, no gauges legible, no words or numerals anywhere, vast empty dark negative space on one side for a title, ultra high resolution 8K, masterpiece quality, hyper-detailed, razor-sharp focus, dramatic cinematic key-art lighting, bold high-contrast composition, a single powerful focal subject, deep black palette with one green indicator and a cold steel rim, photorealistic, volumetric light, shallow depth of field, 16:9 thumbnail hero shot, scroll-stopping. Avoid: on-screen text, letters, numerals, readable gauge markings, watermark, logo, identifiable real person, low-resolution.

---

# EP81 — ステーション・ナイトクラブ火災（2003） · slug `station`

**要検証**: 壁と天井に使われた素材と、その難燃認定の有無／有罪判決を受けた人物と罪名と量刑／和解の総額と被告数

**本編タイトル**
- **A**: `The Foam on the Walls Was Not Fire Retardant. The Station Sold Tickets Anyway.`
- **B**: `The Club Bought the Cheaper Foam. Nobody Came to Inspect It.`

**サムネ文字**
- 本命: `NOT FIRE` / **`RETARDANT`**
- 代案: `THE CHEAPER` / **`FOAM`**

**プレート**
- `THUMB-01.png`
    Close macro of grey wedge-profile acoustic foam tiles covering a low ceiling, lit from below by a single hard stage light, one tile peeled back at the corner to expose the bare plywood beneath, dust in the beam, vast empty dark negative space on one side for a title, ultra high resolution 8K, masterpiece quality, hyper-detailed, razor-sharp focus, dramatic cinematic key-art lighting, bold high-contrast composition, a single powerful focal subject, deep black palette with one cold white beam and a warm amber edge, photorealistic, volumetric light, shallow depth of field, 16:9 thumbnail hero shot, scroll-stopping. Avoid: no on-screen text, no letters, no watermark, no logo, no identifiable real person, no fire, no flames, no smoke, no crowd, no low-resolution.
- `THUMB-02.png`
    A single black stage monitor speaker sitting alone on the empty plywood stage of a small club, one narrow spotlight on it, the room beyond completely dark and empty, cables coiled on the floor, absolutely no people, vast empty dark negative space on one side for a title, ultra high resolution 8K, masterpiece quality, hyper-detailed, razor-sharp focus, dramatic cinematic key-art lighting, bold high-contrast composition, a single powerful focal subject, deep black palette with one warm spotlight, photorealistic, volumetric light, shallow depth of field, 16:9 thumbnail hero shot, scroll-stopping. Avoid: no on-screen text, no letters, no band names, no watermark, no logo, no identifiable real person, no fire, no crowd, no low-resolution.
- `THUMB-03.png`
    A wall of black acoustic foam behind an empty microphone stand in a small dark venue, hard side light raking across the foam texture, no performer, no audience, vast empty dark negative space on the left for a title, ultra high resolution 8K, masterpiece quality, hyper-detailed, razor-sharp focus, dramatic cinematic key-art lighting, bold high-contrast composition, a single powerful focal subject, deep black palette with a single cold white rim, photorealistic, volumetric light, shallow depth of field, 16:9 thumbnail hero shot, scroll-stopping. Avoid: no on-screen text, no letters, no watermark, no logo, no identifiable real person, no fire, no smoke, no crowd, no low-resolution.
- `THUMB-04.png`
    A glowing green running-man emergency exit pictogram sign above a narrow dark corridor, the corridor stretching away into blackness, no words anywhere on the sign, only the pictogram, empty and silent, vast empty dark negative space on one side for a title, ultra high resolution 8K, masterpiece quality, hyper-detailed, razor-sharp focus, dramatic cinematic key-art lighting, bold high-contrast composition, a single powerful focal subject, deep black palette with a single green sign glow, photorealistic, volumetric light, shallow depth of field, 16:9 thumbnail hero shot, scroll-stopping. Avoid: no on-screen text, no letters, no words on the sign, no watermark, no logo, no identifiable real person, no fire, no smoke, no crowd, no low-resolution.

---

# EP82 — エクソン・バルディーズ（1989） · slug `valdez`

**要検証**: 流出対応計画が約束していた資機材の到着時間／実際に到着した時間／陪審の懲罰賠償額と最高裁の減額後の額と年

**本編タイトル**
- **A**: `The Spill Plan Promised Barges in Five Hours. Exxon Valdez Waited Fourteen.`
- **B**: `A Jury Set the Punishment. Nineteen Years Later the Supreme Court Cut It.`

**サムネ文字**
- 本命: `FIVE HOURS` / **`FOURTEEN`**
- 代案: `NINETEEN YEARS` / **`LATER`**

**プレート**
- `THUMB-01.png`
    A gloved hand holding a single fist-sized beach stone completely coated in glossy black oil, cold grey Alaskan daylight, thick black drips running off the stone, the background falling to pure black, only the hand and forearm visible and no face, vast empty dark negative space on the left for a title, ultra high resolution 8K, masterpiece quality, hyper-detailed, razor-sharp focus, dramatic cinematic key-art lighting, bold high-contrast composition, a single powerful focal subject, deep black palette with cold grey daylight and a faint amber rim, photorealistic, volumetric light, shallow depth of field, 16:9 thumbnail hero shot, scroll-stopping. Avoid: no on-screen text, no letters, no watermark, no logo, no identifiable real person, no face, no oiled wildlife, no animals, no low-resolution.
- `THUMB-02.png`
    Rows of coiled orange oil containment boom stacked and forgotten in a dark unheated warehouse, snow drifted in through a half-open roller door, cold blue daylight cutting one hard shaft across the coils, absolutely no people, vast empty dark negative space on one side for a title, ultra high resolution 8K, masterpiece quality, hyper-detailed, razor-sharp focus, dramatic cinematic key-art lighting, bold high-contrast composition, a single powerful focal subject, deep black palette with cold blue daylight and orange boom accent, photorealistic, volumetric light, shallow depth of field, 16:9 thumbnail hero shot, scroll-stopping. Avoid: no on-screen text, no letters, no watermark, no logo, no identifiable real person, no low-resolution.
- `THUMB-03.png`
    A shoreline of grey rounded cobbles at low tide where the upper half of every stone is coated glossy black and the lower half is still clean grey, the tide line drawn perfectly straight across the frame, overcast Alaskan light, no people and no animals, vast empty dark negative space on one side for a title, ultra high resolution 8K, masterpiece quality, hyper-detailed, razor-sharp focus, dramatic cinematic key-art lighting, bold high-contrast composition, a single powerful focal subject, deep black and cold grey palette, photorealistic, volumetric light, shallow depth of field, 16:9 thumbnail hero shot, scroll-stopping. Avoid: no on-screen text, no letters, no watermark, no logo, no identifiable real person, no wildlife, no low-resolution.
- `THUMB-04.png`
    An empty herring net hanging slack in a cold dark boat shed, one shaft of grey light through a dusty window, coiled rope and an unused float on the plank floor, absolutely no people, vast empty dark negative space on the left for a title, ultra high resolution 8K, masterpiece quality, hyper-detailed, razor-sharp focus, dramatic cinematic key-art lighting, bold high-contrast composition, a single powerful focal subject, deep black palette with cold grey window light, photorealistic, volumetric light, shallow depth of field, 16:9 thumbnail hero shot, scroll-stopping. Avoid: no on-screen text, no letters, no watermark, no logo, no identifiable real person, no low-resolution.

---

# 【最優先・単独】EP35 hinders のサムネ作り直し · slug `hinders`

**これは新作ではありません。既に公開中の動画です。**

`035-hinders` は **28日間で 7,436 回表示され、チャンネル最大**です。YouTube は既に客を送っています。
それを **CTR 1.00 %** で捨てています。上位並みの 3 % に届けば **約150クリックの差**。
**画像1枚の作り直しが、いま最も安く測れる改善**です。

**いまの画がなぜ落ちているか（実測）**: 文字要素が **5つ**あり、`$32,820` と `SEIZED BY` が**物理的に重なり**、
その上に斜めの `NO CRIME.` シールが乗っています。背景のレジは判別できません。**縮小すると灰色の塊**です。

**⚠ 8/10のタイトル実験（判定日 2026-09-07）の対照13本には入っていないので、触っても実験は壊れません。**
ただし**タイトルは変えないでください**。変えるのは画像だけ。それで初めて「サムネ単独の効果」が測れます。

**サムネ文字（2ブロックに減らす）**
- 本命: `NO CRIME` / **`NO CHARGE`**
- 代案: `SHE BROKE` / **`NO LAW`**

**プレート**
- `THUMB-01.png`
    A single small steel cash drawer standing open and completely empty on a dark wooden counter, one hard overhead light, deep shadow filling the rest of the frame, no money, no papers, no people, vast empty black negative space on the left for a title, ultra high resolution 8K, masterpiece quality, hyper-detailed, razor-sharp focus, dramatic cinematic key-art lighting, bold high-contrast composition, a single powerful focal subject, deep black palette with a single warm overhead light and a cold blue edge, photorealistic, volumetric light, shallow depth of field, 16:9 thumbnail hero shot, scroll-stopping. Avoid: no on-screen text, no letters, no numerals, no banknote denominations, no watermark, no logo, no identifiable real person, no low-resolution.
- `THUMB-02.png`
    A neat stack of blank white deposit envelopes on a dark counter with one envelope pulled slightly out of the middle of the stack, completely unmarked and wordless, hard raking sidelight, the background falling to pure black, vast empty black negative space on one side for a title, ultra high resolution 8K, masterpiece quality, hyper-detailed, razor-sharp focus, dramatic cinematic key-art lighting, bold high-contrast composition, a single powerful focal subject, deep black palette with a pale gold rim light, photorealistic, volumetric light, shallow depth of field, 16:9 thumbnail hero shot, scroll-stopping. Avoid: no on-screen text, no letters, no printing on the envelopes, no readable documents, no watermark, no logo, no identifiable real person, no low-resolution.
- `THUMB-03.png`
    A dark closed roller shutter over a small shop front at night seen straight on, one street lamp above throwing a hard pool of light on the empty pavement, no signage lettering anywhere, no people, vast empty dark negative space on one side for a title, ultra high resolution 8K, masterpiece quality, hyper-detailed, razor-sharp focus, dramatic cinematic key-art lighting, bold high-contrast composition, a single powerful focal subject, deep navy-and-black palette with one warm sodium light, photorealistic, volumetric light, shallow depth of field, 16:9 thumbnail hero shot, scroll-stopping. Avoid: no on-screen text, no letters, no shop signage, no watermark, no logo, no identifiable real person, no low-resolution.

---

# 生成後の手順

1. **オーナーが各話1枚選ぶ**（title/thumbnail のペアは人間承認境界・`.claude/rules/16`）
2. `remotion/src/components/ThumbnailFrame.tsx` か `remotion/src/compositions/ThumbConcept.tsx` に
   `backgroundSrc` として渡し、**文字は2ブロックだけ**乗せて 1280×720 で `<Still>` 書き出し
3. `py -3.11 scripts/check_packaging_claims.py --slug <slug>` を通す
   （**サムネの文字も検査対象**。台本に無い主張は落ちます）
4. **縮小して確認する。** 168×94 px に落として、1秒で「何の物か」「何が矛盾か」が分かるか。
   分からなければ物が間違っています。プレートを選び直してください

# 未確定点

- **本編タイトル・サムネ文字はすべて未検証**です。各話の「要検証」を一次資料で埋めてから確定してください
- EP80 は**係争中**。当事者の過失を断定する文言は使えません
- 明るさ・コントラストとCTRの相関は**弱い（|r| ≤ 0.19）**。黒地は既定値であって、証明された勝ち筋ではありません
- **2026-09-07 まで、公開済み動画のサムネを一括で変えないでください。** タイトル実験と混ざります。
  EP35 hinders の1本だけは対照群外なので例外として先行できます
