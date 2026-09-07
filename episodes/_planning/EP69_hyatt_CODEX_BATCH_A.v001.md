# EP69 · THE KANSAS CITY HYATT REGENCY WALKWAYS — IMAGE ORDER (Codex) v001

**Episode `PD-2026-069-hyatt` · slug `hyatt` · 2026-08-11**
**Contract:** `episodes/PD-2026-069-hyatt/episode_spec.v001.json` —
`mandatory_stills` **H001.png … H113.png (113 ids)**, `people_plates` **22 ids, named individually**,
`people_plates_min` **22**, 58 `forbidden_subjects`, 22 `forbidden_claims`,
`era_setting` **Kansas City, Missouri, USA, 1978–1988**.
**Design:** `EP69_hyatt_FILM_BIBLE.v001.md` · **Front:** `EP69_hyatt_PACKAGING.v001.md` ·
**Facts:** `EP69_hyatt_FACTS_LEDGER.v001.md` · **Script:** `EP69_hyatt_script.en.v001.md`.
**Paste files:** `EP69_hyatt_CODEX_PASTE_A/batch_01.txt` … `batch_08.txt`. **The prompt bodies in
this document and in those files are generated from one source and are byte-identical.**

---

## 0. Who generates these, and with what

**Image source policy — `.claude/rules/19-ship-gate.md` line 10, unchanged:**

- **Long-form images are Codex by default.** Every plate in this order is a Codex commission.
  **Do not start a local model to fill this order.**
- **Local generation is an exception, not a lane.** Commercially-clear, tuned local paths —
  **SD3.5 Large** via `sd35_gen.py` (first choice) or **SDXL** via `gen_max.ps1` — may be used
  **only** to repair a Codex plate or to fill an emergency gap that would otherwise stop a build.
  **Bare SDXL is not allowed. FLUX.1-dev is not allowed in any deliverable** (non-commercial).
- **Long edge ≥ 3840** on every plate (spec v2 row 5). `public/img` is the render truth.
- Every plate is an **illustration**, never evidence (CLAUDE invariant 11). AI disclosure goes in
  the description at publish.

---

## 1. How the plate count was derived

**Not guessed. Taken from the script's own section word counts**, measured with
`check_script_craft.narration_lines()` on `EP69_hyatt_script.en.v001.md`:

```
section   narration words   / 45, rounded up   floor   plates
HOOK             56               2              6        6     <- 6 cuts in 21 s; the floor governs
OP               33               1              2        2     <- the brand band sits over one shot
ACT_1           722              17              -       17
ACT_2           882              20              -       20
ACT_3           779              18              -       18
ACT_4           980              22              -       22
ACT_5         1,069              24              -       24
ENDING          171               4              -        4
                                                       -----
                                                        113
```

**One commissioned plate per 45 narration words**, section by section, rounded up, with a floor of
6 for the HOOK and 2 for the OP because those two sections cut far faster than the film's average.
**Checked against the cut budget:** at `target_cut_sec` 3.6 the short edge of the runtime band holds
1560/3.6 = 433 cuts, stills may occupy at most 32% of them = **138**, and 113 fits under that at
every edge of the band (`episode_spec.notes` carries the same arithmetic).

---

## 2. The one thing that is barred, stated plainly

**Depicted people are REQUIRED and welcome in this film** (owner decision 2026-07-04). Faces are
allowed. What is barred, absolutely, is the **likeness of a real, identifiable individual**
(CLAUDE invariant 11), and in this episode that has specific names attached:

| Never depict as a person | Why |
|---|---|
| **Daniel M. Duncan, Jack D. Gillum** | named publicly, disciplined by a state board, and possibly living. Every criticism in this film is a tribunal's finding, read as a finding (⛔-15, ⛔-20) |
| **any victim or survivor of 17 July 1981** | neither the federal report nor the court names one, so there is nothing to select from and nothing to depict (⛔-13, ND-09) |
| **any rescuer, firefighter, witness, board member or judge** | same rule (⛔-13) |
| **the Nissan-style "identifiable employee"** — here, any Havens Steel employee | Havens is a real named company and no tribunal made a finding against it (⛔-16) |

And these must never be produced as an image at all, in any style (⛔-11, ⛔-12, ⛔-14):

1. a body, an injured person, blood, a covered casualty, a rescue in progress, or debris with a
   person under it;
2. the crowded lobby at, or in the seconds before, the moment of collapse — **from any angle,
   including from above, including in silhouette, including abstracted**;
3. anything that reads as an authentic record: drawing S405.1, Shop Drawing 30, a page of the
   442-page Commission decision, a Missouri professional engineer's seal with a real name or the
   real State of Missouri artwork, an NBS test photograph, a newspaper front page, a court exhibit;
4. **the Hyatt Regency itself** — its atrium, its walkways, its signage or its logo. The building
   is real and currently trading. `hyatt` is in `forbidden_subjects` so no clip title can carry it;
   only a human eye can stop a *picture* from carrying it.

**Quoted document text may be set as typography** — the NBS conclusions and the court's findings
are public record and there is a great deal of very good language to use — **but it must never be
styled to look like a photograph or a scan of the original.** Card, not scan. That distinction is
the whole rule, and every card carries its source in small type:
`NBS Building Science Series 143 (1982)` or `Duncan v. Missouri Bd., 744 S.W.2d 524 (Mo. App. 1988)`.

---

## 3. House look, and the three eras

Everything is **photographic**. No illustration style, no infographic style, no isometric anything.
The typographic figures and the five hero objects are built in Remotion, MOTIONKIT and 3D, **not**
baked into plates.

| | **1978–79 — the board** (ACT_1, ACT_2) | **1981 — the room** (ACT_3) | **1984–88 — the record** (ACT_4, ACT_5) |
|---|---|---|---|
| light | tungsten, one lamp, warm pools | daylight through a glazed roof, warm | north light, cold, high contrast |
| palette | vellum cream, brass, oiled steel, dark green | tan travertine, amber, dark foliage | limestone grey, ink, worn carpet |
| lens | 50mm, close, shallow | 24–35mm, wide, deep | 50–85mm, level, static, negative space |
| texture | paper tooth, pencil, mill scale | polished wood, stone, glass | cut stone, brass, paper edges |
| framing | objects and hands | very large and very empty | vertical lines, doorways, empty rooms |

**The period screen is the one that will fail.** Nothing here may contain a mobile phone, a laptop,
a flat-panel monitor, an LED work lamp, a cordless tool, a hi-vis vest, a modern safety helmet, a
CAD screen or a car built after 1990. It is in `[NEG]` on every plate and it is in `era_setting`.
**Look at every delivered plate for it anyway** — `check_pool_frames.py` surfaces suspects for human
attention and does not detect them.

---

## 4. `[STYLE]` and `[NEG]` — expand both, delete nothing

**`[STYLE]`** = appended to the end of every prompt body, exactly as written:

> , cinematic still, photographic, muted natural colour, American Midwest between 1978 and 1988, tungsten interiors and flat midday daylight, low contrast but never crushed: shadows keep their detail and the frame reads clearly on a phone screen, shallow depth of field, restrained documentary framing, worn unglamorous surfaces, painted steel, vellum, brass, cut stone, plaster and travertine, nothing staged for advertising, ultra-detailed, photoreal, 4K, 16:9, fine film grain, no text, no lettering, no numerals, no watermark, no logo, no signage

**`[NEG]`** = appended after `Avoid:`, exactly as written:

> text, lettering, numerals, digits, handwriting, cursive writing, legible signature, dimension callouts, drawing title block, seals, emblems, logos, insignia, badge, name plates, readable words on a sign, recognisable person, identifiable person, likeness of a real individual, portrait of a named person, celebrity, public figure, deepfake, collapsed building, collapsing structure, rubble, debris, wreckage, ruined interior, rescue worker, ambulance, stretcher, injured person, blood, body, casualty, funeral, firefighter, hospital, crowded hotel lobby, packed function room, crowd of people indoors, courtroom interior, gavel, judge's bench, scales of justice, hourglass, a handshake, police officer, uniform, handcuffs, prison bars, mobile phone, smartphone, laptop, flat-panel monitor, LED work lamp, cordless power tool, hi-vis safety vest, modern safety helmet, CAD screen, car built after 1990, night vision green, thermal false colour, crosshairs, CCTV monitor grid, drone shot, aerial view, golden hour, sunset glow, postcard scenery, Christmas, tropical, glossy advertising lighting, flat CGI, cartoon, illustration, oversaturated, HDR halo

> ### ★ `[NEG]` does NOT forbid people ★
> What it forbids is **`recognisable person, identifiable person, likeness of a real individual,`**
> **`portrait of a named person, celebrity, public figure, deepfake`** — i.e. **resembling somebody
> who exists**. EP66's batch A wrote `human face, facial features, eyes` into its `[NEG]`, which
> stopped people appearing at all, and **191 plates had to be regenerated.** Those three tokens are
> deliberately absent here. Do not put them back. `scripts/check_image_order_neg.py` checks that
> the face/likeness family is covered without them.

> ### ★ Per-plate `[NEG]` additions ★
> Where a prompt reads `Avoid: [NEG], …`, the words after the comma are **added to** the canonical
> `[NEG]` above. **Expand the canonical block in full first and delete nothing from it.**

---

## 5. The people lane — `[HSTYLE]`, 22 plates, all mandatory

**This is the lane that makes the film about human beings**, and in this episode it is unusually
constrained, because ⛔-11 bars bodies and casualties, ⛔-12 bars the crowded room and ⛔-13 bars
every real individual in the record. **So the people in this film are people at work, in rooms
where nobody died.** Hands rolling a drawing flat; a hand setting a plain seal onto paper; a
draughtsman at a board; gloved hands on a steel section; three stamps landing on a drawing edge;
a technician holding a rolled print; a caretaker crossing an empty ballroom; a clerk carrying paper
down a corridor; two people talking in a doorway.

`[HSTYLE]` preamble, already prepended to the body of every people-lane plate below:

```
[HSTYLE] photographic, 35mm, natural light, real adults in ordinary late-1970s and 1980s American
working clothes, ordinary bodies, believable American setting, candid framing, no styling, no
beauty retouching, no model look, no stock-photo smiles, expressions neutral and unremarkable,
nobody looking at the lens
```

`episode_spec.people_plates` names all 22 ids explicitly rather than relying on a filename
convention, because `check_episode_inputs` once reported "0 of 10" on forty plates that existed and
were correct: **H011, H016, H021, H029, H034, H038, H043, H050, H055, H059, H067, H072, H078, H083,
H088, H093, H097, H100, H104, H108, H111, H113.**

**Nine of the twenty-two carry a resolvable face — eight full, one in profile only — and that is
deliberate.** None of them is
presented, captioned, cut or narrated as anyone in this record. They are draughtsmen, fabricators,
technicians and clerks in the abstract — the ordinary people whose ordinary conduct the Commission
found had combined into something lethal, which is the film's thesis. A film that hides every face
while arguing that a system of ordinary people killed 114 of them has argued against itself.

---

## 6. The plates

### HOOK — `H001`–`H006` (6 plates, 0 in the people lane)

**`H001.png`**

```
A single length of threaded steel rod about an inch and a quarter across lying alone on a matt black surface that fills the whole frame, seen in macro from the side so the frame is almost entirely the rod, lit by one hard raking light coming in low from the left so that every turn of the thread throws its own small shadow and the crests catch a thin bright line along the top of the bar. The steel is clean mill finish with faint machining marks, slightly grey rather than shiny. Nothing else is in the frame and the background falls away to pure black at both ends [STYLE] Avoid: [NEG]
```

**`H002.png`**

```
A steel fabricator's bench in a workshop in the late 1970s, lit by one shaded bulb hanging above it, with a large sheet of plain unmarked paper laid flat and weighted at two corners by short offcuts of steel bar, a long steel straight-edge lying diagonally across the sheet and a sharpened pencil beside it. The sheet is completely blank. Behind the bench the shop falls away into soft darkness with the shapes of steel stock racked against a wall. No hands and nobody in the frame [STYLE] Avoid: [NEG]
```

**`H003.png`**

```
A large sheet of plain drafting vellum stretched on a drawing board, seen square on from directly above, filling the frame, warm tungsten light raking across it so the tooth of the paper shows. One single fine straight line has been ruled down the middle of the sheet from top to bottom in hard pencil, and there is nothing else on the paper at all: no border, no notes, no marks, no smudges, no other lines [STYLE] Avoid: [NEG]
```

**`H004.png`**

```
The same sheet of plain drafting vellum on the same board from the same position in the same light, now carrying two fine straight pencil lines instead of one, running parallel down the sheet a short distance apart, the second line noticeably fresher and darker than the first. Nothing else is on the paper: no border, no notes, no marks, no other lines [STYLE] Avoid: [NEG]
```

**`H005.png`**

```
A wide view of a very large empty interior atrium in an American building of about 1980, five storeys of open air with a glazed roof high above, tan travertine floor, planting boxes with dark foliage, a low fountain rim, and warm afternoon daylight coming down through the glass and lying across the floor in long soft rectangles. The room is completely empty: not one person anywhere in the frame, no furniture set out, no event, no decoration. Camera at standing height near one wall [STYLE] Avoid: [NEG]
```

**`H006.png`**

```
An extreme close view of the thread of a steel rod, so close that only four or five turns of the thread cross the frame diagonally, hard raking light along the crests, the roots of the thread in deep shadow, faint oil sitting in the grooves. The far end of the rod falls out of focus into a dark workshop with one warm point of light in it [STYLE] Avoid: [NEG]
```

### OP — `H007`–`H008` (2 plates, 0 in the people lane)

**`H007.png`**

```
A plain heavy hexagonal steel nut and one flat round steel washer lying side by side on a dark oiled workbench beside the threaded end of a steel rod, seen close from a low three-quarter angle, one soft light from the left. The three objects are ordinary hardware with mill finish and light handling marks. Deep soft shadow behind them, nothing else in the frame [STYLE] Avoid: [NEG]
```

**`H008.png`**

```
A close view of a round hole drilled through the flat web of a hollow rectangular steel section, seen at a slight angle so the thickness of the steel is visible at the edge of the hole and the dark inside of the section shows through it. The cut edge is clean and slightly burred. Cold diffuse workshop light from above, the rest of the section falling away out of focus [STYLE] Avoid: [NEG]
```

### ACT_1 — `H009`–`H025` (17 plates, 3 in the people lane)

**`H009.png`**

```
A wide exterior of a large American hotel and office tower of about 1980, precast concrete and bronze-tinted glass, twenty storeys, seen from across an empty street at midday under a pale flat sky, with two period cars parked at the kerb and low trees on the pavement. Ordinary, unglamorous, nothing decorative. No signage, no lettering and no brand marks anywhere on the building [STYLE] Avoid: [NEG]
```

**`H010.png`**

```
Looking straight up inside a very large empty atrium at the glazed roof five storeys above, the steel glazing bars making a grid against a bright white sky, planted balconies stepping back on one side, warm reflected light on tan stone. Not one person in the frame. Shot from floor level with a wide lens, the walls converging upward [STYLE] Avoid: [NEG]
```

**`H011.png`**  **[HSTYLE] people lane, resolvable face**

```
[HSTYLE] photographic, 35mm, natural light, real adults in ordinary late-1970s and 1980s American working clothes, ordinary bodies, believable American setting, candid framing, no styling, no beauty retouching, no model look, no stock-photo smiles, expressions neutral and unremarkable, nobody looking at the lens. A draughtsman in his fifties standing at a large tilted drawing board in a quiet office in about 1978, seen from three-quarters at chest height so his head and shoulders and both forearms are in frame, shirt sleeves rolled to the elbow, a pencil in his right hand resting on the board, looking down at the work with a plain unremarkable expression. A goose-neck lamp throws warm light across the board. The sheet on the board is entirely blank. Behind him a wall of plain flat files [STYLE] Avoid: [NEG]
```

**`H012.png`**

```
A narrow steel and concrete footbridge crossing high inside a large open interior space, seen from directly below with a wide lens, hanging from thin vertical steel rods that run up out of frame into the dark ceiling structure. The underside of the bridge, its steel edge beam and the two rods nearest the camera are sharp; the space beyond is soft. Nobody is on the bridge and nobody is in the frame [STYLE] Avoid: [NEG]
```

**`H013.png`**

```
A single thin steel hanger rod running vertically up out of frame into a dark ceiling of steel purlins and ductwork, seen close against the darkness with one hard light glancing off one side of the rod so it reads as a bright vertical line. The ceiling structure behind is barely resolved. Nothing else in the frame [STYLE] Avoid: [NEG]
```

**`H014.png`**

```
Two lengths of eight-inch steel channel section lying on a workshop bench with their open faces turned toward each other and a hand's width of gap between them, seen from a low three-quarter angle so the C-shaped cross-section of the nearer one is clearly readable at the cut end. Cold diffuse shop light, dark bench, faint mill scale on the steel [STYLE] Avoid: [NEG]
```

**`H015.png`**

```
An extreme close view along a continuous fillet weld running down the joint between two pieces of steel, the weld bead showing its regular stacked ripples, slight blue and straw heat colouring in the steel either side of it, fine spatter. Hard low light along the bead so the ripples read as a row of small crescents. The steel falls out of focus at both ends of the frame [STYLE] Avoid: [NEG]
```

**`H016.png`**  **[HSTYLE] people lane, no face**

```
[HSTYLE] photographic, 35mm, natural light, real adults in ordinary late-1970s and 1980s American working clothes, ordinary bodies, believable American setting, candid framing, no styling, no beauty retouching, no model look, no stock-photo smiles, expressions neutral and unremarkable, nobody looking at the lens. Two gloved hands guiding a length of steel channel section down onto a workshop bench, forearms in worn cotton sleeves entering the frame from the right, no head or body visible, the hands and the end of the steel sharp and the shop behind them dark and soft. Ordinary heavy leather work gloves, scuffed [STYLE] Avoid: [NEG]
```

**`H017.png`**

```
The cut end of a hollow rectangular steel box section seen straight on, filling the middle of the frame, so the rectangle of steel wall and the dark hollow inside it are both clearly readable. The cut face is bright where a saw has been across it, the outer faces dull with mill scale. Plain dark background, one soft light from above left [STYLE] Avoid: [NEG]
```

**`H018.png`**

```
A threaded steel rod passing down through a hole in the underside of a hollow steel box section, with a flat washer and a hexagonal nut drawn up tight against the steel, seen close from below and slightly to one side so the nut, the washer, the underside of the section and three or four turns of exposed thread below the nut are all in frame together. One hard light from the side, deep shadow above [STYLE] Avoid: [NEG]
```

**`H019.png`**

```
Six identical thin steel rods hanging vertically in a row from a dark ceiling structure in a large interior space, evenly spaced, receding away from the camera so they read as a rhythm of bright vertical lines against darkness. Nothing hangs on them and nobody is in the frame [STYLE] Avoid: [NEG]
```

**`H020.png`**

```
A large tilted drawing board in a quiet drawing office of about 1978, seen from a standing position just behind and to one side, a parallel rule lying across a big sheet of blank vellum, an adjustable goose-neck lamp throwing a warm pool of light onto the sheet, a jar of pencils and a scale rule at the top edge, and beyond it the dark rest of the room. The sheet is entirely blank. Nobody in the frame [STYLE] Avoid: [NEG]
```

**`H021.png`**  **[HSTYLE] people lane, resolvable face**

```
[HSTYLE] photographic, 35mm, natural light, real adults in ordinary late-1970s and 1980s American working clothes, ordinary bodies, believable American setting, candid framing, no styling, no beauty retouching, no model look, no stock-photo smiles, expressions neutral and unremarkable, nobody looking at the lens. A technician in his late twenties in a plain shirt and a narrow tie standing in a drawing office in about 1979, holding a large rolled drawing upright against his shoulder, framed from the waist up and turned three-quarters toward the camera, looking off to one side with a plain unremarkable expression, ordinary period haircut. Flat daylight from a window on the left. The rolled sheet is plain paper with nothing showing on it [STYLE] Avoid: [NEG]
```

**`H022.png`**

```
A set of drawing instruments laid out on the corner of a drawing board, seen from directly above: a pair of steel dividers, a triangular scale rule, two sharpened pencils, an eraser shield and a brass pencil sharpener, all on plain vellum. Warm tungsten light from the upper left, long soft shadows. No markings on the rule and no printing anywhere [STYLE] Avoid: [NEG]
```

**`H023.png`**

```
A desk-top electronic calculator of the middle 1970s, beige plastic with a small dark display and large square keys, sitting on a pad of plain engineering paper beside a mug, warm lamp light from the left. The display is dark and unreadable and the pad is completely blank. Shallow focus, the office behind out of focus [STYLE] Avoid: [NEG]
```

**`H024.png`**

```
A thick hardback technical volume with a plain dark cloth binding and a completely blank spine lying closed on a wooden desk under a lamp, a pencil across the cover, deep warm shadow around it. Nothing is printed anywhere on the book [STYLE] Avoid: [NEG]
```

**`H025.png`**

```
A drawing office at night, one large empty drawing board in the middle of the frame with the lamp switched off, a wooden stool pushed back from it at an angle, cold blue light from a window at the far end and no other light. The board is bare. Nobody in the frame [STYLE] Avoid: [NEG]
```

### ACT_2 — `H026`–`H045` (20 plates, 4 in the people lane)

**`H026.png`**

```
The inside of a steel fabrication shop in the late 1970s, a long empty aisle running away from the camera between racks of structural steel sections, an overhead travelling crane on rails high up, dusty daylight coming in through high dirty windows, oil-dark concrete floor. Nobody in the frame and no machinery running [STYLE] Avoid: [NEG]
```

**`H027.png`**

```
A large flat drawing table in a fabricator's office with a big sheet of plain paper spread across it and weighted at all four corners by steel offcuts, seen from a standing position at one corner so the sheet runs away in perspective. Bare overhead light. The sheet has nothing on it. A window with a workshop beyond it out of focus in the background [STYLE] Avoid: [NEG]
```

**`H028.png`**

```
Two threaded steel rods lying parallel and close together on a dark oiled bench, one of them roughly twice the length of the other, both the same diameter, seen from directly above with one hard light raking across so both threads read. A flat washer and a hexagonal nut lie beside the shorter one. Nothing else in the frame [STYLE] Avoid: [NEG]
```

**`H029.png`**  **[HSTYLE] people lane, no face**

```
[HSTYLE] photographic, 35mm, natural light, real adults in ordinary late-1970s and 1980s American working clothes, ordinary bodies, believable American setting, candid framing, no styling, no beauty retouching, no model look, no stock-photo smiles, expressions neutral and unremarkable, nobody looking at the lens. Two bare adult hands flattening a large rolled drawing out across a table, one hand pressing the near edge down and the other running along the curl at the far side, forearms in rolled shirt sleeves entering from the bottom of the frame, no head or body visible. Warm lamp light. The sheet is plain and entirely unmarked [STYLE] Avoid: [NEG]
```

**`H030.png`**

```
An exploded arrangement laid out in a neat row on a dark surface, seen from directly above: a length of threaded rod, a flat washer, a hexagonal nut, and beside them a short offcut of hollow rectangular steel box section with a drilled hole in its face. Even soft top light, each object casting its own shadow, generous empty space between them [STYLE] Avoid: [NEG]
```

**`H031.png`**

```
The underside of a length of hollow rectangular steel box section, seen close and straight on, with two round drilled holes in it a short distance apart along the length of the section. Clean cut edges, mill scale on the steel, one raking light from the left so the holes read as two dark ellipses [STYLE] Avoid: [NEG]
```

**`H032.png`**

```
The threaded end of a steel rod in extreme close-up, filling the frame diagonally, the last few turns of thread slightly bruised from handling, a film of dark oil sitting in the roots. Hard narrow light from one side, everything beyond the first inch out of focus into black [STYLE] Avoid: [NEG]
```

**`H033.png`**

```
One flat round steel washer lying alone on dark oiled wood, seen from slightly above, filling the middle third of the frame, the hole in its centre black, one hard light from the upper left casting a long shadow to the right. Faint circular grinding marks on the face of the washer. Nothing else in the frame [STYLE] Avoid: [NEG]
```

**`H034.png`**  **[HSTYLE] people lane, resolvable face**

```
[HSTYLE] photographic, 35mm, natural light, real adults in ordinary late-1970s and 1980s American working clothes, ordinary bodies, believable American setting, candid framing, no styling, no beauty retouching, no model look, no stock-photo smiles, expressions neutral and unremarkable, nobody looking at the lens. A man in his forties in a short-sleeved shirt sitting at a plain steel desk in a fabricator's office under a low hanging lamp, framed from the chest up and turned three-quarters to the camera, looking down at a large sheet of plain paper in front of him with a neutral working expression, a pencil in his hand. The office behind him is dim and ordinary. The sheet is blank [STYLE] Avoid: [NEG]
```

**`H035.png`**

```
A wooden rack holding a dozen rolled drawings in cardboard tubes, the open ends of the tubes turned toward the camera and filling the frame in a rough grid, the paper inside each one visible as a pale spiral. Flat side light. Nothing is written or printed on any tube [STYLE] Avoid: [NEG]
```

**`H036.png`**

```
A steel flat-file cabinet with one wide shallow drawer pulled out, seen from a standing height at a slight angle, large sheets of plain paper lying flat inside the open drawer with their edges showing. Cold overhead light, grey-green paint on the cabinet. Nothing on any sheet is visible and there are no labels on the drawer fronts [STYLE] Avoid: [NEG]
```

**`H037.png`**

```
Three wooden-handled rubber stamps lying face down in a row on the bare corner of a large sheet of plain paper, seen from directly above, warm lamp light from the left throwing three short shadows. The handles are worn. No printing on the handles and no ink impression anywhere on the sheet [STYLE] Avoid: [NEG]
```

**`H038.png`**  **[HSTYLE] people lane, no face**

```
[HSTYLE] photographic, 35mm, natural light, real adults in ordinary late-1970s and 1980s American working clothes, ordinary bodies, believable American setting, candid framing, no styling, no beauty retouching, no model look, no stock-photo smiles, expressions neutral and unremarkable, nobody looking at the lens. A single adult hand pressing a wooden-handled rubber stamp down onto the corner of a large sheet of plain paper on a table, forearm in a rolled shirt sleeve entering from the right, no head or body in frame, seen from a low angle across the surface of the sheet so the paper runs away out of focus. The hand and the stamp are sharp [STYLE] Avoid: [NEG]
```

**`H039.png`**

```
The bare corner of a large sheet of plain paper carrying three overlapping rectangular ink impressions, seen close from directly above in warm lamp light. The impressions are worn, uneven and deliberately unreadable: soft edges, broken ink, no legible characters of any kind inside any of them [STYLE] Avoid: [NEG]
```

**`H040.png`**

```
A loose pile of large folded drawings lying on a wooden chair in the corner of an office, seen from standing height, the folds and edges catching flat daylight from a window out of frame. The uppermost sheet shows only blank paper. Dust on the floor beside the chair [STYLE] Avoid: [NEG]
```

**`H041.png`**

```
An American construction site in 1979, the structural steel frame of a large building four storeys up against a pale flat sky, bare beams and columns, timber formwork on the deck, a stack of steel decking, an old crawler crane at the edge of the frame. Ordinary and unglamorous. Nobody in the frame [STYLE] Avoid: [NEG]
```

**`H042.png`**

```
A tower crane standing against a completely flat pale grey sky above the unfinished concrete frame of a large building, seen from the ground with a long lens so the jib runs right across the top of the frame. No lettering anywhere on the crane. Nobody in the frame [STYLE] Avoid: [NEG]
```

**`H043.png`**  **[HSTYLE] people lane, no face**

```
[HSTYLE] photographic, 35mm, natural light, real adults in ordinary late-1970s and 1980s American working clothes, ordinary bodies, believable American setting, candid framing, no styling, no beauty retouching, no model look, no stock-photo smiles, expressions neutral and unremarkable, nobody looking at the lens. Three men in ordinary work clothes and plain old-fashioned hard hats standing together on the open deck of an unfinished building, seen from behind at about twenty feet so no face is visible, one of them pointing up at the steel above them. Flat overcast daylight, bare concrete deck, the city beyond soft in the haze [STYLE] Avoid: [NEG]
```

**`H044.png`**

```
A steel erection detail high in an unfinished frame: the end of a beam bolted to a column, two thin hanger rods dropping away below it, seen from below against a bright overcast sky so the steel reads as dark silhouette with a rim of light along its top edges. Nobody in the frame [STYLE] Avoid: [NEG]
```

**`H045.png`**

```
The inside of a site office trailer in 1979, a plywood board on the wall with large sheets pinned to it, a plain desk under the window with a mug and a hard hat on it, a bare fluorescent tube overhead. The pinned sheets are blank paper. Nobody in the frame [STYLE] Avoid: [NEG]
```

### ACT_3 — `H046`–`H063` (18 plates, 3 in the people lane)

**`H046.png`**

```
The unfinished roof structure of a large atrium seen from the floor below, long steel purlins running across the frame with empty glazing frames between them and bright white sky showing through, timber props standing up from the deck at intervals. Bare, incomplete, nobody in the frame [STYLE] Avoid: [NEG]
```

**`H047.png`**

```
One bent length of steel angle lying alone on a swept concrete floor in an unfinished interior, the kink in the middle of it clearly visible, flat daylight from a large opening at the far end. The floor around it is clean and empty. Nothing else in the frame and nobody in the frame [STYLE] Avoid: [NEG]
```

**`H048.png`**

```
An empty ballroom in an American hotel of about 1980, a polished wooden dance floor filling the middle of the frame, a low carpeted bandstand at the far end with no instruments and no musicians on it, banquet chairs stacked neatly against the side wall, warm tungsten light from ceiling fittings. Completely empty: nobody anywhere in the frame [STYLE] Avoid: [NEG]
```

**`H049.png`**

```
A wide of a large empty hotel atrium in mid-afternoon, tan travertine floor, planting boxes, a low fountain, five storeys of open air above with a glazed roof, strong warm daylight coming down through the glass and lying in long rectangles across the floor. Camera at standing height at one end of the room. Not one person anywhere in the frame [STYLE] Avoid: [NEG]
```

**`H050.png`**  **[HSTYLE] people lane, no face**

```
[HSTYLE] photographic, 35mm, natural light, real adults in ordinary late-1970s and 1980s American working clothes, ordinary bodies, believable American setting, candid framing, no styling, no beauty retouching, no model look, no stock-photo smiles, expressions neutral and unremarkable, nobody looking at the lens. A caretaker in plain work clothes crossing the middle of a large empty ballroom floor at midday, seen from across the room so the figure is small in the frame and turned away from the camera, a folded cloth over one shoulder. Warm light from high windows, the polished floor reflecting the figure. Nobody else in the frame [STYLE] Avoid: [NEG]
```

**`H051.png`**

```
The same ballroom with round banquet tables and chairs now set out in rows across the floor, seen from the same position at the same height in the same warm tungsten light, every chair empty and nobody anywhere in the room. Plain white cloths, no decoration, no place settings [STYLE] Avoid: [NEG]
```

**`H052.png`**

```
A low carpeted bandstand in an empty function room with a single microphone stand on it and nothing else, no instruments, no music stands, no musicians, seen straight on from the floor with warm light from above. The room in front of it is empty [STYLE] Avoid: [NEG]
```

**`H053.png`**

```
The same large empty hotel atrium in late afternoon, the daylight through the glazed roof now lower and more amber, the shadows longer and running across the tan floor at a steep angle, the planting darker. Camera at standing height at the same end of the room as before. Not one person anywhere in the frame [STYLE] Avoid: [NEG]
```

**`H054.png`**

```
The same large empty hotel atrium in early evening, daylight almost gone from the glazed roof, the interior lamps now on and throwing warm pools onto the tan floor, the upper storeys falling into blue shadow. Camera at standing height at the same end of the room as before. Not one person anywhere in the frame [STYLE] Avoid: [NEG]
```

**`H055.png`**  **[HSTYLE] people lane, resolvable face**

```
[HSTYLE] photographic, 35mm, natural light, real adults in ordinary late-1970s and 1980s American working clothes, ordinary bodies, believable American setting, candid framing, no styling, no beauty retouching, no model look, no stock-photo smiles, expressions neutral and unremarkable, nobody looking at the lens. A hotel porter in a plain dark jacket standing at the edge of a wide empty carpeted floor with his hands behind his back, framed from the waist up and turned toward the camera, an ordinary tired neutral expression, ordinary period haircut. Warm interior light. No badge, no name plate, no insignia anywhere on the jacket. The room behind him is empty [STYLE] Avoid: [NEG]
```

**`H056.png`**

```
A polished wooden dance floor seen close from a low angle, the grain and the scuffs of the boards running away from the camera, warm light glancing across it from the left so the surface reads as a long bright plane. The far edge of the floor and the darkness beyond are out of focus. Nobody in the frame [STYLE] Avoid: [NEG]
```

**`H057.png`**

```
A tall stack of banquet chairs pushed against a papered wall in an empty function room, seen from a low three-quarter angle, the frames making a repeating pattern of legs and seat backs, one warm lamp on the wall above them. Nobody in the frame [STYLE] Avoid: [NEG]
```

**`H058.png`**

```
A plain service corridor behind a hotel function room, painted breeze block walls, a run of grey vinyl floor, three identical closed doors along one side and a bare bulkhead light overhead, running away from the camera to a corner. No signage of any kind. Nobody in the frame [STYLE] Avoid: [NEG]
```

**`H059.png`**  **[HSTYLE] people lane, no face**

```
[HSTYLE] photographic, 35mm, natural light, real adults in ordinary late-1970s and 1980s American working clothes, ordinary bodies, believable American setting, candid framing, no styling, no beauty retouching, no model look, no stock-photo smiles, expressions neutral and unremarkable, nobody looking at the lens. Two adult hands setting a row of glasses out along a long table under a plain white cloth, forearms in rolled white sleeves entering from the right, no head or body in frame, the near glasses sharp and the far end of the table out of focus. Warm interior light [STYLE] Avoid: [NEG]
```

**`H060.png`**

```
One thin steel hanger rod seen against a dark ceiling from a low angle, standing very slightly out of vertical, a hard narrow light running down one side of it. The ceiling behind is almost black. Nothing else in the frame [STYLE] Avoid: [NEG]
```

**`H061.png`**

```
An extreme macro of a heavy flat steel washer bearing hard against a steel plate, the plate around the washer beginning to dish very slightly downward so the surface curves away from the rim, a bright line of light along the deformed edge. Cold hard light from one side. Nothing else in the frame [STYLE] Avoid: [NEG]
```

**`H062.png`**

```
A nearly black frame with one narrow shaft of pale grey light entering from the upper left and falling across a small area of plain concrete floor, everything else in deep unresolved darkness. No object, no person, no texture other than the concrete in the light [STYLE] Avoid: [NEG]
```

**`H063.png`**

```
A large hotel atrium at night with all the interior lamps off, seen from standing height at one end, the tan floor now a cold grey plane lit only by faint spill from outside through the glazed roof, the planting reduced to black shapes. Completely empty and completely still [STYLE] Avoid: [NEG]
```

### ACT_4 — `H064`–`H085` (22 plates, 4 in the people lane)

**`H064.png`**

```
A plain American federal office building of the 1960s seen from across an empty forecourt at midday, precast concrete panels, regular windows, a flat parapet, low steps up to a recessed entrance. Flat pale light, no flags, no lettering, no signage of any kind. Two period cars parked at the kerb. Nobody in the frame [STYLE] Avoid: [NEG]
```

**`H065.png`**

```
A large structural test frame in a laboratory of the early 1980s: two heavy steel uprights and a crosshead, a short steel specimen clamped upright in the middle of it, hydraulic hoses running down to a pump unit on the floor, painted concrete floor and a high bay behind. Cold even light. Nobody in the frame and nothing readable on any instrument [STYLE] Avoid: [NEG]
```

**`H066.png`**

```
A dial gauge on a magnetic stand clamped against a steel plate, seen close from a low angle so the round face of the gauge fills the left of the frame and the plunger touching the steel is sharp on the right. The face of the gauge is turned just far enough away that no marking on it can be read. Cold workshop light [STYLE] Avoid: [NEG]
```

**`H067.png`**  **[HSTYLE] people lane, no face**

```
[HSTYLE] photographic, 35mm, natural light, real adults in ordinary late-1970s and 1980s American working clothes, ordinary bodies, believable American setting, candid framing, no styling, no beauty retouching, no model look, no stock-photo smiles, expressions neutral and unremarkable, nobody looking at the lens. Two adult hands adjusting the stem of a dial gauge on a test rig, forearms in the cuffs of a plain white coat entering from the left, no head or body in frame, the hands and the gauge sharp and the steel frame beyond out of focus. Cold even laboratory light [STYLE] Avoid: [NEG]
```

**`H068.png`**

```
A hydraulic ram and a load cell mounted in the crosshead of a steel test frame, seen close from below, thick steel plate, four tension rods running down past the camera, a pressure hose looping away to the right. No dials or readouts are legible anywhere in the frame. Cold light, deep shadow above [STYLE] Avoid: [NEG]
```

**`H069.png`**

```
A short steel test specimen lying on its side on a laboratory bench after being pulled apart, the torn metal at the failure surface bright and crystalline against the dull mill finish of the rest, the deformation clearly visible. One raking light from the left, plain dark bench, nothing else in the frame [STYLE] Avoid: [NEG]
```

**`H070.png`**

```
A short offcut of hollow rectangular steel box section standing on a laboratory bench with a threaded rod and its washer pulled part of the way down through the drilled hole in its face, the steel around the hole bent downward into a shallow funnel. Seen close from a low three-quarter angle, one hard light from the left. Nothing else in the frame [STYLE] Avoid: [NEG]
```

**`H071.png`**

```
A strip chart recorder of the early 1980s with a pen arm tracing a single continuous line onto a wide roll of paper feeding out of the front, seen close from above at a slight angle. The trace is a plain curve; no grid numbers or scale markings can be read anywhere on the paper. Cold laboratory light [STYLE] Avoid: [NEG]
```

**`H072.png`**  **[HSTYLE] people lane, resolvable face**

```
[HSTYLE] photographic, 35mm, natural light, real adults in ordinary late-1970s and 1980s American working clothes, ordinary bodies, believable American setting, candid framing, no styling, no beauty retouching, no model look, no stock-photo smiles, expressions neutral and unremarkable, nobody looking at the lens. A woman in her thirties in a plain white laboratory coat standing beside a large steel test frame, framed from the waist up and turned three-quarters to the camera, one hand resting on the frame, looking off toward the specimen with a plain working expression, hair tied back in an ordinary early-1980s style. Cold even light, the high bay behind her out of focus [STYLE] Avoid: [NEG]
```

**`H073.png`**

```
A steel rule laid flat across a deformed steel plate, seen very close from a low angle so the rule runs away from the camera and the dishing of the plate lifts it clear of the surface in the middle. The graduations on the rule are turned away and cannot be read. Hard raking light from the right [STYLE] Avoid: [NEG]
```

**`H074.png`**

```
A shallow steel tray holding a dozen identical short steel test coupons stacked loosely, seen from directly above, each one showing a bright torn end. Cold even light from above, the tray filling most of the frame. Nothing is written on the tray or on any coupon [STYLE] Avoid: [NEG]
```

**`H075.png`**

```
A large empty structural testing hall, high roof with north light, an overhead travelling crane, two test frames standing idle at the far end, painted lines on a bare concrete floor running away from the camera. Cold daylight, no equipment running, nobody in the frame [STYLE] Avoid: [NEG]
```

**`H076.png`**

```
A stack of six thick bound technical reports with plain uniform card covers lying flat on a desk under a lamp, seen close from a low three-quarter angle so the block of paper edges fills the middle of the frame. Nothing is printed on any cover or spine [STYLE] Avoid: [NEG]
```

**`H077.png`**

```
A single thick government report lying closed on a wooden desk under a work lamp, its cover plain uncoated card with no printing on it at all, the edges of the paper block slightly uneven, a pencil lying across the corner. Warm lamp light, deep shadow beyond [STYLE] Avoid: [NEG]
```

**`H078.png`**  **[HSTYLE] people lane, no face**

```
[HSTYLE] photographic, 35mm, natural light, real adults in ordinary late-1970s and 1980s American working clothes, ordinary bodies, believable American setting, candid framing, no styling, no beauty retouching, no model look, no stock-photo smiles, expressions neutral and unremarkable, nobody looking at the lens. Two adult hands turning the pages of a thick bound report open flat on a desk, forearms in plain shirt sleeves entering from the bottom of the frame, no head or body visible, seen from above at a steep angle. The pages are blank paper. Warm lamp light from the left [STYLE] Avoid: [NEG]
```

**`H079.png`**

```
A slide rule and a pad of plain paper lying on a wooden desk beside a heavy mug, seen from directly above in warm lamp light, a pencil across the pad. The scales of the slide rule are turned away and unreadable, and the pad is completely blank [STYLE] Avoid: [NEG]
```

**`H080.png`**

```
A large blackboard on an office wall, wiped clean but carrying the faint ghosting of old chalk, seen straight on so it fills the frame, a wooden chalk rail along the bottom with two short pieces of chalk and a felt eraser on it. Nothing is written on the board. Cold daylight from the left [STYLE] Avoid: [NEG]
```

**`H081.png`**

```
A steel rod held upright in the jaws of a heavy bench vice, seen close from a low angle against a dark workshop, one hard light from the right catching the thread and the top edge of the vice. Iron filings on the bench top below. Nothing else in the frame [STYLE] Avoid: [NEG]
```

**`H082.png`**

```
A plain rectangular meeting room with one long table down the middle, a single microphone on a short stand at the near end of it, and a dozen empty chairs pushed in around it. Grey carpet, plain walls, cold daylight from a window on the left. Nobody in the frame and nothing on the table but the microphone [STYLE] Avoid: [NEG]
```

**`H083.png`**  **[HSTYLE] people lane, resolvable face**

```
[HSTYLE] photographic, 35mm, natural light, real adults in ordinary late-1970s and 1980s American working clothes, ordinary bodies, believable American setting, candid framing, no styling, no beauty retouching, no model look, no stock-photo smiles, expressions neutral and unremarkable, nobody looking at the lens. A man in his sixties in a plain dark jacket and open-collared shirt seated alone at the end of a long table in a plain room, framed from the chest up and turned three-quarters to the camera, hands folded in front of him, an ordinary composed expression, looking slightly away from the lens. Cold window light from the left. Nothing on the table in front of him [STYLE] Avoid: [NEG]
```

**`H084.png`**

```
Four rows of empty stacking chairs facing a long table at the far end of a plain hearing room, seen from behind the back row at seated height, cold flat light from windows down one side, grey carpet and plain walls. Every chair is empty and nobody is in the frame [STYLE] Avoid: [NEG]
```

**`H085.png`**

```
A large wall calendar hanging on a plain painted wall, seen slightly from below with a long lens so the printed grid is soft and completely unreadable, warm light from a lamp out of frame to the right. No characters of any kind are legible anywhere on it [STYLE] Avoid: [NEG]
```

### ACT_5 — `H086`–`H109` (24 plates, 6 in the people lane)

**`H086.png`**

```
The front of a large American civic building in pale limestone, seen from low on the steps at midday, six plain square piers carrying a heavy cornice, deep shadow between them, a flat bright sky above. Sober and undecorated. No signage, no inscription, no lettering anywhere on the stone [STYLE] Avoid: [NEG]
```

**`H087.png`**

```
A pair of heavy bronze doors set in a stone opening, closed, seen straight on and filling most of the frame, shallow panelled relief on the metal, a dark green patina in the recesses and a polished line along the edges where hands have passed. No words, no numbers and no emblem anywhere on the doors [STYLE] Avoid: [NEG]
```

**`H088.png`**  **[HSTYLE] people lane, no face**

```
[HSTYLE] photographic, 35mm, natural light, real adults in ordinary late-1970s and 1980s American working clothes, ordinary bodies, believable American setting, candid framing, no styling, no beauty retouching, no model look, no stock-photo smiles, expressions neutral and unremarkable, nobody looking at the lens. One adult hand resting on a polished brass handrail on a flight of stone stairs, seen close from below and behind so only the hand, the wrist and a dark coat cuff are in frame, the rail running away out of focus up the steps. Cold daylight from a high window [STYLE] Avoid: [NEG]
```

**`H089.png`**

```
A stone colonnade seen along its length in hard raking afternoon light, the columns throwing a regular rhythm of deep black shadows across a pale stone floor, the far end of the run falling into darkness. Nobody in the frame [STYLE] Avoid: [NEG]
```

**`H090.png`**

```
A polished stone floor in a large public hall with one long shaft of window light lying across it, seen from standing height at a low angle so the floor runs away and the light picks up the veining in the stone. The rest of the hall is in cool shadow. Nobody in the frame [STYLE] Avoid: [NEG]
```

**`H091.png`**

```
A tall arched window high in a stone wall seen from inside a dark room, the bright overcast sky outside blowing out the glass, the stone reveal and the sill catching a rim of light and everything else in the room reduced to deep shadow. Nobody in the frame [STYLE] Avoid: [NEG]
```

**`H092.png`**

```
A plain administrative hearing room: one long table across the middle of the frame with a microphone on a short stand at its centre, two chairs behind it, a low panelled wall beyond and grey carpet in front. Cold even daylight, no flag, no seal, no emblem and no lettering anywhere. Nobody in the frame [STYLE] Avoid: [NEG]
```

**`H093.png`**  **[HSTYLE] people lane, no face**

```
[HSTYLE] photographic, 35mm, natural light, real adults in ordinary late-1970s and 1980s American working clothes, ordinary bodies, believable American setting, candid framing, no styling, no beauty retouching, no model look, no stock-photo smiles, expressions neutral and unremarkable, nobody looking at the lens. A single person seated at the far end of a very long table in a large plain room, seen from the near end so the figure is small in the frame and turned three-quarters away from the camera, papers stacked in front of them. Cold flat daylight from a window wall on the left. Nobody else in the room [STYLE] Avoid: [NEG]
```

**`H094.png`**

```
A tall stack of loose typed pages, roughly four hundred sheets high, banded once with a rubber band and standing on a plain table, seen from a low angle so the block of paper rises against a plain dark wall. Cold side light picking out the uneven edges of the sheets. No text is legible on the top sheet [STYLE] Avoid: [NEG]
```

**`H095.png`**

```
The same tall block of paper seen edge-on in extreme close-up so the layered sheet edges fill the whole frame as hundreds of fine horizontal lines, cold raking light from one side making each edge throw its own hairline shadow. Nothing else in the frame [STYLE] Avoid: [NEG]
```

**`H096.png`**

```
A manual typewriter of the 1970s on a plain steel office desk, seen from a low three-quarter angle, a single blank sheet of paper rolled into the platen, a stack of clean paper beside it. Cold window light from the left, plain painted wall behind. Nothing is typed on the sheet and no brand mark is visible on the machine [STYLE] Avoid: [NEG]
```

**`H097.png`**  **[HSTYLE] people lane, resolvable face**

```
[HSTYLE] photographic, 35mm, natural light, real adults in ordinary late-1970s and 1980s American working clothes, ordinary bodies, believable American setting, candid framing, no styling, no beauty retouching, no model look, no stock-photo smiles, expressions neutral and unremarkable, nobody looking at the lens. A woman in her fifties in a plain blouse standing at an open drawer of a tall steel filing cabinet in an ordinary office, framed from the waist up and turned three-quarters toward the camera, one hand on the drawer front, looking down into it with a neutral working expression, ordinary early-1980s hair. Cold overhead light. The folders in the drawer carry no labels [STYLE] Avoid: [NEG]
```

**`H098.png`**

```
A wall of identical small steel filing drawers with brass cup handles, filling the whole frame in a regular grid, seen straight on in cold even light. Every card holder on every drawer front is empty and there is no writing anywhere [STYLE] Avoid: [NEG]
```

**`H099.png`**

```
A heavy brass desk seal press standing on a wooden desk under a lamp, seen close from a low three-quarter angle, the jaws open and the die faces completely plain and blank. Warm lamp light from the left, deep shadow behind. No engraving of any kind on the press [STYLE] Avoid: [NEG]
```

**`H100.png`**  **[HSTYLE] people lane, no face**

```
[HSTYLE] photographic, 35mm, natural light, real adults in ordinary late-1970s and 1980s American working clothes, ordinary bodies, believable American setting, candid framing, no styling, no beauty retouching, no model look, no stock-photo smiles, expressions neutral and unremarkable, nobody looking at the lens. One adult hand pressing a plain brass hand seal down onto the corner of a sheet of paper on a desk, forearm in a shirt sleeve entering from the right, no head or body in frame, seen from a low angle across the desk. The die face is blank and the paper is unmarked. Warm lamp light [STYLE] Avoid: [NEG]
```

**`H101.png`**

```
A framed certificate lying face down on a wooden desk, only the plain brown paper backing, the turned wooden frame and the hanging wire visible, a thin film of dust on it. Warm lamp light from the left, deep shadow around. Nothing is written or printed on the backing [STYLE] Avoid: [NEG]
```

**`H102.png`**

```
A plain wooden desk in an office with a blank brass nameplate standing on it, empty of any engraving, a closed folder and a pen beside it, an empty chair pushed back behind the desk. Cold daylight from a window out of frame. Nobody in the frame [STYLE] Avoid: [NEG]
```

**`H103.png`**

```
A long corridor of identical closed office doors running away from the camera, plain painted walls, a run of worn carpet, a line of bulkhead lights on the ceiling. Every door is blank: no numbers, no name plates, no signage anywhere. Nobody in the corridor [STYLE] Avoid: [NEG]
```

**`H104.png`**  **[HSTYLE] people lane, resolvable face**

```
[HSTYLE] photographic, 35mm, natural light, real adults in ordinary late-1970s and 1980s American working clothes, ordinary bodies, believable American setting, candid framing, no styling, no beauty retouching, no model look, no stock-photo smiles, expressions neutral and unremarkable, nobody looking at the lens. Two adults standing talking in the open doorway of a plain office, seen from twelve feet away at chest height, one turned toward the other in three-quarter view and neither of them looking at the camera, ordinary early-1980s office clothes, plain expressions in mid-conversation. Cold flat daylight from a window beyond them [STYLE] Avoid: [NEG]
```

**`H105.png`**

```
An empty office at dusk, one desk with a closed folder on it, a chair turned out from the desk at an angle as though somebody has just left it, a dark window behind with the blue of the sky in it and one lamp still burning on a side table. Nobody in the frame [STYLE] Avoid: [NEG]
```

**`H106.png`**

```
A wall calendar page seen close in warm lamp light with a column of small pencil marks running down one side of the grid, the printed numbers deliberately soft and unreadable. The marks are simple short strokes, nothing else. Plain painted wall behind [STYLE] Avoid: [NEG]
```

**`H107.png`**

```
A single plain envelope lying face down on a doormat just inside a front door, seen from standing height looking down, cold morning light coming through the frosted glass of the door and falling across the mat. The envelope is completely blank. Nobody in the frame [STYLE] Avoid: [NEG]
```

**`H108.png`**  **[HSTYLE] people lane, no face**

```
[HSTYLE] photographic, 35mm, natural light, real adults in ordinary late-1970s and 1980s American working clothes, ordinary bodies, believable American setting, candid framing, no styling, no beauty retouching, no model look, no stock-photo smiles, expressions neutral and unremarkable, nobody looking at the lens. A clerk in ordinary office clothes carrying a tall stack of loose paper down a plain corridor, seen from behind at about twenty feet so no face is visible, the stack held against the chest with both arms. Cold overhead light, worn carpet, closed doors down both sides [STYLE] Avoid: [NEG]
```

**`H109.png`**

```
The front of a large stone civic building at dusk, seen from across an empty street, one row of windows on the second floor lit warm yellow and every other window dark, the sky a deep blue behind the parapet. No signage, no inscription and no lettering anywhere. Nobody in the frame [STYLE] Avoid: [NEG]
```

### ENDING — `H110`–`H113` (4 plates, 2 in the people lane)

**`H110.png`**

```
A single length of threaded steel rod lying alone on a matt black surface that fills the whole frame, seen in macro from the side, lit by one hard raking light from the right so every turn of the thread throws its own shadow and a thin bright line runs along the crests. Slightly cooler and harder light than the same object at the head of the film. Nothing else in the frame [STYLE] Avoid: [NEG]
```

**`H111.png`**  **[HSTYLE] people lane, no face**

```
[HSTYLE] photographic, 35mm, natural light, real adults in ordinary late-1970s and 1980s American working clothes, ordinary bodies, believable American setting, candid framing, no styling, no beauty retouching, no model look, no stock-photo smiles, expressions neutral and unremarkable, nobody looking at the lens. A single person in an ordinary dark coat walking away from the camera down a wide empty stone corridor, small in the frame and turned completely away so no face is visible, cold daylight from tall windows down one side falling across the floor in a row of bright patches. Nobody else in the corridor [STYLE] Avoid: [NEG]
```

**`H112.png`**

```
A single wide flat span crossing a large open interior space and resting at each end on two stout square columns that stand on the floor below it, seen from the floor at a low angle with a wide lens, cold daylight from a glazed roof above. Plain, heavy and undecorated, with no rods and nothing hanging. Nobody in the frame [STYLE] Avoid: [NEG]
```

**`H113.png`**  **[HSTYLE] people lane, resolvable face**

```
[HSTYLE] photographic, 35mm, natural light, real adults in ordinary late-1970s and 1980s American working clothes, ordinary bodies, believable American setting, candid framing, no styling, no beauty retouching, no model look, no stock-photo smiles, expressions neutral and unremarkable, nobody looking at the lens. A man in his forties in a plain jacket standing alone in the middle of a very large empty interior space, framed from the knees up and turned about three-quarters away from the camera so only the side of his face is visible in profile, looking up toward the roof. Cold daylight from above, the floor stretching away empty in every direction. Nobody else in the frame [STYLE] Avoid: [NEG]
```

---

## 7. Delivery, naming and checks

- **Names are exactly `H001.png` … `H113.png`.** `check_spec_satisfied.py` reads `mandatory_stills`
  by basename, and a plate called `hyatt_rod_final.png` does not exist as far as the contract is
  concerned.
- **Do not put any `forbidden_subjects` word in a filename.** The gate matches them word-wise
  against source filenames, so `H047_debris_angle.png` fails the build even if the picture is one
  bent piece of steel on a clean floor.
- Deliver to `H:/pd-media/assets/ai/hyatt/`, 3840 long edge, PNG, 16:9.
- Depth maps for the plates that get 2.5D motion go to
  `remotion/public/hyatt/img/<name>_depth.png` (film bible §10 — **a still that is only Ken
  Burns-zoomed is rejected as kamishibai**).
- After delivery: build a **labelled contact sheet and look at it**, period screen first, then
  `py -3.11 scripts/check_episode_inputs.py --slug hyatt`.
- **Four plates are continuity pairs and a generator has no memory between prompts.** `H004` must
  be `H003` with one more pencil line on it; `H051` must be `H048` with the tables set out; `H053`
  and `H054` must be `H049` at two later times of day. The ledger's §12 substitution — the same
  wide of the same empty atrium at three o'clock, at half past four and at seven — **only works if
  it is visibly the same room from the same camera position.** If the delivered plates do not
  match, do NOT regenerate them: re-grade `H003`, `H048` and `H049` and change only the light. This
  is checked by eye on the contact sheet and by no machine.

## 8. What is NOT in this order, and why

- **The five hero objects (H1 the rod, H2 the connection assembling, H3 the two drawings, H4 the
  load bar, H5 the pull-through) are BUILT, not commissioned.** They are 3D and Remotion, because
  they have to move in a controlled way and because H3 and H4 carry numbers, which a generated
  plate may never do. `H001`, `H006`, `H110` and `H018` are the still plates that share H1's and
  H2's subject so the film's first frame and its last frame are the same object.
- **No plate carries a beat that the script does not have.** Every id above is placed in a direction
  block in `EP69_hyatt_script.en.v001.md`, by range, at the head of its section. **A plate with no
  beat is not commissioned** — that rule is why this order is 113 plates and not 160.
- **No thumbnail plate is ordered here.** The three thumbnail plates are specified in
  `EP69_hyatt_PACKAGING.v001.md` §2 with their measured headline ink, and they are commissioned
  with the same `[STYLE]`/`[NEG]` when the owner picks a variant.

*Written 2026-08-11 against the contract, the ledger and the delivered script. The prompt bodies in
this document and in `EP69_hyatt_CODEX_PASTE_A/batch_01.txt` … `batch_08.txt` are emitted from one
source and are byte-identical; the equality is reported by the generator rather than asserted here.*
