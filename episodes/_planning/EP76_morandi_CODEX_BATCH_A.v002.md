# EP76 · MORANDI — IMAGE ORDER (BATCH A) v002 — REGENERATION ONLY

**Amends `EP76_morandi_CODEX_BATCH_A.v001.md` for seven plates. Everything else in v001 stands
unedited** — the bars in §1, the light states in §2, the global prompts in §3 and the other 113
plates are unchanged and are **not** to be regenerated.

---

## 1. WHAT WAS MEASURED, AND WHERE THE REPORT AND THE FILES DISAGREED

The delivery arrived with a report: 120 generated, 115 passing QC and upscaled, five withheld and
**not** staged. Every part of that was checked against the disk before anything was acted on.

**What is true.** 120 plates exist, **every one exactly 3840×2160**, ids matching the order, none
extra. The upscaling is sound and the register is right: the six contact sheets read as Genoa —
grey, ochre, port cranes, rail yard, a concrete river bed — with no holiday Italy, no American
signage, no legible glyph and no resolved likeness anywhere in 120 frames.

**What is not.** Two things:

1. **All 120 were staged in `remotion/public/morandi/img`, including the five said to be withheld.**
   Had a render started, the five would have been cut in. They are now dealt with below.
2. **Four of the five rejections do not survive a look at the file.** Read at 760 px and then at
   full resolution:

| id | the report said | the file shows | verdict |
|---|---|---|---|
| `V070` | a landscape instead of an inspection form | a blank ruled sheet on a desk — what V070 asks for | **ACCEPT** |
| `V073` | a landscape instead of graph paper | blank graph paper, two ruled axes, nothing plotted | **ACCEPT** |
| `V085` | readable digits and lettering on the fax | two full-res crops of the body and the tray: blank moulded plastic, blank thermal paper, no keypad, no display, no glyph | **ACCEPT** |
| `V086` | a landscape instead of a printed form | a blank ruled form with a paperclip | **ACCEPT** |
| `V024` | bridge type and period wrong | a white **steel truss**, not a concrete cable-stayed viaduct | **REJECT — the report was right** |

**And one rejection of my own did not survive either.** V106 — the severed deck, the last image of
ACT_4 — was rejected from a 400 px contact-sheet tile as "an intact viaduct". At full resolution the
deck is plainly cut: a span ends in mid-air, a wide gap of grey sky, the span resumes, the valley and
the port far below, no debris and no vehicle. **It is exactly the brief.** The lesson is the cheap
one and it cost nothing this time: a thumbnail is not evidence.

**Three rejections stand, all confirmed on the full frame**, and all three have been **moved out of
render truth** to `remotion/public/morandi/_rejected_v001/` — retired, not deleted:

| id | why |
|---|---|
| **`V008`** | asked for a stay sawn through showing steel cables in grout; returned concrete with exposed aggregate and no cable anywhere. It is the OP's hero object and the film's central idea |
| **`V020`** | mid-1960s construction with both workmen in **modern orange hi-vis and hard hats** — a period error inside `era_setting`, in a plate whose only job is to be 1965 |
| **`V024`** | a white steel truss where a concrete cable-stayed viaduct was ordered |

**Four more are a defect in the order, not in the generation.** V078, V104, V112 and V114 carry the
`P` people flag while their prompts ask for no person, and two say *empty* outright. The generator
was right and the order was wrong — and it made the people count **20 against a declared
`people_plates_min` of 24**. The prompts below put a figure in each.

**Three plates are off-brief but ship as they are**, recorded so their absence here is not read as an
oversight: V025 (no traffic in a "period traffic" plate), V051 (three towers, one scaffolded, does
not read), V063 (no step visible in the dropped slab). All three work as texture and none carries a
beat.

**Verdicts are recorded per plate, bound to the bytes**, in
`runs/qc/morandi_plate_verdicts.v001.json` — 117 accept, 3 reject, `check_plate_verdicts.py --slug
morandi` **PASS**.

---

## 2. THE SEVEN

Same `[STYLE]` and `[NEG]` as v001 §3, restated below so this file stands alone. Columns as v001.

**`[STYLE]`** — prepend to every plate:

> cinematic still, photographic, documentary, Genoa and the Polcevera valley in Liguria, north-west Italy — a working Mediterranean port city packed into a narrow steep-sided valley, tall narrow apartment blocks in ochre pink and grey render with dark green louvred shutters and roof terraces stacked up both hillsides, corrugated warehouses and a railway goods yard on the valley floor, a canalised river bed of concrete and gravel with a thin stream, container cranes and ferries in the distance, motorway viaducts and tunnel portals running over and through inhabited streets, umbrella pines on the slopes, flat overcast Ligurian daylight with sea haze and no sun in the sky, muted natural colour, low contrast but never crushed: shadows keep their detail and the frame reads clearly on a phone screen, restrained documentary framing, people small in frame and never posed, worn unglamorous ordinary surfaces — weathered reinforced concrete, rust staining, galvanised handrail, corrugated steel, painted render, terrazzo floor, laminate desk, manila card, ring binder board — nothing staged for advertising, no tourism, no scenery, Italian signage may appear but is always out of focus or too small or turned away and never legible, ultra-detailed, photoreal, 4K, long edge 3840 or greater, 16:9, fine film grain, no readable text, no legible lettering, no numerals, no watermark, no logo

**`[NEG]`** — append to every plate, unchanged from v001 and carrying all five families
`scripts/check_image_order_neg.py` requires:

> text, lettering, readable text, legible text, numerals, numbers, digits, house numbers, street numbers, handwriting, cursive, signature, legible signature, seals, seal, emblems, emblem, logos, logo, badge, insignia, unit marking, wordmarks, name plates, licence plate, registration plate, identifiable person, recognisable person, recognizable person, likeness of a real individual, portrait of a named person, celebrity, public figure, deepfake, collapsing bridge, bridge collapsing, falling deck, falling car, falling vehicle, vehicle plunging, car at a broken edge, crashed car, crushed vehicle, wreckage with a vehicle in it, debris field, dust cloud of collapse, body, corpse, human remains, body bag, injured person, blood, stretcher, paramedic, ambulance interior, hospital, funeral, grave, mourner, crying, grieving family, rescue, search and rescue, firefighter carrying person, memorial portrait, photo memorial, candle vigil, lightning strike, thunderstorm, storm clouds dramatic, wall of rain, tornado, earthquake damage, war ruins, movie explosion, action movie, fireball vfx, video game, crash test, vineyard, cypress avenue, tuscan hill town, rolling hills with cypress, amalfi coast, cliff village, gondola, venetian canal, colosseum, roman ruins, leaning tower, piazza postcard, palm tree, beach, surf, sunbathing, cruise ship, tropical, desert, snow, megacity skyline, skyscrapers, expressway interchange, american highway sign, US route shield, US number plate, mainland american main street, uk street, london street, right-hand-drive traffic, asian street, gavel, scales of justice, lady justice, jury box, judge's bench, courtroom interior, handcuffs closeup, firearm, prison bars, money rain, falling banknotes, stock ticker, candlestick chart, handshake, golden hour, sunset glow, blue hour, warm hero light, postcard scenery, glossy advertising lighting, flat CGI, 3D render, cartoon, illustration, oversaturated, HDR halo, watermark

### THE REGENERATION BATCH — V008, V020, V024, V078, V104, V112, V114

| id | beat | prompt | flags |
|---|---|---|---|
| V008 | a stay in section | a large rectangular prestressed concrete member sawn cleanly through and photographed square on to the cut face, filling the frame; set into the pale grey concrete is a dense cluster of dozens of parallel steel cables in grey grout, each cable a tight helix of bright steel wires about a centimetre across, arranged in neat rows; the concrete shell around them is smooth and unbroken; one hard work light from above; this is steel cable embedded in concrete, not gravel and not exposed aggregate | R U |
| V020 | threading the sheath | a hollow precast concrete segment being lowered on a crane sling over a bundle of steel strands on a bridge construction site in the mid 1960s, two workmen guiding it from several metres away in plain dark cotton work clothes and flat caps, sleeves rolled; strictly no high-visibility clothing, no reflective banding, no modern hard hats, nothing fluorescent anywhere in frame | **P** R D C |
| V024 | the opening, 1967 | a newly completed concrete cable-stayed motorway viaduct photographed from the valley floor in 1967: one tall reinforced concrete A-frame tower with exactly four straight diagonal CONCRETE stays running from its head down to a slender horizontal concrete deck, clean pale unweathered concrete throughout, small period saloon cars on the deck at a distance; no steel truss, no lattice, no arch, no suspension cables, no white painted steelwork, no modern vehicles | R D C |
| V078 | the toll plaza | an Italian motorway toll plaza on a flat overcast day, canopies and lane islands, a short queue of cars waiting, and two attendants in plain dark uniform walking between the lanes seen from behind at a distance; no legible signage anywhere | **P** D C |
| V104 | the viaduct, ordinary | an elevated motorway with ordinary traffic on it seen from a residential street below on a grey morning; in the near foreground a woman on a fourth-floor balcony hanging washing on a line, seen from behind and slightly below, the viaduct crossing beyond her | **P** D C |
| V112 | the bench | a worn wooden bench against a painted wall in an institutional corridor with a terrazzo floor; one person sits at the far end of it waiting, seen from the side, too far away and too dark for any detail of the face; a folded coat on the bench beside them | **P** R I |
| V114 | the room after | a plain public room with rows of stacking chairs after a hearing has finished, most seats empty, three people still seated near the back seen from behind, loose papers left on one seat, one chair pushed out of line | **P** R D I |

---

## 3. AFTER THE SEVEN RETURN

1. Upscale to exactly **3840×2160** by the same route as the 117.
2. Overwrite the three quarantined ids in `remotion/public/morandi/img` and add the four reordered
   ones. **The quarantined originals stay in `_rejected_v001/`** — retired, never deleted.
3. Rebuild the contact sheets and read the seven **at full resolution**, not on a tile.
4. Re-run `check_plate_verdicts.py --slug morandi`, then write all 120 basenames into
   `episode_spec.mandatory_stills`, because EP54's fourteen purpose-made stills were silently
   dropped by a surplus-trimming rule and then retired as unreferenced.

## 4. THE PEOPLE COUNT, CORRECTED

With V020, V078, V104, V112 and V114 carrying figures, the plates that actually contain a person are:

`V006 V016 V020 V021 V030 V045 V048 V060 V061 V076 V078 V079 V080 V094 V095 V098 V099 V100 V104
V109 V111 V112 V114 V119` — **24**, which meets `people_plates_min` exactly.

Ten stay in the carve-out with no face resolved at all: `V006 V021 V045 V048 V060 V061 V094 V098
V099 V100`.
