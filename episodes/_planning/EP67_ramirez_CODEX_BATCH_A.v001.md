# EP67 · TRANSUNION v. RAMIREZ — IMAGE ORDER (Codex) v001

**Episode `PD-2026-067-ramirez` · slug `ramirez` · 2026-08-11**
**Contract:** `episodes/PD-2026-067-ramirez/episode_spec.v001.json` —
`mandatory_stills` **R001.png … R096.png (96 ids)**, `people_plates` **R073.png … R096.png (24 ids)**,
`people_plates_min` **24**, 47 `forbidden_subjects`, 17 `forbidden_claims`.
**Design:** `EP67_ramirez_FILM_BIBLE.v001.md` · **Front:** `EP67_ramirez_PACKAGING.v001.md` ·
**Facts:** `EP67_ramirez_FACTS_LEDGER.v001.md`.

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

## 1. The one thing that is barred, stated plainly

**Depicted people are REQUIRED and welcome in this film** (owner decision 2026-07-04). Faces are
allowed. What is barred, absolutely, is the **likeness of a real, identifiable individual**
(CLAUDE invariant 11), and in this episode that has five specific names attached:

| Never depict as a person | Why |
|---|---|
| **Sergio L. Ramirez** | a living private individual, described sympathetically in a published opinion (⛔-07) |
| **his wife, his father-in-law** | same; the record gives their presence and nothing else (SR-01) |
| **the Nissan salesman or any dealership employee** | never named in either opinion, never a party, never heard (⛔-08) |
| **the two SDNs whose entries "purportedly matched" him** | the record does not print their names, and this pass deliberately did not retrieve them (⛔-09, ○-10) |
| **any Justice — Kavanaugh, Thomas, Kagan, or any of the nine** | opinions appear as **attributed typography**, never as a portrait |

And four things must never be produced as an image at all, in any style (⛔-13):

1. a TransUnion credit report, 2. the OFAC Letter, 3. an OFAC / SDN list entry,
4. any court record, docket, verdict form or filing.

**Their text may be set as typography** — the letter and the alert are quoted in a published
opinion, so the *words* are public record — **but it must never be styled to look like a photograph
of the original document.** Card, not scan. That distinction is the whole rule.

**Global negative prompt, on every plate in this order:**

```
no legible text, no readable documents, no paper with writing, no signage, no brand marks,
no logos, no licence plates, no screens with readable content, no gavel, no scales of justice,
no handcuffs, no police, no weapons, no military, no flags of extremist groups, no hourglass,
no handshake, no children, no cartoon, no 3d render look, no watermark, no lens flare wash,
no yellow colour wash, no green night-vision, no crosshair overlay, no CCTV grid, no thermal
false-colour
```

---

## 2. House look for this episode

Two visual eras, and the audience must feel the move between them at **18:30**.

| | **2011 — the counter** (HOOK · ACT_1 · ACT_2) | **2021 — the law** (ACT_4 · ACT_5 · ENDING) |
|---|---|---|
| light | bright Californian daylight, large windows, glass | low side light, deep shadow, north light |
| palette | pale grey, white, asphalt, chrome, one warm skin tone | ink `#0B0E14`, stone, gold `#E5B53A` used once per act |
| lens | 35mm, eye level, shallow but not showy | 50–85mm, level, static, more negative space |
| texture | showroom floor, plastic, keyboard, envelope paper | cut stone, marble, brass, dark wood |
| framing | people present, often partial | vertical lines, doorways, empty rooms |

**ACT_3 sits between them** and mixes: courthouse exteriors in daylight, offices in shadow.

Everything is **photographic**. No illustration style, no infographic style, no isometric anything.
The typographic figures are built in Remotion and MOTIONKIT, not baked into plates.

---

## 3. THE PEOPLE LANE — `[HSTYLE]` · R073–R096 (24 plates, all mandatory)

**This is the lane that makes the film about human beings.** It is declared in the contract as
`people_plates` so no tool has to guess from a filename which plates these are.

`[HSTYLE]` prompt preamble, prepended to every plate R073–R096:

```
[HSTYLE] photographic, 35mm, natural light, real adults, ordinary clothing, ordinary bodies,
believable American setting, candid framing, no styling, no beauty retouching, no model look,
no stock-photo smiles, faces neutral and unremarkable, nobody looking at the lens
```

| id | plate | face? | where it lands |
|---|---|---|---|
| R073 | three adults' shoulders and backs at a sales desk, seen from behind, near hands sharp, everything beyond them soft | **no** — backs only | HOOK 0:05.3 |
| R074 | one adult hand flat on a desk beside a set of keys, wedding band, mid-forties skin | no | HOOK 0:08.3 |
| R075 | a hand on a keyboard, monitor light on the knuckles, screen out of frame | no | HOOK 0:08.3 |
| R076 | a woman's hands signing at a counter, pen mid-stroke, paper blank | no | A1-04 |
| R077 | a man in his forties, seen from behind, standing in a bright showroom, hands at his sides | no | A1-05 |
| R078 | a couple walking away across a car lot at midday, small in frame | no | A1-05 |
| R079 | an adult opening an envelope at a kitchen table, hands and forearms only | no | A1-08 |
| R080 | **a man's face in three-quarter profile, reading, expression neutral, ordinary kitchen behind** | **yes** | A1-12 |
| R081 | the same setting, empty chair, morning light | no | A1-13 |
| R082 | a hand holding a telephone handset against a shoulder | no | A1-15 |
| R083 | **a woman in her thirties at an office desk, mid-shot, looking down at work** | **yes** | A2-10 |
| R084 | a pair of hands at a keyboard in a dim open-plan office, several empty desks behind | no | A2-12 |
| R085 | **a group of eight adults on a city pavement, walking, mixed ages, nobody in focus** | **yes, incidental** | A3-08 |
| R086 | a crowd of about forty adults crossing a wide street, high angle, faces unresolvable | incidental | A3-11 |
| R087 | **a man in his sixties waiting in a plain corridor, seated, hands folded** | **yes** | A3-12 |
| R088 | twelve pairs of shoes and lower legs in a row of waiting-room chairs | no | A3-13 |
| R089 | a hand pushing a stack of paper across a table to another hand | no | A3-14 |
| R090 | **a woman in her fifties on a suburban porch, arms crossed, looking off frame** | **yes** | A4-13 |
| R091 | a family kitchen at night, nobody in it, two chairs pulled out | no | A4-13 |
| R092 | **a man in a coat on stone courthouse steps, back three-quarters, city behind** | face partial | A5-01 |
| R093 | a hand resting on a closed office drawer | no | A5-09 |
| R094 | **two adults talking at a doorway, mid-shot, neither looking at camera** | **yes** | A5-12 |
| R095 | an empty office at dusk, one chair turned out from the desk | no | ENDING |
| R096 | **a wide of a residential street at dusk, three separate people on it, all distant** | incidental | ENDING |

**Nine plates carry a resolvable face and that is deliberate.** None of them is presented,
captioned, cut or narrated as anyone in this record. They are the people the story is *about* in the
aggregate — 8,185 of them — and a film that hides every face while telling you 8,185 people were
called terrorists has argued against itself.

---

## 4. BATCH A — the four things the archive does not have (R001–R053)

Measured in `EP67_ramirez_FOOTAGE_PLAN.v001.md` §3: `car dealership`, `envelope`, `mailbox`,
`desk drawer`, `file cabinet`, `courthouse`, `supreme court` and `courtroom` all return **0 usable
clips** after two query rounds. These 53 plates are what fills those four holes, and they carry the
hook, both thumbnails and the ENDING, so they are the first commission.

### A1 · the dealership counter — R001–R017

Bright showroom, midday, big glass, polished floor. **No brand marks anywhere: no badges, no
dealership signage, no licence plates, no manufacturer logos on anything.**

| id | plate |
|---|---|
| R001 | wide of a car showroom interior from the customer side, rows of glass, polished floor, two saloon cars, nobody in frame |
| R002 | a sales desk from behind the customer's shoulder: desk edge, a monitor turned away, a keyboard, a set of keys on the far side |
| R003 | the same desk, empty chair on the far side, keys still there |
| R004 | close on a set of car keys on a desk, shallow focus, showroom bokeh behind |
| R005 | a monitor seen from its back, screen glow spilling round the edge, nothing legible |
| R006 | a keyboard from directly above, a hand's shadow across it |
| R007 | a saloon car's driver door and window from outside, sky reflected in the glass, no badge |
| R008 | a car forecourt at midday, rows of parked cars, heat shimmer, empty |
| R009 | showroom glass from outside, the interior dim behind reflections of the forecourt |
| R010 | an empty customer chair at a sales desk, seen straight on |
| R011 | a printer on a low cabinet, a blank sheet emerging, no text |
| R012 | a car key fob on a blank contract-sized sheet of paper, the paper genuinely blank |
| R013 | the forecourt seen through the showroom door at closing, low sun |
| R014 | a wing mirror with the empty forecourt in it |
| R015 | overhead of a desk: keyboard, mouse, keys, a plain white mug |
| R016 | a corridor of the dealership, back-of-house, plain doors |
| R017 | the forecourt, empty, one car gone from a marked bay — **the ENDING calls back to this** |

### A2 · the two mailings — R018–R031

Domestic, kitchen-table scale, morning light. **Every envelope and every sheet is blank.**

| id | plate |
|---|---|
| R018 | a plain white envelope face down on a wooden kitchen table, one corner lifted, morning light — **thumbnail variant 2 source** |
| R019 | the same envelope, face up, unaddressed |
| R020 | two envelopes side by side on the same table, slightly different sizes |
| R021 | an envelope half opened, the flap torn, contents not visible |
| R022 | a folded blank sheet lying on the envelope it came from |
| R023 | a stack of three folded sheets, edges only, no text |
| R024 | a domestic letterbox on the inside of a front door, one envelope through it |
| R025 | a hand-height view of a kitchen table with an envelope and a cold cup of coffee |
| R026 | the same table, cleared, envelope gone |
| R027 | an envelope on a car passenger seat |
| R028 | a blank sheet held up to a window, backlit, no text showing through |
| R029 | a waste bin with a single envelope in it |
| R030 | an envelope pinned under a fridge magnet, blank |
| R031 | two envelopes in a drawer, closed over them — **bridges to A3** |

### A3 · the desk drawer — R032–R041

**This is the majority's own metaphor** — ✓ *"as if someone wrote a defamatory letter and then
stored it in her desk drawer"* (HD-08) — and the film argues with it for four minutes. All ten
plates share **one camera position, one lens, one light**, so the six motif states read as the same
drawer (film bible §3).

| id | plate |
|---|---|
| R032 | an office desk drawer, closed, one blank envelope on the desk above it |
| R033 | the same drawer, open a hand's width, dark inside |
| R034 | the same drawer, fully open: rows of identical blank paper cards standing on edge, filling it |
| R035 | the same, one card lifted slightly proud of the rest |
| R036 | the same, one card removed, a gap in the row |
| R037 | the drawer closing, motion, the cards blurring |
| R038 | the drawer closed, desk bare |
| R039 | the drawer closed, **a single blank docket-sized slip lying on the desk above it** — the "sold" beat |
| R040 | the same desk from further back, the office empty, dusk |
| R041 | the drawer closed, room dark, one window bright — **ENDING** |

### A4 · the courts, from outside — R042–R053

**No courtroom interior exists in this film** (film bible §10). Stone, doors, columns, light.

| id | plate |
|---|---|
| R042 | American classical courthouse facade, low angle, midday, no signage |
| R043 | the same building's steps, empty, wet |
| R044 | a heavy bronze door, closed, shallow relief, no words |
| R045 | a colonnade in raking light, deep shadow between columns |
| R046 | a marble floor with a shaft of window light across it |
| R047 | a high window in a stone wall seen from inside a dark room |
| R048 | an appellate-scale civic building, three storeys, plain, overcast |
| R049 | a wide of a plaza in front of a civic building, one figure crossing, tiny |
| R050 | a stone cornice against a hard blue sky |
| R051 | a long empty corridor with a stone floor and tall doors, no signage |
| R052 | a brass handrail on stone stairs, close |
| R053 | the facade at dusk, one row of windows lit |

---

## 5. BATCH B — the identifiers that were never compared (R054–R072)

**The film's central visual argument.** OFAC publishes, for each entry — ✓ *"a full name, address,
nationality, passport, tax ID or cedula number, place of birth, date of birth, former names and
aliases"* (LS-08). TransUnion compared two of them. ACT_2 builds that list on screen one item at a
time and then removes everything but the first and last name.

**These plates are the *objects*, not the words.** The words are Remotion typography over them.

| id | plate |
|---|---|
| R054 | a blank passport-sized booklet, closed, on a dark surface, no crest, no text |
| R055 | the same booklet, open, both pages blank |
| R056 | a plain paper form, blank, on a desk, ruled boxes only, no printing |
| R057 | a rubber date stamp lying on its side, the face unreadable |
| R058 | a globe's surface at a shallow angle, no labels legible |
| R059 | a street of ordinary houses in daylight — *address* |
| R060 | a hospital-corridor-free maternity-free plain civic register office exterior — *place of birth* |
| R061 | a wall calendar with the numbers out of focus — *date of birth* |
| R062 | a name plate on a desk, blank brass |
| R063 | a filing card, blank, held between two fingers |
| R064 | a wall of small identical drawers, brass handles, no labels |
| R065 | a bank of identical grey server cabinets in a cold room, no lights legible |
| R066 | fibre optic cable ends, close, out of focus behind |
| R067 | a cursor-free monitor showing only a field of soft light |
| R068 | overhead of hundreds of identical blank record cards laid in a grid, one lifted — **thumbnail variant 3 source** |
| R069 | the same grid, two cards lifted, far apart |
| R070 | the same grid at a lower angle, receding out of focus |
| R071 | a printed line of perforated continuous paper, folded, blank |
| R072 | a single blank card on an otherwise empty dark table |

---

## 6. BATCH C — the people lane (R073–R096)

**See §3.** Twenty-four plates, all mandatory, `[HSTYLE]` preamble on every one, nine with a
resolvable face, none of them anyone in this record.

---

## 7. BATCH D — optional, staged only if a cut needs it (R097–R130)

Not in `mandatory_stills`. Commissioned in a second pass **after** the first assembly shows where
the film is thin, so nothing is generated that no cut wants (`footage_utilization` ≥ 80%).

| range | subject |
|---|---|
| R097–R104 | Treasury / federal register: plain stone federal building, a flag on a pole against grey sky, an empty official lectern with no seal, a corridor of identical office doors |
| R105–R112 | 1970 and the FCRA: a plain hardback statute book with a blank spine, a bill of continuous paper, an empty committee room, a desk lamp on a wood desk |
| R113–R120 | the money, kept abstract: a bank counter with no branding, a cheque-sized blank slip, an adding machine's ribbon, a paper till roll |
| R121–R126 | weather and the four designed silences: an overcast sky over a low suburb, rain on a car window at rest, a street in flat grey light, dusk over parked cars |
| R127–R130 | the cancelled trip: an airport departures hall at low occupancy with **no readable boards**, a closed suitcase in a hallway, a passport-sized booklet in a drawer, an empty car back seat |

---

## 8. Delivery, naming and checks

- **Names are exactly `R001.png` … `R130.png`.** `check_spec_satisfied.py` reads
  `mandatory_stills` by basename, and a plate called `ramirez_drawer_final.png` is a plate that
  does not exist as far as the contract is concerned.
- **Do not put any of the `forbidden_subjects` words in a filename.** The gate matches them
  word-wise against source filenames, so `R044_gavel_door.png` fails the build even if the picture
  is a door.
- Deliver to `H:/pd-media/assets/ai/ramirez/`, 3840 long edge, PNG.
- Depth maps for the plates that get 2.5D motion go to `remotion/public/ramirez/img/<name>_depth.png`
  (film bible §10 — **a still that is only Ken Burns-zoomed is rejected as kamishibai**).
- After delivery: build a **labelled contact sheet and look at it**, then
  `py -3.11 scripts/check_episode_inputs.py --slug ramirez`.

*Written 2026-08-11 against the contract and the ledger. Every plate above exists to carry a beat
named in `EP67_ramirez_FILM_BIBLE.v001.md` §6. A plate with no beat is not commissioned.*
