/**
 * A tiny, fully deterministic stand-in for a CaseFilm, used only to prove
 * scripts/pd_splice_cuts.py end to end without spending a 31-minute render.
 *
 * It reproduces the three things the splicer depends on, and nothing else:
 *   1. the same frame math as CaseFilm -- lead frames in front, body cuts placed at
 *      `lead + Math.round(cut.start * fps)` for `Math.round(cut.dur * fps)` frames,
 *   2. a real audio master inside the body, so the spliced file has an audio stream
 *      that must survive bit-identical,
 *   3. per-cut picture that depends ONLY on the cut's own `src` and index, so changing
 *      one cut's src changes that cut's pixels and provably nothing else.
 *
 * Deterministic by construction: no Math.random, no Date, every value is a function of
 * the frame number and the cut index (the repo-wide rule -- see the Math.random ban in
 * components/motionkit). Determinism is what makes a spliced master equal to a full
 * re-render, so it is verified empirically by the demo, not assumed here.
 *
 * Rendered with its own entry point so Root.tsx -- and therefore every real episode
 * composition -- is untouched:
 *   cd remotion && npx remotion render src/splicedemo_index.tsx SpliceDemo out.mp4 \
 *       --public-dir=public_splicedemo
 */
import React from 'react';
import {
  AbsoluteFill,
  Audio,
  Composition,
  Sequence,
  interpolate,
  registerRoot,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import demoFilm from './data/splicedemo_film.json';

type DemoCut = {
  id: string;
  start: number;
  dur: number;
  kind: string;
  src: string;
  seed: string;
  act: string;
};

type DemoFilm = {
  fps: number;
  narration: string;
  narrationSeconds: number;
  hookSeconds: number;
  leadSeconds?: number;
  endcardSeconds: number;
  cuts: DemoCut[];
};

const film = demoFilm as unknown as DemoFilm;

/** Same rule as CaseFilm.caseFilmLeadFrames. */
export const demoLeadFrames = (data: DemoFilm, fps: number) =>
  data.leadSeconds == null
    ? Math.round((data.hookSeconds || 0) * fps) + Math.round(3.5 * fps)
    : Math.round(data.leadSeconds * fps);

export const demoDurationInFrames = (data: DemoFilm, fps: number) =>
  demoLeadFrames(data, fps) +
  Math.ceil(data.narrationSeconds * fps) +
  Math.round(data.endcardSeconds * fps);

/** mulberry32 -- deterministic PRNG, seeded from the cut's own src string. */
const seedOf = (s: string) => {
  let h = 2166136261;
  for (let i = 0; i < s.length; i += 1) {
    h ^= s.charCodeAt(i);
    h = Math.imul(h, 16777619);
  }
  return h >>> 0;
};

const mulberry32 = (a: number) => () => {
  a |= 0;
  a = (a + 0x6d2b79f5) | 0;
  let t = Math.imul(a ^ (a >>> 15), 1 | a);
  t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
  return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
};

const PALETTE: Record<string, [string, string]> = {
  'panel/amber': ['#3a2a08', '#f0a92b'],
  'panel/teal': ['#062b2b', '#2bd0c4'],
  'panel/crimson': ['#330a12', '#e04060'],
  'panel/violet': ['#1d0f36', '#9a6cf0'],
  'panel/olive': ['#1f2408', '#a8c23a'],
  'panel/slate': ['#101820', '#7f9ab5'],
  'panel/rust': ['#2e1206', '#d4661f'],
  'panel/indigo': ['#0b1030', '#4f6bff'],
};

const Panel: React.FC<{cut: DemoCut; index: number}> = ({cut, index}) => {
  const frame = useCurrentFrame();
  const {fps, width, height} = useVideoConfig();
  const [bg, fg] = PALETTE[cut.src] ?? ['#000000', '#ffffff'];
  const rnd = mulberry32(seedOf(cut.src) + index);
  const tiles = new Array(48).fill(0).map(() => ({
    x: rnd(),
    y: rnd(),
    s: rnd(),
    p: rnd(),
  }));
  const t = frame / fps;
  // eased, never linear
  const rise = interpolate(frame, [0, Math.round(fps * 0.5)], [0, 1], {
    extrapolateRight: 'clamp',
    easing: (x) => 1 - Math.pow(1 - x, 3),
  });
  return (
    <AbsoluteFill style={{backgroundColor: bg, overflow: 'hidden', opacity: rise}}>
      {tiles.map((tile, i) => {
        const size = 40 + tile.s * 190;
        const drift = Math.sin(t * (0.7 + tile.p * 1.6) + tile.x * 6.283) * 90;
        const lift = Math.cos(t * (0.5 + tile.s * 1.1) + tile.y * 6.283) * 70;
        return (
          <div
            key={i}
            style={{
              position: 'absolute',
              left: tile.x * width - size / 2 + drift,
              top: tile.y * height - size / 2 + lift,
              width: size,
              height: size,
              borderRadius: 8 + tile.p * 40,
              border: `${2 + Math.round(tile.s * 5)}px solid ${fg}`,
              opacity: 0.18 + 0.5 * tile.p * rise,
              transform: `rotate(${(t * (18 + tile.p * 40)).toFixed(4)}deg) scale(${(
                0.85 +
                0.25 * rise
              ).toFixed(4)})`,
            }}
          />
        );
      })}
      <AbsoluteFill
        style={{
          alignItems: 'center',
          justifyContent: 'center',
          color: fg,
          fontFamily: 'Arial, sans-serif',
          fontWeight: 800,
          letterSpacing: 6,
        }}
      >
        <div
          style={{
            fontSize: 92,
            transform: `translateY(${((1 - rise) * 60).toFixed(3)}px)`,
            opacity: rise,
          }}
        >
          {cut.src.toUpperCase()}
        </div>
        <div style={{fontSize: 40, opacity: 0.75 * rise, marginTop: 18}}>{cut.id}</div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

const Slate: React.FC<{label: string}> = ({label}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const glow = 0.4 + 0.3 * Math.sin((frame / fps) * 2.2);
  return (
    <AbsoluteFill
      style={{
        backgroundColor: '#05070c',
        alignItems: 'center',
        justifyContent: 'center',
        color: `rgba(220,230,245,${glow.toFixed(4)})`,
        fontFamily: 'Arial, sans-serif',
        fontSize: 72,
        letterSpacing: 12,
        fontWeight: 700,
      }}
    >
      {label}
    </AbsoluteFill>
  );
};

const Bed: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  return (
    <AbsoluteFill
      style={{
        background: `radial-gradient(120% 90% at ${(50 + 18 * Math.sin(t * 0.8)).toFixed(3)}% ${(
          46 + 12 * Math.cos(t * 0.6)
        ).toFixed(3)}%, #16283f 0%, #05070c 78%)`,
      }}
    />
  );
};

const SpliceDemo: React.FC = () => {
  const {fps} = useVideoConfig();
  const lead = demoLeadFrames(film, fps);
  const body = Math.ceil(film.narrationSeconds * fps);
  const ed = Math.round(film.endcardSeconds * fps);
  return (
    <AbsoluteFill style={{backgroundColor: '#05070c'}}>
      {lead > 0 && (
        <Sequence from={0} durationInFrames={lead} name="Lead">
          <Slate label="LEAD" />
        </Sequence>
      )}
      <Sequence from={lead} durationInFrames={body} name="Body">
        <Audio src={staticFile(film.narration)} />
        {/* Persistent ambient bed, like CaseFilm's AmbientMotion/BodyGrade layers. With the
            panels fading in over it (opacity: rise), a cut boundary is a gradual change rather
            than a hard scene change, so x264 does NOT place a keyframe on every cut -- which is
            what makes the splicer's GOP snapping do real work in this fixture. */}
        <Bed />
        {film.cuts.map((c, i) => (
          <Sequence
            key={c.id}
            from={Math.round(c.start * fps)}
            durationInFrames={Math.max(1, Math.round(c.dur * fps))}
            name={`cut-${i}`}
          >
            <Panel cut={c} index={i} />
          </Sequence>
        ))}
      </Sequence>
      <Sequence from={lead + body} durationInFrames={ed} name="Endcard">
        <Slate label="END" />
      </Sequence>
    </AbsoluteFill>
  );
};

const DemoRoot: React.FC = () => (
  <Composition
    id="SpliceDemo"
    component={SpliceDemo}
    durationInFrames={demoDurationInFrames(film, film.fps)}
    fps={film.fps}
    width={1920}
    height={1080}
  />
);

registerRoot(DemoRoot);
