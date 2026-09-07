# Codex hand-off prompts — EP6–EP8 (surveillance trilogy)

How to use: open a separate Codex thread per episode. Paste **[SHARED CONTEXT]** first, then the
**[EP… TASK]** block for that episode. Claude has finished research + script; Codex does visuals → video.

---

## [SHARED CONTEXT]  (paste into every thread)

You are Codex, operating the Prime Documentary repo (github.com/miyu1103/prime-documentary), branch
`claude/vibrant-archimedes-2mmr5h`. Read `CLAUDE.md` and `episodes/_planning/EP6-8_HANDOFF.md` first.

Division of labor (owner-set): Claude owns the LEFT pipeline (topic → research → claims → script).
**You own the RIGHT pipeline: scenes → images → narration → music → edit → render.**
The scripts are FINISHED, owner-approved (APR-0001), schema-validated, `state=script_verified`, and
LOCKED. **Do NOT rewrite, re-summarize, or regenerate the script or claims.** If you think a factual
line is wrong, STOP and flag it to the owner — do not edit it yourself (it would re-open the gate).

Toolchain (authoritative, see CLAUDE.md §11 + handoff §0A):
- Images: **Codex image generation = primary**; local SDXL/SVD for bulk variants.
- Motion / on-screen graphics: Remotion. Narration: ElevenLabs (PAID). Music/SFX: Suno reuse library.
- Edit & render: **Remotion + FFmpeg** (CPU/libx264, quality-first). Thumbnail: Remotion.
- Heavy media (images/video/audio/renders) → `H:\pd-media` (git-ignored). Repo holds the brain only.

Hard rules (non-negotiable):
1. Every AI image: disclosed as AI, registered in the rights manifest, brand-consistent
   (`remotion/src/brand.ts`), and **NO real-person likeness / deepfake** (invariant 11).
2. No paid API call (ElevenLabs/Runway), upload, or publish without **explicit owner approval** +
   idempotency + budget check. Respect `guard_destructive` / `check_secrets` hooks.
3. Visuals are symbolic reconstruction, never presented as authentic footage; set YouTube
   altered/synthetic disclosure; keep an on-screen "symbolic reconstruction" label.
4. Neutral, advertiser-safe, educational tone. Commit each step to the branch.

Pipeline to run (per episode): `pd-scenes` → `pd-generate-assets` → narration + music + Remotion
motion → `pd-build-edit` (assemble + render) → run QC. **STOP at the first-cut review gate AND the
title/thumbnail gate for owner approval.** Honor each annotated span's `visual_intent` and
`on_screen_text`. Keep ~12:00 pacing (annotated `estimated_duration_seconds`).

---

## [EP6 TASK] — PD-2026-006-terry — Terry v. Ohio (1968)

Locked input:
- `episodes/PD-2026-006-terry/03_script/script.en.v001.md`
- `episodes/PD-2026-006-terry/03_script/script.annotated.v001.json` (30 spans, claim-linked)
- claims: `episodes/PD-2026-006-terry/01_research/claims.v001.json`

Do: build the scene/shot/visual plan, generate images, narrate, score, assemble and render — then
stop for owner review. Working title: "A Cop Can Search You Without a Warrant — Here's the Catch."
Risk R2 (policing — strictly neutral; the later stop-and-frisk debate is documented debate, not
accusation; no city/era stated as fact unless grounded in CLM-0009).
Key visual motifs: a present-tense street stop (no faces); two men casing a store window with an
animated trip-counter; a "probable cause vs reasonable suspicion" diagram; 1968 / 8–1 / "392 U.S. 1"
lower-thirds. Ends teasing EP7 (the phone).

## [EP7 TASK] — PD-2026-007-riley — Riley v. California (2014)

Locked input:
- `episodes/PD-2026-007-riley/03_script/script.en.v001.md`
- `episodes/PD-2026-007-riley/03_script/script.annotated.v001.json` (29 spans, claim-linked)
- claims: `episodes/PD-2026-007-riley/01_research/claims.v001.json`

Working title: "Can the Police Search Your Phone?" Risk R2 (real defendants by role; neutral; no
editorializing on guilt). Key visual motifs: a phone lifted from a pocket at an arrest (no faces); an
animated "wallet vs smartphone" data contrast; "half in your pocket, half in the cloud"; 2014 / 9–0 /
"573 U.S. 373" + the quote "Get a warrant." Phrase the vote as unanimous-in-result (9–0), Alito
concurring in part (CLM-0002). Ends teasing EP8 (location).

## [EP8 TASK] — PD-2026-008-carpenter — Carpenter v. United States (2018)

Locked input:
- `episodes/PD-2026-008-carpenter/03_script/script.en.v001.md`
- `episodes/PD-2026-008-carpenter/03_script/script.annotated.v001.json` (30 spans, claim-linked)
- claims: `episodes/PD-2026-008-carpenter/01_research/claims.v001.json`

Working title: "Your Phone Is Tracking You — and the Police Wanted the Map." Risk R2 (Carpenter is a
convicted person on the public record — neutral, factual; no editorializing beyond the record). Key
visual motifs: a location trail blooming on a dark map over 127 days; pings-to-towers becoming a path;
a single dialed-number list vs a full location map; 2018 / 5–4 / "585 U.S. 296". **The vote is 5–4 —
ignore any 6–3 summary (CLM-0002).** Series capstone: callback to body (Terry) → phone contents
(Riley) → location (Carpenter); ends on the viewer's own device.
