# DEEP RESEARCH — cross-session HANDOFF (v001, 2026-07-26)

Lets a FRESH session run **deep strategic/structural research** for Prime Documentary — the layer BEYOND packaging (thumbnails/titles/shorts, already done) and topic selection (a separate theme thread). This thread answers: *given our content already exists, why do viewers stay or leave, and what structural/craft/distribution changes would 10× retention + reach?*

Read the memory index first: `C:\Users\aab15\.claude\projects\C--Users-aab15-OneDrive-Desktop\memory\MEMORY.md`, especially `pd-analytics-2026-07`, `feedback-ctr-evidence-first`, `feedback-top-1-percent-not-average`, `pd-monetization-strategy`, `pd-ctr-refresh-20260725`, `reference-studio-video-ctr`. Repo: `C:\Users\aab15\Documents\prime-documentary` (git branch `claude/vibrant-archimedes-2mmr5h`). Channel: `UCuQPtAz1rca9eJ4xhvX0yKA` (AI-produced legal / true-crime / wrongful-conviction documentaries).

## GPU-FREE — safe anytime, zero conflict
This is pure read/analyze/write. It does NOT use the GPU (no SDXL, no render), so it runs fully in parallel with the main session's EP50/51/52 GPU builds and any other thread. Do NOT touch the EP50/51/52 build files. Do NOT schedule/publish. Do NOT redo the packaging or theme threads' work.

## WHAT WE ALREADY KNOW (don't re-derive; build ON it)
- **Bottleneck = CTR 1.58%** (target 4-6%). Packaging thread shipped: playbook `CTR_PLAYBOOK.v002.md` ("night-story frame": dark luma~45, silhouette/mid-size subject, one light source, outcome-concealed, 2-4 word hook with 1 red word, no badges/red-bars; big-face/bright LOSES), titles (declarative 6-10 words for long-form; em-dash/colon/question = losing signals), 19 long thumbnails + 17 titles + 42 short thumbnails refreshed live. Per-video CTR baseline captured (`scripts/yt_studio_video_ctr.py`, `scripts/_yt_studio_video_ctr.json`).
- **Retention ~21-26% AVP, trending up** (premium pivot works). Wrongful-conviction/exoneration = highest-retention cluster (~25%). Doctrine/law-explainer topics collapse (Swartz 4.0%, Wiretap 3.6%). Longer wins in-lane (median views peak 16-30 min; ≥1M-view channels ~24-min median). Subs come only from long-form. **Suggested video is the traffic engine.**
- Corpus: a 62,410-row in-lane study (merged_rows.json, lane_ids.json) built in a prior session's scratch (`.../scratchpad/ctr_study/`) — may need REBUILD via the collection scripts; derived findings are committed in `THUMBNAIL_PATTERN_RESEARCH.v001.md`, `CTR_GROWTH_REFERENCE.v001.md`.
- Studio cookie is LIVE: `secrets/studio_cookies.txt` (refreshed 2026-07-26). `scripts/yt_studio_ctr.py` (channel metrics, `yta_web/get_screen`) + `scripts/yt_studio_video_ctr.py` (per-video CTR, REACH tab) work via SAPISIDHASH auth. NOTE: if you get `OSError` writing the shared `_yt_studio_*.json`, that's a file lock from another session — write to your own filename.

## THE RESEARCH MISSION — prioritized questions (each must end in an ACTIONABLE rule for the build pipeline)
1. **★ RETENTION CURVES (highest value).** Pull our OWN per-video audience-retention graphs from Studio (the retention screen is a Studio-innertube endpoint NOT yet scripted — extend the yt_studio auth pattern to hit the audience-retention/`get_screen` for the retention tab; if the endpoint resists, capture what you can). For our top-5 and bottom-5 long-forms: WHERE exactly do viewers drop (first 30s? the OP after the hook? act transitions? specific dull stretches?), and what STRUCTURAL differences separate high- vs low-retention videos? → deliver concrete rules ("never X in the first 45s", "re-hook every N s", "cut any stretch longer than M s without a reveal").
2. **HOOK / FIRST 30 SECONDS.** Study 20-30 in-lane WINNER openings (top by views/day) frame-by-frame + first-line transcripts: cold-open vs branded intro, question vs statement, pace of first cuts, when the first face/stakes appear, how the open loop is set. → an OPENING FORMULA for our films (we just moved to cold-open for EP50 — validate/refine it with data).
3. **STRUCTURE & PACING.** For 20/30/60-min winners: act structure, re-hook cadence, WHERE the biggest reveal sits (we stack it last — confirm), chapter/timestamp usage and its retention effect, "reset" beats. → a STRUCTURAL TEMPLATE per runtime.
4. **NARRATIVE CRAFT.** What storytelling moves retain in true-crime/wrongful-conviction (open loops, teased-then-delayed reveals, villain framing, relatable-victim, emotional turn, second-person address)? Deconstruct 3-5 exemplar scripts/VOs. → a CRAFT CHECKLIST to gate every script against.
5. **DISTRIBUTION MECHANICS.** How is our traffic sourced (suggested/browse/search/external) per Studio? What specifically drives SUGGESTED (our engine) — packaging, session-time, topic adjacency? Session-time levers we don't use yet (end screens, cards, playlists/series, chapters). → a distribution/session-time action list.
6. **AUDIENCE.** Demographics (age/geo/device), returning vs new, comment-sentiment themes (what they praise/criticize) via Studio + public comments. → audience-fit notes for topic + tone.
7. **TOP-1% OUTLIER TEARDOWN.** Pick the 5-8 biggest outliers in the lane (views/day age-controlled) and reverse-engineer WHY (topic × packaging × structure × timing). Separate replicable levers from luck/scale. Aligns with [[feedback-top-1-percent-not-average]].
8. **FORMAT EXPERIMENTS to propose.** Evidence-based bets to A/B once measurable (chaptered long-form, multi-part series, a shorts→long funnel, an intro-hook variant). Each with a hypothesis + how to measure.

## METHOD
Evidence-FIRST ([[feedback-ctr-evidence-first]]): pull real data (our Studio analytics + in-lane winners) BEFORE concluding; study the extreme tail, not the median. Parallelize with subagents — one per question above — then a synthesis agent that reconciles + ranks by expected retention/reach lift and by how cheaply we can act on it. Cross-check any Studio-innertube claim against a second read. Flag confidence + caveats honestly.

## DELIVERABLES (write to episodes/_planning/)
- `DEEP_RESEARCH_FINDINGS.v001.md` — per question: the evidence, the finding, and a hard ACTIONABLE rule for the build pipeline (retention rules, opening formula, structure template per runtime, craft checklist, distribution/session-time action list, outlier teardown, format-experiment proposals). Rank all recommendations by expected impact × ease.
- New memory files for the durable rules (e.g. `pd-retention-rules`, `pd-opening-formula`, `pd-structure-template`) + MEMORY.md pointers, so the build pipeline can enforce them as gates ([[feedback-lessons-must-be-gates]]).
- If you build any new Studio-innertube reader (e.g. retention), commit it to `scripts/` with a docstring.

## COORDINATION (avoid overlap)
- Packaging thread = thumbnails/titles/shorts (DONE — don't redo; you may USE its CTR data).
- Theme thread = EP53-55 topic selection (don't pick topics — but your structure/craft findings feed their briefs).
- Main session = EP50/51/52 GPU builds (don't touch build files; your retention/opening/structure rules will be applied to those builds once delivered).
