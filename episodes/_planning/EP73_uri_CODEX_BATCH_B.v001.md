# EP73 · TEXAS / WINTER STORM URI — IMAGE ORDER (BATCH B) v001

**48 additional reconstruction plates, `U121`–`U168`.**
This is a **top-up to BATCH A, not a replacement.** `EP73_uri_CODEX_BATCH_A.v001.md`
(`U001`–`U120`) is delivered, upscaled to 3840 × 2160, staged, and reviewed — 120/120 pass, verdicts
bound by sha256 in `runs/qc/uri_plate_verdicts.v001.json`. **Nothing in Batch A is to be
regenerated, replaced or overwritten.** These 48 are new ids in a new folder.

Every prompt is `[STYLE]` + the subject in the table + `[NEG]`, exactly as in Batch A. Nothing here
may contradict `EP73_uri_FACTS_LEDGER.v001.md`, and the ⛔ rules there bind these images exactly as
they bind the narration.

---

## 0. WHY THIS BATCH EXISTS

The narration for this film is finished and measured: **1,792.6 seconds of master**, 30:01 with the
end card. The footage side is the only part still short. Stock harvesting supplies weather and
infrastructure adequately and supplies **the specific objects of this story badly** — a gathering
line across a Texas field, an iced separator, a compressor hall, a domestic interior with no power.
That is what is below.

**One rule governs this whole batch and it is the single failure mode the Batch A order was written
to prevent, successfully.** This is a story about **thin ice and a few centimetres of snow in a warm
place that has no equipment for it.** It is not a story about winter. Every plate below has to read
as *the wrong weather in the wrong place*, not as a nice snow scene. Batch A got this right — a
frozen ornamental fountain in a warm-climate town square, a swimming pool with a skin of ice and a
diving board, snow lying in the bed of a pickup. Hold that register exactly.

---

## 1. SIZE AND DELIVERY

- **3840 × 2160, exactly 16:9.** `remotion/public/uri/img` is the render truth and
  `preflight_render_gate.py` refuses anything under a 3840 long edge.
- **Known constraint, measured 2026-08-20:** Codex's built-in image generation is **fixed at
  1672 × 941**. Batch A came back at that size and was raised to 3840 × 2160 by
  `scripts/upscale_oroville_4k_esrgan_v001.py --slug uri` (Real-ESRGAN x4plus, then LANCZOS). **If
  1672 × 941 is still the ceiling, deliver at 1672 × 941 and say so.** Do not stop, do not attempt a
  workaround. The upscale is ours.
- **16:9 IS NOT OPTIONAL.** All 120 of Batch A came back correctly at 16:9 and needed no crop; EP72's
  batch did not, and 28 of its plates had to be cropped by measured image energy — one of which
  silently removed the subject the plate existed for. **If a plate cannot be produced at 16:9,
  deliver nothing for that id and list it as not delivered.**
- **One prompt, one image.** No variants, no `a`/`b` versions, no "pick the best of four".
- **New folder.** `E:\pd-media\assets\ai\uri\_batch_b\`. Nothing existing is overwritten.
- **Filenames are the ids**: `U121.png` … `U168.png`. PNG, no metadata, no watermark.

---

## 2. THE BARS

**Depicted people are required and wanted.** Five of these 48 carry a human figure (`U131`, `U139`,
`U149`, `U150`, `U167` — the five marked `P`), and the owner
decision of 2026-08-21 is explicit that ordinary people belong in these films. What is barred is the
**likeness of a real, identifiable individual**.

| never depicted as a person | why |
|---|---|
| **Any of the 246 who died** | ⛔-05. Not named, not shown, not characterised. No body, no bereavement, no hospital |
| **Any named official, regulator, executive or legislator** | Backs, hands and distance only. No insignia, no name plate |
| **Any identifiable lineman, operator or inspector** | Distance or hands. A face at working distance is fine only if it is plainly an invented, unremarkable person |

**A generated face is fine. A face that reads as a specific real person is not.** Control-room,
plant and inspector figures stay as backs, hands and distance (`U139`, `U150`, `U167` below).
Domestic figures — the people in the cold houses — **may and should have faces**, and those faces
should be ordinary, unstyled and doing nothing dramatic.

**Four categories must never be produced as an image at all, in any style.**

1. **No casualty, no rescue, no grief.** No body, no injured person, no stretcher, no paramedic, no
   ambulance interior, no hospital, no funeral, no mourner, no crying. ⛔-05
2. **No document facsimile.** Every list, page, form, notice, bill, ledger, board and marker in this
   order is **blank, ruled or unprinted**; all typography is composited in Remotion. A generated
   glyph is a fabricated record and is one of the four classes that stop a ship.
3. **No courtroom furniture.** No gavel, no scales of justice, no jury box, no judge's bench.
4. **No branded utility.** No company mark, no logo, no livery on a truck, no hard-hat sticker.

---

## 3. HOUSE LOOK — two light states, unchanged from Batch A

**State A — THE STORM.** Flat white overcast, no sun disc, no shadows with edges. Interiors lit only
by what is actually burning or charged: a candle, a torch, a phone screen, a gas ring. Colour drains
toward grey-blue. This is all of ACT_3 and ACT_4.

**State B — BEFORE AND AFTER.** Ordinary flat Texas daylight, dry grass, wide sky, low buildings.
Warm only in the sense that nothing is frozen. ACT_1, ACT_2 and ACT_5.

Each plate below is marked `A` or `B`. There is no third state. **There is no golden hour anywhere
in this film.**

---

## 4. GLOBAL PROMPTS

**`[STYLE]`** — prepend to every plate, verbatim:

> cinematic still, photographic, flat inland Texas — wide low sky, dry grass, mesquite and live oak, single-storey brick and clapboard houses, wide roads, utility poles everywhere, contemporary and unglamorous, documentary reconstruction, natural light only, muted palette, fine film grain, shallow to medium depth of field, no stylisation

**`[NEG]`** — append to every plate, verbatim. **Do not shorten it and do not add face tokens to
it** — faces are wanted; identifiability is what is barred.

> text, lettering, readable text, legible text, numerals, numbers, digits, house numbers, handwriting, cursive, signature, legible signature, seals, seal, emblems, emblem, logos, logo, badge, insignia, wordmarks, name plates, licence plate, registration plate, identifiable person, recognisable person, recognizable person, likeness of a real individual, portrait of a named person, celebrity, public figure, deepfake, body, corpse, injured person, blood, stretcher, paramedic, ambulance, hospital, funeral, grave, mourner, crying, rescue, search and rescue, gavel, scales of justice, lady justice, jury box, judge's bench, courtroom interior, handcuffs, firearm, prison bars, ski slope, ski resort, skier, snowboard, alpine village, chalet, mountain peak, glacier, aurora, northern lights, frozen lake, ice fishing, snowman, snowball fight, sledging, deep snowdrift, blizzard whiteout, pine forest under heavy snow, siberia, scandinavia, alps, megacity skyline, skyscrapers, palm trees, beach, surf, ocean, tropical, cruise ship, high speed train, subway, action movie explosion, video game, golden hour, sunset glow, postcard scenery, christmas, wedding, handshake, money rain, falling banknotes, stock ticker, candlestick chart, glossy advertising lighting, flat CGI, 3D render, cartoon, illustration, oversaturated, HDR halo, watermark

**Four register rules specific to this episode, on top of the `[NEG]`.** These are hard rejects at
review:

1. **THIN SNOW ONLY.** A few centimetres at most, on ground that has never been ploughed, patchy and
   already dirty at the road edges. Ice on branches, fences, wires and standing water. **Never a
   snowscape.**
2. **A WARM PLACE, WRONGLY COLD.** Every frame must carry something that says this climate does not
   expect this: live oaks still in leaf under ice, an ornamental fountain frozen, a swimming pool
   with a skin of ice, an outdoor tap with no lagging, a house with no porch storm door.
3. **NO MOUNTAINS AND NO CONIFER FOREST.** The land is flat to the horizon. Trees are scattered.
4. **UTILITY POLES, NOT PYLONS, IN TOWN.** Wooden distribution poles with transformers on them along
   every residential street. Steel lattice transmission towers only in open country.

---

## 5. THE PLATE ORDER

**Columns.** `id` · `beat` — what it serves · `prompt` — the subject · `flags`:
`P` = people plate (a human figure, never identifiable) · `R` = carries the on-screen
**RECONSTRUCTION** label for its full duration · `D` = built for the depth-parallax pass (give it
clear foreground / midground / background separation) · `A`/`B` = light state.

### HOOK / OP top-up — U121–U124

| id | beat | prompt | flags |
|---|---|---|---|
| U121 | the console | a bank of desk telephones and a worn keyboard on a control-room desk in low light, screen glow from off frame falling across them, no readable display, nobody in shot | R A |
| U122 | the line in the land | a single line of steel lattice transmission towers marching away across flat dry country to the horizon under a white sky, the nearest tower cropped by the frame edge | R D B |
| U123 | straight up | transmission conductors seen from directly beneath looking straight up into a flat white sky, the wires crossing the frame as thin dark lines, nothing else | R D A |
| U124 | scattered light | a low aerial view at night of widely scattered small settlements across flat dark country, most of the frame unlit, a few strings of road lighting | R D A |

### ACT_1 — THE ISLAND · U125–U130 · *1935 to 1970*

| id | beat | prompt | flags |
|---|---|---|---|
| U125 | the desk | a heavy wooden 1930s office desk with a closed blank ledger and a brass lamp on it, daylight from a tall window, nobody present | R B |
| U126 | the drawers | rows of wooden filing drawers filling the frame, brass pull handles, every label card slot empty | R B |
| U127 | the switchyard | an open-air electrical switchyard of an older generation — porcelain insulators, steel frames, exposed busbar — under flat overcast, no people | R D B |
| U128 | the fence | a chain-link fence with barbed top running across the frame, electrical apparatus visible beyond it, flat dry country behind that | R D B |
| U129 | the empty room | a plain institutional meeting room, long table, chairs pushed in, blank wall, no papers, north light | R B |
| U130 | across the grass | a transmission line crossing dry pale grassland at low level, the conductors sagging between two towers, wide sky, no buildings anywhere | R D B |

### ACT_2 — THE RECOMMENDATION · U131–U138 · *winterization, and the years*

| id | beat | prompt | flags |
|---|---|---|---|
| U131 | the wrap | a pair of working hands wrapping insulation around a length of industrial pipework, close, no face and no arm above the elbow, daylight | **P** R B |
| U132 | the roll | a roll of electrical heating tape standing on a workbench beside a knife and a coil of wire, unlabelled, close | R B |
| U133 | the cabinet | a small weatherproof instrument cabinet standing open on a plant walkway, tubing and fittings inside, no lettering, overcast | R B |
| U134 | the sensing line | a thin steel tube clipped along the outside of a large pipe, running away out of focus, very close, no lagging on it | R B |
| U135 | the shelf | a shelf of plain unlabelled ring binders, evenly spaced, office light, nothing else in frame | R B |
| U136 | the training room | a training room with rows of stacking chairs facing a blank projection screen, lights on, nobody in it | R D B |
| U137 | the empty desk | an office desk cleared to bare wood with an empty name-plate holder on it and a chair pushed in, daylight | R B |
| U138 | the grid of years | a plain white wall planner ruled into a grid of empty boxes, no numbers or words in any of them, flat daylight | R B |

### ACT_3 — FOUR MINUTES AND TWENTY-THREE SECONDS · U139–U150 · *the storm, and the houses*

| id | beat | prompt | flags |
|---|---|---|---|
| U139 | the desk, working | a control-room operator seen from behind at a desk of screens, the screens unreadable, the room otherwise empty, low light | **P** R D A |
| U140 | the first frost | frost on brown winter grass and dead leaves, very close, morning, flat light | R A |
| U141 | the glaze | a thin sheen of ice across a stretch of suburban asphalt, kerb and dead grass at the edge, no traffic, flat white light | R D A |
| U142 | the mailbox | an American roadside mailbox on a wooden post with a thin cap of snow on it, no lettering or numbers, a dark house set well back | R D A |
| U143 | the porch | the front porch of a single-storey brick house with thin snow on the steps, the windows dark, a plastic chair with snow on the seat | R D A |
| U144 | the dial | a domestic electricity meter on an outside wall, the glass dome and dial close, the dial face entirely blank with no numerals, thin ice on the wall beside it | R A |
| U145 | torchlight | a domestic breaker panel open on an interior wall, lit only by a torch beam from off frame, the rest of the room in darkness | R A |
| U146 | the torch upended | a torch standing on end on a floor, its beam thrown up onto a plain ceiling, the room otherwise black | R A |
| U147 | the sofa | a sleeping bag and two folded blankets on a living-room sofa in daylight, curtains drawn most of the way, breath fog faintly visible in the air | R D A |
| U148 | the ring | a kettle standing on a lit gas ring in an otherwise dark kitchen, blue flame the only light source, condensation on the window beyond | R A |
| U149 | the queue | a line of cars with headlights on stopped on a snow-dusted suburban road at dusk, exhaust vapour, low buildings either side | **P** R D A |
| U150 | the lift | a figure in a bucket lift working on a wooden utility pole against a flat white sky, seen from below and far off, no face, no company marking | **P** R D A |

### ACT_4 — THE LOOP · U151–U160 · *the gas, and the water*

| id | beat | prompt | flags |
|---|---|---|---|
| U151 | the gathering line | a small-diameter pipeline running along a wire fence line across a flat dry field under a white sky, thin snow in the furrows, no buildings | R D A |
| U152 | the separator | a horizontal pressure vessel on a small steel skid with a skin of ice down one side and icicles from a fitting, close, overcast | R A |
| U153 | the hall | the interior of a compressor building, large machinery and pipework in rows, overhead lighting, nobody in the frame | R D A |
| U154 | the motor | a large electric motor coupled to a pump on a concrete plinth, close, cooling fins, cable gland, no lettering | R A |
| U155 | the needle low | a large round industrial pressure gauge, the needle resting near the bottom of its travel, the dial face entirely blank with no numerals, frost on the bezel | R A |
| U156 | no flame | a flare stack standing against a flat grey sky with no flame at its tip, the plant below it still, thin snow on the ground | R D A |
| U157 | the pump house | a small windowless concrete pump house beside a chain-link fence, thin snow on its roof, a door with no sign on it | R D A |
| U158 | the tanks | circular water treatment tanks seen from above, the water surfaces flat and still, walkways between them, no people | R D A |
| U159 | the standpipe | an elevated water tower on steel legs against a flat white sky, no lettering on the tank, bare trees below | R D A |
| U160 | the split | an outside tap on a brick house wall with ice built up around it and a split in the copper pipe below, very close | R A |

### ACT_5 — THE PRICE · U161–U168 · *after*

| id | beat | prompt | flags |
|---|---|---|---|
| U161 | the envelopes | a domestic mailbox standing open with several plain white envelopes in it, no printing on any of them, ordinary daylight, snow gone | R B |
| U162 | the chair pulled out | a kitchen table with one chair pulled out and nobody in it, a mug and a blank sheet of paper on the table, low side light | R B |
| U163 | the corridor | a corridor of glass-fronted offices, lights on, every office empty, carpet tiles, no signage | R D B |
| U164 | the dais | an empty raised bench in a plain public chamber, rows of seats facing it, nobody present, flat overhead light | R D B |
| U165 | pen and page | a pen lying on a completely blank sheet of paper on a dark wooden table, lit from directly above, nothing else in frame | R B |
| U166 | the new lagging | bright new insulation cladding on a run of plant pipework, the joints taped, ordinary daylight, no ice anywhere | R B |
| U167 | the walk | a figure in a plain high-visibility vest walking away down a gravel plant road, seen from well behind, no face, no company marking, flat daylight | **P** R D B |
| U168 | the same field, June | the same flat Texas field in full summer — green grass, live oaks in leaf, a wire fence, a transmission line in the distance, wide bright sky, no ice, no snow | R D B |

---

## 6. WHAT TO SEND BACK

A single message containing:

1. **The delivered count** — how many of the 48 exist, and the ids of any that do not, with the
   reason. A missing plate reported is fine. A missing plate not reported is the failure.
2. **The actual pixel dimensions** you produced, stated as a number. If it is 1672 × 941, say
   1672 × 941. **Do not describe a plate as "4K" or "high resolution" — give the two numbers.**
3. **Any id where the aspect ratio is not 16:9**, listed explicitly.
4. **Any id where you changed the prompt**, with the change and why. If you did not change any, say
   so in those words.
5. The absolute path of the delivery folder.

**Do not report success for a plate you did not verify exists on disk.** The plates will be read one
by one on contact sheets before anything is placed, and a claimed-but-absent file costs more time
than an honestly reported gap.
