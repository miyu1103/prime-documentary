# サムネ ヒーロープレート — EP77〜EP82 ＋ EP35再作成 **v004（再開版・全37枚）**

> **v003のテスト1枚（keybridge 01）は合格済み。この発注書は「v003の残り32枚＋EP77の
> CTR実験用追加5枚（06〜10）＝37枚」の生産指示です。**
> 経緯: v003はテスト方式（まず1枚→測定→残り）で、初号機が6回不合格になり32枚が保留された。
> その後、最良試行（gate02）に決定論的な色補正（明度+10%・コントラスト0.975）を当てたところ
> **5バンド全部PASS**した。受領書:
> `episodes/_planning/EP77-82_THUMB_CODEX.v003.unblock_receipt.json`
>
> **つまり: v003のスタイル指示は正しかった。生成が帯域の「近く」まで来れば、最後の数点は
> こちらのローカル補正（`scripts/thumb_autograde.py`）で仕上がる。** 帯域ど真ん中を6回
> 追いかけ回す必要はもうない。

保存先: `E:\pd-media\05_visuals\thumbs\<slug>_v3\`（既存ファイルは**絶対に上書きしない**。
keybridge_v3 には合格済み `THUMB-01.v002_graded.png` が既にある。keybridge は 02〜05 のみ作る）

---

## 0. 合格の実測レシピ（当てずっぽうではない）

合格した初号機の数値（補正後）と、その元になった生成（補正前）:

| | 明るさ | コントラスト | 明るい画素% | 暗い画素% | 彩度 |
|---|---|---|---|---|---|
| 生成そのまま（gate02） | 43.2 | 57.6 | 4.8 | 68.6 | 39.3 |
| ローカル補正後（合格） | 46.2 | **60.5** | 5.6 | 66.4 | 41.4 |
| 判定帯域 | 42〜78 | 60〜95 | 3〜16 | 35〜72 | 30〜85 |

**生成の狙い目: 明るさ45〜65 / コントラスト55以上 / 明るい画素5〜10%。**
コントラストだけ帯域を割っても、他4項目が帯内なら補正で仕上がる。
**明るい画素が3%未満の絵は補正でも救えない**（v1/v2の死因）。光源を大きく白飛びさせること。

## 1. 数値目標（`check_thumb_punch.py` がこの帯域で判定）

```
明るさ      42〜78
コントラスト 60〜95
明るい画素   3〜16 %   ← 狙いは 6〜10 %。3%は下限であって目標ではない
暗い画素    35〜72 %
彩度        30〜85
```

## 2. `[STYLE]` — 各主題の後ろに貼る（v003と同一・変更なし）

```
, the light source itself is IN the frame and is BLOWN OUT PURE WHITE, a large blazing
highlight filling at least a fifth of the picture with visible lens flare and light shafts,
the subject filling roughly half the picture and brightly lit, saturated colour, extreme
contrast between the blown highlight and one deep shadow side, ultra high resolution,
hyper-detailed, razor-sharp focus, photorealistic, volumetric light, 16:9 thumbnail hero shot,
scroll-stopping
```

## 3. `[NEG]` — 最後に貼る（v003と同一・変更なし）

```
Avoid: on-screen text, letters, numerals, readable documents, watermark, logo, identifiable
real person, faces, bodies, injuries, the moment of the accident, dim scene, dark room, night
interior with a small lamp, evenly dark image, flat lighting, low contrast, monochrome,
desaturated, muted colours, empty black frame, small distant subject, low-resolution.
```

**⛔ 二度と書かない語**: `deep black palette` / `vast empty dark negative space` /
`dark room` / `everything else falling to black`

**⛔ 文字は絵に入れない。** 各話の「文字:」行は後工程でローカル合成する文字案の控えであり、
生成プロンプトに含めてはならない（生成グリフは禁止。invariant 11）。

---

# EP77 — ボルチモア橋 · slug `keybridge_v3` — **02〜10の9枚**（01は合格済み・作らない）

文字（控え・合成は後工程）: `SIX MEN` / **`WERE UP THERE`**

| # | 主題 |
|---|---|
| 02 | A bright inspection lamp flaring directly into the lens beside an electrical terminal block, the polished metal and copper blazing white where the light hits, a blue wire stopping short of the clamp |
| 03 | A ship's engine-room alarm panel filling the whole frame with dozens of indicator lamps burning red and amber at full intensity, the panel glass blown out white at the centre |
| 04 | The rotating amber beacon of a works truck blazing directly into the lens at close range, blown out white at its core, a yellow hard hat lit hard beside it |
| 05 | A hard cyan-white floodlight blazing into the lens from the base of a bridge pier, a huge starburst flare, the concrete pier brilliantly lit and filling the right half |

## EP77 追加バリアント 06〜10（CTR実験用・新文法）

**06〜08はスケール対比（豆粒の人間 vs 巨大な物体）、09〜10は物体ミステリー。**
この5枚に限り `[NEG]` の "bodies" を次のとおり緩和する:
**遠景の完全なシルエット人物（画面高12〜22%・顔なし・後ろ姿または横姿・個人特定不可）は可。**
顔・クローズアップの人体・実在人物は引き続き禁止。

| # | 主題 |
|---|---|
| 06 | The colossal bow of a container ship towering out of night river mist, filling the top two-thirds of the frame, lit brilliantly from below by dock floodlights that flare into the lens, two tiny silhouetted workers in hi-vis standing far below on the quay, dwarfed to matchstick size |
| 07 | A vast brilliantly floodlit bridge deck at night stretching away to the horizon, one tiny silhouetted road worker beside a work light tower blazing blown-out white, the huge steel truss structure soaring overhead and filling the sky |
| 08 | A cavernous ship engine room, enormous generator machinery brilliantly lit in every direction and filling the whole frame like a cutaway diagram, one tiny silhouetted engineer on a high catwalk, a single work lamp blown out white at the centre |
| 09 | Extreme macro of a single blue signal wire hanging loose a few millimetres short of its terminal block clamp, a hard inspection light blazing behind it and blown out white, every strand of copper razor sharp, deep shadow on one side |
| 10 | A ship's massive main engine control lever on a brilliantly lit bridge console, pushed to full ahead, one amber alarm lamp beside it blazing and flared, the rest of the console lit hard in cyan-white |

# EP78 — コルガン航空3407便 · slug `colgan_v3` — 5枚

文字（控え）: `EIGHTEEN SECONDS` / **`NOBODY LOOKED`**

| # | 主題 |
|---|---|
| 01 | A cockpit instrument panel filling the frame, lit brilliant red, one display blown out pure white at its centre, the control column in the foreground blurred by violent vibration |
| 02 | An airport approach light bar firing sequenced strobes straight into the lens through heavy falling snow, the strobes blown out white, the snow blazing in the beams |
| 03 | A suburban house window burning brilliant gold and blown out white, filling the left half of the frame, deep blue snow outside |
| 04 | An aircraft airspeed dial filling the frame, glass catching a hard blown-out specular highlight, the instrument face lit brilliant red, needle low |
| 05 | A green emergency exit sign blazing at close range in a crew room, blown out white at its core, the whole wall flooded green |

# EP79 — アラスカ航空261便 · slug `alaska261_v3` — 5枚

文字（控え）: `FOUR EXTENSIONS` / **`APPROVED`**

| # | 主題 |
|---|---|
| 01 | A huge steel acme-threaded jackscrew filling the frame under a blazing inspection lamp that flares into the lens, the worn end catching a blown-out white highlight, threads sharp at the far end |
| 02 | A work lamp blazing directly into the lens in an aircraft hangar, blown out white, a grease gun lit hard in the foreground, the hangar floor brilliantly lit |
| 03 | A hangar bay door open at night with blue-white light flooding out and blowing out the frame, an aircraft tail silhouetted against the glare |
| 04 | A maintenance stand under an aircraft belly with a work lamp blasting upward into the structure, the panels blazing white where the beam lands |
| 05 | The Pacific at dusk with a brilliant orange sun band blown out white at its core across the horizon, the water throwing a hard specular path toward the camera |

# EP80 — コスタ・コンコルディア · slug `concordia_v3` — 5枚

文字（控え）: `HE WAS` / **`ASHORE FIRST`**

| # | 主題 |
|---|---|
| 01 | An enormous white cruise ship hull on its side blasted by shore floodlights that flare into the lens, the white paint blown out, filling two-thirds of the frame, horizon dead level |
| 02 | A ship's dining room tilted thirty degrees with chandeliers blazing gold and blown out white, glassware sliding, the room brilliantly lit, no people |
| 03 | An orange lifeboat hanging sideways from its davit with a floodlight blazing into the lens behind it, the orange burning saturated, the hull brilliantly lit |
| 04 | A ship's bridge console at night with every instrument alight in amber and green at full intensity, one lamp blown out white, an empty chair |
| 05 | A white hull underwater lit by hard diver lights that flare into the lens, the beams cutting bright shafts through blue-green water, the hull blazing where they land |

# EP81 — ステーション・ナイトクラブ火災 · slug `station_v3` — 5枚

**v2はここが5枚とも全滅した（主題が「暗い部屋」だった）。主題は照明そのもの。火は出さない。**

文字（控え）: `NOT FIRE` / **`RETARDANT`**

| # | 主題 |
|---|---|
| 01 | A cluster of stage par-can lights blazing magenta and red directly into the lens at close range, blown out white at their cores, grey acoustic foam ceiling tiles brilliantly lit above them, one tile peeled back |
| 02 | A single hard white followspot blasting straight into the lens from the back of a small club stage, huge flare, the empty stage and a microphone stand brilliantly rim-lit |
| 03 | A green emergency exit sign blazing at close range above a corridor, blown out white at its core, the corridor walls flooded brilliant green |
| 04 | A wall of black acoustic foam raked by a blazing white beam that fills the right half of the frame and flares into the lens, the foam texture blown out where the light lands |
| 05 | A mirror ball throwing hundreds of hard white light spots across a brightly lit ceiling of foam tiles, the ball itself blown out at its centre |

# EP82 — エクソン・バルディーズ · slug `valdez_v3` — 5枚

文字（控え）: `FIVE BILLION` / **`FIVE HUNDRED MILLION`**

| # | 主題 |
|---|---|
| 01 | A gloved hand holding a stone coated in glossy black oil under a blazing work lamp that flares into the lens, the oil throwing a brilliant iridescent specular sheen, the lamp blown out white |
| 02 | Coiled orange containment boom filling the frame under a floodlight blasting into the lens, the orange burning saturated and blown out where the beam lands |
| 03 | A cobble shoreline at low sun with a brilliant orange sun band blown out white on the horizon, the wet black upper halves of the stones throwing hard specular highlights |
| 04 | A fishing harbour at dusk with sodium dock lights blazing and flaring into the lens, blown out white at their cores, the water throwing the orange back brilliantly |
| 05 | Macro of an oil sheen on a steel deck catching a blown-out white specular highlight and brilliant iridescent purple and green, filling the frame |

# 【最優先】EP35 hinders 作り直し · slug `hinders_v3` — 3枚

文字（控え）: `NO CRIME` / **`NO CHARGE`**

| # | 主題 |
|---|---|
| 01 | An open empty steel cash drawer on a counter under a hard overhead lamp blazing into the lens, the brushed metal blown out white where the light lands, deep shadow on one side only |
| 02 | A green glass banker's lamp burning brilliantly at close range beside a stack of blank white envelopes, the lamp shade blown out, the counter flooded green |
| 03 | A closed shop shutter at night under a sodium street lamp blazing into the lens with a heavy starburst, the shutter brilliantly lit, wet pavement throwing the orange back |

---

# 手順（v003の「まず1枚」は完了済み → 話数フォルダ単位で回す）

```
1. 1フォルダ（1話ぶん）を生成するたびに測る:
   py -3.11 scripts/check_thumb_punch.py  E:\pd-media\05_visuals\thumbs\<slug>_v3
2. 落ちた枚のうち「コントラストだけ不足・明るい画素3%以上」のものは再生成しない。
   そのまま残す（ローカル補正 scripts/thumb_autograde.py で仕上げる。担当はClaude側）
3. 「明るい画素3%未満」「明るさ42未満」で落ちた枚だけ、光源を大きくして再生成する
4. 全納品後に必ず:
   py -3.11 scripts/thumb_feed_sheet.py  <フォルダ>   # 168×94で目視
```

**再生成の判断基準は「補正で救えるか」。救える絵に生成回数を使わないこと。**

# 正直に書くこと（v003から引き継ぎ）

- 帯域は**勝った2枚から作った。n=2。**「明るいほど勝つ」の証明ではない
- 検査は**光と色しか見ない。意味は見ない。** 派手で何も言っていない絵は通る
- 初号機の合格が32枚の合格を保証するわけではない。ただし v1(0/29合格)→v2(7/33)→
  v003初号機(補正込み合格)と、変更点1つずつで改善してきた実測がある
- 各話の「文字:」は生成に使わない控え。最終的なオンサムネ文字はタイトルとのペア設計
  （タイトルと同じことを言わない分業原則）で別途確定し、オーナー承認を経て合成する
