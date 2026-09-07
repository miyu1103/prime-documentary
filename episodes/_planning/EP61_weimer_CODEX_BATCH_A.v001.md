# EP61 weimer — Codex 画像生成 **1本で完結する発注** v001（150枚・1プロンプト1枚）

> ## ✅ 今すぐ着手してよいファイルです。**追加バッチは出ません。**
> EP60はバッチが5本に膨らみました。原因は3つとも同じで、**発注時点で構造が決まって
> いなかった**ことです（顔の可否が未決／第1・2幕に専用の絵が無い／実写の測定が発注より後）。
> 今回は逆順にしました。**実写を先に測り（288タイル目視、使えるのは87本）、30分を8区分に
> 割り切り、区分ごとにカット数と枚数を確定させてから**この発注を書いています。
> **どの区分にも絵があります。**下の表がその証明です。

**題材:** クリスタル・ワイマー。ペンシルベニア州フェイエット郡で、やっていない殺人により
**11年以上**服役した女性。有罪判決は破棄され、全訴因が再訴不可で取り下げられた。

**この映画は法廷ドラマではありません。**主題は建物でも制度でもなく、**彼女抜きで過ぎた11年**です。

---

## 0. ★★★ 最重要：1プロンプト = 1枚 ★★★

1. **各プロンプトから画像を1枚だけ作る。** 同じプロンプトで2枚目を作らない。
2. **`_02` / `_03` を作らない。**
3. **「良いのが出るまで回す」を禁止。**
4. 作り直してよいのは §1 の禁止に触れたときだけ。そのときも**文言を直してから1枚**。

EP60はこの規則で **279枚・変種0・指定外0・sha256重複0・知覚的近似重複0** を達成済み。

---

## 1. ★絶対条件（触れた絵は使用不可）

- **事件そのものを描かない。** 遺体・銃・傷・血・現場・規制線・検視。**一切。**
- **歯型・咬み跡・歯科模型を人体と結び付けて描かない。** 被害者の傷なので。
  （石膏模型を器材として置く絵は §4 の指定どおりなら可。歯の形状が判別できる寄りは不可）
- **実在の7人を描かない。** クリスタル・ワイマー本人、元地方検事、情報提供者、元交際相手、
  被害者、歯科医、鑑定人。**人物は全員「実在しない一般人」として描く。**
- **監獄を描かない。** 鉄格子・有刺鉄線・監視塔・独房・手錠。**この映画は刑務所を映しません。**
- **法廷を描かない。** 法廷内観・木槌・判事席。
- **読める文字・数字・署名・印章・ロゴを描かない。**
- **広告調にしない。** 黄金色の夕陽、絵葉書の風景、クリスマス、南国、砂漠、桜、ドローンの映え。
- **黒つぶれさせない。** スマホで見て何が写っているか分かること。

### 生成後のチェック（1枚ずつ目視）

| # | 不合格条件 |
|---|---|
| Q1 | 長辺が3840px未満 |
| Q2 | 読める文字・数字・署名がある |
| Q3 | 印章・紋章・ロゴらしきものがある |
| Q4 | 鉄格子・有刺鉄線・手錠・法廷が写っている |
| Q5 | 遺体・血・銃・傷・現場が写っている |
| Q6 | 既存の他話の画像と実質同じ構図 |
| Q7 | 広告調（黄金色の映え・絵葉書・南国）である |
| Q8 | 画面全体が暗すぎる |

---

## 2. スタイル（★必ず展開してから生成）

**`[STYLE]`** ＝ 末尾にそのまま連結:

> , cinematic still, muted natural colour, overcast western Pennsylvania light, low contrast, low-key but never crushed: shadows keep their detail and the frame reads clearly on a phone screen, soft falloff toward the edges, shallow depth of field, restrained documentary framing, nothing staged for advertising, ultra-detailed, photoreal, 4K, 16:9, fine film grain, no text, no lettering, no numerals, no watermark, no logo, no signage

**`[NEG]`** ＝ `Avoid:` の後にそのまま連結:

> readable text, letterforms, numerals, signage, captions, watermarks, logos, seals, emblems, portraits of real people, prison bars, razor wire, barbed wire, watchtower, cell door, handcuffs, courtroom interior, gavel, judge's bench, police tape, evidence markers, guns, wounds, blood, a body, a bite mark, teeth impressions, dental casts, autopsy, mortuary, festive decoration, Christmas, golden-hour advertising glow, postcard scenery, waterfall, mountain grandeur, tropical, desert, cherry blossom, drone hero shot, crushed blacks, underexposed, pitch dark, cartoon, illustration, painterly, oversaturated, HDR halo, 3D render, CGI

1枚目で展開されているか必ず目視確認すること。

---

## 3. 出力

- 出力先: `H:\pd-media\assets\ai\weimer\`
- **W001.png 〜 W150.png（150枚・3840×2160）**

---

## 4. 区分ごとの割り当て（これが「追加が出ない」証明）

| 区分 | 時間 | 秒 | 枚数 | 何の場面か |
|---|---|---|---|---|
| HOOK | 0:00–0:45 | 45 | **8** | 掴み。1月の夜、そして「11年」という数字。 |
| OP | 0:45–1:10 | 25 | **4** | ブランド。 |
| ACT_1 | 1:10–6:30 | 320 | **22** | 2001年1月、フェイエット郡。彼女が誰で、どんな町だったか。 |
| ACT_2 | 6:30–12:00 | 330 | **24** | 捜査。20か月なにも起きず、そして元交際相手が現れる。 |
| ACT_3 | 12:00–18:00 | 360 | **26** | 歯型。専門家が意見を書き換える。 |
| ACT_4 | 18:00–24:00 | 360 | **40** | 11年。季節が11回来て、彼女はそこにいない。 |
| ACT_5 | 24:00–28:00 | 240 | **18** | ほどける。有罪破棄、訴因取り下げ。 |
| ENDING | 28:00–30:00 | 120 | **8** | 残ったもの。 |
| | | **1800** | **150** | |

実写で埋まるのは約60〜87カット。30分は約390カット（13カット/分）。
残りをこの150枚と figure beats が担います。**区分に穴はありません。**

---

## 5. プロンプト（各1枚）

### HOOK（0:00–0:45・8枚） — 掴み。1月の夜、そして「11年」という数字。

- `W001.png`
A two-lane road running into a small American town before dawn in January, wet tarmac, bare trees on both sides, no vehicles [STYLE] Avoid: [NEG]
- `W002.png`
A modest wooden house on an ordinary street at night, one window lit, snow lying thin on the yard [STYLE] Avoid: [NEG]
- `W003.png`
An empty pavement outside a low apartment building in winter darkness, a single streetlamp, nothing else [STYLE] Avoid: [NEG]
- `W004.png`
A kitchen table in a plain house at night, a mug and a set of keys on it, nobody there [STYLE] Avoid: [NEG]
- `W005.png`
A calendar page on a kitchen wall, the grid blank and unreadable, morning light across it [STYLE] Avoid: [NEG]
- `W006.png`
The same two-lane road in high summer, full green on both sides, empty [STYLE] Avoid: [NEG]
- `W007.png`
The same two-lane road under deep snow, tyre tracks already there, empty [STYLE] Avoid: [NEG]
- `W008.png`
The same two-lane road in bare late autumn, brown leaves at the verge, empty [STYLE] Avoid: [NEG]

### OP（0:45–1:10・4枚） — ブランド。

- `W009.png`
A bare deciduous treeline against a flat white overcast sky, no landmark, no horizon feature [STYLE] Avoid: [NEG]
- `W010.png`
Frost on rough winter grass at ground level, morning, no colour [STYLE] Avoid: [NEG]
- `W011.png`
A plain grey sky filling the frame with one power line crossing it [STYLE] Avoid: [NEG]
- `W012.png`
Cold water moving over stones in a shallow creek, no bank visible, no sky [STYLE] Avoid: [NEG]

### ACT_1（1:10–6:30・22枚） — 2001年1月、フェイエット郡。彼女が誰で、どんな町だったか。

- `W013.png`
A small Pennsylvania town seen from a hillside on an overcast morning, low brick buildings, church spire, wooded ridges behind [STYLE] Avoid: [NEG]
- `W014.png`
A residential street of modest houses with porches, parked cars, power lines overhead, nobody about [STYLE] Avoid: [NEG]
- `W015.png`
A worn wooden front porch with two chairs on it, paint flaking, seen from the yard [STYLE] Avoid: [NEG]
- `W016.png`
A kitchen in a plain house, dishes stacked by the sink, ordinary and untidy, no people [STYLE] Avoid: [NEG]
- `W017.png`
A child's bicycle left lying on its side on a patch of grass beside a driveway [STYLE] Avoid: [NEG]
- `W018.png`
A row of mailboxes on posts at the roadside of a rural street, plain metal, doors shut [STYLE] Avoid: [NEG]
- `W019.png`
The inside of a modest car at night from the back seat, dashboard glow, empty seats [STYLE] Avoid: [NEG]
- `W020.png`
A low brick apartment building at night with a concrete stoop and a bare bulb over the door [STYLE] Avoid: [NEG]
- `W021.png`
An ordinary living room lit only by a television that is off, curtains drawn [STYLE] Avoid: [NEG]
- `W022.png`
A narrow back lane between two houses in winter, chain-link on one side, no snow yet [STYLE] Avoid: [NEG]
- `W023.png`
A woman in her twenties in a plain coat standing at a bus stop shelter at dusk, seen from behind, face not visible [STYLE] Avoid: [NEG]
- `W024.png`
The hands of a young woman holding a paper coffee cup on a doorstep in cold weather, no face in frame [STYLE] Avoid: [NEG]
- `W025.png`
A dog on a chain in a bare backyard looking toward the house, plain daylight [STYLE] Avoid: [NEG]
- `W026.png`
A pickup truck parked on a gravel drive beside a house, mud on the wheel arches [STYLE] Avoid: [NEG]
- `W027.png`
A closed screen door of a modest house, the interior beyond it dark [STYLE] Avoid: [NEG]
- `W028.png`
Winter sunrise over a small town from a distance, the light thin and colourless [STYLE] Avoid: [NEG]
- `W029.png`
An empty parking area outside a small commercial building, cracked asphalt, weeds at the edge [STYLE] Avoid: [NEG]
- `W030.png`
A telephone pole with many staples and old fixings on it, close, plain daylight [STYLE] Avoid: [NEG]
- `W031.png`
A woman in her twenties sitting alone on porch steps at night, seen from behind, shoulders only [STYLE] Avoid: [NEG]
- `W032.png`
A hallway of a modest home at night with one door ajar and a light on beyond it [STYLE] Avoid: [NEG]
- `W033.png`
A patch of muddy ground beside a driveway with tyre ruts filled with water [STYLE] Avoid: [NEG]
- `W034.png`
A plain American church exterior in a small town, clapboard and a modest steeple, overcast, no people [STYLE] Avoid: [NEG]

### ACT_2（6:30–12:00・24枚） — 捜査。20か月なにも起きず、そして元交際相手が現れる。

- `W035.png`
A police cruiser parked on a residential street at first light, seen from a distance, no markings legible [STYLE] Avoid: [NEG]
- `W036.png`
An officer's gloved hands lifting a plain paper evidence bag on a table, no face, no writing on the bag [STYLE] Avoid: [NEG]
- `W037.png`
A swab being sealed into a small plastic tube on a laboratory bench, hands only, no labels [STYLE] Avoid: [NEG]
- `W038.png`
A laboratory bench with a rack of unmarked sample tubes under cold overhead light [STYLE] Avoid: [NEG]
- `W039.png`
A plain interview room with two chairs and a table, empty, institutional grey-green walls [STYLE] Avoid: [NEG]
- `W040.png`
The corner of an interview room table with a paper cup and an ashtray on it, nobody there [STYLE] Avoid: [NEG]
- `W041.png`
A wall clock in a bare institutional room, the face blank and unreadable [STYLE] Avoid: [NEG]
- `W042.png`
A stack of manila folders on a metal desk under a lamp, no writing visible [STYLE] Avoid: [NEG]
- `W043.png`
A woman in her twenties sitting on a plain chair in a bare room, hands in her lap, seen from behind [STYLE] Avoid: [NEG]
- `W044.png`
A man in his thirties in a plain shirt seen from behind in a bare corridor, face not visible [STYLE] Avoid: [NEG]
- `W045.png`
A cassette recorder on a table beside a notepad, close, plain daylight, nothing written [STYLE] Avoid: [NEG]
- `W046.png`
A window of a small police station at night from the street, blinds half shut, light on [STYLE] Avoid: [NEG]
- `W047.png`
An empty desk chair pushed back from a desk in a dim office [STYLE] Avoid: [NEG]
- `W048.png`
A cigarette burning down in an ashtray on a windowsill, grey daylight outside [STYLE] Avoid: [NEG]
- `W049.png`
A yard behind a low municipal building with a chain-link gate standing open [STYLE] Avoid: [NEG]
- `W050.png`
A calendar on an office wall with several months' pages turned back, all blank [STYLE] Avoid: [NEG]
- `W051.png`
A payphone on a brick wall outside a small-town store, receiver on the hook [STYLE] Avoid: [NEG]
- `W052.png`
A man in his thirties sitting in a parked car at night looking straight ahead, face in shadow, unreadable [STYLE] Avoid: [NEG]
- `W053.png`
Two plain chairs facing each other across a table in an empty room, one pushed back [STYLE] Avoid: [NEG]
- `W054.png`
A filing drawer half open showing the tops of unlabelled dividers [STYLE] Avoid: [NEG]
- `W055.png`
A road at night seen through a rain-streaked windscreen from inside a stationary car [STYLE] Avoid: [NEG]
- `W056.png`
A single sheet of paper face down on a desk under a lamp [STYLE] Avoid: [NEG]
- `W057.png`
A hand signing at the bottom of a form, only the hand and pen visible, the writing illegible [STYLE] Avoid: [NEG]
- `W058.png`
The exterior of a small county courthouse at dusk, plain and unremarkable, no signage legible [STYLE] Avoid: [NEG]

### ACT_3（12:00–18:00・26枚） — 歯型。専門家が意見を書き換える。

- `W059.png`
A dental plaster cast of an upper jaw sitting on a plain bench under cold light, seen at an oblique angle, no teeth detail resolved [STYLE] Avoid: [NEG]
- `W060.png`
A pair of calipers lying open on a plain white bench, close, cold light [STYLE] Avoid: [NEG]
- `W061.png`
A photographic light box on a wall with a blank illuminated panel, nothing on it [STYLE] Avoid: [NEG]
- `W062.png`
A magnifying lens on an articulated arm over an empty bench [STYLE] Avoid: [NEG]
- `W063.png`
A ruled scale bar lying alone on a plain surface, the markings not resolvable [STYLE] Avoid: [NEG]
- `W064.png`
A stack of photographic prints face down on a desk beside a lamp [STYLE] Avoid: [NEG]
- `W065.png`
A slide projector in a dark room throwing a blank white rectangle onto a wall [STYLE] Avoid: [NEG]
- `W066.png`
An overhead view of an empty examination table under a surgical lamp, plain and unused [STYLE] Avoid: [NEG]
- `W067.png`
A microscope on a bench with nobody at it, cold overhead light [STYLE] Avoid: [NEG]
- `W068.png`
A man in his fifties in a plain shirt seated at a bench with his back to the camera, writing, face not visible [STYLE] Avoid: [NEG]
- `W069.png`
A telephone handset lying off its cradle on a desk, cord hanging [STYLE] Avoid: [NEG]
- `W070.png`
A wall of institutional cabinets with all drawers shut, flat lighting [STYLE] Avoid: [NEG]
- `W071.png`
A single page being turned on a clipboard, hands only, the writing illegible [STYLE] Avoid: [NEG]
- `W072.png`
An empty lecture chair in a bare room with a bench in front of it [STYLE] Avoid: [NEG]
- `W073.png`
A window in an institutional corridor with a view of a car park in the rain [STYLE] Avoid: [NEG]
- `W074.png`
A gloved hand adjusting an anglepoise lamp over a bench, no face [STYLE] Avoid: [NEG]
- `W075.png`
A row of grey lockers in a plain institutional corridor [STYLE] Avoid: [NEG]
- `W076.png`
A desk diary open to a blank double page, pen resting in the gutter [STYLE] Avoid: [NEG]
- `W077.png`
A tape measure extended across a plain bench and left there [STYLE] Avoid: [NEG]
- `W078.png`
The back of a man in a jacket walking away down an institutional corridor, face not visible [STYLE] Avoid: [NEG]
- `W079.png`
A photocopier in a dim office with its lid raised over an empty glass [STYLE] Avoid: [NEG]
- `W080.png`
A whiteboard wiped clean with faint ghost marks, plain room [STYLE] Avoid: [NEG]
- `W081.png`
A pair of reading glasses folded on a closed folder [STYLE] Avoid: [NEG]
- `W082.png`
A wall-mounted viewing screen switched off in an empty room [STYLE] Avoid: [NEG]
- `W083.png`
A chair at the end of a long empty table in a plain meeting room [STYLE] Avoid: [NEG]
- `W084.png`
A corridor door with a small square observation window, closed, institutional [STYLE] Avoid: [NEG]

### ACT_4（18:00–24:00・40枚） — 11年。季節が11回来て、彼女はそこにいない。

- `W085.png`
Meltwater running along a roadside gutter through dirty snow, close, grey daylight [STYLE] Avoid: [NEG]
- `W086.png`
A rutted dirt track with mud and standing water between bare fields [STYLE] Avoid: [NEG]
- `W087.png`
The first green shoots pushing through brown winter grass, close, overcast [STYLE] Avoid: [NEG]
- `W088.png`
A bare deciduous tree in a field beginning to bud, flat grey sky [STYLE] Avoid: [NEG]
- `W089.png`
The same field in full summer green under heavy cloud [STYLE] Avoid: [NEG]
- `W090.png`
The same field cut and stubbled in late summer [STYLE] Avoid: [NEG]
- `W091.png`
The same field ploughed brown in autumn, low sun behind cloud [STYLE] Avoid: [NEG]
- `W092.png`
The same field under first snow, the furrows still showing [STYLE] Avoid: [NEG]
- `W093.png`
A creek running high and brown with meltwater between bare banks [STYLE] Avoid: [NEG]
- `W094.png`
The same creek low and clear in summer with green overhanging [STYLE] Avoid: [NEG]
- `W095.png`
The same creek edged with ice, water dark beneath [STYLE] Avoid: [NEG]
- `W096.png`
A porch with a summer chair on it and the paint further gone than before [STYLE] Avoid: [NEG]
- `W097.png`
The same porch with autumn leaves gathered against the step [STYLE] Avoid: [NEG]
- `W098.png`
The same porch under snow with nothing on it [STYLE] Avoid: [NEG]
- `W099.png`
A residential street in full summer leaf, parked cars, nobody about [STYLE] Avoid: [NEG]
- `W100.png`
The same street in autumn with leaves down and the trees bare [STYLE] Avoid: [NEG]
- `W101.png`
The same street under grey winter light, snow at the kerb [STYLE] Avoid: [NEG]
- `W102.png`
A washing line in a backyard with sheets on it in summer wind [STYLE] Avoid: [NEG]
- `W103.png`
The same washing line bare in winter [STYLE] Avoid: [NEG]
- `W104.png`
A garden gone to weed behind a modest house, late summer [STYLE] Avoid: [NEG]
- `W105.png`
A window of an ordinary house seen from the road at night with the light on inside [STYLE] Avoid: [NEG]
- `W106.png`
The same window dark [STYLE] Avoid: [NEG]
- `W107.png`
A school bus stop sign post at a rural roadside with no bus and no children [STYLE] Avoid: [NEG]
- `W108.png`
A church car park empty on a grey Sunday morning [STYLE] Avoid: [NEG]
- `W109.png`
A cemetery of plain modern headstones on a hillside, overcast, nobody there [STYLE] Avoid: [NEG]
- `W110.png`
A road resurfaced and freshly marked, the markings not forming any letter [STYLE] Avoid: [NEG]
- `W111.png`
A shopfront in a small town with its window papered over from inside [STYLE] Avoid: [NEG]
- `W112.png`
The same shopfront reopened, lit, with a plain awning [STYLE] Avoid: [NEG]
- `W113.png`
A child's swing set in a backyard, empty, summer [STYLE] Avoid: [NEG]
- `W114.png`
The same swing set rusted and empty in winter [STYLE] Avoid: [NEG]
- `W115.png`
A telephone pole with a new cable added to the old ones [STYLE] Avoid: [NEG]
- `W116.png`
A tree that has grown noticeably taller beside a house, summer [STYLE] Avoid: [NEG]
- `W117.png`
A driveway with a different car on it than before [STYLE] Avoid: [NEG]
- `W118.png`
A hillside of bare trees under low cloud, the whole frame grey [STYLE] Avoid: [NEG]
- `W119.png`
The same hillside in full green [STYLE] Avoid: [NEG]
- `W120.png`
The same hillside in late autumn rust [STYLE] Avoid: [NEG]
- `W121.png`
Rain on a windscreen from inside a parked car, the world outside unreadable [STYLE] Avoid: [NEG]
- `W122.png`
A kitchen table with one place set and nobody at it, evening light [STYLE] Avoid: [NEG]
- `W123.png`
A wall calendar with the current page torn away, only the backing board left [STYLE] Avoid: [NEG]
- `W124.png`
A woman in her thirties standing at a window with her back to the room, face not visible, grey daylight outside [STYLE] Avoid: [NEG]

### ACT_5（24:00–28:00・18枚） — ほどける。有罪破棄、訴因取り下げ。

- `W125.png`
A cardboard box of papers on a plain table, lid off, nothing written visible [STYLE] Avoid: [NEG]
- `W126.png`
A hand pulling a single sheet from a thick folder, hand only [STYLE] Avoid: [NEG]
- `W127.png`
A conference room with a long table and nobody at it, blinds half open [STYLE] Avoid: [NEG]
- `W128.png`
The exterior of a plain government office building on an overcast day, no signage legible [STYLE] Avoid: [NEG]
- `W129.png`
A woman in her thirties in a plain coat standing at the top of concrete steps, seen from behind [STYLE] Avoid: [NEG]
- `W130.png`
A car with its passenger door open on a wide empty road, nobody in frame [STYLE] Avoid: [NEG]
- `W131.png`
A door of a modest house standing open from inside, daylight beyond it [STYLE] Avoid: [NEG]
- `W132.png`
A kitchen with the tap running and a glass being filled, hands only [STYLE] Avoid: [NEG]
- `W133.png`
A pair of worn shoes set down on a wooden floor by a doorway [STYLE] Avoid: [NEG]
- `W134.png`
A bed made up in a plain room with the curtains open [STYLE] Avoid: [NEG]
- `W135.png`
A woman in her thirties sitting on the edge of a bed with her back to the camera, morning light [STYLE] Avoid: [NEG]
- `W136.png`
A phone on a kitchen counter beside a set of keys [STYLE] Avoid: [NEG]
- `W137.png`
An unopened envelope on a doormat inside a front door [STYLE] Avoid: [NEG]
- `W138.png`
A plain corridor of a public building with daylight at the far end [STYLE] Avoid: [NEG]
- `W139.png`
A carrier bag of belongings set down on a porch step [STYLE] Avoid: [NEG]
- `W140.png`
A hand on a door frame, only the hand and the frame in focus [STYLE] Avoid: [NEG]
- `W141.png`
A modest house seen from the road with the front door standing open [STYLE] Avoid: [NEG]
- `W142.png`
The two-lane road out of town in daylight, empty, going away from the camera [STYLE] Avoid: [NEG]

### ENDING（28:00–30:00・8枚） — 残ったもの。

- `W143.png`
A plain field at first light under thin cloud, no feature in it [STYLE] Avoid: [NEG]
- `W144.png`
A creek moving steadily past bare banks, close to the water [STYLE] Avoid: [NEG]
- `W145.png`
A woman in her forties standing alone in a field at dawn, distant, seen from behind [STYLE] Avoid: [NEG]
- `W146.png`
A porch light left on in daylight [STYLE] Avoid: [NEG]
- `W147.png`
A small-town street with the lights coming on at dusk, nobody on it [STYLE] Avoid: [NEG]
- `W148.png`
A bare tree against a pale sky, the whole frame quiet [STYLE] Avoid: [NEG]
- `W149.png`
An empty chair on a porch facing the road [STYLE] Avoid: [NEG]
- `W150.png`
A road going over a rise and out of sight under an overcast sky [STYLE] Avoid: [NEG]

---

## 6. 完了条件（全部緑で完了）

```
[A-1] H:\pd-media\assets\ai\weimer\ に W001..W150 = 150枚
[A-2] _02 / _03 が0件
[A-3] 全150枚の長辺 >= 3840px
[A-4] Q1-Q8 を全150枚で目視。1枚も該当なし
[A-5] Q4（監獄・法廷）と Q5（事件）は特に厳格に。1枚もないのが正しい
[A-6] sha256 重複ゼロ（150枚全体で）
[A-7] 知覚ハッシュの近似重複ゼロ（150枚全体で）
[A-8] 全150枚の平均輝度：45未満が0枚 / 中央値55以上 / 暗いカット3連続まで
[A-9] 1枚目で [STYLE] / [NEG] が展開済みであることを確認した記録
[A-10] BATCH_A_QC_v001.json を出力（schema: pd.weimer.batch_a_qc.v001）
```

**150枚に届かないまま先へ進まない。基準を下げない。水増ししない。**

### ACT_4 は順序に意味があります

40枚が**同じ場所に季節が何度も来る**構造になっています（同じ野原・同じ小川・同じポーチ・
同じ通り・同じ窓を、春夏秋冬で撮り直す）。**同じ場所として一貫させてください。**
ここが崩れると「11年」が伝わりません。実写ではこれが作れないことを測って確認済みです
（雪解け0本・夏0本・秋0本）。

---

*2026-08-03 作成。契約は `episodes/PD-2026-061-weimer/episode_spec.v001.json`。
事実は `Weimer v. County of Fayette, 972 F.3d 177 (3d Cir. 2020)`（CourtListener cluster 4778177、
抜粋は `episodes/_planning/measurements/WEIMER_FACTS.md`）。
実写の実測は288タイル目視で使用可87本。*
