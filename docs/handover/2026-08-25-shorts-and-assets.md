# Handover 2026-08-25 — the shorts + assets lane

This lane is **asset gathering and Shorts**. Owner's direction this session, in order:
build the Shorts, then "素材のDL、とくに動画", then "画像よりも動画を大量に", then "再開して"
— which unfroze the Shorts and carried them from design all the way to rendered files.

Everything below is measured. Commands are inline.

---

## 1. State at handover

```
Shorts 289-309       21 designed, voiced, assembled, registered; RENDERING at handover
                     (bash scripts/render_shorts.sh, log runs/render_shorts_20260825b.log)
Shorts audio         21/21 mixes, measured 50.8-56.7 s, -14 LUFS
plates / depth       294 crops + 294 depth maps (torch lives in Python 3.10, not 3.11)
kinetic beats        42 AE overlays (VP9+alpha), render_beats.sh, all 21 shorts
gates                check_short_design 0 / check_short_constraints 0 / verify_short_designs 0
archive ingest       deep video run since 02:01, 195 items / 47.4 GB, still walking
shelf                ledger PASS after every mutation this session
```

Re-measure:

```
py -3.11 scripts/check_ledger_integrity.py
py -3.11 scripts/check_short_constraints.py episodes/_planning/short_designs/PD-2026-07*.json
py -3.11 scripts/verify_short_designs.py | grep -E "short(289|29[0-9]|30[0-9])"
grep -E "RENDER_DONE|DID NOT PRODUCE" runs/render_shorts_20260825b.log
```

## 2. Seven defects, and the one habit that found all of them

Every one was found by measuring the artefact, never by reading a green line.

| what was wrong | how it presented | how it was found |
|---|---|---|
| music cue named `_v1`, library holds `_v2` | all 21 mixes failed with ffmpeg status `4294967294` — an opaque -2 with no filename | listed the library |
| narration reused on FILE EXISTENCE | two trim passes rewrote text, index and every gate output; **the audio never changed** | durations byte-identical after a "rebuild" |
| word band as a length proxy | 8 Shorts sat inside 159-180 words and rendered 58.7-69.7 s | measured the mix; spoken figures run 0.4-0.8 s/word |
| `depth: true` with no depth maps | three.js `Could not load`, render dead | compared against short282, which had 10 |
| CTA card never drawn | the last two seconds were just a plate | **opened the finished mp4 and looked at it** |
| `destination.title = null` | `len(None)` stack trace inside assemble | ran it |
| plate dir curated by another thread | 11 staged plates read as "not on disk" although their bytes were untouched | `ls` on the siblings |

**The CTA one is the important one.** `assemble_short` flags the funnel cut only on a plate
whose role is `loop`; these designs said `close`, so no card. Then: **short280 and short282,
already published, carry `isCta: 0` too.** This is not a regression in this batch — the lane
stopped authoring the `loop` role at some point and the funnel card has been missing from
shipped Shorts. All 21 now draw FULL CASE + destination thumbnail + title + LINK BELOW,
verified on a real frame at 54.3 s of short289. **Worth checking the shipped back catalogue.**

Fixes are in `gen_newshort_narration.py` (idempotency key), `build_short_mix.py`
(`newest_take`), `check_short_constraints.py` (measures the mix, keeps the word band as the
pre-audio proxy), `assemble_short.py` (`destination_title`, `plate_dirs`),
`emit_short_lines_from_designs.py` (compares delivery, not only text).

## 3. Shorts: what is authored, and what it says

21 Shorts across seven episodes, three per episode, 8-line spine, 14 REUSE plates each.
Delivery arc normalised to the house form (first line intense, last calm, ≥3 building in the
middle) and claim ids cleared — `pd-verify` binds those, the design must not.

Editorial constraints that were read by hand against every line (the machine cannot):
itaewon names no victim and no official without their first-instance status; lahaina never
completes the siren counterfactual; morandi asserts no cause and names no defendant;
lacmegantic gives seven hand brakes against both the railway's nine and the investigation's
17-26; uri never says the grid collapsed and blames no fuel.

**Render is in flight at handover.** When it finishes: `coverfirst` runs per Short inside the
same script, then the 16:20 push takes over from 8/29 (four a day at 06/09/18/21 JST).

## 4. Assets: video only, and the two things that had to be blocked

Owner asked for volume in video and to stop spending on images. Both were done in code:
NASA is now `media_type=video`, and the ingest walks IA/NASA/coverr/mixkit only.

**pexels and pixabay video are exhausted** — 15,704 already on the shelf, and a 12-item
`anonymous_crowd` probe returned 1 new item and 11 dup-shas. The remaining seam is Internet
Archive: 195 items / 47.4 GB this run, 80-570 MB each, mostly mid-century public-domain
newsreel and government film. Under 360p goes to quarantine as `review_required` by the
technical floor, which is why roughly a third of the haul is not on the searchable shelf.

Two classes were blocked at the gate after arriving:

* **Franchise/conspiracy titles self-labelled `publicdomain`** — Sesame Street reached the
  shelf as `pd` because IA licences are uploader-set. 11 quarantined, `IA_TITLE_DENY` added.
* **Real-incident police body-worn and dash footage** — 20 items (Minneapolis body cam, Vegas
  shooting evidence, Cop City). A public-record licence does not make footage of identifiable
  private individuals safe to cut into a documentary. Quarantined, then denied at the gate.

Also this session: **32 of 59 quarantined video candidates restored** after a labelled contact
sheet was read tile by tile (54 % usable, matching the gate's estimate), via the new
`restore_from_quarantine.py`; deny round 4 written from the 27 rejects.

## 5. Traps that cost real time here

* `--cap-gb` is a **cumulative** cap against the whole 1.4 TB archive, not a per-run download
  cap. Any value below the archive total stops the run at pass 1 with 0 items.
* `remotion/public` is **377 GB**, and a hand-run `npx remotion render` copies all of it.
  Always go through `scripts/render_shorts.sh`, which bundles from the pruned `public_min`.
* The ledger's `fetched_at` is **UTC**. Counting "today's" items in JST reads 0 and looks like
  a dead lane.
* `subprocess(..., text=True)` on Windows decodes as cp932 and the reader thread dies on
  non-ASCII ffprobe output — a good probe becomes an empty result and a false reject.
* Root.tsx had **no entries past short282**, so the previous session's six Shorts were
  unrenderable as well. 21 registrations added; `tsc --noEmit` clean.

## 6. My own mistake, recorded

One commit used `git add -A scripts/` and swept in **203 files** of another thread's
uncommitted work under this lane's message. Nothing was altered or lost, but the lanes are
mixed in history. Commit explicit paths.

## 7. Token audit (rule 20)

`token_audit.py --live` at handover: 680 API calls, average context 306,978, peak 481,998,
billed 209M. Above the 300k CRIT line — **the next session should start at the render/QC
step, not continue this one.**
