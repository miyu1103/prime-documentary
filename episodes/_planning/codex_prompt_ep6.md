# Codex prompt — EP6 (Terry v. Ohio) — paste this whole block into one Codex thread

You are Codex, working in the Prime Documentary repo (github.com/miyu1103/prime-documentary), branch
`claude/vibrant-archimedes-2mmr5h`. Before doing anything, read `CLAUDE.md` and
`episodes/_planning/EP6-8_HANDOFF.md`.

## Your role
Division of labor (owner-set): Claude has finished the LEFT pipeline (topic → research → claims →
script). **You own the RIGHT pipeline: scenes → images → narration → music → edit → render.**

The script for this episode is FINISHED, owner-approved (APR-0001), schema-validated, and
`state = script_verified`. It is LOCKED. **Do NOT rewrite, re-summarize, re-time, or regenerate the
script, the annotated script, or the claims.** If you believe a factual line is wrong, STOP and flag
it to the owner — do not edit it yourself (editing re-opens the approval gate).

## Locked input (read, do not modify)
- `episodes/PD-2026-006-terry/03_script/script.en.v001.md` — the narration ([VO:] = spoken).
- `episodes/PD-2026-006-terry/03_script/script.annotated.v001.json` — 30 claim-linked spans, each
  with `visual_intent` and `on_screen_text`. Build your scenes to these spans; respect chapter order
  and `estimated_duration_seconds` (~11 min).
- `episodes/PD-2026-006-terry/01_research/claims.v001.json` — the cited facts behind each span.
- `episodes/PD-2026-006-terry/manifest.json` — current state and active revisions.

## Toolchain (authoritative — CLAUDE.md §11 + handoff §0A)
- Images: **Codex image generation = primary**; local SDXL/SVD for bulk variants.
- Motion / on-screen graphics: Remotion. Narration: ElevenLabs (PAID). Music/SFX: Suno reuse library.
- Edit & render: **Remotion + FFmpeg** (CPU/libx264, quality-first). Thumbnail: Remotion.
- Heavy media (images/video/audio/renders) → `H:\pd-media` (git-ignored). Repo holds the brain only.

## Hard rules (non-negotiable)
1. Every AI image: disclosed as AI, registered in the rights manifest (origin/creator/license/
   verified_at), brand-consistent (`remotion/src/brand.ts`), and **NO real-person likeness or
   deepfake** — McFadden, Terry, Chilton must never be depicted as identifiable real people
   (invariant 11).
2. No paid API (ElevenLabs/Runway), upload, or publish without **explicit owner approval** +
   idempotency + budget check. Respect `guard_destructive` / `check_secrets` hooks.
3. All visuals are symbolic reconstruction, never authentic footage; set the YouTube altered/
   synthetic-content disclosure and keep an on-screen "symbolic reconstruction" label.
4. Tone: neutral, advertiser-safe, educational. Commit each step to the branch with clear messages.

## Pipeline to run (this episode)
1. `pd-scenes` → scene/shot/visual/on-screen-text plan from the annotated spans (continuity +
   generation specs). Reuse each span's `visual_intent` and `on_screen_text`.
2. `pd-generate-assets` → generate the images (Codex primary; SDXL/SVD for variants), QC and register
   them with rights metadata.
3. Narration (ElevenLabs — request owner approval before the paid run) + music (Suno library) +
   Remotion motion/graphics.
4. `pd-build-edit` → assemble and render in Remotion + FFmpeg; run QC.
5. **STOP at the first-cut review gate, then at the title/thumbnail gate, for owner approval. Do not
   publish.**

## EP6 specifics
- Working title: "A Cop Can Search You Without a Warrant — Here's the Catch." (test 3–5 variants at
  the title/thumbnail gate.)
- Risk class: **R2 — policing. Stay strictly neutral** (neither anti- nor pro-police). The later
  stop-and-frisk controversy is documented debate, not accusation (CLM-0009); do not present any
  city/era practice as fact unless it is grounded.
- Visual throughline (present-tense framing): open on a POV street stop with no faces; Act I = two
  men casing a store window with an animated trip-counter to ~12; Act II = an animated "probable
  cause vs reasonable suspicion" sliding scale; Act III = 1968 / 8–1 / "Terry v. Ohio, 392 U.S. 1"
  lower-thirds and a tight, weapons-only frisk motif; Act IV = a modern street-stop montage (still no
  faces). The ending teases EP7 (the phone in your pocket) — leave a clean hook for the next video.
- Brand palette: black / navy / electric-blue / gold (see `remotion/src/brand.ts`).

## First action
Read the four locked input files above and `CLAUDE.md` §11 + the handoff, then post a short scene
plan summary (chapters → shots → image prompts → on-screen text) for owner review BEFORE generating
assets. Then proceed through the pipeline, stopping at the gates.
