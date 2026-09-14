# Codex 縦型画像プロンプト v003-remaining

**393 枚** / 26 本のショート / 13 話ぶん。

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

### `short182_27.png`  (body / L5)
> an adult chair and a student chair

```
two empty chairs facing each other indoors, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1980s New Jersey, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short182_29.png`  (body / L5)
> the room where school rules are made

```
empty auditorium seating seen from stage, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1980s New Jersey, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short182_32.png`  (body / L6)
> everything out of the pockets

```
steel tray holding keys and coins, no face or likeness visible, lit ONLY by one caged ceiling bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1980s New Jersey, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short182_33.png`  (body / L6)
> the coat left behind on the chair

```
jacket hanging over back of chair, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1980s New Jersey, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short182_39.png`  (body / L7)
> the town the school sits in

```
water tower against pale morning sky, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1980s New Jersey, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

## short183 — tlo
*時代設定：1980s New Jersey* / 6 枚

### `short183_26.png`  (body / L5)
> a police vehicle at the building

```
police car parked outside a building daytime, no face or likeness visible, lit ONLY by the car's own interior light which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1980s New Jersey, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short183_28.png`  (body / L5)
> a hand resting on what stays shut

```
palm laid flat on a closed folder, no face or likeness visible, lit ONLY by one desk lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1980s New Jersey, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short183_31.png`  (body / L6)
> a corridor of waiting seats

```
row of empty benches along a corridor, no face or likeness visible, lit ONLY by one overhead fluorescent tube which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1980s New Jersey, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short183_34.png`  (body / L6)
> the office being locked up

```
keys turning in an office door lock, no face or likeness visible, lit ONLY by one desk lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1980s New Jersey, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short183_36.png`  (body / L7)
> the vehicles the school runs on

```
school bus parked in a lot, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1980s New Jersey, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short183_39.png`  (body / L7)
> the door it happens behind

```
closed door with a small window, no face or likeness visible, lit ONLY by one bare overhead bulb which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1980s New Jersey, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

## short184 — atwater
*時代設定：1997 Texas* / 11 枚

### `short184_27.png`  (body / L5)
> the children taken indoors

```
two children walking up a driveway, no face or likeness visible, lit ONLY by hard low afternoon sunlight which is the only light in frame, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1997 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

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
*時代設定：1991 Texas* / 9 枚

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

### `short186_32.png`  (body / L6)
> the hose across the drive

```
hose lying across a wet driveway, no face or likeness visible, lit ONLY by hard low afternoon sunlight which is the only light in frame, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1991 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
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
*時代設定：2009 Texas* / 10 枚

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

## short188 — morton
*時代設定：1986 Texas* / 9 枚

### `short188_26.png`  (body / L5)
> the table the night before

```
kitchen table with two empty chairs, no face or likeness visible, lit ONLY by one kitchen ceiling light which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1986 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
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

### `short188_36.png`  (body / L7)
> what he drove home to

```
police cars parked on a suburban street, no face or likeness visible, lit ONLY by one sodium streetlight which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1986 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
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
*時代設定：2011 Texas* / 7 枚

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

### `short189_31.png`  (body / L6)
> the desk on the other side

```
empty office chair behind a desk, no face or likeness visible, lit ONLY by one desk lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 2011 Texas, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
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

## short190 — carsearch
*時代設定：1925 America* / 10 枚

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

### `short190_29.png`  (body / L5)
> the driver walking back to the car

```
person walking toward a parked car, no face or likeness visible, lit ONLY by the car's own interior light which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, 1925 America, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
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
*時代設定：present-day America* / 5 枚

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

## short192 — tyler
*時代設定：medieval England* / 2 枚

### `short192_33.png`  (body / L6)
> an empty chamber of seats

```
empty auditorium rows of seats, no face or likeness visible, lit ONLY by one overhead fluorescent tube which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, medieval England, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

### `short192_36.png`  (body / L7)
> the county tray the file sat in

```
stack of folders in an office tray, no face or likeness visible, lit ONLY by one desk lamp which is switched on, the subject held in the middle third of the tall frame between y560 and y1180 with quiet empty darkness above it and below it, vertical 9:16 composition, cinematic film still, anamorphic, 35mm grain, medieval England, ONE hard practical light source which is switched on and is the only light in frame, strong chiaroscuro, the subject clearly lit against deep shadow, smoke and volumetric light shafts, desaturated amber and steel blue, shallow depth of field, photorealistic, no lettering, no signage, no readable text
```

## short200 — norfolk
*時代設定：1997 Norfolk Virginia* / 2 枚

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
