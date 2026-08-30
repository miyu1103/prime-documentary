# Handover — 2026-08-30 18:30 JST, the build/publish + design lane (evening)

This session took the lane over at 17:43 with one instruction above all others: **book what is
already built, then fix.** It could not be followed, and the reason is the only thing in this
document that really matters.

**All three "finished" masters were read frame by frame, and none of them can ship.** Every
number below was measured tonight. Where something is a judgement rather than a measurement, it
says so.

---

## 1. The headline

The previous session handed over three masters as ready to book. They are not. 197 labelled
contact sheets were read tile by tile by eleven parallel readers, and every blocking finding was
then re-opened at full resolution by the lane owner before it was written down.

| slug | sheets read | defects recorded | gate |
|---|---|---|---|
| lacmegantic | 72 / 72 | **69** | FAIL |
| uri | 74 / 74 | 49 | FAIL |
| concordia | 51 / 51 | 21 | FAIL |

197 sheets, 139 recorded defects. (While the uri review was briefly incomplete the gate reported
its own coverage gap — *"18 of 74 sheet(s) carry no record of being read"* — which is worth
knowing: it checks coverage, not just verdicts.)

All three reviews are written and **bound to the sha of the master that was actually measured**:

```
runs/qc/lacmegantic_shipped_frames_review.v001.json   a4cedf13d7cc454a…
runs/qc/uri_shipped_frames_review.v001.json           9faf5f31dd47e299…
runs/qc/concordia_shipped_frames_review.v001.json     f0add8ed7bfa680d…
```

The old uri review (bound to the superseded 2e383500 bytes) is kept as
`uri_shipped_frames_review.SUPERSEDED_20260830.json`. Nothing was deleted.

**This is the part that must not be repeated.** The previous session read 74 lacmegantic sheets
and never wrote them down, so the work had to be done again. Tonight's reading is on disk, keyed
by timecode, with the reason for every entry. If this session's chat is lost, the QC is not.

### What actually stops these three

Unambiguous under `config/ship_policy.v001.json`:

- **Readable third-party marks (`rights_and_licence`).** lacmegantic alone carries
  `ESSO NEDERLAND N.V. 's-GRAVENHAGE` on a Dutch tank wagon — under the caption *"Not one hand
  brake was applied to any of the seventy-two tank cars"* — plus `Skånetrafiken` and
  `FITNESS 24SEVEN` on a Swedish tram, a German DB junction signal with its `R` plate,
  `Norfolk Southern 3073`, `Canadian Pacific 3777`, `UTLX 674027`, `STAMFORD E4` on a
  Connecticut fire appliance, `KAR KING`, `MATCON`, `CASE`, `KOMATSU`, `SOUL`, and an `EASTERN`
  livery on a European EMU. uri carries a Chevrolet bowtie, a `SILVERADO` badge, `TEREX` on a
  boom, a utility roundel on two doors, fleet number `906992` and **a front licence plate**, all
  in one shot.
- **Held identifiable invented faces (`real_person_likeness`).** Four in lacmegantic, five in
  uri. Two of the lacmegantic ones are the same fashion-stock woman in a white blouse standing
  at the securement gear — on the beat next to the criminal trial of three named men who were
  **acquitted**. One uri face is held about nine seconds, smiling, while touching frozen gas
  equipment in a film about 246 deaths.

Not a policy class, but the worst single thing found tonight:

- **lacmegantic 11:22.** The card *"47 / People killed. Thirty of them at the Musi-Café. This
  film states the figure once."* is superimposed on a **full-frame close-up of burning logs** —
  thirteen seconds before the film's own card promises *"No casualty, no rescue, no fire with a
  person in the frame. Nothing here is dramatised."* Four separate decorative fire clips are used
  as texture in a film about people who burned to death.

### One thing that is an owner call, not a measurement

**concordia's funnel.** Thirteen cuts show a cruise-line funnel marking; ten are the operator's
yellow, four capped dark blue with a blue "C", one large and near centre frame on the sunset hero
ship. The previous session rebuilt the selected thumbnail partly for this.

**But this episode's `forbidden_subjects` does not name the funnel or the livery.** It names the
capsized, listing, heeled and wrecked ship — and none of those appears anywhere in 51 sheets.
Whether trade dress alone is `rights_and_licence` is a decision. No machine verdict is available:
`--explain-policy` needs an acceptance receipt, and the receipt cannot be produced while the
shipped-frames review says REJECT. That ordering is the guard working correctly.

What is *not* a judgement call is the volume. Thirteen cuts is not one bad plate; it is the look
the plates were generated with.

---

## 2. Two verified defects in shared components

### Timeline overflows the frame — REAL, confirmed on pixels

`remotion/src/components/Figures.tsx`, the `Timeline` renderer:

```
const x0 = 220;  const x1 = width - 220;
const ex = x0 + ((x1 - x0) * i) / (n - 1);
<text x={0} … textAnchor="middle">{e.text}</text>
```

Nodes sit at x=220 and x=1700; captions are **centre-anchored on the node**. Any caption wider
than 440 px therefore falls off the frame at the first and last node, always. Seen directly:
lacmegantic 25:05→25:07 (`23 JUL 2013` → `3 JUL 2013`, last caption cut to *"under the Fishe"*,
captions colliding into *"traiRule 112 revised"*) and uri 26:45→26:50 (heading degrades to
`TIMELINE OF THE CA`, and the whole graphic sits white-on-white over a sheet of paper).

Second, latent: **`n - 1` divides by zero when a timeline has exactly one event** → NaN
coordinates.

**25 episode film jsons carry a timeline figure, 83 figures in total**, most already public:
atwater burge caniglia centralpark cleveland fieldtest flowers forfeiture frazier glover itaewon
lacmegantic lech lejeune morton norfolk postoffice robosigning surfside tekoh thompson tlo uri
willingham young. **Not fixed yet.** One fix serves all of them.

### `lowerthird` loses characters at BOTH ends — REAL, confirmed on pixels

Evidence frame, keep it:
`runs/qc/shipped_frames/uri/frames/024m43s_771__cut0301_p85.jpg`

The card whose source text is

> primary `NINE THOUSAND DOLLARS`
> secondary `The Public Utility Commission set the price … A price meant to exist for minutes ran for days. (TX-31)` (230 chars)

renders as `NE THOUSAND DOLLARS`, with body line 1 missing its leading `The` **and** cut
mid-word at `A price meant t`, and line 2 beginning `t for minutes ran for days.`

Independently confirmed on a second frame by a different reader:
`runs/qc/shipped_frames/uri/frames/017m52s_605__cut0218_p60.jpg`, where the citation is severed
mid-token as `(TX-16` hard against the right frame boundary. Two frames, two readers, two
episodes — the right-edge overrun is not in doubt.

A separate text failure of the same family, worth fixing at the same time:
`runs/qc/shipped_frames/uri/frames/019m47s_209__cut0241_p95.jpg` — the burned-in narration caption
is printed straight **across** the pull-quote's attribution line, giving
`— FERC / NERC F[Most natural gas production and processing]AGES (TX-17)`, both texts unreadable.
The same attribution is clean one second earlier, so this is a collision between two overlay
layers, not a layout constant.

One more caution for whoever picks this up: a reader watching the 20:12→20:16 card described it
as *"sliding left out of frame as a designed exit"*, which is flatly inconsistent with
`slideX = 0` in `motionkit/LowerThird.tsx`. Either a second lowerthird implementation is in play
on this composition, or the exit is being read wrongly. **Settle which component actually renders
these before editing either one.**

**Read this before trying to fix it.** I went down the wrong path first and want to save the next
person the trip. `motionkit/LowerThird.tsx` has `const slideX = 0` and a comment recording that
the owner already removed the horizontal slide on 2026-07-06/07 for exactly this symptom; entrance
is a `clipPath` wipe and exit is `translateY` + fade. **So no code path moves the text left**, and
several readers correctly identified mid-wipe frames as the designed animation rather than a bug —
they were right about those. The frame above is different and cannot be a wipe: a left-to-right
wipe reveals a contiguous left portion, it cannot delete a word from the middle of a sentence and
lose both ends at once. `WordMask` is `flexWrap: 'wrap'` so it does wrap, and short cards render
in full. **The mechanism that widens and re-centres a long card is not yet diagnosed.** Do not
patch a component used by 25+ episodes on a guess; reproduce it in the studio first with that
230-character string.

---

## 3. EP81 station — the stock-footage blocker is CLEARED

**0 → 49 clips staged**, against a floor of 40.

All 135 candidate filmstrips were read (the previous agent had managed 12 and recorded no
verdicts at all, so it was redone from 001). 86 rejected, 49 staged into
`remotion/public/station/factory`. Cross-episode byte de-dup found **0** overlaps, so nothing here
is reused from another film.

- decide file: `runs/qc/station_content_decide.v001.json`
- receipt: `runs/qc/station_title_staging.v001.json`
- `check_pool_frames` reports `binding=exact`, every staged clip carrying a per-clip verdict.

**Eight of those rejections are mine, not the rules'.** A bakery still-life, strawberries and
sugar, a garden nest box with a European blue tit, a snail crossing asphalt, a Christmas lantern
with a red bow, a Southwest desert aerial and summer wheat fields all break none of the five
rejection rules — I opened four of them myself and there is no line in a February night in Rhode
Island they can sit under. Rejecting more is the safe direction; the floor is still cleared with
nine to spare.

**The shelf's labels are still broken, and this is now proven twice.** The query `open door`
returned a French police van (plate `EV-975-SA`), a Kyiv office with a `KYIV STREET ART` poster,
Cyrillic library shelves, a Venice aerial, a `SEO` whiteboard cartoon and a flying saucer. 64% of
what the machine selected had to be thrown away by eye. Nothing mechanical catches this.

---

## 4. i2v — running, and burning ~28 minutes per episode for no reason

Restarted 17:47 and healthy. `--selftest` printed all eight episodes (the rewritten QUEUE holds)
and the pending total was 1,062, matching the handover exactly.

```
18:24  concordia DONE  motion=184/185  depth=0  saturation_exit=0  quarantined=2
18:27  station    on the card, 1 plate pending, GPU 100% / 21.7 GB
       valdez 4/179 · colgan 0/156 · alaska261 0/190 · max737 0/184 · threemile 0/181 · katrina 0/173
```

**The waste, measured:** concordia's round took 17:47 → 18:21 — **34 minutes to make two clips.**
The inner `_chain_i2v_robust.sh` loops `while count_done < TARGET`, and `count_done` counts frame
dirs under `ae-demo/wan_frames_<slug>_*`. But the **outer** queue runs
`reclaim_i2v_frames.py --apply`, which deletes the frame dirs of clips that already have an mp4.
So `count_done` reported `2` against `TARGET=185` and the loop ran to its `MAX_ATTEMPTS=60`
ceiling, restarting ComfyUI on every one of those attempts. It self-terminates, so nothing is
lost — but it costs roughly 20–28 minutes per episode, about three hours across the eight, plus
~45 needless ComfyUI restarts.

**The fix is one line in the outer script**: pass `TARGET = number of plates in ONLY` instead of
the full plate count, because with `--only` the inner loop can never reach the full count.
**It was not applied tonight, deliberately**: bash reads a running script incrementally from disk,
and `_chain_i2v_ep78_82.sh` is executing right now (pid 516850). Editing it in place can make bash
resume at the wrong byte offset. Apply it when the queue is between episodes or stopped.

---

## 5. The calendar

CONFIG was re-dated first, before anything else. It now has **no past date and no collision**
(verified by parsing the file; the one duplicate, 08-26, is oroville/itaewon, both already
public). A straight re-date was not possible — 08-31 onward was already full — so the eleven were
reordered by readiness, which is what the file's own comment says the order is for:

```
08-31 lacmegantic   09-01 uri        09-02 concordia
09-03 keybridge     09-04 station    09-05 valdez
09-06 colgan        09-07 alaska261  09-08 threemile
09-09 max737        09-10 katrina
```

**Those first three assignments are now wrong** and need re-dating again once it is known which
episode is fixed first. They were assigned before the sheets were read.

**Suggestion for the nearest slot, not yet acted on.** EP77 keybridge is the only episode whose
blocker is already cleared: its caption problem is fixed, its 17 invented-person clips were
regenerated and verified clip by clip, and it needs a render it needs anyway. Rendering it costs
~2 h of GPU that has to be paid at some point regardless, and it is the only candidate that could
still reach a near slot. It has **not** had its shipped frames read, and on tonight's evidence it
should not be assumed clean.

---

## 6. Titles — checked by hand, all three pass

Read against the scripts, not against a green check:

- lacmegantic — *"A Town Burned Because Seven Hand Brakes Were Set Where the Rule Asked for
  Nine."* `script.en.v001.md:439` "Seven hand brakes where the railway's own rule said nine";
  `:286` for the ten-per-cent-plus-two rule that produces nine.
- uri — *"246 Died in the Texas Freeze. The Warnings Were Ten Years Old."* `:20`, `:182`.
  Thumbnail `$17,000` is the household figure at `:402`, which is the correct one; `$9,000` is
  the wholesale cap per MWh and is correctly labelled as such on screen at 24:40.
- concordia — *"The Costa Concordia Took Sixty-Nine Minutes to Order Everyone Off the Ship."*
  `:303`, and `:301` for the 22:54:10 abandon-ship order.

Also confirmed on the picture, because the previous handover asked for it: **uri's
`FORFEITURE CASES / YEAR` heading is genuinely gone.** The chart at 14:32–14:37 has no heading at
all and its bars read `263 / Held below 59.4 Hz` and `540 / The nine-minute threshold`, checked on
three full-resolution frames rather than on a contact sheet.

---

## 7. The plate-verdict gap, now demonstrated rather than theorised

All thirteen concordia clips carrying the operator's funnel have plates recorded **`accept` with
an empty reason field** in `runs/qc/concordia_plate_verdicts.v001.json`.

`docs/PD_SHIP_GATE` already states this: *"レビュアーが accept した板が実際に正しいかは、出荷経路上の
どこも再確認しない — 雑なレビューは丁寧なレビューと全く同じように通る."* Tonight is the worked example.
An `accept` with no reason text should not count as a review.

---

## 8. Next actions, in order

1. **Re-date CONFIG again** once the fix order is decided. The current 08-31/09-01/09-02
   assignments assume the three are shippable and they are not.
2. **Get the owner's ruling on the concordia funnel.** It decides whether concordia is a
   thirteen-clip regeneration or a four-item fix.
3. **Fix `Figures.tsx` `Timeline`** — anchor the first and last captions inside the frame, guard
   `n === 1`. Smoke it with `npm run typecheck` in `remotion/`, then prove it on the two known-bad
   films before trusting it.
4. **Reproduce the `lowerthird` both-ends clipping in the studio** with the 230-character string
   before changing anything.
5. **Fix the i2v `count_done` target** when the chain is not executing.
6. **Render EP77 keybridge**, then read its shipped frames before assuming anything.
7. Ask the owner to re-capture `secrets/studio_cookies.txt` — still 401, still no CTR reading.

## 9. One mistake of mine

I told the owner the full-width card clipping was a systemic component bug, then read
`LowerThird.tsx`, found `slideX = 0` and the owner's 2026-07-06 fix, and corrected myself to say
it was a misread wipe. Then I opened the actual frame and the first correction was wrong — the
card really does lose both ends. **The settled answer is in §2 and it is the one supported by
pixels.** Two of eleven readers had it right the whole time; I should have opened the frame before
either statement instead of reasoning from source.

Commits this session: CONFIG re-date only. `runs/` and `remotion/public/` are both gitignored, so
the reviews, the station decide file and the staged pool are local artefacts — they are not
backed up by a push.

---

## 10. What happened after the owner ruled (added 21:10 JST)

The owner was shown the full read and gave three answers. All three are recorded in
`episodes/PD-2026-080-concordia/approvals/APR-0001.json` together with the evidence they were
given, because a ruling that lives only in chat is a ruling nobody can audit later.

1. **concordia's funnel ships as it is.** Fastest route back to a dated slot.
2. **lacmegantic and uri: fix the dangerous cuts only** — readable third-party marks and
   identifiable faces. Season mismatches, near-black holes and clipped cards are recorded, not
   fixed.
3. **A distasteful juxtaposition does not stop a ship; record it.** General, not episode-specific.
   The four blocking classes remain the only grounds for refusal.

### concordia is BOOKED — video `o98hKLTK93g`, 2026-08-31 12:00 JST

Verified on the channel rather than from a manifest: `processed / succeeded / private /
publishAt 2026-08-31T03:00:00Z`, **0 problems**. It sat in `processing` for six minutes after
upload; "uploaded" is not "shippable" and the difference was watched rather than assumed.

Nothing was deleted to get there. All 21 findings survive verbatim under `recorded_deviations`,
and the REJECT verdict is kept at `concordia_shipped_frames_review.REJECT_20260830.json`.

**The machine refused anyway, correctly, and the reason is worth keeping.**
`packaging_claims[description]` came back CONTRADICTED, class `factual_support` — a class the
rulings do not cover. The cause was real: that check is **sentence-scoped by design**, but the
description packed into one sentence what the film says in three (`script.en.v001.md:25-27`), so
no single sentence carried *passengers* + *crew* + *1,023*, and the checker reached five minutes
away for *"Not on the passengers. Not on the crew on the decks"* — a line about where the report
puts the blame, not about a count. The description now states the three facts the way the film
states them. **No threshold and no check was touched**; `refuse` → `permit`, blocking 1 → 0.

Two more things were verified before booking rather than waved through: the AI disclosure
required by invariant 11 **is** in the description (so the end card's missing AI line is
cosmetic), and the `KNOWN ON BOARD, MIN 37` figure a reader flagged as a possible contradiction
matches `script.en.v001.md:261` exactly. That one cleared a suspicion rather than confirming it,
which is the point of checking.

### EP72 and EP73 rebuilt, 23 clips removed, both clean, rendering

| | blocked | audit before → after | diversity | max reuse |
|---|---|---|---|---|
| lacmegantic | 16 clips / 18 cuts | 18 → **0** | 0.69 | 2 |
| uri | 7 clips / 12 cuts | 12 → **0** | 0.70 | 2 |

Thresholds are 0.40 and 4, so both pass with room. `audit_films_vs_blocklist` was run **before**
the rebuild specifically to watch it fail — a check never seen failing is decoration.

**Two traps worth passing on.**

*Order.* Pruning `factory` alone and rebuilding died with `14 cut(s) reference an unreadable
clip`: the asset manifest still pointed at files that had been moved. The order in
`_finish_episode.sh` is **prune factory + img + motion → `build_asset_manifest_motionfirst` →
the film**. Read the pipeline before deciding the order; I did not, and paid one failed build.

*The archive restores what you remove.* All seven blocked plates were still in
`E:/pd-media/assets/ai_video/<slug>/motion/` and `assemble_episode_i2v.py` put them back on every
run — the prune only won because it happens after the assemble. They are now quarantined in
`motion_blocked_20260830/` alongside. This is the trap §3 of the earlier handover recorded for
keybridge; it is general, not keybridge-specific.

### Rendering: `scripts/_render_after_blocklist_20260830.sh`

lacmegantic → uri → keybridge, back to back, started 20:57. **Deliberately not
`_render_queue_tonight.sh`**, which also renders concordia — now booked against sha `f0add8ed`.
New bytes would break the binding its receipt and its review both name. *Never re-render a booked
master.*

keybridge has **not** had its shipped frames read. On tonight's evidence, do not assume it is
clean because its i2v was audited.

### The GPU, and a documented trap that still bit

The chain was stopped to free the card. Killing the parent processes left VRAM at **18 GB / 100%**
— `_chain_i2v_robust.sh`'s own `kill_comfy()` comment explains exactly this: the process holding
the card is a *child* `Python310/python.exe main.py`, and killing the parent orphans it. A tree
kill plus an orphan sweep brought the card to 2,119 MiB, which was measured before launching.

Resume state: **concordia 184 · station 184 · valdez 40 · colgan/alaska261/max737/threemile/
katrina 0.** 1,023 clips remain. Restart with `bash scripts/_chain_i2v_ep78_82.sh` once the render
queue is done.

### i2v: the 28-minutes-per-episode waste is FIXED (`823dfbe2`)

The inner chain is now given `frames_present() + |ONLY|` instead of the episode's full plate
count, because with `--only` it can never reach the full count once `reclaim_i2v_frames.py` has
deleted the finished frame dirs. Measured after the edit: valdez `frames_present=39`, 139 pending
→ target 178; the old code asked for 179. Applied **while the chain was stopped** — it could not
be applied earlier because bash reads a running script incrementally from disk.

### Still open

- `Figures.tsx` `Timeline` overflow — **not touched on purpose.** Editing it mid-queue would give
  three renders three different bundles. Do it between queues, then prove it on lacmegantic 25:05
  and uri 26:45.
- The `lowerthird` both-ends clipping — still not diagnosed. See §2; reproduce before patching.
- After each render: **re-extract the sheets and read them again.** Tonight three masters passed
  every machine gate and carried 139 defects between them.
