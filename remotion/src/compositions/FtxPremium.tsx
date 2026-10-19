import React from 'react';
import {
  AbsoluteFill,
  Img,
  Sequence,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import {BRAND} from '../brand';
import {BrandEndcard, BrandOpening} from '../components/Bookends';
import {Grain} from '../components/Grain';
import {LightSweep, Particles, Vignette} from '../components/Motion';
import {FTX_DURATION_SEC, FTX_SHOTS, type FtxShot} from '../data/ftx_premium';

const INK = BRAND.color.ink;
const GOLD = BRAND.color.gold;
const WHITE = BRAND.color.white;
const SILVER = BRAND.color.silver;
const ELECTRIC = BRAND.color.electric;

const OPENING_FROM_SEC = 15.949;
const OPENING_DUR_SEC = 4.87;

const hash01 = (s: string): number => {
  let h = 2166136261;
  for (let i = 0; i < s.length; i += 1) {
    h ^= s.charCodeAt(i);
    h = Math.imul(h, 16777619);
  }
  return ((h >>> 0) % 100000) / 100000;
};

const LuxuryCamera: React.FC<{seed: string; durationSec: number; children: React.ReactNode}> = ({seed, durationSec, children}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const durationInFrames = Math.max(1, Math.round(durationSec * fps));
  const raw = interpolate(frame, [0, durationInFrames], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const p = 0.5 - Math.cos(raw * Math.PI) / 2;
  const a = hash01(seed);
  const b = hash01(`${seed}-b`);
  const pushIn = a > 0.42;
  const scale = interpolate(p, [0, 1], pushIn ? [1.065, 1.18] : [1.18, 1.07]);
  const x = interpolate(p, [0, 1], [(a - 0.5) * -72, (a - 0.5) * 72]);
  const y = interpolate(p, [0, 1], [(b - 0.5) * -42, (b - 0.5) * 42]);
  const rotate = interpolate(p, [0, 1], [(a - 0.5) * -0.22, (a - 0.5) * 0.22]);
  return (
    <AbsoluteFill style={{transform: `translate(${x}px, ${y}px) scale(${scale}) rotate(${rotate}deg)`, transformOrigin: '50% 47%'}}>
      {children}
    </AbsoluteFill>
  );
};

const CinematicPlate: React.FC<{shot: FtxShot}> = ({shot}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const p = interpolate(frame, [0, Math.max(1, Math.round(shot.durationSec * fps))], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const glow = 0.08 + 0.04 * Math.sin(p * Math.PI * 2 + hash01(shot.id) * Math.PI);
  if (!shot.src) {
    return <AbsoluteFill style={{backgroundColor: INK}} />;
  }
  return (
    <AbsoluteFill style={{backgroundColor: INK, overflow: 'hidden'}}>
      <Img
        src={staticFile(shot.src)}
        style={{
          width: '100%',
          height: '100%',
          objectFit: 'cover',
          transform: 'scale(1.12)',
          filter: 'blur(18px) contrast(1.05) saturate(0.8) brightness(0.42)',
          opacity: 0.62,
        }}
      />
      <LuxuryCamera seed={shot.id} durationSec={shot.durationSec}>
        <Img
          src={staticFile(shot.src)}
          style={{
            width: '100%',
            height: '100%',
            objectFit: 'cover',
            filter: 'contrast(1.06) saturate(0.9) brightness(0.84)',
          }}
        />
      </LuxuryCamera>
      <AbsoluteFill style={{background: `linear-gradient(90deg, ${INK}7A 0%, transparent 30%, transparent 72%, ${INK}88 100%)`}} />
      <AbsoluteFill style={{background: `radial-gradient(48% 42% at ${44 + hash01(`${shot.id}-x`) * 18}% ${28 + hash01(`${shot.id}-y`) * 18}%, rgba(69, 255, 202, ${glow}) 0%, transparent 72%)`}} />
      <LightSweep seed={shot.id} color={shot.section === 'actII_code' ? '#39ff8a' : ELECTRIC} />
      <Particles seed={shot.id} count={shot.kind === 'image' ? 6 : 10} color={shot.section === 'actIII_run' ? GOLD : ELECTRIC} />
      <Vignette strength={0.9} />
    </AbsoluteFill>
  );
};

const TextReveal: React.FC<{lines: string[]; align?: 'center' | 'left'}> = ({lines, align = 'left'}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  return (
    <AbsoluteFill
      style={{
        justifyContent: align === 'center' ? 'center' : 'flex-start',
        alignItems: align === 'center' ? 'center' : 'flex-start',
        padding: align === 'center' ? '0 72px 150px' : '128px 72px 230px',
      }}
    >
      {lines.map((line, i) => {
        const s = spring({frame: frame - i * Math.round(0.18 * fps), fps, config: {damping: 18, stiffness: 110}});
        return (
          <div
            key={line}
            style={{
              opacity: Math.min(1, s * 1.25),
              transform: `translateY(${interpolate(s, [0, 1], [26, 0])}px)`,
              color: i === 0 ? WHITE : GOLD,
              fontFamily: BRAND.font.display,
              fontWeight: 900,
              fontSize: i === 0 ? 60 : 42,
              lineHeight: 1.02,
              letterSpacing: 0,
              textTransform: 'uppercase',
              textShadow: `0 0 32px ${INK}, 0 0 26px ${GOLD}44`,
              borderLeft: align === 'left' && i === 0 ? `4px solid ${GOLD}` : undefined,
              paddingLeft: align === 'left' && i === 0 ? 18 : 0,
              maxWidth: 1060,
            }}
          >
            {line}
          </div>
        );
      })}
    </AbsoluteFill>
  );
};

const CodeOverlay: React.FC = () => {
  const frame = useCurrentFrame();
  const glow = interpolate(Math.sin(frame * 0.06), [-1, 1], [0.32, 0.72]);
  return (
    <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center'}}>
      <div
        style={{
          width: 980,
          padding: '34px 42px',
          background: `${INK}DE`,
          border: `1px solid #39ff8a88`,
          boxShadow: `0 0 ${24 + glow * 18}px #39ff8a44`,
          fontFamily: 'Consolas, monospace',
          color: '#b8ffcf',
          fontSize: 46,
          lineHeight: 1.35,
        }}
      >
        <span style={{color: '#6a7b80'}}>if account == </span>
        <span style={{color: GOLD}}>ALAMEDA</span>
        <br />
        <span style={{color: '#39ff8a'}}>allow_negative = true</span>
      </div>
    </AbsoluteFill>
  );
};

const StampOverlay: React.FC<{text: string}> = ({text}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const s = spring({frame: frame - Math.round(0.3 * fps), fps, config: {damping: 10, stiffness: 160}});
  return (
    <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center'}}>
      <div
        style={{
          transform: `scale(${interpolate(s, [0, 1], [2.2, 1])}) rotate(-7deg)`,
          opacity: Math.min(1, s * 1.3),
          color: '#ff3b30',
          border: '10px solid #ff3b30',
          padding: '24px 42px',
          fontFamily: BRAND.font.display,
          fontSize: 112,
          fontWeight: 900,
          letterSpacing: 4,
          textTransform: 'uppercase',
          background: `${INK}66`,
          boxShadow: `0 0 40px #ff3b3066`,
        }}
      >
        {text}
      </div>
    </AbsoluteFill>
  );
};

const Disclosure: React.FC = () => (
  <AbsoluteFill style={{justifyContent: 'flex-start', alignItems: 'flex-end', padding: '28px 32px'}}>
    <div style={{fontFamily: BRAND.font.body, color: SILVER, fontSize: 16, background: `${INK}B8`, border: `1px solid ${SILVER}44`, padding: '6px 10px', borderRadius: 4}}>
      symbolic AI reconstruction — not real footage
    </div>
  </AbsoluteFill>
);

const ShotStage: React.FC<{shot: FtxShot}> = ({shot}) => {
  if (shot.kind === 'endcard') {
    return <BrandEndcard />;
  }
  return (
    <AbsoluteFill style={{backgroundColor: INK}}>
      <CinematicPlate shot={shot} />
      {shot.kind === 'code' ? <CodeOverlay /> : null}
      {shot.kind === 'stamp' ? <StampOverlay text="GUILTY" /> : null}
      {shot.kind === 'quote' ? <TextReveal lines={shot.overlay ?? []} align="center" /> : null}
      {shot.kind === 'image' && shot.overlay ? <TextReveal lines={shot.overlay} /> : null}
      <Disclosure />
    </AbsoluteFill>
  );
};

export const FtxPremium: React.FC = () => {
  const {fps} = useVideoConfig();
  return (
    <AbsoluteFill style={{backgroundColor: INK}}>
      {FTX_SHOTS.map((shot) => (
        <Sequence key={shot.id} from={Math.round(shot.fromSec * fps)} durationInFrames={Math.max(1, Math.round(shot.durationSec * fps))}>
          <ShotStage shot={shot} />
        </Sequence>
      ))}
      <Sequence from={Math.round(OPENING_FROM_SEC * fps)} durationInFrames={Math.round(OPENING_DUR_SEC * fps)}>
        <BrandOpening
          seriesLabel="How the System Really Works · No. 4"
          title="FTX"
          subtitle="The hidden door behind the $8 billion collapse"
        />
      </Sequence>
      <Grain opacity={0.026} />
    </AbsoluteFill>
  );
};

export const ftxPremiumDurationInFrames = (fps: number): number => Math.round(FTX_DURATION_SEC * fps);
