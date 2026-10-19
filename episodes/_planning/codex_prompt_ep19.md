# CODEX HANDOFF — EP19 Operation Varsity Blues (PD-2026-019-varsityblues)

> This is the single design document Codex reads to BUILD the episode. Claude owns the LEFT side
> (topic/research/claims/script) — already done and LOCKED. Codex owns the RIGHT side
> (scenes → images → narration → music → motion → edit → render → thumbnails).
> **Build the FIRST render to satisfy the whole acceptance table. Numbers, not adjectives.**

## 0. HARD CONSTRAINTS (do not cross)
- **R3 episode (living people who pleaded guilty / were convicted).** NO real-person likeness anywhere
  (video, thumbnails, stills). No real university logos/crests/mascots/landmarks. Symbolic reconstruction only.
- **No publish, no external upload, no paid API** without explicit owner approval + idempotency + budget check.
- Stop at the owner gates: first-cut, title/thumbnail, pre-publish legal/rights review, scheduling.
- Render LOCAL CPU libx264, quality-first; NEVER NVENC. Heavy media → `H:\pd-media\episodes\PD-2026-019-varsityblues\`.
- Respect guard_destructive / check_secrets hooks. Commit each step.

## 1. BINDING SPEC + ACCEPTANCE (the contract)
- Canonical spec: **`docs/PD_ONE_PASS_PRODUCTION_SPEC.v2.md`** (binding from EP19). Build to rows 1–16.
- "Done" ≠ self-QC. **Run the independent gate and do not declare done until it exits 0:**
  ```
  ./.venv/Scripts/python.exe scripts/check_final_acceptance.py 19 --json
  ```
- Duration profile: **mid, target 30:00** (final runtime band ~27–33; narration ~27 min).

## 2. LOCKED INPUTS (DO NOT REWRITE — invariant 6/12)
- Script: `episodes/PD-2026-019-varsityblues/03_script/script.en.v001.md` (~4,630 words, 4-part + CTA).
- Annotated spans (claim-linked, visual_intent per span): `03_script/script.annotated.v001.json` (77 spans).
- Claim ledger (R3 wording locks): `01_research/claims.v001.json` (16 claims).
- Sources: `01_research/sources.v001.json` (11). Topic: `00_topic/topic.v001.json`.
- **R3 WORDING LOCKS (must survive editing — never contradict in any on-screen text/caption):**
  pleaded guilty (not "convicted at trial"); Loughlin & Giannulli pleaded to FRAUD CONSPIRACY only —
  NEVER "convicted of money laundering / bribery" (dismissed); Singer 3 charged → 4 pleaded; counts
  date-qualified (50 at unsealing vs 55 charged / 53 convicted total); universities = VICTIMS, not
  defendants; children's knowledge not imputed; "side door" = Singer's word; legal "back door" donation ≠ crime.

## 3. STRUCTURE & TIMING (build to these)
- **Hook ~0:00–0:08** = fast flash-forward highlight montage (≈2 s cuts; EP19-IMG-001..006).
- Then **Opening → Body (Act 1–4) → Ending**, per the script's marked timecodes.
- Gold **BrandOpening lands AFTER the hook** (~post-cold-open), not at frame 0. **BrandEndcard at tail.**
- OP/ED canonical = `remotion/src/components/Bookends.tsx` (`OPENING_SEC=3.5`, `ENDCARD_SEC=9`; do not fork).

## 4. VOICE (row 2)
- ElevenLabs master, **VOICE_ID `nPczCjzI2devNBz1zQrb`**, `eleven_multilingual_v2`, stability≈0.35,
  similarity≈0.80, style 0, speaker_boost on. SAPI/local = timing draft only, NEVER shipped.
- Generate narration from the [VO:] lines only (ignore `#` production-note lines and `[CLM-xxxx]` tags).

## 5. CAPTIONS (rows 3–4)
- Forced-align to the rendered ElevenLabs audio (verbatim). **1 cue = 1 breath group** (split at the
  narrator's actual breaths). ≤2 lines, ≤42 chars/line, 1.0–6.0 s, ≤17 cps, ≥2-frame gaps. Brand font,
  bottom-safe, drop-shadow. Coverage ≥95%.

## 6. MUSIC / BGM (row 1)
- Continuous library bed (Suno reuse), one track per chapter from the 8-category set. **Duck under VO to a
  floor of ~ -22 LUFS — the bed must stay AUDIBLE under narration; never duck to silence.** No silent
  stretch > 25 s. Integrated loudness -16…-12 LUFS. (Fixes the "BGM not audible" defect.)

## 7. IMAGES — Codex generation (row 5) — APPENDIX A is the prompt pack
- **Generate every one of the 92 numbered MEGA-PROMPTS in `04_scenes/codex_image_prompts.v001.md`**
  (EP19-IMG-001..092), candidate counts as listed, BEFORE edit. That file's §0 Hard Rules, §1 Style Bible,
  §2 Universal Negative, §3 Quality Bar are binding. Codex image gen = PRIMARY; local SDXL (JuggernautXL,
  §10 settings) only as fallback.
- **Output ≥ 3840 px long edge, 16:9**, brand palette (black/navy + electric-blue `#1F6BFF` + gold
  `#E5B53A` + silver). Upscale + denoise + brand LUT if raw gen is smaller.
- Reject any still with a face/real-person likeness, real logo/crest/landmark, readable text, or anatomy
  errors — regenerate. Register every used still in the rights manifest (origin=Codex AI, license,
  verified_at) and disclose as AI symbolic reconstruction.

## 8. MOTION / EDIT (row 8) — fixes "weak animation" + "stutter (かくっ)" + "boring static image"
- **No static image, ever; no frame held > 2 s; no naked hard cut.** Every still gets Ken Burns ≥ 6% zoom
  or parallax; hero beats get organic motion (SVD) + ink/particle overlays.
- **Transitions are designed: 0.3–0.5 s crossfade/dissolve; overlap Sequences by the transition length so
  there is no 1-frame black or jump; carry motion direction through the cut (no velocity reset = the
  "かくっ"); Trail motion blur on fast moves.**
- **Fast pace: average shot ≤ ~6 s; the picture is always changing.**
- **Abundant material (row 7):** use the factory shelf densely — ≥ 1 distinct factory clip per ~30 s as the
  establish/"間" layer; no single clip reused > 3×; every span carries ≥ 1 layer. (`scripts/select_factory_assets.py --theme school/legal/crime/finance`.)

## 9. DEDICATED SUBSCRIBE+LIKE CTA (per script production note, ~29:10–29:35)
- Build exactly to the `# [PRODUCTION — DEDICATED CTA BEAT …]` note in the script: gold "SUBSCRIBE" pill
  slides up (spring damping 14 / stiffness 120, ~0.45 s) + gold underline wipe (Easing.out(Easing.cubic),
  0.5 s); white "LIKE" thumb pops in (spring damping 10 / stiffness 140) and FILLS gold on the spoken word
  "like" with a 6% scale pulse + particle spark (Trail); navy vignette behind; hold ~5 s; ease out 0.4 s;
  one soft UI click SFX on the like-fill; music dips ~3 dB (bed stays audible). NO real YouTube logo. PD brand styling.

## 10. THUMBNAILS (rows 11–13)
- **≥ 3 variants** as Remotion `<Still>` at **1280×720** BEFORE package_ready; background art pre-generated
  by Codex (see `04_scenes/thumb_prompts.v001.md` when added — same Hard Rules: no real-person likeness).
- "派手": UPPERCASE headline ≤ 3–4 words, one curiosity idea, huge subject, very high contrast,
  black/navy + gold `#E5B53A` or electric `#1F6BFF` accent, white/silver text, legible at 320 px.
  Title ≤ 60 chars; ship A/B title×thumb variants. Upload is MANUAL (thumbnails.set ok now; verify).
  Headline ideas (honest to the body): "THE SIDE DOOR", "BOUGHT, NOT EARNED", "$25M TO GET IN".

## 11. RETENTION / LIKE-RATE (row 16) — already engineered in the script
- The cold-open question (the side door + the FBI morning) is paid off in Act 4 / Ending; re-hooks every
  ~2–3 min; earned Like ask in the CTA. Keep the edit tight so the retention curve stays flat-to-rising.

## 12. DEFINITION OF DONE (then STOP for owner)
- `check_final_acceptance.py 19` exits 0; rows 4,5,7,8,11,12,13,15,16 measured → 0 violations.
- First-cut gate → title/thumbnail gate → **R3 legal/rights review** → scheduling = owner gates, in order.
- Final-script approval is also an owner gate: `approvals/APR-0001.json` is currently **pending** — do not
  treat the script as owner-approved until that flips.
