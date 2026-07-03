# PD-2026-025-kyllo — Codex Image Prompts v001 (EARLY / pre-script parallel batch)

Kyllo v. United States (2001). Police aimed a thermal-imaging device at a private home from a public street, at night, without a warrant, and inferred that high-heat lamps were growing marijuana inside. The Supreme Court held 5–4 (Scalia, maj.) that using sense-enhancing technology **not in general public use** to explore details of a home that could not otherwise be known without physical intrusion is a Fourth Amendment **search**. Core line: "at the very core of the Fourth Amendment stands the right of a man to retreat into his own home and there be free from unreasonable governmental intrusion."

**Status: EARLY batch so image generation can run in parallel with scripting.** Scene IDs (S0xx) may shift slightly when the annotated script locks, but these HERO images are stable to the story and safe to generate now. If a scene number moves, the image is re-tagged in `asset_selection`, not regenerated.

Primary image pipeline: **Codex image generation first.** Local SDXL/SVD only for bulk variants under the same rights/QC rules. No paid API or external upload is authorized by this file.

## Global Rules

- Aspect: 16:9, 1920×1080 target. Stills must survive slow push, **2.5D parallax / floating-card treatment**, and crop (leave clean negative space top and lower-third for Remotion text).
- Style: museum-grade cinematic symbolic noir documentary. Black / deep navy base (`#0A0A0C` / `#0B1A2B`), **electric-blue signal `#1F6BFF`**, silver highlights `#C8CDD6`, restrained **muted gold accent `#E5B53A`** (sparingly), controlled contrast, subtle film grain. Cold, surveillance-thriller mood — winter night, breath-cold air, quiet suburb.
- People: **faceless** — silhouettes, backs, torsos, hands, POV only. **No identifiable likeness** of Danny Kyllo, Agent William Elliott, Justice Scalia, Justice Stevens, or any real or modern person.
- Text: **do not generate any text, letters, numbers, signs, logos, badges, readable documents, watermarks, or captions inside images.** Remotion adds all text. (No "4th Amendment" wording, no case citations, no dates, no temperature readouts.)
- Thermal look: thermal/heat imagery is core to this story, but keep it **on-brand and restrained** — deep navy → electric-blue field with **hot spots rendered as white-hot cores with a thin muted-gold edge**, NOT a garish rainbow thermal palette, NOT a full-screen yellow wash. Heat = information, eerie and clinical.
- No drugs depicted: the indoor "grow" is only ever an **intense light/heat leak** through a wall, garage seam, or curtain. No plants, no paraphernalia, no drug references.
- Disclosure: every reenactment/location/object image is **symbolic reconstruction**, rights-registered before edit use. Never look like authentic archival footage.
- Negative: face, facial features, portrait, recognizable person, celebrity, police badge/logo, readable sign, text, numbers, watermark, gore, weapon glamor, aiming gun, drugs, plants, distorted hands, extra fingers, over-processed HDR, cartoon, neon candy colors, rainbow thermal.

## Quality Bar (a selected still must pass ALL)

- Composition: clear subject hierarchy, intentional negative space for overlays, mobile-readable focal point (72% of views are mobile).
- Lighting: motivated source, controlled contrast, no flat stock look, no muddy black crush.
- Material detail: believable siding, glass, frost, breath-fog, haze, grain; no plastic AI sheen.
- Narrative duty: the image must explain, locate, symbolize, or build tension for its exact beat.
- Safety: no identifiable person, no logos/text, no authentic-footage illusion, no drugs.
- Editability: works with 2.5D/parallax/floating-card, has crop room, does not fight captions/lower-thirds.
- Neighbor fit: not redundant with adjacent shots; change scale, angle, brightness, or subject.

Reject & regenerate if any appear: visible face, badge/logo/text/number artifact, mangled hands, weapon glamor, drugs/plants, city-specific landmark not in script, period anachronism (case reenactment is **January 1992**; modern-tie beats are present-day), fake documentary authenticity, generic stock look, rainbow thermal, weak visual role.

## Hero Image Prompts

| ID | Beat | Priority | Candidate Count | Prompt |
|---|---|---:|---:|---|
| COD-S001-thermal-house-reveal | Hook | A | 10 | A quiet suburban home at night seen as an eerie thermal-style heat signature, deep navy façade with an electric-blue cold field and one white-hot glowing core bleeding through a garage wall, thin muted-gold edge on the hot spot, clinical surveillance mood, symbolic reconstruction, museum-grade cinematic still, generous dark negative space top and bottom for text |
| COD-S002-your-home-night | Hook | A | 8 | An ordinary modest single-story home at night from across an empty street, warm interior light in one curtained window, cold navy exterior, frost on the lawn, a feeling of private safety about to be intruded upon, cinematic documentary noir, electric-blue rim light, no people, no text |
| COD-S003-street-1992-cold | Act1 | A | 8 | A 1990s small-town street on a freezing January pre-dawn, wet asphalt, sodium streetlight as soft gold pools, parked cars as dark shapes, breath-cold haze, no readable signs, no faces, period-neutral, deep navy and gold palette, symbolic reconstruction, gallery-quality atmosphere |
| COD-S004-surveillance-car-pov | Act1 | A | 8 | Interior of a parked car at night from behind an anonymous agent's shoulder and gloved hands only, no face, windshield framing a dark house across the street, dashboard as low silhouette, tense stakeout mood, electric-blue dash glow, muted gold streetlight beyond, cinematic reconstruction |
| COD-S005-thermal-device-closeup | Act1 | A | 8 | Extreme close-up of an anonymous handheld thermal-imaging scanner cradled in gloved hands, matte military-grey body, a single cold electric-blue indicator glow, no logos, no readable screen, no text, shallow depth of field, tactile museum-grade object still, dark navy background |
| COD-S006-thermal-scan-house | Act1 | A | 10 | The dark house rendered as a clinical thermal scan: navy-to-electric-blue cold walls with concentrated white-hot cores over the roof vents and one side wall, thin gold heat edges, faint scanline texture, eerie and revealing, symbolic surveillance visualization, not a rainbow thermal, strong negative space |
| COD-S007-heat-leak-wall | Act2 | A | 8 | Macro of a garage wall seam and eave at night leaking an intense warm light from inside, hot glow bleeding through the gap, cold blue exterior around it, no plants, no objects visible inside, symbolic heat-as-evidence motif, tactile material realism, cinematic low-key |
| COD-S008-threshold-doorway | Act2 | A | 8 | A closed front door and threshold of a home at night, single porch light, the doormat and lock in low key, symbolic "core of the home" motif, quiet and inviolable, deep navy shadow with a warm gold pool at the step, no faces, no text, gallery composition |
| COD-S009-warrant-absence | Act2 | B | 6 | Still life of an empty desk with a blank folded document, a pen, and a ring of keys under a hard desk lamp, deep shadow, the sense of a missing signature / missing warrant, no readable text on the paper, navy and gold, precise editorial still |
| COD-S010-courthouse-colonnade | Act3 | A | 8 | A symbolic marble courthouse colonnade at dusk, tall fluted columns receding, cold navy sky, one shaft of gold light between pillars, monumental and severe, no readable inscriptions, no identifiable real building, museum-grade architectural still with strong verticals |
| COD-S011-five-four-division | Act3 | A | 8 | Abstract symbolic composition of a single clean line splitting a dark marble surface, one side lit electric blue and the other muted gold, a five-versus-four tension rendered purely as light and division, no text, no numbers, minimalist gallery-quality metaphor |
| COD-S012-hand-on-opinion | Act3 | B | 6 | Close-up of an anonymous hand resting on a heavy closed leather-bound volume on a dark bench, gold edge light, no readable text, no gavel cliché, restrained judicial gravity, cinematic material detail, navy background |
| COD-S013-modern-surveillance-tie | Act4 | A | 10 | Present-day version of the same idea: an ordinary home at night ringed by faint modern sensing — a small drone silhouette, a doorbell-camera glow, subtle thermal shimmer on the walls, all rendered cold electric-blue with hot-white points, unsettling "what can they see now" mood, no logos, no faces, no text, premium cinematic still |
| COD-S014-retreat-into-home | Act4 | A | 8 | A lone anonymous silhouette seen from behind stepping into a warm doorway and pulling it toward closed, cold blue night outside, warm gold refuge inside, the "right to retreat into your own home" made visual, no face, no text, emotionally resonant museum-grade composition |
| COD-S015-next-episode-phonebooth | Tease | A | 8 | A lone 1960s glass phone booth glowing electric blue on an empty night street, a faint warm handset light inside, symbolic wiretap-privacy tease, cold navy surroundings, no faces, no readable signage, cinematic object still leaving lower-third space for text |

## Additional Hero Prompts — density + variety (for an 11–12 min cut; footage carries the rest)

15 heroes is the old baseline; a 12-minute cut needs ~24+ distinct visuals (material density ≈ runtime/30s) and no repeated-looking neighbors. Footage (factory shelf) carries roughly half the shots; these give the AI-still anchors enough variety. Signature thermal/surveillance beats get the most candidates.

| ID | Beat | Priority | Candidate Count | Prompt |
|---|---|---:|---:|---|
| COD-S016-winter-suburb-aerial | Hook/Act1 | A | 8 | High night aerial over a quiet winter suburb, rows of dark rooftops with a few scattered warm-lit windows, cold navy grade, faint frost sheen, a sense of many private lives below, no readable signs, no faces, cinematic establishing still with wide negative space |
| COD-S017-frosted-window-glow | Act1 | A | 8 | Macro of a frosted window pane at night lit warm gold from inside, ice crystals catching electric-blue moonlight, intimate and private, condensation detail, no figure visible, museum-grade texture, strong standalone mood |
| COD-S018-thermal-through-windshield | Act1 | A | 10 | POV through a frost-edged car windshield at night, the dark house across the street rendered as a faint thermal bloom of cold blue walls and hot-white cores, dashboard silhouette in foreground, clandestine stakeout framing, no faces, no text, no rainbow thermal |
| COD-S019-heat-reveals-presence | Act2 | A | 10 | Abstract surveillance visualization: the faint hot-white outline of a human presence glowing through a cold navy wall, heat as information leaking past a solid barrier, eerie and clinical, thin gold edge on the hot form, no recognizable face, symbolic, generous dark space |
| COD-S020-scanline-facade | Act2 | A | 8 | A dark home façade with a thin electric-blue scan-line sweeping down it and faint measurement ticks of light, a sense of a machine reading the house, cold and invasive, no readable numbers or text, minimalist premium composition |
| COD-S021-property-line-aerial | Act2 | A | 8 | Top-down night view of a single lit house and its yard, the property boundary traced as one clean thin electric-blue line around it, the idea of a legal border around the home made visual, cold navy ground, no text, gallery-quality minimalism |
| COD-S022-curtain-backlit-heat | Act2 | B | 6 | A drawn curtain backlit by intense interior light, the hot glow blooming through the fabric, the silhouette of a simple standing lamp behind it (not plants, not drugs), warm gold against cold blue room edges, symbolic heat-source motif, tactile realism |
| COD-S023-deadbolt-closeup | Act2 | B | 6 | Extreme close-up of a brass deadbolt and door edge, the bolt thrown shut, warm key-light raking across worn metal, cold navy shadow beyond, the sanctity of a locked home, no text, no logos, precise material still |
| COD-S024-courtroom-interior | Act3 | A | 8 | A dignified empty courtroom interior in low key, a long dark bench and tall windows, one cold shaft of light across the floor, monumental and neutral, no people, no readable text or seals, museum-grade architectural composition with vertical calm |
| COD-S025-majority-dissent-books | Act3 | A | 6 | Two heavy leather-bound volumes resting slightly apart on a dark bench, a single blade of light falling in the gap between them, one warmed gold and one cooled blue, a silent majority-versus-dissent metaphor, no readable text, refined still life |
| COD-S026-scales-privacy-power | Act3 | B | 6 | A minimalist balance scale in cold low key, one pan holding a small warm-lit model of a house and the other a cold blue lens/sensor form, equilibrium and tension between privacy and surveillance, no faces, no text, symbolic gallery composition |
| COD-S027-drone-thermal-neighborhood | Act4 | A | 10 | Present-day: a small quadcopter drone silhouette hovering over a night neighborhood seen partly in thermal, houses glowing as soft hot blooms against cold blue streets, unsettling modern-surveillance escalation, no logos, no faces, no text, premium cinematic still |
| COD-S028-sensor-wall-glint | Act4 | A | 8 | A dark wall of many small camera and sensor lenses catching faint electric-blue glints, one lens brighter and awake, the feeling of constant unseen watching, shallow depth of field, cold clinical mood, no brand markings, no text |
| COD-S029-phone-nightstand-privacy | Act4 | A | 8 | A smartphone glowing on a nightstand in a dark bedroom, a faint thermal shimmer over the doorway beyond, the last private space quietly observable, cold navy with a small warm glow, no readable screen, no icons, no faces, intimate premium object still |

## Local SDXL Variant Settings (only if bulk variants are needed)

- Model: RealVisXL V5 or JuggernautXL — pick one and keep it for the whole episode.
- Sampler: DPM++ 2M Karras, 32–40 steps, CFG 4.5–6.5.
- Base 1344×768 → upscale 1920×1080.
- One locked seed family per episode with controlled per-scene offsets.
- Selection: semantic match, no face/likeness, no text/logos, no anatomy issues, brand fit, editability, symbolic-not-authentic clarity, thermal restrained (not rainbow).

## Coverage / Handoff Notes

- These ~28 heroes (15 core + 13 density/variety) cover the hook, four acts, and next-episode tease with enough distinct anchors that no two neighbors look alike; footage from the factory shelf carries roughly half the shots. Remaining scenes are Remotion graphics/diagrams/typography or crop/parallax variants of these heroes.
- Do NOT generate exact dates, temperatures, legal standards, counters, or case citations in images — Remotion owns all text.
- The thermal/heat-leak beats (S001, S006, S007) are the signature visuals — generate the most candidates there (10 each) and select the most restrained, on-brand, non-rainbow options.
- After the annotated script locks, this file may gain 1–3 extra hero prompts for specific scripted beats; already-generated heroes are reused, not regenerated.
