# EP73 · TEXAS / WINTER STORM URI — IMAGE ORDER (BATCH A) v001

**120 reconstruction plates, `U001`–`U120`.** Every prompt is `[STYLE]` + the subject in the table +
`[NEG]`. Nothing here may contradict `EP73_uri_FACTS_LEDGER.v001.md`, and its ⛔ rules bind these
images exactly as they bind the narration.

## 0. Who generates these, and at what size

- **Long edge ≥ 3840 px, 16:9.** `remotion/public/uri/img` is the render truth and the pre-render
  gate refuses anything under it.
- **Known constraints, measured on EP72's delivery (2026-08-21):** Codex's built-in generator is
  **fixed at 1672×941**, and part of a batch can come back at **1881×836 (2.25:1), which is not
  16:9**. Both are handled downstream, but **16:9 is what to ask for**, because a 2.25:1 frame has to
  be cropped and a crop can remove the subject — on EP72 it silently deleted the gloved hand from a
  people plate, and only a human looking at a contact sheet caught it.
- The route to 3840: `scripts/upscale_lacmegantic_4k_esrgan_v001.py --src <dir> --dst <dir>` —
  Real-ESRGAN x4plus then LANCZOS to exactly 3840×2160. Non-16:9 frames go through
  `scripts/crop_lacmegantic_wide28_v001.py` first, which chooses the window by measured image energy
  rather than by assuming the centre.
- **One prompt, one image.** No variants, no `b` versions. Deliver to a NEW folder.

## 1. The bars

**Faces are allowed and wanted** (owner decision 2026-08-21). This film's people are ordinary Texans
with no real individual behind them, so the people lane carries **27 plates** and they may have
faces. What is barred is the **likeness of a real, identifiable individual**.

| never depicted as a person | why |
|---|---|
| **Any of the 246 who died** | ⛔-05. Not named, not shown, not characterised |
| **Any named executive, regulator, legislator, judge or official** | The record appears as typography and as the room, never as a portrait |
| **Any identifiable real Texan** | Invented faces only |

**Four categories must never be produced as an image at all.**

1. **No casualty and no grief.** No body, no hospital, no funeral, no grave, no mourner, no person in
   medical distress, no child in distress. ⛔-05
2. **No document facsimile.** Every list, form, bill, statement, report and map in this order is
   **blank or ruled**; all typography is composited in Remotion. A generated glyph is a fabricated
   record and is one of the four classes that stop a ship.
3. **No wrong snow.** This is the single most likely failure. See §2.
4. **No courtroom furniture.** No gavel, no scales, no jury box, no bench.

## 2. THE SNOW — read this before generating anything

A snow prompt returns Scandinavia by default. **Every frame in this film is wrong if it looks like a
place that knows how to handle snow.**

**Texas in February 2021 was:**

- **two to six inches**, on ground with no plough and no salt — not drifts, not banks, not metres
- **ice on live oaks, palms and crepe myrtles**; ice on a chain-link fence; ice on a satellite dish
- snow lying on a **strip-mall car park**, a drive-through lane, a pickup bed, a football pitch
- a **frozen fountain in a warm-climate town square**; frozen sprinkler heads; a swimming pool with
  a skin of ice and a diving board
- flat brown farmland and low mesquite under thin white, and **an enormous grey sky**

**It was not:** a ski slope, an alpine village, a pine forest under a metre of snow, a frozen lake, an
aurora, a snowplough convoy, a northern city that does this every winter, an igloo, a husky.

## 3. Global prompts

**`[STYLE]`** — prepend to every plate:

> cinematic still, photographic, location and period follow the individual subject exactly; unless another year or place is stated, the register is Texas in February 2021 — flat land, low mesquite and live oak, wide suburban streets, single-storey brick and stucco houses with attached garages, strip malls and drive-throughs, pickup trucks, water towers, transmission pylons crossing open ground, an enormous overcast grey sky. For exterior plates flagged A, or whose subject explicitly asks for snow or outdoor ice: show thin unfamiliar snow only two to six inches deep on ground that has never been ploughed or salted, with ice glazing branches, fences and cars. Never bring snow into an interior. For plates flagged B, or whose subject says ordinary weather, no snow, before, after, summer, office, room or blank ground: do not introduce snow or ice unless the individual subject explicitly requests it. Muted natural colour, low contrast but never crushed: shadows keep their detail and the frame reads clearly on a phone screen, restrained documentary framing, people small in frame and never posed, worn unglamorous ordinary surfaces — wet asphalt, breeze block, vinyl siding, laminate counter, galvanised steel, manila card — nothing staged for advertising, ultra-detailed, photoreal, 4K, long edge 3840 or greater, 16:9, fine film grain. Apply every written-content, identity and watermark exclusion from [NEG].

**`[NEG]`** — append to every plate. Carries all five families `check_image_order_neg.py` requires:

> text, lettering, readable text, legible text, numerals, numbers, digits, house numbers, handwriting, cursive, signature, legible signature, seals, seal, emblems, emblem, logos, logo, badge, insignia, wordmarks, name plates, licence plate, registration plate, identifiable person, recognisable person, recognizable person, likeness of a real individual, portrait of a named person, celebrity, public figure, deepfake, body, corpse, injured person, blood, hospital, funeral, grave, mourner, crying, child in distress, ski resort, ski slope, snowboard, alpine, nordic, aurora, frozen lake, deep snowbank, snowdrift, snow plough convoy, pine forest under snow, igloo, husky, polar bear, european street, asian street, EU number plate, right-hand-drive traffic, new york skyline, chicago skyline, megacity skyline, expressway interchange, palm beach, ocean surf, tropical, desert dune, gavel, scales of justice, jury box, courtroom interior, handcuffs, money rain, falling banknotes, stock ticker, candlestick chart, hacking screens, green code rain, golden hour, sunset glow, postcard scenery, christmas, glossy advertising lighting, flat CGI, 3D render, cartoon, illustration, oversaturated, HDR halo, watermark

**Note what the `[NEG]` does NOT contain:** `human face`, `facial features`, `eye contact`,
`headshot`. Faces are wanted. What is suppressed is *identifiability*.

## 4. THE PLATE ORDER

`P` = people plate · `R` = carries the RECONSTRUCTION label · `D` = depth-parallax pass ·
`A` = the cold days · `B` = before, after, and the rooms.

### HOOK — U001–U006

| id | beat | prompt | flags |
|---|---|---|---|
| U001 | the control room | a utility control room at night, banks of screens on a curved desk seen from behind and above, the room lit mostly by the screens, one operator's back at the edge of frame | **P** R D A |
| U002 | the order | a hand resting beside a desk telephone on a control-room console, close, screens out of focus behind | **P** R A |
| U003 | the street goes | a wide suburban street at night with thin snow, half the houses dark and half still lit, no traffic | R D A |
| U004 | the wellhead | a gas wellhead valve assembly standing in flat open country at night, rime ice on the pipework, one distant light | R D A |
| U005 | the line | a transmission line crossing open snow-dusted farmland at night, pylons receding | R D A |
| U006 | the town, dark | a small Texas town from a low rise at night, most of it unlit, a few generator-lit windows | D A |

### OP — U007–U010

| id | beat | prompt | flags |
|---|---|---|---|
| U007 | the map ground | a top-down matte charcoal paper surface with faint embossed county-boundary contours and subtle fibre texture, evenly lit, empty — a ground for composited typography | R B |
| U008 | the frequency screen | a single screen in a dark room showing an unlabelled line graph, the line low in the frame, no readable numerals | R A |
| U009 | ice on a branch | a live oak branch sheathed in clear ice against a flat grey sky, close | D A |
| U010 | black ground | a plain near-black surface with faint horizontal grain, empty | B |

### ACT_1 — THE ISLAND · U011–U030

| id | beat | prompt | flags |
|---|---|---|---|
| U011 | a line at dusk | a high-voltage transmission line crossing flat Texas ranchland at dusk, no snow, ordinary weather | D B |
| U012 | the substation | a substation seen through a chain-link fence, transformers and busbars, flat daylight | D B |
| U013 | the border | a straight rural road running to the horizon across flat land, a fence line beside it | D B |
| U014 | the old office | a plain 1930s office interior, wooden desk, banker's lamp, no papers legible | R B |
| U015 | the ledger ground | a large ruled ledger open on a desk, columns empty, one lamp | R B |
| U016 | the agreement | a plain sheet of heavy paper on a dark table, blank, a fountain pen beside it | R B |
| U017 | the switchyard | an older switchyard with lattice steel structures, overcast, weeds at the fence | D B |
| U018 | a city at night, 1965 register | a mid-century American city skyline at night with most windows dark, seen from across water — era-neutral, no modern towers | D B |
| U019 | the wall map | a large blank wall map board in an operations room, no printing on it | R B |
| U020 | the room where it is decided | a plain institutional meeting room, long table, chairs, blinds half closed, one anonymous administrator seated at the far end seen from behind, small in frame | **P** D B |
| U021 | the pylon, close | the base of a steel transmission pylon from ground level, looking up, grey sky | D B |
| U022 | the turbine, iced | a single wind turbine on flat ground with rime ice on the blades, grey sky | D A |
| U023 | the wellhead, iced | a gas wellhead valve tree with rime ice on every surface, flat land behind | R D A |
| U024 | ordinary weather | a Texas suburban street on a warm ordinary day, live oaks, parked pickups, nothing wrong | D B |
| U025 | the plant | a gas-fired power station seen in ordinary operation from across a dry brown field, pale vapour rising from active stacks, service pipework visible, flat overcast daylight | D B |
| U026 | the meter | a domestic electricity meter on the outside wall of a brick house, close, no numerals legible | R B |
| U027 | the panel outside | a grey utility box on a stucco wall with cables entering, close | R B |
| U028 | the yard | a utility service yard with spools of cable and parked bucket trucks, overcast | D B |
| U029 | the forecast screen | a weather radar display on a screen in a dim room, no legible text or numerals, a large mass approaching | R A |
| U030 | the week before | a supermarket car park on an ordinary grey day, trolleys, a few cars, two ordinary shoppers crossing in the distance with invented unremarkable faces small in frame | **P** D B |

### ACT_2 — THE RECOMMENDATION · U031–U050

| id | beat | prompt | flags |
|---|---|---|---|
| U031 | 2011, the cold | a Texas street under thin snow at dawn, ten years older in feel: fewer modern cars, same houses | R D A |
| U032 | the plant, iced | steam and rime on the pipework of a power station in freezing fog, no people | R D A |
| U033 | the inquiry room | a plain federal-style hearing room, rows of chairs and a long table at the front, three anonymous attendees seated apart and seen only from behind | **P** D B |
| U034 | the report | a thick bound report lying closed on a desk, cover entirely blank, one lamp | R B |
| U035 | the recommendation page | a single sheet of paper on a desk, blank, held flat by a hand at the edge of frame | **P** R B |
| U036 | insulation | pipe lagging being wrapped around an outdoor pipe run, gloved hands, no face | **P** R B |
| U037 | a heat trace | electrical heat-trace cable taped along a length of steel pipe, close | R B |
| U038 | the cost | a plain invoice-shaped card on a desk, blank, a calculator beside it with a blank display | R B |
| U039 | the decision | an empty chair pushed back from a meeting table in a plain room, papers squared and blank | R D B |
| U040 | the filing | a row of ring binders on a steel shelf, spines blank | R B |
| U041 | the years | a wall calendar grid with no printing, in a plain office | R B |
| U042 | the workshop | a training room with a projector, blank screen and rows of chairs, several anonymous utility trainees seated sparsely with their backs to camera | **P** D B |
| U043 | the design plate | a manufacturer's blank metal data plate riveted to a machine casing, no lettering | R B |
| U044 | the same valve | an outdoor valve assembly on a plant site, no ice, ordinary day | R B |
| U045 | dust | an unopened box file on a shelf with a film of dust, label area blank | R B |
| U046 | the corridor | a plain government office corridor, doors and strip lighting, one distant anonymous office worker walking away from camera | **P** D B |
| U047 | the chair's statement | an anonymous official standing at a lectern in a plain room, seen from behind and to one side with face hidden, no insignia | **P** R D B |
| U048 | ten years | a straight road across flat land in ordinary weather, receding to a vanishing point | D B |
| U049 | the sky changes | a vast flat-bottomed grey cloud mass over open country, cold light | D A |
| U050 | February arriving | first snow settling on brown grass and a wire fence, close, thin cover | D A |

### ACT_3 — FOUR MINUTES AND TWENTY-THREE SECONDS · U051–U080

| id | beat | prompt | flags |
|---|---|---|---|
| U051 | the state, white | a wide aerial-feel view of flat Texas farmland under thin snow, grey sky, no settlement | D A |
| U052 | the strip mall | a strip-mall car park under snow, drive-through lane, no cars moving | D A |
| U053 | the fountain | a small-town square fountain frozen mid-flow, ice on the basin, no people | R D A |
| U054 | the pool | a domestic swimming pool with a skin of ice, diving board, snow on the surround | R D A |
| U055 | the sprinkler | a lawn sprinkler head encased in ice, close, brown grass around it | D A |
| U056 | the pickup | snow lying in the bed of a parked pickup truck on a residential street | D A |
| U057 | the control room, working | a utility control room at night with several operators at consoles, seen from behind, screens bright | **P** R D A |
| U058 | the screen wall | a wall of unlabelled line-graph displays in a dim control room, no readable numerals | R A |
| U059 | the frequency trace | one screen filling the frame, a single line descending, no legible text | R A |
| U060 | the phone | a desk telephone handset lifted, a hand and a forearm, control room behind out of focus | **P** R A |
| U061 | the clock | a plain analogue wall clock in an operations room, hands near half past one, no numerals legible | R A |
| U062 | the street goes dark | a suburban street at night in which the near half is lit and the far half is not | R D A |
| U063 | the traffic light | a dead traffic signal over an empty snow-dusted intersection at night | R D A |
| U064 | the breaker panel | a domestic breaker panel open on an interior wall, a hand at it holding a torch, no face | **P** R A |
| U065 | the candle | a candle burnt low on a kitchen counter, ice on the window behind | R D A |
| U066 | the blanket | a blanket hung over an interior doorway with clothes pegs, dim room beyond | R D A |
| U067 | breath | breath visible in a domestic interior, a figure in a coat indoors seen from behind | **P** R A |
| U068 | the family | three figures under blankets on a sofa by candlelight, faces turned away or in shadow | **P** R D A |
| U069 | the phone screen | a face lit only by a phone screen in a dark room, expression neutral, invented person | **P** R A |
| U070 | the mug | two hands wrapped around a mug at a kitchen table, steam, no face | **P** R A |
| U071 | the window | frost patterns on the inside of a domestic window, a grey street beyond | D A |
| U072 | the driveway | an unshovelled driveway with undisturbed snow and a dark house behind | R D A |
| U073 | the note | a plain sheet taped to a front door, no writing on it, snow on the step | R A |
| U074 | the queue | a queue of people outside a shop under a grey sky, coats and hats, faces small | **P** D A |
| U075 | the generator | a portable generator running in a carport with an extension lead, no person | R A |
| U076 | the car running | a car idling in a driveway with exhaust visible in the cold, windows fogged | R D A |
| U077 | the lineman | a utility worker in high-visibility clothing at the top of a pole against a grey sky, distant | **P** R D A |
| U078 | the substation, iced | a close layered view through an electrical substation, ceramic insulator strings and aluminium busbars edged with rime ice, steel gantries receding, no people | R D A |
| U079 | four days | the same suburban street in daylight, still snow-covered, still no traffic | D A |
| U080 | the margin | a single line drawn across a dark screen with a second line below it, no text | R A |

### ACT_4 — THE LOOP · U081–U105

| id | beat | prompt | flags |
|---|---|---|---|
| U081 | the field | a gas field of low wellheads across flat land under thin snow, grey sky | R D A |
| U082 | the wellhead, close | a wellhead valve tree glazed with ice, close, no lettering on any plate | R D A |
| U083 | the gauge, iced | a pressure gauge on a wellhead with ice across the glass, no numerals legible | R A |
| U084 | the separator | a horizontal separator vessel on a gas pad with frozen pipework | R D A |
| U085 | the compressor | a gas compressor station at night, buildings and stacks, lights on | R D A |
| U086 | the compressor, dark | the same low gas compressor compound seen from outside its chain-link perimeter with every building and security lamp dark, silent exhaust stacks, thin snow on the metal roofs | R D A |
| U087 | the meter run | a gas metering skid with valves and pipework, ice on the frame | R B |
| U088 | the pipeline marker | a plain pipeline marker post in open country, sign blank, snow at its base | R D A |
| U089 | the list | a printed list on a plain desk under a lamp, the page entirely blank, ruled | R B |
| U090 | the list, held | two hands holding a blank ruled page over a desk, no face | **P** R B |
| U091 | the switch | an industrial disconnect switch on a pole, handle down, snow on the crossarm | R A |
| U092 | the loop ground | a plain dark surface for a composited three-node diagram, empty | R B |
| U093 | the plant, no fuel | a gas-fired power station at night standing cold and dormant, stacks black against the grey sky with no vapour, yard lights off, iced foreground fence and untouched thin snow | R D A |
| U094 | the yard, still | a plant yard with snow undisturbed by any vehicle track | D A |
| U095 | the valve closed | a large hand-operated valve wheel on plant pipework, gloved hands closing it | **P** R A |
| U096 | the water plant | a municipal water treatment plant from outside the fence, tanks, grey sky | R D A |
| U097 | the pumps, dark | a pump hall interior with no lights on, daylight through high windows | R D B |
| U098 | the tap | a kitchen tap running a thin brown stream into a sink | R A |
| U099 | the bathtub | a bathtub being filled with water, hands at the tap, no face | **P** R A |
| U100 | the bottles | a supermarket shelf stripped bare except for a few bottles of water | D A |
| U101 | the pallet | a pallet of bottled water in a car park with people collecting from it, faces small | **P** D A |
| U102 | the pot on the stove | a large pot of water on a gas hob in a domestic kitchen | R A |
| U103 | the burst pipe | water-stained ceiling tiles and a dripping join in a domestic hallway, no flood | R B |
| U104 | the meter, spinning | a domestic water meter in its pit, lid off, snow at the edge | R B |
| U105 | the boil notice | a blank card taped inside a shop window, no writing, street beyond | R A |

### ACT_5 — THE PRICE · U106–U120

| id | beat | prompt | flags |
|---|---|---|---|
| U106 | the thaw | the same suburban street with the snow half gone, wet asphalt, grey sky | D B |
| U107 | the number ground | a top-down sheet of pale warm-grey vellum on a white desk, softly side-lit with one clean folded edge and generous empty centre — ground for a composited figure | R B |
| U108 | the empty room | a plain domestic room with the furniture removed and one chair left, daylight | R D B |
| U109 | the statement | a blank statement-shaped sheet on a kitchen table under a lamp, a phone face-down beside it | R B |
| U110 | the hands | two hands resting flat on a kitchen table either side of a blank sheet, no face | **P** R B |
| U111 | the office | a utility company office interior, desks and screens off, two anonymous employees in coats walking away toward the exit, small in frame | **P** D B |
| U112 | the chamber | a legislative chamber interior from the back with a few anonymous staff crossing distant aisles, faces unresolved, no insignia legible | **P** D B |
| U113 | the bill | a thick bound document on a desk, cover blank, a pen across it | R B |
| U114 | the map board | a large blank board on an office wall with pins and string but no printing | R B |
| U115 | the inspector | a figure in high-visibility clothing walking a gas pad in ordinary weather, distant | **P** D B |
| U116 | the lagging, new | new pipe insulation on outdoor plant pipework, clean and recent | R B |
| U117 | the heat trace, new | new heat-trace cable and cladding on a wellhead, clean | R B |
| U118 | the same field, summer | the same gas field under a hot flat sky, dry grass, no snow | D B |
| U119 | the line, ordinary | the transmission line from U011, ordinary weather, nothing wrong | D B |
| U120 | the bathtub, empty | an empty domestic bathtub, dry, daylight from a small window | R D B |

## 5. THE PEOPLE PLATES — the twenty-seven

`U001 U002 U020 U030 U033 U035 U036 U042 U046 U047 U057 U060 U064 U067 U068 U069 U070 U074 U077 U090 U095 U099 U101 U110 U111 U112 U115` carry a figure. **Faces are welcome on the ordinary people**
(U068, U069, U070, U074, U101) and must be **invented, unremarkable and not repeated between
plates**. The control-room, plant and official figures (U001, U057, U095, U115, U047) stay as backs,
hands and distance, because those roles map to real people who can be identified.

## 6. What must never be generated — the checklist

- A person who could be recognised as someone real.
- Any of the 246. Any grieving person. Any casualty, hospital, funeral or medical distress.
- A child in distress.
- A readable document, bill, sign, licence plate or handwriting.
- Ski slopes, alpine villages, deep snowbanks, frozen lakes, aurora, huskies, ploughs in convoy.
- New York, Chicago or any city that handles snow routinely. European or Asian streets. EU plates.
- A gavel, scales, jury box or courtroom.
- Golden hour. This film is one enormous grey sky and one long night.

## 7. Paste files and the next step

Generated in this pass as `U001.png`–`U120.png` under
`E:\pd-media\assets\ai\uri\_v001`, one prompt to one image with no retries or variants. Paste-source
files are preserved in `EP73_uri_CODEX_PASTE/batch_01.txt … batch_15.txt`, eight plates each. Raw
technical QC passes; owner contact-sheet review, any approved replacement generation, 4K upscale,
and Remotion staging remain pending:

```
py -3.11 scripts/check_image_order_neg.py --file episodes/_planning/EP73_uri_CODEX_BATCH_A.v001.md
py -3.11 scripts/check_prompt_diversity.py
```

**Before any of that**, the human review the contract requires: `footage_review_required` is `true`,
and a labelled contact sheet of the **snow**, **wellhead**, **control-room** and **domestic-interior**
registers must be opened by a person. The snow register is the one that will fail.
