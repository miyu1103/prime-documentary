# 2026-08-21 — EP76 morandi: spec, ledger, bible, script (design session)

**State reached: `script_draft`, sized from a real measurement.** The left process for
`PD-2026-076-morandi` — the Morandi bridge collapse, Genoa, 14 August 2018 — is complete through the
script. Nothing has been generated, staged, rendered or spent beyond one ~$1 ElevenLabs measurement.

## What exists now

| artefact | path |
|---|---|
| machine contract | `episodes/PD-2026-076-morandi/episode_spec.v001.json` — `check_episode_spec.py --slug morandi` exits 0 |
| facts | `episodes/_planning/EP76_morandi_FACTS_LEDGER.v001.md` — 141 rows, 10 absences, 14 quarantine rules |
| design | `episodes/_planning/EP76_morandi_FILM_BIBLE.v001.md` — 14 sections, EP72 structure |
| script | `episodes/_planning/EP76_morandi_script.en.v001.md` — 328 chunks / 5,118 spoken words |
| narration registry | `scripts/gen_narration_case.py` — `PD-2026-076-morandi` added, `design_speech_seconds` 1669.0 |

## The two documents this film is built on were READ, not summarised

The handover for this episode warned that the load-bearing record is Italian and technical and that
an English secondary summary must not be narrated as the record. Both primary documents are scanned
image PDFs with **zero extractable text**; they were read by rendering the pages with PyMuPDF and
reading the images.

1. **MIT Commissione Ispettiva Ministeriale, *Relazione — crollo del Viadotto Polcevera*, Roma,
   14 September 2018** (5 PDFs, 225 pages, `mit.gov.it`). Pages read: **1–8, 21–31, 47–49, 53–54,
   59–60, 74–88**. This is the film's spine, and almost every VERBATIM row comes from it.
2. **Tribunale di Genova, dispositivo, RG NR 10468/18 — RG DIB 2037/22, 16 July 2026**, president
   Dott. Paolo Lepri (10 pages, obtained through Giurisprudenza Penale). **Read in full.**

The court-appointed experts' report of December 2020 — the document every English retelling quotes —
was **not** read. Every row from it is graded SECONDARY and is barred from carrying a beat (⛔-13,
⛔-14). Local copies of both PDFs and the rendered pages are in this session's scratchpad only; the
URLs are in the ledger's source table.

## The fact that changes this episode

**The first-instance verdict was delivered on 16 July 2026 — five weeks before this session.** Of 57
defendants, 32 were convicted and 25 acquitted or time-barred; Giovanni Castellucci was sentenced to
12 years; the written reasons were given a 90-day deadline and are not yet filed; an appeal was
announced. None of the seven incumbent long-form videos measured for this slot can contain it.

Three things in that judgment are legally load-bearing and are pinned in `forbidden_claims`:

- The court **excluded article 61 no. 3** — acting while foreseeing the event — **for every
  defendant**, and **acquitted all of them of articles 432 and 437 "perché il fatto non sussiste"**.
  The convictions are for negligence. The film may not say anyone knew.
- **Roberto Ferrazza was acquitted.** Any naming of him carries the acquittal in the same sentence.
- **Massimiliano Giacobbi, who signed the 2017 retrofitting project, died before judgment**
  ("estinzione dei reati a seguito di morte del reo").

## Pacing: measured, not modelled

`gen_narration_case.py --ep PD-2026-076-morandi --measure-section ACT_1` was run **before** the
script was written to length: 46 chunks / 650 words, ffprobed **211.906 s = 184.0 raw wpm** (173.0
words per finished minute). The script then extracts 328 chunks / 5,118 words →
**1,669.0 s speech + 108.6 s gaps = 1,777.6 s master → 1,786.6 s film (29:47)**, inside
`runtime_seconds` [1740, 1920] and `script_words` [4900, 5400].

The registry entry for EP76 carries 1669.0, not the 171.79 model.

## Instrument fixed: `check_script_length` no longer counts citation comments

`PD_ONE_PASS_PRODUCTION_SPEC.v3` §6.6 documented the defect and named the fix; it had not been
applied. On this script it read **5,872 words against 5,114 actually spoken — +758** — and reported
`FAIL … LONG by 392 words` on a 29:47 script. `scripts/check_script_length.py::count_words` now
strips `<!--.*?-->` before counting (first, because a comment can contain brackets).

Verified against the episodes named in §6.6 — the fix reproduces the documented deltas:

| script | before | after | §6.6 predicted |
|---|---|---|---|
| EP69 hyatt v001 | 7,294 | 5,053 | 5,099 |
| EP68 pinto v002 | 6,769 | 4,964 | 4,971 |
| EP71 oroville v001 | 6,237 | 4,924 | 4,981 |
| EP70 wronghouse v001 | 7,983 | 6,950 | 7,008 |

EP70 still FAILs a 29–32 min band, correctly: it is a 40-minute episode.

## Ledger discrepancies recorded rather than smoothed over

- **AB-06** — the primary record says **43 dead, 13 injured, ~243 m of deck**; widely republished
  secondary accounts say 11 injured and 250 m. The film uses the primary figures and does not
  mention the others.
- **AB-10** — SRC-0001 contradicts itself on the pier 11 works: §2.2 heads them "1992–1996", p.80
  calls them "93–97". The start year 1992 is corroborated by the cost table. **The script narrates
  the start year and anchors no arithmetic to an end year.**
- **AB-03** — the MIT commission and the court's experts disagree on the first cause, and the
  commission called its own account "plausible but not definitive". The film gives both and resolves
  neither.

## What is NOT done

1. **Image order (~120 plates), thumbnails, scene plan, `fact_recheck.v001`.** Not started.
2. **Footage staging.** `check_cross_episode_reuse.py` has not been run; `footage_review_required`
   is `true` and a labelled contact sheet must be opened by a person before any clip enters a cut.
   The shelf's labels are known to be wrong (`pd-factory-shelf-mislabeled`).
3. **Narration.** No full run. The dry run estimates **$8.86**; only the ACT_1 measurement was spent.
4. **`--measure-section HOOK`** to confirm the trimmed 67-word hook lands at 0:22.4.
5. **Nothing has been rendered.** `preflight_render_gate.py` must be green before any render — it
   has failed on 25 of 32 episodes and been overridden on 10, and on 2026-08-20 EP70 and EP71 were
   each one command from a three-hour render of a captionless slideshow.

## Codex image-order notes for whoever writes it

- Faces are allowed and wanted. Keep `human face`, `facial features`, `eye contact`, `headshot`,
  `profile of a face` OUT of `[NEG]`; keep `identifiable person`, `recognisable person`,
  `likeness of a real individual` IN.
- Codex output is capped at 1672×941. The proven route to 3840 is
  `scripts/upscale_oroville_4k_esrgan_v001.py` (Real-ESRGAN x4plus → LANCZOS to 3840×2160). Clone it
  per episode; a plain 2× enlargement does not clear the floor.
- The register is a working Mediterranean port city, not holiday Italy. `forbidden_subjects` bars
  Tuscany, vineyards, cypress avenues, Amalfi, gondolas, Venice canals, the Colosseum and Roman
  ruins, as well as US route shields, American highway signage, UK streets and right-hand-drive
  traffic. Italian lettering must be **present and unreadable**, never absent.
- **No generated plate may carry legible text that reads as a document, report, score sheet or
  judgment** (⛔-12). Every glyph that must be read is composited in Remotion over a blank ground.
