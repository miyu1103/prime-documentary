# EP56–EP60 Codex requested image batch — completion v001

Date: 2026-08-02  
Generator: Codex built-in `image_gen` only  
Scope: still-image generation, import, registration, and image QC only

## Result

- Logical deliverables: **73 / 73**
- Built-in generation requests: **77**
- Accepted final images: **73**
- Rejected first attempts: **4** (`postoffice` S212, S214, S216, S217)
- Missing files: **0**
- Bad dimensions: **0**
- Primary/render-copy SHA-256 mismatches: **0**
- Manifest registration misses: **0**

## Delivered sets

| Set | IDs | Count | Final size | Primary location | Render location |
|---|---:|---:|---:|---|---|
| EP56 postoffice gap-fill | S211–S224 | 14 | 3840×2160 | `H:\pd-media\assets\ai\postoffice` | `remotion/public/postoffice/img` |
| EP57 fieldtest people | P003–P014 | 12 | 3840×2160 | `episodes/PD-2026-057-fieldtest/04_scenes/generated_images` | `remotion/public/fieldtest/img` |
| EP58 lejeune gap-fill | S211–S224 | 14 | 3840×2160 | `H:\pd-media\assets\ai\lejeune` | `remotion/public/lejeune/img` |
| EP59 robosigning gap-fill | S211–S224 | 14 | 3840×2160 | `H:\pd-media\assets\ai\robosigning` | `remotion/public/robosigning/img` |
| EP60 surfside people | P001–P018 | 18 | 3840×2160 | `episodes/PD-2026-060-surfside/04_scenes/generated_images` | `remotion/public/surfside/img` |
| EP60 surfside thumbnail face | SURFSIDE_FACE_v001 | 1 | 1920×1080 | `H:\pd-media\assets\ai\surfside\thumb` | n/a |

## QC and repairs

- All final PNGs opened successfully with Pillow and matched their required dimensions.
- Every duplicated primary/render pair matched byte-for-byte by SHA-256.
- Five labeled contact sheets were reviewed for scene intent, obvious anatomy failures, visible text/logos, anonymity, and continuity.
- EP57 P010/P011 were produced as a matched pair: P011 used P010 as the image reference and changed only the vial liquid from pink to cobalt blue.
- EP60 thumbnail passed on the first attempt: subject left, right half dark and empty, no text or logo.
- EP56 S212/S214/S216/S217 initially contained an indoor red pillar box; S212 also had a legible-looking green display. Those four were rejected and selectively regenerated. The accepted v002 images remove the pillar box and display.
- Rejected EP56 files are preserved under `H:\pd-media\assets\ai\postoffice\rejected_gapfill_v001`.
- Accepted repair candidates remain under `H:\pd-media\assets\ai\postoffice\candidates_gapfill_v002`.

Contact sheets (local QC cache):

- `cache/montages/ep56_postoffice_gapfill.jpg`
- `cache/montages/ep57_fieldtest_people.jpg`
- `cache/montages/ep58_lejeune_gapfill.jpg`
- `cache/montages/ep59_robosigning_gapfill.jpg`
- `cache/montages/ep60_surfside_people.jpg`

## Registration

- EP56–EP59 requested additions are present in each episode's `05_visuals/asset_manifest.v003.json`.
- EP57 P003–P014 are present in both `stills[]` and `people[]`; `counts.people` is 14 including the existing P001/P002.
- EP60 P001–P018 are present in both `stills[]` and `people[]`; `counts.people` is 18.
- Pre-update backups for EP56–EP59 are stored beside each manifest with suffix `.before-requested-images-20260802.bak`.

## Cost and side effects

- No SDXL, ComfyUI, A1111, CLI image API, `OPENAI_API_KEY`, upload, publish, or external messaging path was used.
- The built-in image tool does not expose per-request billing metadata here, so a currency cost cannot be stated. Total built-in generation requests were 77.
- No existing approved image was overwritten. The only replacements were four newly generated, QC-rejected EP56 candidates, and their first versions were backed up before promotion.

## Remaining out of scope

`check_episode_inputs.py --slug surfside` now sees **130 stills, including 18 faces**, so the people-image gap is closed. It still reports four downstream input problems: missing narration index, missing narration audio, zero factory clips, and no `Ep60*` Remotion composition. Those are not part of this image-only delivery.
