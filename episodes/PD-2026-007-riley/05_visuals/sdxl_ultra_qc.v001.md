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
