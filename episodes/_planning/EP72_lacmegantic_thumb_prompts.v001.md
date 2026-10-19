# EP72 · LAC-MÉGANTIC — THUMBNAIL ART + PACKAGING v001

Covers rows 11, 12 and 13 of `PD_ONE_PASS_PRODUCTION_SPEC.v3`: at least three thumbnail variants
rendered as Remotion `<Still>` at **1280×720** from pre-generated background art, one selected before
`package_ready`; and a title in the measured winning shape.

## 0. The rule that governs this file before any craft rule

`⛔-01` binds the **title, the thumbnail text and the description** exactly as it binds the narration,
and `ship_policy.factual_support` names them as "the first claim a viewer meets and the most widely
read sentence the channel publishes". Three men were **acquitted** of criminal negligence causing
death. **Every candidate below has to survive being read on its own, with no film around it.**

Two consequences, and they are not negotiable:

- **No packaging line may name or imply an individual culprit.** Not "the engineer", not "one man",
  not "he".
- **No real person's likeness appears on the thumbnail.** The channel's own CTR measurement says a
  human face is the strongest single driver; this episode cannot use one. What it uses instead is a
  **human presence with no face** — hands on a brake wheel, a back, a silhouette — which is the same
  compromise EP50 landed on for the same class of reason.

## 1. Thumbnail art — four concepts, all at 1280×720

Every prompt takes the `[STYLE]` and `[NEG]` from
`EP72_lacmegantic_CODEX_BATCH_A.v001.md`, plus: **huge subject, very high contrast, black or deep
navy ground, one idea only, nothing in the frame that is not load-bearing, legible at 320 px.**
Accent colour is gold `#E5B53A` for T1/T2 and electric `#1F6BFF` for T3; T4 carries no accent.
Headlines are composited in Remotion — **never generated into the art.**

### T1 — THE WHEEL (recommended)

> art: two bare hands gripping a rust-brown cast-iron hand-brake wheel on the end of a black tank car at night, filling the left two thirds of the frame, lit hard from one side by a single yard floodlight, the rest of the frame falling to black, wet steel, no face anywhere in frame, deep shadow with detail

- **Headline:** `7 SET` / `9 REQUIRED` — two lines, gold on black, the numerals enormous.
- Why it works: the whole contradiction is two numbers, and both are the **railway's own** — the
  applied count (LM-43) against the railway's own General Special Instruction minimum (LM-44).
- **⛔-04 check:** it never states the "needed" figure, which is a range, not a number.

### T2 — THE ENGINE THAT WAS THE BRAKE

> art: the front of a diesel locomotive at night seen three-quarters from below, a small orange flame and heavy smoke on the roof above the nose, everything else in near-darkness, one floodlight raking the flank, no person in frame, no fire touching any building

- **Headline:** `THEY PUT` / `IT OUT` — white on black, gold underline under the second line.
- Why it works: it promises the mechanism the film is actually about, and it is legible as a picture
  of a locomotive on fire without showing a burning town.
- **⛔-10 check:** no building alight, no person in frame.

### T3 — THE GAUGE

> art: extreme close-up of a round brass-rimmed air pressure gauge on a locomotive control stand, needle low, one point of light reflected in the hazed glass, the surrounding cab almost black, shot slightly off axis

- **Headline:** `NOBODY` / `WAS WATCHING` — white on black, electric blue rim light on the gauge.
- Why it works: it is the film's clock and it reads instantly as dread without any hazard imagery.
- Risk: the least self-explanatory of the four at 320 px. Test it small before selecting.

### T4 — THE EMPTY CHAIR

> art: a single plain wooden chair against a pale institutional wall in an otherwise empty room, daylight from one side, shot straight on and slightly wide so the emptiness of the room is the subject, muted colour, no accent colour anywhere

- **Headline:** `ALL THREE` / `ACQUITTED` — near-white on grey, no accent.
- Why it works: it is the ending, and it is the one concept that carries `⛔-01` **in the thumbnail
  itself** rather than depending on the film to correct an impression.
- Use as the B variant against T1 in the A/B test.

## 2. Selection and the measured floor

- Render all four as Remotion `<Still>` at 1280×720 and check `thumbnail_visibility`: the selected
  thumbnail's **luma mean must be ≥ 33** with the contrast floor met. **T2, T3 and T4 are all dark
  by design** — they must be measured, not eyeballed, and lifted in the composite if they fall under.
- Ship **T1 and T4** as the A/B pair. T1 sells the mechanism, T4 sells the ending; they fail
  differently, which is the point of a pair.

## 3. Title — the measured shape

Row 13: **59–100 characters**, third person, **no question form**, no case citation, no doctrine, a
searchable proper noun as a suffix, at least two variants shipped.

| # | title | chars | notes |
|---|---|---|---|
| **A** | `A Fire Was Put Out at Midnight. The Engine They Switched Off Was the Brake.` | 74 | Recommended. States the mechanism, names nobody, promises the reveal without giving the outcome |
| **B** | `Seven Hand Brakes Held a 10,000-Ton Train. The Railway's Own Rule Said Nine.` | 75 | The numbers version. Pairs naturally with thumbnail T1 |
| C | `The Firefighters Did Everything Right. Ninety Minutes Later the Town Was Gone.` | 77 | Strongest emotionally; slight risk of reading as blame on the fire service, which the film explicitly rejects — **only with T2** |
| D | `A Jury Acquitted All Three. It Was Never Allowed to See the Investigation.` | 73 | The `⛔-01`-safe option, and the one to use if any packaging concern is raised |

**Searchable suffix.** The town's name is the search term and it carries an accent that not every
keyboard produces. Use ` | Lac-Mégantic` in the description and the first line of the description
body; **do not** append it to titles A–D, all of which are already inside the character band and
would exceed the median at 90+ characters with it.

**Barred title forms for this episode**, on top of the standing rules: anything beginning "How", any
"Why nobody…", any "The man who…", and any construction in which a singular human subject is the
grammatical agent of the disaster.

## 4. Description — the first three lines

The three lines above the fold are a claim under `ship_policy.factual_support` and must carry:

1. what happened, with the date and the town;
2. the fact that eighteen causes and contributing factors were identified and **no individual was
   established as the cause**;
3. that three men were tried and **acquitted**, and that six former employees, including the
   engineer, separately **pleaded guilty to a regulatory offence** — both, in that order (`⛔-01`).

Sources for the description's fact block are the ledger rows, not this file.

## 5. What still has to happen

1. Generate the four background plates at 1280×720 or larger from the prompts above.
2. Render the four `<Still>`s with the headlines composited.
3. Measure `thumbnail_visibility` on each; lift any that fall under the luma floor.
4. Select T1, keep T4 as the paired variant, and record the choice in `09_package`.
