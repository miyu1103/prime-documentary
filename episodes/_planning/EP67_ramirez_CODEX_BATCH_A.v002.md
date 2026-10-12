# EP67 · TRANSUNION v. RAMIREZ — IMAGE ORDER (Codex) **v002 · the prompts**

**Episode `PD-2026-067-ramirez` · slug `ramirez` · 2026-08-11**

> **What changed from v001.** v001 named the lanes and the id ranges and contained **zero prompts** — 0 occurrences of `[STYLE]`, 0 of `Avoid: [NEG]`. It could not be pasted into anything. This revision writes the prompt bodies. **v001 is not edited and stays on disk** (invariant 6); everything it says about policy, era and the barred likenesses still binds and is restated below.

> **And the count changed: 152 prompts, not 96.** Re-derived with the builder's own solver rather than guessed — see §0.1. They are in **three tiers, and the tiers are not interchangeable**:
>
> | tier | ids | count | in `episode_spec.mandatory_stills`? |
> |---|---|---:|---|
> | **1 · declared** | `R001`–`R122` | **122** | **yes** — the film will place exactly this many still cuts |
> | **2 · headroom** | `R123`–`R146` | **24** | **no** — cover against rejections and against the script growing |
> | **3 · thumbnail** | `T001`–`T006` | **6** | **no** — a thumbnail never becomes a cut |
>
> **Declaring all 152 would fail the build.** `check_spec_satisfied.py` fails any `mandatory_stills` id that appears in no cut, and at the current script length the solver places 122 still cuts and no more. That correction had to be made late on EP65. **Do not "tidy" these three numbers into agreement.**

**Design:** `EP67_ramirez_FILM_BIBLE.v001.md` · **Front:** `EP67_ramirez_PACKAGING.v001.md` · **Facts:** `EP67_ramirez_FACTS_LEDGER.v001.md` · **Script:** `EP67_ramirez_script.en.v001.md`.

**Paste files:** `episodes/_planning/EP67_ramirez_CODEX_PASTE_A/` — one file per group, generated from the same Python source as this document (`scripts/build_ep67_ramirez_image_order.py`), so the prompt bodies cannot drift apart.

---

## 0.1 How many plates, derived rather than chosen

`scripts/build_case_film_generic.py` decides the cut mix. Its constants: `MAX_STILL_REUSE = 1` (**a still is used once**, so the still-cut count *is* the distinct-still count), `MIN_VIDEO_SHARE = 0.68`, `_CAP_FACTORY = 1`. The episode declares `target_cut_sec` **3.8** and `distinct_video_assets` **222** (v002; 260 retired). The builder reads the declared cut length at line 406 and scales the runtime it hands the solver by `TARGET_CUT_SEC / 3.8`, so 3.8 is what the real build uses — running the solver at the module default 4.6 gives a different and wrong answer.

```
py -3.11 -c "import sys;sys.path.insert(0,'scripts');import build_case_film_generic as B;B.TARGET_CUT_SEC=3.8;print(B.solve_totals(60*5000/159.5,260,0,400))"

across the DECLARED word band script_words [4400,5000] x the measured pace band 159.5-169.7
still pool left unbounded (400) so the ceiling shows itself:

 words    wpm   narr s |  cuts  video  STILL
  4400  169.7   1555.7 |   382    260    122
  4400  159.5   1655.2 |   382    260    122
  4682  169.7   1655.4 |   382    260    122
  4682  159.5   1761.3 |   382    260    122
  5000  169.7   1767.8 |   382    260    122
  5000  159.5   1880.9 |   382    260    122
```

**122 is flat across the whole declared band, and that is not a coincidence.** The binding constraint is not runtime — it is `still_max_for_share = floor(video x (1 - 0.68) / 0.68)`, and `video` is capped at the declared 260 distinct video assets. `floor(260 x 0.32 / 0.68)` = **122**. Lengthening the script does not raise the still requirement; only raising `distinct_video_assets` does.

**Rejection allowance.** EP66's batch C is the only measured rate this channel has: 191 ordered, **11 REJECT (5.8%)** and 10 further FLAG (**11.0% combined**).

```
  122 / (1 - 0.058) = 130    hard rejects only
  122 / (1 - 0.110) = 138    rejects + flags
```

**Ordered: 146 plates.** 138 from the reject-and-flag allowance, plus 8 more, because the still ceiling moves with `distinct_video_assets`: at a video pool of 300 the ceiling is `floor(300 x 0.32 / 0.68)` = **141**, and archive supply was measured at 5,537 usable clips, so the pool may well be raised at staging. 146 covers a video pool up to about 310. **Declared: 122.** The difference is the whole point — see the tier table above.

> **`docs/PD_CANON.md` rule 25 applies: the band is a prediction, the delivered VO is the measurement.** `episode_spec.v001.json` carries a TODO saying `mandatory_stills` is re-derived from the measured narration master before assembly. If the delivered master lands outside 1555.7-1880.9 s, or if `distinct_video_assets` is changed, **re-run the solver and re-declare** — do not carry 122 forward on faith.

**Where the plates went, and why there.** Narration words per section, counted from the script with citation comments and stage directions excluded:

| section | words | share | dedicated plates in v001 | added here |
|---|---:|---:|---|---|
| HOOK + OP | 196 | 4.6% | borrows from A1 / C | — |
| ACT_1 | 529 | 12.5% | R001–R031, R073–R082 | R127–R130 (headroom) |
| ACT_2 | 985 | **23.2%** | R054–R072, R083–R084 | **+8 R097–R104**, +8 R131–R138 (headroom) |
| ACT_3 | 827 | 19.5% | R042–R053 shared, R085–R089 | **+8 R105–R112**, +5 R139–R143 (headroom) |
| ACT_4 | 676 | **15.9%** | R090, R091 + a shared court lane | **+10 R113–R122 with ACT_5**, +4 R123–R126 (headroom) |
| ACT_5 | 830 | **19.6%** | R092–R094 + the same shared court lane | **+10 R113–R122 with ACT_4**, +3 R144–R146 (headroom) |
| ENDING | 197 | 4.6% | R017, R041, R095, R096 | R145, R146 (headroom) |

ACT_4 and ACT_5 together are **35.5% of the narration**, and in v001 they had four dedicated plates each plus a twelve-plate courthouse lane they were expected to share with ACT_3 — which `MAX_STILL_REUSE = 1` makes impossible: twelve plates across three acts is four each, full stop. That is why lane G exists and why it is ten plates rather than an even spread. ACT_2 is the longest act and the one the bible names as most likely to fall into kamishibai, so it takes eight. ACT_3 takes the eight the script's own ACT_3 header already calls by name (`R105–R112`).

**Thumbnails are their own lane and add nothing to `mandatory_stills`.** `T001`–`T006` are two candidates for each of PACKAGING §2's three variants. They are built to a **thumbnail-only `[TSTYLE]`** (§2) because the canonical `[STYLE]` asks for low contrast — which is correct for a film frame and is exactly why EP65's four candidates came back dull and had to be re-ordered. **`[NEG]` is not deviated for them.**

---

## 1. Who generates these, and the one thing that is barred

- **Long-form images are Codex by default** (`.claude/rules/19-ship-gate.md` line 10). Every plate here is a Codex commission. **Do not start a local model to fill this order.**
- Local generation is an exception, not a lane: **SD3.5 Large** (`sd35_gen.py`) or **SDXL** (`gen_max.ps1`) only to repair a Codex plate or fill an emergency gap. **Bare SDXL is not allowed. FLUX.1-dev is not allowed in any deliverable.**
- **Long edge ≥ 3840, PNG, 16:9.** Every plate is an illustration, never evidence (CLAUDE invariant 11).

**People are required and faces are welcome** (owner decision 2026-07-04). What is barred absolutely is the **likeness of a real, identifiable individual**, and in this episode that has five names attached:

| Never depict as a person | Why |
|---|---|
| **Sergio L. Ramirez** | a living private individual (⛔-07) |
| **his wife, his father-in-law** | same; the record gives their presence and nothing else (SR-01) |
| **the Nissan salesman or any dealership employee** | never named, never a party, never heard (⛔-08) |
| **the two SDNs who "purportedly matched" him** | the record does not print their names (⛔-09) |
| **any Justice** | opinions appear as attributed typography, never as a portrait |

Nine plates in lane C carry a resolvable face. **Every one of them is written as INVENTED and COMPLETELY FICTIONAL in the prompt body itself**, and none is captioned, cut or narrated as anyone in this record.

**Four things are never produced as an image at all, in any style** (⛔-13): a TransUnion credit report, the OFAC Letter, an OFAC / SDN list entry, any court record or filing. Their *words* may be set as Remotion typography — card, not scan.

### 1.1 No readable anything, and it is ordered in the POSITIVE prompt

This episode is dense with the hazard: credit reports, letters, a dealership desk, court buildings, a passport. **A generator asked for "a credit report" writes words on it.** EP66's `L146` proved a `[NEG]` ban alone does not hold — the wordmark came back twice after being banned twice. So every document in this order is ordered as a **shape**, in the positive prompt, using one of two fixed clauses:

- **grey ruled blocks** — *The paper carries no writing of any kind, and this is what is on it instead: EVENLY SPACED FLAT GREY HORIZONTAL BARS of one uniform width and one uniform weight, laid in parallel like ruled bands of tone, each bar a solid unbroken block of soft grey with straight ends and no letter shapes, no word shapes, no gaps between words and no broken or ragged edge anywhere along it, so the sheet reads as printed matter purely by its rhythm of grey and white and carries not one readable character*
- **genuinely blank** — *The sheet is completely blank: an unbroken field of off-white paper with no print, no ruling, no letterform, no number and no mark of any kind on it*

The same applies to brands (**no Nissan badge, no dealership signage, no TransUnion mark, no Treasury seal** — the car is *a mid-size saloon*, the lot is *a lot*), to screens (*The screen is never legible: it is a single soft bloom of even light with no icons, no windows, no rows, no cursor and nothing that could be read as a document*), and to hands.

### 1.2 Hands

EP66's `L236` failed twice on a raised hand with fused fingers. The fix that worked was to **rest the hand flat on a surface**, and that geometry is reused verbatim wherever hands are the subject:

> THE HAND IS AT REST FLAT ON THE SURFACE, not raised and not held in the air, the palm laid down in full contact with it and the wrist straight, THE FOUR FINGERS LYING SIDE BY SIDE AND SEPARATE with a visible line of shadow between each pair and one nail showing on each, and the thumb clearly apart from the fingers along the near side

`R087` deviates from v001's wording for this reason: v001 said *"hands folded"*, which is interlocked fingers — the exact failure. It is ordered here as **both hands flat and separate on his own knees**, and `interlocked fingers` is added to that plate's `[NEG]`.

### 1.3 Era

`era_setting` is **Dublin, CALIFORNIA**, 2011–2026. Nothing may date the shot outside it and nothing may relocate it: an Irish establishing shot pulled on the word *dublin* is the mistake the field exists to make visible. Every lane's `[NEG]` carries the European-streetscape block.

---

## 2. Style blocks (★ expand before generating)

**`[STYLE]`** — appended to every plate in this order, exactly as written:

> cinematic still, photographic, restrained documentary framing, muted natural colour, low contrast but never crushed: shadows keep their detail and the frame reads clearly on a phone screen, soft falloff toward the edges, shallow depth of field, ordinary suburban and civic California in the United States between 2011 and 2026, plain worn everyday surfaces, nothing staged for advertising, nothing in shot that would date the picture outside those years, ultra-detailed, photoreal, 4K, 16:9, fine film grain, no text, no lettering, no numerals, no watermark, no logo, no signage

**`[NEG]`** — after `Avoid:`, exactly as written. **This block is byte-identical to EP66 batch D's** and was lifted out of `EP66_openfields_CODEX_BATCH_D.v001.md` by the generator rather than retyped:

> text, lettering, numerals, digits, house numbers, handwriting, cursive writing, legible signature, seals, emblems, logos, insignia, badge, name plates, readable words on a sign, recognisable person, identifiable person, likeness of a real individual, portrait of a named person, celebrity, public figure, deepfake, police officer, sheriff, trooper, uniform, patrol car, flashing lights, handcuffs, rifle, shotgun, firearm, holster, dead animal, carcass, blood, taxidermy, mounted antlers, courtroom interior, gavel, judge's bench, prison bars, razor wire, scales of justice, hourglass, a handshake, night vision green, thermal false colour, crosshairs, CCTV monitor grid, drone shot, aerial view from above the treetops, golden hour, sunset glow, postcard scenery, autumn colour explosion, Christmas, tropical, modern smartphones, laptops, glossy advertising lighting, flat CGI, cartoon, illustration, oversaturated, HDR halo

> ### ★ Per-plate `[NEG]` additions ★
> Every plate reads `Avoid: [NEG], …`. That means: **expand the canonical block above in full, then append the extra words.** **Do not delete one word of the canonical block.** Only additions ever happen.
>
> ### ★ The `[NEG]` does not forbid people ★
> What it forbids is **`recognisable person, identifiable person, likeness of a real individual, portrait of a named person, celebrity, public figure, deepfake`** — resembling a real someone. EP66's batch A wrote `human face, facial features, eyes …`, stopped people appearing at all, and **cost 191 plates a rebuild. Those three tokens are absent here and must stay absent.**

**`[HSTYLE]`** — prepended (before the body) on lane C only, R073–R096, exactly as `EP67_ramirez_CODEX_BATCH_A.v001.md` §3 wrote it:

> photographic, 35mm, natural light, real adults, ordinary clothing, ordinary bodies, believable American setting, candid framing, no styling, no beauty retouching, no model look, no stock-photo smiles, faces neutral and unremarkable, nobody looking at the lens

**`[TSTYLE]`** — **thumbnail lane only**, T001–T006. Replaces `[STYLE]` on those six prompts and nowhere else. The `[NEG]` is unchanged:

> editorial photographic still made to be a video thumbnail, ONE HARD DIRECTIONAL KEY LIGHT from the side, HIGH CONTRAST AND BRIGHT OVERALL EXPOSURE, the subject clearly brighter than everything behind it and cleanly separated from it, shadow only where it defines an edge and never filling the frame, THE ENTIRE UPPER 40 PERCENT OF THE FRAME IS ONE UNBROKEN UNIFORM FIELD - plain wall, plain sky or plain out-of-focus darkness, with no object, no edge, no horizon and no detail crossing it anywhere - and the whole subject sits inside the lower 60 percent with the bottom third the brightest part of the picture, ordinary suburban and civic California in the United States between 2011 and 2026, ultra-detailed, photoreal, 4K, 16:9, no text, no lettering, no numerals, no watermark, no logo, no signage

---

## 3. Naming and delivery

- **Names are exactly `R001.png` … `R146.png` and `T001.png` … `T006.png`.** `check_spec_satisfied.py` reads `mandatory_stills` by basename; a plate called `ramirez_drawer_final.png` does not exist as far as the contract is concerned. **No `_v2`, no `_02`, no `_A`.**
- **One prompt = one image.** Do not run a prompt twice and keep the better one.
- **Do not put any `forbidden_subjects` word in a filename** — the gate matches them word-wise against source filenames, so `R044_gavel_door.png` fails the build even though the picture is a door.
- Deliver to `H:\pd-media\assets\ai\ramirez\`, long edge ≥ 3840, 16:9, PNG.
- Depth maps for the plates that take 2.5D motion go to `remotion/public/ramirez/img/<name>_depth.png` — **a still that is only Ken Burns-zoomed is rejected as kamishibai.**
- After delivery: build a **labelled contact sheet and look at it**, then `py -3.11 scripts/check_episode_inputs.py --slug ramirez`.

---

## 4. THE PROMPTS — tier 1, declared, 122 plates (R001–R122)

Each plate gives the line of narration it lands on and the ledger row behind it. **A plate with no beat is not commissioned** — that rule is why there are no filler plates in this order.

### A1 · the dealership counter — R001–R017 (17 plates)

*HOOK / OP / ACT_1 — bright Californian daylight, glass, chrome, asphalt*

#### `R001.png`

**Lands on:** "Dublin, California. February 27th, 2011." · **ledger** SR-01

- `R001.png`
A wide of a car showroom interior seen from the customer's side of the floor at eye height: a polished pale floor running away to a full-height glass wall, flat Californian midday coming through it, two plain mid-size saloon cars parked at an angle on the floor with nobody anywhere in the frame. No vehicle anywhere in this frame carries a mark of any kind: no badge, no emblem, no oval on the grille, no wordmark, no nameplate, no model lettering, no dealer sticker and no plate of any kind on any part of any of them, front or rear, and there is no dealership signage, no banner, no price board and no poster anywhere on the walls or the glass. Every surface is bare painted plasterboard, glass or floor [STYLE] Avoid: [NEG], licence plate, registration plate, number plate, badge on the grille, oval emblem, manufacturer wordmark, chrome nameplate, dealership signage, price sticker, window sticker, European streetscape, Irish town, Georgian doorway, EU number plate, foreign-language signage, cobbled lane, thatched roof, tram, showroom banner, wall poster, price board, balloons, sales pennant

**Save as:** `H:\pd-media\assets\ai\ramirez\R001.png`

**`[NEG]` addition:** append `, licence plate, registration plate, number plate, badge on the grille, oval emblem, manufacturer wordmark, chrome nameplate, dealership signage, price sticker, window sticker, European streetscape, Irish town, Georgian doorway, EU number plate, foreign-language signage, cobbled lane, thatched roof, tram, showroom banner, wall poster, price board, balloons, sales pennant` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R002.png`

**Lands on:** "The salesman runs a credit check, and says Nissan will not sell him the car." · **ledger** SR-02 / SR-03

- `R002.png`
A sales desk seen from just behind and above a customer's shoulder, the shoulder a soft dark mass at the very bottom edge of the frame and out of focus: the desk edge crosses the middle of the frame, a slim computer monitor stands at the far side TURNED AWAY so only its plain back panel and a spill of light round its edge are visible. The screen is never legible: it is a single soft bloom of even light with no icons, no windows, no rows, no cursor and nothing that could be read as a document. A keyboard lies flat in front of it and a single set of car keys sits on the far corner of the desk just out of reach. The desk top is bare wood-effect laminate with no paper on it. Bright showroom daylight from the left [STYLE] Avoid: [NEG], readable screen, spreadsheet on a monitor, web page, icons, cursor, user interface, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, licence plate, registration plate, number plate, badge on the grille, oval emblem, manufacturer wordmark, chrome nameplate, dealership signage, price sticker, window sticker, face, head, second person in frame

**Save as:** `H:\pd-media\assets\ai\ramirez\R002.png`

**`[NEG]` addition:** append `, readable screen, spreadsheet on a monitor, web page, icons, cursor, user interface, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, licence plate, registration plate, number plate, badge on the grille, oval emblem, manufacturer wordmark, chrome nameplate, dealership signage, price sticker, window sticker, face, head, second person in frame` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R003.png`

**Lands on:** "That is the entire record of what was said at that counter." · **ledger** ND-08

- `R003.png`
The same sales desk from the same camera position, now with nobody at it at all: the chair on the far side stands empty and slightly turned out, the keys are still on the far corner where they were, the monitor is still turned away. The screen is never legible: it is a single soft bloom of even light with no icons, no windows, no rows, no cursor and nothing that could be read as a document. Nothing on the desk has moved. Bright showroom daylight from the left, the floor beyond soft and out of focus [STYLE] Avoid: [NEG], readable screen, spreadsheet on a monitor, web page, icons, cursor, user interface, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, person in the chair, hands in frame

**Save as:** `H:\pd-media\assets\ai\ramirez\R003.png`

**`[NEG]` addition:** append `, readable screen, spreadsheet on a monitor, web page, icons, cursor, user interface, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, person in the chair, hands in frame` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R004.png`

**Lands on:** "The salesman runs a credit check, and says Nissan will not sell him the car." · **ledger** SR-03

- `R004.png`
A close, shallow-focus still of a single set of car keys lying on a laminate desk top, the fob a plain unmarked black plastic rectangle with no buttons legible and no maker's mark, the ring and two cut keys lying flat beside it, everything beyond the keys dissolving into soft bright showroom bokeh. Nobody in frame, no hand near them, nothing else on the desk [STYLE] Avoid: [NEG], licence plate, registration plate, number plate, badge on the grille, oval emblem, manufacturer wordmark, chrome nameplate, dealership signage, price sticker, window sticker, keyring tag, engraved key, buttons with symbols, hand, fingers

**Save as:** `H:\pd-media\assets\ai\ramirez\R004.png`

**`[NEG]` addition:** append `, licence plate, registration plate, number plate, badge on the grille, oval emblem, manufacturer wordmark, chrome nameplate, dealership signage, price sticker, window sticker, keyring tag, engraved key, buttons with symbols, hand, fingers` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R005.png`

**Lands on:** "What came back was a report produced by TransUnion …" · **ledger** SR-02

- `R005.png`
A computer monitor photographed from directly behind it, so the frame is filled by the plain matte back panel of the case and its plain stand, with the light of the screen spilling out around the edges of the panel onto the desk and the wall as a soft even glow. NOT ONE PIXEL OF THE SCREEN ITSELF IS VISIBLE from this angle. No cable labels, no vents shaped like letters, no maker's mark on the case. Bright interior daylight [STYLE] Avoid: [NEG], readable screen, spreadsheet on a monitor, web page, icons, cursor, user interface, front of the monitor, reflected screen content, brand logo on the bezel

**Save as:** `H:\pd-media\assets\ai\ramirez\R005.png`

**`[NEG]` addition:** append `, readable screen, spreadsheet on a monitor, web page, icons, cursor, user interface, front of the monitor, reflected screen content, brand logo on the bezel` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R006.png`

**Lands on:** "The dealership ran his credit, the way a dealership does." · **ledger** SR-02

- `R006.png`
A plain black computer keyboard photographed from directly overhead, filling most of the frame at a slight angle, THE KEYCAPS ALL COMPLETELY BLANK — smooth unmarked squares of dark plastic with no letters, no numbers and no symbols printed on any of them — and the hard shadow of a hand and forearm falling across the left half of the keys from outside the frame. The hand itself is not in shot, only its shadow. Laminate desk visible around the edges [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, letters on the keycaps, symbols on the keys, hand in frame, fingers

**Save as:** `H:\pd-media\assets\ai\ramirez\R006.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, letters on the keycaps, symbols on the keys, hand in frame, fingers` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R007.png`

**Lands on:** "Sergio Ramirez has come to buy a Nissan Maxima." · **ledger** SR-01

- `R007.png`
The driver's door and front side window of a plain mid-size saloon car seen square on from outside at standing height, filling the frame from edge to edge, a clean reflection of pale sky and a soft line of parked cars sliding across the glass. No vehicle anywhere in this frame carries a mark of any kind: no badge, no emblem, no oval on the grille, no wordmark, no nameplate, no model lettering, no dealer sticker and no plate of any kind on any part of any of them, front or rear. The door handle is a plain flush chrome bar, the mirror housing is unpainted plastic with nothing on it, and there is no writing on the glass and no sticker in the corner of the window. Flat Californian midday [STYLE] Avoid: [NEG], licence plate, registration plate, number plate, badge on the grille, oval emblem, manufacturer wordmark, chrome nameplate, dealership signage, price sticker, window sticker, European streetscape, Irish town, Georgian doorway, EU number plate, foreign-language signage, cobbled lane, thatched roof, tram, inspection sticker, VIN plate, reflection of a person

**Save as:** `H:\pd-media\assets\ai\ramirez\R007.png`

**`[NEG]` addition:** append `, licence plate, registration plate, number plate, badge on the grille, oval emblem, manufacturer wordmark, chrome nameplate, dealership signage, price sticker, window sticker, European streetscape, Irish town, Georgian doorway, EU number plate, foreign-language signage, cobbled lane, thatched roof, tram, inspection sticker, VIN plate, reflection of a person` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R008.png`

**Lands on:** "Dublin, California. February 27th, 2011." · **ledger** SR-01

- `R008.png`
A car forecourt at midday: four straight rows of parked cars on hot pale asphalt seen from standing height at one corner of the lot, heat shimmer rising off the far row, low dry planting and a plain kerb along the far edge, a flat pale sky above. Nobody in the frame and no movement in it. No vehicle anywhere in this frame carries a mark of any kind: no badge, no emblem, no oval on the grille, no wordmark, no nameplate, no model lettering, no dealer sticker and no plate of any kind on any part of any of them, front or rear. No price stickers on any windscreen, no flags, no pennants and no signage of any kind on the lot [STYLE] Avoid: [NEG], licence plate, registration plate, number plate, badge on the grille, oval emblem, manufacturer wordmark, chrome nameplate, dealership signage, price sticker, window sticker, European streetscape, Irish town, Georgian doorway, EU number plate, foreign-language signage, cobbled lane, thatched roof, tram, windscreen price sticker, bunting, flags on poles, dealer sign

**Save as:** `H:\pd-media\assets\ai\ramirez\R008.png`

**`[NEG]` addition:** append `, licence plate, registration plate, number plate, badge on the grille, oval emblem, manufacturer wordmark, chrome nameplate, dealership signage, price sticker, window sticker, European streetscape, Irish town, Georgian doorway, EU number plate, foreign-language signage, cobbled lane, thatched roof, tram, windscreen price sticker, bunting, flags on poles, dealer sign` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R009.png`

**Lands on:** "His name is on a terrorist list." · **ledger** SR-03

- `R009.png`
A full-height showroom glass wall seen from outside on the forecourt, the interior behind it gone dim and grey because the glass is carrying a bright reflection of the empty lot and the sky: the cars inside read only as faint dark shapes through the reflection. The glass has no lettering, no vinyl graphics, no opening hours and no logo on it anywhere. Flat midday light, nobody in frame [STYLE] Avoid: [NEG], licence plate, registration plate, number plate, badge on the grille, oval emblem, manufacturer wordmark, chrome nameplate, dealership signage, price sticker, window sticker, European streetscape, Irish town, Georgian doorway, EU number plate, foreign-language signage, cobbled lane, thatched roof, tram, vinyl lettering on glass, opening hours, decal, reflection of a person

**Save as:** `H:\pd-media\assets\ai\ramirez\R009.png`

**`[NEG]` addition:** append `, licence plate, registration plate, number plate, badge on the grille, oval emblem, manufacturer wordmark, chrome nameplate, dealership signage, price sticker, window sticker, European streetscape, Irish town, Georgian doorway, EU number plate, foreign-language signage, cobbled lane, thatched roof, tram, vinyl lettering on glass, opening hours, decal, reflection of a person` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R010.png`

**Lands on:** "He was not a party. He is not named anywhere in either opinion." · **ledger** ND-08

- `R010.png`
An empty customer chair at a sales desk, photographed straight on from the far side of the desk at seated eye height: a plain fabric office chair pushed back a few inches and slightly askew, the near edge of the desk crossing the bottom of the frame as a dark bar, bright showroom floor and soft glass beyond. Nothing on the desk, nobody in the frame [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, person seated, coat over the chair

**Save as:** `H:\pd-media\assets\ai\ramirez\R010.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, person seated, coat over the chair` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R011.png`

**Lands on:** "What came back was a report produced by TransUnion …" · **ledger** SR-02

- `R011.png`
A plain grey office printer standing on a low cabinet against a pale wall, seen from the side at chest height, a single sheet of paper halfway out of its output slot and hanging slightly. The sheet is completely blank: an unbroken field of off-white paper with no print, no ruling, no letterform, no number and no mark of any kind on it. The printer's own panel is a blank dark rectangle with no icons and no display, and the machine carries no maker's mark. Soft interior daylight [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, readable screen, spreadsheet on a monitor, web page, icons, cursor, user interface, printed page, control panel icons, brand logo on the printer

**Save as:** `H:\pd-media\assets\ai\ramirez\R011.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, readable screen, spreadsheet on a monitor, web page, icons, cursor, user interface, printed page, control panel icons, brand logo on the printer` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R012.png`

**Lands on:** "His wife bought the car in her own name." · **ledger** SR-04

- `R012.png`
A plain unmarked black car key fob lying at the centre of a single contract-sized sheet of paper on a laminate desk, photographed from directly overhead. The sheet is completely blank: an unbroken field of off-white paper with no print, no ruling, no letterform, no number and no mark of any kind on it — it is a completely empty white rectangle with two soft fold-creases across it and nothing printed anywhere, no signature line, no boxes, no small print at the foot. Even light from a window to the left [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, signature line, printed clauses, small print, boxes with labels

**Save as:** `H:\pd-media\assets\ai\ramirez\R012.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, signature line, printed clauses, small print, boxes with labels` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R013.png`

**Lands on:** "So that is one man, over about a week, in one town." · **ledger** SR-01

- `R013.png`
The forecourt seen from inside the showroom through the open front door at the end of the day: the door frame makes a dark vertical border down both sides of the frame, low late sun coming in almost level and laying a long bright wedge across the floor tiles in the foreground, the parked cars outside reduced to dark shapes against the glare. Nobody in frame, no signage on the door or the glass [STYLE] Avoid: [NEG], licence plate, registration plate, number plate, badge on the grille, oval emblem, manufacturer wordmark, chrome nameplate, dealership signage, price sticker, window sticker, European streetscape, Irish town, Georgian doorway, EU number plate, foreign-language signage, cobbled lane, thatched roof, tram, opening hours on the door, vinyl lettering, sunset orange grade

**Save as:** `H:\pd-media\assets\ai\ramirez\R013.png`

**`[NEG]` addition:** append `, licence plate, registration plate, number plate, badge on the grille, oval emblem, manufacturer wordmark, chrome nameplate, dealership signage, price sticker, window sticker, European streetscape, Irish town, Georgian doorway, EU number plate, foreign-language signage, cobbled lane, thatched roof, tram, opening hours on the door, vinyl lettering, sunset orange grade` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R014.png`

**Lands on:** "A car he did not buy." · **ledger** SR-04

- `R014.png`
A close of a car's wing mirror seen from just behind and to the side, filling the right half of the frame, the mirror glass carrying a small sharp reflection of an empty asphalt forecourt with two distant parked cars on it and a pale sky. The mirror housing is plain unpainted plastic with nothing written on it, and there is no warning text etched into the mirror glass. Flat daylight [STYLE] Avoid: [NEG], licence plate, registration plate, number plate, badge on the grille, oval emblem, manufacturer wordmark, chrome nameplate, dealership signage, price sticker, window sticker, etched warning text on the mirror, reflection of a person, European streetscape, Irish town, Georgian doorway, EU number plate, foreign-language signage, cobbled lane, thatched roof, tram

**Save as:** `H:\pd-media\assets\ai\ramirez\R014.png`

**`[NEG]` addition:** append `, licence plate, registration plate, number plate, badge on the grille, oval emblem, manufacturer wordmark, chrome nameplate, dealership signage, price sticker, window sticker, etched warning text on the mirror, reflection of a person, European streetscape, Irish town, Georgian doorway, EU number plate, foreign-language signage, cobbled lane, thatched roof, tram` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R015.png`

**Lands on:** "Nobody in this film knows what the salesman was looking at …" · **ledger** ⛔-08

- `R015.png`
An overhead of a working desk top, filling the frame: a keyboard with COMPLETELY BLANK UNMARKED KEYCAPS, a plain grey mouse, a set of car keys, and a plain white mug with nothing printed on it, arranged the way a desk actually is rather than composed. No paper anywhere on the desk. Even overhead interior light, laminate grain visible [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, letters on the keycaps, printed mug, notepad, sticky notes

**Save as:** `H:\pd-media\assets\ai\ramirez\R015.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, letters on the keycaps, printed mug, notepad, sticky notes` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R016.png`

**Lands on:** "because no court ever asked him" · **ledger** ND-08

- `R016.png`
A back-of-house corridor in a commercial building, photographed straight down its length at eye height: pale painted breeze-block walls, a hard-wearing grey floor, four plain flush doors in a row on the right and one at the far end, all closed, ALL OF THEM WITH BARE FACES — no numbers, no nameplates, no signs, no notices. Even fluorescent light from a run of fittings overhead, nobody in the frame [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, door numbers, nameplate, fire notice, exit sign, European streetscape, Irish town, Georgian doorway, EU number plate, foreign-language signage, cobbled lane, thatched roof, tram

**Save as:** `H:\pd-media\assets\ai\ramirez\R016.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, door numbers, nameplate, fire notice, exit sign, European streetscape, Irish town, Georgian doorway, EU number plate, foreign-language signage, cobbled lane, thatched roof, tram` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R017.png`

**Lands on:** "Two words. A first name and a last name. That was the whole comparison." · **ledger** SR-04 / LS-14

- `R017.png`
The same car forecourt as the wide daylight lot, now with ONE EMPTY BAY IN THE MIDDLE OF AN OTHERWISE FULL ROW: the painted bay lines make a clear rectangle of bare pale asphalt with a car parked tight on either side of it, and the asphalt inside the empty bay is very slightly cleaner than the asphalt around it. Same standing height and same flat light as the earlier forecourt plate, nobody in frame. No vehicle anywhere in this frame carries a mark of any kind: no badge, no emblem, no oval on the grille, no wordmark, no nameplate, no model lettering, no dealer sticker and no plate of any kind on any part of any of them, front or rear [STYLE] Avoid: [NEG], licence plate, registration plate, number plate, badge on the grille, oval emblem, manufacturer wordmark, chrome nameplate, dealership signage, price sticker, window sticker, European streetscape, Irish town, Georgian doorway, EU number plate, foreign-language signage, cobbled lane, thatched roof, tram, numbers painted in the bay, reserved sign, person, dusk

**Save as:** `H:\pd-media\assets\ai\ramirez\R017.png`

**`[NEG]` addition:** append `, licence plate, registration plate, number plate, badge on the grille, oval emblem, manufacturer wordmark, chrome nameplate, dealership signage, price sticker, window sticker, European streetscape, Irish town, Georgian doorway, EU number plate, foreign-language signage, cobbled lane, thatched roof, tram, numbers painted in the bay, reserved sign, person, dusk` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

### A2 · the two mailings — R018–R031 (14 plates)

*ACT_1 — domestic, kitchen-table scale, morning light*

#### `R018.png`

**Lands on:** "The letter that follows will not say how to argue with it." · **ledger** SR-10

- `R018.png`
A plain white business envelope lying FACE DOWN on a bare wooden kitchen table, photographed from a low three-quarter angle a foot away, ONE CORNER OF THE FLAP LIFTED SLIGHTLY AND STANDING PROUD of the table so it catches the light. Low warm morning sun comes across the table from the left and lays the envelope's own shadow to the right. The envelope is entirely unmarked: no address, no window, no stamp, no franking, no return corner, no printing on the flap. The lower third of the frame — the bare table in front of the envelope — is the brightest part of the picture [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, address block, postage stamp, franking mark, window envelope, return address, barcode

**Save as:** `H:\pd-media\assets\ai\ramirez\R018.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, address block, postage stamp, franking mark, window envelope, return address, barcode` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R019.png`

**Lands on:** "The next day, Ramirez asked TransUnion for his own credit file." · **ledger** SR-05

- `R019.png`
The same plain white envelope on the same bare wooden kitchen table in the same morning light, now lying FACE UP AND FLAT, sealed, its front a completely empty white rectangle: no address, no name, no window, no stamp, no franking, no printing of any kind on it. Same low three-quarter angle, same distance, the table grain running away to the right [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, address block, postage stamp, franking mark, window envelope, barcode

**Save as:** `H:\pd-media\assets\ai\ramirez\R019.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, address block, postage stamp, franking mark, window envelope, barcode` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R020.png`

**Lands on:** "He had two mailings in front of him now." · **ledger** SR-09

- `R020.png`
TWO plain white envelopes lying side by side and slightly overlapping on the same bare wooden kitchen table, ONE CLEARLY LARGER AND DEEPER THAN THE OTHER so the difference in size is the subject of the picture, both face up and both completely blank — no address, no window, no stamp, no franking, no printing at all on either. Morning light from the left, seen from a low three-quarter angle [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, address block, postage stamp, window envelope, franking, barcode

**Save as:** `H:\pd-media\assets\ai\ramirez\R020.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, address block, postage stamp, window envelope, franking, barcode` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R021.png`

**Lands on:** "The day after that, a second envelope arrived." · **ledger** SR-05

- `R021.png`
A plain white envelope lying on a wooden kitchen table with its flap TORN RAGGEDLY OPEN along the top edge, the torn paper fibres standing up along the tear, the mouth of the envelope gaping slightly but ANGLED AWAY FROM THE CAMERA SO NOTHING INSIDE IT CAN BE SEEN — the interior is a flat dark gap. The envelope's face is blank. Morning light from the left [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, contents visible, letter emerging, address block, stamp

**Save as:** `H:\pd-media\assets\ai\ramirez\R021.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, contents visible, letter emerging, address block, stamp` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R022.png`

**Lands on:** "It came with the standard federal summary of a consumer's rights …" · **ledger** SR-05

- `R022.png`
A single sheet of paper, folded in three and lying open-side-down across the envelope it came out of, on a bare wooden kitchen table, photographed from overhead. The paper carries no writing of any kind, and this is what is on it instead: EVENLY SPACED FLAT GREY HORIZONTAL BARS of one uniform width and one uniform weight, laid in parallel like ruled bands of tone, each bar a solid unbroken block of soft grey with straight ends and no letter shapes, no word shapes, no gaps between words and no broken or ragged edge anywhere along it, so the sheet reads as printed matter purely by its rhythm of grey and white and carries not one readable character. The envelope beneath it is blank. Morning light from the left, the fold creases catching a soft highlight [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, printed paragraphs, headings, bullet points, letterhead, signature

**Save as:** `H:\pd-media\assets\ai\ramirez\R022.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, printed paragraphs, headings, bullet points, letterhead, signature` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R023.png`

**Lands on:** "and it did not enclose another copy of his rights" · **ledger** SR-05

- `R023.png`
A stack of three folded sheets of paper lying on a wooden table, photographed from a very low angle almost level with the table so that ONLY THE FOLDED EDGES AND THE THICKNESS OF THE STACK ARE VISIBLE and no printed face of any sheet is turned toward the camera: the picture is three pale horizontal bands of paper edge with fine shadow between them. Morning light from the left, everything beyond the stack soft [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, printed face visible, text on the edge, page numbers

**Save as:** `H:\pd-media\assets\ai\ramirez\R023.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, printed face visible, text on the edge, page numbers` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R024.png`

**Lands on:** "The day after that, a second envelope arrived." · **ledger** SR-05

- `R024.png`
A domestic letter slot seen from INSIDE a house, on the inside face of a painted front door, at chest height and square on: the sprung brass flap is pushed up and one plain white envelope is halfway through it, held in the slot, about to drop. The envelope's visible face is completely blank. The door is plain painted timber with no numbers, no nameplate and no notice on it. Cool daylight leaking round the door edge [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, house numbers on the door, nameplate, address on the envelope, junk mail, European streetscape, Irish town, Georgian doorway, EU number plate, foreign-language signage, cobbled lane, thatched roof, tram

**Save as:** `H:\pd-media\assets\ai\ramirez\R024.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, house numbers on the door, nameplate, address on the envelope, junk mail, European streetscape, Irish town, Georgian doorway, EU number plate, foreign-language signage, cobbled lane, thatched roof, tram` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R025.png`

**Lands on:** "Ramirez testified that he was confused by them." · **ledger** SR-09

- `R025.png`
A kitchen table seen from a seated height about two feet back: a plain white blank envelope lying flat in the middle of the table and a half-drunk mug of coffee gone cold beside it with a dull skin on the surface, morning light across the table from a window out of frame left, an ordinary American kitchen soft and dim behind. Nobody in the frame. The envelope and the mug are both unmarked [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, address on the envelope, printed mug, newspaper, phone on the table

**Save as:** `H:\pd-media\assets\ai\ramirez\R025.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, address on the envelope, printed mug, newspaper, phone on the table` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R026.png`

**Lands on:** "TransUnion eventually removed the alert from his file." · **ledger** SR-11

- `R026.png`
The same kitchen table from the same seated height and the same morning light, now COMPLETELY CLEARED: bare wood from edge to edge, the grain and two old ring marks the only things in the lower half of the frame, the same soft kitchen behind. No envelope, no mug, nobody in the frame [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, any object on the table, person

**Save as:** `H:\pd-media\assets\ai\ramirez\R026.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, any object on the table, person` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R027.png`

**Lands on:** "He cancelled a trip he had planned." · **ledger** SR-10

- `R027.png`
A plain white blank envelope lying on the cloth passenger seat of an ordinary car, photographed from the driver's side at head height looking down and across, the seat belt buckle and the door card visible at the edges, flat daylight coming through the side window and laying a soft bright patch across the seat. The envelope has no address, no stamp and no printing. Nobody in the car [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, address block, stamp, licence plate, registration plate, number plate, badge on the grille, oval emblem, manufacturer wordmark, chrome nameplate, dealership signage, price sticker, window sticker, dashboard display, person

**Save as:** `H:\pd-media\assets\ai\ramirez\R027.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, address block, stamp, licence plate, registration plate, number plate, badge on the grille, oval emblem, manufacturer wordmark, chrome nameplate, dealership signage, price sticker, window sticker, dashboard display, person` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R028.png`

**Lands on:** "Neither one told him how to dispute anything." · **ledger** SR-10

- `R028.png`
A single sheet of paper HELD UP FLAT AGAINST A BRIGHT WINDOW and backlit, filling most of the frame, the light coming through the fibres so the paper glows evenly — AND NOTHING SHOWS THROUGH IT: no reverse printing, no shadow of type, no watermark, no fold. It is a plain luminous rectangle. Two hands hold it at the lower corners, both flat against the paper with fingers straight and separate, seen only as dark silhouetted edges. The window frame is a soft dark cross behind [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, fingers fused into one mass, fingers merged, webbed fingers, mitten hand, stub fingers, missing thumb, extra fingers, six fingers, malformed hand, interlocked fingers, raised hand, hand held up in the air, blurred hand, reverse printing showing through, watermark, letterhead

**Save as:** `H:\pd-media\assets\ai\ramirez\R028.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, fingers fused into one mass, fingers merged, webbed fingers, mitten hand, stub fingers, missing thumb, extra fingers, six fingers, malformed hand, interlocked fingers, raised hand, hand held up in the air, blurred hand, reverse printing showing through, watermark, letterhead` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R029.png`

**Lands on:** "A trip he did not take." · **ledger** SR-10

- `R029.png`
A plain kitchen waste bin seen from directly above with its lid open, mostly empty, ONE PLAIN WHITE ENVELOPE lying alone at the bottom of the liner, creased once across the middle and face up, completely blank. Dim domestic light from above, the bin's plastic rim making a bright ellipse around the dark interior [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, address on the envelope, other rubbish with packaging, brand packaging

**Save as:** `H:\pd-media\assets\ai\ramirez\R029.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, address on the envelope, other rubbish with packaging, brand packaging` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R030.png`

**Lands on:** "One said nothing about any alert." · **ledger** SR-09

- `R030.png`
A plain white envelope held flat against the pale metal door of a domestic refrigerator by a single plain magnet, photographed square on at chest height. The envelope is blank on both the face and the flap; the magnet is an unmarked coloured disc. The fridge door is bare around it — no photographs, no notes, no lists, no other magnets. Even kitchen daylight [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, notes on the fridge, shopping list, photographs, novelty magnet with text

**Save as:** `H:\pd-media\assets\ai\ramirez\R030.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, notes on the fridge, shopping list, photographs, novelty magnet with text` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R031.png`

**Lands on:** "The other said he was a potential match to a Treasury list." · **ledger** SR-06

- `R031.png`
TWO plain white blank envelopes lying flat side by side in the bottom of a shallow open desk drawer, seen from a standing three-quarter angle looking down into it, the drawer pulled out about two thirds and the rest of its interior empty dark wood. A hand is not in frame. Soft north light from the left catching the near edge of the drawer front. Both envelopes are entirely unmarked [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, address block, stamp, other contents in the drawer, hand

**Save as:** `H:\pd-media\assets\ai\ramirez\R031.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, address block, stamp, other contents in the drawer, hand` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

### A3 · the desk drawer — R032–R041 (10 plates)

*ACT_1 → ENDING — the majority's own metaphor, ONE camera position for all ten*

#### `R032.png`

**Lands on:** "The next day, Ramirez asked TransUnion for his own credit file." · **ledger** SR-05 · motif state 1

- `R032.png`
A closed office desk drawer. The identical camera position, lens and light as every other plate in this drawer set: a plain dark-wood office desk photographed square-on from a seated eye height about four feet away, the drawer front filling the lower middle third of the frame and its two straight horizontal edges level with the bottom of the frame, one soft north window light coming from the left and falling away to the right, and nothing on the desk except what is named here. The drawer is fully shut and its front is plain unmarked wood with one plain brass handle and no label holder and no keyhole plate. ON THE DESK TOP ABOVE IT lies one plain white envelope, flat, face up, completely blank [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, label holder on the drawer, address on the envelope, other objects on the desk

**Save as:** `H:\pd-media\assets\ai\ramirez\R032.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, label holder on the drawer, address on the envelope, other objects on the desk` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R033.png`

**Lands on:** "Here is how it worked, in the Supreme Court's words." · **ledger** LS-14

- `R033.png`
The same desk drawer OPEN ABOUT A HAND'S WIDTH. The identical camera position, lens and light as every other plate in this drawer set: a plain dark-wood office desk photographed square-on from a seated eye height about four feet away, the drawer front filling the lower middle third of the frame and its two straight horizontal edges level with the bottom of the frame, one soft north window light coming from the left and falling away to the right, and nothing on the desk except what is named here. The gap above the drawer front is a flat black band and NOTHING INSIDE IT IS RESOLVED — no contents, no edges, no paper, just depth. The desk top above is bare. The brass handle catches one small highlight [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, contents visible in the gap, files, folders with tabs

**Save as:** `H:\pd-media\assets\ai\ramirez\R033.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, contents visible in the gap, files, folders with tabs` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R034.png`

**Lands on:** "TransUnion did not compare any data other than first and last names." · **ledger** LS-14 · motif state 2

- `R034.png`
The same desk drawer FULLY OPEN. The identical camera position, lens and light as every other plate in this drawer set: a plain dark-wood office desk photographed square-on from a seated eye height about four feet away, the drawer front filling the lower middle third of the frame and its two straight horizontal edges level with the bottom of the frame, one soft north window light coming from the left and falling away to the right, and nothing on the desk except what is named here. The drawer is filled from front to back with ROWS OF IDENTICAL PLAIN CARDS STANDING ON EDGE, packed tight and all the same height, all the same off-white, their top edges making one continuous straight line across the drawer. EVERY CARD IS COMPLETELY BLANK — no tabs, no labels, no printing, no colour coding, no index. The picture is rhythm and repetition, not filing [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, tabbed dividers, coloured tabs, handwritten labels, index cards with writing

**Save as:** `H:\pd-media\assets\ai\ramirez\R034.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, tabbed dividers, coloured tabs, handwritten labels, index cards with writing` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R035.png`

**Lands on:** "OFAC information was the only consumer-report data that TransUnion collected using name alone." · **ledger** LS-17

- `R035.png`
The same fully open drawer of identical blank cards. The identical camera position, lens and light as every other plate in this drawer set: a plain dark-wood office desk photographed square-on from a seated eye height about four feet away, the drawer front filling the lower middle third of the frame and its two straight horizontal edges level with the bottom of the frame, one soft north window light coming from the left and falling away to the right, and nothing on the desk except what is named here. ONE SINGLE CARD near the middle of the row STANDS ABOUT AN INCH PROUD of all the others, breaking the straight top line, and casts a thin shadow down onto its neighbours. Every card, including the proud one, is completely blank [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, writing on the raised card, tab, label, coloured card

**Save as:** `H:\pd-media\assets\ai\ramirez\R035.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, writing on the raised card, tab, label, coloured card` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R036.png`

**Lands on:** "only one thousand, eight hundred and fifty-three of them … had their credit reports disseminated" · **ledger** MN-02 · motif state 3

- `R036.png`
The same fully open drawer of identical blank cards, with ONE CARD MISSING: a narrow vertical gap in the row where a single card has been taken out, the cards on either side leaning very slightly into the space. The identical camera position, lens and light as every other plate in this drawer set: a plain dark-wood office desk photographed square-on from a seated eye height about four feet away, the drawer front filling the lower middle third of the frame and its two straight horizontal edges level with the bottom of the frame, one soft north window light coming from the left and falling away to the right, and nothing on the desk except what is named here. All remaining cards completely blank [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, writing on any card, hand in frame, card lying on the desk

**Save as:** `H:\pd-media\assets\ai\ramirez\R036.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, writing on any card, hand in frame, card lying on the desk` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R037.png`

**Lands on:** "as if someone wrote a defamatory letter and then stored it in her desk drawer" · **ledger** HD-08 · motif state 4

- `R037.png`
The same desk drawer CAUGHT IN THE ACT OF CLOSING. The identical camera position, lens and light as every other plate in this drawer set: a plain dark-wood office desk photographed square-on from a seated eye height about four feet away, the drawer front filling the lower middle third of the frame and its two straight horizontal edges level with the bottom of the frame, one soft north window light coming from the left and falling away to the right, and nothing on the desk except what is named here. The drawer front is a third of the way out and MOTION-SMEARED HORIZONTALLY along its travel, the rows of blank cards inside pulled into soft horizontal streaks of off-white by the same movement while the desk top, the wall and the window light behind stay perfectly sharp. Nobody in frame and no hand on the handle [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, hand on the drawer, whole frame blurred, writing on the cards

**Save as:** `H:\pd-media\assets\ai\ramirez\R037.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, hand on the drawer, whole frame blurred, writing on the cards` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R038.png`

**Lands on:** "A letter that is not sent does not harm anyone, no matter how insulting the letter is." · **ledger** HD-08

- `R038.png`
The same desk drawer CLOSED and the desk top above it COMPLETELY BARE. The identical camera position, lens and light as every other plate in this drawer set: a plain dark-wood office desk photographed square-on from a seated eye height about four feet away, the drawer front filling the lower middle third of the frame and its two straight horizontal edges level with the bottom of the frame, one soft north window light coming from the left and falling away to the right, and nothing on the desk except what is named here. Nothing on the desk at all — no envelope, no paper, no object — only wood grain, the two straight edges of the drawer front and one plain brass handle [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, any object on the desk, hand

**Save as:** `H:\pd-media\assets\ai\ramirez\R038.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, any object on the desk, hand` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R039.png`

**Lands on:** "But why is it so speculative that a company in the business of selling credit reports to third parties will in fact sell a credit report to a third party?" · **ledger** KG-04 · motif state 5

- `R039.png`
The same desk drawer CLOSED, and lying on the desk top above it A SINGLE SMALL SLIP OF PAPER about the size of a docket slip, alone in the middle of the bare desk, catching the window light. The sheet is completely blank: an unbroken field of off-white paper with no print, no ruling, no letterform, no number and no mark of any kind on it. The identical camera position, lens and light as every other plate in this drawer set: a plain dark-wood office desk photographed square-on from a seated eye height about four feet away, the drawer front filling the lower middle third of the frame and its two straight horizontal edges level with the bottom of the frame, one soft north window light coming from the left and falling away to the right, and nothing on the desk except what is named here. Nothing else on the desk [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, printed slip, carbon copy lines, stamp, signature, numbers

**Save as:** `H:\pd-media\assets\ai\ramirez\R039.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, printed slip, carbon copy lines, stamp, signature, numbers` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R040.png`

**Lands on:** "many of them would first learn that they were injured when they received a check" · **ledger** HD-10

- `R040.png`
The same desk and the same closed drawer SEEN FROM FURTHER BACK, about twelve feet away, so the desk now sits small in the lower middle of the frame and the whole of a plain empty office is visible around it: two other bare desks, a run of low cabinets, a bare wall, one window on the left going blue with dusk while the room falls to shadow. Nobody in the room. No notices, no whiteboard, no posters on any wall [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, wall notices, whiteboard with writing, posters, calendar, person

**Save as:** `H:\pd-media\assets\ai\ramirez\R040.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, wall notices, whiteboard with writing, posters, calendar, person` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R041.png`

**Lands on:** "So this film ends where the record ends." · **ledger** ⛔-12 · ○-04 · motif state 6

- `R041.png`
The same desk drawer CLOSED, the room now dark. The identical camera position, lens and light as every other plate in this drawer set: a plain dark-wood office desk photographed square-on from a seated eye height about four feet away, the drawer front filling the lower middle third of the frame and its two straight horizontal edges level with the bottom of the frame, one soft north window light coming from the left and falling away to the right, and nothing on the desk except what is named here. The one difference is the light: the only light in the frame is ONE BRIGHT WINDOW on the left, so the drawer front, the desk edge and the handle read as dim shapes with a single hard rim of light along their left edges, and the rest of the room falls to deep but never crushed shadow that still holds its detail. Nobody in the room. Nothing on the desk [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, crushed black shadow, lamp, screen glow, person, object on the desk

**Save as:** `H:\pd-media\assets\ai\ramirez\R041.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, crushed black shadow, lamp, screen glow, person, object on the desk` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

### A4 · the courts, from outside — R042–R053 (12 plates)

*ACT_3 / ACT_4 / ACT_5 — stone, doors, columns, light. No courtroom interior*

#### `R042.png`

**Lands on:** "To have Article III standing to sue in federal court, plaintiffs must demonstrate … that they suffered a concrete harm." · **ledger** HD-01 · TURN

- `R042.png`
An American classical civic courthouse facade photographed from the pavement at a low angle looking up, filling the frame: six plain stone columns, a deep unadorned pediment above them, cut ashlar stone, hard midday sun raking across it from the left so the flutes throw black shadow. THE PEDIMENT AND THE FRIEZE ARE COMPLETELY BLANK STONE — no carved lettering, no motto, no seal, no relief sculpture, no flag, no plaque. Nobody in the frame [STYLE] Avoid: [NEG], courtroom, judge's bench, jury box, witness stand, gavel, scales of justice, state seal, carved motto, engraved lettering on stone, banner, memorial plaque, European streetscape, Irish town, Georgian doorway, EU number plate, foreign-language signage, cobbled lane, thatched roof, tram, carved inscription on the pediment, statue, flag on a pole

**Save as:** `H:\pd-media\assets\ai\ramirez\R042.png`

**`[NEG]` addition:** append `, courtroom, judge's bench, jury box, witness stand, gavel, scales of justice, state seal, carved motto, engraved lettering on stone, banner, memorial plaque, European streetscape, Irish town, Georgian doorway, EU number plate, foreign-language signage, cobbled lane, thatched roof, tram, carved inscription on the pediment, statue, flag on a pole` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R043.png`

**Lands on:** "That is the first thing the Supreme Court of the United States said about this case, on the twenty-fifth of June, 2021." · **ledger** ID-01

- `R043.png`
A broad flight of stone courthouse steps photographed from the bottom looking up, empty, THE STONE STILL WET FROM RAIN so the treads hold a cold sheen and a few shallow puddles sit in the worn hollows. Overcast light with no sun. Plain stone balustrades on either side with no carving and no plaque on them. Nobody on the steps [STYLE] Avoid: [NEG], courtroom, judge's bench, jury box, witness stand, gavel, scales of justice, state seal, carved motto, engraved lettering on stone, banner, memorial plaque, European streetscape, Irish town, Georgian doorway, EU number plate, foreign-language signage, cobbled lane, thatched roof, tram, plaque, inscription, person, umbrella

**Save as:** `H:\pd-media\assets\ai\ramirez\R043.png`

**`[NEG]` addition:** append `, courtroom, judge's bench, jury box, witness stand, gavel, scales of justice, state seal, carved motto, engraved lettering on stone, banner, memorial plaque, European streetscape, Irish town, Georgian doorway, EU number plate, foreign-language signage, cobbled lane, thatched roof, tram, plaque, inscription, person, umbrella` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R044.png`

**Lands on:** "Justice Kavanaugh delivered the opinion of the Court." · **ledger** ID-02

- `R044.png`
A heavy bronze door, closed, photographed square on and filling the frame, its surface a grid of shallow rectangular panels with softly worn edges and a deep green-brown patina streaked by rain. EVERY PANEL IS BLANK — no relief figures, no words, no seal, no numbers, no letterbox, no notice taped to it. One plain vertical pull handle. Cool overcast light from the left [STYLE] Avoid: [NEG], courtroom, judge's bench, jury box, witness stand, gavel, scales of justice, state seal, carved motto, engraved lettering on stone, banner, memorial plaque, relief sculpture, inscription, seal, notice on the door, opening hours

**Save as:** `H:\pd-media\assets\ai\ramirez\R044.png`

**`[NEG]` addition:** append `, courtroom, judge's bench, jury box, witness stand, gavel, scales of justice, state seal, carved motto, engraved lettering on stone, banner, memorial plaque, relief sculpture, inscription, seal, notice on the door, opening hours` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R045.png`

**Lands on:** "He was joined by the Chief Justice and by Justices Alito, Gorsuch and Barrett." · **ledger** ID-03

- `R045.png`
A stone colonnade photographed from inside it looking along its length, the columns marching away to the right and RAKING LOW LIGHT cutting between them so the floor is a hard ladder of bright bands and deep shadow. The stone is plain and unadorned, the ceiling coffers empty. Nobody in the frame, no furniture, no signage [STYLE] Avoid: [NEG], courtroom, judge's bench, jury box, witness stand, gavel, scales of justice, state seal, carved motto, engraved lettering on stone, banner, memorial plaque, European streetscape, Irish town, Georgian doorway, EU number plate, foreign-language signage, cobbled lane, thatched roof, tram, inscription, statue, banner, person

**Save as:** `H:\pd-media\assets\ai\ramirez\R045.png`

**`[NEG]` addition:** append `, courtroom, judge's bench, jury box, witness stand, gavel, scales of justice, state seal, carved motto, engraved lettering on stone, banner, memorial plaque, European streetscape, Irish town, Georgian doorway, EU number plate, foreign-language signage, cobbled lane, thatched roof, tram, inscription, statue, banner, person` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R046.png`

**Lands on:** "The holding is one sentence long." · **ledger** HD-02

- `R046.png`
A polished marble floor photographed from standing height looking down and across an empty hall, ONE HARD-EDGED SHAFT OF WINDOW LIGHT lying across it as a bright parallelogram with the pattern of the glazing bars soft inside it. The marble is veined pale grey; there is no inlaid seal, no compass rose, no medallion and no lettering set into the floor. Nobody in the frame [STYLE] Avoid: [NEG], courtroom, judge's bench, jury box, witness stand, gavel, scales of justice, state seal, carved motto, engraved lettering on stone, banner, memorial plaque, inlaid seal in the floor, mosaic emblem, compass rose, person

**Save as:** `H:\pd-media\assets\ai\ramirez\R046.png`

**`[NEG]` addition:** append `, courtroom, judge's bench, jury box, witness stand, gavel, scales of justice, state seal, carved motto, engraved lettering on stone, banner, memorial plaque, inlaid seal in the floor, mosaic emblem, compass rose, person` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R047.png`

**Lands on:** "An injury in law is not an injury in fact." · **ledger** HD-04

- `R047.png`
A tall arched window high in a stone wall SEEN FROM INSIDE A DARK ROOM, the room itself almost entirely in shadow so that the window is the only bright thing in the frame and the stone reveal around it is a soft grey gradient. The glass is plain and the view through it is blown out to featureless white. No furniture, nobody in the room, no lettering anywhere [STYLE] Avoid: [NEG], courtroom, judge's bench, jury box, witness stand, gavel, scales of justice, state seal, carved motto, engraved lettering on stone, banner, memorial plaque, stained glass, crest in the glass, person, crushed black shadow

**Save as:** `H:\pd-media\assets\ai\ramirez\R047.png`

**`[NEG]` addition:** append `, courtroom, judge's bench, jury box, witness stand, gavel, scales of justice, state seal, carved motto, engraved lettering on stone, banner, memorial plaque, stained glass, crest in the glass, person, crushed black shadow` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R048.png`

**Lands on:** "TransUnion appealed, and it appealed to a court that mostly agreed with the jury." · **ledger** MN-06

- `R048.png`
A plain three-storey American civic office building of the appellate scale, photographed square on from across the street in flat overcast light: a regular grid of identical windows, a plain stone or precast facade, a shallow set-back entrance at the centre. THE BUILDING CARRIES NO NAME, no lettering above the door, no seal, no flag and no signage of any kind. An empty pavement across the foreground [STYLE] Avoid: [NEG], courtroom, judge's bench, jury box, witness stand, gavel, scales of justice, state seal, carved motto, engraved lettering on stone, banner, memorial plaque, European streetscape, Irish town, Georgian doorway, EU number plate, foreign-language signage, cobbled lane, thatched roof, tram, building name in stone, flagpole, sign over the entrance, person

**Save as:** `H:\pd-media\assets\ai\ramirez\R048.png`

**`[NEG]` addition:** append `, courtroom, judge's bench, jury box, witness stand, gavel, scales of justice, state seal, carved motto, engraved lettering on stone, banner, memorial plaque, European streetscape, Irish town, Georgian doorway, EU number plate, foreign-language signage, cobbled lane, thatched roof, tram, building name in stone, flagpole, sign over the entrance, person` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R049.png`

**Lands on:** "Ramirez sued in February 2012. In 2014 the district court certified a class." · **ledger** ID-08

- `R049.png`
A wide of an empty paved civic plaza in front of a large plain stone building, photographed from one corner at standing height so the plaza fills the lower two thirds of the frame: large pale slabs, a shallow step across the middle distance, ONE SINGLE FIGURE crossing it far away and very small, no bigger than a fiftieth of the frame height, reduced to a dark shape with no features. Flat overcast light [STYLE] Avoid: [NEG], courtroom, judge's bench, jury box, witness stand, gavel, scales of justice, state seal, carved motto, engraved lettering on stone, banner, memorial plaque, European streetscape, Irish town, Georgian doorway, EU number plate, foreign-language signage, cobbled lane, thatched roof, tram, sculpture, monument, banner, crowd, recognisable face

**Save as:** `H:\pd-media\assets\ai\ramirez\R049.png`

**`[NEG]` addition:** append `, courtroom, judge's bench, jury box, witness stand, gavel, scales of justice, state seal, carved motto, engraved lettering on stone, banner, memorial plaque, European streetscape, Irish town, Georgian doorway, EU number plate, foreign-language signage, cobbled lane, thatched roof, tram, sculpture, monument, banner, crowd, recognisable face` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R050.png`

**Lands on:** "It did not decide whether the class was properly certified. It sent that question back." · **ledger** ND-03

- `R050.png`
A stone cornice photographed from directly below against a hard clear blue sky, so the frame is split by one strong diagonal edge: heavy plain moulding, weather-darkened joints, a run of shallow dentils under it, all of it BLANK STONE with no carved lettering, no dates, no seal and no relief. Bright sunlight from behind the building so the stone reads cool against the blue [STYLE] Avoid: [NEG], courtroom, judge's bench, jury box, witness stand, gavel, scales of justice, state seal, carved motto, engraved lettering on stone, banner, memorial plaque, carved date, inscription, gargoyle, statue, flag

**Save as:** `H:\pd-media\assets\ai\ramirez\R050.png`

**`[NEG]` addition:** append `, courtroom, judge's bench, jury box, witness stand, gavel, scales of justice, state seal, carved motto, engraved lettering on stone, banner, memorial plaque, carved date, inscription, gargoyle, statue, flag` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R051.png`

**Lands on:** "It did not decide whether the 6,332 could sue in a state court." · **ledger** ND-04

- `R051.png`
A long empty corridor photographed straight down its length at eye height: a stone floor running to a vanishing point, tall panelled doors in a row on both sides all closed, plain plastered walls above a stone dado, cool daylight coming in from a window at the far end. EVERY DOOR IS BARE — no numbers, no nameplates, no signs, no notices, no directory board on any wall. Nobody in the corridor [STYLE] Avoid: [NEG], courtroom, judge's bench, jury box, witness stand, gavel, scales of justice, state seal, carved motto, engraved lettering on stone, banner, memorial plaque, door numbers, nameplate, directory board, exit sign, person

**Save as:** `H:\pd-media\assets\ai\ramirez\R051.png`

**`[NEG]` addition:** append `, courtroom, judge's bench, jury box, witness stand, gavel, scales of justice, state seal, carved motto, engraved lettering on stone, banner, memorial plaque, door numbers, nameplate, directory board, exit sign, person` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R052.png`

**Lands on:** "Three judges heard that appeal, and they did not agree with each other." · **ledger** ID-07

- `R052.png`
A close of a brass handrail on a stone stair, the rail running diagonally through the frame from lower left to upper right, its top face polished bright by decades of hands and its underside dark with tarnish, the plain stone treads and the moulded stringer soft behind it. Side light from the left. No engraving on the rail, no plaque on the wall, nobody in frame [STYLE] Avoid: [NEG], courtroom, judge's bench, jury box, witness stand, gavel, scales of justice, state seal, carved motto, engraved lettering on stone, banner, memorial plaque, engraved rail, plaque, hand on the rail, person

**Save as:** `H:\pd-media\assets\ai\ramirez\R052.png`

**`[NEG]` addition:** append `, courtroom, judge's bench, jury box, witness stand, gavel, scales of justice, state seal, carved motto, engraved lettering on stone, banner, memorial plaque, engraved rail, plaque, hand on the rail, person` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R053.png`

**Lands on:** "Now — what did the Supreme Court actually decide? Less than almost anyone remembers." · **ledger** ND-01 … ND-06

- `R053.png`
A plain stone civic facade at dusk photographed from across the street, the sky above it gone deep blue-grey and the stone reading cold, with ONE HORIZONTAL ROW OF WINDOWS on the second floor LIT WARM FROM WITHIN while every other window in the building is dark. No street lighting flare, no signage on the building, no flag, nobody on the pavement [STYLE] Avoid: [NEG], courtroom, judge's bench, jury box, witness stand, gavel, scales of justice, state seal, carved motto, engraved lettering on stone, banner, memorial plaque, European streetscape, Irish town, Georgian doorway, EU number plate, foreign-language signage, cobbled lane, thatched roof, tram, illuminated sign, floodlighting, flag, person, lens flare

**Save as:** `H:\pd-media\assets\ai\ramirez\R053.png`

**`[NEG]` addition:** append `, courtroom, judge's bench, jury box, witness stand, gavel, scales of justice, state seal, carved motto, engraved lettering on stone, banner, memorial plaque, European streetscape, Irish town, Georgian doorway, EU number plate, foreign-language signage, cobbled lane, thatched roof, tram, illuminated sign, floodlighting, flag, person, lens flare` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

### B · the identifiers that were never compared — R054–R072 (19 plates)

*ACT_2 — the objects, never the words. Typography goes over them in Remotion*

#### `R054.png`

**Lands on:** "An entry often will have, for example, a full name, an address, a nationality, a passport" · **ledger** LS-08

- `R054.png`
A closed passport-sized booklet lying alone on a dark matte surface, photographed from directly overhead in soft even light, filling about a third of the frame. THE COVER IS COMPLETELY BLANK: a plain dark blue-grey grained board with no crest, no coat of arms, no gold blocking, no country name, no chip symbol and no lettering anywhere on it. The corners are slightly rounded and softly worn [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, coat of arms, gold blocking, country name, chip symbol, crest, passport cover design

**Save as:** `H:\pd-media\assets\ai\ramirez\R054.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, coat of arms, gold blocking, country name, chip symbol, crest, passport cover design` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R055.png`

**Lands on:** "Passport information." · **ledger** SR-08

- `R055.png`
The same passport-sized booklet lying OPEN at its centre spread on the same dark surface, photographed from directly overhead. The paper carries no writing of any kind, and this is what is on it instead: EVENLY SPACED FLAT GREY HORIZONTAL BARS of one uniform width and one uniform weight, laid in parallel like ruled bands of tone, each bar a solid unbroken block of soft grey with straight ends and no letter shapes, no word shapes, no gaps between words and no broken or ragged edge anywhere along it, so the sheet reads as printed matter purely by its rhythm of grey and white and carries not one readable character — both facing pages carry only the flat grey bars, in two short stacks, and nothing else: no photograph window, no machine-readable zone, no stamps, no crest, no numbers. Soft even light, the gutter shadow down the middle [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, photo page, machine readable zone, visa stamps, crest, portrait window

**Save as:** `H:\pd-media\assets\ai\ramirez\R055.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, photo page, machine readable zone, visa stamps, crest, portrait window` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R056.png`

**Lands on:** "a tax identification or cedula number" · **ledger** LS-08

- `R056.png`
A single plain paper form lying flat on a plain desk, photographed from directly overhead and filling the frame. THE FORM IS A GRID OF EMPTY RULED BOXES AND NOTHING ELSE: fine grey rectangles in rows, each one completely empty, with no field labels, no headings, no small print, no numbers, no logo and no signature line anywhere on the sheet. Even soft light, one shallow crease across the paper [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, field labels, headings, printed instructions, tick boxes with words, logo

**Save as:** `H:\pd-media\assets\ai\ramirez\R056.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, field labels, headings, printed instructions, tick boxes with words, logo` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R057.png`

**Lands on:** "a date of birth" · **ledger** LS-08

- `R057.png`
A wooden-handled rubber date stamp LYING ON ITS SIDE on a plain desk, close, so that the rubber face is turned toward the camera at an angle: the raised rubber on the face is a SOFT ILLEGIBLE JUMBLE OF WORN GREY-BLACK SHAPES with no readable characters, no digits and no date bands that resolve. Shallow focus, the handle sharp and the face slightly soft. Bare desk around it [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, readable date, digits on the stamp, month letters, ink pad with a brand

**Save as:** `H:\pd-media\assets\ai\ramirez\R057.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, readable date, digits on the stamp, month letters, ink pad with a brand` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R058.png`

**Lands on:** "a nationality" · **ledger** LS-08

- `R058.png`
The curved surface of a physical desk globe photographed very close at a shallow raking angle, so the horizon of the sphere runs across the frame and the land masses read only as soft blocks of muted colour: NO COUNTRY NAMES, NO CITY NAMES, NO BORDER LINES AND NO LETTERING of any kind are legible anywhere on it — the printing dissolves into colour and grain. One soft window highlight sliding along the curve [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, country names, city labels, latitude numbers, readable map text

**Save as:** `H:\pd-media\assets\ai\ramirez\R058.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, country names, city labels, latitude numbers, readable map text` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R059.png`

**Lands on:** "an address" · **ledger** LS-08

- `R059.png`
A street of ordinary single-storey American suburban houses photographed from the middle of the road at standing height in flat daylight: identical driveways, mown front lawns, a kerbline running to a vanishing point, parked cars at the kerb. NO HOUSE NUMBERS ON ANY HOUSE, no mailbox lettering, no street sign, no realtor board, nobody in the frame. Plain pale sky [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, house numbers, street sign, mailbox with a name, realtor sign, licence plate, registration plate, number plate, badge on the grille, oval emblem, manufacturer wordmark, chrome nameplate, dealership signage, price sticker, window sticker, European streetscape, Irish town, Georgian doorway, EU number plate, foreign-language signage, cobbled lane, thatched roof, tram

**Save as:** `H:\pd-media\assets\ai\ramirez\R059.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, house numbers, street sign, mailbox with a name, realtor sign, licence plate, registration plate, number plate, badge on the grille, oval emblem, manufacturer wordmark, chrome nameplate, dealership signage, price sticker, window sticker, European streetscape, Irish town, Georgian doorway, EU number plate, foreign-language signage, cobbled lane, thatched roof, tram` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R060.png`

**Lands on:** "a place of birth" · **ledger** LS-08

- `R060.png`
The exterior of a small plain civic register office: a low mid-century public building of pale brick with a flat canopy over a glazed entrance, three steps up, a low wall and a strip of clipped planting in front, photographed square on from across the pavement in flat overcast light. THE BUILDING CARRIES NO NAME AND NO SIGN of any kind, the glass beside the door is clear and empty, and nobody is in the frame [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, building name, opening hours, notice board, seal over the door, European streetscape, Irish town, Georgian doorway, EU number plate, foreign-language signage, cobbled lane, thatched roof, tram, person

**Save as:** `H:\pd-media\assets\ai\ramirez\R060.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, building name, opening hours, notice board, seal over the door, European streetscape, Irish town, Georgian doorway, EU number plate, foreign-language signage, cobbled lane, thatched roof, tram, person` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R061.png`

**Lands on:** "a date of birth" · **ledger** LS-08

- `R061.png`
A paper wall calendar hanging on a plain painted wall, photographed square on from six feet away with the focus set on the wall beside it so THE CALENDAR ITSELF IS OUT OF FOCUS: its month grid reads only as a soft blur of pale squares and grey smudges, with no digits, no month name and no weekday letters resolvable anywhere on it. Even daylight from the left, the wall bare around it [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, readable numbers, month name, weekday letters, sharp calendar, photograph on the calendar

**Save as:** `H:\pd-media\assets\ai\ramirez\R061.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, readable numbers, month name, weekday letters, sharp calendar, photograph on the calendar` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R062.png`

**Lands on:** "a full name" · **ledger** LS-08

- `R062.png`
A desk nameplate standing on a plain desk, photographed close and square on at desk height, filling the middle of the frame: a plain brushed brass plate in a plain dark wooden holder, ITS FACE COMPLETELY BLANK — bare brushed metal with a soft directional grain and one shallow reflection running along it, and no engraving, no name, no title, no lettering, no logo. The desk beyond it is empty and soft [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, engraved name, job title, initials, logo on the plate

**Save as:** `H:\pd-media\assets\ai\ramirez\R062.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, engraved name, job title, initials, logo on the plate` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R063.png`

**Lands on:** "former names, and aliases" · **ledger** LS-08

- `R063.png`
A single plain filing card HELD LIGHTLY BETWEEN THE TIPS OF A THUMB AND A FOREFINGER at the bottom corner, the rest of the hand out of the frame, the card standing upright and filling the middle of the picture, front on. THE CARD IS COMPLETELY BLANK — no ruling, no printing, no writing, no tab, no punch hole. The two visible digits are clearly separate, each with its own nail and its own shadow on the card. Soft even light, dark soft background [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, fingers fused into one mass, fingers merged, webbed fingers, mitten hand, stub fingers, missing thumb, extra fingers, six fingers, malformed hand, interlocked fingers, raised hand, hand held up in the air, blurred hand, writing on the card, ruled lines, index tab

**Save as:** `H:\pd-media\assets\ai\ramirez\R063.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, fingers fused into one mass, fingers merged, webbed fingers, mitten hand, stub fingers, missing thumb, extra fingers, six fingers, malformed hand, interlocked fingers, raised hand, hand held up in the air, blurred hand, writing on the card, ruled lines, index tab` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R064.png`

**Lands on:** "It publishes, alongside them, the things that tell one human being from another." · **ledger** LS-08

- `R064.png`
A wall of small identical wooden index drawers filling the entire frame, photographed square on and lit from the left: eight rows by twelve columns of the same little drawer front, each with the same plain brass cup handle and the same empty brass label holder above it, and EVERY LABEL HOLDER IS EMPTY — bare metal frames with no cards and no writing in any of them. The wood is worn pale at the handles [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, cards in the label holders, letters on the drawers, alphabet dividers, numbers

**Save as:** `H:\pd-media\assets\ai\ramirez\R064.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, cards in the label holders, letters on the drawers, alphabet dividers, numbers` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R065.png`

**Lands on:** "run through a computer-based screening system" · **ledger** LS-09

- `R065.png`
A bank of identical grey server cabinets in a cold windowless room, photographed straight down the aisle between two rows at eye height: perforated dark doors in a long repeating rank, a hard even overhead light, a bare raised floor. The status lights on the cabinets are SOFT UNRESOLVED SPECKS OF GREEN AND AMBER with no pattern that could be read, and there are no maker's marks, no rack labels and no printed asset tags anywhere [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, readable screen, spreadsheet on a monitor, web page, icons, cursor, user interface, rack labels, asset tags, brand logo on the cabinets, blue neon glow

**Save as:** `H:\pd-media\assets\ai\ramirez\R065.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, readable screen, spreadsheet on a monitor, web page, icons, cursor, user interface, rack labels, asset tags, brand logo on the cabinets, blue neon glow` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R066.png`

**Lands on:** "The tool works on approximate string matching." · **ledger** LS-11

- `R066.png`
A close, very shallow-focus still of the cut ends of a bundle of fibre optic cables, the polished ferrules catching small hard points of light, the bundle running out of the bottom of the frame and everything behind it dissolved into a soft dark wash. No connectors with printing, no cable labels, no colour-coded tags with writing. Cool light [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, cable labels, printed connectors, neon blue grade, readable screen, spreadsheet on a monitor, web page, icons, cursor, user interface

**Save as:** `H:\pd-media\assets\ai\ramirez\R066.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, cable labels, printed connectors, neon blue grade, readable screen, spreadsheet on a monitor, web page, icons, cursor, user interface` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R067.png`

**Lands on:** "Its own search tool carries a warning that using it is not a substitute for undertaking appropriate due diligence." · **ledger** LS-11

- `R067.png`
A computer monitor seen square on from the front in a dim room, THE ENTIRE SCREEN A SINGLE FIELD OF SOFT EVEN PALE LIGHT with no content on it whatsoever: no window, no cursor, no icon, no line of text, no menu bar, no reflection of a room. The bezel is plain matte black with no maker's mark. The light from the screen falls on a bare desk in front of it. Nobody in frame [STYLE] Avoid: [NEG], readable screen, spreadsheet on a monitor, web page, icons, cursor, user interface, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, desktop icons, reflection of a person, brand logo on the bezel

**Save as:** `H:\pd-media\assets\ai\ramirez\R067.png`

**`[NEG]` addition:** append `, readable screen, spreadsheet on a monitor, web page, icons, cursor, user interface, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, desktop icons, reflection of a person, brand logo on the bezel` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R068.png`

**Lands on:** "Thousands of law-abiding Americans happen to share a first and last name with one of the terrorists, drug traffickers or serious criminals on OFAC's list." · **ledger** LS-15

- `R068.png`
Hundreds of small identical pale record cards laid out edge to edge IN A DENSE REGULAR GRID filling the entire frame, photographed from directly overhead in even soft light, the picture reading as texture and repetition. EVERY CARD IS COMPLETELY BLANK — no printing, no ruling, no writing, no numbers. ONE SINGLE CARD near the lower middle is LIFTED SLIGHTLY OUT OF THE GRID at an angle and catches a brighter highlight along its raised edge, throwing a small shadow onto the cards beneath. The lower edge of the frame is the brightest part of the picture [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, writing on the cards, printed forms, ruled lines, hand, numbers

**Save as:** `H:\pd-media\assets\ai\ramirez\R068.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, writing on the cards, printed forms, ruled lines, hand, numbers` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R069.png`

**Lands on:** "The court's own example is that Cortez would match with Cortes." · **ledger** LS-16

- `R069.png`
The same dense overhead grid of identical blank record cards, now with TWO CARDS LIFTED slightly out of the grid, FAR APART FROM ONE ANOTHER — one near the upper left, one near the lower right — each catching its own highlight and throwing its own small shadow, everything between them flat and identical. Same overhead camera, same even light. All cards completely blank [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, writing on the cards, hand, numbers, arrows, connecting line

**Save as:** `H:\pd-media\assets\ai\ramirez\R069.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, writing on the cards, hand, numbers, arrows, connecting line` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R070.png`

**Lands on:** "Unsurprisingly, the Supreme Court says, the product generated many false positives." · **ledger** LS-15

- `R070.png`
The same field of identical blank record cards photographed FROM A LOW RAKING ANGLE just above the surface instead of overhead, so the near cards are sharp and huge in the foreground and the grid recedes fast into soft focus and finally into a pale blur at the top of the frame. All cards completely blank, no card lifted. Even soft light from the left [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, writing on the cards, hand, sharp far cards, numbers

**Save as:** `H:\pd-media\assets\ai\ramirez\R070.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, writing on the cards, hand, sharp far cards, numbers` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R071.png`

**Lands on:** "In collecting other types of data for use on consumer reports — such as tax liens or bankruptcy judgments" · **ledger** LS-17

- `R071.png`
A folded stack of continuous fanfold computer paper lying on a plain dark surface, photographed from a low three-quarter angle so the concertina folds and the perforated sprocket margins down both sides are the shape of the picture. The paper carries no writing of any kind, and this is what is on it instead: EVENLY SPACED FLAT GREY HORIZONTAL BARS of one uniform width and one uniform weight, laid in parallel like ruled bands of tone, each bar a solid unbroken block of soft grey with straight ends and no letter shapes, no word shapes, no gaps between words and no broken or ragged edge anywhere along it, so the sheet reads as printed matter purely by its rhythm of grey and white and carries not one readable character, and the sprocket holes are the only regular punctuation in the frame. Soft side light picking out each fold [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, printed rows of figures, column headings, dot matrix text, tractor-feed labels

**Save as:** `H:\pd-media\assets\ai\ramirez\R071.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, printed rows of figures, column headings, dot matrix text, tractor-feed labels` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R072.png`

**Lands on:** "OFAC information was the only consumer-report data that TransUnion collected using name alone." · **ledger** LS-17

- `R072.png`
ONE single plain pale card lying alone at the centre of an otherwise completely empty dark table, photographed from a low three-quarter angle a foot away, one soft light from the left so the card is the brightest thing in the frame and its thin shadow runs away to the right. THE CARD IS COMPLETELY BLANK. Nothing else is in the frame at all [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, writing on the card, second card, hand, spotlight vignette

**Save as:** `H:\pd-media\assets\ai\ramirez\R072.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, writing on the card, second card, hand, spotlight vignette` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

### C · the people lane  [HSTYLE] — R073–R096 (24 plates)

*all acts — 24 plates, all mandatory, nine carrying a resolvable face*

#### `R073.png`

**Lands on:** "His wife is with him, and his father-in-law." · **ledger** SR-01

- `R073.png`
[HSTYLE] photographic, 35mm, natural light, real adults, ordinary clothing, ordinary bodies, believable American setting, candid framing, no styling, no beauty retouching, no model look, no stock-photo smiles, faces neutral and unremarkable, nobody looking at the lens. THREE ADULTS SEEN FROM BEHIND at a sales desk, framed from behind their shoulders at seated height: three backs and three sets of shoulders fill the lower half of the frame as dark soft masses, NO FACE IS VISIBLE AND NOT ONE HEAD IS TURNED, and the near hands of the middle figure rest flat on the desk edge in sharp focus with the fingers separate. Everything beyond them — the desk, the chair opposite, the bright showroom — falls away into soft focus. Ordinary weekday clothes, no coats, nothing branded [STYLE] Avoid: [NEG], fingers fused into one mass, fingers merged, webbed fingers, mitten hand, stub fingers, missing thumb, extra fingers, six fingers, malformed hand, interlocked fingers, raised hand, hand held up in the air, blurred hand, face, profile, turned head, reflection of a face, licence plate, registration plate, number plate, badge on the grille, oval emblem, manufacturer wordmark, chrome nameplate, dealership signage, price sticker, window sticker

**Save as:** `H:\pd-media\assets\ai\ramirez\R073.png`

**`[NEG]` addition:** append `, fingers fused into one mass, fingers merged, webbed fingers, mitten hand, stub fingers, missing thumb, extra fingers, six fingers, malformed hand, interlocked fingers, raised hand, hand held up in the air, blurred hand, face, profile, turned head, reflection of a face, licence plate, registration plate, number plate, badge on the grille, oval emblem, manufacturer wordmark, chrome nameplate, dealership signage, price sticker, window sticker` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R074.png`

**Lands on:** "The salesman runs a credit check" · **ledger** SR-02

- `R074.png`
[HSTYLE] photographic, 35mm, natural light, real adults, ordinary clothing, ordinary bodies, believable American setting, candid framing, no styling, no beauty retouching, no model look, no stock-photo smiles, faces neutral and unremarkable, nobody looking at the lens. ONE adult hand alone on a laminate desk beside a set of car keys, photographed close from a low three-quarter angle. THE HAND IS AT REST FLAT ON THE SURFACE, not raised and not held in the air, the palm laid down in full contact with it and the wrist straight, THE FOUR FINGERS LYING SIDE BY SIDE AND SEPARATE with a visible line of shadow between each pair and one nail showing on each, and the thumb clearly apart from the fingers along the near side. A plain worn wedding band sits on the ring finger. The skin is mid-forties, dry, ordinary, with visible knuckle creases and short unmanicured nails. The keys lie a few inches beyond the fingertips, unmarked. Bright daylight from the left, the rest of the desk soft [STYLE] Avoid: [NEG], fingers fused into one mass, fingers merged, webbed fingers, mitten hand, stub fingers, missing thumb, extra fingers, six fingers, malformed hand, interlocked fingers, raised hand, hand held up in the air, blurred hand, manicured nails, jewellery beyond one plain band, wristwatch with a readable face, licence plate, registration plate, number plate, badge on the grille, oval emblem, manufacturer wordmark, chrome nameplate, dealership signage, price sticker, window sticker

**Save as:** `H:\pd-media\assets\ai\ramirez\R074.png`

**`[NEG]` addition:** append `, fingers fused into one mass, fingers merged, webbed fingers, mitten hand, stub fingers, missing thumb, extra fingers, six fingers, malformed hand, interlocked fingers, raised hand, hand held up in the air, blurred hand, manicured nails, jewellery beyond one plain band, wristwatch with a readable face, licence plate, registration plate, number plate, badge on the grille, oval emblem, manufacturer wordmark, chrome nameplate, dealership signage, price sticker, window sticker` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R075.png`

**Lands on:** "The salesman runs a credit check" · **ledger** SR-02

- `R075.png`
[HSTYLE] photographic, 35mm, natural light, real adults, ordinary clothing, ordinary bodies, believable American setting, candid framing, no styling, no beauty retouching, no model look, no stock-photo smiles, faces neutral and unremarkable, nobody looking at the lens. A hand on a computer keyboard photographed close from the side at desk height, THE PALM AND FINGERS RESTING DOWN ON THE KEYS rather than typing in mid-air, THE FOUR FINGERS SIDE BY SIDE AND SEPARATE each on its own key with a line of shadow between them and one nail visible on each, the thumb down by the space bar and clearly apart. The keycaps are blank and unmarked. A cool screen light from out of frame right lies along the knuckles and the back of the hand; THE SCREEN ITSELF IS NOT IN THE FRAME [STYLE] Avoid: [NEG], fingers fused into one mass, fingers merged, webbed fingers, mitten hand, stub fingers, missing thumb, extra fingers, six fingers, malformed hand, interlocked fingers, raised hand, hand held up in the air, blurred hand, readable screen, spreadsheet on a monitor, web page, icons, cursor, user interface, letters on the keycaps, hands typing in mid-air, second hand

**Save as:** `H:\pd-media\assets\ai\ramirez\R075.png`

**`[NEG]` addition:** append `, fingers fused into one mass, fingers merged, webbed fingers, mitten hand, stub fingers, missing thumb, extra fingers, six fingers, malformed hand, interlocked fingers, raised hand, hand held up in the air, blurred hand, readable screen, spreadsheet on a monitor, web page, icons, cursor, user interface, letters on the keycaps, hands typing in mid-air, second hand` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R076.png`

**Lands on:** "His wife bought the car in her own name." · **ledger** SR-04

- `R076.png`
[HSTYLE] photographic, 35mm, natural light, real adults, ordinary clothing, ordinary bodies, believable American setting, candid framing, no styling, no beauty retouching, no model look, no stock-photo smiles, faces neutral and unremarkable, nobody looking at the lens. A woman's two hands at a counter, framed from the forearms down and seen from just above and in front, both hands DOWN ON THE COUNTER TOP AND IN FULL CONTACT WITH IT: the left hand lies flat and steady on the corner of a sheet of paper with its four fingers side by side and separate, and the right hand rests on the paper on the heel of the palm with a plain pen held between the thumb and the first two fingers, THE PEN'S TIP TOUCHING THE PAPER AND AT REST. Every finger on both hands is separately visible with its own nail. The sheet is completely blank: an unbroken field of off-white paper with no print, no ruling, no letterform, no number and no mark of any kind on it. Bright daylight from the left [STYLE] Avoid: [NEG], fingers fused into one mass, fingers merged, webbed fingers, mitten hand, stub fingers, missing thumb, extra fingers, six fingers, malformed hand, interlocked fingers, raised hand, hand held up in the air, blurred hand, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, hand raised off the surface, pen in mid-air, signature on the paper, printed contract

**Save as:** `H:\pd-media\assets\ai\ramirez\R076.png`

**`[NEG]` addition:** append `, fingers fused into one mass, fingers merged, webbed fingers, mitten hand, stub fingers, missing thumb, extra fingers, six fingers, malformed hand, interlocked fingers, raised hand, hand held up in the air, blurred hand, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, hand raised off the surface, pen in mid-air, signature on the paper, printed contract` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R077.png`

**Lands on:** "A car he did not buy." · **ledger** SR-04

- `R077.png`
[HSTYLE] photographic, 35mm, natural light, real adults, ordinary clothing, ordinary bodies, believable American setting, candid framing, no styling, no beauty retouching, no model look, no stock-photo smiles, faces neutral and unremarkable, nobody looking at the lens. A man in his forties SEEN ENTIRELY FROM BEHIND, standing still in the middle of a bright empty car showroom, framed from the knees up and placed slightly left of centre: an ordinary dark jacket, ordinary trousers, ordinary short hair, both arms hanging at his sides with the hands relaxed and the fingers loosely separate. HIS HEAD IS NOT TURNED AND NO PART OF HIS FACE IS VISIBLE. The showroom glass and floor beyond him are bright and soft [STYLE] Avoid: [NEG], fingers fused into one mass, fingers merged, webbed fingers, mitten hand, stub fingers, missing thumb, extra fingers, six fingers, malformed hand, interlocked fingers, raised hand, hand held up in the air, blurred hand, face, profile, turned head, reflection of his face in the glass, licence plate, registration plate, number plate, badge on the grille, oval emblem, manufacturer wordmark, chrome nameplate, dealership signage, price sticker, window sticker

**Save as:** `H:\pd-media\assets\ai\ramirez\R077.png`

**`[NEG]` addition:** append `, fingers fused into one mass, fingers merged, webbed fingers, mitten hand, stub fingers, missing thumb, extra fingers, six fingers, malformed hand, interlocked fingers, raised hand, hand held up in the air, blurred hand, face, profile, turned head, reflection of his face in the glass, licence plate, registration plate, number plate, badge on the grille, oval emblem, manufacturer wordmark, chrome nameplate, dealership signage, price sticker, window sticker` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R078.png`

**Lands on:** "A car he did not buy." · **ledger** SR-04

- `R078.png`
[HSTYLE] photographic, 35mm, natural light, real adults, ordinary clothing, ordinary bodies, believable American setting, candid framing, no styling, no beauty retouching, no model look, no stock-photo smiles, faces neutral and unremarkable, nobody looking at the lens. Two adults WALKING AWAY FROM THE CAMERA across an open car forecourt at midday, seen from behind and far off so that together they occupy less than a sixth of the frame height and no feature of either is resolvable — two ordinary dark silhouettes against hot pale asphalt, one slightly ahead of the other. Rows of parked unmarked cars either side, flat hard light, a pale sky [STYLE] Avoid: [NEG], fingers fused into one mass, fingers merged, webbed fingers, mitten hand, stub fingers, missing thumb, extra fingers, six fingers, malformed hand, interlocked fingers, raised hand, hand held up in the air, blurred hand, face, turned head, licence plate, registration plate, number plate, badge on the grille, oval emblem, manufacturer wordmark, chrome nameplate, dealership signage, price sticker, window sticker, close figures, recognisable clothing brand

**Save as:** `H:\pd-media\assets\ai\ramirez\R078.png`

**`[NEG]` addition:** append `, fingers fused into one mass, fingers merged, webbed fingers, mitten hand, stub fingers, missing thumb, extra fingers, six fingers, malformed hand, interlocked fingers, raised hand, hand held up in the air, blurred hand, face, turned head, licence plate, registration plate, number plate, badge on the grille, oval emblem, manufacturer wordmark, chrome nameplate, dealership signage, price sticker, window sticker, close figures, recognisable clothing brand` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R079.png`

**Lands on:** "The day after that, a second envelope arrived." · **ledger** SR-05

- `R079.png`
[HSTYLE] photographic, 35mm, natural light, real adults, ordinary clothing, ordinary bodies, believable American setting, candid framing, no styling, no beauty retouching, no model look, no stock-photo smiles, faces neutral and unremarkable, nobody looking at the lens. An adult's hands and forearms only, opening an envelope at a wooden kitchen table, framed from just above and in front with the head and body entirely out of the frame: BOTH HANDS REST DOWN ON THE TABLE, the left hand flat and holding the envelope steady against the wood with four separate fingers, the right hand also down on the table working a thumb under the flap. Every finger on both hands is distinct with its own nail and its own shadow. The envelope is blank. Morning light from the left [STYLE] Avoid: [NEG], fingers fused into one mass, fingers merged, webbed fingers, mitten hand, stub fingers, missing thumb, extra fingers, six fingers, malformed hand, interlocked fingers, raised hand, hand held up in the air, blurred hand, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, hands raised in the air, address on the envelope, letter opener, face

**Save as:** `H:\pd-media\assets\ai\ramirez\R079.png`

**`[NEG]` addition:** append `, fingers fused into one mass, fingers merged, webbed fingers, mitten hand, stub fingers, missing thumb, extra fingers, six fingers, malformed hand, interlocked fingers, raised hand, hand held up in the air, blurred hand, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, hands raised in the air, address on the envelope, letter opener, face` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R080.png`

**Lands on:** "Ramirez testified that he was confused by them." · **ledger** SR-09

- `R080.png`
[HSTYLE] photographic, 35mm, natural light, real adults, ordinary clothing, ordinary bodies, believable American setting, candid framing, no styling, no beauty retouching, no model look, no stock-photo smiles, faces neutral and unremarkable, nobody looking at the lens. AN INVENTED, COMPLETELY FICTIONAL man in his forties, in three-quarter profile, seated at an ordinary American kitchen table reading something held low and out of the bottom of the frame: HIS FACE IS VISIBLE AND IN FOCUS, unremarkable, evenly lit by flat window light, the expression neutral and unperformed with the eyes cast downward and NOT DIRECTED AT THE CAMERA. Ordinary short hair, an ordinary plain shirt, no styling, no retouching. The kitchen behind him is soft: cabinets, a kettle, a window [STYLE] Avoid: [NEG], fingers fused into one mass, fingers merged, webbed fingers, mitten hand, stub fingers, missing thumb, extra fingers, six fingers, malformed hand, interlocked fingers, raised hand, hand held up in the air, blurred hand, looking at the camera, smiling for the camera, model look, retouched skin, studio lighting, celebrity resemblance

**Save as:** `H:\pd-media\assets\ai\ramirez\R080.png`

**`[NEG]` addition:** append `, fingers fused into one mass, fingers merged, webbed fingers, mitten hand, stub fingers, missing thumb, extra fingers, six fingers, malformed hand, interlocked fingers, raised hand, hand held up in the air, blurred hand, looking at the camera, smiling for the camera, model look, retouched skin, studio lighting, celebrity resemblance` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R081.png`

**Lands on:** "Neither one told him how to dispute anything." · **ledger** SR-10

- `R081.png`
[HSTYLE] photographic, 35mm, natural light, real adults, ordinary clothing, ordinary bodies, believable American setting, candid framing, no styling, no beauty retouching, no model look, no stock-photo smiles, faces neutral and unremarkable, nobody looking at the lens. The same ordinary American kitchen, the same table and the same flat morning window light, NOW WITH NOBODY IN IT: the chair he was sitting in stands empty and pushed back at an angle, the table bare in front of it. Same camera position, same height, same lens. Nothing on the table, no person anywhere in the frame [STYLE] Avoid: [NEG], fingers fused into one mass, fingers merged, webbed fingers, mitten hand, stub fingers, missing thumb, extra fingers, six fingers, malformed hand, interlocked fingers, raised hand, hand held up in the air, blurred hand, person, silhouette in the doorway, object on the table

**Save as:** `H:\pd-media\assets\ai\ramirez\R081.png`

**`[NEG]` addition:** append `, fingers fused into one mass, fingers merged, webbed fingers, mitten hand, stub fingers, missing thumb, extra fingers, six fingers, malformed hand, interlocked fingers, raised hand, hand held up in the air, blurred hand, person, silhouette in the doorway, object on the table` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R082.png`

**Lands on:** "The Supreme Court says he consulted a lawyer …" · **ledger** SR-11

- `R082.png`
[HSTYLE] photographic, 35mm, natural light, real adults, ordinary clothing, ordinary bodies, believable American setting, candid framing, no styling, no beauty retouching, no model look, no stock-photo smiles, faces neutral and unremarkable, nobody looking at the lens. A hand holding a corded telephone handset clamped against a shoulder and an ear, framed tight from the collarbone up to the jaw ONLY — the chin, the mouth and everything above them are OUTSIDE THE TOP OF THE FRAME AND NOT VISIBLE. The hand steadies the handset from below with the four fingers side by side and separate along its length, each with its own nail, and the thumb apart on the near side. An ordinary shirt collar, ordinary skin, soft interior light from the left [STYLE] Avoid: [NEG], fingers fused into one mass, fingers merged, webbed fingers, mitten hand, stub fingers, missing thumb, extra fingers, six fingers, malformed hand, interlocked fingers, raised hand, hand held up in the air, blurred hand, face, mouth, chin, readable screen, spreadsheet on a monitor, web page, icons, cursor, user interface, mobile phone, brand on the handset

**Save as:** `H:\pd-media\assets\ai\ramirez\R082.png`

**`[NEG]` addition:** append `, fingers fused into one mass, fingers merged, webbed fingers, mitten hand, stub fingers, missing thumb, extra fingers, six fingers, malformed hand, interlocked fingers, raised hand, hand held up in the air, blurred hand, face, mouth, chin, readable screen, spreadsheet on a monitor, web page, icons, cursor, user interface, mobile phone, brand on the handset` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R083.png`

**Lands on:** "Beginning in 2002, TransUnion introduced an add-on product called OFAC Name Screen Alert." · **ledger** LS-13

- `R083.png`
[HSTYLE] photographic, 35mm, natural light, real adults, ordinary clothing, ordinary bodies, believable American setting, candid framing, no styling, no beauty retouching, no model look, no stock-photo smiles, faces neutral and unremarkable, nobody looking at the lens. AN INVENTED, COMPLETELY FICTIONAL woman in her thirties at an ordinary office desk, mid-shot from across the desk at seated height: HER FACE IS VISIBLE AND IN FOCUS, plain and unremarkable, LOOKING DOWN AT HER WORK AND NOT AT THE CAMERA, the expression neutral and unperformed. Ordinary work clothes, ordinary hair, no styling and no retouching. Her hands rest down on the desk with the fingers separate. The monitor beside her is turned away. The screen is never legible: it is a single soft bloom of even light with no icons, no windows, no rows, no cursor and nothing that could be read as a document. A plain open-plan office soft behind her [STYLE] Avoid: [NEG], fingers fused into one mass, fingers merged, webbed fingers, mitten hand, stub fingers, missing thumb, extra fingers, six fingers, malformed hand, interlocked fingers, raised hand, hand held up in the air, blurred hand, readable screen, spreadsheet on a monitor, web page, icons, cursor, user interface, looking at the camera, smiling for the camera, model look, retouched skin, headset, lanyard with a printed badge

**Save as:** `H:\pd-media\assets\ai\ramirez\R083.png`

**`[NEG]` addition:** append `, fingers fused into one mass, fingers merged, webbed fingers, mitten hand, stub fingers, missing thumb, extra fingers, six fingers, malformed hand, interlocked fingers, raised hand, hand held up in the air, blurred hand, readable screen, spreadsheet on a monitor, web page, icons, cursor, user interface, looking at the camera, smiling for the camera, model look, retouched skin, headset, lanyard with a printed badge` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R084.png`

**Lands on:** "Accuity's software conducted a name-only search …" · **ledger** LS-16

- `R084.png`
[HSTYLE] photographic, 35mm, natural light, real adults, ordinary clothing, ordinary bodies, believable American setting, candid framing, no styling, no beauty retouching, no model look, no stock-photo smiles, faces neutral and unremarkable, nobody looking at the lens. A pair of hands at a keyboard in a dim open-plan office, framed from just behind and above the hands with the body out of frame: BOTH PALMS ARE DOWN AND IN CONTACT WITH THE DESK AND THE KEYS, all eight fingers side by side and separate with a line of shadow between each pair and both thumbs clearly apart, the keycaps blank and unmarked. Behind and above the hands, four or five empty desks recede into soft focus and low light. THE SCREEN IS NOT IN THE FRAME [STYLE] Avoid: [NEG], fingers fused into one mass, fingers merged, webbed fingers, mitten hand, stub fingers, missing thumb, extra fingers, six fingers, malformed hand, interlocked fingers, raised hand, hand held up in the air, blurred hand, readable screen, spreadsheet on a monitor, web page, icons, cursor, user interface, letters on the keycaps, hands typing in mid-air, face, person at a far desk in focus

**Save as:** `H:\pd-media\assets\ai\ramirez\R084.png`

**`[NEG]` addition:** append `, fingers fused into one mass, fingers merged, webbed fingers, mitten hand, stub fingers, missing thumb, extra fingers, six fingers, malformed hand, interlocked fingers, raised hand, hand held up in the air, blurred hand, readable screen, spreadsheet on a monitor, web page, icons, cursor, user interface, letters on the keycaps, hands typing in mid-air, face, person at a far desk in focus` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R085.png`

**Lands on:** "TransUnion sent the same OFAC letter to eight thousand, one hundred and eighty-four other consumers …" · **ledger** SR-13

- `R085.png`
[HSTYLE] photographic, 35mm, natural light, real adults, ordinary clothing, ordinary bodies, believable American setting, candid framing, no styling, no beauty retouching, no model look, no stock-photo smiles, faces neutral and unremarkable, nobody looking at the lens. About EIGHT ordinary adults walking along a city pavement in daylight, photographed from across the street at standing height with a long lens so the whole group is compressed and NOBODY IS IN FOCUS — every face is soft and unresolvable, mixed ages, mixed heights, ordinary weekday clothes, some walking toward the camera and some away. A plain shopfront run behind them with no readable signage. Flat overcast daylight [STYLE] Avoid: [NEG], fingers fused into one mass, fingers merged, webbed fingers, mitten hand, stub fingers, missing thumb, extra fingers, six fingers, malformed hand, interlocked fingers, raised hand, hand held up in the air, blurred hand, sharp face, portrait, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, shop signage, brand logo, crowd of hundreds

**Save as:** `H:\pd-media\assets\ai\ramirez\R085.png`

**`[NEG]` addition:** append `, fingers fused into one mass, fingers merged, webbed fingers, mitten hand, stub fingers, missing thumb, extra fingers, six fingers, malformed hand, interlocked fingers, raised hand, hand held up in the air, blurred hand, sharp face, portrait, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, shop signage, brand logo, crowd of hundreds` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R086.png`

**Lands on:** "The parties stipulated that the class contained eight thousand, one hundred and eighty-five members …" · **ledger** MN-02

- `R086.png`
[HSTYLE] photographic, 35mm, natural light, real adults, ordinary clothing, ordinary bodies, believable American setting, candid framing, no styling, no beauty retouching, no model look, no stock-photo smiles, faces neutral and unremarkable, nobody looking at the lens. A CROWD OF ABOUT FORTY ordinary adults crossing a wide city street on a marked crossing, photographed from a high angle two floors up looking down, so the people read as a field of heads, shoulders and shortened bodies and NO FACE IS RESOLVABLE ANYWHERE IN THE FRAME. The crossing stripes make plain pale bars under them. Mixed ages, ordinary clothes, flat overcast daylight. No banners, nothing carried, nobody looking up [STYLE] Avoid: [NEG], fingers fused into one mass, fingers merged, webbed fingers, mitten hand, stub fingers, missing thumb, extra fingers, six fingers, malformed hand, interlocked fingers, raised hand, hand held up in the air, blurred hand, sharp face, upturned face, banner, placard, protest, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words

**Save as:** `H:\pd-media\assets\ai\ramirez\R086.png`

**`[NEG]` addition:** append `, fingers fused into one mass, fingers merged, webbed fingers, mitten hand, stub fingers, missing thumb, extra fingers, six fingers, malformed hand, interlocked fingers, raised hand, hand held up in the air, blurred hand, sharp face, upturned face, banner, placard, protest, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R087.png`

**Lands on:** "only one thousand, eight hundred and fifty-three of them" · **ledger** MN-02

- `R087.png`
[HSTYLE] photographic, 35mm, natural light, real adults, ordinary clothing, ordinary bodies, believable American setting, candid framing, no styling, no beauty retouching, no model look, no stock-photo smiles, faces neutral and unremarkable, nobody looking at the lens. AN INVENTED, COMPLETELY FICTIONAL man in his sixties seated alone on a row of plain chairs in a bare institutional corridor, mid-shot from the side and slightly in front at seated eye height: HIS FACE IS VISIBLE, ordinary, tired, entirely neutral, LOOKING ALONG THE CORRIDOR AND NOT AT THE CAMERA. BOTH HANDS REST FLAT AND SEPARATE ON HIS OWN KNEES, one on each knee, palms down, THE FINGERS OF EACH HAND SIDE BY SIDE AND APART, NOT CLASPED AND NOT INTERLOCKED. Plain painted walls, a hard floor, even daylight from a window out of frame [STYLE] Avoid: [NEG], fingers fused into one mass, fingers merged, webbed fingers, mitten hand, stub fingers, missing thumb, extra fingers, six fingers, malformed hand, interlocked fingers, raised hand, hand held up in the air, blurred hand, clasped hands, interlocked fingers, hands folded together, looking at the camera, model look, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, courtroom, judge's bench, jury box, witness stand, gavel, scales of justice, state seal, carved motto, engraved lettering on stone, banner, memorial plaque

**Save as:** `H:\pd-media\assets\ai\ramirez\R087.png`

**`[NEG]` addition:** append `, fingers fused into one mass, fingers merged, webbed fingers, mitten hand, stub fingers, missing thumb, extra fingers, six fingers, malformed hand, interlocked fingers, raised hand, hand held up in the air, blurred hand, clasped hands, interlocked fingers, hands folded together, looking at the camera, model look, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, courtroom, judge's bench, jury box, witness stand, gavel, scales of justice, state seal, carved motto, engraved lettering on stone, banner, memorial plaque` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R088.png`

**Lands on:** "The trial ran six days." · **ledger** MN-04

- `R088.png`
[HSTYLE] photographic, 35mm, natural light, real adults, ordinary clothing, ordinary bodies, believable American setting, candid framing, no styling, no beauty retouching, no model look, no stock-photo smiles, faces neutral and unremarkable, nobody looking at the lens. TWELVE pairs of shoes and lower legs in a row of waiting-room chairs, photographed from knee height straight along the row so the frame is a rhythm of feet, ankles and chair legs and NOTHING ABOVE THE KNEE IS IN THE FRAME. Ordinary worn everyday shoes, mixed styles, some feet flat, some crossed at the ankle. A hard-wearing floor and the plain steel chair frame running through the picture. Even overhead light [STYLE] Avoid: [NEG], fingers fused into one mass, fingers merged, webbed fingers, mitten hand, stub fingers, missing thumb, extra fingers, six fingers, malformed hand, interlocked fingers, raised hand, hand held up in the air, blurred hand, face, torso, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, uniform boots, courtroom, judge's bench, jury box, witness stand, gavel, scales of justice, state seal, carved motto, engraved lettering on stone, banner, memorial plaque

**Save as:** `H:\pd-media\assets\ai\ramirez\R088.png`

**`[NEG]` addition:** append `, fingers fused into one mass, fingers merged, webbed fingers, mitten hand, stub fingers, missing thumb, extra fingers, six fingers, malformed hand, interlocked fingers, raised hand, hand held up in the air, blurred hand, face, torso, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, uniform boots, courtroom, judge's bench, jury box, witness stand, gavel, scales of justice, state seal, carved motto, engraved lettering on stone, banner, memorial plaque` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R089.png`

**Lands on:** "Ramirez testified about what happened at the dealership." · **ledger** SR-15

- `R089.png`
[HSTYLE] photographic, 35mm, natural light, real adults, ordinary clothing, ordinary bodies, believable American setting, candid framing, no styling, no beauty retouching, no model look, no stock-photo smiles, faces neutral and unremarkable, nobody looking at the lens. Two adults' hands on a plain table with a stack of paper between them, framed from directly above with both bodies out of the frame: THE NEAR HAND LIES FLAT ON THE TABLE WITH ITS FINGERTIPS AGAINST THE EDGE OF THE STACK, palm down and in full contact with the surface, four fingers side by side and separate, and THE FAR HAND ALSO LIES FLAT ON THE TABLE just beyond the stack, waiting, its four fingers likewise separate. Every finger on both hands shows its own nail and its own shadow. The paper carries no writing of any kind, and this is what is on it instead: EVENLY SPACED FLAT GREY HORIZONTAL BARS of one uniform width and one uniform weight, laid in parallel like ruled bands of tone, each bar a solid unbroken block of soft grey with straight ends and no letter shapes, no word shapes, no gaps between words and no broken or ragged edge anywhere along it, so the sheet reads as printed matter purely by its rhythm of grey and white and carries not one readable character — and that is the top sheet of the stack. Even soft light [STYLE] Avoid: [NEG], fingers fused into one mass, fingers merged, webbed fingers, mitten hand, stub fingers, missing thumb, extra fingers, six fingers, malformed hand, interlocked fingers, raised hand, hand held up in the air, blurred hand, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, hands raised, handshake, pointing finger, printed report, signature

**Save as:** `H:\pd-media\assets\ai\ramirez\R089.png`

**`[NEG]` addition:** append `, fingers fused into one mass, fingers merged, webbed fingers, mitten hand, stub fingers, missing thumb, extra fingers, six fingers, malformed hand, interlocked fingers, raised hand, hand held up in the air, blurred hand, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, hands raised, handshake, pointing finger, printed report, signature` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R090.png`

**Lands on:** "The plaintiffs did not present any evidence that those class members even knew …" · **ledger** HD-10

- `R090.png`
[HSTYLE] photographic, 35mm, natural light, real adults, ordinary clothing, ordinary bodies, believable American setting, candid framing, no styling, no beauty retouching, no model look, no stock-photo smiles, faces neutral and unremarkable, nobody looking at the lens. AN INVENTED, COMPLETELY FICTIONAL woman in her fifties standing on the porch of an ordinary American suburban house, mid-shot from the front at eye height about ten feet away: HER FACE IS VISIBLE AND IN FOCUS, ordinary and unremarkable, neutral, LOOKING OFF TO ONE SIDE OF THE FRAME AND NOT AT THE CAMERA. Her arms are folded across her front with each hand tucked flat under the opposite upper arm so no fingers are extended into the air. An ordinary cardigan, ordinary hair, no styling and no retouching. Flat overcast daylight, plain porch boards and a plain door behind her [STYLE] Avoid: [NEG], fingers fused into one mass, fingers merged, webbed fingers, mitten hand, stub fingers, missing thumb, extra fingers, six fingers, malformed hand, interlocked fingers, raised hand, hand held up in the air, blurred hand, looking at the camera, smiling for the camera, model look, retouched skin, house numbers, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words

**Save as:** `H:\pd-media\assets\ai\ramirez\R090.png`

**`[NEG]` addition:** append `, fingers fused into one mass, fingers merged, webbed fingers, mitten hand, stub fingers, missing thumb, extra fingers, six fingers, malformed hand, interlocked fingers, raised hand, hand held up in the air, blurred hand, looking at the camera, smiling for the camera, model look, retouched skin, house numbers, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R091.png`

**Lands on:** "many of them would first learn that they were injured when they received a check" · **ledger** HD-10

- `R091.png`
[HSTYLE] photographic, 35mm, natural light, real adults, ordinary clothing, ordinary bodies, believable American setting, candid framing, no styling, no beauty retouching, no model look, no stock-photo smiles, faces neutral and unremarkable, nobody looking at the lens. An ordinary American family kitchen at night WITH NOBODY IN IT, photographed square on from the far side of the room at standing height: the overhead light off, one small warm lamp or under-cupboard light on somewhere to the left, a window black behind the sink, TWO CHAIRS PULLED OUT FROM THE TABLE AND LEFT ASKEW, the table bare. Shadow everywhere but never crushed — every corner still holds its detail. No person, no reflection of a person [STYLE] Avoid: [NEG], fingers fused into one mass, fingers merged, webbed fingers, mitten hand, stub fingers, missing thumb, extra fingers, six fingers, malformed hand, interlocked fingers, raised hand, hand held up in the air, blurred hand, person, silhouette, crushed black shadow, readable screen, spreadsheet on a monitor, web page, icons, cursor, user interface, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words

**Save as:** `H:\pd-media\assets\ai\ramirez\R091.png`

**`[NEG]` addition:** append `, fingers fused into one mass, fingers merged, webbed fingers, mitten hand, stub fingers, missing thumb, extra fingers, six fingers, malformed hand, interlocked fingers, raised hand, hand held up in the air, blurred hand, person, silhouette, crushed black shadow, readable screen, spreadsheet on a monitor, web page, icons, cursor, user interface, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R092.png`

**Lands on:** "Justice Thomas wrote first, for himself and three colleagues …" · **ledger** TH-01

- `R092.png`
[HSTYLE] photographic, 35mm, natural light, real adults, ordinary clothing, ordinary bodies, believable American setting, candid framing, no styling, no beauty retouching, no model look, no stock-photo smiles, faces neutral and unremarkable, nobody looking at the lens. A man in a plain overcoat standing on broad stone civic steps, seen FROM BEHIND AND SLIGHTLY TO ONE SIDE at three-quarters so that only the very edge of his cheek and jaw is visible and NO FEATURE OF HIS FACE CAN BE MADE OUT, framed from the knees up and placed left of centre, one hand hanging at his side with the fingers loosely separate and the other in his coat pocket. He is looking away up the steps. A plain city street soft and grey behind and below. Flat overcast daylight [STYLE] Avoid: [NEG], fingers fused into one mass, fingers merged, webbed fingers, mitten hand, stub fingers, missing thumb, extra fingers, six fingers, malformed hand, interlocked fingers, raised hand, hand held up in the air, blurred hand, face, profile, turned head, briefcase with a logo, courtroom, judge's bench, jury box, witness stand, gavel, scales of justice, state seal, carved motto, engraved lettering on stone, banner, memorial plaque, European streetscape, Irish town, Georgian doorway, EU number plate, foreign-language signage, cobbled lane, thatched roof, tram

**Save as:** `H:\pd-media\assets\ai\ramirez\R092.png`

**`[NEG]` addition:** append `, fingers fused into one mass, fingers merged, webbed fingers, mitten hand, stub fingers, missing thumb, extra fingers, six fingers, malformed hand, interlocked fingers, raised hand, hand held up in the air, blurred hand, face, profile, turned head, briefcase with a logo, courtroom, judge's bench, jury box, witness stand, gavel, scales of justice, state seal, carved motto, engraved lettering on stone, banner, memorial plaque, European streetscape, Irish town, Georgian doorway, EU number plate, foreign-language signage, cobbled lane, thatched roof, tram` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R093.png`

**Lands on:** "Think about what that does to the desk-drawer letter." · **ledger** LS-19 · HD-08

- `R093.png`
[HSTYLE] photographic, 35mm, natural light, real adults, ordinary clothing, ordinary bodies, believable American setting, candid framing, no styling, no beauty retouching, no model look, no stock-photo smiles, faces neutral and unremarkable, nobody looking at the lens. One hand at rest on the front of a CLOSED office drawer, photographed close from a low three-quarter angle. THE HAND IS AT REST FLAT ON THE SURFACE, not raised and not held in the air, the palm laid down in full contact with it and the wrist straight, THE FOUR FINGERS LYING SIDE BY SIDE AND SEPARATE with a visible line of shadow between each pair and one nail showing on each, and the thumb clearly apart from the fingers along the near side — here the surface is the flat wooden drawer front itself, the palm laid against it with the fingers hanging down over the brass handle, separate and still, not gripping and not pulling. Mid-forties skin, short unmanicured nails. Soft north light from the left, the desk and the room beyond soft and dim [STYLE] Avoid: [NEG], fingers fused into one mass, fingers merged, webbed fingers, mitten hand, stub fingers, missing thumb, extra fingers, six fingers, malformed hand, interlocked fingers, raised hand, hand held up in the air, blurred hand, gripping the handle, pulling the drawer, drawer open, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words

**Save as:** `H:\pd-media\assets\ai\ramirez\R093.png`

**`[NEG]` addition:** append `, fingers fused into one mass, fingers merged, webbed fingers, mitten hand, stub fingers, missing thumb, extra fingers, six fingers, malformed hand, interlocked fingers, raised hand, hand held up in the air, blurred hand, gripping the handle, pulling the drawer, drawer open, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R094.png`

**Lands on:** "If federal courts are closed to these plaintiffs, state courts are not …" · **ledger** TH-08 · ND-04

- `R094.png`
[HSTYLE] photographic, 35mm, natural light, real adults, ordinary clothing, ordinary bodies, believable American setting, candid framing, no styling, no beauty retouching, no model look, no stock-photo smiles, faces neutral and unremarkable, nobody looking at the lens. TWO INVENTED, COMPLETELY FICTIONAL adults talking in a doorway, mid-shot from about eight feet away at eye height, one standing inside the room and one in the corridor, TURNED TOWARD EACH OTHER IN PROFILE SO NEITHER LOOKS ANYWHERE NEAR THE CAMERA. Both faces are visible in profile, ordinary, mid-conversation and unperformed. Ordinary work clothes. Their hands are down at their sides or resting on the door frame with fingers separate. The door frame makes a hard vertical edge between them. Even flat daylight [STYLE] Avoid: [NEG], fingers fused into one mass, fingers merged, webbed fingers, mitten hand, stub fingers, missing thumb, extra fingers, six fingers, malformed hand, interlocked fingers, raised hand, hand held up in the air, blurred hand, looking at the camera, model look, retouched skin, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, lanyard with a printed badge, courtroom, judge's bench, jury box, witness stand, gavel, scales of justice, state seal, carved motto, engraved lettering on stone, banner, memorial plaque

**Save as:** `H:\pd-media\assets\ai\ramirez\R094.png`

**`[NEG]` addition:** append `, fingers fused into one mass, fingers merged, webbed fingers, mitten hand, stub fingers, missing thumb, extra fingers, six fingers, malformed hand, interlocked fingers, raised hand, hand held up in the air, blurred hand, looking at the camera, model look, retouched skin, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, lanyard with a printed badge, courtroom, judge's bench, jury box, witness stand, gavel, scales of justice, state seal, carved motto, engraved lettering on stone, banner, memorial plaque` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R095.png`

**Lands on:** "Most of them, the majority pointed out, did not know." · **ledger** HD-10

- `R095.png`
[HSTYLE] photographic, 35mm, natural light, real adults, ordinary clothing, ordinary bodies, believable American setting, candid framing, no styling, no beauty retouching, no model look, no stock-photo smiles, faces neutral and unremarkable, nobody looking at the lens. A plain empty office at dusk, photographed from the doorway at standing height: two or three bare desks, a run of low cabinets, one window on the left going deep blue, the overhead lights off so the room is lit only by that window. ONE CHAIR IS TURNED OUT FROM ITS DESK at an angle, as though somebody had just stood up. NOBODY IS IN THE ROOM. Nothing on any desk. Shadow that still holds its detail [STYLE] Avoid: [NEG], fingers fused into one mass, fingers merged, webbed fingers, mitten hand, stub fingers, missing thumb, extra fingers, six fingers, malformed hand, interlocked fingers, raised hand, hand held up in the air, blurred hand, person, silhouette, readable screen, spreadsheet on a monitor, web page, icons, cursor, user interface, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, crushed black shadow

**Save as:** `H:\pd-media\assets\ai\ramirez\R095.png`

**`[NEG]` addition:** append `, fingers fused into one mass, fingers merged, webbed fingers, mitten hand, stub fingers, missing thumb, extra fingers, six fingers, malformed hand, interlocked fingers, raised hand, hand held up in the air, blurred hand, person, silhouette, readable screen, spreadsheet on a monitor, web page, icons, cursor, user interface, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, crushed black shadow` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R096.png`

**Lands on:** "Six thousand, three hundred and thirty-two of them were told … that nothing had happened to them yet." · **ledger** HD-11

- `R096.png`
[HSTYLE] photographic, 35mm, natural light, real adults, ordinary clothing, ordinary bodies, believable American setting, candid framing, no styling, no beauty retouching, no model look, no stock-photo smiles, faces neutral and unremarkable, nobody looking at the lens. A wide of an ordinary American residential street at dusk, photographed from the middle of the road at standing height: single-storey houses either side, driveways, a kerbline running away, the sky above still pale and the street below already dim. THREE SEPARATE PEOPLE are in the frame, ALL FAR AWAY AND ALL FAR APART FROM EACH OTHER — one on each pavement and one at a distant driveway — each no more than a fortieth of the frame height and each reduced to a soft dark shape with no resolvable feature. No house numbers, no street sign, nobody near the camera [STYLE] Avoid: [NEG], fingers fused into one mass, fingers merged, webbed fingers, mitten hand, stub fingers, missing thumb, extra fingers, six fingers, malformed hand, interlocked fingers, raised hand, hand held up in the air, blurred hand, sharp face, person close to the camera, house numbers, street sign, European streetscape, Irish town, Georgian doorway, EU number plate, foreign-language signage, cobbled lane, thatched roof, tram, streetlight flare

**Save as:** `H:\pd-media\assets\ai\ramirez\R096.png`

**`[NEG]` addition:** append `, fingers fused into one mass, fingers merged, webbed fingers, mitten hand, stub fingers, missing thumb, extra fingers, six fingers, malformed hand, interlocked fingers, raised hand, hand held up in the air, blurred hand, sharp face, person close to the camera, house numbers, street sign, European streetscape, Irish town, Georgian doorway, EU number plate, foreign-language signage, cobbled lane, thatched roof, tram, streetlight flare` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

### E · Treasury and the federal register — R097–R104 (8 plates)

*ACT_2 — added at 122; ACT_2 is 23.2% of the narration and the longest act*

#### `R097.png`

**Lands on:** "The list is real, and it belongs to the Treasury." · **ledger** LS-01

- `R097.png`
A plain modern American federal office building photographed square on from across a wide empty pavement in flat overcast light: a heavy flat stone facade, a regular grid of deep-set identical windows, a low set-back entrance under a plain canopy. THE FACADE CARRIES NOTHING AT ALL — no name, no seal, no eagle, no lettering, no flag, no plaque, no notice board. A bare kerb and an empty road across the foreground, nobody in the frame [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, courtroom, judge's bench, jury box, witness stand, gavel, scales of justice, state seal, carved motto, engraved lettering on stone, banner, memorial plaque, European streetscape, Irish town, Georgian doorway, EU number plate, foreign-language signage, cobbled lane, thatched roof, tram, federal seal, eagle, building name, flag, security bollards with markings

**Save as:** `H:\pd-media\assets\ai\ramirez\R097.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, courtroom, judge's bench, jury box, witness stand, gavel, scales of justice, state seal, carved motto, engraved lettering on stone, banner, memorial plaque, European streetscape, Irish town, Georgian doorway, EU number plate, foreign-language signage, cobbled lane, thatched roof, tram, federal seal, eagle, building name, flag, security bollards with markings` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R098.png`

**Lands on:** "Their assets are blocked, and United States persons are generally prohibited from dealing with them." · **ledger** LS-02

- `R098.png`
A single plain metal flagpole standing empty against a flat pale grey overcast sky, photographed from below at a slight angle so the pole runs from the bottom right of the frame up and out of the top: NO FLAG IS ON IT, only the bare halyard hanging slack against the pole and the plain truck and finial at the top. The upper corner of a plain stone building edges into the lower left. No wind, no sun, nobody in frame [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, courtroom, judge's bench, jury box, witness stand, gavel, scales of justice, state seal, carved motto, engraved lettering on stone, banner, memorial plaque, flag, banner, pennant, eagle finial, emblem, European streetscape, Irish town, Georgian doorway, EU number plate, foreign-language signage, cobbled lane, thatched roof, tram

**Save as:** `H:\pd-media\assets\ai\ramirez\R098.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, courtroom, judge's bench, jury box, witness stand, gavel, scales of justice, state seal, carved motto, engraved lettering on stone, banner, memorial plaque, flag, banner, pennant, eagle finial, emblem, European streetscape, Irish town, Georgian doorway, EU number plate, foreign-language signage, cobbled lane, thatched roof, tram` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R099.png`

**Lands on:** "It is generally unlawful to transact business with any person on the list." · **ledger** LS-04

- `R099.png`
An empty wooden lectern standing alone on a low platform in a plain meeting room, photographed square on from eight feet away at standing height. THE FRONT PANEL OF THE LECTERN IS BARE POLISHED WOOD — no seal, no emblem, no crest, no plaque and no lettering on it anywhere. There is no microphone with a branded flag on it, no paper on the reading surface and nobody behind it. A plain curtain or plain painted wall behind, even soft light [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, courtroom, judge's bench, jury box, witness stand, gavel, scales of justice, state seal, carved motto, engraved lettering on stone, banner, memorial plaque, seal on the lectern, crest, microphone flag, flags behind, person

**Save as:** `H:\pd-media\assets\ai\ramirez\R099.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, courtroom, judge's bench, jury box, witness stand, gavel, scales of justice, state seal, carved motto, engraved lettering on stone, banner, memorial plaque, seal on the lectern, crest, microphone flag, flags behind, person` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R100.png`

**Lands on:** "Individuals on the OFAC list are terrorists, drug traffickers, or other serious criminals." · **ledger** LS-04

- `R100.png`
A corridor of identical closed office doors photographed straight down its length at eye height in an ordinary government office building: pale painted walls, a hard-wearing carpet tile floor, six plain flush doors on the left and six on the right, all shut and ALL OF THEM COMPLETELY BARE — no numbers, no nameplates, no signs, no notices, no directory. Even fluorescent light overhead, nobody in the corridor [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, door numbers, nameplate, directory board, exit sign, person, European streetscape, Irish town, Georgian doorway, EU number plate, foreign-language signage, cobbled lane, thatched roof, tram

**Save as:** `H:\pd-media\assets\ai\ramirez\R100.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, door numbers, nameplate, directory board, exit sign, person, European streetscape, Irish town, Georgian doorway, EU number plate, foreign-language signage, cobbled lane, thatched roof, tram` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R101.png`

**Lands on:** "On the eight Treasury pages retrieved for this film, there is no current count of any kind." · **ledger** LS-05

- `R101.png`
A glass-fronted public notice case mounted on a plain painted wall, photographed square on from four feet away, THE CASE COMPLETELY EMPTY: nothing pinned inside it, only the bare green felt board behind the glass, the plain aluminium frame, one small lock, and a soft reflection of the opposite wall sliding across the glass. Nothing readable anywhere. Even corridor light [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, notices pinned inside, posters, printed sheets, headings, reflection of a person

**Save as:** `H:\pd-media\assets\ai\ramirez\R101.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, notices pinned inside, posters, printed sheets, headings, reflection of a person` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R102.png`

**Lands on:** "There is one official figure, from a 2021 sanctions review …" · **ledger** LS-05

- `R102.png`
A shelf of about fifteen identical grey paper-bound official volumes standing upright, photographed square on and close so the row of spines fills the frame: uniform height, uniform width, uniform dull grey board, softly worn at the head and tail. EVERY SPINE IS COMPLETELY BLANK — no titles, no volume numbers, no year, no labels, no gilt. Even soft light from the left, the shelf edge a dark line beneath [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, titles on the spines, volume numbers, year, gilt lettering, library labels

**Save as:** `H:\pd-media\assets\ai\ramirez\R102.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, titles on the spines, volume numbers, year, gilt lettering, library labels` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R103.png`

**Lands on:** "Treasury publishes the list as a data file …" · **ledger** LS-05 · ⛔-11

- `R103.png`
A single aisle in a cold data hall, photographed at eye height with ONE CABINET DOOR STANDING OPEN on the left: inside it, dense ranks of identical dark equipment and a neat bundle of pale cabling dropping down the side, everything else in the aisle closed and identical. No maker's marks, no rack labels, no printed asset tags, no readable status displays anywhere. Hard even overhead light, nobody in the frame [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, readable screen, spreadsheet on a monitor, web page, icons, cursor, user interface, rack labels, asset tags, brand logos, blue neon grade, person

**Save as:** `H:\pd-media\assets\ai\ramirez\R103.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, readable screen, spreadsheet on a monitor, web page, icons, cursor, user interface, rack labels, asset tags, brand logos, blue neon grade, person` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R104.png`

**Lands on:** "That is our count of their file. It is not a Treasury statement …" · **ledger** ⛔-11

- `R104.png`
A plain desk photographed from directly overhead, almost completely empty, with ONE CLOSED GREY RING BINDER lying alone slightly off centre. THE BINDER IS COMPLETELY UNMARKED — a plain grey cover with no title, no label window, no spine card, no printing of any kind — and nothing else is on the desk at all. Even soft light from the left, the desk surface a flat neutral grey-brown [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, label on the binder, spine card, title, sticky notes, pen, hand

**Save as:** `H:\pd-media\assets\ai\ramirez\R104.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, label on the binder, spine card, title, sticky notes, pen, hand` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

### F · 1970 and the statute — R105–R112 (8 plates)

*ACT_3 — added at 122; the script's own ACT_3 header already calls R105–R112*

#### `R105.png`

**Lands on:** "In 1970, Congress passed and President Nixon signed the Fair Credit Reporting Act." · **ledger** MN-09

- `R105.png`
A single plain hardback statute volume lying closed on a wooden desk, photographed from a low three-quarter angle so the cover and the fore-edge are both visible: heavy dark cloth boards, softly bumped corners, a plain sewn head band. THE COVER AND THE SPINE ARE COMPLETELY BLANK — no title, no gilt, no author, no volume number, no library label. One warm desk light from the left, the rest of the desk bare and soft [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, gilt title, spine lettering, library label, embossed crest

**Save as:** `H:\pd-media\assets\ai\ramirez\R105.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, gilt title, spine lettering, library label, embossed crest` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R106.png`

**Lands on:** "it requires a consumer reporting agency to follow reasonable procedures to assure maximum possible accuracy" · **ledger** MN-09

- `R106.png`
The same plain hardback volume lying OPEN at a middle spread on the same desk in the same warm light, photographed from directly overhead so both pages fill the frame. The paper carries no writing of any kind, and this is what is on it instead: EVENLY SPACED FLAT GREY HORIZONTAL BARS of one uniform width and one uniform weight, laid in parallel like ruled bands of tone, each bar a solid unbroken block of soft grey with straight ends and no letter shapes, no word shapes, no gaps between words and no broken or ragged edge anywhere along it, so the sheet reads as printed matter purely by its rhythm of grey and white and carries not one readable character — each page carries two justified columns of the flat grey bars and nothing else: no headings, no page numbers, no section marks, no footnotes, no marginal notes. The gutter shadow runs down the middle and the paper is warm off-white [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, printed columns of text, section numbers, page numbers, footnotes, marginalia, highlighter

**Save as:** `H:\pd-media\assets\ai\ramirez\R106.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, printed columns of text, section numbers, page numbers, footnotes, marginalia, highlighter` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R107.png`

**Lands on:** "… when the data is an OFAC alert, had been said out loud once already." · **ledger** N9-01

- `R107.png`
An empty committee room photographed from the back at standing height: one long plain table across the far end, a curved run of plain chairs behind it, rows of plain public seating in the foreground, tall windows down the left throwing flat daylight across the carpet. THE ROOM IS COMPLETELY EMPTY — nobody in any seat, nothing on the table, no name cards, no microphones with branded flags, no seal on the wall, no lettering anywhere [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, courtroom, judge's bench, jury box, witness stand, gavel, scales of justice, state seal, carved motto, engraved lettering on stone, banner, memorial plaque, name cards, seal on the wall, microphone flags, person, flags

**Save as:** `H:\pd-media\assets\ai\ramirez\R107.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, courtroom, judge's bench, jury box, witness stand, gavel, scales of justice, state seal, carved motto, engraved lettering on stone, banner, memorial plaque, name cards, seal on the wall, microphone flags, person, flags` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R108.png`

**Lands on:** "In 2005, a consumer sued." · **ledger** TH-04

- `R108.png`
A green-shaded desk lamp switched on over a wooden desk in an otherwise dark office, photographed from a seated three-quarter angle: the lamp throws one warm pool of light onto a plain leather blotter and falls away fast into shadow that still holds its detail. THE BLOTTER IS COMPLETELY EMPTY — no paper, no pen, no book, nothing in the pool of light at all. Nobody in the room [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, papers on the desk, open book, pen, person, crushed black shadow

**Save as:** `H:\pd-media\assets\ai\ramirez\R108.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, papers on the desk, open book, pen, person, crushed black shadow` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R109.png`

**Lands on:** "TransUnion had sold an OFAC credit report about her to a car dealership." · **ledger** TH-04

- `R109.png`
A tall stack of folded continuous fanfold paper standing on a plain floor beside a desk, photographed from a low angle so the stack rises through most of the frame and the concertina edges and sprocket margins step up it like a ladder. The paper carries no writing of any kind, and this is what is on it instead: EVENLY SPACED FLAT GREY HORIZONTAL BARS of one uniform width and one uniform weight, laid in parallel like ruled bands of tone, each bar a solid unbroken block of soft grey with straight ends and no letter shapes, no word shapes, no gaps between words and no broken or ragged edge anywhere along it, so the sheet reads as printed matter purely by its rhythm of grey and white and carries not one readable character — visible on the top sheet and faintly through the fold edges. Cool even office light, the wall behind plain and bare [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, printed figures, column headings, dot matrix text, tractor labels

**Save as:** `H:\pd-media\assets\ai\ramirez\R109.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, printed figures, column headings, dot matrix text, tractor labels` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R110.png`

**Lands on:** "Twenty-seven years apart." · **ledger** TH-04

- `R110.png`
TWO identical paper wall calendars hanging SIDE BY SIDE on a plain painted wall, photographed square on from six feet away with the focus set on the wall so both calendars are SOFT AND OUT OF FOCUS: each reads only as a pale rectangle with a blurred grid of grey squares, and NO DIGIT, NO MONTH NAME AND NO WEEKDAY LETTER is resolvable on either of them. A clear gap of bare wall between the two. Even daylight from the left [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, readable numbers, month names, sharp calendar, photograph on the calendar, circled date

**Save as:** `H:\pd-media\assets\ai\ramirez\R110.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, readable numbers, month names, sharp calendar, photograph on the calendar, circled date` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R111.png`

**Lands on:** "in August 2010 the Third Circuit affirmed that" · **ledger** TH-04 · N9-02

- `R111.png`
A plain heavy exterior door of a civic office building, closed, photographed square on from four feet away: dark painted timber, a broad brass kick plate at the foot polished bright by boots, a plain brass pull handle, a plain stone surround. THE DOOR AND THE KICK PLATE AND THE SURROUND ARE ALL BLANK — no name, no numbers, no opening hours, no seal, no plaque, no notice taped to the glass. Flat overcast light [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, courtroom, judge's bench, jury box, witness stand, gavel, scales of justice, state seal, carved motto, engraved lettering on stone, banner, memorial plaque, opening hours, door number, nameplate, notice, seal, European streetscape, Irish town, Georgian doorway, EU number plate, foreign-language signage, cobbled lane, thatched roof, tram

**Save as:** `H:\pd-media\assets\ai\ramirez\R111.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, courtroom, judge's bench, jury box, witness stand, gavel, scales of justice, state seal, carved motto, engraved lettering on stone, banner, memorial plaque, opening hours, door number, nameplate, notice, seal, European streetscape, Irish town, Georgian doorway, EU number plate, foreign-language signage, cobbled lane, thatched roof, tram` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R112.png`

**Lands on:** "Despite this warning, TransUnion continued to use problematic matching technology …" · **ledger** N9-03

- `R112.png`
An open stone stairwell photographed from the bottom looking straight up, so three flights of plain stone steps and their plain iron balustrades spiral away above the camera and make a receding rectangular well with a pale skylight at the very top. Every surface is plain — no signs, no floor numbers, no arrows, no notices. Cool daylight falling down the well, nobody on any flight [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, courtroom, judge's bench, jury box, witness stand, gavel, scales of justice, state seal, carved motto, engraved lettering on stone, banner, memorial plaque, floor numbers, arrows, signs, person, vertigo fisheye distortion

**Save as:** `H:\pd-media\assets\ai\ramirez\R112.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, courtroom, judge's bench, jury box, witness stand, gavel, scales of justice, state seal, carved motto, engraved lettering on stone, banner, memorial plaque, floor numbers, arrows, signs, person, vertigo fisheye distortion` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

### G · the law, ACT_4 and ACT_5 — R113–R122 (10 plates)

*ACT_4 / ACT_5 — added at 122; those two acts are 35.5% of the narration and owned only four dedicated plates each*

#### `R113.png`

**Lands on:** "Congress can write a law that says a company owes you something." · **ledger** HD-05 · HD-14

- `R113.png`
A tall narrow window set in a deep stone reveal, photographed from inside a plain room at eye height and slightly to one side, so the thickness of the wall is the subject: the splayed reveal runs back to a small bright pane and ONE SHAFT OF LIGHT lies along the stone sill and spills a little way onto the floor. The glass is plain and blown out to white. No furniture, no lettering, nobody in the room [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, courtroom, judge's bench, jury box, witness stand, gavel, scales of justice, state seal, carved motto, engraved lettering on stone, banner, memorial plaque, stained glass, crest, person, crushed black shadow

**Save as:** `H:\pd-media\assets\ai\ramirez\R113.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, courtroom, judge's bench, jury box, witness stand, gavel, scales of justice, state seal, carved motto, engraved lettering on stone, banner, memorial plaque, stained glass, crest, person, crushed black shadow` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R114.png`

**Lands on:** "So where is the line?" · **ledger** HD-06

- `R114.png`
A pair of tall panelled doors, CLOSED, photographed dead square on from ten feet away so they fill the frame symmetrically: dark polished timber, six deep recessed panels each, a plain brass ring handle on each leaf, a plain stone architrave around them. THE DOORS ARE COMPLETELY BARE — no lettering, no numbers, no nameplates, no notices, no crest above them. Low side light so one leaf is a stop brighter than the other [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, courtroom, judge's bench, jury box, witness stand, gavel, scales of justice, state seal, carved motto, engraved lettering on stone, banner, memorial plaque, lettering above the doors, crest, nameplate, notice, person

**Save as:** `H:\pd-media\assets\ai\ramirez\R114.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, courtroom, judge's bench, jury box, witness stand, gavel, scales of justice, state seal, carved motto, engraved lettering on stone, banner, memorial plaque, lettering above the doors, crest, nameplate, notice, person` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R115.png`

**Lands on:** "distinguishes between credit files that consumer reporting agencies maintain internally, and the consumer credit reports that consumer reporting agencies disseminate to third-party creditors" · **ledger** HD-06

- `R115.png`
An interior stone archway framing A SECOND, SMALLER ARCHWAY BEYOND IT, photographed dead square on down the axis so the two openings sit one inside the other like a diagram of inside and outside: the near arch is dark and close, the far arch is smaller, paler and full of flat daylight. Both spaces are completely empty — no furniture, no people, no signage, no carving on either arch [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, courtroom, judge's bench, jury box, witness stand, gavel, scales of justice, state seal, carved motto, engraved lettering on stone, banner, memorial plaque, statue in the archway, carving, inscription, person

**Save as:** `H:\pd-media\assets\ai\ramirez\R115.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, courtroom, judge's bench, jury box, witness stand, gavel, scales of justice, state seal, carved motto, engraved lettering on stone, banner, memorial plaque, statue in the archway, carving, inscription, person` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R116.png`

**Lands on:** "The mere presence of an inaccuracy in an internal credit file, if it is not disclosed to a third party, causes no concrete harm." · **ledger** HD-07

- `R116.png`
A bare plastered wall meeting a stone floor, photographed close and square on so the frame is almost abstract: two thirds pale wall, one third grey stone, one dark horizontal line where they meet, and ONE HARD DIAGONAL EDGE OF SUNLIGHT cutting across both from the upper left. Nothing else is in the frame — no skirting detail, no socket, no mark, no object, nobody [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, courtroom, judge's bench, jury box, witness stand, gavel, scales of justice, state seal, carved motto, engraved lettering on stone, banner, memorial plaque, furniture, socket, sign, person, graffiti

**Save as:** `H:\pd-media\assets\ai\ramirez\R116.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, courtroom, judge's bench, jury box, witness stand, gavel, scales of justice, state seal, carved motto, engraved lettering on stone, banner, memorial plaque, furniture, socket, sign, person, graffiti` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R117.png`

**Lands on:** "What about the risk that it would be sent later?" · **ledger** HD-09

- `R117.png`
A plain stone bench set into a shallow alcove in a stone wall, photographed from a three-quarter angle six feet away: the seat is worn hollow in the middle by long use, the alcove is plain with no carving and no plaque, and hard side light from the left rakes across the stone and throws the bench's shadow onto the floor. Nobody sitting on it and nothing left on it [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, courtroom, judge's bench, jury box, witness stand, gavel, scales of justice, state seal, carved motto, engraved lettering on stone, banner, memorial plaque, plaque, inscription, person, coat on the bench

**Save as:** `H:\pd-media\assets\ai\ramirez\R117.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, courtroom, judge's bench, jury box, witness stand, gavel, scales of justice, state seal, carved motto, engraved lettering on stone, banner, memorial plaque, plaque, inscription, person, coat on the bench` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R118.png`

**Lands on:** "So the eight thousand, one hundred and eighty-five split in two." · **ledger** HD-11

- `R118.png`
A wide flight of stone steps photographed FROM ABOVE looking straight down them, so the treads make a stack of horizontal bands running to the bottom of the frame: the stone is worn unevenly, deeper in two lanes where people walk and untouched at the edges, and flat overcast light makes every nosing read as a fine dark line. The steps are completely empty [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, courtroom, judge's bench, jury box, witness stand, gavel, scales of justice, state seal, carved motto, engraved lettering on stone, banner, memorial plaque, person, handrail shadow shaped like letters, painted markings, hazard stripes

**Save as:** `H:\pd-media\assets\ai\ramirez\R118.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, courtroom, judge's bench, jury box, witness stand, gavel, scales of justice, state seal, carved motto, engraved lettering on stone, banner, memorial plaque, person, handrail shadow shaped like letters, painted markings, hazard stripes` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R119.png`

**Lands on:** "The judgment below was reversed, and the case was remanded for further proceedings." · **ledger** HD-12

- `R119.png`
A plain interior balcony rail on an upper floor, photographed from behind the rail looking down and out over an empty stone hall below: the rail runs across the lower third of the frame as a strong horizontal, the floor of the hall lies far below with one shaft of window light across it, and NOBODY IS ANYWHERE IN THE HALL. The rail and the balustrade are plain with no motif and no lettering [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, courtroom, judge's bench, jury box, witness stand, gavel, scales of justice, state seal, carved motto, engraved lettering on stone, banner, memorial plaque, person below, inlaid seal in the floor, banner, sculpture

**Save as:** `H:\pd-media\assets\ai\ramirez\R119.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, courtroom, judge's bench, jury box, witness stand, gavel, scales of justice, state seal, carved motto, engraved lettering on stone, banner, memorial plaque, person below, inlaid seal in the floor, banner, sculpture` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R120.png`

**Lands on:** "It would be very easy to make the majority sound stupid here, and it was not." · **ledger** HD-10

- `R120.png`
A shuttered window in a dark panelled room, photographed square on from six feet away: the louvred shutters are almost closed and lay a ladder of hard bright slats across the dark wood panelling to the right of the window and across the floor. The panelling is plain, the shadow detail holds everywhere, and there is no furniture, no picture on the wall, no lettering and nobody in the room [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, courtroom, judge's bench, jury box, witness stand, gavel, scales of justice, state seal, carved motto, engraved lettering on stone, banner, memorial plaque, portrait on the wall, framed picture, person, crushed black shadow, venetian blind noir cliche with smoke

**Save as:** `H:\pd-media\assets\ai\ramirez\R120.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, courtroom, judge's bench, jury box, witness stand, gavel, scales of justice, state seal, carved motto, engraved lettering on stone, banner, memorial plaque, portrait on the wall, framed picture, person, crushed black shadow, venetian blind noir cliche with smoke` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R121.png`

**Lands on:** "Justice Kagan wrote separately, and shorter." · **ledger** KG-01

- `R121.png`
A single reading lamp lit on a side table in an otherwise dark panelled room, photographed from a standing three-quarter angle: the lamp throws a warm pool onto the table and the arm of an empty upholstered chair beside it, and the rest of the room falls away into shadow that still holds its grain and its edges. THE TABLE IS EMPTY and the chair is empty. Nobody in the room [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, book on the table, papers, person, crushed black shadow, portrait on the wall

**Save as:** `H:\pd-media\assets\ai\ramirez\R121.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, book on the table, papers, person, crushed black shadow, portrait on the wall` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

#### `R122.png`

**Lands on:** "It did not decide what would have happened in a suit for an injunction rather than damages." · **ledger** ND-05

- `R122.png`
A stone threshold seen from INSIDE a dark room, the heavy door standing wide open onto flat grey daylight so the doorway is a bright rectangle and the worn stone sill is the brightest thing in the lower frame: WHAT IS BEYOND THE DOOR IS BLOWN OUT AND FEATURELESS — no street, no building, no figure, nothing resolvable at all, only even white light. The door leaf and the jamb are plain with no lettering. Nobody in the frame [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, courtroom, judge's bench, jury box, witness stand, gavel, scales of justice, state seal, carved motto, engraved lettering on stone, banner, memorial plaque, view of a street, figure in the doorway, silhouette, sign on the door

**Save as:** `H:\pd-media\assets\ai\ramirez\R122.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, courtroom, judge's bench, jury box, witness stand, gavel, scales of justice, state seal, carved motto, engraved lettering on stone, banner, memorial plaque, view of a street, figure in the doorway, silhouette, sign on the door` to the canonical `[NEG]`. **Delete nothing from the canonical block.**

## 5. TIER 2 — headroom, 24 plates, R123–R146, **not declared in the spec**

**Generate these.** They are not optional in the sense of "skip them"; they are ordered in this pass so that a rejected tier-1 plate can be swapped for a working one without a second commission round, and so that a longer delivered narration or a raised `distinct_video_assets` does not leave the film short. What they are *not* is **declared**: `episode_spec.v001.json` lists R001–R122 only, because a declared still that lands in no cut fails `check_spec_satisfied.py`.

Every one of them still carries a script line and a ledger row — **a plate with no beat is not commissioned**, headroom or otherwise.

v001 listed R097–R130 as an optional second pass. Here is what happened to each band, so nobody has to guess later:

| v001 optional band | disposition |
|---|---|
| R097–R104 Treasury / federal register | **promoted to tier 1**, lane E |
| R105–R112 1970 and the FCRA | **promoted to tier 1**, lane F — the script's ACT_3 header already called them by name |
| R113–R120 the money, kept abstract | **band reassigned** to lane G (ACT_4 / ACT_5 stone), which is where the shortage measured. The four money plates survive as R123–R126 |
| R121–R126 weather and the four designed silences | **dropped.** The designed silences already have plates written for them — R091 carries ACT_4's four seconds — and a weather plate is the definition of 汎用素材 |
| R127–R130 the cancelled trip | **kept**, as R127–R130 |

### H · the money, and the cancelled trip — R123–R130 (8 plates)

*ACT_1 / ACT_3 / ACT_4 / ACT_5 — headroom tier: ordered, NOT declared*

#### `R123.png` *(tier 2 · not declared)*

**Lands on:** "statutory and punitive damages are available under the Act for willful violations" · **ledger** MN-10

- `R123.png`
A retail bank counter photographed square on from the customer's side at standing height, the counter running across the frame with a plain glass screen above it and an empty teller position behind: everything completely unbranded — no name, no logo, no rate board, no posters, no leaflet stand with printed covers, no numbered ticket display. A plain terminal on the counter is turned away. The screen is never legible: it is a single soft bloom of even light with no icons, no windows, no rows, no cursor and nothing that could be read as a document. Nobody in the frame. Even interior daylight [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, readable screen, spreadsheet on a monitor, web page, icons, cursor, user interface, bank logo, rate board, posters, leaflets with text, queue number display, person

**Save as:** `H:\pd-media\assets\ai\ramirez\R123.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, readable screen, spreadsheet on a monitor, web page, icons, cursor, user interface, bank logo, rate board, posters, leaflets with text, queue number display, person` to the canonical `[NEG]`.

#### `R124.png` *(tier 2 · not declared)*

**Lands on:** "many of them would first learn that they were injured when they received a check" · **ledger** HD-10

- `R124.png`
A single cheque-sized slip of pale paper lying alone on a plain dark surface, photographed from directly overhead so it sits small and precise in the middle of the frame. The paper carries no writing of any kind, and this is what is on it instead: EVENLY SPACED FLAT GREY HORIZONTAL BARS of one uniform width and one uniform weight, laid in parallel like ruled bands of tone, each bar a solid unbroken block of soft grey with straight ends and no letter shapes, no word shapes, no gaps between words and no broken or ragged edge anywhere along it, so the sheet reads as printed matter purely by its rhythm of grey and white and carries not one readable character, in three short groups laid where the lines of a payment slip would be, plus one longer flat grey bar across the foot where a signature would sit. No numbers, no letters, no name, no amount box, no printed border. One soft light from the left [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, amount box, numbers, signature, bank name, printed border, currency symbol

**Save as:** `H:\pd-media\assets\ai\ramirez\R124.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, amount box, numbers, signature, bank name, printed border, currency symbol` to the canonical `[NEG]`.

#### `R125.png` *(tier 2 · not declared)*

**Lands on:** "More than sixty million dollars." · **ledger** MN-04

- `R125.png`
A narrow paper ribbon curling out of a plain mechanical adding machine and falling in a loose spiral onto the desk beneath it, photographed close from a low three-quarter angle with the machine soft behind: THE RIBBON IS COMPLETELY BLANK — plain white paper with no printing, no figures, no rules and no marks anywhere along its length. The machine's keys are unmarked blanks. Warm side light from the left [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, printed figures on the tape, numbers on the keys, brand name on the machine

**Save as:** `H:\pd-media\assets\ai\ramirez\R125.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, printed figures on the tape, numbers on the keys, brand name on the machine` to the canonical `[NEG]`.

#### `R126.png` *(tier 2 · not declared)*

**Lands on:** "And it set no figure." · **ledger** MN-11

- `R126.png`
A paper till roll unspooled across a plain desk in a long loose S, photographed from directly overhead so the whole run of paper is visible: THE PAPER IS COMPLETELY BLANK from the roll to the torn end — no printing, no figures, no lines, no perforation marks. The roll itself sits at the top of the frame, half unwound. Even soft light [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, printed receipt, figures, barcode, dashed lines, totals

**Save as:** `H:\pd-media\assets\ai\ramirez\R126.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, printed receipt, figures, barcode, dashed lines, totals` to the canonical `[NEG]`.

#### `R127.png` *(tier 2 · not declared)*

**Lands on:** "He cancelled a trip he had planned." · **ledger** SR-10

- `R127.png`
An airport departures hall at a quiet hour, photographed from a mezzanine at a shallow downward angle: a wide pale floor, a long line of check-in desks along the right, only five or six travellers spread across the whole space and all of them far off and unresolvable. THE LARGE DISPLAY BOARDS OVERHEAD ARE BLANK PANELS OF EVEN DARK GREY with nothing on them at all, and there is no signage, no airline name and no gate lettering anywhere in the frame [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, readable screen, spreadsheet on a monitor, web page, icons, cursor, user interface, flight information board, airline logo, gate numbers, signage, sharp face, European streetscape, Irish town, Georgian doorway, EU number plate, foreign-language signage, cobbled lane, thatched roof, tram

**Save as:** `H:\pd-media\assets\ai\ramirez\R127.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, readable screen, spreadsheet on a monitor, web page, icons, cursor, user interface, flight information board, airline logo, gate numbers, signage, sharp face, European streetscape, Irish town, Georgian doorway, EU number plate, foreign-language signage, cobbled lane, thatched roof, tram` to the canonical `[NEG]`.

#### `R128.png` *(tier 2 · not declared)*

**Lands on:** "an international vacation he had planned with his family" · **ledger** SR-10

- `R128.png`
A closed hard-shell suitcase standing upright on its wheels in an ordinary domestic hallway beside a front door, photographed square on from four feet away at chest height: plain dark shell, plain handle, NO AIRLINE TAGS, NO STICKERS, NO NAME LABEL AND NO BRAND MARK anywhere on it. The hallway beyond is plain — a bare wall, a plain floor, the door with no numbers on it. Cool daylight from a fanlight out of frame [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, luggage tag, airline sticker, name label, brand logo, house numbers, person

**Save as:** `H:\pd-media\assets\ai\ramirez\R128.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, luggage tag, airline sticker, name label, brand logo, house numbers, person` to the canonical `[NEG]`.

#### `R129.png` *(tier 2 · not declared)*

**Lands on:** "ultimately canceled a planned trip to Mexico" · **ledger** SR-11

- `R129.png`
A closed passport-sized booklet lying face up in an open shallow drawer among nothing else, photographed from a standing angle looking down into the drawer. THE COVER IS COMPLETELY BLANK — plain dark grained board with no crest, no coat of arms, no gold blocking, no country name, no chip symbol, no lettering of any kind. The drawer interior is bare wood. Soft north light from the left [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, coat of arms, gold blocking, country name, crest, chip symbol, other contents in the drawer

**Save as:** `H:\pd-media\assets\ai\ramirez\R129.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, coat of arms, gold blocking, country name, crest, chip symbol, other contents in the drawer` to the canonical `[NEG]`.

#### `R130.png` *(tier 2 · not declared)*

**Lands on:** "A trip he did not take." · **ledger** SR-10 · SR-11

- `R130.png`
The empty rear bench seat of an ordinary car photographed from the front passenger position looking back, in flat daylight through the windows: plain cloth upholstery, three seat belts hanging slack in their guides, nothing on the seat and nobody in the car. THE SEAT IS COMPLETELY BARE — nothing fixed to it, nothing strapped into it, no bags and no coats. The door cards and the headrests are plain and unmarked [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, licence plate, registration plate, number plate, badge on the grille, oval emblem, manufacturer wordmark, chrome nameplate, dealership signage, price sticker, window sticker, infant seat, booster seat, bags, coats, person, dashboard display

**Save as:** `H:\pd-media\assets\ai\ramirez\R130.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, licence plate, registration plate, number plate, badge on the grille, oval emblem, manufacturer wordmark, chrome nameplate, dealership signage, price sticker, window sticker, infant seat, booster seat, bags, coats, person, dashboard display` to the canonical `[NEG]`.

### J · the machine and the company, second angles — R131–R138 (8 plates)

*ACT_2 — headroom tier: ordered, NOT declared*

#### `R131.png` *(tier 2 · not declared)*

**Lands on:** "A search would result in a match if the consumer's first and last name were either identical or similar to a name on the list." · **ledger** LS-16

- `R131.png`
TWO plain pale filing cards lying side by side and touching along one long edge on a dark matte surface, photographed from directly overhead in even soft light, THE TWO CARDS ALMOST BUT NOT QUITE THE SAME SIZE — one is a few millimetres wider and a shade taller than the other, so their outer edges do not line up and that near-miss is the whole subject of the picture. BOTH CARDS ARE COMPLETELY BLANK: no printing, no ruling, no writing, no tab, no punch hole. Nothing else is in the frame [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, writing on the cards, hand, arrows, tick, cross, comparison marks

**Save as:** `H:\pd-media\assets\ai\ramirez\R131.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, writing on the cards, hand, arrows, tick, cross, comparison marks` to the canonical `[NEG]`.

#### `R132.png` *(tier 2 · not declared)*

**Lands on:** "Beginning in 2002, TransUnion introduced an add-on product called OFAC Name Screen Alert." · **ledger** LS-13

- `R132.png`
A shallow office drawer pulled fully open, seen from a standing angle looking down into it, filled front to back with IDENTICAL EMPTY HANGING FILE POCKETS on two steel rails: every pocket the same colour, the same height and slack because nothing is in any of them. ALL THE TAB HOLDERS ARE EMPTY — bare plastic frames with no cards and no writing in a single one. Even office light from above, nobody in frame [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, cards in the tab holders, handwritten labels, coloured tabs, files inside

**Save as:** `H:\pd-media\assets\ai\ramirez\R132.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, cards in the tab holders, handwritten labels, coloured tabs, files inside` to the canonical `[NEG]`.

#### `R133.png` *(tier 2 · not declared)*

**Lands on:** "In collecting other types of data for use on consumer reports — such as tax liens or bankruptcy judgments — TransUnion used at least one additional identifier …" · **ledger** LS-17

- `R133.png`
A bank of grey steel filing cabinets photographed square on from six feet away, TWO DRAWERS IN THE SAME COLUMN treated differently: the upper drawer is pulled fully out and packed with identical blank paper files standing on edge, and the drawer below it is shut. EVERY LABEL HOLDER ON EVERY DRAWER FRONT IS EMPTY — bare metal frames, no cards, no writing, no numbers anywhere on the run. Flat even office light, nobody in frame [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, drawer labels, numbers on the drawers, writing on the files, hand

**Save as:** `H:\pd-media\assets\ai\ramirez\R133.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, drawer labels, numbers on the drawers, writing on the files, hand` to the canonical `[NEG]`.

#### `R134.png` *(tier 2 · not declared)*

**Lands on:** "TransUnion presented no data showing that any of its name matches through the OFAC product were correct." · **ledger** LS-19

- `R134.png`
A single plain pale card lying alone on top of a folded stack of continuous fanfold paper, photographed close from a low three-quarter angle so the card is sharp and the perforated sprocket margins of the stack run away soft behind it. THE CARD IS COMPLETELY BLANK, and the fanfold sheet beneath it carries no writing either. The paper carries no writing of any kind, and this is what is on it instead: EVENLY SPACED FLAT GREY HORIZONTAL BARS of one uniform width and one uniform weight, laid in parallel like ruled bands of tone, each bar a solid unbroken block of soft grey with straight ends and no letter shapes, no word shapes, no gaps between words and no broken or ragged edge anywhere along it, so the sheet reads as printed matter purely by its rhythm of grey and white and carries not one readable character. One soft light from the left [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, writing on the card, printed figures, column headings, hand

**Save as:** `H:\pd-media\assets\ai\ramirez\R134.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, writing on the card, printed figures, column headings, hand` to the canonical `[NEG]`.

#### `R135.png` *(tier 2 · not declared)*

**Lands on:** "the company had determined that the alerts it was placing on consumer credit reports were exempt from the Fair Credit Reporting Act" · **ledger** LS-20

- `R135.png`
An empty corporate meeting room photographed from one corner at standing height: one long plain table, eight identical chairs pushed in, and a blank pale wall at the far end WITH NOTHING MOUNTED ON IT AT ALL — no screen, no whiteboard, no poster, no clock, no logo, no lettering. A run of windows down the left throws flat daylight across the table. Nothing on the table, nobody in the room [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, readable screen, spreadsheet on a monitor, web page, icons, cursor, user interface, whiteboard with writing, company logo, poster, person

**Save as:** `H:\pd-media\assets\ai\ramirez\R135.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, readable screen, spreadsheet on a monitor, web page, icons, cursor, user interface, whiteboard with writing, company logo, poster, person` to the canonical `[NEG]`.

#### `R136.png` *(tier 2 · not declared)*

**Lands on:** "That was the position. Whether it was right is the next act." · **ledger** LS-20

- `R136.png`
An internal glazed partition between two offices, photographed square on from four feet away, the horizontal blind on the far side HALF OPEN so alternating bands of the empty room beyond and of pale blind slat cross the frame. The room beyond holds one bare desk and one empty chair. The glass carries a soft reflection of a plain wall and nothing else, and there is no lettering on it. Nobody in either room [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, readable screen, spreadsheet on a monitor, web page, icons, cursor, user interface, lettering on the glass, company name, person, reflection of a face

**Save as:** `H:\pd-media\assets\ai\ramirez\R136.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, readable screen, spreadsheet on a monitor, web page, icons, cursor, user interface, lettering on the glass, company name, person, reflection of a face` to the canonical `[NEG]`.

#### `R137.png` *(tier 2 · not declared)*

**Lands on:** "That is not the sentence that decides this case, though. This one is, and it is a footnote." · **ledger** LS-17

- `R137.png`
A plain corporate reception counter in an empty lobby, photographed square on from ten feet away at standing height: a long pale stone counter, an empty chair behind it, and a blank wall rising behind that WITH NOTHING ON IT — no company name, no logo, no lettering, no artwork, no directory board. A polished floor runs across the foreground and flat daylight comes from a glazed wall out of frame left. Nobody in the lobby [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, company name on the wall, logo, directory board, artwork, person

**Save as:** `H:\pd-media\assets\ai\ramirez\R137.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, company name on the wall, logo, directory board, artwork, person` to the canonical `[NEG]`.

#### `R138.png` *(tier 2 · not declared)*

**Lands on:** "For a tax lien, a name was not enough. For a terrorist list, it was." · **ledger** LS-17

- `R138.png`
TWO plain pale cards lying flat on a large empty dark table, FAR APART FROM ONE ANOTHER — one near the left edge of the frame and one near the right, with a wide expanse of bare dark table between them and absolutely nothing in that gap. Photographed from directly overhead. BOTH CARDS ARE COMPLETELY BLANK. One soft light from the left so each card casts its own thin separate shadow [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, writing on the cards, line joining them, arrow, hand, third card

**Save as:** `H:\pd-media\assets\ai\ramirez\R138.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, writing on the cards, line joining them, arrow, hand, third card` to the canonical `[NEG]`.

### K · the letters going out, and the trial — R139–R143 (5 plates)

*ACT_3 — headroom tier: ordered, NOT declared*

#### `R139.png` *(tier 2 · not declared)*

**Lands on:** "Between the first of January and the twenty-sixth of July, 2011, the letters kept going out." · **ledger** MN-01

- `R139.png`
A plain mail-room bench photographed from a standing three-quarter angle: a wide grey worktop with a shallow open tray on it holding A TIGHT ROW OF IDENTICAL PLAIN WHITE ENVELOPES STANDING ON EDGE, all the same size, packed so their top edges make one straight unbroken line across the tray. EVERY ENVELOPE IS BLANK — no address, no window, no stamp, no franking mark. Hard even overhead light, a bare wall behind, nobody in the frame [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, address blocks, window envelopes, stamps, franking, barcodes

**Save as:** `H:\pd-media\assets\ai\ramirez\R139.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, address blocks, window envelopes, stamps, franking, barcodes` to the canonical `[NEG]`.

#### `R140.png` *(tier 2 · not declared)*

**Lands on:** "TransUnion sent the same OFAC letter to eight thousand, one hundred and eighty-four other consumers …" · **ledger** SR-13

- `R140.png`
The feed tray of a plain grey mailing machine, photographed close from a low three-quarter angle, A STACK OF IDENTICAL BLANK WHITE ENVELOPES loaded into it with the topmost one just entering the rollers. EVERY ENVELOPE IS BLANK — no address, no window, no stamp, no franking mark — and the machine itself carries no maker's name and no control panel with readable icons. Even workshop light, nobody in the frame [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, readable screen, spreadsheet on a monitor, web page, icons, cursor, user interface, address blocks, franking impression, brand name on the machine, panel icons

**Save as:** `H:\pd-media\assets\ai\ramirez\R140.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, readable screen, spreadsheet on a monitor, web page, icons, cursor, user interface, address blocks, franking impression, brand name on the machine, panel icons` to the canonical `[NEG]`.

#### `R141.png` *(tier 2 · not declared)*

**Lands on:** "eight thousand, one hundred and eighty-four other consumers who had also requested copies of their credit reports in that window" · **ledger** SR-13

- `R141.png`
A wall of identical small residential mailboxes in an apartment lobby, photographed square on so the grid of doors fills the whole frame: eight across and six down, every door shut, every one the same brushed aluminium with the same small keyhole and the same little name-card slot. ALL THE NAME SLOTS ARE EMPTY AND NO DOOR CARRIES A NUMBER. Even flat lobby light, nobody in the frame [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, box numbers, name cards, handwritten labels, junk mail sticking out, person

**Save as:** `H:\pd-media\assets\ai\ramirez\R141.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, box numbers, name cards, handwritten labels, junk mail sticking out, person` to the canonical `[NEG]`.

#### `R142.png` *(tier 2 · not declared)*

**Lands on:** "In July 2011, TransUnion finally stopped sending the letters …" · **ledger** LS-21

- `R142.png`
A single bundle of identical plain white envelopes held together by a paper band, LYING ON ITS SIDE AND PUSHED TO ONE END of an otherwise completely empty grey counter, photographed from a low three-quarter angle so the bare counter runs away empty across the rest of the frame. Every envelope in the bundle is blank, AND THE PAPER BAND AROUND THEM IS BLANK TOO — no printing, no writing, no batch mark. Cool even light, nobody in the frame [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, printing on the band, batch number, address blocks, stamps, hand

**Save as:** `H:\pd-media\assets\ai\ramirez\R142.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, printing on the band, batch number, address blocks, stamps, hand` to the canonical `[NEG]`.

#### `R143.png` *(tier 2 · not declared)*

**Lands on:** "The trial ran six days." · **ledger** MN-04

- `R143.png`
Six identical plain white paper cups left standing on a bare wooden table in a plain room at the end of a long day, photographed from a standing three-quarter angle: most upright, two knocked slightly askew, all of them empty and ALL OF THEM COMPLETELY UNMARKED with no printing, no logo and no writing on any cup. Nothing else on the table at all. Flat overhead light, nobody in the room [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, printing on the cups, logo, coffee shop branding, notepads, person

**Save as:** `H:\pd-media\assets\ai\ramirez\R143.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, printing on the cups, logo, coffee shop branding, notepads, person` to the canonical `[NEG]`.

### L · what was not decided, and the ending — R144–R146 (3 plates)

*ACT_5 / ENDING — headroom tier: ordered, NOT declared*

#### `R144.png` *(tier 2 · not declared)*

**Lands on:** "It did not decide whether TransUnion violated the Fair Credit Reporting Act." · **ledger** ND-01

- `R144.png`
A single plain panelled door standing closed at the far end of a dim corridor, photographed straight down the corridor from twenty feet away at eye height: the walls and the floor fall away into shadow that still holds all of its detail, and A THIN HARD LINE OF LIGHT shows under the door and lies a short way out across the floor. The door is completely bare — no number, no nameplate, no sign, no notice. Nobody in the corridor [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, courtroom, judge's bench, jury box, witness stand, gavel, scales of justice, state seal, carved motto, engraved lettering on stone, banner, memorial plaque, door number, nameplate, exit sign, person, crushed black shadow

**Save as:** `H:\pd-media\assets\ai\ramirez\R144.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, courtroom, judge's bench, jury box, witness stand, gavel, scales of justice, state seal, carved motto, engraved lettering on stone, banner, memorial plaque, door number, nameplate, exit sign, person, crushed black shadow` to the canonical `[NEG]`.

#### `R145.png` *(tier 2 · not declared)*

**Lands on:** "The record this film is built on ends on the twenty-fifth of June, 2021 …" · **ledger** ⛔-12 · ○-04

- `R145.png`
The same ordinary American residential street as the dusk plate, photographed from the same position in the middle of the road at the same standing height, NOW AT FIRST LIGHT AND COMPLETELY EMPTY: the same houses, the same driveways, the same kerbline running away to the same vanishing point, the sky pale and cold, every window dark, NOBODY ANYWHERE IN THE FRAME and nothing moving. No house numbers, no street sign, no parked car in the road [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, European streetscape, Irish town, Georgian doorway, EU number plate, foreign-language signage, cobbled lane, thatched roof, tram, house numbers, street sign, person, car headlights, sunrise glow

**Save as:** `H:\pd-media\assets\ai\ramirez\R145.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, European streetscape, Irish town, Georgian doorway, EU number plate, foreign-language signage, cobbled lane, thatched roof, tram, house numbers, street sign, person, car headlights, sunrise glow` to the canonical `[NEG]`.

#### `R146.png` *(tier 2 · not declared)*

**Lands on:** "Justice Kagan's question is still on the table, and it is a short one." · **ledger** KG-04

- `R146.png`
ONE plain white envelope lying alone at the centre of a large bare wooden table, photographed from a low angle almost level with the table top so the envelope reads as one thin bright horizontal in the middle of the frame and the room beyond falls soft and grey. The envelope is completely blank and still sealed. Nothing else is on the table and nobody is in the room. Flat even daylight from a window out of frame left [STYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, address block, stamp, person, hand, second envelope

**Save as:** `H:\pd-media\assets\ai\ramirez\R146.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, address block, stamp, person, hand, second envelope` to the canonical `[NEG]`.

## 6. TIER 3 — thumbnail plates, 6, T001–T006, **never a cut**

Two candidates for each of PACKAGING §2's three variants, so the owner has a real A/B inside each concept rather than one take per idea. **These are never placed in the film and are never declared in `mandatory_stills`** — a thumbnail is not a cut, and EP65 had to un-declare its thumbnail plates late for exactly this reason.

They use **`[TSTYLE]`, not `[STYLE]`** (§2). The reason is measured: the canonical `[STYLE]` asks for low contrast and soft falloff, which is right for a film frame and is why EP65's four thumbnail candidates were all dull and had to be re-ordered. `[TSTYLE]` asks for one hard directional key, high contrast, bright exposure and a subject brighter than its background. **`[NEG]` is not deviated.**

The builder (`scripts/build_ep62_65_thumbnails.py`, PACKAGING §2) lays a black scrim at alpha 120 over the top 66% and fits the headline into it, and the unscrimmed band at y 475–634 is what `thumb_subject_luma` measures. So each prompt asks for **the entire upper 40% as one unbroken field** — nothing for a headline to collide with — and for **the bottom third to be the brightest part of the frame**.

#### `T001.png` *(thumbnail · not declared · never a cut)*

**Serves:** PACKAGING §2 variant 1 — headline NAME ONLY / kicker NO OTHER CHECK · **ledger** SR-02 · SR-03

- `T001.png`
A car-dealership sales desk seen from behind the customer's shoulder and slightly above, THE WHOLE SUBJECT SITTING IN THE LOWER 60 PERCENT OF THE FRAME: TWO ADULT HANDS LIE FLAT AND SEPARATE ON THE DESK TOP in the near foreground, palms down and in full contact with the surface, the four fingers of each hand side by side with a line of shadow between each pair and one nail visible on each, both thumbs clearly apart; a set of unmarked car keys sits on the far side of the desk just out of their reach; a slim monitor stands at the far edge TURNED AWAY so only its plain back is visible. The screen is never legible: it is a single soft bloom of even light with no icons, no windows, no rows, no cursor and nothing that could be read as a document. Bright showroom glass and a sunlit forecourt fill the bottom third and are the brightest thing in the picture. The upper 40 percent is one unbroken field of plain out-of-focus showroom shadow [TSTYLE] Avoid: [NEG], fingers fused into one mass, fingers merged, webbed fingers, mitten hand, stub fingers, missing thumb, extra fingers, six fingers, malformed hand, interlocked fingers, raised hand, hand held up in the air, blurred hand, readable screen, spreadsheet on a monitor, web page, icons, cursor, user interface, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, licence plate, registration plate, number plate, badge on the grille, oval emblem, manufacturer wordmark, chrome nameplate, dealership signage, price sticker, window sticker, face, head, object in the top of the frame, ceiling detail, hanging sign, low contrast, dull flat lighting, dark subject, detail crossing the top of the frame

**Save as:** `H:\pd-media\assets\ai\ramirez\T001.png`

**`[NEG]` addition:** append `, fingers fused into one mass, fingers merged, webbed fingers, mitten hand, stub fingers, missing thumb, extra fingers, six fingers, malformed hand, interlocked fingers, raised hand, hand held up in the air, blurred hand, readable screen, spreadsheet on a monitor, web page, icons, cursor, user interface, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, licence plate, registration plate, number plate, badge on the grille, oval emblem, manufacturer wordmark, chrome nameplate, dealership signage, price sticker, window sticker, face, head, object in the top of the frame, ceiling detail, hanging sign, low contrast, dull flat lighting, dark subject, detail crossing the top of the frame` to the canonical `[NEG]`. **The canonical `[NEG]` is not deviated for thumbnails.**

#### `T002.png` *(thumbnail · not declared · never a cut)*

**Serves:** PACKAGING §2 variant 1, alternate — headline NAME ONLY · **ledger** SR-02 · SR-03

- `T002.png`
The same dealership desk, closer and lower: ONE ADULT HAND LIES FLAT ON THE BARE DESK in the near lower left of the frame with its four fingers side by side and separate, each with its own nail and its own shadow, and the thumb clearly apart; A SET OF UNMARKED CAR KEYS lies on the desk to the right of it. Both are low in the frame and both are hit by one hard directional key light from the left that makes them markedly brighter than anything behind them. The bottom third of the frame is bright bare desk. The upper 40 percent is one unbroken field of plain dark out-of-focus interior with nothing in it at all [TSTYLE] Avoid: [NEG], fingers fused into one mass, fingers merged, webbed fingers, mitten hand, stub fingers, missing thumb, extra fingers, six fingers, malformed hand, interlocked fingers, raised hand, hand held up in the air, blurred hand, readable screen, spreadsheet on a monitor, web page, icons, cursor, user interface, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, licence plate, registration plate, number plate, badge on the grille, oval emblem, manufacturer wordmark, chrome nameplate, dealership signage, price sticker, window sticker, face, object in the top of the frame, low contrast, dull flat lighting, dark subject, detail crossing the top of the frame

**Save as:** `H:\pd-media\assets\ai\ramirez\T002.png`

**`[NEG]` addition:** append `, fingers fused into one mass, fingers merged, webbed fingers, mitten hand, stub fingers, missing thumb, extra fingers, six fingers, malformed hand, interlocked fingers, raised hand, hand held up in the air, blurred hand, readable screen, spreadsheet on a monitor, web page, icons, cursor, user interface, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, licence plate, registration plate, number plate, badge on the grille, oval emblem, manufacturer wordmark, chrome nameplate, dealership signage, price sticker, window sticker, face, object in the top of the frame, low contrast, dull flat lighting, dark subject, detail crossing the top of the frame` to the canonical `[NEG]`. **The canonical `[NEG]` is not deviated for thumbnails.**

#### `T003.png` *(thumbnail · not declared · never a cut)*

**Serves:** PACKAGING §2 variant 2 — headline NEVER SENT / kicker 6,332 FILES · **ledger** HD-08

- `T003.png`
An office desk drawer pulled HALF OPEN with A SINGLE UNOPENED PLAIN WHITE ENVELOPE lying alone inside it and the rest of the drawer bare empty wood, photographed from a standing angle looking down, THE DRAWER AND THE ENVELOPE FILLING THE LOWER 60 PERCENT OF THE FRAME. One hard directional daylight from the left makes the envelope the brightest object in the picture and lays a crisp shadow from it across the drawer bottom; the bright uncluttered desk surface runs across the bottom third. The envelope is completely blank — no address, no window, no stamp. The upper 40 percent is one unbroken field of plain out-of-focus dark office with nothing crossing it [TSTYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, address block, stamp, other contents in the drawer, hand, object in the top of the frame, low contrast, dull flat lighting, dark subject, detail crossing the top of the frame

**Save as:** `H:\pd-media\assets\ai\ramirez\T003.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, address block, stamp, other contents in the drawer, hand, object in the top of the frame, low contrast, dull flat lighting, dark subject, detail crossing the top of the frame` to the canonical `[NEG]`. **The canonical `[NEG]` is not deviated for thumbnails.**

#### `T004.png` *(thumbnail · not declared · never a cut)*

**Serves:** PACKAGING §2 variant 2, alternate — headline NEVER SENT · **ledger** HD-08

- `T004.png`
The same desk drawer and the same single blank envelope, closer and from a lower angle almost level with the desk top: the drawer front makes one strong bright horizontal across the lower third of the frame, the near corner of the envelope rises just above it catching a hard key light from the left, and the whole picture is bright and high contrast. The envelope is completely blank. The upper 40 percent is one unbroken field of plain out-of-focus darkness with nothing in it [TSTYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, address block, stamp, hand, object in the top of the frame, low contrast, dull flat lighting, dark subject, detail crossing the top of the frame

**Save as:** `H:\pd-media\assets\ai\ramirez\T004.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, address block, stamp, hand, object in the top of the frame, low contrast, dull flat lighting, dark subject, detail crossing the top of the frame` to the canonical `[NEG]`. **The canonical `[NEG]` is not deviated for thumbnails.**

#### `T005.png` *(thumbnail · not declared · never a cut)*

**Serves:** PACKAGING §2 variant 3 — headline 8,185 NAMES / kicker ONE CHECK EACH · **ledger** MN-02 · LS-15

- `T005.png`
A dense field of small identical pale record cards laid edge to edge in a regular grid, photographed from directly above, ONE CARD LIFTED SLIGHTLY OUT OF THE GRID near the bottom of the frame and catching a hard directional key light so that it is markedly brighter than every card around it and throws a crisp shadow onto them. EVERY CARD IS COMPLETELY BLANK — no printing, no ruling, no writing, no numbers. The grid is brightest along the bottom edge of the frame, and the upper 40 percent of the frame is one unbroken even field of the same cards gone soft and featureless out of focus, with no edge crossing it [TSTYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, writing on the cards, printed forms, hand, numbers, object in the top of the frame, low contrast, dull flat lighting, dark subject, detail crossing the top of the frame

**Save as:** `H:\pd-media\assets\ai\ramirez\T005.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, writing on the cards, printed forms, hand, numbers, object in the top of the frame, low contrast, dull flat lighting, dark subject, detail crossing the top of the frame` to the canonical `[NEG]`. **The canonical `[NEG]` is not deviated for thumbnails.**

#### `T006.png` *(thumbnail · not declared · never a cut)*

**Serves:** PACKAGING §2 variant 3, alternate — headline 8,185 NAMES · **ledger** MN-02 · LS-15

- `T006.png`
The same field of identical blank record cards, photographed from a slightly raking angle just above the surface so the near cards are large and bright across the bottom third of the frame, ONE CARD STANDING PROUD of the others in the lower middle and lit hard from the left so it is the brightest and sharpest thing in the picture. All cards completely blank. The upper 40 percent of the frame is one unbroken field of the receding grid gone entirely soft and even, with no edge and no horizon crossing it [TSTYLE] Avoid: [NEG], readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, writing on the cards, hand, numbers, object in the top of the frame, low contrast, dull flat lighting, dark subject, detail crossing the top of the frame

**Save as:** `H:\pd-media\assets\ai\ramirez\T006.png`

**`[NEG]` addition:** append `, readable document, printed words on paper, letterforms, typed lines, printed paragraph, form fields with labels, letterhead, stamp with words, writing on the cards, hand, numbers, object in the top of the frame, low contrast, dull flat lighting, dark subject, detail crossing the top of the frame` to the canonical `[NEG]`. **The canonical `[NEG]` is not deviated for thumbnails.**

## 7. Checking this order

```
py -3.11 scripts/check_image_order_neg.py --file episodes/_planning/EP67_ramirez_CODEX_BATCH_A.v002.md
py -3.11 scripts/check_design_doc.py --slug ramirez
py -3.11 scripts/check_episode_spec.py --slug ramirez
py -3.11 scripts/build_ep67_ramirez_image_order.py --verify
```

The first proves the `[NEG]` carries all five token families (face/likeness, readable text, handwriting, marks of authority, numerals). The last re-derives this document and the paste files from the same source and reports prompt count, distinct save names, control characters, block lengths, banned-token counts and md↔paste body equality.

Byte-identity of the `[NEG]` against batch D can be confirmed directly:

```
py -3.11 -c "import re;g=lambda p:max([l for l in open(p,encoding='utf-8').read().splitlines() if l.lstrip().startswith('>') and re.search(r'\btext\b.*\blettering\b',l,re.I)],key=len).lstrip('> ').strip();d=g('episodes/_planning/EP66_openfields_CODEX_BATCH_D.v001.md');r=g('episodes/_planning/EP67_ramirez_CODEX_BATCH_A.v002.md');print('NEG identical:',d==r,len(d),len(r))"
```

*Generated 2026-08-11 from `scripts/build_ep67_ramirez_image_order.py`. Do not hand-edit this file — edit the generator and re-run it, or the paste files drift.*

---

> **Correction, 2026-08-12.** *(corrected 2026-08-12: the declaration was lowered to **222** in `episode_spec.v002.json` — 260 was never derived from the allocator; see `decisions/0009-DISTINCT-VIDEO-ASSETS-CORRECTION.md`. The figure below is the retired one, kept for provenance.)*
