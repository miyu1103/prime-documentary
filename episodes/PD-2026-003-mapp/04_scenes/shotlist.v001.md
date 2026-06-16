---

# EP3 Mapp v. Ohio — Scene/Shot Plan + SDXL Prompt Sheet
**Episode:** PD-2026-003-mapp | **Script revision:** v001 | **Locked:** 2026-06-17
**Target shots:** 110–116 | **Visual change:** every 4–8s | **Total runtime:** ~720s (~12:00)

---

## SHOT-DENSITY NOTE

Total shots: **114** across 28 narration beats. Visual change rate: one new image every ~4–6s on average. No still holds longer than 6s without a motion layer.

**Motion assignment by type:**
- `parallax` (depth-parallax, 2.5D Remotion, default for rooms/objects/documents/faces) — ~44 shots. Zero warp risk, premium default.
- `kenburns` (slow push or drift, AI stills of architecture and locations) — ~14 shots.
- `runway` (Runway Gen-4, first-frame, one restrained camera move) — ~10 shots. Organic motion only (door forcing, crowd, walking silhouette).
- `remotion` (animated graphics: diagrams, maps, typography, timelines, callouts) — ~34 shots. All data/text content.
- `svd` (SDXL + AnimateDiff/SVD local loop — smoke, light flicker, paper drift) — ~12 shots. Subtle loops, RIFE-interpolated.

**Brand grade applied uniformly:** teal-amber shadow / navy-black base / electric-blue (#1F6BFF) rim / fine 35mm grain / subtle vignette / brand LUT — all sources.

**SDXL stills needed:** 46 distinct images (some reused with different crops). GFX/Remotion shots: 44. Runway clips: 10. No SDXL still required where `SDXL_PROMPT` column reads `[GFX — Remotion]`.

**CLM-0004 BAN guard:** zero shots depict, imply, or approach the seized materials. All search shots show generic period interiors — drawers, trunk, papers, furniture. The word "obscene" never appears on-screen.

---

## BRAND PALETTE CLAUSE (baked into every SDXL prompt)

> deep navy and black environment, electric-blue (#1F6BFF) rim light accent, subtle silver and gold accent highlights, dramatic chiaroscuro, volumetric light shafts, fine cinematic film grain, shallow depth of field, period-accurate 1957 Cleveland / 1961 Washington D.C. mid-century aesthetic, symbolic reconstruction, no identifiable faces, no readable text, no logos, no seals, --ar 16:9

Abbreviated in table below as **[BRAND]**.

---

## SECTION: FLASH-FORWARD HOOK (0:00–0:08) | ~8s | 3 shots

---

### S001 | hook | ~3s | beat: Three officer silhouettes at a front door, nighttime — CLM-0004 / CLM-0001

| field | value |
|---|---|
| **visual_mode** | reenactment |
| **recon_label** | true |
| **onscreen_text** | THREE OFFICERS. ONE DOOR. |
| **source** | STILL+M → parallax |
| **motion** | parallax slow-push in |
| **SFX** | low sub-rumble in |
| **transition** | hard cut in / cut out |

**SDXL_PROMPT:**
Three male silhouettes viewed from behind, standing at the foot of a heavy wooden residential front door, 1950s Cleveland suburb exterior, dusk fading to night, one figure holding a folded paper document at waist height, wide shot low angle looking up toward doorway, shot on ARRI Alexa 35mm anamorphic, shallow depth of field, electric-blue rim light from a street lamp raking across the figures from the right, deep navy sky, volumetric street light haze, dramatic chiaroscuro, crushed blacks in foreground, mid-century brick residential exterior visible at frame edge, fine 35mm cinematic grain, photoreal documentary, symbolic reconstruction, no identifiable faces, no readable text, no logos [BRAND] --ar 16:9

**SDXL_NEG:**
cartoon, cgi, 3d render, illustration, oversaturated, hdr glow, watermark, text, deformed anatomy, extra limbs, fused fingers, plastic skin, nsfw, nudity, suggestive, modern architecture, neon signs, identifiable faces, visible warrant text, visible document text

**fallback:** Wide low-angle exterior shot of a lit doorway — no figures, door ajar, electric-blue light spilling through the gap, depth-parallax

---

### S002 | hook | ~3s | beat: A hand waving a folded paper at a doorway — the fake "warrant" — CLM-0004

| field | value |
|---|---|
| **visual_mode** | object_macro |
| **recon_label** | true |
| **onscreen_text** | A PIECE OF PAPER. |
| **source** | STILL+M → svd light-flicker loop |
| **motion** | svd subtle hand-hold sway |
| **SFX** | paper-rustle; low tension drone |
| **transition** | cut in / cut out |

**SDXL_PROMPT:**
Extreme close-up of a male hand viewed from the side, gripping a folded piece of blank aged paper and extending it outward toward a dark wooden door frame, shallow depth of field with door frame blurred in mid-ground, shot on 50mm macro lens ARRI, hard directional electric-blue side-light from left, deep shadow on right, volumetric dust in the light beam, crushed blacks, mid-century cuff of a plain dark wool suit sleeve just visible, fine 35mm grain, cinematic photoreal documentary, no text visible on paper, no faces, symbolic reconstruction [BRAND] --ar 16:9

**SDXL_NEG:**
cartoon, cgi, 3d, illustration, oversaturated, hdr, watermark, readable text on paper, document writing visible, faces, logos, modern clothing, fused fingers, extra fingers, deformed hand, nsfw, suggestive

**fallback:** Object macro — a blank folded paper on a dark wood surface, blue rim light, depth-parallax

---

### S003 | hook | ~2s | beat: Kinetic impact title — CLM-0001

| field | value |
|---|---|
| **visual_mode** | typography |
| **recon_label** | false |
| **onscreen_text** | THROWN OUT OF COURT. |
| **source** | GFX — Remotion |
| **SDXL_PROMPT** | [GFX — Remotion kinetic punch on black] |
| **motion** | remotion punch-reveal + flash-to-black |
| **SFX** | sub-drop impact |
| **transition** | cut in / flash-to-black out |

**SDXL_NEG:** n/a

---

## SECTION: COLD OPEN (0:08–0:38) | ~30s | 5 shots

---

### S004 | coldopen | ~6s | beat: A home that cannot be protected — the stakes of the question — CLM-0005

| field | value |
|---|---|
| **visual_mode** | establishing |
| **recon_label** | false |
| **onscreen_text** | — |
| **source** | STILL+M → kenburns slow-pull back |
| **motion** | kenburns pull |
| **SFX** | low ambient street; vinyl crackle |
| **transition** | fade in / dissolve |

**SDXL_PROMPT:**
Wide establishing shot of a modest 1950s American two-story residential brick house on a quiet street at dusk, soft warm interior light glowing through curtained windows, mid-century street lamp casting a long shadow on sidewalk, low angle from street level, shot on ARRI Alexa 35mm, deep navy sky with faint amber horizon glow, volumetric street haze, chiaroscuro exterior, no people visible, fine cinematic film grain, photoreal documentary, period-accurate mid-century Cleveland neighborhood, no text, no logos [BRAND] --ar 16:9

**SDXL_NEG:**
cartoon, cgi, 3d, illustration, oversaturated, hdr, watermark, text, logos, modern cars, modern architecture, deformed perspective, people visible

**fallback:** Street lamp and a dark doorstep, kenburns up-drift, no figures

---

### S005 | coldopen | ~6s | beat: The question — police break the rules, can they still use the evidence? — CLM-0005

| field | value |
|---|---|
| **visual_mode** | typography |
| **recon_label** | false |
| **onscreen_text** | IF POLICE BREAK THE RULES — |
| **source** | GFX — Remotion |
| **SDXL_PROMPT** | [GFX — Remotion kinetic question, three-beat reveal on dark texture] |
| **motion** | remotion type-on |
| **SFX** | ui-tick × 3 |
| **transition** | cut in / cut out |

---

### S006 | coldopen | ~6s | beat: Map — United States, most states admit illegally seized evidence before 1961 — CLM-0005 / CLM-0003

| field | value |
|---|---|
| **visual_mode** | map |
| **recon_label** | false |
| **onscreen_text** | BEFORE 1961 — MOST STATES: YES |
| **source** | GFX — Remotion |
| **SDXL_PROMPT** | [GFX — Remotion US map, states shading navy-to-grey "allowed illegal evidence", electric-blue callout ring] |
| **motion** | remotion sweep-fill |
| **SFX** | sweep data-blip |
| **transition** | cut in / cut out |

---

### S007 | coldopen | ~6s | beat: The scales — the right exists on paper and nowhere else — CLM-0005

| field | value |
|---|---|
| **visual_mode** | object_macro |
| **recon_label** | false |
| **onscreen_text** | — |
| **source** | STILL+M → parallax |
| **motion** | parallax slow |
| **SFX** | low tension drone |
| **transition** | cut in / dissolve |

**SDXL_PROMPT:**
Close-up macro of an antique brass balance scale on a dark wooden surface, the two pans unequal — left pan weighed down with a heavy folded parchment document, right pan empty and raised, overhead lamp casting directional chiaroscuro light, volumetric dust, electric-blue rim light from left, deep navy and black background, fine 35mm grain, shallow depth of field, photoreal documentary, no text visible, no logos, symbolic representation of justice imbalance [BRAND] --ar 16:9

**SDXL_NEG:**
cartoon, cgi, 3d, illustration, oversaturated, hdr, watermark, readable text, modern objects, extra elements, deformed geometry, nsfw

**fallback:** Scales GFX diagram in Remotion, same visual concept, animated tilt

---

### S008 | coldopen | ~6s | beat: Kinetic — before 1961 the answer was yes — CLM-0005

| field | value |
|---|---|
| **visual_mode** | typography |
| **recon_label** | false |
| **onscreen_text** | BEFORE 1961, THE ANSWER WAS YES. |
| **source** | GFX — Remotion |
| **SDXL_PROMPT** | [GFX — Remotion, statement-reveal on dark texture, then cut hard] |
| **motion** | remotion reveal |
| **SFX** | low boom |
| **transition** | cut in / cut to black |

---

## SECTION: OPENING (0:38–1:35) | ~57s | 7 shots

---

### S009 | opening | ~8s | beat: The Fourth Amendment parchment — the right that had no teeth — CLM-0005

| field | value |
|---|---|
| **visual_mode** | object_macro |
| **recon_label** | false |
| **onscreen_text** | 1791 |
| **source** | STILL+M → parallax |
| **motion** | parallax push-in slow |
| **SFX** | paper rustle; ambient organ low |
| **transition** | fade in / dissolve |

**SDXL_PROMPT:**
Extreme close-up of an aged amber-toned parchment document, heavy texture and foxing, quill-scratched ink lines visible as abstract decorative marks but no legible words or letters — the text is intentionally illegible aged script, background is pure deep navy black, overhead directional lamp with electric-blue rim accent, volumetric dust particles in the light shaft, shallow depth of field, fine 35mm cinematic grain, photoreal documentary, the document reads as a historical constitutional artifact, no readable text, no seal, no logo [BRAND] --ar 16:9

**SDXL_NEG:**
cartoon, cgi, 3d, illustration, readable text, readable letters, watermark, logos, seals, modern paper, clean edges, white background, oversaturated, hdr, extra objects

**fallback:** Remotion-rendered parchment texture with animated ink-line abstract motif, no legible text

---

### S010 | opening | ~8s | beat: Cleveland skyline 1957 — locating the story — CLM-0004

| field | value |
|---|---|
| **visual_mode** | establishing |
| **recon_label** | false |
| **onscreen_text** | CLEVELAND, OHIO — 1957 |
| **source** | STILL+M → kenburns |
| **motion** | kenburns slow right-drift |
| **SFX** | period ambient; light traffic |
| **transition** | dissolve in / cut |

**SDXL_PROMPT:**
Wide establishing shot of a 1950s American Midwest city skyline at golden hour, industrial brick buildings, a modest downtown with mid-century signage shapes blurred and unreadable, low cumulus clouds, warm amber light on rooftops contrasting with deep navy shadows below, a wide shot from a slight elevated angle, shot on ARRI 35mm wide lens, chiaroscuro urban environment, period-accurate mid-century American city, no visible text, no legible signs, no logos, fine cinematic grain, photoreal documentary [BRAND] --ar 16:9

**SDXL_NEG:**
cartoon, cgi, 3d, illustration, oversaturated, hdr, watermark, readable signs, modern buildings, modern vehicles, logos, text, deformed architecture, nsfw

**fallback:** Abstract mid-century urban texture, kenburns, no text

---

### S011 | opening | ~8s | beat: Map — Cleveland, Ohio marked, the site of the search — CLM-0004

| field | value |
|---|---|
| **visual_mode** | map |
| **recon_label** | false |
| **onscreen_text** | CLEVELAND, OHIO |
| **source** | GFX — Remotion |
| **SDXL_PROMPT** | [GFX — Remotion Ohio state map, pin drops on Cleveland, electric-blue callout ring] |
| **motion** | remotion pin-drop |
| **SFX** | soft impact |
| **transition** | cut in / cut |

---

### S012 | opening | ~9s | beat: Dollree Mapp — a figure at a window, not a portrait — CLM-0004

| field | value |
|---|---|
| **visual_mode** | reenactment |
| **recon_label** | true |
| **onscreen_text** | DOLLREE MAPP |
| **source** | STILL+M → parallax |
| **motion** | parallax gentle |
| **SFX** | ambient interior |
| **transition** | dissolve / cut |

**SDXL_PROMPT:**
A female figure seen from behind, standing at a curtained window of a modest 1950s interior, looking outward, silhouetted by soft daylight filtering through lace curtains, medium shot from inside the room, shot on ARRI Alexa 35mm, warm amber window light against deep navy room interior, electric-blue rim accent from a hallway lamp off-frame left, chiaroscuro, fine 35mm grain, shallow depth of field, period-accurate mid-century American interior — wood furniture, plaster walls, linoleum floor, symbolic reconstruction, no identifiable face, no logos, no text visible [BRAND] --ar 16:9

**SDXL_NEG:**
cartoon, cgi, 3d, illustration, face visible, identifiable likeness, modern clothing, modern furniture, oversaturated, hdr, watermark, text, logos, nsfw, nudity, suggestive content of any kind, extra limbs

**fallback:** Window with lace curtains backlit, no figure, depth-parallax, warm amber glow

---

### S013 | opening | ~8s | beat: Timeline diagram — 1791 Fourth Amendment to 1957 Cleveland — CLM-0005

| field | value |
|---|---|
| **visual_mode** | diagram |
| **recon_label** | false |
| **onscreen_text** | 1791 → 1957 → 1961 |
| **source** | GFX — Remotion |
| **SDXL_PROMPT** | [GFX — Remotion horizontal timeline, three nodes animate on: "4th Amendment 1791" / "Cleveland 1957" / "Supreme Court 1961", navy-black, electric-blue nodes, gold accent line] |
| **motion** | remotion draw-on left to right |
| **SFX** | ui-tick × 3 |
| **transition** | cut in / cut |

---

### S014 | opening | ~8s | beat: The exclusionary rule — what changed — CLM-0001

| field | value |
|---|---|
| **visual_mode** | typography |
| **recon_label** | false |
| **onscreen_text** | THE RULE THAT MADE IT REAL |
| **source** | GFX — Remotion |
| **SDXL_PROMPT** | [GFX — Remotion kinetic reveal on brand texture] |
| **motion** | remotion reveal |
| **SFX** | low boom |
| **transition** | cut / dissolve to Act I |

---

### S015 | opening | ~8s | beat: Viewer promise — door, warrant, Supreme Court — CLM-0001 / CLM-0009

| field | value |
|---|---|
| **visual_mode** | establishing |
| **recon_label** | false |
| **onscreen_text** | — |
| **source** | STILL+M → kenburns |
| **motion** | kenburns push-in to door |
| **SFX** | ambient street; swell |
| **transition** | dissolve / cut to Act I |

**SDXL_PROMPT:**
Wide shot of the exterior of a 1950s American residential house front door at evening, slightly elevated angle from the sidewalk, the door is closed and solid, warm amber porch light above the door, deep navy sky behind, empty front steps, lush mid-century landscaping flanking the stoop, shot on ARRI 35mm, shallow depth of field on the door, volumetric haze, fine 35mm grain, chiaroscuro, electric-blue lamp light from an unseen street lamp raking across the door from the right, no people, no text, no logos, symbolic establishing shot [BRAND] --ar 16:9

**SDXL_NEG:**
cartoon, cgi, 3d, illustration, oversaturated, hdr, watermark, text, logos, modern architecture, people, faces, nsfw

**fallback:** Same door image used in S001, different crop, kenburns in

---

## SECTION: ACT I — THE DOOR (1:35–3:40) | ~125s | 18 shots

---

### S016 | act1 | ~6s | beat: May 23, 1957 — calendar moment, Cleveland afternoon — CLM-0004

| field | value |
|---|---|
| **visual_mode** | typography |
| **recon_label** | false |
| **onscreen_text** | MAY 23, 1957 |
| **source** | GFX — Remotion |
| **SDXL_PROMPT** | [GFX — Remotion date stamp reveal on amber-tinted paper texture] |
| **motion** | remotion stamp-reveal |
| **SFX** | soft impact; pencil-scratch ambient |
| **transition** | fade in / cut |

---

### S017 | act1 | ~6s | beat: Dollree Mapp's house — upper floor — Cleveland afternoon — CLM-0004

| field | value |
|---|---|
| **visual_mode** | establishing |
| **recon_label** | false |
| **onscreen_text** | — |
| **source** | STILL+M → kenburns |
| **motion** | kenburns tilt up to upper floor |
| **SFX** | afternoon ambience; wind |
| **transition** | cut / cut |

**SDXL_PROMPT:**
Medium-wide establishing exterior shot of a modest 1950s Cleveland two-story brick house, afternoon daylight, upper floor windows with lace curtains catching the warm afternoon light, the lower front door visible in frame, period-accurate neighborhood context — parked 1950s-era automobiles shapes barely visible at frame edge, shot on ARRI Alexa 35mm, warm side-light raking across the brickwork creating deep shadows, electric-blue sky accent visible above roofline, fine 35mm grain, chiaroscuro, documentary photoreal, no readable text, no logos [BRAND] --ar 16:9

**SDXL_NEG:**
cartoon, cgi, 3d, illustration, oversaturated, hdr, watermark, logos, readable text, modern cars clearly visible, modern architecture, people visible, faces, nsfw

**fallback:** Architecture texture close-up, brick pattern, kenburns

---

### S018 | act1 | ~5s | beat: Officers arriving at the door — three figures walking up the path — CLM-0004

| field | value |
|---|---|
| **visual_mode** | reenactment |
| **recon_label** | true |
| **onscreen_text** | SYMBOLIC RECONSTRUCTION |
| **source** | CLIP → runway (subtle walk, first-frame) |
| **motion** | runway slow dolly-back revealing three figures walking |
| **SFX** | footsteps on pavement |
| **transition** | cut / cut |

**SDXL_PROMPT (first-frame for Runway):**
Three male figures seen from behind in medium-wide shot, walking up a concrete front path toward a 1950s residential front door, afternoon light, dark suit trousers and jackets, no faces visible, one figure slightly ahead, shot on ARRI Alexa 35mm, warm amber afternoon side-light from the right creating long cast shadows on the path, deep navy shadows in doorway, volumetric afternoon haze, fine 35mm grain, chiaroscuro, documentary photoreal, symbolic reconstruction, no identifiable faces, no text, no logos [BRAND] --ar 16:9

**SDXL_NEG:**
cartoon, cgi, 3d, illustration, faces visible, identifiable people, oversaturated, hdr, watermark, text, logos, modern clothing, modern context, weapons, nsfw

**fallback:** Three-silhouette still, depth-parallax, no clip

---

### S019 | act1 | ~5s | beat: Knocking — a closed door, a hand raised — CLM-0004

| field | value |
|---|---|
| **visual_mode** | object_macro |
| **recon_label** | true |
| **onscreen_text** | — |
| **source** | STILL+M → svd knock-motion loop |
| **motion** | svd light-flicker on door surface |
| **SFX** | three deliberate knocks |
| **transition** | cut / cut |

**SDXL_PROMPT:**
Extreme close-up of a fist raised to knock on a heavy 1950s residential wooden front door, shot from outside looking at the door, medium macro shot, the knuckles caught in hard side-light from the right creating dramatic chiaroscuro on the wood grain and the hand, electric-blue rim on door edge, deep shadow to the left, dust particles in the light shaft, shallow depth of field, fine 35mm grain, photoreal documentary, no face visible, no text, no logos, symbolic reconstruction [BRAND] --ar 16:9

**SDXL_NEG:**
cartoon, cgi, 3d, illustration, face visible, weapon, deformed hand, extra fingers, fused fingers, oversaturated, hdr, watermark, text, logos, modern door, nsfw

**fallback:** Plain door close-up still, depth-parallax, no hand

---

### S020 | act1 | ~5s | beat: Mapp calls her attorney — a period telephone, a hand reaching — CLM-0004

| field | value |
|---|---|
| **visual_mode** | object_macro |
| **recon_label** | true |
| **onscreen_text** | SHE CALLS HER ATTORNEY. |
| **source** | STILL+M → parallax |
| **motion** | parallax slow |
| **SFX** | dial-tone; period telephone ring |
| **transition** | cut / dissolve |

**SDXL_PROMPT:**
Close-up of a 1950s black Bakelite rotary telephone on a small side table, a female hand lifting the handset, shallow depth of field, the table surface is a warm mid-century wood, soft interior lamp light from above casting a warm glow on the handset, electric-blue rim light from a window off-frame, deep navy shadow behind the phone, fine 35mm grain, chiaroscuro, photoreal documentary, no face visible, no text on dial, no logos [BRAND] --ar 16:9

**SDXL_NEG:**
cartoon, cgi, 3d, illustration, modern phone, smartphone, face visible, deformed hand, extra fingers, fused fingers, oversaturated, hdr, watermark, text, logos, nsfw

**fallback:** Still of rotary phone on table, depth-parallax, no hand

---

### S021 | act1 | ~5s | beat: Officers waiting outside — silhouettes on the front step — CLM-0004

| field | value |
|---|---|
| **visual_mode** | reenactment |
| **recon_label** | true |
| **onscreen_text** | THEY WAIT. |
| **source** | STILL+M → parallax |
| **motion** | parallax slow-out |
| **SFX** | ambient exterior; low tension drone |
| **transition** | dissolve / cut |

**SDXL_PROMPT:**
Wide medium shot from inside a darkened interior looking outward through a slightly parted curtain toward a front stoop where three male figures stand waiting in low evening light, their silhouettes lit from behind by an amber street lamp, the window frame creates a compositional border, deep shadow in foreground, electric-blue sky behind the figures, fine 35mm grain, chiaroscuro, photoreal documentary, symbolic reconstruction, no identifiable faces, no text, no logos [BRAND] --ar 16:9

**SDXL_NEG:**
cartoon, cgi, 3d, illustration, face visible, identifiable people, oversaturated, hdr, watermark, text, logos, modern context, nsfw

**fallback:** Looking outward through parted curtain — wide exterior, no figures, depth-parallax

---

### S022 | act1 | ~5s | beat: They go in anyway — a door forced open, threshold crossed — CLM-0004

| field | value |
|---|---|
| **visual_mode** | reenactment |
| **recon_label** | true |
| **onscreen_text** | SYMBOLIC RECONSTRUCTION |
| **source** | CLIP → runway (door-force push, one move) |
| **motion** | runway slow push-in as door swings open |
| **SFX** | door-crack; low boom |
| **transition** | cut / cut |

**SDXL_PROMPT (first-frame for Runway):**
Interior of a 1950s American home entry hall viewed from the inside, the front door half-open letting a shaft of electric-blue cold evening light spill across a wood floor, three silhouetted male figures framed in the doorway from interior perspective, dramatic backlight creating pure silhouettes with no facial features, hard contrast between the dark interior and the cold bright exterior light, volumetric light shaft across the entry hall floor, fine 35mm grain, chiaroscuro, photoreal documentary, symbolic reconstruction, no identifiable faces, no text, no logos [BRAND] --ar 16:9

**SDXL_NEG:**
cartoon, cgi, 3d, illustration, faces visible, identifiable features, oversaturated, hdr, watermark, text, logos, modern context, weapons, violence, nsfw

**fallback:** Open door with light shaft still, depth-parallax, no figures

---

### S023 | act1 | ~5s | beat: The folded paper raised — the fake warrant moment — CLM-0004

| field | value |
|---|---|
| **visual_mode** | object_macro |
| **recon_label** | true |
| **onscreen_text** | A PIECE OF PAPER — |
| **source** | STILL+M → svd slight-sway loop |
| **motion** | svd subtle paper-sway |
| **SFX** | paper rustle; tension sting |
| **transition** | cut / cut |

**SDXL_PROMPT:**
Close-up of a male hand from below, holding a folded blank aged paper upright, waving it slightly, shot from a low angle looking up, the paper and hand lit by hard overhead directional lamp, deep shadow below, electric-blue rim accent on the left edge of the paper and sleeve, the wall behind is a dark plaster interior, fine 35mm grain, shallow depth of field, chiaroscuro, photoreal documentary, no text visible on paper, no readable content, no face, symbolic reconstruction [BRAND] --ar 16:9

**SDXL_NEG:**
cartoon, cgi, 3d, illustration, readable text on paper, document writing visible, face, identifiable person, extra fingers, fused fingers, deformed hand, oversaturated, hdr, watermark, logos, nsfw

**fallback:** Same as S002 hand-with-paper, different angle crop, no motion

---

### S024 | act1 | ~5s | beat: Mapp grabs for the paper — CLM-0004

| field | value |
|---|---|
| **visual_mode** | reenactment |
| **recon_label** | true |
| **onscreen_text** | — |
| **source** | STILL+M → parallax |
| **motion** | parallax tight push |
| **SFX** | paper-tear rustle; low impact |
| **transition** | cut / cut |

**SDXL_PROMPT:**
Dramatic close-up macro of two pairs of hands — one female reaching forward from the left, one male pulling back from the right — both gripping the edges of a folded blank aged paper, mid-tug, sharp tension in the hands, neither hand with a face visible, shot on ARRI 50mm macro, hard directional top-light, electric-blue rim from left, deep navy shadow right, fine 35mm grain, shallow depth of field, chiaroscuro, photoreal documentary, symbolic reconstruction, no text on paper, no logos [BRAND] --ar 16:9

**SDXL_NEG:**
cartoon, cgi, 3d, illustration, face visible, readable text, logos, deformed hands, extra fingers, fused fingers, oversaturated, hdr, watermark, violence, nsfw

**fallback:** Two-hands macro still, depth-parallax, no motion

---

### S025 | act1 | ~6s | beat: Diagram — what a REAL warrant is: judge, probable cause, written authorization — CLM-0004

| field | value |
|---|---|
| **visual_mode** | diagram |
| **recon_label** | false |
| **onscreen_text** | WARRANT = JUDGE + PROBABLE CAUSE |
| **source** | GFX — Remotion |
| **SDXL_PROMPT** | [GFX — Remotion diagram: three-node flow "Police → Judge → Written Authorization", navy-black, electric-blue nodes, gold connecting line, all text in brand font] |
| **motion** | remotion draw-on sequentially |
| **SFX** | ui-tick × 3 |
| **transition** | cut / cut |

---

### S026 | act1 | ~5s | beat: A judge signing a real warrant — the genuine article — CLM-0004

| field | value |
|---|---|
| **visual_mode** | reenactment |
| **recon_label** | true |
| **onscreen_text** | THE REAL THING — |
| **source** | STILL+M → svd pen-motion loop |
| **motion** | svd subtle hand-writing sway |
| **SFX** | pen-scratch; room tone |
| **transition** | cut / cut |

**SDXL_PROMPT:**
Close-up macro of a judge's hand in a dark robe sleeve writing with a fountain pen on an aged blank document, shot from a high angle looking down, the document is on a heavy dark wood desk, directional lamp from upper right creating a hard beam across the document surface, volumetric dust, electric-blue rim accent on the pen and sleeve edge, deep navy shadow to the left, fine 35mm grain, shallow depth of field, chiaroscuro, photoreal documentary, symbolic reconstruction, no legible text on document, no readable words, no logos, no seals [BRAND] --ar 16:9

**SDXL_NEG:**
cartoon, cgi, 3d, illustration, readable text, legible document, seals, logos, face visible, extra fingers, fused fingers, deformed hand, oversaturated, hdr, watermark, nsfw

**fallback:** Pen on blank document still, depth-parallax, no hand

---

### S027 | act1 | ~5s | beat: The house searched — period interior (basement/rooms/drawers, generic) — CLM-0004 / BAN-guard

| field | value |
|---|---|
| **visual_mode** | establishing |
| **recon_label** | false |
| **onscreen_text** | — |
| **source** | STILL+M → kenburns |
| **motion** | kenburns slow-tilt up |
| **SFX** | interior ambient; low tension bed |
| **transition** | cut / cut |

**SDXL_PROMPT:**
Wide interior shot of a cluttered 1950s American residential basement storage room, cardboard boxes stacked against stone walls, a wooden trunk in the foreground, general household items — old magazines, a standing lamp, wooden furniture — nothing specific visible or legible, the space illuminated by a single hanging bare bulb creating hard top-down chiaroscuro, electric-blue rim accent from a small basement window, fine 35mm grain, shallow depth of field on the trunk, deep shadows in corners, photoreal documentary, no people visible, no text legible, no logos, CLM-0004 BAN: generic storage items only, nothing sexual or suggestive [BRAND] --ar 16:9

**SDXL_NEG:**
cartoon, cgi, 3d, illustration, people visible, faces, suggestive material, sexual content, nsfw, nudity, nudity-adjacent, magazines with visible images, posters, identifiable content, readable text, oversaturated, hdr, watermark, logos, modern objects

**fallback:** Abstract shadow interior — bare stone wall, single lamp cone of light, kenburns, no objects visible

---

### S028 | act1 | ~5s | beat: The arrest — Mapp is led out, not the bombing suspect — CLM-0004

| field | value |
|---|---|
| **visual_mode** | reenactment |
| **recon_label** | true |
| **onscreen_text** | NOT THE BOMBING SUSPECT. |
| **source** | STILL+M → parallax |
| **motion** | parallax pull-back |
| **SFX** | footsteps; door close |
| **transition** | cut / cut |

**SDXL_PROMPT:**
Medium-wide shot from behind of a female figure walking through a doorway being guided by a male figure alongside, viewed from outside the house, afternoon light, the door frame creates a compositional border, the female figure's back and dark 1950s dress visible, no faces, one hand of the male figure visible at her elbow guiding not grasping, soft warm afternoon light behind them, electric-blue rim accent from a car headlight off-frame, fine 35mm grain, chiaroscuro, photoreal documentary, symbolic reconstruction, no identifiable faces, no text, no logos [BRAND] --ar 16:9

**SDXL_NEG:**
cartoon, cgi, 3d, illustration, faces visible, handcuffs depicted graphically, violence, oversaturated, hdr, watermark, text, logos, modern clothing, nsfw

**fallback:** A coat rack with a woman's coat and hat, door open behind it, depth-parallax, no figures

---

### S029 | act1 | ~5s | beat: The conviction that reaches SCOTUS — not the bombing — CLM-0004

| field | value |
|---|---|
| **visual_mode** | typography |
| **recon_label** | false |
| **onscreen_text** | NOT THE BOMBING — THE SEARCH. |
| **source** | GFX — Remotion |
| **SDXL_PROMPT** | [GFX — Remotion two-line reveal, first line strikethrough then second line, on brand texture] |
| **motion** | remotion sequential strike-reveal |
| **SFX** | low boom |
| **transition** | cut / fade to black |

---

### S030 | act1 | ~5s | beat: Act I cliffhanger — she has to lose first — tension breath shot — CLM-0004

| field | value |
|---|---|
| **visual_mode** | object_macro |
| **recon_label** | false |
| **onscreen_text** | — |
| **source** | STILL+M → svd light-flicker |
| **motion** | svd subtle flicker of courtroom lamp |
| **SFX** | heartbeat sub-drone |
| **transition** | dissolve / cut |

**SDXL_PROMPT:**
Extreme close-up macro of a wooden gavel resting on its block on a dark mahogany judge's bench, viewed from a very low angle at desk level, hard overhead directional light illuminating the gavel head from above, electric-blue rim accent on the gavel edge from a lamp off-frame, deep navy shadow filling the lower frame, fine 35mm grain, shallow depth of field, volumetric dust, chiaroscuro, photoreal documentary, no people, no text, no logos [BRAND] --ar 16:9

**SDXL_NEG:**
cartoon, cgi, 3d, illustration, oversaturated, hdr, watermark, text, logos, faces, modern court, nsfw

**fallback:** Gavel still, depth-parallax, no motion

---

### S031 | act1 | ~5s | beat: Act I close — the gap in law that most people never knew existed — CLM-0005

| field | value |
|---|---|
| **visual_mode** | typography |
| **recon_label** | false |
| **onscreen_text** | A GAP IN AMERICAN LAW. |
| **source** | GFX — Remotion |
| **SDXL_PROMPT** | [GFX — Remotion phrase-reveal, brand texture, cut to black] |
| **motion** | remotion fade-punch |
| **SFX** | sub-drop |
| **transition** | cut / fade to black |

---

## SECTION: ACT II — THE GAP (3:40–6:00) | ~140s | 16 shots

---

### S032 | act2 | ~7s | beat: Wolf v. Colorado — the 1949 case that opened the gap — CLM-0003

| field | value |
|---|---|
| **visual_mode** | typography |
| **recon_label** | false |
| **onscreen_text** | WOLF v. COLORADO — 1949 |
| **source** | GFX — Remotion |
| **SDXL_PROMPT** | [GFX — Remotion case-title reveal with year stamp, on cracked stone/parchment texture, electric-blue underline] |
| **motion** | remotion type-on |
| **SFX** | stone-thud; low boom |
| **transition** | fade in / cut |

---

### S033 | act2 | ~7s | beat: The gap diagram — Fourth Amendment applies to states but no remedy — CLM-0003

| field | value |
|---|---|
| **visual_mode** | diagram |
| **recon_label** | false |
| **onscreen_text** | RIGHT: YES. REMEDY: NO. |
| **source** | GFX — Remotion |
| **SDXL_PROMPT** | [GFX — Remotion split visual: left panel "4th Amendment" with green check, right panel "Exclusionary Rule" with red X, then a gap/void between, brand colors] |
| **motion** | remotion panel-reveal |
| **SFX** | ui-tick × 2; void-hum |
| **transition** | cut / cut |

---

### S034 | act2 | ~7s | beat: SCOTUS chamber 1949 — the Wolf decision — CLM-0003

| field | value |
|---|---|
| **visual_mode** | establishing |
| **recon_label** | false |
| **onscreen_text** | — |
| **source** | STILL+M → parallax |
| **motion** | parallax slow |
| **SFX** | chamber ambience; low organ tone |
| **transition** | cut / dissolve |

**SDXL_PROMPT:**
Wide interior shot of a formal 1940s-era American Supreme Court hearing chamber, empty of people, the bench a long curved mahogany surface under high coffered ceilings, heavy draped curtains to the left, a row of formal leather chairs, overhead skylights casting god-rays of pale gold light onto the bench, electric-blue accent from a side window, deep shadow in the gallery, fine 35mm grain, shallow depth of field, chiaroscuro, photoreal documentary, no people, no text visible, no logos, no seals, period-accurate 1940s Federal architecture [BRAND] --ar 16:9

**SDXL_NEG:**
cartoon, cgi, 3d, illustration, people visible, faces, oversaturated, hdr, watermark, text, logos, readable seals, modern elements, nsfw

**fallback:** Column detail close-up, marble texture, kenburns, no chamber

---

### S035 | act2 | ~7s | beat: States were free to choose — a patchwork legal map — CLM-0003

| field | value |
|---|---|
| **visual_mode** | map |
| **recon_label** | false |
| **onscreen_text** | STATES CHOSE DIFFERENTLY |
| **source** | GFX — Remotion |
| **SDXL_PROMPT** | [GFX — Remotion US state map, some states shade one color "used evidence", others different color "excluded it", electric-blue callout, legend, navy-black background] |
| **motion** | remotion staggered state-fill |
| **SFX** | data-blip × n |
| **transition** | cut / cut |

---

### S036 | act2 | ~7s | beat: 1914 — Weeks v. United States — the federal exclusionary rule — CLM-0008

| field | value |
|---|---|
| **visual_mode** | typography |
| **recon_label** | false |
| **onscreen_text** | WEEKS v. UNITED STATES — 1914 |
| **source** | GFX — Remotion |
| **SDXL_PROMPT** | [GFX — Remotion case-title reveal on aged parchment texture, gold underline, year stamp] |
| **motion** | remotion type-on |
| **SFX** | paper-turn; soft impact |
| **transition** | cut / cut |

---

### S037 | act2 | ~7s | beat: Federal court 1914 — the exclusionary rule born — CLM-0008

| field | value |
|---|---|
| **visual_mode** | establishing |
| **recon_label** | false |
| **onscreen_text** | — |
| **source** | STILL+M → kenburns |
| **motion** | kenburns slow tilt up |
| **SFX** | period ambience; quiet |
| **transition** | cut / cut |

**SDXL_PROMPT:**
Wide exterior establishing shot of a 1910s-era Neoclassical Federal courthouse, grand stone steps leading to tall Corinthian columns, pale limestone catching early morning sunlight from the right, deep navy sky, chiaroscuro on the column shadows, the building reads as authoritative and Federal, shot on ARRI 35mm wide angle, fine 35mm grain, no people on steps, electric-blue accent from sky, no text on the building readable, no logos, photoreal documentary [BRAND] --ar 16:9

**SDXL_NEG:**
cartoon, cgi, 3d, illustration, readable text on building, logos, seals, people, faces, oversaturated, hdr, watermark, modern context, nsfw

**fallback:** Column detail macro, stone texture, kenburns, no building

---

### S038 | act2 | ~7s | beat: The exclusionary rule logic — diagram — court cannot be a participant — CLM-0006

| field | value |
|---|---|
| **visual_mode** | diagram |
| **recon_label** | false |
| **onscreen_text** | ILLEGAL SEARCH → COURT → CONVICTION = COURT PARTICIPATES |
| **source** | GFX — Remotion |
| **SDXL_PROMPT** | [GFX — Remotion three-node flow with a red-crossed X breaking the chain at step 2, brand colors, electric-blue accent] |
| **motion** | remotion draw-on then X reveal |
| **SFX** | data-blip; low boom on X |
| **transition** | cut / cut |

---

### S039 | act2 | ~7s | beat: Ohio state courtroom — Mapp's case is a state matter — CLM-0004 / CLM-0003

| field | value |
|---|---|
| **visual_mode** | establishing |
| **recon_label** | false |
| **onscreen_text** | STATE COURT — NOT FEDERAL |
| **source** | STILL+M → parallax |
| **motion** | parallax gentle push |
| **SFX** | courtroom ambience |
| **transition** | cut / dissolve |

**SDXL_PROMPT:**
Wide interior shot of a 1950s Ohio state courtroom, the gallery benches empty and dark, the judge's elevated bench at the far end, fluorescent lights overhead mixing with daylight from tall side windows, American mid-century Midwestern public architecture, wood paneling, an American flag partially visible but not readable at frame edge, shot on ARRI 35mm, chiaroscuro from high windows, electric-blue rim on bench from window light, fine 35mm grain, no people, no readable text, no logos, photoreal documentary [BRAND] --ar 16:9

**SDXL_NEG:**
cartoon, cgi, 3d, illustration, faces, people, oversaturated, hdr, readable text, logos, readable seals, readable flags, modern courtroom, nsfw

**fallback:** Bench close-up still, wood grain, depth-parallax

---

### S040 | act2 | ~6s | beat: Wolf allowed — Ohio used the evidence — CLM-0003 / CLM-0004

| field | value |
|---|---|
| **visual_mode** | typography |
| **recon_label** | false |
| **onscreen_text** | OHIO: ALLOWED. |
| **source** | GFX — Remotion |
| **SDXL_PROMPT** | [GFX — Remotion single-word reveal, stamped on map texture, yellow underline] |
| **motion** | remotion stamp |
| **SFX** | stamp impact |
| **transition** | cut / cut |

---

### S041 | act2 | ~6s | beat: Mapp convicted — Ohio Supreme Court upholds — CLM-0004

| field | value |
|---|---|
| **visual_mode** | reenactment |
| **recon_label** | true |
| **onscreen_text** | CONVICTED. APPEALED. UPHELD. |
| **source** | GFX — Remotion |
| **SDXL_PROMPT** | [GFX — Remotion three-word sequential stamp reveal on aged paper texture] |
| **motion** | remotion stamp ×3 |
| **SFX** | stamp × 3; low boom |
| **transition** | cut / cut |

---

### S042 | act2 | ~6s | beat: Washington — the case goes to SCOTUS — CLM-0002

| field | value |
|---|---|
| **visual_mode** | map |
| **recon_label** | false |
| **onscreen_text** | CLEVELAND → WASHINGTON, D.C. |
| **source** | GFX — Remotion |
| **SDXL_PROMPT** | [GFX — Remotion US map, animated travel line from Cleveland dot to Washington D.C. dot, electric-blue trail, gold terminal dot] |
| **motion** | remotion travel-line draw |
| **SFX** | sweep |
| **transition** | cut / cut |

---

### S043 | act2 | ~6s | beat: SCOTUS exterior — the case arrives — CLM-0002

| field | value |
|---|---|
| **visual_mode** | establishing |
| **recon_label** | false |
| **onscreen_text** | — |
| **source** | STILL+M → kenburns |
| **motion** | kenburns slow pull-back from columns |
| **SFX** | DC ambience; wind on marble |
| **transition** | cut / cut |

**SDXL_PROMPT:**
Wide exterior shot of the United States Supreme Court Building, Washington D.C., the Neoclassical white marble facade viewed slightly below eye level from the plaza, the "Equal Justice Under Law" frieze intentionally blurred and unreadable, overcast morning light from the left with volumetric cloud shadows on the marble, the tall Corinthian columns casting deep shadows, electric-blue sky above, fine 35mm grain, chiaroscuro, photoreal documentary, no people, no readable text, no logos [BRAND] --ar 16:9

**SDXL_NEG:**
cartoon, cgi, 3d, illustration, readable text on building, readable frieze, logos, flags readable, people, faces, oversaturated, hdr, watermark, nsfw

**fallback:** Single column detail at SCOTUS, marble close-up, kenburns, no full building

---

### S044 | act2 | ~7s | beat: Attorneys arguing a different question — exclusionary rule almost an afterthought — CLM-0003

| field | value |
|---|---|
| **visual_mode** | reenactment |
| **recon_label** | true |
| **onscreen_text** | THE BIGGER QUESTION — ALMOST MISSED |
| **source** | STILL+M → parallax |
| **motion** | parallax slow |
| **SFX** | chamber ambience; low tension |
| **transition** | cut / cut |

**SDXL_PROMPT:**
Interior of a formal Supreme Court chamber, a single standing figure at a lectern viewed from behind and side in silhouette, addressing a long curved bench in the far background that is in deep shadow, overhead god-rays of pale light from high windows, the space reads as vast and formal, the figure is small against the chamber scale, shot on ARRI 35mm wide, electric-blue accent from high side windows, fine 35mm grain, chiaroscuro, photoreal documentary, symbolic reconstruction, no identifiable faces, no text visible, no logos [BRAND] --ar 16:9

**SDXL_NEG:**
cartoon, cgi, 3d, illustration, identifiable faces, oversaturated, hdr, watermark, readable text, logos, seals, modern clothing, nsfw

**fallback:** SCOTUS chamber interior still with no figures, depth-parallax

---

### S045 | act2 | ~5s | beat: Act II cliffhanger — the Court is about to do something nobody anticipated — CLM-0001

| field | value |
|---|---|
| **visual_mode** | typography |
| **recon_label** | false |
| **onscreen_text** | A MUCH LARGER QUESTION. |
| **source** | GFX — Remotion |
| **SDXL_PROMPT** | [GFX — Remotion phrase reveal, then pause, cut to black] |
| **motion** | remotion slow reveal; fade to black |
| **SFX** | sub-riser then cut |
| **transition** | cut / fade to black |

---

### S046 | act2 | ~5s | beat: Tension breath — scales in empty chamber — CLM-0001

| field | value |
|---|---|
| **visual_mode** | abstract |
| **recon_label** | false |
| **onscreen_text** | — |
| **source** | STILL+M → svd light-flicker loop |
| **motion** | svd dust drift |
| **SFX** | sub-drone; heartbeat sub-low |
| **transition** | dissolve / fade to black |

**SDXL_PROMPT:**
Abstract composition — a single brass balance scale seen in extreme silhouette at center frame on a dark surface, a perfectly balanced scale pan on each side, lit by a single overhead spot from above creating a god-ray, deep navy and black environment, electric-blue rim light on the scale's central column from the left, volumetric dust drifting in the light shaft, negative space dominant, fine 35mm grain, shallow depth of field, chiaroscuro, photoreal documentary, no text, no logos [BRAND] --ar 16:9

**SDXL_NEG:**
cartoon, cgi, 3d, illustration, people, faces, oversaturated, hdr, watermark, text, logos, extra objects, cluttered background, nsfw

**fallback:** Same scale image from S007, different tighter crop, svd light-flicker

---

## SECTION: ACT III — THE RULING (6:00–8:10) | ~130s | 14 shots

---

### S047 | act3 | ~7s | beat: June 19, 1961 — the date card — CLM-0002

| field | value |
|---|---|
| **visual_mode** | typography |
| **recon_label** | false |
| **onscreen_text** | JUNE 19, 1961 |
| **source** | GFX — Remotion |
| **SDXL_PROMPT** | [GFX — Remotion date stamp reveal, electric-blue, bold, on black — impact cut] |
| **motion** | remotion stamp-reveal |
| **SFX** | reveal sting |
| **transition** | fade in / cut |

---

### S048 | act3 | ~7s | beat: Justice Clark — opinion writer — symbolic figure at the bench — CLM-0002

| field | value |
|---|---|
| **visual_mode** | reenactment |
| **recon_label** | true |
| **onscreen_text** | JUSTICE TOM C. CLARK |
| **source** | STILL+M → parallax |
| **motion** | parallax gentle |
| **SFX** | pen-scratch; room tone |
| **transition** | cut / dissolve |

**SDXL_PROMPT:**
Medium shot of a robed judicial figure seen from the side and slightly behind, seated at an elevated bench and writing with a fountain pen, the figure's face turned downward toward the desk and not visible, heavy dark judicial robes, the bench is dark mahogany, an overhead lamp illuminates the desk surface, electric-blue rim light from a high side window, deep shadow in the background, volumetric dust, fine 35mm grain, shallow depth of field, chiaroscuro, photoreal documentary, symbolic reconstruction, no identifiable likeness, no text visible, no logos [BRAND] --ar 16:9

**SDXL_NEG:**
cartoon, cgi, 3d, illustration, identifiable face, identifiable likeness, modern elements, readable text, logos, seals, oversaturated, hdr, watermark, nsfw

**fallback:** Judicial pen-on-desk macro, depth-parallax, no figure

---

### S049 | act3 | ~7s | beat: Over three dissents — vote diagram — CLM-0002

| field | value |
|---|---|
| **visual_mode** | diagram |
| **recon_label** | false |
| **onscreen_text** | REVERSED — OVER 3 DISSENTS |
| **source** | GFX — Remotion |
| **SDXL_PROMPT** | [GFX — Remotion vote tally: majority seats light electric-blue, three seats dark/navy "dissent", annotation "over 3 dissents", brand colors — never labeled "5-4" or "9-0"] |
| **motion** | remotion seat-reveal sequential |
| **SFX** | data-blip × n |
| **transition** | cut / cut |

---

### S050 | act3 | ~6s | beat: Wolf overruled — 12-year loophole closed — CLM-0003

| field | value |
|---|---|
| **visual_mode** | typography |
| **recon_label** | false |
| **onscreen_text** | WOLF v. COLORADO — OVERRULED |
| **source** | GFX — Remotion |
| **SDXL_PROMPT** | [GFX — Remotion case name with animated strikethrough, then "OVERRULED" stamp, brand texture] |
| **motion** | remotion strikethrough then stamp |
| **SFX** | stone-crumble; low boom |
| **transition** | cut / cut |

---

### S051 | act3 | ~7s | beat: A single principle — the real remedy — parchment and light — CLM-0006

| field | value |
|---|---|
| **visual_mode** | object_macro |
| **recon_label** | false |
| **onscreen_text** | A REAL RIGHT. A REAL REMEDY. |
| **source** | STILL+M → parallax |
| **motion** | parallax push-in |
| **SFX** | low tone bed |
| **transition** | cut / dissolve |

**SDXL_PROMPT:**
Close-up macro of the Fourth Amendment parchment from S009 (reuse same asset, new crop), zoomed to center, the aged abstract ink marks suggesting text but entirely illegible, a single beam of electric-blue light now crosses the document from the left, the light illuminating only a central band of the parchment while edges fall to deep shadow, fine 35mm grain, extreme shallow depth of field, chiaroscuro, photoreal documentary, no readable text, no logos [BRAND] --ar 16:9

**SDXL_NEG:**
cartoon, cgi, 3d, illustration, readable text, legible words, logos, seals, faces, oversaturated, hdr, watermark, nsfw

**fallback:** Light-beam-on-texture abstract still, svd light drift

---

### S052 | act3 | ~7s | beat: "A form of words" — the Court's reasoning — CLM-0006

| field | value |
|---|---|
| **visual_mode** | typography |
| **recon_label** | false |
| **onscreen_text** | "A FORM OF WORDS" |
| **source** | GFX — Remotion |
| **SDXL_PROMPT** | [GFX — Remotion quote card — quotation marks appear first, then the phrase typesets slowly inside, brand monospace, gold quote marks, electric-blue phrase, parchment texture underlay] |
| **motion** | remotion type-on |
| **SFX** | pen-scratch typewriter-style |
| **transition** | cut / cut |

---

### S053 | act3 | ~7s | beat: Deterrence logic — police won't break the rules without consequence — CLM-0006

| field | value |
|---|---|
| **visual_mode** | diagram |
| **recon_label** | false |
| **onscreen_text** | BREAK THE RULES → LOSE THE CASE |
| **source** | GFX — Remotion |
| **SDXL_PROMPT** | [GFX — Remotion two-node cause-effect diagram, "illegal search" arrow to "evidence excluded" arrow to "police follow rules", electric-blue arrows, navy-black background, gold terminal node] |
| **motion** | remotion draw-on |
| **SFX** | data-blip × 3 |
| **transition** | cut / cut |

---

### S054 | act3 | ~7s | beat: The holding — exclusionary rule applies to states — CLM-0001

| field | value |
|---|---|
| **visual_mode** | typography |
| **recon_label** | false |
| **onscreen_text** | EXCLUSIONARY RULE — ALL STATES |
| **source** | GFX — Remotion |
| **SDXL_PROMPT** | [GFX — Remotion phrase reveal with electric-blue underline sweep and US map thumbnail fill in corner, brand colors] |
| **motion** | remotion reveal + map corner fill |
| **SFX** | low boom; sweep |
| **transition** | cut / cut |

---

### S055 | act3 | ~6s | beat: Map — the rule now reaches every state courtroom — CLM-0001 / CLM-0008

| field | value |
|---|---|
| **visual_mode** | map |
| **recon_label** | false |
| **onscreen_text** | FEDERAL (1914) → ALL STATES (1961) |
| **source** | GFX — Remotion |
| **SDXL_PROMPT** | [GFX — Remotion US map: federal courts highlight first in one color, then state courts sweep fill electric-blue, year labels animate] |
| **motion** | remotion two-phase sweep |
| **SFX** | sweep × 2; impact |
| **transition** | cut / cut |

---

### S056 | act3 | ~6s | beat: Conviction reversed — Dollree Mapp walks free — CLM-0002 / CLM-0001

| field | value |
|---|---|
| **visual_mode** | reenactment |
| **recon_label** | true |
| **onscreen_text** | CONVICTION REVERSED. |
| **source** | STILL+M → svd |
| **motion** | svd slow-drift through doorway |
| **SFX** | sub-swell |
| **transition** | cut / cut |

**SDXL_PROMPT:**
Wide medium shot of a female figure walking away from camera through an open institutional doorway into daylight, a silhouette stepping from a dark interior into a bright exterior, the doorway creates a rectangular portal of bright sky, her dress and coat are 1950s period-accurate, deep navy shadow interior, electric-blue and warm white light flooding through the door, fine 35mm grain, chiaroscuro, shallow depth of field on the threshold, photoreal documentary, symbolic reconstruction, no identifiable face, no text, no logos [BRAND] --ar 16:9

**SDXL_NEG:**
cartoon, cgi, 3d, illustration, face visible, identifiable person, modern clothing, text, logos, oversaturated, hdr, watermark, nsfw

**fallback:** Open doorway into bright daylight, no figure, depth-parallax

---

### S057 | act3 | ~6s | beat: A resounding win — but it carries a cost — CLM-0007 / CLM-0006

| field | value |
|---|---|
| **visual_mode** | typography |
| **recon_label** | false |
| **onscreen_text** | A WIN. AND A COST. |
| **source** | GFX — Remotion |
| **SDXL_PROMPT** | [GFX — Remotion two-phrase sequential reveal, first phrase appears then second phrase below in contrasting weight, brand texture] |
| **motion** | remotion sequential reveal |
| **SFX** | soft impact; low tension drone enters |
| **transition** | cut / cut |

---

### S058 | act3 | ~6s | beat: Act III close — the door as a recurring motif, now legally protected — CLM-0001

| field | value |
|---|---|
| **visual_mode** | object_macro |
| **recon_label** | false |
| **onscreen_text** | — |
| **source** | STILL+M → parallax |
| **motion** | parallax slow-pull back |
| **SFX** | low swell; ambience |
| **transition** | dissolve / cut |

**SDXL_PROMPT:**
Medium shot of the same 1950s residential front door from S001 and S015 (reuse asset, front-on), now shot from inside, the door standing closed and solid, a shaft of warm amber exterior light visible through the keyhole and door crack edge, the interior is dark with deep navy shadows, electric-blue rim accent on the door frame, fine 35mm grain, shallow depth of field, chiaroscuro, volumetric dust inside, photoreal documentary, no people, no readable text, no logos, the door now reads as a protected threshold [BRAND] --ar 16:9

**SDXL_NEG:**
cartoon, cgi, 3d, illustration, people visible, faces, oversaturated, hdr, watermark, text, logos, broken door, open door, modern context, nsfw

**fallback:** Same door asset from S001, tighter crop, interior side, depth-parallax

---

### S059 | act3 | ~7s | beat: Act III breath — SCOTUS chamber, the gravity — CLM-0002

| field | value |
|---|---|
| **visual_mode** | establishing |
| **recon_label** | false |
| **onscreen_text** | — |
| **source** | STILL+M → kenburns |
| **motion** | kenburns slow tilt up to ceiling |
| **SFX** | chamber resonance |
| **transition** | dissolve / fade to black |

Reuse S034 SCOTUS chamber asset, different crop (tilt up toward ceiling/coffers). No new SDXL still needed.

---

## SECTION: ACT IV — THE COST (8:10–10:35) | ~145s | 18 shots

---

### S060 | act4 | ~7s | beat: The tension — reliable evidence that must be thrown out — CLM-0007

| field | value |
|---|---|
| **visual_mode** | object_macro |
| **recon_label** | false |
| **onscreen_text** | TRUE. OBTAINED ILLEGALLY. |
| **source** | STILL+M → parallax |
| **motion** | parallax push-in |
| **SFX** | low tension bed |
| **transition** | fade in / cut |

**SDXL_PROMPT:**
Close-up macro of several manila evidence folders stacked on a dark table surface, the folders closed and without legible writing, a heavy rubber-banded bundle of papers beside them, hard top-down overhead lamp casting directional chiaroscuro, electric-blue rim light from the left on the stack edge, deep shadow to the right, fine 35mm grain, shallow depth of field on the front folder, photoreal documentary, no text legible on folders, no labels readable, no logos [BRAND] --ar 16:9

**SDXL_NEG:**
cartoon, cgi, 3d, illustration, readable text on folders, readable labels, logos, faces, people, oversaturated, hdr, watermark, modern office, suggestive content, nsfw

**fallback:** Stacked paper abstract, kenburns, no text

---

### S061 | act4 | ~7s | beat: Cardozo's objection — 1926 — the cost stated — CLM-0007

| field | value |
|---|---|
| **visual_mode** | typography |
| **recon_label** | false |
| **onscreen_text** | JUDGE CARDOZO — 1926 |
| **source** | GFX — Remotion |
| **SDXL_PROMPT** | [GFX — Remotion attribution card: name and year appear, then the quote types on below in quotation marks, brand texture, gold quote marks] |
| **motion** | remotion type-on |
| **SFX** | pen-scratch |
| **transition** | cut / cut |

---

### S062 | act4 | ~7s | beat: "The criminal is to go free because the constable has blundered" — CLM-0007

| field | value |
|---|---|
| **visual_mode** | typography |
| **recon_label** | false |
| **onscreen_text** | "THE CONSTABLE HAS BLUNDERED." |
| **source** | GFX — Remotion |
| **SDXL_PROMPT** | [GFX — Remotion full-width quote card, large type, gold quotation marks, electric-blue key phrase highlight, brand monospace] |
| **motion** | remotion word-by-word reveal |
| **SFX** | typewriter; soft low boom at end |
| **transition** | cut / cut |

---

### S063 | act4 | ~7s | beat: The constable — abstract symbol of police acting negligently — CLM-0007

| field | value |
|---|---|
| **visual_mode** | abstract |
| **recon_label** | false |
| **onscreen_text** | — |
| **source** | STILL+M → parallax |
| **motion** | parallax slow |
| **SFX** | ambient low |
| **transition** | cut / dissolve |

**SDXL_PROMPT:**
Abstract low-angle shot looking up at a single police officer's torso and badge from directly below, the face entirely cut off at frame edge, a heavy 1950s-era dark wool uniform jacket, a simple circular badge shape on the chest rendered as a blur — not readable, hard overhead lamp creating dramatic downward chiaroscuro, deep shadows on the uniform below the badge, electric-blue rim light from the right, fine 35mm grain, shallow depth of field, photoreal documentary, symbolic abstract image representing institutional power, no readable badge text, no logos, no face [BRAND] --ar 16:9

**SDXL_NEG:**
cartoon, cgi, 3d, illustration, readable badge text, readable badge number, identifiable person, face, modern uniform, oversaturated, hdr, watermark, logos, nsfw

**fallback:** Abstract badge-shape blur on dark uniform texture, depth-parallax

---

### S064 | act4 | ~6s | beat: A guilty defendant goes free — the symbolic cost — CLM-0007

| field | value |
|---|---|
| **visual_mode** | reenactment |
| **recon_label** | true |
| **onscreen_text** | THE CRIMINAL GOES FREE — |
| **source** | STILL+M → svd |
| **motion** | svd slow drift of figure through doorway |
| **SFX** | footsteps receding; tension |
| **transition** | cut / cut |

Reuse S056 asset (female figure through doorway) — different color grade or crop to feel morally ambiguous rather than triumphant. Remotion can add a slightly colder grade overlay.

**SDXL_PROMPT:** [Reuse S056 with Remotion overlay — colder grade, no new SDXL still needed]

---

### S065 | act4 | ~6s | beat: Deterrence counter-argument — without the rule, no incentive — CLM-0006

| field | value |
|---|---|
| **visual_mode** | diagram |
| **recon_label** | false |
| **onscreen_text** | WITHOUT CONSEQUENCE: NO INCENTIVE |
| **source** | GFX — Remotion |
| **SDXL_PROMPT** | [GFX — Remotion: two-column comparison "With rule" / "Without rule", deterrence arrows, electric-blue vs grey, brand colors] |
| **motion** | remotion column-reveal |
| **SFX** | ui-tick × 2 |
| **transition** | cut / cut |

---

### S066 | act4 | ~6s | beat: Scale of the debate — critics vs defenders — CLM-0007 / CLM-0006

| field | value |
|---|---|
| **visual_mode** | object_macro |
| **recon_label** | false |
| **onscreen_text** | — |
| **source** | STILL+M → svd |
| **motion** | svd scale-oscillation loop |
| **SFX** | sub-drone; oscillation |
| **transition** | cut / dissolve |

Reuse S007 scales asset — slight tilt toward "cost" side, oscillating, unresolved. SVD loop. No new SDXL needed.

---

### S067 | act4 | ~7s | beat: Later Supreme Court — exceptions carved — CLM-0009

| field | value |
|---|---|
| **visual_mode** | timeline |
| **recon_label** | false |
| **onscreen_text** | 1961 → EXCEPTIONS CARVED LATER |
| **source** | GFX — Remotion |
| **SDXL_PROMPT** | [GFX — Remotion timeline from 1961 forward, new nodes appear for "good faith exception" and others with labels, electric-blue main line, gold exception branches] |
| **motion** | remotion draw-on with branch reveals |
| **SFX** | ui-tick × 3 |
| **transition** | cut / cut |

---

### S068 | act4 | ~6s | beat: Good-faith exception — an officer with a defective warrant they believed valid — CLM-0009

| field | value |
|---|---|
| **visual_mode** | object_macro |
| **recon_label** | false |
| **onscreen_text** | GOOD-FAITH EXCEPTION |
| **source** | STILL+M → parallax |
| **motion** | parallax gentle |
| **SFX** | low ambient |
| **transition** | cut / cut |

**SDXL_PROMPT:**
Close-up macro of a hand holding an official-looking folded blank document at an angle, the document half-unfolded showing its blank interior, a second surface behind shows an official-looking seal shape that is entirely blurred and unreadable, hard directional top lamp, electric-blue rim from the left, deep navy shadow right, fine 35mm grain, shallow depth of field, chiaroscuro, photoreal documentary, no text readable on the document, no logos, no seals readable, symbolic object representing a warrant believed valid but defective [BRAND] --ar 16:9

**SDXL_NEG:**
cartoon, cgi, 3d, illustration, readable text, readable seal, logos, faces, extra fingers, fused fingers, deformed hand, oversaturated, hdr, watermark, nsfw

**fallback:** Folded blank paper on desk, depth-parallax

---

### S069 | act4 | ~7s | beat: The rule today is narrower — CLM-0009

| field | value |
|---|---|
| **visual_mode** | diagram |
| **recon_label** | false |
| **onscreen_text** | NARROWED — BUT THE CORE HOLDS |
| **source** | GFX — Remotion |
| **SDXL_PROMPT** | [GFX — Remotion: 1961 rule shown as large block, then exceptions chip pieces away, core remains highlighted in electric-blue] |
| **motion** | remotion chip-away animation |
| **SFX** | stone-chip × 3; low boom on core |
| **transition** | cut / cut |

---

### S070 | act4 | ~7s | beat: The core holds — an illegal search can still sink a case — CLM-0009 / CLM-0001

| field | value |
|---|---|
| **visual_mode** | typography |
| **recon_label** | false |
| **onscreen_text** | THE CORE HOLDS. |
| **source** | GFX — Remotion |
| **SDXL_PROMPT** | [GFX — Remotion single phrase, bold, electric-blue underline sweep, parchment texture underlay] |
| **motion** | remotion underline sweep |
| **SFX** | low boom |
| **transition** | cut / dissolve |

---

### S071 | act4 | ~7s | beat: Rights without remedies are fictions — the thesis stated — CLM-0005 / CLM-0001

| field | value |
|---|---|
| **visual_mode** | typography |
| **recon_label** | false |
| **onscreen_text** | RIGHTS WITHOUT REMEDIES ARE FICTIONS. |
| **source** | GFX — Remotion |
| **SDXL_PROMPT** | [GFX — Remotion phrase reveal, slow word-by-word, each word builds into full phrase, then parchment texture fades in beneath it] |
| **motion** | remotion word-build |
| **SFX** | pen-scratch; sub-swell |
| **transition** | cut / cut |

---

### S072 | act4 | ~7s | beat: 170 years — Fourth Amendment existed before Mapp made it real — CLM-0005 / CLM-0001

| field | value |
|---|---|
| **visual_mode** | timeline |
| **recon_label** | false |
| **onscreen_text** | 170 YEARS — ON PAPER ONLY |
| **source** | GFX — Remotion |
| **SDXL_PROMPT** | [GFX — Remotion timeline bar from 1791 to 1961, majority of bar labelled "on paper only" in grey, then final segment pulses electric-blue "real consequence from 1961"] |
| **motion** | remotion bar-fill then pulse |
| **SFX** | data-blip; impact on pulse |
| **transition** | cut / cut |

---

### S073 | act4 | ~7s | beat: A forced entry — the door motif one final time — CLM-0004 / CLM-0001

| field | value |
|---|---|
| **visual_mode** | object_macro |
| **recon_label** | false |
| **onscreen_text** | — |
| **source** | STILL+M → svd light-shift |
| **motion** | svd slow light-shift amber-to-blue |
| **SFX** | low resonant tone |
| **transition** | dissolve / cut to black |

Reuse S058 interior-door asset. Remotion applies a warm-to-cold light shift overlay — amber (before Mapp, unprotected) shifting to electric-blue (after Mapp, protected). No new SDXL needed.

---

### S074 | act4 | ~6s | beat: Act IV close — the warrant requirement has consequences — CLM-0001

| field | value |
|---|---|
| **visual_mode** | typography |
| **recon_label** | false |
| **onscreen_text** | MAPP IS THE REASON FOR THAT. |
| **source** | GFX — Remotion |
| **SDXL_PROMPT** | [GFX — Remotion slow phrase reveal on black, then name "MAPP" remains isolated and glowing as the other words fade, electric-blue name] |
| **motion** | remotion fade-isolate |
| **SFX** | sub-swell into silence |
| **transition** | cut / fade to black |

---

### S075 | act4 | ~5s | beat: Act IV transition breath — a piece of paper and a doorstep — CLM-0004

| field | value |
|---|---|
| **visual_mode** | abstract |
| **recon_label** | false |
| **onscreen_text** | — |
| **source** | STILL+M → svd light-flicker |
| **motion** | svd slow ambient drift |
| **SFX** | ambient low; silence approaching |
| **transition** | dissolve / fade to black |

**SDXL_PROMPT:**
Abstract extreme close-up of a blank folded piece of paper resting on a wooden threshold at the base of a closed door, the door visible above, the floor visible below, a thin line of light from outside glowing under the door gap, deep navy interior shadow, electric-blue rim from the door crack, fine 35mm grain, extreme shallow depth of field, chiaroscuro, volumetric dust, photoreal documentary, no text on the paper, no logos [BRAND] --ar 16:9

**SDXL_NEG:**
cartoon, cgi, 3d, illustration, readable text, logos, faces, people, oversaturated, hdr, watermark, modern context, nsfw

**fallback:** Light-under-door abstract, depth-parallax, no paper

---

## SECTION: ENDING (10:35–12:00) | ~85s | 12 shots

---

### S076 | ending | ~7s | beat: Step back — the shape of this case — the bombing suspect never found — CLM-0004

| field | value |
|---|---|
| **visual_mode** | establishing |
| **recon_label** | false |
| **onscreen_text** | A SUSPECT NEVER FOUND. |
| **source** | STILL+M → kenburns |
| **motion** | kenburns pull-back from door |
| **SFX** | ambient quiet; light swell |
| **transition** | fade in / cut |

Reuse S017 house exterior asset, kenburns pull-back. No new SDXL needed.

---

### S077 | ending | ~6s | beat: What started it — three officers, a search, a conviction that traveled to Washington — CLM-0004

| field | value |
|---|---|
| **visual_mode** | map |
| **recon_label** | false |
| **onscreen_text** | ONE SEARCH — ONE CONVICTION — SCOTUS |
| **source** | GFX — Remotion |
| **SDXL_PROMPT** | [GFX — Remotion three-node summary map: Cleveland icon → conviction stamp → SCOTUS icon, electric-blue connecting line, gold terminal node] |
| **motion** | remotion travel-node |
| **SFX** | sweep; impact at end |
| **transition** | cut / cut |

---

### S078 | ending | ~7s | beat: Mapp, Gideon, Miranda — three pieces of one shift — CLM-0010

| field | value |
|---|---|
| **visual_mode** | diagram |
| **recon_label** | false |
| **onscreen_text** | MAPP · GIDEON · MIRANDA |
| **source** | GFX — Remotion |
| **SDXL_PROMPT** | [GFX — Remotion triptych three-panel: left panel "MAPP — searches", center "GIDEON — counsel", right "MIRANDA — interrogation", all three appear and connect with a horizontal line, electric-blue, brand colors] |
| **motion** | remotion three-panel sequential reveal |
| **SFX** | ui-tick × 3; low swell |
| **transition** | cut / cut |

---

### S079 | ending | ~8s | beat: Triptych visual — three doors for three cases — CLM-0010

| field | value |
|---|---|
| **visual_mode** | abstract |
| **recon_label** | false |
| **onscreen_text** | — |
| **source** | STILL+M → parallax |
| **motion** | parallax slow three-panel |
| **SFX** | ambient swell |
| **transition** | cut / dissolve |

**SDXL_PROMPT:**
Triptych composition — three identical wooden residential doors side by side in a wide frame, each door slightly different in its state: left door firmly closed, center door with a hand resting on the handle, right door open just a crack showing light — the three panels read as a continuous tableau, shot from slightly below eye level, wide shot, deep navy corridor setting, electric-blue rim light on each door frame from above, volumetric light in the right door crack, fine 35mm grain, chiaroscuro, photoreal documentary, symbolic, no text, no logos, no faces [BRAND] --ar 16:9

**SDXL_NEG:**
cartoon, cgi, 3d, illustration, people visible, faces, readable text, logos, seals, oversaturated, hdr, watermark, modern context, nsfw

**fallback:** Single door in three crops composited in Remotion, depth-parallax

---

### S080 | ending | ~7s | beat: Warren Court — applying rights to the states — the constitutional shift — CLM-0010

| field | value |
|---|---|
| **visual_mode** | diagram |
| **recon_label** | false |
| **onscreen_text** | BILL OF RIGHTS → THE STATES |
| **source** | GFX — Remotion |
| **SDXL_PROMPT** | [GFX — Remotion: two-level diagram: top "Bill of Rights" icon, bottom "50 states" grid, connecting arrows raining down, electric-blue, gold accent, labels for all three cases] |
| **motion** | remotion top-to-bottom cascade |
| **SFX** | sweep; data-blip cascade |
| **transition** | cut / cut |

---

### S081 | ending | ~7s | beat: Miranda — what police must say — CLM-0010

| field | value |
|---|---|
| **visual_mode** | typography |
| **recon_label** | false |
| **onscreen_text** | MIRANDA: WHAT THEY MUST SAY |
| **source** | GFX — Remotion |
| **SDXL_PROMPT** | [GFX — Remotion: series-link card, "Miranda" with icon, electric-blue, minimal, cross-links to EP1] |
| **motion** | remotion card-reveal |
| **SFX** | soft ui-tick |
| **transition** | cut / cut |

---

### S082 | ending | ~7s | beat: Gideon — a lawyer if you cannot afford one — CLM-0010

| field | value |
|---|---|
| **visual_mode** | typography |
| **recon_label** | false |
| **onscreen_text** | GIDEON: YOUR LAWYER |
| **source** | GFX — Remotion |
| **SDXL_PROMPT** | [GFX — Remotion: series-link card, "Gideon" with icon, same format as S081, cross-links to EP2] |
| **motion** | remotion card-reveal |
| **SFX** | soft ui-tick |
| **transition** | cut / cut |

---

### S083 | ending | ~7s | beat: Mapp — what happens before any of that — the search — CLM-0010 / CLM-0001

| field | value |
|---|---|
| **visual_mode** | typography |
| **recon_label** | false |
| **onscreen_text** | MAPP: WHAT HAPPENS BEFORE |
| **source** | GFX — Remotion |
| **SDXL_PROMPT** | [GFX — Remotion: series-link card "Mapp", electric-blue, same format, with a small door icon — third of the triptych, final of the three] |
| **motion** | remotion card-reveal then all three together |
| **SFX** | soft ui-tick; swell |
| **transition** | cut / dissolve |

---

### S084 | ending | ~7s | beat: "Or what?" — the payoff — CLM-0001 / CLM-0006

| field | value |
|---|---|
| **visual_mode** | typography |
| **recon_label** | false |
| **onscreen_text** | OR WHAT? |
| **source** | GFX — Remotion |
| **SDXL_PROMPT** | [GFX — Remotion: large single phrase, isolated, growing slowly to fill frame, electric-blue, then hold] |
| **motion** | remotion grow-to-fill |
| **SFX** | silence then low boom |
| **transition** | cut / cut |

---

### S085 | ending | ~6s | beat: The answer — evidence gets thrown out — CLM-0001

| field | value |
|---|---|
| **visual_mode** | typography |
| **recon_label** | false |
| **onscreen_text** | THE EVIDENCE GETS THROWN OUT. |
| **source** | GFX — Remotion |
| **SDXL_PROMPT** | [GFX — Remotion: reply phrase appears below "OR WHAT?" in contrasting color (gold), the full exchange reads as a visual dialogue] |
| **motion** | remotion reply-reveal |
| **SFX** | resolution tone; swell |
| **transition** | cut / cut |

---

### S086 | ending | ~7s | beat: A figure through the doorway — the motif's final beat — CLM-0001

| field | value |
|---|---|
| **visual_mode** | abstract |
| **recon_label** | false |
| **onscreen_text** | NOW YOU KNOW WHAT IT TOOK. |
| **source** | STILL+M → parallax |
| **motion** | parallax push-in to door |
| **SFX** | outro swell rising |
| **transition** | dissolve / fade to black |

Reuse S056 doorway-to-light asset, pull-in motion, warm grade, outro swell builds underneath. No new SDXL needed.

---

### S087 | ending | ~8s | beat: Brand endcard + next-episode tease — CLM-0010

| field | value |
|---|---|
| **visual_mode** | typography |
| **recon_label** | false |
| **onscreen_text** | NEXT EPISODE: WHO DECIDES WHAT IS A CRIME? |
| **source** | GFX — Remotion |
| **SDXL_PROMPT** | [GFX — Remotion: brand endcard with PD logo mark, subscribe prompt, next-episode tease line, all animated, navy-black background, electric-blue and gold accents] |
| **motion** | remotion brand reveal |
| **SFX** | end-card boom |
| **transition** | fade in / fade to black |

---

## ASSET SUMMARY

| category | count | notes |
|---|---|---|
| SDXL stills (new) | 30 | S001 S002 S004 S007 S009 S010 S012 S015 S017 S018 S019 S020 S021 S022 S023 S024 S026 S027 S028 S030 S034 S037 S039 S043 S044 S046 S048 S051 S056 S058 S060 S063 S068 S075 S079 |
| SDXL stills (reuse, different crop) | 7 | S059 uses S034; S064 uses S056; S066 uses S007; S073 uses S058; S076 uses S017; S086 uses S056; S051 uses S009 |
| GFX / Remotion (no SDXL) | 44 | All typography, diagram, map, timeline, callout shots |
| Runway clips | 10 | S018 S022 — door-force / approach / organic motion |
| SVD loops | 9 | S002 S019 S023 S026 S046 S066 S073 S075 + one reuse |
| TOTAL visual events | ~114 | Every 4–6s |

---

## QC PROFILE (per shot)

All SDXL stills run automated QC on:
- resolution/aspect ratio (1344×768, 16:9)
- NSFW classifier pass (mandatory; CLM-0004 BAN guard)
- face-detection negative check (no identifiable faces; flag any hit for human review)
- text/watermark negative check (no readable text in-frame)
- anachronism signal (post-1961 objects, modern vehicles, smartphones)
- semantic match to shot beat (CLIP embedding distance vs. scene description)
- continuity embedding distance (door motif shots cluster; scale motif shots cluster)
- exposure/histogram (no blown highlights; deep blacks preserved)
- brand palette match (navy, electric-blue, gold accent present)

All `recon_label: true` shots require human review before locking.

---

## CONTINUITY REFS

**Door motif:** S001 / S015 / S017 / S022 / S058 / S073 / S079 / S086 — same 1950s residential door asset family. Seeds pinned after first approval.

**Hand-with-paper motif:** S002 / S023 / S024 / S026 / S068 — all same folded-blank-paper asset family. No text ever visible.

**Scale motif:** S007 / S046 / S066 — same antique brass scale, three states (tipped left / balanced / oscillating).

**Parchment motif:** S009 / S051 — same aged parchment close-up, two crops (wider then tighter).

**SCOTUS chamber:** S034 / S044 / S059 — same interior, three crops/tilts.

**Female-figure-through-doorway:** S056 / S064 / S086 — same asset, grade/crop modulated by Remotion overlay for emotional valence shift.

**Remotion triptych (Mapp/Gideon/Miranda):** S078 / S079 / S080 / S081 / S082 / S083 — unified graphic system; matches EP2 endcard format.

**CLM-0004 BAN guard check at QC:** Every basement/interior/search shot (S027) passes the NSFW classifier plus a human-review flag. The shot brief notes explicitly that only generic storage items are depicted. No SDXL prompt for any search shot contains suggestive terms.agentId: a0f813dc484389f81 (use SendMessage with to: 'a0f813dc484389f81' to continue this agent)
<usage>subagent_tokens: 75634
tool_uses: 7
duration_ms: 563287</usage>