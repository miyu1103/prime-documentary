import React from 'react';
import {
  AbsoluteFill,
  Img,
  interpolate,
  OffthreadVideo,
  Sequence,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import {Trail} from '@remotion/motion-blur';
import {BRAND} from '../brand';
import {KineticType} from '../components/KineticType';
import {CitationLowerThird} from '../components/CitationLowerThird';
import {Grain} from '../components/Grain';
import {Particles, LightSweep, Vignette} from '../components/Motion';

/**
 * MotionSample — 15s proof that PD videos move like film, not a slideshow.
 * Owner-driven rules (2026-07-03): no left→right sweep line, no yellow/gold
 * full-screen wash, no plain zoom/pan-only stills. Motion is carried by real
 * footage (moving stock), floating-card fake-2.5D over blurred self, motion
 * graphics and fast cross-dissolves. fps=30, 1920x1080, 450 frames = 15s.
 * DB Cooper (EP21) theme, reusing already-shot EP21 stills + factory footage.
 */

const {ink, navy, electric, white, silver, gold} = BRAND.color;

export const motionSampleDurationInFrames = (fps: number) => Math.round(fps * 15);

/** Cross-dissolve edges: fade in over `edge` frames and out over `edge` at the end. */
const FadeInOut: React.FC<{edge?: number; children: React.ReactNode}> = ({
  edge = 12,
  children,
}) => {
  const frame = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  const opacity = interpolate(
    frame,
    [0, edge, durationInFrames - edge, durationInFrames],
    [0, 1, 1, 0],
    {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'},
  );
  return <AbsoluteFill style={{opacity}}>{children}</AbsoluteFill>;
};

/** Full-frame moving footage with a cinematic grade. Footage supplies the motion. */
const Footage: React.FC<{
  src: string;
  startFrom?: number;
  grade?: string;
}> = ({src, startFrom = 0, grade = 'brightness(0.72) contrast(1.08) saturate(0.92)'}) => (
  <AbsoluteFill style={{backgroundColor: ink, overflow: 'hidden'}}>
    <OffthreadVideo
      src={staticFile(src)}
      muted
      startFrom={startFrom}
      style={{
        width: '100%',
        height: '100%',
        objectFit: 'cover',
        transform: 'scale(1.05)',
        filter: grade,
      }}
    />
  </AbsoluteFill>
);

/** Continuous slow float — keeps overlaid text/graphics alive after they land. */
const Drift: React.FC<{amp?: number; speed?: number; children: React.ReactNode}> = ({
  amp = 10,
  speed = 0.6,
  children,
}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = (frame / fps) * speed;
  const x = Math.sin(t * Math.PI) * amp;
  const y = Math.cos(t * Math.PI * 0.8) * amp * 0.6;
  return <AbsoluteFill style={{transform: `translate(${x}px, ${y}px)`}}>{children}</AbsoluteFill>;
};

/** Drifting particles + a travelling light pool — layered over footage for extra life. */
const Atmosphere: React.FC<{seed: string; particles?: number; color?: string}> = ({
  seed,
  particles = 34,
  color = electric,
}) => (
  <>
    <LightSweep seed={seed} color={color} />
    <Particles seed={seed} count={particles} color={color} />
  </>
);

/**
 * Fake-2.5D still: a sharp framed "photo card" floats over a blurred, enlarged
 * copy of itself, each drifting the opposite way — real depth without a cutout,
 * and clearly not a flat zoom.
 */
const FloatingCardStill: React.FC<{src: string; seed: string}> = ({src, seed}) => {
  const frame = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  const p = interpolate(frame, [0, durationInFrames], [0, 1]);
  const bgX = interpolate(p, [0, 1], [-56, 56]);
  const bgY = interpolate(p, [0, 1], [-22, 22]);
  const cardX = interpolate(p, [0, 1], [44, -44]);
  const cardY = interpolate(p, [0, 1], [18, -18]);
  const cardRot = interpolate(p, [0, 1], [-2.6, 2.6]);
  const cardScale = interpolate(p, [0, 1], [1.0, 1.07]);
  const enter = spring({frame, fps: 30, config: {damping: 200}});
  const cardIn = interpolate(enter, [0, 1], [40, 0]);
  return (
    <AbsoluteFill style={{backgroundColor: ink, overflow: 'hidden'}}>
      {/* blurred, enlarged background bleed */}
      <AbsoluteFill
        style={{
          transform: `translate(${bgX}px, ${bgY}px) scale(1.45)`,
          filter: 'blur(20px) brightness(0.4) saturate(0.85)',
        }}
      >
        <Img src={staticFile(src)} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
      </AbsoluteFill>
      <LightSweep seed={seed} color={electric} />
      {/* floating sharp photo card */}
      <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center'}}>
        <div
          style={{
            width: '68%',
            height: '72%',
            transform: `translate(${cardX}px, ${cardY + cardIn}px) rotate(${cardRot}deg) scale(${cardScale})`,
            borderRadius: 10,
            overflow: 'hidden',
            border: `1px solid ${silver}44`,
            boxShadow: '0 40px 120px rgba(0,0,0,0.65)',
          }}
        >
          <Img src={staticFile(src)} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
        </div>
      </AbsoluteFill>
      <Particles seed={seed} count={26} color={electric} />
      <Vignette />
    </AbsoluteFill>
  );
};

/** Motion-graphics ransom counter, $0 → $200,000, with motion-blur trail. */
const RansomCounter: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const enter = spring({frame, fps, config: {damping: 14, stiffness: 90, mass: 0.8}});
  // clamp so the spring overshoot never prints e.g. $200,009; round to the nearest $1,000.
  const raw = interpolate(enter, [0, 1], [0, 200000], {extrapolateRight: 'clamp'});
  const value = Math.min(200000, Math.round(raw / 1000) * 1000);
  const y = interpolate(enter, [0, 1], [50, 0]);
  const money = '$' + value.toLocaleString('en-US');
  return (
    <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center'}}>
      <Trail layers={6} lagInFrames={1.4} trailOpacity={0.45}>
        <div
          style={{
            transform: `translateY(${y}px)`,
            color: white,
            fontFamily: BRAND.font.display,
            fontWeight: 900,
            fontSize: 200,
            letterSpacing: -2,
            textShadow: `0 0 50px ${electric}66, 0 6px 24px rgba(0,0,0,0.7)`,
          }}
        >
          {money}
        </div>
      </Trail>
      <div
        style={{
          marginTop: 10,
          color: silver,
          fontFamily: BRAND.font.body,
          fontSize: 34,
          letterSpacing: 8,
          textTransform: 'uppercase',
        }}
      >
        In ransom cash
      </div>
    </AbsoluteFill>
  );
};

const EndTag: React.FC = () => {
  const frame = useCurrentFrame();
  const enter = spring({frame, fps: 30, config: {damping: 200}});
  const y = interpolate(enter, [0, 1], [40, 0]);
  return (
    <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center', gap: 16}}>
      <div
        style={{
          transform: `translateY(${y}px)`,
          opacity: enter,
          color: white,
          fontFamily: BRAND.font.display,
          fontWeight: 900,
          fontSize: 96,
          letterSpacing: -1,
          textTransform: 'uppercase',
          textAlign: 'center',
          lineHeight: 1.0,
        }}
      >
        The Cooper
        <br />
        Vanishing
      </div>
      <div
        style={{
          opacity: enter,
          color: gold,
          fontFamily: BRAND.font.body,
          fontSize: 30,
          letterSpacing: 10,
          textTransform: 'uppercase',
        }}
      >
        Prime Documentary
      </div>
    </AbsoluteFill>
  );
};

export const MotionSample: React.FC = () => {
  return (
    <AbsoluteFill style={{backgroundColor: ink}}>
      {/* S1 hook — storm, the date lands (0–96, 3.2s) */}
      <Sequence from={0} durationInFrames={96} name="Hook">
        <FadeInOut>
          <Footage src="sample/storm.mp4" startFrom={40} grade="brightness(0.5) contrast(1.15) saturate(0.7)" />
          <Atmosphere seed="hook" particles={30} color={silver} />
          <Drift amp={9}>
            <KineticType
              transparent
              lines={[
                {text: 'November 24, 1971', at: 6},
                {text: 'A man vanished into the sky', at: 34, emphasis: true},
              ]}
            />
          </Drift>
          <Vignette />
        </FadeInOut>
      </Sequence>

      {/* S2 airport — he boards (88–184, 3.2s) */}
      <Sequence from={88} durationInFrames={96} name="Board">
        <FadeInOut>
          <Footage src="sample/airport.mp4" startFrom={90} />
          <Atmosphere seed="board" particles={26} />
          <Drift amp={8}>
            <KineticType
              transparent
              align="flex-start"
              lines={[
                {text: 'He bought a one-way', at: 10},
                {text: 'ticket to Seattle', at: 24},
              ]}
            />
          </Drift>
          <Vignette />
        </FadeInOut>
      </Sequence>

      {/* S3 money — motion-graphics counter, then bills (176–272, 3.2s) */}
      <Sequence from={176} durationInFrames={96} name="Ransom">
        <FadeInOut>
          <Sequence from={0} durationInFrames={58} name="cash">
            <Footage src="sample/cash.mp4" startFrom={120} grade="brightness(0.52) contrast(1.14) saturate(0.45)" />
            <Atmosphere seed="cash" particles={22} />
            <RansomCounter />
            <Vignette />
          </Sequence>
          <Sequence from={58} durationInFrames={38} name="bills">
            <Footage src="sample/bills.mp4" startFrom={30} />
            <Atmosphere seed="bills" particles={22} />
            <Drift amp={7}>
              <KineticType transparent lines={[{text: 'Then he demanded a parachute', at: 4}]} />
            </Drift>
            <Vignette />
          </Sequence>
        </FadeInOut>
      </Sequence>

      {/* S4 floating-card 2.5D still + citation (264–364, 3.3s — the depth showcase) */}
      <Sequence from={264} durationInFrames={100} name="Still2D">
        <FadeInOut>
          <FloatingCardStill src="sample/img18.png" seed="cooper-still" />
          <CitationLowerThird label="Flight 305 — Seattle, 1971" source="FBI case NORJAK (unsolved)" />
        </FadeInOut>
      </Sequence>

      {/* S5 finale — forest jump → city-night end tag (356–450, 3.1s) */}
      <Sequence from={356} durationInFrames={94} name="Finale">
        <FadeInOut>
          <Sequence from={0} durationInFrames={52} name="jump">
            <Footage src="sample/forest.mp4" startFrom={30} grade="brightness(0.55) contrast(1.12) saturate(0.85)" />
            <Atmosphere seed="forest" particles={30} color={silver} />
            <Drift amp={8}>
              <KineticType transparent lines={[{text: 'Somewhere over the forest', at: 6}]} />
            </Drift>
            <VanishWord />
            <Vignette />
          </Sequence>
          <Sequence from={52} durationInFrames={42} name="tag">
            <Footage src="sample/citynight.mp4" startFrom={100} grade="brightness(0.4) contrast(1.1) saturate(0.9)" />
            <Atmosphere seed="tag" particles={26} />
            <EndTag />
            <Vignette />
          </Sequence>
        </FadeInOut>
      </Sequence>

      {/* grain over the whole piece */}
      <Grain />
    </AbsoluteFill>
  );
};

/** "VANISHED" flies in fast with a motion-blur trail. */
const VanishWord: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const enter = spring({frame: frame - 24, fps, config: {damping: 16, stiffness: 120, mass: 0.9}});
  const x = interpolate(enter, [0, 1], [220, 0]);
  const opacity = interpolate(frame, [24, 34], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center', marginTop: 90}}>
      <Trail layers={8} lagInFrames={1.6} trailOpacity={0.4}>
        <div
          style={{
            transform: `translateX(${x}px)`,
            opacity,
            color: white,
            fontFamily: BRAND.font.display,
            fontWeight: 900,
            fontSize: 190,
            letterSpacing: 4,
            textTransform: 'uppercase',
            textShadow: '0 6px 30px rgba(0,0,0,0.7)',
          }}
        >
          Vanished
        </div>
      </Trail>
    </AbsoluteFill>
  );
};
