# Codex prompt — EP8 (Carpenter v. United States) — paste this whole block into one Codex thread

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
- `episodes/PD-2026-008-carpenter/03_script/script.en.v001.md` — the narration ([VO:] = spoken).
- `episodes/PD-2026-008-carpenter/03_script/script.annotated.v001.json` — 30 claim-linked spans, each
  with `visual_intent` and `on_screen_text`. Build your scenes to these spans; respect chapter order
  and `estimated_duration_seconds` (~11 min).
- `episodes/PD-2026-008-carpenter/01_research/claims.v001.json` — the cited facts behind each span.
- `episodes/PD-2026-008-carpenter/manifest.json` — current state and active revisions.

## Toolchain (authoritative — CLAUDE.md §11 + handoff §0A)
- Images: **Codex image generation = primary**; local SDXL/SVD for bulk variants.
- Motion / on-screen graphics: Remotion. Narration: ElevenLabs (PAID). Music/SFX: Suno reuse library.
- Edit & render: **Remotion + FFmpeg** (CPU/libx264, quality-first). Thumbnail: Remotion.
- Heavy media (images/video/audio/renders) → `H:\pd-media` (git-ignored). Repo holds the brain only.

## Hard rules (non-negotiable)
1. Every AI image: disclosed as AI, registered in the rights manifest (origin/creator/license/
   verified_at), brand-consistent (`remotion/src/brand.ts`), and **NO real-person likeness or
   deepfake** — Timothy Carpenter must never be depicted as an identifiable real person
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

## EP8 specifics
- Working title: "Your Phone Is Tracking You — and the Police Wanted the Map." (test 3–5 variants at
  the title/thumbnail gate.)
- Risk class: **R2 — Carpenter is a convicted person on the public record. Stay neutral and
  factual; do not editorialize on guilt beyond the record.**
- Accuracy note for on-screen text: the vote is **5–4** (CLM-0002). **Ignore any "6–3" summary** — a
  stray AI-generated case summary misreports it; the correct vote is 5–4.
- Visual throughline (present-tense framing) — this is the series capstone: open on a location trail
  blooming on a dark map from a phone icon, "127 days · no warrant"; Act I = Detroit 2010–2011 store
  robberies (symbolic) → pings-to-towers becoming a connected path → "~12,898 points"; Act II = a
  thin single dialed-number list vs a full life-mapping location trail (the third-party doctrine,
  Smith 1979 / Miller 1976); Act III = 2018 / 5–4 / "Carpenter v. United States, 585 U.S. 296"
  lower-thirds; Act IV = "location was just the first door" (search/purchases/messages/sensors). The
  ending is the trilogy payoff — callback to Terry (the body) → Riley (the phone's contents) →
  Carpenter (location); land it on the viewer's own device.
- Brand palette: black / navy / electric-blue / gold (see `remotion/src/brand.ts`).

## First action
Read the four locked input files above and `CLAUDE.md` §11 + the handoff, then post a short scene
plan summary (chapters → shots → image prompts → on-screen text) for owner review BEFORE generating
assets. Then proceed through the pipeline, stopping at the gates.
