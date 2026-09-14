# EP60 Surfside — people shots needed from Codex (v001)

## Why this file exists

`remotion/public/surfside/img` holds **112 stills and not one human being.** Measured, not
guessed: `scripts/register_face_stills.py --slug surfside` registered **0** face plates, and a
contact strip of S003 / S021 / S046 / S071 / S096 is garage, column, walkway, balcony, slab.

The photography is good. The problem is that this is a film about an engineer nobody listened
to, a board that could not agree on a bill, and ninety-eight people who died in the dark — and
right now it has no face in it. Every other episode carries `P###` people plates, and the
assembler uses them for the emotional beats. Without them EP60 renders as architecture for
forty minutes.

**These are for Codex** (project rule: long-form images come from Codex; local SDXL is only for
repairs and emergency gaps).

## Hard constraints — same as every PD episode

- **No real-person likeness.** Not Frank Morabito, not any named resident, not any official.
  Generic people only. This is invariant 11.
- **No legible text anywhere** in frame — no signage, no document text, no name tags. Generated
  text always renders as garbage and it reads as fake.
- Match the existing set: cinematic, muted palette, natural or practical light, shallow depth of
  field, 16:9, photographic — not illustration, not 3D render.
- Faces may be partly turned, lowered, backlit or cropped. Emotion should come from posture and
  hands as much as expression.

## Naming

Save as `P001.png` … `P018.png` into `episodes/PD-2026-060-surfside/04_scenes/generated_images/`.
Then run:

    .venv/Scripts/python.exe scripts/register_face_stills.py --slug surfside

which copies them into the render-visible dir and registers them as face plates.

## The shots

### Act I — the deck (the engineer)

1. **P001** — A man in his fifties in an unbranded work jacket crouching on a concrete garage
   floor, torch in one hand, looking up at the underside of a slab. Only the torch and one
   distant fixture light him. Shot from behind and slightly low.
2. **P002** — Close on a pair of hands holding a hammer against a concrete ceiling, mid-tap.
   Face out of frame. Dust in the torch beam.
3. **P003** — The same man standing alone in a stairwell writing on a clipboard, from the
   waist up, face three-quarters away, harsh overhead light.

### Act II — the report, and what was done with it

4. **P004** — Six people around a folding table in a bland community room, seen from the back of
   the room over someone's shoulder. Nobody is looking at the same thing. Fluorescent light.
5. **P005** — A woman in her sixties in a cardigan at that table, elbow down, one hand over her
   mouth, listening. Not crying — calculating.
6. **P006** — A man in a short-sleeved shirt leaning back with arms folded, faintly impatient,
   half-lit by a window behind him.
7. **P007** — A single hand pushing a stapled report across a table toward someone off-frame.
   Only the hand and the edge of a sleeve.

### Act III — the arithmetic

8. **P008** — A person alone at a kitchen table at night with a calculator and a stack of
   envelopes, head in one hand. Lamp from the left, rest of the room dark.
9. **P009** — Two neighbours talking in a bright open-air corridor, one leaning on the railing,
   both mid-sentence, body language not agreeing.
10. **P010** — An older man standing at a mailbox bank in a lobby, holding an opened envelope,
    reading, shoulders down.

### Act IV — the last spring

11. **P011** — A family of three on a balcony at golden hour seen from inside through the open
    door, backlit into near-silhouette, ordinary and warm.
12. **P012** — A child asleep in a car seat at night, streetlight passing across the window.
13. **P013** — A woman in a swimsuit and towel walking away from camera along a pool deck at
    dusk, alone, long shadow.

### The night

14. **P014** — A firefighter in full turnout gear standing still in a floodlit dust cloud,
    seen from behind, helmet down.
15. **P015** — Two rescue workers on a debris pile at night, small in frame, work lights
    throwing long shadows, everything else black.
16. **P016** — A crowd of people standing behind a barrier tape at night, faces mostly turned
    away or lowered, one person holding a phone to their ear.

### Ending

17. **P017** — Hands tying a bunch of flowers to a chain-link fence. No faces. Early morning
    light.
18. **P018** — A wide, still shot of a person standing alone facing an empty lot at sunrise,
    seen from behind, very small in the frame.

## After delivery

`check_episode_inputs.py --slug surfside` will still report the other three gaps
(narration audio, factory clips, Remotion composition) — those are mine to build, not yours.
