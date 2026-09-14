# NEXT-THEME SELECTION — cross-session HANDOFF (v001, 2026-07-26)

Lets a FRESH session pick the next Prime Documentary episode topics (EP53+) while the main session builds EP50/51/52. Read the memory index `C:\Users\aab15\.claude\projects\C--Users-aab15-OneDrive-Desktop\memory\MEMORY.md` first, especially: `pd-topic-novelty-gate`, `pd-analytics-2026-07`, `feedback-ctr-evidence-first`, `feedback-top-1-percent-not-average`, `pd-monetization-strategy`.

Repo: `C:\Users\aab15\Documents\prime-documentary` (git branch `claude/vibrant-archimedes-2mmr5h`).

## GOAL
Propose the next ~5-8 episode topics (EP53+), RANKED by evidence, each novelty-checked, with a one-line why + the story engine + suggested runtime. Optionally draft 3×-checked scripts for the top picks.

## HARD GATES (do not skip)
1. **NOVELTY GATE** ([[pd-topic-novelty-gate]]): before proposing ANY topic, grep the existing 45+ episode inventory to confirm it is NOT a dupe. Burned before (EP46=Kelo dup of EP10, EP47=Mahanoy dup of EP11). Inventory sources: `episodes/PD-2026-*/` dir names + `episodes/_planning/*` + any master ledger. List what you checked.
2. **EVIDENCE-FIRST** ([[feedback-ctr-evidence-first]]): don't guess what will do well. The Studio cookie is LIVE (`secrets/studio_cookies.txt`, refreshed 2026-07-26) — pull our own per-topic performance via `scripts/yt_studio_ctr.py` (note: the MAIN session may also run it — if you get an OSError writing `_yt_studio_ctr.json`, that's a file-lock from the other session, harmless; copy the pattern into your own output filename). Study in-lane winners.
3. **TOP 1%, not average** ([[feedback-top-1-percent-not-average]]): pick bold, outlier-potential topics, not safe median ones.

## WHAT THE DATA SAYS (from pd-analytics-2026-07 + this thread)
- **Wrongful-conviction / exoneration is the channel's HIGHEST-retention cluster** (~25% AVP; Hinton, and now EP48-52 all in this lane).
- **Longer wins in-lane** (median views peak 16-30 min; ≥1M-view channels run ~24-min median). 12/20/30/60-min all viable IF narrative-driven.
- **Narrative propulsion, NOT doctrine.** Person-suffering arcs with a villain + payoff-at-end retain; doctrine/law explainers collapse (Swartz 4.0%, Wiretap 3.6% AVP). A protagonist + open loop + re-hook ~75s + biggest reveal LAST.
- **CTR 1.58% is THE bottleneck** — favor topics with strong emotive-thumbnail + curiosity-gap potential.
- Living-persons / race-charged cases need care (silhouette thumbnails, no likeness — see EP50 lessons in [[feedback-thread-retro-20260725]]).

## STARTING MATERIAL (already in repo)
- `episodes/_planning/TOPIC_PIPELINE.v001.md` — 18 ranked novelty-checked topics. **Tier-S already USED: Willingham=EP51, Michael Morton=EP52.** Remaining Tier-S candidates: **Walter McMillian, Norfolk Four, Scottsboro Boys, Brown v. Mississippi** — plus the rest of the 18. Start here, re-novelty-check, then expand with new research.
- `episodes/_planning/CTR_GROWTH_REFERENCE.v001.md`, `CTR_PLAYBOOK.v001.md`, `THUMBNAIL_PATTERN_RESEARCH.v001.md`.
- Story-engine framework: wronged-innocent / relatable-victim / villain(real-killer or corrupt-official) / payoff-at-end. The best have a "the villain is punished" or "the real perpetrator revealed" turn (Morton = both).

## DELIVERABLE
Write `episodes/_planning/TOPIC_PIPELINE.v002.md` (or NEXT_THEMES.v001.md): EP53+ candidates ranked, each with: title-angle, one-line hook, story engines, suggested runtime, novelty-check result (what it's NOT a dupe of), thumbnail-CTR angle, and a confidence/evidence note. Flag any living-persons sensitivity. Parallel agents can each research + vet a batch of candidates, then synthesize a ranked list.

## CONSTRAINT
GPU-free work (research/writing only) — safe to run anytime, no conflict with the main session's GPU builds. Do NOT touch the EP50/51/52 build files. Do NOT schedule/publish anything.
