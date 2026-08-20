# EP75 · LAHAINA — IMAGE ORDER (BATCH A) v001

**132 reconstruction plates, `H001`–`H132`.** Every prompt is `[STYLE]` + the subject in the table +
`[NEG]`. Nothing in this order may contradict `EP75_lahaina_FACTS_LEDGER.v001.md` or `.v002.md`, and
the ⛔ rules there bind these images exactly as they bind the narration. Design is
`EP75_lahaina_FILM_BIBLE.v001.md`; the machine contract is
`episodes/PD-2026-075-lahaina/episode_spec.v001.json`.

## 0. Who generates these, and at what size

- **Long edge ≥ 3840 px, 16:9.** `remotion/public/lahaina/img` is the render truth and the pre-render
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

## 0.5 THIS EPISODE IS CONTEMPORARY, AND THAT IS THE WHOLE PROBLEM

EP72 was rural Quebec in 2013 and the shelf's European bias worked in its favour. **This one inverts.**
The subject is a real place three years ago, it is one of the most photographed holiday destinations
on earth, and **every query in this episode will return holiday footage.** Nothing here is a period
problem. Everything here is a **register and place** problem.

- **Hawaiʻi is the United States.** US number plates, US flags, US uniforms, US fire and police
  apparatus are all *correct*. What is wrong is a **mainland street** standing in for a Pacific town.
- The town is a narrow coastal shelf with a **steep dry mountain wall directly behind it**. Not a
  plain, not a valley floor, not a coastal city.
- The vegetation that burns is **dry non-native grass on abandoned plantation land, and low scrub**.
  **Never conifer, never pine, never crown fire, never snow.**
- The houses are **single-storey plantation-era timber with corrugated metal roofs**, jalousie
  windows, carports, **chain-link fences**, low lava-rock walls, utility poles with many crossarms.
- **No Hawaiian cultural imagery, ever, as decoration.** No hula, no lei, no kahili, no petroglyph, no
  ceremony. It is not scenery and it is not a substitute for anything.
- **The ocean appears only as a direction**, shot flat and grey, never at golden hour, never as
  beauty. **The film never opens on the sea.** ⛔-12.

## 1. The bars

**Depicted people are required** — **twenty-four plates carry a human figure directly**, which meets
the spec floor of twenty-four **without depending on the five variants** in §5. With those variants
the people lane is twenty-nine. What is barred absolutely is the **likeness of a real, identifiable individual**.

| never depicted as a person | why |
|---|---|
| **Any of the 102 who died** | ⛔-07. Not named, not shown, not characterised. **No burned vehicle that reads as containing anyone** |
| **Any named official** — the agency administrator, the EOC director, the duty officer, the chiefs, the Attorney General | ⛔-17. They exist in this film as roles and as composited typography, never as a portrait |
| **The officer at the gate; the operator whose house burned; the dispatchers** | ⛔-17. Narrated as actions. Never a face with a caption naming what that person did |
| **Any identifiable firefighter or police officer** | Silhouette and distance. **No readable insignia, no badge number, no unit marking** |

**Six categories must never be produced as an image at all, in any style.**

1. **No casualty, no rescue, no grief.** No body, no remains, no body bag, no injured person, no
   blood, no stretcher, no ambulance interior, no hospital, no funeral, no grave, no mourner, no
   memorial carrying a face. ⛔-07
2. **No fire with a person in the frame.** The fire in this film is **grey-brown smoke, a plume on a
   ridge, light on the underside of cloud, and a street lost in smoke with nobody in it.** Never a
   burning building with a figure in it, never a person running from flames. ⛔-07, spec
   `forbidden_subjects`
3. **No document facsimile, and no screen facsimile.** Every card, form, log, sheet, folder, alert and
   phone display in this order is **blank or ruled**; all typography is composited in Remotion. A
   generated glyph is a fabricated record and is one of the four classes that stop a ship.
4. **No holiday register in any form.** No resort, no turquoise water, no white sand, no sunset palm,
   no pool, no luau, no surfing, no cocktail, no drone-over-hotel, no cruise ship, no honeymooners.
   This is 25 of the spec's 65 `forbidden_subjects` and it is the single most likely way this episode
   goes wrong.
5. **No conspiracy iconography.** No beam from the sky, no energy weapon, no laser, no UFO, no
   unexplained light source, no "anomalous" glow, no arrow-and-circle graphic. This topic shares its
   search terms with that audience and **the film must be impossible to mistake for it.** ⛔-04
6. **No courtroom furniture.** No gavel, no scales of justice, no jury box, no judge's bench, no
   handcuffs. The law appears as a corridor, a bench, a stack of files and a blank form.

## 2. House look — four light states

The film is one day, and the day changes four times. **State letters are `W` `S` `N` `O`.**

**`W` — WIND DAY.** Before the fire, and the whole of ACT_1's forecast material. Hard flat leeward
daylight, a very high sun, dust in the air, grass and leaves moving hard in every frame, shadows
short and sharp. Bright, dry, ordinary, and completely unromantic. Nothing here looks like a warning.

**`S` — SMOKE.** From 14:55. The sun is up but you cannot see it. Grey-brown flat light, low
contrast, no orange, no ember glamour, visibility falling as the act runs. **The single most
important instruction in this order: the afternoon is GREY, not orange.** Fire photography's default
is a warm hero light and it is wrong for this film.

**`N` — NIGHT.** From about 20:00. Sodium street light where poles still stand, vehicle headlights,
beacon light, and everything else black. Smoke lit from below. **No flame nearer than mid-distance.**

**`O` — OVERCAST AFTER.** The investigation, the record, the town now. Cold flat daylight, muted grey
and rust, ash grey-white, oxidised steel, no shadow of any strength.

The film moves W → S → N → O once each, in that order, and never goes back.

## 3. Global prompts

**`[STYLE]`** — prepend to every plate:

> cinematic still, photographic, documentary, the leeward west coast of Maui in the Hawaiian Islands, United States, contemporary 2023 — a small low-rise Pacific town on a narrow coastal shelf with a steep dry mountain wall rising directly behind it, single-storey plantation-era timber houses with corrugated metal roofs and jalousie windows, carports, chain-link fences, low lava-rock walls, timber utility poles carrying many crossarms, two-lane roads, dry pale non-native grass and low scrub on abandoned plantation slopes, muted natural colour, low contrast but never crushed: shadows keep their detail and the frame reads clearly on a phone screen, restrained documentary framing, people small in frame and never posed, worn unglamorous ordinary surfaces — ash, corrugated steel, oxidised galvanised metal, melted aluminium, chain-link wire, dry grass, painted breeze block, laminate desk, ruled card, kiawe bark — nothing staged for advertising, no tourism, no scenery, ultra-detailed, photoreal, 4K, long edge 3840 or greater, 16:9, fine film grain, no text, no lettering, no numerals, no watermark, no logo, no readable signage

**`[NEG]`** — append to every plate. This is the canonical negative and it carries all five families
`scripts/check_image_order_neg.py` requires:

> text, lettering, readable text, legible text, numerals, numbers, digits, house numbers, street numbers, handwriting, cursive, signature, legible signature, seals, seal, emblems, emblem, logos, logo, badge, insignia, unit marking, wordmarks, name plates, licence plate, registration plate, identifiable person, recognisable person, recognizable person, likeness of a real individual, portrait of a named person, celebrity, public figure, deepfake, body, corpse, human remains, body bag, injured person, blood, burn victim, stretcher, paramedic, ambulance interior, hospital, funeral, grave, mourner, crying, grieving family, person running from flames, people fleeing fire, firefighter carrying person, cpr, rescue, resort, hotel, beach holiday, beach vacation, turquoise water, white sand beach, sunset palm, palm silhouette, palm trees, tropical paradise, luau, hula, lei greeting, tiki, surfing, surfer, snorkeling, scuba, swimming pool, cocktail, sunbathing, tourist selfie, honeymoon, cruise ship, drone over hotel, golf course, whale watching, directed energy weapon, energy beam, laser from sky, beam from the sky, ufo, conspiracy graphic, anomalous glow, movie explosion, action movie, video game, fireball vfx, fire with people in frame, pine forest fire, conifer forest, pine trees, spruce, crown fire, snow, desert, megacity skyline, skyscrapers, european street, asian cityscape, EU number plate, right-hand-drive traffic, mainland american main street, US route shield, expressway interchange, gavel, scales of justice, jury box, judge's bench, courtroom interior, handcuffs closeup, prison bars, money rain, falling banknotes, stock ticker, candlestick chart, memorial portrait, photo memorial, golden hour, sunset glow, orange hero light, warm firelight glamour, postcard scenery, glossy advertising lighting, flat CGI, 3D render, cartoon, illustration, oversaturated, HDR halo, watermark

**Faces are allowed, and wanted.** The `[NEG]` deliberately does **not** contain `human face`,
`facial features`, `eye contact` or `headshot`. The owner's decision of 2026-07-04 is that depicted
people are required; EP71 and EP72 both keep those tokens out for the same reason. What is barred is
**identifiability**, not the existence of a face.

So: **a generated face is fine. A face that reads as a specific real person is not.**

**The carve-out this episode keeps.** Four roles in this film map to real, identifiable, living
individuals whose actions are described in the narration: **the emergency-management administrator,
the EOC duty staff, the police officer at the gate, and the ladder-company operator whose house
burned.** A resolved face attached to one of those roles is a likeness claim whatever the prompt
says. Those roles stay as backs, hands and silhouettes — `H055 H082 H083 H103 H104 H105 H121`.
**Everyone else in this film — the residents, the drivers in the traffic, the linemen, the
firefighters at distance, the figures on the street now — may have faces.**

## 4. THE PLATE ORDER

**Columns.** `id` · `beat` — the script span it serves · `prompt` — the subject · `flags`:
`P` = people plate (a human figure, never identifiable) · `R` = carries the on-screen
**RECONSTRUCTION** label for its full duration · `D` = built for the depth-parallax pass ·
`W`/`S`/`N`/`O` = light state.

> **`R` is the default, not the exception.** This is a real event three years old for which real
> photographs exist, and invariant 11 bars presenting a generated image as an authentic record. Every
> plate that depicts **the day itself, the town, or the fire** carries `R`. Only abstract grounds,
> hardware studies and present-day material are without it.

### HOOK — H001–H008 · *"Three o'clock on a Tuesday afternoon…"*

| id | beat | prompt | flags |
|---|---|---|---|
| H001 | dry grass, wind in it | dry pale knee-high grass on a steep slope filling the frame, bent hard and all one way by strong wind, seed heads blurred by movement, a hard high sun, no sky | R D W |
| H002 | the slope above the town | a steep dry grass and scrub hillside seen from below, an abandoned plantation terrace line crossing it, a few dark kiawe trees, roofs just visible at the bottom edge | R D W |
| H003 | the engine stops | a modern American fire engine standing on a dirt shoulder at the edge of dry grassland, dust still hanging around its wheels, doors open, seen from behind and slightly below | R S |
| H004 | boots on ash and dirt | work boots and the lower legs of a standing figure on scorched dirt and gravel, dry grass stems at the frame edge, hard daylight, shot from ground height | **P** R D W |
| H005 | a hand on the radio | a bare hand holding a portable radio up near a shoulder, close, the microphone cord across the frame, no face in frame, bright flat light | **P** R S |
| H006 | the first smoke, low | a low grey-brown smoke front moving fast and flat across dry grassland, pressed down almost horizontal by wind, no flame visible anywhere in frame | R D S |
| H007 | the town below, grey | a small low-rise coastal town seen from the dry hillside above it, corrugated roofs in a loose grid, the sea beyond flat and grey under a colourless sky, smoke haze across the middle distance | R D S |
| H008 | a phone in a hand, blank | a hand holding an ordinary smartphone at waist height, the screen completely blank and dark, outdoors in flat daylight, shallow depth of field, no face in frame | **P** R S |

### OP — H009–H014

| id | beat | prompt | flags |
|---|---|---|---|
| H009 | the pole, hero one | a galvanised steel pole carrying a cluster of grey civil-defence warning siren horns, seen from below against a flat pale overcast sky, nothing else in frame | R D O |
| H010 | the pole, hero two | the same siren head from level with it and further back, the pole running out of the bottom of frame, a dry hillside blurred behind | R D O |
| H011 | the pole in its place | a warning siren pole standing beside a two-lane coastal road with a low sea wall behind it, ordinary, unremarkable, flat grey daylight | R D O |
| H012 | the wall map | a large plain wall map of an island group in a municipal office, small plain markers dotted along its coastlines, no lettering anywhere, one desk lamp | R O |
| H013 | the network, abstract | an evenly lit dark grey matte surface with a faint scatter of small pale dots across it, no pattern, no text, no map outline | O |
| H014 | black ground | a plain matte near-black surface with faint horizontal grain, evenly lit, empty | O |

### ACT_1 — THE SOUND THEY KNEW · H015–H038 · *"Hawaiʻi has more outdoor warning sirens…"*

| id | beat | prompt | flags |
|---|---|---|---|
| H015 | the horn cluster, macro | extreme close-up of a cluster of grey painted steel siren horns, weather staining and salt corrosion around the bolts, flat sky behind | R O |
| H016 | the drive unit | the motor and drive housing of an outdoor warning siren at the top of a steel pole, cabling entering it from below, close, clear detail | R O |
| H017 | the base | the concrete base of a warning siren pole with a locked grey steel cabinet bolted to it, weeds at the foot, blank cabinet door | R D O |
| H018 | monthly test, frame one | a warning siren pole against an empty pale sky, seen from a fixed low angle, early morning light, nothing else in frame | R D W |
| H019 | monthly test, frame two | the identical framing of the same siren pole with a higher, harder sun and a shorter shadow | R D W |
| H020 | monthly test, frame three | the identical framing of the same siren pole under flat overcast, colours muted | R D O |
| H021 | monthly test, frame four | the identical framing of the same siren pole with thin cloud crossing behind it, late flat light, still no drama | R D O |
| H022 | the street hears it | an ordinary residential street of single-storey timber houses with corrugated roofs and chain-link front fences, empty of people, mid-morning, a siren pole small in the distance | R D W |
| H023 | a radio on a counter | a small mains-powered radio standing on a kitchen counter beside a jar and a folded cloth, dial and speaker grille plain, no lettering, domestic morning light | R O |
| H024 | the published page | a plain sheet of white paper lying squared on a laminate desk, entirely blank, one lamp raking across it, a pen beside it | R O |
| H025 | the hazard list, ground | a sheet of pale enamelled steel signage bolted flat to a wall, entirely blank, one rivet at each corner, salt-weathered around the edges, shot straight on | R O |
| H026 | a hillside of fuel | a wide of dry pale grassland running up a leeward mountain slope, old plantation terracing still visible under it, dark scrub in the gullies, hard sun | R D W |
| H027 | the fuel, close | close on dry pale grass stems and dead thatch at ground level, brittle, sun-bleached, a few small stones, shallow depth of field | R W |
| H028 | wind in the trees | dark kiawe and scrub trees bending hard in strong wind on a dry slope, leaves blurred, sky bleached white | R D W |
| H029 | the forecast desk | a plain office workstation with two blank dark monitors, a keyboard and a mug, blinds half drawn, no person, flat interior light | R O |
| H030 | a hand at the desk | a hand resting beside a keyboard on a desk in an office, close, a blank monitor edge in frame, no face | **P** R O |
| H031 | the chart, blank | a plain white sheet of paper with faint printed grid lines and nothing plotted on it, on a desk under a lamp | R O |
| H032 | the storm at distance | a very distant band of high cloud over open ocean seen from a dry hillside, the sea flat and grey, no drama, no golden light | D W |
| H033 | pressure, abstract | a smooth dark grey gradient surface with faint parallel banding running diagonally, no text, no symbols | O |
| H034 | the wind arrives | dry grass and dust streaming across a two-lane road surface in strong wind, seen at road height, nothing else moving | R D W |
| H035 | dust off the slope | a plume of pale dust lifting off a bare dry hillside and streaming sideways, hard midday sun | R D W |
| H036 | the town, ordinary | a low-rise Pacific town street on an ordinary bright weekday, a few parked pickups, corrugated roofs, power lines overhead, nobody in shot | R D W |
| H037 | an ordinary Tuesday | a small corner shop front on a two-lane road, roller shutter half up, a plastic chair outside, no signage legible, hard flat sun | R D W |
| H038 | the warning nobody reads | a plain municipal noticeboard behind glass on a post beside a pavement, the board inside completely blank, dry grass behind it | R O |

### ACT_2 — THE MORNING · H039–H064 · *"The fires started before dawn…"*

| id | beat | prompt | flags |
|---|---|---|---|
| H039 | before dawn | a two-lane road running toward a dark mountain wall before sunrise, the sky just going pale grey, street lights still on, no traffic | R D N |
| H040 | upcountry, far off | a distant orange-brown smoke column rising off a high dark ridge before dawn, seen from many miles away across dark farmland, no flame visible | R D N |
| H041 | the pole and the grass | a timber utility pole with several crossarms standing in unmown dry grass at the edge of a road, the grass growing right up the base of the pole | R D W |
| H042 | pole 25, the ground | close on dry grass and dead thatch at the foot of a timber utility pole, the pole butt weathered and stained, hard early light | R W |
| H043 | the line, broken | a broken overhead electrical conductor hanging down from a crossarm and swinging, seen against a bleached white sky, no ground in frame | R W |
| H044 | the crossarm | close on the top of a timber utility pole — crossarm, insulators, tie wire — against flat sky, no lettering anywhere | R W |
| H045 | slack line, swaying | overhead power lines running between poles, visibly slack and moving in wind, seen from below along the road | R D W |
| H046 | first smoke, morning | a thin grey smoke column rising off a dry slope in early morning light and immediately being bent flat by wind | R D W |
| H047 | the engine at the gate | an American fire engine standing at a wire farm gate on a dirt track at the foot of a dry hillside, morning, doors closed | R W |
| H048 | the dozer | a private tracked bulldozer working a firebreak through dry grass on a slope, dust behind it, the operator a shape in the open cab too distant to resolve, seen from far off | **P** R D W |
| H049 | the water tender | a large water tanker truck parked on a dirt track beside burned ground, hose run out across the dirt, no people | R W |
| H050 | hose on the burn | a charged hose line lying across scorched black ground, water darkening the ash around the nozzle, no person in frame | R W |
| H051 | the burn, cold | a wide of burned black hillside under hard morning sun, no smoke at all, no flame, ash and blackened grass stubble, absolutely still | R D W |
| H052 | walking the burn | a figure walking across burned black ground on a slope, small in frame, seen from behind, hard shadow | **P** R D W |
| H053 | ash underfoot | close on scorched ground — grey ash, black grass stubble, a few unburned stems at the edge — shot from standing height looking down | R W |
| H054 | the gulch | a dry rocky gulch running down a hillside with a fallen utility pole and slack wires lying across it, dry brush on both banks | R D W |
| H055 | the officer looks | the back and shoulder of a standing figure in work clothing looking out across burned ground, seen from behind, no face, hard light | **P** R D W |
| H056 | 05:40, the intersection | a two-lane road intersection at first light with a broken utility pole down across the northbound lanes and wires on the road surface, no vehicles yet | R D N |
| H057 | traffic cones | traffic cones and a temporary barrier across one lane of a road with a downed line beyond, flat early light, nobody in frame | R D W |
| H058 | the queue begins | a line of stationary cars on a two-lane road seen from behind at windscreen height, brake lights on, dust in the air | **P** R D W |
| H059 | mauka | a steep dry mountain wall rising directly behind low corrugated roofs, seen from a street, the slope filling the top two-thirds of the frame | R D W |
| H060 | makai | a two-lane road running downhill straight toward a flat grey sea, low buildings on both sides, the horizon high and colourless | R D W |
| H061 | the cell mast | a lattice communications mast on a low ridge above a town, seen against a bleached sky, dry grass at its base | R D W |
| H062 | the phone, no service | close on a smartphone held in one hand, screen dark and blank, the hand lowering it, blurred street behind, no face | **P** R S |
| H063 | the shelter, empty | the interior of a municipal recreation hall with a stack of folded cots against one wall and rows of empty stacking chairs, strip lighting, nobody | R D O |
| H064 | the station bay, empty | an empty fire station apparatus bay with the roller door up, oil-stained concrete floor, a coiled hose on a rack, no vehicle, no people, midday | R D W |

### ACT_3 — THIRTY-EIGHT MINUTES · H065–H088 · *"Thirty-eight minutes."*

| id | beat | prompt | flags |
|---|---|---|---|
| H065 | the empty shoulder | a dirt shoulder beside a dry field with tyre tracks in it and nothing else, hard early-afternoon sun, absolutely still | R D W |
| H066 | the ground, watched | a patch of burned black ground close up under hard sun, faint heat shimmer above it, no smoke, no glow | R W |
| H067 | grass, moving again | dry grass on a slope pressed flat and streaming in a sudden gust, seed heads torn loose and flying, hard light | R D W |
| H068 | 14:55, first smoke | a fast low grey smoke front crossing dry grassland close to the ground, wind-flattened, a dark scrub line beyond, no flame | R D S |
| H069 | twenty by a hundred | a small elongated patch of burning grass on a slope seen from perhaps forty metres, smoke coming off it flat and grey, no people | R S |
| H070 | the shed | a small corrugated metal garden shed at the edge of a dry lot with grey smoke coming from behind and above it, no flame visible | R D S |
| H071 | embers, dark ground | small orange embers scattered and streaking across a dark ashy ground surface, close, motion blurred by wind, nothing else lit | R S |
| H072 | embers, air | a scatter of small bright embers streaming through grey-brown smoke against a blown-out pale sky, no structure in frame | R S |
| H073 | the bypass | a modern two-lane bypass road cut across a dry slope, empty, with a grey smoke haze crossing it low | R D S |
| H074 | over the road | thick grey-brown smoke rolling low across a road surface, visibility down to a few car lengths, no vehicles, no figures | R D S |
| H075 | the park | a small municipal park with dry grass, a chain-link backstop and a bare climbing frame, grey smoke crossing behind it, nobody | R D S |
| H076 | the first houses | the backs of two single-storey timber houses with corrugated roofs seen across an unmown lot, heavy grey smoke behind their rooflines, no flame | R D S |
| H077 | vehicles alight | a parked pickup and a saloon car on a residential kerb with grey-brown smoke pouring past them and their paint blistering, **empty cabs clearly visible, doors open, nobody inside or nearby** | R S |
| H078 | the radio, cab | the interior of a fire apparatus cab from the passenger side — dash radio, handset on its hook, windscreen filled with grey smoke, no person | R S |
| H079 | command | a hand holding a radio handset up in a vehicle cab, close, the windscreen white with smoke beyond, no face in frame | **P** R S |
| H080 | the cut-off | a residential street running uphill, smoke thick across the top third, a hose line lying up the centre of the road, a single distant silhouette | **P** R D S |
| H081 | visibility gone | a street scene in which almost nothing resolves — a kerb line, a leaning pole, a suggestion of a roof — everything else flat grey-brown smoke | R D S |
| H082 | the console | an emergency operations workstation seen over a shoulder: two blank dark screens, a desk phone, a notepad with nothing written on it | **P** R O |
| H083 | the room | a plain municipal operations room with rows of desks, blank screens, a large blank wall board, strip lighting, two indistinct figures at the far end | **P** R D O |
| H084 | the alert, blank | a smartphone lying face up on a laminate desk with its screen lit plain white and completely empty of content, close, top-down | R O |
| H085 | the mast, dead | a lattice communications mast on a ridge with smoke crossing behind it, seen from below, no lights, no movement | R D S |
| H086 | the shelter door | the closed double doors of a municipal hall from outside, a plastic chair beside them, dry grass at the kerb, nobody | R D S |
| H087 | power off | a transformer on a timber pole seen from below against a smoke-white sky, the lines running away slack in both directions | R S |
| H088 | the clock ground | a section of unpainted concrete wall shot straight on, fine aggregate and form-board marks visible, one hairline crack running down it, nothing mounted on it | O |

### ACT_4 — EVERYTHING THAT WAS ALREADY THERE · H089–H110

| id | beat | prompt | flags |
|---|---|---|---|
| H089 | the ocean's edge | a low sea wall of dark rock at the bottom of a town street with flat grey water beyond it and grey smoke lying across the whole horizon, no people, no colour | R D S |
| H090 | the street, parked both sides | a narrow residential street with cars parked along both kerbs leaving barely one lane clear, single-storey houses, power lines overhead, empty of people | R D W |
| H091 | the dead end | a narrow residential street ending in a chain-link fence with dry scrub beyond it, no through route, flat hard light | R D W |
| H092 | eight ways out | a plain aerial-style view of a small grid town on a coastal shelf between a mountain wall and the sea, roads visible, no labels, no text | R D O |
| H093 | the gate, hero one | a galvanised chain-link gate closed across a dirt access track with a heavy padlock and chain on it, dry grass either side, seen straight on | R D W |
| H094 | the gate, hero two | the same padlock and chain close up, the wire diamonds of the gate filling the frame behind it, hard light | R W |
| H095 | the cars behind it | a line of stationary cars nose to tail on a dirt track, seen from in front and low, dust and grey smoke beyond them, windscreens reflecting flat sky | **P** R D S |
| H096 | the saw | a battery reciprocating saw held in two hands cutting into a padlock shackle, extreme close, sparks small and few, no face in frame | **P** R S |
| H097 | the tow strap | a nylon tow strap looped through chain-link wire and pulled taut, close, the wire deforming under it | R S |
| H098 | the shoulder | a chain-link gate leaf swinging open, seen from the side, the wire mesh blurred with movement, a figure's back and shoulder just entering the frame edge | **P** R D S |
| H099 | through the gate | the view along a dirt track away from an opened gate, cars moving away from camera, dust behind them, grey smoke beyond | **P** R D S |
| H100 | the fence, after | a section of chain-link fence pushed out of shape and standing open, dry grass, ash on the ground, flat cold light | R D O |
| H101 | the school gate | a locked galvanised gate across a paved access road beside a low institutional building, chain and padlock, nobody | R D W |
| H102 | the barrier | a steel bollard and a low concrete barrier blocking a dirt track between two lots, dry grass growing round them | R D W |
| H103 | hands on wire | two hands gripping chain-link wire from the inside, close, fingers hooked through the diamonds, no face | **P** R S |
| H104 | in the traffic | the interior of a car from behind the driver's seat, hands at the top of the wheel, the windscreen filled with stationary brake lights and grey smoke, no face | **P** R D S |
| H105 | the hydrant | a municipal fire hydrant at a kerb with a hose already connected and lying slack, a gloved hand on the operating nut, no face | **P** R S |
| H106 | a trickle | close on a fire hose coupling with only a thin stream of water running out of it onto ash-covered ground | R S |
| H107 | the main | an excavated trench in a road surface exposing a water main and a valve, plastic barrier either side, flat cold light | R D O |
| H108 | melted plumbing | close on melted and collapsed plastic pipework among ash and burned timber at ground level, oxidised copper beside it | R O |
| H109 | the tank | a large municipal water storage tank on a dry hillside, cylindrical, weathered paint, dry grass, flat grey sky | R D O |
| H110 | the slope, above | a wide still view of a dry mountain slope above a town, unmown grass and old plantation terracing, nothing happening, hard flat light | R D W |

### ACT_5 — WHAT THE REPORT WOULD NOT WRITE · H111–H128

| id | beat | prompt | flags |
|---|---|---|---|
| H111 | the volumes | three thick plain bound reports stacked on a desk, covers entirely blank, one lamp raking across them | R O |
| H112 | the open report | a thick bound document lying open on a desk, the pages blank and faintly ruled, a lamp at the frame edge | R O |
| H113 | a document ground, cream | a plain sheet of cream paper filling the frame, faint texture, evenly lit, entirely blank | R O |
| H114 | a document ground, board | a sheet of dark grey pressed fibreboard filling the frame, coarse fibre visible in raking light, one scuffed corner, nothing printed on it | R O |
| H115 | the server rack | a rack of storage servers behind a mesh door in a plain machine room, small indicator lights, no lettering | O |
| H116 | the evidence room | rows of plain document storage boxes on steel shelving in a windowless room, lids on, label areas blank | R O |
| H117 | the plain room | a plain municipal meeting room with a long table and stacking chairs, empty, blinds half drawn | D O |
| H118 | the pole returns | the same galvanised siren pole and horn cluster from ACT_1, framed identically, under colder flatter light | R D O |
| H119 | one of four | four warning siren poles standing in a line along a coastal road at wide intervals, seen along the road so they recede, flat grey sea beyond | R D O |
| H120 | the blank sheet, hero | a single ruled sign-in form lying alone and completely blank on a plain wooden table in an empty room, daylight from one side | R D O |
| H121 | the empty chair | a plain office chair pushed back from an empty desk in a municipal office, a blank notepad on the desk, nobody | **P** R D O |
| H122 | the folders | a stack of manila folders on a table, edges uneven, covers blank | R O |
| H123 | the filing cabinet | a grey steel filing cabinet with one drawer standing open and empty, in a plain office corner | R O |
| H124 | the envelope | a plain unmarked envelope lying on a laminate desk beside a telephone, blank | R O |
| H125 | the corridor | a wide institutional corridor with a wooden bench along one wall, empty, strip lighting | **P** D O |
| H126 | the bench | a worn wooden bench against a painted wall in a public building, empty, a folded coat left on one end | **P** R O |
| H127 | the building | a plain mid-century public building seen from across a street under flat overcast, no signage legible, no people | D O |
| H128 | the ledger ground | a plain ruled accounts page filling the frame, columns empty, nothing written | R O |

### ENDING — H129–H132

| id | beat | prompt | flags |
|---|---|---|---|
| H129 | the sheet, held | the same blank ruled form on the same plain table, framed slightly wider, the room's floor and skirting visible, nothing else | R D O |
| H130 | the town now | a rebuilt two-lane street in a low-rise Pacific town under flat overcast, new kerbs, young planted trees, a few people at a distance, none identifiable | **P** D O |
| H131 | the wall that stood | a low lava-rock wall standing alone on a cleared lot with ash-grey ground around it and dry grass returning at its base, flat cold light | R D O |
| H132 | the radio, last | the small mains radio from ACT_1 on a kitchen counter, framed identically, colder light, the room otherwise empty | R O |

## 5. THE PEOPLE PLATES — twenty-four directly, twenty-nine with variants

The spec floor is **24** (`people_plates_min`), and **this order meets it in the table itself**, so
the floor does not depend on anything being produced later:

```
H004 H005 H008 H030 H048 H052 H055 H058 H062 H079 H080 H082
H083 H095 H096 H098 H099 H103 H104 H105 H121 H125 H126 H130
```

That is **twenty-four carrying a figure directly**. **Five more are wanted** and are to be produced as
variants of `H058`, `H080`, `H095`, `H099` and `H130` with a **different figure position and a
different number of figures** — never a different named person, because no plate resolves one.

**The seven identifiability-restricted plates** — `H055 H082 H083 H103 H104 H105 H121` — are backs,
hands, silhouettes and empty chairs, because the roles they serve map to real named individuals whose
actions the narration describes. **The other twenty-one may have faces**, and should: a town that
never shows a face is a town the audience does not believe in.

## 6. What must never be generated for this film — the checklist

- A person who could be recognised as a specific real individual.
- Any of the 102. Any casualty, remains, body bag, injury, grief or memorial-with-a-face.
- **A burned vehicle that reads as occupied.** `H077` is written with open doors and visible empty
  cabs for exactly this reason, and it is the only burning-vehicle plate in the order.
- **Fire with a person in frame.** Anywhere. In any plate.
- **Orange hero light on the afternoon.** The afternoon of 8 August is `S` — grey-brown — and a warm
  cinematic firelight pass would falsify the single most important visual fact in the film.
- A readable document, form, log, screen, alert, sign, placard, licence plate, headline or
  handwriting.
- **Anything that could read as a beam, a directed energy source, or an unexplained light.**
- A gavel, scales, jury box, judge's bench, handcuffs.
- Resort, turquoise water, white sand, sunset palm, pool, luau, hula, surfing, cocktail, cruise ship,
  drone-over-hotel, honeymooners, golf.
- Conifers, pine, spruce, crown fire, snow, desert, a megacity skyline, a European or Asian street, a
  mainland-US main street.
- Golden hour. **This film has four light states and not one of them is pretty.**

## 7. Paste files, the checks, and the next step

Paste files are **not** generated in this pass. The next agent runs the established split —
`EP75_lahaina_CODEX_PASTE/batch_01.txt … batch_17.txt`, eight plates each — and **verifies before
commissioning anything**:

```
py -3.11 scripts/check_image_order_neg.py --file episodes/_planning/EP75_lahaina_CODEX_BATCH_A.v001.md
py -3.11 scripts/check_prompt_diversity.py episodes/_planning/EP75_lahaina_CODEX_BATCH_A.v001.md
```

Then, in order:

1. **Codex generates. 1672×941.** One prompt, one image, into a new folder.
2. **Upscale every plate to 3840×2160** with a per-episode clone of
   `upscale_oroville_4k_esrgan_v001.py` **before the plates enter the pool.** Not after. EP71 is the
   proof of what happens otherwise.
3. **A person opens a labelled contact sheet** of the grass, smoke, street and gate registers before a
   single plate enters a cut. `footage_review_required` is `true` in the spec, the factory shelf's
   labels are known to be wrong, and no gate in this pipeline has ever looked at an image.
4. `check_plate_verdicts.py` — and note that a `REJECT` recorded but not acted on is now a
   **ship blocker** (`pd_ship_policy.plate_verdict_rows`). Regenerate or exclude; do not leave a
   rejected plate in the pool.
