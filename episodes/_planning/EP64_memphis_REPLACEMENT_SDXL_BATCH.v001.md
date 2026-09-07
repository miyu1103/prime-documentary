# EP64 memphis — replacement plate batch (v001)

**Status: PREPARED, NOTHING EXECUTED.** No image generated, no splice run, no render started, no
upload touched. A render is live on this machine and the GPU is booked; nothing here is run tonight.
Everything below is measured against files on disk on 2026-08-12.

---

## 0. Read this before you generate anything: you probably do not need to

**Zero images are required to clear the block and re-book EP64.**

All sixteen rejected plates were re-ordered and re-generated on **2026-08-05**. The corrected
prompts, and an explicit retirement list, are in
`episodes/_planning/EP64_memphis_CODEX_BATCH_A.v001.md` at the section headed
**`### ★再発注（2026-08-05・全219枚目視QC）`** (line 811). That section ends:

> **廃止：`M013` `M048` `M049` `M070` `M073` `M079` `M094` `M117` `M156` `M159` `M168` `M172`
> `M181` `M191` `M202` `M210`。カットに使わない（削除はしない）。**
> — *retired: do not use in a cut (do not delete)*

and it carries a replacement table, one new plate per retired plate:

| retired | replacement | retired | replacement | retired | replacement |
|---|---|---|---|---|---|
| M013 | **M220** | M079 | **M225** | M172 | **M231** |
| M048 | **M221** | M094 | **M226** | M181 | **M232** |
| M049 | **M222** | M117 | **M227** | M191 | **M233** |
| M070 | **M223** | M156 | **M228** | M202 | **M234** |
| M073 | **M224** | M159 | **M229** | M210 | **M235** |
|      |            | M168 | **M230** | —(new) | **M236** |

**All seventeen exist and all seventeen are in the film.** Measured on
`H:\pd-media\assets\ai\memphis` and `remotion/src/data/memphis_film.json`: M001–M236 exist with no
gaps; M220–M236 each appear in exactly one cut; the sixteen retired plates *also* each appear in a
cut (M202 in two).

So the defect is not a generation defect. **It is an assembly defect.** The replacements were
appended to the pool and packed as *additional* cuts in ACT_5, OP and ACT_1 instead of being
substituted for the plates they were ordered to replace, and `remotion/src/data/memphis_film.json`
was never re-pointed. `episode_spec.v001.json` was updated — `mandatory_stills` names M220–M234 and
names **none** of the sixteen retired plates — so the paperwork moved and the assembly did not.

I opened **M227** at full resolution. It is exactly the M117 brief: an empty windowless room, a bare
table, two plain chairs facing each other across it, one overhead fitting, **nobody in it**. I opened
**M234**: two adults from directly behind, both of full adult build, no face, no profile.

**Therefore the re-book path is a source swap, not a generation run.** See §5.

## What this batch is for, then

Swapping a retired plate's cut to its replacement makes that replacement appear **twice** in the
film — once where it already sits and once where the retired plate was. That is an `asset_reuse` /
`footage_diversity` hit, which `config/ship_policy.v001.json` classes as **advisory**: it does not
stop a ship. This batch exists so the duplication can be removed properly when the GPU is free.

| tier | plates | why |
|---|---|---|
| **A — de-duplication for the two cuts that get spliced now** | `M237` (for cut-0239), `M238` (for cut-0046) | optional; only if the owner would rather not see M227 and M234 twice |
| **B — backlog, next revision** | `M239`–`M252` (14) | the fourteen advisory rejects, if and only if EP64 is ever revised |

**16 images ≤ 30 → local SDXL.** Route and commands in §4.

---

## 1. Why each original failed — the mechanism, not the symptom

Re-rolling a prompt that failed for a structural reason produces the same failure. These are the
structural reasons, read out of the prompts themselves.

### 1.1 The one that matters: M117, and why "no people" was never available

The prompt that produced it, verbatim
(`episodes/_planning/EP64_memphis_CODEX_BATCH_A.v001.md:416`):

```
Two chairs facing each other across a plain table in a small windowless room, nothing on the table, one overhead light and hard shadows under both chairs [STYLE] Avoid: [NEG]
```

It never says the room is empty — and, critically, **it could not have delegated that to `[NEG]`.**
The `[NEG]` block in force when M117 was generated contained no face- or person-suppressing token
at all. The brief says so itself, in the 2026-08-05 addendum to §2: *"上の `[NEG]` には **顔を抑える
語が1つも入っていなかった**"* — the face words were added afterwards, and the addendum states in
terms that they *apply only to plates generated from that point on*. Three plates across two
episodes came back with fully identifiable faces from prompts that never mentioned a person
(EP62 `G174`, EP65 `R019`, `R041`). M117 is the fourth.

But the deeper reason is the R043 reason, and it is why a stronger negative would still not have
worked. **The identifying content of this image is not an object that can be subtracted; it is the
social function of the arrangement.** Two chairs facing each other across a bare table under one
hard overhead light is not a description of furniture — in every photograph the model has ever seen,
it is a description of *two people talking*. Naming that arrangement and then declining to mention
people returns the people, exactly as naming a legislative chamber and subtracting its insignia
returned an identifiable chamber. You cannot negate your way out of a composition whose meaning is
the thing you are trying to exclude.

The fix is not a bigger `[NEG]`. It is to **describe the room as furniture, surfaces and light only,
never by what happens in it, and to make the emptiness the stated subject and the stated moment.**
That is what M227 does — *"one chair pushed in square and the other pulled back a hand's width as
though somebody has just stood up … the room completely empty of people"*. The absence is given a
cause and a time, so there is something to render instead of the people.

### 1.2 Set collapse — nine plates lost to one clause in a shared suffix

Five of the sixteen rejects came back as the family's kitchen or living room when an institution was
ordered: **M070** (line printer on a kitchen counter), **M073** (courthouse steps → kitchen),
**M094** (law-report shelf → kitchen), **M156** (ledger cards → domestic interior), **M168**
(municipal corridor doors → domestic doors). Four more of the flagged plates did the same —
**M071**, **M090**, **M091**, **M093**. Nine plates, one cause.

The cause is in `[STYLE]`, which is appended verbatim to **every prompt in the film**:

> … *Memphis in the middle 1970s — a modest single-storey frame house with painted weatherboard,
> worn linoleum, formica, enamel, bakelite, an ordinary working household, municipal offices of the
> same decade in steel and wood* …

The domestic clause is long, concrete and first. The institutional clause is six words and last.
When the prompt **body** was short and named its location only by function — *"the same steps"*,
*"a shelf of identical volumes"*, *"a second identical door"* — the suffix outweighed the body and
returned the house. Adding *"no kitchen"* to the body could not have fixed it either, because the
kitchen is not in the body: it is in a shared string the prompt author does not control per plate.

The fix, which the 2026-08-05 rewrites use, is to **out-weigh the suffix from inside the body**:
name the institution's own materials (*steel cabinets, lifted floor tiles, strip lighting, dark
wooden library shelf, worn linoleum corridor, plain stone facade*), state a distance and a light that
cannot occur in a domestic room, and put the exclusion in the body rather than trusting `[NEG]`.

### 1.3 "Identical framing to the earlier plate" is an instruction to an editor, not a constraint

**M156, M168, M172, M191** — four of the sixteen — all say some version of *"identical framing"* or
*"framed exactly as earlier in the film"*, and all four came back unmatched. They had to: the model
cannot see the earlier plate. A reference to a frame that exists only in the brief is not a
constraint on the image.

The fix is to **re-state the earlier framing's content in full inside every prompt that must rhyme
with it** — the vantage, the height, the distance, the light direction and the surface — so that two
independently generated plates land in the same place because they were both described, not because
one was told to copy the other.

### 1.4 The rest, briefly

| plate | mechanism |
|---|---|
| **M013** | *"both sets of meters … doubled"* — relational words with no cardinal. A wall of "doubled" hardware is as plausibly seven as four; the model was never given a count. Fix: state the cardinal as a compositional fact (*"exactly four meters and no more"*) and the arrangement that makes the count legible. |
| **M048** | The brief asked one plate to hold two motif states — state 4 (a flat sheet, date band above a white lower half) and state 8 (an envelope falling into a mailbox). No single photograph is both. This was a brief defect, not a generation failure; the 2026-08-05 fix split it into M221 and the newly ordered M236. |
| **M049** | *"The same slip held up flat against a window"* — "held" implies a holder. The prompt ordered a person without naming one. Fix: state what holds it (*a window frame and a wooden clothes peg*) and exclude hand, arm, shoulder and head in the body. |
| **M079** | *"the type dissolved to grey"* — "dissolved" names an appearance the model has no exemplar for, so text renders as text. Fix: specify **geometry** instead of appearance — *"continuous smooth horizontal bands of even grey tone with absolutely no letterforms, no word gaps, no ascenders and no descenders"*. |
| **M159** | *"beside an office window at dusk"* never said what the window looks out on, and "office window at dusk" means a city skyline to a generator. Separately: **no prompt can suppress a generator watermark**, because the mark is applied after sampling, not composed. The only controls are a four-corner sweep at QC — which is how it was found — and retiring the file. |
| **M181** | *"A single **printed** slip lifted from that stack"* — asked for a printed item held between finger and thumb, the model supplied the most photographed one: a photograph. Fix: say blank, and negate pictorial content in the body (*no photograph, no picture, no image, no halftone*). |
| **M202** | *"Two **adults** … one leaning back and one forward"* — "adults" is a label with no scale anchor, and the only thing distinguishing the two figures in the sentence is posture. With nothing fixing size, posture difference renders as size difference. Fix: constrain build **comparatively** (*"both of them plainly grown adults of similar full adult build and shoulder width"*) and forbid the smaller figure in the body. |
| **M210** | The prompt asked for a **result** (*"so the cord reads as a single bright line"*) rather than the light that produces it, and left the upper third to chance. Fix: state the light's side, the handset's fraction of frame height, and empty the upper third by listing what must not be in it. |

---

## 2. Where each replacement lands

Master time = film time **+ 11.5 s** (hookSeconds 8.0 + `Bookends` OPENING_SEC 3.5). Verified at the
pixels on three cuts, not assumed. The **hook lane** has no such offset: it renders at master
00:00–00:08.

| new | retires | cut | film time | master time | treatment | tier |
|---|---|---|---|---|---|---|
| `M237` | M117 | `cut-0239` | 21:05.659 | **21:17.16** | duotone, lift 1.484 | **A** |
| `M238` | M202 | `cut-0046` | 04:05.267 | **04:16.77** | duotone, lift 1.282 | **A** |
| `M239` | M013 | `cut-0079` | 06:57.974 | 07:09.47 | — | B |
| `M240` | M048 | `cut-0118` | 10:22.918 | 10:34.42 | — | B |
| `M241` | M049 | `cut-0119` | 10:27.735 | 10:39.24 | — | B |
| `M242` | M070 | `cut-0139` | 12:12.830 | 12:24.33 | — | B |
| `M243` | M073 | `cut-0151` | 13:16.498 | 13:28.00 | — | B |
| `M244` | M079 | `cut-0166` | 14:35.806 | 14:47.31 | — | B |
| `M245` | M094 | `cut-0204` | 17:58.549 | 18:10.05 | — | B |
| `M246` | M156 | `cut-0248` | 21:52.365 | 22:03.87 | — | B |
| `M247` | M159 | `cut-0254` | 22:24.376 | 22:35.88 | — | B |
| `M248` | M168 | `cut-0272` | 24:00.409 | 24:11.91 | — | B |
| `M249` | M172 | `cut-0284` | 25:04.431 | 25:15.93 | — | B |
| `M250` | M181 | `cut-0320` | 28:16.497 | 28:27.99 | — | B |
| `M251` | M191 | `cut-0330` | 29:07.992 | 29:19.49 | — | B |
| `M252` | M210 | `cut-0343` | 30:16.018 | 30:27.52 | — | B |

`M237` and `M238` land on **duotone** cuts with `lift` 1.484 / 1.282. That pushes contrast hard, so
the brief's rule *黒つぶれさせない* applies with extra force: judge the treated frame, not the raw
PNG.

**Ids:** M001–M236 exist with no gaps (measured across `remotion/public/memphis/img`,
`img_unused`, `motion`, `public_ep64/memphis/img` and `H:\pd-media\assets\ai\memphis`), so **M237 is
the first free id**. Nothing here overwrites an existing plate — CLAUDE invariant 6.

**M210's row is bookkeeping only.** The finding against it was for THUMB-03, and I opened
`09_package/thumbnail.selected.v005.png`: the selected thumbnail is the meter plate carrying *BOTH
WERE RUNNING / TWO METER SETS*. It is not derived from M210. THUMB-03 was never selected, so that
rejection has no live consequence.

---

## 3. The prompts

House style is fixed by §2 and §0.5 of `EP64_memphis_CODEX_BATCH_A.v001.md`: **one sentence, no full
stop**, a stated distance, a stated light **and** a stated moment, terminating in
`[STYLE] Avoid: [NEG]` — both expanded **verbatim** from §2 before generation (the §2 `[NEG]` is the
post-2026-08-05 one, with the face words).

These are deliberately **second camera positions** on the corrected 2026-08-05 briefs, not copies of
them: the point of the batch is that M237 and M227 are two different photographs of the same room.
`§0` of the brief is absolute — **one prompt, one image, no `_02`, no rolling until it looks good.**

---

### Tier A

**`M237.png`** — retires `M117`, lands at cut-0239 (master 21:17.16, duotone lift 1.484)

```
A small windowless municipal interview room photographed from just inside its open doorway at standing height from four metres, a plain table standing square in the middle of the worn linoleum with one plain wooden chair on each side of it turned to face each other across its bare top, nothing whatsoever on the table and nothing hung on the bare plaster walls, one bare overhead fitting hanging directly above the table throwing a hard short pool of light straight down so the chair legs and the table legs each lay their own separate shadow outward across the floor and the corners of the room fall away to unlit grey, the near chair pulled back a hand's width and standing at a slight angle as though somebody left the room a minute ago and the door has been open since, the room completely empty of people with no figure, no seated person, no face, no hand, no arm, no silhouette and nobody at all anywhere in the frame or in the doorway [STYLE] Avoid: [NEG]
```

Why this and not a re-roll of M227's wording: same brief, different vantage (M227 is head-on from
three metres, this is four metres and offset through the doorway) and a different moment (M227's
chair *has just been pushed back*, this one *has been standing a minute*), so the two plates read as
two photographs of one room rather than two takes of one photograph. The emptiness carries a cause
and a time, per §1.1. The hard down-light against unlit corners is a contrast structure, not a tonal
one, so `lift 1.484` strengthens it instead of crushing it.

**`M238.png`** — retires `M202`, lands at cut-0046 (master 04:16.77, duotone lift 1.282)

```
Two adults sitting at a formica kitchen table in a modest 1970s Memphis house photographed from directly behind them at seated height from two and a half metres, both of them plainly grown adults of the same full adult build with the same shoulder width and the same head height as each other, no child, no young person, no teenager and no smaller or slighter figure anywhere in the frame, only the backs of their heads and the tops of their shoulders in view with no face, no profile, no cheek, no ear turned to camera and no reflection of a face in the window glass beyond, both of them sitting still and square with their forearms resting on the table and an untouched mug in front of each, flat grey overcast morning light coming through the window past them so their shoulders read as two matched dark masses against it, the rest of the kitchen unlit and nothing moving in the room [STYLE] Avoid: [NEG]
```

Why: the size constraint is stated **comparatively and three times** (build, shoulder width, head
height), because a single "adults" label is what failed in §1.4. Both figures are given the *same*
posture, removing the posture asymmetry that the generator rendered as a size asymmetry. The face
exclusion is extended to the window reflection, which is the one route left open in a
shot-from-behind.

---

### Tier B — backlog, only if EP64 is revised

**`M239.png`** — retires `M013`
```
The side wall of a modest single-storey painted weatherboard house photographed square on from four metres so the whole run of boards fills the frame, carrying exactly four meters and no more and no fewer: two round glass-domed electric meters mounted side by side on the upper boards and two rectangular cast-iron gas meters mounted side by side directly below them, the two pairs separated by a clear hand's width of empty board so that the counting of them is unmistakable at a glance, every dial cover a plain blank disc and every index window a smooth featureless rectangle carrying no scale, no marking and no figure of any kind, their service pipes dropping to the ground in four parallel runs, low afternoon sun raking from the right so each of the four instruments lays its own separate hard shadow across the boards, the yard beyond thrown soft and nobody anywhere in the picture [STYLE] Avoid: [NEG]
```

**`M240.png`** — retires `M048` (motif state 4 only; state 8 is M236's job)
```
A single unfolded printed final notice lying flat and alone on a worn pale formica kitchen table photographed from directly overhead dead square with the lens parallel to the table from one metre, the sheet filling three quarters of the frame width with its four edges well inside the frame, one heavy horizontal rule crossing it at the midpoint with the half above that rule carrying a dense even band of grey printed texture in which no character resolves anywhere and the half below left completely bare white paper with nothing on it at all so that the difference between a filled top and an empty bottom is the whole subject, a single window's daylight falling flat across the sheet from the left with the table darkening toward every corner, one soft crease still standing where the sheet was folded, nobody in the room [STYLE] Avoid: [NEG]
```

**`M241.png`** — retires `M049`
```
A single thin printed slip pegged flat against the inside of a small kitchen window pane so that flat overcast daylight passes straight through it, photographed square on from eighty centimetres with the sheet filling most of the frame, the printing on the near face dissolved to an even featureless grey wash and the reverse side showing through as a faint mirrored ghost with no character resolving on either face, the slip held only by two wooden clothes pegs clipped to the window catch so that no hand, no finger, no arm, no shoulder, no head, no person and no shadow of a person is anywhere in the picture, a net curtain hanging just out of focus behind the glass and the kitchen behind the camera already dim [STYLE] Avoid: [NEG]
```

**`M242.png`** — retires `M070`
```
A wide fanfold of continuous printer paper spilling from the output slot of a line printer into a wire floor basket in a municipal data processing room of the early 1970s, photographed from two metres at waist height so the machine, the falling paper and two further tape cabinets behind it all read at once, every printed line reduced to an even featureless grey band with no character resolving anywhere, the room around it plainly institutional in painted steel, lifted floor tiles and overhead strip lighting with no kitchen cabinet, no domestic furniture, no curtain and no window anywhere in the frame, no person in the room, in any doorway or in any reflection, the strip light throwing hard shadow down the pleats of the fanfold as the top fold is still falling [STYLE] Avoid: [NEG]
```

**`M243.png`** — retires `M073`
```
The wide shallow stone entrance steps of a plain mid-century federal courthouse seen from the pavement at the foot of the flight, photographed from a crouch at half a metre above the ground so the treads climb away and fill the lower two thirds of the frame with the plain stone facade closing the top, the stone still dark and wet from rain that stopped a few minutes ago with standing water lying in the worn hollows and holding the flat grey sky, nothing cut into the stone anywhere and no plate, no inscription and no lettering of any kind, no interior, no room, no furniture and no domestic detail whatever in the frame, the steps completely empty of people, a wet iron handrail running up the right side [STYLE] Avoid: [NEG]
```

**`M244.png`** — retires `M079`
```
A single loose page of a trial transcript lying at a shallow angle on a plain dark office desk under a metal desk lamp, photographed from fifty centimetres so the page fills the frame corner to corner, the typed matter rendered as continuous smooth horizontal bands of even grey tone with absolutely no letterforms, no word gaps, no ascenders, no descenders and no punctuation anywhere so that the lines read as ruled grey ribbons and never as characters, one paragraph block marked down its left margin by a hard vertical pencil line drawn firmly enough to dent and shine the paper fibre, the lamp raking from the right so the dent catches a single edge of light, the rest of the desk falling away to darkness and nobody in the room [STYLE] Avoid: [NEG]
```

**`M245.png`** — retires `M094`
```
A single tall bound volume drawn half out of a long run of identical bound volumes on a dark wooden library shelf, photographed square on from eighty centimetres at the shelf's own height so the run of spines fills the frame edge to edge, every spine plain leather and cloth with no lettering, no gilt, no label and no numbering anywhere on any of them, the dark empty gap beside the drawn volume the only interruption in the run, a low reading lamp grazing from the right so each spine carries its own vertical edge of light, no kitchen, no window, no curtain, no domestic furniture and no person anywhere in the frame [STYLE] Avoid: [NEG]
```

**`M246.png`** — retires `M156` (must rhyme with M155; framing re-stated in full per §1.3)
```
Two identical blank buff ledger cards lying on a plain dark wooden office desk with their long edges overlapping by a finger's width so one card rides on top of the other, photographed from directly overhead dead square with the lens parallel to the desk from seventy centimetres so the pair sits in the middle of the frame with an even margin of bare desk all round, both cards carrying nothing but faint printed ruling with no writing, no figures and no marks of any kind in any column, one flat lamp from the left laying a single narrow shadow under the raised card's edge so the overlap is unmistakable, no formica, no kitchen, no domestic setting and no person anywhere in the picture [STYLE] Avoid: [NEG]
```

**`M247.png`** — retires `M159`
```
A wire office basket heaped with folded blank paper slips standing on the sill of a plain sash window in a low-rise municipal office at dusk, photographed from ninety centimetres at the basket's own height so the heap fills the left of the frame and the window the right, every slip's printing reduced to an even featureless grey with no character resolving anywhere, the last flat daylight coming in almost level across the top of the heap so only the uppermost folds catch it while the mass beneath goes to shadow, through the window nothing but low two-storey rooftops, telephone wires and bare trees against an overcast sky with no tower block, no high-rise, no city skyline and no distant spire anywhere in it, the office behind the camera unlit and empty [STYLE] Avoid: [NEG]
```

**`M248.png`** — retires `M168` (the dark twin of M167; framing re-stated in full per §1.3)
```
A single closed office door with a frosted glass upper panel at the end of a long municipal corridor of worn linoleum and plain painted plaster, photographed from the far dark end of the corridor at head height so the walls recede and the door sits small and centred at the vanishing point, nothing at all lit behind the frosted glass so the panel is a flat dead grey rectangle with no glow, no warmth and no shape behind it, no name plate and nothing lettered on the door or on the wall beside it, one weak ceiling fitting halfway down lighting only the floor near the camera, no second door beside it, no kitchen, no domestic interior, no window and no person anywhere in the frame [STYLE] Avoid: [NEG]
```

**`M249.png`** — retires `M172` (must rhyme with M171; framing re-stated in full per §1.3)
```
A modest street of single-storey painted weatherboard Memphis houses photographed from the centre of the road at standing height looking straight down the row, at full night an hour after dusk, a porch light burning above every doorway along both sides except one house squarely in the middle of the frame which stands completely unlit with every window black, the sky above the roofline a deep even blue-black with no sun and no colour left in it, the road surface holding a faint sheen from the porch lights, no figure anywhere on the street, on any porch or at any window, no car moving and nothing in the frame but the one gap in the line of lights [STYLE] Avoid: [NEG]
```

**`M250.png`** — retires `M181`
```
A single blank paper slip lifted between a thumb and forefinger from the top of a tall square stack of identical blank slips on a plain office desk, photographed from the desk's own level from fifty centimetres so the stack fills the lower half of the frame and the lifted slip sits just clear above it, caught at the instant the slip leaves the pile while the rest of the stack stays perfectly square, every slip in the frame plain unmarked paper carrying faint printed ruling and nothing else with no photograph, no picture, no image, no halftone, no portrait, no writing and no figures on any of them, one desk lamp from the left so the lifted slip throws a hard shadow back down onto the stack, only the one hand in the frame cropped at the wrist and no face anywhere [STYLE] Avoid: [NEG]
```

**`M251.png`** — retires `M191` (must rhyme with M020 / M023 / M209; framing re-stated per §1.3)
```
Two identical windowed envelopes lying overlapped on a pale worn formica counter top, photographed from directly overhead dead square from seventy centimetres so the pair fills the centre of the frame with an even margin of counter all round, both envelopes exactly the same size, the same shape and the same fold with a clear rectangular address window cut in each and nothing at all visible inside either window and no printing resolving anywhere on either of them, the upper envelope slit open along its top edge with its flap standing slightly proud while the lower one remains sealed, the last flat daylight from a window to the left casting one shared soft shadow to the right, nobody in the room [STYLE] Avoid: [NEG]
```

**`M252.png`** — retires `M210` (body cut only; THUMB-03 was never selected — see §2)
```
A black bakelite wall telephone handset hanging off its cradle on its coiled cord in an otherwise dark 1970s kitchen, photographed square on from one and a half metres with the handset dead centre and filling more than half the frame height, one hard directional light from the right side only picking the coiled cord out as a single continuous bright line running down the middle of the picture against a wall that falls away to near black on both sides, the handset catching a hard specular edge along its length so it separates cleanly from the ground, the entire upper third of the frame an empty unlit flat dark wall with nothing in it at all and no shelf, no cabinet, no window, no doorway and no second room, no lit kitchen anywhere in the frame, the cord's last swing already stopped and nobody in the picture [STYLE] Avoid: [NEG]
```

---

## 4. Route and commands

### Why local SDXL

`.claude/rules/19-ship-gate.md`: long-form images are **Codex by default**, with the standing owner
exception (2026-07-05) permitting commercial-safe local generation for exactly two cases — fixing a
Codex image, or the emergency addition of a missing one. These are fixes to Codex plates pulled from
a finished master. The owner's rule for tonight is **≤30 → local SDXL, >30 → a Codex file**; this
batch is **16**, so: local SDXL. Bare SDXL is not permitted; FLUX.1-dev is not permitted in a
deliverable at all.

### `gen_max.ps1`, not `sd35_gen.py` — the same reason as EP65 R043

`C:\Users\aab15\ComfyUI\sd35_gen.py` **has no negative-prompt argument**. Its CLI is positional
(`prompt, out, seed, W, H, steps, cfg`) and the negative is a hardcoded module constant. This
episode's `[NEG]` cannot be passed through it — and `[NEG]` is the only thing suppressing faces,
text, uniforms and courtroom furniture. Generating the fix for a likeness failure with a tool that
cannot carry the likeness guardrail is not a trade worth making.
`C:\Users\aab15\stable-diffusion-webui\gen_max.ps1` takes `-Neg` and is equally commercial-safe
(JuggernautXL Ragnarok / RealVisXL V5.0 full) through the tuned path the directive requires.

### Do not run this while the render is live

A Remotion render owns the 4090 tonight. Precedent in this repo:
`scripts/upscale_hinders_4k_lanczos_v001.py` exists because a live render left ~570 MB free VRAM and
R-ESRGAN would have OOM'd. **Neither step below runs until the GPU is free.** If ComfyUI is up, shut
it down first — the directive forbids both fully loaded at once (or free A1111 with
`Invoke-RestMethod -Method Post http://127.0.0.1:7860/sdapi/v1/unload-checkpoint`).

### Step 1 — generate

Start A1111 with `& ".\venv\Scripts\python.exe" launch.py --api --no-half-vae --xformers` (the
`.bat` does not work). Then, per plate — `-Prompt` is the prompt body from §3 **with `[STYLE]`
expanded verbatim from §2 of the brief and `Avoid: [NEG]` dropped**, `-Neg` is the §2 `[NEG]` block
verbatim (the post-2026-08-05 one, with the face words):

```powershell
& "C:\Users\aab15\stable-diffusion-webui\gen_max.ps1" `
  -Prompt "<body from §3>, cinematic still, muted natural colour, flat humid Tennessee light with haze standing in it, low contrast, low-key but never crushed: shadows keep their detail and the frame reads clearly on a phone screen, soft falloff toward the edges, shallow depth of field, restrained documentary framing with a point of view, Memphis in the middle 1970s - a modest single-storey frame house with painted weatherboard, worn linoleum, formica, enamel, bakelite, an ordinary working household, municipal offices of the same decade in steel and wood, nothing staged for advertising, ultra-detailed, photoreal, 4K, 16:9, fine film grain, no text, no lettering, no numerals, no watermark, no logo, no signage" `
  -Neg "<the [NEG] block from §2 of EP64_memphis_CODEX_BATCH_A.v001.md, verbatim>" `
  -Orient video -Model realvis -NoADetailer -Seed 2640237 `
  -Out "H:\pd-media\assets\ai\memphis\M237_base.png"
```

- `-Orient video` is the only 16:9 option (1344×768 base, ×`hr_scale 2` → 2688×1536).
- `-NoADetailer` on every plate in this batch: **none of them contains a person**, and a face
  detector given no faces is an invitation. (M238 contains two figures from behind with no face —
  still `-NoADetailer`, for exactly that reason.)
- `-Model realvis` (RealVisXL V5.0 full); `juggernaut` is the equally licensed fallback.
- **Seeds are `264` + the plate number** (M237 → `2640237`) — arbitrary, but recorded, so every
  plate is reproducible.

### Step 2 — upscale to 3840×2160

`gen_max.ps1` tops out at 2688×1536. Use the A1111 `extra-single-image` endpoint with
`upscaler_1 = "R-ESRGAN 4x+"`, `resize_mode 1`, `upscaling_resize_w 3840`,
`upscaling_resize_h 2160`, `upscaling_crop true`, writing
`H:\pd-media\assets\ai\memphis\M237.png`. Verify with PIL that the result is exactly `(3840, 2160)`
before anything else — that is the measured size of every plate in this set.

### Step 3 — where the file has to be

The master was rendered with `--public-dir remotion/public_ep64`. Copy the one new file in; do
**not** re-run `build_render_public_dir.py`, which does `rm -rf` first.

```bash
cp "H:/pd-media/assets/ai/memphis/M237.png" remotion/public/memphis/img/M237.png
cp remotion/public/memphis/img/M237.png     remotion/public_ep64/memphis/img/M237.png
```

### Step 4 — visual QC, one plate at a time, at full resolution

1. No readable text, numeral, sign, plate, seal or logo anywhere.
2. No face, no profile, no hand where none was ordered, no reflection of one.
3. **Four-corner sweep at native resolution for a generator watermark** — this is how M159 was
   caught and it is invisible on a contact sheet.
4. Nothing that identifies a real building.
5. Reads on a phone **after** the cut's treatment. M237 and M238 are `duotone` with `lift` 1.484 /
   1.282 — simulate the treatment; do not judge the raw PNG.
6. Not a catalogue photograph: somebody's eye height, not a real-estate frame.
7. It still means what its sentence means when it is five seconds long and silent.

Then record the verdict in `runs/qc/memphis_plate_verdicts.v001.json` and the hash beside it.

---

## 5. The re-book path — and it does not need this batch

Per `config/ship_policy.v001.json` → `no_rebuild_rule`, ladder step 3: **splice only the affected
range.** A full re-render is 1h35–2h10; a splice of one cut is ~10–15 min.

Adjudication of all 65 outstanding plates is in
`episodes/PD-2026-064-memphis/09_package/plate_adjudication.v001.json`. Result: **one blocking
finding**, `M117` at `cut-0239` (`real_person_likeness`).

**Precondition, already measured and already true:**

```
$ sha256sum remotion/src/data/memphis_film.json \
            episodes/PD-2026-064-memphis/08_edit/memphis_film.rendered.json
b1b70acf8d5dea5bf11d629f26f7f421b2f9b083cc41e851175ef794a336c9be  (both)
```

The film json still describes the shipped master, so the splice is available. Prove it before
writing anything (`--verify-only`, exit 0 = this json reproduces this master; exit 3 = it does not).

```bash
py -3.11 scripts/pd_splice_cuts.py --slug memphis --comp Ep64Memphis \
  --master episodes/PD-2026-064-memphis/08_edit/memphis_final_bgm.v002.mp4 \
  --out    episodes/PD-2026-064-memphis/08_edit/memphis_final_bgm.v003.mp4 \
  --public-dir remotion/public_ep64 \
  --replace cut-0239=memphis/img/M227.png \
  --replace cut-0046=memphis/img/M234.png \
  --verify 2 --dry-run          # then without --dry-run, with --receipt
```

Using the **existing** M227 and M234 needs no GPU at all. It makes each of them appear twice in the
film (M227 at 21:17 and 25:37, M234 at 04:17 and 26:26) — an `asset_reuse` deviation, which is
advisory and gets recorded, not escalated. If the duplication is unacceptable, generate `M237` and
`M238` from §3 first and put those in `--replace` instead. **That is the entire decision this batch
exists to serve.**

### ⚠ One thing the splice cannot reach: the hook

`M202` is in the film **twice** — `cut-0046`, and **`hook[4]`, on screen at master 00:04.0–00:05.0**,
inside the eight-second hook. `pd_splice_cuts.py` only edits `film["cuts"]`; its `--replace` takes a
cut id, and its own guard aborts if the edit touches anything outside the named cuts
(`pd_splice_cuts.py:818`). It computes a fixed pre-roll of `hookSeconds + OPENING_SEC` frames and
treats everything before it as unreachable. **The hook instance of M202 cannot be spliced.**

Since M202 is adjudicated **advisory** — I opened both frames and neither figure shows a face,
profile or reflection, so there is no identifiability — this does not stop the ship. The honest
record is: the body cut is fixed because it is nearly free inside a splice run that has to happen
anyway; the one-second hook instance is recorded as a deviation and fixed in the next revision,
because reaching it means either a tool change or a two-hour re-render for one second of an
ambiguous read. If a reviewer disagrees and calls the figure a child, that inverts: `child` is a
**blocking** term in `ship_policy.forbidden_subject_terms`, the defect becomes distributed and
un-spliceable, and ladder step 4 (full re-render, with a written reason) applies.

### After the splice — the sha changes, so everything bound to it is void

```bash
# 1. re-snapshot the film json beside the master (the splice tool does NOT do this)
cd episodes/PD-2026-064-memphis/08_edit && \
  cp memphis_film.rendered.json memphis_film.rendered.json.bak_pre_splice_$(date +%Y%m%d_%H%M%S) && \
  cp ../../../remotion/src/data/memphis_film.json memphis_film.rendered.json

# 2. fresh acceptance receipt on the NEW bytes (v001/v002 exist -> v003)
py -3.11 scripts/check_final_acceptance.py memphis \
  --render episodes/PD-2026-064-memphis/08_edit/memphis_final_bgm.v003.mp4 --emit-receipt

# 3. new final_delivery revision -> v003, pinning the new sha/bytes/duration
py -3.11 scripts/write_final_delivery.py --slug memphis \
  --render episodes/PD-2026-064-memphis/08_edit/memphis_final_bgm.v003.mp4

# 4. re-extract and GENUINELY re-read the shipped frames
py -3.11 scripts/check_shipped_frames.py --slug memphis --which-master   # confirm it picks v003
py -3.11 scripts/check_shipped_frames.py --slug memphis
```

**A splice changes the video stream.** `check_shipped_frames`'s review re-binds only while the video
stream md5 is unchanged, and the master's is
`13520cf9628443309276955985d445d3` (`blocking_findings.v001.json`). After the splice that value is
different, so **the binding written earlier tonight is void and every sheet must be read again — not
re-affirmed, read.** An unread sheet is not a pass, and the tool exits 1 if any produced sheet was
never read. Archive the old review before rewriting the fixed-name file:

```bash
cp runs/qc/memphis_shipped_frames_review.v001.json \
   runs/qc/memphis_shipped_frames_review.v001.json.bak_$(date +%Y%m%d_%H%M%S)
```

Then whole-file gates (loudness, `animation_density`, `motion_energy`, `footage_diversity`) on v003 —
a scan, not a render — and finally:

```bash
# point CONFIG['memphis']['video'] at the new master via scripts/pd_edit.py, then
py -3.11 scripts/upload_schedule_case_v001.py --ep memphis --replaces=-OYk7ji78as --dry-run
```

Note the leading hyphen: `--replaces=-OYk7ji78as`, not `--replaces -OYk7ji78as`, or argparse reads it
as a flag. The slot is `2026-08-18T03:00:00Z` (12:00 JST) and is currently unheld.

### Housekeeping that is not optional

- **Retire the sixteen** so no future build can pick them up:
  `mkdir -p remotion/public/memphis/img_rejected` and move them there — the brief's own instruction
  is *カットに使わない（削除はしない）*, do not use, do not delete. **`M159` above all**: its plate
  carries a generator watermark, and although I verified it is cropped out of every frame of its cut
  in the shipped master, the file itself is a licence hazard for any future reuse.
- `check_spec_satisfied` is unaffected: `mandatory_stills` already names M220–M234 and names none of
  the sixteen.
- Record every advisory finding in `09_package/release_deviations.v001.json` with its measured
  value — 64 of the 65 adjudicated plates, the `asset_reuse` duplication, and the M202 hook
  instance. Nothing is silently waived.

---

## 6. The structural hole, named once

`scripts/check_plate_verdicts.py` is imported by `check_episode_inputs.py` and
`preflight_render_gate.py` — both **input-stage** gates. It is referenced **zero** times in
`check_final_acceptance.py` and zero times in `upload_schedule_case_v001.py`. Once a film is
rendered, nothing re-asks the plate question, which is how a master built from sixteen retired
plates reached a scheduled slot with every gate green.

But note what this episode actually shows, which is worse and more specific: **the verdicts were
acted on.** Sixteen replacements were ordered, generated, QC'd and written into the spec. The only
step that never happened was re-pointing the film json — and there is no check anywhere that asks
*"does any cut still use a plate this episode's own brief marked 廃止?"* That check is one pass over
`film["cuts"]` against the retirement list, it would have failed loudly on 2026-08-09, and it does
not exist.
