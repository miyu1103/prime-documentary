# Visual QC Plan — PD-2026-032-carsearch v001

Revolution-format episode: symbolic reconstruction stills + code-built motion graphics + heavy commercial factory b-roll. The bar is deliberately high — every selected still should be strong enough to pause on, crop into a thumbnail, or reuse as a premium brand asset. **Nothing is trusted on self-report** (CLAUDE invariant 13): factory footage is eyeballed on a labeled contact sheet, depth maps are inspected, and the perceptual motion budget is machine-verified before render.

---

## 0. Contact-sheet gate (do this FIRST, before staging anything)

A past failure was **corrupted factory-shelf labels** injecting off-theme footage (an "evidence_bag" theme returning cartoon/cowboy clips) that machine gates cannot detect. So:

1. Build a **labeled contact sheet** (thumbnail grid) for every candidate factory clip AND every generated still, grouped by scene (S001…S022), each tile stamped with its filename, theme label, and target scene.
2. A human **eyeballs every tile**. Reject anything off-theme, off-era, off-brand, or mislabeled — do not rely on the shelf label.
3. Only clips/stills that pass the eyeball are staged for edit. Record the pass in the rights manifest.
4. Themes to pull and verify for this episode: night traffic stop / patrol lights, wet asphalt, suburban driveway & porch at dusk, aerial night highway, 1920s car & road, courthouse/gavel, hands-on-container search, motorcycle, tarp/wind, rental lot, phone lock screen. **Reject:** cowboy/western, cartoon/CGI-looking, modern branded vehicles with readable logos, identifiable faces, any clip that reads as authentic news/archival.

## 1. Acceptance standard (a still is accepted only if it passes ALL)

1. **Scene fit** — supports the exact scene purpose in `scene_plan.v001.json`.
2. **Visual role** — identify, locate, explain, humanize, tension, symbolize, or reset attention.
3. **Composition** — clear focal hierarchy, strong silhouette/object shape, intentional negative space for kinetic type.
4. **Light & texture** — motivated light, deep but readable shadows, believable asphalt / chrome / fabric / glass / metal.
5. **Brand fit** — black/navy + electric-blue + gold + silver; restrained, advertiser-safe; no candy color; no police-strobe dominance.
6. **Rights/safety** — AI-disclosed, no real-person likeness (esp. Carroll, Taft, McReynolds, **Ryan Collins — living, R2**, Sotomayor, Alito), no faces, no logos, no generated text, no authentic-footage implication.
7. **Technical** — clean hands/body geometry, no extra limbs, no watermark, no compression artifacts, 16:9 crop-safe, ≥3840px long edge.
8. **Editability** — supports DepthStill parallax / Ken Burns; subject not blocked by lower-third or captions.
9. **Neighboring-shot diversity** — differs from adjacent selected visuals in scale, angle, brightness, subject, or visual mode (fast ~2.2s cutting must never repeat a frame).

## 2. Depth-map QC (DepthStill parallax — the ≥40% budget)

- Every still tagged `DEPTH` in the shotlist gets a depth map from `gen_depth.py`. **Inspect each depth map** for: correct foreground/background separation, no haloing on hands/silhouettes, no flicker on parallax preview.
- If a depth map is bad, either repair it or downgrade that still to Ken Burns — **but then re-check the depth budget stays ≥40%** of still cuts (target 56.8%, floor 40%).
- Confirm the parallax amplitude is visible (not a frozen frame) but not seasick.

## 3. Motion-budget verification (machine, before render — §5 of the design)

Verify in the builder and record PASS/FAIL against `scene_plan.v001.json → coverage.motion_budget`:

- depth-treated still cuts / total still cuts **≥ 40%** (plan: 54/95 = 56.8%).
- moving FigureBeats **≥ 6** (plan: 9).
- hero motion surfaces **≥ 2** (plan: 3 — hook BrightLine, CarKeyLock, Collins BrightLine slam).
- average cut **≈ 2.2s** (plan: 690/314 = 2.20s); no scene holds a single static frame.
- transitions are ForcefulCut only; **no `WipeTransition` gold vertical sweep**, no default crossfade.
- After render: `motion_energy` mean ≥ 12 on the body, plus a 60–90s probe slice eyeballed for real movement.

## 4. Candidate counts

- Hero / Tier A stills (S001 hook, S004 Carroll, S013/S014 Collins turn, S016 payoff support, S021 resolve): **≥8 candidates** before selection; **+4** after prompt repair if needed.
- Tier B stills: **≥4 candidates**.
- Motion graphics (carsearch/motionkit): no AI image — verify exact text, dates, vote (8-1, not 7-1), quotes (Taft, Sotomayor), citations, counter (0→68), and animation timing in the actual render.

## 5. Hard rejection (reject immediately if any appear)

- identifiable face or portrait-like likeness (any era; Collins is living);
- police badge/logo, readable signage/plates, generated legal text, watermark, signature;
- weapon glamorization, aiming, violence, gore, or fearbait;
- modern objects in 1920s scenes (S004/S005 era beats) unless deliberately abstracted and approved;
- real, identifiable landmark implying a location not stated in the script;
- photojournalistic framing that could be mistaken for authentic footage (invariant 11);
- AI anatomy defects, plastic skin, smeared hands, duplicated people;
- generic stock-photo look, or a visual that performs no narrative job;
- **off-theme factory clip from a corrupted shelf label** (cowboy/cartoon/etc.).

## 6. Human review required (before locking selected images)

- **S001** hook (night traffic stop + driveway);
- **S004 / S005** 1920s Carroll reconstruction (era accuracy, no faces);
- **S008 / S010 / S011** stop & search sequence (no fearbait, no glamorized weapon/contraband);
- **S013 / S014** Collins driveway/tarp reconstruction (**Ryan Collins is a living person — role only, no likeness**);
- **S019** cuffed-person / rental beat;
- **S021** resolving driver/car-and-home image.

## 7. Selection workflow

1. Generate the required candidate count for one prompt family.
2. Reject hard failures first.
3. Score survivors 1–5 on scene fit, composition, light, material detail, brand fit, safety, editability.
4. Keep the best 1–2 per hero prompt; mark alternates for crop/coverage only (feeds the ~2.2s cutting without repeats).
5. Compare against neighboring shots before final selection.
6. Register selected files in the rights manifest: origin, creator, license/rights basis, hash, prompt id, generated_at, verified_at, AI disclosure.
7. If no candidate reaches the standard, repair the prompt or switch the visual mode. **Do not lower the bar** (invariant 15).

## 8. First-cut implication

No generated still or factory clip enters the first-cut render unless it is selected, **contact-sheet eyeballed**, rights-registered, and QC-marked pass (or warn-with-owner-note). Temporary placeholders may appear only in a clearly marked internal animatic — never in an owner-facing first cut. After render, confirm the real file exists and its `sha256` differs from the previous render before muxing or emitting a receipt (no false greens).
