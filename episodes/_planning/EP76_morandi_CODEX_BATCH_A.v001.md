# EP76 · MORANDI — IMAGE ORDER (BATCH A) v001

**120 reconstruction plates, `V001`–`V120`.** Every prompt is `[STYLE]` + the subject in the table +
`[NEG]`. Nothing in this order may contradict `EP76_morandi_FACTS_LEDGER.v001.md`, and the ⛔ rules
there bind these images exactly as they bind the narration. Design is
`EP76_morandi_FILM_BIBLE.v001.md`; the machine contract is
`episodes/PD-2026-076-morandi/episode_spec.v001.json`.

## 0. Who generates these, and at what size

- **Long edge ≥ 3840 px, 16:9.** `remotion/public/morandi/img` is the render truth and the pre-render
  gate refuses anything under it.
- **Known constraint, measured 2026-08-20 and still true:** Codex's built-in image generation is
  **fixed at 1672×941** and cannot be prompted out of it. A native-4K path is preferred. Where one is
  not available, the sanctioned fallback is `scripts/upscale_oroville_4k_esrgan_v001.py` —
  Real-ESRGAN x4plus to 6688×3764, then a LANCZOS reduction to exactly 3840×2160. Clone it per
  episode. **A plain 2× enlargement is not acceptable** and does not clear the floor. EP71 shipped
  117 of 118 plates at 1672×941 into a pool the builder drew from anyway; that is the failure this
  paragraph exists to prevent.
- **One prompt, one image.** No variants to choose from, no `b` versions.
- Deliver to a NEW folder. Nothing existing is overwritten; the old set is retired, never deleted.

## 0.5 THE PLACE IS A WORKING PORT CITY, NOT A HOLIDAY

The two ways the shelf and the generator will get this wrong are opposite, and both are fatal.

- **Wrong continent.** For EP73 a European street was an error. **Here it is correct** — and that is
  why the *American* register is the one that will leak in. No US route shields, no American highway
  signage, no US number plates. Italy drives on the **right**, so a right-hand-drive vehicle is wrong
  even in a European street.
- **Wrong Italy.** Tuscan hills, cypress avenues, vineyards, the Amalfi coast, Venetian canals and
  gondolas, the Colosseum, Roman ruins. **This is a different country from this film.** Genoa is a
  working Mediterranean port packed into a narrow valley: container cranes and ferries, tall narrow
  ochre, pink and grey blocks with green louvred shutters stacked up steep hills, roof terraces with
  washing, railway yards, corrugated warehouses, a canalised river bed of concrete and gravel with a
  thin stream in it, motorway viaducts and tunnel portals running **over and through** the housing.
- **Italian lettering must be PRESENT and UNREADABLE, never absent.** A Ligurian street with no
  writing anywhere reads as a set. Shopfront fascias, wall notices and road signs may be in frame —
  out of focus, at an angle, too small, or partly hidden, but never legible. The negative list bars
  *readable* text, not the existence of signage.

## 1. The bars

**Depicted people are required** — **twenty-four plates carry a human figure directly**, which meets
the spec floor of twenty-four without depending on variants. What is barred absolutely is the
**likeness of a real, identifiable individual**.

| never depicted as a person | why |
|---|---|
| **Any of the 43 who died or the 13 injured** | ⛔-05. Not named, not shown, not characterised. **No vehicle anywhere that reads as containing anyone** |
| **Any of the 32 convicted at first instance**, Giovanni Castellucci above all | The judgment is not final and an appeal was announced. ⛔-01 |
| **Any of the 25 acquitted or time-barred**, Roberto Ferrazza above all | They were acquitted. ⛔-01 |
| **Riccardo Morandi** | A real, identifiable individual. His work is shown; his likeness is not |
| **The inspector who entered a score; the officer who ran the procedure; the verifier; the designer; the committee members** | ⛔-07. These are real people and the film indicts a system, not a face. Backs, hands and distance only |
| **Any identifiable firefighter, police officer or official** | Silhouette and distance. **No readable insignia, no badge, no unit marking** |

**Six categories must never be produced as an image at all, in any style.**

1. **No collapse, and no fall.** No deck coming down, no falling vehicle, no vehicle at a broken
   edge, no debris field with a car in it, no dust cloud of a structure failing. The event in this
   film is **the gap afterwards, the scale of it, and a severed road with a barrier across it**.
   ⛔-06, spec `forbidden_subjects`
2. **No casualty, no rescue, no grief.** No body, no remains, no injured person, no blood, no
   stretcher, no ambulance interior, no hospital, no funeral, no grave, no mourner, no memorial
   carrying a face, no candle vigil. ⛔-05
3. **No document facsimile, and no screen facsimile.** Every card, form, sheet, folder, ledger,
   drawing, manual and report in this order is **blank or ruled**; all typography and every numeral
   is composited in Remotion. **A generated glyph is a fabricated record** and is one of the four
   classes that stop a ship. ⛔-12
4. **No holiday-Italy register in any form.** No vineyard, no cypress avenue, no Tuscan hill town, no
   Amalfi cliff, no gondola, no Venetian canal, no Colosseum, no Roman ruin, no piazza-as-postcard.
5. **No courtroom furniture.** No gavel, no scales of justice, no jury box, no judge's bench, no
   handcuffs. Italian courts do not look like that and this film does not need it. The law appears as
   a corridor, a bench, a trolley of bound files and an empty chair.
6. **No weather as cause.** No dramatic storm, no lightning strike, no wall of rain over the valley,
   no wind-bent tree at the moment of failure. **Nothing in the record attributes the collapse to the
   weather** and no frame may imply it. ⛔-08

## 2. House look — three light states

The film has three places, and each has its own light. **State letters are `C` `I` `U`.**

**`C` — CONCRETE DAY.** Outdoors, and the default. Flat Ligurian overcast with sea haze: a pale
grey-white sky with no sun in it, muted ochre and grey render, dark green shutters, wet or drying
asphalt, the sea a flat band with no sparkle. **No golden hour anywhere in this film**, and no blue
hour either. Bright is allowed; pretty is not.

**`I` — INTERIOR.** Offices, archives, committee rooms, the paperwork. Plain fluorescent ceiling
light or one desk lamp against daylight through a blind. Laminate, manila, grey steel, terrazzo,
ring binders. Colour drains almost out; what is left is warm grey and paper cream.

**`U` — UNDERSIDE.** Beneath the deck, inside the box girders, on the gantry. Deep shadow that keeps
its detail, daylight bouncing up off concrete from the open edges, one work light where there is one.
Concrete grey, rust orange, galvanised silver, and black.

The film moves **C → U → I → C**: it starts on the road, goes under it, ends in the rooms where it
was decided, and comes back out. `U` belongs to ACT_1's stay, ACT_2's opened pier and ACT_3's
inspections; `I` takes over in ACT_4 and ACT_5.

## 3. Global prompts

**`[STYLE]`** — prepend to every plate. **The period is stated in each subject line; where a plate
states none, it is contemporary.**

> cinematic still, photographic, documentary, Genoa and the Polcevera valley in Liguria, north-west Italy — a working Mediterranean port city packed into a narrow steep-sided valley, tall narrow apartment blocks in ochre pink and grey render with dark green louvred shutters and roof terraces stacked up both hillsides, corrugated warehouses and a railway goods yard on the valley floor, a canalised river bed of concrete and gravel with a thin stream, container cranes and ferries in the distance, motorway viaducts and tunnel portals running over and through inhabited streets, umbrella pines on the slopes, flat overcast Ligurian daylight with sea haze and no sun in the sky, muted natural colour, low contrast but never crushed: shadows keep their detail and the frame reads clearly on a phone screen, restrained documentary framing, people small in frame and never posed, worn unglamorous ordinary surfaces — weathered reinforced concrete, rust staining, galvanised handrail, corrugated steel, painted render, terrazzo floor, laminate desk, manila card, ring binder board — nothing staged for advertising, no tourism, no scenery, Italian signage may appear but is always out of focus or too small or turned away and never legible, ultra-detailed, photoreal, 4K, long edge 3840 or greater, 16:9, fine film grain, no readable text, no legible lettering, no numerals, no watermark, no logo

**`[NEG]`** — append to every plate. This is the canonical negative and it carries all five families
`scripts/check_image_order_neg.py` requires:

> text, lettering, readable text, legible text, numerals, numbers, digits, house numbers, street numbers, handwriting, cursive, signature, legible signature, seals, seal, emblems, emblem, logos, logo, badge, insignia, unit marking, wordmarks, name plates, licence plate, registration plate, identifiable person, recognisable person, recognizable person, likeness of a real individual, portrait of a named person, celebrity, public figure, deepfake, collapsing bridge, bridge collapsing, falling deck, falling car, falling vehicle, vehicle plunging, car at a broken edge, crashed car, crushed vehicle, wreckage with a vehicle in it, debris field, dust cloud of collapse, body, corpse, human remains, body bag, injured person, blood, stretcher, paramedic, ambulance interior, hospital, funeral, grave, mourner, crying, grieving family, rescue, search and rescue, firefighter carrying person, memorial portrait, photo memorial, candle vigil, lightning strike, thunderstorm, storm clouds dramatic, wall of rain, tornado, earthquake damage, war ruins, movie explosion, action movie, fireball vfx, video game, crash test, vineyard, cypress avenue, tuscan hill town, rolling hills with cypress, amalfi coast, cliff village, gondola, venetian canal, colosseum, roman ruins, leaning tower, piazza postcard, palm tree, beach, surf, sunbathing, cruise ship, tropical, desert, snow, megacity skyline, skyscrapers, expressway interchange, american highway sign, US route shield, US number plate, mainland american main street, uk street, london street, right-hand-drive traffic, asian street, gavel, scales of justice, lady justice, jury box, judge's bench, courtroom interior, handcuffs closeup, firearm, prison bars, money rain, falling banknotes, stock ticker, candlestick chart, handshake, golden hour, sunset glow, blue hour, warm hero light, postcard scenery, glossy advertising lighting, flat CGI, 3D render, cartoon, illustration, oversaturated, HDR halo, watermark

**Faces are allowed, and wanted.** The `[NEG]` deliberately does **not** contain `human face`,
`facial features`, `eye contact`, `headshot` or `profile of a face`. The owner's decision of
2026-08-21 is that depicted people are required and welcome; EP71, EP72 and EP75 all keep those
tokens out for the same reason. What is barred is **identifiability**, not the existence of a face.

So: **a generated face is fine. A face that reads as a specific real person is not.**

**The carve-out this episode keeps.** Six roles in this film map to real, identifiable individuals
whose acts the narration describes: **the inspector who entered a score, the officer who ran the
project procedure, the verifier, the designer, the committee that approved it, and anyone who was on
the bridge on 14 August 2018.** A resolved face attached to one of those roles is a likeness claim
whatever the prompt says. Those roles stay as backs, hands and silhouettes —
`V006 V021 V045 V048 V060 V061 V094 V098 V099 V100`. **Everyone else in this film — the residents on
the balconies and in the streets, the drivers, the people at the bus stop and in the toll queue, the
construction workers of the 1960s, the figures on the street now — may have faces.**

## 4. THE PLATE ORDER

**Columns.** `id` · `beat` — the script span it serves · `prompt` — the subject · `flags`:
`P` = people plate (a human figure, never identifiable) · `R` = carries the on-screen
**RECONSTRUCTION** label for its full duration · `D` = built for the depth-parallax pass ·
`C`/`I`/`U` = light state.

> **`R` is the default, not the exception.** This is a real event eight years old for which real
> photographs exist, and invariant 11 bars presenting a generated image as an authentic record. Every
> plate that depicts **this bridge, this valley, this paperwork or that day** carries `R`. Only
> abstract grounds, generic hardware studies and generic present-day material are without it.

### HOOK — V001–V006 · *"On the first of August 2012…"*

| id | beat | prompt | flags |
|---|---|---|---|
| V001 | the valley from above | a wide view down into a narrow urban valley in an Italian port city from a hillside: apartment blocks stacked up both slopes, corrugated warehouses and a railway goods yard on the flat floor, a concrete river bed with a thin stream, low flat grey cloud | R D C |
| V002 | the underside | the soffit of a reinforced concrete motorway deck seen from directly beneath, transverse ribs and drainage outlets receding into shadow, daylight only at the far edges | R D U |
| V003 | the concrete gone | close on a concrete beam where the cover has broken away and rusted reinforcing steel is exposed, rust staining running down the face, damp along the lower edge | R U |
| V004 | broken wires | macro of a bundle of high-tensile steel wires inside a broken concrete duct, several of the wires cleanly parted, the ends splayed and rust-brown | R U |
| V005 | the form | a printed inspection form on a clipboard hooked over a galvanised steel handrail high above a valley, the sheet ruled into empty boxes, wind lifting one corner | R I |
| V006 | the hand and the box | a hand holding a ballpoint pen above one empty ruled box on a blank printed form, shot from directly above, forearm at the edge of frame, no face in frame | **P** R I |

### OP — V007–V010

| id | beat | prompt | flags |
|---|---|---|---|
| V007 | the four ties | the four diagonal concrete stays of a cable-stayed bridge tower against flat grey cloud, seen from below, the deck cutting across them | R D C |
| V008 | a stay in section | a cut section through a large rectangular prestressed concrete member, dark, showing a dense cluster of steel strands embedded in grout at its core | R U |
| V009 | traffic on a viaduct | two lanes of ordinary traffic on an elevated motorway seen at deck level from the hard shoulder, concrete barrier to the right, rooftops far below and beyond | D C |
| V010 | black ground | a plain matte near-black surface with faint horizontal grain, evenly lit, entirely empty | I |

### ACT_1 — THE SHEATH · V011–V034 · *"The Polcevera is a river in Genoa…"*

| id | beat | prompt | flags |
|---|---|---|---|
| V011 | the valley, 1960s | a narrow industrial valley in an Italian port city in the early 1960s: low workshops, a goods yard, overhead tram wires, apartment blocks climbing both hillsides, no motorway anywhere in the frame | R D C |
| V012 | the drawing board | a large drawing board in an engineering office of the early 1960s, a T-square and set squares lying on a blank sheet of drafting paper, an anglepoise lamp | R I |
| V013 | the blank sheet | a blank sheet of drafting paper filling the frame, faint blue printed grid, one pencil laid across it | R I |
| V014 | falsework | a bridge under construction in the mid 1960s: timber and steel falsework rising from a valley floor, a concrete pier half formed inside it, a lattice crane | R D C |
| V015 | the tower rising | a tall reinforced concrete A-frame bridge tower under construction, formwork panels still clamped to it, seen from below against pale sky | R D C |
| V016 | workers on the deck | small figures in overalls walking along an unfinished concrete bridge deck in the mid 1960s, seen from a long way off, faces far too small to resolve | **P** R D C |
| V017 | the strands laid | a bundle of bright steel strands laid out along an unfinished concrete member on a bridge site in the mid 1960s, sleeved and clamped at intervals | R U |
| V018 | tensioning | a hydraulic jack clamped to the end of a prestressing tendon on a concrete member, hoses trailing away, period industrial equipment of the 1960s | R U |
| V019 | the segments | precast concrete segments stacked on a bridge construction site in the mid 1960s, each with a large rectangular opening through the middle | R C |
| V020 | threading the sheath | a precast concrete segment being lowered by crane over a bundle of steel strands on a bridge site, two workers guiding it from a distance | **P** R D C |
| V021 | grout | grout being pumped into a duct through a steel nipple on a concrete member, hose and pressure gauge, gloved hands only at the edge of frame | **P** R U |
| V022 | the finished stay | a long rectangular prestressed concrete stay running diagonally out of frame, seen close along its flank, pour joints and formwork lines visible | R D U |
| V023 | the saddle | the top of a concrete bridge tower where four diagonal members meet a transverse beam, seen from directly beneath | R U |
| V024 | the opening, 1967 | a newly completed concrete cable-stayed motorway viaduct in 1967 seen from the valley floor, clean pale concrete, period saloon cars small on the deck | R D C |
| V025 | period traffic | 1960s Italian traffic on a new elevated motorway — small saloons and a single coach — seen from far enough away that no vehicle detail resolves | D C |
| V026 | white ground | a plain white ground with a single fine horizontal line ruled across it, evenly lit, nothing else in frame | I |
| V027 | the tower against cloud | a concrete bridge tower ninety metres tall seen from below against flat grey cloud, four stays cutting away from its head | R D C |
| V028 | the infill deck | a short simply supported concrete bridge deck sitting between two much larger structures, its six beams visible from beneath | R D U |
| V029 | what is underneath | the underside of a motorway viaduct with a corrugated-roof factory directly below it, a railway line and a two-lane road all in the same frame | R D C |
| V030 | the balcony | a resident standing at the railing of a fourth-floor balcony in a Ligurian apartment block, washing on a line beside them, a motorway viaduct crossing a short distance away at the same height | **P** R D C |
| V031 | the strand, new | macro of seven-wire steel prestressing strand, the helical lay of the wires bright and lightly oiled, lying on plain grey card | R I |
| V032 | the strand, later | macro of the same seven-wire steel strand, rust-brown and deeply pitted, several outer wires reduced to half their thickness, lying on plain grey card | R I |
| V033 | the void | a cut concrete duct in section showing grey grout that has not filled it, a void running along the top with bare strand exposed in it | R U |
| V034 | the shell | a large rectangular concrete member in section filling the frame, its outer shell intact and pale, the core dark | R D U |

### ACT_2 — ONE OF THREE · V035–V054 · *"By the beginning of the 1980s…"*

| id | beat | prompt | flags |
|---|---|---|---|
| V035 | the report, 1981 | a plain bound engineering report lying closed on a desk in an office of the early 1980s, cover blank, a rotary telephone beside it | R I |
| V036 | hatches cut | a rectangular access hatch cut into the underside of a concrete bridge deck, its edges rough, darkness beyond it | R U |
| V037 | inside the box | the interior of a hollow concrete box girder: a low chamber with transverse walls and small openings, one work light on a cable | R D U |
| V038 | inside, the cables | close inside a concrete box girder chamber — prestressing ducts running along the wall, one broken open, strands visible inside it | R U |
| V039 | scaffold on the tower | scaffolding wrapped around the upper part of a concrete bridge tower in the early 1990s, a hoist, sheeting flapping at the edges | R D C |
| V040 | the core | a diamond core drill clamped to a concrete face, water running down it, a cylindrical core half withdrawn | R U |
| V041 | the cores laid out | a row of concrete core samples lying on a plank, some sound and some crumbling at one end, no markings on any of them | R I |
| V042 | opening the stay | a large rectangular concrete member with a section of its outer shell broken away, the steel inside exposed to daylight | R U |
| V043 | severed strands | close on a bundle of prestressing strands inside broken concrete, several strands parted clean through, the cut ends splayed and rust-brown | R U |
| V044 | slack | close on prestressing strands that have gone visibly slack inside a broken duct, one sagging away from the bundle | R U |
| V045 | the hands and the strand | two gloved hands holding a short length of severed steel strand up to the light, no face in frame | **P** R U |
| V046 | the new ducts | new polyethylene ducts clamped in a row down the outside flank of a large weathered concrete member, bright plastic against grey | R D U |
| V047 | the anchorage | a steel anchorage block bolted to the top of a concrete transverse beam, new bright bolts against old grey concrete | R U |
| V048 | tensioning, 1990s | a hydraulic jack on an external cable anchorage high on a bridge tower, hoses running down the tower face, one figure at the far end of the platform | **P** R U |
| V049 | the temporary gantry | a purpose-built working platform suspended beneath a bridge deck in the 1990s, cables and winches, nobody on it | R D U |
| V050 | traffic continues | traffic running on a motorway viaduct while a working platform hangs beneath the deck, seen from the side at a distance | D C |
| V051 | one of three | three concrete bridge towers in a line along a valley seen from a hillside, only the nearest one wrapped in scaffolding | R D C |
| V052 | the other two | two concrete bridge towers seen from below, unwrapped and weathered, water staining running down the stay flanks | R D C |
| V053 | the walkway | a galvanised steel inspection walkway bolted along the underside of a bridge abutment, empty, 2000s | R U |
| V054 | the equipment stored | working platforms and hoists in storage beneath a motorway structure, tarpaulins and chains, unused for years | R D U |

### ACT_3 — THE NUMBER IN THE BOX · V055–V080 · *"From here the story is made of paper…"*

| id | beat | prompt | flags |
|---|---|---|---|
| V055 | the manual | a plain ring-bound technical manual lying open on a laminate desk, its pages ruled but entirely blank, one desk lamp | R I |
| V056 | the scale, blank | a printed table on a plain sheet: ruled rows and columns filling the frame, every cell empty | R I |
| V057 | the box, hero | extreme close on one empty ruled box on a printed inspection form, the surrounding rows blank, one lamp raking across the paper | R I |
| V058 | the clipboard on the rail | a clipboard carrying a blank ruled form, hooked over a galvanised handrail high above a valley, the drop soft behind it | R D U |
| V059 | the gantry, working | a self-propelled inspection gantry running along the underside of a motorway deck, its platform extended, seen from the side | R D U |
| V060 | on the platform | a worker in plain high-visibility clothing standing on an inspection platform beneath a concrete deck, seen from behind, no insignia and no unit marking | **P** R U |
| V061 | the torch | a hand torch held against a concrete soffit, the beam picking out a crack and a run of rust staining, hand only in frame | **P** R U |
| V062 | the hammer | a small steel inspection hammer resting against a concrete face beside a patch of hollow render | R U |
| V063 | the slab that dropped | a bridge deck slab that has settled at one end where the bearing beneath it partly failed, a step visible in the running surface | R C |
| V064 | the bearing | a steel bridge bearing between a pier head and a deck, corroded, one plate visibly displaced | R U |
| V065 | severed bars | reinforcing bars sheared through where a concrete cantilever has failed, the broken ends bright against dark rust | R U |
| V066 | the edge beam | the outer edge beam of a bridge deck seen from below and to the side, its lower bulb spalled away, cables in view | R D U |
| V067 | corroded cables in the chamber | prestressing cables inside a box girder chamber, heavily corroded, one duct broken open, water staining running below it | R U |
| V068 | the chamber you climb into | a narrow access opening into a concrete box girder chamber, one ladder rung, darkness beyond | R U |
| V069 | the foundation | the base of a concrete bridge pier where it meets the ground, weeds along it, a drainage channel, undisturbed for decades | R D C |
| V070 | the observations box | a printed form on a desk with a large empty ruled area across the foot of it, headed by nothing, entirely blank | R I |
| V071 | the shelf that thins | a shelf of ring binders in an office store room, every spine blank, one gap where a binder is missing | R I |
| V072 | the drainpipe | a corroded steel bracket on the flank of a concrete bridge beam, the drainpipe sagging away from it, staining below | R U |
| V073 | the graph, blank | a blank graph grid printed on a plain sheet, axes ruled, no line drawn on it | R I |
| V074 | the office at night | an ordinary open-plan office at night, desks tidy, screens off, one strip light left on at the far end | I |
| V075 | the ledger | a plain ruled accounts ledger open on a desk, its columns empty, a lamp at the edge of frame | R I |
| V076 | the barrier going on | new precast concrete traffic barrier units being set along the edge of a motorway deck, a crane hook, workers at a distance | **P** R D C |
| V077 | weight added | close on the base of a concrete traffic barrier bolted down through a bridge deck slab, new bright bolts, old grey concrete | R C |
| V078 | the toll plaza | an Italian motorway toll plaza on a flat overcast day, canopies and lane islands, a short queue of cars, no legible signage | **P** D C |
| V079 | the ordinary drive | the view forward through a car windscreen on an elevated motorway, two hands on the wheel at the bottom of frame, no face, wipers at rest | **P** D C |
| V080 | underneath, waiting | a bus stop on a street directly beneath a motorway viaduct, people waiting, the concrete soffit filling the top third of the frame | **P** D C |

### ACT_4 — THE THING NOBODY WROTE · V081–V106 · *"There is one document at the centre…"*

| id | beat | prompt | flags |
|---|---|---|---|
| V081 | the index | a card index drawer pulled open on a desk, dividers standing upright, every tab blank | R I |
| V082 | the empty tab | close on one blank index tab standing above the others in a card drawer, nothing filed behind it | R I |
| V083 | the archive shelf | a shelf of identical archive box files in a store room, every label area blank, one box pulled out of line | R I |
| V084 | the letter | a single sheet of headed paper lying on a desk, the head area blank, an envelope beside it | R I |
| V085 | the fax | a fax machine on a side table in a 2010s office, a curl of blank thermal paper in the tray | R I |
| V086 | the form, level zero | a printed form on a desk ruled into many small empty fields, a paperclip at one corner | R I |
| V087 | the drawings | a stack of rolled engineering drawings standing in the corner of an office, the ends blank | R I |
| V088 | the drawing unrolled | a large engineering drawing unrolled and weighted flat on a table, the sheet entirely blank, a weight at each corner | R I |
| V089 | the title block | close on the empty title block panel at the corner of a blank engineering drawing, ruled boxes, nothing entered | R I |
| V090 | the calculation | a bound calculation report open on a desk, its pages ruled and blank, a pen laid across them | R I |
| V091 | the sixty-two | a stack of identical blank comment slips squared up on a desk, the top one lifted slightly | R I |
| V092 | the verifier's desk | a desk in a technical office: lamp, rolled drawings, a chair pushed in, nobody there | R I |
| V093 | the signature line | close on a blank ruled signature line at the foot of a plain sheet, a pen resting beside it | R I |
| V094 | the hands and the file | two hands closing a thick bound file on a desk, no face in frame | **P** R I |
| V095 | the corridor | a corridor in a plain Italian public office building, terrazzo floor, doors with blank plates, strip lighting, one figure far away | **P** D I |
| V096 | the committee room | a plain municipal committee room: a long table, stacking chairs, a projector screen down, empty | R D I |
| V097 | the lectern | a plain wooden lectern at the front of a meeting room, a glass of water on it, nobody there | R I |
| V098 | past the empty chair | a meeting room seen past the back of one empty chair in the foreground, figures at the far end of the table too distant to resolve | **P** R D I |
| V099 | the back at the lectern | a figure standing at a lectern in a meeting room seen from behind, gesturing towards a screen that is blank | **P** R I |
| V100 | the sheet passed | a plain sheet of paper being passed across a meeting table, two pairs of hands only, the sheet blank | **P** R I |
| V101 | the stamp | a rubber date stamp lying on an ink pad beside a blank document, the stamp face turned away | R I |
| V102 | the chaser | an outgoing post tray on an office desk with three plain envelopes in it, address areas blank | R I |
| V103 | the gantry bolt | close on a heavy bolt fixed through the lower flange of a concrete bridge beam, drilled, the concrete cracked around it | R U |
| V104 | the viaduct, ordinary | the viaduct on an ordinary morning with traffic on it, seen from a residential street below, washing on a balcony in the foreground | **P** D C |
| V105 | the deck, level | the running surface of a two-lane motorway deck from driver height, concrete barriers on both sides, hills beyond | D C |
| V106 | the gap | two ends of a severed elevated road with nothing between them, seen from a distance across a valley, flat grey light, no debris and no vehicle in frame | R D C |

### ACT_5 — WHAT WAS DECIDED · V107–V116

| id | beat | prompt | flags |
|---|---|---|---|
| V107 | the barrier | a line of new steel crash barrier set across the full width of a road that simply stops, nothing beyond it, flat grey light | R D C |
| V108 | the emptied windows | a Ligurian apartment block directly beneath an elevated road, every window dark, shutters closed, nothing on the balconies | R D C |
| V109 | the cordon | a plastic cordon strung between two posts across a residential street, lifting in the wind, a resident standing well back on the pavement with their back to camera | **P** R D C |
| V110 | two reports | two thick bound documents lying side by side on a table, both covers blank, one noticeably thicker than the other | R I |
| V111 | the corridor of the court | a wide institutional corridor with a wooden bench along one wall, terrazzo floor, one figure seated far away | **P** D I |
| V112 | the bench | a worn wooden bench against a painted wall, empty, a folded coat left at one end | **P** R I |
| V113 | the files, stacked | a trolley of bound case files in an institutional corridor, spines blank, stacked high | R I |
| V114 | the room after | a plain public room with rows of chairs, one chair out of line, papers left on a seat, otherwise empty | **P** R D I |
| V115 | the calendar | a plain wall calendar in an office, its grid ruled, no dates and nothing written on it | R I |
| V116 | the reasons, unwritten | a thick ring binder standing open on a desk, every page in it blank, one lamp beside it | R I |

### ENDING — V117–V120

| id | beat | prompt | flags |
|---|---|---|---|
| V117 | the new bridge | a modern white steel-and-concrete motorway viaduct on slender elliptical piers crossing an urban valley, flat overcast daylight, no drama and no warm light | D C |
| V118 | the new deck | the running surface of a new motorway viaduct from driver height, ordinary traffic, hills and port cranes beyond | D C |
| V119 | the crossing, anywhere | an ordinary concrete road overbridge in a European town with traffic passing over it, seen from the road beneath, a pedestrian walking through the frame | **P** D C |
| V120 | the road that stops | the barrier across the severed road again, closer and held: worn asphalt, the line of steel barrier, the drop, and the city beyond it | R D C |

## 5. THE PEOPLE PLATES — the twenty-four

`V006 V016 V020 V021 V030 V045 V048 V060 V061 V076 V078 V079 V080 V094 V095 V098 V099 V100 V104
V109 V111 V112 V114 V119` — twenty-four plates that carry a human figure directly, which meets the
spec floor without variants.

Ten of them are in the **carve-out** and must stay as backs, hands and silhouettes with no face
resolved at all: `V006 V021 V045 V048 V060 V061 V094 V098 V099 V100`. The other fourteen —
residents, drivers, people at a bus stop and in a toll queue, 1960s construction workers, a
pedestrian now — **may have faces**, and should.

## 6. What must never be generated for this film — the checklist

- A face that reads as a specific real person. Any of the 43, any of the 13 injured, any family.
- Castellucci or any of the 32 convicted at first instance. Ferrazza or any of the 25 acquitted.
  Riccardo Morandi.
- **The collapse, in any form.** No falling deck, no falling vehicle, no car at a broken edge, no
  debris field, no dust cloud.
- Rescue, casualty, injury, hospital, funeral, grave, mourner, memorial with a face.
- A readable document, form, drawing, sign, headline, number or signature. **Every glyph is
  composited in Remotion.**
- A gavel, scales, jury box, judge's bench, handcuffs.
- American highway signage, US route shields, US number plates, right-hand-drive traffic, a UK or
  Asian street.
- Vineyards, cypresses, Tuscan hills, Amalfi, gondolas, Venice, the Colosseum, Roman ruins.
- A storm, lightning or rain presented as the moment of failure.
- Golden hour, sunset, blue hour. **This film has three light states and none of them is pretty.**

## 7. Paste files and the next step

```
py -3.11 scripts/check_image_order_neg.py --file episodes/_planning/EP76_morandi_CODEX_BATCH_A.v001.md
py -3.11 scripts/export_codex_batch_paste.py --order episodes/_planning/EP76_morandi_CODEX_BATCH_A.v001.md --per-batch 8
py -3.11 scripts/check_prompt_diversity.py
```

**Before any plate enters a cut**, the human review the contract requires: `footage_review_required`
is `true`, and a labelled contact sheet of the viaduct, underside, paperwork and present-day
registers must be opened by a person. The shelf's own labels are known to be wrong, and a plate that
nobody looked at is a plate nobody can vouch for.
