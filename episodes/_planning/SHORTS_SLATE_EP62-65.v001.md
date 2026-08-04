# SHORTS_SLATE EP62–65 v001 — 12 Shorts for the four new episodes

**Created:** 2026-08-04 · **Status:** PLAN ONLY. Nothing rendered, nothing scheduled, no GPU used, no paid API called.
**Scope:** `short259`–`short270` (12 Shorts, 3 per episode) across EP62 greene / EP63 correa / EP64 memphis / EP65 marmet.
**Governing method (do NOT invent a new pipeline):** `SHORTS_METHOD.v001.md` (the 12 rules) + `SHORTS_REMOTION_SPEC.md` (Short.tsx data contract, safe areas) + `SHORTS_CONVERSION_v001.md` §4 (end CTA) + `docs/PD_SHORTS_TO_LONGFORM_FUNNEL.v001.md` (the 5-layer funnel, already implemented in code) + the build checklist in `SHORTS_SLATE_EP53-56.v001.md` §7.
**Predecessor slate:** `SHORTS_SLATE_EP57-59.v001.md` (`short73`–`short81`). Numbers up to `short181` are taken; this slate reserves 182–193.

---

## 0. State of play (measured on disk and on the live channel, 2026-08-04)

| Episode | Slug | Facts ledger | Script | episode_spec | AI stills | Footage pool staged | Footage QC |
|---|---|---|---|---|---|---|---|
| EP62 | `greene` | ✅ 83 facts / 69 verbatim | ❌ none | ✅ valid | **0** | 47 | ✅ done — **12 accepted of 47** |
| EP63 | `correa` | ✅ 177 / 105 | ❌ none | ✅ valid | **0** | 54 | ⏳ sheets built, not yet read |
| EP64 | `memphis` | ✅ 122 / 109 | ❌ none | ✅ valid | **0** | 81 | ⏳ sheets built, not yet read |
| EP65 | `marmet` | ✅ 54 / 38 (+ Brown II remand text) | ❌ none | ✅ valid | **0** | 57 | ⏳ sheets built, not yet read |

**Four consequences that shape every short below.**

1. **There is no long-form script yet, so every line traces to the FACTS LEDGER, not to a script.** This is stronger, not weaker: each ledger row carries its own grade and source, and only rows graded ✓ **VERBATIM** or ✓ may be spoken. Rows graded ○ (research instruction) and ⛔ (quarantine) may not appear in a short **at all**, and each short below names the IDs it stands on. When the long-form scripts are written, re-point `provenance` at the script lines — the sentences will not change.
2. **Every line is a re-record.** No `vc_master` exists for any of the four. 12 shorts × 5 lines ≈ 1,800 words ≈ 10,400 characters ≈ **$3.12** at the pipeline's $0.30/1k-char estimate. These shorts therefore do **not** wait for the long-form VO — only for the images.
3. **Images are the hard blocker, and the archive will not rescue them.** 0 of the required stills exist. The staged footage pools are half the size of every shipped episode's (135–259), and the one pool read end-to-end — greene — survived at **12 of 47**: the queries returned Tokyo, Kyoto, a beach, a deer, a horror clown and toilet paper. `front door`, `mailbox`, `heater`, `armchair`, `radiator` and `power lines` return **zero** hits in the whole archive. Every hero beat in this slate is an AI plate.
4. **Plate IDs below are motif requests, not file paths.** ★ Learned expensively on 2026-07-30: three of `short60`'s plates picked by prompt ID were a different picture on disk. **Never select a plate by reading the prompt list. Generate, build a labelled contact sheet, pick with your eyes**, then write file numbers into `short<NNN>.ts`.

---

## 1. Rules applied to every short in this slate

Identical to `SHORTS_SLATE_EP53-56.v001.md` §1, plus the four this slate tightens:

- **R-A. Beat floor.** ≥20 beats and ≥16 **distinct** plates per short; no plate twice in adjacent beats; the hook plate recurs only as the loop tail. There is no i2v for these four, so every hook is a depth-parallax still — the owner rejects slow cutting as 紙芝居. **No beat longer than 2.3 s.**
- **R-B. Eyes-on plate selection.** §0.4. The contact sheet is an artifact of the build, not an optional check.
- **R-C. No real-person likeness, and no face on a beat that names a real person.** All four episodes name living or once-living people. Carry those beats with hands, backs, silhouettes and objects.
- **R-D. The franchise here is not a number — it is a sentence the court actually wrote.** EP57–59 were number-driven. These four are **document-driven**: a paper on a door, a number called in a waiting room, a bill in the wrong name, a signature on an admission form. Every short below lands one **verbatim** line as its telop payoff, and that line must trace to a ✓ VERBATIM row by ID.

**Vertical-format constraints** (`SHORTS_REMOTION_SPEC.md` §4): 1080×1920 @30 fps. Telop zone y 180–560. Caption zone y 1280–1560. Nothing important at x>960 or y>1620. Citations top-left via `CitationTopLeft`, **never on the same beat as a top telop** (the short19 defect).

**Every plate in this slate is subject to the four episodes' shared `forbidden_subjects`** — no courtroom interiors, no gavels, no prison cells or bars, no readable text/numerals/signage/seals, no identifiable real building, and no stock-photo emotion (a hand on a shoulder, a tear, a clock ticking down). These are in each `episode_spec.v001.json` in machine-readable form; read them there, not from prose.

**Length.** `SHORTS_METHOD` rule 4 sets the target at **20–40 s**, going to ~60 s only when the payoff needs it. The EP53–59 slates all sat at 44–58 s without recording a reason. This slate targets **34–44 s** and treats anything above 44 s as a deviation that the short itself must justify in one line. Completion percentage beats length; a legal short that pads to fit a quote loses the swipe.

---

## 1.5 The loop and the funnel — mandatory, per short

The point of a Short on this channel is **not the Short**. Measured on 2026-08-02: shorts convert at 0.77 subscribers per 1,000 views, long-form at 3.67 — **4.8× per view** — and at that moment 46 published shorts carried **zero** links to a long-form. The entrance worked; there was no corridor. So every short in this slate carries the corridor as a build requirement, not as an afterthought.

### A. The loop contract (`SHORTS_METHOD` rule 5)

Every short in this slate is `loop: true` and must specify `loop_join`. Three parts, all verifiable before scheduling:

1. **Visual join.** The final beat's image resolves into the **first frame** of the short. Built by replaying the opening cuts in reverse across the last ~1.5 s and landing on plate `_01`. A cut that merely fades to black is not a loop.
2. **Audio join.** The last spoken word lands **at or before** the final beat, and the bed's last 0.4 s is at the same level and tone as its first 0.4 s. No music tail that has to stop.
3. **Second-watch reward** (`SHORTS_METHOD` rule 5: "reward a 2nd watch with one detail"). One element that is invisible on pass 1 and decisive on pass 2 — usually a telop that reads differently once the payoff is known. Each short below names it.

**The loop is what makes the funnel work.** The structure is deliberately unclosed: the short answers its own question and leaves a *different* question standing (`funnel_question_left_for_longform`, already written into every short below). On the second pass the viewer notices that the standing question is not answered anywhere in the 40 seconds — and the only place it can be is the description. That is the corridor.

### B. The five funnel layers (`docs/PD_SHORTS_TO_LONGFORM_FUNNEL.v001.md` — implemented in code)

One placement is not enough; the viewer can notice at any of five points, so all five are built.

| Layer | What it is | Where it is implemented | Per-short field |
|---|---|---|---|
| 1 | **Description line 1** — `▶ FULL CASE: <title>` + URL, on the FIRST line (the description collapses; line 2 is never read) | `schedule_short_youtube.py` → `ensure_funnel_description()` | `funnel_long_title` |
| 2 | **In-video card, last ~2 s** — a `▼ LINK BELOW` band over the loop tail. **Not a fake button** (nothing in a Short is tappable); scrim `0.46`, never `0.72` | `Short.tsx` → `isCta` / `ctaFadeOutSec` | `ctaLongTitle` `ctaHeadline` `ctaLongThumbSrc` |
| 3 | **Pinned comment** — the standing question, then `Full case here → <URL>` | manual/API at publish | `funnel_question_left_for_longform` |
| 4 | **Studio "Related video"** — **not settable by API**, ~30 s of manual work per short | `SHORTS_RELATED_VIDEO_WORKLIST.v001.md` | worklist row |
| 5 | **The loop itself** — §A above | `short<NNN>.ts` `buildBeats()` loop tail | `loop_join` |

**Hard dependency, and it is the one that bites:** layers 1, 3 and 4 all need the long-form's **video ID**. A short in this slate therefore cannot be scheduled until its episode has at least a private upload. Layers 2 and 5 are built into the render and do not wait.

### C. Verification before any short in this slate is scheduled

1. `loop_join` present, and the last frame visually matches frame 0 — checked by exporting frame 0 and the final frame and comparing them side by side, not by reading the code.
2. The second-watch detail is nameable in one sentence.
3. The standing question is **not** answered anywhere in the short's own 40 seconds. If it is, the corridor is closed and the short has to be re-cut.
4. Description line 1 is the funnel line, and it is line **1**.
5. The CTA band reads `▼ LINK BELOW`, is not button-shaped, and its scrim is 0.46.
6. The pinned comment text exists and matches `funnel_question_left_for_longform`.
7. The Related-video worklist row exists.

---

## 2. EP62 — the paper on the door (`greene`) — 3 shorts

Format lane **F-D** ("the notice that never arrived"). Locks from `EP62_greene_FACTS_LEDGER.v001`:
the landlord was the **Housing Authority of Louisville — a government body**, so no greedy-landlord framing anywhere (Q-08);
"she never saw the notice" is an **allegation at summary judgment, never a finding** (GL-23/24/25) and must be spoken as a claim;
the Court did **not** ban posting (GL-66) and did **not** order the mail (GL-67);
**no national number** of any kind exists in the opinion (§10);
nothing is known about what happened to Lindsey, Hodgens or Ray afterwards (GL-24, Q-05).

---

### short259 — "The children were pulling the notices off the doors. The men posting them knew."

- **Slot:** see §6 · **Format:** F-D · **Target 36–44 s** · ~120 w, 100% re-record
- **Hook (first 1 s):** *"The men whose job was to tape eviction notices to doors were asked, under oath, whether children pulled them off. One answered: we had plenty of trouble."* — frame 0 = a slip of paper on a door, corner lifting.
- **Open loop:** if the notice comes off the door, what happens to the case? **Payoff (last 3 s):** the tenants lost by default, and the Supreme Court held that posting alone was not enough.

**Ledger source (verbatim, by ID):**
> GL-41 — *"Q. Were you aware of there being any problem with children ripping the Writs off? A. Oh, we had plenty of trouble."*
> GL-40 — *"Q. Did you ever see kids pulling them off? A. Yes. … Q. Where was that? A. Village West."*
> GL-43 — the Court's reading: notices were *"not infrequently"* removed *"before they could have their intended effect."*
> GL-56 — *"merely posting notice on an apartment door does not satisfy minimum standards of due process."*

**Line plan (120 w total at ~175 wpm ≈ 41 s)** — L1 hook 22 w · L2 what posting physically is 24 w · L3 the depositions 28 w · L4 the holding 26 w · L5 CTA 20 w.
L5: *"This was 1982, and the Court decided only this case. The full story is on the channel — follow for the cases they don't teach you."*

**Plate motifs (≥16, pick off the contact sheet):** a slip of paper taped to a plain door, no readable text (hero) · a thumbtack close · adhesive tape peeling · a low-rise brick housing block in flat daylight · a walkway of identical doors · a doorframe at child height · a hand at the top of a door, out of a child's reach · a paper on the ground by a step · a stairwell landing · an empty walkway at dusk · a curtain moving in a lit window · a shadow crossing a curtain · a deposition room with two empty chairs · a court file tied with tape · a door with nothing on it · a key not turning.
**Telops:** `TAPED TO\nTHE DOOR` · `"PLENTY OF\nTROUBLE"` · `NOT INFREQUENTLY\nREMOVED` · `LOST BY DEFAULT` · `NOT ENOUGH`.
**Cover / ShortThumb:** background = the paper lifting off the door · headline `THE NOTICE\nCAME OFF` · badge `THEY KNEW`.
**CTA props:** `ctaLongTitle: 'A Paper on the Door'` (20 ch) · `ctaHeadline: 'FULL CASE'` · `ctaLongThumbSrc: shorts/short259/short182_ctathumb.png`.
**Funnel question left for the long-form:** *what does a State have to do instead — and did anyone ever tell these three women?*

> **Lock:** never say the writs *were* torn off in these three cases. The record says servers saw it happen at Village West; it does not say it happened to Lindsey, Hodgens or Ray.

---

### short260 — "One knock. Nobody home. That was the whole procedure."

- **Slot:** see §6 · **Format:** F-D · **Target 36–44 s** · ~120 w
- **Hook:** *"An officer knocked once. Nobody answered. Under Kentucky law that was the end of the attempt — the paper went on the door and the clock started."*
- **Payoff:** the Supreme Court's answer was that missing someone once proves nothing at all.

**Ledger source (verbatim):**
> GL-20 — *"But if no one is at home at the time of that visit, as is apparently true in a 'good percentage' of cases, posting follows forthwith."*
> GL-21 — *"Neither the statute, nor the practice of the process servers, makes provision for even a second attempt at personal service, perhaps at some time of day when the tenant is more likely to be at home."*
> GL-58 — *"The failure to effect personal service on the first visit hardly suggests that the tenant has abandoned his interest in the apartment."*

**Telops:** `ONE VISIT` · `NO SECOND\nATTEMPT` · `"A GOOD\nPERCENTAGE"` · `THE CLOCK STARTS` · `IT PROVES NOTHING`.
**Plate motifs:** a knuckle about to touch a door (no face) · an empty walkway seen from a door · a hallway with light under one door · a wristwatch at midday · an office worker's empty flat mid-afternoon · a bus stop in daylight · a shift-work locker · a door viewed from inside, nobody coming · a paper going up · a calendar page with days crossed, unreadable · a court docket shelf · a writ of possession in a gloved hand, illegible.
**Cover:** headline `ONE KNOCK.\nTHAT WAS ALL.` · badge `1982`.
**Funnel question:** *why was it the sheriff's name on a case about a housing authority's paper?*

---

### short261 — "The dissent's answer: mailboxes get robbed."

- **Slot:** see §6 · **Format:** F-D · **Target 36–44 s** · ~120 w
- **Hook:** *"When the Court said a letter would have been better than a paper on the door, one Justice wrote back: it is no secret that unattended mailboxes are subject to plunder by thieves."*
- **Payoff:** eleven States allowed exactly this practice at the time — and the Court struck it down on the testimony of a handful of process servers.

**Ledger source (verbatim, ALL labelled `DISSENT` on screen — R-C of `SHORTS_METHOD`):**
> GL-73 — *"Today, the Court holds that the Constitution prefers the use of the Postal Service to posted notice."*
> GL-80 — *"It is no secret, after all, that unattended mailboxes are subject to plunder by thieves."*
> GL-74 — *"The sole ground for the Court's result is the scant and conflicting testimony of a handful of process servers in Kentucky."*
> GL-75 — *"at least 11 States authorizing notice in summary eviction proceedings solely by posting."*

**Telops:** `DISSENT` · `"PLUNDER\nBY THIEVES"` · `11 STATES` · `A HANDFUL OF\nWITNESSES` · `5–4? NOT IN\nTHE OPINION`.
**Plate motifs:** a bank of dented mailboxes, no names legible · an open mailbox flap · a letter on a doormat · a post van at a kerb, unbranded · a State map with no labels · a bench of empty legislative seats · a stack of briefs · a pen held over a page, no letterforms · a door with paper, seen from far.
**Cover:** headline `"MAILBOXES\nGET ROBBED"` · badge `THE DISSENT`.
**Funnel question:** *if neither the door nor the mail is reliable, what is?*

> **Lock:** the vote count is **not in the document**. The final telop above exists to say so on screen, not to imply one. Never write "5–4" or "6–3" (§10 quarantine).

---

## 3. EP63 — the number that was never called (`correa`) — 3 shorts

Format lane **F-E** ("nobody said no"). Locks from `EP63_correa_FACTS_LEDGER.v001`:
**never say the hospital's delay killed her** — this is the single most likely factual failure in the episode; death was attributed to hypovolemic shock at a different facility, and the damages affirmed were for her suffering while waiting and the family's grief;
the hospital never refused her — it gave her a number (HA-08);
the First Circuit expressly **declined** to review the improper-transfer finding;
no member of staff is named or characterised;
Ms Gonzalez is never depicted, and neither is her death.

---

### short262 — "The hospital never said no. It just never called her number."

- **Slot:** see §6 · **Format:** F-E · **Target 36–44 s** · ~120 w
- **Hook:** *"A sixty-five-year-old woman walked into an emergency room with chest pains and was handed a number. Nobody ever refused her anything. Nobody ever called it either."*
- **Payoff:** the court's own phrase for what she received was *a high number and a cold shoulder* — and it held that the law forbids that as surely as it forbids turning someone away.

**Ledger source (verbatim):**
> CR-02 — *"Ms. Gonzalez, a sixty-five-year-old widow, awoke … 'feeling real bad,' and experiencing 'chills, cold sweat, dizziness, [and] chest pains.'"*
> HA-15 — *"the jury heard testimony from which it could have concluded that Ms. Gonzalez went to the Hospital in critical condition and received only a high number and a cold shoulder."*
> HA-08 — the hospital's position: it never denied her screening and *"would have ministered to her had she waited."*

**Telops:** `SHE WAS GIVEN\nA NUMBER` · `NOBODY SAID NO` · `"A HIGH NUMBER\nAND A COLD\nSHOULDER"` · `CONSTRUCTIVE\nDUMPING` · `SHE WAITED`.
**Plate motifs:** a paper ticket in a hand, digits not legible (hero) · rows of linked waiting-room chairs, empty · a wall-mounted number display, blank · a reception counter with nobody behind it · a corridor of closed doors · a bench with one coat left on it · a wall clock, hands only · a door swinging shut · a strip light flickering · an empty triage bay seen from the doorway · a chair in a row, slightly out of line · the same room, later, darker.
**Cover:** headline `THEY NEVER\nCALLED HER` · badge `1991`.
**CTA props:** `ctaLongTitle: 'The Number That Was Never Called'` (33 ch → shorten to `'Never Called'`) · `ctaHeadline: 'FULL CASE'`.
**Funnel question:** *what does the law actually require an emergency room to do — and what did the court refuse to decide?*

> **Lock, non-negotiable:** no line in this short may say or imply that the wait caused her death. The short ends at the wait.

---

### short263 — "'Appropriate' is one of the most wonderful weasel words in the dictionary."

- **Slot:** see §6 · **Format:** F-E · **Target 36–44 s** · ~120 w
- **Hook:** *"Congress wrote that an emergency room must give you an appropriate medical screening. A federal judge called that word one of the most wonderful weasel words in the dictionary."*
- **Payoff:** so the court wrote the test itself, and it turned out to be about sameness, not about quality: whatever the screening is, it has to be given to everyone the same way.

**Ledger source (verbatim):**
> AS-01 — *"EMTALA requires an appropriate medical screening, but does not explain what constitutes one. The adjectival phrase is not self-defining."*
> AS-02 — *"'Appropriate' is one of the most wonderful weasel words in the dictionary, and a great aid to the resolution of disputed issues in the drafting of legislation."*
> AS-04 — the test: *"reasonably calculated to identify critical medical conditions that may be afflicting symptomatic patients."*
> AS-05 — *"The essence of this requirement is that there be some screening procedure, and that it be administered even-handedly."*

**Telops:** `"APPROPRIATE"` · `A WEASEL WORD` · `NOT SELF-\nDEFINING` · `SOME PROCEDURE` · `EVEN-HANDEDLY`.
**Plate motifs:** a statute page with the type dissolved to grey (no readable text) · a dictionary open, words illegible · a pen resting on a blank form · a scale of two identical trays · two identical chairs side by side, one occupied by a coat · a queue of identical tickets · a corridor with two doors, one open · a clipboard hanging on a hook, blank · a stamp with no legend.
**Cover:** headline `"A WONDERFUL\nWEASEL WORD"` · badge `WHO DECIDES?`.
**Funnel question:** *if the rule is only "treat everyone the same", what happens when a hospital treats everyone badly?*

---

### short264 — "The money was not for her death. It was for the wait."

- **Slot:** see §6 · **Format:** F-E · **Target 44–50 s** · ~145 w — *deviation from the 20–40 s canon band, justified: five figures / two verbatim quotes that cannot be cut without changing the meaning*
- **Hook:** *"A jury awarded seven hundred thousand dollars. Almost none of it was about how she died — it was about the hours she spent sitting there, and about what her family lost."*
- **Payoff:** the hospital tried to argue the damages were wrong, but it had skipped the pretrial order, and the court called that locking the barn door long after the horse had bolted.

**Ledger source (verbatim):**
> PR-10 — the jury *"assessed $200,000 in damages on the decedent's account (payable to the heirs)."*
> PR-11 — and *"$500,000 … for the pain, suffering, and mental anguish experienced by the survivors — $100,000 apiece for the three children … and $50,000 apiece for the four grandchildren."*
> PF-08 — *"the woman described by one witness as the trunk of the family tree was cut down."*
> DM-06 — *"this motion is a classic example of a litigant locking the barn door long after the horse has bolted."*
> DM-03 — *"This was a waiver, pure and simple."*

**Telops:** `$200,000` · `$500,000` · `3 CHILDREN\n4 GRANDCHILDREN` · `"THE TRUNK OF\nTHE FAMILY TREE"` · `WAIVED`.
**Plate motifs:** a kitchen table set for many, nobody there · a stack of plates · a doorway into an empty living room · four small chairs · a coat on a hook · a family gathering shot from behind, faces away · a barn door swinging (the court's own image) · an empty church pew · a hand closing a folder.
**Cover:** headline `$700,000` · badge `NOT FOR THE DEATH`.
**Funnel question:** *what did the appeals court refuse to look at, and why does that matter?*

> **Lock:** the $200,000 is described in the opinion as *on the decedent's account*, for what she suffered **while waiting**. Do not caption it as compensation for her life.

---

## 4. EP64 — the bill in the wrong name (`memphis`) — 3 shorts

Format lane **F-D**. Locks from `EP64_memphis_FACTS_LEDGER.v001`:
the opinion **contradicts itself** on who failed to merge the accounts (majority: a contractor the Crafts hired; footnote citing respondents' brief: the utility) and on how many terminations there were (majority: five; dissent: "several") — **the script may not pick a side**;
**nobody ever decided whether the Crafts owed the money**, so "they were overcharged" is not available;
the Court expressly preserved the utility's power to cut service **after** a hearing;
no house fire, nobody freezing, no utility worker as villain.

---

### short265 — "Two bills arrived. One was addressed to a person who did not exist."

- **Slot:** see §6 · **Format:** F-D · **Target 36–44 s** · ~120 w
- **Hook:** *"A family moved into a house in Memphis and started getting two electricity bills. The second one was in the name Willie C. Craft. The man who lived there was Willie S. Craft."*
- **Payoff:** one letter. The power went off five times, and to this day no court has ever decided whether they owed the money.

**Ledger source (verbatim):**
> ML-17 — *"they noticed that there were two separate gas and electric meters and only one water meter serving the premises. The residence had been used previously as a duplex."*
> ML-19 — *"In 1973, the Crafts began receiving two bills: their regular bill, and a second bill with an account number in the name of Willie C. Craft, as opposed to Willie S. Craft."*
> ML-16 — *"Willie S. and Mary Craft, respondents here, reside at 1019 Alaska Street in Memphis."*

**Telops:** `TWO METERS` · `TWO BILLS` · `WILLIE C.` · `WILLIE S.` · `NOBODY EVER\nDECIDED`.
**Plate motifs:** two meter dials side by side on a wall (hero) · a hand tracing between them · an envelope on a mat, address dissolved · a kitchen counter with post stacked · a wall socket · a hallway light going out · a fuse panel · a house front in flat winter light · a doorbell · a phone handset on a wall cradle · a lamp with no bulb · a switch flipped with nothing happening.
**Cover:** headline `ONE LETTER\nAPART` · badge `THE POWER WENT OFF`.
**CTA props:** `ctaLongTitle: 'The Bill in the Wrong Name'` (26 ch) · `ctaHeadline: 'FULL CASE'`.
**Funnel question:** *if you cannot tell which bill is yours, who do you even argue with?*

> **Lock:** do not say the utility double-billed them, and do not say the Crafts hired a bad contractor. The opinion says both and never resolves it (§12 of the ledger). The short says *the record does not agree with itself* — that is the honest line and it is more interesting than either version.

---

### short266 — "The notice said pay or we cut you off. That was all it said."

- **Slot:** see §6 · **Format:** F-D · **Target 36–44 s** · ~120 w
- **Hook:** *"The final notice told them exactly one thing: pay by this date or the service stops. It did not mention that a human being existed who could look at the bill."*
- **Payoff:** the Supreme Court held that a cutoff notice has to tell you where, during which hours, and before whom you can argue.

**Ledger source (verbatim):**
> ML-39 — *"The 'final notice' contained in MLG&W's bills simply stated that payment was overdue and that service would be discontinued if payment was not made by a certain date."*
> ML-41 — *"[T]he MLG&W notice fails to mention 'that a dispute concerning the amount due might be resolved through discussion with representatives of the company.'"*
> ML-68 — *"recipients of a cutoff notice should be told where, during which hours of the day, and before whom disputed bills appropriately may be considered."*

**Telops:** `PAY OR\nWE STOP` · `NOTHING ELSE` · `WHERE` · `WHAT HOURS` · `BEFORE WHOM`.
**Plate motifs:** a printed slip with the type reduced to grey texture · a bill folded in three · a letter slot from inside · a counter window with the shutter down · an office corridor after hours · a wall of pigeonholes · a chair facing a closed door · a queue rope with nobody in it · a telephone ringing on an empty desk · a street of houses at dusk with one dark.
**Cover:** headline `"PAY OR\nWE CUT YOU OFF"` · badge `THAT WAS ALL`.
**Funnel question:** *the Court did not stop the shutoff. So what did it actually change?*

---

### short267 — "Two thousand customers a month. The dissent said the system worked."

- **Slot:** see §6 · **Format:** F-D · **Target 44–50 s** · ~145 w — *deviation from the 20–40 s canon band, justified: five figures / two verbatim quotes that cannot be cut without changing the meaning*
- **Hook:** *"The utility cut off about two thousand customers every month. Three Justices thought that was fine — and one of them said the Court was being condescending."*
- **Payoff:** the majority won, but it also wrote that the utility keeps the right to cut you off after the hearing. Nobody's power was saved by this case.

**Ledger source (verbatim, ALL dissent rows labelled `DISSENT` on screen):**
> ML-96 — *"Each month the Division terminates the service of about 2,000 customers."*
> ML-97 — the notices carried the legend *"PHONE 523-0711 INFORMATION CENTER"*, answered by *"30 or 40 Division employees, all of whom are empowered to delay cutoff."*
> ML-93 — *"In my judgment, the Court's holding confuses and trivializes the principle that the State may not deprive any person of life, liberty, or property without due process of law."*
> Majority, on what survives: the utility *"would retain the option to terminate service after affording the notice and hearing required."*

**Telops:** `2,000 A MONTH` · `DISSENT` · `"CONFUSES AND\nTRIVIALIZES"` · `A HEARING` · `THEN THEY CAN\nSTILL CUT IT`.
**Plate motifs:** a switchboard of unlit indicators · rows of desks with handsets · a ledger of account cards, unreadable · a meter reader's satchel · a service van at a kerb, unbranded · a street at night with one house dark · a hearing-room table with two chairs · a door marked only by a blank plate.
**Cover:** headline `2,000 A MONTH` · badge `AND IT KEPT GOING`.
**Funnel question:** *what did the Court leave undecided — and did the Crafts ever get their money?*

> **Lock, mandatory final content beat:** the telop `THEY CAN STILL CUT IT` exists so the short cannot be misread as "a hearing before shutoff means no shutoff". This is the episode's most likely misreading.

---

## 5. EP65 — the paper you sign at the door (`marmet`) — 3 shorts

Format lane **F-A** ("the machine that manufactures agreement"). Locks from `EP65_marmet_FACTS_LEDGER.v001` + the Brown II remand text:
the Supreme Court **did not hold the clauses valid** and did **not** force anybody into arbitration — it vacated and remanded (MB-34);
the decision is **per curiam** — never call it unanimous or attribute it to a Justice;
the three families are **never merged** — Marchio's agreement was materially different (MB-21);
**no statistics** of any kind — none are in the opinion;
never frame it as "your mother": the opinion never uses the word and records no relationships (only "a family member").

---

### short268 — "The one thing you could still sue about was their right to collect from you."

- **Slot:** see §6 · **Format:** F-A · **Target 36–44 s** · ~120 w
- **Hook:** *"The admission agreement said every dispute goes to arbitration. It carved out exactly one exception — claims to collect late payments owed by the patient."*
- **Payoff:** so the nursing home kept the courthouse for its own money, and gave away the courthouse for everything else, including death.

**Ledger source (verbatim):**
> MB-23 — *"The contracts included a clause requiring the parties to arbitrate all disputes, other than claims to collect late payments owed by the patient."*
> MB-07 — *"In each case, a family member of a patient requiring extensive nursing care had signed an agreement with a nursing home on behalf of the patient."*
> MB-24 — the filing fee fell on *"the party filing the arbitration."*

**Telops:** `ALL DISPUTES` · `ONE EXCEPTION` · `LATE PAYMENTS` · `THEIRS` · `EVERYTHING ELSE:\nNOT A COURT`.
**Plate motifs:** a signature line on a form, no letterforms (hero) · a pen laid across paper · a clipboard held out, hand only · a page turning · a stack of admission folders · a reception desk with a bowl of pens · a corridor with a handrail · an empty armchair by a window · a winter window from inside · a wheeled tray · a door held open from behind · two cups on a tray.
**Cover:** headline `SIGN HERE` · badge `NOT A COURT`.
**CTA props:** `ctaLongTitle: 'The Paper You Sign at the Door'` (30 ch) · `ctaHeadline: 'FULL CASE'`.
**Funnel question:** *does a relative's signature bind the person who did not sign? The Court left that open.*

> **Lock:** the asymmetry is in the document. State it flat. Do **not** add an adjective — no "cynical", no "cruel". The sentence does the work.

---

### short269 — "The Supreme Court never said the clause was valid."

- **Slot:** see §6 · **Format:** F-A · **Target 36–44 s** · ~120 w
- **Hook:** *"Everyone remembers this case as the one where the Supreme Court forced three families into arbitration. It did not. It sent the question back and refused to answer it."*
- **Payoff:** four months later the state court gave up exactly one paragraph and kept everything else.

**Ledger source (verbatim):**
> MB-34 — *"The decision of the State Supreme Court of Appeals must be vacated."*
> MB-49 — on remand the state court *"must consider whether, absent that general public policy, the arbitration clauses … are unenforceable under state common law principles."*
> Brown II (229 W. Va. 382, 13 June 2012) — *"In accordance with the Supreme Court's mandate, we overrule Syllabus Point 21 of Brown I. We otherwise find that the Supreme Court's decision does not counsel us to alter our original analysis of West Virginia's common law of contracts."*

**Telops:** `VACATED` · `NOT DECIDED` · `SENT BACK` · `ONE POINT\nOVERRULED` · `THE REST STOOD`.
**Plate motifs:** an envelope going back the way it came · a file returned to a shelf · a stairway seen from the bottom · a door closing on a corridor · a bench outside a closed room · a page with one paragraph struck through, no readable words · a state map, no labels · a courthouse step in flat light (exterior only — interiors are forbidden).
**Cover:** headline `IT NEVER SAID\nTHEY WERE VALID` · badge `VACATED`.
**Funnel question:** *what happened to Brown, Taylor and Marchio after that? The opinion does not say.*

> **Lock:** the disposition on remand is **not uniform** — two cases reversed and remanded, the third a certified question answered. If a beat needs to name the outcome, name all three or none. And never say "vacate" for what the state court did to its own point: the word is **overrule**.

---

### short270 — "A state court called the Supreme Court's reasoning 'created from whole cloth'."

- **Slot:** see §6 · **Format:** F-A · **Target 36–44 s** · ~120 w
- **Hook:** *"West Virginia's highest court read the Supreme Court's arbitration cases and wrote that they were tendentious, and created from whole cloth."*
- **Payoff:** it got reversed for it — and then, on remand, it did not back down.

**Ledger source (verbatim):**
> MB-30 — the state court *"found unpersuasive this Court's interpretation of the FAA, calling it 'tendentious' … and 'created from whole cloth'."*
> MB-36 — *"The West Virginia court's interpretation of the FAA was both incorrect and inconsistent with clear instruction in the precedents of this Court."*
> MB-35 — *"When this Court has fulfilled its duty to interpret federal law, a state court may not contradict or fail to implement the rule so established."*
> Brown II — the unconscionability doctrine is *"a general, state, common-law, contract-law principle that is not specific to arbitration."*

**Telops:** `"TENDENTIOUS"` · `"CREATED FROM\nWHOLE CLOTH"` · `REVERSED` · `PER CURIAM` · `IT DID NOT\nBACK DOWN`.
**Plate motifs:** a bolt of cloth being unrolled (the court's own metaphor) · scissors on a table · a shelf of unlabelled reporters · two law books facing each other · a lectern in an empty room · a stairwell between floors · a hand closing a book · a corridor with two doors facing.
**Cover:** headline `"CREATED FROM\nWHOLE CLOTH"` · badge `A STATE COURT SAID IT`.
**Funnel question:** *who wins when a state court and the Supreme Court disagree about contract law?*

> **Lock:** `PER CURIAM` is a mandatory telop in this short. The decision has no named author and no recorded vote, and the most common error about it is to attribute one.

---

## 6. Schedule

**Live audit run 2026-08-04** (`scripts/yt_schedule_audit.py`, read-only; the channel API is the source of truth — do **not** re-derive from local manifests):

- **Last reservation on the channel: 2026-08-15 12:00 JST.**
- **First open 12:00 JST slot: 2026-08-16 (Sun).** Open from there through 08/23 and beyond.

**Two rules the owner set on 2026-07-30, and they bind this slate.**

1. **A batch runs on CONSECUTIVE days in NUMBER order.** Do not scatter a batch across a backfilled hole.
2. **A Short is paired with its OWN episode — it publishes 1–3 days AFTER that episode's long-form, never before it, and never weeks later.**

**Rule 2 is currently unsatisfiable and that is the whole scheduling story:** none of EP62–65 has a script, let alone a render or an upload. So the absolute dates below are a **shape**, and the binding form of this schedule is relative:

| Short | Publishes | Relative to |
|---|---|---|
| `short259` `short260` `short261` | E+1, E+4, E+7 | EP62 `greene` long-form public date |
| `short262` `short263` `short264` | E+2, E+5, E+8 | EP63 `correa` |
| `short265` `short266` `short267` | E+3, E+6, E+9 | EP64 `memphis` |
| `short268` `short269` `short270` | E+1, E+4, E+7 | EP65 `marmet` |

Interleave 62 → 63 → 64 so no case runs two days straight and the plate load spreads across separate libraries (`footage_diversity` intent). EP65 follows as its own block.

**Shape, if the four long-forms were already public** (first open slot onward, one per day, 12:00 JST = 03:00 UTC):

| Date (JST) | Day | Short | Episode | Working title |
|---|---|---|---|---|
| 2026-08-16 | Sun | `short259` | EP62 | The notice came off |
| 2026-08-17 | Mon | `short262` | EP63 | They never called her |
| 2026-08-18 | Tue | `short265` | EP64 | One letter apart |
| 2026-08-19 | Wed | `short260` | EP62 | One knock, that was all |
| 2026-08-20 | Thu | `short263` | EP63 | A wonderful weasel word |
| 2026-08-21 | Fri | `short266` | EP64 | Pay or we cut you off |
| 2026-08-22 | Sat | `short261` | EP62 | Mailboxes get robbed |
| 2026-08-23 | Sun | `short264` | EP63 | $700,000, not for the death |
| 2026-08-24 | Mon | `short267` | EP64 | 2,000 a month |
| 2026-08-25 | Tue | `short268` | EP65 | Sign here |
| 2026-08-26 | Wed | `short269` | EP65 | It never said they were valid |
| 2026-08-27 | Thu | `short270` | EP65 | Created from whole cloth |

> **Re-derive the actual dates from a live audit at build time.** The last reservation moves every day the other threads book something.

> **Funnel dependency.** Schedule the short, but **do not** post the pinned comment or set the Studio Related-video until the matching long-form is public. Layer 1 (the description's first line) needs the long-form's video ID, so a short cannot be scheduled at all until its episode has at least a private upload with an ID.

---

## 6.5 Loop join and funnel, per short — this table is the build contract

`loop_join` = how the last beat returns to frame 0. **Second watch** = the one element that reads differently once the payoff is known (`SHORTS_METHOD` rule 5). **Standing question** = the pinned comment text and the reason the viewer goes to the description; it must not be answered inside the short.

### EP62 `greene` — long-form working title **“A Paper on the Door”** (`funnel_long_title`)

| | `short259` | `short260` | `short261` |
|---|---|---|---|
| **Frame 0** | a slip of paper taped to a plain door, corner lifting | a knuckle about to touch a door | a bank of dented mailboxes |
| **`loop_join`** | last beat is the same door **bare**; over the final 1.2 s the paper fades back onto it and the corner lifts — landing exactly on frame 0 | last beat is the empty walkway seen from the door; the camera settles and the knuckle re-enters frame from the left | last beat is a single letter on a doormat; a hand lifts it away and the mailbox bank is behind it |
| **Second watch** | the telop `THEY KNEW` on beat 3 reads as *the process servers knew* on pass 1, and as *the State knew* on pass 2 | `ONE VISIT` is a description on pass 1 and a verdict on pass 2 | the last telop `5–4? NOT IN THE OPINION` looks like trivia on pass 1; on pass 2 it is the short telling you it refuses to invent a number |
| **Standing question (pinned)** | *What does a State have to do instead — and did anyone ever tell these three women?* | *Why is the case named after the sheriff, when the landlord was the city's own housing authority?* | *If neither the door nor the mail is reliable, what is?* |

### EP63 `correa` — long-form working title **“Never Called”**

| | `short262` | `short263` | `short264` |
|---|---|---|---|
| **Frame 0** | a paper ticket in a hand, digits not legible | a statute page with the type dissolved to grey | a kitchen table set for many, nobody there |
| **`loop_join`** | last beat is the empty waiting room in late light; the light lifts back to daylight and the ticket re-enters the bottom of frame | last beat is a blank clipboard on a hook; it turns and becomes the dissolved page | last beat is a hand closing a folder; the folder becomes the tabletop and the chairs are back |
| **Second watch** | the empty chairs in beat 2 are the same chairs as the last beat — on pass 1 they are a room, on pass 2 they are the whole hour she sat there | `EVEN-HANDEDLY` reads as fairness on pass 1; on pass 2 it reads as *the same bad service for everybody is still legal* | `$200,000` reads as the value of a life on pass 1; the telop `NOT FOR THE DEATH` on pass 2 says it never was |
| **Standing question (pinned)** | *What does the law actually require an emergency room to do — and what did the court refuse to decide?* | *If the rule is only “treat everyone the same”, what happens when a hospital treats everyone badly?* | *What did the appeals court refuse to look at, and why does that matter?* |

### EP64 `memphis` — long-form working title **“The Bill in the Wrong Name”**

| | `short265` | `short266` | `short267` |
|---|---|---|---|
| **Frame 0** | two meter dials side by side on a wall | a printed slip, type reduced to grey texture | a switchboard of unlit indicators |
| **`loop_join`** | last beat is a switch flipped with nothing happening; the room stays dark and the two dials come up out of the dark in the same position as frame 0 | last beat is a street of houses at dusk with one dark; the dark window fills frame and becomes the slip | last beat is a street at night with one house dark; the window grid resolves into the switchboard's unlit indicators |
| **Second watch** | `NOBODY EVER DECIDED` reads as an ending on pass 1; on pass 2 it reverses the opening — the two bills were never resolved either | `BEFORE WHOM` reads as a requirement on pass 1; on pass 2 you notice there is nobody behind any counter in the whole short | `2,000 A MONTH` reads as scale on pass 1; on pass 2, after `THEY CAN STILL CUT IT`, it reads as *and it did not stop* |
| **Standing question (pinned)** | *If you cannot tell which bill is yours, who do you even argue with?* | *The Court did not stop the shutoff. So what did it actually change?* | *What did the Court leave undecided — and did the Crafts ever get their money?* |

### EP65 `marmet` — long-form working title **“The Paper You Sign at the Door”**

| | `short268` | `short269` | `short270` |
|---|---|---|---|
| **Frame 0** | a signature line on a form, no letterforms | an envelope going back the way it came | a bolt of cloth being unrolled |
| **`loop_join`** | last beat is two cups on a tray; the tray becomes the tabletop and the pen is laid back across the form | last beat is a file returned to a shelf; the shelf tilts and the envelope is on it, moving back | last beat is a hand closing a book; the closing page becomes the cloth, rolling back up |
| **Second watch** | `ONE EXCEPTION` reads as a detail on pass 1; on pass 2, knowing whose exception it is, the empty armchair in beat 8 is the person who never signed | `VACATED` reads as a win on pass 1 and as *nothing was decided* on pass 2 | `PER CURIAM` reads as jargon on pass 1; on pass 2 it is the reason nobody can be blamed for the decision |
| **Standing question (pinned)** | *Does a relative's signature bind the person who never signed it?*（最高裁が答えを残した問い） | *What happened to Brown, Taylor and Marchio after that? The opinion does not say.* | *Who wins when a state court and the Supreme Court disagree about contract law?* |

> **The four long-form working titles above are `funnel_long_title` and appear verbatim on description line 1** (`▶ FULL CASE: <title>`). They are working titles: when the long-form's real title is approved at the title/thumbnail gate, update this table and the `CONFIG` dict in `schedule_short_youtube.py` **before** scheduling, or the corridor points at a title the viewer will not recognise on arrival.

---

## 7. Build order (what unblocks what)

1. **Write the four long-form scripts** from the facts ledgers. Not a blocker for the audio (see §0.2), but it is the blocker for the funnel (§6) and it is where the `provenance` of every line above will finally point.
2. **Finish the footage QC** — `correa`, `memphis`, `marmet` sheets are built and unread (`runs/qc/<slug>_factory/`). greene is done at 12/47. Record verdicts in `runs/qc/<slug>_clip_verdicts.v001.json`, then `write_factory_clip_qc.py --slug <slug>`.
3. **Commission the AI plates.** One Codex batch per episode, sized from the QC gap — the long-form's batch and these shorts' plates come from **the same order**, so the shorts do not generate a second wave. Fill `mandatory_stills` in each `episode_spec.v001.json` the moment that brief is written.
4. **Contact sheet + eyes-on pick** (§0.4 / R-B) → write file numbers into the short.
5. **Write `short<NNN>_lines.v001.json`** under `episodes/<EPID>/09_package/` — all five lines `source: "rerecord"`, `provenance` = the ledger row text quoted above.
6. **`gen_newshort_narration.py --short NNN --ep <EPID> --text-json …`** (dry-run first for chars/$; voice `nPczCjzI2devNBz1zQrb`, `eleven_multilingual_v2`; delivery arc L1 intense → L5 calm).
7. **`build_short_mix.py --short NNN --ep <EPID>`** → `short<NNN>_timing.ts` + the −14 LUFS mix (with the speechnorm + glue-compressor chain that fixed the mid-short volume drop from short17 on). Check `SHORT<NNN>_TOTAL_SEC ≤ 58`; if over, re-run step 6 with `--gap 0.45`.
8. **Copy plates → `remotion/public/shorts/short<NNN>/`, `gen_depth_maps.py --dir …`** (every `short<NNN>_XX.png` needs `short<NNN>_XX_depth.png` or the render crashes).
9. **Write `short<NNN>.ts`** on the `short60.ts` / `short66.ts` pattern (doc-comment carrying the locks, `CUTS`, `buildBeats()`, the loop tail, the three `ctaLong*` props).
10. **Register the compositions in `Root.tsx`**, `npm run typecheck` clean.
11. **Render** via a slim public dir — `remotion/public` is ~176 GB and Remotion copies the whole `--public-dir` into its bundle. Build `remotion/public_shorts_slim` with hardlinks (`cp -rl`); symlinks silently produce an empty bundle (failure F-18b).
12. **`bash scripts/coverfirst.sh <NNN>`**, then measure — `ffprobe` for 1080×1920 / 30 fps / ≤58 s, no static hold >2 s, telops unobstructed, no `SUBSCRIBE` in frame, TikTok cut free of any external platform name.
13. **Schedule** with `scripts/schedule_short_youtube.py --short NNN --publish-at <UTC>` after adding the short's metadata to that script's `CONFIG` dict. Privacy `private` + future `publishAt`.

---

## 8. Totals

- **12 new shorts**, 3 per episode, `short259`–`short270`.
- **Audio: 100% re-record** — ≈1,800 words ≈ 10,400 characters ≈ **$3.12**. No dependency on the long-form VO.
- **Images: 0 of the required plates exist today**, across all four episodes. The archive cannot substitute: greene's staged pool survived visual QC at 12 of 47, and the core motifs of all four episodes (`front door`, `mailbox`, `heater`, `radiator`, `armchair`, `power lines`) return zero hits in a 142,000-row archive.
- **Every spoken line traces to a graded ledger row by ID.** No line in this slate rests on a summary, a memory or a search result.
- **Schedule:** relative to each episode's own long-form (§6). The absolute block 2026-08-16 → 2026-08-27 is a shape and must be re-derived at build time.
