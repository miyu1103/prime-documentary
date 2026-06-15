# 0007 — Quality-up, owner-effort-neutral automation levers

Status: **accepted** (owner direction 2026-06-15). Both channels. Goal: **raise quality to the max
while NOT increasing the owner's manual workload.** Everything here is done by the system (local 4090,
local automation, cloud agents) — not by the owner. Owner stays on the four human gates + the few
manual generators (Midjourney/Runway/Suno) + one-time setups. Binds `automation-architect`,
`visual-director`, `edit-engineer`, `audio-director`, the review/QC agents, and the local node.

## A. Use the RTX 4090 fully (free, local, automated)
- **Auto 2.5D parallax from depth maps:** run a depth estimator (e.g. MiDaS/Depth-Anything) on every
  still → drive layered parallax in Remotion automatically. Big motion gain, zero owner effort.
- **Frame interpolation (RIFE/FILM):** smooth AI clips / make clean slow-mo / raise effective fps.
- **Auto upscale + denoise:** clean low-res PD newsreel + AI stills to a crisp, uniform quality.
- **Local bulk generation (SDXL / SVD / AnimateDiff):** generate many variants for free → auto-select
  (reduces reliance on manual Midjourney and on owner curation).
- **LivePortrait / lip-sync:** make Pino (and any face) talk automatically — no owner effort.

## B. Automated finishing passes (uniform premium look, zero owner effort)
- **Brand color-grade LUT** applied to every shot → consistent look across mixed sources.
- **Auto grain / vignette / light** pass for a filmic, cohesive feel.
- **Audio auto-mastering** (EQ, de-ess, compression, **−14 LUFS** normalize) + **auto-ducking** of
  music/ambience under VO.
- **Caption auto-sync** from TTS timestamps (word-for-word, frame-accurate) — already standard (0004 §E3).

## C. AI self-review BEFORE the owner sees it (higher quality, *less* owner review)
- Run `fact-checker`, `retention-engineer`, `editorial-chief`, `rights-editor` **automatically** on
  the draft; fix issues; only a polished cut reaches the owner → owner reviews less, quality higher.
- **Automated first-30s / pacing / dead-spot critique** before final render.
- **QC gates** (0004 §G, §N) auto-block defects without owner involvement.

## D. Smarter sourcing (cuts the owner's manual generation)
- **Auto-batch-download PD real footage** (Universal Newsreel / Prelinger) and **PD images**
  (Wikimedia Commons, NASA, gov archives) with rights capture → more real footage, *fewer* manual
  Midjourney generations.
- **Cloud pre-writes the full prompt list** so any manual generation is bulk paste, minimal thinking.

## E. Templates & growing reuse (consistency, speed, no fiddling)
- **Templated assembly** (numbers/assets swap in) so the owner never hand-edits the timeline.
- **Motif / B-roll / music / SFX / ambience libraries grow each episode** → future episodes need less
  new generation.
- **Pino rig built once** → every Pino video animates automatically.

## F. Reduce the owner's decisions
- **Auto-draft titles / thumbnails / descriptions** (to 0005) → owner just picks; **A/B (YouTube
  Studio Test & Compare)** decides the rest from real data.
- **Batch production + batch approvals** so the owner reviews in one sitting (less context-switching).
- Earn **Autonomy Level 4** on proven steps (CLAUDE.md §3) → fewer gates over time, by measured
  performance.

## Priority (best quality-per-owner-effort first)
1. Auto depth→2.5D parallax (A) · 2. Audio auto-mastering + LUT grade (B) · 3. AI self-review pre-owner
(C) · 4. Auto-batch PD footage (D) · 5. Frame interpolation + upscale (A/B) · 6. Templated assembly +
growing libraries (E). All free or in-plan; none add owner clicks.

> Constraint: none of this lowers the safety/rights/BAN gates (§N) or fabricates facts; automated
> review augments, never replaces, the owner's four approval gates.
