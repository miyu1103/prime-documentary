# Codex 縦型画像プロンプト v004-remaining

**518 枚** / 31 本のショート / 15 話ぶん。

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

## short184 — atwater
*時代設定：1997 Texas* / 10 枚

### `short184_28.png`  (body / L5)
> the truck left where it stopped

```
pickup truck parked on a residential street, no face or likeness visible, lit ONLY by one sodium streetlight which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1997 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short184_29.png`  (body / L5)
> the house they were taken to

```
front porch of a small house, no face or likeness visible, lit ONLY by hard low afternoon sunlight which is the only light in frame, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1997 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short184_31.png`  (body / L6)
> the shoes she was made to hand over

```
shoes on a tiled floor, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1997 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short184_33.png`  (body / L6)
> pockets emptied at the counter

```
hands emptying pockets onto a counter, no face or likeness visible, lit ONLY by one desk lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1997 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short184_34.png`  (body / L6)
> the photograph taken of her

```
old camera on a tripod indoors, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1997 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short184_35.png`  (body / L6)
> the hour, measured

```
clock above a corridor doorway, no face or likeness visible, lit ONLY by one overhead fluorescent tube which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1997 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short184_36.png`  (body / L7)
> fifty dollars, counted out

```
cash and coins on a counter, no face or likeness visible, lit ONLY by one desk lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1997 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short184_38.png`  (body / L7)
> the belt that started it

```
seatbelt buckle clicking closed in car, no face or likeness visible, lit ONLY by the car's own interior light which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1997 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short184_39.png`  (body / L7)
> the road she was driving

```
two lane road through open country, no face or likeness visible, lit ONLY by one sodium streetlight which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1997 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short184_40.png`  (body / L7)
> the town it happened in

```
traffic passing a small town intersection, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1997 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

## short185 — atwater
*時代設定：2001 America* / 9 枚

### `short185_26.png`  (body / L5)
> the building the remedy was sent to

```
state capitol steps in daylight, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2001 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short185_27.png`  (body / L5)
> someone speaking to the chamber

```
hands resting on a wooden lectern, no face or likeness visible, lit ONLY by one overhead fluorescent tube which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2001 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short185_28.png`  (body / L5)
> where the statute gets written

```
empty legislative chamber with wooden desks, no face or likeness visible, lit ONLY by one overhead fluorescent tube which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2001 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short185_30.png`  (body / L5)
> the way in and the way up

```
wide staircase inside a public building, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2001 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short185_32.png`  (body / L6)
> the vehicle behind you

```
patrol car driving along a highway, no face or likeness visible, lit ONLY by the car's own interior light which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2001 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short185_35.png`  (body / L6)
> the shoulder where it happens

```
roadside grass beside a country highway, no face or likeness visible, lit ONLY by one sodium streetlight which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2001 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short185_36.png`  (body / L7)
> the window coming down

```
car window rolling down in sunlight, no face or likeness visible, lit ONLY by daylight through that window, the only light in frame, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2001 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short185_37.png`  (body / L7)
> what gets handed back

```
hand passing a card through a car window, no face or likeness visible, lit ONLY by the car's own interior light which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2001 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short185_39.png`  (body / L7)
> the border the rule changes at

```
empty road crossing open farmland, no face or likeness visible, lit ONLY by one sodium streetlight which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2001 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

## short186 — willingham
*時代設定：1991 Texas* / 11 枚

### `short186_29.png`  (body / L5)
> the crew who put it out

```
firefighter helmet resting on a truck, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1991 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short186_30.png`  (body / L5)
> the trucks at the kerb

```
fire truck parked outside a house, no face or likeness visible, lit ONLY by one sodium streetlight which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1991 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short186_31.png`  (body / L6)
> the water that hit the glass

```
water spraying from a fire hose, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1991 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short186_32.png`  (body / L6)
> the hose across the drive

```
hose lying across a wet driveway, no face or likeness visible, lit ONLY by hard low afternoon sunlight which is the only light in frame, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1991 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short186_34.png`  (body / L6)
> hands on the nozzle

```
gloved hands holding a nozzle, no face or likeness visible, lit ONLY by one caged ceiling bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1991 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short186_35.png`  (body / L6)
> what the water left behind

```
puddles on a road after spraying, no face or likeness visible, lit ONLY by one sodium streetlight which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1991 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short186_36.png`  (body / L7)
> the grill on the porch

```
small charcoal grill on a porch, no face or likeness visible, lit ONLY by hard low afternoon sunlight which is the only light in frame, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1991 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short186_37.png`  (body / L7)
> the porch itself

```
porch steps of a wooden house, no face or likeness visible, lit ONLY by hard low afternoon sunlight which is the only light in frame, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1991 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short186_38.png`  (body / L7)
> the front door of the house

```
screen door of a small house, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1991 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short186_39.png`  (body / L7)
> the yard he collapsed in

```
front yard of a single storey house, no face or likeness visible, lit ONLY by hard low afternoon sunlight which is the only light in frame, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1991 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short186_40.png`  (body / L7)
> the house on West 11th Street

```
wooden house exterior in daylight, no face or likeness visible, lit ONLY by one sodium streetlight which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1991 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

## short187 — willingham
*時代設定：2009 Texas* / 11 枚

### `short187_26.png`  (body / L5)
> the room booked for the review

```
empty conference room with long table, no face or likeness visible, lit ONLY by one kitchen ceiling light which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2009 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short187_27.png`  (body / L5)
> seats nobody sat in

```
chairs pushed under a boardroom table, no face or likeness visible, lit ONLY by one kitchen ceiling light which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2009 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short187_29.png`  (body / L5)
> the meeting, closed

```
door closing on an empty meeting room, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2009 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short187_31.png`  (body / L6)
> the building the decision came from

```
state office building exterior daylight, no face or likeness visible, lit ONLY by one desk lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2009 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short187_32.png`  (body / L6)
> the place a finding is read aloud

```
podium standing in an empty hall, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2009 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short187_33.png`  (body / L6)
> the public who came to hear it

```
audience chairs in a public hall, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2009 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short187_34.png`  (body / L6)
> the desk the report sat on

```
hand resting beside a lit desk lamp, no face or likeness visible, lit ONLY by that desk lamp itself which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2009 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short187_35.png`  (body / L6)
> leaving the building afterward

```
car pulling away from a government building, no face or likeness visible, lit ONLY by the car's own interior light which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2009 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short187_37.png`  (body / L7)
> the file, closed again

```
hands closing a thick folder, no face or likeness visible, lit ONLY by one desk lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2009 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short187_38.png`  (body / L7)
> the bench that never revisited it

```
empty judge's bench in a courtroom, no face or likeness visible, lit ONLY by one laboratory bench task light which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2009 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short187_40.png`  (body / L7)
> where the case is kept now

```
row of filing cabinets in an office, no face or likeness visible, lit ONLY by one desk lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2009 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

## short188 — morton
*時代設定：1986 Texas* / 12 枚

### `short188_26.png`  (body / L5)
> the table the night before

```
kitchen table with two empty chairs, no face or likeness visible, lit ONLY by one kitchen ceiling light which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1986 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short188_27.png`  (body / L5)
> the hallway of an ordinary house

```
hallway of a suburban house daytime, no face or likeness visible, lit ONLY by one overhead fluorescent tube which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1986 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short188_28.png`  (body / L5)
> the birthday that became a motive

```
birthday candles on a kitchen counter, no face or likeness visible, lit ONLY by one desk lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1986 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short188_29.png`  (body / L5)
> dinner out, the night before

```
family dining table set for dinner, no face or likeness visible, lit ONLY by one kitchen ceiling light which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1986 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short188_30.png`  (body / L5)
> the little boy's toy

```
toy left on a living room floor, no face or likeness visible, lit ONLY by one kitchen ceiling light which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1986 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short188_31.png`  (body / L6)
> the store he opened that morning

```
empty grocery store aisle in morning, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1986 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short188_32.png`  (body / L6)
> the lot before the doors opened

```
shopping trolleys lined up outside store, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1986 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short188_34.png`  (body / L6)
> the back of the store

```
loading dock door of a supermarket, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1986 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short188_36.png`  (body / L7)
> what he drove home to

```
police cars parked on a suburban street, no face or likeness visible, lit ONLY by one sodium streetlight which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1986 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short188_37.png`  (body / L7)
> the car searched in the driveway

```
hands closing the boot of a car, no face or likeness visible, lit ONLY by the car's own interior light which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1986 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short188_38.png`  (body / L7)
> the house he was taken from

```
front lawn of a suburban house, no face or likeness visible, lit ONLY by hard low afternoon sunlight which is the only light in frame, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1986 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short188_40.png`  (body / L7)
> the street after the cars left

```
quiet residential street in the morning, no face or likeness visible, lit ONLY by one sodium streetlight which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1986 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

## short189 — morton
*時代設定：2011 Texas* / 10 枚

### `short189_27.png`  (body / L5)
> the record, boxed

```
stack of cardboard boxes in a storeroom, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2011 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short189_28.png`  (body / L5)
> the office that took it for free

```
law office desk with a lamp daytime, no face or likeness visible, lit ONLY by one desk lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2011 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short189_29.png`  (body / L5)
> a drawer opened at last

```
hand pulling a drawer in a cabinet, no face or likeness visible, lit ONLY by one desk lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2011 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short189_30.png`  (body / L5)
> the case carried in and out

```
briefcase on an office chair, no face or likeness visible, lit ONLY by one desk lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2011 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short189_31.png`  (body / L6)
> the desk on the other side

```
empty office chair behind a desk, no face or likeness visible, lit ONLY by one desk lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2011 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short189_32.png`  (body / L6)
> the corridor the objections ran down

```
corridor of a county courthouse daytime, no face or likeness visible, lit ONLY by one overhead fluorescent tube which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2011 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short189_34.png`  (body / L6)
> another year on the wall

```
round clock high on a corridor wall, no face or likeness visible, lit ONLY by one overhead fluorescent tube which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2011 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short189_35.png`  (body / L6)
> waiting for a ruling

```
people waiting on a bench outdoors, no face or likeness visible, lit ONLY by one laboratory bench task light which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2011 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short189_37.png`  (body / L7)
> the bench where it was read

```
test tubes in a rack on bench, no face or likeness visible, lit ONLY by one laboratory bench task light which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2011 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short189_40.png`  (body / L7)
> one strip of blue cloth

```
blue cloth folded on a steel tray, no face or likeness visible, lit ONLY by one desk lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2011 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

## short190 — carsearch
*時代設定：1925 America* / 13 枚

### `short190_26.png`  (body / L5)
> the stamp nobody had to press

```
rubber stamp resting on ink pad, no face or likeness visible, lit ONLY by one desk lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1925 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short190_27.png`  (body / L5)
> the months that never mattered

```
calendar pages turning on wall, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1925 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short190_28.png`  (body / L5)
> the call that was never made

```
smartphone face down on table, no face or likeness visible, lit ONLY by one kitchen ceiling light which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1925 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short190_29.png`  (body / L5)
> the driver walking back to the car

```
person walking toward a parked car, no face or likeness visible, lit ONLY by the car's own interior light which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1925 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short190_30.png`  (body / L5)
> one blank sheet left on the ground

```
single sheet of paper on floor, no face or likeness visible, lit ONLY by one desk lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1925 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short190_31.png`  (body / L6)
> the dissent, tied shut

```
closed file tied with a band, no face or likeness visible, lit ONLY by one desk lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1925 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short190_32.png`  (body / L6)
> the shelves the dissent went into

```
archive shelves rows of storage boxes, no face or likeness visible, lit ONLY by one desk lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1925 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short190_33.png`  (body / L6)
> the lamp the dissent was written under

```
desk lamp switched on in dark room, no face or likeness visible, lit ONLY by that desk lamp itself which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1925 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short190_34.png`  (body / L6)
> the tray it landed in

```
metal in tray full of forms, no face or likeness visible, lit ONLY by one desk lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1925 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short190_35.png`  (body / L6)
> the pages nobody read again

```
hands resting on a paper stack, no face or likeness visible, lit ONLY by one desk lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1925 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short190_36.png`  (body / L7)
> the bag on the passenger seat

```
duffel bag on a car seat, no face or likeness visible, lit ONLY by the car's own interior light which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1925 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short190_37.png`  (body / L7)
> what a person carries, turned out

```
keys coins and wallet on counter, no face or likeness visible, lit ONLY by one desk lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1925 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short190_38.png`  (body / L7)
> the table where it is all laid out

```
bare metal table under a lamp, no face or likeness visible, lit ONLY by one kitchen ceiling light which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1925 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

## short191 — carsearch
*時代設定：present-day America* / 7 枚

### `short191_26.png`  (body / L5)
> the air inside a stopped car

```
sunlight through a car windscreen, no face or likeness visible, lit ONLY by the car's own interior light which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, present-day America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short191_27.png`  (body / L5)
> the beacon at the window

```
police lights flashing on a street, no face or likeness visible, lit ONLY by the police beacon itself which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, present-day America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short191_30.png`  (body / L5)
> a window at first light over a desk

```
office window morning light on desk, no face or likeness visible, lit ONLY by daylight through that window, the only light in frame, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, present-day America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short191_31.png`  (body / L6)
> one state's own skyline

```
water tower against a morning sky, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, present-day America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short191_33.png`  (body / L6)
> a state courtroom gallery

```
empty courtroom wooden benches, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, present-day America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short191_34.png`  (body / L6)
> the chamber where a state writes its rules

```
empty legislative chamber with seats, no face or likeness visible, lit ONLY by one overhead fluorescent tube which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, present-day America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short191_38.png`  (body / L7)
> a driver walking away from the stop

```
person walking away on a roadside, no face or likeness visible, lit ONLY by the car's own interior light which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, present-day America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

## short192 — tyler
*時代設定：medieval England* / 5 枚

### `short192_29.png`  (body / L5)
> a hand set down beside the book

```
hand resting on a closed book, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, medieval England, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short192_33.png`  (body / L6)
> an empty chamber of seats

```
empty auditorium rows of seats, no face or likeness visible, lit ONLY by one overhead fluorescent tube which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, medieval England, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short192_35.png`  (body / L6)
> one sheet on the floor of a hall

```
sheet of paper on a stone floor, no face or likeness visible, lit ONLY by one desk lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, medieval England, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short192_36.png`  (body / L7)
> the county tray the file sat in

```
stack of folders in an office tray, no face or likeness visible, lit ONLY by one desk lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, medieval England, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
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
*時代設定：2000s England* / 14 枚

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
*時代設定：1999 to 2015 England* / 35 枚

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
*時代設定：2010 to 2019 England* / 34 枚

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
*時代設定：2010 Houston, Texas* / 29 枚

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
*時代設定：2010 Houston, Texas* / 29 枚

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
*時代設定：2010 Houston, Texas* / 30 枚

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
*時代設定：1981 coastal North Carolina* / 30 枚

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
*時代設定：1997 North Carolina* / 29 枚

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
*時代設定：2026 eastern North Carolina* / 34 枚

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
*時代設定：2010 Florida* / 30 枚

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
*時代設定：2009 Pennsylvania* / 27 枚

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
*時代設定：2010 Georgia* / 29 枚

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
