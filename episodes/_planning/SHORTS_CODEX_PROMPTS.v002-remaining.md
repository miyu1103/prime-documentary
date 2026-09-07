# Codex 縦型画像プロンプト v002-remaining

**682 枚** / 31 本のショート / 15 話ぶん。

## 出力の指定（全枚共通）

| | |
|---|---|
| サイズ | **1080 × 1920 ちょうど**（16:9で作って切るのは不可） |
| 形式 | PNG / sRGB |
| ファイル名 | 各プロンプトの見出しの名前をそのまま使ってください |
| ネガティブ | 全枚共通。下記 |

```
cartoon, anime, illustration, 3d render, cgi, plastic skin, waxy, deformed, extra fingers, bad hands, blurry, lowres, jpeg artifacts, oversaturated, text, watermark, signature
```

## 守ってほしいこと（全部、壊してから学んだものです）

- **native vertical** — Render 1080x1920. Never crop from 16:9 - a centre crop of a 16:9 frame keeps 31.6% of the width, and the first build of short82 lost the handcuffs, the benches and the bars that way.
- **quiet bands** — Keep y0-560 (persona mark + telop) and y1210-1430 (caption band) visually quiet. Subject sits y560-1180, or below y1450. Measured by drawing the real Shorts furniture over a rendered frame.
- **no readable text** — No lettering anywhere. Documents, signage, clock faces, book spines and plates are blank. EP01's library carried 'PRCRETY OBSCROVIL'; an archive clip carried a legible 'Lease Agreement'. Both are instant tells.
- **no likeness** — Silhouettes, backs, hands and objects only. No frontal faces. Real people in these cases are living or recently dead (CLAUDE.md invariant 11).
- **name the light** — Every prompt names ONE practical source and states it is switched on and is the only light in frame. Without this SD3.5 returns flat daylight - measured: 'empty interrogation room' came back as a bright minimalist interior with the lamp off.
- **exposure floor** — Target mean luma 45-70. short82 v001 averaged 29 with 64% of frames under 25 and was unreadable on a phone.

プロンプト本文には既にこれらが書き込んであります。**文言を削らずにそのまま渡してください。**

## 納品

- ファイル名は `short<NN>_<nn>.png`。この名前のまま返してください（`remotion/public/shorts/short<NN>/` にそのまま入ります）
- **ラベル付きコンタクトシート**を1バッチにつき1枚。目視選別に使います
- 1枚ずつの説明は不要です（下の `subject` が対応します）

---

## short182 — tlo
*時代設定：1980s New Jersey* / 22 枚

### `short182_01.png`  (hook / L1)
> a hand opening the bag on the desk

```
macro of one hand drawing open the zipper of a canvas school satchel lying on a scarred wooden office desk, no face or body visible, lit ONLY by one desk lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1980s New Jersey, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short182_02.png`  (hook / L1)
> the chair a student is questioned in

```
a single empty wooden chair standing in a cone of light on the near side of a bare administrator's desk in a dark school office, dust drifting through the beam, lit ONLY by the fixture switched on above it, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1980s New Jersey, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short182_03.png`  (hook / L1)
> the office lamp above the search

```
low angle looking up into a bare conical office lamp burning straight into camera above a wooden desk, heavy dust in the beam, the room beyond swallowed in black, lit ONLY by that lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1980s New Jersey, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short182_04.png`  (hook / L1)
> the room once the bag is open

```
a shaft of light crossing an empty school office thick with slowly drifting dust and nothing else in frame, lit ONLY by that shaft, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1980s New Jersey, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short182_05.png`  (body / L2)
> the court that wrote the test

```
tall marble courthouse columns photographed from directly below against a dark storm sky with no inscriptions anywhere, lit ONLY by hard uplights switched on at their bases, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1980s New Jersey, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short182_06.png`  (body / L2)
> the room where a purse was argued over

```
rows of empty polished wooden courtroom gallery benches receding into shadow, lit ONLY by one shaft of light from a high window, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1980s New Jersey, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short182_07.png`  (body / L2)
> the bench the case climbed to

```
a judge's high wooden bench photographed from the floor looking up, empty, lit ONLY by one shaft of window light falling across its face, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1980s New Jersey, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short182_08.png`  (body / L2)
> the case as a stack of paper

```
a leaning tower of worn case folders on a small desk with every label worn completely blank, lit ONLY by one desk lamp switched on beside it, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1980s New Jersey, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short182_09.png`  (body / L2)
> second period

```
a plain round institutional wall clock with a completely blank featureless face and no numerals mounted on a tiled school wall, lit ONLY by one fixture switched on beside it, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1980s New Jersey, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short182_10.png`  (body / L2)
> the rule, reduced to one page

```
one completely blank sheet of paper lying on a scuffed school corridor floor, lit ONLY by a hard shaft of corridor light falling across it, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1980s New Jersey, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short182_11.png`  (body / L2)
> the morning the rule was set

```
an office window at first light with a desk buried in blank folders silhouetted against it, lit ONLY by the pale dawn beyond the glass, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1980s New Jersey, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short182_12.png`  (body / L3)
> the restroom door swinging shut

```
a heavy school restroom door swinging shut on a narrowing blade of light seen from inside a dark tiled room, lit ONLY by that closing light, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1980s New Jersey, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short182_13.png`  (body / L3)
> the bag set down between them

```
macro of two hands laid flat on a scarred wooden desk on either side of a closed canvas bag, no face or body above the wrists, lit ONLY by one hard overhead lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1980s New Jersey, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short182_14.png`  (body / L3)
> the reasons an office collects

```
a metal in-tray overflowing with blank unreadable forms on a grey school office desk, lit ONLY by one fluorescent tube switched on above, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1980s New Jersey, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short182_15.png`  (body / L3)
> the walk from the restroom to the office

```
a long school corridor receding into darkness toward one brightly lit doorway at the far end, lit ONLY by that doorway, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1980s New Jersey, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short182_16.png`  (body / L3)
> a bank of lockers, all shut

```
a long school corridor lined with identical closed steel lockers with every nameplate worn blank, lit ONLY by a row of ceiling fixtures switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1980s New Jersey, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short182_17.png`  (body / L4)
> how far a search can reach

```
a wall of grey steel lockers and shelving packed with unlabelled bundles shot straight on, lit ONLY by one flickering fluorescent tube switched on overhead, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1980s New Jersey, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short182_18.png`  (body / L4)
> everything a bag is made to give up

```
looking down the aisle of a deep school storeroom with shelving stacked to the ceiling with unlabelled boxes, lit ONLY by one bulb switched on at the far end, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1980s New Jersey, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short182_19.png`  (body / L4)
> the contents laid out in a row

```
ordinary small personal objects laid out in a row across a dark wooden desk with every marking worn completely blank, lit ONLY by one desk lamp switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1980s New Jersey, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short182_20.png`  (body / L4)
> the file that followed her

```
a thin case file closed and tied with a band on a dark desk with its cover worn completely blank, lit ONLY by one desk lamp switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1980s New Jersey, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short182_21.png`  (body / L4)
> the finding, stamped

```
macro of a wooden-handled rubber stamp resting on an ink pad with the die face worn completely smooth and unreadable, lit ONLY by one desk lamp switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1980s New Jersey, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short182_22.png`  (body / L4)
> the rule that reached every school

```
a dark relief map of the United States showing state borders as thin glowing seams and absolutely no place names or lettering, lit ONLY by that internal glow, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1980s New Jersey, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

## short183 — tlo
*時代設定：1980s New Jersey* / 22 枚

### `short183_01.png`  (hook / L1)
> a patrol car at the school kerb

```
tight low angle on the front fender and single roof beacon of a police cruiser parked at a school kerb, chrome and dark paint filling frame, lit ONLY by that beacon which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1980s New Jersey, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short183_02.png`  (hook / L1)
> the car waiting outside the building

```
the interior of a parked patrol car seen from the passenger side with empty seats and a red wash crossing the dashboard from behind, lit ONLY by those beacons, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1980s New Jersey, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short183_03.png`  (hook / L1)
> an office door closing behind a student

```
a heavy school office door swinging shut on a narrowing blade of light seen from inside a dark room, lit ONLY by that closing light, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1980s New Jersey, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short183_04.png`  (hook / L1)
> the lamp over the desk where it happens

```
low angle looking up into a bare conical lamp burning straight into camera above a plain wooden desk, heavy dust in the beam, the room beyond swallowed in black, lit ONLY by that lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1980s New Jersey, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short183_05.png`  (body / L2)
> the educator's empty chair

```
a single empty wooden chair standing in a cone of light in a dark school office with a bare desk beyond it, dust motes drifting, lit ONLY by the fixture switched on above it, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1980s New Jersey, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short183_06.png`  (body / L2)
> a corridor of identical classroom doors

```
a long school corridor of identical closed classroom doors with all nameplates blank, lit ONLY by a row of ceiling fixtures switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1980s New Jersey, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short183_07.png`  (body / L2)
> the school day, measured out

```
a plain round institutional wall clock with a completely blank featureless face and no numerals above a corridor doorway, lit ONLY by one fixture switched on beside it, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1980s New Jersey, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short183_08.png`  (body / L2)
> the corridor toward the front office

```
a long institutional corridor receding into darkness toward one brightly lit doorway at the far end, lit ONLY by that doorway, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1980s New Jersey, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short183_09.png`  (body / L2)
> the everyday work of keeping order

```
a metal in-tray overflowing with blank unreadable forms on a grey desk, lit ONLY by one fluorescent tube switched on above, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1980s New Jersey, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short183_10.png`  (body / L2)
> the office before the bell

```
a school office window at first light with a desk buried in blank folders silhouetted against it, lit ONLY by the pale dawn beyond the glass, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1980s New Jersey, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short183_11.png`  (body / L2)
> discipline files, stacked

```
a leaning tower of worn school discipline folders on a small desk with every label worn completely blank, lit ONLY by one desk lamp switched on beside it, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1980s New Jersey, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short183_12.png`  (body / L3)
> the table police use instead

```
a bare metal table and two chairs under a single conical lamp hanging low in a tall bare room, lit ONLY by that lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1980s New Jersey, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short183_13.png`  (body / L3)
> the warrant an officer would need

```
macro of one hand pressing a pen to a completely blank unreadable sheet on a dark desk, no face or body visible, lit ONLY by a single desk lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1980s New Jersey, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short183_14.png`  (body / L3)
> the courthouse that signs them

```
tall marble courthouse columns photographed from directly below against a dark sky with no inscriptions anywhere, lit ONLY by hard uplights switched on at their bases, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1980s New Jersey, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short183_15.png`  (body / L3)
> the bench a warrant has to pass

```
a judge's high wooden bench photographed from the floor looking up, empty, lit ONLY by one shaft of window light falling across its face, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1980s New Jersey, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short183_16.png`  (body / L3)
> the space between the two standards

```
a shaft of light crossing an empty room thick with slowly drifting dust, nothing else in frame, lit ONLY by that shaft, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1980s New Jersey, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short183_17.png`  (body / L4)
> three justices in the minority

```
rows of empty polished wooden courtroom gallery benches receding into shadow with three seats in the front row catching the light, lit ONLY by one shaft from a high window, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1980s New Jersey, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short183_18.png`  (body / L4)
> the student with the least power to push back

```
a lone dark silhouette standing in a single vertical shaft of light in a vast dark hall, the figure placed HIGH in frame with its head in the upper third and a long empty floor below it, face not visible, lit ONLY by that shaft, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1980s New Jersey, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short183_19.png`  (body / L4)
> the record of every search

```
looking down the aisle of a deep records room with shelving stacked to the ceiling with unlabelled boxes, lit ONLY by one bulb switched on at the far end, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1980s New Jersey, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short183_20.png`  (body / L4)
> the dissent, filed and closed

```
a thick case file closed and tied with a band on a dark desk with its cover worn completely blank, lit ONLY by one desk lamp switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1980s New Jersey, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short183_21.png`  (body / L4)
> one rule, every state

```
a dark relief map of the United States showing state borders as thin glowing seams and absolutely no place names, lit ONLY by that internal glow, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1980s New Jersey, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short183_22.png`  (body / L4)
> the standard, filed away

```
a wall of grey steel filing shelves packed with unlabelled folders shot straight on, lit ONLY by one flickering fluorescent tube switched on overhead, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1980s New Jersey, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

## short184 — atwater
*時代設定：1997 Texas* / 22 枚

### `short184_01.png`  (hook / L1)
> the cuffs closing at the roadside

```
macro of steel handcuffs closing on a pair of wrists held behind a back, no face or body above the forearms, lit ONLY by one hard raking afternoon sun, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1997 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short184_02.png`  (hook / L1)
> the cab of the pickup, belts loose

```
the interior of a parked pickup truck seen from the passenger side with an empty bench seat and an unbuckled lap belt hanging loose across the upholstery, lit ONLY by hard afternoon sun through the windscreen, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1997 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short184_03.png`  (hook / L1)
> the patrol car that pulled in behind

```
tight low angle on the front fender and single roof beacon of a patrol car parked on the shoulder of a two lane road, chrome and dark paint filling frame, lit ONLY by that beacon which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1997 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short184_04.png`  (hook / L1)
> the cell door closing on an hour

```
a heavy steel door swinging shut on a narrowing blade of light seen from inside a dark holding cell, lit ONLY by that closing light, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1997 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short184_05.png`  (body / L2)
> the penalty the statute set

```
one completely blank sheet of paper lying on a scuffed municipal floor, lit ONLY by a hard shaft of corridor light falling across it, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1997 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short184_06.png`  (body / L2)
> fifty dollars

```
a small fan of banknotes lying on a dark counter with every denomination and marking illegible, lit ONLY by one lamp switched on above the counter, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1997 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short184_07.png`  (body / L2)
> what a seatbelt ticket became

```
a leaning tower of worn traffic folders on a small steel desk with every label worn completely blank, lit ONLY by one desk lamp switched on beside it, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1997 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short184_08.png`  (body / L2)
> the fine, stamped and paid

```
macro of a wooden-handled rubber stamp resting on an ink pad with the die face worn completely smooth and unreadable, lit ONLY by one desk lamp switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1997 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short184_09.png`  (body / L2)
> the hour she sat there

```
a plain round institutional wall clock with a completely blank featureless face and no numerals on a painted block wall, lit ONLY by one fixture switched on beside it, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1997 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short184_10.png`  (body / L2)
> one state's traffic law

```
a dark relief map of the United States showing state borders as thin glowing seams and absolutely no place names, lit ONLY by that internal glow, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1997 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short184_11.png`  (body / L2)
> the courthouse where the fine was entered

```
tall stone courthouse columns photographed from directly below against a dark sky with no inscriptions anywhere, lit ONLY by hard uplights switched on at their bases, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1997 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short184_12.png`  (body / L3)
> the road at first light

```
a two lane road running out to a flat horizon at first light with a wire fence in the foreground, lit ONLY by the pale dawn beyond, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1997 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short184_13.png`  (body / L3)
> dust on the shoulder after they left

```
a shaft of low sun crossing an empty stretch of roadside gravel thick with slowly drifting dust, lit ONLY by that shaft, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1997 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short184_14.png`  (body / L3)
> the ticket book he did not reach for

```
a closed ticket book lying face down on a patrol car bonnet with its cover worn completely blank, lit ONLY by one hard low sun, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1997 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short184_15.png`  (body / L3)
> the corridor at the station

```
a long station corridor receding into darkness toward one brightly lit doorway at the far end, lit ONLY by that doorway, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1997 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short184_16.png`  (body / L3)
> hands flat on the booking counter

```
macro of two hands laid flat on a scarred booking counter, no face or body above the wrists, lit ONLY by one hard overhead lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1997 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short184_17.png`  (body / L4)
> everything she was carrying

```
a steel booking tray holding a belt, a set of keys and a few coins on a counter, lit ONLY by one hard overhead lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1997 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short184_18.png`  (body / L4)
> one chair in a municipal room

```
a single empty chair standing in a cone of light in a bare municipal room, dust motes drifting, lit ONLY by the fixture switched on above it, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1997 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short184_19.png`  (body / L4)
> the holding cell itself

```
the interior of a bare holding cell with a small high barred window throwing one hard shaft onto the concrete floor, lit ONLY by that window, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1997 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short184_20.png`  (body / L4)
> the corridor of identical doors

```
a long municipal corridor of identical closed doors with all nameplates blank, lit ONLY by a row of ceiling fixtures switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1997 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short184_21.png`  (body / L4)
> the bond that let her out

```
macro of one hand pressing a pen to a completely blank unreadable sheet on a counter, no face or body visible, lit ONLY by a single desk lamp switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1997 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short184_22.png`  (body / L4)
> the seat the children were lifted out of

```
one empty child seat in the cab of a parked truck with a small jacket still over its back, everything around it in shadow, lit ONLY by a single low sun through the side glass, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1997 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

## short185 — atwater
*時代設定：2001 America* / 22 枚

### `short185_01.png`  (hook / L1)
> the line that now runs along a border

```
a dark relief map of the United States showing state borders as thin glowing seams and absolutely no place names or lettering, lit ONLY by that internal glow, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2001 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short185_02.png`  (hook / L1)
> the chamber the remedy was handed to

```
an empty tiered committee chamber with rows of vacant seats and a long bench, all nameplates blank, lit ONLY by one bank of overhead lights switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2001 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short185_03.png`  (hook / L1)
> the court that declined to draw it

```
tall marble courthouse columns photographed from directly below against a dark storm sky with no inscriptions anywhere, lit ONLY by hard uplights switched on at their bases, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2001 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short185_04.png`  (hook / L1)
> a door closing on the remedy

```
a heavy panelled door swinging shut on a narrowing blade of light seen from inside a dark room, lit ONLY by that closing light, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2001 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short185_05.png`  (body / L2)
> the roadside the rule is applied on

```
the interior of a parked car seen from the passenger side with empty seats and a red and blue wash crossing the dashboard from behind, lit ONLY by those beacons, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2001 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short185_06.png`  (body / L2)
> the beacon behind the driver

```
tight low angle on the front fender and single roof beacon of a patrol car parked at a kerb, chrome and dark paint filling frame, lit ONLY by that beacon which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2001 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short185_07.png`  (body / L2)
> the corridor a case travels

```
a long institutional corridor receding into darkness toward one brightly lit doorway at the far end, lit ONLY by that doorway, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2001 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short185_08.png`  (body / L2)
> the split second at the window

```
a plain round institutional wall clock with a completely blank featureless face and no numerals, hard side light, lit ONLY by one fixture switched on beside it, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2001 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short185_09.png`  (body / L2)
> the bench that set the rule

```
a judge's high wooden bench photographed from the floor looking up, empty, lit ONLY by one shaft of window light falling across its face, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2001 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short185_10.png`  (body / L2)
> hands on a table in dissent

```
macro of two weathered hands laid flat on a scarred wooden table, no face or body above the wrists, lit ONLY by one hard overhead lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2001 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short185_11.png`  (body / L2)
> four votes, not five

```
rows of empty polished wooden courtroom gallery benches receding into shadow, lit ONLY by one shaft of light from a high window, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2001 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short185_12.png`  (body / L3)
> the room where the balance was weighed

```
a shaft of light crossing an empty panelled room thick with slowly drifting dust, nothing else in frame, lit ONLY by that shaft, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2001 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short185_13.png`  (body / L3)
> the lamp over a late decision

```
low angle looking up into a bare conical lamp burning straight into camera through drifting dust, the room beyond swallowed in black, lit ONLY by that lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2001 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short185_14.png`  (body / L3)
> the seat the dissent spoke from

```
a single empty wooden chair standing in a cone of light in a large dark empty chamber, dust motes drifting, lit ONLY by the fixture switched on above it, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2001 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short185_15.png`  (body / L3)
> the bills that pile up in a session

```
a metal in-tray overflowing with blank unreadable forms on a grey desk, lit ONLY by one fluorescent tube switched on above, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2001 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short185_16.png`  (body / L3)
> the corridor outside the chamber

```
a long government corridor of identical closed doors with all nameplates blank, lit ONLY by a row of ceiling fixtures switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2001 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short185_17.png`  (body / L4)
> a statute being signed

```
macro of one hand pressing a pen to a completely blank unreadable sheet, no face or body visible, lit ONLY by a single desk lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2001 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short185_18.png`  (body / L4)
> the statutes, stacked by state

```
a leaning tower of worn statute folders on a small desk with every label worn completely blank, lit ONLY by one desk lamp switched on beside it, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2001 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short185_19.png`  (body / L4)
> the law, enacted

```
macro of a wooden-handled rubber stamp resting on an ink pad with the die face worn completely smooth and unreadable, lit ONLY by one desk lamp switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2001 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short185_20.png`  (body / L4)
> fifty different answers, shelved

```
looking down the aisle of a deep records room with shelving stacked to the ceiling with unlabelled boxes, lit ONLY by one bulb switched on at the far end, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2001 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short185_21.png`  (body / L4)
> a desk before the session opens

```
an office window at first light with a desk buried in blank folders silhouetted against it, lit ONLY by the pale dawn beyond the glass, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2001 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short185_22.png`  (body / L4)
> the case, closed and shelved

```
a thick case file closed and tied with a band on a dark desk with its cover worn completely blank, lit ONLY by one desk lamp switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2001 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

## short186 — willingham
*時代設定：1991 Texas* / 22 枚

### `short186_01.png`  (hook / L1)
> the pooled scorch on a bare floor

```
one dark irregular pooled scorch mark on bare charred floorboards in an empty gutted room, lit ONLY by a hard shaft of daylight through the doorway, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1991 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short186_02.png`  (hook / L1)
> ash in the light of the burned room

```
a shaft of daylight crossing an empty fire-gutted room thick with slowly drifting ash and nothing else in frame, lit ONLY by that shaft, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1991 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short186_03.png`  (hook / L1)
> one chair left standing in the char

```
a single scorched wooden chair standing in a cone of daylight in a large dark burned-out room, ash drifting around it, lit ONLY by that daylight, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1991 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short186_04.png`  (hook / L1)
> hands held over the char

```
macro of two gloved hands held flat just above charred floorboards, no face or body above the wrists, lit ONLY by one hard work lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1991 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short186_05.png`  (body / L2)
> the bench where fire evidence is read

```
a laboratory bench holding a heavy analytical instrument with all displays dark and unreadable, lit ONLY by one task lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1991 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short186_06.png`  (body / L2)
> a sealed sample can from the scene

```
a sealed steel evidence can standing on a steel counter with all writing worn completely blank, lit ONLY by one hard overhead lamp switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1991 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short186_07.png`  (body / L2)
> twenty indicators, filed

```
a leaning tower of worn case folders on a small steel desk with every label worn completely blank, lit ONLY by one desk lamp switched on beside it, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1991 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short186_08.png`  (body / L2)
> the room the fire was explained in

```
rows of empty polished wooden courtroom benches receding into shadow, lit ONLY by one shaft of light from a high window, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1991 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short186_09.png`  (body / L2)
> the bench the testimony was given to

```
a judge's high wooden bench photographed from the floor looking up, empty, lit ONLY by one shaft of window light falling across its face, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1991 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short186_10.png`  (body / L2)
> the morning of the fire

```
a plain round wall clock with a completely blank featureless face and no numerals hanging on a smoke-stained wall, lit ONLY by one fixture switched on beside it, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1991 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short186_11.png`  (body / L2)
> the hallway of the little frame house

```
a short narrow house hallway with smoke damage on the walls receding toward one brightly lit open doorway, lit ONLY by that doorway, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1991 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short186_12.png`  (body / L3)
> the heat gathering at the ceiling

```
low angle looking up into a bare ceiling fixture burning straight into camera through heavy smoke, the room beyond swallowed in black, lit ONLY by that fixture which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1991 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short186_13.png`  (body / L3)
> a door shutting inside a filling room

```
an interior door swinging shut on a narrowing blade of light seen from inside a smoke-filled dark room, lit ONLY by that closing light, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1991 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short186_14.png`  (body / L3)
> smoke against the window glass

```
a small house window at first light with smoke pressed against the inside of the glass, lit ONLY by the pale dawn beyond, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1991 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short186_15.png`  (body / L3)
> the closed room, everything in it

```
a plain domestic room with furniture pushed back to the walls under a low ceiling, everything coated in soot, lit ONLY by one bare bulb switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1991 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short186_16.png`  (body / L3)
> the house sealed after the fire

```
a heavy scorched door secured with a chain and padlock in a dim burned corridor with all notices worn blank, lit ONLY by one work lamp switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1991 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short186_17.png`  (body / L4)
> one blackened nail in the wood

```
macro of one blackened nail standing in charred wood on a dark surface, lit ONLY by a single hard rim light, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1991 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short186_18.png`  (body / L4)
> the shelves that burned with the house

```
a wall of scorched steel shelving packed with unlabelled ruined boxes shot straight on, lit ONLY by one work lamp switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1991 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short186_19.png`  (body / L4)
> where the file was kept

```
looking down the aisle of a deep records room with shelving stacked to the ceiling with unlabelled boxes, lit ONLY by one bulb switched on at the far end, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1991 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short186_20.png`  (body / L4)
> an investigator in the burned doorway

```
a lone dark silhouette standing in a single vertical shaft of daylight in a burned-out room, the figure placed HIGH in frame with its head in the upper third and a long empty floor below it, face not visible, lit ONLY by that shaft, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1991 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short186_21.png`  (body / L4)
> the reading that spread across the country

```
a dark relief map of the United States showing state borders as thin glowing seams and absolutely no place names, lit ONLY by that internal glow, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1991 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short186_22.png`  (body / L4)
> the file closed on the fire

```
a thick case file closed and tied with a band on a dark desk with its cover worn completely blank, lit ONLY by one desk lamp switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1991 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

## short187 — willingham
*時代設定：2009 Texas* / 22 枚

### `short187_01.png`  (hook / L1)
> the chamber the meeting was set for

```
an empty tiered committee chamber with rows of vacant seats and a long bench, all nameplates blank, lit ONLY by one bank of overhead lights switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2009 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short187_02.png`  (hook / L1)
> the chairman's seat, vacated

```
a single empty upholstered chair standing in a cone of light behind a long committee bench in a dark chamber, lit ONLY by the fixture switched on above it, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2009 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short187_03.png`  (hook / L1)
> the table set for a meeting that did not happen

```
a long polished conference table with chairs pushed in and a dark blank wall behind it, nobody present, lit ONLY by one pendant switched on above the table, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2009 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short187_04.png`  (hook / L1)
> two days before

```
a plain round institutional wall clock with a completely blank featureless face and no numerals on a panelled wall, lit ONLY by one fixture switched on beside it, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2009 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short187_05.png`  (body / L2)
> the science the commission existed to test

```
a laboratory bench holding a heavy analytical instrument with all displays dark and unreadable, lit ONLY by one task lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2009 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short187_06.png`  (body / L2)
> the review, in folders

```
a leaning tower of worn review folders on a small desk with every label worn completely blank, lit ONLY by one desk lamp switched on beside it, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2009 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short187_07.png`  (body / L2)
> the work that arrives at a commission

```
a metal in-tray overflowing with blank unreadable forms on a grey government desk, lit ONLY by one fluorescent tube switched on above, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2009 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short187_08.png`  (body / L2)
> the office before the hearing

```
an office window at first light with a desk buried in blank folders silhouetted against it, lit ONLY by the pale dawn beyond the glass, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2009 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short187_09.png`  (body / L2)
> the original investigation, stored

```
looking down the aisle of a deep records room with shelving stacked to the ceiling with unlabelled boxes, lit ONLY by one bulb switched on at the far end, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2009 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short187_10.png`  (body / L2)
> the corridor to the hearing room

```
a long government corridor receding into darkness toward one brightly lit doorway at the far end, lit ONLY by that doorway, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2009 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short187_11.png`  (body / L2)
> the offices along that corridor

```
a long government corridor of identical closed doors with all nameplates blank, lit ONLY by a row of ceiling fixtures switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2009 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short187_12.png`  (body / L3)
> the report, written out

```
macro of one hand pressing a pen to a completely blank unreadable sheet on a dark desk, no face or body visible, lit ONLY by a single desk lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2009 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short187_13.png`  (body / L3)
> one page of the finding

```
one completely blank sheet of paper lying on a scuffed institutional floor, lit ONLY by a hard shaft of corridor light falling across it, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2009 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short187_14.png`  (body / L3)
> hands on the table where it was read

```
macro of two hands laid flat on a long polished committee table, no face or body above the wrists, lit ONLY by one hard overhead lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2009 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short187_15.png`  (body / L3)
> the state's own paper on the case

```
a wall of grey steel filing shelves packed with unlabelled folders shot straight on, lit ONLY by one flickering fluorescent tube switched on overhead, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2009 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short187_16.png`  (body / L3)
> the report, bound and closed

```
a thick bound report closed and tied with a band on a dark desk with its cover worn completely blank, lit ONLY by one desk lamp switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2009 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short187_17.png`  (body / L4)
> the lamp left burning in the chamber

```
low angle looking up into a bare conical lamp burning straight into camera through drifting dust, the room beyond swallowed in black, lit ONLY by that lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2009 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short187_18.png`  (body / L4)
> the room after the meeting was called off

```
a shaft of light crossing an empty panelled chamber thick with slowly drifting dust, nothing else in frame, lit ONLY by that shaft, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2009 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short187_19.png`  (body / L4)
> the courts that never reopened it

```
tall stone courthouse columns photographed from directly below against a dark storm sky with no inscriptions anywhere, lit ONLY by hard uplights switched on at their bases, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2009 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short187_20.png`  (body / L4)
> the bench that has not ruled

```
a judge's high wooden bench photographed from the floor looking up, empty, lit ONLY by one shaft of window light falling across its face, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2009 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short187_21.png`  (body / L4)
> the conviction, still stamped

```
macro of a wooden-handled rubber stamp resting on an ink pad with the die face worn completely smooth and unreadable, lit ONLY by one desk lamp switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2009 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short187_22.png`  (body / L4)
> one state, one unanswered question

```
a dark relief map of the United States showing state borders as thin glowing seams and absolutely no place names, lit ONLY by that internal glow, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2009 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

## short188 — morton
*時代設定：1986 Texas* / 22 枚

### `short188_01.png`  (hook / L1)
> the instrument that produced the estimate

```
a laboratory bench holding a heavy analytical instrument with all displays dark and unreadable, lit ONLY by one task lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1986 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short188_02.png`  (hook / L1)
> six in the morning

```
a plain round kitchen wall clock with a completely blank featureless face and no numerals, lit ONLY by one fixture switched on beside it, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1986 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short188_03.png`  (hook / L1)
> hands flat on a bare table

```
macro of two weathered hands laid flat on a scarred wooden kitchen table, no face or body above the wrists, lit ONLY by one hard overhead lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1986 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short188_04.png`  (hook / L1)
> the lamp over the estimate

```
low angle looking up into a bare conical lamp burning straight into camera through drifting dust, the room beyond swallowed in black, lit ONLY by that lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1986 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short188_05.png`  (body / L2)
> the kitchen window before dawn

```
a kitchen window at first light with a plain table and two chairs silhouetted against it, lit ONLY by the pale dawn beyond the glass, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1986 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short188_06.png`  (body / L2)
> the car he left in

```
the interior of a parked sedan seen from the passenger side with empty seats and one hard streetlight wash across the dashboard, lit ONLY by that streetlight which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1986 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short188_07.png`  (body / L2)
> the front door closing behind him

```
a residential front door swinging shut on a narrowing blade of porch light seen from inside a dark hallway, lit ONLY by that closing light, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1986 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short188_08.png`  (body / L2)
> the back corridor of the store

```
a long service corridor of identical closed doors with all nameplates blank, lit ONLY by a row of ceiling fixtures switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1986 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short188_09.png`  (body / L2)
> the stockroom before opening

```
a long stockroom aisle receding into darkness toward one brightly lit doorway at the far end, lit ONLY by that doorway, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1986 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short188_10.png`  (body / L2)
> the shift, on paper

```
a leaning tower of worn work folders on a small desk with every label worn completely blank, lit ONLY by one desk lamp switched on beside it, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1986 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short188_11.png`  (body / L2)
> the clock he punched

```
macro of a wall-mounted punch clock with a completely blank unreadable card slot and a worn steel face, lit ONLY by one bare bulb switched on beside it, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1986 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short188_12.png`  (body / L3)
> the house once everyone had gone

```
a shaft of light crossing an empty domestic room thick with slowly drifting dust, nothing else in frame, lit ONLY by that shaft, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1986 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short188_13.png`  (body / L3)
> the chair pulled back from the table

```
a single empty wooden chair standing in a cone of light in a dark family kitchen, dust motes drifting, lit ONLY by the fixture switched on above it, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1986 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short188_14.png`  (body / L3)
> two chairs turned toward each other

```
two plain chairs turned to face each other across a bare floor in a small dim room, nobody in them, lit ONLY by one window shaft, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1986 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short188_15.png`  (body / L3)
> one figure in a shaft of light

```
a lone dark silhouette standing in a single vertical shaft of light in a vast dark room, the figure placed HIGH in frame with its head in the upper third and a long empty floor below it, face not visible, lit ONLY by that shaft, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1986 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short188_16.png`  (body / L3)
> the theory, written down

```
macro of one hand pressing a pen to a completely blank unreadable sheet on a dark desk, no face or body visible, lit ONLY by a single desk lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1986 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short188_17.png`  (body / L4)
> an evidence envelope, sealed and blank

```
a sealed paper evidence envelope on a steel counter with all writing worn completely blank, lit ONLY by one hard overhead lamp switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1986 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short188_18.png`  (body / L4)
> the shelves the case sat on

```
a wall of grey steel filing shelves packed with unlabelled folders shot straight on, lit ONLY by one flickering fluorescent tube switched on overhead, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1986 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short188_19.png`  (body / L4)
> the sheriff's own file room

```
looking down the aisle of a deep records room with shelving stacked to the ceiling with unlabelled boxes, lit ONLY by one bulb switched on at the far end, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1986 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short188_20.png`  (body / L4)
> the case, closed on him

```
a thick case file closed and tied with a band on a dark desk with its cover worn completely blank, lit ONLY by one desk lamp switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1986 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short188_21.png`  (body / L4)
> the arrest, on one blank page

```
one completely blank sheet of paper lying on a scuffed institutional floor, lit ONLY by a hard shaft of corridor light falling across it, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1986 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short188_22.png`  (body / L4)
> one county in one state

```
a dark relief map of the United States showing state borders as thin glowing seams and absolutely no place names, lit ONLY by that internal glow, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1986 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

## short189 — morton
*時代設定：2011 Texas* / 22 枚

### `short189_01.png`  (hook / L1)
> the evidence room door, closed

```
a heavy steel evidence room door closed in a dim corridor with its dial and markings worn smooth and unreadable, lit ONLY by one hard uplight switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2011 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short189_02.png`  (hook / L1)
> what a chain keeps shut

```
a heavy door secured with a chain and padlock in a dim service corridor with all notices worn blank, lit ONLY by one caged bulb switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2011 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short189_03.png`  (hook / L1)
> the cloth in its sealed envelope

```
a sealed paper evidence envelope lying on a steel counter with all writing worn completely blank, lit ONLY by one hard overhead lamp switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2011 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short189_04.png`  (hook / L1)
> six years, measured out

```
a plain round institutional wall clock with a completely blank featureless face and no numerals, hard side light, lit ONLY by one fixture switched on beside it, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2011 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short189_05.png`  (body / L2)
> the aisle it sat in

```
looking down the aisle of a deep evidence store with shelving stacked to the ceiling with unlabelled boxes, lit ONLY by one bulb switched on at the far end, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2011 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short189_06.png`  (body / L2)
> a wall of untested cases

```
a wall of grey steel filing shelves packed with unlabelled folders shot straight on, lit ONLY by one flickering fluorescent tube switched on overhead, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2011 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short189_07.png`  (body / L2)
> the case, in folders

```
a leaning tower of worn case folders on a small steel desk with every label worn completely blank, lit ONLY by one desk lamp switched on beside it, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2011 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short189_08.png`  (body / L2)
> one drawer among the closed ones

```
one empty steel evidence drawer pulled out from a wall of closed ones, lit ONLY by a single overhead fixture switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2011 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short189_09.png`  (body / L2)
> the locker room, undisturbed

```
a shaft of light crossing an empty storage room thick with slowly drifting dust, nothing else in frame, lit ONLY by that shaft, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2011 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short189_10.png`  (body / L2)
> one page of the request

```
one completely blank sheet of paper lying on a scuffed institutional floor, lit ONLY by a hard shaft of corridor light falling across it, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2011 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short189_11.png`  (body / L2)
> the desk the motions were written at

```
an office window at first light with a desk buried in blank folders silhouetted against it, lit ONLY by the pale dawn beyond the glass, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2011 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short189_12.png`  (body / L3)
> a motion, filed again

```
macro of one hand pressing a pen to a completely blank unreadable sheet on a dark desk, no face or body visible, lit ONLY by a single desk lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2011 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short189_13.png`  (body / L3)
> hands on a table across years

```
macro of two weathered hands laid flat on a scarred wooden table, no face or body above the wrists, lit ONLY by one hard overhead lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2011 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short189_14.png`  (body / L3)
> the seat kept for a client

```
a single empty wooden chair standing in a cone of light in a large dark empty room, dust motes drifting, lit ONLY by the fixture switched on above it, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2011 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short189_15.png`  (body / L3)
> the corridor between filings

```
a long institutional corridor receding into darkness toward one brightly lit doorway at the far end, lit ONLY by that doorway, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2011 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short189_16.png`  (body / L3)
> the offices that said no

```
a long county office corridor of identical closed doors with all nameplates blank, lit ONLY by a row of ceiling fixtures switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2011 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short189_17.png`  (body / L4)
> the courthouse the fight ran through

```
tall stone courthouse columns photographed from directly below against a dark storm sky with no inscriptions anywhere, lit ONLY by hard uplights switched on at their bases, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2011 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short189_18.png`  (body / L4)
> the bench that finally ordered it

```
a judge's high wooden bench photographed from the floor looking up, empty, lit ONLY by one shaft of window light falling across its face, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2011 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short189_19.png`  (body / L4)
> the room the order was read in

```
rows of empty polished wooden courtroom gallery benches receding into shadow, lit ONLY by one shaft of light from a high window, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2011 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short189_20.png`  (body / L4)
> each objection, stamped

```
macro of a wooden-handled rubber stamp resting on an ink pad with the die face worn completely smooth and unreadable, lit ONLY by one desk lamp switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2011 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short189_21.png`  (body / L4)
> the file that would not open

```
a thick case file closed and tied with a band on a dark desk with its cover worn completely blank, lit ONLY by one desk lamp switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2011 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short189_22.png`  (body / L4)
> the bench that would read it

```
a forensic laboratory bench with a heavy analytical instrument, all displays dark and unreadable, lit ONLY by one task lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2011 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

## short190 — carsearch
*時代設定：1925 America* / 22 枚

### `short190_01.png`  (hook / L1)
> a patrol car's single beacon at the kerb

```
tight low angle on the front fender and single roof beacon of a police cruiser stopped at a kerb, chrome and dark paint filling the frame, lit ONLY by that beacon which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1925 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short190_02.png`  (hook / L1)
> the empty interior of a stopped car

```
the interior of a parked car seen from the passenger side with the seats empty and a hard wash of light crossing the dashboard from behind, lit ONLY by that wash of light, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1925 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short190_03.png`  (hook / L1)
> hands laid flat on the roof of a car

```
macro of two weathered hands laid flat on the cold roof of a car with nothing visible above the wrists, lit ONLY by one hard raking lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1925 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short190_04.png`  (hook / L1)
> the courthouse that wrote the rule

```
tall marble courthouse columns photographed from directly below against a dark storm sky with no inscriptions anywhere, lit ONLY by hard uplights switched on at their bases, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1925 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short190_05.png`  (body / L2)
> a front door held shut from inside

```
a residential front door seen from inside a dark hallway with a security chain across it and one hard blade of light beneath it, lit ONLY by that light, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1925 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short190_06.png`  (body / L2)
> the door that does not move

```
a heavy panelled house door swinging shut on a narrowing blade of light seen from inside a dark room, lit ONLY by that closing light, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1925 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short190_07.png`  (body / L2)
> how long a house can be made to wait

```
a plain round wall clock with a completely blank featureless face and no numerals hanging above a dark porch, lit ONLY by one fixture switched on beside it, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1925 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short190_08.png`  (body / L2)
> a chair set by a door for a long wait

```
a single empty wooden chair standing in a cone of light on a bare porch beside a shut door, lit ONLY by the fixture switched on above it, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1925 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short190_09.png`  (body / L2)
> a house window from night into first light

```
a house window at first light with the sill and curtain silhouetted against it, lit ONLY by the pale dawn beyond the glass, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1925 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short190_10.png`  (body / L2)
> the still air of a house nobody entered

```
a shaft of light crossing an empty hallway thick with slowly drifting dust and nothing else in frame, lit ONLY by that shaft, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1925 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short190_11.png`  (body / L2)
> the warrant that has to be signed first

```
macro of one hand pressing a pen to a completely blank unreadable sheet on a dark desk, no face or body visible, lit ONLY by a single desk lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1925 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short190_12.png`  (body / L3)
> the road out of the county

```
a long empty two-lane road receding into darkness toward one bright pool of light at the far end, lit ONLY by that pool of light, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1925 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short190_13.png`  (body / L3)
> the county line a car can cross

```
a dark relief map of the United States showing state borders as thin glowing seams and absolutely no place names or lettering, lit ONLY by that internal glow which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1925 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short190_14.png`  (body / L3)
> the signature that arrives too late

```
a wooden judge's gavel caught mid-strike above its round block with motion blur on the head, lit ONLY by one brass bench lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1925 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short190_15.png`  (body / L3)
> the paperwork a warrant takes

```
a leaning tower of worn folders on a small desk with every label worn completely blank, lit ONLY by one desk lamp switched on beside it, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1925 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short190_16.png`  (body / L3)
> the kerb where the car used to be

```
heavy doors swinging open onto blinding daylight and an empty kerb beyond, seen from inside a dark room, lit ONLY by that daylight, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1925 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short190_17.png`  (body / L4)
> the bench that set the standard

```
a judge's high wooden bench photographed from the floor looking up, empty, lit ONLY by one shaft of window light falling across its face, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1925 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short190_18.png`  (body / L4)
> the room the rule came out of

```
rows of empty polished wooden courtroom gallery benches receding into shadow, lit ONLY by one shaft of light from a high window, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1925 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short190_19.png`  (body / L4)
> the shelf of decisions behind it

```
a wall of grey steel filing shelves packed with unlabelled folders shot straight on, lit ONLY by one flickering fluorescent tube switched on overhead, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1925 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short190_20.png`  (body / L4)
> one driver alone under the rule

```
a lone dark figure standing in a single vertical shaft of light in a vast dark hall, placed high in the frame with a long empty floor below and the face not visible, lit ONLY by that shaft, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1925 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short190_21.png`  (body / L4)
> the small thing they might be hunting

```
macro of one small brass object standing alone on a dark surface, lit ONLY by a single hard rim light which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1925 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short190_22.png`  (body / L4)
> the trunk lid, closed

```
the closed rear lid of a dark car photographed straight on in a bare chamber with all badges and markings worn smooth and unreadable, lit ONLY by one hard uplight switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1925 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

## short191 — carsearch
*時代設定：present-day America* / 22 枚

### `short191_01.png`  (hook / L1)
> handcuffs closing at a roadside

```
macro of steel handcuffs closing on a pair of wrists with no face or body visible above the forearms and a car fender out of focus behind, lit ONLY by one hard raking light which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, present-day America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short191_02.png`  (hook / L1)
> the car left shut while the arrest happens

```
the interior of a parked car seen through the passenger window with the doors closed and the seats empty and a red wash crossing the dashboard from behind, lit ONLY by those beacons which are switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, present-day America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short191_03.png`  (hook / L1)
> the kerb they sit you on

```
a single empty folding chair standing in a cone of light on a bare stretch of kerb in the dark, lit ONLY by the fixture switched on above it, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, present-day America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short191_04.png`  (hook / L1)
> the tray your pockets go into

```
a steel booking tray holding a belt, laces and a few coins on a counter, lit ONLY by one hard overhead lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, present-day America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short191_05.png`  (body / L2)
> the bench that narrowed the rule

```
a judge's high wooden bench photographed from the floor looking up, empty, lit ONLY by one shaft of window light falling across its face, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, present-day America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short191_06.png`  (body / L2)
> the case the rule came from

```
a leaning tower of worn case folders on a small desk with every label worn completely blank, lit ONLY by one desk lamp switched on beside it, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, present-day America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short191_07.png`  (body / L2)
> the lamp over the question

```
low angle looking up into a bare conical lamp burning straight into camera through heavy smoke with the room beyond swallowed in black, lit ONLY by that lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, present-day America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short191_08.png`  (body / L2)
> the table where the offense is named

```
a bare metal table and two chairs under a single conical lamp hanging low in a tall bare room, lit ONLY by that lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, present-day America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short191_09.png`  (body / L2)
> how long the car stays shut

```
a plain round institutional wall clock with a completely blank featureless face and no numerals, hard side light, lit ONLY by one fixture switched on beside it, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, present-day America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short191_10.png`  (body / L2)
> the sealed envelope nobody opens

```
a sealed paper envelope lying on a steel counter with all writing worn completely blank, lit ONLY by one hard overhead lamp switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, present-day America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short191_11.png`  (body / L2)
> a door that stays closed

```
a heavy steel door closed in a dark chamber with its dial and markings worn smooth and unreadable, lit ONLY by one hard uplight switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, present-day America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short191_12.png`  (body / L3)
> a hand over a blank rental form

```
macro of one hand resting flat on a completely blank unreadable form on a counter, no face or body visible, lit ONLY by a single desk lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, present-day America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short191_13.png`  (body / L3)
> a phone face down on the passenger seat

```
a smartphone lying face down on a dark car seat with its edge catching one hard light and the screen not visible, lit ONLY by a single overhead lamp switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, present-day America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short191_14.png`  (body / L3)
> a car door closing on a blade of light

```
a car door swinging shut on a narrowing blade of light seen from inside the dark cabin, lit ONLY by that closing light, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, present-day America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short191_15.png`  (body / L3)
> the counter where the keys change hands

```
a long empty rental counter with a dark board behind it and nobody present and all panels blank, lit ONLY by one pendant switched on above the counter, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, present-day America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short191_16.png`  (body / L3)
> hands on a steering wheel

```
macro of two hands resting on the rim of a steering wheel with no face or body visible above the wrists, lit ONLY by one hard lamp switched on outside the windscreen, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, present-day America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short191_17.png`  (body / L4)
> the tray of forms nobody reads

```
a metal in-tray overflowing with blank unreadable forms on a grey desk, lit ONLY by one fluorescent tube switched on above, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, present-day America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short191_18.png`  (body / L4)
> the wall of files behind the counter

```
a wall of grey steel filing shelves packed with unlabelled folders shot straight on, lit ONLY by one flickering fluorescent tube switched on overhead, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, present-day America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short191_19.png`  (body / L4)
> the stamp on the agreement

```
macro of a wooden-handled rubber stamp resting on an ink pad with the die face worn completely smooth and unreadable, lit ONLY by one desk lamp switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, present-day America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short191_20.png`  (body / L4)
> two seats, one name on the paper

```
two plain chairs turned to face each other across a bare floor in a small dim room with nobody in them, lit ONLY by one window shaft, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, present-day America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short191_21.png`  (body / L4)
> one driver among a lot of cars

```
a lone dark figure standing in a single vertical shaft of light in a vast dark parking structure, placed high in the frame with a long empty floor below and the face not visible, lit ONLY by that shaft, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, present-day America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short191_22.png`  (body / L4)
> the court that said so

```
tall marble courthouse columns photographed from directly below against a dark storm sky with no inscriptions anywhere, lit ONLY by hard uplights switched on at their bases, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, present-day America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

## short192 — tyler
*時代設定：medieval England* / 22 枚

### `short192_01.png`  (hook / L1)
> the modern file closed, the old law opened

```
a thick bound volume closed and tied with a leather band on a dark oak table with its cover worn completely blank, lit ONLY by one candle which is switched on beside it, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, medieval England, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short192_02.png`  (hook / L1)
> a hand over a blank sheet of parchment

```
macro of one hand pressing a quill to a completely blank unreadable sheet of parchment, no face or body visible, lit ONLY by a single candle which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, medieval England, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short192_03.png`  (hook / L1)
> stone columns of an old hall

```
tall weathered stone columns photographed from directly below against a dark storm sky with no inscriptions anywhere, lit ONLY by hard torches switched on at their bases, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, medieval England, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short192_04.png`  (hook / L1)
> one flame burning into camera

```
low angle looking up into a single burning lantern flame through heavy smoke with the hall beyond swallowed in black, lit ONLY by that lantern which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, medieval England, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short192_05.png`  (body / L2)
> the chest emptied down to the debt

```
one open wooden strongbox pulled out from a row of closed ones against a stone wall with the interior part filled and unreadable, lit ONLY by a single lantern switched on above, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, medieval England, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short192_06.png`  (body / L2)
> coin counted out on a plank table

```
stacks of dull coins on a rough plank table with the faces worn illegible, lit ONLY by one candle which is switched on beside them, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, medieval England, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short192_07.png`  (body / L2)
> hands flat on a plank table

```
macro of two weathered hands laid flat on a scarred plank table with no face or body above the wrists, lit ONLY by one hanging lantern which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, medieval England, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short192_08.png`  (body / L2)
> an iron-bound door, closed

```
a heavy iron-bound door closed in a dark stone chamber with all markings worn smooth and unreadable, lit ONLY by one torch switched on beside it, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, medieval England, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short192_09.png`  (body / L2)
> an empty chair in a stone hall

```
a single empty carved wooden chair standing in a cone of light in a vast dark stone hall with dust drifting, lit ONLY by the lantern switched on above it, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, medieval England, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short192_10.png`  (body / L2)
> one coin standing on edge

```
macro of one worn coin standing on edge on a dark surface with its face illegible, lit ONLY by a single hard rim light which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, medieval England, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short192_11.png`  (body / L2)
> dust in a stone room

```
a shaft of light crossing an empty stone room thick with slowly drifting dust and nothing else in frame, lit ONLY by that shaft, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, medieval England, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short192_12.png`  (body / L3)
> the seal pressed into wax

```
macro of a metal seal matrix resting on a pool of dark wax with the die face worn completely smooth and unreadable, lit ONLY by one candle switched on beside it, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, medieval England, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short192_13.png`  (body / L3)
> a narrow window at first light over a writing desk

```
a narrow stone window at first light with a writing desk of blank parchment silhouetted against it, lit ONLY by the pale dawn beyond the glass, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, medieval England, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short192_14.png`  (body / L3)
> a riverbank at last light

```
a slow riverbank at last light with reeds and driftwood in the foreground, lit ONLY by the last light on the water, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, medieval England, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short192_15.png`  (body / L3)
> a stone corridor to a lit doorway

```
a long stone corridor receding into darkness toward one brightly lit doorway at the far end, lit ONLY by that doorway, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, medieval England, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short192_16.png`  (body / L3)
> a blank-faced clock in a hall

```
a plain round hall clock with a completely blank featureless face and no numerals, hard side light, lit ONLY by one lantern switched on beside it, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, medieval England, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short192_17.png`  (body / L4)
> the residue set aside on the table

```
a small heap of coins and a folded cloth set apart on a dark plank table with every marking worn completely blank, lit ONLY by one candle switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, medieval England, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short192_18.png`  (body / L4)
> a wooden mallet mid-strike

```
a wooden mallet caught mid-strike above a worn block with motion blur on the head, lit ONLY by one lantern which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, medieval England, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short192_19.png`  (body / L4)
> an aisle of chests and boxes

```
looking down the aisle of a deep stone store room with shelving stacked to the ceiling with unlabelled chests, lit ONLY by one lantern switched on at the far end, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, medieval England, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short192_20.png`  (body / L4)
> one figure in a shaft of light

```
a lone dark figure standing in a single vertical shaft of light in a vast dark stone hall, placed high in the frame with a long empty floor below and the face not visible, lit ONLY by that shaft, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, medieval England, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short192_21.png`  (body / L4)
> a heavy door closing on light

```
a heavy studded door swinging shut on a narrowing blade of light seen from inside a dark stone room, lit ONLY by that closing light, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, medieval England, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short192_22.png`  (body / L4)
> doors opening onto daylight

```
heavy studded doors swinging open onto blinding daylight seen from inside a dark stone hall, lit ONLY by that daylight beyond, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, medieval England, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

## short193 — tyler
*時代設定：2020 Minneapolis* / 22 枚

### `short193_01.png`  (hook / L1)
> a hand over a blank statement

```
macro of one hand resting a pen on a completely blank unreadable statement on a kitchen table, no face or body visible, lit ONLY by a single desk lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2020 Minneapolis, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short193_02.png`  (hook / L1)
> a kitchen window at first light

```
a kitchen window at first light with a table of blank unopened envelopes silhouetted against it, lit ONLY by the pale dawn beyond the glass, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2020 Minneapolis, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short193_03.png`  (hook / L1)
> unopened mail behind a shut front door

```
a residential front door seen from inside a dark hallway with unopened envelopes piled on the mat and one hard blade of light under the door, lit ONLY by that light, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2020 Minneapolis, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short193_04.png`  (hook / L1)
> a used car under one lamp

```
the front quarter of an ordinary used sedan parked in a dark lot with its paint dulled and every badge worn smooth, lit ONLY by one overhead lamp switched on above it, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2020 Minneapolis, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short193_05.png`  (body / L2)
> the stamp that adds a charge

```
macro of a wooden-handled rubber stamp resting on an ink pad with the die face worn completely smooth and unreadable, lit ONLY by one desk lamp switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2020 Minneapolis, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short193_06.png`  (body / L2)
> the tray the notices land in

```
a metal in-tray overflowing with blank unreadable notices on a grey municipal desk, lit ONLY by one fluorescent tube switched on above, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2020 Minneapolis, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short193_07.png`  (body / L2)
> the file thickening on a desk

```
a leaning tower of worn folders on a small desk with every label worn completely blank, lit ONLY by one desk lamp switched on beside it, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2020 Minneapolis, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short193_08.png`  (body / L2)
> month after month on a blank clock

```
a plain round institutional wall clock with a completely blank featureless face and no numerals, hard side light, lit ONLY by one fixture switched on beside it, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2020 Minneapolis, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short193_09.png`  (body / L2)
> the debt counted in banded notes

```
banded stacks of currency on a dark desk with the denominations illegible, lit ONLY by one green banker's lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2020 Minneapolis, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short193_10.png`  (body / L2)
> the wall of county files

```
a wall of grey steel filing shelves packed with unlabelled folders shot straight on, lit ONLY by one flickering fluorescent tube switched on overhead, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2020 Minneapolis, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short193_11.png`  (body / L2)
> the corridor the file travels

```
a long municipal corridor of identical closed doors with all nameplates blank, lit ONLY by a row of ceiling fixtures switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2020 Minneapolis, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short193_12.png`  (body / L3)
> a line on dark glass that only rises

```
a single pale line rising smoothly across dark glass with no dips, abstract and unlabelled and no numerals anywhere, lit ONLY by its own glow which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2020 Minneapolis, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short193_13.png`  (body / L3)
> statements fanned out, all blank

```
printed statements fanned across a dark desk with every figure and heading worn completely blank, lit ONLY by one desk lamp switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2020 Minneapolis, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short193_14.png`  (body / L3)
> hands flat on a kitchen table

```
macro of two weathered hands laid flat on a scarred kitchen table with no face or body above the wrists, lit ONLY by one hard overhead lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2020 Minneapolis, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short193_15.png`  (body / L3)
> pages of a calendar caught mid-turn

```
a stack of wall calendar pages caught mid-turn with all dates worn blank and unreadable, lit ONLY by one angled desk lamp switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2020 Minneapolis, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short193_16.png`  (body / L3)
> dust in the room she left

```
a shaft of light crossing an empty one-bedroom living room thick with slowly drifting dust and nothing else in frame, lit ONLY by that shaft, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2020 Minneapolis, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short193_17.png`  (body / L4)
> a single empty chair in the condo

```
a single empty upholstered chair standing in a cone of light in an otherwise dark and empty apartment, lit ONLY by the fixture switched on above it, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2020 Minneapolis, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short193_18.png`  (body / L4)
> a coat still on the hook

```
one coat still hanging on a hook by a dark door with everything around it in shadow, lit ONLY by a single overhead reading light switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2020 Minneapolis, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short193_19.png`  (body / L4)
> a door closing on a blade of light

```
an apartment door swinging shut on a narrowing blade of light seen from inside a dark room, lit ONLY by that closing light, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2020 Minneapolis, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short193_20.png`  (body / L4)
> the unit sealed with a padlock

```
a residential storage door secured with a chain and padlock in a dim corridor with all notices worn blank, lit ONLY by one caged bulb switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2020 Minneapolis, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short193_21.png`  (body / L4)
> a bank of closed steel boxes

```
a wall of closed steel deposit boxes in a dark chamber with all dials and markings worn smooth and unreadable, lit ONLY by one hard uplight switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2020 Minneapolis, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short193_22.png`  (body / L4)
> one figure in a municipal hall

```
a lone dark figure standing in a single vertical shaft of light in a vast dark municipal hall, placed high in the frame with a long empty floor below and the face not visible, lit ONLY by that shaft, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2020 Minneapolis, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

## short194 — rolin
*時代設定：2020 America* / 22 枚

### `short194_01.png`  (hook / L1)
> banded cash on a metal table

```
banded stacks of currency laid out on a bare metal table with the denominations illegible, lit ONLY by one hard overhead lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2020 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short194_02.png`  (hook / L1)
> the table where it was counted

```
a bare steel table and two chairs under a single conical lamp hanging low in a tall bare room, lit ONLY by that lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2020 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short194_03.png`  (hook / L1)
> a sealed evidence envelope

```
a sealed paper evidence envelope on a steel counter with all writing worn completely blank, lit ONLY by one hard overhead lamp switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2020 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short194_04.png`  (hook / L1)
> a hand over a blank form

```
macro of one hand pressing a pen to a completely blank unreadable form on a counter, no face or body visible, lit ONLY by a single desk lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2020 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short194_05.png`  (body / L2)
> the courtroom where the money is the defendant

```
rows of empty polished wooden courtroom gallery benches receding into shadow, lit ONLY by one shaft of light from a high window, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2020 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short194_06.png`  (body / L2)
> the bench above an empty room

```
a judge's high wooden bench photographed from the floor looking up, empty, lit ONLY by one shaft of window light falling across its face, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2020 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short194_07.png`  (body / L2)
> the docket stack

```
a leaning tower of worn case folders on a small desk with every label worn completely blank, lit ONLY by one desk lamp switched on beside it, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2020 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short194_08.png`  (body / L2)
> the chair the owner would have sat in

```
a single empty wooden chair standing in a cone of light in a large dark empty courtroom, lit ONLY by the fixture switched on above it, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2020 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short194_09.png`  (body / L2)
> the docket stamp

```
macro of a wooden-handled rubber stamp resting on an ink pad with the die face worn completely smooth and unreadable, lit ONLY by one desk lamp switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2020 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short194_10.png`  (body / L2)
> a blank clock over the hearing

```
a plain round institutional wall clock with a completely blank featureless face and no numerals, hard side light, lit ONLY by one fixture switched on beside it, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2020 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short194_11.png`  (body / L2)
> dust in an empty court

```
a shaft of light crossing an empty wood-panelled room thick with slowly drifting dust and nothing else in frame, lit ONLY by that shaft, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2020 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short194_12.png`  (body / L3)
> a booking tray of ordinary things

```
a steel booking tray holding a belt, laces and a few coins on a counter, lit ONLY by one hard overhead lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2020 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short194_13.png`  (body / L3)
> an empty room where nobody was named

```
an empty lineup room with a bare marked wall and a height strip worn blank, lit ONLY by one harsh fixture switched on above, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2020 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short194_14.png`  (body / L3)
> one traveller alone in a hall

```
a lone dark figure standing in a single vertical shaft of light in a vast dark terminal hall, placed high in the frame with a long empty floor below and the face not visible, lit ONLY by that shaft, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2020 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short194_15.png`  (body / L3)
> hands flat on a counter

```
macro of two hands laid flat on a scuffed counter with no face or body above the wrists, lit ONLY by one hard overhead lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2020 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short194_16.png`  (body / L3)
> two chairs in a small side room

```
two plain chairs turned to face each other across a bare floor in a small dim room with nobody in them, lit ONLY by one window shaft, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2020 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short194_17.png`  (body / L4)
> the chamber that wrote the act

```
an empty tiered committee chamber with rows of vacant seats and a long bench with all nameplates blank, lit ONLY by one bank of overhead lights switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2020 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short194_18.png`  (body / L4)
> printed pages, every figure blank

```
printed pages fanned across a dark desk with every figure and heading worn completely blank, lit ONLY by one desk lamp switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2020 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short194_19.png`  (body / L4)
> the filing wall of the statute

```
a wall of grey steel filing shelves packed with unlabelled folders shot straight on, lit ONLY by one flickering fluorescent tube switched on overhead, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2020 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short194_20.png`  (body / L4)
> a gavel mid-strike

```
a wooden judge's gavel caught mid-strike above its round block with motion blur on the head, lit ONLY by one brass bench lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2020 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short194_21.png`  (body / L4)
> a lamp burning into camera

```
low angle looking up into a bare conical lamp burning straight into camera through heavy smoke with the room beyond swallowed in black, lit ONLY by that lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2020 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short194_22.png`  (body / L4)
> a closed vault door

```
a heavy steel vault door closed in a dark chamber with dial and markings worn smooth and unreadable, lit ONLY by one hard uplight switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2020 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

## short195 — rolin
*時代設定：2019 America* / 22 枚

### `short195_01.png`  (hook / L1)
> an aisle of seizure records

```
looking down the aisle of a deep federal records room with shelving stacked to the ceiling with unlabelled boxes, lit ONLY by one bulb switched on at the far end, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2019 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short195_02.png`  (hook / L1)
> a tower of case folders

```
a leaning tower of worn case folders on a grey steel desk with every label worn completely blank, lit ONLY by one desk lamp switched on beside it, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2019 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short195_03.png`  (hook / L1)
> banded notes filling a counter

```
banded stacks of currency filling a dark steel counter with the denominations illegible, lit ONLY by one hard overhead lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2019 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short195_04.png`  (hook / L1)
> a lamp burning into camera over the count

```
low angle looking up into a bare conical lamp burning straight into camera through heavy smoke with the room beyond swallowed in black, lit ONLY by that lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2019 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short195_05.png`  (body / L2)
> a wall of unlabelled files

```
a wall of grey steel filing shelves packed with unlabelled folders shot straight on, lit ONLY by one flickering fluorescent tube switched on overhead, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2019 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short195_06.png`  (body / L2)
> one sealed envelope among many

```
a row of sealed paper evidence envelopes on a steel counter with all writing worn completely blank, lit ONLY by one hard overhead lamp switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2019 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short195_07.png`  (body / L2)
> an in-tray of blank forms

```
a metal in-tray overflowing with blank unreadable forms on a grey desk, lit ONLY by one fluorescent tube switched on above, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2019 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short195_08.png`  (body / L2)
> the stamp that opens a case

```
macro of a wooden-handled rubber stamp resting on an ink pad with the die face worn completely smooth and unreadable, lit ONLY by one desk lamp switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2019 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short195_09.png`  (body / L2)
> one drawer of many pulled open

```
one empty steel drawer pulled out from a wall of closed ones, lit ONLY by a single overhead fixture switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2019 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short195_10.png`  (body / L2)
> a decade on a blank clock

```
a plain round institutional wall clock with a completely blank featureless face and no numerals, hard side light, lit ONLY by one fixture switched on beside it, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2019 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short195_11.png`  (body / L2)
> report pages, every figure blank

```
printed report pages fanned across a dark desk with every figure and heading worn completely blank, lit ONLY by one desk lamp switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2019 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short195_12.png`  (body / L3)
> a terminal corridor to a lit gate

```
a long airport corridor receding into darkness toward one brightly lit gate at the far end, lit ONLY by that gate, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2019 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short195_13.png`  (body / L3)
> one empty seat at a gate

```
a single empty moulded gate seat standing in a cone of light in a large dark departure hall, lit ONLY by the fixture switched on above it, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2019 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short195_14.png`  (body / L3)
> a boarding card face down

```
a folded card lying face down on a dark counter with its edge catching one hard light and nothing readable visible, lit ONLY by a single overhead lamp switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2019 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short195_15.png`  (body / L3)
> hands flat on a screening table

```
macro of two hands laid flat on a stainless screening table with no face or body above the wrists, lit ONLY by one hard overhead lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2019 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short195_16.png`  (body / L3)
> years of dates worn blank

```
a stack of wall calendar pages caught mid-turn with all dates worn blank and unreadable, lit ONLY by one angled desk lamp switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2019 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short195_17.png`  (body / L4)
> one traveller in a vast hall

```
a lone dark figure standing in a single vertical shaft of light in a vast dark terminal, placed high in the frame with a long empty floor below and the face not visible, lit ONLY by that shaft, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2019 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short195_18.png`  (body / L4)
> a seat with a coat still on it

```
one empty gate seat with a dark coat still hanging over its back and everything around it in shadow, lit ONLY by a single overhead reading light switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2019 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short195_19.png`  (body / L4)
> a line on dark glass that only rises

```
a single pale line rising smoothly across dark glass with no dips, abstract and unlabelled and no numerals anywhere, lit ONLY by its own glow which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2019 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short195_20.png`  (body / L4)
> dust in the light of a shut terminal

```
a shaft of light crossing an empty terminal concourse thick with slowly drifting dust and nothing else in frame, lit ONLY by that shaft, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2019 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short195_21.png`  (body / L4)
> a tray of a traveller's things

```
a grey screening tray holding a belt, a watch and a few coins on a stainless counter, lit ONLY by one hard overhead lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2019 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short195_22.png`  (body / L4)
> a locked steel door behind the checkpoint

```
a heavy steel door closed in a dark service corridor with its dial and markings worn smooth and unreadable, lit ONLY by one hard uplight switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2019 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

## short196 — hinders
*時代設定：2015 rural North Carolina* / 22 枚

### `short196_01.png`  (hook / L1)
> two chairs facing each other

```
two plain wooden chairs turned to face each other across a bare floor in a small dim room with nobody in them, lit ONLY by one window shaft, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2015 rural North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short196_02.png`  (hook / L1)
> two case folders side by side

```
two worn case folders laid side by side on a scarred desk with every label worn completely blank, lit ONLY by one desk lamp switched on beside them, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2015 rural North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short196_03.png`  (hook / L1)
> a gavel mid-strike

```
a wooden judge's gavel caught mid-strike above its round block with motion blur on the head, lit ONLY by one brass bench lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2015 rural North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short196_04.png`  (hook / L1)
> a lamp burning into camera

```
low angle looking up into a bare conical lamp burning straight into camera through heavy smoke with the room beyond swallowed in black, lit ONLY by that lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2015 rural North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short196_05.png`  (body / L2)
> a water tower over a country crossroads

```
an industrial water tower against a pale dawn sky with no lettering on the tank, lit ONLY by that dawn, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2015 rural North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short196_06.png`  (body / L2)
> a store's front door at first light

```
the glass front door of a small country store seen from inside a dark interior with all sign panels worn blank and one hard blade of light beneath it, lit ONLY by that light, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2015 rural North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short196_07.png`  (body / L2)
> the day's takings on a counter

```
banded stacks of small currency on a worn store counter with the denominations illegible, lit ONLY by one bulb which is switched on above the register, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2015 rural North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short196_08.png`  (body / L2)
> a register drawer standing open

```
an open steel register drawer pulled proud of a worn store counter with its compartments part filled and the notes illegible, lit ONLY by one bulb switched on above it, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2015 rural North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short196_09.png`  (body / L2)
> a store window at first light

```
a store window at first light with a counter of blank cartons silhouetted against it, lit ONLY by the pale dawn beyond the glass, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2015 rural North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short196_10.png`  (body / L2)
> a blank clock over the register

```
a plain round wall clock with a completely blank featureless face and no numerals hanging above a store counter, lit ONLY by one fixture switched on beside it, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2015 rural North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short196_11.png`  (body / L2)
> a store safe, closed

```
a small heavy steel safe closed in a dark back room with its dial and markings worn smooth and unreadable, lit ONLY by one hard uplight switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2015 rural North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short196_12.png`  (body / L3)
> deposit slips fanned across a desk

```
small paper slips fanned across a dark desk with every figure and heading worn completely blank, lit ONLY by one desk lamp switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2015 rural North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short196_13.png`  (body / L3)
> a line on dark glass that only rises

```
a single pale line rising smoothly across dark glass with no dips, abstract and unlabelled and no numerals anywhere, lit ONLY by its own glow which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2015 rural North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short196_14.png`  (body / L3)
> hands flat on a store counter

```
macro of two weathered hands laid flat on a scarred store counter with no face or body above the wrists, lit ONLY by one hard overhead lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2015 rural North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short196_15.png`  (body / L3)
> three years of dates worn blank

```
a stack of wall calendar pages caught mid-turn with all dates worn blank and unreadable, lit ONLY by one angled desk lamp switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2015 rural North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short196_16.png`  (body / L3)
> the bank's wall of files

```
a wall of grey steel filing shelves packed with unlabelled folders shot straight on, lit ONLY by one flickering fluorescent tube switched on overhead, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2015 rural North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short196_17.png`  (body / L4)
> a stool behind an empty counter

```
a single empty stool standing in a cone of light behind a bare store counter in an otherwise dark room, lit ONLY by the fixture switched on above it, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2015 rural North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short196_18.png`  (body / L4)
> one coin standing on the counter

```
macro of one worn coin standing on edge on a dark counter with its face illegible, lit ONLY by a single hard rim light which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2015 rural North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short196_19.png`  (body / L4)
> dust in a closed store

```
a shaft of light crossing an empty store aisle thick with slowly drifting dust and nothing else in frame, lit ONLY by that shaft, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2015 rural North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short196_20.png`  (body / L4)
> the stamp on the seizure order

```
macro of a wooden-handled rubber stamp resting on an ink pad with the die face worn completely smooth and unreadable, lit ONLY by one desk lamp switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2015 rural North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short196_21.png`  (body / L4)
> one owner alone in a hall

```
a lone dark figure standing in a single vertical shaft of light in a vast dark hall, placed high in the frame with a long empty floor below and the face not visible, lit ONLY by that shaft, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2015 rural North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short196_22.png`  (body / L4)
> a store door chained shut

```
a shop door secured with a chain and padlock in a dim covered walkway with all notices worn blank, lit ONLY by one caged bulb switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2015 rural North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

## short197 — hinders
*時代設定：2015 America* / 22 枚

### `short197_01.png`  (hook / L1)
> an aisle of pulled files

```
looking down the aisle of a deep records room with shelving stacked to the ceiling with unlabelled boxes and one box pulled out, lit ONLY by one bulb switched on at the far end, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2015 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short197_02.png`  (hook / L1)
> a tower of case folders on a desk

```
a leaning tower of worn case folders on a grey steel desk with every label worn completely blank, lit ONLY by one desk lamp switched on beside it, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2015 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short197_03.png`  (hook / L1)
> a report's pages, every figure blank

```
printed report pages fanned across a dark desk with every figure and heading worn completely blank, lit ONLY by one desk lamp switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2015 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short197_04.png`  (hook / L1)
> a lamp burning into camera over the desk

```
low angle looking up into a bare conical lamp burning straight into camera through heavy smoke with the room beyond swallowed in black, lit ONLY by that lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2015 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short197_05.png`  (body / L2)
> a wall of unlabelled folders

```
a wall of grey steel filing shelves packed with unlabelled folders shot straight on, lit ONLY by one flickering fluorescent tube switched on overhead, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2015 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short197_06.png`  (body / L2)
> an in-tray overflowing

```
a metal in-tray overflowing with blank unreadable forms on a grey desk, lit ONLY by one fluorescent tube switched on above, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2015 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short197_07.png`  (body / L2)
> banded notes on a dark desk

```
banded stacks of currency on a dark desk with the denominations illegible, lit ONLY by one green banker's lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2015 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short197_08.png`  (body / L2)
> one drawer pulled from a wall of them

```
one empty steel drawer pulled out from a wall of closed ones, lit ONLY by a single overhead fixture switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2015 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short197_09.png`  (body / L2)
> a line on dark glass that only rises

```
a single pale line rising smoothly across dark glass with no dips, abstract and unlabelled and no numerals anywhere, lit ONLY by its own glow which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2015 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short197_10.png`  (body / L2)
> a blank clock over the audit

```
a plain round institutional wall clock with a completely blank featureless face and no numerals, hard side light, lit ONLY by one fixture switched on beside it, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2015 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short197_11.png`  (body / L2)
> the stamp on each file

```
macro of a wooden-handled rubber stamp resting on an ink pad with the die face worn completely smooth and unreadable, lit ONLY by one desk lamp switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2015 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short197_12.png`  (body / L3)
> an empty diner counter

```
a long empty diner counter with stools pushed in and a dark back wall and nobody present, lit ONLY by one pendant switched on above the counter, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2015 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short197_13.png`  (body / L3)
> a shop window at first light

```
a small shop window at first light with a counter of blank cartons silhouetted against it, lit ONLY by the pale dawn beyond the glass, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2015 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short197_14.png`  (body / L3)
> hands flat on a diner counter

```
macro of two weathered hands laid flat on a scarred diner counter with no face or body above the wrists, lit ONLY by one hard overhead lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2015 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short197_15.png`  (body / L3)
> a single stool in a cone of light

```
a single empty stool standing in a cone of light in a large dark empty room, lit ONLY by the fixture switched on above it, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2015 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short197_16.png`  (body / L3)
> dust in a closed kitchen

```
a shaft of light crossing an empty commercial kitchen thick with slowly drifting dust and nothing else in frame, lit ONLY by that shaft, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2015 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short197_17.png`  (body / L4)
> a room where nobody was identified

```
an empty lineup room with a bare marked wall and a height strip worn blank, lit ONLY by one harsh fixture switched on above, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2015 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short197_18.png`  (body / L4)
> a sealed envelope on a counter

```
a sealed paper evidence envelope on a steel counter with all writing worn completely blank, lit ONLY by one hard overhead lamp switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2015 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short197_19.png`  (body / L4)
> one owner alone in a hall

```
a lone dark figure standing in a single vertical shaft of light in a vast dark hall, placed high in the frame with a long empty floor below and the face not visible, lit ONLY by that shaft, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2015 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short197_20.png`  (body / L4)
> a bank vault door, closed

```
a heavy steel vault door closed in a dark chamber with dial and markings worn smooth and unreadable, lit ONLY by one hard uplight switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2015 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short197_21.png`  (body / L4)
> a door closing on a blade of light

```
a heavy door swinging shut on a narrowing blade of light seen from inside a dark room, lit ONLY by that closing light, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2015 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short197_22.png`  (body / L4)
> years of dates worn blank

```
a stack of wall calendar pages caught mid-turn with all dates worn blank and unreadable, lit ONLY by one angled desk lamp switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, no face or likeness visible, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2015 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

## short200 — norfolk
*時代設定：1997 Norfolk Virginia* / 22 枚

### `short200_01.png`  (hook / L1)
> a bare interrogation lamp burning into camera

```
a low angle looking straight up into a bare conical interrogation lamp burning into the camera through drifting smoke, the room beyond swallowed in black, lit only by that lamp which is switched on, vertical 9:16 cinematic film still, 1997 Norfolk Virginia, no lettering or readable documents anywhere and no faces visible.
```

### `short200_02.png`  (hook / L1)
> the bare interrogation table at the police department

```
a bare metal interrogation table and two empty chairs standing under one low conical lamp in a tall windowless room, lit only by that lamp which is switched on, vertical 9:16 cinematic film still, 1997 Norfolk Virginia, no lettering or readable documents anywhere and no faces visible.
```

### `short200_03.png`  (hook / L1)
> a sealed evidence envelope from the apartment

```
a sealed paper evidence envelope lying square on a steel counter with every marking worn smooth and blank, lit only by one hard overhead lamp which is switched on, vertical 9:16 cinematic film still, 1997 Norfolk Virginia, no lettering or readable documents anywhere and no faces visible.
```

### `short200_04.png`  (hook / L1)
> a young sailor's hands flat on the table

```
a macro of two young hands laid flat and motionless on a scarred wooden table with nothing visible above the wrists, lit only by one hard overhead lamp which is switched on, vertical 9:16 cinematic film still, 1997 Norfolk Virginia, no lettering or readable documents anywhere and no faces visible.
```

### `short200_05.png`  (body / L2)
> the laboratory bench where the exclusions were run

```
a forensic laboratory bench carrying a heavy analytical instrument with all of its display panels dark and unreadable and clean glassware set out beside it, lit only by one task lamp which is switched on, vertical 9:16 cinematic film still, 1997 Norfolk Virginia, no lettering or readable documents anywhere and no faces visible.
```

### `short200_06.png`  (body / L2)
> the hours running through the night

```
a plain round institutional wall clock with a completely blank face and no numerals at all, mounted high on a bare painted wall, lit only by one fixture switched on beside it, vertical 9:16 cinematic film still, 1997 Norfolk Virginia, no lettering or readable documents anywhere and no faces visible.
```

### `short200_07.png`  (body / L2)
> two silhouettes across the interrogation table

```
two dark silhouettes facing each other across a small bare table with a single lamp hanging between them and neither face visible, lit only by that lamp, vertical 9:16 cinematic film still, 1997 Norfolk Virginia, no lettering or readable documents anywhere and no faces visible.
```

### `short200_08.png`  (body / L2)
> the case file growing heavier

```
a leaning tower of worn case folders stacked on a small metal desk with every label rubbed completely blank, lit only by one desk lamp switched on beside it, vertical 9:16 cinematic film still, 1997 Norfolk Virginia, no lettering or readable documents anywhere and no faces visible.
```

### `short200_09.png`  (body / L2)
> the paperwork of a case nobody stopped

```
a metal in-tray on a grey government desk overflowing with blank unmarked forms, lit only by one fluorescent tube switched on above it, vertical 9:16 cinematic film still, 1997 Norfolk Virginia, no lettering or readable documents anywhere and no faces visible.
```

### `short200_10.png`  (body / L2)
> the small apartment, afterwards

```
a single shaft of light crossing a small empty room thick with slowly drifting dust and nothing else in frame, lit only by that shaft, vertical 9:16 cinematic film still, 1997 Norfolk Virginia, no lettering or readable documents anywhere and no faces visible.
```

### `short200_11.png`  (body / L2)
> the door that opened to someone she knew

```
a residential front door seen from inside a dim hallway with its security chain hanging loose and one hard blade of light beneath it, lit only by that light, vertical 9:16 cinematic film still, 1997 Norfolk Virginia, no lettering or readable documents anywhere and no faces visible.
```

### `short200_12.png`  (body / L3)
> the next man brought into the room

```
one empty wooden chair standing alone in a hard cone of light in a large dark room with dust drifting through the beam, lit only by the fixture switched on above it, vertical 9:16 cinematic film still, 1997 Norfolk Virginia, no lettering or readable documents anywhere and no faces visible.
```

### `short200_13.png`  (body / L3)
> another arrest, another sailor

```
a macro of steel handcuffs closing around a pair of wrists with nothing visible above the forearms, lit only by one hard raking light, vertical 9:16 cinematic film still, 1997 Norfolk Virginia, no lettering or readable documents anywhere and no faces visible.
```

### `short200_14.png`  (body / L3)
> the men who were named by other men

```
an empty police lineup room with a bare marked wall and a height strip worn completely blank, lit only by one harsh fixture switched on above, vertical 9:16 cinematic film still, 1997 Norfolk Virginia, no lettering or readable documents anywhere and no faces visible.
```

### `short200_15.png`  (body / L3)
> the corridor between cells and questions

```
a long institutional corridor receding into darkness toward one brightly lit doorway at the far end, lit only by that doorway, vertical 9:16 cinematic film still, 1997 Norfolk Virginia, no lettering or readable documents anywhere and no faces visible.
```

### `short200_16.png`  (body / L3)
> the file that grew as it grew more false

```
the aisle of a deep records room with wooden shelving stacked to the ceiling with unlabelled evidence boxes, lit only by one bulb switched on at the far end, vertical 9:16 cinematic film still, 1997 Norfolk Virginia, no lettering or readable documents anywhere and no faces visible.
```

### `short200_17.png`  (body / L4)
> capital charges with no confession behind them

```
an extreme close-up of thick iron cell bars with a dark empty cell beyond them, lit only by one caged bulb switched on in the corridor behind, vertical 9:16 cinematic film still, 1997 Norfolk Virginia, no lettering or readable documents anywhere and no faces visible.
```

### `short200_18.png`  (body / L4)
> the courthouse where the death penalty stayed on the table

```
tall marble courthouse columns photographed from directly below against a heavy storm sky with no inscriptions anywhere, lit only by hard uplights switched on at their bases, vertical 9:16 cinematic film still, 1997 Norfolk Virginia, no lettering or readable documents anywhere and no faces visible.
```

### `short200_19.png`  (body / L4)
> a statement signed by a man who was not there

```
a macro of one hand pressing a pen to a completely blank sheet of paper on a bare table, no face or body visible, lit only by a single desk lamp which is switched on, vertical 9:16 cinematic film still, 1997 Norfolk Virginia, no lettering or readable documents anywhere and no faces visible.
```

### `short200_20.png`  (body / L4)
> three more sailors held on other men's words

```
the silhouette of a standing figure behind vertical iron bars with bright corridor light behind it and no face visible, lit only by that corridor light, vertical 9:16 cinematic film still, 1997 Norfolk Virginia, no lettering or readable documents anywhere and no faces visible.
```

### `short200_21.png`  (body / L4)
> an alibi that did not matter

```
a lone dark silhouette standing high in a single vertical shaft of light in a vast dark hall with a long empty floor below it, lit only by that shaft, vertical 9:16 cinematic film still, 1997 Norfolk Virginia, no lettering or readable documents anywhere and no faces visible.
```

### `short200_22.png`  (body / L4)
> the trials that stayed on the calendar

```
rows of empty polished courtroom gallery benches receding into shadow beneath one high window, lit only by the shaft from that window, vertical 9:16 cinematic film still, 1997 Norfolk Virginia, no lettering or readable documents anywhere and no faces visible.
```

## short201 — flowers
*時代設定：1996 to 2010 Winona Mississippi* / 22 枚

### `short201_01.png`  (hook / L1)
> a hand marking a blank juror sheet

```
a macro of one hand pressing a pencil to a completely blank unlined sheet on a courthouse table, no face or body visible, lit only by one desk lamp which is switched on, vertical 9:16 cinematic film still, 1996 to 2010 Winona Mississippi, no lettering or readable documents anywhere and no faces visible.
```

### `short201_02.png`  (hook / L1)
> the jury box the count is about

```
rows of empty wooden jury benches in a small county courtroom receding into shadow, lit only by one shaft of light from a high window, vertical 9:16 cinematic film still, 1996 to 2010 Winona Mississippi, no lettering or readable documents anywhere and no faces visible.
```

### `short201_03.png`  (hook / L1)
> the paper the count came out of

```
a leaning stack of worn court folders on a bare storeroom table with every label worn completely blank, lit only by one bulb switched on above them, vertical 9:16 cinematic film still, 1996 to 2010 Winona Mississippi, no lettering or readable documents anywhere and no faces visible.
```

### `short201_04.png`  (hook / L1)
> twenty-three years of it

```
a plain round courthouse wall clock with a completely blank featureless face hanging on a bare plaster wall, lit only by one fixture switched on beside it, vertical 9:16 cinematic film still, 1996 to 2010 Winona Mississippi, no lettering or readable documents anywhere and no faces visible.
```

### `short201_05.png`  (body / L2)
> the storeroom where the records live

```
the aisle of a county courthouse storeroom with wooden shelves stacked to the ceiling with unlabelled boxes, lit only by one bulb switched on at the far end, vertical 9:16 cinematic film still, 1996 to 2010 Winona Mississippi, no lettering or readable documents anywhere and no faces visible.
```

### `short201_06.png`  (body / L2)
> shelves nobody had ever pulled

```
a wall of grey steel filing shelves packed with unlabelled folders shot straight on, lit only by one flickering fluorescent tube switched on overhead, vertical 9:16 cinematic film still, 1996 to 2010 Winona Mississippi, no lettering or readable documents anywhere and no faces visible.
```

### `short201_07.png`  (body / L2)
> a working day that starts before light

```
a courthouse office window at first light with a desk buried in blank folders silhouetted against it, lit only by the pale dawn beyond the glass, vertical 9:16 cinematic film still, 1996 to 2010 Winona Mississippi, no lettering or readable documents anywhere and no faces visible.
```

### `short201_08.png`  (body / L2)
> a single sheet, and then thousands

```
one completely blank sheet of paper lying on a scuffed courthouse floor, lit only by a hard shaft of corridor light falling across it, vertical 9:16 cinematic film still, 1996 to 2010 Winona Mississippi, no lettering or readable documents anywhere and no faces visible.
```

### `short201_09.png`  (body / L2)
> the air of a room nobody enters

```
a shaft of light crossing a still storeroom thick with slowly drifting dust and nothing else in frame, lit only by that shaft, vertical 9:16 cinematic film still, 1996 to 2010 Winona Mississippi, no lettering or readable documents anywhere and no faces visible.
```

### `short201_10.png`  (body / L2)
> the clerk's desk the records passed over

```
a metal in-tray on a clerk's desk overflowing with blank unmarked forms, lit only by one fluorescent tube switched on above, vertical 9:16 cinematic film still, 1996 to 2010 Winona Mississippi, no lettering or readable documents anywhere and no faces visible.
```

### `short201_11.png`  (body / L2)
> a trial file, closed

```
a thick case file closed and tied with a band on a dark wooden desk with its cover worn completely blank, lit only by one desk lamp switched on, vertical 9:16 cinematic film still, 1996 to 2010 Winona Mississippi, no lettering or readable documents anywhere and no faces visible.
```

### `short201_12.png`  (body / L3)
> county by county

```
a long county courthouse corridor receding into darkness toward one brightly lit doorway at the far end, lit only by that doorway, vertical 9:16 cinematic film still, 1996 to 2010 Winona Mississippi, no lettering or readable documents anywhere and no faces visible.
```

### `short201_13.png`  (body / L3)
> trial by trial

```
a corridor of identical closed office doors with every nameplate blank, lit only by a row of ceiling fixtures switched on, vertical 9:16 cinematic film still, 1996 to 2010 Winona Mississippi, no lettering or readable documents anywhere and no faces visible.
```

### `short201_14.png`  (body / L3)
> the work of counting by hand

```
a macro of two hands laid flat on a scarred wooden table beside one closed unlabelled folder, no face or body above the wrists, lit only by one desk lamp switched on, vertical 9:16 cinematic film still, 1996 to 2010 Winona Mississippi, no lettering or readable documents anywhere and no faces visible.
```

### `short201_15.png`  (body / L3)
> the county seal on everything and nothing

```
a macro of a wooden-handled rubber stamp resting on an ink pad with the die face worn completely smooth, lit only by one desk lamp switched on, vertical 9:16 cinematic film still, 1996 to 2010 Winona Mississippi, no lettering or readable documents anywhere and no faces visible.
```

### `short201_16.png`  (body / L3)
> one district inside one state

```
a dark relief map of the United States with state borders drawn as thin glowing seams and absolutely no place names, lit only by that internal glow, vertical 9:16 cinematic film still, 1996 to 2010 Winona Mississippi, no lettering or readable documents anywhere and no faces visible.
```

### `short201_17.png`  (body / L4)
> the seat a struck juror never took

```
a single empty wooden juror chair standing in a hard cone of light in a dark courtroom, lit only by the fixture switched on above it, vertical 9:16 cinematic film still, 1996 to 2010 Winona Mississippi, no lettering or readable documents anywhere and no faces visible.
```

### `short201_18.png`  (body / L4)
> the bench that watched it happen

```
a judge's high wooden bench photographed from the floor looking up, entirely empty, lit only by one shaft of window light falling across its face, vertical 9:16 cinematic film still, 1996 to 2010 Winona Mississippi, no lettering or readable documents anywhere and no faces visible.
```

### `short201_19.png`  (body / L4)
> the questioning of prospective jurors

```
a low angle into a bare conical lamp burning into camera through smoke above a bare courthouse table, lit only by that lamp which is switched on, vertical 9:16 cinematic film still, 1996 to 2010 Winona Mississippi, no lettering or readable documents anywhere and no faces visible.
```

### `short201_20.png`  (body / L4)
> a quarter of a century

```
a stack of wall calendar pages caught mid-turn with every date worn completely blank, lit only by one angled desk lamp switched on, vertical 9:16 cinematic film still, 1996 to 2010 Winona Mississippi, no lettering or readable documents anywhere and no faces visible.
```

### `short201_21.png`  (body / L4)
> the courthouse the numbers came from

```
tall stone courthouse columns photographed from directly below against a heavy grey sky with no inscriptions anywhere, lit only by hard uplights switched on at their bases, vertical 9:16 cinematic film still, 1996 to 2010 Winona Mississippi, no lettering or readable documents anywhere and no faces visible.
```

### `short201_22.png`  (body / L4)
> one man inside the arithmetic

```
a lone dark silhouette standing high in a single vertical shaft of light in a vast dark hall with a long empty floor below, lit only by that shaft, vertical 9:16 cinematic film still, 1996 to 2010 Winona Mississippi, no lettering or readable documents anywhere and no faces visible.
```

## short202 — burge
*時代設定：1973 to 2011 Chicago* / 22 枚

### `short202_01.png`  (hook / L1)
> the clock the whole case runs on

```
a plain round institutional wall clock with a completely blank featureless face and no numerals, hanging on a bare precinct wall, lit only by one fixture switched on beside it, vertical 9:16 cinematic film still, 1973 to 2011 Chicago, no lettering or readable documents anywhere and no faces visible.
```

### `short202_02.png`  (hook / L1)
> the lamp in the room at Area 2

```
a low angle looking up into a bare conical lamp burning straight into camera through heavy smoke with the room beyond swallowed in black, lit only by that lamp which is switched on, vertical 9:16 cinematic film still, 1973 to 2011 Chicago, no lettering or readable documents anywhere and no faces visible.
```

### `short202_03.png`  (hook / L1)
> the charging decision that never came

```
a macro of a wooden-handled rubber stamp resting untouched on a dried ink pad with the die face worn completely smooth, lit only by one desk lamp switched on, vertical 9:16 cinematic film still, 1973 to 2011 Chicago, no lettering or readable documents anywhere and no faces visible.
```

### `short202_04.png`  (hook / L1)
> a man's hands after the room

```
a macro of two weathered hands laid flat and still on a scarred wooden table with nothing visible above the wrists, lit only by one hard overhead lamp which is switched on, vertical 9:16 cinematic film still, 1973 to 2011 Chicago, no lettering or readable documents anywhere and no faces visible.
```

### `short202_05.png`  (body / L2)
> four years of claims on a desk

```
a leaning tower of worn case folders stacked on a small desk with every label worn completely blank, lit only by one desk lamp switched on beside it, vertical 9:16 cinematic film still, 1973 to 2011 Chicago, no lettering or readable documents anywhere and no faces visible.
```

### `short202_06.png`  (body / L2)
> the interview room at the heart of it

```
a bare metal interview table and two chairs standing under a single conical lamp hung low in a tall bare-walled room, lit only by that lamp which is switched on, vertical 9:16 cinematic film still, 1973 to 2011 Chicago, no lettering or readable documents anywhere and no faces visible.
```

### `short202_07.png`  (body / L2)
> the chair a suspect was left in

```
a single empty wooden chair standing in a hard cone of light in a large dark empty room with dust drifting, lit only by the fixture switched on above it, vertical 9:16 cinematic film still, 1973 to 2011 Chicago, no lettering or readable documents anywhere and no faces visible.
```

### `short202_08.png`  (body / L2)
> one page of a report nobody acted on

```
one completely blank sheet of paper lying on a scuffed institutional floor, lit only by a hard shaft of corridor light falling across it, vertical 9:16 cinematic film still, 1973 to 2011 Chicago, no lettering or readable documents anywhere and no faces visible.
```

### `short202_09.png`  (body / L2)
> the years passing in an empty room

```
a shaft of light crossing an empty room thick with slowly drifting dust and nothing else in frame, lit only by that shaft, vertical 9:16 cinematic film still, 1973 to 2011 Chicago, no lettering or readable documents anywhere and no faces visible.
```

### `short202_10.png`  (body / L2)
> complaints that went into a tray

```
a metal in-tray overflowing with blank unreadable forms on a grey municipal desk, lit only by one fluorescent tube switched on above, vertical 9:16 cinematic film still, 1973 to 2011 Chicago, no lettering or readable documents anywhere and no faces visible.
```

### `short202_11.png`  (body / L2)
> three years, counted down

```
a stack of wall calendar pages caught mid-turn with all dates worn completely blank, lit only by one angled desk lamp switched on, vertical 9:16 cinematic film still, 1973 to 2011 Chicago, no lettering or readable documents anywhere and no faces visible.
```

### `short202_12.png`  (body / L3)
> 1973, and the man who did not come back the same

```
two dark silhouettes facing each other across a small bare table with one hanging lamp between them and neither face visible, lit only by that lamp, vertical 9:16 cinematic film still, 1973 to 2011 Chicago, no lettering or readable documents anywhere and no faces visible.
```

### `short202_13.png`  (body / L3)
> the corridor at Area 2

```
a long precinct corridor receding into darkness toward one brightly lit doorway at the far end, lit only by that doorway, vertical 9:16 cinematic film still, 1973 to 2011 Chicago, no lettering or readable documents anywhere and no faces visible.
```

### `short202_14.png`  (body / L3)
> February 1982

```
a macro of steel handcuffs closing on a pair of wrists with no face or body above the forearms, lit only by one hard raking light, vertical 9:16 cinematic film still, 1973 to 2011 Chicago, no lettering or readable documents anywhere and no faces visible.
```

### `short202_15.png`  (body / L3)
> the medical record that survived

```
a sealed paper evidence envelope resting on a steel counter with all writing worn completely blank, lit only by one hard overhead lamp switched on, vertical 9:16 cinematic film still, 1973 to 2011 Chicago, no lettering or readable documents anywhere and no faces visible.
```

### `short202_16.png`  (body / L3)
> the deadline closing

```
a heavy door swinging shut on a narrowing blade of light seen from inside a dark room, lit only by that closing light, vertical 9:16 cinematic film still, 1973 to 2011 Chicago, no lettering or readable documents anywhere and no faces visible.
```

### `short202_17.png`  (body / L4)
> a decade of files, unopened

```
a wall of grey steel filing shelves packed with unlabelled folders shot straight on, lit only by one flickering fluorescent tube switched on overhead, vertical 9:16 cinematic film still, 1973 to 2011 Chicago, no lettering or readable documents anywhere and no faces visible.
```

### `short202_18.png`  (body / L4)
> the report locked in a drawer

```
the aisle of a deep records room with shelving stacked to the ceiling with unlabelled boxes, lit only by one bulb switched on at the far end, vertical 9:16 cinematic film still, 1973 to 2011 Chicago, no lettering or readable documents anywhere and no faces visible.
```

### `short202_19.png`  (body / L4)
> two years of fighting to keep it there

```
a heavy door secured with a chain and padlock in a dim service corridor with all notices worn blank, lit only by one caged bulb switched on, vertical 9:16 cinematic film still, 1973 to 2011 Chicago, no lettering or readable documents anywhere and no faces visible.
```

### `short202_20.png`  (body / L4)
> the morning the report was finally released

```
an office window at first light with a desk buried in blank folders silhouetted against it, lit only by the pale dawn beyond the glass, vertical 9:16 cinematic film still, 1973 to 2011 Chicago, no lettering or readable documents anywhere and no faces visible.
```

### `short202_21.png`  (body / L4)
> the courthouse the cases never reached

```
tall stone courthouse columns photographed from directly below against a dark storm sky with no inscriptions anywhere, lit only by hard uplights switched on at their bases, vertical 9:16 cinematic film still, 1973 to 2011 Chicago, no lettering or readable documents anywhere and no faces visible.
```

### `short202_22.png`  (body / L4)
> more than a hundred men

```
a lone dark silhouette standing high in a single vertical shaft of light in a vast dark hall with a long empty floor below it, lit only by that shaft, vertical 9:16 cinematic film still, 1973 to 2011 Chicago, no lettering or readable documents anywhere and no faces visible.
```

## short203 — postoffice
*時代設定：2000s England* / 22 枚

### `short203_01.png`  (hook / L1)
> the helpline handset on the counter

```
a black telephone handset lying off its cradle on a worn post-office counter with the coiled cord hanging down, lit only by one pendant bulb switched on above the counter, vertical 9:16 cinematic film still, 2000s England, no lettering or readable documents anywhere and no faces visible.
```

### `short203_02.png`  (hook / L1)
> closing time, again

```
a plain round wall clock with a completely blank featureless face hanging above a village post-office counter, lit only by one fixture switched on beside it, vertical 9:16 cinematic film still, 2000s England, no lettering or readable documents anywhere and no faces visible.
```

### `short203_03.png`  (hook / L1)
> a sub-postmistress counting again

```
a macro of two hands laid flat on a worn wooden shop counter beside a closed cash drawer with nothing visible above the wrists, lit only by one lamp switched on above, vertical 9:16 cinematic film still, 2000s England, no lettering or readable documents anywhere and no faces visible.
```

### `short203_04.png`  (hook / L1)
> the shop after the shutters come down

```
a low angle looking up into a bare pendant bulb burning into camera above a shop counter with the room beyond swallowed in black, lit only by that bulb which is switched on, vertical 9:16 cinematic film still, 2000s England, no lettering or readable documents anywhere and no faces visible.
```

### `short203_05.png`  (body / L2)
> the till that would not agree

```
banded bundles of banknotes and loose coins counted out across a wooden shop counter with every denomination illegible, lit only by one desk lamp switched on, vertical 9:16 cinematic film still, 2000s England, no lettering or readable documents anywhere and no faces visible.
```

### `short203_06.png`  (body / L2)
> the branch paperwork, night after night

```
a leaning tower of worn ledgers and folders stacked on a small back-room desk with every label worn completely blank, lit only by one desk lamp switched on, vertical 9:16 cinematic film still, 2000s England, no lettering or readable documents anywhere and no faces visible.
```

### `short203_07.png`  (body / L2)
> the branch safe

```
a small steel safe door closed in a cramped back room with its dial and markings worn completely smooth, lit only by one hard uplight switched on, vertical 9:16 cinematic film still, 2000s England, no lettering or readable documents anywhere and no faces visible.
```

### `short203_08.png`  (body / L2)
> the shop, empty, at the end of it

```
a shaft of light crossing an empty shop floor thick with slowly drifting dust and nothing else in frame, lit only by that shaft, vertical 9:16 cinematic film still, 2000s England, no lettering or readable documents anywhere and no faces visible.
```

### `short203_09.png`  (body / L2)
> forms that arrived and kept arriving

```
a metal in-tray on a back-room desk overflowing with blank unmarked forms, lit only by one fluorescent tube switched on above, vertical 9:16 cinematic film still, 2000s England, no lettering or readable documents anywhere and no faces visible.
```

### `short203_10.png`  (body / L2)
> opening up the next morning

```
a village shop window at first light with a counter and blank folders silhouetted against it, lit only by the pale dawn beyond the glass, vertical 9:16 cinematic film still, 2000s England, no lettering or readable documents anywhere and no faces visible.
```

### `short203_11.png`  (body / L2)
> the stool nobody sat down on

```
one empty wooden chair standing in a hard cone of light behind a dark shop counter, lit only by the fixture switched on above it, vertical 9:16 cinematic film still, 2000s England, no lettering or readable documents anywhere and no faces visible.
```

### `short203_12.png`  (body / L3)
> signing for a loss that was not real

```
a macro of one hand pressing a pen to a completely blank ledger page on a counter, no face or body visible, lit only by a single desk lamp switched on, vertical 9:16 cinematic film still, 2000s England, no lettering or readable documents anywhere and no faces visible.
```

### `short203_13.png`  (body / L3)
> the kitchen table at two in the morning

```
printed sheets fanned across a kitchen table with every figure and heading worn completely blank, lit only by one desk lamp switched on, vertical 9:16 cinematic film still, 2000s England, no lettering or readable documents anywhere and no faces visible.
```

### `short203_14.png`  (body / L3)
> locking up on an impossible number

```
a heavy shop door swinging shut on a narrowing blade of evening light seen from inside a dark shop, lit only by that closing light, vertical 9:16 cinematic film still, 2000s England, no lettering or readable documents anywhere and no faces visible.
```

### `short203_15.png`  (body / L3)
> a receipt on the shop floor

```
one completely blank slip of paper lying on a scuffed shop floor, lit only by a hard shaft of light falling across it, vertical 9:16 cinematic film still, 2000s England, no lettering or readable documents anywhere and no faces visible.
```

### `short203_16.png`  (body / L3)
> the shoebox of receipts, kept

```
a thick file closed and tied with a band on a kitchen table with its cover worn completely blank, lit only by one desk lamp switched on, vertical 9:16 cinematic film still, 2000s England, no lettering or readable documents anywhere and no faces visible.
```

### `short203_17.png`  (body / L4)
> the same call, in a thousand villages

```
a long narrow shop corridor receding into darkness toward one brightly lit doorway at the far end, lit only by that doorway, vertical 9:16 cinematic film still, 2000s England, no lettering or readable documents anywhere and no faces visible.
```

### `short203_18.png`  (body / L4)
> a debt that only grew

```
a single pale line rising smoothly across dark glass with no dips and no numerals anywhere, lit only by its own glow, vertical 9:16 cinematic film still, 2000s England, no lettering or readable documents anywhere and no faces visible.
```

### `short203_19.png`  (body / L4)
> each of them alone in a dark shop

```
a lone dark silhouette standing high in a single vertical shaft of light in a vast dark hall with a long empty floor below it, lit only by that shaft, vertical 9:16 cinematic film still, 2000s England, no lettering or readable documents anywhere and no faces visible.
```

### `short203_20.png`  (body / L4)
> the counter stamp of a centuries-old institution

```
a macro of a wooden-handled rubber date stamp resting on an ink pad with the die face worn completely smooth, lit only by one desk lamp switched on, vertical 9:16 cinematic film still, 2000s England, no lettering or readable documents anywhere and no faces visible.
```

### `short203_21.png`  (body / L4)
> the branch that closed

```
a shop shutter secured with a chain and padlock in a dim doorway with all notices worn blank, lit only by one lamp switched on above, vertical 9:16 cinematic film still, 2000s England, no lettering or readable documents anywhere and no faces visible.
```

### `short203_22.png`  (body / L4)
> years of the same call

```
a stack of wall calendar pages caught mid-turn with all dates worn completely blank, lit only by one angled desk lamp switched on, vertical 9:16 cinematic film still, 2000s England, no lettering or readable documents anywhere and no faces visible.
```

## short204 — postoffice
*時代設定：1999 to 2015 England* / 22 枚

### `short204_01.png`  (hook / L1)
> the charge decided in-house

```
a macro of a wooden-handled rubber stamp pressed onto an ink pad on a bare office desk with the die face worn completely smooth, lit only by one desk lamp switched on, vertical 9:16 cinematic film still, 1999 to 2015 England, no lettering or readable documents anywhere and no faces visible.
```

### `short204_02.png`  (hook / L1)
> the court the company walked into

```
tall stone Crown Court columns photographed from directly below against a heavy grey sky with no inscriptions anywhere, lit only by hard uplights switched on at their bases, vertical 9:16 cinematic film still, 1999 to 2015 England, no lettering or readable documents anywhere and no faces visible.
```

### `short204_03.png`  (hook / L1)
> a charge sheet signed by the employer

```
a macro of one hand pressing a pen to a completely blank sheet on a bare desk, no face or body visible, lit only by a single desk lamp which is switched on, vertical 9:16 cinematic film still, 1999 to 2015 England, no lettering or readable documents anywhere and no faces visible.
```

### `short204_04.png`  (hook / L1)
> an arrest made by a company

```
a macro of steel handcuffs closing on a pair of wrists with no face or body above the forearms, lit only by one hard raking light, vertical 9:16 cinematic film still, 1999 to 2015 England, no lettering or readable documents anywhere and no faces visible.
```

### `short204_05.png`  (body / L2)
> seven hundred files

```
a leaning tower of worn prosecution folders stacked on a small desk with every label worn completely blank, lit only by one desk lamp switched on beside it, vertical 9:16 cinematic film still, 1999 to 2015 England, no lettering or readable documents anywhere and no faces visible.
```

### `short204_06.png`  (body / L2)
> a wall of cases, one a week

```
a wall of grey steel filing shelves packed with unlabelled folders shot straight on, lit only by one flickering fluorescent tube switched on overhead, vertical 9:16 cinematic film still, 1999 to 2015 England, no lettering or readable documents anywhere and no faces visible.
```

### `short204_07.png`  (body / L2)
> fifteen years of it

```
a plain round office wall clock with a completely blank featureless face on a bare wall, lit only by one fixture switched on beside it, vertical 9:16 cinematic film still, 1999 to 2015 England, no lettering or readable documents anywhere and no faces visible.
```

### `short204_08.png`  (body / L2)
> a Crown Court, half empty

```
rows of empty polished courtroom benches receding into shadow beneath one high window, lit only by the shaft from that window, vertical 9:16 cinematic film still, 1999 to 2015 England, no lettering or readable documents anywhere and no faces visible.
```

### `short204_09.png`  (body / L2)
> the department that ran the prosecutions

```
a corridor of identical closed office doors with every nameplate blank, lit only by a row of ceiling fixtures switched on, vertical 9:16 cinematic film still, 1999 to 2015 England, no lettering or readable documents anywhere and no faces visible.
```

### `short204_10.png`  (body / L2)
> hands on a table in an interview under caution

```
a macro of two hands laid flat on a scarred wooden table with nothing visible above the wrists, lit only by one hard overhead lamp switched on, vertical 9:16 cinematic film still, 1999 to 2015 England, no lettering or readable documents anywhere and no faces visible.
```

### `short204_11.png`  (body / L2)
> one a week, for a decade and a half

```
a stack of wall calendar pages caught mid-turn with all dates worn completely blank, lit only by one angled desk lamp switched on, vertical 9:16 cinematic film still, 1999 to 2015 England, no lettering or readable documents anywhere and no faces visible.
```

### `short204_12.png`  (body / L3)
> the police who were never called

```
a tight low angle on the front wing and dark roof bar of a parked patrol car standing empty at a kerb in flat daylight, lit only by that daylight, vertical 9:16 cinematic film still, 1999 to 2015 England, no lettering or readable documents anywhere and no faces visible.
```

### `short204_13.png`  (body / L3)
> the corridor to a hearing room

```
a long institutional corridor receding into darkness toward one brightly lit doorway at the far end, lit only by that doorway, vertical 9:16 cinematic film still, 1999 to 2015 England, no lettering or readable documents anywhere and no faces visible.
```

### `short204_14.png`  (body / L3)
> the chair a sub-postmaster was put in

```
one empty wooden chair standing in a hard cone of light in a large dark room, lit only by the fixture switched on above it, vertical 9:16 cinematic film still, 1999 to 2015 England, no lettering or readable documents anywhere and no faces visible.
```

### `short204_15.png`  (body / L3)
> the lamp above the interview

```
a low angle looking up into a bare conical lamp burning into camera through drifting smoke with the room beyond in black, lit only by that lamp which is switched on, vertical 9:16 cinematic film still, 1999 to 2015 England, no lettering or readable documents anywhere and no faces visible.
```

### `short204_16.png`  (body / L3)
> the shop suspended on the spot

```
a shaft of light crossing an empty shop back room thick with slowly drifting dust and nothing else in frame, lit only by that shaft, vertical 9:16 cinematic film still, 1999 to 2015 England, no lettering or readable documents anywhere and no faces visible.
```

### `short204_17.png`  (body / L4)
> the back room turned into an interview room

```
a bare table and two chairs standing under a single low lamp in a cramped back room with bare walls, lit only by that lamp which is switched on, vertical 9:16 cinematic film still, 1999 to 2015 England, no lettering or readable documents anywhere and no faces visible.
```

### `short204_18.png`  (body / L4)
> the investigator and the shopkeeper

```
two dark silhouettes facing each other across a small bare table with one hanging lamp between them and neither face visible, lit only by that lamp, vertical 9:16 cinematic film still, 1999 to 2015 England, no lettering or readable documents anywhere and no faces visible.
```

### `short204_19.png`  (body / L4)
> what theft meant

```
an extreme close-up of thick iron cell bars with a dark empty cell beyond them, lit only by one caged bulb switched on in the corridor behind, vertical 9:16 cinematic film still, 1999 to 2015 England, no lettering or readable documents anywhere and no faces visible.
```

### `short204_20.png`  (body / L4)
> the offer, and the door

```
a heavy door swinging shut on a narrowing blade of light seen from inside a dark room, lit only by that closing light, vertical 9:16 cinematic film still, 1999 to 2015 England, no lettering or readable documents anywhere and no faces visible.
```

### `short204_21.png`  (body / L4)
> the plea, on one page

```
one completely blank sheet of paper lying on a scuffed courthouse floor, lit only by a hard shaft of corridor light falling across it, vertical 9:16 cinematic film still, 1999 to 2015 England, no lettering or readable documents anywhere and no faces visible.
```

### `short204_22.png`  (body / L4)
> a shopkeeper against an institution

```
a lone dark silhouette standing high in a single vertical shaft of light in a vast dark hall with a long empty floor below, lit only by that shaft, vertical 9:16 cinematic film still, 1999 to 2015 England, no lettering or readable documents anywhere and no faces visible.
```

## short205 — postoffice
*時代設定：2010 to 2019 England* / 22 枚

### `short205_01.png`  (hook / L1)
> a pen laid down on an internal report

```
a macro of one hand laying a pen down beside a completely blank typed page on a polished desk, no face or body visible, lit only by one desk lamp switched on, vertical 9:16 cinematic film still, 2010 to 2019 England, no lettering or readable documents anywhere and no faces visible.
```

### `short205_02.png`  (hook / L1)
> the lamp over the desk it landed on

```
a low angle looking up into a bare conical lamp burning into camera through drifting smoke with the room beyond in black, lit only by that lamp which is switched on, vertical 9:16 cinematic film still, 2010 to 2019 England, no lettering or readable documents anywhere and no faces visible.
```

### `short205_03.png`  (hook / L1)
> the senior desks it went to

```
a long polished conference table with the chairs pushed in and a dark blank projection wall behind it and nobody present, lit only by one pendant switched on above the table, vertical 9:16 cinematic film still, 2010 to 2019 England, no lettering or readable documents anywhere and no faces visible.
```

### `short205_04.png`  (hook / L1)
> the report, filed

```
a leaning tower of unmarked report binders stacked on an office desk with every spine worn completely blank, lit only by one desk lamp switched on, vertical 9:16 cinematic film still, 2010 to 2019 England, no lettering or readable documents anywhere and no faces visible.
```

### `short205_05.png`  (body / L2)
> everything the institution kept

```
the aisle of a deep records room with shelving stacked to the ceiling with unlabelled boxes, lit only by one bulb switched on at the far end, vertical 9:16 cinematic film still, 2010 to 2019 England, no lettering or readable documents anywhere and no faces visible.
```

### `short205_06.png`  (body / L2)
> the disclosure that never came

```
a wall of grey steel filing shelves packed with unlabelled folders shot straight on, lit only by one flickering fluorescent tube switched on overhead, vertical 9:16 cinematic film still, 2010 to 2019 England, no lettering or readable documents anywhere and no faces visible.
```

### `short205_07.png`  (body / L2)
> eleven weeks

```
a plain round office wall clock with a completely blank featureless face on a bare wall, lit only by one fixture switched on beside it, vertical 9:16 cinematic film still, 2010 to 2019 England, no lettering or readable documents anywhere and no faces visible.
```

### `short205_08.png`  (body / L2)
> the memos that stayed internal

```
a metal in-tray overflowing with blank unmarked papers on a grey office desk, lit only by one fluorescent tube switched on above, vertical 9:16 cinematic film still, 2010 to 2019 England, no lettering or readable documents anywhere and no faces visible.
```

### `short205_09.png`  (body / L2)
> an office after hours

```
a shaft of light crossing an empty open-plan office thick with slowly drifting dust and nothing else in frame, lit only by that shaft, vertical 9:16 cinematic film still, 2010 to 2019 England, no lettering or readable documents anywhere and no faces visible.
```

### `short205_10.png`  (body / L2)
> the figures the branches could not dispute

```
printed statements fanned across a dark desk with every figure and heading worn completely blank, lit only by one desk lamp switched on, vertical 9:16 cinematic film still, 2010 to 2019 England, no lettering or readable documents anywhere and no faces visible.
```

### `short205_11.png`  (body / L2)
> the morning after the decision

```
an office window at first light with a desk buried in blank folders silhouetted against it, lit only by the pale dawn beyond the glass, vertical 9:16 cinematic film still, 2010 to 2019 England, no lettering or readable documents anywhere and no faces visible.
```

### `short205_12.png`  (body / L3)
> the cost of checking

```
a single pale line rising smoothly across dark glass with no dips and no numerals anywhere, lit only by its own glow, vertical 9:16 cinematic film still, 2010 to 2019 England, no lettering or readable documents anywhere and no faces visible.
```

### `short205_13.png`  (body / L3)
> the chair in the dock

```
one empty wooden chair standing in a hard cone of light in a large dark room, lit only by the fixture switched on above it, vertical 9:16 cinematic film still, 2010 to 2019 England, no lettering or readable documents anywhere and no faces visible.
```

### `short205_14.png`  (body / L3)
> one page, decisive

```
one completely blank sheet of paper lying on a scuffed office floor, lit only by a hard shaft of corridor light falling across it, vertical 9:16 cinematic film still, 2010 to 2019 England, no lettering or readable documents anywhere and no faces visible.
```

### `short205_15.png`  (body / L3)
> the appeal that was not allowed to open

```
a heavy door swinging shut on a narrowing blade of light seen from inside a dark room, lit only by that closing light, vertical 9:16 cinematic film still, 2010 to 2019 England, no lettering or readable documents anywhere and no faces visible.
```

### `short205_16.png`  (body / L3)
> prosecution by prosecution

```
a macro of a wooden-handled rubber stamp resting on an ink pad with the die face worn completely smooth, lit only by one desk lamp switched on, vertical 9:16 cinematic film still, 2010 to 2019 England, no lettering or readable documents anywhere and no faces visible.
```

### `short205_17.png`  (body / L4)
> Guildford Crown Court

```
tall stone Crown Court columns photographed from directly below against a heavy grey sky with no inscriptions anywhere, lit only by hard uplights switched on at their bases, vertical 9:16 cinematic film still, 2010 to 2019 England, no lettering or readable documents anywhere and no faces visible.
```

### `short205_18.png`  (body / L4)
> the jury that was assured

```
rows of empty polished courtroom benches receding into shadow beneath one high window, lit only by the shaft from that window, vertical 9:16 cinematic film still, 2010 to 2019 England, no lettering or readable documents anywhere and no faces visible.
```

### `short205_19.png`  (body / L4)
> fifteen months

```
an extreme close-up of thick iron cell bars with a dark empty cell beyond them, lit only by one caged bulb switched on in the corridor behind, vertical 9:16 cinematic film still, 2010 to 2019 England, no lettering or readable documents anywhere and no faces visible.
```

### `short205_20.png`  (body / L4)
> the corridor out of the courtroom

```
a long institutional corridor receding into darkness toward one brightly lit doorway at the far end, lit only by that doorway, vertical 9:16 cinematic film still, 2010 to 2019 England, no lettering or readable documents anywhere and no faces visible.
```

### `short205_21.png`  (body / L4)
> a witness's hands on the rail

```
a macro of two hands resting on a polished wooden rail with nothing visible above the wrists, lit only by one hard overhead lamp switched on, vertical 9:16 cinematic film still, 2010 to 2019 England, no lettering or readable documents anywhere and no faces visible.
```

### `short205_22.png`  (body / L4)
> the expert on the stand

```
a lone dark silhouette standing high in a single vertical shaft of light in a vast dark hall with a long empty floor below, lit only by that shaft, vertical 9:16 cinematic film still, 2010 to 2019 England, no lettering or readable documents anywhere and no faces visible.
```

## short250 — fieldtest
*時代設定：2010 Houston, Texas* / 22 枚

### `short250_01.png`  (hook / L1)
> a patrol car beacon over an empty strip-mall kerb

```
tight low angle on the front fender and single roof beacon of a police cruiser parked at a strip-mall kerb, chrome and dark paint filling the frame, no lettering on the bodywork, lit ONLY by that beacon which is switched on and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Houston, Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short250_02.png`  (hook / L1)
> a small sealed test pouch lying on a car bonnet

```
macro of a small sealed plastic test pouch lying on the bonnet of a car, its printed panel worn completely blank and unreadable, lit ONLY by one hard work light which is switched on and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Houston, Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short250_03.png`  (hook / L1)
> a blank-faced institutional clock counting the ninety seconds

```
a plain round institutional wall clock with a completely blank featureless face and no numerals or markings, hard side light across it, lit ONLY by one fixture switched on beside it, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Houston, Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short250_04.png`  (hook / L1)
> two gloved hands holding a vial of pink liquid

```
macro of two gloved hands holding a small glass vial of pale pink liquid over a dark car floormat, no face or body above the wrists, lit ONLY by one hard torch beam which is switched on and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Houston, Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short250_05.png`  (body / L2)
> the stopped car seen from the passenger side

```
the interior of a parked car seen from the passenger side, empty seats, a red and blue wash crossing the dashboard from behind, no dials or displays legible, lit ONLY by those beacons which are switched on and are the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Houston, Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short250_06.png`  (body / L2)
> dust drifting across an empty parking bay

```
a shaft of light crossing an empty asphalt parking bay at the edge of a low strip mall, thick with slowly drifting dust and nothing else in frame, lit ONLY by that shaft, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Houston, Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short250_07.png`  (body / L2)
> one white crumb on a ribbed car floormat

```
macro of one small white crumb resting on the ribbed rubber floormat of a car, the frame shallow and dark all around it, lit ONLY by a single hard rim light which is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Houston, Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short250_08.png`  (body / L2)
> a car door swinging shut on a blade of daylight

```
a car door swinging shut on a narrowing blade of daylight seen from inside the dark cabin, no badges or lettering visible, lit ONLY by that closing light, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Houston, Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short250_09.png`  (body / L2)
> a booking tray holding a driver's effects

```
a steel booking tray holding a belt, a set of car keys and a few coins on a counter, every label blank, lit ONLY by one hard overhead lamp which is switched on and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Houston, Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short250_10.png`  (body / L2)
> a hand pressing a pen to a blank evidence form

```
macro of one hand pressing a ballpoint pen to a completely blank unreadable form laid on the boot lid of a car, no face or body visible, lit ONLY by a single hand torch which is switched on and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Houston, Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short250_11.png`  (body / L2)
> a stamp resting on an ink pad at a booking counter

```
macro of a wooden-handled rubber stamp resting on an ink pad on a booking counter, the die face worn completely smooth and unreadable, lit ONLY by one desk lamp which is switched on and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Houston, Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short250_12.png`  (body / L3)
> the laboratory bench the roadside did not have

```
a forensic laboratory bench with a heavy analytical instrument, every display dark and unreadable, nobody present, lit ONLY by one task lamp which is switched on and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Houston, Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short250_13.png`  (body / L3)
> an in-tray standing completely empty

```
a metal in-tray standing completely empty on a grey desk with no forms or printouts in it at all, lit ONLY by one fluorescent tube which is switched on above it and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Houston, Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short250_14.png`  (body / L3)
> handcuffs closing on wrists over dark asphalt

```
macro of steel handcuffs closing on a pair of wrists over dark asphalt, no face or body above the forearms, lit ONLY by one hard raking light which is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Houston, Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short250_15.png`  (body / L3)
> a case file closed and tied with a band

```
a thick case file closed and tied with a band on a dark desk, its cover worn completely blank, lit ONLY by one desk lamp which is switched on and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Houston, Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short250_16.png`  (body / L3)
> doors swinging open onto blinding daylight

```
heavy doors swinging open onto blinding daylight seen from inside a dark room, no signage anywhere, lit ONLY by that daylight beyond, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Houston, Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short250_17.png`  (body / L4)
> painted steel cell bars, extreme close

```
extreme close-up of thick painted steel cell bars with a dark empty cell beyond, lit ONLY by one caged bulb which is switched on in the corridor behind and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Houston, Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short250_18.png`  (body / L4)
> a cell block corridor of steel doors

```
a long cell block corridor of steel doors receding into the distance, all numbers worn blank, lit ONLY by a row of caged ceiling bulbs which are switched on and are the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Houston, Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short250_19.png`  (body / L4)
> a bare cell with a high barred window

```
the interior of a bare cell, a small high barred window throwing one hard shaft onto the concrete floor, lit ONLY by that window, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Houston, Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short250_20.png`  (body / L4)
> a booking corridor receding to a lit doorway

```
a long institutional booking corridor receding into darkness toward one brightly lit doorway at the far end, lit ONLY by that doorway, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Houston, Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short250_21.png`  (body / L4)
> a lone silhouette high in a shaft of light

```
a lone dark silhouette standing in a single vertical shaft of light in a vast dark hall, the figure placed high in frame with its head in the upper third and a long empty floor below it, face not visible, lit ONLY by that shaft, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Houston, Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short250_22.png`  (body / L4)
> a window at first light over a booking desk

```
an office window at first light with a booking desk buried in blank unlabelled folders silhouetted against it, lit ONLY by the pale dawn beyond the glass, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Houston, Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

## short251 — fieldtest
*時代設定：2010 Houston, Texas* / 22 枚

### `short251_01.png`  (hook / L1)
> a lone silhouette high in a courthouse shaft of light

```
a lone dark silhouette standing in a single vertical shaft of light in a vast dark courthouse hall, the figure placed high in frame with its head in the upper third and a long empty floor below it, face not visible, lit ONLY by that shaft, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Houston, Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short251_02.png`  (hook / L1)
> a blank-faced clock high on a corridor wall

```
a plain round institutional wall clock with a completely blank featureless face and no numerals, mounted high on a bare corridor wall, lit ONLY by one fixture which is switched on beside it and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Houston, Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short251_03.png`  (hook / L1)
> two plain chairs turned to face each other

```
two plain chairs turned to face each other across a bare floor in a small dim room, nobody in them, lit ONLY by one window shaft which is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Houston, Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short251_04.png`  (hook / L1)
> a courthouse corridor receding to a lit doorway

```
a long courthouse corridor receding into darkness toward one brightly lit doorway at the far end, all nameplates blank, lit ONLY by that doorway, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Houston, Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short251_05.png`  (body / L2)
> calendar pages caught mid-turn, dates worn blank

```
a stack of wall calendar pages caught mid-turn, all dates worn blank and unreadable, lit ONLY by one angled desk lamp which is switched on and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Houston, Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short251_06.png`  (body / L2)
> a leaning tower of worn case folders

```
a leaning tower of worn case folders on a small desk, every label worn completely blank, lit ONLY by one desk lamp which is switched on beside it and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Houston, Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short251_07.png`  (body / L2)
> an in-tray overflowing with blank forms

```
a metal in-tray overflowing with blank unreadable forms on a grey desk, lit ONLY by one fluorescent tube which is switched on above it and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Houston, Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short251_08.png`  (body / L2)
> two weathered hands laid flat on a scarred table

```
macro of two weathered hands laid flat on a scarred wooden table, no face or body above the wrists, lit ONLY by one hard overhead lamp which is switched on and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Houston, Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short251_09.png`  (body / L2)
> a bare holding cell with a high barred window

```
the interior of a bare holding cell, a small high barred window throwing one hard shaft onto the concrete floor, lit ONLY by that window, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Houston, Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short251_10.png`  (body / L2)
> a records room aisle of unlabelled boxes

```
looking down the aisle of a deep records room, shelving stacked to the ceiling with unlabelled boxes, lit ONLY by one bulb which is switched on at the far end and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Houston, Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short251_11.png`  (body / L2)
> dust drifting in a shaft across an empty holding room

```
a shaft of light crossing an empty holding room thick with slowly drifting dust, nothing else in frame, lit ONLY by that shaft, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Houston, Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short251_12.png`  (body / L3)
> a judge's high bench seen from the floor

```
a judge's high wooden bench photographed from the floor looking up, empty, no inscriptions anywhere, lit ONLY by one shaft of window light falling across its face, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Houston, Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short251_13.png`  (body / L3)
> rows of empty courtroom gallery benches

```
rows of empty polished wooden courtroom gallery benches receding into shadow, lit ONLY by one shaft of light from a high window, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Houston, Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short251_14.png`  (body / L3)
> a single empty chair in a cone of light

```
a single empty wooden chair standing in a cone of light in a large dark empty courtroom, dust motes drifting around it, lit ONLY by the fixture which is switched on above it and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Houston, Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short251_15.png`  (body / L3)
> a gavel caught mid-strike above its block

```
a wooden judge's gavel caught mid-strike above its round block with motion blur on the head, lit ONLY by one brass bench lamp which is switched on and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Houston, Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short251_16.png`  (body / L3)
> an empty tiered chamber of vacant seats

```
an empty tiered chamber with rows of vacant seats and a long bench, all nameplates blank, lit ONLY by one bank of overhead lights which are switched on and are the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Houston, Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short251_17.png`  (body / L4)
> a cell block corridor of steel doors

```
a long cell block corridor of steel doors receding into the distance, all numbers worn blank, lit ONLY by a row of caged ceiling bulbs which are switched on and are the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Houston, Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short251_18.png`  (body / L4)
> a backlit silhouette behind vertical bars

```
silhouette of a figure standing behind vertical steel bars with bright corridor light behind, face not visible, strong vertical rhythm across the frame, lit ONLY by that corridor light, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Houston, Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short251_19.png`  (body / L4)
> a phone lying face down on a dark table

```
a smartphone lying face down on a dark table, its edge catching one hard light, screen not visible, lit ONLY by a single desk lamp which is switched on and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Houston, Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short251_20.png`  (body / L4)
> two silhouettes across a small bare table

```
two dark silhouettes facing each other across a small bare table, faces not visible, one hanging lamp between them, lit ONLY by that lamp which is switched on, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Houston, Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short251_21.png`  (body / L4)
> a bare metal table under a low hanging lamp

```
a bare metal table and two chairs under a single conical lamp hanging low in a tall bare room, lit ONLY by that lamp which is switched on and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Houston, Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short251_22.png`  (body / L4)
> painted steel cell bars, extreme close

```
extreme close-up of thick painted steel cell bars with a dark empty cell beyond, lit ONLY by one caged bulb which is switched on in the corridor behind and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Houston, Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

## short252 — fieldtest
*時代設定：2010 Houston, Texas* / 22 枚

### `short252_01.png`  (hook / L1)
> a wall of steel shelves packed with unlabelled folders

```
a wall of grey steel filing shelves packed with unlabelled folders shot straight on, every spine worn completely blank, lit ONLY by one flickering fluorescent tube which is switched on overhead and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Houston, Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short252_02.png`  (hook / L1)
> a records room aisle stacked to the ceiling

```
looking down the aisle of a deep records room, shelving stacked to the ceiling with unlabelled boxes, lit ONLY by one bulb which is switched on at the far end and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Houston, Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short252_03.png`  (hook / L1)
> a leaning tower of worn case folders

```
a leaning tower of worn case folders on a small desk, every label worn completely blank, lit ONLY by one desk lamp which is switched on beside it and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Houston, Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short252_04.png`  (hook / L1)
> an in-tray overflowing with blank forms

```
a metal in-tray overflowing with blank unreadable forms on a grey desk, lit ONLY by one fluorescent tube which is switched on above it and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Houston, Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short252_05.png`  (body / L2)
> a gavel caught mid-strike above its block

```
a wooden judge's gavel caught mid-strike above its round block with motion blur on the head, lit ONLY by one brass bench lamp which is switched on and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Houston, Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short252_06.png`  (body / L2)
> a thick file closed and tied with a band

```
a thick case file closed and tied with a band on a dark desk, its cover worn completely blank, lit ONLY by one desk lamp which is switched on and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Houston, Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short252_07.png`  (body / L2)
> a laboratory bench with a heavy instrument

```
a forensic laboratory bench with a heavy analytical instrument, every display dark and unreadable, nobody present, lit ONLY by one task lamp which is switched on and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Houston, Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short252_08.png`  (body / L2)
> a sealed evidence envelope on a steel counter

```
a sealed paper evidence envelope on a steel counter, all writing worn completely blank, lit ONLY by one hard overhead lamp which is switched on and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Houston, Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short252_09.png`  (body / L2)
> a hand pressing a pen to a blank sheet

```
macro of one hand pressing a pen to a completely blank unreadable sheet on a desk, no face or body visible, lit ONLY by a single desk lamp which is switched on and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Houston, Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short252_10.png`  (body / L2)
> a rubber stamp resting on an ink pad

```
macro of a wooden-handled rubber stamp resting on an ink pad, the die face worn completely smooth and unreadable, lit ONLY by one desk lamp which is switched on and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Houston, Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short252_11.png`  (body / L2)
> a window at first light over a desk of blank folders

```
an office window at first light with a desk buried in blank unlabelled folders silhouetted against it, lit ONLY by the pale dawn beyond the glass, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Houston, Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short252_12.png`  (body / L3)
> rows of empty courtroom gallery benches

```
rows of empty polished wooden courtroom gallery benches receding into shadow, lit ONLY by one shaft of light from a high window, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Houston, Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short252_13.png`  (body / L3)
> a judge's high bench from the floor, empty

```
a judge's high wooden bench photographed from the floor looking up, empty, no inscriptions anywhere, lit ONLY by one shaft of window light falling across its face, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Houston, Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short252_14.png`  (body / L3)
> a single empty chair in a cone of light

```
a single empty wooden chair standing in a cone of light in a large dark empty room, dust motes drifting around it, lit ONLY by the fixture which is switched on above it and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Houston, Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short252_15.png`  (body / L3)
> two weathered hands laid flat on a table

```
macro of two weathered hands laid flat on a scarred wooden table, no face or body above the wrists, lit ONLY by one hard overhead lamp which is switched on and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Houston, Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short252_16.png`  (body / L3)
> a shaft of light crossing an empty room, thick with dust

```
a shaft of light crossing an empty room thick with slowly drifting dust, nothing else in frame, lit ONLY by that shaft, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Houston, Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short252_17.png`  (body / L4)
> a cruiser fender and roof beacon, tight

```
tight low angle on the front fender and single roof beacon of a police cruiser parked at a kerb, chrome and dark paint filling the frame, no lettering on the bodywork, lit ONLY by that beacon which is switched on and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Houston, Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short252_18.png`  (body / L4)
> a car interior washed by beacons from behind

```
the interior of a parked car seen from the passenger side, empty seats, a red and blue wash crossing the dashboard from behind, no displays legible, lit ONLY by those beacons which are switched on, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Houston, Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short252_19.png`  (body / L4)
> handcuffs closing on a pair of wrists

```
macro of steel handcuffs closing on a pair of wrists, no face or body above the forearms, lit ONLY by one hard raking light which is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Houston, Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short252_20.png`  (body / L4)
> a booking tray of personal effects

```
a steel booking tray holding a belt, laces and a few coins on a counter, every label blank, lit ONLY by one hard overhead lamp which is switched on and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Houston, Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short252_21.png`  (body / L4)
> a cell block corridor of steel doors

```
a long cell block corridor of steel doors receding into the distance, all numbers worn blank, lit ONLY by a row of caged ceiling bulbs which are switched on and are the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Houston, Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short252_22.png`  (body / L4)
> cell bars in extreme close-up

```
extreme close-up of thick iron cell bars with a dark empty cell beyond, lit ONLY by one caged bulb which is switched on in the corridor behind and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Houston, Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

## short253 — lejeune
*時代設定：1981 coastal North Carolina* / 22 枚

### `short253_01.png`  (hook / L1)
> a hand writing in the remarks box of a blank form

```
macro of one hand pressing a ballpoint pen into the remarks box of a completely blank unreadable printed form on a laboratory bench, no face or body visible, lit ONLY by one desk lamp which is switched on and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1981 coastal North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short253_02.png`  (hook / L1)
> a laboratory bench of clear sample bottles

```
a laboratory bench with a row of clear glass sample bottles and a heavy analytical instrument behind them, every display dark and every label worn blank, lit ONLY by one task lamp which is switched on and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1981 coastal North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short253_03.png`  (hook / L1)
> a rubber stamp resting on an ink pad

```
macro of a wooden-handled rubber stamp resting on an ink pad on a laboratory desk, the die face worn completely smooth and unreadable, lit ONLY by one desk lamp which is switched on and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1981 coastal North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short253_04.png`  (hook / L1)
> a window at first light over a desk of blank folders

```
an office window at first light with a desk buried in blank unlabelled folders silhouetted against it, lit ONLY by the pale dawn beyond the glass, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1981 coastal North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short253_05.png`  (body / L2)
> a leaning tower of worn folders, labels blank

```
a leaning tower of worn folders on a small desk, every label worn completely blank, lit ONLY by one desk lamp which is switched on beside it and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1981 coastal North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short253_06.png`  (body / L2)
> a records room aisle of unlabelled boxes

```
looking down the aisle of a deep records room, shelving stacked to the ceiling with unlabelled boxes, lit ONLY by one bulb which is switched on at the far end and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1981 coastal North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short253_07.png`  (body / L2)
> a wall of grey steel filing shelves

```
a wall of grey steel filing shelves packed with unlabelled folders shot straight on, every spine worn blank, lit ONLY by one flickering fluorescent tube which is switched on overhead and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1981 coastal North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short253_08.png`  (body / L2)
> a thick file closed and tied with a band

```
a thick file closed and tied with a band on a dark desk, its cover worn completely blank, lit ONLY by one desk lamp which is switched on and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1981 coastal North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short253_09.png`  (body / L2)
> a shaft of light crossing an empty room, thick with dust

```
a shaft of light crossing an empty room thick with slowly drifting dust, nothing else in frame, lit ONLY by that shaft, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1981 coastal North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short253_10.png`  (body / L2)
> an in-tray overflowing with blank forms

```
a metal in-tray overflowing with blank unreadable forms on a grey steel desk, lit ONLY by one fluorescent tube which is switched on above it and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1981 coastal North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short253_11.png`  (body / L2)
> a blank-faced institutional wall clock

```
a plain round institutional wall clock with a completely blank featureless face and no numerals, hard side light across it, lit ONLY by one fixture which is switched on beside it and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1981 coastal North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short253_12.png`  (body / L3)
> one sealed water sample vial on a dark bench

```
macro of one sealed glass water sample vial standing on a dark laboratory bench, its label worn completely blank, lit ONLY by a single hard rim light which is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1981 coastal North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short253_13.png`  (body / L3)
> two hands laid flat on a laboratory bench

```
macro of two weathered hands laid flat on a scarred laboratory bench, no face or body above the wrists, lit ONLY by one hard overhead lamp which is switched on and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1981 coastal North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short253_14.png`  (body / L3)
> a heavy steel door closed on a brick pump house

```
a heavy steel door closed on a brick pump house, its dial and every marking worn smooth and unreadable, lit ONLY by one hard uplight which is switched on and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1981 coastal North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short253_15.png`  (body / L3)
> a water tower against a pale dawn sky

```
an industrial water tower silhouetted against a pale dawn sky with no lettering anywhere on the tank, lit ONLY by that dawn, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1981 coastal North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short253_16.png`  (body / L3)
> a single empty stool in a cone of light

```
a single empty wooden stool standing in a cone of light in a large dark empty laboratory, dust motes drifting around it, lit ONLY by the fixture which is switched on above it and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1981 coastal North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short253_17.png`  (body / L4)
> a screen door of family quarters from inside

```
a screen door of brick family quarters seen from inside a dim hallway, one hard blade of daylight under it, no numbers or lettering anywhere, lit ONLY by that light, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1981 coastal North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short253_18.png`  (body / L4)
> a walkway of identical doors along a housing block

```
a long exterior walkway of identical closed doors along a brick family housing block, all numbers and nameplates blank, lit ONLY by a row of bulkhead fixtures which are switched on and are the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1981 coastal North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short253_19.png`  (body / L4)
> a bare bulb burning over a kitchen sink

```
low angle looking up into a bare bulb burning over a kitchen sink through faint steam, the room beyond swallowed in black, lit ONLY by that bulb which is switched on and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1981 coastal North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short253_20.png`  (body / L4)
> two plain chairs facing each other in a dim room

```
two plain chairs turned to face each other across a bare floor in a small dim room, nobody in them, lit ONLY by one window shaft which is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1981 coastal North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short253_21.png`  (body / L4)
> a screen door swinging shut on a blade of light

```
a screen door swinging shut on a narrowing blade of daylight seen from inside a dark hallway, lit ONLY by that closing light, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1981 coastal North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short253_22.png`  (body / L4)
> a lone silhouette high in a shaft of light in a pump hall

```
a lone dark silhouette standing in a single vertical shaft of light in a vast dark pump hall, the figure placed high in frame with its head in the upper third and a long empty floor below it, face not visible, lit ONLY by that shaft, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1981 coastal North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

## short254 — lejeune
*時代設定：1997 North Carolina* / 22 枚

### `short254_01.png`  (hook / L1)
> a single empty chair in a cone of light

```
a single empty wooden chair standing in a cone of light in a large dark empty room, dust motes drifting around it, lit ONLY by the fixture which is switched on above it and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1997 North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short254_02.png`  (hook / L1)
> a shaft of light crossing an empty room, thick with dust

```
a shaft of light crossing an empty room thick with slowly drifting dust, nothing else in frame, lit ONLY by that shaft, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1997 North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short254_03.png`  (hook / L1)
> a kitchen window at first light over a bare table

```
a kitchen window at first light with a bare wooden table silhouetted against it, lit ONLY by the pale dawn beyond the glass, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1997 North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short254_04.png`  (hook / L1)
> a blank-faced kitchen wall clock

```
a plain round wall clock with a completely blank featureless face and no numerals hanging on a kitchen wall, hard side light across it, lit ONLY by one fixture which is switched on beside it and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1997 North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short254_05.png`  (body / L2)
> an empty tiered committee chamber

```
an empty tiered committee chamber with rows of vacant seats and a long bench, all nameplates blank, lit ONLY by one bank of overhead lights which are switched on and are the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1997 North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short254_06.png`  (body / L2)
> a government corridor of identical closed doors

```
a long government corridor of identical closed doors, all nameplates blank, lit ONLY by a row of ceiling fixtures which are switched on and are the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1997 North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short254_07.png`  (body / L2)
> an in-tray overflowing with blank forms

```
a metal in-tray overflowing with blank unreadable forms on a grey desk, lit ONLY by one fluorescent tube which is switched on above it and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1997 North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short254_08.png`  (body / L2)
> a leaning tower of worn folders on a desk

```
a leaning tower of worn folders on a small desk, every label worn completely blank, lit ONLY by one desk lamp which is switched on beside it and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1997 North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short254_09.png`  (body / L2)
> a long conference table with chairs pushed in

```
a long polished conference table with chairs pushed in and a dark panelled wall behind it, nobody present, no plaques or lettering anywhere, lit ONLY by one pendant which is switched on above the table, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1997 North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short254_10.png`  (body / L2)
> a rubber stamp resting on an ink pad

```
macro of a wooden-handled rubber stamp resting on an ink pad, the die face worn completely smooth and unreadable, lit ONLY by one desk lamp which is switched on and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1997 North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short254_11.png`  (body / L2)
> a wall of grey steel filing shelves

```
a wall of grey steel filing shelves packed with unlabelled folders shot straight on, every spine worn blank, lit ONLY by one flickering fluorescent tube which is switched on overhead and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1997 North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short254_12.png`  (body / L3)
> a screen door of base housing seen from inside

```
a screen door of brick family quarters seen from inside a dim hallway, one hard blade of daylight under it, no numbers or lettering anywhere, lit ONLY by that light, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1997 North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short254_13.png`  (body / L3)
> a door swinging shut on a blade of light

```
a heavy door swinging shut on a narrowing blade of light seen from inside a dark room, lit ONLY by that closing light, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1997 North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short254_14.png`  (body / L3)
> a water tower against a pale dawn sky

```
an industrial water tower silhouetted against a pale dawn sky with no lettering anywhere on the tank, lit ONLY by that dawn, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1997 North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short254_15.png`  (body / L3)
> a bare bulb burning over a kitchen sink

```
low angle looking up into a bare bulb burning over a kitchen sink, the room beyond swallowed in black, lit ONLY by that bulb which is switched on and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1997 North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short254_16.png`  (body / L3)
> two plain chairs facing each other in a dim room

```
two plain chairs turned to face each other across a bare floor in a small dim room, nobody in them, lit ONLY by one window shaft which is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1997 North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short254_17.png`  (body / L4)
> two weathered hands laid flat on a kitchen table

```
macro of two weathered hands laid flat on a scarred kitchen table, no face or body above the wrists, lit ONLY by one hard overhead lamp which is switched on and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1997 North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short254_18.png`  (body / L4)
> a lone silhouette high in a shaft of light in a drill hall

```
a lone dark silhouette standing in a single vertical shaft of light in a vast dark drill hall, the figure placed high in frame with its head in the upper third and a long empty floor below it, face not visible, lit ONLY by that shaft, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1997 North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short254_19.png`  (body / L4)
> a barracks corridor receding to a lit doorway

```
a long barracks corridor receding into darkness toward one brightly lit doorway at the far end, all nameplates blank, lit ONLY by that doorway, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1997 North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short254_20.png`  (body / L4)
> a steel tray of folded uniform effects

```
a steel tray holding a folded uniform belt, a plain cap and a few coins on a counter, all insignia and lettering absent, lit ONLY by one hard overhead lamp which is switched on and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1997 North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short254_21.png`  (body / L4)
> a hand pressing a pen to a blank request form

```
macro of one hand pressing a pen to a completely blank unreadable request form on a kitchen table, no face or body visible, lit ONLY by a single desk lamp which is switched on and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1997 North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short254_22.png`  (body / L4)
> a door opening onto blinding daylight

```
a heavy door swinging open onto blinding daylight seen from inside a dark room, lit ONLY by that daylight beyond, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1997 North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

## short255 — lejeune
*時代設定：2026 eastern North Carolina* / 22 枚

### `short255_01.png`  (hook / L1)
> a records aisle of unlabelled claim boxes

```
looking down the aisle of a deep records room, shelving stacked to the ceiling with unlabelled claim boxes, lit ONLY by one bulb which is switched on at the far end and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2026 eastern North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short255_02.png`  (hook / L1)
> a wall of steel shelves packed with unlabelled folders

```
a wall of grey steel filing shelves packed with unlabelled folders shot straight on, every spine worn blank, lit ONLY by one flickering fluorescent tube which is switched on overhead and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2026 eastern North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short255_03.png`  (hook / L1)
> claim forms fanned across a dark desk

```
printed claim forms fanned across a dark desk, every figure and heading worn completely blank, lit ONLY by one desk lamp which is switched on and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2026 eastern North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short255_04.png`  (hook / L1)
> a leaning tower of worn claim folders

```
a leaning tower of worn claim folders on a small desk, every label worn completely blank, lit ONLY by one desk lamp which is switched on beside it and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2026 eastern North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short255_05.png`  (body / L2)
> courthouse columns from directly below

```
tall marble courthouse columns photographed from directly below against a dark storm sky, no inscriptions anywhere, lit ONLY by hard uplights which are switched on at their bases, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2026 eastern North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short255_06.png`  (body / L2)
> an empty tiered committee chamber

```
an empty tiered committee chamber with rows of vacant seats and a long bench, all nameplates blank, lit ONLY by one bank of overhead lights which are switched on and are the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2026 eastern North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short255_07.png`  (body / L2)
> a long conference table with chairs pushed in

```
a long polished conference table with chairs pushed in and a dark panelled wall behind it, nobody present, no lettering anywhere, lit ONLY by one pendant which is switched on above the table, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2026 eastern North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short255_08.png`  (body / L2)
> a hand pressing a pen to a blank sheet

```
macro of one hand pressing a pen to a completely blank unreadable sheet, no face or body visible, lit ONLY by a single desk lamp which is switched on and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2026 eastern North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short255_09.png`  (body / L2)
> a rubber stamp resting on an ink pad

```
macro of a wooden-handled rubber stamp resting on an ink pad, the die face worn completely smooth and unreadable, lit ONLY by one desk lamp which is switched on and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2026 eastern North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short255_10.png`  (body / L2)
> a chain and padlock hanging loose and open on a door

```
a heavy door in a dim service corridor with a chain and padlock hanging loose and open from its bar, every notice worn blank, lit ONLY by one caged bulb which is switched on and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2026 eastern North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short255_11.png`  (body / L2)
> heavy doors swinging open onto blinding daylight

```
heavy doors swinging open onto blinding daylight seen from inside a dark room, no signage anywhere, lit ONLY by that daylight beyond, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2026 eastern North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short255_12.png`  (body / L3)
> a judge's high bench from the floor, empty

```
a judge's high wooden bench photographed from the floor looking up, empty, no inscriptions anywhere, lit ONLY by one shaft of window light falling across its face, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2026 eastern North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short255_13.png`  (body / L3)
> a single empty chair in a cone of light

```
a single empty wooden chair standing in a cone of light in a large dark empty room, dust motes drifting around it, lit ONLY by the fixture which is switched on above it and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2026 eastern North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short255_14.png`  (body / L3)
> two weathered hands laid flat on a table

```
macro of two weathered hands laid flat on a scarred wooden table, no face or body above the wrists, lit ONLY by one hard overhead lamp which is switched on and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2026 eastern North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short255_15.png`  (body / L3)
> a blank-faced institutional wall clock

```
a plain round institutional wall clock with a completely blank featureless face and no numerals, hard side light across it, lit ONLY by one fixture which is switched on beside it and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2026 eastern North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short255_16.png`  (body / L3)
> a shaft of light crossing an empty room, thick with dust

```
a shaft of light crossing an empty room thick with slowly drifting dust, nothing else in frame, lit ONLY by that shaft, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2026 eastern North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short255_17.png`  (body / L4)
> rows of empty courtroom gallery benches

```
rows of empty polished wooden courtroom gallery benches receding into shadow, lit ONLY by one shaft of light from a high window, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2026 eastern North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short255_18.png`  (body / L4)
> two plain chairs facing each other in a dim room

```
two plain chairs turned to face each other across a bare floor in a small dim room, nobody in them, lit ONLY by one window shaft which is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2026 eastern North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short255_19.png`  (body / L4)
> a gavel caught mid-strike above its block

```
a wooden judge's gavel caught mid-strike above its round block with motion blur on the head, lit ONLY by one brass bench lamp which is switched on and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2026 eastern North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short255_20.png`  (body / L4)
> a corridor of identical closed doors, nameplates blank

```
a long government corridor of identical closed doors, all nameplates blank, lit ONLY by a row of ceiling fixtures which are switched on and are the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2026 eastern North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short255_21.png`  (body / L4)
> a courthouse corridor receding to a lit doorway

```
a long courthouse corridor receding into darkness toward one brightly lit doorway at the far end, lit ONLY by that doorway, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2026 eastern North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short255_22.png`  (body / L4)
> a lone silhouette high in a shaft of light

```
a lone dark silhouette standing in a single vertical shaft of light in a vast dark hall, the figure placed high in frame with its head in the upper third and a long empty floor below it, face not visible, lit ONLY by that shaft, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2026 eastern North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

## short256 — robosigning
*時代設定：2010 Florida* / 22 枚

### `short256_01.png`  (hook / L1)
> a suburban front door from inside a dim hallway

```
a suburban front door seen from inside a dim hallway with one hard blade of daylight under it, no numbers or lettering anywhere, lit ONLY by that light, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Florida, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short256_02.png`  (hook / L1)
> a padlock and hasp screwed across a house door

```
macro of a heavy padlock and steel hasp screwed across a suburban front door, every notice taped beside it worn completely blank, lit ONLY by one porch fixture which is switched on and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Florida, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short256_03.png`  (hook / L1)
> banded cash standing on a closing table

```
banded stacks of cash standing on a dark closing table, the notes plain and their denominations completely illegible, lit ONLY by one desk lamp which is switched on and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Florida, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short256_04.png`  (hook / L1)
> a hand pressing a pen to a blank closing document

```
macro of one hand pressing a pen to a completely blank unreadable closing document, no face or body visible, lit ONLY by a single desk lamp which is switched on and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Florida, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short256_05.png`  (body / L2)
> a front door swinging shut on a blade of light

```
a front door swinging shut on a narrowing blade of daylight seen from inside a dark hallway, lit ONLY by that closing light, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Florida, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short256_06.png`  (body / L2)
> dust drifting in a shaft across an emptied living room

```
a shaft of light crossing an emptied living room thick with slowly drifting dust, nothing else in frame, lit ONLY by that shaft, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Florida, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short256_07.png`  (body / L2)
> a single chair left in a stripped room

```
a single empty wooden chair standing in a cone of light in a large stripped empty room, dust motes drifting around it, lit ONLY by the fixture which is switched on above it and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Florida, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short256_08.png`  (body / L2)
> a row of identical suburban front doors

```
a row of identical closed suburban front doors along a walkway, all house numbers blank, lit ONLY by a row of porch fixtures which are switched on and are the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Florida, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short256_09.png`  (body / L2)
> a garage door standing open onto flat daylight

```
a garage door standing open onto flat daylight seen from inside the dark garage, no lettering anywhere, lit ONLY by that daylight, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Florida, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short256_10.png`  (body / L2)
> a blank-faced clock on a bare wall

```
a plain round wall clock with a completely blank featureless face and no numerals hanging on a bare stripped wall, lit ONLY by one fixture which is switched on beside it and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Florida, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short256_11.png`  (body / L2)
> an empty hallway receding to a lit doorway

```
an empty domestic hallway receding into darkness toward one brightly lit doorway at the far end, lit ONLY by that doorway, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Florida, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short256_12.png`  (body / L3)
> a phone lying face down on a kitchen counter

```
a telephone lying face down on a dark kitchen counter, its edge catching one hard light, screen not visible, lit ONLY by a single under-cabinet lamp which is switched on and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Florida, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short256_13.png`  (body / L3)
> two hands laid flat on a kitchen table

```
macro of two weathered hands laid flat on a scarred kitchen table, no face or body above the wrists, lit ONLY by one hard overhead lamp which is switched on and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Florida, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short256_14.png`  (body / L3)
> two plain chairs facing each other in an empty room

```
two plain chairs turned to face each other across a bare floor in a small empty room, nobody in them, lit ONLY by one window shaft which is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Florida, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short256_15.png`  (body / L3)
> a lone silhouette high in a shaft of light in a bare room

```
a lone dark silhouette standing in a single vertical shaft of light in a bare stripped room, the figure placed high in frame with its head in the upper third and a long empty floor below it, face not visible, lit ONLY by that shaft, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Florida, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short256_16.png`  (body / L3)
> a long table with chairs pushed in, nobody present

```
a long polished table with chairs pushed in and a dark wall behind it, nobody present, no lettering anywhere, lit ONLY by one pendant which is switched on above the table, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Florida, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short256_17.png`  (body / L4)
> a bare lamp burning into camera through faint dust

```
low angle looking up into a bare conical lamp burning straight into camera through faint dust, the room beyond swallowed in black, lit ONLY by that lamp which is switched on and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Florida, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short256_18.png`  (body / L4)
> an in-tray overflowing with blank forms

```
a metal in-tray overflowing with blank unreadable forms on a grey desk, lit ONLY by one fluorescent tube which is switched on above it and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Florida, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short256_19.png`  (body / L4)
> a leaning tower of worn folders, labels blank

```
a leaning tower of worn folders on a small desk, every label worn completely blank, lit ONLY by one desk lamp which is switched on beside it and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Florida, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short256_20.png`  (body / L4)
> a rubber stamp resting on an ink pad

```
macro of a wooden-handled rubber stamp resting on an ink pad, the die face worn completely smooth and unreadable, lit ONLY by one desk lamp which is switched on and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Florida, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short256_21.png`  (body / L4)
> an office window at first light over a stacked desk

```
an office window at first light with a desk buried in blank unlabelled folders silhouetted against it, lit ONLY by the pale dawn beyond the glass, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Florida, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short256_22.png`  (body / L4)
> heavy doors swinging open onto blinding daylight

```
heavy doors swinging open onto blinding daylight seen from inside a dark room, no signage anywhere, lit ONLY by that daylight beyond, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Florida, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

## short257 — robosigning
*時代設定：2009 Pennsylvania* / 22 枚

### `short257_01.png`  (hook / L1)
> a hand mid-signature over a blank sheet

```
macro of one hand pressing a pen to a completely blank unreadable sheet, no face or body visible, lit ONLY by a single desk lamp which is switched on and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2009 Pennsylvania, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short257_02.png`  (hook / L1)
> an in-tray overflowing with blank forms

```
a metal in-tray overflowing with blank unreadable forms on a grey desk, lit ONLY by one fluorescent tube which is switched on above it and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2009 Pennsylvania, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short257_03.png`  (hook / L1)
> a leaning stack of unread folders on a desk

```
a leaning tower of worn folders on a small desk, every label worn completely blank, lit ONLY by one desk lamp which is switched on beside it and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2009 Pennsylvania, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short257_04.png`  (hook / L1)
> a bare lamp burning into camera over a desk

```
low angle looking up into a bare conical lamp burning straight into camera above a desk, the room beyond swallowed in black, lit ONLY by that lamp which is switched on and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2009 Pennsylvania, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short257_05.png`  (body / L2)
> a judge's high bench from the floor, empty

```
a judge's high wooden bench photographed from the floor looking up, empty, no inscriptions anywhere, lit ONLY by one shaft of window light falling across its face, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2009 Pennsylvania, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short257_06.png`  (body / L2)
> rows of empty courtroom gallery benches

```
rows of empty polished wooden courtroom gallery benches receding into shadow, lit ONLY by one shaft of light from a high window, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2009 Pennsylvania, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short257_07.png`  (body / L2)
> a gavel caught mid-strike above its block

```
a wooden judge's gavel caught mid-strike above its round block with motion blur on the head, lit ONLY by one brass bench lamp which is switched on and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2009 Pennsylvania, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short257_08.png`  (body / L2)
> a rubber stamp resting on an ink pad

```
macro of a wooden-handled rubber stamp resting on an ink pad, the die face worn completely smooth and unreadable, lit ONLY by one desk lamp which is switched on and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2009 Pennsylvania, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short257_09.png`  (body / L2)
> a single empty chair in a cone of light

```
a single empty wooden chair standing in a cone of light in a large dark empty room, dust motes drifting around it, lit ONLY by the fixture which is switched on above it and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2009 Pennsylvania, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short257_10.png`  (body / L2)
> a blank-faced institutional wall clock

```
a plain round institutional wall clock with a completely blank featureless face and no numerals, hard side light across it, lit ONLY by one fixture which is switched on beside it and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2009 Pennsylvania, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short257_11.png`  (body / L2)
> courtroom doors opening onto flat daylight

```
heavy courtroom doors swinging open onto flat daylight seen from inside a dark room, no signage anywhere, lit ONLY by that daylight beyond, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2009 Pennsylvania, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short257_12.png`  (body / L3)
> two hands laid flat on a wooden table

```
macro of two weathered hands laid flat on a scarred wooden table, no face or body above the wrists, lit ONLY by one hard overhead lamp which is switched on and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2009 Pennsylvania, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short257_13.png`  (body / L3)
> two plain chairs facing each other in a small room

```
two plain chairs turned to face each other across a bare floor in a small dim room, nobody in them, lit ONLY by one window shaft which is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2009 Pennsylvania, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short257_14.png`  (body / L3)
> a shaft of light crossing an empty hearing room

```
a shaft of light crossing an empty hearing room thick with slowly drifting dust, nothing else in frame, lit ONLY by that shaft, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2009 Pennsylvania, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short257_15.png`  (body / L3)
> a lone silhouette high in a shaft of light

```
a lone dark silhouette standing in a single vertical shaft of light in a vast dark hall, the figure placed high in frame with its head in the upper third and a long empty floor below it, face not visible, lit ONLY by that shaft, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2009 Pennsylvania, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short257_16.png`  (body / L3)
> a long conference table with chairs pushed in

```
a long polished conference table with chairs pushed in and a dark panelled wall behind it, nobody present, no lettering anywhere, lit ONLY by one pendant which is switched on above the table, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2009 Pennsylvania, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short257_17.png`  (body / L4)
> two silhouettes across a small bare table

```
two dark silhouettes facing each other across a small bare table, faces not visible, one hanging lamp between them, lit ONLY by that lamp which is switched on, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2009 Pennsylvania, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short257_18.png`  (body / L4)
> a bare table and two chairs under a hanging lamp

```
a bare table and two chairs under a single conical lamp hanging low in a tall bare room, lit ONLY by that lamp which is switched on and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2009 Pennsylvania, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short257_19.png`  (body / L4)
> a phone lying face down on a table

```
a telephone lying face down on a dark table, its edge catching one hard light, screen not visible, lit ONLY by a single desk lamp which is switched on and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2009 Pennsylvania, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short257_20.png`  (body / L4)
> documents fanned across a dark desk, figures blank

```
printed documents fanned across a dark desk, every figure and heading worn completely blank, lit ONLY by one desk lamp which is switched on and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2009 Pennsylvania, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short257_21.png`  (body / L4)
> an office window at first light over a stacked desk

```
an office window at first light with a desk buried in blank unlabelled folders silhouetted against it, lit ONLY by the pale dawn beyond the glass, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2009 Pennsylvania, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short257_22.png`  (body / L4)
> a wall of grey steel filing shelves

```
a wall of grey steel filing shelves packed with unlabelled folders shot straight on, every spine worn blank, lit ONLY by one flickering fluorescent tube which is switched on overhead and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2009 Pennsylvania, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

## short258 — robosigning
*時代設定：2010 Georgia* / 22 枚

### `short258_01.png`  (hook / L1)
> a wall of steel shelves packed with unlabelled boxes

```
a wall of grey steel shelves packed with unlabelled document boxes shot straight on, every box face worn completely blank, lit ONLY by one flickering fluorescent tube which is switched on overhead and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Georgia, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short258_02.png`  (hook / L1)
> a deep records aisle stacked to the ceiling

```
looking down the aisle of a deep records room, shelving stacked to the ceiling with unlabelled boxes, lit ONLY by one bulb which is switched on at the far end and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Georgia, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short258_03.png`  (hook / L1)
> documents fanned across a dark desk, headings blank

```
printed documents fanned across a dark desk, every heading and figure worn completely blank, lit ONLY by one desk lamp which is switched on and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Georgia, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short258_04.png`  (hook / L1)
> a bare lamp burning into camera over a signing desk

```
low angle looking up into a bare conical lamp burning straight into camera above a signing desk, the room beyond swallowed in black, lit ONLY by that lamp which is switched on and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Georgia, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short258_05.png`  (body / L2)
> rows of empty desks in a low office suite

```
rows of empty desks in a long low office suite, every screen dark and every surface unlabelled, nobody present, lit ONLY by one bank of ceiling fixtures which are switched on and are the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Georgia, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short258_06.png`  (body / L2)
> a leaning tower of unlabelled folders on a desk

```
a leaning tower of folders on a small desk, every label worn completely blank, lit ONLY by one desk lamp which is switched on beside it and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Georgia, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short258_07.png`  (body / L2)
> an in-tray overflowing with blank forms

```
a metal in-tray overflowing with blank unreadable forms on a grey desk, lit ONLY by one fluorescent tube which is switched on above it and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Georgia, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short258_08.png`  (body / L2)
> two weathered hands laid flat on a work bench

```
macro of two weathered hands laid flat on a scarred work bench, no face or body above the wrists, lit ONLY by one hard overhead lamp which is switched on and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Georgia, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short258_09.png`  (body / L2)
> a low-rise office block in an industrial park at dawn

```
a low-rise office block in an industrial park silhouetted against a pale dawn sky, no signage or lettering anywhere on the building, lit ONLY by that dawn, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Georgia, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short258_10.png`  (body / L2)
> an office window at first light over a stacked desk

```
an office window at first light with a desk buried in blank unlabelled paper silhouetted against it, lit ONLY by the pale dawn beyond the glass, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Georgia, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short258_11.png`  (body / L2)
> a long table with chairs pushed in, nobody present

```
a long polished table with chairs pushed in and a dark wall behind it, nobody present, no lettering anywhere, lit ONLY by one pendant which is switched on above the table, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Georgia, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short258_12.png`  (body / L3)
> a hand mid-signature over a blank sheet

```
macro of one hand pressing a pen to a completely blank unreadable sheet, no face or body visible, lit ONLY by a single desk lamp which is switched on and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Georgia, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short258_13.png`  (body / L3)
> a rubber stamp resting on an ink pad, die worn smooth

```
macro of a wooden-handled rubber stamp resting on an ink pad, the die face worn completely smooth and unreadable, lit ONLY by one desk lamp which is switched on and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Georgia, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short258_14.png`  (body / L3)
> a shaft of light crossing an empty signing room

```
a shaft of light crossing an empty signing room thick with slowly drifting dust, nothing else in frame, lit ONLY by that shaft, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Georgia, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short258_15.png`  (body / L3)
> a blank-faced clock above rows of desks

```
a plain round wall clock with a completely blank featureless face and no numerals mounted above rows of empty desks, lit ONLY by one fixture which is switched on beside it and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Georgia, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short258_16.png`  (body / L3)
> a single empty chair beside a paper trolley

```
a single empty office chair standing in a cone of light beside a loaded paper trolley in a large dark room, every sheet blank, lit ONLY by the fixture which is switched on above it and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Georgia, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short258_17.png`  (body / L4)
> one ballpoint pen standing upright on a dark desk

```
macro of one ballpoint pen standing upright on a dark desk, the frame shallow and dark all around it, lit ONLY by a single hard rim light which is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Georgia, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short258_18.png`  (body / L4)
> a corridor of desks receding to a lit doorway

```
a long room of desks receding into darkness toward one brightly lit doorway at the far end, lit ONLY by that doorway, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Georgia, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short258_19.png`  (body / L4)
> a pay envelope and a few notes on a desk

```
a small unmarked pay envelope and a few plain notes lying on a dark desk, denominations completely illegible, lit ONLY by one desk lamp which is switched on and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Georgia, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short258_20.png`  (body / L4)
> a lone silhouette high in a shaft of light in a warehouse office

```
a lone dark silhouette standing in a single vertical shaft of light in a vast dark warehouse office, the figure placed high in frame with its head in the upper third and a long empty floor below it, face not visible, lit ONLY by that shaft, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Georgia, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short258_21.png`  (body / L4)
> a phone lying face down beside a stack of paper

```
a telephone lying face down beside a stack of blank paper on a dark desk, screen not visible, lit ONLY by a single desk lamp which is switched on and is the only light in frame, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Georgia, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short258_22.png`  (body / L4)
> loading doors swinging open onto blinding daylight

```
heavy loading doors swinging open onto blinding daylight seen from inside a dark room, no signage anywhere, lit ONLY by that daylight beyond, the subject held between y560 and y1180 of the 1080x1920 frame with the top band y0-560 and the caption band y1210-1430 kept empty and quiet, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Georgia, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```
