# EP60 surfside — Codex 画像生成 引き継ぎプロンプト v001（40分・112枚・1プロンプト1枚）

> ## ⚠ 下書き。まだ Codex に渡さないこと。
> **オーナー指示 2026-08-01: 画像生成ファイルは台本ができた後でよい。**
> このファイルは台本（`EP60_surfside_FILM_BIBLE.v001`）より先に書かれてしまったので、
> 幕構成の見込みからプロンプトを積算している。**カット表と突き合わせていない。**
>
> 台本とカット表が出来たら、この112行を1行ずつカットに対応づけ、
> **対応先の無いプロンプトは削る／足りないカットにはプロンプトを足す**。
> その差分を当てて `v002` にしたものが、実際に渡す版になる。
>
> 先にプロンプトを書くと使われない絵が出る、というのが本作で直している当の失敗
> （実測: 210枚指定して約100枚が1カットも使われず終わっていた）。この下書きも
> 例外ではない前提で扱うこと。

**この1ファイルだけで作業できます。** 他の設計書を読む必要はありません。守るべき制約・スタイル・禁止事項・全プロンプト・完了条件を本文に書き切ってあります。

**題材:** 2021年6月24日、フロリダ州サーフサイドのシャンプレンタワー南棟が部分崩落し98人が亡くなった件。2026年6月22日にNISTが技術的知見を公表した。
**この映画は再現映像ではなく、記録の映画です。** 崩落そのものは描きません。

---

## 0. ★★★ 最重要：1プロンプト = 1枚 ★★★

**オーナー指示 2026-07-31。**

1. **各プロンプトから画像を1枚だけ生成する。** 同じプロンプトで2枚目を作らない。
2. **`_02` / `_03` を作らない。** 候補を並べて選ぶ工程は存在しない。
3. **「良いのが出るまで回す」を禁止。** 過去の設計書にあった「accepted が210になるまで繰り返す」「3回失敗したら…再度1枚」は**本ファイルには存在しない**。持ち込まない。
4. **やり直してよいのは、絵が §1 の禁止に触れたときだけ。** そのときも**プロンプトの文言を直してから1枚**。同じ文で引き直さない。
5. 生成器側でも強制済み: `scripts/generate_sdxl_4k.py` は既定 `--variants 1`、2以上は `--allow-variants` と理由なしには**実行を拒否**する。

> 背景（なぜこの規則があるか）: 実測で、ある話は257枚の仕様に対し**628枚**書き出され、355枚が捨てられていた。さらに全話で **S101〜S210 の約100枚が1カットも使われずに終わっていた**。本ファイルは**112枚しか要求せず、112枚すべてが画面に出る**。

---

## 1. ★絶対条件（違反した絵は使用不可）

### 1.1 事実・権利のロック

- **崩落の瞬間・瓦礫・救助・遺体を描かない。** 一切。
- **実在の建物「シャンプレンタワー南棟」の肖像を作らない。** 建物は**類型**として描く（1981年前後のフロリダ海岸の分譲高層住宅一般）。実物の写真と見紛うものを作らない。
- **実在人物の顔・肖像を作らない。** 人物は必要な場合のみ、**後ろ姿・手元・シルエット・顔が判別できない距離**で描く。
- **読める文字を一切描かない。** 書類・図面・標識・掲示物の文字は、**線の連なりに潰れて読めない**状態にする。数字も同じ。
- **公的な印章・紋章・ロゴ・州章・企業マークを描かない。**
- **偽の記録を作らない**（本物の報告書・判決文・警察文書に見える画像は不可）。
- 生成画像は**説明のための象徴**であって証拠ではない。公開時にAI使用を開示する。

### 1.2 機械チェック（生成後に必ず実行）

```
# ① まず許容フレーズを消す。ここを消さずに ② を当てない。
#    （"unreadable" "no letterforms" 等はプロンプト側の禁止指定なので誤検出する）
# ② 残った文字列にだけ当てる。
禁止語: text, lettering, letters, words, caption, label, signage, logo, emblem, seal,
        crest, watermark, signature, handwriting, numerals, digits
```

出力画像の目視で以下があれば**その絵は不合格**。プロンプトを直して1枚だけ作り直す。

| # | 不合格条件 |
|---|---|
| Q1 | 長辺が3840px未満 |
| Q2 | 読める文字・数字・署名が写っている |
| Q3 | 印章・紋章・ロゴらしきものが写っている |
| Q4 | 顔が判別できる人物が写っている |
| Q5 | 崩落・瓦礫・負傷者が写っている |
| Q6 | 他の絵と実質同じ構図（sha256重複・近接構図） |

---

## 2. 枚数（この数で確定。勝手に増やさない・減らさない）

| 役割 | ファイル | 枚数 | 用途 |
|---|---|---|---|
| 本編スチル | `S001.png` 〜 `S110.png` | **110** | 各1カット。全部使う |
| サムネイル | `T01.png`, `T02.png` | **2** | タイトルA/B用 |
| **合計** | | **112** | **1プロンプト1枚 = 112プロンプト** |

**i2v（静止画を動かす）用の種画像は作りません。** 直近2話は i2v をゼロで仕上げ、動きは実写素材で足りている実測があるためです。

**実写で撮れるものはAIで作りません。** 夜の街・書類の署名・法廷・工事現場・地下駐車場（一般）・救急車・海岸・夜明けは、実写素材が十分にあります（実測: 夜の街314本、書類747本、法廷144本、工事127本、駐車場45本、夜明け137本）。
**AIが担うのは、実写素材に無いものだけ**です（実測: `rebar` 1件、`corrosion` 0件、`spalling` 0件、`condominium` 0件、`surfside` 0件）。

内訳:
- **60枚** = 壊れていくコンクリートそのもの（鉄筋の腐食・剥落・スラブ裏・柱頭・滞水・ひび）
- **32枚** = 建物の類型（バルコニー・プールデッキ・共用廊下・駐車マス・夜の外観）
- **18枚** = この事件固有の象徴（受け皿の書類・査定通知・証拠袋の紙）

---

## 3. スタイル指定（マクロ）

★**必ず展開してから生成すること。** 過去に `[STYLE]` を展開しないまま267枚を生成し、**禁止事項155語が全部の絵から消える**事故が起きている。展開されているかを生成前に1件目で必ず目視確認する。

**`[STYLE]`** ＝ 以下をプロンプト末尾にそのまま連結:

> , cinematic still, cold institutional grey-blue concrete as the base palette, one warm amber note reserved strictly for morning light, corrosion stain and warning — never flooding the frame, near-black falloff at the edges, telephoto compression, shallow depth of field, restrained documentary framing, ultra-detailed, photoreal, 4K, 16:9, fine film grain, no text, no lettering, no numerals, no watermark, no logo, no seal, no emblem, no readable documents, no identifiable face

**`[NEG]`** ＝ `Avoid:` の後にそのまま連結:

> readable text, letterforms, numerals, signage, captions, watermarks, logos, seals, emblems, crests, identifiable faces, portraits of real people, collapsed buildings, rubble, debris fields, rescue scenes, injured people, bodies, gore, dramatic explosion, disaster movie lighting, cartoon, illustration, painterly, oversaturated, HDR halo

---

## 4. 生成コマンド

プロンプトは `episodes/PD-2026-060-surfside/04_scenes/ai_prompts.v001.md` に §5 の形式のまま転記してから:

```bash
./.venv/Scripts/python.exe scripts/generate_sdxl_4k.py PD-2026-060-surfside
```

`--variants` は**付けない**（既定で1枚）。出力先は `H:\pd-media\assets\ai\surfside\`。

---

## 5. プロンプト（112行・各1枚）

各ブロックは「ファイル名の行」→「プロンプトの行」の2行。プロンプト行の `[STYLE]` と `[NEG]` は §3 で置換すること。

### 5.1 COLD OPEN ＋ ACT I — 建物と、その下（S001–S026 / 26枚）

```
- `S001.png`
The underside of a thick concrete deck slab seen from directly below in near-darkness, a shallow grid of beams receding, one cold strip of light grazing the soffit, the ceiling of a place nobody looks at [STYLE] Avoid: [NEG]
- `S002.png`
A square concrete column head where it meets a deck slab, the thickened panel around it catching a low raking light, the joint that carries everything [STYLE] Avoid: [NEG]
- `S003.png`
An empty underground parking level at night, rows of columns receding into blackness, a single fluorescent tube burning far down the row, painted bay lines faded to nothing [STYLE] Avoid: [NEG]
- `S004.png`
Shallow water standing across a flat concrete deck after rain, the sky reflected in it, a drain sitting slightly too high to take it [STYLE] Avoid: [NEG]
- `S005.png`
A 1981-era Florida beachfront residential tower seen from the beach at dusk as a type, twelve floors of stacked balconies in silhouette, sea grass in the foreground, no identifying features [STYLE] Avoid: [NEG]
- `S006.png`
A tiled pool deck at first light, empty loungers stacked at the edge, a planter of heavy tropical greenery sitting on the slab [STYLE] Avoid: [NEG]
- `S007.png`
An unoccupied swimming pool at night lit only from within, the water perfectly still, the deck around it dark [STYLE] Avoid: [NEG]
- `S008.png`
A sliding glass balcony door from inside a dark apartment, curtain half drawn, the ocean a pale band beyond the rail [STYLE] Avoid: [NEG]
- `S009.png`
A residential corridor at night, identical doors receding, carpet worn down the centre line, one light out [STYLE] Avoid: [NEG]
- `S010.png`
A bank of brass mailboxes in a residential lobby, every door shut, cold overhead light [STYLE] Avoid: [NEG]
- `S011.png`
A lift lobby with the floor indicator dark, polished stone worn dull at the threshold [STYLE] Avoid: [NEG]
- `S012.png`
A single parked car in an underground bay seen from behind, dust settled on the boot lid, the column beside it filling the frame edge [STYLE] Avoid: [NEG]
- `S013.png`
Reinforcing steel bars laid in a grid inside formwork before a pour, clean and orderly, seen from above [STYLE] Avoid: [NEG]
- `S014.png`
A concrete slab edge in section, the pale aggregate face exposed, a line of reinforcement running through it [STYLE] Avoid: [NEG]
- `S015.png`
A drawing of a structural floor plan rendered as an unreadable smear of grid lines on drafting paper, a scale rule lying across it [STYLE] Avoid: [NEG]
- `S016.png`
An architect's rolled drawings standing in a corner of a site office, rubber bands perished, dust on the tops [STYLE] Avoid: [NEG]
- `S017.png`
A concrete pour in progress at night on an open deck, a chute and a screed board, workers only as distant silhouettes [STYLE] Avoid: [NEG]
- `S018.png`
The waterproof membrane on a flat deck, its seam lifting slightly at one edge where it meets an upstand [STYLE] Avoid: [NEG]
- `S019.png`
A drainage outlet in a concrete deck choked with sand and leaf litter, water pooled around its rim [STYLE] Avoid: [NEG]
- `S020.png`
Salt haze over a coastal balcony rail at dawn, white crystalline bloom on the steel [STYLE] Avoid: [NEG]
- `S021.png`
A heavy planter box on a deck slab seen from below the deck, its weight expressed by the sag of the surface it sits on [STYLE] Avoid: [NEG]
- `S022.png`
Paving slabs laid over a waterproof deck, sand bedding visible at a lifted corner [STYLE] Avoid: [NEG]
- `S023.png`
A garage ramp descending into darkness, tyre marks polished into the concrete [STYLE] Avoid: [NEG]
- `S024.png`
A residential building's service corridor with painted pipework overhead, a strip light flickering [STYLE] Avoid: [NEG]
- `S025.png`
An air-conditioning condensate line dripping steadily onto a concrete floor, a pale mineral trail beneath it [STYLE] Avoid: [NEG]
- `S026.png`
A twelve-storey residential tower seen at night from across a quiet street, most windows dark, two lit [STYLE] Avoid: [NEG]
```

### 5.2 ACT II — 2018年、それは書かれた（S027–S050 / 24枚）

```
- `S027.png`
A torch beam raking across a concrete garage ceiling, catching a map of hairline cracks [STYLE] Avoid: [NEG]
- `S028.png`
An engineer's gloved hand held flat against a spalled concrete surface, the palm not touching the deepest part [STYLE] Avoid: [NEG]
- `S029.png`
Concrete spalling on a column face, a fist-sized piece gone, the reinforcement behind it exposed and rust-stained [STYLE] Avoid: [NEG]
- `S030.png`
A corroded reinforcing bar emerging from broken concrete, its surface flaked into layers, orange staining running down the pale face below it [STYLE] Avoid: [NEG]
- `S031.png`
Rust weeping from a hairline crack in a concrete soffit, a brown tear-track a metre long [STYLE] Avoid: [NEG]
- `S032.png`
Macro of a crack in concrete wide enough to admit a coin, its edges crumbling [STYLE] Avoid: [NEG]
- `S033.png`
A camera flash lighting one small area of a vast dark garage ceiling, the rest falling away to black [STYLE] Avoid: [NEG]
- `S034.png`
A clipboard resting on a car bonnet in a garage, its form filled with unreadable marks [STYLE] Avoid: [NEG]
- `S035.png`
A surveyor's chalk mark on a concrete column, a plain cross with no letters [STYLE] Avoid: [NEG]
- `S036.png`
A hammer resting against a column base after a sounding survey, dust on the concrete beneath [STYLE] Avoid: [NEG]
- `S037.png`
A stack of survey photographs face down on a desk, only the blank backs visible [STYLE] Avoid: [NEG]
- `S038.png`
A typed report lying open on a desk under a lamp, every line of type dissolved into an unreadable grey band [STYLE] Avoid: [NEG]
- `S039.png`
A bound report closed on a table with a plain cover, no title, a paperclip at one corner [STYLE] Avoid: [NEG]
- `S040.png`
A hand sliding a report across a polished meeting table towards an empty chair, cropped at the wrist [STYLE] Avoid: [NEG]
- `S041.png`
An empty community meeting room set out with folding chairs in rows, a jug of water untouched [STYLE] Avoid: [NEG]
- `S042.png`
The same folding chairs after the meeting, pushed back at angles, one lying folded on the floor [STYLE] Avoid: [NEG]
- `S043.png`
A municipal counter with a bell and a closed shutter behind it, flat institutional light [STYLE] Avoid: [NEG]
- `S044.png`
A wire in-tray on a public official's desk with a single report sitting on top of routine paperwork [STYLE] Avoid: [NEG]
- `S045.png`
A dark wooden drawer half open, a bound document lying inside face up, its type an unreadable smear [STYLE] Avoid: [NEG]
- `S046.png`
An office filing cabinet drawer closing on a row of hanging folders, cold fluorescent light above [STYLE] Avoid: [NEG]
- `S047.png`
A desk telephone sitting silent beside a closed folder, cord neatly coiled [STYLE] Avoid: [NEG]
- `S048.png`
A wall calendar with its grid blurred to unreadable, one month's page curled at the corner [STYLE] Avoid: [NEG]
- `S049.png`
A concrete column photographed straight on with a scale card leaning against its base, the card's markings illegible [STYLE] Avoid: [NEG]
- `S050.png`
A garage ceiling seen wide with a single patch of newer, paler repair concrete in one bay [STYLE] Avoid: [NEG]
```

### 5.3 ACT III — 金額（S051–S068 / 18枚）

```
- `S051.png`
A carbon-copy contractor's estimate on a desk, its columns of figures reduced to grey rules with no digits [STYLE] Avoid: [NEG]
- `S052.png`
A pocket calculator lying face up on a stack of papers, its display blank [STYLE] Avoid: [NEG]
- `S053.png`
A residential letterbox with an envelope pushed halfway in, unaddressed [STYLE] Avoid: [NEG]
- `S054.png`
A kitchen table at night with one envelope opened and the letter unfolded beside it, its lines illegible [STYLE] Avoid: [NEG]
- `S055.png`
A pair of reading glasses set down on a document, the page beneath them out of focus [STYLE] Avoid: [NEG]
- `S056.png`
A community notice board in a lobby with plain unmarked sheets pinned to it [STYLE] Avoid: [NEG]
- `S057.png`
A show of hands in a dim meeting room seen from behind and above, faces out of frame [STYLE] Avoid: [NEG]
- `S058.png`
A ledger book open on a table, its ruled columns a soft blur, a pen laid in the gutter [STYLE] Avoid: [NEG]
- `S059.png`
An empty chairperson's seat at the head of a meeting table, papers squared in front of it [STYLE] Avoid: [NEG]
- `S060.png`
A car park bay marked out on cracked asphalt with the paint worn to a ghost [STYLE] Avoid: [NEG]
- `S061.png`
A stack of unopened envelopes fanned across a desk, all blank [STYLE] Avoid: [NEG]
- `S062.png`
A whiteboard wiped almost clean, the ghost of erased marks still on it, no letters legible [STYLE] Avoid: [NEG]
- `S063.png`
A contractor's site sign frame standing empty at a kerb, nothing mounted in it [STYLE] Avoid: [NEG]
- `S064.png`
Scaffold poles stacked and banded on a pavement, unused, tarpaulin folded on top [STYLE] Avoid: [NEG]
- `S065.png`
A repair permit envelope lying on a hall table under keys, its face turned to an unreadable smear [STYLE] Avoid: [NEG]
- `S066.png`
Three years of dust on a stored roll of drawings in a cupboard, seen close [STYLE] Avoid: [NEG]
- `S067.png`
A hand hovering over a chequebook without writing, cropped at the cuff [STYLE] Avoid: [NEG]
- `S068.png`
The same underground garage as before, unchanged, the cracked ceiling exactly as it was [STYLE] Avoid: [NEG]
```

### 5.4 ACT IV — 最後の春（S069–S084 / 16枚）

```
- `S069.png`
A towel left folded on a pool lounger in the morning sun, nobody in frame [STYLE] Avoid: [NEG]
- `S070.png`
A bicycle chained to a rail in a garage, tyres soft [STYLE] Avoid: [NEG]
- `S071.png`
A balcony table with two chairs and a cup left out, the sea beyond in haze [STYLE] Avoid: [NEG]
- `S072.png`
Laundry drying on a balcony rail against a bright coastal sky [STYLE] Avoid: [NEG]
- `S073.png`
A lit apartment window seen from the street at night, curtains open, the room beyond ordinary and empty [STYLE] Avoid: [NEG]
- `S074.png`
A pot plant on a windowsill catching late afternoon light [STYLE] Avoid: [NEG]
- `S075.png`
A hallway with a delivery box left outside a door [STYLE] Avoid: [NEG]
- `S076.png`
A car reversing out of a garage bay, taillights bright, driver not visible [STYLE] Avoid: [NEG]
- `S077.png`
A pool deck at midday with the water surface broken by wind, empty [STYLE] Avoid: [NEG]
- `S078.png`
A contractor's tape marking off a small area of deck, the rest of the deck in normal use [STYLE] Avoid: [NEG]
- `S079.png`
A drill bit and a bag of anchors on a folded dust sheet, work about to begin [STYLE] Avoid: [NEG]
- `S080.png`
An extension lead run down a garage ramp and taped to the floor [STYLE] Avoid: [NEG]
- `S081.png`
A residential building seen from the beach at sunset, warm light on the balconies [STYLE] Avoid: [NEG]
- `S082.png`
An open apartment door with a key still in the lock, the corridor beyond dim [STYLE] Avoid: [NEG]
- `S083.png`
A bedroom at night with the curtains open and the sea black beyond, bed made, nobody in frame [STYLE] Avoid: [NEG]
- `S084.png`
A kitchen clock on a wall, its hands present but its numerals dissolved to nothing [STYLE] Avoid: [NEG]
```

### 5.5 ACT V — 三週間（S085–S104 / 20枚）

```
- `S085.png`
A single hairline crack in a concrete soffit, photographed very close, running out of frame in both directions [STYLE] Avoid: [NEG]
- `S086.png`
The same crack wider, its edges shed to powder, fine debris on the floor beneath [STYLE] Avoid: [NEG]
- `S087.png`
Concrete dust lying in a small cone on a garage floor directly beneath a ceiling defect [STYLE] Avoid: [NEG]
- `S088.png`
A column head where the slab above it has begun to depress around the connection, the geometry no longer flat [STYLE] Avoid: [NEG]
- `S089.png`
Reinforcement exposed across a wide patch of soffit, the bars parallel and heavily corroded [STYLE] Avoid: [NEG]
- `S090.png`
A steel bar reduced by rust to a fraction of its section, seen in close macro against pale concrete [STYLE] Avoid: [NEG]
- `S091.png`
Water tracking along a crack line in a ceiling and dripping from its lowest point [STYLE] Avoid: [NEG]
- `S092.png`
A puddle on a garage floor with fine grey sediment settled in it [STYLE] Avoid: [NEG]
- `S093.png`
A deck surface from above with a shallow depression holding water where the slab has moved [STYLE] Avoid: [NEG]
- `S094.png`
Paving on a deck lifted very slightly out of plane along one line, seen at a raking angle [STYLE] Avoid: [NEG]
- `S095.png`
An empty garage at two in the morning, one column in the foreground, the far end unlit [STYLE] Avoid: [NEG]
- `S096.png`
A concrete slab soffit seen wide with the light falling off to black at every edge, nothing else in frame [STYLE] Avoid: [NEG]
- `S097.png`
A load path expressed as an abstract dark diagram of columns and a slab, geometry only, no annotation [STYLE] Avoid: [NEG]
- `S098.png`
The junction of two structural elements photographed head on, the smaller carrying the larger [STYLE] Avoid: [NEG]
- `S099.png`
A hairline fracture ring in a concrete surface around a column head, faint but continuous [STYLE] Avoid: [NEG]
- `S100.png`
A stairwell at night with an emergency light casting a single hard shadow [STYLE] Avoid: [NEG]
- `S101.png`
A residential tower at one in the morning seen from a distance, almost all windows dark [STYLE] Avoid: [NEG]
- `S102.png`
The sea at night from a beach, no horizon visible, the sound implied [STYLE] Avoid: [NEG]
- `S103.png`
An interior corridor with the lights out, only an exit sign's glow with no legible letters [STYLE] Avoid: [NEG]
- `S104.png`
An unremarkable concrete surface filling the frame, structurally sound in appearance, giving nothing away [STYLE] Avoid: [NEG]
```

### 5.6 ENDING（S105–S110 / 6枚）

```
- `S105.png`
A document sealed inside a clear evidence sleeve on a table, its type illegible, a plain tag tied at one corner [STYLE] Avoid: [NEG]
- `S106.png`
A courtroom bench and empty chairs photographed from the gallery in flat daylight [STYLE] Avoid: [NEG]
- `S107.png`
A settlement agreement lying closed on a table with a pen beside it, no words visible [STYLE] Avoid: [NEG]
- `S108.png`
A vacant coastal lot at dawn, fenced, sand blown across flat ground, nothing standing [STYLE] Avoid: [NEG]
- `S109.png`
Sunrise over open water seen from a beach, the light low and level [STYLE] Avoid: [NEG]
- `S110.png`
A concrete column in a working garage somewhere else entirely, ordinary and sound, in daylight [STYLE] Avoid: [NEG]
```

### 5.7 サムネイル（T01–T02 / 2枚）

サムネイルは**顔を使いません**（この映画では犠牲者を名指しせず描かない方針のため）。物と時間で引きます。

```
- `T01.png`
A concrete deck slab underside at night with a single deep crack running across it, one hard light from below, vast negative space in the upper left for large text, dread held in geometry alone, 1280x720 composition [STYLE] Avoid: [NEG]
- `T02.png`
A still swimming pool at night viewed from the deck with the dark bulk of a residential tower rising behind it, one lit window, clean negative space on the right for large text, 1280x720 composition [STYLE] Avoid: [NEG]
```

---

## 6. 完了条件（全部緑で完了。1つでも赤なら未完了）

```
[A-1] H:\pd-media\assets\ai\surfside\ に S001..S110 (110枚) + T01,T02 (2枚) = 112枚
[A-2] _02 / _03 が0件（1プロンプト1枚が守られている）
[A-3] 全112枚の長辺 >= 3840px（T01/T02 は 1280x720 で可）
[A-4] §1.2 の Q1–Q6 を全112枚で目視。1枚も該当なし
[A-5] sha256 重複ゼロ
[A-6] 生成に使ったプロンプト文で [STYLE] / [NEG] が展開済みであることを1件目で確認した記録
```

**枚数が112に届かないまま先へ進まない。基準を下げない。水増ししない。**

---

*2026-07-31/08-01 作成。枚数は実測から積算: 40分 ≒ 520カット、実写63% / AIスチル21% ≒ 110カット、AIスチルは1カット1枚使い切り。実写素材の在庫（夜の街314・書類747・法廷144・工事127・駐車場45・夜明け137）と欠品（rebar 1・corrosion 0・spalling 0・condominium 0・surfside 0）を YouTube/アーカイブ台帳17万行に対して実測し、AIは欠品側にだけ割り当てた。事実は `EP60_surfside_FACTS_LEDGER.v001.md`、配分の根拠は `EP60_surfside_ASSET_DESIGN.v001.md`。*
