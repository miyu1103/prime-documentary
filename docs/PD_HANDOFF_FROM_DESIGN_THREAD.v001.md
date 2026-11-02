# What a designed episode must carry before it reaches the build thread

Binding for EP77-EP85 and everything after. Written 2026-08-25 by the build/publish thread
after five episodes arrived "designed" and each one then cost the GPU two to three extra
hours for things that could have been settled before a single frame was rendered.

The build thread's job is: assemble → render → read the shipped frames → book. It is not a
second design pass. Every item below is something that, when it is missing, stops that job
dead — and the stop is always discovered late, because most of them are only visible after a
2.5-hour render.

---

## Why this document exists (the measured cost)

On 2026-08-25 the build thread rendered EP74 itaewon **three times** and EP75 lahaina
**twice**. About five of the thirteen GPU hours that day were re-work, and every cause was
knowable in advance:

* 17 clips of foreign footage in two episodes — a New York subway sign, a Taipei bridge,
  Moscow, Venice, an Icelandic moorland, an Andean altiplano — all of which had been *kept*
  during pool selection with the note "anonymous, no place tell". At contact-sheet size the
  tells are not legible. At full frame they are unmistakable.
* Six studio food close-ups running under fatality statistics and a legal amendment.
* 37 of 91 generated clips that opened in colour and played out grey.
* Declared people plates that existed nowhere on disk.

None of that is a design opinion. All of it is a check somebody has to run once, and it is
cheaper by hours to run it while the episode is still on paper.

---

## The checklist

### 1. `episode_spec.v*.json` — the machine contract

Nothing reads a number from prose. The spec is the only place a tool looks.

- [ ] Validates against `schemas/episode_spec.v001.json` (`py -3.11 scripts/check_episode_spec.py --slug <slug>` exits 0).
- [ ] `people_plates` is a **list of the actual filenames** that show a person — not a count,
      not a plan. Every name in it exists in `remotion/public/<slug>/img/`.
- [ ] `people_plates_min` is a number the episode can actually meet. If the film has 12 people
      plates, do not declare 24 and leave it for the build thread: the gate refuses the build
      and the declared value may not be lowered to make it pass.
- [ ] `distinct_video_assets` is at most the number of clips actually staged. Declaring 265
      against a 191-clip pool produces a permanent red gate that everyone learns to ignore.
- [ ] `forbidden_subjects` includes **place terms**, not only subject terms. For a Seoul film
      that means `japan, kyoto, kobe, china, taipei, taiwan, hong kong, singapore, moscow,
      russia, paris, france, london, venice, italy, warsaw, dublin, brno, mexico, australia,
      new york, nyc, brooklyn, texas, austin, vietnam, netherlands, europe` and any other
      place the shelf might hand you. This one line catches contamination by filename before
      the GPU is spent — it caught 32 cuts on EP74.
- [ ] `mandatory_stills` names files that exist.

### 2. The footage pool — judged at FULL FRAME, not at sheet scale

**This is the single biggest source of re-renders.** The rule that failed all week was
"anonymous keeps": a clip with no visible tell was kept. Seven of those turned out to be
foreign footage once they filled the screen.

- [ ] Every staged clip has been opened at full frame, not judged from a contact sheet tile.
- [ ] **Ambiguity fails closed.** If you cannot say what country a clip is in, reject it.
      The one exception is genuinely place-free material — macros, hands, rain on glass, an
      unmarked interior — which is fine anywhere.
- [ ] The country test depends on what the LOCAL language is. In a Seoul film the *absence*
      of hangul is itself a tell. In a Texas film English signage is expected and carries no
      tell. Apply the right test for the episode.
- [ ] No clip whose filename names a foreign place, whatever the frames appear to show.
- [ ] No identifiable real face held in frame; no readable brand, shop sign or wordmark.
- [ ] Meaning matches the narration. A close-up of grilled pork under "one officer for every
      730 people" is Korea-correct and still wrong.
- [ ] `runs/qc/<slug>_clip_verdicts.v001.json` records a verdict for **every** clip, with the
      reason for each reject, and is bound to the pool's `pool_id_sha256`.
- [ ] Rejects are moved to `factory/_eyeball_reject/`, not left in the pool.
- [ ] The pool holds at least 40 clips and enough distinct assets to meet the declared floor.

### 3. Generated plates

- [ ] `runs/qc/<slug>_plate_verdicts.v001.json` carries a resolved verdict for every plate,
      each bound to that file's sha256 (`check_plate_verdicts.py --scaffold` then read them).
- [ ] No plate shows an identifiable real person, a readable document, a watermark or a
      generator mark.
- [ ] Plate numbering does not collide with an existing file. A re-order that reuses a live
      id overwrites a plate that is already in the film — EP72's "add L168" order named a
      plate that had been in the manifest for three days.
- [ ] Every ordered plate is 16:9 and at least 3840x2160.

### 4. Generated motion (i2v), if the episode uses it

- [ ] `py -3.11 scripts/check_motion_saturation.py --slug <slug>` exits 0. It fails a clip
      that starts in colour and ends grey — the defect that put 37 broken clips into EP75.
- [ ] Spot-check the end frame of a sample of clips against their source plates. The
      generator will invent content that is not in the plate: on a bare concrete wall it
      produced a man in a suit, and on a roadside it produced a woman's face.
- [ ] No `*_depth` file anywhere in `img/`, `motion/` or the archive. Depth maps are renderer
      inputs and have shipped as picture twice.

### 5. `EP<NN>_<slug>_filmconfig.v001.json`

Schema `pd_filmconfig.v001`. Copy `episodes/_planning/EP75_lahaina_filmconfig.v001.json` and
change the values. It must carry:

- [ ] `slug`, `episode_id`, `assets`, `narration_index`, `narration`, `captions`, `out`
      — all pointing at files that exist.
- [ ] `hookSeconds` and `hookLine` taken from the actual narration, not estimated.
- [ ] `figures_by_section` — the on-screen cards, per section, each with a `_row` naming the
      claim it comes from. **Every number on a card must be a number the script says**, and
      every `value` must be numeric: a string in a `stat` card renders as `NaN` in 100-pixel
      type, which is exactly what shipped on EP76.
- [ ] The AI-visualization disclosure lower-third in `HOOK` (invariant 11).

### 6. Remotion composition

- [ ] `remotion/src/Root.tsx` has a composition whose id starts with `Ep<NN>` (e.g. `Ep77KeyBridge`),
      with its component and duration wired. Without it the build refuses before it starts.

### 7. Packaging

- [ ] `09_package/youtube_meta.v001.json` exists — the booking path reads only this file, and
      no episode can be scheduled without it.
- [ ] `description` is **under 5,000 characters** (the uploader enforces this) and passes
      `py -3.11 scripts/check_packaging_claims.py --slug <slug> --package` with **0 hard
      failures**. Write the description from the script's own sentences; paraphrase gets
      flagged as unverified.
- [ ] Title passes the same checker. Every number, date and name in it must be in the script.
- [ ] At least **three** thumbnail candidates at 1280x720 in `09_package/`, plus
      `thumbnail.selected.v001.png`.

### 8. Audio and captions

- [ ] `06_audio/narration_index.v001.json` exists and the master VO is on disk.
- [ ] `08_edit/captions.final.v001.srt` exists (the canonical name — a working split with a
      different name will be measured by mistake).

---

## The one command that tells you if you are done

```
py -3.11 scripts/check_episode_inputs.py --slug <slug>
```

**`READY to build` is the handoff condition.** Anything else is unfinished design work, and
the build thread will send it back rather than spend the GPU on it.

---

## Two rules about working in parallel

1. **One thread owns an episode at a time.** Pools, sheets and verdict files are all bound to
   file hashes; two threads touching the same episode produce verdicts that describe files
   that no longer exist. On 2026-08-25 a reviewer reported Singapore, Brooklyn and Moscow as
   "in the shipped master" — they were in sheets from a master replaced hours earlier.
2. **Only the publishing thread uploads or schedules.** A `publishAt` in the past publishes
   immediately.
