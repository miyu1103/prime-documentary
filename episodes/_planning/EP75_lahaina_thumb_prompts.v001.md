# EP75 · LAHAINA — THUMBNAIL ART + PACKAGING v001

Covers rows 11, 12 and 13 of `PD_ONE_PASS_PRODUCTION_SPEC.v3`: at least three thumbnail variants
rendered as Remotion `<Still>` at **1280×720** from pre-generated background art, one selected before
`package_ready`; and a title in the measured winning shape. Direction is `FILM_BIBLE.v001` §16.

## 0. The rules that govern this file before any craft rule

`ship_policy.factual_support` names the title, the thumbnail text and the description as claims, and
`check_packaging_claims.py` gates them against this episode's own script. **Every candidate below was
run through that gate and the measured result is printed next to it.** Nothing here is proposed on
taste alone.

Four constraints specific to this episode, and none of them is negotiable:

1. **⛔-01 — no counterfactual, anywhere in the package.** No title, thumbnail line or description
   sentence may state or imply that sounding the siren would have changed the outcome. **This is
   harder in packaging than in narration**, because a thumbnail has no room to qualify.
2. **⛔-03 — the word *failed* may not appear.** Not on the thumbnail, not in the title. No source says
   the sirens failed.
3. **⛔-04 — no question form, no ellipsis, no "what really happened".** This topic sits beside an
   active conspiracy audience and the packaging is the first thing they and everyone else see. **A
   question mark on this thumbnail would be read as an invitation.**
4. **⛔-07 — no victim, no face, no burned town from the air.** The channel's own CTR measurement says
   a human face is the strongest single driver. **This episode may not use one.** What it uses instead
   is municipal hardware, shot huge.

## 1. Thumbnail art — four concepts, all at 1280×720

Every prompt takes `[STYLE]` and `[NEG]` from `EP75_lahaina_CODEX_BATCH_A.v001.md`, plus: **huge
subject, very high contrast, one idea only, nothing in frame that is not load-bearing, legible at
320 px.** Accent is gold `#E5B53A` on T1/T2, electric `#1F6BFF` on T4; T3 carries no accent.
**Headlines are composited in Remotion — never generated into the art.**

### T2 — NEVER USED FOR FIRE (recommended)

> art: a cluster of grey painted steel outdoor warning siren horns on a galvanised pole, filling three quarters of the frame, shot from below against a flat pale overcast sky, salt corrosion and weather staining around the bolts, hard edge light from one side, the sky falling away to near-white at the corners, nothing else in frame, no text anywhere

- **Headline:** `NEVER USED` / `FOR FIRE` — two lines, gold on the pale sky, numerals none.
- Why it works: it is Finding 38, it is the whole film, and it is the one line that cannot be
  misread as either blame or counterfactual. It states a **history**, not a consequence.
- **⛔-01 check:** no outcome claimed. **⛔-03 check:** the word *failed* does not appear.
- Bright by design, which is the right side of the `thumbnail_visibility` luma floor to be on.

### T1 — ONE SIREN

> art: a single outdoor warning siren pole standing alone on a dry grass slope, seen from level and slightly below, the pole hard against a flat colourless sky, dry pale grass filling the bottom third, a low blurred suggestion of corrugated roofs far below, no smoke, no fire, no people

- **Headline:** `ONE` / `SIREN` — enormous, gold on near-black lower band.
- Why it works: Finding 37, and the single most quotable number in the record.
- **Binding condition:** `ONE SIREN` alone is an incomplete claim. **This concept may only ship
  paired with title B**, which carries *inside the burn perimeter* — so the qualifier exists
  somewhere the viewer meets it. Do not ship T1 with title A.

### T3 — THE ROAD OUT

> art: a heavy padlock and chain closing a galvanised chain-link gate across a dirt access track, the padlock filling the left half of the frame in sharp focus, the wire diamonds receding behind it, dry grass either side, flat hard daylight, grey smoke haze in the far distance, no people, no flame

- **Headline:** `THE ROAD OUT` / `WAS PADLOCKED` — near-white on the shadowed wire, no accent.
- Why it works: it is the only concept with a physical antagonist in it, and it is a true and small
  fact rather than a large one. Reads instantly at 320 px.
- **Risk:** it is the concept most likely to be read as an accusation against a named body. The
  title it ships with must be neutral — pair with **A**, never with D.

### T4 — SENT TO DEAD PHONES

> art: a hand holding an ordinary smartphone at arm's length, the screen entirely blank and black, filling the right half of the frame, the background a street lost in flat grey-brown smoke and completely out of focus, no face in frame, no flame, cold light on the hand

- **Headline:** `SENT TO` / `DEAD PHONES` — white with an electric blue rim on the handset.
- Why it works: it is the film's mechanism in two words and it needs no prior knowledge.
- **⛔-07 check:** no face. **Dark by design** — measure `thumbnail_visibility` and lift in the
  composite if it falls under the luma floor.

### The four headlines, measured as claims

Run as `check_packaging_claims.py --slug lahaina --title <A> --thumb-text "<headline>"`:

| headline | measured |
|---|---|
| `NEVER USED FOR FIRE` | **PASS · unsupported=0 · zero soft notes** |
| `ONE SIREN` | **PASS · unsupported=0 · zero soft notes** |
| `THE ROAD OUT WAS PADLOCKED` | PASS · unsupported=0 · 1 soft note |
| `SENT TO DEAD PHONES` | PASS · unsupported=0 · 2 soft notes |

The gate cannot judge tone or implication and says so in its own output. **The four constraints in
§0 are still a human read**, and they are the eighth item in FILM BIBLE §17.

## 2. Selection and the measured floor

- Render all four as Remotion `<Still>` at 1280×720 and measure `thumbnail_visibility`: the selected
  thumbnail's **luma mean must be ≥ 33** with the contrast floor met. **T4 is dark by design and T3
  is half dark** — measure, do not eyeball.
- **Ship T2 and T4 as the A/B pair.** T2 sells the contradiction, T4 sells the mechanism; they fail
  differently, which is the point of a pair. T1 is the third variant required by
  `thumbnail_candidates_min`.

## 3. Title — measured against the script, not chosen on taste

Row 13: **59–100 characters**, third person, **no question form**, no citation, no doctrine, a
searchable proper noun, at least two variants shipped.

Every row below was run as
`py -3.11 scripts/check_packaging_claims.py --slug lahaina --title "<title>"`
against the script and both ledgers. The result column is that run. **Re-run after the ledger grew to
694 sentences (the LH-38 upgrade): A and B both still PASS with unsupported=0 and zero soft notes.**

| # | title | chars | measured | notes |
|---|---|---|---|---|
| **A** | `Hawaii Built the World's Largest Warning Siren Network. It Had Never Been Used for a Fire.` | 90 | **PASS · claims=3 · unsupported=0 · zero soft notes** | **Recommended.** The whole contradiction, no counterfactual, no blame, no number that needs a qualifier. Ships with T2 or T3 |
| **B** | `Only One Siren Was Operable Inside the Burn Perimeter at Lahaina on August 8, 2023.` | 83 | **PASS · claims=6 · unsupported=0 · zero soft notes** | Finding 37 in the report's own words, with the qualifier and the searchable noun in the title itself. **The only title T1 may ship with** |
| C | `The Evacuation Order Was Sent to Cellphones. Lahaina's Cell Service Had Died That Morning.` | 90 | PASS · unsupported=0 · **3 soft notes** (UNVERIFIED, non-blocking) | The mechanism version, pairs with T4. The notes are wording drift — the script says "destroying cellular phone communication", not "cell service died" |
| D | `The Warning Network Was Tested Every Month. It Had Never Been Used for a Wildfire, Lahaina` | 90 | PASS · unsupported=0 · 2 soft notes | The monthly-test irony. **Do not pair with T3** — gate plus this title reads as an indictment |

**Searchable suffix.** `Lahaina` is the search term and it needs no accent. It is already inside
titles B and D. For A and C it goes in the **first line of the description**, not appended to the
title — both are at 90 characters and would break the 100-character ceiling.

**Barred title forms for this episode**, on top of the standing rules:

- Anything beginning *How*, *Why*, or *What really*.
- Any question form, any ellipsis, any "the truth about".
- Any construction with a **named person or agency as the grammatical agent** of the outcome.
- Any counterfactual, in any tense: *would have*, *could have*, *if only*, *should have*.
- The words *failed*, *ignored*, *covered up*, *hid*, *knew*.

## 4. Description — the first three lines

The three lines above the fold are a claim under `ship_policy.factual_support` and must carry, in
this order:

1. **What happened, with the date and the place** — Lahaina, Maui, 8 August 2023, and the County's
   own figure of **at least 102 lives** with the date it was stated (LH-19).
2. **The cause, plainly and attributed** — the County and ATF origin-and-cause finding: broken power
   lines re-energised, sparks into unmaintained vegetation near pole 25, classified **Accidental**
   (LH-11, LH-14, LH-16). **This belongs above the fold precisely because of ⛔-04**: the description
   is where a searcher who arrived from the conspiracy material lands first.
3. **What the investigation found about the warning** — 84 findings and 140 recommendations; one
   siren operable inside the burn perimeter; the network had never been used for a wildfire; and
   **no finding says that sounding it would have changed the outcome** (LH-30, LH-31, AB-01).

Sources for the description's fact block are the ledger rows, not this file.

**A draft exists and it passes.** `episodes/PD-2026-075-lahaina/09_package/description.draft.v001.txt`,
3,567 characters, run 2026-08-21 as
`check_packaging_claims.py --slug lahaina --title <A> --thumb-text "NEVER USED FOR FIRE"
--description-file <the draft>`:

```
[PASS] PD-2026-075-lahaina  claims=109 unsupported=0 (+62 soft, not blocking)
```

**62 soft notes is the documented normal for a prose description** and not a defect — rule 19 records
that a 4,000-character description reliably produces ~55 UNVERIFIED notes because prose paraphrases
what the script states in other words. **Zero blocking is the number that matters.**

**One instrument false positive was found and is worth knowing about.** The first draft named the
department by its full legal title, *County of Maui Department of Fire and Public Safety*. The gate
returned **CONTRADICTED** on that line, because the words "Public Safety" collide with Finding 30 —
*"Hawaiian Electric did not have a Public Safety Power Shut-Off program in place at the time of the
fire"* — and the matcher attached that negation to the date claim. **Nothing was contradicted.** It
was resolved by using **Maui Fire Department**, which is the abbreviation the record itself uses, so
accuracy was not traded away to satisfy a matcher. **Do not restore the full legal title in the
description**: it will block the ship on a `factual_support` verdict that is not true.

The settlement paragraph is **procedural and dated** (⛔-15) and must be **re-verified on the day the
description is finalised** (⛔-11) — as of 2026-08-21 no payment had been made, and the draft says
"AS OF AUGUST 2026" in its own subheading for exactly that reason.

## 5. What still has to happen

1. Generate the four background plates at 1280×720 or larger from the prompts above. They are **not**
   in `CODEX_BATCH_A` — commission them separately so a thumbnail plate never leaks into the film pool.
2. Render the four `<Still>`s with the headlines composited in Remotion.
3. Measure `thumbnail_visibility` on each; lift any that falls under the luma floor.
4. Select **T2**, keep **T4** as the paired variant, and record the choice in `09_package`.
5. Re-run `check_packaging_claims.py --package` once `youtube_meta.v001.json` exists, so the title,
   the thumbnail text and the description are all measured together rather than one at a time.
