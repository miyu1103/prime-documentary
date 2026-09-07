# EP74 · ITAEWON — IMAGE ORDER (BATCH B) v001 — SEVEN RE-ORDERS

**Six plates and one thumbnail background, re-ordered.** `EP74_itaewon_CODEX_BATCH_A.v001.md`
remains in force in full: §0 (size and generator), §1 (the bars), §2 (the two light states), §3
(`[STYLE]` and `[NEG]`) and §5 (delivery) are unchanged and are **not restated except for the
`[NEG]`, which is repeated below because a negative block that lives in another document does not
protect anything ordered in this one.**

---

## 0. Why these seven, and what the review actually found

All 120 batch-A plates were viewed on 2026-08-21 on ten labelled contact sheets, plus two at full
3840×2160. **Every blocking bar was clean across all 120** — no body, no identifiable face, no
legible glyph (the eight document plates are genuinely blank), no Japanese, Chinese or Western
signage. Nothing here is about a bar.

Six plates were rejected because **they do not show what was ordered**, and the pattern is the whole
lesson of batch A:

> **Orders naming a SCENE TYPE came back right almost without exception** — a corridor, a row of
> empty chairs, a blank manila folder, a line of turnstiles, barrier tape, an unmarked whistle, a
> date stamp with no legible numerals, flowers with blank cards.
>
> **Orders naming a SPECIFIC OBJECT came back as another good-looking generic alley** — this
> hotel's rear elevation, that terrace, the kerb where the alley meets the road, the alley floor.

Section B of batch A was the entire Hamilton Hotel terrace group, `I025`–`I028`, and **not one of
its four plates contains a terrace.** That leaves a load-bearing ACT_1 beat with no picture:
seventeen point two square metres, *"made the narrow path even narrower"*, and a fine issued the
year before.

**The fix in this batch is structural, not cosmetic.** In batch A the subject sat in a table cell and
the camera position lived in the style block, where it was advisory. Here **the object and the
camera are the first two clauses of the prompt body**, before any atmosphere, and each plate carries
a one-line `MUST CONTAIN` that a reviewer can check without reading the order.

The six rejected plates are retired to `remotion/public/itaewon/img_rejected_v001/`. They are not
deleted, and they are out of the pool the builder draws from — `check_episode_inputs` caught them
sitting in it, which is exactly the EP64 memphis failure.

---

## 1. `[NEG]` — carried in full

Append to every prompt below. Identical to batch A §3.

> text, lettering, readable text, legible text, numerals, numbers, digits, house numbers, handwriting, cursive, signature, legible signature, seals, seal, emblems, emblem, logos, logo, badge, insignia, wordmarks, name plates, licence plate, registration plate, identifiable person, recognisable person, recognizable person, likeness of a real individual, portrait of a named person, celebrity, public figure, deepfake, body, corpse, dead body, fallen person, person on the ground, person being crushed, crush, pile of people, trampled, injured person, blood, cpr, chest compression, resuscitation, defibrillator, stretcher, gurney, paramedic, ambulance interior, hospital, emergency room, morgue, autopsy, coffin, funeral, grave, mourner, crying, grieving, rescue, search and rescue, victim portrait, portrait wall, memorial photograph, framed photograph of a person, gavel, scales of justice, lady justice, jury box, judge's bench, courtroom interior, handcuffs, firearm, prison bars, japanese signage, kana, hiragana, katakana, chinese characters as shopfront, chinese lantern, tokyo, shibuya, shanghai, hong kong, bangkok, times square, london street, european street, EU number plate, right-hand-drive traffic, american highway sign, US route shield, american flag, megacity skyline, skyscraper cluster, expressway interchange, palm trees, beach, surf, ocean, tropical, desert, cruise ship, mardi gras, carnival, parade float, confetti, music festival, concert crowd, stadium crowd, sports fans, fireworks, new year countdown, horror movie, zombie, video game, crash test, action movie explosion, golden hour, sunset glow, postcard scenery, christmas, wedding, handshake, money rain, falling banknotes, stock ticker, glossy advertising lighting, flat CGI, 3D render, cartoon, illustration, anime, oversaturated, HDR halo, watermark

`human face`, `facial features`, `eye contact` and `headshot` are deliberately absent and must not be
added. **None of the seven plates below contains a person at all**, so the question does not arise
here, but the rule is the rule.

---

## 2. The seven

Deliver as `I005.png`, `I006.png`, `I025.png`, `I026.png`, `I027.png`, `I028.png` into
`remotion/public/itaewon/img/`, and the thumbnail background as `T01_bg.png`. Long edge ≥ 3840, 16:9.
**One prompt, one image.**

### I005 — THE KERB

**MUST CONTAIN:** a granite kerbstone in close-up, filling the lower third of the frame. **If the
frame reads as "a street", it is wrong.**

> `[STYLE]` + **a worn granite kerbstone photographed in close-up from 40 cm above the road surface, the camera low and looking along the kerb so that it fills the lower third of the frame and recedes away to the left; the stone's rounded, chipped top edge and the joint between two kerb sections are the sharpest things in the picture; behind and above it, thrown far out of focus, the dark mouth of a narrow alley opening onto a main road at night; wet asphalt in the foreground catching one warm reflection; no people, no vehicles, no legible signage** + `[NEG]`

### I006 — THE ALLEY FLOOR

**MUST CONTAIN:** a cast-iron drain grate, seen from directly above. **No horizon, no sky, no
building faces, no vanishing point.**

> `[STYLE]` + **the floor of a narrow alley photographed from chest height with the camera pointing STRAIGHT DOWN, so the frame contains nothing but ground; a rectangular cast-iron drain grate slightly left of centre, a run of small square edging tiles along one side, and a darker rectangular patch where the asphalt has been cut and refilled; wet after rain, lit by a single overhead lamp out of frame; no horizon, no sky, no walls, no people** + `[NEG]`

### I025 — THE HOTEL'S REAR ELEVATION

**MUST CONTAIN:** a large multi-storey building occupying at least two thirds of the frame. **If the
frame reads as "an alley with buildings on both sides", it is wrong.**

> `[STYLE]` + **the rear elevation of a large six-storey hillside hotel, filling the right two thirds of the frame and rising out of the top of it: rendered concrete, service balconies, stacked air-conditioning condensers on wall brackets, small service windows, a fire escape stair; the camera stands in a narrow alley at its foot, at eye level, looking up and across at the building; the opposite alley wall is a dark vertical band down the left edge; night, a single service light on the building, no legible name anywhere, no people** + `[NEG]`

### I026 — THE TERRACE, IN SILHOUETTE

**MUST CONTAIN:** a flat-roofed terrace structure projecting horizontally from a building, read as a
black outline against the sky, occupying the upper half of the frame.

> `[STYLE]` + **a flat-roofed terrace structure projecting horizontally out from the flank of a large building, photographed from below at night as a hard black silhouette against a deep blue-black sky; its steel handrail, its edge beam and the diagonal support brackets under it read as a clean black outline; the terrace occupies the upper half of the frame and its underside is in complete shadow; a single distant street lamp behind it, flaring slightly at the edge; no people, no legible signage** + `[NEG]`

### I027 — THE TERRACE, FROM UNDERNEATH

**MUST CONTAIN:** the underside of a projecting structure, seen looking straight up, with its
brackets bolted into a wall. **An elevated road or a bridge is the wrong object.**

> `[STYLE]` + **the underside of a projecting terrace photographed from directly beneath it, camera pointing straight up; the frame is filled by the terrace's soffit, three steel support brackets bolted into a rendered concrete wall, a grey drainage pipe running along the wall and a line of bolt heads; past the terrace's edge, flat overcast daylight and a sliver of white sky; no people, no legible signage** + `[NEG]`

### I028 — WHERE THE TERRACE NARROWS THE PASSAGE

**MUST CONTAIN:** the same passage visibly **narrower** at the point where a structure overhangs it
than it is further up. The narrowing is the subject.

> `[STYLE]` + **a narrow sloping alley photographed square-on from its lower end, camera at eye level, looking up the slope; on the right, a terrace structure projects out from the building above and visibly overhangs the passage, so that the gap between the two walls is plainly narrower under the terrace than it is further up the alley; the far end of the alley is higher in the frame than the near end; overcast daylight, shutters down, wet ground, no people** + `[NEG]`

### T01_bg — THE THUMBNAIL BACKGROUND

**MUST CONTAIN:** the alley receding **uphill**. The far end is **higher** in the frame than the near
end. The previous plate was rejected for reading downhill, and this film's alley rises from the main
road, so a downhill frame inverts the film's geometry on its own cover.

> `[STYLE]` + **a narrow empty alley between two low buildings at night, photographed square-on from its LOWER end with the camera at chest height looking UP the slope, so that the far end of the passage sits HIGHER in the frame than the near end and the ground rises away from the viewer; both walls hard in the frame and close enough to touch, the passage visibly narrower at the near end than at the far end; wet asphalt holding the reflection of unreadable sign light; nobody in it at all; deep dark negative space across the upper third of the frame for a headline; high contrast, the two walls reading as bright edges against a black centre** + `[NEG]`

---

## 3. On delivery

1. Long edge ≥ 3840. Batch A came back at exactly 3840×2160 on all 120, so the path is proven.
2. **Check each plate against its own `MUST CONTAIN` line before anything else.** That single line is
   why this batch exists; a beautiful alley that is not the ordered object is a reject, and six of
   them cost this episode a day.
3. Then the four bars, as always: a body, a real face, a legible glyph, wrong-country signage.
4. Rebuild the contact sheets and record verdicts:

```
py -3.11 scripts/build_plate_contact_sheet.py --slug itaewon
py -3.11 scripts/check_plate_verdicts.py --slug itaewon --scaffold --reviewer "<name>"
py -3.11 scripts/check_plate_verdicts.py --slug itaewon      # must exit 0
py -3.11 scripts/check_episode_inputs.py --slug itaewon      # catches a reject left in the pool
```

**Do not delete `img_rejected_v001/`.** It is the evidence of what was rejected and why, and the
rule is that a retired artefact is retired, never removed.
