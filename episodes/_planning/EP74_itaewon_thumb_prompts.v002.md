# EP74 · ITAEWON — THUMBNAIL ORDER & PACKAGING v002

**Supersedes v001 by AMENDMENT OF NAMED SECTIONS ONLY.** §0, §1, §2 (the bars, the house look and
the canonical `[NEG]`) and §3 (the six thumbnail concepts `T01`–`T06`) of
`EP74_itaewon_thumb_prompts.v001.md` **remain in force, unedited, and are not restated.** This file
replaces **§4 (titles)** and **§5 (kickers and description)**, and adds **§7 — the measured results**.

**Why v002.** v001's titles were reasoned, not measured. `check_packaging_claims.py` has now been run
against every one of them, and **the recommended title of v001 FAILS.** The script changed too:
v005 speaks the transport figures and the suspension of both appeals, which changes what a title is
allowed to say.

---

## 2b. THE CANONICAL `[NEG]`, CARRIED FORWARD

v002 orders no new plates — `T01`–`T06` and their prompts live in v001 §3 and are unchanged. The
`[NEG]` is nonetheless repeated here in full rather than referenced, for the same reason v001's first
draft was rejected by `check_image_order_neg.py`: **a negative block that lives in another document
does not protect anything ordered in this one**, and a reader who opens the newest revision must find
the mechanism in it. Append to every thumbnail prompt:

> text, lettering, readable text, legible text, numerals, numbers, digits, house numbers, handwriting, cursive, signature, legible signature, seals, seal, emblems, emblem, logos, logo, badge, insignia, wordmarks, name plates, licence plate, registration plate, identifiable person, recognisable person, recognizable person, likeness of a real individual, portrait of a named person, celebrity, public figure, deepfake, body, corpse, dead body, fallen person, person on the ground, person being crushed, crush, pile of people, trampled, injured person, blood, cpr, chest compression, resuscitation, defibrillator, stretcher, gurney, paramedic, ambulance interior, hospital, emergency room, morgue, autopsy, coffin, funeral, grave, mourner, crying, grieving, rescue, search and rescue, victim portrait, portrait wall, memorial photograph, framed photograph of a person, candles, flowers laid on the ground, gavel, scales of justice, lady justice, jury box, judge's bench, courtroom interior, handcuffs, firearm, prison bars, japanese signage, kana, hiragana, katakana, chinese characters as shopfront, chinese lantern, tokyo, shibuya, shanghai, hong kong, bangkok, times square, london street, european street, EU number plate, right-hand-drive traffic, american highway sign, US route shield, american flag, megacity skyline, skyscraper cluster, expressway interchange, palm trees, beach, surf, ocean, tropical, desert, cruise ship, mardi gras, carnival, parade float, confetti, music festival, concert crowd, stadium crowd, sports fans, fireworks, new year countdown, horror movie, zombie, video game, crash test, action movie explosion, golden hour, sunset glow, postcard scenery, christmas, wedding, handshake, money rain, falling banknotes, stock ticker, glossy advertising lighting, flat CGI, 3D render, cartoon, illustration, anime, oversaturated, HDR halo, watermark

**On faces, deliberately** — `human face`, `facial features`, `eye contact` and `headshot` are absent
and must not be added. Identifiability is what is barred, not faces.

---

## 4. TITLE — measured, not reasoned *(replaces v001 §4)*

Run against `episodes/_planning/EP74_itaewon_script.en.v005.md` and the four ledger revisions —
**682 sentences from 4 files** — on 2026-08-21.

| verdict | chars | title |
|---|---|---|
| **PASS ★ A** | 77 | **Officers Were Deployed To Four Of The Eleven Reports Before The Itaewon Crush** |
| **PASS ★ B** | 74 | **The Court Convicted The Police Chief And Acquitted The District In Itaewon** |
| PASS | 75 | No Law Required Anyone To Plan For The Crowd That Filled That Itaewon Alley |
| PASS | 77 | The Police Received Eleven Reports About That Itaewon Alley And Attended Four |
| PASS | 71 | A Court Acquitted The District Because No Law Covered The Itaewon Crowd |
| **FAIL** | 69 | ~~Eleven People Called The Police Before 159 Died In That Itaewon Alley~~ |
| **FAIL** | 69 | ~~Police Went To Four Of Eleven Warnings Before The Itaewon Crowd Crush~~ |

All are 59–100 characters, third person, no question form, no citation, **Itaewon** as the searchable
suffix term.

**The A/B pair is A and B.** A is the film's spine and is almost verbatim from script line 285 —
which is exactly why it passes. B is the film's contradiction in one line.

**Why the two failures matter more than the five passes.**

- The v001 recommendation, *"Eleven People Called The Police Before 159 Died…"*, returned
  **UNVERIFIED** on `['alley', 'die', 'call']`: no single line in the record carries all three. This
  is the numeral-versus-words risk v001 declared, and it was real. **It was the recommended title.**
- *"Police Went To Four Of Eleven Warnings…"* returned **CONTRADICTED** — a negation cue attached to
  *go*, three tokens away, inside a quoted emergency call: *"…even though no more can go down."* A
  false positive in substance, and it is still disqualifying, because the standing rule is that the
  check is never weakened to accommodate a title. **Rewriting the title was cheaper than arguing
  with the instrument**, and "Officers Were Deployed" is closer to the script anyway.

## 5. THUMBNAIL TEXT AND DESCRIPTION *(replaces v001 §5)*

**Thumbnail text — all ten candidates PASS**, headline and headline-plus-kicker alike: `3.2 METRES` ·
`3.2 METRES / 159 DIED IN THIS ALLEY` · `FOUR OF ELEVEN` · `FOUR OF ELEVEN / EVERY CALL SAID THE SAME
THING` · `137 OFFICERS` · `137 OFFICERS / FOR A HUNDRED THOUSAND PEOPLE` · `NOBODY ORGANISED IT` ·
`ELEVEN CALLS` · `ELEVEN CALLS / THE FIRST CAME AT 6:34` · `NO LAW REQUIRED IT`.

**Selected: `3.2 METRES / 159 DIED IN THIS ALLEY`** on concept `T01`. v001's caution against
*THE ALLEY THAT KILLED 159* stands — "killed" is a causal verb the script does not use of the alley,
and *159 DIED IN THIS ALLEY* is script line 336 almost word for word.

**Description — the text of record.** Verified as a whole with title A and the selected thumbnail
text: **PASS, claims=34, unsupported=0**, and no `CONTRADICTED`, `NUMBER_MISMATCH` or
`QUALIFIED_ONLY` anywhere.

> On 29 October 2022, between 6:34 in the evening and 11 minutes past 10, police in Itaewon received
> eleven distress reports about dangerous levels of overcrowding. Officers were deployed to four of
> them.
>
> A hundred and fifty-nine people died in an alley about fifty metres long, five metres wide at the
> top and three point two at the bottom. On the last Saturday in October, 137 officers were on duty
> in the district.
>
> Two years later a court convicted the former Yongsan police station chief at first instance and
> acquitted the Yongsan ward office chief, because related law and regulations did not require them
> to come up with safety measures for events without organizers.
>
> The Seoul High Court has since paused both appeals, to wait for a fact-finding body that is still
> working.
>
> This film contains no footage of the crush and names none of the dead.

**Two rewrites were needed to get there, and both are worth recording.** A version that said
*"Both appeals were later suspended, so that a special investigation commission could establish what
happened"* returned **CONTRADICTED**: a negation cue two tokens from *special*, in the row about the
special act being **rejected** in January 2024. And a version that tightened every sentence onto a
script line returned a hard **NUMBER_MISMATCH** on *"A hundred and fifty-nine people died there"*,
because the record carries 157 and 158 in the same neighbourhood as *died*. **The looser phrasing is
the one that survives**, which is the opposite of the intuition, and it is why this was measured
instead of assumed.

---

## 7. THE MEASURED RESULTS *(new)*

```
py -3.11 scripts/check_packaging_claims.py --slug itaewon \
  --title "Officers Were Deployed To Four Of The Eleven Reports Before The Itaewon Crush" \
  --thumb-text "3.2 METRES / 159 DIED IN THIS ALLEY" \
  --description-file <the description above>

[PASS] PD-2026-074-itaewon  claims=34 unsupported=0 (+27 soft, not blocking)
       record=682 sentences from 4 files
```

**This clears the last item that was standing between EP74 and a render** (`fact_recheck.v002` §2
R4). It does not clear anything else: the checker says so itself, and so does this file —
*it cannot judge tone, implication, or a claim the script makes badly.* Somebody still has to read
the title against the film.

**Re-run it on the day of publish**, against the final script and the final description, not against
this file.
