# サムネ ヒーロープレート — EP77〜EP82 ＋ EP35再作成 **v003**

> **v001 → 29枚中29枚が不合格。v002 → 33枚中26枚が不合格。**
> **v003は当てずっぽうではありません。落ちた項目を数えたら、原因は1つに絞れました。**
> 保存先: `E:\pd-media\05_visuals\thumbs\<slug>_v3\`（v2の隣に新フォルダ。上書きしない）

---

## 0. 何が直って、何が直っていないか（実測）

| | v1（29枚） | v2（33枚） | 勝ち組2枚 |
|---|---|---|---|
| 彩度 | 11.5 | **改善（47〜71まで出た）** | 54.9 |
| **明るい画素の割合** | 0.7 % | **0.4〜2.7 %** ← ここ | **7.2 %** |
| コントラスト | 33.4 | **31〜57** ← ここ | 74.0 |
| 明るさ | 19.1 | 20〜52 | 58.2 |

**v2で落ちた項目を数えた結果**

```
contrast     25件
bright_pct   20件   ← 白飛びした面が無い
brightness   17件
dark_pct     12件
saturation    9件   ← v1から大幅改善。色の指示は効いた
```

**色は直りました。直っていないのは「白飛びした明るい面」です。**

コントラストが低いのは結果であって原因ではありません。**画面の中に、はっきり白く飛んだ面積が無い**から、明暗の幅が出ていないだけです。

**そして station_v2 は5枚とも明るさ20〜24でした。** 原因は私です。**主題そのものを「暗いクラブの中」にした**ので、どう撮っても暗い絵にしかなりません。

---

## 1. v003 で変える2点（これだけ）

**① 光源を「背景」ではなく「主題」にする**

v2は「画面の中に光源がある」と書きました。Codexは**小さな光を隅に置きました**。

v003はこう書きます。**光っているもの自体を大きく写す。画面の1/5以上が白飛びしていること。**

**② 暗い場所を主題にしない**

「暗い部屋の中の小さな物」は、指示として自滅しています。**明るく照らされた面を主題**にします。

**触らないこと**：彩度・色の指定は v2 のままで足りています。

---

## 2. 数値目標（`check_thumb_punch.py` がこの帯域で判定）

```
明るさ      42〜78     ← v2 は 20〜52
コントラスト 60〜95     ← v2 は 31〜57
明るい画素   3〜16 %    ← v2 は 0.4〜2.7 %  ★ここが本丸
暗い画素    35〜72 %    ← v2 は 58〜86 %
彩度        30〜85     ← v2 で概ね達成
```

**狙いは明るい画素 6〜10 %。** 3 % は下限であって目標ではありません。

---

## 3. `[STYLE]` — 主題の後ろに貼る（v2から書き換え）

```
, the light source itself is IN the frame and is BLOWN OUT PURE WHITE, a large blazing
highlight filling at least a fifth of the picture with visible lens flare and light shafts,
the subject filling roughly half the picture and brightly lit, saturated colour, extreme
contrast between the blown highlight and one deep shadow side, ultra high resolution,
hyper-detailed, razor-sharp focus, photorealistic, volumetric light, 16:9 thumbnail hero shot,
scroll-stopping
```

## 4. `[NEG]` — 最後に貼る

```
Avoid: on-screen text, letters, numerals, readable documents, watermark, logo, identifiable
real person, faces, bodies, injuries, the moment of the accident, dim scene, dark room, night
interior with a small lamp, evenly dark image, flat lighting, low contrast, monochrome,
desaturated, muted colours, empty black frame, small distant subject, low-resolution.
```

**⛔ 二度と書かない語**：`deep black palette` / `vast empty dark negative space` /
`dark room` / `everything else falling to black`。**v1とv2を殺したのはこれらです。**

---

# EP77 — ボルチモア橋 · slug `keybridge_v3`

文字: `SIX MEN` / **`WERE UP THERE`**

| # | 主題 |
|---|---|
| 01 | The blazing white lamp head of a portable work light tower filling the left third of the frame, its amber beam blasting across an empty bridge deck through river mist, an orange traffic cone standing inside the pool of light |
| 02 | A bright inspection lamp flaring directly into the lens beside an electrical terminal block, the polished metal and copper blazing white where the light hits, a blue wire stopping short of the clamp |
| 03 | A ship's engine-room alarm panel filling the whole frame with dozens of indicator lamps burning red and amber at full intensity, the panel glass blown out white at the centre |
| 04 | The rotating amber beacon of a works truck blazing directly into the lens at close range, blown out white at its core, a yellow hard hat lit hard beside it |
| 05 | A hard cyan-white floodlight blazing into the lens from the base of a bridge pier, a huge starburst flare, the concrete pier brilliantly lit and filling the right half |

# EP78 — コルガン航空3407便 · slug `colgan_v3`

文字: `EIGHTEEN SECONDS` / **`NOBODY LOOKED`**

| # | 主題 |
|---|---|
| 01 | A cockpit instrument panel filling the frame, lit brilliant red, one display blown out pure white at its centre, the control column in the foreground blurred by violent vibration |
| 02 | An airport approach light bar firing sequenced strobes straight into the lens through heavy falling snow, the strobes blown out white, the snow blazing in the beams |
| 03 | A suburban house window burning brilliant gold and blown out white, filling the left half of the frame, deep blue snow outside |
| 04 | An aircraft airspeed dial filling the frame, glass catching a hard blown-out specular highlight, the instrument face lit brilliant red, needle low |
| 05 | A green emergency exit sign blazing at close range in a crew room, blown out white at its core, the whole wall flooded green |

# EP79 — アラスカ航空261便 · slug `alaska261_v3`

文字: `FOUR EXTENSIONS` / **`APPROVED`**

| # | 主題 |
|---|---|
| 01 | A huge steel acme-threaded jackscrew filling the frame under a blazing inspection lamp that flares into the lens, the worn end catching a blown-out white highlight, threads sharp at the far end |
| 02 | A work lamp blazing directly into the lens in an aircraft hangar, blown out white, a grease gun lit hard in the foreground, the hangar floor brilliantly lit |
| 03 | A hangar bay door open at night with blue-white light flooding out and blowing out the frame, an aircraft tail silhouetted against the glare |
| 04 | A maintenance stand under an aircraft belly with a work lamp blasting upward into the structure, the panels blazing white where the beam lands |
| 05 | The Pacific at dusk with a brilliant orange sun band blown out white at its core across the horizon, the water throwing a hard specular path toward the camera |

# EP80 — コスタ・コンコルディア · slug `concordia_v3`

文字: `HE WAS` / **`ASHORE FIRST`**

| # | 主題 |
|---|---|
| 01 | An enormous white cruise ship hull on its side blasted by shore floodlights that flare into the lens, the white paint blown out, filling two-thirds of the frame, horizon dead level |
| 02 | A ship's dining room tilted thirty degrees with chandeliers blazing gold and blown out white, glassware sliding, the room brilliantly lit, no people |
| 03 | An orange lifeboat hanging sideways from its davit with a floodlight blazing into the lens behind it, the orange burning saturated, the hull brilliantly lit |
| 04 | A ship's bridge console at night with every instrument alight in amber and green at full intensity, one lamp blown out white, an empty chair |
| 05 | A white hull underwater lit by hard diver lights that flare into the lens, the beams cutting bright shafts through blue-green water, the hull blazing where they land |

# EP81 — ステーション・ナイトクラブ火災 · slug `station_v3`

**v2はここが5枚とも全滅しました。主題を「暗い部屋」から「照明そのもの」に変えます。火は出しません。**

文字: `NOT FIRE` / **`RETARDANT`**

| # | 主題 |
|---|---|
| 01 | A cluster of stage par-can lights blazing magenta and red directly into the lens at close range, blown out white at their cores, grey acoustic foam ceiling tiles brilliantly lit above them, one tile peeled back |
| 02 | A single hard white followspot blasting straight into the lens from the back of a small club stage, huge flare, the empty stage and a microphone stand brilliantly rim-lit |
| 03 | A green emergency exit sign blazing at close range above a corridor, blown out white at its core, the corridor walls flooded brilliant green |
| 04 | A wall of black acoustic foam raked by a blazing white beam that fills the right half of the frame and flares into the lens, the foam texture blown out where the light lands |
| 05 | A mirror ball throwing hundreds of hard white light spots across a brightly lit ceiling of foam tiles, the ball itself blown out at its centre |

# EP82 — エクソン・バルディーズ · slug `valdez_v3`

文字: `FIVE BILLION` / **`FIVE HUNDRED MILLION`**

| # | 主題 |
|---|---|
| 01 | A gloved hand holding a stone coated in glossy black oil under a blazing work lamp that flares into the lens, the oil throwing a brilliant iridescent specular sheen, the lamp blown out white |
| 02 | Coiled orange containment boom filling the frame under a floodlight blasting into the lens, the orange burning saturated and blown out where the beam lands |
| 03 | A cobble shoreline at low sun with a brilliant orange sun band blown out white on the horizon, the wet black upper halves of the stones throwing hard specular highlights |
| 04 | A fishing harbour at dusk with sodium dock lights blazing and flaring into the lens, blown out white at their cores, the water throwing the orange back brilliantly |
| 05 | Macro of an oil sheen on a steel deck catching a blown-out white specular highlight and brilliant iridescent purple and green, filling the frame |

# 【最優先】EP35 hinders 作り直し · slug `hinders_v3`

**v2は3枚中2枚が合格しています。落ちた1枚を含め、全部作り直します。**

文字: `NO CRIME` / **`NO CHARGE`**

| # | 主題 |
|---|---|
| 01 | An open empty steel cash drawer on a counter under a hard overhead lamp blazing into the lens, the brushed metal blown out white where the light lands, deep shadow on one side only |
| 02 | A green glass banker's lamp burning brilliantly at close range beside a stack of blank white envelopes, the lamp shade blown out, the counter flooded green |
| 03 | A closed shop shutter at night under a sodium street lamp blazing into the lens with a heavy starburst, the shutter brilliantly lit, wet pavement throwing the orange back |

---

# 手順（**まず1枚だけ**）

```
1. keybridge_v3 の 01 を 1枚だけ生成する
2. py -3.11 scripts/check_thumb_punch.py E:\pd-media\05_visuals\thumbs\keybridge_v3
3. 合格していたら残り32枚。落ちていたら、その1枚の数字を見て直す
```

**33枚出してから測るのを、これ以上繰り返さないための順番です。**

納品後は必ず両方:

```
py -3.11 scripts/check_thumb_punch.py  <フォルダ>   # 光と色
py -3.11 scripts/thumb_feed_sheet.py   <フォルダ>   # 168×94で目視
```

# 正直に書くこと

- 帯域は**勝った2枚から作りました。n=2 です。**「明るいほど勝つ」の証明ではありません
- 検査は**光と色しか見ません。意味は見ません。** 派手で何も言っていない絵は通ります
- **v3で直る保証はありません。** ただし v1→v2 で彩度は実際に直りました。**今回の変更点は1つだけ**なので、効いたかどうかは1枚で分かります
