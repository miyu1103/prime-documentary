// =====================================================================
// EP35 "hinders" — @remotion/three HERO FigureBeats (5 of the 8 heroes).
//
//   F3   ThresholdMeter         — real 3D $10,000 reporting-threshold gauge
//   F11  PolicyReversalTimeline — 3D spine, camera fly-through, WITHOUT PREJUDICE
//   F14  McLellanParallel       — two displacement planes (Iowa | North Carolina)
//   F14b McLellanLedger         — 3D ledger, instancedMesh(301) sequential light-up
//   F15  TIGTA-Dots             — instancedMesh(278), 91% (253) green / 9% (25) red
//
// Discipline (manifest §SH.0 / §SH.1 / §5 / §6):
//   - Fully DETERMINISTIC. Every camera / mesh / instance transform is derived
//     from useCurrentFrame(). r3f `useFrame` is BANNED (non-deterministic, breaks
//     Codex frame reproducibility) — instead the camera is set from frame-derived
//     props inside the render body (the DepthCamV idiom from Short.tsx) and
//     instanced matrices/colors are written in a per-render useLayoutEffect keyed
//     to the current frame.
//   - All easing required (spring{damping,mass} or Easing.out(Easing.cubic)); no
//     constant-velocity linear motion.
//   - No opacity-only reveals — always paired with translateY / scale.
//   - Deterministic RNG only (mulberry32); Math.random is banned.
//   - MSAA on (gl={{antialias:true}}). A thin 2D headline layer (MaskTitle) and
//     FigureFX grain/vignette sit in front of every 3D canvas.
//   - No forbidden motion: no gold vertical sweep, no orbiting faint light, no
//     lissajous, no fixed-position glow "breathing", no blink. Motion is
//     reveal-driven one-directional OR event-driven, and a secondary structural
//     motion continues to cut-end so no ROI freezes >0.67s.
//   - Fact numbers are frozen: $10,000 / 301 / ~$2M / 278 / 91% (=253 green / 25
//     red). Never altered.
//
// Extends (does NOT fork) the established 3D grammar:
//   src/compositions/Short.tsx  (ThreeCanvas + useThree camera-from-frame +
//                                subdivided plane displacementMap)
//   prototypes/motion3d/Figures.tsx (spring/Easing motion, count-ups, staggers)
// and the shared ./theme primitives.
// =====================================================================
import React from 'react';
import {
  AbsoluteFill,
  Easing,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import {ThreeCanvas} from '@remotion/three';
import {useThree} from '@react-three/fiber';
import * as THREE from 'three';
import {
  BG,
  INK,
  INK2,
  MUTED,
  LANES,
  FigureFX,
  FigureProps,
  HinderBackdrop,
  MaskTitle,
  mulberry32,
  resolveAccent,
  resolveTokens,
  sceneFade,
  sec,
} from './theme';

// ---------------------------------------------------------------------
// Shared 3D helpers
// ---------------------------------------------------------------------

/** Set the camera from frame-derived props inside render (the DepthCamV idiom
 *  from Short.tsx) — deterministic, no r3f useFrame. */
const Rig: React.FC<{pos: [number, number, number]; look: [number, number, number]}> = ({pos, look}) => {
  const camera = useThree((s) => s.camera);
  camera.position.set(pos[0], pos[1], pos[2]);
  camera.lookAt(look[0], look[1], look[2]);
  camera.updateProjectionMatrix();
  return null;
};

/** Canvas shell: MSAA on, deterministic camera rig, shared 3-point-ish lights. */
const Stage: React.FC<{
  width: number;
  height: number;
  camPos: [number, number, number];
  look: [number, number, number];
  accent: string;
  fov?: number;
  children: React.ReactNode;
}> = ({width, height, camPos, look, accent, fov = 42, children}) => (
  <ThreeCanvas
    width={width}
    height={height}
    camera={{fov, position: camPos, near: 0.1, far: 200}}
    gl={{antialias: true}}
    style={{position: 'absolute'}}
  >
    <Rig pos={camPos} look={look} />
    <ambientLight intensity={1.15} />
    <pointLight position={[6, 7, 8]} intensity={140} color={'#ffffff'} />
    <pointLight position={[-7, -3, 6]} intensity={90} color={accent} />
    {children}
  </ThreeCanvas>
);

/** Instanced field whose per-instance matrix + color are rewritten every frame in
 *  a useLayoutEffect (runs on each re-render, i.e. each frame). Fully
 *  deterministic — no r3f useFrame. This is how we drive instancedMesh(301) and
 *  instancedMesh(278) from useCurrentFrame(). */
const InstancedField: React.FC<{
  count: number;
  geo: React.ReactNode;
  /** write instance i's transform into `o` and its color into `col`. */
  update: (i: number, o: THREE.Object3D, col: THREE.Color) => void;
}> = ({count, geo, update}) => {
  const ref = React.useRef<THREE.InstancedMesh>(null);
  const dummy = React.useMemo(() => new THREE.Object3D(), []);
  const col = React.useMemo(() => new THREE.Color(), []);
  // No dependency array on purpose: useCurrentFrame() changes each frame ->
  // parent re-renders -> this effect re-runs with the fresh `update` closure.
  React.useLayoutEffect(() => {
    const mesh = ref.current;
    if (!mesh) return;
    for (let i = 0; i < count; i++) {
      update(i, dummy, col);
      dummy.updateMatrix();
      mesh.setMatrixAt(i, dummy.matrix);
      mesh.setColorAt(i, col);
    }
    mesh.instanceMatrix.needsUpdate = true;
    if (mesh.instanceColor) mesh.instanceColor.needsUpdate = true;
  });
  return (
    <instancedMesh
      ref={ref}
      args={[undefined as unknown as THREE.BufferGeometry, undefined as unknown as THREE.Material, count]}
    >
      {geo}
      <meshBasicMaterial toneMapped={false} />
    </instancedMesh>
  );
};

/** A near foreground plate that keeps drifting (one-directional eased) so the
 *  foreground layer never freezes — genuine L3 near/mid/far parallax. */
const NearPlate: React.FC<{
  frame: number;
  dur: number;
  color: string;
  x: number;
  y?: number;
  z: number;
  w?: number;
  h?: number;
  amp?: number;
}> = ({frame, dur, color, x, y = -1.5, z, w = 2.6, h = 1.1, amp = 0.55}) => {
  const dx = interpolate(frame, [0, Math.max(1, dur)], [0, amp], {
    easing: Easing.out(Easing.cubic),
    extrapolateRight: 'clamp',
  });
  return (
    <mesh position={[x + dx, y, z]}>
      <planeGeometry args={[w, h]} />
      <meshBasicMaterial color={color} transparent opacity={0.18} toneMapped={false} />
    </mesh>
  );
};

/** Deterministic grayscale relief canvas used as a stand-in displacement/height
 *  map. mulberry32-seeded so every frame/render is identical. */
const useProcTexture = (seed: number): THREE.CanvasTexture =>
  React.useMemo(() => {
    const rnd = mulberry32(seed);
    const c = document.createElement('canvas');
    c.width = 256;
    c.height = 256;
    const ctx = c.getContext('2d') as CanvasRenderingContext2D;
    const g = ctx.createLinearGradient(0, 0, 256, 256);
    g.addColorStop(0, '#141414');
    g.addColorStop(1, '#8a8a8a');
    ctx.fillStyle = g;
    ctx.fillRect(0, 0, 256, 256);
    for (let i = 0; i < 180; i++) {
      const x = rnd() * 256;
      const y = rnd() * 256;
      const r = 5 + rnd() * 28;
      const v = Math.floor(50 + rnd() * 190);
      ctx.fillStyle = `rgba(${v},${v},${v},0.14)`;
      ctx.beginPath();
      ctx.arc(x, y, r, 0, Math.PI * 2);
      ctx.fill();
    }
    const tex = new THREE.CanvasTexture(c);
    tex.colorSpace = THREE.SRGBColorSpace;
    return tex;
  }, [seed]);

/** A readable 3D panel label (e.g. "WITHOUT PREJUDICE") drawn to a CanvasTexture
 *  so the phrase genuinely lives in the 3D scene, not just as a 2D caption. */
const useLabelTexture = (text: string, fg: string): THREE.CanvasTexture =>
  React.useMemo(() => {
    const c = document.createElement('canvas');
    c.width = 512;
    c.height = 128;
    const ctx = c.getContext('2d') as CanvasRenderingContext2D;
    ctx.fillStyle = 'rgba(6,8,15,0.86)';
    ctx.fillRect(0, 0, 512, 128);
    ctx.strokeStyle = fg;
    ctx.lineWidth = 5;
    ctx.strokeRect(8, 8, 496, 112);
    ctx.fillStyle = fg;
    ctx.font = '700 40px Inter, system-ui, sans-serif';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(text, 256, 66);
    const tex = new THREE.CanvasTexture(c);
    tex.colorSpace = THREE.SRGBColorSpace;
    return tex;
  }, [text, fg]);

/** eased 0..1 helper */
const ease01 = (frame: number, a: number, b: number, easing = Easing.out(Easing.cubic)): number =>
  interpolate(frame, [a, b], [0, 1], {easing, extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});

// Shared overlay wrapper for the 2D headline/readout layer (translateY reveal —
// never opacity-only).
const OverlayLayer: React.FC<{opacity: number; y: number; children: React.ReactNode}> = ({opacity, y, children}) => (
  <AbsoluteFill style={{opacity, transform: `translateY(${y}px)`, pointerEvents: 'none'}}>{children}</AbsoluteFill>
);

// =====================================================================
// F3 — ThresholdMeter (hero, federal). Real 3D $10,000-threshold gauge.
//   Independent motion elements (>=6):
//     1. deposit blocks (8) pseudo-gravity stagger-stack (spring, stagger 6f)
//     2. gauge needle sweep 0-60f  (Easing.inOut(quad))
//     3. gauge fill-arc growth (thetaLength grows with needle)
//     4. camera front -> oblique dolly 0-60f (Easing.out cubic)
//     5. post-completion micro-light running along the arc (freeze-killer)
//     6. near "slip" plate parallax drift (one-directional eased)
//   + 2D MaskTitle "$10,000 REPORTING THRESHOLD".
// =====================================================================

const N_BLOCKS = 8;

const GaugeArc: React.FC<{radius: number; fill: number; accent: string; accentHi: string}> = ({
  radius,
  fill,
  accent,
  accentHi,
}) => (
  <group position={[0, -0.2, 0]}>
    {/* base half-arc (upper semicircle) */}
    <mesh>
      <ringGeometry args={[radius - 0.16, radius, 96, 1, 0, Math.PI]} />
      <meshBasicMaterial color={accent} transparent opacity={0.28} toneMapped={false} side={THREE.DoubleSide} />
    </mesh>
    {/* filled portion grows with the needle */}
    <mesh>
      <ringGeometry args={[radius - 0.16, radius, 96, 1, 0, Math.max(0.001, Math.PI * fill)]} />
      <meshBasicMaterial color={accentHi} toneMapped={false} side={THREE.DoubleSide} />
    </mesh>
  </group>
);

export const ThresholdMeter: React.FC<FigureProps> = (p) => {
  const frame = useCurrentFrame();
  const {fps, width, height} = useVideoConfig();
  const accent = resolveAccent(p);
  const tok = resolveTokens(p);
  const {opacity, y} = sceneFade(frame, p.dur);

  const REVEAL = sec(fps, 1.0); // 60f @60fps
  const R = 2.4;

  // needle sweep (2) & fill (3)
  const needleP = interpolate(frame, [0, REVEAL], [0, 1], {
    easing: Easing.inOut(Easing.quad),
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const needleAngle = Math.PI * (1 - needleP); // sweep left(PI) -> right(0)

  // camera front -> oblique dolly (4)
  const dolly = ease01(frame, 0, REVEAL);
  const camPos: [number, number, number] = [dolly * 3.4, 0.6 + dolly * 1.9, 6.4 - dolly * 1.1];

  // post-completion micro-light running along the arc (5)
  const doneF = Math.max(0, frame - REVEAL);
  const lightAngle = Math.PI * (1 - ((doneF * 0.05) % 1));
  const lightOn = interpolate(frame, [REVEAL, REVEAL + 8], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});

  return (
    <AbsoluteFill style={{backgroundColor: BG}}>
      <HinderBackdrop accent={accent} tint={tok.tint} />
      <AbsoluteFill style={{opacity, transform: `translateY(${y}px)`}}>
        <Stage width={width} height={height} camPos={camPos} look={[0, 0.4, 0]} accent={accent}>
          <GaugeArc radius={R} fill={needleP} accent={accent} accentHi={tok.accentHi} />

          {/* needle (2) */}
          <mesh position={[(Math.cos(needleAngle) * R) / 2, -0.2 + (Math.sin(needleAngle) * R) / 2, 0.05]} rotation={[0, 0, needleAngle]}>
            <boxGeometry args={[R, 0.07, 0.07]} />
            <meshBasicMaterial color={tok.accentHi} toneMapped={false} />
          </mesh>
          <mesh position={[0, -0.2, 0.06]}>
            <cylinderGeometry args={[0.16, 0.16, 0.1, 24]} />
            <meshStandardMaterial color={accent} emissive={accent} emissiveIntensity={0.6} />
          </mesh>

          {/* deposit blocks pseudo-gravity stagger-stack (1) */}
          {Array.from({length: N_BLOCKS}).map((_, i) => {
            const s = spring({frame: frame - i * sec(fps, 0.1), fps, config: {damping: 10, mass: 1}});
            const targetY = -1.9 + i * 0.34;
            const yy = interpolate(s, [0, 1], [3.4, targetY]); // falls from above
            const sc = interpolate(s, [0, 0.55, 1], [0.25, 1.12, 1]); // squash on land
            const glow = 0.25 + 0.4 * s;
            return (
              <mesh key={i} position={[-3.2, yy, 0.1]} scale={[1, sc, 1]}>
                <boxGeometry args={[1.5, 0.28, 0.5]} />
                <meshStandardMaterial color={accent} emissive={accent} emissiveIntensity={glow} roughness={0.4} metalness={0.1} />
              </mesh>
            );
          })}

          {/* post-completion micro-light on arc (5) */}
          <mesh
            position={[Math.cos(lightAngle) * R, -0.2 + Math.sin(lightAngle) * R, 0.12]}
            scale={[lightOn, lightOn, lightOn]}
          >
            <sphereGeometry args={[0.12, 16, 16]} />
            <meshBasicMaterial color={'#ffffff'} toneMapped={false} />
          </mesh>

          {/* near slip plate parallax (6) */}
          <NearPlate frame={frame} dur={p.dur} color={accent} x={2.4} z={2.1} amp={0.7} />
        </Stage>
      </AbsoluteFill>

      <OverlayLayer opacity={opacity} y={y}>
        <div style={{position: 'absolute', top: 132, left: 150}}>
          <MaskTitle text="$10,000" start={0.1} size={112} weight={800} color={INK} />
          <div style={{marginTop: 6}}>
            <MaskTitle text="REPORTING THRESHOLD" start={0.28} size={40} weight={600} color={tok.accentHi} stagger={0.03} />
          </div>
        </div>
        <div
          style={{
            position: 'absolute',
            bottom: 96,
            left: 150,
            fontFamily: 'Inter, system-ui, sans-serif',
            fontSize: 24,
            letterSpacing: 6,
            textTransform: 'uppercase',
            color: MUTED,
          }}
        >
          Deposit at or above ${'→'} bank must report
        </div>
      </OverlayLayer>

      <FigureFX />
    </AbsoluteFill>
  );
};

// =====================================================================
// F11 — PolicyReversalTimeline (hero, federal). 3D spine + camera fly-through.
//   Independent motion elements (>=6):
//     1. camera fly-through following the playhead (x + z travel)
//     2. playhead marker continuous rightward slide (Easing.inOut quad)
//     3. node latch pops (staggered, event-driven when playhead passes node)
//     4. zoompunch scale (1 -> 1.12 -> 1) on each node latch
//     5. "WITHOUT PREJUDICE" 3D CanvasTexture panels (camera parallax + latch reveal)
//     6. data-flow particles drifting +x along the spine (instanced)
//   + 2D MaskTitle "2014 · POLICY REVERSAL".
// =====================================================================

const TL_MINX = -6;
const TL_MAXX = 6;
const TL_NODES = [-4.2, -2.1, 0, 2.1, 4.2];

export const PolicyReversalTimeline: React.FC<FigureProps> = (p) => {
  const frame = useCurrentFrame();
  const {fps, width, height} = useVideoConfig();
  const accent = resolveAccent(p);
  const tok = resolveTokens(p);
  const {opacity, y} = sceneFade(frame, p.dur);

  const T = Math.max(1, Math.round(p.dur * 0.9));
  const label = useLabelTexture('WITHOUT PREJUDICE', tok.accentHi);

  // playhead x — continuous eased rightward scan (2)
  const playheadAt = React.useCallback(
    (f: number) =>
      interpolate(f, [0, T], [TL_MINX, TL_MAXX], {
        easing: Easing.inOut(Easing.quad),
        extrapolateLeft: 'clamp',
        extrapolateRight: 'clamp',
      }),
    [T],
  );
  const headX = playheadAt(frame);

  // deterministic latch frame per node (first frame the eased playhead crosses it)
  const latchFrames = React.useMemo(() => {
    return TL_NODES.map((nx) => {
      for (let f = 0; f <= T; f++) {
        if (playheadAt(f) >= nx) return f;
      }
      return T;
    });
  }, [T, playheadAt]);

  // camera follows the playhead (1)
  const camPos: [number, number, number] = [headX * 0.55, 1.1, 6.2];
  const look: [number, number, number] = [headX * 0.55, 0, -1.5];

  return (
    <AbsoluteFill style={{backgroundColor: BG}}>
      <HinderBackdrop accent={accent} tint={tok.tint} />
      <AbsoluteFill style={{opacity, transform: `translateY(${y}px)`}}>
        <Stage width={width} height={height} camPos={camPos} look={look} accent={accent} fov={48}>
          {/* spine */}
          <mesh position={[0, -0.6, 0]}>
            <boxGeometry args={[TL_MAXX - TL_MINX + 1.2, 0.05, 0.05]} />
            <meshBasicMaterial color={accent} transparent opacity={0.5} toneMapped={false} />
          </mesh>

          {/* nodes: latch pop (3) + zoompunch (4) + WITHOUT PREJUDICE panel (5) */}
          {TL_NODES.map((nx, i) => {
            const lf = latchFrames[i];
            const s = spring({frame: frame - lf, fps, config: {damping: 12, mass: 0.7}});
            const punch = interpolate(frame - lf, [0, 4, 9], [1, 1.12, 1], {
              extrapolateLeft: 'clamp',
              extrapolateRight: 'clamp',
            });
            const grow = interpolate(s, [0, 1], [0.0001, 1]); // scale reveal (not opacity)
            const bloom = interpolate(frame - lf, [0, 5, 26], [0, 1, 0.32], {
              extrapolateLeft: 'clamp',
              extrapolateRight: 'clamp',
            });
            return (
              <group key={i} position={[nx, -0.6, 0]}>
                {/* node core */}
                <mesh position={[0, 0, 0]} scale={[grow * punch, grow * punch, grow * punch]}>
                  <sphereGeometry args={[0.22, 20, 20]} />
                  <meshBasicMaterial color={tok.accentHi} toneMapped={false} />
                </mesh>
                {/* latch bloom halo (one-shot decay, NOT a breathing loop) */}
                <mesh scale={[grow, grow, grow]}>
                  <sphereGeometry args={[0.5, 16, 16]} />
                  <meshBasicMaterial color={accent} transparent opacity={0.22 * bloom} toneMapped={false} />
                </mesh>
                {/* WITHOUT PREJUDICE 3D panel */}
                <mesh position={[0, 1.05, 0]} scale={[grow, grow, grow]}>
                  <planeGeometry args={[1.9, 0.48]} />
                  <meshBasicMaterial map={label} transparent toneMapped={false} side={THREE.DoubleSide} />
                </mesh>
                {/* riser connecting node to panel */}
                <mesh position={[0, 0.55, 0]} scale={[1, grow, 1]}>
                  <boxGeometry args={[0.03, 0.9, 0.03]} />
                  <meshBasicMaterial color={accent} transparent opacity={0.5} toneMapped={false} />
                </mesh>
              </group>
            );
          })}

          {/* playhead marker (2) */}
          <mesh position={[headX, -0.6, 0.2]}>
            <boxGeometry args={[0.08, 1.5, 0.08]} />
            <meshBasicMaterial color={'#ffffff'} toneMapped={false} />
          </mesh>
          <mesh position={[headX, -0.6, 0.2]}>
            <sphereGeometry args={[0.16, 16, 16]} />
            <meshBasicMaterial color={'#ffffff'} toneMapped={false} />
          </mesh>

          {/* data-flow particles drifting +x along spine (6) */}
          <InstancedField
            count={48}
            geo={<sphereGeometry args={[0.05, 8, 8]} />}
            update={(i, o, col) => {
              const rnd = mulberry32(7000 + i * 131);
              const speed = 0.045 + rnd() * 0.05;
              const span = TL_MAXX - TL_MINX;
              const x = TL_MINX + ((rnd() * span + frame * speed) % span);
              const yy = -0.6 + (rnd() - 0.5) * 0.5;
              const zz = (rnd() - 0.5) * 0.6;
              o.position.set(x, yy, zz);
              o.scale.setScalar(0.6 + rnd() * 0.8);
              col.set(accent);
            }}
          />
        </Stage>
      </AbsoluteFill>

      <OverlayLayer opacity={opacity} y={y}>
        <div style={{position: 'absolute', top: 128, left: 150}}>
          <MaskTitle text="2014" start={0.1} size={96} weight={800} color={INK} />
          <div style={{marginTop: 4}}>
            <MaskTitle text="POLICY REVERSAL" start={0.26} size={44} weight={600} color={tok.accentHi} stagger={0.03} />
          </div>
        </div>
      </OverlayLayer>

      <FigureFX />
    </AbsoluteFill>
  );
};

// =====================================================================
// F14 — McLellanParallel (hero, iowa | nc). Two displacement planes.
//   Independent motion elements (>=6):
//     1. left (Iowa) plane slides open leftward   0-24f (Easing.out cubic)
//     2. right (NC) plane slides open rightward    0-24f (Easing.out cubic)
//     3. left plane independent parallax drift (own eased y/x)
//     4. right plane independent parallax drift (different phase)
//     5. central boundary line draws (scaleY grows) then holds w/ marker travel
//     6. red marker travels rightward across the seam (spring)
//   + 2D MaskTitle "IOWA" / "NORTH CAROLINA".
//
//   depth textures: currently a deterministic PROCEDURAL relief (useProcTexture)
//   drives displacement so the plane is genuinely 3D. TODO(depth): swap each
//   plane's map/displacementMap for the dpt-large output of the real slice image
//   (`<slice>_depth.png` from tools/depth/gen_depth.py) once those stills exist —
//   see the two `// TODO(depth-swap)` markers below.
// =====================================================================

const ParallaxPlane: React.FC<{
  tex: THREE.CanvasTexture;
  tint: string;
  x: number;
  driftX: number;
  driftY: number;
}> = ({tex, tint, x, driftX, driftY}) => (
  <mesh position={[x + driftX, driftY, 0]}>
    {/* subdivided so the displacement does not look faceted */}
    <planeGeometry args={[2.4, 3.2, 80, 100]} />
    {/* TODO(depth-swap): map + displacementMap should become the dpt-large depth
        of the real Iowa / NC slice still (near=bright, 0-255, GaussianBlur(2)). */}
    <meshStandardMaterial
      map={tex}
      displacementMap={tex}
      displacementScale={0.55}
      color={tint}
      roughness={0.85}
      metalness={0.05}
    />
  </mesh>
);

export const McLellanParallel: React.FC<FigureProps> = (p) => {
  const frame = useCurrentFrame();
  const {fps, width, height} = useVideoConfig();
  const {opacity, y} = sceneFade(frame, p.dur);

  const iowa = LANES.iowa;
  const nc = LANES.nc;
  const texL = useProcTexture(140001);
  const texR = useProcTexture(140002);

  const OPEN = sec(fps, 0.4); // 24f @60fps
  const open = ease01(frame, 0, OPEN); // (1)(2)

  // independent parallax drifts (3)(4) — one-directional eased, different phase
  const driftLX = interpolate(frame, [0, p.dur], [0, -0.35], {easing: Easing.out(Easing.cubic), extrapolateRight: 'clamp'});
  const driftLY = interpolate(frame, [0, p.dur], [0, 0.22], {easing: Easing.out(Easing.cubic), extrapolateRight: 'clamp'});
  const driftRX = interpolate(frame, [0, p.dur], [0, 0.35], {easing: Easing.out(Easing.cubic), extrapolateRight: 'clamp'});
  const driftRY = interpolate(frame, [0, p.dur], [0, -0.18], {easing: Easing.out(Easing.cubic), extrapolateRight: 'clamp'});

  const gapX = interpolate(open, [0, 1], [0.0, 1.55]);

  // boundary seam draw (5)
  const seam = spring({frame: frame - sec(fps, 0.35), fps, config: {damping: 24, mass: 1}});

  // red marker travels rightward across the seam (6)
  const markS = spring({frame: frame - sec(fps, 0.6), fps, config: {damping: 16, mass: 1}});
  const markY = interpolate(markS, [0, 1], [-1.7, 1.7]);

  const camDolly = ease01(frame, 0, p.dur, Easing.out(Easing.cubic));
  const camPos: [number, number, number] = [0, 0, 6.6 - camDolly * 0.5];

  return (
    <AbsoluteFill style={{backgroundColor: BG}}>
      <HinderBackdrop accent={iowa.accent} tint={'#12100a'} />
      <AbsoluteFill style={{opacity, transform: `translateY(${y}px)`}}>
        <Stage width={width} height={height} camPos={camPos} look={[0, 0, 0]} accent={nc.accent}>
          <ParallaxPlane tex={texL} tint={iowa.tint} x={-gapX} driftX={driftLX} driftY={driftLY} />
          <ParallaxPlane tex={texR} tint={nc.tint} x={gapX} driftX={driftRX} driftY={driftRY} />

          {/* central boundary line draws then holds (5) */}
          <mesh position={[0, 0, 0.4]} scale={[1, interpolate(seam, [0, 1], [0.0001, 1]), 1]}>
            <boxGeometry args={[0.03, 3.6, 0.03]} />
            <meshBasicMaterial color={INK} transparent opacity={0.7} toneMapped={false} />
          </mesh>

          {/* red marker travelling up the seam (6) */}
          <mesh position={[0, markY, 0.5]}>
            <sphereGeometry args={[0.13, 16, 16]} />
            <meshBasicMaterial color={'#d0505a'} toneMapped={false} />
          </mesh>
          <mesh position={[0, markY, 0.5]}>
            <sphereGeometry args={[0.28, 16, 16]} />
            <meshBasicMaterial color={'#d0505a'} transparent opacity={0.25} toneMapped={false} />
          </mesh>
        </Stage>
      </AbsoluteFill>

      <OverlayLayer opacity={opacity} y={y}>
        <div style={{position: 'absolute', top: 120, left: 130}}>
          <MaskTitle text="IOWA" start={0.1} size={64} weight={800} color={iowa.accentHi} />
        </div>
        <div style={{position: 'absolute', top: 120, right: 130, textAlign: 'right'}}>
          <MaskTitle text="NORTH CAROLINA" start={0.16} size={64} weight={800} color={nc.accentHi} />
        </div>
        <div
          style={{
            position: 'absolute',
            bottom: 90,
            width: '100%',
            textAlign: 'center',
            fontFamily: 'Inter, system-ui, sans-serif',
            fontSize: 26,
            letterSpacing: 6,
            textTransform: 'uppercase',
            color: MUTED,
          }}
        >
          Two owners · one federal law
        </div>
      </OverlayLayer>

      <FigureFX />
    </AbsoluteFill>
  );
};

// =====================================================================
// F14b — McLellanLedger (hero, nc). 3D ledger, instancedMesh(301).
//   Independent motion elements (>=6):
//     1. 301 ledger cells sequentially light up (scale-pop reveal + color latch)
//     2. cumulative ~$2M count-up 0-90f (Easing.out cubic)
//     3. year strip horizontal scroll (2007-2009, CLM-0012)
//     4. per-cell spark burst (second instancedMesh(301), brief pop at light time)
//     5. camera overhead scroll-follow drift
//     6. near ledger-slip plate parallax
//   + 2D MaskTitle "301 DEPOSITS" and "~$2M" counter.
//
//   instancedMesh(301): a single <instancedMesh args={[,,301]}> whose 301 matrices
//   AND colors are rewritten every frame in InstancedField's useLayoutEffect. Cell
//   i sits at grid (i%COLS, i/COLS); its light frame is i*ST where ST is derived so
//   all 301 reveals fit inside the reveal window (the manifest's nominal 4f stagger
//   is compressed — 301*4f would be 1204f, far beyond any cut).
//   Fact numbers frozen: 301 deposits, ~$2M.
// =====================================================================

const LEDGER_N = 301;
const LEDGER_COLS = 23; // 23*14 = 322 slots >= 301

export const McLellanLedger: React.FC<FigureProps> = (p) => {
  const frame = useCurrentFrame();
  const {fps, width, height} = useVideoConfig();
  const accent = resolveAccent({lane: 'nc', accent: p.accent});
  const tok = LANES.nc;
  const {opacity, y} = sceneFade(frame, p.dur);

  const rows = Math.ceil(LEDGER_N / LEDGER_COLS);
  const SX = 0.5;
  const SY = 0.5;
  const revealSpan = Math.max(1, Math.min(p.dur * 0.72, sec(fps, 6)));
  const ST = revealSpan / LEDGER_N; // derived stagger so 301 fit the window

  const COUNT_END = Math.min(sec(fps, 1.5), Math.max(1, p.dur - 6)); // ~90f @60
  const countP = ease01(frame, 0, COUNT_END);
  const dollarsM = 2.0 * countP; // ~$2M frozen

  const litColor = React.useMemo(() => new THREE.Color(tok.accentHi), [tok.accentHi]);
  const dimColor = React.useMemo(() => new THREE.Color('#12281f'), []);
  const sparkColor = React.useMemo(() => new THREE.Color('#ffffff'), []);

  const cellPos = (i: number): [number, number] => {
    const gx = i % LEDGER_COLS;
    const gy = Math.floor(i / LEDGER_COLS);
    return [(gx - (LEDGER_COLS - 1) / 2) * SX, ((rows - 1) / 2 - gy) * SY];
  };

  // camera overhead scroll-follow drift (5)
  const camDrift = interpolate(frame, [0, p.dur], [0, 0.9], {easing: Easing.out(Easing.cubic), extrapolateRight: 'clamp'});
  const camPos: [number, number, number] = [0, 1.4 + camDrift, 7.2];

  // year strip scroll (3)
  const scrollX = interpolate(frame, [0, p.dur], [0, -520], {easing: Easing.out(Easing.cubic), extrapolateRight: 'clamp'});
  const years = ['2007', '2008', '2009', '2007', '2008', '2009', '2007', '2008', '2009'];

  return (
    <AbsoluteFill style={{backgroundColor: BG}}>
      <HinderBackdrop accent={accent} tint={tok.tint} />
      <AbsoluteFill style={{opacity, transform: `translateY(${y}px)`}}>
        <Stage width={width} height={height} camPos={camPos} look={[0, 0, 0]} accent={accent} fov={44}>
          {/* 301 ledger cells (1) */}
          <InstancedField
            count={LEDGER_N}
            geo={<boxGeometry args={[SX * 0.78, SY * 0.78, 0.16]} />}
            update={(i, o, col) => {
              const [px, py] = cellPos(i);
              const s = spring({frame: frame - i * ST, fps, config: {damping: 12, mass: 0.6}});
              const pop = interpolate(s, [0, 0.5, 1], [0.0001, 1.28, 1]); // scale reveal (not opacity)
              o.position.set(px, py, 0);
              o.scale.set(pop, pop, Math.max(0.0001, s));
              col.copy(dimColor).lerp(litColor, Math.min(1, s * 1.4));
            }}
          />
          {/* per-cell spark burst (4) */}
          <InstancedField
            count={LEDGER_N}
            geo={<sphereGeometry args={[0.09, 8, 8]} />}
            update={(i, o, col) => {
              const [px, py] = cellPos(i);
              const lf = i * ST;
              const b = interpolate(frame, [lf, lf + 3, lf + 11], [0, 1, 0], {
                extrapolateLeft: 'clamp',
                extrapolateRight: 'clamp',
              });
              o.position.set(px, py, 0.22);
              o.scale.setScalar(0.0001 + b * 1.4);
              col.copy(sparkColor);
            }}
          />
          {/* near ledger-slip plate parallax (6) */}
          <NearPlate frame={frame} dur={p.dur} color={accent} x={-3.4} y={-1.9} z={2.4} amp={0.6} />
        </Stage>
      </AbsoluteFill>

      <OverlayLayer opacity={opacity} y={y}>
        <div style={{position: 'absolute', top: 118, left: 150}}>
          <MaskTitle text="301 DEPOSITS" start={0.1} size={72} weight={800} color={INK} />
          <div style={{marginTop: 4}}>
            <MaskTitle text="OVER THREE YEARS" start={0.26} size={34} weight={600} color={tok.accentHi} stagger={0.03} />
          </div>
        </div>
        {/* ~$2M count-up (2) */}
        <div
          style={{
            position: 'absolute',
            top: 150,
            right: 160,
            textAlign: 'right',
            fontFamily: 'Inter, system-ui, sans-serif',
            color: INK,
          }}
        >
          <div style={{fontSize: 22, letterSpacing: 6, color: MUTED, textTransform: 'uppercase'}}>Cumulative</div>
          <div style={{fontSize: 120, fontWeight: 800, letterSpacing: -4, color: tok.accentHi, fontVariantNumeric: 'tabular-nums'}}>
            ~${dollarsM.toFixed(2)}M
          </div>
        </div>
        {/* year strip scroll (3) */}
        <div style={{position: 'absolute', bottom: 70, left: 0, width: '100%', overflow: 'hidden', height: 44}}>
          <div
            style={{
              display: 'flex',
              gap: 120,
              transform: `translateX(${scrollX}px)`,
              fontFamily: 'Inter, system-ui, sans-serif',
              fontSize: 30,
              letterSpacing: 10,
              color: MUTED,
              whiteSpace: 'nowrap',
            }}
          >
            {years.map((yr, i) => (
              <span key={i}>{yr}</span>
            ))}
          </div>
        </div>
      </OverlayLayer>

      <FigureFX />
    </AbsoluteFill>
  );
};

// =====================================================================
// F15 — TIGTA-Dots (hero, federal). instancedMesh(278).
//   Independent motion elements (>=6):
//     1. 278 dots assemble from scattered -> grid 0-40f (scale+position reveal)
//     2. spatial green wave flips 253 dots 40-90f (wave-front sweep, "stagger2f")
//     3. 25 red dots latch red (kept, carried by the group parallax — never blink)
//     4. wave-front emissive bar travels rightward with the flip
//     5. camera slow parallax overhead (continuous, one-directional)
//     6. background relief plate drift (one-directional eased)
//   + 2D MaskTitle "278 SAMPLED" + "253 / 278 LEGAL SOURCE (91%)" readout.
//
//   instancedMesh(278): one <instancedMesh args={[,,278]}> rewritten each frame.
//   The 25 red indices are chosen by a mulberry32 Fisher-Yates shuffle (deterministic)
//   -> 253 green + 25 red = 278 (253/278 = 91.0%). Numbers frozen: 278 / 91%.
// =====================================================================

const TIGTA_N = 278;
const TIGTA_RED = 25; // 278 - 25 = 253 green ; 253/278 = 91.0%
const TIGTA_COLS = 19; // 19*15 = 285 slots >= 278

export const TIGTADots: React.FC<FigureProps> = (p) => {
  const frame = useCurrentFrame();
  const {width, height} = useVideoConfig();
  const accent = resolveAccent(p);
  const tok = resolveTokens(p);
  const {opacity, y} = sceneFade(frame, p.dur);

  const rows = Math.ceil(TIGTA_N / TIGTA_COLS);
  const SX = 0.6;
  const SY = 0.6;
  const minX = -((TIGTA_COLS - 1) / 2) * SX - 0.4;
  const maxX = ((TIGTA_COLS - 1) / 2) * SX + 0.4;

  // deterministic scatter start + red-set
  const scatter = React.useMemo(() => {
    const r = mulberry32(20250715);
    return Array.from({length: TIGTA_N}, () => [(r() * 2 - 1) * 7, (r() * 2 - 1) * 4, (r() * 2 - 1) * 2.2] as [number, number, number]);
  }, []);
  const redSet = React.useMemo(() => {
    const r = mulberry32(915_2026);
    const idx = Array.from({length: TIGTA_N}, (_, i) => i);
    for (let i = idx.length - 1; i > 0; i--) {
      const j = Math.floor(r() * (i + 1));
      const t = idx[i];
      idx[i] = idx[j];
      idx[j] = t;
    }
    return new Set(idx.slice(0, TIGTA_RED));
  }, []);

  const NEUTRAL = React.useMemo(() => new THREE.Color(tok.accentHi), [tok.accentHi]);
  const GREEN = React.useMemo(() => new THREE.Color('#3fbf7a'), []);
  const RED = React.useMemo(() => new THREE.Color('#d0505a'), []);

  const gridPos = (i: number): [number, number, number] => {
    const gx = i % TIGTA_COLS;
    const gy = Math.floor(i / TIGTA_COLS);
    return [(gx - (TIGTA_COLS - 1) / 2) * SX, ((rows - 1) / 2 - gy) * SY, 0];
  };

  // wave-front x (2)(4): sweeps left->right 40-90f
  const waveFront = interpolate(frame, [40, 90], [minX - 0.3, maxX + 0.3], {
    easing: Easing.out(Easing.cubic),
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  // camera slow parallax overhead (5) — continuous, one-directional
  const camDrift = interpolate(frame, [0, p.dur], [0, 1.2], {easing: Easing.out(Easing.cubic), extrapolateRight: 'clamp'});
  const camPos: [number, number, number] = [camDrift * 0.6, 0.4 + camDrift, 8.2 - camDrift * 0.4];

  const bgTex = useProcTexture(150003);

  const greenCount = Math.round(
    interpolate(waveFront, [minX, maxX], [0, 253], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}),
  );
  const pct = frame >= 40 ? 91 : 0;

  return (
    <AbsoluteFill style={{backgroundColor: BG}}>
      <HinderBackdrop accent={accent} tint={tok.tint} />
      <AbsoluteFill style={{opacity, transform: `translateY(${y}px)`}}>
        <Stage width={width} height={height} camPos={camPos} look={[0, 0, 0]} accent={accent} fov={46}>
          {/* background relief plate drift (6) */}
          <mesh position={[0, 0, -3.2 + interpolate(frame, [0, p.dur], [0, 0.4], {extrapolateRight: 'clamp'})]}>
            <planeGeometry args={[16, 10, 40, 26]} />
            <meshStandardMaterial map={bgTex} displacementMap={bgTex} displacementScale={0.5} color={tok.tint} roughness={0.9} />
          </mesh>

          {/* 278 dots: assemble (1) + wave flip (2) + red latch (3) */}
          <InstancedField
            count={TIGTA_N}
            geo={<sphereGeometry args={[0.16, 14, 14]} />}
            update={(i, o, col) => {
              const gp = gridPos(i);
              const sp = scatter[i];
              const gx = i % TIGTA_COLS;
              const delay = gx * 0.8;
              const t = interpolate(frame, [delay, delay + 26], [0, 1], {
                easing: Easing.out(Easing.cubic),
                extrapolateLeft: 'clamp',
                extrapolateRight: 'clamp',
              });
              const px = sp[0] + (gp[0] - sp[0]) * t;
              const py = sp[1] + (gp[1] - sp[1]) * t;
              const pz = sp[2] + (gp[2] - sp[2]) * t;
              o.position.set(px, py, pz);
              o.scale.setScalar(0.2 + 0.8 * t); // scale reveal (not opacity)
              const isRed = redSet.has(i);
              const target = isRed ? RED : GREEN;
              // spatial wave: flip amount ramps as the wave-front passes this column
              const flip = interpolate(gp[0], [waveFront - 0.45, waveFront + 0.1], [1, 0], {
                extrapolateLeft: 'clamp',
                extrapolateRight: 'clamp',
              });
              col.copy(NEUTRAL).lerp(target, flip * t);
            }}
          />

          {/* wave-front emissive bar travels right (4) */}
          <mesh position={[waveFront, 0, 0.3]} scale={[1, interpolate(frame, [38, 46], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}), 1]}>
            <boxGeometry args={[0.06, rows * SY + 0.6, 0.06]} />
            <meshBasicMaterial color={'#5fd1a0'} toneMapped={false} />
          </mesh>
        </Stage>
      </AbsoluteFill>

      <OverlayLayer opacity={opacity} y={y}>
        <div style={{position: 'absolute', top: 118, left: 150}}>
          <MaskTitle text="278 SAMPLED" start={0.1} size={72} weight={800} color={INK} />
          <div style={{marginTop: 4}}>
            <MaskTitle text="TIGTA STRUCTURING REVIEW" start={0.26} size={32} weight={600} color={INK2} stagger={0.028} />
          </div>
        </div>
        <div
          style={{
            position: 'absolute',
            bottom: 96,
            left: 150,
            fontFamily: 'Inter, system-ui, sans-serif',
            color: INK,
          }}
        >
          <div style={{fontSize: 22, letterSpacing: 6, color: MUTED, textTransform: 'uppercase'}}>Legal-source funds</div>
          <div style={{fontSize: 96, fontWeight: 800, letterSpacing: -3, color: '#5fd1a0', fontVariantNumeric: 'tabular-nums'}}>
            {greenCount} / 278 <span style={{fontSize: 56, color: INK2}}>({pct}%)</span>
          </div>
        </div>
      </OverlayLayer>

      <FigureFX />
    </AbsoluteFill>
  );
};
