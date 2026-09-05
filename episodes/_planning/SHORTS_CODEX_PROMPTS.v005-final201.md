# Codex 縦型画像プロンプト v005-final201

**201 枚** / 29 本のショート / 14 話ぶん。

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
*時代設定：1980s New Jersey* / 5 枚

### `short182_31.png`  (body / L6)
> what a school keeps locked

```
padlock and chain on metal door, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1980s New Jersey, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short182_34.png`  (body / L6)
> the ruling that followed

```
wooden gavel resting on a bench, no face or likeness visible, lit ONLY by one laboratory bench task light which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1980s New Jersey, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short182_36.png`  (body / L7)
> an ordinary room in an ordinary school

```
empty school laboratory bench daytime, no face or likeness visible, lit ONLY by one laboratory bench task light which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1980s New Jersey, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short182_37.png`  (body / L7)
> one drawer, then the next

```
metal drawer pulled open on a desk, no face or likeness visible, lit ONLY by one desk lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1980s New Jersey, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short182_40.png`  (body / L7)
> the door at the end of the day

```
open door at end of hallway, no face or likeness visible, lit ONLY by one overhead fluorescent tube which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1980s New Jersey, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

## short183 — tlo
*時代設定：1980s New Jersey* / 2 枚

### `short183_37.png`  (body / L7)
> the bag itself

```
student backpack on a bench, no face or likeness visible, lit ONLY by one laboratory bench task light which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1980s New Jersey, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short183_40.png`  (body / L7)
> the yard outside the rule

```
students crossing a schoolyard in daylight, no face or likeness visible, lit ONLY by hard low afternoon sunlight which is the only light in frame, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1980s New Jersey, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

## short186 — willingham
*時代設定：1991 Texas* / 2 枚

### `short186_31.png`  (body / L6)
> the water that hit the glass

```
water spraying from a fire hose, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1991 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short186_34.png`  (body / L6)
> hands on the nozzle

```
gloved hands holding a nozzle, no face or likeness visible, lit ONLY by one caged ceiling bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1991 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

## short187 — willingham
*時代設定：2009 Texas* / 1 枚

### `short187_40.png`  (body / L7)
> where the case is kept now

```
row of filing cabinets in an office, no face or likeness visible, lit ONLY by one desk lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2009 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

## short188 — morton
*時代設定：1986 Texas* / 3 枚

### `short188_27.png`  (body / L5)
> the hallway of an ordinary house

```
hallway of a suburban house daytime, no face or likeness visible, lit ONLY by one overhead fluorescent tube which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1986 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short188_34.png`  (body / L6)
> the back of the store

```
loading dock door of a supermarket, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1986 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short188_37.png`  (body / L7)
> the car searched in the driveway

```
hands closing the boot of a car, no face or likeness visible, lit ONLY by the car's own interior light which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1986 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

## short189 — morton
*時代設定：2011 Texas* / 3 枚

### `short189_30.png`  (body / L5)
> the case carried in and out

```
briefcase on an office chair, no face or likeness visible, lit ONLY by one desk lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2011 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short189_32.png`  (body / L6)
> the corridor the objections ran down

```
corridor of a county courthouse daytime, no face or likeness visible, lit ONLY by one overhead fluorescent tube which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2011 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short189_40.png`  (body / L7)
> one strip of blue cloth

```
blue cloth folded on a steel tray, no face or likeness visible, lit ONLY by one desk lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2011 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

## short190 — carsearch
*時代設定：1925 America* / 3 枚

### `short190_28.png`  (body / L5)
> the call that was never made

```
smartphone face down on table, no face or likeness visible, lit ONLY by one kitchen ceiling light which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1925 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short190_30.png`  (body / L5)
> one blank sheet left on the ground

```
single sheet of paper on floor, no face or likeness visible, lit ONLY by one desk lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1925 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short190_35.png`  (body / L6)
> the pages nobody read again

```
hands resting on a paper stack, no face or likeness visible, lit ONLY by one desk lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1925 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

## short191 — carsearch
*時代設定：present-day America* / 2 枚

### `short191_26.png`  (body / L5)
> the air inside a stopped car

```
sunlight through a car windscreen, no face or likeness visible, lit ONLY by the car's own interior light which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, present-day America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short191_38.png`  (body / L7)
> a driver walking away from the stop

```
person walking away on a roadside, no face or likeness visible, lit ONLY by the car's own interior light which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, present-day America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

## short192 — tyler
*時代設定：medieval England* / 3 枚

### `short192_29.png`  (body / L5)
> a hand set down beside the book

```
hand resting on a closed book, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, medieval England, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short192_35.png`  (body / L6)
> one sheet on the floor of a hall

```
sheet of paper on a stone floor, no face or likeness visible, lit ONLY by one desk lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, medieval England, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short192_38.png`  (body / L7)
> a counter of small personal things

```
coins and keys on a counter, no face or likeness visible, lit ONLY by one desk lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, medieval England, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

## short193 — tyler
*時代設定：2020 Minneapolis* / 6 枚

### `short193_27.png`  (body / L5)
> the table where the loan ended

```
empty table with two chairs, no face or likeness visible, lit ONLY by one kitchen ceiling light which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2020 Minneapolis, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short193_28.png`  (body / L5)
> a hallway to a lit apartment door

```
apartment hallway with a lit door, no face or likeness visible, lit ONLY by one overhead fluorescent tube which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2020 Minneapolis, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short193_30.png`  (body / L5)
> someone leaving a building into daylight

```
person walking out of a building, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2020 Minneapolis, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short193_34.png`  (body / L6)
> a gavel resting on its block

```
gavel resting on a wooden block, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2020 Minneapolis, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short193_35.png`  (body / L6)
> an aisle of records boxes

```
aisle of archive storage boxes, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2020 Minneapolis, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short193_36.png`  (body / L7)
> an empty appellate bench

```
empty judges bench in courtroom, no face or likeness visible, lit ONLY by one laboratory bench task light which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2020 Minneapolis, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

## short194 — rolin
*時代設定：2020 America* / 9 枚

### `short194_26.png`  (body / L5)
> the low bar and the high one

```
balance scales on a desk, no face or likeness visible, lit ONLY by one desk lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2020 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short194_28.png`  (body / L5)
> a door closing on the hearing

```
heavy door closing slowly, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2020 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short194_30.png`  (body / L5)
> one blank sheet left on the floor

```
blank paper on a tiled floor, no face or likeness visible, lit ONLY by one desk lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2020 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short194_31.png`  (body / L6)
> the drawer the proceeds go into

```
metal drawer sliding open, no face or likeness visible, lit ONLY by one desk lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2020 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short194_35.png`  (body / L6)
> the vehicle the proceeds paid for

```
police vehicle parked at a kerb, no face or likeness visible, lit ONLY by the car's own interior light which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2020 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short194_37.png`  (body / L7)
> the tray of requisitions

```
office tray stacked with folders, no face or likeness visible, lit ONLY by one desk lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2020 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short194_38.png`  (body / L7)
> the room where the budget is set

```
empty boardroom with long table, no face or likeness visible, lit ONLY by one kitchen ceiling light which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2020 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short194_39.png`  (body / L7)
> the store room, padlocked

```
padlocked chain on a metal door, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2020 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short194_40.png`  (body / L7)
> someone leaving through a bright doorway

```
person exits through a bright doorway, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2020 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

## short195 — rolin
*時代設定：2019 America* / 9 枚

### `short195_26.png`  (body / L5)
> a terminal window at first light

```
airport window in morning light, no face or likeness visible, lit ONLY by daylight through that window, the only light in frame, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2019 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short195_31.png`  (body / L6)
> an office door chained shut

```
chain and padlock on office door, no face or likeness visible, lit ONLY by one desk lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2019 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short195_32.png`  (body / L6)
> a blank sheet on an office floor

```
paper on the floor of an office, no face or likeness visible, lit ONLY by one desk lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2019 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short195_33.png`  (body / L6)
> an empty briefing room

```
empty meeting room chairs and table, no face or likeness visible, lit ONLY by one kitchen ceiling light which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2019 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short195_35.png`  (body / L6)
> doors opening onto daylight

```
doors opening onto a bright street, no face or likeness visible, lit ONLY by one sodium streetlight which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2019 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short195_36.png`  (body / L7)
> handcuffs on a counter

```
handcuffs lying on a table, no face or likeness visible, lit ONLY by one desk lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2019 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short195_37.png`  (body / L7)
> a single key on a steel counter

```
single key on a metal counter, no face or likeness visible, lit ONLY by one desk lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2019 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short195_39.png`  (body / L7)
> the hearing room where it was asked

```
empty hearing room with seats, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2019 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short195_40.png`  (body / L7)
> the gallery that never filled

```
rows of empty wooden pews, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2019 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

## short196 — hinders
*時代設定：2015 rural North Carolina* / 8 枚

### `short196_26.png`  (body / L5)
> doors opening onto daylight

```
double doors open to daylight, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2015 rural North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short196_28.png`  (body / L5)
> the table where it was signed

```
empty table in a bright room, no face or likeness visible, lit ONLY by one kitchen ceiling light which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2015 rural North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short196_29.png`  (body / L5)
> the things handed back

```
personal belongings on a counter, no face or likeness visible, lit ONLY by one desk lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2015 rural North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short196_30.png`  (body / L5)
> walking out with it settled

```
man walking out of a building, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2015 rural North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short196_33.png`  (body / L6)
> the tray where it was filed away

```
documents stacked in an office tray, no face or likeness visible, lit ONLY by one desk lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2015 rural North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short196_34.png`  (body / L6)
> a single blank sheet on the floor

```
single sheet on an office floor, no face or likeness visible, lit ONLY by one desk lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2015 rural North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short196_38.png`  (body / L7)
> a chamber of empty seats

```
tiered chamber with empty seats, no face or likeness visible, lit ONLY by one overhead fluorescent tube which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2015 rural North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short196_40.png`  (body / L7)
> the corridor she left down

```
empty corridor with tiled floor, no face or likeness visible, lit ONLY by one overhead fluorescent tube which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2015 rural North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

## short197 — hinders
*時代設定：2015 America* / 8 枚

### `short197_27.png`  (body / L5)
> a phone face down beside it

```
phone face down on a desk, no face or likeness visible, lit ONLY by one desk lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2015 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short197_31.png`  (body / L6)
> an empty committee chamber

```
empty committee room with seats, no face or likeness visible, lit ONLY by one overhead fluorescent tube which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2015 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short197_33.png`  (body / L6)
> doors opening on daylight

```
glass doors opening to a street, no face or likeness visible, lit ONLY by one sodium streetlight which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2015 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short197_35.png`  (body / L6)
> a floor of dark desks after hours

```
empty office cubicles overhead view, no face or likeness visible, lit ONLY by one desk lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2015 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short197_36.png`  (body / L7)
> someone walking away down a hallway

```
person walking down a hallway away, no face or likeness visible, lit ONLY by one overhead fluorescent tube which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2015 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short197_37.png`  (body / L7)
> the table where the questions happen

```
table and chairs in a bare room, no face or likeness visible, lit ONLY by one kitchen ceiling light which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2015 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short197_39.png`  (body / L7)
> a room with a rail and a gate

```
wooden railing inside a hall, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2015 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short197_40.png`  (body / L7)
> a grain elevator against a pale sky

```
grain silo against a pale sky, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2015 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

## short200 — norfolk
*時代設定：1997 Norfolk Virginia* / 12 枚

### `short200_26.png`  (body / L5)
> the months between exclusion and exclusion

```
wall calendar pages turning on desk, no face or likeness visible, lit ONLY by one desk lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1997 Norfolk Virginia, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short200_27.png`  (body / L5)
> the laboratory finishing its arithmetic

```
rubber stamp pressed onto ink pad, no face or likeness visible, lit ONLY by one desk lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1997 Norfolk Virginia, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short200_29.png`  (body / L5)
> the court that kept the charges alive

```
empty wooden judge bench in courtroom, no face or likeness visible, lit ONLY by one laboratory bench task light which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1997 Norfolk Virginia, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short200_31.png`  (body / L6)
> a letter leaving a prison cell

```
hand pushing open heavy metal door, no face or likeness visible, lit ONLY by one caged ceiling bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1997 Norfolk Virginia, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short200_32.png`  (body / L6)
> the envelope that reached the police

```
thick paper folder tied with string, no face or likeness visible, lit ONLY by one desk lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1997 Norfolk Virginia, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short200_33.png`  (body / L6)
> the only man whose DNA was there

```
steel tray with keys and coins, no face or likeness visible, lit ONLY by one desk lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1997 Norfolk Virginia, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short200_34.png`  (body / L6)
> the prison the letter came from

```
long prison corridor with cell doors, no face or likeness visible, lit ONLY by one caged ceiling bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1997 Norfolk Virginia, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short200_35.png`  (body / L6)
> the offices the letter passed through

```
office corridor lined with closed doors, no face or likeness visible, lit ONLY by one overhead fluorescent tube which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1997 Norfolk Virginia, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short200_36.png`  (body / L7)
> the plea the state accepted anyway

```
wooden gavel resting on its block, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1997 Norfolk Virginia, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short200_37.png`  (body / L7)
> the theory enlarged instead of dropped

```
rows of empty seats in chamber, no face or likeness visible, lit ONLY by one overhead fluorescent tube which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1997 Norfolk Virginia, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short200_39.png`  (body / L7)
> the pardons, seventeen years later

```
metal gate sliding open in daylight, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1997 Norfolk Virginia, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short200_40.png`  (body / L7)
> four men walking out innocent

```
person walking away down bright corridor, no face or likeness visible, lit ONLY by one overhead fluorescent tube which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1997 Norfolk Virginia, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

## short201 — flowers
*時代設定：1996 to 2010 Winona Mississippi* / 11 枚

### `short201_26.png`  (body / L5)
> the courtroom where the strikes were made

```
gavel struck on a wooden bench, no face or likeness visible, lit ONLY by one laboratory bench task light which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1996 to 2010 Winona Mississippi, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short201_27.png`  (body / L5)
> the questions asked of each juror

```
empty tiered seats in meeting hall, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1996 to 2010 Winona Mississippi, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short201_28.png`  (body / L5)
> the same answers, different outcomes

```
two empty chairs facing each other, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1996 to 2010 Winona Mississippi, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short201_29.png`  (body / L5)
> a juror sent home

```
heavy door swinging shut in hallway, no face or likeness visible, lit ONLY by one overhead fluorescent tube which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1996 to 2010 Winona Mississippi, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short201_31.png`  (body / L6)
> the room where selection happens

```
bare table and two metal chairs, no face or likeness visible, lit ONLY by one kitchen ceiling light which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1996 to 2010 Winona Mississippi, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short201_33.png`  (body / L6)
> what a defendant hands over

```
personal belongings laid on metal counter, no face or likeness visible, lit ONLY by one desk lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1996 to 2010 Winona Mississippi, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short201_35.png`  (body / L6)
> the district beyond the courthouse

```
doors opening onto a bright street, no face or likeness visible, lit ONLY by one overhead fluorescent tube which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1996 to 2010 Winona Mississippi, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short201_36.png`  (body / L7)
> a small-town prosecution

```
patrol car parked outside a courthouse, no face or likeness visible, lit ONLY by one overhead fluorescent tube which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1996 to 2010 Winona Mississippi, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short201_38.png`  (body / L7)
> the pattern nobody stopped

```
man walking away toward bright doorway, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1996 to 2010 Winona Mississippi, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short201_39.png`  (body / L7)
> another county, same storeroom

```
water tower against a pale sky, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1996 to 2010 Winona Mississippi, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short201_40.png`  (body / L7)
> the towns the count has not reached

```
slow river bank in evening light, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1996 to 2010 Winona Mississippi, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

## short202 — burge
*時代設定：1973 to 2011 Chicago* / 10 枚

### `short202_26.png`  (body / L5)
> the special prosecutors' inquiry

```
empty public hearing room wooden seats, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1973 to 2011 Chicago, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short202_27.png`  (body / L5)
> the trial that could not begin

```
courtroom benches empty in daytime light, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1973 to 2011 Chicago, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short202_28.png`  (body / L5)
> the finding with nowhere to go

```
high wooden bench seen from below, no face or likeness visible, lit ONLY by one laboratory bench task light which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1973 to 2011 Chicago, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short202_29.png`  (body / L5)
> one hundred and forty-eight claims

```
police lineup room with plain wall, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1973 to 2011 Chicago, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short202_31.png`  (body / L6)
> proof beyond a reasonable doubt

```
gavel lifted above a wooden block, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1973 to 2011 Chicago, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short202_32.png`  (body / L6)
> what a conviction would have taken

```
belt and laces in booking tray, no face or likeness visible, lit ONLY by one desk lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1973 to 2011 Chicago, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short202_33.png`  (body / L6)
> the men still inside on those confessions

```
small cell with a high window, no face or likeness visible, lit ONLY by one caged ceiling bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1973 to 2011 Chicago, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short202_34.png`  (body / L6)
> the cases that stayed standing

```
iron doors along a cell block, no face or likeness visible, lit ONLY by one caged ceiling bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1973 to 2011 Chicago, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short202_37.png`  (body / L7)
> the belief, arriving late

```
heavy doors opening onto white daylight, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1973 to 2011 Chicago, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short202_38.png`  (body / L7)
> four men off death row

```
prison gate standing open in daylight, no face or likeness visible, lit ONLY by one caged ceiling bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1973 to 2011 Chicago, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

## short203 — postoffice
*時代設定：2000s England* / 10 枚

### `short203_26.png`  (body / L5)
> the contract nobody had dwelt on

```
shelves of box files in storeroom, no face or likeness visible, lit ONLY by one desk lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2000s England, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short203_27.png`  (body / L5)
> the terms they had signed

```
long empty table in meeting room, no face or likeness visible, lit ONLY by one kitchen ceiling light which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2000s England, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short203_30.png`  (body / L5)
> the house they remortgaged

```
front door of a terraced house, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2000s England, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short203_32.png`  (body / L6)
> driving to the branch in the morning

```
car parked outside a village shop, no face or likeness visible, lit ONLY by the car's own interior light which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2000s England, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short203_33.png`  (body / L6)
> savings, gone

```
empty metal drawer pulled open, no face or likeness visible, lit ONLY by one desk lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2000s England, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short203_34.png`  (body / L6)
> one village among thousands

```
water tower above a village skyline, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2000s England, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short203_35.png`  (body / L6)
> the coast where one of them began

```
seaside promenade railing in flat light, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2000s England, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short203_36.png`  (body / L7)
> the hall he hired

```
rows of folding chairs in hall, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2000s England, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short203_38.png`  (body / L7)
> strangers arriving

```
people walking into a village hall, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2000s England, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short203_40.png`  (body / L7)
> a room that was not empty after all

```
coat left hanging over a chair, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2000s England, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

## short204 — postoffice
*時代設定：1999 to 2015 England* / 13 枚

### `short204_26.png`  (body / L5)
> the bench that took the plea

```
empty judge seat behind wooden bench, no face or likeness visible, lit ONLY by one laboratory bench task light which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1999 to 2015 England, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short204_27.png`  (body / L5)
> the sentence that followed

```
gavel and block on a desk, no face or likeness visible, lit ONLY by one desk lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1999 to 2015 England, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short204_28.png`  (body / L5)
> the conversation with a solicitor

```
chairs facing across a small room, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1999 to 2015 England, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short204_29.png`  (body / L5)
> the shortfall repaid

```
hand smoothing a blank sheet flat, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1999 to 2015 England, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short204_31.png`  (body / L6)
> the investigators' own file

```
wire tray piled with plain envelopes, no face or likeness visible, lit ONLY by one desk lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1999 to 2015 England, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short204_32.png`  (body / L6)
> the report that said no evidence

```
storage room with boxes on shelves, no face or likeness visible, lit ONLY by one desk lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1999 to 2015 England, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short204_33.png`  (body / L6)
> the branch that was audited

```
daylight through a window onto desk, no face or likeness visible, lit ONLY by one desk lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1999 to 2015 England, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short204_34.png`  (body / L6)
> the home that went with the shop

```
chain across a residential front door, no face or likeness visible, lit ONLY by one kitchen ceiling light which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1999 to 2015 England, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short204_35.png`  (body / L6)
> the file sealed and sent up

```
sealed brown envelope on a counter, no face or likeness visible, lit ONLY by one desk lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1999 to 2015 England, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short204_37.png`  (body / L7)
> the wing he turned sixty on

```
row of locked doors in prison, no face or likeness visible, lit ONLY by one caged ceiling bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1999 to 2015 England, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short204_38.png`  (body / L7)
> agreeing the machine was innocent

```
hands gripping vertical metal bars, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1999 to 2015 England, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short204_39.png`  (body / L7)
> release, with the conviction intact

```
gate opening onto a prison yard, no face or likeness visible, lit ONLY by one caged ceiling bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1999 to 2015 England, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short204_40.png`  (body / L7)
> going home to a village that read the papers

```
man walking away along a pavement, no face or likeness visible, lit ONLY by one kitchen ceiling light which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1999 to 2015 England, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

## short205 — postoffice
*時代設定：2010 to 2019 England* / 12 枚

### `short205_27.png`  (body / L5)
> the bugs logged on the vendor's side

```
smartphone placed screen down on wood, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 to 2019 England, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short205_29.png`  (body / L5)
> the questions nobody asked the expert

```
empty table and two chairs indoors, no face or likeness visible, lit ONLY by one kitchen ceiling light which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 to 2019 England, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short205_30.png`  (body / L5)
> the evidence the jury heard

```
witness box empty in a courtroom, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 to 2019 England, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short205_31.png`  (body / L6)
> the papers that did not survive

```
padlock hanging from a metal latch, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 to 2019 England, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short205_32.png`  (body / L6)
> the advice that did

```
brown envelope sealed with red tape, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 to 2019 England, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short205_33.png`  (body / L6)
> the weekly calls about the defects

```
doors along a strip-lit office corridor, no face or likeness visible, lit ONLY by one overhead fluorescent tube which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 to 2019 England, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short205_34.png`  (body / L6)
> minutes that were not kept

```
open drawer in a metal cabinet, no face or likeness visible, lit ONLY by one desk lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 to 2019 England, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short205_35.png`  (body / L6)
> the answer given to Parliament

```
empty committee room with long table, no face or likeness visible, lit ONLY by one kitchen ceiling light which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 to 2019 England, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short205_36.png`  (body / L7)
> the support centre at Bracknell

```
heavy steel door of a strongroom, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 to 2019 England, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short205_38.png`  (body / L7)
> the convictions falling

```
glass doors opening onto a street, no face or likeness visible, lit ONLY by one sodium streetlight which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 to 2019 England, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short205_39.png`  (body / L7)
> the people who were cleared

```
figure walking away across a forecourt, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 to 2019 England, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short205_40.png`  (body / L7)
> the count that has not moved

```
closed folder tied shut on desk, no face or likeness visible, lit ONLY by one desk lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 to 2019 England, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

## short250 — fieldtest
*時代設定：2010 Houston, Texas* / 7 枚

### `short250_26.png`  (body / L5)
> bottles of household cleaning products on a shelf

```
bottles of cleaning products on shelf, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Houston, Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short250_27.png`  (body / L5)
> pills spilling from a bottle onto a counter

```
pills spilling onto white counter, no face or likeness visible, lit ONLY by one desk lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Houston, Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short250_28.png`  (body / L5)
> a gloved hand pouring liquid between glass beakers

```
gloved hand pouring liquid beaker, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Houston, Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short250_29.png`  (body / L5)
> shelves of chemical bottles in a storeroom

```
shelves of chemical bottles storeroom, no face or likeness visible, lit ONLY by one desk lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Houston, Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short250_37.png`  (body / L7)
> rows of empty wooden courtroom benches

```
empty wooden courtroom benches rows, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Houston, Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short250_39.png`  (body / L7)
> a hand turning the pages of a wall calendar

```
hand turning wall calendar pages, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Houston, Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short250_40.png`  (body / L7)
> a single sheet of paper lying on a floor

```
single paper sheet on floor, no face or likeness visible, lit ONLY by one desk lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Houston, Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

## short251 — fieldtest
*時代設定：2010 Houston, Texas* / 7 枚

### `short251_26.png`  (body / L5)
> a wall of steel filing shelves

```
wall of steel filing shelves, no face or likeness visible, lit ONLY by one desk lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Houston, Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short251_27.png`  (body / L5)
> a sealed envelope lying on a metal counter

```
sealed envelope on metal counter, no face or likeness visible, lit ONLY by one desk lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Houston, Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short251_30.png`  (body / L5)
> a front door seen from a dim hallway

```
front door from dim hallway, no face or likeness visible, lit ONLY by one overhead fluorescent tube which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Houston, Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short251_31.png`  (body / L6)
> a heavy gate standing open onto daylight

```
heavy gate open onto daylight, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Houston, Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short251_34.png`  (body / L6)
> a steel drawer pulled from a wall of drawers

```
steel drawer pulled from wall, no face or likeness visible, lit ONLY by one desk lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Houston, Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short251_35.png`  (body / L6)
> a bare hanging light bulb glowing

```
bare hanging light bulb glowing, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Houston, Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short251_40.png`  (body / L7)
> an empty cardboard box left on a kerb

```
empty cardboard box on kerb, no face or likeness visible, lit ONLY by one sodium streetlight which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Houston, Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

## short252 — fieldtest
*時代設定：2010 Houston, Texas* / 8 枚

### `short252_28.png`  (body / L5)
> a long corridor leading to a lit doorway

```
long corridor toward lit doorway, no face or likeness visible, lit ONLY by one overhead fluorescent tube which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Houston, Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short252_29.png`  (body / L5)
> a silhouette standing in a bright doorway

```
silhouette standing in bright doorway, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Houston, Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short252_30.png`  (body / L5)
> calendar pages turning on a wall

```
calendar pages turning on wall, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Houston, Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short252_32.png`  (body / L6)
> a hand sliding a letter into an envelope

```
hand sliding letter into envelope, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Houston, Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short252_34.png`  (body / L6)
> an empty office with a long table and chairs

```
empty office long table chairs, no face or likeness visible, lit ONLY by one desk lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Houston, Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short252_36.png`  (body / L7)
> a residential front door seen from a hallway

```
residential front door seen hallway, no face or likeness visible, lit ONLY by one overhead fluorescent tube which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Houston, Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short252_37.png`  (body / L7)
> a padlock and chain fastened on a door

```
padlock and chain on door, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Houston, Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short252_39.png`  (body / L7)
> an envelope lying on a doormat

```
envelope lying on a doormat, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Houston, Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

## short253 — lejeune
*時代設定：1981 coastal North Carolina* / 8 枚

### `short253_26.png`  (body / L5)
> a long table with chairs pushed in

```
long table with chairs pushed, no face or likeness visible, lit ONLY by one kitchen ceiling light which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1981 coastal North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short253_30.png`  (body / L5)
> rows of vacant seats in a chamber

```
rows of vacant chamber seats, no face or likeness visible, lit ONLY by one overhead fluorescent tube which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1981 coastal North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short253_31.png`  (body / L6)
> a rusted valve wheel on a pipe

```
rusted valve wheel on pipe, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1981 coastal North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short253_32.png`  (body / L6)
> a heavy metal gate standing open

```
heavy metal gate standing open, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1981 coastal North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short253_34.png`  (body / L6)
> water running from a tap into a glass

```
water running into a glass, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1981 coastal North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short253_36.png`  (body / L7)
> columns of a public building seen from below

```
columns of public building below, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1981 coastal North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short253_37.png`  (body / L7)
> empty benches in a wide hall

```
empty benches in wide hall, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1981 coastal North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short253_39.png`  (body / L7)
> a coiled hose lying on wet concrete

```
coil of hose on concrete, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1981 coastal North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

## short254 — lejeune
*時代設定：1997 North Carolina* / 7 枚

### `short254_27.png`  (body / L5)
> a closed manila folder on a counter

```
closed manila folder on counter, no face or likeness visible, lit ONLY by one desk lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1997 North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short254_33.png`  (body / L6)
> a telephone on a kitchen counter

```
telephone on a kitchen counter, no face or likeness visible, lit ONLY by one desk lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1997 North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short254_36.png`  (body / L7)
> a lamp switched on over a table

```
lamp switched on over table, no face or likeness visible, lit ONLY by one kitchen ceiling light which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1997 North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short254_37.png`  (body / L7)
> a coffee cup beside an open folder

```
coffee cup beside open folder, no face or likeness visible, lit ONLY by one desk lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1997 North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short254_38.png`  (body / L7)
> an empty chair pushed back from a table

```
empty chair pushed from table, no face or likeness visible, lit ONLY by one kitchen ceiling light which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1997 North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short254_39.png`  (body / L7)
> a ring binder lying open on a floor

```
ring binder open on floor, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1997 North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short254_40.png`  (body / L7)
> a flat coastal marsh at first light

```
flat coastal marsh first light, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1997 North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

## short255 — lejeune
*時代設定：2026 eastern North Carolina* / 12 枚

### `short255_26.png`  (body / L5)
> a window at dawn over a desk of folders

```
window dawn over desk folders, no face or likeness visible, lit ONLY by one desk lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2026 eastern North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short255_30.png`  (body / L5)
> a heavy closed door at the end of a hall

```
heavy closed door end hall, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2026 eastern North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short255_31.png`  (body / L6)
> banded notes counted out on a desk

```
banded notes counted on desk, no face or likeness visible, lit ONLY by one desk lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2026 eastern North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short255_32.png`  (body / L6)
> an empty steel drawer pulled open

```
empty steel drawer pulled open, no face or likeness visible, lit ONLY by one desk lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2026 eastern North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short255_33.png`  (body / L6)
> a hand holding a folded cheque

```
hand holding a folded cheque, no face or likeness visible, lit ONLY by one caged ceiling bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2026 eastern North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short255_34.png`  (body / L6)
> a phone lying face down on a bench

```
phone lying face down bench, no face or likeness visible, lit ONLY by one laboratory bench task light which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2026 eastern North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short255_35.png`  (body / L6)
> a row of ceiling lights along a hall

```
row of ceiling lights hall, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2026 eastern North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short255_36.png`  (body / L7)
> coins laid out in a row on a counter

```
coins laid in row counter, no face or likeness visible, lit ONLY by one desk lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2026 eastern North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short255_37.png`  (body / L7)
> a pair of shoes left beside a chair

```
pair of shoes beside chair, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2026 eastern North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short255_38.png`  (body / L7)
> a gate standing open onto flat daylight

```
gate standing open flat daylight, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2026 eastern North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short255_39.png`  (body / L7)
> a tray of personal effects on a counter

```
tray of personal effects counter, no face or likeness visible, lit ONLY by one desk lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2026 eastern North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short255_40.png`  (body / L7)
> a slow river bank in flat daylight

```
slow river bank flat daylight, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2026 eastern North Carolina, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

## short256 — robosigning
*時代設定：2010 Florida* / 8 枚

### `short256_26.png`  (body / L5)
> a car driving on an interstate highway

```
car driving on interstate highway, no face or likeness visible, lit ONLY by the car's own interior light which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Florida, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short256_30.png`  (body / L5)
> a fuel nozzle in a car filler

```
fuel nozzle in car filler, no face or likeness visible, lit ONLY by the car's own interior light which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Florida, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short256_31.png`  (body / L6)
> bolt cutters lying on a workbench

```
bolt cutters on a workbench, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Florida, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short256_34.png`  (body / L6)
> a screen door swinging on its frame

```
screen door swinging on frame, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Florida, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short256_35.png`  (body / L6)
> a toolbox open on a concrete floor

```
toolbox open on concrete floor, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Florida, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short256_38.png`  (body / L7)
> a swimming pool with still green water

```
swimming pool with green water, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Florida, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short256_39.png`  (body / L7)
> a photograph lying on an empty floor

```
photograph lying on empty floor, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Florida, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short256_40.png`  (body / L7)
> a loft hatch open above a ladder

```
loft hatch open above ladder, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Florida, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

## short257 — robosigning
*時代設定：2009 Pennsylvania* / 5 枚

### `short257_26.png`  (body / L5)
> a clock second hand sweeping across its face

```
clock second hand sweeping face, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2009 Pennsylvania, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short257_32.png`  (body / L6)
> a pen lying across a closed folder

```
pen lying across closed folder, no face or likeness visible, lit ONLY by one desk lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2009 Pennsylvania, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short257_33.png`  (body / L6)
> a coat hanging on the back of a chair

```
coat hanging on chair back, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2009 Pennsylvania, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short257_34.png`  (body / L6)
> a drawer of hanging files pulled open

```
drawer of hanging files open, no face or likeness visible, lit ONLY by one desk lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2009 Pennsylvania, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short257_40.png`  (body / L7)
> a bound transcript closed on a table

```
bound transcript closed on table, no face or likeness visible, lit ONLY by one kitchen ceiling light which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2009 Pennsylvania, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

## short258 — robosigning
*時代設定：2010 Georgia* / 7 枚

### `short258_27.png`  (body / L5)
> sheets stacking in a printer tray

```
sheets stacking in printer tray, no face or likeness visible, lit ONLY by one desk lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Georgia, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short258_29.png`  (body / L5)
> a time card rack on a wall

```
time card rack on wall, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Georgia, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short258_31.png`  (body / L6)
> a public counter in a government office

```
public counter in government office, no face or likeness visible, lit ONLY by one desk lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Georgia, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short258_34.png`  (body / L6)
> a heavy door to a records vault

```
heavy door to records vault, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Georgia, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short258_36.png`  (body / L7)
> envelopes stacked in a mail tray

```
envelopes stacked in mail tray, no face or likeness visible, lit ONLY by one desk lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Georgia, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short258_39.png`  (body / L7)
> an envelope lying on a wooden floor

```
envelope lying on wooden floor, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Georgia, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short258_40.png`  (body / L7)
> a stack of unopened envelopes bound with a band

```
stack unopened envelopes bound band, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2010 Georgia, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```
