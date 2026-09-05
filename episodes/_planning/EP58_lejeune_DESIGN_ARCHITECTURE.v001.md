# EP58 — IT WAS THE WATER (Camp Lejeune · Jerry Ensminger and Mike Partain) — DESIGN ARCHITECTURE (v001)
### The creative + quality + guardrail spine for EP58 (30-min case film). This is the SOURCE OF INTENT that CODEX_A and CODEX_B both inherit. Where a later doc conflicts with this one on VISUAL INTENT or QUALITY BAR, this wins.

> episode_id `PD-2026-058-lejeune` · slug `lejeune` · EP58 · fps 30 · 1920×1080 · id `Ep58Lejeune` · target **30:00** (band 29.0–31.0 min = 1740–1860 s)
> Companions: `EP58_lejeune_script.en.v001.md` (LOCKED voice, **4,738 spoken words** — R3-relocked 2026-07-29), `EP58_lejeune_FACTS_LEDGER.v001.md` (the ONLY fact source; CL-numbers), `EP58_lejeune_CODEX_A_ASSETS.v001.md` (asset generation), `EP58_lejeune_CODEX_B_BUILD.v001.md` (build/render — to be written). CTR packaging = CTR_PLAYBOOK §4A.
> **HARD FRAME (from the ledger):** **Jerry Ensminger and Mike Partain are LIVING public advocates who have testified before Congress under oath** — their existence, positions, actions and sworn words are statable and quotable, and both were confirmed alive and active in July 2026 (CL-18 / CL-26b; the 2021 Find A Grave decedent of the same name is a different man). **NO LIKENESS of either man, of Janey Ensminger, or of any officer, official, judge or legislator.** **Janey Ensminger died at nine on 24 September 1985: ONE narration passage, her father's own sworn wording as the ceiling, never sentimentalised — and NEVER DEPICTED. No sick or dying child anywhere in this film, and no healthy child either; grief is carried by objects, absence and adult figures. No medical imagery of any kind (no bed, no drip, no chart, no procedure), no coffin, no memorial marker in close-up.** **The villain is institutional.** **No individual has ever been charged, disciplined or reprimanded** — a federal criminal investigation was completed and declined in 2007 (CL-44) — so no officer or official is named as a wrongdoer, and the dry-cleaner's private proprietors are never named (CL-45). **No court has ever found the United States liable.** **Causation is the fatal-defect risk: "associated with," never "caused"** — ledger §W is binding on narration, on-screen text, AE copy and every CODEX prompt.

---

## 0. THE QUALITY BAR (what "past-best" means, operationally)
This film is judged against every prior episode and must beat them on all five axes at once. None is optional.

1. **Restraint that is also dense.** The *tone* is quiet — a father, a form, and forty years of arithmetic; no melodrama, no horror grammar, no swelling strings under a dead child. The *motion* is relentless — something is always animating with intent. A still, silent hold of 4+ seconds is a FAILURE unless it is a deliberate, earned breath (max 3 in the whole film, each ≤2.5s).
2. **Every cut earns its place.** **563 cuts** across ~30 min; mean_shot ≈ 3.16s, max 7.0s. still-share ≤ 0.45 (design 0.4334). first-use ≥ 0.70 (design 0.8650). **avg uses/source ≤ ~1.4 (design 1.156)**; distinct source count 487.
3. **Premium motion density (HARD).** **≥ 82 in-film FigureBeats** (≥2.5/min → floor 75; design **86** = 2.88/min), variety ≥ 6 kinds (design 15), plus **17 AE hero cards** composited on top. `motion_density` and `animation_mix` gates must PASS before any render is called final.
4. **Zero legibility/quality defects.** No garbled captions, no clipped AE text (measured-fit mandatory), no black frames, no desync (VO onset 0.0 — HOOK-AUDIO standard), **no `dochighlight` figure (BANNED)**, **no `DATE_STAMP` / `SEAM_TRANSITION` AE layout (BANNED — they do not exist in the JSX and crash the build; date cards are `CENTER_STACK`)**, **no `depth`-displacement footage treatment (BANNED, §1)**, no global haze wash (screen-wash ≤ 0.07).
5. **Truth, with dignity.** Every on-screen number, name, date and quote traces to the FACTS_LEDGER at high confidence or is hedged in copy or cut. **The five corrections at the head of the ledger are binding: no "~1,000,000 exposed"; Janey was conceived at Camp Lejeune and not, on this record, born there; the television belongs to Partain and not to Ensminger; the Grainger chemist on the record is Babson, not Hargett; the "250-gallon tank" is unsourceable and is cut.**

If any one of these fails, the episode is not done — regardless of how good the rest looks.

---

## 1. VISUAL LANGUAGE (the elevated system)
One palette, one grammar, so the three spine objects — **the tap and the glass**, **the carbon-copy form**, and **the father's binder** — can accumulate meaning for twenty-five minutes and detonate in Acts III and V.

- **Accent — chlorinated tap-water aqua `#4FA3B4`** = RGB (79,163,180) = normalized **[0.310, 0.639, 0.706]**. The colour of water under a kitchen light: the system colour for type accents, the figures lane, and every tap, glass, pipe, valve and sample bottle in the film. INK base `#090B0C`. Bone-white `#EAE7DE` for type. ★Deliberately separated from EP50 "steel-cyan" (there: the accent, on urban metal) and EP52 "evidence-blue #3F5E8C" (there: a cold evidence note) — this is a *water* colour and appears wherever water does and nowhere else.
- **Environmental note — pine-and-clay dusk `#7A5236`** — **EXTERIORS ONLY** (loblolly treelines, red-clay road shoulders, the base perimeter at last light). Never on type, figures or cards. ★Separated from EP43 "porch-amber" and EP41 "sodium prison gold": those are light sources; this is *earth and bark*, and it never illuminates anything.
- **Dread note — solvent-drum ochre `#B0762A`** — used on **≤6 beats total**, ONLY on degreaser drums, disposal-yard metal and the storage-tank seam. It is the only colour in the film that means something bad. It never floods the frame.
- **One reserved COLD-DAYLIGHT note — record-daylight `#D6E0E4`** = RGB (214,224,228). Appears ONLY at the 2007 and 2010 hearing rooms, the 2012 and 2022 signings, and the ENDING — and NOWHERE else. **This is the visual thesis: the only light this story ever earns is the flat daylight of a public record.** It is deliberately *cold* relief, not warm — a warm-amber redemption note would sentimentalise a dead child, which is banned.
- **People (anonymized, non-identifiable — DELIBERATELY PRESENT).** **85 of the 210 body stills (40.5%)** and **18 of the 42 motion seeds** carry anonymized figures (backs, hands, silhouettes — **adults only**). Roles: a family carrying cartons into base quarters; hands at a sink; a formation cropped below the waist; a man alone at a kitchen table under one lamp; a technician's hands on a dial and a pen; a records trolley in a corridor; a hearing gallery from behind; a queue outside a government office; an older adult's hands on the arms of a chair; a figure walking away at dawn. **Anti-samey rule:** no two human-present stills may share subject + composition + lighting (CODEX_A §5.5a-5 variety matrix + Q4 phash watch-list). What stays banned absolutely: **any real-person likeness; ANY child, sick or healthy; any medical bed, drip, chart or procedure; any coffin, funeral or close memorial marker; any real unit patch, insignia, rank device or corporate logo; readable fake documents.**
- **Recurring motifs (build a vocabulary, then pay it off):**
  - **The tap and the glass (SIGNATURE A):** state chain — *running and ordinary* (hook) → *filled in daylight, unremarked* (Act I) → *standing full and untouched while the form exists* (Act III) → *shut off over a dry sink* (Act III close) → *standing on a hearing table* (Act V) → *empty in dawn light* (ENDING). Water is always the aqua note; the glass is always plain.
  - **The carbon-copy form (SIGNATURE B):** a printed analytical result form on a metal clipboard, all type and handwriting an unreadable smear. States — *blank* → *written in the margin* → *carbon lifted* → *slid into a folder* → *boxed on a shelf* → *returned redacted* → *stacked as an exhibit*. Seven states, one or two frames each, no more.
  - **The father's binder (SIGNATURE C):** a thick three-ring binder with blank tabs. *Empty and opened* (Act II) → *tabs multiplying* → *a shelf of them* (Act IV) → *carried to a hearing table* (Act V) → *closed on a kitchen table at dawn* (ENDING). It is the film's macro loop and its last image.
  - **The absent child:** a tricycle standing still on a concrete walk; an empty swing; a chair pushed back from a laid table. **Never a child.** These carry the grief and they are used sparingly — four beats in the whole film.
  - **The wells:** a pump house running → a capped well head in long grass → a padlock closing on the compound gate.
  - **The quarters:** the same brick duplex row in *1970s morning* → *winter dusk* → *dawn now*. Three states only.
  - **The queue and the counter:** claim forms stacking, mail trays overflowing, a line along a wall — the scale of Act V, rendered as paper and shoulders, never as a graphic of people.
- **Type & motion grammar:** all reveals use `overflow:hidden` + translateY mask lifts (house style); easing spring OR `Easing.out(Easing.cubic)` — NEVER linear; multi-element reveals STAGGER 2–4 frames; fast moves get `@remotion/motion-blur` Trail. Opacity NEVER alone — always paired with translateY/scale.
- **Clear image, no wash (HARD).** No global haze/fog/vignette-wash, no scanline/CRT texture. Neutral minimal grade inside the aqua-and-grey system, screen-wash opacity ≤ 0.07.
- **Footage treatment — `bleed`/`parallax`/`duotone`/`focus`, NEVER `depth` (HARD).** No depth maps, no `depth_path` anywhere.
- **Sound design intent (for B):** dread by ambience, never by acted distress — a tap running and stopping, water in a glass, the specific rattle of a three-ring binder closing, paper, a filing drawer, cicadas and a screen door in the Act I warmth, fluorescent hum in the corridors, coastal wind. **A single recurring leitmotif: one drop of water, used sparingly, and never over the Janey passage.** **HARD BAN: no screams, no acted human distress audio, no real-person archival audio, no hospital sound of any kind.** Brian narration + dramatized ambience/SFX only.

---

## 1a. ★★ THE FOUR-LAYER BUDGET (owner directive 2026-07-29 — binding on CODEX_A and CODEX_B) ★★

This film is **not** mainly AI stills. It is built from four layers, and the budget is fixed in *cuts*:

| Layer | What it is | Cuts | **% of 563 cuts** | Sourcing route |
|---|---|---|---|---|
| **L1 — real archival / factory footage** | 235 rights-cleared clips selected from the 111,821-item archive (`H:\pd-media\assets\archive\_ledger\*.jsonl`) + the 88,740-item factory shelf | **235** | **41.7%** | `search_archive.py` **only** + a labelled contact sheet before locking (CODEX_A §7.0) |
| **L2 — After Effects hero cards** | **17 cards**, six proven layouts only, each carrying a real ledger fact as *designed motion*, not a static plate | overlaid (**82.5 s** of card time — recomputed R3 from the §3 duration column; not counted as cuts) | on top | §3 below |
| **L3 — Codex AI stills** | **210** stills (**85 human-present = 40.5%**), full literal prompts, **filling only what L1 cannot legally or ethically cover** | **244** | **43.3%** | CODEX_A §5 |
| **L4 — i2v motion + overlays** | **42** Wan/RIFE motion clips (18 of them human) + 30 particle/light/vfx overlays | **84** | **14.9%** | CODEX_A §8, §9 |

**Why L3 is still 210 despite L1 arriving.** Sixteen archive queries were actually run this session (the full table with commands, hits and filenames is in **CODEX_A §7.0a**). Three findings decide the split:
1. **`search_archive.py "camp lejeune"` returns ZERO.** There is no case-specific footage in the archive. L1 can supply *the era, the place and the objects*; it cannot supply *this story*.
2. **The NARA (1,319 items) and LoC (610 items) hits skew to combat history and courthouse architecture.** The genuinely usable government item is **LoC's photographs of the U.S. Post Office and Courthouse in New Bern, North Carolina** — geographically correct, since New Bern is an EDNC seat. **The NARA Marine Corps images are NOT used: they show real, identifiable serving officers, which breaches the likeness ban.**
3. **Everything this film must never show — a sick child, a hospital bed, a funeral — must simply not exist in any layer.** L3's job is to carry grief through *objects and absence*, which is a thing no stock library holds and no archive can supply.

**⚠ The shelf's own theme folders are ~40% mislabeled — measured, and re-observed this session.** `AF-BG-0506__courtroom_interior.jpg` is actually *"tap black faucet kitchen sink"*; `AF-BG-41474__chains_and_padlock_rusty.mp4` is actually *"a rusted drum"*; `AF-BG-21082__foggy_harbor_dawn.jpg` is actually *"foggy marsh"*. **Never select by raw folder or filename.** Use `search_archive.py` or the corrected browse tree at `D:\pd-media-browse\factory_browse\<theme>\`, and **a labelled contact sheet is mandatory before locking** (`select_factory_assets.py` emits one and exits 3 if it fails). **Check `license_decision` on every row: `_quarantine/**` items are `review_required` and may not be designed in.** NARA video may be a bundled reel — record in/out seconds for every adopted clip.

### Per-act layer assignment (which layer carries which beat)

| Section | L1 (archive/factory) carries | L2 (AE cards) carries | L3 (Codex stills) carries | L4 (i2v) carries |
|---|---|---|---|---|
| **HOOK / OPENING** | the running tap, the glass filling, a dark kitchen window, a pine treeline, a marsh | `ACT_TITLE`-class opening card + `CENTER_STACK` 408,000 / 3,759 | the man turned away at the counter; the buried form in a drawer; the title beds | tap poised to run; dark window before the pines move; treeline before the gust |
| **ACT I — the quarters** | base-housing environment: clothesline, screen door, walkway, water tower, sink, bathtub, hose, rain | `ACT_TITLE_CARD I` + `CENTER_STACK` PCE 215 vs 5 / TCE 1,400 vs 5 | the family arriving; the formation cropped below the waist; the tricycle; the empty chair; the laid table | family mid-step; sheets before the gust; hands filling a glass |
| **ACT II — August 1997** | typewriter, envelope, post slot, filing drawer, photocopier, microfilm, corridors, mailbox | `ACT_TITLE_CARD II` + `QUOTE_CARD #1` (the 1981 remark, held for III) | the stillness; the first blank notepad; the binder born; the tabs; the night porch | hand lifting a handset; envelope over a slot; drawer poised to shut |
| **ACT III — what the lab wrote** | glassware, sample bottles, pipette, chart recorder, valve, pipework, pump house, drums, dry-cleaner shopfront, drain | `ACT_TITLE_CARD III` + **`QUOTE_CARD #1`** (CLW 0443, the mid reveal) + `CENTER_STACK` 1980 · 1981 · 1982 · WELLS OFF 1984–85 | **the form's seven states** (blank → written → carbon → filed → boxed); the untouched glass; the tap shut | pen poised in the margin; chart needle before the kick; tap closing |
| **ACT IV — the man born on the base** | hospital exterior (far), waiting chairs, record ledgers, **the television's light in a dim room (the film's ONLY television outside the Act V advertising beat — the record puts the broadcast with Partain, CL-25)**, corkboard, index cards, conference table, capitol, printout, hearing hall | `ACT_TITLE_CARD IV` + **`QUOTE_CARD #2`** (Partain's opening line) + `CENTER_STACK` ATSDR WITHDREW ITS OWN ASSESSMENT + `SPLIT_COMPARE` 64 MEN (2010) ↔ 125+ (2026) | the home desk at night; the wall of names; the reflection; the hearing gallery | index cards laid one by one; map pins; a report pushed back onto a shelf |
| **ACT V — the two-year window** | capitol steps, signing pen, courthouse, empty courtroom, docket, claim forms, mail trays, late-night TV, corridor benches | `ACT_TITLE_CARD V` + `CENTER_STACK` "AT LEAST AS LIKELY AS NOT" + `CENTER_STACK` NO JURY · 6 FEB 2024 + **`MONEY_STACK`** $10,000 / $24,000 / $405 | the queue; the clerk's stack; the binder on the hearing table; the deposition room; the closed binder | claim forms stacking; docket page turning; pen above a signing line |
| **ENDING** | dawn kitchen, empty glass, dripping tap, binder shelf, treeline at first light, courthouse door | `CENTER_STACK` 30 OCTOBER 2026 (falling action; the fact is planted at 0:40) | the empty chair at dawn; the walkway; still water | binder closing; one drop gathering; dawn on the quarters |

---

## 2. ANIMATION INTENT PER ACT (motion as dramaturgy)
Density stays high throughout; its CHARACTER tracks the story. The **biggest payoffs are stacked LATE** (the Act that removed every barrier → what it actually paid → the deadline), so retention runs to completion.

- **HOOK (★R3-measured **43.5 s** at 178.1 wpm / 45.4 s at 170.4 — NOT the ~33 s this document previously claimed · VOICE LEADS FROM 0:00 — HOOK-AUDIO standard):** Brian's cold-open line plays from frame 0. Visual: a tap running into a plain glass under one hard kitchen light; a hand not taking it. Ambience UNDER the voice (water, a fridge hum, cicadas beyond the screen door) — no music-only runway. One mask-lift line: **"THEY WROTE IT DOWN."** Branded opening = a ≤5.0s overlapping sting placed AFTER the BUT-loop **at ~0:44–0:49**, music ducked ≥12 dB under Brian. ★R3: the loop is *planted* at 23.3 s and its *core* lands at 31.7 s, so R-10 (loop by ~0:32) and R-11 (sting only after the loop exists) are both satisfied; what was wrong was the arithmetic, not the structure.
- **OPENING (post-brand, ~0:49–1:06, 16.8 s at 178.1 wpm):** ONE escalating sentence over the claim-count card, then the anchor "Camp Lejeune, North Carolina" and a cut to a well head. No thesis paragraph.
- **ACT I — THE QUARTERS:** warm, humid, slow — the only warmth the film has. Sheets moving, a hose arc, ice in a glass, a walkway with a tricycle on it. The chemistry is folded in over *objects in the ground*, not over a diagram. The act turns cold in two cuts at the Janey passage: motion drops to near-still for exactly one earned breath (≤2.5s) on the empty chair, then resumes.
- **ACT II — AUGUST 1997 (the machine of paper):** the densest cutting in the first half. Every ignored request is a glimpse → a drawer closing → a photocopier bar → a stack growing. The binder motif is born and starts multiplying. `mechanism gears` runs under the FOIA sequence.
- **ACT III — WHAT THE LABORATORY WROTE (the engine · mid reveal):** motion slows and tightens onto paper. Macro on a pen, on carbon, on a clipboard. The 1981 remark lands on the film's only true held beat: `QUOTE_CARD #1`, mask-lift, ~5.5s, over a near-black frame. Then the arithmetic accelerates — 1980, 1981, 1982, wells off 1984–85 — and the act ends on the tap shutting over a dry sink.
- **ACT IV — THE MAN BORN ON THE BASE (register change · the tonal reset lives here at 55–70%):** a new person, a new decade, a new lane. Partain's line opens on `QUOTE_CARD #2`. The 20–40s breather sits at ~60% on the ATSDR withdrawal — slower cutting, wider frames, record-daylight arrives for the first time. Then the science accelerates back up on `timeline` and `compbars`.
- **ACT V — THE TWO-YEAR WINDOW (the payoff cascade):** the fastest act. Statute of repose → the Act → the advertising blitz → 408,000 → the callback to the form → the jury order → no trial date → the money. The cascade terminates on **`MONEY_STACK` $10,000 · $24,000 · $405** with a hard cut to black-frame silence for 0.8s before the ENDING.
- **ENDING — the deadline lands last:** back to the kitchen. The tap. The empty glass. The binder closing. End on **"NO TRIAL. NO FINDING. ONE DEADLINE: 30 OCTOBER 2026."** in bone-white on record-daylight. BGM terminates on a downbeat, out ≤60s from the final scripted line.

---

## 3. AE HERO PROGRAM — the SIX PROVEN LAYOUTS ONLY (17 cards)
**AE uses ONLY the six implemented layouts** — no bespoke set-pieces, no phantom layouts.

### Allowed layouts (EXACTLY these six)
`ACT_TITLE_CARD` / `CENTER_STACK` / `MONEY_STACK` / `QUOTE_CARD` / `VOTE_SPLIT` / `SPLIT_COMPARE`.
> ★★ **`DATE_STAMP` and `SEAM_TRANSITION` DO NOT EXIST** in the clone source (JSX ends in `else throw "unsupported layout"`). Using them CRASHES the build. **Date cards = `CENTER_STACK`.** This is a ban, not a preference.
> ★★ **`VOTE_SPLIT` IS NOT USED in EP58** — this session verified no vote count to the ledger's standard. If the packaging pass ever verifies the PACT Act roll-call, it may replace one `CENTER_STACK`; until then the layout is unused.

### The 17-card deck (contract table lives in CODEX_B §7.2) — layout · ledger fact rendered · duration · act position

| # | Layout | Copy (exact) | Ledger | On-screen | Act position |
|---|---|---|---|---|---|
| 1 | `CENTER_STACK` | 408,000 CLAIMS · 3,759 LAWSUITS | CL-36 | 4.5 s | post-brand ~2.9% |
| 2 | `ACT_TITLE_CARD` | I · THE QUARTERS | — | 3.0 s | 3% |
| 3 | `CENTER_STACK` | TARAWA TERRACE · PCE 215 µg/L · LIMIT 5 | CL-04 | 5.0 s | ~11% |
| 4 | `CENTER_STACK` | HADNOT POINT · TCE 1,400 µg/L · 280× THE LIMIT | CL-04 | 5.0 s | ~12% |
| 5 | `ACT_TITLE_CARD` | II · AUGUST 1997 | — | 3.0 s | 18.8% |
| 6 | `CENTER_STACK` | DIAGNOSED 1983 · DIED 1985 · TOLD 1997 | **CL-14b** (the 1983 derivation, R3-added) + CL-14/15 | 5.5 s | ~20% |
| 7 | `ACT_TITLE_CARD` | III · WHAT THE LABORATORY WROTE | — | 3.0 s | 36% |
| 8 | `CENTER_STACK` | FOUR NOTES ON FOUR FORMS · 30 OCT 1980 · 29 DEC 1980 · 30 JAN 1981 · 9 MAR 1981 | CL-21a/b/**d**/c | **5.5 s** | ~37% |
| 9 | **`QUOTE_CARD` #1** | **"Water highly contaminated with other chlorinated hydrocarbons (solvents)!"** — U.S. Army laboratory analytical result form, samples 9 March 1981, Hadnot Point · CLW 0443 | CL-21c | **7.0 s** | **38.9% — MID REVEAL** |
| 10 | `CENTER_STACK` | WELLS OFF: NOV–DEC 1984 · FEB 1985 · PLANT CLOSED 1987 | CL-24 | 5.5 s | ~42% |
| 11 | `ACT_TITLE_CARD` | IV · THE MAN BORN ON THE BASE | — | 3.0 s | 51% |
| 12 | **`QUOTE_CARD` #2** | **"'You have male breast cancer' were the words which greeted me and my wife on our 18th wedding anniversary."** — Mike Partain, sworn testimony to Congress, 16 September 2010 | CL-26 | **6.5 s** | 51.4% |
| 13 | `SPLIT_COMPARE` | THE REGISTRY HE BUILT: 64 MEN (2010) ↔ 125+ (2026) | CL-26c | 5.0 s | ~56% |
| 14 | `CENTER_STACK` | 28 APRIL 2009 · ATSDR WITHDRAWS ITS OWN ASSESSMENT | CL-29 | 5.5 s | 60.9% |
| 15 | `ACT_TITLE_CARD` | V · THE TWO-YEAR WINDOW | — | 3.0 s | 69% |
| 16 | `CENTER_STACK` | THE STANDARD CONGRESS SET · "AT LEAST AS LIKELY AS NOT" | CL-34 | 5.0 s | ~75% |
| 17 | **`MONEY_STACK`** | THREE OF THE TWENTY-FIVE · $10,000 · $24,000 · $405 | CL-40 | **7.5 s** | **91.8% — PRIMARY PEAK** |

Deck total = **82.5 s** of card time (R3: 4.5+3+5+5+3+5.5+3+**5.5**+7+5.5+3+6.5+5+5.5+3+5+7.5 — card 8 went 4.5→5.5 s when R3 gave it the four-form sequence). A second `CENTER_STACK` for the ENDING ("30 OCTOBER 2026") is rendered by the **film's own OST layer, not by AE**, because it must remain re-cuttable up to the day of publication (§6 re-check).

### Rules for the WHOLE AE program
- **ACCENT tuple** `[0.310, 0.639, 0.706]` (#4FA3B4 tap-water aqua) — RGB tuple, not just a hex comment. INK `[0.035, 0.043, 0.047]`. **Record-daylight `[0.839, 0.878, 0.894]` (#D6E0E4) ONLY on cards 12, 14, 16 and 17.** Solvent ochre is an IMAGE note, never an AE colour.
- **numberticker/year rule (HARD):** YEAR figures render with **`group:false`** ("1981" not "1,981"; 1953/1980/1982/1985/1987/1997/2009/2022/2024/2026 too). Correctly-grouped large numbers (408,000 / 3,759 / $10,000 / 1,400) stay `group:true`. Enforced by `check_year_grouping.py`.
- **Concentration units are typography, not narration:** cards 3 and 4 carry "µg/L" and the limit on the same card so the ratio is legible without arithmetic.
- **Measured-fit MANDATORY** (Python `fit_size()` pre-fit + JSX `sourceRectAtTime(t,false).width` re-fit + quote-wrap; no advance-width estimation). Card 9's quote is long — it must be pre-fit and re-fit, and it is the single most likely clip point in the deck.
- **Two-step AE**: JSX builds `.aep` (`AfterFX -noui -r`) → assert `.aep` mtime > `.jsx` mtime → SEPARATE `aerender -project`. Output to a REPO path on C: (exFAT H: silently writes 0 mp4s). Working method and the AE-2026-JP traps: memory `pd-ae-hero-beat-pipeline`.
- **No card asserts a contested figure.** Card 13 is explicitly labelled a registry, not a study (CL-26c). No card says "caused". No card states a total number of people exposed (CL-08). **No card carries a real insignia, seal or emblem.**
- **Only VERIFIED verbatim in quotes** (`APPROVED_QUOTES` = ledger §VERIFIED-VERBATIM). If a candidate fails verbatim verification it is CUT, not paraphrased into a quote card.
- Final deck — id/layout/copy — must match CODEX_B exactly; `validate_lejeune_beats` cross-checks this table against the CODEX_B deck, and `check_AE_layouts` asserts every layout is one of the 6 proven (`DATE_STAMP`/`SEAM_TRANSITION` = FAIL).

---

## 4. IN-FILM FIGURE-BEAT SYSTEM (≥82 beats — the density engine)
Rendered inside the Remotion film via the real `FigureBeats.tsx` union. **Validate EVERY beat against the actual union** (timeline→events[] · bar→data[]/items[] · compbars→items[] · routemap/pindropmap→pins[] · kinetic→lines[] · mechanism→{closingdoor|gears|faultsplit} · numberticker→{value;…;group?} · stat→{value;label} · arrow→{from;to;label} · highlightring→{cx;cy;r;label} · spotlight/regionmap/lowerthird/acttitle per union). **`dochighlight` = 0 (BANNED).** **quote = 0** (verified quotes live on AE QUOTE_CARDs). **votetally = 0.** stub = 0.

- **86 beats, 2.88/min at the provisional 1,790.0 s runtime** (floor 75; ≥82 required), **variety 15 kinds**, distributed so **no 30-second window is figure-less**. Per act: **HOOK/OPENING 5 · ACT I 12 · ACT II 14 · ACT III 20 · ACT IV 17 · ACT V 15 · ENDING 3 = 86.** Heaviest in **ACT III** (the paper machine) and **ACT IV** (the science).
- **Signature figures:**
  - a `timeline` that RETURNS and extends four times — 1953 → 1957 → 1980 → 1981 → 1982 → 1984 → 1985 → 1987 → 1997 → 2009 → 2012 → 2022 → 2024 → 2026 — the film's spine and its most-reused figure;
  - `mechanism gears` = the FOIA machine in Act II (request → partial return → new reference → new request);
  - `mechanism closingdoor` = the form going into the folder, used **once**, at the mid reveal;
  - `mechanism faultsplit` = the legal hinge in Act V — *statute of repose closes in 1995* vs *§804(j)(3) removes it in 2022* — built once and paid off immediately;
  - `compbars` of **215 vs 5** and **1,400 vs 5** (the two clean concentrations, CL-04) — the only concentration figures in the film;
  - `numberticker` climbing **408,000** against a `stat` of **2,446 paid**, the film's arithmetic of disbelief;
  - `bar` of the four-year gap between the 1981 remark and the February 1985 shutdown;
  - `stat` "NO TRIAL DATE" / "$405" / "88% — INSUFFICIENT DOCUMENTATION";
  - abstract `pindropmap` of the two water systems on a stylised coastal plain (**no real base map, no readable place names, no installation boundary**);
  - `kinetic` lines for the three bellwether outcomes (ten thousand · twenty-four thousand · four hundred and five).
- Figures use the aqua system; the ONLY figures that take record-daylight are the Act V and ENDING beats.
- **⚠ Figure ban specific to this film:** no figure may plot *illness against exposure* for an individual, and no figure may present the male-breast-cancer registry as an incidence rate (CL-26c, §W).

---

## 5. COMPOSITION & TIMING (30-min) — ★VOICE-LEADS-FROM-0 model, with the measured-VO re-lock written in
- `id="Ep58Lejeune"`, 1920×1080, fps 30, ENDCARD_SEC 9.
- Script `EP58_lejeune_script.en.v001.md` = **4,738 spoken words** (gate: `check_script_length.py --lo 1740 --hi 1860` = **PASS**; owner band 4,600–4,750 ✓ — 12 words of headroom left, do not spend it).

### 5.1 PROVISIONAL model (used until the ElevenLabs master exists — do not treat as final)
```
words_total          = 4,738        (★R3 re-locked 2026-07-29; was 4,737 before the R3 fact/craft fixes)
wpm_provisional      = 178.1        -> narration 1,596.2 s
designed_gap_seconds = 184.8        (act turns, music holds under AE cards, 3 earned breaths, OST landings)
endcard              = 9.0
total_seconds        = 1,790.0      = 29:50   (band 1740-1860 ✓)
speech ratio         = 1790.0 / 1593.8 = 1.121   (measured band 1.04-1.30 ✓)
durationInFrames     = 53,700       (1790 x 30)
mean_shot            = (1790.0 - 9) / 563 = 3.163 s/cut   (<= 7.0 ✓)
```
★**R3 re-check of the whole ladder at 4,738 words** (this is the table §5.3 step 3 must reproduce):
| measured wpm | narration s | designed_gap s | ratio | verdict |
|---|---|---|---|---|
| 178.1 (channel median / provisional) | 1,596.2 | **184.8** | 1.121 | ✓ |
| 175.0 (the planning expectation, §5.2) | 1,624.5 | **156.5** | 1.104 | ✓ |
| 172.0 | 1,652.8 | **128.2** | 1.085 | ✓ |
| 170.4 (the EP55 pace, the realistic slow end) | 1,668.3 | **115.2** | 1.075 | ✓ |
| **165.2** | **1,721.0** | **60.0** | 1.040 | ⚠ gap floor exactly — below this, §5.3 step 3's escape hatch fires |

### 5.2 ★ EXPECT ~175 wpm, NOT 178.1 — and absorb the drift in the gap budget, never by re-TTS
The 178.1 wpm figure is a **channel-wide median from 31 episodes**, and Brian's real pace on this kind of prose has been slower on **both** recent long-forms: **EP55 measured 170.4 wpm (+71.2 s vs provisional)** and **EP56 measured 175.1 wpm (+71.8 s)**. Plan for **~175 wpm**, i.e. narration ≈ **1,624 s**, i.e. **+28 s** on the provisional. Do not re-write the script to hit a number, and **do not re-run TTS to speed the voice** — the voice is a canon setting (ElevenLabs "Brian", `nPczCjzI2devNBz1zQrb`, stability ≈0.35 / similarity ≈0.80), and re-generating it to chase a runtime is exactly the failure mode this section exists to prevent.

### 5.3 THE RE-LOCK PROCEDURE (run once, after the master exists — this is the binding sequence)
1. Generate the master. Measure it with ffprobe: record **speech seconds** (sum of the narration clips) and **in-master gap seconds** separately. Do not use the mp3's total duration as `narrationSeconds`.
2. Recompute the gap budget: **`designed_gap = 1790.0 − measured_speech − 9.0`**. Keep the total at **1,790.0 s** unless the gap would fall outside its own band.
3. **Gap band for this film:** `designed_gap` must land in **[1740 − 9 − measured_speech, 1860 − 9 − measured_speech]** and must not go below **~60 s** (below that, act turns and card holds start eating each other and `check_padding` will flag dead-air compression). Worked examples:
   - measured 1,624 s (175.0 wpm) → gap **156.0 s**, total 1,790.0, ratio 1.104 ✓
   - measured 1,653 s (172.0 wpm) → gap **128.0 s**, total 1,790.0, ratio 1.085 ✓
   - measured 1,668 s (170.4 wpm, the EP55 pace) → gap **113.0 s**, total 1,790.0, ratio 1.075 ✓
   - measured 1,596 s (178.1 wpm, the provisional) → gap **185.0 s**, total 1,790.0, ratio 1.121 ✓
   - ★**R3 ARITHMETIC CORRECTION.** The trigger is **1,721 s**, not 1,791 s: `designed_gap = 1790.0 − speech − 9.0`, so the ~60 s gap floor is breached the moment `speech > 1790 − 9 − 60 = 1,721.0 s` (= 165.1 wpm on 4,737 words — reachable, since EP55 came in at 170.4). At speech 1,791 s the gap would already be **−10 s**, i.e. arithmetically impossible, so 1,791 could never have been the trigger. **If measured speech exceeds 1,721 s**, the gap floor is breached — then and only then raise the total toward the 1,860 s ceiling (e.g. speech 1,800 → gap 51 → total 1,860, ratio 1.033 ⚠ below 1.04, so trim card holds rather than the script). **Never cut narration to fit; never re-TTS.**
4. Re-lock `durationInFrames = round(total_seconds × 30)` and set `narrationSeconds = measured_speech`.
5. Re-derive **only** §3.3 items [2] `mean_shot` and [8] `factory floor` in CODEX_A. **The asset counts are ratios and do not move** — still 210 / factory 235 / i2v 42 / cuts 563 / still-share 0.4334 / first-use 0.8650 / avg-uses 1.156 are all unchanged by any re-lock.
6. Re-run `check_padding`, `check_animation_mix`, `check_motion_density`. Record the measured wpm in the review log so the next episode plans against three data points, not two.
7. **A drift >45 s is not an error to hide — it is the expected case.** The narration runner should FAIL_STOP on it and hand the re-lock to the parent, exactly as it did on EP56.

### 5.4 Other locks
- **VO onset / captions / BGM / AE film_offset all anchor at `BODY_START_SEC = 0.0`** (HOOK-AUDIO). Brian's cold-open line is the narration index's FIRST chunk at `start: 0.0`. No silent runway; the branded sting overlaps ducked at **~0:44–0:49** (★R3-corrected from ~0:33–0:38) and must measure **≤5.0 s**. **The final frame numbers come from the measured VO, not from these estimates — §5.3.**
- **Narration voice = ElevenLabs "Brian" (`nPczCjzI2devNBz1zQrb`), NEVER SAPI.**
- **Real-audio constraint (HARD):** Brian + dramatized SFX/ambience ONLY. No real-person audio (no archival Ensminger or Partain, no hearing-room tape, no news anchors). No hospital audio of any kind.
- **Captions:** breath-unit splitting with a 0.60 s lead, `_smart_split` grammar-aware breaks, `medium.en`. The three long verbatim quotes (cards 9, 12 and the 88% line) are the highest-risk caption spans and must be eyeballed individually.
- **Chapters (5–7, non-spoiler curiosity nouns, published in the description):** 1. The Quarters · 2. A Glass of Water · 3. August 1997 · 4. What the Laboratory Wrote · 5. The Man Born on the Base · 6. The Two-Year Window · 7. October. **Spoiler blocklist honoured: no chapter contains a figure, an outcome, "settlement", "$405", or "nobody".**

---

## 6. GATES (nothing ships until all PASS — lessons are gates, not promises)
**Preflight (before spend):** `check_script_length --lo 1740 --hi 1860` · `check_planning_package.py 58 lejeune` · `check_prompt_diversity.py <CODEX_A>` (**including the coverage gate**) · `check_lejeune_facts.py` (B clones it; rules **R-CAUSATION** [associated with, never caused; never chemical-to-person], **R-CHILD-HARM** [no child depicted, sick or healthy; no medical imagery; no coffin or close marker], **R-LIVING** [Ensminger and Partain living, self-public, sworn words only], **R-JANEY** [one passage, her father's sworn wording as ceiling, no depiction], **R-NOBODY-CHARGED** [no individual named as wrongdoer; "publicly disciplined or prosecuted" wording], **R-LIABILITY** [no court has found the US liable], **R-NUM** [only PCE 215 and TCE 1,400 quantified; no total-exposed figure; 408,000 = claims and 3,759 = suits kept apart], **R-TVMEDIUM** [★R3-added: television/broadcast imagery only at act 4 (Partain, CL-25) and act 5 (the 2022 ad blitz, CL-46) — NEVER at act 0 or act 2, because the medium of Ensminger's 1997 discovery is not in the record (CL-15)], **R-INSIGNIA**, **R-READABLE**, **R-DOCHL**, **R-DATESTAMP**, **R-QUOTE** [ledger §VERIFIED-VERBATIM only], **R-ADadjacent** [no dollar sign, claim-hotline register or advertisement layout in packaging]) · `validate_lejeune_beats` · `check_lejeune_asset_manifest` · `check_AE_layouts` [6 implemented only] · `check_year_grouping`.
**Post-build (before final):** `check_motion_density --ep PD-2026-058-lejeune` · `check_animation_mix` · `check_caption_breaks` · `check_caption_integrity` · `check_visual_asset_qc` · `check_asset_reuse` · `check_padding` · `preflight_render_gate`.
**Post-render (before "done"):** **FULL ~30-MINUTE eyeball, 3×** (structure / caption-text / audio-sync — across the WHOLE runtime, not sampled), plus a dedicated **child-and-medical sweep** of every frame carrying a human figure. Then `check_final_acceptance 58`.
**Pre-publish re-check (ledger §RE-CHECK):** the 30 October deadline, DOJ's payout totals, the claim and suit counts, whether any Track 1 trial date exists, and both advocates' status. **The final 60 seconds are written to be re-cuttable and must be re-verified in the publication week.**

---

## 7. HANDOFF
CODEX_A (`EP58_lejeune_CODEX_A_ASSETS.v001.md`, image/asset generation) and CODEX_B (`EP58_lejeune_CODEX_B_BUILD.v001.md`, build/render — to be written) inherit from this architecture + the locked script + the FACTS_LEDGER. A↔B connect only through `episodes/PD-2026-058-lejeune/05_visuals/asset_manifest.v001.json`. This document is the intent; those are the execution. Where CODEX_A/B conflict with this doc on VISUAL INTENT or the QUALITY BAR (§0–§1a), **this doc wins**.
