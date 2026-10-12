# Archive rebuild — brief for the ingest thread

Written 2026-08-20 by the session that found the loss. **Read all of §1 and §2 before running
anything.** This is a separate lane from the publishing/episode thread; the boundaries in §2
are not advice.

---

## 1. What happened, in one paragraph

The plain Samsung T7 that held `H:\pd-media` failed its **USB interface** — proven by
swapping only the drive in a port and cable that the T7 Shield then used successfully, twice.
It draws bus power (the LED lights) and never enumerates. The T7 encrypts in its controller,
so chip-off recovery is not realistically available. It took with it `_ledger` (39,092
licensed videos), the files behind all 88,850 entries of `assets/asset_manifest.v001.json`,
every past episode's AI plates / i2v masters / narration masters, and EP71's full-size plates.
**The catalogue survived in the repo; the files did not.**

## 2. Boundaries — do not cross these

1. **Do not touch publishing.** No uploads, no scheduling, no `upload_schedule_case_v001.py`,
   no thumbnails, no comments. Exactly one session operates the calendar and it is not this
   one. EP66/67/68 are booked for 08-20/21/22 and EP69 re-uploads after 16:00 local on 08-20.
2. **Do not run renders or i2v.** The GPU takes one job. If a render is running, ingest is
   still fine (it is network and disk only) — but never start one from this lane.
3. **Do not delete anything on D:, E: or F:.** The surviving shelf is all that is left.
4. **`C:\Users\aab15\.codex\generated_images` and `.codex\sessions` are NOT junk.** 12,095
   PNGs and their session transcripts are the only surviving copy of some past episodes'
   Codex plates — EP71's 118 were recovered from exactly there on 08-19. Never clean them.
5. **Never convert `review_required` to approved** to make a count look better. An unknown
   licence stays unknown (`.claude/rules/media-truth-license.md`).

## 3. Step 0 — REINDEX FIRST. Do not skip this.

The new ledger is empty, so the ingest believes it owns nothing and will re-download the
13,875 videos and 8,635 audio files it is standing on.

```
py -3.11 scripts/reindex_archive_shelf.py --dry-run --limit 400 --no-hash   # look
py -3.11 scripts/reindex_archive_shelf.py                                   # real run
```

The real run hashes ~884 GB and is the slow part (allow a few hours; it is resumable, and an
interrupted run costs nothing because rows already written are skipped by `(source, id)`).
`--no-hash` is available and much faster, but it loses content-level dedup and every row it
writes says so.

**About renaming: none is needed and none is possible.** Files the ingest wrote are already
`<source>__<id>__<slug>.<ext>`, which is exactly what the reindexer parses — 45k of them.
The remaining **10,262 videos carry no source prefix**, and with the ledger gone nothing
identifies where they came from, so they cannot be renamed into attribution. They are indexed
into `unattributed.jsonl` as `review_required` and **must not enter a cut**. Recording them is
only so the ingest does not re-download duplicates of them.

## 4. Step 1 — download

Storage was repointed on 2026-08-20: tiers are now **E → D → F** (H is removed) and the ledger
lives at `E:\pd-archive\_ledger`. Free space at handover: E 1,082 GB, D 648 GB, F 511 GB.

```
py -3.11 scripts/ingest_archive_sources.py --help          # sources and themes
py -3.11 scripts/ingest_archive_sources.py --source nasa --theme space_nasa --limit 2 --passes 1 --dry-run
py -3.11 scripts/ingest_modern_web.py --help               # pixabay / pexels / mixkit / coverr
```

Two lanes exist and they write the same ledger directory:

- `ingest_archive_sources.py` — ia, loc, nara, met, nasa, wikimedia, noaa, nypl,
  smithsonian, freesound, mixkit, coverr, pixabay, unsplash. Keyless or free keys, all present
  in `.env` (`PEXELS_API_KEY`, `PIXABAY_API_KEY`, `OPENVERSE_*` verified present 08-20).
- `ingest_modern_web.py` — the modern-stock lane; this is what produced the 88,850 that were
  lost.

**Run ONE lane at a time.** They append to shared JSONL ledgers, and concurrent lanes have
torn lines before (the code comments say so at `atomic_append`).

Start small, verify, then widen. Use `--cap-gb` to bound a run.

## 5. What to rebuild, and in what order

`assets/asset_manifest.v001.json` is still in the repo and is the **shopping list** — it
records what the lost shelf held, by type and subtype:

```
88,850 entries    image 73,167 / video 15,683
source            pixabay 53,729 / pexels 34,795 / sdxl 216 / local_a1111 110
type              backgrounds 64,264 / light_assets 7,428 / particle_assets 6,564
                  vfx_overlays 6,229 / texture_assets 3,911 / loops 454
subtype           ~300 items each, e.g. american_flag_waving 334,
                  hydro_dam_water_release 334, front_door_house 328,
                  courthouse_steps 313, long_shadow_of_a_person 313
```

Priority order, because two episodes are blocked on it:

1. **What EP70 wronghouse needs** — Atlanta / Georgia / suburban house exteriors / federal
   courthouse / 1973 period, 1973–2026. `episodes/PD-2026-070-wronghouse/episode_spec.v001.json`
   carries `era_setting` and `forbidden_subjects`; read both before writing queries.
2. **What EP71 oroville needs** — Northern California valley, Feather River, spillway,
   evacuation shelter, cattle, 2005–2023, contemporary. Its spec declares
   `distinct_video_assets: 260`. **Its `forbidden_subjects` bars flood/breach/collapse/rescue
   imagery — a query that asks for those fails the build** (EP60 staged 31 such clips before a
   human noticed, which is why the constraint is now machine-readable).
3. General backgrounds/textures to restore the everyday shelf.

**Neither episode has a `FOOTAGE_PLAN` or an entry in
`config/episode_footage_queries.v001.json`.** Both are required before
`prestage_footage_review.py` will run at all — it exits with `no query set for <slug>`. See
`episodes/_planning/EP69_hyatt_FOOTAGE_PLAN.v001.md` for the form: every query term is one the
plan measured a usable count for on the shelf, terms measured as misleading are listed and
excluded with their counts, and **no query term may be a `forbidden_subjects` word**, because
`check_spec_satisfied` matches those against staged filenames.

## 6. Audio does NOT need rebuilding

The 08-19 handover says the audio library is gone. That was measured against the *curated*
`library/sfx` and `library/ambience` (22 + 10 files). **The raw shelf survives on D:** —
8,635 Freesound files, 23.4 GB:

| | files |
|---|---|
| `D:\pd-archive\sfx_environment` | 2,819 |
| `D:\pd-archive\sfx_human_movement` | 2,739 |
| `D:\pd-archive\sfx_mechanical` | 1,629 |
| `D:\pd-archive\ambience_beds` | 1,067 |
| `D:\pd-archive\bgm_general` | 381 |

Every one is `freesound__<id>__…`, so the original Freesound id is recoverable per file — and
it needs to be, because **Freesound licences are per-item** (CC0 / CC-BY / CC-BY-NC), which is
why the reindexer marks them `review_required` rather than clearing them. The seven Suno music
tracks are separately safe in `library/music/music_registry.v001.json` with prompts and hashes.

## 7. Verify, then report

```
py -3.11 scripts/build_archive_inventory.py     # what the shelf can supply, by SUBJECT
py -3.11 -c "import sys; sys.path.insert(0,'scripts'); from shelf import shelf_rows; print(sum(1 for _ in shelf_rows()))"
```

`shelf.py` still hard-codes `H:\pd-media\assets\archive\_ledger` at line 30 and will report
`shelf 0 items` until it is repointed to `E:\pd-archive\_ledger`. **Fix it through
`scripts/pd_edit.py`** (it proves the text landed and reverts on failure) and re-run the line
above to show a non-zero count before believing anything downstream.

A theme's hit count is not a supply count — EP71's own spec measured 1,293 candidate clips and
a 70-clip sample judged **50% off-register**. Before reporting a theme as restocked, build a
labelled contact sheet and look at it. The shelf's labels were measured 40% wrong once already
(`FACTORY_LABEL_AUDIT.v001`), and that is with a ledger; without one it is worse.

## 8. Done looks like

- `reindex_archive_shelf.py` has run and `shelf_rows()` returns a non-zero count.
- `ingest` has been run for the EP70 and EP71 registers, with a `--cap-gb` you chose.
- `FOOTAGE_PLAN` documents and `episode_footage_queries.v001.json` entries exist for
  `wronghouse` and `oroville`, with every term measured and no forbidden word among them.
- `prestage_footage_review.py --slug wronghouse --dry-run` runs instead of refusing.
- You looked at a contact sheet and can say what the shelf actually holds.

Write what you found to `docs/handover/YYYY-MM-DD.md` before the session ends. A handover that
only exists in a chat log does not exist.
