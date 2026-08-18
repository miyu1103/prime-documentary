# EP71 · OROVILLE — IMAGE ORDER (Codex) v001

**Episode `PD-2026-071-oroville` · slug `oroville` · 2026-08-12**

**Contract:** `episodes/PD-2026-071-oroville/episode_spec.v001.json` —
`mandatory_stills` **O001.png … O118.png (118 ids)**, `people_plates` **20 ids**, `people_plates_min`
**20**, **131** `forbidden_subjects`, **27** `forbidden_claims`, `era_setting` **USA 2005–2023, centre
of gravity 2017**, `target_cut_sec` **3.8**.
**Design:** `EP71_oroville_FILM_BIBLE.v001.md` · **Scenes:** `EP71_oroville_SCENE_PLAN.v001.md` ·
**Facts:** `EP71_oroville_FACTS_LEDGER.v001.md` · **Script:** `EP71_oroville_script.en.v001.md` ·
**Rights:** `episodes/PD-2026-071-oroville/09_package/rights_prescreen.v001.json`.

---

## 0. Who generates these, and with what

**Image source policy — `.claude/rules/19-ship-gate.md`, unchanged:**

- **Long-form images are Codex by default.** Every plate in this order is a Codex commission.
  **Do not start a local model to fill this order.**
- **Local generation is an exception, not a lane.** Commercially clear, tuned local paths — **SD3.5
  Large** via `sd35_gen.py` (first choice) or **SDXL** via `gen_max.ps1` — may be used **only** to
  repair a Codex plate or to fill an emergency gap that would otherwise stop a build. **Bare SDXL is
  not allowed. FLUX.1-dev is not allowed in any deliverable** (non-commercial).
- **Long edge ≥ 3840** on every plate (production spec v2 row 5). `public/img` is the render truth.
- Every plate is an **illustration, never evidence** (CLAUDE invariant 11). AI disclosure goes in the
  description at publish, and the on-screen **RECONSTRUCTION** label goes on every plate marked `R`
  in the tables below.

---

## 1. The things that are barred, stated plainly

**Depicted people are REQUIRED and welcome in this film** (owner decision 2026-07-04). Twenty plates
carry a human figure. What is barred, absolutely, is the **likeness of a real, identifiable
individual** (invariant 11, HC-6), and in this episode that has names attached.

| Never depict as a person | Why |
|---|---|
| **Denise Johnson** | a private individual who rented a house, sued for two days' expenses and lost. She is the protagonist and she is never shown. HC-6 |
| **Francis Bechtel, Jacob Klein, Chantel Ramirez, Marie Giordano, Carol A. Gissell** | private individuals who sued and lost. Accused of nothing. HC-2, HC-6 |
| **Nicoli Nicholas, Jeanette Morton, Connie Parks, Genoa Widener, Kaysi and Greg Levias, Bob Mulholland, Ron Stork** | private individuals and one named advocate, all quoted from published sources |
| **Any judge or lawyer** | the courts appear as **attributed typography**, never as portraits |
| **Any employee of the Department of Water Resources** | HC-3. No court found any of the JCCP 4974 allegations true, and **those names appear nowhere in this repository** |

**And four whole categories must never be produced as an image at all, in any style.**

1. **No disaster that did not happen.** No flooded street, no flooded house, no submerged vehicle, no
   wall of water, no breached dam, no burst dam, no collapsed structure, no rubble, no wreckage. **The
   dam did not fail and no town flooded.** Thirteen inundation words are in `forbidden_subjects` so
   the build fails on a filename rather than on a viewing.
2. **No casualties and no rescue.** No body, no injured person, no blood, no ambulance, no paramedic,
   no stretcher, no hospital, no funeral, no grave. Nobody died and nobody was hurt.
3. **No document facsimile** (⛔-26). Not the appellate opinion, not a complaint page, not a
   government claim form, not a county emergency broadcast, not a phone alert, not a television
   chyron, not a newspaper page, not a court exhibit. **Their words may be set as typography in
   Remotion — the words are public record — but never styled to look like a photograph of the
   original paper. Card, not scan.** That distinction is the whole rule.
4. **No children.** `child`, `children`, `baby`, `toddler`, `kids`, `playground` are in
   `forbidden_subjects`. The day-care beat is dressed as **rooms with nobody in them**, which is
   stronger than the literal image and cheaper to defend.

**Global negative prompt, on every plate in this order.** This is the canonical `[NEG]` and it is
checked by `scripts/check_image_order_neg.py`, which requires a face/likeness token, a readable-text
token, a handwriting token, a marks-of-authority token and a numerals token:

> text, lettering, numerals, digits, house numbers, handwriting, cursive, legible signature, readable words on a page, seals, emblems, logos, insignia, badge, wordmarks, name plates, licence plate, registration plate, recognisable person, identifiable person, likeness of a real individual, portrait of a named person, celebrity, public figure, deepfake, flooded street, flooded house, submerged vehicle, wall of water, breached dam, burst dam, collapsed structure, rubble, wreckage, ruins, rescue, search and rescue, body, corpse, drowning, blood, injured person, ambulance, paramedic, stretcher, hospital, funeral, grave, tornado, hurricane, wildfire, forest fire, earthquake, volcano, ocean storm, crashing waves, beach, surf, palm trees, tropical, cruise ship, megacity skyline, skyscrapers, expressway interchange, foreign signage, European street, Asian street, EU number plate, right-hand-drive traffic, children, baby, toddler, playground, gavel, scales of justice, lady justice, jury box, judge's bench, courtroom interior, handcuffs, firearm, prison bars, handshake, hourglass, money rain, falling banknotes, cryptocurrency, candlestick chart, drone show, night vision green, thermal false colour, crosshairs, CCTV monitor grid, golden hour, sunset glow, postcard scenery, Christmas, wedding, glossy advertising lighting, flat CGI, 3D render, cartoon, illustration, oversaturated, HDR halo, watermark

**Note what the `[NEG]` deliberately does NOT contain: `human face`, `facial features`, `eyes`.**
Those three tokens would suppress the people lane, and the people lane is required. What is suppressed
instead is *identifiability* — `recognisable person`, `identifiable person`, `likeness of a real
individual`, `portrait of a named person`.

**Global style prompt, on every plate in this order** (`[STYLE]`):

> cinematic still, photographic, the inland agricultural valley and low foothills of Northern California in February, contemporary — mid 2010s, overcast winter daylight or plain interior fluorescent and sodium light, muted natural colour, low contrast but never crushed: shadows keep their detail and the frame reads clearly on a phone screen, restrained documentary framing, people small in frame and never posed, worn unglamorous ordinary surfaces — wet asphalt, painted breeze block, laminate, vinyl flooring, galvanised steel, orchard bark, dry grass, manila card — nothing staged for advertising, ultra-detailed, photoreal, 4K, long edge 3840 or greater, 16:9, fine film grain, no text, no lettering, no numerals, no watermark, no logo, no signage

---

## 2. House look — two light states, and the audience must feel the move at 16:09

| | **the afternoon** (HOOK · OP · ACT_1 · ACT_2 · ACT_3) | **the record** (ACT_4 · ACT_5 · ENDING) |
|---|---|---|
| light | overcast February daylight; sodium and fluorescent interiors; headlamps | flat north light, paper white, one lamp |
| palette | wet asphalt grey, orchard brown, supermarket white, tail-light red | manila, ink black, document ground, gold `#E5B53A` once per act |
| lens | 35 mm, level, from a distance, people small in frame | 50–85 mm, static, rooms with nobody in them |
| framing | the room contains the person | the room contains nobody |

**Why this episode's era is unusual, and what it means for you.** Almost every PD film has to be aged
into a past decade. **This one is 2017**, so contemporary is correct: modern cars, flat-panel
televisions, LED forecourt lighting and smartphones are all period-accurate here and must NOT be aged
out. What is wrong is not the decade but the **continent and the climate**. Measured on the archive
shelf on 2026-08-12: foreign place markers outnumber American ones 6.7 to 1, and the shelf's
"California" is Monterey sea lions and the Pacific Coast Highway. So every plate must read as **inland
Northern California** — flat valley floor, orchard rows, levee banks, irrigation ditches, low brown
foothills, two-lane roads, single-storey houses with attached garages. **Never coastal. Never a
skyline. Never a canyon. Never a palm.**

---

## 3. THE PLATE ORDER

**Columns.** `id` · `beat` — the script span it serves · `prompt` — the subject; prepend `[STYLE]`
and append `[NEG]` to every one · `P` = a people plate (a human figure, never identifiable) ·
`R` = carries the on-screen **RECONSTRUCTION** label for its full duration · `D` = built for the
depth-parallax pass.

### HOOK — O001–O006 · script span: *"On the afternoon of Sunday…"* → *"…within the next sixty minutes."*

| id | beat | prompt | flags |
|---|---|---|---|
| O001 | she walks in | interior of an ordinary American supermarket entrance lobby, looking outward through sliding glass doors at a half-full car park under flat overcast winter light; trolley bay to one side; the doors half open; nobody in the foreground; the composition is a doorway looking out | R D |
| O002 | the trolley | a shopping trolley stopped in the middle of a grocery aisle, half filled with unbranded packages, abandoned mid-shop; strip lighting overhead; the aisle recedes out of focus | R D |
| O003 | the announcement | a white ceiling speaker grille set into a suspended-tile ceiling, shot from below at a slight angle, fluorescent troffer beside it, shallow depth of field | R |
| O004 | a woman, not anybody | the far end of a supermarket aisle: a woman standing still with her back three-quarters to camera, out of focus, unidentifiable, one hand on a trolley handle; other shoppers blurred and moving out of frame past her | **P** R D |
| O005 | the doors | supermarket sliding glass doors seen from inside as they begin to close, wet car park beyond, reflections of the interior lights on the glass | R D |
| O006 | the town emptying | wide, high, level: an American two-lane road running out across flat farmland at dusk, a line of vehicle taillights receding, low brown foothills on the far horizon, no signage | D |

### OP — O007–O008 · script span: *"Five years later…"* → *"…never named anywhere in particular."*

| id | beat | prompt | flags |
|---|---|---|---|
| O007 | the paperwork ground | a plain sheet of manila card on a dark desk under one lamp, photographed square on, completely blank — this is the film's document ground and text is composited in Remotion, never generated | — |
| O008 | the open line, first | pure black field with a single hand-drawn red boundary line, confident and unbroken, curving across the frame and running off the edge without closing; nothing else in frame | — |

### ACT_1 — O009–O028 · THE ORDER

| id | beat | prompt | flags |
|---|---|---|---|
| O009 | a rented house | a single-storey rented house on an ordinary inland Californian street on an overcast February afternoon, damp asphalt, chain-link and a carport; a figure at the front door at distance, seen from behind, unidentifiable | **P** D |
| O010 | the street | the same street, level, empty, wet, low foothills visible at the end of it | D |
| O011 | the reservoir exists | a large inland reservoir surface seen wide and flat at midday, brown hills beyond, no structure emphasised, no drama | D |
| O012 | the living room | an ordinary American living room in the mid 2010s, lit only by the glow of a large flat-panel television that is out of frame; an empty armchair; curtains drawn against grey daylight | R D |
| O013 | the screen | a modern flat-panel television screen filling the frame, showing an out-of-focus indistinct daytime picture with a blank horizontal band along the bottom edge — **the band is empty; the crawl text is composited in Remotion** | R |
| O014 | the room behind | the same living room from the doorway: the television glow on the wall, nobody in the room, a coat over the back of a chair | R D |
| O015 | the window | net curtain at a front window, seen from inside, a shape of a vehicle passing beyond it, unresolved | D |
| O016 | he goes to look | a man's silhouette at a front window from behind, dark against grey daylight, unidentifiable, one hand on the frame | **P** R D |
| O017 | timestamp ground 1 | dark neutral document ground, empty, faint horizontal ruling — typography composited in Remotion | — |
| O018 | timestamp ground 2 | the same ground, one stop darker, for the second broadcast card | — |
| O019 | timestamp ground 3 | the same ground with a faint vertical division at the left third | — |
| O020 | timestamp ground 4 | the same ground, darkest, for the fourth broadcast card | — |
| O021 | the valley floor | wide aerial-height view of flat inland Californian farmland at dusk: orchard rows in parallel lines, an irrigation channel, a levee bank, a two-lane road, no buildings, low foothills far off | D |
| O022 | the valley floor, low | the same landscape from ground level: orchard trunks in rows receding, bare winter branches, wet ground | D |
| O023 | loading the car | close on a car boot being loaded in a hurry at dusk: hands stacking a cardboard box, blankets, a plastic crate; the hands are all that is in frame of the person | **P** |
| O024 | the back seat | a rear car seat piled with bedding, carrier bags and a folded pushchair, doors open, forecourt light outside | — |
| O025 | the forecourt | an American petrol station forecourt at night, canopy lights, two vehicles at the pumps, seen at distance across the apron, no brand marks | D |
| O026 | the boot lid | a car boot lid that will not close over what is inside it, seen from behind at dusk | — |
| O027 | the door left behind | a front door of a single-storey house closed, porch light on, nobody there, wet path | D |
| O028 | coming back | the same front door two days later in flat daylight, a figure entering with a bag, seen from behind, unidentifiable | **P** D |

### ACT_2 — O029–O046 · WHY NOBODY TOLD THEM

| id | beat | prompt | flags |
|---|---|---|---|
| O029 | what a spillway is | a large plain concrete channel carrying water downhill, seen square on from above, no people, no machinery, engineering without drama | D |
| O030 | the concrete | close on wet weathered concrete surface with a cold joint running through it, water sheeting across | — |
| O031 | the drain idea | water leaving a rectangular concrete opening into a broad channel, mid shot, overcast light | — |
| O032 | the lip | a low concrete weir crest with dry ground on the downhill side of it, seen along its length | D |
| O033 | headward erosion | a bare brown hillside with a fresh gully cut into it by running water, soil and rock displaced downhill, no vegetation on the scar | D |
| O034 | the notch working back | close on the head of a small erosion gully in bare soil, water undercutting the lip of it, sediment in suspension | — |
| O035 | somebody on the ridge | a lone figure standing on a bare foothill ridge at distance, small in frame, back to camera, looking down a slope; overcast | **P** D |
| O036 | the bare slope | wide: a dry brown Northern Californian foothill covered in winter grass and scattered oak, no structures | D |
| O037 | the filing ground | a plain desk with a squared stack of blank paper under one lamp, photographed from above, no writing of any kind | — |
| O038 | a filing cabinet | a grey metal four-drawer filing cabinet against a plain wall, one drawer very slightly open, institutional light | D |
| O039 | 2005 | a cardboard document box on a metal shelf with a blank label field, archive room light | — |
| O040 | the attribution ground | the document ground again, slightly warmer, for the attributed-quotation card | — |
| O041 | the advocate's desk | a cluttered working desk in a small office — a lamp, a mug, a rolled map, a chair pushed back — with a figure just leaving frame at the edge, unidentifiable | **P** D |
| O042 | whose framing | plain dark ground with a faint horizontal rule across the lower third | — |
| O043 | the tannoy again | the supermarket ceiling speaker from a different angle, wider, more ceiling around it | R |
| O044 | the aisle | a supermarket aisle from the end, unbranded packaging, strip lighting, nobody in it | R D |
| O045 | the car park through glass | the wet supermarket car park seen through the entrance glass from inside, vehicles blurred by the reflection | R D |
| O046 | language emptied a valley | the valley floor at last light, very wide, very flat, a single line of headlights crossing it | D |

### ACT_3 — O047–O065 and O115–O118 · THE TWO DAYS

| id | beat | prompt | flags |
|---|---|---|---|
| O047 | the fairground gate | an American county fairground entrance gate at dusk, metal gates open, gravel apron, a low painted hall building behind, figures at distance walking in, all unidentifiable | **P** R D |
| O048 | the car park filling | a gravel and grass overflow car park filling with vehicles in the evening, seen from a distance and slightly above, no faces readable | R D |
| O049 | the hall from outside | a long low mid-century American exhibition hall at a fairground, corrugated roof, floodlight on one wall, rain in the light | R D |
| O050 | the empty corner | a small-town American street corner in the evening, wet, entirely empty, one street light | D |
| O051 | the doorway | a doorway of a small-town shop at night with a pushchair folded against the wall beside it, nobody there | R |
| O052 | the hall, wide | interior of a large plain hall — painted breeze-block walls, exposed roof trusses, strip lighting — with rows of low camp beds laid out on a bare floor, all of them empty and made up, nobody in the room | R D |
| O053 | boots | close on a pair of worn boots and a folded coat on a bare hall floor beside the leg of a camp bed; a person's lower legs at the edge of frame, nothing above the knee | **P** R |
| O054 | the cot | a single camp bed with a folded grey blanket squared on it, photographed from above under strip lighting, bare floor around it | R |
| O055 | stacked chairs | a stack of grey plastic folding chairs against a painted breeze-block wall under a fluorescent fitting, institutional and worn | R D |
| O056 | the paper sign | a sheet of plain paper taped to the inside of a glass door, blank, backlit by grey daylight from outside — **the sign carries no writing; text is composited in Remotion** | R |
| O057 | shoes in a line | a row of shoes lined up against a skirting board on a hall floor, nobody in frame | R |
| O058 | the borrowed record | a hand at the edge of frame holding the corner of a blank photographic print over a plain desk, the print entirely featureless | **P** |
| O059 | cattle at distance | beef cattle grazing at a distance on flat unfamiliar rangeland pasture under an overcast sky, a wire fence in the foreground, no farm buildings | D |
| O060 | the loading ramp | an empty steel livestock loading ramp at a ranch yard, gate open, churned mud, nobody there | D |
| O061 | hay under a tarpaulin | stacked hay bales under a weathered green tarpaulin, ropes and tyres holding it down, winter light | — |
| O062 | the gate | a closed metal farm gate across a dirt track, cattle far off beyond it, low foothills behind | D |
| O063 | the number ground | plain dark ground, empty, for the counting figure composited in Remotion | — |
| O064 | filling in the form | close on a hand resting beside a plain sheet of paper on a kitchen table with a pen laid across it — **the paper is blank and the pen is not writing** | **P** |
| O065 | the shuttered shop | the front of a closed small-town American business in daylight, roller shutter down, no signage legible, wet pavement | D |
| O115 | the sign-in table | a folding table just inside a hall doorway with a clipboard, a stack of blank cards and a plastic box on it, one empty chair behind, nobody there | R |
| O116 | the queue wall | a bare painted hall wall with a worn strip along it at shoulder height and a line of empty folding chairs against it | R D |
| O117 | paper cups | paper cups and a steel urn on a folding table under strip lighting in a hall, half the cups used, nobody in frame | R |
| O118 | the doorway, rain outside | a hall doorway from inside, propped open, hard rain falling through the light outside it, wet floor just inside | R D |

### ACT_4 — O066–O087 · WHICH PEOPLE?

**The light state changes here.** Flat north light, paper white, 50–85 mm, static, rooms with nobody
in them. The pictures almost stop; the typography carries the motion.

| id | beat | prompt | flags |
|---|---|---|---|
| O066 | an empty room | a plain institutional room with one tall window, a single table and no chairs, flat north light, nobody | D |
| O067 | the corridor | a long institutional corridor with closed doors down one side, daylight from the far end, nobody | D |
| O068 | one chair | a single wooden chair against a bare wall in flat window light, photographed square on | — |
| O069 | the table | an empty laminate table under a window, one shadow across it, nothing on it | D |
| O070 | leaving | a figure at the far end of an institutional corridor walking away from camera, small, unidentifiable | **P** D |
| O071 | the unnamed door | a plain painted door in an institutional wall with an empty name-card holder beside it, no writing on it | — |
| O072 | the reported version | plain document ground, warm white, empty, for the card that will be struck through | — |
| O073 | struck through | the same ground one stop cooler, empty | — |
| O074 | the shelf of files | metal shelving stacked with identical unlabelled document boxes, archive room, flat light | D |
| O075 | the ground again | plain cool document ground, empty | — |
| O076 | at the lectern | a figure standing at a lectern in an empty lecture room, from behind and to one side, unidentifiable, rows of empty seats in front | **P** D |
| O077 | the lecture room | tiered rows of empty seats in a plain lecture room under flat daylight, nobody | D |
| O078 | the whiteboard | a wiped whiteboard on a plain wall with a smeared eraser mark across it, no writing | — |
| O079 | the projector | a ceiling data projector in a plain room, off, seen from below | — |
| O080 | the transmitter | a lattice radio transmitter mast at distance against a flat overcast sky, no other structure | D |
| O081 | squaring the papers | a pair of hands squaring a stack of blank paper on a desk in flat window light, nothing above the wrists | **P** |
| O082 | the document ground | plain cool ground, empty, for the trial court's quotation | — |
| O083 | the open line, hesitating | pure black field with a hand-drawn red boundary line that begins confidently, then thins and wavers before stopping partway across the frame | — |
| O084 | the open line, abandoned | pure black field with a red boundary line stopping abruptly in mid-air, one end unresolved, enclosing nothing | — |
| O085 | the map with nothing on it | a plain unmarked pale cartographic field of contour tone with no boundaries, no names and no marks of any kind | — |
| O086 | one word | plain deep ground, empty, for a single word set alone | — |
| O087 | at the window | a figure standing at a tall institutional window with their back to camera, looking out at grey daylight, unidentifiable | **P** D |

### ACT_5 — O088–O109 · COSTS

| id | beat | prompt | flags |
|---|---|---|---|
| O088 | the empty desk | an empty wooden desk under a window in flat north light, one lamp switched off, nothing on the surface | D |
| O089 | the chair | an office chair pushed back from an empty desk, seen from the doorway | D |
| O090 | the window | a tall sash window with grey sky beyond, seen straight on, the room dark around it | D |
| O091 | the lamp | a plain desk lamp switched off, close, in flat daylight | — |
| O092 | leaving the desk | a hand lifting off the edge of a desk, the rest of the person out of frame, flat light | **P** |
| O093 | the identical spines | a long run of identical unlabelled book spines on a library shelf, receding, no writing anywhere | D |
| O094 | the stamp ground | plain manila card, blank, square on, one crease across it | — |
| O095 | the ground, cooler | plain pale ground, empty, for the rules-of-court card | — |
| O096 | the closed folder | a plain closed card folder on a desk, no markings, flat light | — |
| O097 | locking up | a figure pulling a shutter or a door closed on a small-town shop front, from behind, unidentifiable, daylight | **P** D |
| O098 | the stack, edge on | a stack of paper seen from the edge, the layers visible, nothing readable | — |
| O099 | broadcast ground 1 | plain cold ground for the first order card, empty | — |
| O100 | broadcast ground 2 | the same, one stop darker | — |
| O101 | broadcast ground 3 | the same, coldest | — |
| O102 | the riverbank | a figure standing on a riverbank at distance looking at brown water carrying silt, back to camera, unidentifiable, winter | **P** D |
| O103 | the river | a wide brown inland river carrying sediment past a bare gravel bank, overcast, no structures | D |
| O104 | the blank line | plain document ground with a single empty ruled line across it and nothing on the line | — |
| O105 | the drawer | an open desk drawer containing nothing but a paper clip, flat light | — |
| O106 | the empty room | a small plain room with a bare bulb and no furniture, daylight from one window | D |
| O107 | the coat on the chair | an empty chair with a coat left over the back of it in a plain room, nobody there | **P** D |
| O108 | the shop, closed | the same supermarket entrance as O001, from the same position and the same lens, lights off inside, doors closed, the car park beyond empty and wet — **framing must match O001 exactly** | R D |
| O109 | the glass | close on the supermarket entrance glass with the interior dark behind it, faint daylight reflection | R |

### ENDING — O110–O114

| id | beat | prompt | flags |
|---|---|---|---|
| O110 | the reservoir at rest | a wide still inland reservoir at flat light, no movement, no structure emphasised — **the last frame of water in the film** | D |
| O111 | walking away | a figure walking away from a supermarket entrance across a wet car park, seen from behind at distance, unidentifiable, carrying nothing | **P** R D |
| O112 | the document that exists | one plain sheet of manila card on a dark ground, square on, blank | — |
| O113 | the document that does not | two plain sheets of manila card side by side on a dark ground, both blank, one of them noticeably paler | — |
| O114 | the doorway from outside | the supermarket doorway seen from **outside** for the first time in the film, closed, dark within, the reflection of the empty car park on the glass | R D |

---

## 4. THE PEOPLE PLATES — the twenty, and what they may show

These are exactly the twenty ids in `episode_spec.people_plates`:

```
O004  O009  O016  O023  O028  O035  O041  O047  O053  O058
O064  O070  O076  O081  O087  O092  O097  O102  O107  O111
```

**Faces are permitted. Recognition is not.** Every one of the twenty is a figure from behind, at
distance, out of focus, in silhouette, or cropped to hands and lower legs. Not one of them stands in
for a named individual as a portrait, and not one may be captioned or implied to be a real person.
Twelve of the twenty carry the on-screen **RECONSTRUCTION** label because they sit inside a
reconstructed scene.

**If a generated plate reads as a specific identifiable individual, it is rejected and regenerated.**
That is the only acceptance test that matters on this lane.

---

## 5. WHAT MUST NEVER BE GENERATED FOR THIS FILM, AS A CHECKLIST

- A photograph of the appellate opinion, a complaint, a claim form or any court paper. **Card, not scan.**
- A television chyron, a phone emergency alert or a broadcast graphic that reads as real. The bands in
  O013 are **empty**; the words go on in Remotion.
- An official Butte County map, or anything that could be mistaken for one. The open line in O008,
  O083 and O084 is PD's own drawing and is labelled as such.
- Anything flooded, breached, collapsed, rescued or mourned. **The dam did not fail.**
- The Silver Dollar Fairgrounds as a real place. O052–O057 and O115–O118 are a generic American hall
  and are labelled reconstructions.
- A real supermarket brand, fascia, own-label packaging or livery.
- Any child, in any plate, anywhere.

---

## 6. PASTE FILES AND THE NEXT STEP

**Not generated in this pass** — this session was writing and research only, with no builds
permitted. The next agent to touch this order should run the established split:

```
EP71_oroville_CODEX_PASTE_A/batch_01.txt … batch_15.txt   (15 files, 8 plates each, 118 plates)
```

and verify the negative prompt before commissioning anything:

```
py -3.11 scripts/check_image_order_neg.py --file episodes/_planning/EP71_oroville_CODEX_BATCH_A.v001.md
py -3.11 scripts/check_prompt_diversity.py   # the 118 prompts must not collapse onto one composition
```

**Before any of that**, the human review the contract already requires:
`footage_review_required` is `true`, and a labelled contact sheet of the supermarket, cattle,
police and California sub-registers must be opened by a person. The shelter register does not need
reviewing — it is empty, which is why these ten plates exist.
