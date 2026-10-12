# Handover 2026-08-25 — the shorts + assets lane

This lane is **asset gathering and Shorts**. This session ran from the design of 21 Shorts all
the way to 21 rendered files, rebuilt the shelf's search, walked a deep video ingest, and then
designed 18 more Shorts. **Stop here and start the next session at the audio step** — the token
audit reads 433k average context against a 300k CRIT line (§8).

Everything below is measured. Commands are inline.

---

## 1. State at handover

```
short289-309   21 RENDERED and verified: 52.2-57.8 s, coverfirst on all, funnel card on real
               frames, three gates clean. NOT uploaded (see §4).
short310-327   18 DESIGNED for EP77-82, three gates clean. No audio, no plates staged, no
               render. This is where the next session picks up.
uploads        PAUSED until 2026-12-31 by owner decision (§4). Nothing auto-resumes.
shelf search   semantic index 30,470 clips, vertical 9:16 index 30,710 clips, both rebuilt
ingest         deep video run alive since 02:01, 586 items / 114.7 GB, ledger PASS
```

Re-measure:

```
py -3.11 scripts/check_ledger_integrity.py
py -3.11 scripts/check_short_constraints.py episodes/_planning/short_designs/PD-2026-0[78]*.json
py -3.11 scripts/verify_short_designs.py | grep -E "short3(1[0-9]|2[0-7])"
py -3.11 scripts/fill_short_schedule.py --dry-run        # must print "paused until 2026-12-31"
```

## 2. The next session's job, in order

1. `py -3.11 scripts/build_all_short_audio.py --only 310,311,...,327` — voice + mix + captions.
   Expect ~2 minutes for 18 and about $5 of ElevenLabs (standing approval).
2. `py -3.11 scripts/stage_short_reuse_plates.py --short NNN` for each — 14 crops per Short.
3. Depth maps: `gen_depth_maps.py --dir remotion/public/shorts/shortNNN` **with the Python 3.10
   interpreter** (`C:\Users\aab15\AppData\Local\Programs\Python\Python310\python.exe`) — torch is
   not in 3.11. Without them the render dies inside three.js with no filename in the error.
4. `bash scripts/ae/render_beats.sh runs/ae_jobs/shortNNN.json` for each — 2 kinetic overlays.
5. `py -3.11 scripts/assemble_short.py --short NNN`, then register in `remotion/src/Root.tsx`
   (the registrations for 289-309 are the template; nothing past short327 exists).
6. `bash scripts/render_shorts.sh 310 311 312` **in chunks of three** (§5).

Measured order-of-operations warning: audio must exist before assemble (the cut lengths come
from the mix's own LINE_WINDOWS), and depth + AE overlays must exist before render.

## 3. What the 18 new designs say, and why they are shaped that way

EP77-82 are all live or legally sensitive, and each spec's `forbidden_claims` was read by hand
against every line. The constraints that shaped the writing:

* **EP77 keybridge** — a live criminal case. No Short names a defendant or repeats the
  indictment's allegation as fact; the Board's finding that Maryland were **likely unaware** is
  spoken rather than reversed into knowledge.
* **EP78 colgan** — nothing about fatigue, pay or commuting: none is in the probable cause or
  the four contributing factors. The one-in-eight check-ride failure rate is spoken so the
  captain's record cannot be read as a mark of a dangerous man.
* **EP79 alaska261** — no mechanic named, no end play figure that belongs to another carrier's
  assembly, no motive asserted for any FAA approval.
* **EP80 concordia** — no charge or trial, and the passengers' own testimony that the crew acted
  with humanity is carried so the Shorts cannot read as blaming them.
* **EP81 station** — no charges, no claim the exits were illegal, no claim the crowd panicked.
  NIST's own contrary bench result (sparks on foam, no ignition) is included so the finding is
  not overstated.
* **EP82 valdez** — no probable cause, nothing about the master or alcohol. The word
  **"grounding" is in that episode's forbidden_subjects** and the gate caught it in two lines;
  both were rewritten.

## 4. Uploads are stopped, and the stop no longer expires

Owner, 2026-08-25: do not book more Shorts, because a Shorts upload is what stops the long-form
being scheduled. Measured at the time: `PD-ShortsPush` and `PD-ShortsPush-Retry` were both Ready
and `config/shorts_pause.v001.json` said `paused_until: 2026-08-29` — four days later the push
would have resumed on its own and spent 6,600 of the daily 10,000 units. `paused_until` is now
**2026-12-31**, with the reason and the lift instruction inside the file.

The arithmetic, measured, because it is narrower than it looks:

```
daily allowance                10,000
one long-form  (insert+thumb)   1,650
four Shorts    (insert+thumb)   6,600
comments + reads                 ~450
total                           8,700   <- four Shorts and a long-form DO coexist
five Shorts                    10,350   <- this is what pushed the long-form out on 8/24
```

Publication state: **22 Shorts booked, last one 2026-08-31 06:00 JST**, nothing after. Stock that
could ship the moment the pause lifts: 32 older Shorts already in `schedule_short_youtube.py`'s
CONFIG, plus the 21 rendered here — **the 21 are NOT in that CONFIG**, so the daily push cannot
see them. Writing their titles/descriptions costs zero quota and is safe while paused.

## 5. Traps measured this session (all silent failures)

| trap | how it presented |
|---|---|
| music cue named `_v1`, library holds `_v2` | all 21 mixes died with ffmpeg status 4294967294 — an opaque -2, no filename |
| narration reused on FILE EXISTENCE | two trim passes rewrote text, index and gate output; **the audio never changed** |
| word band as a length proxy | 8 Shorts sat inside 159-180 words and rendered 58.7-69.7 s |
| `depth: true` with no depth maps | three.js "Could not load", render dead |
| CTA card never drawn | the funnel cut only fires on a plate whose role is `loop`; the designs said `close` |
| one transient image error | poisoned the bundle and every one of the next 15 renders failed instantly |
| `--cap-gb` on ingest | it is a CUMULATIVE cap against the whole 1.4 TB archive; any value stops the run at pass 1 |
| `kind` field on ledger rows | 207,846 of 211,157 rows have none, so the vertical indexer saw 7% of the shelf and said "complete" |
| semantic index paths | 18,084 of 31,480 rows pointed at files that no longer exist, 15,955 on the dead H: drive |

**The CTA one reaches the back catalogue**: short280 and short282, already published, carry
`isCta: 0`. The funnel card has been missing from shipped Shorts. Worth a sweep.

## 6. Search works again, and was proven on a real query

`index_footage_semantic.py --query "an empty courtroom with wooden benches"` returns in 7 s, and
the top hits' filenames say lecture-theatre, synagogue and house-of-representatives while their
frames are exactly what was asked for. That is the failure mode the index exists for.
`refresh_shelf_indexes.py` runs prune → embed → score after any ingest; run it when the current
ingest finishes.

Vertical index: 30,710 clips scored, **3,675 (12%) keep their subject through the 9:16 crop**,
2,513 also clear the motion and brightness floors. Before today the file did not exist.

## 7. Rights work, and what was stopped at the gate

* **Franchise/conspiracy titles self-labelled `publicdomain`** — Sesame Street reached the shelf
  as `pd` because IA licences are uploader-set. 11 quarantined, denylist added.
* **Real-incident police body-worn footage** — 20 items (Minneapolis body cam, Vegas shooting
  evidence, Cop City), then 1 more that slipped through because the list had "body worn" but not
  "worn cam". All quarantined; terms split apart in `IA_TITLE_DENY`.
* **32 of 59 quarantined video candidates restored** after a labelled contact sheet was read tile
  by tile (54% usable), via the new `restore_from_quarantine.py`. Deny round 4 written from the
  27 rejects.

## 8. Token audit (rule 20) — the reason to stop here

```
API calls        984
average context  433,166   <- CRIT line is 300,000
peak context     769,683
billed total     435,809,034   (amplification 1,158x)
```

One session carried the design, audio, depth, AE, render and QC of 21 Shorts, a search rebuild,
an ingest campaign and 18 more designs. That is five or six sessions' work in one context. The
next session should open at step 1 of §2 and nothing else.

## 9. Scope notes

* **EP50 centralpark**: skipped by owner decision (2026-08-25). It has script + 984 plates but no
  `episode_spec`, and the Shorts gates cannot run without one.
* **EP83-85**: plates ARE delivered — 188/186/70 files under `E:\pd-media\05_visuals\<slug>\img`
  — but not staged into `remotion/public/<slug>/img`, which is the assembly thread's step. Once
  staged, these three episodes can be designed the same way.
* **EP78 fukushima**: removed. It held one file recording that the premise did not survive
  verification, and EP78 became colgan on 2026-08-24.
