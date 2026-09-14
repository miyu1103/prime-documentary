# CODEX HANDOFF — EP32 "Your Car, Your Rights" (PD-2026-032-carsearch)

> The single document a Codex thread reads to generate THIS episode's hero images correctly.
> Claude owns the LEFT side (topic / research / claims / script — LOCKED at `script_verified`) and
> owns everything AFTER generation (4K upscale, depth maps, motion-graphics, assembly, render).
> **Codex's ONLY job here: generate the 40 hero cinematic STILLS listed in the prompt pack.**
> Numbers and rules, not adjectives. Do exactly what this says and STOP at each gate.

---

## 0. WHAT THIS EPISODE IS

A prestige documentary on the law of vehicle searches — how the "automobile exception" grew from
**Carroll v. US (1925)** through probable cause and scope, **Collins v. Virginia** (the motorcycle
in the driveway / curtilage), and the modern map of a driver's rights (Gant, Byrd). Dark, restrained,
Veritasium/prestige-doc grade. It resolves on the quiet boundary between **your car and your home**.

The moving explainers — the glowing **bright-line** motif, the **car cutaway**, the **probable-cause
meter**, the **timeline**, the **curtilage shield**, the **US map**, the **checklist / car-key lock**,
kinetic type — are **built in code as motion-graphics. DO NOT generate those.** Codex delivers only the
photoreal cinematic plates and reconstruction beats the edit cuts between.

## 1. YOUR JOB (scope — read twice)

- Generate **exactly 40 hero stills, S001..S040 — ONE image per prompt, NOT a candidate pool.**
- The **full text of all 40 prompts is in `episodes/_planning/EP32_carsearch_ai_prompts.v001.md`**
  (titles S001..S040, each with its own scene description). **That file is authoritative — read it and
  generate from it verbatim.** This handoff wraps it with rules, delivery paths, and stop-gates; it does
  **NOT** restate or rewrite the 40 prompts. If this doc and the prompt pack ever disagree on style/negatives,
  the prompt pack's per-image description wins for content; the Hard Rules in §2 below always win for safety.
- Regenerate ONLY a specific shot that fails the Hard Rules (§2) or Quality Bar (§4).

## 2. ABSOLUTE HARD RULES (read first — apply to EVERY image)

1. **NO real-person face or likeness of ANYONE.** People are anonymous only: faces turned away,
   silhouetted, cropped at the shoulders, from behind, out of focus, or hands-only. No look-alikes,
   no celebrity/known-figure resemblance, no recognizable faces. (Invariant 11 — likeness risk is real.)
2. **NO on-image text of any kind** — no letters, numbers, captions, subtitles, signage, readable
   documents/screens, logos, badges, seals, or watermarks. **All text, citations, case names, and UI are
   added later by Claude as Remotion typography.** (E.g. the rental agreement in S021 must be blurred/unreadable.)
3. **Illustration / reconstruction only — never presented as an authentic archival record** (invariant 11).
   Nothing may look like real news footage, a real photograph, surveillance capture, or a genuine court/
   police document. Period beats are plausible *reconstructions*, not "found footage."
4. **No real logos, badges, seals, department insignia, or identifiable landmarks/real building interiors.**
   Use archetypal, generic equivalents.
5. **No gore.** Historically plausible props only (1920s beats must be 1920s-accurate).

A visible face/likeness, any readable text, a real logo/seal, a real landmark, or an authentic-looking
record = **automatic reject and regenerate.**

## 3. HOUSE STYLE (global — applies to every still)

- **Genre:** prestige legal documentary / noir; "your car, your home, and the line between them."
- **Palette:** dark noir — deep navy/black base with a single warm-amber OR electric-blue accent light;
  volumetric haze, shallow depth of field, filmic grain, high dynamic range; moody, premium, restrained.
  No candy neon, no oversaturation, no teal-orange grade.
- **Light:** motivated and low-key — red-and-blue patrol wash on wet asphalt, a raking flashlight beam,
  a warm porch lamp at blue hour, cold moonlight through columns, a single sodium streetlight.
- **Composition:** one clear subject; deliberate negative space for later Remotion text and the motion-
  graphics bright line; strong fore/mid/background depth; built for slow push, parallax, and depth-map crop.
- **Global negatives (append to every generation):**
  `text, letters, numbers, watermark, logo, caption, subtitles, signage, readable document, badge, seal,
  specific real person, celebrity likeness, recognizable face, deformed hands, extra fingers, bad anatomy,
  cartoon, 3d-render look, plastic AI sheen, low-res, jpeg artifacts, oversaturated, teal-orange grade,
  real landmark, real building interior, news-footage look, surveillance look, gore.`

## 4. QUALITY BAR (reject unless ALL pass)

- Clear subject + negative space for text; focal point readable at 320 px (mobile).
- Motivated, controlled cinematic light; real falloff; no flat stock look; no black crush.
- Believable materials + grain; clean anatomy on any implied figure; no plastic sheen.
- Narrative duty: the still locates / explains / builds tension / symbolizes its exact beat.
- Safety: passes every §2 Hard Rule.
- Editability: parallax / Ken-Burns / depth-map friendly, crop room, does not fight bottom-safe captions.
- Neighbor fit: visibly distinct from adjacent shots (the S025..S040 variants exist precisely so fast
  ~2.2 s cuts never repeat a frame — keep angle/framing genuinely different from the base shot they vary).

## 5. DELIVERY (exact)

- **40 files, one per prompt**, named **`PD-2026-032-S0NN-IMG-001.png`** (S001 → `PD-2026-032-S001-IMG-001.png`,
  … S040 → `PD-2026-032-S040-IMG-001.png`).
- Into: **`episodes/PD-2026-032-carsearch/04_scenes/generated_images/codex_v001/`**
- Format 16:9, PNG. Generate at the **highest quality the model allows, then upscale each to ≥ 3840 px on the
  long edge** before delivery. (If the base generation is smaller, upscale is part of your delivery here.)
- No text baked in; no alternate crops; exactly one image per S0NN.

## 6. PER-GATE STOP-AND-REPORT PROTOCOL (do not skip)

Work in the order below and **STOP at each gate. Do not proceed to the next stage until owner/Claude approves.**

- **GATE A — before generating:** confirm you have read the prompt pack (§1) and the Hard Rules (§2).
  Report: "Ready to generate 40 stills S001..S040 per EP32_carsearch_ai_prompts.v001.md." → **STOP for go.**
- **GATE B — after generating:** produce **one labeled contact sheet** (a grid thumbnailing all 40, each cell
  labeled S001..S040 with its one-line title) plus the 40 full-res files in the delivery folder.
  Report counts and any shot you are unsure about. → **STOP. Owner/Claude reviews the contact sheet.**
- **GATE C — regeneration only:** regenerate ONLY the specific S0NN shots flagged at Gate B (Hard-Rule or
  Quality-Bar failures). Re-deliver those cells + an updated contact sheet. → **STOP for re-review.**
- Do **NOT** self-approve, do NOT proceed to any downstream step, and do NOT upscale-to-final or touch
  assembly on your own initiative beyond the ≥3840 px delivery upscale in §5.

**Explicit division of labor:** After Codex's stills pass Gate B/C, **Claude handles everything downstream —
final 4K conditioning, depth-map generation per still, the code-built motion-graphics, factory b-roll
selection, assembly, and render.** Codex does not build motion, does not add text, does not assemble.

## 7. RIGHTS / PROVENANCE (per delivered still)

Every delivered still is registered by Claude in the rights manifest as **origin = Codex AI, AI-disclosed
symbolic reconstruction, no real-person likeness present.** Keep generation clean so that record is true:
no likeness, no real logo/seal, no readable real text, no authentic-looking record (invariant 11).

---

## 8. SHOT INDEX — S001..S040 → ACT / beat (context only; full prompt text is in the prompt pack)

| ID | One-line title | ACT / beat |
|----|----------------|------------|
| S001 | Night traffic stop, trunk open | HOOK / OPENING |
| S002 | Suburban driveway at dusk | HOOK / OPENING |
| S003 | The bright line (concept plate) | HOOK / OPENING (motion-graphics plate) |
| S004 | 1920s night highway | ACT I — Carroll / 1925 |
| S005 | Liquor in the back | ACT I — Carroll / 1925 |
| S006 | Tearing the seat | ACT I — Carroll / 1925 |
| S007 | Bottles lined up as evidence | ACT I — Carroll / 1925 |
| S008 | 1925 courthouse exterior | ACT I — Carroll / 1925 |
| S009 | House vs car (concept) | ACT I — Carroll / 1925 |
| S010 | Officer at the window (routine stop) | ACT II — Probable cause / scope |
| S011 | The glovebox / interior search | ACT II — Probable cause / scope |
| S012 | Trunk and bags | ACT II — Probable cause / scope |
| S013 | Night highway from above | ACT II — Probable cause / scope |
| S014 | Orange-and-black motorcycle, motion blur | ACT III — Collins / the motorcycle |
| S015 | House with a covered shape in the driveway | ACT III — Collins / the motorcycle |
| S016 | Lifting the tarp | ACT III — Collins / the motorcycle |
| S017 | Footsteps up the driveway | ACT III — Collins / the motorcycle |
| S018 | The home's edge (curtilage concept) | ACT III — Collins / the motorcycle |
| S019 | Supreme Court interior, empty | ACT III — Collins / the motorcycle |
| S020 | Handcuffed away from the car (Gant limit) | ACT IV — The map of your rights / limits |
| S021 | Rental car keys and agreement (Byrd) | ACT IV — The map of your rights / limits |
| S022 | Calm driver at a stop | ACT IV — The map of your rights / limits |
| S023 | Car and home, final image | ACT IV — resolving image |
| S024 | Phone lock screen glow | NEXT teaser (next episode) |
| S025 | Traffic stop, hand on the window | EXTRA / variant — traffic stop |
| S026 | Driver's POV | EXTRA / variant — traffic stop |
| S027 | 1920s highway, wide | EXTRA / variant — Carroll |
| S028 | The tail car | EXTRA / variant — Carroll |
| S029 | One bottle to the light | EXTRA / variant — Carroll evidence |
| S030 | Gavel on the bench | EXTRA / variant — courtroom |
| S031 | Trunk slammed shut | EXTRA / variant — scope aftermath |
| S032 | Bag pulled from the back seat | EXTRA / variant — scope / container |
| S033 | Motorcycle tank detail | EXTRA / variant — Collins |
| S034 | The whole quiet street | EXTRA / variant — establishing |
| S035 | Tarp half-lifted, chrome glint | EXTRA / variant — Collins reveal |
| S036 | The porch, intimate | EXTRA / variant — curtilage |
| S037 | Signing at the station | EXTRA / variant — procedural beat |
| S038 | Rental lot at dusk | EXTRA / variant — Byrd |
| S039 | Family car, golden hour (the stakes) | EXTRA / variant — thematic stakes |
| S040 | House key + car key (thematic macro) | EXTRA / variant — thematic close |

---

## 9. HANDOFF NOTES

- 40 hero stills cover Hook + Act I (Carroll) + Act II (scope) + Act III (Collins/curtilage) + Act IV
  (the rights map) + a next-episode teaser, plus angle/framing variants for fast non-repeating cutting.
- The assembly also layers **abundant commercial factory b-roll (real footage, ~100+ clips, visually
  QC'd)** + the **code-built motion-graphics** — so no single layer is overworked and cuts run fast (~2.2 s)
  without repeating a frame. Codex only owns the stills.
- Period beats S004–S008 and S027–S029 must be **1920s-accurate**; modern beats are neutral US-suburban.
- Reminder of the whole point: keep people anonymous, keep the frame text-free, keep it a cinematic
  reconstruction — never an authentic record (invariant 11).
