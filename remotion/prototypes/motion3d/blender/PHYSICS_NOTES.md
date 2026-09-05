# bpp_physics.py — challenge #4: rigid-body collapse

Blender rigid-body: a block tower toppled by a strong WIND force field + a falling
glowing core → collapse (metaphor: 崩れる暮らし/証言/金庫). EEVEE + Glare Bloom + DOF.

## Blender 5.1 gotchas (locked)
- **A single-frame STILL render does NOT run the sim** — `bpy.ops.ptcache.bake_all`
  is unreliable headless, so a still shows frame-1 (initial) positions. **Always render
  the ANIMATION (`render(animation=True)` from frame 1)** — it steps physics forward per
  frame and simulates correctly. (This misled the whole first diagnosis.)
- Kinematic animated "wrecking ball" did NOT collide reliably → use a **WIND force field**
  (`effector_add(type='WIND')`, `field.strength` keyframed 95→0 over frames 1-18) to topple.
  Rigid-body world respects force fields by default (`effector_weights`).
- friction 0.35 / restitution 0.05 so blocks slide and scatter (0.7 was too sticky = no collapse).
- Engine `BLENDER_EEVEE`; encode PNGseq → `libx264 crf16 yuv420p` (row 6).

Run: `blender -b -P bpp_physics.py -- <OUT> 1920 1080 1 90 96`  (owner-gated, point use only)
