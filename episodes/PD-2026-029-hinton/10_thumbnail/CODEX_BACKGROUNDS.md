# EP29 hinton — thumbnail background art (Codex hand-off)

The video passes 20/21 acceptance gates. The ONLY remaining hard gate is
`thumbnail_ready` (needs ≥3 thumbnails @1280×720 + a selected one). Per the design
(`EP29_hinton_thumb_prompts.v001.md`, rule 19) the backgrounds are **Codex-generated**.

## What to generate (Codex) — 3 backgrounds, each 1280×720

Common spec (ALL): 1280×720 · huge subject · very high contrast · black / deep-navy
ground · ONE accent color only = gold `#E5B53A` **or** electric `#1F6BFF` · cinematic ·
reads at 320px · **no real-person face · no on-image text · no logo** · leave negative
space (top or one side) for a headline.

- **bg1.png** — A death-row cell's heavy steel door filling the frame in deep navy shadow,
  a single hard shaft of **gold** light breaking across it from one side, dust in the beam.
  Vast dark space top-left for a headline. Oppressive, then a sliver of hope. No text, no faces.
- **bg2.png** — Extreme macro of a single bullet on a steel surface, a cracked/shattered
  "match" implied by a fracture of light across it, deep black background, one **gold** glint.
  Clinical and cold. Room to the right for a headline. No text, no faces.
- **bg3.png** — A five-by-seven death-row cell seen through bars, a lone shaft of daylight on
  the concrete floor, an anonymous figure's shadow (no face), navy tones with a single warm
  accent. Claustrophobic. Headline space top. No text, no faces.

## Where to drop them
`remotion/public/hinton/thumb/bg1.png`, `bg2.png`, `bg3.png` (long-edge ≥1280 is fine;
they are composited under the headline).

## Then (auto) — one command to green the gate
```
py -3.11 scripts/build_hinton_thumbnails.py --select A
py -3.11 scripts/check_final_acceptance.py 29 --render remotion/out/hinton_final.v001.bgm.mp4 --emit-receipt
```
Headlines are baked into the registered Still comps (Thumb-hinton-A/B/C):
A = `30 YEARS. INNOCENT.` · B = `THE BULLETS LIED` · C = `THEY WANTED HIM DEAD`.
Swap `--select` to pick the cover. Expect a GREEN receipt (owner review of title/thumb still required).
