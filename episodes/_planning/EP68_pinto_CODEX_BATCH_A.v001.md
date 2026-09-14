# EP68 · THE FORD PINTO / *GRIMSHAW v. FORD* — IMAGE ORDER (Codex) v001

**Episode `PD-2026-068-pinto` · slug `pinto` · 2026-08-11**
**Contract:** `episodes/PD-2026-068-pinto/episode_spec.v001.json` —
`mandatory_stills` **R001.png … R104.png (104 ids)**, `people_plates` **R081.png … R104.png (24 ids)**,
`people_plates_min` **24**, **124** `forbidden_subjects`, **23** `forbidden_claims`,
`era_setting` **USA 1968–1981**.
**Design:** `EP68_pinto_FILM_BIBLE.v001.md` · **Front:** `EP68_pinto_PACKAGING.v001.md` ·
**Facts:** `EP68_pinto_FACTS_LEDGER.v001.md` plus the new rows in film bible §0.5.
**Paste files:** `EP68_pinto_CODEX_PASTE_A/batch_01.txt` … `batch_13.txt` (13 files, 8 plates each).

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

## 1. The things that are barred, stated plainly

**Depicted people are REQUIRED and welcome in this film** (owner decision 2026-07-04). Faces are
allowed, and nine plates carry one. What is barred, absolutely, is the **likeness of a real,
identifiable individual** (CLAUDE invariant 11), and in this episode that has names attached:

| Never depict as a person | Why |
|---|---|
| **Richard Grimshaw** | he was **13** at the time of the crash and **may be living**; a private individual who was a child (⛔-08) |
| **Lilly Gray**, and her surviving family | she died of burns; the record gives the family's presence and nothing else (⛔-09) |
| **Judy Ulrich, Lynn Ulrich, Donna Ulrich** | 18, 16 and 18, who died in Indiana in 1978. Named once in the film, from the wire report, and never depicted |
| **the driver of the van** | never charged, a private individual (⛔-11) |
| **any Ford employee** — Iacocca, MacDonald, Alexander, Kennedy, Copp, Grush, Saunby, Hromi, MacLean, Misch | no court found any individual liable or guilty, and the Elkhart grand jury deliberately charged only the corporation (⛔-10) |
| **any judge, prosecutor or defence lawyer** | the two courts appear as **attributed typography**, never as portraits |

**And two whole categories must never be produced as an image at all, in any style.**

1. **No fire and no crash.** No burning vehicle, no flame, no smoke, no embers, no charred
   surface, no person on fire, no burn injury, no scarring, no skin graft, no bandage, no
   hospital, no ambulance. No collision, no crashed car, no crumpled bodywork, no shattered
   windscreen, no debris field. **This film shows the crash by not showing it** — film bible
   §3.5 fixes what it shows instead, beat by beat, and this order is the other half of that
   decision. Twenty-three fire words and eight crash words are in `forbidden_subjects` so the
   build fails on a filename, not on a viewing.
2. **No document facsimile** (⛔-15): not the Grush/Saunby report, not exhibit 125, not a Ford
   crash-test report, not an NHTSA report or recall notice, not a page of the *Grimshaw* record,
   not the Elkhart indictment, not a period front page. **Their text may be set as typography**
   in Remotion — the words are public record — **but never styled to look like a photograph of
   the original paper. Card, not scan.** That distinction is the whole rule.

**Global negative prompt, on every plate in this order** (this is the canonical `[NEG]`; it is
checked by `scripts/check_image_order_neg.py`, which requires a face/likeness token, a readable-
text token, a handwriting token, a marks-of-authority token and a numerals token):

> text, lettering, numerals, digits, handwriting, cursive writing, legible signature, readable words on a page, seals, emblems, logos, insignia, badge, name plates, wordmarks, manufacturer script, grille emblem, licence plate, registration plate, recognisable person, identifiable person, likeness of a real individual, portrait of a named person, celebrity, public figure, deepfake, fire, flame, flames, smoke, burning, embers, soot, charred surfaces, a burning vehicle, a person on fire, burn injury, scarring, skin graft, bandages, hospital, ambulance, paramedic, blood, a crashed car, collision, wreckage, crumpled bodywork, shattered windscreen, police officer, uniform, patrol car, flashing lights, handcuffs, firearm, courtroom interior, gavel, judge's bench, jury box, witness stand, prison bars, scales of justice, hourglass, a handshake, children, modern smartphones, flat-screen monitors, LED headlights, modern cars, contemporary clothing, plastic modern fittings, night vision green, thermal false colour, crosshairs, CCTV monitor grid, drone shot, golden hour, sunset glow, postcard scenery, Christmas, tropical, glossy advertising lighting, flat CGI, cartoon, illustration, oversaturated, HDR halo

**Note what the `[NEG]` deliberately does NOT contain: `human face`, `facial features`, `eyes`.**
Those three tokens would suppress the people lane, and the people lane is required. What is
suppressed instead is *identifiability* — `recognisable person`, `identifiable person`,
`likeness of a real individual`, `portrait of a named person`.

**Global style prompt, on every plate in this order** (`[STYLE]`):

> cinematic still, photographic, muted natural colour, the United States between 1968 and 1981, mixed tungsten and daylight, low contrast but never crushed: shadows keep their detail and the frame reads clearly on a phone screen, shallow depth of field, restrained documentary framing, worn unglamorous period surfaces — painted steel, brushed aluminium, laminate, bakelite, manila card, newsprint, enamel — nothing staged for advertising, ultra-detailed, photoreal, 4K, 16:9, fine film grain, no text, no lettering, no numerals, no watermark, no logo, no signage

---

## 2. House look for this episode

Two visual eras, and the audience must feel the move between them at **17:40**.

| | **1968–1972 — the car** (ACT_1 · ACT_2) | **1977–1981 — the paper** (ACT_3 · ACT_4 · ACT_5) |
|---|---|---|
| light | tungsten and work lamps, hard raking light on metal | cold north light, window light, fluorescent troffers |
| palette | oil-black, cast iron, primer grey, one warm skin tone | manila, newsprint grey, pale stone, gold `#E5B53A` once per act |
| lens | macro and 35mm, low, close to the object | 50–85mm, level, static, more negative space |
| texture | painted steel, cast housing, rubber, gravel, concrete | paper fibre, laminate, bakelite, cut stone, brass |
| framing | the object fills the frame | rooms with nobody in them |

**ACT_3 sits between them** and mixes: press halls and mail rooms in working light, federal
interiors in shadow.

Everything is **photographic**. No illustration style, no infographic style, no isometric
anything. The typographic figures — the table, the two prices, the quotations — are built in
Remotion and MOTIONKIT, **not baked into plates**.

---

## A1 · THE PAPER — the eight pages, exhibit 125, and the record — R001–R020 (20 plates)

Every sheet is blank or illegible. Typed characters may appear as TEXTURE at an oblique angle or out of focus; not one word, number or letterhead may resolve. No facsimile of any real document exists in this film.

| id | plate | face? | where it lands |
|---|---|---|---|
| R001 | A grey steel office desk under one bright articulated work lamp, photographed straight on from standing height, the desk surface empty and slightly scuffed, the room behind it dark and unresolved, a single powe… | no | HOOK 0:00 |
| R002 | An adult hand laying a small stack of eight typed sheets square on a grey steel office desk lit by one bright articulated work lamp, the room behind it dark and unresolved, seen from just above and behind the h… | no | HOOK 0:02.6 |
| R003 | A small stack of eight typed sheets on a grey steel desk seen from directly overhead under one work lamp, a plain steel paper clip being pressed onto the top left corner, the paper warm white and slightly foxed… | no | HOOK 0:05 |
| R004 | The work lamp swung low so its beam rakes across one page and blows out a ruled grid of tabulated figures into pure white, the ruled lines visible as faint darker threads and the figures themselves entirely los… | no | HOOK 0:09.6 |
| R005 | A small stack of eight typed sheets lying square on a grey steel office desk with the work lamp switched off and only a cold window light on it from the left, the room otherwise dark, the paper the brightest th… | no | HOOK 0:18.2; ENDING |
| R006 | A plain unmarked manila envelope, unsealed and empty, lying flat on a grey steel office desk beside a small stack of typed sheets, its flap open toward camera, one work lamp above | no | OP |
| R007 | A single typed sheet held up against a bright window, backlit, so the typing shows through as an even grey blur and the paper fibre is visible | no | ACT_4 |
| R008 | A tall grey steel filing cabinet with one drawer pulled fully out, rows of manila folders standing on edge inside it, every tab blank, shot from slightly above at a shallow angle | no | ACT_1; ACT_4 |
| R009 | A tall grey steel filing cabinet with every drawer closed, standing in a dim office corner, one desk lamp reflecting off its painted steel front | no | ACT_4 |
| R010 | A stack of continuous perforated computer paper, folded concertina fashion on a low table, the printing on it reduced to fine grey banding by distance and focus | no | ACT_3 |
| R011 | A wide shallow tray of loose typed pages on a mail-room bench, several hundred sheets, seen from directly above, individual sheets indistinguishable | no | ACT_3 |
| R012 | A period electric typewriter on a steel typing table, three-quarter from the side, a blank sheet rolled into the platen, the keys catching a hard side light | no | ACT_1; ACT_4 |
| R013 | Close on the paper bail of that typewriter with a blank sheet under it, extremely shallow focus, the rest of the machine falling away | no | ACT_4 |
| R014 | A cardboard document box with its lid off on a linoleum floor, packed upright with unlabelled folders, a strip of hard corridor light across it | no | ACT_2 |
| R015 | Two identical unmarked manila folders lying side by side on a desk, one very slightly thicker than the other | no | ACT_4 |
| R016 | A hand sliding one sheet out from the middle of a bound stack, only the hand and the sheet edge in focus | no | ACT_4 |
| R017 | A shallow wooden in-tray on the corner of a desk holding a low stack of blank paper, morning light from the left | no | ACT_1 |
| R018 | A waste-paper basket beside a desk with a single crumpled sheet in the bottom of it | no | ACT_4 |
| R019 | A rubber date stamp lying on its side on an ink pad, the rubber face turned away from camera and unreadable | no | ACT_3 |
| R020 | A dark storeroom wall of identical grey steel filing cabinets receding into shadow, one narrow overhead strip light | no | ENDING |

## A2 · THE GAP AND THE FLOAT — hero objects H1 and H2 — R021–R038 (18 plates)

H1 is the film's central image and returns six times: ONE camera position, ONE lens, ONE light across R021–R030 so the returns read as the same car. H2 is the carburettor float, the only reconstruction in the film.

| id | plate | face? | where it lands |
|---|---|---|---|
| R021 | **H1** — The rear axle and differential housing fill the left of the frame, the flat forward face of the fuel tank fills the right, and between them there is a narrow open gap of bare air with the co | no | ACT_1 4:20 — H1 first appearance |
| R022 | **H1** — A plain unmarked steel machinist's rule has been laid horizontally across that gap, bridging from the housing to the tank face, its graduations too fine and too oblique to read | no | ACT_1 — H1 second |
| R023 | **H1** — Closer on the differential housing alone, several bolt heads standing proud of its cast surface and facing the tank, oil-blackened and sharply lit | no | ACT_1 A1-08 |
| R024 | **H1** — Closer on the flat forward face of the tank alone, a plain pressed-steel shell with a faint factory seam across it and nothing else | no | ACT_1 |
| R025 | **H1** — The filler neck where it enters the top of the tank, a short rubber and steel joint, seen from below | no | ACT_1 |
| R026 | **H1** — Wider, showing the whole rear underbody: the tank, the axle, the two rear wheels and the underside of the boot floor, with the gap now small in the middle of the frame | no | ACT_4 |
| R027 | **H1** — The same view with the work light switched off and only a cold blue-grey ambient light from the open shutter door behind | no | ACT_5 |
| R028 | **H1** — The empty lift with no car on it, arms lowered, the concrete floor stained, the same light | no | ENDING — H1 last |
| R029 | Close on a single bolt head on a cast-iron surface, macro, oil in the threads, the background a shallow black | no | ACT_1 |
| R030 | A plain unmarked steel machinist's rule lying alone on a workbench under a work light, seen along its length so the graduations foreshorten into an unreadable band | no | ACT_1; ENDING |
| R031 | A brass carburettor float — a small hollow closed brass cylinder on a thin pivot arm — held in a bench vice under a work lamp, macro, the brass dull and slightly discoloured | no | ACT_2 — H2 |
| R032 | A small hollow brass carburettor float on a thin pivot arm, suspended in a clear glass beaker of pale amber liquid and floating high on the surface, macro, backlit so the liquid glows and the meniscus reads cle… | no | ACT_2 — H2 |
| R033 | A small hollow brass carburettor float on a thin pivot arm lying sunk on the bottom of a clear glass beaker of pale amber liquid, the liquid still, macro, backlit, framed and lit exactly as the companion plate … | no | ACT_2 — H2 |
| R034 | A period carburettor removed from an engine and standing on a workbench, its top cover off, seen from above, the float chamber open | no | ACT_2 |
| R035 | An engine bay of an early-1970s American subcompact seen from above with the bonnet up, air cleaner in the middle, everything plain and unbranded | no | ACT_2 |
| R036 | A drafting board at a shallow angle with a large sheet of tracing paper pinned to it, a parallel rule across it, the drawing on the sheet reduced to pale grey lines with no dimension or note legible | no | ACT_1 |
| R037 | A pair of hands at a drafting board carrying a large pinned sheet of tracing paper, one holding a pencil and one steadying a parallel rule, cropped at the forearms | no | ACT_1 |
| R038 | A set of steel dividers, a scale rule and two pencils lying on tracing paper, seen from directly above under a drafting lamp | no | ACT_1 |

## A3 · THE ROAD AND THE MIDDLE LANE — hero object H5, and the unbadged car — R039–R052 (14 plates)

The car is an early-1970s American subcompact hatchback SHAPE and nothing more. No badge, no nameplate, no grille emblem, no plate. It is never occupied and never damaged.

| id | plate | face? | where it lands |
|---|---|---|---|
| R039 | A three-lane American freeway seen from directly above from a fixed high vantage such as a road overbridge, at midday, dry pale concrete, the lane markings running vertically through the frame, all three lanes … | no | ACT_2 — H5 first |
| R040 | A three-lane American freeway photographed from directly above from a fixed high vantage such as a road overbridge, at midday, dry pale concrete, the lane markings running vertically through the frame, dry scru… | no | ACT_2 — H5; thumbnail variant 3 source |
| R041 | A three-lane American freeway photographed from directly above from a fixed high vantage such as a road overbridge, at midday, dry pale concrete, the lane markings running vertically through the frame, dry scru… | no | ACT_2 — H5; ENDING |
| R042 | A three-lane American freeway seen from ground level at the hard shoulder, a low wide lens, heat shimmer over the concrete, no vehicles, dry Southern Californian scrub and a low ridge on the horizon | no | ACT_2 |
| R043 | An early-1970s American subcompact hatchback parked alone on a dry gravel shoulder, side profile, midday, its bodywork a plain unmarked pale colour with no badge, no nameplate, no grille emblem and no plate fro… | no | ACT_1; ACT_3 |
| R044 | A plain unmarked early-1970s american subcompact hatchback in a pale colour, with no badge, no nameplate, no grille emblem, no model script and no plate front or rear, three-quarter from the front on a dry grav… | no | ACT_1 |
| R045 | The rear three-quarter of a plain unmarked early-1970s American subcompact hatchback in a pale colour, with no badge, no nameplate, no grille emblem, no model script and no plate front or rear, on a dry gravel … | no | ACT_1 |
| R046 | Close on the rear wheel and lower rear wing of a plain unmarked early-1970s American subcompact hatchback in a pale colour, with no badge, no nameplate, no grille emblem, no model script and no plate front or r… | no | ACT_1 |
| R047 | The driver's door and window of a plain unmarked early-1970s American subcompact hatchback in a pale colour, with no badge, no nameplate, no grille emblem, no model script and no plate front or rear, seen from … | no | ACT_2 |
| R048 | The empty driver's seat and steering wheel of an early-1970s American car seen from the passenger side, vinyl and hard plastic, nobody in the car, the door shut | no | ACT_2 |
| R049 | A two-lane American highway running away from camera between flat fields, tar-strip patches on the surface, low afternoon light, no traffic | no | ACT_5 |
| R050 | A wide of an American freeway interchange from a fixed high vantage, mid-1970s in character, light traffic of period cars, seen small | no | ACT_3 |
| R051 | A dry roadside verge at close range: gravel, a steel guard rail, dry grass, one plain white-painted post | no | ACT_2 |
| R052 | A row of early-1970s American cars parked nose-in on a hardstanding, seen from behind at eye level, all unbadged and unplated, flat overcast light | no | ACT_3 |

## A4 · THE COURTS, FROM OUTSIDE — R053–R066 (14 plates)

No courtroom interior exists in this film. Stone, doors, columns, corridors, light.

| id | plate | face? | where it lands |
|---|---|---|---|
| R053 | An American classical courthouse facade of pale stone with six plain columns, photographed head-on from the pavement at midday, no signage of any kind on the building | no | ACT_2 |
| R054 | The wide stone steps of an American classical courthouse of pale stone with plain columns above them, empty and wet, seen from the bottom looking up | no | ACT_2 |
| R055 | A heavy bronze double door, closed, shallow relief panels, no words and no crest | no | ACT_2 |
| R056 | A stone colonnade in raking afternoon light, deep shadow between the columns, nobody in the frame | no | ACT_4 |
| R057 | A polished stone floor with a single hard shaft of window light lying across it, shot low | no | ACT_2 |
| R058 | A tall window high in a stone wall, seen from inside a dark room, the glass blown out to white | no | ACT_4 |
| R059 | A long empty corridor with a stone floor, tall panelled doors down one side, no signage, one distant window at the end | no | ACT_2; ACT_5 |
| R060 | A plain mid-century American county courthouse of brick and limestone, three storeys, flat overcast light, a bare flagpole with no flag on it | no | ACT_5 |
| R061 | A wide of an empty civic plaza in front of a stone building, one small distant figure crossing it | no | ACT_5 |
| R062 | A brass handrail on stone stairs, close, worn bright by use | no | ACT_2 |
| R063 | A stone cornice against a hard blue sky, low angle | no | ACT_2 |
| R064 | A plain mid-century american county courthouse of brick and limestone, three storeys, with a bare flagpole and no signage at dusk, with one row of windows lit and the rest dark | no | ACT_5 |
| R065 | A row of empty wooden public benches in a stone-floored anteroom, nobody sitting | no | ACT_5 |
| R066 | A plain unmarked wooden double door at the end of a corridor, closed, one overhead light above it | no | ACT_5 |

## A5 · THE PERIOD ROOMS — 1968 to 1981, which the archive does not have — R067–R080 (14 plates)

The footage plan measured every period query at zero. These fourteen plates are the film's only 1970s interiors and they carry the product review, the press and the regulator.

| id | plate | face? | where it lands |
|---|---|---|---|
| R067 | A 1971 American corporate meeting room: a long veneered table, twelve tubular-framed chairs pushed in, a projector screen rolled down at one end, fluorescent troffers overhead, nobody in the room | no | ACT_1 A1-13 |
| R068 | A 1971 American corporate meeting room seen from the head of a long veneered table, tubular-framed chairs down both sides and a rolled-down projector screen at the far end, with one chair pulled out and a plain… | no | ACT_1 |
| R069 | A 1970s open-plan engineering office: steel desks in rows, drafting lamps, telephone cords, low partitions, nobody at the desks, late light through venetian blinds | no | ACT_1 |
| R070 | A 1970s newspaper press hall: a web of newsprint running at speed through a large offset press, the paper a blur, the ink smell almost visible, no headline legible | no | ACT_3 — HOOK cut 4 |
| R071 | A folded magazine dropping onto a Formica kitchen table in morning light, its cover facing up but out of focus so nothing on it can be read | no | HOOK 0:14; ACT_3 |
| R072 | A 1970s American federal office interior: government-issue steel desks, a wall of card-index drawers, a wire in-tray, an institutional green wall, nobody present | no | ACT_3 |
| R073 | A 1970s mail room: a long sorting bench with pigeonholes above it, canvas sacks below, hundreds of plain unmarked envelopes stacked in the racks | no | ACT_3 |
| R074 | A 1970s American domestic kitchen at breakfast, empty: Formica, a percolator, patterned curtains, morning sun across the table | no | ACT_3 |
| R075 | A period suburban living room with a wood-cased television set switched off in the corner, an armchair, nobody present, afternoon light | no | ACT_3 |
| R076 | A 1970s vehicle test laboratory: a concrete hall, a fixed barrier block at one end, high-speed camera rigs on tripods, floodlights on stands, no vehicle present | no | ACT_1 A1-07 |
| R077 | Close on a period high-speed film camera on a heavy tripod in a concrete vehicle test hall, side on, the lens turned away from camera | no | ACT_1 |
| R078 | An automobile assembly line in the early 1970s: unpainted body shells moving on an overhead conveyor, sparks absent, the hall receding, workers small and distant | no | ACT_1 |
| R079 | A row of finished but unbadged small car bodies in a factory yard under flat cloud, seen from the side | no | ACT_1 |
| R080 | A 1970s telephone on a steel desk, receiver on its cradle, coiled cord, one shaft of window light | no | ACT_3 |

## A6 · THE PEOPLE LANE — [HSTYLE] — R081–R104 (24 plates)

Depicted people are REQUIRED. Nine plates carry a resolvable face on purpose. None of them is anyone in this record.

`[HSTYLE]` prompt preamble, prepended to every plate R081–R104:

```
[HSTYLE] photographic, 35mm, natural light, real adults of the 1970s, ordinary period clothing and ordinary bodies, believable American setting, candid framing, no styling, no beauty retouching, no model look, no stock-photo smiles, expressions neutral and unremarkable, nobody looking at the lens
```

| id | plate | face? | where it lands |
|---|---|---|---|
| R081 | An adult's two hands squaring a small stack of typed sheets on a steel desk under one work lamp, cropped at the forearms, a plain wristwatch on the left wrist, mid-forties skin | no | HOOK 0:02.6 |
| R082 | A pair of hands at a drafting board in a 1970s engineering office, one holding a pencil against a parallel rule, cropped at the elbows, shirt sleeves rolled | no | ACT_1 |
| R083 | A man in his fifties in a 1970s short-sleeved shirt and tie, seated at a drafting board, seen in three-quarter profile, looking down at the work | **yes** | ACT_1 |
| R084 | Twelve pairs of period shoes and lower legs under a long meeting table, seen from floor level, nobody's upper body in frame | no | ACT_1 A1-13 |
| R085 | A woman in her thirties in period office clothing standing at a bank of card-index drawers with one drawer open, mid-shot, looking down into it | **yes** | ACT_1 |
| R086 | A hand pressing a paper clip onto a stack of typed sheets, extreme close, only the hand and the paper in frame | no | HOOK 0:05 |
| R087 | A worker's gloved hands on a steel body panel on an assembly line, cropped at the wrists | no | ACT_1 |
| R088 | A man in his forties in factory overalls standing beside a conveyor, mid-shot, half-turned away, an unremarkable expression | **yes** | ACT_1 |
| R089 | The back of a man in a 1970s suit standing at a window of an upper-floor office, city roofs beyond, seen from inside the dark room | no | ACT_1 |
| R090 | A hand lifting a folded magazine off a kitchen table, cropped at the wrist | no | ACT_3 |
| R091 | A woman in her sixties in period clothing seated at a kitchen table reading a magazine, mid-shot, the magazine's cover turned away from camera | **yes** | ACT_3 |
| R092 | A mail-room worker's hands and forearms sorting plain envelopes into pigeonholes, no face in frame | no | ACT_3 |
| R093 | A man in his fifties in a plain 1970s suit standing in a stone corridor with his back to a tall window, mid-shot, three-quarter, looking off frame | **yes** | ACT_2 |
| R094 | A crowd of about forty adults in 1970s clothing crossing a wide American street, high fixed angle, faces unresolvable at that distance | incidental | ACT_3 |
| R095 | A group of eight adults in 1970s clothing on a city pavement, walking toward camera, mixed ages, nobody in focus | **yes** | ACT_3 |
| R096 | Nine pairs of shoes and lower legs in a row of waiting-room chairs in a stone-floored anteroom | no | ACT_2 |
| R097 | A hand pushing a thick stack of paper across a table toward another hand, cropped above the wrists | no | ACT_2 |
| R098 | A man in his seventies in a plain jacket seated alone on a wooden bench in a courthouse corridor, hands folded, looking at the floor | **yes** | ACT_2 |
| R099 | A woman's hands and forearms at a period electric typewriter, mid-keystroke, a blank sheet in the platen | no | ACT_4 |
| R100 | A woman in her forties in period clothing standing in the doorway of a 1970s federal office, mid-shot, half-turned, an unremarkable expression | **yes** | ACT_3 |
| R101 | The backs of two adults in 1970s clothing walking away down a long stone corridor, small in frame | no | ACT_5 |
| R102 | A farmer's hands on a wooden fence rail at the edge of an Indiana cornfield in August, cropped at the forearms, corn at full height behind | no | ACT_5 |
| R103 | A man in his sixties in work clothes standing at the edge of a cornfield in flat August light, mid-shot, three-quarter, looking away down the road | **yes** | ACT_5 |
| R104 | An empty 1970s office at dusk with one chair turned out from a desk and the lamp still on, nobody present | no | ENDING |

**Nine plates carry a resolvable face and that is deliberate.** None of them is presented,
captioned, cut or narrated as anyone in this record. They are the people the film is about in
the aggregate — the engineers at the boards, the committee at the table, the readers of a
magazine — and a film that hides every face while telling you a jury of ordinary people sat for
six months has argued against itself.

---

## 7. BATCH B — optional, staged only if a cut needs it (R105–R140)

Not in `mandatory_stills`. Commissioned in a second pass **after** the first assembly shows where
the film is thin, so nothing is generated that no cut wants (`footage_utilization` ≥ 80%).

| range | subject |
|---|---|
| R105–R112 | more of the gap: the same H1 camera position with the lift at three heights; the tank shell from four angles |
| R113–R120 | Indiana, August 1978: a two-lane road between corn at full height, a grain elevator, a small-town main street with no signage, a county road junction |
| R121–R128 | the regulator: a card-index room, a wall of unlabelled drawers, a plain federal corridor, a bare lectern with no seal |
| R129–R134 | money kept abstract: an adding-machine ribbon, a paper till roll, a bank counter with no branding, a period ledger with blank ruling |
| R135–R140 | the five designed silences: overcast over a low suburb, rain on a car window at rest, a street in flat grey light, dusk over an empty forecourt |

---

## 8. Delivery, naming and checks

- **Names are exactly `R001.png` … `R140.png`.** `check_spec_satisfied.py` reads
  `mandatory_stills` by basename, and a plate called `pinto_gap_final.png` is a plate that does
  not exist as far as the contract is concerned.
- **Do not put any of the 124 `forbidden_subjects` words in a filename.** The gate matches them
  word-wise against source filenames, so `R023_crash_bolt.png` fails the build even if the
  picture is a bolt, and `R032_fire_float.png` fails even though nothing is burning.
- Deliver to `H:/pd-media/assets/ai/pinto/`, 3840 long edge, PNG, 16:9.
- Depth maps for the plates that get 2.5D motion go to
  `remotion/public/pinto/img/<name>_depth.png` (film bible §10 — **a still that is only Ken
  Burns-zoomed is rejected as kamishibai**).
- The ten H1 plates R021–R030 must be generated as a **set in one session**, because they share
  one camera position, one lens and one light and the film cuts between them six times. If they
  drift, the motif reads as six different cars.
- After delivery: build a **labelled contact sheet and look at it**, then
  `py -3.11 scripts/check_episode_inputs.py --slug pinto`.

*Written 2026-08-11 against the contract, the ledger and the new rows in film bible §0.5. Every
plate above exists to carry a beat named in `EP68_pinto_FILM_BIBLE.v001.md` §6 or a substitution
named in §3.5. A plate with no beat is not commissioned.*
