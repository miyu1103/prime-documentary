# EP72 · LAC-MÉGANTIC — IMAGE ORDER (BATCH A) v001

**120 reconstruction plates, `L001`–`L120`.** Every prompt is `[STYLE]` + the subject in the table +
`[NEG]`. Nothing in this order may contradict `EP72_lacmegantic_FACTS_LEDGER.v001/v002/v003.md`, and
the ⛔ rules there bind these images exactly as they bind the narration.

## 0. Who generates these, and at what size

- **Long edge ≥ 3840 px, 16:9.** `remotion/public/lacmegantic/img` is the render truth and the
  pre-render gate refuses anything under it.
- **Known constraint, measured 2026-08-20:** Codex's built-in image generation is **fixed at
  1672×941** and cannot be prompted out of it. A native-4K path is preferred. Where one is not
  available, the sanctioned fallback is the one proven on EP71 the same day:
  `scripts/upscale_oroville_4k_esrgan_v001.py` — Real-ESRGAN x4plus to 6688×3764, then a LANCZOS
  reduction to exactly 3840×2160. Clone it per episode. **A plain 2× enlargement is not acceptable**
  and does not even clear the floor.
- **One prompt, one image.** No variants to choose from, no `b` versions.
- Deliver to a NEW folder. Nothing existing is overwritten; the old set is retired, never deleted.

## 1. The bars

**Depicted people are required** — twenty plates carry a human figure. What is barred absolutely is
the **likeness of a real, identifiable individual**, and in this film that has names attached.

| never depicted as a person | why |
|---|---|
| **Thomas Harding, Richard Labrie, Jean Demaître** | Acquitted of criminal negligence causing death, January 2018 (LM-35). ⛔-01 |
| **Any of the 47 who died** | ⛔-05. Not named, not shown, not characterised |
| **Any identifiable firefighter, investigator, official, juror or executive** | Silhouette and distance only. No insignia, no unit marking |

**Four categories must never be produced as an image at all, in any style.**

1. **No casualty and no rescue.** No body, no injured person, no blood, no stretcher, no ambulance
   interior, no hospital, no funeral, no grave, no mourner. ⛔-05
2. **No fire with a person in the frame.** The fire is light on rooftops, smoke crossing a lamp, and
   reflection at a distance. Never a burning building with a figure in it. ⛔-10
3. **No document facsimile.** Every card, page, folder, placard and report in this order is
   **blank or ruled**; all typography is composited in Remotion. A generated glyph is a fabricated
   record and is one of the four classes that stop a ship.
4. **No courtroom furniture.** No gavel, no scales of justice, no jury box, no judge's bench, no
   handcuffs. The law appears as a corridor, a bench, a stack of files and an empty chair.

## 2. House look — two light states

**State A — SODIUM.** The night of 5–6 July 2013. Yard floodlight and sodium street light, wet
ballast, black tank car flanks, deep shadow that keeps its detail, spruce edges going blue-black.
Amber and cyan only where a real lamp puts them. This is ACT_1's shop, all of ACT_2 and ACT_3.

**State B — OVERCAST DAY.** Everything else: the 2012 shop by day, the loading rack, the wreck site,
the offices, the town now. Flat July-to-October daylight in inland Quebec, low contrast, muted green
and grey, no golden hour anywhere.

The film moves from A to B once, at the top of ACT_4, and the audience should feel the change.

## 3. Global prompts

**`[STYLE]`** — prepend to every plate:

> cinematic still, photographic, the Estrie region of Quebec, Canada — a small lakeside mill town, low forested hills, spruce and birch, a single-track freight railway running through inhabited streets, contemporary and specifically 2012 to 2018, muted natural colour, low contrast but never crushed: shadows keep their detail and the frame reads clearly on a phone screen, restrained documentary framing, people small in frame and never posed, worn unglamorous ordinary surfaces — wet ballast, creosoted sleepers, black tank car steel, galvanised handrail, painted breeze block, laminate desk, manila card, spruce bark — nothing staged for advertising, ultra-detailed, photoreal, 4K, long edge 3840 or greater, 16:9, fine film grain, no text, no lettering, no numerals, no watermark, no logo, no signage

**`[NEG]`** — append to every plate. This is the canonical negative and it carries all five families
`scripts/check_image_order_neg.py` requires:

> text, lettering, readable text, legible text, numerals, numbers, digits, house numbers, handwriting, cursive, signature, legible signature, seals, seal, emblems, emblem, logos, logo, badge, insignia, wordmarks, name plates, licence plate, registration plate, identifiable person, recognisable person, recognizable person, likeness of a real individual, portrait of a named person, celebrity, public figure, deepfake, body, corpse, injured person, blood, burn victim, stretcher, paramedic, ambulance, hospital, funeral, grave, mourner, crying, rescue, search and rescue, gavel, scales of justice, lady justice, jury box, judge's bench, courtroom interior, handcuffs, firearm, prison bars, american highway sign, US route shield, EU number plate, right-hand-drive traffic, european street, asian street, megacity skyline, skyscrapers, expressway interchange, palm trees, beach, surf, ocean, tropical, desert, cruise ship, high speed train, passenger train interior, subway, steam locomotive, crash test, action movie explosion, fireball with people, video game, golden hour, sunset glow, postcard scenery, christmas, wedding, handshake, money rain, falling banknotes, stock ticker, candlestick chart, glossy advertising lighting, flat CGI, 3D render, cartoon, illustration, oversaturated, HDR halo, watermark

**REVISED 2026-08-21 — faces are allowed, and wanted.** The first draft of this order put
`human face`, `facial features`, `eye contact`, `headshot` and `profile of a face` into the `[NEG]`.
That was stricter than the channel's own standard and it suppressed the people lane. The owner's
decision of 2026-07-04 is that **depicted people are required and welcome**; EP71's order says the
same in terms, and deliberately keeps those tokens out. What is barred is **identifiability**, not
the existence of a face.

So: **a generated face is fine. A face that reads as a specific real person is not.**

**The one carve-out this episode keeps, and it is not about faces in general.** Five roles in this
film map to real, named, living or recently-tried individuals: **the locomotive engineer, the rail
traffic controller, the operations manager, the company's chairman, and any of the 47 who died.**
A resolved face attached to one of those roles is a likeness claim whatever the prompt says. Those
five roles stay as backs, hands and silhouettes (`L003 L004 L015 L039 L041 L042`). **Everyone else
in this film — the taxi driver, the firefighters at distance, the townspeople, the office and yard
workers, the figures on the rebuilt street — may have faces**, and the people plates should be
re-commissioned that way.

## 4. THE PLATE ORDER

**Columns.** `id` · `beat` — the script span it serves · `prompt` — the subject · `flags`:
`P` = people plate (a human figure, never identifiable) · `R` = carries the on-screen
**RECONSTRUCTION** label for its full duration · `D` = built for the depth-parallax pass ·
`A`/`B` = light state.

### HOOK — L001–L006 · *"Shortly before midnight…"*

| id | beat | prompt | flags |
|---|---|---|---|
| L001 | the line behind the houses | a single-track railway line running behind a row of modest clapboard houses at night, one kitchen window lit, long grass to the ballast edge, no people | R D A |
| L002 | flame at distance | the front of a parked diesel locomotive seen from perhaps eighty metres, a small orange flame and thick smoke rising from the roof above the nose, everything else in darkness | R A |
| L003 | boots on gravel | work boots and the lower legs of a standing figure on wet railway ballast, lit from one side by a distant floodlight, shot from ground height | **P** R D A |
| L004 | a hand on a valve | a bare hand resting on a large steel valve wheel on the end of a tank car, close, shallow depth of field, no face in frame | **P** R A |
| L005 | the line of cars | a line of black tank cars receding into darkness under widely spaced yard floodlights, wet rail catching the light | R D A |
| L006 | the town below | a small town at night seen from a low hill above it, street lights in a grid, a dark lake beyond, no movement | D A |

### OP — L007–L010

| id | beat | prompt | flags |
|---|---|---|---|
| L007 | the grade | a railway line running downhill through spruce and cleared farmland, seen from beside the track so the fall of the grade is visible, dusk | D A |
| L008 | the patch | extreme close-up of a grey-brown polymeric repair compound filling a machined recess in cast iron, slightly glossy, tool marks around it | R B |
| L009 | the wheel | a cast-iron hand-brake wheel on the end platform of a freight car, weathered, rust in the spokes, chain visible below | R D A |
| L010 | black ground | a plain matte near-black surface with faint horizontal grain, evenly lit, empty | B |

### ACT_1 — THE REPAIR · L011–L030 · *"In October of 2012…"*

| id | beat | prompt | flags |
|---|---|---|---|
| L011 | the shop, outside | a small railway locomotive repair shop at dusk, corrugated walls, sliding doors half open, one locomotive nose visible inside | R B |
| L012 | the shop, inside | the interior of a locomotive shop, overhead gantry, tools on a bench, a locomotive with body panels removed, empty of people | R B |
| L013 | the engine opened | a large diesel engine block opened for repair, cylinder liners visible, oil-darkened metal, work light clamped to the frame | R B |
| L014 | the bearing | macro of a cast steel bearing shell seated in a machined housing, one hairline crack running across it | R B |
| L015 | the bolt | a torque wrench on a bolt head, close, a gloved hand at the edge of frame | **P** R B |
| L016 | the compound | an open tub of grey-brown two-part repair compound with a mixing stick across it on a workbench | R B |
| L017 | curing | the same repair, some hours later, matte and hardened, a work light raking across it | R B |
| L018 | back outside | a locomotive standing outside a repair shop at first light, hood doors closed, exhaust haze above the stack | R B |
| L019 | the yard, morning | a small freight yard on an overcast morning, three tracks, weeds in the ballast, no people | D B |
| L020 | the loading rack | an oil loading rack at a rail terminal, articulated arms lowered into the domes of black tank cars, flat daylight | D B |
| L021 | the coupling | close on a knuckle coupler joining two tank cars, slack chains, wet steel | B |
| L022 | the dome | the top of a tank car — walkway, dome cover, handrail — from above and slightly behind | D B |
| L023 | the consist | a very long line of black tank cars from a low three-quarter angle, receding until it blurs | D B |
| L024 | the buffer car | a single boxcar coupled between locomotives and tank cars, its paint faded, seen side-on | B |
| L025 | the cab, empty | the interior of a diesel locomotive cab, control stand, brake handles, a seat, no person, dim | R D B |
| L026 | the throttle | close on a locomotive control stand: throttle lever, reverser, two brake handles, worn paint | R B |
| L027 | the road out | a two-lane road running beside a railway line through mixed farm and forest, overcast | D B |
| L028 | the crossing | a level crossing on a rural road, spruce close on both sides, no vehicle | D B |
| L029 | the long run | the same track from the front of a moving train, curving through forest, motion soft at the edges | D B |
| L030 | the light going | the line at the end of the afternoon, the sun already behind the hills, blue-grey air | D A |

### ACT_2 — SEVEN · L031–L055 · *"At ten minutes to eleven…"*

| id | beat | prompt | flags |
|---|---|---|---|
| L031 | Nantes, arriving | a very small rural rail siding beside a two-lane road at last light, one crossing, low buildings, forest behind | R D A |
| L032 | the main track | a single main track running away downhill, ballast shoulder, no siding, no platform | D A |
| L033 | stopped | a locomotive consist standing still on the main track at night, marker lights on, exhaust drifting | R A |
| L034 | the grade, drawn from the ground | the same track seen along its length so that the descent is unmistakable, the horizon low | D A |
| L035 | the town, below | the lit town seen from the track above it, the rails running toward it out of frame | D A |
| L036 | the wheel, hero one | a hand-brake wheel on a tank car end platform, three-quarter, wet with dew, floodlight from behind | R D A |
| L037 | the wheel, hero two | the same wheel from directly above, the chain and rod visible below it | R A |
| L038 | the wheel, hero three | a hand-brake wheel in the extreme foreground, the line of cars falling away behind it out of focus | R D A |
| L039 | a hand on the wheel | two hands gripping a hand-brake wheel and turning it, forearms lit, no face in frame | **P** R A |
| L040 | the chain | close on a brake chain drawing tight over a sheave, links rust-brown | R A |
| L041 | the walk | a figure walking away along the ballast beside a line of tank cars, small in frame, lit from behind | **P** R D A |
| L042 | underfoot | ballast stone and sleeper ends lit by a hand torch, wet, shot from waist height looking down | **P** R A |
| L043 | the brake stand | the brake stand in a locomotive cab: two handles, gauges above, no person | R B |
| L044 | the gauge, established | a round brass-rimmed air pressure gauge on a locomotive control stand, needle mid-scale, glass slightly hazed | R B |
| L045 | the rule book | a plain ring-bound operating manual lying open on a desk, pages blank, the light from one lamp | R B |
| L046 | the instruction card | a plain card on a laminate surface, ruled but blank, a pencil beside it | R B |
| L047 | slack | close on couplers between two cars with the slack run out, gap visible, chains hanging | A |
| L048 | the test | a wide of the standing train from the side, still, at night, absolutely nothing moving | R D A |
| L049 | headlights arrive | car headlights sweeping across a gravel yard road at night, dust and moisture in the beam | A |
| L050 | the taxi waiting | an ordinary sedan standing with its engine running on a gravel siding road at night, interior light off | A |
| L051 | the hotel corridor | a narrow small-town hotel corridor at night, patterned carpet, doors, one wall light | **P** R D B |
| L052 | the hotel window | a small hotel room window at night with the curtain half drawn, a street light outside, the room dark | R D B |
| L053 | the yard, emptied | the yard with the train standing in it and no vehicle and no person anywhere, floodlight and shadow | R D A |
| L054 | idling | a locomotive nose at night, exhaust rising steadily from the stack, marker lights on | R A |
| L055 | rail and light | the rail head catching a single floodlight, running out of frame downhill, everything else black | D A |

### ACT_3 — THE THING THEY SWITCHED OFF · L056–L085

| id | beat | prompt | flags |
|---|---|---|---|
| L056 | smoke | thick dark smoke pouring from the exhaust stack of a locomotive at night, lit from below by yard light | R A |
| L057 | droplets | close on oily droplets beading on a painted locomotive hood, floodlight behind them | R A |
| L058 | the phone call | a domestic kitchen at night, a landline handset lifted from its cradle on the wall, no person's face | **P** R D B |
| L059 | the truck arrives | a rural volunteer fire truck on a gravel road at night, headlights and one beacon, seen from behind | R A |
| L060 | the hose | a charged hose line running away across ballast, a figure at the far end in silhouette | **P** R A |
| L061 | the shut-off | macro of a red emergency fuel shut-off switch on the flank of a locomotive, painted metal around it | R A |
| L062 | the breaker panel | an electrical breaker panel inside a locomotive cab, rows of small levers, worn labels unreadable | R B |
| L063 | the hand on the breakers | a gloved hand moving a row of small breaker levers downward, close, no face | **P** R B |
| L064 | fire dying | steam and smoke rising where a fire has just been put out, one work light through it, no flame left | R A |
| L065 | the crews leave | tail lights of two vehicles receding down a gravel road at night, dust in the beam | R A |
| L066 | the foreman's truck | a railway maintenance pickup with a beacon on the roof, parked, empty, at night | R A |
| L067 | the yard after | the same yard, entirely still, no vehicle, one floodlight, the train standing | R D A |
| L068 | the gauge, hero one | the air pressure gauge, close, needle high, glass reflecting one point of light | R A |
| L069 | the gauge, hero two | the same gauge, needle noticeably lower, the reflection unchanged | R A |
| L070 | the gauge, hero three | the same gauge, needle low, the frame slightly darker | R A |
| L071 | the brake pipe | close on the brake pipe hose slung between two cars, wet, at night | A |
| L072 | the clock | a plain analogue wall clock in an unlit railway building, hands near one, no numerals legible | R B |
| L073 | the rails, downhill | two rails running away downhill at night, converging, lit only near the camera | D A |
| L074 | the first movement | extreme close on a freight car wheel on rail, the tread just beginning to turn, motion blur only at the rim | R A |
| L075 | gathering | the side of a moving train at night, blurred, one light streaking across the flank | R A |
| L076 | through the forest | a rail line running through dense night forest, the trees smeared by speed | D A |
| L077 | the crossing at speed | a rural level crossing at night from the side, the crossing empty, lights not yet flashing | A |
| L078 | the curve | a railway curve seen from outside it at night, the outer rail higher than the inner, ballast bright | R D A |
| L079 | superelevation | close along the rail head through a curve, showing the cant, wet steel | A |
| L080 | the edge of town | the first houses beside the line, dark, seen from track level | R D A |
| L081 | light on rooftops | orange light thrown across the roofs of a small town at night from a source out of frame, no flame visible | R D A |
| L082 | smoke past a lamp | dense smoke crossing the beam of a street light, the lamp head sharp, the rest lost | R A |
| L083 | reflection | orange light reflected in a puddle on a residential street, the street otherwise empty and dark | R D A |
| L084 | two streets out | a quiet residential street at night, wet asphalt, parked cars, an orange glow in the sky beyond the roofline | R D A |
| L085 | first light | a lake at dawn under low grey cloud, a thin column of smoke on the far shore, no detail | D B |

### ACT_4 — EIGHTEEN · L086–L105

| id | beat | prompt | flags |
|---|---|---|---|
| L086 | the site, wide | a wide flat view of a cleared industrial ground with rail track running through it, machinery at rest, overcast, no people | B |
| L087 | the shell | a section of black tank car steel with a large torn opening in the side, seen close, edges bright where they tore | B |
| L088 | the head | the flat end of a tank car, punctured, the metal folded inward | B |
| L089 | the fittings | valve fittings sheared off the top of a tank car, lying on ballast | B |
| L090 | investigators, distant | two figures in high-visibility clothing standing far off across the site, unrecognisable, backs to camera | **P** B |
| L091 | the report | a plain thick bound document lying closed on a desk, cover blank, one lamp | R B |
| L092 | a document ground, cream | a plain sheet of cream paper filling the frame, faint texture, evenly lit, entirely blank | R B |
| L093 | a document ground, grey | a plain grey card filling the frame, faint horizontal grain, blank | R B |
| L094 | a document ground, manila | a manila folder cover filling the frame, blank, one crease | R B |
| L095 | the binder | a ring binder open on a desk, pages blank, a lamp at the edge of frame | R B |
| L096 | the box | a document storage box on a steel shelf, lid on, label area blank | R B |
| L097 | the shipping paper | a single sheet of paper on a clipboard on a desk, blank, a pen beside it | R B |
| L098 | the placard | a blank diamond-shaped metal placard bracket on the side of a tank car, the placard itself empty | R B |
| L099 | the sample | a small glass sample bottle of dark liquid standing on a laboratory bench, no label | R B |
| L100 | the test bench | laboratory glassware and a pressure test rig on a bench, no people, no readouts legible | R B |
| L101 | the audit folder | a slim folder on an office desk beside a telephone, blank cover | R B |
| L102 | the office corridor | an empty corridor in a plain government office building, doors, strip lighting | **P** D B |
| L103 | the desk | an office desk with blank forms squared up on it, a lamp, an empty chair pushed in | R B |
| L104 | the wall planner | a large blank wall planner grid in an office, no writing on it | R B |
| L105 | the patch returns | the polymeric repair from ACT_1, re-lit, colder, filling the frame | R B |

### ACT_5 — WHO ANSWERED · L106–L120

| id | beat | prompt | flags |
|---|---|---|---|
| L106 | the emptied office | a small railway company office with the desks cleared, chairs left out of place, blinds half down | R B |
| L107 | the ledger | a plain accounts ledger open on a desk, ruled columns, no figures written in | R B |
| L108 | the building | a plain mid-century public building seen from across a street in flat daylight, no signage legible | D B |
| L109 | the corridor | a wide institutional corridor with a wooden bench along one wall, empty | **P** D B |
| L110 | the bench | a worn wooden bench against a painted wall, empty, one coat left on it | **P** R B |
| L111 | the files | a stack of manila folders on a table, edges uneven, blank | R B |
| L112 | three cards | three blank white cards laid side by side on a dark table, evenly spaced, lit flat | R B |
| L113 | the public room | a plain municipal meeting room with rows of stacking chairs and a table at the front, empty | D B |
| L114 | the chair, hero one | a single plain wooden chair against a pale wall in an empty room, daylight from one side | R D B |
| L115 | the chair, hero two | the same chair from further back, the room's floor and skirting visible, nothing else in frame | R D B |
| L116 | the new street | a newly built small-town main street on an overcast day, young trees, wide pavement, few people, none identifiable | **P** D B |
| L117 | the panels | solar panels on the flat roof of a low modern building, grey sky, a town beyond | D B |
| L118 | the train, still | a long freight train passing through the middle of a small town in daylight, seen from a side street, a figure waiting at the barrier with their back to camera | **P** D B |
| L119 | the corridor of land | a surveyed strip of cleared ground running through farmland and spruce, stakes in the earth, no machinery | D B |
| L120 | the lake | the lake at dusk from the town shore, low hills opposite, still water, no people | D B |

## 5. THE PEOPLE PLATES — the twenty

`L003 L004 L015 L039 L041 L042 L051 L058 L060 L063 L090 L102 L109 L110 L116 L118` are the sixteen
that carry a figure directly. Four more are required and are to be produced as variants of
`L041`, `L060`, `L109` and `L116` with a different figure position — **never a different face,
because no face is ever resolved.** Every one is a back, a silhouette, a pair of hands, or a figure
too distant and too small for a face to exist.

## 6. What must never be generated for this film — the checklist

- A person who could be recognised. A face that resolves at all.
- Any of the 47. Any grieving person. Any casualty, injury, rescue or hospital image.
- Fire with a person in frame.
- A readable document, sign, placard, licence plate, headline or handwriting.
- A gavel, scales, jury box, judge's bench, handcuffs.
- American highway signage, US route shields, EU number plates, right-hand-drive traffic.
- Palm trees, ocean, beach, desert, a city skyline, an expressway interchange.
- A passenger train, a subway, a steam locomotive, a European multiple unit.
- Golden hour. This film has two light states and neither is pretty.

## 7. Paste files and the next step

Not generated in this pass. The next agent should run the established split —
`EP72_lacmegantic_CODEX_PASTE/batch_01.txt … batch_15.txt`, eight plates each — and verify before
commissioning anything:

```
py -3.11 scripts/check_image_order_neg.py --file episodes/_planning/EP72_lacmegantic_CODEX_BATCH_A.v001.md
py -3.11 scripts/check_prompt_diversity.py
```

**Before any of that**, the human review the contract requires: `footage_review_required` is `true`,
and a labelled contact sheet of the yard, the shop, the wreck site and the town-now registers must be
opened by a person before any plate enters a cut.
