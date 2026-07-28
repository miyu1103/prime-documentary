# EP59 — HE PAID CASH (the foreclosure forgery machine) — DESIGN ARCHITECTURE (v001)
### The creative + quality + guardrail spine for EP59 (30-min case film). This is the SOURCE OF INTENT that CODEX_A and CODEX_B both inherit. Where a later doc conflicts with this one on VISUAL INTENT or QUALITY BAR, this wins.

> episode_id `PD-2026-059-robosigning` · slug `robosigning` · EP59 · fps 30 · 1920×1080 · id `Ep59Robosigning` · target **30:00** (band 29.0–31.0 min = 1740–1860 s)
> Companions: `EP59_robosigning_script.en.v001.md` (LOCKED voice, 4,675 spoken words MEASURED), `EP59_robosigning_FACTS_LEDGER.v001.md` (the ONLY fact source), `EP59_robosigning_CODEX_A_ASSETS.v001.md` (asset generation), `EP59_robosigning_CODEX_B_BUILD.v001.md` (build/render — to be written). CTR packaging = `CTR_PLAYBOOK.v002` §4A.
> **HARD FRAME (from the ledger):** **Charlie and Maria Cardoso are living private citizens whose current status could not be established** — only their own sworn federal complaint and named newspaper reporting are used, nothing is asserted about their present lives, and **no likeness of them exists anywhere in this film**. **They never lost title**: there was no mortgage on the property, so what the bank's contractors took was **possession and their belongings**, not the deed — the words "they lost the house" and "they got the house back" are BANNED. **Warren and Maureen Nyerges** are living and self-public through wire reporting. **The banks and servicers are companies** and are held to adjudicated findings, signed settlements, consent orders and their own published statements. **Jeffrey Stephan is living and was a mid-level employee** — he is the film's *evidence*, characterised only from his own sworn testimony, and the words "architect" and "mastermind" are BANNED. **Linda Green is victim-adjacent** — a real auto-parts shipping clerk whose name other people wrote; **the exculpation is spoken in the same breath as her name, the first time it appears**. **Lorraine Brown was convicted and imprisoned — statable exactly as adjudicated.** The permitted wording for the criminal reckoning is the ledger's (RS-45) and no shorter form is allowed. **No legible signature, no readable fabricated document, no real bank logo, no government seal, and no eviction staging anywhere in the film.**

---

## 0. THE QUALITY BAR (what "past-best" means, operationally)
This film is judged against every prior episode and must beat them on all five axes at once. None is optional.

1. **Restraint that is also dense.** The *tone* is quiet and procedural — this is a paperwork crime, and the horror is that it is boring at the scale of one page and monstrous at the scale of a million. No melodrama, no eviction-porn, no horror grammar. The *motion* is relentless — something is always animating with intent. A still, silent hold of 4+ seconds is a FAILURE unless it is a deliberate, earned breath (max 3 in the whole film, each <=2.5s).
2. **Every cut earns its place.** **563 cuts** across ~30 min; mean_shot ~3.15s, max 7.0s. No filler slides. still-share <= 0.45 (design 0.433). first-use >= 0.70 (design 0.865). **avg uses/source <= ~1.4 (design 1.156)**; distinct source count spec'd LARGE (487) for a 30-min film.
3. **Premium motion density (HARD).** **>= 84 in-film FigureBeats** (>=2.5/min -> floor 75; design 84 = 2.83/min at 1,783 s), variety >= 6 kinds (design 15), plus **17 AE hero cards** composited on top. motion_density and animation_mix gates must PASS before any render is called final.
4. **Zero legibility/quality defects.** No garbled captions, no clipped AE text (measured-fit mandatory), no black frames, no desync (VO onset 0.0 — HOOK-AUDIO standard), **no dochighlight** (BANNED — it reads as a rendering bug and the owner has flagged it three times), **no unsupported AE layout** (`DATE_STAMP` / `SEAM_TRANSITION` do not exist in the JSX and crash the build — BANNED), **no `depth`-displacement footage treatment** (BANNED, §1), **no global haze/scanline/yellow wash** (screen-wash <= 0.07).
5. **Truth, with dignity.** Every on-screen number, name, date and quote traces to the FACTS_LEDGER (RS-IDs) at high confidence, or it is hedged in copy or cut. **No photoreal likeness of ANY named real person.** **No legible signature anywhere in the film** — the signature is the subject, so every signature on screen is an abstract mark. **No readable fabricated documents, no real bank logos, no government seals.** The homeowners' loss is carried by empty rooms and paperwork, never by staged distress.

If any one of these fails, the episode is not done — regardless of how good the rest looks.

---

## 1. VISUAL LANGUAGE (the elevated system)
One palette, one grammar, so the spine objects — **the signature**, **the stack**, **the paid-in-full deed** and **the lockbox on an empty house** — can accumulate meaning for 25 minutes and detonate in Acts IV–V.

- **Accent — recorder's-stamp teal `#0F6E68`** = RGB (15,110,104) = normalized **[0.059, 0.431, 0.408]**. The colour of the ink a county recorder presses into a page to make a private act into a public fact. It is the film's system colour for type accents, figures, the evidence lane and every stamp/ink surface. INK base `#0A0B0D`. Bone-white `#EDEAE2` for type. ★Deliberately separated from EP44's "teal-green hospital" (there: a pale institutional interior wash; here: a dark saturated INK teal that only ever lands on paper, stamps, pen strokes and typography — never on walls, never as room light).
- **Dread note — notice-orange `#D4692A`** = RGB (212,105,42). The flat printed orange of a notice taped to a door, an auction placard, a lockbox tag, a returned envelope. Used on **<= 8 beats total** and never floods the frame. It is the colour the eye learns to dread. ★Separated from EP43 "porch-amber" and EP55 "sodium prison gold": those are *light*; this is *print*.
- **One reserved WARM note — paid-in-full morning `#F0DFB4`** = RGB (240,223,180). Appears ONLY in (a) the Act I cash-purchase / closing-table beats and (b) the ENDING's restored-house beat. NOWHERE else. The middle of the film is fluorescent and grey by design; the only warm light the film earns is the morning a family owned a house outright, and the morning they got it back.
- **Base light — American office fluorescent + flat Florida daylight.** Drop ceilings, cubicle grey, parking-lot glare, screened porches. The film lives in flat institutional light the way EP55 lived in green-gray.
- **People (anonymized, non-identifiable — DELIBERATELY PRESENT).** **88 of the 210 body stills (41.9%, machine-counted from the finished prompt set — >=40% human-present from birth, per the owner directive continued from EP52/EP55/EP56)** and **18 of the 42 motion seeds** carry anonymized figures (backs, hands, silhouettes — adults only; children only as out-of-focus shapes). Roles: a retired couple carrying boxes into a bright empty house; hands counting cash at a closing table; a homeowner at a kitchen table under a lamp with paperwork; a call-centre floor of headsets seen from behind; a signing floor of identical desks and moving wrists; a notary's hands and a stamp; a clerk at a records counter; a court reporter's hands; a gallery of reporters' backs; a mailroom of hands stuffing envelopes; a figure standing at a locked front door with a key that no longer fits; a hand cutting a lockbox off a handle. Anti-samey rule: no two HP stills may share subject + composition + lighting (CODEX_A §5.5a variety matrix + Q4 phash watch-list). What stays banned absolutely: **likeness of any real person; any legible signature or readable document; any real logo or seal; any handcuff/eviction/distress staging; any identifiable child's face.**
- **Recurring motifs (build a vocabulary, then pay it off):**
  - **The signature (SIGNATURE A — the spine object):** an abstract wet ink stroke on a blank line. **Never letters.** One mark alone (Act I) -> a page of marks that do not match each other (Act IV) -> a wall of mismatched marks (Act IV climax) -> one mark under an exhibit sticker (Act V). The film's whole argument is visible in the fact that the *same* name is written in a dozen different hands.
  - **The stack (SIGNATURE B):** identical documents accumulating. A thin file in a hand -> an overflowing tray -> a trolley of boxes -> a pallet on a loading dock -> one box carried out of a courthouse. The stack is the film's arithmetic.
  - **The paid-in-full deed:** a single folded document with a raised seal, text an unreadable smear. Signed in warm light -> filed in a drawer -> pulled out again under a kitchen lamp -> laid flat on an exhibit table -> back in the drawer.
  - **The lockbox on an empty house:** a realtor key safe hanging on a door handle. It is the object that says *this house now belongs to a process*. Three states only: on a lived-in house, on a dark bare house, cut open on the mat.
  - **The minute:** a second hand crossing, an office wall clock at 2 a.m., a stopwatch face, a calendar page. The unit of the film is one document per working minute.
  - **The cheque:** a printed cheque in a hand, blurred; then a returned envelope with a printed mark. The remedy, rendered at its actual size.
- **Type & motion grammar:** all reveals use `overflow:hidden` + translateY mask lifts (house style); easing spring OR `Easing.out(Easing.cubic)` — NEVER linear; multi-element reveals STAGGER 2–4 frames; fast moves get `@remotion/motion-blur` Trail. Opacity NEVER alone — always paired with translateY/scale.
- **Clear image, no wash (HARD).** No global haze/fog/vignette-wash, no scanline/CRT texture, no yellow wash. Neutral minimal grade inside the teal system, screen-wash opacity <= 0.07.
- **Footage treatment — `bleed`/`parallax`/`duotone`/`focus`, NEVER `depth` (HARD).** `depth`-displacement melts subjects (EP48/49 warp defect) — BANNED; therefore **no depth maps, no `depth_path`** anywhere. Still images move by parallax and bleed, not by Ken Burns zoom (a zoom on a still is what the owner calls 紙芝居).
- **Sound design intent (for B):** the sound of this film is *paper and machinery* — a pen stroke, a stamp, a photocopier bar, a printer tray, a fax handshake, a phone hold tone, an office HVAC hum, a mail sorter, a truck door. Silence where a person should have read something. **HARD BAN: no screams, no acted distress audio, no real-person archival audio, no courtroom gavel bangs as punctuation.**

---

## 1a. ★ THE FOUR-LAYER ASSET BUDGET (owner directive 2026-07-29 — BINDING)
This film is **not** mainly AI stills. It is built from four layers, and the percentages below are contract values that CODEX_A §3.3 [9] re-derives independently.

| Layer | What | Cuts | % of 563 cuts | Who builds it |
|---|---|---|---|---|
| **1. Real archive / factory footage** | 235 rights-cleared clips selected from the 112,692-item archive (88,850-item factory shelf + `loc` 612 / `nara` 1,319 for period record-keeping and courthouses) | **235** | **41.7%** | CODEX_A §7 |
| **2. After Effects hero cards** | **17 cards**, ~105 s total, composited ON TOP of cuts (not counted as cuts) | 0 (overlay) | — (~5.9% of runtime) | CODEX_B §7.2, spec'd in §3 below |
| **3. Codex AI stills** | 210 unique prompts, 1 image each, **88 human-present (41.9%)** — fills the gaps the archive cannot cover (the signature itself, the mismatched hands, the specific house, the specific stack) | **244** | **43.3%** | CODEX_A §5 |
| **4. i2v motion + overlays** | 42 Wan 2.2 i2v clips (18 with anonymized humans) at 2 cuts each; 30 particle/light/vfx overlays composited | **84** | **14.9%** | CODEX_A §8, §9 |

**Moving-image share = Layer 1 + Layer 4 = 56.6%** (floor 45%). **Still share = 43.3%** (ceiling 45%).

**Why the archive is first, not last, in this episode.** The subject is physical: paper, pens, stamps, counters, houses, mailboxes, loading docks. All of it exists as real footage, and real footage of a hand signing a document is more persuasive than any generated image of one. The archive queries run for this episode confirmed the veins (CODEX_A §7.1/§7.3), including real clips whose provider titles are literally *"person signing on the documents"*, *"man signing the paper"* and *"woman signing the contract"*. **AI stills are reserved for what cannot be filmed without lying**: the abstract signature motif, the wall of mismatched marks, the specific empty house with its lockbox, the paid-in-full deed, and the anonymized figures the ban list requires.

**Where each layer carries the beat (per act):**

| Act | Layer 1 — archive/footage carries | Layer 2 — AE carries | Layer 3 — Codex stills carry | Layer 4 — i2v carries |
|---|---|---|---|---|
| **HOOK + OPENING** | the street, the door, the mailbox, the drive at night | nothing until the sting (no card may precede the BUT-loop) | the lockbox on the door, the one wet ink mark, the bare living room | the door and the ink mark, moving |
| **ACT I — the house they owned** | the closing table, cash counting, moving boxes, the records counter, the suburb | **AE-04 the price paid, in one number** | the paid-in-full deed, the warm empty rooms, the drawer | the couple's backs walking in; the deed folding shut |
| **ACT II — nobody was reading** | call floor, phone bank, fax, photocopier, mail trays, night office | **AE-06 the escalation ladder that goes nowhere** | the letter that answers nothing, the overflowing tray, the kitchen table at 1 a.m. | hands on a headset; the tray filling |
| **ACT III — what a sworn statement is** | courthouse exterior/corridor/gallery, clerk counter, stenotype, deposition room | **AE-08 what "personal knowledge" means, built from the words of the oath itself; AE-09 THE COUNTER (hardest card #1)** | the empty witness chair, the blank notary journal, the oath silhouette | a hand rising to take an oath; the transcript riffling |
| **ACT IV — the signature factory** | industrial park, loading dock, rows of desks, pallets of paper, sorting machines, press lecterns | **AE-11 ONE NAME, TWELVE HANDS (hardest card #2); AE-12 the chain of title that breaks (hardest card #3)** | the page of mismatched marks, the wall of marks, the signing floor | wrists writing in repetition; the stack growing |
| **ACT V — the price of a million homes** | cheque printing, envelope stuffing, mailbags, federal building, boarded houses | **AE-14 $25 BILLION -> ONE HOUSEHOLD (hardest card #4); AE-15 the sentence** | the cheque in a hand, the returned envelope, the boarded window | the envelope machine; a figure at a locked door |
| **ENDING** | dawn suburb, kitchen light, mower, mailbox | **AE-17 the present-tense card, date-stamped** | the lockbox cut open on the mat, the deed back in the drawer | the front door opening inward |

---

## 2. ANIMATION INTENT PER ACT (motion as dramaturgy)
Density stays high throughout; its CHARACTER tracks the story. The film's motion argument is **repetition** — the same gesture, faster and faster, until the viewer feels the minute.

- **HOOK (0:00–~0:32 · VOICE LEADS FROM 0:00 — HOOK-AUDIO standard):** Brian's cold-open line plays from frame 0 over the film's literal thumbnail shot — a realtor lockbox on a front door at night. Tense ambience UNDER the voice (a porch bulb's hum, a distant road, a key touching metal) — no screams, no music-only runway. One mask-lift line lands before the sting. Branded opening element = a **≤5 s** overlapping sting at ~0:32, music ducked ≥12 dB under Brian, **placed only after the BUT-loop exists**.
- **OPENING (post-brand, ~0:37–0:47):** ONE escalating sentence, then a date/place anchor into Act I. No thesis paragraph. The whole post-brand block is a single new concrete plus a date.
- **ACT I — THE HOUSE THEY OWNED:** the warmest act, and the only place the paid-in-full morning colour is allowed. Motion is slow, physical and domestic — cash counted onto a table, a stamp pressed, a deed folded into a drawer, a sprinkler arc. The **deed motif is born** and the **stack motif is born small** (one thin file in one hand). The EP33 contradiction is named here in a single sentence — *when a bank forecloses properly, this is what happens* — so a returning viewer never finds the inconsistency before the film does. First `mechanism gears` beat is planted late in the act, unpaid.
- **ACT II — NOBODY WAS READING (the response, and REVERSAL 1):** motion becomes procedural and slightly too fast — hold tones, a copier bar, a printer tray, a cart in a corridor, a sorting machine. The reversal is that **telling the truth to the machine changes nothing, because nobody is reading.** The document counter is planted here as the macro loop and left open. Register shifts from domestic to institutional; the palette loses its warm note entirely and does not get it back until the ENDING.
- **ACT III — WHAT A SWORN STATEMENT IS (the evidence, and the MID REVEAL at ~50%):** the act opens by *folding in* what an affidavit is — one sentence at a time, always attached to a person doing something (a hand rising, a file being opened, a stamp pressed) — and **never as a block**. Motion slows and lengthens here; the only near-4 s holds in the film live in this act, around the deposition. The **MID REVEAL lands at ~50%**: the deposition itself — the volume, in the signer's own sworn words, and the admission that the documents were not executed on personal knowledge. **AE-09, the signature-per-minute counter, runs in real time under this beat** and is the single most important motion-graphic in the film.
- **ACT IV — THE SIGNATURE FACTORY (the deep dive — the densest act):** the tempo becomes mechanical. Cut length shortens; the wrist, the pen, the page, the stamp, the stack, the pallet, the truck. This is where the film escalates from n=1 to n=many, and where **AE-11 (one name, twelve hands)** and **AE-12 (the chain of title that breaks)** carry the explanatory load that narration must not. The name-lending employee's exculpation is spoken **in the same breath as the first appearance of her name**, non-negotiably. The act ends with the machine stopping — the halt, the fifty attorneys general — and then the reversal-of-the-reversal seventeen days later when it starts again.
- **ACT V — THE PRICE OF A MILLION HOMES (the resolution ladder, PRIMARY REVEAL 65–85%):** the motion inverts — instead of paper being produced, paper is being *sent*: cheque printers, envelope inserters, mail hampers, a roadside mailbox. The ladder is arithmetic: the headline number, the share of it that was cash, the per-household figure, the $300 tier, the cheques that could not be cashed, the review that was stopped before it could count. Then the punished-villain beat, stated exactly as adjudicated. Then, briefly and plainly, the restored victim. **Cold-open callback at 70–90%: the same front door, the same lockbox.**
- **ENDING (≤60 s falling action, nothing new after 92%):** present tense and date-stamped. The lockbox is cut off; the deed goes back in the drawer; the paid-in-full morning colour returns for the only other time in the film. Then the last turn: the same paper is moving again — dormant second liens bought by debt buyers and foreclosed a decade later — and the record of what has happened to the agency built to stop it, stated as record and attributed, never asserted. BGM terminates on a downbeat. Last frame: one blank sheet on a bare floor.

---

## 3. AE HERO PROGRAM — the SIX PROVEN LAYOUTS ONLY (17 cards, ~105 s)
**AE uses ONLY the six implemented layouts** — no bespoke set-pieces, no phantom layouts.

### Allowed layouts (EXACTLY these six)
`ACT_TITLE_CARD` / `CENTER_STACK` / `MONEY_STACK` / `QUOTE_CARD` / `VOTE_SPLIT` / `SPLIT_COMPARE`.
> ★★ **`DATE_STAMP` and `SEAM_TRANSITION` DO NOT EXIST** in the clone source (the JSX ends in `else throw "unsupported layout"`). Using them CRASHES the build. **Date cards = `CENTER_STACK`.**
> ★★ **`VOTE_SPLIT` IS NOT USED in EP59** — the ledger contains no verified vote count, and a vote-shaped card would be a decoration. It is listed as allowed and deliberately spent zero times.

### ★ Why AE is load-bearing in THIS episode
Finance explainers are the channel's measured floor (**3.97% AVP**). The defence is not narration and not more nouns — it is **motion graphics that make an abstraction physical**. Four cards carry the episode's entire explanatory load and get the most design attention; if they land, the film works, and if they are mushy, no amount of script polish will save it.

**THE FOUR HARDEST CARDS (design priority order):**
1. **AE-09 · THE COUNTER (`CENTER_STACK`, Act III, ~12 s).** A signature counter that **runs in real time on screen** while the narration states the deposition volume. The viewer watches marks accumulate at the actual rate and understands, without being told, that no human being could have read any of them. This is the film's thesis rendered as a clock. Numberticker `group:true` for the running count; the elapsed-seconds readout beside it is the emotional payload.
2. **AE-11 · ONE NAME, TWELVE HANDS (`SPLIT_COMPARE`, Act IV, ~9 s).** Twelve abstract ink strokes, staggered in 3-frame intervals, all claiming to be one signature and all visibly different. **No letterforms — the strokes are pure marks, per the ledger's binding ban.** The card does in nine seconds what a paragraph cannot do at all.
3. **AE-12 · THE CHAIN THAT BREAKS (`SPLIT_COMPARE`, Act IV, ~8 s).** Lender → servicer → trust, drawn as three linked plates with `arrow` transitions; one link is then shown to be a document that was created after the fact. This is the only securitisation content in the film and it exists **as a diagram, not as narration** — which is precisely how R-2's explanation-block trap is avoided.
4. **AE-14 · $25 BILLION → ONE HOUSEHOLD (`MONEY_STACK`, Act V, ~11 s).** The headline settlement figure resolves down through its own components to the per-household payment. The whole card is one continuous scale move; the viewer's eye never leaves the number while it shrinks by four orders of magnitude.

### The 17-card deck (contract table — CODEX_B §7.2 must match this exactly)

| # | id | layout | renders (ledger row) | dur | act / position |
|---|---|---|---|---|---|
| 1 | AE-01 | `ACT_TITLE_CARD` | ACT I title | 4 s | Act I open |
| 2 | AE-02 | `CENTER_STACK` | the date and place anchor for the purchase (RS-01/RS-02) | 5 s | Act I early |
| 3 | AE-03 | `CENTER_STACK` | what a paid-in-full deed means — owned outright, no lender (RS-03) | 6 s | Act I mid |
| 4 | AE-04 | `MONEY_STACK` | the price paid, in cash, in one number (RS-02) | 7 s | Act I mid |
| 5 | AE-05 | `ACT_TITLE_CARD` | ACT II title | 4 s | Act II open |
| 6 | AE-06 | `CENTER_STACK` | the escalation ladder that went nowhere — who was told, and when (RS-07/RS-08) | 7 s | Act II late |
| 7 | AE-07 | `ACT_TITLE_CARD` | ACT III title | 4 s | Act III open |
| 8 | AE-08 | `QUOTE_CARD` | **the sworn words themselves** — the "personal knowledge" formula, verbatim from the ledger | 8 s | Act III mid |
| 9 | **AE-09** | `CENTER_STACK` | **THE COUNTER — the deposition volume, running in real time (RS-20/RS-21)** | 12 s | Act III, at the MID REVEAL (~50%) |
| 10 | AE-10 | `ACT_TITLE_CARD` | ACT IV title | 4 s | Act IV open |
| 11 | **AE-11** | `SPLIT_COMPARE` | **ONE NAME, TWELVE HANDS (RS-34/RS-35)** | 9 s | Act IV, first appearance of the signature grid |
| 12 | **AE-12** | `SPLIT_COMPARE` | **the chain of title, and the link created after the fact (RS-30/RS-64)** | 8 s | Act IV mid |
| 13 | AE-13 | `CENTER_STACK` | the halt: 23 judicial states, then all 50, then 50 attorneys general — three dates (RS-50/52/54) | 7 s | Act IV late |
| 14 | AE-14 | `ACT_TITLE_CARD` | ACT V title | 4 s | Act V open |
| 15 | **AE-15** | `MONEY_STACK` | **$25 BILLION → $1.5 BILLION IN CASH → $1,480 PER HOUSEHOLD (RS-60/61/62)** | 11 s | Act V, the primary-reveal ladder |
| 16 | AE-16 | `SPLIT_COMPARE` | **2.36 MILLION OF 3.9 MILLION GOT $300 ↔ 1,082 GOT $125,000 (RS-66)** | 8 s | Act V, immediately after AE-15 |
| 17 | AE-17 | `CENTER_STACK` | the present-tense close, `status_as_of` stamped in copy (RS-80/RS-84/RS-86) | 7 s | ENDING |

**Total ≈ 105 s.** (Note the numbering: AE-14 is the Act V title card and **AE-15 is the money ladder** — the "$25bn → one household" card referenced as hardest-card #4 above.)

### Rules for the WHOLE AE program
- **ACCENT tuple** `[0.059, 0.431, 0.408]` (#0F6E68 recorder's-stamp teal) — RGB tuple, not just a hex comment. INK `[0.039, 0.043, 0.051]`. **Paid-in-full morning `[0.941, 0.875, 0.706]` (#F0DFB4) ONLY on AE-02/03/04 and AE-17's final beat.** Notice-orange is an IMAGE note, never an AE colour.
- **numberticker/year rule (HARD):** YEAR figures render with **`group:false`** ("2010" not "2,010"; 2005/2009/2011/2012/2013/2026 too). Correctly-grouped large numbers ($25,000,000,000 / 2,358,441 / 3,949,896 / $1,480 / $300) stay `group:true`. Enforced by `check_year_grouping.py`.
- **Measured-fit MANDATORY** (Python `fit_size()` pre-fit + JSX `sourceRectAtTime(t,false).width` re-fit + quote-wrap; no advance-width estimation).
- **Two-step AE**: JSX builds `.aep` (`AfterFX -noui -r`) → assert `.aep` mtime > `.jsx` mtime → SEPARATE `aerender -project`. Output to a REPO path on C: (exFAT H: silently writes 0 mp4s). Known trap: a crash-recovery dialog blocks every launch — delete `PriorSafeMode.txt` and always `app.quit()`; set `gpuAccelType = SOFTWARE` if the GPU path is unstable.
- **No card asserts a contested figure.** Every number on every card traces to an RS row at A or A− grade. Specifically: **no card shows a count of bounced cheques (none exists — RS-69), no card shows a national count of fabricated documents (none exists — RS-76), and no card shows the 88% RIF percentage** unless it is re-verified against the GAO slides first (RS-86 iii).
- **NO AE MOMENT RENDERS A LEGIBLE SIGNATURE.** AE-11's twelve marks are abstract strokes. This is the film's single most important visual ban and it is enforced in the card spec, not left to the animator.
- **Only VERIFIED verbatim in quotes** (`APPROVED_QUOTES` — final text fixed by the FACTS_LEDGER's verbatim section). If a candidate fails verbatim verification it is CUT, not paraphrased into a quote card.
- Final deck — id/layout/copy — must match CODEX_B exactly; `validate_robosigning_beats` cross-checks this table against the CODEX_B deck, and `check_AE_layouts` asserts every layout is one of the 6 proven (`DATE_STAMP`/`SEAM_TRANSITION` = FAIL).

---

## 4. IN-FILM FIGURE-BEAT SYSTEM (>=84 beats — the density engine)
Rendered inside the Remotion film via the real `FigureBeats.tsx` union. **Validate EVERY beat against the actual union** (timeline->events[] · bar->data[]/items[] · compbars->items[] · routemap/pindropmap->pins[] · kinetic->lines[] · mechanism->{closingdoor|gears|faultsplit} · numberticker->{value;…;group?} · stat->{value;label} · arrow->{from;to;label} · highlightring->{cx;cy;r;label} · spotlight/regionmap/lowerthird/acttitle per union). **dochighlight = 0 (BANNED).** **quote = 0** (verified quotes live on AE QUOTE_CARDs). stub = 0.

- **84 beats, 2.83/min at the provisional 1,783.0 s runtime (floor 75 / >=2.5 per min), variety 15 kinds**, distributed so **no 30 s window is figure-less**. Heaviest in **ACT IV** (the factory arithmetic, 20) and **ACT V** (the remedy arithmetic, 19).
- **Per-act allocation:** HOOK+OPENING 4 · ACT I 11 · ACT II 12 · ACT III 14 · ACT IV 20 · ACT V 19 · ENDING 4 = **84**.
- **Signature figures:**
  - a `timeline` that RETURNS and extends (2005 -> 2009 -> Sept 2010 -> Oct 2010 -> Apr 2011 -> Feb 2012 -> Jan 2013 -> Jun 2013 -> today);
  - the **document counter** as `numberticker` beats climbing across acts (the film's macro loop — planted in Act II, paid at the Act III deposition, exploded in Act IV);
  - `mechanism gears` = what a foreclosure affidavit is *supposed* to do (a person reads a file, swears to it, a court relies on it) — built ONCE in Act III;
  - `mechanism faultsplit` = the same machine with the reading step removed — the film's hinge, paid off in Act IV;
  - `mechanism closingdoor` = the notice going onto a door;
  - `compbars` of "documents signed" vs "documents read";
  - `bar` of remedy per household against the value of a house;
  - `stat` beats: "one per working minute", "23 states", "50 attorneys general", "one prison sentence";
  - abstract `pindropmap` of recorders' offices across the country (stylized, no real county names on screen);
  - `kinetic` lines for the one-name-many-hands beat (the words of the oath, broken apart);
  - `arrow` beats for the chain of title moving from lender to servicer to trust.
- Figures use the teal system; the ONLY figures that take paid-in-full morning are the Act I closing beat and the ENDING.
- **Rule: no figure may display a legible signature or a fabricated document.** Figures render *numbers and relationships*, never fake paperwork.

---

## 5. COMPOSITION & TIMING (30-min) — ★VOICE-LEADS-FROM-0 model (HOOK-AUDIO standard) + opening formula v2
- `id="Ep59Robosigning"`, 1920x1080, fps 30, ENDCARD_SEC 9.
- Script `EP59_robosigning_script.en.v001.md` = **4,675 spoken words MEASURED (gate-equivalent count)** (owner band 4,600–4,750; gate `check_script_length.py --lo 1740 --hi 1860` = PASS; the pasted output lives in the review log).
- **Provisional timing:** 4,675 / 178.1 wpm = **1,575.0 s** speech + designed gap budget **199.0 s** + endcard **9 s** = **1,783.0 s = 29:43**, inside the 1740–1860 band; speech ratio **1.132** ∈ measured 1.04–1.30. Per-act measured words: HOOK 159 / OPENING 60 / ACT I 491 / ACT II 547 / ACT III 822 / ACT IV 930 / ACT V 1,200 / ENDING 466. `durationInFrames` provisional = 1783 x 30 = **53,490**.
- **★★ MEASURED-VO RE-LOCK PROCEDURE (mandatory — EP55 and EP56 both drifted +71 s, so expect it).** Brian's real pace on dense factual text is **170–176 wpm**, not the gate model's 178.1. After the ElevenLabs master is generated:
  1. `ffprobe` the master; record **speech seconds** (sum of chunks) and **in-master gaps** separately.
  2. If `|measured − provisional| > 45 s`, do NOT re-TTS and do NOT edit the script. **Absorb the drift in the gap budget.**
  3. Recompute `total = narration_measured + gap_rescaled + 9`, choosing `gap_rescaled` so that **total ∈ [1740, 1860]** AND **speech ratio = total / narration_measured ∈ [1.04, 1.30]**.
  4. Re-lock `durationInFrames = total x 30`; set `narrationSeconds = narration_measured`.
  5. Record BOTH the provisional and the re-locked numbers in the review log, and re-derive only CODEX_A §3.3 [2] and [8] (mean_shot and the factory floor). **Asset counts do not change.**
  6. **Worked band for this script:** if the master measures 1,660 s (≈170 wpm), the admissible gap budget is **71.0–191.0 s**; take **~114 s** for a 1,783 s total, or up to 191 s if the act-turn breaths need it.
- **Opening formula v2 timing (FINDINGS R-7..R-13 — build-binding):** VO from frame 0 (sound <=1.5 s, case-specific first frame); protagonist named <=0:15; opposing force planted <=0:28; **BUT-loop by ~0:32, BEFORE the sting**; **brand sting <=5 s (0:32–0:37), audio-continuous, fused with the title line** — the 10 s-class BrandOpening cut is BANNED here; post-brand = ONE escalating sentence + date/place anchor (0:37–0:47); first-45 s bans (no channel self-description, no two sentences without a new concrete). **Verify at build: sting length <=5.0 s measured on the render.**
- **VO onset / captions / BGM / AE film_offset all anchor at `BODY_START_SEC = 0.0`** (HOOK-AUDIO). Brian's cold-open line is the narration_index's FIRST chunk at `start: 0.0`. No silent runway.
- **Narration voice = ElevenLabs "Brian" (voice_id `nPczCjzI2devNBz1zQrb`), NEVER SAPI.** Canonical settings (stability~0.35 / similarity~0.80 / style 0 / speaker_boost on).
- **Real-audio constraint (HARD):** Brian + dramatized SFX/ambience ONLY. No real-person audio — no deposition audio, no 60 Minutes clips, no news anchors, no congressional-hearing audio.
- **Captions:** one cue per breath group, forced-aligned to the rendered audio, lead 0.60 s, grammatical splits (`_smart_split`), `medium.en`. Pronunciation watch-list for CODEX_B: *affidavit* (AF-ih-DAY-vit), *notarized*, *Alpharetta* (al-fuh-RET-uh), *Duval*, *escrow*, *assignment of mortgage*.
- **BGM:** ends on a downbeat, cleanly, without changing runtime (standing owner directive). Audible floor maintained under narration.
- **Chapters (>=25 min -> 5–7 curiosity-noun chapters, spoiler blocklist enforced — no *fraud/guilty/settlement/prison/won* in titles):**
  1. **The House That Was Paid For** · 2. **The Letter That Answered Nothing** · 3. **What "Personal Knowledge" Means** · 4. **One Name, Twelve Hands** · 5. **A Minute Per Document** · 6. **The Cheque in the Mail** · 7. **Still on the Counter**
  (Published in the description; one per major turn; names tease, never resolve.)

---

## 6. GATES (nothing ships until all PASS — lessons are gates, not promises)
**Preflight (before spend):** `check_script_length --lo 1740 --hi 1860`; `check_planning_package.py 59 robosigning`; `check_prompt_diversity.py` (incl. the coverage gate); `check_robosigning_facts.py` (clone of `check_burge_facts.py`; rules: **R-SIGN-ILLEGIBLE** [no legible signature anywhere, in any asset or card], **R-READABLE** [no readable fabricated document], **R-NO-LOGO** [no bank logo, corporate name, state or federal seal], **R-GREEN-VICTIM** [the name-lending employee is never called a forger/fraudster; the on-screen framing must say her name was used by other hands], **R-STEPHAN-EMPLOYEE** [the signer is characterised only from his own sworn words; never "mastermind"], **R-BROWN-SCOPE** [the convicted executive's conviction and sentence are statable exactly as adjudicated, and no further], **R-PRISON-WORDING** [the permitted formulation is the FACTS_LEDGER's; never "the only person charged" or "the only person convicted"], **R-LIVING** [no likeness of any living private homeowner; only what they have publicised], **R-NO-EVICTION-VIOLENCE**, **R-NUM** [ledger hedges preserved], **R-DOCHL** [dochighlight = 0], **R-QUOTE** [only ledger-verified verbatim with attribution], **R-DATE**); `validate_robosigning_beats`; `check_robosigning_asset_manifest`; `check_AE_layouts` [the 6 implemented layouts only — `DATE_STAMP`/`SEAM_TRANSITION` = FAIL]; `check_year_grouping`.
**Post-build (before final):** `check_motion_density --ep PD-2026-059-robosigning`, `check_animation_mix`, `check_caption_breaks`, `check_caption_integrity`, `check_visual_asset_qc`, `check_asset_reuse` (incl. `footage_diversity`: distinct >= 0.40, reuse <= 4, generic symbols <= 2), `check_padding`, `preflight_render_gate`.
**Post-render (before "done"):** **FULL ~30-MINUTE eyeball, 3x** (structure / caption-text / audio-sync — across the WHOLE runtime, not sampled), plus a **dedicated signature-legibility pass** (scrub every frame containing a signature motif and confirm no letterform is readable). Then `check_final_acceptance 59 --render <mp4> --emit-receipt`, and confirm the receipt's `video_sha256` matches the file before anything is scheduled.

---

## 7. HANDOFF
CODEX_A (`EP59_robosigning_CODEX_A_ASSETS.v001.md`, image/asset generation) and CODEX_B (`EP59_robosigning_CODEX_B_BUILD.v001.md`, build/render — to be written) inherit from this architecture + the locked script + the FACTS_LEDGER. A and B connect only through `episodes/PD-2026-059-robosigning/05_visuals/asset_manifest.v001.json`. This document is the intent; those are the execution. Where CODEX_A/B conflict with this doc on VISUAL INTENT or the QUALITY BAR (§0–§1a), **this doc wins**.
