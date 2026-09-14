# EP69 · THE HYATT REGENCY WALKWAYS — IMAGE ORDER **BATCH B** (Codex) v001

**Episode `PD-2026-069-hyatt` · slug `hyatt` · 2026-08-11**

> **What this adds.** Batch A ordered **113** plates and nothing else. This adds the two tiers it had no room for: **14 headroom plates** and **6 thumbnail plates**. Batch A is not edited and stays on disk (invariant 6); everything it says about policy, era, the barred likenesses and the `[NEG]` still binds and is restated below.

| tier | ids | count | in `episode_spec.mandatory_stills`? |
|---|---|---:|---|
| **1 · declared** | `H001`–`H113` | **113** | **yes** — batch A, unchanged |
| **2 · headroom** | `H114`–`H127` | **14** | **no** — cover against rejections and against the script growing |
| **3 · thumbnail** | `T001`–`T006` | **6** | **no** — a thumbnail never becomes a cut |

**Declaring the headroom would fail the build.** `check_spec_satisfied.py` fails any `mandatory_stills` id that appears in no cut, and the solver places only the declared number of still cuts. That correction had to be made late on EP65. **`episode_spec.v001.json` is not edited by this order.** Thumbnails are never declared and never become cuts.

**Paste files:** `EP69_hyatt_CODEX_PASTE_A/headroom_01.txt` … `thumbs_01.txt`, and the merged single file `EP69_hyatt_CODEX_PASTE_ALL.txt` which now carries **all 133** prompts in one file. Both are emitted from `scripts/build_ep68_ep69_headroom_order.py` together with this document, so the prompt bodies cannot drift apart; the equality is *checked by the generator*, not asserted here.

---

## 0. How many, derived rather than chosen

EP66 batch C is the only measured plate-rejection rate this channel has: **191 ordered, 11 REJECT (5.8%) and 10 further FLAG — 11.0% combined.** Reproduced mechanically from `runs/qc/openfields_plate_verdicts.v001.md` by `check_plate_verdicts.ingest_md`, which returns `{'accept': 170, 'reject': 11, 'unresolved': 10}`.

```
declared mandatory_stills          113
distinct_video_assets              236   target_cut_sec 3.6
build_case_film_generic.solve_totals still-cut ceiling, flat across the whole declared
  script_words x pace band         117   = floor(250 x 0.32 / 0.68)

  113 / (1 - 0.058)  =  120     hard rejects only
  113 / (1 - 0.110)  =  127     rejects + flags   <- used

HEADROOM  127 - 113 = 14
THUMBS    6   (episode_spec.thumbnail_candidates_min = 3)
ORDERED   113 + 14 + 6 = 133
```

**Note, measured and not tidied away.** The solver's still-cut ceiling for this episode is **117**, which is 4 above the declared 113. The headroom above is sized to protect the DECLARED count against rejection, not to fill that ceiling. `docs/PD_CANON.md` rule 25 applies: the band is a prediction and the delivered VO is the measurement — if `mandatory_stills` is ever re-derived upward from the real narration master, or if `distinct_video_assets` changes, **re-run `scripts/build_ep68_ep69_headroom_order.py --derive` and re-order**. Do not carry 113 forward on faith.

**Six thumbnails, not three.** `episode_spec.thumbnail_candidates_min` is 3 and the packaging document specifies three variants. Each variant is ordered as a **framing pair**, so a variant that comes back badly framed still leaves three candidates and no thumbnail has to be re-ordered on the day.

§8 of `EP69_hyatt_CODEX_BATCH_A.v001.md` said the three thumbnail plates would be commissioned later 'with the same `[STYLE]`/`[NEG]`'. The `[NEG]` is indeed unchanged. The `[STYLE]` is NOT: the canonical one mandates low contrast, which is precisely why EP65's four candidates came back dull and had to be re-ordered.

---

## 1. `[NEG]` — this episode's own, unchanged, on every plate in every tier

**This is the canonical `[NEG]`. It is read out of `EP69_hyatt_CODEX_BATCH_A.v001.md` at generation time and never retyped, and the generator refuses to write if the copy in the paste files is not byte-identical to it:**

> text, lettering, numerals, digits, handwriting, cursive writing, legible signature, dimension callouts, drawing title block, seals, emblems, logos, insignia, badge, name plates, readable words on a sign, recognisable person, identifiable person, likeness of a real individual, portrait of a named person, celebrity, public figure, deepfake, collapsed building, collapsing structure, rubble, debris, wreckage, ruined interior, rescue worker, ambulance, stretcher, injured person, blood, body, casualty, funeral, firefighter, hospital, crowded hotel lobby, packed function room, crowd of people indoors, courtroom interior, gavel, judge's bench, scales of justice, hourglass, a handshake, police officer, uniform, handcuffs, prison bars, mobile phone, smartphone, laptop, flat-panel monitor, LED work lamp, cordless power tool, hi-vis safety vest, modern safety helmet, CAD screen, car built after 1990, night vision green, thermal false colour, crosshairs, CCTV monitor grid, drone shot, aerial view, golden hour, sunset glow, postcard scenery, Christmas, tropical, glossy advertising lighting, flat CGI, cartoon, illustration, oversaturated, HDR halo

**It is NOT deviated for the thumbnail lane.** Only the style block changes there.

**Note what it deliberately does NOT contain: `human face`, `facial features`, `eyes`.** Those three suppress the people lane, and the people lane is required. What is suppressed instead is *identifiability*: `recognisable person`, `identifiable person`, `likeness of a real individual`, `portrait of a named person`, `celebrity`, `public figure`, `deepfake`. The generator checks for all seven and refuses if any of the three banned tokens returns; `scripts/check_image_order_neg.py` checks this document independently.

---

## 2. `[STYLE]` — unchanged, on every headroom plate

> cinematic still, photographic, muted natural colour, American Midwest between 1978 and 1988, tungsten interiors and flat midday daylight, low contrast but never crushed: shadows keep their detail and the frame reads clearly on a phone screen, shallow depth of field, restrained documentary framing, worn unglamorous surfaces, painted steel, vellum, brass, cut stone, plaster and travertine, nothing staged for advertising, ultra-detailed, photoreal, 4K, 16:9, fine film grain, no text, no lettering, no numerals, no watermark, no logo, no signage

## 3. `[TSTYLE]` — the thumbnail lane only, and why it exists

> editorial photographic still made to be a video thumbnail, ONE HARD DIRECTIONAL KEY LIGHT from the side, HIGH CONTRAST AND BRIGHT OVERALL EXPOSURE, the subject clearly brighter than everything behind it and cleanly separated from it, shadow only where it defines an edge and never filling the frame, THE ENTIRE UPPER 40 PERCENT OF THE FRAME IS ONE UNBROKEN UNIFORM FIELD - plain wall, plain sky or plain out-of-focus darkness, with no object, no edge, no horizon and no detail crossing it anywhere - and the whole subject sits inside the lower 60 percent with the bottom third the brightest part of the picture, the American Midwest between 1978 and 1988, ultra-detailed, photoreal, 4K, 16:9, no text, no lettering, no numerals, no watermark, no logo, no signage

**EP65's lesson, stated so nobody undoes this.** The canonical `[STYLE]` above mandates *low contrast*, which is correct for a film frame and is exactly why EP65's four thumbnail candidates came back as dull grey paper and had to be re-ordered. A thumbnail is not a film frame. `build_ep62_65_thumbnails.py` lays a **black scrim at alpha 120 over the top 66%** before the headline goes on, and `thumb_subject_luma` wants a subject box of mean luma **>= 60** with a bright connected component **>= 150 px**. So: one hard directional key, high contrast, bright overall exposure, subject brighter than background, the whole subject inside the lower 60% with the bottom third the brightest part of the picture, and **the entire upper 40% of the frame an unbroken field** so a headline can be burned into it. Not a mood; a measurement.

---

## 4. Headroom — 14 plates, `H114`–`H127`, **not declared in the spec**

Every one still carries a script line and a section reference — **a plate with no beat is not commissioned**, headroom or otherwise. Every prompt is **self-contained**: none of them says "the same X" about a plate that lives in another file, because a generator has no memory between prompts.

| id | script line it carries | where it lands |
|---|---|---|
| `H114` | One long steel rod becomes two shorter ones, four inches apart. | ACT_2 — the change, shown as tool and stock, never as an act |
| `H115` | Two walkways will hang from that detail | ACT_2 — the two holes, four inches apart (FN-02) |
| `H116` | Between fifteen hundred and two thousand area residents chose to escape the heat at the hotel's tea dance | ACT_3 — the building, an hour before, with nobody in it (EV-04, ⛔-12) |
| `H117` | a weekly event with big band music and a dance contest | ACT_3 — the evening, from the side nobody watched (EV-04) |
| `H118` | Crowd in atrium area is estimated at fifteen hundred to two thousand | ACT_3 — the atrium at rest, an hour before (EV-05, ⛔-12) |
| `H119` | Permission to weigh the spans and to cut specimens out of them came later, by court order | ACT_4 — weighing, by court order (ID-06) |
| `H120` | their involvement was limited by court order to visual and photographic observations | ACT_4 — what the investigators were allowed to do first (ID-06) |
| `H121` | Efforts to obtain copies of the structural design calculations, the report says, were unsuccessful. | ACT_4 — the calculations that do not exist in the record |
| `H122` | and to cut specimens out of them came later, by court order | ACT_4 — the metallurgy (ID-06) |
| `H123` | the Commission conducted twenty-seven days of hearing | ACT_5 — outside the room, twenty-seven times (DC-01) |
| `H124` | no one had yet taken responsibility for the collapse | ACT_5 — the file, closed (DC-22) |
| `H125` | It was filed on the fifteenth of November, 1985. | ACT_5 — time, with the numbers taken off (DC-03) |
| `H126` | Its decision runs four hundred and forty-two pages. | ACT_5 — the record, boxed (DC-02) |
| `H127` | One hundred and fourteen people went to a tea dance and did not come home. | ENDING — the room, afterwards (⛔-12, ⛔-14) |

### `H114.png` — ACT_2 — the change, shown as tool and stock, never as an act

*Script line:* One long steel rod becomes two shorter ones, four inches apart.

```
One long length of threaded steel rod about an inch and a quarter across lying diagonally across a dark oiled workbench, photographed from directly above with a hard raking light running along the thread so every turn stands out, a plain hand hacksaw lying beside it with its blade clear of the rod and not touching it. Nothing else is on the bench and nobody is in the frame [STYLE] Avoid: [NEG], cut rod, sawn end, swarf on the blade, sparks, brand name on the saw, stamped markings on the rod, person in frame, hands
```

### `H115.png` — ACT_2 — the two holes, four inches apart (FN-02)

*Script line:* Two walkways will hang from that detail

```
The upper face of a short length of hollow rectangular steel box section lying on a fabricator's bench, photographed from directly above and close so the section runs across the frame, TWO ROUND HOLES DRILLED THROUGH IT A SHORT DISTANCE APART near the middle of its length, bright curls of fresh swarf lying around each hole and a light film of cutting oil on the steel. One hard side light rakes across the surface. No writing, no marking-out lines with figures, nobody in the frame [STYLE] Avoid: [NEG], dimension callouts, figures written on the steel, marking-out numerals, stamped part numbers, drawing title block, person in frame, hands
```

### `H116.png` — ACT_3 — the building, an hour before, with nobody in it (EV-04, ⛔-12)

*Script line:* Between fifteen hundred and two thousand area residents chose to escape the heat at the hotel's tea dance

```
A hotel lift landing of about 1980, empty: two sets of brushed bronze lift doors closed in a travertine-clad wall, a low bench opposite them, a shallow planter of foliage, warm downlighters in a plain plaster soffit, tan stone floor holding a soft reflection. Photographed straight on from standing height. There is no signage, no floor indicator lettering and no numeral anywhere, and nobody is present [STYLE] Avoid: [NEG], floor numbers, lift indicator numerals, directional signage, hotel branding, logos, person in frame, crowd
```

### `H117.png` — ACT_3 — the evening, from the side nobody watched (EV-04)

*Script line:* a weekly event with big band music and a dance contest

```
A hotel kitchen pass of about 1980, empty and clean: a long stainless steel counter running across the frame with a row of identical plain white plates stacked on it under a strip of warm heat lamps, quarry-tiled floor, stainless shelving behind, everything wiped down and still. Photographed from the service side at standing height. Nobody is present and no label, ticket or board carries any writing [STYLE] Avoid: [NEG], order tickets with writing, menu boards, labels, brand names on equipment, person in frame, crowd, food service in progress
```

### `H118.png` — ACT_3 — the atrium at rest, an hour before (EV-05, ⛔-12)

*Script line:* Crowd in atrium area is estimated at fifteen hundred to two thousand

```
A low travertine fountain basin in a large open hotel interior, photographed from standing height at close range so the basin edge runs across the lower half of the frame, the water flat and still with the jet off, warm afternoon daylight coming down from a glazed roof far above and lying in one broad soft band across the surface, planting boxes soft behind. Nobody is in the frame and nothing in it identifies any particular building [STYLE] Avoid: [NEG], hotel branding, logos, signage, plaques, coins in the water, person in frame, crowd, recognisable real building
```

### `H119.png` — ACT_4 — weighing, by court order (ID-06)

*Script line:* Permission to weigh the spans and to cut specimens out of them came later, by court order

```
A heavy steel load cell and a large shackle hanging on a chain in a high-roofed testing hall, photographed close from below against the dark roof structure so the cell fills the middle of the frame, its cable running away out of the top of the shot, one hard light from the side picking out the machined steel and the pin. Nobody is in the frame and the cell carries no dial face, no scale and no lettering [STYLE] Avoid: [NEG], digits on a display, dial with numerals, calibration plate with figures, brand name, person in frame, rubble, debris
```

### `H120.png` — ACT_4 — what the investigators were allowed to do first (ID-06)

*Script line:* their involvement was limited by court order to visual and photographic observations

```
A photographic copy stand in a laboratory of the early 1980s: a plain flat baseboard with a vertical column behind it, a large-format camera mounted on the column looking straight down, two adjustable lamps angled onto the board from either side and switched on, and the board completely empty. Photographed three-quarter from standing height in an otherwise dim room. Nobody is present [STYLE] Avoid: [NEG], documents on the board, printed pages, photographs of anything, brand name on the camera, scale bars with numerals, person in frame
```

### `H121.png` — ACT_4 — the calculations that do not exist in the record

*Script line:* Efforts to obtain copies of the structural design calculations, the report says, were unsuccessful.

```
A hardbound laboratory notebook lying open on a wooden bench under flat north light, photographed from directly above so both pages fill the frame, BOTH PAGES COMPLETELY BLANK with only a faint printed ruling across them, a plain pencil lying across the gutter and a steel rule along the outer edge of the right-hand page. Nothing else on the bench, nobody in the frame [STYLE] Avoid: [NEG], handwriting, figures, sketches, printed page numbers, printed headings, readable ruling labels, person in frame
```

### `H122.png` — ACT_4 — the metallurgy (ID-06)

*Script line:* and to cut specimens out of them came later, by court order

```
A bench-mounted hardness tester of the early 1980s: a heavy cast column and an anvil with a short steel offcut sitting on it, photographed close from a low three-quarter angle in a laboratory, one hard light from the right putting a bright edge along the cast housing and the machined anvil. The instrument's dial is turned away from the camera and no face, scale or figure is visible anywhere. Nobody is in the frame [STYLE] Avoid: [NEG], dial with numerals, gauge face, digits, calibration plate, brand name, nameplate, person in frame
```

### `H123.png` — ACT_5 — outside the room, twenty-seven times (DC-01)

*Script line:* the Commission conducted twenty-seven days of hearing

```
A small windowless anteroom outside a hearing room in a plain American public building of the middle 1980s: four grey stacking chairs standing in a row against a bare painted wall, an empty coat rail on the opposite wall, a hard vinyl floor, one recessed fluorescent panel in the ceiling. Photographed straight on from standing height. Nobody is present, and there is no notice, no sign and no lettering anywhere in the room [STYLE] Avoid: [NEG], notices on the wall, room numbers, name plates, directory boards, seals, person in frame, courtroom interior, gavel, judge's bench
```

### `H124.png` — ACT_5 — the file, closed (DC-22)

*Script line:* no one had yet taken responsibility for the collapse

```
A plain government-issue steel office desk photographed from directly above under flat north light, the desk top otherwise completely bare, with ONE CLOSED PLAIN MANILA FOLDER lying square in the middle of it and nothing else at all — no pen, no paper, no telephone. The folder's tab is blank. Nobody is in the frame [STYLE] Avoid: [NEG], writing on the tab, labels, printed forms, readable documents, seals, person in frame
```

### `H125.png` — ACT_5 — time, with the numbers taken off (DC-03)

*Script line:* It was filed on the fifteenth of November, 1985.

```
A plain institutional wall clock hanging on a bare painted wall in an empty room, photographed slightly from below with a long lens so the clock fills the middle of the frame against flat wall, its face plain white with ONLY BARE TICK MARKS AROUND THE EDGE AND NO NUMERALS ANYWHERE ON IT, two plain black hands, a plain chrome bezel. Flat daylight from the left. Nobody is in the frame [STYLE] Avoid: [NEG], numerals on the dial, digits, brand name on the face, maker's mark, lettering, person in frame
```

### `H126.png` — ACT_5 — the record, boxed (DC-02)

*Script line:* Its decision runs four hundred and forty-two pages.

```
Five identical plain cardboard document boxes with their lids on, stacked two and three high in the corner of a bare office of the middle 1980s, photographed from standing height at a shallow angle, one overhead fluorescent panel above them, a hard vinyl floor and plain painted walls. Every box is completely unmarked — no label, no writing, no number. Nobody is in the frame [STYLE] Avoid: [NEG], labels with writing, box numbers, case numbers, handwriting on cardboard, seals, person in frame
```

### `H127.png` — ENDING — the room, afterwards (⛔-12, ⛔-14)

*Script line:* One hundred and fourteen people went to a tea dance and did not come home.

```
A very large empty interior atrium in an American building of about 1980 at first light, photographed from the floor at standing height at one end: pale tan travertine running away from the camera and still wet from cleaning so it holds one long soft reflection of the glazed roof five storeys above, the daylight cold and even, planting boxes dark at the edges. Nobody is present, nothing crosses the space overhead, and nothing in the picture identifies any particular building [STYLE] Avoid: [NEG], walkways, bridges overhead, suspended structures, hotel branding, logos, signage, person in frame, crowd, rubble, debris, recognisable real building
```

---

## 5. Thumbnails — 6 plates, `T001`–`T006`, **never declared, never a cut**

| id | packaging variant |
|---|---|
| `T001` | packaging variant 1 — ONE ROD / TWO RODS · SAME STEEL |
| `T002` | packaging variant 1 — second framing |
| `T003` | packaging variant 2 — A NUT AND / A WASHER · 114 PEOPLE |
| `T004` | packaging variant 2 — second framing |
| `T005` | packaging variant 3 — NEVER / CALCULATED · NOBODY CHECKED |
| `T006` | packaging variant 3 — second framing |

### `T001.png` — packaging variant 1 — ONE ROD / TWO RODS · SAME STEEL

*Reference:* PACKAGING §2 variant 1

```
TWO LENGTHS OF THREADED STEEL ROD about an inch and a quarter across lying side by side on a dark oiled workbench, ONE LONG AND ONE ROUGHLY HALF ITS LENGTH, with a plain heavy hexagonal steel nut and one flat round steel washer lying beside them, photographed from just above the bench at a shallow angle SO ALL OF IT SITS IN THE LOWER 60 PERCENT OF THE FRAME. One hard directional key light from the left runs along the thread so every turn stands out and the steel is markedly brighter than anything behind it. The bright bare bench top runs across the bottom third and is the brightest part of the picture. THE ENTIRE UPPER 40 PERCENT OF THE FRAME IS ONE UNBROKEN FIELD of plain dark out-of-focus workshop with no object, no edge and no detail crossing it anywhere [TSTYLE] Avoid: [NEG], stamped markings on the rod, size markings, grade markings, brand name, dimension callouts, hand, person in frame, rust, object in the top of the frame, low contrast, dull flat lighting, dark subject, detail crossing the top of the frame
```

### `T002.png` — packaging variant 1 — second framing

*Reference:* PACKAGING §2 variant 1

```
The same two lengths of threaded steel rod, one long and one roughly half its length, lying side by side on the same dark oiled bench with the same plain nut and flat washer beside them, now closer and from a lower angle almost level with the bench top so the near ends of the rods read large across the lower third of the frame and the thread catches one hard key light from the left as a row of bright specular ridges. High contrast, bright exposure, the bench top the brightest thing in the picture. THE ENTIRE UPPER 40 PERCENT IS ONE UNBROKEN FIELD of plain dark out-of-focus workshop with nothing in it at all [TSTYLE] Avoid: [NEG], stamped markings on the rod, size markings, grade markings, brand name, dimension callouts, hand, person in frame, rust, object in the top of the frame, low contrast, dull flat lighting, dark subject, detail crossing the top of the frame
```

### `T003.png` — packaging variant 2 — A NUT AND / A WASHER · 114 PEOPLE

*Reference:* PACKAGING §2 variant 2

```
A SINGLE THREADED STEEL ROD about an inch and a quarter across PASSING DOWN THROUGH A ROUND HOLE IN THE FLAT WEB OF A HOLLOW RECTANGULAR STEEL BOX SECTION, with a flat round washer and a heavy hexagonal nut bearing up against the underside of the web, photographed close and slightly from below SO THE WHOLE ASSEMBLY SITS IN THE LOWER 60 PERCENT OF THE FRAME. One hard directional shop light from the left makes the machined steel markedly brighter than anything behind it and lays a crisp shadow under the nut; the bright lower edge of the box section runs across the bottom third and is the brightest part of the picture. Clean bright steel, no rust, no damage, no deformation. THE ENTIRE UPPER 40 PERCENT IS ONE UNBROKEN FIELD of plain dark out-of-focus shop with nothing crossing it [TSTYLE] Avoid: [NEG], stamped markings, grade markings, dimension callouts, brand name, rust, bent metal, torn steel, hand, person in frame, object in the top of the frame, low contrast, dull flat lighting, dark subject, detail crossing the top of the frame
```

### `T004.png` — packaging variant 2 — second framing

*Reference:* PACKAGING §2 variant 2

```
The same single threaded steel rod passing down through the same round hole in the flat web of the same hollow rectangular steel box section, the same flat washer and heavy hexagonal nut bearing up against the underside, now tighter and squarer on so the washer and the nut fill the lower half of the frame and the machined faces read large. One hard key light from the left, high contrast, bright exposure, the bright underside of the section running across the bottom third. Clean bright steel, no rust, no deformation. THE ENTIRE UPPER 40 PERCENT IS ONE UNBROKEN FIELD of plain dark out-of-focus shop [TSTYLE] Avoid: [NEG], stamped markings, grade markings, dimension callouts, brand name, rust, bent metal, torn steel, hand, person in frame, object in the top of the frame, low contrast, dull flat lighting, dark subject, detail crossing the top of the frame
```

### `T005.png` — packaging variant 3 — NEVER / CALCULATED · NOBODY CHECKED

*Reference:* PACKAGING §2 variant 3 — the packaging's 'low tungsten light' is the FILM-FRAME register and is deliberately overridden here; see the [TSTYLE] note

```
A large tilted drafting board with a big sheet of plain vellum pinned flat across it and a long parallel rule lying square on the sheet, one plain pencil resting on the bottom edge of the board and a wooden stool pushed back from it and empty, photographed from standing height at a shallow angle SO THE BOARD AND THE STOOL SIT IN THE LOWER 60 PERCENT OF THE FRAME. THE SHEET IS COMPLETELY BLANK: an unbroken field of pale vellum with no line, no drawing, no ruling, no figure and no mark of any kind on it. ONE HARD DIRECTIONAL KEY LIGHT from the left makes the sheet the brightest object in the picture and lays a crisp shadow from the parallel rule across it; the bottom edge of the board is bright and is the brightest part of the frame. THE ENTIRE UPPER 40 PERCENT OF THE FRAME IS ONE UNBROKEN FIELD of plain dark out-of-focus drawing office with no object, no edge and no detail crossing it [TSTYLE] Avoid: [NEG], lines on the sheet, drawing, dimension callouts, drawing title block, figures, handwriting, printed grid, stamps, hand, person in frame, object in the top of the frame, low contrast, dull flat lighting, dark subject, detail crossing the top of the frame
```

### `T006.png` — packaging variant 3 — second framing

*Reference:* PACKAGING §2 variant 3

```
The same tilted drafting board with the same completely blank sheet of pale vellum pinned across it and the same long parallel rule lying square on it, now closer and from a lower angle almost level with the board so the near edge of the board makes one strong bright horizontal across the lower third of the frame and the blank sheet rises away from it, one plain pencil in the near corner. THE SHEET IS COMPLETELY BLANK — no line, no drawing, no figure, no mark. One hard key light from the left, high contrast, bright exposure, the sheet markedly brighter than everything behind it. THE ENTIRE UPPER 40 PERCENT IS ONE UNBROKEN FIELD of plain dark out-of-focus drawing office with nothing in it [TSTYLE] Avoid: [NEG], lines on the sheet, drawing, dimension callouts, drawing title block, figures, handwriting, printed grid, stamps, hand, person in frame, object in the top of the frame, low contrast, dull flat lighting, dark subject, detail crossing the top of the frame
```

---

## 6. Delivery

- Names are exactly `H114.png` … `H127.png` and `T001.png` … `T006.png`. No `_v2`, no `_02`, no `_A`.
- Deliver to `H:\pd-media\assets\ai\hyatt`, long edge >= 3840, PNG, 16:9.
- **Headroom plates are NOT added to `episode_spec.mandatory_stills`** and thumbnail plates are not added to anything. Neither file is edited by this order.
- After delivery: `py -3.11 scripts/check_plate_verdicts.py --slug hyatt --scaffold --reviewer <name>`, open every plate, record a verdict for each, then `py -3.11 scripts/check_episode_inputs.py --slug hyatt`. The plate gate blocks the build until every plate in the set carries a resolved verdict bound to the file on disk.

*Generated by `scripts/build_ep68_ep69_headroom_order.py`. The prompt bodies in this document and in the paste files come from one source and the generator checks they are byte-identical.*

---

> **Correction, 2026-08-12.** `distinct_video_assets` was corrected in `episode_spec.v002.json` because the original figure was never derived from the allocator. Superseded numbers may remain in the body above for provenance; the spec is authoritative. See `decisions/0009-DISTINCT-VIDEO-ASSETS-CORRECTION.md`.
