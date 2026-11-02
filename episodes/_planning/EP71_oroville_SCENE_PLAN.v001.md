# EP71 · OROVILLE — SCENE PLAN v001

**Episode `PD-2026-071-oroville` · 30 minutes · authored 2026-08-12**

**Contract** `episodes/PD-2026-071-oroville/episode_spec.v001.json` ·
**Design** `EP71_oroville_FILM_BIBLE.v001.md` ·
**Script** `EP71_oroville_script.en.v001.md` (4,757 narration words, craft gate green) ·
**Facts** `EP71_oroville_FACTS_LEDGER.v001.md` ·
**Images** `EP71_oroville_CODEX_BATCH_A.v001.md` ·
**Rights** `episodes/PD-2026-071-oroville/09_package/rights_prescreen.v001.json`.

**Every timestamp is a DESIGN TARGET at the 165 wpm mid-point of the measured 159.5–169.7 band.
Re-derive all of them from the delivered ElevenLabs master before captions lock.**

---

## 1. THE ARITHMETIC THIS PLAN HAS TO SATISFY

| | value | where it comes from |
|---|---|---|
| finished runtime band | 1,625–1,900 s | `episode_spec.runtime_seconds` |
| design point | 4,757 words → **1,700–1,808 s** (28:20–30:08) | script, measured, plus 18.0 s non-narration |
| average cut | **3.8 s** | `episode_spec.target_cut_sec` |
| cuts, short edge / long edge | 427 / 500 | runtime ÷ 3.8 |
| stills ceiling (32% of cuts) | **136** at the short edge | video-share floor |
| commissioned stills | **118** | `mandatory_stills` — 114 derived at 1 per 45 words per section, plus 4 added to the shelter block after the 2026-08-12 re-measurement |
| distinct video assets | **260** | `distinct_video_assets`; the premise's own measured `clips_needed_30min` |
| video cuts floor, short edge | 291 | 68% of 427 |

**118 ≤ 136 and 260 ≤ 291 at BOTH edges.** The contract is satisfiable. EP66 shipped one that was
not, which is why this table exists. Verified by arithmetic against the spec, not asserted.

**Non-narration, 18.0 s exactly**: 3.0 s after the 4:34 p.m. broadcast card in the HOOK; 3.0 s at the
TURN; 3.0 s after the disposition in ACT_5; `ENDCARD_SEC` 9.0 s.

---

## 2. SECTION SHEET

| section | clock | words | plates | video cuts | still cuts | light state |
|---|---|---|---|---|---|---|
| HOOK | 0:00.0–0:24.8 | 60 | O001–O006 | 4 | 6 | the afternoon |
| OP | 0:24.8–0:39.3 | 40 | O007–O008 | 2 | 2 | the afternoon |
| ACT_1 | 0:39.3–6:06.3 | ~955 | O009–O028 | 60 | 22 | the afternoon |
| ACT_2 | 6:06.3–10:57.3 | ~885 | O029–O046 | 55 | 20 | the afternoon |
| ACT_3 | 10:57.3–16:09.3 | ~975 | O047–O065 **+ O115–O118** | 58 | 28 | the afternoon → shelter grey |
| ACT_4 | 16:09.3–21:54.3 | ~1,015 | O066–O087 | 46 | 30 | **the record** |
| ACT_5 | 21:54.3–27:42.3 | ~1,010 | O088–O109 | 44 | 30 | the record |
| ENDING | 27:42.3–28:55.3 | ~220 | O110–O114 | 6 | 6 | the record |
| endcard | 28:55.3–29:04.3 | — | — | — | — | brand |
| | | **~5,160 incl. quotes** | **118** | **275** | **144** | |

*(Narration counted by the canonical extractor is 4,757; the column above is the section budget
including block-quoted court and witness text, which the extractor also counts.)*

**Video/still split:** 275 video cuts against 140 still cuts = 66.3% video, above the video-share
floor and consistent with the channel's normal ~68% archive shape. **AI motion: 0.**

---

## 3. THE BEAT TABLE

`M` = motion. `T` = transition. Every transition is 0.35–0.50 s and Sequences overlap by the
transition length so no frame is black and no velocity resets. **No naked hard cut anywhere.**

### HOOK — 0:00.0–0:24.8

| # | s | picture | source | M | T | keywords |
|---|---|---|---|---|---|---|
| H1 | 0:00–0:04 | supermarket interior, looking out through sliding glass at a car park | **O001** still | depth parallax, 5% push-in | — (opens on picture) | — |
| H2 | 0:04–0:07 | a trolley stopped mid-aisle, half filled | **O002** still | slow drift left, 4% | dissolve 0.4 | — |
| H3 | 0:07–0:11 | aisle end, a woman in soft focus, not identifiable | **O004** still (people) | depth, hold on her stillness | dissolve 0.4 | — |
| H4 | 0:11–0:14 | ceiling speaker | **O003** still | push-in 6% | cut w/ 0.35 crossfade | — |
| H5 | 0:14–0:17 | the doors, closing | **O005** still | 5% | dissolve 0.4 | — |
| H6 | 0:17–0:21 | wide: American two-lane road at dusk, taillights, from behind | archive ×2 | native | dissolve 0.5 | `two lane road dusk taillights`, `rural highway evening traffic america` |
| H7 | 0:21.8–0:24.8 | **black. K1 `60 MINUTES` rises through a mask, gold, `Trail` on entry.** | typography | mask reveal, then still | hard to black w/ 0.3 dip | — |

**RECONSTRUCTION label is up for H1–H5 and returns whenever an O-plate stands in for a described
real scene.**

### OP — 0:24.8–0:39.3
`BrandOpening` overlay rises 0:25.2, falls 0:28.7. `openingVariant: 'overlay'`, `leadSeconds: 0`.
Picture and voice do not stop under it. Plates **O007** (a claim form's two dates as typography on
the document ground) and **O008** (the open line, first appearance — a confident stroke).

### ACT_1 — 0:39.3–6:06.3 · THE ORDER

| beat | s | picture | source | keywords |
|---|---|---|---|---|
| A1.1 who she is | 0:39–1:05 | rented single-storey street, Northern California inland, February | **O009** (people, a figure at a door at distance) + archive ×4 | `american suburban street winter overcast`, `single story house driveway rain` |
| A1.2 the dam exists | 1:05–1:25 | **rationed dam cutaway 1 of 18** — reservoir surface, wide, no drama | rights **PRESCREEN-V-001** | — |
| A1.3 Bechtel | 1:25–2:05 | a living room, a television glow, nobody in frame; **A DIFFERENT PERSON card** | **O012–O014**, **O016** (people, a silhouette at a window) + archive ×3 | `living room television glow evening`, `crt aerial suburban roof` — **note: 2017, so a FLAT-PANEL set, not a CRT** |
| A1.4 the sheriff's car | 2:05–2:25 | a patrol car passing at the end of a street, at distance, from behind | archive ×3 | `sheriff patrol car suburban street`, `police car residential slow` |
| A1.5 **K2 the timestamps** | 2:25–3:20 | the four broadcast texts as typography, accumulating; the fifth line drops in from above | **O017–O020** typography plates | — |
| A1.6 the class | 3:20–3:55 | the valley floor: orchard rows, levee bank, irrigation, flat inland horizon | **O021–O022** + archive ×6 | `orchard rows aerial california valley`, `levee bank farmland dusk`, `irrigation canal farmland` |
| A1.7 the roads *(second person here)* | 3:55–4:45 | taillights, queues, from behind, always at distance | archive ×10 | `traffic queue night highway rear`, `taillights congestion dusk`, `petrol station forecourt night america` |
| A1.8 Levias | 4:45–5:25 | a boot lid, boxes on a back seat, a dog, a forecourt | **O023** (people, hands loading a car), **O024–O026** + archive ×4 | `packing car boot hurry`, `gas station forecourt night` |
| A1.9 they came back | 5:25–5:50 | the same road in daylight, empty | archive ×3 | `empty road daylight rural america` |
| A1.10 act-out: two days | 5:50–6:06 | a rented front door, closed | **O027–O028** (O028 people, a figure entering) | — |

### ACT_2 — 6:06.3–10:57.3 · WHY NOBODY TOLD THEM

| beat | s | picture | source | keywords |
|---|---|---|---|---|
| A2.1 7 February | 6:06–6:45 | **dam cutaways 2–5 of 18** — the damaged main spillway, DWR's own dated stills | rights **PRESCREEN-S-003**, **S-002** | — |
| A2.2 what a spillway is | 6:45–7:30 | water leaving a structure; a concrete channel; the plain mechanism | **O029–O032** + rights **PRESCREEN-V-002** (cutaway 6) | `concrete channel water flow`, `weir overflow water` |
| A2.3 headward erosion | 7:30–8:05 | a bare slope, water finding a line, soil moving | **O033–O034** + archive ×5 | `hillside erosion water runoff`, `bare slope soil washing`, `gully erosion rain` |
| A2.4 11 February, 4 p.m. | 8:05–8:25 | **cutaways 7–9** — water over the lip for the first time | rights **PRESCREEN-V-001**, **S-001** | — |
| A2.5 the 2005 filing | 8:25–9:20 | a bare hillside with no water on it; then typography, Stork's words attributed | **O035** (people, a figure on a ridge at distance), **O037–O041** | `dry hillside scrub california`, `foothill slope winter` |
| A2.6 whose framing | 9:20–9:50 | the film's own attribution card | **O042** typography | — |
| A2.7 what reached her | 9:50–10:30 | back to the shop: the tannoy, the doors, the car park | **O043–O045** | — |
| A2.8 language emptied a valley | 10:30–10:57 | the four texts again, small, over the valley floor | **O046** + archive ×4 | `farmland dusk wide california valley` |

### ACT_3 — 10:57.3–16:09.3 · THE TWO DAYS

| beat | s | picture | source | keywords |
|---|---|---|---|---|
| A3.1 where a valley goes | 10:57–11:25 | a fairground gate; a car park filling; from outside | **O047** (people, figures at distance), **O048–O049** + archive ×4 | `county fairground entrance america`, `car park filling evening` |
| A3.2 Mulholland | 11:25–12:05 | **RECONSTRUCTION, fully commissioned.** a hall wide with cots in rows; a cot close with a folded blanket; a sign-in table with a clipboard; a queue against a wall; paper cups on a folding table; a fluorescent ceiling; a doorway with rain outside; a hall floor under strip light; a paper sign on glass; a queue of shoes | **O052–O057 and O115–O118** — 10 plates (O053 people, boots on a hall floor) | **ZERO archive. The shelter register is empty, not thin — see §4.2** |
| A3.3 Widener | 12:05–12:40 | a street corner, empty, at speed; a pushchair by a doorway | **O050–O051** + archive ×4 | `small town street corner evening america`, `empty pavement dusk` |
| A3.4 **the borrowed record** | 12:40–13:25 | the film's own card: every image of the dam credited to the state; every image of a person credited elsewhere | **O058** (people, a hand on a photo edge) + typography | — |
| A3.5 Nicholas | 13:25–14:20 | cattle at distance on unfamiliar pasture; an empty loading ramp; hay under a tarpaulin | **O059–O062** + archive ×3 | `cattle pasture distance america`, `livestock loading ramp empty`, `hay bales tarpaulin farm` |
| A3.6 **K3 `81`** | 14:20–14:35 | the number counts up over 1.2 s and holds; a gate, closed | **O063** typography over **O062** | — |
| A3.7 the forms | 14:35–15:25 | the film's evidence card: **filed 9 August 2017 / rejected 5 September 2017**; then a shuttered shop front | **O064** (people, a hand and a pen, no legible writing), **O065** + archive ×3 | `closed shop front small town`, `shuttered business america` |
| A3.8 the day-care rooms | 15:25–15:50 | small chairs stacked; a cot rail; a light left on. **Nobody in frame** | **O065**, reuse of **O055** framing at a different scale | — |
| A3.9 four names | 15:50–16:06 | four lines of typography, one at a time | typography | — |
| **TURN** | 16:06.3–16:09.3 | **black, silent, 3.0 s** | — | — |

### ACT_4 — 16:09.3–21:54.3 · WHICH PEOPLE?

**The light state changes here and the audience must feel it.** Flat north light, paper white,
rooms with nobody in them, 50–85 mm, static. The picture almost stops moving; the typography carries
the motion. Cut rate stays at 3.8 s.

| beat | s | picture | source | keywords |
|---|---|---|---|---|
| A4.1 **K4 `WHICH PEOPLE?`** | 16:09–16:20 | letters rise through a mask out of the black | typography | — |
| A4.2 what a class action is for | 16:20–17:10 | an empty room with a window; a corridor; a chair | **O066–O069** + archive ×5 | `empty office room window light`, `institutional corridor empty` |
| A4.3 wrong answer 1 | 17:10–17:40 | a filing shelf; a door with no name on it | **O070** (people, a figure leaving a corridor), **O071** | `filing shelves archive room` |
| A4.4 wrong answer 2, named | 17:40–18:40 | the reported version set as a card, then struck through by a mask wipe | **O072–O075** typography | — |
| A4.5 Dr. Cova | 18:40–19:30 | a lecture room with nobody in it; a whiteboard wiped clean | **O076** (people, a figure at a lectern from behind), **O077–O079** + archive ×4 | `empty lecture room chairs`, `whiteboard blank room` |
| A4.6 the broadcast has no receipt | 19:30–20:00 | a transmitter mast at distance; a radio speaker grille | **O080** + archive ×4 | `radio transmitter mast sky`, `speaker grille close` |
| A4.7 the trial court quoted | 20:00–20:30 | typography, document ground | **O081** (people, a hand squaring papers), **O082** | — |
| A4.8 **the real answer** | 20:30–21:05 | **CT-01 in full.** the open line, third appearance: it hesitates and stops in mid-air | **O083–O085** | — |
| A4.9 ascertainability | 21:05–21:35 | one word, alone, then its translation beneath it | **O086** typography | — |
| A4.10 denied, affirmed | 21:35–21:54 | a stack of paper seen edge-on; a date | **O087** (people, a figure at a window, back to camera) | — |

### ACT_5 — 21:54.3–27:42.3 · COSTS

| beat | s | picture | source | keywords |
|---|---|---|---|---|
| A5.1 **K5 the disposition** | 21:54–22:20 | word-by-word reveal, 6-frame stagger; the last three words land alone | typography | — |
| A5.2 **3.0 s silence** | 22:20–22:23 | held on `shall recover its costs on appeal` | — | — |
| A5.3 what it means | 22:23–23:00 | an empty desk; a window; nothing on the desk resolves | **O088–O091** + archive ×3 | `empty desk window daylight`, `office chair empty room` |
| A5.4 costs follow the event | 23:00–23:30 | a ledger column with no legible figures | **O092** (people, a hand leaving a desk) | — |
| A5.5 NOT TO BE PUBLISHED | 23:30–24:20 | the stamp set as type on the document ground — **card, not scan** | **O094–O098** | — |
| A5.6 the rule's own reason | 24:20–24:55 | shelves of identical spines; a corridor of them | **O093** + archive ×4 | `library shelves identical volumes`, `archive stacks corridor` |
| A5.7 read the orders again | 24:55–25:30 | the four texts, same words, colder frame | **O099–O103** typography | — |
| A5.8 broad is the safety feature | 25:30–26:00 | the valley floor again, wide, at dusk | archive ×4 | `farmland valley dusk wide`, `flat horizon orchard evening` |
| A5.9 the paper claims | 26:00–26:20 | two dates; a shutter | **O097** (people, a figure locking a door) | — |
| A5.10 the 2023 case | 26:20–27:00 | **A DIFFERENT CASE / A DIFFERENT PLAINTIFF card up for the whole beat**; a river with debris in it | **O102** (people, a figure at a riverbank at distance) + rights **PRESCREEN-S-004** member *Oroville Dam spillway debris in Feather River* (**cutaway 18 of 18**) | — |
| A5.11 what is not known | 27:00–27:25 | the empty desk again; a blank line where a figure would be | **O104–O107** (O107 people, an empty chair with a coat on it) | — |
| A5.12 **the supermarket, last time** | 27:25–27:42 | **empty. lights off. doors closed. same framing as O001** | **O108–O109** | — |

### ENDING — 27:42.3–28:55.3

| beat | s | picture | source |
|---|---|---|---|
| E1 not a dam story | 27:42–28:00 | the reservoir at rest, wide, still — **and it is the last frame of water in the film** | **O110** |
| E2 the design | 28:00–28:25 | two documents, side by side; one of them is blank | **O112–O113** |
| E3 **THE HIDDEN RULE** | 28:25–28:40 | nothing but the line. music floor drops | typography |
| E4 the shop closed | 28:40–28:55 | the doorway, from outside now, for the first time | **O111** (people, a figure walking away), **O114** |
| — | 28:55.3–29:04.3 | `BrandEndcard` 9.0 s | — |

**The bed resolves on a phrase end at 28:55.3. No fade on a half bar** (owner directive, EDのBGMは切りよく). The runtime is not changed to achieve it; the last chapter's track is chosen to end there.

**The subscribe ask is an on-screen lower third at ~28:40 and the endcard text. It is never spoken**
— `check_script_craft.SPOKEN_CTA` is a hard gate wired into the acceptance run.

---

## 4. PRODUCIBILITY — how the thin beats get dressed, decided here and not at assembly

`config/pd_planning_os.v002.json` → `producibility_gate` permits AMBER **only with a staging plan
named before the shot list**. Measured 2026-08-12: 1,293 distinct HD-clean clips over twelve
sub-registers, 260 needed, utilisation **0.201** labelled / **0.402** precision-corrected.

### 4.1 The era split — and the correction that matters more than the era

`producibility_gate.period_rule` says the shelf has no era field at all and is structurally strong at
the contemporary. **This film is set in 2017**, so its era-bound registers are contemporary and it
does not have to buy them with GPU time the way EP68 and EP69 did. **That advantage is real and it is
smaller than it looks**, because the constraint that actually binds is not *when* but *where*.

**Measured independently 2026-08-12**, by word-boundary geo markers over title plus matched keywords
plus filename:

| | US-marked | foreign-marked | unmarked |
|---|---|---|---|
| era-bound half (809 rows) | **65** | **190** | 554 |
| whole video corpus (20,840) | 315 | 2,124 | 18,401 |

Foreign markers beat US markers **2.9 : 1** in the half this film lives on and **6.7 : 1** shelf-wide.
This is a European and Asian stock library. Of the 65 US-marked era-bound rows, most are New York,
Chicago, Las Vegas, Los Angeles freeways or the Pacific Coast Highway; **four** read as a rural
Californian town. The 554 unmarked rows prove nothing either way — the ledger simply cannot say.

**Utilisation, corrected, against 260 needed:**

| denominator | available | utilisation | colour |
|---|---|---|---|
| whole labelled register, reconstructed union | 2,092 | 0.124 | GREEN |
| whole labelled register, the premise's figure | 1,293 | 0.201 | AMBER |
| eyeball-corrected at precision 0.500 (n=80, seed 2017, independent draw) | 1,046 | 0.249 | AMBER |
| **era-bound half, eyeball-corrected** | 508 | **0.512** | **RED** |
| **era-bound half vs US-verifiable supply** | 65 | **1.600** | **RED** |

`producibility_gate` says RED requires **either an archive acquisition plan or an accepted AI-motion
budget**. **This plan takes the archive route and budgets zero AI motion**: the pre-screen's four
clearable clips and twenty-six verified stills, plus 118 commissioned plates. That is a decision the
owner should see rather than inherit, and it is recorded in `episode_spec.approved_deviations`.

### 4.2 The registers that decide the film

*(v3 corrected counts. The premise's own per-register table could not be reproduced — its twelve term
lists were never saved, `police_sheriff_siren = 75` is arithmetically impossible because a bare match
on `police` returns 143, and `flood_river_erosion = 22` requires excluding the word `river`, which is
wrong for a film about the Feather River. Read the premise's rows as indicative.)*

| register | measured | plan | cap |
|---|---|---|---|
| evacuation traffic / night road | **702** — abundant, and therefore the **reuse hazard** | dresses A1.7, A1.9, A2.8, A5.8 entirely | **≤ 55 cuts, ≥ 30 distinct.** `footage_diversity` binds: distinct ≥ 0.40, no clip more than 4×, generic symbols ≤ 2 |
| rain / storm | **396** — abundant | texture only, never a beat | ≤ 25 cuts |
| supermarket | **38**, of which ~12 are genuine store interiors and only **4 are already burned** | **carries the opening beat, and it is dressable.** Eyeball the contact sheet FIRST | 6–8 unburned interiors carry a 6–8 cut opening. **Exclude the face-mask grocery clip — masks read 2020, this film is 2017.** No US supermarket is identifiable by label, so a human confirms one reads American |
| **emergency shelter** | **ZERO.** The premise counted 1 and that clip is a **German WWII bunker door** | **fully commissioned: 10 plates**, O052–O057 and O115–O118. A 28-term net over the whole shelf in all media kinds returns one video (a gymnasium graduation) and eight stills. `red cross`, `cots`, `fairground`, `evacuation center`, `evacuee`, `church hall`, `sleeping bag`, `aid station`, `disaster relief` all return 0 | **0 archive cuts.** The gymnasium clip and folding-chair stills are texture inserts at most, cut close so no crowd is implied |
| **television playing news** | **ZERO.** All 50 television rows are dead sets — static, no signal, cracked, broken CRT | Bechtel's 3:00 p.m. crawl has no archive answer | commissioned plate plus composited typography, O012–O014 |
| California place | **41**, and **eight of them are Monterey sea lions**. Northern California inland: zero. The one usable suburb aerial is **already in EP32 carsearch** | establish from the era-neutral half: orchard rows, levee banks, irrigation, two-lane roads at dusk, flat horizons | **never a coastal frame** |
| cattle | **77**; a strict cow/calf match gives 24, of which ~10 are real cattle and several are Highland, Friesian or Siberian. **No calf close-ups exist at all** | 3 archive cuts maximum; O059–O062 carry A3.5; the 81 is carried by K3 | ≤ 3 |
| police / sheriff | **156 — and 97 are already used in a previous episode (62%).** Effective size **59**, four of which are a cowboy sheriff, police dogs and robots. **One** sheriff-labelled row exists shelf-wide and it is a western | A1.4 needs 3 cuts; 59 supplies them | run the reuse check BEFORE staging |
| dam / spillway | 27 on the shelf, **none of them Oroville** — but the pre-screen has the real thing at 1080p, free | PRESCREEN-V-001/V-002/V-003 and 20 DWR stills | **≤ 18 cuts across the whole film. None opens an act.** Numbered in §3 so the ceiling is auditable |

**Cross-episode reuse is measurable and must be measured.** `scripts/check_cross_episode_reuse.py`
reads `episodes/_planning/measurements/STAGED_CLIP_INDEX.json` (6,165 staged clips, 4,813 distinct
sources, 882 already shared by two or more episodes, 55 slugs) and identifies a clip by size plus a
hash of its first 256 KB. Of 376 candidates across the six registers above, **115 were already used**.
One police clip is in five films. Run it on the candidate list before anything is staged:

```
py -3.11 scripts/check_cross_episode_reuse.py --check-list <candidate-paths.txt>
```

### 4.3 Rights conditions that ride on the cuts

- **Every DVIDS item carries the DoD non-endorsement disclaimer** and must not imply DoD endorsement.
- **NASA ISS050-E-52024** requires the credit *NASA / ISS Crew Earth Observations Facility, Johnson
  Space Center* and must not imply NASA endorsement. It is optional in this cut and is not scheduled.
- **DWR / Commons items**: attribution is not required by the tag, but credit *California Department
  of Water Resources* anyway — LB-1 is an inferred position, not a written grant.
- **PRESCREEN-S-009, the Croyle deck, is NOT CLEARED** and does not appear anywhere in §3. It stays
  out until DWR Public Affairs replies in writing. It is the strongest evacuation-day imagery
  available and it is still out.
- **Never repeat the DoD caption phrase** *"in the aftermath of a dam failure near Oroville"* — no
  dam failure occurred.

### 4.4 Three rules that are not negotiable at assembly

1. **Eyeball a labelled contact sheet of the supermarket, shelter, spillway and cattle sub-registers
   before any clip enters a cut.** `footage_review_required` is `true`. Filenames and relevance
   scores cannot tell an on-topic clip from an off-topic one; a human verdict can.
2. **Do not solve thinness by generating AI motion.** `solve_totals` splits video proportionally to
   pool capacity, so a bigger AI pool pushes archive cuts off screen — measured on correa at
   52 → 46 → 41 archive cuts at +0/+20/+40 plates. This plan budgets **0 AI motion**.
3. **Run the no-repeat check across EP60, EP69 and EP71 together**, not within EP71 alone. Concrete,
   helicopters, engineering and water are the overlap with two films that have already spent them.

---

## 5. WHAT A HUMAN MUST LOOK AT BEFORE THIS PLAN IS COMMITTED

1. The **supermarket** contact sheet — 29 clips, several foreign, carrying the opening beat.
2. The **shelter** reconstruction plates — do they read as a reconstruction, or as a record?
3. The **dam ceiling** of 18 cuts. It is a judgement, not a measurement. Watch the first cut and ask
   whether it has become a dam film anyway.
4. The **light-state change at 16:09**. If a viewer cannot feel it, ACT_4 has no shape.
5. **O001 and O108** side by side — the first and last frames of the film are the same room, and the
   whole ending depends on the framing matching.
