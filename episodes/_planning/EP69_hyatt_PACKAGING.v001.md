# EP69 — PACKAGING PACKAGE (v001)

**Episode:** `PD-2026-069-hyatt` · slug `hyatt`
**Subject:** the collapse of the second- and fourth-floor suspended walkways at the **Hyatt Regency
Hotel, Kansas City, Missouri, 17 July 1981, approximately 7:05 p.m.** A steel fabricator proposed
changing one continuous hanger rod into two shorter ones. The change doubled the load at the
fourth-floor connections, from **20.3 kips to 40.7**, against a code-required ultimate capacity of
**68** and an actual capacity of **18.6**. **114 people died.** No one was ever criminally charged;
a state licensing board revoked the engineers' certificates, and they became the first American
engineers to lose a licence for gross negligence.
**Written:** 2026-08-11. **Status:** DRAFT — owner approval required before the script is locked.

> **Order of work for this episode (owner rule):** title, thumbnail and the first twenty seconds are
> designed and approved FIRST. The body is written to serve them. This document is that first
> deliverable. Nothing below may be changed by the script writer without a new revision.

---

## 0. What this is built on, and what was measured while building it

Binding inputs read in full before a word of this was written:
`episodes/_planning/EP69_hyatt_FACTS_LEDGER.v001.md` (138 fact rows, 140 machine-verified
✓ VERBATIM quotations, 21 quarantine entries, 12 open questions, and a **binding shot-substitution
table at §12**), `docs/PD_ONE_PASS_PRODUCTION_SPEC.v2.md`, `docs/PD_CANON.md`,
`.claude/rules/19-ship-gate.md`, `C:/Users/aab15/CLAUDE.md` (the opening design manual, answered
item by item as §7 below).

**The ledger's verifier was re-run before this package was written**, not taken on trust:

```bash
cd episodes/PD-2026-069-hyatt/01_research/sources && py -3.11 verify_quotes.v001.py
# VERIFIED 140 of 140  FAILED 0
```

Measurements that bind this package:

| Measured | Value | Where it came from |
|---|---|---|
| Title band | **59–100 chars**, no question form, no second person, no case citation | spec v2 row 13; `check_packaging_qc.TITLE_MIN_CHARS/TITLE_MAX_CHARS` |
| Narration pace, end to end | **159.5–169.7 wpm**; EP66's delivered master 4,278 words / 1604.211 s = **160.0** | `docs/PD_CANON.md` rule 25 |
| The narration tool's own `measured wpm` | **171.8 on EP66 — 7% fast**, because it counts speech and excludes the silence between chunks | same rule; not used anywhere here |
| Delivered script | **4,692 narration words** (`check_script_craft`, all mechanical gates green) | `EP69_hyatt_script.en.v001.md` |
| Thumbnail headline ink, this episode's candidates | **215–239 px** at size 248 (floor 150) | replicated `scripts/build_ep62_65_thumbnails.py` fitter; font resolved to `remotion/public/fonts/Anton.ttf` |
| Archive supply for this story | **14,747 distinct clips across 20 registers** (663 queries, two rounds) | `EP69_hyatt_FOOTAGE_PLAN.v001.md` |

**One thing this episode inherits and does not re-litigate.** Every PD long-form before EP66 put
11.5 seconds of silence in front of the first spoken word — an 8-second montage plus a 3.5-second
full-screen title card — straight across the 10→15 s window where the channel loses 2.13 retention
points per second. EP66 closed that hole: narration starts at 0:00 and the brand mark became a
lower-band overlay. **EP69 is built on the closed version from the start.** `leadSeconds: 0`,
`openingVariant: 'overlay'`.

---

## 1. Title candidates

Pattern (row 13): `[dramatic present-tense clause] — [what is withheld] | [The subject]`.
There is no protagonist to name here, so the right-hand side names the object instead. All four are
third person, inside 59–100 chars, none begins with a question word, none contains "you", and none
contains a case citation or the phrase "Supreme Court Case". Character counts are `len()` of the
exact string including the pipe.

| # | Title | Chars |
|---|---|---|
| **T1 ★** | A Steel Fabricator Asks to Use Two Rods Instead of One \| The Hyatt Regency Walkways | **83** |
| T2 | The Engineer Said Two Rods Were Basically the Same as One \| The Hyatt Regency Walkways | **86** |
| T3 | Nothing Got Weaker. One Beam Was Asked to Carry Two \| The Hyatt Regency Walkways | **80** |
| T4 | Two Walkways Hung From a Nut and a Washer Over a Crowded Room \| The Hyatt Regency | **81** |

**Ship T1 as A and T2 as B.** Row 13 requires at least two A/B variants; these two test the same
event from the two ends of the chain — the request, and the answer to it — so the difference between
them is attributable to one variable.

One sentence on each, and where each one can go wrong:

- **T1 — RECOMMENDED.** The only candidate that is a single physical act a viewer can picture in one
  beat, and it is the act the whole film turns on. It is drawn from the record word for word —
  ✓ *"Because of certain fabricating problems Havens proposed to Duncan the use of a 'double rod'
  system"* (CH-05). It withholds the load, the collapse, the toll and the discipline. It also puts
  no fault on the fabricator, which matters: **no tribunal in the retrieved record made any finding
  against Havens** (⛔-16, ND-07), and "asks" is a request, not a failure.
- **T2.** The strongest sentence in the whole file — ✓ *"basically the same as the one rod concept"*
  (CH-10) — attached to the person the record actually disciplined. It is B rather than A because
  it needs the viewer to already care about rods, where T1 creates the caring.
- **T3.** The film's controlling idea, and it is exactly true (LD-04, LD-20). It is the most abstract
  of the four and the least clickable at thumbnail size; kept because it is the sentence the body is
  built to prove and it may test well against an engineering-literate audience.
- **T4 — DO NOT SHIP WITHOUT AN OWNER LINE.** Every clause is accurate (DS-05, DS-06, ID-02), but
  "over a crowded room" borders on selling the casualties, and the channel's audience measures badly
  against that register. Kept here because somebody will propose it and this is the record of why it
  was not chosen.

**Accuracy note for whoever writes the metadata.** The numbers are **not interchangeable** and must
never be blended. **20.3** and **40.7** are design loads *arriving at* a connection. **68** is the
ultimate capacity the code *expected*. **18.6** is the capacity the connections *had*. **21.4** is
the load actually *on* one at 7:05 p.m. NBS's famous **31 percent** is 21.4 ÷ 68 — **a load ratio.**
The as-built **capacity** ratio is 18.6 ÷ 68 ≈ **27 percent**, NBS never states it, and it is ours
(LD-11, ⛔-01). Do not write "NIST" anywhere: it is the **National Bureau of Standards** and the
report is **May 1982** (⛔-21). Do not write "convicted" or "charged": **no criminal charges were
ever filed** (DC-21, ⛔-18).

---

## 2. Thumbnail specification

Buildable by `scripts/build_ep62_65_thumbnails.py` with a `hyatt` entry added to its `SPEC` dict —
**no new builder** (invariant 14). What that builder actually does, read from the source and then
replicated so every number below is measured rather than hoped for:

- Cover-crops the plate to 16:9 → **1280×720**, then lays a **black scrim at alpha 120 over the top
  66%** (y 0–475), so the picture keeps its own light below that line.
- Searches every contiguous 1–3 line break of the headline × sizes 248→98 step −2 and keeps the
  split whose **tallest glyph ink** is greatest while every line fits 1200 px wide. It warns below
  150 px.
- Kicker: **46 px**, drawn as a filled accent tag under the headline, shrinking only if it overruns
  the width. It has no ink fitter, so three short words is the ceiling.
- **The font it resolves to on this machine is now `remotion/public/fonts/Anton.ttf`**, verified by
  calling `build_ep62_65_thumbnails.font(100).path` today. Until 2026-08-11 it fell through to
  `C:/Windows/Fonts/arialbd.ttf` because the loader looked for `Anton-Regular.ttf`. Every ink figure
  below was produced through the current resolution path. **If anyone renames the font files,
  re-measure.**

Gate targets: `thumb_subject_luma` wants subject-box (x 0.20–0.80, y 0.12–0.88) mean luma ≥ 60,
tallest bright connected component ≥ **150 px**, dark outline ring ≥ 12 px. `thumbnail_visibility`
wants selected-thumb mean luma ≥ 33. `episode_spec.thumbnail_candidates_min` is **3**.

**Plate rules for all three, and they are hard.** No real-person likeness. **No image of the Hyatt
Regency, its atrium, its walkways, its signage or its logo** — the building is real, currently
trading under other ownership, and a plate that reads as *that* atrium is a claim this film has no
right to make (⛔-14). **No body, no injured person, no rescue, no debris, no crowd at the moment of
collapse, in any style, at any level of abstraction** (⛔-11, ⛔-12). **No readable text anywhere in
the plate**: no legible drawing, no dimension callouts, no stamps carrying a name, no engineer's
seal with real State of Missouri artwork. Generated plates commissioned at long edge ≥ 3840. **The
lower third must be the brightest part of the frame**, because the scrim eats the top 66% and the
unscrimmed band at y 475–634 is what carries `subject_luma`.

### Variant 1 — recommended, pairs with T1

- **Image:** two threaded steel rods lying side by side on a dark workbench, one long and one short,
  macro, hard raking light along the thread, a nut and a plain washer beside them. The bench surface
  is bright and uncluttered across the lower third. No hands, no text, no tooling marks that read as
  writing.
- **Headline:** `ONE ROD / TWO RODS` — **measured ink 218 px at size 248**.
- **Kicker:** `SAME STEEL` — accent RED `#D22628`.

### Variant 2

- **Image:** a single 1¼-inch threaded rod passing through a hole in the web of a hollow steel box
  beam, seen close and slightly from below, the washer and nut bearing on the underside. Clean shop
  light, no rust, no drama; the beam edge catches the light at the bottom of the frame. **This is
  hero object H1 and H2 in one still**, so the thumbnail and the film's first frame are the same
  object.
- **Headline:** `A NUT AND / A WASHER` — **measured ink 218 px at size 248**.
- **Kicker:** `114 PEOPLE` — accent GOLD `#E5B53A`.

### Variant 3

- **Image:** a drafting board in low tungsten light with a large sheet of plain vellum on it, a
  parallel rule across the sheet, one pencil resting on the edge — and the sheet is **blank**. A
  stool pushed back from the board, empty. Bright across the bottom edge where the lamp falls on the
  board.
- **Headline:** `NEVER / CALCULATED` — **measured ink 218 px at size 248**.
- **Kicker:** `NOBODY CHECKED` — accent GOLD `#E5B53A`.

Measured alternatives, if a variant has to be replaced: `TWO RODS` 218 px · `BASICALLY THE SAME`
218 px · `DOUBLED` 218 px · `114` 215 px · `ONE LINE REDRAWN` 218 px · `NOTHING GOT WEAKER` 218 px ·
`68 REQUIRED / 18.6 THERE` **239 px**, the tallest of the set.

**Archive backing for the plates.** The footage plan measured `threaded rod` at **0** usable clips,
`fastener` **0**, `workbench` **0**, `drafting table` **0**, `blueprint` **0** and `ballroom` **0**,
across two query rounds and 340 retries. **All three thumbnail plates are therefore generated, not
archive stills**, and the archive is not asked for the one thing it does not have. The retries
behind each of those zeros are in `EP69_hyatt_FOOTAGE_PLAN.v001.md` §3.

---

## 3. The first twenty seconds, as narration

Written to the katz shape — a time, a place, a person doing one thing, ending on something nobody in
the frame knows — and against the tyler failure, which summarised the outcome inside the first ten
seconds and retained 0.447. **Every one of these words is spoken. There is no silent montage and no
silent card.** The narration audio starts at 0:00.

**Pace basis.** `docs/PD_CANON.md` rule 25: measured **159.5–169.7 wpm end to end**, with EP66's
delivered master at **160.0**. The table below is timed at **160.0 wpm** and is **56 words**, so it
occupies **19.8 s at the fast edge and 21.1 s at the slow edge**. The declared window is
**0:00.0–0:21.0**, and whatever is left over at the fast edge is a hold on the last image, not a gap
in the voice. **Re-time against the real ElevenLabs render before the captions are locked** — these
are design targets, not measurements of an audio file that does not exist yet.

**HOOK — 0:00.0–0:21.0** · 56 words · voiced from frame 0 · written before the body, not after it.

| Time | Words spoken | On screen |
|---|---|---|
| **0:00.0–0:02.0** | "Kansas City, Missouri. January 1979." | H001 — hero object **H1**: one 1¼-inch threaded rod, macro on black, turning slowly, hard raking light running along the thread. No context, no scale, no room. |
| **0:02.0–0:06.9** | "In a fabricator's shop, somebody redraws one detail on a hotel walkway." | H002 — a fabricator's bench in low shop light, a straight-edge and a pencil on a sheet, hands out of frame. 0.4 s motion-blurred push, then hold. |
| **0:06.9–0:11.0** *(THE BEAT)* | "One long steel rod becomes two shorter ones, four inches apart." **"two shorter ones" lands at ≈0:09.1.** | H003 → H004 — hero object **H3**: PD's own clean line drawing of the one-rod detail, drawn live in white on ink; then the second rod arrives **in a single stroke**, offset four inches, and the first line dims. This is the only cut in the hook that changes meaning rather than subject. |
| **0:11.0–0:14.0** | "Nobody has ever established whose hand drew it." | Cut to black-level 12% for 4 frames, then back on the same drawing with the pencil gone. The line lands on the cut, not inside a shot. |
| **0:14.0–0:18.4** | "Two walkways will hang from that detail, over a crowded room." | H005 — a wide of a large **empty** atrium, generic, unpeopled, warm afternoon light through glass above. **Nothing in this shot is the Hyatt Regency and nobody is in it** (⛔-12, ⛔-14). |
| **0:18.4–0:21.0** | "On the drawing, it looks like the same thing." | H006 — back to **H1**, the rod, still turning, filling the frame. |
| **0:21.0–0:21.4** | *(hold — the question is standing, unasked)* | The rod, still turning. |
| **0:21.4–0:24.9** | "That detail is a nut, a washer, and a hole through a steel beam…" *(first line after the window — the OP)* | Same shot; the brand overlay rises over the lower band here (§4). |

Exact words at exact seconds, as asked: *"Kansas"* at 0:00.0 · *"1979"* at ≈0:01.4 ·
*"redraws"* at ≈0:04.4 · *"walkway"* at ≈0:06.3 · *"two shorter ones"* at ≈0:09.1 ·
*"four inches"* at ≈0:10.1 · *"Nobody"* at ≈0:11.0 · *"hand drew it"* at ≈0:13.3 ·
*"hang"* at ≈0:15.3 · *"crowded room"* at ≈0:17.5 · *"the same thing"* at ≈0:20.3.

**What is deliberately absent from these twenty-one seconds:** the collapse, the date 1981, the
number 114, the word *dead*, the word *investigation*, the word *board*, the two engineers' names,
the load figures, and any statement that anything went wrong at all. A viewer at 0:21 knows that
somebody changed one line on a drawing, that nobody knows who, and that two walkways were going to
hang on it. **That viewer does not know that the building fell, and does not know that the change
doubled the load.** That is the standing question, and the body spends twenty-nine minutes paying it
off.

### Every clause traced to the ledger, before this is recorded

| Clause | Ledger row | Status |
|---|---|---|
| "Kansas City, Missouri. January 1979." | RV-01 ✓ VERBATIM (shop drawings dated 7 Jan – 9 Feb 1979) | exact |
| "In a fabricator's shop, somebody redraws one detail" | CH-01 ✓ *"shop drawings were prepared by the steel fabricator which called for the use of two sets of hanger rods rather than a single set"* | exact |
| "One long steel rod becomes two shorter ones" | CH-02 ✓ VERBATIM | exact |
| "four inches apart" | CH-04 ✓ (NBS §10.5 and §3.3) | supported |
| "Nobody has ever established whose hand drew it." | CH-07 ✓ *"The chain of events has never been exactly determined"* · ND-01 | exact |
| "Two walkways will hang from that detail" | DS-01 ✓ VERBATIM · EV-03 ✓ VERBATIM | exact |
| "over a crowded room" | ID-02 ✓ *"Approximately 1500 to 2000 people were in the lobby"* | supported |
| "On the drawing, it looks like the same thing." | CH-10 ✓ *"basically the same as the one rod concept"* — the film's own compression of a quotation it will read in full at 8:07 | supported |

**Nothing in the hook is an inference about anyone's state of mind**, which is what ⛔-15 forbids,
and **no individual is named, characterised or given invented dialogue.** "Somebody" is the honest
word: the record says so itself (CH-07).

---

## 4. Where the brand opening and the brand endcard go

**`BrandOpening` is placed at 0:21.4**, as a 3.5-second lower-band overlay running **0:21.4–0:24.9**,
over footage and narration that never stop. **`BrandEndcard` is placed at the tail**, 9.0 seconds
long, starting at `narrationSeconds` and running to the end of the composition — i.e. at
**≈29:50–29:59** at the design point. Both are the canonical components in
`remotion/src/components/Bookends.tsx`; **neither is forked** (invariant 14, spec v2 row 14, which
fixes `OPENING_SEC = 3.5` and `ENDCARD_SEC = 9.0`).

**OP — 0:21.4–0:33.4.** The `OP` narration section runs under and past the overlay; the voice does
not stop for the brand mark. That is the entire reason the overlay exists.

Why 21.4 and not earlier: the hook window closes at 21.0, and a brand mark that arrives on top of a
standing question costs less than one that arrives instead of a question. Deleting it is not
available — `op_ed_bookends` is a hard gate measured on the built film by
`check_final_acceptance.check_bookends`, which was rewritten on 2026-08-10 precisely because
`leadSeconds: 0` with no variant used to render **no opening at all** and still pass.

`film.json` for this episode therefore declares, explicitly, both of:

```
"leadSeconds": 0,            // narration starts at frame 0; no silent lead
"openingVariant": "overlay"  // BrandOpening renders as a lower band, not a full-screen card
```

An `openingVariant` that is absent means `'card'`, and `leadSeconds: 0` with `'card'` is the
combination that renders nothing. **Both keys are declared. Neither is inferred.**

---

## 5. Subscribe ask and comment question — and the conflict, stated rather than resolved

**There is a live contradiction between two binding requirements and I am not going to pick one
silently.**

- `scripts/check_script_craft.py` line 42, `SPOKEN_CTA`, **fails any narration containing the word
  "subscribe"**, and it is a HARD check wired into `check_final_acceptance` through
  `check_script_craft.evaluate`. Its basis is measured: 46 published Shorts read a call to action
  aloud and 45 of them converted zero subscribers.
- The channel's own documents ask for a **spoken** subscribe ask at the reversal beat, and
  `pd-growth-countermeasures` records subscription conversion as the highest-ROI unfixed problem.
- **EP66 is red on exactly this conflict.**

**What EP69 does, and why.** The ask lands at the reversal beat, at the same second it would have
been spoken, **as on-screen type and a pinned comment — not as narration.** The film's spoken word
count therefore contains no CTA and `check_script_craft` is green (verified: `spoken CTA: 0`).
This is recorded in `episode_spec.approved_deviations` as **OWNER DECISION REQUIRED**, because it is
a deliberate choice between two rules and the owner may want the other one. **If the owner wants it
spoken, one sentence goes into ACT_2 and the acceptance receipt goes red on `script_craft`; that is
the whole cost, and it is knowable in advance rather than discovered at the gate.**

**Where the reversal is.** It is not the collapse. It is earlier and smaller: the viewer assumes
that a change approved by an engineer was checked by an engineer. **Measured position 6:37** — the
line "The fourth floor connection went to about forty point seven", carrying AE beat
`ep69_kin_doubled`, immediately before the technician's question at 7:49.

**Subscribe ask, on screen 6:52–7:02, lower third, over the load bar. Every clause is true and
checkable:**

> There are more cases like this one on the channel already, and more coming.
> If you want them, subscribe.

- "more like this one already" — true; the catalogue is records, procedure, and what happens when a
  system's ordinary behaviour is lethal.
- "more coming" — true; the 12:00 JST long-form slot is filled with further episodes in build. It
  promises no sequel to *this* episode, which the owner has rejected before as a lie.
- No emotional command, no "smash", no "if this made you angry". The measured audience responds
  badly to those.
- **Do not** add "and hit like" here. The earned Like ask stays in the ending card.

**Comment question, pinned at publish and set on screen once at ≈7:04–7:12:**

> A technician asked whether two rods were as strong as one, and was told they were basically
> the same. Name one thing he could have asked for that would have settled it in an afternoon.

Answerable by anyone who has just watched the load path move (a calculation is the obvious answer,
and the firm's own procedure required one — RV-09), specific to this episode, not a yes/no, not an
emotional prompt. Pin it at publish and put it verbatim in the description's second line.

---

## 6. Where I chose against something binding, and why

1. **The 8-second silent montage hook (spec v2 row 9) is replaced by a 21.0-second voiced cold open
   written FIRST.** Same deviation EP66 and EP67 took, same reason: the current row-9 structure lays
   11.5 seconds of silence across the steepest retention loss in the film. **This needs an owner
   approval record (APR) before the build starts.**
2. **AE kinetic beats: six, not the "one or two" the 2026-08-04 approval names, and one of them is
   in the ENDING.** This record's argument is carried by six numbers — 20.3 / 40.7 / 68 / 18.6 /
   21.4 / 114 — and a film that says them without showing them is a film that will be misquoted.
   Two of the six are deliberately paired inside forty seconds at the turn, as the arithmetic
   climax. Named and bound to their script lines in `scripts/ae/jobs_ep69_hyatt.json` and in film
   bible §12.5. **This widening also wants an owner line.**
3. **The subscribe ask is on screen rather than spoken.** §5. **Owner decision required.**
4. **The film shows no photograph or frame of the actual event, and says so out loud at 12:40.**
   ⛔-10 is a standing prohibition, not a judgement call, but *telling the audience* that the
   footage exists and is not being used is a choice. It is made because the audience will otherwise
   spend the act wondering where the pictures are, and because the ledger's §12 substitution — the
   empty room at three o'clock, at half past four, and at seven — only reads as a decision if it is
   named as one.
5. **The ending stops at 26 January 1988 and says so.** Open question ○-06 — whether Daniel Duncan
   and Jack Gillum are living — **is not closed**, and the freshest retrieved information about
   either man is from 1994–95. **This must be closed before the script locks and again before
   publish.** An R3 episode that criticises named professionals on the record of a state board
   cannot be wrong about whether they are alive.

---

## 7. OPENING OVERLAY — 動画オープニング設計書ルール準拠

`C:/Users/aab15/CLAUDE.md`（動画オープニング設計書の作成ルール）に従い、すべて数値で書く。
同ルールが禁じる抽象表現はこの節に一つも無い。**フレーム直書きはしない。**F値はすべて
`Math.round(秒 * fps)` の算出結果であり、括弧内は 30fps のときの実数である。

### 7.0 環境・Remotion設定（マニュアル セクション0）

リポジトリから読んだ実値。**記憶ではない。**実装者はここだけ見れば調べ直す必要がない。

| 項目 | 値 | 出所 |
|---|---|---|
| 解像度 | **1920 × 1080** | `remotion/src/brand.ts` `BRAND.video` |
| fps | **30**（オープニング設計書ルールの例示は60だが PD 長尺は 30。**F値は必ず `useVideoConfig()` の fps から算出**） | 同上 |
| composition id | **`Ep69Hyatt`**（`remotion/src/Root.tsx` に登録・中身は既存 `CaseFilm` を呼ぶだけ） | `Root.tsx` |
| durationInFrames | `Math.round((narrationSeconds + ENDCARD_SEC) * fps)`（`leadSeconds: 0` のため hook 分の加算は無い） | `CaseFilm.tsx` の算出式。**直書き禁止** |
| 中間画像フォーマット | **png**（`setVideoImageFormat('png')`） | `remotion/remotion.config.ts` |
| コーデック | **h264 / libx264**・**CRF 16** | 同上 |
| pixelFormat | **yuv420p** | 同上 |
| colorSpace（色空間） | **bt709**（`setColorSpace`） | 同上 |
| 音声 | **aac**・ビットレート **320k** | 同上 |
| GPU | **angle**（`setChromiumOpenGlRenderer('angle')`） | 同上 |
| 並列度 concurrency | `os.cpus().length`。ただし WebGL/深度を含む長尺は **`--concurrency=4`** | 同上＋正典 §7 |

必要な依存パッケージ（**導入済み。再インストール不要**）:

```bash
npm i @remotion/motion-blur     # Trail。7.3 の入退場に使う
```

**新規 Composition を作らない。** `Ep69Hyatt` は `CaseFilm` を呼び、`BrandOpening` に
`variant='overlay'` を渡すだけである。部品を fork しないこと（invariant 14）。

### 7.1 前提と不変条件

- 対象は既存部品 `remotion/src/components/Bookends.tsx` の `BrandOpening`。**新規作成しない**。
- 追加するのは `variant` プロップのみ。既定 `'card'` は現行の全画面3.5秒であり、
  **EP62–65 は1ビットも変わらない**。EP69 は `'overlay'` を指定する。
- `OPENING_SEC = 3.5` と `ENDCARD_SEC = 9.0` は**変更しない**（row 14 が固定と定める）。
- `BrandEndcard` は末尾 **9.0秒**（`Math.round(9.0 * fps)` = 270F）。位置は
  `from={Math.round(narrationSeconds * fps)}`。

### 7.2 秒数ベースのタイムライン（開始 21.40s ／ 全長 3.50s）

| 区間 | 秒 | F | 内容 |
|---|---|---|---|
| in | 21.40–21.80 | 0–12 | 帯とモノグラムが下から入る |
| in | 21.53–22.00 | 4–18 | シリーズ名が切り上がる |
| in | 21.67–22.20 | 8–24 | タイトルが切り上がる |
| hold | 22.20–24.00 | 24–78 | 静止。裏は動き続ける |
| out | 24.00–24.90 | 78–105 | 3要素が下へ抜ける |

**ナレーションは止めない。**この 3.5 秒の裏で `OP` セクションの台詞が進む
（0:21.4–0:33.4・33語）。これが本節の存在理由である。

### 7.3 各モーションの数値（**等速は禁止**・opacity 単独も禁止）

| 要素 | 開始F | 終了F | 移動量 | イージング | opacity |
|---|---|---|---|---|---|
| スクリム帯 | 0 | 12 | translateY **+72 → 0 px** | `spring({fps, config:{damping: 20, mass: 0.6}})` | 0 → 0.82（**translateY と併用**） |
| モノグラム | 0 | 12 | translateY **+40 → 0 px** ／ scale **0.94 → 1.0** | `spring({fps, config:{damping: 18, mass: 0.5}})` | 0 → 1（併用） |
| シリーズ名 | 4 | 18 | translateY **+100% → 0 px**（親 `overflow:hidden`） | `Easing.out(Easing.cubic)` | 常時 1（**マスクで見せる**） |
| タイトル | 8 | 24 | translateY **+100% → 0 px**（親 `overflow:hidden`） | `Easing.out(Easing.cubic)` | 常時 1（同上） |
| 退場（3要素） | 78 / 84 / 90 | +15 | translateY **0 → +64 px** | `Easing.in(Easing.cubic)` | 1 → 0（併用） |

- **スタッガー**：入場は +4F ずつ、退場は -6F ずつ。3要素を同時に動かさない。
- **モーションブラー**：入退場の translate に `@remotion/motion-blur` の `Trail`
  （`layers={6} lagInFrames={1.2}`）。hold 区間には掛けない。
- 数値はすべて**定数として1箇所**に置く：`OVERLAY = { inF: 12, holdF: 54, outF: 15, bandH: 360, scale: 0.36 }`。

### 7.4 レイヤー構成（下から。最低3層の要件を満たす）

1. **本編カット**（`OffthreadVideo` ／ 静止画）— 止めない。overlay は上に乗るだけ
2. **スクリム帯**（画面下 22%・`rgba(8,10,14,0.82)`・上端 12px はグラデでフェード）
3. **モノグラム**（左・高さ 64px）
4. **文字**（シリーズ名 28px ／ タイトル 46px・`overflow:hidden` の親でマスク）

全画面カードと違い **1層目が生き続ける**。「話が止まらない」の実装上の意味はこれである。

### 7.5 props と型

```ts
type BrandOpeningProps = {
  seriesLabel: string;
  title: string;
  subtitle?: string;
  variant?: 'card' | 'overlay';   // 既定 'card' = 現行。EP62-65 は無変更
};
```

`film.json` 側が受け取る props 名は **`openingVariant`**（`'card' | 'overlay'`）と
**`leadSeconds`**（number）。EP69 は `openingVariant: 'overlay'`・`leadSeconds: 0`。
どちらも任意項目であり、宣言しない既存話の挙動は変わらない。

### 7.6 確認方法

`npm run studio` で `Ep69Hyatt` を開き、**21.4s と 24.9s の前後 15F** を1コマ送りで確認する。
見る点は3つ——①本編カットが裏で動き続けているか ②文字が下からマスクで現れるか
（フェードだけになっていないか） ③3要素が同時に動いていないか。

**書き出しコマンド**（マニュアル §5 の「props 差し替えで量産できる形」）:

```bash
# 本番（全尺）
bash scripts/_finish_episode.sh hyatt Ep69Hyatt 69

# オープニングだけ確認する（0:19–0:27 ＝ frames 570-810 @30fps）
cd remotion && npx remotion render Ep69Hyatt ../out/ep69_op_check.mp4 \
  --public-dir=public_ep69 --frames=570-810

# variant を差し替えて比較する（card = 現行の全画面 ／ overlay = 本設計）
cd remotion && npx remotion render Ep69Hyatt ../out/ep69_op_card.mp4 \
  --public-dir=public_ep69 --frames=570-810 \
  --props='{"openingVariant":"card"}'
```

**props を差し替えるだけで両方が出せること自体が要件である。**`variant` をコードに直書きしない。

## 8. What must happen next, in order

1. **Owner approves T1 (+T2 as B), one thumbnail variant, and the 21-second cold open** — this
   package, before the script is locked.
2. **APRs written** for the four deviations in §6: the row-9 hook inversion, the six AE beats, the
   on-screen (not spoken) subscribe ask, and naming the withheld footage on air.
3. **○-06 closed** — whether Daniel Duncan and Jack Gillum are living — before the script locks and
   again before publish. Nothing else in the package depends on the answer; the ENDING is written to
   stand either way.
4. **`scripts/ae/kinetic_beat.jsx` taught to read `job.canvas`** through `scripts/pd_edit.py`, then
   `scripts/ae/render_beats.sh scripts/ae/jobs_ep69_hyatt.json`. Line 32 currently hardcodes
   `var W = 1080, H = 1920` and every beat will come out portrait.
5. `episodes/PD-2026-069-hyatt/episode_spec.v001.json` — **written and validating** (it is).
6. Footage staged from `EP69_hyatt_FOOTAGE_PLAN.v001.md` §4, **with a labelled contact sheet looked
   at by a person before any clip enters a cut**, and with the period screen in `era_setting`
   applied by eye — the shelf's steel and construction registers are dominated by 2015–2024
   material and no machine gate measures a decade.

*This document is the contract for the front of EP69. If a later stage wants to change the title,
the thumbnail or the first twenty seconds, it writes v002 and gets it approved again — it does not
edit this file.*
