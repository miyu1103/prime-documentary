# EP77 · KEYBRIDGE — IMAGE ORDER (BATCH A) v001

**121 reconstruction plates, `H001`–`H121`.** Every prompt is the subject in the table plus
`[STYLE]` plus `[NEG]`, in that order.

Nothing here may contradict `episodes/_planning/EP77_keybridge_FACTS_LEDGER.v001.md`. The ⛔
rules there bind these images exactly as they bind the narration. The machine contract is
`episodes/PD-2026-077-keybridge/episode_spec.v001.json`; the script is
`episodes/_planning/EP77_keybridge_script.en.v001.md`.

## 0. Size, and the one constraint that has bitten every episode

- **Long edge ≥ 3840 px, 16:9.** `remotion/public/keybridge/img` is render truth and the
  pre-render gate refuses anything under it.
- **Codex's built-in generation is fixed at 1672×941** and cannot be prompted out of it. If a
  native-4K path is not available, the sanctioned fallback is Real-ESRGAN x4plus to 6688×3764
  then a LANCZOS reduction to exactly 3840×2160. **A plain 2× enlargement does not clear the
  floor.** EP71 shipped 117 of 118 plates at 1672×941 into a pool the builder used anyway.
- **Aspect ratio 16:9 exactly — width ÷ height = 1.778.** Not 2.35:1, not 2.25:1, not 2.13:1.
  EP75 had six plates come back in cinemascope and they were remade.
- **One prompt, one image.** No variants, no `b` versions.
- Deliver to `E:\pd-media\05_visuals\keybridge\img\`. **Nothing existing is overwritten.**

## 1. What this film is, in one paragraph, so the plates fit it

Baltimore, the small hours of **26 March 2024**. A container ship leaves the Port of Baltimore,
loses power twice on the way out, and strikes a pier of the Francis Scott Key Bridge. Eight
people are on the bridge deck patching potholes; six die. Twenty months later the Safety Board
finds the cause is **a loose signal wire that a band of labelling stopped seating in a terminal
block**. In 2026 a grand jury charges the ship's managers, and the chief engineer admits in a
deferred prosecution agreement that an unsafe fuel pump was in use on three ships.

**The film is about the gap between a drawing and a machine.** Not a disaster film.

## 2. The bars — absolute

| never | why |
|---|---|
| **The moment of impact, the collapse, or the wreck in the water** | `forbidden_subjects`. This film never shows the accident |
| **The six who died. Any body, any injury, any rescue, any funeral** | `forbidden_subjects`, invariant 11 |
| **Any identifiable real person** — the captain, the pilots, the chief engineer, the defendants, officials | Invariant 11. Human figures YES, likeness NO. Backs, hands, silhouettes, figures at distance |
| **Readable documents of any kind** — indictments, reports, logs, emails, charts with legible text | Invariant 11. Paper may appear; **letters may not resolve** |
| **Anything that reads as a verdict** — a gavel coming down, handcuffs, a cell | This is a live criminal case and nobody has been tried |
| **Children** | `forbidden_subjects` |
| **Ship or company names, real logos, real number plates** | Rights and likeness |

**Human figures are required.** `people_plates_min` is **20**; the people lane below is **24**
so the floor survives three rejections.

## 3. `[STYLE]` — paste after every subject

```
, cinematic documentary reconstruction, one practical light source visible in the frame
throwing a directional beam, atmospheric haze and river mist catching the light, deep shadow
on one side only, restrained colour with a single dominant accent, high contrast, ultra high
resolution, hyper-detailed, razor-sharp focus, photorealistic, volumetric light, shallow depth
of field, 16:9
```

**This is NOT the thumbnail style.** Thumbnail plates are loud on purpose
(`EP77-82_THUMB_CODEX.v002.md`). Film plates sit under narration for thirty minutes and must
not shout. **But they must not be flat black either** — the 2026-08-23 thumbnail set measured
brightness 19.1 against the winners' 58.2 because a prompt said "deep black palette". **Do not
write that phrase here.** Every plate has a light in it.

## 4. `[NEG]` — paste at the end of every subject

**`[NEG]`** — the canonical negative for EP77. It carries every token family
`scripts/check_image_order_neg.py` requires, because a plate whose own prompt forgets a bar is
protected only by this line:

> Avoid: text, lettering, legible text, readable text, captions, subtitles, handwriting, cursive, signature, numerals, numbers, digits, house numbers, readable documents, signage lettering, watermark, seal, seals, emblem, emblems, logo, logos, badge, insignia, human face, facial features, portrait, identifiable person, recognisable person, looking at the camera, bodies, corpse, injuries, blood, rescue operations, the moment of collision, the bridge collapsing, wreckage in water, children, gavel, handcuffs, prison bars, police uniform, patrol car, golden hour, drone shot, cartoon, oversaturated, flat evenly-dark image, muted grey wash, desaturated, low-resolution, distorted anatomy, extra fingers.

---

## 5. HOOK — `H001`–`H006`

| id | subject |
|---|---|
| H001 | A wall-mounted operations clock in a dim traffic control room, hands near half past one, a single desk lamp raking across it |
| H002 | A bank of highway CCTV monitors glowing in a dark room, empty night roads on every screen, no text overlays |
| H003 | An empty six-lane bridge deck at night seen down its centre line, sodium lamps receding, wet asphalt, no vehicles |
| H004 | A gloved hand resting on a radio handset on a control desk, the transmit light glowing red, everything else dark |
| H005 | A single orange traffic cone standing in a pool of work light on an empty bridge deck, river mist drifting through the beam |
| H006 | A wide low view of a steel truss span at night from the water, one pier lit from below, black river, no vessels |

## 6. ACT_1 — the night shift and the transit · `H007`–`H036`

| id | subject |
|---|---|
| H007 | Two anonymous road workers in high-visibility jackets seen from behind, setting cones on a bridge deck at night, faces not visible **[PEOPLE]** |
| H008 | A works truck with a rotating amber beacon parked on a closed lane, the beacon flaring, the deck beyond it empty |
| H009 | Close on a hot-tar patching kit and hand tools laid on the deck under a portable lamp |
| H010 | A thermos and two paper cups on a concrete parapet, steam rising, harbour lights far behind |
| H011 | A gloved hand pressing fresh asphalt into a pothole with a hand tamper, lit by a low work lamp **[PEOPLE]** |
| H012 | A container terminal at night from the water, gantry cranes lit, stacks of containers in rows, no legible markings |
| H013 | The bow of a large container ship seen from the quay at night, floodlit, towering, no name visible |
| H014 | Mooring lines being let go from a bollard on a wet quay, an anonymous dockworker's hands only **[PEOPLE]** |
| H015 | A ship's engine room walkway between towering machinery, work lights in a receding line, nobody present |
| H016 | An engine control room console with rows of indicator lamps and switches, warm glow, no legible labels |
| H017 | A marine diesel generator unit in a machinery space, painted steel, a single inspection lamp on it |
| H018 | A high-voltage switchboard cabinet with its door closed, a green lamp lit on the panel, dark room |
| H019 | Two anonymous engineers in overalls seen from behind at a machinery panel, helmets on, faces away **[PEOPLE]** |
| H020 | A pilot ladder against a black hull at night, lit by a deck light, water below |
| H021 | A ship's bridge interior at night, instrument glow only, an anonymous figure in silhouette at the window **[PEOPLE]** |
| H022 | A radar display glowing green in a darkened wheelhouse, no legible text, reflections on glass |
| H023 | A hand on a ship's engine telegraph lever in low light **[PEOPLE]** |
| H024 | A tugboat under way at night seen from the ship's rail, its deck lights burning, wake churning |
| H025 | A tug's tow line slack in black water as it releases, floodlit from above |
| H026 | The wake of a large vessel in a narrow channel at night, channel buoys blinking green and red |
| H027 | A loaded container stack seen from the ship's bridge wing at night, containers receding to the bow |
| H028 | A voyage data recorder capsule mounted on a ship's deck, orange, weathered, floodlit at night |
| H029 | An electrical breaker panel with two large breakers, one handle in the open position, hard side light |
| H030 | A machinery space plunged into darkness with only a single emergency light burning at the far end |
| H031 | An emergency generator unit starting in a dark compartment, one red lamp lit on its panel |
| H032 | Anonymous hands in work gloves closing a heavy electrical breaker by hand, sparks of light on the metal **[PEOPLE]** |
| H033 | Ship's lighting coming back on along a long internal corridor, receding fluorescents, empty |
| H034 | A silent propeller shaft tunnel, the shaft stationary, a single lamp above it |
| H035 | A rudder post and steering gear machinery in a dark compartment, hydraulic pipework, one lamp |
| H036 | An empty bridge deck at night viewed from far off across the water, the span lit, nothing else |

## 7. ACT_2 — why this should not have happened · `H037`–`H056`

| id | subject |
|---|---|
| H037 | A naval architect's line drawing of a ship's electrical distribution pinned on a bulkhead, lines and boxes only, no legible lettering |
| H038 | Two identical step-down transformers side by side in a machinery space, painted grey, one lamp between them |
| H039 | A closed-bus tie breaker on a switchboard, chunky handle, hard light |
| H040 | A row of four marine diesel generators in a long machinery space, receding, work lights above |
| H041 | A classification society plate riveted to a bulkhead, blank, no legible text, raking light |
| H042 | A ship's main engine seen from below, enormous, cylinder heads receding, a single lamp |
| H043 | Cooling water pipework with a pressure gauge, needle at rest, no legible numerals |
| H044 | A steering gear pump unit, three units in a row, only one lit |
| H045 | A tug boat far away across black water at night, its lights small, the distance obvious |
| H046 | A harbour pilot's hand on a VHF radio, transmit light on, dark wheelhouse **[PEOPLE]** |
| H047 | A coastguard watch room at night, screens glowing, an anonymous operator seen from behind **[PEOPLE]** |
| H048 | A traffic control room with a wall of monitors, an operator's silhouette against them **[PEOPLE]** |
| H049 | A patrol car parked across a closed highway ramp at night, roof bar flashing, no markings legible |
| H050 | A boom gate lowering across an empty approach road at night, warning lamp flashing |
| H051 | An empty toll plaza at night, lanes lit, no vehicles at all |
| H052 | A ship's rudder seen underwater from behind, still, lit by diffuse light |
| H053 | A propeller blade at rest under water, barnacle-flecked, light shafts from above |
| H054 | A stopwatch face in a gloved hand, hands sweeping, no legible numerals **[PEOPLE]** |
| H055 | A ship's telegraph set to a bell position, brass and glass, warm lamp light |
| H056 | The black surface of a river at night with a single reflected light stretching across it |

## 8. ACT_3 — the anatomy · `H057`–`H091`

| id | subject |
|---|---|
| H057 | A quayside at dusk with a ship alongside, gangway down, an anonymous crew member in a hard hat walking up it seen from behind, cargo work under floodlights **[PEOPLE]** |
| H058 | An exhaust scrubber unit on a ship's funnel casing, pipework and platforms, one lamp |
| H059 | An anonymous crewman's gloved hand on a large exhaust damper lever **[PEOPLE]** |
| H060 | A closed damper plate inside an exhaust duct, soot-stained metal, torch beam across it |
| H061 | A generator control panel with an alarm lamp lit amber, dark machinery behind |
| H062 | A fuel supply line with a pressure gauge and a hand valve, hard raking light |
| H063 | A pump unit on a steel deck plate, painted, unremarkable, one work lamp on it |
| H064 | An engineer's clipboard and pen on a machinery ledge, the page blank, no writing **[PEOPLE-adjacent, no face]** |
| H065 | A switchboard with two breaker positions labelled by shape only, one open one closed, no text |
| H066 | A transformer nameplate, blank, raking light, no legible characters |
| H067 | Extreme macro of a terminal block with a spring-clamp gate, a stripped copper wire beside it |
| H068 | Extreme macro of a plastic labelling band wrapped around an insulated wire, the band blank |
| H069 | Extreme macro of the same wire held a hair short of the clamp gate, the gap unmistakable, hard light |
| H070 | A terminal rail with dozens of identical blocks in a row, receding, one lit brighter |
| H071 | A technician's hands with a small screwdriver at a terminal rail, no face **[PEOPLE]** |
| H072 | An electrical test meter's probe tips touching a terminal, the display not legible |
| H073 | A ship's machinery space photographed with investigators' portable lights, tripods, cables, nobody in frame |
| H074 | Two anonymous investigators in coveralls and hard hats seen from behind in a machinery space **[PEOPLE]** |
| H075 | An evidence table with anonymous machine components laid out on brown paper under a lamp |
| H076 | A conference room at night with a long table and empty chairs, one overhead light on |
| H077 | A public hearing room with a raised dais and empty seats, house lights low, no signage |
| H078 | A microphone on a hearing-room table, water glass beside it, no papers legible |
| H079 | An anonymous figure at a lectern seen from behind against a lit screen, the screen showing an abstract diagram **[PEOPLE]** |
| H080 | A screen showing a simplified circuit diagram of boxes and lines, no text, viewed at an angle |
| H081 | A bridge pier rising out of black water, concrete, massive, floodlit from a boat |
| H082 | A sheet-pile and concrete dolphin structure in the water beside a bridge pier, weathered, lit |
| H083 | An engineer's scale model of a bridge pier on a desk under a lamp, no markings |
| H084 | A stack of engineering binders on a shelf, spines blank, dusty, one lamp |
| H085 | A highway bridge seen from beneath, girders receding, a service walkway, harsh work lighting |
| H086 | A container ship passing under a bridge span at dusk, seen from far off, everything calm |
| H087 | A row of identical container ships at anchor waiting outside a port at dawn |
| H088 | An empty state transport authority office at night, desks, screens off, one lamp burning |
| H089 | A wall-mounted map of a harbour with shipping channels marked as coloured lines only, no text |
| H090 | A calculator and a mechanical pencil on a drawing of structural sections, no legible figures |
| H091 | A single filing drawer pulled open in a dark records room, folders unlabelled, torch beam |

## 9. ACT_4 — the outcome · `H092`–`H111`

| id | subject |
|---|---|
| H092 | The exterior of a federal courthouse at dusk, columns lit, empty steps, no signage legible |
| H093 | An empty courtroom gallery, wooden benches, one bank of lights on |
| H094 | A lawyer's trolley of document boxes in a marble corridor, boxes unlabelled **[PEOPLE-adjacent]** |
| H095 | Two anonymous figures in suits walking away down a courthouse corridor, seen from behind **[PEOPLE]** |
| H096 | A stack of bound legal volumes on a table under a green desk lamp, spines blank |
| H097 | A ship's registry office counter, brass fittings, nobody present |
| H098 | A container terminal working again at dawn, cranes moving, an anonymous figure in a high-visibility vest small against a gantry leg, the channel open **[PEOPLE]** |
| H099 | A salvage crane barge on a river at first light, cables and hooks, no wreck visible |
| H100 | A newly poured concrete pier cap with reinforcement bar stubs, construction lighting |
| H101 | Surveyors' equipment on a tripod beside a highway at dawn, an anonymous surveyor stooping to the eyepiece seen from behind **[PEOPLE]** |
| H102 | An anonymous inspector in a hard hat and harness on a bridge walkway, seen from behind **[PEOPLE]** |
| H103 | A bridge inspection gantry hanging beneath a deck, empty, seen from the water |
| H104 | A long line of bridges receding into haze along a coastline at dawn, aerial |
| H105 | A highway sign gantry silhouetted at sunrise, blank panels, no lettering |
| H106 | An engineer's desk with a physical model of a pier protection dolphin, a lamp, no papers legible |
| H107 | A committee room with a horseshoe table and empty chairs, flags in the corner, no text |
| H108 | Anonymous hands passing a bound report across a desk, cover blank **[PEOPLE]** |
| H109 | A harbour at dusk with a bridge under construction, cranes on the span, warm sky |
| H110 | A wide aerial of a working port at night, lights, ships at berth, a bridge in the distance |
| H111 | An empty road-crew break room at night, lockers, a kettle, one strip light |

## 10. ENDING — `H112`–`H121`

| id | subject |
|---|---|
| H112 | Extreme macro of one wire seated fully and correctly in a terminal clamp, clean metal, hard light |
| H113 | A hand in a work glove closing a switchboard cabinet door, deliberate, no face **[PEOPLE]** |
| H114 | A bridge pier at dawn with new protective dolphins in the water around it |
| H115 | A car's headlights crossing an empty bridge deck at dawn, seen from the road surface |
| H116 | A family car crossing a long bridge over water in early morning light, seen from far away |
| H117 | An anonymous driver's hands on a steering wheel, bridge cables passing overhead **[PEOPLE]** |
| H118 | Anonymous gloved hands stacking cones onto a truck bed at the end of a shift, dawn light, no face **[PEOPLE]** |
| H119 | An empty high-visibility jacket hanging on a hook in a works depot, morning light through a window |
| H120 | A wide dawn view of a working harbour with a bridge in the middle distance, calm water |
| H121 | A single work light being switched off on an empty bridge deck as the sky lightens |

---

## 11. The people lane — 24 plates, floor is 20

`H007 H011 H014 H019 H021 H023 H032 H046 H047 H048 H054 H057 H059 H071 H074 H079 H094 H095
H098 H101 H102 H108 H113 H117 H118` — **25 marked**, against a spec floor of **20**.
(A first draft of this file claimed 24 and only marked 20. The self-check caught it; at a
measured rejection rate of 22-34 % a floor with no margin is a rebuild.)

**Every one is a back, a hand, a silhouette or a distant figure. No face resolves anywhere.**

## 12. Checks before this order is called done

```
py -3.11 scripts/check_image_order_neg.py episodes/_planning/EP77_keybridge_CODEX_BATCH_A.v001.md
py -3.11 scripts/check_episode_inputs.py --slug keybridge
```

Then, after delivery:

1. **Every plate at 3840×2160, ratio exactly 1.778.**
2. **Contact sheets read tile by tile, six frames minimum per sheet.** The measured acceptance
   rate on staged material is 22–34 %; assume rejections and plan the regeneration batch.
3. **No face resolves.** EP65 shipped an archive clip whose file name said "woman" and whose
   frames showed an identifiable person; three checks passed it and a human reading the
   shipped frames caught it.
4. **No letters resolve anywhere**, especially on H037, H064, H066, H080, H089, H090, H096,
   H105 and H108, which all contain paper or panels by design.
