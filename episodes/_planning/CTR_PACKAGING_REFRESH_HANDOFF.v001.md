# CTR PACKAGING REFRESH — cross-session HANDOFF (v001, 2026-07-25)

**Purpose:** this doc lets a FRESH session (with parallel subagents available) execute the "CTR packaging blitz" while the ORIGINAL session keeps doing the GPU-serial EP51/52 episode builds. Everything needed is here + in the auto-memory (`.claude/.../memory/*.md`). Read the memory index `MEMORY.md` first.

Repo: `C:\Users\aab15\Documents\prime-documentary` (git branch `claude/vibrant-archimedes-2mmr5h`). Media on `H:\pd-media`. Channel `UCuQPtAz1rca9eJ4xhvX0yKA`.

---
## WHY THIS WORKSTREAM (context)
Channel's #1 bottleneck = **CTR 1.58%** (target 4-6%; measured 2026-07-25 via live Studio cookie). Retention is fine (~21-26%). So packaging (thumbnails + shorts + the research behind them) is the highest-leverage work, it hits the LIVE catalogue immediately, and it's embarrassingly parallel (dozens of independent units) — ideal for parallel agents. The GPU-bound episode builds stay in the other session (one 4090 = GPU serializes; agents don't help there).

## THREE WORKSTREAMS

### 1. CTR RESEARCH  ← start here (GPU-FREE, zero conflict, most parallel)
- Studio cookie is LIVE: `secrets/studio_cookies.txt` (refreshed 2026-07-25). Auth pattern (SAPISIDHASH) + working reader = `scripts/yt_studio_ctr.py` (run `py -3.11 scripts/yt_studio_ctr.py`; writes `scripts/_yt_studio_ctr.json` + summary). Studio innertube client: CLIENT_NAME=62, CLIENT_VERSION in that file, SERIALIZED_DELEGATION there too. `creator/list_creator_videos` endpoint works (mask fields are scalar/`{"all":true}`) — use it to pull PER-VIDEO CTR now that the cookie is live (this was impossible before).
- Prior findings already in repo: `episodes/_planning/THUMBNAIL_PATTERN_RESEARCH.v001.md` (winners vs flops: faces help (+9pt) but MODERATE size ~15-21% not huge; eyes upper-third centerY~31%; DARK luma~62; RESTRAINED saturation~84; huge face-filling = FLOP signal), `CTR_PLAYBOOK.v001.md`, `CTR_GROWTH_REFERENCE.v001.md`.
- Corpus: the 62,410-row in-lane study (`merged_rows.json`, `lane_ids.json`, haarcascade) lived in a PRIOR session's scratch (`.../scratchpad/ctr_study/`) — may need REBUILD in the fresh session (re-pull via yt_studio + the collection scripts). The DERIVED findings above are already committed, so research can proceed on those + fresh own-CTR data.
- Parallel research angles (one agent each, then synthesize): (a) own per-video CTR ranking now the cookie is live — which of OUR thumbnails over/under-perform; (b) in-lane winner thumbnail composition re-run (bigger sample); (c) title n-gram analysis split by short vs long; (d) 5-8 competitor channel teardowns (packaging patterns); (e) retention-curve read of our own long-forms. Deliver a ranked, evidence-first packaging playbook update. Principle: [[feedback-ctr-evidence-first]] — study in-lane winners FIRST, never guess.

### 2. ALL-THUMBNAIL REFRESH (~75 public videos)
- **Data-driven spec** (from THUMBNAIL_PATTERN_RESEARCH): emotive subject PRESENT but MODERATE (~20-30% frame height, NOT a 55%+ face — huge face = flop); eyes on the upper third (centerY ~30-35%); DARK moody grade (luma ~60); RESTRAINED saturation (~84); 2-4 word hook in negative space, never over the face; PD logo bottom-right chip. 1280x720, <2MB.
- **★ SENSITIVITY RULE (hard, learned on EP50):** for race-charged or specific LIVING-person cases, DO NOT use a generated "emotive face" — it either misrepresents (e.g. a white face on the Central Park Five) or risks resembling the real living people. Use a **race-neutral SILHOUETTE / atmospheric hero** instead (still gets CTR via human presence + tension). EP50's shipped thumbnail `episodes/PD-2026-050-centralpark/09_package/thumbnail.v001.png` (hooded silhouette under an interrogation lamp, "5 CONFESSIONS / NO EVIDENCE") is the REFERENCE EXEMPLAR for this style. Judge each video: generic dramatized character OK → face; real/sensitive people → silhouette/atmospheric.
- **Tools:** face recipe (2-stage likeness firewall, JuggernautXL→DreamShaperXL illustrative) = `scripts/build_face_thumbnails_ep4447.py` (EPS dict; add per-slug entries; USE MODERATE face size, not the old 55-60%). Atmospheric/silhouette builder = `scripts/build_centralpark_thumb_atmos.py` (clone per episode; SDXL bg + text composite). Apply to YouTube = `scripts/apply_thumbnails_v002.py` (thumbnail.set is LIVE-SWAPPABLE, no re-upload).
- **Enumerate the ~75 public videos** via the Data API / Studio list (the fresh session pulls the list). Parallelize: agents own batches of ~10 videos each (plan the concept per video from its case → gen/composite → QC legibility at small size). GPU note below.

### 3. SHORTS REFRESH (through EP52)
- Owner rules: **all 60 seconds**; **remove dialogue/caption text** from thumbnails; more CTR-conscious (bolder, cleaner, emotive). Reference method = `episodes/_planning/SHORTS_METHOD.v001.md` + the kids-for-cash reference; existing shorts docs `SHORTS_EP*.md`, `SHORTS_PLAN.md`, `SHORTS_CONVERSION_v001.md`, `SHORTS_MOTION_DESIGN.md`.
- Tools: `scripts/build_shorts_hero_cards.py`, `scripts/replace_short_thumbnail.py`, `scripts/check_short_thumbs.py`, `scripts/build_shorts_thumb_mapping.py`. Shorts are mostly light-GPU compositing on EXISTING short videos → highly parallel across agents.
- Enumerate the scheduled + public shorts through EP52; refresh thumbnail (remove text, CTR layout) + confirm 60s runtime.

## HARD CONSTRAINTS (do not violate)
- **GPU coordination:** the ORIGINAL session is running SDXL/i2v/Remotine renders on the single 4090. NEVER run SDXL/render in this fresh session at the same time — VRAM exhaustion silently crashes one job (no output). RESEARCH (workstream 1) is GPU-free = always safe; do it first/continuously. For thumbnail SDXL gen, coordinate a GPU window with the owner, or prefer compositing over EXISTING images (many thumbnails can reuse already-generated episode stills — no new gen).
- **Live-channel writes:** thumbnail.set is low-risk (swaps only the image). But ANY status/schedule edit MUST preserve `publishAt` (a bulk status write without it UNSCHEDULES the video — burned before). Match videos by EXACT title + EXCLUDE `#Shorts` (loose matching once hijacked a short). Get owner OK before MASS-applying thumbnails to live videos.
- **Money/publish boundary:** do not publish/schedule/spend without owner approval (APR-0001 pattern). Thumbnail swaps on already-public videos: confirm the batch with the owner first, then apply.
- **Verify, don't assume:** eyeball every generated thumbnail at SMALL size (it must read as a mobile-feed thumbnail); size-audit any asset before trusting it ([[feedback-codex-codexb-unreliable]] — Codex/imagegen produces black stubs; check file size / luma).

## CURRENT STATE (what's done / not)
- CTR packaging execution: **NOT STARTED** (0 thumbnails refreshed, 0 shorts refreshed this cycle). Groundwork EXISTS: research findings + specs committed, EP50 silhouette exemplar shipped, cookie live.
- Meanwhile the OTHER session is: finishing EP52 (factory stock-selection is stubbed — 227/240 black; being fixed) → build → render; then EP51; EP50 awaiting owner playback → schedule. Do NOT touch EP50-52 episode builds from this fresh session (avoid collision).
- All status + lessons: memory files `pd-analytics-2026-07`, `feedback-ctr-evidence-first`, `feedback-top-1-percent-not-average`, `pd-ep50/51/52-status`, `feedback-thread-retro-20260725`, `THUMBNAIL_PATTERN_RESEARCH.v001.md`.

## SUGGESTED ORDER (fresh session)
1. Research burst (parallel agents, GPU-free) → refreshed packaging playbook + own-CTR ranking of worst-performing thumbnails (prioritize which to redo first).
2. Thumbnail refresh, worst-CTR-first, batches of ~10 per agent (reuse existing stills where possible; coordinate any SDXL gen against the other session's GPU use). Get owner sign-off before applying live.
3. Shorts refresh through EP52 (light-GPU compositing, parallel).
