# サムネ ヒーロープレート — EP77〜EP82 ＋ EP35再作成（Codex生成用）**v002**

> **v001 は失敗しました。作り直しです。**
> v001 の29枚は納品され、**29枚とも新しい検査に落ちました**。理由は好みではなく数字です（§0）。
> **v001 は使わないでください。**

**保存先**: `E:\pd-media\05_visuals\thumbs\<slug>_v2\` に `THUMB-01.png`〜。
**v001 の隣に新しいフォルダを作ってください。上書きしないこと**（古い方は記録として残す）。

---

## 0. なぜ作り直すのか — 実測

v001 の指示に「**deep black palette, vast empty dark negative space**」と書いたのは私です。
Codexはそのとおりに作りました。**そして、そのとおりだったから失敗しました。**

| | チャンネルが**勝った**2枚 | v001 の29枚 | 差 |
|---|---|---|---|
| 明るさ | **58.2** | 19.1 | **1/3** |
| コントラスト | **74.0** | 33.4 | 半分以下 |
| 明るい画素の割合 | **7.2 %** | 0.7 % | **1/10** |
| 暗い画素の割合 | 60.8 % | **85.9 %** | 暗すぎる |
| 彩度（色の強さ） | **54.9** | 11.5 | **1/5** |

勝った2枚の内訳:

| | CTR | 明るさ | 彩度 | 何があるか |
|---|---|---|---|---|
| `016-titan` | **3.14 %** | 66.7 | **73.5** | **シアンと緑の光線**が画面の中にある |
| `017-onecoin` | **3.71 %** | 49.8 | **36.2** | **金色のキーライト**が画面の中にある |

**両方とも、画面の中に強い色のついた光源があります。** v001の29枚には光源がありません。
静物写真であって、映画のワンカットではありませんでした。

**検査**: `py -3.11 scripts/check_thumb_punch.py <フォルダ>`
実演済み — 勝った2枚は通り、**v001は29枚中29枚落ちます**。

---

## 1. v002 の絶対条件（v001から変わった点）

**変わっていないもの**
- **画像に文字を入れない**（Remotionで重ねる）／**実在人物の肖像なし**／**読める書類を作らない**
- **事故の瞬間・遺体・被災者の苦痛を出さない**
- 16:9・1プロンプト1枚

**変わったもの — ここが全部**

| v001（失敗） | v002（これでいく） |
|---|---|
| deep black palette | **黒地に、強い色のついた光源が画面の中にある** |
| vast empty dark negative space | **暗いのは片側だけ。全体を暗くしない** |
| a single powerful focal subject（結果：小さい静物） | **主役が画面の40〜60%を占める** |
| （明るさの指定なし） | **明るい部分を必ず作る**（画素の3〜16%が白飛び寸前） |
| （彩度の指定なし） | **強い色を1色**（シアン／琥珀／緑／赤／金のどれか） |

**数値目標**（`check_thumb_punch.py` がこの帯域で判定します）

```
明るさ 42〜78 ／ コントラスト 60〜95 ／ 明るい画素 3〜16% ／ 暗い画素 35〜72% ／ 彩度 30〜85
```

## 2. 全プレート共通のプロンプト部品

各行の主題の前後に、これをそのまま付けてください。

**[STYLE]**（主題の後ろに置く）
```
, one strong coloured practical light source visible inside the frame throwing a hard beam and
lens flare, the subject filling roughly half the picture, cinematic key-art lighting with a
blown-out highlight and deep shadow on one side only, saturated colour, high contrast,
ultra high resolution, hyper-detailed, razor-sharp focus, photorealistic, volumetric light
shafts, atmospheric haze catching the beam, 16:9 thumbnail hero shot, scroll-stopping
```

**[NEG]**（最後に置く）
```
Avoid: on-screen text, letters, numerals, readable documents, watermark, logo, identifiable
real person, faces, bodies, injuries, the moment of the accident, flat lighting, evenly dark
image, monochrome, desaturated, muted colours, empty black frame, small distant subject,
low-resolution.
```

**⚠ `deep black palette` と `vast empty negative space` は二度と書かないこと。** それがv001を殺しました。

---

# EP77 — ボルチモア橋崩落（2024） · slug `keybridge_v2`

事実は `EP77_keybridge_FACTS_LEDGER.v001.md` にあります。**係争中。有罪を断定する語は使えません。**

**サムネ文字**: `SIX MEN` / **`WERE UP THERE`** ／ 代案 `LIGHTS BACK` / **`NOT THE PROPELLER`**

| # | 主題（この後ろに [STYLE]、最後に [NEG]） |
|---|---|
| 01 | A tall portable work light tower blazing white-hot on an empty highway bridge deck at night, its amber beam cutting through river mist, a single orange traffic cone standing inside the pool of light, wet asphalt throwing the glare back |
| 02 | Extreme macro of an electrical terminal block cut open, the gold spring clamp glowing orange as if hot, a thick blue wire stopping visibly short of it, an inspection lamp flaring from the right, copper catching the light |
| 03 | A ship's engine-room switchboard filling the frame with every indicator lamp burning red and amber at once, an alarm wall in the dark, the glow reflecting off brushed steel |
| 04 | A yellow hard hat resting on a concrete barrier, lit by the rotating amber beacon of a works truck flaring directly into the lens, the empty road falling away behind |
| 05 | A steel truss bridge span seen from water level, one pier lit from below by a hard cyan-white floodlight with a visible starburst flare, the span filling the upper half of the frame, black water below |

# EP78 — コルガン航空3407便（2009） · slug `colgan_v2`

**⚠ 前提を差し替えた回です**（福島は取り止め）。事実は EP78 の台帳を作ってから。
NTSBの推定原因は**機長の操作**であり、システムだけを責める絵にしないこと。

**サムネ文字**: `FOUR TIMES` / **`APPROVED`**（案）／ 代案 `THE RECORD` / **`NOBODY SAW`**

| # | 主題 |
|---|---|
| 01 | A dark cockpit at night lit only by deep red instrument glow, the control column in the foreground blurred by violent vibration, red light flaring off the glass |
| 02 | An airport approach light bar blazing sequenced white strobes through heavy falling snow, the beams filling the frame, everything else black |
| 03 | A single suburban house window burning warm gold in a deep blue snowbound street at night, seen from low across untouched snow |
| 04 | An aircraft airspeed instrument face lit red in the dark, needle low, glass catching a hard reflection, filling most of the frame, no numerals legible |
| 05 | An empty airline crew rest room at night lit only by a blazing green exit sign, a folded uniform jacket on a chair, the green light flooding the wall |

# EP79 — アラスカ航空261便（2000） · slug `alaska261_v2`

**FAAが給油間隔を4回にわたって延長認可**（500飛行時間 → 約2,550時間）。

**サムネ文字**: `FOUR EXTENSIONS` / **`APPROVED`** ／ 代案 `WORN` / **`ON PAPER, FINE`**

| # | 主題 |
|---|---|
| 01 | Extreme macro of a huge steel acme-threaded jackscrew under a hard inspection lamp, the threads crisp at one end and worn mirror-smooth at the other, the worn end catching a blazing hot highlight |
| 02 | A grease gun standing on an oil-stained hangar floor with a work lamp flaring behind it, amber light raking across the concrete, the hangar swallowed in blue shadow |
| 03 | A vast hangar at night with one bay door open and blue-white light flooding out across the apron, an aircraft tail in silhouette against it |
| 04 | A maintenance stand under an aircraft belly at night, a single work lamp blazing upward into the structure, hard shadows fanning across the panels |
| 05 | The Pacific at dusk from high above, a burning orange band of low sun across black water, one set of ripple rings, nothing else |

# EP80 — コスタ・コンコルディア（2012） · slug `concordia_v2`

**破棄院が16年を確定（2017-05-12）。**

**サムネ文字**: `HE WAS` / **`ASHORE FIRST`** ／ 代案 `SIXTEEN` / **`YEARS`**

| # | 主題 |
|---|---|
| 01 | An enormous white cruise ship hull lying on its side in shallow water at night, blasted by hard white shore floodlights with visible flare, the horizon line kept dead level so the ship reads as wrong, filling most of the frame |
| 02 | A formal ship dining room tilted thirty degrees, chandeliers still blazing gold, glassware and chairs sliding across white cloth, warm light against deep blue shadow, no people |
| 03 | An orange lifeboat hanging uselessly sideways from its davit against a towering hull, a floodlight flaring behind it, the orange burning against black steel |
| 04 | A darkened ship's bridge with the whole instrument console alight in amber and green, an empty captain's chair turned away, black sea beyond the glass |
| 05 | The submerged flank of a white hull lit by hard diver lights from below, blue-green water, shafts of light rising through the murk |

# EP81 — ステーション・ナイトクラブ火災（2003） · slug `station_v2`

**不抗争の答弁。兄は4年服役、弟は1日も服役していません。火は絶対に出さないこと。**

**サムネ文字**: `NOT FIRE` / **`RETARDANT`** ／ 代案 `ONE SERVED` / **`FOUR YEARS`**

| # | 主題 |
|---|---|
| 01 | Close macro of grey wedge acoustic foam covering a low ceiling, lit from below by a blazing magenta and red stage light, one tile peeled back to bare plywood, dust burning in the beam |
| 02 | A small club stage in the dark with one hard white spotlight blazing straight into the lens, an empty microphone stand in silhouette, black foam wall behind |
| 03 | A green emergency exit pictogram blazing at the end of a narrow dark corridor, the green light flooding the walls, heavy flare, no words on the sign |
| 04 | A black stage monitor speaker washed in saturated red stage light, chrome grille catching a hot highlight, the empty room black behind |
| 05 | A wall of black acoustic foam raked by a single blue-white beam from the side, the texture blazing where the light hits and falling to black elsewhere |

# EP82 — エクソン・バルディーズ（1989） · slug `valdez_v2`

**陪審50億ドル → 控訴審25億ドル → 最高裁が約5億ドル（2008-06-25）。**
**「5時間の約束」は出典が無いので使わないこと。**

**サムネ文字**: `FIVE BILLION` / **`FIVE HUNDRED MILLION`** ／ 代案 `NINETEEN YEARS` / **`LATER`**

| # | 主題 |
|---|---|
| 01 | A gloved hand holding a single stone completely coated in glossy black oil under a hard cold-white work light, the oil catching an iridescent rainbow sheen, thick drips, black behind, no face |
| 02 | Rows of coiled orange containment boom in a dark warehouse blasted by a work floodlight, the orange burning saturated against blue shadow, snow drifted at the open door |
| 03 | A cobble shoreline at low sun, the upper half of every stone glossy black and the lower half clean, a burning orange sky band on the horizon, the tide line dead straight |
| 04 | A fishing harbour at dusk with sodium dock lights blazing and flaring, boats in silhouette, the water throwing the orange back |
| 05 | Macro of an oil sheen on a steel deck catching iridescent purple and green under a hard lamp, filling the frame, water beading |

# 【最優先・単独】EP35 hinders 作り直し · slug `hinders_v2`

**表示7,436回・CTR 1.00%。チャンネル最大の取りこぼし。** 文字は2ブロックに減らす。

**サムネ文字**: `NO CRIME` / **`NO CHARGE`**

| # | 主題 |
|---|---|
| 01 | An open steel cash drawer, completely empty, on a dark counter under a single hard overhead lamp flaring into the lens, the brushed metal blazing, deep shadow all around, no money and no papers |
| 02 | A green glass banker's lamp burning on a dark counter beside a stack of blank white envelopes, the green glow flooding the wood, everything else falling away |
| 03 | A closed roller shutter on a small shop front at night under a blazing sodium street lamp with a heavy starburst flare, wet pavement throwing the orange back, no signage |

---

# 納品後の手順

```
py -3.11 scripts/check_thumb_punch.py E:\pd-media\05_visuals\thumbs\keybridge_v2
```

1. **この検査を通ること。** 落ちたら光源が足りないか、暗すぎるか、色が無い
2. `py -3.11 scripts/thumb_feed_sheet.py` で **168×94 に縮小して見る**。
   **v001 は原寸で美しく、縮小すると意味が消えました**（端子台の隙間が見えなくなった）
3. オーナーが各話1枚選ぶ
4. Remotionで文字を**2ブロックだけ**乗せて 1280×720 書き出し
5. `check_packaging_claims.py` を通す（サムネの文字も検査対象）

# 正直に書いておくこと

- この帯域は**勝った2枚から作りました。n=2 です。** 「明るくて彩度が高いほど勝つ」ことの証明ではなく、
  **「今のPDで勝った2枚はそうだった」という事実**です
- 検査は**光と色しか見ません。意味は見ません。** 派手で何も言っていない絵は通ってしまいます。
  **縮小して人が見る工程を飛ばさないこと**
