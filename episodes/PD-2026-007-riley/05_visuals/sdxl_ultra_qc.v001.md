# PD-2026-007 Riley - SDXL Ultra QC v001

## Scope

Local A1111 SDXL candidates generated to:

`H:/pd-media/episodes/PD-2026-007-riley/05_visuals/sdxl_ultra_v001/`

No paid API, no upload, no publish.

## Generated So Far

- `hook/RILEY_H01_phone_lift_pocket_*`: 6 candidates.
- `opening/RILEY_H02_phone_window_life_c01_seed808043.png`: 1 candidate.
- Contact sheet: `contact_hook_opening_v001.png`.

## QC Result

Status: `reject_for_selection`

The first S001 SDXL batch is not selected. It is clean enough for safety review, but it misses the
owner's quality bar and the exact scene intent.

Reasons:

- The shots are too wide and torso-led, not a decisive macro image of a phone being lifted from a pocket.
- Several candidates read as a person holding a phone after the fact, not the phone-search seizure moment.
- The composition is serviceable but not museum-grade: weak subject hierarchy, limited negative-space drama, and insufficient material detail.
- The opening candidate is a useful mood reference only; it is too abstract and not yet a final S002 image.

## Action

- Keep the files as rejected candidates/mood references only.
- Do not route them into Remotion.
- Do not register them as selected rights-manifest assets.
- Regenerate S001 with the revised prompt in `scripts/gen_riley_sdxl_ultra.py`, which now forces
  extreme macro pocket/phone composition and supports targeted `--ids` reruns.

## Current Blocker

A1111 is currently busy with other local generation jobs (`generate_madoff_sdxl_gallery_v003.py` and
`gen_terry_sdxl_ultra.py`). The EP7 targeted rerun was stopped rather than interfering with those
jobs. Resume with:

```powershell
python .\scripts\gen_riley_sdxl_ultra.py --ids RILEY_H01_phone_lift_pocket --candidates 4
```

Then rebuild the contact sheet and score against `04_scenes/visual_qc_plan.v001.md`.

## Update - 2026-06-20 16:36 +09:00

Additional S001 sets were generated:

- `sdxl_ultra_v002`: closer to phone-pocket intent, rejected because the images still read as people
  holding phones rather than the decisive seizure object.
- `sdxl_ultra_v003`: rejected; visually stronger but still too hand/person-led and not a pocket image.
- `sdxl_ultra_v004`: rejected; did not follow no-person/object-portrait instruction.
- `sdxl_ultra_v005`: first object-led set; candidate 06 became a useful direction but the screen was
  too bright/blue.
- `sdxl_ultra_v006`: selected `hook/RILEY_H01_phone_lift_pocket_c06_seed857894.png` as
  `H:/pd-media/episodes/PD-2026-007-riley/05_visuals/selected/PD-2026-007-S001-IMG-001.v001.png`.

Selected S001 score:

- Concept clarity: 18/20
- Composition/editability: 20/20
- Light/color: 19/20
- Material realism: 18/20
- Safety/rights: 20/20
- Total: 95/100

Rationale: the image is object-led, faceless, no text/logo, brand-consistent, with strong negative
space and a clear privacy-through-phone motif. It is less literal than a hand removing the phone, but
that is preferable to accepting weaker person-led reconstructions. The seizure action will be
completed in Remotion with motion, SFX, and the on-screen `symbolic reconstruction` label.
