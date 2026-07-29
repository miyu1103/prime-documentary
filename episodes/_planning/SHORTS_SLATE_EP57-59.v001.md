# SHORTS_SLATE EP57–59 v001 — 9 Shorts for the three new episodes

**Created:** 2026-07-30 · **Status:** PLAN ONLY. Nothing rendered, nothing scheduled, no GPU used, no API written.
**Scope:** `short73`–`short81` (9 Shorts, 3 per episode) across EP57 fieldtest / EP58 lejeune / EP59 robosigning.
**Governing method (do NOT invent a new pipeline):** `SHORTS_METHOD.v001.md` (the 12 rules) + `SHORTS_REMOTION_SPEC.md` (Short.tsx data contract, safe areas) + `SHORTS_CONVERSION_v001.md` §4 (end CTA) + the build checklist in `SHORTS_SLATE_EP53-56.v001.md` §7, which is the working path and is unchanged here.
**Predecessor slate:** `SHORTS_SLATE_EP53-56.v001.md` reserves `short60`–`short72` and the slots up to 2026-09-01. This slate starts the day after.

> ⛔ **This slate is BLOCKED and cannot be built today.** See §0. It is written now so that the moment Codex finishes EP57–59's images the build is a checklist, not a design problem.

---

## 0. State of play (measured on disk, 2026-07-30)

| Episode | Slug | Script | AI stills on disk | i2v clips | VO master | Captions |
|---|---|---|---|---|---|---|
| EP57 | `fieldtest` | ✅ `EP57_fieldtest_script.en.v001.md` (7,178 w) | **11 of 267** (`S001`–`S011`) | none | ❌ | ❌ |
| EP58 | `lejeune` | ✅ `EP58_lejeune_script.en.v001.md` (7,810 w) | **7 of 267** (`S001`–`S007`) | none | ❌ | ❌ |
| EP59 | `robosigning` | ✅ `EP59_robosigning_script.en.v001.md` (7,855 w) | **6 of 267** (`S001`–`S006`) | none | ❌ | ❌ |

Paths: stills `H:\pd-media\assets\ai\<slug>\`, i2v `H:\pd-media\assets\ai_video\<slug>\` (none of the three exists yet). There is no `episodes/PD-2026-057-*` … `-059-*` directory yet — the three episodes still live entirely in `_planning`.

**Three consequences that shape every short below:**

1. **Every line is a re-record.** EP53–55's shorts cut 27 of 46 lines free out of an existing `vc_master_v001.mp3`. Here there is no master, so all 45 lines (9 shorts × 5) are synthesized. ≈ **1,350 words ≈ 7,800 characters ≈ $2.34** at the pipeline's $0.30/1k-char estimate. Trivial, and it means these shorts do **not** have to wait for the long-form VO — only for the images.
2. **No i2v anywhere.** EP54 could put real video in the hook (`kind:'video'`). These three cannot until Wan i2v is run on their `M##_src` seeds. Until then every hook is a depth-parallax still, which the owner has rejected as 紙芝居 when the cut rate is slow. **Mitigation, and it is a hard requirement here: ≥20 beats per short, no beat longer than 2.3 s** (the cadence used on `short60`/`short63`/`short66`).
3. **Plate IDs in this document are motif requests, not file paths.** ★ Learned the expensive way on 2026-07-30: three of `short60`'s plates picked by prompt ID off `EP53_norfolk_CODEX_A_ASSETS.v001.md` turned out to be a completely different picture on disk (the "top-down interrogation table" was an abstract card, the "microcassette" was a cup and ashtray, the "jail visiting booth" was an empty floor). **Never select a plate by reading the prompt list. Generate the episode's images, build a labelled contact sheet, and pick with your eyes** — then write the file numbers into `short<NN>.ts`. Same failure family as the factory-shelf mislabel incident; machine gates cannot see it.

---

## 1. Rules applied to every short in this slate

Identical to `SHORTS_SLATE_EP53-56.v001.md` §1 (1-second hook, no brand intro, open loop → payoff, 40–58 s, loop tail, muted-first with a pattern interrupt ≤2 s, faces/motion, franchise format, sub-conversion, persona, cross-platform, retention iteration), plus four that this slate tightens:

- **R-A. Beat floor.** ≥20 beats and ≥16 **distinct** plates per short; no plate twice in adjacent beats; the hook plate may recur only as the loop tail. (`short60` = 23 beats / 18 plates, `short66` = 24 / 23, `short63` = 23 / 22.)
- **R-B. Eyes-on plate selection.** §0.3 above. The contact sheet is an artifact of the build, not an optional check.
- **R-C. Face plates must match the person the beat names.** `short63` was about to put EP54's F07 — an illustrative white woman — on the beat naming James Bibbs, a Black man. Pulled at QC. If no face plate matches, carry the beat with hands/backs and meet METHOD rule 7 with motion instead.
- **R-D. Numbers are the franchise.** All three episodes are number-driven (416 · 0.0134 g · 408,000 · 2,446 · 10,000 a month · 350 an hour). Every short below lands one number as its telop payoff, and that number must trace verbatim to the episode's FACTS_LEDGER.

**Vertical-format constraints** (`SHORTS_REMOTION_SPEC.md` §4): 1080×1920 @30 fps. Telop zone y 180–560. Caption zone y 1280–1560. Nothing important at x>960 or y>1620. Citations top-left via `CitationTopLeft`, **never on the same beat as a top telop** (the short19 defect).

---

## 2. EP57 — the $2 field test (`fieldtest`) — 3 shorts

Format lane **F-B** ("the number that convicted her"). Locks from `EP57_fieldtest_FACTS_LEDGER.v001`: Amy Albritton is LIVING and her conviction was **set aside** — say so; the crumb was **not a controlled substance** (lab: N.A.M. / N.C.S.); the officer's roadside figure was **0.02 g** and the laboratory's was **0.0134 g**; the 416 count is Harris County's own, produced by its **own** conviction integrity unit; no officer is named or characterised as having lied — the film's claim is about the **instrument**, not about intent. Two items are flagged in the review log for re-confirmation before publish (the Colorado "first in the nation" line and the 1.5M/90%/46% error-rate figures) — **neither may appear in a short until confirmed.**

---

### short73 — "A two-dollar test turned blue. That was the whole case."

- **Slot:** 2026-09-02 (Wed) 12:00 JST · **Format:** F-B · **Target 46–52 s** · ~150 w, 100% re-record
- **Hook (first 1 s):** *"A police officer dropped a crumb from a car floor into a two-dollar vial of pink liquid. It turned blue. That was the entire test."* — frame 0 = the vial, mid-drop.
- **Open loop:** what was actually in the vial? **Payoff (last 3 s):** six months later a mass spectrometer said it was not a drug at all — and by then she had already pleaded guilty.

**Script source (ACT I / ACT IV, `EP57_fieldtest_script.en.v001.md`):**
> "That is the entire procedure. No machine, no reading, no printout, no second opinion. There is a colour."
> "It turned blue."
> "The fragmentation pattern did not match cocaine… It was not a drug."

**Line plan** — L1 hook 24 w · L2 the stop and the search 34 w · L3 the vial and the colour 32 w · L4 the laboratory 34 w · L5 CTA 26 w.
L5: *"Her conviction was eventually set aside. The full case is on the channel — follow for the cases they don't teach you."*

**Plate motifs (≥16, pick off the contact sheet):** roadside stop at dusk · a needle in a ceiling lining · an over-the-counter headache powder packet · **the crumb on a car floor mat (hero)** · the patrol-car trunk · **the pouch and the pink vial (hook)** · the lid coming off · **the liquid going blue (payoff of L3)** · a handwritten evidence form, illegible · handcuffs in a parking lot · a jail property envelope · a gas chromatograph–mass spectrometer · a printout of a fragmentation pattern, unreadable · a laboratory balance · an empty apartment · a set of keys handed back.
**Telops:** `IT TURNED BLUE` · `$2 TEST` · `NO MACHINE.\nNO PRINTOUT.` · `0.0134 GRAMS` · `NOT A DRUG`.
**Cover / ShortThumb:** background = the vial going blue · headline `A $2 TEST\nSAID GUILTY` · badge `NOT A DRUG`.
**CTA props:** `ctaLongTitle: 'A $2 Test Destroyed Her Life'` (28 ch) · `ctaHeadline: 'FULL CASE'` · `ctaLongThumbSrc: shorts/short73/short73_ctathumb.png`.

---

### short74 — "The prosecutors counted their own mistakes. There were 416."

- **Slot:** 2026-09-05 (Sat) 12:00 JST · **Format:** F-B · **Target 48–56 s** · ~155 w
- **Hook:** *"A district attorney's office went back through its own files and counted the people it had convicted on evidence that was never a drug. It stopped counting at four hundred and sixteen."*
- **Payoff:** every single one of them had already pleaded guilty.

**Script source (ACT IV, verbatim):**
> "Between January 2004 and June 2015, the office had failed to correct four hundred and sixteen variants. Every single one had ended in a guilty plea."
> "All two hundred and twelve of those people pleaded guilty. Ninety-three per cent were sentenced to jail or prison."
> "Notice who found this. Not a defence campaign, not a newspaper, not a federal investigation."

**Telops:** `416` · `EVERY ONE\nPLEADED GUILTY` · `93% JAILED` · `63% UNDER\nONE GRAM` · `THEY FOUND IT\nTHEMSELVES`.
**Plate motifs:** a wall of case files · a spreadsheet column, unreadable · a records room · a lone desk lamp over a stack · a courthouse corridor · a guilty-plea form, illegible · a cell door · a scale · an integrity-unit office at night.
**Cover:** headline `THEY CONVICTED\n416 PEOPLE` · badge `WRONG EVERY TIME`.

> **Lock:** the 416 figure and the 212 / 93% / 63% breakdown are Harris County's own audit. Do **not** write "the police lied" or attribute intent anywhere in this short.

---

### short75 — "The letter was mailed to the home the conviction took away."

- **Slot:** 2026-09-08 (Tue) 12:00 JST · **Format:** F-B · **Target 44–50 s** · ~145 w
- **Hook:** *"The letter telling her she had been convicted in error was posted to the apartment her conviction had cost her."*
- **Payoff:** she found out from reporters, years late, and answered in six words: *"I knew it! I told them!"*

**Script source (ACT IV, verbatim):**
> "It was posted to the address on her driver's licence. She was not there. That address was the apartment that came with the job, and the job had ended the day she pleaded guilty."

**Telops:** `DEAR SIR\nOR MADAM` · `MAILED 2014` · `SHE WAS\nNOT THERE` · `"I KNEW IT!"` · `CONVICTION\nSET ASIDE`.
**Plate motifs:** a form letter, unreadable · a mailbox with a stranger's name · an emptied apartment · a moving box · a returned envelope · a bar counter shift · a rental office desk · a courthouse door in daylight.
**Cover:** headline `THE LETTER\nWENT NOWHERE` · badge `TOO LATE`.

---

## 3. EP58 — Camp Lejeune (`lejeune`) — 3 shorts

Format lane **F-C** ("they knew, and nothing happened"). Locks from `EP58_lejeune_FACTS_LEDGER.v001`: Jerry Ensminger and Mike Partain are LIVING and named with dignity; Janey Ensminger is named once, never depicted. The film's claim is **documentary, not intentional** — the Army's laboratory wrote what it wrote; the script explicitly refuses to claim anybody understood it at the time, and **no short may cross that line**. There is **no official total** of people exposed — the widely-quoted ~1,000,000 is not a government figure and must not be used. Exposure window per statute: 1 Aug 1953 – 31 Dec 1987.

---

### short76 — "The Army's own laboratory wrote 'solvents!' in 1981."

- **Slot:** 2026-09-03 (Thu) 12:00 JST · **Format:** F-C · **Target 48–54 s** · ~150 w
- **Hook:** *"In 1981 the Army's own laboratory wrote nine words on a water-sample form. The last one ends in an exclamation mark."*
- **Payoff:** the form sat in a government file for sixteen years until a retired drill instructor asked for it.

**Script source (ACT III, verbatim):**
> "'Water highly contaminated with other chlorinated hydrocarbons — solvents!'"
> "That form has a number. It is CLW 0443, and it sat in a government file for sixteen years until a retired drill instructor asked for it."
> "Nothing happened. That is the finding, and it needs no adjective. The wells kept running. The families kept drinking."

**Telops:** `30 OCT 1980` · `9 MARCH 1981` · `"SOLVENTS!"` · `CLW 0443` · `WELLS OFF\n1984–85`.
**Plate motifs:** a base water tower at dawn · a sample bottle on a lab bench · a technician's handwriting in a form margin, unreadable · a gas chromatograph trace · a filing cabinet · a records-request envelope · a kitchen tap in base quarters · a well head being shut · a child's empty bedroom (no person).
**Cover:** headline `THEY WROTE IT\nDOWN IN 1981` · badge `NOTHING HAPPENED`.

> **Lock telop, mandatory on the final content beat:** `THE RECORD SAYS WHAT IT SAYS` — the short must not assert that anyone knowingly concealed it.

---

### short77 — "408,000 people filed. 2,446 have been paid."

- **Slot:** 2026-09-06 (Sun) 12:00 JST · **Format:** F-B · **Target 50–58 s** · ~160 w
- **Hook:** *"Congress opened a courthouse door that had been shut for thirty years. Four hundred and eight thousand people walked through it. Two thousand four hundred and forty-six have been paid."*
- **Payoff:** four years after the law passed, not one of those cases has been tried, and there is no trial date.

**Script source (ACT V, verbatim):**
> "By the middle of June 2026 the Department of Justice told the court the number: four hundred and eight thousand."
> "Not one of those cases has been tried. Four years after the law passed, there is no trial date."

**Telops:** `408,000 FILED` · `2,446 PAID` · `NO JURY` · `NO TRIAL DATE` · `THE WINDOW\nCLOSED 2024`.
**Plate motifs:** a federal courthouse in flat daylight · mail trays of claim forms · a television ad frame (no logos) · a docket screen, unreadable · an empty jury box · a settlement grid on paper · a calendar page.
**Cover:** headline `408,000 FILED\n2,446 PAID` · badge `NO TRIAL DATE`.

> **Locks:** the jury ruling and the 88%/2% documentation figures come from the court's own docket and the government's June 2026 filing — quote them as the government's characterisation, not as fact about any individual claim. **Do not** use the $405 line from the ending in a short: it is a costs figure inside a specific disposition and reads, out of context, as the value of a life. R3 flagged it.

---

### short78 — "A law can end your case before you know you are sick."

- **Slot:** 2026-09-09 (Wed) 12:00 JST · **Format:** F-C · **Target 46–52 s** · ~148 w
- **Hook:** *"North Carolina has a rule that can kill a lawsuit ten years after the harm — even if the illness has not appeared yet."*
- **Payoff:** it took an Act of Congress, named for a nine-year-old, to take the wall down.

**Script source (ACT V, verbatim):**
> "Unlike a statute of limitations, which starts running when you discover you were injured, a statute of repose starts running from the defendant's last act."
> "In 2012, the Janey Ensminger Act…"

**Telops:** `STATUTE OF\nREPOSE` · `10 YEARS` · `THE CLOCK STARTS\nWITHOUT YOU` · `2012` · `2022: THE DOOR\nOPENS`.
**Plate motifs:** a courthouse clock · a closed docket book · a legislative chamber (empty) · a signed bill on a desk, unreadable · a kitchen table with paperwork · a headstone in flat light (no name legible).
**Cover:** headline `THE CLOCK RAN\nWITHOUT THEM` · badge `30 YEARS`.

---

## 4. EP59 — the foreclosure signature machine (`robosigning`) — 3 shorts

Format lane **F-A** ("the machine that manufactures agreement"). Locks from `EP59_robosigning_FACTS_LEDGER.v001`: Charlie and Maria Cardoso owned the house **outright — no lender, no lien, no debt**; **Linda Green was a real person who did nothing wrong** and must be named that way in the same breath as the forgery; Jeffrey Stephan's and Chris Pendley's words are quoted from a deposition and a broadcast and must be verbatim; the two Stephan deposition quotes are flagged in the review log for a second verbatim check **before publish**. ★ Every plate in this episode must be checked for **readable signatures and readable text** — that is this episode's single biggest generation risk and it has its own gate (`A-DONE-6`).

---

### short79 — "He swore he had read ten thousand documents a month."

- **Slot:** 2026-09-04 (Fri) 12:00 JST · **Format:** F-A · **Target 48–54 s** · ~152 w
- **Hook:** *"A man in Pennsylvania swore, under penalty of perjury, that he had personally read every one of ten thousand documents a month."*
- **Payoff:** asked whether they were executed on his own personal knowledge, he answered: *"Right."*

**Script source (ACT III, verbatim):**
> "In a month, Stephan said, my team brings to me approximately, I'd say a round number of ten thousand."
> "So these documents wouldn't be actually executed on your own personal knowledge? Right, Stephan said."

**Telops:** `10,000 A MONTH` · `10,000 MINUTES\nIN A MONTH` · `HE DID NOT\nREAD THEM` · `NOT NOTARISED\nIN THE ROOM` · `"RIGHT."`.
**Plate motifs:** a document execution unit's desk · a stack of affidavits (all illegible) · a pen mid-signature, no letterforms · a wall clock · a notary stamp on a desk with nobody there · a courtroom where nobody appears for the homeowner · a judge's empty bench.
**Cover:** headline `10,000 SWORN\nDOCUMENTS` · badge `UNREAD`.

> **Quote handling:** the two Stephan lines are the payoff. They are on the R3 re-verify list — if the verbatim check has not been signed off, **this short does not ship**, and short80 or short81 takes the slot.

---

### short80 — "Linda Green was real. Dozens of people signed her name."

- **Slot:** 2026-09-07 (Mon) 12:00 JST · **Format:** F-A · **Target 46–52 s** · ~148 w
- **Hook:** *"One name appears on those mortgage documents more than any other — and the woman it belongs to did nothing wrong."*
- **Payoff:** *"So you're Linda Green?" — "Yeah. Can't you tell."*

**Script source (ACT IV, verbatim):**
> "Linda Green was real. In 2003 she was a shipping clerk for auto parts…"
> "So you're Linda Green, Pelley asked him. Yeah, Pendley said. Can't you tell."
> "Every one of those pages was filed with a county recorder."

**Telops:** `ONE NAME` · `MANY HANDS` · `350 AN HOUR` · `$10 AN HOUR` · `FILED WITH\nTHE COUNTY`.
**Plate motifs:** a low-rise office suite in an industrial park · rows of desks · a signature repeated down a page in different hands (no letterforms) · a notary seal · a county recorder's shelf of ledgers · a deed being stamped.
**Cover:** headline `ONE NAME.\nMANY HANDS.` · badge `FILED ANYWAY`.

> **Lock, non-negotiable:** the on-screen and spoken framing is always "Linda Green **was a real person who did nothing wrong**". Never a telop that reads as accusing her.

---

### short81 — "They paid cash for the house. The bank foreclosed anyway."

- **Slot:** 2026-09-10 (Thu) 12:00 JST · **Format:** F-A · **Target 48–54 s** · ~152 w
- **Hook:** *"They bought the house outright. No loan, no lender, nothing to fall behind on. In 2009 three men arrived to foreclose on it."*
- **Payoff:** the bank's **own** estate agent told it that it was foreclosing on the wrong house — and it went ahead.

**Script source (ACT I, verbatim):**
> "When the Cardosos paid cash, no lender was involved. Nobody held a lien on the place. There was no loan to fall behind on."
> "The real estate agent that Bank of America itself had hired to handle the property contacted the bank to tell it that it was foreclosing on the wrong house."
> "Their own real estate agent told them, and nevertheless Bank of America steamrolled right ahead."

**Telops:** `PAID CASH` · `NO LOAN.\nNO LIEN.` · `THEY CAME ANYWAY` · `ITS OWN AGENT\nTOLD IT` · `IT KEPT GOING`.
**Plate motifs:** a three-bedroom house with a pool in flat Florida light · a deed, unreadable · an empty driveway · a broken fence with mower tracks · a lockbox on a front door · a notice taped to glass, illegible · a phone handset on a kitchen counter · a pool going green.
**Cover:** headline `THEY PAID CASH` · badge `FORECLOSED`.
**CTA props:** `ctaLongTitle: 'He Paid Cash'` (12 ch) · `ctaHeadline: 'FULL CASE'`.

---

## 5. Schedule (one short per day, 12:00 JST)

Audited live with `python scripts/yt_schedule_audit.py` on 2026-07-30 (read-only; the channel API is the source of truth — do **not** re-derive this from local manifests). After that day's bookings, 28 uploads carry a future `publishAt` and the last is **2026-08-24** (`short60`/`short63`/`short66`). **8/14 and 8/15 are open** — a two-day hole left when those three were moved to consecutive days — and the ten unbuilt shorts of `SHORTS_SLATE_EP53-56.v001.md` come before this slate.

> **Rule the owner set on 2026-07-30, and it binds this slate too: a batch runs on CONSECUTIVE days in NUMBER order.** Do not scatter a batch across a backfilled hole. Fill holes with a separate, earlier batch.

The table below is therefore a shape, not a booking: **re-derive the actual dates from a live audit at build time**, keeping the interleave and the one-per-day cadence.

| Date (JST) | Day | Short | Episode | Working title |
|---|---|---|---|---|
| 2026-09-02 | Wed | `short73` | EP57 | A $2 test turned blue |
| 2026-09-03 | Thu | `short76` | EP58 | They wrote it down in 1981 |
| 2026-09-04 | Fri | `short79` | EP59 | 10,000 sworn documents |
| 2026-09-05 | Sat | `short74` | EP57 | 416 |
| 2026-09-06 | Sun | `short77` | EP58 | 408,000 filed, 2,446 paid |
| 2026-09-07 | Mon | `short80` | EP59 | One name, many hands |
| 2026-09-08 | Tue | `short75` | EP57 | The letter went nowhere |
| 2026-09-09 | Wed | `short78` | EP58 | The clock ran without them |
| 2026-09-10 | Thu | `short81` | EP59 | They paid cash |

Episodes are interleaved 57 → 58 → 59 so no case runs two days straight and the footage load spreads across three separate still libraries (`footage_diversity` intent).

> **Funnel dependency.** None of EP57–59's long-forms exists. Schedule the short, but **do not** post the pinned comment or set the Studio Related-video until the matching long-form is public — the same hold that already applies to `short57`–`short59` and the EP53–56 slate.

---

## 6. Build order (what unblocks what)

1. **Codex finishes the episode's images** (EP57 11/267 · EP58 7/267 · EP59 6/267). This is the only hard blocker. `CODEX_A_ASSETS.v001.md` per episode is the generation contract; ★ EP59 additionally requires `A-DONE-6` (no readable text / no readable signature) to pass on all 267.
2. **Contact sheet + eyes-on pick** (§0.3 / R-B). Reject any plate with readable typography, a legible signature or an official-looking seal, and any plate whose content does not match the beat it was picked for.
3. **Write `short<NN>_lines.v001.json`** under `episodes/<EP>/09_package/` — all five lines `source: "rerecord"` here.
4. **`gen_newshort_narration.py --short NN --ep <EP> --text-json …`** (dry-run first for chars/$; voice `nPczCjzI2devNBz1zQrb`, `eleven_multilingual_v2`; delivery arc L1 intense → L5 calm).
5. **`build_short_mix.py --short NN --ep <EP>`** → `short<NN>_timing.ts` + the −14 LUFS mix. Check `SHORT<NN>_TOTAL_SEC ≤ 58`; if over, re-run step 4 with `--gap 0.45`.
6. **Copy plates → `remotion/public/shorts/short<NN>/`, `gen_depth_maps.py --dir …`** (every `short<NN>_XX.png` needs `short<NN>_XX_depth.png` or the render crashes).
7. **Write `short<NN>.ts`** on the `short60.ts` / `short66.ts` pattern (doc-comment carrying the locks, `CUTS`, `buildBeats()`, the loop tail, and the three `ctaLong*` props).
8. **Register three compositions in `Root.tsx`**, `npm run typecheck` clean.
9. **Render** via a slim public dir — `remotion/public` is **176 GB** and Remotion copies the whole `--public-dir` into its bundle. Build `remotion/public_shorts_slim` with hardlinks (`cp -rl`), fonts included; symlinks silently produce an empty bundle (failure F-18b).
10. **`bash scripts/coverfirst.sh <NN>`**, then measure — `ffprobe` for 1080×1920 / 30 fps / ≤58 s, no static hold >2 s, telops unobstructed, no `SUBSCRIBE` in frame, TikTok cut free of any external platform name.
11. **Schedule** with `scripts/schedule_short_youtube.py --short NN --publish-at <UTC>` (12:00 JST = 03:00 UTC) after adding the short's metadata to that script's `CONFIG` dict. Privacy `private` + future `publishAt`.

---

## 7. Totals

- **9 new shorts**, 3 per episode, `short73`–`short81`.
- **Audio: 100% re-record** — ≈1,350 words ≈ 7,800 characters ≈ **$2.34**. No dependency on the long-form VO.
- **Images: 0 usable today.** 24 of 801 plates exist across the three episodes (3.0%).
- **Schedule:** 2026-09-02 → 2026-09-10, one per day at 12:00 JST, zero collisions with the 25 reservations on the channel and with the EP53–56 slate's 8/14 → 9/01.
