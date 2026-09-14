# motion3d — premium-motion reference prototypes

Reference implementations for the premium 3D / hero / figures tier.
**Spec:** `docs/PD_MOTION3D_HERO_AND_FIGURES_SPEC.md`.

**These are prototypes, not wired into production `Root.tsx`.** They were built in the pino-channel Remotion
workbench and copied here for version control. `@remotion/three` is not yet installed in this `remotion/`.

- `Opening3D.tsx` — L1 real-3D openings (`OpeningDoc3D` / `OpeningMotion3D` / `OpeningPhoto3D`). Needs
  `@remotion/three three @react-three/fiber@8`.
- `Figures.tsx` — animated figures (`StatCounter` / `Timeline` / `BarChart` / `NetworkDiagram`). Port target:
  merge into `src/components/DiagramFlow.tsx`.
- `blender/bpp_eevee.py` — L2 EEVEE fast hero (Blender 5.1 headless).
- `blender/bpp_cycles.py` — L3 Cycles glass hero (OptiX GPU).

Blender: `blender -b -P blender/bpp_cycles.py -- <OUT> 1920 1080 1 100 160`
Encode:  `npx remotion ffmpeg -framerate 30 -i <OUT>/f_%04d.png -c:v libx264 -crf 16 -pix_fmt yuv420p -y hero.mp4`

Shipping in an episode = the owner-gated port in the spec §5.
