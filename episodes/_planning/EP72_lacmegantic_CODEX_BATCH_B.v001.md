# EP72 · LAC-MÉGANTIC — IMAGE ORDER (BATCH B) v001

**48 additional reconstruction plates, `L121`–`L168`.**
This is a **top-up to BATCH A, not a replacement.** `EP72_lacmegantic_CODEX_BATCH_A.v001.md`
(`L001`–`L120`) is delivered, reviewed and accepted — 120/120 pass, verdicts bound by sha256 in
`runs/qc/lacmegantic_plate_verdicts.v001.json`. **Nothing in Batch A is to be regenerated, replaced
or overwritten.** These 48 are new ids in a new folder.

Every prompt is `[STYLE]` + the subject in the table + `[NEG]`, exactly as in Batch A. Nothing here
may contradict `EP72_lacmegantic_FACTS_LEDGER.v001/.v002/.v003.md`, and the ⛔ rules there bind
these images exactly as they bind the narration.

---

## 0. WHY THIS BATCH EXISTS — read this, it determines what you should draw

The footage side of this film was harvested and then **watched, clip by clip**
(`runs/qc/lacmegantic_stock_verdicts.v001.md`): 108 stock clips, three frames each, all read.
**55 were unusable** — snow in a story that happens on the night of 5–6 July 2013, passenger and
steam trains the film bible bars, overhead catenary on a line that is not electrified, and thirteen
clips that are not documentary objects at all. Combined with a shared library whose files turned out
to be gone, the film currently has **43 usable stock clips**.

So these 48 plates are not decoration and they are not more of the same. **Each one covers a subject
that the stock search could not supply after five passes.** Concretely, stock gave us almost nothing
for: a small inland-Quebec lakeside town at night at street level; brake hardware beyond two
generic wheels; the interior registers of a locomotive repair shop; the ruptured-tank site; and the
town as it is now. That is what is below.

**Do not add faces or drama to compensate for the number.** The film's register is flat, factual and
quiet. A plate that tries to be a photograph of an event is worse than a plate that is a place.

---

## 1. SIZE AND DELIVERY — the part that has gone wrong before

- **3840 × 2160, exactly 16:9.** `remotion/public/lacmegantic/img` is the render truth and
  `preflight_render_gate.py` refuses anything under a 3840 long edge.
- **Known constraint, measured 2026-08-20:** Codex's built-in image generation is **fixed at
  1672 × 941** and cannot be prompted out of it. If that is still true, **deliver at 1672 × 941 and
  say so** — do not stop, and do not attempt a workaround. The sanctioned upscale is already written
  and proven: `scripts/upscale_oroville_4k_esrgan_v001.py --slug lacmegantic --src <your folder>
  --dst <out>` (Real-ESRGAN x4plus to 6688 × 3764, then LANCZOS to exactly 3840 × 2160). That step
  is ours, not yours.
- **16:9 IS NOT OPTIONAL AND HAS BEEN BROKEN BEFORE.** Twenty-eight plates of Batch A came back at
  **1881 × 836 (2.25 : 1)** and had to be cropped by measured image energy, and one of those crops
  silently deleted the gloved hand the plate existed for (`L015`). **If a plate cannot be produced
  at 16:9, deliver nothing for that id and list it as not delivered.** A 2.25 : 1 plate squeezed or
  cropped into 16:9 is a framing decision nobody made.
- **One prompt, one image.** No variants, no `a`/`b` versions, no "pick the best of four". Generate
  each id once from the prompt as written.
- **New folder.** `E:\pd-media\assets\ai\lacmegantic\_batch_b\`. Nothing existing is overwritten;
  Batch A is retired only if it is ever replaced, and it is not being replaced.
- **Filenames are the ids**: `L121.png` … `L168.png`. PNG, no metadata, no watermark.

---

## 2. THE BARS — identical to Batch A, restated because this file must stand alone

**Depicted people are required and wanted.** Four of these 48 carry a human figure (`L131`, `L136`,
`L145`, `L167` — the four marked `P`). What is barred is
the **likeness of a real, identifiable individual**.

| never depicted as a person | why |
|---|---|
| **Thomas Harding, Richard Labrie, Jean Demaître** | Acquitted of criminal negligence causing death, January 2018 (LM-35). ⛔-01 |
| **Any of the 47 who died** | ⛔-05. Not named, not shown, not characterised |
| **Any identifiable firefighter, investigator, official, juror or executive** | Silhouette and distance only. No insignia, no unit marking |

**A generated face is fine. A face that reads as a specific real person is not.** The five roles that
map to real named individuals — the locomotive engineer, the rail traffic controller, the operations
manager, the company chairman, and any of the 47 — stay as **backs, hands and silhouettes**. In this
batch that applies to `L131`, `L136`, `L145` and `L167`, which are marked `P` and are hands or
distance only. Everyone else may have a face.

**Four categories must never be produced as an image at all, in any style.**

1. **No casualty and no rescue.** No body, no injured person, no blood, no stretcher, no ambulance
   interior, no hospital, no funeral, no grave, no mourner. ⛔-05
2. **No fire with a person in the frame.** Fire appears as light on rooftops, smoke crossing a lamp,
   and reflection at a distance. Never a burning building with a figure in it. ⛔-10
3. **No document facsimile.** Every card, page, form, folder, placard, tape and marker in this order
   is **blank, ruled or unprinted**; all typography is composited in Remotion. A generated glyph is a
   fabricated record and is one of the four classes that stop a ship.
4. **No courtroom furniture.** No gavel, no scales of justice, no jury box, no judge's bench, no
   handcuffs.

---

## 3. HOUSE LOOK — two light states, unchanged from Batch A

**State A — SODIUM.** The night of 5–6 July 2013. Yard floodlight and sodium street light, wet
ballast, black tank car flanks, deep shadow that keeps its detail, spruce edges going blue-black.
Amber and cyan only where a real lamp puts them.

**State B — OVERCAST DAY.** Flat July-to-October daylight in inland Quebec. Low contrast, muted
green and grey. **No golden hour anywhere in this film.**

Each plate below is marked `A` or `B`. There is no third state.

---

## 4. GLOBAL PROMPTS

**`[STYLE]`** — prepend to every plate, verbatim:

> cinematic still, photographic, the Estrie region of Quebec, Canada — a small lakeside mill town, low forested hills, spruce and birch, a single-track freight railway running through inhabited streets, contemporary and unglamorous, documentary reconstruction, natural light only, muted palette, fine film grain, shallow to medium depth of field, no stylisation

**`[NEG]`** — append to every plate, verbatim. This is the canonical negative and it carries all five
families `scripts\check_image_order_neg.py` requires. **Do not shorten it and do not add face
tokens to it** — faces are wanted; identifiability is what is barred.

> text, lettering, readable text, legible text, numerals, numbers, digits, house numbers, handwriting, cursive, signature, legible signature, seals, seal, emblems, emblem, logos, logo, badge, insignia, wordmarks, name plates, licence plate, registration plate, identifiable person, recognisable person, recognizable person, likeness of a real individual, portrait of a named person, celebrity, public figure, deepfake, body, corpse, injured person, blood, burn victim, stretcher, paramedic, ambulance, hospital, funeral, grave, mourner, crying, rescue, search and rescue, gavel, scales of justice, lady justice, jury box, judge's bench, courtroom interior, handcuffs, firearm, prison bars, american highway sign, US route shield, EU number plate, right-hand-drive traffic, european street, asian street, megacity skyline, skyscrapers, expressway interchange, palm trees, beach, surf, ocean, tropical, desert, cruise ship, high speed train, passenger train interior, subway, steam locomotive, crash test, action movie explosion, fireball with people, video game, golden hour, sunset glow, postcard scenery, christmas, wedding, handshake, money rain, falling banknotes, stock ticker, candlestick chart, glossy advertising lighting, flat CGI, 3D render, cartoon, illustration, oversaturated, HDR halo, watermark

**Five register rules specific to this episode, on top of the `[NEG]`.** These are the exact classes
that made half the harvested footage unusable. Every one of them is a hard reject at review:

1. **NO SNOW, NO ICE, NO BARE WINTER TREES.** The night is **5–6 July 2013**. Foliage is full summer
   green. The 2012 shop scenes are October — turning leaves are correct there, snow is not.
2. **NO PASSENGER TRAINS AND NO STEAM.** Freight only: black tank cars, hoppers, boxcars, a
   road-switcher diesel.
3. **NO OVERHEAD ELECTRIFICATION.** No catenary, no pantograph, no masts and wire above the track.
   This line is not electrified and overhead wire reads instantly as European mainline.
4. **NO GRAFFITI AND NO REPORTING MARKS.** Tank car flanks are plain, weathered, unlettered.
5. **NO CROWDS AND NO CITY.** Population in frame is one or two figures at most. Buildings are two
   storeys, clapboard and brick. No skyline, ever.

---

## 5. THE PLATE ORDER

**Columns.** `id` · `beat` — what it serves · `prompt` — the subject · `flags`:
`P` = people plate (a human figure, never identifiable) · `R` = carries the on-screen
**RECONSTRUCTION** label for its full duration · `D` = built for the depth-parallax pass (give it
clear foreground / midground / background separation) · `A`/`B` = light state.

### HOOK top-up — L121–L124 · *the town before anything happens*

| id | beat | prompt | flags |
|---|---|---|---|
| L121 | the lit window | the upper floor of a modest two-storey clapboard house at night seen from the street opposite, one curtained window lit warm, the rest of the facade dark, a power line crossing the frame | R D A |
| L122 | the rail head | extreme low angle from between the rails, the polished head of one rail running away into darkness and catching a single distant lamp, ballast stones filling the foreground | R D A |
| L123 | the ridge | a low wooded ridge of spruce and birch against a night sky that is not quite black, a scatter of house lights along its base, no moon | R D A |
| L124 | the water, at night | still black lake water occupying most of the frame, one shore light doubled in the reflection, a low dark treeline along the far edge | R D A |

### OP top-up — L125–L126

| id | beat | prompt | flags |
|---|---|---|---|
| L125 | the gradient, as land | a two-lane rural road climbing steadily away from a valley floor, seen from below so the slope is legible, overcast, no vehicles | R D B |
| L126 | the ground itself | wet railway ballast filling the whole frame from directly above, angular grey stone, one rail edge entering at the corner, water standing between the stones | R B |

### ACT_1 — THE REPAIR · L127–L132 · *October 2012, the shop*

| id | beat | prompt | flags |
|---|---|---|---|
| L127 | the shop yard | an industrial locomotive repair yard in flat autumn daylight, a large shed with the nose of a diesel locomotive just inside the open doorway, oil-stained concrete apron, turning maples beyond the fence | R D B |
| L128 | the bench | a heavy workbench with hand tools laid out on it — spanners, a mallet, calipers — worn wood, unlabelled, overhead fluorescent light | R B |
| L129 | the rag and the tin | an oily rag beside an open unlabelled metal tin of grey compound on a workbench, close, shallow depth of field | R B |
| L130 | the seam | a very close view of a repaired join in a large steel casting, filler standing slightly proud of the surface, tool marks, no lettering anywhere | R B |
| L131 | the roof of the engine | the top deck of a diesel locomotive with body panels lifted open, a pair of hands reaching into the machinery from the edge of frame, October sky above | **P** R B |
| L132 | the blank form | a clipboard holding a completely blank ruled form lying on a workbench beside a pen, daylight from a high window | R B |

### ACT_2 — SEVEN · L133–L142 · *Nantes, the brakes, the hotel*

| id | beat | prompt | flags |
|---|---|---|---|
| L133 | the siding | a single railway track on a visible gradient running beside a rural road at night, one street lamp, dark spruce on both sides, no train yet | R D A |
| L134 | the end platform | the end platform of a black tank car seen whole from ground level at night, the brake wheel and its stand clearly readable as shapes, handrails, floodlight from one side | R A |
| L135 | ratchet and pawl | an extreme close view of a hand brake ratchet wheel and its pawl, worn steel, grease, lit hard from one side, night | R A |
| L136 | the chain | the winding drum and slack chain beneath a brake stand, a gloved hand entering frame from the right and resting on the drum, no face, no arm above the elbow | **P** R A |
| L137 | shoe and tread | a cast brake shoe pressed against the tread of a railway wheel, very close, rust, brake dust, night light | R A |
| L138 | the count | the ends of a line of black tank cars receding into darkness, each end carrying its brake wheel, the wheels forming a diminishing row, no numbers anywhere | R D A |
| L139 | the road up | a rural road climbing past a level crossing at night, one lamp, the track crossing the road at a shallow angle, no traffic | R D A |
| L140 | the empty bracket | an ornate iron sign bracket projecting from a small-town building front at night, the sign panel itself absent, sodium light | R A |
| L141 | the room | an unlit small hotel room at night, curtains half open, the light of the town falling across the ceiling, an unmade bed at the edge of frame | R A |
| L142 | through the glass | a distant lit railway yard seen through a slightly reflective window pane at night, the room dark, condensation at the edge of the glass | R D A |

### ACT_3 — THE THING THEY SWITCHED OFF · L143–L154 · *the fire, and the run*

| id | beat | prompt | flags |
|---|---|---|---|
| L143 | the stack | the exhaust stack on the roof of a diesel locomotive at night, heat shimmer above it, a thin trail of smoke, no flame | R A |
| L144 | the hose down | a charged fire hose lying across railway ballast at night, water running from a coupling, reflected light in the puddle | R A |
| L145 | the pump panel | the control panel of a fire appliance at night, round dials and levers, unlettered, a hand on one lever at the edge of frame | **P** R A |
| L146 | in the glass | orange flame reflected in the dark side glass of a locomotive cab, the cab itself unlit and empty, night | R A |
| L147 | the isolator | a large industrial electrical isolator handle in the down position inside a grey cabinet, no lettering, torchlight | R A |
| L148 | the cab, dark | the interior of a locomotive cab at night with no lights on, only the faint sheen of instrument glass and the seat back visible, nobody in it | R A |
| L149 | the needle low | a large round air pressure gauge in close-up, the needle resting near the bottom of its travel, the dial face entirely blank with no numerals | R A |
| L150 | the first turn | an extreme close view of a railway wheel flange against rail, the wheel just beginning to move, ballast beneath, night | R A |
| L151 | the sleepers | wooden sleepers and ballast passing directly beneath at speed, motion blur, night, one rail edge sharp | R A |
| L152 | the wall of trees | a wall of dense spruce close beside the track rushing past at night, headlight spill on the nearest trunks, everything beyond black | R D A |
| L153 | the bare post | a plain white-painted wooden post standing beside a curving track at night, no lettering or symbol on it, grass at its base | R A |
| L154 | the last curve | the rooftops and street lamps of a small town seen ahead and below from a curving railway line, night, the track entering frame from the bottom corner | R D A |

### ACT_4 — EIGHTEEN · L155–L162 · *the site, and the work on it*

| id | beat | prompt | flags |
|---|---|---|---|
| L155 | the ground, after | a wide view of scorched bare earth and twisted rail where buildings used to stand, flat overcast daylight, nobody in frame, intact town visible at the edges | R D B |
| L156 | the shell | a ruptured cylindrical tank car shell lying on its side on burnt ground, the metal split and peeled open, daylight, no fire, no people | R B |
| L157 | the bogie | a railway bogie standing alone and upright on bare ground, separated from any car, overcast daylight | R B |
| L158 | the plain line | a length of plain unprinted barrier tape stretched across a small-town street between two posts, daylight, the street empty behind it | R D B |
| L159 | the mark | a small painted survey mark on scorched ground beside a graduated scale rod lying flat, close, overcast | R B |
| L160 | the jar | a plain glass jar of dark liquid standing on a laboratory bench, unlabelled, north light | R B |
| L161 | the rig | portable work lights on stands illuminating a cleared site at dusk, cables across the ground, nobody in frame | R D B |
| L162 | the drawing table | a large completely blank drawing sheet on a drafting table held down by weights, a scale rule beside it, window light | R B |

### ACT_5 — WHO ANSWERED · L163–L168 · *after*

| id | beat | prompt | flags |
|---|---|---|---|
| L163 | the counter | a plain public service counter in a municipal building, nobody behind it, a closed roller shutter above, fluorescent light | R B |
| L164 | the stack | a tall stack of plain manila folders standing on the floor against a wall, no labels, daylight from one side | R B |
| L165 | one window | a single lit window in an otherwise dark office building seen from the street at night, no signage on the building | R D A |
| L166 | the new surface | fresh road surface running through a cleared block of a small town, new kerbs, young grass either side, overcast daylight | R D B |
| L167 | the planting | a young planted tree tied to a support stake in newly laid ground, a figure walking away in the far distance, back turned | **P** R D B |
| L168 | the water, morning | the lake at first light, flat calm, low forested shore, no boat, no person, no sun disc in frame | R D B |

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

**Do not report success for a plate you did not verify exists on disk.** The plates will be read
one by one on contact sheets before anything is placed, and a claimed-but-absent file costs more
time than an honestly reported gap.
