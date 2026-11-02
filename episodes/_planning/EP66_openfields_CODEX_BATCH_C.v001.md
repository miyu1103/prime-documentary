# EP66 openfields — Codex 画像生成 **バッチC 再発注** v001（**21枚**・1プロンプト1枚）

> ## ★★★ この21枚は、**同じ ID の既存ファイルを上書きします。** ★★★
> 保存先も名前もバッチBと同一（`H:\pd-media\assets\ai\openfields\L###.png`）。
> **新しい ID を作らないでください。** `_v2` も `_02` も作らないでください。
> 上書きされた時点で、`mandatory_stills` / `people_plates` の宣言はそのまま有効です。
>
> ## ★★★ バッチA（`L001`–`L069`）は引き続き**廃棄**です。 ★★★
> 棚には残っていますが、`mandatory_stills` に入れず、生成もせず、ID も再利用しません。
> このバッチCが触るのは `L070`–`L260` の中の 21 枚だけです。

**由来:** `runs/qc/openfields_plate_verdicts.v001.md` の目視QC。191枚のうち **REJECT 11・FLAG 10** が出ました。この発注書はその21枚**だけ**を作り直します。
**残り170枚は合格。触りません。**

> ### ★L092 は発注しません（QCの結論は ACCEPT）★
> 遠景の二人組が近接プロフィールに見えたため一度は疑われましたが、発注文そのものが「近景の一人の風化した顔がはっきり見え、二人目は遠くに小さく」と書いており、**二人目は右の地平に写っています**。verdicts §2 が明示的に **ACCEPT** としています。§7 の作り直しリストにも入っていません。**したがって対象外です。**

---

## 0. ★★★ 最重要：1プロンプト = 1枚 ★★★

1. **各プロンプトから画像を1枚だけ作る。** 同じプロンプトで2枚目を作らない。
2. **`_02` / `_03` を作らない。**「良いのが出るまで回す」を禁止する。
3. 作り直してよいのは §1 の禁止に触れたときだけ。そのときも**文言を直してから1枚**。
4. **既存の同名ファイルを上書きする。**別名で出すと、どちらが正典か分からなくなります。

## 1. ★絶対条件（バッチB §1 と同一。緩和はありません）

正典は `episodes/PD-2026-066-openfields/episode_spec.v001.json` の `forbidden_subjects` です。
**契約は本日更新され、`face` / `portrait` / `headshot` は禁止語ではなくなりました**（`people_plates` は `L235`–`L254`）。以下は再掲です。

- **人物は入れる。顔も描く。禁じられているのは「実在する特定の人物に似ていること」だけ。**
  完全に架空の一般人であること。有名人・公人・実在の誰かに似せない。
  カメラ目線の作り笑い・広告のモデル顔にしない。**働いている人の、作っていない顔。**
- **読める文字・数字・手書き・印章・ロゴを描かない。** 掲示の面は**(a) 退色して完全に読めない無地の板 / (b) 紫の塗りの帯 / (c) 釘穴と色の抜けた樹皮の矩形**の3通りだけ。
  **車体のバッジ・文字マーク・ネームプレート・グリルの楕円もここに含まれます**（`L146` と `L173` はこれで落ちました）。
- **制服・記章・パトカー・手錠・銃・仕留められた動物・血を描かない。** 職員は一人も登場しません。
- **監視スリラーの意匠を作らない。** トレイルカメラは**幹にベルトで留めた小さくて安っぽい艶消しオリーブの樹脂の箱**です。それが全部です。
  **銀色の金属缶でも、レンズ鏡胴のあるコンパクトカメラでもありません**（`L208` と `L209` はこれで落ちました）。
- **実在と特定できる土地・建物を描かない。法廷を描かない。広告調にしない。黒つぶれさせない。**
- **航空カットは `L138` の1枚だけ。** 本文の `with the horizon kept high in the frame` を削らない。プロンプトにも成果物名にも `drone` と書かない（契約が `drone` を落とします）。

## 2. スタイル（★必ず展開してから生成）

**`[STYLE]` も `[NEG]` もバッチBと1語も違いません。**`scripts/check_image_order_neg.py` を通過済み（§6）。**この2ブロックを1語も変えずに展開してください。**

**`[STYLE]`** ＝ 末尾にそのまま連結:

> , cinematic still, muted natural colour, flat overcast daylight of a late Appalachian autumn, low contrast but never crushed: shadows keep their detail and the frame reads clearly on a phone screen, soft falloff toward the edges, shallow depth of field, restrained documentary framing, rural Pennsylvania and Middle Tennessee between 2019 and 2026, ordinary working farmland and unmanaged second-growth woodland, worn unglamorous surfaces, nothing staged for advertising, ultra-detailed, photoreal, 4K, 16:9, fine film grain, no text, no lettering, no numerals, no watermark, no logo, no signage

**`[NEG]`** ＝ `Avoid:` の後にそのまま連結:

> text, lettering, numerals, digits, house numbers, handwriting, cursive writing, legible signature, seals, emblems, logos, insignia, badge, name plates, readable words on a sign, recognisable person, identifiable person, likeness of a real individual, portrait of a named person, celebrity, public figure, deepfake, police officer, sheriff, trooper, uniform, patrol car, flashing lights, handcuffs, rifle, shotgun, firearm, holster, dead animal, carcass, blood, taxidermy, mounted antlers, courtroom interior, gavel, judge's bench, prison bars, razor wire, scales of justice, hourglass, a handshake, night vision green, thermal false colour, crosshairs, CCTV monitor grid, drone shot, aerial view from above the treetops, golden hour, sunset glow, postcard scenery, autumn colour explosion, Christmas, tropical, modern smartphones, laptops, glossy advertising lighting, flat CGI, cartoon, illustration, oversaturated, HDR halo

> ### ★プレートごとの `[NEG]` 追記について★
> 何枚かは `Avoid: [NEG], …` と、`[NEG]` の後ろに読点で語が続いています。
> **これは上の正典 `[NEG]` を展開したうえで、その末尾にさらに続ける、という意味です。**
> **正典 `[NEG]` の語を1語も削らないでください。**追記だけが増えます。
>
> ### ★`[NEG]` は「人」を禁じていません★
> 禁じているのは **`recognisable person, identifiable person, likeness of a real individual,`**
> **`portrait of a named person, celebrity, public figure, deepfake`** ——**実在の誰かに似ること**だけです。
> バッチAの `[NEG]` は `human face, facial features, eyes …` と書いて**人が写ること自体**を止めており、
> **191枚を作り直す羽目になった原因がそれです。元に戻さないでください。**

## 3. 命名と保存先

- ファイル名は**元と同じ**（`L170.png` など）。**連番を新規に振らない。**
- 保存先 `H:\pd-media\assets\ai\openfields\`（バッチB・バッチAと同じ棚）。**同名で上書き。**
- 長辺 3840px 以上・16:9・PNG。

## 4. 対象一覧（21枚）

| # | ID | 区分 | QC判定 | 作り直す理由（1行） |
|---:|---|---|---|---|
| 1 | `L170` | ACT_5 / 回収対A | REJECT | PAIR A BROKEN: L075 は角材の門柱・平らな低い樹列・冷たい灰色。L170 は丸柱が内側に寄り、背景を裸の斜面が埋め、暖色に転んでいた。26分の回収が読めない。 |
| 2 | `L175` | ENDING / 回収対B | REJECT | PAIR B BROKEN: L082 は左右の枠に切られた角材柱・両側から迫る裸木で道が閉じる。L175 は銀化した柱が枠内に収まり、道の奥が明るく抜けていた。 |
| 3 | `L172` | ACT_5 / 回収対C | REJECT | PAIR C BROKEN ＋ 被写体違い: L074 は艶消しオリーブの角い樹脂箱。L172 は銀色の丸い金属缶で、画角も寄りすぎていた。 |
| 4 | `L146` | ACT_4 | REJECT | BADGE: 「無標のピックアップ」と発注したのに、テールゲートに工場の文字マークとクロームのネームプレートが出た。`[NEG]` の `name plates` だけでは止まらなかったので本文に書く。 |
| 5 | `L173` | ACT_5 | REJECT | EMBLEM ＋ 車が別物: グリル中央にメーカーの楕円が出た上、L096 の暗色クルーキャブではなく緑色の90年代小型車になっていて回収が成立しない。 |
| 6 | `L209` | CAMERA | REJECT | 被写体違い: 「小さな樹脂の箱」と発注したのに、レンズ鏡胴とファインダーと操作パネルの付いた白いコンパクトカメラが出た。CAMERA register は幹に留めた安物の箱だけである。 |
| 7 | `L208` | CAMERA | FLAG | 発注違い: 「二本の幹」と書いたのに柱に付き、かつ物がオリーブの樹脂箱でなく銀の金属缶で、L074/L148/L149/L203 との器具の連続性が切れた。 |
| 8 | `L189` | BOUNDARY | FLAG | GHOST PRINT: 中央の板の面に、横二〜三列に並ぶ薄い灰色の塊が残っていて「行」に見える。読めはしないが、発注は「行にも語にも見えないところまで潰す」ことを要求している。 |
| 9 | `L247` | PEOPLE | REJECT | 手の破綻: 手そのものが被写体なのに、native で数えると近い手に融合した余分な指があり、遠い手の指が手首に溶けている。組んだ手をほどいて別々に置く。 |
| 10 | `L252` | PEOPLE | FLAG | 二点: 右の地平に `[NEG]` が禁じた夕陽の暖色が乗った。加えて組んだ指が数えられない。 |
| 11 | `L236` | PEOPLE | FLAG | 発注違い ＋ 手の破綻: 「片手を上の針金に沿わせて歩く」と書いたのに両手を下ろしており、その右手の指が塊に融合している。 |
| 12 | `L235` | PEOPLE | FLAG（§7 では owner call） | 境界事例: 姿勢は正しいが、カメラ目線で微笑が出ている。発注は「カメラのために作った表情はしない」。 |
| 13 | `L102` | ACT_2 カード背景 | FLAG | Q11: 文字を置く帯に丘の稜線と梢が入る（帯の 2.13% がエッジ・5.51% が非空）。カード背景7枚で最悪。 |
| 14 | `L099` | ACT_2 カード背景 | FLAG（§7 では optional） | Q11 軽微: 帯は明るい（平均219.2）が泥のテクスチャが乗っており（エッジ 0.90%）、タイポグラフィが平らな面でなく模様の上に載る。 |
| 15 | `L138` | ACT_4 | FLAG | `[NEG]` の `autumn colour explosion` / `postcard scenery`: 地平線は残っているが、樹冠が飽和したオレンジの塊になり絵葉書の空撮に見える。 |
| 16 | `L229` | DUSK | FLAG | `[NEG]` の `golden hour, sunset glow`: 地平に暖かいオレンジの帯が出た。DUSK 区分の見出しは夕陽の色を明示的に禁じている。 |
| 17 | `L255` | THUMB | REJECT | 上部が空いていない: 1280x720 換算で帯の 169 行目から樹列と門の上端が入り（帯の 15.86% が非空）、見出しが置けない。構図も左右が反転していた（発注は「やや右」）。 |
| 18 | `L256` | THUMB | REJECT | 上部が塞がっている: 幹が全高を貫き、帯の各行の 41-49% を占める（非空 43.87%・エッジ 17.82%）。見出しはどこにも置けない。 |
| 19 | `L257` | THUMB | REJECT | 上部が塞がっている: 幹が全高を貫く（帯の非空 29.75%・エッジ 21.53%）。発注は「上1/3は枝も葉も無い明るい空」だった。 |
| 20 | `L259` | THUMB | REJECT | 上部が空いていない: 163 行目から門柱と頭頂が帯に入る（非空 4.33%）。手と顔そのものは native で確認済みで良好（指の数が正しく、視線はカメラを外している）。 |
| 21 | `L260` | THUMB | FLAG（§7 では optional） | 境界事例: 板の上の切株のこぶが 190 行目で帯の下端を削る（非空 2.34%）。150px の見出しと 12px の縁取りは今でも収まるが、「何も横切らない」という指定は満たしていない。 |

> ### ★§0.6 の三対は「似た絵」ではなく「同じ絵」を要求します★
> `L170` / `L175` / `L172` の本文は、**一枚目の実画像を開いて、そこに写っているものから書き起こしました**（`L075` / `L082` / `L074`。棚の実ファイルを 4K のまま拡大して読んでいます）。
> **生成前に一枚目を横に置いてください。**カメラ高・画角・被写体の位置が違えば回収が成立しません。

> ### ★QCの §7 から意図的に外した2点（画像が §7 と食い違ったため）★
> 1. **`L170` の `[NEG]` に `hill, ridge, rising ground behind the field` を入れませんでした。**
>    §7 はそう書いていますが、**一枚目の `L075` 自身が、平らな樹列の右奥に霞んだ低い尾根を持っています。**
>    尾根を一律に禁じると `L170` は `L075` と一致しなくなります。実際の失敗は「裸の斜面が背景を埋めたこと」なので、そちらだけを禁じました。
> 2. **`L175` の `[NEG]` に `evergreen conifers` を足しました。**§7 にはありませんが、`L082` の背景は全部落葉樹で、現行 `L175` は道の奥に針葉樹を置いています。

## 5. プロンプト（各1枚）

### `L170.png` — ACT_5 / 回収対A・REJECT

**作り直す理由:** PAIR A BROKEN: L075 は角材の門柱・平らな低い樹列・冷たい灰色。L170 は丸柱が内側に寄り、背景を裸の斜面が埋め、暖色に転んでいた。26分の回収が読めない。**本文は L075 の実画像から書き起こした。**

- `L170.png`
The identical framing as the empty field at the head of the film: a SQUARED timber gate post, its faces dark and green with moss and lichen, standing upright about a tenth of the frame width in from the LEFT EDGE with a narrow strip of field visible to the left of it, its flat sawn top just below the top edge of the frame and its foot running out of the bottom edge, and on the post now nothing but a loop of loose rusted wire hanging down its left face where a chain used to hang, the same flat low line of bare winter trees running level across the middle of the frame with one faint hazy low wooded ridge far behind them on the right almost lost in the haze, the same brown winter field of tufted dead grass running from the foot of the post to that tree line, the same even pale cool grey overcast sky filling the upper third, camera at the height a small box strapped to a trunk would sit [STYLE] Avoid: [NEG], bare hillside filling the background, wooded slope rising close behind the field, round pole post, post set in toward the middle of the frame, warm colour grade, mown pasture

**保存先:** `H:\pd-media\assets\ai\openfields\L170.png`（**既存を上書き**）

**`[NEG]` 追記:** 正典 `[NEG]` の末尾に `, bare hillside filling the background, wooded slope rising close behind the field, round pole post, post set in toward the middle of the frame, warm colour grade, mown pasture` を足す。**正典側は1語も削らない。**

### `L175.png` — ENDING / 回収対B・REJECT

**作り直す理由:** PAIR B BROKEN: L082 は左右の枠に切られた角材柱・両側から迫る裸木で道が閉じる。L175 は銀化した柱が枠内に収まり、道の奥が明るく抜けていた。**本文は L082 の実画像から書き起こした。**

- `L175.png`
The identical framing as the head of the film: a heavy rusted chain drawn straight across the mouth of a gravel farm track between two SQUARED WEATHERED TIMBER POSTS, the left post darker and slightly the narrower of the two and cut off by the very left edge of the frame with its flat sawn top about a seventh of the way down, the right post paler grey-brown and broader and cut off by the right edge with its top about a fifth of the way down, both posts green with moss at the foot, one plain rectangular steel padlock hanging at the centre of the chain's gentle sag at about the middle of the frame, wet grey gravel with standing puddles running away from the camera and bending slightly left until dense bare trees and dead brush crowding in from both sides close it off, a wooded slope behind the trees on the right and only a small patch of pale sky showing between the branches above, photographed head-on at chest height in low flat morning light [STYLE] Avoid: [NEG], bright gap in the distance, open sky down the track, silvered posts, evergreen conifers

**保存先:** `H:\pd-media\assets\ai\openfields\L175.png`（**既存を上書き**）

**`[NEG]` 追記:** 正典 `[NEG]` の末尾に `, bright gap in the distance, open sky down the track, silvered posts, evergreen conifers` を足す。**正典側は1語も削らない。**

### `L172.png` — ACT_5 / 回収対C・REJECT

**作り直す理由:** PAIR C BROKEN ＋ 被写体違い: L074 は艶消しオリーブの角い樹脂箱。L172 は銀色の丸い金属缶で、画角も寄りすぎていた。**本文は L074 の実画像から書き起こした。**

- `L172.png`
The same dull OLIVE-GREEN RECTANGULAR plastic box as before, matt and unbranded, strapped to the same dark rough-barked hardwood trunk which stands just right of centre and runs the full height of the frame, the box on the LEFT side of the trunk at about mid height with its lens face turned off to the left of the frame and one single black webbing strap crossing the bark horizontally beneath it, the pale cut branch stub on the trunk just above and to the right of the box with its cut face now weathered grey instead of raw cream, the webbing strap gone slack around the bark, an open brown field and thin saplings visible past the trunk on the left and closer woodland on the right, pale white sky between the bare branches, seen from the same few feet away and at the same slightly low angle as before [STYLE] Avoid: [NEG], metal canister, silver, aluminium, cylindrical, rounded box

**保存先:** `H:\pd-media\assets\ai\openfields\L172.png`（**既存を上書き**）

**`[NEG]` 追記:** 正典 `[NEG]` の末尾に `, metal canister, silver, aluminium, cylindrical, rounded box` を足す。**正典側は1語も削らない。**

### `L146.png` — ACT_4・REJECT

**作り直す理由:** BADGE: 「無標のピックアップ」と発注したのに、テールゲートに工場の文字マークとクロームのネームプレートが出た。`[NEG]` の `name plates` だけでは止まらなかったので本文に書く。

- `L146.png`
A plain unmarked pickup truck parked on the gravel shoulder of a public road at the edge of hardwood timber, empty and shut, seen from a hundred yards away at eye height with nobody near it, the tailgate and tailgate panel completely bare with no badge, no wordmark, no nameplate and no lettering of any kind on any part of the vehicle [STYLE] Avoid: [NEG]

**保存先:** `H:\pd-media\assets\ai\openfields\L146.png`（**既存を上書き**）

### `L173.png` — ACT_5・REJECT

**作り直す理由:** EMBLEM ＋ 車が別物: グリル中央にメーカーの楕円が出た上、L096 の暗色クルーキャブではなく緑色の90年代小型車になっていて回収が成立しない。**本文は L096 の実画像から書き起こした。**

- `L173.png`
The same dark modern crew-cab pickup as before, standing in the same mown green grass field lane with both cab doors open, seen from the same camera position at the same eye height from the near end of the lane so the truck sits small near the centre of the frame, a brown worked field on the left of the lane and a line of bare trees on the right, low wooded hills faint in the far distance under a pale grey sky, later in the day and in flatter light, nobody in it and nobody near it, the grille and the tailgate completely bare with no badge, emblem, oval, wordmark or nameplate anywhere on the vehicle [STYLE] Avoid: [NEG]

**保存先:** `H:\pd-media\assets\ai\openfields\L173.png`（**既存を上書き**）

### `L209.png` — CAMERA・REJECT

**作り直す理由:** 被写体違い: 「小さな樹脂の箱」と発注したのに、レンズ鏡胴とファインダーと操作パネルの付いた白いコンパクトカメラが出た。CAMERA register は幹に留めた安物の箱だけである。

- `L209.png`
A small dull olive rectangular plastic box of the same kind strapped to the trunks elsewhere in this set, lying face up on the open tailgate of a pickup truck among wet leaves and a loose coil of black webbing strap, seen from above at waist height, the box plain and unmarked with no lens ring, no buttons, no display panel and no lettering [STYLE] Avoid: [NEG], compact camera, consumer camera, lens barrel, viewfinder, control buttons, display screen

**保存先:** `H:\pd-media\assets\ai\openfields\L209.png`（**既存を上書き**）

**`[NEG]` 追記:** 正典 `[NEG]` の末尾に `, compact camera, consumer camera, lens barrel, viewfinder, control buttons, display screen` を足す。**正典側は1語も削らない。**

### `L208.png` — CAMERA・FLAG

**作り直す理由:** 発注違い: 「二本の幹」と書いたのに柱に付き、かつ物がオリーブの樹脂箱でなく銀の金属缶で、L074/L148/L149/L203 との器具の連続性が切れた。

- `L208.png`
Two small dull OLIVE-GREEN RECTANGULAR plastic boxes of the same kind, matt and unbranded, one strapped to a TREE TRUNK on each side of a junction of two woodland tracks, both turned to face down the same lane, seen from the lane at eye height [STYLE] Avoid: [NEG], metal canister, silver, cylindrical, mounted on a post

**保存先:** `H:\pd-media\assets\ai\openfields\L208.png`（**既存を上書き**）

**`[NEG]` 追記:** 正典 `[NEG]` の末尾に `, metal canister, silver, cylindrical, mounted on a post` を足す。**正典側は1語も削らない。**

### `L189.png` — BOUNDARY・FLAG

**作り直す理由:** GHOST PRINT: 中央の板の面に、横二〜三列に並ぶ薄い灰色の塊が残っていて「行」に見える。読めはしないが、発注は「行にも語にも見えないところまで潰す」ことを要求している。

- `L189.png`
Three identical blank weathered placards on three successive trunks along a boundary, receding away from the camera into the wood, each one turned squarely to face the camera, each face a single UNIFORM FLAT PALE SURFACE with no darker areas, no smudges, no rows of marks and no shapes of any kind on it, as though it had been repainted plain [STYLE] Avoid: [NEG], faded print, ghost lettering, rows of marks, printed rows

**保存先:** `H:\pd-media\assets\ai\openfields\L189.png`（**既存を上書き**）

**`[NEG]` 追記:** 正典 `[NEG]` の末尾に `, faded print, ghost lettering, rows of marks, printed rows` を足す。**正典側は1語も削らない。**

### `L247.png` — PEOPLE・REJECT

**作り直す理由:** 手の破綻: 手そのものが被写体なのに、native で数えると近い手に融合した余分な指があり、遠い手の指が手首に溶けている。組んだ手をほどいて別々に置く。

- `L247.png`
An invented older man's hands and forearms resting on the top rail of a wooden fence with his face visible above them looking out across the field, his two hands resting SEPARATELY and flat on the top rail a hand's width apart, palms down, fingers relaxed and clearly separated, not crossed and not clasped, deep lines and grey stubble, flat daylight and no jewellery [STYLE] Avoid: [NEG], interlocked fingers, clasped hands, crossed hands, fused fingers, extra fingers, malformed hand

**保存先:** `H:\pd-media\assets\ai\openfields\L247.png`（**既存を上書き**）

**`[NEG]` 追記:** 正典 `[NEG]` の末尾に `, interlocked fingers, clasped hands, crossed hands, fused fingers, extra fingers, malformed hand` を足す。**正典側は1語も削らない。**

### `L252.png` — PEOPLE・FLAG

**作り直す理由:** 二点: 右の地平に `[NEG]` が禁じた夕陽の暖色が乗った。加えて組んだ指が数えられない。

- `L252.png`
An invented man sitting on an upturned bucket beside a cold fire ring at the edge of a field in the last flat grey daylight before dusk, no warm colour anywhere in the sky, his forearms resting on his knees with his hands hanging loose and open, fingers apart, not clasped, his face lit evenly by that flat daylight and no fire burning [STYLE] Avoid: [NEG]

**保存先:** `H:\pd-media\assets\ai\openfields\L252.png`（**既存を上書き**）

### `L236.png` — PEOPLE・FLAG

**作り直す理由:** 発注違い ＋ 手の破綻: 「片手を上の針金に沿わせて歩く」と書いたのに両手を下ろしており、その右手の指が塊に融合している。

- `L236.png`
An invented woman in her fifties in a quilted work jacket walking a fence line with her RIGHT HAND RAISED and clearly trailing along the top wire, the hand open with fingers separated and visible against the field, her other hand at her side, seen from the front at about twenty feet at eye height, her face lit evenly by flat cloud, a stubble field running away behind her [STYLE] Avoid: [NEG]

**保存先:** `H:\pd-media\assets\ai\openfields\L236.png`（**既存を上書き**）

### `L235.png` — PEOPLE・FLAG（§7 では owner call）

**作り直す理由:** 境界事例: 姿勢は正しいが、カメラ目線で微笑が出ている。発注は「カメラのために作った表情はしない」。

- `L235.png`
An entirely invented ordinary man in his sixties in a heavy canvas work coat closing a steel tube farm gate across a track, both hands on the top rail, turned three-quarters toward the camera so his weathered face is clearly visible in flat overcast light, HIS EYES DIRECTED PAST THE CAMERA AT THE GATE LATCH, mouth closed, no smile, no expression put on for the camera [STYLE] Avoid: [NEG]

**保存先:** `H:\pd-media\assets\ai\openfields\L235.png`（**既存を上書き**）

### `L102.png` — ACT_2 カード背景・FLAG

**作り直す理由:** Q11: 文字を置く帯に丘の稜線と梢が入る（帯の 2.13% がエッジ・5.51% が非空）。カード背景7枚で最悪。

- `L102.png`
The closed gate, the fence line and the blank weathered placard all held small together in the LOWER THIRD of a wide frame with the working field behind them, and the whole UPPER HALF of the frame an even pale sky with NO hill, NO ridge, NO treetop and NO branch entering it [STYLE] Avoid: [NEG]

**保存先:** `H:\pd-media\assets\ai\openfields\L102.png`（**既存を上書き**）

### `L099.png` — ACT_2 カード背景・FLAG（§7 では optional）

**作り直す理由:** Q11 軽微: 帯は明るい（平均219.2）が泥のテクスチャが乗っており（エッジ 0.90%）、タイポグラフィが平らな面でなく模様の上に載る。

- `L099.png`
A single line of boot prints crossing wet bare ground from the lower left of the frame away into the distance, the upper third of the frame a smooth unbroken area of wet bare ground with no prints, no stones and no straw in it and no horizon line, branch or wire crossing it [STYLE] Avoid: [NEG]

**保存先:** `H:\pd-media\assets\ai\openfields\L099.png`（**既存を上書き**）

### `L138.png` — ACT_4・FLAG

**作り直す理由:** `[NEG]` の `autumn colour explosion` / `postcard scenery`: 地平線は残っているが、樹冠が飽和したオレンジの塊になり絵葉書の空撮に見える。

- `L138.png`
A low oblique aerial over unbroken Appalachian hardwood forest AFTER LEAF FALL, the canopy bare grey-brown with no colour in it, under flat overcast light, with the horizon kept high in the frame, one narrow forest road threading through the timber and no other break in the canopy [STYLE] Avoid: [NEG]

**保存先:** `H:\pd-media\assets\ai\openfields\L138.png`（**既存を上書き**）

### `L229.png` — DUSK・FLAG

**作り直す理由:** `[NEG]` の `golden hour, sunset glow`: 地平に暖かいオレンジの帯が出た。DUSK 区分の見出しは夕陽の色を明示的に禁じている。

- `L229.png`
A field at dusk seen through a wire fence from outside it, the strands of wire crossing the sky in the upper part of the frame, everything beyond the wire in silhouette, and the sky above the wire a FLAT COLD PALE GREY with no warm colour, no orange, no yellow and no glow anywhere in it [STYLE] Avoid: [NEG]

**保存先:** `H:\pd-media\assets\ai\openfields\L229.png`（**既存を上書き**）

### `L255.png` — THUMB・REJECT

**作り直す理由:** 上部が空いていない: 1280x720 換算で帯の 169 行目から樹列と門の上端が入り（帯の 15.86% が非空）、見出しが置けない。構図も左右が反転していた（発注は「やや右」）。

- `L255.png`
A closed steel tube farm gate with a chain and a plain padlock at its latch post, shot dead centre and close from directly in front at chest height, one hard directional key light raking from the left so the wet metal stands out bright against the darker ground, the horizon line held BELOW the midpoint of the frame and the gate, its chain and its padlock sitting wholly in the lower half of the frame and set slightly RIGHT of centre, and the ENTIRE UPPER 40% OF THE FRAME an unbroken field of pale bright overcast sky with nothing whatever entering it: no branch, no twig, no trunk, no post, no wire, no chain, no tree line, no distant hill and no horizon line anywhere within that upper 40% [STYLE] Avoid: [NEG]

**保存先:** `H:\pd-media\assets\ai\openfields\L255.png`（**既存を上書き**）

### `L256.png` — THUMB・REJECT

**作り直す理由:** 上部が塞がっている: 幹が全高を貫き、帯の各行の 41-49% を占める（非空 43.87%・エッジ 17.82%）。見出しはどこにも置けない。

- `L256.png`
A small dull olive plastic box strapped to a tree trunk with a black webbing strap, seen at very close range from slightly below, the TRUNK CUT OFF BY THE FRAME so that its top edge is no higher than 40% down from the top of the frame and it occupies only the lower two thirds, the box strapped low on it and left of centre, one hard directional key light from the right throwing a crisp shadow of the box across the bark, and the ENTIRE UPPER 40% OF THE FRAME an unbroken field of pale bright overcast sky with nothing whatever entering it: no branch, no twig, no trunk, no post, no wire, no chain, no tree line, no distant hill and no horizon line anywhere within that upper 40% [STYLE] Avoid: [NEG]

**保存先:** `H:\pd-media\assets\ai\openfields\L256.png`（**既存を上書き**）

### `L257.png` — THUMB・REJECT

**作り直す理由:** 上部が塞がっている: 幹が全高を貫く（帯の非空 29.75%・エッジ 21.53%）。発注は「上1/3は枝も葉も無い明るい空」だった。

- `L257.png`
A thick vertical stripe of purple paint on the trunk of a tree, seen close and straight on, the TRUNK ENDING BELOW the upper 40% of the frame and filling only the lower two thirds, the purple stripe low in the frame and right of centre, hard light raking across the bark from the left so the paint reads bright and saturated against the grey wood, and the ENTIRE UPPER 40% OF THE FRAME an unbroken field of pale bright overcast sky with nothing whatever entering it: no branch, no twig, no trunk, no post, no wire, no chain, no tree line, no distant hill and no horizon line anywhere within that upper 40% [STYLE] Avoid: [NEG]

**保存先:** `H:\pd-media\assets\ai\openfields\L257.png`（**既存を上書き**）

### `L259.png` — THUMB・REJECT

**作り直す理由:** 上部が空いていない: 163 行目から門柱と頭頂が帯に入る（非空 4.33%）。手と顔そのものは native で確認済みで良好（指の数が正しく、視線はカメラを外している）。

- `L259.png`
An invented ordinary person's hands closing a padlock through a chain on a gate post with their face visible above the hands looking down at them, one hard key light from the right so both the hands and the face stand out bright against the darker gate, the GATE POST CUT OFF at 45% down from the top of the frame, the head and both hands held wholly in the lower half of the frame and set slightly RIGHT of centre, five clearly separated fingers on each hand and the eyes directed down at the padlock and not at the camera, and the ENTIRE UPPER 40% OF THE FRAME an unbroken field of pale bright overcast sky with nothing whatever entering it: no branch, no twig, no trunk, no post, no wire, no chain, no tree line, no distant hill and no horizon line anywhere within that upper 40%, and no hair entering that band either [STYLE] Avoid: [NEG]

**保存先:** `H:\pd-media\assets\ai\openfields\L259.png`（**既存を上書き**）

### `L260.png` — THUMB・FLAG（§7 では optional）

**作り直す理由:** 境界事例: 板の上の切株のこぶが 190 行目で帯の下端を削る（非空 2.34%）。150px の見出しと 12px の縁取りは今でも収まるが、「何も横切らない」という指定は満たしていない。

- `L260.png`
A blank weathered placard nailed to a tree at head height, its face faded to an even featureless pale surface with no characters or lines on it anywhere, shot dead centre and close, the BROKEN STUMP TOP CROPPED OUT of the frame entirely and the placard's top edge no higher than 45% down from the top of the frame, the placard and the trunk occupying the lower two thirds, one hard key light from the left so the board is markedly brighter than the wood behind it, and the ENTIRE UPPER 40% OF THE FRAME an unbroken field of pale bright overcast sky with nothing whatever entering it: no branch, no twig, no trunk, no post, no wire, no chain, no tree line, no distant hill and no horizon line anywhere within that upper 40% [STYLE] Avoid: [NEG]

**保存先:** `H:\pd-media\assets\ai\openfields\L260.png`（**既存を上書き**）

---

## 6. 発注書の検査（生成を始める前に済ませてある）

```
py -3.11 scripts/check_image_order_neg.py --file episodes/_planning/EP66_openfields_CODEX_BATCH_C.v001.md
```

顔／実在人物・読める文字・手書き・紋章／記章・数字の**五族すべて**が `[NEG]` に入っていることを機械が確認します。**`[NEG]` を1語でも削ったら、必ず再実行すること。**

## 7. 生成後にやること（発注者側）

1. **21枚を1枚ずつ目視**する。特に:
   - `L170` / `L175` / `L172` は **`L075` / `L082` / `L074` と並べて**見る。構図がずれていたら、その1枚だけ文言を直してもう1枚。
   - `L255`–`L257` / `L259` / `L260` は **1280x720 に縮小して、上 40% が本当に空で明るいか**を測る（`py -3.11 scripts/check_thumb_subject_luma.py --thumb <file>`。`outline` と `text height` は見出しを焼く前なので無意味。`subject luma` と `whole luma` だけ読む）。
   - `L146` / `L173` は**テールゲートとグリルを native で拡大**して、バッジが無いことを確かめる（前回は 372px のコンタクトシートでは見えず、4x で初めて出ました）。
   - `L247` / `L236` / `L252` は**手を native で拡大**して、指が数えられることを確かめる。
2. 合格したら、`mandatory_stills` / `people_plates` は**変更不要**（ID が同じため）。
3. `L255`–`L260` は `mandatory_stills` に入れない（THUMB はカットにならない）。契約 `thumbnail_candidates_min: 4` に対し、現在の合格は `L258` の1枚だけです。**このバッチが通って初めて 4 を満たします。**

