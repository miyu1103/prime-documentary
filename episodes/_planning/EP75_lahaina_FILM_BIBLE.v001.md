# EP75 · LAHAINA — FILM BIBLE v001

**Binding design document.** Written against `EP75_lahaina_FACTS_LEDGER.v001.md` **and `.v002.md`**,
`episodes/PD-2026-075-lahaina/episode_spec.v001.json`, and `docs/PD_ONE_PASS_PRODUCTION_SPEC.v3.md`.
Where this file and the ledger disagree, **the ledger wins**. Where this file and the spec disagree,
**the spec wins** — it is the machine contract.

Runtime **29:00–32:00**. Narration **4,900–5,400 words**, and that band is a frame, not an
instruction: §15 says how the script is actually sized. Five acts. Mean cut **3.8 s**.
**265 distinct video assets. 24 people plates. 13–17 figure beats per act. 4 audio layers.**

---

## 0. Read this first: the five ways this film goes wrong

**One. It becomes conspiracy-adjacent.** This topic shares its search terms with an active
directed-energy-weapon audience, and the thing that feeds them is not a false claim — it is a
**rhetorical shape**: raise a question, leave it open, let the viewer supply a villain. This film never
does that. The cause is on the record, dated and attributed, and it is stated in a flat declarative
sentence in ACT_2. The words *some say*, *many believe*, *questions remain*, *we may never know* and
*the official story* appear **zero times**. ⛔-04 governs every act, and it is the reason §5's register
is what it is.

**Two. It completes the sentence the record refuses to complete.** The seductive line is "if the
sirens had sounded, people would have lived." **Nowhere in the 84 findings is that finding** (AB-01).
The film's permitted shape is: the system existed, it was built for this among other things, one siren
inside the burn perimeter was operable, it had never once been used for a wildfire, and it was not
used. **Then stop.** ⛔-01, ⛔-02 and ⛔-03 are three separate rules because there are three separate
ways to break this, and the third is the sneakiest: the word *failed*. No source says the sirens
failed. Two different sources say two different things, and the film says each one separately, with
its own attribution.

**Three. It prosecutes the firefighters.** Crews reported the morning fire extinguished and returned
to quarters at 14:17; it was reported again at 14:55 at the same place (LH-220, LH-221, LH-222). That
38-minute gap is the hinge of the film and it is **never spoken as an accusation** (⛔-16). It travels
in the same passage as the County's own statement that its firefighters "went above and beyond their
due diligence" (LH-15) and as Finding 67, which says the mopup they performed was the mopup proven
successful under typical conditions and appears to have been insufficient under the conditions of that
day (LH-85). Three sentences, in that order, every time.

**Four. It is beautiful.** Maui footage on every shelf is holiday footage, and every query in this
episode will return turquoise water. The spec carries 65 `forbidden_subjects` and
`footage_review_required` is `true`. The register of this film is **grey smoke, ash, corrugated steel,
melted aluminium, chain-link fence, a standing stone wall**. The word *paradise* does not appear. The
film never opens on the sea. ⛔-12.

**Five. It has no ending, so it reaches for one.** There is no verdict, no sentencing, no vindication.
The settlement has not paid anybody as of the day this was written (LH-115). The ending is built out
of an absence and an argument, and §14 is where it is built.

---

## 1. CONTROLLING IDEA

> **A warning system is not the equipment you own. It is the thing you are in the habit of using —
> and this one's habit was the sea.**

Hawaiʻi built the largest integrated outdoor warning siren network in the world. It tested it on the
first business day of every month, in daylight, on schedule, in public. Its own published list of what
the network is for includes wildfires. And on 8 August 2023 one siren inside the burn perimeter was
operable, the network had never once been used to warn of a wildfire, and the warning that was sent
went out as a text message to a region whose cellular communication had been destroyed that morning.

**The one-sentence contradiction** (ledger v002, closing line; every act serves it):

> Hawaiʻi built the largest outdoor warning siren network in the world and tested it on the first
> business day of every month — and on the day a town burned from the mountain side down, one siren
> inside the burn perimeter was operable, the network had never once been used to warn of a wildfire,
> and the first evacuation order in the county's alert log naming a Lahaina neighbourhood is
> timestamped 16:16, sent to cellphones in a region whose cellular service had died that morning.

---

## 2. Four problems this film has, and how each becomes structure

| problem | why it is a problem | what it becomes |
|---|---|---|
| Everyone already knows the ending | Lahaina burned. No suspense of outcome exists | **Suspense of arrival.** The viewer is made to want to know *when the town was told, and how*. The clock is the spine and the answer lands at 16:16 in ACT_3 |
| The record refuses to blame anyone | The film cannot deliver the punishment the form promises | The refusal becomes the subject. ACT_5 is built as **"what the investigation found, and what it would not write"** — 84 findings, 140 recommendations, and no finding that the siren would have changed anything. That is stated out loud as the film's thesis, not apologised for |
| The cause is a system, not an event | Thirteen findings is a list, and a list is not a film | The 84 are never listed. **Five are dramatised as objects** (§3). The number 84 lands once, in ACT_5, as a figure beat |
| The topic sits next to a conspiracy | Any gap the film leaves will be filled by the audience with the wrong thing | **The film leaves no gaps.** Every question it raises, it answers within ninety seconds, in a declarative sentence, with a date and a source. §5 |

---

## 3. MOTIF — five hero objects, and nothing else carries a beat

Every act is anchored to one object. No other object gets a hero close-up.

1. **The siren head on its pole.** A grey cluster of horns on a galvanised steel pole against a flat
   sky. Not menacing, not beautiful — municipal. ACT_1, and it returns in the last thirty seconds.
2. **The monthly test.** The same pole in the same frame with the light changed, cut four times in
   eleven seconds: the network doing exactly what it was built to do, exactly on schedule, at a scale
   nobody was measuring. ACT_1.
3. **A phone in a hand, showing no service.** Composited in Remotion — no generated UI, no readable
   text (⛔ `fabricated_record`). ACT_2 seeds it, ACT_3 detonates it. **The film's centre.**
4. **The chain-link gate.** A padlocked cyclone gate across a dirt access road (LH-263). ACT_4, and
   the only act of rescue the film shows.
5. **The blank sign-in sheet.** A ruled form, empty, on a plain table. Typography composited in
   Remotion, never generated (LH-290). ACT_5 and the ending.

## 3.5 SUBSTITUTION TABLE — what to show instead of what may not be shown

| may not be shown | shown instead |
|---|---|
| Any of the 102 who died; any grieving person; any memorial with a face | An unlit window; a kerb; a driveway with nothing on it; ash on a step |
| Any burned vehicle presented as containing anyone | Melted aluminium wheel rims on ash, ground-level, empty frame, no interior |
| A burning town with people in it | Grey smoke crossing a ridge; a plume seen from three miles away; light on the underside of cloud; a street in smoke with no figure in it |
| Any named official, dispatcher, duty officer or officer | A hand on a radio; a chair at a console; a back in a doorway. **Never a face with a role caption over it** |
| Any real document, alert screen, log or phone UI | Blank card, ruled form, folder, blank screen — **all typography composited in Remotion** |
| Firefighters as identifiable people | Silhouettes at distance; a hose line; a helmet on a bumper. **No insignia, no badge, no unit marking readable** |
| Hawaiian cultural imagery as scenery | Nothing. It is not a substitute for anything. It appears only where the narration is about it, and the narration is not |
| The ocean as beauty | The ocean only ever as the direction the fire was moving, shot flat and grey, never at golden hour |

---

## 4. ARC — five acts, one turn, one recognition

| section | minutes | title | what it does |
|---|---|---|---|
| HOOK | 0:00–0:20 | — | 15:00. An engine crew reports a fire twenty feet by a hundred. §8 |
| OP | 0:20–0:52 | — | `BrandOpening` 3.5 s over continuing footage, then the thesis and the promise |
| ACT_1 | 0:52–6:40 | **THE SOUND THEY KNEW** | The network: largest in the world, tested monthly, wildfires on its own published list. Then the week of forecasts that were right (LH-200–LH-206), and the two findings that explain why being right was not enough (LH-63, LH-64) |
| ACT_2 | 6:40–12:20 | **THE MORNING** | 00:22, 06:34, pole 25, contained before nine. Poles already down across the evacuation route at 05:40. The phones die in the late morning. The shelters close. **14:17** |
| ACT_3 | 12:20–18:40 | **THIRTY-EIGHT MINUTES** | 14:52. 14:55. 15:00. 15:05. 15:21. 15:23. 15:37. And **16:16** — the film's answer and its largest card |
| ACT_4 | 18:40–24:20 | **EVERYTHING THAT WAS ALREADY THERE** | Why the town could not get out and could not be fought: eight exits to six, a padlocked gate, and the water — including the myth the record kills |
| ACT_5 | 24:20–29:40 | **WHAT THE REPORT WOULD NOT WRITE** | 518 pages, 84 findings, 140 recommendations, 850 gigabytes. Finding 37. Finding 38. The records that were never produced. The settlement, dated |
| ENDING | 29:40–30:40 | — | The absence, the second-person turn, one specific ask |

**The turn** is at 16:16, at the top of the last third of ACT_3. For eighteen minutes the viewer has
been assembling a chain of minutes and expects the chain to end in a decision — a person who chose not
to press something. It does not. It ends in a **timestamp on a log**, sent over a network that had
already died, from an agency whose sign-in sheet for that day does not exist.

**The recognition** is in ACT_5: the investigation that produced 84 findings and 140 recommendations
never wrote the one sentence everybody wants, and the reason is not cowardice. It is that the sentence
cannot be shown to be true, and the film says so.

---

## 5. REGISTER — the voice

Third person. Past tense. Short declaratives. **No emotion commands** — *imagine*, *shocking*,
*unbelievable*, *heartbreaking*, *devastating*, *you won't believe* appear **zero times**. The
measured comparators use none.

**Six phrases are banned outright** because they are the register of the material this film sits next
to: *some say*, *many believe*, *questions remain*, *we may never know*, *the official story*, *what
they don't want you to know*. ⛔-04.

Numbers are spoken plainly and once. Times are spoken as times — "three o'clock", "sixteen minutes
past four" — and the film never says "shockingly late" or any equivalent; the timestamp does that work
alone. Technical terms are defined in the sentence that uses them and never twice: *wildland-urban
interface*, *Red Flag Warning*, *Wireless Emergency Alert*, *spotting*, *mopup*, *burn perimeter*.

**Two registers alternate**, and the change is the pacing device:

- **The procedural voice** — flat, specific, present in every act. "At three o'clock, Engine 11
  arrived and reported a fire about twenty feet by a hundred, moving toward the ocean."
- **The consequence voice** — one sentence at a time, never adjacent to itself. "The message went out
  to phones that had stopped working four hours earlier."

**Hawaiian words are pronounced, not avoided, and never explained twice.** *Mauka* (toward the
mountain) and *makai* (toward the sea) are defined once each, in ACT_2, because the whole geography of
this film is the difference between them — the fire came *mauka* and the warning network faced
*makai*. `Lahainaluna`, `Kuʻialua`, `Kelawea`, `Honoapiʻilani` are said correctly and not repeated more
than they need to be. **This is not colour. It is the load-bearing fact of the film's geography.**

---

## 6. THE BEAT MAP

Sixty-five to eighty-five figure beats, thirteen to seventeen per act (spec). One beat per ~22 s of
act. Beats are numbered `F01…`; each names its ledger row.

**ACT_1 — THE SOUND THEY KNEW (14 beats).** F01 the pole against sky (hero, LH-01) · F02 **"largest in
the world"** (quote card, LH-01) · F03 the map of the network, dots blooming (LH-05, *stated as
reported*) · F04 **the first business day of every month** (LH-03) · F05 the monthly test, four cuts in
eleven seconds (hero 2) · F06 the published hazard list, wildfires among them (LH-02) · F07 what you
are actually told to do — turn on the radio (LH-04) · F08 1 August, the forecast (LH-201) · F09
3 August, severe fire weather (LH-202) · F10 **"this much notice of such a warning was rare"** (quote
card, LH-203) · F11 **03:33, 6 August, Red Flag** — and Lahaina named (LH-204) · F12 gusts to 60 mph,
forecast (LH-205) · F13 **Finding 6: little perceptible difference from a typical summer day** (LH-63) ·
F14 Finding 8: the weather data came from an airport on another island (LH-64).

**ACT_2 — THE MORNING (15 beats).** F15 00:22, Olinda (LH-223) · F16 **06:34, pole 25** (LH-11, the
cause, flat) · F17 the re-energisation of broken lines (LH-11) · F18 unmaintained vegetation (LH-11,
LH-66) · F19 05:40 — poles already down at Keawe and the highway (LH-261) · F20 **"limited evacuation
from south to north"** (quote card, LH-261) · F21 contained before nine (LH-12) · F22 **no flames, no
smoke, no perceptibly combusting material** (LH-12, held) · F23 the relieving officer walks the burn;
lines already down in the gulch, standing lines swaying (LH-224) · F24 11:27, Kula (LH-223) · F25 12:50,
network issues at Lahaina locations (LH-258) · F26 **the phones die** (LH-250, hero 3 seeded) · F27
what that means, in the report's words (LH-251) · F28 13:13, shelter population zero (LH-257) · F29
14:00, Civic Center shelter closed (LH-257) · F30 **14:17** (LH-221, the act's last card).

**ACT_3 — THIRTY-EIGHT MINUTES (17 beats).** F31 the empty road at 14:30 · F32 **14:52 — rekindled by a
severe wind event** (LH-13, County's words) · F33 **Accidental** (LH-16) · F34 14:55, numerous callers
(LH-230) · F35 14:57, smoke visible (LH-231) · F36 **15:00 — twenty by a hundred** (LH-232, number
card) · F37 15:05, a shed (LH-233) · F38 how embers travel (LH-241) · F39 15:21, over the bypass
(LH-234) · F40 15:23, over Lahainaluna Road, very poor visibility (LH-235) · F41 15:28, a structure
(LH-236) · F42 15:30, vehicles (LH-237) · F43 **15:37 — the radio** (LH-238, quote card, the act's
emotional peak) · F44 16:04, an alert goes out — for Kula (LH-254) · F45 16:11, power off (LH-240) ·
F46 **16:16** (LH-255, **the film's largest card**) · F47 the network it was sent over (LH-250 recalled) ·
F48 16:30, the EOC fully activated (LH-211).

**ACT_4 — EVERYTHING THAT WAS ALREADY THERE (15 beats).** F49 the roads, drawn (LH-262) · F50 parked
cars, narrow streets (LH-69) · F51 **eight exits to six** (LH-264, number card) · F52 the gate, locked
(hero 4, LH-263) · F53 **30–50 cars** (LH-263) · F54 the saw, the tow strap, the shoulder (LH-263) ·
F55 Finding 16: no ready capability to unlock emergency gates (LH-70) · F56 Finding 76: no equipment to
remove barriers (LH-71) · F57 **the myth, killed** — Finding 21, uninterrupted power, full capacity
(LH-40) · F58 Finding 24: the houses bleeding the system (LH-41) · F59 no water from hydrants in some
parts (LH-280) · F60 "a trickle" (LH-281) · F61 Finding 23: the monitoring system fails at 15:30
(LH-43) · F62 **Finding 30: no Public Safety Power Shut-Off program** (LH-50) · F63 **Finding 61: a
statewide culture of dismissing wildfire risk — "This cannot be overstated"** (LH-60, act's last card).

**ACT_5 — WHAT THE REPORT WOULD NOT WRITE (16 beats).** F64 the Attorney General commissions it
(LH-90) · F65 "independent, unbiased, and transparent" (LH-91, quote card) · F66 Phase One: 375 pages,
12,000 records (LH-92) · F67 **84 findings, 140 recommendations, 850 gigabytes** (LH-93, number card) ·
F68 **Finding 37 — one operable siren inside the burn perimeter** (LH-30) · F69 **Finding 38 — never
used for a wildfire** (LH-31) · F70 and MEMA has since implemented a process (LH-31, second half —
**never omitted**) · F71 Finding 36: many residents did not get the text (LH-33) · F72 Finding 75: the
alert systems did not adequately inform (LH-34) · F73 **Finding 39 — people refused because there
appeared to be no official notification** (LH-35) · F74 what the agency head said, attributed and dated
(LH-120, LH-121, LH-122 — **upgraded 2026-08-21 from the read source SRC-0014; v001's LH-38 paraphrase is barred**) · F75 the County's suit against the carriers (LH-37) · F76 **the sign-in sheet that does not
exist** (hero 5, LH-290) · F77 no activity logs (LH-291) · F78 the subpoena for the siren maintenance
logs (LH-294) · F79 the settlement, procedurally, with its date (LH-111, LH-114, LH-115).

---

## 7. RETENTION MAP

Measured channel rules: half of the audience is gone by 42 seconds; the steepest loss is 10→15 s; no
explaining between 80 and 180 s; re-hook every 2–3 min; no flat stretch over 20 s; **no emotion
commands**.

| time | device |
|---|---|
| 0:00 | Voice from frame 0. No silence, no music-only runway |
| 0:10–0:15 | **The strongest single beat**: "the phones in the town below them had already stopped working" |
| 0:20 | An unanswered question stands: *then how was the town supposed to be told?* |
| 2:30 | Re-hook: the network's own list of what it is for, and wildfires are on it |
| 5:00 | Re-hook: a forecaster says this much notice is rare |
| 8:00 | Re-hook: the fire that morning, and where it started |
| 11:00 | Re-hook: **the phones die** — and the cold-open question sharpens |
| 12:20 | Re-hook: 14:17. The act ends on a time, and the next act's title is a number |
| 15:00 | Re-hook: the radio at 15:37 |
| 18:00 | Re-hook: **16:16** — the cold-open question is answered here, and a new one opens |
| 21:00 | Re-hook: a padlocked gate and a man's shoulder |
| 23:00 | Re-hook: the water myth, killed in one sentence |
| 26:00 | Re-hook: Finding 37 |
| 28:30 | Re-hook: the sheet that was never produced |
| 29:40 | The absence, and the ask |

**The cold-open loop closes at 18:00**, not at the end. What carries the last twelve minutes is the
question the answer creates: *if the town was told by a system that had already died, what was the
other system for?*

---

## 8. THE HOOK — voiced from frame 0, written FIRST

Binding from EP66 onward (spec v3 row 9). Narration audio starts at **0:00 ± 0.5 s**. No outcome
stated in the first ten seconds. Shape: a time, a place, one person doing one thing, ending on
something the subject does not know.

> **"Three o'clock on a Tuesday afternoon, on the mountain side of a town on Maui, an engine crew
> pulls up to a burning field and reports what it can see. A fire about twenty feet by a hundred,
> moving toward the ocean. It is the same field they were called to that morning. What nobody standing
> in it knows is that the phones in the town below them stopped working hours ago."**

Sixty-eight words, ~21 s at the measured pace — trim in the edit to land at 0:20 with the last clause
intact.

**What the hook may not do:** give a death toll, use the words *disaster*, *tragedy*, *paradise* or
*devastating*, name any person, name the fire's cause, or say the word *siren*. **The word "siren" is
withheld through the whole hook and the whole opening** so that its first appearance is the first line of ACT_1 and reads as the answer to the question the hook opened. The
number 102 does not appear until ACT_5.

---

## 9. WHAT THE IMAGES MUST CARRY — the motion budget, in numbers

Manual v3 row 14: anything that moves is specified in numbers, not adjectives. `fps = 30`; every
duration below is derived from fps in code, never hard-coded as a frame literal.

| element | start → end | displacement | easing |
|---|---|---|---|
| Hook plate push-in | f0 → f36 (0.0→1.2 s) | scale 1.06 → 1.00 | `Easing.out(Easing.cubic)` |
| Hook Trail motion blur | f0 → f18 | layers 6, decay 0.72 | linear decay of the blur only |
| Still cut (default) | f0 → f114 (3.8 s) | scale 1.000 → 1.055, y +0 → −18 px | `Easing.out(Easing.cubic)` |
| Cut transition | 0.4 s overlap | cross-dissolve, motion carried through | velocity never reset at the cut |
| Figure card in | f0 → f12 | translateY 48 → 0 px, opacity 0 → 1 | `spring({damping: 14, mass: 0.6})` |
| Figure card stagger | 3 frames per line | — | same spring |
| Number ticker | f0 → f24 | 0 → value, ease-out | `Easing.out(Easing.cubic)` |
| **Clock card (ACT_3 only)** | f0 → f20 | digits mask up 34 → 0 px, 2 frames apart | `Easing.out(Easing.cubic)` |
| **Siren horn (hero 1)** | f0 → f210 (7.0 s) | rotation −6° → +6°, scale 1.00 → 1.04 | `Easing.inOut(Easing.quad)` |
| Ambient overlay | continuous | drifting particulate, orbit radius 40 px, period 9 s | linear orbit, eased opacity |

**Bans, from the engine of record:** no left→right vertical sweep line, no full-screen gold wash, no
plain zoom-only cut, no opacity-only reveal, no constant-linear motion anywhere, no held frame longer
than 2 s, no naked hard cut.

**Density floors:** ≥2.5 kinetic beats per minute; animated coverage ≥25 % of body; ≥3 distinct
animated forms; animated + footage coverage ≥45 %. `depth` maps on ≥40 % of stills; ≥6 FigureBeats;
≥2 hero surfaces (`feedback_perceptual_motion_and_verify`). Long-form WebGL renders at
`--concurrency=4`.

---

## 10. PRODUCIBILITY — the staging plan, named before the shot list

**This episode's structural advantage is that it is contemporary**: modern stock is period-correct and
nothing has to be aged. Its structural danger is that **the place is a holiday destination** and the
shelf will offer holiday footage for every query in the film. `footage_review_required` is `true`.

| register | plan | ceiling |
|---|---|---|
| Sirens, poles, municipal hardware | **Commissioned plates.** The shelf has no outdoor-warning-siren subtype. Assume plates + i2v | 26 cuts |
| Dry grass, old plantation land, low scrub on a slope | Shelf, **eyeballed first** — the trap is that "grassland" returns prairie and savannah. Non-native grass on a leeward slope, no conifers, no snow | 40 cuts, ≥22 distinct |
| Smoke — plume, ridge, ground-level | Shelf + commissioned. **Never with a person in frame.** No flame closer than mid-distance | 34 cuts |
| Two-lane shoreline road, small Pacific town street | Commissioned. **Mainland-US main street is wrong** and it is what will be offered | 30 cuts, ≥18 distinct |
| Utility poles, transformers, downed lines | Shelf industrial rows **unverified** — eyeball. EP68 pinto and EP69 hyatt spent this register already | 24 cuts |
| Ash, corrugated steel, melted aluminium, standing stone wall | Commissioned. **This is the film's signature register and it must not repeat** | 30 cuts |
| Chain-link fence and gates | Commissioned, and one of them is hero 4 | 12 cuts |
| Radios, consoles, an operations room | Commissioned, blank grounds, typography in Remotion | 26 cuts |
| Phones, screens | Commissioned, **blank screens only**; every glyph composited | 14 cuts |
| Documents, forms, folders | Commissioned, blank; typography in Remotion. ⛔ `fabricated_record` | 22 cuts |

**Four rules that are not negotiable at assembly.**

1. **Run `check_cross_episode_reuse.py` BEFORE staging, not after.**
2. **Eyeball a labelled contact sheet** of the grass, smoke, street and industrial registers before the
   shot list is committed — the factory shelf's labels are known to be wrong
   (`pd-factory-shelf-mislabeled`), and "grass fire" is exactly the kind of label that returns a
   cartoon.
3. **Do not solve thinness by generating more AI plates.** The video budget splits proportionally to
   pool capacity; a bigger AI pool pushes archive cuts off screen.
4. **Codex plates arrive at 1672×941 maximum.** Upscale to ≥3840 through
   `upscale_oroville_4k_esrgan_v001.py` (Real-ESRGAN x4plus → LANCZOS) before they enter the pool, or
   `plate_review` rejects them and the builder stages them anyway — the exact EP71 failure.

---

## 11. PEOPLE — required, and none of them real

**Twenty-four people plates minimum** (spec), above EP72's twenty, because this film's people are a
whole town — residents, dispatchers, officers, linemen, firefighters — rather than three named
defendants, and the pool has to carry them without repeating.

**Faces are permitted and are wanted.** The `[NEG]` block on every people plate must **not** contain
*human face*, *facial features*, *eye contact* or *headshot*; it **must** contain *identifiable
person*, *recognisable person*, *likeness of a real individual*, *portrait of a real person*.

| never depicted as a person | why |
|---|---|
| **Any of the 102 who died** | ⛔-07. Not named, not shown, not characterised. No burned vehicle presented as containing anyone |
| **Any named official** — the agency administrator, the EOC director, the duty officer, the chiefs | ⛔-17. They appear as roles. The record is quoted as typography, never as a portrait |
| **The officer at the gate; the operator whose house burned** | ⛔-17. Narrated as actions. Never a face with a caption naming what they did |
| **Any identifiable firefighter or police officer** | Silhouette and distance; no insignia, no unit marking, no badge number readable |

The twenty-four: a hand on a radio · a back in a station doorway · a figure at a console, seen over the
shoulder · hands holding a phone with a blank screen · a silhouette against a hose line · a figure
walking a burned slope · hands on a chain-link gate · a driver's hands on a wheel in traffic · a
figure at a window looking mauka · distant figures at a barrier · a lineman on a pole, mid-distance ·
a hand closing a folder · and their variants across light and time of day.

---

## 12. WHAT THIS FILM MUST NOT SAY

The full list is `⛔-01…⛔-17` across ledger v001 and v002, plus `forbidden_claims` in the episode
spec. The **six** that will actually be tempting while writing:

1. **"The sirens failed."** Never. No source says it. ⛔-03. The form is two separate sentences with
   two separate sources: Finding 37 says one siren inside the burn perimeter was operable; reporting
   says none were activated.
2. **"If the sirens had sounded…"** Barred in every grammatical form, including the implied one — a
   pause after "and they were not used" that invites the viewer to finish it. ⛔-01, AB-01.
3. **"The power went out and the pumps stopped."** The record says the opposite in Finding 21.
   ⛔-08, AB-04. This one is dangerous because it is the version most viewers arrive with.
4. **"They left too early."** ⛔-16. Three sentences, in order, every time: they reported it out at
   14:17; the County says they went above and beyond; Finding 67 says the mopup that works in normal
   weather was not enough in that weather.
5. **"The county hid the records."** ⛔-14. The sheet was not produced after multiple requests. The
   report says the consequence in its own words. **No motive is supplied.**
6. **"Victims still haven't been paid."** ⛔-15. Procedural, and dated: notices went out in June 2026,
   an appeal over fees is pending before the Hawaiʻi Supreme Court, and while it is pending no payment
   can be made. As of August 2026.

## 12.5 AFTER EFFECTS KINETIC BEATS — five

| id | act | beat | form |
|---|---|---|---|
| B1 | ACT_1 | **the monthly test** | Four identical framings of the pole, cut on 11 frames, light changing each time; the words FIRST BUSINESS DAY mask up under the fourth and hold 1.6 s |
| B2 | ACT_3 | **the clock** | Times land as a stack: 14:55 / 14:57 / 15:00 / 15:05 / 15:21 / 15:23 / 15:37, each masking up 34 px, 2 frames apart, the earlier ones dimming to 40 % but never leaving frame |
| B3 | ACT_3 | **16:16** | The stack from B2 is still on screen. 16:16 lands **alone, on the right**, at 2.2× the size of everything else, and the whole left column dims to 25 % under it. Held 4.0 s. **The film's largest card** |
| B4 | ACT_4 | **eight to six** | Eight tick marks across frame; two extinguish, 6 frames apart; the remaining six re-centre with `spring({damping: 14})` |
| B5 | ENDING | **the sheet** | No typography. A 9.0 s hold on the blank ruled form with ambient motion only, then the endcard |

## 12.6 WHERE THE CAPTIONS BREAK

One cue = one breath group. ≤2 lines, ≤42 characters per line, 1.0–6.0 s, ≤17 cps, no orphan
single-word cue, never split a preposition from its noun. Lead 0.60 s, `_smart_split`, `medium.en`.
The phrases that will break badly if left to the splitter:

- "only one siren … was operable / within the burn perimeter" — break after *operable*, never after *was*
- "had not been utilized for warning / of WUI fires prior to August 8, 2023" — break after *warning*
- "destroying cellular phone communication / within the Lahaina region" — break after *communication*
- "Honoapiʻilani Highway" / "Lahainaluna Road" / "Kuʻialua Street" — **never split a Hawaiian name**
- "a marked and substantial" — not in this film; if it appears, it is a paste from EP72. Delete it

---

## 13. THE LIST — what the record does not have, stated in the film

From the ledger's absences, stated rather than papered over:

- **No finding says that sounding the sirens would have saved lives** (AB-01). The film says this out
  loud, in ACT_5, as the thing the report would not write.
- **No individual is named as having decided not to activate them** (AB-02). The 84 findings name
  agencies.
- **The exact mechanism by which embers survived several hours of no flame and no smoke is not
  explained** beyond "remained undetected" (AB-03).
- **We have not read Phase Three or the full MFD/ATF report** (AB-05, revised). Every load-bearing row
  is from Phase One, the Phase Two findings appendix, the AG's own decks, the County's own release, or
  HI-EMA's own page.
- **There is no primary figure for acreage, structures destroyed, or measured wind speed** (AB-06,
  revised) — and the film does not invent one. The 60 mph figure is a *forecast*, attributed and dated.
- **The water-rights and stream-diversion dispute is real and is not in this film**, because no primary
  source for it has been read (AB-07, ⛔-09).
- **Phase One says of itself that it does not analyse causation** (AB-08).

---

## 14. THE ENDING — built, not shrugged

The last ninety seconds are the film's argument and they are written in this order, and only this
order:

1. **The absence, stated flatly.** Eighty-four findings. One hundred and forty recommendations. Not one
   of them says that the siren would have changed the outcome.
2. **Why that is not a loose end.** The findings are what is left when the question of blame has been
   asked properly and has come back as a system: weather, fuel, codes, roads, water, power, warning
   (LH-60, LH-93, ⛔-13).
3. **The turn to the second person**, and it is about habit, not equipment. Every place has a warning
   system, and every warning system is really a habit — the one thing it is used for, over and over,
   until that is the only thing anyone believes it means. In Hawaiʻi the habit was the sea.
4. **What changed.** MEMA has implemented a process for activating sirens for wildfires (LH-31,
   LH-117). This is stated as fact, without irony and without "too late".
5. **One specific ask**, and it is not "subscribe". It is: *find out what the warning where you live is
   for, and what you are supposed to do when you hear it* — which is exactly what HI-EMA's own page
   tells you (LH-04) and what almost nobody knows.
6. **Hero 5 holds 9.0 s with no typography**, then the endcard. BGM resolves on a phrase; the runtime
   is not extended to accommodate it (`feedback_pd_craft_directives`).

**The ending never says the word "lesson," never says "may never happen again," and never addresses
the dead.**

---

## 15. HOW THIS SCRIPT IS SIZED — do not skip this

The declared band is **4,900–5,400 words**, and it is a **frame, not a target**.

- **`check_script_length` overcounts.** It does not strip `<!-- … -->`, and every factual line in this
  script carries a citation comment. Measured inflation on comparable scripts: +975 to +2,195 words
  (spec v3 §6.6). **It is not used for sizing.**
- **Size from `gen_narration_case.py --ep PD-2026-075-lahaina --dry-run`**, which reports the words the
  TTS extractor will actually speak.
- **Then measure, then write to the measurement.** `--measure-section ACT_1` generates only that
  section, ffprobes it, and prints the real words-per-minute. EP72's model said 171.79 raw wpm and the
  voice delivered **191.1** — 11 % faster — because the register is short declaratives. A script sized
  on the model finishes four minutes short. ElevenLabs is standing-approved
  (`feedback_elevenlabs_standing_approval`); the measurement costs about a dollar and it is the
  cheapest dollar in the build.
- The registry entry for this episode is **provisional and says so in its own comment**. Rewrite
  `design_speech_seconds` from the measurement before any full run.

**MEASURED 2026-08-21 — this is now the binding number and the step is done.**
`--measure-section ACT_1` generated 54 chunks / 808 words and ffprobed **259.133 s** of speech:

| quantity | measured |
|---|---|
| raw words per minute | **187.1** (registry model said 171.79; EP72 measured 191.1) |
| words per finished minute | **176.3** |
| script at final dry run | **349 chunks / 5,321 words** |
| speech | 1,706.4 s |
| gaps | 117.0 s (348 beat gaps @ 0.30 s, seven section boundaries @ 1.8 s, no scripted silence) |
| master | 1,823.4 s |
| **film with 9.0 s endcard** | **1,832.4 s = 30:32** |

Inside `runtime_seconds` [1740, 1920] with **92 s of headroom at the low edge and 88 s at the high
edge**. Cross-checked against the finished-minute rate: 5,321 / 176.3 + 12.6 + 9.0 = 1,832.5 s. The
two models agree to 0.1 s. `design_speech_seconds` in the narration registry has been rewritten to
1706.4 and carries this derivation in its own comment. **Do not re-measure; do not re-size.**

---

## 16. PACKAGING DIRECTION — each piece must pass ⛔ alone

Title, thumbnail text and description are **claims** and are gated as claims
(`check_packaging_claims.py`, blocking class `factual_support`). Each must survive without the film's
context to soften it.

- **Title: 59–100 characters, third person, no question form, no citation, real searchable noun
  ("Lahaina" or "Maui") as a suffix.** Written from a sentence that is actually in the script.
- **The title may not** contain a counterfactual, the word *failed*, a death toll, a victim, or any
  form of *they knew*.
- **Thumbnail: UPPERCASE, ≤4 words, one idea, huge subject, high contrast, gold `#E5B53A`**, readable
  at 320 px, ≥3 variants at 1280×720. The subject is **the siren pole or the gate**, never a fire,
  never a burned town from the air, never a person.
- Safe directions, all of which are sentences the script actually says: **ONE SIREN WORKED** (Finding
  37, and it must be paired with *within the burn perimeter* in the title so the pairing exists
  somewhere in the package) · **NEVER USED FOR FIRE** (Finding 38) · **THE ALERT WENT TO DEAD PHONES**
  (LH-250 + LH-255).
- **Forbidden on the thumbnail:** flames as the subject, an aerial of the burned town, a face, the
  word PARADISE, a question mark, a red arrow pointing at nothing.

---

## 17. HUMAN MUST CONFIRM — nine things no gate measures

1. That no frame, line, caption, card or title completes the sentence "if the sirens had sounded…".
2. That the film never once uses the shape *raise a question, leave it open* — the conspiracy register.
3. That the 14:17→14:55 gap is never adjacent to a word implying fault, and that LH-15 and LH-85 are in
   the same passage every time.
4. That no cut contains turquoise water, a resort, a palm silhouette, or anything a viewer would call
   scenery.
5. That the fire is never shown with a person in frame, and no burned vehicle reads as occupied.
6. That every on-screen document, form, screen and alert is composited typography on a blank ground —
   no generated glyph anywhere.
7. That the hook's last clause survives the trim to 0:20, and that the word *siren* is not spoken
   before 1:10.
8. That the settlement paragraph carries its date, and that it was re-verified on the day the packaging
   was written — not only on the day the script was.
9. That the ending reads as an argument about habit, not as a shrug and not as an accusation.
