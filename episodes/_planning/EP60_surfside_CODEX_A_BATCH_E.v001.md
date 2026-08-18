# EP60 surfside — Codex 画像生成 **バッチE：実写で埋まらなかった4領域** v001（100枚・1プロンプト1枚）

> ## ✅ 今すぐ着手してよいファイルです。
> **なぜ5本目が必要になったか（実測の記録）:**
> バッチA〜Dの179枚は納品済みです。その上で、残り約330カットを実写素材で埋められるかを
> **34モチーフ・約800枚のタイルを目視して**検証しました。結果は **確保できた実写が約75本**。
> 足りないのではなく、**特定の4領域が棚に存在しない**ことが分かりました。
>
> 決定的だったのはこれです。**この映画の中心的なイメージ — コンクリートから滲み出す錆 —
> は、288本を目視して1枚もありませんでした。** 剥落した被り、露出した鉄筋、スラブ下面の
> ひび、接合部の割れ。すべてゼロ。`concrete` は24/24が装飾的な壁テクスチャ、`rust` が返す
> のは南京錠と自転車、`column` は24/24が銀行と大聖堂の柱でした。
>
> このファイルはその穴だけを埋めます。**S151–S250 の100枚。**

**題材:** 2021年6月24日、フロリダ州サーフサイドのシャンプレンタワー南棟が部分崩落し98人が亡くなった件。
**この映画は再現映像ではありません。崩落そのものを描かず、犠牲者を描きません。**

---

## 0. ★★★ 最重要：1プロンプト = 1枚 ★★★

1. **各プロンプトから画像を1枚だけ作る。** 同じプロンプトで2枚目を作らない。
2. **`_02` / `_03` を作らない。** 候補を並べて選ぶ工程は存在しない。
3. **「良いのが出るまで回す」を禁止。**
4. **作り直してよいのは §1 の禁止に触れたときだけ。** そのときも**文言を直してから1枚**。

バッチA・B・C・D はこの規則で **179枚・変種0・指定外0・sha256重複0・知覚的近似重複0** を
達成済み（全15,931組を独立検証済み）。再生成はバッチCの2件のみで、どちらも
**同じプロンプトを回し直したのではなく、文言を直してから1枚**でした。**同じ水準で。**

---

## 1. ★絶対条件（触れた絵は使用不可）

- **崩落・瓦礫・救助・遺体を描かない。** 建物が壊れていく過程を描くのであって、壊れた結果ではない。
- **実在の建物「シャンプレンタワー南棟」の肖像を作らない。** 建物は**1981年前後のフロリダ海岸の
  分譲高層住宅という類型**として描く。実物の写真と見紛うものを作らない。
- **顔を作らない。** このバッチに顔は一枚もありません（顔はバッチCが担当済み）。人が要る場面は
  **手元・後ろ姿・シルエット・顔が判別できない距離**のみ。
- **読める文字・数字・署名・印章・紋章・ロゴを描かない。** 書類は「書類に見える面」であって、
  読める文書ではない。
- **廃墟趣味にしない。** 落書き、割れたガラス、オレンジとティールの色調は禁止。
  **あの建物は最後の夜まで人が住み、手入れを議論していた家**であって、廃墟ではありません。

### 生成後のチェック（1枚ずつ目視）

| # | 不合格条件 |
|---|---|
| Q1 | 長辺が3840px未満 |
| Q2 | 読める文字・数字・署名がある |
| Q3 | 印章・紋章・ロゴらしきものがある |
| Q4 | **顔が写っている**（このバッチは顔ゼロが正しい） |
| Q5 | 崩落・瓦礫・負傷が写っている |
| Q6 | 既存の S001–S150・T01–T05・F001–F024（**現物179枚**）と実質同じ構図 |
| Q7 | 落書き・割れたガラス・廃墟趣味の色調がある |

---

## 2. スタイル（★必ず展開してから生成）

**`[STYLE]`** ＝ 末尾にそのまま連結:

> , cinematic still, cold institutional grey-blue concrete as the base palette, one warm amber note reserved strictly for morning light, corrosion stain and warning — never flooding the frame, near-black falloff at the edges, telephoto compression, shallow depth of field, restrained documentary framing, ultra-detailed, photoreal, 4K, 16:9, fine film grain, no text, no lettering, no numerals, no watermark, no logo, no seal, no emblem, no readable documents, no identifiable face

**`[NEG]`** ＝ `Avoid:` の後にそのまま連結:

> readable text, letterforms, numerals, signage, captions, watermarks, logos, seals, emblems, crests, faces, identifiable faces, portraits of real people, collapsed buildings, rubble, debris fields, rescue scenes, injured people, bodies, gore, dramatic explosion, disaster movie lighting, graffiti, smashed glass, urbex ruin aesthetic, orange and teal grading, cartoon, illustration, painterly, oversaturated, HDR halo

1枚目で展開されているか必ず目視確認すること。

---

## 3. 出力

- 出力先: `H:\pd-media\assets\ai\surfside\`
- **S151.png 〜 S250.png（100枚・3840×2160）**
- 既存の S001–S150・T01–T05・F001–F024 は上書きしない。

---

## 4. プロンプト（100行・各1枚）

### 4.1 ①構造の劣化の連鎖（S151–S185 / 35枚）

**実写ゼロの領域。** 288本を目視して、剥落・露出した鉄筋・滲む錆は1枚もありませんでした。
この35枚が第5幕（パンチングシアの説明）と第2幕（技師が見たもの）を支えます。
**順序に意味があります。** 健全な状態 → 水が入る → 錆びる → 膨張する → 被りが割れる →
鉄筋が露出する → 断面が減る、という一本の因果を35枚で辿ります。

- `S151.png`
The underside of a flat reinforced-concrete slab where it meets the head of a square column, seen from directly below in a dim garage, the concrete sound and unmarked, cold grey [STYLE] Avoid: [NEG]
- `S152.png`
A grid of square concrete columns receding into darkness beneath a low flat deck, each column head widening slightly where it meets the slab, nothing wrong yet [STYLE] Avoid: [NEG]
- `S153.png`
A construction joint running across the underside of a concrete deck, the two pours meeting in a hairline seam, dust and shadow gathered along it [STYLE] Avoid: [NEG]
- `S154.png`
The top surface of a concrete deck under a thin skin of standing water after rain, the water finding the low point and staying there [STYLE] Avoid: [NEG]
- `S155.png`
A dark seam in a concrete deck surface where the waterproofing membrane has split, the split filled with grit, seen at a low raking angle [STYLE] Avoid: [NEG]
- `S156.png`
Water tracking downward through a concrete slab from above, a damp irregular stain spreading on the soffit below, still wet at its darkest point [STYLE] Avoid: [NEG]
- `S157.png`
A pale white crystalline bloom of efflorescence creeping out of a crack in a concrete ceiling, salt left behind by water that has already passed through [STYLE] Avoid: [NEG]
- `S158.png`
A single rust-coloured tear running down a grey concrete column from a point high on its face, the stain narrow and deliberate, everything else clean [STYLE] Avoid: [NEG]
- `S159.png`
Several rust stains bleeding out of a concrete soffit in a line, each one marking a reinforcing bar buried somewhere above [STYLE] Avoid: [NEG]
- `S160.png`
An extreme close view of a rust stain where it emerges from concrete, the iron oxide granular and dark at the source, fading to pale orange as it runs [STYLE] Avoid: [NEG]
- `S161.png`
A hairline crack in a concrete soffit running parallel to a reinforcing bar beneath the surface, the crack following the steel rather than the shape of the room [STYLE] Avoid: [NEG]
- `S162.png`
A crack in concrete that has opened wide enough to show darkness inside it, its edges still sharp, no loose material yet [STYLE] Avoid: [NEG]
- `S163.png`
A patch of concrete cover that has lifted away from the surface as a shallow dome, sounding hollow, not yet fallen [STYLE] Avoid: [NEG]
- `S164.png`
The same kind of lifted patch seen from the side against raking light, the gap between the loose cover and the sound concrete behind it just visible [STYLE] Avoid: [NEG]
- `S165.png`
A shallow spall in a concrete soffit where a piece of cover has come away, leaving a rough pale crater with a darker centre [STYLE] Avoid: [NEG]
- `S166.png`
A spall in a concrete face with a single corroded reinforcing bar showing at its base, the bar swollen and flaking, the concrete around it stained [STYLE] Avoid: [NEG]
- `S167.png`
Two parallel corroded reinforcing bars exposed in a broken patch of a concrete slab, their surfaces layered and scaling, the void behind them dark [STYLE] Avoid: [NEG]
- `S168.png`
A close view of corroded reinforcing steel where the section has thinned, the bar noticeably narrower than the sound length beside it [STYLE] Avoid: [NEG]
- `S169.png`
The ribbed surface of a reinforcing bar half-buried in concrete, the ribs blurred and softened by corrosion, cold grey around it [STYLE] Avoid: [NEG]
- `S170.png`
A cross-section of concrete broken open to show reinforcing steel sitting far closer to the surface than it should, a thin skin of cover above it [STYLE] Avoid: [NEG]
- `S171.png`
A cross-section of concrete showing two reinforcing bars set too far apart, the gap between them wide and empty [STYLE] Avoid: [NEG]
- `S172.png`
A column head seen from below where the slab meets it, a ring of fine cracks around the junction, faint but continuous [STYLE] Avoid: [NEG]
- `S173.png`
The same column head with the crack ring more open, the concrete inside the ring beginning to sit slightly lower than the slab around it [STYLE] Avoid: [NEG]
- `S174.png`
A shallow conical depression in the underside of a slab immediately around a column head, the shape of a punching shear failure beginning [STYLE] Avoid: [NEG]
- `S175.png`
A column standing free of the slab above it by a hair, a dark line of separation running around the top of the column [STYLE] Avoid: [NEG]
- `S176.png`
The soffit of a slab bay adjacent to a failed connection, its own cracking spreading outward from the shared edge, load arriving where it was not expected [STYLE] Avoid: [NEG]
- `S177.png`
A wide dim view of a column grid beneath a deck where one column head is visibly darker and more damaged than every other, and nothing else in the frame has changed [STYLE] Avoid: [NEG]
- `S178.png`
Salt-laden air condensing on a concrete surface near the sea, fine droplets held on the rough grey face [STYLE] Avoid: [NEG]
- `S179.png`
A concrete surface facing the ocean, its outer skin pitted and eaten back by decades of salt air, the aggregate beginning to show through [STYLE] Avoid: [NEG]
- `S180.png`
A drainage outlet in a concrete deck blocked with grit and debris, water standing around it instead of leaving [STYLE] Avoid: [NEG]
- `S181.png`
Heavy planters sitting on a concrete deck, soil dark and saturated with water, the load concentrated where they stand [STYLE] Avoid: [NEG]
- `S182.png`
A layer of sand and paving slabs sitting on top of a concrete deck in cross-section, the dead weight of it obvious, the structural slab beneath thin by comparison [STYLE] Avoid: [NEG]
- `S183.png`
A hammer tapping the underside of a concrete slab, the hand and forearm only, listening for the hollow sound of delamination [STYLE] Avoid: [NEG]
- `S184.png`
A gloved fingertip tracing the line of a crack across a concrete soffit, following where it goes rather than where it started [STYLE] Avoid: [NEG]
- `S185.png`
A concrete column photographed straight on in a dim garage, sound, grey, unremarkable, the way it looked on every ordinary day [STYLE] Avoid: [NEG]

### 4.2 ②住宅の共有部（S186–S210 / 25枚）

**実写で確保できたのは廊下3本と玄関ドア1本だけ。** `corridor` は24本中19本が刑務所、
`hallway` は19本が学校、`lobby` は在庫が1本（病院の待合室）でした。
ここは「毎日通っていて誰も見ていなかった場所」の register です。**空であること**が要件です。

- `S186.png`
An empty residential corridor at night, plain flush front doors receding on both sides, low ceiling lights, carpet worn along the centre line [STYLE] Avoid: [NEG]
- `S187.png`
The same kind of corridor in flat daylight from a window at the far end, no one in it, the doors all closed [STYLE] Avoid: [NEG]
- `S188.png`
A single closed apartment front door seen straight on, plain, a thin line of light beneath it, nothing on the door but its handle [STYLE] Avoid: [NEG]
- `S189.png`
A closed apartment door seen from a low angle in a dark corridor, the doorframe and the wall beside it filling the rest of the frame [STYLE] Avoid: [NEG]
- `S190.png`
A doormat outside a closed apartment door, plain and slightly askew, corridor carpet around it [STYLE] Avoid: [NEG]
- `S191.png`
A bank of small metal mailboxes in a residential lobby, all doors shut, no numbers or names legible, morning light across them [STYLE] Avoid: [NEG]
- `S192.png`
The same mailbox bank at night with one small door standing open and empty, the rest closed [STYLE] Avoid: [NEG]
- `S193.png`
A plain residential lobby with a few chairs against a wall, empty, seen from the entrance, the light cold and even [STYLE] Avoid: [NEG]
- `S194.png`
A glass entrance door of a residential block seen from inside at night, the street beyond it dark and empty [STYLE] Avoid: [NEG]
- `S195.png`
An intercom panel beside a residential entrance, buttons blank, the metal dulled by salt air [STYLE] Avoid: [NEG]
- `S196.png`
A lift lobby on a residential floor, brushed steel doors closed, a small call panel beside them, no one waiting [STYLE] Avoid: [NEG]
- `S197.png`
The inside of an ordinary lift car with plain steel walls, empty, lit flatly, the doors closed [STYLE] Avoid: [NEG]
- `S198.png`
A concrete stairwell in a residential building, the flights turning back on themselves, a painted steel handrail, no one on the stairs [STYLE] Avoid: [NEG]
- `S199.png`
Looking straight down the void of a residential stairwell from an upper floor, the flights spiralling away into shadow [STYLE] Avoid: [NEG]
- `S200.png`
A fire door at the head of a concrete stairwell, closed, plain, the corridor light bleeding under it [STYLE] Avoid: [NEG]
- `S201.png`
A residential balcony walkway running along the outside of a concrete building, a plain rail, doors on one side, ocean haze beyond [STYLE] Avoid: [NEG]
- `S202.png`
A single balcony seen from below, the concrete slab of it cantilevered out, the underside stained where water has run off [STYLE] Avoid: [NEG]
- `S203.png`
An empty balcony with two chairs and a small table facing the sea, nobody in them, the light grey and even [STYLE] Avoid: [NEG]
- `S204.png`
A sliding balcony door seen from inside a dim room, closed, the sea beyond it flat and colourless [STYLE] Avoid: [NEG]
- `S205.png`
A residential corridor window looking out over a low coastal town at dusk, the glass slightly salt-clouded [STYLE] Avoid: [NEG]
- `S206.png`
A laundry room in a residential building, machines along one wall, empty, the floor concrete and slightly damp [STYLE] Avoid: [NEG]
- `S207.png`
A pool deck seen from the walkway above at first light, the water still, the chairs stacked and unused [STYLE] Avoid: [NEG]
- `S208.png`
A poolside gate standing closed, the concrete deck beyond it empty, morning light low across the surface [STYLE] Avoid: [NEG]
- `S209.png`
A residential parking bay with one car in it under a low concrete ceiling, the bay markings faded, nothing else in frame [STYLE] Avoid: [NEG]
- `S210.png`
A door to a building services room standing slightly ajar in a garage, darkness beyond it, plain and unremarkable [STYLE] Avoid: [NEG]

### 4.3 ③記録保管（S211–S230 / 20枚）

**実写で確保できたのは木製カード目録5本のみで、しかも5本とも同じ部屋。**
`filing` は在庫2本（うち1本は馬の蹄を削る蹄鉄工）、`shelf` は20本中8本が法律書、
`boxes` は24/24が引っ越しの段ボール、`stack` は20/24が札束でした。
**要件は「冷たいスチール」**です。既に押さえてある暖かい木のカード目録と**対比**させます。

- `S211.png`
A wall of grey steel filing cabinets in a plain room, all drawers closed, flat institutional light [STYLE] Avoid: [NEG]
- `S212.png`
One steel filing drawer pulled halfway out, the tops of file dividers visible inside, no lettering readable [STYLE] Avoid: [NEG]
- `S213.png`
A hand lifting a file from a steel drawer, hand and forearm only, the rest of the drawer in shadow [STYLE] Avoid: [NEG]
- `S214.png`
Rows of plain steel shelving in a records room, each shelf carrying uniform document boxes, the aisle receding into dimness [STYLE] Avoid: [NEG]
- `S215.png`
A single document box on a steel shelf, its lid slightly out of true, dust along the top edge [STYLE] Avoid: [NEG]
- `S216.png`
A stack of document boxes on the floor of a storeroom, unlabelled, the concrete floor cold and bare [STYLE] Avoid: [NEG]
- `S217.png`
A closed cardboard document box carried in two hands, hands only, plain corridor behind [STYLE] Avoid: [NEG]
- `S218.png`
A thick report lying closed on a steel desk under a single lamp, its cover plain, nothing legible [STYLE] Avoid: [NEG]
- `S219.png`
The same report seen from directly above, closed, a pen resting beside it, the desk surface empty otherwise [STYLE] Avoid: [NEG]
- `S220.png`
A ring binder standing among others on a plain shelf, its spine blank, pulled a centimetre proud of the rest [STYLE] Avoid: [NEG]
- `S221.png`
A wire in-tray on a desk holding a single closed envelope, everything else cleared away [STYLE] Avoid: [NEG]
- `S222.png`
A stack of loose paper squared off on a desk, the edges not quite aligned, side light raking across them [STYLE] Avoid: [NEG]
- `S223.png`
A manila folder lying open on a desk showing a blank inner face, hands absent, lamp light from one side [STYLE] Avoid: [NEG]
- `S224.png`
A sheet of technical drawing rolled out flat and weighted at two corners, the lines abstract and unreadable at this scale [STYLE] Avoid: [NEG]
- `S225.png`
A drawer of hanging files seen from above, the tabs blank, the file bodies packed tight [STYLE] Avoid: [NEG]
- `S226.png`
An office storeroom with steel shelving on both sides, boxes to the ceiling, a bare bulb overhead [STYLE] Avoid: [NEG]
- `S227.png`
Dust in a shaft of light in a records room, the shelving behind it out of focus [STYLE] Avoid: [NEG]
- `S228.png`
A photocopier lid raised over a blank glass platen in a dim office, the machine cold and industrial [STYLE] Avoid: [NEG]
- `S229.png`
A steel filing cabinet standing alone against a bare wall in an empty room, one drawer very slightly open [STYLE] Avoid: [NEG]
- `S230.png`
A cardboard box of paperwork left on a chair in an empty meeting room, the chairs around it pushed in [STYLE] Avoid: [NEG]

### 4.4 ④建物そのもの（S231–S250 / 20枚）

**実写で使えたのは団地の空撮1本と中層ビル1本だけ。** `facade` は19本中8本がガラスの高層ビル、
`apartment` は8/10が既出、`housing` は在庫3本、`column` は24/24が銀行と大聖堂の柱でした。
**類型として描くこと。実在の建物の肖像を作らないこと。**

- `S231.png`
A plain twelve-storey concrete residential block on a flat sandy coast seen from the beach in overcast light, balcony stacks repeating up its face, no ornament [STYLE] Avoid: [NEG]
- `S232.png`
The same kind of block seen at dusk from across an empty street, windows lit unevenly, the sky drained of colour [STYLE] Avoid: [NEG]
- `S233.png`
A concrete residential tower photographed straight up its face from the ground, balcony slabs receding to a flat grey sky [STYLE] Avoid: [NEG]
- `S234.png`
A tight frame of balcony stacks on a concrete residential building, the rhythm of slab and rail filling the whole picture [STYLE] Avoid: [NEG]
- `S235.png`
The corner of a concrete residential block where two facades meet, weathering running differently down each face [STYLE] Avoid: [NEG]
- `S236.png`
A concrete residential building seen from the sea side in flat morning haze, its outline soft, the beach empty in front of it [STYLE] Avoid: [NEG]
- `S237.png`
The flat gravel roof of a residential block with mechanical plant on it, ponded water standing in a low corner, overcast [STYLE] Avoid: [NEG]
- `S238.png`
A roof parapet of a concrete building seen from the roof surface, the sea horizon beyond it, nothing else in frame [STYLE] Avoid: [NEG]
- `S239.png`
The ramp down into an underground garage beneath a residential building, the entrance dark, concrete walls either side [STYLE] Avoid: [NEG]
- `S240.png`
A wide dim view of an underground residential garage, columns in a grid, a few parked cars, low ceiling [STYLE] Avoid: [NEG]
- `S241.png`
The junction where a pool deck meets the base of a residential tower, seen from ground level, concrete on concrete [STYLE] Avoid: [NEG]
- `S242.png`
A raised concrete pool deck seen from below at its edge, the underside of the slab visible where it oversails the garage [STYLE] Avoid: [NEG]
- `S243.png`
A residential building's ground-floor entrance drive, plain concrete paving, a low planter wall, nobody about [STYLE] Avoid: [NEG]
- `S244.png`
The service side of a residential block, bin store and plant, unglamorous, in flat grey light [STYLE] Avoid: [NEG]
- `S245.png`
A concrete residential building in heavy rain seen from across a road, water running down its face, the light nearly monochrome [STYLE] Avoid: [NEG]
- `S246.png`
The same building type at first light, one warm amber note where the sun touches the top three floors and nothing else [STYLE] Avoid: [NEG]
- `S247.png`
An aerial straight down on a residential block, its flat roof, its pool deck and its parking, the geometry legible as a plan [STYLE] Avoid: [NEG]
- `S248.png`
A residential block seen past palm fronds in overcast light, the fronds dark and unlit, the building plain behind them [STYLE] Avoid: [NEG]
- `S249.png`
A row of ordinary low coastal buildings with one taller concrete block among them, none of them remarkable [STYLE] Avoid: [NEG]
- `S250.png`
A concrete residential building at night from a distance, most windows dark, a handful lit, the sea black in front of it [STYLE] Avoid: [NEG]

---

## 5. 完了条件（全部緑で完了）

```
[E-1] H:\pd-media\assets\ai\surfside\ に S151..S250 = 100枚
[E-2] _02 / _03 が0件
[E-3] 全100枚の長辺 >= 3840px
[E-4] §1 の Q1–Q7 を全100枚で目視。1枚も該当なし
[E-5] Q4（顔）は特に厳格に。このバッチに顔は一枚も無いのが正しい
[E-6] sha256 重複ゼロ（S001–S250 / T01–T05 / F001–F024 の全279枚で）
[E-7] 知覚ハッシュの近似重複ゼロ（同じく全279枚で）
[E-8] 1枚目で [STYLE] / [NEG] が展開済みであることを確認した記録
[E-9] BATCH_E_QC_v001.json を A/B/C/D と同じ形式で出力
      （schema は pd.surfside.batch_e_qc.v001。deliverable_count / generation_attempts /
        regeneration_count / rejections / checks を含める。
        checks に all_279_present と all_279_sha256_duplicates_zero を入れる）
```

**100枚に届かないまま先へ進まない。基準を下げない。水増ししない。**

§4.1 は**順序に意味がある35枚**です。S151が健全な接合部、S177が「一つだけ違う柱」。
途中を飛ばすと因果が途切れます。**通し番号どおりに作ってください。**

---

## 6. これで EP60 の画像は完結します

| バッチ | 枚数 | 守備範囲 | 状態 |
|---|---|---|---|
| A | 56 | S001–S056：コンクリートの破壊、接合部、ガレージ | ✅納品済 |
| B | 56 | S057–S110＋T01–T02：第3幕の金額、第4幕の春、第5幕の設計と調査、その夜、結末 | ✅納品済 |
| C | 27 | F001–F024＋T03–T05：払う側の住民の顔、サムネイル用の顔 | ✅納品済 |
| D | 40 | S111–S150：第1幕の建物と所有、第2幕の技師とあの部屋 | ✅納品済 |
| **E** | **100** | **S151–S250：劣化の連鎖、住宅の共有部、記録保管、建物そのもの** | ← このファイル |
| **合計** | **279** | | |

本編は約520カット。**実写素材は目視で約75本しか確保できませんでした**（34モチーフ・約800枚の
タイルを13体のエージェントで検証、報告された84件のファイル名は全数実在照合済み）。
断面図（Blender）が4〜6ショット、AEカードが12〜16枚。**残りをこの279枚が担います。**

---

*2026-08-02 作成。台本 `EP60_surfside_script.en.v004.md`（6,304語・36.4分）と
`EP60_surfside_ASSET_DESIGN.v002.md` から積算。事実は `EP60_surfside_FACTS_LEDGER.v002.md`。
実写素材の実測は `EP60_surfside_FOOTAGE_REVIEW.v001.md`。*

*このバッチが存在する理由を一行で言うと：**棚には「コンクリートから滲み出す錆」が
288本のうち1枚も無かった**からです。*
