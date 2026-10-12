# Factory B-roll — Visual QC Checklist (MANDATORY)
Episode: PD-2026-032-carsearch — "Can the Police Search Your Car?"
Companion to: `asset_selection.v001.json` (candidate plan)
Rule this enforces: ship-gate `footage_diversity` + owner directive "factory棚のラベルは信用しない／出荷前に必ず目視QC".

## Why this exists (the failure we are preventing)
The factory shelf's folder/subtype labels are **wrong often enough to break an episode**. Proven this session:
`motorcycle`, `handcuffs`, `tarp`, `glovebox`, `bottle`, `driveway`, `rental`, `taillight`, `trunk` all return **0** clips even though the inventory doc implies some exist — and in the past a **cowboy** clip slipped into a legal episode. **A green machine gate does NOT prove a clip matches the scene.** A human eye must see every first frame before it enters the render. Never trust the folder label alone.

## Hard rule
> No factory clip enters the Remotion/CaseFilm render until its **first frame has been eyeballed on a labeled contact sheet and marked KEEP**. Selection by query is a *candidate*, not an approval.

---

## Step 1 — Pull candidates (read-only, no bulk copy)
For every candidate in `asset_selection.v001.json`, list the shelf files (do not copy media yet):
```
python scripts/select_factory_assets.py --subtype <subtype> --kind video --json
```
Pull **more** files than the plan's `candidate_clips` count for each subtype (e.g. 2–3× headroom) so rejects can be swapped without re-querying.

## Step 2 — Build a LABELED contact sheet of FIRST FRAMES
Extract frame 0 of every candidate and tile it with its label burned in (`AF-id · subtype · scene`).
- Use ffmpeg to grab `-frames:v 1` at t=0 (and a mid-frame t=50% as a second thumbnail — first frames can be black/fade-in).
- Montage into `qc/contact_sheet_carsearch.v001.jpg` with the label under each tile.
- One tile per candidate FILE (not per subtype). This is the artifact a human scans.

## Step 3 — Eyeball every tile against its scene need
For each tile, confirm ALL of:
- [ ] **Subject actually matches** the scene need in `asset_selection.v001.json` (a "police_car_lights_night" tile really is a police car at night — not a taxi, not a fire truck, not a cowboy).
- [ ] **No wrong era / wrong place** (1920s beats must not show modern cars/signage; US legal story must not show foreign courthouses).
- [ ] **No watermark / logo / stock-agency bug / burned-in text / timecode.**
- [ ] **No real, identifiable person's face** used as if it were the real case's person (invariant 11). Prefer silhouettes, hands, backs, empty establishing shots.
- [ ] **No real license plate, badge number, or real-brand insignia** readable on screen.
- [ ] **Not featureless / flat / mushy** — must hold up at 1920×1080; no heavy compression blocks, no near-black nothing-frame.
- [ ] **Tone fits** the PD palette (black / navy / blue / gold); reject clashing color casts.
- [ ] **Motion is usable** for a ~2.2s cut (no jarring zoom-in-progress, no on-screen date overlays, no hard cut mid-clip).

Mark each tile **KEEP** / **BLOCK** / **BACKUP**.

## Step 4 — Block-list mismatches
Record every reject in `qc/blocklist_carsearch.v001.json` with `{af_id, subtype, reason}` so it is never re-pulled for this episode. Reasons to always block: mislabeled subject, watermark, readable plate/badge/face, wrong era, featureless, tone clash.

## Step 5 — Diversity gate (must pass before render)
Cross-check the KEEP set against the ship-gate thresholds (mirrors `asset_selection.v001.json > diversity_tally`):
- [ ] distinct clip files / total placements **≥ 0.40** (plan is ~1.00 — every cut is a unique file).
- [ ] no single clip file reused **> 4** times (plan cap = 2).
- [ ] generic-symbol clips (gavel / scales / flag / lady-justice / constitution-as-symbol) **≤ 2** total (plan = 2: `judge_gavel_wooden`×1, `lady_justice_statue`×1).
- [ ] **No repeated framing** across scenes: subtypes that recur (`police_car_lights_night`, `suburban_house_exterior_night`, `car_light_trails_long_exposure`, `highway_night_long_exposure`, `courthouse_steps`, `front_door_house`, `world_map_dark_glowing`, `drone_city_aerial_night`, `rain_street_reflection_night`) MUST use a **visually distinct file/angle** in each scene — never the same file recut.

## Step 6 — Gaps do NOT get faked from the shelf
These beats are **not on the shelf** (verified 0 results). Do **not** substitute a mislabeled clip. Route to Codex AI stills (no real-person likeness / no real plate) or to Remotion motifs:
- Gloved hands tearing a seat cushion; a whisky bottle to the light (SPN-0004) → Codex.
- Car interior: glovebox / open trunk / zipped bag / hand pulling a bag (SPN-0010) → Codex + Remotion `CarCutaway`.
- Orange-and-black motorcycle blur; tarp-covered shape in a driveway; hand peeling the tarp; footsteps up a driveway (SPN-0013/0014) → Codex.
- Person handcuffed on a curb (SPN-0019) → Codex (no likeness) or Remotion.
- Rental car lot (SPN-0019) → `empty_parking_garage` substitute is acceptable ONLY if QC confirms it reads as a lot; otherwise Codex.
- US state-by-state "smell = probable cause" map (SPN-0020) → Remotion `RegionHighlightMap` (data graphic, not b-roll).

## Step 7 — Promote only KEEP clips
Copy only KEEP files into `remotion/public/carsearch/factory/`, and record `{af_id, path, sha256, scene}` for each (provenance — invariant 7). Anything not on the KEEP list never reaches the render.

## Sign-off
- [ ] Contact sheet built and every tile reviewed by a human.
- [ ] Block-list written.
- [ ] Diversity gate checks tick.
- [ ] Gaps routed (not faked).
- [ ] Only KEEP clips promoted, with provenance.

Reviewer: __________  Date: __________  Result: PASS / FAIL
