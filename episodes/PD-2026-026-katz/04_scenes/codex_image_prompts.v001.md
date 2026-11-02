# PD-2026-026-katz — Codex Image Prompts v001 (EARLY / pre-script parallel batch)

Katz v. United States, 389 U.S. 347 (1967). In 1965 the FBI attached an electronic listening-and-recording device to the **outside** of a public glass telephone booth in Los Angeles to record Charlie Katz's calls (he was transmitting illegal gambling wagers). No physical entry, no trespass into the booth. The Supreme Court held 7–1 (Stewart, maj.; Black dissent; Harlan's famous concurrence) that **"the Fourth Amendment protects people, not places,"** and that a person who shuts a booth door and pays the toll is entitled to assume his words are private — so the eavesdropping was a search. Harlan's concurrence gave us the **"reasonable expectation of privacy"** test (a subjective expectation society accepts as reasonable). This overturned the old rule that the Fourth Amendment required a physical trespass.

**Status: EARLY batch so image generation can run in parallel with scripting.** Scene IDs may shift when the annotated script locks; these HERO images are stable to the story. This is the direct sequel to EP25 Kyllo ("walls" → "no walls"): Kyllo protected the home by its walls; Katz protects the person even in a glass box on a public sidewalk.

Primary image pipeline: **Codex image generation first.** Local SDXL/SVD only for bulk variants under the same rights/QC rules. No paid API or external upload is authorized by this file.

## Global Rules

- Aspect: 16:9, 1920×1080 target. Stills must survive slow push, **2.5D parallax / floating-card treatment**, and crop (clean negative space top and lower-third for Remotion text).
- Style: museum-grade cinematic symbolic noir documentary. Black / deep navy base (`#0A0A0C` / `#0B1A2B`), **electric-blue signal `#1F6BFF`**, silver highlights `#C8CDD6`, restrained **muted gold accent `#E5B53A`** (sparingly), controlled contrast, subtle film grain. Mood: 1960s night, rain-slick streets, neon reflections, the loneliness and intimacy of a private call in a public place.
- People: **faceless** — silhouettes, backs, torsos, hands, POV only. **No identifiable likeness** of Charlie Katz, any FBI agent, or Justices Stewart / Harlan / Black.
- Text: **do not generate any text, letters, numbers, signs, logos, badges, readable documents, dial labels, watermarks, or captions inside images.** Remotion adds all text. (No "people not places," no case citations, no dates, no phone numbers.)
- Surveillance look: the wiretap/eavesdropping is core — render it as **a hidden microphone or reel-to-reel recorder, wires, and glowing sound-waves** in cold electric-blue with a thin gold edge; eerie, clandestine, clinical. No garish neon-candy colors.
- Disclosure: every reenactment/location/object image is **symbolic reconstruction**, rights-registered before edit use. Never look like authentic archival footage.
- Negative: face, facial features, portrait, recognizable person, celebrity, FBI/police badge or logo, readable sign/number/dial, watermark, text, gore, weapon glamor, distorted hands, extra fingers, over-processed HDR, cartoon, neon candy colors.

## Quality Bar (a selected still must pass ALL)

- Composition: clear subject hierarchy, intentional negative space for overlays, mobile-readable focal point (72% of views are mobile).
- Lighting: motivated source (neon, streetlight, booth glow), controlled contrast, no flat stock look, no muddy black crush.
- Material detail: believable glass, rain, chrome, bakelite handset, tape reels; no plastic AI sheen.
- Narrative duty: the image must explain, locate, symbolize, or build tension for its exact beat.
- Safety: no identifiable person, no logos/text, no authentic-footage illusion.
- Editability: works with 2.5D/parallax/floating-card, has crop room, does not fight captions/lower-thirds.
- Neighbor fit: not redundant with adjacent shots; change scale, angle, brightness, or subject.

Reject & regenerate if any appear: visible face, badge/logo/text/number artifact, mangled hands, glamorized weapon, period anachronism (case reenactment is **mid-1960s Los Angeles**; modern-tie beats are present-day), fake documentary authenticity, generic stock look, weak visual role.

## Hero Image Prompts

| ID | Beat | Priority | Candidate Count | Prompt |
|---|---|---:|---:|---|
| COD-S001-booth-glow-night | Hook | A | 10 | A lone 1960s glass telephone booth glowing warm from within on an empty rain-slick night street, an anonymous silhouette inside seen through the misted glass, no face, cold navy surroundings and electric-blue reflections, intimate and isolated, museum-grade cinematic still, wide dark negative space |
| COD-S002-hidden-mic-on-booth | Hook | A | 10 | Extreme close-up of a small anonymous microphone and thin wire taped to the metal top edge of a glass phone booth at night, clandestine surveillance detail, cold electric-blue rim light, one faint gold streetlight beyond, no logos, no text, tactile museum-grade realism |
| COD-S003-handset-glow | Act1 | A | 8 | A vintage telephone handset lifted in an anonymous hand inside a booth, a soft warm glow where it meets the ear, no face, chrome and bakelite detail, cold blue glass behind, the private word made physical, no readable dial or numbers |
| COD-S004-sunset-strip-1965 | Act1 | A | 8 | A mid-1960s Los Angeles boulevard at night, wet asphalt mirroring soft neon as abstract color pools (no readable signage), period cars as dark shapes, a single lit phone booth on the corner, cinematic reconstruction, deep navy and gold, no faces |
| COD-S005-agents-listening-car | Act1 | A | 8 | Interior of a parked car at night from behind two anonymous agents' shoulders, headphones and a small reel recorder glowing between them, windshield framing a distant lit booth, tense stakeout, no faces, electric-blue dash glow, no logos |
| COD-S006-reel-recorder | Act1 | A | 8 | A reel-to-reel tape recorder turning slowly in shadow, one faint red record glow, spooling ribbon catching electric-blue light, the private call being captured, clandestine noir, no text, shallow depth of field |
| COD-S007-soundwave-from-booth | Act2 | A | 10 | A glass phone booth at night with a glowing electric-blue sound-wave leaking out through its seams into the dark air, the idea of private words escaping into surveillance, symbolic, no face, thin gold edge, generous negative space |
| COD-S008-glass-room-seen-not-heard | Act2 | A | 8 | A person's anonymous silhouette sealed inside a glowing glass booth on a bare sidewalk, fully visible yet enclosed, the paradox of being seen but expecting not to be heard, cold blue and warm interior, no face, gallery composition |
| COD-S009-old-rule-trespass | Act2 | B | 6 | A symbolic image of a heavy old door and a brass keyhole in deep shadow, the outdated idea that privacy needs a physical wall to breach, cold navy with a single gold light, no text, museum-grade still |
| COD-S010-people-not-places | Act3 | A | 8 | A lone anonymous human silhouette standing in an empty vast space, a faint protective aura of electric-blue light around only the person and not the ground, the shift from protecting places to protecting people, symbolic, no face, minimalist premium composition |
| COD-S011-courthouse-colonnade | Act3 | A | 8 | A symbolic marble courthouse colonnade at dusk, tall fluted columns receding, cold navy sky, one shaft of gold light between pillars, monumental and severe, no readable inscriptions, no identifiable real building, museum-grade architecture |
| COD-S012-expectation-of-privacy | Act3 | A | 8 | A single glowing soap-bubble-like sphere of electric-blue light enclosing a small warm point, fragile and transparent, the "reasonable expectation of privacy" made visual, deep navy void, no text, elegant symbolic still |
| COD-S013-lone-dissent | Act3 | B | 6 | A single empty judicial chair turned slightly away in cold low key, one dissenting voice, dignified and solitary, no people, no seals, shaft of blue light, museum-grade composition |
| COD-S014-modern-phones-privacy | Act4 | A | 10 | Present-day: a modern smartphone glowing on a dark table with faint electric-blue data-streams and signal arcs rising from it into the night, the "phone booth" of today, unsettling ambient surveillance, no readable screen, no icons, no faces, no logos, premium cinematic still |
| COD-S015-next-episode-highway-stop | Tease | A | 8 | A single car pulled over on a dark empty highway at night, cold headlight beams and faint red-and-blue light spill on wet asphalt (restrained, not a full wash), a lone silhouette of a police dog implied in the dark, tense traffic-stop tease, no faces, no logos, lower-third space for text |

## Additional Hero Prompts — density + variety (11–12 min cut; footage carries the rest)

| ID | Beat | Priority | Candidate Count | Prompt |
|---|---|---:|---:|---|
| COD-S016-neon-reflections-wet-street | Act1 | A | 8 | Macro of rain-wet pavement at night mirroring smeared neon into abstract electric-blue and gold streaks, no readable signs, moody 1960s city texture, cinematic, strong standalone atmosphere |
| COD-S017-coin-slot-payphone | Act1 | B | 6 | Extreme close-up of a chrome payphone coin slot and cord in warm low light, worn metal detail, the toll that "buys" privacy, cold blue shadow, no readable numbers or labels, tactile still |
| COD-S018-wire-running-into-dark | Act2 | A | 8 | A thin surveillance wire running from the top of a glass booth along a wall into the dark, following the secret path of the tap, electric-blue rim light, clandestine, no text, minimalist premium composition |
| COD-S019-ear-listening-motif | Act2 | A | 8 | A symbolic close-up of headphones resting on a dark surface with a faint glowing sound-wave curling from the cups, the act of listening, cold clinical blue, no face, shallow depth of field |
| COD-S020-booth-empty-aftermath | Act2 | B | 6 | An empty lit phone booth on a deserted night street, door ajar, the handset left hanging, quiet aftermath, cold navy and one warm interior glow, no face, gallery-quality stillness |
| COD-S021-courtroom-interior | Act3 | A | 8 | A dignified empty courtroom interior in low key, a long dark bench and tall windows, one cold shaft of light across the floor, monumental and neutral, no people, no readable text or seals, vertical calm |
| COD-S022-scales-place-vs-person | Act3 | A | 6 | A minimalist balance scale in cold low key, a small model house on one pan and a small warm human figure of light on the other, the pan with the person rising to prominence, symbolic "people not places," no faces, no text |
| COD-S023-city-of-glass-booths | Act4 | B | 6 | A wide symbolic night view of a city where scattered glass booths glow like fragile points of private light among dark buildings, the shrinking spaces of privacy, cold blue, no readable signage, premium establishing still |
| COD-S024-data-cloud-wiretap | Act4 | A | 8 | Present-day surveillance abstraction: streams of electric-blue data and call-metadata arcs flowing between dark rooftops and a distant cold server glow, modern eavesdropping without any wire, no text, no logos, no faces, cinematic |
| COD-S025-hand-on-glass-from-inside | Act4 | B | 6 | An anonymous hand pressed against the misted inner glass of a booth from inside, warm skin against cold blue condensation, the fragile membrane between private and public, no face, intimate macro, negative space |
| COD-S026-lone-booth-dawn | Ending | A | 6 | A single glass phone booth standing on an empty corner as cold dawn breaks navy-to-grey, quiet and monumental in its smallness, the case that redefined privacy, no faces, generous space for the end tag |

## Local SDXL Variant Settings (only if bulk variants are needed)

- Model: RealVisXL V5 or JuggernautXL — pick one and keep it for the whole episode.
- Sampler: DPM++ 2M Karras, 32–40 steps, CFG 4.5–6.5. Base 1344×768 → upscale 1920×1080.
- One locked seed family per episode with controlled per-scene offsets.
- Selection: semantic match, no face/likeness, no text/logos, no anatomy issues, brand fit, editability, symbolic-not-authentic clarity.

## Coverage / Handoff Notes

- These ~26 heroes cover the hook, four acts, and the EP27 (Rodriguez traffic-stop) tease with distinct anchors; footage from the factory shelf carries roughly half the shots. Remaining scenes are Remotion graphics/typography or crop/parallax variants.
- Do NOT generate exact dates, legal standards, phone numbers, or case citations in images — Remotion owns all text.
- Signature beats are the glowing booth + hidden mic + escaping sound-wave (S001, S002, S007) — generate the most candidates there (10 each).
- Continuity with EP25 Kyllo: same palette and grain; the phone-booth tease image from Kyllo (COD-S015) rhymes with S001 here.
