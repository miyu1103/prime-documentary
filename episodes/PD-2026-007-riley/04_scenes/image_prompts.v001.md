# PD-2026-007 Riley - Image Prompt Pack v001

Inputs are locked to `script.en.v001.md`, `script.annotated.v001.json`, and `claims.v001.json`.
Do not generate readable text inside images. All exact text, citations, labels, and vote graphics
must be rendered in Remotion.

## Global Style

Use Prime Documentary palette from `remotion/src/brand.ts`: black, deep navy, electric blue, silver,
and restrained gold. Images are symbolic reconstructions, not authentic footage. No logos, no
watermarks, no readable UI, no real-person likeness, no identifiable David Riley or Brima Wurie,
no identifiable judges, no sensational gang imagery, no gore, no minors.

Base prompt suffix:

`cinematic documentary still, symbolic reconstruction, not authentic footage, deep black and navy palette, electric blue practical glow, restrained gold accent, fine film grain, realistic materials, high contrast, shallow depth of field where appropriate, no on-image text, no readable logos, no watermark, no identifiable faces, no real-person likeness, 16:9`

Base negative constraints:

`readable text, logos, brand icons, real public figure likeness, identifiable defendant face, judge portrait, police brutality imagery, gore, weapons pointed at camera, extremist symbols, gang signs, sensational crime scene, extra fingers, malformed hands, distorted phone, duplicate objects, overprocessed HDR, plastic skin, frame or border`

## Prompts

### PD-2026-007-S001-IMG-001 - Arrest POV Phone Lift
Present-tense point-of-view close shot of a smartphone being lifted from a jacket pocket during an
arrest, only hands and torso fragments visible, no face, police uniform suggested only by dark fabric
and reflected blue light, tense but neutral, phone screen dark with a faint electric-blue edge glow.

### PD-2026-007-S002-IMG-001 - Phone As Window
Dark tabletop with a wallet, keys, and a smartphone; the smartphone opens visually into layered
abstract life data, photos as blurred rectangles, messages as unreadable light blocks, map points,
calendar shapes, all non-branded and unreadable.

### PD-2026-007-S003-IMG-001 - San Diego Roadside Stop
Anonymous 2009 roadside traffic stop at night in Southern California, police lights reflected on a
car body, no license plate, no readable street signs, no faces, palm silhouettes distant and subtle.

### PD-2026-007-S004-IMG-001 - Car Search Symbolic
Close detail of a car trunk or interior being searched, flashlight beam across dark upholstery,
sealed evidence markers suggested without readable text, no visible faces, no dramatic violence.

### PD-2026-007-S004-IMG-002 - Phone Evidence Table
Smartphone and sealed evidence bag on a dark police-station table, gloved hand partially visible,
cold overhead light, no readable label, no face.

### PD-2026-007-S005-IMG-001 - Station Phone Search
Smartphone on a detective desk under cold blue light, anonymous hands near the device, blurred file
folders in background, no readable documents, no face, neutral investigative tone.

### PD-2026-007-S006-IMG-001 - Case File Escalation
Anonymous case folder, phone silhouette, and a thin gold line connecting a roadside stop to a larger
case board; all documents unreadable, no photos, no suspect faces.

### PD-2026-007-S007-IMG-001 - Smartphone And Flip Phone
Modern smartphone beside a basic flip phone on a dark evidence table, both closed or unreadable,
electric-blue rim light, subtle gold case divider line, no hands.

### PD-2026-007-S010-IMG-001 - Wallet And Phone Analogy
Macro still life of a simple wallet with a few cards next to a smartphone, dark tabletop, phone
screen black, composition designed for Remotion overlays.

### PD-2026-007-S011-IMG-001 - Data Layers
Smartphone emitting many abstract data layers into dark space, generic icons only, no brand shapes,
blurred photo tiles without faces, electric-blue and silver layers with small gold highlights.

### PD-2026-007-S012-IMG-001 - Pocket And Cloud
Anonymous hand holding a phone while thin blue data threads rise toward abstract cloud-server shapes
in the distance, no logos, no readable UI, no face.

### PD-2026-007-S014-IMG-001 - Symbolic Supreme Court
Empty symbolic Supreme Court chamber or marble courthouse corridor, no justices, no portraits,
dramatic navy shadows and restrained gold light, space left for lower-third citation.

### PD-2026-007-S015-IMG-001 - Privacies Of Life
Anonymous human silhouette formed from phone data fragments, messages as unreadable blocks,
calendar shapes, map pins, photos with no faces, intimate but restrained, dark negative space.

### PD-2026-007-S016-IMG-001 - House Versus Phone
Abstract composition of a small house outline dwarfed by an expanding smartphone data field, no real
address or room detail, cinematic but diagram-friendly.

### PD-2026-007-S018-IMG-001 - Katz Phone Booth Callback
1960s public phone booth at night, a human silhouette inside with face fully hidden by shadow and
glass reflection, privacy field suggested by electric-blue light, no readable signage.

### PD-2026-007-S019-IMG-001 - Category Protection
Smartphone and flip phone under a single dramatic overhead light, both anonymous and unreadable,
clean negative space for a bracket graphic.

### PD-2026-007-S022-IMG-001 - Apps Reveal A Life
Generic non-branded app-like tiles floating from a locked phone: prayer symbol, heart, medical
cross, book, map dot, message bubbles, all abstract and unreadable, no real app logos, no faces.

### PD-2026-007-S022-IMG-002 - Private Corners Montage
Close macro of a phone with blurred generic app tiles reflected in glass, blue and gold light,
private mood, no readable text, no brand shapes, no identifiable person.

### PD-2026-007-S023-IMG-001 - Phone To Carrier Trail
Phone on dark surface emitting pulsing location points to a distant abstract cell tower and cloud,
no real map, no carrier logo, no readable place names.

### PD-2026-007-S025-IMG-001 - Locked Phone Warrant Path
Locked smartphone on dark table with a gold light path leading toward an abstract judge bench or
warrant seal shape, no readable text in the image.

### PD-2026-007-S027-IMG-001 - Carpenter Location Trail Tease
Abstract night map with a continuous electric-blue location trail leaving a phone, no real streets,
no readable labels, clean space for next-episode text.

## Generation Plan

- Generate Tier hero/A images first: S001, S002, S004, S005, S007, S011, S012, S015, S022, S023, S027.
- Use 4-6 candidates for hero/A beats; 2-3 for B/C beats.
- QC rejects any identifiable face, real-person resemblance, readable logo/text, sensational crime
  imagery, or image that could be mistaken for authentic evidence.
- Register selected assets in the rights manifest with AI disclosure, origin, creator, prompt ref,
  checksum, and verification timestamp before use in edit.
- Do not accept merely usable images. Hero/A selections must feel museum-grade as still frames:
  decisive composition, controlled light, precise subject hierarchy, believable materials, no AI
  gloss, and a clear documentary idea. If the best candidate is only adequate, revise prompt/model/
  seed and regenerate instead of routing it into the edit.
