# EP76 · MORANDI — PACKAGING & THUMBNAIL PROMPTS v001

**Contract** `episodes/PD-2026-076-morandi/episode_spec.v001.json` ·
**Facts** `EP76_morandi_FACTS_LEDGER.v001.md` ·
**Image bars** `EP76_morandi_CODEX_BATCH_A.v001.md` §1–§3, which bind these plates identically.

> **The four ship-blocking classes bind the title, the thumbnail text and the description exactly as
> they bind the narration** (`config/ship_policy.v001.json`, ONE_PASS v3 §3 and row 17). A title is a
> claim. Every candidate below was run through `check_packaging_claims.py` against this episode's own
> record before it was written down.

---

## 1. THE BARS, RESTATED FOR PACKAGING

1. **No named person on the thumbnail, in any form** — not Castellucci, not Ferrazza, not Morandi,
   not a face that reads as any of them. ⛔-01.
2. **No collapse, no falling deck, no vehicle at a broken edge, no debris.** The event is the gap,
   the scale, and a road that stops. ⛔-06.
3. **No casualty, no rescue, no memorial with a face.** ⛔-05.
4. **No number that is not a ledger row.** ⛔-11.
5. **No implication of foresight or intent**, because the court struck that circumstance out for
   every defendant and acquitted all of them of the intentional offences. ⛔-02. A thumbnail reading
   THEY KNEW would be a `factual_support` failure on its own, without the film around it.
6. **Every glyph on the thumbnail is composited**, never generated. ⛔-12.

---

## 2. TITLE — three candidates, all measured

House rule (v3 row 13): **59–100 characters, third person, no question form**, no citation or
doctrine, real searchable name present, at least two A/B variants.

| id | title | chars | `check_packaging_claims` |
|---|---|---|---|
| **A** | **Structural Spending On The Genoa Motorway Viaduct Fell To 23,000 Euros A Year** | **77** | **PASS** — claims 3, unsupported 0 |
| B | A Motorway Company Wrote The Rule That Said Close The Road. Genoa, 14 August 2018 | 81 | **PASS** — claims 6, unsupported 0 |
| C | The Safety Assessment Was Owed In 2013, Reported As Done In 2017, And Never Made | 80 | **PASS** — unsupported 0 |

**Recommended: A.** It is the film's hardest measured fact (MO-42), it is a number a viewer can hold,
it names Genoa for search, and it accuses nobody. B is the strongest sentence but leans closest to
implying a decision not to close the road, which is the one implication ⛔-02 polices. C is the
truest description of the film and the weakest hook, because "safety assessment" is an abstraction.

**A/B pair for the channel's variant test: A and B.**

**What none of them do**: name a person, use a question, state a cause, or say "they knew".

---

## 3. THUMBNAIL TEXT — UPPERCASE, one idea, ≤ 4 words

| id | text | pairs with | note |
|---|---|---|---|
| **T-a** | **€23,000 A YEAR** | title A | the film's largest number card, and the one that needs no context |
| T-b | THE MANUAL SAID 70 | title B | requires the film; strong for returning viewers, weak cold |
| T-c | NEVER WRITTEN | title C | abstract; only works over the empty index tab |
| T-d | 98% BEFORE 1999 | title A | the same fact as T-a, harder to read at 320 px |

**Selected: T-a, `€23,000 A YEAR`.** Gold `#E5B53A`, set in the lower third, readable at 320 px.

---

## 4. HOUSE LOOK FOR THE PLATES

Same `[STYLE]` and `[NEG]` as `EP76_morandi_CODEX_BATCH_A.v001.md` §3, unchanged, with two
additions for thumbnails only:

- **The subject fills the frame.** These are not scene plates; the object is large, centred or set
  hard to one side with clear space for the type.
- **Contrast is pushed one stop past the film's**, because a thumbnail competes at 320 px. It is
  still flat Ligurian daylight — **no golden hour, no orange rim light, no lens flare**.

---

## 4.5 GLOBAL PROMPTS — identical to the image order, restated so this file stands alone

**`[STYLE]`** — prepend to every thumbnail plate:

> cinematic still, photographic, documentary, Genoa and the Polcevera valley in Liguria, north-west Italy — a working Mediterranean port city packed into a narrow steep-sided valley, tall narrow apartment blocks in ochre pink and grey render with dark green louvred shutters and roof terraces stacked up both hillsides, corrugated warehouses and a railway goods yard on the valley floor, a canalised river bed of concrete and gravel with a thin stream, container cranes and ferries in the distance, motorway viaducts and tunnel portals running over and through inhabited streets, umbrella pines on the slopes, flat overcast Ligurian daylight with sea haze and no sun in the sky, muted natural colour, low contrast but never crushed: shadows keep their detail and the frame reads clearly on a phone screen, restrained documentary framing, people small in frame and never posed, worn unglamorous ordinary surfaces — weathered reinforced concrete, rust staining, galvanised handrail, corrugated steel, painted render, terrazzo floor, laminate desk, manila card, ring binder board — nothing staged for advertising, no tourism, no scenery, Italian signage may appear but is always out of focus or too small or turned away and never legible, ultra-detailed, photoreal, 4K, long edge 3840 or greater, 16:9, fine film grain, no readable text, no legible lettering, no numerals, no watermark, no logo

**`[NEG]`** — append to every thumbnail plate. Identical to the image order's canonical negative,
and it carries all five families `scripts/check_image_order_neg.py` requires:

> text, lettering, readable text, legible text, numerals, numbers, digits, house numbers, street numbers, handwriting, cursive, signature, legible signature, seals, seal, emblems, emblem, logos, logo, badge, insignia, unit marking, wordmarks, name plates, licence plate, registration plate, identifiable person, recognisable person, recognizable person, likeness of a real individual, portrait of a named person, celebrity, public figure, deepfake, collapsing bridge, bridge collapsing, falling deck, falling car, falling vehicle, vehicle plunging, car at a broken edge, crashed car, crushed vehicle, wreckage with a vehicle in it, debris field, dust cloud of collapse, body, corpse, human remains, body bag, injured person, blood, stretcher, paramedic, ambulance interior, hospital, funeral, grave, mourner, crying, grieving family, rescue, search and rescue, firefighter carrying person, memorial portrait, photo memorial, candle vigil, lightning strike, thunderstorm, storm clouds dramatic, wall of rain, tornado, earthquake damage, war ruins, movie explosion, action movie, fireball vfx, video game, crash test, vineyard, cypress avenue, tuscan hill town, rolling hills with cypress, amalfi coast, cliff village, gondola, venetian canal, colosseum, roman ruins, leaning tower, piazza postcard, palm tree, beach, surf, sunbathing, cruise ship, tropical, desert, snow, megacity skyline, skyscrapers, expressway interchange, american highway sign, US route shield, US number plate, mainland american main street, uk street, london street, right-hand-drive traffic, asian street, gavel, scales of justice, lady justice, jury box, judge's bench, courtroom interior, handcuffs closeup, firearm, prison bars, money rain, falling banknotes, stock ticker, candlestick chart, handshake, golden hour, sunset glow, blue hour, warm hero light, postcard scenery, glossy advertising lighting, flat CGI, 3D render, cartoon, illustration, oversaturated, HDR halo, watermark

**Faces are allowed and wanted**, and identifiability is what is barred — the same carve-out as the
image order §3. None of the six concepts below resolves a face at all.

---

## 5. SIX CONCEPTS — `T01`–`T06`, 1280×720, three to be built

Every one is `[STYLE]` + the subject + `[NEG]`. **Text is composited in Remotion afterwards; nothing
here asks the generator for a glyph.**

| id | concept | prompt | carries |
|---|---|---|---|
| **T01** | **the road that stops** | a two-lane elevated motorway carriageway photographed from the running surface, ending abruptly at a line of new steel crash barrier with nothing beyond it but haze and a city far below, flat grey Ligurian daylight, worn asphalt and painted lane markings leading the eye to the edge, no vehicle and no person in frame | T-a, T-c. **The strongest and the safest** |
| T02 | the score box | extreme close on one empty ruled box on a printed inspection form, the paper slightly creased, the surrounding rows blank, one hard lamp raking across it from the left leaving deep shadow in the right third | T-b. Clear space right |
| T03 | the sheath, cut | a large rectangular prestressed concrete member cut through and photographed square on, filling the frame, its pale outer shell intact and its core a dense dark cluster of steel strands set in grout, one work light from above | T-a. The film's idea in one object |
| T04 | four ties against cloud | the four diagonal concrete stays of a bridge tower converging at its head, seen from directly beneath against a flat white overcast sky, the deck cutting hard across the lower third | T-a, T-d. Clean type space top left |
| T05 | the empty tab | a card index drawer pulled open, one blank tab standing proud of the others, nothing filed behind it, shallow depth of field, plain office lamp | T-c |
| T06 | underneath, with people | a bus stop on a street directly beneath a motorway viaduct, three people waiting, the concrete soffit filling the top half of the frame and dwarfing them, flat daylight | T-a. The "this is you" read |

**Build T01, T03 and T04** — three variants, which is `thumbnail_candidates_min`. T01 is the
selection unless the contact sheet says otherwise.

---

## 6. DESCRIPTION — the rule, not the text

The description is written at package time, from the script, and is checked with
`check_packaging_claims.py --slug morandi --description-file <path>` before it goes anywhere.

Three things it must contain and one it must not:

1. The AI-disclosure line the channel uses for generated imagery (invariant 11).
2. **The legal status, in full**: 32 convicted at first instance on 16 July 2026, 25 acquitted or
   time-barred, the written reasons not yet filed, an appeal announced, **the judgment not final**.
3. The two disagreeing findings on the first cause, with their dates and authors.
4. **It must not** name a convicted person without that status in the same sentence, and must not
   assert a cause.

---

## 7. WHAT IS NOT DECIDED HERE

- **No plate has been generated.** T01–T06 are an order, not an asset.
- The selection between A and B is a **title/thumbnail approval**, which is an owner gate
  (`.claude/rules/16`), not an agent decision.
