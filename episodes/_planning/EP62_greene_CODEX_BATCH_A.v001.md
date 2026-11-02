# EP62 greene — Codex 画像生成 **1本で完結する発注** v001（222枚・1プロンプト1枚）

> ## ✅ 今すぐ着手してよいファイルです。**追加バッチは出ません。**
> EP60はバッチが5本に膨らみました。原因は3つとも同じで、**発注時点で構造が決まっていなかった**
> ことです。今回は逆順にしました。**実写を先に測り（47本取り込み・全タイル目視・使えるのは12本）、
> 29分を8区分に割り切り、区分ごとに枚数を確定させてから**この発注を書いています。
> **どの区分にも絵があります。**下の表がその証明です。
> 枚数の根拠は `EP62_65_IMAGE_BUDGET.v001.md`：契約 `distinct_video_assets` 234 − 実写採用12 = **222**。

**題材:** *Greene v. Lindsey*, 456 U.S. 444 (1982)。ケンタッキー州ルイビルの公営住宅で、立ち退きの
通知が**ドアに貼られただけ**だった。住人は見ていないと主張し、欠席判決で家を失う手前まで行った。

**この映画は「強欲な家主」の話ではありません。**訴えられた側は**ルイビル住宅公社＝政府機関**です。
主題は**誰も読まなかった一枚の紙**であり、立ち退きそのものではありません。

---

## 0. ★★★ 最重要：1プロンプト = 1枚 ★★★

1. **各プロンプトから画像を1枚だけ作る。** 同じプロンプトで2枚目を作らない。
2. **`_02` / `_03` を作らない。**
3. **「良いのが出るまで回す」を禁止する。**
4. 作り直してよいのは §1 の禁止に触れたときだけ。そのときも**文言を直してから1枚**。

EP60はこの規則で **279枚・変種0・指定外0・sha256重複0・知覚的近似重複0** を達成済み。

---

## 1. ★絶対条件（触れた絵は使用不可）

`episodes/PD-2026-062-greene/episode_spec.v001.json` の `forbidden_subjects` がこの節の正典です。

- **立ち退きの最中を描かない。** 歩道に出された家具・追い出される家族・**ドアの前の保安官**。一切。
- **制服の執行官・保安官・警官を描かない。** この映画に「来た人」は映りません。映るのは**紙**です。
- **家主というキャラクターを描かない。** 被告は政府機関です。
- **実在の3人（Linnie Lindsey / Barbara Hodgens / Pamela Ray）とその住居を描かない。** 人物は全員
  「実在しない一般人」として描く。
- **法廷を描かない。** 法廷内観・木槌・判事席。棚の法廷映像は61話で使い切っており、絵も作りません。
  **裁判所は外観のみ可。**
- **監獄を描かない。** 鉄格子・有刺鉄線・独房・手錠。この話は収監の話ではありません。
- **読める文字・数字・署名・印章・ロゴを描かない。** 通知の紙も**文字が判別できない状態**で描く
  （実際の令状を映せないため。ここは事故が最も起きやすい箇所です）。
- **実在と特定できる建物を描かない。** 看板・紋章・特徴的な建築で場所が割れる絵は不可。
- **子どもの顔を描かない。** 子どもは「痕跡」でのみ表す（自転車・チョーク・ボール・低い位置の手）。
- **広告調にしない。** 黄金色の夕陽、絵葉書の風景、クリスマス、南国、砂漠、ドローンの映え、
  暖炉のくつろぎループ。
- **同情の演出を禁止する。** 肩に置かれた手、涙、時計のカウントダウン、寄り添う老夫婦。
- **黒つぶれさせない。** スマホで見て何が写っているか分かること。

### 生成後のチェック（1枚ずつ目視）

| # | 不合格条件 |
|---|---|
| Q1 | 長辺が3840px未満 |
| Q2 | 読める文字・数字・署名がある（**紙の上も含む**） |
| Q3 | 印章・紋章・ロゴらしきものがある |
| Q4 | 制服・バッジ・パトカー・法廷・鉄格子が写っている |
| Q5 | 立ち退きの最中（歩道の家具・運び出される荷物・泣いている人）が写っている |
| Q6 | 既存の他話の画像と実質同じ構図 |
| Q7 | 広告調（黄金色の映え・絵葉書・くつろぎ暖炉）である |
| Q8 | 画面全体が暗すぎる |
| Q9 | 子どもの顔が判別できる |

---

## 2. スタイル（★必ず展開してから生成）

**`[STYLE]`** ＝ 末尾にそのまま連結:

> , cinematic still, muted natural colour, flat humid Ohio Valley light, low contrast, low-key but never crushed: shadows keep their detail and the frame reads clearly on a phone screen, soft falloff toward the edges, shallow depth of field, restrained documentary framing, mid-1970s to early-1980s American public housing period detail, nothing staged for advertising, ultra-detailed, photoreal, 4K, 16:9, fine film grain, no text, no lettering, no numerals, no watermark, no logo, no signage

**`[NEG]`** ＝ `Avoid:` の後にそのまま連結:

> text, lettering, numerals, handwriting, signatures, seals, emblems, logos, signage, house numbers, street signs, police uniform, sheriff badge, patrol car, courtroom interior, gavel, judge's bench, prison bars, razor wire, handcuffs, furniture on a pavement, people being evicted, crying, a hand on a shoulder, golden hour, sunset glow, postcard scenery, drone shot, cosy fireplace, Christmas, tropical, modern smartphones, modern cars, flat CGI, cartoon, illustration, oversaturated

---

## 3. 命名と保存先

- ファイル名 `G001.png` … `G222.png`。**欠番を作らない。**
- 保存先 `H:\pd-media\assets\ai\greene\`。
- 長辺 3840px 以上・16:9・PNG。

---

## 4. 区分と枚数（合計222枚）

| 区分 | 秒 | 枚数 | 中身 |
|---|---|---|---|
| HOOK | 0:00–0:50 | 12 | ドアの紙。留守。気づかないまま進む手続き |
| OP | 0:50–1:15 | 5 | ブランド。無地のテクスチャ |
| ACT_1 | 1:15–6:30 | 35 | 1975年ルイビル。公営住宅という場所と、そこに住むということ |
| ACT_2 | 6:30–11:30 | 35 | 「掲示」という手続きそのもの。画鋲・テープ・一度きりの訪問 |
| ACT_3 | 11:30–16:30 | 35 | 記録に残った証言。紙は剥がされていた |
| ACT_4 | 16:30–21:30 | 35 | 三つの裁判所。負けて、覆って、最高裁へ |
| ACT_5 | 21:30–26:30 | 35 | 判断と反対意見。郵便という選択肢 |
| ENDING | 26:30–29:00 | 17 | 何が変わり、何が変わらなかったか |
| PEOPLE | — | 10 | 人物プレート（顔なし規則・`people_plates_min: 10`） |
| THUMB | — | 3 | サムネ候補（`thumbnail_candidates_min: 3`） |

---

## 5. プロンプト（各1枚）

### HOOK（0:00–0:50・12枚） — ドアに貼られた紙。留守。

- `G001.png`
A single sheet of plain paper taped flat to a painted apartment door, the sheet blank and its text illegible, one corner already lifting [STYLE] Avoid: [NEG]
- `G002.png`
The same door from three paces back, the paper small in the middle of it, the walkway empty on both sides [STYLE] Avoid: [NEG]
- `G003.png`
Extreme close on a brass thumbtack pushed through paper into a painted wooden door, the paint chipped around it [STYLE] Avoid: [NEG]
- `G004.png`
A strip of adhesive tape peeling away from a door, half a sheet of paper hanging from it, no text visible [STYLE] Avoid: [NEG]
- `G005.png`
An empty concrete walkway of a two-storey brick housing block at midday, a row of identical closed doors receding, nobody on it [STYLE] Avoid: [NEG]
- `G006.png`
A sheet of paper lying face down on a concrete step below a door, one edge dark with damp [STYLE] Avoid: [NEG]
- `G007.png`
A door photographed from inside a dim apartment, daylight in the gap beneath it, nothing else in the frame [STYLE] Avoid: [NEG]
- `G008.png`
A knuckle a few centimetres from a painted door, arrested mid-air, no face and no body beyond the forearm [STYLE] Avoid: [NEG]
- `G009.png`
The same brick housing block at dusk, three windows lit out of thirty, no figures [STYLE] Avoid: [NEG]
- `G010.png`
A close view of a doorframe at the height of a small child, the paint scuffed, nothing on the door [STYLE] Avoid: [NEG]
- `G011.png`
A bare door with a clean unfaded rectangle where something was taped for a long time and then removed [STYLE] Avoid: [NEG]
- `G012.png`
A wide low-angle of the same walkway at night, one bulb burning above one door, the rest dark [STYLE] Avoid: [NEG]

### OP（0:50–1:15・5枚） — ブランド。無地。

- `G013.png`
A flat expanse of painted breeze-block wall filling the frame, one hairline crack, overcast light [STYLE] Avoid: [NEG]
- `G014.png`
The torn edge of a sheet of ordinary paper at extreme magnification, fibres raised, plain grey ground [STYLE] Avoid: [NEG]
- `G015.png`
A plain overcast sky filling the frame with a single utility line crossing one corner [STYLE] Avoid: [NEG]
- `G016.png`
Rain standing in the shallow depressions of a worn concrete slab, no horizon, no sky [STYLE] Avoid: [NEG]
- `G017.png`
Weathered brick in raking side light, mortar joints picked out, no windows and no edges of the building [STYLE] Avoid: [NEG]

### ACT_1（1:15–6:30・35枚） — 1975年ルイビル。公営住宅という場所。

- `G018.png`
A low-rise brick public housing development seen from across an open lawn on a flat grey morning, no signage anywhere [STYLE] Avoid: [NEG]
- `G019.png`
Two parallel blocks of the same development with a strip of worn grass between them, washing lines strung across it, no people [STYLE] Avoid: [NEG]
- `G020.png`
A concrete stoop with two steps and a metal handrail worn shiny by use, the door beyond it shut [STYLE] Avoid: [NEG]
- `G021.png`
An outdoor stairwell of poured concrete seen from the bottom, the treads chipped, daylight at the top [STYLE] Avoid: [NEG]
- `G022.png`
A row of plain metal mailboxes on a wall, all doors shut, no names and no numbers legible [STYLE] Avoid: [NEG]
- `G023.png`
A child's bicycle lying on its side on a patch of bare earth beside a walkway, nobody near it [STYLE] Avoid: [NEG]
- `G024.png`
Chalk marks faded almost to nothing on a concrete slab, a hopscotch grid half washed away [STYLE] Avoid: [NEG]
- `G025.png`
A kitchen in a modest apartment in the mid 1970s, enamel sink, a kettle on the stove, nobody there [STYLE] Avoid: [NEG]
- `G026.png`
A living room with a worn sofa and drawn curtains, a lamp on but the room still dim, no people [STYLE] Avoid: [NEG]
- `G027.png`
A narrow interior hallway with three doors off it, one ajar, a light on beyond it [STYLE] Avoid: [NEG]
- `G028.png`
A pair of shoes set neatly inside a front door on a mat, nobody in frame [STYLE] Avoid: [NEG]
- `G029.png`
A window from inside with a net curtain drawn across it, the shapes of the block opposite showing through [STYLE] Avoid: [NEG]
- `G030.png`
The shadow of a person crossing a drawn curtain from inside, seen from the walkway, no features [STYLE] Avoid: [NEG]
- `G031.png`
A kettle steaming on a gas ring in a small kitchen, morning light through a small window [STYLE] Avoid: [NEG]
- `G032.png`
A coat and a headscarf hanging on a hook by a door, the wall behind them marked [STYLE] Avoid: [NEG]
- `G033.png`
A bus stop shelter on an ordinary city street at dawn, empty, the road wet [STYLE] Avoid: [NEG]
- `G034.png`
A woman's hands at a bus stop holding a folded paper bag, no face, plain winter coat sleeves [STYLE] Avoid: [NEG]
- `G035.png`
A time clock on a workplace wall with its face blank and unreadable, a rack of cards beside it [STYLE] Avoid: [NEG]
- `G036.png`
An industrial laundry room with tumbling machines and nobody attending them [STYLE] Avoid: [NEG]
- `G037.png`
A cleaner's trolley parked in an empty corridor of an office building at night [STYLE] Avoid: [NEG]
- `G038.png`
A worn linoleum floor at eye level, the pattern rubbed through along one path [STYLE] Avoid: [NEG]
- `G039.png`
A bedroom with a single bed made up tight, a chair beside it with folded clothes, curtains half drawn [STYLE] Avoid: [NEG]
- `G040.png`
A small child's shoes side by side under a chair, nobody in frame [STYLE] Avoid: [NEG]
- `G041.png`
The corner of a housing block where two walkways meet, a drainpipe, weeds at the base [STYLE] Avoid: [NEG]
- `G042.png`
Laundry hanging still on a line between two poles under a white sky [STYLE] Avoid: [NEG]
- `G043.png`
An open kitchen drawer with ordinary cutlery in it, a hand just leaving the frame [STYLE] Avoid: [NEG]
- `G044.png`
A rent book sized notebook closed on a kitchen table, its cover plain and unmarked, a pen beside it [STYLE] Avoid: [NEG]
- `G045.png`
Coins and folded notes counted out on a kitchen table, the denominations not legible, two hands only [STYLE] Avoid: [NEG]
- `G046.png`
A telephone on a hallway table, the handset in its cradle, the cord hanging [STYLE] Avoid: [NEG]
- `G047.png`
A calendar on a kitchen wall with its grid blank and unreadable, afternoon light across it [STYLE] Avoid: [NEG]
- `G048.png`
A view down onto the development from an upper walkway, cars of the period parked in rows [STYLE] Avoid: [NEG]
- `G049.png`
A screen door with a torn corner of mesh, the interior beyond it dark [STYLE] Avoid: [NEG]
- `G050.png`
An electricity meter cupboard standing open on an exterior wall, the dials blank and unreadable [STYLE] Avoid: [NEG]
- `G051.png`
A patch of communal grass with a bald worn circle where children have played [STYLE] Avoid: [NEG]
- `G052.png`
Rain on the concrete of an open walkway, running along the edge, no figures [STYLE] Avoid: [NEG]

### ACT_2（6:30–11:30・35枚） — 「掲示」という手続き。

- `G053.png`
A gloved hand holding a folded sheet of paper against a door, the sheet blank, no uniform and no cuff insignia visible [STYLE] Avoid: [NEG]
- `G054.png`
A box of brass thumbtacks tipped on a car seat, spilled across the vinyl [STYLE] Avoid: [NEG]
- `G055.png`
A roll of adhesive tape on a dashboard beside a clipboard whose paper is blank [STYLE] Avoid: [NEG]
- `G056.png`
The interior of a plain sedan of the period from the passenger side, a stack of blank papers on the seat, nobody in it [STYLE] Avoid: [NEG]
- `G057.png`
A car parked at the kerb of a housing development with its driver's door standing open, nobody visible [STYLE] Avoid: [NEG]
- `G058.png`
A single set of footprints across a strip of wet concrete, going one way only [STYLE] Avoid: [NEG]
- `G059.png`
The paper going onto the door: two hands pressing tape at the top corners, no face, no sleeve markings [STYLE] Avoid: [NEG]
- `G060.png`
The same door a moment later, the hands gone, the sheet flat and blank [STYLE] Avoid: [NEG]
- `G061.png`
A door seen from the far end of a walkway, the paper on it barely readable as a white rectangle [STYLE] Avoid: [NEG]
- `G062.png`
Four identical doors in a row, one of them carrying a white rectangle, the others bare [STYLE] Avoid: [NEG]
- `G063.png`
A wristwatch on a forearm showing a time that cannot be read, held over a steering wheel [STYLE] Avoid: [NEG]
- `G064.png`
Mid-afternoon light on an empty walkway, every door shut, no sound implied [STYLE] Avoid: [NEG]
- `G065.png`
The gap under a closed door seen from outside at floor level, no light beyond it [STYLE] Avoid: [NEG]
- `G066.png`
A doorbell push worn smooth, the surround cracked, no label [STYLE] Avoid: [NEG]
- `G067.png`
A hand knocking, caught at the instant of contact, seen from the side, no face [STYLE] Avoid: [NEG]
- `G068.png`
The same door from inside, empty rooms behind the camera, the letter of light under it unbroken [STYLE] Avoid: [NEG]
- `G069.png`
A clipboard held at waist height with a blank form on it, a pen tucked under the clip, no face [STYLE] Avoid: [NEG]
- `G070.png`
A statute book closed on a desk, its spine plain, no lettering [STYLE] Avoid: [NEG]
- `G071.png`
A single page held up to a window so the light comes through it, the type dissolved to grey texture [STYLE] Avoid: [NEG]
- `G072.png`
A wire tray of blank forms on an office counter, the office plain and unbranded [STYLE] Avoid: [NEG]
- `G073.png`
A rubber date stamp resting on an ink pad, the stamp face blank [STYLE] Avoid: [NEG]
- `G074.png`
A metal filing cabinet drawer half open with unlabelled folders in it [STYLE] Avoid: [NEG]
- `G075.png`
An office corridor of the period with frosted glass doors, nobody in it [STYLE] Avoid: [NEG]
- `G076.png`
A window of a municipal office seen from the street, blinds half drawn, no signage [STYLE] Avoid: [NEG]
- `G077.png`
A map of a city district pinned to a wall with the labels illegible, one area circled [STYLE] Avoid: [NEG]
- `G078.png`
A route of streets seen from a car windscreen through rain, wipers mid-sweep [STYLE] Avoid: [NEG]
- `G079.png`
A car's wing mirror with a brick block receding in it, blurred [STYLE] Avoid: [NEG]
- `G080.png`
A tyre stopped against a concrete kerb, weeds in the joint [STYLE] Avoid: [NEG]
- `G081.png`
A hand returning a stack of blank papers to a rubber band on a car seat [STYLE] Avoid: [NEG]
- `G082.png`
An empty walkway in the rain with a white rectangle on one door, softened by water [STYLE] Avoid: [NEG]
- `G083.png`
The same sheet an hour later, curling at both bottom corners [STYLE] Avoid: [NEG]
- `G084.png`
A gust of wind moving a taped sheet against a door, caught at full lift [STYLE] Avoid: [NEG]
- `G085.png`
A blank sheet caught against a chain-link fence at ankle height [STYLE] Avoid: [NEG]
- `G086.png`
A drain grating with a corner of wet paper across one bar [STYLE] Avoid: [NEG]
- `G087.png`
A door with nothing on it, photographed straight on in flat light, filling the frame [STYLE] Avoid: [NEG]

### ACT_3（11:30–16:30・35枚） — 記録に残った証言。紙は剥がされていた。

- `G088.png`
A small hand at the very edge of frame reaching up toward the bottom corner of a taped sheet, no face, no body [STYLE] Avoid: [NEG]
- `G089.png`
A door at low camera height, the paper on it seen from a child's eye level [STYLE] Avoid: [NEG]
- `G090.png`
Torn paper corners still under two strips of tape on an otherwise bare door [STYLE] Avoid: [NEG]
- `G091.png`
Scraps of white paper scattered along the base of a brick wall [STYLE] Avoid: [NEG]
- `G092.png`
A single scrap of paper turning over on concrete in the wind [STYLE] Avoid: [NEG]
- `G093.png`
A hand pressing a sheet back onto a door higher up than before, at full stretch, no face [STYLE] Avoid: [NEG]
- `G094.png`
The same door with the sheet placed unusually high, well above the handle [STYLE] Avoid: [NEG]
- `G095.png`
A deposition room: a plain table, two chairs, a jug of water, nobody in the room [STYLE] Avoid: [NEG]
- `G096.png`
A reel-to-reel tape recorder on a table with the reels turning, no labels [STYLE] Avoid: [NEG]
- `G097.png`
A stenotype machine on its stand with a ribbon of blank paper folding into a basket [STYLE] Avoid: [NEG]
- `G098.png`
A microphone on a plain table pointing at an empty chair [STYLE] Avoid: [NEG]
- `G099.png`
Two hands folded on a table in a plain room, sleeves ordinary, no face and no insignia [STYLE] Avoid: [NEG]
- `G100.png`
A glass of water half drunk on a table beside a closed folder [STYLE] Avoid: [NEG]
- `G101.png`
A transcript bound at the spine, closed, its cover blank [STYLE] Avoid: [NEG]
- `G102.png`
A stack of transcripts on a shelf, all spines blank [STYLE] Avoid: [NEG]
- `G103.png`
A single page of a transcript at an angle, the type dissolved to grey, one paragraph marked with a pencil line [STYLE] Avoid: [NEG]
- `G104.png`
A pencil resting in the gutter of an open book, the text unreadable [STYLE] Avoid: [NEG]
- `G105.png`
A wall clock in a plain room with its face blank, hands only [STYLE] Avoid: [NEG]
- `G106.png`
An empty chair at a table, pushed back at an angle as if just left [STYLE] Avoid: [NEG]
- `G107.png`
Venetian blinds half open in an office, hard bars of light across the table [STYLE] Avoid: [NEG]
- `G108.png`
A housing development seen from a distance through a chain-link fence, slightly out of focus [STYLE] Avoid: [NEG]
- `G109.png`
A named-nothing sign post with the plate removed, just the empty bracket [STYLE] Avoid: [NEG]
- `G110.png`
A group of small bicycles left against a wall, no children present [STYLE] Avoid: [NEG]
- `G111.png`
A ball resting still in a corner where two concrete surfaces meet [STYLE] Avoid: [NEG]
- `G112.png`
A skipping rope lying in a loop on a walkway [STYLE] Avoid: [NEG]
- `G113.png`
Small handprints on a painted wall at low height, faint [STYLE] Avoid: [NEG]
- `G114.png`
An open communal doorway seen from inside looking out at bright daylight, figures too far to identify [STYLE] Avoid: [NEG]
- `G115.png`
A dog lying in the shade against a brick wall, chain slack [STYLE] Avoid: [NEG]
- `G116.png`
A woman's back at a door, key in hand, seen from behind at a distance [STYLE] Avoid: [NEG]
- `G117.png`
A key turning in a plain cylinder lock, hand only [STYLE] Avoid: [NEG]
- `G118.png`
A door opening inward onto a dim hallway, from the walkway side, no person [STYLE] Avoid: [NEG]
- `G119.png`
A doormat with nothing on it, seen from directly above [STYLE] Avoid: [NEG]
- `G120.png`
The inside face of a door with no paper on it, the paint scratched near the handle [STYLE] Avoid: [NEG]
- `G121.png`
An empty walkway at first light, everything still [STYLE] Avoid: [NEG]
- `G122.png`
A brick wall with the ghost of removed tape in a rectangle, close [STYLE] Avoid: [NEG]

### ACT_4（16:30–21:30・35枚） — 三つの裁判所。

- `G123.png`
A federal courthouse exterior in flat daylight, wide steps, columns, no signage or seals [STYLE] Avoid: [NEG]
- `G124.png`
The same courthouse from across the street with traffic of the period passing [STYLE] Avoid: [NEG]
- `G125.png`
Courthouse steps from the bottom, empty, wet from rain [STYLE] Avoid: [NEG]
- `G126.png`
A pair of heavy exterior doors closed, brass handles, no lettering [STYLE] Avoid: [NEG]
- `G127.png`
A corridor of a public building with a bench along one wall, nobody on it [STYLE] Avoid: [NEG]
- `G128.png`
A bench outside a closed door, one coat left on it [STYLE] Avoid: [NEG]
- `G129.png`
A closed door with a blank plate where a name would be [STYLE] Avoid: [NEG]
- `G130.png`
A legal brief squared on a desk, its cover blank, a paperclip on the corner [STYLE] Avoid: [NEG]
- `G131.png`
A stack of briefs tied with cotton tape, all blank [STYLE] Avoid: [NEG]
- `G132.png`
A typewriter on a desk with a sheet in the platen, the typing illegible [STYLE] Avoid: [NEG]
- `G133.png`
A carbon paper sheet lifted off a typed page, both illegible [STYLE] Avoid: [NEG]
- `G134.png`
A row of law reports on a shelf, spines uniform and blank [STYLE] Avoid: [NEG]
- `G135.png`
A single volume pulled half out of a shelf of identical volumes [STYLE] Avoid: [NEG]
- `G136.png`
A reading desk under a lamp in a library at night, one closed book on it, nobody there [STYLE] Avoid: [NEG]
- `G137.png`
A wooden library ladder against tall shelves, unattended [STYLE] Avoid: [NEG]
- `G138.png`
An office window at night with a lamp burning, seen from the street below [STYLE] Avoid: [NEG]
- `G139.png`
A hand closing a folder on a desk, sleeve plain, no face [STYLE] Avoid: [NEG]
- `G140.png`
A wire out-tray with a single folder in it [STYLE] Avoid: [NEG]
- `G141.png`
A mail sack open on a floor with plain envelopes inside, none addressed legibly [STYLE] Avoid: [NEG]
- `G142.png`
A postal sorting frame of pigeonholes, most of them empty [STYLE] Avoid: [NEG]
- `G143.png`
A plain envelope on a doormat seen from above, the address dissolved to grey [STYLE] Avoid: [NEG]
- `G144.png`
A letter slot in a door from inside, an envelope halfway through it [STYLE] Avoid: [NEG]
- `G145.png`
A postal van of the period at a kerb, unbranded, doors shut [STYLE] Avoid: [NEG]
- `G146.png`
A bank of dented apartment mailboxes with one door hanging open and nothing inside [STYLE] Avoid: [NEG]
- `G147.png`
A hand posting an envelope into a public letter box, no face [STYLE] Avoid: [NEG]
- `G148.png`
A public letter box on a street corner in the rain [STYLE] Avoid: [NEG]
- `G149.png`
An appellate courthouse exterior, mid-century, plain stone, no signage [STYLE] Avoid: [NEG]
- `G150.png`
A flight of interior stairs in a public building, marble treads worn, nobody on them [STYLE] Avoid: [NEG]
- `G151.png`
An empty lectern in a plain wood-panelled room that is clearly not a courtroom, no bench and no gallery [STYLE] Avoid: [NEG]
- `G152.png`
Three chairs behind a plain table in an empty panelled room [STYLE] Avoid: [NEG]
- `G153.png`
A window in a stone building with rain running down it, the city grey beyond [STYLE] Avoid: [NEG]
- `G154.png`
A briefcase standing closed beside a chair leg [STYLE] Avoid: [NEG]
- `G155.png`
An overcoat on a stand in a corner of an office [STYLE] Avoid: [NEG]
- `G156.png`
A desk calendar with its pages blank, half the month turned [STYLE] Avoid: [NEG]
- `G157.png`
A ceiling of a public building seen from below, plain plaster and one hanging fitting [STYLE] Avoid: [NEG]

### ACT_5（21:30–26:30・35枚） — 判断と反対意見。

- `G158.png`
A single sheet of paper falling through still air against a dark neutral ground [STYLE] Avoid: [NEG]
- `G159.png`
Two identical doors side by side, one with a white rectangle taped to it and one with an envelope on the mat below [STYLE] Avoid: [NEG]
- `G160.png`
A pair of brass scales at rest and level on a plain surface, no ornament [STYLE] Avoid: [NEG]
- `G161.png`
An envelope and a taped sheet lying side by side on a table, both blank [STYLE] Avoid: [NEG]
- `G162.png`
A mailbox with its door forced and hanging, nothing inside [STYLE] Avoid: [NEG]
- `G163.png`
Loose envelopes scattered on the ground beneath a bank of mailboxes [STYLE] Avoid: [NEG]
- `G164.png`
A hand reaching into a mailbox that is empty, no face [STYLE] Avoid: [NEG]
- `G165.png`
An outline map of a country with no borders drawn and no labels, plain paper on a table [STYLE] Avoid: [NEG]
- `G166.png`
Eleven plain pebbles laid out in a line on a wooden surface [STYLE] Avoid: [NEG]
- `G167.png`
A legislative chamber that is empty, seats in curved rows, no emblem or flag [STYLE] Avoid: [NEG]
- `G168.png`
A gallery of empty public seating in a plain hall [STYLE] Avoid: [NEG]
- `G169.png`
A sheet of paper being folded in half by two hands, blank on both sides [STYLE] Avoid: [NEG]
- `G170.png`
The same sheet unfolded and creased, lying flat [STYLE] Avoid: [NEG]
- `G171.png`
A pen held above a blank page, not touching it [STYLE] Avoid: [NEG]
- `G172.png`
A wooden desk drawer opened to reveal blank stationery [STYLE] Avoid: [NEG]
- `G173.png`
A pile of unopened plain envelopes on a hall table [STYLE] Avoid: [NEG]
- `G174.png`
A doorway with light behind it and a figure standing in silhouette, unidentifiable [STYLE] Avoid: [NEG]
- `G175.png`
A curtain moving slightly at a lit window seen from outside at night [STYLE] Avoid: [NEG]
- `G176.png`
A window from inside at night, the walkway lamp visible through the net [STYLE] Avoid: [NEG]
- `G177.png`
An interior door standing open onto an empty room in daylight [STYLE] Avoid: [NEG]
- `G178.png`
An empty room with pale rectangles on the wall where pictures used to hang [STYLE] Avoid: [NEG]
- `G179.png`
A bare mattress on a bedstead in an otherwise empty room [STYLE] Avoid: [NEG]
- `G180.png`
A kitchen with the cupboard doors standing open and the shelves empty [STYLE] Avoid: [NEG]
- `G181.png`
A single cardboard box taped shut on a bare floor [STYLE] Avoid: [NEG]
- `G182.png`
A stack of three cardboard boxes against a wall in an empty room, no labels [STYLE] Avoid: [NEG]
- `G183.png`
A window without curtains in an emptied room, daylight flat [STYLE] Avoid: [NEG]
- `G184.png`
A set of keys on a bare kitchen counter [STYLE] Avoid: [NEG]
- `G185.png`
A door closing, caught with a hand's width of gap left, no person visible [STYLE] Avoid: [NEG]
- `G186.png`
A hallway light switch in the off position, close [STYLE] Avoid: [NEG]
- `G187.png`
A corridor of the housing block at night with every door shut and one bulb out [STYLE] Avoid: [NEG]
- `G188.png`
A pair of hands turning a plain paper over and finding the other side blank as well [STYLE] Avoid: [NEG]
- `G189.png`
Rain on a window at night, the block opposite reduced to blurred lights [STYLE] Avoid: [NEG]
- `G190.png`
A white rectangle on a distant door seen through rain from far away [STYLE] Avoid: [NEG]
- `G191.png`
The wet concrete of a walkway reflecting one lit window [STYLE] Avoid: [NEG]
- `G192.png`
A doorstep in the first light of morning, nothing on it [STYLE] Avoid: [NEG]

### ENDING（26:30–29:00・17枚） — 何が変わり、何が変わらなかったか。

- `G193.png`
The brick housing block at dawn under a clear pale sky, no people, no signage [STYLE] Avoid: [NEG]
- `G194.png`
A door with both a taped sheet and an envelope on the mat below it, both blank [STYLE] Avoid: [NEG]
- `G195.png`
A hand taking an envelope from a mailbox, the address illegible, no face [STYLE] Avoid: [NEG]
- `G196.png`
An envelope opened on a kitchen table, the letter beside it, the text dissolved to grey [STYLE] Avoid: [NEG]
- `G197.png`
A chair pulled out at a kitchen table with a letter on the cloth in front of it, nobody seated [STYLE] Avoid: [NEG]
- `G198.png`
A wide view of the development in late afternoon, long shadows, still no people [STYLE] Avoid: [NEG]
- `G199.png`
A walkway seen end-on with every door bare [STYLE] Avoid: [NEG]
- `G200.png`
A plain modern apartment door in flat light, unmistakably later in period, nothing on it [STYLE] Avoid: [NEG]
- `G201.png`
A stack of legal volumes closed on a desk, spines blank, a lamp off beside them [STYLE] Avoid: [NEG]
- `G202.png`
An empty conference chair at the end of a long plain table [STYLE] Avoid: [NEG]
- `G203.png`
A window of a housing block lit from inside at dusk, curtains drawn, one shadow crossing [STYLE] Avoid: [NEG]
- `G204.png`
The torn top corner of a sheet of paper still under a piece of tape, close, end of the film [STYLE] Avoid: [NEG]
- `G205.png`
A doorstep with a single blade of grass growing through the joint [STYLE] Avoid: [NEG]
- `G206.png`
A wide flat sky over the rooflines of the development, evening, no sun visible [STYLE] Avoid: [NEG]
- `G207.png`
An unopened envelope resting against a skirting board inside a door [STYLE] Avoid: [NEG]
- `G208.png`
A door photographed straight on with the paper freshly taped and flat, identical framing to the opening image [STYLE] Avoid: [NEG]
- `G209.png`
The same door bare, identical framing, the loop closed [STYLE] Avoid: [NEG]

### PEOPLE（10枚） — 人物プレート。**全員実在しない一般人。顔の扱いに注意。**

- `G210.png`
A woman in her thirties in a plain 1970s coat standing at an apartment door with her back to camera, hand on the handle, face not visible [STYLE] Avoid: [NEG]
- `G211.png`
The hands of a woman in her fifties holding a folded sheet of blank paper at a kitchen table, no face in frame [STYLE] Avoid: [NEG]
- `G212.png`
A man in his forties in plain workwear seen from behind at the foot of a concrete stairwell, face not visible [STYLE] Avoid: [NEG]
- `G213.png`
A woman's silhouette against a net curtain from inside a dim room, features not resolvable [STYLE] Avoid: [NEG]
- `G214.png`
Two adults seated at a kitchen table seen from behind, shoulders and backs of heads only [STYLE] Avoid: [NEG]
- `G215.png`
A pair of working hands resting on a formica table top, no face, no jewellery [STYLE] Avoid: [NEG]
- `G216.png`
A woman in a plain dress standing at a window with her back to camera, looking out at a brick block [STYLE] Avoid: [NEG]
- `G217.png`
An adult's hand and a child's hand held together at waist height, both cropped at the wrist, no faces [STYLE] Avoid: [NEG]
- `G218.png`
A person in an overcoat walking away down an empty walkway, seen from far behind [STYLE] Avoid: [NEG]
- `G219.png`
The back of a woman's head and shoulders in a hallway facing an open front door, face not visible [STYLE] Avoid: [NEG]

### THUMB（3枚） — サムネ候補。**縦横比は16:9のまま。文字は焼き込まない。**

- `G220.png`
A single blank sheet of paper taped to a plain door, shot dead centre and close, hard directional light, the composition leaving the upper third clear for a headline [STYLE] Avoid: [NEG]
- `G221.png`
A woman's silhouette on the inside of a drawn curtain with a white rectangle visible on the door beside the window, dramatic side light, upper third clear [STYLE] Avoid: [NEG]
- `G222.png`
A torn corner of paper still stuck under tape on an otherwise bare door, extreme close, strong contrast, upper third clear [STYLE] Avoid: [NEG]

---

## 5.5 ショート3本のプレートは、この222枚の**内数**です

`SHORTS_SLATE_EP62-65.v001.md` の `short182` / `short183` / `short184` が要求するモチーフを、上のプロンプトに
1つずつ突き合わせた表です。**ショート用の二度目の発注は出しません。**

| short182「通知は剥がれた」 | 使うプレート |
|---|---|
| ドアに貼られた紙（フック＝1コマ目） | `G001` |
| 画鋲の寄り / テープの剥がれ | `G003` `G004` |
| 低層レンガの集合住宅 / 同じドアの並ぶ通路 | `G018` `G005` |
| 子どもの背丈のドア枠 / 手の届かない高さに貼り直す手 | `G010` `G093` `G094` |
| 段の下に落ちた紙 / 階段室 | `G006` `G021` |
| 灯った窓のカーテンが動く / カーテンを横切る影 | `G175` `G030` |
| 証言録取の部屋（椅子2脚） / テープで括られた記録 | `G095` `G131` |
| 何も貼られていないドア（＝落ち） | `G087` |
| ループ結合＝1コマ目に戻る | `G208` → `G209` |

| short183「一度叩いて、留守。それで終わり」 | 使うプレート |
|---|---|
| 触れる直前の拳（フック＝1コマ目） | `G008` `G067` |
| ドアから見た無人の通路 | `G064` |
| ドアの下の光の線（在/不在） | `G065` `G068` |
| 真昼の腕時計 / 昼間の空き部屋 | `G063` `G026` |
| 勤務中であることの痕跡（タイムレコーダー・洗濯工場・清掃台車） | `G035` `G036` `G037` |
| バス停 | `G033` |
| 空白のカレンダー | `G047` |
| 記録の棚 / 手袋の手の令状 | `G134` `G053` |
| ループ結合 | `G121` → `G008` |

| short184「反対意見＝郵便受けは荒らされる」 | 使うプレート |
|---|---|
| へこんだ郵便受けの列（フック＝1コマ目） | `G022` `G146` |
| こじ開けられた郵便受け / 空の郵便受けに伸びる手 | `G162` `G164` |
| 玄関マットの封筒 / 郵便車 / 投函する手 | `G143` `G145` `G147` |
| ラベルの無い地図 / 11個の小石 | `G165` `G166` |
| 無人の議場 | `G167` `G168` |
| 準備書面の束 / 紙の上のペン | `G131` `G171` |
| 遠くのドアの白い長方形 | `G190` |
| ループ結合 | `G143` → `G022` |

> **縦位置の制約。** ショートは 1080×1920 です。上の表に出るプレートは**主題が中央にあり、左右を切っても
> 意味が壊れない**こと。生成後の目視で、**9:16に切ったサムネイルも並べて確認**してください。
> 端に寄った構図（例：`G088` の画面端の小さな手）はショートに使わず、長尺のみに使います。

---

## 6. 生成後にやること（発注者側）

1. **全222枚をラベル付きコンタクトシートで目視**する。プロンプトIDで選ばない
   （short60は3枚がプロンプト一覧どおりに選んで別の絵だった）。
2. `episodes/PD-2026-062-greene/episode_spec.v001.json` の `mandatory_stills` に **G001〜G222 を全部書く**。
   空のままだと `check_spec_satisfied.py` の唯一の保護が無効になります。
3. 1枚 = 1モーションクリップとして `remotion/public/greene/motion/` に書き出す
   （i2v または深度パララックス。**ズーム/パンだけは不可**）。
4. `python scripts/check_episode_inputs.py --slug greene` で
   **accepted(12) + motion ≥ 234** をレンダー前に確認する。
