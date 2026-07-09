# CODEX HANDOFF — EP36 "The Algorithm Said It Was You" (PD-2026-036-williams)

> The single document a Codex thread reads to generate THIS episode's hero images correctly.
> Claude owns the LEFT side (topic / research / claims / script — LOCKED at `script_verified`) and
> owns everything AFTER generation (4K upscale, depth maps, motion-graphics, assembly, render).
> **Codex's ONLY job here: generate the hero cinematic STILLS listed in the prompt pack.**
> Numbers and rules, not adjectives. Do exactly what this says and STOP at each gate.

---

## 0. WHAT THIS EPISODE IS

A prestige documentary on the **first known US wrongful arrest by facial recognition**. In January 2020,
Detroit police arrested **Robert Julian-Borchak Williams** — an innocent man — in his own driveway, in
front of his wife and daughters, on the strength of a **face-recognition match run against a grainy
store-camera still**. The software picked him; the detectives ran with it; he spent about **30 hours in
jail** before anyone noticed he looked nothing like the actual thief. The episode walks the human story
end to end — the blurry surveillance frame, the algorithmic "match," the driveway arrest, the holding
cell, the measured **racial-accuracy gap** in the technology (NIST FRVT / MIT Gender Shades), and the
**2024 ACLU settlement** that changed when Detroit police may act on a face match. Second-person hook:
*this could be your face.* Cold, restrained, prestige-doc grade — the proven Riley/Carpenter
surveillance vein applied to your face.

The moving explainers — the **face-match grid** UI, the **similarity/confidence meter**, the
**accuracy/bias bar chart**, the **2018 → 2020 → 2024 timeline**, the pixel-zoom on the surveillance
frame, kinetic type and all case/citation cards — are **built in code as motion-graphics. DO NOT generate
those, and DO NOT bake any chart, grid, number, or timeline into a still.** Codex delivers only the
photoreal cinematic plates and reconstruction beats the edit cuts between and layers the motion-graphics
on top of.

## 1. YOUR JOB (scope — read twice)

- Generate **exactly the hero stills listed in the prompt pack — ONE image per prompt, NOT a candidate
  pool.** The pack sets the exact IDs (S001..S0NN) and the exact count; do not add, drop, or merge shots.
- The **full text of every prompt is in `episodes/_planning/EP36_williams_ai_prompts.v001.md`** (each
  S0NN with its own scene description). **That file is authoritative — read it and generate from it
  verbatim.** This handoff wraps it with rules, delivery paths, and stop-gates; it does **NOT** restate or
  rewrite the prompts. If this doc and the prompt pack ever disagree on style/negatives, the prompt pack's
  per-image description wins for content; the Hard Rules in §2 below always win for safety.
- Regenerate ONLY a specific shot that fails the Hard Rules (§2) or Quality Bar (§4).

## 2. ABSOLUTE HARD RULES (read first — apply to EVERY image)

1. **NO real-person face or likeness of ANYONE — and, specifically, NEVER depict Robert Williams'
   likeness.** Robert Julian-Borchak Williams is a **living, named private individual**; rendering his
   face, or a recognizable look-alike of him, is an automatic reject (Invariant 11 — likeness risk is
   real and this is a real person). ALL people in every still are anonymous only: faces turned away,
   silhouetted, cropped at the shoulders, from behind, out of focus, or hands-only. No look-alikes of
   Williams, his family, any Detroit officer, any public figure, or any celebrity. No recognizable face
   of anyone.
2. **NO on-image text of any kind** — no letters, numbers, captions, subtitles, signage, readable
   documents/screens, logos, badges, seals, percentages, similarity scores, dates, or watermarks. **All
   text, citations, case names, chart numbers, timeline dates, and UI are added later by Claude as
   Remotion typography and motion-graphics.** Any document, phone screen, monitor, warrant, or booking
   card in frame must be blurred/illegible.
3. **Illustration / reconstruction only — never presented as an authentic archival record** (Invariant
   11). Nothing may look like real news footage, a real body-cam/dashcam capture, a genuine
   surveillance-camera export, a real booking photo, or an actual police/court document. **The grainy
   store-camera beat is a plausible *reconstruction* of low-quality footage — it is NOT, and must never
   read as, real evidence, a real mugshot, or authentic captured footage.** Period/procedural beats are
   reconstructions, not "found footage."
4. **No real logos, badges, seals, department insignia, vendor/product UI, or identifiable
   landmarks/real building interiors.** No "Detroit Police," no real software-vendor branding, no real
   courthouse. Use archetypal, generic equivalents.
5. **No gore. No inflammatory or degrading framing.** Race is central to the accuracy-gap story; depict
   anonymous figures with dignity and neutrality — no caricature, no menacing/criminalizing framing of
   any figure. Contemporary, US-accurate props only (2018–2024 beats).

A visible face/likeness (especially Williams'), any readable text/number, a real logo/seal/vendor UI, a
real landmark, or an authentic-looking record/mugshot/footage = **automatic reject and regenerate.**

## 3. HOUSE STYLE (global — applies to every still)

- **Genre:** modern surveillance / rights documentary; "a machine looked at a face and got a man
  arrested." Cold institution versus warm human life.
- **Palette:** restrained and cold — desaturated slate, charcoal, and deep blue base with a single
  motivated accent: the **cyan-blue glow of a screen / camera / face-scan**, or the **cold green-white of
  fluorescent booking light**. The human beats (the family home, the driveway before it turns) carry a
  single **warm domestic amber** to contrast the machine's cold light. Volumetric haze, shallow depth of
  field, filmic grain, high dynamic range; premium, moody, understated. No candy neon, no oversaturation,
  no teal-orange grade.
- **Light:** motivated and low-key — cyan monitor/scan glow on a face turned away, cold overhead
  fluorescents in a holding area, a warm porch/kitchen lamp at blue hour, a raking flashlight on a
  driveway, grey daylight through blinds. The surveillance-reconstruction beats read deliberately
  low-resolution/high-noise *as a stylized reconstruction*, never as a real camera export.
- **Composition:** one clear subject; deliberate negative space for later Remotion text, the face-match
  grid, the bias chart, and the timeline; strong fore/mid/background depth; built for slow push, pixel
  push-in, parallax, and depth-map crop.
- **Global negatives (append to every generation):**
  `text, letters, numbers, percentages, dates, watermark, logo, caption, subtitles, signage, readable
  document, readable screen, badge, seal, insignia, mugshot, Robert Williams, specific real person,
  celebrity likeness, recognizable face, look-alike, deformed hands, extra fingers, bad anatomy, cartoon,
  3d-render look, plastic AI sheen, low-res artifacts unintended, jpeg artifacts, oversaturated,
  teal-orange grade, real landmark, real building interior, real police department, real news-footage
  look, authentic surveillance export, gore.`

## 4. QUALITY BAR (reject unless ALL pass)

- Clear subject + negative space for text/graphics; focal point readable at 320 px (mobile).
- Motivated, controlled cinematic light; real falloff; no flat stock look; no black crush.
- Believable materials + grain; clean anatomy on any implied figure; no plastic sheen.
- Narrative duty: the still locates / explains / builds tension / symbolizes its exact beat.
- Safety: passes every §2 Hard Rule (no Williams likeness, no readable text/number, no authentic-record
  look).
- Editability: parallax / Ken-Burns / pixel-push / depth-map friendly, crop room, does not fight
  bottom-safe captions or the motion-graphics overlays (grid / chart / timeline).
- Neighbor fit: visibly distinct from adjacent shots so fast (~2.2 s) cuts never repeat a frame — keep
  angle/framing genuinely different from any base shot a variant varies.

## 5. DELIVERY (exact)

- **One file per prompt**, named **`PD-2026-036-S0NN-IMG-001.png`** (S001 → `PD-2026-036-S001-IMG-001.png`,
  … through the last ID in the prompt pack).
- Into: **`episodes/PD-2026-036-williams/04_scenes/generated_images/codex_v001/`**
- Format 16:9, PNG. Generate at the **highest quality the model allows, then upscale each to ≥ 3840 px on
  the long edge** before delivery. (If the base generation is smaller, upscale is part of your delivery
  here.)
- No text/numbers baked in; no alternate crops; exactly one image per S0NN.

## 6. PER-GATE STOP-AND-REPORT PROTOCOL (do not skip)

Work in the order below and **STOP at each gate. Do not proceed to the next stage until owner/Claude approves.**

- **GATE A — before generating:** confirm you have read the prompt pack (§1) and the Hard Rules (§2).
  Report: "Ready to generate the stills S001..S0NN per EP36_williams_ai_prompts.v001.md." → **STOP for go.**
- **GATE B — after generating:** produce **one labeled contact sheet** (a grid thumbnailing every still,
  each cell labeled S0NN with its one-line title) plus the full-res files in the delivery folder. Report
  counts and any shot you are unsure about (especially any figure that risks reading as a specific person,
  or any beat that risks reading as real footage/evidence). → **STOP. Owner/Claude reviews the contact sheet.**
- **GATE C — regeneration only:** regenerate ONLY the specific S0NN shots flagged at Gate B (Hard-Rule or
  Quality-Bar failures). Re-deliver those cells + an updated contact sheet. → **STOP for re-review.**
- Do **NOT** self-approve, do NOT proceed to any downstream step, and do NOT upscale-to-final or touch
  assembly on your own initiative beyond the ≥3840 px delivery upscale in §5.

**Explicit division of labor:** Codex generates the stills only. After they pass Gate B/C, **Claude
handles everything downstream — final 4K conditioning, depth-map generation per still, the code-built
motion-graphics (face-match grid, similarity meter, bias bar chart, 2018→2020→2024 timeline, kinetic
type, all citation/case cards), commercial factory b-roll selection, assembly, and render.** Codex does
not build motion, does not add text or charts, does not assemble. **Do NOT auto-launch local SDXL/SD3.5**
— long-form images are Codex's job here (rule 19); local models are a Claude-side exception reserved only
for fixing a Codex image or an emergency missing-image add.

## 7. RIGHTS / PROVENANCE (per delivered still)

Every delivered still is registered by Claude in the rights manifest as **origin = Codex AI, AI-disclosed
symbolic reconstruction, no real-person likeness present.** This episode centers on a **real, living,
named private individual (Robert Williams, R2 risk)** — keep generation clean so that record is true: no
likeness of Williams or his family, no real officer likeness, no real Detroit PD or vendor logo/seal, no
readable real text, no authentic-looking surveillance frame / mugshot / booking record / court document
(Invariant 11). Generated visuals are **illustration / reconstruction, never presented as authentic
footage.**

---

## 8. SHOT INDEX (hero stills — derived from script.annotated.v001)

> Hero photoreal plates + reconstruction beats ONLY. The moving explainers (face-match grid, similarity
> meter, bias bar chart, 2018→2020→2024 timeline, map pins, kinetic type, case cards) are code-built by
> Claude and are NOT generated here — several plates below are deliberately neutral *backings* the
> motion-graphics sit on top of. The exact per-image prompt text is finalized in the scene-planning pass
> (`EP36_williams_ai_prompts.v001.md`, 04_scenes); this index fixes the count, the beats, and the safety
> intent. Every still obeys §2 Hard Rules — no Williams/any real likeness, no readable text/number, no
> authentic-record look.

| ID | one-line title | ACT / beat |
|----|----------------|------------|
| S001 | Grainy store-camera reconstruction — a dark-cap figure, illegible by design (a stylized recon, NOT a real export) | HOOK / the blurry "evidence" |
| S002 | Suburban driveway at blue hour; warm porch light going cold as headlights sweep in; anonymous | ACT I / the arrest |
| S003 | An anonymous figure walked off a front lawn in handcuffs, seen from behind; family silhouettes in a lit window | ACT I / handcuffed in front of family |
| S004 | Cold-fluorescent holding/booking reconstruction; hands only; two blurred photographs on a steel table (NOT a real mugshot/record) | ACT I / ~30 hours in a cell |
| S005 | A dark server room / face-database, aisles of racks under cyan glow — "the quiet machine" | ACT I→II / the machine that looked at you |
| S006 | A downtown watch-shop interior at night, a wall of watches, one camera on the ceiling | ACT II / the 2018 theft |
| S007 | Anonymous candidate-portrait plates (neutral backing the code-built face-match grid arranges) — no real likeness, no UI | ACT II / how the match is made |
| S008 | A physical six-photo lineup card on a detective's table, faces blurred/anonymous; a hand hovering | ACT II / the circular lineup |
| S009 | A clean, neutral data-lab / standards-lab environment plate (backing for the bias chart) | ACT III / the federal study |
| S010 | A lopsided-dataset plate: rows of anonymous silhouettes, most one tone, a few others — dignified, neutral | ACT III / trained on too few of us |
| S011 | A DMV / license-photo setting; an ordinary anonymous face turned away under a cold scan line — viewer's-eye | ACT III / your face is in the lineup |
| S012 | A neutral courthouse/legal exterior at dusk (archetypal, NO real landmark) | ACT IV / the lawsuit & settlement |
| S013 | A city-scale map/aerial plate at night (neutral backing for the timeline + single-pin motion-graphic) | ACT IV / one city, one rule |
| S014 | A row of anonymous suburban door-frames at dusk, warm interiors snuffing to cold; no faces | ACT IV / he was not the last |
| S015 | The hook's blurry frame finally resolving into an ordinary anonymous face turning away — release | ENDING / the face turns away |
| S016 | Driveway VARIANT — wider, from the street, the two cruisers' light on the house | ACT I (non-repeat cut) |
| S017 | Holding-cell VARIANT — tight on an institutional clock and a bolted door | ACT I (non-repeat cut) |
| S018 | Face-scan VARIANT — extreme macro of a single eye crossed by a scan line | ACT III (non-repeat cut) |

**Count: 18 hero stills (S001–S018).** Deliver as `PD-2026-036-S0NN-IMG-001.png` per §5. This count may be
refined by ±a few in the scene-planning pass; the prompt pack is authoritative for the final list. Every
figure anonymous; every store-camera/booking beat a stylized reconstruction, never a real record
(Invariant 11).
