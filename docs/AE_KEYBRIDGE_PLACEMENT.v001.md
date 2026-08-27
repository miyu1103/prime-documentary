# EP77 keybridge — where the six AE cards go, and how they would reach the film

**Status:** proposal. Nothing here is implemented. Written 2026-08-27.
**Binding on:** nothing yet. ADR-0011 binds this document, not the other way round.
**Scope:** the six cards that exist on disk as transparent webm. The wiring section (§4) is a
proposal for the owner to accept or reject; §1–§3 are measurements and a placement table.

---

## 0. What was measured, and when

Every number below came from a command, not from a document.

| what | measured value | how |
|---|---|---|
| cards installed | **11** of 14, in `remotion/public/keybridge/ae/` | `ls`; six were there on 2026-08-26, five more were rendered 2026-08-27 |
| still missing | `keybridge_ae007` (system_map), `keybridge_ae011` (comparison), `keybridge_ae014` (timeline) | all three are now **buildable** — the five missing kinds landed in `kinetic_card.jsx` on 2026-08-27 |
| every installed card | 1920×1080, 30.00 fps, `alpha_mode=1`, duration = its `seconds` to within 0.01 s | `scripts/ae/verify_cards.py` |
| film | `remotion/src/data/keybridge_film.json` — 241 cuts, 504 captions, 71 figures, `narrationSeconds` 1624.758, `hookSeconds` 17.9, `leadSeconds` 0.0, `openingVariant` `overlay` | read directly |
| cut starts | body-relative; `leadSeconds` is 0, so they are also absolute within `<Sequence name="Body">` | `CaseFilm.tsx:822` |
| AE assets reachable by the film today | **0** | see §4 |

Timestamps in this document are **body-relative seconds** — the same clock the film json's
`cuts[].start` uses. With `leadSeconds: 0` that is also the film's own clock.

---

## 1. The placement table

`snap` is the recommended start. Where a cut boundary fell within 1.0 s of the sentence, the card
is snapped onto it so the card's entrance and the picture change land together; otherwise the
sentence wins. Script lines are `episodes/PD-2026-077-keybridge/03_script/script.en.v001.md`.

| # | card | kind | start | dur | ends | cuts it covers | script | the line it lands on |
|---|---|---|---|---|---|---|---|---|
| 1 | `keybridge_ae001` | hero_number | **0:04.00** | 8.0 | 0:12.00 | cut-0000 → cut-0001 | `:9` | "At twenty-seven minutes and fifty-three seconds past one in the morning, a duty officer in Baltimore gave an order to stop the traffic." |
| 2 | `keybridge_ae005` | hero_number | **3:15.17** | 8.0 | 3:23.17 | cut-0029 → cut-0030 | `:71` | "At about twenty-five minutes past one, she was six tenths of a mile out." |
| 3 | `keybridge_ae013` | quote_card | **14:35.86** | 10.0 | 14:45.86 | cut-0130 → cut-0131 | `:267` | "Before a word of it: an indictment is merely an accusation, and all defendants are presumed innocent until proven guilty beyond a reasonable doubt in a court of law." |
| 4 | `keybridge_ae010` | list_build | **15:09.58** | 10.0 | 15:19.58 | cut-0135 → cut-0136 | `:271` | "They are charged with conspiracy to defraud the United States, with willfully failing to immediately inform the Coast Guard of a known hazardous condition, with obstruction of an agency proceeding, and with false statements." |
| 5 | `keybridge_ae012` | hero_number | **20:38.56** | 8.0 | 20:46.56 | cut-0183 → cut-0184 | `:352` | "Sixty-eight bridges in the United States for which the NTSB recommended a vulnerability evaluation." |
| — | `keybridge_ae003` | title_card | **unplaced** | 7.5 | — | — | none | see §2 |

Exact snap deltas, so nobody has to re-derive them: ae001 +0.00 (no boundary within 1 s of 4.00 —
the nearest is 6.57), ae005 −0.03, ae013 +0.18, ae010 −0.04, ae012 +0.00 (the caption start and
a cut boundary are 0.00 apart here by coincidence, cut-0183 runs 1233.32–1240.11).

**ae013 must precede ae010, and it does: 14:35.86 vs 15:09.58, a 33.7 s gap.** That is the
script's own order — `:267` puts the presumption of innocence before `:271` states the counts —
and it is the legally careful one. If either card moves, this ordering is the constraint that
survives; do not let a timing tweak invert it.

**Every card spans a cut change.** Cuts here run 6.57–6.79 s and cards run 8–10 s, so this is
unavoidable and it is fine: an AE plate composites *over* the picture and the picture keeps
cutting underneath. It is also a small gift — a cut hidden under a held graphic reads as
deliberate. It is the reason the snap in §1 matters more than usual: if the card's entrance is
0.2 s off the cut it lands on, both moves are visible and neither reads as intended.

### Two duplications the cards inherit from their copy, which are worth fixing before ship

Not defects in the component — defects in `scripts/ae/jobs_keybridge.json`, visible in the
rendered frames:

- `ae002` (timeline) headline is `SIXTY-SEVEN SECONDS` and its big value renders `67 SECONDS`.
  The card says the same thing twice, in two sizes.
- `ae004` (map_move) big value renders `0.6 MILES` and its single caption line is
  `0.6 MILES FROM THE BRIDGE`. Same.
- `ae006` (comparison) column labels are `IN PORT` / `UNDER WAY` and every row underneath
  re-states `IN PORT:` / `UNDER WAY:`. The prefixes can come out; the columns already say it.

Neither card is placed by this document, so none of this blocks §1.

---

## 2. `keybridge_ae003` "26 MARCH 2024" — it has no home in the script

**Measured, not inferred.** The string "26 March" does not occur in the script. Every date
sentence in the narration is the *twenty-fifth*:

| script | body time | line |
|---|---|---|
| `:20` | **0:38.15** | "On the night of the twenty-fifth of March, 2024, that crew was on the Francis Scott Key Bridge in Baltimore, patching the deck." |
| `:431` | **26:49.12** | "That list did not exist on the twenty-fifth of March, 2024." |

The date on the card is not wrong. Its declared source, `KB-002`
(`episodes/_planning/EP77_keybridge_FACTS_LEDGER.v001.md:42`), reads: *"Contact occurred **26
March 2024, about 01:29 eastern daylight time**"*. Both dates are true — the crew went up on the
night of the 25th and the ship hit the pier in the small hours of the 26th. The script simply
chose the 25th, everywhere, and never explains the rollover.

So there is no sentence to hang it on, and the two nearest sentences are actively hostile to it:
a card reading `26 MARCH 2024` beside narration saying "the twenty-fifth of March" puts two
different dates in the eye and the ear inside one second. That is the shape
`check_packaging_claims.py` calls `NUMBER_MISMATCH`, and it would be a real one even though
neither number is false.

**Its declared act is `OP`** (`jobs_keybridge.json:36`), i.e. title-sequence furniture, not
narration — which is a coherent intent for a datestamp. But the OP slot is occupied: with
`openingVariant: "overlay"`, `CaseFilm.tsx:805` puts `<BrandOpening variant="overlay">` at
`(hookSeconds + 0.2) × fps` = **0:18.10**, inside cut-0002. Dropping a second full-frame title
graphic into the same 3.5 s is two title cards fighting, and it still pre-echoes a date the
narration contradicts twenty seconds later.

### Three ways out. This is the owner's call; I am not choosing one.

| | what to do | cost | what it buys |
|---|---|---|---|
| **a. hold it** *(default — costs nothing)* | leave ae003 out of v001. The webm stays on disk. | zero | Five cards that place themselves from the script. No contradiction on screen. Nothing downstream needs ae003: six cards already miss ADR-0011's ≥12 / ≥90 s floors (see §3), so dropping one changes no gate result. |
| **b. re-cut the copy** *(the one real fix)* | change the headline to agree with the narration — `THE NIGHT OF 25 MARCH 2024`, or `25–26 MARCH 2024` if the rollover is worth showing — then place it at **0:38.15** on cut-0005/cut-0006, against `:20`. | one card, ~15 s of AE (`render_cards.sh scripts/ae/jobs_keybridge.json keybridge_ae003`) | ae003 then places itself from the script like the other five, and the OP collision disappears. The ledger still supports it: KB-002 gives the 26th, KB-004 and the script give the night of the 25th. |
| **c. place it as-is at the contact** | **5:06.25**, cut-0045, `:108` "At about twenty-nine minutes past one, the Dali struck pier number seventeen." | zero | This is the only sentence in the film whose cited row *is* KB-002, and 01:29 on the 26th is the moment the date names. But the audience heard "the night of the twenty-fifth" four and a half minutes earlier and gets no reconciliation, so the contradiction is deferred rather than removed. |

Recommendation: **(b)** if anyone is willing to spend fifteen seconds of After Effects,
**(a)** otherwise. Not **(c)**.

---

## 3. What the six do *not* do

ADR-0011's clarification of 2026-08-23 sets floors of **≥12 beats, ≥1 per act, ≥90 s on screen**.

| floor | six cards | all fourteen declared |
|---|---|---|
| beats | 6 | 14 ✓ |
| seconds on screen | **51.5** | **124.5** ✓ |
| one per act | HOOK, OP, ACT_1, ACT_3, ACT_4, ENDING — **ACT_2 has none** | all seven ✓ |

Two things follow. First, six cards is roughly half the declared design and the film should
carry more of it before anyone measures EP77 against the ADR. Second, all fourteen kinds are now
buildable: eleven are rendered and verified, and `ae007` / `ae011` / `ae014` need only a run of
`render_cards.sh`. ACT_2's gap is filled by ae006 and ae007, both of which exist or can be built
today.

One note for whoever places the rest: `ae004` (0.6 miles out) and `ae005` (01:25) both attach to
the **same sentence**, `:71` at 3:15.20 — "At about twenty-five minutes past one, she was six
tenths of a mile out." They cannot both start there. ae005 has the snap in §1; ae004 needs its
own beat, and the obvious one is `:108` / 5:06 if ae003 does not take it.

---

## 4. How a card would reach the film — the smallest change that respects ADR-0011

### 4.1 What is true today, measured

| | file:line | state |
|---|---|---|
| the asset scanner | `scripts/build_asset_manifest_motionfirst.py:145-165` | scans `img/`, `motion/`, `factory/`, `overlay/` by flat `iterdir()`. **There is no `ae` class and no `ae/` scan.** `.webm` is already an accepted extension for all three video classes. |
| the film builder | `scripts/build_case_film_generic.py:800-812` | writes `overlays: [...]` from the manifest's `overlay` class, and cut objects with keys `id, start, dur, kind, src, seed, act` (+`srcSeconds`, `treatment`, `lift`). **It never writes a per-cut `overlay`.** |
| keybridge's film | `remotion/src/data/keybridge_film.json` | 241 cuts, **0** with an `overlay` key, `overlays: []`. Across all 54 `*_film.json`: **0** cuts with a non-null `overlay`. |
| the top-level `overlays` key | `CaseFilm.tsx` | appears **once**, inside a prose comment at line 30. Not in the `FilmData` type (67–104). **Dead key** — 17 films populate it and it renders nothing. |
| the per-cut `overlay` field | `CaseFilm.tsx:490-516` | *is* read and rendered — but with `opacity: 0.28`, `mixBlendMode` defaulting to `plus-lighter`, `objectFit: 'cover'`, and **no `transparent` prop**. That is a light-leak compositor. Type run through it arrives at 28% on an additive blend with its alpha plane discarded. |
| `heroCuts` | `CaseFilm.tsx:83, 842-852, 529-545` | read and rendered full-frame over the graded body, under the captions. **No `transparent`**, plus `objectFit: 'cover'` and a Ken Burns `transform`. Built for opaque Blender mp4s. `build_case_film_generic.py` never writes it. |
| the render's public dir | `scripts/build_render_public_dir.py:40` | `POOL_DIRS = ("img","motion","motion2","factory","overlay","stock")`. **`ae` is absent.** Remotion bundles whatever is under `--public-dir` (`pd_render_guarded.sh:38`), so an unlinked `ae/*.webm` **404s mid-render**, and `verify()` (67–87) only checks `cuts[].src` so it would not report it. **This is the actual blocker.** |
| the working precedent | `remotion/src/compositions/Short.tsx:1005-1023` | Shorts composite AE plates correctly and have for ~70 episodes: `<OffthreadVideo src={staticFile(b.src)} transparent muted style={{width:'100%',height:'100%'}} />` inside a `<Sequence from={atSec*fps} durationInFrames={durSec*fps}>`, wrapped in an `AbsoluteFill` with `pointerEvents:'none'`, mounted at line 1058 **after** the cuts and **before** the caption band. Data field: `kineticBeats?: {src, atSec, durSec, phrase?}[]` (125–130, 161), written as literals in `remotion/src/data/shortNNN.ts`. |

The docstring at `Short.tsx:1000-1004` already states the trap in writing: *"`transparent` is not
optional: without it Remotion's frame extractor decodes the WebM without its alpha plane and the
overlay arrives as type on a black card that hides the picture."*

### 4.2 The proposal — four touches

**A. `remotion/src/compositions/CaseFilm.tsx` — one optional field, one small component.**

Add to `FilmData`:

```ts
  /** AE plates (ADR-0011). Optional: a film without the key gains no element. */
  aeBeats?: {src: string; atSec: number; durSec: number; phrase?: string}[];
```

and an `AeBeatLayer` with the same body as `Short.tsx`'s `KineticBeatLayer` — `transparent`,
`muted`, `width/height: 100%`, **no `objectFit`, no `mixBlendMode`, no `opacity`** — mounted
inside `<Sequence name="Body">` immediately after the `heroCuts` map (line 852) and before
`<Captions>` (853). That is the same stack position Shorts uses: over the graded picture, under
the caption band.

*Why not extend one of the two existing channels (invariant 14).* Both were examined:

- The per-cut `overlay` is not a generic compositor, it is a specific effect — 28% opacity on an
  additive blend, for particles and light leaks, deliberately. Making it carry legible type means
  changing those three properties, and 0 films use it today but the code path is shared; the
  change would be silent and untestable.
- `heroCuts` is closer and is the honest alternative: it already renders full-frame in the right
  stack position, and `check_motion_density.py:183` already counts it. Reusing it would mean
  adding an opt-in flag (`transparent?: boolean`) that also suppresses `objectFit:'cover'` and
  the Ken Burns transform — three conditionals inside `HeroCut` rather than one new component. It
  is a smaller diff. It is rejected here for two reasons and the owner may overrule both:
  a Ken Burns drift on a 1920×1080 type card pushes glyphs out of the safe area, and folding AE
  plates into the same field as pre-composed 3D hero videos makes them indistinguishable to the
  density gates, which weight the two differently.

**B. `scripts/build_render_public_dir.py:40` — add `"ae"` to `POOL_DIRS`.** One word. Without it
nothing above matters: the plate is not in the bundle and the render 404s.

**C. Registration, per ADR-0011 §"AE output is a plate".** Two small pieces:

- `scripts/build_asset_manifest_motionfirst.py` — one more `scan()` beside the existing four, for
  `ae/`, emitting an `ae` class plus `counts.ae`. It is a flat `iterdir()` like the others and
  `.webm` is already accepted, so it is a line, not a feature. Note: `asset_manifest.v003` has
  **no schema file** in `schemas/` (its class list lives only in those Python literals), so there
  is no schema migration — but any reader that iterates `counts` should be checked before this
  lands.
- Provenance and the pixel receipt: have `scripts/ae/verify_cards.py` emit
  `runs/ae_qc/<slug>_cards.v001.json` — per card, its `id`, `kind`, `source` ledger row from the
  jobs file, `sha256` of the installed webm, the measured contrast per zone, and the path of the
  QC frame a human looked at. That single artifact satisfies both ADR-0011 requirements at once:
  "registered like any other asset" and "a verify step that reads pixels".

**D. `scripts/build_case_film_generic.py` — write `aeBeats` from a placement file.** The table in
§1 in machine form, as `episodes/PD-2026-077-keybridge/08_edit/ae_placement.v001.json`
(`[{id, atSec, durSec}]`); the builder resolves each `id` to `<slug>/ae/<id>.webm`, drops any id
with no file on disk, and writes `aeBeats`. **If it also writes `externalKineticBeats`, it must
never write that key alone** — `check_motion_density.py:184` and `check_animation_mix.py:228`
both count it, `grep -rn externalKineticBeats remotion/src` returns nothing, and
`build_lech_film_data.py:173-181` writes it with no `src` at all. Writing only that key turns the
density gate green with nothing on screen.

### 4.3 Why this satisfies ADR-0011

*"AE output is a plate, not a live layer… The film json never depends on AE being installed."*
Under this proposal the builder reads two things: a placement json and the webm files already
sitting in `remotion/public/<slug>/ae/`. After Effects is never invoked at film-build time or at
render time. On a machine with no AE, an empty `ae/` directory yields `aeBeats: []` and the film
renders exactly as it does today. The plate is produced by a separate, already-existing runner
(`render_cards.sh`), verified by a separate pixel-reading step, and cut in by Remotion — which is
the ADR's sentence, unaltered.

### 4.4 What this would touch, plainly

```
remotion/src/compositions/CaseFilm.tsx        +1 optional type field, +1 component (~14 lines), +1 mount line
scripts/build_render_public_dir.py            +1 word in POOL_DIRS          <- without this, nothing works
scripts/build_asset_manifest_motionfirst.py   +1 scan() call, +1 counts key
scripts/ae/verify_cards.py                    + a receipt writer
scripts/build_case_film_generic.py            + read placement json, + write aeBeats
episodes/PD-2026-077-keybridge/08_edit/ae_placement.v001.json   (new, this document's §1 table)
```

**Not touched:** `scripts/ae/kinetic_beat.jsx` and `remotion/src/compositions/Short.tsx` (the
Shorts path is working and is only the template here), the per-cut `overlay` field, `heroCuts`,
the dead top-level `overlays` key, and all 54 existing `*_film.json` — none of which gains an
element, because every addition is an optional key that no existing film sets.

---

## 5. Reproducing the measurements in this document

```bash
# the cards, probed and read as pixels (writes QC frames to runs/ae_qc/)
py -3.11 scripts/ae/verify_cards.py --jobs scripts/ae/jobs_keybridge.json

# build the three that are still missing (ae007 / ae011 / ae014)
bash scripts/ae/render_cards.sh scripts/ae/jobs_keybridge.json \
     keybridge_ae007 keybridge_ae011 keybridge_ae014
```

`render_cards.sh` refuses by name any kind `kinetic_card.jsx` cannot draw, refuses to render when
the build log is dirty, and clears `PriorSafeMode.txt` before launching AE. None of those three
guards may be weakened to make a card ship.
