# PD ONE-PASS PRODUCTION SPEC & ACCEPTANCE CONTRACT (v1)

**Status:** BINDING for every episode from EP17 onward (EP16 retrofit-optional). Consolidates decisions/0002, 0004, 0005, 0006, 0007 + `scripts/check_final_acceptance.py`.
**Purpose:** Eliminate the recurring rework spiral (Riley v007 / Carpenter v008 / Madoff v010; "caption" appears 85× in event logs). Every problem the owner keeps hitting is pre-specified here with an **exact spec** + a **measurable gate** + a **verification command**. Codex must build the FIRST render to satisfy this whole table.

## THE ONE RULE
> **"Done" ≠ validator PASS. "Done" = the independent acceptance script measures the real `final.mp4` (+ provenance) and ALL hard gates pass.** The producing agent may NOT hand-write its own quality gate (EP14 graded its own homework and shipped SAPI voice / no captions / black frames). Self-reported QC is rejected (CLAUDE.md invariant 13, rule 17). A new revision re-runs the full gate.

Final gate command (must exit 0 before "package_ready"):
```
./.venv/Scripts/python.exe scripts/check_final_acceptance.py <NN> --json
```
The runtime band is read from the episode's duration profile (standard 11.5–12.5 / mid 27–33 / feature 55–65), NOT hardcoded.

---

## A. THE FAILURE-MODE → SPEC → GATE TABLE (the contract)

Each row is a thing that has gone wrong. Build to the SPEC; the GATE is how it's proven; nothing ships until every hard GATE passes.

| # | Recurring problem | EXACT SPEC (build to this) | GATE (hard, measured on real file) | Verify |
|---|---|---|---|---|
| 1 | **BGM doesn't play** | Continuous **library music bed**, ducked under VO to ~ -22 LUFS (VO at front), one track per chapter from the 8-category set (hook/opening/explainer_bed/tension_build/somber/reveal/outro/ambience). No chapter without a bed except the deliberate silence beat. | `bgm_present`: no silent stretch > **25 s**; music energy present across the timeline. | check_final_acceptance |
| 2 | **Voice is "different"** | Narration master = **ElevenLabs**, `VOICE_ID=nPczCjzI2devNBz1zQrb`, `model_id=eleven_multilingual_v2`, `stability≈0.35`, `similarity_boost≈0.80`, style 0, speaker_boost on. SAPI/local = timing draft ONLY, never shipped. | `voice_is_master`: narration provider contains `eleven`, never `sapi/windows/zira/local`. | check_final_acceptance |
| 3 | **Narration ≠ captions** | Captions are **forced-aligned to the rendered ElevenLabs audio** (not pasted from the script). Text must match spoken words verbatim. | Caption text ↔ narration token match **≥ 99%**; `captions_final` sidecar `.srt` non-empty, covers **≥ 95%** of runtime. | check_final_acceptance + caption-diff |
| 4 | **Captions break badly / hard to read** | ≤ **2 lines/cue**, ≤ **42 chars/line**, break only at clause/punctuation boundaries (never split a word or a preposition off its noun), **1.0 s ≤ cue ≤ 6.0 s**, ≥ 2 frames gap between cues, no orphan single-word cues, reading speed ≤ 17 cps. Burned-in style = brand font, bottom-safe, drop-shadow. | Caption QC json: 0 violations of the line/char/duration/cps rules. | caption QC script |
| 5 | **Images coarse / low quality** | SDXL gen 1344×768 (juggernautXL) → **upscale to long edge ≥ 3840 px** (R-ESRGAN/Topaz on 4090) + denoise + brand LUT grade. Reject any still that is blurry, has artifacts, bad anatomy, text, or a real-person likeness. | Image QC: every used still long-edge ≥ 3840, sharpness (variance-of-Laplacian) ≥ threshold, 0 NEG-violations. | image QC script |
| 6 | **Not "Max quality"** | Render **libx264 `-preset slow -crf 16` (≤17)**, `-pix_fmt yuv420p`, 1920×1080 (4K master if source allows), **never NVENC**. Audio `aac 192k`. Integrated loudness **-16…-12 LUFS**. Per-chapter render → concat. | `runtime_band` + `loudness` pass; crf/preset asserted from render log. | check_final_acceptance |
| 7 | **Downloaded factory assets barely used** | **Every span carries ≥ 1 layer**; across the episode use **≥ 1 distinct factory clip per ~45 s** as the establish/"間" layer; no single clip reused > 3×; b-roll must match the span's `search_keywords`. The 221 GB / 65k shelf is the point — use it. | Asset-usage audit: distinct_factory_used ≥ runtime/45; max-reuse ≤ 3; 0 empty spans. | asset-usage script |
| 8 | **Animation is weak / unwatchable** | **No static image, ever.** Each still gets MovingImage (Ken Burns ≥ 6% zoom or parallax via `Parallax.tsx`/`Motion.tsx`), b-roll = MovingVideo, hero beats get organic loops (SVD/AnimateDiff) + ink/particle overlays; transitions are designed, not hard cuts only. No frame held motionless > 2 s. | Motion audit: 0 spans with zero motion; mean motion magnitude ≥ threshold. | motion audit script |
| 9 | **Hook is not a highlight** | **Hook 0:00–0:30 = a flash-forward highlight montage** of the 3–5 strongest beats (5–8 s cuts, the best images, the killer line, the open question). **Written LAST**, after the script, and **the body must pay it off** (promise-payoff QC). | `hook_added`: runtime exceeds (body+bookends) by ≥ 25 s; promise-payoff check = the teased reveal appears later. | check_final_acceptance + payoff QC |
| 10 | **Not Hook/Opening/Body/Ending** | Mandatory 4-part spine with explicit chapter ids: **hook** (0:00–0:30) → **opening** (thesis + "what you'll learn", channel ID) → **body** (the episode) → **ending** (payoff + single clear CTA: subscribe / next). | Structure gate: all four chapter roles present and ordered; CTA present in last 30 s. | structure QC |
| 11 | **No thumbnail prepared** | **≥ 3 thumbnail variants** rendered as Remotion `<Still>` at **1280×720** (`BRAND.thumb`) BEFORE package_ready; files exist on disk; a `selected` is chosen. Upload is **manual** (thumbnails.set API blocked, PD-001). | thumbnail_present: ≥ 3 PNG 1280×720 (< YouTube size limit) + 1 selected. | thumbnail QC |
| 12 | **Thumbnail not striking** | UPPERCASE headline **≤ 3–4 words** (auto-split), one **emotional/curiosity** idea, huge subject, **high contrast** black/navy bg + **gold `#E5B53A` or electric `#1F6BFF` accent** + white/silver text, readable at mobile thumbnail size (test at 320 px wide). No clutter. | thumbnail QC: headline word-count ≤4, contrast ratio ≥ threshold, legible at 320px. | thumbnail QC |
| 13 | **Thumb/title not CTR-max** | Title **≤ 60 chars, hook first**; thumbnail+title = the episode's curiosity hypothesis, **honest** (body delivers the promise — a package that can't pay off the promise does NOT win even at high CTR). Ship **A/B title×thumb variants** for the experiment loop (doc27). | Packaging gate: title ≤60, ≥2 A/B variants, promise-payoff = true. | packaging QC |

> "他にも大量に": rows 1–13 are the known set; the **catch-all** is row 0 (THE ONE RULE) — the independent acceptance script is the final wall. If a new defect class appears, it is added here as a row AND a check, so it can never recur silently (no silent caps, rule 17).

---

## B. WHAT MUST EXIST BEFORE CODEX IS ASKED TO RENDER (left-process gate)
Claude does not hand off until these are locked, so Codex can hit row 1–13 on the FIRST pass:
1. `script.annotated.<v>` — with the **hook written last + promise-payoff verified**, and the explicit hook/opening/body/ending chapter roles.
2. `shotlist.<v>` — every span has asset_type + motion + factory `search_keywords` (drives rows 7–8).
3. `ai_prompts.<v>` — hero prompts with the upscale target noted (row 5).
4. `thumb_prompts.<v>` + headline/kicker candidates (rows 11–13).
5. `fact_recheck.<v>` packet (R2/R3) — facts/quotes locked verbatim (prevents the EP16-style v002).
6. Duration profile set in `manifest.target_duration_minutes` (selects the runtime band).

## C. VERIFIER STATUS (infra to keep current)
`scripts/check_final_acceptance.py` machine-enforces (hard gates, measured on the real file):
rows **1 (bgm), 2 (voice master), 3 (caption coverage), 4 (caption format: lines/chars/cue/cps),
6 (runtime band from profile + render resolution ≥1920×1080), 8 (motion: no static/freeze beyond a held beat), 9 (hook headroom), 11 (≥3 thumbnails @1280×720 + selected)** + black-frame + loudness. Verified non-regressing on EP15 (all hard PASS) and correctly flagging EP16 draft captions.
**Still manual** (specified above, never skipped/self-attested until coded): row 5 (source still ≥3840 px + sharpness), row 7 (factory-usage density), row 12 (thumbnail CTR design legibility), row 13 (title ≤60 / A-B / promise-payoff semantics).

## D. DEFINITION OF DONE (per episode)
- `check_final_acceptance.py <NN>` → exit 0 (all hard gates).
- Rows 4,5,7,8,11,12,13 measured (script or manual) → 0 violations.
- first-cut / title-thumbnail / pre-publish fact re-check / scheduling = owner gates, in order.
- Then, and only then, `state = package_ready`.

*This spec is the contract. Building to "looks good" is the bug. Building to this table is the fix.*
