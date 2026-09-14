# EP74 · ITAEWON — THUMBNAIL ORDER & PACKAGING v001

**Six thumbnail concepts `T01`–`T06`** against a declared minimum of three
(`thumbnail_candidates_min: 3`), and **four title candidates** against a required minimum of two
A/B variants.

Reads with `EP74_itaewon_FACTS_LEDGER.v001/v002/v003.md`, `EP74_itaewon_FILM_BIBLE.v001.md` §12,
`EP74_itaewon_script.en.v004.md` (every claim below cites its line), and
`EP74_itaewon_CODEX_BATCH_A.v001.md` (same `[STYLE]`, same `[NEG]`, same bars).

## 0. The gates this must clear

| gate | requirement |
|---|---|
| `thumbnail_ready` | **≥3 variants at 1280×720**, one selected, before `package_ready` |
| `thumbnail_visibility`, `thumb_subject_luma` | one idea, huge subject, high contrast, **readable at 320 px** |
| `packaging_qc` | title **59–100 characters**, third person, **no question form**, no citation or doctrine, real searchable term as suffix, **≥2 A/B variants** |
| `check_packaging_claims.py` → `factual_support` | **the title, the thumbnail text and the description are claims and are machine-checked against this episode's own script and ledger.** `UNVERIFIED` is not a pass |
| `ship_policy` `real_person_likeness` | **no real-person likeness anywhere in a thumbnail.** Blocking |

## 1. The bars — the same five as the image order, plus one

1. **No crush and nothing that implies one.** No body, no fallen person, no covered figure, no
   stretcher, no blood, no crowd at crush density. ⛔-02. **A thumbnail is the one frame everybody
   sees whether they watch or not** — this bar is stricter here than anywhere else in the film.
2. **No identifiable person.** Nobody in a thumbnail is a face. Where people appear they are backs,
   silhouettes and motion blur at distance.
3. **All headline typography is composited in Remotion / the thumbnail builder.** The generated
   plate is the background and carries **no glyph at all**. A generated letterform is a fabricated
   record.
4. **No courtroom furniture, and no gavel** — Korean courts do not use one.
5. **No victim imagery, no memorial portraiture, no flowers-and-candles thumbnail.** Grief is not
   the hook and will not be used as one.
6. **New here: no number the script does not speak.** The thumbnail text is a claim. `160` is
   forbidden outright (⛔-03), and any figure not in the ledger is forbidden (⛔-12).

## 2. House look for the background plates

Same `[STYLE]` as `EP74_itaewon_CODEX_BATCH_A.v001.md` §3.

**`[NEG]`** — carried in full here rather than by reference, because `check_image_order_neg.py`
requires every order to hold the mechanism itself. **It rejected the first draft of this file for
exactly that reason**, and it was right to: a negative block that lives in another document does not
protect the plates ordered in this one. Append to every thumbnail prompt:

> text, lettering, readable text, legible text, numerals, numbers, digits, house numbers, handwriting, cursive, signature, legible signature, seals, seal, emblems, emblem, logos, logo, badge, insignia, wordmarks, name plates, licence plate, registration plate, identifiable person, recognisable person, recognizable person, likeness of a real individual, portrait of a named person, celebrity, public figure, deepfake, body, corpse, dead body, fallen person, person on the ground, person being crushed, crush, pile of people, trampled, injured person, blood, cpr, chest compression, resuscitation, defibrillator, stretcher, gurney, paramedic, ambulance interior, hospital, emergency room, morgue, autopsy, coffin, funeral, grave, mourner, crying, grieving, rescue, search and rescue, victim portrait, portrait wall, memorial photograph, framed photograph of a person, candles, flowers laid on the ground, gavel, scales of justice, lady justice, jury box, judge's bench, courtroom interior, handcuffs, firearm, prison bars, japanese signage, kana, hiragana, katakana, chinese characters as shopfront, chinese lantern, tokyo, shibuya, shanghai, hong kong, bangkok, times square, london street, european street, EU number plate, right-hand-drive traffic, american highway sign, US route shield, american flag, megacity skyline, skyscraper cluster, expressway interchange, palm trees, beach, surf, ocean, tropical, desert, cruise ship, mardi gras, carnival, parade float, confetti, music festival, concert crowd, stadium crowd, sports fans, fireworks, new year countdown, horror movie, zombie, video game, crash test, action movie explosion, golden hour, sunset glow, postcard scenery, christmas, wedding, handshake, money rain, falling banknotes, stock ticker, glossy advertising lighting, flat CGI, 3D render, cartoon, illustration, anime, oversaturated, HDR halo, watermark

**Two tokens are in this `[NEG]` and not in the image order's:** `candles` and
`flowers laid on the ground`. Bar 5 of §1 forbids a grief thumbnail outright, and the memorial plate
`I119` that is permitted inside the film is not permitted as the cover of it.

**On faces, deliberately** — as in the image order, `human face`, `facial features`, `eye contact`
and `headshot` are absent and must not be added. Identifiability is what is barred.

Three additions to the composition:

- **Composed for a 320 px read.** One subject, one plane, nothing in the frame that disappears when
  the image is a thumbnail on a phone.
- **Deep negative space on one third of the frame** for the headline. Say which third in the prompt.
- **Contrast held wide**: the subject reads as a single bright shape against a dark field, or the
  reverse. No mid-grey compositions.

Headline colour: **gold `#E5B53A`** on five of six; **blue `#1F6BFF`** on `T03` only, so the A/B set
is not monochrome. Headline is UPPERCASE, ≤4 words, one idea.

---

## 3. The six concepts

### T01 — **3.2 METRES** ★ recommended

> **The idea:** the whole film in one measurement. It needs no country, no names and no context, and
> it is the thing a viewer can feel in their own body.

| | |
|---|---|
| headline | **3.2 METRES** (gold `#E5B53A`, occupying the upper third) |
| kicker | *THE ALLEY THAT KILLED 159* — optional, small, lower left |
| subject | the alley at its narrowest, shot square-on from the bottom, both walls hard in frame, **empty** |
| ledger | IT-02, IT-22 |
| script | line 127 — "At the top it is about five metres across. At the bottom … it is three point two." · line 336 — "A hundred and fifty-nine people died there." |
| prompt | `[STYLE]` + *a narrow empty alley between two low buildings at night, photographed square-on from its lower end, both walls hard in the frame and close enough to touch, wet asphalt holding the reflection of unreadable sign light, the passage visibly narrower at the near end than the far end, nobody in it at all, deep dark negative space across the upper third of the frame, high contrast, the walls reading as two bright edges against a black centre* + `[NEG]` |

### T02 — **FOUR OF ELEVEN**

> **The idea:** the state received eleven warnings and went to four. The graphic does the arithmetic
> before the viewer reads a word.

| | |
|---|---|
| headline | **FOUR OF ELEVEN** (gold `#E5B53A`, right half) |
| kicker | *EVERY CALL SAID THE SAME THING* |
| subject | eleven ruled rows, four filled solid gold, seven empty outline — **built in Remotion, not generated** — over a dark plate of the alley mouth at night |
| ledger | IT-13, IT-18 |
| script | line 208 — "eleven distress reports about dangerous levels of overcrowding" · line 285 — "Officers were deployed to four of them." |
| prompt | background only: `[STYLE]` + *the mouth of a narrow alley at night seen from across a main road, traffic light streaks crossing the foreground, the alley itself a black vertical slot in the middle distance, the left two thirds of the frame nearly empty and very dark* + `[NEG]` |

### T03 — **137 OFFICERS**

| | |
|---|---|
| headline | **137 OFFICERS** (blue `#1F6BFF`, lower third) |
| kicker | *FOR A HUNDRED THOUSAND PEOPLE* |
| subject | a very wide, very dark night street with a single small high-visibility figure far off — the scale gap is the image |
| ledger | IT-08, IT-55, IT-56 |
| script | line 492 — "A hundred and thirty-seven." · line 497 — "the number of police officers deployed to Itaewon for Halloween" |
| prompt | `[STYLE]` + *a wide dark city street at night seen down its length, one small high-visibility vest far away and turned away, no face, no marking, everything else in shadow, the figure tiny in a very large empty frame, lower third of the frame dark and clear* + `[NEG]` |

### T04 — **NOBODY ORGANISED IT**

| | |
|---|---|
| headline | **NOBODY ORGANISED IT** (gold `#E5B53A`, centred) |
| kicker | *AND SO NOBODY HAD TO PLAN FOR IT* |
| subject | the alley at dawn, completely empty, hosed, flat morning light |
| ledger | IT-26, IT-34 |
| script | line 187 — "Nobody organised it. There was no ticket, no promoter, no stage, no permit, no name on anything." · line 648 — "Related law and regulations did not require them to come up with safety measures for events without organizers." |
| prompt | `[STYLE]` + *a narrow sloping alley photographed from its top end at dawn, completely empty, wet from a hose, every shutter down, flat grey morning light, the passage receding to a bright opening at the far end, nobody in frame, the centre of the frame clean and uncluttered* + `[NEG]` |

### T05 — **ELEVEN CALLS**

| | |
|---|---|
| headline | **ELEVEN CALLS** (gold `#E5B53A`, upper left) |
| kicker | *THE FIRST CAME AT 6:34* |
| subject | one phone screen lighting a hand in a dark crowded street; the hand is the only bright thing; **no face** |
| ledger | IT-13, IT-14 |
| script | line 208 · line 280 — "Eleven calls." |
| prompt | `[STYLE]` + *a single lit phone screen held low in a dark crowded street at night, the light falling only on the hand and cuff, the crowd around it reduced to dark shoulders and out-of-focus sign glow, no face anywhere in frame, the upper left of the frame very dark and empty* + `[NEG]` |

### T06 — **NO LAW REQUIRED IT**

| | |
|---|---|
| headline | **NO LAW REQUIRED IT** (gold `#E5B53A`, right third) |
| kicker | *THE COURT SAID SO IN WRITING* |
| subject | a closed statute volume on a plain desk, raking light, **spine and cover blank** |
| ledger | IT-34, IT-34a, IT-79 |
| script | line 640 — "The same court found them not guilty." · line 648 |
| prompt | `[STYLE]` + *a heavy bound volume lying closed on a plain wooden desk under low raking daylight, cover and spine completely blank with no lettering or marking of any kind, deep shadow behind it, the right third of the frame empty and dark* + `[NEG]` |

**Recommendation: T01.** It is the only concept that needs no prior knowledge, it is legible at
320 px as two walls and a number, and it is the film's controlling image. T03 is the strongest
contrast partner for an A/B pair because it is the only blue one and the only wide one.

---

## 4. Title candidates

All four are third person, contain no question mark, cite no case or doctrine, and carry **Itaewon**
as the searchable suffix term. Character counts are measured, not estimated — see §6.

| id | title | chars | script support |
|---|---|---|---|
| **A ★** | Eleven People Called The Police Before 159 Died In That Itaewon Alley | 69 | lines 208, 336 |
| **B ★** | Police Went To Four Of Eleven Warnings Before The Itaewon Crowd Crush | 69 | lines 208, 285 |
| C | The Court Convicted The Police Chief And Acquitted The District In Itaewon | 74 | lines 618, 640 |
| D | No Law Required Anyone To Plan For The Crowd That Filled That Itaewon Alley | 75 | lines 187, 648 |

**A and B are the A/B pair.** Both hook on the calls, which is the film's spine, and neither needs a
Korean name to land. C is held in reserve: it is the sharpest "wait, what?" of the four, but it asks
the viewer to hold two officials apart in a thumbnail-sized moment. D is the most accurate to the
controlling idea and the least clickable.

**A known matcher risk, declared.** `check_packaging_claims.py` matches word stems and numbers
against the script. The script speaks every figure **in words** — "a hundred and fifty-nine", "a
hundred and thirty-seven" — while titles A and thumbnails T03 use **numerals**. That mismatch is the
documented false-positive mode (`UNVERIFIED`, 85 % of blocking findings across the live catalogue).
**Run the checker before locking anything.** If it fires on the numeral, the fix is *not* to weaken
the check: either use the word form in the title, or add one narration line that speaks the figure in
the matching form. Titles C and D carry no numerals and are immune to this.

## 5. Kicker and description bank

Kickers, for whichever thumbnail is chosen — each must also survive the claims check:

- *THE FIRST CAME AT 6:34* (IT-13, line 208)
- *EVERY CALL SAID THE SAME THING* (IT-14, IT-16, IT-17)
- *FOR A HUNDRED THOUSAND PEOPLE* (IT-55, line 497 area)
- *THE ALLEY THAT KILLED 159* — **caution:** "killed" is a causal verb the script does not use of the
  alley. Prefer *159 DIED IN THIS ALLEY* (IT-22, line 336)
- *AND SO NOBODY HAD TO PLAN FOR IT* (IT-26, IT-34)

Description opening — the first two lines are what shows above the fold, and they are claims too:

> On 29 October 2022, between 6:34 in the evening and 11 minutes past 10, police in Itaewon received
> eleven distress reports about dangerous levels of overcrowding. Officers were deployed to four of
> them.

Both sentences are line 208 and line 285 almost verbatim, which is the cheapest possible way to be
green on `factual_support`.

## 6. Verification, before anything is locked

```
py -3.11 scripts/check_image_order_neg.py --file episodes/_planning/EP74_itaewon_thumb_prompts.v001.md
py -3.11 scripts/check_packaging_claims.py --slug itaewon      # title, thumb text, description
```

Then build **all six** at 1280×720, put them on one labelled contact sheet, and have a person open it
looking for exactly four things: **anything that reads as a body**; **any face that reads as a real
person**; **any glyph the generator drew rather than the builder composited**; **any signage that is
Japanese, Chinese or Western**.

`thumbnail_ready` wants three. Six exist so that the choice is a choice.
