# EP64 memphis — Codex 画像生成 **1本で完結する発注** v001（210枚・1プロンプト1枚）

> ## ✅ 今すぐ着手してよいファイルです。**追加バッチは出ません。**
> 順番は EP62 と同じで、**測ってから発注**しています。実写を先に測り（81本取り込み・
> コンタクトシート5枚を全タイル目視・使えるのは **24本**）、**台本の実語数を区分ごとに数え**、
> 語数比で枚数を割り付けてからプロンプトを書きました。**どの区分にも絵があります。**
> 枚数の根拠は `EP62_65_IMAGE_BUDGET.v001.md`：契約 `distinct_video_assets` 234 − 実写採用24 = **210**。

**題材:** *Memphis Light, Gas & Water Division v. Craft*, 436 U.S. 1 (1978)。
テネシー州メンフィス、1972〜1978年。二世帯住宅だった平屋を買った一家の壁には、**ガスメーターが2つ、
電気メーターが2つ、水道メーターが1つ**あった。売主は「2組目は死んでいる」と言った。回っていた。
1973年から**請求書が毎月2通**届きはじめる。2通目の名義は **Willie C. Craft** — 実際に住んでいたのは
**Willie S. Craft**。**1文字違い。** 電気は5回止まり、その間、どこへ行って何を言えばいいのかを
誰も教えなかった。

**この映画は「請求ミスの話」ではありません。**主題は**紙**です。止める前に、
「どこで・何時に・誰の前で」争えるのかを**知らせる義務**があったか。
そして最高裁は、**聴取のあとで止める権限は残した**とはっきり書いています。

---

## 0. ★★★ 最重要：1プロンプト = 1枚 ★★★

1. **各プロンプトから画像を1枚だけ作る。** 同じプロンプトで2枚目を作らない。
2. **`_02` / `_03` を作らない。**
3. **「良いのが出るまで回す」を禁止する。**
4. 作り直してよいのは §1 の禁止に触れたときだけ。そのときも**文言を直してから1枚**。

EP60はこの規則で **279枚・変種0・指定外0・sha256重複0・知覚的近似重複0** を達成済み。

### 0.5 ★作画の水準（オーナー指示 2026-08-04）

この4話の craft 基準は**アカデミー／パルムドールの脚本水準**に置かれています。絵も同じです。
**視点のある写真を作ってください。**各プロンプトは意図的に3つを指定してあります。

- **距離**（何メートルから見ているか・どこから覗いているか）
- **光**（方向と質。「霞を通した朝日が左から」「窓の桟の影が横切る」）
- **瞬間**（何が起きた直後か、何が起きる直前か。「コードの最後の揺れがもう止まっている」）

**カタログ調（対象が真ん中にきれいに置かれ、光がどこからでもなく、時間が止まっていない絵）は
不合格**にしてください。抽象的なきれいさより、**その一枚が何を語るか**が優先です。

---

## 1. ★絶対条件（触れた絵は使用不可）

`episodes/PD-2026-064-memphis/episode_spec.v001.json` の `forbidden_subjects` がこの節の正典です。

- **★この話で最大の事故：因果の絵を作らない。** 家の火事・凍える人・毛布にくるまった子ども・
  倒れた人・遺体・寒さの被害。**一切。** 判決文は「止まったせいで何かが起きた」とは一度も書いて
  いません（反対意見は逆に *the record does not reveal any actual case of harm to health or safety*
  と書いています）。**寒がる子どもの絵を1枚入れた瞬間に、適正手続の話が因果の主張にすり替わります。**
  必要な「必需品」の register は**人のいない冷えた器物**（消えたガスリング・点いていない暖房器具・
  冷たい蛇口）で出す。人を苦しめない。
- **公益事業の作業員を悪役として描かない。** 制服・制帽・バッジ・ドアの前に立ちはだかる人影は不可。
  検針員が出るのは**道具と手だけ**（鞄・ルートブック・メーター板に伸びる袖）。
- **Craft一家を描かない。** 実在人物の肖像も一切描かない。人物は全員「実在しない一般人」。
- **読める文字・数字・署名・印章・ロゴを描かない。** 特に**請求書・最終通知・メーターの目盛り・
  台帳カード**は繰り返し画面に出ます。**すべて判読不能**に描く。ここが事故の最頻発点です。
- **法廷を描かない。** 法廷内観・木槌・判事席。棚の法廷映像は23/24が使用済みで、絵も作りません。
  **裁判所は外観のみ可。**
- **監獄を描かない。** 鉄格子・有刺鉄線・独房・手錠。収監の話ではありません。
- **実在と特定できる建物を描かない。** 看板・紋章・特徴的な建築で場所が割れる絵は不可。
- **1970年代でないものを描かない。** デジタル表示・現代のスマートメーター・現代の家電・
  80年代以降の車。**この話は1970年代です。**
- **広告調にしない。** 黄金色の夕陽、絵葉書の風景、くつろぐ暖炉、クリスマス、ドローンの映え。
  実写側で暖炉ループを7本落としています。同じ絵を発注で作り直さない。
- **同情の演出を禁止する。** 肩に置かれた手、涙、カウントダウンする時計、寄り添う老夫婦。
- **黒つぶれさせない。** スマホで見て何が写っているか分かること。

### ★実写の在庫と衝突させない（この発注固有の制約）

`runs/qc/memphis_clip_verdicts.v001.json` の採用24本は **ろうそく5本・マッチ3本**に偏っています。
残りは炎・冬・カーテン・壁の影・ガスリング2本・街灯1本。
**したがって、この発注では「ろうそく」「マッチ」を1枚も作りません。**`[NEG]` に名指しで入れてあります。
カーテン・壁の影・冬の街も最小限にとどめ、代わりに**棚に存在しない register**（下記）を厚く作ります。

**棚に存在しない＝この発注が作るしかないもの**（142,000行の全文検索で0件。`heater` は *theater* を返す）:

| 無いもの | このバッチでの担当 |
|---|---|
| **電気メーター／ガスメーター** — **映画の冒頭画** | `M001` `M002` `M013` `M019` `M025` `M030` `M066` `M141` `M190` `M197` `M208` |
| 暖房器具・ラジエーター | `M109` `M110` |
| ヒューズボックス・配電盤 | `M033` `M105` `M106` `M107` |
| 電線・引込線 | `M008` `M010` |

---

## 2. スタイル（★必ず展開してから生成）

**`[STYLE]`** ＝ 末尾にそのまま連結:

> , cinematic still, muted natural colour, flat humid Tennessee light with haze standing in it, low contrast, low-key but never crushed: shadows keep their detail and the frame reads clearly on a phone screen, soft falloff toward the edges, shallow depth of field, restrained documentary framing with a point of view, Memphis in the middle 1970s — a modest single-storey frame house with painted weatherboard, worn linoleum, formica, enamel, bakelite, an ordinary working household, municipal offices of the same decade in steel and wood, nothing staged for advertising, ultra-detailed, photoreal, 4K, 16:9, fine film grain, no text, no lettering, no numerals, no watermark, no logo, no signage

**`[NEG]`** ＝ `Avoid:` の後にそのまま連結:

> text, lettering, numerals, digits, readable dial figures, handwriting, signatures, seals, emblems, logos, signage, house numbers, street signs, fire, flame, a burning building, smoke rising from a house, a person shivering, a person wrapped in blankets against the cold, frost on skin, a body, an injured or unconscious person, a crying child, uniform, cap insignia, badge, patrol car, a figure looming in a doorway, courtroom interior, gavel, judge's bench, prison bars, razor wire, handcuffs, a hand on a shoulder, a tear, a clock counting down, candle, lit match, cosy fireplace, golden hour, sunset glow, postcard scenery, drone shot, Christmas, tropical, modern appliances, smart meter, digital display, LED, modern cars, catalogue product lighting, centred symmetrical stock composition, flat CGI, cartoon, illustration, oversaturated

---

## 3. 命名と保存先

- ファイル名 `M001.png` … `M210.png`。**欠番を作らない。**
- 保存先 `H:\pd-media\assets\ai\memphis\`。
- 長辺 3840px 以上・16:9・PNG。

---

## 4. 区分と枚数（合計210枚）— **台本の実語数から割り付けた**

`episodes/_planning/EP64_memphis_script.en.v001.md` を機械で数えた結果（発話語のみ。見出し・
`【】`ディレクション・`⟨HELD⟩` を除外）。**合計 5,354語。**契約の実測レート（約176語／完成1分）で
分に直すと **30.4分**で、契約 `runtime_seconds` [1620, 1920] の内側に入ります。

| 区分 | 実語数 | 語数比 | 推定尺 | 比例配分 | **発注枚数** | 1分あたり | 中身 |
|---|---:|---:|---:|---:|---:|---:|---|
| HOOK | — | — | **8秒** | — | **5** | — | ★下記。本編最強の4〜5カットのフラッシュフォワード |
| OP | 62 | 1.16% | 0.35分 | 2 | **5** | 14.3 | ブランド。無地のテクスチャ |
| ACT_1 | 681 | 12.72% | 3.87分 | 25 | **25** | 6.5 | 1972年の入居から1974年の提訴まで。誰の過ちかが二重になる |
| ACT_2 | 984 | 18.38% | 5.59分 | 36 | **36** | 6.4 | 市営という事実。4段階の時計。通知と2種類のちらし。書かれなかった梯子 |
| ACT_3 | 741 | 13.84% | 4.21分 | 27 | **27** | 6.4 | 地裁で負けた負け方。35ドル。誰も金額を決めなかった |
| ACT_4 | 1068 | 19.95% | 6.07分 | 40 | **39** | 6.4 | 財産権・通知の水準・聴取。コンピュータ依存。訴訟費用の方が高い |
| ACT_5 | 1424 | 26.60% | 8.09分 | 53 | **52** | 6.4 | 止める権限は残る。反対意見（数字・電話・同じ事実の反転） |
| ENDING | 224 | 4.18% | 1.27分 | 8 | **8** | 6.3 | 何が決まり、何が決まらなかったか。電話へのコールバック |
| PEOPLE | — | — | — | — | **10** | — | 人物プレート（顔なし規則・`people_plates_min: 10`） |
| THUMB | — | — | — | — | **3** | — | サムネ候補（`thumbnail_candidates_min: 3`） |
| **計** | **5,354** | 100% | **30.4分** | | **210** | | |

*（HOOK の170語は現行台本の旧60秒版のもので、下記のとおり書き直されます。比例配分列は
残り197枚を6区分＋OPの語数比で最大剰余法により割り付けた値です。）*

### ★ HOOK は8秒（オーナー指示 2026-08-04・`docs/PD_ONE_PASS_PRODUCTION_SPEC.v2.md` 行9）

HOOK は約60秒の語りではなく、**8秒のフラッシュフォワード**になります。**約2秒カット×4**、
決め台詞1本、問いを開いたまま本編へ。したがって、

- **HOOK に固有の絵は作りません。** 5枚は**本編で最も強い絵**であり、
  **全てが後段でもう一度出ます**（行9の promise-payoff 要件）。
- 冒頭画は議論の余地なく**壁に並んだ2つのメーター**です。事件の第一事実であり、
  **棚に存在しない**register で、この映画にしか無い絵です。

| HOOK | 絵 | 後段での payoff |
|---|---|---|
| `M001` | 壁に並ぶ2つのガスメーター（1コマ目） | ACT_1 `M013`（2組が同時に写る側面）／ENDING `M190` |
| `M002` | 回っている電気メーターの円盤 | ACT_1 `M019` `M025`／ENDING `M197` |
| `M003` | 罫線まで一致する2通の請求書 | ACT_1 `M021` `M022`／ENDING `M191` |
| `M004` | 真昼に照明の消えた廊下 | ACT_5 `M174` `M175` `M176` |
| `M005` | 台に戻されないまま垂れた受話器 | ACT_5 `M146`–`M149`／ENDING `M193` |

ID割り当て（欠番なし・重複なし）:
`HOOK M001–M005` / `OP M006–M010` / `ACT_1 M011–M035` / `ACT_2 M036–M071` /
`ACT_3 M072–M098` / `ACT_4 M099–M137` / `ACT_5 M138–M189` / `ENDING M190–M197` /
`PEOPLE M198–M207` / `THUMB M208–M210`

---

## 5. プロンプト（各1枚）

### HOOK（8秒・5枚） — 本編最強の絵だけ。全て後段で回収される。

- `M001.png`
Two domestic gas meters bolted side by side on the painted weatherboard wall of a modest single-storey house, framed straight on from a metre away so the pair fills the frame and the doubling is the whole subject, dial faces blank and unreadable, the first sun pushing through Tennessee haze from the left so each meter lays its own hard shadow across the boards [STYLE] Avoid: [NEG]
- `M002.png`
Extreme close on the glass dome of an electric meter at the instant the disc inside is turning, the disc smeared by its own movement while the dust on the outside of the glass stays needle sharp, the surrounding scale rubbed smooth and blank, the wall behind thrown to nothing [STYLE] Avoid: [NEG]
- `M003.png`
Two identical bills laid one across the other on a formica kitchen table, shot from directly above from waist height, the rulings matching line for line and every character dissolved to grey, the shadow of a window bar falling across both sheets in low afternoon light [STYLE] Avoid: [NEG]
- `M004.png`
The hallway of a small house at midday with every light out, shot from the dark end so the passage reads as a tunnel toward the glazed front door, dust standing motionless in the single shaft of daylight, nobody in it [STYLE] Avoid: [NEG]
- `M005.png`
A wall-mounted kitchen telephone with the handset lifted off its cradle and hanging on the coiled cord, shot close from below against a dim ceiling at the moment the cord's last swing has already stopped, nobody in frame [STYLE] Avoid: [NEG]

### OP（62語・5枚） — ブランド。無地。

- `M006.png`
A flat field of painted weatherboard filling the frame at arm's length, one proud nail head casting a shadow no longer than itself, overcast light with no direction in it [STYLE] Avoid: [NEG]
- `M007.png`
The cast-iron body of a gas meter at extreme magnification, the paint lifted in scales along a seam, raking light from one side so each scale has an edge, no dial in frame [STYLE] Avoid: [NEG]
- `M008.png`
A plain overcast Tennessee sky filling the frame, shot from directly beneath a service cable that crosses one corner and leaves the rest empty [STYLE] Avoid: [NEG]
- `M009.png`
The fibrous torn edge of an ordinary paper bill at extreme magnification, back-lit so the raised fibres glow and the sheet itself stays grey, nothing printed on it [STYLE] Avoid: [NEG]
- `M010.png`
A run of copper and iron pipework against a wall in hard raking side light from the right, every joint and union picked out by its own shadow, no building visible around it [STYLE] Avoid: [NEG]

### ACT_1（681語・25枚） — 1972年の入居から1974年の提訴まで。誰の過ちかが二重になる。

- `M011.png`
A modest single-storey house seen from across a humid front lawn in flat October light, shot from the far kerb so the lawn takes the bottom third, the curtains drawn and nobody about [STYLE] Avoid: [NEG]
- `M012.png`
A single water meter set in a concrete pit in the grass beside a garden path, the lid tipped back on its hinge, the mechanism below dark with standing damp, shot from standing height looking straight down [STYLE] Avoid: [NEG]
- `M013.png`
The side wall of the house framed wide enough that both sets of meters read at once, gas and electric doubled along the same boards, every dial face blank, late morning light skimming the wall from the left [STYLE] Avoid: [NEG]
- `M014.png`
A removal carton set down on the bare boards of an empty front room, the room otherwise stripped, daylight falling in one uncurtained rectangle beside it [STYLE] Avoid: [NEG]
- `M015.png`
The front elevation of the house showing two front doors where a partition once divided it, the second one painted over and its threshold unworn, shot square on from the path [STYLE] Avoid: [NEG]
- `M016.png`
An interior doorway cut through a former partition wall, shot from the dark side so the newer plaster reads against the old, the join in the floorboards running out toward the camera [STYLE] Avoid: [NEG]
- `M017.png`
A second front door boarded over from the inside, seen from a dim hallway three paces back, one line of daylight along the bottom of the boards [STYLE] Avoid: [NEG]
- `M018.png`
A kitchen in a modest 1970s Memphis house shot from the doorway, enamel sink, a kettle on the gas ring, morning light through a small window and nobody there [STYLE] Avoid: [NEG]
- `M019.png`
A hand raised toward the glass of an electric meter and stopped short of touching it, no face, the dial unreadable behind the reflection of an overcast sky [STYLE] Avoid: [NEG]
- `M020.png`
Two windowed envelopes standing upright in a wire rack on a kitchen shelf, shot at shelf height so they lean against each other, the printing on both reduced to grey [STYLE] Avoid: [NEG]
- `M021.png`
A printed bill folded in three on a formica table, its columns dissolved to plain grey, the two creases still holding the sheet half shut [STYLE] Avoid: [NEG]
- `M022.png`
A close view of the top corner of a bill where an account line would sit, the paper filling the frame at an angle, the printing deliberately unresolved and one fingertip just entering the corner [STYLE] Avoid: [NEG]
- `M023.png`
Two envelopes held apart by two hands so they sit side by side against a kitchen wall, no face in frame, the printing on both reduced to grey, one held fractionally higher than the other [STYLE] Avoid: [NEG]
- `M024.png`
A meter reader's canvas satchel and a route board set down on a concrete step, shot from a crouch so the step runs out of frame, no person and nothing marked on either [STYLE] Avoid: [NEG]
- `M025.png`
A gloved hand wiping dust from the glass of a gas meter in one stroke, only the forearm in frame, a plain sleeve with nothing on it, the cleared arc of glass brighter than the rest [STYLE] Avoid: [NEG]
- `M026.png`
A pipe wrench and a spool of solder on a folded cloth beside an opened meter housing, shot from directly above at the moment the work is stopped, not finished [STYLE] Avoid: [NEG]
- `M027.png`
Two gas pipes cut and capped with a new union half made up between them, close and slightly below so the unfinished thread reads, work light from one side [STYLE] Avoid: [NEG]
- `M028.png`
An electrical junction opened on a wall with the conductors twisted and taped, the cover leaning against the skirting where somebody set it down, harsh light from a hand lamp out of frame [STYLE] Avoid: [NEG]
- `M029.png`
A conduit run stopping short of a second meter position, the empty mounting bracket still bolted to the wall beyond the last fixing, flat overcast light [STYLE] Avoid: [NEG]
- `M030.png`
A single meter standing where two used to be, the paler unweathered rectangle of the removed one still on the boards beside it, shot square on so the absence is the subject [STYLE] Avoid: [NEG]
- `M031.png`
A contractor's invoice pad lying face down on a kitchen table beside a pencil, nothing showing, the pencil rolled to a stop against the pad [STYLE] Avoid: [NEG]
- `M032.png`
A wall calendar in a small kitchen with its grid blank and unreadable, winter afternoon light crossing it at a low angle so the curl of the page throws a shadow across the month [STYLE] Avoid: [NEG]
- `M033.png`
A domestic fuse panel opened on a hallway wall, the porcelain carriers pulled half out and left that way, nothing labelled anywhere on it, light only from the room behind the camera [STYLE] Avoid: [NEG]
- `M034.png`
A woman's coat and handbag being lifted from a hook by a door, only the hands in frame, no face, the coat still holding the shape of the hook [STYLE] Avoid: [NEG]
- `M035.png`
A city bus pulling away from a kerb on a humid Memphis morning seen from the pavement it has just left, nothing advertised on its flank, exhaust hanging in the flat light [STYLE] Avoid: [NEG]

### ACT_2（984語・36枚） — 市営という事実。4段階の時計。通知と2種類のちらし。書かれなかった梯子。

- `M036.png`
A municipal utility office building of the period seen from the far pavement in flat light, plain brick, a blank stone panel above the entrance where a name would be cut [STYLE] Avoid: [NEG]
- `M037.png`
An empty boardroom with a long table and a ring of chairs, shot from the foot of the table, plain panelling and nothing at all on the wall behind the head chair [STYLE] Avoid: [NEG]
- `M038.png`
A public service counter with its shutter half drawn and nobody behind it, shot from the customer's side of the ledge at chest height [STYLE] Avoid: [NEG]
- `M039.png`
A row of linked waiting chairs against the wall of a municipal office, every seat empty, shot down the row so the seats compress into a single line [STYLE] Avoid: [NEG]
- `M040.png`
A ticket dispenser on a counter post with a blank paper tongue hanging from its slot, close, the paper curled from having hung there a long time [STYLE] Avoid: [NEG]
- `M041.png`
A wire in-tray stacked with identical printed slips, the printing on all of them reduced to grey, low side light so the stack shows every edge [STYLE] Avoid: [NEG]
- `M042.png`
A wall of pigeonholes behind a counter with a single plain envelope in most compartments, shot square on so the grid fills the frame [STYLE] Avoid: [NEG]
- `M043.png`
A metal card index drawer pulled fully open, the cards packed edge to edge and none of them marked, shot from above and along so the drawer runs to a vanishing point [STYLE] Avoid: [NEG]
- `M044.png`
A wall of card index cabinets in an office, drawer fronts in ranks to the ceiling, nothing labelled anywhere, one drawer left standing an inch proud [STYLE] Avoid: [NEG]
- `M045.png`
A mail room bench with a franking machine and a canvas bag of plain envelopes beside it, shot from the working side at the end of a shift [STYLE] Avoid: [NEG]
- `M046.png`
A canvas mail sack open on a floor with plain windowed envelopes spilling from the mouth of it, shot from a crouch so the spill comes toward the camera [STYLE] Avoid: [NEG]
- `M047.png`
An envelope lying on a doormat inside a front door seen from directly above, the address dissolved to grey, the light from the letter slot still lying across it [STYLE] Avoid: [NEG]
- `M048.png`
A printed final notice lying alone at the centre of a kitchen table, the whole sheet reduced to grey with one heavy rule across it, shot square from above under a bare hanging bulb [STYLE] Avoid: [NEG]
- `M049.png`
The same slip held up flat against a window so the daylight comes through it, the printing dissolved entirely and the ghost of the reverse side showing through [STYLE] Avoid: [NEG]
- `M050.png`
A folded flyer half out of a bill envelope on a counter, both of them blank, shot at counter height so the flyer's fold stands up off the surface [STYLE] Avoid: [NEG]
- `M051.png`
Two differently folded flyers laid side by side on a table, one noticeably smaller than the other, neither carrying a mark, shot from above under one lamp [STYLE] Avoid: [NEG]
- `M052.png`
A small neighbourhood storefront office with a plain glass door and a desk visible inside, shot from across a quiet street, nothing lettered on the glass [STYLE] Avoid: [NEG]
- `M053.png`
A desk in a small counselling office with two chairs drawn up facing it, shot from the doorway, nobody in the room and the blind half down [STYLE] Avoid: [NEG]
- `M054.png`
A closed office door with an empty brass frame where a name card would slide in, close and slightly to one side so the frame catches the corridor light [STYLE] Avoid: [NEG]
- `M055.png`
A short flight of interior stairs in a municipal building, the treads worn hollow along the middle, shot from the bottom looking up, nobody on them [STYLE] Avoid: [NEG]
- `M056.png`
A corridor of frosted glass doors receding, all of them shut, one light still on beyond the last, shot from the corridor's dark end at head height [STYLE] Avoid: [NEG]
- `M057.png`
A steel office desk with a telephone, a blotter and a wire tray, the chair pushed back and empty, shot from where a visitor would stand [STYLE] Avoid: [NEG]
- `M058.png`
A larger wooden desk further along the same corridor, better lit and better furnished, nobody at it, shot from the same standing height as the steel desk [STYLE] Avoid: [NEG]
- `M059.png`
A telephone handset lying off its cradle on a desk blotter, the coiled cord pulled taut out of frame, shot close from the desk's own level [STYLE] Avoid: [NEG]
- `M060.png`
A switchboard of unlit indicator lamps and dark jack fields filling the frame, the operator's chair pushed back and empty, one work light throwing everything else into shadow [STYLE] Avoid: [NEG]
- `M061.png`
A room of paired desks with a telephone handset on every one of them, every seat empty, strip lighting overhead and the whole room shot from the door [STYLE] Avoid: [NEG]
- `M062.png`
A meter reader's route book open on a car seat, its ruled columns dissolved to grey, a pencil lying in the fold, shot from the driver's side through an open door [STYLE] Avoid: [NEG]
- `M063.png`
An unbranded panel van parked at a residential kerb with its side door slid open and nothing visible inside, shot from across the road in flat light [STYLE] Avoid: [NEG]
- `M064.png`
A pair of work boots standing on a concrete doorstep, only the boots and the lower doorframe in frame, shot from the ground at the height of the step [STYLE] Avoid: [NEG]
- `M065.png`
A hand holding out a small paid receipt on a doorstep, the slip blank, no face, a plain cuff, the paper caught at the instant it is offered and not yet taken [STYLE] Avoid: [NEG]
- `M066.png`
The meter position on a house wall photographed straight on with a padlock hanging open on the isolating handle, the shackle swung clear, hard midday light [STYLE] Avoid: [NEG]
- `M067.png`
A sealed cover clipped over a gas meter's control with the seal wire twisted tight, close enough that the twist fills a third of the frame, nothing stamped on the seal [STYLE] Avoid: [NEG]
- `M068.png`
An accounting machine of the early 1970s on a steel desk with a wide sheet in its platen, the print dissolved to grey, shot from the operator's chair with the room dark behind [STYLE] Avoid: [NEG]
- `M069.png`
A rack of magnetic tape reels in a machine room, the room otherwise empty, shot along the rack so the reels repeat away into shallow focus [STYLE] Avoid: [NEG]
- `M070.png`
A concertina of continuous printer paper spilling from a line printer into a basket, every line reduced to grey, caught mid-fall so the paper is still moving [STYLE] Avoid: [NEG]
- `M071.png`
A rules book chained to a counter post by a brass chain, hanging open at a blank spread, shot from the customer's side where it would have to be read standing up [STYLE] Avoid: [NEG]

### ACT_3（741語・27枚） — 地裁で負けた負け方。35ドル。誰も金額を決めなかった。

- `M072.png`
A federal courthouse exterior in flat humid daylight, wide steps and plain stone, shot from across the road at street level, no plate and nothing at all cut into the stone [STYLE] Avoid: [NEG]
- `M073.png`
The same steps from the bottom, empty, the stone still dark and wet from rain that has just stopped [STYLE] Avoid: [NEG]
- `M074.png`
A pair of heavy exterior doors closed, brass push plates rubbed bright by hands, nothing lettered on them, shot square on from three paces [STYLE] Avoid: [NEG]
- `M075.png`
A public corridor with a bench along one wall and a terrazzo floor, shot from bench height so the floor runs away, nobody on the bench [STYLE] Avoid: [NEG]
- `M076.png`
A closed door in a public building with a blank plate mounted beside it, the corridor light falling on the plate from one side [STYLE] Avoid: [NEG]
- `M077.png`
A bound trial transcript closed on a plain desk, its cover unmarked, shot at desk level so the block of pages reads as a solid object [STYLE] Avoid: [NEG]
- `M078.png`
A stack of transcripts tied with cotton tape on a shelf, every cover blank, the tape cutting into the topmost one [STYLE] Avoid: [NEG]
- `M079.png`
A single transcript page at an angle under a desk lamp, the type dissolved to grey, one paragraph scored down its margin with a pencil line drawn hard enough to dent the paper [STYLE] Avoid: [NEG]
- `M080.png`
A typewriter on a steel desk with a sheet in the platen, the typing illegible, shot from the typist's seat with the room going dark beyond the machine [STYLE] Avoid: [NEG]
- `M081.png`
A carbon sheet being lifted away from a typed page, both surfaces unreadable, caught at the instant of separation with light passing between them [STYLE] Avoid: [NEG]
- `M082.png`
A rubber date stamp resting face up on an ink pad, its face worn smooth and blank, close under a single desk lamp [STYLE] Avoid: [NEG]
- `M083.png`
A wire out-tray holding one closed folder on an otherwise clear desk, shot from above so the empty desk takes most of the frame [STYLE] Avoid: [NEG]
- `M084.png`
A cheque stub pad open on a desk beside a fountain pen, every line on it blank, the pen capped and set down parallel to the pad [STYLE] Avoid: [NEG]
- `M085.png`
A small printed credit slip lying alone on a formica table, the amount dissolved to grey, shot from above with the table's whole worn surface around it [STYLE] Avoid: [NEG]
- `M086.png`
Coins counted into two small piles on a kitchen table, two hands only and no face, one pile visibly shorter than the other [STYLE] Avoid: [NEG]
- `M087.png`
A ledger card held up to a window, its ruled columns visible against the daylight and nothing written in any of them [STYLE] Avoid: [NEG]
- `M088.png`
A drawer of ledger cards with one card standing proud of the rest, none of them marked, shot from directly above and close [STYLE] Avoid: [NEG]
- `M089.png`
Two identical printed slips pinned side by side on a plain board, both reduced to grey, shot square on so nothing distinguishes one from the other [STYLE] Avoid: [NEG]
- `M090.png`
A registered mail receipt book open on a post office counter, every ruled line blank, shot from the customer's side with the counter's chipped edge in the foreground [STYLE] Avoid: [NEG]
- `M091.png`
A pair of small brass scales at rest and dead level on a plain desk, no ornament on them, one raking light so both pans read [STYLE] Avoid: [NEG]
- `M092.png`
A law library reading desk under a lamp at night with one closed volume on it, nobody there, the shelves beyond falling into darkness [STYLE] Avoid: [NEG]
- `M093.png`
A run of law reports on a shelf with plain unmarked spines, shot at an oblique angle so the run compresses toward the edge of frame [STYLE] Avoid: [NEG]
- `M094.png`
A single volume drawn half out of a shelf of identical volumes, the gap beside it dark, shot straight on at shelf height [STYLE] Avoid: [NEG]
- `M095.png`
A wooden library ladder standing against tall shelves, unattended, shot from the floor looking up along the rails [STYLE] Avoid: [NEG]
- `M096.png`
An appellate courthouse exterior in mid-century stone, plain, no plate anywhere on it, shot low from the pavement so the building leans away [STYLE] Avoid: [NEG]
- `M097.png`
A briefcase standing closed against a chair leg in an empty corridor, shot from the floor so the corridor runs away above it [STYLE] Avoid: [NEG]
- `M098.png`
An empty lectern in a plain panelled room that is clearly not a court, no bench and no gallery behind it, shot from where a speaker would stand [STYLE] Avoid: [NEG]

### ACT_4（1,068語・39枚） — 財産権・通知の水準・聴取。コンピュータ依存。訴訟費用の方が高い。

- `M099.png`
A doorway standing open onto a lit hallway seen from a dark room, shot from deep inside the dark so the lit doorway is a small bright rectangle, nobody in either [STYLE] Avoid: [NEG]
- `M100.png`
A threshold seen from directly above, a worn brass strip dividing two floor coverings, the wear heaviest at the centre where feet have crossed [STYLE] Avoid: [NEG]
- `M101.png`
A brass key held between two fingers a hand's width above a plain door lock, no face, the key not yet in the keyway [STYLE] Avoid: [NEG]
- `M102.png`
A statute volume closed on a desk with a slip of paper marking a place in it, the spine plain, low lamp light along the edge of the pages [STYLE] Avoid: [NEG]
- `M103.png`
A page held up to a window so the light passes through it, the type dissolved to grey, two fingers pinching one corner [STYLE] Avoid: [NEG]
- `M104.png`
A pair of pipe cocks on a wall, one turned open and one turned shut, close and square on so the difference between them is the only subject [STYLE] Avoid: [NEG]
- `M105.png`
An isolating switch on a meter board in the on position, the handle worn smooth by years of hands, nothing marked around it, flat light [STYLE] Avoid: [NEG]
- `M106.png`
The same isolating switch thrown to the off position, identical framing, the room behind it now dark [STYLE] Avoid: [NEG]
- `M107.png`
A wall switch in the down position with a bare ceiling fitting above it, shot close from below so the dead fitting hangs over the switch [STYLE] Avoid: [NEG]
- `M108.png`
A domestic gas ring unlit and cold with an empty pan standing on it, the burner ports dark, shot from directly above under a window's grey light [STYLE] Avoid: [NEG]
- `M109.png`
A parlour heater of the period standing unlit against the wall of an empty room, plain pressed metal with no glow anywhere in it, shot at its own height from two paces [STYLE] Avoid: [NEG]
- `M110.png`
A cast-iron radiator under a window in an empty room, the paint chipped along the top rib, the valve closed tight, winter daylight falling straight down its face [STYLE] Avoid: [NEG]
- `M111.png`
An enamel bathtub seen from above with the tap running clear and no steam anywhere in the room, the water shallow and still moving [STYLE] Avoid: [NEG]
- `M112.png`
A hand held under a running tap in an enamel sink, no face, the water breaking over the knuckles [STYLE] Avoid: [NEG]
- `M113.png`
A refrigerator of the period standing open in an unlit kitchen with its interior lamp dead and the shelves nearly bare, shot from the doorway so the open door dominates [STYLE] Avoid: [NEG]
- `M114.png`
A tin bath and a stack of folded towels set down on linoleum in a dim room, shot from a crouch, the bath dry [STYLE] Avoid: [NEG]
- `M115.png`
A wooden desk in a small office with one visitor's chair drawn up square to it, both of them empty, shot from the visitor's side of the room [STYLE] Avoid: [NEG]
- `M116.png`
A blotter, a telephone and a single closed folder on a desk with the chair behind it empty, shot from the doorway at standing height [STYLE] Avoid: [NEG]
- `M117.png`
Two chairs facing each other across a plain table in a small windowless room, nothing on the table, one overhead light and hard shadows under both chairs [STYLE] Avoid: [NEG]
- `M118.png`
A hand resting flat on a closed folder on a desk, the sleeve plain and nothing on the cuff, no face, the hand not moving [STYLE] Avoid: [NEG]
- `M119.png`
A wooden in-tray and out-tray on a counter with one folder caught mid-transit between them, held by a hand that is out of frame at the wrist [STYLE] Avoid: [NEG]
- `M120.png`
A wall clock in a plain municipal office with its face blank and only the hands on it, shot from below against a stained ceiling [STYLE] Avoid: [NEG]
- `M121.png`
A window with slatted blinds half drawn, hard slats of light lying across an empty desk and up the wall behind it, late afternoon [STYLE] Avoid: [NEG]
- `M122.png`
A punched card standing proud from a tray of identical cards, the perforations casting shadow into the card behind it, nothing printed on any of them [STYLE] Avoid: [NEG]
- `M123.png`
A tray of punched cards being lifted out of a cabinet, two hands only, the tray tipped just enough that the cards lean [STYLE] Avoid: [NEG]
- `M124.png`
A card reader of the early 1970s with its hopper full and the machine standing idle, shot close along the hopper so the card edges run away [STYLE] Avoid: [NEG]
- `M125.png`
A run of mainframe cabinets in a machine room with the floor tiles lifted and cabling beneath, nobody present, shot from the opened floor at knee height [STYLE] Avoid: [NEG]
- `M126.png`
A wide continuous form folded into a stack on a trolley, every printed line dissolved to grey, shot along the edge of the stack so the fanfold pleats read [STYLE] Avoid: [NEG]
- `M127.png`
An operator's console keyboard in a machine room with the chair empty and the panel lamps dark, shot from where the operator would sit [STYLE] Avoid: [NEG]
- `M128.png`
An empty stool at a keypunch machine that is still loaded with work, shot from the aisle so the stool sits between camera and machine [STYLE] Avoid: [NEG]
- `M129.png`
A telephone ringing unanswered on an empty desk in an office after hours, one lamp lit at the far end of the room, the handset seated and vibrating in its cradle [STYLE] Avoid: [NEG]
- `M130.png`
A lawyer's office window lit at night seen from the pavement below, every other window on the floor dark, shot steeply up through wires [STYLE] Avoid: [NEG]
- `M131.png`
A professional fee note lying face down on a desk beside an unopened bill, both blank, shot from above with a hand just leaving the frame [STYLE] Avoid: [NEG]
- `M132.png`
A bill and a small change purse laid side by side on a kitchen table, the purse open and nearly empty, no face, hard window light from the left [STYLE] Avoid: [NEG]
- `M133.png`
Notes and coins counted into one small pile on a formica table, the denominations not readable, two hands only, the counting stopped [STYLE] Avoid: [NEG]
- `M134.png`
A pay envelope lying flat and unopened on a counter, plain and unmarked, one corner overhanging the counter's edge [STYLE] Avoid: [NEG]
- `M135.png`
An empty chair drawn up to a counter window whose shutter is closed, shot from behind the chair so the closed shutter fills the far wall [STYLE] Avoid: [NEG]
- `M136.png`
A single sheet of plain paper falling through still air against a dark neutral ground, caught turning on its own edge halfway down [STYLE] Avoid: [NEG]
- `M137.png`
A plain door standing open with daylight beyond it and the room on this side of it empty, shot from the dark interior corner [STYLE] Avoid: [NEG]

### ACT_5（1,424語・52枚） — 止める権限は残る。反対意見（数字・電話・同じ事実の反転）。

- `M138.png`
A meter reader's canvas satchel hung over a fence post beside a house wall, no person anywhere, the satchel still swinging a little [STYLE] Avoid: [NEG]
- `M139.png`
A line of stepping stones along the side of a house leading toward the meter position, the grass worn to bare earth between them, shot low along the path [STYLE] Avoid: [NEG]
- `M140.png`
A gate in a chain-link fence standing open onto a side yard, shot from the pavement so the open gate frames the empty yard beyond [STYLE] Avoid: [NEG]
- `M141.png`
A hand about to lift the isolating cover on a meter board, a plain sleeve and no face, the fingers on the lip of the cover and not yet pulling [STYLE] Avoid: [NEG]
- `M142.png`
A printed notice pushed halfway under a front door from outside, seen from the hallway floor, the print dissolved to grey and the outdoor light coming in around it [STYLE] Avoid: [NEG]
- `M143.png`
A letter slot in a front door seen from inside with an envelope caught halfway through it, the flap resting on the envelope's edge [STYLE] Avoid: [NEG]
- `M144.png`
A pile of unopened plain envelopes on a hall table beside a set of keys, shot at table height so the pile's depth reads [STYLE] Avoid: [NEG]
- `M145.png`
A desk diary open at a blank spread under a lamp, no writing on either page, the gutter shadow running down the middle [STYLE] Avoid: [NEG]
- `M146.png`
The dial of a period telephone at extreme close range, the finger stops present and the ring around them entirely unmarked, one hard light raking the bakelite [STYLE] Avoid: [NEG]
- `M147.png`
A finger in the dial of a wall telephone caught mid-pull, no face, the ring behind it blank and the dial already blurred by the movement [STYLE] Avoid: [NEG]
- `M148.png`
The coiled cord of a wall telephone hanging in a long loop with the handset out of frame, shot against a pale kitchen wall so the loop reads as a line [STYLE] Avoid: [NEG]
- `M149.png`
A wall telephone with the handset back on its cradle and the kitchen behind it empty, shot from the same low angle as the hanging handset earlier [STYLE] Avoid: [NEG]
- `M150.png`
A bank of desks in a large room with a telephone handset on every one of them, no people, shot from the end of the room so the desks repeat to the far wall [STYLE] Avoid: [NEG]
- `M151.png`
Two rows of switchboard positions with their headsets hung up and every indicator dark, shot down the aisle between them [STYLE] Avoid: [NEG]
- `M152.png`
The jack field of a switchboard at close range with the cords dressed and idle, the plugs seated in their rest positions [STYLE] Avoid: [NEG]
- `M153.png`
A tally sheet clipped to a board on an office wall with its ruled grid entirely empty, the clip's shadow across the top row [STYLE] Avoid: [NEG]
- `M154.png`
A drawer of account cards under a hand with the cards fanned open, none of them marked, shot from directly above so the fan fills the frame [STYLE] Avoid: [NEG]
- `M155.png`
Two ledger cards laid apart on a desk so that they do not touch, both blank, shot square on with a hand's width of bare desk between them [STYLE] Avoid: [NEG]
- `M156.png`
The same two cards pushed together until their edges overlap, identical framing, one card riding on top of the other [STYLE] Avoid: [NEG]
- `M157.png`
A rubber band drawn tight around a thick bundle of identical printed slips on a counter, the band biting into the paper [STYLE] Avoid: [NEG]
- `M158.png`
A stack of complaint slips driven onto a desk spindle, every one of them blank, shot low so the spindle stands against a bright window [STYLE] Avoid: [NEG]
- `M159.png`
A wire basket heaped with folded slips beside an office window at dusk, the last daylight coming in flat across the top of the heap [STYLE] Avoid: [NEG]
- `M160.png`
A cash counter window with a small hatch at the bottom and the shutter drawn down over it, shot from the customer's side at eye height [STYLE] Avoid: [NEG]
- `M161.png`
A queue rope on chromed posts in an empty municipal hall, shot along the rope so it snakes away across the floor [STYLE] Avoid: [NEG]
- `M162.png`
A worn linoleum floor at eye level with the pattern rubbed through along one path across it, the path running from bottom of frame toward a counter out of focus [STYLE] Avoid: [NEG]
- `M163.png`
A woman's shoes and the hem of a plain coat at a counter, cropped at the knee and no face, one heel lifted as the weight shifts [STYLE] Avoid: [NEG]
- `M164.png`
A handbag set on a counter ledge with the clasp open and a folded slip lying on top of it, shot from the counter's own level [STYLE] Avoid: [NEG]
- `M165.png`
A payment book of stubs open on a counter with every line in it blank, a thumb holding the pages down at one corner [STYLE] Avoid: [NEG]
- `M166.png`
A hand pressing a bell push on a counter top, no face, the counter otherwise entirely clear, caught at the moment of contact [STYLE] Avoid: [NEG]
- `M167.png`
A closed door at the end of a municipal corridor with a light still on behind its frosted glass, shot from the far end of the corridor [STYLE] Avoid: [NEG]
- `M168.png`
A second identical door beside the first with nothing lit behind its glass, identical framing, the two doors indistinguishable but for the light [STYLE] Avoid: [NEG]
- `M169.png`
A plain office with a desk, two chairs and a filing cabinet seen from the doorway, nobody in it, the desk lamp left on [STYLE] Avoid: [NEG]
- `M170.png`
A door with a fresh empty plate frame newly screwed to it, the paint around the screw heads still bright and unweathered, close [STYLE] Avoid: [NEG]
- `M171.png`
A modest street of single-storey Memphis houses at dusk with porch lights on along the row and one house dark in the middle of the frame, shot from the centre of the road [STYLE] Avoid: [NEG]
- `M172.png`
The same street an hour later with the dark house still dark, identical framing, no figures anywhere in it [STYLE] Avoid: [NEG]
- `M173.png`
A bedroom window seen from the street at night with nothing lit behind it and the neighbouring window lit, shot from below the sill line [STYLE] Avoid: [NEG]
- `M174.png`
A living room from the doorway lit only by daylight through a gap in the drapes, the television dark and the room otherwise still [STYLE] Avoid: [NEG]
- `M175.png`
A hallway light fitting with the bulb gone out of it, shot from directly below against the ceiling so the empty socket is the whole subject [STYLE] Avoid: [NEG]
- `M176.png`
A hand on a light switch in a dark hallway with the switch already down, no face, the hand still resting on it [STYLE] Avoid: [NEG]
- `M177.png`
A sofa and a low table in a dim front room with a folded newspaper on the table, the print reduced to grey, shot from the far corner of the room [STYLE] Avoid: [NEG]
- `M178.png`
A kitchen table with two mugs standing untouched on it and both chairs pushed back, shot from above so the two empty places read [STYLE] Avoid: [NEG]
- `M179.png`
A hardback book closed on a desk beside a pair of spectacles with the covers plain, one lamp from the left [STYLE] Avoid: [NEG]
- `M180.png`
A tall stack of identical printed slips on a desk with the topmost one blank, shot from the desk's level so the stack towers [STYLE] Avoid: [NEG]
- `M181.png`
A single printed slip lifted from that stack between two fingers with the rest still square, caught at the instant it clears the pile [STYLE] Avoid: [NEG]
- `M182.png`
An office at night with one desk lamp still on and every other desk in shadow, shot from the dark end of the room [STYLE] Avoid: [NEG]
- `M183.png`
A window of a municipal office building lit from inside at night seen from the pavement, the blinds half drawn and nobody crossing behind them [STYLE] Avoid: [NEG]
- `M184.png`
A car of the period parked under a street light on a residential Memphis street at night, unbranded and nobody in it, shot from across the road [STYLE] Avoid: [NEG]
- `M185.png`
An empty counter hall at closing time with the chairs squared up and one light left on, shot from behind the counter for once [STYLE] Avoid: [NEG]
- `M186.png`
A headset lying across a switchboard shelf with its cord still plugged into the field, the position unoccupied, shot close along the shelf [STYLE] Avoid: [NEG]
- `M187.png`
A deferred payment agreement pad open on a counter with its ruled lines empty and a pen laid across it, shot from the customer's side [STYLE] Avoid: [NEG]
- `M188.png`
A paint tin and a brush set down on newspaper below a freshly painted office door, the door's plate frame still empty, shot from the corridor floor [STYLE] Avoid: [NEG]
- `M189.png`
A bedside table in a dark bedroom with a glass of water and a bottle of tablets on it, the labels dissolved to grey, the bed itself empty and made [STYLE] Avoid: [NEG]

### ENDING（224語・8枚） — 何が決まり、何が決まらなかったか。電話へのコールバック。

- `M190.png`
The two gas meters on the house wall again, framed exactly as the first image of the film, the dial faces blank, the light now late instead of early so the shadows fall the other way [STYLE] Avoid: [NEG]
- `M191.png`
Two windowed envelopes overlapping on a formica counter, framed exactly as earlier in the film, both unreadable, one now open [STYLE] Avoid: [NEG]
- `M192.png`
A printed slip and a plain envelope lying side by side on a kitchen table, both reduced to grey, shot from above in the last of the daylight [STYLE] Avoid: [NEG]
- `M193.png`
A hand setting a wall telephone handset back onto its cradle, no face, the kitchen dim behind it, caught a moment before the handset seats [STYLE] Avoid: [NEG]
- `M194.png`
A kitchen at first light with the telephone on the wall and nobody in the room, the whole frame cold and even and nothing moving in it [STYLE] Avoid: [NEG]
- `M195.png`
A modest Memphis street at dawn under a pale flat sky with every porch light out and no people, shot from the middle of the road [STYLE] Avoid: [NEG]
- `M196.png`
A concrete doorstep with one blade of grass grown through the joint, close and low, the first sun just reaching the edge of the step [STYLE] Avoid: [NEG]
- `M197.png`
The two electric meters on the wall photographed straight on in flat light, identical framing to the second image of the film, the discs now completely still [STYLE] Avoid: [NEG]

### PEOPLE（10枚） — 人物プレート。**全員実在しない一般人。顔は出さない。**

- `M198.png`
A woman in her forties in a plain 1970s coat standing at a municipal counter with her back to camera, face not visible, shot from behind and to one side so the shut counter fills the space in front of her [STYLE] Avoid: [NEG]
- `M199.png`
The hands of a woman in her forties holding two folded printed slips at a kitchen table, no face in frame, the printing dissolved to grey, both slips held at the same height [STYLE] Avoid: [NEG]
- `M200.png`
A man in his forties in plain workwear seen from behind at the side of a house, looking toward the meter position, face not visible, shot from the far end of the side path [STYLE] Avoid: [NEG]
- `M201.png`
A woman's silhouette against a drawn window blind from inside a dim room, the features not resolvable, the blind's light the only light in the frame [STYLE] Avoid: [NEG]
- `M202.png`
Two adults seated at a kitchen table seen from behind, shoulders and the backs of their heads only, one leaning back and one forward [STYLE] Avoid: [NEG]
- `M203.png`
A pair of working hands resting flat on a formica table top, no face and no jewellery, shot close from the table's own level [STYLE] Avoid: [NEG]
- `M204.png`
A woman standing at a wall telephone with her back to camera and the handset to her ear, face not visible, shot from the far side of a dim kitchen [STYLE] Avoid: [NEG]
- `M205.png`
A person in a plain jacket walking away along a residential pavement seen from far behind, the figure small and the street wide [STYLE] Avoid: [NEG]
- `M206.png`
An adult's hand and a child's hand held together at waist height, both cropped at the wrist and no faces, walking rather than posed [STYLE] Avoid: [NEG]
- `M207.png`
The back of a woman's head and shoulders in a hallway facing an open front door, face not visible, the daylight beyond her blowing out the doorway [STYLE] Avoid: [NEG]

### THUMB（3枚） — サムネ候補。**縦横比は16:9のまま。文字は焼き込まない。**

- `M208.png`
Two electric meters side by side on a painted house wall shot dead centre and close under hard directional light from the right, the dial faces blank, the upper third of the frame left clear for a headline [STYLE] Avoid: [NEG]
- `M209.png`
Two identical windowed envelopes overlapping at the centre of a dark formica surface under strong low side light, both of them unreadable, the upper third of the frame clear [STYLE] Avoid: [NEG]
- `M210.png`
A wall telephone handset hanging off its cradle on the cord in a dark kitchen, centred and lit from one side only so the cord reads as a single bright line, the upper third clear [STYLE] Avoid: [NEG]

---

## 5.5 ショート3本のプレートは、この210枚の**内数**です

`SHORTS_SLATE_EP62-65.v001.md` の `short265` / `short266` / `short267` が要求するモチーフを、上の
プロンプトに1つずつ突き合わせた表です。**ショート用の二度目の発注は出しません。**
各ショートの `R-A` 要件は「≥16 distinct plates」で、下の3表はそれぞれ **18 / 19 / 21枚**あります。

| `short265`「Two bills arrived. One was addressed to a person who did not exist.」 | 使うプレート |
|---|---|
| **frame 0** 壁に並んだ2つのメーター | `M001` |
| 回っている電気メーターの円盤 | `M002` |
| メーターのガラスに伸びる手 | `M019` |
| 平屋の正面／2つある玄関ドア | `M011` `M015` |
| 玄関マットの封筒／棚の封筒立て／並べて持たれた2通 | `M047` `M020` `M023` |
| 罫線まで一致する2通の請求書 | `M003` |
| ヒューズ盤 | `M033` |
| 真昼に照明の消えた廊下／電球のない照明 | `M004` `M175` |
| 壁掛け電話（受話器が垂れている／戻っている） | `M005` `M149` |
| スイッチを倒しても何も起きない | `M107` `M176` `M106` |
| 寄りのメーター（サムネ兼用・縦でも成立） | `M208` |
| **loop_join** `M106`（切られたまま暗い）→ 同じ位置に `M001` が浮かび上がる | `M106` → `M001` |

| `short266`「The notice said pay or we cut you off. That was all it said.」 | 使うプレート |
|---|---|
| **frame 0** 活字が灰色に溶けた最終通知 | `M048` |
| 三つ折りの請求書 | `M021` |
| 内側から見た郵便投入口 | `M143` |
| シャッターの下りた出納窓口／半分閉じた窓口 | `M160` `M038` |
| 2種類のちらし | `M050` `M051` |
| 時間外の廊下／一灯だけの事務室 | `M056` `M182` |
| 郵便棚 | `M042` |
| 閉じた窓口に向いた椅子／並んだ待合椅子 | `M135` `M039` |
| 誰も並んでいない誘導ロープ | `M161` |
| 無人の机で鳴る電話 | `M129` |
| 「どこで・何時に・誰の前で」＝面談机／文字盤の無い時計 | `M115` `M120` |
| 名札の入っていない枠／灯りのあるドア | `M054` `M167` |
| 夕暮れの通りで一軒だけ暗い | `M171` |
| **loop_join** `M171` の暗い窓が画面を埋め、そのまま `M048` の紙面になる | `M171` → `M048` |

| `short267`「Two thousand customers a month. The dissent said the system worked.」 | 使うプレート |
|---|---|
| **frame 0** 灯の消えた交換台 | `M060` |
| 受話器の並ぶ机の列（2枚） | `M061` `M150` |
| 交換台の列／ジャックフィールドの寄り | `M151` `M152` |
| 挿しっぱなしのヘッドセット（＝30〜40人がその場で3日延ばせた） | `M186` |
| カード索引の引き出し／手の下で開かれた台帳カード | `M043` `M154` |
| 罫線だけの集計表 | `M153` |
| 串刺しの苦情伝票 | `M158` |
| ダイヤルの寄り／回している指（＝通知に刷られていた番号） | `M146` `M147` |
| 検針鞄／無標記のバン | `M138` `M063` |
| 夜の通りで一軒だけ暗い（2枚） | `M171` `M172` |
| 椅子2脚の小部屋（＝面談） | `M117` |
| 真新しい空の名札枠／空白のプレート | `M170` `M076` |
| **止める権限は残る**（＝必須の落ち） | `M141` `M106` |
| **loop_join** `M172` の窓の並びが `M060` の消えた表示灯に解像する | `M172` → `M060` |

> **★縦位置の制約＝上の3表に出るプレートはすべて 9:16 センターセーフ指定です。**
> ショートは 1080×1920。**主題を画面中央に置き、左右を切っても意味が壊れないこと。**
> フック1コマ目の `M001` `M048` `M060` は特に厳格で、プロンプト本文に
> `fills the frame` / `at the centre of a kitchen table` / `filling the frame` を明記してあります。
> 生成後の目視では、**16:9のコンタクトシートと9:16に切ったサムネイルを並べて**確認してください。
> 端に寄った構図（例：`M163` の膝から下、`M121` のブラインドの光、`M139` の低い小径）は
> ショートに使わず、長尺のみに使います。
>
> **`short267` の落ちは削れません。** `THEY CAN STILL CUT IT` のテロップに当てる絵（`M141` `M106`）は
> 必ず生成すること。この話で最も起きやすい誤読は「聴取が入った＝止まらなくなった」で、
> スレートはそれを禁じています。

---

## 6. 生成後にやること（発注者側）

1. **全210枚をラベル付きコンタクトシートで目視**する。プロンプトIDで選ばない
   （short60は3枚がプロンプト一覧どおりに選んで別の絵だった）。
2. `episodes/PD-2026-064-memphis/episode_spec.v001.json` の `mandatory_stills` に
   **M001〜M210 を全部書く**。空のままだと `check_spec_satisfied.py` の唯一の保護が無効になります
   （EP54は、棚に無いから作らせた14枚が完成品から消えて誰も気づきませんでした）。
3. 1枚 = 1モーションクリップとして `remotion/public/memphis/motion/` に書き出す
   （i2v または深度パララックス。**ズーム/パンだけは不可**）。
4. `python scripts/check_episode_inputs.py --slug memphis` で
   **accepted(24) + motion ≥ 234** をレンダー前に確認する。
5. 実写24本のうち**ろうそく5本・マッチ3本**は `footage_diversity` の再利用上限に直撃します。
   カットリストを組むときは、この210枚を主、実写を従として配分してください。
6. **HOOK の5枚（`M001`–`M005`）は本編カットにも必ず入れる。**8秒フックは
   promise-payoff が要件で、フックで見せた絵が本編に出てこないと約束が果たされません（§4）。

### 生成後のチェック（1枚ずつ目視）

| # | 不合格条件 |
|---|---|
| Q1 | 長辺が3840px未満 |
| Q2 | 読める文字・数字・署名がある（**請求書・最終通知・メーターの目盛り・台帳カードの上も含む**） |
| Q3 | 印章・紋章・ロゴらしきものがある |
| Q4 | 炎・燃えている家・家から立ちのぼる煙が写っている |
| Q5 | 震える人・毛布にくるまった人・倒れた人・泣いている子ども（＝**因果の絵**）が写っている |
| Q6 | 制服・制帽・バッジ・ドアの前に立ちはだかる人影（＝検針員を悪役にした絵）が写っている |
| Q7 | 法廷内観・木槌・判事席・鉄格子・独房が写っている |
| Q8 | 1970年代でない物（デジタル表示・現代の家電・現代のメーター・80年代以降の車）が写っている |
| Q9 | カタログ調である（光に方向がない／時間が止まっていない／構図に視点がない）、画面全体が暗すぎる、または既存の他話・本バッチ内の別プレートと実質同じ構図である |
