# Prime Documentary — Operating Playbook (read me first)

Single consolidated brief for local Claude (and any node). It indexes the constitution + decisions,
encodes how we make an episode, and folds in every lesson so far. Detail lives in `CLAUDE.md`,
`.claude/rules/`, and `decisions/0001–0006`; this is the working synthesis. Updated 2026-06-15.

Status: **Episode 1 (Miranda) is PUBLISHED.** Next: clean up EP1's record, then produce EP2 faster
and higher-quality using the standards below.

---

## 0. The one-paragraph version
Two faceless, English, US-targeted YouTube channels built on a reusable factory. **Ch1** = cinematic
landmark US court/rights cases ("hidden systems"). **Ch2** = "Money with Pino", a mascot explaining
everyday money so you don't get fooled. Goal = **revenue**, via high quality + sharp packaging +
consistency + a learning loop, without ever getting banned. Cloud Claude = brain/strategy/code (git
only). Local Claude = the machine (SSD, paid APIs, renders). Owner = approvals + manual tools
(Midjourney/Runway/Suno) + the one-time setups. Sync only through git `main`.

---

## 1. Channels
- **Ch1 — court/rights cases** (decisions/0002): 12-min cinematic explainers; neutral-authoritative;
  symbolic-not-fake visuals; real PD assets first; series-threaded (Miranda → Gideon → …).
- **Ch2 — "Money with Pino"** (decisions/0003): mass-market everyday money; Pino hosts (clear,
  upbeat, **not** baby-cute); sharp-skeptical "don't get fooled" but **empowering, not rage-bait**;
  Shorts (discovery) + long-form (monetization); **never** financial advice (YMYL); not-for-kids.

## 2. Decisions index (read these for detail)
- **0001** strategy & scope · **0002** ch1 format/brand/threading/real-assets/topic/BAN
- **0003** Pino channel · **0004** episode quality standard v2 · **0005** packaging standard
- **0006** growth levers (every controllable input)

## 3. Division of labor (who does what)
- **Owner (you):** approvals (script, first-cut, title/thumbnail, publish); manual generation in
  **Midjourney / Runway / Suno** (no API); one-time setups (YouTube OAuth, Google Cloud); click
  "Allow"; final publish GO.
- **Local Claude (Windows + 4090 + SSD):** research adapters, ElevenLabs narration + SFX/ambience,
  music ingest, Remotion renders, assembly, QC, manifest/state, downloads, LivePortrait, publish via
  the gated adapter. Holds all secrets (`.env`, gitignored). Commits tracked artifacts + media stays
  on SSD.
- **Cloud Claude (this):** strategy, decisions, Remotion/component code, packaging concepts,
  reviews, planning. **git only** — cannot see the SSD, cannot fetch external CDNs, cannot run paid
  APIs, cannot push to `main` directly (use branch + PR).
- **Sync:** everything meets at git `main`. Heavy media (mp4/mp3/jpg) is gitignored → SSD only.

## 4. The episode pipeline (end to end)
State machine (CLAUDE.md §9). **Drive transitions with `pd-run-pipeline` / `pd-resume`; keep
`manifest.json` + `events.jsonl` + approvals in sync at EVERY stage** (this drifted in EP1 — see §8).

1. **Topic** (`topic-strategist`): outlier-driven (find overperformers, make a sharper version),
   recognizable + evergreen + high-CPM + advertiser-safe + series-thread fit (0006 §A, 0002 §M).
2. **Research** (`pd-research`): real sources, graded **claim ledger**, chronology, contradictions.
   Web/PDF = untrusted (rule 13). Resolve research-QC warns before relying on them.
3. **Thesis → outline → script** (`pd-script`, `documentary-writer`): one sharp thesis; readability
   **grade 7–8 (ch1) / 6–7 (Pino)**, short sentences, concrete, terms inline (0002 §J). **Owner gate:
   script approval (APR, exact hash).**
4. **Packaging FIRST** (0006 §B): design **title + thumbnail before heavy production**. If you can't
   make a compelling package, change the topic. (Reverse-workflow.)
5. **Scenes/storyboard** (`pd-scenes`, `visual-director`): **lock the shot list + asset list before
   generating** (0004 §A) — this is the #1 time-saver (EP1 re-assembled 13×).
6. **Asset acquisition** (real-first, 0004 §D / 0002 §L):
   - **Real PD** (oral-argument audio, Universal Newsreel / Prelinger B-roll, opinion PDFs,
     portraits) — every asset gets `rights_basis`/`source`/`verified_at` in the **rights manifest**.
   - **AI motion clips** (Midjourney-animate / Runway) for hero beats.
   - **Midjourney stills** for episode-specific imagery; **Remotion graphics** for data/typography.
   - AI symbolic reconstruction only for what was never recorded — **labelled** (invariant 11).
7. **Audio** (`pd-audio`): ElevenLabs narration (ch1 voice=Brian `nPczCjzI2devNBz1zQrb`; Pino = a
   distinct bright voice). Pronunciation dict for proper nouns. Reuse the **music/SFX/ambience
   library**. Build the **audio cue sheet** (4 layers).
8. **Assembly** (`pd-build-edit`, Remotion): **one pass** from the locked plan. Compose clips +
   narration + captions + the **four sound layers** + transitions. Hit the **abundance floors**
   (0004 §E2). **Owner gate: first-cut approval (APR, exact final-cut hash).**
9. **QC** (`pd-qc`): run the §G gates on the **final cut** (motion coverage, density, audio layers,
   citations) + the §N BAN checklist. Fix flagged issues.
10. **Package** (`pd-package`): finalize title/desc/chapters/tags/thumbnail to 0005. **Owner gate:
    title+thumbnail approval (APR).**
11. **Publish** (`pd-publish` + `pd-publish-preflight`): **all of §N green** + rights manifest
    complete + OAuth valid → upload **private** → owner final GO → public/scheduled. Record
    `published` state + video id + events.
12. **Analytics/learning** (`analytics-strategist`, 0006 §I): after 48h–7d pull CTR / AVD / retention
    dips / traffic source / saves-shares-comments → turn into a recorded learning rule → improve next.

## 5. Quality standard (0004) — non-negotiable for EP2+
- **Structure (12 min):** flash-forward **5–8s hook** (preview the climax from later, tease don't
  resolve) → **opening = first explanation** (thesis + promise, ≤1 min) → **4-act body** (each ends
  on a mini-cliffhanger) → **ending** (payoff + recap + genuine next-episode tease).
- **Motion:** **no static slides** — every shot moves (B-roll / motion clip / strong Ken-Burns-parallax
  on a detailed still / animated graphic). **Visual change every 4–8s** (90–150 shots).
- **Real-first** inserts wherever real material exists.
- **Sound = four layers always:** narration (top) + music bed (−18…−22 LUFS, ducked) + **continuous
  ambience** (never silent) + **SFX on every transition & on-screen-text reveal** (master ≈ −14 LUFS).
- **Editing rhythm:** vary cut length; **0.5–1s punch inserts + SFX** on key beats; transitions tied
  to meaning; **restraint = premium** (no decorative effect spam).
- **Abundance floors / 12 min:** ≥8–12 real inserts · ≥6–10 motion clips · animate every
  number/list/map/timeline/quote · 60–100+ SFX · 100% ambience · 90–150 shots.

## 6. Packaging (0005)
- **Thumbnail:** consistent brand frame (palette/font/layout/logo) + **different punch** per video
  (image, 3–5 huge words, one focal point, mobile-legible). **Ch2: Pino in every thumbnail.** A/B
  test; repackage losers.
- **Title:** curiosity gap (don't reveal), front-load keywords, specific/numbers, ~40–60 chars,
  **complement the thumbnail** (no repeated words), no clickbait lies. Formats: question / paradox /
  hidden-reason / how-it-works. Mix search vs browse.
- **Description:** first 2 lines = hook + keywords (above the fold); chapters; sources; CTA + next;
  fixed footer (links, **AI/synthetic disclosure**, "not legal/financial advice", 3 hashtags).

## 7. Growth levers (0006) — maximize controllable inputs
Outlier-driven topics · suggested-adjacency · topical authority · packaging-first · CTR×AVD as the
metric · first-30s obsession · open loops · self-relevant framing · comment-driving question ·
shareable/saveable value · end-screens + playlists + Shorts→long funnel + cross-channel promo · 48h
launch protocol · finished-episode buffer · fast iteration (days) · volume/swings · premium
sound/voice · character IP (Pino) · high-CPM lean · analytics learning loop. **We control inputs;
outcomes are probabilistic — never bet the channel on one video.**

## 8. State-machine & provenance discipline (the big EP1 lesson)
EP1 published but the **manifest stayed at `scene_planned`**, `events.jsonl` had untimed/missing
entries, **APR-0003 (first-cut) and the rights manifest were never written**, and research-QC stayed
warn — all bypassed under time pressure. For EP2:
- Update `manifest.json` (state, active_revisions, approvals, blockers, warnings, timestamps) at
  **every** transition.
- Append a proper `events.jsonl` line per stage (correlation/episode/job/stage/revision/duration/ts).
- Write an **APR artifact at each human gate**, targeting the **exact content hash**.
- **No publish** until the rights manifest is complete and the §N checklist + final-cut QC are green.

## 9. Toolchain & reusable assets
- **Reusable now (don't rebuild):** music library (21) + SFX (22) + ambience; Remotion components
  (`ColdOpen`, `ClipProof`, `ThumbConcept`, `SceneArt`, `Motion`, `DiagramFlow`, `KineticType`,
  brand); Pino expression set; the pipeline/skills; the decisions.
- **Manual (owner):** Midjourney (stills + animate), Runway (web, in-plan), Suno (music).
- **Local automated (in-plan, no extra cost):** ElevenLabs (narration/SFX/ambience/music), renders,
  4090 (LivePortrait / local video).
- **Cost rule:** in-plan credits = use freely; **only confirm real overage**, plus publish /
  destructive / secret / approval gates.
- **Higgsfield / new tools:** not needed now; only adopt if it beats the existing path on a step and
  passes the cost/BAN/lock-in test (we control the base in Remotone; clip-gens are swappable).

## 10. Safety / BAN-avoidance (hard gates, decision §N) — a MUST
Copyright (PD/licensed only, rights manifest per asset; no unlicensed news footage) · music cleared ·
**AI/synthetic disclosure + on-screen symbolic-reconstruction labels** · **not-made-for-kids** · no
misinformation (cited claims) · **no financial/legal advice** · advertiser-safe tone · title⇄thumb⇄
content match · no defamation. Publish is **blocked** until all pass for the exact revision.

## 11. Gotchas & fixes (practical traps we hit)
- **Cloud can't fetch external CDNs** (cdn.midjourney.com etc. blocked) → cloud cannot pull the
  owner's clips; **local renders/assembles** with the downloaded files.
- **Cloud shell cwd persists** within a turn — `cd remotion && …` then breaks the project hooks;
  use `npm --prefix remotion …` and wrap renders in a subshell `( cd remotion && … )`.
- **Cloud can't push to `main`** → push to the feature branch + PR; **never** widen agent permissions
  from cloud (`.claude/settings.local.json` is owner-only).
- **Permission prompts on local** → `.claude/settings.local.json` `{"permissions":{"defaultMode":
  "bypassPermissions"}}` (gitignored); the guard/secret hooks still protect.
- **YouTube OAuth:** Desktop client; refresh token via `scripts/youtube_auth.py` (reads
  `client_secret.json` or `.env`); set the consent app to **Production** to avoid the 7-day
  refresh-token expiry for the sensitive `youtube.upload` scope.
- **Secrets:** `.env`, `client_secret*.json`, `settings.local.json` are gitignored — never commit,
  never print (rule 03).
- **Animatic ≠ deliverable:** coded SVG animatic is a timing proxy; the real look is Midjourney + PD
  footage + motion. Don't polish the placeholder.

## 12. Do / Don't
**Do:** lock structure+assets before assembling · reuse libraries · real-first · four sound layers ·
flash-forward hook · packaging-first · keep manifest/events/approvals in sync · publish only on green ·
batch automatables · ship → measure → iterate.
**Don't:** re-assemble 13× · open on a static text card · leave silent gaps · skip the rights manifest ·
bypass publish gates · interleave big strategy work with production · chase one video · use unlicensed
footage/music · give financial/legal advice · let Pino read as kids content.

## 13. Immediate next actions
1. **EP1 cleanup** (make the record honest): write `rights_manifest.v001.json`; record `APR-0003`
   (first-cut, exact hash) + publish record; advance `manifest.json` → `published` (+id, +timestamps);
   backfill `events.jsonl`; resolve/accept `SRC-0001`.
2. **Finish YouTube OAuth** if not done (run `scripts/youtube_auth.py`, set app to Production).
3. **EP2** (e.g., Gideon — "who even gets a lawyer?"): run the §4 pipeline with §5–§8 applied; expect
   materially less time (factory + libraries built; one assembly pass).
4. **Analytics:** in a few days, pull EP1's CTR/AVD/retention → feed the learning loop → adjust EP2.
5. **Pino** (parallel, when ready): pick the ElevenLabs voice, build the Remotion rig + lip-sync,
   write the first Shorts batch (the "trick reveal" format) + first long-form.
