# Decision 0002 — First Channel: US Court-Case Documentary Format

- Status: Accepted
- Date: 2026-06-13
- Owner: Prime Documentary
- Relation to 0001: Concretizes 0001 for the **first operating channel**. Narrows the
  duration to ~12 min (0001 said 15–40 min; this is a deliberate format choice for this
  niche) and commits to one channel/niche while the production system stabilizes.

> This document is the handoff record between the cloud planning session and the local
> Claude Code session on the owner's Windows machine. Read this + `HANDOFF.md` + `CLAUDE.md`
> to resume work.

## 1. Business objective

- Goal: **monetize on YouTube** (revenue), targeting the **US** audience because CPM/RPM is high.
- Constraints: **minimize human labor**, **use AI tools heavily**, all videos in **English**.
- Channel already exists, is **US/English**, currently **unmonetized (zero)**; run it effectively
  as a new channel. Near-term KPI: reach **YPP threshold (1,000 subs + 4,000 watch hours)**.

## 2. Genre, series and risk posture

- Genre: **US court cases** ("裁判系"), English, US audience.
- Series concept / subscribe-promise: *"each video decodes one famous US court case that
  secretly shapes your life"* — the **"hidden system"** causal angle, not case re-telling.
- Risk posture: **start low-risk and ramp**. Open with **historical/landmark decided cases**
  (R1–R2): public-domain opinions, deceased/institutional parties, advertiser-friendly.
- Avoid initially: ongoing cases (sub judice), graphic true-crime, politically charged
  cases (e.g. abortion). These conflict with advertiser-friendliness and defamation safety.
- Editorial ethics (docs/32): distinguish charged vs convicted; never state allegations as
  fact; generated visuals are clearly **reconstruction/illustration**, never real footage.

## 3. First episode and initial batch

- **Episode 1 = Miranda v. Arizona (1966)** — "Why Do Police Have to Read You Your Rights?".
  Chosen for max search volume + familiarity + curiosity gap + full safety.
- Follow-on batch (broad → niche): **Gideon v. Wainwright**, **Mapp v. Ohio**,
  **United States v. Nixon**, **Loving v. Virginia**. A "famous rights / famous cases"
  cluster drives binge watch-time toward YPP.

## 4. Episode format template (~12 min, ~1,700–1,900 words @ ~150 wpm)

| Part | Time | Words | Content |
|---|---|---|---|
| Hook | 0:00–0:30 | ~75 | Pose the central question; tease the outcome (retention, docs/26). |
| Opening | 0:30–1:15 | ~110 | State the thesis + "what you'll learn" promise; light channel ID. |
| Main (chronological) | 1:15–10:30 | ~1,400 | 4 acts: ① event → ② trial → ③ ruling → ④ impact. |
| Ending | 10:30–12:00 | ~220 | "Hidden system" payoff + subscribe / next-episode CTA. |

- Main-act split (draft): event ~2:00 / trial ~2:30 / ruling ~2:00 / impact ~2:45.
- 12 min is intentional: 8 min+ enables multiple mid-roll ads (revenue).
- Maps to `pd-script` chapter structure.

## 5. Style and production spec

- Tone: **neutral, authoritative explainer** (trust + advertiser-safe).
- Narrator: **ElevenLabs**, middle-aged male, low, calm.
- Language: **American English, plain and clear** (broad reach, retention).
- Captions: **open captions** (burned-in, styled).
- On-screen citations: **burn in sources for major claims** (linked to `claim_id`).
- Visual look: **stylized / symbolic, avoid photoreal**. Hybrid: photo-symbolic stills
  (Midjourney) animated via parallax for "reconstruction" + diagram animation (SDXL) for
  the system explanation.
- **Motion = animation-first ($0)** in DaVinci/Fusion: 2.5D parallax, kinetic typography,
  animated diagrams/maps/timelines, cutout/collage motion, light/dust/grain overlays,
  mask reveals, match cuts. This is how we avoid a "slideshow" feel without paid render.
- **Runway: always used, but capped within the current monthly subscription** (no overage).
  Treat as a budget-gated resource (rules/11): per-episode Runway allowance ≈ monthly
  credits ÷ ~13 episodes; reserve it for a few hero shots per episode.
- Edit rhythm: **multi-layer, slightly fast pace**.
- Music: **Suno**, cinematic and restrained.
- Title: **question / curiosity-gap** form (high CTR, low misrepresentation).
- Thumbnail: **Canva**, symbolic visual + large short text, high contrast, no faces.
- Disclaimer (synthetic-media + legal): **short cold-open line + description**
  ("educational / dramatized reconstructions / not legal advice"), per docs/13, docs/32.

## 6. Cadence and throughput

- Target: **3 videos / week** (~13/month).
- Tension: 3/week vs "low labor" vs legal fact-check load. Resolution:
  - Low-risk landmark cases (lighter fact-check),
  - strong **automated QC** (claim grade + citation required) so the machine gates quality,
  - **batch pre-production + inventory** (build a buffer; batch the approval gate),
  - **build a reusable motion-template library first** (one-time investment → low marginal
    labor per episode).
- The human bottleneck is the **approval gate**, not generation. Keep it batched.

## 7. Tooling inventory (all paid / active)

| Stage | Tool | Billing | Integration |
|---|---|---|---|
| Image | Midjourney | subscription | ingested asset (no official commercial API) |
| Image/diagram | SDXL | local/credits | API/local adapter (Windows RTX 4090) |
| Video | Runway | subscription + credits | API adapter, budget-capped to monthly plan |
| Music | Suno | subscription | ingested asset |
| Narration | ElevenLabs | metered (chars) | API adapter |
| Edit | DaVinci Resolve | one-time | local + scripting (motion = $0 here) |
| Thumbnail | Canva | subscription | semi-manual export |
| Publish/analytics | YouTube | free | API adapter |
| Script/research | Claude + other LLM | metered (tokens) | API adapter, tiered routing (docs/24) |

- Provider terms/limits are time-sensitive → manage in a provider capability registry
  (docs/33) with `verified_at`. Do not hard-code.

## 8. Infrastructure (cross-machine: Windows + MacBook Pro)

- **Brain (A)** — topic/research/script/plans/manifest/QC (small JSON/MD): **GitHub repo**,
  cloned to each machine's **internal drive**. Versioned, off-site, auto-synced.
- **Heavy media (B)** — images/video/audio/DaVinci projects: **4TB external SSD**.
  - Format **exFAT** (Windows + macOS read/write). Eject safely (no journaling).
  - **Back up approved masters + final renders** (2nd drive or cloud) — a single SSD is a
    single point of failure (docs/34).
  - Reference media by **logical URI** (`artifact://episodes/.../...`) with a per-machine
    base-path → SSD-mount mapping. Never store `C:\...` / `/Volumes/...` as truth (rule 14).
  - **Do not put the git repo on the exFAT SSD** (permissions/case/perf). Repo on internal,
    media on SSD.
- Node roles (docs/25): **Windows = generation node** (SDXL/RTX 4090, ComfyUI) + SSD home;
  **MacBook Pro = mobile review/approval/script + driving Claude Code**. Heavy SDXL gen is
  Windows-bound; cloud tools (Midjourney/Runway/ElevenLabs/Suno/Canva) work from either.
- The owner now runs **Claude Code locally on Windows** so it can operate the real
  filesystem, the SSD, and local tools.

## 9. Build status

- Reference pipeline exists (deterministic stubs): `topic → … → qc_report` (see HANDOFF.md).
- **PR #1 (draft)**: minimal one-screen studio UI over `run_pipeline`
  (`src/pd_factory/studio.py`, `web.py`, `make ui`). Independent of channel content.

## 10. Open items / next actions for the local session

1. **Confirm the SSD**: `Get-Volume` → verify ~4TB and filesystem (reformat to exFAT now
   while empty if it is NTFS and Mac write access is wanted). Record the drive letter.
2. **Runway plan tier**: how many credits / generation-seconds per month? Needed to set the
   per-episode Runway budget number.
3. **Choose the cloud backup target** for approved masters (Drive / Dropbox / iCloud / 2nd drive).
4. **Scaffold episode**: create `episodes/PD-2026-001-miranda/` (00_topic brief + manifest),
   then begin **② real research adapter** (CourtListener / Oyez) to fill `01_research/` with
   real sources + a graded claim ledger (this is the first point real external input enters;
   isolate behind an adapter + preflight + idempotency + budget; treat fetched text as
   untrusted, rules/13).
5. Build the **reusable motion-template library** in DaVinci/Fusion before scaling to 3/week.

## Rationale

A single, low-risk, repeatable episode class (US landmark cases) lets us calibrate quality,
prove the research→citation→QC loop, and build the template/automation that makes 3/week
sustainable — while the cited-primary-source + original-system-angle approach is also the
defense against YouTube's mass-produced/inauthentic-content demonetization risk.

## Revisit conditions

- After the first batch (≈5 episodes) is published and QC-clean,
- once per-episode human review time and Runway cost are measured,
- before adding higher-risk case types or a second channel.

---

## Addendum — 2026-06-14 (tooling refinement)

- Status: Accepted. Owner decision during the first local Claude Code session.
- Effect: **supersedes the named items in §5 and §7 above** where they conflict. The
  format (§4), risk posture (§2), first episode (§3) and infrastructure (§8) are unchanged.

### A. Editing engine — Remotion + FFmpeg (supersedes the DaVinci motion text in §5/§7)

- The assembly edit is produced **as code**: **Remotion** for compositions/graphics/motion,
  **FFmpeg** for muxing/encode. **No DaVinci GUI hand-finishing.** DaVinci is optional and
  only for a final color/loudness pass if ever wanted.
- This makes docs/08's "deterministic assembly + rule-based motion + template graphics"
  literally a render pipeline, not a manual timeline. The motion-template library (§10.5) is
  therefore a **Remotion component library**, not a DaVinci/Fusion template set.

### B. Visuals — Midjourney (manual) + Remotion; **SDXL dropped** (supersedes §5/§7 image rows)

- **SDXL is not used.** Photo-symbolic stills come from **Midjourney**.
- Midjourney has no usable commercial API → **generation is manual (owner)**. Division of labor:
  **Claude writes the prompts**, and after the owner generates the 4-up, **Claude views the
  images and recommends the single best pick.** Selection criteria: composition, `--sref`
  consistency, no anatomical/structural breakage, scene-intent match, symbolic (must not read
  as authentic footage — invariant 11).
- **Brand look is unified across all episodes via Midjourney `--sref`.**
- **Use stills richly — do not ration them.** Budget **30–50+ Midjourney stills per episode**
  (cheap relative to retention value). To keep the manual-generation load sustainable, split
  into two pools: (a) a **reusable generic-motif library** (gavel, courtroom, document/scales,
  flag, jail bars, map textures, abstract "system" imagery, negative-space breathers) ingested
  once and reused across episodes, registered in **`library/visual/visual_registry.json`**
  (tags: motif, mood, `--sref`, orientation, `content_hash`, `rights_basis`, `verified_at`,
  reuse-tracking) — mirrors the music-library model; and (b) **episode-specific imagery**
  (the actual case: people-as-symbol, specific places/objects, the unique "hidden system"
  visual), where Claude concentrates prompt and selection effort. Claude writes all prompts and
  recommends picks for both pools; the owner only clicks generate.
- **Diagrams, maps, timelines, kinetic typography, lower-thirds (with burned-in citations
  linked to `claim_id`), chapter cards, parallax on stills, transitions, open captions** are
  all **rendered by Remotion** (code), not generated images.
- Hero video clips (a few per episode) remain **Runway** (API, budget-capped — paid, confirm).

### C. Audio — narration ElevenLabs; **music = reuse library** (supersedes §5 music / §7 Suno row)

- Narration: **ElevenLabs** (paid/metered — confirm before master generation), per docs/07
  draft-vs-master split.
- Music is **not generated per episode.** Build a **reusable library** with **Suno**:
  pre-generate **~50 tracks across 8 categories** — `hook`, `opening`, `explainer_bed`,
  `tension_build`, `somber`, `reveal`, `outro`, `ambience` — plus **15–20 short SFX**.
  **Claude writes the per-category briefs/prompts; owner generates in Suno and ingests.**
- Register every track in **`music_registry.json`** with tags (category, mood, BPM, energy,
  length, rights/licence, `suno_origin`, `verified_at`). Implement **automatic scene→track
  selection** that matches by tag **and avoids reuse within the most recent N episodes**.
- Music remains an **ingested asset** with rights metadata (not assumed programmatic; docs/07,
  rule on Suno-origin assets).

### D. Thumbnail — Remotion still component (supersedes §5 thumbnail / §7 Canva row)

- **Canva is dropped.** The thumbnail is a **Remotion still composition**: background = a
  **Midjourney still (or one frame pulled from video)**; **text, decoration and brand are
  drawn by Remotion**.
- **Auto-render multiple A/B variants** (title wording × layout) and present them for the
  owner to choose at the **title/thumbnail approval gate** (§ gates unchanged).

### E. Consequences to reconcile (tracked, not yet done)

- **Provider registry (docs/33):** update records — drop SDXL; add Remotion (local/free),
  FFmpeg (local/free), Midjourney (manual, no API), Suno (manual ingest, library model),
  Canva removed. Set `verified_at`.
- **Folder spec drift:** pipeline code uses `02_thesis/05_assets/06_audio/07_edit/08_qc`
  while docs/19 uses `02_story/05_visuals/06_voice/08_edit`. With Remotion-as-editor and no
  SDXL, fold this into one canonical layout in a follow-up (docs/19 + code + this episode).
