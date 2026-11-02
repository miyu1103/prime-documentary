# MOTIONKIT — reusable premium motion-graphics component build prompts (v001)

**Purpose:** a distributable spec pack so multiple threads/agents can build the reusable premium
motion-graphics library **in parallel**. These components are episode-agnostic and become the
backbone of the "revolution" look (Kurzgesagt/TED-Ed-style *moving* explanation, not stock+text).
Hand any numbered section to a thread; each builds ONE section's files. No two touch the same file.

---
## SHARED CONVENTIONS (every builder reads this first)
- **Working dir:** `C:\Users\aab15\Documents\prime-documentary\remotion`. Comp target: **fps 30, 1920×1080**.
- **FIRST read** `src/brand.ts` for exact `BRAND.color` (ink, navy, electric, gold, white, silver) + `BRAND.font` (display, body), and skim `src/components/Figures.tsx` for house style. Use ONLY brand tokens for color.
- **Create NEW files under `src/components/motionkit/`** (create the dir). Do NOT edit any existing file. Never touch another section's files. Filenames are given per component.
- **Imports:** `react`, `remotion` (AbsoluteFill, interpolate, spring, Easing, useCurrentFrame, useVideoConfig, Sequence, random), `@remotion/motion-blur` (`Trail`), and `../../brand`. No new npm deps.
- **QUALITY RULES (hard):** (1) every motion eased — `spring({fps,frame,config})` or `interpolate(...,{easing:Easing.out(Easing.cubic)})`; **NEVER linear**. (2) **No opacity-only reveals** — always pair with translateY/scale. (3) **Text = mask reveal**: `overflow:hidden` wrapper + inner `translateY` slide-up (切り上がり). (4) **Fast entrances get motion blur**: wrap the moving element in `<Trail layers={6} lagInFrames={1.1} trailOpacity={0.5}>`. (5) **Deterministic only**: drive everything from `useCurrentFrame()` + element index; use remotion `random('seed'+i)` — **no Math.random / Date**. (6) Timings from fps: `Math.round(fps*sec)`. (7) Full-screen scene backdrop: `radial-gradient(125% 105% at 50% 42%, ${BRAND.color.navy} 0%, #06080f 82%)`. (8) **Never fully static** — even a held state must keep a subtle eased breath/shimmer (this whole kit exists to beat the "紙芝居" gate). (9) ≥3 depth layers per full-screen scene.
- **Deliverable per component:** the .tsx file(s), each exporting the named React.FC with the given props. **MUST typecheck**: from the remotion dir run `npx tsc --noEmit -p tsconfig.json` until it exits 0. Do NOT modify `src/Root.tsx`. Report each file path, exact props signature, one-line description, "tsc clean".
- **Banned:** the gold vertical sweep (`WipeTransition`), full-screen yellow/gold wash, plain zoom/pan-only. No real-person likeness. No on-image real logos.
- Components are OVERLAYS or full-screen SCENES. Overlays take a transparent background; scenes render their own dark backdrop. Each takes an optional `dur?: number` (frames; default `useVideoConfig().durationInFrames`).

---
## SECTION 1 — Kinetic captions & titles (`src/components/motionkit/`)  [one thread]
1. **`KineticCaptions.tsx`** — `export const KineticCaptions: React.FC<{lines: string[]; style?: 'wordpop'|'maskslide'|'emphasis'; emphasisWords?: string[]; dur?: number}>`. Big lower-third-ish kinetic caption. `wordpop`: words appear one-by-one with a spring pop + slight up-move + Trail blur. `maskslide`: each line mask-reveals (translateY slide-up) staggered. `emphasis`: normal reveal but words in `emphasisWords` scale-punch + turn gold + glow. White body, gold emphasis, heavy drop-shadow, bottom-safe. Never static.
2. **`QuoteCard.tsx`** — `export const QuoteCard: React.FC<{quote: string; attribution: string; dur?: number}>`. A verbatim-quote scene: large serif/display quote types-on or mask-reveals word-group by word-group with easing; a gold quotation-mark glyph scales in; the attribution mask-reveals below with a gold underline that draws (scaleX spring). Dark backdrop, restrained, cinematic.
3. **`ActTitle.tsx`** — `export const ActTitle: React.FC<{kicker?: string; title: string; index?: number; dur?: number}>`. A chapter/act title card: a small kicker chip scales in, the big title mask-reveals with a gold underline draw, a faint act number (index) ghosts behind. Quick in, brief hold with breath, quick out.
4. **`LowerThird.tsx`** — `export const LowerThird: React.FC<{primary: string; secondary?: string; accent?: string; dur?: number}>`. A broadcast lower-third strip that slides in from the left with a motion-blur Trail, a gold accent bar that grows (scaleX), primary (bold) + secondary (muted) text mask-revealing staggered; slides out at the end. Overlay (transparent bg).

## SECTION 2 — Callout / highlight system for REAL footage (`src/components/motionkit/`)  [one thread]
These OVERLAY on top of footage/stills to point at things (Vox/Johnny-Harris style). Transparent bg.
5. **`HighlightRing.tsx`** — `export const HighlightRing: React.FC<{cx: number; cy: number; r: number; label?: string; dur?: number}>`. A hand-drawn-feeling ring/ellipse that DRAWS on around a point (`cx,cy,r` as 0..1 fractions of the frame) via `strokeDashoffset` spring, a soft glow, and an optional mask-revealed label with a tiny connector line. Gentle wobble so it's alive.
6. **`AnnotationArrow.tsx`** — `export const AnnotationArrow: React.FC<{from: [number,number]; to: [number,number]; label?: string; dur?: number}>`. An arrow whose shaft draws from `from`→`to` (0..1 coords) with a spring, arrowhead pops at the end, optional label mask-reveals near the tail. Electric or gold accent.
7. **`Spotlight.tsx`** — `export const Spotlight: React.FC<{cx: number; cy: number; r: number; dim?: number; dur?: number}>`. Darkens the whole frame except a soft-edged circular window at `cx,cy,r` (0..1); the window eases open (r springs from 0), `dim` = darkness of the masked area (default 0.72). For isolating a detail in a busy shot.
8. **`DocHighlight.tsx`** — `export const DocHighlight: React.FC<{rects: {x:number;y:number;w:number;h:number}[]; mode?: 'underline'|'box'|'redact'; dur?: number}>`. Draws animated `underline`s (grow scaleX), `box`es (draw-on stroke), or `redact` bars (wipe-in blackout) over document regions (0..1 rects), staggered. For evidence/quotes/records.

## SECTION 3 — Map system (`src/components/motionkit/`)  [one thread]
Abstract/stylized maps (geographic accuracy NOT required; a clean readable US-ish shape is fine).
9. **`RouteMap.tsx`** — `export const RouteMap: React.FC<{pins: {x:number;y:number;label?:string}[]; dur?: number}>`. A dark stylized map plane; a glowing route line draws L→R/point-to-point between pins via `strokeDashoffset` spring with an electric glint traveling the tip (Trail); each pin drops (spring + squash) and its label mask-reveals, staggered. Subtle parallax on the map.
10. **`PinDropMap.tsx`** — `export const PinDropMap: React.FC<{pins: {x:number;y:number;label?:string}[]; dur?: number}>`. A stylized map where multiple pins drop in staggered with a bounce (overshoot spring) + a ripple ring; labels mask-reveal. For "this happened in N places."
11. **`RegionHighlightMap.tsx`** — `export const RegionHighlightMap: React.FC<{label?: string; pattern?: 'uniform'|'varied'; dur?: number}>`. A stylized US map of cell-regions; `varied` lights cells in different eased colors/intensities (electric/gold/dim) NON-uniformly with a never-resolving shimmer (for "it depends where you are / unsettled"); `uniform` lights them together. Mask-revealed label.

## SECTION 4 — Data & mechanism figures (`src/components/motionkit/`)  [one thread]
12. **`VoteTally.tsx`** — `export const VoteTally: React.FC<{majority: number; dissent: number; label?: string; dur?: number}>`. Renders N seats/dots (majority+dissent) that light up staggered — majority in gold, dissent in a restrained red — resolving to e.g. "8–1"; a big mask-revealed vote number; for court votes (5–4, 8–1, 9–0). Never static.
13. **`ComparisonBars.tsx`** — `export const ComparisonBars: React.FC<{items: {label:string;value:number;accent?:string}[]; dur?: number}>`. Horizontal bars grow 0→value staggered (spring), values count in sync, 4px-rounded ends anchored to a baseline, direct labels (no tick clutter), recessive axis. For "A vs B" contrasts.
14. **`NumberTicker.tsx`** — `export const NumberTicker: React.FC<{value: number; prefix?: string; suffix?: string; decimals?: number; topLabel?: string; label?: string; dur?: number}>`. A hero number counts 0→value with `Easing.out(Easing.cubic)`, tabular-nums, a gold accent underline that draws, top kicker + bottom label mask-reveal. (Standalone StatCounter.)
15. **`MechanismReveal.tsx`** — `export const MechanismReveal: React.FC<{kind: 'closingdoor'|'gears'|'faultsplit'; dur?: number}>`. A conceptual mechanism: `closingdoor` = a vector door swinging shut (eased) with a lock click; `gears` = interlocking gears that spin up in sequence (a "system/machine"); `faultsplit` = the ground/frame cracking apart along a fault line (spring, with debris drift). Single accent, ≥3 layers, motion-blur on the fast parts.

## SECTION 5 — Atmospheric overlays (`src/components/motionkit/`)  [one thread]
Reusable transparent overlays to layer over any shot so no frame is dead. All screen-blended, subtle.
16. **`Atmospherics.tsx`** — export FOUR components in one file: `DustMotes` (drifting rising particles, deterministic, `{count?:number;color?:string}`), `SoftGlow` (one or two large soft radial glows slowly orbiting — NOT a hard sweep line, `{color?:string}`), `FilmGrain` (per-frame `feTurbulence` seed=frame%N, mixBlendMode overlay, opacity 0.05–0.09), `VignetteBreath` (a vignette whose strength gently breathes). All deterministic, all eased, all pointerEvents:none. These are the "always-alive" bed under scenes.

---
## Integration notes (Claude/me does this after build)
- I wire these into `CaseFilm.tsx` (or the EP32 composition) per the DESIGN's **perceptual motion budget**: depth cuts ≥40%, moving figures (`NumberTicker`/`VoteTally`/`ComparisonBars`/`CaseTimeline`/`FigureBeats`) ≥6, hero motion surfaces ≥2, avg cut ~2.2s, transitions via `ForcefulCut`.
- After build I **eyeball-verify** each (test-render a still/short clip) — a green typecheck is necessary, not sufficient.
- EP32-specific scenes already built (`src/components/carsearch/`): BrightLine, CarCutaway, ProbableCauseMeter, CurtilageShield, StateMap, CaseTimeline, ForcefulCut, CarKeyLock. This MOTIONKIT is the reusable layer beneath them for all episodes.
