# EP68 · THE FORD PINTO / *GRIMSHAW v. FORD* — IMAGE ORDER **BATCH B** (Codex) v001

**Episode `PD-2026-068-pinto` · slug `pinto` · 2026-08-11**

> **What this adds.** Batch A ordered **104** plates and nothing else. This adds the two tiers it had no room for: **13 headroom plates** and **6 thumbnail plates**. Batch A is not edited and stays on disk (invariant 6); everything it says about policy, era, the barred likenesses and the `[NEG]` still binds and is restated below.

| tier | ids | count | in `episode_spec.mandatory_stills`? |
|---|---|---:|---|
| **1 · declared** | `R001`–`R104` | **104** | **yes** — batch A, unchanged |
| **2 · headroom** | `R105`–`R117` | **13** | **no** — cover against rejections and against the script growing |
| **3 · thumbnail** | `T001`–`T006` | **6** | **no** — a thumbnail never becomes a cut |

**Declaring the headroom would fail the build.** `check_spec_satisfied.py` fails any `mandatory_stills` id that appears in no cut, and the solver places only the declared number of still cuts. That correction had to be made late on EP65. **`episode_spec.v001.json` is not edited by this order.** Thumbnails are never declared and never become cuts.

**Paste files:** `EP68_pinto_CODEX_PASTE_A/headroom_01.txt` … `thumbs_01.txt`, and the merged single file `EP68_pinto_CODEX_PASTE_ALL.txt` which now carries **all 123** prompts in one file. Both are emitted from `scripts/build_ep68_ep69_headroom_order.py` together with this document, so the prompt bodies cannot drift apart; the equality is *checked by the generator*, not asserted here.

---

## 0. How many, derived rather than chosen

EP66 batch C is the only measured plate-rejection rate this channel has: **191 ordered, 11 REJECT (5.8%) and 10 further FLAG — 11.0% combined.** Reproduced mechanically from `runs/qc/openfields_plate_verdicts.v001.md` by `check_plate_verdicts.ingest_md`, which returns `{'accept': 170, 'reject': 11, 'unresolved': 10}`.

```
declared mandatory_stills          104
distinct_video_assets              265   target_cut_sec 3.7
build_case_film_generic.solve_totals still-cut ceiling, flat across the whole declared
  script_words x pace band         124   = floor(265 x 0.32 / 0.68)

  104 / (1 - 0.058)  =  111     hard rejects only
  104 / (1 - 0.110)  =  117     rejects + flags   <- used

HEADROOM  117 - 104 = 13
THUMBS    6   (episode_spec.thumbnail_candidates_min = 3)
ORDERED   104 + 13 + 6 = 123
```

**Note, measured and not tidied away.** The solver's still-cut ceiling for this episode is **124**, which is 20 above the declared 104. The headroom above is sized to protect the DECLARED count against rejection, not to fill that ceiling. `docs/PD_CANON.md` rule 25 applies: the band is a prediction and the delivered VO is the measurement — if `mandatory_stills` is ever re-derived upward from the real narration master, or if `distinct_video_assets` changes, **re-run `scripts/build_ep68_ep69_headroom_order.py --derive` and re-order**. Do not carry 104 forward on faith.

**Six thumbnails, not three.** `episode_spec.thumbnail_candidates_min` is 3 and the packaging document specifies three variants. Each variant is ordered as a **framing pair**, so a variant that comes back badly framed still leaves three candidates and no thumbnail has to be re-ordered on the day.

§7 of `EP68_pinto_CODEX_BATCH_A.v001.md` sketched an optional batch B at `R105`–`R140` to be commissioned **after** the first assembly. That plan is superseded: a thin pool discovered after assembly costs a rebuild, and the ids used here stay inside the range it reserved, so nothing collides.

---

## 1. `[NEG]` — this episode's own, unchanged, on every plate in every tier

**This is the canonical `[NEG]`. It is read out of `EP68_pinto_CODEX_BATCH_A.v001.md` at generation time and never retyped, and the generator refuses to write if the copy in the paste files is not byte-identical to it:**

> text, lettering, numerals, digits, handwriting, cursive writing, legible signature, readable words on a page, seals, emblems, logos, insignia, badge, name plates, wordmarks, manufacturer script, grille emblem, licence plate, registration plate, recognisable person, identifiable person, likeness of a real individual, portrait of a named person, celebrity, public figure, deepfake, fire, flame, flames, smoke, burning, embers, soot, charred surfaces, a burning vehicle, a person on fire, burn injury, scarring, skin graft, bandages, hospital, ambulance, paramedic, blood, a crashed car, collision, wreckage, crumpled bodywork, shattered windscreen, police officer, uniform, patrol car, flashing lights, handcuffs, firearm, courtroom interior, gavel, judge's bench, jury box, witness stand, prison bars, scales of justice, hourglass, a handshake, children, modern smartphones, flat-screen monitors, LED headlights, modern cars, contemporary clothing, plastic modern fittings, night vision green, thermal false colour, crosshairs, CCTV monitor grid, drone shot, golden hour, sunset glow, postcard scenery, Christmas, tropical, glossy advertising lighting, flat CGI, cartoon, illustration, oversaturated, HDR halo

**It is NOT deviated for the thumbnail lane.** Only the style block changes there.

**Note what it deliberately does NOT contain: `human face`, `facial features`, `eyes`.** Those three suppress the people lane, and the people lane is required. What is suppressed instead is *identifiability*: `recognisable person`, `identifiable person`, `likeness of a real individual`, `portrait of a named person`, `celebrity`, `public figure`, `deepfake`. The generator checks for all seven and refuses if any of the three banned tokens returns; `scripts/check_image_order_neg.py` checks this document independently.

---

## 2. `[STYLE]` — unchanged, on every headroom plate

> cinematic still, photographic, muted natural colour, the United States between 1968 and 1981, mixed tungsten and daylight, low contrast but never crushed: shadows keep their detail and the frame reads clearly on a phone screen, shallow depth of field, restrained documentary framing, worn unglamorous period surfaces — painted steel, brushed aluminium, laminate, bakelite, manila card, newsprint, enamel — nothing staged for advertising, ultra-detailed, photoreal, 4K, 16:9, fine film grain, no text, no lettering, no numerals, no watermark, no logo, no signage

## 3. `[TSTYLE]` — the thumbnail lane only, and why it exists

> editorial photographic still made to be a video thumbnail, ONE HARD DIRECTIONAL KEY LIGHT from the side, HIGH CONTRAST AND BRIGHT OVERALL EXPOSURE, the subject clearly brighter than everything behind it and cleanly separated from it, shadow only where it defines an edge and never filling the frame, THE ENTIRE UPPER 40 PERCENT OF THE FRAME IS ONE UNBROKEN UNIFORM FIELD - plain wall, plain sky or plain out-of-focus darkness, with no object, no edge, no horizon and no detail crossing it anywhere - and the whole subject sits inside the lower 60 percent with the bottom third the brightest part of the picture, the United States between 1968 and 1981, ultra-detailed, photoreal, 4K, 16:9, no text, no lettering, no numerals, no watermark, no logo, no signage

**EP65's lesson, stated so nobody undoes this.** The canonical `[STYLE]` above mandates *low contrast*, which is correct for a film frame and is exactly why EP65's four thumbnail candidates came back as dull grey paper and had to be re-ordered. A thumbnail is not a film frame. `build_ep62_65_thumbnails.py` lays a **black scrim at alpha 120 over the top 66%** before the headline goes on, and `thumb_subject_luma` wants a subject box of mean luma **>= 60** with a bright connected component **>= 150 px**. So: one hard directional key, high contrast, bright overall exposure, subject brighter than background, the whole subject inside the lower 60% with the bottom third the brightest part of the picture, and **the entire upper 40% of the frame an unbroken field** so a headline can be burned into it. Not a mood; a measurement.

---

## 4. Headroom — 13 plates, `R105`–`R117`, **not declared in the spec**

Every one still carries a script line and a section reference — **a plate with no beat is not commissioned**, headroom or otherwise. Every prompt is **self-contained**: none of them says "the same X" about a plate that lives in another file, because a generator has no memory between prompts.

| id | script line it carries | where it lands |
|---|---|---|
| `R105` | The design was not on trial. It could not be. | ACT_1 / ACT_4 — H1 register, second camera position |
| `R106` | The remedy was a longer fuel filler pipe with an improved seal, and a polyethylene shield installed on the front of the fuel tank. | ACT_3 — the tank shell alone, and the remedy |
| `R107` | What was left was a fight about speed. | ACT_2 — the H5 freeway register at a second hour |
| `R108` | The wire report named them: | ACT_3 / ACT_5 — the wire copy, never legible |
| `R109` | On the tenth of August, nineteen seventy-eight, in Elkhart County, Indiana | ACT_5 — Indiana, the road register (IN-04) |
| `R110` | and the Indiana register | ACT_5 — the Indiana register (section direction block) |
| `R111` | and judgment was entered at Winamac, in the Pulaski County Circuit Court | ACT_5 — Winamac, from outside (IN2-02 / SW2-14) |
| `R112` | On the thirteenth of March nineteen eighty, the jury found Ford not guilty. | ACT_5 — the town, the morning after |
| `R113` | The venue then changed | ACT_5 — the change of venue (IN2-01 / IN2-02) |
| `R114` | The hearing never happened. | ACT_3 / ACT_4 — the regulator, in public session |
| `R115` | Then it lists what it did, and the list is worth reading. | ACT_3 — the regulator, from inside |
| `R116` | It counts deaths, and it prices them. | ACT_4 — the money, kept abstract (⛔-15: no document facsimile) |
| `R117` | Almost nobody will notice what the table is about. | ENDING — one of the film's designed silences |

### `R105.png` — ACT_1 / ACT_4 — H1 register, second camera position

*Script line:* The design was not on trial. It could not be.

```
A workshop lift raised to chest height with an early-1970s American subcompact hatchback standing on it, photographed from the side at floor level from twelve feet away so the whole underbody runs across the middle of the frame as one long dark band, one work light on a stand throwing hard raking light along it from the left, bare stained concrete in the foreground and a dim shop wall behind. Nobody is in the frame. No vehicle anywhere in this frame carries a mark of any kind: no badge, no emblem, no oval on the grille, no wordmark, no nameplate, no model lettering and no plate of any kind on any part of it, front or rear. The car is undamaged and intact [STYLE] Avoid: [NEG], licence plate, registration plate, number plate, badge on the grille, oval emblem, manufacturer wordmark, chrome nameplate, shop signage, price sticker, crumpled bodywork, collision damage, fire, flame, smoke, scorch marks, person in frame
```

### `R106.png` — ACT_3 — the tank shell alone, and the remedy

*Script line:* The remedy was a longer fuel filler pipe with an improved seal, and a polyethylene shield installed on the front of the fuel tank.

```
A plain pressed-steel fuel tank shell removed from a car and standing alone on a heavy workbench on its flat forward face, photographed straight on from bench height under one work lamp, the pressed seam running across it and nothing else on its surface, the metal dull grey and lightly scuffed, a dark shop falling away behind it. The shell is empty, clean, dry and undamaged, and there is no liquid, no vapour, no flame and no scorching anywhere in the picture. No badge, no stamped mark, no label and no writing on it [STYLE] Avoid: [NEG], fire, flame, smoke, fuel spill, liquid, vapour, scorch marks, rust holes, crumpled metal, stamped lettering, part number, manufacturer wordmark, label, sticker
```

### `R107.png` — ACT_2 — the H5 freeway register at a second hour

*Script line:* What was left was a fight about speed.

```
A wide three-lane American freeway photographed from the hard shoulder at dusk with a low wide lens, the pale concrete running away to a low ridge on the horizon and going cold blue-grey as the light leaves it, dry Southern Californian scrub along the shoulder, the lane markings just holding their brightness. There is no vehicle anywhere in the frame and nobody is on the road [STYLE] Avoid: [NEG], vehicles, cars, traffic, headlights, tail lights, street lighting, road signs, gantry, billboard, golden hour, sunset glow, orange sky
```

### `R108.png` — ACT_3 / ACT_5 — the wire copy, never legible

*Script line:* The wire report named them:

```
A 1970s wire-service teleprinter standing on a steel stand in the corner of a newspaper office, photographed three-quarter from the side at standing height, a continuous roll of pale paper feeding up out of the machine and falling in a loose fold to the floor, the printing on the paper reduced by distance and shallow focus to fine even grey banding with no character, word or line resolving anywhere on it. Flat overhead office light, nobody in the room [STYLE] Avoid: [NEG], legible typing, readable words on a page, letterforms, printed paragraph, headline, masthead, letterhead, manufacturer wordmark on the machine, nameplate, person in frame
```

### `R109.png` — ACT_5 — Indiana, the road register (IN-04)

*Script line:* On the tenth of August, nineteen seventy-eight, in Elkhart County, Indiana

```
A two-lane blacktop road running dead straight away from the camera between two walls of corn at full height in flat mid-August light, photographed from the middle of the road at standing height, the crown of the road slightly raised, telephone poles receding down the left verge, a wide pale sky above and no cloud shape in it. Northern Indiana farmland. There is no vehicle in the frame and nobody is on the road, and no sign, board or marker carries any writing [STYLE] Avoid: [NEG], vehicles, cars, traffic, road signs with words, billboards, mailboxes with names, farm signage, golden hour, sunset glow, person in frame
```

### `R110.png` — ACT_5 — the Indiana register (section direction block)

*Script line:* and the Indiana register

```
A tall corrugated-steel grain elevator standing over a set of rail sidings under flat overcast light in a small Midwestern farming town, photographed from across the tracks at standing height so the elevator fills the right of the frame and empty gravel and rail run away to the left, weeds between the sleepers, no lettering, no company name and no painted sign anywhere on the steel. Nobody is in the frame [STYLE] Avoid: [NEG], painted lettering on the silo, company name, grain co-op sign, billboard, modern trucks, modern cars, person in frame
```

### `R111.png` — ACT_5 — Winamac, from outside (IN2-02 / SW2-14)

*Script line:* and judgment was entered at Winamac, in the Pulaski County Circuit Court

```
A small Midwestern county courthouse square in flat grey light: a modest three-storey limestone courthouse standing across an empty street with a bare metal flagpole in front of it carrying no flag, a small open bandstand on the lawn, mature trees bare of leaves, photographed from the far pavement at standing height. There is no signage of any kind on the building or the lawn, no vehicle at the kerb and nobody in the frame [STYLE] Avoid: [NEG], courthouse signage, engraved lettering on the stone, plaques, notice boards, flags, vehicles at the kerb, modern cars, person in frame, courtroom interior
```

### `R112.png` — ACT_5 — the town, the morning after

*Script line:* On the thirteenth of March nineteen eighty, the jury found Ford not guilty.

```
A two-storey small-town American main street at midday, brick shopfronts down both sides with plain canvas awnings out over the pavement, photographed from the middle of the road at standing height so the street runs away into flat haze, the pavement empty, the light hard and colourless. Not one window, awning, board or fascia carries any lettering, name or number, and there is no vehicle and nobody in the frame [STYLE] Avoid: [NEG], shop signage, fascia lettering, window lettering, awning text, street signs, house numbers, billboards, parked cars, modern cars, person in frame
```

### `R113.png` — ACT_5 — the change of venue (IN2-01 / IN2-02)

*Script line:* The venue then changed

```
A gravel county road junction between two flat fields, photographed from the middle of one road at standing height so both roads run away to the horizon, a single plain white-painted wooden signpost standing at the corner with two blank arms on it that carry no lettering, no arrow and no number, dry grass in the verge, a wide pale overcast sky. No vehicle, no building and nobody in the frame [STYLE] Avoid: [NEG], lettering on the signpost, route numbers, arrows with names, road signs with words, mailboxes with names, vehicles, person in frame
```

### `R114.png` — ACT_3 / ACT_4 — the regulator, in public session

*Script line:* The hearing never happened.

```
A plain 1970s American federal hearing room, completely empty: a low carpeted dais across the far end with a bare wooden lectern standing on it that carries no seal, no crest and no lettering of any kind, six rows of grey stacking chairs facing it, a run of fluorescent troffers in a low acoustic-tile ceiling, institutional pale green walls. Photographed from the back of the room at standing height. Nobody is present [STYLE] Avoid: [NEG], seal on the lectern, crest, flag, insignia, nameplates, lettering on the wall, courtroom interior, gavel, judge's bench, jury box, witness stand, person in frame
```

### `R115.png` — ACT_3 — the regulator, from inside

*Script line:* Then it lists what it did, and the list is worth reading.

```
A long institutional corridor in a 1970s American federal building, photographed straight down its length from standing height: a painted green dado running the full length of both walls, a row of identical closed flush doors down the right side with blank plates where the numbers would be, a hard vinyl floor holding a long reflection, and one bright window at the far end burning out to white. Nobody is in the corridor [STYLE] Avoid: [NEG], door numbers, name plates with words, directory boards, exit signage, notices on the walls, person in frame
```

### `R116.png` — ACT_4 — the money, kept abstract (⛔-15: no document facsimile)

*Script line:* It counts deaths, and it prices them.

```
A period adding machine standing on a grey steel office desk under one lamp, photographed close from a low three-quarter angle, a narrow paper till roll feeding up out of the top of it and curling over the edge of the desk toward the floor in one long loose fall, the printing on the roll reduced by focus to a soft grey stipple with no figure, column or character resolving anywhere along it. The desk is otherwise bare [STYLE] Avoid: [NEG], legible numbers, digits on the roll, printed figures, columns of numerals, keys with numerals, brand name on the machine, nameplate, person in frame
```

### `R117.png` — ENDING — one of the film's designed silences

*Script line:* Almost nobody will notice what the table is about.

```
Rain running down the side window glass of a stationary car, photographed from inside the car at seat height with the glass filling the frame, the water breaking into long vertical runs and beads, the world beyond the glass dissolved into soft flat grey with no shape, edge or object resolving in it. The interior is dark vinyl and hard plastic of the early 1970s, the car is not moving and nobody is in it [STYLE] Avoid: [NEG], readable signage beyond the glass, buildings, other vehicles, headlights, wipers in motion, person in frame, reflection of a face
```

---

## 5. Thumbnails — 6 plates, `T001`–`T006`, **never declared, never a cut**

| id | packaging variant |
|---|---|
| `T001` | packaging variant 1 — WRONG MEMO / IT WAS ROLLOVER |
| `T002` | packaging variant 1 — second framing |
| `T003` | packaging variant 2 — 9 INCHES / CRUSH SPACE |
| `T004` | packaging variant 2 — second framing |
| `T005` | packaging variant 3 — 500 OR 27 / NHTSA, MAY 1978 |
| `T006` | packaging variant 3 — second framing |

### `T001.png` — packaging variant 1 — WRONG MEMO / IT WAS ROLLOVER

*Reference:* PACKAGING §2 variant 1

```
Eight sheets of typed paper fanned out across a grey steel office desk, photographed from a steep oblique angle from just above the near edge of the desk SO THE WHOLE FAN OF PAPER SITS IN THE LOWER 60 PERCENT OF THE FRAME, one hard directional work lamp raking across it from the left so the paper is markedly brighter than anything behind it and throws crisp shadows, a plain steel paper clip on the top sheet. The typing is visible only as an even grey ribbed texture at that angle and NOT ONE WORD, NUMBER, LINE OR LETTERFORM RESOLVES ANYWHERE. The bright bare desk top runs across the bottom third and is the brightest part of the picture. THE ENTIRE UPPER 40 PERCENT OF THE FRAME IS ONE UNBROKEN FIELD of plain out-of-focus dark office with no object, no edge and no detail crossing it anywhere [TSTYLE] Avoid: [NEG], legible typing, readable words on a page, letterforms, typed lines, printed paragraph, letterhead, margins with page numbers, stamp with words, signature, hand, person in frame, object in the top of the frame, low contrast, dull flat lighting, dark subject, detail crossing the top of the frame
```

### `T002.png` — packaging variant 1 — second framing

*Reference:* PACKAGING §2 variant 1

```
The same fan of eight typed sheets on the same bare grey steel desk, closer and from a lower angle almost level with the desk top: the near edges of the paper make one strong bright horizontal band across the lower third of the frame, one hard key light from the left rakes along them, and the plain steel paper clip catches a specular highlight. At this angle the typing is pure grey texture and NOT ONE CHARACTER IS READABLE. The picture is bright and high contrast throughout the lower 60 percent, and THE ENTIRE UPPER 40 PERCENT IS ONE UNBROKEN FIELD of plain out-of-focus darkness with nothing in it at all [TSTYLE] Avoid: [NEG], legible typing, readable words on a page, letterforms, typed lines, printed paragraph, letterhead, stamp with words, signature, hand, person in frame, object in the top of the frame, low contrast, dull flat lighting, dark subject, detail crossing the top of the frame
```

### `T003.png` — packaging variant 2 — 9 INCHES / CRUSH SPACE

*Reference:* PACKAGING §2 variant 2

```
The underbody of an early-1970s American subcompact hatchback raised high on a workshop lift, photographed from twelve feet away at standing height so THE WHOLE UNDERBODY RUNS AS ONE BRIGHT BAND ACROSS THE LOWER 60 PERCENT OF THE FRAME: the rear axle and the differential housing on the left, the flat forward face of the tank shell on the right, and a plain unmarked steel machinist's rule laid horizontally across the narrow gap between them, its graduations too fine and too oblique to read. One hard shop light from below and to the left makes the metal markedly brighter than anything behind it, and the bright swept concrete floor runs across the bottom third. THE ENTIRE UPPER 40 PERCENT IS ONE UNBROKEN FIELD of plain dark out-of-focus shop with nothing crossing it. The car is undamaged, carries no badge, no emblem, no wordmark, no nameplate and no plate of any kind, and there is no fire, no smoke, no scorching and no liquid anywhere in the picture [TSTYLE] Avoid: [NEG], licence plate, registration plate, number plate, badge on the grille, oval emblem, manufacturer wordmark, chrome nameplate, shop signage, readable markings on the rule, fire, flame, smoke, scorch marks, fuel spill, crumpled bodywork, hand, person in frame, object in the top of the frame, low contrast, dull flat lighting, dark subject, detail crossing the top of the frame
```

### `T004.png` — packaging variant 2 — second framing

*Reference:* PACKAGING §2 variant 2

```
The same raised underbody and the same plain unmarked steel machinist's rule laid across the gap between the differential housing and the flat face of the tank shell, now closer and tighter so the housing, the gap and the rule fill the lower half of the frame and read large, one hard shop light from below and to the left putting a bright specular edge along the rule and the machined faces. The bright concrete floor is just visible along the bottom edge and is the brightest thing in the picture. THE ENTIRE UPPER 40 PERCENT IS ONE UNBROKEN FIELD of plain dark out-of-focus shop. No badge, no emblem, no wordmark, no nameplate, no plate, no readable graduation on the rule, and no fire, smoke, scorching or liquid anywhere [TSTYLE] Avoid: [NEG], licence plate, registration plate, number plate, badge on the grille, oval emblem, manufacturer wordmark, chrome nameplate, readable markings on the rule, fire, flame, smoke, scorch marks, fuel spill, crumpled bodywork, hand, person in frame, object in the top of the frame, low contrast, dull flat lighting, dark subject, detail crossing the top of the frame
```

### `T005.png` — packaging variant 3 — 500 OR 27 / NHTSA, MAY 1978

*Reference:* PACKAGING §2 variant 3

```
A single unbadged early-1970s American subcompact hatchback standing stopped and alone in the middle lane of a wide dry three-lane freeway at midday, photographed from a fixed high vantage on a road overbridge looking down and along the carriageway, THE CAR AND THE ROAD FILLING THE LOWER 60 PERCENT OF THE FRAME with the car small and central in it. Hard overhead sun makes the pale concrete and the car roof markedly brighter than everything else, and the bright empty asphalt runs across the bottom third. Dry Southern Californian scrub along the shoulder, both other lanes completely empty, no other vehicle anywhere. Nobody is in or near the car, it is undamaged, and it carries no badge, no emblem, no wordmark, no nameplate and no plate of any kind. THE ENTIRE UPPER 40 PERCENT OF THE FRAME IS ONE UNBROKEN FIELD of flat white overexposed sky with no cloud, no horizon line, no gantry, no pole and no detail crossing it anywhere [TSTYLE] Avoid: [NEG], licence plate, registration plate, number plate, badge on the grille, oval emblem, manufacturer wordmark, chrome nameplate, other vehicles, traffic, road signs, gantry, overhead structure, billboards, crumpled bodywork, fire, flame, smoke, person in frame, object in the top of the frame, horizon crossing the top of the frame, low contrast, dull flat lighting, dark subject
```

### `T006.png` — packaging variant 3 — second framing

*Reference:* PACKAGING §2 variant 3

```
The same unbadged early-1970s American subcompact hatchback standing stopped and alone in the middle lane of the same wide dry three-lane freeway at midday, now seen from lower and closer on the same overbridge so the car reads larger from behind and the two empty lanes spread away on either side of it, all of it inside the lower 60 percent of the frame. Hard overhead sun, high contrast, the bright pale concrete across the bottom third the brightest part of the picture, dry scrub at the shoulder. No other vehicle anywhere, nobody in or near the car, no damage, and no badge, emblem, wordmark, nameplate or plate of any kind. THE ENTIRE UPPER 40 PERCENT IS ONE UNBROKEN FIELD of flat white overexposed sky with nothing crossing it [TSTYLE] Avoid: [NEG], licence plate, registration plate, number plate, badge on the grille, oval emblem, manufacturer wordmark, chrome nameplate, other vehicles, traffic, road signs, gantry, overhead structure, billboards, crumpled bodywork, fire, flame, smoke, person in frame, object in the top of the frame, horizon crossing the top of the frame, low contrast, dull flat lighting, dark subject
```

---

## 6. Delivery

- Names are exactly `R105.png` … `R117.png` and `T001.png` … `T006.png`. No `_v2`, no `_02`, no `_A`.
- Deliver to `H:\pd-media\assets\ai\pinto`, long edge >= 3840, PNG, 16:9.
- **Headroom plates are NOT added to `episode_spec.mandatory_stills`** and thumbnail plates are not added to anything. Neither file is edited by this order.
- After delivery: `py -3.11 scripts/check_plate_verdicts.py --slug pinto --scaffold --reviewer <name>`, open every plate, record a verdict for each, then `py -3.11 scripts/check_episode_inputs.py --slug pinto`. The plate gate blocks the build until every plate in the set carries a resolved verdict bound to the file on disk.

*Generated by `scripts/build_ep68_ep69_headroom_order.py`. The prompt bodies in this document and in the paste files come from one source and the generator checks they are byte-identical.*
