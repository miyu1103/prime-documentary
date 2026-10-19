# BACKCATALOGUE REMASTER PLAN — 7 scheduled episodes (v001)

**Purpose:** stage the premium re-master (63° scanline + haze removal) of the 7
still-SCHEDULED/private Prime Documentary episodes so the GPU batch runs instantly
once the GPU frees from EP50. **STAGING ONLY** — this document plans; it renders,
deletes, uploads, and schedules NOTHING.

Author: staging pass 2026-07-25. Repo: `C:\Users\aab15\Documents\prime-documentary`.

---

## THE FIX (shared, already committed — confirmed inherited by all 7)

`remotion/src/compositions/CaseFilm.tsx` (EP49 fix, owner 2026-07-24):
- `BodyGrade` screen-wash opacity **0.18 → 0.07** (line ~490) — kills the milky haze.
- `DriftLight` **63° white repeating-linear-gradient scanline REMOVED** (lines ~341–360),
  replaced with a subtle non-scanline film texture; grade modes are now `bleed` / `depth`.

Because `CaseFilm.tsx` is the **single shared component**, simply RE-RENDERING each
episode's composition on the current code inherits the fix. **No asset regeneration.**

**Composition → component wiring (verified in `remotion/src/Root.tsx`):**

| Ep | Comp id | Component | Data source | Inherits fix? |
|----|---------|-----------|-------------|---------------|
| 41 thompson | `Ep41Thompson` | `CaseFilm` (defaultProps) | `src/data/thompson_film.json` | ✅ direct |
| 42 young | `Ep42Young` | **`YoungFilm`** wrapper | `src/data/young_film.json` | ✅ — `YoungFilm.tsx` is a 17-line thin wrapper that renders `<CaseFilm data={youngFilm} …/>`; **NOT a fork**, no local grade |
| 43 caniglia | `Ep43Caniglia` | `CaseFilm` (defaultProps) | `src/data/caniglia_film.json` | ✅ direct |
| 44 tekoh | `Ep44Tekoh` | `CaseFilm` (defaultProps) | `src/data/tekoh_film.json` | ✅ direct |
| 45 cleveland | `Ep45Cleveland` | `CaseFilm` (defaultProps) | `src/data/cleveland_film.json` | ✅ direct |
| 46 tlo | `Ep46Tlo` | `CaseFilm` (defaultProps) | `src/data/tlo_film.json` | ✅ direct |
| 47 atwater | `Ep47Atwater` | `CaseFilm` (defaultProps) | `src/data/atwater_film.json` | ✅ direct |

**All 7 cleanly inherit the fix. No per-episode fork of the old grade exists.**

---

## GLOBAL TRAPS — read before running the batch (these are the real blockers)

The grade fix itself is GO on all 7. The blockers are all in the **package/upload**
layer, and every one of them must be handled per-episode or the schedule step fails
closed or silently re-publishes the OLD defective video.

### TRAP 1 — sha256 guard + APR binding (BLOCKS every schedule script)
Each `scripts/schedule_<slug>.py` hardcodes `EXPECTED_HASH` = the OLD render's sha256,
AND guard 3 additionally requires `APR-0001.json` `content_hash` == that same sha
("BLOCKED: APR sha does not match render sha (re-approval required for new video)").
A re-render produces a **new sha**, so BOTH checks fail. Per episode you must:
1. Recompute `sha256` of the new `_ae` file.
2. Update `EXPECTED_HASH` (and `VIDEO_FILE` path/version) in `schedule_<slug>.py`.
3. Update `episodes/PD-2026-0XX-<slug>/approvals/APR-0001.json` `content_hash` **and**
   `video_sha256` to the new sha, **re-approved by owner** (or mint APR-0002 and point
   the script at it). Guard also checks `decision=="approved"` + `decided_by=="owner"`.

### TRAP 2 — finalize-if-exists REUSE (silently re-publishes the OLD video)
`schedule_<slug>.py` pre-flight scans the channel's recent uploads for a title/slug
match; if a PRIVATE match exists it **FINALIZES that existing video** (thumb/schedule/
caption) instead of uploading the new file. The currently-scheduled defective videos
WILL match. Therefore the old scheduled video **MUST be deleted first**; only then does
the scan find nothing and perform a fresh upload of the fixed render.
**There is NO delete/unpublish script in `scripts/`** (only `replace_miranda_youtube_v004.py`
and `replace_short_thumbnail.py`, neither reusable). → Must write a small delete helper
(YouTube `videos.delete`, channel-allowlisted) OR delete each video by hand in Studio
before running its schedule script. Video IDs to delete are listed per-episode below.
Delete+reupload = **new video_id** (URL changes) — acceptable, these are private/0-view.

### TRAP 3 — `public_slim` must be rebuilt per episode
Renders use `--public-dir=public_slim` to dodge the 48 GB full-`public` copy. There is
**no committed slim-builder**; `public_slim/` currently holds only `glover/` + `strieff/`
(EP48/49, the last renders) plus shared `fonts/` + `banner_sunrise.png`. Before each
render, rebuild `public_slim/` to contain the target slug's referenced assets: copy
`remotion/public/<slug>/` (incl. any `*_depth.png` used by CaseFilm `depth` mode) into
`public_slim/<slug>/`, keeping the shared `fonts/` + `banner_sunrise.png`.

### TRAP 4 — tlo & atwater NumberTicker comma bug returns on re-render
The old finals carried a **separate overlay fix** (`TloTickerFix` value=1985,
`AtwaterTickerFix` value=2001, both `group:false`) region-composited over the year
figure, because `build_tlo_film.py` (numberticker 1985, line ~262) and
`build_atwater_film.py` (numberticker 2001, line ~246) emit the year **without
`group:false`** → the base render shows "1,985" / "2,001". A plain re-render REINTRODUCES
the comma bug, and **the ticker-fix overlay is NOT part of `composite_<slug>_hero.py`**
(those overlay only the AE hero cards) and has **no committed script**.
**Recommended permanent fix (do at staging, non-GPU):** add `"group": False` to the year
`numberticker` in `build_tlo_film.py` and `build_atwater_film.py`, re-run those build
scripts to regenerate `tlo_film.json` / `atwater_film.json`, so the base render prints
"1985"/"2001" natively and no overlay is needed. (Cross-check: `build_glover_film.py`
and `build_centralpark_film.py` already pass `group:False` on year tickers — same pattern.)
Alternative: re-render `TloTickerFix`/`AtwaterTickerFix` and re-apply the ffmpeg region
overlay after composite — but that path is unscripted; prefer the `group:false` rebuild.

### TRAP 5 — v002 thumbnail for the face-fix set (caniglia/cleveland/tlo/atwater)
`apply_thumbnails_v002.py` shows the text-on-face fix set = **caniglia, cleveland, tlo,
atwater**, and the fixed asset is **`thumbnail.face.v002.png`** (NOT `selected.v002`).
But every `schedule_<slug>.py` currently points `THUMB_FILE` → `thumbnail.selected.v001.png`.
For these 4, update `THUMB_FILE` → `09_package/thumbnail.face.v002.png` before scheduling,
else the re-upload uses the OLD v001 thumb. (thompson & young keep `thumbnail.selected.v001.png`.)
- caniglia: `thumbnail.face.v002.png` present (Jul 24 23:25). ✅
- cleveland/tlo/atwater: `thumbnail.face.v002.png` present (Jul 24 22:21). ✅
- Note: `apply_thumbnails_v002.py` itself targets the OLD video_ids and becomes moot after
  delete+reupload — the new upload's thumbnail is set by `schedule_<slug>.py`.

---

## STANDARD PER-EPISODE RECIPE (order of operations)

All GPU/heavy steps are the **render**; everything else is CPU/ffmpeg/API.

```
# 0. (once) confirm CaseFilm.tsx fix is in the tree (it is) + typecheck
cd remotion && npx tsc --noEmit

# 1. rebuild slim public for THIS slug  (TRAP 3)
#    copy remotion/public/<slug>/  ->  remotion/public_slim/<slug>/   (+ keep fonts/, banner_sunrise.png)

# 2. [tlo/atwater only] apply group:false ticker fix + rebuild json  (TRAP 4)
#    python scripts/build_tlo_film.py     /  python scripts/build_atwater_film.py

# 3. RENDER base film (GPU)  — rely on Root.tsx defaultProps
cd remotion && npx remotion render <CompId> <BASE_OUT>.mp4 --public-dir=public_slim --concurrency=4 --gl=angle
#    (settings baked by remotion.config: libx264 / crf16 / yuv420p / bt709 / aac320k)

# 4. BGM (Brian VO bed, ducked, -14 LUFS)
python scripts/build_<slug>_bgm_real.py <BASE_OUT>.mp4 <BGM_OUT>.mp4

# 5. AE hero composite -> new _ae final  (reuses existing AE hero-card renders; grade-independent)
python scripts/composite_<slug>_hero.py <BGM_OUT>.mp4 <AE_OUT>.mp4

# 6. sha256 the new _ae; update schedule_<slug>.py (VIDEO_FILE + EXPECTED_HASH)
#    + APR-0001.json (content_hash + video_sha256, owner re-approve)   (TRAP 1)
#    + [face-fix set] THUMB_FILE -> thumbnail.face.v002.png            (TRAP 5)

# 7. DELETE the old scheduled private video (Studio or delete helper)  (TRAP 2)

# 8. schedule (fresh upload at SAME publishAt)
py -3.11 scripts/schedule_<slug>.py --dry-run   # verify guards pass + no existing match
py -3.11 scripts/schedule_<slug>.py             # real
```

Base-render / final locations:
- **Local finals** (thompson, young, caniglia, tekoh, cleveland): base render → `remotion/out/<slug>.mp4`;
  finals live in `episodes/PD-2026-0XX-<slug>/08_edit/`.
- **External-SSD finals** (tlo, atwater): finals live on `H:/pd-media/episodes/.../07_render/`
  (H: confirmed mounted). Write BGM/composite outputs there.

---

## PER-EPISODE EXECUTION ORDER (by publishAt)

Version bump column = suggested new `_ae` version (don't clobber the approved-but-defective file).

### 1) thompson — publishAt `2026-07-26T03:00:00Z` (12:00 JST) — old vid `OkwHIpI7DkE`
- **Comp id:** `Ep41Thompson` (CaseFilm) → **GO** (inherits fix).
- **Render:** `npx remotion render Ep41Thompson out/thompson.mp4 --public-dir=public_slim --concurrency=4 --gl=angle`
- **BGM:** `python scripts/build_thompson_bgm.py <base> <bgm>` *(note: only `build_thompson_bgm.py` exists — NO `_bgm_real.py` variant; use this one)*
- **Composite:** `python scripts/composite_thompson_hero.py <bgm> <ae>`
- **New final:** `episodes/PD-2026-041-thompson/08_edit/thompson_final_bgm.v003_ae.mp4` (bump v002→v003)
- **schedule_thompson.py edits:** `VIDEO_FILE`→v003_ae; `EXPECTED_HASH`→new sha; APR-0001 (old sha `859ff726…`) re-approve to new sha.
- **Thumbnail:** keep `thumbnail.selected.v001.png` (not in face-fix set).
- **Delete first:** `OkwHIpI7DkE`.
- **FLAG:** BGM script name differs (`build_thompson_bgm.py`, no `_real`). Everything else GO.

### 2) young — publishAt `2026-07-27T03:00:00Z` — old vid `Enok7A7wGBA`
- **Comp id:** `Ep42Young` (`YoungFilm`→CaseFilm wrapper) → **GO** (inherits fix; not a fork).
- **Render:** `npx remotion render Ep42Young out/young.mp4 --public-dir=public_slim --concurrency=4 --gl=angle` (no `--props`; wrapper reads `young_film.json`).
- **BGM:** `python scripts/build_young_bgm_real.py <base> <bgm>`
- **Composite:** `python scripts/composite_young_hero.py <bgm> <ae>`
- **New final:** `.../08_edit/young_final_bgm.v004_ae.mp4` (bump v003→v004).
- **schedule_young.py edits:** `VIDEO_FILE`→v004_ae; `EXPECTED_HASH`→new sha (old `d55bf28d…`); APR-0001 re-approve.
- **Thumbnail:** keep `thumbnail.selected.v001.png`.
- **Delete first:** `Enok7A7wGBA`.
- **GO** (standard).

### 3) caniglia — publishAt `2026-07-28T03:00:00Z` — old vid `yRwxBfrOY5o`
- **Comp id:** `Ep43Caniglia` (CaseFilm) → **GO**.
- **Render:** `npx remotion render Ep43Caniglia out/caniglia.mp4 --public-dir=public_slim --concurrency=4 --gl=angle`
- **BGM:** `python scripts/build_caniglia_bgm_real.py <base> <bgm>`
- **Composite:** `python scripts/composite_caniglia_hero.py <bgm> <ae>`
- **New final:** `.../08_edit/caniglia_final_bgm.v002_ae.mp4` (bump v001→v002).
- **schedule_caniglia.py edits:** `VIDEO_FILE`→v002_ae; `EXPECTED_HASH`→new sha (old `613a0222…`); APR-0001 re-approve;
  **THUMB_FILE → `thumbnail.face.v002.png`** (face-fix set).
- **Delete first:** `yRwxBfrOY5o`.
- **FLAG:** face-fix thumb swap required (asset present ✅). Otherwise GO.

### 4) tekoh — publishAt `2026-07-29T03:00:00Z` — old vid `GGW1SIAAgkY`
- **Comp id:** `Ep44Tekoh` (CaseFilm) → **GO**.
- **Render:** `npx remotion render Ep44Tekoh out/tekoh.mp4 --public-dir=public_slim --concurrency=4 --gl=angle`
- **BGM:** `python scripts/build_tekoh_bgm_real.py <base> <bgm>`
- **Composite:** `python scripts/composite_tekoh_hero.py <bgm> <ae>`
- **New final:** `.../08_edit/tekoh_final_bgm.v004_ae.mp4` (bump v003→v004).
- **schedule_tekoh.py edits:** `VIDEO_FILE`→v004_ae; `EXPECTED_HASH`→new sha (old `e0a66aba…`); APR-0001 re-approve.
- **Thumbnail:** keep `thumbnail.selected.v001.png` (NOT in face-fix set).
- **Delete first:** `GGW1SIAAgkY`.
- **GO** (standard).

### 5) cleveland — publishAt `2026-07-30T03:00:00Z` — old vid `AxOlQ2NIaBU`
- **Comp id:** `Ep45Cleveland` (CaseFilm) → **GO**.
- **Render:** `npx remotion render Ep45Cleveland out/cleveland.mp4 --public-dir=public_slim --concurrency=4 --gl=angle`
- **BGM:** `python scripts/build_cleveland_bgm_real.py <base> <bgm>`
- **Composite:** `python scripts/composite_cleveland_hero.py <bgm> <ae>`
- **New final:** `.../08_edit/cleveland_final_bgm.v003_ae.mp4` (bump v002→v003).
- **schedule_cleveland.py edits:** `VIDEO_FILE`→v003_ae; `EXPECTED_HASH`→new sha (old `a13e0367…`); APR-0001 re-approve;
  **THUMB_FILE → `thumbnail.face.v002.png`** (face-fix set).
- **Delete first:** `AxOlQ2NIaBU`.
- **FLAG:** face-fix thumb swap required (asset present ✅). Otherwise GO.

### 6) tlo — publishAt `2026-08-14T03:00:00Z` — old vid `hC5KE6IqmhM`
- **Comp id:** `Ep46Tlo` (CaseFilm) → **GO on grade**, but see ticker flag.
- **PRE-STEP (TRAP 4):** add `"group": False` to the 1985 numberticker in `build_tlo_film.py`
  (line ~262) → `python scripts/build_tlo_film.py` to regenerate `tlo_film.json`.
- **Render:** `npx remotion render Ep46Tlo <H:/…/tlo.mp4> --public-dir=public_slim --concurrency=4 --gl=angle`
- **BGM:** `python scripts/build_tlo_bgm_real.py <base> <bgm>`
- **Composite:** `python scripts/composite_tlo_hero.py <bgm> <ae>`
- **New final:** `H:/pd-media/episodes/PD-2026-046-tlo/07_render/tlo_final_bgm.v003_ae.mp4` (bump v002→v003).
- **schedule_tlo.py edits:** `VIDEO_FILE`→H: v003_ae; `EXPECTED_HASH`→new sha (old `2c8db4eb…`); APR-0001 re-approve;
  **THUMB_FILE → `thumbnail.face.v002.png`** (face-fix set).
- **Delete first:** `hC5KE6IqmhM`.
- **FLAG:** (a) NumberTicker "1,985" comma bug will return unless `group:false` rebuild done (TRAP 4);
  (b) face-fix thumb swap; (c) final on external SSD H:. Not a plain re-render.

### 7) atwater — publishAt `2026-08-15T03:00:00Z` — old vid `i95peRcdtz4`
- **Comp id:** `Ep47Atwater` (CaseFilm) → **GO on grade**, but see ticker flag.
- **PRE-STEP (TRAP 4):** add `"group": False` to the 2001 numberticker in `build_atwater_film.py`
  (line ~246) → `python scripts/build_atwater_film.py` to regenerate `atwater_film.json`.
- **Render:** `npx remotion render Ep47Atwater <H:/…/atwater.mp4> --public-dir=public_slim --concurrency=4 --gl=angle`
- **BGM:** `python scripts/build_atwater_bgm_real.py <base> <bgm>`
- **Composite:** `python scripts/composite_atwater_hero.py <bgm> <ae>`
- **New final:** `H:/pd-media/episodes/PD-2026-047-atwater/07_render/atwater_final_bgm.v003_ae.mp4` (bump v002→v003).
- **schedule_atwater.py edits:** `VIDEO_FILE`→H: v003_ae; `EXPECTED_HASH`→new sha (old `84af9bb9…`); APR-0001 re-approve;
  **THUMB_FILE → `thumbnail.face.v002.png`** (face-fix set).
- **Delete first:** `i95peRcdtz4`.
- **FLAG:** (a) NumberTicker "2,001" comma bug will return unless `group:false` rebuild done (TRAP 4);
  (b) face-fix thumb swap; (c) final on external SSD H:; (d) `Ep47Atwater` defaultProps
  `title`/`subtitle` in Root.tsx are a **copy-paste of the T.L.O. text** ("A Teacher Searched
  Her Purse…") — the on-screen title card would be WRONG. Verify/fix the `Ep47Atwater`
  defaultProps title+subtitle before render (the scheduled YouTube title/meta is unaffected,
  but the burned-in card is). **BLOCKER until corrected.**

---

## STATUS SUMMARY

| # | Ep | publishAt (JST 12:00) | Comp id | Grade fix | Schedule script | Blockers |
|---|----|----|----|----|----|----|
| 1 | thompson | 07-26 | Ep41Thompson | ✅ | ✅ | BGM script is `_bgm` not `_bgm_real`; +TRAP 1/2/3 |
| 2 | young | 07-27 | Ep42Young | ✅ | ✅ | TRAP 1/2/3 only — GO |
| 3 | caniglia | 07-28 | Ep43Caniglia | ✅ | ✅ | face.v002 thumb swap; +TRAP 1/2/3 |
| 4 | tekoh | 07-29 | Ep44Tekoh | ✅ | ✅ | TRAP 1/2/3 only — GO |
| 5 | cleveland | 07-30 | Ep45Cleveland | ✅ | ✅ | face.v002 thumb swap; +TRAP 1/2/3 |
| 6 | tlo | 08-14 | Ep46Tlo | ✅ | ✅ | ticker group:false; face.v002; H: SSD; +TRAP 1/2/3 |
| 7 | atwater | 08-15 | Ep47Atwater | ✅ | ✅ | **Root defaultProps wrong title (BLOCKER)**; ticker group:false; face.v002; H: SSD; +TRAP 1/2/3 |

**Grade-fix inheritance: GO on all 7** — no old-grade fork; `YoungFilm` is a thin CaseFilm wrapper.
**All 7 have build_film + BGM + composite + schedule scripts, and existing finals + captions.**

### Cross-cutting blockers to resolve before the batch (apply to all 7 unless noted)
1. **Delete helper missing (TRAP 2)** — no channel `videos.delete` script exists; write one
   (allowlist `UCuQPtAz1rca9eJ4xhvX0yKA`) or delete each old video by hand in Studio. Without
   this, every schedule run re-finalizes the OLD defective video.
2. **sha/APR re-approval (TRAP 1)** — new render sha must be written into each
   `schedule_<slug>.py` `EXPECTED_HASH` + `VIDEO_FILE`, and into `APR-0001.json`
   (`content_hash`+`video_sha256`), owner-re-approved. Fails closed otherwise.
3. **public_slim rebuild per slug (TRAP 3)** — currently holds glover/strieff only.
4. **tlo & atwater ticker `group:false` rebuild (TRAP 4)** — else "1,985"/"2,001" returns.
5. **caniglia/cleveland/tlo/atwater `THUMB_FILE` → `thumbnail.face.v002.png` (TRAP 5).**
6. **atwater `Ep47Atwater` defaultProps title/subtitle are wrong (T.L.O. text)** — fix before render.

*Nothing in this plan has been executed. No render, delete, upload, or schedule was run.*
