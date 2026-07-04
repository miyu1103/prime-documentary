# PD PREMIUM MOTION: 3D HERO + FIGURES SPEC (tier addition)

**Status:** Owner directive 2026-07-05. **Additive premium-motion tier.** This does **NOT** replace the
OP/ED canonical (`remotion/src/components/Bookends.tsx`) or the existing `DiagramFlow`/`Parallax`
components — it raises the ceiling above them (CLAUDE invariant 14: extend, do not fork). Elective per
episode; when used, it must be built to the exact numbers below (root-CLAUDE ethos + v2 §E: Codex reads
this standalone, zero interpretation room).

**Why:** the recurring "アニメがしょぼい / 紙芝居" defect (v2 row 8, ship-gate `animation_density`) is a
depth + render-quality problem. 2D板の合成では奥行きが出ない。This tier adds (1) real 3D depth in Remotion,
(2) a Blender-rendered hero shot at film/CM quality, (3) richer in-body figures for retention (v2 row 16).

**Binds with:** v2 rows **8 (animation), 14 (OP/ED), 16 (retention)**, row **6 (encode)**. Encode of any
rendered sequence uses the row-6 values verbatim (libx264 / crf16 / yuv420p / bt709 / aac320k).

---

## 0. Motion quality ladder (measured on this Windows/RTX node, 2026-07-05)

| Tier | Engine | Look | Render cost (1080p) | Use |
|---|---|---|---|---|
| L0 (baseline) | Remotion 2D板 | 旧OP／板の合成 | instant | 避ける（紙芝居の主因） |
| **L1 depth** | `@remotion/three` (WebGL) | 本物の奥行き・パララックス・DOF風 | ~real-time render | OP背景プレート・タイトル奥行き |
| **L2 hero (fast)** | Blender **EEVEE** | 発光ジェム＋ブルーム＋反射床＋DOF | **~1.8 s/frame** (90–120f ≈ 1–2 min) | 掴みヒーロー・章トランジション |
| **L3 hero (ceiling)** | Blender **Cycles** (OptiX GPU) | 本物のガラス屈折・ベベル・GI | **~8 s/frame** (100f ≈ 13 min) | 最上級の掴み1カット |

L3の"さらに上"（分散/HDRI環境/ボリューメトリック/8K→1080p縮小）は可能だが frame 時間が延びる。品質⇔時間のトレードオフを話者承認で選ぶ。

---

## 1. L1 — Real 3D depth in Remotion (`@remotion/three`)

**Deps (pin to remotion 4.0.x line):**
```
npm i @remotion/three@4.0.484 three @react-three/fiber@8 @types/three
```
**Rule:** camera moves through a real 3D scene (`ThreeCanvas`), so near/far elements parallax automatically.
Drive ALL motion from `useCurrentFrame()` (never r3f `useFrame` — nondeterministic; breaks Codex reproducibility).

**Canonical uses:**
- **OP background plate** behind `BrandOpening` (Bookends stays the title layer; 3D is only the backdrop → invariant 14).
- **Photo-parallax title card:** real footage on a 3D plane + slow dolly + foreground out-of-focus bokeh
  (faster than the plate = depth) + grade + grain + vignette. This is the documentary title-card look.

**Quality numbers (mandatory):**
- Every motion eased: `spring{damping,mass}` or `Easing.out(Easing.cubic)`. **等速線形禁止.**
- **No opacity-only** reveals — pair with `translateY`/`scale`.
- Text = `overflow:hidden` + `translateY` mask reveal, **1文字スタッガー ≈ 0.045 s**.
- Fast moves get `@remotion/motion-blur` `Trail`. **NOTE:** never wrap a bare inline flex row in `Trail`
  (collapses layout → garbled glyphs); wrap an `AbsoluteFill`, or omit Trail on slow title-card rises.
- ≥3 back layers (grad bg / grid / glow). Film grain = per-frame `feTurbulence` (seed = `frame%N`),
  `mixBlendMode:overlay`, opacity 0.05–0.09. Vignette via radial-gradient overlay.
- Timing from fps (`Math.round(fps*sec)`) — no hardcoded frames.
- Deterministic randomness: seeded `mulberry32` (no `Math.random`).

**Reference impl:** `remotion/prototypes/motion3d/Opening3D.tsx` (`OpeningDoc3D` / `OpeningMotion3D` /
`OpeningPhoto3D`; props `{title,subtitle,accent,hasLogo[,image]}`). To ship in production it is **ported into
`remotion/src/components/`** with the deps above installed (port is owner-gated — see §5).

---

## 2. L2/L3 — Blender hero render pipeline

Blender **5.1** at `C:\Program Files\Blender Foundation\Blender 5.1\blender.exe`. Headless:
```
blender -b -P <script.py> -- <OUT> <RX> <RY> <FS> <FE> <SAMPLES>
```
`FS==FE` → single test still `<OUT>_test.png`; else → PNG sequence `<OUT>/f_0001.png…` (Blender 5.x removed
in-app FFMPEG video output — **always render PNG seq, encode separately**).

**Blender 5.1 API gotchas (locked):**
- EEVEE engine id = `BLENDER_EEVEE` (not `..._NEXT`). Cycles = `CYCLES`.
- Compositor: `scene.node_tree` is gone → create a `CompositorNodeTree` and assign to
  `scene.compositing_node_group`; final node = `NodeGroupOutput` (add a `NodeSocketColor` "Image").
- Glare node controls are **input sockets**, not properties: `Type='Bloom'`, `Quality='High'`,
  `Highlights Threshold=0.75`, `Strength=1.0`, `Size=0.8` (menu values are the display strings).
- Actions are slotted: `action.fcurves` removed — do **not** set fcurve interpolation; default bezier easing
  is fine (and satisfies the "no linear" rule).
- Principled input names are 4.x-style: `Emission Color`+`Emission Strength`, `Specular IOR Level`,
  `Transmission Weight`, `Coat Weight`.

### L2 EEVEE (fast hero)
Engine `BLENDER_EEVEE`; `taa_render_samples` 96–192; `use_raytracing/use_ssr/use_gtao=True`.
Gem = faceted icosphere (flat-shaded), dark metallic (Metallic 0.88, Roughness 0.16, `Coat Weight` 0.35)
+ emissive wireframe overlay (Wireframe modifier 0.03, `Emission Strength` ~6) + emissive core. Orbiting
emissive satellites. Reflective metallic floor. 3-point area lights + 3 off-camera emissive **softboxes**
(strength 1.4/1.1/0.8) for metallic highlights. Camera DOF `aperture_fstop` 2.2, focus on gem. Bloom via
Glare(Bloom). ~1.8 s/frame @1080p. **Reference:** `remotion/prototypes/motion3d/blender/bpp_eevee.py`.

### L3 Cycles (ceiling hero)
Engine `CYCLES`; device GPU: try `OPTIX`→`CUDA`→`HIP`→`ONEAPI`, enable all non-CPU devices, else CPU.
`cycles.samples` 160–200, `use_denoising=True`; `view_settings.view_transform='AgX'` (cinematic).
Gem = **glass**: Principled `Transmission Weight=1.0`, `Roughness=0.02`, `IOR=1.85`, faint blue base;
**Bevel modifier** width 0.025 / 3 segments (edges catch light). Emissive core `Emission Strength≈2.2`
(higher blows out through the glass lens). Softboxes strength 1.4/1.1/0.8. Bloom via Glare(Bloom).
**~8 s/frame @1080p on OptiX.** **Reference:** `remotion/prototypes/motion3d/blender/bpp_cycles.py`.

### Encode (row-6 compliant)
```
npx remotion ffmpeg -framerate 30 -i <OUT>/f_%04d.png -c:v libx264 -crf 16 -pix_fmt yuv420p -y hero.mp4
```
(Remotion bundles ffmpeg; no external install.) fps = 30 for hero clips.

### Integrate into the episode
Bring `hero.mp4` into Remotion as `OffthreadVideo` behind `BrandOpening` **as the hook/cold-open hero plate,
before the gold BrandOpening lands** (v2 row 9/10/14 ordering unchanged). The 3D render is an abstract
generated visual → invariant 11 satisfied (no real-person likeness, not presented as record).

---

## 3. Figures tier (extends `DiagramFlow`, for retention row 16)

Four animated figure types, single-accent palette, dark surface. Used in-body to explain, killing the
"static image bores" failure (row 8) and building the retention curve (row 16).

- **StatCounter** — hero number counts 0→value with `Easing.out(Easing.cubic)`, accent underline, label.
- **Timeline** — baseline draws L→R (spring), event dots pop staggered (0.18 s), year+caption mask-rise, alternating above/below.
- **BarChart** — bars grow 0→value staggered (0.12 s), value counts in sync, **4px rounded data-ends anchored to baseline**, **direct labels** (no number-on-every-tick clutter), recessive axis.
- **NetworkDiagram** — edges draw via `strokeDashoffset` (spring), nodes pop + label ("follow the money" relationship map).

**Palette (dataviz-validated approach):** single accent hue for data (sequential/identity), text in ink
tokens (`#fff`/`#c8d2e6`/`#6b7688`) **never the series color**, axis/grid recessive. If a future figure needs
≥2 categorical series, run the categorical-palette validator before shipping (CVD ≥ 12).

**Reference impl:** `remotion/prototypes/motion3d/Figures.tsx` (`StatCounter/Timeline/BarChart/NetworkDiagram`
+ `Figures` showcase; props data-driven). Port target = merge as new variants of
`remotion/src/components/DiagramFlow.tsx` (do not create a parallel diagram system — invariant 14).

---

## 4. Gate (proposed; manual until coded — v2 §C convention)

Add to the acceptance ladder (initially manual, then code into `check_final_acceptance.py`):
- `hero_present` (if tier elected): a hero plate exists in the hook window, is `OffthreadVideo` (real render,
  not a still), resolution 1920×1080, encoded crf ≤17 / yuv420p (reuses row-6 assertion).
- `figure_density` (retention): explainer spans use ≥1 animated figure per major claim block; 0 static
  figure holds > 2 s (rolls into row 8 motion audit).
- All L1/L2/L3 quality numbers in §1–§3 are the spec; violations = rework (same as v2 rows).

Until coded these are **manual** review items (like rows 5/7/12/13/15). No silent cap (rule 17): if a hero is
skipped for time, log it.

---

## 5. Port status & next step (owner-gated)

Reference implementations currently live under `remotion/prototypes/motion3d/` (prototyped in the
pino-channel Remotion workbench, copied here for version control). They are **not yet wired into the
production `Root.tsx`** and `@remotion/three` is **not yet installed** in `remotion/`. Shipping in an episode
requires the one-time port:
1. `npm i @remotion/three@4.0.484 three @react-three/fiber@8 @types/three` in `remotion/`.
2. Port `OpeningPhoto3D` behind `BrandOpening`; merge `Figures` into `DiagramFlow`.
3. Add the §4 gates.

This port is a bounded vertical slice (rule 18) and an owner-gated change to the binding motion path — do it
as its own reviewed commit, not silently inside an episode render.
