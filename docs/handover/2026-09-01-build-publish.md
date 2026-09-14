# Handover — build/publish + EP77-85 design — 2026-09-01

Written mid-session at 05:00 JST while the EP73 uri render is running. Everything below is
measured, not remembered. Where a number came from a tool, the tool is named.

---

## 1. The one thing to take from this session

**Four "finished" masters that had passed every machine gate were read by eleven people, and
fifteen ship-blocking defects came out. The machine gates found none of them. And five of the
fifteen were invisible on the contact sheets — they existed only in the master.**

- **A face the sheets could not see.** EP73 uri 20:08.7: a woman steps in from frame right,
  near-frontal, sharply lit, in focus, head about a third of frame height, held ~1.2s. The sheets
  sample four frames per cut and all four caught the wall or the back of her head. Found by
  re-sampling the cut from the master at 4 fps.
- **Six readable corporate marks the 960px sheets could not resolve.** ABB nameplates, Cyrillic
  placards (ШКАФ, ЛР 221), the HollyFrontier wordmark, UTLX 663976 (Union Tank Car's reporting
  mark, in a film about a runaway oil train), an "aquablue" hull mark, MSC/MAERSK/ONE livery.
  Every one needed a full-resolution crop at 5-20x.
- **Four false statements on screen**, including a full-screen card quoting a named real
  office-holder saying words the script never used.

The procedural conclusion is in `feedback_contact_sheets_are_not_enough` (memory): the contact
sheet is the entry to a read, never the answer. Re-sample every people-bearing cut at 4 fps and
enlarge every surface that could carry lettering.

---

## 2. LIVE STATE at 05:00 JST 2026-09-01

Long-form calendar (`scripts/upload_schedule_case_v001.py`), all 12:00 JST:

| date | slug | master | read | booked |
|---|---|---|---|---|
| 08-31 | concordia | ✅ | ✅ | **PUBLISHED** `o98hKLTK93g` |
| 09-01 | uri | rendering (6th) | 74/74 on the OLD bytes | no |
| 09-02 | lacmegantic | queued | 72/72 on the OLD bytes | no |
| 09-03 | keybridge | queued | 49/49 on the OLD bytes | no |
| 09-04 | station | queued | 47/47 on the OLD bytes, PASS | no |
| 09-05 | valdez | — | — | no |
| 09-06 | colgan | — | — | no |
| 09-07 | alaska261 | — | — | no |
| 09-08..10 | threemile / max737 / katrina | — | — | no |

**Every read above describes bytes that no longer exist.** All four masters are being rebuilt
with tonight's blocks and fixes. They must be read again from scratch.

Shorts: resumed on the owner's instruction. 4 booked for 09-01 (06:00 / 09:00 / 18:00 / 21:00).
Funnel records authored for short182-197, so 09-02..09-04 are supplied.

API quota at 04:30: **3,165 units left**, resets 16:00 JST. uri's upload needs 1,650, so it fits;
nothing else long-form can go out before 16:00.

Running: `scripts/_render_uri_20260901.sh` (uri), then `scripts/_render_queue_20260901.sh` picks
up automatically and renders keybridge → station → lacmegantic. i2v restarts after each.

---

## 3. What was fixed in code, and what it is worth

| fix | commit | verified how |
|---|---|---|
| Lower-third clipped at both frame edges | `51ac1e79` | rendered uri f46405-46415, opened the frame |
| Figures.Timeline captions off frame | `4bff2186` + `6a4862aa` | rendered uri f11020-11030, opened the frame |
| AI disclosure overwriting a card | `b5497bfd` | ran build_figures on a fixture, asserted output |
| _finish_episode never pruned `factory` | `9a6008fa` | — |
| audit read the bench film, not the rendered one | `9a6008fa` | — |

**The lower-third bug had been "fixed" twice before inside the component and kept coming back,
because the component was never the cause.** FigureBeats wraps every figure in two centre-anchored
ken-burns transforms (FigureScene scale→1.16 + pan ±46, Drift scale 1.035 + pan ±17). Their own
doc comment states the safety argument: "so CENTERED content stays centered". A lower-third pinned
at left:92 is not centred content — for it the arithmetic gives ~250px of displacement, so the
left edge lands at −158. That is why the same card was reported clipped at the left in one shot
and the right in another.

**The disclosure bug cost 20 cards across 15 episodes** — the films' opening and closing
statements. `figures[0] = {**figures[0], **disclosure}` overwrites `kind`, so a kinetic card's
`lines` survived in the dict and were never drawn. morton lost "A MONSTER DID IT. DADDY WASN'T
HOME."; postoffice lost "THE COMPUTER LIED. PEOPLE WENT TO PRISON. NO ONE HAS."; concordia lost
"SIXTY-NINE MINUTES TO SAY THE WORD." **Most of those are already public.** Repairing them means
replacing a published upload — owner's call, not taken.

---

## 4. Two traps that cost real time tonight

**The film json you audit is not the film that was rendered.** `audit_films_vs_blocklist` read
`remotion/src/data/<slug>_film.json`. For uri that file had been rebuilt clean at 11:45 — five
and a half hours AFTER the 06:05 render — so the audit said CLEAN while the master carried all
five clips blocked the day before. It now reads `episodes/*/08_edit/*_film.rendered.json` first.
**But even that is not the pixels**: morandi's rendered snapshot names 50 blocked clips, and
frames pulled from the published master at those timecodes show none of them. Only a read of the
master settles it.

**A bash heredoc silently truncated a code edit.** An apostrophe inside a comment closed the
quoting early; the replacement cut off mid-comment and took `return figures` with it. `pd_edit`
reported "python parses" — because a truncated function IS valid Python, it just returns None.
The builder for every film was left broken. Restored from git and redone through a script file
with an ast check that the function still returns a value.
**Rule: multi-line code edits go in a file, never in a heredoc, and the smoke check must assert
behaviour, not syntax.**

---

## 5. What EP78-85 actually need (measured, and smaller than it looks)

The design work is **done** — all eight have a filmconfig with 69-72 figures, narration.mp3, and
312-380 image plates. What is missing:

| slug | date | factory clips | i2v motion | Root.tsx composition |
|---|---|---|---|---|
| valdez | 09-05 | **0** (need ≥40) | 179 ✅ | **missing Ep82** |
| colgan | 09-06 | 30 (need ≥40) | 156 ✅ | **missing Ep78** |
| alaska261 | 09-07 | 51 ✅ | **24/190** | **missing Ep79** |
| threemile | 09-08 | 0 | 0/190 | missing |
| max737 | 09-09 | 0 | 0/190 | missing |
| katrina | 09-10 | 0 | 0/190 | missing |

alaska261's ONLY input problem is the missing composition. Agents are staging valdez footage and
registering the three compositions now; both are non-GPU and run alongside the renders.

Remaining GPU: ~29h of i2v + ~10h of renders against ~190h of wall clock before 09-09. **The
constraint is ordering, not capacity.** Plan: clear the 09-02..09-04 renders, then give the card
to i2v for a full day.

**`scripts/select_factory_assets.py` can no longer be used.** Its ledger does not exist and
`E:\pd-media\assets\factory` is fourteen empty directories; it degrades to parsing filenames and
prints UNVERIFIED. The live shelf is `E:\pd-archive` (ledger `E:\pd-archive\_ledger`), reached
through `prestage_footage_review.py` → look at the frames → `stage_footage_by_title.py`.

---

## 6. Open, needing the owner

1. **20 lost kinetic cards in 15 mostly-published episodes** (§3). Re-render + replace, or leave.
2. **Readable brands in two published episodes** — norfolk `H8j_K1x9Dog` uses the CASE and
   KOMATSU clips; postoffice `4FlCaOVpln0` uses the EASTERN EMU. Recorded in the blocklist's
   `cross_episode_notes`; replacing a public upload is destructive and was not done.
3. **Internal ledger ids are burned into the picture** — every lower-third ends "(LM-27, LM-30)",
   "(TX-17)" etc. Readers on both films flagged that these are production references a viewer
   cannot use. May be intended house style; nobody has said.
4. **09-08..09-10 are not yet safe.** They need ~29h of i2v plus footage staging from a shelf that
   is thin for these registers. If it does not converge, those dates move rather than the quality.

---

## 7. First commands for the next session

```
git pull
py -3.11 scripts/handover_snapshot.py
tail -30 runs/logs/render_queue_20260901.log      # did keybridge/station/lacmegantic land?
py -3.11 scripts/check_shipped_frames.py --slug uri --which-master
py -3.11 scripts/audit_films_vs_blocklist.py | head -20
```

Then read the new masters — **all four of them, from scratch, at 4 fps on every people-bearing
cut, with full-resolution crops on every surface that could carry lettering.** The reads in
`runs/qc/*_shipped_frames_review*.json` describe bytes that have been replaced.
