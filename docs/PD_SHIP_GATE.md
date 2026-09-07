# PD Ship Gate — the mechanical "definition of done" (binding on every thread)

Owner 2026-07-04: the recurring pain was not a missing spec — it was shipping before the
spec was actually met, i.e. self-certified "done". This gate makes the promise mechanical:
**a long-form episode cannot be scheduled unless an independent gate has measured the exact
render bytes and issued a green receipt.** No agent (any thread) may bypass it.

## The rule

1. Build the final render (BGM-muxed master).
2. Run the independent gate and emit a receipt bound to the render's sha256:

   ```
   .venv/Scripts/python.exe scripts/check_final_acceptance.py <ep> --render <final.mp4> --emit-receipt
   ```

   It writes `episodes/<ep>/09_package/acceptance_receipt.v001.json` with per-check results,
   `status`, and `video_sha256`.
3. Schedule ONLY via `scripts/upload_schedule_case_v001.py --ep <slug>`. It **hard-refuses**
   to upload unless a receipt exists whose `video_sha256` matches the file and whose only
   tolerated hard failure is `runtime_band` (the single owner-accepted deviation).
4. Never hand-write acceptance. Never weaken a check/threshold to pass (CLAUDE invariant 15).

## What the gate mechanically enforces (hard checks)

- `voice_is_master` — ElevenLabs master narration, not the SAPI review proxy.
- `captions_final` / `caption_format` / `caption_narration_match` — real sidecar, clean
  breaks (≤2 lines, ≤50 char, ≤27 cps), and **100%-grade token match to the narration**.
- `structure_4part` — HOOK → OPENING → body → ENDING, with a real cold-open hook.
- `op_ed_bookends` — canonical BrandOpening + BrandEndcard.
- `render_resolution` ≥ 1920×1080 · `images_present` (no long black) · `bgm_present` /
  `bgm_ending` (continuous ducked bed that resolves, not chopped).
- `motion_present` + **`animation_density`** — not merely "not frozen": near-still spans are
  flagged, so a 紙芝居 / slow-Ken-Burns slideshow FAILS. Premium motion is required, not optional.
- **`footage_diversity`** — distinct/total ≥ 0.40, no clip reused > 4×, generic symbols
  (scales/gavel/clock…) ≤ 2×. Kills the "同じ素材の使い回し / 天秤を何度も見た" class.
- **`thumbnail_visibility`** — the selected thumbnail must be bright/punchy (luma + contrast
  floor), not a dull dark panel. Plus `thumbnail_ready` (≥3 @1280×720 + selected).
- `image_resolution` (4K hero stills) · `factory_used` (shelf actually cut in).

## Premium animation is a requirement, not a nicety

The `CaseFilm` engine MUST render beautiful, dynamic, high-end motion (owner's #1 theme):
designed **motion-blurred cut transitions**, real motion blur (`@remotion/motion-blur` Trail)
on kinetic beats + hook, **mask-reveal kinetic typography** ("切り上がり"), animated accents.
`animation_density` is the mechanical floor; the look bar is the approved MotionSample.
Banned: left→right vertical sweep line, full-screen yellow/gold wash, plain zoom/pan-only.

## Other standing constraints (propagate to all threads)

- Long-form hero images = **Codex only**. Do not auto-launch SDXL for long-form.
- Footage shelf: stage a wide, theme-varied pool (`select_factory_assets.py --theme …`) so
  `build_case_film_assets.py` clears the diversity target; the builder warns how many more to add.
- Public scheduling stays an owner-gated step; the receipt lock does not replace owner approval.
