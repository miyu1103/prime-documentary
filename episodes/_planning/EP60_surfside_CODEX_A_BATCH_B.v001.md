# EP60 surfside — Codex 画像生成 **バッチB** v001（56枚・1プロンプト1枚）

> ## ✅ これも今すぐ着手してよいファイルです。
> **バッチA（S001–S056）と合わせて、EP60の画像は合計112枚で完結します。**
> バッチAは「実写に存在しないコンクリートの破壊」でした。バッチBは**台本 v003 が要求する、それ以外の絵**です。
> 台本（`EP60_surfside_script.en.v003.md`・6,154語・35.6分）が確定したので、幕ごとに必要な絵を拾って積算しました。
>
> **実写素材で撮れるものは、ここに入れていません。**夜の街・法廷・工事現場・救急車・夜明けの海・一般的な書類は棚にあります（実測: 夜の街314本・法廷144本・工事127本・書類747本・夜明け137本）。
> AIが担うのは、**この事件のこの場面**であって、汎用の素材では代わりが利かないものだけです。

**題材:** 2021年6月24日、フロリダ州サーフサイドのシャンプレンタワー南棟が部分崩落し98人が亡くなった件。
**この映画は再現映像ではありません。崩落そのものは描きません。**

---

## 0. ★★★ 最重要：1プロンプト = 1枚 ★★★

1. **各プロンプトから画像を1枚だけ作る。** 同じプロンプトで2枚目を作らない。
2. **`_02` / `_03` を作らない。** 候補を並べて選ぶ工程は存在しない。
3. **「良いのが出るまで回す」を禁止。**
4. **作り直してよいのは §1 の禁止に触れたときだけ。** そのときも**文言を直してから1枚**。

---

## 1. ★絶対条件（触れた絵は使用不可）

- **崩落・瓦礫・救助・遺体を描かない。**
- **実在の建物「シャンプレンタワー南棟」の肖像を作らない。** 建物は**1981年前後のフロリダ海岸の分譲高層住宅という類型**として描く。実物の写真と見紛うものを作らない。
- **実在人物の顔を作らない。** 人は**手元・後ろ姿・シルエット・顔が判別できない距離**のみ。
- **読める文字・数字を一切描かない。** 書類・図面・掲示物・カレンダーの文字は、線の連なりに潰れて読めない状態にする。
- **印章・紋章・ロゴを描かない。**
- **本物の報告書・公文書に見える画像を作らない。**

### 生成後のチェック（1枚ずつ目視）

| # | 不合格条件 |
|---|---|
| Q1 | 長辺が3840px未満（T01/T02は1280×720で可） |
| Q2 | 読める文字・数字・署名がある |
| Q3 | 印章・紋章・ロゴらしきものがある |
| Q4 | 顔が判別できる人物がいる |
| Q5 | 崩落・瓦礫・負傷者が写っている |
| Q6 | 他の絵と実質同じ構図（バッチAの56枚とも照合すること） |

---

## 2. スタイル（★必ず展開してから生成）

**`[STYLE]`** ＝ 末尾にそのまま連結:

> , cinematic still, cold institutional grey-blue concrete as the base palette, one warm amber note reserved strictly for morning light, corrosion stain and warning — never flooding the frame, near-black falloff at the edges, telephoto compression, shallow depth of field, restrained documentary framing, ultra-detailed, photoreal, 4K, 16:9, fine film grain, no text, no lettering, no numerals, no watermark, no logo, no seal, no emblem, no readable documents, no identifiable face

**`[NEG]`** ＝ `Avoid:` の後にそのまま連結:

> readable text, letterforms, numerals, signage, captions, watermarks, logos, seals, emblems, crests, identifiable faces, portraits of real people, collapsed buildings, rubble, debris fields, rescue scenes, injured people, bodies, gore, dramatic explosion, disaster movie lighting, cartoon, illustration, painterly, oversaturated, HDR halo

1枚目で展開されているか必ず目視確認すること（過去に展開漏れで禁止事項155語が全画像から消えた事故あり）。

---

## 3. 出力

- 出力先: `H:\pd-media\assets\ai\surfside\`
- **S057.png 〜 S110.png（54枚）＋ T01.png・T02.png（2枚）= 56枚**
- 番号はバッチAの続き。S001–S056 は既存なので上書きしない。

---

## 4. プロンプト（56行・各1枚）

### 4.1 第1幕 — 建物と、共有されているもの（S057–S072 / 16枚）

台本：*「その建物の人たちは所有者だった。借り手ではない。…共有されているもののうち、デッキは人が実際に使う場所だった」*

```
- `S057.png`
A twelve-storey 1981-era beachfront residential tower seen from the sand at dusk as a generic type, stacked balconies in silhouette, sea grass in the foreground, no identifying features [STYLE] Avoid: [NEG]
- `S058.png`
The same order of tower seen from a quiet street at night, most windows dark, two lit, palms motionless [STYLE] Avoid: [NEG]
- `S059.png`
A row of identical balcony rails on a coastal apartment block photographed flat-on in hard morning light [STYLE] Avoid: [NEG]
- `S060.png`
A residential corridor at night, identical doors receding, carpet worn along the centre line, one ceiling light out [STYLE] Avoid: [NEG]
- `S061.png`
A lift lobby in a residential building, floor indicator dark, polished stone worn dull at the threshold [STYLE] Avoid: [NEG]
- `S062.png`
A bank of brass mailboxes in a residential lobby, every door shut, cold overhead light [STYLE] Avoid: [NEG]
- `S063.png`
A sliding glass balcony door seen from inside a dark apartment, curtain half drawn, the ocean a pale band beyond the rail [STYLE] Avoid: [NEG]
- `S064.png`
An empty swimming pool deck at first light, loungers stacked at one edge, the water perfectly still [STYLE] Avoid: [NEG]
- `S065.png`
A swimming pool at night lit only from within, the deck around it dark, no people [STYLE] Avoid: [NEG]
- `S066.png`
Sun umbrellas folded and tied on a pool deck at dawn, long shadows across the tiles [STYLE] Avoid: [NEG]
- `S067.png`
A poolside gate standing open onto a deck, the tower rising behind it out of focus [STYLE] Avoid: [NEG]
- `S068.png`
A stack of folded pool towels on a shelf in a shaded alcove, nobody present [STYLE] Avoid: [NEG]
- `S069.png`
A residential building's plant room door in a corridor, painted shut-looking, a single caged bulb above it [STYLE] Avoid: [NEG]
- `S070.png`
Looking straight up a coastal residential tower from its base, twelve floors of balconies converging, flat white sky [STYLE] Avoid: [NEG]
- `S071.png`
A municipal counter in a small town hall, a bell on the surface, shutters closed behind it, flat institutional light [STYLE] Avoid: [NEG]
- `S072.png`
A wall calendar in an office with its grid and numerals dissolved to unreadable marks, one page curled at the corner [STYLE] Avoid: [NEG]
```

### 4.2 第2幕 — 技師の仕事、報告書、そしてあの部屋（S073–S088 / 16枚）

台本：*「彼はデッキを歩いた。ランプを降りてガレージに入った。そしてコンクリートについて最も多くを教えるもの — 叩くこと — をやった」* ／ *「議事録によれば、建物は非常に良い状態だと彼は言った」*

```
- `S073.png`
An anonymised engineer's hand swinging a small hammer against a concrete ceiling, cropped at the wrist, dust caught in a torch beam [STYLE] Avoid: [NEG]
- `S074.png`
An engineer's boots and the base of a tripod on a garage floor beside a column, seen from behind at low level [STYLE] Avoid: [NEG]
- `S075.png`
A hand-held work light lying on a garage floor, its beam thrown flat across the concrete towards a column [STYLE] Avoid: [NEG]
- `S076.png`
A clipboard resting on a car bonnet in a garage, its form filled with unreadable marks, a pen across it [STYLE] Avoid: [NEG]
- `S077.png`
A folding measuring rule opened against a cracked concrete surface, the markings blurred to nothing [STYLE] Avoid: [NEG]
- `S078.png`
A bound engineering report lying closed on a desk under a lamp, plain cover, a paperclip at one corner [STYLE] Avoid: [NEG]
- `S079.png`
The same report open, its typed lines dissolved into an unreadable grey band, a hand at the frame edge turning a page [STYLE] Avoid: [NEG]
- `S080.png`
Photographs laid out face down in a grid on a desk, only the blank backs showing [STYLE] Avoid: [NEG]
- `S081.png`
A manila envelope on a hall table with keys beside it, its face turned to an unreadable smear [STYLE] Avoid: [NEG]
- `S082.png`
A wire out-tray on an office desk holding a single thick envelope, cold fluorescent light overhead [STYLE] Avoid: [NEG]
- `S083.png`
An empty community meeting room set out with folding chairs in uneven rows, a jug of water and glasses on a side table [STYLE] Avoid: [NEG]
- `S084.png`
A long table in that meeting room with a bound report lying on it, chairs pushed back, nobody present [STYLE] Avoid: [NEG]
- `S085.png`
The same room after the meeting, chairs at angles, one folded flat on the floor, lights still on [STYLE] Avoid: [NEG]
- `S086.png`
A municipal filing cabinet drawer closing on a row of hanging folders, cold institutional light [STYLE] Avoid: [NEG]
- `S087.png`
A dark wooden drawer half open with a bound document lying inside face up, its type an unreadable smear [STYLE] Avoid: [NEG]
- `S088.png`
An office desk telephone sitting silent beside a closed folder, cord neatly coiled [STYLE] Avoid: [NEG]
```

### 4.3 第3幕 — 金額（S089–S098 / 10枚）

台本：*「積立金は約70万6,000ドル。試算は1,030万ドル。…7%」* ／ *「1ベッドルームは80,190ドル。4ベッドルームのペントハウスは336,135ドル」*

```
- `S089.png`
An accounts ledger open on a desk, its ruled columns a soft blur with no legible figures, a pen laid in the gutter [STYLE] Avoid: [NEG]
- `S090.png`
A pocket calculator lying face up on a stack of papers, its display blank [STYLE] Avoid: [NEG]
- `S091.png`
A bank statement lying on a kitchen table with every line dissolved to unreadable, a mug at the frame edge [STYLE] Avoid: [NEG]
- `S092.png`
A residential letterbox with an envelope pushed halfway in, unaddressed, seen close [STYLE] Avoid: [NEG]
- `S093.png`
A kitchen table at night with an opened envelope and the letter unfolded beside it, lines illegible, one lamp lit [STYLE] Avoid: [NEG]
- `S094.png`
A pair of reading glasses set down on a document, the page beneath them out of focus [STYLE] Avoid: [NEG]
- `S095.png`
A community notice board in a lobby with plain unmarked sheets pinned to it in a grid [STYLE] Avoid: [NEG]
- `S096.png`
Raised hands seen from behind and above in a dim meeting room, faces out of frame, a vote in progress [STYLE] Avoid: [NEG]
- `S097.png`
An empty chairperson's seat at the head of a meeting table, papers squared in front of it [STYLE] Avoid: [NEG]
- `S098.png`
A chequebook lying open and unwritten on a table, a pen beside it untouched [STYLE] Avoid: [NEG]
```

### 4.4 第4幕 — 最後の春（S099–S106 / 8枚）

台本：*「タオルはラウンジャーに置かれたままだった。…建物は6月24日に落ちた。金は7月1日が期限だった」*

```
- `S099.png`
A towel left folded on a poolside lounger in morning sun, nobody in frame [STYLE] Avoid: [NEG]
- `S100.png`
Laundry drying on a balcony rail against a bright coastal sky, gently moving [STYLE] Avoid: [NEG]
- `S101.png`
A balcony table with two chairs and a cup left out, the sea beyond in haze [STYLE] Avoid: [NEG]
- `S102.png`
A car reversing out of an underground bay, taillights bright, driver not visible [STYLE] Avoid: [NEG]
- `S103.png`
A lit apartment window seen from the street at night, curtains open, the room beyond ordinary and empty [STYLE] Avoid: [NEG]
- `S104.png`
A potted plant on a windowsill catching late afternoon light, the sea out of focus behind [STYLE] Avoid: [NEG]
- `S105.png`
A contractor's tape marking off a small area of pool deck while the rest of the deck stays in normal use [STYLE] Avoid: [NEG]
- `S106.png`
A folded dust sheet and a bag of anchors set down beside a column in a garage, work not yet started [STYLE] Avoid: [NEG]
```

### 4.5 第5幕・その夜・結末（S107–S110 / 4枚）

台本：*「連邦の研究所で」* ／ *「木曜日だった。中にいた人のほとんどは眠っていた」* ／ *「書類が揃ったまま、その建物は落ちた」*

```
- `S107.png`
Gloved hands arranging aged technical drawings side by side on a glowing light table in a darkened laboratory, every line a smear [STYLE] Avoid: [NEG]
- `S108.png`
A coastal residential tower seen from far down a dark empty street at one-thirty in the morning, almost every window unlit [STYLE] Avoid: [NEG]
- `S109.png`
A document sealed inside a clear evidence sleeve on a table, its type illegible, a plain tag tied at one corner [STYLE] Avoid: [NEG]
- `S110.png`
A vacant coastal lot at dawn behind a plain fence, sand blown flat across bare ground, nothing standing [STYLE] Avoid: [NEG]
```

### 4.6 サムネイル（T01–T02 / 2枚）

**顔は使いません**（本作は犠牲者を名指しせず描かない方針）。物と時間で引きます。

```
- `T01.png`
A concrete deck slab seen from directly below at night with one deep crack running across it, a single hard light raking from below, vast negative space in the upper left for large text, 1280x720 composition [STYLE] Avoid: [NEG]
- `T02.png`
A still swimming pool at night viewed across the deck with the dark bulk of a residential tower rising behind it and one lit window, clean negative space on the right for large text, 1280x720 composition [STYLE] Avoid: [NEG]
```

---

## 5. 完了条件（全部緑で完了）

```
[B-1] H:\pd-media\assets\ai\surfside\ に S057..S110 (54枚) + T01,T02 (2枚) = 56枚
[B-2] バッチAと合わせて S001..S110 + T01,T02 = 112枚
[B-3] _02 / _03 が0件
[B-4] S057..S110 の長辺 >= 3840px（T01/T02 は 1280x720 で可）
[B-5] §1 の Q1–Q6 を全56枚で目視。1枚も該当なし。Q6はバッチAの56枚とも照合
[B-6] sha256 重複ゼロ（112枚全体で）
[B-7] 1枚目で [STYLE] / [NEG] が展開済みであることを確認した記録
```

**56枚に届かないまま先へ進まない。基準を下げない。水増ししない。**

---

*2026-08-01 作成。台本 `EP60_surfside_script.en.v003.md`（6,154語・35.6分・全craftゲート緑）の幕構成から積算。実写素材で代替できるもの（夜の街314本・法廷144本・工事127本・書類747本・夜明け137本）は除外し、この事件のこの場面にしか使えない絵だけを残した。事実は `EP60_surfside_FACTS_LEDGER.v001.md`、配分の根拠は `EP60_surfside_ASSET_DESIGN.v001.md`。*
